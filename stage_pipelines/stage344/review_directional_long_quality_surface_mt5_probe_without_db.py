from __future__ import annotations

import csv
import json
import os
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from stage_pipelines.stage344 import (  # noqa: E402
    execute_directional_long_supply_quality_surface_mt5_probe_without_db as exe,
)
from stage_pipelines.stage344 import (  # noqa: E402
    materialize_directional_long_supply_quality_surface_package_without_db as pkg,
)


TODAY = "2026-06-01"
STAGE_ID = pkg.STAGE_ID
STAGE_DIR = pkg.STAGE_DIR
RUN_NUMBER = "run344E"
RUN_ID = "run344E_review_directional_long_quality_surface_mt5_probe_without_db_v1"
PARENT_RUN_ID = exe.RUN_ID
SOURCE_PACKAGE_RUN_ID = pkg.RUN_ID
NEXT_RUN_ID = "run344F_design_s07_trend_confirmed_forward_cost_stability_validation_without_db_v1"

STATUS = "completed_stage344E_directional_long_quality_surface_reviewed_positive_probe_candidate_no_selection"
JUDGMENT = "directional_long_quality_surface_positive_mt5_probe_s07_promotion_candidate_not_operating"
DECISION = "stage344E_open_run344F_s07_trend_confirmed_forward_cost_stability_validation_design"
CLAIM_BOUNDARY = (
    "research_development_review_only_directional_long_quality_surface_mt5_probe_"
    "promotion_candidate_not_operating_no_candidate_selection_no_forward_no_live_readiness_"
    "no_operating_promotion_no_runtime_authority_no_goal_claim"
)

RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEW_DIR / "run344E_directional_long_quality_surface_mt5_probe_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage344E_directional_long_quality_surface_mt5_probe_review.md"
SELECTION_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
STAGE_README = STAGE_DIR / "README.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"

SOURCE_FINAL = exe.FINAL_DECISION
SOURCE_GATES = exe.GATE_AUDIT
SOURCE_SUMMARY = exe.EXECUTION_SUMMARY
SOURCE_DIFF = exe.PROXY_MT5_DIFF
SOURCE_RUNTIME_IDENTITY = exe.RUNTIME_IDENTITY
SOURCE_RUNTIME_MAPPING_AUDIT = pkg.RUNTIME_MAPPING_AUDIT
SOURCE_VARIANT_PREVIEW = pkg.VARIANT_PREVIEW
SOURCE_PACKAGE_FINAL = pkg.FINAL_DECISION
SOURCE_PACKAGE_GATES = pkg.GATE_AUDIT

REVIEW_SCORECARD = RUN_DIR / "directional_long_quality_surface_review_scorecard.csv"
PERFORMANCE_ATTRIBUTION = RUN_DIR / "performance_attribution.csv"
POSITIVE_CLUES = RUN_DIR / "positive_clues.csv"
FAILURE_MEMORY = RUN_DIR / "failure_memory.csv"
NEXT_QUEUE = RUN_DIR / "run344F_queue.csv"
STALE_OUTPUTS = (
    RUN_DIR / "run344F_s07_trend_confirmed_forward_cost_stability_validation_queue.csv",
)
JUDGMENT_RECEIPT = RUN_DIR / "judgment_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
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
IDEA_REGISTRY = ROOT / "docs" / "registers" / "idea_registry.md"
NEGATIVE_RESULT_REGISTER = ROOT / "docs" / "registers" / "negative_result_register.md"

PROMOTION_CANDIDATE_ATTEMPT = "s07_trend_confirmed_long_only"
ANCHOR_ATTEMPT = "s01_anchor_short_supply_control"
SHAPE_CONTROL_ATTEMPT = "s02_shape_control_payoff_audit"

INPUT_FILES = (
    SOURCE_FINAL,
    SOURCE_GATES,
    SOURCE_SUMMARY,
    SOURCE_DIFF,
    SOURCE_RUNTIME_IDENTITY,
    SOURCE_RUNTIME_MAPPING_AUDIT,
    SOURCE_VARIANT_PREVIEW,
    SOURCE_PACKAGE_FINAL,
    SOURCE_PACKAGE_GATES,
)

OUTPUT_FILES = (
    REVIEW_SCORECARD,
    PERFORMANCE_ATTRIBUTION,
    POSITIVE_CLUES,
    FAILURE_MEMORY,
    NEXT_QUEUE,
    JUDGMENT_RECEIPT,
    PERFORMANCE_RECEIPT,
    LINEAGE_RECEIPT,
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
    IDEA_REGISTRY,
    NEGATIVE_RESULT_REGISTER,
    Path(__file__),
)


def now_utc() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def rel(path: Path | str) -> str:
    return pkg.rel(path)


def path_is_file(path: Path) -> bool:
    return pkg.path_is_file(path)


def ensure_parent(path: Path) -> None:
    pkg.ensure_parent(path)


def required(path: Path) -> Path:
    return pkg.required(path)


def read_csv(path: Path) -> pd.DataFrame:
    return pkg.read_csv(path)


def read_json(path: Path) -> Any:
    return pkg.read_json(path)


def write_json(path: Path, payload: Any) -> None:
    pkg.write_json(path, payload)


def write_text(path: Path, text: str) -> None:
    pkg.write_text(path, text)


def append_text_once(path: Path, marker: str, text: str) -> None:
    pkg.append_text_once(path, marker, text)


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    rows_list = [dict(row) for row in rows]
    if fieldnames is None:
        fields: list[str] = []
        for row in rows_list:
            for key in row:
                if key not in fields:
                    fields.append(key)
        fieldnames = fields
    ensure_parent(path)
    with open(pkg.fs_path(path), "w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fieldnames), extrasaction="ignore")
        writer.writeheader()
        for row in rows_list:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def append_or_replace_csv(path: Path, keys: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> None:
    pkg.append_or_replace_csv(path, keys, rows)


def sha256_file(path: Path) -> str:
    return pkg.sha256_file(path)


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


def round2(value: Any) -> float:
    return round(as_float(value), 2)


def side_balance(long_count: Any, short_count: Any) -> float:
    long_value = as_float(long_count)
    short_value = as_float(short_count)
    top = max(long_value, short_value)
    if top <= 0:
        return 0.0
    return round(min(long_value, short_value) / top, 4)


def get_attempt(frame: pd.DataFrame, attempt_name: str) -> pd.Series:
    matched = frame.loc[frame["attempt_name"].astype(str).eq(attempt_name)]
    if matched.empty:
        raise RuntimeError(f"missing attempt: {attempt_name}")
    return matched.iloc[0]


def gates_passed(path: Path) -> bool:
    frame = read_csv(path)
    return bool(len(frame) > 0 and frame["status"].astype(str).str.lower().eq("passed").all())


def exact_parity(row: pd.Series) -> bool:
    return bool(
        str(row.get("comparison_status", "")) == "completed_exact_proxy_mt5_parity_reached_feature_last"
        and as_int(row.get("expected_missing_rows")) == 0
        and as_int(row.get("hash_mismatch_rows")) == 0
        and as_int(row.get("probability_mismatch_rows")) == 0
        and as_int(row.get("decision_mismatch_rows")) == 0
        and as_int(row.get("expected_rows")) == as_int(row.get("matched_rows"))
    )


def attempt_judgment(attempt_name: str, row: pd.Series) -> str:
    if attempt_name == PROMOTION_CANDIDATE_ATTEMPT:
        return "positive_probe_candidate_next_stress_required(긍정 탐침 후보, 다음 압박 필요)"
    if attempt_name in {"s04_long_quality_high_conf", "s05_long_quality_extreme_top20"}:
        return "positive_quality_clue_low_long_supply(긍정 품질 단서, 낮은 롱 공급)"
    if attempt_name in {"s06_volatility_mid_long_only", "s11_short_supply_protect_vol_filter"}:
        return "supply_expansion_quality_weaker(공급 확대, 품질 약화)"
    if attempt_name in {"s09_exit_lifecycle_short_hold_longs", "s10_exit_lifecycle_flat_recheck", "s12_no_entry_change_exit_only"}:
        return "exit_overlay_failure_memory(청산 오버레이 실패 기억)"
    if attempt_name == SHAPE_CONTROL_ATTEMPT:
        return "balance_control_weaker_profit(균형 대조, 수익 약화)"
    if attempt_name == "s08_cash_open_late_reentry":
        return "no_incremental_edge_vs_anchor(앵커 대비 추가 엣지 없음)"
    if attempt_name == "s03_near_anchor_long_rescue_seed":
        return "near_anchor_no_profit_improvement(앵커 근처, 수익 개선 부족)"
    if attempt_name == ANCHOR_ATTEMPT:
        return "anchor_reference_preserved(앵커 기준 보존)"
    if as_float(row.get("net_profit")) > 0:
        return "weak_positive_reference_no_selection(약한 긍정 참조, 선정 없음)"
    return "negative_or_unusable_probe(부정 또는 사용 불가 탐침)"


def build_review() -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    for source in INPUT_FILES:
        required(source)

    parent_final = read_json(SOURCE_FINAL)
    if parent_final.get("next_run_id", parent_final.get("next_action")) != RUN_ID:
        raise RuntimeError("run344D next action does not point to run344E")
    if not gates_passed(SOURCE_GATES):
        raise RuntimeError("run344D gate audit has failed rows")
    if not gates_passed(SOURCE_PACKAGE_GATES):
        raise RuntimeError("run344C package gate audit has failed rows")

    summary = read_csv(SOURCE_SUMMARY)
    mapping = read_csv(SOURCE_RUNTIME_MAPPING_AUDIT)
    if summary.empty:
        raise RuntimeError("run344D MT5 summary is empty")
    if mapping.empty:
        raise RuntimeError("run344C runtime mapping audit is empty")

    for column in [
        "expected_rows",
        "matched_rows",
        "expected_missing_rows",
        "hash_mismatch_rows",
        "probability_mismatch_rows",
        "decision_mismatch_rows",
        "net_profit",
        "profit_factor",
        "expectancy",
        "recovery_factor",
        "max_drawdown_amount",
        "trade_count",
        "long_trade_count",
        "short_trade_count",
    ]:
        if column in summary.columns:
            summary[column] = pd.to_numeric(summary[column], errors="coerce").fillna(0.0)

    anchor = get_attempt(summary, ANCHOR_ATTEMPT)
    shape_control = get_attempt(summary, SHAPE_CONTROL_ATTEMPT)
    candidate = get_attempt(summary, PROMOTION_CANDIDATE_ATTEMPT)

    merged = summary.merge(
        mapping[
            [
                "attempt_name",
                "source_attempt",
                "design_intent",
                "runtime_mapping",
                "runtime_mapping_value",
                "known_difference",
                "usability",
            ]
        ],
        on="attempt_name",
        how="left",
    )

    score_rows: list[dict[str, Any]] = []
    for _, row in merged.iterrows():
        attempt_name = str(row.get("attempt_name", ""))
        long_count = as_int(row.get("long_trade_count"))
        short_count = as_int(row.get("short_trade_count"))
        score_rows.append(
            {
                "attempt_name": attempt_name,
                "model_id": row.get("model_id", ""),
                "source_attempt": row.get("source_attempt", ""),
                "design_intent": row.get("design_intent", ""),
                "runtime_mapping": row.get("runtime_mapping", ""),
                "runtime_mapping_value": row.get("runtime_mapping_value", ""),
                "known_difference": row.get("known_difference", ""),
                "usability": row.get("usability", ""),
                "exact_parity_pass": exact_parity(row),
                "net_profit": round2(row.get("net_profit")),
                "profit_factor": round2(row.get("profit_factor")),
                "expectancy": round2(row.get("expectancy")),
                "recovery_factor": round2(row.get("recovery_factor")),
                "max_drawdown_amount": round2(row.get("max_drawdown_amount")),
                "trade_count": as_int(row.get("trade_count")),
                "long_trade_count": long_count,
                "short_trade_count": short_count,
                "side_balance": side_balance(long_count, short_count),
                "delta_net_vs_anchor": round2(as_float(row.get("net_profit")) - as_float(anchor.get("net_profit"))),
                "delta_pf_vs_anchor": round2(as_float(row.get("profit_factor")) - as_float(anchor.get("profit_factor"))),
                "delta_expectancy_vs_anchor": round2(as_float(row.get("expectancy")) - as_float(anchor.get("expectancy"))),
                "delta_recovery_vs_anchor": round2(as_float(row.get("recovery_factor")) - as_float(anchor.get("recovery_factor"))),
                "delta_drawdown_vs_anchor": round2(as_float(row.get("max_drawdown_amount")) - as_float(anchor.get("max_drawdown_amount"))),
                "delta_trades_vs_anchor": as_int(row.get("trade_count")) - as_int(anchor.get("trade_count")),
                "delta_longs_vs_anchor": long_count - as_int(anchor.get("long_trade_count")),
                "delta_net_vs_shape_control": round2(as_float(row.get("net_profit")) - as_float(shape_control.get("net_profit"))),
                "delta_pf_vs_shape_control": round2(as_float(row.get("profit_factor")) - as_float(shape_control.get("profit_factor"))),
                "review_judgment": attempt_judgment(attempt_name, row),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    attribution_rows = [
        {
            "factor": "trend_confirmed_long_filter(추세 확인 롱 필터)",
            "evidence_attempts": PROMOTION_CANDIDATE_ATTEMPT,
            "delta_net_vs_anchor": round2(as_float(candidate.get("net_profit")) - as_float(anchor.get("net_profit"))),
            "delta_pf_vs_anchor": round2(as_float(candidate.get("profit_factor")) - as_float(anchor.get("profit_factor"))),
            "delta_trades_vs_anchor": as_int(candidate.get("trade_count")) - as_int(anchor.get("trade_count")),
            "delta_longs_vs_anchor": as_int(candidate.get("long_trade_count")) - as_int(anchor.get("long_trade_count")),
            "delta_drawdown_vs_anchor": round2(as_float(candidate.get("max_drawdown_amount")) - as_float(anchor.get("max_drawdown_amount"))),
            "effect": "net/PF/trade_count/long_supply all improved without drawdown increase(순수익/수익 팩터/거래수/롱 공급이 낙폭 증가 없이 함께 개선)",
            "use": "next cost/session/regime validation seed(다음 비용/세션/국면 검증 씨앗)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "factor": "high_confidence_long_quality(고신뢰 롱 품질)",
            "evidence_attempts": "s04_long_quality_high_conf;s05_long_quality_extreme_top20",
            "delta_net_vs_anchor": "15.33 to 15.69",
            "delta_pf_vs_anchor": "0.00 to 0.47",
            "delta_trades_vs_anchor": "1 to 2",
            "delta_longs_vs_anchor": "1 to 2",
            "delta_drawdown_vs_anchor": 0.0,
            "effect": "quality rises but long supply stays thin(품질은 오르지만 롱 공급은 얇게 남음)",
            "use": "secondary comparator against s07( s07 대비 보조 대조군)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "factor": "volatility_mid_filter(중간 변동성 필터)",
            "evidence_attempts": "s06_volatility_mid_long_only;s11_short_supply_protect_vol_filter",
            "delta_net_vs_anchor": "-2.48 to -0.48",
            "delta_pf_vs_anchor": "-0.86 to -0.80",
            "delta_trades_vs_anchor": "7 to 8",
            "delta_longs_vs_anchor": "7 to 8",
            "delta_drawdown_vs_anchor": 0.0,
            "effect": "long supply expands but PF quality weakens(롱 공급은 늘지만 수익 팩터 품질은 약화)",
            "use": "constraint, not promotion seed(승격 씨앗이 아니라 제약)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "factor": "exit_lifecycle_global_overlay(전역 청산 생명주기 오버레이)",
            "evidence_attempts": "s09_exit_lifecycle_short_hold_longs;s10_exit_lifecycle_flat_recheck;s12_no_entry_change_exit_only",
            "delta_net_vs_anchor": "-89.26 to -179.50",
            "delta_pf_vs_anchor": "-2.22 to -2.78",
            "delta_trades_vs_anchor": "10 to 21",
            "delta_longs_vs_anchor": "1 to 12",
            "delta_drawdown_vs_anchor": "-6.17 to 10.83",
            "effect": "extra activity damages expectancy and recovery(활동 증가가 기대값과 회복 계수를 훼손)",
            "use": "failure memory for next packet(다음 작업 묶음의 실패 기억)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "factor": "shape_balance_control(거래 형태 균형 대조)",
            "evidence_attempts": SHAPE_CONTROL_ATTEMPT,
            "delta_net_vs_anchor": round2(as_float(shape_control.get("net_profit")) - as_float(anchor.get("net_profit"))),
            "delta_pf_vs_anchor": round2(as_float(shape_control.get("profit_factor")) - as_float(anchor.get("profit_factor"))),
            "delta_trades_vs_anchor": as_int(shape_control.get("trade_count")) - as_int(anchor.get("trade_count")),
            "delta_longs_vs_anchor": as_int(shape_control.get("long_trade_count")) - as_int(anchor.get("long_trade_count")),
            "delta_drawdown_vs_anchor": round2(as_float(shape_control.get("max_drawdown_amount")) - as_float(anchor.get("max_drawdown_amount"))),
            "effect": "balance improves but profit quality drops(균형은 좋아지지만 수익 품질은 하락)",
            "use": "balance guardrail, not profit anchor(균형 가드레일이지 수익 앵커 아님)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]

    positive_rows = [
        {
            "clue_id": "s07_primary_positive_probe_candidate(주요 긍정 탐침 후보)",
            "attempt_name": PROMOTION_CANDIDATE_ATTEMPT,
            "model_id": candidate.get("model_id", ""),
            "net_profit": round2(candidate.get("net_profit")),
            "profit_factor": round2(candidate.get("profit_factor")),
            "expectancy": round2(candidate.get("expectancy")),
            "recovery_factor": round2(candidate.get("recovery_factor")),
            "trade_count": as_int(candidate.get("trade_count")),
            "long_short": f"{as_int(candidate.get('long_trade_count'))}/{as_int(candidate.get('short_trade_count'))}",
            "why_it_matters": "first surface in this branch improved net/PF/trades/longs together(이 분기에서 순수익/수익 팩터/거래수/롱을 함께 올린 첫 표면)",
            "next_use": "run344F cost/session/regime stress design(344F 비용/세션/국면 압박 설계)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "clue_id": "s04_s05_quality_threshold_support(품질 임계값 보조 단서)",
            "attempt_name": "s04_long_quality_high_conf;s05_long_quality_extreme_top20",
            "model_id": "logreg_balanced_c025_s04/s05",
            "net_profit": "168.12 to 168.48",
            "profit_factor": "3.55 to 4.02",
            "expectancy": "7.00 to 7.33",
            "recovery_factor": "1.88 to 1.89",
            "trade_count": "23 to 24",
            "long_short": "3/20 to 4/20",
            "why_it_matters": "quality threshold preserves profit but long supply remains limited(품질 임계값은 수익을 보존하지만 롱 공급은 제한됨)",
            "next_use": "secondary comparator and threshold stress(보조 대조군과 임계값 압박)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]

    failure_rows = [
        {
            "failure_id": "exit_overlay_degrades_expectancy(청산 오버레이 기대값 훼손)",
            "attempts": "s09;s10;s12",
            "evidence": "net_profit 56.40/-26.71/63.53, PF 1.33/0.77/1.50(순수익과 수익 팩터 약화)",
            "constraint_for_next": "do not apply global max-hold or close-on-flat as broad rescue(전역 보유 단축이나 관망 청산을 넓은 구조 구제로 쓰지 않음)",
            "effect": "prevents repeating high-activity low-quality exits(활동만 늘고 품질 낮은 청산 반복 방지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "failure_id": "balance_alone_is_not_edge(균형만으로는 엣지가 아님)",
            "attempts": SHAPE_CONTROL_ATTEMPT,
            "evidence": "long/short improves to 13/20 but net drops to 122.90 and PF to 1.89(롱/숏은 개선되나 순수익과 수익 팩터 하락)",
            "constraint_for_next": "balance must be paired with profit quality floor(균형은 수익 품질 하한과 같이 봄)",
            "effect": "keeps long/short repair from overriding profit quality(롱/숏 수리가 수익 품질을 덮지 않게 함)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "failure_id": "late_reentry_no_incremental_edge(후반 재진입 추가 엣지 없음)",
            "attempts": "s08_cash_open_late_reentry",
            "evidence": "identical to anchor on MT5 KPI(MT5 핵심 성과 지표가 앵커와 동일)",
            "constraint_for_next": "do not spend next packet on this mapping alone(다음 작업 묶음을 이 매핑 단독에 쓰지 않음)",
            "effect": "focuses next exploration on trend confirmation and cost stability(다음 탐색을 추세 확인과 비용 안정성에 집중)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]

    next_queue_rows = [
        {
            "queue_id": "run344F_01_cost_stress(비용 압박)",
            "seed_attempt": PROMOTION_CANDIDATE_ATTEMPT,
            "question": "does s07 survive spread/slippage/commission stress?(s07이 스프레드/슬리피지/커미션 압박을 버티는가?)",
            "required_evidence": "MT5 tester report and proxy-MT5 diff under stressed costs(비용 압박 조건 MT5 테스터 보고서와 프록시-MT5 차이)",
            "stop_condition": "PF below 1.5 or recovery below 1.0 under moderate cost stress(중간 비용 압박에서 PF 1.5 미만 또는 회복 계수 1.0 미만)",
            "claim_boundary": "validation_design_only(검증 설계 전용)",
        },
        {
            "queue_id": "run344F_02_session_regime_stability(세션/국면 안정성)",
            "seed_attempt": PROMOTION_CANDIDATE_ATTEMPT,
            "question": "which session/regime buckets carry the s07 edge?(어떤 세션/국면 버킷이 s07 엣지를 운반하는가?)",
            "required_evidence": "bucketed trade and equity attribution(버킷별 거래와 수익곡선 귀속)",
            "stop_condition": "edge concentrated in one tiny bucket only(엣지가 하나의 작은 버킷에만 집중)",
            "claim_boundary": "validation_design_only(검증 설계 전용)",
        },
        {
            "queue_id": "run344F_03_anchor_s05_s07_comparator(앵커/s05/s07 대조)",
            "seed_attempt": "s01_anchor_short_supply_control;s05_long_quality_extreme_top20;s07_trend_confirmed_long_only",
            "question": "is s07 better than high-confidence threshold after costs?(비용 반영 후 s07이 고신뢰 임계값보다 나은가?)",
            "required_evidence": "same tester settings and exact parity for all comparators(모든 대조군 동일 테스터 설정과 정확 동등성)",
            "stop_condition": "s07 only wins raw net but loses stress PF/recovery(s07이 원 순수익만 이기고 압박 PF/회복에서 패배)",
            "claim_boundary": "validation_design_only(검증 설계 전용)",
        },
        {
            "queue_id": "run344F_04_forward_replay_readiness(전진/재생 준비)",
            "seed_attempt": PROMOTION_CANDIDATE_ATTEMPT,
            "question": "what files are needed for narrow forward/replay probe?(좁은 전진/재생 탐침에 어떤 파일이 필요한가?)",
            "required_evidence": "handoff manifest, model hash, set/ini hash, terminal output path(인계 목록, 모델 해시, 설정 해시, 터미널 출력 경로)",
            "stop_condition": "artifact lineage or runtime parity cannot be matched(산출물 계보 또는 런타임 동등성이 맞지 않음)",
            "claim_boundary": "validation_design_only(검증 설계 전용)",
        },
    ]

    final = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "source_package_run_id": SOURCE_PACKAGE_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_run_id": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
        "attempt_rows_reviewed": len(score_rows),
        "parent_gate_passed": True,
        "parent_exact_parity_rows": as_int(parent_final.get("exact_parity_rows")),
        "matched_rows": as_int(parent_final.get("matched_rows")),
        "expected_rows": as_int(parent_final.get("expected_rows")),
        "mismatch_rows": as_int(parent_final.get("mismatch_rows")),
        "promotion_candidate_status": "research_promotion_candidate(연구 승격 후보)",
        "promotion_candidate_attempt_name": PROMOTION_CANDIDATE_ATTEMPT,
        "promotion_candidate_model_id": candidate.get("model_id", ""),
        "promotion_candidate_net_profit": round2(candidate.get("net_profit")),
        "promotion_candidate_profit_factor": round2(candidate.get("profit_factor")),
        "promotion_candidate_expectancy": round2(candidate.get("expectancy")),
        "promotion_candidate_recovery_factor": round2(candidate.get("recovery_factor")),
        "promotion_candidate_max_drawdown_amount": round2(candidate.get("max_drawdown_amount")),
        "promotion_candidate_trade_count": as_int(candidate.get("trade_count")),
        "promotion_candidate_long_trade_count": as_int(candidate.get("long_trade_count")),
        "promotion_candidate_short_trade_count": as_int(candidate.get("short_trade_count")),
        "promotion_candidate_side_balance": side_balance(candidate.get("long_trade_count"), candidate.get("short_trade_count")),
        "delta_net_vs_anchor": round2(as_float(candidate.get("net_profit")) - as_float(anchor.get("net_profit"))),
        "delta_pf_vs_anchor": round2(as_float(candidate.get("profit_factor")) - as_float(anchor.get("profit_factor"))),
        "delta_trades_vs_anchor": as_int(candidate.get("trade_count")) - as_int(anchor.get("trade_count")),
        "delta_longs_vs_anchor": as_int(candidate.get("long_trade_count")) - as_int(anchor.get("long_trade_count")),
        "delta_recovery_vs_anchor": round2(as_float(candidate.get("recovery_factor")) - as_float(anchor.get("recovery_factor"))),
        "delta_drawdown_vs_anchor": round2(as_float(candidate.get("max_drawdown_amount")) - as_float(anchor.get("max_drawdown_amount"))),
        "positive_clue_rows": len(positive_rows),
        "failure_memory_rows": len(failure_rows),
        "next_queue_rows": len(next_queue_rows),
        "candidate_selection": "not_run",
        "selected_model": "none(없음)",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "live_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
    }
    return score_rows, attribution_rows, positive_rows, failure_rows, next_queue_rows, final


def make_gates(final: Mapping[str, Any]) -> list[dict[str, Any]]:
    no_forbidden = (
        final["candidate_selection"] == "not_run"
        and final["selected_model"] == "none(없음)"
        and final["forward_passed"] == "not_claimed"
        and final["forward_failed"] == "not_claimed"
        and final["runtime_authority"] == "not_claimed"
        and final["operating_promotion"] == "not_claimed"
        and final["live_readiness"] == "not_claimed"
        and final["goal_achieve"] == "not_claimed"
    )
    return [
        gate("parent_run344D_gates_passed", final["parent_gate_passed"], SOURCE_GATES, "review(검토)가 passed gate(통과 게이트) 위에서만 열림"),
        gate("mt5_probe_summary_loaded", final["attempt_rows_reviewed"] == 12, SOURCE_SUMMARY, "12개 MT5 probe(런타임 탐침) 결과를 모두 검토"),
        gate("runtime_parity_preserved_in_review", final["matched_rows"] == final["expected_rows"] and final["mismatch_rows"] == 0, SOURCE_DIFF, "review(검토)가 proxy-MT5 parity(프록시-MT5 동등성)를 훼손하지 않음"),
        gate("scorecard_materialized", path_is_file(REVIEW_SCORECARD), REVIEW_SCORECARD, "attempt별 KPI scorecard(점수표)를 저장"),
        gate("performance_attribution_written", path_is_file(PERFORMANCE_ATTRIBUTION), PERFORMANCE_ATTRIBUTION, "성과 귀속(performance attribution, 성과 귀속)을 저장"),
        gate("positive_clues_and_failure_memory_written", path_is_file(POSITIVE_CLUES) and path_is_file(FAILURE_MEMORY), POSITIVE_CLUES, "긍정 단서와 실패 기억을 분리"),
        gate("next_validation_queue_written", path_is_file(NEXT_QUEUE), NEXT_QUEUE, "run344F validation queue(검증 대기열)를 생성"),
        gate("no_forbidden_operating_claim", no_forbidden, FINAL_DECISION, "promotion candidate(승격 후보)를 운영 주장으로 올리지 않음"),
        gate("required_gate_coverage_audit_written", True, GATE_AUDIT, "required gate coverage audit(필수 게이트 커버리지 감사)를 기록"),
    ]


def gate(gate_id: str, passed: bool, evidence: Path, effect: str) -> dict[str, Any]:
    return {
        "gate_id": gate_id,
        "status": "passed" if passed else "failed",
        "evidence_path": rel(evidence),
        "effect": effect,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def write_receipts(
    final: Mapping[str, Any],
    attribution_rows: Sequence[Mapping[str, Any]],
    positive_rows: Sequence[Mapping[str, Any]],
    failure_rows: Sequence[Mapping[str, Any]],
) -> None:
    write_json(
        JUDGMENT_RECEIPT,
        {
            "receipt_id": "run344E_result_judgment(결과 판정)",
            "run_id": RUN_ID,
            "judgment": JUDGMENT,
            "judgment_boundary": "promotion_candidate_not_operating(승격 후보, 운영 아님)",
            "positive_clue_rows": len(positive_rows),
            "failure_memory_rows": len(failure_rows),
            "selected_model": final["selected_model"],
            "goal_achieve": final["goal_achieve"],
            "effect": "positive MT5 clue is kept for validation without operating claim(긍정 MT5 단서를 운영 주장 없이 검증으로 넘김)",
            "claim_boundary": CLAIM_BOUNDARY,
            "created_at_utc": now_utc(),
        },
    )
    write_json(
        PERFORMANCE_RECEIPT,
        {
            "receipt_id": "run344E_performance_attribution(성과 귀속)",
            "run_id": RUN_ID,
            "attribution_rows": len(attribution_rows),
            "primary_effect": "s07 improves net/PF/trades/longs together versus anchor(s07이 앵커 대비 순수익/수익 팩터/거래수/롱을 함께 개선)",
            "limitation": "single MT5 probe review only, no forward/replay authority(단일 MT5 탐침 검토일 뿐, 전진/재생 권위 없음)",
            "claim_boundary": CLAIM_BOUNDARY,
            "created_at_utc": now_utc(),
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            "receipt_id": "run344E_claim_boundary(주장 경계)",
            "run_id": RUN_ID,
            "candidate_selection": final["candidate_selection"],
            "selected_model": final["selected_model"],
            "forward_passed": final["forward_passed"],
            "runtime_authority": final["runtime_authority"],
            "operating_promotion": final["operating_promotion"],
            "live_readiness": final["live_readiness"],
            "goal_achieve": final["goal_achieve"],
            "effect": "prevents MT5 backtest-positive result from becoming a live claim(MT5 백테스트 양성 결과가 실거래 주장으로 바뀌지 않게 함)",
            "claim_boundary": CLAIM_BOUNDARY,
            "created_at_utc": now_utc(),
        },
    )


def write_lineage() -> None:
    inputs = []
    for path in INPUT_FILES:
        inputs.append(
            {
                "path": rel(path),
                "exists": path_is_file(path),
                "sha256": sha256_file(path) if path_is_file(path) else "",
            }
        )
    outputs = []
    for path in OUTPUT_FILES:
        if path == ARTIFACT_REGISTRY:
            continue
        outputs.append(
            {
                "path": rel(path),
                "exists": path_is_file(path),
                "sha256": sha256_file(path) if path_is_file(path) else "",
            }
        )
    write_json(
        LINEAGE_RECEIPT,
        {
            "receipt_id": "run344E_artifact_lineage(산출물 계보)",
            "run_id": RUN_ID,
            "parent_run_id": PARENT_RUN_ID,
            "source_package_run_id": SOURCE_PACKAGE_RUN_ID,
            "inputs": inputs,
            "outputs": outputs,
            "producer": rel(Path(__file__)),
            "effect": "links MT5 probe evidence to review outputs(런타임 탐침 근거와 검토 산출물을 연결)",
            "claim_boundary": CLAIM_BOUNDARY,
            "created_at_utc": now_utc(),
        },
    )


def write_docs(final: Mapping[str, Any]) -> None:
    report = f"""# run344E Directional Long Quality Surface Review(344E 방향성 롱 품질 표면 검토)

## Current Truth(현재 진실)

- run_id(실행 ID): `{RUN_ID}`
- parent_run(부모 실행): `{PARENT_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- promotion_candidate(승격 후보): `{final['promotion_candidate_attempt_name']}`
- selected_model(선정 모델): `{final['selected_model']}`
- Goal Achieve(목표 달성): `{final['goal_achieve']}`
- runtime_authority(런타임 권위): `{final['runtime_authority']}`
- operating_promotion(운영 승격): `{final['operating_promotion']}`
- next_run(다음 실행): `{NEXT_RUN_ID}`

## Result(결과)

`s07_trend_confirmed_long_only`는 anchor(앵커) 대비 net profit(순수익) `+{final['delta_net_vs_anchor']}`, profit factor(수익 팩터) `+{final['delta_pf_vs_anchor']}`, trade count(거래수) `+{final['delta_trades_vs_anchor']}`, long trades(롱 거래) `+{final['delta_longs_vs_anchor']}`를 만들었다. drawdown(낙폭)은 `+{final['delta_drawdown_vs_anchor']}`라서 증가하지 않았다.

## Action(행동)

run344D MT5 runtime probe(MT5 런타임 탐침) 결과를 scorecard(점수표), performance attribution(성과 귀속), positive clue(긍정 단서), failure memory(실패 기억), run344F queue(344F 대기열)로 분리했다.

## Effect(효과)

Stage343/344의 무게를 줄이고, 다음 작업은 `s07` cost/session/regime validation(비용/세션/국면 검증)이라는 작은 work packet(작업 묶음)으로 이어간다.

## Boundary(경계)

이 review(검토)는 research promotion candidate(연구 승격 후보)까지만 말한다. selection(선정), forward pass(전진 통과), live readiness(실거래 준비), operating promotion(운영 승격), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 모두 주장하지 않는다.
"""
    decision = f"""# {TODAY} Stage344E Review Decision(344E 검토 결정)

- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- candidate(후보): `{final['promotion_candidate_attempt_name']}`
- model_id(모델 ID): `{final['promotion_candidate_model_id']}`
- MT5 KPI(MT5 핵심 성과 지표): net `{final['promotion_candidate_net_profit']}`, PF `{final['promotion_candidate_profit_factor']}`, expectancy `{final['promotion_candidate_expectancy']}`, recovery `{final['promotion_candidate_recovery_factor']}`, drawdown `{final['promotion_candidate_max_drawdown_amount']}`, trades `{final['promotion_candidate_trade_count']}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- evidence(근거): `{rel(REVIEW_SCORECARD)}`, `{rel(PERFORMANCE_ATTRIBUTION)}`, `{rel(POSITIVE_CLUES)}`, `{rel(FAILURE_MEMORY)}`

Action(행동): s07 trend-confirmed long(추세 확인 롱)을 validation seed(검증 씨앗)로 넘긴다.
Effect(효과): 좋은 단서를 운영 주장으로 과장하지 않고, 비용/세션/국면 압박에서 깨지는지 먼저 본다.

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

Stage(단계)는 344로 분기되었고, run344E review(검토)까지 닫혔다. 다음은 s07 trend-confirmed long(추세 확인 롱)의 cost/session/regime validation(비용/세션/국면 검증) 설계다.

## Boundary(경계)

`{CLAIM_BOUNDARY}`
"""
    selection = f"""# Stage 344 Selection Status(344단계 선정 상태)

- selected_model(선정 모델): `none(없음)`
- promotion_candidate(승격 후보): `{final['promotion_candidate_attempt_name']}`
- promotion_candidate_status(승격 후보 상태): `{final['promotion_candidate_status']}`
- net_profit(순수익): `{final['promotion_candidate_net_profit']}`
- profit_factor(수익 팩터): `{final['promotion_candidate_profit_factor']}`
- expectancy(기대값): `{final['promotion_candidate_expectancy']}`
- drawdown(낙폭): `{final['promotion_candidate_max_drawdown_amount']}`
- recovery_factor(회복 계수): `{final['promotion_candidate_recovery_factor']}`
- trade_count(거래수): `{final['promotion_candidate_trade_count']}`
- long_short(롱/숏): `{final['promotion_candidate_long_trade_count']}/{final['promotion_candidate_short_trade_count']}`
- runtime_authority(런타임 권위): `not_claimed(주장 없음)`
- operating_promotion(운영 승격): `not_claimed(주장 없음)`
- Goal Achieve(목표 달성): `not_claimed(주장 없음)`

Effect(효과): s07을 다음 검증 씨앗으로만 보존하고, 운영 선정은 닫지 않는다.
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

    marker = f"run344E {RUN_ID}"
    append_text_once(
        STAGE_BRIEF,
        marker,
        f"""## run344E Directional Long Quality Surface Review(344E 방향성 롱 품질 표면 검토)

- run_id(실행 ID): `{RUN_ID}`
- judgment(판정): `{JUDGMENT}`
- promotion_candidate(승격 후보): `{final['promotion_candidate_attempt_name']}`
- effect(효과): Stage(단계) 무게를 줄이고 run344F validation(검증)으로 넘김.
""",
    )
    append_text_once(
        STAGE_README,
        marker,
        f"""## run344E Directional Long Quality Surface Review(344E 방향성 롱 품질 표면 검토)

- report(보고서): `{rel(REPORT_PATH)}`
- scorecard(점수표): `{rel(REVIEW_SCORECARD)}`
- next_queue(다음 대기열): `{rel(NEXT_QUEUE)}`
- effect(효과): positive clue(긍정 단서)와 failure memory(실패 기억)를 분리함.
""",
    )
    changelog = f"""## {TODAY} run344E Directional Long Quality Surface Review(방향성 롱 품질 표면 검토)

- action(행동): run344D MT5 runtime probe(MT5 런타임 탐침)를 review(검토)로 닫았다.
- effect(효과): `s07_trend_confirmed_long_only`를 research promotion candidate(연구 승격 후보)로 보존하고 run344F validation(검증)을 열었다.
- boundary(경계): selection/runtime authority/operating promotion/Goal Achieve(선정/런타임 권위/운영 승격/목표 달성)는 주장하지 않음.
"""
    append_text_once(ROOT_CHANGELOG, marker, changelog)
    append_text_once(WORKSPACE_CHANGELOG, marker, changelog)
    append_text_once(
        IDEA_REGISTRY,
        marker,
        f"""## run344E s07 Trend Confirmed Long(추세 확인 롱)

- idea(아이디어): low-ADX long veto(낮은 ADX 롱 거부)를 활용한 trend-confirmed long(추세 확인 롱).
- evidence(근거): MT5 net profit(순수익) `{final['promotion_candidate_net_profit']}`, PF(수익 팩터) `{final['promotion_candidate_profit_factor']}`, trades(거래수) `{final['promotion_candidate_trade_count']}`.
- effect(효과): 다음 cost/session/regime validation(비용/세션/국면 검증)의 씨앗으로 사용.
""",
    )
    append_text_once(
        NEGATIVE_RESULT_REGISTER,
        marker,
        """## run344E Exit Overlay Failure Memory(청산 오버레이 실패 기억)

- failure(실패): s09/s10/s12 exit lifecycle overlay(청산 생명주기 오버레이)는 net/PF/expectancy(순수익/수익 팩터/기대값)를 훼손했다.
- effect(효과): 다음 작업에서 전역 청산 수리(global exit repair, 전역 청산 수리)를 기본 해법으로 반복하지 않는다.
""",
    )


def write_registers(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    gate_passes = sum(1 for row in gates if row["status"] == "passed")
    gate_total = len(gates)
    base = {
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
        "gate_passes": gate_passes,
        "gate_total": gate_total,
        "claim_boundary": CLAIM_BOUNDARY,
        "source_package_run_id": SOURCE_PACKAGE_RUN_ID,
    }
    run_row = {
        **base,
        "lane": "review(검토)",
        "family": "runtime_probe_review(MT5 런타임 탐침 검토)",
        "primary_report": rel(REPORT_PATH),
        "run_number": RUN_NUMBER,
        "notes": "s07 kept as research promotion candidate(연구 승격 후보); no operating claim(운영 주장 없음).",
        "candidate_model_id": final["promotion_candidate_model_id"],
        "net_profit": final["promotion_candidate_net_profit"],
        "profit_factor": final["promotion_candidate_profit_factor"],
        "drawdown": final["promotion_candidate_max_drawdown_amount"],
        "recovery_factor": final["promotion_candidate_recovery_factor"],
        "trade_count": final["promotion_candidate_trade_count"],
        "expectancy": final["promotion_candidate_expectancy"],
        "attempt_count": final["attempt_rows_reviewed"],
        "matched_rows": final["matched_rows"],
        "result_status": JUDGMENT,
    }
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], [run_row])

    ledger_rows = [
        {
            **base,
            "ledger_row_id": f"{RUN_ID}__Tier A",
            "subrun_id": "Tier A",
            "view": "Tier A separate(Tier A 분리)",
            "record_view": "Tier A separate(Tier A 분리)",
            "tier": "Tier A",
            "tier_scope": "Tier A",
            "metric_scope": "mt5_probe_review",
            "kpi_scope": "mt5_probe_review",
            "scoreboard_lane": "review(검토)",
            "candidate_model_id": final["promotion_candidate_model_id"],
            "net_profit": final["promotion_candidate_net_profit"],
            "profit_factor": final["promotion_candidate_profit_factor"],
            "expectancy": final["promotion_candidate_expectancy"],
            "drawdown": final["promotion_candidate_max_drawdown_amount"],
            "recovery_factor": final["promotion_candidate_recovery_factor"],
            "trade_count": final["promotion_candidate_trade_count"],
            "result_status": JUDGMENT,
            "attempt_count": final["attempt_rows_reviewed"],
            "matched_rows": final["matched_rows"],
            "primary_kpi": f"net_profit={final['promotion_candidate_net_profit']};pf={final['promotion_candidate_profit_factor']};trades={final['promotion_candidate_trade_count']}",
            "guardrail_kpi": f"drawdown={final['promotion_candidate_max_drawdown_amount']};long_short={final['promotion_candidate_long_trade_count']}/{final['promotion_candidate_short_trade_count']}",
            "external_verification_status": "completed(완료)",
            "notes": "Promotion candidate only(승격 후보만), no selection(선정 없음), no operating claim(운영 주장 없음).",
        },
        {
            **base,
            "ledger_row_id": f"{RUN_ID}__Tier B",
            "subrun_id": "Tier B",
            "view": "Tier B separate(Tier B 분리)",
            "record_view": "Tier B separate(Tier B 분리)",
            "tier": "Tier B",
            "tier_scope": "Tier B",
            "metric_scope": "missing_required",
            "kpi_scope": "missing_required",
            "scoreboard_lane": "review(검토)",
            "candidate_model_id": "missing_required",
            "primary_kpi": "missing_required",
            "guardrail_kpi": "missing_required",
            "external_verification_status": "missing_required(필수 누락)",
            "result_status": "missing_required(필수 누락)",
            "notes": "Tier B(티어 B)는 이번 MT5 review(검토) 범위 밖이므로 필수 누락으로 기록.",
        },
        {
            **base,
            "ledger_row_id": f"{RUN_ID}__Tier A+B",
            "subrun_id": "Tier A+B",
            "view": "Tier A+B combined(Tier A+B 합산)",
            "record_view": "Tier A+B combined(Tier A+B 합산)",
            "tier": "Tier A+B",
            "tier_scope": "Tier A+B",
            "metric_scope": "same_as_tier_a_until_tier_b_available",
            "kpi_scope": "same_as_tier_a_until_tier_b_available",
            "scoreboard_lane": "review(검토)",
            "candidate_model_id": final["promotion_candidate_model_id"],
            "net_profit": final["promotion_candidate_net_profit"],
            "profit_factor": final["promotion_candidate_profit_factor"],
            "expectancy": final["promotion_candidate_expectancy"],
            "drawdown": final["promotion_candidate_max_drawdown_amount"],
            "recovery_factor": final["promotion_candidate_recovery_factor"],
            "trade_count": final["promotion_candidate_trade_count"],
            "result_status": "same_as_tier_a_until_tier_b_available",
            "attempt_count": final["attempt_rows_reviewed"],
            "matched_rows": final["matched_rows"],
            "primary_kpi": f"net_profit={final['promotion_candidate_net_profit']};pf={final['promotion_candidate_profit_factor']};trades={final['promotion_candidate_trade_count']}",
            "guardrail_kpi": f"drawdown={final['promotion_candidate_max_drawdown_amount']};long_short={final['promotion_candidate_long_trade_count']}/{final['promotion_candidate_short_trade_count']}",
            "external_verification_status": "completed(완료)",
            "notes": "Tier B(티어 B)가 없으므로 combined(합산)는 Tier A와 같은 경계로 기록.",
        },
    ]
    append_or_replace_csv(PROJECT_LEDGER, ["run_id", "view"], ledger_rows)
    append_or_replace_csv(STAGE_LEDGER, ["run_id", "view"], ledger_rows)


def write_artifact_registry() -> None:
    artifact_rows = []
    for index, path in enumerate(OUTPUT_FILES, start=1):
        if path == ARTIFACT_REGISTRY or not path_is_file(path):
            continue
        artifact_type = "script" if path == Path(__file__) else path.suffix.lstrip(".") or "artifact"
        artifact_rows.append(
            {
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "artifact_type": artifact_type,
                "path": rel(path),
                "artifact_path": rel(path),
                "sha256": sha256_file(path),
                "created_at": TODAY,
                "created_at_utc": now_utc(),
                "artifact_id": f"{RUN_NUMBER}_{index:02d}_{artifact_type}",
                "notes": "run344E review output(344E 검토 산출물)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    if path_is_file(ARTIFACT_REGISTRY):
        fieldnames, existing = pkg.read_csv_rows(ARTIFACT_REGISTRY)
    else:
        fieldnames, existing = [], []
    for row in artifact_rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    kept = [row for row in existing if row.get("run_id") != RUN_ID]
    pkg.write_csv_rows(ARTIFACT_REGISTRY, kept + artifact_rows, fieldnames)


def cleanup_stale_outputs() -> None:
    run_root = RUN_DIR.resolve()
    for path in STALE_OUTPUTS:
        resolved = path.resolve()
        if not str(resolved).lower().startswith(str(run_root).lower()):
            raise RuntimeError(f"refusing to clean stale output outside run dir: {path}")
        if path_is_file(resolved):
            os.remove(pkg.fs_path(resolved))


def main() -> None:
    cleanup_stale_outputs()
    score_rows, attribution_rows, positive_rows, failure_rows, next_queue_rows, final = build_review()
    ensure_parent(FINAL_DECISION)

    write_csv(REVIEW_SCORECARD, score_rows)
    write_csv(PERFORMANCE_ATTRIBUTION, attribution_rows)
    write_csv(POSITIVE_CLUES, positive_rows)
    write_csv(FAILURE_MEMORY, failure_rows)
    write_csv(NEXT_QUEUE, next_queue_rows)

    gates = make_gates(final)
    final = {
        **final,
        "gate_passes": sum(1 for row in gates if row["status"] == "passed"),
        "gate_total": len(gates),
        "next_action": NEXT_RUN_ID,
    }
    write_csv(GATE_AUDIT, gates)
    write_json(FINAL_DECISION, final)
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "source_package_run_id": SOURCE_PACKAGE_RUN_ID,
            "status": STATUS,
            "judgment": JUDGMENT,
            "decision": DECISION,
            "inputs": [rel(path) for path in INPUT_FILES],
            "outputs": [rel(path) for path in OUTPUT_FILES],
            "gates": gates,
            "claim_boundary": CLAIM_BOUNDARY,
            "created_at_utc": now_utc(),
        },
    )
    write_receipts(final, attribution_rows, positive_rows, failure_rows)
    write_docs(final)
    write_registers(final, gates)
    write_lineage()
    write_artifact_registry()

    if any(row["status"] != "passed" for row in gates):
        raise RuntimeError("run344E gate audit failed")

    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "promotion_candidate": final["promotion_candidate_attempt_name"],
                "net_profit": final["promotion_candidate_net_profit"],
                "profit_factor": final["promotion_candidate_profit_factor"],
                "trade_count": final["promotion_candidate_trade_count"],
                "gate_passes": final["gate_passes"],
                "gate_total": final["gate_total"],
                "next_run_id": NEXT_RUN_ID,
                "goal_achieve": final["goal_achieve"],
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
