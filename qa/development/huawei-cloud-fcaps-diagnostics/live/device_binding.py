#!/usr/bin/env python3
"""Verify the documented Huawei virtio/VBD branch, never generalize it to SCSI/WWN."""
import argparse,datetime,hashlib,importlib.util,json,subprocess
from pathlib import Path
spec=importlib.util.spec_from_file_location('cloud',Path(__file__).with_name('cloud.py'));cloud=importlib.util.module_from_spec(spec);spec.loader.exec_module(cloud)

def bind_virtio(volume_id,attachments,devices):
 selected=[a for a in attachments if a.get('volumeId')==volume_id]
 if len(selected)!=1 or selected[0].get('bus')!='virtio':raise ValueError('Requires exactly one selected virtio attachment')
 prefix=volume_id[:20]
 if len(prefix)!=20 or len([a for a in attachments if a.get('volumeId','')[:20]==prefix])!=1:raise ValueError('Ambiguous volume serial prefix')
 matches=[d for d in devices if d.get('DEVTYPE')=='disk' and d.get('ID_SERIAL')==prefix and '/virtio' in d.get('DEVPATH','')]
 if len(matches)!=1:raise ValueError('Requires exactly one whole-disk serial match')
 pci=selected[0].get('pciAddress');path=matches[0].get('ID_PATH','')
 if pci and path!='pci-'+pci:raise ValueError('PCI identity does not match the selected cloud attachment')
 return matches[0]['DEVNAME']

def main():
 p=argparse.ArgumentParser();p.add_argument('--context',type=Path,required=True);p.add_argument('--host',required=True);p.add_argument('--skill',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();c=json.loads(a.context.read_text())
 args=['hcloud','ECS','ListServerBlockDevices/v2','--cli-profile='+c['profile'],'--cli-region='+c['region'],'--project_id='+c['project_id'],'--server_id='+c['server_id']]
 result=subprocess.run(args,capture_output=True,text=True,timeout=40);data=cloud.decode_response(result.stdout)
 if result.returncode or 'volumeAttachments' not in data:raise SystemExit('Cloud block-device query failed')
 program="""import subprocess,json
root=json.loads(subprocess.check_output(['lsblk','--json','--nodeps','--output','PATH,TYPE'],text=True))
rows=[]
for d in root['blockdevices']:
 if d['type']!='disk':continue
 p=subprocess.run(['udevadm','info','--query=property','--name='+d['path']],capture_output=True,text=True,check=True)
 rows.append(dict(line.split('=',1) for line in p.stdout.splitlines() if '=' in line))
print(json.dumps(rows))
"""
 import shlex
 remote=subprocess.run(['ssh','-o','BatchMode=yes','-o','ControlPath=/tmp/fcaps-ssh-%C','root@'+a.host,'python3 -c '+shlex.quote(program)],capture_output=True,text=True,timeout=30)
 if remote.returncode:raise SystemExit('Cannot read target udev identities')
 devices=json.loads(remote.stdout);bound=[]
 for vid in c['volume_ids']:
  device=bind_virtio(vid,data['volumeAttachments'],devices);bound.append({'device':device,'volume_serial_matches':True,'pci_matches':True})
 section=(a.skill/'references/helpers.md').read_text().split('## H-device\n',1)[1].split('\n## ',1)[0]
 out={'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'helper':'H-device','status':'passed','scope':'current ECS virtio/VBD attachments only; no SCSI/WWN/XEN inference','bindings':bound,'cloud_response_sha256':hashlib.sha256(result.stdout.encode()).hexdigest(),'host_response_sha256':hashlib.sha256(remote.stdout.encode()).hexdigest(),'helper_sha256':hashlib.sha256(section.encode()).hexdigest()}
 a.output.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');a.output.chmod(0o600);print('PASS H-device:',len(bound),'unique virtio serial + PCI mappings')

if __name__=='__main__':main()
