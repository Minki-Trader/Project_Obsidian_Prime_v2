from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any, Mapping, Sequence

from foundation.control_plane.kpi_interpretation_audit import ECONOMIC_METRIC_COLUMNS
from foundation.control_plane.ledger import io_path, path_exists


TARGET_CHECK_ID = "kpi_interpretation::missing_or_out_of_scope_row_has_economic_metrics"
IDENTITY_FIELDS = ("ledger_row_id", "run_id", "record_view", "tier_scope", "kpi_scope")


class KpiCleanupError(RuntimeError):
    pass


def cleanup_kpi_interpretation_findings(
    audit_path: Path | str,
    *,
    output_manifest: Path | str | None = None,
    dry_run: bool = False,
) -> dict[str, Any]:
    audit_file = Path(audit_path)
    audit_payload = _read_json(audit_file)
    target_findings = _target_findings(audit_payload)
    by_path: dict[str, list[Mapping[str, Any]]] = defaultdict(list)
    for finding in target_findings:
        details = finding.get("details", {})
        path = str(details.get("path", "")).strip()
        if not path:
            raise KpiCleanupError("Target finding is missing details.path.")
        by_path[path].append(finding)

    manifest: dict[str, Any] = {
        "cleanup_name": "kpi_interpretation_cleanup",
        "source_audit_path": audit_file.as_posix(),
        "source_audit_sha256": _sha256_bytes(io_path(audit_file).read_bytes()),
        "target_check_id": TARGET_CHECK_ID,
        "dry_run": dry_run,
        "target_findings": len(target_findings),
        "cleaned_files": [],
        "cleaned_rows": 0,
        "cleared_values": 0,
    }

    for raw_path, findings in sorted(by_path.items()):
        file_manifest = _clean_file(Path(raw_path), findings, dry_run=dry_run)
        manifest["cleaned_files"].append(file_manifest)
        manifest["cleaned_rows"] += len(file_manifest["rows"])
        manifest["cleared_values"] += sum(len(row["cleared_values"]) for row in file_manifest["rows"])

    manifest_path = Path(output_manifest) if output_manifest else audit_file.parent / "kpi_interpretation_cleanup_manifest.json"
    io_path(manifest_path.parent).mkdir(parents=True, exist_ok=True)
    io_path(manifest_path).write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    manifest["manifest_path"] = manifest_path.as_posix()
    return manifest


def _clean_file(path: Path, findings: Sequence[Mapping[str, Any]], *, dry_run: bool) -> dict[str, Any]:
    if not path_exists(path):
        raise KpiCleanupError(f"Ledger path is missing: {path.as_posix()}")

    raw_bytes = io_path(path).read_bytes()
    before_sha = _sha256_bytes(raw_bytes)
    had_bom = raw_bytes.startswith(b"\xef\xbb\xbf")
    newline = "\r\n" if b"\r\n" in raw_bytes.splitlines(keepends=True)[:1] else "\n"
    text = raw_bytes.decode("utf-8-sig")
    rows = list(csv.reader(io.StringIO(text)))
    if not rows:
        raise KpiCleanupError(f"Ledger path is empty: {path.as_posix()}")
    header = rows[0]
    column_index = {name: index for index, name in enumerate(header)}
    missing_columns = sorted({column for finding in findings for column in _finding_economic_values(finding)} - set(column_index))
    if missing_columns:
        raise KpiCleanupError(f"Ledger {path.as_posix()} is missing expected economic columns: {missing_columns}")

    row_manifests: list[dict[str, Any]] = []
    seen_lines: set[int] = set()
    for finding in sorted(findings, key=lambda item: int(item.get("details", {}).get("line", 0))):
        details = finding.get("details", {})
        line = int(details.get("line", 0))
        if line in seen_lines:
            continue
        seen_lines.add(line)
        row_index = line - 1
        if row_index <= 0 or row_index >= len(rows):
            raise KpiCleanupError(f"Finding line {line} is outside {path.as_posix()}.")
        row = rows[row_index]
        if len(row) < len(header):
            row.extend([""] * (len(header) - len(row)))
        mapping = _row_mapping(header, row)
        _assert_identity_match(path, line, mapping, details)

        cleared_values: dict[str, str] = {}
        for column, expected_value in sorted(_finding_economic_values(finding).items()):
            current_value = str(mapping.get(column, "")).strip()
            if current_value != str(expected_value).strip():
                raise KpiCleanupError(
                    f"Finding value mismatch at {path.as_posix()}:{line} column {column}: "
                    f"expected {expected_value!r}, found {current_value!r}."
                )
            cleared_values[column] = row[column_index[column]]
            row[column_index[column]] = ""

        row_manifests.append(
            {
                "line": line,
                "identity": {field: mapping.get(field, "") for field in IDENTITY_FIELDS},
                "cleared_values": cleared_values,
            }
        )

    after_bytes = raw_bytes
    if not dry_run:
        buffer = io.StringIO()
        writer = csv.writer(buffer, lineterminator=newline)
        writer.writerows(rows)
        output_text = buffer.getvalue()
        encoding = "utf-8-sig" if had_bom else "utf-8"
        io_path(path).write_text(output_text, encoding=encoding, newline="")
        after_bytes = io_path(path).read_bytes()

    return {
        "path": path.as_posix(),
        "before_sha256": before_sha,
        "after_sha256": _sha256_bytes(after_bytes),
        "had_utf8_bom": had_bom,
        "newline": "\\r\\n" if newline == "\r\n" else "\\n",
        "rows": row_manifests,
    }


def _assert_identity_match(path: Path, line: int, row: Mapping[str, str], details: Mapping[str, Any]) -> None:
    mismatches: dict[str, dict[str, str]] = {}
    for field in IDENTITY_FIELDS:
        expected = str(details.get(field, "")).strip()
        if not expected:
            continue
        actual = str(row.get(field, "")).strip()
        if actual != expected:
            mismatches[field] = {"expected": expected, "actual": actual}
    if mismatches:
        raise KpiCleanupError(f"Finding identity mismatch at {path.as_posix()}:{line}: {mismatches}")


def _target_findings(audit_payload: Mapping[str, Any]) -> list[Mapping[str, Any]]:
    return [finding for finding in audit_payload.get("findings", []) if finding.get("check_id") == TARGET_CHECK_ID]


def _finding_economic_values(finding: Mapping[str, Any]) -> Mapping[str, str]:
    values = finding.get("details", {}).get("economic_values", {})
    return {key: str(value) for key, value in values.items() if key in ECONOMIC_METRIC_COLUMNS}


def _row_mapping(header: Sequence[str], row: Sequence[str]) -> dict[str, str]:
    return {column: row[index] if index < len(row) else "" for index, column in enumerate(header)}


def _read_json(path: Path) -> Mapping[str, Any]:
    with io_path(path).open("r", encoding="utf-8-sig") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict):
        raise KpiCleanupError(f"Audit JSON must be an object: {path.as_posix()}")
    return payload


def _sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Clean blocked KPI interpretation rows from ledger CSV files.")
    parser.add_argument("audit_json")
    parser.add_argument("--output-manifest")
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    manifest = cleanup_kpi_interpretation_findings(
        args.audit_json,
        output_manifest=args.output_manifest,
        dry_run=args.dry_run,
    )
    print(json.dumps(manifest, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
