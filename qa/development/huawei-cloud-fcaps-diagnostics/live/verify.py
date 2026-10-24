#!/usr/bin/env python3
"""Run bounded Linux queries over an existing SSH connection; credentials stay outside files.

Pre-write: --catalog contains reviewed candidates. Post-write: --skill reads canonical
Markdown commands. Conditional capture/trace/scans are never auto-executed.
"""
import argparse, datetime, hashlib, json, re, shlex, subprocess
from pathlib import Path

def contracts(skill):
    rows=[]
    for p in sorted((skill/'references/commands').rglob('*.md')):
        for line in p.read_text().splitlines():
            m=re.match(r'^\| `(LINUX|WINDOWS|KUBERNETES)/([^`]+)`<br>`(.+?)` \| ',line)
            if m:
                rows.append(dict(id=m[1]+'/'+m[2],env=m[1].lower(),command=m[3].replace('\\|','|'),file=str(p.relative_to(skill)),row_sha256=hashlib.sha256(line.encode()).hexdigest()))
    return rows

REMOTE=r'''
import json,sys,subprocess,shlex,datetime,hashlib,platform,os
request=json.load(sys.stdin)
def call(argv,timeout=25):
 try:
  p=subprocess.run(argv,capture_output=True,text=True,errors='replace',timeout=timeout,env={**os.environ,'LC_ALL':'C','SYSTEMD_COLORS':'0'})
  return dict(exit_code=p.returncode,stdout=p.stdout,stderr=p.stderr)
 except FileNotFoundError:return dict(exit_code=127,stdout='',stderr='tool unavailable')
 except subprocess.TimeoutExpired:return dict(exit_code=124,stdout='',stderr='runner timeout; no complete result')
now=datetime.datetime.now(datetime.timezone.utc)
routes=call(['ip','-json','route','show','default'])
iface=next((x['dev'] for x in json.loads(routes['stdout'] or '[]') if x.get('dev')),None)
units=call(['systemctl','list-units','--type=service','--all','--no-pager','--plain','--no-legend'])['stdout']
unit=next((u for u in ['ssh.service','sshd.service'] if u in units),'systemd-journald.service')
bindings={'unit':unit,'start':(now-datetime.timedelta(minutes=15)).strftime('%Y-%m-%d %H:%M:%S UTC'),'end':now.strftime('%Y-%m-%d %H:%M:%S UTC'),'path':'/','iface':iface,'name':'example.com'}
device=call(['findmnt','--target','/','--noheadings','--output','SOURCE'])['stdout'].strip()
parent=call(['lsblk','--nodeps','--noheadings','--output','PKNAME',device])['stdout'].strip() if device.startswith('/dev/') else ''
bindings.update({'device':device,'blockDevice':'/dev/'+parent if parent else device,'target':'127.0.0.1','key':'net.ipv4.tcp_tw_reuse','vulnerability':'spec_rstack_overflow'})
env={'platform':platform.platform(),'os_release':open('/etc/os-release').read(),'uid':os.geteuid(),'versions':{}}
for name,argv in [('systemd',['systemctl','--version']),('sysstat',['iostat','-V']),('iproute2',['ip','-Version']),('util-linux',['lsblk','--version'])]:env['versions'][name]=call(argv)
records=[]
for row in request['rows']:
 cmd=row['command'];cid=row['id'];meta=request['meta'][cid]
 rec={'id':cid,'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'command':cmd,'row_sha256':row.get('row_sha256'),'help':None}
 if meta.get('help'):
  rec['help']=call(shlex.split(meta['help']))
 if not meta.get('live',True):
  rec.update(status='not_run',reason='conditional collection or platform-specific scan; no automatic execution')
 else:
  argv=shlex.split(cmd)
  effective={**bindings,**meta.get('test_bindings',{})}
  for i,a in enumerate(argv):
   for k,v in effective.items():
    if v is not None:a=a.replace('$'+k,str(v))
   argv[i]=a
  if any('$' in a for a in argv):rec.update(status='blocked',reason='unresolved input')
  else:
   out=call(argv);rec.update(out);rec['argv']=argv
   good=out['exit_code']==0;assertions=[]
   key=cid.split('/')[1]
   if good and key in ['addresses','routes','rules','nic-statistics','block-devices','mounts']:
    try:
     obj=json.loads(out['stdout']);good=bool(obj);assertions.append({'name':'structured nonempty output','passed':good})
    except ValueError:good=False
   elif good and key in ['unit-journal','kernel-journal']:
    try:
     events=[json.loads(l) for l in out['stdout'].splitlines() if l.strip()]
     good=all('MESSAGE' in e and '__REALTIME_TIMESTAMP' in e for e in events)
     assertions.append({'name':'journal JSON schema','passed':good})
     if key=='unit-journal':
      good=good and all(e.get('_SYSTEMD_UNIT')==unit or e.get('UNIT')==unit or e.get('OBJECT_SYSTEMD_UNIT')==unit or e.get('COREDUMP_UNIT')==unit for e in events)
      assertions.append({'name':'requested service identity','passed':good})
     rec['event_count']=len(events)
    except ValueError:good=False
   elif good and key=='dns-query':
    good='status: NOERROR' in out['stdout'];assertions.append({'name':'DNS response NOERROR','passed':good})
   elif good and key=='icmp-probe':
    good='3 packets transmitted, 3 received' in out['stdout'];assertions.append({'name':'three loopback replies','passed':good})
   elif good and key=='mtr-report':
    try:
     result=json.loads(out['stdout']);good=bool(result.get('report',{}).get('hubs'))
    except ValueError:good=False
    assertions.append({'name':'structured finite hop report; loopback only','passed':good})
   elif good and key=='metadata-http':
    good=out['stdout'].isdigit() and 100<=int(out['stdout'])<=599;assertions.append({'name':'HTTP response status, no body collected','passed':good})
   elif good and key=='udev-device':
    good='DEVTYPE=disk' in out['stdout'] and 'DEVNAME='+effective['blockDevice'] in out['stdout'];assertions.append({'name':'selected whole-disk identity','passed':good})
   elif good and key=='filesystem-id':
    good='DEVNAME='+effective['device'] in out['stdout'] and 'TYPE=' in out['stdout'];assertions.append({'name':'selected filesystem identity','passed':good})
   elif good and key=='conntrack-capacity':
    good='net.netfilter.nf_conntrack_count =' in out['stdout'] and 'net.netfilter.nf_conntrack_max =' in out['stdout'];assertions.append({'name':'count and maximum present','passed':good})
   elif good:
    good=bool(out['stdout'].strip());assertions.append({'name':'nonempty query output','passed':good})
   rec['assertions']=assertions
   rec['status']='passed' if good else ('blocked' if out['exit_code']==127 else 'failed')
   if good and key in ['unit-journal','kernel-journal'] and rec.get('event_count')==0:rec['status']='empty'
   if key=='cron' and out['exit_code']==1 and 'no crontab' in out['stderr']:rec.update(status='empty',reason='no crontab for current user')
   if key=='deleted-open-files' and out['exit_code']==1 and not out['stdout'].strip() and not out['stderr'].strip():rec.update(status='empty',reason='no unlinked open files in lsof scope')
   if key=='network-manager' and out['exit_code']==10 and 'not running' in out['stderr']:rec.update(status='blocked',reason='NetworkManager daemon is not running')
   if key in ['failed-logins','recent-logins'] and good and not any('pts/' in l or 'tty' in l for l in out['stdout'].splitlines()):rec.update(status='empty',reason='no login rows in retained file')
 rec['evidence_sha256']=hashlib.sha256(json.dumps({k:rec[k] for k in ['stdout','stderr','exit_code'] if k in rec},sort_keys=True).encode()).hexdigest()
 records.append(rec)
print(json.dumps({'environment':env,'records':records}))
'''

def main():
    p=argparse.ArgumentParser();p.add_argument('--catalog',type=Path,required=True);p.add_argument('--skill',type=Path);p.add_argument('--host',required=True);p.add_argument('--user',default='root');p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();catalog=json.loads(a.catalog.read_text());rows=contracts(a.skill) if a.skill else catalog
    request={'rows':[r for r in rows if r['env']=='linux'],'meta':{r['id']:r for r in catalog}}
    argv=['ssh','-o','BatchMode=yes','-o','ConnectTimeout=10','-o','ControlPath=/tmp/fcaps-ssh-%C',a.user+'@'+a.host,'python3 -c '+shlex.quote(REMOTE)]
    started=datetime.datetime.now(datetime.timezone.utc).isoformat()
    result=subprocess.run(argv,input=json.dumps(request),capture_output=True,text=True,timeout=240)
    if result.returncode:raise SystemExit('SSH validation unavailable: '+result.stderr[:300])
    data=json.loads(result.stdout);data['started']=started;data['finished']=datetime.datetime.now(datetime.timezone.utc).isoformat();data['phase']='post-write' if a.skill else 'pre-write'
    a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n');a.output.chmod(0o600)
    from collections import Counter
    print(json.dumps({'phase':data['phase'],'states':dict(Counter(r['status'] for r in data['records'])),'issues':[{'id':r['id'],'status':r['status'],'reason':r.get('reason') or r.get('stderr','')[:180]} for r in data['records'] if r['status'] in ['failed','blocked']]}))

if __name__=='__main__':main()
