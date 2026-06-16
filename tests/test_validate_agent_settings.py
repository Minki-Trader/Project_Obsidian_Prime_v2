from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / ".agents/skills/obsidian-architecture-guard/scripts/validate_agent_settings.py"


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
