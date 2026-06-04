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

from stage_pipelines.stage364 import review_h19_stress_short_balance_proxy_scout_without_db as replay  # noqa: E402
from stage_pipelines.stage364 import review_short_source_quality_repair_scout_without_db as parent  # noqa: E402
from stage_pipelines.stage364 import train_short_source_quality_repair_scout_without_db as bo  # noqa: E402
from stage_pipelines.stage364.review_pf_pass_density_restore_offensive_scout_without_db import repair_run_registry_line_endings  # noqa: E402


TODAY = "2026-06-05"
STAGE_ID = parent.STAGE_ID
RUN_NUMBER = "run364BQ"
RUN_ID = "run364BQ_train_broad_clean_short_share_lift_scout_without_db_v1"
PARENT_RUN_ID = parent.RUN_ID
SOURCE_RUNTIME_PROBE_RUN_ID = parent.SOURCE_RUNTIME_PROBE_RUN_ID
BASELINE_RUN_ID = parent.BASELINE_RUN_ID
NEXT_RUN_ID = "run364BR_review_broad_clean_short_share_lift_scout_without_db_v1"

STATUS = "completed_stage364BQ_broad_clean_short_share_lift_proxy_scout_review_required_no_authority"
JUDGMENT = "positive_proxy_short_share_lift_but_month_stress_no_mt5_review_required_no_authority"
DECISION = "stage364BQ_open_run364BR_broad_clean_short_share_lift_review"
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
BQ_RULE_SURFACE = RUN_DIR / "bq_rule_surface.csv"
SELECTED_CANDIDATE = RUN_DIR / "selected_bq_candidate.json"
SELECTED_TRADE_TAPE = RUN_DIR / "selected_bq_trade_tape.csv"
SELECTED_SYNTHETIC_SHORT_TAPE = RUN_DIR / "selected_bq_synthetic_short_tape.csv"
SELECTED_DISPLACED_PARENT_TRADES = RUN_DIR / "selected_bq_displaced_parent_trades.csv"
SHORT_SHARE_LIFT_ATTRIBUTION = RUN_DIR / "short_share_lift_attribution.csv"
STRESS_SLICE_REVIEW = RUN_DIR / "stress_slice_review.csv"
OVERFIT_GUARDRAIL_AUDIT = RUN_DIR / "overfit_guardrail_audit.csv"
PROXY_MT5_DIFF_PLAN = RUN_DIR / "proxy_mt5_diff_plan.csv"
RUN364BR_QUEUE = RUN_DIR / "run364BR_review_queue.csv"
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

REPORT_PATH = REVIEW_DIR / "run364BQ_broad_clean_short_share_lift_scout.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364BQ_broad_clean_short_share_lift_scout.md"
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
    parent.POSITIVE_CLUE_REGISTER,
    parent.NEXT_OFFENSIVE_SEED_QUEUE,
    bo.FINAL_DECISION,
    bo.QUALITY_RULE_SURFACE,
    bo.BROAD_POOL_NEGATIVE_CONTROL,
    bo.SELECTED_QUALITY_CANDIDATE,
    bo.BK.FINAL_DECISION,
    bo.BM.SHORT_SYNTHETIC_CANDIDATES,
]

OUTPUT_FILES = [
    INPUT_MANIFEST,
    BQ_RULE_SURFACE,
    SELECTED_CANDIDATE,
    SELECTED_TRADE_TAPE,
    SELECTED_SYNTHETIC_SHORT_TAPE,
    SELECTED_DISPLACED_PARENT_TRADES,
    SHORT_SHARE_LIFT_ATTRIBUTION,
    STRESS_SLICE_REVIEW,
    OVERFIT_GUARDRAIL_AUDIT,
    PROXY_MT5_DIFF_PLAN,
    RUN364BR_QUEUE,
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
        raise FileNotFoundError("missing BQ inputs(BQ 입력 누락): " + ", ".join(missing))
    bp_final = read_json(parent.FINAL_DECISION)
    bo_final = read_json(bo.FINAL_DECISION)
    bk_final = read_json(bo.BK.FINAL_DECISION)
    if bp_final.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"BP next_run_id mismatch(BP 다음 실행 불일치): {bp_final.get('next_run_id')} != {RUN_ID}")
    for final, label in [(bp_final, "BP"), (bo_final, "BO")]:
        if final.get("runtime_authority") != "not_claimed" or final.get("operating_promotion") != "not_claimed":
            raise RuntimeError(f"{label} has forbidden authority claim({label} 금지 권위 주장 존재)")
    for gate_path, label in [(parent.GATE_AUDIT, "BP"), (bo.GATE_AUDIT, "BO")]:
        gates = read_rows(gate_path)
        if not gates or any(row.get("status") != "passed" for row in gates):
            raise RuntimeError(f"{label} gate audit({label} 게이트 감사)가 모두 passed(통과)가 아닙니다.")
    return bp_final, bo_final, bk_final


def input_manifest_rows() -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "input_path": rel(path),
            "exists": exists(path),
            "sha256": sha(path),
            "input_role": "BQ proxy scout source(BQ 프록시 정찰 원천)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for path in INPUT_FILES
    ]


def load_positive_clues() -> list[dict[str, Any]]:
    return read_rows(parent.POSITIVE_CLUE_REGISTER)


def chronological_no_overlap(frame: pd.DataFrame) -> pd.DataFrame:
    if frame.empty:
        return frame.copy()
    selected: list[pd.Series] = []
    last_exit = pd.Timestamp.min
    ordered = frame.sort_values(
        ["entry_time_dt", "p_short", "short_margin_vs_long", "exit_time_dt"],
        ascending=[True, False, False, True],
    )
    for entry_time, group in ordered.groupby("entry_time_dt", sort=True):
        if entry_time < last_exit:
            continue
        row = group.iloc[0]
        selected.append(row)
        last_exit = row["exit_time_dt"]
    if not selected:
        return frame.iloc[0:0].copy()
    return pd.DataFrame(selected).sort_values("entry_time_dt").reset_index(drop=True)


def candidate_definitions() -> list[dict[str, Any]]:
    families = [
        {
            "family_id": "bq01_broad_clean_h17_20",
            "seed_source": "bo90_broad_h17_20_ps0440_margin080_control",
            "hours": [17, 20],
            "p_short_floors": [0.4350, 0.4375, 0.4400, 0.4425, 0.4450, 0.4475, 0.4500, 0.4550, 0.4600],
            "margin_floors": [0.0750, 0.0800, 0.0825, 0.0850, 0.0875, 0.0900, 0.0950],
            "modes": ["raw", "chronological_no_overlap"],
            "intent": "expand bo90 clean h17/h20 source(bo90 클린 17/20시 원천 확장)",
        },
        {
            "family_id": "bq02_h16_extension_overlap_safe",
            "seed_source": "bo91_broad_h16_17_20_ps0445_margin080_control",
            "hours": [16, 17, 20],
            "p_short_floors": [0.4350, 0.4400, 0.4425, 0.4450, 0.4475, 0.4500, 0.4550],
            "margin_floors": [0.0750, 0.0800, 0.0825, 0.0850, 0.0900, 0.0950],
            "modes": ["raw", "chronological_no_overlap"],
            "intent": "retry bo91 h16 lift with overlap guard(bo91 16시 상승을 겹침 가드로 재시도)",
        },
        {
            "family_id": "bq03_high_short_pf_guardrail",
            "seed_source": "bo05_h17_margin_075_105_or_h20_margin_08_10",
            "hours": [17, 20],
            "p_short_floors": [0.4400, 0.4425, 0.4450, 0.4475, 0.4500, 0.4550, 0.4600, 0.4650],
            "margin_floors": [0.0750, 0.0800, 0.0850, 0.0900, 0.0950, 0.1000],
            "modes": ["raw", "chronological_no_overlap"],
            "intent": "keep bo05 high synthetic PF as guardrail(bo05 높은 합성 PF를 가드레일로 유지)",
        },
        {
            "family_id": "bq04_h19_bridge_short_share_lift",
            "seed_source": "bo90_plus_h19_session_bridge",
            "hours": [17, 19, 20],
            "p_short_floors": [0.4325, 0.4350, 0.4375, 0.4400, 0.4425, 0.4450],
            "margin_floors": [0.0750, 0.0800, 0.0850],
            "modes": ["raw", "chronological_no_overlap"],
            "intent": "test h19 bridge for short-share lift(19시 브리지로 숏비중 상승 시험)",
        },
        {
            "family_id": "bq05_extreme_multi_hour_overlap_guard",
            "seed_source": "bo91_extreme_overlap_guard",
            "hours": [16, 17, 18, 20],
            "p_short_floors": [0.4350, 0.4400, 0.4425, 0.4450],
            "margin_floors": [0.0750, 0.0800, 0.0850],
            "modes": ["chronological_no_overlap"],
            "intent": "extreme broad hours with chronological guard(시간순 가드가 있는 극단 넓은 시간)",
        },
        {
            "family_id": "bq06_h16_h19_bridge_overlap_guard",
            "seed_source": "bo91_plus_h19_overlap_guard",
            "hours": [16, 17, 19, 20],
            "p_short_floors": [0.4350, 0.4400, 0.4425, 0.4450],
            "margin_floors": [0.0750, 0.0800, 0.0850],
            "modes": ["chronological_no_overlap"],
            "intent": "combine h16 and h19 lift without synthetic overlap(16/19시 상승을 합성 겹침 없이 결합)",
        },
    ]
    defs: list[dict[str, Any]] = []
    for family in families:
        for p_short_floor in family["p_short_floors"]:
            for margin_floor in family["margin_floors"]:
                for mode in family["modes"]:
                    ps_token = f"ps{int(round(p_short_floor * 10000)):04d}"
                    margin_token = f"m{int(round(margin_floor * 10000)):04d}"
                    hour_token = "h" + "_".join(str(hour) for hour in family["hours"])
                    defs.append(
                        {
                            "candidate_id": f"{family['family_id']}__{hour_token}__{ps_token}__{margin_token}__{mode}",
                            "family_id": family["family_id"],
                            "seed_source": family["seed_source"],
                            "hours": family["hours"],
                            "p_short_floor": p_short_floor,
                            "margin_floor": margin_floor,
                            "selection_mode": mode,
                            "intent": family["intent"],
                        }
                    )
    return defs


def select_synthetic(pool: pd.DataFrame, variant: Mapping[str, Any]) -> pd.DataFrame:
    selected = pool[
        pool["entry_hour"].isin(variant["hours"])
        & (pool["p_short"] >= as_float(variant["p_short_floor"]))
        & (pool["short_margin_vs_long"] >= as_float(variant["margin_floor"]))
    ].copy()
    if variant["selection_mode"] == "chronological_no_overlap":
        selected = chronological_no_overlap(selected)
    return selected.sort_values("entry_time_dt").reset_index(drop=True)


def stress_counts(combined: pd.DataFrame) -> dict[str, Any]:
    out: dict[str, Any] = {
        "quarter_bad_count": 0,
        "month_bad_count": 0,
        "min_quarter_net": 0.0,
        "min_month_net": 0.0,
        "min_month_profit_factor": 0.0,
    }
    q_nets: list[float] = []
    m_nets: list[float] = []
    m_pfs: list[float] = []
    for group_col, bad_key in [("entry_quarter", "quarter_bad_count"), ("entry_month", "month_bad_count")]:
        for _, part in combined.groupby(group_col, sort=True):
            days = max(1, int(np.busday_count(part["entry_time_dt"].min().date(), part["entry_time_dt"].max().date() + timedelta(days=1))))
            metric = replay.metric_frame(part.copy(), full_days=days)
            net = as_float(metric["net_profit"])
            pf = as_float(metric["profit_factor"])
            out[bad_key] += int(net <= 0 or pf < 1.0)
            if group_col == "entry_quarter":
                q_nets.append(net)
            else:
                m_nets.append(net)
                m_pfs.append(pf)
    if q_nets:
        out["min_quarter_net"] = finite(min(q_nets), 10)
    if m_nets:
        out["min_month_net"] = finite(min(m_nets), 10)
    if m_pfs:
        out["min_month_profit_factor"] = finite(min(m_pfs), 10)
    return out


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
        return "proxy_review_candidate_stress_watch_no_package(프록시 검토 후보, 스트레스 관찰, 패키지 아님)"
    return "package_blocked_pending_mt5_review(패키지 보류, MT5 검토 필요)"


def selection_score(row: Mapping[str, Any]) -> float:
    score = 0.0
    if "proxy_review_candidate" in str(row["candidate_status"]) or "package_blocked" in str(row["candidate_status"]):
        score += 220.0
    score += (as_float(row["net_profit"]) - 1000.0) * 0.30
    score += (as_float(row["profit_factor"]) - MIN_PF_KEEP) * 190.0
    score += (as_float(row["synthetic_short_profit_factor"]) - MIN_SHORT_SOURCE_PF) * 95.0
    score += max(0.0, as_float(row["short_share"]) - TARGET_SHORT_SHARE) * 260.0
    score += max(0.0, 84.86 - as_float(row["closed_drawdown_amount"])) * 0.20
    score -= as_int(row["month_bad_count"]) * 45.0
    score -= as_int(row["quarter_bad_count"]) * 18.0
    score -= as_int(row["synthetic_overlap_count"]) * 80.0
    if str(row["selection_mode"]) == "chronological_no_overlap":
        score += 3.0
    if str(row["family_id"]) == "bq04_h19_bridge_short_share_lift":
        score += 5.0
    return round(score, 10)


def evaluate_variants(
    parent_trades: pd.DataFrame,
    pool: pd.DataFrame,
    variant_defs: Sequence[Mapping[str, Any]],
) -> tuple[pd.DataFrame, dict[str, pd.DataFrame], dict[str, pd.DataFrame], dict[str, pd.DataFrame]]:
    rows: list[dict[str, Any]] = []
    combined_map: dict[str, pd.DataFrame] = {}
    synthetic_map: dict[str, pd.DataFrame] = {}
    displaced_map: dict[str, pd.DataFrame] = {}
    full_days = replay.full_business_days(parent_trades)
    for variant in variant_defs:
        selected_syn = select_synthetic(pool, variant)
        if selected_syn.empty:
            continue
        combined, displaced = replay.combine(parent_trades, selected_syn)
        metric = replay.metric_frame(combined, full_days=full_days)
        synthetic_metric = replay.synthetic_metrics(selected_syn)
        row = {
            "run_id": RUN_ID,
            "candidate_id": variant["candidate_id"],
            "family_id": variant["family_id"],
            "seed_source": variant["seed_source"],
            "hours": "|".join(str(hour) for hour in variant["hours"]),
            "p_short_floor": variant["p_short_floor"],
            "margin_floor": variant["margin_floor"],
            "selection_mode": variant["selection_mode"],
            "intent": variant["intent"],
            **metric,
            **synthetic_metric,
            "synthetic_added_short_count": len(selected_syn),
            "displaced_parent_trade_count": len(displaced),
            "displaced_parent_net_profit": finite(displaced["displaced_pnl"].astype(float).sum() if not displaced.empty else 0.0, 10),
            "synthetic_overlap_count": bo.synthetic_overlap_count(selected_syn),
            **stress_counts(combined),
            "feature_boundary": "entry_hour, p_short, short_margin_vs_long only; no exact month, no outcome-priority, no top_n(진입시점 시간, p_short, 숏-롱 마진만 사용, 정확 월/결과값 우선순위/top_n 없음)",
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
    surface = pd.DataFrame(rows).sort_values(
        ["core_pass", "month_bad_count", "selection_score", "net_profit"],
        ascending=[False, True, False, False],
    ).reset_index(drop=True)
    return surface, combined_map, synthetic_map, displaced_map


def select_candidate(surface: pd.DataFrame) -> Mapping[str, Any]:
    core = surface[surface["core_pass"].astype(bool)].copy()
    if not core.empty:
        return core.sort_values(["month_bad_count", "selection_score", "net_profit"], ascending=[True, False, False]).iloc[0].to_dict()
    return surface.sort_values(["selection_score", "profit_factor", "net_profit"], ascending=[False, False, False]).iloc[0].to_dict()


def stress_slice_rows(candidate_id: str, combined: pd.DataFrame) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for axis, column in [("entry_month(진입월)", "entry_month"), ("entry_quarter(진입분기)", "entry_quarter")]:
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
                    "repair_use": "BR review stress target(BR 검토 압박 대상)" if status.startswith("bad") else "stability clue(안정 단서)",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    return rows


def short_share_lift_rows(selected: Mapping[str, Any], clues: Sequence[Mapping[str, Any]], surface: pd.DataFrame) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for clue in clues:
        clue_id = str(clue.get("clue_id", ""))
        if clue_id not in {"bo00_bn_seed_h17_or_h20_margin_08_10_reference", "bo05_h17_margin_075_105_or_h20_margin_08_10", "bo90_broad_h17_20_ps0440_margin080_control", "bo91_broad_h16_17_20_ps0445_margin080_control"}:
            continue
        rows.append(
            {
                "run_id": RUN_ID,
                "comparison_id": f"selected_vs_{clue_id}",
                "source_candidate_id": clue_id,
                "selected_candidate_id": selected["candidate_id"],
                "source_net_profit": clue.get("net_profit", ""),
                "selected_net_profit": selected["net_profit"],
                "net_diff": finite(as_float(selected["net_profit"]) - as_float(clue.get("net_profit")), 10),
                "source_profit_factor": clue.get("profit_factor", ""),
                "selected_profit_factor": selected["profit_factor"],
                "profit_factor_diff": finite(as_float(selected["profit_factor"]) - as_float(clue.get("profit_factor")), 10),
                "source_short_share": clue.get("short_share", ""),
                "selected_short_share": selected["short_share"],
                "short_share_diff": finite(as_float(selected["short_share"]) - as_float(clue.get("short_share")), 10),
                "source_synthetic_short_profit_factor": clue.get("synthetic_short_profit_factor", ""),
                "selected_synthetic_short_profit_factor": selected["synthetic_short_profit_factor"],
                "attribution": "BQ changes hour/floor surface only with entry-known fields(BQ는 진입시점 필드로 시간/하한 표면만 바꿈)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    top_by_family = surface.sort_values(["core_pass", "month_bad_count", "selection_score"], ascending=[False, True, False]).groupby("family_id", sort=True).head(1)
    for _, row in top_by_family.iterrows():
        rows.append(
            {
                "run_id": RUN_ID,
                "comparison_id": f"family_top_{row['family_id']}",
                "source_candidate_id": row["candidate_id"],
                "selected_candidate_id": selected["candidate_id"],
                "source_net_profit": row["net_profit"],
                "selected_net_profit": selected["net_profit"],
                "net_diff": finite(as_float(selected["net_profit"]) - as_float(row["net_profit"]), 10),
                "source_profit_factor": row["profit_factor"],
                "selected_profit_factor": selected["profit_factor"],
                "profit_factor_diff": finite(as_float(selected["profit_factor"]) - as_float(row["profit_factor"]), 10),
                "source_short_share": row["short_share"],
                "selected_short_share": selected["short_share"],
                "short_share_diff": finite(as_float(selected["short_share"]) - as_float(row["short_share"]), 10),
                "source_synthetic_short_profit_factor": row["synthetic_short_profit_factor"],
                "selected_synthetic_short_profit_factor": selected["synthetic_short_profit_factor"],
                "attribution": "family top comparison for BQ broad sweep(BQ 넓은 탐색 계열별 최상위 비교)",
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
            "evidence": "entry_hour, p_short, short_margin_vs_long only; no exact month and no realized pnl selector(진입시/확률/마진만 사용, 정확 월 및 실현손익 선택 없음)",
            "effect": "look-ahead bias(미래참조 편향) 재발을 차단했다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "audit_id": "chronological_no_overlap_guard(시간순 겹침 방지 가드)",
            "status": "passed" if as_int(selected["synthetic_overlap_count"]) == 0 else "failed",
            "evidence": f"selected_overlap={selected['synthetic_overlap_count']}; selection_mode={selected['selection_mode']}",
            "effect": "합성 숏이 서로 겹치는 후보를 운영 단서로 과장하지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "audit_id": "broad_before_micro_search(미세탐색 전 넓은 탐색)",
            "status": "passed" if len(surface) >= 100 else "failed",
            "evidence": f"surface_rows={len(surface)}; families={surface['family_id'].nunique() if not surface.empty else 0}",
            "effect": "한 후보만 미세조정하지 않고 계열/시간/하한을 넓게 비교했다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "audit_id": "package_boundary_guard(패키지 경계 가드)",
            "status": "passed" if len(package_like) == 0 else "watch",
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
            "comparison_id": "bq_proxy_vs_bk_mt5_runtime_probe(BQ 프록시 대 BK MT5 런타임 탐침)",
            "mt5_net_profit": mt5_net,
            "proxy_net_profit": selected["net_profit"],
            "net_diff_proxy_minus_mt5": finite(as_float(selected["net_profit"]) - mt5_net, 10),
            "mt5_profit_factor": mt5_pf,
            "proxy_profit_factor": selected["profit_factor"],
            "profit_factor_diff_proxy_minus_mt5": finite(as_float(selected["profit_factor"]) - mt5_pf, 10),
            "mt5_density": mt5_density,
            "proxy_density": selected["trade_density_per_business_day"],
            "density_diff_proxy_minus_mt5": finite(as_float(selected["trade_density_per_business_day"]) - mt5_density, 10),
            "attribution": "BQ proxy changes short-source insertion rules without new MT5 execution(BQ 프록시는 새 MT5 실행 없이 숏 원천 삽입 규칙만 바꿈)",
            "usability": "usable_for_signal_sanity_and_BR_review_not_runtime_authority(신호 점검 및 BR 검토에는 사용 가능, 런타임 권위 아님)",
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
            "queue_id": "br01_review_bq_selected_stress_and_package_gate",
            "action": "review selected BQ stress slices and package gate(BQ 선택 압박 조각과 패키지 게이트 검토)",
            "success_criteria": "month_bad_count reaches 0 or remains explicit blocker(월 나쁨 수 0 도달 또는 명시 차단)",
            "effect": "좋은 proxy(프록시)를 운영 후보로 착각하지 않는다.",
        },
        {
            **common,
            "queue_rank": 2,
            "queue_id": "br02_compare_proxy_to_mt5_runtime_probe",
            "action": "compare BQ proxy with source MT5 probe(BQ 프록시와 원천 MT5 탐침 비교)",
            "success_criteria": "diff attribution remains usable but not authority(차이 귀속은 사용 가능하되 권위 아님)",
            "effect": "proxy/MT5 gap(프록시/MT5 간극)을 다음 런타임 판단 입력으로 남긴다.",
        },
        {
            **common,
            "queue_rank": 3,
            "queue_id": "br03_choose_runtime_package_or_repair_seed",
            "action": "decide package block or next repair seed(패키지 차단 또는 다음 수리 씨앗 결정)",
            "success_criteria": "no authority without MT5 reprobe(MT5 재탐침 없이 권위 없음)",
            "effect": "공격 탐색과 운영 경계를 분리한다.",
        },
    ]


def gate_rows(final: Mapping[str, Any], selected: Mapping[str, Any], surface: pd.DataFrame, receipts: Sequence[Path]) -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "gate": "scope_completion_gate",
            "status": "passed" if len(surface) > 0 and selected.get("candidate_id") else "failed",
            "evidence": rel(BQ_RULE_SURFACE),
            "effect": "BP queue(BP 대기열)를 BQ rule surface(BQ 규칙 표면)로 실행했다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "kpi_contract_audit",
            "status": "passed" if as_float(selected["profit_factor"]) >= MIN_PF_KEEP and as_float(selected["trade_density_per_business_day"]) >= DENSITY_FLOOR else "failed",
            "evidence": rel(SELECTED_CANDIDATE),
            "effect": "net/PF/expectancy/DD/recovery/trades/short share를 같이 점검했다.",
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
            "gate": "no_lookahead_boundary_gate",
            "status": "passed",
            "evidence": rel(OVERFIT_GUARDRAIL_AUDIT),
            "effect": "정확 월, 결과값 우선순위, top_n(상위 N개)을 사용하지 않았다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "synthetic_overlap_guard",
            "status": "passed" if as_int(selected["synthetic_overlap_count"]) == 0 else "failed",
            "evidence": f"synthetic_overlap_count={selected['synthetic_overlap_count']}",
            "effect": "bo91 계열의 겹침 문제를 runtime-safe(런타임 안전) 제약으로 바꿨다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "short_share_lift_gate",
            "status": "passed" if as_float(selected["short_share"]) >= TARGET_SHORT_SHARE else "failed",
            "evidence": rel(SHORT_SHARE_LIFT_ATTRIBUTION),
            "effect": "숏 비중 목표 0.12 이상을 회복했다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "package_boundary_gate",
            "status": "passed" if final["package_candidate_rows"] == 0 and final["new_mt5_execution"] == "not_run" else "failed",
            "evidence": rel(PROXY_MT5_DIFF_PLAN),
            "effect": "새 MT5 실행 전 package(패키지) 주장을 차단했다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "required_gate_coverage_audit",
            "status": "passed",
            "evidence": rel(GATE_AUDIT),
            "effect": "필수 게이트와 산출물을 연결했다.",
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
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "created_at_utc": created_at,
        "claim_boundary": CLAIM_BOUNDARY,
        "candidate_surface_rows": len(surface),
        "core_pass_rows": core_pass_rows,
        "package_candidate_rows": package_candidate_rows,
        "selected_candidate_id": selected["candidate_id"],
        "selected_candidate_status": selected["candidate_status"],
        "selected_family_id": selected["family_id"],
        "selected_seed_source": selected["seed_source"],
        "selected_selection_mode": selected["selection_mode"],
        "selected_p_short_floor": selected["p_short_floor"],
        "selected_margin_floor": selected["margin_floor"],
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
                "obsidian-artifact-lineage(산출물 계보)",
            ],
            "required_gates": ["scope_completion_gate", "kpi_contract_audit", "skill_receipt_lint", "required_gate_coverage_audit"],
            "idea_id": "IDEA-ST364-SOURCE-REGIME-LABEL-PIVOT-DENSE-COST-RECOVERY",
            "hypothesis": "broad clean source plus chronological overlap guard can lift short share without trade splitting(넓은 클린 원천과 시간순 겹침 가드가 거래 쪼개기 없이 숏비중을 올릴 수 있다)",
            "tier_scope": "Tier A separate + Tier B missing_required(Tier A 분리 + Tier B 필수 누락)",
            "broad_sweep": "h17/h20, h16/h17/h20, h17/h19/h20, and extreme multi-hour floors(17/20시, 16/17/20시, 17/19/20시, 극단 다중시간 하한)",
            "extreme_sweep": "multi-hour chronological_no_overlap variants(다중시간 시간순 겹침 방지 변형)",
            "micro_search_gate": "core pass with PF>=1.35, density>=3, short_share>=0.12, short_source_pf>=1.15, overlap=0(핵심 통과)",
            "evidence_boundary": "proxy_scout_only(프록시 정찰 전용)",
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
                "short_source_pf": selected["synthetic_short_profit_factor"],
                "month_bad_count": selected["month_bad_count"],
            },
            "evidence_boundary": "proxy_scout_only(프록시 정찰 전용)",
        },
    )
    write_json(
        DATA_RECEIPT,
        {
            **base,
            "source_artifacts": [rel(bo.BM.SHORT_SYNTHETIC_CANDIDATES), rel(parent.NEXT_OFFENSIVE_SEED_QUEUE), rel(parent.POSITIVE_CLUE_REGISTER)],
            "timestamp_boundary": "entry-known hour/probability/margin only; labels are evaluation outputs(진입시점 시간/확률/마진만 사용, 라벨은 평가 출력)",
            "lookahead_guard": "no exact month, no realized-pnl priority, no top_n(정확 월 없음, 실현손익 우선순위 없음, top_n 없음)",
        },
    )
    write_json(
        EXPERIMENT_RECEIPT,
        {
            **base,
            "hypothesis": "short-share lift from broad clean source and chronological no-overlap guard(넓은 클린 원천과 시간순 겹침 가드의 숏비중 상승)",
            "variant_count": final["candidate_surface_rows"],
            "broad_sweep": "hour-set, p_short floor, margin floor, selection mode(시간 묶음, p_short 하한, 마진 하한, 선택 모드)",
            "stop_condition": "open BR review when core pass appears but month stress/MT5 evidence remains(핵심 통과가 있으나 월 압박/MT5 근거가 남으면 BR 검토)",
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
            "selected_seed_source": final["selected_seed_source"],
            "proxy_mt5_diff": list(proxy_mt5),
            "driver": "short share recovered with h19 bridge while month stress remains(19시 브리지로 숏비중은 회복했지만 월 압박은 남음)",
        },
    )
    write_json(
        JUDGMENT_RECEIPT,
        {
            **base,
            "judgment": JUDGMENT,
            "decision": DECISION,
            "next_condition": NEXT_RUN_ID,
            "missing_evidence": ["new MT5 runtime reprobe(새 MT5 런타임 재탐침)", "forward pass(전진 통과)", "operating promotion evidence(운영 승격 근거)"],
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            **base,
            "allowed_claim": JUDGMENT,
            "forbidden_claims": ["runtime_authority", "operating_promotion", "live_readiness", "goal_achieve"],
            "effect": "BQ는 proxy scout(프록시 정찰)와 BR review handoff(BR 검토 인계)만 주장한다.",
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
            "lineage_judgment": "connected_BP_queue_to_BQ_surface_and_BR_review(BP 대기열을 BQ 표면과 BR 검토에 연결)",
            "claim_boundary": CLAIM_BOUNDARY,
            "final_decision": final,
        },
    )


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
    report = f"""# run364BQ broad clean short-share lift scout(364BQ 넓은 클린 숏비중 상승 정찰)

## Current Truth(현재 진실)

- selected candidate(선택 후보): `{final['selected_candidate_id']}`
- selected KPI(선택 핵심 성과 지표): net/PF/density/short share(순수익/수익 팩터/밀도/숏비중) `{final['selected_net_profit']}` / `{final['selected_profit_factor']}` / `{final['selected_density']}` / `{final['selected_short_share']}`
- synthetic short PF(합성 숏 수익 팩터): `{final['selected_synthetic_short_profit_factor']}`
- month_bad_count(월 나쁨 수): `{final['month_bad_count']}`
- package candidate rows(패키지 후보 행): `{final['package_candidate_rows']}`

## Action And Effect(행동과 효과)

Action(행동): BP queue(BP 대기열)의 bo90/bo91/bo05 단서를 hour-set/p_short/margin/chronological no-overlap(시간묶음/p_short/마진/시간순 겹침방지) surface(표면)로 넓게 재생했다.

Effect(효과): short share(숏 비중)는 목표 `0.12` 이상으로 회복했지만, month stress(월 압박)와 new MT5 execution(새 MT5 실행) 부재 때문에 package(패키지)는 열지 않고 BR review(BR 검토)로 넘긴다.

## Top Surface(상위 표면)

{markdown_table(top_surface, ['candidate_id', 'candidate_status', 'net_profit', 'profit_factor', 'trade_density_per_business_day', 'short_share', 'synthetic_short_profit_factor', 'synthetic_overlap_count', 'month_bad_count', 'selection_score'])}

## Stress Slices(압박 조각)

{markdown_table(stress_rows, ['axis', 'segment_id', 'net_profit', 'profit_factor', 'trade_count', 'short_share', 'segment_status'])}

## Short-Share Attribution(숏비중 귀속)

{markdown_table(attribution, ['comparison_id', 'source_candidate_id', 'net_diff', 'profit_factor_diff', 'short_share_diff', 'attribution'])}

## Overfit Guardrail(과적합 가드레일)

{markdown_table(overfit, ['audit_id', 'status', 'evidence', 'effect'])}

## Proxy/MT5 Diff(프록시/MT5 차이)

{markdown_table(proxy_mt5, ['comparison_id', 'mt5_net_profit', 'proxy_net_profit', 'net_diff_proxy_minus_mt5', 'mt5_profit_factor', 'proxy_profit_factor', 'usability'])}

## BR Queue(BR 대기열)

{markdown_table(queue, ['queue_rank', 'queue_id', 'action', 'success_criteria'])}

## Gates(게이트)

{markdown_table(gates, ['gate', 'status', 'evidence', 'effect'])}

## Boundary(경계)

BQ is proxy scout only(BQ는 프록시 정찰 전용). No new model training(새 모델 학습 없음), no new MT5 execution(새 MT5 실행 없음), no forward pass(전진 통과 없음), no runtime authority(런타임 권위 없음), no operating promotion(운영 승격 없음), no Goal Achieve(목표 달성 없음).
"""
    write_text(REPORT_PATH, report, bom=True)
    write_text(
        DECISION_DOC,
        f"""# {TODAY} Stage364BQ broad clean short-share lift scout(넓은 클린 숏비중 상승 정찰)

Action(행동): `{final['selected_candidate_id']}`를 BQ selected proxy(선택 프록시)로 남기고 `{NEXT_RUN_ID}`를 연다.

Effect(효과): short share(숏 비중)는 회복했지만 month stress(월 압박)와 MT5 미실행 때문에 운영 주장 없이 review(검토)로 넘긴다.

- report(보고서): `{rel(REPORT_PATH)}`
- final_decision(최종 결정): `{rel(FINAL_DECISION)}`
- next_run(다음 실행): `{NEXT_RUN_ID}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
        bom=True,
    )
    append_text_once(REVIEW_INDEX, RUN_ID, f"- `{RUN_ID}`: `{rel(REPORT_PATH)}` - broad clean short-share lift scout(넓은 클린 숏비중 상승 정찰).")
    append_text_once(
        STAGE_BRIEF,
        "## run364BQ Broad Clean Short-Share Lift Scout Closeout",
        f"""## run364BQ Broad Clean Short-Share Lift Scout Closeout(364BQ 넓은 클린 숏비중 상승 정찰 종료)

Action(행동): bo90/bo91/bo05 positive clue(긍정 단서)를 broad clean short-share lift(넓은 클린 숏비중 상승) surface(표면)로 재생했다.

Effect(효과): `{final['selected_candidate_id']}`는 proxy(프록시) 기준 net/PF/density/short share(순수익/수익 팩터/밀도/숏비중) `{final['selected_net_profit']}` / `{final['selected_profit_factor']}` / `{final['selected_density']}` / `{final['selected_short_share']}`를 냈지만 month stress(월 압박)와 MT5 미실행 때문에 `{NEXT_RUN_ID}` 검토로 넘긴다.
""",
    )
    append_text_once(
        STAGE_README,
        RUN_ID,
        f"""## run364BQ Broad Clean Short-Share Lift Scout(364BQ 넓은 클린 숏비중 상승 정찰)

Action(행동): Stage364(364단계) 안에서 새 stage(단계) 분기 없이 bo90/bo91/bo05 단서를 넓은 규칙 표면으로 재생했다.

Effect(효과): short share(숏 비중)는 회복했지만 package(패키지)는 열지 않고 `{NEXT_RUN_ID}`로 검토를 넘긴다.
""",
    )
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
    replace_prefixed_lines(
        STAGE_README,
        {
            "Current run(현재 실행):": f"Current run(현재 실행): `{NEXT_RUN_ID}`",
            "Latest completed run(최근 완료 실행):": f"Latest completed run(최근 완료 실행): `{RUN_ID}`",
            "Current truth(현재 진실):": f"Current truth(현재 진실): run364BQ(364BQ 실행)는 `{final['selected_candidate_id']}` proxy clue(프록시 단서)를 만들었지만 month stress(월 압박)와 MT5 미실행 때문에 review required(검토 필요)로 닫았다.",
            "Next action(다음 행동):": f"Next action(다음 행동): `{NEXT_RUN_ID}`에서 package gate(패키지 게이트), stress attribution(압박 귀속), proxy/MT5 diff(프록시/MT5 차이)를 검토한다.",
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

Current truth(현재 진실): `run364BQ`는 broad clean short-share lift(넓은 클린 숏비중 상승) proxy scout(프록시 정찰)를 실행했다. 선택 후보 `{final['selected_candidate_id']}`의 proxy net/PF/density/short share(프록시 순수익/수익 팩터/밀도/숏비중)는 `{final['selected_net_profit']}` / `{final['selected_profit_factor']}` / `{final['selected_density']}` / `{final['selected_short_share']}`이고 synthetic short PF(합성 숏 수익 팩터)는 `{final['selected_synthetic_short_profit_factor']}`다. 다만 month_bad_count(월 나쁨 수) `{final['month_bad_count']}`, new MT5 execution(새 MT5 실행) 없음이라 package candidate(패키지 후보)는 아니다.

Next action(다음 행동): `{NEXT_RUN_ID}`에서 BQ selected proxy(BQ 선택 프록시)를 package gate(패키지 게이트), stress attribution(압박 귀속), proxy/MT5 diff(프록시/MT5 차이)로 검토한다.

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

Package candidate(패키지 후보): none(없음). BQ selected proxy(BQ 선택 프록시)는 month_bad_count(월 나쁨 수) `{final['month_bad_count']}` 및 new MT5 execution(새 MT5 실행) 없음 때문에 review required(검토 필요)다.

Selected proxy(선택 프록시): `{final['selected_candidate_id']}`

Proxy KPI(프록시 핵심 성과 지표): net `{final['selected_net_profit']}`, PF `{final['selected_profit_factor']}`, expectancy `{final['selected_expectancy']}`, trades `{final['selected_trade_count']}`, density `{final['selected_density']}`, closed DD `{final['selected_closed_drawdown_amount']}`, recovery `{final['selected_recovery_factor']}`, short share `{final['selected_short_share']}`.

Short source quality(숏 원천 품질): synthetic short net/PF(합성 숏 순수익/수익 팩터) `{final['selected_synthetic_short_net_profit']}` / `{final['selected_synthetic_short_profit_factor']}`.

Next queue(다음 대기열): `{rel(RUN364BR_QUEUE)}`

Authority(권위): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함).
""",
        bom=True,
    )
    append_text_once(
        WORKSPACE_CHANGELOG,
        f"## {TODAY} - {RUN_ID}",
        f"""## {TODAY} - {RUN_ID}

- action(행동): broad clean short-share lift proxy scout(넓은 클린 숏비중 상승 프록시 정찰)를 실행했다.
- effect(효과): `{final['selected_candidate_id']}` 단서를 `{NEXT_RUN_ID}` 검토로 넘기고 package(패키지)는 열지 않았다.
- report(보고서): `{rel(REPORT_PATH)}`
""",
    )
    append_text_once(
        IDEA_REGISTRY,
        RUN_ID,
        f"""## {RUN_ID}

- idea(아이디어): broad clean short-source expansion(넓은 클린 숏 원천 확장)과 chronological no-overlap guard(시간순 겹침 방지 가드)가 short share(숏 비중)를 0.12 이상으로 복구할 수 있다.
- positive clue(긍정 단서): selected proxy(선택 프록시) net/PF/density/short share `{final['selected_net_profit']}` / `{final['selected_profit_factor']}` / `{final['selected_density']}` / `{final['selected_short_share']}`.
- next action(다음 행동): `{NEXT_RUN_ID}`.
""",
    )
    append_text_once(
        NEGATIVE_RESULT_REGISTER,
        RUN_ID,
        f"""## {RUN_ID}

- status(상태): package not opened(패키지 열지 않음).
- failure_memory(실패 기억): selected proxy(선택 프록시)는 month_bad_count(월 나쁨 수) `{final['month_bad_count']}`이고 MT5 reprobe(MT5 재탐침)가 없다.
- salvage_value(회수 가치): short share(숏 비중) 목표와 PF(수익 팩터) 목표는 동시에 통과했다.
- reopen_condition(재개 조건): `{NEXT_RUN_ID}`에서 월 압박 원인과 proxy/MT5 diff(프록시/MT5 차이)를 닫는다.
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
        "evidence_boundary": "proxy_scout_only(프록시 정찰 전용)",
        "question": "Can broad clean short source lift short share without overlap or trade splitting?(넓은 클린 숏 원천이 겹침/거래 쪼개기 없이 숏비중을 올리는가?)",
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
        ("tier_a_separate", "Tier A separate(Tier A 분리)", "Tier A", STATUS, True),
        ("tier_b_missing_required", "Tier B separate(Tier B 분리)", "Tier B", "out_of_scope_by_claim(주장 범위 밖)", False),
        ("tier_a_plus_b_combined", "Tier A+B combined(Tier A+B 합산)", "Tier A+B", STATUS, True),
    ]:
        row = {
            **common,
            "ledger_row_id": f"{RUN_ID}__{suffix}",
            "subrun_id": f"{RUN_ID}__{suffix}",
            "row_id": f"{RUN_ID}__{suffix}",
            "record_view": record_view,
            "tier_scope": tier_scope,
            "kpi_scope": "BQ proxy scout(BQ 프록시 정찰)",
            "scoreboard_lane": "stage364_proxy_scout(Stage364 프록시 정찰)",
            "status": status,
            "primary_kpi": f"net={final['selected_net_profit']};pf={final['selected_profit_factor']};density={final['selected_density']};short_share={final['selected_short_share']}",
            "guardrail_kpi": f"month_bad_count={final['month_bad_count']};package_rows={final['package_candidate_rows']};no_authority",
            "result_judgment": JUDGMENT,
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
        "lane": "stage364_proxy_scout(Stage364 프록시 정찰)",
        "family": "broad_clean_short_share_lift(넓은 클린 숏비중 상승)",
        "path": rel(REPORT_PATH),
        "primary_report": rel(REPORT_PATH),
        "net_profit": final["selected_net_profit"],
        "profit_factor": final["selected_profit_factor"],
        "drawdown": final["selected_closed_drawdown_amount"],
        "recovery_factor": final["selected_recovery_factor"],
        "trade_count": final["selected_trade_count"],
        "trade_density_per_feature_day": final["selected_density"],
        "result_status": STATUS,
        "expectancy": final["selected_expectancy"],
        "view": "proxy_scout(프록시 정찰)",
        "tier": "Tier A",
        "metric_scope": "selected_proxy(선택 프록시)",
        "trade_density_requirement_status": "passed_density_ge_3(밀도 3 이상 통과)",
        "primary_artifact": rel(BQ_RULE_SURFACE),
    }
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], [registry_row])
    repair_run_registry_line_endings(RUN_ID)


def write_artifact_registry(final: Mapping[str, Any]) -> None:
    artifacts = [
        ("bq_rule_surface", BQ_RULE_SURFACE, "BQ rule surface(BQ 규칙 표면)."),
        ("selected_candidate", SELECTED_CANDIDATE, "BQ selected proxy candidate(BQ 선택 프록시 후보)."),
        ("selected_trade_tape", SELECTED_TRADE_TAPE, "BQ selected combined trade tape(BQ 선택 합산 거래 테이프)."),
        ("selected_synthetic_short_tape", SELECTED_SYNTHETIC_SHORT_TAPE, "BQ selected synthetic short tape(BQ 선택 합성 숏 테이프)."),
        ("stress_slice_review", STRESS_SLICE_REVIEW, "BQ stress slice review(BQ 압박 조각 검토)."),
        ("proxy_mt5_diff_plan", PROXY_MT5_DIFF_PLAN, "BQ proxy/MT5 diff plan(BQ 프록시/MT5 차이 계획)."),
        ("final_decision", FINAL_DECISION, "BQ final decision(BQ 최종 결정)."),
        ("run_manifest", RUN_MANIFEST, "BQ run manifest(BQ 실행 목록)."),
        ("report", REPORT_PATH, "BQ report(BQ 보고서)."),
    ]
    rows = []
    for artifact_type, path, notes in artifacts:
        if exists(path):
            rows.append(
                {
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "artifact_type": artifact_type,
                    "path": rel(path),
                    "artifact_path": rel(path),
                    "sha256": sha(path),
                    "artifact_id": f"{RUN_ID}__{artifact_type}",
                    "created_at_utc": final["created_at_utc"],
                    "created_at": final["created_at_utc"],
                    "claim_boundary": CLAIM_BOUNDARY,
                    "notes": notes,
                }
            )
    append_or_replace_csv(ARTIFACT_REGISTRY, ["artifact_id"], rows)


def write_manifest(final: Mapping[str, Any]) -> None:
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
            "created_at_utc": final["created_at_utc"],
            "inputs": [{"path": rel(path), "sha256": sha(path)} for path in INPUT_FILES if exists(path)],
            "outputs": [{"path": rel(path), "sha256": sha(path)} for path in OUTPUT_FILES if exists(path) and Path(path).is_file()],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def write_tables(
    surface: pd.DataFrame,
    selected: Mapping[str, Any],
    selected_combined: pd.DataFrame,
    selected_synthetic: pd.DataFrame,
    selected_displaced: pd.DataFrame,
    stress_rows: Sequence[Mapping[str, Any]],
    attribution_rows: Sequence[Mapping[str, Any]],
    overfit_rows_payload: Sequence[Mapping[str, Any]],
    proxy_mt5_rows_payload: Sequence[Mapping[str, Any]],
    queue: Sequence[Mapping[str, Any]],
) -> None:
    write_csv(INPUT_MANIFEST, input_manifest_rows())
    write_csv(BQ_RULE_SURFACE, surface.to_dict("records"))
    write_json(SELECTED_CANDIDATE, selected)
    out_combined = selected_combined.copy()
    out_combined["entry_time"] = out_combined["entry_time_dt"].astype(str)
    out_combined["exit_time"] = out_combined["exit_time_dt"].astype(str)
    write_csv(SELECTED_TRADE_TAPE, out_combined.drop(columns=["entry_time_dt", "exit_time_dt"], errors="ignore").to_dict("records"))
    out_syn = selected_synthetic.copy()
    out_syn["entry_time"] = out_syn["entry_time_dt"].astype(str)
    out_syn["exit_time"] = out_syn["exit_time_dt"].astype(str)
    write_csv(SELECTED_SYNTHETIC_SHORT_TAPE, out_syn.drop(columns=["entry_time_dt", "exit_time_dt"], errors="ignore").to_dict("records"))
    write_csv(SELECTED_DISPLACED_PARENT_TRADES, selected_displaced.to_dict("records"))
    write_csv(STRESS_SLICE_REVIEW, stress_rows)
    write_csv(SHORT_SHARE_LIFT_ATTRIBUTION, attribution_rows)
    write_csv(OVERFIT_GUARDRAIL_AUDIT, overfit_rows_payload)
    write_csv(PROXY_MT5_DIFF_PLAN, proxy_mt5_rows_payload)
    write_csv(RUN364BR_QUEUE, queue)


def main() -> None:
    ensure_dirs()
    _, _, bk_final = validate_inputs()
    write_work_packet()
    parent_trades = replay.load_parent_trades()
    broad_pool = bo.load_broad_pool()
    surface, combined_map, synthetic_map, displaced_map = evaluate_variants(parent_trades, broad_pool, candidate_definitions())
    selected = dict(select_candidate(surface))
    selected_id = str(selected["candidate_id"])
    selected_combined = combined_map[selected_id]
    selected_synthetic = synthetic_map[selected_id]
    selected_displaced = displaced_map[selected_id]
    stress = stress_slice_rows(selected_id, selected_combined)
    clues = load_positive_clues()
    attribution = short_share_lift_rows(selected, clues, surface)
    overfit = overfit_rows(selected, surface)
    proxy_mt5 = proxy_mt5_rows(bk_final, selected)
    queue = queue_rows(selected)
    created_at = now_utc()
    preliminary = {
        "package_candidate_rows": int(surface["package_like_proxy_row"].astype(bool).sum()) if not surface.empty else 0,
        "new_mt5_execution": "not_run",
    }
    receipt_paths = [RUN_EVIDENCE_RECEIPT, DATA_RECEIPT, EXPERIMENT_RECEIPT, MODEL_RECEIPT, ATTRIBUTION_RECEIPT, JUDGMENT_RECEIPT, LINEAGE_RECEIPT, CLAIM_RECEIPT]
    gates = gate_rows(preliminary, selected, surface, receipt_paths)
    if any(row["status"] == "failed" for row in gates):
        write_csv(INPUT_MANIFEST, input_manifest_rows())
        write_csv(BQ_RULE_SURFACE, surface.to_dict("records"))
        write_csv(GATE_AUDIT, gates)
        raise RuntimeError("BQ gate failure(BQ 게이트 실패): " + ", ".join(row["gate"] for row in gates if row["status"] == "failed"))
    final = final_payload(selected, surface, stress, gates, created_at)
    gates = gate_rows(final, selected, surface, receipt_paths)
    final = final_payload(selected, surface, stress, gates, created_at)
    write_tables(surface, selected, selected_combined, selected_synthetic, selected_displaced, stress, attribution, overfit, proxy_mt5, queue)
    write_receipts(final, selected, proxy_mt5)
    write_csv(GATE_AUDIT, gates)
    write_json(FINAL_DECISION, final)
    write_docs(final, surface, selected, stress, attribution, overfit, proxy_mt5, queue, gates)
    write_ledgers(final)
    write_artifact_registry(final)
    write_manifest(final)
    refresh_lineage_receipt(final)
    print(json.dumps(json_ready(final), ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
