from __future__ import annotations

import csv
import hashlib
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping


STAGE_MIN = 10
STAGE_MAX = 32
STAGE_RE = re.compile(r"(?:stage|stages/|st)(?P<num>\d{2})", re.IGNORECASE)
RUN_RE = re.compile(r"\brun(?P<num>\d{2}[A-Z]*)", re.IGNORECASE)


@dataclass(frozen=True)
class EvidenceRow:
    source: str
    source_path: str
    stage_number: int | None
    run_id: str
    row_id: str
    status: str
    judgment: str
    text: str

    def compact(self) -> dict[str, Any]:
        return {
            "source": self.source,
            "source_path": self.source_path,
            "stage_number": self.stage_number,
            "run_id": self.run_id,
            "row_id": self.row_id,
            "status": self.status,
            "judgment": self.judgment,
            "text": self.text[:2400],
        }


def collect_evidence_rows(root: Path) -> tuple[list[EvidenceRow], dict[str, Any]]:
    rows: list[EvidenceRow] = []
    rows.extend(_registry_rows(root / "docs/registers/run_registry.csv", source="run_registry"))
    rows.extend(_registry_rows(root / "docs/registers/alpha_run_ledger.csv", source="alpha_run_ledger"))
    rows.extend(_stage_doc_rows(root / "stages"))
    rows.extend(_packet_rows(root / "docs/agent_control/packets"))
    rows.extend(_negative_memory_rows(root / "docs/registers/negative_result_register.md"))
    rows = [row for row in rows if _stage_in_scope(row.stage_number)]
    inventory = {
        "stage_min": STAGE_MIN,
        "stage_max": STAGE_MAX,
        "row_count": len(rows),
        "source_counts": _counts(row.source for row in rows),
        "stage_counts": _counts(f"stage{row.stage_number:02d}" for row in rows if row.stage_number),
        "unique_runs": len({row.run_id for row in rows if row.run_id}),
        "source_files": _source_file_inventory(root),
    }
    return rows, inventory


def _registry_rows(path: Path, *, source: str) -> list[EvidenceRow]:
    if not path.exists():
        return []
    output: list[EvidenceRow] = []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        for index, row in enumerate(csv.DictReader(handle)):
            text = " ".join(str(value) for value in row.values() if value)
            stage_number = _stage_number(str(row.get("stage_id", "")) + " " + text)
            output.append(
                EvidenceRow(
                    source=source,
                    source_path=path.as_posix(),
                    stage_number=stage_number,
                    run_id=str(row.get("run_id", "")),
                    row_id=str(row.get("ledger_row_id") or row.get("run_id") or f"{source}:{index}"),
                    status=str(row.get("status", "")),
                    judgment=str(row.get("judgment", "")),
                    text=text,
                )
            )
    return output


def _stage_doc_rows(stages_root: Path) -> list[EvidenceRow]:
    rows: list[EvidenceRow] = []
    if not stages_root.exists():
        return rows
    wanted = ("00_spec", "03_reviews", "04_selected")
    for path in sorted(stages_root.rglob("*.md")):
        rel = path.as_posix()
        if not any(part in path.parts for part in wanted):
            continue
        stage_number = _stage_number(rel)
        if not _stage_in_scope(stage_number):
            continue
        text = _read_text(path, limit=16000)
        rows.append(
            EvidenceRow(
                source="stage_doc",
                source_path=rel,
                stage_number=stage_number,
                run_id=_run_id(text) or _run_id(path.name),
                row_id=path.as_posix(),
                status=_status_hint(text),
                judgment=_judgment_hint(text),
                text=text,
            )
        )
    return rows


def _packet_rows(packet_root: Path) -> list[EvidenceRow]:
    rows: list[EvidenceRow] = []
    if not packet_root.exists():
        return rows
    names = ("work_packet.yaml", "packet.md", "closeout_report.md", "README.md")
    for packet_dir in sorted(path for path in packet_root.iterdir() if path.is_dir()):
        packet_text = packet_dir.name
        stage_number = _stage_number(packet_text)
        if not _stage_in_scope(stage_number):
            continue
        for name in names:
            path = packet_dir / name
            if not path.exists():
                continue
            text = _read_text(path, limit=18000)
            rows.append(
                EvidenceRow(
                    source="agent_control_packet",
                    source_path=path.as_posix(),
                    stage_number=stage_number,
                    run_id=_run_id(packet_text + " " + text),
                    row_id=path.as_posix(),
                    status=_status_hint(text),
                    judgment=_judgment_hint(text),
                    text=packet_text + " " + text,
                )
            )
    return rows


def _negative_memory_rows(path: Path) -> list[EvidenceRow]:
    if not path.exists():
        return []
    rows: list[EvidenceRow] = []
    for index, line in enumerate(_read_text(path).splitlines()):
        if not line.startswith("| `NR-"):
            continue
        stage_number = _stage_number(line)
        rows.append(
            EvidenceRow(
                source="negative_result_register",
                source_path=path.as_posix(),
                stage_number=stage_number,
                run_id=_run_id(line),
                row_id=f"negative_result_register:{index}",
                status="recorded",
                judgment="negative_memory",
                text=line,
            )
        )
    return rows


def _source_file_inventory(root: Path) -> list[dict[str, Any]]:
    paths = [
        root / "docs/registers/run_registry.csv",
        root / "docs/registers/alpha_run_ledger.csv",
        root / "docs/registers/negative_result_register.md",
        root / "docs/workspace/workspace_state.yaml",
        root / "docs/context/current_working_state.md",
    ]
    inventory: list[dict[str, Any]] = []
    for path in paths:
        if path.exists():
            inventory.append({"path": path.as_posix(), "sha256": _sha256(path), "bytes": path.stat().st_size})
    return inventory


def _stage_number(text: str) -> int | None:
    match = STAGE_RE.search(text)
    if not match:
        return None
    return int(match.group("num"))


def _run_id(text: str) -> str:
    match = RUN_RE.search(text)
    return match.group(0) if match else ""


def _stage_in_scope(stage_number: int | None) -> bool:
    return stage_number is not None and STAGE_MIN <= stage_number <= STAGE_MAX


def _read_text(path: Path, *, limit: int | None = None) -> str:
    try:
        text = path.read_text(encoding="utf-8-sig", errors="replace")
    except OSError as exc:
        text = f"read_error:{type(exc).__name__}:{path.as_posix()}"
    return text[:limit] if limit is not None else text


def _status_hint(text: str) -> str:
    lowered = text.lower()
    for token in ("reviewed", "completed", "blocked", "invalid", "inconclusive"):
        if token in lowered:
            return token
    return ""


def _judgment_hint(text: str) -> str:
    lowered = text.lower()
    for token in ("runtime_probe", "structural_scout", "negative", "inconclusive", "blocked"):
        if token in lowered:
            return token
    return ""


def _counts(values: Iterable[str]) -> dict[str, int]:
    output: dict[str, int] = {}
    for value in values:
        output[value] = output.get(value, 0) + 1
    return dict(sorted(output.items()))


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()
