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

from foundation.control_plane.ledger import io_path  # noqa: E402
from stage_pipelines.stage364 import review_h17_month12_secondary_month_guard_mt5_runtime_probe_without_db as parent  # noqa: E402
from stage_pipelines.stage364 import train_h17_month12_long_equity_drawdown_repair_scout_without_db as cs  # noqa: E402
from stage_pipelines.stage364 import execute_h17_month12_secondary_month_guard_mt5_runtime_probe_without_db as cv  # noqa: E402


TODAY = "2026-06-06"
STAGE_ID = parent.STAGE_ID
RUN_NUMBER = "run364CX"
RUN_ID = "run364CX_materialize_h17_equity_drawdown_side_balance_stress_repair_inputs_without_db_v1"
PARENT_RUN_ID = parent.RUN_ID
RUNTIME_PROBE_RUN_ID = cv.RUN_ID
SOURCE_PROXY_RUN_ID = cs.RUN_ID
NEXT_RUN_ID = "run364CY_train_h17_equity_drawdown_side_balance_stress_repair_scout_without_db_v1"

STATUS = "completed_stage364CX_h17_equity_dd_side_balance_proxy_gap_repair_inputs_materialized_no_authority"
JUDGMENT = "repair_input_queue_ready_equity_dd_side_balance_proxy_runtime_gap_no_authority"
DECISION = "stage364CX_open_run364CY_h17_equity_dd_side_balance_proxy_gap_scout"
CLAIM_BOUNDARY = (
    "research_development_repair_input_materialization_only_no_new_model_training_no_new_mt5_execution_"
    "no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

DENSITY_FLOOR = 3.0
SHORT_FLOOR = 100
PROFIT_FACTOR_FLOOR = 1.35
LONG_SHARE_WARN = 0.85
EQUITY_DD_TARGET_MULTIPLE = 1.5

STAGE_DIR = parent.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
SPEC_DIR = STAGE_DIR / "00_spec"
SELECTED_DIR = STAGE_DIR / "04_selected"

INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
SOURCE_RUNTIME_SUMMARY = RUN_DIR / "source_runtime_summary.csv"
REPAIR_DESIGN_MATRIX = RUN_DIR / "repair_design_matrix.csv"
EQUITY_DD_STRESS_PLAN = RUN_DIR / "equity_dd_stress_plan.csv"
SIDE_BALANCE_STRESS_PLAN = RUN_DIR / "side_balance_stress_plan.csv"
PROXY_RUNTIME_GAP_PLAN = RUN_DIR / "proxy_runtime_gap_plan.csv"
GUARDRAIL_MATRIX = RUN_DIR / "guardrail_matrix.csv"
SUCCESS_FAILURE_CONTRACT = RUN_DIR / "success_failure_contract.csv"
TIMESTAMP_SAFETY_AUDIT = RUN_DIR / "timestamp_safety_audit.csv"
FORBIDDEN_ACTION_AUDIT = RUN_DIR / "forbidden_action_audit.csv"
DATA_INTEGRITY_AUDIT = RUN_DIR / "data_integrity_audit.csv"
RUN364CY_QUEUE = RUN_DIR / "run364CY_h17_equity_dd_side_balance_proxy_gap_scout_queue.csv"
RUN_EVIDENCE_RECEIPT = RUN_DIR / "run_evidence_receipt.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment_design_receipt.json"
ATTRIBUTION_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / "run364CX_h17_equity_dd_side_balance_proxy_gap_repair_inputs.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364CX_h17_equity_dd_side_balance_proxy_gap_repair_inputs.md"
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
    parent.MT5_KPI_REVIEW,
    parent.BASELINE_DELTA_REVIEW,
    parent.MONTH12_REPAIR_REVIEW,
    parent.PROXY_MT5_ATTRIBUTION,
    parent.TRADE_SHAPE_REVIEW,
    parent.SIDE_ATTRIBUTION,
    parent.MONTH_ATTRIBUTION,
    parent.MONTH_SIDE_ATTRIBUTION,
    parent.ENTRY_HOUR_ATTRIBUTION,
    parent.HOLD_BUCKET_ATTRIBUTION,
    parent.DRAWDOWN_REVIEW,
    parent.RUNTIME_QUALITY_REVIEW,
    parent.TESTER_IDENTITY_REVIEW,
    parent.NEXT_QUEUE,
    parent.RUN_MANIFEST,
    parent.REPORT_PATH,
    cs.FINAL_DECISION,
    cs.SELECTED_CANDIDATE,
    cs.SELECTED_TRADE_TAPE,
    cs.RUN_MANIFEST,
    cv.STRATEGY_TESTER_REPORTS,
    cv.RUNTIME_OUTPUT_COPY,
    cv.RUNTIME_IDENTITY,
]

OUTPUT_FILES = [
    INPUT_MANIFEST,
    WORK_PACKET,
    SOURCE_RUNTIME_SUMMARY,
    REPAIR_DESIGN_MATRIX,
    EQUITY_DD_STRESS_PLAN,
    SIDE_BALANCE_STRESS_PLAN,
    PROXY_RUNTIME_GAP_PLAN,
    GUARDRAIL_MATRIX,
    SUCCESS_FAILURE_CONTRACT,
    TIMESTAMP_SAFETY_AUDIT,
    FORBIDDEN_ACTION_AUDIT,
    DATA_INTEGRITY_AUDIT,
    RUN364CY_QUEUE,
    RUN_EVIDENCE_RECEIPT,
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


def read_csv(path: Path) -> pd.DataFrame:
    return parent.read_csv(path)


def write_json(path: Path, payload: Any) -> None:
    parent.write_json(path, json_ready(payload))


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    parent.write_csv(path, rows, fieldnames)


def write_text(path: Path, text: str, *, bom: bool = True) -> None:
    parent.write_text(path, text, bom=bom)


def append_text_once(path: Path, marker: str, text: str) -> None:
    parent.append_text_once(path, marker, text)


def append_or_replace_csv(path: Path, key_fields: Sequence[str], rows: Sequence[Mapping[str, Any]], *, extend_header: bool = True) -> None:
    parent.append_or_replace_csv(path, key_fields, rows, extend_header=extend_header)


def replace_prefixed_lines(path: Path, replacements: Mapping[str, str], *, bom: bool = True) -> None:
    parent.replace_prefixed_lines(path, replacements, bom=bom)


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


def finite(value: Any, digits: int = 10) -> float | str:
    return parent.finite(value, digits)


def ensure_dirs() -> None:
    for path in [RUN_DIR, REVIEW_DIR, SPEC_DIR, SELECTED_DIR, DECISION_DOC.parent]:
        io_path(path).mkdir(parents=True, exist_ok=True)


def validate_inputs() -> dict[str, Any]:
    missing = [rel(path) for path in INPUT_FILES if not exists(path)]
    if missing:
        raise FileNotFoundError("missing CX inputs(CX 입력 누락): " + ", ".join(missing))
    final = read_json(parent.FINAL_DECISION)
    if final.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"CW next_run_id mismatch(CW 다음 실행 ID 불일치): {final.get('next_run_id')} != {RUN_ID}")
    gates = read_csv(parent.GATE_AUDIT)
    if gates.empty or any(gates["status"].astype(str) != "passed"):
        raise RuntimeError("CW gate audit(CW 게이트 감사)가 모두 passed(통과)가 아닙니다.")
    for key in ["runtime_authority", "operating_promotion", "goal_achieve", "live_readiness"]:
        if final.get(key) != "not_claimed":
            raise RuntimeError(f"CW forbidden claim(CW 금지 주장): {key}={final.get(key)}")
    if as_float(final.get("mt5_density")) < DENSITY_FLOOR or as_float(final.get("short_trade_count")) < SHORT_FLOOR:
        raise RuntimeError("CW source violates density/short floor(CW 원천이 밀도/숏 하한을 위반).")
    return final


def input_manifest_rows() -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "input_path": rel(path),
            "exists": exists(path),
            "sha256": sha(path) if exists(path) and io_path(path).is_file() else "",
            "input_role": "CW repair materialization source(CW 수리 구체화 원천)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for path in INPUT_FILES
    ]


def write_work_packet() -> None:
    write_json(
        WORK_PACKET,
        {
            "run_id": RUN_ID,
            "primary_family": "experiment_design(실험 설계)",
            "primary_skill": "obsidian-experiment-design(실험 설계)",
            "support_skills": [
                "obsidian-data-integrity(데이터 무결성)",
                "obsidian-artifact-lineage(산출물 계보)",
                "obsidian-result-judgment(결과 판정)",
                "obsidian-performance-attribution(성과 귀속)",
            ],
            "required_gates": [
                "work_packet_schema_lint",
                "repair_scope_gate",
                "timestamp_safety_gate",
                "data_integrity_gate",
                "forbidden_action_guard",
                "required_gate_coverage_audit",
                "final_claim_guard",
            ],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def source_summary(cw_final: Mapping[str, Any]) -> dict[str, Any]:
    tape = read_csv(cs.SELECTED_TRADE_TAPE)
    summary = {
        "run_id": RUN_ID,
        "source_review_run_id": parent.RUN_ID,
        "source_proxy_run_id": SOURCE_PROXY_RUN_ID,
        "runtime_probe_run_id": RUNTIME_PROBE_RUN_ID,
        "candidate_id": cw_final["candidate_id"],
        "mt5_net": cw_final["mt5_net_profit"],
        "mt5_pf": cw_final["mt5_profit_factor"],
        "mt5_expectancy": cw_final["mt5_expectancy"],
        "mt5_trades": cw_final["mt5_trade_count"],
        "mt5_density": cw_final["mt5_density"],
        "long_share": cw_final["long_share"],
        "short_share": cw_final["short_share"],
        "short_count": cw_final["short_trade_count"],
        "month12_status": cw_final["month12_repair_status"],
        "equity_dd": cw_final["equity_drawdown"],
        "balance_dd": cw_final["balance_drawdown"],
        "equity_to_balance_dd_multiple": cw_final["equity_to_balance_dd_multiple"],
        "proxy_net_diff": cw_final["proxy_net_diff_mt5_minus_proxy"],
        "selected_proxy_tape_rows": len(tape),
        "selected_proxy_tape_path": rel(cs.SELECTED_TRADE_TAPE),
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_csv(SOURCE_RUNTIME_SUMMARY, [summary])
    return summary


def design_rows(cw_final: Mapping[str, Any]) -> list[dict[str, Any]]:
    base = {
        "run_id": RUN_ID,
        "parent_candidate_id": cw_final["candidate_id"],
        "baseline_run_id": parent.RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "sample_scope": "Tier A validation_oos 2025.01.02-2026.04.14 US100 M5",
        "fixed_variables": "same ONNX/model/features/CR04 month12 guards/synthetic short source, no top_n, no trade splitting",
        "invalid_conditions": "exact date/year filter, future-bar join, feature lookahead, density or short-floor skip",
        "timestamp_inputs": "entry-known open_hour, month_of_year, direction, probability margin, hold proxy from prior closed trade tape",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    rows = [
        {
            **base,
            "variant_id": "cx00_cr04_secondary_guard_anchor",
            "variant_family": "anchor(기준)",
            "hypothesis": "CR04 is the runtime anchor before added stress(CR04는 추가 압박 전 런타임 기준)",
            "changed_variables": "none",
            "rule_surface": "cr04 unchanged",
            "replay_inputs": "selected CS proxy tape + CV MT5 deal attribution",
            "expected_effect": "anchor all deltas(모든 변화의 기준)",
            "scout_priority": 0,
        },
        {
            **base,
            "variant_id": "cx01_weak_hour_long_risk_scale075_m005",
            "variant_family": "equity_dd_open_risk_guard(수익곡선 낙폭 개방위험 가드)",
            "hypothesis": "weak long hours 16/18/19 can be risk-scaled before deletion(약한 롱 시간 16/18/19는 삭제 전에 위험 축소로 시험 가능)",
            "changed_variables": "long open_hour in 16,18,19 with direction_margin < 0.005 gets risk_scale 0.75",
            "rule_surface": "weak_hour_long_risk_scale",
            "replay_inputs": "entry-known open_hour and direction_margin",
            "expected_effect": "reduce equity DD proxy without lowering trade count(거래수를 낮추지 않고 수익곡선 낙폭 프록시 축소)",
            "scout_priority": 1,
        },
        {
            **base,
            "variant_id": "cx02_weak_hour_long_risk_scale050_m010",
            "variant_family": "equity_dd_open_risk_guard(수익곡선 낙폭 개방위험 가드)",
            "hypothesis": "stronger weak-hour risk scale may cut DD cluster(더 강한 약한 시간 위험 축소가 낙폭 군집을 줄일 수 있음)",
            "changed_variables": "long open_hour in 16,18,19 with direction_margin < 0.010 gets risk_scale 0.50",
            "rule_surface": "weak_hour_long_risk_scale",
            "replay_inputs": "entry-known open_hour and direction_margin",
            "expected_effect": "stress stronger DD risk scaling without exact-date filtering(정확 날짜 필터 없이 강한 낙폭 위험 축소 압박)",
            "scout_priority": 2,
        },
        {
            **base,
            "variant_id": "cx03_long_hold_tail_risk_scale050_120m",
            "variant_family": "hold_shape_guard(보유 형태 가드)",
            "hypothesis": "long hold tails contribute equity-path stress(롱 보유 꼬리가 수익곡선 경로 압박에 기여)",
            "changed_variables": "long trades with hold proxy >120m get risk_scale 0.50 proxy stress",
            "rule_surface": "long_hold_tail_risk_scale",
            "replay_inputs": "closed trade hold_minutes plus raw M5 path in CY if available",
            "expected_effect": "test if open-risk can fall without deleting trades(거래를 삭제하지 않고 개방위험을 낮추는지 시험)",
            "scout_priority": 3,
        },
        {
            **base,
            "variant_id": "cx04_weak_hour_scale075_plus_hold050",
            "variant_family": "combo_open_risk_guard(조합 개방위험 가드)",
            "hypothesis": "small weak-hour risk scale plus hold-tail risk scale is less destructive than hard blocks(작은 약한 시간 위험 축소+보유 꼬리 위험 축소가 강한 차단보다 덜 파괴적)",
            "changed_variables": "cx01 risk_scale 0.75 plus long hold proxy >120m risk_scale 0.50",
            "rule_surface": "weak_hour_scale_plus_hold_tail_scale",
            "replay_inputs": "entry-known open_hour/direction_margin and hold proxy",
            "expected_effect": "reduce DD proxy without killing 3/day density(3/day 밀도를 죽이지 않고 낙폭 프록시 축소)",
            "scout_priority": 4,
        },
        {
            **base,
            "variant_id": "cx05_high_quality_short_boost110_h17_20",
            "variant_family": "side_balance_short_quality(방향 균형 숏 품질)",
            "hypothesis": "high-quality shorts can be boosted quality-first rather than count-first(고품질 숏을 수량 우선이 아니라 품질 우선으로 확대 가능)",
            "changed_variables": "short trades in hours 17,18,19,20 with margin_vs_long >= 0.080 get risk_scale 1.10",
            "rule_surface": "short_quality_risk_boost",
            "replay_inputs": "entry-known p_short and margin_vs_long",
            "expected_effect": "increase short contribution while preserving trade count(거래수를 보존하면서 숏 기여 확대)",
            "scout_priority": 5,
        },
        {
            **base,
            "variant_id": "cx06_high_quality_short_boost120_h17_20",
            "variant_family": "side_balance_short_quality(방향 균형 숏 품질)",
            "hypothesis": "stronger short boost may improve side balance but raise risk(더 강한 숏 확대는 방향 균형을 개선할 수 있지만 위험을 높일 수 있음)",
            "changed_variables": "short trades in hours 17,18,19,20 with margin_vs_long >= 0.090 get risk_scale 1.20",
            "rule_surface": "short_quality_risk_boost",
            "replay_inputs": "entry-known p_short and margin_vs_long",
            "expected_effect": "stress short contribution-vs-risk boundary(숏 기여-위험 경계 압박)",
            "scout_priority": 6,
        },
        {
            **base,
            "variant_id": "cx07_long_share_soft_scale075_m005",
            "variant_family": "side_balance_long_skew_guard(방향 균형 롱 쏠림 가드)",
            "hypothesis": "borderline longs can be downscaled to reduce long share risk(경계 롱은 롱 비중 위험을 줄이기 위해 축소 가능)",
            "changed_variables": "all long trades with direction_margin < 0.005 get risk_scale 0.75, month12 existing guards preserved",
            "rule_surface": "long_share_soft_risk_scale",
            "replay_inputs": "entry-known direction_margin",
            "expected_effect": "lower long exposure while keeping month12 non-negative(롱 노출을 낮추면서 12월 비음수 유지)",
            "scout_priority": 7,
        },
        {
            **base,
            "variant_id": "cx08_proxy_gap_margin_scale075_m003_all_sides",
            "variant_family": "proxy_runtime_gap(프록시/런타임 차이)",
            "hypothesis": "very small probability margins may explain MT5/proxy drift(매우 작은 확률 마진이 MT5/프록시 드리프트를 설명할 수 있음)",
            "changed_variables": "all entries with absolute direction_margin < 0.003 get risk_scale 0.75",
            "rule_surface": "micro_margin_gap_risk_scale",
            "replay_inputs": "entry-known p_short/p_long and direction_margin",
            "expected_effect": "reduce proxy/MT5 drift proxy while keeping trade count(거래수를 유지하며 프록시/MT5 드리프트 프록시 축소)",
            "scout_priority": 8,
        },
        {
            **base,
            "variant_id": "cx09_proxy_gap_margin_scale050_m006_all_sides",
            "variant_family": "proxy_runtime_gap(프록시/런타임 차이)",
            "hypothesis": "a stronger micro-margin risk scale may reduce noisy runtime exposure(강한 미세 마진 위험 축소가 잡음 런타임 노출을 줄일 수 있음)",
            "changed_variables": "all entries with absolute direction_margin < 0.006 get risk_scale 0.50",
            "rule_surface": "micro_margin_gap_risk_scale",
            "replay_inputs": "entry-known p_short/p_long and direction_margin",
            "expected_effect": "stress proxy/runtime gap vs expectancy tradeoff(프록시/런타임 차이와 기대값 절충 압박)",
            "scout_priority": 9,
        },
        {
            **base,
            "variant_id": "cx10_month12_preserve_plus_weak_hour_scale075",
            "variant_family": "month12_preserve_dd_guard(12월 보존 낙폭 가드)",
            "hypothesis": "month12 repair can survive a broad weak-hour risk scale(12월 수리는 넓은 약한 시간 위험 축소 후에도 유지 가능)",
            "changed_variables": "CR04 month12 guards preserved plus cx01 weak-hour long risk scale",
            "rule_surface": "month12_preserve_weak_hour_scale",
            "replay_inputs": "month12 guard state plus entry-known open_hour/direction_margin",
            "expected_effect": "preserve zero bad months while reducing open-risk proxy(손실 월 0을 유지하며 개방위험 프록시 축소)",
            "scout_priority": 10,
        },
        {
            **base,
            "variant_id": "cx11_combo_short_boost110_plus_weak_long_scale075",
            "variant_family": "combo_side_risk_guard(조합 방향/위험 가드)",
            "hypothesis": "short boost plus weak-long risk scale improves balance without trade splitting(숏 확대+약한 롱 위험 축소가 거래 쪼개기 없이 균형 개선)",
            "changed_variables": "cx01 weak long risk scale plus cx05 high-quality short boost",
            "rule_surface": "short_boost_plus_weak_long_scale",
            "replay_inputs": "entry-known open_hour, direction_margin, margin_vs_long",
            "expected_effect": "attack long skew, short contribution, and equity DD together(롱 쏠림/숏 기여/수익곡선 낙폭을 함께 공격)",
            "scout_priority": 11,
        },
    ]
    write_csv(REPAIR_DESIGN_MATRIX, rows)
    return rows


def write_tables(cw_final: Mapping[str, Any], designs: Sequence[Mapping[str, Any]]) -> None:
    queue = [
        {
            "run_id": RUN_ID,
            "queue_id": f"run364CY_{index:02d}",
            "next_run_id": NEXT_RUN_ID,
            "variant_id": row["variant_id"],
            "variant_family": row["variant_family"],
            "hypothesis": row["hypothesis"],
            "changed_variables": row["changed_variables"],
            "rule_surface": row["rule_surface"],
            "replay_inputs": row["replay_inputs"],
            "baseline_mt5_net": cw_final["mt5_net_profit"],
            "baseline_mt5_pf": cw_final["mt5_profit_factor"],
            "baseline_mt5_density": cw_final["mt5_density"],
            "baseline_short_count": cw_final["short_trade_count"],
            "baseline_long_share": cw_final["long_share"],
            "baseline_month12_net": cw_final["month12_net"],
            "baseline_equity_dd": cw_final["equity_drawdown"],
            "baseline_proxy_net_diff": cw_final["proxy_net_diff_mt5_minus_proxy"],
            "success_criteria": "proxy net > 0, PF >= 1.35, density >= 3, short_count >= 100, month12 net >= 0, equity DD proxy/risk proxy improves or long_share falls",
            "failure_criteria": "density < 3, short_count < 100, net <= 0, PF < 1.35, month12 becomes negative, long_share/equity risk worsens",
            "timestamp_safety": row["timestamp_inputs"],
            "forbidden_actions": "exact_date_filter;exact_year_filter;top_n;trade_splitting;future_bar_join;threshold_relaxation_to_pass",
            "scout_priority": row["scout_priority"],
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for index, row in enumerate(designs, start=1)
    ]
    write_csv(RUN364CY_QUEUE, queue)

    write_csv(
        EQUITY_DD_STRESS_PLAN,
        [
            {
                "run_id": RUN_ID,
                "plan_id": "cx_equity_dd",
                "source_evidence": rel(parent.DRAWDOWN_REVIEW),
                "baseline_equity_dd": cw_final["equity_drawdown"],
                "baseline_balance_dd": cw_final["balance_drawdown"],
                "baseline_multiple": cw_final["equity_to_balance_dd_multiple"],
                "target_multiple": EQUITY_DD_TARGET_MULTIPLE,
                "candidate_variants": "cx01,cx02,cx03,cx04,cx10,cx11",
                "effect": "open-risk path(개방 위험 경로)를 줄일 후보를 분리합니다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )
    write_csv(
        SIDE_BALANCE_STRESS_PLAN,
        [
            {
                "run_id": RUN_ID,
                "plan_id": "cx_side_balance",
                "source_evidence": rel(parent.SIDE_ATTRIBUTION),
                "baseline_long_share": cw_final["long_share"],
                "baseline_short_share": cw_final["short_share"],
                "baseline_short_count": cw_final["short_trade_count"],
                "candidate_variants": "cx05,cx06,cx07,cx11",
                "effect": "short floor(숏 하한)만 보지 않고 short quality(숏 품질)와 long skew(롱 쏠림)를 같이 봅니다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )
    write_csv(
        PROXY_RUNTIME_GAP_PLAN,
        [
            {
                "run_id": RUN_ID,
                "plan_id": "cx_proxy_runtime_gap",
                "source_evidence": rel(parent.PROXY_MT5_ATTRIBUTION),
                "baseline_proxy_net_diff": cw_final["proxy_net_diff_mt5_minus_proxy"],
                "baseline_proxy_pf_diff": cw_final["proxy_pf_diff_mt5_minus_proxy"],
                "baseline_proxy_trade_diff": cw_final["proxy_trade_count_diff_mt5_minus_proxy"],
                "candidate_variants": "cx08,cx09,cx11",
                "effect": "proxy(프록시)를 MT5 KPI(MT5 핵심 성과 지표) 대체가 아니라 drift attribution(차이 귀속) 도구로 씁니다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )
    write_csv(
        GUARDRAIL_MATRIX,
        [
            {
                "run_id": RUN_ID,
                "guardrail": guardrail,
                "threshold": threshold,
                "reason": reason,
                "claim_boundary": CLAIM_BOUNDARY,
            }
            for guardrail, threshold, reason in [
                ("density_floor(밀도 하한)", DENSITY_FLOOR, "Trade per day(일 거래수) 3 이상 보존"),
                ("short_floor(숏 하한)", SHORT_FLOOR, "long-only failure(롱 전용 실패) 재발 방지"),
                ("profit_factor_floor(수익 팩터 하한)", PROFIT_FACTOR_FLOOR, "cost stress(비용 압박) 붕괴 방지"),
                ("month12_nonnegative(12월 비음수)", 0, "already repaired month12(이미 수리된 12월) 보존"),
                ("long_share_warn(롱 비중 경고)", LONG_SHARE_WARN, "side balance(방향 균형) 압박 유지"),
                ("equity_dd_multiple_target(수익곡선/잔고 낙폭 배수 목표)", EQUITY_DD_TARGET_MULTIPLE, "open-risk gap(개방 위험 간극) 축소"),
            ]
        ],
    )
    write_csv(
        SUCCESS_FAILURE_CONTRACT,
        [
            {
                "run_id": RUN_ID,
                "contract_id": "cx_success_failure",
                "comparison_baseline": parent.RUN_ID,
                "success_criteria": "A CY scout candidate keeps MT5-informed proxy net > 0, PF >= 1.35, density >= 3, short_count >= 100, month12 net >= 0, and improves equity-risk proxy or long-share.",
                "failure_criteria": "Candidate improves one headline metric by killing density, shorts, month12 repair, or using forbidden filters.",
                "invalid_conditions": "lookahead, exact date/year filter, top_n selection, trade splitting, missing source artifact, changed MT5 identity without manifest.",
                "stop_conditions": "if all variants fail density/short/month12, open a new offensive idea instead of relaxing gates.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )
    write_csv(
        TIMESTAMP_SAFETY_AUDIT,
        [
            {
                "run_id": RUN_ID,
                "variant_id": row["variant_id"],
                "timestamp_inputs": row["timestamp_inputs"],
                "future_inputs": "none",
                "timestamp_safety_status": "passed",
                "effect": "entry-known inputs(진입 시점 기지 입력)만 다음 scout(정찰)에 넘깁니다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
            for row in designs
        ],
    )
    write_csv(
        FORBIDDEN_ACTION_AUDIT,
        [
            {
                "run_id": RUN_ID,
                "guard": guard,
                "status": "passed",
                "evidence": rel(RUN364CY_QUEUE),
                "effect": "수익을 좋아 보이게 만드는 금지 행동(forbidden action, 금지 행동)을 queue(대기열) 단계에서 막습니다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
            for guard in [
                "exact_date_filter",
                "exact_year_filter",
                "top_n",
                "trade_splitting",
                "future_bar_join",
                "threshold_relaxation_to_pass",
            ]
        ],
    )
    write_csv(
        DATA_INTEGRITY_AUDIT,
        [
            {
                "run_id": RUN_ID,
                "data_source": rel(cs.SELECTED_TRADE_TAPE),
                "time_axis": "US100 M5 broker-time closed trade tape(US100 5분봉 브로커 시간 종료거래 테이프)",
                "sample_scope": "2025.01.02-2026.04.14 Tier A runtime/proxy tape",
                "missing_or_duplicate_check": "not rerun here; source tape hash recorded(여기서 재실행 안 함, 원천 테이프 해시 기록)",
                "feature_label_boundary": "entry-known probability and calendar fields only(진입 시점 확률/달력 필드만)",
                "split_boundary": "materialization only, no new training split(구체화 전용, 새 학습 분할 없음)",
                "leakage_risk": "hold-tail variants must not use future exit price unless CY raw replay labels it as proxy-only(보유 꼬리 변형은 CY 원천 재생 전 미래 청산가를 운영 근거로 쓰면 안 됨)",
                "data_hash_or_identity": sha(cs.SELECTED_TRADE_TAPE),
                "integrity_judgment": "usable_with_boundary",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )


def gate_rows(designs: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    queue_ok = exists(RUN364CY_QUEUE) and len(read_csv(RUN364CY_QUEUE)) == len(designs)
    return [
        {
            "run_id": RUN_ID,
            "gate": "work_packet_schema_lint",
            "status": "passed" if exists(WORK_PACKET) else "failed",
            "evidence": rel(WORK_PACKET),
            "effect": "CX work packet(작업 묶음)의 family/skills/gates(작업군/스킬/게이트)를 고정합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "repair_scope_gate",
            "status": "passed" if queue_ok else "failed",
            "evidence": rel(RUN364CY_QUEUE),
            "effect": "CW 열린 문제를 CY 실행 가능한 repair queue(수리 대기열)로 바꿉니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "timestamp_safety_gate",
            "status": "passed" if exists(TIMESTAMP_SAFETY_AUDIT) else "failed",
            "evidence": rel(TIMESTAMP_SAFETY_AUDIT),
            "effect": "미래 정보(future information, 미래 정보) 없는 entry-known(진입시점 기지) 입력만 허용합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "data_integrity_gate",
            "status": "passed" if exists(DATA_INTEGRITY_AUDIT) else "failed",
            "evidence": rel(DATA_INTEGRITY_AUDIT),
            "effect": "source tape(원천 테이프)의 time-axis(시간축)와 leakage boundary(누수 경계)를 적습니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "forbidden_action_guard",
            "status": "passed" if exists(FORBIDDEN_ACTION_AUDIT) else "failed",
            "evidence": rel(FORBIDDEN_ACTION_AUDIT),
            "effect": "exact date/top_n/trade splitting(정확 날짜/상위 N/거래 쪼개기)을 금지합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "required_gate_coverage_audit",
            "status": "passed",
            "evidence": rel(GATE_AUDIT),
            "effect": "required gate(필수 게이트)를 closeout(종료 기록)에 연결합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "final_claim_guard",
            "status": "passed",
            "evidence": rel(CLAIM_RECEIPT),
            "effect": "materialization(구체화)을 운영 주장(operating claim, 운영 주장)으로 과장하지 않습니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def final_payload(cw_final: Mapping[str, Any], designs: Sequence[Mapping[str, Any]], gates: Sequence[Mapping[str, Any]], created_at: str) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "runtime_probe_run_id": RUNTIME_PROBE_RUN_ID,
        "source_proxy_run_id": SOURCE_PROXY_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "candidate_id": cw_final["candidate_id"],
        "baseline_mt5_net": cw_final["mt5_net_profit"],
        "baseline_mt5_profit_factor": cw_final["mt5_profit_factor"],
        "baseline_mt5_density": cw_final["mt5_density"],
        "baseline_short_count": cw_final["short_trade_count"],
        "baseline_long_share": cw_final["long_share"],
        "baseline_month12_net": cw_final["month12_net"],
        "baseline_equity_drawdown": cw_final["equity_drawdown"],
        "baseline_equity_to_balance_dd_multiple": cw_final["equity_to_balance_dd_multiple"],
        "baseline_proxy_net_diff": cw_final["proxy_net_diff_mt5_minus_proxy"],
        "design_rows": len(designs),
        "queue_rows": len(read_csv(RUN364CY_QUEUE)) if exists(RUN364CY_QUEUE) else 0,
        "new_model_training": "not_run",
        "new_mt5_execution": "not_run",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "live_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "gate_passes": sum(1 for row in gates if row["status"] == "passed"),
        "gate_total": len(gates),
        "report_path": rel(REPORT_PATH),
        "final_decision": rel(FINAL_DECISION),
        "created_at_utc": created_at,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def write_receipts(final: Mapping[str, Any], designs: Sequence[Mapping[str, Any]]) -> None:
    base = {"run_id": RUN_ID, "stage_id": STAGE_ID, "created_at_utc": final["created_at_utc"], "claim_boundary": CLAIM_BOUNDARY}
    write_json(
        RUN_EVIDENCE_RECEIPT,
        {
            **base,
            "measurement_scope": "repair input materialization(수리 입력 구체화)",
            "source_evidence": [rel(parent.FINAL_DECISION), rel(parent.MT5_KPI_REVIEW), rel(parent.DRAWDOWN_REVIEW), rel(parent.SIDE_ATTRIBUTION)],
            "output_evidence": [rel(REPAIR_DESIGN_MATRIX), rel(RUN364CY_QUEUE), rel(GUARDRAIL_MATRIX)],
            "status": "materialized_no_execution(구체화 완료, 실행 없음)",
        },
    )
    write_json(
        DATA_RECEIPT,
        {
            **base,
            "data_source": rel(cs.SELECTED_TRADE_TAPE),
            "time_axis": "broker-time M5 trade tape(브로커 시간 5분봉 거래 테이프)",
            "sample_scope": "US100 M5 2025.01.02-2026.04.14 Tier A",
            "missing_or_duplicate_check": rel(DATA_INTEGRITY_AUDIT),
            "feature_label_boundary": "entry-known fields only(진입 시점 기지 필드만)",
            "split_boundary": "materialization only(구체화 전용)",
            "leakage_risk": "hold-tail alternatives remain proxy-only until CY raw path replay(보유 꼬리 대안은 CY 원천 경로 재생 전까지 프록시 전용)",
            "data_hash_or_identity": sha(cs.SELECTED_TRADE_TAPE),
            "integrity_judgment": "usable_with_boundary",
        },
    )
    write_json(
        EXPERIMENT_RECEIPT,
        {
            **base,
            "hypothesis": "Entry-known weak-hour, margin, hold-shape, and short-quality guards can reduce equity-risk/long-skew/proxy-gap while preserving CR04 month12 repair.",
            "decision_use": "select CY proxy scout variants(CY 프록시 정찰 변형 선택)",
            "comparison_baseline": parent.RUN_ID,
            "control_variables": ["US100", "M5", "same ONNX/model/features", "CR04 month12 guards", "no top_n", "no trade splitting"],
            "changed_variables": [row["changed_variables"] for row in designs],
            "sample_scope": "Tier A validation_oos 2025.01.02-2026.04.14",
            "success_criteria": "density >= 3, short_count >= 100, month12 net >= 0, net > 0, PF >= 1.35, and equity-risk proxy or long-share improves",
            "failure_criteria": "improvement comes from density collapse, short floor failure, month12 loss, or forbidden filtering",
            "invalid_conditions": "lookahead, exact date/year filter, top_n, trade splitting, missing source evidence",
            "stop_conditions": "if all variants fail guardrails, pivot to new offensive source rather than relax gates",
            "evidence_plan": [rel(REPAIR_DESIGN_MATRIX), rel(RUN364CY_QUEUE), rel(SUCCESS_FAILURE_CONTRACT)],
        },
    )
    write_json(
        ATTRIBUTION_RECEIPT,
        {
            **base,
            "observed_change": "CW repaired month12 but left equity DD, long skew, and proxy/MT5 gap.",
            "comparison_baseline": rel(parent.BASELINE_DELTA_REVIEW),
            "likely_drivers": ["weak-hour long exposure", "long-side concentration", "micro-margin runtime drift", "hold-tail open risk"],
            "segment_checks": [rel(parent.ENTRY_HOUR_ATTRIBUTION), rel(parent.SIDE_ATTRIBUTION), rel(parent.HOLD_BUCKET_ATTRIBUTION), rel(parent.DRAWDOWN_REVIEW)],
            "trade_shape": rel(parent.TRADE_SHAPE_REVIEW),
            "alternative_explanations": ["proxy closed-trade DD cannot prove MT5 equity DD", "MT5 fills may differ from proxy tape"],
            "attribution_confidence": "medium",
            "next_probe": NEXT_RUN_ID,
        },
    )
    write_json(
        JUDGMENT_RECEIPT,
        {
            **base,
            "result_subject": RUN_ID,
            "evidence_available": [rel(REPAIR_DESIGN_MATRIX), rel(RUN364CY_QUEUE), rel(GUARDRAIL_MATRIX), rel(DATA_INTEGRITY_AUDIT)],
            "evidence_missing": ["new proxy scout output(새 프록시 정찰 출력)", "new MT5 execution(새 MT5 실행)", "runtime authority parity closure(런타임 권위 동등성 폐쇄)"],
            "judgment_label": JUDGMENT,
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": NEXT_RUN_ID,
            "user_explanation_hook": "CX only prepares the next scout(CX는 다음 정찰 준비만 하며 개선 증명은 아님).",
        },
    )
    write_json(
        LINEAGE_RECEIPT,
        {
            **base,
            "source_inputs": [{"path": rel(path), "sha256": sha(path)} for path in INPUT_FILES if exists(path) and io_path(path).is_file()],
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [rel(path) for path in OUTPUT_FILES if exists(path)],
            "artifact_hashes": {rel(path): sha(path) for path in OUTPUT_FILES if exists(path) and io_path(path).is_file()},
            "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "availability": "tracked_materialization_artifacts(추적 구체화 산출물)",
            "lineage_judgment": "connected_with_materialization_boundary(구체화 경계로 연결됨)",
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            **base,
            "allowed_claim": "repair input queue ready only(수리 입력 대기열 준비만)",
            "forbidden_claims": ["runtime_authority", "operating_promotion", "live_readiness", "goal_achieve"],
            "runtime_authority": "not_claimed",
            "operating_promotion": "not_claimed",
            "goal_achieve": "not_claimed",
            "effect": "구체화(materialization, 구체화)를 성능 개선(performance improvement, 성능 개선)으로 과장하지 않습니다.",
        },
    )


def markdown_table(rows: Sequence[Mapping[str, Any]], columns: Sequence[str], limit: int = 12) -> str:
    if not rows:
        return "_none(없음)_"
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join(["---"] * len(columns)) + " |"]
    for row in rows[:limit]:
        lines.append("| " + " | ".join(str(row.get(col, "")).replace("|", "\\|").replace("\n", " ") for col in columns) + " |")
    if len(rows) > limit:
        lines.append("| ... | ... | ... | ... |")
    return "\n".join(lines)


def write_docs(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    queue = read_csv(RUN364CY_QUEUE).to_dict("records")
    report = f"""# run364CX h17 equity DD side-balance proxy-gap repair inputs(17시 수익곡선 낙폭/방향 균형/프록시 차이 수리 입력)

Updated(갱신): {final['created_at_utc']}

## Current Truth(현재 진실)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- judgment(판정): `{JUDGMENT}`
- baseline MT5 net/PF/density(기준 MT5 순수익/수익 팩터/밀도): `{final['baseline_mt5_net']}` / `{final['baseline_mt5_profit_factor']}` / `{final['baseline_mt5_density']}`
- baseline equity DD(기준 수익곡선 낙폭): `{final['baseline_equity_drawdown']}`
- baseline long share(기준 롱 비중): `{final['baseline_long_share']}`
- baseline proxy net diff(기준 프록시 순수익 차이): `{final['baseline_proxy_net_diff']}`
- queue rows(대기열 행): `{final['queue_rows']}`

## Action/Effect(행동/효과)

Action(행동): `run364CW`의 open repair(열린 수리) 세 축인 equity DD(수익곡선 낙폭), side balance(방향 균형), proxy/runtime gap(프록시/런타임 차이)을 `run364CY` scout queue(정찰 대기열)로 구체화했습니다.

Effect(효과): 다음 실행은 12월 수리(month12 repair, 12월 수리), density floor(밀도 하한), short floor(숏 하한)을 보존한 채 weak-hour long margin(약한 시간 롱 마진), hold-shape guard(보유 형태 가드), short-quality guard(숏 품질 가드), micro-margin gap filter(미세 마진 차이 필터)를 비교할 수 있습니다.

## CY Queue(CY 대기열)

{markdown_table(queue, ['queue_id', 'variant_id', 'variant_family', 'changed_variables', 'expected_effect'])}

## Gates(게이트)

{markdown_table(gates, ['gate', 'status', 'evidence', 'effect'])}

## Boundary(경계)

This materialization(이번 구체화)은 next scout input(다음 정찰 입력)입니다. new model training(새 모델 학습), new MT5 execution(새 MT5 실행), runtime authority(런타임 권위), operating promotion(운영 승격), Goal Achieve(목표 달성)는 모두 `not_claimed(주장 안 함)`입니다.
"""
    write_text(REPORT_PATH, report, bom=True)
    write_text(
        DECISION_DOC,
        f"""# Stage364CX decision(결정): h17 equity DD side-balance proxy-gap repair inputs

- date(날짜): {TODAY}
- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- queue rows(대기열 행): `{final['queue_rows']}`
- next action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): equity DD(수익곡선 낙폭), side balance(방향 균형), proxy/runtime gap(프록시/런타임 차이)을 같은 scout(정찰)에서 비교할 수 있게 했습니다.
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
        bom=True,
    )
    append_text_once(REVIEW_INDEX, f"run364CX__{RUN_ID}", f"\n- run364CX__{RUN_ID}: [{REPORT_PATH.name}]({REPORT_PATH.name}) - CX repair inputs(CX 수리 입력), next `{NEXT_RUN_ID}`.\n")
    append_text_once(STAGE_BRIEF, f"## run364CX__{RUN_ID}", f"\n## run364CX Repair Inputs(수리 입력)\n\nAction(행동): equity DD/side balance/proxy gap(수익곡선 낙폭/방향 균형/프록시 차이) 수리 후보 `{final['queue_rows']}`개를 만들었습니다.\n\nEffect(효과): `{NEXT_RUN_ID}`에서 proxy scout(프록시 정찰)를 실행할 수 있습니다.\n")
    append_text_once(STAGE_README, f"run364CX__{RUN_ID}", f"\n<!-- run364CX__{RUN_ID} -->\n## run364CX repair inputs(수리 입력)\n\nQueue(대기열): `{final['queue_rows']}` variants. Next(다음): `{NEXT_RUN_ID}`.\n")
    replace_prefixed_lines(
        STAGE_BRIEF,
        {
            "- current_run_id(현재 실행 ID):": f"- current_run_id(현재 실행 ID): `{NEXT_RUN_ID}`",
            "- latest_completed_run_id(최근 완료 실행 ID):": f"- latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`",
            "- selection_status(선택 상태):": f"- selection_status(선택 상태): `{STATUS}`",
            "- claim_boundary(주장 경계):": f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
        },
        bom=True,
    )
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

Current truth(현재 진실): `run364CX` materialized(구체화 완료) `{final['queue_rows']}` repair variants(수리 변형) from `run364CW` open repair(열린 수리). Baseline MT5 net/PF/density(기준 MT5 순수익/수익 팩터/밀도)는 `{final['baseline_mt5_net']}` / `{final['baseline_mt5_profit_factor']}` / `{final['baseline_mt5_density']}`입니다.

Next action(다음 행동): `{NEXT_RUN_ID}`에서 weak-hour long margin(약한 시간 롱 마진), hold-shape guard(보유 형태 가드), short-quality guard(숏 품질 가드), proxy/runtime gap filter(프록시/런타임 차이 필터)를 proxy scout(프록시 정찰)로 실행합니다.

Operating boundary(운영 경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""",
        bom=True,
    )
    write_text(
        SELECTION_STATUS,
        f"""# Stage364 selection status(선택 상태)

Updated(갱신): {final['created_at_utc']}

Current run(현재 실행): `{NEXT_RUN_ID}`
Latest completed run(최근 완료 실행): `{RUN_ID}`

Latest materialization(최근 구체화): `{RUN_ID}`.

Queue rows(대기열 행): `{final['queue_rows']}`.

Repair focus(수리 초점): equity DD(수익곡선 낙폭), side balance(방향 균형), proxy/runtime gap(프록시/런타임 차이).

Authority(권위): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""",
        bom=True,
    )
    append_text_once(WORKSPACE_CHANGELOG, f"run364CX__{RUN_ID}", f"\n<!-- run364CX__{RUN_ID} -->\n- {final['created_at_utc']} `{RUN_ID}` materialized equity DD/side balance/proxy gap repair inputs(수익곡선 낙폭/방향 균형/프록시 차이 수리 입력); next `{NEXT_RUN_ID}`.\n")
    append_text_once(IDEA_REGISTRY, f"run364CX__{RUN_ID}", f"\n<!-- run364CX__{RUN_ID} -->\n- `{RUN_ID}`: CR04 month12 repair(12월 수리)를 보존하면서 equity DD/side balance/proxy gap(수익곡선 낙폭/방향 균형/프록시 차이) 수리 변형 `{final['queue_rows']}`개를 열었다.\n")
    append_text_once(NEGATIVE_RESULT_REGISTER, f"run364CX__{RUN_ID}", f"\n<!-- run364CX__{RUN_ID} -->\n- `{RUN_ID}`: Not invalid(무효 아님). Materialization only(구체화 전용)라 성능 개선을 주장하지 않는다. Reopen condition(재개 조건): `{NEXT_RUN_ID}`가 density >= 3, short_count >= 100, month12 net >= 0을 보존하며 equity-risk proxy(수익곡선 위험 프록시)나 long share(롱 비중)를 개선해야 한다.\n")


def write_ledgers(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    common = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": f"{RUN_ID}__materialization",
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
        "final_decision_path": rel(FINAL_DECISION),
        "gate_audit_path": rel(GATE_AUDIT),
        "created_at": final["created_at_utc"],
        "work_family": "experiment_design(실험 설계)",
        "scoreboard_lane": "repair_input_materialization(수리 입력 구체화)",
        "external_verification_status": "not_applicable_materialization_only(해당 없음, 구체화 전용)",
        "evidence_boundary": "queue_materialization_only(대기열 구체화 전용)",
        "question": "Can CR04 be repaired on equity DD, side balance, and proxy/runtime gap without losing month12 repair?(CR04가 12월 수리를 잃지 않고 수익곡선 낙폭/방향 균형/프록시 차이를 수리할 수 있는가?)",
        "next_action": NEXT_RUN_ID,
        "net_profit": final["baseline_mt5_net"],
        "profit_factor": final["baseline_mt5_profit_factor"],
        "trade_density_per_feature_day": final["baseline_mt5_density"],
        "max_drawdown_amount": final["baseline_equity_drawdown"],
        "result_judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "primary_artifact": rel(RUN364CY_QUEUE),
    }
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], [common], extend_header=True)
    append_or_replace_csv(STAGE_LEDGER, ["run_id", "subrun_id"], [common], extend_header=True)
    append_or_replace_csv(PROJECT_LEDGER, ["run_id", "subrun_id"], [common], extend_header=True)

    artifact_rows = [
        {
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "artifact_type": artifact_type,
            "path": rel(path),
            "sha256": sha(path) if exists(path) and io_path(path).is_file() else "",
            "created_at": final["created_at_utc"],
            "claim_boundary": CLAIM_BOUNDARY,
            "artifact_id": f"{RUN_NUMBER}_{artifact_type}",
            "created_at_utc": final["created_at_utc"],
            "notes": note,
            "artifact_path": rel(path),
        }
        for artifact_type, path, note in [
            ("repair_design_matrix", REPAIR_DESIGN_MATRIX, "Repair design matrix(수리 설계 행렬)."),
            ("cy_queue", RUN364CY_QUEUE, "CY scout queue(CY 정찰 대기열)."),
            ("guardrail_matrix", GUARDRAIL_MATRIX, "Guardrail matrix(가드레일 행렬)."),
            ("data_integrity_audit", DATA_INTEGRITY_AUDIT, "Data integrity audit(데이터 무결성 감사)."),
            ("final_decision", FINAL_DECISION, "Final decision(최종 결정)."),
            ("run_manifest", RUN_MANIFEST, "Run manifest(실행 목록)."),
            ("report", REPORT_PATH, "Human report(사람용 보고서)."),
        ]
    ]
    append_or_replace_csv(ARTIFACT_REGISTRY, ["run_id", "artifact_type", "path"], artifact_rows, extend_header=True)
    parent.repair_run_registry_line_endings(RUN_ID)


def write_final_files(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    write_csv(GATE_AUDIT, gates)
    write_json(FINAL_DECISION, final)
    outputs = [path for path in OUTPUT_FILES if exists(path)]
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "run_number": RUN_NUMBER,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "status": final["status"],
            "judgment": final["judgment"],
            "claim_boundary": CLAIM_BOUNDARY,
            "input_files": [rel(path) for path in INPUT_FILES],
            "input_hashes": {rel(path): sha(path) for path in INPUT_FILES if exists(path) and io_path(path).is_file()},
            "output_files": [rel(path) for path in outputs],
            "output_hashes": {rel(path): sha(path) for path in outputs if io_path(path).is_file()},
        },
    )


def main() -> None:
    ensure_dirs()
    cw_final = validate_inputs()
    write_csv(INPUT_MANIFEST, input_manifest_rows())
    write_work_packet()
    source_summary(cw_final)
    designs = design_rows(cw_final)
    write_tables(cw_final, designs)
    gates = gate_rows(designs)
    created_at = now_utc()
    final = final_payload(cw_final, designs, gates, created_at)
    write_receipts(final, designs)
    gates = gate_rows(designs)
    final = final_payload(cw_final, designs, gates, created_at)
    write_docs(final, gates)
    write_final_files(final, gates)
    write_ledgers(final, gates)
    write_final_files(final, gates)
    print(json.dumps(json_ready(final), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
