#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
QA_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$ROOT/skills/en/huawei-cloud-billing-scout"

run_local_or_npx() {
  local bin=$1
  shift
  if command -v "$bin" >/dev/null 2>&1; then "$bin" "$@"
  else npx "$bin" "$@"; fi
}

python3 "$QA_DIR/bin/verify_ops.py" "$SKILL_DIR" "$QA_DIR/fixtures/ops_contracts.yml"
run_local_or_npx skills-ref validate "$SKILL_DIR"
run_local_or_npx markdownlint-cli2 --config "$QA_DIR/.markdownlint.json" "$SKILL_DIR/**/*.md"
skillcheck "$SKILL_DIR" --target-agent cursor --strict-cursor --min-desc-score 70

printf 'OK: huawei-cloud-billing-scout English validation passed\n'
