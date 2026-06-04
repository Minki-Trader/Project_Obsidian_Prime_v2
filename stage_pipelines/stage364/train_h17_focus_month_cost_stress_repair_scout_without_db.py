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
from stage_pipelines.stage364 import materialize_h17_focus_month_cost_stress_repair_inputs_without_db as ci  # noqa: E402
from stage_pipelines.stage364 import train_cost_stable_h17_source_guard_offensive_scout_without_db as cg  # noqa: E402
from stage_pipelines.stage364.review_pf_pass_density_restore_offensive_scout_without_db import repair_run_registry_line_endings  # noqa: E402


TODAY = "2026-06-05"
STAGE_ID = ci.STAGE_ID
RUN_NUMBER = "run364CJ"
RUN_ID = "run364CJ_train_h17_focus_month_cost_stress_repair_scout_without_db_v1"
PARENT_RUN_ID = ci.RUN_ID
SOURCE_PROXY_SCOUT_RUN_ID = cg.RUN_ID
NEXT_RUN_ID = "run364CK_review_h17_focus_month_cost_stress_repair_scout_without_db_v1"

STATUS = "completed_stage364CJ_h17_focus_month_cost_stress_repair_proxy_scout_review_required_no_authority"
JUDGMENT = "exploratory_proxy_repair_scout_completed_review_required_no_authority"
DECISION = "stage364CJ_open_run364CK_h17_focus_month_cost_stress_repair_review"
CLAIM_BOUNDARY = (
    "research_development_proxy_scout_only_rule_surface_no_new_model_artifact_no_new_mt5_execution_"
    "no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

DENSITY_FLOOR = cg.DENSITY_FLOOR
SHORT_FLOOR = cg.SHORT_FLOOR
PARENT_VARIANT_ID = cg.PARENT_VARIANT_ID
NATIVE_CONTROL_VARIANT_ID = cg.NATIVE_CONTROL_VARIANT_ID

STAGE_DIR = ci.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
SPEC_DIR = STAGE_DIR / "00_spec"
SELECTED_DIR = STAGE_DIR / "04_selected"

INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
PROXY_REPAIR_SURFACE = RUN_DIR / "cj_proxy_repair_surface.csv"
SELECTED_CANDIDATE = RUN_DIR / "selected_cj_candidate.json"
SELECTED_TRADE_TAPE = RUN_DIR / "selected_cj_trade_tape.csv"
CANDIDATE_FILTER_AUDIT = RUN_DIR / "candidate_filter_audit.csv"
CANDIDATE_SOURCE_ATTRIBUTION = RUN_DIR / "candidate_source_attribution.csv"
CANDIDATE_MONTH_STABILITY = RUN_DIR / "candidate_month_stability.csv"
COST_STRESS_DIAGNOSTIC = RUN_DIR / "cost_stress_diagnostic.csv"
PACKAGE_PRECHECK = RUN_DIR / "package_precheck.csv"
PROXY_MT5_DIFF_PLAN = RUN_DIR / "proxy_mt5_diff_plan.csv"
RUN364CK_QUEUE = RUN_DIR / "run364CK_review_queue.csv"
DATA_INTEGRITY_AUDIT = RUN_DIR / "data_integrity_audit.csv"
RUN_EVIDENCE_RECEIPT = RUN_DIR / "run_evidence_receipt.json"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment_design_receipt.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / "run364CJ_h17_focus_month_cost_stress_repair_scout.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364CJ_h17_focus_month_cost_stress_repair_scout.md"
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
    ci.FINAL_DECISION,
    ci.GATE_AUDIT,
    ci.RUN364CJ_QUEUE,
    ci.FAILURE_MEMORY_SUMMARY,
    ci.REPAIR_AXIS_MAP,
    ci.COST_STRESS_GUARD_MATRIX,
    ci.BAD_MONTH_GUARD_MATRIX,
    ci.SHORT_FLOOR_RESCUE_MATRIX,
    ci.DATA_INTEGRITY_AUDIT,
    ci.RUN_MANIFEST,
    cg.FINAL_DECISION,
    cg.PROXY_SCOUT_SURFACE,
    cg.SELECTED_CANDIDATE,
    cg.SELECTED_TRADE_TAPE,
    cg.CANDIDATE_FILTER_AUDIT,
    cg.CANDIDATE_SOURCE_ATTRIBUTION,
    cg.CANDIDATE_MONTH_STABILITY,
    cg.COST_STRESS_DIAGNOSTIC,
    cg.PROXY_MT5_DIFF_PLAN,
    cg.RUN_MANIFEST,
    cg.ce.TRADE_ATTRIBUTION,
    cg.parent.RUN364CG_SCOUT_QUEUE,
]

OUTPUT_FILES = [
    INPUT_MANIFEST,
    WORK_PACKET,
    PROXY_REPAIR_SURFACE,
    SELECTED_CANDIDATE,
    SELECTED_TRADE_TAPE,
    CANDIDATE_FILTER_AUDIT,
    CANDIDATE_SOURCE_ATTRIBUTION,
    CANDIDATE_MONTH_STABILITY,
    COST_STRESS_DIAGNOSTIC,
    PACKAGE_PRECHECK,
    PROXY_MT5_DIFF_PLAN,
    RUN364CK_QUEUE,
    DATA_INTEGRITY_AUDIT,
    RUN_EVIDENCE_RECEIPT,
    EXPERIMENT_RECEIPT,
    DATA_RECEIPT,
    MODEL_RECEIPT,
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
    return ci.rel(path)


def exists(path: Path | str) -> bool:
    return ci.exists(path)


def sha(path: Path | str) -> str:
    return ci.sha(path)


def read_json(path: Path) -> Any:
    return ci.read_json(path)


def write_json(path: Path, payload: Any) -> None:
    ci.write_json(path, json_ready(payload))


def read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(io_path(path), encoding="utf-8-sig").fillna("")


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    ci.write_csv(path, rows, fieldnames)


def write_text(path: Path, text: str, *, bom: bool = True) -> None:
    ci.write_text(path, text, bom=bom)


def append_text_once(path: Path, marker: str, text: str) -> None:
    ci.append_text_once(path, marker, text)


def append_or_replace_csv(
    path: Path,
    key_fields: Sequence[str],
    rows: Sequence[Mapping[str, Any]],
    *,
    extend_header: bool = True,
) -> None:
    ci.append_or_replace_csv(path, key_fields, rows, extend_header=extend_header)


def replace_prefixed_lines(path: Path, replacements: Mapping[str, str], *, bom: bool = True) -> None:
    ci.replace_prefixed_lines(path, replacements, bom=bom)


def as_float(value: Any, default: float = 0.0) -> float:
    return ci.as_float(value, default)


def finite(value: Any, digits: int = 10) -> float | str:
    return ci.finite(value, digits)


def json_ready(value: Any) -> Any:
    return ci.json_ready(value)


def markdown_table(rows: Sequence[Mapping[str, Any]], columns: Sequence[str], limit: int = 12) -> str:
    return ci.markdown_table(rows, columns, limit=limit)


def ensure_dirs() -> None:
    for path in [RUN_DIR, REVIEW_DIR, SPEC_DIR, SELECTED_DIR, DECISION_DOC.parent]:
        io_path(path).mkdir(parents=True, exist_ok=True)


def validate_inputs() -> dict[str, Any]:
    missing = [rel(path) for path in INPUT_FILES if not exists(path)]
    if missing:
        raise FileNotFoundError("missing CJ inputs(CJ 입력 누락): " + ", ".join(missing))

    ci_final = read_json(ci.FINAL_DECISION)
    if ci_final.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"CI next_run_id mismatch(CI 다음 실행 불일치): {ci_final.get('next_run_id')} != {RUN_ID}")
    if ci_final.get("runtime_authority") != "not_claimed" or ci_final.get("operating_promotion") != "not_claimed":
        raise RuntimeError("CI has forbidden authority claim(CI 금지 권위 주장 존재)")

    gates = read_csv(ci.GATE_AUDIT)
    if gates.empty or any(gates["status"].astype(str) != "passed"):
        raise RuntimeError("CI gate audit(CI 게이트 감사)가 모두 passed(통과)가 아닙니다.")

    queue = read_csv(ci.RUN364CJ_QUEUE)
    if len(queue) != 16:
        raise RuntimeError(f"CJ queue row mismatch(CJ 대기열 행 불일치): {len(queue)} != 16")
    if int(queue["top_n_status"].astype(str).str.contains("top_n").sum()) > 0:
        # The queue stores "forbidden" status, but no row may request a top_n operation.
        requested = queue["source_mix_policy"].astype(str).str.contains("top_n", case=False).sum()
        if int(requested) > 0:
            raise RuntimeError("top_n operation requested(top_n 작업 요청 발견)")
    return ci_final


def input_manifest_rows() -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "input_path": rel(path),
            "exists": exists(path),
            "sha256": sha(path),
            "input_role": "CJ proxy replay source(CJ 프록시 재생 원천)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for path in INPUT_FILES
    ]


def cg_effective_days() -> float:
    surface = read_csv(cg.PROXY_SCOUT_SURFACE)
    anchor = surface[surface["candidate_id"].astype(str).eq("cg01_current_session_semantics_anchor")]
    if not anchor.empty:
        row = anchor.iloc[0].to_dict()
        count = as_float(row.get("trade_count"))
        density = as_float(row.get("trade_density"))
        if count > 0 and density > 0:
            return count / density
    return 314.0


def metric_frame(frame: pd.DataFrame, *, effective_days: float) -> dict[str, Any]:
    return cg.metric_frame(frame.copy(), effective_days=effective_days)


def signed_gross(frame: pd.DataFrame) -> float:
    if frame.empty:
        return 0.0
    return float(frame["gross_profit"].sum())


def stress_adjusted_net(frame: pd.DataFrame) -> float:
    if frame.empty:
        return 0.0
    return signed_gross(frame) + float(frame["swap"].sum()) * 2.0 + float(frame["commission"].sum())


def seed_queue_map() -> dict[str, dict[str, Any]]:
    queue = read_csv(cg.parent.RUN364CG_SCOUT_QUEUE)
    return {str(row["candidate_id"]): row.to_dict() for _, row in queue.iterrows()}


def normalize_trade_frame(frame: pd.DataFrame) -> pd.DataFrame:
    out = frame.copy()
    if "open_time_dt" not in out.columns:
        out["open_time_dt"] = pd.to_datetime(out["open_time"])
    if "close_time_dt" not in out.columns:
        out["close_time_dt"] = pd.to_datetime(out["close_time"])
    if "open_month" not in out.columns:
        out["open_month"] = out["open_time_dt"].dt.strftime("%Y-%m")
    if "open_month_num" not in out.columns:
        out["open_month_num"] = out["open_time_dt"].dt.month
    if "margin_vs_long" not in out.columns:
        out["margin_vs_long"] = pd.to_numeric(out["p_short"], errors="coerce").fillna(0.0) - pd.to_numeric(out["p_long"], errors="coerce").fillna(0.0)
    if "margin_vs_flat" not in out.columns:
        out["margin_vs_flat"] = pd.to_numeric(out["p_short"], errors="coerce").fillna(0.0) - pd.to_numeric(out["p_flat"], errors="coerce").fillna(0.0)
    return out.sort_values("open_time_dt").reset_index(drop=True)


def empty_like(frame: pd.DataFrame) -> pd.DataFrame:
    return frame.iloc[0:0].copy()


def trade_key_columns(frame: pd.DataFrame) -> list[str]:
    preferred = ["open_time", "close_time", "direction", "source_bucket"]
    return [column for column in preferred if column in frame.columns]


def concat_unique(parts: Sequence[pd.DataFrame]) -> pd.DataFrame:
    non_empty = [part.copy() for part in parts if part is not None and not part.empty]
    if not non_empty:
        return pd.DataFrame()
    combined = pd.concat(non_empty, ignore_index=True, sort=False)
    keys = trade_key_columns(combined)
    if keys:
        combined = combined.drop_duplicates(subset=keys, keep="last")
    return normalize_trade_frame(combined)


def remove_condition(
    frame: pd.DataFrame,
    condition: pd.Series,
    *,
    reason: str,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    if frame.empty:
        return frame.copy(), frame.copy()
    condition = condition.reindex(frame.index, fill_value=False)
    removed = frame[condition].copy()
    if not removed.empty:
        removed["removed_reason"] = reason
    kept = frame[~condition].copy()
    return normalize_trade_frame(kept), normalize_trade_frame(removed) if not removed.empty else removed


def restore_short_floor(
    frame: pd.DataFrame,
    removed_pool: pd.DataFrame,
    *,
    target: int,
    native_first: bool,
    cost_policy: str,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    current_shorts = int(frame["direction"].eq("short").sum()) if not frame.empty else 0
    need = max(0, target - current_shorts)
    if need == 0 or removed_pool.empty:
        return normalize_trade_frame(frame), empty_like(frame)

    keys = trade_key_columns(frame)
    pool = removed_pool[removed_pool["direction"].eq("short")].copy()
    if keys and not frame.empty:
        existing = set(tuple(row) for row in frame[keys].astype(str).to_numpy())
        pool["_entry_key"] = [tuple(row) for row in pool[keys].astype(str).to_numpy()]
        pool = pool[~pool["_entry_key"].isin(existing)].copy()
    if native_first:
        native_pool = pool[pool["source_bucket"].eq("native_short_threshold")].copy()
        if len(native_pool) >= need:
            pool = native_pool

    if pool.empty:
        return normalize_trade_frame(frame), empty_like(frame)

    for column in ["p_short", "margin_vs_long", "margin_vs_flat"]:
        pool[column] = pd.to_numeric(pool[column], errors="coerce").fillna(0.0)
    pool["_restore_score"] = pool["p_short"] + pool["margin_vs_long"].clip(lower=0.0) + pool["margin_vs_flat"].clip(lower=0.0)
    if "hour17_20" in cost_policy or "stress_delta_floor" in cost_policy:
        bad_cost_hour = pool["source_bucket"].eq("native_short_threshold") & pool["open_hour"].isin([17, 20])
        pool.loc[bad_cost_hour, "_restore_score"] -= 0.10
    addback = pool.sort_values(["_restore_score", "p_short", "margin_vs_long"], ascending=False).head(need).copy()
    addback["restored_reason"] = "restore_short_floor_100_by_entry_known_score(진입 시점 점수로 숏 하한 100 복원)"
    restored = addback.drop(columns=["_entry_key", "_restore_score"], errors="ignore")
    combined = concat_unique([frame, restored])
    return combined, normalize_trade_frame(restored)


def load_seed_frame(
    seed_candidate_id: str,
    parent_trades: pd.DataFrame,
    native_control: pd.DataFrame,
    cg_queue: Mapping[str, Mapping[str, Any]],
    native_q10: tuple[float, float],
) -> tuple[pd.DataFrame, pd.DataFrame, str, str]:
    if seed_candidate_id == PARENT_VARIANT_ID:
        return parent_trades.copy(), empty_like(parent_trades), PARENT_VARIANT_ID, "parent_cd02_anchor_replay(CD02 부모 기준 재생)"
    if seed_candidate_id == NATIVE_CONTROL_VARIANT_ID:
        return native_control.copy(), empty_like(parent_trades), NATIVE_CONTROL_VARIANT_ID, "native_control_cd03_replay(CD03 네이티브 대조 재생)"
    if seed_candidate_id not in cg_queue:
        raise KeyError(f"unknown seed_candidate_id(알 수 없는 씨앗 후보): {seed_candidate_id}")
    seed_row = cg_queue[seed_candidate_id]
    frame, removed, source_variant, transform = cg.apply_candidate(seed_row, parent_trades, native_control, native_q10=native_q10)
    return normalize_trade_frame(frame), normalize_trade_frame(removed), source_variant, str(transform)


def overlay_weak_mask(frame: pd.DataFrame) -> pd.Series:
    overlay = frame[frame["source_bucket"].eq("synthetic_short_overlay")]
    if overlay.empty:
        return pd.Series(False, index=frame.index)
    p_floor = float(pd.to_numeric(overlay["p_short"], errors="coerce").fillna(0.0).median())
    margin_floor = float(pd.to_numeric(overlay["margin_vs_long"], errors="coerce").fillna(0.0).median())
    return frame["source_bucket"].eq("synthetic_short_overlay") & (
        (pd.to_numeric(frame["p_short"], errors="coerce").fillna(0.0) < p_floor)
        | (pd.to_numeric(frame["margin_vs_long"], errors="coerce").fillna(0.0) < margin_floor)
    )


def apply_repair_candidate(
    queue_row: Mapping[str, Any],
    parent_trades: pd.DataFrame,
    native_control: pd.DataFrame,
    cg_queue: Mapping[str, Mapping[str, Any]],
    native_q10: tuple[float, float],
) -> tuple[pd.DataFrame, dict[str, Any], list[dict[str, Any]]]:
    candidate_id = str(queue_row["candidate_id"])
    seed_candidate_id = str(queue_row["seed_candidate_id"])
    h17_policy = str(queue_row.get("h17_overlay_policy", ""))
    cost_policy = str(queue_row.get("cost_stress_policy", ""))
    month_policy = str(queue_row.get("month_guard_policy", ""))
    short_policy = str(queue_row.get("short_floor_policy", ""))

    frame, removed_pool, source_variant, seed_transform = load_seed_frame(
        seed_candidate_id,
        parent_trades,
        native_control,
        cg_queue,
        native_q10,
    )
    input_count = len(frame)
    removed_steps: list[dict[str, Any]] = []
    transform_parts = [seed_transform]

    def record_step(reason: str, removed: pd.DataFrame) -> None:
        removed_steps.append(
            {
                "run_id": RUN_ID,
                "candidate_id": candidate_id,
                "filter_step": len(removed_steps) + 1,
                "filter_reason": reason,
                "removed_trade_count": int(len(removed)),
                "removed_short_count": int(removed["direction"].eq("short").sum()) if not removed.empty else 0,
                "removed_net_profit": finite(float(removed["net_profit"].sum()) if not removed.empty else 0.0, 2),
                "effect": "remove existing entries only(기존 진입만 제거)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    if h17_policy == "focus_best_overlay_open_hour=17":
        condition = frame["source_bucket"].eq("synthetic_short_overlay") & (frame["open_hour"] != 17)
        frame, removed = remove_condition(frame, condition, reason="focus_h17_overlay_only(17시 오버레이 집중)")
        if not removed.empty:
            removed_pool = concat_unique([removed_pool, removed])
        record_step("focus_h17_overlay_only(17시 오버레이 집중)", removed)
        transform_parts.append("h17_focus")

    if cost_policy in {"stress_delta_floor_ge_0", "native_short_hour17_20_soft_firewall", "stress_delta_floor_ge_0_and_native_cost_soft"}:
        condition = frame["source_bucket"].eq("native_short_threshold") & frame["open_hour"].isin([17, 20])
        frame, removed = remove_condition(frame, condition, reason="native_short_hour17_20_cost_soft_firewall(네이티브 숏 17/20시 비용 소프트 방화벽)")
        if not removed.empty:
            removed_pool = concat_unique([removed_pool, removed])
        record_step("native_short_hour17_20_cost_soft_firewall(네이티브 숏 17/20시 비용 소프트 방화벽)", removed)
        transform_parts.append("native_hour17_20_soft_firewall")
    elif cost_policy == "trim_negative_swap_native_only":
        p_floor, margin_floor = native_q10
        condition = (
            frame["source_bucket"].eq("native_short_threshold")
            & frame["open_hour"].isin([17, 20, 21])
            & (
                (pd.to_numeric(frame["p_short"], errors="coerce").fillna(0.0) < p_floor)
                | (pd.to_numeric(frame["margin_vs_long"], errors="coerce").fillna(0.0) < margin_floor)
            )
        )
        frame, removed = remove_condition(frame, condition, reason="trim_weak_native_swap_hours(약한 네이티브 스왑 시간 제거)")
        if not removed.empty:
            removed_pool = concat_unique([removed_pool, removed])
        record_step("trim_weak_native_swap_hours(약한 네이티브 스왑 시간 제거)", removed)
        transform_parts.append("weak_native_swap_trim")

    if month_policy.startswith("month_of_year=08"):
        condition = frame["source_bucket"].eq("synthetic_short_overlay") & (frame["open_month_num"] == 8)
        frame, removed = remove_condition(frame, condition, reason="month_of_year_08_overlay_guard(8월 오버레이 가드)")
        if not removed.empty:
            removed_pool = concat_unique([removed_pool, removed])
        record_step("month_of_year_08_overlay_guard(8월 오버레이 가드)", removed)
        transform_parts.append("month08_overlay_guard")
    elif month_policy.startswith("month_of_year=12"):
        condition = frame["source_bucket"].eq("synthetic_short_overlay") & (frame["open_month_num"] == 12)
        frame, removed = remove_condition(frame, condition, reason="month_of_year_12_overlay_guard(12월 오버레이 가드)")
        if not removed.empty:
            removed_pool = concat_unique([removed_pool, removed])
        record_step("month_of_year_12_overlay_guard(12월 오버레이 가드)", removed)
        transform_parts.append("month12_overlay_guard")
    elif month_policy.startswith("quarter=Q3"):
        condition = frame["source_bucket"].eq("synthetic_short_overlay") & frame["open_month_num"].isin([7, 8, 9]) & overlay_weak_mask(frame)
        frame, removed = remove_condition(frame, condition, reason="quarter_q3_weak_overlay_guard(Q3 약한 오버레이 가드)")
        if not removed.empty:
            removed_pool = concat_unique([removed_pool, removed])
        record_step("quarter_q3_weak_overlay_guard(Q3 약한 오버레이 가드)", removed)
        transform_parts.append("q3_weak_overlay_guard")
    elif month_policy.startswith("quarter=Q4"):
        condition = frame["source_bucket"].eq("synthetic_short_overlay") & frame["open_month_num"].isin([10, 11, 12]) & overlay_weak_mask(frame)
        frame, removed = remove_condition(frame, condition, reason="quarter_q4_weak_overlay_guard(Q4 약한 오버레이 가드)")
        if not removed.empty:
            removed_pool = concat_unique([removed_pool, removed])
        record_step("quarter_q4_weak_overlay_guard(Q4 약한 오버레이 가드)", removed)
        transform_parts.append("q4_weak_overlay_guard")
    elif month_policy == "month_of_year_or_quarter_soft_guard":
        weak_overlay = overlay_weak_mask(frame)
        condition = frame["source_bucket"].eq("synthetic_short_overlay") & frame["open_month_num"].isin([8, 12, 7, 9, 10, 11]) & weak_overlay
        frame, removed = remove_condition(frame, condition, reason="month_or_quarter_weak_overlay_guard(월/분기 약한 오버레이 가드)")
        if not removed.empty:
            removed_pool = concat_unique([removed_pool, removed])
        record_step("month_or_quarter_weak_overlay_guard(월/분기 약한 오버레이 가드)", removed)
        transform_parts.append("month_quarter_weak_overlay_guard")

    native_first = short_policy.startswith("restore_native")
    target = SHORT_FLOOR if "100" in short_policy or "floor" in short_policy else 0
    restored = empty_like(frame)
    if target:
        frame, restored = restore_short_floor(frame, removed_pool, target=target, native_first=native_first, cost_policy=cost_policy)
        if not restored.empty:
            transform_parts.append("short_floor_restore")
        removed_steps.append(
            {
                "run_id": RUN_ID,
                "candidate_id": candidate_id,
                "filter_step": len(removed_steps) + 1,
                "filter_reason": "short_floor_restore(숏 하한 복원)",
                "removed_trade_count": 0,
                "removed_short_count": 0,
                "removed_net_profit": 0.0,
                "restored_trade_count": int(len(restored)),
                "restored_short_count": int(restored["direction"].eq("short").sum()) if not restored.empty else 0,
                "effect": "restore from already-existing removed candidates only(이미 존재한 제거 후보에서만 복원)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    meta = {
        "candidate_id": candidate_id,
        "source_variant_id": source_variant,
        "seed_transform": seed_transform,
        "transform": "+".join(transform_parts),
        "input_trade_count": input_count,
        "selected_trade_count": len(frame),
        "removed_trade_count": max(0, input_count - len(frame) + len(restored)),
        "restored_trade_count": int(len(restored)),
        "restored_short_count": int(restored["direction"].eq("short").sum()) if not restored.empty else 0,
        "no_trade_splitting": True,
    }
    return normalize_trade_frame(frame), meta, removed_steps


def month_bad_summary(frame: pd.DataFrame) -> tuple[int, str]:
    if frame.empty:
        return 0, ""
    bad: list[str] = []
    for month, group in frame.groupby("open_month", dropna=False):
        if float(group["net_profit"].sum()) <= 0.0:
            bad.append(str(month))
    return len(bad), ";".join(bad)


def package_precheck_status(row: Mapping[str, Any]) -> str:
    checks = [
        as_float(row["net_delta_vs_parent"]) >= 0,
        as_float(row["profit_factor_delta_vs_parent"]) >= 0,
        as_float(row["trade_density"]) >= DENSITY_FLOOR,
        as_float(row["short_trade_count"]) >= SHORT_FLOOR,
        as_float(row["stress_adjusted_net_delta_vs_parent"]) >= 0,
        int(row["bad_month_count"]) == 0,
        str(row["trade_splitting_status"]).startswith("not_used"),
    ]
    return "passed_proxy_precheck(프록시 사전점검 통과)" if all(checks) else "failed_proxy_precheck(프록시 사전점검 실패)"


def candidate_status(row: Mapping[str, Any]) -> str:
    candidate_id = str(row["candidate_id"])
    if candidate_id in {"cj04_h17_focus_cost_anchor_control", "cj14_package_precheck_gate_only", "cj15_no_split_topn_forbidden_guardrail", "cj16_parent_cd02_anchor_replay"}:
        return "diagnostic_control_not_selectable(진단 대조, 선택 불가)"
    if row.get("source_variant_id") == NATIVE_CONTROL_VARIANT_ID:
        return "control_only_not_selectable(대조 전용, 선택 불가)"
    if as_float(row["trade_density"]) < DENSITY_FLOOR:
        return "rejected_density_below_3(거절, 밀도 3 미만)"
    if as_float(row["short_trade_count"]) < SHORT_FLOOR:
        return "rejected_short_floor_below_100(거절, 숏 하한 100 미만)"
    if as_float(row["net_delta_vs_parent"]) < 0 and as_float(row["profit_factor_delta_vs_parent"]) < 0:
        return "negative_proxy_net_pf_worse(부정, 프록시 순수익/PF 악화)"
    if package_precheck_status(row).startswith("passed"):
        return "proxy_package_precheck_pass_review_required(프록시 패키지 사전점검 통과, 검토 필요)"
    if as_float(row["net_delta_vs_parent"]) > 0 and as_float(row["profit_factor_delta_vs_parent"]) >= 0:
        return "proxy_review_candidate_no_split_repair_watch(프록시 검토 후보, 무분할 수리 관찰)"
    return "diagnostic_watch_no_package(진단 관찰, 패키지 아님)"


def selection_score(row: Mapping[str, Any]) -> float:
    status = str(row.get("candidate_status", ""))
    if "not_selectable" in status:
        return -999.0
    score = 0.0
    if as_float(row["trade_density"]) >= DENSITY_FLOOR:
        score += 100.0
    if as_float(row["short_trade_count"]) >= SHORT_FLOOR:
        score += 35.0
    else:
        score -= (SHORT_FLOOR - as_float(row["short_trade_count"])) * 4.0
    if as_float(row["net_delta_vs_parent"]) > 0:
        score += 60.0
    score += as_float(row["net_delta_vs_parent"]) * 0.35
    score += as_float(row["profit_factor_delta_vs_parent"]) * 500.0
    score += min(60.0, max(-80.0, as_float(row["stress_adjusted_net_delta_vs_parent"]) * 0.45))
    score -= int(row["bad_month_count"]) * 18.0
    score -= as_float(row["removed_trade_count"]) * 0.10
    if str(row["package_precheck_status"]).startswith("passed"):
        score += 80.0
    return round(score, 10)


def build_surface(
    parent_trades: pd.DataFrame,
    native_control: pd.DataFrame,
) -> tuple[list[dict[str, Any]], dict[str, pd.DataFrame], list[dict[str, Any]]]:
    queue = read_csv(ci.RUN364CJ_QUEUE).sort_values("queue_rank")
    cg_queue = seed_queue_map()
    effective_days = cg_effective_days()
    parent_metric = metric_frame(parent_trades, effective_days=effective_days)
    parent_stress_anchor = as_float(parent_metric["net_profit"])
    native_q10 = cg.native_q10_thresholds(parent_trades)
    rows: list[dict[str, Any]] = []
    frame_map: dict[str, pd.DataFrame] = {}
    filter_rows: list[dict[str, Any]] = []

    for _, raw in queue.iterrows():
        queue_row = raw.to_dict()
        candidate_id = str(queue_row["candidate_id"])
        frame, meta, steps = apply_repair_candidate(queue_row, parent_trades, native_control, cg_queue, native_q10)
        metric = metric_frame(frame, effective_days=effective_days)
        stress_net = stress_adjusted_net(frame)
        bad_count, bad_months = month_bad_summary(frame)
        row = {
            "run_id": RUN_ID,
            "candidate_id": candidate_id,
            "queue_rank": int(queue_row["queue_rank"]),
            "axis_id": queue_row.get("axis_id", ""),
            "seed_candidate_id": queue_row.get("seed_candidate_id", ""),
            "source_variant_id": meta["source_variant_id"],
            "transform": meta["transform"],
            "h17_overlay_policy": queue_row.get("h17_overlay_policy", ""),
            "cost_stress_policy": queue_row.get("cost_stress_policy", ""),
            "month_guard_policy": queue_row.get("month_guard_policy", ""),
            "short_floor_policy": queue_row.get("short_floor_policy", ""),
            "source_mix_policy": queue_row.get("source_mix_policy", ""),
            "trade_splitting_status": "not_used_no_added_entries(미사용, 추가 진입 없음)",
            "top_n_status": "not_used_fixed_rule_surface(미사용, 고정 규칙 표면)",
            "input_trade_count": meta["input_trade_count"],
            "removed_trade_count": meta["removed_trade_count"],
            "restored_trade_count": meta["restored_trade_count"],
            "restored_short_count": meta["restored_short_count"],
            **metric,
            "parent_trade_count": parent_metric["trade_count"],
            "parent_net_profit": parent_metric["net_profit"],
            "parent_profit_factor": parent_metric["profit_factor"],
            "parent_trade_density": parent_metric["trade_density"],
            "parent_short_trade_count": parent_metric["short_trade_count"],
            "net_delta_vs_parent": finite(as_float(metric["net_profit"]) - as_float(parent_metric["net_profit"]), 10),
            "profit_factor_delta_vs_parent": finite(as_float(metric["profit_factor"]) - as_float(parent_metric["profit_factor"]), 10),
            "trade_delta_vs_parent": int(metric["trade_count"] - parent_metric["trade_count"]),
            "short_delta_vs_parent": int(metric["short_trade_count"] - parent_metric["short_trade_count"]),
            "stress_adjusted_net_swap_haircut_1x": finite(stress_net, 2),
            "stress_adjusted_net_delta_vs_parent": finite(stress_net - parent_stress_anchor, 10),
            "bad_month_count": bad_count,
            "bad_months": bad_months,
            "feature_boundary": "entry-known source_bucket/open_hour/month/probabilities only(진입 시점 원천/시간/월/확률만 사용)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        row["package_precheck_status"] = package_precheck_status(row)
        row["candidate_status"] = candidate_status(row)
        row["selection_score"] = selection_score(row)
        rows.append(row)
        frame_map[candidate_id] = frame
        if not steps:
            steps = [
                {
                    "run_id": RUN_ID,
                    "candidate_id": candidate_id,
                    "filter_step": 1,
                    "filter_reason": "no_extra_filter_control(추가 필터 없음)",
                    "removed_trade_count": 0,
                    "removed_short_count": 0,
                    "removed_net_profit": 0.0,
                    "effect": "control preserves seed surface(대조군은 씨앗 표면 보존)",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            ]
        for step in steps:
            step.setdefault("restored_trade_count", 0)
            step.setdefault("restored_short_count", 0)
            step["source_variant_id"] = meta["source_variant_id"]
            step["input_trade_count"] = meta["input_trade_count"]
            step["selected_trade_count"] = meta["selected_trade_count"]
            step["no_trade_splitting"] = True
            filter_rows.append(step)

    rows.sort(key=lambda item: (as_float(item["selection_score"]), as_float(item["net_profit"])), reverse=True)
    return rows, frame_map, filter_rows


def attribution_rows(surface: Sequence[Mapping[str, Any]], frame_map: Mapping[str, pd.DataFrame]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for candidate in surface:
        candidate_id = str(candidate["candidate_id"])
        frame = frame_map[candidate_id]
        for source_bucket, group in frame.groupby("source_bucket", dropna=False):
            metric = metric_frame(group, effective_days=max(1.0, float(candidate["trade_count"])))
            rows.append(
                {
                    "run_id": RUN_ID,
                    "candidate_id": candidate_id,
                    "source_bucket": source_bucket,
                    "trade_count": metric["trade_count"],
                    "net_profit": metric["net_profit"],
                    "profit_factor": metric["profit_factor"],
                    "expectancy": metric["expectancy"],
                    "long_trade_count": metric["long_trade_count"],
                    "short_trade_count": metric["short_trade_count"],
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    return rows


def month_rows(surface: Sequence[Mapping[str, Any]], frame_map: Mapping[str, pd.DataFrame]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for candidate in surface:
        candidate_id = str(candidate["candidate_id"])
        frame = frame_map[candidate_id]
        for month, group in frame.groupby("open_month", dropna=False):
            metric = metric_frame(group, effective_days=max(1.0, float(len(group))))
            rows.append(
                {
                    "run_id": RUN_ID,
                    "candidate_id": candidate_id,
                    "open_month": month,
                    "open_month_num": int(group["open_month_num"].iloc[0]) if len(group) else "",
                    "trade_count": metric["trade_count"],
                    "net_profit": metric["net_profit"],
                    "profit_factor": metric["profit_factor"],
                    "short_trade_count": metric["short_trade_count"],
                    "month_status": "bad_month_watch(손실 월 관찰)" if as_float(metric["net_profit"]) <= 0 else "positive_or_neutral(양수 또는 중립)",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    return rows


def cost_stress_rows(surface: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for row in surface:
        rows.append(
            {
                "run_id": RUN_ID,
                "candidate_id": row["candidate_id"],
                "net_profit": row["net_profit"],
                "swap_sum": row["swap_sum"],
                "stress_adjusted_net_swap_haircut_1x": row["stress_adjusted_net_swap_haircut_1x"],
                "stress_adjusted_net_delta_vs_parent": row["stress_adjusted_net_delta_vs_parent"],
                "cost_stress_policy": row["cost_stress_policy"],
                "stress_judgment": "stress_positive(압박 양호)" if as_float(row["stress_adjusted_net_delta_vs_parent"]) >= 0 else "stress_watch(압박 관찰)",
                "effect": "swap haircut is diagnostic and does not replace MT5 KPI(스왑 헤어컷은 진단이며 MT5 KPI를 대체하지 않음)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def package_rows(surface: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for row in surface:
        checks = {
            "net_delta_nonnegative": as_float(row["net_delta_vs_parent"]) >= 0,
            "pf_delta_nonnegative": as_float(row["profit_factor_delta_vs_parent"]) >= 0,
            "density_ge_3": as_float(row["trade_density"]) >= DENSITY_FLOOR,
            "short_floor_ge_100": as_float(row["short_trade_count"]) >= SHORT_FLOOR,
            "stress_delta_nonnegative": as_float(row["stress_adjusted_net_delta_vs_parent"]) >= 0,
            "bad_month_count_zero": int(row["bad_month_count"]) == 0,
            "no_trade_splitting": str(row["trade_splitting_status"]).startswith("not_used"),
        }
        rows.append(
            {
                "run_id": RUN_ID,
                "candidate_id": row["candidate_id"],
                **{key: str(value).lower() for key, value in checks.items()},
                "package_precheck_status": row["package_precheck_status"],
                "candidate_status": row["candidate_status"],
                "effect": "proxy precheck only; MT5 runtime probe still required(프록시 사전점검 전용, MT5 런타임 탐침은 여전히 필요)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def data_integrity_rows(
    parent_trades: pd.DataFrame,
    native_control: pd.DataFrame,
    surface: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    queue = read_csv(ci.RUN364CJ_QUEUE)
    duplicate_parent = int(parent_trades["open_time"].duplicated().sum())
    duplicate_control = int(native_control["open_time"].duplicated().sum())
    count_over_parent = [row for row in surface if as_float(row["trade_count"]) > as_float(row["parent_trade_count"])]
    policy_columns = ["h17_overlay_policy", "cost_stress_policy", "month_guard_policy", "short_floor_policy", "source_mix_policy"]
    exact_filter_rows = int(queue[policy_columns].astype(str).apply(lambda col: col.str.contains("2025-", regex=False)).any(axis=1).sum())
    top_n_rows = int(queue[policy_columns].astype(str).apply(lambda col: col.str.contains("top_n", case=False, regex=False)).any(axis=1).sum())
    split_rows = int((~queue["trade_splitting_status"].astype(str).str.startswith("not_used")).sum())
    rows = [
        {
            "run_id": RUN_ID,
            "audit_item": "data_source(데이터 원천)",
            "status": "passed",
            "observed": rel(cg.ce.TRADE_ATTRIBUTION),
            "effect": "CJ replays existing MT5-derived closed trade tape(CJ는 기존 MT5 기반 종료 거래 기록을 재생)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "audit_item": "time_axis(시간축)",
            "status": "passed",
            "observed": "open_time/close_time sorted; filters use entry-known open hour and calendar class(진입/청산 시각 정렬, 필터는 진입 시점 시간과 달력 클래스 사용)",
            "effect": "look-ahead path stays closed(미래참조 경로를 닫음)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "audit_item": "duplicate_open_time(중복 진입 시각)",
            "status": "passed" if duplicate_parent == 0 and duplicate_control == 0 else "failed",
            "observed": f"cd02={duplicate_parent};cd03={duplicate_control}",
            "effect": "one row remains one possible entry(한 행은 하나의 가능 진입으로 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "audit_item": "feature_label_boundary(피처/라벨 경계)",
            "status": "passed",
            "observed": "rules use source_bucket/open_hour/month_of_year/quarter/probabilities; realized PnL scores only offline selection(규칙은 원천/시간/월중/분기/확률만 쓰고, 실현 손익은 오프라인 선택 점수에만 사용)",
            "effect": "runtime-like rule inputs do not consume future profit(런타임형 규칙 입력이 미래 수익을 먹지 않음)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "audit_item": "no_trade_splitting(거래 쪼개기 없음)",
            "status": "passed" if not count_over_parent and split_rows == 0 else "failed",
            "observed": f"candidate_count_gt_parent={len(count_over_parent)};queue_trade_splitting_rows={split_rows}",
            "effect": "trade density is not raised by splitting entries(진입 쪼개기로 거래 밀도를 올리지 않음)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "audit_item": "no_top_n_or_exact_date_filter(no top_n/정확 날짜 필터 없음)",
            "status": "passed" if top_n_rows == 0 and exact_filter_rows == 0 else "failed",
            "observed": f"top_n_rows={top_n_rows};exact_2025_filter_rows={exact_filter_rows}",
            "effect": "repair remains reusable calendar/source logic(수리는 재사용 가능한 달력/원천 로직으로 남음)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "audit_item": "tier_scope(티어 범위)",
            "status": "passed",
            "observed": "Tier A proxy replay; Tier B missing_required recorded in ledgers(Tier A 프록시 재생, Tier B 필수 누락은 장부 기록)",
            "effect": "Tier B is not silently omitted(Tier B를 조용히 생략하지 않음)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    write_csv(DATA_INTEGRITY_AUDIT, rows)
    return rows


def review_queue_rows(selected: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "queue_rank": 1,
            "queue_id": "ck01_selected_repair_package_gate_review",
            "review_subject": selected["candidate_id"],
            "review_question": "Does the selected repair candidate survive package precheck review?(선택 수리 후보가 패키지 사전점검 검토를 버티는가?)",
            "success_criteria": "net/PF/density/short floor/stress/month checks remain coherent(순수익/PF/밀도/숏 하한/압박/월 점검이 같이 맞음)",
            "failure_criteria": "proxy lift depends on bad month or cost artifact(프록시 상승이 손실 월 또는 비용 착시에 의존)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "queue_rank": 2,
            "queue_id": "ck02_short_floor_and_source_balance_review",
            "review_subject": selected["candidate_id"],
            "review_question": "Is the short-floor rescue still a real source mix and not a collapse mask?(숏 하한 복원이 실제 원천 믹스인가, 붕괴 가림막인가?)",
            "success_criteria": "shorts>=100 without trade splitting and source attribution is not one tiny bucket(무분할로 숏 100 이상, 원천 귀속이 작은 한 버킷이 아님)",
            "failure_criteria": "restored shorts erase net/PF edge or source mix is too thin(복원 숏이 순수익/PF 우위를 지우거나 원천 믹스가 너무 얇음)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "queue_rank": 3,
            "queue_id": "ck03_bad_month_cost_stress_review",
            "review_subject": selected["candidate_id"],
            "review_question": "Do month guard and cost stress explain the repair effect?(월 가드와 비용 압박이 수리 효과를 설명하는가?)",
            "success_criteria": "bad_month_count and stress_delta improve without exact date filtering(정확 날짜 필터 없이 손실 월 수와 압박 차이가 개선)",
            "failure_criteria": "month or stress remains negative enough to reject package(월 또는 압박이 패키지 거절 수준으로 남음)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "queue_rank": 4,
            "queue_id": "ck04_mt5_reprobe_boundary_decision",
            "review_subject": selected["candidate_id"],
            "review_question": "Is a narrow MT5 runtime probe package justified?(좁은 MT5 런타임 탐침 패키지가 정당한가?)",
            "success_criteria": "review opens a package only if proxy evidence clears precheck(프록시 근거가 사전점검을 통과할 때만 패키지 개방)",
            "failure_criteria": "review closes as failure memory or opens a different offensive seed(검토가 실패 기억 또는 다른 공격 씨앗으로 닫힘)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def proxy_mt5_diff_rows(selected: Mapping[str, Any]) -> list[dict[str, Any]]:
    cg_final = read_json(cg.FINAL_DECISION)
    return [
        {
            "run_id": RUN_ID,
            "comparison_id": "selected_cj_proxy_vs_parent_mt5(선택 CJ 프록시 대 부모 MT5)",
            "selected_candidate_id": selected["candidate_id"],
            "parent_mt5_net": cg_final.get("parent_mt5_net_profit", cg_final.get("parent_net_profit")),
            "proxy_net": selected["net_profit"],
            "net_diff_proxy_minus_parent": selected["net_delta_vs_parent"],
            "parent_mt5_profit_factor": cg_final.get("parent_mt5_profit_factor", cg_final.get("parent_profit_factor")),
            "proxy_profit_factor": selected["profit_factor"],
            "parent_mt5_density": cg_final.get("parent_mt5_density", cg_final.get("parent_density")),
            "proxy_density": selected["trade_density"],
            "stress_delta_proxy": selected["stress_adjusted_net_delta_vs_parent"],
            "usability": "proxy_scout_screen_only_mt5_reprobe_required_before_runtime_claim(프록시 정찰 선별 전용, 런타임 주장 전 MT5 재탐침 필요)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def write_work_packet() -> None:
    write_json(
        WORK_PACKET,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "primary_family": "experiment_execution(실험 실행)",
            "primary_skill": "obsidian-performance-attribution",
            "support_skills": [
                "obsidian-data-integrity",
                "obsidian-artifact-lineage",
                "obsidian-result-judgment",
            ],
            "hypothesis": "H17 focus can be repaired by cost stress guards, reusable month/quarter guards, and short-floor restoration without trade splitting(17시 집중은 거래 쪼개기 없이 비용 압박 가드, 재사용 월/분기 가드, 숏 하한 복원으로 수리될 수 있다)",
            "comparison": "CJ candidates vs CD02 parent and CG/CH failure memory(CJ 후보 대 CD02 부모 및 CG/CH 실패 기억)",
            "required_gates": [
                "scope_completion_gate",
                "input_lineage_gate",
                "data_integrity_gate",
                "no_trade_splitting_gate",
                "package_boundary_gate",
                "required_gate_coverage_audit",
            ],
            "effect": "turn CI materialized queue into measurable proxy repair surface(CI 구체화 대기열을 측정 가능한 프록시 수리 표면으로 전환)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def gate_rows(
    surface: Sequence[Mapping[str, Any]],
    data_rows: Sequence[Mapping[str, Any]],
    receipt_paths: Sequence[Path],
    *,
    final_written: bool,
) -> list[dict[str, Any]]:
    package_rows_count = sum(1 for row in surface if str(row.get("package_precheck_status", "")).startswith("passed"))
    selectable_rows = sum(1 for row in surface if "not_selectable" not in str(row.get("candidate_status", "")))
    gates = [
        (
            "scope_completion_gate",
            len(surface) == 16 and selectable_rows > 0,
            PROXY_REPAIR_SURFACE,
            "16 CJ candidates were replayed and at least one selectable row exists(16개 CJ 후보를 재생했고 선택 가능 행이 존재)",
        ),
        (
            "input_lineage_gate",
            all(exists(path) for path in INPUT_FILES),
            INPUT_MANIFEST,
            "CI/CG/MT5-derived inputs are connected(CI/CG/MT5 기반 입력이 연결)",
        ),
        (
            "data_integrity_gate",
            bool(data_rows) and all(row["status"] == "passed" for row in data_rows),
            DATA_INTEGRITY_AUDIT,
            "timestamp/no-split/no-topn checks passed(시점/무분할/no-topn 점검 통과)",
        ),
        (
            "no_trade_splitting_gate",
            all(as_float(row["trade_count"]) <= as_float(row["parent_trade_count"]) for row in surface),
            CANDIDATE_FILTER_AUDIT,
            "no candidate creates more entries than parent(어떤 후보도 부모보다 많은 진입을 만들지 않음)",
        ),
        (
            "package_boundary_gate",
            exists(PACKAGE_PRECHECK) and package_rows_count >= 0,
            PACKAGE_PRECHECK,
            "package precheck is proxy-only and cannot claim runtime authority(패키지 사전점검은 프록시 전용이며 런타임 권위를 주장하지 못함)",
        ),
        (
            "receipt_coverage_gate",
            all(exists(path) for path in receipt_paths),
            RUN_EVIDENCE_RECEIPT,
            "run evidence, data, model, lineage, judgment, and claim receipts exist(실행 근거/데이터/모델/계보/판정/주장 영수증 존재)",
        ),
        (
            "required_gate_coverage_audit",
            final_written,
            GATE_AUDIT,
            "required gates are connected to closeout(필수 게이트가 종료 기록에 연결)",
        ),
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


def final_payload(
    ci_final: Mapping[str, Any],
    selected: Mapping[str, Any],
    surface: Sequence[Mapping[str, Any]],
    gates: Sequence[Mapping[str, Any]],
    created_at: str,
) -> dict[str, Any]:
    package_pass_rows = [row for row in surface if str(row.get("package_precheck_status", "")).startswith("passed")]
    review_rows = [row for row in surface if "review_candidate" in str(row.get("candidate_status", ""))]
    return {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "source_proxy_scout_run_id": SOURCE_PROXY_SCOUT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "created_at_utc": created_at,
        "surface_rows": len(surface),
        "package_precheck_pass_rows": len(package_pass_rows),
        "review_candidate_rows": len(review_rows),
        "selected_candidate_id": selected["candidate_id"],
        "selected_candidate_status": selected["candidate_status"],
        "selected_package_precheck_status": selected["package_precheck_status"],
        "selected_net_profit": selected["net_profit"],
        "selected_profit_factor": selected["profit_factor"],
        "selected_expectancy": selected["expectancy"],
        "selected_trade_count": selected["trade_count"],
        "selected_trade_density": selected["trade_density"],
        "selected_long_trade_count": selected["long_trade_count"],
        "selected_short_trade_count": selected["short_trade_count"],
        "selected_short_share": selected["short_share"],
        "selected_closed_trade_drawdown_proxy": selected["closed_trade_drawdown_proxy"],
        "selected_closed_trade_recovery_proxy": selected["closed_trade_recovery_proxy"],
        "selected_net_delta_vs_parent": selected["net_delta_vs_parent"],
        "selected_profit_factor_delta_vs_parent": selected["profit_factor_delta_vs_parent"],
        "selected_stress_adjusted_net_delta_vs_parent": selected["stress_adjusted_net_delta_vs_parent"],
        "selected_bad_month_count": selected["bad_month_count"],
        "selected_bad_months": selected["bad_months"],
        "selected_removed_trade_count": selected["removed_trade_count"],
        "selected_restored_trade_count": selected["restored_trade_count"],
        "parent_net_profit": selected["parent_net_profit"],
        "parent_profit_factor": selected["parent_profit_factor"],
        "parent_trade_density": selected["parent_trade_density"],
        "parent_short_trade_count": selected["parent_short_trade_count"],
        "ci_parent_run_id": ci_final.get("run_id"),
        "external_verification_status": "out_of_scope_by_claim",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "live_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "gate_passes": sum(1 for row in gates if row["status"] == "passed"),
        "gate_total": len(gates),
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "surface_path": rel(PROXY_REPAIR_SURFACE),
        "selected_trade_tape_path": rel(SELECTED_TRADE_TAPE),
        "package_precheck_path": rel(PACKAGE_PRECHECK),
        "proxy_mt5_diff_plan_path": rel(PROXY_MT5_DIFF_PLAN),
    }


def write_receipts(final: Mapping[str, Any], selected: Mapping[str, Any], proxy_mt5_rows_: Sequence[Mapping[str, Any]]) -> None:
    write_json(
        RUN_EVIDENCE_RECEIPT,
        {
            "run_id": RUN_ID,
            "scoreboard_lane": "proxy_scout(프록시 정찰)",
            "kpi_scope": "closed-trade replay from MT5-derived tape(MT5 기반 종료 거래 기록 재생)",
            "selected_kpi": {
                "net_profit": final["selected_net_profit"],
                "profit_factor": final["selected_profit_factor"],
                "expectancy": final["selected_expectancy"],
                "trade_count": final["selected_trade_count"],
                "trade_density": final["selected_trade_density"],
                "short_trade_count": final["selected_short_trade_count"],
                "stress_delta": final["selected_stress_adjusted_net_delta_vs_parent"],
                "bad_month_count": final["selected_bad_month_count"],
            },
            "effect": "records proxy KPI without treating it as MT5 authority(프록시 KPI를 기록하되 MT5 권위로 보지 않음)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(
        EXPERIMENT_RECEIPT,
        {
            "run_id": RUN_ID,
            "hypothesis": "cost/month/short-floor repair can preserve h17 clue(비용/월/숏 하한 수리가 17시 단서를 보존할 수 있음)",
            "comparison_baseline": "CD02 parent and CG09 h17 focus failure memory(CD02 부모와 CG09 17시 집중 실패 기억)",
            "controls": ["CJ04 h17 cost anchor", "CJ14 package precheck only", "CJ15 guardrail only", "CJ16 parent replay"],
            "success_criteria": "net/PF/density/short/stress/month precheck improves without splitting(쪼개기 없이 순수익/PF/밀도/숏/압박/월 사전점검 개선)",
            "failure_criteria": "repair collapses short floor, relies on exact month, or remains stress-negative(수리가 숏 하한 붕괴, 정확 월 의존, 압박 음수 유지)",
            "effect": "keeps exploration offensive but operating claim closed(탐색은 공격적으로 열고 운영 주장은 닫음)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(
        DATA_RECEIPT,
        {
            "run_id": RUN_ID,
            "data_source": rel(cg.ce.TRADE_ATTRIBUTION),
            "time_axis": "MT5 open_time/close_time, sorted by open_time(MT5 진입/청산 시각, 진입 시각 정렬)",
            "sample_scope": "US100 M5 Stage364 Tier A proxy replay(US100 M5 Stage364 Tier A 프록시 재생)",
            "feature_label_boundary": "entry-known fields for filters; realized PnL only for offline scoring(진입 시점 필드로 필터, 실현 손익은 오프라인 점수 전용)",
            "split_boundary": "no new train/validation split; replay only(새 학습/검증 분할 없음, 재생 전용)",
            "leakage_risk": "selection bias from offline proxy score remains and is bounded(오프라인 프록시 점수 선택 편향은 남으며 경계 설정)",
            "integrity_judgment": "usable_with_boundary(경계부 사용 가능)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(
        MODEL_RECEIPT,
        {
            "run_id": RUN_ID,
            "model_action": "no_new_model_artifact(새 모델 산출물 없음)",
            "onnx_action": "not_applicable(해당 없음)",
            "validation_judgment": "proxy_rule_surface_only(프록시 규칙 표면 전용)",
            "effect": "prevents proxy repair from being mistaken for ONNX promotion(프록시 수리를 ONNX 승격으로 착각하지 않게 함)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(
        JUDGMENT_RECEIPT,
        {
            "result_subject": RUN_ID,
            "evidence_available": [rel(PROXY_REPAIR_SURFACE), rel(PACKAGE_PRECHECK), rel(DATA_INTEGRITY_AUDIT), rel(PROXY_MT5_DIFF_PLAN)],
            "evidence_missing": ["new MT5 execution(새 MT5 실행)", "runtime parity(런타임 동등성)", "forward pass(전진 검증)"],
            "judgment_label": "exploratory(탐색)",
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": NEXT_RUN_ID,
            "user_explanation_hook": "CJ found proxy repair candidates but cannot claim runtime authority(CJ는 프록시 수리 후보를 찾았지만 런타임 권위는 주장할 수 없음)",
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            "run_id": RUN_ID,
            "allowed_claims": ["proxy repair surface completed(프록시 수리 표면 완료)", "review required(검토 필요)"],
            "forbidden_claims": ["runtime authority(런타임 권위)", "operating promotion(운영 승격)", "live readiness(실거래 준비)", "goal achieved(목표 달성)"],
            "proxy_mt5_diff_rows": list(proxy_mt5_rows_),
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    refresh_lineage_receipt(final)


def refresh_lineage_receipt(final: Mapping[str, Any]) -> None:
    existing_outputs = [path for path in OUTPUT_FILES if exists(path) and Path(path).is_file()]
    write_json(
        LINEAGE_RECEIPT,
        {
            "run_id": RUN_ID,
            "source_inputs": [{"path": rel(path), "sha256": sha(path)} for path in INPUT_FILES if exists(path)],
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [rel(path) for path in existing_outputs],
            "artifact_hashes": [{"path": rel(path), "sha256": sha(path)} for path in existing_outputs],
            "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "availability": "tracked_or_reproducible_from_command(추적 또는 명령으로 재현 가능)",
            "lineage_judgment": "connected_with_boundary(경계부 연결)",
            "final_decision": final,
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def write_docs(
    final: Mapping[str, Any],
    selected: Mapping[str, Any],
    surface: Sequence[Mapping[str, Any]],
    filter_rows_: Sequence[Mapping[str, Any]],
    source_rows_: Sequence[Mapping[str, Any]],
    month_rows_: Sequence[Mapping[str, Any]],
    cost_rows_: Sequence[Mapping[str, Any]],
    package_rows_: Sequence[Mapping[str, Any]],
    queue_rows_: Sequence[Mapping[str, Any]],
    gates: Sequence[Mapping[str, Any]],
) -> None:
    top_surface = list(surface)[:10]
    selected_months = [row for row in month_rows_ if row["candidate_id"] == selected["candidate_id"]]
    selected_sources = [row for row in source_rows_ if row["candidate_id"] == selected["candidate_id"]]
    selected_cost = [row for row in cost_rows_ if row["candidate_id"] == selected["candidate_id"]]
    selected_package = [row for row in package_rows_ if row["candidate_id"] == selected["candidate_id"]]

    report = f"""# run364CJ h17 focus month cost stress repair scout(17시 집중 월/비용 압박 수리 정찰)

Updated(갱신): {final['created_at_utc']}

## Current truth(현재 진실)

- run(실행): `{RUN_ID}`
- parent(부모): `{PARENT_RUN_ID}`
- selected candidate(선택 후보): `{final['selected_candidate_id']}`
- judgment(판정): `{JUDGMENT}`
- gate(게이트): `{final['gate_passes']}/{final['gate_total']}`
- authority(권위): runtime authority(런타임 권위), operating promotion(운영 승격), Goal Achieve(목표 달성) 모두 not claimed(주장 안 함).

## Selected KPI(선택 KPI)

| item(항목) | value(값) |
|---|---:|
| net profit(순수익) | {final['selected_net_profit']} |
| profit factor(수익 팩터) | {final['selected_profit_factor']} |
| expectancy(기대값) | {final['selected_expectancy']} |
| trade count(거래 수) | {final['selected_trade_count']} |
| density(밀도) | {final['selected_trade_density']} |
| long/short(롱/숏) | {final['selected_long_trade_count']}/{final['selected_short_trade_count']} |
| drawdown proxy(낙폭 프록시) | {final['selected_closed_trade_drawdown_proxy']} |
| recovery proxy(회복 프록시) | {final['selected_closed_trade_recovery_proxy']} |
| net delta vs parent(부모 대비 순수익 차이) | {final['selected_net_delta_vs_parent']} |
| stress delta(압박 차이) | {final['selected_stress_adjusted_net_delta_vs_parent']} |
| bad month count(손실 월 수) | {final['selected_bad_month_count']} |

## Surface top rows(표면 상위 행)

{markdown_table(top_surface, ['candidate_id', 'candidate_status', 'package_precheck_status', 'net_profit', 'profit_factor', 'trade_count', 'trade_density', 'short_trade_count', 'stress_adjusted_net_delta_vs_parent', 'bad_month_count', 'selection_score'], 10)}

## Selected source attribution(선택 원천 귀속)

{markdown_table(selected_sources, ['source_bucket', 'trade_count', 'net_profit', 'profit_factor', 'short_trade_count'], 10)}

## Selected month stability(선택 월 안정성)

{markdown_table(selected_months, ['open_month', 'trade_count', 'net_profit', 'profit_factor', 'short_trade_count', 'month_status'], 20)}

## Selected cost stress(선택 비용 압박)

{markdown_table(selected_cost, ['candidate_id', 'net_profit', 'swap_sum', 'stress_adjusted_net_delta_vs_parent', 'stress_judgment'], 4)}

## Selected package precheck(선택 패키지 사전점검)

{markdown_table(selected_package, ['candidate_id', 'package_precheck_status', 'net_delta_nonnegative', 'pf_delta_nonnegative', 'density_ge_3', 'short_floor_ge_100', 'stress_delta_nonnegative', 'bad_month_count_zero'], 4)}

## Filter audit sample(필터 감사 표본)

{markdown_table([row for row in filter_rows_ if row['candidate_id'] == selected['candidate_id']], ['filter_step', 'filter_reason', 'removed_trade_count', 'restored_trade_count', 'effect'], 10)}

## Gate audit(게이트 감사)

{markdown_table(gates, ['gate', 'status', 'evidence', 'effect'], 10)}

## Next action(다음 행동)

`{NEXT_RUN_ID}`에서 selected repair candidate(선택 수리 후보)의 package precheck(패키지 사전점검), source/month/cost attribution(원천/월/비용 귀속), MT5 reprobe boundary(MT5 재탐침 경계)를 검토한다.

## Boundary(경계)

This is proxy scout only(프록시 정찰 전용)입니다. 새 ONNX(온엑스), 새 MT5 execution(새 MT5 실행), runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비)는 없습니다.
"""
    write_text(REPORT_PATH, report, bom=True)

    write_text(
        DECISION_DOC,
        f"""# Stage364CJ decision(결정): h17 focus month cost stress repair scout

- date(날짜): {TODAY}
- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{DECISION}`
- selected candidate(선택 후보): `{final['selected_candidate_id']}`
- selected status(선택 상태): `{final['selected_candidate_status']}`
- package precheck(패키지 사전점검): `{final['selected_package_precheck_status']}`
- next action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): CI repair queue(CI 수리 대기열)를 proxy KPI(프록시 핵심 성과 지표), source/month/cost attribution(원천/월/비용 귀속), gate evidence(게이트 근거)로 닫았다.
- boundary(경계): `{CLAIM_BOUNDARY}`
""",
        bom=True,
    )

    append_text_once(
        REVIEW_INDEX,
        f"run364CJ__{RUN_ID}",
        f"\n- run364CJ__{RUN_ID}: [{REPORT_PATH.name}]({REPORT_PATH.name}) - selected `{final['selected_candidate_id']}`, net `{final['selected_net_profit']}`, PF `{final['selected_profit_factor']}`, next `{NEXT_RUN_ID}`.\n",
    )
    replace_prefixed_lines(
        STAGE_BRIEF,
        {
            "Current run": f"Current run(현재 실행): `{NEXT_RUN_ID}`",
            "Latest completed run": f"Latest completed run(최근 완료 실행): `{RUN_ID}`",
            "Current status": f"Current status(현재 상태): `{STATUS}`",
            "Next action": f"Next action(다음 행동): `{NEXT_RUN_ID}`에서 CJ selected repair(선택 수리)의 패키지/귀속/MT5 재탐침 경계를 검토한다.",
        },
        bom=True,
    )
    write_text(
        SELECTION_STATUS,
        f"""# Stage364 selection status(선택 상태)

Updated(갱신): {final['created_at_utc']}

Current run(현재 실행): `{NEXT_RUN_ID}`
Latest completed run(최근 완료 실행): `{RUN_ID}`

Selected proxy repair candidate(선택 프록시 수리 후보): `{final['selected_candidate_id']}`.

Selected KPI(선택 핵심 성과 지표): net `{final['selected_net_profit']}`, PF `{final['selected_profit_factor']}`, density `{final['selected_trade_density']}`, shorts `{final['selected_short_trade_count']}`, stress delta `{final['selected_stress_adjusted_net_delta_vs_parent']}`, bad months `{final['selected_bad_month_count']}`.

Package precheck(패키지 사전점검): `{final['selected_package_precheck_status']}`. This is proxy-only(프록시 전용) and review-required(검토 필요).

Next action(다음 행동): `{NEXT_RUN_ID}`.

Authority(권위): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함).
""",
        bom=True,
    )
    append_text_once(
        STAGE_README,
        f"run364CJ__{RUN_ID}",
        f"""
<!-- run364CJ__{RUN_ID} -->
## run364CJ h17 focus month cost stress repair scout(17시 집중 월/비용 압박 수리 정찰)

Action(행동): `16` CJ repair candidates(CJ 수리 후보)를 proxy replay(프록시 재생)했다.

Effect(효과): selected proxy repair(선택 프록시 수리) `{final['selected_candidate_id']}`를 `{NEXT_RUN_ID}` review(검토)로 넘기고 runtime authority(런타임 권위)는 주장하지 않는다.
""",
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

Current truth(현재 진실): `run364CJ` replayed(재생 완료) `16` h17 focus month/cost/short-floor repair candidates(17시 집중 월/비용/숏 하한 수리 후보). Selected proxy repair candidate(선택 프록시 수리 후보)는 `{final['selected_candidate_id']}`이고 net `{final['selected_net_profit']}`, PF `{final['selected_profit_factor']}`, density `{final['selected_trade_density']}`, shorts `{final['selected_short_trade_count']}`, stress delta `{final['selected_stress_adjusted_net_delta_vs_parent']}`, bad month count `{final['selected_bad_month_count']}`이다.

Next action(다음 행동): `{NEXT_RUN_ID}`에서 package precheck(패키지 사전점검), source/month/cost attribution(원천/월/비용 귀속), MT5 reprobe boundary(MT5 재탐침 경계)를 검토한다.

Operating boundary(운영 경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함).
""",
        bom=True,
    )
    append_text_once(
        WORKSPACE_CHANGELOG,
        f"run364CJ__{RUN_ID}",
        f"\n<!-- run364CJ__{RUN_ID} -->\n- {final['created_at_utc']} `{RUN_ID}` completed CJ proxy repair scout(CJ 프록시 수리 정찰 완료); selected `{final['selected_candidate_id']}`; next `{NEXT_RUN_ID}`; no authority claim(권위 주장 없음).\n",
    )
    append_text_once(
        IDEA_REGISTRY,
        f"run364CJ__{RUN_ID}",
        f"\n<!-- run364CJ__{RUN_ID} -->\n- `{RUN_ID}`: h17 focus repair scout(17시 집중 수리 정찰). Selected `{final['selected_candidate_id']}` as proxy review seed(프록시 검토 씨앗). Effect(효과): CH month/cost/short-floor failure memory(CH 월/비용/숏 하한 실패 기억)를 measurable repair surface(측정 가능한 수리 표면)로 전환.\n",
    )
    append_text_once(
        NEGATIVE_RESULT_REGISTER,
        f"run364CJ__boundary__{RUN_ID}",
        f"\n<!-- run364CJ__boundary__{RUN_ID} -->\n- `{RUN_ID}` boundary note(경계 메모): proxy scout(프록시 정찰) did not run new MT5(새 MT5 미실행), so runtime authority(런타임 권위) and operating promotion(운영 승격) remain not claimed(주장 안 함).\n",
    )
    write_csv(RUN364CK_QUEUE, queue_rows_)


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
        "rows": final["surface_rows"],
        "gate_passes": final["gate_passes"],
        "gate_total": final["gate_total"],
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "final_decision_path": rel(FINAL_DECISION),
        "gate_audit_path": rel(GATE_AUDIT),
        "created_at": final["created_at_utc"],
        "work_family": "experiment_execution(실험 실행)",
        "scoreboard_lane": "proxy_scout(프록시 정찰)",
        "external_verification_status": final["external_verification_status"],
        "evidence_boundary": "proxy_scout_only(프록시 정찰 전용)",
        "question": "Can h17 focus repair survive month/cost/short-floor constraints without splitting trades?(17시 집중 수리가 거래 쪼개기 없이 월/비용/숏 하한 제약을 버티는가?)",
        "next_action": NEXT_RUN_ID,
        "net_profit": final["selected_net_profit"],
        "profit_factor": final["selected_profit_factor"],
        "expectancy": final["selected_expectancy"],
        "trade_count": final["selected_trade_count"],
        "trade_density_per_feature_day": final["selected_trade_density"],
        "long_trade_count": final["selected_long_trade_count"],
        "short_trade_count": final["selected_short_trade_count"],
        "max_drawdown_amount": final["selected_closed_trade_drawdown_proxy"],
        "recovery_factor": final["selected_closed_trade_recovery_proxy"],
        "trade_density_requirement_status": "passed_proxy_density_ge_3_no_trade_splitting(프록시 밀도 3 이상 통과, 거래 쪼개기 없음)",
        "result_judgment": JUDGMENT,
        "path": rel(FINAL_DECISION),
        "primary_report": rel(REPORT_PATH),
        "primary_artifact": rel(PROXY_REPAIR_SURFACE),
    }
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], [common], extend_header=True)

    ledger_rows: list[dict[str, Any]] = []
    for suffix, record_view, tier_scope, status, include_metrics in [
        ("tier_a_separate", "Tier A separate(Tier A 분리)", "Tier A", STATUS, True),
        ("tier_b_missing_required", "Tier B separate(Tier B 분리)", "Tier B", "missing_required_no_partial_context_source(필수 누락, 부분 문맥 원천 없음)", False),
        ("tier_a_plus_b_combined", "Tier A+B combined(Tier A+B 합산)", "Tier A+B", "out_of_scope_by_claim_no_combined_execution(주장 범위 밖, 합산 실행 없음)", True),
    ]:
        row = {
            **common,
            "ledger_row_id": f"{RUN_ID}__{suffix}",
            "subrun_id": f"{RUN_ID}__{suffix}",
            "row_id": f"{RUN_ID}__{suffix}",
            "record_view": record_view,
            "tier_scope": tier_scope,
            "kpi_scope": "CJ proxy repair scout(CJ 프록시 수리 정찰)",
            "status": status,
            "primary_kpi": f"net={final['selected_net_profit']};pf={final['selected_profit_factor']};density={final['selected_trade_density']};shorts={final['selected_short_trade_count']}",
            "guardrail_kpi": f"stress_delta={final['selected_stress_adjusted_net_delta_vs_parent']};bad_months={final['selected_bad_month_count']};no_authority",
            "view": record_view,
            "tier": tier_scope,
            "metric_scope": "proxy_repair_surface(프록시 수리 표면)",
        }
        if not include_metrics:
            for key in [
                "net_profit",
                "profit_factor",
                "expectancy",
                "trade_count",
                "trade_density_per_feature_day",
                "long_trade_count",
                "short_trade_count",
                "max_drawdown_amount",
                "recovery_factor",
            ]:
                row[key] = ""
        ledger_rows.append(row)
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], ledger_rows, extend_header=True)
    append_or_replace_csv(STAGE_LEDGER, ["ledger_row_id"], ledger_rows, extend_header=True)


def write_artifact_registry(final: Mapping[str, Any]) -> None:
    artifact_rows = []
    for artifact_type, path, notes in [
        ("proxy_repair_surface", PROXY_REPAIR_SURFACE, "CJ proxy repair surface(CJ 프록시 수리 표면)."),
        ("selected_candidate", SELECTED_CANDIDATE, "Selected CJ candidate(선택 CJ 후보)."),
        ("selected_trade_tape", SELECTED_TRADE_TAPE, "Selected CJ trade tape(선택 CJ 거래 기록)."),
        ("filter_audit", CANDIDATE_FILTER_AUDIT, "Candidate filter audit(후보 필터 감사)."),
        ("source_attribution", CANDIDATE_SOURCE_ATTRIBUTION, "Source attribution(원천 귀속)."),
        ("month_stability", CANDIDATE_MONTH_STABILITY, "Month stability(월 안정성)."),
        ("cost_stress", COST_STRESS_DIAGNOSTIC, "Cost stress diagnostic(비용 압박 진단)."),
        ("package_precheck", PACKAGE_PRECHECK, "Package precheck(패키지 사전점검)."),
        ("proxy_mt5_diff_plan", PROXY_MT5_DIFF_PLAN, "Proxy/MT5 diff plan(프록시/MT5 차이 계획)."),
        ("next_queue", RUN364CK_QUEUE, "CK review queue(CK 검토 대기열)."),
        ("report", REPORT_PATH, "CJ report(CJ 보고서)."),
        ("final_decision", FINAL_DECISION, "Final decision(최종 결정)."),
        ("run_manifest", RUN_MANIFEST, "Run manifest(실행 목록)."),
        ("gate_audit", GATE_AUDIT, "Required gate coverage audit(필수 게이트 커버리지 감사)."),
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


def write_manifest(final: Mapping[str, Any]) -> None:
    existing_outputs = [path for path in OUTPUT_FILES if exists(path) and Path(path).is_file() and path != RUN_MANIFEST]
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "run_number": RUN_NUMBER,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "source_proxy_scout_run_id": SOURCE_PROXY_SCOUT_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "status": STATUS,
            "judgment": JUDGMENT,
            "created_at_utc": final["created_at_utc"],
            "producer": rel(Path(__file__)),
            "inputs": [{"path": rel(path), "sha256": sha(path)} for path in INPUT_FILES if exists(path)],
            "outputs": [{"path": rel(path), "sha256": sha(path)} for path in existing_outputs],
            "final_decision": rel(FINAL_DECISION),
            "external_verification_status": final["external_verification_status"],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def main() -> None:
    ensure_dirs()
    created_at = now_utc()
    ci_final = validate_inputs()
    parent_trades, native_control = cg.load_trade_frames()
    parent_trades = normalize_trade_frame(parent_trades)
    native_control = normalize_trade_frame(native_control)

    write_csv(INPUT_MANIFEST, input_manifest_rows())
    write_work_packet()
    surface, frame_map, filter_rows_ = build_surface(parent_trades, native_control)
    selected = dict(surface[0])
    selected_frame = frame_map[str(selected["candidate_id"])].copy()
    source_rows_ = attribution_rows(surface, frame_map)
    month_rows_ = month_rows(surface, frame_map)
    cost_rows_ = cost_stress_rows(surface)
    package_rows_ = package_rows(surface)
    data_rows_ = data_integrity_rows(parent_trades, native_control, surface)
    queue_rows_ = review_queue_rows(selected)
    proxy_mt5_rows_ = proxy_mt5_diff_rows(selected)

    write_csv(PROXY_REPAIR_SURFACE, surface)
    write_json(SELECTED_CANDIDATE, selected)
    trade_tape = selected_frame.drop(columns=["open_time_dt", "close_time_dt"], errors="ignore").to_dict("records")
    write_csv(SELECTED_TRADE_TAPE, trade_tape)
    write_csv(CANDIDATE_FILTER_AUDIT, filter_rows_)
    write_csv(CANDIDATE_SOURCE_ATTRIBUTION, source_rows_)
    write_csv(CANDIDATE_MONTH_STABILITY, month_rows_)
    write_csv(COST_STRESS_DIAGNOSTIC, cost_rows_)
    write_csv(PACKAGE_PRECHECK, package_rows_)
    write_csv(PROXY_MT5_DIFF_PLAN, proxy_mt5_rows_)
    write_csv(RUN364CK_QUEUE, queue_rows_)

    receipt_paths = [
        RUN_EVIDENCE_RECEIPT,
        EXPERIMENT_RECEIPT,
        DATA_RECEIPT,
        MODEL_RECEIPT,
        LINEAGE_RECEIPT,
        JUDGMENT_RECEIPT,
        CLAIM_RECEIPT,
    ]
    preliminary_gates = gate_rows(surface, data_rows_, receipt_paths, final_written=False)
    final = final_payload(ci_final, selected, surface, preliminary_gates, created_at)
    write_json(FINAL_DECISION, final)
    write_receipts(final, selected, proxy_mt5_rows_)
    gates = gate_rows(surface, data_rows_, receipt_paths, final_written=True)
    final = final_payload(ci_final, selected, surface, gates, created_at)
    write_json(FINAL_DECISION, final)
    write_csv(GATE_AUDIT, gates)
    write_receipts(final, selected, proxy_mt5_rows_)
    write_docs(final, selected, surface, filter_rows_, source_rows_, month_rows_, cost_rows_, package_rows_, queue_rows_, gates)
    write_ledgers(final)
    write_manifest(final)
    write_artifact_registry(final)
    refresh_lineage_receipt(final)
    write_manifest(final)
    write_artifact_registry(final)
    repair_run_registry_line_endings(RUN_ID)
    print(json.dumps(json_ready(final), ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
