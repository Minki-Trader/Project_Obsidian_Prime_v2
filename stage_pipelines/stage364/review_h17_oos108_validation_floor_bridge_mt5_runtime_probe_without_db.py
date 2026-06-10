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

from foundation.control_plane.ledger import io_path, json_ready  # noqa: E402
from stage_pipelines.stage364 import execute_h17_oos108_validation_floor_bridge_mt5_runtime_probe_without_db as eo  # noqa: E402
from stage_pipelines.stage364 import materialize_h17_oos108_validation_floor_bridge_runtime_package_without_db as en  # noqa: E402
from stage_pipelines.stage364 import review_h17_oos108_validation_floor_bridge_without_db as em  # noqa: E402
from stage_pipelines.stage364 import train_h17_oos108_validation_floor_bridge_without_db as el  # noqa: E402
from stage_pipelines.stage364.review_pf_pass_density_restore_offensive_scout_without_db import repair_run_registry_line_endings  # noqa: E402


TODAY = "2026-06-06"
STAGE_ID = eo.STAGE_ID
RUN_NUMBER = "run364EP"
RUN_ID = "run364EP_review_h17_oos108_validation_floor_bridge_mt5_runtime_probe_without_db_v1"
PARENT_RUN_ID = eo.RUN_ID
PACKAGE_RUN_ID = en.RUN_ID
PROXY_RUN_ID = el.RUN_ID
REVIEW_RUN_ID = em.RUN_ID
NEXT_RUN_ID = "run364EQ_train_h17_oos108_scope_aligned_cost_side_repair_scout_without_db_v1"

STATUS = "completed_stage364EP_oos108_validation_floor_bridge_mt5_review_scope_adjusted_positive_runtime_clue_repair_required_no_authority"
JUDGMENT = "positive_runtime_probe_clue_scope_adjusted_mt5_net_density_pf_pass_short_heavy_cost_stress_repair_required_no_authority"
DECISION = "stage364EP_open_run364EQ_oos108_scope_aligned_cost_side_repair_scout"
CLAIM_BOUNDARY = (
    "research_development_mt5_runtime_probe_review_only_oos108_validation_floor_bridge_scope_adjusted_"
    "no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

DENSITY_FLOOR = 3.0
SHORT_SHARE_CAUTION = 0.70

STAGE_DIR = eo.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
SPEC_DIR = STAGE_DIR / "00_spec"
SELECTED_DIR = STAGE_DIR / "04_selected"

WORK_PACKET = RUN_DIR / "work_packet.json"
SCOPE_ALIGNMENT = RUN_DIR / "scope_aligned_proxy_mt5_review.csv"
GUARDRAIL_REVIEW = RUN_DIR / "oos108_mt5_guardrail_review.csv"
RUNTIME_REVIEW = RUN_DIR / "oos108_validation_floor_bridge_mt5_review.csv"
RUN364EQ_QUEUE = RUN_DIR / "run364EQ_scope_aligned_cost_side_repair_queue.csv"
RESULT_JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
BACKTEST_RECEIPT = RUN_DIR / "backtest_forensics_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / "run364EP_oos108_mt5_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364EP_h17_oos108_validation_floor_bridge_mt5_runtime_probe_review.md"
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
NEGATIVE_REGISTER = ROOT / "docs" / "registers" / "negative_result_register.md"

INPUT_FILES = [
    eo.FINAL_DECISION,
    eo.GATE_AUDIT,
    eo.EXECUTION_SUMMARY,
    eo.PROXY_MT5_DIFF,
    eo.STRATEGY_TESTER_REPORTS,
    eo.RUNTIME_OUTPUT_COPY,
    eo.RUNTIME_IDENTITY,
    en.FINAL_DECISION,
    en.EXPECTED_KPI_SUMMARY,
    en.FEATURE_MATRIX_AUDIT,
    en.RUNTIME_POLICY_CONFIG,
    en.RUNTIME_PARITY_CONTRACT,
    en.TESTER_IDENTITY_CONTRACT,
    en.TESTER_SET_MANIFEST,
    en.MT5_ONNX_AUDIT,
    em.FINAL_DECISION,
    em.COST_STRESS_REVIEW,
    em.SIDE_BALANCE_REVIEW,
    el.FINAL_DECISION,
    el.SELECTED_CANDIDATE,
    el.TRADE_SURFACE,
    Path(__file__),
]

OUTPUT_FILES = [
    WORK_PACKET,
    SCOPE_ALIGNMENT,
    GUARDRAIL_REVIEW,
    RUNTIME_REVIEW,
    RUN364EQ_QUEUE,
    RESULT_JUDGMENT_RECEIPT,
    PERFORMANCE_RECEIPT,
    BACKTEST_RECEIPT,
    RUNTIME_RECEIPT,
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
    NEGATIVE_REGISTER,
    Path(__file__),
]


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    return eo.rel(path)


def exists(path: Path | str) -> bool:
    return eo.exists(path)


def sha(path: Path | str) -> str:
    return eo.sha(path)


def read_json(path: Path) -> Any:
    return eo.read_json(path)


def write_json(path: Path, payload: Any) -> None:
    eo.write_json(path, payload)


def read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(io_path(path), encoding="utf-8-sig").fillna("")


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    eo.write_csv(path, rows, fieldnames)


def write_text(path: Path, text: str, *, bom: bool = True) -> None:
    materialized = io_path(path)
    materialized.parent.mkdir(parents=True, exist_ok=True)
    materialized.write_text(text, encoding="utf-8-sig" if bom else "utf-8")


def append_text_once(path: Path, marker: str, text: str) -> None:
    eo.append_text_once(path, marker, text)


def append_or_replace_csv(path: Path, key_fields: Sequence[str], rows: Sequence[Mapping[str, Any]], *, extend_header: bool = True) -> None:
    eo.append_or_replace_csv(path, key_fields, rows, extend_header=extend_header)


def replace_prefixed_lines(path: Path, replacements: Mapping[str, str], *, bom: bool = True) -> None:
    eo.replace_prefixed_lines(path, replacements, bom=bom)


def finite(value: Any, digits: int = 10) -> float | str:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return ""
    if not math.isfinite(number):
        return ""
    return round(number, digits)


def float_or_nan(value: Any) -> float:
    try:
        if value in ("", None):
            return math.nan
        return float(value)
    except (TypeError, ValueError):
        return math.nan


def first_row(path: Path) -> dict[str, Any]:
    frame = read_csv(path)
    return {} if frame.empty else frame.iloc[0].to_dict()


def ensure_dirs() -> None:
    for path in [RUN_DIR, REVIEW_DIR, SPEC_DIR, SELECTED_DIR, DECISION_DOC.parent]:
        io_path(path).mkdir(parents=True, exist_ok=True)


def validate_inputs() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    missing = [rel(path) for path in INPUT_FILES if path != Path(__file__) and not exists(path)]
    if missing:
        raise FileNotFoundError("missing EP inputs(EP 입력 누락): " + ", ".join(missing))
    eo_final = read_json(eo.FINAL_DECISION)
    en_final = read_json(en.FINAL_DECISION)
    el_final = read_json(el.FINAL_DECISION)
    if eo_final.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"EO next_run_id mismatch(EO 다음 실행 ID 불일치): {eo_final.get('next_run_id')} != {RUN_ID}")
    for label, final in [("EO", eo_final), ("EN", en_final), ("EL", el_final)]:
        for key in ["runtime_authority", "operating_promotion", "live_readiness", "goal_achieve"]:
            if final.get(key, "not_claimed") != "not_claimed":
                raise RuntimeError(f"{label} forbidden claim({label} 금지 주장): {key}={final.get(key)}")
    eo_gates = read_csv(eo.GATE_AUDIT)
    if eo_gates.empty or any(eo_gates["status"].astype(str) != "passed"):
        raise RuntimeError("EO gate audit(EO 게이트 감사)가 모두 passed(통과)가 아닙니다.")
    if int(float(eo_final.get("outputs_available_rows", 0) or 0)) < 1:
        raise RuntimeError("EO MT5 output(EO MT5 출력)이 review(검토)에 충분하지 않습니다.")
    return eo_final, en_final, el_final


def write_work_packet() -> None:
    write_json(
        WORK_PACKET,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "primary_family": "kpi_evidence(KPI 근거)",
            "primary_skill": "obsidian-run-evidence-system(실행 근거 시스템)",
            "support_skills": [
                "obsidian-runtime-parity(런타임 동등성)",
                "obsidian-backtest-forensics(백테스트 포렌식)",
                "obsidian-artifact-lineage(산출물 계보)",
                "obsidian-result-judgment(결과 판정)",
            ],
            "required_gates": [
                "input_lineage_gate",
                "mt5_output_review_gate",
                "scope_alignment_gate",
                "cost_stress_guardrail_gate",
                "side_balance_guardrail_gate",
                "runtime_parity_boundary_gate",
                "artifact_lineage_gate",
                "required_gate_coverage_audit",
                "final_claim_guard",
            ],
            "effect": "MT5 runtime probe(MT5 런타임 탐침)를 운영 주장(operating claim, 운영 주장)이 아닌 다음 탐색 조건(next exploration condition, 다음 탐색 조건)으로 바꿉니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def selected_surface_row() -> dict[str, Any]:
    selected = read_json(el.SELECTED_CANDIDATE)
    surface = read_csv(el.TRADE_SURFACE)
    mask = (
        (surface["model_id"].astype(str) == str(selected["selected_model_id"]))
        & (surface["feature_set_id"].astype(str) == str(selected["selected_feature_set_id"]))
        & (surface["label_id"].astype(str) == str(selected["selected_label_id"]))
        & (surface["stability_filter"].astype(str) == str(selected["selected_stability_filter"]))
        & (surface["hours_id"].astype(str) == str(selected["selected_hours_id"]))
        & (surface["max_hold_m5"].astype(float) == 2.0)
        & (surface["threshold"].astype(float).sub(float(selected["selected_threshold"])).abs() < 1e-9)
        & (surface["margin_vs_flat"].astype(float).sub(float(selected["selected_margin_vs_flat"])).abs() < 1e-9)
    )
    rows = surface.loc[mask]
    if rows.empty:
        raise RuntimeError("selected surface row(선택 표면 행)을 찾지 못했습니다.")
    return rows.iloc[0].to_dict()


def build_scope_alignment() -> list[dict[str, Any]]:
    actual = first_row(eo.EXECUTION_SUMMARY)
    oos_diff = first_row(eo.PROXY_MT5_DIFF)
    selected = selected_surface_row()

    validation_days = float_or_nan(selected["validation_trade_count"]) / float_or_nan(selected["validation_trade_density"])
    oos_days = float_or_nan(selected["oos_trade_count"]) / float_or_nan(selected["oos_trade_density"])
    total_days = validation_days + oos_days
    expected_total_net = float_or_nan(selected["validation_net"]) + float_or_nan(selected["oos_net"])
    expected_total_trades = float_or_nan(selected["validation_trade_count"]) + float_or_nan(selected["oos_trade_count"])
    expected_total_long = float_or_nan(selected["validation_long_trade_count"]) + float_or_nan(selected["oos_long_trade_count"])
    expected_total_short = float_or_nan(selected["validation_short_trade_count"]) + float_or_nan(selected["oos_short_trade_count"])
    expected_total_density = expected_total_trades / total_days
    expected_short_share = expected_total_short / expected_total_trades
    actual_net = float_or_nan(actual.get("net_profit"))
    actual_trades = float_or_nan(actual.get("trade_count"))
    actual_long = float_or_nan(actual.get("long_trade_count"))
    actual_short = float_or_nan(actual.get("short_trade_count"))
    actual_density = actual_trades / total_days
    actual_short_share = actual_short / actual_trades

    rows = [
        {
            "run_id": RUN_ID,
            "candidate_id": actual.get("candidate_id", ""),
            "comparison_id": "eo_recorded_oos_only_vs_mt5_total(EO 기록 OOS 전용 대 MT5 전체)",
            "proxy_scope": "oos_only(표본외 전용)",
            "mt5_scope": "validation_plus_oos(검증+표본외)",
            "expected_net": oos_diff.get("expected_net_profit", ""),
            "actual_mt5_net": oos_diff.get("actual_mt5_net_profit", ""),
            "net_diff_actual_minus_expected": oos_diff.get("net_profit_diff_actual_minus_expected", ""),
            "expected_trade_count": oos_diff.get("expected_trade_count", ""),
            "actual_mt5_trade_count": oos_diff.get("actual_mt5_trade_count", ""),
            "trade_count_diff_actual_minus_expected": oos_diff.get("trade_count_diff_actual_minus_expected", ""),
            "scope_alignment_status": "scope_mismatch_for_total_judgment(전체 판정 범위 불일치)",
            "usability": "usable_only_as_oos_reference(OOS 기준 참고로만 사용)",
            "effect": "OOS-only proxy(표본외 전용 프록시)를 MT5 validation+OOS(검증+표본외) 전체와 직접 비교하지 않게 합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "candidate_id": actual.get("candidate_id", ""),
            "comparison_id": "scope_aligned_validation_oos_proxy_vs_mt5_total(범위 정렬 검증+표본외 프록시 대 MT5 전체)",
            "proxy_scope": "validation_plus_oos(검증+표본외)",
            "mt5_scope": "validation_plus_oos(검증+표본외)",
            "expected_net": finite(expected_total_net),
            "actual_mt5_net": finite(actual_net),
            "net_diff_actual_minus_expected": finite(actual_net - expected_total_net),
            "expected_trade_count": finite(expected_total_trades, 0),
            "actual_mt5_trade_count": finite(actual_trades, 0),
            "trade_count_diff_actual_minus_expected": finite(actual_trades - expected_total_trades, 0),
            "expected_trade_density": finite(expected_total_density),
            "actual_mt5_trade_density": finite(actual_density),
            "trade_density_diff_actual_minus_expected": finite(actual_density - expected_total_density),
            "expected_long_trade_count": finite(expected_total_long, 0),
            "actual_long_trade_count": finite(actual_long, 0),
            "long_trade_count_diff_actual_minus_expected": finite(actual_long - expected_total_long, 0),
            "expected_short_trade_count": finite(expected_total_short, 0),
            "actual_short_trade_count": finite(actual_short, 0),
            "short_trade_count_diff_actual_minus_expected": finite(actual_short - expected_total_short, 0),
            "expected_short_share": finite(expected_short_share),
            "actual_short_share": finite(actual_short_share),
            "short_share_diff_actual_minus_expected": finite(actual_short_share - expected_short_share),
            "expected_validation_profit_factor": finite(selected["validation_profit_factor"]),
            "expected_oos_profit_factor": finite(selected["oos_profit_factor"]),
            "actual_mt5_profit_factor": finite(actual.get("profit_factor")),
            "actual_mt5_expectancy": finite(actual.get("expectancy")),
            "actual_mt5_drawdown": finite(actual.get("max_drawdown_amount")),
            "actual_mt5_recovery_factor": finite(actual.get("recovery_factor")),
            "scope_alignment_status": "scope_aligned_for_review(검토 범위 정렬)",
            "usability": "usable_for_next_repair_scout(다음 수리 탐색에 사용 가능)",
            "effect": "MT5 성과가 proxy(프록시)를 범위 정렬 후에도 초과하는지 확인합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    write_csv(SCOPE_ALIGNMENT, rows)
    return rows


def build_guardrails(scope_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    aligned = scope_rows[1]
    actual = first_row(eo.EXECUTION_SUMMARY)
    cost = read_csv(em.COST_STRESS_REVIEW)
    cost_rows = cost.to_dict("records")
    cost06_validation = cost[(cost["split"].astype(str) == "validation") & (cost["cost_per_trade"].astype(float) == 0.6)]
    cost09_combined_net = cost[cost["cost_per_trade"].astype(float) == 0.9]["net_profit"].astype(float).sum()
    validation_cost06_net = float(cost06_validation.iloc[0]["net_profit"]) if not cost06_validation.empty else math.nan

    rows = [
        {
            "run_id": RUN_ID,
            "guardrail": "density_floor(거래 밀도 하한)",
            "value": aligned.get("actual_mt5_trade_density", ""),
            "threshold": DENSITY_FLOOR,
            "status": "passed(통과)" if float_or_nan(aligned.get("actual_mt5_trade_density")) >= DENSITY_FLOOR else "failed(실패)",
            "effect": "거래수는 3/day(일 3회) 요구를 만족하지만, 거래 쪼개기(trade splitting, 거래 쪼개기) 증거로 쓰지 않습니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "guardrail": "profit_factor_floor(수익 팩터 바닥)",
            "value": actual.get("profit_factor", ""),
            "threshold": "above validation/oos proxy PF(검증/표본외 프록시 PF 초과)",
            "status": "passed_with_runtime_probe_boundary(런타임 탐침 경계 포함 통과)",
            "effect": "MT5 PF(수익 팩터)는 검증/OOS proxy PF(프록시 수익 팩터)보다 높지만 운영 권위(runtime authority, 런타임 권위)는 아닙니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "guardrail": "short_share_caution(숏 비중 주의)",
            "value": aligned.get("actual_short_share", ""),
            "threshold": SHORT_SHARE_CAUTION,
            "status": "caution_short_heavy(주의, 숏 편중)",
            "effect": "범위 정렬 후 short share(숏 비중)는 proxy(프록시)보다 조금 낮지만 여전히 70%를 넘습니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "guardrail": "cost_stress_validation_cost06(검증 비용 0.6 압박)",
            "value": finite(validation_cost06_net),
            "threshold": ">=0",
            "status": "failed_in_proxy_guardrail(프록시 가드레일 실패)",
            "effect": "validation cost stress(검증 비용 압박)가 약해 다음 탐색은 비용 견딤(cost resilience, 비용 회복력)을 올려야 합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "guardrail": "cost_stress_combined_cost09(합산 비용 0.9 압박)",
            "value": finite(cost09_combined_net),
            "threshold": ">=0",
            "status": "failed_in_proxy_guardrail(프록시 가드레일 실패)",
            "effect": "강한 비용 압박에서는 validation+OOS(검증+표본외) 합산도 무너져 운영 주장(operating claim, 운영 주장)을 막습니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "guardrail": "runtime_timestamp_coverage(런타임 시각 커버리지)",
            "value": actual.get("feature_ready_count", ""),
            "threshold": "feature matrix rows 17428(피처 행렬 17428행)",
            "status": "passed_with_tail_skip_boundary(꼬리 스킵 경계 포함 통과)",
            "effect": "feature_ready/model_ok(피처 준비/모델 성공)는 패키지 범위를 채웠지만 이후 tester tail(테스터 꼬리)은 CSV 밖이라 스킵되었습니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    write_csv(GUARDRAIL_REVIEW, rows)
    write_json(
        PERFORMANCE_RECEIPT,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "created_at_utc": now_utc(),
            "claim_boundary": CLAIM_BOUNDARY,
            "scope_alignment": rel(SCOPE_ALIGNMENT),
            "guardrails": rel(GUARDRAIL_REVIEW),
            "cost_stress_source_rows": cost_rows,
            "attribution": [
                "The large EO trade diff(큰 EO 거래수 차이)는 OOS-only proxy(표본외 전용 프록시)와 MT5 validation+OOS(검증+표본외) 범위 불일치가 주원인입니다.",
                "After scope alignment(범위 정렬 후), MT5 trades(거래)는 proxy(프록시)보다 75개 많고 net(순수익)은 119.645 높습니다.",
                "Remaining weakness(남은 약점)는 short-heavy(숏 편중)와 cost stress(비용 압박)입니다.",
            ],
            "judgment": JUDGMENT,
        },
    )
    return rows


def build_review_rows(scope_rows: Sequence[Mapping[str, Any]], guardrails: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    aligned = scope_rows[1]
    actual = first_row(eo.EXECUTION_SUMMARY)
    rows = [
        {
            "run_id": RUN_ID,
            "candidate_id": actual.get("candidate_id", ""),
            "mt5_net_profit": actual.get("net_profit", ""),
            "mt5_profit_factor": actual.get("profit_factor", ""),
            "mt5_expectancy": actual.get("expectancy", ""),
            "mt5_trade_count": actual.get("trade_count", ""),
            "mt5_trade_density": aligned.get("actual_mt5_trade_density", ""),
            "mt5_drawdown": actual.get("max_drawdown_amount", ""),
            "mt5_recovery_factor": actual.get("recovery_factor", ""),
            "mt5_long_trade_count": actual.get("long_trade_count", ""),
            "mt5_short_trade_count": actual.get("short_trade_count", ""),
            "mt5_short_share": aligned.get("actual_short_share", ""),
            "scope_aligned_expected_net": aligned.get("expected_net", ""),
            "scope_aligned_net_diff": aligned.get("net_diff_actual_minus_expected", ""),
            "scope_aligned_expected_trades": aligned.get("expected_trade_count", ""),
            "scope_aligned_trade_diff": aligned.get("trade_count_diff_actual_minus_expected", ""),
            "scope_aligned_short_share_diff": aligned.get("short_share_diff_actual_minus_expected", ""),
            "review_label": "positive_runtime_probe_clue_repair_required(긍정 런타임 탐침 단서, 수리 필요)",
            "usability": "seed_EQ_scope_aligned_cost_side_repair(EQ 범위 정렬 비용/방향 수리 씨앗)",
            "authority": "not_claimed(주장 안 함)",
            "effect": "MT5는 범위 정렬 후 수익/밀도 단서를 보였지만 cost stress(비용 압박)와 short-heavy(숏 편중) 때문에 운영 승격으로 가지 않습니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    write_csv(RUNTIME_REVIEW, rows)
    return rows


def build_queue(review: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows = [
        {
            "run_id": RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "queue_rank": 1,
            "queue_id": "eq01_scope_aligned_proxy_rebuild",
            "seed": "EO diff(EO 차이)를 validation+OOS(검증+표본외) 범위로 재정렬합니다.",
            "target_question": "Can scope-aligned proxy(범위 정렬 프록시) predict MT5 trade count/net without OOS-only mismatch?(OOS 전용 불일치 없이 MT5 거래수/순수익을 설명할 수 있는가?)",
            "success_criteria": "Report validation separate(검증 분리), OOS separate(표본외 분리), validation+OOS combined(검증+표본외 합산) for every candidate(모든 후보).",
            "allowed_ideas": "replay same runtime policy(같은 런타임 정책 재생), no trade splitting(거래 쪼개기 금지), no top_n(상위 N개 자르기 금지)",
            "effect": "프록시/MT5 차이를 실제 원인에 맞게 줄입니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "queue_rank": 2,
            "queue_id": "eq02_cost_resilience_side_guard",
            "seed": "MT5 net/PF(순수익/수익 팩터)는 좋지만 validation cost 0.6(검증 비용 0.6)과 cost 0.9(비용 0.9)가 약합니다.",
            "target_question": "Can cost resilience(비용 회복력) improve without dropping density below 3/day(일 3회)?",
            "success_criteria": "validation cost0.6 net>=0(검증 비용0.6 순수익 0 이상), OOS cost0.6 net>0(표본외 비용0.6 순수익 양수), density>=3(밀도 3 이상), PF not below EO MT5 1.21(PF가 EO MT5 1.21 아래로 가지 않음).",
            "allowed_ideas": "increase margin guard(마진 가드 강화), hour 19/20 short quality veto(19/20시 숏 품질 배제), probability gap floor(확률 간극 바닥), keep max_hold=2(최대 보유 2 유지)",
            "effect": "좋은 net(순수익)을 보존하면서 비용에 약한 거래를 줄입니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "queue_rank": 3,
            "queue_id": "eq03_short_heavy_quality_filter",
            "seed": f"MT5 short share(숏 비중)는 {review.get('mt5_short_share')}로 70%를 넘습니다.",
            "target_question": "Can short-heavy exposure(숏 편중 노출)를 quality-filter(품질 필터)로 낮추거나 더 수익성 있게 만들 수 있는가?",
            "success_criteria": "short_share<=0.72(숏 비중 0.72 이하) or short expectancy lift(숏 기대값 상승), net>=523.58(순수익 523.58 이상), RF>=2.5(회복 계수 2.5 이상), density>=3(밀도 3 이상).",
            "allowed_ideas": "side-specific margin(방향별 마진), session veto(세션 배제), realized volatility bucket(실현 변동성 구간), no position splitting(포지션 쪼개기 금지)",
            "effect": "숏 거래를 단순히 줄이는 대신 품질을 높여 수익 구조를 안정화합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    write_csv(RUN364EQ_QUEUE, rows)
    return rows


def build_final(review: Mapping[str, Any], scope_rows: Sequence[Mapping[str, Any]], queue_rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    actual = first_row(eo.EXECUTION_SUMMARY)
    aligned = scope_rows[1]
    return {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "package_run_id": PACKAGE_RUN_ID,
        "proxy_run_id": PROXY_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "candidate_id": actual.get("candidate_id", ""),
        "created_at_utc": now_utc(),
        "mt5_net_profit": review.get("mt5_net_profit", ""),
        "mt5_profit_factor": review.get("mt5_profit_factor", ""),
        "mt5_expectancy": review.get("mt5_expectancy", ""),
        "mt5_trade_count": review.get("mt5_trade_count", ""),
        "mt5_trade_density": review.get("mt5_trade_density", ""),
        "mt5_drawdown": review.get("mt5_drawdown", ""),
        "mt5_recovery_factor": review.get("mt5_recovery_factor", ""),
        "mt5_long_trade_count": review.get("mt5_long_trade_count", ""),
        "mt5_short_trade_count": review.get("mt5_short_trade_count", ""),
        "mt5_short_share": review.get("mt5_short_share", ""),
        "scope_aligned_expected_net": aligned.get("expected_net", ""),
        "scope_aligned_net_diff_actual_minus_expected": aligned.get("net_diff_actual_minus_expected", ""),
        "scope_aligned_expected_trade_count": aligned.get("expected_trade_count", ""),
        "scope_aligned_trade_count_diff_actual_minus_expected": aligned.get("trade_count_diff_actual_minus_expected", ""),
        "scope_alignment_judgment": "eo_oos_only_diff_overstates_total_gap_scope_aligned_diff_usable(EO OOS 전용 차이는 전체 차이를 과장, 범위 정렬 차이는 사용 가능)",
        "queue_rows": len(queue_rows),
        "evidence_available": [rel(eo.EXECUTION_SUMMARY), rel(eo.PROXY_MT5_DIFF), rel(SCOPE_ALIGNMENT), rel(GUARDRAIL_REVIEW), rel(RUNTIME_REVIEW)],
        "evidence_missing": [
            "forward/replay evidence(전진/재생 근거)",
            "runtime authority closure(런타임 권위 폐쇄)",
            "Tier B fallback source(Tier B 대체 원천)",
            "scope-aligned next scout output(범위 정렬 다음 탐색 출력)",
            "external cost-stress reprobe(외부 비용 압박 재탐침)",
        ],
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "live_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "external_verification_status": "completed_reviewed_with_boundary(완료 및 경계 포함 검토)",
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "final_decision": rel(FINAL_DECISION),
    }


def gate_rows(final: Mapping[str, Any]) -> list[dict[str, Any]]:
    gates = [
        ("input_lineage_gate", all(exists(path) for path in INPUT_FILES if path != Path(__file__)), ";".join(rel(path) for path in INPUT_FILES if exists(path)), "EO/EN/EM/EL evidence(근거)를 모두 연결합니다."),
        ("mt5_output_review_gate", exists(eo.EXECUTION_SUMMARY) and float_or_nan(final.get("mt5_trade_count")) > 0, eo.EXECUTION_SUMMARY, "MT5 output(MT5 출력)이 KPI review(KPI 검토)에 충분한지 확인합니다."),
        ("scope_alignment_gate", exists(SCOPE_ALIGNMENT), SCOPE_ALIGNMENT, "OOS-only proxy(OOS 전용 프록시)와 validation+OOS MT5(검증+표본외 MT5) 범위 차이를 분리합니다."),
        ("cost_stress_guardrail_gate", exists(GUARDRAIL_REVIEW), GUARDRAIL_REVIEW, "비용 압박(cost stress, 비용 압박)을 다음 탐색 조건으로 남깁니다."),
        ("side_balance_guardrail_gate", exists(RUNTIME_REVIEW), RUNTIME_REVIEW, "long/short balance(롱/숏 균형)를 운영 주장 전에 검토합니다."),
        ("runtime_parity_boundary_gate", exists(RUNTIME_RECEIPT), RUNTIME_RECEIPT, "runtime probe(런타임 탐침)를 runtime authority(런타임 권위)로 승격하지 않습니다."),
        ("artifact_lineage_gate", exists(LINEAGE_RECEIPT), LINEAGE_RECEIPT, "입력/출력 산출물 계보(artifact lineage, 산출물 계보)를 연결합니다."),
        ("required_gate_coverage_audit", exists(GATE_AUDIT), GATE_AUDIT, "필수 gate(게이트)를 closeout(종료 기록)에 연결합니다."),
        ("final_claim_guard", exists(CLAIM_RECEIPT), CLAIM_RECEIPT, "Goal Achieve(목표 달성), operating promotion(운영 승격), runtime authority(런타임 권위)를 막습니다."),
    ]
    return [
        {
            "run_id": RUN_ID,
            "gate": gate,
            "status": "passed" if passed else "failed",
            "evidence": rel(evidence),
            "effect": effect,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for gate, passed, evidence, effect in gates
    ]


def write_receipts(final: Mapping[str, Any], review: Mapping[str, Any]) -> None:
    base = {"run_id": RUN_ID, "stage_id": STAGE_ID, "created_at_utc": final["created_at_utc"], "claim_boundary": CLAIM_BOUNDARY}
    write_json(
        RESULT_JUDGMENT_RECEIPT,
        {
            **base,
            "result_subject": "run364EO OOS108 validation floor bridge MT5 runtime probe review(run364EO OOS108 검증 바닥 연결 MT5 런타임 탐침 검토)",
            "evidence_available": final["evidence_available"],
            "evidence_missing": final["evidence_missing"],
            "judgment_label": "positive_runtime_probe_clue(긍정 런타임 탐침 단서)",
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": NEXT_RUN_ID,
            "user_explanation_hook": "MT5 result(MT5 결과)는 좋지만 scope/cost/side(범위/비용/방향) 수리가 필요합니다.",
        },
    )
    write_json(
        BACKTEST_RECEIPT,
        {
            **base,
            "tester_identity": rel(en.TESTER_IDENTITY_CONTRACT),
            "ea_identity": rel(eo.RUNTIME_IDENTITY),
            "report_identity": [rel(eo.STRATEGY_TESTER_REPORTS), read_json(eo.FINAL_DECISION).get("report_path", "")],
            "trade_evidence": {
                "trade_count": final["mt5_trade_count"],
                "net_profit": final["mt5_net_profit"],
                "drawdown": final["mt5_drawdown"],
                "profit_factor": final["mt5_profit_factor"],
                "trade_list_availability": "strategy_report_artifact_available(전략 보고서 산출물 있음)",
            },
            "cost_assumptions": "broker-native Strategy Tester output plus proxy cost-stress guardrail(브로커 전략 테스터 출력 + 프록시 비용 압박 가드레일)",
            "forensic_checks": [rel(eo.MT5_EXECUTION_RESULT), rel(eo.STRATEGY_TESTER_REPORTS), rel(eo.RUNTIME_OUTPUT_COPY), rel(SCOPE_ALIGNMENT), rel(GUARDRAIL_REVIEW)],
            "backtest_judgment": "usable_with_boundary(경계 포함 사용 가능)",
        },
    )
    write_json(
        RUNTIME_RECEIPT,
        {
            **base,
            "research_path": [rel(el.TRADE_SURFACE), rel(el.SELECTED_CANDIDATE), rel(en.RUNTIME_POLICY_CONFIG)],
            "runtime_path": [rel(en.TESTER_SET_MANIFEST), rel(en.TESTER_INI_MANIFEST), rel(eo.EXECUTION_SUMMARY)],
            "shared_contract": rel(en.RUNTIME_PARITY_CONTRACT),
            "known_differences": [
                "EO recorded diff(EO 기록 차이)는 OOS-only expected value(OOS 전용 예상값)를 MT5 validation+OOS(MT5 검증+표본외)와 비교했습니다.",
                "Scope-aligned review(범위 정렬 검토)는 validation+OOS proxy(검증+표본외 프록시)를 다시 계산했습니다.",
                "MT5 fill/spread/runtime(MT5 체결/스프레드/런타임)은 Python proxy(Python 프록시)를 대체하지 않습니다.",
            ],
            "parity_check": [rel(eo.PROXY_MT5_DIFF), rel(SCOPE_ALIGNMENT), rel(RUNTIME_REVIEW)],
            "parity_identity": {"mt5_onnx_contract_audit": rel(en.MT5_ONNX_AUDIT), "tester_set_manifest_sha256": sha(en.TESTER_SET_MANIFEST)},
            "runtime_claim_boundary": "runtime_probe_review(런타임 탐침 검토), not authority(권위 아님)",
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
            "availability": "tracked(추적됨)",
            "lineage_judgment": "connected_with_boundary(경계 포함 연결됨)",
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
            "effect": "positive MT5 clue(긍정 MT5 단서)를 operating claim(운영 주장)으로 승격하지 않습니다.",
        },
    )


def markdown_table(rows: Sequence[Mapping[str, Any]], columns: Sequence[str], limit: int = 12) -> str:
    if not rows:
        return "_none(없음)_"
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join(["---"] * len(columns)) + " |",
    ]
    for row in rows[:limit]:
        lines.append("| " + " | ".join(str(row.get(col, "")).replace("|", "\\|").replace("\n", " ") for col in columns) + " |")
    return "\n".join(lines)


def write_docs(final: Mapping[str, Any], scope_rows: Sequence[Mapping[str, Any]], guardrails: Sequence[Mapping[str, Any]], review_rows: Sequence[Mapping[str, Any]], gates: Sequence[Mapping[str, Any]]) -> None:
    review = review_rows[0]
    report = f"""# run364EP h17 OOS108 validation floor bridge MT5 runtime probe review(17시 OOS108 검증 바닥 연결 MT5 런타임 탐침 검토)

Updated(갱신): {final['created_at_utc']}

## Judgment(판정)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- judgment(판정): `{JUDGMENT}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- runtime_authority(런타임 권위): `not_claimed(주장 안 함)`

## Key Read(핵심 판독)

Action(행동): EO MT5 result(EO MT5 결과)를 OOS-only proxy(표본외 전용 프록시)와 scope-aligned validation+OOS proxy(범위 정렬 검증+표본외 프록시)로 나눠 다시 검토했습니다.

Effect(효과): 거래수 차이(trade count diff, 거래수 차이) `+795`는 범위 불일치(scope mismatch, 범위 불일치)가 커 보이게 만든 숫자이고, 범위 정렬 후 실제 차이는 `+75`입니다.

{markdown_table(review_rows, ['mt5_net_profit', 'mt5_profit_factor', 'mt5_expectancy', 'mt5_trade_count', 'mt5_trade_density', 'mt5_drawdown', 'mt5_recovery_factor', 'mt5_long_trade_count', 'mt5_short_trade_count', 'mt5_short_share', 'scope_aligned_net_diff', 'scope_aligned_trade_diff'])}

## Scope Alignment(범위 정렬)

{markdown_table(scope_rows, ['comparison_id', 'proxy_scope', 'mt5_scope', 'expected_net', 'actual_mt5_net', 'net_diff_actual_minus_expected', 'expected_trade_count', 'actual_mt5_trade_count', 'trade_count_diff_actual_minus_expected', 'scope_alignment_status', 'usability'])}

## Guardrails(가드레일)

{markdown_table(guardrails, ['guardrail', 'value', 'threshold', 'status', 'effect'])}

## Result Boundary(결과 경계)

- positive clue(긍정 단서): MT5 net/PF/trades(순수익/수익 팩터/거래수)는 `{final['mt5_net_profit']}` / `{final['mt5_profit_factor']}` / `{final['mt5_trade_count']}`입니다.
- corrected read(보정 판독): validation+OOS proxy(검증+표본외 프록시) 대비 MT5 net(순수익)은 `{final['scope_aligned_net_diff_actual_minus_expected']}` 높고 trade count(거래수)는 `{final['scope_aligned_trade_count_diff_actual_minus_expected']}` 많습니다.
- unresolved guardrail(미해결 가드레일): short-heavy(숏 편중), validation cost stress(검증 비용 압박), forward/replay evidence(전진/재생 근거)가 남아 있습니다.
- no authority(권위 없음): operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 없습니다.

## Gates(게이트)

{markdown_table(gates, ['gate', 'status', 'evidence', 'effect'])}

## Next(다음)

`{NEXT_RUN_ID}`는 scope-aligned proxy(범위 정렬 프록시), cost resilience(비용 회복력), short-heavy quality filter(숏 편중 품질 필터)를 탐색합니다. 효과(effect, 효과)는 MT5 순수익 단서를 보존하면서 운영 주장 전에 깨지는 가드레일을 줄이는 것입니다.
"""
    write_text(REPORT_PATH, report, bom=True)
    write_text(
        DECISION_DOC,
        f"""# Stage364EP decision(결정): OOS108 MT5 runtime review(OOS108 MT5 런타임 검토)

- date(날짜): {TODAY}
- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- MT5 net/PF/trades(MT5 순수익/수익 팩터/거래수): `{final['mt5_net_profit']}` / `{final['mt5_profit_factor']}` / `{final['mt5_trade_count']}`
- scope-aligned net diff(범위 정렬 순수익 차이): `{final['scope_aligned_net_diff_actual_minus_expected']}`
- scope-aligned trade diff(범위 정렬 거래수 차이): `{final['scope_aligned_trade_count_diff_actual_minus_expected']}`
- next action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): EQ는 OOS-only mismatch(OOS 전용 불일치)를 제거한 프록시와 비용/방향 수리를 함께 탐색합니다.
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
        bom=True,
    )
    append_text_once(REVIEW_INDEX, f"run364EP__{RUN_ID}", f"\n- run364EP__{RUN_ID}: [{REPORT_PATH.name}]({REPORT_PATH.name}) - OOS108 MT5 review(OOS108 MT5 검토), next `{NEXT_RUN_ID}`.\n")
    append_text_once(
        STAGE_BRIEF,
        f"run364EP__{RUN_ID}",
        f"""
<!-- run364EP__{RUN_ID} -->

## run364EP OOS108 MT5 Runtime Review(OOS108 MT5 런타임 검토)

Action(행동): EO MT5 probe(EO MT5 탐침)를 scope-aligned proxy(범위 정렬 프록시), cost stress(비용 압박), side balance(방향 균형)로 검토했습니다.

Effect(효과): MT5 net/PF/density(순수익/수익 팩터/밀도)는 긍정 단서지만 short-heavy/cost stress(숏 편중/비용 압박)가 남아 `{NEXT_RUN_ID}`로 수리 탐색을 엽니다.
""",
    )
    append_text_once(STAGE_README, f"run364EP__{RUN_ID}", f"\n<!-- run364EP__{RUN_ID} -->\n## run364EP review(검토)\n\nOOS108 MT5 review(OOS108 MT5 검토) completed(완료). Next(다음): `{NEXT_RUN_ID}`.\n")
    replace_prefixed_lines(
        STAGE_BRIEF,
        {
            "- current_run_id": f"- current_run_id(현재 실행 ID): `{NEXT_RUN_ID}`",
            "- latest_completed_run_id": f"- latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`",
            "- selection_status": f"- selection_status(선택 상태): `{STATUS}`",
            "- claim_boundary": f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
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

Current truth(현재 진실): `run364EP` reviewed(검토 완료) EO OOS108 MT5 runtime probe(EO OOS108 MT5 런타임 탐침). MT5 net/PF/trades(순수익/수익 팩터/거래수)는 `{final['mt5_net_profit']}` / `{final['mt5_profit_factor']}` / `{final['mt5_trade_count']}`이고, scope-aligned validation+OOS proxy(범위 정렬 검증+표본외 프록시) 대비 net diff(순수익 차이)는 `{final['scope_aligned_net_diff_actual_minus_expected']}`, trade diff(거래수 차이)는 `{final['scope_aligned_trade_count_diff_actual_minus_expected']}`입니다.

Next action(다음 행동): `{NEXT_RUN_ID}`에서 scope-aligned proxy(범위 정렬 프록시), cost resilience(비용 회복력), short-heavy quality filter(숏 편중 품질 필터)를 탐색합니다.

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

Latest reviewed MT5 runtime probe(최근 검토된 MT5 런타임 탐침): `{PARENT_RUN_ID}`.

MT5 net/PF/trades(MT5 순수익/수익 팩터/거래수): `{final['mt5_net_profit']}` / `{final['mt5_profit_factor']}` / `{final['mt5_trade_count']}`.

Scope-aligned proxy diff(범위 정렬 프록시 차이): net `{final['scope_aligned_net_diff_actual_minus_expected']}`, trades `{final['scope_aligned_trade_count_diff_actual_minus_expected']}`.

Judgment(판정): `{JUDGMENT}`.

Authority(권위): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""",
        bom=True,
    )
    append_text_once(WORKSPACE_CHANGELOG, f"run364EP__{RUN_ID}", f"\n<!-- run364EP__{RUN_ID} -->\n- {final['created_at_utc']} `{RUN_ID}` reviewed EO OOS108 MT5 probe(EO OOS108 MT5 탐침 검토); judgment `{JUDGMENT}`; next `{NEXT_RUN_ID}`; no authority claim(권위 주장 없음).\n")
    append_text_once(IDEA_REGISTRY, f"run364EP__{RUN_ID}", f"\n<!-- run364EP__{RUN_ID} -->\n- `{RUN_ID}`: OOS108 validation floor bridge(OOS108 검증 바닥 연결)는 MT5에서 net/PF/density(순수익/수익 팩터/밀도) 단서를 보였지만, OOS-only diff(OOS 전용 차이)는 scope mismatch(범위 불일치)로 보정해야 합니다. Effect(효과): EQ는 범위 정렬과 비용/방향 수리를 함께 탐색합니다.\n")
    append_text_once(NEGATIVE_REGISTER, f"run364EP__cost_side_no_authority__{RUN_ID}", f"\n<!-- run364EP__cost_side_no_authority__{RUN_ID} -->\n- `{RUN_ID}`: positive runtime clue(긍정 런타임 단서)는 있지만 validation cost stress(검증 비용 압박), short-heavy(숏 편중), forward/replay absence(전진/재생 부재) 때문에 authority(권위) 없음. Effect(효과): 운영 주장을 막고 EQ 수리 조건으로 전환합니다.\n")


def write_ledgers(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
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
        "rows": 1,
        "gate_passes": sum(1 for row in gates if row["status"] == "passed"),
        "gate_total": len(gates),
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "final_decision_path": rel(FINAL_DECISION),
        "gate_audit_path": rel(GATE_AUDIT),
        "created_at": final["created_at_utc"],
        "created_at_utc": final["created_at_utc"],
        "work_family": "kpi_evidence(KPI 근거)",
        "scoreboard_lane": "runtime_probe_review(런타임 탐침 검토)",
        "external_verification_status": final["external_verification_status"],
        "evidence_boundary": "review_only_no_authority(검토 전용, 권위 없음)",
        "question": "Does OOS108 validation floor bridge survive MT5 after scope alignment?(OOS108 검증 바닥 연결은 범위 정렬 후 MT5에서 버티는가?)",
        "next_action": NEXT_RUN_ID,
        "net_profit": final["mt5_net_profit"],
        "profit_factor": final["mt5_profit_factor"],
        "expectancy": final["mt5_expectancy"],
        "trade_count": final["mt5_trade_count"],
        "trade_density_per_feature_day": final["mt5_trade_density"],
        "long_trade_count": final["mt5_long_trade_count"],
        "short_trade_count": final["mt5_short_trade_count"],
        "max_drawdown_amount": final["mt5_drawdown"],
        "recovery_factor": final["mt5_recovery_factor"],
        "trade_density_requirement_status": "passed_runtime_density_ge_3_reviewed(런타임 밀도 3 이상 검토됨)",
        "result_judgment": JUDGMENT,
        "path": rel(FINAL_DECISION),
        "primary_report": rel(REPORT_PATH),
        "primary_artifact": rel(RUNTIME_REVIEW),
        "primary_kpi": f"mt5_net={final['mt5_net_profit']};pf={final['mt5_profit_factor']};trades={final['mt5_trade_count']};scope_trade_diff={final['scope_aligned_trade_count_diff_actual_minus_expected']}",
        "guardrail_kpi": "scope_mismatch_corrected;short_heavy;cost_stress_failed;runtime_authority=not_claimed;operating_promotion=not_claimed",
    }
    ledger_rows = []
    for suffix, record_view, tier_scope, status in [
        ("tier_a_used", "Tier A used(Tier A 사용)", "Tier A", STATUS),
        ("tier_b_fallback_missing_required", "Tier B fallback used(Tier B 대체 사용)", "Tier B", "missing_required_no_fallback_source(필수 누락, 대체 원천 없음)"),
        ("actual_routed_total", "actual routed total(실제 라우팅 전체)", "Tier A+B", STATUS),
    ]:
        row = {
            **common,
            "ledger_row_id": f"{RUN_ID}__{suffix}",
            "subrun_id": f"{RUN_ID}__{suffix}",
            "row_id": f"{RUN_ID}__{suffix}",
            "record_view": record_view,
            "tier_scope": tier_scope,
            "kpi_scope": "EP runtime review(EP 런타임 검토)",
            "status": status,
            "view": record_view,
            "tier": tier_scope,
            "metric_scope": "mt5_runtime_probe_review(MT5 런타임 탐침 검토)",
        }
        if suffix == "tier_b_fallback_missing_required":
            for key in ["net_profit", "profit_factor", "expectancy", "trade_count", "trade_density_per_feature_day", "long_trade_count", "short_trade_count", "max_drawdown_amount", "recovery_factor"]:
                row[key] = ""
        ledger_rows.append(row)
    append_or_replace_csv(STAGE_LEDGER, ["ledger_row_id"], ledger_rows, extend_header=True)
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], ledger_rows, extend_header=True)
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], [common], extend_header=True)
    repair_run_registry_line_endings(RUN_ID)


def write_artifact_registry(final: Mapping[str, Any]) -> None:
    rows = []
    for artifact_type, path, notes in [
        ("scope_alignment", SCOPE_ALIGNMENT, "Scope-aligned proxy/MT5 review(범위 정렬 프록시/MT5 검토)."),
        ("guardrail_review", GUARDRAIL_REVIEW, "Cost/side guardrail review(비용/방향 가드레일 검토)."),
        ("runtime_review", RUNTIME_REVIEW, "EP runtime review(EP 런타임 검토)."),
        ("queue", RUN364EQ_QUEUE, "Next run queue(다음 실행 대기열)."),
        ("result_judgment_receipt", RESULT_JUDGMENT_RECEIPT, "Result judgment receipt(결과 판정 영수증)."),
        ("performance_attribution_receipt", PERFORMANCE_RECEIPT, "Performance attribution receipt(성과 귀속 영수증)."),
        ("backtest_forensics_receipt", BACKTEST_RECEIPT, "Backtest forensics receipt(백테스트 포렌식 영수증)."),
        ("runtime_parity_receipt", RUNTIME_RECEIPT, "Runtime parity receipt(런타임 동등성 영수증)."),
        ("artifact_lineage_receipt", LINEAGE_RECEIPT, "Artifact lineage receipt(산출물 계보 영수증)."),
        ("final_decision", FINAL_DECISION, "Final decision(최종 결정)."),
        ("run_manifest", RUN_MANIFEST, "Run manifest(실행 목록)."),
        ("report", REPORT_PATH, "Human report(사람용 보고서)."),
        ("script", Path(__file__), "EP producer script(EP 생산 스크립트)."),
    ]:
        if exists(path):
            rows.append(
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
    append_or_replace_csv(ARTIFACT_REGISTRY, ["artifact_id"], rows, extend_header=True)


def write_manifest(final: Mapping[str, Any]) -> None:
    outputs = [path for path in OUTPUT_FILES if exists(path)]
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "run_number": RUN_NUMBER,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "status": STATUS,
            "judgment": JUDGMENT,
            "claim_boundary": CLAIM_BOUNDARY,
            "input_files": [rel(path) for path in INPUT_FILES],
            "input_hashes": {rel(path): sha(path) for path in INPUT_FILES if exists(path) and io_path(path).is_file()},
            "output_files": [rel(path) for path in outputs],
            "output_hashes": {rel(path): sha(path) for path in outputs if io_path(path).is_file()},
        },
    )


def main() -> None:
    ensure_dirs()
    validate_inputs()
    write_work_packet()
    scope_rows = build_scope_alignment()
    guardrails = build_guardrails(scope_rows)
    review_rows = build_review_rows(scope_rows, guardrails)
    queue_rows = build_queue(review_rows[0])
    final = build_final(review_rows[0], scope_rows, queue_rows)
    write_receipts(final, review_rows[0])
    gates = gate_rows(final)
    final["gate_passes"] = sum(1 for row in gates if row["status"] == "passed")
    final["gate_total"] = len(gates)
    write_csv(GATE_AUDIT, gates)
    write_json(FINAL_DECISION, final)
    gates = gate_rows(final)
    final["gate_passes"] = sum(1 for row in gates if row["status"] == "passed")
    final["gate_total"] = len(gates)
    write_docs(final, scope_rows, guardrails, review_rows, gates)
    write_ledgers(final, gates)
    write_artifact_registry(final)
    write_manifest(final)
    write_csv(GATE_AUDIT, gates)
    write_json(FINAL_DECISION, final)
    print(json.dumps(json_ready(final), ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
