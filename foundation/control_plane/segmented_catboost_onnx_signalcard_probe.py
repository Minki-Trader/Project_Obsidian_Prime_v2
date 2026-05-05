from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np
import pandas as pd

from foundation.adapters.onnx_signal_adapter import OnnxSignalAdapter, summarize_signal_cards
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


RUN_ID = "run27H_segmented_catboost_onnx_signalcard_probe_v1"
PACKET_ID = "stage33_run27H_segmented_catboost_onnx_signalcard_probe_v1"
BOUNDARY = "segmented_catboost_onnx_signalcard_probe_only_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority"
SELECTED_CANDIDATE_ID = "stage18_run12G_catboost_probability_calibration_probe_v1"
SELECTED_SOURCE_STAGE_ID = "18_model_family_challenge__catboost_ordered_boosting_scout"
SELECTED_SOURCE_RUN_ID = "run12G_catboost_probability_calibration_probe_v1"
PARITY_TOLERANCE = 1.0e-5
METADATA_COLUMNS = {"bar_time_server", "timestamp_utc", "split", "row_index", "partial_context_subtype", "route_role"}


def configure_segmented_catboost_onnx_probe(
    *,
    run_id: str,
    packet_id: str,
    boundary: str,
    selected_candidate_id: str,
    selected_source_run_id: str,
) -> None:
    global RUN_ID, PACKET_ID, BOUNDARY, SELECTED_CANDIDATE_ID, SELECTED_SOURCE_RUN_ID
    RUN_ID = run_id
    PACKET_ID = packet_id
    BOUNDARY = boundary
    SELECTED_CANDIDATE_ID = selected_candidate_id
    SELECTED_SOURCE_RUN_ID = selected_source_run_id


def current_segmented_catboost_onnx_probe_config() -> dict[str, str]:
    return {
        "run_id": RUN_ID,
        "packet_id": PACKET_ID,
        "boundary": BOUNDARY,
        "selected_candidate_id": SELECTED_CANDIDATE_ID,
        "selected_source_run_id": SELECTED_SOURCE_RUN_ID,
    }


@dataclass(frozen=True)
class SegmentedCatBoostOnnxProbeResult:
    summary: dict[str, Any]
    adapter_contract: dict[str, Any]
    parity_report: dict[str, Any]
    signalcard_summary: dict[str, Any]
    model_pack_manifest: dict[str, Any]
    stage_rows: list[dict[str, Any]]
    run_registry_row: dict[str, Any]
    artifact_rows: list[dict[str, Any]]


def build_segmented_catboost_onnx_signalcard_probe(root: Path | str = Path(".")) -> SegmentedCatBoostOnnxProbeResult:
    root_path = Path(root)
    selected = _selected_candidate(root_path)
    source_run_root = root_path / str(selected["source_path"])
    source_manifest = _read_json(source_run_root / "run_manifest.json")
    source_summary = _read_json(source_run_root / "summary.json")
    assets = _candidate_assets(root_path, source_run_root, source_manifest)

    contract_segments: dict[str, Any] = {}
    report_segments: dict[str, Any] = {}
    signal_segments: dict[str, Any] = {}
    sample_segments: dict[str, Any] = {}
    for segment_key, segment_assets in assets["segments"].items():
        contract_segments[segment_key] = {
            "segment_id": segment_assets["segment_id"],
            "runtime_split": segment_assets["runtime_split"],
            "source_split": segment_assets["source_split"],
            "segment_filter": segment_assets["segment_filter"],
            "tiers": {},
        }
        report_segments[segment_key] = {"tiers": {}}
        signal_segments[segment_key] = {"tiers": {}}
        sample_segments[segment_key] = {"tiers": {}}
        for tier_name, tier_assets in segment_assets["tiers"].items():
            adapter = OnnxSignalAdapter(
                adapter_id=f"{selected['candidate_id']}__{segment_key}__{tier_name}_onnx_signalcard",
                source_stage_id=str(selected["stage_id"]),
                source_run_id=str(selected["run_id"]),
                mechanism_class=str(selected["mechanism_class"]),
                roles=tuple(role for role in selected["roles"] if role != "Deferred"),
                feature_names=tuple(tier_assets["feature_names"]),
                source_model_path=root_path / str(tier_assets["source_model_path"]),
                onnx_model_path=root_path / str(tier_assets["onnx_model_path"]),
                nonflat_threshold=float(tier_assets["threshold"]),
                tier_scope=str(tier_assets["tier_scope"]),
                claim_boundary=BOUNDARY,
            )
            frame = pd.read_csv(io_path(root_path / str(tier_assets["feature_matrix"])))
            values = frame.loc[:, list(tier_assets["feature_names"])].to_numpy(dtype="float64", copy=False)
            parity = adapter.parity_report(values, tolerance=PARITY_TOLERANCE)
            source_prob = adapter.source_probabilities(values)
            onnx_prob = adapter.onnx_probabilities(values)
            source_cards = adapter.signal_cards(source_prob, row_ids=_row_ids(frame))
            onnx_cards = adapter.signal_cards(onnx_prob, row_ids=_row_ids(frame))
            direction_mismatches = sum(1 for left, right in zip(source_cards, onnx_cards) if left.direction != right.direction)
            report_segments[segment_key]["tiers"][tier_name] = {
                **parity,
                "source_vs_onnx_signal_direction_mismatches": direction_mismatches,
                "source_vs_onnx_signal_direction_mismatch_rate": float(direction_mismatches / len(onnx_cards))
                if onnx_cards
                else 0.0,
                "feature_matrix": str(tier_assets["feature_matrix"]),
                "feature_matrix_sha256": sha256_file_lf_normalized(root_path / str(tier_assets["feature_matrix"])),
                "segment_id": segment_assets["segment_id"],
                "runtime_split": segment_assets["runtime_split"],
                "threshold": float(tier_assets["threshold"]),
                "max_abs_probability_diff_full_matrix": float(np.max(np.abs(source_prob - onnx_prob))) if len(source_prob) else 0.0,
                "mean_abs_probability_diff_full_matrix": float(np.mean(np.abs(source_prob - onnx_prob))) if len(source_prob) else 0.0,
            }
            signal_segments[segment_key]["tiers"][tier_name] = {
                "source": summarize_signal_cards(source_cards),
                "onnx": summarize_signal_cards(onnx_cards),
            }
            sample_segments[segment_key]["tiers"][tier_name] = [card.to_dict() for card in onnx_cards[:10]]
            contract_segments[segment_key]["tiers"][tier_name] = {
                "candidate_contract": adapter.candidate_contract().to_dict(),
                "source_model": _artifact_identity(root_path, root_path / str(tier_assets["source_model_path"])),
                "onnx_model": _artifact_identity(root_path, root_path / str(tier_assets["onnx_model_path"])),
                "feature_matrix": _artifact_identity_lf(root_path, root_path / str(tier_assets["feature_matrix"])),
                "feature_order_hash": ordered_hash(tuple(tier_assets["feature_names"])),
                "nonflat_threshold": float(tier_assets["threshold"]),
            }

    adapter_contract = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "selected_candidate": selected,
        "contract_family": "SignalCard/SegmentedCatBoostOnnxSignalAdapter",
        "segments": contract_segments,
        "output_contract": {"output_type": "SignalCard.v1", "safe_fallback": "no_trade"},
        "claim_boundary": BOUNDARY,
    }
    parity_report = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "selected_candidate_id": selected["candidate_id"],
        "passed": _all_parity_passed(report_segments),
        "segments": report_segments,
        "source_runtime_probe": _source_runtime_probe_summary(source_manifest, source_summary),
        "claim_boundary": BOUNDARY,
    }
    signalcard_summary = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "selected_candidate_id": selected["candidate_id"],
        "segments": signal_segments,
        "samples": sample_segments,
        "claim_boundary": BOUNDARY,
    }
    model_pack_manifest = _model_pack_manifest(root_path, selected, adapter_contract, parity_report, assets, source_manifest)
    summary = _summary(selected, parity_report, signalcard_summary, model_pack_manifest, source_manifest, source_summary)
    return SegmentedCatBoostOnnxProbeResult(
        summary=summary,
        adapter_contract=adapter_contract,
        parity_report=parity_report,
        signalcard_summary=signalcard_summary,
        model_pack_manifest=model_pack_manifest,
        stage_rows=_stage_ledger_rows(summary),
        run_registry_row=_run_registry_row(summary),
        artifact_rows=_artifact_rows(),
    )


def write_segmented_catboost_onnx_signalcard_probe_packet(
    root: Path | str = Path("."),
    *,
    generated_at_utc: str | None = None,
) -> dict[str, Any]:
    root_path = Path(root)
    generated_at = generated_at_utc or datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    result = build_segmented_catboost_onnx_signalcard_probe(root_path)
    run_root = root_path / "stages" / STAGE_ID / "02_runs" / RUN_ID
    reports_root = run_root / "reports"
    model_pack_root = run_root / "model_pack"
    packet_root = root_path / "docs/agent_control/packets" / PACKET_ID
    io_path(reports_root).mkdir(parents=True, exist_ok=True)
    io_path(model_pack_root).mkdir(parents=True, exist_ok=True)
    io_path(packet_root).mkdir(parents=True, exist_ok=True)

    adapter_contract_path = run_root / "adapter_contract.json"
    parity_report_path = run_root / "segmented_onnx_parity_report.json"
    signalcard_summary_path = run_root / "signalcard_summary.json"
    model_pack_manifest_path = model_pack_root / "model_pack_manifest.json"
    manifest_path = run_root / "run_manifest.json"
    result_summary_path = reports_root / "result_summary.md"
    aggregate_summary_path = packet_root / "aggregate_summary.json"

    _write_json(adapter_contract_path, {"generated_at_utc": generated_at, **result.adapter_contract})
    _write_json(parity_report_path, {"generated_at_utc": generated_at, **result.parity_report})
    _write_json(signalcard_summary_path, {"generated_at_utc": generated_at, **result.signalcard_summary})
    _write_json(model_pack_manifest_path, {"generated_at_utc": generated_at, **result.model_pack_manifest})
    manifest = _manifest(
        root_path,
        generated_at,
        adapter_contract_path,
        parity_report_path,
        signalcard_summary_path,
        model_pack_manifest_path,
        result,
    )
    _write_json(manifest_path, manifest)
    _write_markdown(result_summary_path, _result_summary_markdown(generated_at, result))
    aggregate = {
        "packet_id": PACKET_ID,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "source_run_id": SOURCE_RUN_ID,
        "status": "reviewed_segmented_catboost_onnx_signalcard_probe_completed"
        if result.summary["parity_passed"] and result.summary["signal_direction_mismatches"] == 0
        else "blocked_segmented_catboost_onnx_signalcard_probe",
        "judgment": result.summary["judgment"],
        "boundary": BOUNDARY,
        "generated_at_utc": generated_at,
        "adapter_contract_path": _rel(root_path, adapter_contract_path),
        "parity_report_path": _rel(root_path, parity_report_path),
        "signalcard_summary_path": _rel(root_path, signalcard_summary_path),
        "model_pack_manifest_path": _rel(root_path, model_pack_manifest_path),
        "run_manifest_path": _rel(root_path, manifest_path),
        "result_summary_path": _rel(root_path, result_summary_path),
        "selected_candidate": result.summary["selected_candidate"],
        "parity_passed": result.summary["parity_passed"],
        "signal_direction_mismatches": result.summary["signal_direction_mismatches"],
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
    result = build_adapter_feasibility_matrix(root)
    for row in result.matrix_rows:
        if row["candidate_id"] == SELECTED_CANDIDATE_ID:
            return dict(row)
    raise RuntimeError(f"Missing selected candidate in run27E feasibility matrix: {SELECTED_CANDIDATE_ID}")


def _candidate_assets(root: Path, source_run_root: Path, source_manifest: Mapping[str, Any]) -> dict[str, Any]:
    artifacts = dict(source_manifest["model_artifacts"])
    segments: dict[str, Any] = {}
    for threshold in artifacts["segment_thresholds"]:
        segment_id = str(threshold["segment_id"])
        runtime_split = str(threshold["runtime_split"])
        segment_key = f"{segment_id}_{runtime_split}"
        segments[segment_key] = {
            "segment_id": segment_id,
            "runtime_split": runtime_split,
            "source_split": threshold.get("source_split"),
            "segment_filter": threshold.get("segment_filter"),
            "segment_label": threshold.get("segment_label"),
            "tiers": {
                "tier_a": _tier_assets(
                    root,
                    source_run_root,
                    artifacts,
                    segment_id,
                    runtime_split,
                    tier_name="tier_a",
                    matrix_key=str(threshold["tier_a_matrix_key"]),
                    threshold=float(threshold["tier_a_threshold"]),
                ),
                "tier_b": _tier_assets(
                    root,
                    source_run_root,
                    artifacts,
                    segment_id,
                    runtime_split,
                    tier_name="tier_b",
                    matrix_key=str(threshold["tier_b_matrix_key"]),
                    threshold=float(threshold["tier_b_threshold"]),
                ),
            },
        }
    return {"source_run_root": source_run_root, "segments": segments}


def _tier_assets(
    root: Path,
    source_run_root: Path,
    artifacts: Mapping[str, Any],
    segment_id: str,
    runtime_split: str,
    *,
    tier_name: str,
    matrix_key: str,
    threshold: float,
) -> dict[str, Any]:
    prefix = "tier_a" if tier_name == "tier_a" else "tier_b"
    matrix_path = source_run_root / "features" / segment_id / f"{prefix}_{segment_id}_{runtime_split}_feature_matrix.csv"
    columns = pd.read_csv(io_path(matrix_path), nrows=0).columns
    feature_names = tuple(column for column in columns if column not in METADATA_COLUMNS)
    return {
        "tier_scope": "Tier A" if tier_name == "tier_a" else "Tier B fallback",
        "feature_names": feature_names,
        "feature_matrix": _rel(root, matrix_path),
        "feature_matrix_key": matrix_key,
        "source_model_path": _rel(root, _resolve_path(root, artifacts[f"{tier_name}_joblib"]["path"])),
        "onnx_model_path": _rel(root, _resolve_path(root, artifacts[f"{tier_name}_onnx"]["path"])),
        "threshold": threshold,
    }


def _summary(
    selected: Mapping[str, Any],
    parity_report: Mapping[str, Any],
    signalcard_summary: Mapping[str, Any],
    model_pack_manifest: Mapping[str, Any],
    source_manifest: Mapping[str, Any],
    source_summary: Mapping[str, Any],
) -> dict[str, Any]:
    tier_reports = [
        tier_payload
        for segment_payload in parity_report["segments"].values()
        for tier_payload in segment_payload["tiers"].values()
    ]
    rows = sum(int(report["rows"]) for report in tier_reports)
    mismatches = sum(int(report["source_vs_onnx_signal_direction_mismatches"]) for report in tier_reports)
    max_abs_diff = max(float(report["max_abs_diff"]) for report in tier_reports) if tier_reports else 0.0
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "source_run_id": SOURCE_RUN_ID,
        "selected_candidate": dict(selected),
        "judgment": "inconclusive_segmented_catboost_onnx_signalcard_probe_completed",
        "parity_passed": bool(parity_report["passed"]),
        "parity_rows": rows,
        "parity_max_abs_diff": max_abs_diff,
        "parity_tolerance": PARITY_TOLERANCE,
        "signal_direction_mismatches": mismatches,
        "segment_count": len(parity_report["segments"]),
        "tier_view_count": len(tier_reports),
        "source_mt5_external_verification_status": source_manifest.get("external_verification_status")
        or source_summary.get("external_verification_status"),
        "model_pack_manifest_id": model_pack_manifest["model_pack_id"],
        "onnx_readiness_decision": "existing_segmented_catboost_onnx_packaged_manifest_only_no_new_export",
        "runtime_handoff_decision": f"existing_stage18_mt5_runtime_probe_referenced_not_identity_audited_for_{RUN_ID.lower()}",
        "claim_boundary": BOUNDARY,
        "signalcard_counts": _signalcard_counts(signalcard_summary),
        "required_gates": {
            "why_this_work": "completed",
            "evidence_gap": "completed",
            "input_data_features_split_run_id": "completed",
            "artifact_paths": "completed",
            "validation_oos_wfo_mt5_results": f"completed_by_existing_stage18_{SELECTED_SOURCE_RUN_ID}_evidence_reference",
            "failure_or_defer_reason": "new_onnx_export_deferred_existing_onnx_sufficient_for_probe",
            "claim_boundary": BOUNDARY,
            "next_action_or_stop_rule": "stage18_segmented_mt5_handoff_identity_audit_or_stage33_closeout",
        },
    }


def _model_pack_manifest(
    root: Path,
    selected: Mapping[str, Any],
    adapter_contract: Mapping[str, Any],
    parity_report: Mapping[str, Any],
    assets: Mapping[str, Any],
    source_manifest: Mapping[str, Any],
) -> dict[str, Any]:
    segments: dict[str, Any] = {}
    for segment_key, segment_payload in assets["segments"].items():
        segments[segment_key] = {
            "segment_id": segment_payload["segment_id"],
            "runtime_split": segment_payload["runtime_split"],
            "source_split": segment_payload["source_split"],
            "segment_filter": segment_payload["segment_filter"],
            "tiers": {},
        }
        for tier_name, tier_assets in segment_payload["tiers"].items():
            source_model_path = root / str(tier_assets["source_model_path"])
            onnx_model_path = root / str(tier_assets["onnx_model_path"])
            matrix_path = root / str(tier_assets["feature_matrix"])
            segments[segment_key]["tiers"][tier_name] = {
                "tier_scope": tier_assets["tier_scope"],
                "feature_count": len(tier_assets["feature_names"]),
                "feature_names": list(tier_assets["feature_names"]),
                "feature_order_hash": ordered_hash(tuple(tier_assets["feature_names"])),
                "nonflat_threshold": float(tier_assets["threshold"]),
                "source_model": {"path": str(tier_assets["source_model_path"]), "sha256": sha256_file(source_model_path)},
                "onnx_model": {"path": str(tier_assets["onnx_model_path"]), "sha256": sha256_file(onnx_model_path)},
                "feature_matrix": {
                    "path": str(tier_assets["feature_matrix"]),
                    "sha256_lf_normalized": sha256_file_lf_normalized(matrix_path),
                },
                "python_vs_onnx_parity": parity_report["segments"][segment_key]["tiers"][tier_name],
            }
    return {
        "model_pack_id": f"{RUN_ID}__{selected['candidate_id']}__segmented_catboost_onnx_manifest",
        "selected_candidate_id": selected["candidate_id"],
        "source_stage_id": selected["stage_id"],
        "source_run_id": selected["run_id"],
        "contract_family": adapter_contract["contract_family"],
        "packaging_policy": "manifest_only_existing_segmented_catboost_onnx_artifacts_no_reexport",
        "source_runtime_probe_external_verification_status": source_manifest.get("external_verification_status"),
        "parity_passed": parity_report["passed"],
        "segments": segments,
        "claim_boundary": BOUNDARY,
    }


def _source_runtime_probe_summary(source_manifest: Mapping[str, Any], source_summary: Mapping[str, Any]) -> dict[str, Any]:
    runtime_probe = dict(source_manifest.get("runtime_probe") or {})
    return {
        "source_run_id": source_manifest.get("run_id"),
        "source_stage_id": source_manifest.get("stage_id"),
        "external_verification_status": source_summary.get("external_verification_status"),
        "judgment": source_summary.get("judgment"),
        "attempt_count": len(runtime_probe.get("attempts") or []),
        "segment_threshold_count": len((source_manifest.get("model_artifacts") or {}).get("segment_thresholds") or []),
    }


def _all_parity_passed(segment_reports: Mapping[str, Mapping[str, Any]]) -> bool:
    return all(
        bool(tier_report["passed"])
        for segment_report in segment_reports.values()
        for tier_report in segment_report["tiers"].values()
    )


def _signalcard_counts(signalcard_summary: Mapping[str, Any]) -> dict[str, Any]:
    counts: dict[str, int] = {}
    for segment_payload in signalcard_summary["segments"].values():
        for tier_payload in segment_payload["tiers"].values():
            for direction, count in tier_payload["onnx"]["direction_counts"].items():
                counts[direction] = counts.get(direction, 0) + int(count)
    return dict(sorted(counts.items()))


def _stage_ledger_rows(summary: Mapping[str, Any]) -> list[dict[str, Any]]:
    run_root = f"stages/{STAGE_ID}/02_runs/{RUN_ID}"
    return [
        {
            "ledger_row_id": f"{RUN_ID}__adapter_contract",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "adapter_contract",
            "parent_run_id": RUN_ID,
            "record_view": "SegmentedCatBoost_ONNX_SignalCard_adapter_contract",
            "tier_scope": "Tier A+B segmented",
            "kpi_scope": "adapter_contract",
            "scoreboard_lane": "runtime_parity",
            "status": "completed",
            "judgment": summary["judgment"],
            "path": f"{run_root}/adapter_contract.json",
            "primary_kpi": ledger_pairs((("parity_rows", summary["parity_rows"]), ("segment_count", summary["segment_count"]))),
            "guardrail_kpi": "safe_fallback=no_trade;segment_thresholds_fixed=true",
            "external_verification_status": "referenced_existing_completed",
            "notes": "Segmented CatBoost ONNX artifacts are wrapped in SignalCard adapter contracts; no alpha quality or promotion claim.",
        },
        {
            "ledger_row_id": f"{RUN_ID}__python_vs_onnx_parity",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "python_vs_onnx_parity",
            "parent_run_id": RUN_ID,
            "record_view": "segmented_catboost_python_vs_onnx_signalcard_parity",
            "tier_scope": "Tier A+B segmented",
            "kpi_scope": "runtime_parity",
            "scoreboard_lane": "runtime_parity",
            "status": "completed" if summary["parity_passed"] and summary["signal_direction_mismatches"] == 0 else "blocked",
            "judgment": summary["onnx_readiness_decision"],
            "path": f"{run_root}/segmented_onnx_parity_report.json",
            "primary_kpi": ledger_pairs(
                (
                    ("parity_rows", summary["parity_rows"]),
                    ("max_abs_diff", summary["parity_max_abs_diff"]),
                    ("direction_mismatches", summary["signal_direction_mismatches"]),
                )
            ),
            "guardrail_kpi": f"tolerance={PARITY_TOLERANCE};direction_parity_required=true",
            "external_verification_status": "referenced_existing_completed",
            "notes": "Segmented CatBoost source model and ONNX probabilities are compared on validation/OOS segment matrices.",
        },
        {
            "ledger_row_id": f"{RUN_ID}__model_pack_manifest",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "model_pack_manifest",
            "parent_run_id": RUN_ID,
            "record_view": "existing_segmented_catboost_onnx_model_pack",
            "tier_scope": "Tier A+B segmented",
            "kpi_scope": "runtime_packaging_gate",
            "scoreboard_lane": "runtime_parity",
            "status": "completed",
            "judgment": summary["onnx_readiness_decision"],
            "path": f"{run_root}/model_pack/model_pack_manifest.json",
            "primary_kpi": ledger_pairs((("onnx_artifact_generated", 0), ("model_pack_manifest_generated", 1))),
            "guardrail_kpi": "manifest_only_no_reexport;mt5_handoff_identity_audit_still_required",
            "external_verification_status": "referenced_existing_completed",
            "notes": "Model pack records existing segmented CatBoost ONNX paths, thresholds, feature matrices, and hashes.",
        },
    ]


def _run_registry_row(summary: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "segmented_catboost_onnx_signalcard_probe",
        "status": "reviewed",
        "judgment": summary["judgment"],
        "path": f"stages/{STAGE_ID}/02_runs/{RUN_ID}",
        "notes": ledger_pairs(
            (
                ("selected_candidate", summary["selected_candidate"]["candidate_id"]),
                ("parity_passed", summary["parity_passed"]),
                ("parity_rows", summary["parity_rows"]),
                ("direction_mismatches", summary["signal_direction_mismatches"]),
                ("boundary", BOUNDARY),
            )
        ),
    }


def _artifact_rows() -> list[dict[str, Any]]:
    run_root = f"stages/{STAGE_ID}/02_runs/{RUN_ID}"
    return [
        {
            "artifact_id": f"{RUN_ID}__adapter_contract",
            "type": "SegmentedCatBoost_ONNX_SignalCard_adapter_contract",
            "path": f"{run_root}/adapter_contract.json",
            "status": "tracked_reviewed",
            "notes": "SignalCard adapter contract for the selected Stage18 segmented CatBoost ONNX candidate.",
        },
        {
            "artifact_id": f"{RUN_ID}__parity_report",
            "type": "segmented_catboost_python_vs_onnx_parity_report",
            "path": f"{run_root}/segmented_onnx_parity_report.json",
            "status": "tracked_reviewed",
            "notes": "Segmented source model vs ONNX probability and SignalCard direction parity.",
        },
        {
            "artifact_id": f"{RUN_ID}__signalcard_summary",
            "type": "SignalCard_output_summary",
            "path": f"{run_root}/signalcard_summary.json",
            "status": "tracked_reviewed",
            "notes": "SignalCard direction, score, confidence summaries and samples across segments.",
        },
        {
            "artifact_id": f"{RUN_ID}__model_pack_manifest",
            "type": "existing_segmented_catboost_onnx_model_pack_manifest",
            "path": f"{run_root}/model_pack/model_pack_manifest.json",
            "status": "tracked_reviewed",
            "notes": "Manifest-only model pack that references existing segmented CatBoost ONNX artifacts and hashes.",
        },
    ]


def _manifest(
    root: Path,
    generated_at: str,
    adapter_contract_path: Path,
    parity_report_path: Path,
    signalcard_summary_path: Path,
    model_pack_manifest_path: Path,
    result: SegmentedCatBoostOnnxProbeResult,
) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "packet_id": PACKET_ID,
        "source_run_id": SOURCE_RUN_ID,
        "generated_at_utc": generated_at,
        "producer": "foundation.control_plane.segmented_catboost_onnx_signalcard_probe",
        "outputs": {
            "adapter_contract": {"path": _rel(root, adapter_contract_path), "sha256": sha256_file_lf_normalized(adapter_contract_path)},
            "segmented_onnx_parity_report": {"path": _rel(root, parity_report_path), "sha256": sha256_file_lf_normalized(parity_report_path)},
            "signalcard_summary": {"path": _rel(root, signalcard_summary_path), "sha256": sha256_file_lf_normalized(signalcard_summary_path)},
            "model_pack_manifest": {
                "path": _rel(root, model_pack_manifest_path),
                "sha256": sha256_file_lf_normalized(model_pack_manifest_path),
            },
        },
        "selected_candidate": result.summary["selected_candidate"],
        "claim_boundary": BOUNDARY,
    }


def _result_summary_markdown(generated_at: str, result: SegmentedCatBoostOnnxProbeResult) -> str:
    summary = result.summary
    selected = summary["selected_candidate"]
    lines = [
        f"# Stage33 {RUN_ID} Segmented CatBoost ONNX SignalCard Probe(33단계 {RUN_ID} 분할 캣부스트 온닉스 신호 카드 탐침)",
        "",
        f"- generated_at_utc(생성 시각 UTC): `{generated_at}`",
        f"- run_id(실행 ID): `{RUN_ID}`",
        f"- selected candidate(선택 후보): `{selected['candidate_id']}`",
        f"- parity rows(동등성 행): `{summary['parity_rows']}`",
        f"- parity passed(동등성 통과): `{summary['parity_passed']}`",
        f"- max abs diff(최대 절대 차이): `{summary['parity_max_abs_diff']}`",
        f"- signal direction mismatches(신호 방향 불일치): `{summary['signal_direction_mismatches']}`",
        f"- ONNX readiness decision(온닉스 준비도 결정): `{summary['onnx_readiness_decision']}`",
        "",
        f"효과(effect, 효과): {RUN_ID}({RUN_ID} 실행)는 {selected['candidate_id']}(선택 후보)의 segmented CatBoost ONNX artifacts(분할 캣부스트 온닉스 산출물)를 SignalCard adapter(신호 카드 어댑터)로 감싸고 Python source model(파이썬 원천 모델)과 ONNX runtime(온닉스 런타임)을 비교한다.",
        "",
        "## Explicit Non-Claims(명시 비주장)",
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
    return [str(index) for index in range(len(frame))]


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def _resolve_path(root: Path, value: Any) -> Path:
    path = Path(str(value))
    return path if path.is_absolute() else root / path


def _artifact_identity(root: Path, path: Path) -> dict[str, Any]:
    return {"path": _rel(root, path), "sha256": sha256_file(path)}


def _artifact_identity_lf(root: Path, path: Path) -> dict[str, Any]:
    return {"path": _rel(root, path), "sha256_lf_normalized": sha256_file_lf_normalized(path)}


def _write_json(path: Path, payload: Mapping[str, Any]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _write_markdown(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text, encoding="utf-8-sig")


def _upsert_registers(root: Path, result: SegmentedCatBoostOnnxProbeResult) -> None:
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
    parser = argparse.ArgumentParser(description="Run Stage33 segmented CatBoost ONNX SignalCard adapter probe.")
    parser.add_argument("--root", default=".")
    parser.add_argument("--summary-only", action="store_true")
    args = parser.parse_args(argv)
    if args.summary_only:
        result = build_segmented_catboost_onnx_signalcard_probe(Path(args.root))
        print(json.dumps(json_ready(result.summary), ensure_ascii=False, indent=2))
    else:
        aggregate = write_segmented_catboost_onnx_signalcard_probe_packet(Path(args.root))
        print(json.dumps(json_ready(aggregate), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
