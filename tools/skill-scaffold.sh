#!/usr/bin/env bash
# Scaffold one English/default and Simplified-Chinese skill pair.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BASE_NAME="${1:?usage: skill-scaffold.sh <base-skill-name>}"

if [[ ! "$BASE_NAME" =~ ^[a-z0-9]+(-[a-z0-9]+)*$ || "$BASE_NAME" == *-cn ]]; then
  printf 'invalid base skill name (kebab-case, without -cn): %s\n' "$BASE_NAME" >&2
  exit 1
fi

replace() {
  local file=$1 old=$2 new=$3
  if sed --version >/dev/null 2>&1; then
    sed -i "s|$old|$new|g" "$file"
  else
    sed -i '' "s|$old|$new|g" "$file"
  fi
}

for locale in en cn; do
  if [[ "$locale" == en ]]; then
    name=$BASE_NAME
    language=en
    translation_of="${BASE_NAME}-cn"
  else
    name="${BASE_NAME}-cn"
    language=zh-CN
    translation_of=$BASE_NAME
  fi

  skill_dir="$ROOT/skills/$locale/$name"
  qa_dir="$ROOT/qa/$locale/$name"
  [[ ! -e "$skill_dir" && ! -e "$qa_dir" ]] || {
    printf 'pair already exists: %s\n' "$name" >&2
    exit 1
  }

  mkdir -p "$(dirname "$skill_dir")" "$(dirname "$qa_dir")"
  cp -R "$ROOT/template/skill" "$skill_dir"
  mkdir -p "$qa_dir/evals" "$qa_dir/assertions"
  cp "$ROOT/template/qa/validate.sh" "$qa_dir/validate.sh"
  cp "$ROOT/template/qa/README.md" "$qa_dir/README.md"
  cp "$ROOT/template/qa/evals/evals.json" "$qa_dir/evals/evals.json"
  cp "$ROOT/template/qa/assertions/README.md" "$qa_dir/assertions/README.md"
  chmod +x "$qa_dir/validate.sh"

  for file in "$skill_dir/SKILL.md" "$qa_dir/validate.sh" "$qa_dir/README.md" "$qa_dir/evals/evals.json"; do
    replace "$file" skill-template "$name"
    replace "$file" __SKILL_NAME__ "$name"
  done
  replace "$qa_dir/validate.sh" '/../.."' '/../../.."'
  replace "$qa_dir/validate.sh" '../../skills/' "../../../skills/$locale/"

  python3 - "$skill_dir/SKILL.md" "$language" "$translation_of" <<'PY'
from pathlib import Path
import sys
path = Path(sys.argv[1])
text = path.read_text(encoding="utf-8")
text = text.replace("metadata:\n", f"metadata:\n  language: {sys.argv[2]}\n  translation_of: {sys.argv[3]}\n", 1)
path.write_text(text, encoding="utf-8")
PY
done

printf 'Scaffolded locale pair: %s + %s-cn\n' "$BASE_NAME" "$BASE_NAME"
printf 'Next: author both SKILL.md files, add docs/catalog entries, then run tools/validate-all.sh\n'
