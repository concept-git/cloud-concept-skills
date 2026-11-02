"""Native profile CLI and model-protocol boundaries, without network calls."""
import json
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import pytest
import yaml
from click.testing import CliRunner

from openkb.cli import cli, initialize_kb, _refresh_schema, _add_single_file_locked
from openkb.schema import agents_md_for_profile, AGENTS_MD
from openkb.agent import compiler


def test_kcs_init_audit_and_refresh(tmp_path):
    runner = CliRunner()
    with runner.isolated_filesystem(temp_dir=tmp_path), patch("openkb.cli.register_kb"):
        result = runner.invoke(cli, ["init", "--knowledge-profile", "kcs", "--model", "test", "--language", "zh"], input="\n")
        assert result.exit_code == 0, result.output
        kb = Path.cwd()
        assert yaml.safe_load((kb / ".openkb/config.yaml").read_text())["knowledge_profile"] == "kcs"
        schema = kb / "wiki/AGENTS.md"
        assert schema.read_text() == agents_md_for_profile("kcs")
        before = {p: p.read_bytes() for p in kb.rglob("*") if p.is_file()}
        with patch.object(compiler.litellm, "completion", side_effect=AssertionError("No model expected")):
            result = runner.invoke(cli, ["--kb-dir", str(kb), "kcs-audit"])
        assert result.exit_code == 0, result.output
        assert json.loads(result.output)["valid"]
        assert all(p.read_bytes() == value for p, value in before.items())
        schema.write_text(AGENTS_MD)
        assert _refresh_schema(kb / "wiki")
        assert schema.read_text() == agents_md_for_profile("kcs")
        assert (kb / "wiki/AGENTS.md.bak").read_text() == AGENTS_MD


def test_python_initializer_and_missing_local_model(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    with patch("openkb.cli.register_kb"):
        kb = tmp_path / "kb"
        initialize_kb(kb, model="test", knowledge_profile="kcs")
    assert (kb / "wiki/AGENTS.md").read_text() == agents_md_for_profile("kcs")
    (kb / ".openkb/config.yaml").write_text("knowledge_profile: kcs\nmodel: null\n")
    source = tmp_path / "ticket.md"
    source.write_text("ticket")
    with patch("openkb.cli._setup_llm_key", side_effect=AssertionError("Must stop before setup")):
        assert _add_single_file_locked(source, kb) == "failed"
    with pytest.raises(ValueError):
        initialize_kb(tmp_path / "invalid", knowledge_profile="invalid")
    assert not (tmp_path / "invalid").exists()


def test_compiler_completion_does_not_send_tools():
    response = SimpleNamespace(
        choices=[SimpleNamespace(message=SimpleNamespace(content='{"ok":true}'), finish_reason="stop")],
        usage=SimpleNamespace(prompt_tokens=1, completion_tokens=1),
    )
    with patch.object(compiler.litellm, "completion", return_value=response) as call:
        result = compiler._llm_call("openai/internal", [{"role": "user", "content": "JSON"}],
                                    "protocol-check", response_format={"type": "json_object"})
    assert json.loads(result)["ok"]
    assert "tools" not in call.call_args.kwargs
    assert "tool_choice" not in call.call_args.kwargs
    assert call.call_args.kwargs["response_format"] == {"type": "json_object"}
