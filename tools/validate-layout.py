#!/usr/bin/env python3
"""Check category directories, installer metadata, and maintained local links."""
import argparse
import json
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit

import yaml

CATEGORIES = ("engineering", "in-progress", "productivity", "misc")
PUBLISHED = ("engineering", "productivity", "misc")


def validate(root):
    for name in CATEGORIES:
        if not (root / name).is_dir():
            raise ValueError(f"missing category directory: {name}")
    for name in ("skills", "development"):
        if (root / name).exists():
            raise ValueError(f"legacy directory remains: {name}")

    config = json.loads((root / "skills.sh.json").read_text())
    if config.get("paths") != [f"./{name}" for name in PUBLISHED]:
        raise ValueError("skills.sh.json paths must list the published categories")
    catalog = yaml.safe_load((root / "catalog.yml").read_text())["skills"]
    grouped = [name for group in config["groupings"] for name in group["skills"]]
    if len(grouped) != len(set(grouped)) or set(grouped) != {item["id"] for item in catalog}:
        raise ValueError("installer groupings and catalog skill IDs differ")
    for item in catalog:
        skill_md = root / item["path"] / "SKILL.md"
        meta = yaml.safe_load(skill_md.read_text().split("---", 2)[1])
        homepage = meta["metadata"]["openclaw"]["homepage"]
        if homepage != f"https://github.com/concept-git/cloud-concept-skills/tree/main/{item['path']}":
            raise ValueError(f"skill homepage differs from catalog path: {item['id']}")

    documents = [root / name for name in ("README.md", "README-CN.md", "CLAUDE.md")]
    for category in CATEGORIES:
        documents.extend(path for path in (root / category).rglob("*.md")
                         if not {"vendor", "node_modules", "__pycache__"}
                         & set(path.relative_to(root / category).parts))
    for document in documents:
        for target in re.findall(r"\]\(([^\s)]+)\)", document.read_text()):
            url = urlsplit(target)
            if url.scheme or url.netloc or not url.path:
                continue
            if not (document.parent / unquote(url.path)).exists():
                raise ValueError(f"broken local link in {document.relative_to(root)}: {target}")
    return len(catalog), len(documents)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    try:
        skills, documents = validate(args.root)
    except (OSError, KeyError, ValueError, yaml.YAMLError) as error:
        raise SystemExit(f"FAIL: {error}")
    print(f"OK: category layout, {skills} installer entries and local links in {documents} documents validated")
