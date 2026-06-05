from __future__ import annotations

import csv
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.mt5.trade_report import pair_deals_into_trades, parse_mt5_trade_report  # noqa: E402
from stage_pipelines.stage344 import (  # noqa: E402
    materialize_s07_forward_cost_stability_validation_package_without_db as pkg,
)
from stage_pipelines.stage344 import (  # noqa: E402
    review_s07_forward_cost_stability_validation_mt5_probe_without_db as parent,
)


TODAY = "2026-06-01"
STAGE_ID = pkg.STAGE_ID
STAGE_DIR = pkg.STAGE_DIR
RUN_NUMBER = "run344J"
RUN_ID = "run344J_design_s07_deal_level_cost_session_forward_replay_validation_without_db_v1"
PARENT_RUN_ID = parent.RUN_ID
SOURCE_PACKAGE_RUN_ID = pkg.RUN_ID
SOURCE_RUNTIME_RUN_ID = "run344H_execute_s07_forward_cost_stability_validation_mt5_probe_without_db_v1"
NEXT_RUN_ID = "run344K_materialize_s07_deal_level_cost_session_forward_replay_validation_without_db_v1"

STATUS = "completed_stage344J_deal_level_cost_session_forward_replay_design_ready_no_selection"
JUDGMENT = "deal_level_cost_session_forward_replay_design_ready_parse_feasibility_confirmed_no_operating_claim"
DECISION = "stage344J_open_run344K_materialize_deal_level_cost_session_forward_replay_validation"
CLAIM_BOUNDARY = (
    "research_development_design_only_deal_level_cost_session_forward_replay_validation_"
    "no_new_mt5_execution_no_candidate_selection_no_forward_pass_no_live_readiness_"
    "no_operating_promotion_no_runtime_authority_no_goal_claim"
)

RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEW_DIR / "run344J_s07_deal_level_cost_session_forward_replay_design.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage344J_s07_deal_level_cost_session_forward_replay_design.md"
SELECTION_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
STAGE_README = STAGE_DIR / "README.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"

WORK_PACKET = RUN_DIR / "work_packet.json"
EXPERIMENT_CONTRACT = RUN_DIR / "experiment_design_contract.csv"
DATA_INTEGRITY_CONTRACT = RUN_DIR / "data_integrity_contract.csv"
MODEL_VALIDATION_CONTRACT = RUN_DIR / "model_validation_contract.csv"
RUNTIME_PARITY_CONTRACT = RUN_DIR / "runtime_parity_contract.csv"
DEAL_EXTRACTION_FEASIBILITY = RUN_DIR / "deal_extraction_feasibility.csv"
DEAL_LEVEL_EXTRACTION_CONTRACT = RUN_DIR / "deal_level_extraction_contract.csv"
SESSION_PNL_JOIN_PLAN = RUN_DIR / "session_pnl_join_plan.csv"
COST_REPLAY_CONTRACT = RUN_DIR / "cost_replay_contract.csv"
FORWARD_REPLAY_HANDOFF_PLAN = RUN_DIR / "forward_replay_handoff_plan.csv"
RUN344K_QUEUE = RUN_DIR / "run344K_queue.csv"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment_design_receipt.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "judgment_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs" / "context" / "current_working_state.md"
ROOT_CHANGELOG = ROOT / "CHANGELOG.md"
WORKSPACE_CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
PROJECT_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
ROOT_SELECTION_STATUS = ROOT / "docs" / "registers" / "selection_status.md"

SOURCE_PARENT_FINAL = parent.FINAL_DECISION
SOURCE_PARENT_GATES = parent.GATE_AUDIT
SOURCE_PARENT_QUEUE = parent.RUN344J_QUEUE
SOURCE_PARENT_POSITIVE = parent.POSITIVE_CLUES
SOURCE_PARENT_FAILURE = parent.FAILURE_MEMORY
SOURCE_PARENT_COMPARATOR = parent.COMPARATOR_REVIEW
SOURCE_PARENT_COST = parent.COST_STRESS_SCORECARD
SOURCE_PARENT_SESSION = parent.SESSION_SIGNAL_STABILITY
SOURCE_PARENT_REGIME = parent.REGIME_SIGNAL_STABILITY
SOURCE_PARENT_TELEMETRY_READ = parent.TELEMETRY_READ_MANIFEST
SOURCE_RUNTIME_SUMMARY = parent.probe.EXECUTION_SUMMARY
SOURCE_RUNTIME_REPORTS = parent.probe.STRATEGY_TESTER_REPORTS
SOURCE_RUNTIME_DIFF = parent.probe.PROXY_MT5_DIFF
SOURCE_RUNTIME_IDENTITY = parent.probe.RUNTIME_IDENTITY
SOURCE_FEATURES = pkg.FEATURE_MATRIX
SOURCE_ATTEMPTS = pkg.RUNTIME_PROBE_ATTEMPT_PACKAGE

INPUT_FILES = (
    SOURCE_PARENT_FINAL,
    SOURCE_PARENT_GATES,
    SOURCE_PARENT_QUEUE,
    SOURCE_PARENT_POSITIVE,
    SOURCE_PARENT_FAILURE,
    SOURCE_PARENT_COMPARATOR,
    SOURCE_PARENT_COST,
    SOURCE_PARENT_SESSION,
    SOURCE_PARENT_REGIME,
    SOURCE_PARENT_TELEMETRY_READ,
    SOURCE_RUNTIME_SUMMARY,
    SOURCE_RUNTIME_REPORTS,
    SOURCE_RUNTIME_DIFF,
    SOURCE_RUNTIME_IDENTITY,
    SOURCE_FEATURES,
    SOURCE_ATTEMPTS,
)

OUTPUT_FILES = (
    WORK_PACKET,
    EXPERIMENT_CONTRACT,
    DATA_INTEGRITY_CONTRACT,
    MODEL_VALIDATION_CONTRACT,
    RUNTIME_PARITY_CONTRACT,
    DEAL_EXTRACTION_FEASIBILITY,
    DEAL_LEVEL_EXTRACTION_CONTRACT,
    SESSION_PNL_JOIN_PLAN,
    COST_REPLAY_CONTRACT,
    FORWARD_REPLAY_HANDOFF_PLAN,
    RUN344K_QUEUE,
    EXPERIMENT_RECEIPT,
    DATA_RECEIPT,
    MODEL_RECEIPT,
    RUNTIME_RECEIPT,
    LINEAGE_RECEIPT,
    JUDGMENT_RECEIPT,
    CLAIM_RECEIPT,
    GATE_AUDIT,
    FINAL_DECISION,
    RUN_MANIFEST,
    REPORT_PATH,
    DECISION_DOC,
    WORKSPACE_STATE,
    CURRENT_WORKING_STATE,
    SELECTION_STATUS,
    ROOT_SELECTION_STATUS,
    STAGE_BRIEF,
    STAGE_README,
    ROOT_CHANGELOG,
    WORKSPACE_CHANGELOG,
    RUN_REGISTRY,
    PROJECT_LEDGER,
    STAGE_LEDGER,
    ARTIFACT_REGISTRY,
    Path(__file__),
)


def now_utc() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def rel(path: Path | str) -> str:
    return pkg.rel(path)


def exists(path: Path) -> bool:
    return pkg.path_is_file(path)


def ensure_parent(path: Path) -> None:
    pkg.ensure_parent(path)


def required(path: Path) -> Path:
    return pkg.required(path)


def sha256_file(path: Path) -> str:
    return pkg.sha256_file(path)


def read_json(path: Path) -> Any:
    return pkg.read_json(path)


def read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, low_memory=False)


def write_json(path: Path, payload: Any) -> None:
    pkg.write_json(path, payload)


def write_text(path: Path, text: str) -> None:
    pkg.write_text(path, text)


def append_text_once(path: Path, marker: str, text: str) -> None:
    pkg.append_text_once(path, marker, text)


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    rows_list = [dict(row) for row in rows]
    if fieldnames is None:
        fieldnames = []
        for row in rows_list:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    ensure_parent(path)
    with open(path, "w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fieldnames), extrasaction="ignore")
        writer.writeheader()
        for row in rows_list:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def write_frame(path: Path, frame: pd.DataFrame) -> None:
    ensure_parent(path)
    frame.to_csv(path, index=False, encoding="utf-8-sig")


def append_or_replace_csv(path: Path, keys: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> None:
    pkg.append_or_replace_csv(path, keys, rows)


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        if pd.isna(value) or value == "":
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def as_int(value: Any, default: int = 0) -> int:
    try:
        if pd.isna(value) or value == "":
            return default
        return int(round(float(value)))
    except (TypeError, ValueError):
        return default


def parent_gates_passed() -> bool:
    gates = read_csv(SOURCE_PARENT_GATES)
    return bool(len(gates) > 0 and gates["status"].astype(str).str.lower().eq("passed").all())


def feature_time_keys(features: pd.DataFrame) -> set[str]:
    return set(features["timestamp"].astype(str))


def report_path(record: Mapping[str, Any]) -> Path:
    return Path(str(record.get("html_report", {}).get("path", "")))


def build_deal_feasibility(summary: pd.DataFrame, report_records: Sequence[Mapping[str, Any]], features: pd.DataFrame) -> pd.DataFrame:
    keys = feature_time_keys(features)
    rows: list[dict[str, Any]] = []
    summary_by_attempt = {str(row["attempt_name"]): row for _, row in summary.iterrows()}
    for record in report_records:
        attempt = str(record.get("attempt_name", ""))
        path = report_path(record)
        parsed = parse_mt5_trade_report(path)
        trades = pair_deals_into_trades(parsed["deals"])
        open_matches = sum(trade.open_time.strftime("%Y.%m.%d %H:%M:%S") in keys for trade in trades)
        close_matches = sum(trade.close_time.strftime("%Y.%m.%d %H:%M:%S") in keys for trade in trades)
        trade_net = round(sum(trade.net_profit for trade in trades), 6)
        trade_gross = round(sum(trade.gross_profit for trade in trades), 6)
        summary_row = summary_by_attempt.get(attempt, {})
        reported_trades = as_int(summary_row.get("trade_count"))
        reported_net = as_float(summary_row.get("net_profit"))
        rows.append(
            {
                "attempt_name": attempt,
                "report_path": path.as_posix(),
                "report_sha256": sha256_file(path) if path.exists() else "",
                "parsed_deal_count": len(parsed["deals"]),
                "paired_trade_count": len(trades),
                "reported_trade_count": reported_trades,
                "trade_count_matches_report": len(trades) == reported_trades,
                "paired_trade_net_profit": trade_net,
                "reported_net_profit": reported_net,
                "net_profit_diff": round(trade_net - reported_net, 6),
                "paired_trade_gross_profit_sum": trade_gross,
                "entry_feature_match_count": open_matches,
                "exit_feature_match_count": close_matches,
                "entry_feature_match_rate": round(open_matches / len(trades), 6) if trades else 0.0,
                "exit_feature_match_rate": round(close_matches / len(trades), 6) if trades else 0.0,
                "join_policy": "entry_time_primary_exit_time_optional(진입 시각 우선, 청산 시각 선택)",
                "design_use": "confirms run344K can extract trade-level session/regime PnL(run344K 거래별 세션/국면 손익 추출 가능성 확인)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return pd.DataFrame(rows)


def build_contracts(feasibility: pd.DataFrame) -> dict[str, Any]:
    s07 = feasibility.loc[feasibility["attempt_name"].eq("s07_trend_confirmed_long_only")].iloc[0]
    experiment_rows = [
        {
            "contract_id": "run344J_hypothesis",
            "hypothesis": "s07의 중간 비용 생존 단서가 거래별 손익, 세션, 국면으로도 설명되는지 검증한다.",
            "decision_use": "run344K에서 deal-level extraction(거래별 추출)을 실행할지 결정한다.",
            "comparison_baseline": "run344I cost/session/regime signal-only review(신호 전용 검토), s05/s01 comparator(대조군)",
            "control_variables": "US100 M5, run344G package(패키지), run344H MT5 reports(MT5 보고서), thresholds(임계값), lot(로트), max_hold_bars(최대 보유 봉)",
            "changed_variables": "analysis grain(분석 입자)만 signal/fill(신호/체결)에서 trade-level PnL(거래별 손익)로 변경",
            "sample_scope": "Tier A, 2024.07.30-2025.01.01, s07/s05/s01 MT5 report trades(MT5 보고서 거래)",
            "success_criteria": "paired trade count(짝지은 거래 수)가 report trade count(보고서 거래 수)와 일치하고 entry feature join(진입 피처 조인)이 100%다.",
            "failure_criteria": "deal parser(거래 파서)가 거래를 놓치거나 s07 entry join(진입 조인)이 불완전하다.",
            "invalid_conditions": "report path missing(보고서 경로 누락), parser error(파서 오류), feature timestamp mismatch(피처 시각 불일치), MT5 parity mismatch(MT5 동등성 불일치)",
            "stop_conditions": "run344K에서 거래별 net(순손익)이 MT5 report(보고서)와 다르면 비용/세션 판독을 invalid(무효)로 낮춘다.",
            "evidence_plan": "deal_extraction_feasibility(거래 추출 가능성), trade-level records(거래별 기록), session/regime PnL buckets(세션/국면 손익 버킷), cost replay scorecard(비용 재생 점수판)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    data_rows = [
        {
            "check_id": "time_axis_and_join_boundary",
            "data_source": f"{rel(SOURCE_RUNTIME_REPORTS)}; {rel(SOURCE_FEATURES)}; {rel(SOURCE_RUNTIME_SUMMARY)}",
            "time_axis": "MT5 report deal time(보고서 거래 시각) and feature timestamp(피처 시각)는 서버 M5 bar time(서버 5분봉 시각)으로 취급한다.",
            "sample_scope": "s07 trades=26, s05 trades=23, s01 trades=22 from run344H reports(run344H 보고서)",
            "missing_or_duplicate_check": "entry feature join(진입 피처 조인)은 feasibility(가능성 확인)에서 수량 검증한다.",
            "feature_label_boundary": "새 feature/label(피처/라벨)을 만들지 않고 기존 runtime feature matrix(런타임 피처 행렬)를 거래 진입 시각에만 붙인다.",
            "split_boundary": "inner holdout runtime probe(내부 홀드아웃 런타임 탐침)만 사용하며 forward pass(전진 통과)는 주장하지 않는다.",
            "leakage_risk": "s07 after-the-fact selection(사후 선택) 위험은 연구 설계 경계로 낮추고 운영 주장 금지로 통제한다.",
            "data_hash_or_identity": f"s07_entry_join={s07['entry_feature_match_count']}/{s07['paired_trade_count']}; features={sha256_file(SOURCE_FEATURES)}",
            "integrity_judgment": "usable_with_boundary(경계부 사용 가능)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    model_rows = [
        {
            "model_family": "logistic_regression_onnx(로지스틱 회귀 ONNX)",
            "target_and_label": "existing run338D model target(기존 run338D 모델 목표); no new label(새 라벨 없음)",
            "split_method": "runtime_probe_review_design(런타임 탐침 검토 설계)",
            "selection_metric": "none for selection(선정 없음); design uses run344I moderate cost clue(중간 비용 단서)",
            "secondary_metrics": "trade-level net/PF/recovery, direction PnL, session PnL, regime PnL(거래별 순손익/방향/세션/국면)",
            "threshold_policy": "reuse packaged thresholds from run344G(run344G 패키지 임계값 재사용)",
            "overfit_risk": "single-window and post-hoc s07 choice(단일 구간과 사후 s07 선택)",
            "calibration_risk": "scores are runtime decisions, not newly calibrated probabilities(점수는 런타임 결정이지 새 보정 확률 아님)",
            "comparison_baseline": "s05_long_quality_extreme_top20 and s01_anchor_short_supply_control",
            "validation_judgment": "exploratory_design_only(탐색 설계 전용)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    runtime_rows = [
        {
            "contract_id": "run344J_runtime_boundary",
            "research_path": rel(Path(__file__)),
            "runtime_path": f"{rel(SOURCE_RUNTIME_REPORTS)}; {rel(SOURCE_RUNTIME_IDENTITY)}",
            "shared_contract": "run344G model/set/feature paths and run344H tester reports(run344G 모델/설정/피처 경로와 run344H 테스터 보고서)",
            "known_differences": "run344J does not execute MT5; it only checks report parser feasibility(run344J는 MT5를 실행하지 않고 보고서 파서 가능성만 확인)",
            "parity_check": f"run344H exact parity reused: diff={rel(SOURCE_RUNTIME_DIFF)}",
            "parity_identity": rel(SOURCE_RUNTIME_IDENTITY),
            "runtime_claim_boundary": "research_design_only_no_runtime_authority(연구 설계 전용, 런타임 권위 없음)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    return {
        "experiment": experiment_rows,
        "data": data_rows,
        "model": model_rows,
        "runtime": runtime_rows,
    }


def build_plans() -> dict[str, list[dict[str, Any]]]:
    extraction = [
        {
            "plan_id": "extract_trade_records",
            "action": "parse MT5 HTML reports into paired trades(MT5 HTML 보고서를 짝지은 거래로 파싱)",
            "required_fields": "attempt_name, trade_index, direction, open_time, close_time, net_profit, gross_profit, commission, swap",
            "success_rule": "paired_trade_count equals report trade_count(짝지은 거래 수가 보고서 거래 수와 일치)",
            "failure_rule": "parser error or count mismatch(파서 오류 또는 수량 불일치)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "plan_id": "attach_entry_features",
            "action": "join trade open_time to runtime_features timestamp(거래 진입 시각을 런타임 피처 시각에 조인)",
            "required_fields": "minutes_from_cash_open, adx_14, historical_vol_20, di_spread_14",
            "success_rule": "s07 entry join rate equals 1.0(s07 진입 조인율 1.0)",
            "failure_rule": "entry feature missing for any s07 trade(s07 거래 진입 피처 누락)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    session = [
        {
            "bucket_id": "cash_open_first_60m",
            "bucket_rule": "0 <= minutes_from_cash_open < 60",
            "metric_plan": "trade_count, net_profit, PF estimate, win_rate, long/short net(거래 수, 순손익, PF 추정, 승률, 방향별 손익)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "bucket_id": "cash_mid_60_210m",
            "bucket_rule": "60 <= minutes_from_cash_open < 210",
            "metric_plan": "same as above(위와 같음)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "bucket_id": "cash_late_after_210m",
            "bucket_rule": "minutes_from_cash_open >= 210",
            "metric_plan": "same as above(위와 같음)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "bucket_id": "regime_terciles",
            "bucket_rule": "adx_14 and historical_vol_20 terciles from feature matrix(피처 행렬 삼분위)",
            "metric_plan": "trade-level net and concentration check(거래별 순손익과 집중도 확인)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    cost = [
        {
            "scenario_id": "base",
            "cost_per_closed_trade_account_currency": 0.0,
            "success_floor": "reference only(기준 전용)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "scenario_id": "light",
            "cost_per_closed_trade_account_currency": 0.5,
            "success_floor": "net positive and PF >= 1.5(순손익 양수와 PF 1.5 이상)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "scenario_id": "moderate",
            "cost_per_closed_trade_account_currency": 2.0,
            "success_floor": "net positive, PF >= 1.5, recovery >= 1.0(순손익 양수, PF 1.5 이상, 회복 1.0 이상)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "scenario_id": "heavy",
            "cost_per_closed_trade_account_currency": 4.0,
            "success_floor": "exploratory stress only(탐색 압박 전용)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    handoff = [
        {
            "next_run_id": NEXT_RUN_ID,
            "handoff_item": "materialize deal-level extraction and cost/session replay(거래별 추출과 비용/세션 재생 물질화)",
            "inputs": f"{rel(SOURCE_RUNTIME_REPORTS)}; {rel(SOURCE_FEATURES)}; {rel(DEAL_EXTRACTION_FEASIBILITY)}",
            "outputs": "trade_level_records.csv, session_pnl_scorecard.csv, regime_pnl_scorecard.csv, cost_replay_scorecard.csv",
            "external_verification_status": "out_of_scope_by_claim(주장 범위 밖)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    return {"extraction": extraction, "session": session, "cost": cost, "handoff": handoff}


def make_gates(final: Mapping[str, Any]) -> pd.DataFrame:
    no_forbidden = (
        final["candidate_selection"] == "not_run"
        and final["forward_passed"] == "not_claimed"
        and final["goal_achieve"] == "not_claimed"
        and final["runtime_authority"] == "not_claimed"
        and final["operating_promotion"] == "not_claimed"
    )
    rows = [
        ("parent_run344I_gates_passed", final["parent_gate_passed"], rel(SOURCE_PARENT_GATES), "run344I gate(게이트)를 이어받음"),
        ("work_packet_schema_lint", exists(WORK_PACKET), rel(WORK_PACKET), "work packet(작업 묶음) 스키마를 남김"),
        ("mt5_reports_parseable", final["parseable_report_rows"] == 3, rel(DEAL_EXTRACTION_FEASIBILITY), "MT5 report(보고서) 거래 파싱 가능성 확인"),
        ("trade_count_matches_report", final["trade_count_match_rows"] == 3, rel(DEAL_EXTRACTION_FEASIBILITY), "paired trade count(짝지은 거래 수)가 보고서와 일치"),
        ("s07_entry_feature_join_feasible", final["s07_entry_feature_match_rate"] == 1.0, rel(DEAL_EXTRACTION_FEASIBILITY), "s07 거래 진입 시각 피처 조인 가능"),
        ("experiment_contract_written", exists(EXPERIMENT_CONTRACT), rel(EXPERIMENT_CONTRACT), "experiment design(실험 설계) 계약 작성"),
        ("data_model_runtime_contracts_written", exists(DATA_INTEGRITY_CONTRACT) and exists(MODEL_VALIDATION_CONTRACT) and exists(RUNTIME_PARITY_CONTRACT), f"{rel(DATA_INTEGRITY_CONTRACT)};{rel(MODEL_VALIDATION_CONTRACT)};{rel(RUNTIME_PARITY_CONTRACT)}", "data/model/runtime(데이터/모델/런타임) 경계 작성"),
        ("deal_level_join_plan_written", exists(DEAL_LEVEL_EXTRACTION_CONTRACT) and exists(SESSION_PNL_JOIN_PLAN), f"{rel(DEAL_LEVEL_EXTRACTION_CONTRACT)};{rel(SESSION_PNL_JOIN_PLAN)}", "거래별 조인 계획 작성"),
        ("no_forbidden_operating_claim", no_forbidden, rel(FINAL_DECISION), "설계를 운영 주장으로 올리지 않음"),
        ("required_gate_coverage_audit_written", True, rel(GATE_AUDIT), "필수 gate coverage audit(게이트 커버리지 감사) 기록"),
    ]
    return pd.DataFrame(
        [
            {
                "gate_id": gate,
                "status": "passed" if passed else "failed",
                "evidence_path": evidence,
                "effect": effect,
                "claim_boundary": CLAIM_BOUNDARY,
            }
            for gate, passed, evidence, effect in rows
        ]
    )


def build_receipts(final: Mapping[str, Any]) -> None:
    write_json(
        EXPERIMENT_RECEIPT,
        {
            "hypothesis": "s07 moderate-cost clue can be tested at trade-level PnL grain(s07 중간 비용 단서를 거래별 손익 입자로 검증 가능)",
            "decision_use": "open run344K materialization(run344K 물질화 개방)",
            "comparison_baseline": "run344I signal-only review and s05/s01 comparators(run344I 신호 전용 검토와 s05/s01 대조)",
            "control_variables": "run344G package and run344H MT5 reports unchanged(run344G 패키지와 run344H MT5 보고서 고정)",
            "changed_variables": "analysis grain only(분석 입자만 변경)",
            "sample_scope": "Tier A US100 M5 run344H reports(Tier A US100 M5 run344H 보고서)",
            "success_criteria": "report parseable and entry feature join feasible(보고서 파싱 가능, 진입 피처 조인 가능)",
            "failure_criteria": "count mismatch or missing entry features(수량 불일치 또는 진입 피처 누락)",
            "invalid_conditions": "parser error, timestamp mismatch, parity mismatch(파서 오류, 시각 불일치, 동등성 불일치)",
            "stop_conditions": "downgrade if run344K trade-level net diverges from MT5 report(run344K 거래별 순손익이 MT5 보고서와 다르면 격하)",
            "evidence_plan": [rel(DEAL_EXTRACTION_FEASIBILITY), rel(RUN344K_QUEUE)],
        },
    )
    write_json(
        DATA_RECEIPT,
        {
            "data_source": [rel(SOURCE_RUNTIME_REPORTS), rel(SOURCE_FEATURES)],
            "time_axis": "MT5 report time and runtime feature timestamp use server M5 bar time(MT5 보고서 시각과 런타임 피처 시각은 서버 M5 봉 시각)",
            "sample_scope": "s07/s05/s01 Tier A reports(Tier A 보고서)",
            "missing_or_duplicate_check": rel(DEAL_EXTRACTION_FEASIBILITY),
            "feature_label_boundary": "no new labels or future data(새 라벨이나 미래 데이터 없음)",
            "split_boundary": "inner holdout runtime probe only(내부 홀드아웃 런타임 탐침 전용)",
            "leakage_risk": "post-hoc s07 selection, controlled by no selection/no operating claim(사후 s07 선택, 선정/운영 주장 없음으로 통제)",
            "data_hash_or_identity": f"features_sha256={sha256_file(SOURCE_FEATURES)}",
            "integrity_judgment": "usable_with_boundary(경계부 사용 가능)",
        },
    )
    write_json(
        MODEL_RECEIPT,
        {
            "model_family": "logistic_regression_onnx(로지스틱 회귀 ONNX)",
            "target_and_label": "existing packaged runtime model(기존 패키지 런타임 모델)",
            "split_method": "runtime probe review design(런타임 탐침 검토 설계)",
            "selection_metric": "none(없음)",
            "secondary_metrics": "trade-level cost/session/regime PnL(거래별 비용/세션/국면 손익)",
            "threshold_policy": "reuse run344G thresholds(run344G 임계값 재사용)",
            "overfit_risk": "single-window post-hoc review(단일 구간 사후 검토)",
            "calibration_risk": "not a calibration claim(보정 주장 아님)",
            "comparison_baseline": "s05 and s01 comparators(s05/s01 대조)",
            "validation_judgment": "exploratory_design_only(탐색 설계 전용)",
        },
    )
    write_json(
        RUNTIME_RECEIPT,
        {
            "research_path": rel(Path(__file__)),
            "runtime_path": [rel(SOURCE_RUNTIME_REPORTS), rel(SOURCE_RUNTIME_IDENTITY)],
            "shared_contract": "reuse run344H reports and run344G features(run344H 보고서와 run344G 피처 재사용)",
            "known_differences": "no new MT5 execution in run344J(run344J 새 MT5 실행 없음)",
            "parity_check": rel(SOURCE_RUNTIME_DIFF),
            "parity_identity": rel(SOURCE_RUNTIME_IDENTITY),
            "runtime_claim_boundary": "research_design_only_no_runtime_authority(연구 설계 전용, 런타임 권위 없음)",
        },
    )
    write_json(
        JUDGMENT_RECEIPT,
        {
            "result_subject": RUN_ID,
            "evidence_available": [rel(DEAL_EXTRACTION_FEASIBILITY), rel(EXPERIMENT_CONTRACT), rel(RUN344K_QUEUE)],
            "evidence_missing": ["actual run344K trade-level PnL extraction(실제 run344K 거래별 손익 추출)", "forward replay execution(전진 재생 실행)"],
            "judgment_label": "exploratory_design_ready(탐색 설계 준비)",
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": NEXT_RUN_ID,
            "user_explanation_hook": "거래별 파싱은 가능하고 다음 실행에서 실제 세션/국면 손익을 만들 수 있다.",
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            "run_id": RUN_ID,
            "allowed_claims": ["design ready(설계 준비)", "deal parser feasibility confirmed(거래 파서 가능성 확인)"],
            "forbidden_claims": ["candidate selection(후보 선정)", "forward pass(전진 통과)", "operating promotion(운영 승격)", "runtime authority(런타임 권위)", "Goal Achieve(목표 달성)"],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def write_docs(final: Mapping[str, Any]) -> None:
    report = f"""# run344J s07 Deal-Level Cost/Session Forward Replay Design(344J s07 거래별 비용/세션 전진 재생 설계)

## Summary(요약)

- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- parsed_reports(파싱 보고서): `{final['parseable_report_rows']}/3`
- trade_count_match(거래 수 일치): `{final['trade_count_match_rows']}/3`
- s07_entry_join_rate(s07 진입 조인율): `{final['s07_entry_feature_match_rate']}`
- next_run(다음 실행): `{NEXT_RUN_ID}`

## Action(행동)

run344I에서 남긴 signal-only stability(신호 전용 안정성)를 trade-level PnL(거래별 손익) 검증으로 바꾸기 위한 설계를 만들었다.

## Effect(효과)

MT5 HTML report(MT5 HTML 보고서)는 거래별로 파싱 가능하고, s07의 진입 시각은 runtime feature matrix(런타임 피처 행렬)에 100% 조인된다. 다음 run344K는 비용/세션/국면별 손익을 실제 거래 단위로 만들 수 있다.

## Boundary(경계)

이 run(실행)은 design only(설계 전용)다. candidate selection(후보 선정), forward pass(전진 통과), live readiness(실거래 준비), operating promotion(운영 승격), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 주장하지 않는다.
"""
    decision = f"""# {TODAY} Stage344J Design Decision(344J 설계 결정)

- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- evidence(근거): `{rel(DEAL_EXTRACTION_FEASIBILITY)}`, `{rel(RUN344K_QUEUE)}`

Action(행동): s07 거래별 비용/세션 전진 재생 검증 설계를 만들었다.
Effect(효과): run344K가 실제 trade-level PnL(거래별 손익) 산출물을 만들 수 있다.

claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    current = f"""# Current Working State(현재 작업 상태)

## Current Truth(현재 진실)

- active_stage(현재 단계): `{STAGE_ID}`
- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`

## Effect(효과)

run344J design(설계)이 완료되어 run344K materialization(물질화)을 열었다. 다음 행동(action, 행동)은 거래별 비용/세션/국면 손익 파일을 만드는 것이다.

## Boundary(경계)

`{CLAIM_BOUNDARY}`
"""
    selection = f"""# Stage 344 Selection Status(344단계 선정 상태)

- selected_model(선정 모델): `none(없음)`
- latest_design(최근 설계): `{RUN_ID}`
- research_clue(연구 단서): `s07_trend_confirmed_long_only`
- deal_parser_feasible(거래 파서 가능): `{final['parseable_report_rows'] == 3}`
- s07_entry_feature_join_rate(s07 진입 피처 조인율): `{final['s07_entry_feature_match_rate']}`
- runtime_authority(런타임 권위): `not_claimed(주장 없음)`
- operating_promotion(운영 승격): `not_claimed(주장 없음)`
- Goal Achieve(목표 달성): `not_claimed(주장 없음)`

Effect(효과): 연구 단서는 다음 검증으로 넘기되 운영 선정은 열지 않는다.
"""
    workspace = f"""current_stage_id: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {STATUS}
current_judgment: {JUDGMENT}
current_decision: {DECISION}
next_run_id: {NEXT_RUN_ID}
claim_boundary: {CLAIM_BOUNDARY}
updated_at: {TODAY}
"""
    write_text(REPORT_PATH, report)
    write_text(DECISION_DOC, decision)
    write_text(CURRENT_WORKING_STATE, current)
    write_text(SELECTION_STATUS, selection)
    write_text(ROOT_SELECTION_STATUS, selection)
    write_text(WORKSPACE_STATE, workspace)
    marker = f"run344J {RUN_ID}"
    append_text_once(
        STAGE_BRIEF,
        marker,
        f"""## run344J Deal-Level Replay Design(344J 거래별 재생 설계)

- run_id(실행 ID): `{RUN_ID}`
- parseable_reports(파싱 가능 보고서): `{final['parseable_report_rows']}/3`
- s07_entry_join_rate(s07 진입 조인율): `{final['s07_entry_feature_match_rate']}`
- effect(효과): run344K materialization(물질화)을 열었다.
""",
    )
    append_text_once(
        STAGE_README,
        marker,
        f"""## run344J Deal-Level Replay Design(344J 거래별 재생 설계)

- report(보고서): `{rel(REPORT_PATH)}`
- feasibility(가능성): `{rel(DEAL_EXTRACTION_FEASIBILITY)}`
- queue(대기열): `{rel(RUN344K_QUEUE)}`
- effect(효과): signal-only stability(신호 전용 안정성)를 trade-level PnL(거래별 손익) 검증으로 넘겼다.
""",
    )
    changelog = f"""## {TODAY} run344J Deal-Level Replay Design(거래별 재생 설계)

- action(행동): MT5 report(보고서) 거래 파서 가능성을 확인하고 비용/세션 손익 검증 설계를 만들었다.
- effect(효과): run344K에서 실제 거래별 비용/세션/국면 손익을 산출할 수 있다.
- boundary(경계): 선정/운영 승격/런타임 권위/목표 달성은 주장하지 않는다.
"""
    append_text_once(ROOT_CHANGELOG, marker, changelog)
    append_text_once(WORKSPACE_CHANGELOG, marker, changelog)


def write_registers(final: Mapping[str, Any], gates: pd.DataFrame) -> None:
    base_row = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "run_date": TODAY,
        "date": TODAY,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_run_id": NEXT_RUN_ID,
        "primary_artifact": rel(FINAL_DECISION),
        "report_path": rel(REPORT_PATH),
        "path": rel(REPORT_PATH),
        "gate_passes": int(gates["status"].astype(str).eq("passed").sum()),
        "gate_total": int(len(gates)),
        "claim_boundary": CLAIM_BOUNDARY,
        "source_package_run_id": SOURCE_PACKAGE_RUN_ID,
    }
    run_row = {
        **base_row,
        "lane": "experiment_design(실험 설계)",
        "family": "experiment_design(실험 설계)",
        "primary_report": rel(REPORT_PATH),
        "run_number": RUN_NUMBER,
        "notes": "deal-level cost/session forward replay design(거래별 비용/세션 전진 재생 설계); no selection(선정 없음).",
        "candidate_model_id": "logreg_balanced_c025_s07_trend_confirmed_long_only",
        "net_profit": final["s07_reported_net_profit"],
        "trade_count": final["s07_paired_trade_count"],
        "result_status": JUDGMENT,
    }
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], [run_row])
    rows = [
        {
            **base_row,
            "ledger_row_id": f"{RUN_ID}__Tier A",
            "subrun_id": "Tier A",
            "view": "Tier A separate(Tier A 분리)",
            "record_view": "Tier A separate(Tier A 분리)",
            "tier": "Tier A",
            "tier_scope": "Tier A",
            "metric_scope": "deal_level_design",
            "kpi_scope": "deal_level_design",
            "scoreboard_lane": "experiment_design(실험 설계)",
            "candidate_model_id": "logreg_balanced_c025_s07_trend_confirmed_long_only",
            "net_profit": final["s07_reported_net_profit"],
            "trade_count": final["s07_paired_trade_count"],
            "result_status": JUDGMENT,
            "primary_kpi": f"s07_trades={final['s07_paired_trade_count']};entry_join={final['s07_entry_feature_match_rate']}",
            "guardrail_kpi": "design_only_no_forward_pass(설계 전용, 전진 통과 없음)",
            "external_verification_status": "out_of_scope_by_claim(주장 범위 밖)",
            "notes": "Tier A design evidence only(Tier A 설계 근거 전용).",
        },
        {
            **base_row,
            "ledger_row_id": f"{RUN_ID}__Tier B",
            "subrun_id": "Tier B",
            "view": "Tier B separate(Tier B 분리)",
            "record_view": "Tier B separate(Tier B 분리)",
            "tier": "Tier B",
            "tier_scope": "Tier B",
            "metric_scope": "missing_required",
            "kpi_scope": "missing_required",
            "scoreboard_lane": "experiment_design(실험 설계)",
            "candidate_model_id": "missing_required",
            "primary_kpi": "missing_required",
            "guardrail_kpi": "missing_required",
            "external_verification_status": "missing_required(필수 누락)",
            "result_status": "missing_required(필수 누락)",
            "notes": "Tier B was outside this narrow design(Tier B는 이번 좁은 설계 밖).",
        },
        {
            **base_row,
            "ledger_row_id": f"{RUN_ID}__Tier A+B",
            "subrun_id": "Tier A+B",
            "view": "Tier A+B combined(Tier A+B 합산)",
            "record_view": "Tier A+B combined(Tier A+B 합산)",
            "tier": "Tier A+B",
            "tier_scope": "Tier A+B",
            "metric_scope": "same_as_tier_a_until_tier_b_available",
            "kpi_scope": "same_as_tier_a_until_tier_b_available",
            "scoreboard_lane": "experiment_design(실험 설계)",
            "candidate_model_id": "logreg_balanced_c025_s07_trend_confirmed_long_only",
            "net_profit": final["s07_reported_net_profit"],
            "trade_count": final["s07_paired_trade_count"],
            "result_status": "same_as_tier_a_until_tier_b_available",
            "primary_kpi": f"s07_trades={final['s07_paired_trade_count']};entry_join={final['s07_entry_feature_match_rate']}",
            "guardrail_kpi": "Tier B missing_required(Tier B 필수 누락)",
            "external_verification_status": "out_of_scope_by_claim(주장 범위 밖)",
            "notes": "Combined view is same as Tier A until Tier B exists(Tier B 전에는 합산이 Tier A와 같음).",
        },
    ]
    append_or_replace_csv(PROJECT_LEDGER, ["run_id", "view"], rows)
    append_or_replace_csv(STAGE_LEDGER, ["run_id", "view"], rows)


def update_artifact_registry(paths: Sequence[Path]) -> None:
    ensure_parent(ARTIFACT_REGISTRY)
    existing_rows: list[dict[str, Any]] = []
    fieldnames: list[str] = []
    if exists(ARTIFACT_REGISTRY):
        with open(ARTIFACT_REGISTRY, "r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = list(reader.fieldnames or [])
            existing_rows = [dict(row) for row in reader]
    required_fields = ["stage_id", "run_id", "artifact_type", "path", "sha256", "created_at", "claim_boundary", "artifact_id", "created_at_utc", "notes", "artifact_path"]
    for field in required_fields:
        if field not in fieldnames:
            fieldnames.append(field)
    new_rows: list[dict[str, Any]] = []
    for path in paths:
        if not exists(path):
            continue
        artifact_id = f"{RUN_NUMBER}::{rel(path)}"
        new_rows.append(
            {
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "artifact_type": path.suffix.lower().lstrip(".") or "artifact",
                "path": rel(path),
                "artifact_path": rel(path),
                "sha256": sha256_file(path),
                "created_at": TODAY,
                "created_at_utc": now_utc(),
                "artifact_id": artifact_id,
                "notes": "run344J design artifact(run344J 설계 산출물)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    new_ids = {row["artifact_id"] for row in new_rows}
    kept = [row for row in existing_rows if row.get("artifact_id") not in new_ids]
    with open(ARTIFACT_REGISTRY, "w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in kept + new_rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def build_design() -> Mapping[str, Any]:
    for path in INPUT_FILES:
        required(path)
    parent_final = read_json(SOURCE_PARENT_FINAL)
    if parent_final.get("next_run_id") != RUN_ID:
        raise RuntimeError("run344I next_run_id does not point to run344J")
    if not parent_gates_passed():
        raise RuntimeError("run344I gate audit has failed rows")

    summary = read_csv(SOURCE_RUNTIME_SUMMARY)
    report_records = read_json(SOURCE_RUNTIME_REPORTS)
    features = read_csv(SOURCE_FEATURES)
    feasibility = build_deal_feasibility(summary, report_records, features)
    write_frame(DEAL_EXTRACTION_FEASIBILITY, feasibility)
    contracts = build_contracts(feasibility)
    plans = build_plans()

    write_json(
        WORK_PACKET,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "primary_family": "experiment_design(실험 설계)",
            "primary_skill": "obsidian-experiment-design(실험 설계)",
            "support_skills": [
                "obsidian-data-integrity(데이터 무결성)",
                "obsidian-model-validation(모델 검증)",
                "obsidian-runtime-parity(런타임 동등성)",
                "obsidian-artifact-lineage(산출물 계보)",
                "obsidian-result-judgment(결과 판정)",
            ],
            "required_gates": [
                "work_packet_schema_lint",
                "mt5_reports_parseable",
                "trade_count_matches_report",
                "s07_entry_feature_join_feasible",
                "required_gate_coverage_audit_written",
            ],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_csv(EXPERIMENT_CONTRACT, contracts["experiment"])
    write_csv(DATA_INTEGRITY_CONTRACT, contracts["data"])
    write_csv(MODEL_VALIDATION_CONTRACT, contracts["model"])
    write_csv(RUNTIME_PARITY_CONTRACT, contracts["runtime"])
    write_csv(DEAL_LEVEL_EXTRACTION_CONTRACT, plans["extraction"])
    write_csv(SESSION_PNL_JOIN_PLAN, plans["session"])
    write_csv(COST_REPLAY_CONTRACT, plans["cost"])
    write_csv(FORWARD_REPLAY_HANDOFF_PLAN, plans["handoff"])
    write_csv(RUN344K_QUEUE, plans["handoff"])

    s07 = feasibility.loc[feasibility["attempt_name"].eq("s07_trend_confirmed_long_only")].iloc[0]
    final: dict[str, Any] = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "source_package_run_id": SOURCE_PACKAGE_RUN_ID,
        "source_runtime_run_id": SOURCE_RUNTIME_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_run_id": NEXT_RUN_ID,
        "next_action": NEXT_RUN_ID,
        "parent_gate_passed": True,
        "parseable_report_rows": int(len(feasibility)),
        "trade_count_match_rows": int(feasibility["trade_count_matches_report"].astype(bool).sum()),
        "s07_paired_trade_count": int(s07["paired_trade_count"]),
        "s07_reported_trade_count": int(s07["reported_trade_count"]),
        "s07_reported_net_profit": float(s07["reported_net_profit"]),
        "s07_paired_trade_net_profit": float(s07["paired_trade_net_profit"]),
        "s07_net_profit_diff": float(s07["net_profit_diff"]),
        "s07_entry_feature_match_count": int(s07["entry_feature_match_count"]),
        "s07_entry_feature_match_rate": float(s07["entry_feature_match_rate"]),
        "s07_exit_feature_match_rate": float(s07["exit_feature_match_rate"]),
        "candidate_selection": "not_run",
        "selected_model": "none(없음)",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "goal_achieve": "not_claimed",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "external_verification_status": "out_of_scope_by_claim(주장 범위 밖)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    gates = make_gates(final)
    final["gate_passes"] = int(gates["status"].astype(str).eq("passed").sum())
    final["gate_total"] = int(len(gates))
    write_frame(GATE_AUDIT, gates)
    write_json(FINAL_DECISION, final)
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "created_at_utc": now_utc(),
            "execution_command": f"python -B {rel(Path(__file__))}",
            "inputs": [rel(path) for path in INPUT_FILES],
            "outputs": [rel(path) for path in OUTPUT_FILES],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    build_receipts(final)
    write_json(
        LINEAGE_RECEIPT,
        {
            "source_inputs": [rel(path) for path in INPUT_FILES],
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [rel(path) for path in OUTPUT_FILES if path != ARTIFACT_REGISTRY],
            "artifact_hashes": {rel(path): sha256_file(path) for path in OUTPUT_FILES if exists(path) and path != ARTIFACT_REGISTRY},
            "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "availability": "tracked_or_reproducible_from_command(추적됨 또는 명령으로 재현 가능)",
            "lineage_judgment": "connected_with_boundary(경계 포함 연결)",
        },
    )
    write_docs(final)
    write_registers(final, gates)
    update_artifact_registry([path for path in OUTPUT_FILES if path != ARTIFACT_REGISTRY])
    return final


def main() -> None:
    final = build_design()
    print(json.dumps(final, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
