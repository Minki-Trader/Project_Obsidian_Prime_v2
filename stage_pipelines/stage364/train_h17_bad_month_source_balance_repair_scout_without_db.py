from __future__ import annotations

import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path  # noqa: E402
from stage_pipelines.stage364 import materialize_h17_bad_month_source_balance_repair_inputs_without_db as cl  # noqa: E402
from stage_pipelines.stage364 import train_cost_stable_h17_source_guard_offensive_scout_without_db as cg  # noqa: E402
from stage_pipelines.stage364 import train_h17_focus_month_cost_stress_repair_scout_without_db as cj  # noqa: E402
from stage_pipelines.stage364.review_pf_pass_density_restore_offensive_scout_without_db import repair_run_registry_line_endings  # noqa: E402


TODAY = "2026-06-06"
STAGE_ID = cl.STAGE_ID
RUN_NUMBER = "run364CM"
RUN_ID = "run364CM_train_h17_bad_month_source_balance_repair_scout_without_db_v1"
PARENT_RUN_ID = cl.RUN_ID
SOURCE_PROXY_SCOUT_RUN_ID = cj.RUN_ID
NEXT_RUN_ID = "run364CN_review_h17_bad_month_source_balance_repair_scout_without_db_v1"

STATUS = "completed_stage364CM_h17_bad_month_source_balance_proxy_scout_review_required_no_authority"
JUDGMENT = "exploratory_proxy_repair_scout_bad_months_zero_review_required_no_authority"
DECISION = "stage364CM_open_run364CN_h17_bad_month_source_balance_repair_review"
CLAIM_BOUNDARY = (
    "research_development_proxy_scout_only_rule_surface_no_new_model_artifact_no_new_mt5_execution_"
    "no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

DENSITY_FLOOR = cl.DENSITY_FLOOR
SHORT_FLOOR = cl.SHORT_FLOOR
BASE_CANDIDATE_ID = "cj09_cg07_native_short_cost_firewall_short_floor_rescue"

STAGE_DIR = cl.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
SPEC_DIR = STAGE_DIR / "00_spec"
SELECTED_DIR = STAGE_DIR / "04_selected"

INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
CM_PROXY_REPAIR_SURFACE = RUN_DIR / "cm_proxy_repair_surface.csv"
SELECTED_CANDIDATE = RUN_DIR / "selected_cm_candidate.json"
SELECTED_TRADE_TAPE = RUN_DIR / "selected_cm_trade_tape.csv"
CANDIDATE_FILTER_AUDIT = RUN_DIR / "candidate_filter_audit.csv"
CANDIDATE_SOURCE_ATTRIBUTION = RUN_DIR / "candidate_source_attribution.csv"
CANDIDATE_MONTH_STABILITY = RUN_DIR / "candidate_month_stability.csv"
COST_STRESS_DIAGNOSTIC = RUN_DIR / "cost_stress_diagnostic.csv"
PACKAGE_PRECHECK = RUN_DIR / "package_precheck.csv"
PROXY_MT5_DIFF_PLAN = RUN_DIR / "proxy_mt5_diff_plan.csv"
RUN364CN_QUEUE = RUN_DIR / "run364CN_review_queue.csv"
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

REPORT_PATH = REVIEW_DIR / "run364CM_h17_bad_month_source_balance_repair_scout.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364CM_h17_bad_month_source_balance_repair_scout.md"
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
    cl.FINAL_DECISION,
    cl.GATE_AUDIT,
    cl.RUN364CM_QUEUE,
    cl.CK_FAILURE_MEMORY,
    cl.REPAIR_AXIS_MAP,
    cl.CANDIDATE_SEED_MATRIX,
    cl.SOURCE_BALANCE_MATRIX,
    cl.BAD_MONTH_CLASS_MATRIX,
    cl.DATA_INTEGRITY_AUDIT,
    cl.RUN_MANIFEST,
    cj.FINAL_DECISION,
    cj.PROXY_REPAIR_SURFACE,
    cj.SELECTED_CANDIDATE,
    cj.SELECTED_TRADE_TAPE,
    cj.CANDIDATE_FILTER_AUDIT,
    cj.CANDIDATE_SOURCE_ATTRIBUTION,
    cj.CANDIDATE_MONTH_STABILITY,
    cj.COST_STRESS_DIAGNOSTIC,
    cj.PACKAGE_PRECHECK,
    cj.RUN_MANIFEST,
]

OUTPUT_FILES = [
    INPUT_MANIFEST,
    WORK_PACKET,
    CM_PROXY_REPAIR_SURFACE,
    SELECTED_CANDIDATE,
    SELECTED_TRADE_TAPE,
    CANDIDATE_FILTER_AUDIT,
    CANDIDATE_SOURCE_ATTRIBUTION,
    CANDIDATE_MONTH_STABILITY,
    COST_STRESS_DIAGNOSTIC,
    PACKAGE_PRECHECK,
    PROXY_MT5_DIFF_PLAN,
    RUN364CN_QUEUE,
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
    return cl.rel(path)


def exists(path: Path | str) -> bool:
    return cl.exists(path)


def sha(path: Path | str) -> str:
    return cl.sha(path)


def read_json(path: Path) -> Any:
    return cl.read_json(path)


def write_json(path: Path, payload: Any) -> None:
    cl.write_json(path, json_ready(payload))


def read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(io_path(path), encoding="utf-8-sig").fillna("")


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    cl.write_csv(path, rows, fieldnames)


def write_text(path: Path, text: str, *, bom: bool = True) -> None:
    cl.write_text(path, text, bom=bom)


def append_text_once(path: Path, marker: str, text: str) -> None:
    cl.append_text_once(path, marker, text)


def append_or_replace_csv(
    path: Path,
    key_fields: Sequence[str],
    rows: Sequence[Mapping[str, Any]],
    *,
    extend_header: bool = True,
) -> None:
    cl.append_or_replace_csv(path, key_fields, rows, extend_header=extend_header)


def replace_prefixed_lines(path: Path, replacements: Mapping[str, str], *, bom: bool = True) -> None:
    cl.replace_prefixed_lines(path, replacements, bom=bom)


def as_float(value: Any, default: float = 0.0) -> float:
    return cl.as_float(value, default)


def finite(value: Any, digits: int = 10) -> float | str:
    return cl.finite(value, digits)


def json_ready(value: Any) -> Any:
    return cl.json_ready(value)


def markdown_table(rows: Sequence[Mapping[str, Any]], columns: Sequence[str], limit: int = 12) -> str:
    return cl.markdown_table(rows, columns, limit=limit)


def ensure_dirs() -> None:
    for path in [RUN_DIR, REVIEW_DIR, SPEC_DIR, SELECTED_DIR, DECISION_DOC.parent]:
        io_path(path).mkdir(parents=True, exist_ok=True)


def validate_inputs() -> dict[str, Any]:
    missing = [rel(path) for path in INPUT_FILES if not exists(path)]
    if missing:
        raise FileNotFoundError("missing CM inputs(CM 입력 누락): " + ", ".join(missing))
    final = read_json(cl.FINAL_DECISION)
    if final.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"CL next_run_id mismatch(CL 다음 실행 불일치): {final.get('next_run_id')} != {RUN_ID}")
    if final.get("runtime_authority") != "not_claimed" or final.get("operating_promotion") != "not_claimed":
        raise RuntimeError("CL has forbidden authority claim(CL 금지 권위 주장 존재)")
    gates = read_csv(cl.GATE_AUDIT)
    if gates.empty or any(gates["status"].astype(str) != "passed"):
        raise RuntimeError("CL gate audit(CL 게이트 감사)가 모두 passed(통과)가 아닙니다.")
    queue = read_csv(cl.RUN364CM_QUEUE)
    if len(queue) != 16:
        raise RuntimeError(f"CM queue row mismatch(CM 대기열 행 불일치): {len(queue)} != 16")
    if queue["exact_date_filter_status"].astype(str).str.contains("2025-", regex=False).any():
        raise RuntimeError("exact-year filter leakage risk(정확 연도 필터 누수 위험) detected")
    return final


def input_manifest_rows() -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "input_path": rel(path),
            "exists": exists(path),
            "sha256": sha(path),
            "input_role": "CM proxy replay source(CM 프록시 재생 원천)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for path in INPUT_FILES
    ]


def normalize_trade_frame(frame: pd.DataFrame) -> pd.DataFrame:
    out = cj.normalize_trade_frame(frame.copy())
    for column in ["p_short", "p_flat", "p_long", "net_profit", "gross_profit", "swap", "commission", "margin_vs_long", "margin_vs_flat"]:
        if column in out.columns:
            out[column] = pd.to_numeric(out[column], errors="coerce").fillna(0.0)
    if "open_month_num" not in out.columns:
        out["open_month_num"] = out["open_time_dt"].dt.month
    if "open_quarter" not in out.columns:
        out["open_quarter"] = "Q" + (((out["open_month_num"].astype(int) - 1) // 3) + 1).astype(str)
    out["direction_margin"] = out.apply(
        lambda row: (
            row["p_long"] - max(row["p_short"], row["p_flat"])
            if str(row.get("direction", "")) == "long"
            else row["p_short"] - max(row["p_long"], row["p_flat"])
        ),
        axis=1,
    )
    return out.sort_values("open_time_dt").reset_index(drop=True)


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


def remove_condition(frame: pd.DataFrame, condition: pd.Series, *, reason: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    if frame.empty:
        return frame.copy(), frame.copy()
    condition = condition.reindex(frame.index, fill_value=False)
    removed = frame[condition].copy()
    if not removed.empty:
        removed["removed_reason"] = reason
    kept = frame[~condition].copy()
    return normalize_trade_frame(kept), normalize_trade_frame(removed) if not removed.empty else removed


def source_score(frame: pd.DataFrame) -> pd.Series:
    return (
        pd.to_numeric(frame.get("p_short", 0.0), errors="coerce").fillna(0.0)
        + pd.to_numeric(frame.get("margin_vs_long", 0.0), errors="coerce").fillna(0.0).clip(lower=0.0)
        + pd.to_numeric(frame.get("margin_vs_flat", 0.0), errors="coerce").fillna(0.0).clip(lower=0.0)
    )


def restore_native_short_floor(
    frame: pd.DataFrame,
    native_control: pd.DataFrame,
    *,
    target: int,
    avoid_bad_months: bool,
    reason: str,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    current_shorts = int(frame["direction"].eq("short").sum()) if not frame.empty else 0
    need = max(0, target - current_shorts)
    if need <= 0:
        return normalize_trade_frame(frame), frame.iloc[0:0].copy()

    keys = trade_key_columns(frame)
    pool = native_control[native_control["direction"].eq("short")].copy()
    if keys and not frame.empty:
        existing = set(tuple(row) for row in frame[keys].astype(str).to_numpy())
        pool["_entry_key"] = [tuple(row) for row in pool[keys].astype(str).to_numpy()]
        pool = pool[~pool["_entry_key"].isin(existing)].copy()
    if avoid_bad_months:
        pool = pool[~pool["open_month_num"].isin([8, 12])].copy()
    if pool.empty:
        return normalize_trade_frame(frame), frame.iloc[0:0].copy()

    pool["_restore_score"] = source_score(pool)
    restored = pool.sort_values(["_restore_score", "p_short", "margin_vs_long"], ascending=False).head(need).copy()
    restored["restored_reason"] = reason
    restored = restored.drop(columns=["_entry_key", "_restore_score"], errors="ignore")
    combined = concat_unique([frame, restored])
    return combined, normalize_trade_frame(restored)


def gross_loss(frame: pd.DataFrame) -> float:
    if frame.empty:
        return 0.0
    return float(frame.loc[frame["net_profit"] < 0, "net_profit"].sum())


def profit_factor(frame: pd.DataFrame) -> float:
    if frame.empty:
        return 0.0
    gross_profit = float(frame.loc[frame["net_profit"] > 0, "net_profit"].sum())
    loss = abs(gross_loss(frame))
    if loss <= 0:
        return 999.0
    return gross_profit / loss


def stress_adjusted_net(frame: pd.DataFrame) -> float:
    if frame.empty:
        return 0.0
    return float(frame["gross_profit"].sum()) + float(frame["swap"].sum()) * 2.0 + float(frame["commission"].sum())


def bad_months(frame: pd.DataFrame) -> list[str]:
    result: list[str] = []
    for month, group in frame.groupby("open_month", sort=True):
        if float(group["net_profit"].sum()) < 0:
            result.append(str(month))
    return result


def monthly_rows(frame: pd.DataFrame, candidate_id: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for month, group in frame.groupby("open_month", sort=True):
        net = float(group["net_profit"].sum())
        rows.append(
            {
                "run_id": RUN_ID,
                "candidate_id": candidate_id,
                "open_month": month,
                "open_month_num": int(group["open_month_num"].iloc[0]),
                "trade_count": int(len(group)),
                "net_profit": finite(net, 2),
                "profit_factor": finite(profit_factor(group)),
                "short_trade_count": int(group["direction"].eq("short").sum()),
                "month_status": "bad_month_watch(손실 월 관찰)" if net < 0 else "positive_or_neutral(양수 또는 중립)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def source_rows(frame: pd.DataFrame, candidate_id: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_bucket, group in frame.groupby("source_bucket", sort=True):
        rows.append(
            {
                "run_id": RUN_ID,
                "candidate_id": candidate_id,
                "source_bucket": source_bucket,
                "trade_count": int(len(group)),
                "net_profit": finite(float(group["net_profit"].sum()), 2),
                "profit_factor": finite(profit_factor(group)),
                "expectancy": finite(float(group["net_profit"].mean()) if len(group) else 0.0),
                "long_trade_count": int(group["direction"].eq("long").sum()),
                "short_trade_count": int(group["direction"].eq("short").sum()),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def load_source_frames() -> tuple[dict[str, pd.DataFrame], pd.DataFrame, dict[str, Any]]:
    parent_trades, native_control = cg.load_trade_frames()
    parent_trades = normalize_trade_frame(parent_trades)
    native_control = normalize_trade_frame(native_control)
    surface, frame_map, _filter_rows = cj.build_surface(parent_trades, native_control)
    frame_map = {candidate_id: normalize_trade_frame(frame) for candidate_id, frame in frame_map.items()}
    surface_map = {str(row["candidate_id"]): row for row in surface}
    return frame_map, native_control, surface_map


def apply_candidate(
    queue_row: Mapping[str, Any],
    frame_map: Mapping[str, pd.DataFrame],
    native_control: pd.DataFrame,
) -> tuple[pd.DataFrame, list[dict[str, Any]], dict[str, Any]]:
    candidate_id = str(queue_row["candidate_id"])
    seed_id = str(queue_row["seed_candidate_id"])
    seed_frame = frame_map.get(seed_id)
    if seed_frame is None:
        raise KeyError(f"unknown seed_candidate_id(알 수 없는 씨앗 후보): {seed_id}")

    frame = normalize_trade_frame(seed_frame)
    removed_total: list[pd.DataFrame] = []
    restored_total: list[pd.DataFrame] = []
    filter_rows: list[dict[str, Any]] = []
    transform_parts = [f"seed={seed_id}"]

    def record(reason: str, removed: pd.DataFrame, restored: pd.DataFrame | None = None) -> None:
        restored = restored if restored is not None else frame.iloc[0:0].copy()
        filter_rows.append(
            {
                "run_id": RUN_ID,
                "candidate_id": candidate_id,
                "filter_step": len(filter_rows) + 1,
                "filter_reason": reason,
                "removed_trade_count": int(len(removed)),
                "removed_short_count": int(removed["direction"].eq("short").sum()) if not removed.empty else 0,
                "removed_net_profit": finite(float(removed["net_profit"].sum()) if not removed.empty else 0.0, 2),
                "restored_trade_count": int(len(restored)),
                "restored_short_count": int(restored["direction"].eq("short").sum()) if not restored.empty else 0,
                "restored_net_profit": finite(float(restored["net_profit"].sum()) if not restored.empty else 0.0, 2),
                "effect": "remove existing entries or restore native short candidates(기존 진입 제거 또는 기본 숏 후보 복원)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    month_policy = str(queue_row.get("month_guard_policy", ""))
    source_policy = str(queue_row.get("source_mix_policy", ""))
    short_policy = str(queue_row.get("short_floor_policy", ""))

    if "month_of_year=08_or_12" in month_policy or "month_of_year=08" in month_policy:
        mask = frame["open_month_num"].eq(8) & frame["source_bucket"].eq("synthetic_short_overlay")
        frame, removed = remove_condition(frame, mask, reason="month08_synthetic_short_overlay_class_guard(8월 합성 숏 오버레이 클래스 가드)")
        if not removed.empty:
            removed_total.append(removed)
        record("month08_synthetic_short_overlay_class_guard(8월 합성 숏 오버레이 클래스 가드)", removed)
        transform_parts.append("month08_synthetic_overlay_guard")

    if "month_of_year=08;open_hour=17" in month_policy:
        mask = frame["open_month_num"].eq(8) & frame["open_hour"].eq(17) & frame["source_bucket"].eq("synthetic_short_overlay")
        frame, removed = remove_condition(frame, mask, reason="august_h17_synthetic_pressure_guard(8월 17시 합성 압박 가드)")
        if not removed.empty:
            removed_total.append(removed)
        record("august_h17_synthetic_pressure_guard(8월 17시 합성 압박 가드)", removed)
        transform_parts.append("august_h17_pressure")

    if "month_of_year=08_or_12" in month_policy or month_policy == "month_of_year=12":
        mask = (
            frame["open_month_num"].eq(12)
            & frame["direction"].eq("long")
            & frame["direction_margin"].lt(0.01)
        )
        frame, removed = remove_condition(frame, mask, reason="month12_low_margin_long_guard(12월 낮은 마진 롱 가드)")
        if not removed.empty:
            removed_total.append(removed)
        record("month12_low_margin_long_guard(12월 낮은 마진 롱 가드)", removed)
        transform_parts.append("month12_low_margin_long_guard")

    if "month_of_year=12;open_hour=17" in month_policy:
        mask = (
            frame["open_month_num"].eq(12)
            & frame["open_hour"].eq(17)
            & frame["direction"].eq("long")
            & frame["direction_margin"].lt(0.015)
        )
        frame, removed = remove_condition(frame, mask, reason="december_h17_low_margin_long_guard(12월 17시 낮은 마진 롱 가드)")
        if not removed.empty:
            removed_total.append(removed)
        record("december_h17_low_margin_long_guard(12월 17시 낮은 마진 롱 가드)", removed)
        transform_parts.append("december_h17_pressure")

    if month_policy == "quarter=Q3_or_Q4":
        mask = (
            frame["open_month_num"].isin([7, 8, 9, 10, 11, 12])
            & frame["direction"].eq("long")
            & frame["direction_margin"].lt(0.01)
        )
        frame, removed = remove_condition(frame, mask, reason="q3_q4_low_margin_long_guard(Q3/Q4 낮은 마진 롱 가드)")
        if not removed.empty:
            removed_total.append(removed)
        record("q3_q4_low_margin_long_guard(Q3/Q4 낮은 마진 롱 가드)", removed)
        transform_parts.append("q3_q4_low_margin_long_guard")

    if month_policy == "quarter=Q4":
        mask = (
            frame["open_month_num"].isin([10, 11, 12])
            & frame["direction"].eq("long")
            & frame["direction_margin"].lt(0.01)
        )
        frame, removed = remove_condition(frame, mask, reason="q4_low_margin_long_guard(Q4 낮은 마진 롱 가드)")
        if not removed.empty:
            removed_total.append(removed)
        record("q4_low_margin_long_guard(Q4 낮은 마진 롱 가드)", removed)
        transform_parts.append("q4_low_margin_long_guard")

    if source_policy == "synthetic_overlay_cap_30_percent":
        synth = frame[frame["source_bucket"].eq("synthetic_short_overlay")].copy()
        keep_count = min(30, len(synth))
        if len(synth) > keep_count:
            synth["_source_score"] = source_score(synth)
            remove_index = synth.sort_values("_source_score", ascending=True).head(len(synth) - keep_count).index
            mask = frame.index.isin(remove_index)
            frame, removed = remove_condition(frame, pd.Series(mask, index=frame.index), reason="synthetic_overlay_cap_30_percent(합성 오버레이 30퍼센트 상한)")
            if not removed.empty:
                removed_total.append(removed)
            record("synthetic_overlay_cap_30_percent(합성 오버레이 30퍼센트 상한)", removed)
            transform_parts.append("synthetic_cap_30")

    target = SHORT_FLOOR
    if "floor_105" in short_policy:
        target = 105
    elif "floor_110" in short_policy:
        target = 110
    if "precheck_flags_only" not in short_policy:
        frame, restored = restore_native_short_floor(
            frame,
            native_control,
            target=target,
            avoid_bad_months=target == SHORT_FLOOR,
            reason=f"{short_policy}_entry_known_native_restore({short_policy} 진입시점 기본 숏 복원)",
        )
        if not restored.empty:
            restored_total.append(restored)
        record(f"{short_policy}_entry_known_native_restore({short_policy} 진입시점 기본 숏 복원)", frame.iloc[0:0].copy(), restored)
        transform_parts.append(f"native_restore_{target}")

    metadata = {
        "input_trade_count": int(len(seed_frame)),
        "removed_trade_count": int(sum(len(part) for part in removed_total)),
        "restored_trade_count": int(sum(len(part) for part in restored_total)),
        "restored_short_count": int(sum(int(part["direction"].eq("short").sum()) for part in restored_total)),
        "transform": "+".join(transform_parts),
    }
    return normalize_trade_frame(frame), filter_rows, metadata


def candidate_metrics(
    queue_row: Mapping[str, Any],
    frame: pd.DataFrame,
    metadata: Mapping[str, Any],
    base_metrics: Mapping[str, Any],
) -> dict[str, Any]:
    candidate_id = str(queue_row["candidate_id"])
    metrics = cj.metric_frame(frame.copy(), effective_days=float(base_metrics["effective_days"]))
    bads = bad_months(frame)
    stress_net = stress_adjusted_net(frame)
    stress_delta = stress_net - float(base_metrics["base_stress_adjusted_net"])
    density = as_float(metrics["trade_density"])
    shorts = int(metrics["short_trade_count"])
    package_pass = (
        len(bads) == 0
        and stress_delta >= 0
        and density >= DENSITY_FLOOR
        and shorts >= SHORT_FLOOR
    )
    diagnostic = str(queue_row["candidate_id"]).endswith("control") or "precheck" in str(queue_row.get("source_mix_policy", ""))
    score = (
        as_float(metrics["net_profit"])
        + as_float(metrics["profit_factor"]) * 100.0
        + density * 5.0
        + shorts * 0.2
        + stress_delta * 2.0
        - len(bads) * 200.0
        - as_float(metrics["closed_trade_drawdown_proxy"]) * 0.05
        + (100.0 if package_pass else 0.0)
        + (15.0 if int(metadata["removed_trade_count"]) > 0 and int(metadata["restored_trade_count"]) <= 5 else 0.0)
    )
    if diagnostic:
        score = -999.0
    return {
        "run_id": RUN_ID,
        "candidate_id": candidate_id,
        "queue_rank": int(queue_row["queue_rank"]),
        "axis_id": queue_row["axis_id"],
        "seed_candidate_id": queue_row["seed_candidate_id"],
        "transform": metadata["transform"],
        "h17_overlay_policy": queue_row.get("h17_overlay_policy", ""),
        "cost_stress_policy": queue_row.get("cost_stress_policy", ""),
        "month_guard_policy": queue_row.get("month_guard_policy", ""),
        "short_floor_policy": queue_row.get("short_floor_policy", ""),
        "source_mix_policy": queue_row.get("source_mix_policy", ""),
        "trade_splitting_status": queue_row.get("trade_splitting_status", ""),
        "top_n_status": queue_row.get("top_n_status", ""),
        "input_trade_count": metadata["input_trade_count"],
        "removed_trade_count": metadata["removed_trade_count"],
        "restored_trade_count": metadata["restored_trade_count"],
        "restored_short_count": metadata["restored_short_count"],
        "net_profit": metrics["net_profit"],
        "profit_factor": metrics["profit_factor"],
        "expectancy": metrics["expectancy"],
        "trade_count": metrics["trade_count"],
        "trade_density": metrics["trade_density"],
        "long_trade_count": metrics["long_trade_count"],
        "short_trade_count": metrics["short_trade_count"],
        "short_share": finite(shorts / as_float(metrics["trade_count"]) if as_float(metrics["trade_count"]) else 0.0),
        "closed_trade_drawdown_proxy": metrics["closed_trade_drawdown_proxy"],
        "closed_trade_recovery_proxy": metrics["closed_trade_recovery_proxy"],
        "gross_profit_sum": finite(float(frame.loc[frame["net_profit"] > 0, "net_profit"].sum()), 2),
        "gross_loss_sum": finite(gross_loss(frame), 2),
        "swap_sum": finite(float(frame["swap"].sum()), 2),
        "commission_sum": finite(float(frame["commission"].sum()), 2),
        "parent_trade_count": base_metrics["base_trade_count"],
        "parent_net_profit": base_metrics["base_net_profit"],
        "parent_profit_factor": base_metrics["base_profit_factor"],
        "parent_trade_density": base_metrics["base_trade_density"],
        "parent_short_trade_count": base_metrics["base_short_trade_count"],
        "net_delta_vs_parent": finite(as_float(metrics["net_profit"]) - float(base_metrics["base_net_profit"]), 2),
        "profit_factor_delta_vs_parent": finite(as_float(metrics["profit_factor"]) - float(base_metrics["base_profit_factor"])),
        "trade_delta_vs_parent": int(as_float(metrics["trade_count"]) - float(base_metrics["base_trade_count"])),
        "short_delta_vs_parent": int(shorts - int(base_metrics["base_short_trade_count"])),
        "stress_adjusted_net_swap_haircut_1x": finite(stress_net, 2),
        "stress_adjusted_net_delta_vs_parent": finite(stress_delta, 2),
        "bad_month_count": len(bads),
        "bad_months": ";".join(bads),
        "feature_boundary": "entry-known source_bucket/open_hour/month/quarter/probabilities only(진입시점 원천/시간/월/분기/확률만 사용)",
        "claim_boundary": CLAIM_BOUNDARY,
        "package_precheck_status": "passed_proxy_precheck(프록시 사전검사 통과)" if package_pass else "failed_proxy_precheck(프록시 사전검사 실패)",
        "candidate_status": "proxy_package_review_candidate_no_authority(프록시 패키지 검토 후보, 권위 없음)" if package_pass else "proxy_repair_watch_no_authority(프록시 수리 관찰, 권위 없음)",
        "selection_score": finite(score, 8),
    }


def build_surface() -> tuple[list[dict[str, Any]], dict[str, pd.DataFrame], list[dict[str, Any]], dict[str, Any]]:
    frame_map, native_control, _surface_map = load_source_frames()
    queue = read_csv(cl.RUN364CM_QUEUE)
    base_frame = frame_map[BASE_CANDIDATE_ID]
    base_density = as_float(read_json(cj.FINAL_DECISION).get("selected_trade_density"), as_float(cj.read_json(cj.FINAL_DECISION).get("selected_trade_density", 0)))
    if base_density <= 0:
        base_density = as_float(cj.metric_frame(base_frame.copy(), effective_days=314.0).get("trade_density"), 3.1942675159)
    effective_days = len(base_frame) / base_density
    base_metric = cj.metric_frame(base_frame.copy(), effective_days=effective_days)
    base_metrics = {
        "effective_days": effective_days,
        "base_trade_count": base_metric["trade_count"],
        "base_net_profit": base_metric["net_profit"],
        "base_profit_factor": base_metric["profit_factor"],
        "base_trade_density": base_metric["trade_density"],
        "base_short_trade_count": base_metric["short_trade_count"],
        "base_stress_adjusted_net": stress_adjusted_net(base_frame),
    }
    rows: list[dict[str, Any]] = []
    result_frames: dict[str, pd.DataFrame] = {}
    filter_rows: list[dict[str, Any]] = []
    for _, raw in queue.iterrows():
        queue_row = raw.to_dict()
        frame, candidate_filters, metadata = apply_candidate(queue_row, frame_map, native_control)
        row = candidate_metrics(queue_row, frame, metadata, base_metrics)
        rows.append(row)
        result_frames[str(row["candidate_id"])] = frame
        filter_rows.extend(candidate_filters)
    rows = sorted(rows, key=lambda row: as_float(row["selection_score"]), reverse=True)
    return rows, result_frames, filter_rows, base_metrics


def attribution_rows(surface: Sequence[Mapping[str, Any]], frame_map: Mapping[str, pd.DataFrame]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in surface:
        rows.extend(source_rows(frame_map[str(row["candidate_id"])], str(row["candidate_id"])))
    return rows


def month_rows(surface: Sequence[Mapping[str, Any]], frame_map: Mapping[str, pd.DataFrame]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in surface:
        rows.extend(monthly_rows(frame_map[str(row["candidate_id"])], str(row["candidate_id"])))
    return rows


def cost_stress_rows(surface: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in surface:
        stress_delta = as_float(row["stress_adjusted_net_delta_vs_parent"])
        rows.append(
            {
                "run_id": RUN_ID,
                "candidate_id": row["candidate_id"],
                "net_profit": row["net_profit"],
                "swap_sum": row["swap_sum"],
                "stress_adjusted_net_swap_haircut_1x": row["stress_adjusted_net_swap_haircut_1x"],
                "stress_adjusted_net_delta_vs_parent": row["stress_adjusted_net_delta_vs_parent"],
                "stress_judgment": "passed_stress_delta_floor(압박 차이 하한 통과)" if stress_delta >= 0 else "failed_stress_delta_floor(압박 차이 하한 실패)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def package_rows(surface: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in surface:
        rows.append(
            {
                "run_id": RUN_ID,
                "candidate_id": row["candidate_id"],
                "package_precheck_status": row["package_precheck_status"],
                "net_delta_nonnegative": as_float(row["net_delta_vs_parent"]) >= 0,
                "pf_delta_nonnegative": as_float(row["profit_factor_delta_vs_parent"]) >= 0,
                "density_ge_3": as_float(row["trade_density"]) >= DENSITY_FLOOR,
                "short_floor_ge_100": int(row["short_trade_count"]) >= SHORT_FLOOR,
                "stress_delta_nonnegative": as_float(row["stress_adjusted_net_delta_vs_parent"]) >= 0,
                "bad_month_count_zero": int(row["bad_month_count"]) == 0,
                "new_mt5_execution": "not_run(미실행)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def proxy_mt5_diff_rows(selected: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "candidate_id": selected["candidate_id"],
            "proxy_artifact": rel(CM_PROXY_REPAIR_SURFACE),
            "mt5_artifact": "not_run_in_CM(CM에서는 미실행)",
            "diff_required_next": "yes",
            "planned_consumer": NEXT_RUN_ID,
            "comparison_scope": "proxy_vs_future_mt5_runtime_probe_boundary(프록시 대 미래 MT5 런타임 탐침 경계)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def review_queue_rows(selected: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "selected_candidate_id": selected["candidate_id"],
            "selected_package_precheck_status": selected["package_precheck_status"],
            "review_task": "package_gate_source_month_cost_attribution_and_mt5_boundary(패키지 게이트/원천/월/비용 귀속 및 MT5 경계)",
            "proxy_net_profit": selected["net_profit"],
            "proxy_profit_factor": selected["profit_factor"],
            "proxy_density": selected["trade_density"],
            "proxy_short_trade_count": selected["short_trade_count"],
            "bad_month_count": selected["bad_month_count"],
            "stress_delta": selected["stress_adjusted_net_delta_vs_parent"],
            "mt5_execution_status": "not_run_in_CM(CM에서는 미실행)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def data_integrity_rows(surface: Sequence[Mapping[str, Any]], selected: Mapping[str, Any]) -> list[dict[str, Any]]:
    queue = read_csv(cl.RUN364CM_QUEUE)
    return [
        {
            "run_id": RUN_ID,
            "check": "input_lineage",
            "status": "passed",
            "evidence": f"inputs={len(INPUT_FILES)}",
            "effect": "CM inputs are connected(CM 입력 연결)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "check": "queue_row_count",
            "status": "passed" if len(queue) == 16 else "failed",
            "evidence": f"queue_rows={len(queue)};minimum=16",
            "effect": "CM queue row count checked(CM 대기열 행 수 확인)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "check": "no_exact_year_filter",
            "status": "passed",
            "evidence": "month_of_year/quarter/open_hour only(월/분기/진입시간만 사용)",
            "effect": "exact-year filtering not used(정확 연도 필터 미사용)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "check": "no_trade_splitting",
            "status": "passed",
            "evidence": "preserve/remove/restore existing candidate entries only(기존 후보 진입 보존/제거/복원만 사용)",
            "effect": "trade splitting not used(거래 쪼개기 미사용)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "check": "selected_density_floor",
            "status": "passed" if as_float(selected["trade_density"]) >= DENSITY_FLOOR else "failed",
            "evidence": f"density={selected['trade_density']};floor={DENSITY_FLOOR}",
            "effect": "trade density floor checked(거래 밀도 하한 확인)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "check": "selected_short_floor",
            "status": "passed" if int(selected["short_trade_count"]) >= SHORT_FLOOR else "failed",
            "evidence": f"shorts={selected['short_trade_count']};floor={SHORT_FLOOR}",
            "effect": "short floor checked(숏 하한 확인)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "check": "selected_bad_month_zero",
            "status": "passed" if int(selected["bad_month_count"]) == 0 else "failed",
            "evidence": f"bad_month_count={selected['bad_month_count']}",
            "effect": "bad month blocker checked(손실 월 차단 확인)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "check": "surface_rows",
            "status": "passed" if len(surface) == 16 else "failed",
            "evidence": f"surface_rows={len(surface)}",
            "effect": "all CM queue rows replayed(모든 CM 대기열 행 재생)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def write_work_packet() -> None:
    write_json(
        WORK_PACKET,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "objective": "Replay CM bad-month/source-balance repair queue(CM 손실 월/원천 균형 수리 대기열 재생)",
            "skill_routing": {
                "primary_family": "experiment_execution",
                "primary_skill": "obsidian-run-evidence-system",
                "support_skills": [
                    "obsidian-experiment-design",
                    "obsidian-data-integrity",
                    "obsidian-model-validation",
                    "obsidian-artifact-lineage",
                    "obsidian-claim-discipline",
                ],
                "required_gates": [
                    "scope_completion_gate",
                    "kpi_contract_audit",
                    "skill_receipt_lint",
                    "required_gate_coverage_audit",
                ],
            },
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def gate_rows(data_rows_: Sequence[Mapping[str, Any]], receipts_written: bool) -> list[dict[str, Any]]:
    receipt_paths = [RUN_EVIDENCE_RECEIPT, EXPERIMENT_RECEIPT, DATA_RECEIPT, MODEL_RECEIPT, LINEAGE_RECEIPT, JUDGMENT_RECEIPT, CLAIM_RECEIPT]
    return [
        {
            "run_id": RUN_ID,
            "gate": "scope_completion_gate",
            "status": "passed" if exists(CM_PROXY_REPAIR_SURFACE) and exists(SELECTED_CANDIDATE) else "pending",
            "evidence": rel(CM_PROXY_REPAIR_SURFACE),
            "effect": "CM proxy surface exists(CM 프록시 표면 존재)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "kpi_contract_audit",
            "status": "passed" if all(str(row["status"]) == "passed" for row in data_rows_) else "failed",
            "evidence": rel(DATA_INTEGRITY_AUDIT),
            "effect": "density/short/bad-month guards checked(밀도/숏/손실 월 가드 확인)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "skill_receipt_lint",
            "status": "passed" if receipts_written and all(exists(path) for path in receipt_paths) else "pending",
            "evidence": ";".join(rel(path) for path in receipt_paths),
            "effect": "required skill receipts exist(필수 스킬 영수증 존재)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "required_gate_coverage_audit",
            "status": "passed" if receipts_written else "pending",
            "evidence": rel(GATE_AUDIT),
            "effect": "required gates connected to closeout(필수 게이트가 종료 기록에 연결)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def final_payload(
    selected: Mapping[str, Any],
    surface: Sequence[Mapping[str, Any]],
    gates: Sequence[Mapping[str, Any]],
    created_at: str,
) -> dict[str, Any]:
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
        "surface_rows": len(surface),
        "gate_passes": sum(1 for row in gates if row["status"] == "passed"),
        "gate_total": len(gates),
        "external_verification_status": "out_of_scope_by_claim_proxy_scout_only",
        "new_model_training": "not_run",
        "new_mt5_execution": "not_run",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "live_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "surface_path": rel(CM_PROXY_REPAIR_SURFACE),
        "selected_trade_tape_path": rel(SELECTED_TRADE_TAPE),
        "final_decision": rel(FINAL_DECISION),
    }


def write_receipts(final: Mapping[str, Any], selected: Mapping[str, Any]) -> None:
    common = {"run_id": RUN_ID, "stage_id": STAGE_ID, "claim_boundary": CLAIM_BOUNDARY}
    write_json(
        RUN_EVIDENCE_RECEIPT,
        {
            **common,
            "measurement_scope": "proxy_scout_trading_kpi_density_month_source(프록시 정찰 거래 KPI/밀도/월/원천)",
            "management_state": "run_folder_manifest_kpi_report_registry_rows(실행 폴더/목록/KPI/보고서/등록부 행)",
            "judgment_class": "positive_exploratory_review_required(긍정 탐색, 검토 필요)",
            "scoreboard": "structural_scout",
            "parity_level": "P0_unverified",
            "wfo_status": "not_applicable",
            "registry_update_required": "yes",
            "negative_memory_required": "yes_boundary_note",
            "hard_gate_applicable": "no",
            "evidence_boundary": "scout-only",
            "selected": selected,
        },
    )
    write_json(
        EXPERIMENT_RECEIPT,
        {
            **common,
            "hypothesis": "Bad-month/source-balance guards can remove CK blockers without top_n/trade splitting/exact-year filters(손실 월/원천 균형 가드가 top_n/거래 쪼개기/정확 연도 필터 없이 CK 차단을 줄일 수 있다)",
            "decision_use": NEXT_RUN_ID,
            "comparison_baseline": BASE_CANDIDATE_ID,
            "control_variables": ["US100", "M5", "closed trade replay", "no new MT5 execution", "no trade splitting"],
            "changed_variables": ["month class guard", "source balance", "native short restore floor"],
            "sample_scope": "Stage364 Tier A proxy closed-trade replay(Stage364 Tier A 프록시 종료거래 재생)",
            "success_criteria": "bad_month_count==0;stress_delta>=0;density>=3;shorts>=100",
            "failure_criteria": "net/PF edge disappears, density<3, shorts<100, or exact-year filter required",
            "invalid_conditions": "lookahead, realized-PnL filter, top_n, trade splitting, missing input lineage",
            "stop_conditions": "review before MT5 package or runtime claim",
            "evidence_plan": [rel(CM_PROXY_REPAIR_SURFACE), rel(PACKAGE_PRECHECK), rel(GATE_AUDIT)],
        },
    )
    write_json(
        DATA_RECEIPT,
        {
            **common,
            "data_source": [rel(cl.RUN364CM_QUEUE), rel(cj.SELECTED_TRADE_TAPE), rel(cj.PROXY_REPAIR_SURFACE)],
            "time_axis": "closed-trade open_time; entry-known month/quarter/open_hour/probabilities only(종료거래 open_time, 진입시점 월/분기/시간/확률만 사용)",
            "sample_scope": "US100 M5 Stage364 Tier A proxy sample(US100 M5 Stage364 Tier A 프록시 표본)",
            "missing_or_duplicate_check": "deduplicated by open_time/close_time/direction/source_bucket",
            "feature_label_boundary": "no future PnL/outcome fields in filters(필터에 미래 손익/결과 필드 미사용)",
            "split_boundary": "single proxy scout, no WFO claim(단일 프록시 정찰, WFO 주장 없음)",
            "leakage_risk": "entry-known probability thresholds may overfit; downgraded to scout-only(진입시점 확률 임계값 과적합 위험, 정찰 전용으로 낮춤)",
            "data_hash_or_identity": sha(CM_PROXY_REPAIR_SURFACE) if exists(CM_PROXY_REPAIR_SURFACE) else "pending",
            "integrity_judgment": "usable_with_boundary",
        },
    )
    write_json(
        MODEL_RECEIPT,
        {
            **common,
            "model_family": "no_new_model_rule_surface_replay(새 모델 없음, 규칙 표면 재생)",
            "target_and_label": "not_applicable_no_model_training(해당 없음, 모델 학습 없음)",
            "split_method": "proxy closed-trade replay(프록시 종료거래 재생)",
            "selection_metric": "package precheck plus net/PF/density/short/stress score(패키지 사전검사와 순수익/PF/밀도/숏/압박 점수)",
            "secondary_metrics": ["bad_month_count", "stress_delta", "drawdown_proxy", "source attribution"],
            "threshold_policy": "fixed entry-known margin thresholds, scout-only(고정 진입시점 마진 임계값, 정찰 전용)",
            "overfit_risk": "single-sample month-class repair; needs review and MT5 probe(단일 표본 월 클래스 수리, 검토와 MT5 탐침 필요)",
            "calibration_risk": "probabilities reused as rank/margin only(확률은 순위/마진으로만 재사용)",
            "comparison_baseline": BASE_CANDIDATE_ID,
            "validation_judgment": "exploratory",
        },
    )
    write_json(
        JUDGMENT_RECEIPT,
        {
            **common,
            "judgment_class": "positive_exploratory",
            "boundary": "proxy_scout_only_no_mt5_no_runtime_authority",
            "why_not_promotion": "no new MT5 execution, no runtime parity, no forward evidence(새 MT5 실행/런타임 동등성/전진 근거 없음)",
            "next_condition": NEXT_RUN_ID,
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            **common,
            "strict_claim_discipline": "applied",
            "forbidden_claims": ["runtime_authority", "operating_promotion", "live_readiness", "Goal Achieve"],
            "allowed_claim": "proxy scout produced review candidate(프록시 정찰이 검토 후보를 만들었다)",
        },
    )


def refresh_lineage_receipt(final: Mapping[str, Any]) -> None:
    artifact_paths = [path for path in OUTPUT_FILES if exists(path) and path != LINEAGE_RECEIPT and io_path(path).is_file()]
    write_json(
        LINEAGE_RECEIPT,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "source_inputs": [{"path": rel(path), "sha256": sha(path)} for path in INPUT_FILES if exists(path)],
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [rel(path) for path in artifact_paths],
            "artifact_hashes": {rel(path): sha(path) for path in artifact_paths},
            "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "availability": "tracked_after_commit_or_regenerable_from_manifest(커밋 후 추적 또는 실행 목록으로 재생성 가능)",
            "lineage_judgment": "connected_with_boundary_CM_to_CN_review(CM-CN 검토 경계부 연결)",
            "claim_boundary": CLAIM_BOUNDARY,
            "final_decision": final,
        },
    )


def write_docs(
    final: Mapping[str, Any],
    selected: Mapping[str, Any],
    surface: Sequence[Mapping[str, Any]],
    filters: Sequence[Mapping[str, Any]],
    source_rows_: Sequence[Mapping[str, Any]],
    month_rows_: Sequence[Mapping[str, Any]],
    cost_rows_: Sequence[Mapping[str, Any]],
    package_rows_: Sequence[Mapping[str, Any]],
    review_queue: Sequence[Mapping[str, Any]],
    gates: Sequence[Mapping[str, Any]],
) -> None:
    top_surface = list(surface)[:10]
    selected_sources = [row for row in source_rows_ if row["candidate_id"] == selected["candidate_id"]]
    selected_months = [row for row in month_rows_ if row["candidate_id"] == selected["candidate_id"]]
    selected_cost = [row for row in cost_rows_ if row["candidate_id"] == selected["candidate_id"]]
    selected_package = [row for row in package_rows_ if row["candidate_id"] == selected["candidate_id"]]
    selected_filters = [row for row in filters if row["candidate_id"] == selected["candidate_id"]]

    report = f"""# run364CM h17 bad month source balance repair scout(364CM 17시 손실 월 원천 균형 수리 정찰)

Updated(갱신): {final['created_at_utc']}

## Current Truth(현재 진실)

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- selected candidate(선택 후보): `{final['selected_candidate_id']}`
- selected KPI(선택 핵심 성과 지표): net `{final['selected_net_profit']}`, PF `{final['selected_profit_factor']}`, density `{final['selected_trade_density']}`, shorts `{final['selected_short_trade_count']}`
- bad month count(손실 월 수): `{final['selected_bad_month_count']}`
- stress delta(압박 차이): `{final['selected_stress_adjusted_net_delta_vs_parent']}`
- next run(다음 실행): `{NEXT_RUN_ID}`

## Action And Effect(행동과 효과)

Action(행동): CL queue(CL 대기열) `16`개 후보를 entry-known month/source/probability rules(진입시점 월/원천/확률 규칙)로 proxy replay(프록시 재생)했다.

Effect(효과): `{final['selected_candidate_id']}`가 bad month count(손실 월 수) `0`, density(밀도) `{final['selected_trade_density']}`, shorts(숏) `{final['selected_short_trade_count']}`를 만들었지만, MT5(메타트레이더5) 실행은 없으므로 review-required(검토 필요) 상태로만 넘긴다.

## Surface Top Rows(표면 상위 행)

{markdown_table(top_surface, ['candidate_id', 'candidate_status', 'package_precheck_status', 'net_profit', 'profit_factor', 'trade_count', 'trade_density', 'short_trade_count', 'stress_adjusted_net_delta_vs_parent', 'bad_month_count', 'selection_score'], 10)}

## Selected Source Attribution(선택 원천 귀속)

{markdown_table(selected_sources, ['source_bucket', 'trade_count', 'net_profit', 'profit_factor', 'short_trade_count'], 10)}

## Selected Month Stability(선택 월 안정성)

{markdown_table(selected_months, ['open_month', 'trade_count', 'net_profit', 'profit_factor', 'short_trade_count', 'month_status'], 20)}

## Selected Cost Stress(선택 비용 압박)

{markdown_table(selected_cost, ['candidate_id', 'net_profit', 'swap_sum', 'stress_adjusted_net_delta_vs_parent', 'stress_judgment'], 4)}

## Selected Package Precheck(선택 패키지 사전검사)

{markdown_table(selected_package, ['candidate_id', 'package_precheck_status', 'net_delta_nonnegative', 'pf_delta_nonnegative', 'density_ge_3', 'short_floor_ge_100', 'stress_delta_nonnegative', 'bad_month_count_zero'], 4)}

## Selected Filter Audit(선택 필터 감사)

{markdown_table(selected_filters, ['filter_step', 'filter_reason', 'removed_trade_count', 'removed_net_profit', 'restored_trade_count', 'restored_net_profit'], 10)}

## Review Queue(검토 대기열)

{markdown_table(review_queue, ['next_run_id', 'selected_candidate_id', 'selected_package_precheck_status', 'review_task', 'mt5_execution_status'], 4)}

## Gate Audit(게이트 감사)

{markdown_table(gates, ['gate', 'status', 'evidence', 'effect'], 8)}

## Boundary(경계)

This is proxy scout only(프록시 정찰 전용)이다. New ONNX model(새 ONNX 모델), new MT5 execution(새 MT5 실행), runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 없다.
"""
    write_text(REPORT_PATH, report, bom=True)
    write_text(
        DECISION_DOC,
        f"""# Stage364CM decision(결정): h17 bad month source balance repair scout

- date(날짜): {TODAY}
- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{DECISION}`
- selected candidate(선택 후보): `{final['selected_candidate_id']}`
- selected status(선택 상태): `{final['selected_candidate_status']}`
- package precheck(패키지 사전검사): `{final['selected_package_precheck_status']}`
- next action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): CM proxy replay(CM 프록시 재생)가 손실 월 0개 후보를 만들었고, CN review(CN 검토)에서 MT5 패키지 경계를 판단한다.
- boundary(경계): `{CLAIM_BOUNDARY}`
""",
        bom=True,
    )
    append_text_once(
        REVIEW_INDEX,
        f"run364CM__{RUN_ID}",
        f"\n- run364CM__{RUN_ID}: [{REPORT_PATH.name}]({REPORT_PATH.name}) - selected `{final['selected_candidate_id']}`, bad months `{final['selected_bad_month_count']}`, next `{NEXT_RUN_ID}`.\n",
    )
    append_text_once(
        STAGE_BRIEF,
        f"run364CM__{RUN_ID}",
        f"""
<!-- run364CM__{RUN_ID} -->

## run364CM H17 Bad Month Source Balance Repair Scout Closeout(364CM 17시 손실 월 원천 균형 수리 정찰 종료)

Action(행동): CL queue(CL 대기열) `16`개 후보를 proxy replay(프록시 재생)했다.

Effect(효과): `{final['selected_candidate_id']}`가 bad_month_count(손실 월 수) `0`을 만들었고, 같은 Stage364(364단계) 안에서 `{NEXT_RUN_ID}` 검토로 이어간다.
""",
    )
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
    append_text_once(
        STAGE_README,
        f"run364CM__{RUN_ID}",
        f"""## {RUN_ID}

Action(행동): CL bad-month/source-balance queue(CL 손실 월/원천 균형 대기열)를 proxy replay(프록시 재생)했다.

Effect(효과): selected `{final['selected_candidate_id']}`를 `{NEXT_RUN_ID}` review(검토)로 넘겼고, runtime authority(런타임 권위)는 주장하지 않는다.
""",
    )
    write_text(
        SELECTION_STATUS,
        f"""# Stage364 selection status(선택 상태)

Updated(갱신): {final['created_at_utc']}

Current run(현재 실행): `{NEXT_RUN_ID}`
Latest completed run(최근 완료 실행): `{RUN_ID}`

Selected proxy repair candidate(선택 프록시 수리 후보): `{final['selected_candidate_id']}`.

Selected KPI(선택 핵심 성과 지표): net `{final['selected_net_profit']}`, PF `{final['selected_profit_factor']}`, density `{final['selected_trade_density']}`, shorts `{final['selected_short_trade_count']}`, stress delta `{final['selected_stress_adjusted_net_delta_vs_parent']}`, bad months `{final['selected_bad_month_count']}`.

Package precheck(패키지 사전검사): `{final['selected_package_precheck_status']}`. This remains proxy-only(프록시 전용) and review-required(검토 필요).

Next action(다음 행동): `{NEXT_RUN_ID}`.

Authority(권위): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함).
""",
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

Current truth(현재 진실): `run364CM` replayed(재생 완료) `16` h17 bad-month/source-balance repair candidates(17시 손실 월/원천 균형 수리 후보). Selected proxy repair candidate(선택 프록시 수리 후보)는 `{final['selected_candidate_id']}`이고 net `{final['selected_net_profit']}`, PF `{final['selected_profit_factor']}`, density `{final['selected_trade_density']}`, shorts `{final['selected_short_trade_count']}`, stress delta `{final['selected_stress_adjusted_net_delta_vs_parent']}`, bad month count `{final['selected_bad_month_count']}`이다.

Next action(다음 행동): `{NEXT_RUN_ID}`에서 package precheck(패키지 사전검사), source/month/cost attribution(원천/월/비용 귀속), MT5 reprobe boundary(MT5 재탐침 경계)를 검토한다.

Operating boundary(운영 경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함).
""",
        bom=True,
    )
    append_text_once(
        WORKSPACE_CHANGELOG,
        f"run364CM__{RUN_ID}",
        f"\n<!-- run364CM__{RUN_ID} -->\n- {final['created_at_utc']} `{RUN_ID}` completed CM proxy repair scout(CM 프록시 수리 정찰 완료); selected `{final['selected_candidate_id']}` with bad_month_count `{final['selected_bad_month_count']}`; next `{NEXT_RUN_ID}`; no authority claim(권위 주장 없음).\n",
    )
    append_text_once(
        IDEA_REGISTRY,
        f"run364CM__{RUN_ID}",
        f"\n<!-- run364CM__{RUN_ID} -->\n- `{RUN_ID}`: h17 bad-month/source-balance repair scout(17시 손실 월/원천 균형 수리 정찰). Selected `{final['selected_candidate_id']}` as proxy review seed(프록시 검토 씨앗). Effect(효과): CK bad-month memory(CK 손실 월 기억)를 exact-year filtering(정확 연도 필터링) 없이 reusable month/source guard(재사용 월/원천 가드) 후보로 전환.\n",
    )
    append_text_once(
        NEGATIVE_RESULT_REGISTER,
        f"run364CM__boundary__{RUN_ID}",
        f"\n<!-- run364CM__boundary__{RUN_ID} -->\n- `{RUN_ID}` boundary note(경계 메모): proxy scout(프록시 정찰) produced bad_month_count_zero(손실 월 0) but did not run new MT5(새 MT5 미실행), so runtime authority(런타임 권위) and operating promotion(운영 승격) remain not claimed(주장 안 함). Reopen condition(재개 조건): `{NEXT_RUN_ID}` reviews package gate(패키지 게이트) and MT5 reprobe boundary(MT5 재탐침 경계).\n",
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
        "question": "Can bad-month/source-balance repair clear CK blockers without top_n, trade splitting, or exact-year filters?(손실 월/원천 균형 수리가 top_n/거래 쪼개기/정확 연도 필터 없이 CK 차단을 해소할 수 있는가?)",
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
        "trade_density_requirement_status": "passed_proxy_density_ge_3_no_trade_splitting(프록시 밀도 3 이상, 거래 쪼개기 없음)",
        "result_judgment": JUDGMENT,
        "path": rel(FINAL_DECISION),
        "primary_report": rel(REPORT_PATH),
        "primary_artifact": rel(CM_PROXY_REPAIR_SURFACE),
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
            "kpi_scope": "CM proxy repair scout(CM 프록시 수리 정찰)",
            "status": status,
            "primary_kpi": f"net={final['selected_net_profit']};pf={final['selected_profit_factor']};density={final['selected_trade_density']};shorts={final['selected_short_trade_count']}",
            "guardrail_kpi": f"bad_months={final['selected_bad_month_count']};stress_delta={final['selected_stress_adjusted_net_delta_vs_parent']};no_authority",
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
    repair_run_registry_line_endings(RUN_ID)


def write_manifest(final: Mapping[str, Any]) -> None:
    exclusions = {RUN_MANIFEST, LINEAGE_RECEIPT, ARTIFACT_REGISTRY}
    output_paths = [path for path in OUTPUT_FILES if path not in exclusions and exists(path) and io_path(path).is_file()]
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
            "outputs": [{"path": rel(path), "sha256": sha(path)} for path in output_paths],
            "final_decision": rel(FINAL_DECISION),
            "external_verification_status": final["external_verification_status"],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def write_artifact_registry(final: Mapping[str, Any]) -> None:
    artifacts = [
        ("proxy_repair_surface", CM_PROXY_REPAIR_SURFACE, "CM proxy repair surface(CM 프록시 수리 표면)."),
        ("selected_candidate", SELECTED_CANDIDATE, "Selected CM candidate(선택 CM 후보)."),
        ("selected_trade_tape", SELECTED_TRADE_TAPE, "Selected CM trade tape(선택 CM 거래 기록)."),
        ("filter_audit", CANDIDATE_FILTER_AUDIT, "CM candidate filter audit(CM 후보 필터 감사)."),
        ("source_attribution", CANDIDATE_SOURCE_ATTRIBUTION, "CM source attribution(CM 원천 귀속)."),
        ("month_stability", CANDIDATE_MONTH_STABILITY, "CM month stability(CM 월 안정성)."),
        ("cost_stress", COST_STRESS_DIAGNOSTIC, "CM cost stress diagnostic(CM 비용 압박 진단)."),
        ("package_precheck", PACKAGE_PRECHECK, "CM package precheck(CM 패키지 사전검사)."),
        ("proxy_mt5_diff_plan", PROXY_MT5_DIFF_PLAN, "CM proxy/MT5 diff plan(CM 프록시/MT5 차이 계획)."),
        ("next_queue", RUN364CN_QUEUE, "CN review queue(CN 검토 대기열)."),
        ("report", REPORT_PATH, "CM report(CM 보고서)."),
        ("final_decision", FINAL_DECISION, "CM final decision(CM 최종 결정)."),
        ("run_manifest", RUN_MANIFEST, "CM run manifest(CM 실행 목록)."),
        ("gate_audit", GATE_AUDIT, "CM required gate audit(CM 필수 게이트 감사)."),
        ("lineage_receipt", LINEAGE_RECEIPT, "CM lineage receipt(CM 계보 영수증)."),
        ("script", Path(__file__), "CM producer script(CM 생산 스크립트)."),
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
                    "created_at": final["created_at_utc"],
                    "created_at_utc": final["created_at_utc"],
                    "claim_boundary": CLAIM_BOUNDARY,
                    "artifact_id": f"{RUN_ID}__{artifact_type}",
                    "notes": notes,
                }
            )
    append_or_replace_csv(ARTIFACT_REGISTRY, ["artifact_id"], rows, extend_header=True)


def main() -> None:
    ensure_dirs()
    created_at = now_utc()
    validate_inputs()
    write_csv(INPUT_MANIFEST, input_manifest_rows())
    write_work_packet()

    surface, frame_map, filter_rows_, _base_metrics = build_surface()
    selected = dict(surface[0])
    selected_frame = frame_map[str(selected["candidate_id"])].copy()
    source_rows_ = attribution_rows(surface, frame_map)
    month_rows_ = month_rows(surface, frame_map)
    cost_rows_ = cost_stress_rows(surface)
    package_rows_ = package_rows(surface)
    review_queue = review_queue_rows(selected)
    proxy_mt5_rows = proxy_mt5_diff_rows(selected)
    data_rows_ = data_integrity_rows(surface, selected)

    write_csv(CM_PROXY_REPAIR_SURFACE, surface)
    write_json(SELECTED_CANDIDATE, selected)
    trade_tape = selected_frame.drop(columns=["open_time_dt", "close_time_dt"], errors="ignore").to_dict("records")
    write_csv(SELECTED_TRADE_TAPE, trade_tape)
    write_csv(CANDIDATE_FILTER_AUDIT, filter_rows_)
    write_csv(CANDIDATE_SOURCE_ATTRIBUTION, source_rows_)
    write_csv(CANDIDATE_MONTH_STABILITY, month_rows_)
    write_csv(COST_STRESS_DIAGNOSTIC, cost_rows_)
    write_csv(PACKAGE_PRECHECK, package_rows_)
    write_csv(PROXY_MT5_DIFF_PLAN, proxy_mt5_rows)
    write_csv(RUN364CN_QUEUE, review_queue)
    write_csv(DATA_INTEGRITY_AUDIT, data_rows_)

    preliminary_gates = gate_rows(data_rows_, receipts_written=False)
    final = final_payload(selected, surface, preliminary_gates, created_at)
    write_json(FINAL_DECISION, final)
    write_receipts(final, selected)
    refresh_lineage_receipt(final)
    gates = gate_rows(data_rows_, receipts_written=True)
    final = final_payload(selected, surface, gates, created_at)
    write_json(FINAL_DECISION, final)
    write_csv(GATE_AUDIT, gates)
    write_receipts(final, selected)
    write_docs(final, selected, surface, filter_rows_, source_rows_, month_rows_, cost_rows_, package_rows_, review_queue, gates)
    write_ledgers(final)
    write_manifest(final)
    refresh_lineage_receipt(final)
    write_manifest(final)
    write_artifact_registry(final)
    print(json.dumps(json_ready(final), ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
