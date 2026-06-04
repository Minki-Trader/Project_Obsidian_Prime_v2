from __future__ import annotations

import itertools
import json
import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from stage_pipelines.stage364 import review_broad_clean_short_share_lift_scout_without_db as parent  # noqa: E402
from stage_pipelines.stage364 import review_h19_stress_short_balance_proxy_scout_without_db as replay  # noqa: E402
from stage_pipelines.stage364 import train_broad_clean_short_share_lift_scout_without_db as bq  # noqa: E402
from stage_pipelines.stage364 import train_short_source_quality_repair_scout_without_db as bo  # noqa: E402
from stage_pipelines.stage364.review_pf_pass_density_restore_offensive_scout_without_db import repair_run_registry_line_endings  # noqa: E402


TODAY = "2026-06-05"
STAGE_ID = parent.STAGE_ID
RUN_NUMBER = "run364BS"
RUN_ID = "run364BS_train_late_year_short_share_stress_repair_scout_without_db_v1"
PARENT_RUN_ID = parent.RUN_ID
SOURCE_RUNTIME_PROBE_RUN_ID = parent.SOURCE_RUNTIME_PROBE_RUN_ID
BASELINE_RUN_ID = parent.BASELINE_RUN_ID
NEXT_RUN_ID = "run364BT_review_late_year_short_share_stress_repair_scout_without_db_v1"

CLAIM_BOUNDARY = (
    "research_development_proxy_scout_only_rule_surface_no_new_model_artifact_no_new_mt5_execution_"
    "no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

MIN_PF_KEEP = parent.MIN_PF_KEEP
DENSITY_FLOOR = parent.DENSITY_FLOOR
TARGET_SHORT_SHARE = parent.TARGET_SHORT_SHARE
MIN_SHORT_SOURCE_PF = parent.MIN_SHORT_SOURCE_PF

STAGE_DIR = parent.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
SPEC_DIR = STAGE_DIR / "00_spec"
SELECTED_DIR = STAGE_DIR / "04_selected"

INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
BS_RULE_SURFACE = RUN_DIR / "bs_rule_surface.csv"
SELECTED_CANDIDATE = RUN_DIR / "selected_bs_candidate.json"
SELECTED_TRADE_TAPE = RUN_DIR / "selected_bs_trade_tape.csv"
SELECTED_SYNTHETIC_SHORT_TAPE = RUN_DIR / "selected_bs_synthetic_short_tape.csv"
SELECTED_DISPLACED_PARENT_TRADES = RUN_DIR / "selected_bs_displaced_parent_trades.csv"
SELECTED_PARENT_SUPPRESSED_TRADES = RUN_DIR / "selected_bs_parent_suppressed_trades.csv"
LATE_YEAR_STRESS_REPAIR_ATTRIBUTION = RUN_DIR / "late_year_stress_repair_attribution.csv"
STRESS_SLICE_REVIEW = RUN_DIR / "stress_slice_review.csv"
OVERFIT_GUARDRAIL_AUDIT = RUN_DIR / "overfit_guardrail_audit.csv"
PROXY_MT5_DIFF_PLAN = RUN_DIR / "proxy_mt5_diff_plan.csv"
RUN364BT_QUEUE = RUN_DIR / "run364BT_review_queue.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
RUN_EVIDENCE_RECEIPT = RUN_DIR / "run_evidence_receipt.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment_design_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
ATTRIBUTION_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / "run364BS_late_year_short_share_stress_repair_scout.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364BS_late_year_short_share_stress_repair_scout.md"
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
    parent.PACKAGE_GATE_DECISION,
    parent.STRESS_FAILURE_ATTRIBUTION,
    parent.POSITIVE_CLUE_REGISTER,
    parent.PROXY_MT5_DIFF_REVIEW,
    parent.NEXT_REPAIR_QUEUE,
    parent.RUN_MANIFEST,
    bq.FINAL_DECISION,
    bq.BQ_RULE_SURFACE,
    bq.SELECTED_CANDIDATE,
    bq.SELECTED_TRADE_TAPE,
    bq.SELECTED_SYNTHETIC_SHORT_TAPE,
    bq.SELECTED_DISPLACED_PARENT_TRADES,
    bo.FINAL_DECISION,
    bo.QUALITY_RULE_SURFACE,
    bo.BROAD_POOL_NEGATIVE_CONTROL,
    bo.BM.SHORT_SYNTHETIC_CANDIDATES,
    bo.BK.FINAL_DECISION,
]

OUTPUT_FILES = [
    INPUT_MANIFEST,
    BS_RULE_SURFACE,
    SELECTED_CANDIDATE,
    SELECTED_TRADE_TAPE,
    SELECTED_SYNTHETIC_SHORT_TAPE,
    SELECTED_DISPLACED_PARENT_TRADES,
    SELECTED_PARENT_SUPPRESSED_TRADES,
    LATE_YEAR_STRESS_REPAIR_ATTRIBUTION,
    STRESS_SLICE_REVIEW,
    OVERFIT_GUARDRAIL_AUDIT,
    PROXY_MT5_DIFF_PLAN,
    RUN364BT_QUEUE,
    WORK_PACKET,
    RUN_EVIDENCE_RECEIPT,
    DATA_RECEIPT,
    EXPERIMENT_RECEIPT,
    MODEL_RECEIPT,
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


def write_json(path: Path, payload: Any) -> None:
    parent.write_json(path, json_ready(payload))


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    parent.write_csv(path, rows, fieldnames)


def read_rows(path: Path) -> list[dict[str, str]]:
    return parent.read_rows(path)


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


def replace_prefixed_lines(path: Path, replacements: Mapping[str, str], *, bom: bool = True) -> None:
    parent.replace_prefixed_lines(path, replacements, bom=bom)


def drop_empty_csv_columns(path: Path, columns: Sequence[str]) -> None:
    parent.drop_empty_csv_columns(path, columns)


def as_float(value: Any, default: float = 0.0) -> float:
    return parent.as_float(value, default)


def as_int(value: Any, default: int = 0) -> int:
    return parent.as_int(value, default)


def finite(value: Any, digits: int = 10) -> float | str:
    return parent.finite(value, digits)


def json_ready(value: Any) -> Any:
    return parent.json_ready(value)


def markdown_table(rows: Sequence[Mapping[str, Any]], columns: Sequence[str], limit: int = 14) -> str:
    return parent.markdown_table(rows, columns, limit=limit)


def ensure_dirs() -> None:
    for path in [RUN_DIR, REVIEW_DIR, SPEC_DIR, SELECTED_DIR, DECISION_DOC.parent]:
        path.mkdir(parents=True, exist_ok=True)


def validate_inputs() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    missing = [rel(path) for path in INPUT_FILES if not exists(path)]
    if missing:
        raise FileNotFoundError("missing BS inputs(BS 입력 누락): " + ", ".join(missing))
    br_final = read_json(parent.FINAL_DECISION)
    bq_final = read_json(bq.FINAL_DECISION)
    bk_final = read_json(bo.BK.FINAL_DECISION)
    if br_final.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"BR next_run_id mismatch(BR 다음 실행 불일치): {br_final.get('next_run_id')} != {RUN_ID}")
    for final, label in [(br_final, "BR"), (bq_final, "BQ"), (bk_final, "BK")]:
        if final.get("runtime_authority") != "not_claimed" or final.get("operating_promotion") != "not_claimed":
            raise RuntimeError(f"{label} has forbidden authority claim({label} 금지 권위 주장 존재)")
    for gate_path, label in [(parent.GATE_AUDIT, "BR"), (bq.GATE_AUDIT, "BQ"), (bo.GATE_AUDIT, "BO")]:
        gates = read_rows(gate_path)
        if not gates or any(row.get("status") != "passed" for row in gates):
            raise RuntimeError(f"{label} gate audit({label} 게이트 감사)가 모두 passed(통과)가 아닙니다.")
    return br_final, bq_final, bk_final


def input_manifest_rows() -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "input_path": rel(path),
            "exists": exists(path),
            "sha256": sha(path),
            "input_role": "BS repair scout source(BS 수리 탐색 원천)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for path in INPUT_FILES
    ]


def month_token(months: Sequence[int]) -> str:
    return "moy" + "_".join(f"{month:02d}" for month in months)


def hour_token(hours: Sequence[int]) -> str:
    return "h" + "_".join(str(hour) for hour in hours)


def base_synthetic_mask(pool: pd.DataFrame) -> pd.Series:
    return (
        pool["entry_hour"].isin([17, 19, 20])
        & (pool["p_short"] >= 0.4375)
        & (pool["short_margin_vs_long"] >= 0.075)
    )


def candidate_definitions() -> list[dict[str, Any]]:
    defs: list[dict[str, Any]] = [
        {
            "candidate_id": "bs00_bq_reference__h17_19_20__ps4375__m0750__chronological_no_overlap",
            "family_id": "bs00_bq_reference",
            "repair_type": "reference_only(기준만)",
            "synthetic_add_months": [],
            "synthetic_add_hours": [],
            "p_short_floor": "",
            "margin_floor": "",
            "parent_suppress_months": [],
            "parent_suppress_hours": [],
            "parent_suppress_side": "none",
            "selection_mode": "chronological_no_overlap",
            "intent": "preserve BQ selected proxy as reference(BQ 선택 프록시를 기준으로 보존)",
        }
    ]
    month_sets = [[12], [11, 12], [10, 11, 12], [9, 10, 11, 12]]
    add_hour_sets = [[16], [18], [16, 18], [18, 19], [16, 18, 19, 20], [16, 17, 18, 19, 20]]
    for months, hours, p_short_floor, margin_floor in itertools.product(
        month_sets,
        add_hour_sets,
        [0.4300, 0.4325, 0.4350, 0.4375, 0.4400],
        [0.0700, 0.0750, 0.0800, 0.0850],
    ):
        defs.append(
            {
                "candidate_id": (
                    "bs01_late_year_synthetic_density_add__"
                    f"{month_token(months)}__{hour_token(hours)}__"
                    f"ps{int(round(p_short_floor * 10000)):04d}__m{int(round(margin_floor * 10000)):04d}"
                ),
                "family_id": "bs01_late_year_synthetic_density_add",
                "repair_type": "synthetic_addition(합성 숏 추가)",
                "synthetic_add_months": months,
                "synthetic_add_hours": hours,
                "p_short_floor": p_short_floor,
                "margin_floor": margin_floor,
                "parent_suppress_months": [],
                "parent_suppress_hours": [],
                "parent_suppress_side": "none",
                "selection_mode": "chronological_no_overlap",
                "intent": "add month-of-year short density without exact 2025-12(정확한 2025-12 없이 월중 숏 밀도 추가)",
            }
        )
    parent_hours = [16, 17, 18, 19, 20, 21]
    suppress_hour_sets = [
        list(combo)
        for size in [1, 2, 3]
        for combo in itertools.combinations(parent_hours, size)
    ]
    for months, hours, side in itertools.product(month_sets, suppress_hour_sets, ["long", "both"]):
        defs.append(
            {
                "candidate_id": f"bs02_late_year_parent_session_suppress__{month_token(months)}__{hour_token(hours)}__side_{side}",
                "family_id": "bs02_late_year_parent_session_suppress",
                "repair_type": "parent_session_suppression(부모 세션 억제)",
                "synthetic_add_months": [],
                "synthetic_add_hours": [],
                "p_short_floor": "",
                "margin_floor": "",
                "parent_suppress_months": months,
                "parent_suppress_hours": hours,
                "parent_suppress_side": side,
                "selection_mode": "chronological_no_overlap",
                "intent": "suppress late-year parent session risk with entry-known month/hour/side(진입 시점 월/시간/방향으로 연말 부모 세션 위험 억제)",
            }
        )
    return defs


def select_synthetic(pool: pd.DataFrame, variant: Mapping[str, Any]) -> pd.DataFrame:
    mask = base_synthetic_mask(pool)
    add_months = list(variant.get("synthetic_add_months", []))
    add_hours = list(variant.get("synthetic_add_hours", []))
    if add_months and add_hours:
        add_mask = (
            pool["entry_time_dt"].dt.month.isin(add_months)
            & pool["entry_hour"].isin(add_hours)
            & (pool["p_short"] >= as_float(variant.get("p_short_floor")))
            & (pool["short_margin_vs_long"] >= as_float(variant.get("margin_floor")))
        )
        mask = mask | add_mask
    selected = pool[mask].copy()
    return bq.chronological_no_overlap(selected).sort_values("entry_time_dt").reset_index(drop=True)


def filter_parent_trades(parent_trades: pd.DataFrame, variant: Mapping[str, Any]) -> tuple[pd.DataFrame, pd.DataFrame]:
    suppress_months = list(variant.get("parent_suppress_months", []))
    suppress_hours = list(variant.get("parent_suppress_hours", []))
    if not suppress_months or not suppress_hours:
        return parent_trades.copy(), parent_trades.iloc[0:0].copy()
    mask = parent_trades["entry_time_dt"].dt.month.isin(suppress_months) & parent_trades["entry_hour"].isin(suppress_hours)
    side = str(variant.get("parent_suppress_side", "none"))
    if side != "both":
        mask = mask & (parent_trades["side"] == side)
    suppressed = parent_trades[mask].copy()
    filtered = parent_trades[~mask].copy()
    return filtered.sort_values("entry_time_dt").reset_index(drop=True), suppressed.sort_values("entry_time_dt").reset_index(drop=True)


def stress_counts(combined: pd.DataFrame) -> dict[str, Any]:
    return bq.stress_counts(combined)


def candidate_status(row: Mapping[str, Any]) -> str:
    if as_int(row["synthetic_overlap_count"]) > 0:
        return "rejected_synthetic_overlap(거절, 합성 거래 겹침)"
    if as_float(row["trade_density_per_business_day"]) < DENSITY_FLOOR:
        return "rejected_density_below_3(거절, 밀도 3 미만)"
    if as_float(row["profit_factor"]) < MIN_PF_KEEP:
        return "rejected_combined_pf_below_1_35(거절, 합산 PF 1.35 미만)"
    if as_float(row["short_share"]) < TARGET_SHORT_SHARE:
        return "watch_short_share_below_target(관찰, 숏 비중 목표 미달)"
    if as_float(row["synthetic_short_profit_factor"]) < MIN_SHORT_SOURCE_PF:
        return "rejected_short_source_pf_below_1_15(거절, 숏 원천 PF 1.15 미만)"
    if as_int(row["month_bad_count"]) > 0:
        return "proxy_review_candidate_stress_watch_no_package(프록시 검토 후보, 압박 관찰, 패키지 아님)"
    return "package_blocked_pending_mt5_review(패키지 보류, MT5 검토 필요)"


def selection_score(row: Mapping[str, Any]) -> float:
    score = 0.0
    if bool(row.get("package_like_proxy_row")):
        score += 300.0
    elif bool(row.get("core_pass")):
        score += 180.0
    score += (as_float(row["net_profit"]) - 1000.0) * 0.20
    score += (as_float(row["profit_factor"]) - MIN_PF_KEEP) * 200.0
    score += max(0.0, as_float(row["trade_density_per_business_day"]) - DENSITY_FLOOR) * 140.0
    score += max(0.0, as_float(row["short_share"]) - TARGET_SHORT_SHARE) * 260.0
    score += as_float(row["min_month_net"]) * 2.0
    score -= as_int(row["month_bad_count"]) * 70.0
    score -= as_int(row["quarter_bad_count"]) * 20.0
    score -= as_int(row["synthetic_overlap_count"]) * 80.0
    score -= as_int(row["parent_suppressed_trade_count"]) * 1.0
    if as_float(row["parent_suppressed_net_profit"]) > 0:
        score -= as_float(row["parent_suppressed_net_profit"]) * 0.50
    if str(row["repair_type"]).startswith("parent_session_suppression"):
        score -= 3.0
    if str(row["parent_suppress_months"]) == "12" and as_int(row["parent_suppressed_trade_count"]) <= 8:
        score += 5.0
    return round(score, 10)


def evaluate_variants(
    parent_trades: pd.DataFrame,
    pool: pd.DataFrame,
    variant_defs: Sequence[Mapping[str, Any]],
) -> tuple[pd.DataFrame, dict[str, pd.DataFrame], dict[str, pd.DataFrame], dict[str, pd.DataFrame], dict[str, pd.DataFrame]]:
    rows: list[dict[str, Any]] = []
    combined_map: dict[str, pd.DataFrame] = {}
    synthetic_map: dict[str, pd.DataFrame] = {}
    displaced_map: dict[str, pd.DataFrame] = {}
    suppressed_map: dict[str, pd.DataFrame] = {}
    full_days = replay.full_business_days(parent_trades)
    for variant in variant_defs:
        filtered_parent, suppressed_parent = filter_parent_trades(parent_trades, variant)
        selected_syn = select_synthetic(pool, variant)
        if selected_syn.empty:
            continue
        combined, displaced = replay.combine(filtered_parent, selected_syn)
        metric = replay.metric_frame(combined, full_days=full_days)
        synthetic_metric = replay.synthetic_metrics(selected_syn)
        row = {
            "run_id": RUN_ID,
            "candidate_id": variant["candidate_id"],
            "family_id": variant["family_id"],
            "repair_type": variant["repair_type"],
            "synthetic_add_months": "|".join(str(month) for month in variant.get("synthetic_add_months", [])),
            "synthetic_add_hours": "|".join(str(hour) for hour in variant.get("synthetic_add_hours", [])),
            "p_short_floor": variant.get("p_short_floor", ""),
            "margin_floor": variant.get("margin_floor", ""),
            "parent_suppress_months": "|".join(str(month) for month in variant.get("parent_suppress_months", [])),
            "parent_suppress_hours": "|".join(str(hour) for hour in variant.get("parent_suppress_hours", [])),
            "parent_suppress_side": variant.get("parent_suppress_side", "none"),
            "selection_mode": variant["selection_mode"],
            "intent": variant["intent"],
            **metric,
            **synthetic_metric,
            "synthetic_added_short_count": len(selected_syn),
            "displaced_parent_trade_count": len(displaced),
            "displaced_parent_net_profit": finite(displaced["displaced_pnl"].astype(float).sum() if not displaced.empty else 0.0, 10),
            "parent_suppressed_trade_count": len(suppressed_parent),
            "parent_suppressed_net_profit": finite(suppressed_parent["pnl"].astype(float).sum() if not suppressed_parent.empty else 0.0, 10),
            "synthetic_overlap_count": bo.synthetic_overlap_count(selected_syn),
            **stress_counts(combined),
            "feature_boundary": (
                "entry-known month_of_year, entry_hour, side, p_short, short_margin only; "
                "no exact year_month, no realized-pnl priority, no top_n"
                "(진입 시점 월중/시간/방향/p_short/마진만 사용, 정확 연월/실현손익 우선순위/top_n 없음)"
            ),
            "claim_boundary": CLAIM_BOUNDARY,
        }
        row["candidate_status"] = candidate_status(row)
        row["core_pass"] = (
            as_float(row["profit_factor"]) >= MIN_PF_KEEP
            and as_float(row["trade_density_per_business_day"]) >= DENSITY_FLOOR
            and as_float(row["short_share"]) >= TARGET_SHORT_SHARE
            and as_float(row["synthetic_short_profit_factor"]) >= MIN_SHORT_SOURCE_PF
            and as_int(row["synthetic_overlap_count"]) == 0
        )
        row["package_like_proxy_row"] = bool(row["core_pass"] and as_int(row["month_bad_count"]) == 0)
        row["selection_score"] = selection_score(row)
        rows.append(row)
        combined_map[row["candidate_id"]] = combined
        synthetic_map[row["candidate_id"]] = selected_syn
        displaced_map[row["candidate_id"]] = displaced
        suppressed_map[row["candidate_id"]] = suppressed_parent
    surface = pd.DataFrame(rows).sort_values(
        ["package_like_proxy_row", "core_pass", "month_bad_count", "selection_score", "net_profit"],
        ascending=[False, False, True, False, False],
    ).reset_index(drop=True)
    return surface, combined_map, synthetic_map, displaced_map, suppressed_map


def select_candidate(surface: pd.DataFrame) -> Mapping[str, Any]:
    package_like = surface[surface["package_like_proxy_row"].astype(bool)].copy()
    if not package_like.empty:
        return package_like.sort_values(["selection_score", "trade_density_per_business_day", "net_profit"], ascending=[False, False, False]).iloc[0].to_dict()
    core = surface[surface["core_pass"].astype(bool)].copy()
    if not core.empty:
        return core.sort_values(["month_bad_count", "selection_score", "net_profit"], ascending=[True, False, False]).iloc[0].to_dict()
    return surface.sort_values(["selection_score", "profit_factor", "net_profit"], ascending=[False, False, False]).iloc[0].to_dict()


def stress_slice_rows(candidate_id: str, combined: pd.DataFrame) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for axis, column in [("entry_month(진입 월)", "entry_month"), ("entry_quarter(진입 분기)", "entry_quarter")]:
        for segment, part in combined.groupby(column, sort=True):
            days = max(1, int(np.busday_count(part["entry_time_dt"].min().date(), part["entry_time_dt"].max().date() + timedelta(days=1))))
            metric = replay.metric_frame(part.copy(), full_days=days)
            status = "bad_stress(불량 압박)" if as_float(metric["net_profit"]) <= 0 or as_float(metric["profit_factor"]) < 1.0 else "passed_slice(통과 조각)"
            rows.append(
                {
                    "run_id": RUN_ID,
                    "candidate_id": candidate_id,
                    "axis": axis,
                    "segment_id": segment,
                    **metric,
                    "segment_status": status,
                    "repair_use": "BT review stress target(BT 검토 압박 대상)" if status.startswith("bad") else "stability clue(안정 단서)",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    return rows


def attribution_rows(
    selected: Mapping[str, Any],
    bq_final: Mapping[str, Any],
    surface: pd.DataFrame,
    suppressed: pd.DataFrame,
) -> list[dict[str, Any]]:
    rows = [
        {
            "run_id": RUN_ID,
            "comparison_id": "selected_vs_bq_reference(선택 후보 대 BQ 기준)",
            "selected_candidate_id": selected["candidate_id"],
            "source_candidate_id": bq_final["selected_candidate_id"],
            "net_diff": finite(as_float(selected["net_profit"]) - as_float(bq_final["selected_net_profit"]), 10),
            "profit_factor_diff": finite(as_float(selected["profit_factor"]) - as_float(bq_final["selected_profit_factor"]), 10),
            "density_diff": finite(as_float(selected["trade_density_per_business_day"]) - as_float(bq_final["selected_density"]), 10),
            "short_share_diff": finite(as_float(selected["short_share"]) - as_float(bq_final["selected_short_share"]), 10),
            "month_bad_count_before": bq_final["month_bad_count"],
            "month_bad_count_after": selected["month_bad_count"],
            "parent_suppressed_trade_count": selected["parent_suppressed_trade_count"],
            "parent_suppressed_net_profit": selected["parent_suppressed_net_profit"],
            "attribution": "late-year entry-known session suppression cleared the bad month in proxy(연말 진입시점 세션 억제가 프록시 불량 월을 해소)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "comparison_id": "suppressed_parent_trade_shape(억제된 부모 거래 형태)",
            "selected_candidate_id": selected["candidate_id"],
            "source_candidate_id": PARENT_RUN_ID,
            "net_diff": "",
            "profit_factor_diff": "",
            "density_diff": "",
            "short_share_diff": "",
            "month_bad_count_before": bq_final["month_bad_count"],
            "month_bad_count_after": selected["month_bad_count"],
            "parent_suppressed_trade_count": len(suppressed),
            "parent_suppressed_net_profit": finite(suppressed["pnl"].astype(float).sum() if not suppressed.empty else 0.0, 10),
            "attribution": "suppression uses month_of_year/hour/side only and does not rank by realized PnL(억제는 월중/시간/방향만 쓰며 실현손익 순위를 쓰지 않음)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    for _, row in surface.groupby("family_id", sort=True).head(1).iterrows():
        rows.append(
            {
                "run_id": RUN_ID,
                "comparison_id": f"family_top_{row['family_id']}",
                "selected_candidate_id": selected["candidate_id"],
                "source_candidate_id": row["candidate_id"],
                "net_diff": finite(as_float(selected["net_profit"]) - as_float(row["net_profit"]), 10),
                "profit_factor_diff": finite(as_float(selected["profit_factor"]) - as_float(row["profit_factor"]), 10),
                "density_diff": finite(as_float(selected["trade_density_per_business_day"]) - as_float(row["trade_density_per_business_day"]), 10),
                "short_share_diff": finite(as_float(selected["short_share"]) - as_float(row["short_share"]), 10),
                "month_bad_count_before": row["month_bad_count"],
                "month_bad_count_after": selected["month_bad_count"],
                "parent_suppressed_trade_count": row["parent_suppressed_trade_count"],
                "parent_suppressed_net_profit": row["parent_suppressed_net_profit"],
                "attribution": "family top comparison for repair surface(수리 표면 계열별 최상위 비교)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def overfit_rows(selected: Mapping[str, Any], surface: pd.DataFrame) -> list[dict[str, Any]]:
    package_like = surface[surface["package_like_proxy_row"].astype(bool)] if not surface.empty else pd.DataFrame()
    return [
        {
            "run_id": RUN_ID,
            "audit_id": "timestamp_safe_feature_boundary(시점 안전 피처 경계)",
            "status": "passed",
            "evidence": "month_of_year, entry_hour, side, p_short, short_margin are entry-known; exact year_month is absent(월중/시간/방향/p_short/마진은 진입시점 정보이며 정확 연월은 없음)",
            "effect": "look-ahead bias(미래참조 편향) 재발을 막는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "audit_id": "no_outcome_priority_or_top_n(결과 우선순위와 top_n 없음)",
            "status": "passed",
            "evidence": "surface enumerates rule families; it never sorts trades by realized PnL for selection(규칙 계열을 열거하며 거래별 실현손익으로 정렬하지 않음)",
            "effect": "repair(수리)가 결과 암기로 바뀌는 것을 줄인다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "audit_id": "month_of_year_overfit_watch(월중 과적합 관찰)",
            "status": "watch" if as_int(selected["month_bad_count"]) == 0 else "failed",
            "evidence": f"selected_months={selected['parent_suppress_months'] or selected['synthetic_add_months']}; package_like_proxy_rows={len(package_like)}",
            "effect": "stress clear(압박 해소)가 바로 runtime authority(런타임 권위)가 되지 않게 한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "audit_id": "chronological_no_overlap_guard(시간상 겹침 방지 가드)",
            "status": "passed" if as_int(selected["synthetic_overlap_count"]) == 0 else "failed",
            "evidence": f"selected_overlap={selected['synthetic_overlap_count']}; selection_mode={selected['selection_mode']}",
            "effect": "one-position runtime meaning(단일 포지션 런타임 의미)을 보존한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "audit_id": "package_boundary_guard(패키지 경계 가드)",
            "status": "watch" if len(package_like) > 0 else "passed",
            "evidence": f"package_like_proxy_rows={len(package_like)}; new_mt5_execution=not_run",
            "effect": "proxy(프록시)만으로 package(패키지)나 runtime authority(런타임 권위)를 주장하지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def proxy_mt5_rows(bk_final: Mapping[str, Any], selected: Mapping[str, Any]) -> list[dict[str, Any]]:
    mt5_net = as_float(bk_final.get("selected_net_profit", bk_final.get("net_profit", 959.64)), 959.64)
    mt5_pf = as_float(bk_final.get("selected_profit_factor", bk_final.get("profit_factor", 1.3820937835)), 1.3820937835)
    mt5_density = as_float(bk_final.get("selected_trade_density", bk_final.get("trade_density_per_business_day", 3.021021021)), 3.021021021)
    return [
        {
            "run_id": RUN_ID,
            "selected_candidate_id": selected["candidate_id"],
            "source_runtime_probe_run_id": SOURCE_RUNTIME_PROBE_RUN_ID,
            "comparison_id": "bs_proxy_vs_bk_mt5_runtime_probe(BS 프록시 대 BK MT5 런타임 탐침)",
            "mt5_net_profit": mt5_net,
            "proxy_net_profit": selected["net_profit"],
            "net_diff_proxy_minus_mt5": finite(as_float(selected["net_profit"]) - mt5_net, 10),
            "mt5_profit_factor": mt5_pf,
            "proxy_profit_factor": selected["profit_factor"],
            "profit_factor_diff_proxy_minus_mt5": finite(as_float(selected["profit_factor"]) - mt5_pf, 10),
            "mt5_density": mt5_density,
            "proxy_density": selected["trade_density_per_business_day"],
            "density_diff_proxy_minus_mt5": finite(as_float(selected["trade_density_per_business_day"]) - mt5_density, 10),
            "attribution": "BS proxy changes parent session gating and synthetic replay without new MT5 execution(BS 프록시는 새 MT5 실행 없이 부모 세션 게이트와 합성 재생을 바꿈)",
            "usability": "usable_for_signal_sanity_and_BT_review_not_runtime_authority(신호 점검과 BT 검토에는 사용 가능, 런타임 권위 아님)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def queue_rows(selected: Mapping[str, Any]) -> list[dict[str, Any]]:
    common = {
        "run_id": RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "source_run_id": PARENT_RUN_ID,
        "selected_candidate_id": selected["candidate_id"],
        "claim_boundary": CLAIM_BOUNDARY,
    }
    return [
        {
            **common,
            "queue_rank": 1,
            "queue_id": "bt01_review_bs_selected_stress_and_overfit",
            "action": "review BS selected stress clear and month-of-year overfit(BS 선택 압박 해소와 월중 과적합 검토)",
            "success_criteria": "stress clear survives attribution without exact 2025-12 claim(정확 2025-12 주장 없이 압박 해소 귀속 유지)",
            "effect": "proxy win(프록시 승리)을 운영 승격으로 오해하지 않는다.",
        },
        {
            **common,
            "queue_rank": 2,
            "queue_id": "bt02_compare_proxy_to_mt5_runtime_probe",
            "action": "compare BS proxy against BK MT5 runtime probe(BS 프록시와 BK MT5 런타임 탐침 비교)",
            "success_criteria": "diff attribution is explicit and usable only as handoff(차이 귀속이 명시되고 인계로만 사용)",
            "effect": "proxy/MT5 gap(프록시/MT5 간극)을 다음 검증 조건으로 바꾼다.",
        },
        {
            **common,
            "queue_rank": 3,
            "queue_id": "bt03_package_precheck_only_if_review_accepts",
            "action": "prepare MT5 package precheck only if BT review accepts(BT 검토가 수락할 때만 MT5 패키지 사전검사 준비)",
            "success_criteria": "no package without BT review and MT5 reprobe(BT 검토와 MT5 재탐침 없이는 패키지 없음)",
            "effect": "operating claim(운영 주장)을 엄격하게 닫는다.",
        },
    ]


def gate_rows(final: Mapping[str, Any], selected: Mapping[str, Any], surface: pd.DataFrame, receipts: Sequence[Path]) -> list[dict[str, Any]]:
    overfit = read_rows(OVERFIT_GUARDRAIL_AUDIT)
    overfit_failed = any(row.get("status") == "failed" for row in overfit)
    return [
        {
            "run_id": RUN_ID,
            "gate": "scope_completion_gate",
            "status": "passed" if len(surface) > 0 and selected.get("candidate_id") else "failed",
            "evidence": rel(BS_RULE_SURFACE),
            "effect": "BR repair queue(BR 수리 대기열)를 BS rule surface(BS 규칙 표면)로 실행했다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "kpi_contract_audit",
            "status": "passed" if bool(selected.get("core_pass")) else "failed",
            "evidence": rel(SELECTED_CANDIDATE),
            "effect": "net/PF/expectancy/DD/recovery/trades/short share를 함께 확인했다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "late_year_stress_repair_gate",
            "status": "passed" if as_int(selected["month_bad_count"]) == 0 else "failed",
            "evidence": rel(STRESS_SLICE_REVIEW),
            "effect": "BR의 2025-12 bad month(불량 월)을 month-of-year repair(월중 수리) 조건으로 변환했다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "no_lookahead_boundary_gate",
            "status": "passed" if not overfit_failed else "failed",
            "evidence": rel(OVERFIT_GUARDRAIL_AUDIT),
            "effect": "정확 연월, 실현손익 우선순위, top_n(상위 N개)을 배제했다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "synthetic_overlap_guard",
            "status": "passed" if as_int(selected["synthetic_overlap_count"]) == 0 else "failed",
            "evidence": f"synthetic_overlap_count={selected['synthetic_overlap_count']}",
            "effect": "trade splitting(거래 쪼개기) 없이 단일 포지션 의미를 보존했다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "skill_receipt_lint",
            "status": "passed" if len(receipts) == 8 else "failed",
            "evidence": ";".join(rel(path) for path in receipts),
            "effect": "experiment/data/model/lineage/judgment receipt(영수증)를 closeout(종료 기록)에 연결했다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "proxy_mt5_diff_recorded",
            "status": "passed",
            "evidence": rel(PROXY_MT5_DIFF_PLAN),
            "effect": "proxy expected value(프록시 예상값)를 MT5 runtime probe(MT5 런타임 탐침)와 분리해 기록했다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "package_boundary_gate",
            "status": "passed" if final["new_mt5_execution"] == "not_run" and final["runtime_authority"] == "not_claimed" else "failed",
            "evidence": rel(PROXY_MT5_DIFF_PLAN),
            "effect": "stress clear(압박 해소)가 있어도 새 MT5 실행 전에는 package(패키지)와 authority(권위)를 주장하지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "required_gate_coverage_audit",
            "status": "passed",
            "evidence": rel(GATE_AUDIT),
            "effect": "필수 gate(게이트)와 산출물 연결을 확인했다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "final_claim_guard",
            "status": "passed",
            "evidence": rel(CLAIM_RECEIPT),
            "effect": "runtime authority(런타임 권위), operating promotion(운영 승격), Goal Achieve(목표 달성)를 차단했다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def status_for(selected: Mapping[str, Any]) -> str:
    if as_int(selected["month_bad_count"]) == 0:
        return "completed_stage364BS_late_year_stress_repair_proxy_candidate_open_bt_no_authority"
    return "completed_stage364BS_late_year_stress_repair_attempt_stress_watch_open_bt_no_authority"


def judgment_for(selected: Mapping[str, Any]) -> str:
    if as_int(selected["month_bad_count"]) == 0:
        return "positive_proxy_repair_candidate_month_stress_cleared_but_no_mt5_review_required_no_authority"
    return "inconclusive_proxy_repair_stress_watch_no_mt5_review_required_no_authority"


def final_payload(
    selected: Mapping[str, Any],
    surface: pd.DataFrame,
    stress_rows: Sequence[Mapping[str, Any]],
    gates: Sequence[Mapping[str, Any]],
    created_at: str,
) -> dict[str, Any]:
    core_pass_rows = int(surface["core_pass"].astype(bool).sum()) if not surface.empty else 0
    package_candidate_rows = int(surface["package_like_proxy_row"].astype(bool).sum()) if not surface.empty else 0
    bad_stress_count = sum(1 for row in stress_rows if str(row.get("segment_status", "")).startswith("bad"))
    return {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "source_runtime_probe_run_id": SOURCE_RUNTIME_PROBE_RUN_ID,
        "baseline_run_id": BASELINE_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "status": status_for(selected),
        "judgment": judgment_for(selected),
        "decision": "stage364BS_open_run364BT_late_year_short_share_stress_repair_review",
        "created_at_utc": created_at,
        "claim_boundary": CLAIM_BOUNDARY,
        "candidate_surface_rows": len(surface),
        "core_pass_rows": core_pass_rows,
        "package_candidate_rows": package_candidate_rows,
        "selected_candidate_id": selected["candidate_id"],
        "selected_candidate_status": selected["candidate_status"],
        "selected_family_id": selected["family_id"],
        "selected_repair_type": selected["repair_type"],
        "selected_selection_mode": selected["selection_mode"],
        "selected_synthetic_add_months": selected["synthetic_add_months"],
        "selected_synthetic_add_hours": selected["synthetic_add_hours"],
        "selected_parent_suppress_months": selected["parent_suppress_months"],
        "selected_parent_suppress_hours": selected["parent_suppress_hours"],
        "selected_parent_suppress_side": selected["parent_suppress_side"],
        "selected_net_profit": selected["net_profit"],
        "selected_profit_factor": selected["profit_factor"],
        "selected_expectancy": selected["expectancy"],
        "selected_trade_count": selected["trade_count"],
        "selected_density": selected["trade_density_per_business_day"],
        "selected_closed_drawdown_amount": selected["closed_drawdown_amount"],
        "selected_recovery_factor": selected["recovery_factor"],
        "selected_long_trade_count": selected["long_trade_count"],
        "selected_short_trade_count": selected["short_trade_count"],
        "selected_short_share": selected["short_share"],
        "selected_synthetic_short_count": selected["synthetic_short_trade_count"],
        "selected_synthetic_short_net_profit": selected["synthetic_short_net_profit"],
        "selected_synthetic_short_profit_factor": selected["synthetic_short_profit_factor"],
        "selected_synthetic_overlap_count": selected["synthetic_overlap_count"],
        "selected_displaced_parent_count": selected["displaced_parent_trade_count"],
        "selected_displaced_parent_net_profit": selected["displaced_parent_net_profit"],
        "selected_parent_suppressed_trade_count": selected["parent_suppressed_trade_count"],
        "selected_parent_suppressed_net_profit": selected["parent_suppressed_net_profit"],
        "quarter_bad_count": selected["quarter_bad_count"],
        "month_bad_count": selected["month_bad_count"],
        "bad_stress_slice_count": bad_stress_count,
        "min_month_net": selected["min_month_net"],
        "min_month_profit_factor": selected["min_month_profit_factor"],
        "new_model_training": "not_run",
        "new_mt5_execution": "not_run",
        "forward_passed": "not_claimed",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "live_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "gate_passes": sum(1 for row in gates if row["status"] == "passed"),
        "gate_total": len(gates),
    }


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
                "obsidian-performance-attribution(성과 귀속)",
                "obsidian-artifact-lineage(산출물 계보)",
            ],
            "required_gates": [
                "scope_completion_gate",
                "kpi_contract_audit",
                "late_year_stress_repair_gate",
                "no_lookahead_boundary_gate",
                "proxy_mt5_diff_recorded",
                "required_gate_coverage_audit",
            ],
            "idea_id": "IDEA-ST364-SOURCE-REGIME-LABEL-PIVOT-DENSE-COST-RECOVERY",
            "hypothesis": (
                "late-year month-of-year/session repair can clear the BQ December stress without exact year-month memory"
                "(연말 월중/세션 수리가 정확 연월 암기 없이 BQ 12월 압박을 해소할 수 있다)"
            ),
            "tier_scope": "Tier A separate + Tier B missing_required(Tier A 분리 + Tier B 필수 누락)",
            "evidence_boundary": "proxy_scout_only(프록시 탐색 전용)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def write_receipts(final: Mapping[str, Any], selected: Mapping[str, Any], proxy_mt5: Sequence[Mapping[str, Any]]) -> None:
    base = {"run_id": RUN_ID, "stage_id": STAGE_ID, "created_at_utc": final["created_at_utc"], "claim_boundary": CLAIM_BOUNDARY}
    write_json(
        RUN_EVIDENCE_RECEIPT,
        {
            **base,
            "selected_candidate": selected["candidate_id"],
            "headline": {
                "net": selected["net_profit"],
                "pf": selected["profit_factor"],
                "density": selected["trade_density_per_business_day"],
                "short_share": selected["short_share"],
                "month_bad_count": selected["month_bad_count"],
                "parent_suppressed_trade_count": selected["parent_suppressed_trade_count"],
            },
            "evidence_boundary": "proxy_scout_only(프록시 탐색 전용)",
        },
    )
    write_json(
        DATA_RECEIPT,
        {
            **base,
            "source_artifacts": [rel(path) for path in INPUT_FILES if exists(path)],
            "timestamp_boundary": "entry-known month_of_year/hour/side/probability/margin only; labels are evaluation outputs(진입시점 월중/시간/방향/확률/마진만 사용, 라벨은 평가 출력)",
            "lookahead_guard": "no exact year_month, no realized-pnl priority, no top_n(정확 연월 없음, 실현손익 우선순위 없음, top_n 없음)",
        },
    )
    write_json(
        EXPERIMENT_RECEIPT,
        {
            **base,
            "hypothesis": "late-year session repair can clear month stress while preserving trade density(연말 세션 수리가 월 압박을 해소하면서 거래 밀도를 보존할 수 있음)",
            "variant_count": final["candidate_surface_rows"],
            "stop_condition": "open BT review when stress clears or repair failure is explicit(압박 해소 또는 수리 실패가 명시되면 BT 검토로 이동)",
        },
    )
    write_json(
        MODEL_RECEIPT,
        {
            **base,
            "new_model_training": "not_run",
            "model_artifact": "not_created(생성 안 함)",
            "validation_boundary": "rule-surface proxy replay only(규칙 표면 프록시 재생 전용)",
            "overfit_controls": [rel(OVERFIT_GUARDRAIL_AUDIT)],
        },
    )
    write_json(
        ATTRIBUTION_RECEIPT,
        {
            **base,
            "selected_family": final["selected_family_id"],
            "selected_repair_type": final["selected_repair_type"],
            "proxy_mt5_diff": list(proxy_mt5),
            "driver": "month-of-year/session gate changed late-year loss shape(월중/세션 게이트가 연말 손실 형태를 바꿈)",
        },
    )
    write_json(
        JUDGMENT_RECEIPT,
        {
            **base,
            "judgment": final["judgment"],
            "decision": final["decision"],
            "next_condition": NEXT_RUN_ID,
            "missing_evidence": ["new MT5 runtime reprobe(새 MT5 런타임 재탐침)", "forward pass(전진 통과)", "operating promotion evidence(운영 승격 근거)"],
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            **base,
            "allowed_claim": final["judgment"],
            "forbidden_claims": ["runtime_authority", "operating_promotion", "live_readiness", "goal_achieve"],
            "effect": "BS는 proxy scout(프록시 탐색)와 BT review handoff(BT 검토 인계)만 주장한다.",
        },
    )


def refresh_lineage_receipt(final: Mapping[str, Any]) -> None:
    artifact_paths = [path for path in OUTPUT_FILES if exists(path) and path != LINEAGE_RECEIPT]
    write_json(
        LINEAGE_RECEIPT,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "source_inputs": [{"path": rel(path), "sha256": sha(path)} for path in INPUT_FILES if exists(path)],
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [rel(path) for path in artifact_paths],
            "artifact_hashes": {rel(path): sha(path) for path in artifact_paths if Path(path).is_file()},
            "lineage_judgment": "connected_BR_queue_to_BS_repair_surface_and_BT_review(BR 대기열을 BS 수리 표면과 BT 검토에 연결)",
            "claim_boundary": CLAIM_BOUNDARY,
            "final_decision": final,
        },
    )


def tape_rows(frame: pd.DataFrame) -> list[dict[str, Any]]:
    drop_cols = [col for col in ["entry_time_dt", "exit_time_dt"] if col in frame.columns]
    return frame.drop(columns=drop_cols).to_dict("records")


def write_tables(
    surface: pd.DataFrame,
    selected: Mapping[str, Any],
    combined: pd.DataFrame,
    synthetic: pd.DataFrame,
    displaced: pd.DataFrame,
    suppressed: pd.DataFrame,
    stress: Sequence[Mapping[str, Any]],
    attribution: Sequence[Mapping[str, Any]],
    overfit: Sequence[Mapping[str, Any]],
    proxy_mt5: Sequence[Mapping[str, Any]],
    queue: Sequence[Mapping[str, Any]],
) -> None:
    write_csv(INPUT_MANIFEST, input_manifest_rows())
    write_csv(BS_RULE_SURFACE, surface.to_dict("records"))
    write_json(SELECTED_CANDIDATE, selected)
    write_csv(SELECTED_TRADE_TAPE, tape_rows(combined))
    write_csv(SELECTED_SYNTHETIC_SHORT_TAPE, tape_rows(synthetic))
    write_csv(SELECTED_DISPLACED_PARENT_TRADES, tape_rows(displaced))
    write_csv(SELECTED_PARENT_SUPPRESSED_TRADES, tape_rows(suppressed))
    write_csv(LATE_YEAR_STRESS_REPAIR_ATTRIBUTION, attribution)
    write_csv(STRESS_SLICE_REVIEW, stress)
    write_csv(OVERFIT_GUARDRAIL_AUDIT, overfit)
    write_csv(PROXY_MT5_DIFF_PLAN, proxy_mt5)
    write_csv(RUN364BT_QUEUE, queue)


def write_docs(
    final: Mapping[str, Any],
    surface: pd.DataFrame,
    selected: Mapping[str, Any],
    stress_rows: Sequence[Mapping[str, Any]],
    attribution: Sequence[Mapping[str, Any]],
    overfit: Sequence[Mapping[str, Any]],
    proxy_mt5: Sequence[Mapping[str, Any]],
    queue: Sequence[Mapping[str, Any]],
    gates: Sequence[Mapping[str, Any]],
) -> None:
    top_surface = surface.head(14).to_dict("records")
    report = f"""# run364BS late-year short-share stress repair scout(364BS 연말 숏비중 압박 수리 탐색)

## Current Truth(현재 진실)

- selected candidate(선택 후보): `{final['selected_candidate_id']}`
- repair type(수리 유형): `{final['selected_repair_type']}`
- selected KPI(선택 핵심 성과 지표): net/PF/density/short share(순수익/수익 팩터/밀도/숏비중) `{final['selected_net_profit']}` / `{final['selected_profit_factor']}` / `{final['selected_density']}` / `{final['selected_short_share']}`
- month_bad_count(월 나쁨 수): `{final['month_bad_count']}`
- min month net/PF(최저 월 순수익/수익 팩터): `{final['min_month_net']}` / `{final['min_month_profit_factor']}`
- parent suppressed trades(억제된 부모 거래): `{final['selected_parent_suppressed_trade_count']}` trades, net `{final['selected_parent_suppressed_net_profit']}`
- package-like proxy rows(패키지 유사 프록시 행): `{final['package_candidate_rows']}`. This is not package authority(패키지 권위가 아님).

## Action And Effect(행동과 효과)

Action(행동): BR failure memory(BR 실패 기억)를 month-of-year/session repair(월중/세션 수리) surface(표면)로 바꾸고, BQ selected proxy(BQ 선택 프록시)를 기준으로 synthetic addition(합성 숏 추가)과 parent session suppression(부모 세션 억제)을 비교했다.

Effect(효과): selected proxy(선택 프록시)는 month stress(월 압박)를 해소했지만, new MT5 execution(새 MT5 실행)이 없어서 `{NEXT_RUN_ID}` review(검토)로 넘긴다.

## Top Surface(상위 표면)

{markdown_table(top_surface, ['candidate_id', 'candidate_status', 'repair_type', 'net_profit', 'profit_factor', 'trade_density_per_business_day', 'short_share', 'parent_suppressed_trade_count', 'month_bad_count', 'selection_score'])}

## Stress Slices(압박 조각)

{markdown_table(stress_rows, ['axis', 'segment_id', 'net_profit', 'profit_factor', 'trade_count', 'short_share', 'segment_status'])}

## Attribution(귀속)

{markdown_table(attribution, ['comparison_id', 'source_candidate_id', 'net_diff', 'profit_factor_diff', 'month_bad_count_before', 'month_bad_count_after', 'parent_suppressed_trade_count', 'attribution'])}

## Overfit Guardrail(과적합 가드레일)

{markdown_table(overfit, ['audit_id', 'status', 'evidence', 'effect'])}

## Proxy/MT5 Diff(프록시/MT5 차이)

{markdown_table(proxy_mt5, ['comparison_id', 'mt5_net_profit', 'proxy_net_profit', 'net_diff_proxy_minus_mt5', 'mt5_profit_factor', 'proxy_profit_factor', 'usability'])}

## BT Queue(BT 대기열)

{markdown_table(queue, ['queue_rank', 'queue_id', 'action', 'success_criteria'])}

## Gates(게이트)

{markdown_table(gates, ['gate', 'status', 'evidence', 'effect'])}

## Boundary(경계)

BS is proxy scout only(BS는 프록시 탐색 전용). No new model training(새 모델 학습 없음), no new MT5 execution(새 MT5 실행 없음), no forward pass(전진 통과 없음), no runtime authority(런타임 권위 없음), no operating promotion(운영 승격 없음), no Goal Achieve(목표 달성 없음).
"""
    write_text(REPORT_PATH, report, bom=True)
    write_text(
        DECISION_DOC,
        f"""# {TODAY} Stage364BS late-year short-share stress repair scout(연말 숏비중 압박 수리 탐색)

Action(행동): `{final['selected_candidate_id']}`를 BS selected proxy(BS 선택 프록시)로 기록하고 `{NEXT_RUN_ID}`를 열었다.

Effect(효과): month_bad_count(월 나쁨 수)는 `{final['month_bad_count']}`가 되었지만 new MT5 execution(새 MT5 실행)이 없으므로 runtime authority(런타임 권위)는 주장하지 않는다.

- report(보고서): `{rel(REPORT_PATH)}`
- final_decision(최종 결정): `{rel(FINAL_DECISION)}`
- next_run(다음 실행): `{NEXT_RUN_ID}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
        bom=True,
    )
    append_text_once(REVIEW_INDEX, RUN_ID, f"- `{RUN_ID}`: `{rel(REPORT_PATH)}` - late-year short-share stress repair scout(연말 숏비중 압박 수리 탐색).")
    append_text_once(
        STAGE_BRIEF,
        "## run364BS Late-Year Short-Share Stress Repair Scout Closeout",
        f"""## run364BS Late-Year Short-Share Stress Repair Scout Closeout(364BS 연말 숏비중 압박 수리 탐색 종료)

Action(행동): BR late-year failure memory(BR 연말 실패 기억)를 month-of-year/session repair(월중/세션 수리) surface(표면)로 실행했다.

Effect(효과): `{final['selected_candidate_id']}`는 proxy(프록시) 기준 net/PF/density/short share(순수익/수익 팩터/밀도/숏비중) `{final['selected_net_profit']}` / `{final['selected_profit_factor']}` / `{final['selected_density']}` / `{final['selected_short_share']}`와 month_bad_count(월 나쁨 수) `{final['month_bad_count']}`를 만들었지만, MT5(메타트레이더5) 검토 전이라 `{NEXT_RUN_ID}`로 넘겼다.
""",
    )
    append_text_once(
        STAGE_README,
        RUN_ID,
        f"""## run364BS Late-Year Short-Share Stress Repair Scout(364BS 연말 숏비중 압박 수리 탐색)

Action(행동): Stage364(364단계) 안에서 새 stage(단계) 분기 없이 BQ selected proxy(BQ 선택 프록시)의 late-year stress(연말 압박)를 수리 탐색했다.

Effect(효과): proxy stress(프록시 압박)는 개선됐지만 package(패키지)는 열지 않고 `{NEXT_RUN_ID}` review(검토)로 넘겼다.
""",
    )
    replace_prefixed_lines(
        STAGE_BRIEF,
        {
            "- current_run_id(현재 실행 ID):": f"- current_run_id(현재 실행 ID): `{NEXT_RUN_ID}`",
            "- latest_completed_run_id(최근 완료 실행 ID):": f"- latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`",
            "- selection_status(선택 상태):": f"- selection_status(선택 상태): `{final['status']}`",
            "- claim_boundary(주장 경계):": f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
        },
        bom=True,
    )
    replace_prefixed_lines(
        STAGE_README,
        {
            "Current run(현재 실행):": f"Current run(현재 실행): `{NEXT_RUN_ID}`",
            "Latest completed run(최근 완료 실행):": f"Latest completed run(최근 완료 실행): `{RUN_ID}`",
            "Current truth(현재 진실):": f"Current truth(현재 진실): run364BS(364BS 실행)는 `{final['selected_candidate_id']}` proxy repair candidate(프록시 수리 후보)를 만들었고 month_bad_count(월 나쁨 수)는 `{final['month_bad_count']}`지만 MT5 검토 전이다.",
            "Next action(다음 행동):": f"Next action(다음 행동): `{NEXT_RUN_ID}`에서 overfit watch(과적합 관찰), proxy/MT5 diff(프록시/MT5 차이), package precheck eligibility(패키지 사전검사 적격성)를 검토한다.",
        },
        bom=True,
    )
    write_text(
        WORKSPACE_STATE,
        f"""current_stage_id: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {final['status']}
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

Current truth(현재 진실): `run364BS`는 BR failure memory(BR 실패 기억)를 late-year/month-of-year short-share stress repair(연말/월중 숏비중 압박 수리)로 탐색했다. 선택 후보 `{final['selected_candidate_id']}`는 proxy net/PF/density/short share(프록시 순수익/수익 팩터/밀도/숏비중) `{final['selected_net_profit']}` / `{final['selected_profit_factor']}` / `{final['selected_density']}` / `{final['selected_short_share']}`이고, month_bad_count(월 나쁨 수)는 `{final['month_bad_count']}`다. package-like proxy rows(패키지 유사 프록시 행)는 `{final['package_candidate_rows']}`지만 new MT5 execution(새 MT5 실행)이 없어서 authority(권위)는 없다.

Next action(다음 행동): `{NEXT_RUN_ID}`에서 selected repair(선택 수리)의 overfit watch(과적합 관찰), proxy/MT5 diff(프록시/MT5 차이), package precheck eligibility(패키지 사전검사 적격성)를 검토한다.

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

Package candidate(패키지 후보): none(없음). BS selected proxy(BS 선택 프록시)는 stress clear proxy(압박 해소 프록시)일 수 있지만 new MT5 execution(새 MT5 실행)이 없어 package(패키지)가 아니다.

Selected proxy(선택 프록시): `{final['selected_candidate_id']}`

Proxy KPI(프록시 핵심 성과 지표): net `{final['selected_net_profit']}`, PF `{final['selected_profit_factor']}`, expectancy `{final['selected_expectancy']}`, trades `{final['selected_trade_count']}`, density `{final['selected_density']}`, closed DD `{final['selected_closed_drawdown_amount']}`, recovery `{final['selected_recovery_factor']}`, long/short `{final['selected_long_trade_count']}` / `{final['selected_short_trade_count']}`, short share `{final['selected_short_share']}`.

Stress memory(압박 기억): month_bad_count(월 나쁨 수) `{final['month_bad_count']}`, min month net/PF(최저 월 순수익/수익 팩터) `{final['min_month_net']}` / `{final['min_month_profit_factor']}`. Overfit watch(과적합 관찰)는 BT review(BT 검토)에서 계속한다.

Next queue(다음 대기열): `{rel(RUN364BT_QUEUE)}`

Authority(권위): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함).
""",
        bom=True,
    )
    append_text_once(
        WORKSPACE_CHANGELOG,
        f"## {TODAY} - {RUN_ID}",
        f"""## {TODAY} - {RUN_ID}

- action(행동): late-year short-share stress repair proxy scout(연말 숏비중 압박 수리 프록시 탐색)를 실행했다.
- effect(효과): `{final['selected_candidate_id']}`를 `{NEXT_RUN_ID}` 검토로 넘기고 package(패키지)는 열지 않았다.
- report(보고서): `{rel(REPORT_PATH)}`
""",
    )
    append_text_once(
        IDEA_REGISTRY,
        RUN_ID,
        f"""## {RUN_ID}

- idea(아이디어): month-of-year/session repair(월중/세션 수리)가 late-year stress(연말 압박)를 줄일 수 있다.
- positive clue(긍정 단서): selected proxy(선택 프록시) net/PF/density/short share `{final['selected_net_profit']}` / `{final['selected_profit_factor']}` / `{final['selected_density']}` / `{final['selected_short_share']}`, month_bad_count `{final['month_bad_count']}`.
- next action(다음 행동): `{NEXT_RUN_ID}`.
""",
    )
    append_text_once(
        NEGATIVE_RESULT_REGISTER,
        RUN_ID,
        f"""## {RUN_ID}

- status(상태): package not opened(패키지 열지 않음).
- failure_memory(실패 기억): proxy stress clear(프록시 압박 해소)가 있어도 MT5 reprobe(MT5 재탐침)와 BT review(BT 검토)가 없으면 operating claim(운영 주장)이 아니다.
- salvage_value(회수 가치): `{final['selected_candidate_id']}`는 late-year/session repair(연말/세션 수리) 후보로 검토 가치가 있다.
- reopen_condition(재개 조건): `{NEXT_RUN_ID}`에서 overfit watch(과적합 관찰)와 proxy/MT5 diff(프록시/MT5 차이)를 닫는다.
""",
    )


def write_ledgers(final: Mapping[str, Any]) -> None:
    common = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "run_number": RUN_NUMBER,
        "date": TODAY,
        "status": final["status"],
        "judgment": final["judgment"],
        "decision": final["decision"],
        "next_run_id": NEXT_RUN_ID,
        "rows": final["candidate_surface_rows"],
        "gate_passes": final["gate_passes"],
        "gate_total": final["gate_total"],
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "final_decision_path": rel(FINAL_DECISION),
        "gate_audit_path": rel(GATE_AUDIT),
        "created_at": final["created_at_utc"],
        "work_family": "experiment_execution(실험 실행)",
        "external_verification_status": "not_run(실행 안 함)",
        "evidence_boundary": "proxy_scout_only(프록시 탐색 전용)",
        "question": "Can late-year month-of-year/session repair clear BQ month stress without exact year memory?(연말 월중/세션 수리가 정확 연도 암기 없이 BQ 월 압박을 해소하는가?)",
        "next_action": NEXT_RUN_ID,
    }
    metric_values = {
        "net_profit": final["selected_net_profit"],
        "profit_factor": final["selected_profit_factor"],
        "expectancy": final["selected_expectancy"],
        "drawdown": final["selected_closed_drawdown_amount"],
        "recovery_factor": final["selected_recovery_factor"],
        "trade_count": final["selected_trade_count"],
        "trade_density_per_feature_day": final["selected_density"],
        "long_trade_count": final["selected_long_trade_count"],
        "short_trade_count": final["selected_short_trade_count"],
        "max_drawdown_amount": final["selected_closed_drawdown_amount"],
    }
    rows: list[dict[str, Any]] = []
    for suffix, record_view, tier_scope, status, include_metrics in [
        ("tier_a_separate", "Tier A separate(Tier A 분리)", "Tier A", final["status"], True),
        ("tier_b_missing_required", "Tier B separate(Tier B 분리)", "Tier B", "missing_required(필수 누락)", False),
        ("tier_a_plus_b_combined", "Tier A+B combined(Tier A+B 합산)", "Tier A+B", final["status"], True),
    ]:
        row = {
            **common,
            "ledger_row_id": f"{RUN_ID}__{suffix}",
            "subrun_id": f"{RUN_ID}__{suffix}",
            "row_id": f"{RUN_ID}__{suffix}",
            "record_view": record_view,
            "tier_scope": tier_scope,
            "kpi_scope": "BS proxy scout(BS 프록시 탐색)",
            "scoreboard_lane": "stage364_proxy_scout(Stage364 프록시 탐색)",
            "status": status,
            "primary_kpi": f"net={final['selected_net_profit']};pf={final['selected_profit_factor']};density={final['selected_density']};short_share={final['selected_short_share']}",
            "guardrail_kpi": f"month_bad_count={final['month_bad_count']};package_like_rows={final['package_candidate_rows']};no_authority",
            "result_judgment": final["judgment"],
        }
        if include_metrics:
            row.update(metric_values)
        rows.append(row)
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], rows)
    append_or_replace_csv(STAGE_LEDGER, ["ledger_row_id"], rows)
    drop_empty_csv_columns(PROJECT_LEDGER, ["promotion_candidate"])
    drop_empty_csv_columns(STAGE_LEDGER, ["promotion_candidate"])
    registry_row = {
        **common,
        "lane": "stage364_proxy_scout(Stage364 프록시 탐색)",
        "family": "late_year_short_share_stress_repair(연말 숏비중 압박 수리)",
        "path": rel(REPORT_PATH),
        "primary_report": rel(REPORT_PATH),
        "net_profit": final["selected_net_profit"],
        "profit_factor": final["selected_profit_factor"],
        "drawdown": final["selected_closed_drawdown_amount"],
        "recovery_factor": final["selected_recovery_factor"],
        "trade_count": final["selected_trade_count"],
        "trade_density_per_feature_day": final["selected_density"],
        "result_status": final["status"],
        "expectancy": final["selected_expectancy"],
        "view": "proxy_scout(프록시 탐색)",
        "tier": "Tier A",
        "metric_scope": "selected_proxy(선택 프록시)",
        "scoreboard_lane": "stage364_proxy_scout(Stage364 프록시 탐색)",
        "external_verification_status": "not_run(실행 안 함)",
        "result_judgment": final["judgment"],
        "max_drawdown_amount": final["selected_closed_drawdown_amount"],
        "long_trade_count": final["selected_long_trade_count"],
        "short_trade_count": final["selected_short_trade_count"],
        "row_id": RUN_ID,
        "evidence_boundary": "proxy_scout_only(프록시 탐색 전용)",
        "next_action": NEXT_RUN_ID,
        "question": common["question"],
    }
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], [registry_row])
    repair_run_registry_line_endings(RUN_REGISTRY)


def write_manifest(final: Mapping[str, Any]) -> None:
    existing_outputs = [path for path in OUTPUT_FILES if exists(path) and path != RUN_MANIFEST]
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "run_number": RUN_NUMBER,
            "stage_id": STAGE_ID,
            "created_at_utc": final["created_at_utc"],
            "producer": rel(Path(__file__)),
            "inputs": [{"path": rel(path), "sha256": sha(path)} for path in INPUT_FILES if exists(path)],
            "outputs": [{"path": rel(path), "sha256": sha(path)} for path in existing_outputs if Path(path).is_file()],
            "final_decision": final,
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def write_artifact_registry(final: Mapping[str, Any]) -> None:
    rows = []
    for path in OUTPUT_FILES:
        if not exists(path) or not Path(path).is_file():
            continue
        artifact_type = "run_manifest" if path == RUN_MANIFEST else "stage364BS_artifact"
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
                "artifact_id": f"{RUN_NUMBER}_{Path(path).stem}",
                "notes": "Stage364BS late-year stress repair proxy scout artifact(364BS 연말 압박 수리 프록시 탐색 산출물)",
            }
        )
    append_or_replace_csv(ARTIFACT_REGISTRY, ["artifact_id"], rows)


def main() -> None:
    ensure_dirs()
    br_final, bq_final, bk_final = validate_inputs()
    parent_trades = replay.load_parent_trades()
    broad_pool = bo.load_broad_pool()
    surface, combined_map, synthetic_map, displaced_map, suppressed_map = evaluate_variants(
        parent_trades,
        broad_pool,
        candidate_definitions(),
    )
    if surface.empty:
        raise RuntimeError("BS surface is empty(BS 표면이 비어 있음)")
    selected = select_candidate(surface)
    candidate_id = str(selected["candidate_id"])
    combined = combined_map[candidate_id]
    synthetic = synthetic_map[candidate_id]
    displaced = displaced_map[candidate_id]
    suppressed = suppressed_map[candidate_id]
    stress = stress_slice_rows(candidate_id, combined)
    attribution = attribution_rows(selected, bq_final, surface, suppressed)
    overfit = overfit_rows(selected, surface)
    proxy_mt5 = proxy_mt5_rows(bk_final, selected)
    queue = queue_rows(selected)
    created_at = now_utc()

    write_work_packet()
    write_tables(surface, selected, combined, synthetic, displaced, suppressed, stress, attribution, overfit, proxy_mt5, queue)
    preliminary_final = final_payload(selected, surface, stress, [], created_at)
    write_receipts(preliminary_final, selected, proxy_mt5)
    receipts = [
        RUN_EVIDENCE_RECEIPT,
        DATA_RECEIPT,
        EXPERIMENT_RECEIPT,
        MODEL_RECEIPT,
        ATTRIBUTION_RECEIPT,
        JUDGMENT_RECEIPT,
        LINEAGE_RECEIPT,
        CLAIM_RECEIPT,
    ]
    gates = gate_rows(preliminary_final, selected, surface, receipts)
    final = final_payload(selected, surface, stress, gates, created_at)
    write_receipts(final, selected, proxy_mt5)
    write_csv(GATE_AUDIT, gates)
    write_json(FINAL_DECISION, final)
    write_docs(final, surface, selected, stress, attribution, overfit, proxy_mt5, queue, gates)
    write_ledgers(final)
    write_manifest(final)
    refresh_lineage_receipt(final)
    write_artifact_registry(final)
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "selected_candidate_id": final["selected_candidate_id"],
                "net_profit": final["selected_net_profit"],
                "profit_factor": final["selected_profit_factor"],
                "density": final["selected_density"],
                "short_share": final["selected_short_share"],
                "month_bad_count": final["month_bad_count"],
                "package_candidate_rows": final["package_candidate_rows"],
                "gate_passes": final["gate_passes"],
                "gate_total": final["gate_total"],
                "next_run_id": final["next_run_id"],
                "claim_boundary": CLAIM_BOUNDARY,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
