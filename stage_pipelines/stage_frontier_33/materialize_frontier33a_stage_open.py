from __future__ import annotations

import csv
import hashlib
import json
import math
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists
from foundation.models.onnx_bridge import ordered_hash
from stage_pipelines.stage_frontier_03 import frontier03b_regime_asymmetric_label_proxy_scout as f03b
from stage_pipelines.stage_frontier_23 import frontier23b_payoff_asymmetry_pf_source_proxy_scout as f23b
from stage_pipelines.stage_frontier_32 import frontier32d_stage_closeout as f32d
from stage_pipelines.stage_frontier_32 import materialize_frontier32a_stage_open as f32a


STAGE_ID = "stage_frontier_33__path_native_exit_label_or_mfe_mae_surface_for_density_edge_onnx_scout"
RUN_ID = "frontier33A_stage_open_path_native_exit_label_or_mfe_mae_surface_hypothesis_design_v1"
RUN_NUMBER = "frontier33A"
PARENT_RUN_ID = f32d.RUN_ID
NEXT_RUN_ID = "frontier33B_path_native_mfe_mae_exit_surface_proxy_scout_v1"
STATUS = "opened_frontier33_path_native_exit_label_no_authority"
JUDGMENT = "stage_opened_after_grok_accepted_path_native_exit_boundary"

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REPORT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_report.md"
GROK_RECEIPT_PATH = STAGE_ROOT / "03_reviews" / "grok_stage_open_receipt.md"
LOCAL_VERIFICATION_PATH = STAGE_ROOT / "03_reviews" / "local_verification.md"
SCRIPT_PATH = Path("stage_pipelines/stage_frontier_33/materialize_frontier33a_stage_open.py")
DECISION_PATH = Path("docs/decisions/2026-06-14_stage_frontier_33_path_native_exit_label_open.md")

GROK_PACKET = Path("docs/agent_control/grok_reviews/2026-06-14_frontier33_stage_open/small_review")
F32_SELECTION = Path("stages") / f32d.STAGE_ID / "04_selected" / "selection_status.md"
F32_NEGATIVE_MEMORY = Path("stages") / f32d.STAGE_ID / "04_selected" / "negative_memory.md"
F32_CLOSEOUT_SUMMARY = Path("stages") / f32d.STAGE_ID / "02_runs" / f32d.RUN_ID / "stage_closeout_summary.json"
RAW_US100_PATH = f32a.RAW_US100_PATH
RAW_US100_MANIFEST = f32a.RAW_US100_MANIFEST

RUN_REGISTRY = Path("docs/registers/run_registry.csv")
ALPHA_LEDGER = Path("docs/registers/alpha_run_ledger.csv")
IDEA_REGISTRY = Path("docs/registers/idea_registry.md")
CHANGELOG = Path("docs/workspace/changelog.md")
WORKSPACE_STATE = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE = Path("docs/context/current_working_state.md")

LOCKS = {
    "selection_split": "train_only_parameter_source",
    "forward_splits": "validation_oos_read_only",
    "active_changed_variable": "path_native_mfe_mae_exit_quality_label_and_entry_surface",
    "raw_price_source": RAW_US100_PATH.as_posix(),
    "price_basis": "Bid",
    "entry_exit_basis": "raw_open_to_raw_open_matching_dataset_future_return",
    "path_label_source": "train_only_mfe_mae_quantiles_and_first_hit_sl_tp",
    "threshold_source": "train_split_mfe_mae_quantiles_only",
    "intrabar_tie_break_rule": {
        "long_both_stop_and_take_same_bar": "conservative_stop_first",
        "short_both_stop_and_take_same_bar": "conservative_stop_first",
        "reason": "M5 OHLC has no tick order, so ambiguous same-bar hits must not inflate PF.",
    },
    "forbidden_primary_path": [
        "reuse_f31_or_f32_return_space_caps_as_parameters",
        "rerank_or_refit_by_validation_or_oos_thresholds",
        "change_stop_take_thresholds_after_forward_path_read",
        "claim_runtime_from_python_path_proxy_only",
        "claim_onnx_readiness_from_path_native_proxy_only",
        "run_mt5_before_path_proxy_candidate_and_pre_expensive_grok",
        "inherit_f31_f32_winner_baseline_promotion_runtime_authority",
    ],
    "success_boundary": {
        "scout_clue": "validation_oos_pf_ge_1_05_density_5_to_10_dd_le_20",
        "seed_surface": "validation_oos_pf_ge_1_20_density_5_to_10_dd_le_15",
        "runtime_probe_candidate": "validation_oos_pf_ge_1_50_density_5_to_10_dd_le_12_executable_first_hit_representation",
        "not_runtime_authority": "MT5 tester output is required before runtime probe observation and much more before runtime authority.",
    },
    "tier_pair_boundary": "Tier B and Tier A+B are missing_required until explicitly materialized in this frontier.",
}


def main() -> int:
    ensure_dirs()
    normalize_grok_markdown()
    created_at = utc_now()
    frame = f23b.load_frame()
    feature_order = f23b.read_feature_order()
    raw_manifest = read_json(RAW_US100_MANIFEST)
    grok = read_grok_packet(GROK_PACKET)
    alignment = build_alignment_audit(frame)
    local = local_verification(frame, feature_order, raw_manifest, grok, alignment)
    if local["judgment"] != "pass_open_ready_with_path_native_locks":
        raise RuntimeError(f"Frontier33A local verification failed: {json.dumps(local, ensure_ascii=False)}")
    summary = build_summary(created_at, frame, feature_order, raw_manifest, grok, alignment, local)
    write_outputs(summary)
    update_registries(summary)
    update_current_truth(summary)
    print(json.dumps(json_ready({
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "grok_classification": grok["classification"],
        "alignment_p99_abs_delta": summary["alignment_audit"]["p99_abs_delta"],
        "runtime_probe_status": summary["runtime_probe_status"],
        "next_run_id": NEXT_RUN_ID,
        "report": REPORT_PATH.as_posix(),
    }), ensure_ascii=False, indent=2))
    return 0


def ensure_dirs() -> None:
    for path in (
        RUN_ROOT,
        STAGE_ROOT / "00_spec",
        STAGE_ROOT / "01_inputs",
        STAGE_ROOT / "02_runs" / "active",
        STAGE_ROOT / "02_runs" / "archived",
        STAGE_ROOT / "03_reviews",
        STAGE_ROOT / "04_selected",
        DECISION_PATH.parent,
    ):
        io_path(path).mkdir(parents=True, exist_ok=True)
    ensure_stage_ledger_header()


def ensure_stage_ledger_header() -> None:
    path = STAGE_ROOT / "03_reviews" / "stage_run_ledger.csv"
    if path_exists(path):
        return
    with io_path(ALPHA_LEDGER).open("r", encoding="utf-8-sig", newline="") as handle:
        header = next(csv.reader(handle))
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        csv.writer(handle, lineterminator="\n").writerow(header)


def normalize_grok_markdown() -> None:
    for name in ("input_prompt.md", "prompt.md", "clean_output.md"):
        path = GROK_PACKET / name
        if path_exists(path):
            text = io_path(path).read_text(encoding="utf-8-sig")
            f03b.write_text_sig(path, text.rstrip() + "\n")


def read_grok_packet(packet: Path) -> dict[str, Any]:
    metadata = read_json(packet / "metadata.json")
    output = read_text(packet / "clean_output.md")
    lowered = output.lower()
    accepted = (
        ("verdict:** accepted" in lowered or "verdict: accepted" in lowered)
        and ("novelty_ok:** yes" in lowered or "novelty_ok: yes" in lowered)
        and ("frontier_boundary_ok:** yes" in lowered or "frontier_boundary_ok: yes" in lowered)
        and ("hypothesis_scope_ok:** yes" in lowered or "hypothesis_scope_ok: yes" in lowered)
        and ("runtime_claim_boundary_ok:** yes" in lowered or "runtime_claim_boundary_ok: yes" in lowered)
        and ("leakage_risk:** medium" in lowered or "leakage_risk: medium" in lowered or "leakage_risk:** low" in lowered or "leakage_risk: low" in lowered)
    )
    return {
        "packet": packet.as_posix(),
        "prompt": (packet / "prompt.md").as_posix(),
        "output": (packet / "clean_output.md").as_posix(),
        "metadata": (packet / "metadata.json").as_posix(),
        "prompt_hash": metadata.get("prompt_hash", ""),
        "success": bool(metadata.get("success")),
        "returncode": metadata.get("returncode"),
        "timed_out": bool(metadata.get("timed_out")),
        "unexpected_top_level_artifacts": metadata.get("unexpected_top_level_artifacts", []),
        "classification": "accepted_path_native_exit_label_boundary_medium_leakage_guarded" if accepted else "needs_local_verification",
        "accepted": accepted,
        "output_excerpt": output[:3600],
    }


def build_alignment_audit(frame: pd.DataFrame) -> dict[str, Any]:
    raw = pd.read_csv(io_path(RAW_US100_PATH), usecols=["time_open_unix", "open", "high", "low", "close", "spread_points"])
    raw["timestamp"] = pd.to_datetime(raw["time_open_unix"], unit="s", utc=True)
    raw = raw[["timestamp", "open", "high", "low", "close", "spread_points"]].rename(columns={"open": "entry_open"})
    sample = frame[["timestamp", "future_timestamp", "future_log_return_12"]].copy()
    merged = sample.merge(raw[["timestamp", "entry_open"]], on="timestamp", how="left")
    future = raw[["timestamp", "entry_open"]].rename(columns={"timestamp": "future_timestamp", "entry_open": "future_open"})
    merged = merged.merge(future, on="future_timestamp", how="left")
    calc = np.log(merged["future_open"].astype("float64") / merged["entry_open"].astype("float64"))
    delta = (calc - pd.to_numeric(merged["future_log_return_12"], errors="coerce")).abs()
    return {
        "raw_path": RAW_US100_PATH.as_posix(),
        "rows_checked": int(len(merged)),
        "missing_entry_open_rows": int(merged["entry_open"].isna().sum()),
        "missing_future_open_rows": int(merged["future_open"].isna().sum()),
        "median_abs_delta": float(delta.median()),
        "p99_abs_delta": float(delta.quantile(0.99)),
        "max_abs_delta": float(delta.max()),
        "within_1e_4_rows": int((delta <= 0.0001).sum()),
        "within_2e_4_rows": int((delta <= 0.0002).sum()),
        "basis_judgment": "open_to_open_alignment_usable_for_path_native_first_hit_proxy",
    }


def local_verification(
    frame: pd.DataFrame,
    feature_order: list[str],
    raw_manifest: dict[str, Any],
    grok: dict[str, Any],
    alignment: dict[str, Any],
) -> dict[str, Any]:
    workspace = read_text(WORKSPACE_STATE)
    f32_selection = read_text(F32_SELECTION)
    f32_negative = read_text(F32_NEGATIVE_MEMORY)
    checks = {
        "workspace_current_f32d_or_f33a": (
            f"current_stage_id: {f32d.STAGE_ID}" in workspace and f"current_run_id: {f32d.RUN_ID}" in workspace
        ) or (
            f"current_stage_id: {STAGE_ID}" in workspace and f"current_run_id: {RUN_ID}" in workspace
        ),
        "workspace_next_frontier33a_or_frontier33b": f"next_run_id: {RUN_ID}" in workspace or f"next_run_id: {NEXT_RUN_ID}" in workspace,
        "f32_selection_points_to_f33a": RUN_ID in f32_selection,
        "f32_negative_memory_present": "f32_return_space_handoff_surface_failed_executable_sl_tp_raw_path_proxy" in f32_negative,
        "raw_manifest_bid_us100_m5": raw_manifest.get("contract_symbol") == "US100"
        and raw_manifest.get("timeframe") == "M5"
        and raw_manifest.get("price_basis") == "Bid",
        "raw_ohlc_exists": path_exists(RAW_US100_PATH),
        "alignment_no_missing_rows": alignment["missing_entry_open_rows"] == 0 and alignment["missing_future_open_rows"] == 0,
        "alignment_p99_abs_delta_small": float(alignment["p99_abs_delta"]) <= 0.0002,
        "feature_hash_matches_contract": ordered_hash(feature_order) == f23b.EXPECTED_FEATURE_HASH,
        "dataset_has_required_splits": set(frame["split"].astype(str).unique()) == {"train", "validation", "oos"},
        "grok_transport_success": grok["success"] and grok["returncode"] == 0 and not grok["timed_out"],
        "grok_accepted_boundary": grok["accepted"],
        "grok_no_unexpected_top_level_artifacts": not grok["unexpected_top_level_artifacts"],
        "return_space_cap_reuse_forbidden": "reuse_f31_or_f32_return_space_caps_as_parameters" in LOCKS["forbidden_primary_path"],
        "threshold_source_train_only": LOCKS["threshold_source"] == "train_split_mfe_mae_quantiles_only",
        "intrabar_tie_break_locked": LOCKS["intrabar_tie_break_rule"]["long_both_stop_and_take_same_bar"] == "conservative_stop_first",
    }
    return {
        "checks": checks,
        "judgment": "pass_open_ready_with_path_native_locks" if all(checks.values()) else "needs_manual_review",
        "alignment_audit": alignment,
        "grok_leakage_note": "Grok marked leakage risk medium because path horizon choices could smuggle F32 return-space caps back in; F33A forbids cap reuse and locks train-only MFE/MAE thresholds.",
    }


def build_summary(
    created_at: str,
    frame: pd.DataFrame,
    feature_order: list[str],
    raw_manifest: dict[str, Any],
    grok: dict[str, Any],
    alignment: dict[str, Any],
    local: dict[str, Any],
) -> dict[str, Any]:
    return {
        "created_at_utc": created_at,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "hypothesis": "path_native_mfe_mae_first_hit_exit_labels_can_find_density_edge_without_return_space_cap_translation",
        "decision_use": "decide_whether_any_path_native_entry_exit_surface deserves pre_expensive_grok_and_mt5_runtime_probe",
        "comparison_baseline": "F32 negative memory and F23 feature input surface, reference only not inherited authority",
        "dataset_rows": int(len(frame)),
        "split_counts": {key: int(value) for key, value in frame["split"].astype(str).value_counts().to_dict().items()},
        "feature_count": int(len(feature_order)),
        "feature_order_hash": ordered_hash(feature_order),
        "raw_manifest": {
            "contract_symbol": raw_manifest.get("contract_symbol"),
            "broker_symbol": raw_manifest.get("broker_symbol"),
            "timeframe": raw_manifest.get("timeframe"),
            "price_basis": raw_manifest.get("price_basis"),
            "row_count": raw_manifest.get("row_count"),
            "time_basis": raw_manifest.get("time_basis"),
            "timezone_status": raw_manifest.get("timezone_status"),
        },
        "alignment_audit": alignment,
        "locks": LOCKS,
        "grok": grok,
        "local_verification": local,
        "runtime_probe_status": "runtime_probe_out_of_scope_by_claim_stage_open_no_path_proxy_yet",
        "result_boundary": "stage_open_no_model_training_no_wfo_no_mt5_no_onnx_no_authority",
        "claim_boundary": {claim: "not_claimed" for claim in f03b.FORBIDDEN_CLAIMS},
    }


def write_outputs(summary: dict[str, Any]) -> None:
    write_json(STAGE_ROOT / "01_inputs" / "raw_open_to_open_alignment_audit.json", summary["alignment_audit"])
    write_json(RUN_ROOT / "stage_open_summary.json", summary)
    write_json(RUN_ROOT / "run_manifest.json", run_manifest(summary))
    write_json(RUN_ROOT / "path_native_exit_label_lock.json", LOCKS)
    f03b.write_text_sig(STAGE_ROOT / "00_spec" / "stage_brief.md", stage_brief(summary))
    f03b.write_text_sig(REPORT_PATH, report_text(summary))
    f03b.write_text_sig(GROK_RECEIPT_PATH, grok_receipt(summary))
    f03b.write_text_sig(LOCAL_VERIFICATION_PATH, local_verification_text(summary))
    f03b.write_text_sig(STAGE_ROOT / "04_selected" / "selection_status.md", selection_status(summary))
    f03b.write_text_sig(DECISION_PATH, decision_text(summary))


def run_manifest(summary: dict[str, Any]) -> dict[str, Any]:
    artifacts = [
        SCRIPT_PATH,
        GROK_PACKET / "prompt.md",
        GROK_PACKET / "clean_output.md",
        GROK_PACKET / "metadata.json",
        F32_SELECTION,
        F32_NEGATIVE_MEMORY,
        F32_CLOSEOUT_SUMMARY,
        RAW_US100_MANIFEST,
        f23b.DATASET_PATH,
        f23b.FEATURE_ORDER_PATH,
        STAGE_ROOT / "01_inputs" / "raw_open_to_open_alignment_audit.json",
        RUN_ROOT / "stage_open_summary.json",
        RUN_ROOT / "path_native_exit_label_lock.json",
        REPORT_PATH,
    ]
    return {
        "identity": {
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "parent_run_id": PARENT_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "created_at_utc": summary["created_at_utc"],
        },
        "artifacts": [artifact_identity(path) for path in artifacts],
        "runtime_claim_boundary": "research_only_stage_open_no_path_proxy_yet",
        "claim_boundary": summary["claim_boundary"],
    }


def update_registries(summary: dict[str, Any]) -> None:
    upsert_csv_io(RUN_REGISTRY, "run_id", run_registry_row(summary))
    for row in ledger_rows(summary):
        upsert_csv_io(ALPHA_LEDGER, "ledger_row_id", row)
        upsert_csv_io(STAGE_ROOT / "03_reviews" / "stage_run_ledger.csv", "ledger_row_id", row)
    f03b.append_once(CHANGELOG, RUN_ID, changelog_entry(summary))
    f03b.append_once(IDEA_REGISTRY, RUN_ID, idea_registry_entry(summary))


def run_registry_row(summary: dict[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "stage_open(단계 개방)",
        "family": "experiment_design(실험 설계)",
        "work_family": "experiment_execution(실험 실행)",
        "status": summary["status"],
        "judgment": summary["judgment"],
        "path": REPORT_PATH.as_posix(),
        "notes": f"grok={summary['grok']['classification']};alignment_p99={fmt(summary['alignment_audit']['p99_abs_delta'])};next={NEXT_RUN_ID};no_authority",
        "run_number": RUN_NUMBER,
        "date": "2026-06-14",
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "claim_boundary": summary["result_boundary"],
        "report_path": REPORT_PATH.as_posix(),
        "created_at_utc": summary["created_at_utc"],
        "primary_kpi": f"raw_rows={summary['raw_manifest']['row_count']};dataset_rows={summary['dataset_rows']}",
        "guardrail_kpi": "stage_open_no_path_proxy_no_mt5_no_onnx_no_authority",
        "external_verification_status": summary["runtime_probe_status"],
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "result_path": REPORT_PATH.as_posix(),
    }


def ledger_rows(summary: dict[str, Any]) -> list[dict[str, Any]]:
    return [{
        "ledger_row_id": f"{RUN_ID}__stage_open",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": f"{RUN_ID}__stage_open",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "stage_open(단계 개방)",
        "tier_scope": "not_applicable_stage_open(단계 개방에는 해당 없음)",
        "kpi_scope": "planning_only_no_trading_kpi(계획 전용, 거래 KPI 없음)",
        "scoreboard_lane": "stage_open(단계 개방)",
        "status": summary["status"],
        "judgment": summary["judgment"],
        "path": REPORT_PATH.as_posix(),
        "primary_kpi": f"grok={summary['grok']['classification']};feature_hash={summary['feature_order_hash']}",
        "guardrail_kpi": "path_native_lock_no_wfo_no_mt5_no_onnx_no_authority",
        "external_verification_status": summary["runtime_probe_status"],
        "notes": f"next={NEXT_RUN_ID};changed_variable={LOCKS['active_changed_variable']};no_authority",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "run_family": "stage_open(단계 개방)",
    }]


def update_current_truth(summary: dict[str, Any]) -> None:
    io_path(WORKSPACE_STATE).write_text(workspace_state(summary), encoding="utf-8-sig")
    f03b.write_text_sig(CURRENT_WORKING_STATE, current_working_state(summary))


def workspace_state(summary: dict[str, Any]) -> str:
    return "\n".join([
        f"current_stage_id: {STAGE_ID}",
        f"current_run_id: {RUN_ID}",
        f"latest_completed_run_id: {RUN_ID}",
        f"current_status: {summary['status']}",
        f"current_judgment: {summary['judgment']}",
        f"next_run_id: {NEXT_RUN_ID}",
        "runtime_authority: not_claimed",
        "operating_promotion: not_claimed",
        "goal_achieve: not_claimed",
        f"updated_at_utc: '{summary['created_at_utc']}'",
        "",
    ])


def stage_brief(summary: dict[str, Any]) -> str:
    return f"""# Frontier33 Stage Brief(전선33 단계 요약)

Opened(개방): {summary['created_at_utc']}

Hypothesis(가설): raw OHLC path(원천 시가/고가/저가/종가 경로)에서 MFE/MAE(최대 유리/불리 이동)와 first-hit SL/TP label(선터치 손절/익절 라벨)을 train-only(학습 전용)로 만들면, F32 return-space cap translation(수익률 공간 한도 번역)보다 더 실행 가능한 density-edge surface(밀도-우위 표면)를 찾을 수 있습니다.

Action(행동): F33(전선33)을 path-native exit label(경로 기반 청산 라벨) stage(단계)로 열고, raw US100 M5 Bid OHLC(원천 유에스100 5분봉 매수호가 시가/고가/저가/종가) 정렬과 Grok review(그록 검토)를 잠갔습니다.

Effect(효과): F31/F32 winner, baseline, promotion, runtime authority(승자/기준선/승격/런타임 권위)를 상속하지 않고, train-only MFE/MAE threshold(학습 전용 최대 유리/불리 이동 임계값)만 새 changed variable(변경 변수)로 시험합니다.

Intrabar tie-break(봉내 동시 터치 규칙): same-bar stop/take hit(같은 봉 손절/익절 동시 터치)는 conservative stop-first(보수적 손절 우선)입니다.

Claim boundary(주장 경계): no completion, no baseline, no promotion, no runtime authority, no live readiness, no Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음).
"""


def report_text(summary: dict[str, Any]) -> str:
    align = summary["alignment_audit"]
    return f"""# Frontier33A Stage Open Report(전선33A 단계 개방 보고서)

Updated(갱신): {summary['created_at_utc']}

Status(상태): `{summary['status']}`

Judgment(판정): `{summary['judgment']}`

Action(행동): F33(전선33)을 path-native MFE/MAE first-hit exit label(경로 기반 최대 유리/불리 이동 선터치 청산 라벨) hypothesis(가설)로 열었습니다.

Effect(효과): F32 negative memory(부정 기억)의 return-space cap translation(수익률 공간 한도 번역)을 반복하지 않도록, return cap reuse(수익률 한도 재사용)를 금지하고 train-only path threshold(학습 전용 경로 임계값)로 제한합니다.

Grok classification(그록 분류): `{summary['grok']['classification']}`

Raw alignment(원천 정렬): rows(행) `{align['rows_checked']}`, missing entry/future(진입/미래 누락) `{align['missing_entry_open_rows']}/{align['missing_future_open_rows']}`, p99 abs delta(99퍼센타일 절대 차이) `{fmt(align['p99_abs_delta'])}`.

Runtime probe status(런타임 탐침 상태): `{summary['runtime_probe_status']}`

Next action(다음 행동): `{NEXT_RUN_ID}`

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def grok_receipt(summary: dict[str, Any]) -> str:
    grok = summary["grok"]
    return f"""# Frontier33A Grok Stage-Open Receipt(전선33A 그록 단계 개방 영수증)

Trigger reason(호출 이유): goal(목표)이 Grok second opinion(그록 2차 의견)을 stage open(단계 개방)에 요구합니다.

Review size(검토 크기): small review(소규모 검토)

Direction before Grok(그록 전 방향): F32 return-space cap translation failure(수익률 공간 한도 번역 실패)를 반복하지 않고, path-native MFE/MAE first-hit label(경로 기반 최대 유리/불리 이동 선터치 라벨)을 시험합니다.

Prompt(프롬프트): `{grok['prompt']}`

Output(출력): `{grok['output']}`

Metadata(메타데이터): `{grok['metadata']}`

Classification(분류): `{grok['classification']}`

Accepted advice(수용 조언): stage open(단계 개방), novelty OK(신규성 승인), medium leakage risk(중간 누수 위험), return-space cap reuse prohibition(수익률 공간 한도 재사용 금지)을 수용했습니다.

Rejected advice(거절 조언): F31/F32 proxy(전선31/32 프록시)를 baseline/promotion/runtime authority(기준선/승격/런타임 권위)로 상속하는 경로는 없습니다.

Local verification(로컬 검증): `{summary['local_verification']['judgment']}`
"""


def local_verification_text(summary: dict[str, Any]) -> str:
    rows = [f"- {key}: `{value}`" for key, value in summary["local_verification"]["checks"].items()]
    return f"""# Frontier33A Local Verification(전선33A 로컬 검증)

Judgment(판정): `{summary['local_verification']['judgment']}`

{chr(10).join(rows)}

Effect(효과): Grok(그록) 조언을 로컬 workspace state(작업공간 상태), F32 negative memory(전선32 부정 기억), raw bars(원천 봉), dataset(데이터셋), lock(잠금)과 대조한 뒤 stage open(단계 개방)을 기록했습니다.
"""


def selection_status(summary: dict[str, Any]) -> str:
    return f"""# Frontier33 Selection Status(전선33 선택 상태)

Updated(갱신): {summary['created_at_utc']}

Selection(선택): no selected baseline/completion/promotion/runtime authority(선택 기준선/완성/승격/런타임 권위 없음).

Latest run(최근 실행): `{RUN_ID}`

Status(상태): `{summary['status']}`

Judgment(판정): `{summary['judgment']}`

Runtime probe status(런타임 탐침 상태): `{summary['runtime_probe_status']}`

Next action(다음 행동): `{NEXT_RUN_ID}`

Claim boundary(주장 경계): no completion, no baseline, no promotion, no runtime authority, no live readiness, no Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음).
"""


def decision_text(summary: dict[str, Any]) -> str:
    return f"""# Decision(결정): Open Frontier33 Path-Native Exit Label(전선33 경로 기반 청산 라벨 개방)

Date(날짜): 2026-06-14

Decision(결정): Open(개방) `{STAGE_ID}` with run(실행) `{RUN_ID}`.

Effect(효과): F32(전선32)의 return-space cap translation(수익률 공간 한도 번역) 실패를 negative memory(부정 기억)로 두고, raw path MFE/MAE(원천 경로 최대 유리/불리 이동)를 새 원천으로 시험합니다.

Next run(다음 실행): `{NEXT_RUN_ID}`
"""


def current_working_state(summary: dict[str, Any]) -> str:
    return f"""# Current Working State(현재 작업 상태)

Updated(갱신): {summary['created_at_utc']}

## Active Stage(현재 단계)

- stage(단계): `{STAGE_ID}`
- latest run(최근 실행): `{RUN_ID}`
- status(상태): `{summary['status']}`
- judgment(판정): `{summary['judgment']}`
- next run(다음 실행): `{NEXT_RUN_ID}`

## Current Truth(현재 진실)

Action(행동): F33(전선33)은 path-native exit label / MFE-MAE surface(경로 기반 청산 라벨 / 최대 유리-불리 이동 표면) 가설로 열렸습니다.

Effect(효과): F32(전선32)의 return-space cap translation failure(수익률 공간 한도 번역 실패)를 반복하지 않도록 return-space cap reuse(수익률 공간 한도 재사용)를 금지하고, 다음 실행은 train-only MFE/MAE path proxy(학습 전용 최대 유리/불리 이동 경로 프록시)입니다.

Runtime probe boundary(런타임 탐침 경계): `{summary['runtime_probe_status']}`

Claim boundary(주장 경계): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def changelog_entry(summary: dict[str, Any]) -> str:
    return (
        f"- {summary['created_at_utc']}: `{RUN_ID}` opened Frontier33 path-native exit label(전선33 경로 기반 청산 라벨). "
        f"Effect(효과): alignment_p99={fmt(summary['alignment_audit']['p99_abs_delta'])}, next=`{NEXT_RUN_ID}`, no authority(권위 없음).\n"
    )


def idea_registry_entry(summary: dict[str, Any]) -> str:
    return (
        f"- `IDEA-FR33-PATH-NATIVE-EXIT-LABEL-ONNX-SCOUT`: `{RUN_ID}` opened train-only MFE/MAE first-hit label(학습 전용 최대 유리/불리 이동 선터치 라벨). "
        "Effect(효과): return-space cap translation(수익률 공간 한도 번역)을 반복하지 않는 새 path-native source(경로 기반 원천)를 시험합니다.\n"
    )


def artifact_identity(path: Path) -> dict[str, str]:
    return {"path": path.as_posix(), "sha256": sha256_io(path) if path_exists(path) else "missing"}


def sha256_io(path: Path) -> str:
    digest = hashlib.sha256()
    with io_path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def read_text(path: Path) -> str:
    return io_path(path).read_text(encoding="utf-8-sig")


def upsert_csv_io(path: Path, key: str, row: dict[str, Any]) -> None:
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        header = next(csv.reader(handle))
    rows: list[dict[str, str]] = []
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        rows.extend(dict(item) for item in csv.DictReader(handle))
    normalized = {column: stringify(row.get(column, "")) for column in header}
    replaced = False
    for index, existing in enumerate(rows):
        if existing.get(key) == normalized.get(key):
            rows[index] = normalized
            replaced = True
            break
    if not replaced:
        rows.append(normalized)
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=header, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for item in rows:
            writer.writerow({column: stringify(item.get(column, "")) for column in header})


def stringify(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(json_ready(value), ensure_ascii=False, sort_keys=True)
    if isinstance(value, float):
        if not math.isfinite(value):
            return ""
        return f"{value:.12g}"
    return str(value)


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def fmt(value: Any) -> str:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return "NA"
    if not math.isfinite(number):
        return "NA"
    return f"{number:.6f}"


if __name__ == "__main__":
    raise SystemExit(main())
