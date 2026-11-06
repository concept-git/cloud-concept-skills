"""Offline integration tests: no OpenKB dependencies, model or cloud account required."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from extract_kcs import plan_run, run_pipeline
from foundry_common import FoundryError, load_package, write_json
from prepare_materials import prepare
from validate_kcs import validate


def generate(output: Path, manifest: dict):
    (output / "articles").mkdir(exist_ok=True)
    (output / "evidence").mkdir(exist_ok=True)
    (output / "articles/case.md").write_text(
        "---\nstatus: draft\n---\n# 连接失败如何检查\n\n## Issue\n连接失败。\n\n"
        "## Environment\n来源平台。\n\n## Resolution\n1. 核对错误和通道条件。\n\n"
        "## Cause\n尚未确定。\n", encoding="utf-8")
    source = manifest["sources"][0]
    data = {
        "schema_version": "1", "article": "articles/case.md", "input_kind": manifest["input_kind"],
        "target_platform": "source-platform", "completeness": "partial",
        "sources": [{"id": "S1", "kind": manifest["input_kind"],
                     "repository_or_alias": manifest["source_name"], "revision": manifest["revision"],
                     "path": source["path"], "sha256": source["sha256"], "locators_read": ["L1-L2"]}],
        "claims": [{"id": "R1", "article_locator": "Resolution step 1", "statement": "核对通道条件。",
                    "basis": "source_guidance", "refs": [{"source_id": "S1", "locator": "L1-L2"}]}],
        "gaps": [{"area": "verification", "detail": "无事件观测。", "affected_claims": ["R1"]}],
        "checks": {k: {"status": "not_run", "detail": "offline fixture"}
                   for k in ("structure", "source_review", "runtime_validation")},
    }
    write_json(output / "evidence/case.json", data)
    (output / "extraction-report.md").write_text("# 草稿报告\n未执行诊断。\n", encoding="utf-8")


class FakeBackend:
    def __init__(self, manifest, mode="valid"):
        self.manifest, self.mode, self.imports, self.extract_calls = manifest, mode, [], 0

    def configure(self, kb):
        self.kb = kb

    def ingest(self, path, kb):
        self.imports.append(path)
        return "failed" if self.mode == "import-failed" else "added"

    def extract(self, kb, intent, max_turns):
        self.extract_calls += 1
        output = kb / "output/kcs/run-one"
        if self.mode == "empty":
            return
        generate(output, self.manifest)
        if self.mode == "invented-hash":
            path = output / "evidence/case.json"
            data = json.loads(path.read_text())
            data["sources"][0]["sha256"] = "0" * 64
            write_json(path, data)
        if self.mode == "tampered-input":
            source = self.manifest["sources"][0]["snapshot"]
            (kb / "output/kcs-inputs/run-one" / source).write_text("changed", encoding="utf-8")


class PipelineTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.source = self.root / "approved"
        self.source.mkdir()
        (self.source / "SKILL.md").write_text("# Entry\nRead references/check.md.\n", encoding="utf-8")
        (self.source / "references").mkdir()
        (self.source / "references/check.md").write_text("# Check\nIf channel missing, report unknown.\n", encoding="utf-8")
        (self.source / ".env").write_text("LLM_API_KEY=must-not-copy\n", encoding="utf-8")
        self.package = self.root / "package"
        self.manifest = prepare(self.source, self.package, "skill", "test/sample", "rev-one", [])
        self.kb = self.root / "kb"
        (self.kb / ".openkb").mkdir(parents=True)
        (self.kb / ".openkb/config.yaml").write_text("model: configured-internal-model\n", encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def run_fixture(self, mode="valid"):
        backend = FakeBackend(self.manifest, mode)
        state = run_pipeline(self.package, self.kb, "run-one", "连接失败", backend=backend, mode="export")
        return backend, state

    def test_snapshot_preserves_source_and_excludes_hidden_credentials(self):
        self.assertEqual(load_package(self.package), self.manifest)
        self.assertEqual(len(self.manifest["sources"]), 2)
        self.assertFalse((self.package / "sources/.env").exists())
        for entry in self.manifest["sources"]:
            self.assertEqual((self.source / entry["path"]).read_bytes(),
                             (self.package / entry["snapshot"]).read_bytes())
            self.assertIn("L1:", (self.package / entry["document"]).read_text())

    def test_same_basename_gets_distinct_document_and_fences_remain_data(self):
        (self.source / "other").mkdir()
        (self.source / "other/check.md").write_text("````\n# embedded\n````\n", encoding="utf-8")
        manifest = prepare(self.source, self.root / "second", "skill", "sample", None, [])
        self.assertEqual(len({s["document"] for s in manifest["sources"]}), 3)
        entry = next(s for s in manifest["sources"] if s["path"] == "other/check.md")
        self.assertIn("`````text", (self.root / "second" / entry["document"]).read_text())

    def test_nested_output_and_overwrite_are_refused(self):
        with self.assertRaises(FoundryError):
            prepare(self.source, self.source / "package", "skill", "test", None, [])
        with self.assertRaises(FoundryError):
            prepare(self.source, self.package, "skill", "test", None, [])

    def test_symlink_material_is_not_followed(self):
        (self.source / "alias.md").symlink_to(self.source / "SKILL.md")
        with self.assertRaises(FoundryError):
            prepare(self.source, self.root / "second", "skill", "test", None, [])

    def test_unsupported_attachment_is_reported(self):
        (self.source / "attachment.pdf").write_bytes(b"PDF fixture")
        result = prepare(self.source, self.root / "second", "ticket", "ticket-alias", None, [])
        self.assertTrue(any(e["path"] == "attachment.pdf" and "unsupported" in e["reason"]
                            for e in result["skipped"]))

    def test_binary_and_size_limits_fail_before_publication(self):
        (self.source / "binary.txt").write_bytes(b"a\x00b")
        with self.assertRaises(FoundryError):
            prepare(self.source, self.root / "second", "skill", "test", None, [])
        self.assertFalse((self.root / "second").exists())
        with self.assertRaises(FoundryError):
            prepare(self.source, self.root / "second", "skill", "test", None, [], max_bytes=1)

    def test_changed_source_and_manifest_traversal_are_rejected(self):
        original = self.package / self.manifest["sources"][0]["snapshot"]
        original.write_text("tampered", encoding="utf-8")
        with self.assertRaises(FoundryError):
            load_package(self.package)
        data = json.loads((self.package / "manifest.json").read_text())
        data["sources"][0]["snapshot"] = "../escape.txt"
        write_json(self.package / "manifest.json", data)
        with self.assertRaises(FoundryError):
            load_package(self.package)

    def test_dry_run_has_no_writes_or_model_import(self):
        kb = self.root / "not-created"
        result = subprocess.run([sys.executable, str(SCRIPTS / "extract_kcs.py"),
                                 "--materials", str(self.package), "--kb", str(kb),
                                 "--run-id", "dry-one", "--scenario", "连接失败", "--dry-run"],
                                text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["source_count"], 2)
        self.assertFalse(kb.exists())
        self.assertNotIn("must-not-copy", result.stdout)

    def test_pipeline_ingests_then_generates_and_validates(self):
        # Unlisted files in a package must not enter the model-readable snapshot.
        (self.package / "unlisted.txt").write_text("not in manifest", encoding="utf-8")
        backend, state = self.run_fixture()
        self.assertEqual(len(backend.imports), 2)
        self.assertEqual(backend.extract_calls, 1)
        self.assertEqual(state["phase"], "completed")
        self.assertTrue(state["validation"]["valid"])
        self.assertEqual(state["validation"]["runtime_validation"], "not_run")
        self.assertFalse((self.kb / "output/kcs-inputs/run-one/unlisted.txt").exists())
        self.assertTrue((self.kb / ".openkb/kcs-foundry/run-one/state.json").is_file())
        self.assertTrue((self.kb / "skills/kcs-extractor/references/output-contract.md").is_file())

    def test_import_failure_prevents_generation_and_no_retry(self):
        backend = FakeBackend(self.manifest, "import-failed")
        with self.assertRaises(FoundryError):
            run_pipeline(self.package, self.kb, "run-one", "连接失败", backend=backend, mode="export")
        self.assertEqual(backend.extract_calls, 0)
        self.assertEqual(len(backend.imports), 1)
        state = json.loads((self.kb / ".openkb/kcs-foundry/run-one/state.json").read_text())
        self.assertEqual(state["phase"], "failed")
        with self.assertRaises(FoundryError):
            run_pipeline(self.package, self.kb, "run-one", "连接失败", backend=backend, mode="export")
        self.assertEqual(len(backend.imports), 1)

    def test_empty_generator_success_is_not_pipeline_success(self):
        _, state = self.run_fixture("empty")
        self.assertEqual(state["phase"], "validation_failed")
        self.assertIn("no KCS articles generated", state["validation"]["errors"])

    def test_model_invented_hash_is_rejected(self):
        _, state = self.run_fixture("invented-hash")
        self.assertEqual(state["phase"], "validation_failed")
        self.assertTrue(any("trusted manifest" in e for e in state["validation"]["errors"]))

    def test_model_tampered_input_is_detected(self):
        with self.assertRaises(FoundryError):
            self.run_fixture("tampered-input")
        state = json.loads((self.kb / ".openkb/kcs-foundry/run-one/state.json").read_text())
        self.assertEqual(state["phase"], "failed")
        self.assertEqual(load_package(self.package), self.manifest)

    def test_existing_run_or_different_installed_skill_is_not_overwritten(self):
        self.run_fixture()
        with self.assertRaises(FoundryError):
            plan_run(self.package, self.kb, "run-one", "连接失败", None)
        (self.kb / "skills/kcs-extractor/SKILL.md").write_text("local modification", encoding="utf-8")
        with self.assertRaises(FoundryError):
            run_pipeline(self.package, self.kb, "run-two", "连接失败", backend=FakeBackend(self.manifest), mode="export")

    def test_validator_rejects_false_runtime_claim_and_broken_link(self):
        output = self.root / "drafts"
        output.mkdir()
        generate(output, self.manifest)
        path = output / "evidence/case.json"
        data = json.loads(path.read_text())
        data["checks"]["runtime_validation"]["status"] = "passed"
        write_json(path, data)
        article = output / "articles/case.md"
        article.write_text(article.read_text() + "\n[missing](missing.md)\n", encoding="utf-8")
        result = validate(output, self.manifest)
        self.assertFalse(result["valid"])
        self.assertTrue(any("runtime validation" in e for e in result["errors"]))
        self.assertTrue(any("file link" in e for e in result["errors"]))

    def test_invalid_json_symlink_and_orphan_evidence_fail_closed(self):
        output = self.root / "drafts"
        output.mkdir()
        generate(output, self.manifest)
        path = output / "evidence/case.json"
        path.write_text("not-json", encoding="utf-8")
        self.assertFalse(validate(output, self.manifest)["valid"])
        path.unlink()
        path.symlink_to(self.package / "manifest.json")
        self.assertFalse(validate(output, self.manifest)["valid"])
        path.unlink()
        generate(output, self.manifest)
        write_json(output / "evidence/orphan.json", {})
        (output / "repair.sh").write_text("must not be a generated KCS artifact", encoding="utf-8")
        result = validate(output, self.manifest)
        self.assertTrue(any("orphan evidence" in e for e in result["errors"]))
        self.assertTrue(any("unexpected artifact" in e for e in result["errors"]))

    def test_missing_kb_and_bad_run_id_stop_before_backend(self):
        backend = FakeBackend(self.manifest)
        (self.kb / ".openkb/config.yaml").unlink()
        with self.assertRaises(FoundryError):
            run_pipeline(self.package, self.kb, "run-one", "连接失败", backend=backend, mode="export")
        self.assertFalse(hasattr(backend, "kb"))
        with self.assertRaises(FoundryError):
            plan_run(self.package, self.kb, "../escape", "连接失败", None)

    def test_all_cli_help_works_without_openkb(self):
        for name in ("prepare_materials.py", "extract_kcs.py", "validate_kcs.py"):
            result = subprocess.run([sys.executable, str(SCRIPTS / name), "--help"], capture_output=True)
            self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
