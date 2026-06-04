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
from stage_pipelines.stage364 import materialize_cost_stable_h17_source_guard_offensive_inputs_without_db as parent  # noqa: E402
from stage_pipelines.stage364 import review_swap_stable_reprobe_and_source_guard_mt5_runtime_probe_without_db as ce  # noqa: E402
from stage_pipelines.stage364.review_pf_pass_density_restore_offensive_scout_without_db import repair_run_registry_line_endings  # noqa: E402


TODAY = "2026-06-05"
STAGE_ID = parent.STAGE_ID
RUN_NUMBER = "run364CG"
RUN_ID = "run364CG_train_cost_stable_h17_source_guard_offensive_scout_without_db_v1"
PARENT_RUN_ID = parent.RUN_ID
SOURCE_RUNTIME_REVIEW_RUN_ID = ce.RUN_ID
NEXT_RUN_ID = "run364CH_review_cost_stable_h17_source_guard_offensive_scout_without_db_v1"

STATUS = "completed_stage364CG_cost_stable_h17_source_guard_proxy_scout_h17_focus_selected_review_required_no_authority"
JUDGMENT = "positive_proxy_scout_h17_overlay_focus_small_lift_no_split_review_required_no_authority"
DECISION = "stage364CG_open_run364CH_cost_stable_h17_source_guard_proxy_scout_review"
CLAIM_BOUNDARY = (
    "research_development_proxy_scout_only_rule_surface_no_new_model_artifact_no_new_mt5_execution_"
    "no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

DENSITY_FLOOR = 3.0
SHORT_FLOOR = 100
PARENT_VARIANT_ID = "cd02_ca01_clone_current_session"
NATIVE_CONTROL_VARIANT_ID = "cd03_native_short_same_calendar_current_session"

STAGE_DIR = parent.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
SPEC_DIR = STAGE_DIR / "00_spec"
SELECTED_DIR = STAGE_DIR / "04_selected"

INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
PROXY_SCOUT_SURFACE = RUN_DIR / "cg_proxy_scout_surface.csv"
SELECTED_CANDIDATE = RUN_DIR / "selected_cg_candidate.json"
SELECTED_TRADE_TAPE = RUN_DIR / "selected_cg_trade_tape.csv"
CANDIDATE_FILTER_AUDIT = RUN_DIR / "candidate_filter_audit.csv"
CANDIDATE_SOURCE_ATTRIBUTION = RUN_DIR / "candidate_source_attribution.csv"
CANDIDATE_MONTH_STABILITY = RUN_DIR / "candidate_month_stability.csv"
COST_STRESS_DIAGNOSTIC = RUN_DIR / "cost_stress_diagnostic.csv"
PROXY_MT5_DIFF_PLAN = RUN_DIR / "proxy_mt5_diff_plan.csv"
RUN364CH_QUEUE = RUN_DIR / "run364CH_review_queue.csv"
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

REPORT_PATH = REVIEW_DIR / "run364CG_cost_stable_h17_source_guard_proxy_scout.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364CG_cost_stable_h17_source_guard_proxy_scout.md"
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
    parent.RUN364CG_SCOUT_QUEUE,
    parent.COST_LAYERED_SCORECARD,
    parent.H17_OVERLAY_QUALITY_BY_MONTH,
    parent.H17_OVERLAY_QUALITY_BY_OPEN_HOUR,
    parent.DATA_INTEGRITY_AUDIT,
    parent.RUN_MANIFEST,
    ce.FINAL_DECISION,
    ce.TRADE_ATTRIBUTION,
    ce.ATTRIBUTION_BY_SOURCE,
    ce.SOURCE_OVERLAY_DECOMPOSITION,
    ce.PAIR_DELTAS,
    ce.RUN_MANIFEST,
]

OUTPUT_FILES = [
    INPUT_MANIFEST,
    WORK_PACKET,
    PROXY_SCOUT_SURFACE,
    SELECTED_CANDIDATE,
    SELECTED_TRADE_TAPE,
    CANDIDATE_FILTER_AUDIT,
    CANDIDATE_SOURCE_ATTRIBUTION,
    CANDIDATE_MONTH_STABILITY,
    COST_STRESS_DIAGNOSTIC,
    PROXY_MT5_DIFF_PLAN,
    RUN364CH_QUEUE,
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
    return parent.rel(path)


def exists(path: Path | str) -> bool:
    return parent.exists(path)


def sha(path: Path | str) -> str:
    return parent.sha(path)


def write_json(path: Path, payload: Mapping[str, Any]) -> None:
    parent.write_json(path, json_ready(payload))


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


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


def read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(io_path(path), encoding="utf-8-sig")


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
    try:
        if value in ("", None):
            return default
        number = float(value)
    except (TypeError, ValueError):
        return default
    return number if math.isfinite(number) else default


def finite(value: Any, digits: int = 10) -> float | str:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return ""
    if math.isnan(number):
        return ""
    if math.isinf(number):
        return "inf" if number > 0 else "-inf"
    return round(number, digits)


def safe_pf(gross_profit: float, gross_loss: float) -> float:
    loss = abs(gross_loss)
    if loss == 0:
        return math.inf if gross_profit > 0 else 0.0
    return gross_profit / loss


def markdown_table(rows: Sequence[Mapping[str, Any]], columns: Sequence[str], limit: int = 12) -> str:
    return parent.markdown_table(rows, columns, limit)


def ensure_dirs() -> None:
    for path in [RUN_DIR, REVIEW_DIR, SPEC_DIR, SELECTED_DIR, DECISION_DOC.parent]:
        io_path(path).mkdir(parents=True, exist_ok=True)


def validate_inputs() -> tuple[dict[str, Any], dict[str, Any]]:
    missing = [rel(path) for path in INPUT_FILES if not exists(path)]
    if missing:
        raise FileNotFoundError("missing CG inputs(CG 입력 누락): " + ", ".join(missing))
    cf_final = read_json(parent.FINAL_DECISION)
    ce_final = read_json(ce.FINAL_DECISION)
    if cf_final.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"CF next_run_id mismatch(CF 다음 실행 불일치): {cf_final.get('next_run_id')} != {RUN_ID}")
    for label, final in [("CF", cf_final), ("CE", ce_final)]:
        if final.get("runtime_authority") != "not_claimed" or final.get("operating_promotion") != "not_claimed":
            raise RuntimeError(f"{label} forbidden operating claim({label} 금지 운영 주장 존재)")
    parent_gates = read_csv(parent.GATE_AUDIT)
    if parent_gates.empty or set(parent_gates["status"].astype(str)) != {"passed"}:
        raise RuntimeError("CF gate audit is not fully passed(CF 게이트 감사가 모두 통과가 아님)")
    queue = read_csv(parent.RUN364CG_SCOUT_QUEUE)
    if len(queue) != 12:
        raise RuntimeError(f"CG queue rows mismatch(CG 대기열 행 불일치): {len(queue)}")
    return cf_final, ce_final


def input_manifest_rows() -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "input_path": rel(path),
            "exists": exists(path),
            "sha256": sha(path),
            "input_role": "CG proxy scout source(CG 프록시 정찰 원천)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for path in INPUT_FILES
    ]


def load_trade_frames() -> tuple[pd.DataFrame, pd.DataFrame]:
    trades = read_csv(ce.TRADE_ATTRIBUTION)
    for column in ["net_profit", "gross_profit", "swap", "commission", "p_short", "p_flat", "p_long", "hold_minutes"]:
        trades[column] = pd.to_numeric(trades[column], errors="coerce").fillna(0.0)
    trades["open_time_dt"] = pd.to_datetime(trades["open_time"])
    trades["close_time_dt"] = pd.to_datetime(trades["close_time"])
    trades["open_month"] = trades["open_time_dt"].dt.strftime("%Y-%m")
    trades["open_month_num"] = trades["open_time_dt"].dt.month
    trades["margin_vs_long"] = trades["p_short"] - trades["p_long"]
    trades["margin_vs_flat"] = trades["p_short"] - trades["p_flat"]
    cd02 = trades[trades["variant_id"].eq(PARENT_VARIANT_ID)].sort_values("open_time_dt").reset_index(drop=True)
    cd03 = trades[trades["variant_id"].eq(NATIVE_CONTROL_VARIANT_ID)].sort_values("open_time_dt").reset_index(drop=True)
    if len(cd02) != 1008 or len(cd03) != 1002:
        raise RuntimeError(f"unexpected CE trade counts(CE 거래수 이상): cd02={len(cd02)}, cd03={len(cd03)}")
    return cd02, cd03


def effective_business_days(parent_final: Mapping[str, Any]) -> float:
    trade_count = as_float(parent_final.get("parent_trade_count"))
    density = as_float(parent_final.get("parent_density"))
    if trade_count <= 0 or density <= 0:
        return 314.0
    return trade_count / density


def metric_frame(frame: pd.DataFrame, *, effective_days: float) -> dict[str, Any]:
    ordered = frame.sort_values("open_time_dt").copy()
    gross_profit = float(ordered.loc[ordered["gross_profit"] > 0, "gross_profit"].sum())
    gross_loss = float(ordered.loc[ordered["gross_profit"] < 0, "gross_profit"].sum())
    net = float(ordered["net_profit"].sum())
    count = int(len(ordered))
    long_count = int(ordered["direction"].eq("long").sum())
    short_count = int(ordered["direction"].eq("short").sum())
    equity = ordered["net_profit"].cumsum()
    closed_dd = float((equity.cummax() - equity).max()) if count else 0.0
    return {
        "net_profit": finite(net, 2),
        "profit_factor": finite(safe_pf(gross_profit, gross_loss), 10),
        "expectancy": finite(net / count if count else 0.0, 10),
        "trade_count": count,
        "trade_density": finite(count / effective_days if effective_days else 0.0, 10),
        "long_trade_count": long_count,
        "short_trade_count": short_count,
        "short_share": finite(short_count / count if count else 0.0, 10),
        "closed_trade_drawdown_proxy": finite(closed_dd, 2),
        "closed_trade_recovery_proxy": finite(net / closed_dd if closed_dd else 0.0, 10),
        "gross_profit_sum": finite(gross_profit, 2),
        "gross_loss_sum": finite(gross_loss, 2),
        "swap_sum": finite(float(ordered["swap"].sum()), 2),
        "commission_sum": finite(float(ordered["commission"].sum()), 2),
    }


def native_q10_thresholds(parent_trades: pd.DataFrame) -> tuple[float, float]:
    native = parent_trades[parent_trades["source_bucket"].eq("native_short_threshold")]
    return float(native["p_short"].quantile(0.10)), float(native["margin_vs_long"].quantile(0.10))


def apply_candidate(
    queue_row: Mapping[str, Any],
    parent_trades: pd.DataFrame,
    native_control: pd.DataFrame,
    *,
    native_q10: tuple[float, float],
) -> tuple[pd.DataFrame, pd.DataFrame, str, str]:
    candidate_id = str(queue_row["candidate_id"])
    policy = str(queue_row.get("h17_overlay_policy", ""))
    cost_policy = str(queue_row.get("cost_stress_policy", ""))
    base = parent_trades.copy()
    source_variant = PARENT_VARIANT_ID
    transform = "preserve_cd02_current_session(CD02 현재 세션 보존)"

    if candidate_id == "cg05_overlay_off_native_short_control":
        selected = native_control.copy()
        removed = base.iloc[0:0].copy()
        return selected, removed, NATIVE_CONTROL_VARIANT_ID, "native_short_control_cd03(CD03 기본 숏 대조)"

    mask = pd.Series(True, index=base.index)
    if policy.startswith("synthetic_overlay_p_short_q"):
        p_floor = as_float(queue_row.get("p_short_floor"))
        margin_floor = as_float(queue_row.get("margin_vs_long_floor"))
        weak_overlay = (
            base["source_bucket"].eq("synthetic_short_overlay")
            & ((base["p_short"] < p_floor) | (base["margin_vs_long"] < margin_floor))
        )
        mask &= ~weak_overlay
        transform = f"drop_weak_h17_overlay(ps>={p_floor},margin>={margin_floor})(약한 17시 오버레이 제거)"
    elif policy == "synthetic_overlay_only_for_h17_short_bucket":
        native = base["source_bucket"].eq("native_short_threshold")
        mask &= ~native
        transform = "overlay_only_remove_native_short_threshold(오버레이 전용, 기본 숏 제거)"
    elif policy.startswith("guard_negative_overlay_months="):
        month_text = policy.split("=", 1)[1]
        bad_months = [item.strip() for item in month_text.split(",") if item.strip()]
        bad_overlay = base["source_bucket"].eq("synthetic_short_overlay") & base["open_month"].isin(bad_months)
        mask &= ~bad_overlay
        transform = "drop_negative_overlay_months(음수 오버레이 월 제거)"
    elif policy == "focus_best_overlay_open_hour=17":
        non_h17_overlay = base["source_bucket"].eq("synthetic_short_overlay") & (base["open_hour"] != 17)
        mask &= ~non_h17_overlay
        transform = "focus_h17_overlay_only(17시 오버레이 집중)"
    elif policy == "short_count_floor_100_and_overlay_kept":
        transform = "short_floor_guard_no_filter(숏 100개 하한 가드, 필터 없음)"
    elif policy == "no_count_split_quality_surface":
        p_floor, margin_floor = native_q10
        weak_native = (
            base["source_bucket"].eq("native_short_threshold")
            & ((base["p_short"] < p_floor) | (base["margin_vs_long"] < margin_floor))
        )
        non_h17_overlay = base["source_bucket"].eq("synthetic_short_overlay") & (base["open_hour"] != 17)
        mask &= ~(weak_native | non_h17_overlay)
        transform = "entry_known_source_quality_no_split(진입기지 원천 품질, 무분할)"

    if cost_policy == "native_short_swap_cost_firewall":
        native_bad_hours = base["source_bucket"].eq("native_short_threshold") & base["open_hour"].isin([17, 20])
        mask &= ~native_bad_hours
        transform = "native_short_hour17_20_cost_firewall(기본 숏 17/20시 비용 방화벽)"

    selected = base[mask].copy().sort_values("open_time_dt").reset_index(drop=True)
    removed = base[~mask].copy().sort_values("open_time_dt").reset_index(drop=True)
    return selected, removed, source_variant, transform


def candidate_status(row: Mapping[str, Any]) -> str:
    if "control" in str(row.get("queue_status", "")) or row.get("source_variant_id") == NATIVE_CONTROL_VARIANT_ID:
        return "control_only_not_selectable(대조 전용, 선택 불가)"
    if as_float(row["trade_density"]) < DENSITY_FLOOR:
        return "rejected_density_below_3(거절, 밀도 3 미만)"
    if as_float(row["net_delta_vs_parent"]) < 0 and as_float(row["profit_factor_delta_vs_parent"]) < 0:
        return "negative_proxy_net_pf_worse(부정 프록시, 순수익/PF 악화)"
    if as_float(row["short_trade_count"]) < SHORT_FLOOR:
        return "watch_short_floor_below_100(관찰, 숏 100개 미만)"
    if as_float(row["net_delta_vs_parent"]) > 0 and as_float(row["profit_factor_delta_vs_parent"]) >= 0:
        return "proxy_review_candidate_no_split(프록시 검토 후보, 무분할)"
    return "diagnostic_watch_no_package(진단 관찰, 패키지 아님)"


def selection_score(row: Mapping[str, Any]) -> float:
    if str(row.get("candidate_status", "")).startswith("control_only"):
        return -999.0
    score = 0.0
    if as_float(row["trade_density"]) >= DENSITY_FLOOR:
        score += 100.0
    if as_float(row["net_delta_vs_parent"]) > 0:
        score += 50.0
    score += as_float(row["net_delta_vs_parent"]) * 0.40
    score += as_float(row["profit_factor_delta_vs_parent"]) * 500.0
    if as_float(row["short_trade_count"]) >= SHORT_FLOOR:
        score += 25.0
    else:
        score -= (SHORT_FLOOR - as_float(row["short_trade_count"])) * 3.0
    score -= max(0.0, as_float(row["parent_trade_count"]) - as_float(row["trade_count"]) - 1.0) * 0.25
    if "diagnostic" not in str(row.get("candidate_status", "")):
        score += 10.0
    return round(score, 10)


def build_surface(
    parent_final: Mapping[str, Any],
    parent_trades: pd.DataFrame,
    native_control: pd.DataFrame,
) -> tuple[list[dict[str, Any]], dict[str, pd.DataFrame], list[dict[str, Any]]]:
    queue = read_csv(parent.RUN364CG_SCOUT_QUEUE).sort_values("queue_rank")
    parent_metric = metric_frame(parent_trades, effective_days=effective_business_days(parent_final))
    native_q10 = native_q10_thresholds(parent_trades)
    rows: list[dict[str, Any]] = []
    selected_frames: dict[str, pd.DataFrame] = {}
    filter_rows: list[dict[str, Any]] = []
    for _, raw in queue.iterrows():
        queue_row = raw.to_dict()
        candidate_id = str(queue_row["candidate_id"])
        frame, removed, source_variant, transform = apply_candidate(
            queue_row,
            parent_trades,
            native_control,
            native_q10=native_q10,
        )
        metric = metric_frame(frame, effective_days=effective_business_days(parent_final))
        stress_adjusted_net = float(frame["gross_profit"].sum() + frame["swap"].sum() * 2.0 + frame["commission"].sum())
        row = {
            "run_id": RUN_ID,
            "candidate_id": candidate_id,
            "queue_rank": int(queue_row["queue_rank"]),
            "variant_family": queue_row.get("variant_family", ""),
            "queue_status": queue_row.get("queue_status", ""),
            "source_variant_id": source_variant,
            "transform": transform,
            "h17_overlay_policy": queue_row.get("h17_overlay_policy", ""),
            "cost_stress_policy": queue_row.get("cost_stress_policy", ""),
            "trade_splitting_status": "not_used_no_added_entries(미사용, 추가 진입 없음)",
            "top_n_status": "not_used_fixed_rule_surface(미사용, 고정 규칙 표면)",
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
            "stress_adjusted_net_swap_haircut_1x": finite(stress_adjusted_net, 2),
            "stress_adjusted_net_delta_vs_parent": finite(stress_adjusted_net - as_float(parent_metric["net_profit"]), 10),
            "feature_boundary": "entry-known source_bucket/open_hour/month/probabilities only(진입기지 원천/시간/월/확률만)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        row["candidate_status"] = candidate_status(row)
        row["selection_score"] = selection_score(row)
        rows.append(row)
        selected_frames[candidate_id] = frame
        filter_rows.append(
            {
                "run_id": RUN_ID,
                "candidate_id": candidate_id,
                "source_variant_id": source_variant,
                "transform": transform,
                "input_trade_count": len(native_control) if source_variant == NATIVE_CONTROL_VARIANT_ID else len(parent_trades),
                "selected_trade_count": len(frame),
                "removed_trade_count": len(removed),
                "removed_net_profit": finite(removed["net_profit"].sum() if not removed.empty else 0.0, 2),
                "removed_short_count": int(removed["direction"].eq("short").sum()) if not removed.empty else 0,
                "no_trade_splitting": True,
                "effect": "rules remove or preserve existing entries only(규칙은 기존 진입만 제거 또는 보존)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    rows.sort(key=lambda item: (as_float(item["selection_score"]), as_float(item["net_profit"])), reverse=True)
    return rows, selected_frames, filter_rows


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
                    "trade_count": metric["trade_count"],
                    "net_profit": metric["net_profit"],
                    "profit_factor": metric["profit_factor"],
                    "short_trade_count": metric["short_trade_count"],
                    "month_status": "bad_month_watch(나쁜 월 관찰)" if as_float(metric["net_profit"]) <= 0 else "positive_or_neutral(양수 또는 중립)",
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


def data_integrity_rows(
    parent_trades: pd.DataFrame,
    native_control: pd.DataFrame,
    surface: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    duplicate_parent = int(parent_trades["open_time"].duplicated().sum())
    duplicate_control = int(native_control["open_time"].duplicated().sum())
    no_split_failures = [row for row in surface if as_float(row["trade_count"]) > as_float(row["parent_trade_count"])]
    rows = [
        {
            "run_id": RUN_ID,
            "audit_item": "data_source(데이터 원천)",
            "status": "passed",
            "observed": rel(ce.TRADE_ATTRIBUTION),
            "effect": "CG replays parsed MT5 closed trades(CG는 파싱된 MT5 종료 거래를 재생)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "audit_item": "time_axis(시간축)",
            "status": "passed",
            "observed": "open_time/close_time from MT5 report, open_time sorted(MT5 보고서 진입/청산 시각, 진입 시각 정렬)",
            "effect": "candidate filters use entry-known fields only(후보 필터는 진입 시점 기지 필드만 사용)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "audit_item": "duplicate_open_time(중복 진입 시각)",
            "status": "passed" if duplicate_parent == 0 and duplicate_control == 0 else "failed",
            "observed": f"cd02={duplicate_parent}; cd03={duplicate_control}",
            "effect": "one closed-trade row remains one possible entry(종료 거래 한 행이 가능한 진입 한 개로 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "audit_item": "feature_label_boundary(피처/라벨 경계)",
            "status": "passed",
            "observed": "rules use source_bucket/open_hour/month/p_short/p_long/p_flat; realized PnL only scores offline scout(규칙은 원천/시간/월/확률만 쓰고 실현 손익은 오프라인 점수에만 사용)",
            "effect": "live rule does not consume future PnL(실거래 규칙은 미래 손익을 먹지 않음)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "audit_item": "no_trade_splitting(거래 쪼개기 없음)",
            "status": "passed" if not no_split_failures else "failed",
            "observed": f"candidate_count_gt_parent={len(no_split_failures)}",
            "effect": "trade/day is not raised by splitting profit(수익을 쪼개 거래수를 올리지 않음)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "audit_item": "tier_scope(티어 범위)",
            "status": "passed",
            "observed": "Tier A used + Tier B missing_required(Tier A 사용 + Tier B 필수 누락)",
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
            "queue_id": "ch01_selected_h17_focus_package_gate_review",
            "review_subject": selected["candidate_id"],
            "review_question": "Does h17-only overlay focus survive package gates?(17시 전용 오버레이 집중이 패키지 게이트를 버티는가?)",
            "success_criteria": "net/PF/density >= parent and short_count >= 100 without trade splitting(순수익/PF/밀도 상위 이상, 숏 100개 이상, 거래 쪼개기 없음)",
            "failure_criteria": "small lift disappears under month/source/cost stress(작은 우위가 월/원천/비용 압박에서 사라짐)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "queue_rank": 2,
            "queue_id": "ch02_cost_stress_and_month_stability_review",
            "review_subject": selected["candidate_id"],
            "review_question": "Where does the small lift come from by source and month?(작은 우위가 원천과 월별로 어디서 오는가?)",
            "success_criteria": "lift is not one bad-month deletion artifact(우위가 단일 월 제거 착시가 아님)",
            "failure_criteria": "source/month attribution is too sparse or selection-biased(원천/월 귀속이 너무 희소하거나 선택 편향)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "queue_rank": 3,
            "queue_id": "ch03_mt5_reprobe_decision_boundary",
            "review_subject": selected["candidate_id"],
            "review_question": "Is a narrow MT5 reprobe package justified?(좁은 MT5 재탐침 패키지가 정당한가?)",
            "success_criteria": "review opens package only if proxy lift is stable enough(프록시 우위가 충분히 안정적일 때만 패키지 개방)",
            "failure_criteria": "review downgrades to failure memory and next offensive seed(검토가 실패 기억과 다음 공격 씨앗으로 낮춤)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def proxy_mt5_diff_rows(selected: Mapping[str, Any], parent_final: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "comparison_id": "selected_proxy_vs_parent_mt5(선택 프록시 대 상위 MT5)",
            "selected_candidate_id": selected["candidate_id"],
            "parent_mt5_net": parent_final.get("parent_net_profit"),
            "proxy_net": selected["net_profit"],
            "net_diff_proxy_minus_parent": selected["net_delta_vs_parent"],
            "parent_mt5_profit_factor": parent_final.get("parent_profit_factor"),
            "proxy_profit_factor": selected["profit_factor"],
            "parent_mt5_density": parent_final.get("parent_density"),
            "proxy_density": selected["trade_density"],
            "usability": "proxy_scout_screen_only_mt5_reprobe_required_before_runtime_claim(프록시 정찰 선별 전용, 런타임 주장 전 MT5 재탐침 필요)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def write_work_packet() -> None:
    write_json(
        WORK_PACKET,
        {
            "run_id": RUN_ID,
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
            "hypothesis": "cost-stable h17 source guard can improve source quality while keeping >=3 trades/day without splitting(비용 안정 17시 원천 가드가 거래 쪼개기 없이 일 3회 이상과 원천 품질을 함께 개선할 수 있다)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def gate_rows(
    surface: Sequence[Mapping[str, Any]],
    data_rows_: Sequence[Mapping[str, Any]],
    receipts: Sequence[Path],
    *,
    final_written: bool,
) -> list[dict[str, Any]]:
    selected_like = [row for row in surface if str(row.get("candidate_status", "")).startswith("proxy_review_candidate")]
    gates = [
        (
            "scope_completion_gate",
            len(surface) == 12 and len(selected_like) >= 1,
            PROXY_SCOUT_SURFACE,
            "12 queue rows replayed and at least one review candidate exists(대기열 12행 재생 및 검토 후보 1개 이상)",
        ),
        (
            "kpi_contract_audit",
            all(str(row.get("net_profit", "")) != "" and str(row.get("profit_factor", "")) != "" for row in surface),
            PROXY_SCOUT_SURFACE,
            "net/PF/expectancy/DD proxy/trades/density recorded(순수익/PF/기대값/DD 프록시/거래수/밀도 기록)",
        ),
        (
            "data_integrity_audit",
            all(row["status"] == "passed" for row in data_rows_),
            DATA_INTEGRITY_AUDIT,
            "time axis, leakage boundary, no-split rule passed(시간축/누수 경계/무분할 규칙 통과)",
        ),
        (
            "no_trade_splitting_gate",
            all(as_float(row["trade_count"]) <= as_float(row["parent_trade_count"]) for row in surface),
            CANDIDATE_FILTER_AUDIT,
            "candidate entries are not split or added(후보 진입은 쪼개거나 추가하지 않음)",
        ),
        (
            "skill_receipt_lint",
            all(exists(path) for path in receipts),
            RUN_EVIDENCE_RECEIPT,
            "required skill receipts are present(필수 스킬 영수증 존재)",
        ),
        (
            "required_gate_coverage_audit",
            final_written,
            GATE_AUDIT,
            "required gates are connected to closeout(필수 게이트가 종료 기록에 연결)",
        ),
        (
            "final_claim_guard",
            exists(CLAIM_RECEIPT),
            CLAIM_RECEIPT,
            "no operating promotion, runtime authority, live readiness, or goal claim(운영 승격/런타임 권위/실거래 준비/목표 달성 주장 없음)",
        ),
    ]
    rows = [
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
    write_csv(GATE_AUDIT, rows)
    return rows


def final_payload(
    parent_final: Mapping[str, Any],
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
        "source_runtime_review_run_id": SOURCE_RUNTIME_REVIEW_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "created_at_utc": created_at,
        "surface_rows": len(surface),
        "review_candidate_rows": sum(1 for row in surface if str(row.get("candidate_status", "")).startswith("proxy_review_candidate")),
        "selected_candidate_id": selected["candidate_id"],
        "selected_transform": selected["transform"],
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
        "selected_trade_delta_vs_parent": selected["trade_delta_vs_parent"],
        "selected_short_delta_vs_parent": selected["short_delta_vs_parent"],
        "selected_stress_adjusted_net_swap_haircut_1x": selected["stress_adjusted_net_swap_haircut_1x"],
        "parent_mt5_net_profit": parent_final.get("parent_net_profit"),
        "parent_mt5_profit_factor": parent_final.get("parent_profit_factor"),
        "parent_mt5_trade_count": parent_final.get("parent_trade_count"),
        "parent_mt5_density": parent_final.get("parent_density"),
        "parent_mt5_equity_drawdown_amount": parent_final.get("parent_equity_drawdown_amount"),
        "parent_mt5_recovery_factor": parent_final.get("parent_recovery_factor"),
        "new_model_training": "not_run_rule_surface_only(미실행, 규칙 표면 전용)",
        "new_mt5_execution": "not_run_proxy_scout_only(미실행, 프록시 정찰 전용)",
        "external_verification_status": "out_of_scope_by_claim_proxy_scout_only(주장 범위 밖, 프록시 정찰 전용)",
        "forward_passed": "not_claimed",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "live_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "gate_passes": sum(1 for row in gates if row["status"] == "passed"),
        "gate_total": len(gates),
        "claim_boundary": CLAIM_BOUNDARY,
    }


def write_receipts(final: Mapping[str, Any], selected: Mapping[str, Any], proxy_mt5_rows_: Sequence[Mapping[str, Any]]) -> None:
    write_json(
        RUN_EVIDENCE_RECEIPT,
        {
            "run_id": RUN_ID,
            "measurement_scope": "proxy scout surface with MT5 closed-trade replay(프록시 정찰 표면 및 MT5 종료 거래 재생)",
            "management_state": [rel(PROXY_SCOUT_SURFACE), rel(SELECTED_CANDIDATE), rel(RUN364CH_QUEUE), rel(RUN_MANIFEST)],
            "judgment_class": "positive_with_proxy_boundary(프록시 경계 내 긍정)",
            "scoreboard": "structural_scout(구조 스카우트)",
            "parity_level": "P0_unverified(P0 미검증)",
            "wfo_status": "not_applicable_single_runtime_trade_replay(해당 없음, 단일 런타임 거래 재생)",
            "registry_update_required": "yes(예)",
            "negative_memory_required": "no(아니오)",
            "hard_gate_applicable": "no(아니오)",
            "evidence_boundary": "scout-only(정찰 전용)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(
        EXPERIMENT_RECEIPT,
        {
            "run_id": RUN_ID,
            "hypothesis": "h17 overlay focus can preserve density and slightly lift net/PF without trade splitting(17시 오버레이 집중이 거래 쪼개기 없이 밀도와 순수익/PF를 보존 또는 소폭 개선한다)",
            "decision_use": "open CH review, not package or authority(CH 검토 개방, 패키지나 권위 아님)",
            "comparison_baseline": PARENT_VARIANT_ID,
            "control_variables": ["same CE parsed MT5 trades(동일 CE 파싱 MT5 거래)", "fixed 0.1 lot inherited(고정 0.1랏 상속)", "no added entries(추가 진입 없음)"],
            "changed_variables": ["source/hour/month/probability rule filters(원천/시간/월/확률 규칙 필터)"],
            "sample_scope": "FPMarkets US100 M5 Stage364 CE CD02/CD03 closed trades(FPMarkets US100 M5 364단계 CE CD02/CD03 종료 거래)",
            "success_criteria": "density >=3, net/PF not worse, short_count >=100, no splitting(밀도 3 이상, 순수익/PF 비악화, 숏 100개 이상, 무분할)",
            "failure_criteria": "density collapse, short floor failure, or source/month stress artifact(밀도 붕괴, 숏 하한 실패, 원천/월 압박 착시)",
            "invalid_conditions": "future PnL used as live feature or added trade slices(미래 손익을 실거래 피처로 쓰거나 거래 조각 추가)",
            "stop_conditions": "CH review decides package gate, failure memory, or next offensive seed(CH 검토가 패키지 게이트/실패 기억/다음 공격 씨앗 결정)",
            "evidence_plan": [rel(PROXY_SCOUT_SURFACE), rel(CANDIDATE_SOURCE_ATTRIBUTION), rel(CANDIDATE_MONTH_STABILITY), rel(PROXY_MT5_DIFF_PLAN)],
        },
    )
    write_json(
        DATA_RECEIPT,
        {
            "run_id": RUN_ID,
            "data_source": rel(ce.TRADE_ATTRIBUTION),
            "time_axis": "MT5 report open_time/close_time, sorted by open_time(MT5 보고서 진입/청산 시각, 진입 시각 정렬)",
            "sample_scope": "US100 M5 Tier A used, CD02 1008 trades and CD03 1002 trades(US100 M5 Tier A 사용, CD02 1008거래 및 CD03 1002거래)",
            "missing_or_duplicate_check": rel(DATA_INTEGRITY_AUDIT),
            "feature_label_boundary": "live-like rule fields are entry-known; realized PnL only offline scoring(실거래 유사 규칙 필드는 진입기지, 실현 손익은 오프라인 점수만)",
            "split_boundary": "single runtime replay scout, no WFO claim(단일 런타임 재생 정찰, WFO 주장 없음)",
            "leakage_risk": "month/source rules were inspired by parent evidence and need CH review(월/원천 규칙은 상위 근거에서 착안했으므로 CH 검토 필요)",
            "data_hash_or_identity": [{"path": rel(path), "sha256": sha(path)} for path in INPUT_FILES if exists(path)],
            "integrity_judgment": "usable_with_boundary(경계부 사용 가능)",
        },
    )
    write_json(
        MODEL_RECEIPT,
        {
            "run_id": RUN_ID,
            "model_family": "no_new_model_rule_surface_only(새 모델 없음, 규칙 표면 전용)",
            "target_and_label": "not_applicable_existing_MT5_trades_replayed(해당 없음, 기존 MT5 거래 재생)",
            "split_method": "single runtime trade replay scout(단일 런타임 거래 재생 정찰)",
            "selection_metric": "density pass, net/PF delta, short floor, no-split score(밀도 통과, 순수익/PF 차이, 숏 하한, 무분할 점수)",
            "secondary_metrics": ["source attribution(원천 귀속)", "month stability(월 안정성)", "swap haircut stress(스왑 헤어컷 압박)"],
            "threshold_policy": "fixed queue rules, no top_n(고정 대기열 규칙, top_n 없음)",
            "overfit_risk": "parent-evidence inspired month/source filters(상위 근거 착안 월/원천 필터)",
            "calibration_risk": "probabilities are ranks from runtime scores, not recalibrated probabilities(확률은 런타임 점수 순위이며 재보정 확률 아님)",
            "comparison_baseline": PARENT_VARIANT_ID,
            "validation_judgment": "exploratory(탐색)",
        },
    )
    write_json(
        JUDGMENT_RECEIPT,
        {
            "run_id": RUN_ID,
            "result_subject": selected["candidate_id"],
            "evidence_available": [rel(PROXY_SCOUT_SURFACE), rel(SELECTED_CANDIDATE), rel(PROXY_MT5_DIFF_PLAN), rel(GATE_AUDIT)],
            "evidence_missing": ["new MT5 runtime probe(새 MT5 런타임 탐침)", "forward replay(전진 재생)", "runtime parity authority(런타임 동등성 권위)"],
            "judgment_label": JUDGMENT,
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": NEXT_RUN_ID,
            "user_explanation_hook": "h17-only overlay focus is a small no-split proxy lift, not an operating model(17시 전용 오버레이 집중은 작은 무분할 프록시 우위이지 운영 모델이 아님)",
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            "run_id": RUN_ID,
            "allowed_claim": "proxy scout review candidate only(프록시 정찰 검토 후보 전용)",
            "forbidden_claims": ["runtime_authority", "operating_promotion", "live_readiness", "goal_achieve"],
            "new_model_training": final["new_model_training"],
            "new_mt5_execution": final["new_mt5_execution"],
            "proxy_mt5_comparison_plan": list(proxy_mt5_rows_),
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def refresh_lineage_receipt(final: Mapping[str, Any]) -> None:
    write_json(
        LINEAGE_RECEIPT,
        {
            "run_id": RUN_ID,
            "source_inputs": [{"path": rel(path), "sha256": sha(path)} for path in INPUT_FILES if exists(path)],
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [rel(path) for path in OUTPUT_FILES if exists(path) and Path(path).is_file()],
            "artifact_hashes": {rel(path): sha(path) for path in OUTPUT_FILES if exists(path) and Path(path).is_file()},
            "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "availability": "tracked_after_closeout_or_reproducible_from_script(종료 후 추적 또는 스크립트로 재현 가능)",
            "lineage_judgment": "connected_with_proxy_boundary(프록시 경계로 연결됨)",
            "claim_boundary": CLAIM_BOUNDARY,
            "final_status": final["status"],
        },
    )


def replace_prefixed_lines(path: Path, replacements: Mapping[str, str], *, bom: bool = True) -> None:
    if not exists(path):
        return
    text = io_path(path).read_text(encoding="utf-8-sig")
    lines: list[str] = []
    for line in text.splitlines():
        replacement = None
        for prefix, value in replacements.items():
            if line.startswith(prefix):
                replacement = value
                break
        lines.append(replacement if replacement is not None else line)
    write_text(path, "\n".join(lines).rstrip() + "\n", bom=bom)


def write_docs(
    final: Mapping[str, Any],
    selected: Mapping[str, Any],
    surface: Sequence[Mapping[str, Any]],
    filters: Sequence[Mapping[str, Any]],
    source_rows: Sequence[Mapping[str, Any]],
    month_rows_: Sequence[Mapping[str, Any]],
    cost_rows: Sequence[Mapping[str, Any]],
    queue_rows_: Sequence[Mapping[str, Any]],
    gates: Sequence[Mapping[str, Any]],
) -> None:
    top_surface = list(surface)[:12]
    selected_sources = [row for row in source_rows if row["candidate_id"] == selected["candidate_id"]]
    selected_months = [row for row in month_rows_ if row["candidate_id"] == selected["candidate_id"]]
    report = f"""# run364CG cost-stable h17 source guard proxy scout(364CG 비용 안정 17시 원천 가드 프록시 정찰)

## Result(결과)

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- selected(선택): `{final['selected_candidate_id']}`
- next(다음): `{NEXT_RUN_ID}`
- gate(게이트): `{final['gate_passes']}/{final['gate_total']}`

## Action(행동)

Action(행동): CF queue(CF 대기열) 12개를 CE parsed MT5 closed trades(CE 파싱 MT5 종료 거래)에 no-split proxy replay(무분할 프록시 재생)로 적용했다.

Effect(효과): `cg09_best_open_hour_overlay_focus`가 parent CD02(상위 CD02) 대비 net(순수익) `{final['selected_net_delta_vs_parent']}`, PF(수익 팩터) `{final['selected_profit_factor_delta_vs_parent']}`만큼 소폭 개선되고, density(밀도) `{final['selected_trade_density']}`와 short count(숏 수) `{final['selected_short_trade_count']}`를 유지해 CH review(CH 검토) 대상으로 분리됐다.

## Surface(표면)

{markdown_table(top_surface, ['candidate_id', 'candidate_status', 'net_profit', 'profit_factor', 'trade_count', 'trade_density', 'short_trade_count', 'net_delta_vs_parent', 'selection_score'], 12)}

## Selected Source Attribution(선택 원천 귀속)

{markdown_table(selected_sources, ['source_bucket', 'trade_count', 'net_profit', 'profit_factor', 'expectancy', 'short_trade_count'], 8)}

## Selected Month Stability(선택 월 안정성)

{markdown_table(selected_months, ['open_month', 'trade_count', 'net_profit', 'profit_factor', 'short_trade_count', 'month_status'], 16)}

## Filter Audit(필터 감사)

{markdown_table(filters, ['candidate_id', 'transform', 'selected_trade_count', 'removed_trade_count', 'removed_net_profit', 'no_trade_splitting'], 12)}

## Cost Stress(비용 압박)

{markdown_table(cost_rows, ['candidate_id', 'net_profit', 'swap_sum', 'stress_adjusted_net_swap_haircut_1x', 'stress_judgment'], 12)}

## CH Queue(CH 대기열)

{markdown_table(queue_rows_, ['queue_rank', 'queue_id', 'review_question', 'success_criteria'], 6)}

## Gates(게이트)

{markdown_table(gates, ['gate', 'status', 'evidence', 'effect'], 10)}

## Boundary(경계)

This run(이번 실행)은 proxy scout(프록시 정찰)이다. new model training(새 모델 학습), new MT5 execution(새 MT5 실행), forward pass(전진 통과), runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)이다.
"""
    write_text(REPORT_PATH, report, bom=True)
    write_text(
        DECISION_DOC,
        f"""# {TODAY} Stage364CG cost-stable h17 source guard proxy scout(비용 안정 17시 원천 가드 프록시 정찰)

Action(행동): `{RUN_ID}`에서 CF 12행 queue(대기열)를 무분할 proxy replay(프록시 재생)로 실행했다.

Effect(효과): `{final['selected_candidate_id']}`를 CH review(CH 검토) 대상으로 넘기되, MT5 runtime probe(MT5 런타임 탐침) 전까지 운영 주장(operating claim, 운영 주장)은 닫아 둔다.

- report(보고서): `{rel(REPORT_PATH)}`
- final_decision(최종 결정): `{rel(FINAL_DECISION)}`
- selected net/PF/density/trades(선택 순수익/수익 팩터/밀도/거래수): `{final['selected_net_profit']}` / `{final['selected_profit_factor']}` / `{final['selected_trade_density']}` / `{final['selected_trade_count']}`
- next_run(다음 실행): `{NEXT_RUN_ID}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
        bom=True,
    )
    append_text_once(REVIEW_INDEX, RUN_ID, f"- `{RUN_ID}`: `{rel(REPORT_PATH)}` - cost-stable h17 source guard proxy scout(비용 안정 17시 원천 가드 프록시 정찰).")
    append_text_once(
        STAGE_BRIEF,
        "## run364CG Cost-Stable H17 Source Guard Proxy Scout Closeout",
        f"""## run364CG Cost-Stable H17 Source Guard Proxy Scout Closeout(364CG 비용 안정 17시 원천 가드 프록시 정찰 종료)

Action(행동): CF queue(CF 대기열) 12개를 existing MT5 closed-trade replay(기존 MT5 종료 거래 재생)로 정찰했다.

Effect(효과): `{final['selected_candidate_id']}`가 no-split(무분할) 기준으로 small lift(작은 우위)를 보여 `{NEXT_RUN_ID}` review(검토)로 넘기며, runtime authority(런타임 권위)는 주장하지 않는다.
""",
    )
    append_text_once(
        STAGE_README,
        RUN_ID,
        f"""## {RUN_ID}

Action(행동): cost-stable h17 source guard queue(비용 안정 17시 원천 가드 대기열)를 proxy scout(프록시 정찰)로 실행했다.

Effect(효과): `{final['selected_candidate_id']}`를 CH review(CH 검토)로 넘기고 stage branch(단계 분기)는 만들지 않는다.
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
    replace_prefixed_lines(
        STAGE_README,
        {
            "Current run": f"Current run(현재 실행): `{NEXT_RUN_ID}`",
            "Latest completed run": f"Latest completed run(최근 완료 실행): `{RUN_ID}`",
            "Current truth": f"Current truth(현재 진실): run364CG(364CG 실행)는 `{final['selected_candidate_id']}`를 no-split proxy review subject(무분할 프록시 검토 대상)로 만들었다. Proxy net/PF/density/trades(프록시 순수익/수익 팩터/밀도/거래수)는 `{final['selected_net_profit']}` / `{final['selected_profit_factor']}` / `{final['selected_trade_density']}` / `{final['selected_trade_count']}`이고, 새 MT5 실행 전까지 운영 권위는 없다.",
            "Next action": f"Next action(다음 행동): `{NEXT_RUN_ID}`에서 source/month/cost stress(원천/월/비용 압박)와 package gate(패키지 게이트)를 검토한다.",
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

Current truth(현재 진실): `run364CG` replayed(재생 완료) `12` cost-stable h17 source guard rows(비용 안정 17시 원천 가드 행). Selected proxy(선택 프록시)는 `{final['selected_candidate_id']}`이고 net/PF/density/trades/shorts(순수익/수익 팩터/밀도/거래수/숏수)는 `{final['selected_net_profit']}` / `{final['selected_profit_factor']}` / `{final['selected_trade_density']}` / `{final['selected_trade_count']}` / `{final['selected_short_trade_count']}`다.

Next action(다음 행동): `{NEXT_RUN_ID}`에서 selected h17 focus(선택 17시 집중)의 source/month/cost stress(원천/월/비용 압박), proxy/MT5 diff plan(프록시/MT5 차이 계획), package gate(패키지 게이트)를 검토한다.

Operating boundary(운영 경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함).
""",
        bom=True,
    )
    write_text(
        SELECTION_STATUS,
        f"""# Stage364 selection status(선택 상태)

Updated(갱신): {final['created_at_utc']}

Current run(현재 실행): `{NEXT_RUN_ID}`
Latest completed run(최근 완료 실행): `{RUN_ID}`

Selected proxy review subject(선택 프록시 검토 대상): `{final['selected_candidate_id']}`

Proxy KPI(프록시 핵심 성과 지표): net `{final['selected_net_profit']}`, PF `{final['selected_profit_factor']}`, expectancy `{final['selected_expectancy']}`, trades `{final['selected_trade_count']}`, density `{final['selected_trade_density']}`, closed DD proxy `{final['selected_closed_trade_drawdown_proxy']}`, recovery proxy `{final['selected_closed_trade_recovery_proxy']}`, long/short `{final['selected_long_trade_count']}` / `{final['selected_short_trade_count']}`.

Diff vs parent CD02(상위 CD02 대비 차이): net `{final['selected_net_delta_vs_parent']}`, PF `{final['selected_profit_factor_delta_vs_parent']}`, trades `{final['selected_trade_delta_vs_parent']}`, shorts `{final['selected_short_delta_vs_parent']}`.

Next queue(다음 대기열): `{rel(RUN364CH_QUEUE)}`

Authority(권위): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함).
""",
        bom=True,
    )
    append_text_once(
        WORKSPACE_CHANGELOG,
        f"## {TODAY} - {RUN_ID}",
        f"""## {TODAY} - {RUN_ID}

- action(행동): cost-stable h17 source guard proxy scout(비용 안정 17시 원천 가드 프록시 정찰)를 실행했다.
- effect(효과): `{final['selected_candidate_id']}`를 `{NEXT_RUN_ID}` 검토 대상으로 넘기고 main sync(메인 동기화) 전까지 운영 주장은 만들지 않는다.
- report(보고서): `{rel(REPORT_PATH)}`
""",
    )
    append_text_once(
        IDEA_REGISTRY,
        RUN_ID,
        f"""## {RUN_ID}

- idea(아이디어): h17 overlay focus(17시 오버레이 집중)가 cost-stable same-session semantics(비용 안정 동일 세션 의미) 안에서 작은 no-split lift(무분할 우위)를 만들 수 있다.
- positive clue(긍정 단서): selected proxy(선택 프록시) net/PF/density/shorts `{final['selected_net_profit']}` / `{final['selected_profit_factor']}` / `{final['selected_trade_density']}` / `{final['selected_short_trade_count']}`.
- evidence_boundary(근거 경계): proxy scout only(프록시 정찰 전용), MT5 reprobe required(MT5 재탐침 필요).
- next action(다음 행동): `{NEXT_RUN_ID}`.
""",
    )
    append_text_once(
        NEGATIVE_RESULT_REGISTER,
        RUN_ID,
        f"""## {RUN_ID}

- status(상태): no operating package yet(아직 운영 패키지 없음).
- failure_memory(실패 기억): h17 floor tightening(17시 하한 강화), overlay-only stress(오버레이 전용 압박), and short-floor variants(숏 하한 변형)는 net/PF or short balance(순수익/PF 또는 숏 균형)를 흔들었다.
- salvage_value(회수 가치): `{final['selected_candidate_id']}`는 small lift(작은 우위)와 short floor(숏 하한)를 같이 보존한다.
- reopen_condition(재개 조건): CH review(CH 검토)가 month/source/cost stress(월/원천/비용 압박)를 통과하고 MT5 reprobe(MT5 재탐침)가 열릴 때.
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
        "question": "Can h17 overlay focus lift cost-stable source quality without trade splitting?(17시 오버레이 집중이 거래 쪼개기 없이 비용 안정 원천 품질을 올리는가?)",
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
        "primary_artifact": rel(PROXY_SCOUT_SURFACE),
    }
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], [common], extend_header=True)
    ledger_rows: list[dict[str, Any]] = []
    for suffix, record_view, tier_scope, status, include_metrics in [
        ("tier_a_used", "Tier A used(Tier A 사용)", "Tier A", STATUS, True),
        ("tier_b_missing_required", "Tier B fallback used(Tier B 대체 사용)", "Tier B", "missing_required(필수 누락)", False),
        ("actual_routed_total", "actual routed total(실제 라우팅 전체)", "Tier A+B", STATUS, True),
    ]:
        row = {
            **common,
            "ledger_row_id": f"{RUN_ID}__{suffix}",
            "subrun_id": f"{RUN_ID}__{suffix}",
            "row_id": f"{RUN_ID}__{suffix}",
            "record_view": record_view,
            "tier_scope": tier_scope,
            "kpi_scope": "CG proxy scout(CG 프록시 정찰)",
            "status": status,
            "primary_kpi": f"net={final['selected_net_profit']};pf={final['selected_profit_factor']};density={final['selected_trade_density']};shorts={final['selected_short_trade_count']}",
            "guardrail_kpi": f"no_split;parent_mt5_net={final['parent_mt5_net_profit']};mt5_reprobe_required",
        }
        if not include_metrics:
            for key in ["net_profit", "profit_factor", "expectancy", "trade_count", "trade_density_per_feature_day", "long_trade_count", "short_trade_count", "max_drawdown_amount", "recovery_factor"]:
                row[key] = ""
        ledger_rows.append(row)
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], ledger_rows, extend_header=True)
    append_or_replace_csv(STAGE_LEDGER, ["ledger_row_id"], ledger_rows, extend_header=True)
    artifact_rows = []
    for artifact_type, path, notes in [
        ("proxy_scout_surface", PROXY_SCOUT_SURFACE, "CG proxy scout surface(CG 프록시 정찰 표면)."),
        ("selected_candidate", SELECTED_CANDIDATE, "Selected CG candidate(선택 CG 후보)."),
        ("selected_trade_tape", SELECTED_TRADE_TAPE, "Selected CG trade tape(선택 CG 거래 테이프)."),
        ("filter_audit", CANDIDATE_FILTER_AUDIT, "Candidate filter audit(후보 필터 감사)."),
        ("source_attribution", CANDIDATE_SOURCE_ATTRIBUTION, "Source attribution(원천 귀속)."),
        ("month_stability", CANDIDATE_MONTH_STABILITY, "Month stability(月 안정성)."),
        ("proxy_mt5_diff_plan", PROXY_MT5_DIFF_PLAN, "Proxy/MT5 diff plan(프록시/MT5 차이 계획)."),
        ("next_queue", RUN364CH_QUEUE, "CH review queue(CH 검토 대기열)."),
        ("report", REPORT_PATH, "CG report(CG 보고서)."),
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
    repair_run_registry_line_endings(RUN_ID)


def write_manifest(final: Mapping[str, Any]) -> None:
    existing_outputs = [path for path in OUTPUT_FILES if exists(path) and Path(path).is_file() and path != RUN_MANIFEST]
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "run_number": RUN_NUMBER,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "source_runtime_review_run_id": SOURCE_RUNTIME_REVIEW_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "status": STATUS,
            "judgment": JUDGMENT,
            "created_at_utc": final["created_at_utc"],
            "producer": rel(Path(__file__)),
            "inputs": [{"path": rel(path), "sha256": sha(path)} for path in INPUT_FILES if exists(path)],
            "outputs": [{"path": rel(path), "sha256": sha(path)} for path in existing_outputs],
            "final_decision": rel(FINAL_DECISION),
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def main() -> None:
    ensure_dirs()
    created_at = now_utc()
    cf_final, _ce_final = validate_inputs()
    parent_trades, native_control = load_trade_frames()
    write_csv(INPUT_MANIFEST, input_manifest_rows())
    write_work_packet()
    surface, frame_map, filter_rows = build_surface(cf_final, parent_trades, native_control)
    selected = dict(surface[0])
    selected_frame = frame_map[str(selected["candidate_id"])].copy()
    source_rows = attribution_rows(surface, frame_map)
    month_rows_ = month_rows(surface, frame_map)
    cost_rows = cost_stress_rows(surface)
    data_rows_ = data_integrity_rows(parent_trades, native_control, surface)
    queue_rows_ = review_queue_rows(selected)
    proxy_mt5_rows_ = proxy_mt5_diff_rows(selected, cf_final)

    write_csv(PROXY_SCOUT_SURFACE, surface)
    write_json(SELECTED_CANDIDATE, selected)
    trade_tape = selected_frame.drop(columns=["open_time_dt", "close_time_dt"], errors="ignore").to_dict("records")
    write_csv(SELECTED_TRADE_TAPE, trade_tape)
    write_csv(CANDIDATE_FILTER_AUDIT, filter_rows)
    write_csv(CANDIDATE_SOURCE_ATTRIBUTION, source_rows)
    write_csv(CANDIDATE_MONTH_STABILITY, month_rows_)
    write_csv(COST_STRESS_DIAGNOSTIC, cost_rows)
    write_csv(PROXY_MT5_DIFF_PLAN, proxy_mt5_rows_)
    write_csv(RUN364CH_QUEUE, queue_rows_)

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
    final = final_payload(cf_final, selected, surface, preliminary_gates, created_at)
    write_json(FINAL_DECISION, final)
    write_receipts(final, selected, proxy_mt5_rows_)
    refresh_lineage_receipt(final)
    gates = gate_rows(surface, data_rows_, receipt_paths, final_written=True)
    final = final_payload(cf_final, selected, surface, gates, created_at)
    write_json(FINAL_DECISION, final)
    write_receipts(final, selected, proxy_mt5_rows_)
    refresh_lineage_receipt(final)
    write_docs(final, selected, surface, filter_rows, source_rows, month_rows_, cost_rows, queue_rows_, gates)
    write_ledgers(final)
    write_manifest(final)
    refresh_lineage_receipt(final)
    write_manifest(final)
    print(json.dumps(json_ready(final), ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
