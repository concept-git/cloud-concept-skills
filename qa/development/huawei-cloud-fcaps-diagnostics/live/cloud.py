#!/usr/bin/env python3
"""Recheck ten read-only Huawei Cloud resource bindings using an existing local context."""
import argparse,datetime,hashlib,importlib.util,json,re,subprocess
from pathlib import Path

def decode_response(text):
 """Remove only the observed KooCLI update notice; unknown prefixes remain errors."""
 lines=text.lstrip().splitlines()
 while lines and re.fullmatch(r'可执行`hcloud update`更新KooCLI至最新版本\d+(?:\.\d+)+',lines[0]):
  lines.pop(0)
 data=json.loads('\n'.join(lines))
 if not isinstance(data,dict):raise ValueError('Expected an API response object')
 return data

def main():
 p=argparse.ArgumentParser();p.add_argument('--context',type=Path,required=True);p.add_argument('--skill',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
 spec=importlib.util.spec_from_file_location('gate',Path(__file__).parents[1]/'validate.py');gate=importlib.util.module_from_spec(spec);spec.loader.exec_module(gate)
 c=json.loads(a.context.read_text());calls=[];checks=[];started=datetime.datetime.now(datetime.timezone.utc).isoformat()
 def call(service,op,**params):
  args=['hcloud',service,op,'--cli-profile='+c['profile'],'--cli-region='+c['region']]+['--'+k+'='+str(v) for k,v in params.items()]
  x=subprocess.run(args,capture_output=True,text=True,timeout=45)
  try:d=decode_response(x.stdout)
  except ValueError:raise RuntimeError(service+'/'+op+' did not return JSON')
  if x.returncode or 'error' in d or 'error_code' in d:raise RuntimeError(service+'/'+op+' returned an API error')
  calls.append(dict(id=service+'/'+op,status='passed',at=datetime.datetime.now(datetime.timezone.utc).isoformat(),argv=['--cli-region='+c['region']],response_keys=list(d),list_counts={},counts={},error=None,error_code=None,assertions=[],sha256=hashlib.sha256(x.stdout.encode()).hexdigest(),exit_code=x.returncode))
  return d
 def check(name,value):
  checks.append(dict(name=name,passed=bool(value)))
  if not value:raise AssertionError(name)
  calls[-1]['assertions'].append(dict(name=name,passed=True))
 project=c['project_id'];server=c['server_id']
 if len(c['vpc_ids'])!=1 or len(c['volume_ids'])!=1 or len(c['security_group_ids'])!=1:raise RuntimeError('Fixture requires one explicitly selected VPC, volume and security group')
 s=call('ECS','ShowServer/v2',project_id=project,server_id=server)['server'];check('目标 ECS 标识与响应一致',s['id']==server)
 nics=call('ECS','ListServerInterfaces/v2',project_id=project,server_id=server)['interfaceAttachments'];check('ECS 网卡包含可衔接端口',bool(nics) and all(x.get('port_id') for x in nics))
 # Bind the pre-established target port; never silently select the first interface.
 known={x['port_id'] for x in c['ports']};matches=[x for x in nics if x['port_id'] in known]
 if len(matches)!=1:raise RuntimeError('Target interface is ambiguous; select by known IP/MAC before retrying')
 nic=matches[0];port=call('VPC','ShowPort/v3',project_id=project,port_id=nic['port_id'])['port'];check('H-port：ECS port_id 对应 VPC 端口',port['id']==nic['port_id'])
 subnets=call('VPC','ListSubnets/v2',project_id=project,vpc_id=c['vpc_ids'][0])['subnets']
 neutron={x['subnet_id'] for x in nic['fixed_ips']};matches=[x for x in subnets if x.get('neutron_subnet_id') in neutron and x.get('vpc_id')==c['vpc_ids'][0]]
 check('H-subnet：Neutron 子网匹配到唯一 VPC 子网',len(matches)==1)
 sub=call('VPC','ShowSubnet/v2',project_id=project,subnet_id=matches[0]['id'])['subnet'];check('H-subnet：转换后的 VPC 子网 ID 可查询明细',sub['id']==matches[0]['id'])
 sgid=next((x for x in port['security_groups'] if x in c['security_group_ids']),None)
 if not sgid:raise RuntimeError('No known security group binding')
 sg=call('VPC','ShowSecurityGroup/v3',project_id=project,security_group_id=sgid)['security_group'];check('端口安全组标识可查询明细',sg['id']==sgid)
 volumes=s['os-extended-volumes:volumes_attached'];vid=next((x['id'] for x in volumes if x['id'] in c['volume_ids']),None)
 if not vid:raise RuntimeError('No known volume binding')
 v=call('EVS','ShowVolume/v2',project_id=project,volume_id=vid)['volume'];check('H-volume：ECS 挂载盘 ID 可查询 EVS 明细',v['id']==vid and any(x.get('server_id')==server for x in v.get('attachments',[])))
 ips=call('EIP','ListPublicips/v2',project_id=project)['publicips'];matches=[x for x in ips if x.get('port_id')==port['id'] and x.get('id') in c['publicip_ids']];check('H-eip：公网 IP 按 port_id 匹配',len(matches)==1)
 ip=matches[0];public=call('EIP','ShowPublicip/v3',project_id=project,publicip_id=ip['id'])['publicip'];check('H-eip：公网 IP 标识可查询明细',public['id']==ip['id'])
 bandwidth=call('EIP','ShowBandwidth/v2',project_id=project,bandwidth_id=ip['bandwidth_id'])['bandwidth'];check('H-eip：bandwidth_id 可查询对应带宽',bandwidth['id']==ip['bandwidth_id'])
 result=dict(completed=True,started=started,finished=datetime.datetime.now(datetime.timezone.utc).isoformat(),checks=checks,contract_sha256=gate.contract_digest(a.skill),live_calls=calls)
 a.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');a.output.chmod(0o600)
 print('PASS cloud bindings',len(checks),'API calls',len(calls))

if __name__=='__main__':main()
