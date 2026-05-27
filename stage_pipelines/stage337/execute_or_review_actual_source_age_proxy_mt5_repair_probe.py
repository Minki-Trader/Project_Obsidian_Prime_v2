from __future__ import annotations

import json
import sys
import csv
from pathlib import Path
from typing import Any, Mapping, Sequence

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from stage_pipelines.stage337 import reprobe_tester_rollover_boundary as rollover


TODAY = "2026-05-27"
STAGE_ID = "337_onnx_research_packet__cost_buffer_direction_curve_rebuild"
RUN_NUMBER = "run337Z"
RUN_ID = "run337Z_execute_or_review_actual_source_age_proxy_mt5_repair_probe_v1"
PARENT_RUN_ID = "run337Y_materialize_actual_source_age_proxy_mt5_repair_probe_inputs_v1"
SOURCE_RUN_ID = "run337U_source_clean_cost_buffer_rebuild_or_tester_rollover_reprobe_v1"
NEXT_RUN_ID = "run337AA_tester_history_cache_repair_or_actual_source_session_policy_probe_v1"
CLAIM_BOUNDARY = (
    "research_development_only_stage337Z_actual_source_age_proxy_mt5_reprobe_no_model_training_"
    "no_threshold_retuning_no_lot_optimization_no_candidate_selection_no_forward_passed_no_forward_failed_"
    "no_live_readiness_no_deployment_no_operating_promotion_no_runtime_authority_no_goal_achieve"
)

STATUS_REPAIRED = "completed_stage337Z_actual_source_age_proxy_mt5_reprobe_reached_feature_last_no_forward_decision"
STATUS_PARTIAL = "completed_stage337Z_actual_source_age_proxy_mt5_reprobe_gap_or_execution_issue_no_forward_decision"
STATUS_MATERIALIZED = "completed_stage337Z_actual_source_age_proxy_mt5_reprobe_materialized_only_no_forward_decision"
JUDGMENT_REPAIRED = "run337Z_runtime_reprobe_reaches_feature_last_proxy_mt5_parity_usable_for_next_forward_attribution"
JUDGMENT_PARTIAL = "run337Z_runtime_reprobe_completed_or_attempted_but_tester_gap_or_execution_issue_blocks_forward_decision"
JUDGMENT_MATERIALIZED = "run337Z_runtime_reprobe_inputs_materialized_execution_pending"
DECISION_REPAIRED = "stage337Z_open_forward_attribution_after_runtime_boundary_repair_no_selection"
DECISION_PARTIAL = "stage337Z_open_run337AA_tester_history_cache_or_source_session_policy_repair_no_selection"
DECISION_MATERIALIZED = "stage337Z_execution_pending_no_selection"

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
RUN337Y_DIR = STAGE_DIR / "02_runs" / "run337Y"
RUN337U_DIR = STAGE_DIR / "02_runs" / "run337U"
MT5_DIR = RUN_DIR / "mt5"
FEATURE_COPY_DIR = RUN_DIR / "feature_matrices"
MODEL_COPY_DIR = RUN_DIR / "models"
TELEMETRY_DIR = RUN_DIR / "runtime_telemetry"
REVIEWS_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEWS_DIR / "run337Z_actual_source_age_proxy_mt5_reprobe.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-27_stage337Z_actual_source_age_proxy_mt5_reprobe.md"
SELECTED_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
STAGE_LEDGER = REVIEWS_DIR / "stage_run_ledger.csv"
COMMON_ROOT = "Project_Obsidian_Prime_v2/stage337/run337Z_actual_source_age_proxy_mt5_reprobe"


def rel(path: Path) -> str:
    return rollover.rel(path)


def json_ready(value: Any) -> Any:
    return rollover.json_ready(value)


def configure_run337z() -> None:
    log_date = TODAY.replace("-", "")
    rollover.TODAY = TODAY
    rollover.STAGE_ID = STAGE_ID
    rollover.RUN_NUMBER = RUN_NUMBER
    rollover.RUN_ID = RUN_ID
    rollover.PARENT_RUN_ID = PARENT_RUN_ID
    rollover.SOURCE_RUN_ID = SOURCE_RUN_ID
    rollover.NEXT_RUN_ID = NEXT_RUN_ID
    rollover.CLAIM_BOUNDARY = CLAIM_BOUNDARY
    rollover.STATUS_REPAIRED = STATUS_REPAIRED
    rollover.STATUS_PARTIAL = STATUS_PARTIAL
    rollover.STATUS_MATERIALIZED = STATUS_MATERIALIZED
    rollover.JUDGMENT_REPAIRED = JUDGMENT_REPAIRED
    rollover.JUDGMENT_PARTIAL = JUDGMENT_PARTIAL
    rollover.JUDGMENT_MATERIALIZED = JUDGMENT_MATERIALIZED
    rollover.DECISION_REPAIRED = DECISION_REPAIRED
    rollover.DECISION_PARTIAL = DECISION_PARTIAL
    rollover.DECISION_MATERIALIZED = DECISION_MATERIALIZED
    rollover.STAGE_DIR = STAGE_DIR
    rollover.RUN_DIR = RUN_DIR
    rollover.RUN337Q_DIR = RUN337U_DIR
    rollover.RUN337Q_ATTEMPTS = RUN337U_DIR / "rollover_reprobe_handoff_attempts.json"
    rollover.RUN337Q_RUNTIME = RUN337U_DIR / "frozen_forward_mt5_result.csv"
    rollover.RUN337Q_GAP = RUN337U_DIR / "tester_rollover_feature_last_gap.csv"
    rollover.RUN337Q_FINAL = RUN337U_DIR / "final_tester_rollover_reprobe_decision.json"
    rollover.RUN337T_REPORT = REVIEWS_DIR / "run337Y_actual_measurement_inputs.md"
    rollover.MT5_DIR = MT5_DIR
    rollover.FEATURE_COPY_DIR = FEATURE_COPY_DIR
    rollover.MODEL_COPY_DIR = MODEL_COPY_DIR
    rollover.TELEMETRY_DIR = TELEMETRY_DIR
    rollover.REVIEWS_DIR = REVIEWS_DIR
    rollover.REPORT_PATH = REPORT_PATH
    rollover.DECISION_DOC = DECISION_DOC
    rollover.SELECTED_STATUS = SELECTED_STATUS
    rollover.STAGE_LEDGER = STAGE_LEDGER
    rollover.RUN_REGISTRY = RUN_REGISTRY
    rollover.ARTIFACT_REGISTRY = ARTIFACT_REGISTRY
    rollover.WORKSPACE_STATE = WORKSPACE_STATE
    rollover.CURRENT_STATE = CURRENT_STATE
    rollover.CHANGELOG = CHANGELOG
    rollover.TESTER_LOG = rollover.DEFAULT_PORTABLE_ROOT / "Tester" / "logs" / f"{log_date}.log"
    rollover.TESTER_AGENT_LOG = rollover.DEFAULT_PORTABLE_ROOT / "Tester" / "Agent-127.0.0.1-3000" / "logs" / f"{log_date}.log"
    rollover.TERMINAL_LOG = rollover.DEFAULT_PORTABLE_ROOT / "Logs" / f"{log_date}.log"
    rollover.COMMON_ROOT = COMMON_ROOT
    rollover.ATTEMPT_NAME = "u42_plain_rf"


def rewrite_attempt_to_rollover(attempt: dict[str, Any], tester_to_date: str) -> dict[str, Any]:
    tester = dict(attempt["ini"]["tester"])
    tester["ToDate"] = tester_to_date
    tester["Report"] = f"Project_Obsidian_Prime_v2_{RUN_ID}_{attempt['attempt_name']}"
    ini_path = Path(str(attempt["ini"]["path"]))
    attempt["ini"] = rollover.base.materialize_ini_file(tester, ini_path)
    attempt["to_date"] = tester_to_date
    attempt["attempt_role"] = "stage337Z_actual_source_age_proxy_mt5_reprobe_same_frozen_u42_model_feature_threshold_risk"
    attempt["record_view_prefix"] = f"mt5_stage337Z_{attempt['artifact_slug']}"
    attempt["source_run_id"] = SOURCE_RUN_ID
    attempt["repair_contract"] = "fresh MT5 reprobe only; same ONNX, feature order, threshold, risk, lot, ATR SL/TP, and feature CSV"
    attempt["signal_policy"] = "same frozen ONNX and runtime settings; actual source-age/proxy/MT5 repair gate"
    return attempt


def sanitize_proxy_rows(rows: Sequence[Mapping[str, Any]], *, source_label: str) -> list[dict[str, Any]]:
    cleaned: list[dict[str, Any]] = []
    for row in rows:
        item = dict(row)
        if "timestamp_aligned" not in str(item.get("proxy_source", "")):
            item["proxy_source"] = source_label.replace("stage337U", "stage337Z").replace("run337Q", "run337U")
        item["claim_boundary"] = CLAIM_BOUNDARY
        cleaned.append(item)
    return cleaned


def sanitize_diff_rows(rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    cleaned: list[dict[str, Any]] = []
    for row in rows:
        item = dict(row)
        item["mt5_source"] = "stage337Z_actual_source_age_proxy_mt5_reprobe_tier_a_telemetry_summary"
        item["usable_for_forward_pass_fail"] = False
        item["claim_boundary"] = CLAIM_BOUNDARY
        cleaned.append(item)
    return cleaned


def classify(
    runtime_rows: Sequence[Mapping[str, Any]],
    gap_rows: Sequence[Mapping[str, Any]],
    aligned_diff_rows: Sequence[Mapping[str, Any]],
    materialize_only: bool,
) -> tuple[str, str, str]:
    if materialize_only:
        return STATUS_MATERIALIZED, JUDGMENT_MATERIALIZED, DECISION_MATERIALIZED
    completed = sum(
        1
        for row in runtime_rows
        if row.get("tester_status") == "completed"
        and row.get("runtime_status") == "completed"
        and row.get("report_status") == "completed"
    )
    reached = sum(1 for row in gap_rows if row.get("gap_status") == "tester_reached_feature_last")
    matches = sum(1 for row in aligned_diff_rows if str(row.get("usable_for_runtime_signal_parity", "")).lower() == "true")
    if completed == len(runtime_rows) and reached == len(gap_rows) and matches == len(aligned_diff_rows) and aligned_diff_rows:
        return STATUS_REPAIRED, JUDGMENT_REPAIRED, DECISION_REPAIRED
    return STATUS_PARTIAL, JUDGMENT_PARTIAL, DECISION_PARTIAL


def gate_rows(
    runtime_rows: Sequence[Mapping[str, Any]],
    gap_rows: Sequence[Mapping[str, Any]],
    raw_diff_rows: Sequence[Mapping[str, Any]],
    aligned_diff_rows: Sequence[Mapping[str, Any]],
    boundary_rows: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    completed = sum(
        1
        for row in runtime_rows
        if row.get("tester_status") == "completed"
        and row.get("runtime_status") == "completed"
        and row.get("report_status") == "completed"
    )
    reached = sum(1 for row in gap_rows if row.get("gap_status") == "tester_reached_feature_last")
    raw_matches = sum(1 for row in raw_diff_rows if str(row.get("usable_for_runtime_signal_parity", "")).lower() == "true")
    aligned_matches = sum(1 for row in aligned_diff_rows if str(row.get("usable_for_runtime_signal_parity", "")).lower() == "true")
    return [
        {
            "gate_name": "run337Y_actual_measurement_inputs_reviewed",
            "status": "covered",
            "evidence_path": rel(RUN337Y_DIR / "mt5_reprobe_manifest.json"),
            "effect": "run337Y(337Y 실행)가 요구한 fresh MT5(신규 메타트레이더5) 실행/차단 게이트를 run337Z(337Z 실행) 입력으로 고정한다.",
        },
        {
            "gate_name": "frozen_runtime_identity_preserved",
            "status": "covered",
            "evidence_path": rel(RUN_DIR / "rollover_reprobe_handoff_manifest.csv"),
            "effect": "ONNX(온엑스), feature order(피처 순서), threshold(임계값), risk/lot(위험/랏), ATR SL/TP(ATR 손절/익절)를 바꾸지 않았음을 남긴다.",
        },
        {
            "gate_name": "fresh_mt5_runtime_execution_or_blocker",
            "status": "covered" if completed == len(runtime_rows) else "covered_partial",
            "evidence_path": rel(RUN_DIR / "frozen_forward_mt5_result.csv"),
            "effect": f"MT5 Strategy Tester(메타트레이더5 전략 테스터)를 실제로 실행하거나 차단 사유를 남긴다; completed={completed}/{len(runtime_rows)}.",
        },
        {
            "gate_name": "tester_reached_feature_last",
            "status": "covered_repaired" if reached == len(gap_rows) else "covered_blocker",
            "evidence_path": rel(RUN_DIR / "tester_rollover_feature_last_gap.csv"),
            "effect": f"tester observed bar(테스터 관측 봉)가 feature_last(피처 마지막 시점)에 닿았는지 확인한다; reached={reached}/{len(gap_rows)}.",
        },
        {
            "gate_name": "proxy_mt5_difference_recorded",
            "status": "covered" if aligned_matches == len(aligned_diff_rows) and aligned_diff_rows else "covered_partial",
            "evidence_path": rel(RUN_DIR / "timestamp_aligned_proxy_mt5_difference.csv"),
            "effect": f"proxy expected(프록시 예상값)와 MT5 observed(MT5 관측값)를 비교한다; raw={raw_matches}/{len(raw_diff_rows)}, aligned={aligned_matches}/{len(aligned_diff_rows)}.",
        },
        {
            "gate_name": "no_forward_or_goal_claim",
            "status": "covered",
            "evidence_path": rel(RUN_DIR / "final_decision.json"),
            "effect": "Forward Passed/Failed(전진 통과/실패), runtime authority(런타임 권위), Goal Achieve(목표 달성)를 주장하지 않는다.",
        },
    ]


def build_receipts(
    status: str,
    judgment: str,
    decision: str,
    runtime_rows: Sequence[Mapping[str, Any]],
    gap_rows: Sequence[Mapping[str, Any]],
    aligned_diff_rows: Sequence[Mapping[str, Any]],
    tester_to_date: str,
    feature_latest: Any,
) -> list[Path]:
    completed = sum(
        1
        for row in runtime_rows
        if row.get("tester_status") == "completed"
        and row.get("runtime_status") == "completed"
        and row.get("report_status") == "completed"
    )
    reached = sum(1 for row in gap_rows if row.get("gap_status") == "tester_reached_feature_last")
    matches = sum(1 for row in aligned_diff_rows if str(row.get("usable_for_runtime_signal_parity", "")).lower() == "true")
    return [
        rollover.write_json(
            RUN_DIR / "data_integrity_receipt.json",
            {
                "run_id": RUN_ID,
                "data_source": "run337U u42 frozen feature CSV and fresh run337Z MT5 tester output",
                "time_axis": "MT5 bar_time and feature timestamp are compared through tester observed bar and feature_last",
                "feature_label_boundary": "no model training, no threshold retune, no lot optimization, no future feature fill",
                "integrity_judgment": "usable_for_runtime_probe_not_forward_decision",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        rollover.write_json(
            RUN_DIR / "runtime_parity_receipt.json",
            {
                "run_id": RUN_ID,
                "runtime_completed": f"{completed}/{len(runtime_rows)}",
                "tester_reached_feature_last": f"{reached}/{len(gap_rows)}",
                "timestamp_aligned_signal_parity": f"{matches}/{len(aligned_diff_rows)}",
                "runtime_claim_boundary": "runtime_probe_only_no_runtime_authority",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        rollover.write_json(
            RUN_DIR / "backtest_forensics_receipt.json",
            {
                "run_id": RUN_ID,
                "tester_identity": "FPMarketsSC-Live US100 M5 real-tick Strategy Tester actual source-age/proxy/MT5 reprobe",
                "requested_tester_to_date": tester_to_date,
                "feature_latest_timestamp": feature_latest.isoformat().replace("+00:00", "Z"),
                "trade_evidence": [
                    {key: row.get(key, "") for key in ("attempt_name", "net_profit", "profit_factor", "trade_count", "max_drawdown_amount")}
                    for row in runtime_rows
                ],
                "backtest_judgment": "usable_with_boundary_for_runtime_probe_not_forward_decision",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        rollover.write_json(
            RUN_DIR / "result_judgment_receipt.json",
            {
                "run_id": RUN_ID,
                "status": status,
                "judgment": judgment,
                "decision": decision,
                "forward_passed": "not_claimed",
                "forward_failed": "not_claimed",
                "runtime_authority": "not_claimed",
                "goal_achieve": "not_claimed",
                "next_action": NEXT_RUN_ID,
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        rollover.write_json(
            RUN_DIR / "artifact_lineage_receipt.json",
            {
                "run_id": RUN_ID,
                "parent_run_id": PARENT_RUN_ID,
                "source_run_id": SOURCE_RUN_ID,
                "source_inputs": [rel(RUN337Y_DIR / "mt5_reprobe_manifest.json"), rel(RUN337U_DIR / "rollover_reprobe_handoff_attempts.json")],
                "lineage_judgment": "same frozen u42 ONNX package carried into run337Z with new runtime identity only",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
    ]


def write_report(
    status: str,
    judgment: str,
    decision: str,
    latest_probe: Mapping[str, Any],
    runtime_rows: Sequence[Mapping[str, Any]],
    gap_rows: Sequence[Mapping[str, Any]],
    raw_diff_rows: Sequence[Mapping[str, Any]],
    aligned_diff_rows: Sequence[Mapping[str, Any]],
    tester_to_date: str,
) -> Path:
    completed = sum(
        1
        for row in runtime_rows
        if row.get("tester_status") == "completed"
        and row.get("runtime_status") == "completed"
        and row.get("report_status") == "completed"
    )
    reached = sum(1 for row in gap_rows if row.get("gap_status") == "tester_reached_feature_last")
    raw_matches = sum(1 for row in raw_diff_rows if str(row.get("usable_for_runtime_signal_parity", "")).lower() == "true")
    aligned_matches = sum(1 for row in aligned_diff_rows if str(row.get("usable_for_runtime_signal_parity", "")).lower() == "true")
    lines = [
        "# Stage337Z Actual Source-Age Proxy MT5 Reprobe(337Z 실제 원천 나이 프록시 MT5 재탐침)",
        "",
        f"- run_id(실행 ID): `{RUN_ID}`",
        f"- status(상태): `{status}`",
        f"- judgment(판정): `{judgment}`",
        f"- decision(결정): `{decision}`",
        f"- requested ToDate(요청 종료일): `{tester_to_date}`",
        f"- API latest US100 close(API 최신 US100 종가): `{latest_probe.get('last_close_utc', '')}`",
        f"- MT5 completed(MT5 완료): `{completed}/{len(runtime_rows)}`",
        f"- tester reached feature_last(테스터가 피처 마지막 시점 도달): `{reached}/{len(gap_rows)}`",
        f"- raw proxy parity(원시 프록시 동등성): `{raw_matches}/{len(raw_diff_rows)}`",
        f"- timestamp-aligned proxy parity(시점 맞춤 프록시 동등성): `{aligned_matches}/{len(aligned_diff_rows)}`",
        "- Forward Passed(전진 통과): `not_claimed`",
        "- Forward Failed(전진 실패): `not_claimed`",
        "- runtime authority(런타임 권위): `not_claimed`",
        "- Goal Achieve(목표 달성): `not_claimed`",
        "",
        "## Runtime Metrics(런타임 지표)",
        "",
        "| attempt(시도) | status(상태) | net(순익) | PF(수익요인) | trades(거래수) | DD(드로다운) |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for row in runtime_rows:
        status_label = f"{row.get('tester_status', '')}/{row.get('runtime_status', '')}/{row.get('report_status', '')}"
        lines.append(
            f"| `{row.get('attempt_name', '')}` | `{status_label}` | `{row.get('net_profit', '')}` | "
            f"`{row.get('profit_factor', '')}` | `{row.get('trade_count', '')}` | `{row.get('max_drawdown_amount', '')}` |"
        )
    lines.extend(
        [
            "",
            "## Boundary(경계)",
            "",
            "run337Z(337Z 실행)는 새 후보 개발이 아니다. 효과(effect, 효과)는 run337Y(337Y 실행)가 요구한 "
            "fresh MT5 runtime execution(신규 MT5 런타임 실행), tester feature_last reach(테스터 피처 마지막 도달), "
            "proxy-vs-MT5 difference(프록시 대 MT5 차이)를 실제 근거로 닫는 것이다.",
            "",
            "ONNX(온엑스), Adapter package(어댑터 패키지), feature order(피처 순서), D/B decision surface(D/B 결정 표면), "
            "score threshold(점수 임계값), risk/lot logic(위험/랏 로직), ATR SL/TP(ATR 손절/익절)는 바꾸지 않았다.",
        ]
    )
    return rollover.write_md(REPORT_PATH, "\n".join(lines))


def write_decision_doc(
    status: str,
    judgment: str,
    decision: str,
    latest_probe: Mapping[str, Any],
    tester_to_date: str,
    reached: int,
    total: int,
) -> Path:
    text = f"""# Stage337Z Decision(337Z 결정)

- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{status}`
- judgment(판정): `{judgment}`
- decision(결정): `{decision}`
- requested ToDate(요청 종료일): `{tester_to_date}`
- API latest US100 close(API 최신 US100 종가): `{latest_probe.get('last_close_utc', '')}`
- tester reached feature_last(테스터 피처 마지막 도달): `{reached}/{total}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime authority(런타임 권위): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

Effect(효과): run337Z(337Z 실행)는 frozen u42(고정 u42) runtime probe(런타임 탐침)를 다시 실행해 proxy expected(프록시 예상값)와 MT5 observed(MT5 관측값)를 비교했다. 결과는 운영 주장(operating claim, 운영 주장)이 아니라 다음 tester/session repair(테스터/세션 수정) 또는 attribution(기여도 분석) 입력이다.
"""
    return rollover.write_md(DECISION_DOC, text)


def update_status_docs(
    status: str,
    decision: str,
    runtime_rows: Sequence[Mapping[str, Any]],
    gap_rows: Sequence[Mapping[str, Any]],
    aligned_diff_rows: Sequence[Mapping[str, Any]],
) -> list[Path]:
    completed = sum(
        1
        for row in runtime_rows
        if row.get("tester_status") == "completed"
        and row.get("runtime_status") == "completed"
        and row.get("report_status") == "completed"
    )
    reached = sum(1 for row in gap_rows if row.get("gap_status") == "tester_reached_feature_last")
    aligned = sum(1 for row in aligned_diff_rows if str(row.get("usable_for_runtime_signal_parity", "")).lower() == "true")
    selection_text = f"""# Stage337 Selection Status(337단계 선택 상태)

- stage_id(단계 ID): `{STAGE_ID}`
- stage_status(단계 상태): `open_active`
- selected_candidate(선택 후보): `none`
- latest_run(최신 실행): `{RUN_ID}`
- latest_decision(최신 결정): `{decision}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- frozen_runtime_probe(고정 런타임 탐침): `{completed}/{len(runtime_rows)} completed(완료)`
- tester_reached_feature_last(테스터 피처 마지막 도달): `{reached}/{len(gap_rows)}`
- timestamp_aligned_proxy_parity(시점 맞춤 프록시 동등성): `{aligned}/{len(aligned_diff_rows)}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- Forward Blocked(전진 차단): `current_run_boundary`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): run337Z(337Z 실행)는 실제 MT5(메타트레이더5) 재탐침과 proxy-vs-MT5(프록시 대 MT5) 비교를 남겼고, Forward Passed/Failed(전진 통과/실패)는 아직 주장하지 않는다.
"""
    rollover.write_md(SELECTED_STATUS, selection_text)

    if rollover.path_exists(WORKSPACE_STATE):
        text, had_bom = rollover.read_text_lossless(WORKSPACE_STATE)
        lines = text.splitlines()
        for idx, line in enumerate(lines):
            if line.startswith("current_run_id:"):
                lines[idx] = f"current_run_id: {NEXT_RUN_ID}"
                break
        focus = (
            "- >-\n"
            f"  Stage337 run337Z focus complete: run337Z(337Z 실행)는 `{status}`로 MT5(메타트레이더5) 재탐침을 기록했다. "
            f"Effect(효과): completed(완료) `{completed}/{len(runtime_rows)}`, tester reached feature_last(테스터 피처 마지막 도달) `{reached}/{len(gap_rows)}`, "
            f"timestamp-aligned proxy parity(시점 맞춤 프록시 동등성) `{aligned}/{len(aligned_diff_rows)}`이며 Forward/Goal(전진/목표) 주장은 하지 않는다."
        )
        text = "\n".join(lines) + "\n"
        if "Stage337 run337Z focus complete" in text:
            text = rollover.re.sub(r"- >-\n  Stage337 run337Z focus complete:.*?(?=\n- >-|\Z)", focus, text, count=1, flags=rollover.re.S)
        else:
            split_lines = text.splitlines()
            try:
                pos = split_lines.index("current_focus:")
                split_lines.insert(pos + 1, focus)
            except ValueError:
                split_lines.extend(["current_focus:", focus])
            text = "\n".join(split_lines) + "\n"
        rollover.write_text_preserving(WORKSPACE_STATE, text, had_bom)

    current_entry = f"""
## Stage337 run337Z(337Z 실행) - {TODAY}

- status(상태): `{status}`
- decision(결정): `{decision}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): MT5 runtime reprobe(MT5 런타임 재탐침) `{completed}/{len(runtime_rows)}`, tester feature_last reach(테스터 피처 마지막 도달) `{reached}/{len(gap_rows)}`, timestamp-aligned proxy parity(시점 맞춤 프록시 동등성) `{aligned}/{len(aligned_diff_rows)}`를 기록했다.
"""
    if rollover.path_exists(CURRENT_STATE):
        text, had_bom = rollover.read_text_lossless(CURRENT_STATE)
        if "## Stage337 run337Z(337Z 실행)" in text:
            text = rollover.re.sub(r"## Stage337 run337Z\(337Z 실행\).*?(?=\n## |\Z)", current_entry.strip(), text, count=1, flags=rollover.re.S)
            rollover.write_text_preserving(CURRENT_STATE, text.rstrip() + "\n", had_bom)
        else:
            rollover.write_text_preserving(CURRENT_STATE, text.rstrip() + "\n\n" + current_entry.strip() + "\n", had_bom)

    if rollover.path_exists(CHANGELOG):
        text, had_bom = rollover.read_text_lossless(CHANGELOG)
        line = (
            f"\n- {TODAY}: Stage337 run337Z(337Z 실행) `{status}`. "
            f"Effect(효과): MT5 runtime reprobe(MT5 런타임 재탐침) `{completed}/{len(runtime_rows)}`와 "
            "proxy-vs-MT5(프록시 대 MT5) 비교를 기록했고 Forward/Goal(전진/목표) 주장은 없다.\n"
        )
        if "Stage337 run337Z(337Z 실행)" in text:
            text = rollover.re.sub(r"\n- [^\n]*Stage337 run337Z\(337Z 실행\)[^\n]*", line.rstrip(), text, count=1)
            rollover.write_text_preserving(CHANGELOG, text.rstrip() + "\n", had_bom)
        else:
            rollover.write_text_preserving(CHANGELOG, text.rstrip() + line, had_bom)
    return [SELECTED_STATUS, WORKSPACE_STATE, CURRENT_STATE, CHANGELOG]


def update_registers(status: str, judgment: str, decision: str, artifact_paths: Sequence[Path]) -> list[Path]:
    registry_paths = [
        rollover.upsert_csv(
            RUN_REGISTRY,
            ["run_id"],
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "family": "actual_source_age_proxy_mt5_reprobe",
                "lane": "runtime_parity_repair",
                "status": status,
                "judgment": judgment,
                "primary_report": rel(REPORT_PATH),
                "path": rel(REPORT_PATH),
                "notes": f"decision={decision};next_action={NEXT_RUN_ID};goal_achieve_not_claimed.",
            },
        ),
        rollover.upsert_csv(
            STAGE_LEDGER,
            ["run_key"],
            {
                "run_key": f"{RUN_ID}__actual_source_age_proxy_mt5_reprobe",
                "ledger_row_id": f"{RUN_ID}__actual_source_age_proxy_mt5_reprobe",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "family": "actual_source_age_proxy_mt5_reprobe",
                "work_family": "runtime_parity_repair",
                "question": "can the frozen u42 ONNX runtime probe execute again with actual source-age and proxy-MT5 evidence",
                "metric_scope": "runtime_boundary_reprobe_no_forward_decision",
                "evidence_scope": "MT5 tester telemetry report proxy parity tester feature_last reach",
                "kpi_scope": "diagnostic_runtime_probe_not_forward_kpi",
                "status": status,
                "judgment": judgment,
                "claim_boundary": CLAIM_BOUNDARY,
                "primary_artifact": rel(REPORT_PATH),
                "path": rel(REPORT_PATH),
                "notes": f"next_action={NEXT_RUN_ID};goal_achieve_not_claimed.",
                "decision": decision,
            },
        ),
    ]
    generated = rollover.now_utc()
    unique_paths: list[Path] = []
    seen: set[str] = set()
    for path in [*artifact_paths, Path(__file__)]:
        key = str(path)
        if key in seen:
            continue
        seen.add(key)
        unique_paths.append(path)
    rows: list[dict[str, Any]] = []
    for path in unique_paths:
        if not rollover.path_exists(path) or not rollover.io_path(path).is_file():
            continue
        suffix = path.suffix.lower()
        rows.append(
            {
                "artifact_id": f"{RUN_ID}::{rel(path)}",
                "artifact_type": suffix.lstrip(".") or "file",
                "path": rel(path),
                "artifact_path": rel(path),
                "sha256": rollover.sha256_file_lf_normalized(path)
                if suffix in {".csv", ".json", ".md", ".txt", ".ini", ".set", ".py"}
                else rollover.sha256_file(path),
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": generated,
                "notes": status,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    registry_paths.append(rollover.append_csv_rows(ARTIFACT_REGISTRY, rows))
    return registry_paths


def patch_rollover_functions() -> None:
    rollover.rewrite_attempt_to_rollover = rewrite_attempt_to_rollover
    rollover.sanitize_proxy_rows = sanitize_proxy_rows
    rollover.sanitize_diff_rows = sanitize_diff_rows
    rollover.classify = classify
    rollover.gate_rows = gate_rows
    rollover.build_receipts = build_receipts
    rollover.write_report = write_report
    rollover.write_decision_doc = write_decision_doc
    rollover.update_status_docs = update_status_docs
    rollover.update_registers = update_registers


def write_post_run_aliases() -> None:
    final_source = RUN_DIR / "final_tester_rollover_reprobe_decision.json"
    final_alias = RUN_DIR / "final_decision.json"
    if rollover.path_exists(final_source):
        payload = json.loads(rollover.io_path(final_source).read_text(encoding="utf-8-sig"))
        rollover.write_json(final_alias, payload)

    manifest_path = RUN_DIR / "run_manifest.json"
    if rollover.path_exists(manifest_path):
        manifest = json.loads(rollover.io_path(manifest_path).read_text(encoding="utf-8-sig"))
        manifest["command"] = "python stage_pipelines/stage337/execute_or_review_actual_source_age_proxy_mt5_repair_probe.py"
        artifacts = list(manifest.get("artifacts", []))
        for path in (Path(__file__), final_alias):
            item = rel(path)
            if item not in artifacts and rollover.path_exists(path):
                artifacts.append(item)
        manifest["artifacts"] = artifacts
        rollover.write_json(manifest_path, manifest)

    rows: list[dict[str, Any]] = []
    generated = rollover.now_utc()
    for path in (final_alias, manifest_path):
        if not rollover.path_exists(path):
            continue
        rows.append(
            {
                "artifact_id": f"{RUN_ID}::{rel(path)}::post_alias",
                "artifact_type": path.suffix.lower().lstrip(".") or "file",
                "path": rel(path),
                "artifact_path": rel(path),
                "sha256": rollover.sha256_file_lf_normalized(path),
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": generated,
                "notes": "post_run_alias",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    if rows:
        rollover.append_csv_rows(ARTIFACT_REGISTRY, rows)
    dedupe_artifact_registry_for_run()


def dedupe_artifact_registry_for_run() -> None:
    if not rollover.path_exists(ARTIFACT_REGISTRY):
        return
    with rollover.io_path(ARTIFACT_REGISTRY).open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        columns = list(reader.fieldnames or [])
        rows = [dict(row) for row in reader]
    if not columns:
        return
    last_index_by_id: dict[str, int] = {}
    for index, row in enumerate(rows):
        artifact_id = str(row.get("artifact_id", ""))
        if artifact_id.startswith(f"{RUN_ID}::"):
            last_index_by_id[artifact_id] = index
    if not last_index_by_id:
        return
    keep_rows: list[dict[str, Any]] = []
    for index, row in enumerate(rows):
        artifact_id = str(row.get("artifact_id", ""))
        if artifact_id.startswith(f"{RUN_ID}::") and last_index_by_id.get(artifact_id) != index:
            continue
        keep_rows.append(row)
    rollover.write_csv(ARTIFACT_REGISTRY, columns, keep_rows)


def main() -> int:
    configure_run337z()
    patch_rollover_functions()
    code = rollover.main()
    write_post_run_aliases()
    return code


if __name__ == "__main__":
    raise SystemExit(main())
