#!/usr/bin/env python3
"""Audit native KCS knowledge and cross-batch source provenance, without a model."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from foundry_common import FoundryError


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--kb", type=Path, required=True)
    args = parser.parse_args()
    try:
        from native_kcs import validate_native

        report = validate_native(args.kb.expanduser().resolve())
    except (FoundryError, OSError, ValueError) as exc:
        print(f"Native KCS validation failed: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
