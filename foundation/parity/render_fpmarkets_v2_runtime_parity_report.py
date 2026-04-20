from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter
from datetime import date
from pathlib import Path
from typing import Any

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from foundation.parity.runtime_pack_paths import DEFAULT_MT5_REQUEST, resolve_runtime_pack_paths


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Render a runtime parity report from a materialized comparison summary."
    )
    parser.add_argument(
        "--comparison-json",
        default=None,
        help="Repo-relative path to the machine-readable parity comparison summary.",
    )
    parser.add_argument(
        "--python-snapshot",
        default=None,
        help="Repo-relative path to the Python snapshot JSON.",
    )
    parser.add_argument(
        "--mt5-request",
        default=str(DEFAULT_MT5_REQUEST),
        help="Repo-relative path to the MT5 request pack JSON.",
    )
    parser.add_argument(
        "--mt5-snapshot",
        default=None,
        help="Repo-relative path to the MT5 snapshot JSONL artifact.",
    )
    parser.add_argument(
        "--fixture-bindings",
        default=None,
        help="Repo-relative path to the fixture bindings JSON.",
    )
    parser.add_argument(
        "--report-path",
        default=None,
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


def likely_root_cause(comparison: dict[str, Any], *, ready_row_count: int) -> str:
    aggregate = comparison["aggregate_results"]
    matching = comparison["matching"]
    warnings = comparison.get("warnings", [])

    if matching["missing_fixture_ids"]:
        return "the MT5 snapshot export is incomplete because one or more bound fixture windows are still missing"
    if matching["unexpected_record_count"] > 0:
        return "the MT5 snapshot export includes unmatched rows, so the frozen runtime parity pack is not yet cleanly isolated"
    if aggregate["exact_parity"]:
        return f"no contract-surface mismatch was detected across the evaluated ready rows ({ready_row_count})"
    if aggregate["tolerance_parity"]:
        return "the evaluated pack stays within tolerance and the remaining exact mismatch is consistent with floating-point serialization drift"
    if warnings:
        return "localized mismatch remains on the contract surface; inspect the warning list and dominant drift features before any closure claim"
    return "localized model-input mismatch remains on the evaluated runtime parity pack"


def count_by(items: list[dict[str, Any]], field_name: str, *, fallback_to_fixture_id: bool) -> Counter[str]:
    counter: Counter[str] = Counter()
    for fixture in items:
        value = fixture.get(field_name)
        if value is None and fallback_to_fixture_id:
            value = fixture.get("fixture_id")
        if value is None:
            value = "not_labeled"
        counter[str(value)] += 1
    return counter


def format_counts(counter: Counter[str]) -> str:
    if not counter:
        return "not_applicable"
    ordered = sorted(counter.items(), key=lambda item: (item[0]))
    return "|".join(f"{name}={count}" for name, count in ordered)


def negative_fixture_summary(
    python_snapshot: dict[str, Any],
    comparison: dict[str, Any],
) -> str:
    negative_ids = [
        fixture_id
        for fixture_id, payload in python_snapshot["fixtures"].items()
        if not bool(payload["valid_row"])
    ]
    if not negative_ids:
        return "not_applicable"

    matched_non_ready = 0
    missing_fixture_ids: list[str] = []
    mismatched_skip_reason_ids: list[str] = []
    skip_reason_counts: Counter[str] = Counter()
    for fixture_id in negative_ids:
        fixture_result = comparison["fixtures"].get(fixture_id, {})
        if (
            fixture_result.get("status") == "matched"
            and fixture_result.get("actual_row_ready") is False
            and fixture_result.get("negative_skip_reason_match") is not False
        ):
            matched_non_ready += 1
            skip_reason = str(fixture_result.get("skip_reason") or "").strip() or "empty"
            skip_reason_counts[skip_reason] += 1
        elif fixture_result.get("status") == "matched" and fixture_result.get("actual_row_ready") is False:
            mismatched_skip_reason_ids.append(fixture_id)
        else:
            missing_fixture_ids.append(fixture_id)

    parts = [f"matched_non_ready={matched_non_ready}/{len(negative_ids)}"]
    if skip_reason_counts:
        ordered_reasons = sorted(skip_reason_counts.items(), key=lambda item: (-item[1], item[0]))
        parts.append("skip_reasons=" + ",".join(f"{name}={count}" for name, count in ordered_reasons))
    if mismatched_skip_reason_ids:
        parts.append("mismatched_skip_reason=" + ",".join(sorted(mismatched_skip_reason_ids)))
    if missing_fixture_ids:
        parts.append("missing=" + ",".join(sorted(missing_fixture_ids)))
    return "; ".join(parts)


def stage_specific_what_this_does_not_prove(stage_name: str) -> str:
    if stage_name == "05_exploration_kernel_freeze":
        return (
            "no runtime-helper parity closure, no separate broader-sample parity closure read, "
            "no Tier B or Tier C readiness claim, and no operating promotion"
        )
    if stage_name == "03_runtime_parity_closure":
        return "no runtime-helper parity closure, no broader-sample parity closure, and no operating promotion"
    return "no runtime-helper parity closure and no operating promotion"


def what_remains_open(stage_name: str, comparison: dict[str, Any]) -> str:
    aggregate = comparison["aggregate_results"]
    matching = comparison["matching"]
    identity_trace = comparison["identity"]["machine_readable_identity_trace"]
    if matching["missing_fixture_ids"]:
        return "complete the missing MT5 fixture rows, then rerun the comparison and re-read the evaluated pack verdict"
    if matching["unexpected_record_count"] > 0:
        return "remove or isolate the unexpected MT5 rows, then rerun the same frozen pack before any new claim is made"
    if aggregate["tolerance_parity"]:
        if stage_name == "05_exploration_kernel_freeze":
            if identity_trace["traceable"]:
                return (
                    "runtime-helper parity, any explicit broader-sample closure read beyond this first broader evaluated pack, "
                    "and any downstream exploration or operating promotion"
                )
            return (
                "runtime-helper parity, fully traceable MT5 identity fields across the broader pack, "
                "and any downstream exploration or operating promotion"
            )
        if identity_trace["traceable"]:
            return "runtime-helper parity, broader-sample parity beyond the first five windows, and any downstream operating promotion"
        return "runtime-helper parity, fully traceable MT5 identity fields, broader-sample parity beyond the first five windows, and any downstream operating promotion"
    if stage_name == "05_exploration_kernel_freeze":
        return "inspect the broader-pack mismatch, update the Stage 05 blocker read, and rerun the same frozen 24-window pack before opening any new lane"
    return "inspect the dominant drift features, re-check timestamp identity, and confirm whether the mismatch is localized or systemic before any closure claim"


def next_sampling_plan(stage_name: str, comparison: dict[str, Any]) -> str:
    aggregate = comparison["aggregate_results"]
    if stage_name == "05_exploration_kernel_freeze":
        if aggregate["tolerance_parity"]:
            return (
                "update the Stage 05 read from this first broader evaluated pack, keep Stage 05 open, "
                "and decide whether the next evidence is additional broader-sample coverage or a separate runtime-helper parity lane"
            )
        return (
            "inspect the broader-pack mismatch, update the Stage 05 mismatch-open read, "
            "and rerun the same frozen 24-window pack before opening any downstream lane"
        )
    if aggregate["tolerance_parity"]:
        return (
            "use this evaluated pack to maintain the bounded Stage 03 model-input parity read and keep any "
            "broader-sample or runtime-helper work explicitly downstream"
        )
    return "repair the localized MT5 export or feature mismatch, rerun the same frozen pack, and only then revisit the stage read"


def gate_before_closure(stage_name: str) -> str:
    policy_anchor = (
        "follow the canonical same-pass sync norm in docs/policies/agent_trigger_policy.md "
        "(align workspace state + current working state + active-stage selection/review read, "
        "add a durable decision memo when meaning changes, and update artifact registry rows when identity changes)"
    )
    if stage_name == "05_exploration_kernel_freeze":
        return (
            f"{policy_anchor}; keep Stage 05 open for this evaluated pack and do not blur it into runtime-helper parity, "
            "Tier B or Tier C readiness, or operating promotion"
        )
    if stage_name == "03_runtime_parity_closure":
        return f"{policy_anchor} before any Stage 03 closure claim is made from this evaluated pack"
    return f"{policy_anchor} before any closure claim is made from this evaluated pack"


def render_report(
    comparison: dict[str, Any],
    python_snapshot: dict[str, Any],
    mt5_request: dict[str, Any],
    stage_name: str,
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
    stratum_counts = count_by(fixtures, "selection_stratum", fallback_to_fixture_id=True)
    bucket_counts = count_by(fixtures, "selection_bucket", fallback_to_fixture_id=True)

    report = f"""# Runtime Parity Report

## Identity

- dataset_id: `{identity['dataset_id']}`
- fixture_set_id: `{identity['fixture_set_id']}`
- report_id: `{identity['report_id']}`
- reviewed_on: `{reviewed_on}`
- bundle_id: `{identity['bundle_id']}`
- runtime_id: `{identity['runtime_id']}`
- stage: `{stage_name}`

## Scope

- closure_scope: `{classify_scope(comparison)}`
- audited_window(s): `{windows_utc}`
- audited_row_count: `{ready_rows} ready rows + {non_ready_rows} negative non-ready rows`

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

- fixture_strata: `{format_counts(stratum_counts)}`
- fixture_buckets: `{format_counts(bucket_counts)}`
- negative_fixture_result: `{negative_fixture_summary(python_snapshot, comparison)}`

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

- likely_root_cause: `{likely_root_cause(comparison, ready_row_count=ready_rows)}`
- what_this_does_not_prove: `{stage_specific_what_this_does_not_prove(stage_name)}`
- what_remains_open: `{what_remains_open(stage_name, comparison)}`

## Required Follow-Up

- next_sampling_plan: `{next_sampling_plan(stage_name, comparison)}`
- gate_before_closure: `{gate_before_closure(stage_name)}`
- owner: `Project_Obsidian_Prime_v2 workspace`
"""
    return report


def main() -> int:
    args = parse_args()
    resolved_paths = resolve_runtime_pack_paths(
        Path(args.mt5_request),
        fixture_bindings_path=Path(args.fixture_bindings) if args.fixture_bindings else None,
        python_snapshot_path=Path(args.python_snapshot) if args.python_snapshot else None,
        mt5_snapshot_path=Path(args.mt5_snapshot) if args.mt5_snapshot else None,
        comparison_json_path=Path(args.comparison_json) if args.comparison_json else None,
        report_path=Path(args.report_path) if args.report_path else None,
    )
    comparison_path = resolved_paths.comparison_json_path
    python_snapshot_path = resolved_paths.python_snapshot_path
    mt5_request_path = resolved_paths.mt5_request_path
    mt5_snapshot_path = resolved_paths.mt5_snapshot_path
    fixture_bindings_path = resolved_paths.fixture_bindings_path
    report_path = resolved_paths.report_path

    comparison = load_json(comparison_path)
    python_snapshot = load_json(python_snapshot_path)
    mt5_request = resolved_paths.mt5_request

    rendered = render_report(
        comparison=comparison,
        python_snapshot=python_snapshot,
        mt5_request=mt5_request,
        stage_name=resolved_paths.stage_name,
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
                "stage_name": resolved_paths.stage_name,
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
