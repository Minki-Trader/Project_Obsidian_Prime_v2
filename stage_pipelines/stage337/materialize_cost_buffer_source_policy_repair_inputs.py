from __future__ import annotations

import csv
import hashlib
import json
import math
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[2]
TODAY = "2026-05-27"
STAGE_ID = "337_onnx_research_packet__cost_buffer_direction_curve_rebuild"
RUN_NUMBER = "run337W"
RUN_ID = "run337W_materialize_cost_buffer_source_policy_repair_inputs_v1"
PARENT_RUN_ID = "run337V_cost_buffer_rebuild_and_source_policy_repair_design_v1"
NEXT_RUN_ID = "run337X_review_materialized_cost_buffer_source_policy_repair_inputs_v1"
STATUS = "completed_stage337W_cost_buffer_source_policy_repair_inputs_materialized_no_training_no_mt5"
JUDGMENT = "source_policy_cost_buffer_overfit_parity_inputs_materialized_no_onnx_or_forward_decision"
DECISION = "stage337W_open_run337X_review_materialized_repair_inputs_no_selection"
CLAIM_BOUNDARY = (
    "research_development_only_stage337W_materialization_no_model_training_no_threshold_retuning_"
    "no_lot_optimization_no_candidate_selection_no_forward_passed_no_forward_failed_no_live_readiness_"
    "no_deployment_no_operating_promotion_no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
RUN337V_DIR = STAGE_DIR / "02_runs" / "run337V"
RUN337U_DIR = STAGE_DIR / "02_runs" / "run337U"
REVIEWS_DIR = STAGE_DIR / "03_reviews"
SELECTED_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
REPORT_PATH = REVIEWS_DIR / "run337W_repair_inputs.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-27_stage337W_repair_inputs.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
STAGE_LEDGER = REVIEWS_DIR / "stage_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"

V_FAILURE_DIGEST = RUN337V_DIR / "run337V_failure_memory_digest.csv"
V_SOURCE_POLICY = RUN337V_DIR / "source_policy_repair_matrix.csv"
V_COST_BRANCHES = RUN337V_DIR / "cost_buffer_rebuild_hypothesis_matrix.csv"
V_OVERFIT_GATES = RUN337V_DIR / "overfit_parity_gate_contract.csv"
V_ECONOMIC_SOURCES = RUN337V_DIR / "economic_regime_source_policy_contract.csv"
V_QUEUE = RUN337V_DIR / "run337W_materialization_queue.csv"
U_DECISION = RUN337U_DIR / "final_tester_rollover_reprobe_decision.json"
U_GAP = RUN337U_DIR / "tester_rollover_feature_last_gap.csv"

SOURCE_AGE_AUDIT_CSV = RUN_DIR / "source_age_and_availability_audit.csv"
FEATURE_LABEL_BOUNDARY_CSV = RUN_DIR / "feature_label_boundary_audit.csv"
SOURCE_CLEAN_DECISION_CSV = RUN_DIR / "source_clean_repair_decision.csv"
BRANCH_SPEC_MANIFEST_CSV = RUN_DIR / "branch_spec_manifest.csv"
COST_LADDER_CONTRACT_CSV = RUN_DIR / "cost_ladder_contract.csv"
DIRECTION_CURVE_GATE_CSV = RUN_DIR / "direction_curve_gate_template.csv"
PROXY_EXPECTED_TEMPLATE_CSV = RUN_DIR / "proxy_expected_template.csv"
PROXY_MT5_SCHEMA_CSV = RUN_DIR / "timestamp_aligned_proxy_mt5_difference_schema.csv"
USABILITY_RULE_CSV = RUN_DIR / "usability_decision_rule.csv"
TESTER_BOUNDARY_PLAN_CSV = RUN_DIR / "tester_boundary_repair_plan.csv"
TESTER_FEATURE_GATE_CSV = RUN_DIR / "tester_feature_last_reach_gate.csv"
MODEL_VALIDATION_FIREWALL_CSV = RUN_DIR / "model_validation_firewall.csv"
NO_FORWARD_THRESHOLD_CSV = RUN_DIR / "no_forward_threshold_search_contract.csv"
WFO_SPLIT_PLAN_CSV = RUN_DIR / "wfo_split_plan.csv"
REQUIRED_GATE_AUDIT_CSV = RUN_DIR / "required_gate_coverage_audit.csv"
EXPERIMENT_RECEIPT_JSON = RUN_DIR / "experiment_design_receipt.json"
DATA_INTEGRITY_JSON = RUN_DIR / "data_integrity_receipt.json"
MODEL_VALIDATION_JSON = RUN_DIR / "model_validation_receipt.json"
RUNTIME_PARITY_JSON = RUN_DIR / "runtime_parity_receipt.json"
RESULT_JUDGMENT_JSON = RUN_DIR / "result_judgment_receipt.json"
ARTIFACT_LINEAGE_JSON = RUN_DIR / "artifact_lineage_receipt.json"
FINAL_DECISION_JSON = RUN_DIR / "final_decision.json"
RUN_MANIFEST_JSON = RUN_DIR / "run_manifest.json"

COST_POINTS = [0, 0.5, 1, 2, 5, 10]


ATTEMPT_SPECS: dict[str, dict[str, Any]] = {
    "m48_plain_rf": {
        "feature_set_id": "macro48_no_equity_breadth_or_top3",
        "sources": ["VIX", "USDX", "US10YR"],
        "decision": "source_policy_repair_required_before_training_or_forward_decision",
        "role": "highest_profit_clue_but_source_policy_blocked",
        "note_ko": "거시 원천 시점 기준 정책이 통과되기 전에는 수익 단서만 보존한다.",
    },
    "c56_plain_rf": {
        "feature_set_id": "core56_no_top3_weight_features",
        "sources": ["mega-cap equities", "VIX", "USDX", "US10YR"],
        "decision": "source_policy_repair_required_before_training_or_forward_decision",
        "role": "low_trade_count_high_pf_clue_but_source_policy_blocked",
        "note_ko": "주식 원천 가용성/낡음 여부를 분리하기 전에는 높은 PF도 운영 단서로 쓰지 않는다.",
    },
    "u42_plain_rf": {
        "feature_set_id": "us100_technical42_no_external",
        "sources": ["US100 broker M5"],
        "decision": "keep_as_source_clean_control_not_selection",
        "role": "source_clean_cost_fragility_control",
        "note_ko": "원천은 깨끗하지만 비용 버퍼가 약해 실패 기억 대조군으로만 둔다.",
    },
}

SOURCE_POLICY: dict[str, dict[str, str]] = {
    "VIX": {
        "feature_role": "volatility regime(변동성 국면)",
        "asof_rule": "published_timestamp <= US100_bar_close",
        "missing_rule": "mark_unavailable_and_skip_or_flag; no_future_fill",
        "stress_slice": "vix_regime",
    },
    "USDX": {
        "feature_role": "USD regime(달러 국면)",
        "asof_rule": "source_timestamp <= decision_timestamp",
        "missing_rule": "mark_age_bucket_and_skip_if_over_max_age",
        "stress_slice": "usd_regime",
    },
    "US10YR": {
        "feature_role": "rate regime(금리 국면)",
        "asof_rule": "latest_known_rate_point_only",
        "missing_rule": "session_aware_missing_flag_required",
        "stress_slice": "rate_regime",
    },
    "mega-cap equities": {
        "feature_role": "equity breadth(대형주 폭)",
        "asof_rule": "cash_session_timestamp_explicit_and_lte_us100_bar_close",
        "missing_rule": "no_silent_bridge_over_closed_session",
        "stress_slice": "equity_source_age",
    },
    "US100 broker M5": {
        "feature_role": "technical control(기술 대조군)",
        "asof_rule": "broker_bar_close_open_convention_must_match_MT5_runtime",
        "missing_rule": "tester_gap_recorded_and_not_silently_filled",
        "stress_slice": "technical_control",
    },
}

BRANCH_SPECS: dict[str, dict[str, str]] = {
    "cost_margin_objective_pretraining": {
        "branch_type": "defensive_rebuild",
        "hypothesis": "entry score(진입 점수)가 비용 여유(cost margin, 비용 여유)를 먼저 확보해야 전진 구간에서 의미가 있다.",
        "forbidden_shortcut": "forward data(전진 데이터)로 threshold(임계값)를 다시 맞추거나 손실 시간대를 사후 삭제하지 않는다.",
        "controls": "cost ladder(비용 사다리) +0,+0.5,+1,+2,+5,+10; 모든 지점의 PF/net/DD를 함께 보고한다.",
        "success": "base PF >= 1.20, +1 PF >= 1.10, +2 net > 0, +5가 치명적 붕괴가 아니어야 한다.",
        "failure": "u42처럼 +1 PF가 1.10 아래로 밀리거나 +5 net이 음수로 붕괴하면 실패 기억으로 남긴다.",
    },
    "direction_symmetry_rebuild": {
        "branch_type": "defensive_plus_offensive",
        "hypothesis": "long/short(롱/숏) 중 한쪽 포켓을 사후 필터가 아니라 구조로 설명해야 한다.",
        "forbidden_shortcut": "forward 손익을 본 뒤 shorts(숏)를 끄는 방식은 금지한다.",
        "controls": "long attribution(롱 귀속), short attribution(숏 귀속), D/B/D+B source(원천) 분해를 요구한다.",
        "success": "양방향이 치명적이지 않거나, 사전 선언된 단방향 모델이 밀도/비용 게이트를 통과한다.",
        "failure": "sell bucket(매도 묶음)이 음수인데 원천/라벨 설명 없이 남아 있으면 실패다.",
    },
    "curve_pocket_robustness_rebuild": {
        "branch_type": "curve_quality",
        "hypothesis": "headline net(총 순익)보다 worst pocket(최악 포켓), underwater stretch(수중 구간), recovery(회복)를 먼저 본다.",
        "forbidden_shortcut": "월/요일/시간 포켓을 forward 손실을 본 뒤 제거하지 않는다.",
        "controls": "month, weekday, hour, session, ADX, volatility, chronology, rolling pocket을 모두 기록한다.",
        "success": "단일 포켓이 곡선을 깨지 않고 recovery factor(회복 계수)가 밀도 붕괴 없이 개선된다.",
        "failure": "월요일/화요일/ADX 20-25 같은 포켓이 계속 음수로 남으면 실패다.",
    },
    "aggressive_density_preserving_rebuild": {
        "branch_type": "offensive_probe",
        "hypothesis": "trade supply(거래 공급)를 살리면서 비용 버퍼를 넓히는 구조가 있는지 본다.",
        "forbidden_shortcut": "거래 수를 굶겨 PF(손익비)만 좋게 보이게 만들지 않는다.",
        "controls": "trades/day(일 거래 수), signal rate(신호율), fill rate(체결률), skip reason(스킵 사유)을 기록한다.",
        "success": "거래 수가 쓸만하고 비용/곡선 게이트가 함께 무너지지 않는다.",
        "failure": "거래가 너무 적거나 proxy-only(프록시 전용) 개선이면 실패다.",
    },
}

OUTPUT_FILES = [
    SOURCE_AGE_AUDIT_CSV,
    FEATURE_LABEL_BOUNDARY_CSV,
    SOURCE_CLEAN_DECISION_CSV,
    BRANCH_SPEC_MANIFEST_CSV,
    COST_LADDER_CONTRACT_CSV,
    DIRECTION_CURVE_GATE_CSV,
    PROXY_EXPECTED_TEMPLATE_CSV,
    PROXY_MT5_SCHEMA_CSV,
    USABILITY_RULE_CSV,
    TESTER_BOUNDARY_PLAN_CSV,
    TESTER_FEATURE_GATE_CSV,
    MODEL_VALIDATION_FIREWALL_CSV,
    NO_FORWARD_THRESHOLD_CSV,
    WFO_SPLIT_PLAN_CSV,
    REQUIRED_GATE_AUDIT_CSV,
]


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    item = Path(path)
    try:
        return item.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return item.as_posix()


def path_exists(path: Path) -> bool:
    return path.exists()


def json_ready(value: Any) -> Any:
    if isinstance(value, Path):
        return rel(value)
    if isinstance(value, Mapping):
        return {str(key): json_ready(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_ready(item) for item in value]
    if isinstance(value, float):
        return value if math.isfinite(value) else None
    return value


def csv_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, float):
        return "" if math.isfinite(value) else f"{value:.12g}"
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(json_ready(value), ensure_ascii=False, sort_keys=True)
    return str(value)


def safe_float(value: Any, default: float = math.nan) -> float:
    try:
        number = float(str(value).strip())
    except (TypeError, ValueError):
        return default
    return number if math.isfinite(number) else default


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path_exists(path):
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def read_json(path: Path) -> dict[str, Any]:
    if not path_exists(path):
        return {}
    return json.loads(path.read_text(encoding="utf-8-sig"))


def require_inputs(paths: Sequence[Path]) -> None:
    missing = [rel(path) for path in paths if not path_exists(path)]
    if missing:
        raise FileNotFoundError("missing required run337W inputs: " + "; ".join(missing))


def write_csv(path: Path, columns: Sequence[str], rows: Iterable[Mapping[str, Any]]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: csv_value(row.get(column, "")) for column in columns})
    return path


def write_json(path: Path, payload: Any) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return path


def write_md(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + "\n", encoding="utf-8-sig", newline="\n")
    return path


def read_text_with_bom(path: Path) -> tuple[str, bool]:
    raw = path.read_bytes()
    return raw.decode("utf-8-sig"), raw.startswith(b"\xef\xbb\xbf")


def write_text_preserve_bom(path: Path, text: str, had_bom: bool) -> Path:
    encoding = "utf-8-sig" if had_bom or path.suffix.lower() in {".md", ".txt"} else "utf-8"
    path.write_text(text, encoding=encoding, newline="\n")
    return path


def normalized_sha256(path: Path) -> str:
    data = path.read_bytes().replace(b"\r\n", b"\n")
    return hashlib.sha256(data).hexdigest()


def upsert_csv(path: Path, key_columns: Sequence[str], row: Mapping[str, Any]) -> Path:
    rows: list[dict[str, str]] = []
    columns: list[str] = []
    if path_exists(path):
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            columns = list(reader.fieldnames or [])
            rows = [dict(item) for item in reader]
    for column in row:
        if column not in columns:
            columns.append(column)
    key = tuple(str(row.get(column, "")) for column in key_columns)
    rows = [item for item in rows if tuple(str(item.get(column, "")) for column in key_columns) != key]
    rows.append({column: csv_value(row.get(column, "")) for column in columns})
    return write_csv(path, columns, rows)


def load_inputs() -> dict[str, Any]:
    required = [
        V_QUEUE,
        V_SOURCE_POLICY,
        V_COST_BRANCHES,
        V_OVERFIT_GATES,
        V_ECONOMIC_SOURCES,
        V_FAILURE_DIGEST,
        U_DECISION,
    ]
    require_inputs(required)
    return {
        "queue": read_csv(V_QUEUE),
        "source_policy": read_csv(V_SOURCE_POLICY),
        "cost_branches": read_csv(V_COST_BRANCHES),
        "overfit_gates": read_csv(V_OVERFIT_GATES),
        "economic_sources": read_csv(V_ECONOMIC_SOURCES),
        "failure_digest": read_csv(V_FAILURE_DIGEST),
        "u_decision": read_json(U_DECISION),
        "u_gap": read_csv(U_GAP),
    }


def digest_by_attempt(inputs: Mapping[str, Any]) -> dict[str, dict[str, str]]:
    return {row.get("attempt_name", ""): row for row in inputs["failure_digest"]}


def materialize_source_contracts(inputs: Mapping[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    source_rows: list[dict[str, Any]] = []
    boundary_rows: list[dict[str, Any]] = []
    decision_rows: list[dict[str, Any]] = []
    failure = digest_by_attempt(inputs)
    for attempt, spec in ATTEMPT_SPECS.items():
        failure_row = failure.get(attempt, {})
        feature_set_id = failure_row.get("feature_set_id") or spec["feature_set_id"]
        for source_family in spec["sources"]:
            policy = SOURCE_POLICY[source_family]
            source_rows.append(
                {
                    "attempt_name": attempt,
                    "feature_set_id": feature_set_id,
                    "source_family": source_family,
                    "feature_role": policy["feature_role"],
                    "asof_rule": policy["asof_rule"],
                    "availability_status": "pending_external_or_broker_timestamp_measurement",
                    "max_age_policy": "session_aware_explicit_age_bucket_required",
                    "missing_rule": policy["missing_rule"],
                    "lookahead_guard": "source_timestamp_must_be_lte_US100_decision_bar_close",
                    "stress_slice": policy["stress_slice"],
                    "invalid_if": "future_fill_or_silent_stale_fill_or_source_close_after_decision_bar",
                    "next_evidence": "run337X_source_age_review",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
        boundary_rows.append(
            {
                "attempt_name": attempt,
                "feature_set_id": feature_set_id,
                "label_boundary": "label_return_window_starts_after_decision_bar",
                "feature_boundary": "all_features_known_at_or_before_decision_bar_close",
                "fixed_variables": "selected_candidate_none;threshold_search_forbidden;lot_optimization_forbidden;runtime_claim_forbidden",
                "changed_variables": "source_availability_flags_and_cost_buffer_contracts_only",
                "leakage_risk": "lookahead_bias(미래참조 편향), stale_source_fill(낡은 원천 채움), forward_threshold_search(전진 임계값 탐색)",
                "required_negative_control": "shift_source_timestamp_forward_one_bar_and_expect_invalid_flag",
                "boundary_status": "materialized_contract_ready_for_run337X_review",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        decision_rows.append(
            {
                "attempt_name": attempt,
                "feature_set_id": feature_set_id,
                "source_decision": spec["decision"],
                "repair_or_control_role": spec["role"],
                "selection_use": "not_allowed",
                "forward_pass_fail_use": "not_allowed_until_source_cost_proxy_tester_gates_pass",
                "note_ko": spec["note_ko"],
                "next_condition": NEXT_RUN_ID,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return source_rows, boundary_rows, decision_rows


def materialize_branch_contracts(inputs: Mapping[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    failure = digest_by_attempt(inputs)
    branch_ids = [row.get("branch_id", "") for row in inputs["cost_branches"] if row.get("branch_id", "")]
    if not branch_ids:
        branch_ids = list(BRANCH_SPECS)

    branch_rows: list[dict[str, Any]] = []
    for branch_id in branch_ids:
        spec = BRANCH_SPECS.get(branch_id, {})
        branch_rows.append(
            {
                "branch_id": branch_id,
                "branch_type": spec.get("branch_type", "review_required"),
                "hypothesis": spec.get("hypothesis", "run337X review required"),
                "fixed_variables": "no_forward_threshold_search;no_lot_optimization;no_runtime_authority;no_selection",
                "changed_variables": "predeclared_source_policy_or_cost_buffer_design_only",
                "forbidden_shortcut": spec.get("forbidden_shortcut", "post_hoc_forward_filtering_forbidden"),
                "predeclared_controls": spec.get("controls", "required_controls_missing"),
                "success_criteria": spec.get("success", "must_be_defined_before_training"),
                "failure_criteria": spec.get("failure", "must_be_defined_before_training"),
                "materialization_status": "template_materialized_no_training",
                "next_review": NEXT_RUN_ID,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    ladder_rows: list[dict[str, Any]] = []
    for attempt, spec in ATTEMPT_SPECS.items():
        failure_row = failure.get(attempt, {})
        for point in COST_POINTS:
            known_net = math.nan
            known_pf = math.nan
            if point == 0:
                known_net = safe_float(failure_row.get("base_net_profit"))
                known_pf = safe_float(failure_row.get("base_profit_factor"))
            elif point == 1:
                known_net = safe_float(failure_row.get("cost_plus_1_net_profit"))
                known_pf = safe_float(failure_row.get("cost_plus_1_profit_factor"))
            elif point == 5:
                known_net = safe_float(failure_row.get("cost_plus_5_net_profit"))
                known_pf = safe_float(failure_row.get("cost_plus_5_profit_factor"))
            ladder_rows.append(
                {
                    "attempt_name": attempt,
                    "feature_set_id": failure_row.get("feature_set_id") or spec["feature_set_id"],
                    "extra_round_trip_points": point,
                    "known_reference_net": known_net,
                    "known_reference_pf": known_pf,
                    "required_output": "net_profit;gross_profit;gross_loss;profit_factor;expectancy;max_drawdown;recovery;underwater_stretch;trades_per_day",
                    "pass_gate": "pf_ge_1_10_at_plus_1;net_positive_at_plus_2;plus_5_not_catastrophic;trade_count_useful",
                    "failure_memory": failure_row.get("repair_priority", spec["role"]),
                    "use_boundary": "reference_context_only_not_selection",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )

    direction_rows = [
        ("D_source", "D source(방향 원천) 단독 순익/PF/DD/거래 수/기대값"),
        ("B_source", "B source(기본 원천) 단독 순익/PF/DD/거래 수/기대값"),
        ("D_plus_B_source", "D+B source(D+B 원천) 결합 귀속과 충돌 구간"),
        ("long_short", "long/short(롱/숏) 순익/PF/DD/거래 수/최악 포켓"),
        ("session_hour", "session/hour(세션/시간)별 순익/PF/DD/거래 수"),
        ("month_weekday", "month/weekday(월/요일)별 곡선 포켓"),
        ("volatility_adx", "volatility/ADX(변동성/ADX) 국면별 비용 민감도"),
        ("macro_regime", "VIX/USD/rate(변동성 지수/달러/금리) 국면별 귀속"),
        ("chron_rolling", "chronological/rolling(시간순/롤링) 최악 구간과 수중 구간"),
    ]
    direction_gate_rows = [
        {
            "axis": axis,
            "required_metrics": metrics,
            "minimum_scope": "all_attempts_and_future_branch_candidates",
            "invalid_if": "headline_net_positive_but_axis_omitted",
            "usable_for_forward_pass_fail": False,
            "required_before_onnx_ready": True,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for axis, metrics in direction_rows
    ]
    return branch_rows, ladder_rows, direction_gate_rows


def materialize_proxy_contracts(inputs: Mapping[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    attempts = list(ATTEMPT_SPECS)
    template_rows = [
        {
            "attempt_name": attempt,
            "expected_feature_ready_count": "computed_by_python_proxy",
            "expected_model_ok_count": "computed_by_python_proxy",
            "expected_long_count": "computed_by_python_proxy",
            "expected_short_count": "computed_by_python_proxy",
            "expected_flat_count": "computed_by_python_proxy",
            "expected_probability_fields": "p_long;p_short;p_flat_or_score_if_available",
            "mt5_runtime_fields_required": "feature_ready_count;model_ok_count;long_count;short_count;flat_count;signal_count",
            "timestamp_alignment_rule": "proxy rows must be cut to MT5 tester_last_observed_bar_time before parity judgment",
            "usable_for_kpi_authority": False,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for attempt in attempts
    ]
    schema_rows = [
        ("attempt_name", "string", "attempt identity", True),
        ("symbol", "string", "US100 only unless explicitly declared", True),
        ("timestamp_utc", "datetime", "bar close timestamp in UTC", True),
        ("dimension", "enum", "feature_ready/model_ok/long/short/flat/signal/probability", True),
        ("proxy_expected_value", "number", "Python expected value from frozen or candidate package", True),
        ("mt5_runtime_value", "number", "MT5 telemetry observed value", True),
        ("difference_proxy_minus_mt5", "number", "zero required for matched status", True),
        ("difference_status", "enum", "matched/explainable_runtime_bar_reach_difference/mismatch_requires_review/missing_value", True),
        ("usable_for_runtime_signal_parity", "bool", "true only for matched or explicitly explainable row reach", True),
        ("usable_for_forward_pass_fail", "bool", "false until tester reaches feature_last and KPI gates pass", True),
        ("explanation", "string", "human-readable reason in Korean and English pair when needed", False),
    ]
    schema_contract_rows = [
        {
            "column_name": column,
            "data_type": dtype,
            "validation_rule": rule,
            "required": required,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for column, dtype, rule, required in schema_rows
    ]
    usability_rows = [
        {
            "usability_label": "usable_for_runtime_signal_parity",
            "condition": "all timestamp-aligned proxy-vs-MT5 dimensions are matched or explicitly explainable",
            "allowed_claim": "signal parity diagnostic(신호 동등성 진단)",
            "forbidden_claim": "KPI authority(KPI 권위), Forward Passed/Failed(전진 통과/실패)",
            "next_action": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "usability_label": "usable_for_forward_pass_fail",
            "condition": "tester reaches feature_last, cost/source/direction/curve gates are complete, and no threshold search occurs",
            "allowed_claim": "forward decision review(전진 판정 검토)",
            "forbidden_claim": "Goal Achieve(목표 달성)",
            "next_action": "future_forward_decision_only_after_all_gates",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "usability_label": "proxy_only_result",
            "condition": "proxy exists but MT5 runtime probe is missing or row-level mismatch remains",
            "allowed_claim": "research clue(연구 단서)",
            "forbidden_claim": "runtime authority(런타임 권위)",
            "next_action": "run_MT5_probe_or_record_blocker",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "usability_label": "tester_gap_remains",
            "condition": "tester_last_observed_bar_time < feature_latest_timestamp",
            "allowed_claim": "blocked_or_repair_required(차단 또는 수리 필요)",
            "forbidden_claim": "Forward Passed/Failed(전진 통과/실패)",
            "next_action": "repair_history_or_wait_reprobe_policy",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    return template_rows, schema_contract_rows, usability_rows


def materialize_tester_boundary(inputs: Mapping[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    decision = inputs["u_decision"]
    api_latest = decision.get("api_latest_us100_close_utc", "")
    feature_latest = decision.get("feature_latest_timestamp", "")
    gap_minutes = decision.get("tester_to_feature_last_gap_minutes", "")
    reached = decision.get("tester_reached_feature_last", 0)
    status = "passed" if str(reached) == "1" else "blocked_tester_gap_remains"

    plan_rows = [
        {
            "plan_step": "verify_broker_history_latest",
            "condition": "US100 M5 broker history must contain bars through feature_latest_timestamp",
            "evidence": "terminal_history_snapshot_or_export",
            "action": "refresh_history_and_record_latest_bar",
            "effect": "테스터가 실제 최신 구간을 볼 수 있는지 분리한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "plan_step": "verify_tester_ToDate_semantics",
            "condition": "Strategy Tester(전략 테스터) ToDate must include the intended current-day bars",
            "evidence": "tester_log_and_telemetry_last_bar",
            "action": "reprobe_with_rollover_ToDate_and_compare_last_observed_bar",
            "effect": "날짜 경계 때문에 최신 봉이 빠지는지 확인한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "plan_step": "verify_feature_handoff_latest",
            "condition": "feature handoff(피처 인계) feature_last must be <= available broker history latest",
            "evidence": "feature_manifest_and_history_snapshot",
            "action": "record feature_last, source_last, and broker_last in one row",
            "effect": "피처가 데이터보다 앞서 있거나 테스터가 뒤처진 경우를 분리한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "plan_step": "wait_or_reprobe_policy",
            "condition": "broker terminal has not rolled current-day bars into tester yet",
            "evidence": "repeat snapshot after broker/session rollover",
            "action": "wait then rerun narrow MT5 probe",
            "effect": "데이터가 아직 안 들어온 상황을 후보 실패로 오판하지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "plan_step": "claim_downgrade_rule",
            "condition": "tester gap remains after repair attempts",
            "evidence": "tester_feature_last_reach_gate.csv",
            "action": "mark forward decision blocked, not passed or failed",
            "effect": "보지 못한 최신 구간으로 전진 판정을 내리지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    gate_rows = [
        {
            "gate_id": "tester_feature_last_reach",
            "api_latest_us100_close_utc": api_latest,
            "feature_latest_timestamp": feature_latest,
            "tester_last_observed_bar_time": "from_runtime_telemetry_required",
            "tester_to_feature_last_gap_minutes": gap_minutes,
            "required_condition": "tester_last_observed_bar_time >= feature_latest_timestamp",
            "current_status": status,
            "blocks_claim": "Forward Passed;Forward Failed;runtime_authority;Goal Achieve",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    return plan_rows, gate_rows


def materialize_model_validation(inputs: Mapping[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    firewall_rows = [
        ("source_asof_boundary", "training_or_forward_review", "source_timestamp <= decision_bar_close for all external sources", "lookahead_bias_or_silent_future_fill", "macro/equity source leak"),
        ("feature_label_boundary", "training", "features known before label window begins", "feature_label_overlap_missing", "label leakage"),
        ("no_forward_threshold_search", "forward_review", "threshold, D/B surface, lot, ATR SL/TP fixed before forward", "forward_data_used_for_tuning", "another overfit path"),
        ("proxy_mt5_row_level_difference", "runtime_claim", "timestamp-aligned proxy-vs-MT5 counts compared", "row_level_difference_missing", "proxy-only authority"),
        ("tester_feature_last_reach", "forward_decision", "tester telemetry reaches feature_last", "tester_gap_remaining", "partial current-day inference"),
        ("cost_curve_direction_joint_gate", "onnx_ready_review", "cost stress, curve pocket, long/short, D/B and regimes all reported", "headline_only_kpi", "pretty headline masking broken pockets"),
        ("wfo_split_lock", "training", "walk-forward split plan locked before candidate search", "split_changed_after_result", "split overfit"),
        ("failure_memory_binding", "review", "u42/m48/c56 failure memory remains attached to new branches", "prior_failure_ignored", "regression repetition"),
    ]
    firewall = [
        {
            "firewall_id": firewall_id,
            "required_before": required_before,
            "condition": condition,
            "blocks_if_missing": blocks,
            "overfit_path_blocked": overfit_path,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for firewall_id, required_before, condition, blocks, overfit_path in firewall_rows
    ]
    threshold_rows = [
        {
            "contract_id": "fixed_score_threshold",
            "rule": "score threshold(점수 임계값)은 forward data(전진 데이터)를 본 뒤 조정하지 않는다.",
            "forbidden": "threshold search, quantile retune, hour/session deletion after forward PnL",
            "required_evidence": "threshold_identity_audit.csv",
            "violation_judgment": "invalid_overfit_research",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "contract_id": "fixed_db_surface",
            "rule": "D/B decision surface(D/B 판단 표면)는 forward 결과를 본 뒤 바꾸지 않는다.",
            "forbidden": "post_hoc D-only/B-only switch",
            "required_evidence": "db_surface_identity_audit.csv",
            "violation_judgment": "invalid_surface_tuning",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "contract_id": "fixed_risk_and_lot",
            "rule": "lot logic(랏 로직), risk logic(위험 로직), ATR SL/TP(ATR 손절/익절)는 실험 경계 밖이다.",
            "forbidden": "lot optimization or ATR rescue after weak forward result",
            "required_evidence": "risk_lot_identity_audit.csv",
            "violation_judgment": "invalid_risk_reoptimization",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "contract_id": "no_forward_data_training",
            "rule": "2026-04-14 이후 forward data(전진 데이터)는 학습/튜닝에 쓰지 않는다.",
            "forbidden": "forward rows in training, validation, calibration, threshold fitting",
            "required_evidence": "split_membership_audit.csv",
            "violation_judgment": "invalid_forward_leakage",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    split_rows = [
        {
            "split_id": "train_history_pre_forward",
            "date_scope": "historical training window before frozen forward boundary",
            "allowed_use": "future branch training only after source/firewall review",
            "forbidden_use": "include 2026-04-14+ rows",
            "required_evidence": "split_membership_audit.csv",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "split_id": "validation_pre_forward",
            "date_scope": "pre-forward validation window",
            "allowed_use": "model comparison and failure memory",
            "forbidden_use": "retune after seeing latest forward",
            "required_evidence": "walk_forward_manifest.csv",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "split_id": "forward_holdout_2026_04_14_plus",
            "date_scope": "2026-04-14+ latest available US100 M5 broker data",
            "allowed_use": "frozen forward judgment only",
            "forbidden_use": "training, threshold fitting, lot optimization, weak-pocket deletion",
            "required_evidence": "forward_data_inventory.csv",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "split_id": "rolling_wfo_slices",
            "date_scope": "predeclared rolling windows only",
            "allowed_use": "robustness profile and instability attribution",
            "forbidden_use": "choose best window after result",
            "required_evidence": "wfo_slice_manifest.csv",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    return firewall, threshold_rows, split_rows


def materialize_gate_audit(rows_by_file: Mapping[Path, Sequence[Mapping[str, Any]]]) -> list[dict[str, Any]]:
    gate_map = [
        ("source_age_and_availability", SOURCE_AGE_AUDIT_CSV, "원천 시점과 가용성 누락을 먼저 드러낸다."),
        ("feature_label_boundary", FEATURE_LABEL_BOUNDARY_CSV, "피처-라벨 겹침과 미래참조를 막는다."),
        ("source_clean_repair_decision", SOURCE_CLEAN_DECISION_CSV, "m48/c56 수리와 u42 대조군 역할을 분리한다."),
        ("cost_ladder_contract", COST_LADDER_CONTRACT_CSV, "비용 증가에 따른 붕괴를 숨기지 않는다."),
        ("direction_curve_gate", DIRECTION_CURVE_GATE_CSV, "방향/곡선/국면 포켓을 headline KPI 아래에 숨기지 않는다."),
        ("proxy_expected_template", PROXY_EXPECTED_TEMPLATE_CSV, "프록시 예상값과 MT5 런타임 값을 비교할 입력 모양을 고정한다."),
        ("proxy_mt5_difference_schema", PROXY_MT5_SCHEMA_CSV, "row-level parity(행 단위 동등성) 판정을 표준화한다."),
        ("usability_decision_rule", USABILITY_RULE_CSV, "proxy-only(프록시 전용) 결과의 주장 범위를 낮춘다."),
        ("tester_boundary_repair_plan", TESTER_BOUNDARY_PLAN_CSV, "테스터가 최신 feature_last에 도달하지 못한 상황을 수리 경로로 남긴다."),
        ("tester_feature_last_reach_gate", TESTER_FEATURE_GATE_CSV, "보지 못한 forward 구간으로 통과/실패 판정을 못 하게 막는다."),
        ("model_validation_firewall", MODEL_VALIDATION_FIREWALL_CSV, "새 학습 전 과적합 방화벽을 고정한다."),
        ("no_forward_threshold_search", NO_FORWARD_THRESHOLD_CSV, "forward data(전진 데이터) 재튜닝을 금지한다."),
        ("wfo_split_plan", WFO_SPLIT_PLAN_CSV, "walk-forward split(워크포워드 분할)을 결과 전에 고정한다."),
    ]
    return [
        {
            "gate_name": gate,
            "status": "present" if len(rows_by_file.get(path, [])) > 0 else "missing",
            "evidence_path": rel(path),
            "row_count": len(rows_by_file.get(path, [])),
            "effect": effect,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for gate, path, effect in gate_map
    ]


def build_receipts(metrics: Mapping[str, Any], generated_at: str) -> list[Path]:
    receipt_payloads = [
        (
            EXPERIMENT_RECEIPT_JSON,
            {
                "receipt_type": "experiment_design(실험 설계)",
                "run_id": RUN_ID,
                "generated_at_utc": generated_at,
                "question": "Can the cost/source/parity/tester/model-validation repair design be made into concrete no-overfit inputs?",
                "hypothesis_boundary": "input materialization only; no model training, no MT5 execution, no forward decision",
                "predeclared_controls": ["no_forward_threshold_search", "cost_ladder", "direction_curve_gate", "proxy_mt5_difference_schema"],
                "stop_conditions": ["required input missing", "gate row missing", "training attempted in run337W"],
                "metrics": metrics,
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            DATA_INTEGRITY_JSON,
            {
                "receipt_type": "data_integrity(데이터 무결성)",
                "run_id": RUN_ID,
                "source_age_audit": rel(SOURCE_AGE_AUDIT_CSV),
                "feature_label_boundary_audit": rel(FEATURE_LABEL_BOUNDARY_CSV),
                "tester_feature_last_gate": rel(TESTER_FEATURE_GATE_CSV),
                "known_blocker": "run337U tester gap remains until repaired or re-probed",
                "effect": "미래참조 편향과 원천 낡음 문제를 학습 전에 막는다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            MODEL_VALIDATION_JSON,
            {
                "receipt_type": "model_validation(모델 검증)",
                "run_id": RUN_ID,
                "model_training": "not_run",
                "threshold_retuning": "forbidden",
                "firewall": rel(MODEL_VALIDATION_FIREWALL_CSV),
                "wfo_split_plan": rel(WFO_SPLIT_PLAN_CSV),
                "effect": "과적합을 위한 또 다른 과적합 경로를 차단한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            RUNTIME_PARITY_JSON,
            {
                "receipt_type": "runtime_parity(런타임 동등성)",
                "run_id": RUN_ID,
                "mt5_execution": "not_run",
                "proxy_template": rel(PROXY_EXPECTED_TEMPLATE_CSV),
                "difference_schema": rel(PROXY_MT5_SCHEMA_CSV),
                "usability_rule": rel(USABILITY_RULE_CSV),
                "effect": "proxy expected(프록시 예상값)와 MT5 runtime probe(MT5 런타임 탐침)의 차이를 같은 표준으로 보게 한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            RESULT_JUDGMENT_JSON,
            {
                "receipt_type": "result_judgment(결과 판정)",
                "run_id": RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "decision": DECISION,
                "forward_passed": "not_claimed",
                "forward_failed": "not_claimed",
                "goal_achieve": "not_claimed",
                "effect": "보고서 작성과 물질화를 Goal Achieve(목표 달성)로 오해하지 않는다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            ARTIFACT_LINEAGE_JSON,
            {
                "receipt_type": "artifact_lineage(산출물 계보)",
                "run_id": RUN_ID,
                "parent_run_id": PARENT_RUN_ID,
                "source_inputs": [rel(V_QUEUE), rel(V_SOURCE_POLICY), rel(V_COST_BRANCHES), rel(V_OVERFIT_GATES), rel(V_ECONOMIC_SOURCES), rel(V_FAILURE_DIGEST), rel(U_DECISION)],
                "producer": rel(Path(__file__)),
                "consumer": NEXT_RUN_ID,
                "outputs": [rel(path) for path in OUTPUT_FILES],
                "effect": "다음 검토가 어떤 입력에서 어떤 산출물이 나왔는지 추적한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
    ]
    return [write_json(path, payload) for path, payload in receipt_payloads]


def write_report(metrics: Mapping[str, Any]) -> Path:
    text = f"""
# Stage337W Materialized Repair Inputs(337W 수리 입력 물질화)

- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- parent_run(부모 실행): `{PARENT_RUN_ID}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- selected_candidate(선택 후보): `none`
- model training(모델 학습): `not_run`
- MT5 execution(MT5 실행): `not_run`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## What Was Materialized(무엇을 물질화했나)

- source age rows(원천 나이 행): `{metrics['source_age_rows']}`
- feature boundary rows(피처 경계 행): `{metrics['feature_boundary_rows']}`
- source repair decision rows(원천 수리 결정 행): `{metrics['source_decision_rows']}`
- branch specs(분기 명세): `{metrics['branch_spec_rows']}`
- cost ladder rows(비용 사다리 행): `{metrics['cost_ladder_rows']}`
- direction/curve gate rows(방향/곡선 게이트 행): `{metrics['direction_gate_rows']}`
- proxy expected rows(프록시 예상값 행): `{metrics['proxy_template_rows']}`
- proxy-MT5 schema rows(프록시-MT5 스키마 행): `{metrics['proxy_schema_rows']}`
- usability rules(활용성 규칙): `{metrics['usability_rule_rows']}`
- tester boundary rows(테스터 경계 행): `{metrics['tester_boundary_rows']}`
- model firewall rows(모델 방화벽 행): `{metrics['model_firewall_rows']}`
- gate audit rows(게이트 감사 행): `{metrics['gate_rows']}`

## Read(판독)

run337W(337W 실행)는 run337V(337V 실행)의 설계를 실제 CSV/JSON 입력으로 바꿨다. 효과(effect, 효과)는 다음 run337X(337X 실행)가 source age audit(원천 나이 감사), feature-label boundary(피처-라벨 경계), proxy-MT5 difference(프록시-MT5 차이), tester feature_last reach(테스터 피처 끝 도달), cost/curve/direction gate(비용/곡선/방향 게이트)를 빠뜨렸는지 바로 검토할 수 있게 하는 것이다.

이번 실행은 수익 개선이나 후보 선택이 아니다. model training(모델 학습), threshold retuning(임계값 재조정), lot optimization(랏 최적화), MT5 runtime probe(MT5 런타임 탐침), Forward Passed/Failed(전진 통과/실패), operating promotion(운영 승격), Goal Achieve(목표 달성)는 모두 주장하지 않는다.
"""
    return write_md(REPORT_PATH, text)


def write_decision_doc(metrics: Mapping[str, Any]) -> Path:
    text = f"""
# Stage337W Decision(337W 결정)

- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- materialized_gate_rows(물질화 게이트 행): `{metrics['gate_rows']}`
- selected_candidate(선택 후보): `none`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

Effect(효과): run337W(337W 실행)는 cost buffer(비용 버퍼), source policy(원천 정책), proxy-MT5 parity(프록시-MT5 동등성), tester boundary(테스터 경계), model validation firewall(모델 검증 방화벽)을 실제 검토 입력으로 만들었다. 다음 최소 조건은 run337X(337X 실행)에서 이 입력들이 빠짐없이 게이트를 닫는지 검토하는 것이다.
"""
    return write_md(DECISION_DOC, text)


def update_status_docs(metrics: Mapping[str, Any]) -> list[Path]:
    artifacts: list[Path] = []
    selection_text = f"""# Stage337 Selection Status(337단계 선택 상태)

- stage_id(단계 ID): `{STAGE_ID}`
- stage_status(단계 상태): `open_active`
- selected_candidate(선택 후보): `none`
- latest_run(최신 실행): `{RUN_ID}`
- latest_decision(최신 결정): `{DECISION}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- source_policy_inputs_materialized(원천 정책 입력 물질화): `{metrics['source_age_rows']} source_age_rows`
- cost_buffer_inputs_materialized(비용 버퍼 입력 물질화): `{metrics['cost_ladder_rows']} cost_ladder_rows`
- proxy_mt5_inputs_materialized(프록시-MT5 입력 물질화): `{metrics['proxy_schema_rows']} schema_rows`
- tester_boundary_required(테스터 경계 필요): `tester must reach feature_last before Forward Passed/Failed`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- Forward Blocked(전진 차단): `current_run_boundary`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): run337W는 run337X 검토용 입력을 만들었고, 아직 모델 학습/MT5 실행/선택/운영 주장은 없다.
"""
    artifacts.append(write_md(SELECTED_STATUS, selection_text))

    focus_entry = (
        "- >-\n"
        f"  Stage337 run337W focus complete: Stage337(337단계) run337W(337W 실행)는 `{STATUS}`로 cost/source/parity/tester/model-validation inputs(비용/원천/동등성/테스터/모델 검증 입력)를 물질화했다. "
        f"Effect(효과): source age rows(원천 나이 행) `{metrics['source_age_rows']}`, cost ladder rows(비용 사다리 행) `{metrics['cost_ladder_rows']}`, proxy schema rows(프록시 스키마 행) `{metrics['proxy_schema_rows']}`를 만들고 Forward/Goal(전진/목표)은 주장하지 않는다.\n"
    )
    if path_exists(WORKSPACE_STATE):
        text, had_bom = read_text_with_bom(WORKSPACE_STATE)
        lines = text.splitlines()
        for index, line in enumerate(lines):
            if line.startswith("current_run_id:"):
                lines[index] = f"current_run_id: {NEXT_RUN_ID}"
            if line.startswith("updated_on:"):
                lines[index] = f"updated_on: '{TODAY}'"
        text = "\n".join(lines) + "\n"
        if "Stage337 run337W focus complete" not in text and "current_focus:\n" in text:
            text = text.replace("current_focus:\n", "current_focus:\n" + focus_entry + "\n", 1)
        artifacts.append(write_text_preserve_bom(WORKSPACE_STATE, text, had_bom))

    if path_exists(CURRENT_STATE):
        text, had_bom = read_text_with_bom(CURRENT_STATE)
        entry = f"""
## Stage337 run337W(337W 실행) - {TODAY}

- status(상태): `{STATUS}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): source age(원천 나이), feature-label boundary(피처-라벨 경계), proxy-MT5 schema(프록시-MT5 스키마), tester boundary(테스터 경계), model validation firewall(모델 검증 방화벽)을 실제 입력 파일로 만들었다. Forward/Goal(전진/목표)은 주장하지 않는다.
"""
        if "## Stage337 run337W(337W 실행)" not in text:
            text = text.rstrip() + "\n\n" + entry.strip() + "\n"
        artifacts.append(write_text_preserve_bom(CURRENT_STATE, text, had_bom))

    if path_exists(CHANGELOG):
        text, had_bom = read_text_with_bom(CHANGELOG)
        line = f"- {TODAY}: Stage337 run337W(337W 실행) `{STATUS}`. Effect(효과): 비용/원천/프록시-MT5/테스터/모델 검증 입력을 물질화했고 Forward/Goal(전진/목표) 주장은 없음."
        if "Stage337 run337W(337W 실행)" not in text:
            text = text.rstrip() + "\n" + line + "\n"
        artifacts.append(write_text_preserve_bom(CHANGELOG, text, had_bom))

    return artifacts


def update_registers(artifact_paths: Sequence[Path], metrics: Mapping[str, Any], generated_at: str) -> list[Path]:
    registry_paths = [
        upsert_csv(
            RUN_REGISTRY,
            ["run_id"],
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "materialization_runtime_parity_model_validation",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT_PATH),
                "notes": f"decision={DECISION};next_action={NEXT_RUN_ID};goal_achieve_not_claimed.",
                "family": "cost_buffer_source_policy_input_materialization",
                "primary_report": rel(REPORT_PATH),
            },
        ),
        upsert_csv(
            STAGE_LEDGER,
            ["run_key"],
            {
                "ledger_row_id": f"{RUN_ID}__cost_buffer_source_policy_input_materialization",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "work_family": "materialization_runtime_parity_model_validation",
                "evidence_scope": "run337V queue and run337U tester boundary evidence",
                "kpi_scope": "materialization_no_new_kpi",
                "status": STATUS,
                "judgment": JUDGMENT,
                "claim_boundary": CLAIM_BOUNDARY,
                "path": rel(REPORT_PATH),
                "notes": f"next_action={NEXT_RUN_ID};artifact_file_count={metrics['artifact_file_count']};goal_achieve_not_claimed.",
                "decision": DECISION,
                "run_key": f"{RUN_ID}__cost_buffer_source_policy_input_materialization",
                "family": "cost_buffer_source_policy_input_materialization",
                "question": "can run337V repair design be made into concrete no-overfit inputs",
                "metric_scope": "input_materialization_only_no_forward_decision",
                "primary_artifact": rel(REPORT_PATH),
            },
        ),
        upsert_csv(
            ALPHA_LEDGER,
            ["ledger_row_id"],
            {
                "ledger_row_id": f"{RUN_ID}__materialized_repair_inputs",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": "materialized_repair_inputs",
                "parent_run_id": PARENT_RUN_ID,
                "record_view": "cost_source_parity_tester_validation_inputs",
                "tier_scope": "out_of_scope_by_claim_no_tier_kpi",
                "kpi_scope": "no_new_kpi_materialization_contract",
                "scoreboard_lane": "materialization",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT_PATH),
                "primary_kpi": "not_applicable",
                "guardrail_kpi": "source_asof;proxy_mt5;tester_feature_last;no_forward_threshold",
                "external_verification_status": "out_of_scope_by_claim",
                "notes": f"next_action={NEXT_RUN_ID};goal_achieve_not_claimed.",
            },
        ),
    ]
    registry_paths.append(append_artifact_rows([*artifact_paths, Path(__file__)], generated_at))
    return registry_paths


def append_artifact_rows(paths: Sequence[Path], generated_at: str) -> Path:
    existing_rows = read_csv(ARTIFACT_REGISTRY)
    columns = ["artifact_id", "artifact_type", "path", "sha256", "stage_id", "run_id", "created_at_utc", "notes", "artifact_path", "claim_boundary"]
    new_ids = {f"{RUN_ID}::{rel(path)}" for path in paths}
    rows = [row for row in existing_rows if row.get("artifact_id") not in new_ids]
    for path in paths:
        if not path_exists(path) or not path.is_file():
            continue
        suffix = path.suffix.lower().lstrip(".") or "file"
        rows.append(
            {
                "artifact_id": f"{RUN_ID}::{rel(path)}",
                "artifact_type": suffix,
                "path": rel(path),
                "sha256": normalized_sha256(path),
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": generated_at,
                "notes": STATUS,
                "artifact_path": rel(path),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return write_csv(ARTIFACT_REGISTRY, columns, rows)


def main() -> int:
    generated_at = now_utc()
    RUN_DIR.mkdir(parents=True, exist_ok=True)
    inputs = load_inputs()

    source_age_rows, feature_boundary_rows, source_decision_rows = materialize_source_contracts(inputs)
    branch_rows, cost_ladder_rows, direction_rows = materialize_branch_contracts(inputs)
    proxy_template_rows, proxy_schema_rows, usability_rows = materialize_proxy_contracts(inputs)
    tester_plan_rows, tester_gate_rows = materialize_tester_boundary(inputs)
    model_firewall_rows, threshold_rows, split_rows = materialize_model_validation(inputs)

    rows_by_file: dict[Path, list[dict[str, Any]]] = {
        SOURCE_AGE_AUDIT_CSV: source_age_rows,
        FEATURE_LABEL_BOUNDARY_CSV: feature_boundary_rows,
        SOURCE_CLEAN_DECISION_CSV: source_decision_rows,
        BRANCH_SPEC_MANIFEST_CSV: branch_rows,
        COST_LADDER_CONTRACT_CSV: cost_ladder_rows,
        DIRECTION_CURVE_GATE_CSV: direction_rows,
        PROXY_EXPECTED_TEMPLATE_CSV: proxy_template_rows,
        PROXY_MT5_SCHEMA_CSV: proxy_schema_rows,
        USABILITY_RULE_CSV: usability_rows,
        TESTER_BOUNDARY_PLAN_CSV: tester_plan_rows,
        TESTER_FEATURE_GATE_CSV: tester_gate_rows,
        MODEL_VALIDATION_FIREWALL_CSV: model_firewall_rows,
        NO_FORWARD_THRESHOLD_CSV: threshold_rows,
        WFO_SPLIT_PLAN_CSV: split_rows,
    }
    gate_rows = materialize_gate_audit(rows_by_file)
    rows_by_file[REQUIRED_GATE_AUDIT_CSV] = gate_rows

    artifact_paths: list[Path] = [
        write_csv(SOURCE_AGE_AUDIT_CSV, ["attempt_name", "feature_set_id", "source_family", "feature_role", "asof_rule", "availability_status", "max_age_policy", "missing_rule", "lookahead_guard", "stress_slice", "invalid_if", "next_evidence", "claim_boundary"], source_age_rows),
        write_csv(FEATURE_LABEL_BOUNDARY_CSV, ["attempt_name", "feature_set_id", "label_boundary", "feature_boundary", "fixed_variables", "changed_variables", "leakage_risk", "required_negative_control", "boundary_status", "claim_boundary"], feature_boundary_rows),
        write_csv(SOURCE_CLEAN_DECISION_CSV, ["attempt_name", "feature_set_id", "source_decision", "repair_or_control_role", "selection_use", "forward_pass_fail_use", "note_ko", "next_condition", "claim_boundary"], source_decision_rows),
        write_csv(BRANCH_SPEC_MANIFEST_CSV, ["branch_id", "branch_type", "hypothesis", "fixed_variables", "changed_variables", "forbidden_shortcut", "predeclared_controls", "success_criteria", "failure_criteria", "materialization_status", "next_review", "claim_boundary"], branch_rows),
        write_csv(COST_LADDER_CONTRACT_CSV, ["attempt_name", "feature_set_id", "extra_round_trip_points", "known_reference_net", "known_reference_pf", "required_output", "pass_gate", "failure_memory", "use_boundary", "claim_boundary"], cost_ladder_rows),
        write_csv(DIRECTION_CURVE_GATE_CSV, ["axis", "required_metrics", "minimum_scope", "invalid_if", "usable_for_forward_pass_fail", "required_before_onnx_ready", "claim_boundary"], direction_rows),
        write_csv(PROXY_EXPECTED_TEMPLATE_CSV, ["attempt_name", "expected_feature_ready_count", "expected_model_ok_count", "expected_long_count", "expected_short_count", "expected_flat_count", "expected_probability_fields", "mt5_runtime_fields_required", "timestamp_alignment_rule", "usable_for_kpi_authority", "claim_boundary"], proxy_template_rows),
        write_csv(PROXY_MT5_SCHEMA_CSV, ["column_name", "data_type", "validation_rule", "required", "claim_boundary"], proxy_schema_rows),
        write_csv(USABILITY_RULE_CSV, ["usability_label", "condition", "allowed_claim", "forbidden_claim", "next_action", "claim_boundary"], usability_rows),
        write_csv(TESTER_BOUNDARY_PLAN_CSV, ["plan_step", "condition", "evidence", "action", "effect", "claim_boundary"], tester_plan_rows),
        write_csv(TESTER_FEATURE_GATE_CSV, ["gate_id", "api_latest_us100_close_utc", "feature_latest_timestamp", "tester_last_observed_bar_time", "tester_to_feature_last_gap_minutes", "required_condition", "current_status", "blocks_claim", "claim_boundary"], tester_gate_rows),
        write_csv(MODEL_VALIDATION_FIREWALL_CSV, ["firewall_id", "required_before", "condition", "blocks_if_missing", "overfit_path_blocked", "claim_boundary"], model_firewall_rows),
        write_csv(NO_FORWARD_THRESHOLD_CSV, ["contract_id", "rule", "forbidden", "required_evidence", "violation_judgment", "claim_boundary"], threshold_rows),
        write_csv(WFO_SPLIT_PLAN_CSV, ["split_id", "date_scope", "allowed_use", "forbidden_use", "required_evidence", "claim_boundary"], split_rows),
        write_csv(REQUIRED_GATE_AUDIT_CSV, ["gate_name", "status", "evidence_path", "row_count", "effect", "claim_boundary"], gate_rows),
    ]

    metrics = {
        "source_age_rows": len(source_age_rows),
        "feature_boundary_rows": len(feature_boundary_rows),
        "source_decision_rows": len(source_decision_rows),
        "branch_spec_rows": len(branch_rows),
        "cost_ladder_rows": len(cost_ladder_rows),
        "direction_gate_rows": len(direction_rows),
        "proxy_template_rows": len(proxy_template_rows),
        "proxy_schema_rows": len(proxy_schema_rows),
        "usability_rule_rows": len(usability_rows),
        "tester_boundary_rows": len(tester_gate_rows),
        "model_firewall_rows": len(model_firewall_rows),
        "threshold_contract_rows": len(threshold_rows),
        "wfo_split_rows": len(split_rows),
        "gate_rows": len(gate_rows),
        "artifact_file_count": 0,
    }
    artifact_paths.extend(build_receipts(metrics, generated_at))
    artifact_paths.append(write_report(metrics))
    artifact_paths.append(write_decision_doc(metrics))
    artifact_paths.extend(update_status_docs(metrics))

    metrics["artifact_file_count"] = len([path for path in artifact_paths if path_exists(path)]) + 2
    final_decision = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        **metrics,
        "mt5_execution": "not_run",
        "model_training": "not_run",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "runtime_authority": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    artifact_paths.append(write_json(FINAL_DECISION_JSON, final_decision))
    artifact_paths.append(
        write_json(
            RUN_MANIFEST_JSON,
            {
                **final_decision,
                "generated_at_utc": generated_at,
                "producer": rel(Path(__file__)),
                "source_inputs": [rel(V_QUEUE), rel(V_SOURCE_POLICY), rel(V_COST_BRANCHES), rel(V_OVERFIT_GATES), rel(V_ECONOMIC_SOURCES), rel(V_FAILURE_DIGEST), rel(U_DECISION)],
                "artifacts": [rel(path) for path in [*artifact_paths, RUN_MANIFEST_JSON] if path_exists(path) or path == RUN_MANIFEST_JSON],
            },
        )
    )
    artifact_paths.extend(update_registers(artifact_paths, metrics, generated_at))
    print(json.dumps(final_decision, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
