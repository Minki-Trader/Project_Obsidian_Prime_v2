from __future__ import annotations

import hashlib
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from stage_pipelines.stage337 import (  # noqa: E402
    design_runtime_positive_low_pf_recovery_drawdown_dual_probe_repair_without_db as jk,
)
from stage_pipelines.stage337 import (  # noqa: E402
    materialize_runtime_negative_collapse_cost_stress_trade_shape_repair_inputs_without_db as jd,
)


aw = jk.aw

TODAY = "2026-06-01"
STAGE_ID = jk.STAGE_ID
STAGE_DIR = jk.STAGE_DIR
RUN_NUMBER = "run337JL"
RUN_ID = "run337JL_materialize_runtime_positive_low_pf_recovery_drawdown_dual_probe_repair_inputs_without_db_v1"
PARENT_RUN_ID = jk.RUN_ID
NEXT_RUN_ID = "run337JM_review_runtime_positive_low_pf_recovery_drawdown_dual_probe_repair_inputs_without_db_v1"
STATUS = "completed_stage337JL_runtime_positive_low_pf_recovery_drawdown_dual_probe_repair_inputs_materialized_no_training_no_selection"
JUDGMENT = "timestamp_safe_runtime_positive_low_pf_recovery_drawdown_dual_probe_repair_inputs_materialized_review_required"
DECISION = "stage337JL_open_run337JM_runtime_positive_low_pf_recovery_drawdown_dual_probe_repair_input_review"
CLAIM_BOUNDARY = (
    "research_development_input_materialization_only_no_model_training_no_threshold_tuning_no_lot_optimization_"
    "no_candidate_selection_no_mt5_execution_no_forward_passed_no_forward_failed_no_live_readiness_"
    "no_operating_promotion_no_runtime_authority_no_goal_achieve"
)

RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEW_DIR / "run337JL_positive_low_pf_recovery_drawdown_dual_probe_repair_inputs.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage337JL_positive_low_pf_recovery_drawdown_dual_probe_repair_inputs.md"

RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
PROJECT_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
ROOT_SELECTION_STATUS = ROOT / "docs" / "registers" / "selection_status.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs" / "context" / "current_working_state.md"
SELECTION_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
STAGE_BRIEF = STAGE_DIR / "README.md"
ROOT_CHANGELOG = ROOT / "CHANGELOG.md"
WORKSPACE_CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"

BASE_INPUT_FRAME = jd.JD_INPUT_FRAME
BASE_ALLOWED_FEATURES = jd.JD_ALLOWED_FEATURES

JL_INPUT_FRAME = RUN_DIR / "jl_runtime_positive_low_pf_recovery_drawdown_repair_input_frame.parquet"
JL_ALLOWED_FEATURES = RUN_DIR / "jl_allowed_model_feature_set.csv"
JL_SOURCE_MAP = RUN_DIR / "jl_source_map.csv"
JL_WEIGHT_RECIPE = RUN_DIR / "jl_weight_recipe_matrix.csv"
JL_WEIGHT_AUDIT = RUN_DIR / "jl_weight_audit.csv"
JL_FEATURE_BOUNDARY = RUN_DIR / "jl_feature_label_boundary_audit.csv"
JL_TIER_RECORDS = RUN_DIR / "jl_tier_records.csv"
JL_RUNTIME_PARITY_PLAN = RUN_DIR / "jl_runtime_parity_guard_plan.csv"
JL_TASK_SEEDS = RUN_DIR / "run337JM_training_task_seed_matrix.csv"
JM_QUEUE = RUN_DIR / "run337JM_input_review_queue.csv"
RUN_EVIDENCE_RECEIPT = RUN_DIR / "run_evidence_receipt.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

JL_WEIGHT_COLUMNS = (
    "jl_pf_recovery_profit_quality_weight",
    "jl_drawdown_holding_loss_guard_weight",
    "jl_density_throttle_short_edge_weight",
    "jl_long_loss_quarantine_short_preserve_weight",
    "jl_negative_control_session_regime_firewall_weight",
    "jl_cost_stress_slippage_buffer_weight",
    "jl_equity_smoothness_recovery_weight",
    "jl_router_blend_scout_weight",
)
JL_TARGET_COLUMNS = (
    "jl_label_class_profit_quality_fwd18",
    "jl_valid_profit_quality_fwd18",
    "jl_label_class_density_throttle_fwd18",
    "jl_valid_density_throttle_fwd18",
)
FORBIDDEN_FEATURE_TOKENS = (
    "label",
    "future",
    "target",
    "mt5",
    "profit",
    "expectancy",
    "recovery",
    "drawdown",
    "telemetry",
    "proxy",
)
FORBIDDEN_FEATURE_SUFFIXES = ("_weight", "_sample_weight")

INPUT_FILES = (
    jk.FINAL_DECISION,
    jk.GATE_AUDIT,
    jk.DESIGN_MATRIX,
    jk.FAILURE_MEMORY_MATRIX,
    jk.EXPERIMENT_CONTRACT,
    jk.FEATURE_LABEL_WEIGHT_CONTRACT,
    jk.RUNTIME_PARITY_GUARD,
    jk.TIER_PAIR_CONTRACT,
    jk.MATERIALIZATION_QUEUE,
    jd.FINAL_DECISION,
    jd.GATE_AUDIT,
    jd.JD_INPUT_FRAME,
    jd.JD_ALLOWED_FEATURES,
    jd.JD_WEIGHT_AUDIT,
    jd.JD_TASK_SEEDS,
    jk.jj.RUNTIME_REVIEW,
    jk.jj.TRADE_SHAPE_COMPARISON,
)

OUTPUT_FILES = (
    JL_INPUT_FRAME,
    JL_ALLOWED_FEATURES,
    JL_SOURCE_MAP,
    JL_WEIGHT_RECIPE,
    JL_WEIGHT_AUDIT,
    JL_FEATURE_BOUNDARY,
    JL_TIER_RECORDS,
    JL_RUNTIME_PARITY_PLAN,
    JL_TASK_SEEDS,
    JM_QUEUE,
    RUN_EVIDENCE_RECEIPT,
    DATA_RECEIPT,
    MODEL_RECEIPT,
    PERFORMANCE_RECEIPT,
    RUNTIME_RECEIPT,
    JUDGMENT_RECEIPT,
    CLAIM_RECEIPT,
    LINEAGE_RECEIPT,
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
    ROOT_CHANGELOG,
    WORKSPACE_CHANGELOG,
    RUN_REGISTRY,
    PROJECT_LEDGER,
    STAGE_LEDGER,
    ARTIFACT_REGISTRY,
    Path(__file__),
)


def now_utc() -> str:
    return datetime.now(tz=UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def io(path: Path) -> Path:
    return aw.io_path(path)


def rel(path: Path | str) -> str:
    return aw.rel(path)


def exists(path: Path) -> bool:
    return io(path).exists()


def ensure_parent(path: Path) -> None:
    io(path.parent).mkdir(parents=True, exist_ok=True)


def read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(io(path), low_memory=False)


def read_json(path: Path) -> Any:
    return json.loads(io(path).read_text(encoding="utf-8-sig"))


def write_csv(path: Path, frame: pd.DataFrame) -> Path:
    ensure_parent(path)
    frame.to_csv(io(path), index=False, encoding="utf-8-sig", lineterminator="\n")
    return path


def write_json(path: Path, payload: Any) -> Path:
    ensure_parent(path)
    io(path).write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True, default=str) + "\n",
        encoding="utf-8",
    )
    return path


def write_bom_text(path: Path, text: str) -> Path:
    ensure_parent(path)
    io(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig", newline="\n")
    return path


def sha(path: Path) -> str:
    return aw.sha256_file(path)


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        if value in ("", None) or pd.isna(value):
            return default
        number = float(value)
    except (TypeError, ValueError):
        return default
    return number if np.isfinite(number) else default


def as_int(value: Any, default: int = 0) -> int:
    return int(round(as_float(value, float(default))))


def num(frame: pd.DataFrame, column: str, default: float = 0.0) -> pd.Series:
    if column not in frame.columns:
        return pd.Series(default, index=frame.index, dtype="float64")
    return pd.to_numeric(frame[column], errors="coerce").replace([np.inf, -np.inf], np.nan).fillna(default).astype("float64")


def rank01(values: pd.Series | np.ndarray) -> pd.Series:
    series = pd.Series(values).replace([np.inf, -np.inf], np.nan).astype("float64")
    if series.notna().sum() == 0:
        return pd.Series(0.5, index=series.index, dtype="float64")
    return series.rank(pct=True).fillna(0.5).astype("float64")


def norm01(values: pd.Series | np.ndarray) -> pd.Series:
    series = pd.Series(values).replace([np.inf, -np.inf], np.nan).astype("float64")
    low = series.quantile(0.05)
    high = series.quantile(0.95)
    if not np.isfinite(low) or not np.isfinite(high) or high <= low:
        return pd.Series(0.0, index=series.index, dtype="float64")
    return ((series - low) / (high - low)).clip(0.0, 1.0).fillna(0.0)


def clip_weight(values: pd.Series | np.ndarray, lower: float = 0.10, upper: float = 12.0) -> pd.Series:
    return pd.Series(values).replace([np.inf, -np.inf], np.nan).fillna(1.0).clip(lower, upper).astype("float64")


def feature_hash(features: Sequence[str]) -> str:
    return hashlib.sha256("\n".join(features).encode("utf-8")).hexdigest()


def passed_status(series: pd.Series) -> pd.Series:
    return series.astype(str).str.lower().isin(["pass", "passed", "true", "1", "yes"])


def append_or_replace_csv(path: Path, key_columns: Iterable[str], row: Mapping[str, Any]) -> None:
    frame = read_csv(path) if exists(path) else pd.DataFrame()
    if frame.empty:
        frame = pd.DataFrame(columns=list(row.keys()))
    for column in row:
        if column not in frame.columns:
            frame[column] = ""
    mask = pd.Series(True, index=frame.index)
    for key in key_columns:
        if key in frame.columns:
            mask = mask & frame[key].astype(str).eq(str(row[key]))
        else:
            mask = mask & False
    frame = frame.loc[~mask].copy()
    frame = pd.concat([frame, pd.DataFrame([row])], ignore_index=True)
    ordered = list(dict.fromkeys(list(frame.columns) + list(row.keys())))
    write_csv(path, frame[ordered])


def append_text_once(path: Path, marker: str, text: str) -> None:
    current = io(path).read_text(encoding="utf-8-sig") if exists(path) else ""
    if marker in current:
        return
    next_text = (current.rstrip() + "\n\n" + text.strip() + "\n") if current.strip() else text.strip() + "\n"
    write_bom_text(path, next_text)


def read_source_frame() -> pd.DataFrame:
    frame = pd.read_parquet(io(BASE_INPUT_FRAME)).copy()
    if "timestamp" in frame.columns:
        frame["timestamp"] = pd.to_datetime(frame["timestamp"], utc=True)
    sort_cols = [column for column in ("timestamp", "source_row_id", "cost_policy_id") if column in frame.columns]
    if sort_cols:
        frame = frame.sort_values(sort_cols).reset_index(drop=True)
    return frame


def allowed_features_copy() -> pd.DataFrame:
    allowed = read_csv(BASE_ALLOWED_FEATURES).copy()
    if "feature_name" not in allowed.columns:
        allowed = allowed.rename(columns={allowed.columns[0]: "feature_name"})
    allowed["jl_usage"] = "allowed_model_input_for_run337JM_review_and_later_training(337JM 검토와 이후 학습 허용 입력)"
    allowed["claim_boundary"] = CLAIM_BOUNDARY
    return allowed


def probability_context(frame: pd.DataFrame) -> tuple[pd.Series, pd.Series]:
    columns = ["mean_prob_short", "mean_prob_flat", "mean_prob_long"]
    if not all(column in frame.columns for column in columns):
        fallback = pd.Series(0.5, index=frame.index, dtype="float64")
        return fallback, fallback
    probs = frame.loc[:, columns].apply(pd.to_numeric, errors="coerce").fillna(1.0 / 3.0).clip(1e-6, 1.0)
    row_sum = probs.sum(axis=1).replace(0.0, np.nan)
    probs = probs.div(row_sum, axis=0).fillna(1.0 / 3.0)
    sorted_probs = np.sort(probs.to_numpy(dtype="float64"), axis=1)
    margin = pd.Series(sorted_probs[:, -1] - sorted_probs[:, -2], index=frame.index, dtype="float64")
    entropy = pd.Series(-(probs * np.log(probs)).sum(axis=1) / np.log(3.0), index=frame.index, dtype="float64")
    return margin.clip(0.0, 1.0), entropy.clip(0.0, 1.0)


def materialize_frame(base: pd.DataFrame) -> pd.DataFrame:
    frame = base.copy()
    f6 = num(frame, "hx_future_log_return_6", np.nan)
    f18 = num(frame, "hx_future_log_return_18", np.nan)
    f24 = num(frame, "hx_future_log_return_24", np.nan)
    valid18 = num(frame, "hx_valid_fwd18", 0).astype(int).eq(1) & f18.notna()
    valid6 = num(frame, "hx_valid_fwd6", 0).astype(int).eq(1) & f6.notna()
    valid24 = num(frame, "hx_valid_fwd24", 0).astype(int).eq(1) & f24.notna()

    label18 = num(frame, "hx_label_class_fwd18", 1).astype(int).clip(0, 2)
    label6 = num(frame, "hx_label_class_fwd6", 1).astype(int).clip(0, 2)
    label24 = num(frame, "hx_label_class_fwd24", 1).astype(int).clip(0, 2)
    active = label18.isin([0, 2])
    short_mask = label18.eq(0)
    long_mask = label18.eq(2)
    flat_mask = label18.eq(1)

    abs18 = f18.abs().fillna(0.0)
    dynamic_buffer = (0.00020 + 0.35 * num(frame, "atr_14", 0.0).abs().rank(pct=True).fillna(0.0) * 0.00035).clip(0.00020, 0.00070)
    profit_label = pd.Series(1, index=frame.index, dtype="int64")
    profit_label.loc[valid18 & f18.lt(-dynamic_buffer)] = 0
    profit_label.loc[valid18 & f18.gt(dynamic_buffer)] = 2
    frame["jl_label_class_profit_quality_fwd18"] = profit_label
    frame["jl_valid_profit_quality_fwd18"] = valid18.astype(int)

    margin, entropy = probability_context(frame)
    density_label = label18.copy()
    weak_active = active & (margin.lt(0.08) | entropy.gt(0.92))
    density_label.loc[weak_active] = 1
    frame["jl_label_class_density_throttle_fwd18"] = density_label.astype(int)
    frame["jl_valid_density_throttle_fwd18"] = valid18.astype(int)

    base_weight = num(frame, "jd_runtime_pnl_proxy_weight", 1.0).clip(0.20, 8.0)
    jd_blend = num(frame, "jd_blended_runtime_negative_repair_weight", 1.0).clip(0.20, 8.0)
    cost_survival = num(frame, "jd_cost_buffer_survival_weight", num(frame, "cost_survival_weight", 1.0)).clip(0.10, 8.0)
    side_weight = num(frame, "jd_side_long_rescue_short_preserve_weight", 1.0).clip(0.10, 8.0)
    drawdown_weight = num(frame, "jd_lifecycle_exit_drawdown_compression_weight", 1.0).clip(0.10, 8.0)
    firewall_weight = num(frame, "jd_session_regime_loss_firewall_weight", 1.0).clip(0.10, 8.0)

    low_margin = num(frame, "low_margin_rate_model", num(frame, "low_margin_rate", 0.0)).clip(0.0, 1.0)
    underwater = num(frame, "underwater_rate_model", num(frame, "underwater_rate", 0.0)).clip(0.0, 1.0)
    drawdown = num(frame, "drawdown_pressure_norm", 0.0).clip(0.0, 1.0)
    side_gap = num(frame, "side_quality_gap_norm", 0.0).clip(0.0, 1.0)
    side_quality = num(frame, "side_quality_weight", 1.0).clip(0.10, 5.0)
    vol = norm01(num(frame, "historical_vol_20", 0.0))
    adx = norm01(num(frame, "adx_14", 0.0))
    vix = norm01(num(frame, "vix_zscore_20", 0.0).abs())
    session_edge = (num(frame, "is_first_30m_after_open", 0.0) + num(frame, "is_last_30m_before_cash_close", 0.0)).clip(0.0, 1.0)
    risk_pressure = (0.36 * drawdown + 0.30 * underwater + 0.18 * low_margin + 0.10 * vol + 0.06 * session_edge).clip(0.0, 1.0)
    agreement_6_18 = (label6.eq(label18) & valid6 & valid18).astype(float)
    agreement_18_24 = (label24.eq(label18) & valid24 & valid18).astype(float)
    return_rank = rank01(abs18)

    pf_quality = (1.0 + 0.95 * return_rank + 0.35 * margin + 0.15 * adx - 0.45 * low_margin - 0.30 * risk_pressure).clip(0.35, 2.10)
    pf_quality = pf_quality.where(active, 0.82 + 0.20 * risk_pressure)
    frame["jl_pf_recovery_profit_quality_weight"] = clip_weight(base_weight * pf_quality)

    drawdown_guard = (1.28 - 0.82 * risk_pressure + 0.28 * agreement_6_18 + 0.12 * agreement_18_24).clip(0.25, 1.65)
    drawdown_guard = drawdown_guard.where(active, 0.95 + 0.35 * risk_pressure)
    frame["jl_drawdown_holding_loss_guard_weight"] = clip_weight(drawdown_weight * drawdown_guard)

    density_factor = (0.72 + 0.82 * margin + 0.28 * (1.0 - entropy) - 0.35 * low_margin).clip(0.30, 1.75)
    density_factor.loc[short_mask] = (density_factor.loc[short_mask] + 0.22 * side_quality.loc[short_mask]).clip(0.30, 1.95)
    density_factor.loc[weak_active] = density_factor.loc[weak_active] * 0.62
    frame["jl_density_throttle_short_edge_weight"] = clip_weight(base_weight * density_factor)

    side_factor = pd.Series(1.0, index=frame.index, dtype="float64")
    side_factor.loc[long_mask] = (0.62 + 0.36 * (1.0 - risk_pressure.loc[long_mask]) + 0.12 * margin.loc[long_mask]).clip(0.25, 1.15)
    side_factor.loc[short_mask] = (1.18 + 0.24 * margin.loc[short_mask] + 0.18 * (1.0 - low_margin.loc[short_mask])).clip(0.80, 1.75)
    side_factor.loc[flat_mask] = (0.94 + 0.20 * risk_pressure.loc[flat_mask]).clip(0.80, 1.25)
    frame["jl_long_loss_quarantine_short_preserve_weight"] = clip_weight(side_weight * side_factor * (1.0 + 0.12 * side_gap))

    regime_pressure = (0.30 * vix + 0.25 * vol + 0.20 * session_edge + 0.15 * underwater + 0.10 * low_margin).clip(0.0, 1.0)
    firewall_factor = (1.14 - 0.64 * regime_pressure + 0.20 * margin).clip(0.25, 1.45)
    firewall_factor = firewall_factor.where(active, 0.92 + 0.28 * regime_pressure)
    frame["jl_negative_control_session_regime_firewall_weight"] = clip_weight(firewall_weight * firewall_factor)

    cost_factor = (cost_survival * (1.12 - 0.44 * low_margin - 0.28 * vol + 0.18 * margin)).clip(0.25, 1.75)
    frame["jl_cost_stress_slippage_buffer_weight"] = clip_weight(base_weight * cost_factor)

    smooth_factor = (1.20 - 0.72 * risk_pressure + 0.22 * agreement_6_18 + 0.20 * agreement_18_24 + 0.10 * (1.0 - entropy)).clip(0.30, 1.65)
    smooth_factor = smooth_factor.where(active, 0.94 + 0.26 * risk_pressure)
    frame["jl_equity_smoothness_recovery_weight"] = clip_weight(jd_blend * smooth_factor)

    frame["jl_router_blend_scout_weight"] = clip_weight(
        0.20 * frame["jl_pf_recovery_profit_quality_weight"]
        + 0.15 * frame["jl_drawdown_holding_loss_guard_weight"]
        + 0.15 * frame["jl_density_throttle_short_edge_weight"]
        + 0.15 * frame["jl_long_loss_quarantine_short_preserve_weight"]
        + 0.15 * frame["jl_negative_control_session_regime_firewall_weight"]
        + 0.10 * frame["jl_cost_stress_slippage_buffer_weight"]
        + 0.10 * frame["jl_equity_smoothness_recovery_weight"]
    )
    return frame


def source_map(frame: pd.DataFrame) -> pd.DataFrame:
    sources = [
        ("jk_final", jk.FINAL_DECISION, "parent decision(부모 결정)", "JK 설계 결과를 입력 물질화 조건으로 고정한다."),
        ("jk_design", jk.DESIGN_MATRIX, "design matrix(설계 행렬)", "8개 수리 축을 가중치와 task seed(작업 씨앗)로 바꾼다."),
        ("jk_failure_memory", jk.FAILURE_MEMORY_MATRIX, "failure memory(실패 기억)", "positive clue(긍정 단서)와 negative control(부정 대조)을 함께 보존한다."),
        ("jd_input_frame", jd.JD_INPUT_FRAME, "base frame(기반 프레임)", "검토된 timestamp-safe(시점 안전) JD 입력을 재사용한다."),
        ("jd_allowed_features", jd.JD_ALLOWED_FEATURES, "allowed features(허용 피처)", "기존 58개 모델 입력만 유지한다."),
        ("jj_runtime_review", jk.jj.RUNTIME_REVIEW, "runtime review(런타임 검토)", "MT5 positive clue(MT5 긍정 단서)와 weak KPI(약한 KPI)를 근거로 둔다."),
    ]
    rows = []
    for source_id, path, source_type, effect in sources:
        rows.append(
            {
                "source_id": source_id,
                "source_path": rel(path),
                "source_type": source_type,
                "required": True,
                "exists": exists(path),
                "sha256": sha(path) if exists(path) and io(path).is_file() else "",
                "effect": effect,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    rows.append(
        {
            "source_id": "jl_input_frame",
            "source_path": rel(JL_INPUT_FRAME),
            "source_type": "generated frame(생성 프레임)",
            "required": True,
            "exists": exists(JL_INPUT_FRAME),
            "sha256": sha(JL_INPUT_FRAME) if exists(JL_INPUT_FRAME) else "",
            "effect": f"{len(frame)} rows(행)을 다음 review(검토)로 넘긴다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    )
    return pd.DataFrame(rows)


def weight_recipe() -> pd.DataFrame:
    rows = [
        ("jl001_pf_recovery_profit_quality", "jl_pf_recovery_profit_quality_weight", "hx_future_log_return_18;probability margin(확률 마진);risk pressure(위험 압박)", "large future return(큰 미래 수익률)과 margin(마진)을 보상하고 low margin/risk(낮은 마진/위험)을 벌점 처리", "PF/recovery(수익 팩터/회복)를 직접 노린다."),
        ("jl002_drawdown_holding_loss_guard", "jl_drawdown_holding_loss_guard_weight", "fwd6/fwd18/fwd24 agreement(6/18/24봉 일치);drawdown pressure(낙폭 압박)", "손실 보유 위험이 큰 active(진입) 표본을 낮추고 flat guard(관망 보호)를 높임", "max drawdown(최대 낙폭)을 낮추는 후보를 연다."),
        ("jl003_density_throttle_short_edge", "jl_density_throttle_short_edge_weight", "probability margin/entropy(확률 마진/엔트로피);short label(숏 라벨)", "약한 active(진입)를 관망 쪽으로 밀고 short edge(숏 우위)는 보존", "과도한 density(밀도)를 줄인다."),
        ("jl004_long_loss_quarantine_short_preserve", "jl_long_loss_quarantine_short_preserve_weight", "side label(방향 라벨);side quality(방향 품질);risk pressure(위험 압박)", "weak long(약한 롱)은 낮추고 short preserve(숏 보존)는 높임", "롱 손실 격리와 숏 우위 보존을 동시에 시도한다."),
        ("jl005_negative_control_session_regime_firewall", "jl_negative_control_session_regime_firewall_weight", "session/regime pressure(세션/국면 압박);vix/volatility(VIX/변동성)", "negative control(부정 대조)의 over-throttle(과도 제한) 패턴을 막는 방화벽", "세션/국면 실패 반복을 줄인다."),
        ("jl006_cost_stress_slippage_buffer", "jl_cost_stress_slippage_buffer_weight", "cost survival(비용 생존);low margin(낮은 마진);volatility(변동성)", "비용 압박에 약한 거래를 낮추고 마진 있는 거래를 남김", "낮은 PF(수익 팩터)의 비용 취약성을 줄인다."),
        ("jl007_equity_smoothness_recovery", "jl_equity_smoothness_recovery_weight", "risk pressure(위험 압박);multi-horizon agreement(다중 기간 일치)", "거친 수익곡선 후보를 낮추고 일관된 방향 후보를 높임", "recovery factor(회복 계수)를 개선할 후보를 만든다."),
        ("jl008_router_blend_scout", "jl_router_blend_scout_weight", "all JL repair weights(모든 JL 수리 가중치)", "raw edge(원시 우위)와 negative veto(부정 거부)를 혼합", "dual-probe(이중 탐침) 후보군을 넓힌다."),
    ]
    return pd.DataFrame(
        [
            {
                "recipe_id": recipe_id,
                "materialized_column": column,
                "source_columns": sources,
                "lower_bound": 0.10,
                "upper_bound": 12.0,
                "train_only_formula": formula,
                "effect": effect,
                "claim_boundary": CLAIM_BOUNDARY,
            }
            for recipe_id, column, sources, formula, effect in rows
        ]
    )


def weight_audit(frame: pd.DataFrame) -> pd.DataFrame:
    label = num(frame, "hx_label_class_fwd18", 1).astype(int)
    rows = []
    for column in JL_WEIGHT_COLUMNS:
        values = num(frame, column, np.nan)
        rows.append(
            {
                "weight_column": column,
                "rows": len(values),
                "weight_min": float(values.min()),
                "weight_mean": float(values.mean()),
                "weight_max": float(values.max()),
                "max_saturation_rate": float(values.ge(11.999).mean()),
                "nonfinite_rows": int((~np.isfinite(values.to_numpy())).sum()),
                "short_label_mean": float(values[label.eq(0)].mean()),
                "flat_label_mean": float(values[label.eq(1)].mean()),
                "long_label_mean": float(values[label.eq(2)].mean()),
                "effect": "학습 전용 가중치가 방향별로 어떻게 작동하는지 기록한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return pd.DataFrame(rows)


def forbidden_feature_violations(features: Sequence[str]) -> list[str]:
    generated = {column.lower() for column in (*JL_WEIGHT_COLUMNS, *JL_TARGET_COLUMNS)}
    violations = []
    for feature in features:
        lowered = str(feature).lower()
        if lowered in generated:
            violations.append(feature)
            continue
        if any(lowered.endswith(suffix) for suffix in FORBIDDEN_FEATURE_SUFFIXES):
            violations.append(feature)
            continue
        if any(token in lowered for token in FORBIDDEN_FEATURE_TOKENS):
            violations.append(feature)
    return violations


def feature_boundary(allowed: pd.DataFrame, frame: pd.DataFrame) -> pd.DataFrame:
    features = allowed["feature_name"].astype(str).tolist()
    forbidden = forbidden_feature_violations(features)
    monotonic = True
    if "timestamp" in frame.columns:
        monotonic = bool(pd.to_datetime(frame["timestamp"], utc=True).is_monotonic_increasing)
    duplicate_source = int(frame.duplicated(["source_row_id", "cost_policy_id"]).sum()) if {"source_row_id", "cost_policy_id"}.issubset(frame.columns) else 0
    label_valid = int(num(frame, "jl_valid_profit_quality_fwd18", 0).sum())
    label_classes = int(pd.Series(frame["jl_label_class_profit_quality_fwd18"]).nunique())
    return pd.DataFrame(
        [
            {
                "audit_id": "jl001_allowed_feature_count",
                "status": "passed" if len(features) == 58 else "failed",
                "observed": len(features),
                "expected": "58",
                "evidence": rel(JL_ALLOWED_FEATURES),
                "effect": "기존 58개 pretrade feature(사전거래 피처)를 유지한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "audit_id": "jl002_forbidden_features_excluded",
                "status": "passed" if not forbidden else "failed",
                "observed": ";".join(forbidden),
                "expected": "no label/future/target/MT5/proxy/weight feature(라벨/미래/목표/MT5/프록시/가중치 피처 없음)",
                "evidence": rel(JL_ALLOWED_FEATURES),
                "effect": "새 가중치와 라벨이 모델 입력으로 새지 않게 한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "audit_id": "jl003_timestamp_order",
                "status": "passed" if monotonic else "failed",
                "observed": str(monotonic),
                "expected": "True",
                "evidence": rel(JL_INPUT_FRAME),
                "effect": "time axis(시간축) 순서를 보존한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "audit_id": "jl004_duplicate_source_cost_rows",
                "status": "passed" if duplicate_source == 0 else "failed",
                "observed": duplicate_source,
                "expected": "0",
                "evidence": rel(JL_INPUT_FRAME),
                "effect": "source/cost row(원천/비용 행) 중복을 막는다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "audit_id": "jl005_profit_quality_label_distribution",
                "status": "passed" if label_valid > 85000 and label_classes == 3 else "failed",
                "observed": f"valid={label_valid};classes={label_classes}",
                "expected": "valid>85000;classes=3",
                "evidence": rel(JL_INPUT_FRAME),
                "effect": "profit quality label(수익 품질 라벨)이 학습 가능한지 확인한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ]
    )


def tier_records(final_jk: Mapping[str, Any]) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "view": "Tier A separate(Tier A 분리)",
                "tier": "Tier A",
                "metric_scope": "input_materialization",
                "source": rel(jk.FINAL_DECISION),
                "net_profit": final_jk.get("positive_net_profit", ""),
                "profit_factor": final_jk.get("positive_profit_factor", ""),
                "recovery_factor": final_jk.get("positive_recovery_factor", ""),
                "drawdown": final_jk.get("positive_drawdown", ""),
                "trade_count": final_jk.get("positive_trade_count", ""),
                "status": "materialized_from_tier_a_positive_clue(티어 A 긍정 단서 기반 물질화)",
                "effect": "현재 입력이 Tier A(티어 A) 근거에서 왔음을 기록한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "view": "Tier B separate(Tier B 분리)",
                "tier": "Tier B",
                "metric_scope": "missing_required",
                "source": rel(JL_TIER_RECORDS),
                "status": "missing_required",
                "effect": "Tier B(티어 B) 부재를 숨기지 않는다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "view": "Tier A+B combined(Tier A+B 합산)",
                "tier": "Tier A+B",
                "metric_scope": "missing_required",
                "source": rel(JL_TIER_RECORDS),
                "status": "missing_required",
                "effect": "합산 결과가 없음을 명시한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ]
    )


def runtime_parity_plan(final_jk: Mapping[str, Any]) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "plan_id": "jl_runtime_parity_guard",
                "source_positive_model_id": final_jk.get("positive_clue_model_id", ""),
                "negative_control_model_id": final_jk.get("negative_control_model_id", ""),
                "input_frame": rel(JL_INPUT_FRAME),
                "allowed_features": rel(JL_ALLOWED_FEATURES),
                "required_guard": "ONNX parity(ONNX 동등성), feature order hash(피처 순서 해시), proxy-MT5 diff(프록시-MT5 차이), exact decision comparison(정확 결정 비교)",
                "forbidden_use": "runtime authority(런타임 권위), operating promotion(운영 승격), Goal Achieve(목표 달성)",
                "effect": "JL 입력이 나중에 MT5 runtime probe(MT5 런타임 탐침)와 반드시 비교되게 한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )


def task_seeds(final_jk: Mapping[str, Any]) -> pd.DataFrame:
    positive_model = str(final_jk.get("positive_clue_model_id", ""))
    negative_model = str(final_jk.get("negative_control_model_id", ""))
    tasks = [
        ("jl_jk001_pf_recovery_profit_quality_xgboost", "PF recovery profit quality(PF 회복 수익 품질)", "jl_label_class_profit_quality_fwd18", "jl_valid_profit_quality_fwd18", "jl_pf_recovery_profit_quality_weight", "XGBoost(엑스지부스트)_multiclass", "xgboost_jl_fwd18_pf_recovery_profit_quality", positive_model, "PF/recovery(수익 팩터/회복) 개선 후보를 만든다."),
        ("jl_jk002_drawdown_compression_fwd6_lgbm", "drawdown holding loss guard(낙폭 보유손실 보호)", "hx_label_class_fwd6", "hx_valid_fwd6", "jl_drawdown_holding_loss_guard_weight", "LightGBM(라이트GBM)_multiclass", "lgbm_jl_fwd6_drawdown_compression", positive_model, "짧은 보유 손실을 줄인다."),
        ("jl_jk003_density_throttle_short_edge_extratrees", "density throttle short edge(밀도 제한 숏 우위)", "jl_label_class_density_throttle_fwd18", "jl_valid_density_throttle_fwd18", "jl_density_throttle_short_edge_weight", "ExtraTrees(엑스트라트리즈)_multiclass", "extratrees_jl_fwd18_density_short_edge", positive_model, "과도한 신호 밀도와 비용 노출을 낮춘다."),
        ("jl_jk004_long_quarantine_short_preserve_xgboost", "long quarantine short preserve(롱 격리 숏 보존)", "hx_label_class_fwd18", "hx_valid_fwd18", "jl_long_loss_quarantine_short_preserve_weight", "XGBoost(엑스지부스트)_multiclass", "xgboost_jl_fwd18_long_quarantine_short_preserve", positive_model, "약한 롱 손실과 숏 우위를 분리한다."),
        ("jl_jk005_negative_control_firewall_lgbm", "negative control firewall(부정 대조 방화벽)", "jd_label_class_runtime_pnl_fwd18", "jd_valid_runtime_pnl_fwd18", "jl_negative_control_session_regime_firewall_weight", "LightGBM(라이트GBM)_multiclass", "lgbm_jl_fwd18_negative_control_firewall", negative_model, "세션/국면 실패 패턴 반복을 막는다."),
        ("jl_jk006_cost_stress_buffer_extratrees", "cost stress slippage buffer(비용 압박 슬리피지 버퍼)", "jl_label_class_profit_quality_fwd18", "jl_valid_profit_quality_fwd18", "jl_cost_stress_slippage_buffer_weight", "ExtraTrees(엑스트라트리즈)_multiclass", "extratrees_jl_fwd18_cost_stress_buffer", positive_model, "낮은 PF(수익 팩터)의 비용 취약성을 줄인다."),
        ("jl_jk007_equity_smoothness_recovery_xgboost", "equity smoothness recovery(수익곡선 평활 회복)", "hx_label_class_fwd24", "hx_valid_fwd24", "jl_equity_smoothness_recovery_weight", "XGBoost(엑스지부스트)_multiclass", "xgboost_jl_fwd24_equity_smoothness_recovery", positive_model, "수익곡선 품질과 회복 계수를 압박한다."),
        ("jl_jk008_router_blend_scout_lgbm", "router blend scout(라우터 혼합 정찰)", "jd_label_class_runtime_pnl_fwd18", "jd_valid_runtime_pnl_fwd18", "jl_router_blend_scout_weight", "LightGBM(라이트GBM)_multiclass", "lgbm_jl_fwd18_router_blend_scout", f"{positive_model};{negative_model}", "이중 탐침 구조를 후보로 넓힌다."),
    ]
    return pd.DataFrame(
        [
            {
                "task_id": task_id,
                "repair_family": family,
                "target_column": target,
                "valid_column": valid,
                "sample_weight_column": weight,
                "model_family": model_family,
                "model_config_id": config,
                "base_clue_model_id": base_model,
                "expected_effect": effect,
                "input_frame": rel(JL_INPUT_FRAME),
                "allowed_features": rel(JL_ALLOWED_FEATURES),
                "required_guard": "drop invalid rows; no threshold tuning; review before training(무효 행 제외, 임계값 조정 없음, 학습 전 검토)",
                "forbidden_use": "candidate selection, MT5 claim, runtime authority(후보 선정, MT5 주장, 런타임 권위)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
            for task_id, family, target, valid, weight, model_family, config, base_model, effect in tasks
        ]
    )


def review_queue() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "queue_id": "run337JM_review_jl_inputs",
                "source_run_id": RUN_ID,
                "next_run_id": NEXT_RUN_ID,
                "task": "review_runtime_positive_low_pf_recovery_drawdown_dual_probe_repair_inputs(런타임 양수 저PF/저회복/낙폭 이중 탐침 수리 입력 검토)",
                "required_inputs": ";".join([rel(JL_INPUT_FRAME), rel(JL_ALLOWED_FEATURES), rel(JL_WEIGHT_AUDIT), rel(JL_FEATURE_BOUNDARY), rel(JL_TASK_SEEDS)]),
                "expected_outputs": "input eligibility review(입력 적격성 검토); leakage audit(누출 감사); training readiness(학습 준비도); JN queue(JN 대기열)",
                "blocked_if_missing": "feature boundary pass(피처 경계 통과), finite weights(유한 가중치), label distribution(라벨 분포), Tier records(티어 기록)",
                "effect": "학습 전에 누출과 가중치 이상을 먼저 막는다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )


def build_outputs() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, dict[str, Any]]:
    final_jk = read_json(jk.FINAL_DECISION)
    frame = materialize_frame(read_source_frame())
    allowed = allowed_features_copy()
    ensure_parent(JL_INPUT_FRAME)
    frame.to_parquet(io(JL_INPUT_FRAME), index=False)
    write_csv(JL_ALLOWED_FEATURES, allowed)

    sources = source_map(frame)
    recipes = weight_recipe()
    weights = weight_audit(frame)
    boundary = feature_boundary(allowed, frame)
    tiers = tier_records(final_jk)
    runtime_plan = runtime_parity_plan(final_jk)
    tasks = task_seeds(final_jk)
    queue = review_queue()

    valid_profit = int(num(frame, "jl_valid_profit_quality_fwd18", 0).sum())
    label_classes = int(pd.Series(frame["jl_label_class_profit_quality_fwd18"]).nunique())
    nonfinite_weights = int(weights["nonfinite_rows"].sum())
    saturation_share = float(weights["max_saturation_rate"].astype(float).max())
    forbidden_count = len(forbidden_feature_violations(allowed["feature_name"].astype(str).tolist()))
    summary = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_action": NEXT_RUN_ID,
        "rows": int(len(frame)),
        "columns": int(len(frame.columns)),
        "feature_count": int(len(allowed)),
        "feature_order_hash": feature_hash(allowed["feature_name"].astype(str).tolist()),
        "weight_columns": int(len(JL_WEIGHT_COLUMNS)),
        "target_columns": int(len(JL_TARGET_COLUMNS)),
        "task_seed_rows": int(len(tasks)),
        "valid_profit_quality_rows": valid_profit,
        "profit_quality_label_classes": label_classes,
        "nonfinite_weight_rows": nonfinite_weights,
        "weight_saturation_share": saturation_share,
        "feature_boundary_violations": forbidden_count,
        "tier_record_rows": int(len(tiers)),
        "runtime_parity_plan_rows": int(len(runtime_plan)),
        "positive_clue_model_id": final_jk.get("positive_clue_model_id", ""),
        "negative_control_model_id": final_jk.get("negative_control_model_id", ""),
        "source_frame": rel(BASE_INPUT_FRAME),
        "input_frame": rel(JL_INPUT_FRAME),
        "allowed_features": rel(JL_ALLOWED_FEATURES),
        "candidate_selection": "not_run",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "mt5_runtime_probe": "not_run_in_jl",
        "live_readiness": "not_claimed",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    return frame, sources, recipes, weights, boundary, tiers, runtime_plan, tasks, queue, summary


def gate_row(gate: str, status: str, observed: Any, expected: Any, evidence: Path, effect: str) -> dict[str, Any]:
    return {
        "gate_id": gate,
        "status": status,
        "observed": observed,
        "expected": expected,
        "evidence_path": rel(evidence),
        "effect": effect,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def make_gates(summary: Mapping[str, Any]) -> pd.DataFrame:
    parent_gates = read_csv(jk.GATE_AUDIT)
    no_forbidden = (
        summary["candidate_selection"] == "not_run"
        and summary["forward_passed"] == "not_claimed"
        and summary["forward_failed"] == "not_claimed"
        and summary["goal_achieve"] == "not_claimed"
        and summary["runtime_authority"] == "not_claimed"
        and summary["operating_promotion"] == "not_claimed"
    )
    return pd.DataFrame(
        [
            gate_row("parent_jk_gates_passed", "passed" if passed_status(parent_gates["status"]).all() else "failed", "all passed" if passed_status(parent_gates["status"]).all() else "failed parent gate", "all passed", jk.GATE_AUDIT, "JK design(JK 설계) 통과 뒤 물질화한다."),
            gate_row("input_frame_written", "passed" if exists(JL_INPUT_FRAME) and summary["rows"] >= 87600 else "failed", summary["rows"], ">=87600", JL_INPUT_FRAME, "입력 frame(프레임)을 손실 없이 생성한다."),
            gate_row("allowed_feature_count_preserved", "passed" if summary["feature_count"] == 58 else "failed", summary["feature_count"], "58", JL_ALLOWED_FEATURES, "기존 58개 pretrade feature(사전거래 피처)를 유지한다."),
            gate_row("feature_boundary_passed", "passed" if summary["feature_boundary_violations"] == 0 else "failed", summary["feature_boundary_violations"], "0", JL_FEATURE_BOUNDARY, "feature/label boundary(피처/라벨 경계)를 지킨다."),
            gate_row("weight_columns_materialized", "passed" if summary["weight_columns"] == 8 and exists(JL_WEIGHT_AUDIT) else "failed", summary["weight_columns"], "8", JL_WEIGHT_AUDIT, "학습 전용 가중치를 모두 만든다."),
            gate_row("weights_finite", "passed" if summary["nonfinite_weight_rows"] == 0 else "failed", summary["nonfinite_weight_rows"], "0", JL_WEIGHT_AUDIT, "비유한 가중치를 막는다."),
            gate_row("weight_saturation_controlled", "passed" if summary["weight_saturation_share"] <= 0.20 else "failed", summary["weight_saturation_share"], "<=0.20", JL_WEIGHT_AUDIT, "가중치 과포화를 막는다."),
            gate_row("profit_quality_label_distribution", "passed" if summary["valid_profit_quality_rows"] > 85000 and summary["profit_quality_label_classes"] == 3 else "failed", f"valid={summary['valid_profit_quality_rows']};classes={summary['profit_quality_label_classes']}", "valid>85000;classes=3", JL_INPUT_FRAME, "profit quality label(수익 품질 라벨)이 학습 가능한지 확인한다."),
            gate_row("task_seeds_written", "passed" if exists(JL_TASK_SEEDS) and summary["task_seed_rows"] >= 8 else "failed", summary["task_seed_rows"], ">=8", JL_TASK_SEEDS, "다음 학습 후보를 충분히 연다."),
            gate_row("tier_pair_records_written", "passed" if exists(JL_TIER_RECORDS) and summary["tier_record_rows"] == 3 else "failed", summary["tier_record_rows"], "3", JL_TIER_RECORDS, "Tier A/B 기록을 생략하지 않는다."),
            gate_row("runtime_parity_plan_written", "passed" if exists(JL_RUNTIME_PARITY_PLAN) and summary["runtime_parity_plan_rows"] >= 1 else "failed", summary["runtime_parity_plan_rows"], ">=1", JL_RUNTIME_PARITY_PLAN, "proxy-MT5 비교 필수 조건을 남긴다."),
            gate_row("review_queue_written", "passed" if exists(JM_QUEUE) else "failed", exists(JM_QUEUE), "true", JM_QUEUE, "JM input review(JM 입력 검토)로 연결한다."),
            gate_row("no_forbidden_operating_claim", "passed" if no_forbidden else "failed", "not_claimed", "not_claimed", CLAIM_RECEIPT, "selection/forward/runtime authority/Goal(선정/전진/런타임 권위/목표) 주장을 하지 않는다."),
            gate_row("required_gate_coverage_audit_written", "passed", "written", "written", GATE_AUDIT, "gate coverage(게이트 커버리지)를 closeout(종료 기록)에 연결한다."),
        ]
    )


def write_receipts(summary: Mapping[str, Any]) -> None:
    base = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "created_at_utc": now_utc(),
        "status": STATUS,
        "judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(RUN_EVIDENCE_RECEIPT, {**base, "input_frame": summary["input_frame"], "rows": summary["rows"], "features": summary["feature_count"], "tasks": summary["task_seed_rows"], "next_run_id": NEXT_RUN_ID})
    write_json(DATA_RECEIPT, {**base, "source_frame": summary["source_frame"], "time_axis": "closed-bar timestamp(마감봉 시각)", "feature_boundary": rel(JL_FEATURE_BOUNDARY), "label_boundary": "future labels only as targets/weights(미래 라벨은 목표/가중치로만 사용)", "integrity_judgment": "materialized_review_required(물질화 완료, 검토 필요)"})
    write_json(MODEL_RECEIPT, {**base, "model_training": "not_run(실행 안 함)", "task_seed_matrix": rel(JL_TASK_SEEDS), "allowed_features": rel(JL_ALLOWED_FEATURES), "threshold_policy": "no threshold tuning(임계값 조정 없음)", "validation_judgment": "input_materialized_review_required(입력 물질화, 검토 필요)"})
    write_json(PERFORMANCE_RECEIPT, {**base, "positive_clue_model_id": summary["positive_clue_model_id"], "negative_control_model_id": summary["negative_control_model_id"], "repair_axes": list(JL_WEIGHT_COLUMNS), "effect": "PF/recovery/drawdown/cost/side/equity(수익 팩터/회복/낙폭/비용/방향/수익곡선) 수리를 학습 입력으로 바꾼다."})
    write_json(RUNTIME_RECEIPT, {**base, "runtime_execution": "not_run_in_jl(JL에서 실행 안 함)", "runtime_plan": rel(JL_RUNTIME_PARITY_PLAN), "parent_runtime_evidence": [rel(jk.jj.RUNTIME_REVIEW), rel(jk.jj.ji.PROXY_MT5_DIFF)], "runtime_claim_boundary": "runtime_probe_required_later(나중에 런타임 탐침 필요)"})
    write_json(JUDGMENT_RECEIPT, {**base, "judgment_label": JUDGMENT, "evidence_available": [rel(JL_INPUT_FRAME), rel(JL_WEIGHT_AUDIT), rel(GATE_AUDIT)], "next_condition": NEXT_RUN_ID, "candidate_selection": "not_run(실행 안 함)"})
    write_json(CLAIM_RECEIPT, {**base, "candidate_selection": "not_run", "forward_passed": "not_claimed", "forward_failed": "not_claimed", "runtime_authority": "not_claimed", "operating_promotion": "not_claimed", "live_readiness": "not_claimed", "goal_achieve": "not_claimed"})
    write_json(LINEAGE_RECEIPT, {**base, "source_inputs": [rel(path) for path in INPUT_FILES], "producer": rel(Path(__file__)), "consumer": NEXT_RUN_ID, "artifact_paths": [rel(path) for path in OUTPUT_FILES if exists(path)], "artifact_hashes": {rel(path): sha(path) for path in OUTPUT_FILES if exists(path) and io(path).is_file()}, "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)], "lineage_judgment": "connected_with_boundary(경계 조건부 연결)"})


def write_final(summary: Mapping[str, Any], gates: pd.DataFrame) -> dict[str, Any]:
    final = {**dict(summary), "gate_passes": int(gates["status"].astype(str).eq("passed").sum()), "gate_total": int(len(gates))}
    write_json(FINAL_DECISION, final)
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "created_at": TODAY,
            "created_at_utc": now_utc(),
            "script": rel(Path(__file__)),
            "inputs": [rel(path) for path in INPUT_FILES],
            "outputs": [rel(path) for path in OUTPUT_FILES if exists(path)],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    return final


def write_docs(final: Mapping[str, Any]) -> None:
    report = f"""# run337JL Positive Low PF Recovery Drawdown Repair Inputs(run337JL 양수 저PF 회복 낙폭 수리 입력)

## Summary(요약)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- judgment(판정): `{JUDGMENT}`
- gates(게이트): `{final['gate_passes']}/{final['gate_total']}`
- rows(행): `{final['rows']}`
- feature_count(피처 수): `{final['feature_count']}`
- weight_columns(가중치 열): `{final['weight_columns']}`
- task_seed_rows(작업 씨앗 행): `{final['task_seed_rows']}`
- positive_clue_model(긍정 단서 모델): `{final['positive_clue_model_id']}`
- negative_control_model(부정 대조 모델): `{final['negative_control_model_id']}`

## Action(행동)

JD input frame(JD 입력 프레임)에 JL train-only label/weight(학습 전용 라벨/가중치)를 추가했다.
Effect(효과): PF/recovery/drawdown/cost/side/equity(수익 팩터/회복/낙폭/비용/방향/수익곡선) 수리를 다음 JM review(JM 검토)와 JN training(JN 학습) 후보로 넘긴다.

## Boundary(경계)

No training(학습 없음), no candidate selection(후보 선정 없음), no MT5 execution(MT5 실행 없음), no runtime authority(런타임 권위 없음), no Goal Achieve(목표 달성 없음).
"""
    decision = f"""# {TODAY} Stage337JL Decision(337JL 결정)

- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- evidence(근거): `{rel(JL_INPUT_FRAME)}`, `{rel(JL_WEIGHT_AUDIT)}`, `{rel(JL_TASK_SEEDS)}`

Action(행동): JK design(JK 설계)을 timestamp-safe(시점 안전) input materialization(입력 물질화)로 바꿨다.
Effect(효과): 학습 전에 leakage(누출), feature boundary(피처 경계), weight health(가중치 상태)를 JM에서 검토할 수 있다.

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

JL materialization(JL 입력 물질화)은 JK repair design(JK 수리 설계)을 실제 학습 입력으로 만들었고, 아직 training(학습)이나 selection(선정)은 하지 않았다.

## Claim Boundary(주장 경계)

`{CLAIM_BOUNDARY}`
"""
    selection = f"""# Stage337 Selection Status(337단계 선택 상태)

- latest_run(최신 실행): `{RUN_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- selected_model(선정 모델): `none(없음)`
- positive_clue_model(긍정 단서 모델): `{final['positive_clue_model_id']}`
- negative_control_model(부정 대조 모델): `{final['negative_control_model_id']}`
- runtime_authority(런타임 권위): `not_claimed(주장 없음)`
- operating_promotion(운영 승격): `not_claimed(주장 없음)`
- live_readiness(실거래 준비): `not_claimed(주장 없음)`
- goal_achieve(목표 달성): `not_claimed(주장 없음)`

Effect(효과): input materialization(입력 물질화)을 model selection(모델 선정)으로 오해하지 않게 한다.
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
    write_bom_text(REPORT_PATH, report)
    write_bom_text(DECISION_DOC, decision)
    write_bom_text(CURRENT_WORKING_STATE, current)
    write_bom_text(SELECTION_STATUS, selection)
    write_bom_text(ROOT_SELECTION_STATUS, selection)
    write_bom_text(WORKSPACE_STATE, workspace)
    marker = f"run337JL {RUN_ID}"
    append_text_once(
        STAGE_BRIEF,
        marker,
        f"""## run337JL Positive Low PF Recovery Drawdown Repair Inputs(양수 저PF 회복 낙폭 수리 입력)

- run_id(실행 ID): `{RUN_ID}`
- judgment(판정): `{JUDGMENT}`
- rows(행): `{final['rows']}`
- task_seed_rows(작업 씨앗 행): `{final['task_seed_rows']}`
- effect(효과): JK 설계를 JM review(JM 검토) 가능한 입력으로 물질화했다.
""",
    )
    changelog = f"""## {TODAY} run337JL Positive Low PF Recovery Drawdown Repair Inputs(양수 저PF 회복 낙폭 수리 입력)

- action(행동): `{final['rows']}`개 행과 `{final['task_seed_rows']}`개 task seed(작업 씨앗)를 만들었다.
- effect(효과): PF/recovery/drawdown/cost/side/equity(수익 팩터/회복/낙폭/비용/방향/수익곡선) 수리 후보를 JM review(JM 검토)로 넘겼다.
- boundary(경계): selected model(선정 모델), MT5 execution(MT5 실행), Goal Achieve(목표 달성)는 없다.
"""
    append_text_once(ROOT_CHANGELOG, marker, changelog)
    append_text_once(WORKSPACE_CHANGELOG, marker, changelog)


def update_registers(final: Mapping[str, Any]) -> None:
    base = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "run_date": TODAY,
        "run_number": RUN_NUMBER,
        "lane": "runtime_positive_low_pf_recovery_drawdown_dual_probe_repair_input_materialization",
        "family": "experiment_execution",
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_run_id": NEXT_RUN_ID,
        "rows": final["rows"],
        "notes": f"rows={final['rows']};features={final['feature_count']};weights={final['weight_columns']};tasks={final['task_seed_rows']};next_action={NEXT_RUN_ID};goal_achieve_not_claimed.",
        "primary_artifact": rel(FINAL_DECISION),
        "primary_report": rel(REPORT_PATH),
        "report_path": rel(REPORT_PATH),
        "gate_passes": final["gate_passes"],
        "gate_total": final["gate_total"],
        "claim_boundary": CLAIM_BOUNDARY,
    }
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], base)
    rows = [
        {**base, "view": "Tier A separate(Tier A 분리)", "tier": "Tier A", "metric_scope": "input_materialization", "candidate_model_id": final["positive_clue_model_id"], "result_status": JUDGMENT},
        {**base, "view": "Tier B separate(Tier B 분리)", "tier": "Tier B", "metric_scope": "missing_required", "result_status": "missing_required"},
        {**base, "view": "Tier A+B combined(Tier A+B 합산)", "tier": "Tier A+B", "metric_scope": "missing_required", "result_status": "missing_required"},
    ]
    for row in rows:
        append_or_replace_csv(PROJECT_LEDGER, ["run_id", "view"], row)
        append_or_replace_csv(STAGE_LEDGER, ["run_id", "view"], row)


def artifact_type(path: Path) -> str:
    return "report" if path.suffix.lower() == ".md" else path.suffix.lower().lstrip(".")


def update_artifact_registry(paths: Sequence[Path]) -> None:
    registry = read_csv(ARTIFACT_REGISTRY) if exists(ARTIFACT_REGISTRY) else pd.DataFrame()
    required = ["stage_id", "run_id", "artifact_type", "path", "sha256", "created_at", "claim_boundary"]
    for column in required:
        if column not in registry.columns:
            registry[column] = ""
    rows = []
    for path in paths:
        if exists(path) and io(path).is_file():
            rows.append({"stage_id": STAGE_ID, "run_id": RUN_ID, "artifact_type": artifact_type(path), "path": rel(path), "sha256": sha(path), "created_at": TODAY, "claim_boundary": CLAIM_BOUNDARY})
    if rows:
        registry = registry.loc[~registry["path"].astype(str).isin({row["path"] for row in rows})].copy()
        registry = pd.concat([registry, pd.DataFrame(rows)], ignore_index=True)
        write_csv(ARTIFACT_REGISTRY, registry[list(dict.fromkeys(required + list(registry.columns)))])


def main() -> None:
    for path in (RUN_DIR, REVIEW_DIR, DECISION_DOC.parent):
        io(path).mkdir(parents=True, exist_ok=True)
    missing = [rel(path) for path in INPUT_FILES if not exists(path)]
    if missing:
        raise FileNotFoundError(f"missing required input files: {missing}")

    _frame, sources, recipes, weights, boundary, tiers, runtime_plan, tasks, queue, summary = build_outputs()
    write_csv(JL_SOURCE_MAP, sources)
    write_csv(JL_WEIGHT_RECIPE, recipes)
    write_csv(JL_WEIGHT_AUDIT, weights)
    write_csv(JL_FEATURE_BOUNDARY, boundary)
    write_csv(JL_TIER_RECORDS, tiers)
    write_csv(JL_RUNTIME_PARITY_PLAN, runtime_plan)
    write_csv(JL_TASK_SEEDS, tasks)
    write_csv(JM_QUEUE, queue)
    gates = make_gates(summary)
    write_csv(GATE_AUDIT, gates)
    write_receipts(summary)
    final = write_final(summary, gates)
    write_docs(final)
    update_registers(final)
    update_artifact_registry(OUTPUT_FILES)

    failed = gates.loc[~gates["status"].astype(str).eq("passed")]
    if not failed.empty:
        raise RuntimeError(f"JL gates failed: {failed[['gate_id', 'status']].to_dict(orient='records')}")

    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "rows": final["rows"],
                "feature_count": final["feature_count"],
                "weight_columns": final["weight_columns"],
                "task_seed_rows": final["task_seed_rows"],
                "gates": f"{final['gate_passes']}/{final['gate_total']}",
                "next_action": NEXT_RUN_ID,
                "goal_achieve": "not_claimed",
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
