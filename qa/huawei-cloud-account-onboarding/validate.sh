#!/usr/bin/env bash
# 门禁：布局纯度 + 版本同步 + 跨层命令合同 + 脚本冒烟 + skills-ref/markdownlint/skillcheck。
# 真实 BSS 调用仅在 HUAWEICLOUD_ACCOUNT_ONBOARDING_REAL=1 时执行。
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
QA_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "$QA_DIR/../../skills/huawei-cloud-account-onboarding" && pwd)"

fail() { printf 'FAIL: %s\n' "$1" >&2; exit 1; }
need_cmd() { command -v "$1" >/dev/null 2>&1 || fail "missing command: $1"; }

run_local_or_npx() {
  local bin=$1; shift
  if command -v "$bin" >/dev/null 2>&1; then "$bin" "$@"
  else need_cmd npx; npx "$bin" "$@"; fi
}

# 安装载荷纯度：不含 eval/qa/gate；scripts/ 是运行时载荷（QR 渲染器），允许存在。
check_skill_layout() {
  local f
  for f in SKILL.md references/concepts.md references/commands.md \
           scripts/render-qr.ts scripts/package.json; do
    [[ -f "$SKILL_DIR/$f" ]] || fail "missing skill file: $f"
  done
  [[ -f "$QA_DIR/README.md" ]] || fail "missing QA README"
  [[ -f "$QA_DIR/evals/evals.json" ]] || fail "missing evals file"
  [[ -f "$QA_DIR/assertions/README.md" ]] || fail "missing assertions guide"
  [[ -f "$QA_DIR/fixtures/ops_contracts.yml" ]] || fail "missing ops contract fixture"
  [[ ! -f "$QA_DIR/evals.json" ]] || fail "duplicate eval source: $QA_DIR/evals.json"

  local item
  for item in .DS_Store .agents analysis evals qa tests .workspaces; do
    [[ ! -e "$SKILL_DIR/$item" ]] || fail "forbidden in skill dir: $item"
  done
  local sibling
  for sibling in "$SKILL_DIR"/*-workspace; do
    [[ -e "$sibling" ]] || continue
    fail "Skill Creator workspace belongs at repo root, not skills/: $(basename "$sibling")"
  done
  if git -C "$ROOT" ls-files --error-unmatch \
      "skills/huawei-cloud-account-onboarding/scripts/node_modules" >/dev/null 2>&1; then
    fail "node_modules must not be committed"
  fi
  # 旧 mock 载荷不得回归
  local stale
  for stale in scripts/mock-server.js scripts/create-verification.js \
               scripts/poll-verification.js references/api-contract.md; do
    [[ ! -e "$SKILL_DIR/$stale" ]] || fail "stale mock payload still present: $stale"
  done

  # 技能面只讲 hcloud 命令，不暴露 OpenAPI 路径或 HTTP 动词
  rg -q '/v2/customers|bss\.myhuaweicloud\.com|X-Auth-Token' "$SKILL_DIR" --glob '!node_modules' \
    && fail "skill payload must speak hcloud commands, not raw OpenAPI paths"

  # SKILL.md 是入口不是全文：正文保持精炼，细节沉到 references/
  local body_lines
  body_lines=$(awk 'f>1 && NF {n++} /^---$/{f++} END{print n+0}' "$SKILL_DIR/SKILL.md")
  [[ "$body_lines" -le 25 ]] \
    || fail "SKILL.md body is $body_lines non-empty lines; keep it an entry point (<=25)"
}

check_version_sync() {
  need_cmd python3
  QA_DIR="$QA_DIR" ROOT="$ROOT" SKILL_DIR="$SKILL_DIR" python3 - <<'PY'
import os, sys
from pathlib import Path
try:
    import yaml
except ImportError:
    sys.exit("FAIL: PyYAML required for version sync check")
qa = Path(os.environ["QA_DIR"]); root = Path(os.environ["ROOT"]); skill = Path(os.environ["SKILL_DIR"])
expected = (qa / "VERSION").read_text(encoding="utf-8").strip()
catalog = yaml.safe_load((root / "docs/catalog.yml").read_text(encoding="utf-8"))
entry = next(x for x in catalog.get("skills", []) if x.get("id") == "huawei-cloud-account-onboarding")
if entry.get("version") != expected:
    sys.exit(f"FAIL: docs/catalog.yml version {entry.get('version')!r} != qa/VERSION ({expected})")
meta = yaml.safe_load(skill.joinpath("SKILL.md").read_text(encoding="utf-8").split("---", 2)[1])
if (meta.get("metadata") or {}).get("version") != expected:
    sys.exit(f"FAIL: SKILL.md metadata.version != qa/VERSION ({expected})")
if "license" in meta:
    sys.exit("FAIL: SKILL.md frontmatter must not declare license (ClawHub MIT-0 conflict)")
doc = root / "docs/skills/huawei-cloud-account-onboarding.md"
if expected not in doc.read_text(encoding="utf-8"):
    sys.exit(f"FAIL: docs/skills page does not mention version {expected}")
PY
}

# 跨层合同：fixture 中的 operation / URI / 字段 / 枚举必须写进 commands.md。
check_ops_contract() {
  need_cmd python3
  QA_DIR="$QA_DIR" SKILL_DIR="$SKILL_DIR" python3 - <<'PY'
import os, sys
from pathlib import Path
try:
    import yaml
except ImportError:
    sys.exit("FAIL: PyYAML required for ops contract check")
qa = Path(os.environ["QA_DIR"]); skill = Path(os.environ["SKILL_DIR"])
spec = yaml.safe_load((qa / "fixtures/ops_contracts.yml").read_text(encoding="utf-8"))
commands = (skill / "references/commands.md").read_text(encoding="utf-8")
concepts = (skill / "references/concepts.md").read_text(encoding="utf-8")
missing = []
for op, c in (spec.get("operations") or {}).items():
    if op not in commands:
        missing.append(f"operation not documented: {op}")
    for field, fs in (c.get("response_fields") or {}).items():
        if field not in commands:
            missing.append(f"{op}: response field {field!r}")
        for value, label in (fs.get("enum") or {}).items():
            if f"`{value}`" not in commands or label not in commands:
                missing.append(f"{op}.{field}: enum {value} ({label})")
for op in spec.get("refused_operations") or []:
    if op not in commands:
        missing.append(f"refused op not documented: {op}")
if str(spec["throttle_per_second"]) not in commands:
    missing.append("throttle rate not documented")
if spec["cli_region"] not in commands:
    missing.append(f"cli_region {spec['cli_region']} not documented")
# 门禁事实必须同时出现在概念层
if "不校验实名状态" not in concepts:
    missing.append("concepts.md must state the QR op does not gate on status")
if missing:
    sys.exit("FAIL: commands.md out of sync with ops_contracts.yml:\n  " + "\n  ".join(missing))
PY
}

# 薄马具冒烟：类型检查 + 渲染 + 参数校验退出码。脚本不得触碰 hcloud 或文件系统。
check_scripts() {
  need_cmd node
  [[ -d "$SKILL_DIR/scripts/node_modules" ]] \
    || (cd "$SKILL_DIR/scripts" && npm install --no-fund --no-audit >/dev/null)

  # 纯度：只允许 qrcode 一个 import；不得出现子进程、文件写入、环境变量或网络调用。
  local imports
  imports=$(rg -o "^import .* from '([^']+)'" -r '$1' "$SKILL_DIR/scripts/render-qr.ts")
  [[ "$imports" == "qrcode" ]] \
    || fail "render-qr.ts must import qrcode only, got: ${imports//$'\n'/, }"
  rg -q "child_process|node:fs|writeFile|process\.env|fetch\(|require\(" \
    "$SKILL_DIR/scripts/render-qr.ts" \
    && fail "render-qr.ts must stay pure: no subprocess, file write, env access or network"

  local out
  out=$(cd "$SKILL_DIR/scripts" && npx tsx render-qr.ts \
    'https://auth.huaweicloud.com/authui/thirdLogin?idp=CHNIDP&ticket=GATE_SMOKE') \
    || fail "render-qr.ts failed on a valid https URL"
  rg -q '\u2580' <<<"$out" || fail "render-qr.ts produced no QR modules"
  rg -q '单次使用' <<<"$out" || fail "render-qr.ts must warn the QR is single-use"

  local code=0
  (cd "$SKILL_DIR/scripts" && npx tsx render-qr.ts >/dev/null 2>&1) || code=$?
  [[ $code -eq 2 ]] || fail "render-qr.ts must exit 2 without an argument (got $code)"
  code=0
  (cd "$SKILL_DIR/scripts" && npx tsx render-qr.ts 'http://example.com' >/dev/null 2>&1) || code=$?
  [[ $code -eq 2 ]] || fail "render-qr.ts must exit 2 on non-https URL (got $code)"
}

# 真实 BSS 只读冒烟（默认跳过）。凭据由用户的 hcloud profile 提供。
check_real_bss() {
  if [[ "${HUAWEICLOUD_ACCOUNT_ONBOARDING_REAL:-0}" != "1" ]]; then
    printf 'SKIP: real BSS smoke (set HUAWEICLOUD_ACCOUNT_ONBOARDING_REAL=1 to enable)\n'
    return 0
  fi
  need_cmd hcloud
  local status
  status=$(hcloud BSS ShowRealNameAuthStatus --cli-region=cn-north-1 \
    --cli-output=json --cli-query=verified_status 2>&1) \
    || fail "real BSS ShowRealNameAuthStatus failed: $status"
  rg -q '^-?[0-9]+$' <<<"$status" \
    || fail "verified_status is not an integer: $status"
  case "$status" in
    -1|0|1|2) printf 'OK: real BSS verified_status=%s\n' "$status" ;;
    *) fail "verified_status outside documented enum: $status" ;;
  esac
}

need_cmd rg
check_skill_layout
check_version_sync
check_ops_contract
check_scripts
check_real_bss
run_local_or_npx skills-ref validate "$SKILL_DIR"
(cd "$SKILL_DIR" && run_local_or_npx markdownlint-cli2 \
  --config "$QA_DIR/.markdownlint.json" "**/*.md" "!scripts/node_modules")
need_cmd skillcheck
skillcheck "$SKILL_DIR" --target-agent cursor --strict-cursor --min-desc-score 70

printf 'OK: huawei-cloud-account-onboarding validation passed\n'
