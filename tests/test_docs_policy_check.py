import subprocess

import pytest

from scripts import docs_policy_check


def test_extract_table_statuses_reads_allowed_annotations():
    readme = """
## Source-to-scope status table

| Source | Source-to-scope interpretation in this repo | Status |
|---|---|---|
| ABL, [1703](https://arxiv.org/abs/1703.04541) | text | implemented |
| PRL, [paper](https://example.org/prl) | text | partial |
| Other, [paper](https://example.org/other/) | text | out-of-scope |
"""
    statuses = docs_policy_check.extract_table_statuses(readme)

    assert statuses["https://arxiv.org/abs/1703.04541"] == "implemented"
    assert statuses["https://example.org/prl"] == "partial"
    assert statuses["https://example.org/other"] == "out-of-scope"


def test_changed_in_section_reports_overlap():
    section = docs_policy_check.Section(title="x", start=10, end=20)
    assert docs_policy_check.changed_in_section({8, 9, 10}, section)
    assert not docs_policy_check.changed_in_section({1, 2, 3}, section)


def test_run_git_reports_missing_git(monkeypatch, capsys):
    def fake_check_output(*_args, **_kwargs):
        raise FileNotFoundError("git")

    monkeypatch.setattr(docs_policy_check.subprocess, "check_output", fake_check_output)

    with pytest.raises(SystemExit) as excinfo:
        docs_policy_check.run_git("status")

    captured = capsys.readouterr()
    assert excinfo.value.code == 1
    assert "git executable not found" in captured.err


def test_run_git_reports_failed_command_and_stderr(monkeypatch, capsys):
    def fake_check_output(*_args, **_kwargs):
        raise subprocess.CalledProcessError(
            returncode=128,
            cmd=["git", "diff", "bad..head"],
            stderr="fatal: bad revision 'bad..head'\n",
        )

    monkeypatch.setattr(docs_policy_check.subprocess, "check_output", fake_check_output)

    with pytest.raises(SystemExit) as excinfo:
        docs_policy_check.run_git("diff", "bad..head")

    captured = capsys.readouterr()
    assert excinfo.value.code == 128
    assert "git command failed: git diff bad..head" in captured.err
    assert "fatal: bad revision 'bad..head'" in captured.err
