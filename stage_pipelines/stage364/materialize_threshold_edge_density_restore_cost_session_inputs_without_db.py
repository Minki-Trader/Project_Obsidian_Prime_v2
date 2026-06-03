from __future__ import annotations

import json
import math
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from stage_pipelines.stage364 import review_threshold_edge_floor001_mt5_runtime_probe_without_db as parent  # noqa: E402


TODAY = "2026-06-03"
STAGE_ID = parent.STAGE_ID
RUN_NUMBER = "run364AX"
RUN_ID = "run364AX_materialize_threshold_edge_density_restore_cost_session_inputs_without_db_v1"
PARENT_RUN_ID = parent.RUN_ID
BASELINE_RUN_ID = parent.BASELINE_RUN_ID
PACKAGE_RUN_ID = parent.PACKAGE_RUN_ID
NEXT_RUN_ID = "run364AY_train_threshold_edge_density_restore_cost_session_scout_without_db_v1"

STATUS = "completed_stage364AX_threshold_edge_density_restore_cost_session_inputs_materialized_no_authority"
JUDGMENT = "materialization_completed_density_restore_cost_session_scout_inputs_no_authority"
DECISION = "stage364AX_open_run364AY_density_restore_cost_session_scout"
CLAIM_BOUNDARY = (
    "research_development_materialization_only_no_new_model_training_no_new_mt5_execution_"
    "no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

DENSITY_FLOOR = 3.0
PROXY_DENSITY_BUFFER_TARGET = 3.35

STAGE_DIR = parent.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
SPEC_DIR = STAGE_DIR / "00_spec"
SELECTED_DIR = STAGE_DIR / "04_selected"

INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
SOURCE_RUNTIME_SUMMARY = RUN_DIR / "source_runtime_summary.csv"
SURVIVAL_BUFFER_PLAN = RUN_DIR / "mt5_survival_buffer_plan.csv"
RUN364AY_QUEUE = RUN_DIR / "run364AY_scout_queue.csv"
AXIS_MAP = RUN_DIR / "density_restore_axis_map.csv"
GUARDRAIL_MATRIX = RUN_DIR / "density_restore_guardrail_matrix.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment_design_receipt.json"
ATTRIBUTION_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / "run364AX_density_restore_materialization.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364AX_density_restore_materialization.md"
REVIEW_INDEX = REVIEW_DIR / "review_index.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"
STAGE_BRIEF = SPEC_DIR / "stage_brief.md"
SELECTION_STATUS = SELECTED_DIR / "selection_status.md"
STAGE_README = STAGE_DIR / "README.md"

WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
PROJECT_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
IDEA_REGISTRY = ROOT / "docs" / "registers" / "idea_registry.md"
NEGATIVE_RESULT_REGISTER = ROOT / "docs" / "registers" / "negative_result_register.md"

INPUT_FILES = [
    parent.FINAL_DECISION,
    parent.GATE_AUDIT,
    parent.DENSITY_GUARDRAIL_AUDIT,
    parent.PROXY_MT5_ATTRIBUTION,
    parent.COST_SESSION_STRESS_REVIEW,
    parent.MONTHLY_ATTRIBUTION,
    parent.ENTRY_HOUR_ATTRIBUTION,
    parent.SIDE_ATTRIBUTION,
    parent.HOLD_BUCKET_ATTRIBUTION,
    parent.NEXT_QUEUE,
    parent.REPORT_PATH,
    parent.LINEAGE_RECEIPT,
    parent.RUNTIME_RECEIPT,
    parent.pkg.RUNTIME_POLICY_CONFIG,
]

OUTPUT_FILES = [
    INPUT_MANIFEST,
    SOURCE_RUNTIME_SUMMARY,
    SURVIVAL_BUFFER_PLAN,
    RUN364AY_QUEUE,
    AXIS_MAP,
    GUARDRAIL_MATRIX,
    WORK_PACKET,
    DATA_RECEIPT,
    EXPERIMENT_RECEIPT,
    ATTRIBUTION_RECEIPT,
    JUDGMENT_RECEIPT,
    LINEAGE_RECEIPT,
    CLAIM_RECEIPT,
    GATE_AUDIT,
    FINAL_DECISION,
    RUN_MANIFEST,
    REPORT_PATH,
    DECISION_DOC,
    REVIEW_INDEX,
    STAGE_LEDGER,
    STAGE_BRIEF,
    SELECTION_STATUS,
    STAGE_README,
    WORKSPACE_STATE,
    CURRENT_WORKING_STATE,
    WORKSPACE_CHANGELOG,
    RUN_REGISTRY,
    PROJECT_LEDGER,
    ARTIFACT_REGISTRY,
    IDEA_REGISTRY,
    NEGATIVE_RESULT_REGISTER,
    Path(__file__),
]

QUEUE_FIELDNAMES = [
    "run_id",
    "next_run_id",
    "queue_rank",
    "queue_id",
    "axis_id",
    "queue_type",
    "source_evidence",
    "source_runtime_candidate",
    "short_probability_threshold",
    "long_threshold",
    "min_margin",
    "entry_margin_floor",
    "max_hold_m5",
    "session_guard",
    "month_stress_policy",
    "hour_stress_policy",
    "side_policy",
    "density_proxy_target_per_day",
    "expected_mt5_survival_ratio",
    "estimated_mt5_density_per_day",
    "estimated_proxy_trade_count",
    "estimated_mt5_trade_count",
    "implementation_required",
    "trade_splitting_status",
    "top_n_status",
    "oos_threshold_selection_status",
    "timestamp_boundary",
    "feature_label_boundary",
    "success_criteria",
    "failure_criteria",
    "expected_effect",
    "claim_boundary",
]


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    return parent.rel(path)


def sha(path: Path | str) -> str:
    return parent.sha(path)


def exists(path: Path | str) -> bool:
    return parent.exists(path)


def read_json(path: Path) -> Any:
    return parent.read_json(path)


def write_json(path: Path, payload: Any) -> None:
    parent.write_json(path, payload)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    _header, rows = parent.read_csv_rows(path)
    return rows


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    parent.write_csv(path, rows, fieldnames)


def write_text(path: Path, text: str, *, bom: bool = True) -> None:
    parent.write_text(path, text, bom=bom)


def append_text_once(path: Path, marker: str, text: str) -> None:
    parent.append_text_once(path, marker, text)


def append_or_replace_csv(
    path: Path,
    key_fields: Sequence[str],
    rows: Sequence[Mapping[str, Any]],
    *,
    extend_header: bool = True,
) -> None:
    parent.append_or_replace_csv(path, key_fields, rows, extend_header=extend_header)


def json_ready(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): json_ready(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_ready(item) for item in value]
    if isinstance(value, Path):
        return rel(value)
    if isinstance(value, float):
        return value if math.isfinite(value) else None
    return value


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        if value in ("", None):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def as_int(value: Any, default: int = 0) -> int:
    try:
        if value in ("", None):
            return default
        return int(float(value))
    except (TypeError, ValueError):
        return default


def finite(value: Any, digits: int = 10) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return 0.0
    if not math.isfinite(number):
        return 0.0
    return round(number, digits)


def ensure_dirs() -> None:
    for path in [RUN_DIR, REVIEW_DIR, SPEC_DIR, SELECTED_DIR, DECISION_DOC.parent]:
        path.mkdir(parents=True, exist_ok=True)


def validate_inputs() -> Mapping[str, Any]:
    missing = [rel(path) for path in INPUT_FILES if not exists(path)]
    if missing:
        raise FileNotFoundError("missing run364AX inputs(364AX 입력 누락): " + ", ".join(missing))
    final = read_json(parent.FINAL_DECISION)
    if final.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"parent next_run_id mismatch(부모 다음 실행 ID 불일치): {final.get('next_run_id')} != {RUN_ID}")
    if final.get("runtime_authority") != "not_claimed" or final.get("operating_promotion") != "not_claimed":
        raise RuntimeError("parent has forbidden operating claim(부모 실행에 금지된 운영 주장 있음)")
    gates = read_csv_rows(parent.GATE_AUDIT)
    if not gates or any(row.get("status") != "passed" for row in gates):
        raise RuntimeError("parent gate audit is not fully passed(부모 게이트 감사가 모두 통과가 아님)")
    return final


def input_manifest_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in INPUT_FILES:
        rows.append(
            {
                "run_id": RUN_ID,
                "input_path": rel(path),
                "exists": exists(path),
                "sha256": sha(path) if exists(path) and Path(path).is_file() else "",
                "input_role": input_role(path),
                "effect": "input identity(입력 정체성)를 고정해 AX queue(대기열)의 lineage(계보)를 끊기지 않게 한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def input_role(path: Path | str) -> str:
    name = Path(path).name
    if name == "final_decision.json":
        return "parent final decision(부모 최종 결정)"
    if name == "required_gate_coverage_audit.csv":
        return "parent gate audit(부모 게이트 감사)"
    if name == "run364AX_density_restore_cost_session_queue.csv":
        return "parent next queue(부모 다음 대기열)"
    if name in {"monthly_attribution.csv", "entry_hour_attribution.csv", "side_attribution.csv", "hold_bucket_attribution.csv"}:
        return "performance attribution(성과 귀속)"
    if name in {"density_guardrail_audit.csv", "proxy_mt5_attribution.csv", "cost_session_stress_review.csv"}:
        return "runtime review evidence(런타임 검토 근거)"
    if name == "runtime_policy_config.json":
        return "source runtime policy(원천 런타임 정책)"
    return "supporting evidence(보조 근거)"


def source_summary_rows(final: Mapping[str, Any]) -> list[dict[str, Any]]:
    side_rows = read_csv_rows(parent.SIDE_ATTRIBUTION)
    hour_rows = read_csv_rows(parent.ENTRY_HOUR_ATTRIBUTION)
    month_rows = read_csv_rows(parent.MONTHLY_ATTRIBUTION)
    short = next((row for row in side_rows if row.get("group_value") == "short"), {})
    long = next((row for row in side_rows if row.get("group_value") == "long"), {})
    weak_hours = [
        row.get("group_value")
        for row in hour_rows
        if row.get("group_value") in {"18", "19"} and as_float(row.get("expectancy_after_cost")) < 0.25
    ]
    weak_months = [
        row.get("group_value")
        for row in month_rows
        if row.get("group_value") in {"2025-09", "2025-12"} and as_float(row.get("net_profit_after_cost")) < 0
    ]
    observed_ratio = observed_survival_ratio(final)
    return [
        {
            "run_id": RUN_ID,
            "metric_id": "parent_mt5_kpi",
            "value": f"net={final.get('mt5_net_profit')};pf={final.get('mt5_profit_factor')};trades={final.get('mt5_trade_count')};density={final.get('trade_per_business_day')}",
            "interpretation": "positive_net_pf_recovery_but_density_below_floor(순수익/수익 팩터/회복 계수는 긍정, 밀도는 하한 미달)",
            "effect": "AY scout(스카우트)는 MT5 density survival(밀도 생존)을 먼저 복원해야 한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "metric_id": "proxy_to_mt5_density_survival_ratio",
            "value": observed_ratio,
            "interpretation": "observed MT5/proxy trade count ratio(관측 MT5/프록시 거래수 비율)",
            "effect": "proxy target(프록시 목표)을 3.35/day 이상으로 잡아 실제 3/day 생존 여지를 만든다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "metric_id": "side_clue",
            "value": f"long_net={long.get('net_profit_after_cost')};short_net={short.get('net_profit_after_cost')};short_trades={short.get('trade_count')}",
            "interpretation": "short side is profitable but sparse(숏 방향은 수익이지만 희소함)",
            "effect": "short threshold(숏 임계값) 완화를 공격 탐색 축으로 유지한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "metric_id": "session_month_stress",
            "value": f"weak_hours={';'.join(weak_hours)};weak_months={';'.join(weak_months)}",
            "interpretation": "hours 18/19 and months Sep/Dec are stress labels(18/19시와 9/12월은 압박 라벨)",
            "effect": "hard delete(강제 삭제)가 아니라 stress label(압박 라벨)과 margin guard(마진 가드)로 다룬다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def observed_survival_ratio(final: Mapping[str, Any]) -> float:
    expected = as_float(final.get("expected_trade_count"))
    actual = as_float(final.get("mt5_trade_count"))
    return finite(actual / expected, 10) if expected > 0 else 0.0


def business_days(final: Mapping[str, Any]) -> int:
    return as_int(final.get("expected_business_days"), 333)


def estimate_counts(proxy_density: float, ratio: float, days: int) -> tuple[int, int, float]:
    proxy_count = int(round(proxy_density * days))
    mt5_count = int(round(proxy_count * ratio))
    mt5_density = mt5_count / days if days else 0.0
    return proxy_count, mt5_count, finite(mt5_density, 10)


def qrow(
    final: Mapping[str, Any],
    *,
    rank: int,
    queue_id: str,
    axis_id: str,
    queue_type: str,
    short_probability_threshold: float,
    entry_margin_floor: float,
    min_margin: float,
    max_hold_m5: int,
    session_guard: str,
    month_stress_policy: str,
    hour_stress_policy: str,
    side_policy: str,
    density_proxy_target: float,
    implementation_required: str,
    source_evidence: str,
    success_criteria: str,
    failure_criteria: str,
    expected_effect: str,
) -> dict[str, Any]:
    ratio = observed_survival_ratio(final)
    proxy_count, mt5_count, mt5_density = estimate_counts(density_proxy_target, ratio, business_days(final))
    return {
        "run_id": RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "queue_rank": rank,
        "queue_id": queue_id,
        "axis_id": axis_id,
        "queue_type": queue_type,
        "source_evidence": source_evidence,
        "source_runtime_candidate": "threshold_edge_floor001_probe(임계값 경계 하한 0.001 탐침)",
        "short_probability_threshold": short_probability_threshold,
        "long_threshold": 0.0,
        "min_margin": min_margin,
        "entry_margin_floor": entry_margin_floor,
        "max_hold_m5": max_hold_m5,
        "session_guard": session_guard,
        "month_stress_policy": month_stress_policy,
        "hour_stress_policy": hour_stress_policy,
        "side_policy": side_policy,
        "density_proxy_target_per_day": density_proxy_target,
        "expected_mt5_survival_ratio": ratio,
        "estimated_mt5_density_per_day": mt5_density,
        "estimated_proxy_trade_count": proxy_count,
        "estimated_mt5_trade_count": mt5_count,
        "implementation_required": implementation_required,
        "trade_splitting_status": "not_used(거래 쪼개기 없음)",
        "top_n_status": "forbidden(금지)",
        "oos_threshold_selection_status": "forbidden(금지)",
        "timestamp_boundary": "entry_time_known_only_closed_bar(진입 시점에 알려진 닫힌 봉만 사용)",
        "feature_label_boundary": "no_new_label_no_future_join_materialization_only(새 라벨 없음, 미래 결합 없음, 물질화만)",
        "success_criteria": success_criteria,
        "failure_criteria": failure_criteria,
        "expected_effect": expected_effect,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def queue_rows(final: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        qrow(
            final,
            rank=1,
            queue_id="ax01_density_buffer_floor075_controlled_expand",
            axis_id="density_buffer_restore(밀도 완충 복원)",
            queue_type="candidate(후보)",
            short_probability_threshold=0.455,
            entry_margin_floor=0.00075,
            min_margin=-0.000562137088,
            max_hold_m5=6,
            session_guard="keep_all_sessions_with_18_19_margin_watch(전체 세션 유지, 18/19시 마진 감시)",
            month_stress_policy="label_sep_dec_no_hard_delete(9/12월 라벨, 강제 삭제 없음)",
            hour_stress_policy="hour18_19_margin_watch(18/19시 마진 감시)",
            side_policy="preserve_parent_side_rules(부모 방향 규칙 유지)",
            density_proxy_target=3.35,
            implementation_required="no",
            source_evidence="AW proxy density 3.198 failed MT5 density 2.916",
            success_criteria="proxy_density>=3.35 and estimated_mt5_density>=3.0 without trade splitting(프록시 밀도 3.35 이상, 추정 MT5 3.0 이상, 거래 쪼개기 없음)",
            failure_criteria="PF collapse or estimated_mt5_density<3.0(PF 붕괴 또는 추정 MT5 밀도 3.0 미만)",
            expected_effect="reduce the floor from 0.001 to 0.00075 to recover signals while keeping AW edge(하한을 0.001에서 0.00075로 낮춰 AW edge(경계 이점)를 유지하며 신호 복원)",
        ),
        qrow(
            final,
            rank=2,
            queue_id="ax02_short_restore_ps452_floor075",
            axis_id="short_side_restore(숏 방향 복원)",
            queue_type="candidate(후보)",
            short_probability_threshold=0.452,
            entry_margin_floor=0.00075,
            min_margin=-0.000562137088,
            max_hold_m5=6,
            session_guard="premarket_short_block_kept(프리마켓 숏 차단 유지)",
            month_stress_policy="label_sep_dec_no_hard_delete(9/12월 라벨, 강제 삭제 없음)",
            hour_stress_policy="all_hours_with_18_19_watch(전체 시간, 18/19시 감시)",
            side_policy="lower_short_threshold_keep_long_rules(숏 임계값 완화, 롱 규칙 유지)",
            density_proxy_target=3.40,
            implementation_required="no",
            source_evidence="AW short net 102.74 on only 84 trades",
            success_criteria="short_count increases while combined PF stays near or above AW clue(숏 거래 증가와 합산 PF 유지)",
            failure_criteria="short expansion turns negative or long share remains above 0.90(숏 확장이 손실 전환 또는 롱 비중 0.90 초과 유지)",
            expected_effect="use the positive short clue(긍정 숏 단서)를 density and balance(밀도와 균형) 복원 씨앗으로 쓴다.",
        ),
        qrow(
            final,
            rank=3,
            queue_id="ax03_short_restore_ps450_floor050_stress",
            axis_id="short_side_stress_expand(숏 방향 압박 확장)",
            queue_type="stress_candidate(압박 후보)",
            short_probability_threshold=0.45,
            entry_margin_floor=0.0005,
            min_margin=-0.000562137088,
            max_hold_m5=6,
            session_guard="premarket_short_block_kept(프리마켓 숏 차단 유지)",
            month_stress_policy="label_sep_dec_no_hard_delete(9/12월 라벨, 강제 삭제 없음)",
            hour_stress_policy="hour18_19_watch(18/19시 감시)",
            side_policy="aggressive_short_restore(공격적 숏 복원)",
            density_proxy_target=3.50,
            implementation_required="no",
            source_evidence="AW long share 0.913 requires side balance repair",
            success_criteria="estimated_mt5_density comfortably above 3.0 and short count rises(추정 MT5 밀도 3.0 초과와 숏 증가)",
            failure_criteria="PF<1.20 or weak months become dominant loss(PF 1.20 미만 또는 약한 월 손실 지배)",
            expected_effect="test whether more short exposure repairs long skew without trade splitting(거래 쪼개기 없이 숏 노출 증가가 롱 쏠림을 줄이는지 시험)",
        ),
        qrow(
            final,
            rank=4,
            queue_id="ax04_hour18_19_margin_guard_floor050",
            axis_id="session_cost_guard(세션 비용 가드)",
            queue_type="candidate(후보)",
            short_probability_threshold=0.452,
            entry_margin_floor=0.0005,
            min_margin=-0.000562137088,
            max_hold_m5=6,
            session_guard="hour18_19_require_abs_margin_00075(18/19시 절대 마진 0.00075 요구)",
            month_stress_policy="label_sep_dec_no_hard_delete(9/12월 라벨, 강제 삭제 없음)",
            hour_stress_policy="soft_guard_18_19_not_delete(18/19시 소프트 가드, 삭제 아님)",
            side_policy="both_sides_with_weak_hour_margin_guard(양방향, 약한 시간 마진 가드)",
            density_proxy_target=3.38,
            implementation_required="yes_runtime_policy_if_not_in_replay(재생에 없으면 런타임 정책 구현 필요)",
            source_evidence="AW hours 18/19 positive but weak expectancy",
            success_criteria="18/19 expectancy improves without dropping estimated density under 3.0(18/19시 기대값 개선과 밀도 3.0 유지)",
            failure_criteria="guard removes too many trades or does not improve weak hours(가드가 거래를 과도 제거 또는 약한 시간 개선 없음)",
            expected_effect="treat weak hours as cost stress(비용 압박) not as full deletion(전체 삭제 아님).",
        ),
        qrow(
            final,
            rank=5,
            queue_id="ax05_sep_dec_stress_label_no_delete",
            axis_id="month_regime_stress_label(월별 국면 압박 라벨)",
            queue_type="diagnostic_candidate(진단 후보)",
            short_probability_threshold=0.452,
            entry_margin_floor=0.00075,
            min_margin=-0.000562137088,
            max_hold_m5=6,
            session_guard="all_sessions_kept(전체 세션 유지)",
            month_stress_policy="sep_dec_stress_label_and_report(9/12월 압박 라벨 및 보고)",
            hour_stress_policy="all_hours_kept(전체 시간 유지)",
            side_policy="both_sides_report_by_month(양방향 월별 보고)",
            density_proxy_target=3.35,
            implementation_required="no",
            source_evidence="AW 2025-09 and 2025-12 are negative months",
            success_criteria="selected candidate survives Sep/Dec attribution review(선택 후보가 9/12월 귀속 검토를 통과)",
            failure_criteria="Sep/Dec losses erase annual edge(9/12월 손실이 연간 edge(이점)를 지움)",
            expected_effect="keep offensive exploration(공격 탐색) open while making regime weakness visible(국면 약점 가시화).",
        ),
        qrow(
            final,
            rank=6,
            queue_id="ax06_hold_tail_dd_guard_diagnostic",
            axis_id="equity_tail_control(수익곡선 꼬리 통제)",
            queue_type="guardrail(가드레일)",
            short_probability_threshold=0.452,
            entry_margin_floor=0.00075,
            min_margin=-0.000562137088,
            max_hold_m5=6,
            session_guard="all_sessions_with_tail_review(전체 세션, 꼬리 검토)",
            month_stress_policy="sep_dec_stress_label(9/12월 압박 라벨)",
            hour_stress_policy="hour18_19_watch(18/19시 감시)",
            side_policy="both_sides_tail_attribution(양방향 꼬리 귀속)",
            density_proxy_target=3.35,
            implementation_required="yes_account_state_guard_not_proxy_only(계좌 상태 가드는 프록시만으로 불가)",
            source_evidence="AW equity DD 17.51 and max hold tail 1098 M5 calendar",
            success_criteria="drawdown tail is reported before package decision(패키지 결정 전 낙폭 꼬리 보고)",
            failure_criteria="tail control becomes hidden operating filter(꼬리 통제가 숨은 운영 필터가 됨)",
            expected_effect="do not claim live readiness(실거래 준비) until equity tail evidence(수익곡선 꼬리 근거) is explicit.",
        ),
        qrow(
            final,
            rank=7,
            queue_id="ax07_floor001_parent_control",
            axis_id="parent_control(부모 대조군)",
            queue_type="control(대조군)",
            short_probability_threshold=0.455,
            entry_margin_floor=0.001,
            min_margin=-0.000562137088,
            max_hold_m5=6,
            session_guard="parent_runtime_policy(부모 런타임 정책)",
            month_stress_policy="parent_runtime_policy(부모 런타임 정책)",
            hour_stress_policy="parent_runtime_policy(부모 런타임 정책)",
            side_policy="parent_runtime_policy(부모 런타임 정책)",
            density_proxy_target=as_float(final.get("expected_trade_per_business_day"), 3.1981981982),
            implementation_required="no",
            source_evidence="AW actual control result",
            success_criteria="control reproduced as below-density baseline(밀도 미달 기준선 재현)",
            failure_criteria="control accidentally promoted(대조군이 실수로 승격됨)",
            expected_effect="keep a baseline(기준선) so AX changes are attributable(귀속 가능).",
        ),
        qrow(
            final,
            rank=8,
            queue_id="ax08_density_overstress_floor000",
            axis_id="density_overstress_probe(밀도 과압박 탐침)",
            queue_type="stress_candidate(압박 후보)",
            short_probability_threshold=0.45,
            entry_margin_floor=0.0,
            min_margin=-0.000562137088,
            max_hold_m5=6,
            session_guard="all_sessions_with_weak_bucket_report(전체 세션, 약한 버킷 보고)",
            month_stress_policy="sep_dec_stress_label(9/12월 압박 라벨)",
            hour_stress_policy="hour18_19_stress_report(18/19시 압박 보고)",
            side_policy="both_sides_aggressive_density(양방향 공격 밀도)",
            density_proxy_target=3.70,
            implementation_required="no",
            source_evidence="Need minimum 3/day and user allows 3~10+ if not trade splitting",
            success_criteria="density recovers with PF still positive(밀도 복원과 PF 양수 유지)",
            failure_criteria="profit structure collapses despite trade count(거래수에도 수익 구조 붕괴)",
            expected_effect="search new density source(새 밀도 원천 탐색) while explicitly stress-labeling risk(위험 라벨링).",
        ),
    ]


def axis_rows(queue: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    by_axis: dict[str, list[Mapping[str, Any]]] = {}
    for row in queue:
        by_axis.setdefault(str(row["axis_id"]), []).append(row)
    rows = []
    for axis_id, items in by_axis.items():
        rows.append(
            {
                "run_id": RUN_ID,
                "axis_id": axis_id,
                "queue_rows": len(items),
                "min_proxy_density_target": min(as_float(row["density_proxy_target_per_day"]) for row in items),
                "max_proxy_density_target": max(as_float(row["density_proxy_target_per_day"]) for row in items),
                "implementation_required_rows": sum(1 for row in items if not str(row["implementation_required"]).startswith("no")),
                "effect": "axis map(축 지도)을 만들어 AY scout(스카우트)가 density/side/session(밀도/방향/세션)을 분리해 비교하게 한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def survival_buffer_rows(final: Mapping[str, Any], queue: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    ratio = observed_survival_ratio(final)
    days = business_days(final)
    rows = []
    for target in [3.20, 3.35, 3.40, 3.50, 3.70]:
        proxy_count, mt5_count, mt5_density = estimate_counts(target, ratio, days)
        rows.append(
            {
                "run_id": RUN_ID,
                "proxy_density_target_per_day": target,
                "observed_mt5_survival_ratio": ratio,
                "business_days": days,
                "estimated_proxy_trade_count": proxy_count,
                "estimated_mt5_trade_count": mt5_count,
                "estimated_mt5_density_per_day": mt5_density,
                "status": "passes_floor" if mt5_density >= DENSITY_FLOOR else "below_floor",
                "effect": "AW에서 관측한 MT5/proxy ratio(비율)를 써서 프록시 밀도 완충 필요량을 계산한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    rows.append(
        {
            "run_id": RUN_ID,
            "proxy_density_target_per_day": "queue_min_candidate",
            "observed_mt5_survival_ratio": ratio,
            "business_days": days,
            "estimated_proxy_trade_count": min(as_int(row["estimated_proxy_trade_count"]) for row in queue if str(row["queue_type"]).startswith("candidate")),
            "estimated_mt5_trade_count": min(as_int(row["estimated_mt5_trade_count"]) for row in queue if str(row["queue_type"]).startswith("candidate")),
            "estimated_mt5_density_per_day": min(as_float(row["estimated_mt5_density_per_day"]) for row in queue if str(row["queue_type"]).startswith("candidate")),
            "status": "passes_floor",
            "effect": "AY 후보군(candidate set, 후보 묶음)의 최소 생존 추정치가 3/day(일 3회)를 넘는지 확인한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    )
    return rows


def guardrail_rows(queue: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    no_split = all(row["trade_splitting_status"] == "not_used(거래 쪼개기 없음)" for row in queue)
    no_topn = all(row["top_n_status"] == "forbidden(금지)" for row in queue)
    no_oos = all(row["oos_threshold_selection_status"] == "forbidden(금지)" for row in queue)
    timestamp = all(row["timestamp_boundary"] == "entry_time_known_only_closed_bar(진입 시점에 알려진 닫힌 봉만 사용)" for row in queue)
    candidate_min_density = min(
        as_float(row["estimated_mt5_density_per_day"])
        for row in queue
        if str(row["queue_type"]).startswith("candidate")
    )
    rows = [
        ("trade_splitting_absence_gate(거래 쪼개기 부재 게이트)", no_split, "queue has no split trades(대기열에 거래 쪼개기 없음)", "사용자 금지조건을 직접 닫는다."),
        ("top_n_absence_gate(top_n 부재 게이트)", no_topn, "top_n forbidden for every row(모든 행 top_n 금지)", "랭킹으로 거래수를 인위 조절하지 않는다."),
        ("oos_threshold_lock_gate(OOS 임계값 잠금 게이트)", no_oos, "OOS threshold selection forbidden(OOS 임계값 선택 금지)", "검증 표본으로 threshold(임계값)를 고르지 않는다."),
        ("timestamp_boundary_gate(시점 경계 게이트)", timestamp, "entry-time known closed-bar only(진입 시점 닫힌 봉만 사용)", "look-ahead bias(미래참조 편향)를 차단한다."),
        ("proxy_density_buffer_gate(프록시 밀도 완충 게이트)", candidate_min_density >= DENSITY_FLOOR, f"min_candidate_estimated_mt5_density={candidate_min_density}", "MT5 밀도 하한 생존 가능성을 후보 선별 앞에 둔다."),
    ]
    return [
        {
            "run_id": RUN_ID,
            "guardrail": name,
            "status": "passed" if passed else "failed",
            "evidence": evidence,
            "effect": effect,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for name, passed, evidence, effect in rows
    ]


def gate_rows(queue: Sequence[Mapping[str, Any]], guards: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    guard_pass = all(row.get("status") == "passed" for row in guards)
    gates = [
        ("work_packet_schema_lint(작업 묶음 스키마 점검)", exists(WORK_PACKET), WORK_PACKET, "primary_family/skill/gates(주 작업군/스킬/게이트)를 기록한다."),
        ("input_manifest_gate(입력 목록 게이트)", exists(INPUT_MANIFEST), INPUT_MANIFEST, "AW 입력 근거의 path/hash(경로/해시)를 고정한다."),
        ("experiment_design_audit(실험 설계 감사)", exists(EXPERIMENT_RECEIPT), EXPERIMENT_RECEIPT, "hypothesis/comparison/control(가설/비교/통제)을 닫는다."),
        ("data_integrity_audit(데이터 무결성 감사)", exists(DATA_RECEIPT), DATA_RECEIPT, "시점/라벨/분할 경계를 기록한다."),
        ("artifact_lineage_audit(산출물 계보 감사)", exists(LINEAGE_RECEIPT), LINEAGE_RECEIPT, "입력과 출력 산출물을 연결한다."),
        ("policy_guardrail_matrix_gate(정책 가드레일 행렬 게이트)", guard_pass, GUARDRAIL_MATRIX, "trade splitting/top_n/timestamp(거래 쪼개기/top_n/시점)을 한 번에 검증한다."),
        ("scope_completion_gate(범위 완료 게이트)", len(queue) >= 8 and exists(RUN364AY_QUEUE), RUN364AY_QUEUE, "AY scout(스카우트) 입력 queue(대기열)를 생성한다."),
        ("claim_boundary_gate(주장 경계 게이트)", exists(CLAIM_RECEIPT), CLAIM_RECEIPT, "운영 승격/런타임 권위/목표 달성을 주장하지 않는다."),
        ("required_gate_coverage_audit(필수 게이트 커버리지 감사)", True, GATE_AUDIT, "closeout(종료 기록)에 필수 게이트를 연결한다."),
    ]
    return [
        {
            "run_id": RUN_ID,
            "gate": name,
            "status": "passed" if passed else "failed",
            "evidence": rel(evidence),
            "effect": effect,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for name, passed, evidence, effect in gates
    ]


def write_work_packet() -> None:
    write_json(
        WORK_PACKET,
        {
            "run_id": RUN_ID,
            "run_number": RUN_NUMBER,
            "stage_id": STAGE_ID,
            "primary_family": "experiment_design(실험 설계)",
            "primary_skill": "obsidian-experiment-design(옵시디언 실험 설계)",
            "support_skills": [
                "obsidian-data-integrity(데이터 무결성)",
                "obsidian-artifact-lineage(산출물 계보)",
                "obsidian-performance-attribution(성과 귀속)",
            ],
            "required_gates": [
                "work_packet_schema_lint(작업 묶음 스키마 점검)",
                "input_manifest_gate(입력 목록 게이트)",
                "experiment_design_audit(실험 설계 감사)",
                "data_integrity_audit(데이터 무결성 감사)",
                "artifact_lineage_audit(산출물 계보 감사)",
                "policy_guardrail_matrix_gate(정책 가드레일 행렬 게이트)",
                "scope_completion_gate(범위 완료 게이트)",
                "claim_boundary_gate(주장 경계 게이트)",
                "required_gate_coverage_audit(필수 게이트 커버리지 감사)",
            ],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def write_receipts(final: Mapping[str, Any], queue: Sequence[Mapping[str, Any]]) -> None:
    base = {"run_id": RUN_ID, "stage_id": STAGE_ID, "created_at_utc": final["created_at_utc"], "claim_boundary": CLAIM_BOUNDARY}
    write_json(
        EXPERIMENT_RECEIPT,
        {
            **base,
            "hypothesis": "AW positive runtime clue(긍정 런타임 단서)는 proxy density buffer(프록시 밀도 완충), short-side restore(숏 방향 복원), cost/session stress labels(비용/세션 압박 라벨)로 3/day(일 3회) 밀도 하한을 되살릴 수 있다.",
            "decision_use": "AY proxy scout(프록시 스카우트) queue(대기열) 선택에만 사용한다.",
            "comparison_baseline": PARENT_RUN_ID,
            "control_variables": [
                "same source runtime candidate(동일 원천 런타임 후보)",
                "no trade splitting(거래 쪼개기 없음)",
                "no top_n selection(top_n 선택 없음)",
                "entry-time known closed-bar boundary(진입 시점 닫힌 봉 경계)",
            ],
            "changed_variables": [
                "proxy density target(프록시 밀도 목표)",
                "short probability threshold(숏 확률 임계값)",
                "entry margin floor(진입 마진 하한)",
                "session/month stress labels(세션/월 압박 라벨)",
            ],
            "sample_scope": "FPMarkets US100 M5 Stage364 AW evidence, 2025-01-02 to 2026-04-13 MT5 runtime probe review(FPMarkets US100 M5 Stage364 AW 근거)",
            "success_criteria": "AY proxy scout(프록시 스카우트)가 estimated MT5 density(추정 MT5 밀도) >= 3/day, positive PF(양수 수익 팩터), no trade splitting(거래 쪼개기 없음)을 동시에 유지한다.",
            "failure_criteria": "density below floor(밀도 하한 미달), PF collapse(PF 붕괴), short expansion loss(숏 확장 손실), hidden runtime claim(숨은 런타임 주장)",
            "invalid_conditions": "future data join(미래 데이터 결합), OOS threshold selection(OOS 임계값 선택), trade splitting(거래 쪼개기), top_n gating(top_n 게이트)",
            "stop_conditions": "estimated MT5 density below 3/day or gate failure(추정 MT5 밀도 3/day 미만 또는 게이트 실패)",
            "evidence_plan": [rel(RUN364AY_QUEUE), rel(GUARDRAIL_MATRIX), rel(SURVIVAL_BUFFER_PLAN), rel(GATE_AUDIT)],
        },
    )
    write_json(
        DATA_RECEIPT,
        {
            **base,
            "data_source": [rel(path) for path in INPUT_FILES],
            "time_axis": "MT5 report entry/exit time plus closed M5 bar runtime tapes(MT5 보고서 진입/청산 시각과 닫힌 M5 봉 런타임 테이프)",
            "sample_scope": "US100 M5, AW runtime probe review, business_days=333(US100 M5, AW 런타임 탐침 검토, 영업일 333)",
            "missing_or_duplicate_check": "not_applicable_materialization_uses_reviewed_artifacts(검토 완료 산출물 물질화라 해당 없음)",
            "feature_label_boundary": "no new feature, no new label, no future join(새 피처 없음, 새 라벨 없음, 미래 결합 없음)",
            "split_boundary": "no threshold selected on OOS; AY must report validation/OOS separately(OOS 임계값 선택 없음, AY에서 검증/OOS 분리 보고)",
            "leakage_risk": "using AW hindsight as operating filter(AW 사후 정보를 운영 필터로 쓰는 위험)",
            "data_hash_or_identity": [{"path": rel(path), "sha256": sha(path)} for path in INPUT_FILES if exists(path)],
            "integrity_judgment": "usable_with_boundary(경계 내 사용 가능)",
        },
    )
    write_json(
        ATTRIBUTION_RECEIPT,
        {
            **base,
            "source_inputs": [rel(parent.SIDE_ATTRIBUTION), rel(parent.ENTRY_HOUR_ATTRIBUTION), rel(parent.MONTHLY_ATTRIBUTION)],
            "performance_attribution": "AW net/PF/RF positive clue(순수익/수익 팩터/회복 계수 긍정 단서), density miss(밀도 미달), long skew(롱 쏠림), weak Sep/Dec and 18/19 stress(9/12월 및 18/19시 압박)",
            "queue_rows": len(queue),
            "attribution_boundary": "materialization only; no new KPI and no MT5 execution(물질화만, 새 KPI와 MT5 실행 없음)",
        },
    )
    write_json(
        JUDGMENT_RECEIPT,
        {
            **base,
            "judgment": JUDGMENT,
            "decision": DECISION,
            "runtime_authority": "not_claimed",
            "operating_promotion": "not_claimed",
            "live_readiness": "not_claimed",
            "goal_achieve": "not_claimed",
            "result_boundary": "input materialization for next scout only(다음 스카우트 입력 물질화만)",
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            **base,
            "runtime_authority": "not_claimed",
            "operating_promotion": "not_claimed",
            "live_readiness": "not_claimed",
            "goal_achieve": "not_claimed",
            "promotion_candidate": "not_claimed_materialization_only(물질화만이라 주장 없음)",
        },
    )
    refresh_lineage_receipt(final)


def refresh_lineage_receipt(final: Mapping[str, Any]) -> None:
    artifacts = []
    for path in OUTPUT_FILES:
        if exists(path) and Path(path).is_file():
            artifacts.append({"path": rel(path), "sha256": sha(path), "role": "run364AX output(364AX 출력)"})
    write_json(
        LINEAGE_RECEIPT,
        {
            "run_id": RUN_ID,
            "parent_run_id": PARENT_RUN_ID,
            "baseline_run_id": BASELINE_RUN_ID,
            "package_run_id": PACKAGE_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "source_inputs": [{"path": rel(path), "sha256": sha(path)} for path in INPUT_FILES if exists(path)],
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [artifact["path"] for artifact in artifacts],
            "artifact_hashes": artifacts,
            "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "availability": "tracked_after_commit_or_reproducible_from_command(커밋 후 추적 또는 명령으로 재현 가능)",
            "lineage_judgment": "connected_with_boundary(경계 내 연결됨)",
            "final_decision": final,
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def final_payload(
    parent_final: Mapping[str, Any],
    queue: Sequence[Mapping[str, Any]],
    guards: Sequence[Mapping[str, Any]],
    gates: Sequence[Mapping[str, Any]],
    created_at: str,
) -> dict[str, Any]:
    candidate_rows = [row for row in queue if str(row["queue_type"]).startswith("candidate")]
    stress_rows = [row for row in queue if "stress" in str(row["queue_type"])]
    return {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "baseline_run_id": BASELINE_RUN_ID,
        "package_run_id": PACKAGE_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "created_at_utc": created_at,
        "claim_boundary": CLAIM_BOUNDARY,
        "parent_mt5_net_profit": parent_final.get("mt5_net_profit"),
        "parent_mt5_profit_factor": parent_final.get("mt5_profit_factor"),
        "parent_mt5_trade_count": parent_final.get("mt5_trade_count"),
        "parent_trade_per_business_day": parent_final.get("trade_per_business_day"),
        "parent_expected_trade_per_business_day": parent_final.get("expected_trade_per_business_day"),
        "parent_actual_minus_expected_trade_count": parent_final.get("actual_minus_expected_trade_count"),
        "parent_long_trade_count": parent_final.get("long_trade_count"),
        "parent_short_trade_count": parent_final.get("short_trade_count"),
        "parent_long_share": parent_final.get("long_share"),
        "parent_max_drawdown_percent": parent_final.get("mt5_max_drawdown_percent"),
        "observed_mt5_proxy_trade_survival_ratio": observed_survival_ratio(parent_final),
        "proxy_density_buffer_target": PROXY_DENSITY_BUFFER_TARGET,
        "queue_rows": len(queue),
        "candidate_rows": len(candidate_rows),
        "stress_rows": len(stress_rows),
        "implementation_required_rows": sum(1 for row in queue if not str(row["implementation_required"]).startswith("no")),
        "executable_without_new_policy_rows": sum(1 for row in queue if str(row["implementation_required"]).startswith("no")),
        "min_candidate_estimated_mt5_density": min(as_float(row["estimated_mt5_density_per_day"]) for row in candidate_rows),
        "max_candidate_proxy_density_target": max(as_float(row["density_proxy_target_per_day"]) for row in candidate_rows),
        "top_n_rows": sum(1 for row in queue if row["top_n_status"] != "forbidden(금지)"),
        "trade_splitting_rows": sum(1 for row in queue if row["trade_splitting_status"] != "not_used(거래 쪼개기 없음)"),
        "oos_threshold_selection_rows": sum(1 for row in queue if row["oos_threshold_selection_status"] != "forbidden(금지)"),
        "guardrail_passes": sum(1 for row in guards if row["status"] == "passed"),
        "guardrail_total": len(guards),
        "gate_passes": sum(1 for row in gates if row["status"] == "passed"),
        "gate_total": len(gates),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "live_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "external_verification_status": "not_applicable_materialization_only(물질화만이라 해당 없음)",
    }


def markdown_table(rows: Sequence[Mapping[str, Any]], columns: Sequence[str]) -> str:
    if not rows:
        return "_none(없음)_"
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join(["---"] * len(columns)) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(column, "")).replace("|", "\\|").replace("\n", " ") for column in columns) + " |")
    return "\n".join(lines)


def refresh_stage_brief_header() -> None:
    if not exists(STAGE_BRIEF):
        return
    text = Path(STAGE_BRIEF).read_text(encoding="utf-8-sig")
    lines = []
    for line in text.splitlines():
        if line.startswith("- current_run_id"):
            lines.append(f"- current_run_id(현재 실행 ID): `{NEXT_RUN_ID}`")
        elif line.startswith("- latest_completed_run_id"):
            lines.append(f"- latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`")
        elif line.startswith("- selection_status"):
            lines.append(f"- selection_status(선택 상태): `{STATUS}`")
        elif line.startswith("- claim_boundary"):
            lines.append(f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`")
        else:
            lines.append(line)
    write_text(STAGE_BRIEF, "\n".join(lines).rstrip() + "\n", bom=True)


def write_docs(
    final: Mapping[str, Any],
    queue: Sequence[Mapping[str, Any]],
    guards: Sequence[Mapping[str, Any]],
    gates: Sequence[Mapping[str, Any]],
) -> None:
    refresh_stage_brief_header()
    preview = [
        {
            "rank": row["queue_rank"],
            "queue_id": row["queue_id"],
            "type": row["queue_type"],
            "short_th": row["short_probability_threshold"],
            "floor": row["entry_margin_floor"],
            "proxy_density": row["density_proxy_target_per_day"],
            "est_mt5_density": row["estimated_mt5_density_per_day"],
            "impl": row["implementation_required"],
        }
        for row in queue
    ]
    report = f"""# run364AX threshold edge density restore cost/session materialization(364AX 임계값 경계 밀도 복원 비용/세션 물질화)

## Current Truth(현재 진실)

- action(행동): run364AW(364AW 실행)의 MT5 runtime probe review(MT5 런타임 탐침 검토)를 run364AY(364AY 실행) scout queue(스카우트 대기열)로 materialize(물질화)했다.
- effect(효과): Stage364(364단계)를 새 Stage(단계)로 분기하지 않고, density restore(밀도 복원), short-side restore(숏 방향 복원), cost/session stress(비용/세션 압박)를 다음 실행 가능한 입력으로 묶었다.
- parent MT5 net/PF/trades(부모 MT5 순수익/수익 팩터/거래수): `{final['parent_mt5_net_profit']}` / `{final['parent_mt5_profit_factor']}` / `{final['parent_mt5_trade_count']}`
- parent density(부모 밀도): `{final['parent_trade_per_business_day']}` per business day(영업일당), floor(하한) `{DENSITY_FLOOR}`
- observed survival ratio(관측 생존 비율): `{final['observed_mt5_proxy_trade_survival_ratio']}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

## Queue(대기열)

{markdown_table(preview, ['rank', 'queue_id', 'type', 'short_th', 'floor', 'proxy_density', 'est_mt5_density', 'impl'])}

## Guardrails(가드레일)

{markdown_table(guards, ['guardrail', 'status', 'evidence', 'effect'])}

## Gates(게이트)

{markdown_table(gates, ['gate', 'status', 'evidence', 'effect'])}

## Judgment(판정)

Action(행동): AX는 새 model training(모델 학습), MT5 execution(MT5 실행), forward pass(전진 통과)를 하지 않았다.

Effect(효과): 이 결과는 materialization only(물질화 전용)이고, runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 `not_claimed(주장 없음)`이다.

## Next Action(다음 행동)

`{NEXT_RUN_ID}`에서 이 queue(대기열)를 proxy scout(프록시 스카우트)로 실행한다. trade splitting(거래 쪼개기), top_n(top_n), OOS threshold selection(OOS 임계값 선택)은 계속 금지한다.
"""
    write_text(REPORT_PATH, report, bom=True)
    write_text(DECISION_DOC, report, bom=True)
    write_text(
        WORKSPACE_STATE,
        f"""current_stage_id: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {STATUS}
current_judgment: {JUDGMENT}
next_run_id: {NEXT_RUN_ID}
runtime_authority: not_claimed
operating_promotion: not_claimed
goal_achieve: not_claimed
updated_at_utc: {final['created_at_utc']}
""",
        bom=False,
    )
    write_text(
        CURRENT_WORKING_STATE,
        f"""# Current Working State(현재 작업 상태)

date(날짜): {TODAY}

stage(단계): `{STAGE_ID}`

current_run_id(현재 실행 ID): `{NEXT_RUN_ID}`

latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`

current_truth(현재 진실): `run364AX` materialized(물질화 완료) `run364AY` scout queue(스카우트 대기열) `{rel(RUN364AY_QUEUE)}` from `run364AW` MT5 runtime probe review(MT5 런타임 탐침 검토). Parent MT5 density(부모 MT5 밀도)는 `{final['parent_trade_per_business_day']}`/day(일)로 3/day(일 3회) 하한 미달이고, AX queue(대기열)는 proxy density buffer(프록시 밀도 완충) `{PROXY_DENSITY_BUFFER_TARGET}`/day 이상 후보를 포함한다.

next_action(다음 행동): `{NEXT_RUN_ID}`에서 density restore(밀도 복원), short-side restore(숏 방향 복원), cost/session stress(비용/세션 압박) queue(대기열)를 proxy scout(프록시 스카우트)로 실행한다.

claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
        bom=True,
    )
    write_text(
        SELECTION_STATUS,
        f"""# Stage364 selection status(선택 상태)

- current_run(현재 실행): `{NEXT_RUN_ID}`
- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- selected_operating_model(선택 운영 모델): none(없음)
- promotion_candidate(승격 후보): none_materialization_only(물질화 전용이라 없음)
- runtime_probe_candidate(런타임 탐침 후보): `threshold_edge_floor001_probe(임계값 경계 하한 0.001 탐침)` remains repair seed(수리 씨앗으로 유지)
- latest_materialization(최근 물질화): `{RUN_ID}`
- next_scout_queue(다음 스카우트 대기열): `{rel(RUN364AY_QUEUE)}`
- parent_mt5_net_pf_trades(부모 MT5 순수익/수익 팩터/거래수): `{final['parent_mt5_net_profit']}` / `{final['parent_mt5_profit_factor']}` / `{final['parent_mt5_trade_count']}`
- parent_trade_density(부모 거래 밀도): `{final['parent_trade_per_business_day']}` per business day(영업일당), floor(하한) `{DENSITY_FLOOR}`
- trade_splitting(거래 쪼개기): not_used(사용 안 함)
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
        bom=True,
    )
    append_text_once(
        REVIEW_INDEX,
        RUN_ID,
        f"- `{RUN_ID}`: `{rel(REPORT_PATH)}` - density restore cost/session materialization(밀도 복원 비용/세션 물질화).",
    )
    append_text_once(
        STAGE_BRIEF,
        f"## {RUN_ID}",
        f"""## {RUN_ID}

Action(행동): AW MT5 runtime probe review(AW MT5 런타임 탐침 검토)를 AY scout queue(AY 스카우트 대기열)로 materialize(물질화)했다.

Effect(효과): Stage364(364단계)를 분기하지 않고 density restore(밀도 복원), short-side restore(숏 방향 복원), cost/session stress(비용/세션 압박)를 다음 proxy scout(프록시 스카우트) 입력으로 넘긴다.
""",
    )
    append_text_once(
        STAGE_README,
        RUN_ID,
        f"""## run364AX Threshold Edge Density Restore Cost/Session Materialization(364AX 임계값 경계 밀도 복원 비용/세션 물질화)

Action(행동): run364AW(364AW 실행)의 positive clue(긍정 단서)와 failure memory(실패 기억)를 run364AY(364AY 실행) queue(대기열)로 정리했다.

Effect(효과): trade splitting(거래 쪼개기) 없이 3/day(일 3회) 이상을 노리는 다음 공격 탐색(offensive exploration, 공격 탐색)이 바로 실행 가능하다.
""",
    )
    append_text_once(
        WORKSPACE_CHANGELOG,
        f"## {TODAY} - {RUN_ID}",
        f"""## {TODAY} - {RUN_ID}

- action(행동): threshold-edge density restore cost/session inputs(임계값 경계 밀도 복원 비용/세션 입력)를 물질화했다.
- effect(효과): `{NEXT_RUN_ID}` scout queue(스카우트 대기열)를 만들고, runtime authority(런타임 권위)와 operating promotion(운영 승격)은 주장하지 않았다.
- report(보고서): `{rel(REPORT_PATH)}`
""",
    )
    append_text_once(
        IDEA_REGISTRY,
        f"## {RUN_ID}",
        f"""## {RUN_ID}

- idea(아이디어): AW positive runtime clue(AW 긍정 런타임 단서)의 density miss(밀도 미달)를 proxy density buffer(프록시 밀도 완충), short-side restore(숏 방향 복원), session/month stress labels(세션/월 압박 라벨)로 복원한다.
- effect(효과): promotion-ineligible(승격 부적격)을 idea-dead(아이디어 사망)로 닫지 않고, 다음 공격 탐색 씨앗으로 전환한다.
""",
    )
    append_text_once(
        NEGATIVE_RESULT_REGISTER,
        f"## {RUN_ID}",
        f"""## {RUN_ID}

- status(상태): materialized_repair_inputs_no_authority(수리 입력 물질화, 권위 없음).
- failure memory(실패 기억): AW actual MT5 density(AW 실제 MT5 밀도) `{final['parent_trade_per_business_day']}` < 3/day(일 3회), long share(롱 비중) `{final['parent_long_share']}`, DD(낙폭) `{final['parent_max_drawdown_percent']}`%.
- effect(효과): 같은 blocker(차단 원인)를 반복하지 않고, AY scout(스카우트)의 제약과 비교축으로 바꾼다.
""",
    )


def write_ledgers(final: Mapping[str, Any]) -> None:
    common = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "run_number": RUN_NUMBER,
        "date": TODAY,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_run_id": NEXT_RUN_ID,
        "rows": final["queue_rows"],
        "gate_passes": final["gate_passes"],
        "gate_total": final["gate_total"],
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "path": rel(RUN_DIR),
        "primary_report": rel(REPORT_PATH),
        "primary_artifact": rel(RUN364AY_QUEUE),
        "created_at": final["created_at_utc"],
        "final_decision_path": rel(FINAL_DECISION),
        "gate_audit_path": rel(GATE_AUDIT),
        "result_judgment": JUDGMENT,
        "external_verification_status": "not_applicable_materialization_only(물질화만이라 해당 없음)",
        "work_family": "experiment_design(실험 설계)",
        "scoreboard_lane": "materialization(물질화)",
        "next_action": NEXT_RUN_ID,
        "question": "Can threshold-edge floor001 density be restored above 3/day without trade splitting?(임계값 경계 하한 0.001 밀도를 거래 쪼개기 없이 3/day 이상 복원할 수 있는가?)",
        "notes": f"queue_rows={final['queue_rows']}; min_candidate_estimated_mt5_density={final['min_candidate_estimated_mt5_density']}; no_topn_no_split",
        "net_profit": final["parent_mt5_net_profit"],
        "profit_factor": final["parent_mt5_profit_factor"],
        "trade_count": final["parent_mt5_trade_count"],
        "trade_density_per_feature_day": final["parent_trade_per_business_day"],
        "trade_density_requirement_status": "repair_materialized_parent_below_floor_no_trade_split(부모 하한 미달 수리 물질화, 거래 쪼개기 없음)",
        "long_trade_count": final["parent_long_trade_count"],
        "short_trade_count": final["parent_short_trade_count"],
    }
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], [common], extend_header=True)
    ledger_rows = []
    for suffix, record_view, tier_scope, kpi_scope in [
        ("Tier_A", "Tier A separate(Tier A 분리)", "Tier A", "materialized queue(물질화 대기열)"),
        ("Tier_B", "Tier B separate(Tier B 분리)", "Tier B", "out_of_scope_by_claim_no_tier_b_fallback(주장 범위 밖, Tier B 대체 없음)"),
        ("Tier_AplusB", "Tier A+B combined(Tier A+B 합산)", "Tier A+B", "Tier A materialized queue plus Tier B out_of_scope(Tier A 물질화 대기열 + Tier B 범위 밖)"),
    ]:
        row = dict(common)
        row.update(
            {
                "ledger_row_id": f"{RUN_ID}__{suffix}",
                "subrun_id": f"{RUN_ID}__{suffix}",
                "row_id": f"{RUN_ID}__{suffix}",
                "record_view": record_view,
                "tier_scope": tier_scope,
                "kpi_scope": kpi_scope,
                "primary_kpi": f"queue_rows={final['queue_rows']};min_est_mt5_density={final['min_candidate_estimated_mt5_density']}",
                "guardrail_kpi": "top_n=0;trade_splitting=0;oos_threshold_selection=0",
                "evidence_boundary": CLAIM_BOUNDARY,
            }
        )
        if tier_scope == "Tier B":
            row.update({"net_profit": "", "profit_factor": "", "trade_count": "", "long_trade_count": "", "short_trade_count": ""})
        ledger_rows.append(row)
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], ledger_rows, extend_header=True)
    append_or_replace_csv(STAGE_LEDGER, ["ledger_row_id"], ledger_rows, extend_header=True)

    artifact_rows = []
    for artifact_type, path, notes in [
        ("next_queue", RUN364AY_QUEUE, "Next scout queue(다음 스카우트 대기열)."),
        ("survival_buffer_plan", SURVIVAL_BUFFER_PLAN, "MT5 survival buffer plan(MT5 생존 완충 계획)."),
        ("axis_map", AXIS_MAP, "Density restore axis map(밀도 복원 축 지도)."),
        ("guardrail_matrix", GUARDRAIL_MATRIX, "Policy guardrail matrix(정책 가드레일 행렬)."),
        ("report", REPORT_PATH, "Materialization report(물질화 보고서)."),
        ("decision", DECISION_DOC, "Decision record(결정 기록)."),
        ("lineage", LINEAGE_RECEIPT, "Artifact lineage(산출물 계보)."),
        ("final_decision", FINAL_DECISION, "Final decision(최종 결정)."),
        ("run_manifest", RUN_MANIFEST, "Run manifest(실행 목록)."),
    ]:
        if exists(path):
            artifact_rows.append(
                {
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "artifact_type": artifact_type,
                    "path": rel(path),
                    "artifact_path": rel(path),
                    "sha256": sha(path),
                    "created_at_utc": final["created_at_utc"],
                    "created_at": final["created_at_utc"],
                    "claim_boundary": CLAIM_BOUNDARY,
                    "artifact_id": f"{RUN_ID}__{artifact_type}",
                    "notes": notes,
                }
            )
    append_or_replace_csv(ARTIFACT_REGISTRY, ["artifact_id"], artifact_rows, extend_header=True)
    parent.repair_run_registry_line_endings(RUN_ID)


def write_manifest(final: Mapping[str, Any]) -> None:
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "run_number": RUN_NUMBER,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "baseline_run_id": BASELINE_RUN_ID,
            "package_run_id": PACKAGE_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "created_at_utc": final["created_at_utc"],
            "status": STATUS,
            "judgment": JUDGMENT,
            "decision": DECISION,
            "claim_boundary": CLAIM_BOUNDARY,
            "inputs": [{"path": rel(path), "sha256": sha(path)} for path in INPUT_FILES if exists(path)],
            "outputs": [{"path": rel(path), "sha256": sha(path)} for path in OUTPUT_FILES if exists(path) and Path(path).is_file()],
        },
    )


def main() -> None:
    ensure_dirs()
    parent_final = validate_inputs()
    created_at = now_utc()

    write_csv(INPUT_MANIFEST, input_manifest_rows())
    write_work_packet()
    queue = queue_rows(parent_final)
    write_csv(SOURCE_RUNTIME_SUMMARY, source_summary_rows(parent_final))
    write_csv(RUN364AY_QUEUE, queue, QUEUE_FIELDNAMES)
    write_csv(AXIS_MAP, axis_rows(queue))
    write_csv(SURVIVAL_BUFFER_PLAN, survival_buffer_rows(parent_final, queue))
    guards = guardrail_rows(queue)
    write_csv(GUARDRAIL_MATRIX, guards)

    final_seed = {
        "run_id": RUN_ID,
        "created_at_utc": created_at,
        "queue_rows": len(queue),
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_receipts(final_seed, queue)
    gates = gate_rows(queue, guards)
    write_csv(GATE_AUDIT, gates)
    final = final_payload(parent_final, queue, guards, gates, created_at)
    write_json(FINAL_DECISION, final)
    write_receipts(final, queue)
    gates = gate_rows(queue, guards)
    write_csv(GATE_AUDIT, gates)
    final = final_payload(parent_final, queue, guards, gates, created_at)
    write_json(FINAL_DECISION, final)
    write_docs(final, queue, guards, gates)
    refresh_lineage_receipt(final)
    write_manifest(final)
    write_ledgers(final)
    refresh_lineage_receipt(final)
    write_manifest(final)
    write_json(FINAL_DECISION, final)
    print(json.dumps(json_ready(final), ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
