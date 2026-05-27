from __future__ import annotations

import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from stage_pipelines.stage329 import materialize_forward_feature_frames as stage329b
from stage_pipelines.stage337 import materialize_forward_safe_route_signal_rebuild_inputs_without_db as bo


aw = bo.aw
bg = bo.bg

TODAY = "2026-05-27"
STAGE_ID = bo.STAGE_ID
RUN_NUMBER = "run337BP"
RUN_ID = "run337BP_build_live_computable_feature_frame_preflight_without_db_v1"
PARENT_RUN_ID = bo.RUN_ID
NEXT_RUN_ID = "run337BQ_implement_asof_feature_join_and_runtime_parity_package_without_db_v1"
STATUS = "completed_stage337BP_live_computable_feature_frame_preflight_no_training_no_selection"
JUDGMENT = "feature_frames_materialized_exact_join_preflight_asof_gap_open"
DECISION = "stage337BP_open_run337BQ_asof_join_and_runtime_parity_package"
CLAIM_BOUNDARY = (
    "research_development_only_stage337BP_live_computable_feature_frame_preflight_without_db_"
    "no_model_training_no_threshold_tuning_no_candidate_selection_no_forward_passed_no_forward_failed_"
    "no_live_readiness_no_deployment_no_operating_promotion_no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = bo.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
FEATURE_FRAME_DIR = RUN_DIR / "feature_frames"
FEATURE_ORDER_DIR = RUN_DIR / "feature_orders"
FEATURE_SUMMARY_DIR = RUN_DIR / "feature_summaries"
REVIEWS_DIR = bo.REVIEWS_DIR
REPORT_PATH = REVIEWS_DIR / "run337BP_live_computable_feature_frame_preflight.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-27_stage337BP_live_computable_feature_frame_preflight.md"
SELECTED_STATUS = bo.SELECTED_STATUS
STAGE_BRIEF = bo.STAGE_BRIEF
WORKSPACE_STATE = bo.WORKSPACE_STATE
CURRENT_STATE = bo.CURRENT_STATE
CHANGELOG = bo.CHANGELOG
RUN_REGISTRY = bo.RUN_REGISTRY
ALPHA_LEDGER = bo.ALPHA_LEDGER
ARTIFACT_REGISTRY = bo.ARTIFACT_REGISTRY
STAGE_LEDGER = bo.STAGE_LEDGER

BO_DIR = STAGE_DIR / "02_runs" / "run337BO"
BO_FINAL = BO_DIR / "final_decision.json"
BO_FRESH_INVENTORY = BO_DIR / "fresh_raw_inventory.csv"
BO_QUALITY = BO_DIR / "data_quality_audit.csv"
BO_AVAILABILITY = BO_DIR / "live_input_availability_matrix.csv"
BO_ASOF_PREFLIGHT = BO_DIR / "asof_join_preflight.csv"
BO_FIREWALL = BO_DIR / "outcome_source_firewall.csv"
BO_PARITY_PLAN = BO_DIR / "parity_preflight_plan.csv"
BO_BLOCKED = BO_DIR / "blocked_input_list.csv"
BO_QUEUE = BO_DIR / "run337BP_feature_frame_preflight_queue.csv"
BO_GATE_AUDIT = BO_DIR / "required_gate_coverage_audit.csv"
BO_RAW_REFRESH = BO_DIR / "raw_refresh_probe"

STAGE329_SUMMARY = (
    ROOT
    / "stages"
    / "329_onnx_rebuild__live_feature_control"
    / "02_runs"
    / "run329B"
    / "feature_set_materialization_summary.csv"
)

FEATURE_SET_SUMMARY = RUN_DIR / "feature_set_materialization_summary.csv"
MISSING_FEATURE_COUNTS = RUN_DIR / "missing_feature_counts.csv"
INVALID_ROW_SAMPLES = RUN_DIR / "invalid_row_samples.csv"
FEATURE_LANE_BRIDGE = RUN_DIR / "feature_lane_bridge.csv"
EXACT_ASOF_GAP_REVIEW = RUN_DIR / "exact_asof_gap_review.csv"
FEATURE_FIREWALL = RUN_DIR / "feature_firewall.csv"
PARITY_HANDOFF_MATRIX = RUN_DIR / "parity_handoff_matrix.csv"
RUN337BQ_QUEUE = RUN_DIR / "run337BQ_asof_runtime_parity_queue.csv"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment_design_receipt.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
ARTIFACT_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
REQUIRED_GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (
    BO_FINAL,
    BO_FRESH_INVENTORY,
    BO_QUALITY,
    BO_AVAILABILITY,
    BO_ASOF_PREFLIGHT,
    BO_FIREWALL,
    BO_PARITY_PLAN,
    BO_BLOCKED,
    BO_QUEUE,
    BO_GATE_AUDIT,
)
OUTPUT_FILES = (
    FEATURE_SET_SUMMARY,
    MISSING_FEATURE_COUNTS,
    INVALID_ROW_SAMPLES,
    FEATURE_LANE_BRIDGE,
    EXACT_ASOF_GAP_REVIEW,
    FEATURE_FIREWALL,
    PARITY_HANDOFF_MATRIX,
    RUN337BQ_QUEUE,
    EXPERIMENT_RECEIPT,
    DATA_RECEIPT,
    MODEL_RECEIPT,
    RUNTIME_RECEIPT,
    ARTIFACT_RECEIPT,
    JUDGMENT_RECEIPT,
    REQUIRED_GATE_AUDIT,
    FINAL_DECISION,
    RUN_MANIFEST,
)

SUMMARY_COLUMNS = (
    "feature_set_id",
    "role",
    "feature_count",
    "feature_order_sha256",
    "scope_rows",
    "valid_rows",
    "invalid_rows",
    "alignment_missing_rows",
    "finite_missing_rows",
    "first_valid_timestamp",
    "last_valid_timestamp",
    "status",
    "parquet_path",
    "parquet_sha256",
    "feature_order_path",
    "feature_order_sha256_file",
    "claim_boundary",
)
MISSING_COLUMNS = ("feature_set_id", "feature", "missing_or_nonfinite_rows", "claim_boundary")
INVALID_COLUMNS = ("feature_set_id", "timestamp", "alignment_ready", "finite_ready", "claim_boundary")
LANE_BRIDGE_COLUMNS = (
    "lane_id",
    "feature_set_id",
    "lane_status",
    "feature_set_status",
    "valid_rows",
    "last_valid_timestamp",
    "effect",
    "claim_boundary",
)
ASOF_GAP_COLUMNS = (
    "feature_set_id",
    "current_join_policy",
    "alignment_missing_rows",
    "last_valid_timestamp",
    "asof_required",
    "gap_status",
    "next_action",
    "effect",
    "claim_boundary",
)
FIREWALL_COLUMNS = (
    "feature_set_id",
    "artifact",
    "forbidden_columns_found",
    "status",
    "effect",
    "claim_boundary",
)
PARITY_COLUMNS = (
    "handoff_id",
    "feature_set_id",
    "python_artifact",
    "mt5_required_artifact",
    "preflight_status",
    "blocked_status_if_missing",
    "effect",
    "claim_boundary",
)
QUEUE_COLUMNS = bo.QUEUE_COLUMNS
GATE_COLUMNS = bo.GATE_COLUMNS

LANE_TO_FEATURE_SET = {
    "bn_lane_rank_free_absolute_score": "core56_no_top3_weight_features",
    "bn_lane_live_market_regime_gate": "macro48_no_equity_breadth_or_top3",
    "bn_lane_proxy_only_diagnostic": "us100_technical42_no_external",
}
FORBIDDEN_FEATURE_TERMS = ("pnl", "profit", "trade", "outcome", "label", "future", "rank_forward")


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(aw.io_path(path).read_text(encoding="utf-8-sig"))


def read_rows(path: Path) -> list[dict[str, str]]:
    _, rows = aw.read_csv_table(path, prefer_head=False)
    return rows


def pass_fail(ok: bool) -> str:
    return "passed" if ok else "failed"


def load_inputs() -> dict[str, Any]:
    missing = [aw.rel(path) for path in INPUT_FILES if not aw.path_exists(path)]
    if missing:
        raise FileNotFoundError(f"missing run337BP inputs: {missing}")
    return {
        "bo_final": read_json(BO_FINAL),
        "bo_inventory": read_rows(BO_FRESH_INVENTORY),
        "bo_quality": read_rows(BO_QUALITY),
        "bo_availability": read_rows(BO_AVAILABILITY),
        "bo_asof": read_rows(BO_ASOF_PREFLIGHT),
        "bo_firewall": read_rows(BO_FIREWALL),
        "bo_parity": read_rows(BO_PARITY_PLAN),
        "bo_blocked": read_rows(BO_BLOCKED),
        "bo_queue": read_rows(BO_QUEUE),
        "bo_gate_audit": read_rows(BO_GATE_AUDIT),
        "stage329_summary": read_rows(STAGE329_SUMMARY) if aw.path_exists(STAGE329_SUMMARY) else [],
    }


def load_raw_part_longpath(raw_root: Path, contract_symbol: str, source_name: str, priority: int) -> pd.DataFrame:
    csv_path = stage329b.find_raw_csv(raw_root, contract_symbol)
    frame = pd.read_csv(stage329b.os_path(csv_path))
    required_columns = {"time_open_unix", "time_close_unix", "open", "high", "low", "close"}
    missing = required_columns.difference(frame.columns)
    if missing:
        raise RuntimeError(f"{csv_path} missing columns: {sorted(missing)}")
    frame["timestamp"] = pd.to_datetime(frame["time_close_unix"], unit="s", utc=True)
    frame["timestamp_policy"] = stage329b.fp.RAW_TIME_AXIS_POLICY
    frame = stage329b.attach_event_time_columns(frame)
    frame["__source_name"] = source_name
    frame["__source_priority"] = priority
    return frame


def configure_stage329(us100_last_close_utc: str) -> None:
    target_end = pd.Timestamp(us100_last_close_utc)
    stage329b.RUN_ID = RUN_ID
    stage329b.RUN_NUMBER = RUN_NUMBER
    stage329b.PARENT_RUN_ID = PARENT_RUN_ID
    stage329b.NEXT_ACTION = NEXT_RUN_ID
    stage329b.STATUS = STATUS
    stage329b.JUDGMENT = JUDGMENT
    stage329b.DECISION = DECISION
    stage329b.CLAIM_BOUNDARY = CLAIM_BOUNDARY
    stage329b.STAGE_ID = STAGE_ID
    stage329b.STAGE_DIR = STAGE_DIR
    stage329b.RUN_DIR = RUN_DIR
    stage329b.FEATURE_FRAME_DIR = FEATURE_FRAME_DIR
    stage329b.FEATURE_ORDER_DIR = FEATURE_ORDER_DIR
    stage329b.FEATURE_SUMMARY_DIR = FEATURE_SUMMARY_DIR
    stage329b.REVIEWS_DIR = REVIEWS_DIR
    stage329b.SELECTED_DIR = STAGE_DIR / "04_selected"
    stage329b.DECISION_DOC = DECISION_DOC
    stage329b.FORWARD_RAW_ROOT = BO_RAW_REFRESH
    stage329b.FORWARD_RAW_SUMMARY = BO_FRESH_INVENTORY
    stage329b.FORWARD_REQUESTED_TO_UTC = target_end
    stage329b.COMPUTE_END_UTC = target_end
    stage329b.COMBINED_RAW_CACHE.clear()
    stage329b.COMBINED_IDENTITY_CACHE.clear()
    stage329b.load_raw_part = load_raw_part_longpath


def materialize_feature_preflight(us100_last_close_utc: str) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[Path], dict[str, Any]]:
    configure_stage329(us100_last_close_utc)
    summaries, missing_counts, invalid_samples, frame_artifacts, foundation_counts = stage329b.build_feature_frames()
    clean_summaries: list[dict[str, Any]] = []
    for row in summaries:
        clean = dict(row)
        clean["claim_boundary"] = CLAIM_BOUNDARY
        clean_summaries.append(clean)
    missing_rows = [dict(row, claim_boundary=CLAIM_BOUNDARY) for row in missing_counts]
    if not missing_rows:
        missing_rows = [{"feature_set_id": "", "feature": "", "missing_or_nonfinite_rows": 0, "claim_boundary": CLAIM_BOUNDARY}]
    invalid_rows = [dict(row, claim_boundary=CLAIM_BOUNDARY) for row in invalid_samples]
    if not invalid_rows:
        invalid_rows = [{"feature_set_id": "", "timestamp": "", "alignment_ready": "", "finite_ready": "", "claim_boundary": CLAIM_BOUNDARY}]
    return clean_summaries, missing_rows, invalid_rows, frame_artifacts, foundation_counts


def write_basic_artifacts(
    summaries: Sequence[Mapping[str, Any]],
    missing_rows: Sequence[Mapping[str, Any]],
    invalid_rows: Sequence[Mapping[str, Any]],
) -> list[Path]:
    return [
        aw.write_csv(FEATURE_SET_SUMMARY, SUMMARY_COLUMNS, summaries),
        aw.write_csv(MISSING_FEATURE_COUNTS, MISSING_COLUMNS, missing_rows),
        aw.write_csv(INVALID_ROW_SAMPLES, INVALID_COLUMNS, invalid_rows),
    ]


def summary_by_id(summaries: Sequence[Mapping[str, Any]]) -> dict[str, Mapping[str, Any]]:
    return {str(row.get("feature_set_id")): row for row in summaries}


def build_lane_bridge(src: Mapping[str, Any], summaries: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    by_summary = summary_by_id(summaries)
    availability = {row.get("lane_id"): row for row in src["bo_availability"]}
    rows: list[dict[str, Any]] = []
    for lane_id, feature_set_id in LANE_TO_FEATURE_SET.items():
        lane = availability.get(lane_id, {})
        summary = by_summary.get(feature_set_id, {})
        rows.append(
            {
                "lane_id": lane_id,
                "feature_set_id": feature_set_id,
                "lane_status": lane.get("status", ""),
                "feature_set_status": summary.get("status", ""),
                "valid_rows": summary.get("valid_rows", 0),
                "last_valid_timestamp": summary.get("last_valid_timestamp", ""),
                "effect": "BO 입력 가능 경로를 실제 feature frame(피처 프레임) 산출물과 연결한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_asof_gap_review(summaries: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in summaries:
        feature_set_id = str(row.get("feature_set_id", ""))
        alignment_missing = int(row.get("alignment_missing_rows", 0) or 0)
        gap_status = "gap_open_asof_join_required" if alignment_missing > 0 else "exact_join_sufficient_for_preflight"
        rows.append(
            {
                "feature_set_id": feature_set_id,
                "current_join_policy": "exact_timestamp_join(정확 시각 결합)",
                "alignment_missing_rows": alignment_missing,
                "last_valid_timestamp": row.get("last_valid_timestamp", ""),
                "asof_required": "true",
                "gap_status": gap_status,
                "next_action": NEXT_RUN_ID if alignment_missing > 0 else "carry_to_runtime_parity_preflight",
                "effect": "기존 exact join(정확 결합)으로 생기는 손실을 숨기지 않고 as-of join(시점 기준 결합) 작업으로 넘긴다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_feature_firewall(summaries: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in summaries:
        feature_set_id = str(row.get("feature_set_id", ""))
        order_path_text = str(row.get("feature_order_path", ""))
        order_path = ROOT / order_path_text
        if not order_path_text or not aw.path_exists(order_path):
            rows.append(
                {
                    "feature_set_id": feature_set_id,
                    "artifact": order_path_text,
                    "forbidden_columns_found": "feature_order_missing",
                    "status": "failed",
                    "effect": "feature order(피처 순서)가 없으면 런타임 인계를 할 수 없다.",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
            continue
        features = aw.io_path(order_path).read_text(encoding="utf-8-sig").splitlines()
        found = [term for term in FORBIDDEN_FEATURE_TERMS if any(term in feature.lower() for feature in features)]
        rows.append(
            {
                "feature_set_id": feature_set_id,
                "artifact": aw.rel(order_path),
                "forbidden_columns_found": ";".join(found),
                "status": "passed" if not found else "failed",
                "effect": "결과/라벨/미래/거래 결과 피처가 섞이지 않게 막는다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_parity_matrix(summaries: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in summaries:
        feature_set_id = str(row.get("feature_set_id", ""))
        status = "ready_for_mt5_feature_export_package" if row.get("status") == "materialized" else "blocked_no_feature_frame"
        rows.append(
            {
                "handoff_id": f"bp_parity_{feature_set_id}",
                "feature_set_id": feature_set_id,
                "python_artifact": row.get("parquet_path", ""),
                "mt5_required_artifact": f"Common/Files/Project_Obsidian_Prime_v2/stage337/run337BQ/{feature_set_id}_mt5_features.csv",
                "preflight_status": status,
                "blocked_status_if_missing": "blocked_python_mt5_feature_parity_missing",
                "effect": "다음 run(실행)에서 Python feature(파이썬 피처)와 MT5 feature(MT5 피처)를 같은 시각으로 비교하게 한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_queue(asof_rows: Sequence[Mapping[str, Any]], parity_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    gap_count = sum(1 for row in asof_rows if row.get("gap_status") == "gap_open_asof_join_required")
    ready_parity = sum(1 for row in parity_rows if row.get("preflight_status") == "ready_for_mt5_feature_export_package")
    return [
        {
            "queue_id": "run337BQ_asof_join_runtime_parity_package",
            "next_run_id": NEXT_RUN_ID,
            "review_subject": "as-of feature join and runtime parity package(시점 기준 피처 결합 및 런타임 동등성 패키지)",
            "inputs_to_review": ";".join(
                [
                    aw.rel(FEATURE_SET_SUMMARY),
                    aw.rel(FEATURE_LANE_BRIDGE),
                    aw.rel(EXACT_ASOF_GAP_REVIEW),
                    aw.rel(FEATURE_FIREWALL),
                    aw.rel(PARITY_HANDOFF_MATRIX),
                ]
            ),
            "must_confirm": "as-of join policy, feature export contract, Python-MT5 feature parity(시점 기준 결합 정책, 피처 내보내기 계약, 파이썬-MT5 피처 동등성)",
            "must_reject_if": "uses labels, tunes thresholds, treats exact-join frame as final runtime authority(라벨 사용, 임계값 조정, 정확 결합 프레임을 최종 런타임 권위로 취급)",
            "expected_outputs": f"asof_gap_rows={gap_count};ready_parity_frames={ready_parity}",
            "priority": "P0",
            "effect": "피처 생성 성공을 바로 모델 성공으로 과장하지 않고 런타임 동등성으로 넘긴다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def build_receipts(final: Mapping[str, Any], foundation_counts: Mapping[str, Any]) -> list[Path]:
    payloads = [
        (
            EXPERIMENT_RECEIPT,
            {
                "work_family": "experiment_execution",
                "primary_skill": "obsidian-run-evidence-system",
                "hypothesis": "fresh forward raw inputs can produce live-computable feature frames(최신 전진 원천 입력이 실시간 계산 가능 피처 프레임을 만들 수 있음)",
                "boundary": "feature preflight only; no training or selection(피처 사전점검만, 학습/선택 없음)",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            DATA_RECEIPT,
            {
                "data_source": aw.rel(BO_RAW_REFRESH),
                "feature_window_end": final.get("feature_window_end_utc"),
                "foundation_invalid_reason_breakdown": foundation_counts.get("invalid_reason_breakdown", {}),
                "asof_gap_status": "open_for_run337BQ",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            MODEL_RECEIPT,
            {
                "model_boundary": "no model, no labels, no threshold(모델/라벨/임계값 없음)",
                "selection_metric": "not_applicable",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            RUNTIME_RECEIPT,
            {
                "runtime_boundary": "Python feature frames materialized; MT5 parity package deferred to run337BQ(파이썬 피처 프레임 생성, MT5 동등성 패키지는 run337BQ)",
                "runtime_authority": "not_claimed",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            ARTIFACT_RECEIPT,
            {
                "lineage": f"parent={PARENT_RUN_ID};raw_refresh={aw.rel(BO_RAW_REFRESH)}",
                "feature_summary": aw.rel(FEATURE_SET_SUMMARY),
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            JUDGMENT_RECEIPT,
            {
                "judgment": final["judgment"],
                "forward_passed": "not_claimed",
                "forward_failed": "not_claimed",
                "goal_achieve": "not_claimed",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
    ]
    return [aw.write_json(path, payload) for path, payload in payloads]


def build_gates(
    src: Mapping[str, Any],
    summaries: Sequence[Mapping[str, Any]],
    lane_rows: Sequence[Mapping[str, Any]],
    asof_rows: Sequence[Mapping[str, Any]],
    firewall_rows: Sequence[Mapping[str, Any]],
    parity_rows: Sequence[Mapping[str, Any]],
    queue_rows: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    bo_passed = sum(1 for row in src["bo_gate_audit"] if row.get("status") == "passed")
    materialized_count = sum(1 for row in summaries if row.get("status") == "materialized")
    firewall_ok = all(row.get("status") == "passed" for row in firewall_rows)
    ready_parity = sum(1 for row in parity_rows if row.get("preflight_status") == "ready_for_mt5_feature_export_package")
    asof_gap_named = any(row.get("gap_status") == "gap_open_asof_join_required" for row in asof_rows)
    specs = [
        ("bp_gate_parent_final_loaded", src["bo_final"].get("next_action") == RUN_ID, f"parent_next={src['bo_final'].get('next_action')}", "run337BO opens run337BP(run337BO가 run337BP를 연다)"),
        ("bp_gate_parent_gates_passed", bo_passed == 10 and src["bo_final"].get("passed_gates") == 10, f"bo_gates={bo_passed}", "run337BO gates passed(run337BO 게이트 통과)"),
        ("bp_gate_no_blocked_inputs", len(src["bo_blocked"]) <= 1 and all(not row.get("blocker_id") for row in src["bo_blocked"]), f"blocked_rows={len(src['bo_blocked'])}", "no BO blockers(BO 차단 없음)"),
        ("bp_gate_feature_frames_materialized", materialized_count >= 3, f"materialized={materialized_count}", "three feature frames materialized(세 피처 프레임 생성)"),
        ("bp_gate_lane_bridge_ready", len(lane_rows) == 3, f"lane_rows={len(lane_rows)}", "lane to feature bridge ready(경로-피처 연결 준비)"),
        ("bp_gate_feature_firewall_passed", firewall_ok and len(firewall_rows) == 3, f"firewall_rows={len(firewall_rows)}", "feature firewall passed(피처 방화벽 통과)"),
        ("bp_gate_parity_package_ready", ready_parity >= 3, f"ready_parity={ready_parity}", "parity package inputs ready(동등성 패키지 입력 준비)"),
        ("bp_gate_asof_gap_named", asof_gap_named, f"asof_gap_named={asof_gap_named}", "as-of gap named(시점 기준 결합 공백 명명)"),
        ("bp_gate_queue_ready", len(queue_rows) == 1 and queue_rows[0].get("next_run_id") == NEXT_RUN_ID, f"queue_rows={len(queue_rows)}", "run337BQ queue ready(run337BQ 대기열 준비)"),
        ("bp_gate_no_goal_or_forward_pass_claim", True, "forward_passed=not_claimed;goal=not_claimed", "no forbidden claim(금지 주장 없음)"),
    ]
    return [
        {
            "gate_id": gate_id,
            "status": pass_fail(ok),
            "observed": observed,
            "expected": expected,
            "effect": "feature preflight stays separate from model or runtime authority(피처 사전점검을 모델/런타임 권위와 분리)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for gate_id, ok, observed, expected in specs
    ]


def count_passed(rows: Sequence[Mapping[str, Any]]) -> int:
    return sum(1 for row in rows if row.get("status") == "passed")


def write_report(final: Mapping[str, Any]) -> Path:
    text = f"""# Stage337 run337BP Live-Computable Feature Frame Preflight(실시간 계산 가능 피처 프레임 사전점검)

## Conclusion(결론)

run337BP(337BP 실행)는 run337BO(337BO 실행)의 최신 raw M5(원천 M5)로 3개 feature frame(피처 프레임)을 실제 생성했다.

Effect(효과): feature materialization(피처 물질화)은 통과했지만, 현재 builder(생성기)는 exact timestamp join(정확 시각 결합) 기반이다. 그래서 as-of join(시점 기준 결합)과 Python-MT5 parity(파이썬-MT5 동등성)를 run337BQ(337BQ 실행)에서 닫아야 한다.

## Result(결과)

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- gates(게이트): `{final['passed_gates']}/{final['gate_rows']}`
- materialized_feature_sets(생성 피처 세트): `{final['materialized_feature_sets']}`
- latest_feature_timestamp(최신 피처 시각): `{final['latest_feature_timestamp']}`
- asof_gap_rows(시점 기준 결합 공백 행): `{final['asof_gap_rows']}`
- next_action(다음 행동): `{final['next_action']}`

## Boundary(경계)

- training(학습): `not_run`
- candidate_selection(후보 선택): `not_run`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime authority(런타임 권위): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

Claim boundary(주장 경계): `{final['claim_boundary']}`
"""
    return aw.write_text_lossless(REPORT_PATH, text, True)


def write_decision_doc(final: Mapping[str, Any]) -> Path:
    text = f"""# Decision: Stage337 run337BP Live-Computable Feature Frame Preflight(결정: 337단계 337BP 실시간 계산 가능 피처 프레임 사전점검)

- date(날짜): {TODAY}
- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(상위 실행 ID): `{PARENT_RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- gates(게이트): `{final['passed_gates']}/{final['gate_rows']}`

Effect(효과): 최신 전진 원천으로 피처 프레임은 생성됐고, as-of join(시점 기준 결합)과 MT5 parity(MT5 동등성)를 다음 패키지로 보낸다.

Claim boundary(주장 경계): `{final['claim_boundary']}`
"""
    return aw.write_text_lossless(DECISION_DOC, text, True)


def update_docs(final: Mapping[str, Any]) -> list[Path]:
    artifacts: list[Path] = []
    workspace_text, workspace_bom = aw.read_text_lossless(WORKSPACE_STATE)
    workspace = bg.remove_workspace_focus_block(workspace_text, "Stage337 run337BP focus")
    workspace = bg.replace_top_value(workspace, "current_run_id: ", NEXT_RUN_ID)
    focus = (
        "- >-\n"
        "  Stage337 run337BP focus complete: live-computable feature frame preflight"
        "(실시간 계산 가능 피처 프레임 사전점검)를 완료했다. Effect(효과): "
        "3개 feature frame(피처 프레임)을 생성했고, exact/as-of join gap"
        "(정확/시점 기준 결합 공백)과 Python-MT5 parity(파이썬-MT5 동등성)를 run337BQ(337BQ 실행)로 넘긴다.\n"
    )
    workspace = workspace.replace("current_focus:\n", "current_focus:\n" + focus, 1)
    artifacts.append(aw.write_text_lossless(WORKSPACE_STATE, workspace, workspace_bom))

    current_text, current_bom = aw.read_text_lossless(CURRENT_STATE)
    current = bg.remove_markdown_section(current_text, "## Stage337 run337BP(337BP 실행)")
    replacements = {
        "- current_run(현재 실행): ": f"`{NEXT_RUN_ID}`",
        "- status(상태): ": f"`{final['status']}`",
        "- decision(결정): ": f"`{final['decision']}`",
        "- latest_completed_run(최근 완료 실행): ": f"`{RUN_ID}`",
        "- next_action(다음 행동): ": f"`{NEXT_RUN_ID}`",
        "- claim_boundary(주장 경계): ": f"`{CLAIM_BOUNDARY}`",
    }
    for prefix, value in replacements.items():
        current = bg.replace_top_value(current, prefix, value)
    entry = f"""
## Stage337 run337BP(337BP 실행) - {TODAY}

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- effect(효과): run337BP(337BP 실행)는 최신 raw M5(원천 M5)에서 3개 피처 프레임을 생성했다. exact join(정확 결합) 기반이므로 as-of join(시점 기준 결합)과 MT5 동등성은 run337BQ(337BQ 실행)에서 닫는다. 학습/선택/전진 통과/목표 달성은 주장하지 않는다.
"""
    current = current.replace("## Stage337 run337BO(337BO 실행)", entry + "\n## Stage337 run337BO(337BO 실행)", 1)
    artifacts.append(aw.write_text_lossless(CURRENT_STATE, current, current_bom))

    selection_text = f"""# Stage337 Selection Status(337단계 선택 상태)

- latest_run(최신 실행): `{RUN_ID}`
- latest_decision(최신 결정): `{final['decision']}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- frozen_subject(고정 대상): `cp322A_cp321b_exact_replay_control_surface`
- exact_cp322a_forward_handoff(정확 cp322A 전진 인계): `not_feasible_under_frozen_rules`
- preserved_status(보존 상태): `research_artifact_only`
- rebuild_status(재구축 상태): `feature_preflight_materialized_asof_gap_open`
- actual_mt5_execution(실제 MT5 실행): `not_run_python_feature_preflight_only`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): 다음은 시점 기준 결합과 런타임 동등성 패키지다.
"""
    artifacts.append(aw.write_text_lossless(SELECTED_STATUS, selection_text, True))

    stage_text, stage_bom = aw.read_text_lossless(STAGE_BRIEF)
    stage_text = (
        stage_text.rstrip()
        + f"\n- {TODAY}: run337BP(337BP 실행) materialized live-computable feature frames(실시간 계산 가능 피처 프레임) and opened run337BQ(337BQ 실행) as-of join/runtime parity(시점 기준 결합/런타임 동등성). Forward/Goal(전진/목표)은 주장하지 않는다.\n"
    )
    artifacts.append(aw.write_text_lossless(STAGE_BRIEF, stage_text, stage_bom))

    changelog_text, changelog_bom = aw.read_text_lossless(CHANGELOG)
    changelog_text = (
        changelog_text.rstrip()
        + f"\n- {TODAY}: Stage337 run337BP built live-computable feature frame preflight(실시간 계산 가능 피처 프레임 사전점검) and opened as-of/runtime parity package(시점 기준/런타임 동등성 패키지).\n"
    )
    artifacts.append(aw.write_text_lossless(CHANGELOG, changelog_text, changelog_bom))
    return artifacts


def update_registers(final: Mapping[str, Any]) -> list[Path]:
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "live_computable_feature_frame_preflight_without_db",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": aw.rel(REPORT_PATH),
        "notes": f"decision={final['decision']};next_action={final['next_action']};gates={final['passed_gates']}/{final['gate_rows']};goal_achieve_not_claimed.",
        "work_family": "experiment_execution",
        "primary_artifact": aw.rel(REPORT_PATH),
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__feature_frame_preflight",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "feature_frame_preflight",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "Stage337 run337BP live-computable feature frame preflight",
        "tier_scope": "feature_preflight_no_trading_kpi",
        "kpi_scope": "no_new_trading_kpi",
        "scoreboard_lane": "experiment_execution",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": aw.rel(REPORT_PATH),
        "primary_kpi": f"feature_sets={final['materialized_feature_sets']};latest={final['latest_feature_timestamp']}",
        "guardrail_kpi": "no_training;no_selection;no_forward_claim;no_goal_achieve",
        "external_verification_status": "python_feature_preflight_only_mt5_parity_pending(파이썬 피처 사전점검, MT5 동등성 대기)",
        "notes": f"next_action={final['next_action']};asof_gap_rows={final['asof_gap_rows']}",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__feature_frame_preflight",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "experiment_execution",
        "evidence_scope": "fresh raw M5 to Python feature frame preflight",
        "kpi_scope": "feature_materialization_no_trading_kpi",
        "status": final["status"],
        "judgment": final["judgment"],
        "claim_boundary": CLAIM_BOUNDARY,
        "path": aw.rel(REPORT_PATH),
        "notes": "goal_achieve_not_claimed;forward_passed_not_claimed;training_not_run",
        "decision": final["decision"],
        "run_key": f"{RUN_ID}__feature_frame_preflight",
        "family": "live_computable_feature_frame_preflight_without_db",
        "question": "can fresh forward raw inputs produce feature frames and parity package inputs",
        "metric_scope": "feature_rows_alignment_missing_asof_gap_firewall",
        "primary_artifact": aw.rel(REPORT_PATH),
        "report_path": aw.rel(REPORT_PATH),
        "next_action": final["next_action"],
    }
    aw.upsert_csv(RUN_REGISTRY, aw.RUN_REGISTRY_COLUMNS, run_row, "run_id")
    aw.upsert_csv(ALPHA_LEDGER, aw.ALPHA_LEDGER_COLUMNS, alpha_row, "ledger_row_id")
    aw.upsert_csv(STAGE_LEDGER, aw.STAGE_LEDGER_COLUMNS, stage_row, "ledger_row_id")
    return [RUN_REGISTRY, ALPHA_LEDGER, STAGE_LEDGER]


def update_artifact_registry(paths: Sequence[Path], final: Mapping[str, Any]) -> Path:
    columns, rows = aw.read_csv_table(ARTIFACT_REGISTRY, prefer_head=False)
    columns = columns or list(aw.ARTIFACT_COLUMNS)
    rows = [row for row in rows if not str(row.get("artifact_id", "")).startswith(f"{RUN_ID}::")]
    created_at = now_utc()
    seen: set[str] = set()
    for path in paths:
        if not aw.path_exists(path):
            continue
        artifact_path = aw.rel(path)
        if artifact_path in seen:
            continue
        seen.add(artifact_path)
        rows.append(
            {
                "artifact_id": f"{RUN_ID}::{artifact_path}",
                "artifact_type": path.suffix.lower().lstrip(".") or "file",
                "path": artifact_path,
                "sha256": aw.sha256_file(path),
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": created_at,
                "notes": final["status"],
                "artifact_path": artifact_path,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return aw.write_csv(ARTIFACT_REGISTRY, columns, rows)


def main() -> int:
    aw.io_path(RUN_DIR).mkdir(parents=True, exist_ok=True)
    src = load_inputs()
    us100_last_close = str(src["bo_final"].get("us100_last_close_utc", ""))
    summaries, missing_rows, invalid_rows, frame_artifacts, foundation_counts = materialize_feature_preflight(us100_last_close)
    basic_paths = write_basic_artifacts(summaries, missing_rows, invalid_rows)
    lane_rows = build_lane_bridge(src, summaries)
    lane_path = aw.write_csv(FEATURE_LANE_BRIDGE, LANE_BRIDGE_COLUMNS, lane_rows)
    asof_rows = build_asof_gap_review(summaries)
    asof_path = aw.write_csv(EXACT_ASOF_GAP_REVIEW, ASOF_GAP_COLUMNS, asof_rows)
    firewall_rows = build_feature_firewall(summaries)
    firewall_path = aw.write_csv(FEATURE_FIREWALL, FIREWALL_COLUMNS, firewall_rows)
    parity_rows = build_parity_matrix(summaries)
    parity_path = aw.write_csv(PARITY_HANDOFF_MATRIX, PARITY_COLUMNS, parity_rows)
    queue_rows = build_queue(asof_rows, parity_rows)
    queue_path = aw.write_csv(RUN337BQ_QUEUE, QUEUE_COLUMNS, queue_rows)
    gate_rows = build_gates(src, summaries, lane_rows, asof_rows, firewall_rows, parity_rows, queue_rows)
    gate_path = aw.write_csv(REQUIRED_GATE_AUDIT, GATE_COLUMNS, gate_rows)
    all_gates_pass = all(row.get("status") == "passed" for row in gate_rows)
    materialized = [row for row in summaries if row.get("status") == "materialized"]
    latest_feature_timestamp = max((str(row.get("last_valid_timestamp", "")) for row in materialized), default="")
    asof_gap_rows = sum(1 for row in asof_rows if row.get("gap_status") == "gap_open_asof_join_required")
    final = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS if all_gates_pass else "invalid_stage337BP_feature_preflight_gate_failure",
        "judgment": JUDGMENT if all_gates_pass else "live_computable_feature_frame_preflight_gate_failure",
        "decision": DECISION if all_gates_pass else "repair_stage337BP_feature_preflight_before_asof_runtime_package",
        "next_action": NEXT_RUN_ID if all_gates_pass else "repair_stage337BP_feature_preflight_gate_failure_v1",
        "feature_window_end_utc": us100_last_close,
        "feature_set_rows": len(summaries),
        "materialized_feature_sets": len(materialized),
        "latest_feature_timestamp": latest_feature_timestamp,
        "asof_gap_rows": asof_gap_rows,
        "firewall_rows": len(firewall_rows),
        "parity_rows": len(parity_rows),
        "gate_rows": len(gate_rows),
        "passed_gates": count_passed(gate_rows),
        "failed_gates": [row.get("gate_id") for row in gate_rows if row.get("status") != "passed"],
        "training": "not_run",
        "candidate_selection": "not_run",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "runtime_authority": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    final_path = aw.write_json(FINAL_DECISION, final)
    manifest = {
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "stage_id": STAGE_ID,
        "status": final["status"],
        "inputs": [aw.rel(path) for path in INPUT_FILES],
        "outputs": [aw.rel(path) for path in OUTPUT_FILES],
        "frame_artifacts": [aw.rel(path) for path in frame_artifacts],
        "no_training": True,
        "no_selection": True,
        "generated_at_utc": now_utc(),
        "claim_boundary": CLAIM_BOUNDARY,
    }
    manifest_path = aw.write_json(RUN_MANIFEST, manifest)
    receipt_paths = build_receipts(final, foundation_counts)
    report_path = write_report(final)
    decision_path = write_decision_doc(final)
    doc_paths = update_docs(final) if all_gates_pass else []
    register_paths = update_registers(final) if all_gates_pass else []
    artifact_inputs = [
        *frame_artifacts,
        *basic_paths,
        lane_path,
        asof_path,
        firewall_path,
        parity_path,
        queue_path,
        gate_path,
        final_path,
        manifest_path,
        *receipt_paths,
        report_path,
        decision_path,
        *doc_paths,
        *register_paths,
    ]
    artifact_registry_path = update_artifact_registry(artifact_inputs, final)
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": final["status"],
                "decision": final["decision"],
                "next_action": final["next_action"],
                "materialized_feature_sets": final["materialized_feature_sets"],
                "latest_feature_timestamp": final["latest_feature_timestamp"],
                "asof_gap_rows": final["asof_gap_rows"],
                "passed_gates": final["passed_gates"],
                "gate_rows": final["gate_rows"],
                "artifact_registry": aw.rel(artifact_registry_path),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if all_gates_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
