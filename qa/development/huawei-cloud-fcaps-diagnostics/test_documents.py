#!/usr/bin/env python3
"""Test metadata boundaries and source drift without fetching documents or executing them."""
import copy,importlib.util,json,tempfile
from pathlib import Path
spec=importlib.util.spec_from_file_location('documents',Path(__file__).with_name('documents.py'));m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

def main():
 with tempfile.TemporaryDirectory(prefix='fcaps-documents-') as tmp:
  root=Path(tmp);archive=root/'archive';archive.mkdir();skill=root/'skill';d=skill/'references/documents';d.mkdir(parents=True);(skill/'references/commands').mkdir()
  (skill/'SKILL.md').write_text('[需要依据时读文档](references/documents/index.md)')
  (skill/'references/commands/index.md').write_text('[主题](../documents/huaweicloud.md)')
  (d/'index.md').write_text('按命中条目读取。');(d/'huaweicloud.md').write_text('[故障](https://support.huaweicloud.com/trouble-ecs/example.md)')
  for section,(filename,prefix) in m.SECTIONS.items():
   (archive/(prefix+'.md')).write_text('# '+section+'标题\n\n```\n# command output\n```\n')
   (archive/filename).write_text('url,file,status,bytes\nhttps://support.huaweicloud.com/'+prefix+'/example.md,'+prefix+'.md,downloaded,0\n')
  rows,hashes,manifests=m.source_rows(archive);assert len(rows)==2 and all('标题' in r['title'] for r in rows)
  raw=m.encode(rows);receipt={'snapshot_date':'2026-10-21','catalog_sha256':m.sha(raw.encode()),'counts':{'常见问题':1,'故障排除':1},'pages':hashes,'manifests':manifests};(d/'catalog.jsonl').write_text(raw)
  (d/'index.md').write_text(m.snapshot_line(receipt))
  assert m.check(skill,receipt,archive)['result']=='PASS';print('PASS source titles and baseline')
  cases=[]
  dup=copy.deepcopy(rows)+[copy.deepcopy(rows[0])];cases.append(('duplicate',dup,'Duplicate document ID'))
  ext=copy.deepcopy(rows);ext[0]['url']='https://example.invalid/doc.md';cases.append(('foreign_source',ext,'Noncanonical source URL'))
  full=copy.deepcopy(rows);full[0]['body']='source commands';cases.append(('body_in_catalog',full,'Catalog must contain metadata only'))
  wrong=copy.deepcopy(rows);wrong[0]['id']='wrong/id';cases.append(('wrong_identity',wrong,'ID and URL disagree'))
  for name,changed,expected in cases:
   (d/'catalog.jsonl').write_text(m.encode(changed));result=m.check(skill,receipt)
   assert result['result']=='FAIL' and expected in result['errors'],result;print('PASS rejected '+name)
  (d/'catalog.jsonl').write_text(raw);(archive/'trouble-ecs.md').write_text('# 故障排除标题\nchanged source body\n')
  result=m.check(skill,receipt,archive);assert 'Source content changed; review affected documents' in result['errors'];print('PASS detected source body drift with unchanged title')
  (d/'huaweicloud.md').write_text('[wrong](https://support.huaweicloud.com/trouble-ecs/missing.md)')
  assert any('Curated source not in catalog' in e for e in m.check(skill,receipt)['errors']);print('PASS rejected unknown curated source')
  stale=copy.deepcopy(receipt);stale['snapshot_date']='2026-10-22'
  assert 'Snapshot guidance is stale' in m.check(skill,stale)['errors'];print('PASS rejected stale snapshot date')
  command=skill/'references/commands/fault/linux.md';command.parent.mkdir();command.write_text('| `LINUX/example` | observation | input | constraint |\n')
  (d/'huaweicloud.md').write_text('[LINUX/example](../commands/configuration/linux.md)')
  assert any('outside its canonical file' in e for e in m.check(skill,receipt)['errors']);print('PASS rejected wrong command target')
  links=root/'links.json';extra=[{'id':'usermanual-lts/example','title':'HTML 标题','section':'LTS 用户指南','url':'https://support.huaweicloud.com/usermanual-lts/example.html'},{'id':'usermanual-evs/example','title':'Markdown 标题','section':'EVS 用户指南','url':'https://support.huaweicloud.com/usermanual-evs/example.md'}]
  declared={'checked_date':'2026-10-22','sources':extra};links.write_text(json.dumps(declared,ensure_ascii=False))
  _,curated=m.curated_rows(links);combined=sorted(rows+extra,key=lambda x:x['id']);merged=m.encode(combined)
  updated=copy.deepcopy(receipt);updated.update(catalog_sha256=m.sha(merged.encode()),counts=dict(m.collections.Counter(r['section'] for r in combined)),curated=curated)
  (d/'catalog.jsonl').write_text(merged);(d/'index.md').write_text(m.snapshot_line(updated)+'\n'+m.curated_line(updated));(d/'huaweicloud.md').write_text('\n'.join('[source]('+r['url']+')' for r in extra))
  assert m.check(skill,updated,links=links)['result']=='PASS';print('PASS merged HTML and Markdown metadata')
  declared['sources'].append(dict(extra[0],url=extra[0]['url'].replace('.html','.md')));links.write_text(json.dumps(declared))
  try:m.curated_rows(links)
  except ValueError as e:assert str(e)=='Duplicate curated source';print('PASS rejected duplicate format identity')
  else:raise AssertionError('Duplicate formats accepted')
  declared['sources'].pop();declared['checked_date']='2026-10-23';links.write_text(json.dumps(declared))
  assert 'Curated source receipt differs' in m.check(skill,updated,links=links)['errors'];print('PASS rejected curated metadata drift')
 print('PASS 10 negative cases')

if __name__=='__main__':main()
