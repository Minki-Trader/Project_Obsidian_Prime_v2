from __future__ import annotations

import argparse
import hashlib
import json
from datetime import date
from pathlib import Path
from typing import Any


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Render the Stage 03 runtime parity report from a materialized comparison summary."
    )
    parser.add_argument(
        "--comparison-json",
        default="stages/03_runtime_parity_closure/02_runs/runtime_parity_pack_0001/runtime_parity_comparison_fpmarkets_v2_runtime_minimum_0001.json",
        help="Repo-relative path to the machine-readable parity comparison summary.",
    )
    parser.add_argument(
        "--python-snapshot",
        default="stages/03_runtime_parity_closure/02_runs/runtime_parity_pack_0001/python_snapshot_fpmarkets_v2_runtime_minimum_0001.json",
        help="Repo-relative path to the Python snapshot JSON.",
    )
    parser.add_argument(
        "--mt5-request",
        default="stages/03_runtime_parity_closure/02_runs/runtime_parity_pack_0001/mt5_snapshot_request_fpmarkets_v2_runtime_minimum_0001.json",
        help="Repo-relative path to the MT5 request pack JSON.",
    )
    parser.add_argument(
        "--mt5-snapshot",
        default="stages/03_runtime_parity_closure/02_runs/runtime_parity_pack_0001/mt5_feature_snapshot_audit_fpmarkets_v2_runtime_minimum_0001.jsonl",
        help="Repo-relative path to the MT5 snapshot JSONL artifact.",
    )
    parser.add_argument(
        "--fixture-bindings",
        default="stages/03_runtime_parity_closure/02_runs/runtime_parity_pack_0001/fixture_bindings_fpmarkets_v2_runtime_minimum_0001.json",
        help="Repo-relative path to the fixture bindings JSON.",
    )
    parser.add_argument(
        "--report-path",
        default="stages/03_runtime_parity_closure/03_reviews/report_fpmarkets_v2_runtime_parity_0001.md",
        help="Repo-relative output path for the rendered markdown report.",
    )
    parser.add_argument(
        "--reviewed-on",
        default=date.today().isoformat(),
        help="Date stamp to write into the rendered report.",
    )
    return parser.parse_args()


def read_text_robust(path: Path) -> str:
    payload = path.read_bytes()
    for encoding in ("utf-8-sig", "utf-8", "cp1252"):
        try:
            return payload.decode(encoding)
        except UnicodeDecodeError:
            continue
    raise RuntimeError(f"Could not decode text from {path}")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(read_text_robust(path))


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def fixture_rows(snapshot: dict[str, Any]) -> list[dict[str, Any]]:
    return list(snapshot["fixtures"].values())


def format_bool(value: bool) -> str:
    return "true" if value else "false"


def collect_dominant_drifts(comparison: dict[str, Any]) -> str:
    ranked: dict[str, float] = {}
    for fixture in comparison["fixtures"].values():
        feature_comparison = fixture.get("feature_comparison") or {}
        for item in feature_comparison.get("top_abs_diffs", []):
            name = str(item["name"])
            abs_diff = float(item["abs_diff"])
            ranked[name] = max(ranked.get(name, 0.0), abs_diff)

    if not ranked:
        return "not_applicable"

    ordered = sorted(ranked.items(), key=lambda item: item[1], reverse=True)[:5]
    return "|".join(f"{name}={abs_diff:.6g}" for name, abs_diff in ordered)


def classify_scope(comparison: dict[str, Any]) -> str:
    aggregate = comparison["aggregate_results"]
    matching = comparison["matching"]
    if matching["missing_fixture_ids"] or matching["unexpected_record_count"] > 0:
        return "first_mt5_snapshot_materialized_but_comparison_incomplete"
    if aggregate["exact_parity"]:
        return "first_evaluated_pack_exact_match"
    if aggregate["tolerance_parity"] and comparison["identity"]["machine_readable_identity_trace"]["traceable"]:
        return "first_evaluated_pack_tolerance_closed_identity_trace_materialized_exact_open"
    if aggregate["tolerance_parity"]:
        return "first_evaluated_pack_tolerance_match_exact_open"
    return "first_evaluated_pack_mismatch_open"


def likely_root_cause(comparison: dict[str, Any]) -> str:
    aggregate = comparison["aggregate_results"]
    matching = comparison["matching"]
    warnings = comparison.get("warnings", [])

    if matching["missing_fixture_ids"]:
        return "the MT5 snapshot export is incomplete because one or more bound fixture windows are still missing"
    if matching["unexpected_record_count"] > 0:
        return "the MT5 snapshot export includes unmatched rows, so the first pack identity is not yet cleanly isolated"
    if aggregate["exact_parity"]:
        return "no contract-surface mismatch was detected on the first five-window pack"
    if aggregate["tolerance_parity"]:
        return "the first pack stays within tolerance and the remaining exact mismatch is consistent with floating-point serialization drift"
    if warnings:
        return "localized mismatch remains on the contract surface; inspect the warning list and dominant drift features before any closure claim"
    return "localized model-input mismatch remains on the first pack"


def what_remains_open(comparison: dict[str, Any]) -> str:
    aggregate = comparison["aggregate_results"]
    matching = comparison["matching"]
    identity_trace = comparison["identity"]["machine_readable_identity_trace"]
    if aggregate["tolerance_parity"]:
        if identity_trace["traceable"]:
            return "runtime-helper parity, broader-sample parity beyond the first five windows, and the explicit Stage 04 artifact-identity closure read"
        return "runtime-helper parity, machine-readable MT5 identity fields inside the snapshot rows, broader-sample parity beyond the first five windows, and Stage 04 artifact-identity closure"
    if matching["missing_fixture_ids"]:
        return "complete the missing MT5 fixture rows, then rerun the comparison and re-read the first pack verdict"
    return "inspect the dominant drift features, re-check timestamp identity, and confirm whether the mismatch is localized or systemic before any closure claim"


def next_sampling_plan(comparison: dict[str, Any]) -> str:
    aggregate = comparison["aggregate_results"]
    if aggregate["tolerance_parity"]:
        if comparison["identity"]["machine_readable_identity_trace"]["traceable"]:
            return "close the Stage 03 model-input parity read, hand the machine-readable identity chain to Stage 04, and decide whether the next sample is broader-sample parity or explicit runtime self-check closure"
        return "update the tracked Stage 03 report and selection read from this evaluated pack, then decide whether the next step is broader-sample parity or direct Stage 04 artifact-identity preparation"
    return "repair the localized MT5 export or feature mismatch, rerun the five-window comparison, and only then revisit the Stage 03 closure read"


def render_report(
    comparison: dict[str, Any],
    python_snapshot: dict[str, Any],
    mt5_request: dict[str, Any],
    fixture_bindings_path: Path,
    python_snapshot_path: Path,
    mt5_request_path: Path,
    mt5_snapshot_path: Path,
    reviewed_on: str,
) -> str:
    aggregate = comparison["aggregate_results"]
    fixtures = fixture_rows(python_snapshot)
    ready_rows = sum(1 for fixture in fixtures if fixture["valid_row"])
    non_ready_rows = len(fixtures) - ready_rows
    windows_utc = "|".join(fixture["timestamp_utc"] for fixture in fixtures)
    windows_ny = "|".join(fixture["timestamp_america_new_york"] for fixture in fixtures)
    identity = comparison["identity"]["expected"]
    identity_trace = comparison["identity"]["machine_readable_identity_trace"]

    negative_fixture = comparison["fixtures"]["fix_negative_required_missing_0001"]
    negative_result = (
        f"MT5-side non-ready evidence is materialized at {negative_fixture['expected_timestamp_utc']} "
        f"with skip_reason={negative_fixture['skip_reason'] or 'empty'}"
        if negative_fixture["status"] == "matched"
        else "the negative fixture is still missing from the MT5-side export"
    )

    report = f"""# Runtime Parity Report

## Identity

- dataset_id: `{identity['dataset_id']}`
- fixture_set_id: `{identity['fixture_set_id']}`
- report_id: `{identity['report_id']}`
- reviewed_on: `{reviewed_on}`
- bundle_id: `{identity['bundle_id']}`
- runtime_id: `{identity['runtime_id']}`
- stage: `03_runtime_parity_closure`

## Scope

- closure_scope: `{classify_scope(comparison)}`
- audited_window(s): `{windows_utc}`
- audited_row_count: `{ready_rows} ready rows + {non_ready_rows} negative non-ready row`

## Inputs

- python_snapshot_artifact: `{python_snapshot_path.as_posix()}`
- mt5_snapshot_artifact: `{mt5_snapshot_path.as_posix()}`
- parser_version: `{python_snapshot['parser_version']}`
- feature_contract_version: `{python_snapshot['feature_contract_version']}`
- runtime_contract_version: `{mt5_request['runtime_contract_version']}`
- feature_order_hash: `{python_snapshot['feature_order_hash']}`
- required_artifact_hashes_checked: `fixture_bindings_sha256=sha256:{sha256_file(fixture_bindings_path)}|python_snapshot_sha256=sha256:{sha256_file(python_snapshot_path)}|mt5_request_sha256=sha256:{sha256_file(mt5_request_path)}|mt5_snapshot_sha256=sha256:{sha256_file(mt5_snapshot_path)}`

## Identity Trace

- request_consistent: `{format_bool(bool(identity_trace['request_consistent']))}`
- mt5_identity_fields_present: `{format_bool(bool(identity_trace['mt5_fields_present']))}`
- mt5_identity_values_match: `{format_bool(bool(identity_trace['mt5_values_match']))}`
- machine_readable_identity_trace: `{format_bool(bool(identity_trace['traceable']))}`

## Fixture Coverage

- regular_closed_bar_sample: `fix_regular_closed_bar_0001`
- session_boundary_sample: `fix_session_boundary_0001`
- dst_sensitive_sample: `fix_dst_sensitive_0001`
- external_alignment_sample: `fix_external_alignment_0001`
- negative_fixture_result: `{negative_result}`

## Timestamp Identity

- evaluated_timestamp_utc: `{windows_utc}`
- evaluated_timestamp_america_new_york: `{windows_ny}`

## Results

- exact_parity: `{format_bool(bool(aggregate['exact_parity']))}`
- tolerance_parity: `{format_bool(bool(aggregate['tolerance_parity']))}`
- max_abs_diff: `{aggregate['max_abs_diff']}`
- dominant_drift_features: `{collect_dominant_drifts(comparison)}`
- zero_shift_share: `{aggregate['zero_shift_share_mean']}`
- decision_flip_count: `not_applicable_python_snapshot_has_no_decision_head`

## Interpretation

- likely_root_cause: `{likely_root_cause(comparison)}`
- what_this_does_not_prove: `no runtime-helper parity closure, no broader-sample parity claim, and no Stage 04 artifact-identity closure yet`
- what_remains_open: `{what_remains_open(comparison)}`

## Required Follow-Up

- next_sampling_plan: `{next_sampling_plan(comparison)}`
- gate_before_closure: `Stage 03 selection docs and workspace state must be updated in the same pass before any closure claim is made from this evaluated pack`
- owner: `Project_Obsidian_Prime_v2 workspace`
"""
    return report


def main() -> int:
    args = parse_args()
    comparison_path = Path(args.comparison_json)
    python_snapshot_path = Path(args.python_snapshot)
    mt5_request_path = Path(args.mt5_request)
    mt5_snapshot_path = Path(args.mt5_snapshot)
    fixture_bindings_path = Path(args.fixture_bindings)
    report_path = Path(args.report_path)

    comparison = load_json(comparison_path)
    python_snapshot = load_json(python_snapshot_path)
    mt5_request = load_json(mt5_request_path)

    rendered = render_report(
        comparison=comparison,
        python_snapshot=python_snapshot,
        mt5_request=mt5_request,
        fixture_bindings_path=fixture_bindings_path,
        python_snapshot_path=python_snapshot_path,
        mt5_request_path=mt5_request_path,
        mt5_snapshot_path=mt5_snapshot_path,
        reviewed_on=args.reviewed_on,
    )

    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(rendered, encoding="utf-8")

    print(
        json.dumps(
            {
                "status": "ok",
                "report_path": str(report_path.resolve()),
                "closure_scope": classify_scope(comparison),
                "exact_parity": comparison["aggregate_results"]["exact_parity"],
                "tolerance_parity": comparison["aggregate_results"]["tolerance_parity"],
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
