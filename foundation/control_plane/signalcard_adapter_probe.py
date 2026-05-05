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
from foundation.control_plane.adapter_probe_shortlist import RUN_ID as SOURCE_RUN_ID
from foundation.control_plane.adapter_probe_shortlist import build_adapter_probe_shortlist
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


RUN_ID = "run27C_signalcard_adapter_contract_probe_v1"
PACKET_ID = "stage33_run27C_signalcard_adapter_contract_probe_v1"
BOUNDARY = "signalcard_adapter_probe_only_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority"


@dataclass(frozen=True)
class SignalCardProbeResult:
    summary: dict[str, Any]
    adapter_contract: dict[str, Any]
    parity_report: dict[str, Any]
    signalcard_summary: dict[str, Any]
    model_pack_manifest: dict[str, Any]
    stage_rows: list[dict[str, Any]]
    run_registry_row: dict[str, Any]
    artifact_rows: list[dict[str, Any]]


def build_signalcard_adapter_probe(root: Path | str = Path(".")) -> SignalCardProbeResult:
    root_path = Path(root)
    shortlist = build_adapter_probe_shortlist(root_path).shortlist
    if not shortlist:
        raise RuntimeError("run27C requires at least one run27B shortlisted adapter candidate.")
    selected = dict(shortlist[0])
    source_run_root = root_path / str(selected["source_path"])
    assets = _candidate_assets(root_path, source_run_root)
    tier_reports: dict[str, Any] = {}
    tier_contracts: dict[str, Any] = {}
    tier_signal_summaries: dict[str, Any] = {}
    signal_samples: dict[str, Any] = {}
    for tier_name, tier_assets in assets["tiers"].items():
        feature_names = tuple(tier_assets["feature_names"])
        adapter = OnnxSignalAdapter(
            adapter_id=f"{selected['candidate_id']}__{tier_name}_onnx_signalcard",
            source_stage_id=str(selected["stage_id"]),
            source_run_id=str(selected["run_id"]),
            mechanism_class=str(selected["mechanism_class"]),
            roles=tuple(selected["roles"]),
            feature_names=feature_names,
            source_model_path=root_path / tier_assets["source_model_path"],
            onnx_model_path=root_path / tier_assets["onnx_model_path"],
            nonflat_threshold=float(tier_assets["threshold"]),
            tier_scope=str(tier_assets["tier_scope"]),
            claim_boundary=BOUNDARY,
        )
        tier_contracts[tier_name] = {
            "candidate_contract": adapter.candidate_contract().to_dict(),
            "source_model": _artifact_identity(root_path, root_path / tier_assets["source_model_path"]),
            "onnx_model": _artifact_identity(root_path, root_path / tier_assets["onnx_model_path"]),
            "feature_order_hash": ordered_hash(feature_names),
            "nonflat_threshold": float(tier_assets["threshold"]),
        }
        split_reports: dict[str, Any] = {}
        split_summaries: dict[str, Any] = {}
        tier_samples: dict[str, Any] = {}
        for split_name, matrix_path in tier_assets["feature_matrices"].items():
            frame = pd.read_csv(io_path(root_path / matrix_path))
            values = frame.loc[:, list(feature_names)].to_numpy(dtype="float64", copy=False)
            parity = adapter.parity_report(values, tolerance=1e-5)
            source_prob = adapter.source_probabilities(values)
            onnx_prob = adapter.onnx_probabilities(values)
            source_cards = adapter.signal_cards(source_prob, row_ids=_row_ids(frame))
            onnx_cards = adapter.signal_cards(onnx_prob, row_ids=_row_ids(frame))
            direction_mismatches = sum(1 for left, right in zip(source_cards, onnx_cards) if left.direction != right.direction)
            split_reports[split_name] = {
                **parity,
                "source_vs_onnx_signal_direction_mismatches": direction_mismatches,
                "source_vs_onnx_signal_direction_mismatch_rate": float(direction_mismatches / len(source_cards)) if source_cards else 0.0,
                "max_abs_probability_diff_full_matrix": float(np.max(np.abs(source_prob - onnx_prob))) if len(source_prob) else 0.0,
                "mean_abs_probability_diff_full_matrix": float(np.mean(np.abs(source_prob - onnx_prob))) if len(source_prob) else 0.0,
                "feature_matrix": matrix_path.as_posix(),
                "feature_matrix_sha256": sha256_file_lf_normalized(root_path / matrix_path),
            }
            split_summaries[split_name] = {
                "source": summarize_signal_cards(source_cards),
                "onnx": summarize_signal_cards(onnx_cards),
            }
            tier_samples[split_name] = [card.to_dict() for card in onnx_cards[:10]]
        tier_reports[tier_name] = split_reports
        tier_signal_summaries[tier_name] = split_summaries
        signal_samples[tier_name] = tier_samples

    adapter_contract = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "selected_candidate": selected,
        "contract_family": "SignalCard/OnnxSignalAdapter",
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
    model_pack_manifest = _model_pack_manifest(root_path, selected, adapter_contract, parity_report, assets)
    summary = _summary(selected, parity_report, signalcard_summary, model_pack_manifest)
    return SignalCardProbeResult(
        summary=summary,
        adapter_contract=adapter_contract,
        parity_report=parity_report,
        signalcard_summary=signalcard_summary,
        model_pack_manifest=model_pack_manifest,
        stage_rows=_stage_ledger_rows(summary),
        run_registry_row=_run_registry_row(summary),
        artifact_rows=_artifact_rows(),
    )


def write_signalcard_adapter_probe_packet(root: Path | str = Path("."), *, generated_at_utc: str | None = None) -> dict[str, Any]:
    root_path = Path(root)
    generated_at = generated_at_utc or datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    result = build_signalcard_adapter_probe(root_path)
    run_root = root_path / "stages" / STAGE_ID / "02_runs" / RUN_ID
    reports_root = run_root / "reports"
    model_pack_root = run_root / "model_pack"
    packet_root = root_path / "docs/agent_control/packets" / PACKET_ID
    io_path(reports_root).mkdir(parents=True, exist_ok=True)
    io_path(model_pack_root).mkdir(parents=True, exist_ok=True)
    io_path(packet_root).mkdir(parents=True, exist_ok=True)

    adapter_contract_path = run_root / "adapter_contract.json"
    parity_report_path = run_root / "parity_report.json"
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
        "status": "reviewed_signalcard_adapter_probe_completed",
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


def _candidate_assets(root: Path, source_run_root: Path) -> dict[str, Any]:
    summary = json.loads(io_path(source_run_root / "summary.json").read_text(encoding="utf-8-sig"))
    thresholds = summary.get("thresholds", {})
    models_root = source_run_root / "models"
    mt5_root = source_run_root / "mt5"
    tier_a_feature_order = _read_feature_order(models_root / "tier_a_feature_order.txt")
    tier_b_feature_order = _read_feature_order(models_root / "tier_b_core42_feature_order.txt")
    return {
        "summary_path": source_run_root / "summary.json",
        "thresholds": thresholds,
        "tiers": {
            "tier_a": {
                "tier_scope": "Tier A",
                "feature_names": tier_a_feature_order,
                "source_model_path": _rel(root, source_run_root / "models/tier_a_v13_model.joblib"),
                "onnx_model_path": _rel(root, source_run_root / "models/tier_a_v13_model.onnx"),
                "threshold": float(thresholds["tier_a"]),
                "feature_matrices": {
                    "validation": _rel(root, mt5_root / "tier_a_validation_is_feature_matrix.csv"),
                    "oos": _rel(root, mt5_root / "tier_a_oos_feature_matrix.csv"),
                },
            },
            "tier_b": {
                "tier_scope": "Tier B fallback",
                "feature_names": tier_b_feature_order,
                "source_model_path": _rel(root, source_run_root / "models/tier_b_v13_core42_model.joblib"),
                "onnx_model_path": _rel(root, source_run_root / "models/tier_b_v13_core42_model.onnx"),
                "threshold": float(thresholds["tier_b"]),
                "feature_matrices": {
                    "validation": _rel(root, mt5_root / "tier_b_validation_is_feature_matrix.csv"),
                    "oos": _rel(root, mt5_root / "tier_b_oos_feature_matrix.csv"),
                },
            },
        },
    }


def _read_feature_order(path: Path) -> list[str]:
    lines = io_path(path).read_text(encoding="utf-8-sig").splitlines()
    names = [line.strip() for line in lines if line.strip()]
    if not names:
        raise RuntimeError(f"Feature order is empty: {path}")
    return names


def _row_ids(frame: pd.DataFrame) -> list[Any]:
    if "row_index" in frame.columns:
        return frame["row_index"].astype(str).tolist()
    return [str(index) for index in range(len(frame))]


def _all_parity_passed(tier_reports: Mapping[str, Mapping[str, Mapping[str, Any]]]) -> bool:
    return all(bool(report.get("passed")) for split_reports in tier_reports.values() for report in split_reports.values())


def _summary(
    selected: Mapping[str, Any],
    parity_report: Mapping[str, Any],
    signalcard_summary: Mapping[str, Any],
    model_pack_manifest: Mapping[str, Any],
) -> dict[str, Any]:
    parity_passed = bool(parity_report["passed"])
    direction_mismatches = sum(
        int(report.get("source_vs_onnx_signal_direction_mismatches") or 0)
        for split_reports in parity_report["tiers"].values()
        for report in split_reports.values()
    )
    rows = sum(
        int(report.get("rows") or 0)
        for split_reports in parity_report["tiers"].values()
        for report in split_reports.values()
    )
    return {
        "selected_candidate": {
            "candidate_id": selected["candidate_id"],
            "stage_id": selected["stage_id"],
            "run_id": selected["run_id"],
            "mechanism_class": selected["mechanism_class"],
            "roles": selected["roles"],
        },
        "parity_passed": parity_passed,
        "parity_rows": rows,
        "signal_direction_mismatches": direction_mismatches,
        "signal_direction_mismatch_rate": float(direction_mismatches / rows) if rows else None,
        "model_pack_manifest_id": model_pack_manifest["model_pack_id"],
        "onnx_readiness_decision": "adapter_probe_onnx_packaged_existing_artifacts_parity_passed"
        if parity_passed and direction_mismatches == 0
        else "defer_onnx_readiness_until_signalcard_parity_repairs",
        "judgment": "inconclusive_signalcard_adapter_probe_completed_existing_onnx_parity_passed"
        if parity_passed and direction_mismatches == 0
        else "blocked_signalcard_adapter_probe_parity_mismatch",
        "signalcard_summary": {
            tier: {
                split: values["onnx"]
                for split, values in split_values.items()
            }
            for tier, split_values in signalcard_summary["tiers"].items()
        },
        "required_gates": {
            "evidence_gate": "completed_run27B_shortlist_consumed",
            "adapter_readiness_gate": {
                "status": "completed",
                "input_contract": "fixed_feature_order_per_tier",
                "output_contract": "SignalCard.v1_safe_fallback_no_trade",
            },
            "python_vs_onnx_parity_check": {
                "status": "passed" if parity_passed and direction_mismatches == 0 else "blocked",
                "rows": rows,
                "signal_direction_mismatches": direction_mismatches,
            },
            "mt5_handoff_check": {
                "status": "referenced_existing_completed_mt5_probe",
                "source_run_id": selected["run_id"],
            },
            "claim_boundary": BOUNDARY,
        },
        "claim_boundary": BOUNDARY,
    }


def _model_pack_manifest(
    root: Path,
    selected: Mapping[str, Any],
    adapter_contract: Mapping[str, Any],
    parity_report: Mapping[str, Any],
    assets: Mapping[str, Any],
) -> dict[str, Any]:
    tier_payload: dict[str, Any] = {}
    for tier_name, tier_assets in assets["tiers"].items():
        tier_payload[tier_name] = {
            "tier_scope": tier_assets["tier_scope"],
            "feature_order_hash": ordered_hash(tier_assets["feature_names"]),
            "feature_count": len(tier_assets["feature_names"]),
            "source_model": _artifact_identity(root, root / tier_assets["source_model_path"]),
            "onnx_model": _artifact_identity(root, root / tier_assets["onnx_model_path"]),
            "nonflat_threshold": tier_assets["threshold"],
            "feature_matrices": {
                split: {
                    "path": path.as_posix(),
                    "sha256_lf_normalized": sha256_file_lf_normalized(root / path),
                }
                for split, path in tier_assets["feature_matrices"].items()
            },
        }
    return {
        "model_pack_id": f"{RUN_ID}__{selected['candidate_id']}__existing_onnx_signalcard_pack",
        "packaging_policy": "manifest_only_existing_onnx_artifacts_no_reexport",
        "selected_candidate": adapter_contract["selected_candidate"],
        "tiers": tier_payload,
        "parity_passed": parity_report["passed"],
        "runtime_handoff_reference": {
            "source_run_id": selected["run_id"],
            "source_path": selected["source_path"],
            "mt5_runtime_probe": "completed_existing_stage12_run03H_variant",
        },
        "claim_boundary": BOUNDARY,
    }


def _stage_ledger_rows(summary: Mapping[str, Any]) -> list[dict[str, Any]]:
    run_root = f"stages/{STAGE_ID}/02_runs/{RUN_ID}"
    return [
        {
            "ledger_row_id": f"{RUN_ID}__signalcard_adapter_contract",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "signalcard_adapter_contract",
            "parent_run_id": RUN_ID,
            "record_view": "SignalCard_adapter_contract",
            "tier_scope": "Tier A+B",
            "kpi_scope": "adapter_contract",
            "scoreboard_lane": "runtime_parity",
            "status": "completed",
            "judgment": summary["judgment"],
            "path": f"{run_root}/adapter_contract.json",
            "primary_kpi": ledger_pairs((("parity_rows", summary["parity_rows"]),)),
            "guardrail_kpi": "safe_fallback=no_trade;input_feature_order_fixed=true",
            "external_verification_status": "referenced_existing_completed",
            "notes": "SignalCard adapter contract wraps existing Stage12 ExtraTrees ONNX artifacts; no alpha quality or promotion claim.",
        },
        {
            "ledger_row_id": f"{RUN_ID}__python_vs_onnx_parity",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "python_vs_onnx_parity",
            "parent_run_id": RUN_ID,
            "record_view": "python_vs_onnx_signalcard_parity",
            "tier_scope": "Tier A+B",
            "kpi_scope": "runtime_parity",
            "scoreboard_lane": "runtime_parity",
            "status": "completed" if summary["parity_passed"] and summary["signal_direction_mismatches"] == 0 else "blocked",
            "judgment": summary["onnx_readiness_decision"],
            "path": f"{run_root}/parity_report.json",
            "primary_kpi": ledger_pairs(
                (
                    ("parity_rows", summary["parity_rows"]),
                    ("signal_direction_mismatches", summary["signal_direction_mismatches"]),
                )
            ),
            "guardrail_kpi": "tolerance=1e-5;direction_parity_required=true",
            "external_verification_status": "referenced_existing_completed",
            "notes": "ONNX readiness is limited to existing artifact packaging and SignalCard parity, not runtime authority.",
        },
        {
            "ledger_row_id": f"{RUN_ID}__model_pack_manifest",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "model_pack_manifest",
            "parent_run_id": RUN_ID,
            "record_view": "existing_onnx_signalcard_model_pack",
            "tier_scope": "Tier A+B",
            "kpi_scope": "runtime_packaging_gate",
            "scoreboard_lane": "runtime_parity",
            "status": "completed",
            "judgment": summary["onnx_readiness_decision"],
            "path": f"{run_root}/model_pack/model_pack_manifest.json",
            "primary_kpi": ledger_pairs((("onnx_artifact_generated", 0), ("model_pack_manifest_generated", 1))),
            "guardrail_kpi": "manifest_only_no_reexport;mt5_handoff_reference_existing",
            "external_verification_status": "referenced_existing_completed",
            "notes": "Model pack records existing ONNX paths and hashes; no new ONNX export in run27C.",
        },
    ]


def _run_registry_row(summary: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "signalcard_adapter_onnx_parity_probe",
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
            "type": "SignalCard_adapter_contract",
            "path": f"{run_root}/adapter_contract.json",
            "status": "tracked_reviewed",
            "notes": "SignalCard adapter contract for the selected run27B candidate.",
        },
        {
            "artifact_id": f"{RUN_ID}__parity_report",
            "type": "python_vs_onnx_parity_report",
            "path": f"{run_root}/parity_report.json",
            "status": "tracked_reviewed",
            "notes": "Python source model vs ONNX runtime probability and SignalCard direction parity.",
        },
        {
            "artifact_id": f"{RUN_ID}__signalcard_summary",
            "type": "SignalCard_output_summary",
            "path": f"{run_root}/signalcard_summary.json",
            "status": "tracked_reviewed",
            "notes": "SignalCard direction, score, confidence summaries and samples.",
        },
        {
            "artifact_id": f"{RUN_ID}__model_pack_manifest",
            "type": "existing_onnx_model_pack_manifest",
            "path": f"{run_root}/model_pack/model_pack_manifest.json",
            "status": "tracked_reviewed",
            "notes": "Manifest-only model pack that references existing ONNX artifacts and hashes.",
        },
    ]


def _manifest(
    root: Path,
    generated_at: str,
    adapter_contract_path: Path,
    parity_report_path: Path,
    signalcard_summary_path: Path,
    model_pack_manifest_path: Path,
    result: SignalCardProbeResult,
) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "packet_id": PACKET_ID,
        "source_run_id": SOURCE_RUN_ID,
        "generated_at_utc": generated_at,
        "producer": "foundation.control_plane.signalcard_adapter_probe",
        "outputs": {
            "adapter_contract": {"path": _rel(root, adapter_contract_path), "sha256": sha256_file_lf_normalized(adapter_contract_path)},
            "parity_report": {"path": _rel(root, parity_report_path), "sha256": sha256_file_lf_normalized(parity_report_path)},
            "signalcard_summary": {"path": _rel(root, signalcard_summary_path), "sha256": sha256_file_lf_normalized(signalcard_summary_path)},
            "model_pack_manifest": {
                "path": _rel(root, model_pack_manifest_path),
                "sha256": sha256_file_lf_normalized(model_pack_manifest_path),
            },
        },
        "selected_candidate": result.summary["selected_candidate"],
        "claim_boundary": BOUNDARY,
    }


def _result_summary_markdown(generated_at: str, result: SignalCardProbeResult) -> str:
    selected = result.summary["selected_candidate"]
    lines = [
        "# Stage33 RUN27C SignalCard Adapter Probe(33단계 실행27C 신호 카드 어댑터 탐침)",
        "",
        f"- generated_at_utc(생성 시각 UTC): `{generated_at}`",
        f"- run_id(실행 ID): `{RUN_ID}`",
        f"- selected candidate(선택 후보): `{selected['candidate_id']}`",
        f"- parity rows(동등성 행): `{result.summary['parity_rows']}`",
        f"- parity passed(동등성 통과): `{result.summary['parity_passed']}`",
        f"- signal direction mismatches(신호 방향 불일치): `{result.summary['signal_direction_mismatches']}`",
        f"- ONNX readiness decision(ONNX 준비 결정): `{result.summary['onnx_readiness_decision']}`",
        "",
        "## Evidence Gate(근거 게이트)",
        "",
        "run27C(27C 실행)는 run27B(27B 실행)의 1순위 후보를 SignalCard adapter(신호 카드 어댑터)로 감싸고, validation/OOS(검증/표본외) feature matrix(피처 행렬)에서 Python source model(파이썬 원천 모델)과 ONNX runtime(온닉스 런타임)의 probability(확률)와 SignalCard direction(신호 카드 방향)을 비교했다.",
        "",
        "효과(effect, 효과)는 ONNX(온닉스)를 새로 만들기 전에 기존 ONNX artifact(기존 온닉스 산출물)가 adapter contract(어댑터 계약) 안에서 재현 가능한지 확인하는 것이다.",
        "",
        "## Model Pack(모델 팩)",
        "",
        f"- model_pack_id(모델 팩 ID): `{result.summary['model_pack_manifest_id']}`",
        "- packaging policy(포장 정책): `manifest_only_existing_onnx_artifacts_no_reexport(기존 온닉스 산출물 목록 포장, 재내보내기 없음)`",
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


def _artifact_identity(root: Path, path: Path) -> dict[str, Any]:
    return {"path": _rel(root, path), "sha256": sha256_file(path)}


def _write_json(path: Path, payload: Mapping[str, Any]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _write_markdown(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text, encoding="utf-8-sig")


def _upsert_registers(root: Path, result: SignalCardProbeResult) -> None:
    upsert_csv_rows(root / "docs/registers/run_registry.csv", RUN_REGISTRY_COLUMNS, [result.run_registry_row], key="run_id")
    upsert_csv_rows(root / "docs/registers/alpha_run_ledger.csv", ALPHA_LEDGER_COLUMNS, result.stage_rows, key="ledger_row_id")
    artifact_path = root / "docs/registers/artifact_registry.csv"
    existing = read_csv_rows(artifact_path)
    columns = ("artifact_id", "type", "path", "status", "notes")
    new_ids = {row["artifact_id"] for row in result.artifact_rows}
    rows = [row for row in existing if row.get("artifact_id") not in new_ids]
    rows.extend(result.artifact_rows)
    write_csv_rows(artifact_path, columns, rows)


def _rel(root: Path, path: Path) -> Path:
    return path.relative_to(root)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run Stage33 SignalCard adapter probe for the top run27B candidate.")
    parser.add_argument("--root", default=".")
    parser.add_argument("--summary-only", action="store_true")
    args = parser.parse_args(argv)
    if args.summary_only:
        result = build_signalcard_adapter_probe(Path(args.root))
        print(json.dumps(json_ready(result.summary), ensure_ascii=False, indent=2))
    else:
        aggregate = write_signalcard_adapter_probe_packet(Path(args.root))
        print(json.dumps(json_ready(aggregate), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
