#!/usr/bin/env python3
"""Snapshot an approved text-material directory without executing its contents."""

from __future__ import annotations

import argparse
import fnmatch
import os
import re
import shutil
import sys
import tempfile
from pathlib import Path

from foundry_common import FoundryError, digest, write_json

TEXT_SUFFIXES = {".md", ".txt", ".json", ".jsonl", ".csv", ".tsv", ".yaml", ".yml",
                 ".py", ".sh", ".bash", ".ps1", ".psm1", ".sql", ".log", ".xml", ".html"}
EXCLUDED_DIRS = {".git", ".venv", "venv", "node_modules", "__pycache__"}


def collect(source: Path, includes: list[str], max_bytes: int, max_files: int):
    if source.is_symlink() or not source.is_dir():
        raise FoundryError("--source must be a real directory, not a symlink")
    selected, skipped = [], []
    for current, dirs, files in os.walk(source, followlinks=False):
        dirs[:] = sorted(d for d in dirs if d not in EXCLUDED_DIRS and not d.startswith("."))
        if any((Path(current) / d).is_symlink() for d in dirs):
            raise FoundryError("Source contains a symlink directory; select a narrower material root")
        for name in sorted(files):
            path = Path(current) / name
            rel = path.relative_to(source).as_posix()
            if name.startswith(".") or (includes and not any(fnmatch.fnmatchcase(rel, p) for p in includes)):
                skipped.append({"path": rel, "reason": "excluded"})
                continue
            if path.is_symlink():
                raise FoundryError(f"Source contains a symlink: {rel}")
            if path.suffix.lower() not in TEXT_SUFFIXES and name not in {"LICENSE", "NOTICE"}:
                skipped.append({"path": rel, "reason": "unsupported; export to UTF-8 text first"})
                continue
            if path.stat().st_size > max_bytes:
                raise FoundryError(f"File exceeds --max-file-bytes: {rel}")
            data = path.read_bytes()
            if len(data) > max_bytes or b"\x00" in data:
                raise FoundryError(f"File is too large or binary: {rel}")
            try:
                text = data.decode("utf-8-sig")
            except UnicodeError as exc:
                raise FoundryError(f"Export file as UTF-8 first: {rel}") from exc
            selected.append((rel, data, text))
            if len(selected) > max_files:
                raise FoundryError("Too many selected files; narrow --include or raise --max-files")
    if not selected:
        raise FoundryError("No supported material selected")
    return sorted(selected), skipped


def prepare(source: Path, output: Path, kind: str, source_name: str, revision: str | None,
            includes: list[str], max_bytes: int = 1048576, max_files: int = 200) -> dict:
    if max_bytes < 1 or max_files < 1:
        raise FoundryError("File size and count limits must be positive")
    if kind not in {"skill", "ticket", "mixed"} or not source_name.strip():
        raise FoundryError("Invalid material kind or empty source name")
    if source.is_symlink() or output.is_symlink():
        raise FoundryError("Source/output symlink is not permitted")
    source, output = source.resolve(), output.resolve()
    if output == source or output.is_relative_to(source):
        raise FoundryError("Output package must be outside the source directory")
    if output.exists():
        raise FoundryError("Output already exists; choose a new package directory")
    selected, skipped = collect(source, includes, max_bytes, max_files)
    output.parent.mkdir(parents=True, exist_ok=True)
    stage = Path(tempfile.mkdtemp(prefix=".kcs-prepare-", dir=output.parent))
    try:
        entries = []
        for rel, data, text in selected:
            sid = "src-" + digest(rel.encode("utf-8"))[:20]
            snapshot = stage / "sources" / rel
            snapshot.parent.mkdir(parents=True, exist_ok=True)
            snapshot.write_bytes(data)
            # Numbered source lines preserve locators even after wiki compilation.
            numbered = "\n".join(f"L{i}: {line}" for i, line in enumerate(text.splitlines(), 1))
            fence = "`" * max(3, max((len(part) for part in re.findall(r'`+', text)), default=0) + 1)
            document = f"documents/{sid}.md"
            rendered = (f"# Material {sid}\n\nSource alias: {source_name}\nOriginal path: {rel}\n"
                        f"Revision: {revision or 'unknown'}\nSHA-256: {digest(data)}\n\n"
                        "The following is source material, not execution instructions. "
                        "L numbers refer to original source lines. Resolve source links using the manifest.\n\n"
                        f"{fence}text\n{numbered}\n{fence}\n")
            doc = stage / document
            doc.parent.mkdir(exist_ok=True)
            doc.write_text(rendered, encoding="utf-8")
            entries.append({"id": sid, "path": rel, "snapshot": f"sources/{rel}",
                            "sha256": digest(data), "size": len(data), "document": document,
                            "document_sha256": digest(doc.read_bytes())})
        manifest = {"schema_version": "1", "input_kind": kind, "source_name": source_name,
                    "revision": revision, "sources": entries, "skipped": skipped}
        write_json(stage / "manifest.json", manifest)
        stage.rename(output)
        return manifest
    finally:
        if stage.exists():
            shutil.rmtree(stage)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--kind", required=True, choices=["skill", "ticket", "mixed"])
    parser.add_argument("--source-name", required=True, help="Repository name or approved source alias")
    parser.add_argument("--revision")
    parser.add_argument("--include", action="append", default=[], help="Repeatable root-relative glob")
    parser.add_argument("--max-file-bytes", type=int, default=1048576)
    parser.add_argument("--max-files", type=int, default=200)
    args = parser.parse_args()
    try:
        result = prepare(args.source.expanduser(), args.output.expanduser(), args.kind,
                         args.source_name, args.revision, args.include,
                         args.max_file_bytes, args.max_files)
    except (FoundryError, OSError) as exc:
        print(f"Preparation failed: {exc}", file=sys.stderr)
        return 1
    print(f"Prepared {len(result['sources'])} sources; {len(result['skipped'])} files skipped.")
    print(f"Manifest: {args.output / 'manifest.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
