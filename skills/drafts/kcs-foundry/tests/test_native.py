"""Native Foundry tests, skipped only when YAML/locking test dependencies are absent."""

from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
AVAILABLE = all(importlib.util.find_spec(name) is not None for name in ("yaml", "portalocker"))


@unittest.skipUnless(AVAILABLE, "Native tests require PyYAML and portalocker")
class NativePipelineTests(unittest.TestCase):
    def setUp(self):
        from native_kcs import openkb_modules

        self.kcs, _ = openkb_modules()
        from openkb import frontmatter
        from openkb.schema import agents_md_for_profile, INDEX_SEED

        self.fm = frontmatter
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.kb = self.root / "kb"
        for folder in (".openkb", "wiki/sources", "wiki/summaries", "wiki/concepts", "wiki/entities"):
            (self.kb / folder).mkdir(parents=True, exist_ok=True)
        (self.kb / ".openkb/config.yaml").write_text("knowledge_profile: kcs\nmodel: test\n", encoding="utf-8")
        (self.kb / ".openkb/hashes.json").write_text("{}", encoding="utf-8")
        (self.kb / "wiki/index.md").write_text(INDEX_SEED, encoding="utf-8")
        (self.kb / "wiki/AGENTS.md").write_text(agents_md_for_profile("kcs"), encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def package(self, name):
        from prepare_materials import prepare

        source = self.root / name
        source.mkdir()
        (source / f"{name}.md").write_text(f"# {name}\nAn observed SSH failure, cause unknown.\n", encoding="utf-8")
        package = self.root / f"package-{name}"
        manifest = prepare(source, package, "ticket", "approved-tickets", name, [])
        return package, manifest

    def backend(self, manifest, fail=False):
        outer = self

        class Backend:
            profile = "kcs"
            extract_calls = 0

            def configure(self, kb):
                pass

            def ingest(self, path, kb):
                from foundry_common import write_json

                if fail:
                    return "failed"
                entry = manifest["sources"][0]
                name = Path(entry["document"]).stem
                summary = f"summaries/{name}.md"
                (kb / "wiki/sources" / f"{name}.md").write_bytes(path.read_bytes())
                (kb / "wiki" / summary).write_text(
                    outer.fm.block([outer.fm.kv_line("type", "Summary"),
                                    outer.fm.kv_line("full_text", f"sources/{name}.md")])
                    + "# Summary\n[[concepts/ssh-case]]\n", encoding="utf-8")
                card = kb / "wiki/concepts/ssh-case.md"
                old = card.read_text() if card.exists() else ""
                sources = [summary, *outer.fm.parse(old).get("sources", [])]
                evidence = [{"section": field, "source": s, "locator": "L1-L2", "claim": field,
                             "basis": "extraction_inference" if field == "Cause" else "recorded_observation"}
                            for s in sources for field in outer.kcs.FIELDS]
                body = "# SSH failure\n\n## Issue\nSSH fails.\n\n## Environment\nLinux.\n\n## Resolution\n1. Check evidence.\n\n## Cause\nNot determined.\n"
                payload = {"knowledge_kind": "case", "cause_status": "unknown", "evidence": evidence}
                card.write_text(outer.kcs.render_page(kb / "wiki", body, payload, sources, "SSH case", old), encoding="utf-8")
                summaries = sorted((kb / "wiki/summaries").glob("*.md"))
                (kb / "wiki/index.md").write_text("# Index\n[[concepts/ssh-case]]\n" + "\n".join(
                    f"[[summaries/{p.stem}]]" for p in summaries), encoding="utf-8")
                registry = json.loads((kb / ".openkb/hashes.json").read_text())
                registry[entry["document_sha256"]] = {"doc_name": name}
                write_json(kb / ".openkb/hashes.json", registry)
                return "added"

            def extract(self, *args):
                self.extract_calls += 1
                raise AssertionError("Native compilation must not invoke a second generator")

        return Backend()

    def test_cross_batch_provenance_and_no_second_generator(self):
        from extract_kcs import run_pipeline
        from native_kcs import validate_native

        for name in ("ticket-a", "ticket-b"):
            package, manifest = self.package(name)
            backend = self.backend(manifest)
            state = run_pipeline(package, self.kb, name, "SSH", backend=backend)
            self.assertEqual(state["phase"], "completed")
            self.assertEqual(backend.extract_calls, 0)
            self.assertEqual(state["changed_cards"], ["concepts/ssh-case.md"])
        data = self.fm.parse((self.kb / "wiki/concepts/ssh-case.md").read_text())
        self.assertEqual(len(data["sources"]), 2)
        self.assertTrue(validate_native(self.kb)["valid"])
        self.assertEqual(len(list((self.kb / "provenance/batches").glob("*.json"))), 2)
        self.assertFalse((self.kb / "output/kcs/ticket-b/articles").exists())

    def test_changed_original_snapshot_fails_native_audit(self):
        from extract_kcs import run_pipeline
        from native_kcs import validate_native

        package, manifest = self.package("ticket-a")
        run_pipeline(package, self.kb, "first", "SSH", backend=self.backend(manifest))
        snapshot = self.kb / "raw/kcs-inputs/first" / manifest["sources"][0]["snapshot"]
        snapshot.write_text("tampered", encoding="utf-8")
        self.assertFalse(validate_native(self.kb)["valid"])

    def test_failed_import_does_not_claim_native_success(self):
        from extract_kcs import run_pipeline
        from foundry_common import FoundryError

        package, manifest = self.package("ticket-a")
        with self.assertRaises(FoundryError):
            run_pipeline(package, self.kb, "failed", "SSH", backend=self.backend(manifest, fail=True))
        self.assertFalse((self.kb / "provenance/batches/failed.json").exists())

    def test_native_platform_rewrite_is_not_implicit(self):
        from extract_kcs import plan_run
        from foundry_common import FoundryError

        package, _ = self.package("ticket-a")
        with self.assertRaises(FoundryError):
            plan_run(package, self.kb, "test", "SSH", "another-cloud")


if __name__ == "__main__":
    unittest.main()
