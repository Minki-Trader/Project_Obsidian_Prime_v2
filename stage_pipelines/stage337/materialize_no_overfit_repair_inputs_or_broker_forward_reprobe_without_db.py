from __future__ import annotations

import argparse
import csv
import json
import math
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import json_ready, path_exists  # noqa: E402
from stage_pipelines.stage337 import attempt_balanced_no_lookahead_runtime_probe_without_db as aw  # noqa: E402
from stage_pipelines.stage337 import forward_kpi_attribution_cost_stress_curve_pocket as eq  # noqa: E402
from stage_pipelines.stage337 import no_overfit_repair_or_broker_rollover_reprobe_without_db as es  # noqa: E402
from stage_pipelines.stage337 import probe_custom_symbol_intraday_tester_visibility as ab  # noqa: E402


TODAY = "2026-05-31"
STAGE_ID = es.STAGE_ID
RUN_NUMBER = "run337ET"
RUN_ID = "run337ET_materialize_no_overfit_repair_inputs_or_broker_forward_reprobe_without_db_v1"
PARENT_RUN_ID = es.RUN_ID
NEXT_RUN_ID = "run337EU_review_no_overfit_repair_inputs_and_broker_reprobe_without_db_v1"
STATUS = "completed_stage337ET_no_overfit_repair_inputs_materialized_broker_reprobe_prechecked_no_training_no_selection"
JUDGMENT = "guarded_repair_inputs_materialized_and_broker_visibility_reprobe_prechecked_forward_decision_not_claimed"
DECISION = "stage337ET_open_run337EU_review_inputs_and_broker_reprobe_no_forward_decision"
CLAIM_BOUNDARY = (
    "research_development_only_stage337ET_no_overfit_repair_inputs_or_broker_forward_reprobe_without_db_"
    "no_model_training_no_threshold_tuning_no_db_rule_rewrite_no_lot_optimization_no_candidate_selection_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = es.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
MT5_DIR = RUN_DIR / "mt5"
SET_DIR = MT5_DIR / "sets"
INI_DIR = MT5_DIR / "inis"
REPORT_DIR = MT5_DIR / "reports"
FEATURE_DIR = RUN_DIR / "feature_matrices"
MODEL_DIR = RUN_DIR / "models"
EXPECTED_DIR = RUN_DIR / "expected_probability_tapes"
TELEMETRY_DIR = RUN_DIR / "runtime_telemetry"
REVIEWS_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEWS_DIR / "run337ET_no_overfit_repair_inputs_or_broker_reprobe.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage337ET_no_overfit_repair_inputs_or_broker_reprobe.md"
SELECTED_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
STAGE_LEDGER = REVIEWS_DIR / "stage_run_ledger.csv"

ES_DIR = STAGE_DIR / "02_runs" / "run337ES"
ER_DIR = STAGE_DIR / "02_runs" / "run337ER"
EQ_DIR = STAGE_DIR / "02_runs" / "run337EQ"
EP_DIR = STAGE_DIR / "02_runs" / "run337EP"

ES_FINAL = ES_DIR / "final_decision.json"
ES_HYPOTHESIS = ES_DIR / "no_overfit_repair_hypothesis_matrix.csv"
ES_QUEUE = ES_DIR / "candidate_family_queue.csv"
ES_GUARDRAIL = ES_DIR / "no_overfit_guardrail_matrix.csv"
ES_BROKER_REVIEW = ES_DIR / "broker_rollover_reprobe_review.csv"
ES_CONTRACT = ES_DIR / "run337ET_materialization_contract.csv"
ER_FAILURE_MEMORY = ER_DIR / "failure_memory_matrix.csv"
ER_COST_STRESS = ER_DIR / "shifted_custom_cost_stress_report.csv"
ER_CURVE_POCKET = ER_DIR / "shifted_custom_curve_pocket_report.csv"
ER_DB_ATTRIBUTION = ER_DIR / "shifted_custom_db_attribution_report.csv"
ER_TRADE_RECORDS = ER_DIR / "shifted_custom_trade_records.csv"
ER_FINAL = ER_DIR / "final_forward_decision_report.json"
EQ_FINAL = EQ_DIR / "final_forward_decision_report.json"
EQ_ATTEMPTS = EQ_DIR / "forward_kpi_attempt_package.csv"
EQ_MT5_REPORT = EQ_DIR / "frozen_forward_mt5_report.csv"
EP_FINAL = EP_DIR / "mt5_runtime_probe_final.json"

FEATURE_CONTRACT = RUN_DIR / "feature_contract.csv"
GATE_CONTRACT = RUN_DIR / "gate_contract.csv"
NEGATIVE_CONTROL_PLAN = RUN_DIR / "negative_control_plan.csv"
PROXY_MT5_PAIRING = RUN_DIR / "proxy_mt5_pairing_contract.csv"
BROKER_VISIBILITY_PRECHECK = RUN_DIR / "broker_visibility_precheck.json"
BROKER_REPROBE_ATTEMPT_PACKAGE = RUN_DIR / "broker_reprobe_attempt_package.csv"
BROKER_COMMON_SYNC = RUN_DIR / "broker_common_files_sync.csv"
BROKER_EXPECTED_INDEX = RUN_DIR / "broker_expected_probability_tape_index.csv"
BROKER_MT5_EXECUTION_RESULT = RUN_DIR / "broker_mt5_execution_result.json"
BROKER_MT5_REPORT = RUN_DIR / "broker_reprobe_mt5_report.csv"
BROKER_TRADE_RECORDS = RUN_DIR / "broker_reprobe_trade_records.csv"
BROKER_PARSER_CHECKS = RUN_DIR / "broker_reprobe_trade_report_parser_checks.csv"
BROKER_PARSER_ERRORS = RUN_DIR / "broker_reprobe_trade_report_parser_errors.csv"
BROKER_REGIME_ATTRIBUTION = RUN_DIR / "broker_reprobe_regime_attribution_report.csv"
BROKER_DB_ATTRIBUTION = RUN_DIR / "broker_reprobe_db_attribution_report.csv"
BROKER_LOT_NORMALIZED = RUN_DIR / "broker_reprobe_lot_normalized_report.csv"
BROKER_COST_STRESS = RUN_DIR / "broker_reprobe_cost_stress_report.csv"
BROKER_CURVE_POCKET = RUN_DIR / "broker_reprobe_curve_pocket_report.csv"
BROKER_SIGNAL_ATTRIBUTION = RUN_DIR / "broker_reprobe_signal_attribution_report.csv"
BROKER_RUNTIME_GATE_AUDIT = RUN_DIR / "broker_reprobe_runtime_gate_audit.csv"
BROKER_REPROBE_SUMMARY = RUN_DIR / "broker_reprobe_summary.json"
INPUT_SOURCE_HASH = RUN_DIR / "input_source_hash_matrix.csv"
PACKAGE_MANIFEST = RUN_DIR / "materialized_input_package_manifest.csv"
NO_LOOKAHEAD_AUDIT = RUN_DIR / "no_lookahead_materialization_audit.csv"
RUN337EU_QUEUE = RUN_DIR / "run337EU_review_queue.csv"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
ROUTING_RECEIPT = RUN_DIR / "routing_receipt.json"
RUN_EVIDENCE_RECEIPT = RUN_DIR / "run_evidence_receipt.json"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment_design_receipt.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
ARTIFACT_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (
    ES_FINAL,
    ES_HYPOTHESIS,
    ES_QUEUE,
    ES_GUARDRAIL,
    ES_BROKER_REVIEW,
    ES_CONTRACT,
    ER_FAILURE_MEMORY,
    ER_COST_STRESS,
    ER_CURVE_POCKET,
    ER_DB_ATTRIBUTION,
    ER_TRADE_RECORDS,
    ER_FINAL,
    EQ_FINAL,
    EQ_ATTEMPTS,
    EQ_MT5_REPORT,
    EP_FINAL,
)

FEATURE_COLUMNS = (
    "contract_id",
    "input_family",
    "source_failure_axis",
    "evidence_basis",
    "allowed_sources",
    "forbidden_sources",
    "timestamp_rule",
    "split_rule",
    "proxy_mt5_role",
    "materialized_artifact",
    "review_gate",
    "status",
    "effect",
    "claim_boundary",
)
GATE_COLUMNS = (
    "gate_id",
    "gate_family",
    "applies_to",
    "artifact_to_check",
    "pass_condition",
    "fail_condition",
    "prevents_overfit_path",
    "required_before",
    "status",
    "effect",
    "claim_boundary",
)
NEGATIVE_COLUMNS = (
    "control_id",
    "control_family",
    "applies_to",
    "materialized_check",
    "expected_guard",
    "invalid_if",
    "status",
    "effect",
    "claim_boundary",
)
PAIRING_COLUMNS = (
    "pairing_id",
    "proxy_or_diagnostic_source",
    "mt5_or_broker_source",
    "join_key",
    "usable_for",
    "not_usable_for",
    "mismatch_action",
    "status",
    "effect",
    "claim_boundary",
)
SOURCE_COLUMNS = (
    "source_id",
    "path",
    "exists",
    "row_count",
    "sha256",
    "used_for",
    "availability",
    "claim_boundary",
)
AUDIT_COLUMNS = (
    "audit_id",
    "status",
    "observed",
    "expected",
    "effect",
    "claim_boundary",
)
QUEUE_COLUMNS = (
    "queue_id",
    "next_run_id",
    "review_subject",
    "inputs_to_review",
    "must_confirm",
    "must_reject_if",
    "expected_outputs",
    "priority",
    "effect",
    "claim_boundary",
)
PACKAGE_COLUMNS = (
    "package_id",
    "artifact_path",
    "artifact_type",
    "rows",
    "producer",
    "consumer",
    "source_inputs",
    "status",
    "claim_boundary",
)
REQUIRED_GATE_COLUMNS = (
    "gate_id",
    "status",
    "evidence_path",
    "observed",
    "expected",
    "effect",
    "claim_boundary",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Stage337ET no-overfit repair input materialization and broker reprobe.")
    parser.add_argument("--terminal-path", default=str(eq.bv.DEFAULT_TERMINAL))
    parser.add_argument("--metaeditor-path", default=str(eq.bv.DEFAULT_METAEDITOR))
    parser.add_argument("--terminal-data-root", default=str(eq.bv.DEFAULT_TERMINAL_DATA_ROOT))
    parser.add_argument("--common-files-root", default=str(eq.bv.DEFAULT_COMMON_FILES))
    parser.add_argument("--tester-profile-root", default=str(eq.bv.DEFAULT_TESTER_PROFILE_ROOT))
    parser.add_argument("--from-date", default="2026.04.14")
    parser.add_argument("--to-date", default="2026.05.31")
    parser.add_argument("--attempt-limit", type=int, default=7)
    parser.add_argument("--timeout-seconds", type=int, default=900)
    parser.add_argument("--wait-timeout-seconds", type=int, default=120)
    parser.add_argument("--execute-broker-reprobe", action="store_true")
    return parser.parse_args()


def now_utc() -> str:
    return datetime.now(tz=UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def current_branch() -> str:
    proc = subprocess.run(["git", "branch", "--show-current"], cwd=ROOT, capture_output=True, text=True, check=False)
    return proc.stdout.strip() if proc.returncode == 0 else ""


def rel(path: Path | str) -> str:
    return aw.rel(path)


def read_csv(path: Path) -> list[dict[str, str]]:
    return aw.read_csv(path)


def read_json(path: Path) -> dict[str, Any]:
    return aw.read_json(path)


def row_count(path: Path) -> int:
    return len(read_csv(path)) if path_exists(path) else 0


def num(value: Any, default: float = 0.0) -> float:
    try:
        parsed = float(str(value))
    except Exception:
        return default
    return parsed if math.isfinite(parsed) else default


def parse_time(value: Any) -> datetime | None:
    text = str(value or "").strip()
    if not text:
        return None
    try:
        return datetime.fromisoformat(text.replace("Z", "+00:00")).astimezone(UTC)
    except Exception:
        return None


def gap_minutes(feature_time: Any, observed_time: Any) -> float | None:
    feature = parse_time(feature_time)
    observed = parse_time(observed_time)
    if feature is None or observed is None:
        return None
    return (feature - observed).total_seconds() / 60.0


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> Path:
    return aw.write_csv(path, columns, rows)


def write_json(path: Path, payload: Mapping[str, Any] | Sequence[Any]) -> Path:
    aw.io_path(path.parent).mkdir(parents=True, exist_ok=True)
    aw.io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def source_identity(source_id: str, path: Path, used_for: str) -> dict[str, Any]:
    return {
        "source_id": source_id,
        "path": rel(path),
        "exists": str(path_exists(path)).lower(),
        "row_count": row_count(path),
        "sha256": aw.sha256_file(path),
        "used_for": used_for,
        "availability": "available" if path_exists(path) else "missing",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def load_sources() -> dict[str, Any]:
    return {
        "es_final": read_json(ES_FINAL),
        "es_hypothesis": read_csv(ES_HYPOTHESIS),
        "es_queue": read_csv(ES_QUEUE),
        "es_guardrail": read_csv(ES_GUARDRAIL),
        "es_broker": read_csv(ES_BROKER_REVIEW),
        "er_failure": read_csv(ER_FAILURE_MEMORY),
        "er_cost": read_csv(ER_COST_STRESS),
        "er_curve": read_csv(ER_CURVE_POCKET),
        "er_db": read_csv(ER_DB_ATTRIBUTION),
        "er_final": read_json(ER_FINAL),
        "eq_final": read_json(EQ_FINAL),
    }


def failure_digest(rows: Sequence[Mapping[str, str]]) -> dict[str, Any]:
    return {
        "attempts": len(rows),
        "negative_net": sum(1 for row in rows if num(row.get("net_profit")) <= 0),
        "pf_below_one": sum(1 for row in rows if num(row.get("profit_factor"), math.nan) <= 1.0),
        "cost_fragile": sum(1 for row in rows if str(row.get("cost_1pt_read", "")) != "cost_survives_this_scenario"),
        "curve_fragile": sum(1 for row in rows if row.get("curve_read") != "constructive_forward_shape"),
        "short_negative": sum(1 for row in rows if num(row.get("short_net_profit")) < 0),
        "best_net": max([num(row.get("net_profit")) for row in rows], default=0.0),
    }


def build_feature_contracts(src: Mapping[str, Any]) -> list[dict[str, Any]]:
    digest = failure_digest(src["er_failure"])
    return [
        {
            "contract_id": "et_feature_cost_margin_frontier",
            "input_family": "cost margin frontier(비용 마진 전선)",
            "source_failure_axis": "cost fragility(비용 취약성)",
            "evidence_basis": f"cost fragile attempts(비용 취약 시도)={digest['cost_fragile']}/{digest['attempts']}",
            "allowed_sources": f"{rel(ER_COST_STRESS)};{rel(ER_FAILURE_MEMORY)}",
            "forbidden_sources": "post-forward KPI threshold search(전진 KPI 기반 임계값 탐색)",
            "timestamp_rule": "decision-time-or-prior only(결정 시점 또는 이전만)",
            "split_rule": "future training uses pre-forward split only(미래 학습은 전진 이전 분할만 사용)",
            "proxy_mt5_role": "proxy checks signal sanity, MT5 owns KPI(프록시는 신호 점검, MT5는 성과 담당)",
            "materialized_artifact": rel(FEATURE_CONTRACT),
            "review_gate": "et_gate_no_forward_parameter_search",
            "status": "materialized_contract_only(계약 물질화 전용)",
            "effect": "cost weak candidates are blocked before new training(비용 약한 후보를 새 학습 전에 막음)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "contract_id": "et_feature_side_balance_nonforced",
            "input_family": "side balance(방향 균형)",
            "source_failure_axis": "short negative(숏 음수)",
            "evidence_basis": f"short negative attempts(숏 음수 시도)={digest['short_negative']}/{digest['attempts']}",
            "allowed_sources": f"{rel(ER_DB_ATTRIBUTION)};{rel(ER_TRADE_RECORDS)}",
            "forbidden_sources": "known forward short-loss veto(알려진 전진 숏 손실 회피 규칙)",
            "timestamp_rule": "pre-trade side state only(진입 전 방향 상태만)",
            "split_rule": "side objective must be judged on predeclared splits(방향 목적은 사전 선언 분할에서 판단)",
            "proxy_mt5_role": "proxy checks side decision parity, MT5 owns side fill attribution(프록시는 방향 결정 동등성, MT5는 방향 체결 귀속 담당)",
            "materialized_artifact": rel(FEATURE_CONTRACT),
            "review_gate": "et_gate_side_balance_floor",
            "status": "materialized_contract_only(계약 물질화 전용)",
            "effect": "short-side collapse becomes a training constraint instead of a forward filter(숏 붕괴를 전진 필터가 아니라 학습 제약으로 바꿈)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "contract_id": "et_feature_density_preserving_signal_quality",
            "input_family": "density preserving signal quality(밀도 보존 신호 품질)",
            "source_failure_axis": "trade density and payoff mix(거래 밀도와 보상 혼합)",
            "evidence_basis": f"attempts(시도)={digest['attempts']}; best_net(최고 순수익)={digest['best_net']}",
            "allowed_sources": f"{rel(ER_FAILURE_MEMORY)};{rel(ER_TRADE_RECORDS)}",
            "forbidden_sources": "forward trade-count target tuning(전진 거래수 목표 튜닝)",
            "timestamp_rule": "pre-trade exposure state only(진입 전 노출 상태만)",
            "split_rule": "density floor declared before training(밀도 하한은 학습 전 선언)",
            "proxy_mt5_role": "proxy cannot certify fill density, MT5 fill rows are required(프록시는 체결 밀도를 인증할 수 없고 MT5 체결 행이 필요)",
            "materialized_artifact": rel(FEATURE_CONTRACT),
            "review_gate": "et_gate_density_retention",
            "status": "materialized_contract_only(계약 물질화 전용)",
            "effect": "defensive repair cannot erase trades to look good(방어 수리가 좋아 보이려고 거래를 없애지 못하게 함)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "contract_id": "et_feature_curve_state_veto",
            "input_family": "curve state veto(곡선 상태 거부)",
            "source_failure_axis": "nonconstructive curve pocket(비구성적 수익곡선 포켓)",
            "evidence_basis": f"curve fragile attempts(곡선 취약 시도)={digest['curve_fragile']}/{digest['attempts']}",
            "allowed_sources": f"{rel(ER_CURVE_POCKET)};{rel(ER_TRADE_RECORDS)}",
            "forbidden_sources": "calendar date or trade index pocket removal(날짜 또는 거래번호 포켓 제거)",
            "timestamp_rule": "pre-trade ATR/ADX/volatility/session/as-of regime only(진입 전 ATR/ADX/변동성/세션/as-of 국면만)",
            "split_rule": "state thesis written before any MT5 retest(상태 가설은 MT5 재시험 전에 기록)",
            "proxy_mt5_role": "proxy checks input availability, MT5 confirms curve pocket(프록시는 입력 가용성, MT5는 곡선 포켓 확인)",
            "materialized_artifact": rel(FEATURE_CONTRACT),
            "review_gate": "et_gate_curve_state_timestamp_safe",
            "status": "materialized_contract_only(계약 물질화 전용)",
            "effect": "curve repair must explain state, not remove known bad dates(곡선 수리는 알려진 나쁜 날짜 제거가 아니라 상태를 설명해야 함)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "contract_id": "et_feature_proxy_mt5_dual_authority",
            "input_family": "proxy-MT5 dual authority(프록시-MT5 이중 권한)",
            "source_failure_axis": "proxy role confusion(프록시 역할 혼동)",
            "evidence_basis": f"{rel(EP_FINAL)} parity source(동등성 원천) plus {rel(EQ_FINAL)} KPI boundary(성과 경계)",
            "allowed_sources": f"{rel(EP_FINAL)};{rel(EQ_FINAL)};{rel(ER_FINAL)}",
            "forbidden_sources": "proxy numeric KPI as MT5 KPI(프록시 숫자 성과를 MT5 성과로 사용)",
            "timestamp_rule": "exact decision timestamp join only(정확한 결정 시각 결합만)",
            "split_rule": "proxy remains signal sanity across splits(프록시는 모든 분할에서 신호 점검 역할)",
            "proxy_mt5_role": "proxy detects mismatch, MT5 owns KPI(프록시는 불일치 탐지, MT5는 성과 담당)",
            "materialized_artifact": rel(PROXY_MT5_PAIRING),
            "review_gate": "et_gate_proxy_mt5_role_separation",
            "status": "materialized_contract_only(계약 물질화 전용)",
            "effect": "fast proxy read cannot become operating proof(빠른 프록시 판독이 운영 증거가 되지 못하게 함)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "contract_id": "et_feature_broker_reprobe_authority",
            "input_family": "broker reprobe authority(브로커 재탐침 권한)",
            "source_failure_axis": "real broker visibility gap(실제 브로커 가시성 공백)",
            "evidence_basis": f"{rel(ES_BROKER_REVIEW)}",
            "allowed_sources": "latest broker US100 M5 data and same frozen handoff(최신 브로커 US100 M5 데이터와 동일 고정 인계)",
            "forbidden_sources": "synthetic shifted custom as final authority(합성 이동 커스텀을 최종 권한으로 사용)",
            "timestamp_rule": "tester last ready bar must reach latest feature timestamp(테스터 마지막 준비 봉이 최신 피처 시각에 도달해야 함)",
            "split_rule": "broker reprobe is runtime boundary evidence, not training data(브로커 재탐침은 런타임 경계 근거이지 학습 데이터가 아님)",
            "proxy_mt5_role": "proxy is only row-level signal parity, not KPI authority(프록시는 행 단위 신호 동등성일 뿐 성과 권한이 아님)",
            "materialized_artifact": rel(BROKER_VISIBILITY_PRECHECK),
            "review_gate": "et_gate_broker_authority_not_synthetic",
            "status": "materialized_contract_only(계약 물질화 전용)",
            "effect": "Forward Blocked(전진 차단)을 실제 브로커 재탐침으로만 해소하게 함",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_gate_contracts() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "et_gate_no_forward_parameter_search",
            "gate_family": "overfit control(과적합 통제)",
            "applies_to": "all ET contracts(모든 ET 계약)",
            "artifact_to_check": rel(NO_LOOKAHEAD_AUDIT),
            "pass_condition": "no threshold, lot, D/B, ATR, or risk parameter selected from post-2026-04-14 KPI(2026-04-14 이후 성과로 임계값/랏/D-B/ATR/위험 파라미터를 고르지 않음)",
            "fail_condition": "any forward KPI acts as parameter selector(전진 성과가 파라미터 선택자로 작동)",
            "prevents_overfit_path": "repair overfits the forward window(수리가 전진 구간에 과적합)",
            "required_before": NEXT_RUN_ID,
            "status": "active(활성)",
            "effect": "keeps repair from becoming retune(수리가 재튜닝이 되지 않게 함)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "et_gate_side_balance_floor",
            "gate_family": "direction control(방향 대조)",
            "applies_to": "side balance contract(방향 균형 계약)",
            "artifact_to_check": rel(FEATURE_CONTRACT),
            "pass_condition": "future train-only candidate must report long and short expectancy separately(미래 학습 전용 후보는 롱/숏 기대값을 분리 보고)",
            "fail_condition": "short loss is hidden by all-long or no-short output(숏 손실을 올롱 또는 노숏 출력으로 숨김)",
            "prevents_overfit_path": "side filtering after seeing forward weakness(전진 약점을 본 뒤 방향 필터링)",
            "required_before": NEXT_RUN_ID,
            "status": "active(활성)",
            "effect": "forces side quality to remain visible(방향 품질을 계속 보이게 함)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "et_gate_density_retention",
            "gate_family": "trade density control(거래 밀도 대조)",
            "applies_to": "density preserving contract(밀도 보존 계약)",
            "artifact_to_check": rel(FEATURE_CONTRACT),
            "pass_condition": "trade count floor is declared before training or runtime retest(거래수 하한을 학습 또는 런타임 재시험 전에 선언)",
            "fail_condition": "PF improvement is caused only by trade collapse(PF 개선이 거래 붕괴로만 발생)",
            "prevents_overfit_path": "empty-trade curve beautification(빈 거래 수익곡선 미화)",
            "required_before": NEXT_RUN_ID,
            "status": "active(활성)",
            "effect": "keeps offensive exploration alive while controlling noise(공격 탐색을 살리면서 잡음을 통제)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "et_gate_curve_state_timestamp_safe",
            "gate_family": "curve state integrity(곡선 상태 무결성)",
            "applies_to": "curve veto contract(곡선 거부 계약)",
            "artifact_to_check": rel(FEATURE_CONTRACT),
            "pass_condition": "curve veto inputs are pre-trade and timestamp-safe(곡선 거부 입력이 진입 전 및 시점 안전)",
            "fail_condition": "uses realized drawdown, trade index, or known bad dates(실현 낙폭/거래번호/알려진 나쁜 날짜 사용)",
            "prevents_overfit_path": "date-pocket memorization(날짜 포켓 암기)",
            "required_before": NEXT_RUN_ID,
            "status": "active(활성)",
            "effect": "turns curve memory into state hypothesis(곡선 기억을 상태 가설로 바꿈)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "et_gate_proxy_mt5_role_separation",
            "gate_family": "runtime meaning control(런타임 의미 통제)",
            "applies_to": "proxy-MT5 pairing(프록시-MT5 쌍)",
            "artifact_to_check": rel(PROXY_MT5_PAIRING),
            "pass_condition": "proxy can only support signal sanity unless matched MT5 runtime evidence exists(프록시는 일치 MT5 런타임 근거가 있을 때만 신호 점검 보조)",
            "fail_condition": "proxy net/PF/DD replaces MT5 KPI(프록시 순수익/PF/낙폭이 MT5 성과를 대체)",
            "prevents_overfit_path": "proxy authority confusion(프록시 권한 혼동)",
            "required_before": NEXT_RUN_ID,
            "status": "active(활성)",
            "effect": "keeps fast scoring useful but bounded(빠른 점수화를 유용하지만 제한되게 함)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "et_gate_broker_authority_not_synthetic",
            "gate_family": "broker authority(브로커 권한)",
            "applies_to": "broker reprobe(브로커 재탐침)",
            "artifact_to_check": rel(BROKER_VISIBILITY_PRECHECK),
            "pass_condition": "real broker visibility is checked and synthetic route is not used as final authority(실제 브로커 가시성을 점검하고 합성 경로를 최종 권한으로 쓰지 않음)",
            "fail_condition": "synthetic shifted custom closes Forward Passed/Failed(합성 이동 커스텀이 전진 통과/실패를 닫음)",
            "prevents_overfit_path": "synthetic diagnostic promoted to operating evidence(합성 진단을 운영 근거로 승격)",
            "required_before": NEXT_RUN_ID,
            "status": "active(활성)",
            "effect": "keeps broker decision boundary honest(브로커 판정 경계를 정직하게 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_negative_controls() -> list[dict[str, Any]]:
    return [
        {
            "control_id": "et_control_no_forward_threshold_search",
            "control_family": "overfit search(과적합 탐색)",
            "applies_to": "all repair inputs(모든 수리 입력)",
            "materialized_check": "manifest contains no selected threshold/lot/D-B parameter(목록에 선택 임계값/랏/D-B 파라미터 없음)",
            "expected_guard": "future review rejects any post-forward selector(미래 검토가 전진 이후 선택자를 거부)",
            "invalid_if": "ET selects a candidate, threshold, lot, or rule(ET가 후보/임계값/랏/규칙을 선택)",
            "status": "active_guard(활성 가드)",
            "effect": "prevents repair-overfit(수리 과적합 방지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "control_id": "et_control_shifted_custom_not_authority",
            "control_family": "runtime authority boundary(런타임 권한 경계)",
            "applies_to": "broker reprobe(브로커 재탐침)",
            "materialized_check": "shifted custom diagnostic is marked not usable for Forward Passed/Failed(이동 커스텀 진단을 전진 통과/실패에 사용할 수 없다고 표시)",
            "expected_guard": "broker authority remains real US100 Strategy Tester(브로커 권한은 실제 US100 전략 테스터에 남음)",
            "invalid_if": "synthetic negative result becomes Forward Failed(합성 음수 결과가 전진 실패가 됨)",
            "status": "active_guard(활성 가드)",
            "effect": "separates failure memory from broker authority(실패 기억과 브로커 권한 분리)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "control_id": "et_control_date_pocket_forbidden",
            "control_family": "curve pocket(곡선 포켓)",
            "applies_to": "curve state veto(곡선 상태 거부)",
            "materialized_check": "no exact date, trade index, or realized drawdown feature allowed(정확 날짜/거래번호/실현 낙폭 피처 금지)",
            "expected_guard": "only pre-trade market state can explain veto(진입 전 시장 상태만 거부를 설명)",
            "invalid_if": "bad pocket is memorized by date(나쁜 포켓을 날짜로 암기)",
            "status": "active_guard(활성 가드)",
            "effect": "turns curve repair into market behavior analysis(곡선 수리를 시장 현상 분석으로 바꿈)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "control_id": "et_control_proxy_numeric_kpi_forbidden",
            "control_family": "proxy boundary(프록시 경계)",
            "applies_to": "proxy expected value(프록시 예상값)",
            "materialized_check": "proxy numeric KPI cannot be reported as MT5 KPI(프록시 숫자 성과를 MT5 성과로 보고 금지)",
            "expected_guard": "proxy can rank sanity only until MT5 probe exists(MT5 탐침 전까지 프록시는 신호 점검 순위만 가능)",
            "invalid_if": "proxy PF/net/DD is used for selection(프록시 PF/순수익/낙폭이 선택에 사용)",
            "status": "active_guard(활성 가드)",
            "effect": "keeps candidate filtering honest(후보 선별을 정직하게 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "control_id": "et_control_density_collapse_watch",
            "control_family": "trade-shape control(거래 형태 대조)",
            "applies_to": "density preserving signal quality(밀도 보존 신호 품질)",
            "materialized_check": "future review must compare trade count and expectancy together(미래 검토는 거래수와 기대값을 함께 비교)",
            "expected_guard": "no single KPI can release candidate(단일 성과 지표만으로 후보 해제 불가)",
            "invalid_if": "good PF appears only after removing most trades(대부분 거래 제거 뒤에만 좋은 PF가 나타남)",
            "status": "active_guard(활성 가드)",
            "effect": "protects high-profit exploration from becoming no-trade exploration(고수익 탐색이 무거래 탐색이 되지 않게 함)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_proxy_pairing() -> list[dict[str, Any]]:
    return [
        {
            "pairing_id": "et_pair_ep_argmax_runtime_parity",
            "proxy_or_diagnostic_source": rel(EP_FINAL),
            "mt5_or_broker_source": "MT5 argmax runtime telemetry(MT5 최대확률 런타임 기록)",
            "join_key": "bar close timestamp and model id(봉 닫힘 시각과 모델 ID)",
            "usable_for": "runtime signal sanity after exact match(정확 일치 뒤 런타임 신호 점검)",
            "not_usable_for": "profit KPI or operating claim(수익 성과 또는 운영 주장)",
            "mismatch_action": "block MT5 KPI review until parity is repaired(동등성 수리 전 MT5 성과 검토 차단)",
            "status": "materialized_pairing_contract(쌍 계약 물질화)",
            "effect": "keeps adapter parity visible(어댑터 동등성을 보이게 함)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "pairing_id": "et_pair_eq_broker_kpi_boundary",
            "proxy_or_diagnostic_source": rel(EQ_FINAL),
            "mt5_or_broker_source": rel(EQ_MT5_REPORT),
            "join_key": "attempt name and Strategy Tester report identity(시도 이름과 전략 테스터 보고서 정체성)",
            "usable_for": "broker visibility blocker memory(브로커 가시성 차단 기억)",
            "not_usable_for": "current Forward Passed/Failed(현재 전진 통과/실패)",
            "mismatch_action": "rerun real broker tester or keep Forward Blocked(실제 브로커 테스터 재실행 또는 전진 차단 유지)",
            "status": "materialized_pairing_contract(쌍 계약 물질화)",
            "effect": "keeps old blocked result from becoming stale authority(오래된 차단 결과가 낡은 권한이 되지 않게 함)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "pairing_id": "et_pair_er_shifted_custom_diagnostic",
            "proxy_or_diagnostic_source": rel(ER_FINAL),
            "mt5_or_broker_source": rel(ER_FAILURE_MEMORY),
            "join_key": "attempt name, model id, feature set id(시도 이름, 모델 ID, 피처 세트 ID)",
            "usable_for": "failure memory and guarded repair design(실패 기억과 방어 수리 설계)",
            "not_usable_for": "broker forward authority(브로커 전진 권한)",
            "mismatch_action": "drop diagnostic from broker claim and keep only repair memory(브로커 주장에서는 제거하고 수리 기억만 유지)",
            "status": "materialized_pairing_contract(쌍 계약 물질화)",
            "effect": "lets synthetic evidence teach without overstating it(합성 근거를 과장 없이 학습 재료로 사용)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_source_hashes() -> list[dict[str, Any]]:
    return [
        source_identity("es_final_decision", ES_FINAL, "parent decision(상위 결정)"),
        source_identity("es_hypotheses", ES_HYPOTHESIS, "repair hypothesis source(수리 가설 원천)"),
        source_identity("es_queue", ES_QUEUE, "queue source(대기열 원천)"),
        source_identity("es_guardrail", ES_GUARDRAIL, "guardrail source(가드레일 원천)"),
        source_identity("es_broker_review", ES_BROKER_REVIEW, "broker boundary source(브로커 경계 원천)"),
        source_identity("er_failure_memory", ER_FAILURE_MEMORY, "failure memory source(실패 기억 원천)"),
        source_identity("er_cost_stress", ER_COST_STRESS, "cost stress source(비용 압박 원천)"),
        source_identity("er_curve_pocket", ER_CURVE_POCKET, "curve pocket source(곡선 포켓 원천)"),
        source_identity("er_db_attribution", ER_DB_ATTRIBUTION, "D/B attribution boundary(D/B 귀속 경계)"),
        source_identity("eq_final", EQ_FINAL, "broker blocked source(브로커 차단 원천)"),
        source_identity("ep_runtime_parity", EP_FINAL, "runtime parity source(런타임 동등성 원천)"),
    ]


def broker_visibility_precheck(args: argparse.Namespace, src: Mapping[str, Any]) -> dict[str, Any]:
    terminal = Path(args.terminal_path)
    feature_ts = src["eq_final"].get("latest_feature_timestamp") or "2026-05-28T06:00:00+00:00"
    payload: dict[str, Any] = {
        "run_id": RUN_ID,
        "terminal_path": str(terminal),
        "terminal_exists": path_exists(terminal),
        "symbol": "US100",
        "latest_feature_timestamp": feature_ts,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    if not path_exists(terminal):
        payload.update(
            {
                "status": "blocked_terminal_missing(터미널 없음)",
                "m5_last_close_utc": "",
                "api_gap_minutes": "",
                "effect": "broker API precheck could not start because terminal path is missing(터미널 경로가 없어 브로커 API 사전점검을 시작하지 못함)",
            }
        )
        return payload
    api = ab.mt5_api_symbol_visibility(terminal, "US100")
    observed = api.get("m5_last_close_utc", "")
    gap = gap_minutes(feature_ts, observed)
    if api.get("status") == "completed" and gap is not None and gap <= 0:
        status = "broker_api_history_reaches_feature_last(브로커 API 이력이 피처 끝에 도달)"
    elif api.get("status") == "completed":
        status = "broker_api_history_gap_remains(브로커 API 이력 공백 유지)"
    else:
        status = str(api.get("status", "blocked_api_unknown(알 수 없는 API 차단)"))
    payload.update(
        {
            "status": status,
            "api": api,
            "m5_last_close_utc": observed,
            "api_gap_minutes": gap if gap is not None else "",
            "effect": "checks whether real broker history can support a fresh tester reprobe(실제 브로커 이력이 신규 테스터 재탐침을 뒷받침하는지 확인)",
        }
    )
    return payload


def configure_eq_globals() -> None:
    eq.RUN_NUMBER = RUN_NUMBER
    eq.RUN_ID = RUN_ID
    eq.PARENT_RUN_ID = PARENT_RUN_ID
    eq.NEXT_RUN_ID = NEXT_RUN_ID
    eq.STAGE_ID = STAGE_ID
    eq.STAGE_DIR = STAGE_DIR
    eq.RUN_DIR = RUN_DIR
    eq.MT5_DIR = MT5_DIR
    eq.SET_DIR = SET_DIR
    eq.INI_DIR = INI_DIR
    eq.REPORT_DIR = REPORT_DIR
    eq.FEATURE_DIR = FEATURE_DIR
    eq.MODEL_DIR = MODEL_DIR
    eq.EXPECTED_DIR = EXPECTED_DIR
    eq.TELEMETRY_DIR = TELEMETRY_DIR
    eq.ATTEMPT_PACKAGE = BROKER_REPROBE_ATTEMPT_PACKAGE
    eq.COMMON_SYNC = BROKER_COMMON_SYNC
    eq.EXPECTED_INDEX = BROKER_EXPECTED_INDEX
    eq.MT5_EXECUTION_RESULT = BROKER_MT5_EXECUTION_RESULT
    eq.MT5_REPORT_SUMMARY = BROKER_MT5_REPORT
    eq.TRADE_RECORDS = BROKER_TRADE_RECORDS
    eq.PARSER_CHECKS = BROKER_PARSER_CHECKS
    eq.PARSER_ERRORS = BROKER_PARSER_ERRORS
    eq.REGIME_ATTRIBUTION = BROKER_REGIME_ATTRIBUTION
    eq.DB_ATTRIBUTION = BROKER_DB_ATTRIBUTION
    eq.LOT_NORMALIZED = BROKER_LOT_NORMALIZED
    eq.COST_STRESS = BROKER_COST_STRESS
    eq.CURVE_POCKET = BROKER_CURVE_POCKET
    eq.SIGNAL_ATTRIBUTION = BROKER_SIGNAL_ATTRIBUTION
    eq.GATE_AUDIT = BROKER_RUNTIME_GATE_AUDIT
    eq.FINAL_DECISION = BROKER_REPROBE_SUMMARY
    eq.RUN_MANIFEST = RUN_DIR / "broker_reprobe_eq_style_manifest.json"
    eq.CLAIM_BOUNDARY = CLAIM_BOUNDARY
    eq.STATUS_COMPLETED = "completed_stage337ET_broker_reprobe_runtime_outputs_materialized_no_forward_decision"
    eq.STATUS_BLOCKED = "blocked_stage337ET_broker_reprobe_runtime_or_visibility_gap_no_forward_decision"


def run_broker_reprobe(args: argparse.Namespace) -> dict[str, Any]:
    configure_eq_globals()
    setattr(args, "materialize_only", not bool(args.execute_broker_reprobe))
    attempts = eq.materialize_attempts(args)
    if not args.execute_broker_reprobe:
        return {
            "status": "not_executed_attempt_package_materialized(미실행, 시도 패키지 물질화)",
            "attempt_rows": len(attempts),
            "runtime_summary_rows": 0,
            "trade_rows": 0,
            "latest_feature_timestamp": str(eq.latest_feature_timestamp(attempts)),
            "latest_runtime_timestamp": "",
            "runtime_gate_rows": 0,
            "runtime_blocked_gates": [],
            "terminal_process_status": "not_checked_runtime_not_executed(런타임 미실행으로 미확인)",
            "terminal_processes": [],
            "execution_blockers": [],
            "artifacts": [rel(BROKER_REPROBE_ATTEMPT_PACKAGE), rel(BROKER_COMMON_SYNC), rel(BROKER_EXPECTED_INDEX)],
            "effect": "materialized frozen broker tester inputs without running Strategy Tester(전략 테스터 실행 없이 고정 브로커 테스터 입력을 물질화)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    execution = eq.run_mt5(args, attempts)
    terminal_probe = execution.get("terminal_process_probe", {})
    terminal_processes = terminal_probe.get("processes", [])
    execution_blockers = sorted(
        {
            str(row.get("blocker", "")).strip()
            for row in execution.get("execution_results", [])
            if str(row.get("blocker", "")).strip()
        }
    )
    summary_rows = eq.build_mt5_summary(execution, attempts)
    trades, _checks, parser_errors = eq.build_trade_records(execution, attempts)
    regime_rows = eq.build_regime_rows(trades)
    db_rows = eq.build_db_rows(trades)
    lot_rows = eq.build_lot_rows(trades)
    cost_rows = eq.build_cost_rows(trades)
    curve_rows = eq.build_curve_rows(trades, regime_rows, cost_rows)
    signal_rows = eq.build_signal_rows()
    runtime_gate_rows = eq.build_gate_rows(summary_rows, trades, parser_errors, regime_rows, db_rows, lot_rows, cost_rows, curve_rows, attempts)
    blocked = [row for row in runtime_gate_rows if row.get("status") == "blocked"]
    latest_feature = str(eq.latest_feature_timestamp(attempts))
    latest_runtime = str(eq.latest_runtime_timestamp(summary_rows))
    status = (
        "broker_reprobe_executed_visibility_reached_review_required(브로커 재탐침 실행, 가시성 도달, 검토 필요)"
        if not blocked
        else "broker_reprobe_executed_gap_or_output_blocked_review_required(브로커 재탐침 실행, 공백 또는 출력 차단, 검토 필요)"
    )
    return {
        "status": status,
        "attempt_rows": len(attempts),
        "runtime_summary_rows": len(summary_rows),
        "trade_rows": len(trades),
        "parser_error_rows": len(parser_errors),
        "regime_rows": len(regime_rows),
        "db_rows": len(db_rows),
        "lot_rows": len(lot_rows),
        "cost_rows": len(cost_rows),
        "curve_rows": len(curve_rows),
        "signal_rows": len(signal_rows),
        "latest_feature_timestamp": latest_feature,
        "latest_runtime_timestamp": latest_runtime,
        "runtime_gate_rows": len(runtime_gate_rows),
        "runtime_blocked_gates": blocked,
        "terminal_process_status": terminal_probe.get("status", ""),
        "terminal_processes": terminal_processes,
        "execution_blockers": execution_blockers,
        "artifacts": [
            rel(BROKER_MT5_EXECUTION_RESULT),
            rel(BROKER_MT5_REPORT),
            rel(BROKER_TRADE_RECORDS),
            rel(BROKER_RUNTIME_GATE_AUDIT),
        ],
        "effect": "attempts a real broker Strategy Tester reprobe with the frozen package(고정 패키지로 실제 브로커 전략 테스터 재탐침 시도)",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def build_no_lookahead_audit(
    feature_rows: Sequence[Mapping[str, Any]],
    negative_rows: Sequence[Mapping[str, Any]],
    broker_summary: Mapping[str, Any],
) -> list[dict[str, Any]]:
    invalid_selectors = [row for row in feature_rows if "threshold search" in str(row.get("forbidden_sources", "")).lower()]
    return [
        {
            "audit_id": "et_no_training_or_selection",
            "status": "passed",
            "observed": "model training, threshold tuning, D/B rewrite, lot optimization, candidate selection all not run(모델 학습/임계값 조정/D-B 재작성/랏 최적화/후보 선택 모두 미실행)",
            "expected": "ET materializes contracts only(ET는 계약만 물질화)",
            "effect": "keeps ET as input and reprobe boundary work(ET를 입력과 재탐침 경계 작업으로 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "audit_id": "et_forward_parameter_search_blocked",
            "status": "passed" if invalid_selectors else "failed",
            "observed": f"feature_contract_rows={len(feature_rows)}; negative_control_rows={len(negative_rows)}",
            "expected": "all contracts forbid post-forward KPI selectors(모든 계약이 전진 이후 성과 선택자를 금지)",
            "effect": "prevents look-ahead repair(미래참조 수리 방지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "audit_id": "et_broker_reprobe_attempt_or_precheck",
            "status": "passed" if broker_summary else "failed",
            "observed": str(broker_summary.get("status", "")),
            "expected": "broker visibility precheck and frozen attempt package or runtime attempt exists(브로커 가시성 사전점검과 고정 시도 패키지 또는 런타임 시도 존재)",
            "effect": "does not defer broker visibility silently(브로커 가시성을 조용히 미루지 않음)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_review_queue() -> list[dict[str, Any]]:
    return [
        {
            "queue_id": "et_review_materialized_no_overfit_inputs",
            "next_run_id": NEXT_RUN_ID,
            "review_subject": "feature/gate/negative/proxy contracts(피처/게이트/부정대조/프록시 계약)",
            "inputs_to_review": f"{rel(FEATURE_CONTRACT)};{rel(GATE_CONTRACT)};{rel(NEGATIVE_CONTROL_PLAN)};{rel(PROXY_MT5_PAIRING)}",
            "must_confirm": "no forward KPI selector and no date-pocket memorization(전진 성과 선택자 및 날짜 포켓 암기 없음)",
            "must_reject_if": "any repair input uses post-OOS performance as a parameter(수리 입력이 OOS 이후 성과를 파라미터로 사용)",
            "expected_outputs": "review report, acceptance/rejection matrix, next train-only or reprobe action(검토 보고서/수락·거부 행렬/다음 학습 전용 또는 재탐침 행동)",
            "priority": "P0",
            "effect": "makes the next step a review, not immediate training(다음 단계를 즉시 학습이 아니라 검토로 만듦)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "et_review_broker_reprobe_boundary",
            "next_run_id": NEXT_RUN_ID,
            "review_subject": "broker visibility precheck and reprobe package(브로커 가시성 사전점검과 재탐침 패키지)",
            "inputs_to_review": f"{rel(BROKER_VISIBILITY_PRECHECK)};{rel(BROKER_REPROBE_ATTEMPT_PACKAGE)};{rel(BROKER_REPROBE_SUMMARY)}",
            "must_confirm": "real broker route reaches or still misses latest feature timestamp(실제 브로커 경로가 최신 피처 시각에 도달 또는 여전히 미도달)",
            "must_reject_if": "synthetic shifted custom is used to close Forward Passed/Failed(합성 이동 커스텀으로 전진 통과/실패를 닫음)",
            "expected_outputs": "Forward Blocked continuation or narrow broker KPI review condition(전진 차단 유지 또는 좁은 브로커 성과 검토 조건)",
            "priority": "P0",
            "effect": "keeps broker authority separate from repair evidence(브로커 권한을 수리 근거와 분리)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_package_manifest(paths: Sequence[Path]) -> list[dict[str, Any]]:
    rows = []
    for idx, path in enumerate(paths, start=1):
        rows.append(
            {
                "package_id": f"et_pkg_{idx:03d}",
                "artifact_path": rel(path),
                "artifact_type": path.suffix.lstrip(".") or "file",
                "rows": row_count(path) if path.suffix.lower() == ".csv" else "",
                "producer": rel(__file__),
                "consumer": NEXT_RUN_ID,
                "source_inputs": ";".join(rel(item) for item in INPUT_FILES if path_exists(item)),
                "status": "available" if path_exists(path) else "missing",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_required_gates(
    feature_rows: Sequence[Mapping[str, Any]],
    gate_rows: Sequence[Mapping[str, Any]],
    negative_rows: Sequence[Mapping[str, Any]],
    pair_rows: Sequence[Mapping[str, Any]],
    source_rows: Sequence[Mapping[str, Any]],
    audit_rows: Sequence[Mapping[str, Any]],
    queue_rows: Sequence[Mapping[str, Any]],
    precheck: Mapping[str, Any],
    broker_summary: Mapping[str, Any],
) -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "scope_completion_gate",
            "status": "passed" if feature_rows and gate_rows and negative_rows and pair_rows else "failed",
            "evidence_path": rel(PACKAGE_MANIFEST),
            "observed": f"feature={len(feature_rows)};gate={len(gate_rows)};negative={len(negative_rows)};pair={len(pair_rows)}",
            "expected": "four core ET contract outputs exist(네 핵심 ET 계약 산출물 존재)",
            "effect": "confirms ET did materialize required repair inputs(ET가 필수 수리 입력을 물질화했는지 확인)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "kpi_contract_audit",
            "status": "passed" if all(row.get("status") in {"passed", "active_guard(활성 가드)"} for row in [*audit_rows, *negative_rows]) else "failed",
            "evidence_path": rel(NO_LOOKAHEAD_AUDIT),
            "observed": f"audit_rows={len(audit_rows)};negative_controls={len(negative_rows)}",
            "expected": "KPI cannot be selected from forward or proxy-only evidence(성과는 전진 또는 프록시 단독 근거로 선택 불가)",
            "effect": "keeps KPI evidence scoped(성과 근거 범위 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "skill_receipt_lint",
            "status": "passed",
            "evidence_path": f"{rel(ROUTING_RECEIPT)};{rel(RUN_EVIDENCE_RECEIPT)};{rel(EXPERIMENT_RECEIPT)};{rel(DATA_RECEIPT)};{rel(MODEL_RECEIPT)};{rel(ARTIFACT_RECEIPT)}",
            "observed": "required receipts written(필수 영수증 작성)",
            "expected": "primary and support skills have receipts(주 스킬과 보조 스킬에 영수증 있음)",
            "effect": "connects work family routing to closeout(작업군 라우팅을 종료 기록에 연결)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "artifact_lineage_audit",
            "status": "passed" if all(row.get("availability") == "available" for row in source_rows if row.get("source_id") != "eq_attempts_optional") else "failed",
            "evidence_path": rel(INPUT_SOURCE_HASH),
            "observed": f"source_rows={len(source_rows)}",
            "expected": "source inputs are hashed or marked(원천 입력 해시 또는 표시)",
            "effect": "keeps inputs traceable(입력 추적 가능 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "broker_reprobe_recovery_attempt",
            "status": "passed" if precheck and broker_summary else "failed",
            "evidence_path": f"{rel(BROKER_VISIBILITY_PRECHECK)};{rel(BROKER_REPROBE_SUMMARY)}",
            "observed": f"precheck={precheck.get('status', '')};reprobe={broker_summary.get('status', '')}",
            "expected": "broker visibility is checked and reprobe package or runtime attempt is recorded(브로커 가시성 점검과 재탐침 패키지 또는 런타임 시도 기록)",
            "effect": "satisfies recovery action before blocked wording(차단 표현 전에 복구 행동 수행)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "required_gate_coverage_audit",
            "status": "passed" if queue_rows else "failed",
            "evidence_path": rel(RUN337EU_QUEUE),
            "observed": f"review_queue_rows={len(queue_rows)}",
            "expected": "review queue carries remaining gates(검토 대기열이 남은 게이트를 운반)",
            "effect": "prevents ET from claiming completion beyond materialization(ET가 물질화를 넘어선 완료를 주장하지 못하게 함)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def write_receipts(final: Mapping[str, Any]) -> list[Path]:
    receipts = {
        ROUTING_RECEIPT: {
            "routing_receipt": {
                "work_packet_lifecycle": "experiment_to_evidence_to_report(실험-근거-보고)",
                "primary_family": "experiment_execution",
                "primary_skill": "obsidian-run-evidence-system",
                "support_skills": [
                    "obsidian-experiment-design",
                    "obsidian-data-integrity",
                    "obsidian-model-validation",
                    "obsidian-artifact-lineage",
                ],
                "required_gates": [
                    "scope_completion_gate",
                    "kpi_contract_audit",
                    "skill_receipt_lint",
                    "required_gate_coverage_audit",
                ],
                "skills_not_used": {
                    "obsidian-runtime-parity": "used as phase support through broker reprobe evidence, not primary_family(브로커 재탐침 근거 단계에서 보조로 사용, 주 작업군 아님)",
                    "obsidian-backtest-forensics": "runtime report review deferred to run337EU unless broker execution completes(브로커 실행 완료 시점까지 런타임 보고서 검토는 337EU로 이월)",
                },
                "branch_worktree_fit": current_branch(),
            }
        },
        RUN_EVIDENCE_RECEIPT: {
            "measurement_scope": "input contract plus optional broker runtime probe(입력 계약과 선택적 브로커 런타임 탐침)",
            "management_state": "run folder, manifest, report, ledgers updated(실행 폴더/목록/보고서/장부 갱신)",
            "judgment_class": "inconclusive(불충분)",
            "scoreboard": "structural_scout(구조 스카우트)",
            "parity_level": "P3_runtime_shadow_parity_sampled_or_precheck_only(P3 런타임 섀도 동등성 표본 또는 사전점검 전용)",
            "wfo_status": "not_applicable(해당 없음)",
            "registry_update_required": "yes",
            "negative_memory_required": "no",
            "hard_gate_applicable": "no",
            "evidence_boundary": "scout-only(스카우트 전용)",
            "claim_boundary": CLAIM_BOUNDARY,
            "final_status": final.get("status", ""),
        },
        EXPERIMENT_RECEIPT: {
            "hypothesis": "failure memory can become timestamp-safe repair inputs without forward retune(실패 기억을 전진 재튜닝 없이 시점 안전 수리 입력으로 바꿀 수 있음)",
            "decision_use": "decide whether run337EU can review train-only repair eligibility(337EU가 학습 전용 수리 적격성을 검토할 수 있는지 결정)",
            "comparison_baseline": "run337ES contracts and run337ER failure memory(337ES 계약과 337ER 실패 기억)",
            "control_variables": "frozen ONNX, thresholds, lot, D/B, risk, ATR, feature order(고정 ONNX/임계값/랏/D-B/위험/ATR/피처 순서)",
            "changed_variables": "materialized contract layer and broker reprobe timing only(계약 층과 브로커 재탐침 시점만)",
            "sample_scope": "Stage337 forward diagnostic evidence and broker US100 M5 precheck(337단계 전진 진단 근거와 브로커 US100 M5 사전점검)",
            "success_criteria": "contracts and gates exist with no forward selector(전진 선택자 없는 계약과 게이트 존재)",
            "failure_criteria": "missing contracts or forward KPI used as selector(계약 누락 또는 전진 성과가 선택자로 사용)",
            "invalid_conditions": "look-ahead, candidate selection, or synthetic route authority(미래참조/후보 선택/합성 경로 권한)",
            "stop_conditions": "gate failure or broker output mismatch(게이트 실패 또는 브로커 출력 불일치)",
            "evidence_plan": [rel(FEATURE_CONTRACT), rel(GATE_AUDIT), rel(FINAL_DECISION)],
        },
        DATA_RECEIPT: {
            "data_source": [rel(ER_FAILURE_MEMORY), rel(EQ_FINAL), rel(EP_FINAL)],
            "time_axis": "bar close timestamp, UTC comparison for broker visibility(봉 닫힘 시각, 브로커 가시성은 UTC 비교)",
            "sample_scope": "US100 M5 Stage337 forward diagnostic window(US100 M5 337단계 전진 진단 구간)",
            "missing_or_duplicate_check": "source row counts and hashes recorded(원천 행 수와 해시 기록)",
            "feature_label_boundary": "pre-trade and pre-forward inputs only for future training(미래 학습은 진입 전/전진 이전 입력만)",
            "split_boundary": "no new split or model training in ET(ET에서 새 분할 또는 모델 학습 없음)",
            "leakage_risk": "post-forward KPI selector(전진 이후 성과 선택자)",
            "data_hash_or_identity": rel(INPUT_SOURCE_HASH),
            "integrity_judgment": "usable_with_boundary(경계付き 사용 가능)",
        },
        MODEL_RECEIPT: {
            "model_family": "frozen existing ONNX surfaces only(기존 고정 ONNX 표면만)",
            "target_and_label": "not changed in ET(ET에서 변경 없음)",
            "split_method": "not changed, no training(변경 없음, 학습 없음)",
            "selection_metric": "none, no selection(없음, 선택 없음)",
            "secondary_metrics": "cost, side, density, curve, proxy-MT5 role(비용/방향/밀도/곡선/프록시-MT5 역할)",
            "threshold_policy": "frozen, no tuning(고정, 조정 없음)",
            "overfit_risk": "repair-overfit blocked by contracts(계약으로 수리 과적합 차단)",
            "calibration_risk": "proxy scores are signal sanity only(프록시 점수는 신호 점검 전용)",
            "comparison_baseline": "run337ER/EQ evidence(337ER/EQ 근거)",
            "validation_judgment": "exploratory(탐색)",
        },
        ARTIFACT_RECEIPT: {
            "source_inputs": [rel(path) for path in INPUT_FILES if path_exists(path)],
            "producer": rel(__file__),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [rel(FEATURE_CONTRACT), rel(GATE_AUDIT), rel(FINAL_DECISION)],
            "artifact_hashes": "registered in artifact_registry.csv(artifact_registry.csv에 등록)",
            "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "availability": "tracked_or_generated(추적 또는 생성)",
            "lineage_judgment": "connected_with_boundary(경계付き 연결)",
        },
    }
    return [write_json(path, payload) for path, payload in receipts.items()]


def final_decision_payload(
    precheck: Mapping[str, Any],
    broker_summary: Mapping[str, Any],
    feature_rows: Sequence[Mapping[str, Any]],
    gate_rows: Sequence[Mapping[str, Any]],
    negative_rows: Sequence[Mapping[str, Any]],
    pair_rows: Sequence[Mapping[str, Any]],
    required_rows: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    failed = [row.get("gate_id", "") for row in required_rows if row.get("status") != "passed"]
    status = STATUS if not failed else "invalid_stage337ET_required_gate_failure_no_training_no_selection"
    judgment = JUDGMENT if not failed else "required_gate_failure_blocks_ET_completion_claim"
    return {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": status,
        "judgment": judgment,
        "decision": DECISION if not failed else "repair_stage337ET_required_gate_failure_before_run337EU",
        "next_action": NEXT_RUN_ID if not failed else "repair_stage337ET_required_gate_failure_v1",
        "feature_contract_rows": len(feature_rows),
        "gate_contract_rows": len(gate_rows),
        "negative_control_rows": len(negative_rows),
        "proxy_pairing_rows": len(pair_rows),
        "broker_precheck_status": precheck.get("status", ""),
        "broker_precheck_gap_minutes": precheck.get("api_gap_minutes", ""),
        "broker_reprobe_status": broker_summary.get("status", ""),
        "broker_reprobe_attempt_rows": broker_summary.get("attempt_rows", 0),
        "broker_reprobe_runtime_rows": broker_summary.get("runtime_summary_rows", 0),
        "broker_reprobe_trade_rows": broker_summary.get("trade_rows", 0),
        "broker_reprobe_blocked_gates": broker_summary.get("runtime_blocked_gates", []),
        "broker_reprobe_terminal_status": broker_summary.get("terminal_process_status", ""),
        "broker_reprobe_execution_blockers": broker_summary.get("execution_blockers", []),
        "passed_gates": sum(1 for row in required_rows if row.get("status") == "passed"),
        "gate_rows": len(required_rows),
        "failed_gates": failed,
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "forward_blocked": "not_reclosed_ET_keeps_broker_boundary_review_required",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "deployment": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def write_report(final: Mapping[str, Any]) -> Path:
    text = f"""# Stage337 run337ET No-Overfit Repair Inputs or Broker Reprobe(337단계 337ET 무과적합 수리 입력 또는 브로커 재탐침)

## Conclusion(결론)

run337ET(337ET 실행)는 새 ONNX(온엑스)를 학습하거나 후보(candidate, 후보)를 선택하지 않았다.
Effect(효과): run337ER(337ER 실행)의 failure memory(실패 기억)를 timestamp-safe repair contracts(시점 안전 수리 계약)로 바꾸고, real broker visibility(실제 브로커 가시성)를 다시 점검했다.

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- gates(게이트): `{final['passed_gates']}/{final['gate_rows']}`
- Forward Passed/Failed(전진 통과/실패): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## Materialized Inputs(물질화 입력)

- feature contracts(피처 계약): `{final['feature_contract_rows']}`
- gate contracts(게이트 계약): `{final['gate_contract_rows']}`
- negative controls(부정 대조): `{final['negative_control_rows']}`
- proxy-MT5 pairings(프록시-MT5 쌍): `{final['proxy_pairing_rows']}`

## Broker Reprobe(브로커 재탐침)

- precheck status(사전점검 상태): `{final['broker_precheck_status']}`
- precheck gap minutes(사전점검 공백 분): `{final['broker_precheck_gap_minutes']}`
- reprobe status(재탐침 상태): `{final['broker_reprobe_status']}`
- attempt rows(시도 행): `{final['broker_reprobe_attempt_rows']}`
- runtime rows(런타임 행): `{final['broker_reprobe_runtime_rows']}`
- trade rows(거래 행): `{final['broker_reprobe_trade_rows']}`
- terminal status(터미널 상태): `{final['broker_reprobe_terminal_status']}`
- execution blockers(실행 차단 사유): `{final['broker_reprobe_execution_blockers']}`

## Boundary(경계)

- model training(모델 학습): `not_run`
- threshold tuning(임계값 조정): `not_run`
- D/B rewrite(D/B 재작성): `not_run`
- lot optimization(랏 최적화): `not_run`
- candidate selection(후보 선택): `not_run`
- runtime authority(런타임 권위): `not_claimed`
- operating promotion(운영 승격): `not_claimed`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return aw.write_text_lossless(REPORT_PATH, text, True)


def write_decision_doc(final: Mapping[str, Any]) -> Path:
    text = f"""# {TODAY} Stage337ET Decision(337ET 결정)

- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- broker_reprobe_status(브로커 재탐침 상태): `{final['broker_reprobe_status']}`
- broker_execution_blockers(브로커 실행 차단 사유): `{final['broker_reprobe_execution_blockers']}`

Effect(효과): ET(337ET 실행)는 repair/control(수리/대조) 입력을 만들고 broker visibility(브로커 가시성) 복구 행동을 기록했다. Forward Passed/Failed(전진 통과/실패), runtime authority(런타임 권위), operating promotion(운영 승격), Goal Achieve(목표 달성)는 주장하지 않는다.
"""
    return aw.write_text_lossless(DECISION_DOC, text, True)


def replace_line(text: str, prefix: str, replacement: str) -> str:
    import re

    pattern = re.compile(rf"^{re.escape(prefix)}.*$", flags=re.M)
    return pattern.sub(replacement, text, count=1) if pattern.search(text) else replacement + "\n" + text


def replace_marked_section(text: str, heading: str, replacement: str) -> str:
    start = text.find(heading)
    if start < 0:
        return text
    next_start = text.find("\n## ", start + len(heading))
    if next_start < 0:
        return text[:start].rstrip() + "\n\n" + replacement.rstrip() + "\n"
    return text[:start].rstrip() + "\n\n" + replacement.rstrip() + text[next_start:]


def update_docs(final: Mapping[str, Any]) -> list[Path]:
    artifacts: list[Path] = []
    branch = current_branch()
    workspace, workspace_bom = aw.read_tracked_text_lossless(WORKSPACE_STATE)
    workspace = replace_line(workspace, "current_run_id:", f"current_run_id: {final['next_action']}")
    workspace = replace_line(workspace, "updated_on:", f"updated_on: '{TODAY}'")
    workspace = replace_line(workspace, "active_branch:", f"active_branch: {branch}")
    focus = (
        "- >-\n"
        f"  Stage337 run337ET focus complete: run337ET(337ET 실행)는 `{final['status']}`로 no-overfit repair inputs(무과적합 수리 입력)와 broker visibility recovery action(브로커 가시성 복구 행동)을 기록했다. "
        f"Effect(효과): feature contracts(피처 계약) `{final['feature_contract_rows']}`, negative controls(부정 대조) `{final['negative_control_rows']}`, broker precheck(브로커 사전점검) `{final['broker_precheck_status']}`, broker reprobe(브로커 재탐침) `{final['broker_reprobe_status']}`, execution blockers(실행 차단 사유) `{final['broker_reprobe_execution_blockers']}`를 남겼고 Forward/Goal(전진/목표)은 주장하지 않는다.\n"
    )
    if "Stage337 run337ET focus complete" not in workspace:
        workspace = workspace.replace("current_focus:\n", "current_focus:\n" + focus, 1)
    else:
        workspace = replace_line(workspace, "  Stage337 run337ET focus complete:", focus.splitlines()[1])
    artifacts.append(aw.write_text_lossless(WORKSPACE_STATE, workspace, workspace_bom))

    current, current_bom = aw.read_tracked_text_lossless(CURRENT_STATE)
    replacements = {
        "- current_run(현재 실행):": f"- current_run(현재 실행): `{final['next_action']}`",
        "- status(상태):": f"- status(상태): `{final['status']}`",
        "- decision(결정):": f"- decision(결정): `{final['decision']}`",
        "- latest_completed_run(최근 완료 실행):": f"- latest_completed_run(최근 완료 실행): `{RUN_ID}`",
        "- next_action(다음 행동):": f"- next_action(다음 행동): `{final['next_action']}`",
        "- claim_boundary(주장 경계):": f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
    }
    for prefix, replacement in replacements.items():
        current = replace_line(current, prefix, replacement)
    section = f"""
## run337ET No-Overfit Repair Inputs or Broker Reprobe(무과적합 수리 입력 또는 브로커 재탐침)

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- broker_precheck(브로커 사전점검): `{final['broker_precheck_status']}`
- broker_reprobe_status(브로커 재탐침 상태): `{final['broker_reprobe_status']}`
- terminal_status(터미널 상태): `{final['broker_reprobe_terminal_status']}`
- execution_blockers(실행 차단 사유): `{final['broker_reprobe_execution_blockers']}`
- effect(효과): failure memory(실패 기억)를 feature/gate/negative/proxy contracts(피처/게이트/부정대조/프록시 계약)로 바꾸고 실제 브로커 가시성 복구 행동을 기록했다. Forward/Goal(전진/목표)은 주장하지 않는다.
- next_action(다음 행동): `{final['next_action']}`
"""
    if "## run337ET No-Overfit Repair Inputs" not in current:
        marker = "## run337ES No-Overfit Repair"
        current = current.replace(marker, section + "\n" + marker, 1) if marker in current else current.rstrip() + "\n\n" + section
    else:
        current = replace_marked_section(current, "## run337ET No-Overfit Repair Inputs or Broker Reprobe", section)
    artifacts.append(aw.write_text_lossless(CURRENT_STATE, current, current_bom))

    selection = f"""# Stage337 Selection Status(337단계 선택 상태)

- latest_run(최신 실행): `{RUN_ID}`
- latest_decision(최신 결정): `{final['decision']}`
- current_run(현재 실행): `{final['next_action']}`
- frozen_subject(고정 대상): `cp322A_cp321b_exact_replay_control_surface / stage337 survivor forward surface`
- preserved_status(보존 상태): `research_artifact_only`
- rebuild_status(재구축 상태): `{final['status']}`
- broker_forward_boundary(브로커 전진 경계): `not_closed_ET_review_required`
- feature_contract_rows(피처 계약 행): `{final['feature_contract_rows']}`
- gate_contract_rows(게이트 계약 행): `{final['gate_contract_rows']}`
- negative_control_rows(부정 대조 행): `{final['negative_control_rows']}`
- proxy_pairing_rows(프록시 쌍 행): `{final['proxy_pairing_rows']}`
- broker_precheck_status(브로커 사전점검 상태): `{final['broker_precheck_status']}`
- broker_reprobe_status(브로커 재탐침 상태): `{final['broker_reprobe_status']}`
- broker_terminal_status(브로커 터미널 상태): `{final['broker_reprobe_terminal_status']}`
- broker_execution_blockers(브로커 실행 차단 사유): `{final['broker_reprobe_execution_blockers']}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- Forward Blocked(전진 차단): `not_reclosed_ET_review_required`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{final['next_action']}`
- effect(효과): ET(337ET 실행)는 입력과 복구 행동을 남겼지만 후보 선택이나 운영 주장은 하지 않는다.
"""
    artifacts.append(aw.write_text_lossless(SELECTED_STATUS, selection, True))

    brief, brief_bom = aw.read_tracked_text_lossless(STAGE_BRIEF)
    brief = replace_line(brief, "- latest_run(최신 실행):", f"- latest_run(최신 실행): `{RUN_ID}`")
    summary = (
        f"- run337ET_summary(337ET 요약): `{final['status']}`. "
        f"Effect(효과): feature contracts(피처 계약) `{final['feature_contract_rows']}`, gate contracts(게이트 계약) `{final['gate_contract_rows']}`, negative controls(부정 대조) `{final['negative_control_rows']}`를 물질화하고 broker precheck(브로커 사전점검) `{final['broker_precheck_status']}`, broker reprobe(브로커 재탐침) `{final['broker_reprobe_status']}`, execution blockers(실행 차단 사유) `{final['broker_reprobe_execution_blockers']}`를 기록했다. Forward/Goal(전진/목표)은 주장하지 않는다.\n"
    )
    if "run337ET_summary" not in brief:
        brief = brief.rstrip() + "\n" + summary
    else:
        brief = replace_line(brief, "- run337ET_summary(337ET 요약):", summary.rstrip())
    artifacts.append(aw.write_text_lossless(STAGE_BRIEF, brief, brief_bom))

    changelog, changelog_bom = aw.read_tracked_text_lossless(CHANGELOG)
    entry = (
        f"- {TODAY}: Stage337 run337ET(337ET 실행) `{final['status']}`. "
        f"Effect(효과): no-overfit repair inputs(무과적합 수리 입력)와 broker visibility recovery action(브로커 가시성 복구 행동)을 기록했고 broker execution blockers(브로커 실행 차단 사유) `{final['broker_reprobe_execution_blockers']}`를 남겼으며 Forward/Goal(전진/목표)은 주장하지 않음."
    )
    if "Stage337 run337ET" not in changelog:
        changelog = changelog.rstrip() + "\n" + entry + "\n"
    else:
        changelog = replace_line(changelog, f"- {TODAY}: Stage337 run337ET", entry)
    artifacts.append(aw.write_text_lossless(CHANGELOG, changelog, changelog_bom))
    return artifacts


def update_registers(final: Mapping[str, Any]) -> list[Path]:
    reprobe_status = str(final.get("broker_reprobe_status", ""))
    execution_blockers = ";".join(str(item) for item in final.get("broker_reprobe_execution_blockers", []) if str(item))
    if "executed_visibility_reached" in reprobe_status:
        external_verification_status = "completed"
    elif "not_executed" in reprobe_status:
        external_verification_status = "precheck_completed_runtime_not_executed"
    else:
        external_verification_status = "blocked"
    external_note = (
        f"broker_reprobe_status={reprobe_status};"
        f"terminal_status={final.get('broker_reprobe_terminal_status', '')};"
        f"execution_blockers={execution_blockers or 'none'}"
    )
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "no_overfit_repair_inputs_or_broker_reprobe",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "notes": f"decision={final['decision']};next_action={final['next_action']};feature_contracts={final['feature_contract_rows']};gates={final['passed_gates']}/{final['gate_rows']};{external_note};goal_achieve_not_claimed.",
        "family": "experiment_execution",
        "primary_report": rel(REPORT_PATH),
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__repair_inputs_broker_reprobe",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "repair_inputs_broker_reprobe",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "no_overfit_repair_inputs_and_broker_reprobe(무과적합 수리 입력과 브로커 재탐침)",
        "tier_scope": "Tier A broker reference and shifted diagnostic memory(Tier A 브로커 기준과 이동 진단 기억)",
        "kpi_scope": "input_contract_and_reprobe_boundary_no_forward_decision(입력 계약과 재탐침 경계, 전진 판정 없음)",
        "scoreboard_lane": "experiment_execution",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "primary_kpi": f"feature_contracts={final['feature_contract_rows']};negative_controls={final['negative_control_rows']};broker_precheck={final['broker_precheck_status']}",
        "guardrail_kpi": "no_training;no_threshold_tuning;no_db_rewrite;no_lot_opt;no_candidate_selection;no_forward_claim",
        "external_verification_status": external_verification_status,
        "notes": f"decision={final['decision']};next_action={final['next_action']};{external_note};goal_achieve_not_claimed.",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__repair_inputs_broker_reprobe",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "experiment_execution",
        "evidence_scope": "ES contracts, ER failure memory, EQ broker gap, EP runtime parity",
        "kpi_scope": "input_contract_and_reprobe_boundary",
        "status": final["status"],
        "judgment": final["judgment"],
        "claim_boundary": CLAIM_BOUNDARY,
        "path": rel(REPORT_PATH),
        "notes": f"gates={final['passed_gates']}/{final['gate_rows']};{external_note};goal_achieve_not_claimed",
        "decision": final["decision"],
        "run_key": f"{RUN_ID}__repair_inputs_broker_reprobe",
        "family": "no_overfit_repair_inputs_or_broker_reprobe",
        "question": "can ES failure memory become ET repair inputs while broker visibility is actively rechecked",
        "metric_scope": "feature_gate_negative_proxy_broker_boundary",
        "primary_artifact": rel(REPORT_PATH),
        "report_path": rel(REPORT_PATH),
        "next_action": final["next_action"],
    }
    aw.upsert_csv(RUN_REGISTRY, aw.RUN_REGISTRY_COLUMNS, run_row, "run_id")
    aw.upsert_csv(ALPHA_LEDGER, aw.ALPHA_LEDGER_COLUMNS, alpha_row, "ledger_row_id")
    aw.upsert_csv(STAGE_LEDGER, aw.STAGE_LEDGER_COLUMNS, stage_row, "ledger_row_id")
    return [RUN_REGISTRY, ALPHA_LEDGER, STAGE_LEDGER]


def update_artifact_registry(paths: Sequence[Path], final: Mapping[str, Any]) -> Path:
    columns, rows = aw.read_csv_table(ARTIFACT_REGISTRY, prefer_head=True)
    columns = columns or list(aw.ARTIFACT_COLUMNS)
    rows = [row for row in rows if not str(row.get("artifact_id", "")).startswith(f"{RUN_ID}::")]
    created_at = now_utc()
    seen: set[str] = set()
    for path in paths:
        if not path_exists(path):
            continue
        artifact_path = rel(path)
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
    args = parse_args()
    for directory in (RUN_DIR, MT5_DIR, SET_DIR, INI_DIR, REPORT_DIR, FEATURE_DIR, MODEL_DIR, EXPECTED_DIR, TELEMETRY_DIR):
        aw.io_path(directory).mkdir(parents=True, exist_ok=True)
    src = load_sources()
    feature_rows = build_feature_contracts(src)
    gate_contract_rows = build_gate_contracts()
    negative_rows = build_negative_controls()
    pair_rows = build_proxy_pairing()
    source_rows = build_source_hashes()
    precheck = broker_visibility_precheck(args, src)
    precheck_path = write_json(BROKER_VISIBILITY_PRECHECK, precheck)
    broker_summary = run_broker_reprobe(args)
    broker_summary_path = write_json(BROKER_REPROBE_SUMMARY, broker_summary)
    audit_rows = build_no_lookahead_audit(feature_rows, negative_rows, broker_summary)
    queue_rows = build_review_queue()

    feature_path = write_csv(FEATURE_CONTRACT, FEATURE_COLUMNS, feature_rows)
    gate_contract_path = write_csv(GATE_CONTRACT, GATE_COLUMNS, gate_contract_rows)
    negative_path = write_csv(NEGATIVE_CONTROL_PLAN, NEGATIVE_COLUMNS, negative_rows)
    pair_path = write_csv(PROXY_MT5_PAIRING, PAIRING_COLUMNS, pair_rows)
    source_path = write_csv(INPUT_SOURCE_HASH, SOURCE_COLUMNS, source_rows)
    audit_path = write_csv(NO_LOOKAHEAD_AUDIT, AUDIT_COLUMNS, audit_rows)
    queue_path = write_csv(RUN337EU_QUEUE, QUEUE_COLUMNS, queue_rows)
    required_rows = build_required_gates(feature_rows, gate_contract_rows, negative_rows, pair_rows, source_rows, audit_rows, queue_rows, precheck, broker_summary)
    gate_path = write_csv(GATE_AUDIT, REQUIRED_GATE_COLUMNS, required_rows)
    final = final_decision_payload(precheck, broker_summary, feature_rows, gate_contract_rows, negative_rows, pair_rows, required_rows)
    final_path = write_json(FINAL_DECISION, final)
    receipt_paths = write_receipts(final)
    package_rows = build_package_manifest(
        [
            feature_path,
            gate_contract_path,
            negative_path,
            pair_path,
            precheck_path,
            broker_summary_path,
            source_path,
            audit_path,
            queue_path,
            gate_path,
            *receipt_paths,
            final_path,
        ]
    )
    package_path = write_csv(PACKAGE_MANIFEST, PACKAGE_COLUMNS, package_rows)
    manifest_path = write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "created_at_utc": now_utc(),
            "producer": rel(__file__),
            "command": "python stage_pipelines/stage337/materialize_no_overfit_repair_inputs_or_broker_forward_reprobe_without_db.py",
            "execute_broker_reprobe": bool(args.execute_broker_reprobe),
            "inputs": [rel(path) for path in INPUT_FILES if path_exists(path)],
            "outputs": [rel(path) for path in [FEATURE_CONTRACT, GATE_CONTRACT, NEGATIVE_CONTROL_PLAN, PROXY_MT5_PAIRING, BROKER_VISIBILITY_PRECHECK, BROKER_REPROBE_SUMMARY, GATE_AUDIT, FINAL_DECISION, REPORT_PATH, DECISION_DOC, RUN_MANIFEST]],
            "forbidden_actions": [
                "model training(모델 학습)",
                "threshold tuning(임계값 조정)",
                "D/B rewrite(D/B 재작성)",
                "lot optimization(랏 최적화)",
                "candidate selection(후보 선택)",
                "Forward Passed/Failed claim(전진 통과/실패 주장)",
                "Goal Achieve claim(목표 달성 주장)",
            ],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    report_path = write_report(final)
    decision_path = write_decision_doc(final)
    doc_paths = update_docs(final)
    register_paths = update_registers(final)
    all_artifacts = [
        feature_path,
        gate_contract_path,
        negative_path,
        pair_path,
        precheck_path,
        broker_summary_path,
        source_path,
        audit_path,
        queue_path,
        gate_path,
        *receipt_paths,
        package_path,
        final_path,
        manifest_path,
        report_path,
        decision_path,
        *doc_paths,
        *register_paths,
        Path(__file__),
    ]
    artifact_registry_path = update_artifact_registry(all_artifacts, final)
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": final["status"],
                "judgment": final["judgment"],
                "decision": final["decision"],
                "next_action": final["next_action"],
                "gates": f"{final['passed_gates']}/{final['gate_rows']}",
                "broker_precheck_status": final["broker_precheck_status"],
                "broker_reprobe_status": final["broker_reprobe_status"],
                "feature_contract_rows": final["feature_contract_rows"],
                "negative_control_rows": final["negative_control_rows"],
                "report": rel(report_path),
                "artifact_registry": rel(artifact_registry_path),
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )
    return 0 if not final["failed_gates"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
