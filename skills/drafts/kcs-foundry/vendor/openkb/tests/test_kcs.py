"""KCS profile tests use real compiler/file operations with deterministic model responses."""

from __future__ import annotations

import json
from unittest.mock import AsyncMock, patch

import pytest

from openkb import frontmatter, kcs
from openkb.agent import compiler
from openkb.locks import atomic_write_text
from openkb.schema import AGENTS_MD, INDEX_SEED, agents_md_for_profile, get_agents_md


def body(title="SSH timeout", extra="", links=""):
    return (f"# {title}\n\n## Issue\nSSH times out.\n\n## Environment\nLinux; {extra}\n\n"
            f"## Resolution\n1. Check the connection evidence. {links}\n\n"
            "## Cause\nNot determined; no event-level confirmation.\n")


def payload(doc, kind="case", content=None, previous=None):
    sources = [f"summaries/{doc}.md", *(previous or [])]
    return {"description": "SSH diagnosis", "content": content or body(),
            "knowledge_kind": kind, "cause_status": "unknown",
            "evidence": [{"section": section, "source": source, "locator": "L1-L2",
                          "claim": f"{section} facts from {source}",
                          "basis": "extraction_inference" if section == "Cause" else "source_guidance"}
                         for source in sources for section in kcs.FIELDS]}


@pytest.fixture
def wiki(tmp_path):
    (tmp_path / ".openkb").mkdir()
    atomic_write_text(tmp_path / ".openkb/config.yaml", "knowledge_profile: kcs\n")
    root = tmp_path / "wiki"
    for name in ("sources", "summaries", "concepts", "entities"):
        (root / name).mkdir(parents=True)
    atomic_write_text(root / "index.md", INDEX_SEED)
    atomic_write_text(root / "AGENTS.md", agents_md_for_profile("kcs"))
    return root


async def compile_fixture(wiki, doc, plan, pages):
    source = wiki / "sources" / f"{doc}.md"
    atomic_write_text(source, f"L1: {doc} evidence\nL2: observation without confirmed cause\n")

    def sync_response(model, messages, stage, **kwargs):
        if stage == "summary":
            return json.dumps({"description": doc, "content": f"# {doc}\nSource observations."})
        if stage == "concepts-plan":
            return json.dumps({"concepts": plan, "entities": {}})
        if stage == "summary-rewrite":
            return f"# {doc}\nSource observations."
        raise AssertionError(stage)

    async def page_response(model, messages, stage, **kwargs):
        name = stage.split(": ", 1)[1]
        return json.dumps(pages[name])

    with patch.object(compiler, "_llm_call", side_effect=sync_response), \
         patch.object(compiler, "_llm_call_page_async", side_effect=page_response), \
         patch.object(compiler, "_close_async_llm_clients", new=AsyncMock()):
        await compiler.compile_short_doc(doc, source, wiki.parent, "test-model")


def test_generic_schema_unchanged_and_profile_is_explicit(tmp_path):
    assert agents_md_for_profile("generic") == AGENTS_MD
    assert get_agents_md(tmp_path / "wiki") == AGENTS_MD
    assert kcs.MARKER in agents_md_for_profile("kcs")
    for bad in ("typo", None, ["kcs"]):
        with pytest.raises(ValueError):
            kcs.resolve_profile({"knowledge_profile": bad})


def test_existing_schema_must_be_explicitly_migrated(wiki):
    atomic_write_text(wiki / "AGENTS.md", AGENTS_MD)
    with pytest.raises(ValueError, match="mismatch"):
        get_agents_md(wiki)
    atomic_write_text(wiki / "AGENTS.md", agents_md_for_profile("kcs"))
    assert kcs.MARKER in get_agents_md(wiki)


@pytest.mark.asyncio
async def test_two_batches_update_one_card_and_keep_graph(wiki):
    await compile_fixture(wiki, "ticket-a", {"create": [
        {"name": "ssh-timeout", "knowledge_kind": "case"},
        {"name": "network-path", "knowledge_kind": "pattern"}]}, {
        "ssh-timeout": payload("ticket-a", content=body(links="[[concepts/network-path]]")),
        "network-path": payload("ticket-a", kind="pattern", content=body("Network path", links="[[concepts/ssh-timeout]]"))})
    first = wiki / "concepts/ssh-timeout.md"
    old = frontmatter.parse(first.read_text())
    assert old["status"] == "draft"
    assert kcs.audit_wiki(wiki)["valid"]
    # A manual validation is meaningful only while bound to this fingerprint.
    fm, text = frontmatter.split(first.read_text())
    fm = frontmatter.set_line(fm, "status", "validated")
    fm = frontmatter.set_line(fm, "validation_hash", old["content_hash"])
    atomic_write_text(first, fm + text)
    # Even a mistaken create for an existing slug must update it, not overwrite its sources.
    await compile_fixture(wiki, "ticket-b", {"create": [
        {"name": "ssh-timeout", "knowledge_kind": "case"}]}, {
        "ssh-timeout": payload("ticket-b", content=body(extra="version-specific branch",
                              links="[[concepts/network-path]]"), previous=["summaries/ticket-a.md"])})
    data = frontmatter.parse(first.read_text())
    assert set(data["sources"]) == {"summaries/ticket-a.md", "summaries/ticket-b.md"}
    assert data["status"] == "draft" and "validation_hash" not in data
    assert data["content_hash"] != old["content_hash"]
    assert len(list((wiki / "concepts").glob("*.md"))) == 2
    assert "[[concepts/ssh-timeout]]" in (wiki / "summaries/ticket-b.md").read_text()
    assert list(kcs.sections(first.read_text())) == list(kcs.FIELDS)
    assert kcs.audit_wiki(wiki)["valid"]


def test_unchanged_content_preserves_bound_validation(wiki):
    atomic_write_text(wiki / "sources/a.md", "original")
    compiler._write_summary(wiki, "a", "# A")
    page = kcs.render_page(wiki, body(), payload("a"), ["summaries/a.md"], "description")
    data = frontmatter.parse(page)
    fm, text = frontmatter.split(page)
    fm = frontmatter.set_line(frontmatter.set_line(fm, "status", "validated"), "validation_hash", data["content_hash"])
    same = kcs.render_page(wiki, body(), payload("a"), ["summaries/a.md"], "description", fm + text)
    assert frontmatter.parse(same)["status"] == "validated"
    atomic_write_text(wiki / "sources/a.md", "changed source, same filename")
    changed = kcs.render_page(wiki, body(), payload("a"), ["summaries/a.md"], "description", same)
    assert frontmatter.parse(changed)["status"] == "draft"


@pytest.mark.asyncio
async def test_bad_generation_or_dangling_links_fail_without_new_cards(wiki):
    for content in ("# Unstructured text", body(links="[[concepts/invented]]")):
        with pytest.raises(ValueError, match="generation failed"):
            await compile_fixture(wiki, "a", {"create": [{"name": "new-card", "knowledge_kind": "case"}]},
                                  {"new-card": payload("a", content=content)})
        assert not list((wiki / "concepts").glob("*.md"))


def test_cause_and_sources_require_evidence():
    data = payload("a")
    data["cause_status"] = "source_supported"
    with pytest.raises(ValueError, match="confirmed"):
        kcs.validate_payload(body(), data, {"summaries/a.md"})
    data["cause_status"] = "unknown"
    data["evidence"][0]["source"] = "summaries/invented.md"
    with pytest.raises(ValueError, match="source"):
        kcs.validate_payload(body(), data, {"summaries/a.md"})


@pytest.mark.asyncio
async def test_compiler_binds_aliases_and_retains_previous_sources(wiki):
    first = payload("a")
    for item in first["evidence"]:
        item.pop("source")  # A single document has an unambiguous binding.
    await compile_fixture(wiki, "a", {"create": [{"name": "case", "knowledge_kind": "case"}]},
                          {"case": first})
    second = payload("b", previous=["summaries/a.md"])
    for item in second["evidence"]:
        item["source_ref"] = "S0" if item.pop("source") == "summaries/b.md" else "S1"
    await compile_fixture(wiki, "b", {"update": [{"name": "case", "knowledge_kind": "case"}]},
                          {"case": second})
    data = frontmatter.parse((wiki / "concepts/case.md").read_text())
    assert {e["source"] for e in data["evidence"]} == {"summaries/a.md", "summaries/b.md"}
    assert all("source_ref" not in e for e in data["evidence"])
    assert kcs.audit_wiki(wiki)["valid"]


@pytest.mark.parametrize("item", [
    {}, {"source_ref": "S9"}, {"source": "invented.md"},
    {"source_ref": "S0", "source": "summaries/a.md"},
])
def test_ambiguous_or_wrong_bindings_are_rejected(item):
    mapping = kcs.evidence_source_map("summaries/b.md", {"summaries/a.md", "summaries/b.md"})
    with pytest.raises(ValueError):
        kcs.bind_evidence_sources({"evidence": [item]}, mapping)


def test_removing_a_source_invalidates_previous_validation(wiki):
    for name in ("a", "b"):
        atomic_write_text(wiki / "sources" / f"{name}.md", name)
    data = payload("a", previous=["summaries/b.md"])
    text = kcs.render_page(wiki, body(), data, ["summaries/a.md", "summaries/b.md"], "case")
    metadata = frontmatter.parse(text)
    header, content = frontmatter.split(text)
    header = frontmatter.set_line(frontmatter.set_line(header, "status", "validated"),
                                  "validation_hash", metadata["content_hash"])
    changed, empty = compiler._remove_source_from_frontmatter(header + content, "summaries/a.md")
    assert not empty
    assert frontmatter.parse(changed)["status"] == "draft"
    assert "validation_hash" not in frontmatter.parse(changed)


@pytest.mark.asyncio
async def test_source_edits_and_broken_graph_are_audited(wiki):
    await compile_fixture(wiki, "a", {"create": [{"name": "case", "knowledge_kind": "case"}]},
                          {"case": payload("a")})
    atomic_write_text(wiki / "sources/a.md", "changed")
    assert not kcs.audit_wiki(wiki)["valid"]
    atomic_write_text(wiki / "entities/bad.md", "# Entity\n[[concepts/missing]]")
    result = kcs.audit_wiki(wiki)
    assert any("unresolved" in e for e in result["errors"])
