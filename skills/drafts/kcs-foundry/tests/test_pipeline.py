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
from foundry_common import FoundryError, load_package, write_json
from prepare_materials import prepare


class PipelineTests(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.source = self.root / "approved"
        self.source.mkdir()
        (self.source / "SKILL.md").write_text(
            "# Entry\nRead references/check.md.\n", encoding="utf-8"
        )
        (self.source / "references").mkdir()
        (self.source / "references/check.md").write_text(
            "# Check\nIf channel missing, report unknown.\n", encoding="utf-8"
        )
        (self.source / ".env").write_text("LLM_API_KEY=must-not-copy\n", encoding="utf-8")
        self.package = self.root / "package"
        self.manifest = prepare(self.source, self.package, "skill", "test/sample", "rev-one", [])
        self.kb = self.root / "kb"
        (self.kb / ".openkb").mkdir(parents=True)
        (self.kb / ".openkb/config.yaml").write_text(
            "model: configured-internal-model\n", encoding="utf-8"
        )

    def tearDown(self):
        self.tmp.cleanup()

    def test_snapshot_preserves_source_and_excludes_hidden_credentials(self):
        self.assertEqual(load_package(self.package), self.manifest)
        self.assertEqual(len(self.manifest["sources"]), 2)
        self.assertFalse((self.package / "sources/.env").exists())
        for entry in self.manifest["sources"]:
            self.assertEqual(
                (self.source / entry["path"]).read_bytes(),
                (self.package / entry["snapshot"]).read_bytes(),
            )
            self.assertIn("L1:", (self.package / entry["document"]).read_text())

    def test_same_basename_gets_distinct_document_and_fences_remain_data(self):
        (self.source / "other").mkdir()
        (self.source / "other/check.md").write_text("````\n# embedded\n````\n", encoding="utf-8")
        manifest = prepare(self.source, self.root / "second", "skill", "sample", None, [])
        self.assertEqual(len({s["document"] for s in manifest["sources"]}), 3)
        entry = next((s for s in manifest["sources"] if s["path"] == "other/check.md"))
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
        self.assertTrue(
            any(
                (
                    e["path"] == "attachment.pdf" and "unsupported" in e["reason"]
                    for e in result["skipped"]
                )
            )
        )

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
        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPTS / "extract_kcs.py"),
                "--materials",
                str(self.package),
                "--kb",
                str(kb),
                "--run-id",
                "dry-one",
                "--scenario",
                "连接失败",
                "--dry-run",
            ],
            text=True,
            capture_output=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["source_count"], 2)
        self.assertFalse(kb.exists())
        self.assertNotIn("must-not-copy", result.stdout)

    def test_missing_kb_stops_before_backend_and_does_not_initialize(self):
        from extract_kcs import run_pipeline
        kb = self.root / "missing-kb"
        with self.assertRaisesRegex(FoundryError, "Knowledge base not initialized"):
            run_pipeline(self.package, kb, "missing", "SSH", backend=object())
        self.assertFalse(kb.exists())

    def test_removed_export_flags_fail_before_any_writes(self):
        for flag, value in (
            ("--mode", "export"),
            ("--max-turns", "80"),
            ("--target-platform", "another-cloud"),
        ):
            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS / "extract_kcs.py"),
                    "--materials",
                    str(self.package),
                    "--kb",
                    str(self.kb),
                    "--scenario",
                    "SSH",
                    flag,
                    value,
                ],
                capture_output=True,
            )
            self.assertEqual(result.returncode, 2)
            self.assertFalse((self.kb / ".openkb/kcs-foundry").exists())

    def test_all_cli_help_works_without_openkb(self):
        for name in ("prepare_materials.py", "extract_kcs.py", "validate_kcs.py"):
            result = subprocess.run(
                [sys.executable, str(SCRIPTS / name), "--help"], capture_output=True
            )
            self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
