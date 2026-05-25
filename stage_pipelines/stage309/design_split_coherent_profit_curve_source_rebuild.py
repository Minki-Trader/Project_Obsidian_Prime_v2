from __future__ import annotations

import csv
import hashlib
import json
import sys
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane import ledger  # noqa: E402
from foundation.models.onnx_bridge import ordered_hash  # noqa: E402
from stage_pipelines.stage308 import design_non_return_rank_profit_source_rebuild as s308  # noqa: E402


STAGE_ID = "309_onnx_candidate_campaign__split_coherent_profit_curve_source_rebuild"
RUN_ID = "run309A_design_split_coherent_profit_curve_source_rebuild_packet_v1"
RUN_NUMBER = "run309A"
SOURCE_STAGE_ID = "308_onnx_candidate_campaign__non_return_rank_profit_source_rebuild"
SOURCE_RUN_ID = "run308C_review_non_return_rank_profit_source_mt5_probe_v1"
UPDATED_ON = "2026-05-24"
STATUS = "completed_split_coherent_profit_curve_source_candidates_materialized_no_selection"
JUDGMENT = "split_coherent_profit_curve_source_surfaces_materialized_no_candidate_selection"
NEXT_ACTION = "run309B_execute_split_coherent_profit_curve_source_mt5_probe"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_"
    "no_deployment_no_onnx_until_candidate_package_gate"
)

STAGE_ROOT = ROOT / "stages" / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER
REVIEWS = STAGE_ROOT / "03_reviews"
SELECTED = STAGE_ROOT / "04_selected" / "selection_status.md"
REVIEW_INDEX = REVIEWS / "review_index.md"
STAGE_LEDGER = REVIEWS / "stage_run_ledger.csv"
PAYLOAD_DIR = RUN_ROOT / "payloads"
HANDOFF_DIR = RUN_ROOT / "handoff"
MODEL_DIR = RUN_ROOT / "models"

SOURCE_STAGE = ROOT / "stages" / SOURCE_STAGE_ID
SOURCE_RUN308C = SOURCE_STAGE / "02_runs" / "run308C"
SOURCE_SCOREBOARD = SOURCE_RUN308C / "non_return_rank_profit_source_review_scoreboard.csv"
SOURCE_FAILURE_MEMORY = SOURCE_RUN308C / "failure_memory.csv"
SOURCE_CURVE = SOURCE_RUN308C / "curve_quality_summary.csv"
SOURCE_SEED_QUEUE = SOURCE_RUN308C / "stage309_seed_queue.csv"
SOURCE_REVIEW = SOURCE_STAGE / "03_reviews" / "run308C_review_stage309_open.md"

BRANCH_QUEUE = RUN_ROOT / "branch_design_queue.csv"
MODEL_SCOREBOARD = RUN_ROOT / "model_scout_scoreboard.csv"
CANDIDATE_SUPPLY = RUN_ROOT / "candidate_supply_diagnostics.csv"
PAYLOAD_MANIFEST = RUN_ROOT / "candidate_payload_manifest.csv"
MT5_QUEUE = RUN_ROOT / "mt5_probe_queue.csv"
MODEL_MANIFEST = RUN_ROOT / "model_artifact_manifest.csv"
WFO_FOLD_SCOREBOARD = RUN_ROOT / "wfo_fold_scoreboard.csv"
EXPERIMENT_DESIGN = RUN_ROOT / "experiment_design_receipt.json"
DATA_RECEIPT = RUN_ROOT / "data_integrity_receipt.json"
RESULT_JUDGMENT = RUN_ROOT / "result_judgment.csv"
GATE_AUDIT = RUN_ROOT / "required_gate_coverage_audit.csv"
RUN_MANIFEST = RUN_ROOT / "run_manifest.json"
LINEAGE = RUN_ROOT / "artifact_lineage_receipt.json"
REPORT = REVIEWS / "run309A_materialization.md"

RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
IDEA_REGISTER = ROOT / "docs" / "registers" / "idea_registry.md"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"

RUNTIME_FEATURE_ORDER = ("route_signal_value",)
DECISION_FEATURES = s308.DECISION_FEATURES + (
    "split_coherent_score",
    "validation_curve_guard_score",
    "trend_breadth_confirmation_score",
)

MANIFEST_COLUMNS = (
    "queue_id",
    "materialized_branch_id",
    "stage309_branch_id",
    "stage308_branch_id",
    "stage307_branch_id",
    "stage306_branch_id",
    "package_id",
    "queue_role",
    "payload_path",
    "payload_hash",
    "handoff_path",
    "handoff_hash",
    "model_artifact_path",
    "model_artifact_hash",
    "model_feature_order_path",
    "model_feature_order_hash",
    "direction_surface_hash",
    "direction_feature_order_hash",
    "max_hold_bars",
    "close_on_flat_signal",
    "same_direction_reentry_cooldown_bars",
    "atr_sltp_enabled",
    "atr_period",
    "atr_stop_multiplier",
    "atr_take_profit_multiplier",
    "atr_min_stop_points",
    "atr_max_stop_points",
    "atr_min_take_profit_points",
    "atr_max_take_profit_points",
    "exit_risk_overlay_enabled",
    "exit_risk_close_long_feature_index",
    "exit_risk_close_short_feature_index",
    "exit_risk_close_threshold",
    "exit_risk_min_hold_bars",
    "exit_risk_max_hold_feature_index",
    "model_risk_sizing_enabled",
    "model_risk_min_pct",
    "model_risk_max_pct",
    "model_risk_confidence_floor",
    "model_risk_confidence_ceiling",
    "model_risk_fallback_lot",
    "fixed_lot",
    "approx_validation_trades_per_day",
    "approx_oos_trades_per_day",
    "selected_candidate",
    "adapter_package",
    "onnx_readiness",
    "claim_boundary",
)

BRANCH_COLUMNS = (
    "branch_id",
    "package_id",
    "source_stage_id",
    "source_run_id",
    "hypothesis",
    "decision_use",
    "comparison_baseline",
    "control_variables",
    "changed_variables",
    "sample_scope",
    "success_criteria",
    "failure_criteria",
    "invalid_conditions",
    "stop_conditions",
    "evidence_plan",
    "feature_surface",
    "model_surface",
    "decision_surface",
    "risk_logic",
    "adapter_path",
    "runtime_handoff",
    "failure_memory_plan",
    "claim_boundary",
)

SCOREBOARD_COLUMNS = (
    "materialized_branch_id",
    "package_id",
    "model_family",
    "prediction_kind",
    "mode",
    "validation_proxy_net_bp",
    "validation_proxy_pf",
    "validation_proxy_trade_count",
    "validation_proxy_trades_per_day",
    "validation_proxy_recovery",
    "validation_proxy_worst_month_bp",
    "validation_proxy_worst_rolling_20_bp",
    "validation_proxy_worst_rolling_50_bp",
    "validation_proxy_positive_month_share",
    "oos_proxy_net_bp",
    "oos_proxy_pf",
    "oos_proxy_trade_count",
    "oos_proxy_trades_per_day",
    "oos_proxy_recovery",
    "oos_proxy_worst_month_bp",
    "oos_proxy_worst_rolling_20_bp",
    "oos_proxy_worst_rolling_50_bp",
    "oos_proxy_positive_month_share",
    "density_gate",
    "proxy_edge_gate",
    "curve_proxy_gate",
    "selection_score",
    "selected_candidate",
    "adapter_package",
    "onnx_readiness",
    "claim_boundary",
)

SUPPLY_COLUMNS = (
    "materialized_branch_id",
    "package_id",
    "tier_scope",
    "split",
    "rows",
    "days",
    "active_signal_count",
    "long_signal_count",
    "short_signal_count",
    "active_signals_per_day",
    "approx_trade_count",
    "approx_trades_per_day",
    "max_hold_bars",
    "trade_density_screen",
)

WFO_COLUMNS = (
    "materialized_branch_id",
    "package_id",
    "fold_id",
    "mode",
    "net_bp",
    "pf",
    "trade_count",
    "trades_per_day",
    "recovery",
    "worst_month_bp",
    "worst_rolling_20_bp",
    "worst_rolling_50_bp",
    "positive_month_share",
    "underwater_ratio",
)

MODEL_COLUMNS = (
    "materialized_branch_id",
    "package_id",
    "model_family",
    "prediction_kind",
    "dataset_id",
    "model_artifact_path",
    "model_artifact_hash",
    "model_feature_order_path",
    "model_feature_order_hash",
    "classes",
    "payoff_weight_policy",
    "onnx_exportability_note",
)

RESULT_COLUMNS = (
    "result_subject",
    "evidence_available",
    "evidence_missing",
    "judgment_label",
    "judgment_class",
    "claim_boundary",
    "next_condition",
    "user_explanation_hook",
)

GATE_COLUMNS = ("gate_name", "status", "evidence_path", "effect")

RUN_REGISTRY_COLUMNS = ("run_id", "stage_id", "lane", "status", "judgment", "path", "notes")
STAGE_LEDGER_COLUMNS = (
    "row_id",
    "stage_id",
    "run_id",
    "view",
    "tier_scope",
    "scoreboard",
    "status",
    "judgment",
    "evidence_boundary",
    "report_path",
    "notes",
)
ARTIFACT_COLUMNS = (
    "artifact_id",
    "artifact_type",
    "path",
    "sha256",
    "stage_id",
    "run_id",
    "created_at_utc",
    "notes",
)


@dataclass(frozen=True)
class CandidateSpec:
    package_id: str
    decision_surface: str
    target_density: float
    max_hold_bars: int
    fixed_lot: float
    atr_stop_multiplier: float
    atr_take_profit_multiplier: float
    model_risk_sizing_enabled: bool
    model_risk_max_pct: float
    hypothesis: str
    changed_variables: str
    close_on_flat_signal: bool = True
    same_direction_reentry_cooldown_bars: int = 0
    atr_sltp_enabled: bool = True
    atr_period: int = 14
    model_risk_min_pct: float = 0.006
    model_risk_confidence_floor: float = 0.54
    model_risk_confidence_ceiling: float = 0.99
    model_risk_fallback_lot: float = 0.10


def candidate_specs() -> list[CandidateSpec]:
    return [
        CandidateSpec(
            package_id="cp309A_validation_curve_trend_guard_density50_hold5_surface",
            decision_surface="validation_curve_trend_guard",
            target_density=5.0,
            max_hold_bars=5,
            fixed_lot=0.30,
            atr_stop_multiplier=1.35,
            atr_take_profit_multiplier=4.70,
            model_risk_sizing_enabled=True,
            model_risk_max_pct=0.030,
            hypothesis="Trend quality source(추세 품질 원천)에 smooth/quality guard(완만함/품질 보호문)를 붙이면 validation(검증) 곡선 포켓을 줄이면서 OOS(표본외) 상방을 보존할 수 있다.",
            changed_variables="cp308E clue(308E 단서)를 candidate(후보)로 보존하지 않고, shock guard(충격 보호문), shorter hold(짧은 보유), lower risk(낮은 위험)로 재구성한다.",
            close_on_flat_signal=False,
            same_direction_reentry_cooldown_bars=2,
        ),
        CandidateSpec(
            package_id="cp309B_defensive_curve_quality_density60_hold4_surface",
            decision_surface="defensive_curve_quality",
            target_density=6.0,
            max_hold_bars=4,
            fixed_lot=0.25,
            atr_stop_multiplier=1.18,
            atr_take_profit_multiplier=3.80,
            model_risk_sizing_enabled=True,
            model_risk_max_pct=0.024,
            hypothesis="Defensive curve quality(방어형 곡선 품질) 표면은 순수익을 조금 덜어도 local pocket(국소 포켓)을 먼저 줄일 수 있다.",
            changed_variables="smooth_curve/profit_quality(완만한 곡선/수익 품질) 우선, tighter ATR(더 좁은 평균진폭), hold4(4봉 보유).",
        ),
        CandidateSpec(
            package_id="cp309C_trend_breadth_confirmation_density55_hold5_surface",
            decision_surface="trend_breadth_confirmation",
            target_density=5.5,
            max_hold_bars=5,
            fixed_lot=0.30,
            atr_stop_multiplier=1.42,
            atr_take_profit_multiplier=4.90,
            model_risk_sizing_enabled=True,
            model_risk_max_pct=0.031,
            hypothesis="Trend(추세)와 breadth confirmation(시장 폭 확인)이 같은 방향일 때만 진입하면 split coherence(분할 일관성)가 좋아질 수 있다.",
            changed_variables="trend/breadth/macro(추세/시장폭/거시) 확인, density 5.5/day(일 5.5거래), hold5(5봉 보유).",
            close_on_flat_signal=False,
            same_direction_reentry_cooldown_bars=1,
        ),
        CandidateSpec(
            package_id="cp309D_open_mid_reversion_curve_floor_density80_hold3_surface",
            decision_surface="open_mid_reversion_curve_floor",
            target_density=8.0,
            max_hold_bars=3,
            fixed_lot=0.21,
            atr_stop_multiplier=1.05,
            atr_take_profit_multiplier=3.20,
            model_risk_sizing_enabled=False,
            model_risk_max_pct=0.0,
            hypothesis="Open/mid reversion(초반/중반 되돌림)으로 거래 수를 확보하면서 curve floor(곡선 바닥)를 방어할 수 있다.",
            changed_variables="return/bollinger reversion(수익률/볼린저 되돌림), high density(높은 밀도), fixed risk(고정 위험).",
        ),
        CandidateSpec(
            package_id="cp309E_aggressive_oos_scale_trend_reallocation_density45_hold8_surface",
            decision_surface="aggressive_oos_scale_trend_reallocation",
            target_density=4.5,
            max_hold_bars=8,
            fixed_lot=0.34,
            atr_stop_multiplier=1.58,
            atr_take_profit_multiplier=5.80,
            model_risk_sizing_enabled=True,
            model_risk_max_pct=0.036,
            hypothesis="Aggressive trend reallocation(공격형 추세 재배치)은 cp308E(308E 후보)의 OOS(표본외) 수익 규모를 더 선명하게 만들 수 있다.",
            changed_variables="higher payoff target(높은 보상 목표), lower density(낮은 밀도), shock cap(충격 상한), hold8(8봉 보유).",
            close_on_flat_signal=False,
            same_direction_reentry_cooldown_bars=3,
        ),
        CandidateSpec(
            package_id="cp309F_session_balanced_dual_source_density70_hold4_surface",
            decision_surface="session_balanced_dual_source",
            target_density=7.0,
            max_hold_bars=4,
            fixed_lot=0.24,
            atr_stop_multiplier=1.15,
            atr_take_profit_multiplier=3.70,
            model_risk_sizing_enabled=True,
            model_risk_max_pct=0.025,
            hypothesis="Session balanced dual source(세션 균형 이중 원천)는 한 세션 포켓에 빠지는 위험을 줄일 수 있다.",
            changed_variables="trend/breadth/reversion(추세/시장폭/되돌림)을 세션별로 혼합하고 density 7/day(일 7거래)를 목표로 한다.",
        ),
    ]


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def path_exists(path: Path) -> bool:
    try:
        return ledger.path_exists(path)
    except OSError:
        return path.exists()


def rel(path: Path | str) -> str:
    item = Path(str(path))
    try:
        return item.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return item.as_posix()


def read_text(path: Path) -> str:
    if not path_exists(path):
        return ""
    try:
        return ledger.io_path(path).read_text(encoding="utf-8-sig")
    except OSError:
        return path.read_text(encoding="utf-8-sig")


def write_text(path: Path, text: str) -> None:
    try:
        ledger.io_path(path.parent).mkdir(parents=True, exist_ok=True)
        ledger.io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig", newline="\n")
        return
    except OSError:
        pass
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8-sig", newline="\n")


def write_json(path: Path, payload: Any, *, bom: bool = False) -> None:
    encoding = "utf-8-sig" if bom else "utf-8"
    write_text(path, json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    if not bom:
        try:
            ledger.io_path(path).write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding=encoding)
        except OSError:
            path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding=encoding)


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> None:
    try:
        ledger.write_csv_rows(path, columns, rows)
        return
    except OSError:
        pass
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: row.get(column, "") for column in columns})


def read_csv_dicts(path: Path) -> list[dict[str, str]]:
    if not path_exists(path):
        return []
    try:
        return ledger.read_csv_rows(path)
    except OSError:
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            return [dict(row) for row in csv.DictReader(handle)]


def safe_upsert(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]], key: str) -> None:
    try:
        ledger.upsert_csv_rows(path, columns, rows, key=key)
        return
    except OSError:
        pass
    existing = read_csv_dicts(path)
    incoming = {str(row.get(key, "")): row for row in rows}
    merged = [row for row in existing if str(row.get(key, "")) not in incoming]
    merged.extend(rows)
    write_csv(path, columns, merged)


def sha256_file(path: Path) -> str:
    try:
        return ledger.sha256_file_lf_normalized(path)
    except OSError:
        return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def replace_line_prefix(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + replacement + "\n"


def append_once(text: str, marker: str, addition: str) -> str:
    return text if marker in text else text.rstrip() + "\n\n" + addition.rstrip() + "\n"


def prepend_focus(text: str, focus: str, marker: str) -> str:
    if marker in text:
        return text
    needle = "current_focus:\n"
    if needle in text:
        return text.replace(needle, needle + focus, 1)
    return text.rstrip() + "\ncurrent_focus:\n" + focus


def ncol(frame: pd.DataFrame, column: str, default: float = 0.0) -> np.ndarray:
    return s308.ncol(frame, column, default)


def zscore(values: np.ndarray) -> np.ndarray:
    return s308.zscore(values)


def positive(values: np.ndarray) -> np.ndarray:
    return s308.positive(values)


def add_stage309_features(frame: pd.DataFrame) -> pd.DataFrame:
    out = s308.add_time_features(frame)
    shock = s308.shock_score(out)
    quality = zscore(ncol(out, "profit_quality_score"))
    smooth = zscore(ncol(out, "smooth_curve_score"))
    trend = zscore(ncol(out, "ema20_ema50_diff")) + 0.55 * zscore(ncol(out, "di_spread_14")) + 0.35 * zscore(ncol(out, "ppo_hist_12_26_9"))
    breadth = zscore(ncol(out, "mega8_pos_breadth_1")) + 0.45 * zscore(ncol(out, "top3_weighted_return_1"))
    out["split_coherent_score"] = positive(quality) + positive(smooth) + 0.25 * np.abs(trend) - 0.70 * shock
    out["validation_curve_guard_score"] = positive(smooth) + 0.55 * positive(quality) - 0.90 * shock
    out["trend_breadth_confirmation_score"] = np.sign(trend) * np.sign(breadth) * np.minimum(np.abs(trend), np.abs(breadth))
    return out


def risk_manifest_fields(spec: CandidateSpec) -> dict[str, Any]:
    return {
        "atr_sltp_enabled": int(spec.atr_sltp_enabled),
        "atr_period": spec.atr_period,
        "atr_stop_multiplier": spec.atr_stop_multiplier,
        "atr_take_profit_multiplier": spec.atr_take_profit_multiplier,
        "atr_min_stop_points": 0.0,
        "atr_max_stop_points": 0.0,
        "atr_min_take_profit_points": 0.0,
        "atr_max_take_profit_points": 0.0,
        "exit_risk_overlay_enabled": 0,
        "exit_risk_close_long_feature_index": -1,
        "exit_risk_close_short_feature_index": -1,
        "exit_risk_close_threshold": 0.5,
        "exit_risk_min_hold_bars": 0,
        "exit_risk_max_hold_feature_index": -1,
        "model_risk_sizing_enabled": int(spec.model_risk_sizing_enabled),
        "model_risk_min_pct": spec.model_risk_min_pct,
        "model_risk_max_pct": spec.model_risk_max_pct,
        "model_risk_confidence_floor": spec.model_risk_confidence_floor,
        "model_risk_confidence_ceiling": spec.model_risk_confidence_ceiling,
        "model_risk_fallback_lot": spec.model_risk_fallback_lot,
        "fixed_lot": spec.fixed_lot,
    }


def signal_for_spec(spec: CandidateSpec, frame: pd.DataFrame) -> tuple[np.ndarray, np.ndarray]:
    outside, cash_open, mid, late = s308.session_arrays(frame)
    minutes = ncol(frame, "minutes_from_cash_open")
    shock = s308.shock_score(frame)
    quality = zscore(ncol(frame, "profit_quality_score"))
    scale = zscore(ncol(frame, "profit_scale_score"))
    smooth = zscore(ncol(frame, "smooth_curve_score"))
    trend = zscore(ncol(frame, "ema20_ema50_diff")) + 0.55 * zscore(ncol(frame, "di_spread_14")) + 0.35 * zscore(ncol(frame, "ppo_hist_12_26_9"))
    adx = positive(zscore(ncol(frame, "adx_14", 20.0)))
    breadth = zscore(ncol(frame, "mega8_pos_breadth_1")) + 0.50 * zscore(ncol(frame, "top3_weighted_return_1"))
    ret = zscore(ncol(frame, "return_zscore_20"))
    bb = zscore(ncol(frame, "bb_position_20", 0.5) - 0.5)
    base = s308.base_direction(frame).astype("float64")
    coherent = ncol(frame, "split_coherent_score")
    guard = ncol(frame, "validation_curve_guard_score")
    confirm = ncol(frame, "trend_breadth_confirmation_score")

    if spec.decision_surface == "validation_curve_trend_guard":
        raw = trend
        score = np.abs(raw) + 0.90 * adx + 0.80 * guard + 0.35 * positive(scale) - 0.55 * shock
        keep = (score > np.nanpercentile(score, 50)) & (shock < np.nanpercentile(shock, 78))
    elif spec.decision_surface == "defensive_curve_quality":
        raw = base
        score = 1.25 * positive(smooth) + 0.85 * positive(quality) + 0.35 * mid + 0.20 * cash_open - 0.95 * shock
        keep = (score > np.nanpercentile(score, 40)) & (shock < np.nanpercentile(shock, 72))
    elif spec.decision_surface == "trend_breadth_confirmation":
        raw = trend + 0.55 * breadth
        score = np.abs(raw) + 0.95 * positive(confirm) + 0.35 * coherent - 0.50 * shock
        keep = (score > np.nanpercentile(score, 47)) & (confirm > np.nanpercentile(confirm, 35))
    elif spec.decision_surface == "open_mid_reversion_curve_floor":
        raw = -(0.70 * ret + 0.60 * bb)
        open_mid = (((minutes >= 20) & (minutes <= 300)).astype("float64") + 0.65 * mid + 0.25 * cash_open)
        score = np.abs(raw) + 0.70 * open_mid + 0.45 * positive(guard) - 0.65 * shock
        keep = (score > np.nanpercentile(score, 25)) & (outside < 0.5)
    elif spec.decision_surface == "aggressive_oos_scale_trend_reallocation":
        raw = trend + 0.25 * breadth
        score = np.abs(raw) + 0.95 * adx + 0.75 * positive(scale) + 0.45 * late + 0.20 * mid - 0.40 * shock
        keep = (score > np.nanpercentile(score, 56)) & (shock < np.nanpercentile(shock, 85))
    elif spec.decision_surface == "session_balanced_dual_source":
        reversion = -(0.55 * ret + 0.45 * bb)
        raw = np.where(mid + late > 0.0, trend + 0.35 * breadth, reversion)
        session_balance = 0.45 * cash_open + 0.65 * mid + 0.50 * late
        score = np.abs(raw) + 0.45 * session_balance + 0.40 * positive(coherent) - 0.55 * shock
        keep = score > np.nanpercentile(score, 33)
    else:
        raise ValueError(f"unsupported decision_surface: {spec.decision_surface}")

    signal = np.sign(raw).astype("int8")
    signal = np.where(keep, signal, 0).astype("int8")
    signal = s308.s307.prev.s294.trim_to_density(frame, signal, np.asarray(score, dtype="float64"), spec.max_hold_bars, spec.target_density)
    return signal.astype("int8"), np.asarray(score, dtype="float64")


def source_stage308_seed() -> str:
    rows = read_csv_dicts(SOURCE_SEED_QUEUE)
    return rows[0].get("seed_id", "stage308_preserved_clue") if rows else "stage308_preserved_clue"


def materialize_payload(spec: CandidateSpec, base: pd.DataFrame, seed: Mapping[str, str], stage308_seed: str, frame: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, Any], dict[str, Any], dict[str, Any]]:
    signal, score = signal_for_spec(spec, frame)
    branch_id = f"run309A_{spec.package_id.replace('_surface', '')}"
    payload = base.copy()
    payload["stage309_branch_id"] = branch_id
    payload["stage308_branch_id"] = stage308_seed
    payload["stage307_branch_id"] = seed.get("stage307_branch_id", "")
    payload["stage306_branch_id"] = seed.get("materialized_branch_id", "")
    payload["materialized_branch_id"] = branch_id
    payload["package_id"] = spec.package_id
    payload["queue_role"] = "split_coherent_profit_curve_source_surface"
    payload["candidate_decision_score"] = score
    payload["split_coherent_score_value"] = score
    payload["direction_signal_value"] = signal
    payload["route_signal_value"] = signal
    payload["route_signal_label"] = [s308.s307.prev.s290.signal_label(int(value)) for value in signal]
    payload["signal_active"] = (signal != 0).astype("int8")
    payload["model_risk_pct"] = spec.model_risk_max_pct if spec.model_risk_sizing_enabled else 0.0
    payload["max_hold_bars"] = spec.max_hold_bars
    payload["close_on_flat_signal"] = spec.close_on_flat_signal
    payload["same_direction_reentry_cooldown_bars"] = spec.same_direction_reentry_cooldown_bars
    identity = {
        "package_id": spec.package_id,
        "source_stage_id": SOURCE_STAGE_ID,
        "source_run_id": SOURCE_RUN_ID,
        "decision_surface": spec.decision_surface,
        "target_density": spec.target_density,
        "max_hold_bars": spec.max_hold_bars,
        "runtime_feature_order": list(RUNTIME_FEATURE_ORDER),
        "model_feature_order": list(DECISION_FEATURES),
        "model_feature_order_hash": ordered_hash(DECISION_FEATURES),
        "risk_logic": risk_manifest_fields(spec),
        "claim_boundary": BOUNDARY,
    }
    surface_hash = hashlib.sha256(json.dumps(identity, sort_keys=True).encode("utf-8")).hexdigest()
    payload["direction_surface_hash"] = surface_hash
    payload["variant_decision_surface_hash"] = surface_hash
    payload["direction_feature_order_hash"] = ordered_hash(RUNTIME_FEATURE_ORDER)
    payload["model_feature_order_hash"] = ordered_hash(DECISION_FEATURES)
    payload["payload_claim_boundary"] = BOUNDARY
    validation_metrics = s308.s307.prev.metrics_for_payload(spec, payload, "validation")
    oos_metrics = s308.s307.prev.metrics_for_payload(spec, payload, "oos")
    drop_columns = [name for name in payload.columns if name.startswith(("label", "future_")) or name in {"label_class", "evaluation_label_available"}]
    payload = payload.drop(columns=drop_columns, errors="ignore")
    return payload, identity | {"direction_surface_hash": surface_hash}, validation_metrics, oos_metrics


def supply_rows_for_payload(payload: pd.DataFrame, spec: CandidateSpec) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    frame = payload.copy()
    frame["date"] = pd.to_datetime(frame["timestamp"], utc=True).dt.date.astype(str)
    for (tier_scope, split), part in frame.groupby(["tier_scope", "split"], observed=True):
        active = part.loc[pd.to_numeric(part["route_signal_value"], errors="coerce").fillna(0).ne(0)]
        days = max(1, int(part["date"].nunique()))
        approx_trade_count = int(len(active) / max(1, spec.max_hold_bars))
        approx_tpd = approx_trade_count / days
        rows.append(
            {
                "materialized_branch_id": str(part["materialized_branch_id"].iloc[0]),
                "package_id": spec.package_id,
                "tier_scope": tier_scope,
                "split": split,
                "rows": len(part),
                "days": days,
                "active_signal_count": len(active),
                "long_signal_count": int((pd.to_numeric(part["route_signal_value"], errors="coerce").fillna(0) > 0).sum()),
                "short_signal_count": int((pd.to_numeric(part["route_signal_value"], errors="coerce").fillna(0) < 0).sum()),
                "active_signals_per_day": len(active) / days,
                "approx_trade_count": approx_trade_count,
                "approx_trades_per_day": approx_tpd,
                "max_hold_bars": spec.max_hold_bars,
                "trade_density_screen": "passed" if 4.0 <= approx_tpd <= 10.0 else "failed",
            }
        )
    return rows


def gate_label(validation: Mapping[str, Any], oos: Mapping[str, Any], gate: str) -> str:
    return s308.s307.prev.gate_label(validation, oos, gate)


def build_outputs() -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[Path]]:
    base, seed = s308.s307.base_payload()
    frame = add_stage309_features(base)
    stage308_seed = source_stage308_seed()
    branch_rows: list[dict[str, Any]] = []
    scoreboard_rows: list[dict[str, Any]] = []
    supply_rows: list[dict[str, Any]] = []
    manifest_rows: list[dict[str, Any]] = []
    model_rows: list[dict[str, Any]] = []
    wfo_rows: list[dict[str, Any]] = []
    artifacts: list[Path] = []
    for index, spec in enumerate(candidate_specs(), start=1):
        payload, identity, validation_metrics, oos_metrics = materialize_payload(spec, base, seed, stage308_seed, frame)
        branch_id = f"run309A_{spec.package_id.replace('_surface', '')}"
        payload_path = PAYLOAD_DIR / f"{branch_id}_payload.parquet"
        handoff_path = HANDOFF_DIR / f"{branch_id}_handoff.json"
        model_spec_path = MODEL_DIR / f"{branch_id}_rule_surface.json"
        ledger.io_path(payload_path.parent).mkdir(parents=True, exist_ok=True)
        payload.to_parquet(ledger.io_path(payload_path), index=False)
        write_json(model_spec_path, identity)
        write_json(
            handoff_path,
            {
                "stage309_branch_id": branch_id,
                "stage308_seed_id": stage308_seed,
                "source_stage_id": SOURCE_STAGE_ID,
                "package_id": spec.package_id,
                "runtime_feature_order": list(RUNTIME_FEATURE_ORDER),
                "runtime_feature_order_hash": ordered_hash(RUNTIME_FEATURE_ORDER),
                "model_feature_order": list(DECISION_FEATURES),
                "model_feature_order_hash": ordered_hash(DECISION_FEATURES),
                "decision_surface": identity,
                "risk_logic": risk_manifest_fields(spec),
                "runtime_handoff": "precomputed route_signal_value replay for Stage309 MT5 probe(309단계 MT5 탐침)",
                "claim_boundary": BOUNDARY,
            },
        )
        candidate_supply = supply_rows_for_payload(payload, spec)
        supply_rows.extend(candidate_supply)
        val_supply = next(row for row in candidate_supply if row["tier_scope"] == "Tier A" and row["split"] == "validation")
        oos_supply = next(row for row in candidate_supply if row["tier_scope"] == "Tier A" and row["split"] == "oos")
        den_gate = gate_label(validation_metrics, oos_metrics, "density")
        edge_gate = gate_label(validation_metrics, oos_metrics, "edge")
        curve_gate = gate_label(validation_metrics, oos_metrics, "curve")
        selection_score = (
            s308.s307.prev.s290.selection_score(validation_metrics)
            + s308.s307.prev.s290.selection_score(oos_metrics)
            + min(float(validation_metrics["net_bp"]), float(oos_metrics["net_bp"])) * 1.70
            - max(0.0, 4.0 - min(float(validation_metrics["trades_per_day"]), float(oos_metrics["trades_per_day"]))) * 80.0
        )
        branch_rows.append(
            {
                "branch_id": branch_id,
                "package_id": spec.package_id,
                "source_stage_id": SOURCE_STAGE_ID,
                "source_run_id": SOURCE_RUN_ID,
                "hypothesis": spec.hypothesis,
                "decision_use": "MT5 runtime probe(MT5 런타임 탐침) 후보를 열지 결정한다.",
                "comparison_baseline": "Stage308 cp308E clue(308E 단서): OOS(표본외)는 강하지만 validation(검증) 수익/곡선이 약하다.",
                "control_variables": "US100 M5, split_v1(분할 v1), Stage306 feature base(피처 기반), Tier A/B paired accounting(쌍 기록).",
                "changed_variables": spec.changed_variables,
                "sample_scope": "Tier A/Tier B validation/OOS proxy(검증/표본외 대리)와 MT5 runtime probe(런타임 탐침).",
                "success_criteria": "validation/OOS(검증/표본외) 모두 양수, minimum trade count(최소 거래), 4-10 trades/day(일 4-10거래), profit scale(수익 규모), curve pocket(곡선 포켓) 통과.",
                "failure_criteria": "validation(검증) flat/loss(보합/손실), OOS(표본외) 손실, density(밀도) 이탈, local pocket(국소 포켓) 지속.",
                "invalid_conditions": "source payload(원천 페이로드) 누락, feature order(피처 순서) 불일치, MT5 report parse(보고서 파싱) 누락.",
                "stop_conditions": "candidate gate(후보 관문) 통과 시 Adapter(어댑터), 실패 시 새 수익 원천으로 pivot(전환).",
                "evidence_plan": "branch queue(분기 대기열), proxy scoreboard(대리 점수표), payload manifest(페이로드 목록), MT5 queue(MT5 대기열), run309B/run309C.",
                "feature_surface": "Stage306 feature base(피처 기반) plus split-coherent score(분할 일관 점수), validation curve guard(검증 곡선 보호), trend breadth confirmation(추세/시장폭 확인).",
                "model_surface": "rule_surface_split_coherent_profit_curve_model",
                "decision_surface": spec.decision_surface,
                "risk_logic": json.dumps(risk_manifest_fields(spec), sort_keys=True),
                "adapter_path": "deferred_until_candidate_gate",
                "runtime_handoff": "route_signal_value replay(경로 신호 재생); Adapter trace(어댑터 추적)는 후보 관문 뒤에만 시작한다.",
                "failure_memory_plan": "방어형/공격형 표면별 validation/OOS(검증/표본외) 곡선 실패를 분리 기록한다.",
                "claim_boundary": BOUNDARY,
            }
        )
        manifest_rows.append(
            {
                "queue_id": f"run309A_queue_{index:02d}",
                "materialized_branch_id": branch_id,
                "stage309_branch_id": branch_id,
                "stage308_branch_id": stage308_seed,
                "stage307_branch_id": seed.get("stage307_branch_id", ""),
                "stage306_branch_id": seed.get("materialized_branch_id", ""),
                "package_id": spec.package_id,
                "queue_role": "split_coherent_profit_curve_source_surface",
                "payload_path": rel(payload_path),
                "payload_hash": sha256_file(payload_path),
                "handoff_path": rel(handoff_path),
                "handoff_hash": sha256_file(handoff_path),
                "model_artifact_path": rel(model_spec_path),
                "model_artifact_hash": sha256_file(model_spec_path),
                "model_feature_order_path": rel(model_spec_path),
                "model_feature_order_hash": ordered_hash(DECISION_FEATURES),
                "direction_surface_hash": identity["direction_surface_hash"],
                "direction_feature_order_hash": ordered_hash(RUNTIME_FEATURE_ORDER),
                "max_hold_bars": spec.max_hold_bars,
                "close_on_flat_signal": int(spec.close_on_flat_signal),
                "same_direction_reentry_cooldown_bars": spec.same_direction_reentry_cooldown_bars,
                **risk_manifest_fields(spec),
                "approx_validation_trades_per_day": val_supply["approx_trades_per_day"],
                "approx_oos_trades_per_day": oos_supply["approx_trades_per_day"],
                "selected_candidate": "none",
                "adapter_package": "none",
                "onnx_readiness": "not_claimed",
                "claim_boundary": BOUNDARY,
            }
        )
        model_rows.append(
            {
                "materialized_branch_id": branch_id,
                "package_id": spec.package_id,
                "model_family": "split_coherent_rule_surface",
                "prediction_kind": "runtime_state_profit_curve_source",
                "dataset_id": "stage308_failure_memory_plus_stage306_features",
                "model_artifact_path": rel(model_spec_path),
                "model_artifact_hash": sha256_file(model_spec_path),
                "model_feature_order_path": rel(model_spec_path),
                "model_feature_order_hash": ordered_hash(DECISION_FEATURES),
                "classes": "-1,0,1",
                "payoff_weight_policy": spec.decision_surface,
                "onnx_exportability_note": "Adapter(어댑터) 전에는 ONNX(온엑스)를 시작하지 않는다.",
            }
        )
        scoreboard_rows.append(
            {
                "materialized_branch_id": branch_id,
                "package_id": spec.package_id,
                "model_family": "split_coherent_rule_surface",
                "prediction_kind": "runtime_state_profit_curve_source",
                "mode": spec.decision_surface,
                "validation_proxy_net_bp": validation_metrics["net_bp"],
                "validation_proxy_pf": validation_metrics["pf"],
                "validation_proxy_trade_count": validation_metrics["trade_count"],
                "validation_proxy_trades_per_day": validation_metrics["trades_per_day"],
                "validation_proxy_recovery": validation_metrics["recovery"],
                "validation_proxy_worst_month_bp": validation_metrics["worst_month_bp"],
                "validation_proxy_worst_rolling_20_bp": validation_metrics["worst_rolling_20_bp"],
                "validation_proxy_worst_rolling_50_bp": validation_metrics["worst_rolling_50_bp"],
                "validation_proxy_positive_month_share": validation_metrics["positive_month_share"],
                "oos_proxy_net_bp": oos_metrics["net_bp"],
                "oos_proxy_pf": oos_metrics["pf"],
                "oos_proxy_trade_count": oos_metrics["trade_count"],
                "oos_proxy_trades_per_day": oos_metrics["trades_per_day"],
                "oos_proxy_recovery": oos_metrics["recovery"],
                "oos_proxy_worst_month_bp": oos_metrics["worst_month_bp"],
                "oos_proxy_worst_rolling_20_bp": oos_metrics["worst_rolling_20_bp"],
                "oos_proxy_worst_rolling_50_bp": oos_metrics["worst_rolling_50_bp"],
                "oos_proxy_positive_month_share": oos_metrics["positive_month_share"],
                "density_gate": den_gate,
                "proxy_edge_gate": edge_gate,
                "curve_proxy_gate": curve_gate,
                "selection_score": selection_score,
                "selected_candidate": "none",
                "adapter_package": "none",
                "onnx_readiness": "not_claimed",
                "claim_boundary": BOUNDARY,
            }
        )
        for split_name, metrics in (("validation", validation_metrics), ("oos", oos_metrics)):
            wfo_rows.append(
                {
                    "materialized_branch_id": branch_id,
                    "package_id": spec.package_id,
                    "fold_id": split_name,
                    "mode": spec.decision_surface,
                    "net_bp": metrics["net_bp"],
                    "pf": metrics["pf"],
                    "trade_count": metrics["trade_count"],
                    "trades_per_day": metrics["trades_per_day"],
                    "recovery": metrics["recovery"],
                    "worst_month_bp": metrics["worst_month_bp"],
                    "worst_rolling_20_bp": metrics["worst_rolling_20_bp"],
                    "worst_rolling_50_bp": metrics["worst_rolling_50_bp"],
                    "positive_month_share": metrics["positive_month_share"],
                    "underwater_ratio": metrics["underwater_ratio"],
                }
            )
        artifacts.extend([payload_path, handoff_path, model_spec_path])
    scoreboard_rows.sort(key=lambda row: float(row["selection_score"]), reverse=True)
    return branch_rows, scoreboard_rows, supply_rows, manifest_rows, model_rows, wfo_rows, artifacts


def result_rows(scoreboard_rows: Sequence[Mapping[str, Any]], manifest_rows: Sequence[Mapping[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    density_pass = sum(1 for row in scoreboard_rows if row["density_gate"] == "passed")
    edge_pass = sum(1 for row in scoreboard_rows if row["proxy_edge_gate"] == "passed")
    curve_pass = sum(1 for row in scoreboard_rows if row["curve_proxy_gate"] == "passed")
    result = [
        {
            "result_subject": RUN_ID,
            "evidence_available": f"candidate_rows={len(scoreboard_rows)};mt5_queue_rows={len(manifest_rows)};density_proxy_pass={density_pass};edge_proxy_pass={edge_pass};curve_proxy_pass={curve_pass}",
            "evidence_missing": "MT5 runtime KPI(런타임 KPI);parsed curve review(곡선 검토);candidate package(후보 패키지);Adapter package(어댑터 패키지);ONNX parity(온엑스 동등성)",
            "judgment_label": JUDGMENT,
            "judgment_class": "exploratory_materialization(탐색 물질화)",
            "claim_boundary": BOUNDARY,
            "next_condition": NEXT_ACTION,
            "user_explanation_hook": "Stage309(309단계)는 새 후보를 만들었지만 MT5(메타트레이더5) 전에는 선택 후보가 아니다.",
        }
    ]
    gates = [
        {"gate_name": "fresh_thesis(새 논제)", "status": "passed", "evidence_path": rel(BRANCH_QUEUE), "effect": "Stage308(308단계) OOS clue(표본외 단서)를 새 split-coherent(분할 일관) 질문으로 바꿨다."},
        {"gate_name": "candidate_materialization(후보 물질화)", "status": "passed", "evidence_path": rel(PAYLOAD_MANIFEST), "effect": "후보 payload(페이로드), handoff(인계), MT5 queue(MT5 대기열)를 만들었다."},
        {"gate_name": "density_proxy(밀도 대리)", "status": "passed" if density_pass else "failed", "evidence_path": rel(MODEL_SCOREBOARD), "effect": "4-10 trades/day(일 4-10거래) proxy(대리)를 확인했다."},
        {"gate_name": "adapter_package(어댑터 패키지)", "status": "not_started", "evidence_path": "", "effect": "MT5 review(MT5 검토) 전에는 Adapter(어댑터)를 만들지 않는다."},
        {"gate_name": "onnx_readiness(온엑스 준비)", "status": "not_started", "evidence_path": "", "effect": "후보 선택 전에는 ONNX(온엑스)를 시작하지 않는다."},
    ]
    return result, gates


def report_markdown(scoreboard_rows: Sequence[Mapping[str, Any]], manifest_rows: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        "# run309A Split-Coherent Profit Curve Source Materialization(309A 분할 일관 수익 곡선 원천 물질화)",
        "",
        f"- run_id(실행 ID): `{RUN_ID}`",
        f"- source_run(원천 실행): `{SOURCE_RUN_ID}`",
        f"- candidates(후보): `{len(scoreboard_rows)}`",
        f"- MT5 queue rows(MT5 대기열 행): `{len(manifest_rows)}`",
        "- selected_candidate(선택 후보): `none`",
        "- Adapter package(어댑터 패키지): `none`",
        "- ONNX readiness(온엑스 준비): `not_started`",
        "- Goal Achieve(목표 달성): `not_claimed`",
        f"- next_action(다음 행동): `{NEXT_ACTION}`",
        "",
        "Effect(효과): Stage308(308단계)의 cp308E OOS clue(308E 표본외 단서)를 그대로 repair(수리)하지 않고, split-coherent profit curve source(분할 일관 수익 곡선 원천) 후보로 다시 만들었다.",
        "",
        "| package(패키지) | val bp(검증 bp) | OOS bp(표본외 bp) | trades/day(일거래) | gates(관문) |",
        "|---|---:|---:|---:|---|",
    ]
    for row in scoreboard_rows:
        gate_text = ",".join(name for name, key in (("density", "density_gate"), ("edge", "proxy_edge_gate"), ("curve", "curve_proxy_gate")) if row[key] != "passed")
        lines.append(
            "| {pkg} | {val:.2f} | {oos:.2f} | {vtd:.2f}/{otd:.2f} | {gates} |".format(
                pkg=row["package_id"],
                val=float(row["validation_proxy_net_bp"]),
                oos=float(row["oos_proxy_net_bp"]),
                vtd=float(row["validation_proxy_trades_per_day"]),
                otd=float(row["oos_proxy_trades_per_day"]),
                gates=gate_text or "passed",
            )
        )
    lines.extend(["", f"`{BOUNDARY}`"])
    return "\n".join(lines)


def write_outputs(branch_rows: Sequence[Mapping[str, Any]], scoreboard_rows: Sequence[Mapping[str, Any]], supply_rows: Sequence[Mapping[str, Any]], manifest_rows: Sequence[Mapping[str, Any]], model_rows: Sequence[Mapping[str, Any]], wfo_rows: Sequence[Mapping[str, Any]], payload_artifacts: Sequence[Path]) -> list[Path]:
    result, gates = result_rows(scoreboard_rows, manifest_rows)
    write_csv(BRANCH_QUEUE, BRANCH_COLUMNS, branch_rows)
    write_csv(MODEL_SCOREBOARD, SCOREBOARD_COLUMNS, scoreboard_rows)
    write_csv(CANDIDATE_SUPPLY, SUPPLY_COLUMNS, supply_rows)
    write_csv(PAYLOAD_MANIFEST, MANIFEST_COLUMNS, manifest_rows)
    write_csv(MT5_QUEUE, MANIFEST_COLUMNS, manifest_rows)
    write_csv(MODEL_MANIFEST, MODEL_COLUMNS, model_rows)
    write_csv(WFO_FOLD_SCOREBOARD, WFO_COLUMNS, wfo_rows)
    write_csv(RESULT_JUDGMENT, RESULT_COLUMNS, result)
    write_csv(GATE_AUDIT, GATE_COLUMNS, gates)
    write_json(
        EXPERIMENT_DESIGN,
        {
            "hypothesis": "split-coherent profit curve source(분할 일관 수익 곡선 원천)가 Stage308(308단계)의 OOS(표본외) 단서를 validation(검증) 곡선 안정성과 결합할 수 있는지 본다.",
            "decision_use": "run309B MT5 runtime probe(MT5 런타임 탐침)를 열 후보를 고른다.",
            "comparison_baseline": "Stage308 no-selection(선택 없음), best clue cp308E(308E 단서) validation flat/OOS positive(검증 보합/표본외 양수).",
            "control_variables": ["US100 M5", "split_v1", "Stage306 feature base(피처 기반)", "Tier A/B paired accounting(쌍 기록)"],
            "changed_variables": ["split coherent score(분할 일관 점수)", "curve guard(곡선 보호)", "trend breadth confirmation(추세/시장폭 확인)", "defensive/aggressive risk(방어/공격 위험)"],
            "sample_scope": "Tier A/Tier B validation/OOS proxy(검증/표본외 대리), MT5 runtime probe(MT5 런타임 탐침) 예정.",
            "success_criteria": ["MT5 validation/OOS positive(검증/표본외 양수)", "minimum trade count(최소 거래)", "4-10 trades/day(일 4-10거래)", "profit scale(수익 규모)", "smooth curve(완만한 곡선)"],
            "failure_criteria": ["validation flat/loss(검증 보합/손실)", "OOS loss(표본외 손실)", "deep local pocket(깊은 국소 포켓)", "density outside 4-10(밀도 이탈)"],
            "invalid_conditions": ["feature order mismatch(피처 순서 불일치)", "runtime report missing(MT5 보고서 누락)", "data leakage(데이터 누수)"],
            "stop_conditions": ["candidate gate pass(후보 관문 통과) -> Adapter(어댑터)", "all fail(전부 실패) -> Stage310(310단계) fresh source(새 원천)"],
            "evidence_plan": [rel(MODEL_SCOREBOARD), rel(PAYLOAD_MANIFEST), rel(MT5_QUEUE), "run309B MT5 KPI", "run309C review"],
        },
    )
    write_json(
        DATA_RECEIPT,
        {
            "source_scoreboard": rel(SOURCE_SCOREBOARD),
            "source_failure_memory": rel(SOURCE_FAILURE_MEMORY),
            "source_curve_quality": rel(SOURCE_CURVE),
            "source_seed_queue": rel(SOURCE_SEED_QUEUE),
            "decision_feature_count": len(DECISION_FEATURES),
            "model_feature_order_hash": ordered_hash(DECISION_FEATURES),
            "runtime_feature_order_hash": ordered_hash(RUNTIME_FEATURE_ORDER),
            "claim_boundary": BOUNDARY,
        },
    )
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "source_run_id": SOURCE_RUN_ID,
            "status": STATUS,
            "judgment": JUDGMENT,
            "selected_candidate": "none",
            "adapter_package": "none",
            "onnx_readiness": "not_claimed",
            "goal_achieve": "not_claimed",
            "next_action": NEXT_ACTION,
            "artifacts": [rel(path) for path in [BRANCH_QUEUE, MODEL_SCOREBOARD, CANDIDATE_SUPPLY, PAYLOAD_MANIFEST, MT5_QUEUE, MODEL_MANIFEST, WFO_FOLD_SCOREBOARD, EXPERIMENT_DESIGN, DATA_RECEIPT, RESULT_JUDGMENT, GATE_AUDIT, LINEAGE, REPORT]],
            "claim_boundary": BOUNDARY,
        },
    )
    write_json(
        LINEAGE,
        {
            "run_id": RUN_ID,
            "producer": str(PRODUCER),
            "source_inputs": [rel(SOURCE_SCOREBOARD), rel(SOURCE_FAILURE_MEMORY), rel(SOURCE_CURVE), rel(SOURCE_SEED_QUEUE), rel(SOURCE_REVIEW)],
            "consumer": NEXT_ACTION,
            "artifact_paths": {"scoreboard": rel(MODEL_SCOREBOARD), "mt5_queue": rel(MT5_QUEUE), "report": rel(REPORT)},
            "artifact_hashes": {"model_feature_order_hash": ordered_hash(DECISION_FEATURES), "runtime_feature_order_hash": ordered_hash(RUNTIME_FEATURE_ORDER)},
            "lineage_judgment": "connected_with_boundary",
            "claim_boundary": BOUNDARY,
        },
    )
    write_text(REPORT, report_markdown(scoreboard_rows, manifest_rows))
    return list(payload_artifacts) + [BRANCH_QUEUE, MODEL_SCOREBOARD, CANDIDATE_SUPPLY, PAYLOAD_MANIFEST, MT5_QUEUE, MODEL_MANIFEST, WFO_FOLD_SCOREBOARD, EXPERIMENT_DESIGN, DATA_RECEIPT, RESULT_JUDGMENT, GATE_AUDIT, RUN_MANIFEST, LINEAGE, REPORT]


def update_registers(scoreboard_rows: Sequence[Mapping[str, Any]], manifest_rows: Sequence[Mapping[str, Any]], artifacts: Sequence[Path], created_at: str) -> None:
    safe_upsert(
        RUN_REGISTRY,
        RUN_REGISTRY_COLUMNS,
        [{"run_id": RUN_ID, "stage_id": STAGE_ID, "lane": "split_coherent_profit_curve_source_materialization", "status": STATUS, "judgment": JUDGMENT, "path": rel(REPORT), "notes": f"branches={len(scoreboard_rows)};mt5_queue_rows={len(manifest_rows)};next_action={NEXT_ACTION}"}],
        "run_id",
    )
    safe_upsert(
        ALPHA_LEDGER,
        ledger.ALPHA_LEDGER_COLUMNS,
        [
            {
                "ledger_row_id": f"{RUN_ID}__materialization",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": RUN_NUMBER,
                "parent_run_id": SOURCE_RUN_ID,
                "record_view": "split_coherent_profit_curve_source_materialization",
                "tier_scope": "Tier A/Tier B paired exploration labels",
                "kpi_scope": "proxy_density_edge_curve_screen",
                "scoreboard_lane": "split_coherent_profit_curve_source",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT),
                "primary_kpi": f"materialized={len(scoreboard_rows)};mt5_queue_rows={len(manifest_rows)}",
                "guardrail_kpi": "selected_candidate=none;onnx_readiness=not_claimed",
                "external_verification_status": "out_of_scope_by_claim",
                "notes": f"next_action={NEXT_ACTION}.",
            }
        ],
        "ledger_row_id",
    )
    safe_upsert(
        STAGE_LEDGER,
        STAGE_LEDGER_COLUMNS,
        [{"row_id": f"{RUN_ID}__materialization", "stage_id": STAGE_ID, "run_id": RUN_ID, "view": "split_coherent_profit_curve_source_materialization", "tier_scope": "Tier A/Tier B paired exploration labels", "scoreboard": "model_scout_scoreboard", "status": STATUS, "judgment": JUDGMENT, "evidence_boundary": "materialization_no_candidate_no_onnx", "report_path": rel(REPORT), "notes": f"mt5_queue_rows={len(manifest_rows)};next_action={NEXT_ACTION}"}],
        "row_id",
    )
    artifact_rows = [
        {
            "artifact_id": f"{RUN_ID}__{hashlib.sha1(rel(path).encode('utf-8')).hexdigest()[:12]}",
            "artifact_type": "stage309_split_coherent_profit_curve_source_artifact",
            "path": rel(path),
            "sha256": sha256_file(path),
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": created_at,
            "notes": "run309A split-coherent profit curve source materialization",
        }
        for path in artifacts
        if path_exists(path)
    ]
    safe_upsert(ARTIFACT_REGISTRY, ARTIFACT_COLUMNS, artifact_rows, "artifact_id")


def update_docs(scoreboard_rows: Sequence[Mapping[str, Any]], manifest_rows: Sequence[Mapping[str, Any]]) -> None:
    selected = read_text(SELECTED)
    selected = replace_line_prefix(selected, "- stage_status(", f"- stage_status(단계 상태): `{STATUS}`")
    selected = replace_line_prefix(selected, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    selected = replace_line_prefix(selected, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    selected = append_once(selected, "run309A_report", f"- run309A_report(309A 보고서): `{rel(REPORT)}`")
    selected = append_once(selected, "run309A_mt5_queue", f"- run309A_mt5_queue(309A MT5 대기열): `{rel(MT5_QUEUE)}`")
    write_text(SELECTED, selected)

    review_index = read_text(REVIEW_INDEX) or "# Stage309 Review Index(309단계 검토 색인)\n"
    review_index = append_once(review_index, "run309A_report", f"- run309A_report(309A 보고서): `{rel(REPORT)}`")
    review_index = append_once(review_index, "run309A_mt5_queue", f"- run309A_mt5_queue(309A MT5 대기열): `{rel(MT5_QUEUE)}`")
    write_text(REVIEW_INDEX, review_index)

    idea = read_text(IDEA_REGISTER)
    idea = append_once(
        idea,
        "stage309_split_coherent_profit_curve_source",
        "## stage309_split_coherent_profit_curve_source\n\n- hypothesis(가설): split-coherent profit curve source(분할 일관 수익 곡선 원천)가 OOS upside(표본외 상방)와 validation curve stability(검증 곡선 안정성)를 동시에 만들 수 있다.\n- boundary(경계): exploratory(탐색), no selected candidate(선택 후보 없음), no Adapter(어댑터 없음), no ONNX(온엑스 없음).\n",
    )
    write_text(IDEA_REGISTER, idea)

    current = read_text(CURRENT_STATE)
    current = replace_line_prefix(current, "- current_packet(", f"- current_packet(현재 작업 묶음): `{STAGE_ID}_v1`")
    current = replace_line_prefix(current, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_line_prefix(current, "- active_stage(", f"- active_stage(활성 단계): `{STAGE_ID}`")
    current = replace_line_prefix(current, "- source_stage(", f"- source_stage(원천 단계): `{SOURCE_STAGE_ID}`")
    current = replace_line_prefix(current, "- status(", f"- status(상태): `{STATUS}`")
    current = replace_line_prefix(current, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    current = append_once(
        current,
        "run309A_summary",
        f"- run309A_summary(309A 요약): split-coherent profit curve source(분할 일관 수익 곡선 원천) 후보 `{len(scoreboard_rows)}`개를 materialized(물질화)했다. Effect(효과): Stage308(308단계) cp308E OOS clue(308E 표본외 단서)를 새 validation/OOS(검증/표본외) 곡선 후보로 바꾸고 MT5 queue(MT5 대기열) `{len(manifest_rows)}`개를 만들었으며 선택 후보/Adapter(어댑터)/ONNX(온엑스)는 주장하지 않는다.",
    )
    write_text(CURRENT_STATE, current)

    workspace = read_text(WORKSPACE_STATE)
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    workspace = replace_line_prefix(workspace, "active_stage:", f"active_stage: {STAGE_ID}")
    workspace = replace_line_prefix(workspace, "updated_on:", f"updated_on: '{UPDATED_ON}'")
    focus = (
        f"- >-\n"
        f"  Stage309(309단계) run309A(309A 실행) split-coherent profit curve source materialization(분할 일관 수익 곡선 원천 물질화) `{RUN_ID}`. "
        f"Effect(효과): candidates(후보) `{len(scoreboard_rows)}`개와 MT5 queue(MT5 대기열) `{len(manifest_rows)}`개를 만들었고 selected candidate(선택 후보), Adapter package(어댑터 패키지), ONNX readiness(온엑스 준비)는 주장하지 않는다.\n"
    )
    workspace = prepend_focus(workspace, focus, RUN_ID)
    write_text(WORKSPACE_STATE, workspace)

    changelog = read_text(CHANGELOG) or "# Changelog(변경 기록)\n"
    changelog = append_once(
        changelog,
        RUN_ID,
        f"## {UPDATED_ON} run309A Split-coherent profit curve source materialization(309A 분할 일관 수익 곡선 원천 물질화)\n\n"
        f"- run_id(실행 ID): `{RUN_ID}`\n"
        f"- status(상태): `{STATUS}`\n"
        f"- candidates(후보): `{len(scoreboard_rows)}`\n"
        f"- mt5_queue_rows(MT5 대기열 행): `{len(manifest_rows)}`\n"
        f"- next_action(다음 행동): `{NEXT_ACTION}`\n",
    )
    write_text(CHANGELOG, changelog)


def main() -> None:
    created_at = utc_now()
    branch_rows, scoreboard_rows, supply_rows, manifest_rows, model_rows, wfo_rows, payload_artifacts = build_outputs()
    artifacts = write_outputs(branch_rows, scoreboard_rows, supply_rows, manifest_rows, model_rows, wfo_rows, payload_artifacts)
    update_registers(scoreboard_rows, manifest_rows, artifacts, created_at)
    update_docs(scoreboard_rows, manifest_rows)
    print(
        json.dumps(
            {
                "status": STATUS,
                "judgment": JUDGMENT,
                "candidate_count": len(scoreboard_rows),
                "mt5_queue_rows": len(manifest_rows),
                "best_proxy": scoreboard_rows[0]["package_id"] if scoreboard_rows else "none",
                "best_validation_net_bp": scoreboard_rows[0]["validation_proxy_net_bp"] if scoreboard_rows else 0,
                "best_oos_net_bp": scoreboard_rows[0]["oos_proxy_net_bp"] if scoreboard_rows else 0,
                "next_action": NEXT_ACTION,
                "selected_candidate": "none",
                "adapter_package": "none",
                "onnx_readiness": "not_claimed",
                "goal_achieve": "not_claimed",
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )


PRODUCER = Path("stage_pipelines/stage309/design_split_coherent_profit_curve_source_rebuild.py")


if __name__ == "__main__":
    main()
