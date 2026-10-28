#!/usr/bin/env python3
"""Validate stable rule IDs, local pointers and bilingual dependency references.

This checks documentation structure, not semantic equivalence or cloud behavior.
"""
import argparse
import re
from pathlib import Path


def validate(root):
    expected = [f"G{i:02d}" for i in range(1, 13)]
    manifests = []
    for locale, name in [("en", "huawei-cloud-cost-estimation"),
                         ("zh-CN", "huawei-cloud-cost-estimation-cn")]:
        base = root / "skills" / locale / name
        gotchas = base / "references/gotchas.md"
        text = gotchas.read_text()
        assert re.findall(r"^- \*\*(G\d{2})", text, re.M) == expected, gotchas
        assert re.findall(r"^## ([A-E])\.", text, re.M) == list("ABCDE"), gotchas
        assert not (base / "gotchas.md").exists(), "Stale root gotchas.md"
        definitions = dict(re.findall(r"^\[([^\]]+)\]: (\S+)$", text, re.M))
        assert set(re.findall(r"\]\[([^\]]+)\]", text)) <= definitions.keys()
        manifest = {"sources": definitions, "references": {}}
        for path in sorted(base.rglob("*")):
            if not path.is_file() or path.suffix not in {".md", ".yml"}:
                continue
            body = path.read_text()
            refs = set(re.findall(r"(?<![A-Za-z0-9_])G\d{2}(?![A-Za-z0-9_])", body))
            assert refs <= set(expected), f"Unknown rule in {path}: {refs - set(expected)}"
            manifest["references"][str(path.relative_to(base))] = sorted(refs)
            pointers = re.findall(r"(?<![\w/])((?:\.\./)*(?:references/)?gotchas\.md)", body)
            for pointer in pointers:
                assert (path.parent / pointer).resolve() == gotchas.resolve(), (path, pointer)
            for link in re.findall(r"\]\(([^)]+)\)", body):
                if "://" not in link and not link.startswith("#"):
                    assert (path.parent / link.split("#")[0]).is_file(), (path, link)
        manifests.append(manifest)
    assert manifests[0] == manifests[1], "Gotchas sources or dependent rule IDs differ between locales"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    validate(args.root)
    print("OK: Gotchas IDs, local pointers, sources and bilingual dependencies validated")
