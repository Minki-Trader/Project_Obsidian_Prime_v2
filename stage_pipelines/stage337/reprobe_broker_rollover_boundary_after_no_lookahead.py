# -*- coding: utf-8 -*-
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, path_exists  # noqa: E402
from foundation.mt5 import runtime_support as mt5  # noqa: E402
from foundation.mt5.runtime_artifacts import sha256_file  # noqa: E402
from stage_pipelines.stage335 import independent_proxy_mt5_probe as base  # noqa: E402
from stage_pipelines.stage337 import probe_custom_symbol_intraday_tester_visibility as ab  # noqa: E402
from stage_pipelines.stage337 import reprobe_next_rollover_or_synthetic_custom_parity_repair as ak  # noqa: E402
from stage_pipelines.stage337 import review_runtime_data_and_feature_source_repair_probe as qprobe  # noqa: E402


TODAY = "2026-05-27"
STAGE_ID = "337_onnx_research_packet__cost_buffer_direction_curve_rebuild"
RUN_NUMBER = "run337AN"
RUN_ID = "run337AN_broker_rollover_reprobe_when_utc_day_boundary_available_v1"
PARENT_RUN_ID = "run337AM_no_lookahead_cost_direction_curve_rebuild_input_materialization_v1"
SOURCE_IDENTITY_RUN_ID = "run337AK_next_rollover_or_synthetic_custom_parity_repair_v1"
NEXT_RUN_ID_ASOF = "run337AO_asof_regime_and_db_source_materialization_v1"
NEXT_RUN_ID_ATTRIBUTION = "run337AP_broker_boundary_attribution_cost_stress_v1"
NEXT_RUN_ID_REPAIR = "run337AP_broker_tester_history_repair_or_next_rollover_v1"
NEXT_RUN_ID_RUNTIME_REPAIR = "run337AP_broker_runtime_repair_reprobe_v1"
CLAIM_BOUNDARY = (
    "research_development_only_stage337AN_broker_rollover_reprobe_no_model_training_"
    "no_threshold_retuning_no_lot_optimization_no_candidate_selection_no_forward_passed_"
    "no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)

STATUS_REACHED = "completed_stage337AN_broker_reached_feature_last_exact_proxy_parity_no_forward_decision"
STATUS_GAP_REMAINS = "completed_stage337AN_broker_rollover_reprobe_gap_remains_no_forward_decision"
STATUS_RUNTIME_ISSUE = "completed_stage337AN_broker_rollover_reprobe_runtime_issue_no_forward_decision"
STATUS_PROXY_MISMATCH = "completed_stage337AN_broker_exact_proxy_mismatch_no_forward_decision"
STATUS_MATERIALIZED = "completed_stage337AN_broker_rollover_reprobe_materialized_only_no_forward_decision"
JUDGMENT_REACHED = "broker_tester_feature_last_reached_but_attribution_cost_and_regime_review_still_required"
JUDGMENT_GAP_REMAINS = "broker_tester_feature_last_gap_remains_proxy_runtime_signal_parity_only"
JUDGMENT_RUNTIME_ISSUE = "broker_runtime_reprobe_incomplete_forward_decision_blocked_by_execution_evidence"
JUDGMENT_PROXY_MISMATCH = "broker_exact_timestamp_proxy_does_not_match_mt5_runtime"
JUDGMENT_MATERIALIZED = "broker_rollover_reprobe_inputs_materialized_execution_pending"
DECISION_REACHED = "stage337AN_open_run337AO_asof_regime_db_and_run337AP_attribution_cost_stress_no_selection"
DECISION_GAP_REMAINS = "stage337AN_open_run337AO_asof_regime_db_and_run337AP_broker_history_repair_no_selection"
DECISION_RUNTIME_ISSUE = "stage337AN_open_run337AP_broker_runtime_repair_no_selection"
DECISION_PROXY_MISMATCH = "stage337AN_open_run337AP_proxy_runtime_mismatch_repair_no_selection"
DECISION_MATERIALIZED = "stage337AN_execution_pending_no_selection"

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
RUN337AK_DIR = STAGE_DIR / "02_runs" / "run337AK"
RUN337AK_ATTEMPTS = RUN337AK_DIR / "handoff_attempts.json"
RUN337AM_DIR = STAGE_DIR / "02_runs" / "run337AM"
RUN337AM_FINAL = RUN337AM_DIR / "final_decision.json"
RUN337AM_GUARD = RUN337AM_DIR / "broker_rollover_guard.csv"
MT5_DIR = RUN_DIR / "mt5"
FEATURE_COPY_DIR = RUN_DIR / "feature_matrices"
MODEL_COPY_DIR = RUN_DIR / "models"
TELEMETRY_DIR = RUN_DIR / "runtime_telemetry"
REVIEWS_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEWS_DIR / "run337AN_broker_rollover_reprobe.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-27_stage337AN_broker_rollover_reprobe.md"
SELECTED_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
STAGE_LEDGER = REVIEWS_DIR / "stage_run_ledger.csv"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"

DEFAULT_PORTABLE_ROOT = Path(r"C:\Users\awdse\AppData\Local\ObsidianPrime\mt5_portable_run329E")
DEFAULT_TERMINAL = DEFAULT_PORTABLE_ROOT / "terminal64.exe"
DEFAULT_METAEDITOR = DEFAULT_PORTABLE_ROOT / "MetaEditor64.exe"
DEFAULT_COMMON_FILES = DEFAULT_PORTABLE_ROOT / "Common" / "Files"
DEFAULT_TESTER_PROFILE_ROOT = DEFAULT_PORTABLE_ROOT / "MQL5" / "Profiles" / "Tester"
DEFAULT_TERMINAL_DATA_ROOT = DEFAULT_PORTABLE_ROOT
LOG_DATE = TODAY.replace("-", "")
TESTER_LOG = DEFAULT_PORTABLE_ROOT / "Tester" / "logs" / f"{LOG_DATE}.log"
TESTER_AGENT_LOG = DEFAULT_PORTABLE_ROOT / "Tester" / "Agent-127.0.0.1-3000" / "logs" / f"{LOG_DATE}.log"
TERMINAL_LOG = DEFAULT_PORTABLE_ROOT / "Logs" / f"{LOG_DATE}.log"
COMMON_ROOT = "Project_Obsidian_Prime_v2/stage337/run337AN_broker_rollover_reprobe"
ORIGIN_SYMBOL = "US100"
BROKER_FROM_DATE = "2026.04.14"
BROKER_TO_DATE = "2026.05.30"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Stage337AN broker rollover reprobe after no-lookahead input lock.")
    parser.add_argument("--terminal", default=str(DEFAULT_TERMINAL))
    parser.add_argument("--metaeditor", default=str(DEFAULT_METAEDITOR))
    parser.add_argument("--common-files-root", default=str(DEFAULT_COMMON_FILES))
    parser.add_argument("--tester-profile-root", default=str(DEFAULT_TESTER_PROFILE_ROOT))
    parser.add_argument("--terminal-data-root", default=str(DEFAULT_TERMINAL_DATA_ROOT))
    parser.add_argument("--timeout-seconds", type=int, default=1200)
    parser.add_argument("--wait-timeout-seconds", type=int, default=240)
    parser.add_argument("--materialize-only", action="store_true")
    return parser.parse_args()


def rel(path: Path | str) -> str:
    return ak.rel(path)


def now_utc() -> str:
    return datetime.now(tz=UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def truthy(value: Any) -> bool:
    return value is True or str(value).lower() == "true"


def configure_probe_modules() -> None:
    for module in (base, qprobe, ab, ak):
        module.TODAY = TODAY
        module.STAGE_ID = STAGE_ID
        module.RUN_NUMBER = RUN_NUMBER
        module.RUN_ID = RUN_ID
        module.PARENT_RUN_ID = PARENT_RUN_ID
        module.CLAIM_BOUNDARY = CLAIM_BOUNDARY
        module.RUN_DIR = RUN_DIR
        module.MT5_DIR = MT5_DIR
        module.FEATURE_COPY_DIR = FEATURE_COPY_DIR
        module.MODEL_COPY_DIR = MODEL_COPY_DIR
        module.TELEMETRY_DIR = TELEMETRY_DIR
        module.DEFAULT_PORTABLE_ROOT = DEFAULT_PORTABLE_ROOT
        module.DEFAULT_TERMINAL = DEFAULT_TERMINAL
        module.DEFAULT_METAEDITOR = DEFAULT_METAEDITOR
        module.DEFAULT_COMMON_FILES = DEFAULT_COMMON_FILES
        module.DEFAULT_TESTER_PROFILE_ROOT = DEFAULT_TESTER_PROFILE_ROOT
        module.DEFAULT_TERMINAL_DATA_ROOT = DEFAULT_TERMINAL_DATA_ROOT
        module.TESTER_LOG = TESTER_LOG
        module.TESTER_AGENT_LOG = TESTER_AGENT_LOG
        module.TERMINAL_LOG = TERMINAL_LOG
        module.COMMON_ROOT = COMMON_ROOT
    base.STAGE_DIR = STAGE_DIR
    base.REVIEWS_DIR = REVIEWS_DIR
    base.PORTABLE_EA_SOURCE = DEFAULT_PORTABLE_ROOT / "MQL5" / "Experts" / mt5.EA_SOURCE_PATH
    base.PORTABLE_EA_EX5 = (
        DEFAULT_PORTABLE_ROOT
        / "MQL5"
        / "Experts"
        / "Project_Obsidian_Prime_v2"
        / "foundation"
        / "mt5"
        / "ObsidianPrimeV2_RuntimeProbeEA.ex5"
    )
    ak.REPORT_PATH = REPORT_PATH
    ak.DECISION_DOC = DECISION_DOC
    ak.ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"


def load_source_broker_attempt() -> dict[str, Any]:
    attempts = ak.read_json(RUN337AK_ATTEMPTS)
    source = next(
        (
            dict(row)
            for row in attempts
            if row.get("scenario_symbol") == ORIGIN_SYMBOL and "broker_rollover_control" in str(row.get("attempt_name", ""))
        ),
        None,
    )
    if source is None:
        raise RuntimeError(f"missing broker source attempt in {RUN337AK_ATTEMPTS}")
    return source


def build_broker_source_attempt(source: Mapping[str, Any]) -> dict[str, Any]:
    copied = dict(source)
    copied["attempt_name"] = "u42_plain_rf_an_broker_rollover_reprobe"
    copied["artifact_slug"] = "u42_plain_an_broker_rollover_reprobe"
    copied["scenario_id"] = "broker_rollover_reprobe_after_no_lookahead_lock"
    copied["scenario_symbol"] = ORIGIN_SYMBOL
    copied["scenario_from_date"] = BROKER_FROM_DATE
    copied["scenario_to_date"] = BROKER_TO_DATE
    copied["scenario_model"] = "4"
    copied["scenario_role"] = "broker control(브로커 대조군): original timestamp(원래 시각), real ticks(실제 틱)"
    copied["model_copy"] = {"source": source.get("model_local_path") or source.get("model_copy", {}).get("source", "")}
    copied["feature_export"] = {"path": source.get("feature_local_path", "")}
    copied["source_attempt_name"] = source.get("attempt_name", "")
    copied["source_run_id"] = PARENT_RUN_ID
    copied["source_identity_run_id"] = SOURCE_IDENTITY_RUN_ID
    copied["attempt_role"] = "stage337AN_broker_rollover_reprobe_same_frozen_u42_model_threshold_risk"
    copied["record_view_prefix"] = "mt5_stage337AN_u42_plain_broker_rollover_reprobe"
    return copied


def rewrite_attempt_to_broker_scenario(attempt: dict[str, Any]) -> dict[str, Any]:
    tester = dict(attempt["ini"]["tester"])
    tester["Symbol"] = ORIGIN_SYMBOL
    tester["FromDate"] = BROKER_FROM_DATE
    tester["ToDate"] = BROKER_TO_DATE
    tester["Model"] = "4"
    tester["Report"] = f"Project_Obsidian_Prime_v2_{RUN_ID}_{attempt['attempt_name']}"
    attempt["ini"] = base.materialize_ini_file(tester, Path(str(attempt["ini"]["path"])))
    attempt["from_date"] = tester["FromDate"]
    attempt["to_date"] = tester["ToDate"]
    attempt["tester_symbol"] = tester["Symbol"]
    attempt["tester_model"] = tester["Model"]
    attempt["scenario_id"] = "broker_rollover_reprobe_after_no_lookahead_lock"
    attempt["scenario_symbol"] = ORIGIN_SYMBOL
    attempt["scenario_from_date"] = BROKER_FROM_DATE
    attempt["scenario_to_date"] = BROKER_TO_DATE
    attempt["scenario_model"] = "4"
    attempt["source_run_id"] = PARENT_RUN_ID
    attempt["source_identity_run_id"] = SOURCE_IDENTITY_RUN_ID
    attempt["attempt_role"] = "stage337AN_broker_rollover_reprobe_same_frozen_u42_model_threshold_risk"
    attempt["record_view_prefix"] = f"mt5_stage337AN_{attempt['artifact_slug']}"
    attempt["repair_contract"] = (
        "Only tester rerun timing and artifact identity change. ONNX(온엑스), feature order(피처 순서), "
        "D/B surface(D/B 판단 표면), score threshold(점수 임계값), risk(위험), lot(랏), ATR SL/TP(ATR 손절/익절)는 고정한다."
    )
    attempt["signal_policy"] = "exact tester-cycle timestamp proxy(정확 테스터 주기 시각 프록시)는 runtime signal parity(런타임 신호 동등성)에만 사용한다."
    return attempt


def runtime_completed(row: Mapping[str, Any]) -> bool:
    return (
        str(row.get("tester_status", "")) == "completed"
        and str(row.get("runtime_status", "")) == "completed"
        and str(row.get("report_status", "")) == "completed"
    )


def matched_count(diff_rows: Sequence[Mapping[str, Any]]) -> int:
    return sum(1 for row in diff_rows if truthy(row.get("usable_for_runtime_signal_parity")))


def broker_gap_row(gap_rows: Sequence[Mapping[str, Any]]) -> Mapping[str, Any]:
    return next((row for row in gap_rows if "broker_rollover_reprobe" in str(row.get("attempt_name", ""))), gap_rows[0] if gap_rows else {})


def classify(
    runtime_rows: Sequence[Mapping[str, Any]],
    gap_rows: Sequence[Mapping[str, Any]],
    diff_rows: Sequence[Mapping[str, Any]],
    materialize_only: bool,
) -> tuple[str, str, str, str, str]:
    if materialize_only:
        return STATUS_MATERIALIZED, JUDGMENT_MATERIALIZED, DECISION_MATERIALIZED, RUN_ID, NEXT_RUN_ID_ASOF
    if not runtime_rows or any(not runtime_completed(row) for row in runtime_rows):
        return STATUS_RUNTIME_ISSUE, JUDGMENT_RUNTIME_ISSUE, DECISION_RUNTIME_ISSUE, NEXT_RUN_ID_RUNTIME_REPAIR, NEXT_RUN_ID_ASOF
    matched = matched_count(diff_rows)
    gap_status = broker_gap_row(gap_rows).get("gap_status", "")
    if matched != len(diff_rows) or not diff_rows:
        return STATUS_PROXY_MISMATCH, JUDGMENT_PROXY_MISMATCH, DECISION_PROXY_MISMATCH, NEXT_RUN_ID_REPAIR, NEXT_RUN_ID_ASOF
    if gap_status == "tester_reached_feature_last":
        return STATUS_REACHED, JUDGMENT_REACHED, DECISION_REACHED, NEXT_RUN_ID_ASOF, NEXT_RUN_ID_ATTRIBUTION
    return STATUS_GAP_REMAINS, JUDGMENT_GAP_REMAINS, DECISION_GAP_REMAINS, NEXT_RUN_ID_ASOF, NEXT_RUN_ID_REPAIR


def annotate_gap_rows(gap_rows: Sequence[Mapping[str, Any]], boundary_rows: Sequence[Mapping[str, Any]], attempts: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    boundary_by = {row.get("attempt_name"): row for row in boundary_rows}
    attempt_by = {row.get("attempt_name"): row for row in attempts}
    cleaned: list[dict[str, Any]] = []
    for row in gap_rows:
        item = dict(row)
        boundary = boundary_by.get(item.get("attempt_name"), {})
        attempt = attempt_by.get(item.get("attempt_name"), {})
        item["scenario_id"] = attempt.get("scenario_id", "")
        item["tester_symbol"] = attempt.get("tester_symbol", "")
        item["tester_model"] = attempt.get("tester_model", "")
        item["log_test_from"] = boundary.get("log_test_from", "")
        item["log_test_to"] = boundary.get("log_test_to", "")
        item["claim_boundary"] = CLAIM_BOUNDARY
        cleaned.append(item)
    return cleaned


def sanitize_window_rows(rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    cleaned: list[dict[str, Any]] = []
    for row in rows:
        item = dict(row)
        item["effect"] = (
            "continuous window(연속 구간)와 exact tester cycle(정확 테스터 주기)을 분리한다. "
            "효과(effect, 효과): proxy(프록시) 과대계산 여부를 확인한다."
        )
        item["claim_boundary"] = CLAIM_BOUNDARY
        cleaned.append(item)
    return cleaned


def sanitize_proxy_rows(rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    cleaned: list[dict[str, Any]] = []
    for row in rows:
        item = dict(row)
        item["threshold_policy"] = "frozen_source_set_min_margin_no_search(고정 원천 설정 최소 마진, 탐색 없음)"
        item["proxy_source"] = str(item.get("proxy_source", "")).replace("stage337AK", "stage337AN")
        item["claim_boundary"] = CLAIM_BOUNDARY
        cleaned.append(item)
    return cleaned


def sanitize_diff_rows(rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    cleaned: list[dict[str, Any]] = []
    for row in rows:
        item = dict(row)
        item["mt5_source"] = "stage337AN_runtime_summary_exact_tester_cycle(337AN 정확 테스터 주기 런타임 요약)"
        item["usable_for_forward_pass_fail"] = False
        item["claim_boundary"] = CLAIM_BOUNDARY
        cleaned.append(item)
    return cleaned


def build_proxy_usability_rows(gap_rows: Sequence[Mapping[str, Any]], diff_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    gap = broker_gap_row(gap_rows)
    matched = matched_count(diff_rows)
    total = len(diff_rows)
    forward_ok = gap.get("gap_status") == "tester_reached_feature_last" and matched == total and total > 0
    return [
        {
            "attempt_name": gap.get("attempt_name", "u42_plain_rf_an_broker_rollover_reprobe"),
            "gap_status": gap.get("gap_status", ""),
            "proxy_matched": matched,
            "proxy_total": total,
            "diagnostic_usability": "usable_for_runtime_signal_parity" if matched == total and total > 0 else "not_usable_until_proxy_mt5_mismatch_repaired",
            "forward_usability": (
                "usable_as_broker_boundary_input_not_final_forward_decision"
                if forward_ok
                else "not_usable_for_forward_pass_fail_until_broker_tester_reaches_feature_last"
            ),
            "effect": (
                "proxy expected(프록시 예상값)와 MT5 runtime(메타트레이더5 런타임)을 비교한다. "
                "효과(effect, 효과): 신호 동등성은 보되 forward decision(전진 판정)은 별도 조건으로 남긴다."
            ),
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def build_input_evidence_rows(source: Mapping[str, Any], handoff_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    first_handoff = handoff_rows[0] if handoff_rows else {}
    return [
        {
            "evidence_id": "parent_run337AM_final_decision",
            "path": rel(RUN337AM_FINAL),
            "status": "available" if path_exists(RUN337AM_FINAL) else "missing",
            "effect": "no-lookahead input lock(미래참조 방지 입력 잠금)을 부모 근거로 묶는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "evidence_id": "parent_run337AM_broker_rollover_guard",
            "path": rel(RUN337AM_GUARD),
            "status": "available" if path_exists(RUN337AM_GUARD) else "missing",
            "effect": "이전 tester feature_last(테스터 피처 끝) 실패 조건을 재탐침 조건으로 묶는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "evidence_id": "source_run337AK_broker_attempt",
            "path": rel(RUN337AK_ATTEMPTS),
            "status": "available",
            "attempt_name": source.get("attempt_name", ""),
            "effect": "고정 ONNX(온엑스)와 설정(set, 설정) 정체성을 이어받는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "evidence_id": "new_handoff_identity",
            "path": rel(RUN_DIR / "handoff_attempts.csv"),
            "status": first_handoff.get("materialization_status", ""),
            "model_sha256": first_handoff.get("model_sha256", ""),
            "feature_sha256": first_handoff.get("feature_sha256", ""),
            "effect": "파일 경로만 새 실행으로 격리하고 모델/피처 해시(hash, 해시)를 기록한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_gate_rows(
    runtime_rows: Sequence[Mapping[str, Any]],
    gap_rows: Sequence[Mapping[str, Any]],
    diff_rows: Sequence[Mapping[str, Any]],
    handoff_rows: Sequence[Mapping[str, Any]],
    materialize_only: bool,
) -> list[dict[str, Any]]:
    gap = broker_gap_row(gap_rows)
    matched = matched_count(diff_rows)
    no_retune = bool(handoff_rows) and all(
        truthy(row.get("threshold_keys_unchanged")) and truthy(row.get("risk_lot_keys_unchanged")) for row in handoff_rows
    )
    runtime_ok = bool(runtime_rows) and all(runtime_completed(row) for row in runtime_rows)
    return [
        {
            "gate_id": "source_identity_loaded",
            "status": "passed" if path_exists(RUN337AK_ATTEMPTS) else "failed",
            "evidence_path": rel(RUN337AK_ATTEMPTS),
            "effect": "run337AK 브로커 원천 시도를 재사용한다. 효과(effect, 효과): 새 후보 생성을 막는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "no_retune_identity_guard",
            "status": "passed" if no_retune else "failed",
            "evidence_path": rel(RUN_DIR / "handoff_attempts.csv"),
            "effect": "threshold/risk/lot(임계값/위험/랏) 변경이 없는지 확인한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "mt5_runtime_completed",
            "status": "not_attempted_materialize_only" if materialize_only else ("passed" if runtime_ok else "failed"),
            "evidence_path": rel(RUN_DIR / "runtime_summary.csv"),
            "effect": "Strategy Tester(전략 테스터)와 telemetry(원격 측정)가 모두 생겼는지 확인한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "broker_tester_reached_feature_last",
            "status": "passed" if gap.get("gap_status") == "tester_reached_feature_last" else "failed",
            "evidence_path": rel(RUN_DIR / "tester_feature_last_gap_reprobe.csv"),
            "effect": "브로커 tester(테스터)가 feature_last(피처 끝)에 닿았는지 확인한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "exact_timestamp_proxy_mt5_parity",
            "status": "passed" if matched == len(diff_rows) and diff_rows else "failed",
            "evidence_path": rel(RUN_DIR / "exact_timestamp_proxy_mt5_difference.csv"),
            "effect": "proxy expected(프록시 예상값)와 MT5 runtime(런타임) 신호 수가 같은지 확인한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "forward_claim_boundary",
            "status": "passed",
            "evidence_path": rel(RUN_DIR / "final_decision.json"),
            "effect": "Forward Passed/Failed(전진 통과/실패)와 Goal Achieve(목표 달성)를 주장하지 않게 잠근다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def decision_payload(
    status: str,
    judgment: str,
    decision: str,
    next_action: str,
    secondary_next_action: str,
    api_row: Mapping[str, Any],
    runtime_rows: Sequence[Mapping[str, Any]],
    gap_rows: Sequence[Mapping[str, Any]],
    diff_rows: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    gap = broker_gap_row(gap_rows)
    matched = matched_count(diff_rows)
    runtime_ok = sum(1 for row in runtime_rows if runtime_completed(row))
    broker_boundary = (
        "repaired_feature_last_visibility_pending_attribution"
        if gap.get("gap_status") == "tester_reached_feature_last"
        else "failed"
    )
    forward_blocked = (
        "not_blocked_by_feature_last_but_not_forward_decision"
        if broker_boundary.startswith("repaired")
        else "broker_tester_feature_last_not_reached"
    )
    if status == STATUS_RUNTIME_ISSUE:
        forward_blocked = "broker_runtime_reprobe_incomplete"
    return {
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "source_identity_run_id": SOURCE_IDENTITY_RUN_ID,
        "stage_id": STAGE_ID,
        "status": status,
        "judgment": judgment,
        "decision": decision,
        "next_action": next_action,
        "secondary_next_action": secondary_next_action,
        "runtime_completed": runtime_ok,
        "runtime_total": len(runtime_rows),
        "proxy_mt5_matched": matched,
        "proxy_mt5_rows": len(diff_rows),
        "broker_gap_status": gap.get("gap_status", ""),
        "broker_forward_boundary": broker_boundary,
        "api_latest_us100_close_utc": api_row.get("m5_last_close_utc", ""),
        "feature_last_timestamp": gap.get("feature_last_timestamp", ""),
        "tester_last_observed_bar_time": gap.get("tester_last_observed_bar_time", ""),
        "tester_to_feature_last_gap_minutes": gap.get("tester_to_feature_last_gap_minutes", ""),
        "net_profit": runtime_rows[0].get("net_profit", "") if runtime_rows else "",
        "profit_factor": runtime_rows[0].get("profit_factor", "") if runtime_rows else "",
        "trade_count": runtime_rows[0].get("trade_count", "") if runtime_rows else "",
        "max_drawdown_amount": runtime_rows[0].get("max_drawdown_amount", "") if runtime_rows else "",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "forward_blocked": forward_blocked,
        "runtime_authority": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def receipt_payloads(final: Mapping[str, Any], attempts: Sequence[Mapping[str, Any]], runtime_rows: Sequence[Mapping[str, Any]], gap_rows: Sequence[Mapping[str, Any]]) -> dict[Path, Mapping[str, Any]]:
    runtime_path = rel(attempts[0]["ini"]["path"]) if attempts else rel(MT5_DIR)
    gap = broker_gap_row(gap_rows)
    common = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "status": final["status"],
        "judgment": final["judgment"],
        "claim_boundary": CLAIM_BOUNDARY,
    }
    return {
        RUN_DIR / "data_integrity_receipt.json": {
            **common,
            "receipt_type": "data_integrity",
            "data_source": "US100 M5 broker data(브로커 데이터) through MT5 Strategy Tester(전략 테스터) and frozen u42 feature CSV(고정 u42 피처 CSV)",
            "time_axis": "timestamp_utc(UTC 시각) and MT5 bar_time(메타트레이더5 봉 시각)을 exact tester cycle(정확 테스터 주기) 기준으로 비교",
            "sample_scope": f"{ORIGIN_SYMBOL} M5 {BROKER_FROM_DATE} to {BROKER_TO_DATE}",
            "missing_or_duplicate_check": "tester_feature_last_gap_reprobe.csv에서 feature_last(피처 끝) 도달 여부를 확인",
            "feature_label_boundary": "no new labels(새 라벨 없음), no training(학습 없음), frozen feature order(고정 피처 순서)",
            "split_boundary": "post-OOS forward runtime probe(표본외 이후 전진 런타임 탐침)",
            "leakage_risk": "latest data(최신 데이터)로 threshold(임계값)나 lot(랏)을 맞추는 경로",
            "data_hash_or_identity": attempts[0].get("feature_copy", {}).get("sha256", "") if attempts else "",
            "integrity_judgment": "usable_with_boundary" if gap.get("gap_status") == "tester_reached_feature_last" else "inconclusive",
        },
        RUN_DIR / "runtime_parity_receipt.json": {
            **common,
            "receipt_type": "runtime_parity",
            "research_path": rel(Path(__file__)),
            "runtime_path": runtime_path,
            "shared_contract": "same frozen ONNX(고정 온엑스), feature order(피처 순서), threshold(임계값), risk(위험), lot(랏), ATR SL/TP(ATR 손절/익절)",
            "known_differences": "new run identity(새 실행 정체성) and tester rerun time(테스터 재실행 시점) only",
            "parity_check": f"exact proxy/MT5(정확 프록시/메타트레이더5) {final['proxy_mt5_matched']}/{final['proxy_mt5_rows']}",
            "parity_identity": {"attempts": attempts, "runtime_rows": runtime_rows},
            "runtime_claim_boundary": "runtime_probe(런타임 탐침)",
        },
        RUN_DIR / "backtest_forensics_receipt.json": {
            **common,
            "receipt_type": "backtest_forensics",
            "tester_identity": f"portable MT5(휴대용 메타트레이더5) Strategy Tester(전략 테스터); {ORIGIN_SYMBOL}; M5; model 4(real ticks, 실제 틱); {BROKER_FROM_DATE}-{BROKER_TO_DATE}",
            "ea_identity": "ObsidianPrimeV2_RuntimeProbeEA.ex5 with unchanged frozen u42 handoff(고정 u42 인계)",
            "report_identity": rel(RUN_DIR),
            "trade_evidence": runtime_rows,
            "cost_assumptions": "broker tester costs(브로커 테스터 비용), spread/slippage stress(스프레드/슬리피지 압박)는 다음 attribution(귀속) 실행에서 별도 확인",
            "forensic_checks": ["terminal recovery(터미널 정리)", "tester report(테스터 보고서)", "runtime telemetry(런타임 원격 측정)", "feature_last gap(피처 끝 공백)"],
            "backtest_judgment": "usable_with_boundary" if runtime_rows and all(runtime_completed(row) for row in runtime_rows) else "inconclusive",
        },
        RUN_DIR / "result_judgment_receipt.json": {
            **common,
            "receipt_type": "result_judgment",
            "result_subject": RUN_ID,
            "evidence_available": ["runtime_summary.csv", "tester_feature_last_gap_reprobe.csv", "exact_timestamp_proxy_mt5_difference.csv"],
            "evidence_missing": "final Forward Passed/Failed(전진 통과/실패)는 attribution/cost/regime(귀속/비용/국면) 후에만 가능",
            "judgment_label": "runtime_probe(런타임 탐침)",
            "next_condition": final["secondary_next_action"],
            "user_explanation_hook": "브로커 테스터가 최신 피처 끝을 실제로 봤는지 확인했지만, 운영 권위는 아직 아니다.",
        },
    }


def report_text(final: Mapping[str, Any], gap_rows: Sequence[Mapping[str, Any]], usability: Sequence[Mapping[str, Any]]) -> str:
    gap = broker_gap_row(gap_rows)
    usable = usability[0] if usability else {}
    return f"""# Stage337AN Broker Rollover Reprobe(337AN 브로커 이월 재탐침)

- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- secondary_next_action(보조 다음 행동): `{final['secondary_next_action']}`
- runtime completed(런타임 완료): `{final['runtime_completed']}/{final['runtime_total']}`
- exact proxy/MT5 parity(정확 프록시/메타트레이더5 동등성): `{final['proxy_mt5_matched']}/{final['proxy_mt5_rows']}`
- broker gap(브로커 공백): `{final['broker_gap_status']}`
- broker_forward_boundary(브로커 전진 경계): `{final['broker_forward_boundary']}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## Meaning(의미)

run337AN(337AN 실행)은 run337AM(337AM 실행)의 no-lookahead input lock(미래참조 방지 입력 잠금) 뒤에 브로커 `US100` tester(테스터)가 feature_last(피처 끝)를 보는지 다시 확인했다. 효과(effect, 효과)는 proxy expected(프록시 예상값)를 forward decision(전진 판정)이 아니라 runtime signal parity(런타임 신호 동등성) 근거로만 쓰게 하는 것이다.

## Boundary(경계)

| item(항목) | value(값) |
|---|---:|
| API latest close(API 최신 종가) | `{final['api_latest_us100_close_utc']}` |
| feature last(피처 끝) | `{final['feature_last_timestamp']}` |
| tester last observed(테스터 마지막 관측) | `{final['tester_last_observed_bar_time']}` |
| tester to feature gap minutes(테스터-피처 공백 분) | `{final['tester_to_feature_last_gap_minutes']}` |

## KPI Snapshot(KPI 핵심 지표 스냅샷)

| net profit(순수익) | PF(수익 팩터) | trade count(거래 수) | max DD(최대 손실폭) |
|---:|---:|---:|---:|
| `{final['net_profit']}` | `{final['profit_factor']}` | `{final['trade_count']}` | `{final['max_drawdown_amount']}` |

## Proxy Use(프록시 사용)

| diagnostic usability(진단 사용성) | forward usability(전진 사용성) |
|---|---|
| `{usable.get('diagnostic_usability', '')}` | `{usable.get('forward_usability', '')}` |

## Gate Note(게이트 메모)

- tester gap status(테스터 공백 상태): `{gap.get('gap_status', '')}`
- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
- effect(효과): 이 실행은 모델 학습(model training, 모델 학습), threshold retune(임계값 재조정), lot optimization(랏 최적화), candidate selection(후보 선택), live readiness(실거래 준비), deployment(배포), operating promotion(운영 승격)을 하지 않는다.
"""


def decision_doc_text(final: Mapping[str, Any]) -> str:
    return f"""# 2026-05-27 Stage337AN Broker Rollover Decision(337AN 브로커 이월 결정)

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- secondary_next_action(보조 다음 행동): `{final['secondary_next_action']}`
- selected_candidate(선택 후보): `none`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

Effect(효과): broker tester(브로커 테스터) 가시성을 재검증했다. 이 결과는 forward robustness(전진 강건성) 판정의 입력일 뿐, 운영 권위(runtime authority, 런타임 권위)가 아니다.
"""


def replace_line(text: str, prefix: str, replacement: str) -> str:
    pattern = re.compile(rf"^{re.escape(prefix)}.*$", flags=re.M)
    return pattern.sub(replacement, text, count=1) if pattern.search(text) else replacement + "\n" + text


def upsert_focus_block(text: str, focus: str) -> str:
    block = f"- >-\n  {focus}\n"
    if "current_focus:\n" not in text:
        return text.rstrip() + "\ncurrent_focus:\n" + block
    if "Stage337 run337AN focus complete" in text:
        return re.sub(r"- >-\n  Stage337 run337AN focus complete:.*?(?=\n- >-|\Z)", block.rstrip(), text, count=1, flags=re.S)
    return text.replace("current_focus:\n", "current_focus:\n" + block, 1)


def update_status_docs(final: Mapping[str, Any]) -> list[Path]:
    changed: list[Path] = []
    selected_text = f"""# Stage337 Selection Status(337단계 선택 상태)

- stage_id(단계 ID): `{STAGE_ID}`
- stage_status(단계 상태): `open_active`
- selected_candidate(선택 후보): `none`
- latest_run(최신 실행): `{RUN_ID}`
- latest_decision(최신 결정): `{final['decision']}`
- current_run(현재 실행): `{final['next_action']}`
- secondary_current_run(보조 현재 실행): `{final['secondary_next_action']}`
- broker_forward_boundary(브로커 전진 경계): `{final['broker_forward_boundary']}`
- broker_gap_status(브로커 공백 상태): `{final['broker_gap_status']}`
- exact_proxy_parity(정확 프록시 동등성): `{final['proxy_mt5_matched']}/{final['proxy_mt5_rows']}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- Forward Blocked(전진 차단): `{final['forward_blocked']}`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{final['next_action']}`
- effect(효과): run337AN(337AN 실행)은 frozen broker rollover reprobe(고정 브로커 이월 재탐침)를 실행했고, forward decision(전진 판정)은 아직 주장하지 않는다.
"""
    changed.append(ak.write_md(SELECTED_STATUS, selected_text))
    focus = (
        f"Stage337 run337AN focus complete: run337AN(337AN 실행)은 `{final['status']}`로 broker rollover reprobe(브로커 이월 재탐침)를 닫았다. "
        f"Effect(효과): runtime(런타임) `{final['runtime_completed']}/{final['runtime_total']}`, "
        f"broker gap(브로커 공백) `{final['broker_gap_status']}`, exact proxy/MT5 parity(정확 프록시/메타트레이더5 동등성) "
        f"`{final['proxy_mt5_matched']}/{final['proxy_mt5_rows']}`이며 Forward/Goal(전진/목표)은 주장하지 않는다."
    )
    if path_exists(WORKSPACE_STATE):
        text, bom = ak.read_text(WORKSPACE_STATE)
        text = replace_line(text, "current_run_id:", f"current_run_id: {final['next_action']}")
        text = replace_line(text, "updated_on:", f"updated_on: '{TODAY}'")
        text = upsert_focus_block(text, focus)
        changed.append(ak.write_text(WORKSPACE_STATE, text, bom))
    if path_exists(CURRENT_STATE):
        text, bom = ak.read_text(CURRENT_STATE)
        for prefix, replacement in (
            ("- current_run(현재 실행):", f"- current_run(현재 실행): `{final['next_action']}`"),
            ("- secondary_current_run(보조 현재 실행):", f"- secondary_current_run(보조 현재 실행): `{final['secondary_next_action']}`"),
            ("- status(상태):", f"- status(상태): `{final['status']}`"),
            ("- decision(결정):", f"- decision(결정): `{final['decision']}`"),
            ("- latest_completed_run(최근 완료 실행):", f"- latest_completed_run(최근 완료 실행): `{RUN_ID}`"),
            ("- next_action(다음 행동):", f"- next_action(다음 행동): `{final['next_action']}`"),
            ("- claim_boundary(주장 경계):", f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`"),
        ):
            text = replace_line(text, prefix, replacement)
        entry = f"""## Stage337 run337AN(337AN 실행) - {TODAY}

- status(상태): `{final['status']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- secondary_next_action(보조 다음 행동): `{final['secondary_next_action']}`
- effect(효과): broker gap(브로커 공백) `{final['broker_gap_status']}`, exact proxy/MT5 parity(정확 프록시/메타트레이더5 동등성) `{final['proxy_mt5_matched']}/{final['proxy_mt5_rows']}`를 기록했다. Forward Passed/Failed(전진 통과/실패), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 주장하지 않는다.
"""
        if "## Stage337 run337AN(337AN 실행)" in text:
            text = re.sub(r"## Stage337 run337AN\(337AN 실행\).*?(?=\n## |\Z)", entry.strip(), text, count=1, flags=re.S)
        else:
            text = text.rstrip() + "\n\n" + entry.strip() + "\n"
        changed.append(ak.write_text(CURRENT_STATE, text, bom))
    if path_exists(CHANGELOG):
        text, bom = ak.read_text(CHANGELOG)
        line = (
            f"- {TODAY}: Stage337 run337AN(337AN 실행) `{final['status']}`. "
            f"Effect(효과): broker gap(브로커 공백) `{final['broker_gap_status']}`, "
            f"exact proxy/MT5 parity(정확 프록시/메타트레이더5 동등성) `{final['proxy_mt5_matched']}/{final['proxy_mt5_rows']}`; Forward/Goal(전진/목표) not_claimed(미주장)."
        )
        if "Stage337 run337AN(337AN 실행)" not in text:
            text = text.rstrip() + "\n" + line + "\n"
        changed.append(ak.write_text(CHANGELOG, text, bom))
    if path_exists(STAGE_BRIEF):
        text, bom = ak.read_text(STAGE_BRIEF)
        text = re.sub(r"- latest_run\([^)]*\): `[^`]*`", f"- latest_run(최신 실행): `{RUN_ID}`", text, count=1)
        summary = (
            f"- run337AN_summary(337AN 요약): `{final['status']}`. "
            f"Effect(효과): broker gap(브로커 공백) `{final['broker_gap_status']}`, "
            f"proxy/MT5 parity(프록시/메타트레이더5 동등성) `{final['proxy_mt5_matched']}/{final['proxy_mt5_rows']}`; "
            f"Forward/Goal(전진/목표)은 주장하지 않는다.\n"
        )
        if "run337AN_summary(337AN 요약)" in text:
            text = re.sub(r"- run337AN_summary\(337AN 요약\): [^\n]*(?:\n|$)", summary, text, count=1)
        else:
            text = text.rstrip() + "\n" + summary
        changed.append(ak.write_text(STAGE_BRIEF, text, bom))
    return changed


def update_registers(final: Mapping[str, Any]) -> list[Path]:
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "broker_rollover_reprobe",
        "family": "runtime_parity_repair",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "primary_report": rel(REPORT_PATH),
        "notes": f"decision={final['decision']};next_action={final['next_action']};goal_achieve_not_claimed.",
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__broker_rollover_reprobe",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "broker_rollover_reprobe",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "runtime_boundary_reprobe",
        "tier_scope": "Tier A u42 broker runtime diagnostic(Tier A u42 브로커 런타임 진단)",
        "kpi_scope": "runtime_probe_no_forward_decision(런타임 탐침, 전진 판정 없음)",
        "scoreboard_lane": "runtime_parity_repair",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "primary_kpi": f"broker_gap={final['broker_gap_status']};proxy_mt5={final['proxy_mt5_matched']}/{final['proxy_mt5_rows']}",
        "guardrail_kpi": "no_training;no_threshold_retune;no_lot_opt;no_forward_claim",
        "external_verification_status": "completed" if final["runtime_completed"] == final["runtime_total"] and final["runtime_total"] else "blocked_or_incomplete",
        "notes": f"decision={final['decision']};next_action={final['next_action']};goal_achieve_not_claimed.",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__broker_rollover_reprobe",
        "run_key": f"{RUN_ID}__broker_rollover_reprobe",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "runtime_parity_repair",
        "family": "broker_rollover_reprobe",
        "question": "does the frozen broker tester now reach feature_last after the no-lookahead input lock",
        "evidence_scope": "MT5 Strategy Tester report, runtime telemetry, exact timestamp proxy, broker feature_last gap",
        "kpi_scope": "runtime_probe_no_forward_decision",
        "metric_scope": "runtime_probe_no_forward_decision",
        "status": final["status"],
        "judgment": final["judgment"],
        "claim_boundary": CLAIM_BOUNDARY,
        "path": rel(REPORT_PATH),
        "report_path": rel(REPORT_PATH),
        "primary_artifact": rel(REPORT_PATH),
        "notes": f"secondary_next_action={final['secondary_next_action']};goal_achieve_not_claimed.",
        "decision": final["decision"],
        "next_action": final["next_action"],
    }
    return [
        ak.upsert_csv(RUN_REGISTRY, ["run_id"], run_row),
        ak.upsert_csv(ALPHA_LEDGER, ["ledger_row_id"], alpha_row),
        ak.upsert_csv(STAGE_LEDGER, ["run_key"], stage_row),
    ]


def main() -> int:
    args = parse_args()
    configure_probe_modules()
    terminal_path = Path(args.terminal)
    metaeditor_path = Path(args.metaeditor)
    common_files_root = Path(args.common_files_root)
    tester_profile_root = Path(args.tester_profile_root)
    terminal_data_root = Path(args.terminal_data_root)
    for directory in (RUN_DIR, MT5_DIR, FEATURE_COPY_DIR, MODEL_COPY_DIR, TELEMETRY_DIR):
        io_path(directory).mkdir(parents=True, exist_ok=True)

    source = load_source_broker_attempt()
    prepared = [build_broker_source_attempt(source)]
    broker_api = ab.mt5_api_symbol_visibility(terminal_path, ORIGIN_SYMBOL)
    pre_tester_recovery = qprobe.stop_target_terminal_if_running(terminal_path)
    attempts, handoff_rows, materialized_artifacts = base.build_attempts(prepared, common_files_root)
    scenario_by_attempt = {row["attempt_name"]: row for row in prepared}
    rewritten: list[dict[str, Any]] = []
    for attempt in attempts:
        scenario = scenario_by_attempt.get(str(attempt["attempt_name"]), {})
        for key in ("scenario_id", "scenario_symbol", "scenario_from_date", "scenario_to_date", "scenario_model", "scenario_role"):
            attempt[key] = scenario.get(key, "")
        rewritten.append(rewrite_attempt_to_broker_scenario(dict(attempt)))
    attempts = rewritten

    before_offsets = qprobe.log_offsets([TESTER_LOG, TESTER_AGENT_LOG, TERMINAL_LOG])
    if args.materialize_only:
        execution_result: dict[str, Any] = {
            "compile": {"status": "not_attempted_materialize_only"},
            "execution_results": [],
            "strategy_tester_reports": [],
            "materialize_only": True,
        }
    else:
        execution_result = base.execute_attempts(
            attempts,
            terminal_path=terminal_path,
            metaeditor_path=metaeditor_path,
            common_files_root=common_files_root,
            tester_profile_root=tester_profile_root,
            terminal_data_root=terminal_data_root,
            timeout_seconds=args.timeout_seconds,
            wait_timeout_seconds=args.wait_timeout_seconds,
            materialize_only=False,
        )
    runtime_rows = base.build_fresh_runtime_summary(attempts, execution_result)
    copied_runtime_artifacts = base.copy_runtime_outputs(common_files_root, attempts)
    feature_rows = qprobe.feature_last_rows(attempts)
    boundary_rows = ab.parse_tester_boundary_rows(before_offsets, attempts)
    gap_rows = annotate_gap_rows(
        qprobe.tester_gap_rows(runtime_rows, feature_rows, common_files_root, {"last_close_utc": broker_api.get("m5_last_close_utc", "")}),
        boundary_rows,
        attempts,
    )
    proxy_rows_raw, window_rows_raw = ak.build_exact_timestamp_proxy_rows(attempts, runtime_rows, common_files_root)
    proxy_rows = sanitize_proxy_rows(proxy_rows_raw)
    window_rows = sanitize_window_rows(window_rows_raw)
    diff_rows = sanitize_diff_rows(base.build_signal_difference_rows(proxy_rows, runtime_rows))
    usability = build_proxy_usability_rows(gap_rows, diff_rows)
    status, judgment, decision, next_action, secondary_next_action = classify(runtime_rows, gap_rows, diff_rows, args.materialize_only)
    final = decision_payload(status, judgment, decision, next_action, secondary_next_action, broker_api, runtime_rows, gap_rows, diff_rows)
    gates = build_gate_rows(runtime_rows, gap_rows, diff_rows, handoff_rows, args.materialize_only)
    input_evidence = build_input_evidence_rows(source, handoff_rows)

    artifacts: list[Path] = [
        ak.write_json(RUN_DIR / "broker_api_visibility.json", broker_api),
        ak.write_json(RUN_DIR / "pre_tester_terminal_recovery.json", pre_tester_recovery),
        ak.write_json(RUN_DIR / "execution_result.json", execution_result),
        ak.write_json(RUN_DIR / "final_decision.json", final),
        ak.write_csv(RUN_DIR / "input_evidence_index.csv", ak.columns_for(input_evidence, ["evidence_id"]), input_evidence),
        ak.write_csv(RUN_DIR / "handoff_attempts.csv", ak.columns_for(handoff_rows, ["attempt_name"]), handoff_rows),
        ak.write_json(RUN_DIR / "handoff_attempts.json", attempts),
        ak.write_csv(RUN_DIR / "runtime_summary.csv", ak.columns_for(runtime_rows, ["attempt_name"]), runtime_rows),
        ak.write_csv(RUN_DIR / "feature_last_timestamp_audit.csv", ak.columns_for(feature_rows, ["attempt_name"]), feature_rows),
        ak.write_csv(RUN_DIR / "tester_boundary_reprobe.csv", ak.columns_for(boundary_rows, ["attempt_name"]), boundary_rows),
        ak.write_csv(RUN_DIR / "tester_feature_last_gap_reprobe.csv", ak.columns_for(gap_rows, ["attempt_name"]), gap_rows),
        ak.write_csv(RUN_DIR / "exact_timestamp_proxy_scope.csv", ak.columns_for(window_rows, ["attempt_name"]), window_rows),
        ak.write_csv(RUN_DIR / "exact_timestamp_proxy_expected_result.csv", ak.columns_for(proxy_rows, ["attempt_name"]), proxy_rows),
        ak.write_csv(RUN_DIR / "exact_timestamp_proxy_mt5_difference.csv", ak.columns_for(diff_rows, ["attempt_name"]), diff_rows),
        ak.write_csv(RUN_DIR / "proxy_runtime_usability_reprobe.csv", ak.columns_for(usability, ["attempt_name"]), usability),
        ak.write_csv(RUN_DIR / "broker_rollover_reprobe_decision_matrix.csv", ak.columns_for([final], ["run_id"]), [final]),
        ak.write_csv(RUN_DIR / "required_gate_coverage_audit.csv", ak.columns_for(gates, ["gate_id"]), gates),
        ak.write_md(REPORT_PATH, report_text(final, gap_rows, usability)),
        ak.write_md(DECISION_DOC, decision_doc_text(final)),
        *materialized_artifacts,
        *copied_runtime_artifacts,
    ]
    for path, payload in receipt_payloads(final, attempts, runtime_rows, gap_rows).items():
        artifacts.append(ak.write_json(path, payload))
    artifacts.extend(update_status_docs(final))
    artifacts.extend(update_registers(final))
    manifest = ak.write_json(
        RUN_DIR / "run_manifest.json",
        {
            **final,
            "generated_at_utc": now_utc(),
            "command": "python stage_pipelines/stage337/reprobe_broker_rollover_boundary_after_no_lookahead.py",
            "materialize_only": bool(args.materialize_only),
            "primary_family": "runtime_parity_repair",
            "primary_skill": "obsidian-runtime-parity",
            "support_skills": [
                "obsidian-data-integrity",
                "obsidian-backtest-forensics",
                "obsidian-result-judgment",
            ],
            "artifacts": [rel(path) for path in artifacts if path_exists(path)],
        },
    )
    artifacts.append(manifest)
    artifacts.append(ak.append_artifacts([*artifacts, Path(__file__)], final))
    print(json.dumps(final, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
