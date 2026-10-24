#!/usr/bin/env python3
"""Validate final kubectl contracts against the dedicated local kind fixture.

--setup creates only the fcaps-contracts namespace fixture; never use against CCE.
"""
import argparse,datetime,hashlib,importlib.util,json,os,re,shlex,subprocess
from pathlib import Path
spec=importlib.util.spec_from_file_location('host_verify',Path(__file__).with_name('verify.py'));v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)

def main():
 p=argparse.ArgumentParser();p.add_argument('--skill',type=Path,required=True);p.add_argument('--kubeconfig',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--setup',action='store_true');a=p.parse_args()
 context='kind-fcaps-validation';namespace='fcaps-contracts';env={**os.environ,'KUBECONFIG':str(a.kubeconfig.resolve())};base=['kubectl','--context',context,'--request-timeout=20s']
 def run(args,data=None,timeout=120):return subprocess.run(args,input=data,capture_output=True,text=True,env=env,timeout=timeout)
 if a.setup:
  nodes=run(base+['get','nodes','-o','json']);n=json.loads(nodes.stdout)
  if not n['items'] or any(not x['metadata']['name'].startswith('fcaps-validation-') for x in n['items']):raise SystemExit('Not the dedicated local test cluster')
  objects=[{'apiVersion':'v1','kind':'Namespace','metadata':{'name':namespace}},
   {'apiVersion':'v1','kind':'PersistentVolumeClaim','metadata':{'name':'probe-volume','namespace':namespace},'spec':{'accessModes':['ReadWriteOnce'],'resources':{'requests':{'storage':'64Mi'}}}},
   {'apiVersion':'v1','kind':'Pod','metadata':{'name':'probe','namespace':namespace,'labels':{'app':'fcaps-probe'}},'spec':{'restartPolicy':'Always','containers':[{'name':'probe','image':'busybox:1.36','command':['sh','-c','if [ ! -f /state/started ]; then echo prior-instance; touch /state/started; exit 1; fi; echo current-instance; sleep 86400'],'resources':{'requests':{'cpu':'10m','memory':'8Mi'},'limits':{'cpu':'100m','memory':'32Mi'}},'volumeMounts':[{'name':'state','mountPath':'/state'}]}],'volumes':[{'name':'state','persistentVolumeClaim':{'claimName':'probe-volume'}}]}},
   {'apiVersion':'v1','kind':'Service','metadata':{'name':'probe','namespace':namespace},'spec':{'selector':{'app':'fcaps-probe'},'ports':[{'port':8080,'targetPort':8080}]}},
   {'apiVersion':'networking.k8s.io/v1','kind':'NetworkPolicy','metadata':{'name':'probe-policy','namespace':namespace},'spec':{'podSelector':{'matchLabels':{'app':'fcaps-probe'}},'policyTypes':['Ingress'],'ingress':[]}}]
  applied=run(base+['apply','-f','-'],json.dumps({'apiVersion':'v1','kind':'List','items':objects}))
  if applied.returncode:raise SystemExit(applied.stderr)
  ready=run(base+['-n',namespace,'wait','--for=condition=Ready','pod/probe','--timeout=180s'],timeout=200)
  if ready.returncode:raise SystemExit(ready.stderr)
 pod=json.loads(run(base+['-n',namespace,'get','pod','probe','-o','json']).stdout)
 pvc=json.loads(run(base+['-n',namespace,'get','pvc','probe-volume','-o','json']).stdout)
 bindings={'context':context,'namespace':namespace,'pod':'probe','container':'probe','service':'probe','uid':pod['metadata']['uid'],'pv':pvc['spec']['volumeName'],'start':pod['metadata']['creationTimestamp']}
 records=[]
 for row in v.contracts(a.skill):
  if row['env']!='kubernetes':continue
  argv=shlex.split(row['command'])
  for i,s in enumerate(argv):
   for k,value in bindings.items():s=s.replace('$'+k,value)
   argv[i]=s
  result=run(argv);out=result.stdout;err=result.stderr;key=row['id'].split('/')[1];assertions=[];passed=result.returncode==0
  if passed and '-o' in argv and argv[argv.index('-o')+1]=='json':
   try:
    data=json.loads(out);items=data.get('items',[data]);passed=bool(items)
    if key=='pods':passed=any(x['metadata']['uid']==bindings['uid'] for x in items)
    elif key=='pod-events':passed=all(x.get('involvedObject',{}).get('uid')==bindings['uid'] for x in items)
    elif key=='pv':passed=data['metadata']['name']==bindings['pv']
    elif key=='endpoints':passed=any(any(z.get('targetRef',{}).get('uid')==bindings['uid'] for z in x.get('endpoints',[])) for x in items)
    assertions.append({'name':'structured output and target binding','passed':passed})
   except (ValueError,KeyError):passed=False
  elif passed:
   expected={'context':context,'container-logs':'current-instance','previous-logs':'prior-instance','permission':'yes'}.get(key)
   passed=expected in out if expected else bool(out.strip());assertions.append({'name':'expected target output','passed':passed})
   if key=='pod-describe':
    current=json.loads(run(base+['-n',namespace,'get','pod','probe','-o','json']).stdout)
    passed=passed and bool(re.search(r'^Name:\s+probe$',out,re.M)) and bool(re.search(r'^Namespace:\s+'+namespace+'$',out,re.M)) and current['metadata']['uid']==bindings['uid']
    assertions.append({'name':'name, namespace and unchanged Pod UID','passed':passed})
  state='passed' if passed else 'failed'
  if key in ['pod-usage','node-usage'] and ('Metrics API not available' in err or 'metrics not available' in err or 'metrics API' in err):state='blocked'
  records.append({'id':row['id'],'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'command':row['command'],'row_sha256':row['row_sha256'],'status':state,'exit_code':result.returncode,'stdout':out,'stderr':err,'assertions':assertions})
 result={'environment':{'kind':'local kind; not CCE','client':json.loads(run(['kubectl','version','--client','-o','json']).stdout),'server':json.loads(run(base+['version','-o','json']).stdout)},'phase':'post-write','records':records}
 a.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');a.output.chmod(0o600)
 from collections import Counter
 print(json.dumps({'states':dict(Counter(x['status'] for x in records)),'issues':[{'id':x['id'],'status':x['status'],'error':x['stderr'][:160]} for x in records if x['status']!='passed']}))

if __name__=='__main__':main()
