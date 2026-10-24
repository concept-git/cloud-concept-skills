#!/usr/bin/env python3
"""Check the draft against recorded CLI evidence. Does not call cloud APIs."""
import argparse
import collections
import datetime as dt
import hashlib
import json
from pathlib import Path
import re
import sys

REPO = Path(__file__).resolve().parents[3]
SKILL = REPO / "development/huawei-cloud-fcaps-diagnostics"
META = Path.home() / ".hcloud/metaRepo/template"


def read_log(path):
    return [json.loads(line) for line in path.read_text().splitlines() if line]


def latest(rows):
    return {row["id"]: row for row in rows}


def anchor(title):
    return re.sub(r"[^\w\- ]", "", title.lower()).replace(" ", "-")


def error_summary(row):
    message = row.get("error") or ""
    codes = re.findall(r"\b[A-Za-z][A-Za-z0-9_-]*\.[0-9]+\b", message)
    message = re.sub(r"\b(?:[0-9a-f]{32}|[0-9a-f]{8}-(?:[0-9a-f]{4}-){3}[0-9a-f]{12})\b", "<redacted-id>", message)
    return {"id": row["id"], "error_code": row.get("error_code") or (codes[0] if codes else None), "error": message}


def contract_digest(skill):
    digest = hashlib.sha256()
    for path in sorted(skill.rglob("*.md")):
        if path.name in {"README.md", "STRUCTURE.md", "verification.md"} or "verification" in path.relative_to(skill).parts:
            continue
        digest.update(str(path.relative_to(skill)).encode() + b"\0" + path.read_bytes() + b"\0")
    return digest.hexdigest()


def verification_records(evidence, recheck):
    manifest = json.loads((evidence / "manifest.json").read_text())
    helps = latest(read_log(evidence / "help-results.jsonl"))
    lives = latest(read_log(evidence / "live-results.jsonl") + recheck.get("live_calls", []))
    result = {}
    for row in manifest:
        cid = row["id"]; h = helps[cid]; l = lives.get(cid)
        hd = h["at"][:10]; ld = l["at"][:10] if l else hd
        date = hd if hd == ld else f"帮助 {hd}；调用 {ld}"
        notes = []
        if h.get("region_hint"):
            notes.append("帮助区域 " + h["region_hint"])
        if l:
            region = next((a.split("=", 1)[1] for a in l.get("argv", []) if a.startswith("--cli-region=")), None)
            if region: notes.append("调用区域 " + region)
            if l["status"] == "blocked": notes.append(error_summary(l)["error_code"] or "调用错误")
            elif l["status"] == "empty": notes.append("本次查询范围为空")
            elif l.get("assertions"): notes.append("资源断言 " + str(sum(a['passed'] for a in l['assertions'])) + " 项通过")
        result[cid] = ["通过" if h["status"] == "passed" else "受阻", {"passed":"成功", "empty":"成功空结果", "blocked":"受阻"}[l["status"]] if l else "未执行", date, "；".join(notes) or "—"]
    return result


def write_verification(evidence, skill, recheck):
    rows = verification_records(evidence, recheck)
    lines = ["# 验证记录", "", "仅在判断证据范围时按完整命令 ID 搜索。以下是执行记录，不是命令的永久属性。", "", "CLI：7.2.12。帮助核验来自 2026-10-19；业务调用日期逐条记录。", "", "范围：本次已配置账号和选定 ECS 及关联资源。区域见各行；IAM、EPS 的全局查询仍需相应账号权限。账号与资源标识保留在本地证据中。", "", "未执行表示只完成帮助核验；成功空结果不证明系统正常；单次调用成功不覆盖所有参数或区域。历史受阻只描述当时账号。", "", "完整命令定义见 [FCAPS 索引](../commands/index.md)。" , ""]
    for service in sorted({cid.split('/')[0] for cid in rows}):
        lines += ['## '+service, '', '| 命令 | 帮助核验 | 业务调用 | 记录日期 | 范围或结果 |', '| --- | --- | --- | --- | --- |']
        for cid, fields in rows.items():
            if cid.split('/')[0] == service: lines.append('| `'+cid+'` | '+' | '.join(fields)+' |')
        lines.append('')
    lines += ['## CLI 元工具', '', '| 命令 | 帮助核验 | 本地调用 | 记录日期 |', '| --- | --- | --- | --- |']
    for r in json.loads((evidence/'cli-results.json').read_text()):
        hs='通过' if r['verification']=='help' and r['status']=='passed' else '未单独核验'
        cs='成功' if r['verification']=='local' and r['status']=='passed' else '未执行'
        lines.append('| `'+r['command']+'` | '+hs+' | '+cs+' | '+r['at'][:10]+' |')
    lines += ['', '## 资源衔接', '', 'H-port、H-subnet、H-volume、H-eip 的历史资源衔接检查在 2026-10-19 通过。']
    if recheck.get('completed'):
        lines.append('当前契约修订的复核：'+recheck['finished'][:10]+'，'+str(sum(c['passed'] for c in recheck['checks']))+'/'+str(len(recheck['checks']))+' 项通过。完整记录保留在本地验收报告中。')
    (skill/'references/verification/cloud.md').write_text('\n'.join(lines)+'\n')


def validate(evidence, skill=SKILL, report_dir=None, recheck_path=None):
    report_dir = report_dir or evidence
    report_dir.mkdir(parents=True, exist_ok=True)
    errors = []
    checks = collections.Counter()

    def check(ok, group, message):
        checks[group] += 1
        if not ok:
            errors.append(message)

    manifest = {r["id"]: r for r in json.loads((evidence / "manifest.json").read_text())}
    help_attempts = read_log(evidence / "help-results.jsonl")
    live_attempts = read_log(evidence / "live-results.jsonl")
    recheck = json.loads(recheck_path.read_text()) if recheck_path and recheck_path.exists() else {}
    live_attempts += recheck.get("live_calls", [])
    helps, lives = latest(help_attempts), latest(live_attempts)
    cli_rows = json.loads((evidence / "cli-results.json").read_text())
    for row in cli_rows:
        raw = (evidence / row["file"]).read_bytes()
        check(row["status"] == "passed" and hashlib.sha256(raw).hexdigest() == row["sha256"], "cli_meta_tools", f"CLI evidence failed: {row['command']}")
    files = {p.resolve(): p.read_text() for p in skill.rglob("*.md")}
    runtime = {p: text for p, text in files.items() if p.name not in {"README.md", "STRUCTURE.md"}}
    contracts = {}
    for path, text in runtime.items():
        if "verification" in path.relative_to(skill).parts:
            continue
        for cid, action, inputs, constraints in re.findall(
            r"^\| `([^`]+/[^`]+/v\d+)` \| ([^|]*) \| ([^|]*) \| ([^|]*) \|$", text, re.M
        ):
            check(cid not in contracts, "canonical", f"Duplicate contract: {cid}")
            contracts[cid] = dict(path=path, action=action.strip(), inputs=inputs.strip(), constraints=constraints.strip())
            check("| 命令 | 作用 | 输入与来源 | 约束 |" in text, "format", f"Wrong contract columns: {path.name}")
            check(not re.search(r"· (实|助|阻)|本次调用受阻|帮助使用区域", action+inputs+constraints), "separation", f"Execution evidence mixed into contract: {cid}")
    expected_records = verification_records(evidence, recheck)
    verification_text = (skill / "references/verification/cloud.md").read_text()
    recorded = {}
    for cid, help_state, call_state, date, detail in re.findall(r"^\| `([^`]+/[^`]+/v\d+)` \| ([^|]*) \| ([^|]*) \| ([^|]*) \| ([^|]*) \|$", verification_text, re.M):
        check(cid not in recorded, "verification_unique", f"Duplicate verification: {cid}")
        recorded[cid] = [help_state, call_state, date, detail]
    check(set(recorded) == set(manifest), "verification_coverage", "Verification inventory differs from command inventory")
    for cid, expected in expected_records.items():
        check(recorded.get(cid) == expected, "status", f"Verification evidence mismatch: {cid}")
    cli_section = verification_text.split("## CLI 元工具\n", 1)[-1].split("\n## ", 1)[0]
    cli_snapshot = {}
    for command, help_state, local_state, date in re.findall(r"^\| `([^`]+)` \| ([^|]*) \| ([^|]*) \| ([^|]*) \|$", cli_section, re.M):
        check(command not in cli_snapshot, "cli_verification_unique", f"Duplicate CLI verification: {command}")
        cli_snapshot[command] = [help_state, local_state, date]
    check(set(cli_snapshot) == {r["command"] for r in cli_rows}, "cli_verification_coverage", "CLI verification inventory differs from evidence")
    for row in cli_rows:
        expected = [
            "通过" if row["verification"] == "help" and row["status"] == "passed" else "未单独核验",
            "成功" if row["verification"] == "local" and row["status"] == "passed" else "未执行",
            row["at"][:10],
        ]
        check(cli_snapshot.get(row["command"]) == expected, "cli_verification_status", f"CLI verification evidence mismatch: {row['command']}")
    check(set(contracts) == set(manifest), "coverage", f"Coverage mismatch: missing={sorted(set(manifest)-set(contracts))}, extra={sorted(set(contracts)-set(manifest))}")
    check(set(manifest) <= set(helps), "coverage", "Some commands lack an actual help attempt")
    check(set(lives) <= set(manifest), "coverage", "Live calls outside the documented inventory")

    catalogs = {}
    for cid, row in manifest.items():
        if cid not in contracts or cid not in helps:
            continue
        contract, help_row, live_row = contracts[cid], helps[cid], lives.get(cid)
        service = row["service"].lower()
        if service not in catalogs:
            catalogs[service] = json.loads((META / service / "apis_cn.json").read_text())["apiList"]
        entry = catalogs[service].get(row["operation"].lower(), {})
        check(row["version"] in entry.get("Versions", []), "catalog", f"Unknown command/version: {cid}")
        raw_path = evidence / help_row["file"]
        raw = raw_path.read_text()
        check(hashlib.sha256(raw.encode()).hexdigest() == help_row["sha256"], "help_integrity", f"Help hash mismatch: {cid}")
        if help_row["status"] == "passed":
            check(bool(re.search(r"^Service:\s*\n\s*" + re.escape(row["service"]) + r"\s*$", raw, re.M)), "help_content", f"Help service missing: {cid}")
            check(bool(re.search(r"^Method:\s*\n\s*" + help_row["method"] + r"\b", raw, re.M)), "help_content", f"Help method missing: {cid}")
        for dep in re.findall(r"\[([^\]]+/[^\]]+/v\d+)\]", contract["inputs"] + contract["constraints"]):
            check(dep in manifest, "dependency", f"Unknown dependency: {cid} -> {dep}")

    graph = collections.defaultdict(set)
    for path, text in files.items():
        for cid, target in re.findall(r"\[([^\]]+/[^\]]+/v\d+)\]\(([^\s)]+)\)", text):
            dest = (path.parent / target.partition("#")[0]).resolve()
            check(cid in contracts and dest == contracts[cid]["path"], "dependency_target", f"Dependency points outside its canonical contract: {path.name} -> {cid}")
        for target in re.findall(r"(?<!!)\[[^\]]+\]\(([^\s)]+)\)", text):
            if re.match(r"[a-z]+://", target):
                continue
            rel, _, fragment = target.partition("#")
            dest = (path.parent / rel).resolve() if rel else path
            check(dest.is_file(), "links", f"Missing link: {path.name} -> {target}")
            graph[path].add(dest)
            if fragment and dest in files:
                anchors = {anchor(t) for t in re.findall(r"^#+ (.+)$", files[dest], re.M)}
                check(fragment in anchors, "anchors", f"Missing anchor: {path.name} -> {target}")
    reached, pending = set(), [skill / "SKILL.md"]
    while pending:
        path = pending.pop().resolve()
        if path in reached:
            continue
        reached.add(path)
        pending.extend(graph[path] - reached)
    check(set(runtime) <= reached, "loading", f"Unreachable references: {[str(p.relative_to(skill)) for p in set(runtime)-reached]}")

    for path, text in runtime.items():
        check(not re.search(r"\b[0-9a-f]{8}-(?:[0-9a-f]{4}-){3}[0-9a-f]{12}\b", text), "redaction", f"Resource UUID in runtime: {path.name}")
        check(not re.search(r"--cli-(?:ak|sk|token|access-key|secret-key|security-token)=\S+", text), "redaction", f"Credential argument in runtime: {path.name}")
    recipe_paths = sorted((skill / "references/recipes").glob("*.md"))
    check(len(recipe_paths) == 9, "recipe_scope", "Recipe planning directory must cover the nine agreed topics")
    for path in recipe_paths:
        text = path.read_text()
        body = "\n".join(line for line in text.splitlines() if line and not line.startswith("#"))
        check("规划" in text and 1 <= body.count("。") <= 2 and "hcloud " not in body and "```" not in body, "recipe_scope", f"Recipe exceeds planning scope: {path.name}")

    semantic_cases = {
        "HSS/RunBaselineDetect/v5": (["发起", "检测"], "GET"),
        "COC/CreateDiagnosisTask/v1": (["安装", "Holmes", "采集"], "POST"),
        "ECS/ShowServerRemoteConsole/v2": (["生成", "登录地址"], "POST"),
        "APM/ShowSpanSearch/v1": (["读取"], "POST"),
        "SMN/PublishMessage/v2": (["发送消息"], "POST"),
        "HSS/ListHostStatus/v5": (["读取", "同步"], "GET"),
        "CFW/ListEips/v1": (["读取", "同步"], "GET"),
    }
    for cid, (terms, method) in semantic_cases.items():
        check(all(t in contracts.get(cid, {}).get("action", "") for t in terms) and helps.get(cid, {}).get("method") == method, "effect_semantics", f"Known effect/method distinction lost: {cid}")
    constraint_cases = {
        "VPC/ShowSubnet/v2": ["Neutron"],
        "EVS/CinderListQuotas/v2": ["target_project_id=project_id", "usage=True"],
        "CFW/ListEips/v1": ["sync=0", "1", "同步"],
        "HSS/ListHostStatus/v5": ["refresh=false", "true", "同步"],
        "COC/CreateDiagnosisTask/v1": ["UniAgent", "授权", "type=ECS"],
        "COC/ListDiagnosisTasks/v1": ["page_index", "page_size"],
        "CES/ShowMetricData/v1": ["毫秒"],
        "CES/ListAlarmHistories/v2": ["ISO 8601"],
        "HSS/RunBaselineDetect/v5": ["GET", "检测"],
    }
    for cid, terms in constraint_cases.items():
        check(all(t in contracts.get(cid, {}).get("constraints", "") for t in terms), "constraints", f"Execution constraint lost: {cid}")
    check("time_measure_id" not in contracts.get("BSS/ListCosts/v2", {}).get("inputs", ""), "identifier_semantics", "Time granularity enum misclassified as a resource identifier")
    helpers = (skill / "references/helpers.md").read_text()
    helper_requirements = {
        "H-port": ["按目标 IP 或 MAC", "interfaceAttachments[].port_id", "VPC.PortId", "port.security_groups[]"],
        "H-subnet": ["Neutron.SubnetId", "subnets[].neutron_subnet_id", "同项 `subnets[].id` → `VPC.SubnetId`"],
        "H-volume": ['server["os-extended-volumes:volumes_attached"][].id', "EVS.VolumeId", "系统盘或数据盘"],
        "H-eip": ["publicips[].port_id", "同项 `id` → `EIP.PublicipId`", "同项 `bandwidth_id` → `EIP.BandwidthId`"],
    }
    for heading, terms in helper_requirements.items():
        section = helpers.split("## " + heading + "\n", 1)[-1].split("\n## ", 1)[0]
        check("| 输入 | 获取命令 | 选择条件 | 输出绑定 |" in section and all(t in section for t in terms), "helper_bindings", f"Missing selection or field binding: {heading}")
    for row in lives.values():
        if row["status"] in {"passed", "empty"}:
            check(all(a["passed"] for a in row.get("assertions", [])), "live_assertions", f"Failed assertion labeled successful: {row['id']}")
    check(recheck.get("completed") is True and len(recheck.get("checks", [])) == 10 and all(c["passed"] for c in recheck.get("checks", [])), "post_write", "Current post-write live checks missing or failed")
    check(recheck.get("contract_sha256") == contract_digest(skill), "revision_binding", "Live dependency checks do not match this contract revision")
    report = {
        "at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "scope": "结构、清单覆盖、证据一致性和指定依赖链；不等于全部业务接口实测成功",
        "result": "PASS" if not errors else "FAIL",
        "contracts": len(contracts), "services": len(catalogs),
        "checks": dict(checks), "errors": errors,
        "help": {"unique": len(helps), "attempts": len(help_attempts), **dict(collections.Counter(r["status"] for r in helps.values()))},
        "cli_meta_tools": {"unique": len(cli_rows), **dict(collections.Counter(r["verification"] for r in cli_rows))},
        "live": {"unique": len(lives), "attempts": len(live_attempts), **dict(collections.Counter(r["status"] for r in lives.values()))},
        "verification_states": dict(collections.Counter(r[1] for r in expected_records.values())),
        "blocked": [error_summary(r) for r in lives.values() if r["status"] == "blocked"],
        "help_blocked": [error_summary(r) for r in helps.values() if r["status"] != "passed"],
        "post_write": recheck,
    }
    (report_dir / "acceptance.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    lines = [
        "# 真实验收结果", "",
        f"时间：{report['at']}。KooCLI 7.2.12。", "",
        f"验收：**{report['result']}**。{report['scope']}。", "",
        "| 项目 | 实际结果 |", "| --- | --- |",
        f"| 契约覆盖 | {len(contracts)} 个命令版本，{len(catalogs)} 个服务 |",
        f"| 帮助查询 | {report['help']} |",
        f"| CLI 元工具 | {report['cli_meta_tools']} |",
        f"| 真实 API | {report['live']} |",
        f"| 独立验证记录 | {report['verification_states']} |",
        f"| 检查项 | {sum(checks.values())} 项，失败 {len(errors)} 项 |", "",
        "成功只表示本次请求成功。空列表不证明系统正常。未执行修改、扫描、主机作业、订购或消息发送。",
        "", "## 受阻项", "",
    ]
    for row in report["blocked"] + report["help_blocked"]:
        lines.append(f"- `{row['id']}`：{row.get('error_code') or ''} {row.get('error') or ''}")
    lines += ["", "## 写入后真实复核", ""]
    for item in recheck.get("checks", []):
        lines.append(f"- {'通过' if item['passed'] else '失败'}：{item['name']}")
    lines += ["", "## 本地检查", ""] + [f"- {k}：{v} 项。" for k, v in checks.items()]
    if errors:
        lines += ["", "## 未通过", ""] + ["- " + e for e in errors]
    (report_dir / "acceptance.md").write_text("\n".join(lines) + "\n")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return not errors


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evidence", type=Path, required=True, help="Directory containing the real CLI help and API records")
    parser.add_argument("--skill", type=Path, default=SKILL)
    parser.add_argument("--report-dir", type=Path)
    parser.add_argument("--recheck", type=Path)
    parser.add_argument("--write-verification", action="store_true", help="Refresh the independent verification snapshot, without running acceptance")
    args = parser.parse_args()
    if args.write_verification:
        data = json.loads(args.recheck.read_text()) if args.recheck and args.recheck.exists() else {}
        write_verification(args.evidence.resolve(), args.skill.resolve(), data)
    else:
        sys.exit(0 if validate(args.evidence.resolve(), args.skill.resolve(), args.report_dir, args.recheck) else 1)
