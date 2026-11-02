#!/usr/bin/env python3
"""Validate KCS artifacts against a trusted prepared-material manifest, offline."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

from foundry_common import FoundryError, load_package, load_json, relative_file, write_json

BASES = {"source_guidance", "recorded_observation", "confirmed_in_source", "extraction_inference"}
STATUSES = {"passed", "failed", "partial", "not_run"}


def nonempty(value) -> bool:
    return isinstance(value, str) and bool(value.strip())


def prose(text: str) -> str:
    """Ignore fenced examples when checking article structure and links."""
    result, fence = [], None
    for line in text.splitlines():
        match = re.match(r"^\s*(`{3,}|~{3,})", line)
        if match:
            mark = match.group(1)
            if fence is None:
                fence = (mark[0], len(mark))
            elif mark[0] == fence[0] and len(mark) >= fence[1]:
                fence = None
        elif fence is None:
            result.append(line)
    return "\n".join(result)


def check_article(path: Path, root: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    errors = []
    if not re.match(r"\A---\nstatus: draft\n---\n", text):
        errors.append("frontmatter must contain only status: draft")
    body = prose(text)
    if len(re.findall(r"^# \S.*$", body, re.M)) != 1:
        errors.append("expected one H1")
    if re.findall(r"^## (.+?)\s*$", body, re.M) != ["Issue", "Environment", "Resolution", "Cause"]:
        errors.append("expected four ordered KCS H2 fields")
    sections = re.split(r"^## (?:Issue|Environment|Resolution|Cause)\s*$", body, flags=re.M)
    if len(sections) != 5 or any(not s.strip() for s in sections[1:]):
        errors.append("all four KCS fields must be nonempty")
    if "## Resolution\n" in body:
        resolution = body.split("## Resolution\n", 1)[1].split("## Cause", 1)[0]
        if not re.search(r"^\d+\. \S", resolution, re.M):
            errors.append("Resolution needs numbered steps")
    # Resolve file links without fetching remote resources or trusting generated paths.
    for dest in re.findall(r"\]\(([^)]+)\)", body):
        dest = dest.strip().strip("<>")
        parts = urlsplit(dest)
        if parts.scheme in {"https", "http"} or dest.startswith("#"):
            continue
        try:
            if parts.scheme:
                raise FoundryError("unsupported link scheme")
            raw = unquote(parts.path)
            candidate = path.parent / raw
            if Path(raw).is_absolute() or not candidate.resolve().is_relative_to(root.resolve()):
                raise FoundryError("file link escapes output root")
            rel = candidate.resolve().relative_to(root.resolve()).as_posix()
            if not relative_file(root, rel).is_file():
                raise FoundryError("file link target missing")
        except (FoundryError, ValueError):
            errors.append(f"invalid or missing file link: {dest}")
    return errors


def check_evidence(data: dict, article_rel: str, manifest: dict) -> list[str]:
    errors = []
    if data.get("schema_version") != "1" or data.get("article") != article_rel:
        errors.append("evidence schema or article pairing mismatch")
    if data.get("input_kind") != manifest["input_kind"] or not nonempty(data.get("target_platform")):
        errors.append("input_kind mismatch or missing target_platform")
    if data.get("completeness") not in {"complete", "partial"}:
        errors.append("invalid completeness")
    known = {s["path"]: s for s in manifest["sources"]}
    sources = data.get("sources")
    ids = set()
    if not isinstance(sources, list) or not sources:
        errors.append("sources must be a nonempty list")
        sources = []
    for source in sources:
        if not isinstance(source, dict):
            errors.append("invalid evidence source")
            continue
        sid = source.get("id")
        if not nonempty(sid) or sid in ids:
            errors.append("missing or duplicate evidence source id")
        elif isinstance(sid, str):
            ids.add(sid)
        original = known.get(source.get("path"))
        if original is None or source.get("sha256") != original["sha256"]:
            errors.append("source path/hash is not in the trusted manifest")
        if source.get("repository_or_alias") != manifest["source_name"]:
            errors.append("source alias differs from trusted manifest")
        if source.get("revision") != manifest["revision"]:
            errors.append("source revision differs from trusted manifest")
        if not nonempty(source.get("kind")):
            errors.append("source kind missing")
        locators = source.get("locators_read")
        if not isinstance(locators, list) or not locators or not all(nonempty(v) for v in locators):
            errors.append("source read locators missing")
    claims = data.get("claims")
    claim_ids = set()
    if not isinstance(claims, list) or not claims:
        errors.append("claims must be a nonempty list")
        claims = []
    for claim in claims:
        if not isinstance(claim, dict):
            errors.append("invalid claim")
            continue
        cid = claim.get("id")
        if not nonempty(cid) or cid in claim_ids:
            errors.append("missing or duplicate claim id")
        elif isinstance(cid, str):
            claim_ids.add(cid)
        if not all(nonempty(claim.get(k)) for k in ("article_locator", "statement")):
            errors.append("claim statement or article locator missing")
        if claim.get("basis") not in BASES:
            errors.append("invalid claim basis")
        refs = claim.get("refs")
        if not isinstance(refs, list) or not refs:
            errors.append("claim has no source refs")
            continue
        for ref in refs:
            if not isinstance(ref, dict) or ref.get("source_id") not in ids or not nonempty(ref.get("locator")):
                errors.append("claim source ref does not resolve")
    gaps = data.get("gaps")
    if not isinstance(gaps, list):
        errors.append("gaps must be a list")
        gaps = []
    if data.get("completeness") == "partial" and not gaps:
        errors.append("partial output needs an explicit gap")
    for gap in gaps:
        if not isinstance(gap, dict) or not all(nonempty(gap.get(k)) for k in ("area", "detail")):
            errors.append("invalid gap")
            continue
        affected = gap.get("affected_claims")
        if not isinstance(affected, list) or any(c not in claim_ids for c in affected):
            errors.append("gap claim refs do not resolve")
    checks = data.get("checks")
    if not isinstance(checks, dict):
        errors.append("checks missing")
        checks = {}
    for name in ("structure", "source_review", "runtime_validation"):
        check = checks.get(name)
        if not isinstance(check, dict) or check.get("status") not in STATUSES or not nonempty(check.get("detail")):
            errors.append(f"invalid check: {name}")
    if isinstance(checks.get("runtime_validation"), dict) and checks["runtime_validation"].get("status") != "not_run":
        errors.append("this extraction workflow cannot claim runtime validation")
    return errors


def validate(output: Path, manifest: dict) -> dict:
    output = output.resolve()
    errors, warnings, articles = [], [], []
    if not output.is_dir():
        errors.append("output directory missing")
    else:
        for path in output.rglob("*"):
            if path.is_symlink():
                errors.append(f"symlink in output: {path.relative_to(output)}")
            elif path.is_file():
                rel = path.relative_to(output).as_posix()
                if rel not in {"extraction-report.md", "validation.json"} and not re.fullmatch(
                    r"(?:articles/[a-z0-9]+(?:-[a-z0-9]+)*\.md|evidence/[a-z0-9]+(?:-[a-z0-9]+)*\.json)", rel
                ):
                    errors.append(f"unexpected artifact: {rel}")
        report_path = relative_file(output, "extraction-report.md")
        if not report_path.is_file():
            errors.append("extraction-report.md missing")
        else:
            try:
                if not report_path.read_text(encoding="utf-8").strip():
                    errors.append("extraction-report.md is empty")
            except UnicodeError:
                errors.append("extraction-report.md is not UTF-8")
        article_dir = relative_file(output, "articles")
        evidence_dir = relative_file(output, "evidence")
        for path in sorted(article_dir.glob("*.md")):
            rel = path.relative_to(output).as_posix()
            articles.append(rel)
            try:
                path = relative_file(output, rel)
                errors.extend(f"{rel}: {e}" for e in check_article(path, output))
                evidence = load_json(relative_file(output, f"evidence/{path.stem}.json"))
                errors.extend(f"{rel}: {e}" for e in check_evidence(evidence, rel, manifest))
                if evidence.get("completeness") == "partial":
                    warnings.append(f"{rel}: partial material; review gaps")
            except (FoundryError, OSError, UnicodeError, TypeError) as exc:
                errors.append(f"{rel}: invalid article/evidence ({type(exc).__name__})")
        if not articles:
            errors.append("no KCS articles generated")
        for path in evidence_dir.glob("*.json"):
            if not relative_file(output, f"articles/{path.stem}.md").is_file():
                errors.append(f"orphan evidence: {path.name}")
    return {"valid": not errors, "articles": articles, "errors": errors, "warnings": warnings,
            "source_semantic_review": "not_run", "runtime_validation": "not_run",
            "note": "Structural/provenance checks only; human source review and runtime validation are separate."}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--kb", type=Path, help="Audit native KCS wiki and cross-batch provenance")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--materials", type=Path, help="For legacy export: trusted material package")
    args = parser.parse_args()
    if args.kb:
        if args.output or args.materials:
            parser.error("Use --kb for native audit, or --output with --materials for legacy exports")
        try:
            from native_kcs import validate_native

            report = validate_native(args.kb.expanduser().resolve())
        except (FoundryError, OSError, ValueError) as exc:
            print(f"Native KCS validation failed: {exc}", file=sys.stderr)
            return 1
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0 if report["valid"] else 1
    if not args.output or not args.materials:
        parser.error("Legacy export validation needs both --output and --materials")
    try:
        manifest = load_package(args.materials.expanduser().resolve())
        report = validate(args.output.expanduser(), manifest)
    except (FoundryError, OSError) as exc:
        print(f"Validation failed: {exc}", file=sys.stderr)
        return 1
    write_json(relative_file(args.output.resolve(), "validation.json"), report)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
