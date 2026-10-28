#!/usr/bin/env python3
"""Bound estimation-skill context growth without a tokenizer dependency.

UTF-8 bytes are a portable growth signal, not model-token counts. Budgets cover
full-file reads, including gotchas; optional selective reads may cost less.
An intentional expansion must review these ceilings and the behavior evals.
"""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1] / "skills"
LIMITS = {
    "en": {"entry": 4500, "gotchas": 7500, "quote": 20000, "create": 36000, "package": 45000},
    "zh-CN": {"entry": 4000, "gotchas": 6500, "quote": 18000, "create": 35000, "package": 43000},
}


def measure(base):
    files = {str(p.relative_to(base)): len(p.read_bytes())
             for p in base.rglob("*") if p.is_file() and p.suffix in {".md", ".yml"}}
    quote = sum(files[p] for p in ["SKILL.md", "references/gotchas.md", "references/pricing/commands.md"])
    return {"entry": files["SKILL.md"], "gotchas": files["references/gotchas.md"], "quote": quote,
            "create": quote + files["references/lifecycle/concepts.md"]
                      + files["references/lifecycle/commands.md"],
            "package": sum(files.values())}


def main():
    failures = []
    for locale, limits in LIMITS.items():
        name = "huawei-cloud-cost-estimation" + ("-cn" if locale == "zh-CN" else "")
        for scope, actual in measure(ROOT / locale / name).items():
            limit = limits[scope]
            print(f"{locale} {scope}: {actual}/{limit} UTF-8 bytes")
            if actual > limit:
                failures.append(f"{locale} {scope} exceeds context budget by {actual - limit} bytes")
    if failures:
        print("FAIL: " + "; ".join(failures), file=sys.stderr)
        return 1
    print("OK: estimation skill context budgets passed (bytes, not model tokens)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
