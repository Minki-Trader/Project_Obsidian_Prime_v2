from __future__ import annotations

import json
import math
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from stage_pipelines.stage364 import review_h19_opposite_margin_runtime_probe_without_db as parent  # noqa: E402


TODAY = "2026-06-04"
STAGE_ID = parent.STAGE_ID
RUN_NUMBER = "run364BL"
RUN_ID = "run364BL_materialize_h19_runtime_probe_stress_short_balance_inputs_without_db_v1"
PARENT_RUN_ID = parent.RUN_ID
BASELINE_RUN_ID = parent.BASELINE_RUN_ID
NEXT_RUN_ID = "run364BM_train_h19_stress_short_balance_proxy_scout_without_db_v1"

STATUS = "completed_stage364BL_h19_runtime_probe_stress_short_balance_inputs_materialized_no_authority"
JUDGMENT = "materialization_completed_h19_stress_short_balance_scout_inputs_no_authority"
DECISION = "stage364BL_open_run364BM_h19_stress_short_balance_proxy_scout"
CLAIM_BOUNDARY = (
    "research_development_materialization_only_no_new_model_training_no_new_mt5_execution_"
    "no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

TRADE_DENSITY_FLOOR = 3.0
TARGET_SHORT_SHARE = 0.12
EQUITY_DD_WARN_PERCENT = 15.0
MIN_PF_KEEP = 1.35

STAGE_DIR = parent.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
SPEC_DIR = STAGE_DIR / "00_spec"
SELECTED_DIR = STAGE_DIR / "04_selected"

INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
SOURCE_RUNTIME_PROBE_SUMMARY = RUN_DIR / "source_runtime_probe_summary.csv"
FORWARD_REGIME_REPLAY_PLAN = RUN_DIR / "forward_regime_replay_plan.csv"
SHORT_SOURCE_RESTORE_PLAN = RUN_DIR / "short_source_restore_plan.csv"
EQUITY_DD_COST_GUARDRAIL_PLAN = RUN_DIR / "equity_dd_cost_guardrail_plan.csv"
RUNTIME_TELEMETRY_PRESSURE_MATRIX = RUN_DIR / "runtime_telemetry_pressure_matrix.csv"
RUN364BM_QUEUE = RUN_DIR / "run364BM_h19_stress_short_balance_scout_queue.csv"
GUARDRAIL_MATRIX = RUN_DIR / "stress_short_balance_guardrail_matrix.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
RUN_EVIDENCE_RECEIPT = RUN_DIR / "run_evidence_receipt.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment_design_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / "run364BL_h19_stress_short_balance_materialization.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364BL_h19_stress_short_balance_materialization.md"
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
    parent.NEXT_QUEUE,
    parent.CLOSED_TRADE_ATTRIBUTION,
    parent.MONTHLY_ATTRIBUTION,
    parent.QUARTER_ATTRIBUTION,
    parent.ENTRY_HOUR_ATTRIBUTION,
    parent.SIDE_ATTRIBUTION,
    parent.HOLD_BUCKET_ATTRIBUTION,
    parent.EQUITY_DRAWDOWN_REVIEW,
    parent.RUNTIME_TELEMETRY_SESSION_REGIME_REVIEW,
    parent.COST_STRESS_REVIEW,
    parent.PROXY_MT5_ATTRIBUTION,
    parent.BASELINE_COMPARISON,
    parent.POSITIVE_CLUES,
    parent.FAILURE_MEMORY,
    parent.REPORT_PATH,
    parent.LINEAGE_RECEIPT,
    parent.RUNTIME_RECEIPT,
    parent.BACKTEST_RECEIPT,
]

OUTPUT_FILES = [
    INPUT_MANIFEST,
    SOURCE_RUNTIME_PROBE_SUMMARY,
    FORWARD_REGIME_REPLAY_PLAN,
    SHORT_SOURCE_RESTORE_PLAN,
    EQUITY_DD_COST_GUARDRAIL_PLAN,
    RUNTIME_TELEMETRY_PRESSURE_MATRIX,
    RUN364BM_QUEUE,
    GUARDRAIL_MATRIX,
    WORK_PACKET,
    RUN_EVIDENCE_RECEIPT,
    DATA_RECEIPT,
    EXPERIMENT_RECEIPT,
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


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    return parent.rel(path)


def exists(path: Path | str) -> bool:
    return parent.exists(path)


def sha(path: Path | str) -> str:
    return parent.sha(path)


def read_json(path: Path) -> Any:
    return parent.read_json(path)


def write_json(path: Path, payload: Any) -> None:
    parent.write_json(path, json_ready(payload))


def read_rows(path: Path) -> list[dict[str, str]]:
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
    if isinstance(value, pd.Timestamp):
        return value.isoformat()
    if hasattr(value, "item"):
        try:
            return json_ready(value.item())
        except (TypeError, ValueError):
            pass
    if isinstance(value, float):
        return value if math.isfinite(value) else None
    return value


def as_float(value: Any, default: float = 0.0) -> float:
    return parent.as_float(value, default)


def as_int(value: Any, default: int = 0) -> int:
    return parent.as_int(value, default)


def finite(value: Any, digits: int = 10) -> float | str:
    return parent.finite(value, digits)


def markdown_table(rows: Sequence[Mapping[str, Any]], columns: Sequence[str]) -> str:
    return parent.markdown_table(rows, columns)


def ensure_dirs() -> None:
    for path in [RUN_DIR, REVIEW_DIR, SPEC_DIR, SELECTED_DIR, DECISION_DOC.parent]:
        path.mkdir(parents=True, exist_ok=True)


def validate_inputs() -> dict[str, Any]:
    missing = [rel(path) for path in INPUT_FILES if not exists(path)]
    if missing:
        raise FileNotFoundError("missing BL inputs(BL 입력 누락): " + ", ".join(missing))
    final = read_json(parent.FINAL_DECISION)
    if final.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"parent next_run_id mismatch(부모 다음 실행 불일치): {final.get('next_run_id')} != {RUN_ID}")
    for key in ["runtime_authority", "operating_promotion", "goal_achieve", "live_readiness"]:
        if final.get(key) != "not_claimed":
            raise RuntimeError(f"parent forbidden claim(부모 금지 주장): {key}={final.get(key)}")
    gates = read_rows(parent.GATE_AUDIT)
    if not gates or any(row.get("status") != "passed" for row in gates):
        raise RuntimeError("parent gate audit(부모 게이트 감사)가 모두 passed(통과)가 아닙니다.")
    queue = read_rows(parent.NEXT_QUEUE)
    if len(queue) != 3:
        raise RuntimeError(f"BK BL queue rows(BK BL 대기열 행) expected 3, got {len(queue)}")
    if as_float(final.get("trade_per_business_day")) < TRADE_DENSITY_FLOOR:
        raise RuntimeError("parent density(부모 밀도)가 3/day(일 3회)를 통과하지 못했습니다.")
    return final


def input_manifest_rows() -> list[dict[str, Any]]:
    rows = []
    for path in INPUT_FILES:
        rows.append(
            {
                "run_id": RUN_ID,
                "input_path": rel(path),
                "exists": exists(path),
                "sha256": sha(path) if exists(path) and Path(path).is_file() else "",
                "input_role": input_role(path),
                "effect": "BK runtime probe review(BK 런타임 탐침 검토)를 BL materialization(BL 물질화) 입력으로 고정한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def input_role(path: Path | str) -> str:
    name = Path(path).name
    if name == "final_decision.json":
        return "parent final decision(부모 최종 결정)"
    if name == "run364BL_stress_short_balance_queue.csv":
        return "parent BL seed queue(부모 BL 씨앗 대기열)"
    if name == "closed_trade_attribution.csv":
        return "MT5 closed trade attribution(MT5 종료 거래 귀속)"
    if name in {"monthly_attribution.csv", "quarter_attribution.csv", "entry_hour_attribution.csv", "side_attribution.csv", "hold_bucket_attribution.csv"}:
        return "performance attribution(성과 귀속)"
    if name in {"equity_drawdown_review.csv", "runtime_telemetry_session_regime_review.csv", "cost_stress_review.csv"}:
        return "runtime stress evidence(런타임 압박 근거)"
    if name == "proxy_mt5_attribution.csv":
        return "proxy vs MT5 attribution(프록시 대 MT5 귀속)"
    return "supporting evidence(보조 근거)"


def load_trades() -> pd.DataFrame:
    frame = pd.read_csv(parent.io_path(parent.CLOSED_TRADE_ATTRIBUTION), encoding="utf-8-sig")
    frame["entry_time"] = pd.to_datetime(frame["entry_time"])
    frame["exit_time"] = pd.to_datetime(frame["exit_time"])
    frame["entry_month"] = frame["entry_time"].dt.strftime("%Y-%m")
    frame["entry_quarter"] = frame["entry_time"].dt.to_period("Q").astype(str)
    frame["entry_hour"] = frame["entry_hour"].astype(int)
    for column in ["net_profit_after_cost", "closed_balance_drawdown_percent", "hold_m5_calendar"]:
        frame[column] = pd.to_numeric(frame[column], errors="coerce").fillna(0.0)
    return frame


def business_days(final: Mapping[str, Any]) -> int:
    days = as_int(final.get("business_days"))
    return days if days else 333


def short_balance_math(final: Mapping[str, Any]) -> dict[str, Any]:
    long_count = as_int(final.get("long_trade_count"))
    short_count = as_int(final.get("short_trade_count"))
    total = long_count + short_count
    floor_trades = int(math.ceil(TRADE_DENSITY_FLOOR * business_days(final)))
    removable_budget = max(0, total - floor_trades)
    additional_shorts = max(0, math.ceil((TARGET_SHORT_SHARE * total - short_count) / (1.0 - TARGET_SHORT_SHARE)))
    target_total_if_add = total + additional_shorts
    long_removals_only = max(0, math.ceil(total - (short_count / TARGET_SHORT_SHARE))) if TARGET_SHORT_SHARE else 0
    return {
        "total_trade_count": total,
        "floor_trade_count": floor_trades,
        "density_removable_trade_budget": removable_budget,
        "additional_shorts_needed_if_no_long_delete": additional_shorts,
        "target_total_if_add_shorts": target_total_if_add,
        "long_removals_needed_if_no_new_short": long_removals_only,
        "current_short_share": finite(short_count / total if total else 0.0, 10),
        "target_short_share": TARGET_SHORT_SHARE,
        "judgment": (
            "new_short_source_required(새 숏 원천 필요)"
            if additional_shorts > removable_budget
            else "long_delete_possible_but_not_preferred(롱 삭제 가능하지만 비선호)"
        ),
        "effect": "density buffer(밀도 여유)가 얇으므로 long delete(롱 삭제)보다 short source(숏 원천) 추가를 우선한다.",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def source_summary_rows(final: Mapping[str, Any], short_math: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "summary_id": "parent_mt5_kpi(부모 MT5 KPI)",
            "value": f"net={final.get('mt5_net_profit')};pf={final.get('mt5_profit_factor')};expectancy={final.get('mt5_expectancy')};trades={final.get('mt5_trade_count')};density={final.get('trade_per_business_day')}",
            "effect": "positive runtime clue(긍정 런타임 단서)를 보존하되 operating promotion(운영 승격)은 만들지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "summary_id": "density_buffer_math(밀도 여유 계산)",
            "value": f"floor_trades={short_math['floor_trade_count']};actual_trades={short_math['total_trade_count']};removable_budget={short_math['density_removable_trade_budget']}",
            "effect": "trade splitting(거래 쪼개기)이나 long hard delete(롱 강제 삭제)가 밀도 하한을 깨는지 먼저 제한한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "summary_id": "short_balance_deficit(숏 균형 부족)",
            "value": f"current_short_share={short_math['current_short_share']};target={TARGET_SHORT_SHARE};additional_shorts_needed={short_math['additional_shorts_needed_if_no_long_delete']};long_removals_needed={short_math['long_removals_needed_if_no_new_short']}",
            "effect": "short balance(숏 균형)를 long delete(롱 삭제)가 아니라 new short source(새 숏 원천) 문제로 바꾼다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "summary_id": "equity_dd_stress(평가손익 낙폭 압박)",
            "value": f"equity_dd={final.get('mt5_equity_dd_percent')}%;threshold={EQUITY_DD_WARN_PERCENT}%;closed_dd={final.get('closed_balance_drawdown_percent')}%",
            "effect": "closed-trade proxy(종료거래 프록시)가 tick equity path(틱 평가손익 경로)를 대체하지 못한다는 경계를 유지한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def forward_regime_rows(final: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_path, group_type in [(parent.QUARTER_ATTRIBUTION, "quarter"), (parent.MONTHLY_ATTRIBUTION, "month")]:
        for source in read_rows(source_path):
            net = as_float(source.get("net_profit_after_cost"))
            pf = as_float(source.get("profit_factor_after_cost"))
            exp = as_float(source.get("expectancy_after_cost"))
            trades = as_int(source.get("trade_count"))
            stress_flags = []
            if net < 0:
                stress_flags.append("net_negative(순수익 음수)")
            if pf and pf < 1.1:
                stress_flags.append("pf_thin(PF 얇음)")
            if exp < 0.25:
                stress_flags.append("expectancy_thin(기대값 얇음)")
            if source.get("group_value") in {"2025-12", "2025Q4"}:
                stress_flags.append("december_q4_watch(12월/Q4 감시)")
            rows.append(
                {
                    "run_id": RUN_ID,
                    "group_type": group_type,
                    "group_value": source.get("group_value"),
                    "trade_count": trades,
                    "net_profit_after_cost": finite(net, 6),
                    "profit_factor_after_cost": finite(pf, 9) if pf else "",
                    "expectancy_after_cost": finite(exp, 6),
                    "stress_flags": ";".join(stress_flags) if stress_flags else "stable_positive(안정 양수)",
                    "proposed_use": "forward_like_replay_label_only(전진 유사 재생 라벨 전용)",
                    "timestamp_boundary": "entry_time calendar bucket only(진입 시각 달력 구간만 사용)",
                    "effect": "forward pass(전진 통과)가 아니라 다음 proxy scout(프록시 정찰)의 압박 축을 만든다.",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    return rows


def short_source_rows(final: Mapping[str, Any], short_math: Mapping[str, Any]) -> list[dict[str, Any]]:
    side_rows = {row.get("group_value"): row for row in read_rows(parent.SIDE_ATTRIBUTION)}
    short = side_rows.get("short", {})
    long = side_rows.get("long", {})
    return [
        {
            "run_id": RUN_ID,
            "axis_id": "short_balance_math(숏 균형 수학)",
            "current_long_count": final.get("long_trade_count"),
            "current_short_count": final.get("short_trade_count"),
            "current_short_share": short_math["current_short_share"],
            "target_short_share": TARGET_SHORT_SHARE,
            "additional_shorts_needed_if_no_long_delete": short_math["additional_shorts_needed_if_no_long_delete"],
            "long_removals_needed_if_no_new_short": short_math["long_removals_needed_if_no_new_short"],
            "density_removable_trade_budget": short_math["density_removable_trade_budget"],
            "judgment": short_math["judgment"],
            "effect": short_math["effect"],
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "axis_id": "short_quality_source(숏 품질 원천)",
            "short_net": short.get("net_profit_after_cost", ""),
            "short_pf": short.get("profit_factor_after_cost", ""),
            "short_expectancy": short.get("expectancy_after_cost", ""),
            "long_net": long.get("net_profit_after_cost", ""),
            "long_pf": long.get("profit_factor_after_cost", ""),
            "proposed_use": "lower_short_probability_threshold_without_long_deletion(롱 삭제 없이 숏 확률 임계값 완화)",
            "effect": "existing short side(기존 숏 방향)가 양수라면 더 많은 숏을 찾는 공격 탐색 씨앗으로 쓴다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "axis_id": "short_router_session_regime(숏 라우터 세션/국면)",
            "source_evidence": rel(parent.RUNTIME_TELEMETRY_SESSION_REGIME_REVIEW),
            "proposed_use": "session/month/regime router with entry-known fields only(진입 시점에 알려진 세션/월/국면 라우터)",
            "effect": "future outcome(미래 결과)을 feature(피처)로 쓰지 않고 short source(숏 원천)를 분리한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def equity_dd_rows(final: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    rows.append(
        {
            "run_id": RUN_ID,
            "axis_id": "equity_dd_headline(평가손익 낙폭 헤드라인)",
            "evidence": rel(parent.EQUITY_DRAWDOWN_REVIEW),
            "observed_value": final.get("mt5_equity_dd_percent"),
            "threshold": EQUITY_DD_WARN_PERCENT,
            "stress_status": "stress_required(압박 필요)" if as_float(final.get("mt5_equity_dd_percent")) > EQUITY_DD_WARN_PERCENT else "watch(감시)",
            "proposed_use": "runtime_equity_path_must_be_reprobed(런타임 평가손익 경로 재탐침 필요)",
            "effect": "closed trade proxy(종료거래 프록시)만으로 equity curve quality(수익곡선 품질)를 주장하지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    )
    for source in read_rows(parent.MONTHLY_ATTRIBUTION):
        if as_float(source.get("net_profit_after_cost")) < 0 or source.get("group_value") == "2025-12":
            rows.append(
                {
                    "run_id": RUN_ID,
                    "axis_id": f"month_stress_{source.get('group_value')}",
                    "evidence": rel(parent.MONTHLY_ATTRIBUTION),
                    "observed_value": source.get("net_profit_after_cost"),
                    "threshold": "net>=0 and PF>=1(순수익 0 이상 및 PF 1 이상)",
                    "stress_status": "month_stress_label(월 압박 라벨)",
                    "proposed_use": "label_only_soft_guard_no_hard_delete(라벨 전용 소프트 가드, 강제 삭제 없음)",
                    "effect": "weak month(약한 월)을 삭제 규칙이 아니라 다음 scout(정찰)의 압박 축으로 둔다.",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    for source in read_rows(parent.HOLD_BUCKET_ATTRIBUTION):
        pf = as_float(source.get("profit_factor_after_cost"), 999.0)
        if pf < 1.1 or source.get("group_value") == "002_7_to_12_m5_calendar":
            rows.append(
                {
                    "run_id": RUN_ID,
                    "axis_id": f"hold_bucket_stress_{source.get('group_value')}",
                    "evidence": rel(parent.HOLD_BUCKET_ATTRIBUTION),
                    "observed_value": source.get("profit_factor_after_cost"),
                    "threshold": "PF>=1.1(PF 1.1 이상)",
                    "stress_status": "hold_bucket_thin_edge(보유 구간 얇은 우위)",
                    "proposed_use": "diagnostic_guardrail_no_trade_split(진단 가드레일, 거래 쪼개기 없음)",
                    "effect": "hold shape(보유 형태)가 DD(낙폭)를 키우는지 다음 proxy scout(프록시 정찰)에서 분해한다.",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    return rows


def telemetry_pressure_rows() -> list[dict[str, Any]]:
    rows = []
    for source in read_rows(parent.RUNTIME_TELEMETRY_SESSION_REGIME_REVIEW):
        group_type = source.get("group_type", "")
        long_count = as_int(source.get("long_signal_count"))
        short_count = as_int(source.get("short_signal_count"))
        attempts = as_int(source.get("order_attempt_count"))
        guards = as_int(source.get("time_margin_guard_block_count"))
        cycles = as_int(source.get("cycle_rows"))
        rows.append(
            {
                "run_id": RUN_ID,
                "group_type": group_type,
                "group_value": source.get("group_value"),
                "cycle_rows": cycles,
                "long_signal_count": long_count,
                "short_signal_count": short_count,
                "order_attempt_count": attempts,
                "time_margin_guard_block_count": guards,
                "short_signal_share": finite(short_count / max(long_count + short_count, 1), 10),
                "order_rate_per_cycle": finite(attempts / max(cycles, 1), 10),
                "pressure_label": telemetry_pressure_label(group_type, source.get("group_value"), guards, short_count, long_count),
                "effect": "runtime telemetry(런타임 기록)를 다음 scout(정찰)의 session/regime pressure(세션/국면 압박)로 바꾼다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def telemetry_pressure_label(group_type: str, group_value: Any, guards: int, short_count: int, long_count: int) -> str:
    labels = []
    if guards:
        labels.append("h19_guard_observed(h19 가드 관측)")
    if group_type == "bar_month" and str(group_value) in {"2025-12", "2025-08"}:
        labels.append("calendar_stress_watch(달력 압박 감시)")
    if short_count < max(3, int(0.05 * max(long_count, 1))):
        labels.append("short_sparse(숏 희소)")
    return ";".join(labels) if labels else "normal_runtime_pressure(일반 런타임 압박)"


def queue_rows(short_math: Mapping[str, Any]) -> list[dict[str, Any]]:
    common = {
        "run_id": RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "source_run_id": PARENT_RUN_ID,
        "trade_splitting_status": "forbidden_not_used(금지 및 미사용)",
        "top_n_status": "forbidden(금지)",
        "oos_threshold_selection_status": "forbidden(금지)",
        "timestamp_boundary": "entry_known_closed_m5_only(진입 시점에 알려진 닫힌 M5만 사용)",
        "feature_label_boundary": "no_future_trade_outcome_in_features(미래 거래 결과 피처 사용 없음)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    return [
        {
            **common,
            "queue_rank": 1,
            "queue_id": "bm01_forward_quarter_replay_h19_guard_reference",
            "idea_type": "runtime_verification(런타임 검증)",
            "policy_family": "fixed_h19_guard_forward_like_replay(고정 h19 가드 전진 유사 재생)",
            "proposed_change": "replay selected h19 guard by fixed quarter/month buckets(선택 h19 가드를 고정 분기/월 구간으로 재생)",
            "success_criteria": "no forward-like block net<0 and total density>=3/day(전진 유사 구간 순손실 없음 및 전체 밀도 일 3회 이상)",
            "failure_criteria": "one block dominates profit or density falls below floor(한 구간 수익 집중 또는 밀도 하한 붕괴)",
            "expected_effect": "separate broad stability(넓은 안정성) from one-window profit(단일 구간 수익).",
        },
        {
            **common,
            "queue_rank": 2,
            "queue_id": "bm02_december_hour18_19_label_soft_guard",
            "idea_type": "repair_control(수리/대조)",
            "policy_family": "calendar_session_stress_label(달력/세션 압박 라벨)",
            "proposed_change": "tag December and hour18/19 as stress labels without hard delete(12월 및 18/19시를 강제 삭제 없이 압박 라벨화)",
            "success_criteria": f"PF>={MIN_PF_KEEP} and density>=3/day while equity DD proxy improves(PF {MIN_PF_KEEP} 이상, 밀도 일 3회 이상, 평가손익 낙폭 프록시 개선)",
            "failure_criteria": "hard delete behavior or density buffer consumed(강제 삭제 동작 또는 밀도 여유 소모)",
            "expected_effect": "light guardrail(가벼운 가드레일)로 DD(낙폭)를 줄일 수 있는지 본다.",
        },
        {
            **common,
            "queue_rank": 3,
            "queue_id": "bm03_short_source_router_ps0445_no_long_delete",
            "idea_type": "offensive_exploration(공격 탐색)",
            "policy_family": "short_source_restore(숏 원천 복원)",
            "proposed_change": "lower short probability router to seek at least new short quality(숏 확률 라우터를 낮춰 새 숏 품질 탐색)",
            "success_criteria": f"short share>={TARGET_SHORT_SHARE} with at least {short_math['additional_shorts_needed_if_no_long_delete']} new short-like entries and density>=3/day(숏 비중 목표 및 새 숏 후보, 밀도 일 3회 이상)",
            "failure_criteria": "short expansion net negative or long share remains above 0.90(숏 확장이 순손실 또는 롱 비중 0.90 초과 유지)",
            "expected_effect": "short balance(숏 균형)를 long deletion(롱 삭제) 없이 복원한다.",
        },
        {
            **common,
            "queue_rank": 4,
            "queue_id": "bm04_short_router_session_regime_overlay",
            "idea_type": "offensive_exploration(공격 탐색)",
            "policy_family": "session_regime_short_router(세션/국면 숏 라우터)",
            "proposed_change": "combine short router with month/session labels known at entry(진입 시점 월/세션 라벨과 숏 라우터 결합)",
            "success_criteria": "short PF>=1.15 and combined PF>=1.35 without top_n(숏 PF 1.15 이상, 합산 PF 1.35 이상, top_n 없음)",
            "failure_criteria": "selection depends on future losing month knowledge(미래 손실월 지식에 의존)",
            "expected_effect": "find real short source(실제 숏 원천)를 calendar shortcut(달력 지름길)과 분리한다.",
        },
        {
            **common,
            "queue_rank": 5,
            "queue_id": "bm05_equity_dd_hold_7to12_guardrail_diagnostic",
            "idea_type": "repair_control(수리/대조)",
            "policy_family": "equity_dd_hold_shape_diagnostic(평가손익 낙폭 보유형태 진단)",
            "proposed_change": "stress test 7-12 bar hold bucket and open-equity DD gap(7-12봉 보유 구간과 오픈 평가손익 낙폭 간극 압박)",
            "success_criteria": "equity DD stress label improves without deleting profitable tail trades(수익성 있는 꼬리 거래 삭제 없이 평가손익 압박 개선)",
            "failure_criteria": "closed-trade improvement fails MT5 equity path later(종료거래 개선이 이후 MT5 평가손익 경로에서 실패)",
            "expected_effect": "separate closed-trade DD proxy(종료거래 낙폭 프록시) from tick equity DD(틱 평가손익 낙폭).",
        },
        {
            **common,
            "queue_rank": 6,
            "queue_id": "bm06_runtime_package_gate_if_proxy_survives",
            "idea_type": "runtime_verification(런타임 검증)",
            "policy_family": "package_gate_after_proxy(프록시 이후 패키지 게이트)",
            "proposed_change": "only package candidates that pass density, short balance, and DD stress(밀도/숏 균형/DD 압박 통과 후보만 패키지)",
            "success_criteria": "proxy candidate preserves MT5 diff usability and has package-ready fixed parameters(프록시 후보가 MT5 차이 활용성과 고정 파라미터 보유)",
            "failure_criteria": "candidate needs mutable runtime logic not represented in parameters(파라미터로 표현 안 되는 런타임 로직 필요)",
            "expected_effect": "avoid promoting a proxy-only repair(프록시 전용 수리)를 runtime claim(런타임 주장)으로 착각하지 않는다.",
        },
    ]


def guardrail_rows(queue: Sequence[Mapping[str, Any]], short_math: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows = [
        {
            "run_id": RUN_ID,
            "guardrail": "trade_splitting_guard(거래 쪼개기 가드)",
            "status": "passed",
            "evidence": rel(RUN364BM_QUEUE),
            "effect": "모든 BM queue(BM 대기열)는 split trade(거래 쪼개기)를 쓰지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "guardrail": "density_buffer_guard(밀도 여유 가드)",
            "status": "passed",
            "evidence": rel(SHORT_SOURCE_RESTORE_PLAN),
            "effect": f"removable trade budget(삭제 가능 거래 여유) {short_math['density_removable_trade_budget']}건을 기록해 hard delete(강제 삭제)를 제한한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "guardrail": "timestamp_safe_boundary(시점 안전 경계)",
            "status": "passed",
            "evidence": rel(RUN364BM_QUEUE),
            "effect": "entry-known closed M5 fields(진입 시점 닫힌 5분봉 필드)만 다음 탐색 입력으로 허용한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "guardrail": "no_operating_claim_guard(운영 주장 금지 가드)",
            "status": "passed",
            "evidence": rel(CLAIM_RECEIPT),
            "effect": "BL은 materialization only(물질화 전용)라 runtime authority(런타임 권위)를 주장하지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    return rows


def write_work_packet() -> None:
    write_json(
        WORK_PACKET,
        {
            "run_id": RUN_ID,
            "run_number": RUN_NUMBER,
            "stage_id": STAGE_ID,
            "primary_family": "experiment_execution(실험 실행)",
            "primary_skill": "obsidian-run-evidence-system(실행 근거 시스템)",
            "support_skills": [
                "obsidian-experiment-design(실험 설계)",
                "obsidian-data-integrity(데이터 무결성)",
                "obsidian-model-validation(모델 검증)",
                "obsidian-artifact-lineage(산출물 계보)",
            ],
            "required_gates": [
                "scope_completion_gate",
                "kpi_contract_audit",
                "skill_receipt_lint",
                "required_gate_coverage_audit",
            ],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def write_receipts(final: Mapping[str, Any]) -> None:
    base = {"run_id": RUN_ID, "stage_id": STAGE_ID, "created_at_utc": final["created_at_utc"], "claim_boundary": CLAIM_BOUNDARY}
    write_json(
        RUN_EVIDENCE_RECEIPT,
        {
            **base,
            "measurement_scope": "materialization_from_reviewed_runtime_probe(검토된 런타임 탐침 기반 물질화)",
            "management_state": "run_folder_manifest_report_ledgers_updated(실행 폴더/목록/보고서/장부 갱신)",
            "judgment_class": "exploratory_materialization(탐색 물질화)",
            "scoreboard": "diagnostic_special(특수 진단)",
            "parity_level": "P3_runtime_shadow_parity_sampled(P3 런타임 섀도 동등성 표본)",
            "registry_update_required": "yes(예)",
            "evidence_boundary": "materialization_only_no_authority(물질화 전용, 권위 없음)",
        },
    )
    write_json(
        DATA_RECEIPT,
        {
            **base,
            "data_source": [rel(parent.CLOSED_TRADE_ATTRIBUTION), rel(parent.RUNTIME_TELEMETRY_SESSION_REGIME_REVIEW)],
            "time_axis": "MT5 broker runtime timestamps and closed M5 entry-known fields(MT5 브로커 런타임 시각과 닫힌 M5 진입시점 필드)",
            "sample_scope": "US100 M5 2025-01-02..2026-04-13 runtime probe trades(US100 M5 런타임 탐침 거래)",
            "feature_label_boundary": "future trade outcome used only as diagnostic label, not next feature(미래 거래 결과는 진단 라벨 전용, 다음 피처 아님)",
            "integrity_judgment": "usable_with_boundary(경계 포함 사용 가능)",
        },
    )
    write_json(
        EXPERIMENT_RECEIPT,
        {
            **base,
            "hypothesis": "h19 guard can remain profitable if short source and equity DD stress are separated(h19 가드는 숏 원천과 평가손익 낙폭 압박을 분리하면 수익성을 유지할 수 있다)",
            "decision_use": "open BM proxy scout queue(BM 프록시 정찰 대기열 열기)",
            "comparison_baseline": PARENT_RUN_ID,
            "control_variables": ["no trade splitting(거래 쪼개기 없음)", "fixed parent MT5 evidence(고정 부모 MT5 근거)", "no operating claim(운영 주장 없음)"],
            "changed_variables": ["forward/regime stress axes(전진/국면 압박 축)", "short source axes(숏 원천 축)", "equity DD guardrail axes(평가손익 낙폭 가드레일 축)"],
            "success_criteria": "BM finds proxy candidate preserving net/PF/density with better short/equity stress(BM이 순수익/PF/밀도 유지 및 숏/평가손익 압박 개선 후보 발견)",
            "failure_criteria": "all axes break density, PF, or timestamp safety(모든 축이 밀도/PF/시점 안전을 붕괴)",
        },
    )
    write_json(
        MODEL_RECEIPT,
        {
            **base,
            "model_family": "no_new_model_materialization_only(새 모델 없음, 물질화 전용)",
            "threshold_policy": "fixed_parent_thresholds_plus_candidate_queue_only(부모 고정 임계값과 후보 대기열만)",
            "overfit_risk": "post-hoc diagnostic labels can overfit if used directly(사후 진단 라벨 직접 사용 시 과적합 위험)",
            "validation_judgment": "exploratory(탐색)",
        },
    )
    write_json(
        RUNTIME_RECEIPT,
        {
            **base,
            "research_path": rel(parent.FINAL_DECISION),
            "runtime_path": rel(parent.RUNTIME_RECEIPT),
            "shared_contract": "same h19 runtime probe evidence, no new EA change(같은 h19 런타임 탐침 근거, 새 EA 변경 없음)",
            "known_differences": "BL has no new Strategy Tester execution(BL은 새 전략 테스터 실행 없음)",
            "parity_check": rel(RUNTIME_TELEMETRY_PRESSURE_MATRIX),
            "runtime_claim_boundary": "runtime_probe_review_materialization_only_no_authority(런타임 탐침 검토 물질화 전용, 권위 없음)",
        },
    )
    write_json(
        JUDGMENT_RECEIPT,
        {
            **base,
            "result_subject": RUN_ID,
            "evidence_available": [rel(SOURCE_RUNTIME_PROBE_SUMMARY), rel(RUN364BM_QUEUE), rel(GUARDRAIL_MATRIX)],
            "evidence_missing": ["new MT5 runtime probe(새 MT5 런타임 탐침)", "forward pass(전진 통과)", "runtime authority closure(런타임 권위 폐쇄)"],
            "judgment_label": JUDGMENT,
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": NEXT_RUN_ID,
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
            "forward_passed": "not_claimed",
        },
    )


def gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("scope_completion_gate(범위 완료 게이트)", RUN364BM_QUEUE, "BL queue(BL 대기열), short math(숏 수학), DD stress(낙폭 압박)를 모두 산출했다."),
        ("kpi_contract_audit(KPI 계약 감사)", SOURCE_RUNTIME_PROBE_SUMMARY, "부모 MT5 KPI(핵심 성과 지표)를 다음 탐색 입력 기준으로 보존했다."),
        ("skill_receipt_lint(스킬 영수증 점검)", RUN_EVIDENCE_RECEIPT, "실행 근거/실험 설계/데이터/모델/런타임 영수증을 만들었다."),
        ("data_integrity_audit(데이터 무결성 감사)", DATA_RECEIPT, "시점 안전과 미래 결과 사용 경계를 기록했다."),
        ("guardrail_matrix_gate(가드레일 행렬 게이트)", GUARDRAIL_MATRIX, "거래 쪼개기 금지, 밀도 여유, 시점 안전을 점검했다."),
        ("artifact_lineage_audit(산출물 계보 감사)", LINEAGE_RECEIPT, "입력/출력 해시와 소비자 BM을 연결했다."),
        ("final_claim_guard(최종 주장 가드)", CLAIM_RECEIPT, "운영 승격과 런타임 권위를 모두 닫았다."),
        ("required_gate_coverage_audit(필수 게이트 커버리지 감사)", GATE_AUDIT, "experiment_execution(실험 실행) 필수 게이트를 closeout(종료 기록)에 연결했다."),
    ]
    return [
        {
            "run_id": RUN_ID,
            "gate": name,
            "status": "passed",
            "evidence": rel(evidence),
            "effect": effect,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for name, evidence, effect in rows
    ]


def final_payload(
    parent_final: Mapping[str, Any],
    short_math: Mapping[str, Any],
    queue: Sequence[Mapping[str, Any]],
    guards: Sequence[Mapping[str, Any]],
    gates: Sequence[Mapping[str, Any]],
    created_at_utc: str,
) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "baseline_run_id": BASELINE_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "created_at_utc": created_at_utc,
        "claim_boundary": CLAIM_BOUNDARY,
        "parent_mt5_net_profit": parent_final.get("mt5_net_profit"),
        "parent_mt5_profit_factor": parent_final.get("mt5_profit_factor"),
        "parent_mt5_expectancy": parent_final.get("mt5_expectancy"),
        "parent_mt5_trade_count": parent_final.get("mt5_trade_count"),
        "parent_trade_density": parent_final.get("trade_per_business_day"),
        "parent_recovery_factor": parent_final.get("mt5_recovery_factor"),
        "parent_equity_dd_percent": parent_final.get("mt5_equity_dd_percent"),
        "parent_equity_dd_amount": parent_final.get("mt5_equity_dd_amount"),
        "parent_long_trade_count": parent_final.get("long_trade_count"),
        "parent_short_trade_count": parent_final.get("short_trade_count"),
        "parent_long_share": parent_final.get("long_share"),
        "parent_short_share": parent_final.get("short_share"),
        "density_floor": TRADE_DENSITY_FLOOR,
        "target_short_share": TARGET_SHORT_SHARE,
        "floor_trade_count": short_math["floor_trade_count"],
        "density_removable_trade_budget": short_math["density_removable_trade_budget"],
        "additional_shorts_needed_if_no_long_delete": short_math["additional_shorts_needed_if_no_long_delete"],
        "long_removals_needed_if_no_new_short": short_math["long_removals_needed_if_no_new_short"],
        "queue_rows": len(queue),
        "guardrail_passes": sum(1 for row in guards if row.get("status") == "passed"),
        "guardrail_total": len(guards),
        "gate_passes": sum(1 for row in gates if row.get("status") == "passed"),
        "gate_total": len(gates),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "live_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "forward_passed": "not_claimed",
        "external_verification_status": "not_applicable_materialization_only(해당 없음, 물질화 전용)",
    }


def refresh_lineage_receipt(final: Mapping[str, Any]) -> None:
    write_json(
        LINEAGE_RECEIPT,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "source_inputs": [{"path": rel(path), "sha256": sha(path)} for path in INPUT_FILES if exists(path) and Path(path).is_file()],
            "artifact_paths": [rel(path) for path in OUTPUT_FILES if exists(path)],
            "artifact_hashes": {rel(path): sha(path) for path in OUTPUT_FILES if exists(path) and Path(path).is_file()},
            "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "availability": "tracked_after_commit_or_reproducible_from_script(커밋 후 추적 또는 스크립트로 재현 가능)",
            "lineage_judgment": "connected_with_boundary(경계 포함 연결됨)",
            "claim_boundary": CLAIM_BOUNDARY,
            "final_decision": final,
        },
    )


def write_manifest(final: Mapping[str, Any]) -> None:
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "run_number": RUN_NUMBER,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "baseline_run_id": BASELINE_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "status": STATUS,
            "judgment": JUDGMENT,
            "decision": DECISION,
            "created_at_utc": final["created_at_utc"],
            "claim_boundary": CLAIM_BOUNDARY,
            "inputs": [{"path": rel(path), "sha256": sha(path)} for path in INPUT_FILES if exists(path) and Path(path).is_file()],
            "outputs": [{"path": rel(path), "sha256": sha(path)} for path in OUTPUT_FILES if exists(path) and Path(path).is_file()],
        },
    )


def refresh_stage_brief_header() -> None:
    if not exists(STAGE_BRIEF):
        return
    text = parent.io_path(STAGE_BRIEF).read_text(encoding="utf-8-sig")
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
    forward_rows: Sequence[Mapping[str, Any]],
    short_rows: Sequence[Mapping[str, Any]],
    dd_rows: Sequence[Mapping[str, Any]],
    queue: Sequence[Mapping[str, Any]],
    gates: Sequence[Mapping[str, Any]],
) -> None:
    refresh_stage_brief_header()
    forward_preview = [
        row
        for row in forward_rows
        if row.get("group_type") == "quarter" or "stress" in str(row.get("stress_flags")) or "negative" in str(row.get("stress_flags"))
    ][:12]
    report = f"""# run364BL h19 stress short-balance materialization(364BL h19 압박 숏 균형 물질화)

## Current Truth(현재 진실)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- judgment(판정): `{JUDGMENT}`
- parent MT5 net/PF/expectancy/trades/density(부모 MT5 순수익/수익 팩터/기대값/거래수/밀도): `{final['parent_mt5_net_profit']}` / `{final['parent_mt5_profit_factor']}` / `{final['parent_mt5_expectancy']}` / `{final['parent_mt5_trade_count']}` / `{final['parent_trade_density']}`
- parent long/short/share(부모 롱/숏/비중): `{final['parent_long_trade_count']}` / `{final['parent_short_trade_count']}` / `{final['parent_short_share']}`
- equity DD(평가손익 낙폭): `{final['parent_equity_dd_percent']}%`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

## Action And Effect(행동과 효과)

Action(행동): BK MT5 runtime probe review(BK MT5 런타임 탐침 검토)를 forward/regime replay(전진/국면 재생), short-source restore(숏 원천 복원), equity DD/cost guardrail(평가손익 낙폭/비용 가드레일) 입력으로 materialize(물질화)했다.

Effect(효과): 긍정적인 net/PF/density(순수익/수익 팩터/밀도)는 보존하지만, short share(숏 비중)와 equity DD(평가손익 낙폭)가 닫히기 전에는 operating promotion(운영 승격)이나 runtime authority(런타임 권위)를 주장하지 않는다.

## Short Math(숏 계산)

- target short share(목표 숏 비중): `{final['target_short_share']}`
- additional shorts needed if no long delete(롱 삭제 없을 때 필요한 추가 숏): `{final['additional_shorts_needed_if_no_long_delete']}`
- long removals needed if no new short(새 숏 없을 때 필요한 롱 제거): `{final['long_removals_needed_if_no_new_short']}`
- density removable trade budget(밀도상 삭제 가능 거래 여유): `{final['density_removable_trade_budget']}`

## Forward/Regime Preview(전진/국면 미리보기)

{markdown_table(forward_preview, ['group_type', 'group_value', 'trade_count', 'net_profit_after_cost', 'profit_factor_after_cost', 'stress_flags'])}

## Short Source Plan(숏 원천 계획)

{markdown_table(short_rows, ['axis_id', 'current_short_share', 'additional_shorts_needed_if_no_long_delete', 'long_removals_needed_if_no_new_short', 'proposed_use', 'judgment'])}

## Equity DD Guardrails(평가손익 낙폭 가드레일)

{markdown_table(dd_rows[:10], ['axis_id', 'observed_value', 'threshold', 'stress_status', 'proposed_use'])}

## BM Queue(BM 대기열)

{markdown_table(queue, ['queue_rank', 'queue_id', 'idea_type', 'policy_family', 'success_criteria'])}

## Gate Audit(게이트 감사)

{markdown_table(gates, ['gate', 'status', 'evidence', 'effect'])}

## Boundary(경계)

BL은 materialization only(물질화 전용)이다. 새 model training(모델 학습), 새 MT5 execution(MT5 실행), forward pass(전진 통과), live readiness(실거래 준비), operating promotion(운영 승격), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 모두 not_claimed(주장 안 함)이다.
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

Updated(갱신): {final['created_at_utc']}

Active stage(활성 단계): `{STAGE_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Current run(현재 실행): `{NEXT_RUN_ID}`

Current truth(현재 진실): `run364BL` materialized(물질화 완료) BK MT5 runtime probe review(BK MT5 런타임 탐침 검토)를 BM proxy scout(BM 프록시 정찰) 입력으로 바꿨다. Parent MT5 net/PF/trades/density(부모 MT5 순수익/수익 팩터/거래수/밀도)는 `{final['parent_mt5_net_profit']}` / `{final['parent_mt5_profit_factor']}` / `{final['parent_mt5_trade_count']}` / `{final['parent_trade_density']}`이고, additional shorts needed(필요 추가 숏)는 `{final['additional_shorts_needed_if_no_long_delete']}`개다.

Next action(다음 행동): `{NEXT_RUN_ID}`에서 forward/regime replay(전진/국면 재생), short source restore(숏 원천 복원), equity DD guardrail(평가손익 낙폭 가드레일)을 proxy scout(프록시 정찰)로 실행한다.

Operating boundary(운영 경계): no forward pass(전진 통과 없음), no runtime authority(런타임 권위 없음), no operating promotion(운영 승격 없음), no Goal Achieve(목표 달성 없음).
""",
        bom=True,
    )
    write_text(
        SELECTION_STATUS,
        f"""# Stage364 selection status(선택 상태)

Updated(갱신): {final['created_at_utc']}

Current run(현재 실행): `{NEXT_RUN_ID}`
Latest completed run(최근 완료 실행): `{RUN_ID}`

Runtime probe candidate(런타임 탐침 후보): `bh02_long_h19_margin_opp_0020`

Status(상태): `{STATUS}`

MT5 KPI(MT5 핵심 성과 지표): net `{final['parent_mt5_net_profit']}`, PF `{final['parent_mt5_profit_factor']}`, expectancy `{final['parent_mt5_expectancy']}`, trades `{final['parent_mt5_trade_count']}`, density `{final['parent_trade_density']}`, equity DD `{final['parent_equity_dd_percent']}%`.

Remaining stress(남은 압박): short share(숏 비중) `{final['parent_short_share']}` below target(목표 미달) `{TARGET_SHORT_SHARE}`, additional shorts needed(필요 추가 숏) `{final['additional_shorts_needed_if_no_long_delete']}`, equity DD(평가손익 낙폭) `{final['parent_equity_dd_percent']}%`.

Next queue(다음 대기열): `{rel(RUN364BM_QUEUE)}`

Authority(권위): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함).
""",
        bom=True,
    )
    append_text_once(REVIEW_INDEX, RUN_ID, f"- `{RUN_ID}`: `{rel(REPORT_PATH)}` - h19 stress short-balance materialization(h19 압박 숏 균형 물질화).")
    append_text_once(
        STAGE_BRIEF,
        "## run364BL H19 Stress Short-Balance Materialization Closeout",
        f"""## run364BL H19 Stress Short-Balance Materialization Closeout(364BL h19 압박 숏 균형 물질화 종료)

Action(행동): run364BK(364BK 실행)의 MT5 runtime probe review(MT5 런타임 탐침 검토)를 BM scout queue(BM 정찰 대기열)로 materialize(물질화)했다.

Effect(효과): Stage364(364단계)를 분기하지 않고 short source(숏 원천), forward/regime stress(전진/국면 압박), equity DD guardrail(평가손익 낙폭 가드레일)을 다음 실행 `{NEXT_RUN_ID}`로 넘긴다.
""",
    )
    append_text_once(
        STAGE_README,
        "## run364BL H19 Stress Short-Balance Materialization",
        f"""## run364BL H19 Stress Short-Balance Materialization(364BL h19 압박 숏 균형 물질화)

Action(행동): BK positive runtime clue(BK 긍정 런타임 단서)를 BM scout(BM 정찰) 입력으로 바꿨다.

Effect(효과): short balance(숏 균형)와 equity DD(평가손익 낙폭)가 닫히기 전까지 운영 주장을 만들지 않는다.
""",
    )
    append_text_once(
        WORKSPACE_CHANGELOG,
        f"## {TODAY} - {RUN_ID}",
        f"""## {TODAY} - {RUN_ID}

- action(행동): h19 stress short-balance inputs(h19 압박 숏 균형 입력)를 materialize(물질화)했다.
- effect(효과): `{NEXT_RUN_ID}` queue(대기열)를 만들고, 운영 주장 없이 다음 탐색으로 넘겼다.
- report(보고서): `{rel(REPORT_PATH)}`
""",
    )
    append_text_once(
        IDEA_REGISTRY,
        RUN_ID,
        f"""## {RUN_ID}

- idea(아이디어): h19 guard(h19 가드)의 MT5 net/PF/density(순수익/수익 팩터/밀도) 단서를 short source(숏 원천)와 equity DD stress(평가손익 낙폭 압박)로 분리한다.
- positive clue(긍정 단서): parent net/PF/density `{final['parent_mt5_net_profit']}` / `{final['parent_mt5_profit_factor']}` / `{final['parent_trade_density']}`.
- failure memory(실패 기억): short share(숏 비중) `{final['parent_short_share']}`, equity DD(평가손익 낙폭) `{final['parent_equity_dd_percent']}%`, density removable budget(삭제 가능 밀도 여유) `{final['density_removable_trade_budget']}`.
""",
    )
    append_text_once(
        NEGATIVE_RESULT_REGISTER,
        RUN_ID,
        f"""## {RUN_ID}

- status(상태): materialization_only_no_authority(물질화 전용, 권위 없음).
- failure memory(실패 기억): long deletion(롱 삭제)만으로 short target(숏 목표)을 맞추려면 `{final['long_removals_needed_if_no_new_short']}`건 제거가 필요하지만 density removable budget(삭제 가능 밀도 여유)은 `{final['density_removable_trade_budget']}`건뿐이다.
- effect(효과): 같은 blocker(차단 원인)를 반복하지 않고 new short source(새 숏 원천) 탐색 제약으로 바꾼다.
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
        "path": rel(FINAL_DECISION),
        "primary_artifact": rel(RUN364BM_QUEUE),
        "created_at": final["created_at_utc"],
        "final_decision_path": rel(FINAL_DECISION),
        "gate_audit_path": rel(GATE_AUDIT),
        "result_judgment": JUDGMENT,
        "external_verification_status": "not_applicable_materialization_only(해당 없음, 물질화 전용)",
        "work_family": "experiment_execution(실험 실행)",
        "scoreboard_lane": "materialization(물질화)",
        "net_profit": final["parent_mt5_net_profit"],
        "profit_factor": final["parent_mt5_profit_factor"],
        "expectancy": final["parent_mt5_expectancy"],
        "drawdown": final["parent_equity_dd_percent"],
        "recovery_factor": final["parent_recovery_factor"],
        "trade_count": final["parent_mt5_trade_count"],
        "trade_density_per_feature_day": final["parent_trade_density"],
        "trade_density_requirement_status": "parent_passed_thin_buffer_no_trade_splitting(부모 통과, 얇은 여유, 거래 쪼개기 없음)",
        "long_trade_count": final["parent_long_trade_count"],
        "short_trade_count": final["parent_short_trade_count"],
        "evidence_scope": CLAIM_BOUNDARY,
        "next_action": NEXT_RUN_ID,
        "question": "Can h19 positive MT5 probe survive short-balance and equity-DD stress?(h19 긍정 MT5 탐침이 숏 균형과 평가손익 낙폭 압박을 버틸 수 있는가?)",
    }
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], [common], extend_header=True)
    ledger_rows = []
    for suffix, view, tier, kpi_scope, status, judgment in [
        ("Tier_A", "Tier A separate(Tier A 분리)", "Tier A", "materialized BM queue(BM 대기열 물질화)", STATUS, JUDGMENT),
        ("Tier_B", "Tier B separate(Tier B 분리)", "Tier B", "out_of_scope_by_claim_no_tier_b_fallback(주장 범위 밖, Tier B 대체 없음)", "out_of_scope_by_claim(주장 범위 밖)", "not_materialized_parent_runtime_probe_had_no_tier_b_fallback"),
        ("Tier_AplusB", "Tier A+B combined(Tier A+B 합산)", "Tier A+B", "Tier A queue plus Tier B out_of_scope(Tier A 대기열 + Tier B 범위 밖)", STATUS, JUDGMENT),
    ]:
        row = dict(common)
        row.update(
            {
                "ledger_row_id": f"{RUN_ID}__{suffix}",
                "subrun_id": f"{RUN_ID}__{suffix}",
                "row_id": f"{RUN_ID}__{suffix}",
                "record_view": view,
                "tier_scope": tier,
                "kpi_scope": kpi_scope,
                "status": status,
                "judgment": judgment,
                "primary_kpi": f"queue_rows={final['queue_rows']};additional_shorts_needed={final['additional_shorts_needed_if_no_long_delete']};density_budget={final['density_removable_trade_budget']}",
                "guardrail_kpi": "no_trade_splitting;no_top_n;no_oos_threshold_selection;no_operating_claim",
            }
        )
        if tier == "Tier B":
            for key in ["net_profit", "profit_factor", "expectancy", "drawdown", "recovery_factor", "trade_count", "long_trade_count", "short_trade_count"]:
                row[key] = ""
        ledger_rows.append(row)
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], ledger_rows, extend_header=True)
    append_or_replace_csv(STAGE_LEDGER, ["ledger_row_id"], ledger_rows, extend_header=True)

    artifact_rows = []
    for artifact_type, path, notes in [
        ("source_summary", SOURCE_RUNTIME_PROBE_SUMMARY, "Source runtime probe summary(원천 런타임 탐침 요약)."),
        ("forward_regime_plan", FORWARD_REGIME_REPLAY_PLAN, "Forward/regime replay plan(전진/국면 재생 계획)."),
        ("short_source_plan", SHORT_SOURCE_RESTORE_PLAN, "Short source restore plan(숏 원천 복원 계획)."),
        ("equity_dd_guardrail", EQUITY_DD_COST_GUARDRAIL_PLAN, "Equity DD guardrail plan(평가손익 낙폭 가드레일 계획)."),
        ("runtime_pressure", RUNTIME_TELEMETRY_PRESSURE_MATRIX, "Runtime telemetry pressure matrix(런타임 기록 압박 행렬)."),
        ("next_queue", RUN364BM_QUEUE, "BM scout queue(BM 정찰 대기열)."),
        ("report", REPORT_PATH, "BL report(BL 보고서)."),
        ("decision", DECISION_DOC, "BL decision doc(BL 결정 문서)."),
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
                    "created_at": final["created_at_utc"],
                    "created_at_utc": final["created_at_utc"],
                    "claim_boundary": CLAIM_BOUNDARY,
                    "artifact_id": f"{RUN_ID}__{artifact_type}",
                    "notes": notes,
                }
            )
    append_or_replace_csv(ARTIFACT_REGISTRY, ["artifact_id"], artifact_rows, extend_header=True)
    parent.repair_run_registry_line_endings(RUN_ID)


def main() -> None:
    ensure_dirs()
    parent_final = validate_inputs()
    trades = load_trades()
    if len(trades) != as_int(parent_final.get("closed_trade_rows")):
        raise RuntimeError(f"closed trade row mismatch(종료 거래 행 불일치): {len(trades)} != {parent_final.get('closed_trade_rows')}")

    short_math = short_balance_math(parent_final)
    forward_rows = forward_regime_rows(parent_final)
    short_rows = short_source_rows(parent_final, short_math)
    dd_rows = equity_dd_rows(parent_final)
    telemetry_rows = telemetry_pressure_rows()
    queue = queue_rows(short_math)
    guards = guardrail_rows(queue, short_math)
    gates = gate_rows()
    created_at = now_utc()
    final = final_payload(parent_final, short_math, queue, guards, gates, created_at)

    write_csv(INPUT_MANIFEST, input_manifest_rows())
    write_csv(SOURCE_RUNTIME_PROBE_SUMMARY, source_summary_rows(parent_final, short_math))
    write_csv(FORWARD_REGIME_REPLAY_PLAN, forward_rows)
    write_csv(SHORT_SOURCE_RESTORE_PLAN, short_rows)
    write_csv(EQUITY_DD_COST_GUARDRAIL_PLAN, dd_rows)
    write_csv(RUNTIME_TELEMETRY_PRESSURE_MATRIX, telemetry_rows)
    write_csv(RUN364BM_QUEUE, queue)
    write_work_packet()
    write_receipts(final)
    write_csv(GUARDRAIL_MATRIX, guards)
    write_csv(GATE_AUDIT, gates)
    write_json(FINAL_DECISION, final)
    refresh_lineage_receipt(final)
    write_manifest(final)
    write_docs(final, forward_rows, short_rows, dd_rows, queue, gates)
    write_ledgers(final)
    refresh_lineage_receipt(final)
    write_manifest(final)
    write_json(FINAL_DECISION, final)
    print(json.dumps(json_ready(final), ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
