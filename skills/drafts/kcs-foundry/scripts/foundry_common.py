"""Shared, dependency-free material and path checks for KCS Foundry."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path, PurePosixPath


class FoundryError(ValueError):
    """An actionable input or artifact error."""


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def relative_file(root: Path, value: str) -> Path:
    """Resolve a package-relative file, rejecting escapes and symlinks."""
    if not isinstance(value, str) or not value or "\\" in value:
        raise FoundryError("Expected a nonempty POSIX relative file path")
    rel = PurePosixPath(value)
    if rel.is_absolute() or ".." in rel.parts or value != rel.as_posix():
        raise FoundryError(f"Invalid relative path: {value}")
    root = root.resolve()
    path = root
    for part in rel.parts:
        path = path / part
        if path.is_symlink():
            raise FoundryError(f"Symlink is not permitted: {value}")
    if not path.resolve().is_relative_to(root):
        raise FoundryError(f"Path escapes root: {value}")
    return path


def load_json(path: Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise FoundryError(f"Cannot read JSON: {path.name}") from exc
    if not isinstance(value, dict):
        raise FoundryError(f"Expected JSON object: {path.name}")
    return value


def write_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def validate_slug(value: str) -> str:
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", value) or len(value) > 80:
        raise FoundryError("run-id must be lowercase letters/digits separated by hyphens, <=80 chars")
    return value


def load_package(package: Path) -> dict:
    """Validate both immutable source snapshots and documents prepared for OpenKB."""
    manifest = load_json(relative_file(package, "manifest.json"))
    if manifest.get("schema_version") != "1":
        raise FoundryError("Unsupported material manifest schema")
    if manifest.get("input_kind") not in ("skill", "ticket", "mixed"):
        raise FoundryError("Invalid input_kind")
    if not isinstance(manifest.get("source_name"), str) or not manifest["source_name"].strip():
        raise FoundryError("Missing source_name")
    revision = manifest.get("revision")
    if "revision" not in manifest or (revision is not None and not isinstance(revision, str)):
        raise FoundryError("revision must be a string or null")
    entries = manifest.get("sources")
    if not isinstance(entries, list) or not entries:
        raise FoundryError("Material package has no sources")
    seen_ids, seen_paths, seen_documents = set(), set(), set()
    for entry in entries:
        if not isinstance(entry, dict):
            raise FoundryError("Invalid source entry")
        sid, original, document = (entry.get(k) for k in ("id", "path", "document"))
        if not isinstance(sid, str) or not sid or sid in seen_ids:
            raise FoundryError("Missing or duplicate source id")
        if not isinstance(original, str) or original in seen_paths:
            raise FoundryError("Missing or duplicate source path")
        # Validate logical original paths as well as on-disk snapshot paths.
        relative_file(package / "sources", original)
        if not isinstance(document, str) or document in seen_documents:
            raise FoundryError("Missing or duplicate document path")
        if not document.startswith("documents/") or not document.endswith(".md"):
            raise FoundryError("Prepared documents must be documents/*.md")
        for key, hash_key in (("snapshot", "sha256"), ("document", "document_sha256")):
            path = relative_file(package, entry.get(key))
            expected = entry.get(hash_key)
            if not isinstance(expected, str) or not re.fullmatch(r"[0-9a-f]{64}", expected):
                raise FoundryError(f"Missing valid {hash_key}")
            if not path.is_file() or digest(path.read_bytes()) != expected:
                raise FoundryError(f"Material missing or changed: {entry.get(key)}")
        if entry["snapshot"] != f"sources/{original}":
            raise FoundryError("Source snapshot path does not match original path")
        seen_ids.add(sid)
        seen_paths.add(original)
        seen_documents.add(document)
    return manifest
