#!/usr/bin/env python3
"""Build/check a metadata-only official-document catalog. Never fetch or execute source content."""
import argparse,collections,datetime,hashlib,json,re,sys
from pathlib import Path
from urllib.parse import urlsplit
import csv

QA=Path(__file__).resolve().parent
SKILL=QA.parents[2]/'development/huawei-cloud-fcaps-diagnostics'
SECTIONS={'故障排除':('故障排除_llms_manifest.csv','trouble-ecs'),'常见问题':('高频常见问题_llms_manifest.csv','ecs_faq')}

def sha(data):return hashlib.sha256(data).hexdigest()

def source_rows(archive):
    rows=[];hashes={};manifests={}
    for section,(filename,prefix) in SECTIONS.items():
        manifest=archive/filename;manifests[filename]=sha(manifest.read_bytes())
        for entry in csv.DictReader(manifest.open(encoding='utf-8')):
            url=entry['url'];parts=urlsplit(url)
            if parts.scheme!='https' or parts.netloc!='support.huaweicloud.com' or parts.query or parts.fragment:
                raise ValueError('Unexpected official source URL')
            if not re.fullmatch('/'+prefix+r'/[a-zA-Z0-9_-]+\.md',parts.path):raise ValueError('Unexpected document path')
            source=(archive/entry['file']).resolve()
            if not source.is_relative_to(archive.resolve()):raise ValueError('Archive path escapes its root')
            raw=source.read_bytes();text=raw.decode('utf-8')
            # The first H1 is the article title. Later '# dmidecode ...' can be a command-output heading.
            match=re.search(r'^#\s+(.+)$',text,re.M)
            if not match:raise ValueError('Document has no title: '+parts.path)
            title=re.sub(r'\[([^\]]+)\]\([^)]*\)',r'\1',match[1])
            title=re.sub(r'<[^>]+>','',title).replace('**','').replace('`','').strip()
            if not title or len(title)>300:raise ValueError('Invalid document title')
            cid=prefix+'/'+Path(parts.path).stem
            if cid in hashes:raise ValueError('Duplicate document ID: '+cid)
            rows.append(dict(id=cid,title=title,section=section,url=url));hashes[cid]=sha(raw)
    return sorted(rows,key=lambda x:x['id']),hashes,manifests

def encode(rows):return ''.join(json.dumps(x,ensure_ascii=False,separators=(',',':'))+'\n' for x in rows)

def curated_rows(path):
    if path is None:return [],None
    raw=path.read_bytes();data=json.loads(raw);datetime.date.fromisoformat(data['checked_date'])
    rows=data['sources'];ids=set();urls=set()
    for row in rows:
        if set(row)!={'id','title','section','url'}:raise ValueError('Curated source must contain metadata only')
        parts=urlsplit(row['url'])
        if parts.scheme!='https' or parts.netloc!='support.huaweicloud.com' or parts.query or parts.fragment:raise ValueError('Unexpected curated source URL')
        if not re.fullmatch(r'/[a-zA-Z0-9_./-]+\.(md|html)',parts.path) or parts.path.rsplit('.',1)[0]!='/'+row['id']:raise ValueError('Curated ID and URL disagree')
        if row['id'] in ids or row['url'] in urls:raise ValueError('Duplicate curated source')
        if not isinstance(row['title'],str) or not 0<len(row['title'])<=300 or not isinstance(row['section'],str) or not 0<len(row['section'])<=100:raise ValueError('Invalid curated metadata')
        ids.add(row['id']);urls.add(row['url'])
    return rows,{'checked_date':data['checked_date'],'count':len(rows),'metadata_sha256':sha(raw)}

def snapshot_line(receipt):
    counts=receipt['counts']
    return f"- 索引来自 {receipt['snapshot_date']} 归档：故障排除 {counts['故障排除']} 条、常见问题 {counts['常见问题']} 条。日期表示来源快照，不表示链接当前可用或内容仍适用于目标版本。"

def curated_line(receipt):
    c=receipt['curated']
    return f"- 补充来源：{c['checked_date']} 核验的 {c['count']} 条官方指引。核验范围为网页标题与正文；按需复核当前内容。"

def check(skill,receipt,archive=None,links=None):
    p=skill/'references/documents';raw=(p/'catalog.jsonl').read_text();rows=[json.loads(x) for x in raw.splitlines()];errors=[]
    extra,curated=curated_rows(links);extra_by_id={r['id']:r for r in extra}
    def require(ok,msg):
        if not ok:errors.append(msg)
    seen=set();urls=set()
    for row in rows:
        require(set(row)=={'id','title','section','url'},'Catalog must contain metadata only')
        cid=row.get('id');url=row.get('url','');parts=urlsplit(url)
        require(cid not in seen,'Duplicate document ID');seen.add(cid)
        require(url not in urls,'Duplicate source URL');urls.add(url)
        require(parts.scheme=='https' and parts.netloc=='support.huaweicloud.com' and not parts.query and not parts.fragment,'Noncanonical source URL')
        require(parts.path in {'/'+str(cid)+'.md','/'+str(cid)+'.html'},'ID and URL disagree')
        if cid in extra_by_id:require(row==extra_by_id[cid],'Curated metadata differs from declared source')
        else:require(row.get('section') in SECTIONS and str(cid).split('/')[0]==SECTIONS.get(row.get('section'),('',''))[1],'Section and source disagree')
        require(isinstance(row.get('title'),str) and 0<len(row['title'])<=300,'Invalid title')
    require(rows==sorted(rows,key=lambda x:x['id']),'Catalog order is not deterministic')
    require(sha(raw.encode())==receipt['catalog_sha256'],'Catalog changed without regeneration')
    require(dict(collections.Counter(x['section'] for x in rows))==receipt['counts'],'Catalog counts disagree')
    require(snapshot_line(receipt) in (p/'index.md').read_text(),'Snapshot guidance is stale')
    require(receipt.get('curated')==curated,'Curated source receipt differs')
    require(all(row in rows for row in extra),'Curated source missing from catalog')
    if curated:require(curated_line(receipt) in (p/'index.md').read_text(),'Curated guidance is stale')
    if archive:
        expected,hashes,manifests=source_rows(archive)
        expected=sorted(expected+extra,key=lambda x:x['id'])
        require(rows==expected,'Catalog differs from archive metadata')
        require(hashes==receipt['pages'],'Source content changed; review affected documents')
        require(manifests==receipt['manifests'],'Source manifests changed')
    guide=(p/'huaweicloud.md').read_text()
    for url in re.findall(r'\]\((https://support\.huaweicloud\.com/[^)]+)\)',guide):require(url in urls,'Curated source not in catalog: '+url)
    locations={cid:f.resolve() for f in (skill/'references/commands').rglob('*.md') for cid in re.findall(r'^\| `([^`]+)`',f.read_text(),re.M)}
    for cid,target in re.findall(r'\[([A-Z]+/[^\]]+)\]\((\.\./commands/[^)]+)\)',guide):
        require(cid in locations,'Unknown related command: '+cid)
        require((p/target.partition('#')[0]).resolve()==locations.get(cid),'Related command points outside its canonical file: '+cid)
    require(len((p/'index.md').read_text())<1600,'Document entrypoint is too large')
    require(len(guide)<6500,'Curated guide is too large')
    require(set(f.name for f in p.iterdir())=={'index.md','huaweicloud.md','catalog.jsonl'},'Raw source or unexpected payload in document directory')
    # Both navigation paths must expose documents; the bulk catalog is reached only from the document branch.
    require('references/documents/index.md' in (skill/'SKILL.md').read_text(),'No conditional skill route')
    require('../documents/huaweicloud.md' in (skill/'references/commands/index.md').read_text(),'No FCAPS route')
    return {'result':'PASS' if not errors else 'FAIL','documents':len(rows),'counts':dict(collections.Counter(x['section'] for x in rows)),'errors':errors,'snapshot_date':receipt['snapshot_date'],'index_chars':len((p/'index.md').read_text()),'guide_chars':len(guide),'source_checked':archive is not None}

def main():
    p=argparse.ArgumentParser();p.add_argument('mode',choices=['build','check']);p.add_argument('--archive',type=Path);p.add_argument('--skill',type=Path,default=SKILL);p.add_argument('--receipt',type=Path,default=QA/'documents-source.json');p.add_argument('--links',type=Path,default=QA/'documents-links.json');p.add_argument('--snapshot-date');p.add_argument('--report',type=Path);a=p.parse_args()
    if a.mode=='build':
        if not a.archive or not a.snapshot_date:p.error('build requires --archive and --snapshot-date')
        datetime.date.fromisoformat(a.snapshot_date)
        rows,hashes,manifests=source_rows(a.archive);extra,curated=curated_rows(a.links);rows=sorted(rows+extra,key=lambda x:x['id'])
        if len({r['id'] for r in rows})!=len(rows) or len({r['url'] for r in rows})!=len(rows):raise ValueError('Duplicate source across archive and curated links')
        raw=encode(rows);dest=a.skill/'references/documents/catalog.jsonl';dest.parent.mkdir(parents=True,exist_ok=True)
        previous=json.loads(a.receipt.read_text()) if a.receipt.exists() else {}
        changed=sorted(cid for cid in set(hashes)|set(previous.get('pages',{})) if hashes.get(cid)!=previous.get('pages',{}).get(cid))
        receipt={'snapshot_date':a.snapshot_date,'catalog_sha256':sha(raw.encode()),'counts':dict(collections.Counter(x['section'] for x in rows)),'manifests':manifests,'pages':hashes}
        receipt['curated']=curated
        index=dest.with_name('index.md');updated,n=re.subn(r'^- 索引来自 .*$',lambda _:snapshot_line(receipt),index.read_text(),count=1,flags=re.M)
        if n!=1:raise ValueError('Document entrypoint lacks its source-snapshot line')
        updated,n=re.subn(r'^- 补充来源：.*$',lambda _:curated_line(receipt),updated,count=1,flags=re.M)
        if n!=1:raise ValueError('Document entrypoint lacks its curated-source line')
        dest.write_text(raw);index.write_text(updated);a.receipt.write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'built':len(rows),'changed_documents':len(changed)},ensure_ascii=False))
        if a.report:a.report.write_text(json.dumps({'changed_document_ids':changed},ensure_ascii=False,indent=2)+'\n')
        return True
    result=check(a.skill,json.loads(a.receipt.read_text()),a.archive,a.links)
    if a.report:a.report.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(result,ensure_ascii=False,indent=2));return result['result']=='PASS'

if __name__=='__main__':sys.exit(0 if main() else 1)
