#!/usr/bin/env python3
"""Compile materials directly into native KCS concepts with durable provenance."""

from __future__ import annotations
import argparse
import datetime as dt
import json
import os
import shutil
import sys
import uuid
from pathlib import Path
from foundry_common import (
    FoundryError,
    digest,
    load_package,
    relative_file,
    validate_slug,
    write_json,
)

FOUNDRY = Path(__file__).resolve().parent.parent
VENDOR = FOUNDRY / "vendor" / "openkb"


class OpenKBBackend:
    """Keep pinned upstream API usage in one adapter; import only for live runs."""

    def configure(self, kb: Path) -> None:
        os.environ["LITELLM_LOCAL_MODEL_COST_MAP"] = "True"
        sys.path.insert(0, str(VENDOR))
        try:
            import openkb
            from openkb.cli import _setup_llm_key, add_single_file
            from openkb.config import resolve_credential_bundle, resolve_effective_config
            from openkb.kcs import resolve_profile
        except ImportError as exc:
            raise FoundryError(
                "OpenKB dependencies unavailable; install the pinned vendor package first"
            ) from exc
        if not Path(openkb.__file__).resolve().is_relative_to(VENDOR.resolve()):
            raise FoundryError("A different OpenKB is already imported; use a fresh process")
        (config, sources) = resolve_effective_config(kb)
        if (
            sources.get("model") != "kb"
            or not isinstance(config.get("model"), str)
            or (not config["model"].strip())
        ):
            raise FoundryError("Set an explicit model in this KB's .openkb/config.yaml first")
        _setup_llm_key(kb)
        self.profile = resolve_profile(config)
        self.bundle = resolve_credential_bundle(kb)
        self.add_single_file = add_single_file

    def ingest(self, path: Path, kb: Path) -> str:
        return self.add_single_file(path, kb, bundle=self.bundle)


def tree_hashes(root: Path) -> dict[str, str]:
    result = {}
    for path in sorted(root.rglob("*")):
        if path.is_symlink():
            raise FoundryError("Symlink in skill directory")
        if path.is_file():
            result[path.relative_to(root).as_posix()] = digest(path.read_bytes())
    return result


def plan_run(package: Path, kb: Path, run_id: str, scenario: str) -> tuple[dict, dict]:
    manifest = load_package(package)
    validate_slug(run_id)
    if not scenario.strip():
        raise FoundryError("Scenario must not be empty")
    if package == kb or package.is_relative_to(kb) or kb.is_relative_to(package):
        raise FoundryError("Keep the trusted material package separate from the KB")
    for rel in (
        f"output/kcs/{run_id}",
        f"output/kcs-inputs/{run_id}",
        f"raw/kcs-inputs/{run_id}",
        f".openkb/kcs-foundry/{run_id}",
    ):
        if relative_file(kb, rel).exists():
            raise FoundryError(
                "run-id already exists; choose a new one (no implicit overwrite/retry)"
            )
    plan = {
        "run_id": run_id,
        "mode": "native",
        "scenario": scenario,
        "input_kind": manifest["input_kind"],
        "source_count": len(manifest["sources"]),
        "output": f"output/kcs/{run_id}",
    }
    return (manifest, plan)


def run_pipeline(package: Path, kb: Path, run_id: str, scenario: str, backend=None) -> dict:
    (package, kb) = (package.resolve(), kb.resolve())
    (manifest, plan) = plan_run(package, kb, run_id, scenario)
    if not relative_file(kb, ".openkb/config.yaml").is_file():
        raise FoundryError("Knowledge base not initialized: run openkb init --knowledge-profile kcs --model <approved-model> --language zh inside the target KB directory first")
    backend = backend or OpenKBBackend()
    backend.configure(kb)
    if getattr(backend, "profile", None) != "kcs":
        raise FoundryError(
            "Native mode requires knowledge_profile: kcs and its matching wiki schema"
        )
    state_dir = relative_file(kb, f".openkb/kcs-foundry/{run_id}")
    state_dir.mkdir(parents=True, exist_ok=False)
    write_json(state_dir / "manifest.json", manifest)
    write_json(state_dir / "plan.json", plan)
    state = {"phase": "preparing", "mode": "native", "documents": [], "validation": None}
    write_json(state_dir / "state.json", state)
    try:
        inputs = relative_file(kb, f"raw/kcs-inputs/{run_id}")
        inputs.mkdir(parents=True, exist_ok=False)
        for source in manifest["sources"]:
            for key in ("snapshot", "document"):
                destination = relative_file(inputs, source[key])
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(relative_file(package, source[key]), destination)
        write_json(inputs / "manifest.json", manifest)
        if load_package(inputs) != manifest:
            raise FoundryError("Material package changed before import")
        output = relative_file(kb, plan["output"])
        output.mkdir(parents=True, exist_ok=False)
        state["phase"] = "compiling"
        previous_cards = tree_hashes(kb / "wiki" / "concepts")
        write_json(state_dir / "state.json", state)
        for source in manifest["sources"]:
            result = backend.ingest(relative_file(inputs, source["document"]), kb)
            state["documents"].append({"source_id": source["id"], "result": result})
            write_json(state_dir / "state.json", state)
            if result not in {"added", "skipped"}:
                raise FoundryError(
                    f"OpenKB failed to import {source['id']}; compilation stopped"
                )
            from native_kcs import record_batch

            record_batch(kb, run_id, manifest, [d["source_id"] for d in state["documents"]])
        state["phase"] = "validating"
        write_json(state_dir / "state.json", state)
        if load_package(inputs) != manifest:
            raise FoundryError("Input manifest changed during extraction")
        if load_package(package) != manifest:
            raise FoundryError("Trusted material package changed during extraction")
        from native_kcs import validate_native

        validation = validate_native(kb)
        after_cards = tree_hashes(kb / "wiki" / "concepts")
        state["changed_cards"] = [
            f"concepts/{p}" for (p, h) in after_cards.items() if previous_cards.get(p) != h
        ]
        state["removed_cards"] = [f"concepts/{p}" for p in previous_cards if p not in after_cards]
        lines = [
            "# Native KCS compilation",
            "",
            f"Scenario label: {scenario}",
            "",
            "Canonical knowledge: wiki/concepts (not standalone exported cards).",
            "",
            "Changed nodes:",
            *[f"- {p}" for p in state["changed_cards"]],
            "",
            "Runtime validation: not_run. Semantic source review remains required.",
        ]
        (output / "extraction-report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
        write_json(relative_file(output, "validation.json"), validation)
        state["validation"] = validation
        state["phase"] = "completed" if validation["valid"] else "validation_failed"
        write_json(state_dir / "state.json", state)
        return state
    except Exception as exc:
        state["phase"] = "failed"
        state["error_type"] = type(exc).__name__
        write_json(state_dir / "state.json", state)
        raise


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--materials", type=Path, required=True)
    parser.add_argument("--kb", type=Path, required=True)
    parser.add_argument("--scenario", required=True)
    parser.add_argument(
        "--run-id",
        default=dt.datetime.now(dt.timezone.utc).strftime("%Y%m%d-%H%M%S-") + uuid.uuid4().hex[:8],
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate/print plan without writes, imports or model calls",
    )
    args = parser.parse_args()
    try:
        (package, kb) = (args.materials.expanduser().resolve(), args.kb.expanduser().resolve())
        if args.dry_run:
            (_, plan) = plan_run(package, kb, args.run_id, args.scenario)
            print(json.dumps(plan, ensure_ascii=False, indent=2))
            return 0
        state = run_pipeline(package, kb, args.run_id, args.scenario)
    except FoundryError as exc:
        print(f"Foundry stopped: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:
        print(
            f"Foundry failed ({type(exc).__name__}); inspect private run state. No automatic retry.",
            file=sys.stderr,
        )
        return 1
    print(f"Run phase: {state['phase']}; mode: native; report: {kb / 'output/kcs' / args.run_id}")
    return 0 if state["phase"] == "completed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
