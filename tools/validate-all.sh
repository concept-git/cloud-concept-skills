#!/usr/bin/env bash
# Validate installed locale pairs; development QA requires explicit local evidence.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
status=0
export PYTHONDONTWRITEBYTECODE=1

python3 "$ROOT/tools/check-repository-hygiene.py"

python3 "$ROOT/tools/validate-localization.py"

while IFS= read -r validate; do
  name=$(basename "$(dirname "$validate")")
  printf '==> %s\n' "$name"
  if ! "$validate"; then
    status=1
  fi
  printf '\n'
done < <(find "$ROOT/qa/en" "$ROOT/qa/cn" -mindepth 2 -maxdepth 2 -name validate.sh -type f | sort)

[[ "$status" -eq 0 ]] || exit "$status"
printf 'OK: all skill QA passed\n'
