from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path
from types import ModuleType


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / ".agents/skills/obsidian-architecture-guard/scripts/validate_agent_settings.py"


def load_validator_module() -> ModuleType:
    spec = importlib.util.spec_from_file_location("validate_agent_settings_under_test", SCRIPT)
    if spec is None or spec.loader is None:
        raise AssertionError("validator module spec could not be loaded")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_encoding_scope_passes_bom_file(tmp_path: Path) -> None:
    doc = tmp_path / "ok.md"
    doc.write_text("한국어 문서\n", encoding="utf-8-sig")

    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--repo-root",
            str(tmp_path),
            "--encoding-scope",
            "ok.md",
        ],
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0
    assert "scoped Korean encoding checks passed" in result.stdout


def test_encoding_scope_rejects_korean_without_bom(tmp_path: Path) -> None:
    doc = tmp_path / "bad.md"
    doc.write_text("한국어 문서\n", encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--repo-root",
            str(tmp_path),
            "--encoding-scope",
            "bad.md",
        ],
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 1
    assert "Korean text requires UTF-8 with BOM" in result.stdout


def test_encoding_scope_uses_long_path_safe_existence(monkeypatch, tmp_path: Path) -> None:
    doc = tmp_path / "deep_report.md"
    doc.write_text("한국어 문서\n", encoding="utf-8-sig")
    validator = load_validator_module()

    monkeypatch.setattr(validator, "path_exists", lambda path: True)
    monkeypatch.setattr(validator, "io_path", lambda path: path)
    monkeypatch.setattr(Path, "exists", lambda self: False)

    errors, warnings = validator.check_encoding_scope(tmp_path.resolve(), ["deep_report.md"])

    assert errors == []
    assert warnings == []


def test_encoding_scope_still_rejects_missing_path(tmp_path: Path) -> None:
    validator = load_validator_module()

    errors, warnings = validator.check_encoding_scope(tmp_path.resolve(), ["missing.md"])

    assert warnings == []
    assert errors == ["missing.md: encoding scope path does not exist"]
