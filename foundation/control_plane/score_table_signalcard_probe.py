from __future__ import annotations

import argparse
import csv
import json
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np
import pandas as pd

from foundation.adapters.onnx_signal_adapter import summarize_signal_cards
from foundation.adapters.score_table_signal_adapter import ScoreTableSignalAdapter
from foundation.control_plane.adapter_feasibility_matrix import RUN_ID as SOURCE_RUN_ID
from foundation.control_plane.adapter_feasibility_matrix import build_adapter_feasibility_matrix
from foundation.control_plane.ledger import (
    ALPHA_LEDGER_COLUMNS,
    RUN_REGISTRY_COLUMNS,
    io_path,
    json_ready,
    ledger_pairs,
    read_csv_rows,
    sha256_file_lf_normalized,
    upsert_csv_rows,
    write_csv_rows,
)
from foundation.control_plane.mechanism_role_map import STAGE_ID
from foundation.models.onnx_bridge import ordered_hash, sha256_file


RUN_ID = "run27F_score_table_signalcard_adapter_probe_v1"
PACKET_ID = "stage33_run27F_score_table_signalcard_adapter_probe_v1"
BOUNDARY = "score_table_signalcard_adapter_probe_only_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority"
SELECTED_SOURCE_STAGE_ID = "32_sequence_model__tcn_temporal_convolution_context"
SELECTED_SOURCE_RUN_ID = "run26D_torch_tcn_native_temporal_runtime_probe_v1"
SELECTED_CANDIDATE_ID = f"stage32_{SELECTED_SOURCE_RUN_ID}"
PARITY_TOLERANCE = 2.0e-3


def configure_score_table_signalcard_probe(
    *,
    run_id: str,
    packet_id: str,
    boundary: str,
    selected_candidate_id: str,
    selected_source_stage_id: str,
    selected_source_run_id: str,
    parity_tolerance: float | None = None,
) -> None:
    global RUN_ID, PACKET_ID, BOUNDARY, SELECTED_CANDIDATE_ID, SELECTED_SOURCE_STAGE_ID, SELECTED_SOURCE_RUN_ID, PARITY_TOLERANCE
    RUN_ID = run_id
    PACKET_ID = packet_id
    BOUNDARY = boundary
    SELECTED_CANDIDATE_ID = selected_candidate_id
    SELECTED_SOURCE_STAGE_ID = selected_source_stage_id
    SELECTED_SOURCE_RUN_ID = selected_source_run_id
    if parity_tolerance is not None:
        PARITY_TOLERANCE = float(parity_tolerance)


def current_score_table_signalcard_probe_config() -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "packet_id": PACKET_ID,
        "boundary": BOUNDARY,
        "selected_candidate_id": SELECTED_CANDIDATE_ID,
        "selected_source_stage_id": SELECTED_SOURCE_STAGE_ID,
        "selected_source_run_id": SELECTED_SOURCE_RUN_ID,
        "parity_tolerance": PARITY_TOLERANCE,
    }


@dataclass(frozen=True)
class ScoreTableSignalCardProbeResult:
    summary: dict[str, Any]
    adapter_contract: dict[str, Any]
    parity_report: dict[str, Any]
    signalcard_summary: dict[str, Any]
    adapter_pack_manifest: dict[str, Any]
    stage_rows: list[dict[str, Any]]
    run_registry_row: dict[str, Any]
    artifact_rows: list[dict[str, Any]]


def build_score_table_signalcard_probe(root: Path | str = Path(".")) -> ScoreTableSignalCardProbeResult:
    root_path = Path(root)
    selected = _selected_candidate(root_path)
    source_run_root = root_path / str(selected["source_path"])
    source_manifest = _read_json(source_run_root / "run_manifest.json")
    source_kpi = _read_json(source_run_root / "kpi_record.json")
    source_summary = _read_json_optional(source_run_root / "summary.json")
    assets = _candidate_assets(root_path, source_run_root, source_manifest)
    tier_reports: dict[str, Any] = {}
    tier_contracts: dict[str, Any] = {}
    tier_signal_summaries: dict[str, Any] = {}
    signal_samples: dict[str, Any] = {}
    for tier_name, tier_assets in assets["tiers"].items():
        adapter = ScoreTableSignalAdapter(
            adapter_id=f"{selected['candidate_id']}__{tier_name}_score_table_signalcard",
            source_stage_id=str(selected["stage_id"]),
            source_run_id=str(selected["run_id"]),
            mechanism_class=str(selected["mechanism_class"]),
            roles=tuple(role for role in selected["roles"] if role != "Deferred"),
            feature_names=tuple(tier_assets["feature_names"]),
            score_table_path=root_path / str(tier_assets["score_table_path"]),
            nonflat_threshold=float(tier_assets["threshold"]),
            tier_scope=str(tier_assets["tier_scope"]),
            claim_boundary=BOUNDARY,
        )
        tier_contracts[tier_name] = {
            "candidate_contract": adapter.candidate_contract().to_dict(),
            "score_table": _artifact_identity(root_path, root_path / str(tier_assets["score_table_path"])),
            "feature_order_hash": ordered_hash(tuple(tier_assets["feature_names"])),
            "nonflat_threshold": float(tier_assets["threshold"]),
            "source_score_table_parity": tier_assets["source_score_table_parity"],
        }
        split_reports: dict[str, Any] = {}
        split_summaries: dict[str, Any] = {}
        tier_samples: dict[str, Any] = {}
        predictions = pd.read_parquet(io_path(root_path / str(tier_assets["prediction_path"])))
        predictions = predictions.copy()
        predictions["timestamp_key"] = pd.to_datetime(predictions["timestamp"], utc=True).dt.strftime("%Y-%m-%dT%H:%M:%SZ")
        for split_name, matrix_path in tier_assets["feature_matrices"].items():
            frame = pd.read_csv(io_path(root_path / str(matrix_path)))
            values = frame.loc[:, list(tier_assets["feature_names"])].to_numpy(dtype="float64", copy=False)
            expected_prob = _expected_probabilities(frame, predictions, split_name)
            parity = adapter.parity_report_against_probabilities(values, expected_prob, tolerance=PARITY_TOLERANCE)
            table_prob = adapter.table_probabilities(values)
            expected_cards = adapter.signal_cards(expected_prob, row_ids=_row_ids(frame))
            table_cards = adapter.signal_cards(table_prob, row_ids=_row_ids(frame))
            direction_mismatches = sum(1 for left, right in zip(expected_cards, table_cards) if left.direction != right.direction)
            trading_action_mismatches = sum(
                1
                for left, right in zip(expected_cards, table_cards)
                if _trading_action(left.direction) != _trading_action(right.direction)
            )
            split_reports[split_name] = {
                **parity,
                "score_table_vs_source_prediction_signal_direction_mismatches": direction_mismatches,
                "score_table_vs_source_prediction_signal_direction_mismatch_rate": float(direction_mismatches / len(table_cards))
                if table_cards
                else 0.0,
                "score_table_vs_source_prediction_trading_action_mismatches": trading_action_mismatches,
                "score_table_vs_source_prediction_trading_action_mismatch_rate": float(trading_action_mismatches / len(table_cards))
                if table_cards
                else 0.0,
                "feature_matrix": str(matrix_path),
                "feature_matrix_sha256": sha256_file_lf_normalized(root_path / str(matrix_path)),
                "prediction_path": str(tier_assets["prediction_path"]),
                "prediction_sha256": sha256_file(root_path / str(tier_assets["prediction_path"])),
            }
            split_summaries[split_name] = {
                "source_prediction": summarize_signal_cards(expected_cards),
                "score_table": summarize_signal_cards(table_cards),
            }
            tier_samples[split_name] = [card.to_dict() for card in table_cards[:10]]
        tier_reports[tier_name] = split_reports
        tier_signal_summaries[tier_name] = split_summaries
        signal_samples[tier_name] = tier_samples

    adapter_contract = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "selected_candidate": selected,
        "contract_family": "SignalCard/ScoreTableSignalAdapter",
        "tiers": tier_contracts,
        "output_contract": {"output_type": "SignalCard.v1", "safe_fallback": "no_trade"},
        "claim_boundary": BOUNDARY,
    }
    parity_report = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "selected_candidate_id": selected["candidate_id"],
        "passed": _all_parity_passed(tier_reports),
        "tiers": tier_reports,
        "source_runtime_probe": _source_runtime_probe_summary(source_manifest, source_kpi, source_summary),
        "claim_boundary": BOUNDARY,
    }
    signalcard_summary = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "selected_candidate_id": selected["candidate_id"],
        "tiers": tier_signal_summaries,
        "samples": signal_samples,
        "claim_boundary": BOUNDARY,
    }
    adapter_pack_manifest = _adapter_pack_manifest(root_path, selected, adapter_contract, parity_report, assets, source_manifest)
    summary = _summary(selected, parity_report, signalcard_summary, adapter_pack_manifest, source_manifest, source_kpi, source_summary)
    return ScoreTableSignalCardProbeResult(
        summary=summary,
        adapter_contract=adapter_contract,
        parity_report=parity_report,
        signalcard_summary=signalcard_summary,
        adapter_pack_manifest=adapter_pack_manifest,
        stage_rows=_stage_ledger_rows(summary),
        run_registry_row=_run_registry_row(summary),
        artifact_rows=_artifact_rows(),
    )


def write_score_table_signalcard_probe_packet(root: Path | str = Path("."), *, generated_at_utc: str | None = None) -> dict[str, Any]:
    root_path = Path(root)
    generated_at = generated_at_utc or datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    result = build_score_table_signalcard_probe(root_path)
    run_root = root_path / "stages" / STAGE_ID / "02_runs" / RUN_ID
    reports_root = run_root / "reports"
    adapter_pack_root = run_root / "adapter_pack"
    packet_root = root_path / "docs/agent_control/packets" / PACKET_ID
    io_path(reports_root).mkdir(parents=True, exist_ok=True)
    io_path(adapter_pack_root).mkdir(parents=True, exist_ok=True)
    io_path(packet_root).mkdir(parents=True, exist_ok=True)

    adapter_contract_path = run_root / "adapter_contract.json"
    parity_report_path = run_root / "score_table_parity_report.json"
    signalcard_summary_path = run_root / "signalcard_summary.json"
    adapter_pack_manifest_path = adapter_pack_root / "adapter_pack_manifest.json"
    manifest_path = run_root / "run_manifest.json"
    result_summary_path = reports_root / "result_summary.md"
    aggregate_summary_path = packet_root / "aggregate_summary.json"

    _write_json(adapter_contract_path, {"generated_at_utc": generated_at, **result.adapter_contract})
    _write_json(parity_report_path, {"generated_at_utc": generated_at, **result.parity_report})
    _write_json(signalcard_summary_path, {"generated_at_utc": generated_at, **result.signalcard_summary})
    _write_json(adapter_pack_manifest_path, {"generated_at_utc": generated_at, **result.adapter_pack_manifest})
    manifest = _manifest(
        root_path,
        generated_at,
        adapter_contract_path,
        parity_report_path,
        signalcard_summary_path,
        adapter_pack_manifest_path,
        result,
    )
    _write_json(manifest_path, manifest)
    _write_markdown(result_summary_path, _result_summary_markdown(generated_at, result))
    aggregate = {
        "packet_id": PACKET_ID,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "source_run_id": SOURCE_RUN_ID,
        "status": "reviewed_score_table_signalcard_adapter_probe_completed"
        if result.summary["parity_passed"]
        else "blocked_score_table_signalcard_adapter_probe",
        "judgment": result.summary["judgment"],
        "boundary": BOUNDARY,
        "generated_at_utc": generated_at,
        "adapter_contract_path": _rel(root_path, adapter_contract_path),
        "parity_report_path": _rel(root_path, parity_report_path),
        "signalcard_summary_path": _rel(root_path, signalcard_summary_path),
        "adapter_pack_manifest_path": _rel(root_path, adapter_pack_manifest_path),
        "run_manifest_path": _rel(root_path, manifest_path),
        "result_summary_path": _rel(root_path, result_summary_path),
        "selected_candidate": result.summary["selected_candidate"],
        "parity_passed": result.summary["parity_passed"],
        "signal_direction_mismatches": result.summary["signal_direction_mismatches"],
        "trading_action_mismatches": result.summary["trading_action_mismatches"],
        "adapter_readiness_decision": result.summary["adapter_readiness_decision"],
        "onnx_readiness_decision": result.summary["onnx_readiness_decision"],
        "required_gates": result.summary["required_gates"],
    }
    _write_json(aggregate_summary_path, aggregate)
    _upsert_registers(root_path, result)
    upsert_csv_rows(
        root_path / "stages" / STAGE_ID / "03_reviews/stage_run_ledger.csv",
        ALPHA_LEDGER_COLUMNS,
        result.stage_rows,
        key="ledger_row_id",
    )
    return aggregate


def _selected_candidate(root: Path) -> dict[str, Any]:
    selected = build_adapter_feasibility_matrix(root).summary["selected_next_probe"]
    if selected.get("candidate_id") == SELECTED_CANDIDATE_ID:
        return dict(selected)
    matrix_path = root / "stages" / STAGE_ID / "02_runs/run27E_adapter_feasibility_matrix_v1/adapter_feasibility_matrix.csv"
    if io_path(matrix_path).exists():
        with io_path(matrix_path).open(encoding="utf-8-sig", newline="") as handle:
            for row in csv.DictReader(handle):
                if row.get("candidate_id") == SELECTED_CANDIDATE_ID:
                    return {
                        "candidate_id": row["candidate_id"],
                        "stage_id": row["stage_id"],
                        "run_id": row["run_id"],
                        "mechanism_class": row["mechanism_class"],
                        "roles": [role for role in str(row.get("roles") or "").split("|") if role],
                        "adapter_probe_route": row.get("adapter_probe_route"),
                        "feasibility_state": row.get("feasibility_state"),
                        "next_action": row.get("next_action"),
                        "source_path": row.get("source_path") or f"stages/{row['stage_id']}/02_runs/{row['run_id']}",
                        "decision": row.get("selected_next_probe") == "1",
                    }
    raise RuntimeError(f"{RUN_ID} expected selected candidate {SELECTED_CANDIDATE_ID}, got: {selected.get('candidate_id')}")


def _candidate_assets(root: Path, source_run_root: Path, source_manifest: Mapping[str, Any]) -> dict[str, Any]:
    artifacts = dict(source_manifest["model_artifacts"])
    feature_matrices = dict(source_manifest.get("feature_matrices") or {})
    features = tuple(str(name) for name in artifacts["runtime_feature_order"])
    thresholds = dict(artifacts["thresholds"])
    tier_a_feature_matrices, tier_b_feature_matrices = _feature_matrix_paths(root, source_run_root, feature_matrices)
    return {
        "source_run_root": source_run_root,
        "feature_names": features,
        "tiers": {
            "tier_a": {
                "tier_scope": "Tier A",
                "feature_names": features,
                "score_table_path": _rel(root, _resolve_path(root, artifacts["tier_a_score_table"]["path"])),
                "threshold": float(thresholds["tier_a"]),
                "prediction_path": _prediction_path(root, source_run_root, source_manifest, "tier_a"),
                "source_score_table_parity": artifacts["score_table_parity"]["tier_a"],
                "feature_matrices": tier_a_feature_matrices,
            },
            "tier_b": {
                "tier_scope": "Tier B fallback",
                "feature_names": features,
                "score_table_path": _rel(root, _resolve_path(root, artifacts["tier_b_score_table"]["path"])),
                "threshold": float(thresholds["tier_b"]),
                "prediction_path": _prediction_path(root, source_run_root, source_manifest, "tier_b"),
                "source_score_table_parity": artifacts["score_table_parity"]["tier_b"],
                "feature_matrices": tier_b_feature_matrices,
            },
        },
    }


def _feature_matrix_paths(
    root: Path,
    source_run_root: Path,
    feature_matrices: Mapping[str, Any],
) -> tuple[dict[str, str], dict[str, str]]:
    if feature_matrices:
        return (
            {
                "validation": _rel(root, _resolve_path(root, feature_matrices["tier_a_validation_is"]["path"])),
                "oos": _rel(root, _resolve_path(root, feature_matrices["tier_a_oos"]["path"])),
            },
            {
                "validation": _rel(root, _resolve_path(root, feature_matrices["tier_b_fallback_validation_is"]["path"])),
                "oos": _rel(root, _resolve_path(root, feature_matrices["tier_b_fallback_oos"]["path"])),
            },
        )
    return (
        {
            "validation": _rel(root, _first_existing(source_run_root / "features", ("tier_a_validation_is_quantile_tail_features.csv",))),
            "oos": _rel(root, _first_existing(source_run_root / "features", ("tier_a_oos_quantile_tail_features.csv",))),
        },
        {
            "validation": _rel(root, _first_existing(source_run_root / "features", ("tier_b_fallback_validation_is_quantile_tail_features.csv",))),
            "oos": _rel(root, _first_existing(source_run_root / "features", ("tier_b_fallback_oos_quantile_tail_features.csv",))),
        },
    )


def _prediction_path(root: Path, source_run_root: Path, source_manifest: Mapping[str, Any], tier_key: str) -> str:
    prediction_artifacts = dict(source_manifest.get("prediction_artifacts") or {})
    artifact_key = "tier_a_predictions" if tier_key == "tier_a" else "tier_b_predictions"
    if artifact_key in prediction_artifacts:
        return _rel(root, _resolve_path(root, prediction_artifacts[artifact_key]["path"]))
    filename = "tier_a_stage32_runtime_predictions.parquet" if tier_key == "tier_a" else "tier_b_stage32_runtime_predictions.parquet"
    return _rel(root, source_run_root / "predictions" / filename)


def _first_existing(directory: Path, names: Sequence[str]) -> Path:
    for name in names:
        path = directory / name
        if io_path(path).exists():
            return path
    raise FileNotFoundError(f"None of the expected feature matrices exist under {directory}: {', '.join(names)}")


def _expected_probabilities(frame: pd.DataFrame, predictions: pd.DataFrame, split_name: str) -> np.ndarray:
    work = frame.copy()
    work["timestamp_key"] = pd.to_datetime(work["timestamp_utc"], utc=True).dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    source = predictions.loc[predictions["split"].astype(str).eq(split_name), ["timestamp_key", "p_short", "p_flat", "p_long"]]
    merged = work[["timestamp_key"]].merge(source, on="timestamp_key", how="left", validate="one_to_one")
    missing = merged[["p_short", "p_flat", "p_long"]].isna().any(axis=1)
    if bool(missing.any()):
        raise RuntimeError(f"Missing source prediction rows for {int(missing.sum())} feature rows in split {split_name}.")
    return merged[["p_short", "p_flat", "p_long"]].to_numpy(dtype="float64", copy=False)


def _summary(
    selected: Mapping[str, Any],
    parity_report: Mapping[str, Any],
    signalcard_summary: Mapping[str, Any],
    adapter_pack_manifest: Mapping[str, Any],
    source_manifest: Mapping[str, Any],
    source_kpi: Mapping[str, Any],
    source_summary: Mapping[str, Any],
) -> dict[str, Any]:
    split_reports = [
        split
        for tier_payload in parity_report["tiers"].values()
        for split in tier_payload.values()
    ]
    rows = sum(int(report["rows"]) for report in split_reports)
    direction_mismatches = sum(int(report["score_table_vs_source_prediction_signal_direction_mismatches"]) for report in split_reports)
    trading_action_mismatches = sum(int(report["score_table_vs_source_prediction_trading_action_mismatches"]) for report in split_reports)
    max_abs_diff = max(float(report["max_abs_diff"]) for report in split_reports) if split_reports else 0.0
    exact_direction_gap = direction_mismatches > 0
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "source_run_id": SOURCE_RUN_ID,
        "selected_candidate": dict(selected),
        "judgment": "inconclusive_score_table_signalcard_adapter_probe_completed_with_exact_signalcard_direction_gap"
        if exact_direction_gap
        else "inconclusive_score_table_signalcard_adapter_probe_completed",
        "parity_passed": bool(parity_report["passed"]),
        "parity_rows": rows,
        "parity_max_abs_diff": max_abs_diff,
        "parity_tolerance": PARITY_TOLERANCE,
        "signal_direction_mismatches": direction_mismatches,
        "trading_action_mismatches": trading_action_mismatches,
        "source_mt5_external_verification_status": source_manifest.get("external_verification_status")
        or source_kpi.get("external_verification_status")
        or source_summary.get("external_verification_status"),
        "adapter_pack_manifest_id": adapter_pack_manifest["adapter_pack_id"],
        "adapter_readiness_decision": "defer_exact_signalcard_direction_gap" if exact_direction_gap else "adapter_contract_reusable_for_next_probe",
        "onnx_readiness_decision": "defer_onnx_export_score_table_runtime_advantage_not_established",
        "runtime_handoff_decision": f"existing_{SELECTED_SOURCE_STAGE_ID}_score_table_mt5_runtime_probe_referenced_not_new_terminal_run",
        "claim_boundary": BOUNDARY,
        "signalcard_counts": _signalcard_counts(signalcard_summary),
        "required_gates": {
            "why_this_work": "completed",
            "evidence_gap": "completed",
            "input_data_features_split_run_id": "completed",
            "artifact_paths": "completed",
            "validation_oos_wfo_mt5_results": f"completed_by_existing_{SELECTED_SOURCE_RUN_ID}_evidence_reference",
            "failure_or_defer_reason": "exact_signalcard_direction_gap_and_onnx_deferred_runtime_advantage_absent"
            if exact_direction_gap
            else "onnx_deferred_runtime_advantage_absent",
            "claim_boundary": BOUNDARY,
            "next_action_or_stop_rule": "score_table_mt5_handoff_identity_audit_or_segmented_catboost_adapter_probe",
        },
    }


def _adapter_pack_manifest(
    root: Path,
    selected: Mapping[str, Any],
    adapter_contract: Mapping[str, Any],
    parity_report: Mapping[str, Any],
    assets: Mapping[str, Any],
    source_manifest: Mapping[str, Any],
) -> dict[str, Any]:
    tiers: dict[str, Any] = {}
    for tier_name, tier_assets in assets["tiers"].items():
        table_path = root / str(tier_assets["score_table_path"])
        feature_matrices = {
            split_name: {
                "path": str(matrix_path),
                "sha256_lf_normalized": sha256_file_lf_normalized(root / str(matrix_path)),
            }
            for split_name, matrix_path in tier_assets["feature_matrices"].items()
        }
        tiers[tier_name] = {
            "tier_scope": tier_assets["tier_scope"],
            "feature_count": len(tier_assets["feature_names"]),
            "feature_names": list(tier_assets["feature_names"]),
            "feature_order_hash": ordered_hash(tuple(tier_assets["feature_names"])),
            "nonflat_threshold": float(tier_assets["threshold"]),
            "score_table": {
                "path": str(tier_assets["score_table_path"]),
                "sha256": sha256_file(table_path),
            },
            "feature_matrices": feature_matrices,
            "prediction_path": str(tier_assets["prediction_path"]),
            "prediction_sha256": sha256_file(root / str(tier_assets["prediction_path"])),
            "score_table_vs_prediction_parity": parity_report["tiers"][tier_name],
        }
    return {
        "adapter_pack_id": f"{RUN_ID}__{selected['candidate_id']}__score_table_signalcard_manifest",
        "selected_candidate_id": selected["candidate_id"],
        "source_stage_id": selected["stage_id"],
        "source_run_id": selected["run_id"],
        "contract_family": adapter_contract["contract_family"],
        "packaging_policy": "manifest_only_existing_score_table_artifacts_no_reexport",
        "source_runtime_probe_external_verification_status": source_manifest.get("external_verification_status"),
        "parity_passed": parity_report["passed"],
        "tiers": tiers,
        "claim_boundary": BOUNDARY,
    }


def _source_runtime_probe_summary(
    source_manifest: Mapping[str, Any],
    source_kpi: Mapping[str, Any],
    source_summary: Mapping[str, Any],
) -> dict[str, Any]:
    return {
        "source_run_id": source_manifest.get("run_id"),
        "source_stage_id": source_manifest.get("stage_id"),
        "external_verification_status": source_manifest.get("external_verification_status")
        or source_kpi.get("external_verification_status")
        or source_summary.get("external_verification_status"),
        "judgment": source_manifest.get("judgment") or source_kpi.get("judgment") or source_summary.get("closure_judgment"),
        "attempt_count": len(source_manifest.get("attempts") or source_summary.get("execution_results") or []),
        "strategy_tester_report_count": len(source_manifest.get("strategy_tester_reports") or source_summary.get("strategy_tester_reports") or []),
        "known_runtime_difference": (source_manifest.get("model_artifacts") or {}).get("known_runtime_difference"),
    }


def _all_parity_passed(tier_reports: Mapping[str, Mapping[str, Mapping[str, Any]]]) -> bool:
    return all(bool(split_report["passed"]) for tier_report in tier_reports.values() for split_report in tier_report.values())


def _signalcard_counts(signalcard_summary: Mapping[str, Any]) -> dict[str, Any]:
    counts: dict[str, int] = {}
    for tier_payload in signalcard_summary["tiers"].values():
        for split_payload in tier_payload.values():
            for direction, count in split_payload["score_table"]["direction_counts"].items():
                counts[direction] = counts.get(direction, 0) + int(count)
    return dict(sorted(counts.items()))


def _trading_action(direction: str) -> str:
    return "flat_or_no_trade" if direction in {"flat", "no_trade"} else direction


def _stage_ledger_rows(summary: Mapping[str, Any]) -> list[dict[str, Any]]:
    run_root = f"stages/{STAGE_ID}/02_runs/{RUN_ID}"
    return [
        {
            "ledger_row_id": f"{RUN_ID}__adapter_contract",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "adapter_contract",
            "parent_run_id": RUN_ID,
            "record_view": "ScoreTable_SignalCard_adapter_contract",
            "tier_scope": "Tier A+B",
            "kpi_scope": "adapter_contract",
            "scoreboard_lane": "runtime_parity",
            "status": "completed",
            "judgment": summary["judgment"],
            "path": f"{run_root}/adapter_contract.json",
            "primary_kpi": ledger_pairs((("parity_rows", summary["parity_rows"]),)),
            "guardrail_kpi": "safe_fallback=no_trade;input_feature_order_fixed=true",
            "external_verification_status": "referenced_existing_completed",
            "notes": f"SignalCard adapter contract wraps existing {SELECTED_SOURCE_RUN_ID} score-table artifacts; no alpha quality or promotion claim.",
        },
        {
            "ledger_row_id": f"{RUN_ID}__score_table_vs_prediction_parity",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "score_table_vs_prediction_parity",
            "parent_run_id": RUN_ID,
            "record_view": "score_table_signalcard_parity",
            "tier_scope": "Tier A+B",
            "kpi_scope": "runtime_parity",
            "scoreboard_lane": "runtime_parity",
            "status": "completed" if summary["parity_passed"] and summary["signal_direction_mismatches"] == 0 else "blocked",
            "judgment": summary["onnx_readiness_decision"],
            "path": f"{run_root}/score_table_parity_report.json",
            "primary_kpi": ledger_pairs(
                (
                    ("parity_rows", summary["parity_rows"]),
                    ("max_abs_diff", summary["parity_max_abs_diff"]),
                    ("direction_mismatches", summary["signal_direction_mismatches"]),
                    ("trading_action_mismatches", summary["trading_action_mismatches"]),
                )
            ),
            "guardrail_kpi": f"tolerance={PARITY_TOLERANCE};direction_parity_required=true",
            "external_verification_status": "referenced_existing_completed",
            "notes": f"Score-table probabilities and SignalCard directions are compared against stored {SELECTED_SOURCE_RUN_ID} runtime predictions.",
        },
        {
            "ledger_row_id": f"{RUN_ID}__adapter_pack_manifest",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "adapter_pack_manifest",
            "parent_run_id": RUN_ID,
            "record_view": "existing_score_table_signalcard_adapter_pack",
            "tier_scope": "Tier A+B",
            "kpi_scope": "runtime_packaging_gate",
            "scoreboard_lane": "runtime_parity",
            "status": "completed",
            "judgment": summary["runtime_handoff_decision"],
            "path": f"{run_root}/adapter_pack/adapter_pack_manifest.json",
            "primary_kpi": ledger_pairs((("score_table_artifact_generated", 0), ("adapter_pack_manifest_generated", 1))),
            "guardrail_kpi": "manifest_only_no_reexport;mt5_handoff_reference_existing",
            "external_verification_status": "referenced_existing_completed",
            "notes": f"Adapter pack records existing score-table paths and hashes; no new MT5 terminal run in {RUN_ID}.",
        },
    ]


def _run_registry_row(summary: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "signalcard_adapter_score_table_parity_probe",
        "status": "reviewed",
        "judgment": summary["judgment"],
        "path": f"stages/{STAGE_ID}/02_runs/{RUN_ID}",
        "notes": ledger_pairs(
            (
                ("selected_candidate", summary["selected_candidate"]["candidate_id"]),
                ("parity_passed", summary["parity_passed"]),
                ("parity_rows", summary["parity_rows"]),
                ("direction_mismatches", summary["signal_direction_mismatches"]),
                ("trading_action_mismatches", summary["trading_action_mismatches"]),
                ("boundary", BOUNDARY),
            )
        ),
    }


def _artifact_rows() -> list[dict[str, Any]]:
    run_root = f"stages/{STAGE_ID}/02_runs/{RUN_ID}"
    return [
        {
            "artifact_id": f"{RUN_ID}__adapter_contract",
            "type": "ScoreTable_SignalCard_adapter_contract",
            "path": f"{run_root}/adapter_contract.json",
            "status": "tracked_reviewed",
            "notes": f"SignalCard adapter contract for the selected {SELECTED_SOURCE_RUN_ID} score-table candidate.",
        },
        {
            "artifact_id": f"{RUN_ID}__parity_report",
            "type": "score_table_signalcard_parity_report",
            "path": f"{run_root}/score_table_parity_report.json",
            "status": "tracked_reviewed",
            "notes": "Score-table vs stored runtime prediction probability and SignalCard direction parity.",
        },
        {
            "artifact_id": f"{RUN_ID}__signalcard_summary",
            "type": "SignalCard_output_summary",
            "path": f"{run_root}/signalcard_summary.json",
            "status": "tracked_reviewed",
            "notes": "SignalCard direction, score, confidence summaries and samples.",
        },
        {
            "artifact_id": f"{RUN_ID}__adapter_pack_manifest",
            "type": "existing_score_table_adapter_pack_manifest",
            "path": f"{run_root}/adapter_pack/adapter_pack_manifest.json",
            "status": "tracked_reviewed",
            "notes": "Manifest-only adapter pack that references existing score-table artifacts and hashes.",
        },
    ]


def _manifest(
    root: Path,
    generated_at: str,
    adapter_contract_path: Path,
    parity_report_path: Path,
    signalcard_summary_path: Path,
    adapter_pack_manifest_path: Path,
    result: ScoreTableSignalCardProbeResult,
) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "packet_id": PACKET_ID,
        "source_run_id": SOURCE_RUN_ID,
        "generated_at_utc": generated_at,
        "producer": "foundation.control_plane.score_table_signalcard_probe",
        "outputs": {
            "adapter_contract": {"path": _rel(root, adapter_contract_path), "sha256": sha256_file_lf_normalized(adapter_contract_path)},
            "score_table_parity_report": {"path": _rel(root, parity_report_path), "sha256": sha256_file_lf_normalized(parity_report_path)},
            "signalcard_summary": {"path": _rel(root, signalcard_summary_path), "sha256": sha256_file_lf_normalized(signalcard_summary_path)},
            "adapter_pack_manifest": {
                "path": _rel(root, adapter_pack_manifest_path),
                "sha256": sha256_file_lf_normalized(adapter_pack_manifest_path),
            },
        },
        "selected_candidate": result.summary["selected_candidate"],
        "claim_boundary": BOUNDARY,
    }


def _result_summary_markdown(generated_at: str, result: ScoreTableSignalCardProbeResult) -> str:
    summary = result.summary
    selected = summary["selected_candidate"]
    lines = [
        f"# Stage33 {RUN_ID} Score-Table SignalCard Adapter Probe(33단계 {RUN_ID} 점수표 신호 카드 어댑터 탐침)",
        "",
        f"- generated_at_utc(생성 시각 UTC): `{generated_at}`",
        f"- run_id(실행 ID): `{RUN_ID}`",
        f"- selected candidate(선택 후보): `{selected['candidate_id']}`",
        f"- parity rows(동등성 행): `{summary['parity_rows']}`",
        f"- parity passed(동등성 통과): `{summary['parity_passed']}`",
        f"- max abs diff(최대 절대 차이): `{summary['parity_max_abs_diff']}`",
        f"- signal direction mismatches(신호 방향 불일치): `{summary['signal_direction_mismatches']}`",
        f"- trading action mismatches(거래 행동 불일치): `{summary['trading_action_mismatches']}`",
        f"- adapter readiness decision(어댑터 준비 결정): `{summary['adapter_readiness_decision']}`",
        f"- ONNX readiness decision(온닉스 준비 결정): `{summary['onnx_readiness_decision']}`",
        "",
        "## Evidence Gate(근거 게이트)",
        "",
        f"{RUN_ID}(현재 실행)는 {SELECTED_SOURCE_RUN_ID}(원천 실행)의 score-table(점수표)을 SignalCard adapter(신호 카드 어댑터)로 감싸고 validation/OOS(검증/표본외) feature matrix(피처 행렬)와 stored runtime prediction(저장 런타임 예측)을 비교했다.",
        "",
        "효과(effect, 효과)는 ONNX(온닉스)가 아닌 score-table handoff(점수표 인계)도 같은 SignalCard output contract(신호 카드 출력 계약) 안에서 재사용 가능한지 확인하는 것이다.",
        "",
        "## Adapter Pack(어댑터 팩)",
        "",
        f"- adapter_pack_id(어댑터 팩 ID): `{summary['adapter_pack_manifest_id']}`",
        "- packaging policy(포장 정책): `manifest_only_existing_score_table_artifacts_no_reexport(기존 점수표 산출물 목록 전용 포장, 재내보내기 없음)`",
        "",
        "## Explicit Non-Claims(명시적 비주장)",
        "",
        "- alpha quality(알파 품질) 주장 없음",
        "- operating baseline(운영 기준선) 주장 없음",
        "- promotion candidate(승격 후보) 주장 없음",
        "- runtime authority(런타임 권위) 주장 없음",
        "- live readiness(실거래 준비) 주장 없음",
    ]
    return "\n".join(lines) + "\n"


def _row_ids(frame: pd.DataFrame) -> list[str]:
    if "timestamp_utc" in frame.columns:
        return [str(value) for value in frame["timestamp_utc"].tolist()]
    if "row_index" in frame.columns:
        return [str(value) for value in frame["row_index"].tolist()]
    return [str(index) for index in range(len(frame))]


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def _read_json_optional(path: Path) -> dict[str, Any]:
    if not io_path(path).exists():
        return {}
    return _read_json(path)


def _resolve_path(root: Path, value: Any) -> Path:
    path = Path(str(value))
    if path.is_absolute():
        return path
    return root / path


def _artifact_identity(root: Path, path: Path) -> dict[str, Any]:
    return {"path": _rel(root, path), "sha256": sha256_file(path)}


def _write_json(path: Path, payload: Mapping[str, Any]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _write_markdown(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text, encoding="utf-8-sig")


def _upsert_registers(root: Path, result: ScoreTableSignalCardProbeResult) -> None:
    upsert_csv_rows(root / "docs/registers/run_registry.csv", RUN_REGISTRY_COLUMNS, [result.run_registry_row], key="run_id")
    upsert_csv_rows(root / "docs/registers/alpha_run_ledger.csv", ALPHA_LEDGER_COLUMNS, result.stage_rows, key="ledger_row_id")
    artifact_path = root / "docs/registers/artifact_registry.csv"
    existing = read_csv_rows(artifact_path)
    columns = ("artifact_id", "type", "path", "status", "notes")
    new_ids = {row["artifact_id"] for row in result.artifact_rows}
    rows = [row for row in existing if row.get("artifact_id") not in new_ids]
    rows.extend(result.artifact_rows)
    write_csv_rows(artifact_path, columns, rows)


def _rel(root: Path, path: Path) -> str:
    return path.resolve().relative_to(root.resolve()).as_posix()


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run Stage33 score-table SignalCard adapter probe.")
    parser.add_argument("--root", default=".")
    parser.add_argument("--summary-only", action="store_true")
    args = parser.parse_args(argv)
    if args.summary_only:
        result = build_score_table_signalcard_probe(Path(args.root))
        print(json.dumps(json_ready(result.summary), ensure_ascii=False, indent=2))
    else:
        aggregate = write_score_table_signalcard_probe_packet(Path(args.root))
        print(json.dumps(json_ready(aggregate), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
