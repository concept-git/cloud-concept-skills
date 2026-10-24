#!/usr/bin/env python3
"""Validate platform contracts against actual pre/post evidence; emit scoped summaries."""
import argparse,collections,hashlib,importlib.util,json,re,sys
from pathlib import Path
QA=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('live_verify',QA/'live/verify.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)

def help_state(record):
 h=record.get('help')
 if not h:return '未核验'
 text=h.get('stdout','')+h.get('stderr','')
 if h.get('exit_code')==127:return '工具缺失'
 return '通过' if re.search(r'usage|options|用法|选项',text,re.I) else '未确认'

def main():
 p=argparse.ArgumentParser();p.add_argument('--skill',type=Path,required=True);p.add_argument('--evidence',type=Path,required=True);p.add_argument('--write-verification',action='store_true');a=p.parse_args()
 skill=a.skill.resolve();e=a.evidence.resolve();rows=v.contracts(skill);catalog=json.loads((e/'candidates.json').read_text());sources=json.loads((e/'source-audit.json').read_text());errs=[];checks=collections.Counter()
 def check(ok,group,msg):
  checks[group]+=1
  if not ok:errs.append(msg)
 ids=[r['id'] for r in rows];check(len(ids)==len(set(ids)),'unique','duplicate platform ID');check(set(ids)=={r['id'] for r in catalog},'coverage','candidate inventory mismatch')
 check(set(ids)=={r['id'] for r in sources},'source','migration inventory mismatch')
 allrecords={};summaries={}
 for env in ['linux','windows','kubernetes']:
  before=json.loads((e/(env+'-before.json')).read_text());postpath=e/(env+'-after.json');after=json.loads(postpath.read_text()) if postpath.exists() else before
  b={r['id']:r for r in before['records']};records={r['id']:r for r in after['records']};selected=[r for r in rows if r['env']==env]
  check(set(records)=={r['id'] for r in selected},'evidence_coverage',env+' evidence inventory mismatch')
  scope={'linux':'Huawei ECS / Ubuntu 24.04.4 LTS / root；不外推其他发行版','windows':'无 Windows 目标或 Windows PowerShell；只审阅下载来源','kubernetes':'macOS arm64 kubectl 1.33.9 / local kind Kubernetes 1.33.1；不是 CCE'}[env]
  lines=['# '+env+' 验证','','范围：'+scope+'。','', '帮助与运行分开。受阻、未执行和空结果不是取得完整数据。按 ID 查所需行；[返回地图](../commands/index.md)。','','| 命令 ID | 帮助 | 运行 | 日期 | 边界 |','| --- | --- | --- | --- | --- |']
  for row in selected:
   cid=row['id'];r=records.get(cid,{})
   if not r:continue
   hs=help_state(r if r.get('help') else b.get(cid,{}));state=r['status'];allrecords[cid]=r
   check(state!='failed','execution',cid+' failed real execution')
   if state in ['passed','empty']:
    check(after.get('phase')=='post-write','post_write',cid+' lacks post-write execution')
    check(r.get('row_sha256')==row['row_sha256'],'revision',cid+' stale row evidence')
    check(r.get('command')==row['command'],'syntax',cid+' executed different command')
    check(all(x['passed'] for x in r.get('assertions',[])),'assertions',cid+' failed output assertions')
    check('exit_code' in r and ('stdout' in r or 'stderr' in r),'raw_evidence',cid+' missing raw execution evidence')
   if env=='windows':check(state=='blocked' and hs=='未核验','scope',cid+' falsely labeled Windows validation')
   state_cn={'passed':'取得数据','empty':'成功空结果','blocked':'受阻','not_run':'未执行','failed':'失败','help_only':'未执行'}[state]
   note=''
   if env=='windows':note='缺适用环境；来源审阅不代表帮助通过'
   elif state=='not_run':note='有条件采集或扫描；未执行业务操作'
   elif state=='blocked':note='缺依赖或权限；见本地证据'
   elif state=='empty':note='仅本次范围为空'
   else:note='仅上述环境与参数'
   lines.append('| `'+cid+'` | '+hs+' | '+state_cn+' | '+r.get('at','')[:10]+' | '+note+' |')
  if env=='linux' and (e/'device-after.json').exists():
   binding=json.loads((e/'device-after.json').read_text())
   section=(skill/'references/helpers.md').read_text().split('## H-device\n',1)[1].split('\n## ',1)[0]
   check(binding.get('status')=='passed' and binding.get('helper_sha256')==hashlib.sha256(section.encode()).hexdigest(),'helper_revision','H-device proof is missing or stale')
   lines+=['','## H-device','',''+binding['at'][:10]+'：当前 ECS 的 virtio/VBD 整盘按序列号前缀、实例内唯一性及 PCI 地址验证通过。SCSI、WWN、XEN 和其他环境未验证。']
  expected='\n'.join(lines)+'\n';dest=skill/'references/verification'/f'{env}.md'
  if a.write_verification:dest.write_text(expected)
  else:check(dest.exists() and dest.read_text()==expected,'summary',env+' verification summary differs from evidence')
  summaries[env]=dict(collections.Counter(r['status'] for r in records.values()))
 # Required live scope: all bounded Linux base queries and all local Kubernetes queries.
 for r in catalog:
  if r['env']=='linux' and r.get('live',True) and r.get('required_live',True):check(allrecords.get(r['id'],{}).get('status') in ['passed','empty'],'required_live',r['id']+' did not pass required Linux execution')
  if r['env']=='linux' and not r.get('required_live',True):
   record=allrecords.get(r['id'],{})
   check(record.get('status') in ['passed','empty','blocked'],'optional_scope',r['id']+' has an unexplained optional result')
   if record.get('status')=='blocked':check(help_state(record)=='工具缺失' or 'not running' in record.get('reason',''),'optional_scope',r['id']+' blocked without observed dependency evidence')
  if r['env']=='kubernetes':check(allrecords.get(r['id'],{}).get('status') in ['passed','empty'],'required_live',r['id']+' did not pass required local cluster execution')
 for path in (skill/'references/commands').rglob('*.md'):
  if path.name not in ['linux.md','windows.md','kubernetes.md']:continue
  text=path.read_text();check('| 命令 | 作用 | 输入与来源 | 约束 |' in text,'format',str(path)+' lacks four columns')
  for line in text.splitlines():
   if re.match(r'^\| `(LINUX|WINDOWS|KUBERNETES)/',line):check(len(re.split(r'(?<!\\)\|',line))==6,'format','wrong cell count '+line[:80])
  check(len(text)<14000,'context','oversized platform branch '+str(path))
 entry=(skill/'SKILL.md').read_text();check(len(entry)<1500,'context','entrypoint exceeds local regression budget')
 check('verification/' not in ''.join(r['file'] for r in rows),'separation','contracts in evidence directory')
 for path in skill.rglob('*.md'):
  text=path.read_text();ips=set(re.findall(r'\b(?:\d{1,3}\.){3}\d{1,3}\b',text));check(ips <= {'169.254.169.254'},'privacy','literal target IP in '+str(path))
 report={'result':'PASS' if not errs else 'FAIL','scope':f'{len(rows)} 个非 hcloud 模式的结构与证据；逐条日期和环境决定真实覆盖。Windows 受阻，条件采集未运行。','contracts':len(rows),'states':summaries,'checks':dict(checks),'errors':errs,'entry_chars':len(entry),'max_platform_chars':max(len(p.read_text()) for p in (skill/'references/commands').rglob('*.md') if p.name in ['linux.md','windows.md','kubernetes.md'])}
 (e/'platform-acceptance.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,ensure_ascii=False,indent=2));return not errs

if __name__=='__main__':sys.exit(0 if main() else 1)
