#!/usr/bin/env bash
set -euo pipefail
qa_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec python3 "$qa_dir/validate.py" "$@"
