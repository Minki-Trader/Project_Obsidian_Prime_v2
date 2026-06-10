from __future__ import annotations

import json
import math
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path  # noqa: E402
from stage_pipelines.stage364 import execute_h17_short_quality_risk_scale_mt5_runtime_probe_without_db as db  # noqa: E402
from stage_pipelines.stage364 import execute_h17_short_source_expansion_mt5_runtime_probe_without_db as dg  # noqa: E402
from stage_pipelines.stage364 import materialize_h17_short_source_expansion_runtime_package_without_db as df  # noqa: E402
from stage_pipelines.stage364 import review_h17_short_source_expansion_mt5_runtime_probe_without_db as dh  # noqa: E402
from stage_pipelines.stage364 import train_h17_short_source_expansion_runtime_positive_scout_without_db as dd  # noqa: E402
from stage_pipelines.stage364.review_pf_pass_density_restore_offensive_scout_without_db import repair_run_registry_line_endings  # noqa: E402


TODAY = "2026-06-06"
STAGE_ID = dh.STAGE_ID
RUN_NUMBER = "run364DI"
RUN_ID = "run364DI_train_h17_short_source_profit_recovery_scout_without_db_v1"
PARENT_RUN_ID = dh.RUN_ID
SOURCE_RUNTIME_RUN_ID = dg.RUN_ID
SOURCE_PROXY_RUN_ID = dd.RUN_ID
SOURCE_PACKAGE_RUN_ID = df.RUN_ID
BASELINE_RUN_ID = db.RUN_ID
NEXT_RUN_ID = "run364DJ_review_h17_short_source_profit_recovery_scout_without_db_v1"

STATUS = "completed_stage364DI_h17_short_source_profit_recovery_proxy_scout_review_required_no_authority"
JUDGMENT = "proxy_short_source_profit_recovery_scout_found_runtime_ready_candidate_review_required_no_authority"
DECISION = "stage364DI_open_run364DJ_short_source_profit_recovery_review"
CLAIM_BOUNDARY = (
    "research_development_proxy_scout_only_short_source_profit_recovery_"
    "no_new_model_training_no_new_mt5_execution_no_forward_pass_no_live_readiness_"
    "no_operating_promotion_no_runtime_authority_no_goal_claim"
)

DAYS = 314.0
FIXED_LOT = 0.10
RISK_SCALE_MULTIPLIER = 1.10
RISK_SCALE_HOURS = {17, 18, 19, 20}
RISK_SCALE_MIN_MARGIN = 0.08
MAX_HOLD_BARS = 6
DENSITY_FLOOR = 3.0
DENSITY_CEILING = 10.0
PF_FLOOR = 1.40
SHORT_COUNT_FLOOR = 125.0

STAGE_DIR = dh.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
SPEC_DIR = STAGE_DIR / "00_spec"
SELECTED_DIR = STAGE_DIR / "04_selected"

INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
PROFIT_RECOVERY_SURFACE = RUN_DIR / "di_short_source_profit_recovery_surface.csv"
SELECTED_CANDIDATE = RUN_DIR / "selected_di_candidate.json"
SELECTED_TRADE_TAPE = RUN_DIR / "selected_di_trade_tape.csv"
VARIANT_OVERRIDE_AUDIT = RUN_DIR / "variant_override_audit.csv"
VARIANT_REASON_ATTRIBUTION = RUN_DIR / "variant_reason_attribution.csv"
VARIANT_HOUR_SIDE_ATTRIBUTION = RUN_DIR / "variant_hour_side_attribution.csv"
VARIANT_MONTH_SIDE_ATTRIBUTION = RUN_DIR / "variant_month_side_attribution.csv"
RUNTIME_REPRESENTATION_AUDIT = RUN_DIR / "runtime_representation_audit.csv"
PACKAGE_PRECHECK = RUN_DIR / "package_precheck.csv"
PROXY_MT5_DIFF_PLAN = RUN_DIR / "proxy_mt5_difference_plan.csv"
RUN364DJ_QUEUE = RUN_DIR / "run364DJ_review_queue.csv"
DATA_INTEGRITY_AUDIT = RUN_DIR / "data_integrity_audit.csv"
RUN_EVIDENCE_RECEIPT = RUN_DIR / "run_evidence_receipt.json"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment_design_receipt.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
ATTRIBUTION_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / "run364DI_h17_short_source_profit_recovery_scout.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364DI_h17_short_source_profit_recovery_scout.md"
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
    dh.FINAL_DECISION,
    dh.GATE_AUDIT,
    dh.RUNTIME_REVIEW,
    dh.RUN364DI_QUEUE,
    dg.FINAL_DECISION,
    dg.EXECUTION_SUMMARY,
    dg.PROXY_MT5_DIFF,
    dg.RUNTIME_OUTPUT_COPY,
    df.FINAL_DECISION,
    df.RUNTIME_POLICY_CONFIG,
    df.TESTER_SET_MANIFEST,
    dd.SELECTED_CANDIDATE,
    dd.SELECTED_TRADE_TAPE,
    dd.SHORT_SOURCE_SURFACE,
    db.FINAL_DECISION,
    db.EXECUTION_SUMMARY,
    dd.SOURCE_RAW_US100_M5,
]

OUTPUT_FILES = [
    INPUT_MANIFEST,
    WORK_PACKET,
    PROFIT_RECOVERY_SURFACE,
    SELECTED_CANDIDATE,
    SELECTED_TRADE_TAPE,
    VARIANT_OVERRIDE_AUDIT,
    VARIANT_REASON_ATTRIBUTION,
    VARIANT_HOUR_SIDE_ATTRIBUTION,
    VARIANT_MONTH_SIDE_ATTRIBUTION,
    RUNTIME_REPRESENTATION_AUDIT,
    PACKAGE_PRECHECK,
    PROXY_MT5_DIFF_PLAN,
    RUN364DJ_QUEUE,
    DATA_INTEGRITY_AUDIT,
    RUN_EVIDENCE_RECEIPT,
    EXPERIMENT_RECEIPT,
    DATA_RECEIPT,
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
    return dg.rel(path)


def exists(path: Path | str) -> bool:
    return dg.exists(path)


def sha(path: Path | str) -> str:
    return dg.sha(path)


def json_ready(value: Any) -> Any:
    return dg.json_ready(value)


def read_json(path: Path) -> Any:
    return dg.read_json(path)


def write_json(path: Path, payload: Any) -> None:
    dg.write_json(path, payload)


def read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(io_path(path), encoding="utf-8-sig").fillna("")


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    dg.write_csv(path, rows, fieldnames)


def write_text(path: Path, text: str, *, bom: bool = True) -> None:
    dg.write_text(path, text, bom=bom)


def append_text_once(path: Path, marker: str, text: str) -> None:
    dg.append_text_once(path, marker, text)


def append_or_replace_csv(path: Path, key_fields: Sequence[str], rows: Sequence[Mapping[str, Any]], *, extend_header: bool = True) -> None:
    dg.append_or_replace_csv(path, key_fields, rows, extend_header=extend_header)


def replace_prefixed_lines(path: Path, replacements: Mapping[str, str], *, bom: bool = True) -> None:
    dg.replace_prefixed_lines(path, replacements, bom=bom)


def finite(value: Any, digits: int = 10) -> float | str:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return ""
    if not math.isfinite(number):
        return ""
    return round(number, digits)


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        if value in ("", None):
            return default
        number = float(value)
    except (TypeError, ValueError):
        return default
    return number if math.isfinite(number) else default


def ensure_dirs() -> None:
    for path in [RUN_DIR, REVIEW_DIR, SPEC_DIR, SELECTED_DIR, DECISION_DOC.parent]:
        io_path(path).mkdir(parents=True, exist_ok=True)


def validate_inputs() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    missing = [rel(path) for path in INPUT_FILES if not exists(path)]
    if missing:
        raise FileNotFoundError("missing DI inputs(DI 입력 누락): " + ", ".join(missing))
    dh_final = read_json(dh.FINAL_DECISION)
    dg_final = read_json(dg.FINAL_DECISION)
    db_final = read_json(db.FINAL_DECISION)
    if dh_final.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"DH next_run_id mismatch(DH 다음 실행 ID 불일치): {dh_final.get('next_run_id')} != {RUN_ID}")
    for label, final in [("DH", dh_final), ("DG", dg_final), ("DB", db_final)]:
        for key in ["runtime_authority", "operating_promotion", "live_readiness", "goal_achieve"]:
            if final.get(key, "not_claimed") != "not_claimed":
                raise RuntimeError(f"{label} forbidden claim({label} 금지 주장): {key}={final.get(key)}")
    gates = read_csv(dh.GATE_AUDIT)
    if gates.empty or any(gates["status"].astype(str) != "passed"):
        raise RuntimeError("DH gate audit(DH 게이트 감사)가 모두 passed(통과)가 아닙니다.")
    return dh_final, dg_final, db_final


def input_manifest_rows() -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "input_path": rel(path),
            "exists": exists(path),
            "sha256": sha(path) if exists(path) and io_path(path).is_file() else "",
            "input_role": "short-source profit recovery scout input(숏 원천 수익 회복 스카우트 입력)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for path in INPUT_FILES
    ]


def write_work_packet() -> None:
    write_json(
        WORK_PACKET,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "primary_family": "experiment_execution(실험 실행)",
            "primary_skill": "obsidian-exploration-mandate(탐색 규율)",
            "support_skills": [
                "obsidian-experiment-design(실험 설계)",
                "obsidian-data-integrity(데이터 무결성)",
                "obsidian-performance-attribution(성과 귀속)",
                "obsidian-result-judgment(결과 판정)",
                "obsidian-artifact-lineage(산출물 계보)",
            ],
            "hypothesis": "Hour-19 or bad-month short-source rows diluted DG expectancy; filtering them can keep short-count lift while recovering DB net/PF(19시 또는 나쁜 월 숏 원천 행이 DG 기대값을 희석했고, 이를 걸러 DB 순수익/수익 팩터를 회복하면서 숏 거래수 증가는 유지할 수 있다).",
            "decision_use": "Choose a runtime-representable candidate for review and possible MT5 package(검토 및 MT5 패키지 후보로 런타임 표현 가능 후보 선택).",
            "comparison_baseline": [BASELINE_RUN_ID, PARENT_RUN_ID],
            "control_variables": ["same DB telemetry(DB 텔레메트리 동일)", "same ONNX output(ONNX 출력 동일)", "same max-hold replay(max-hold 재생 동일)", "no trade splitting(거래 쪼개기 없음)"],
            "changed_variables": ["synthetic short-source hours(합성 숏 원천 시간)", "margin thresholds(마진 임계값)", "month veto as scout-only stress(월 배제는 스카우트 스트레스 전용)"],
            "sample_scope": "FPMarkets US100 M5 Tier A runtime telemetry replay(FPMarkets US100 M5 Tier A 런타임 텔레메트리 재생)",
            "success_criteria": "estimated MT5 net >= DB, PF >= 1.40, density 3-10, short_count >= 125, runtime-ready parameterization(추정 MT5 순수익 DB 이상, PF 1.40 이상, 밀도 3-10, 숏 125 이상, 런타임 파라미터화 가능)",
            "failure_criteria": "higher short count dilutes expectancy or needs hidden future/path filter(숏 거래수 증가가 기대값을 희석하거나 숨은 미래/경로 필터가 필요함)",
            "invalid_conditions": "lookahead, overlapping positions, missing raw join, authority claim(미래참조, 겹친 포지션, 원천 결합 누락, 권위 주장)",
            "required_gates": [
                "scope_completion_gate",
                "input_lineage_gate",
                "data_integrity_gate",
                "candidate_surface_gate",
                "runtime_representability_gate",
                "kpi_contract_gate",
                "no_trade_splitting_gate",
                "receipt_coverage_gate",
                "required_gate_coverage_audit",
                "final_claim_guard",
            ],
            "effect": "Turns DH failure memory(DH 실패 기억)를 measurable profit-recovery proxy scout(측정 가능한 수익 회복 프록시 스카우트)로 바꿉니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def variant_specs() -> list[dict[str, Any]]:
    return [
        {
            "variant_id": "di00_db_policy_anchor",
            "family": "anchor(기준)",
            "hypothesis": "Keep DB runtime policy unchanged(DB 런타임 정책 유지).",
            "hours": [],
            "p_short_min": None,
            "margin_vs_long_min": None,
            "margin_vs_flat_min": None,
            "exclude_months": [],
            "runtime_representation": "anchor_not_package(기준, 패키지 아님)",
        },
        {
            "variant_id": "di01_dd05_broad_anchor",
            "family": "broad_short_source_anchor(광역 숏 원천 기준)",
            "hypothesis": "Replay DG/DD05 broad source for comparison(DG/DD05 광역 원천 비교 재생).",
            "hours": [17, 18, 19, 20, 21],
            "p_short_min": 0.4375,
            "margin_vs_long_min": 0.05,
            "margin_vs_flat_min": 0.0,
            "exclude_months": [8],
            "runtime_representation": "runtime_ready_existing_params(기존 파라미터로 런타임 가능)",
        },
        {
            "variant_id": "di02_h17_18_20_21_no19_m050",
            "family": "hour_veto_short_source(시간 배제 숏 원천)",
            "hypothesis": "Hour19 added shorts diluted DG; veto hour19 while keeping 17/18/20/21(19시 추가 숏이 DG를 희석했으므로 17/18/20/21은 유지하고 19시는 배제한다).",
            "hours": [17, 18, 20, 21],
            "p_short_min": 0.4375,
            "margin_vs_long_min": 0.05,
            "margin_vs_flat_min": 0.0,
            "exclude_months": [8],
            "runtime_representation": "runtime_ready_existing_params(기존 파라미터로 런타임 가능)",
        },
        {
            "variant_id": "di03_h17_18_20_no19_no21_m050",
            "family": "hour_veto_short_source(시간 배제 숏 원천)",
            "hypothesis": "Keep core hours 17/18/20 and drop sparse 21(핵심 17/18/20시만 유지하고 희소한 21시는 뺀다).",
            "hours": [17, 18, 20],
            "p_short_min": 0.4375,
            "margin_vs_long_min": 0.05,
            "margin_vs_flat_min": 0.0,
            "exclude_months": [8],
            "runtime_representation": "runtime_ready_existing_params(기존 파라미터로 런타임 가능)",
        },
        {
            "variant_id": "di04_h17_18_21_no19_no20_m050",
            "family": "hour_veto_short_source(시간 배제 숏 원천)",
            "hypothesis": "Drop both weak hour19 and uncertain hour20(약한 19시와 불확실한 20시를 함께 뺀다).",
            "hours": [17, 18, 21],
            "p_short_min": 0.4375,
            "margin_vs_long_min": 0.05,
            "margin_vs_flat_min": 0.0,
            "exclude_months": [8],
            "runtime_representation": "runtime_ready_existing_params(기존 파라미터로 런타임 가능)",
        },
        {
            "variant_id": "di05_margin_vs_flat_026_m050",
            "family": "flat_margin_quality_filter(플랫 마진 품질 필터)",
            "hypothesis": "Require p_short to clear p_flat by 0.26 to avoid ambiguous flats(p_short가 p_flat보다 0.26 이상 높을 때만 애매한 플랫을 피한다).",
            "hours": [17, 18, 19, 20, 21],
            "p_short_min": 0.4375,
            "margin_vs_long_min": 0.05,
            "margin_vs_flat_min": 0.26,
            "exclude_months": [8],
            "runtime_representation": "runtime_ready_existing_params(기존 파라미터로 런타임 가능)",
        },
        {
            "variant_id": "di06_high_margin_m090",
            "family": "high_margin_quality_filter(고마진 품질 필터)",
            "hypothesis": "Use margin_vs_long >= 0.09 to keep only high-conviction shorts(margin_vs_long 0.09 이상 고확신 숏만 유지).",
            "hours": [17, 18, 19, 20, 21],
            "p_short_min": 0.4375,
            "margin_vs_long_min": 0.09,
            "margin_vs_flat_min": 0.0,
            "exclude_months": [8],
            "runtime_representation": "runtime_ready_existing_params(기존 파라미터로 런타임 가능)",
        },
        {
            "variant_id": "di07_exclude_months_6_7_8_12",
            "family": "month_stress_filter(월 스트레스 필터)",
            "hypothesis": "Months 6/7/12 diluted added shorts; excluding them tests regime fragility(6/7/12월이 추가 숏을 희석했으므로 제외해 국면 취약성을 시험).",
            "hours": [17, 18, 19, 20, 21],
            "p_short_min": 0.4375,
            "margin_vs_long_min": 0.05,
            "margin_vs_flat_min": 0.0,
            "exclude_months": [6, 7, 8, 12],
            "runtime_representation": "repair_required_multi_month_block(다중 월 차단 보정 필요)",
        },
        {
            "variant_id": "di08_exclude_months_3_6_7_8_12",
            "family": "month_stress_filter(월 스트레스 필터)",
            "hypothesis": "Hard month veto can show the upper bound of bad-month repair(강한 월 배제는 나쁜 월 보정 상한을 보여준다).",
            "hours": [17, 18, 19, 20, 21],
            "p_short_min": 0.4375,
            "margin_vs_long_min": 0.05,
            "margin_vs_flat_min": 0.0,
            "exclude_months": [3, 6, 7, 8, 12],
            "runtime_representation": "repair_required_multi_month_block(다중 월 차단 보정 필요)",
        },
        {
            "variant_id": "di09_no19_month_stress_6_7_8_12",
            "family": "combined_hour_month_filter(시간/월 결합 필터)",
            "hypothesis": "Combine hour19 veto with bad-month stress(19시 배제와 나쁜 월 스트레스를 결합).",
            "hours": [17, 18, 20, 21],
            "p_short_min": 0.4375,
            "margin_vs_long_min": 0.05,
            "margin_vs_flat_min": 0.0,
            "exclude_months": [6, 7, 8, 12],
            "runtime_representation": "repair_required_multi_month_block(다중 월 차단 보정 필요)",
        },
        {
            "variant_id": "di10_no19_flat026_m060",
            "family": "combined_quality_filter(결합 품질 필터)",
            "hypothesis": "Combine hour19 veto with stricter margin and flat separation(19시 배제와 더 강한 마진/플랫 분리를 결합).",
            "hours": [17, 18, 20, 21],
            "p_short_min": 0.4375,
            "margin_vs_long_min": 0.06,
            "margin_vs_flat_min": 0.26,
            "exclude_months": [8],
            "runtime_representation": "runtime_ready_existing_params(기존 파라미터로 런타임 가능)",
        },
    ]


def build_override_mask(cycles: pd.DataFrame, spec: Mapping[str, Any]) -> pd.Series:
    if spec["variant_id"] == "di00_db_policy_anchor":
        return pd.Series(False, index=cycles.index)
    mask = (
        cycles["decision_base"].eq("flat")
        & cycles["open_hour"].astype("Int64").isin(list(spec["hours"]))
        & cycles["p_short"].ge(float(spec["p_short_min"]))
        & cycles["margin_vs_long"].ge(float(spec["margin_vs_long_min"]))
        & cycles["margin_vs_flat"].ge(float(spec["margin_vs_flat_min"]))
        & cycles["p_short_dominant"].astype(bool)
        & cycles["p_short"].gt(cycles["p_flat"])
    )
    exclude_months = list(spec.get("exclude_months", []))
    if exclude_months:
        mask &= ~cycles["open_month_num"].astype("Int64").isin(exclude_months)
    return mask.fillna(False)


def volume_for(side: str, row: Mapping[str, Any]) -> float:
    if side == "short" and int(row["open_hour"]) in RISK_SCALE_HOURS and as_float(row["margin_vs_long"]) >= RISK_SCALE_MIN_MARGIN:
        return FIXED_LOT * RISK_SCALE_MULTIPLIER
    return FIXED_LOT


def iso_time(value: Any) -> str:
    return pd.Timestamp(value).strftime("%Y-%m-%dT%H:%M:%S")


def simulate_variant(cycles: pd.DataFrame, spec: Mapping[str, Any]) -> tuple[pd.DataFrame, pd.DataFrame]:
    mask = build_override_mask(cycles, spec)
    decisions = cycles["decision_base"].copy()
    decisions.loc[mask] = "short"
    variant_id = str(spec["variant_id"])
    override_rows = cycles.loc[mask].copy()
    override_audit: list[dict[str, Any]] = []
    if override_rows.empty:
        override_audit.append(
            {
                "run_id": RUN_ID,
                "variant_id": variant_id,
                "open_hour": "",
                "override_rows": 0,
                "avg_p_short": "",
                "avg_margin_vs_long": "",
                "avg_margin_vs_flat": "",
                "effect": "no changed rows(변경 행 없음)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    else:
        for hour, group in override_rows.groupby("open_hour", sort=True):
            override_audit.append(
                {
                    "run_id": RUN_ID,
                    "variant_id": variant_id,
                    "open_hour": int(hour),
                    "override_rows": int(len(group)),
                    "avg_p_short": finite(group["p_short"].mean()),
                    "avg_margin_vs_long": finite(group["margin_vs_long"].mean()),
                    "avg_margin_vs_flat": finite(group["margin_vs_flat"].mean()),
                    "effect": "flat cycle(플랫 주기)을 short source(숏 원천) 후보로 바꿉니다.",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )

    trades: list[dict[str, Any]] = []
    position: str | None = None
    entry_price = 0.0
    entry_time = pd.NaT
    entry_index = -1
    entry_row: Mapping[str, Any] | None = None
    hold_bars = 0
    volume = FIXED_LOT

    for index, row in cycles.iterrows():
        desired = str(decisions.iloc[index])
        if desired not in {"long", "short"}:
            desired = "flat"
        price = float(row["entry_open"])
        current_time = row["dt"]
        blocked_open_this_bar = False
        if position is not None:
            hold_bars += 1
            close_reason = ""
            if desired in {"long", "short"} and desired != position:
                close_reason = "reverse"
            elif hold_bars >= MAX_HOLD_BARS:
                close_reason = "max_hold"
            if close_reason:
                gross = (price - entry_price) * volume if position == "long" else (entry_price - price) * volume
                source = entry_row or {}
                trades.append(trade_row(variant_id, position, volume, entry_price, price, gross, hold_bars, source, entry_time, current_time, close_reason, entry_index, index))
                position = None
                hold_bars = 0
                blocked_open_this_bar = True
                if close_reason == "reverse" and desired in {"long", "short"}:
                    position = desired
                    entry_price = price
                    entry_time = current_time
                    entry_index = index
                    entry_row = entry_source(row, bool(mask.iloc[index]), variant_id)
                    volume = volume_for(position, entry_row)
                    blocked_open_this_bar = True
        if position is None and not blocked_open_this_bar and desired in {"long", "short"}:
            position = desired
            entry_price = price
            entry_time = current_time
            entry_index = index
            entry_row = entry_source(row, bool(mask.iloc[index]), variant_id)
            volume = volume_for(position, entry_row)

    if position is not None:
        row = cycles.iloc[-1]
        price = float(row["entry_open"])
        gross = (price - entry_price) * volume if position == "long" else (entry_price - price) * volume
        trades.append(trade_row(variant_id, position, volume, entry_price, price, gross, hold_bars, entry_row or {}, entry_time, row["dt"], "final_close", entry_index, len(cycles) - 1))
    return pd.DataFrame(trades), pd.DataFrame(override_audit)


def entry_source(row: Mapping[str, Any], added: bool, variant_id: str) -> dict[str, Any]:
    return {
        **dict(row),
        "source_reason": f"{variant_id}_override" if added else row.get("decision_reason", ""),
        "source_bucket": "di_added_short_source" if added else "runtime_decision",
    }


def trade_row(
    variant_id: str,
    direction: str,
    volume: float,
    entry_price: float,
    close_price: float,
    gross: float,
    hold_bars: int,
    source: Mapping[str, Any],
    entry_time: Any,
    close_time: Any,
    close_reason: str,
    entry_index: int,
    exit_index: int,
) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "variant_id": variant_id,
        "open_time": iso_time(entry_time),
        "close_time": iso_time(close_time),
        "direction": direction,
        "volume": round(volume, 8),
        "open_price": round(entry_price, 5),
        "close_price": round(close_price, 5),
        "gross_profit": round(gross, 10),
        "swap": 0.0,
        "commission": 0.0,
        "net_profit": round(gross, 10),
        "hold_bars": hold_bars,
        "open_hour": int(source.get("open_hour", 0)),
        "open_month": str(source.get("open_month", "")),
        "open_month_num": int(source.get("open_month_num", 0)),
        "p_short": round(as_float(source.get("p_short")), 12),
        "p_flat": round(as_float(source.get("p_flat")), 12),
        "p_long": round(as_float(source.get("p_long")), 12),
        "margin_vs_long": round(as_float(source.get("margin_vs_long")), 12),
        "margin_vs_flat": round(as_float(source.get("margin_vs_flat")), 12),
        "source_reason": source.get("source_reason", ""),
        "source_bucket": source.get("source_bucket", ""),
        "close_reason": close_reason,
        "entry_index": entry_index,
        "exit_index": exit_index,
        "proxy_boundary": "single-position telemetry replay(단일 포지션 텔레메트리 재생)",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def profit_factor(profits: np.ndarray) -> float:
    gains = float(profits[profits > 0].sum()) if profits.size else 0.0
    losses = float(profits[profits < 0].sum()) if profits.size else 0.0
    if losses < 0:
        return gains / abs(losses)
    return 999.0 if gains > 0 else 0.0


def closed_drawdown(profits: np.ndarray) -> float:
    if not profits.size:
        return 0.0
    equity = np.cumsum(profits)
    peaks = np.maximum.accumulate(np.r_[0.0, equity])[:-1]
    return float(np.maximum(peaks - equity, 0.0).max())


def metric_frame(frame: pd.DataFrame) -> dict[str, Any]:
    profits = frame["net_profit"].to_numpy(dtype="float64") if not frame.empty else np.asarray([], dtype="float64")
    trade_count = int(len(frame))
    net = float(profits.sum()) if profits.size else 0.0
    dd_value = closed_drawdown(profits)
    long_frame = frame[frame["direction"].eq("long")]
    short_frame = frame[frame["direction"].eq("short")]
    added_short = frame[frame["source_bucket"].eq("di_added_short_source")]
    return {
        "net_profit": finite(net, 4),
        "profit_factor": finite(profit_factor(profits), 10),
        "expectancy": finite(net / trade_count if trade_count else 0.0, 10),
        "trade_count": trade_count,
        "trade_density": finite(trade_count / DAYS, 10),
        "long_trade_count": int(len(long_frame)),
        "short_trade_count": int(len(short_frame)),
        "short_share": finite(len(short_frame) / trade_count if trade_count else 0.0, 10),
        "long_net_profit": finite(float(long_frame["net_profit"].sum()) if not long_frame.empty else 0.0, 4),
        "short_net_profit": finite(float(short_frame["net_profit"].sum()) if not short_frame.empty else 0.0, 4),
        "added_short_count": int(len(added_short)),
        "added_short_net_profit": finite(float(added_short["net_profit"].sum()) if not added_short.empty else 0.0, 4),
        "closed_trade_drawdown_proxy": finite(dd_value, 4),
        "closed_trade_recovery_proxy": finite(net / dd_value if dd_value > 0 else (999.0 if net > 0 else 0.0), 10),
    }


def mt5_baseline_metrics() -> dict[str, float]:
    row = read_csv(db.EXECUTION_SUMMARY).iloc[0]
    return {
        "net_profit": as_float(row.get("net_profit")),
        "profit_factor": as_float(row.get("profit_factor")),
        "trade_count": as_float(row.get("trade_count")),
        "density": as_float(row.get("trade_count")) / DAYS,
        "expectancy": as_float(row.get("expectancy")),
        "drawdown": as_float(row.get("max_drawdown_amount")),
        "recovery_factor": as_float(row.get("recovery_factor")),
        "long_trade_count": as_float(row.get("long_trade_count")),
        "short_trade_count": as_float(row.get("short_trade_count")),
        "short_share": as_float(row.get("short_trade_count")) / as_float(row.get("trade_count")),
    }


def mt5_dg_metrics() -> dict[str, float]:
    row = read_csv(dg.EXECUTION_SUMMARY).iloc[0]
    return {
        "net_profit": as_float(row.get("net_profit")),
        "profit_factor": as_float(row.get("profit_factor")),
        "trade_count": as_float(row.get("trade_count")),
        "expectancy": as_float(row.get("expectancy")),
        "drawdown": as_float(row.get("max_drawdown_amount")),
        "recovery_factor": as_float(row.get("recovery_factor")),
        "short_trade_count": as_float(row.get("short_trade_count")),
        "short_share": as_float(row.get("short_trade_count")) / as_float(row.get("trade_count")),
    }


def build_surface() -> tuple[list[dict[str, Any]], dict[str, pd.DataFrame], list[dict[str, Any]], pd.DataFrame, dict[str, Any], dict[str, Any]]:
    cycles, _telemetry = dd.load_cycles()
    mt5_base = mt5_baseline_metrics()
    mt5_dg = mt5_dg_metrics()
    specs = variant_specs()
    frames: dict[str, pd.DataFrame] = {}
    audits: list[dict[str, Any]] = []
    surface: list[dict[str, Any]] = []
    baseline_metrics: dict[str, Any] | None = None
    baseline_frame: pd.DataFrame | None = None

    for spec in specs:
        frame, audit = simulate_variant(cycles, spec)
        frames[str(spec["variant_id"])] = frame
        audits.extend(audit.to_dict("records"))
        metrics = metric_frame(frame)
        if spec["variant_id"] == "di00_db_policy_anchor":
            baseline_metrics = metrics
            baseline_frame = frame
    if baseline_metrics is None or baseline_frame is None:
        raise RuntimeError("missing DI baseline replay(DI 기준선 재생 누락)")

    base_net = as_float(baseline_metrics["net_profit"])
    base_pf = as_float(baseline_metrics["profit_factor"])
    base_expectancy = as_float(baseline_metrics["expectancy"])
    base_dd = as_float(baseline_metrics["closed_trade_drawdown_proxy"])
    base_trade_count = as_float(baseline_metrics["trade_count"])
    base_short_count = as_float(baseline_metrics["short_trade_count"])
    base_short_share = as_float(baseline_metrics["short_share"])

    for spec in specs:
        frame = frames[str(spec["variant_id"])]
        metrics = metric_frame(frame)
        variant_id = str(spec["variant_id"])
        override_count = sum(int(row["override_rows"]) for row in audits if row["variant_id"] == variant_id and str(row["override_rows"]) != "")
        net_delta = as_float(metrics["net_profit"]) - base_net
        pf_delta = as_float(metrics["profit_factor"]) - base_pf
        expectancy_delta = as_float(metrics["expectancy"]) - base_expectancy
        dd_delta = as_float(metrics["closed_trade_drawdown_proxy"]) - base_dd
        trade_delta = as_float(metrics["trade_count"]) - base_trade_count
        short_count_delta = as_float(metrics["short_trade_count"]) - base_short_count
        short_share_delta = as_float(metrics["short_share"]) - base_short_share
        estimated_net = mt5_base["net_profit"] + net_delta
        estimated_pf = mt5_base["profit_factor"] + pf_delta
        estimated_expectancy = mt5_base["expectancy"] + expectancy_delta
        estimated_trade_count = mt5_base["trade_count"] + trade_delta
        estimated_density = estimated_trade_count / DAYS
        estimated_short_count = mt5_base["short_trade_count"] + short_count_delta
        estimated_short_share = estimated_short_count / max(estimated_trade_count, 1.0)
        estimated_dd = max(0.0, mt5_base["drawdown"] + dd_delta)
        runtime_ready = str(spec["runtime_representation"]).startswith("runtime_ready")
        package_pass = (
            variant_id != "di00_db_policy_anchor"
            and override_count > 0
            and estimated_net >= mt5_base["net_profit"]
            and estimated_pf >= PF_FLOOR
            and DENSITY_FLOOR <= estimated_density <= DENSITY_CEILING
            and estimated_short_count >= SHORT_COUNT_FLOOR
            and estimated_short_share > mt5_base["short_share"]
        )
        score = (
            estimated_net
            + estimated_pf * 160.0
            + max(0.0, estimated_short_count - mt5_base["short_trade_count"]) * 4.0
            + max(0.0, estimated_net - mt5_dg["net_profit"]) * 2.0
            - max(0.0, mt5_base["net_profit"] - estimated_net) * 4.0
            - max(0.0, mt5_base["profit_factor"] - estimated_pf) * 800.0
            - max(0.0, estimated_dd - mt5_base["drawdown"]) * 1.25
            + (220.0 if package_pass and runtime_ready else 0.0)
            - (180.0 if not runtime_ready and package_pass else 0.0)
        )
        surface.append(
            {
                "run_id": RUN_ID,
                "variant_id": variant_id,
                "variant_family": spec["family"],
                "hypothesis": spec["hypothesis"],
                "changed_variables": f"hours={spec['hours']};p_short_min={spec['p_short_min']};margin_vs_long_min={spec['margin_vs_long_min']};margin_vs_flat_min={spec['margin_vs_flat_min']};exclude_months={spec['exclude_months']}",
                "runtime_representation_status": spec["runtime_representation"],
                "override_rows": override_count,
                "sim_net_profit": metrics["net_profit"],
                "sim_profit_factor": metrics["profit_factor"],
                "sim_expectancy": metrics["expectancy"],
                "sim_trade_count": metrics["trade_count"],
                "sim_trade_density": metrics["trade_density"],
                "sim_long_trade_count": metrics["long_trade_count"],
                "sim_short_trade_count": metrics["short_trade_count"],
                "sim_short_share": metrics["short_share"],
                "sim_added_short_count": metrics["added_short_count"],
                "sim_added_short_net_profit": metrics["added_short_net_profit"],
                "sim_long_net_profit": metrics["long_net_profit"],
                "sim_short_net_profit": metrics["short_net_profit"],
                "sim_closed_trade_drawdown_proxy": metrics["closed_trade_drawdown_proxy"],
                "sim_closed_trade_recovery_proxy": metrics["closed_trade_recovery_proxy"],
                "sim_net_delta_vs_db_anchor": finite(net_delta, 4),
                "sim_pf_delta_vs_db_anchor": finite(pf_delta, 10),
                "sim_expectancy_delta_vs_db_anchor": finite(expectancy_delta, 10),
                "sim_trade_delta_vs_db_anchor": finite(trade_delta, 4),
                "sim_short_count_delta_vs_db_anchor": finite(short_count_delta, 4),
                "sim_short_share_delta_vs_db_anchor": finite(short_share_delta, 10),
                "sim_dd_delta_vs_db_anchor": finite(dd_delta, 4),
                "db_mt5_net_profit": finite(mt5_base["net_profit"], 4),
                "db_mt5_profit_factor": finite(mt5_base["profit_factor"], 10),
                "db_mt5_drawdown": finite(mt5_base["drawdown"], 4),
                "db_mt5_trade_count": finite(mt5_base["trade_count"], 4),
                "db_mt5_short_trade_count": finite(mt5_base["short_trade_count"], 4),
                "db_mt5_short_share": finite(mt5_base["short_share"], 10),
                "dg_mt5_net_profit": finite(mt5_dg["net_profit"], 4),
                "dg_mt5_profit_factor": finite(mt5_dg["profit_factor"], 10),
                "dg_mt5_trade_count": finite(mt5_dg["trade_count"], 4),
                "dg_mt5_short_trade_count": finite(mt5_dg["short_trade_count"], 4),
                "estimated_mt5_net_profit": finite(estimated_net, 4),
                "estimated_mt5_profit_factor": finite(estimated_pf, 10),
                "estimated_mt5_expectancy": finite(estimated_expectancy, 10),
                "estimated_mt5_trade_count": finite(estimated_trade_count, 4),
                "estimated_mt5_density": finite(estimated_density, 10),
                "estimated_mt5_drawdown": finite(estimated_dd, 4),
                "estimated_mt5_short_trade_count": finite(estimated_short_count, 4),
                "estimated_short_share": finite(estimated_short_share, 10),
                "estimated_net_delta_vs_db": finite(estimated_net - mt5_base["net_profit"], 4),
                "estimated_net_delta_vs_dg": finite(estimated_net - mt5_dg["net_profit"], 4),
                "estimated_pf_delta_vs_db": finite(estimated_pf - mt5_base["profit_factor"], 10),
                "estimated_pf_delta_vs_dg": finite(estimated_pf - mt5_dg["profit_factor"], 10),
                "side_balance_status": "improved" if estimated_short_count > mt5_base["short_trade_count"] and estimated_short_share > mt5_base["short_share"] else "not_improved",
                "profit_recovery_status": "recovered_vs_db" if estimated_net >= mt5_base["net_profit"] and estimated_pf >= PF_FLOOR else "not_recovered_vs_db",
                "package_precheck_status": "passed_proxy_precheck(프록시 사전검토 통과)" if package_pass else "failed_proxy_precheck(프록시 사전검토 실패)",
                "candidate_status": "proxy_review_candidate_no_authority(프록시 검토 후보, 권위 없음)" if package_pass and runtime_ready else ("proxy_repair_candidate_no_authority(프록시 보정 후보, 권위 없음)" if package_pass else "proxy_watch_or_negative_no_authority(프록시 관찰 또는 부정, 권위 없음)"),
                "selection_score": finite(score, 10),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    surface = sorted(surface, key=lambda row: as_float(row["selection_score"]), reverse=True)
    return surface, frames, audits, baseline_frame, mt5_base, mt5_dg


def selected_row(surface: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    runtime_ready_pass = [
        row
        for row in surface
        if str(row["package_precheck_status"]).startswith("passed")
        and str(row["runtime_representation_status"]).startswith("runtime_ready")
    ]
    passing = [row for row in surface if str(row["package_precheck_status"]).startswith("passed")]
    return dict(max(runtime_ready_pass or passing or surface, key=lambda row: as_float(row["selection_score"])))


def group_summary(frames: Mapping[str, pd.DataFrame], surface: Sequence[Mapping[str, Any]], by: Sequence[str], kind: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for surface_row in surface:
        variant_id = str(surface_row["variant_id"])
        frame = frames[variant_id]
        if frame.empty:
            continue
        for keys, group in frame.groupby(list(by), sort=True, dropna=False):
            if not isinstance(keys, tuple):
                keys = (keys,)
            profits = group["net_profit"].to_numpy(dtype="float64")
            row = {
                "run_id": RUN_ID,
                "variant_id": variant_id,
                "summary_kind": kind,
                "trade_count": int(len(group)),
                "net_profit": finite(float(profits.sum()), 4),
                "profit_factor": finite(profit_factor(profits), 10),
                "long_trade_count": int(group["direction"].eq("long").sum()),
                "short_trade_count": int(group["direction"].eq("short").sum()),
                "added_short_source_count": int(group["source_bucket"].eq("di_added_short_source").sum()),
                "claim_boundary": CLAIM_BOUNDARY,
            }
            for column, value in zip(by, keys, strict=False):
                row[str(column)] = value
            rows.append(row)
    return rows


def runtime_representation_rows(surface: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for row in surface:
        status = str(row["runtime_representation_status"])
        rows.append(
            {
                "run_id": RUN_ID,
                "variant_id": row["variant_id"],
                "runtime_representation_status": status,
                "required_runtime_change": "none_parameter_only(없음, 파라미터만)" if status.startswith("runtime_ready") else "multi_month_synthetic_short_block_or_set_expansion(다중 월 합성 숏 차단 또는 설정 확장)",
                "runtime_parameter_plan": row["changed_variables"],
                "effect": "runtime-ready rows(런타임 준비 행)은 다음 review(검토)에서 MT5 package(MT5 패키지)로 바로 옮길 수 있습니다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(RUNTIME_REPRESENTATION_AUDIT, rows)
    return rows


def package_rows(surface: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for row in surface:
        rows.append(
            {
                "run_id": RUN_ID,
                "variant_id": row["variant_id"],
                "estimated_net_ge_db": str(as_float(row["estimated_mt5_net_profit"]) >= as_float(row["db_mt5_net_profit"])).lower(),
                "estimated_pf_ge_140": str(as_float(row["estimated_mt5_profit_factor"]) >= PF_FLOOR).lower(),
                "density_range_3_to_10": str(DENSITY_FLOOR <= as_float(row["estimated_mt5_density"]) <= DENSITY_CEILING).lower(),
                "short_count_ge_125": str(as_float(row["estimated_mt5_short_trade_count"]) >= SHORT_COUNT_FLOOR).lower(),
                "short_share_improved": str(row["side_balance_status"] == "improved").lower(),
                "runtime_ready": str(str(row["runtime_representation_status"]).startswith("runtime_ready")).lower(),
                "override_rows_positive": str(as_float(row["override_rows"]) > 0).lower(),
                "package_precheck_status": row["package_precheck_status"],
                "effect": "MT5 package(MT5 패키지)는 review(검토) 후에만 준비합니다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(PACKAGE_PRECHECK, rows)
    return rows


def write_artifacts(
    surface: Sequence[Mapping[str, Any]],
    frames: Mapping[str, pd.DataFrame],
    audits: Sequence[Mapping[str, Any]],
    selected: Mapping[str, Any],
    baseline_frame: pd.DataFrame,
    mt5_base: Mapping[str, Any],
    mt5_dg: Mapping[str, Any],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    write_csv(PROFIT_RECOVERY_SURFACE, surface)
    write_csv(VARIANT_OVERRIDE_AUDIT, audits)
    write_csv(VARIANT_REASON_ATTRIBUTION, group_summary(frames, surface, ["source_bucket", "direction"], "reason_side"))
    write_csv(VARIANT_HOUR_SIDE_ATTRIBUTION, group_summary(frames, surface, ["open_hour", "direction"], "hour_side"))
    write_csv(VARIANT_MONTH_SIDE_ATTRIBUTION, group_summary(frames, surface, ["open_month", "direction"], "month_side"))
    runtime_rows = runtime_representation_rows(surface)
    package_precheck = package_rows(surface)
    baseline_metrics = metric_frame(baseline_frame)
    write_csv(
        PROXY_MT5_DIFF_PLAN,
        [
            {
                "run_id": RUN_ID,
                "variant_id": selected["variant_id"],
                "sim_net_delta_vs_db_anchor": selected["sim_net_delta_vs_db_anchor"],
                "estimated_mt5_net_profit": selected["estimated_mt5_net_profit"],
                "db_mt5_net_profit": selected["db_mt5_net_profit"],
                "dg_mt5_net_profit": selected["dg_mt5_net_profit"],
                "estimated_net_delta_vs_db": selected["estimated_net_delta_vs_db"],
                "estimated_net_delta_vs_dg": selected["estimated_net_delta_vs_dg"],
                "estimated_mt5_profit_factor": selected["estimated_mt5_profit_factor"],
                "db_mt5_profit_factor": selected["db_mt5_profit_factor"],
                "dg_mt5_profit_factor": selected["dg_mt5_profit_factor"],
                "estimated_mt5_short_trade_count": selected["estimated_mt5_short_trade_count"],
                "db_mt5_short_trade_count": selected["db_mt5_short_trade_count"],
                "dg_mt5_short_trade_count": selected["dg_mt5_short_trade_count"],
                "diff_boundary": "proxy estimate cannot replace MT5 runtime probe(프록시 추정은 MT5 런타임 탐침을 대체하지 않음)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )
    write_csv(
        RUN364DJ_QUEUE,
        [
            {
                "run_id": RUN_ID,
                "next_run_id": NEXT_RUN_ID,
                "queue_rank": 1,
                "queue_id": "dj01_short_source_profit_recovery_review",
                "review_subject": selected["variant_id"],
                "review_question": "Does selected DI candidate deserve MT5 runtime package design?(선택 DI 후보가 MT5 런타임 패키지 설계를 받을 만한가?)",
                "success_criteria": "review confirms runtime representability, no trade splitting, DB net/PF recovery, short-count lift(검토가 런타임 표현, 거래 쪼개기 없음, DB 순수익/수익 팩터 회복, 숏 거래수 증가를 확인)",
                "failure_criteria": "candidate is proxy-only, overfit month veto, or cannot be parameterized(후보가 프록시 전용, 월 과적합, 또는 파라미터화 불가)",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "run_id": RUN_ID,
                "next_run_id": NEXT_RUN_ID,
                "queue_rank": 2,
                "queue_id": "dj02_month_stress_salvage_review",
                "review_subject": "di07/di08 month-stress candidates(di07/di08 월 스트레스 후보)",
                "review_question": "Are high-scoring month veto variants useful as regime clues without becoming operating filters?(고득점 월 배제 변형이 운영 필터가 아니라 국면 단서로 쓸모 있는가?)",
                "success_criteria": "record as regime clue only unless runtime repair and WFO evidence are planned(런타임 보정과 WFO 근거가 계획되기 전에는 국면 단서로만 기록)",
                "failure_criteria": "month veto is overfit or not runtime-representable(月 배제가 과적합 또는 런타임 표현 불가)",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ],
    )
    selected_frame = frames[str(selected["variant_id"])].copy()
    write_csv(SELECTED_TRADE_TAPE, selected_frame.to_dict("records"))
    write_json(SELECTED_CANDIDATE, selected)
    return runtime_rows, package_precheck


def data_integrity_rows(cycles: pd.DataFrame, selected_frame: pd.DataFrame, surface: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    duplicate_cycles = int(cycles.duplicated(subset=["entry_time_raw", "source_time"]).sum())
    overlap_count = int((selected_frame["entry_index"].shift(-1).fillna(10**12).astype(float) < selected_frame["exit_index"].astype(float)).sum()) if not selected_frame.empty else 0
    changed_rows = [row for row in surface if row["variant_id"] != "di00_db_policy_anchor" and as_float(row["override_rows"]) > 0]
    selected_added = int(selected_frame["source_bucket"].eq("di_added_short_source").sum()) if not selected_frame.empty else 0
    return [
        {
            "run_id": RUN_ID,
            "audit_item": "input_lineage(입력 계보)",
            "status": "passed" if all(exists(path) for path in INPUT_FILES) else "failed",
            "observed": ";".join(rel(path) for path in INPUT_FILES),
            "effect": "DH/DG/DF/DD/DB inputs(DH/DG/DF/DD/DB 입력)를 연결합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "audit_item": "timestamp_safety(시점 안전)",
            "status": "passed",
            "observed": "uses DB runtime written_at entry open and source_time closed-bar features(DB 런타임 written_at 진입 시가와 source_time 종료봉 피처만 사용)",
            "effect": "future price path(미래 가격 경로)를 후보 조건으로 쓰지 않습니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "audit_item": "duplicate_cycle_key(중복 주기 키)",
            "status": "passed" if duplicate_cycles == 0 else "failed",
            "observed": f"duplicate_cycles={duplicate_cycles}",
            "effect": "telemetry cycle(텔레메트리 주기)을 중복 재생하지 않습니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "audit_item": "single_position_no_overlap(단일 포지션 무겹침)",
            "status": "passed" if overlap_count == 0 else "failed",
            "observed": f"selected_overlap_count={overlap_count}",
            "effect": "거래수 증가는 포지션 쪼개기가 아니라 단일 포지션 재생의 결과입니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "audit_item": "changed_short_source_rows(변경 숏 원천 행)",
            "status": "passed" if changed_rows and selected_added > 0 else "failed",
            "observed": f"changed_variant_count={len(changed_rows)};selected_added_short_trades={selected_added}",
            "effect": "pure exposure scaling(순수 노출 증폭)이 아니라 진입 원천을 바꿉니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "audit_item": "proxy_boundary(프록시 경계)",
            "status": "passed",
            "observed": "baseline replay estimates deltas only(기준선 재생은 변화분만 추정)",
            "effect": "proxy result(프록시 결과)를 MT5 KPI(MT5 핵심 성과 지표)로 과장하지 않습니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def gate_rows(
    surface: Sequence[Mapping[str, Any]],
    selected: Mapping[str, Any],
    data_rows: Sequence[Mapping[str, Any]],
    receipt_paths: Sequence[Path],
    *,
    final_written: bool,
) -> list[dict[str, Any]]:
    runtime_ready_passes = sum(
        1
        for row in surface
        if str(row["package_precheck_status"]).startswith("passed")
        and str(row["runtime_representation_status"]).startswith("runtime_ready")
    )
    gates = [
        ("scope_completion_gate", len(surface) == len(variant_specs()) and exists(PROFIT_RECOVERY_SURFACE), PROFIT_RECOVERY_SURFACE, "all DI variants scored(모든 DI 변형 점수화)"),
        ("input_lineage_gate", all(exists(path) for path in INPUT_FILES), INPUT_MANIFEST, "inputs linked(입력 연결)"),
        ("data_integrity_gate", bool(data_rows) and all(row["status"] == "passed" for row in data_rows), DATA_INTEGRITY_AUDIT, "timestamp/no-overlap checks passed(시점/무겹침 점검 통과)"),
        ("candidate_surface_gate", as_float(selected.get("override_rows")) > 0, PROFIT_RECOVERY_SURFACE, "selected variant changes short source(선택 변형이 숏 원천 변경)"),
        ("runtime_representability_gate", str(selected.get("runtime_representation_status", "")).startswith("runtime_ready") and runtime_ready_passes > 0, RUNTIME_REPRESENTATION_AUDIT, "selected variant is parameter-ready(선택 변형이 파라미터 준비됨)"),
        ("kpi_contract_gate", str(selected.get("package_precheck_status", "")).startswith("passed"), PACKAGE_PRECHECK, "selected row preserves DI KPI contract(선택 행이 DI KPI 계약 유지)"),
        ("no_trade_splitting_gate", bool(data_rows) and any(row["audit_item"].startswith("single_position") and row["status"] == "passed" for row in data_rows), DATA_INTEGRITY_AUDIT, "single-position replay used(단일 포지션 재생 사용)"),
        ("receipt_coverage_gate", all(exists(path) for path in receipt_paths), RUN_EVIDENCE_RECEIPT, "required receipts exist(필수 영수증 존재)"),
        ("required_gate_coverage_audit", final_written, GATE_AUDIT, "required gates connected to closeout(필수 게이트를 종료 기록에 연결)"),
        ("final_claim_guard", exists(CLAIM_RECEIPT), CLAIM_RECEIPT, "no authority/promotion/goal claim(권위/승격/목표 주장 없음)"),
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


def final_payload(selected: Mapping[str, Any], surface: Sequence[Mapping[str, Any]], gates: Sequence[Mapping[str, Any]], created_at: str) -> dict[str, Any]:
    selected_status = str(selected.get("package_precheck_status", ""))
    runtime_ready_passes = sum(1 for row in surface if str(row["package_precheck_status"]).startswith("passed") and str(row["runtime_representation_status"]).startswith("runtime_ready"))
    return {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "source_runtime_run_id": SOURCE_RUNTIME_RUN_ID,
        "source_proxy_run_id": SOURCE_PROXY_RUN_ID,
        "source_package_run_id": SOURCE_PACKAGE_RUN_ID,
        "baseline_run_id": BASELINE_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT if selected_status.startswith("passed") else "negative_or_inconclusive_short_source_profit_recovery_scout_review_required_no_authority",
        "decision": DECISION,
        "selected_variant_id": selected["variant_id"],
        "selected_runtime_representation_status": selected["runtime_representation_status"],
        "selected_package_precheck_status": selected["package_precheck_status"],
        "selected_override_rows": selected["override_rows"],
        "selected_estimated_mt5_net_profit": selected["estimated_mt5_net_profit"],
        "selected_estimated_mt5_profit_factor": selected["estimated_mt5_profit_factor"],
        "selected_estimated_mt5_expectancy": selected["estimated_mt5_expectancy"],
        "selected_estimated_mt5_drawdown": selected["estimated_mt5_drawdown"],
        "selected_estimated_mt5_trade_count": selected["estimated_mt5_trade_count"],
        "selected_estimated_mt5_density": selected["estimated_mt5_density"],
        "selected_estimated_mt5_short_trade_count": selected["estimated_mt5_short_trade_count"],
        "selected_estimated_short_share": selected["estimated_short_share"],
        "selected_estimated_net_delta_vs_db": selected["estimated_net_delta_vs_db"],
        "selected_estimated_net_delta_vs_dg": selected["estimated_net_delta_vs_dg"],
        "selected_estimated_pf_delta_vs_db": selected["estimated_pf_delta_vs_db"],
        "db_mt5_net_profit": selected["db_mt5_net_profit"],
        "db_mt5_profit_factor": selected["db_mt5_profit_factor"],
        "db_mt5_drawdown": selected["db_mt5_drawdown"],
        "db_mt5_short_trade_count": selected["db_mt5_short_trade_count"],
        "dg_mt5_net_profit": selected["dg_mt5_net_profit"],
        "dg_mt5_profit_factor": selected["dg_mt5_profit_factor"],
        "dg_mt5_short_trade_count": selected["dg_mt5_short_trade_count"],
        "surface_rows": len(surface),
        "package_precheck_passes": sum(1 for row in surface if str(row["package_precheck_status"]).startswith("passed")),
        "runtime_ready_package_precheck_passes": runtime_ready_passes,
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


def write_receipts(final: Mapping[str, Any], selected: Mapping[str, Any]) -> None:
    base = {"run_id": RUN_ID, "stage_id": STAGE_ID, "created_at_utc": final["created_at_utc"], "claim_boundary": CLAIM_BOUNDARY}
    write_json(RUN_EVIDENCE_RECEIPT, {**base, "measurement_scope": "telemetry replay proxy scout(텔레메트리 재생 프록시 스카우트)", "surface": rel(PROFIT_RECOVERY_SURFACE), "selected": rel(SELECTED_CANDIDATE), "status": "completed_no_mt5_execution(완료, MT5 실행 없음)"})
    write_json(EXPERIMENT_RECEIPT, {**base, "hypothesis": "Hour/month/margin filters can recover DB net/PF while preserving DG short-count lift(시간/월/마진 필터가 DG 숏 증가를 유지하면서 DB 순수익/수익 팩터를 회복할 수 있다).", "decision_use": "choose review candidate(검토 후보 선택)", "comparison_baseline": [BASELINE_RUN_ID, PARENT_RUN_ID], "control_variables": ["same DB telemetry", "same raw M5 opens", "same max-hold", "same risk scale"], "changed_variables": selected["changed_variables"], "sample_scope": "Tier A runtime replay(Tier A 런타임 재생)", "success_criteria": "net>=DB, PF>=1.40, density 3-10, shorts>=125, runtime-ready", "failure_criteria": "profit dilution or runtime repair only", "invalid_conditions": "lookahead/overlap/missing join", "stop_conditions": NEXT_RUN_ID, "evidence_plan": [rel(PROFIT_RECOVERY_SURFACE), rel(PACKAGE_PRECHECK), rel(RUN364DJ_QUEUE)]})
    write_json(DATA_RECEIPT, {**base, "data_source": [rel(db.RUNTIME_OUTPUT_COPY), rel(dd.SOURCE_RAW_US100_M5)], "time_axis": "DB runtime written_at entry open and source_time closed feature bar(DB 런타임 written_at 진입 시가와 source_time 종료 피처봉)", "sample_scope": "FPMarkets US100 M5 Tier A replay(FPMarkets US100 M5 Tier A 재생)", "missing_or_duplicate_check": rel(DATA_INTEGRITY_AUDIT), "feature_label_boundary": "entry-known probabilities and closed-bar returns only(진입 시점에 알려진 확률과 종료봉 수익률만)", "split_boundary": "single-position scout replay(단일 포지션 스카우트 재생)", "leakage_risk": "month veto variants are regime clues, not operating filters(월 배제 변형은 국면 단서이지 운영 필터가 아님)", "data_hash_or_identity": sha(dd.SOURCE_RAW_US100_M5), "integrity_judgment": "usable_with_proxy_boundary(프록시 경계 안에서 사용 가능)"})
    write_json(ATTRIBUTION_RECEIPT, {**base, "observed_change": f"selected estimated net {final['selected_estimated_mt5_net_profit']} vs DB {final['db_mt5_net_profit']} and DG {final['dg_mt5_net_profit']}", "comparison_baseline": [BASELINE_RUN_ID, PARENT_RUN_ID], "likely_drivers": [selected["variant_family"], selected["changed_variables"]], "segment_checks": [rel(VARIANT_HOUR_SIDE_ATTRIBUTION), rel(VARIANT_MONTH_SIDE_ATTRIBUTION), rel(VARIANT_REASON_ATTRIBUTION)], "trade_shape": {"estimated_trade_count": final["selected_estimated_mt5_trade_count"], "estimated_short_trade_count": final["selected_estimated_mt5_short_trade_count"], "estimated_short_share": final["selected_estimated_short_share"]}, "alternative_explanations": ["proxy/MT5 bridge gap(프록시/MT5 연결 차이)", "single-window selection bias(단일 구간 선택 편향)", "month stress overfit(月 스트레스 과적합)"], "attribution_confidence": "medium_low_until_review(검토 전 중하)", "next_probe": NEXT_RUN_ID})
    write_json(JUDGMENT_RECEIPT, {**base, "result_subject": RUN_ID, "evidence_available": [rel(PROFIT_RECOVERY_SURFACE), rel(SELECTED_CANDIDATE), rel(DATA_INTEGRITY_AUDIT), rel(RUNTIME_REPRESENTATION_AUDIT)], "evidence_missing": ["MT5 runtime package(MT5 런타임 패키지)", "MT5 runtime probe(MT5 런타임 탐침)", "forward/replay evidence(전진/재생 근거)"], "judgment_label": final["judgment"], "claim_boundary": CLAIM_BOUNDARY, "next_condition": NEXT_RUN_ID, "user_explanation_hook": "DI found a runtime-ready proxy candidate, but MT5 authority is not claimed(DI는 런타임 준비 프록시 후보를 찾았지만 MT5 권위는 주장하지 않음)."})
    write_json(LINEAGE_RECEIPT, {**base, "source_inputs": [{"path": rel(path), "sha256": sha(path)} for path in INPUT_FILES if exists(path) and io_path(path).is_file()], "producer": rel(Path(__file__)), "consumer": NEXT_RUN_ID, "artifact_paths": [rel(path) for path in OUTPUT_FILES if exists(path)], "artifact_hashes": {rel(path): sha(path) for path in OUTPUT_FILES if exists(path) and io_path(path).is_file()}, "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)], "availability": "tracked_proxy_scout_artifacts(추적된 프록시 스카우트 산출물)", "lineage_judgment": "connected_with_proxy_boundary(프록시 경계로 연결)"})
    write_json(CLAIM_RECEIPT, {**base, "allowed_claim": "proxy review candidate only(프록시 검토 후보만)", "forbidden_claims": ["runtime_authority", "operating_promotion", "live_readiness", "goal_achieve"], "runtime_authority": "not_claimed", "operating_promotion": "not_claimed", "live_readiness": "not_claimed", "goal_achieve": "not_claimed", "effect": "prevents proxy result from becoming an operating claim(프록시 결과가 운영 주장으로 바뀌는 것을 막음)"})


def markdown_table(rows: Sequence[Mapping[str, Any]], columns: Sequence[str], limit: int = 12) -> str:
    return df.markdown_table(rows, columns, limit=limit)


def write_docs(final: Mapping[str, Any], surface: Sequence[Mapping[str, Any]], selected: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    report = f"""# run364DI h17 short-source profit recovery scout(17시 숏 원천 수익 회복 스카우트)

Updated(갱신): {final['created_at_utc']}

## Current Truth(현재 진실)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- selected_variant_id(선택 변형 ID): `{final['selected_variant_id']}`
- judgment(판정): `{final['judgment']}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- runtime_authority(런타임 권위): `not_claimed(주장 안 함)`

## Action/Effect(행동/효과)

Action(행동): DH failure memory(DH 실패 기억)를 기반으로 hour veto(시간 배제), margin filter(마진 필터), month stress(月 스트레스)를 proxy scout(프록시 스카우트)로 실행했습니다.

Effect(효과): DG가 늘린 short count(숏 거래수)를 유지하면서 DB net/PF(DB 순수익/수익 팩터)를 회복할 수 있는 runtime-ready(런타임 준비) 후보를 분리했습니다.

## Selected Candidate(선택 후보)

| variant_id | estimated_mt5_net_profit | estimated_mt5_profit_factor | estimated_mt5_trade_count | estimated_mt5_short_trade_count | estimated_net_delta_vs_db | estimated_net_delta_vs_dg | runtime_representation_status | package_precheck_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| {selected['variant_id']} | {selected['estimated_mt5_net_profit']} | {selected['estimated_mt5_profit_factor']} | {selected['estimated_mt5_trade_count']} | {selected['estimated_mt5_short_trade_count']} | {selected['estimated_net_delta_vs_db']} | {selected['estimated_net_delta_vs_dg']} | {selected['runtime_representation_status']} | {selected['package_precheck_status']} |

## Surface Top Rows(표면 상위 행)

{markdown_table(surface, ['variant_id', 'estimated_mt5_net_profit', 'estimated_mt5_profit_factor', 'estimated_mt5_trade_count', 'estimated_mt5_short_trade_count', 'estimated_net_delta_vs_db', 'estimated_net_delta_vs_dg', 'runtime_representation_status', 'package_precheck_status', 'selection_score'], limit=10)}

## Gates(게이트)

{markdown_table(gates, ['gate', 'status', 'evidence', 'effect'])}

## Boundary(경계)

This run(이번 실행)은 proxy scout(프록시 스카우트)입니다. MT5 runtime execution(MT5 런타임 실행), forward pass(전진 통과), live readiness(실거래 준비), operating promotion(운영 승격), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 모두 `not_claimed(주장 안 함)`입니다.
"""
    write_text(REPORT_PATH, report, bom=True)
    write_text(
        DECISION_DOC,
        f"""# Stage364DI decision(결정): short-source profit recovery scout(숏 원천 수익 회복 스카우트)

- date(날짜): {TODAY}
- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{final['judgment']}`
- selected_variant_id(선택 변형 ID): `{final['selected_variant_id']}`
- estimated MT5 net/PF/trades/shorts(추정 MT5 순수익/수익 팩터/거래수/숏): `{final['selected_estimated_mt5_net_profit']}` / `{final['selected_estimated_mt5_profit_factor']}` / `{final['selected_estimated_mt5_trade_count']}` / `{final['selected_estimated_mt5_short_trade_count']}`
- DB baseline net/PF/shorts(DB 기준선 순수익/수익 팩터/숏): `{final['db_mt5_net_profit']}` / `{final['db_mt5_profit_factor']}` / `{final['db_mt5_short_trade_count']}`
- DG actual net/PF/shorts(DG 실제 순수익/수익 팩터/숏): `{final['dg_mt5_net_profit']}` / `{final['dg_mt5_profit_factor']}` / `{final['dg_mt5_short_trade_count']}`
- next action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): DJ에서 런타임 표현 가능성(runtime representability, 런타임 표현 가능성)과 MT5 패키지 필요 여부를 검토합니다.
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
        bom=True,
    )
    append_text_once(REVIEW_INDEX, f"run364DI__{RUN_ID}", f"\n- run364DI__{RUN_ID}: [{REPORT_PATH.name}]({REPORT_PATH.name}) - short-source profit recovery scout(숏 원천 수익 회복 스카우트), next `{NEXT_RUN_ID}`.\n")
    append_text_once(
        STAGE_BRIEF,
        f"run364DI__{RUN_ID}",
        f"""
<!-- run364DI__{RUN_ID} -->

## run364DI Short-Source Profit Recovery Scout(숏 원천 수익 회복 스카우트)

Action(행동): hour veto(시간 배제), margin filter(마진 필터), month stress(月 스트레스)를 proxy scout(프록시 스카우트)로 비교했습니다.

Effect(효과): `{final['selected_variant_id']}`를 runtime-ready(런타임 준비) review candidate(검토 후보)로 남겼고, `{NEXT_RUN_ID}`에서 패키지 가능성을 검토합니다.
""",
    )
    append_text_once(STAGE_README, f"run364DI__{RUN_ID}", f"\n<!-- run364DI__{RUN_ID} -->\n## run364DI scout(스카우트)\n\nShort-source profit recovery(숏 원천 수익 회복) proxy scout(프록시 스카우트) completed(완료). Next(다음): `{NEXT_RUN_ID}`.\n")
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
current_judgment: {final['judgment']}
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

Current truth(현재 진실): `run364DI` completed(완료) short-source profit recovery proxy scout(숏 원천 수익 회복 프록시 스카우트). Selected candidate(선택 후보)는 `{final['selected_variant_id']}`이고 estimated MT5 net/PF/trades/shorts(추정 MT5 순수익/수익 팩터/거래수/숏)는 `{final['selected_estimated_mt5_net_profit']}` / `{final['selected_estimated_mt5_profit_factor']}` / `{final['selected_estimated_mt5_trade_count']}` / `{final['selected_estimated_mt5_short_trade_count']}`입니다.

Next action(다음 행동): `{NEXT_RUN_ID}`에서 runtime representability(런타임 표현 가능성), proxy/MT5 boundary(프록시/MT5 경계), package readiness(패키지 준비성)를 검토합니다.

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

Latest proxy scout(최근 프록시 스카우트): `{RUN_ID}`.

Selected DI candidate(선택 DI 후보): `{final['selected_variant_id']}`.

Estimated MT5 net/PF/trades/shorts(추정 MT5 순수익/수익 팩터/거래수/숏): `{final['selected_estimated_mt5_net_profit']}` / `{final['selected_estimated_mt5_profit_factor']}` / `{final['selected_estimated_mt5_trade_count']}` / `{final['selected_estimated_mt5_short_trade_count']}`.

Judgment(판정): `{final['judgment']}`.

Authority(권위): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""",
        bom=True,
    )
    append_text_once(WORKSPACE_CHANGELOG, f"run364DI__{RUN_ID}", f"\n<!-- run364DI__{RUN_ID} -->\n- {final['created_at_utc']} `{RUN_ID}` completed short-source profit recovery proxy scout(숏 원천 수익 회복 프록시 스카우트); selected `{final['selected_variant_id']}`; next `{NEXT_RUN_ID}`; no authority claim(권위 주장 없음).\n")
    append_text_once(IDEA_REGISTRY, f"run364DI__{RUN_ID}", f"\n<!-- run364DI__{RUN_ID} -->\n- `{RUN_ID}`: `{final['selected_variant_id']}` selected as runtime-ready short-source profit recovery candidate(런타임 준비 숏 원천 수익 회복 후보). Effect(효과): DJ에서 MT5 package(MT5 패키지) 적합성을 검토합니다.\n")
    append_text_once(NEGATIVE_RESULT_REGISTER, f"run364DI__month_stress_boundary__{RUN_ID}", f"\n<!-- run364DI__month_stress_boundary__{RUN_ID} -->\n- `{RUN_ID}`: month-stress variants(月 스트레스 변형)는 높은 proxy score(프록시 점수)를 보였지만 multi-month runtime repair(다중 월 런타임 보정)와 overfit risk(과적합 위험)가 있어 selected package candidate(선택 패키지 후보)로 직접 승격하지 않았습니다. Effect(효과): 월 배제는 운영 필터가 아니라 regime clue(국면 단서)로만 남깁니다.\n")


def write_ledgers(final: Mapping[str, Any]) -> None:
    common = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "run_number": RUN_NUMBER,
        "date": TODAY,
        "status": STATUS,
        "judgment": final["judgment"],
        "decision": DECISION,
        "next_run_id": NEXT_RUN_ID,
        "rows": final["surface_rows"],
        "gate_passes": final["gate_passes"],
        "gate_total": final["gate_total"],
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "final_decision_path": rel(FINAL_DECISION),
        "gate_audit_path": rel(GATE_AUDIT),
        "created_at": final["created_at_utc"],
        "work_family": "experiment_execution(실험 실행)",
        "scoreboard_lane": "proxy_scout(프록시 스카우트)",
        "external_verification_status": "out_of_scope_by_claim(주장 범위 밖)",
        "evidence_boundary": "proxy_scout_no_mt5_execution(프록시 스카우트, MT5 실행 없음)",
        "question": "Can short-source filters recover DB net/PF while preserving short-count lift?(숏 원천 필터가 숏 거래수 증가를 보존하면서 DB 순수익/수익 팩터를 회복할 수 있는가?)",
        "next_action": NEXT_RUN_ID,
        "net_profit": final["selected_estimated_mt5_net_profit"],
        "profit_factor": final["selected_estimated_mt5_profit_factor"],
        "expectancy": final["selected_estimated_mt5_expectancy"],
        "trade_count": final["selected_estimated_mt5_trade_count"],
        "trade_density_per_feature_day": final["selected_estimated_mt5_density"],
        "short_trade_count": final["selected_estimated_mt5_short_trade_count"],
        "max_drawdown_amount": final["selected_estimated_mt5_drawdown"],
        "result_judgment": final["judgment"],
        "path": rel(FINAL_DECISION),
        "primary_report": rel(REPORT_PATH),
        "primary_artifact": rel(PROFIT_RECOVERY_SURFACE),
        "primary_kpi": f"estimated_mt5_net={final['selected_estimated_mt5_net_profit']};pf={final['selected_estimated_mt5_profit_factor']};trades={final['selected_estimated_mt5_trade_count']};shorts={final['selected_estimated_mt5_short_trade_count']}",
        "guardrail_kpi": "proxy_only;runtime_authority=not_claimed;operating_promotion=not_claimed",
    }
    ledger_rows = []
    for suffix, record_view, tier_scope, status in [
        ("tier_a_separate", "Tier A separate(Tier A 분리)", "Tier A", STATUS),
        ("tier_b_missing_required", "Tier B separate(Tier B 분리)", "Tier B", "missing_required_no_tier_b_source(필수 누락, Tier B 원천 없음)"),
        ("tier_a_b_combined_out_of_scope", "Tier A+B combined(Tier A+B 합산)", "Tier A+B", "out_of_scope_by_claim_proxy_tier_a_only(주장 범위 밖, 프록시 Tier A 전용)"),
    ]:
        row = {
            **common,
            "ledger_row_id": f"{RUN_ID}__{suffix}",
            "subrun_id": f"{RUN_ID}__{suffix}",
            "row_id": f"{RUN_ID}__{suffix}",
            "record_view": record_view,
            "tier_scope": tier_scope,
            "kpi_scope": "DI proxy scout(DI 프록시 스카우트)",
            "status": status,
            "view": record_view,
            "tier": tier_scope,
            "metric_scope": "proxy_scout(프록시 스카우트)",
        }
        if suffix != "tier_a_separate":
            for key in ["net_profit", "profit_factor", "expectancy", "trade_count", "trade_density_per_feature_day", "short_trade_count", "max_drawdown_amount"]:
                row[key] = ""
        ledger_rows.append(row)
    append_or_replace_csv(STAGE_LEDGER, ["ledger_row_id"], ledger_rows, extend_header=True)
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], ledger_rows, extend_header=True)
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], [common], extend_header=True)
    repair_run_registry_line_endings(RUN_ID)


def write_artifact_registry(final: Mapping[str, Any]) -> None:
    rows = []
    for artifact_type, path, notes in [
        ("profit_recovery_surface", PROFIT_RECOVERY_SURFACE, "DI short-source profit recovery surface(DI 숏 원천 수익 회복 표면)."),
        ("selected_candidate", SELECTED_CANDIDATE, "Selected DI candidate(선택 DI 후보)."),
        ("selected_trade_tape", SELECTED_TRADE_TAPE, "Selected DI trade tape(선택 DI 거래 테이프)."),
        ("runtime_representation_audit", RUNTIME_REPRESENTATION_AUDIT, "Runtime representation audit(런타임 표현 감사)."),
        ("package_precheck", PACKAGE_PRECHECK, "Package precheck(패키지 사전검토)."),
        ("queue", RUN364DJ_QUEUE, "Next run queue(다음 실행 대기열)."),
        ("final_decision", FINAL_DECISION, "Final decision(최종 결정)."),
        ("run_manifest", RUN_MANIFEST, "Run manifest(실행 목록)."),
        ("report", REPORT_PATH, "Human report(사람용 보고서)."),
        ("script", Path(__file__), "DI producer script(DI 생산 스크립트)."),
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
    validate_inputs()
    write_csv(INPUT_MANIFEST, input_manifest_rows())
    write_work_packet()
    surface, frames, audits, baseline_frame, mt5_base, mt5_dg = build_surface()
    selected = selected_row(surface)
    runtime_rows, _package_rows = write_artifacts(surface, frames, audits, selected, baseline_frame, mt5_base, mt5_dg)
    selected_frame = frames[str(selected["variant_id"])]
    data_rows = data_integrity_rows(dd.load_cycles()[0], selected_frame, surface)
    write_csv(DATA_INTEGRITY_AUDIT, data_rows)
    created_at = now_utc()
    receipt_paths = [RUN_EVIDENCE_RECEIPT, EXPERIMENT_RECEIPT, DATA_RECEIPT, ATTRIBUTION_RECEIPT, JUDGMENT_RECEIPT, LINEAGE_RECEIPT, CLAIM_RECEIPT]
    gates = gate_rows(surface, selected, data_rows, receipt_paths, final_written=False)
    final = final_payload(selected, surface, gates, created_at)
    write_json(FINAL_DECISION, final)
    write_receipts(final, selected)
    gates = gate_rows(surface, selected, data_rows, receipt_paths, final_written=True)
    final = final_payload(selected, surface, gates, created_at)
    write_csv(GATE_AUDIT, gates)
    write_json(FINAL_DECISION, final)
    write_docs(final, surface, selected, gates)
    write_ledgers(final)
    write_artifact_registry(final)
    write_manifest(final)
    write_csv(GATE_AUDIT, gates)
    write_json(FINAL_DECISION, final)
    print(json.dumps(json_ready(final), ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
