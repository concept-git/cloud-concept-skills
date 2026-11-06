"""Durable, cross-batch provenance and validation for native OpenKB KCS nodes."""

from __future__ import annotations

import os
import sys
from pathlib import Path

from foundry_common import FoundryError, load_json, relative_file, validate_slug, write_json

VENDOR = Path(__file__).resolve().parent.parent / "vendor" / "openkb"


def openkb_modules():
    os.environ["LITELLM_LOCAL_MODEL_COST_MAP"] = "True"
    if str(VENDOR) not in sys.path:
        sys.path.insert(0, str(VENDOR))
    try:
        from openkb import kcs
        from openkb.schema import get_agents_md
    except ImportError as exc:
        raise FoundryError("Native wiki checks require the OpenKB YAML/locking dependencies") from exc
    return kcs, get_agents_md


def record_batch(kb: Path, run_id: str, manifest: dict, completed: list[str]) -> None:
    """Persist accepted original->compiled identities, not a model-written source list."""
    validate_slug(run_id)
    kcs, _ = openkb_modules()
    registry = load_json(relative_file(kb, ".openkb/hashes.json"))
    items = []
    for source in manifest["sources"]:
        if source["id"] not in completed:
            continue
        metadata = registry.get(source["document_sha256"])
        if not isinstance(metadata, dict) or not isinstance(metadata.get("doc_name"), str):
            raise FoundryError("Imported document is missing its OpenKB registry identity")
        summary = f"summaries/{metadata['doc_name']}.md"
        if not relative_file(kb / "wiki", summary).is_file():
            raise FoundryError("Imported document has no compiled summary")
        hashes = kcs.source_fingerprints(kb / "wiki", [summary])
        items.append({"summary": summary, "repository_or_alias": manifest["source_name"],
                      "revision": manifest["revision"], "path": source["path"],
                      "sha256": source["sha256"], "document_sha256": source["document_sha256"],
                      "source_snapshot": f"raw/kcs-inputs/{run_id}/{source['snapshot']}",
                      "wiki_source_sha256": hashes[summary]})
    write_json(relative_file(kb, f"provenance/batches/{run_id}.json"),
               {"schema_version": "1", "run_id": run_id, "input_kind": manifest["input_kind"],
                "complete": len(items) == len(manifest["sources"]), "sources": items,
                "skipped": manifest.get("skipped", [])})


def catalog_for_kb(kb: Path) -> dict[str, dict]:
    kcs, _ = openkb_modules()
    variants: dict[str, list[dict]] = {}
    for path in sorted((kb / "provenance" / "batches").glob("*.json")):
        path = relative_file(kb, path.relative_to(kb).as_posix())
        data = load_json(path)
        if data.get("schema_version") != "1" or not isinstance(data.get("sources"), list):
            raise FoundryError("Invalid durable provenance batch")
        for item in data["sources"]:
            if not isinstance(item, dict) or not isinstance(item.get("summary"), str):
                raise FoundryError("Invalid durable provenance entry")
            variants.setdefault(item["summary"], []).append(item)
    catalog = {}
    for summary, items in variants.items():
        try:
            current = kcs.source_fingerprints(kb / "wiki", [summary])[summary]
        except (ValueError, OSError):
            continue
        matches = [item for item in items if item.get("wiki_source_sha256") == current]
        if matches:
            catalog[summary] = matches[0]
    return catalog


def validate_native(kb: Path) -> dict:
    kcs, get_agents_md = openkb_modules()
    from openkb.config import resolve_effective_config
    from openkb.locks import kb_read_lock

    if kcs.resolve_profile(resolve_effective_config(kb)[0]) != "kcs":
        raise FoundryError("Native mode requires knowledge_profile: kcs")
    with kb_read_lock(kb / ".openkb"):
        get_agents_md(kb / "wiki")  # Reject a stale generic schema before accepting cards.
        return kcs.audit_wiki(kb / "wiki", catalog_for_kb(kb))
