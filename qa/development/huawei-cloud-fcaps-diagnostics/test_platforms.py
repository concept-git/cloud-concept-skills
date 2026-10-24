#!/usr/bin/env python3
"""Prove that row drift, missing coverage and false live claims are rejected without executing mutations."""
import argparse,json,re,shutil,subprocess,sys,tempfile
from pathlib import Path

def main():
 p=argparse.ArgumentParser();p.add_argument('--skill',type=Path,required=True);p.add_argument('--evidence',type=Path,required=True);a=p.parse_args();qa=Path(__file__).parent
 with tempfile.TemporaryDirectory(prefix='fcaps-platform-gate-') as tmp:
  root=Path(tmp)
  fixture=root/'evidence';fixture.mkdir()
  for f in a.evidence.glob('*.json'):shutil.copyfile(f,fixture/f.name)
  def run(skill,evidence):
   x=subprocess.run([sys.executable,str(qa/'platforms.py'),'--skill',str(skill),'--evidence',str(evidence)],capture_output=True,text=True)
   return x.returncode,json.loads(x.stdout)
  code,report=run(a.skill,fixture);assert code==0,report['errors'];print('PASS baseline')
  tests=[
   ('changed_sampling','references/commands/performance/linux.md','iostat -x -y 1 5','iostat -x 1 5','stale row evidence'),
   ('wrong_target_environment','references/commands/fault/windows.md','WINDOWS/service-status','LINUX/service-status','candidate inventory mismatch'),
   ('wrong_namespace','references/commands/configuration/kubernetes.md','-n "$namespace" get pods','-n default get pods','stale row evidence'),
   ('missing_mode','references/commands/fault/linux.md',r'^\| `LINUX/unit-journal`[^\n]*\n','','candidate inventory mismatch'),
  ]
  for name,rel,old,new,error in tests:
   s=root/name;shutil.copytree(a.skill,s);path=s/rel;text=path.read_text()
   if name=='missing_mode':text,n=re.subn(old,new,text,count=1,flags=re.M)
   else:n=text.count(old);text=text.replace(old,new,1)
   assert n>=1;path.write_text(text)
   code,r=run(s,fixture);assert code!=0 and any(error in e for e in r['errors']),(name,r['errors']);print('PASS rejected '+name)
  e=root/'false-windows';e.mkdir()
  for f in a.evidence.glob('*.json'):shutil.copyfile(f,e/f.name)
  path=e/'windows-before.json';d=json.loads(path.read_text());d['records'][0]['status']='passed';path.write_text(json.dumps(d))
  code,r=run(a.skill,e);assert code!=0 and any('falsely labeled Windows' in x for x in r['errors']);print('PASS rejected false_windows_live')
 print('PASS 5 injected errors rejected')

if __name__=='__main__':main()
