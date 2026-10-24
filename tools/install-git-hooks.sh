#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
chmod +x "$ROOT/.githooks/pre-commit" "$ROOT/.githooks/pre-push"
git -C "$ROOT" config core.hooksPath .githooks
printf 'OK: local commit and push hygiene hooks enabled\n'
