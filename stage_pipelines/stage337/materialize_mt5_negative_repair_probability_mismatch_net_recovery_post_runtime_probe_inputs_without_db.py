from __future__ import annotations

import json
import math
import re
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import json_ready, path_exists  # noqa: E402
from stage_pipelines.stage337 import design_mt5_negative_repair_probability_mismatch_net_recovery_post_runtime_probe_without_db as hh  # noqa: E402
from stage_pipelines.stage337 import materialize_mt5_negative_repair_lgbm_probability_mismatch_net_recovery_inputs_without_db as ha  # noqa: E402


aw = hh.aw
fb = hh.fb
he = hh.he

TODAY = "2026-05-31"
STAGE_ID = hh.STAGE_ID
RUN_NUMBER = "run337HI"
RUN_ID = "run337HI_materialize_mt5_negative_repair_probability_mismatch_net_recovery_post_runtime_probe_inputs_without_db_v1"
PARENT_RUN_ID = hh.RUN_ID
NEXT_RUN_ID = "run337HJ_review_mt5_negative_repair_probability_mismatch_net_recovery_post_runtime_probe_inputs_without_db_v1"
STATUS = "completed_stage337HI_post_runtime_probe_repair_inputs_materialized_no_training_no_selection"
JUDGMENT = "timestamp_safe_hh_activation_cost_session_regime_parity_repair_inputs_materialized_review_required"
DECISION = "stage337HI_open_run337HJ_review_post_runtime_probe_repair_inputs"
CLAIM_BOUNDARY = (
    "research_development_only_stage337HI_post_runtime_probe_repair_inputs_without_db_"
    "no_model_training_no_threshold_tuning_no_lot_optimization_no_operating_selection_no_mt5_execution_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = hh.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = hh.REVIEWS_DIR
REPORT_PATH = REVIEWS_DIR / "run337HI_post_runtime_probe_repair_inputs.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage337HI_post_runtime_probe_repair_inputs.md"

HH_FINAL = hh.FINAL_DECISION
HH_GATES = hh.GATE_AUDIT
HH_QUEUE = hh.MATERIALIZATION_QUEUE
HH_DESIGN = hh.DESIGN_MATRIX
HH_EXPERIMENT = hh.EXPERIMENT_CONTRACT
HH_OBJECTIVE = hh.OBJECTIVE_CONTRACT
HH_FEATURE_LABEL = hh.FEATURE_LABEL_CONTRACT
HH_TASK_BLUEPRINT = hh.TRAINING_TASK_BLUEPRINT
HH_PARITY_PLAN = hh.PARITY_REPAIR_PLAN
HH_TRADE_PLAN = hh.TRADE_ACTIVATION_PLAN
HH_POSITIVE_SEED = hh.POSITIVE_SEED_PLAN
HH_NEGATIVE = hh.NEGATIVE_CONTROL_PLAN
HH_RELEASE = hh.RELEASE_GATE_CONTRACT
HG_KPI = hh.HG_KPI
HG_PARITY = hh.HG_PARITY
HG_TIMESTAMP = hh.HG_TIMESTAMP
HG_MEMORY = hh.HG_MEMORY

BASE_FRAME = ha.TRAIN_ONLY_REPAIR_FRAME
BASE_FEATURES = ha.ALLOWED_FEATURE_SET
BASE_MANIFEST = ha.RUN_MANIFEST
BASE_WEIGHT_AUDIT = ha.WEIGHT_AUDIT
BASE_FEATURE_BOUNDARY = ha.FEATURE_LABEL_BOUNDARY

TRAIN_ONLY_REPAIR_FRAME = RUN_DIR / "train_only_post_runtime_probe_repair_input_frame.parquet"
MATERIALIZATION_SOURCE_MAP = RUN_DIR / "hi_materialization_source_map.csv"
ALLOWED_FEATURE_SET = RUN_DIR / "hi_allowed_model_feature_set.csv"
WEIGHT_RECIPE_MATRIX = RUN_DIR / "hh_repair_weight_recipe_matrix.csv"
WEIGHT_AUDIT = RUN_DIR / "hh_repair_weight_audit.csv"
TARGET_CONTRACT_AUDIT = RUN_DIR / "target_contract_audit.csv"
PARITY_PRECISION_AUDIT = RUN_DIR / "probability_precision_audit.csv"
FEATURE_LABEL_BOUNDARY = RUN_DIR / "feature_label_boundary_audit.csv"
POSITIVE_SEED_MATERIALIZATION = RUN_DIR / "positive_seed_materialization_matrix.csv"
NEGATIVE_CONTROL_MATERIALIZATION = RUN_DIR / "negative_control_materialization_matrix.csv"
RELEASE_GATE_MATERIALIZATION = RUN_DIR / "release_gate_materialization_matrix.csv"
TRAINING_TASK_SEEDS = RUN_DIR / "run337HK_training_task_seed_matrix.csv"
HJ_QUEUE = RUN_DIR / "run337HJ_review_queue.csv"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
RUN_EVIDENCE_RECEIPT = RUN_DIR / "run_evidence_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_discipline_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (
    HH_FINAL,
    HH_GATES,
    HH_QUEUE,
    HH_DESIGN,
    HH_EXPERIMENT,
    HH_OBJECTIVE,
    HH_FEATURE_LABEL,
    HH_TASK_BLUEPRINT,
    HH_PARITY_PLAN,
    HH_TRADE_PLAN,
    HH_POSITIVE_SEED,
    HH_NEGATIVE,
    HH_RELEASE,
    HG_KPI,
    HG_PARITY,
    HG_TIMESTAMP,
    HG_MEMORY,
    BASE_FRAME,
    BASE_FEATURES,
    BASE_MANIFEST,
    BASE_WEIGHT_AUDIT,
    BASE_FEATURE_BOUNDARY,
)
OUTPUT_FILES = (
    TRAIN_ONLY_REPAIR_FRAME,
    MATERIALIZATION_SOURCE_MAP,
    ALLOWED_FEATURE_SET,
    WEIGHT_RECIPE_MATRIX,
    WEIGHT_AUDIT,
    TARGET_CONTRACT_AUDIT,
    PARITY_PRECISION_AUDIT,
    FEATURE_LABEL_BOUNDARY,
    POSITIVE_SEED_MATERIALIZATION,
    NEGATIVE_CONTROL_MATERIALIZATION,
    RELEASE_GATE_MATERIALIZATION,
    TRAINING_TASK_SEEDS,
    HJ_QUEUE,
    DATA_RECEIPT,
    MODEL_RECEIPT,
    RUNTIME_RECEIPT,
    RUN_EVIDENCE_RECEIPT,
    PERFORMANCE_RECEIPT,
    JUDGMENT_RECEIPT,
    CLAIM_RECEIPT,
    LINEAGE_RECEIPT,
    GATE_AUDIT,
    FINAL_DECISION,
    RUN_MANIFEST,
    REPORT_PATH,
    DECISION_DOC,
    he.SELECTED_STATUS,
    he.WORKSPACE_STATE,
    he.CURRENT_STATE,
    he.CHANGELOG,
    he.STAGE_BRIEF,
    he.RUN_REGISTRY,
    he.ALPHA_LEDGER,
    he.STAGE_LEDGER,
    he.ARTIFACT_REGISTRY,
    Path(__file__),
)

NEW_WEIGHT_COLUMNS = (
    "hh_activation_cost_session_regime_weight",
    "hh_loss_tail_drawdown_recovery_weight",
    "hh_probability_precision_margin_weight",
    "hh_proxy_mt5_negative_control_weight",
    "hh_balanced_release_ladder_weight",
)
TASK_WEIGHT_COLUMNS = {
    "hi_hh001_activation_cost_session_regime_guard": "hh_activation_cost_session_regime_weight",
    "hi_hh002_loss_tail_drawdown_recovery": "hh_loss_tail_drawdown_recovery_weight",
    "hi_hh003_probability_precision_margin": "hh_probability_precision_margin_weight",
    "hi_hh004_proxy_mt5_negative_control": "hh_proxy_mt5_negative_control_weight",
    "hi_hh005_balanced_release_ladder": "hh_balanced_release_ladder_weight",
}
FORBIDDEN_FEATURE_TOKENS = (
    "label",
    "future",
    "claim_boundary",
    "net_profit",
    "profit_factor",
    "recovery",
    "drawdown",
    "expectancy",
)

SOURCE_COLUMNS = ("source_id", "source_path", "source_type", "required", "exists", "sha256", "effect", "claim_boundary")
WEIGHT_RECIPE_COLUMNS = (
    "recipe_id",
    "materialized_column",
    "source_columns",
    "train_only_formula",
    "lower_bound",
    "upper_bound",
    "expected_effect",
    "claim_boundary",
)
WEIGHT_AUDIT_COLUMNS = (
    "weight_column",
    "rows",
    "weight_min",
    "weight_mean",
    "weight_max",
    "nonfinite_rows",
    "short_label_mean",
    "flat_label_mean",
    "long_label_mean",
    "effect",
    "claim_boundary",
)
AUDIT_COLUMNS = ("audit_id", "status", "observed", "expected", "evidence", "effect", "claim_boundary")
TASK_SEED_COLUMNS = (
    "task_id",
    "target_column",
    "sample_weight_column",
    "sample_weight_expression",
    "model_family",
    "model_config_id",
    "positive_seed_source",
    "failure_memory_source",
    "selection_status",
    "required_guard",
    "expected_effect",
    "forbidden_use",
    "claim_boundary",
)
QUEUE_COLUMNS = (
    "queue_id",
    "next_run_id",
    "priority",
    "task",
    "required_inputs",
    "required_outputs",
    "blocked_if_missing",
    "forbidden_action",
    "effect",
    "claim_boundary",
)
GATE_COLUMNS = ("gate_id", "status", "evidence_path", "observed", "expected", "effect", "claim_boundary")


def now_utc() -> str:
    return datetime.now(tz=UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    return aw.rel(path)


def read_csv(path: Path) -> list[dict[str, str]]:
    return aw.read_csv(path)


def read_json(path: Path) -> dict[str, Any]:
    return aw.read_json(path)


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> Path:
    return aw.write_csv(path, columns, rows)


def write_json(path: Path, payload: Mapping[str, Any] | Sequence[Any]) -> Path:
    aw.io_path(path.parent).mkdir(parents=True, exist_ok=True)
    aw.io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def fail_if_missing(paths: Sequence[Path]) -> list[Path]:
    return [path for path in paths if not path_exists(path)]


def as_float(value: Any) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return 0.0
    return number if math.isfinite(number) else 0.0


def as_int(value: Any) -> int:
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return 0


def numeric(frame: pd.DataFrame, column: str, default: float = 0.0) -> pd.Series:
    if column not in frame.columns:
        return pd.Series(default, index=frame.index, dtype="float64")
    return pd.to_numeric(frame[column], errors="coerce").replace([np.inf, -np.inf], np.nan).fillna(default).astype("float64")


def normalize(values: pd.Series | np.ndarray, default: float = 0.5) -> pd.Series:
    series = pd.Series(values, copy=False).replace([np.inf, -np.inf], np.nan).astype("float64")
    if series.notna().sum() == 0:
        return pd.Series(default, index=series.index, dtype="float64")
    lo = float(series.quantile(0.05))
    hi = float(series.quantile(0.95))
    if not math.isfinite(lo) or not math.isfinite(hi) or hi <= lo:
        return pd.Series(default, index=series.index, dtype="float64")
    return ((series.fillna(series.median()) - lo) / (hi - lo)).clip(0.0, 1.0)


def clip_weight(values: pd.Series | np.ndarray, lower: float = 0.10, upper: float = 10.0) -> pd.Series:
    return pd.Series(values, copy=False).replace([np.inf, -np.inf], np.nan).fillna(1.0).clip(lower=lower, upper=upper)


def precision_margin(frame: pd.DataFrame) -> tuple[pd.Series, pd.Series]:
    probs = pd.DataFrame(
        {
            "short": numeric(frame, "mean_prob_short", default=0.33),
            "flat": numeric(frame, "mean_prob_flat", default=0.34),
            "long": numeric(frame, "mean_prob_long", default=0.33),
        },
        index=frame.index,
    )
    sorted_probs = np.sort(probs.to_numpy(dtype="float64"), axis=1)
    margin = pd.Series(sorted_probs[:, -1] - sorted_probs[:, -2], index=frame.index).clip(0.0, 1.0)
    precision_risk = (1.0 - normalize(margin, default=0.5)).clip(0.0, 1.0)
    return margin, precision_risk


def materialize_weights(frame: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series, pd.Series]:
    frame = frame.copy()
    label = pd.to_numeric(frame["label_class"], errors="coerce").fillna(1).astype(int)
    margin, precision_risk = precision_margin(frame)
    low_margin = numeric(frame, "low_margin_rate_model").clip(0.0, 1.0)
    underwater = numeric(frame, "underwater_rate_model").clip(0.0, 1.0)
    drawdown = numeric(frame, "drawdown_pressure_norm").clip(0.0, 1.0)
    direction_residual = numeric(frame, "direction_residual_rate_model").clip(0.0, 1.0)
    abstention = numeric(frame, "abstention_rate_model").clip(0.0, 1.0)
    side_gap = numeric(frame, "side_quality_gap_norm").clip(0.0, 1.0)
    cost_survival = numeric(frame, "cost_survival_weight", default=1.0).clip(0.10, 3.0)
    side_quality = numeric(frame, "side_quality_weight", default=1.0).clip(0.10, 3.0)
    curve_state = numeric(frame, "curve_state_pressure_weight", default=1.0).clip(0.10, 3.0)
    short_quality = numeric(frame, "short_quality_target", default=1.0).clip(0.0, 2.0)
    long_quality = numeric(frame, "long_quality_target", default=1.0).clip(0.0, 2.0)

    gz_precision = numeric(frame, "gz_precision_stable_net_recovery_weight", default=1.0).clip(0.10, 10.0)
    gz_cost = numeric(frame, "gz_cost_expectancy_repair_weight", default=1.0).clip(0.10, 10.0)
    gz_drawdown = numeric(frame, "gz_drawdown_recovery_repair_weight", default=1.0).clip(0.10, 10.0)
    gz_trade = numeric(frame, "gz_trade_shape_balance_repair_weight", default=1.0).clip(0.10, 10.0)
    gz_proxy = numeric(frame, "gz_proxy_negative_control_weight", default=1.0).clip(0.10, 10.0)
    gj_cost = numeric(frame, "gj_cost_session_regime_guard_weight", default=1.0).clip(0.10, 10.0)
    gj_dd = numeric(frame, "gj_drawdown_recovery_pressure_weight", default=1.0).clip(0.10, 10.0)
    gb_cost = numeric(frame, "gb_cost_session_regime_guard_weight", default=1.0).clip(0.10, 10.0)
    ft_cost = numeric(frame, "ft_cost_session_regime_guard_weight", default=1.0).clip(0.10, 10.0)
    ft_dd = numeric(frame, "ft_drawdown_recovery_pressure_weight", default=1.0).clip(0.10, 10.0)

    timestamps = pd.to_datetime(frame["timestamp"], utc=True, errors="coerce")
    hour = timestamps.dt.hour.fillna(0).astype(int)
    cash_overlap = pd.Series(np.where((hour >= 13) & (hour <= 21), 1.07, 0.96), index=frame.index)
    rollover_caution = pd.Series(np.where((hour <= 1) | (hour >= 22), 0.93, 1.01), index=frame.index)
    cost_adverse = (1.0 - normalize(cost_survival, default=0.55)).clip(0.0, 1.0)
    risk_pressure = (0.32 * drawdown + 0.24 * underwater + 0.24 * low_margin + 0.20 * precision_risk).clip(0.0, 1.0)
    churn_pressure = (0.30 * direction_residual + 0.28 * abstention + 0.24 * precision_risk + 0.18 * side_gap).clip(0.0, 1.0)
    activation_side = pd.Series(np.where(label == 1, 0.84 + 0.06 * (1.0 - churn_pressure), 1.13 - 0.12 * churn_pressure), index=frame.index).clip(0.72, 1.18)
    short_balance = pd.Series(np.where(label == 0, 1.08 + 0.10 * short_quality, 1.0), index=frame.index)
    long_balance = pd.Series(np.where(label == 2, 1.04 + 0.08 * long_quality - 0.08 * side_gap, 1.0), index=frame.index)
    flat_guard = pd.Series(np.where(label == 1, 0.95 + 0.04 * (1.0 - churn_pressure), 1.0), index=frame.index)
    side_balance = (short_balance * long_balance * flat_guard).clip(0.72, 1.40)
    positive_seed = (0.34 * gj_cost + 0.26 * gb_cost + 0.24 * ft_cost + 0.16 * gz_cost).clip(0.10, 10.0)
    proxy_negative_region = (normalize(gz_proxy, default=0.5) * (0.45 * cost_adverse + 0.30 * risk_pressure + 0.25 * precision_risk)).clip(0.0, 1.0)

    hh_activation = clip_weight(
        (0.26 * gz_cost + 0.24 * positive_seed + 0.20 * gz_trade + 0.18 * gz_precision + 0.12 * side_quality)
        * cash_overlap
        * rollover_caution
        * activation_side
        * (1.10 - 0.18 * cost_adverse).clip(0.78, 1.10)
        * (1.06 - 0.12 * churn_pressure).clip(0.84, 1.06)
    )
    hh_loss_tail = clip_weight(
        (0.30 * gz_drawdown + 0.22 * gj_dd + 0.18 * ft_dd + 0.16 * curve_state + 0.14 * gz_precision)
        * (1.13 - 0.30 * risk_pressure).clip(0.72, 1.13)
        * (1.08 - 0.18 * underwater).clip(0.76, 1.08)
        * side_balance
    )
    hh_precision = clip_weight(
        (0.32 * gz_precision + 0.22 * gz_proxy + 0.18 * gz_drawdown + 0.16 * gz_cost + 0.12 * side_quality)
        * (1.12 - 0.32 * precision_risk).clip(0.68, 1.12)
        * (1.08 - 0.18 * low_margin).clip(0.76, 1.08)
    )
    hh_proxy_negative = clip_weight(
        (0.30 * gz_proxy + 0.24 * gz_cost + 0.18 * gz_drawdown + 0.16 * positive_seed + 0.12 * gz_precision)
        * (1.02 - 0.26 * proxy_negative_region).clip(0.72, 1.02)
        * (1.04 - 0.12 * precision_risk).clip(0.82, 1.04)
    )
    hh_balanced = clip_weight(
        (0.25 * hh_activation + 0.22 * hh_loss_tail + 0.20 * hh_precision + 0.18 * hh_proxy_negative + 0.15 * positive_seed)
        * (1.06 - 0.14 * risk_pressure).clip(0.82, 1.06)
        * side_balance
    )

    frame["hh_activation_cost_session_regime_weight"] = hh_activation
    frame["hh_loss_tail_drawdown_recovery_weight"] = hh_loss_tail
    frame["hh_probability_precision_margin_weight"] = hh_precision
    frame["hh_proxy_mt5_negative_control_weight"] = hh_proxy_negative
    frame["hh_balanced_release_ladder_weight"] = hh_balanced
    frame["hh_probability_margin"] = margin
    frame["hh_precision_risk"] = precision_risk
    frame["hh_cost_adverse_risk"] = cost_adverse
    frame["hh_activation_pressure"] = (1.0 - activation_side).clip(0.0, 1.0)
    frame["hh_cost_session_regime_seed"] = positive_seed
    frame["hh_loss_tail_pressure"] = risk_pressure
    frame["hh_trade_churn_pressure"] = churn_pressure
    frame["hh_proxy_negative_pressure"] = proxy_negative_region
    return frame, margin, precision_risk


def source_map() -> list[dict[str, Any]]:
    sources = [
        ("hh_final", HH_FINAL, "parent decision(부모 결정)", "confirms HH design closeout(HH 설계 종료 확인)"),
        ("hh_task_blueprint", HH_TASK_BLUEPRINT, "task blueprint(작업 청사진)", "defines HI/HK training seeds(HI/HK 학습 씨앗 정의)"),
        ("hh_parity_plan", HH_PARITY_PLAN, "parity repair plan(동등성 수리 계획)", "keeps probability mismatch repair explicit(확률 불일치 수리 명시)"),
        ("hh_trade_plan", HH_TRADE_PLAN, "trade activation plan(거래 활성화 계획)", "keeps no-trade repair explicit(무거래 수리 명시)"),
        ("hh_positive_seed", HH_POSITIVE_SEED, "positive seed plan(긍정 씨앗 계획)", "preserves GA/GI positive clues(GA/GI 긍정 단서 보존)"),
        ("hg_kpi", HG_KPI, "MT5 KPI memory(MT5 핵심 성과 지표 기억)", "keeps negative MT5 KPI explicit(음수 MT5 지표 명시)"),
        ("hg_parity", HG_PARITY, "runtime parity memory(런타임 동등성 기억)", "keeps probability mismatch explicit(확률 불일치 명시)"),
        ("ha_base_frame", BASE_FRAME, "base train-only frame(기반 학습 전용 프레임)", "provides rows and prior GZ weights(행과 이전 GZ 가중치 제공)"),
        ("ha_allowed_features", BASE_FEATURES, "feature set(피처 묶음)", "keeps model inputs unchanged(모델 입력 유지)"),
    ]
    rows = []
    for source_id, path, source_type, effect in sources:
        rows.append(
            {
                "source_id": source_id,
                "source_path": rel(path),
                "source_type": source_type,
                "required": True,
                "exists": path_exists(path),
                "sha256": aw.sha256_file(path) if path_exists(path) and aw.io_path(path).is_file() else "",
                "effect": effect,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def weight_recipes() -> list[dict[str, Any]]:
    recipes = [
        (
            "hi001_activation_cost_session_regime",
            "hh_activation_cost_session_regime_weight",
            "gz_cost;gz_trade;gz_precision;gj/gb/ft cost seeds;session;activation_side",
            "clip(cost/session/regime seed blend * activation floor * cost/churn guards)",
            "avoid no-trade collapse while preserving positive cost-session-regime clue(무거래 붕괴를 막고 비용-세션-국면 긍정 단서 보존)",
        ),
        (
            "hi002_loss_tail_drawdown_recovery",
            "hh_loss_tail_drawdown_recovery_weight",
            "gz_drawdown;gj_dd;ft_dd;curve_state;risk_pressure;side_balance",
            "clip(drawdown/recovery blend * loss-tail pressure guard)",
            "reduce drawdown and recovery weakness(낙폭과 회복 취약성 축소)",
        ),
        (
            "hi003_probability_precision_margin",
            "hh_probability_precision_margin_weight",
            "gz_precision;gz_proxy;gz_drawdown;low_margin;precision_risk",
            "clip(precision blend * low-margin penalty)",
            "reduce probability mismatch risk(확률 불일치 위험 축소)",
        ),
        (
            "hi004_proxy_mt5_negative_control",
            "hh_proxy_mt5_negative_control_weight",
            "gz_proxy;gz_cost;gz_drawdown;positive_seed;proxy_negative_region",
            "clip(proxy blend * MT5-negative suppression)",
            "keep proxy as negative control, not authority(프록시를 권위가 아닌 음수 대조로 유지)",
        ),
        (
            "hi005_balanced_release_ladder",
            "hh_balanced_release_ladder_weight",
            "hh_activation;hh_loss_tail;hh_precision;hh_proxy_negative;positive_seed",
            "clip(multi-objective blend * risk guard * side balance)",
            "bind net, PF, recovery, parity, and trade activation together(순수익/PF/회복/동등성/거래 활성화를 묶음)",
        ),
    ]
    return [
        {
            "recipe_id": recipe_id,
            "materialized_column": column,
            "source_columns": sources,
            "train_only_formula": formula,
            "lower_bound": "0.10",
            "upper_bound": "10.0",
            "expected_effect": effect,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for recipe_id, column, sources, formula, effect in recipes
    ]


def allowed_feature_rows(base_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for row in base_rows:
        new_row = dict(row)
        new_row["source_layer"] = rel(TRAIN_ONLY_REPAIR_FRAME)
        new_row["claim_boundary"] = CLAIM_BOUNDARY
        rows.append(new_row)
    return rows


def weight_audit(frame: pd.DataFrame) -> list[dict[str, Any]]:
    label = pd.to_numeric(frame["label_class"], errors="coerce").fillna(1).astype(int)
    rows = []
    for column in NEW_WEIGHT_COLUMNS:
        values = pd.to_numeric(frame[column], errors="coerce").replace([np.inf, -np.inf], np.nan)
        rows.append(
            {
                "weight_column": column,
                "rows": int(len(values)),
                "weight_min": float(values.min()),
                "weight_mean": float(values.mean()),
                "weight_max": float(values.max()),
                "nonfinite_rows": int(values.isna().sum()),
                "short_label_mean": float(values[label == 0].mean()),
                "flat_label_mean": float(values[label == 1].mean()),
                "long_label_mean": float(values[label == 2].mean()),
                "effect": "checks bounded train-only HH weights(범위 제한 학습 전용 HH 가중치 점검)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def target_contract_audit(task_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    bad_targets = [row.get("task_id", "") for row in task_rows if row.get("target_column") != "label_class"]
    bad_weights = [row.get("sample_weight_column", "") for row in task_rows if row.get("sample_weight_column") not in NEW_WEIGHT_COLUMNS]
    return [
        {
            "audit_id": "hi_target001_label_class_only",
            "status": "passed" if not bad_targets else "failed",
            "observed": ";".join(bad_targets),
            "expected": "all target_column == label_class(모든 목표 열 label_class)",
            "evidence": rel(TRAINING_TASK_SEEDS),
            "effect": "prevents sample-weight-as-target regression(표본 가중치 목표화 방지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "audit_id": "hi_target002_weight_columns_present",
            "status": "passed" if not bad_weights else "failed",
            "observed": ";".join(bad_weights),
            "expected": ";".join(NEW_WEIGHT_COLUMNS),
            "evidence": rel(TRAIN_ONLY_REPAIR_FRAME),
            "effect": "connects each training seed to materialized HH weight(각 학습 씨앗을 물질화된 HH 가중치와 연결)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def parity_precision_audit(frame: pd.DataFrame, margin: pd.Series, precision_risk: pd.Series) -> list[dict[str, Any]]:
    parent = read_json(HH_FINAL)
    near_boundary_rows = int((margin <= 0.005).sum())
    high_precision_risk_rows = int((precision_risk >= 0.80).sum())
    return [
        {
            "audit_id": "hi_parity001_parent_mismatch_named",
            "status": "passed" if as_int(parent.get("probability_mismatch_rows")) == 11 and as_int(parent.get("decision_mismatch_rows")) == 0 and as_int(parent.get("hash_mismatch_rows")) == 0 else "failed",
            "observed": f"probability={parent.get('probability_mismatch_rows')};decision={parent.get('decision_mismatch_rows')};hash={parent.get('hash_mismatch_rows')}",
            "expected": "probability=11;decision=0;hash=0",
            "evidence": rel(HH_FINAL),
            "effect": "carries probability mismatch memory into inputs(확률 불일치 기억을 입력으로 인계)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "audit_id": "hi_parity002_precision_fields_materialized",
            "status": "passed" if "hh_probability_margin" in frame.columns and "hh_precision_risk" in frame.columns else "failed",
            "observed": f"near_boundary_rows={near_boundary_rows};high_precision_risk_rows={high_precision_risk_rows}",
            "expected": "precision fields present(정밀도 필드 존재)",
            "evidence": rel(TRAIN_ONLY_REPAIR_FRAME),
            "effect": "makes future parity review measurable(향후 동등성 검토를 측정 가능하게 함)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def feature_boundary_rows(allowed_features: Sequence[str], frame: pd.DataFrame, summary: Mapping[str, Any]) -> list[dict[str, Any]]:
    forbidden = [
        feature
        for feature in allowed_features
        if any(token in feature.lower() for token in FORBIDDEN_FEATURE_TOKENS)
        or feature.endswith("_weight")
        or feature.startswith("fd_")
        or feature.startswith("fl_")
        or feature.startswith("ft_")
        or feature.startswith("gb_")
        or feature.startswith("gj_")
        or feature.startswith("gr_")
        or feature.startswith("gz_")
        or feature.startswith("hh_")
    ]
    duplicate_ts = int(pd.to_datetime(frame["timestamp"], utc=True, errors="coerce").duplicated().sum())
    return [
        {
            "audit_id": "hi_feature001_allowed_feature_count",
            "status": "passed" if len(allowed_features) == 58 else "failed",
            "observed": str(len(allowed_features)),
            "expected": "58",
            "evidence": rel(ALLOWED_FEATURE_SET),
            "effect": "keeps reviewed model feature order(검토된 모델 피처 순서 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "audit_id": "hi_feature002_forbidden_features_excluded",
            "status": "passed" if not forbidden else "failed",
            "observed": ";".join(forbidden),
            "expected": "no label/future/weight/outcome/MT5 KPI features(라벨/미래/가중치/결과/MT5 지표 피처 없음)",
            "evidence": rel(ALLOWED_FEATURE_SET),
            "effect": "prevents target leakage into model features(목표 누수 방지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "audit_id": "hi_feature003_nonfinite_weights",
            "status": "passed" if summary["nonfinite_weight_rows"] == 0 else "failed",
            "observed": str(summary["nonfinite_weight_rows"]),
            "expected": "0",
            "evidence": rel(WEIGHT_AUDIT),
            "effect": "repair weights are finite(수리 가중치 유한)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "audit_id": "hi_feature004_timestamp_order",
            "status": "passed" if frame["timestamp"].is_monotonic_increasing else "failed",
            "observed": str(frame["timestamp"].is_monotonic_increasing),
            "expected": "True",
            "evidence": rel(TRAIN_ONLY_REPAIR_FRAME),
            "effect": "keeps time axis ordered(시간축 순서 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "audit_id": "hi_feature005_timestamp_duplicates_named",
            "status": "passed",
            "observed": str(duplicate_ts),
            "expected": "duplicates allowed by cost_policy_id training expansion(비용 정책 학습 확장 중복 허용)",
            "evidence": rel(TRAIN_ONLY_REPAIR_FRAME),
            "effect": "names expanded train-only repeated timestamps(확장 학습 전용 반복 시각 명명)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "audit_id": "hi_feature006_macro_join_safe_by_absence",
            "status": "passed",
            "observed": "no new macro source joined in HI(HI에서 새 거시 자료 결합 없음)",
            "expected": "economic data requires release timestamp(경제자료는 발표 시각 필요)",
            "evidence": rel(HH_FEATURE_LABEL),
            "effect": "prevents macro look-ahead(거시 미래참조 방지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def materialize_task_seeds() -> list[dict[str, Any]]:
    rows = [dict(row) for row in read_csv(HH_TASK_BLUEPRINT)]
    for row in rows:
        task_id = row.get("task_id", "")
        if task_id in TASK_WEIGHT_COLUMNS:
            row["target_column"] = "label_class"
            row["sample_weight_expression"] = TASK_WEIGHT_COLUMNS[task_id]
            row["sample_weight_column"] = TASK_WEIGHT_COLUMNS[task_id]
            row["selection_status"] = "eligible_after_HJ_review(HJ 검토 후 적격)"
            row["claim_boundary"] = CLAIM_BOUNDARY
    return rows


def review_queue() -> list[dict[str, Any]]:
    return [
        {
            "queue_id": "hj_review_post_runtime_probe_repair_inputs",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "task": "review HI train-only frame, HH weights, target contract, feature boundary, and HK training eligibility(HI 학습 전용 프레임, HH 가중치, 목표 계약, 피처 경계, HK 학습 적격성 검토)",
            "required_inputs": f"{rel(TRAIN_ONLY_REPAIR_FRAME)};{rel(WEIGHT_AUDIT)};{rel(TARGET_CONTRACT_AUDIT)};{rel(PARITY_PRECISION_AUDIT)};{rel(TRAINING_TASK_SEEDS)}",
            "required_outputs": "input review, eligible HK training queue, target contract disposition(입력 검토, 적격 HK 학습 대기열, 목표 계약 처분)",
            "blocked_if_missing": "HI frame or audits(HI 프레임 또는 감사)",
            "forbidden_action": "train, tune threshold, execute MT5, or select operating candidate(학습/임계값 조정/MT5 실행/운영 후보 선택)",
            "effect": "forces review before training(학습 전 검토 강제)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def build_summary(frame: pd.DataFrame, allowed_features: Sequence[str], weight_rows: Sequence[Mapping[str, Any]], task_rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    hh_final = read_json(HH_FINAL)
    weight_nonfinite = sum(int(row.get("nonfinite_rows", 0)) for row in weight_rows)
    label_counts = pd.to_numeric(frame["label_class"], errors="coerce").fillna(1).astype(int).value_counts().sort_index()
    return {
        "rows": int(len(frame)),
        "feature_count": int(len(allowed_features)),
        "new_weight_count": len(NEW_WEIGHT_COLUMNS),
        "nonfinite_weight_rows": weight_nonfinite,
        "task_seed_rows": len(task_rows),
        "task_target_label_class_rows": sum(1 for row in task_rows if row.get("target_column") == "label_class"),
        "label_distribution": {str(int(k)): int(v) for k, v in label_counts.items()},
        "first_timestamp": str(frame["timestamp"].iloc[0]) if len(frame) else "",
        "last_timestamp": str(frame["timestamp"].iloc[-1]) if len(frame) else "",
        "hh_best_attempt": hh_final.get("hg_best_attempt", ""),
        "hh_best_net_profit": hh_final.get("best_net_profit", ""),
        "hh_probability_mismatch_rows": hh_final.get("probability_mismatch_rows", ""),
        "hh_ga_seed_net": hh_final.get("ga_seed_net", ""),
        "hh_gi_seed_net": hh_final.get("gi_seed_net", ""),
        "hh_target_label_class_rows": hh_final.get("task_target_label_class_rows", ""),
        "hh_task_rows": hh_final.get("task_rows", ""),
        "positive_seed_rows": hh_final.get("positive_seed_rows", ""),
    }


def build_gates(final: Mapping[str, Any]) -> list[dict[str, Any]]:
    no_forbidden_claim = (
        final["new_training"] == "not_run"
        and final["candidate_selection"] == "not_run"
        and final["mt5_execution"] == "not_run"
        and final["goal_achieve"] == "not_claimed"
    )
    checks = [
        ("input_presence", final["missing_inputs"] == 0, str(final["missing_inputs"]), "0", rel(BASE_FRAME), "required HH/HA inputs exist(필수 HH/HA 입력 존재)"),
        ("parent_hh_gates_passed", final["hh_failed_gate_rows"] == 0, str(final["hh_failed_gate_rows"]), "0", rel(HH_GATES), "HH gates passed(HH 게이트 통과)"),
        ("parent_next_action_matches", final["hh_next_action"] == RUN_ID, str(final["hh_next_action"]), RUN_ID, rel(HH_FINAL), "HI follows HH next action(HI가 HH 다음 행동을 따름)"),
        ("repair_frame_materialized", final["rows"] == 87666 and path_exists(TRAIN_ONLY_REPAIR_FRAME), f"rows={final['rows']}", "87666", rel(TRAIN_ONLY_REPAIR_FRAME), "train-only repair frame exists(학습 전용 수리 프레임 존재)"),
        ("allowed_feature_set_preserved", final["feature_count"] == 58, str(final["feature_count"]), "58", rel(ALLOWED_FEATURE_SET), "reviewed feature set preserved(검토 피처 묶음 유지)"),
        ("target_contract_preserved", final["task_seed_rows"] == final["task_target_label_class_rows"] == 5, f"tasks={final['task_seed_rows']};label_class={final['task_target_label_class_rows']}", "5/5 label_class", rel(TARGET_CONTRACT_AUDIT), "target contract preserved(목표 계약 유지)"),
        ("feature_boundary_passed", final["feature_boundary_failed_rows"] == 0, str(final["feature_boundary_failed_rows"]), "0", rel(FEATURE_LABEL_BOUNDARY), "feature boundary audit passed(피처 경계 감사 통과)"),
        ("new_weights_materialized", final["new_weight_count"] == len(NEW_WEIGHT_COLUMNS), str(final["new_weight_count"]), str(len(NEW_WEIGHT_COLUMNS)), rel(WEIGHT_AUDIT), "HH repair weights materialized(HH 수리 가중치 물질화)"),
        ("nonfinite_weights_zero", final["nonfinite_weight_rows"] == 0, str(final["nonfinite_weight_rows"]), "0", rel(WEIGHT_AUDIT), "weights finite(가중치 유한)"),
        ("parity_precision_audit_complete", final["parity_precision_failed_rows"] == 0 and as_int(final["hh_probability_mismatch_rows"]) == 11, f"failed={final['parity_precision_failed_rows']};parent_prob={final['hh_probability_mismatch_rows']}", "0 failed and parent_prob=11", rel(PARITY_PRECISION_AUDIT), "probability mismatch memory carried(확률 불일치 기억 인계)"),
        ("positive_seed_carried", as_int(final["positive_seed_rows"]) >= 2 and as_float(final["hh_ga_seed_net"]) > 0 and as_float(final["hh_gi_seed_net"]) > 0, f"seeds={final['positive_seed_rows']};ga={final['hh_ga_seed_net']};gi={final['hh_gi_seed_net']}", ">=2 positive seeds", rel(POSITIVE_SEED_MATERIALIZATION), "positive clue carried(긍정 단서 인계)"),
        ("review_queue_materialized", final["review_queue_rows"] == 1 and final["next_action"] == NEXT_RUN_ID, f"queue={final['review_queue_rows']};next={final['next_action']}", f"1 and {NEXT_RUN_ID}", rel(HJ_QUEUE), "HJ review queue opened(HJ 검토 대기열 열림)"),
        ("no_forbidden_claim", no_forbidden_claim, f"training={final['new_training']};selection={final['candidate_selection']};mt5={final['mt5_execution']};goal={final['goal_achieve']}", "not_run/not_run/not_run/not_claimed", rel(FINAL_DECISION), "materialization without operating claim(운영 주장 없는 물질화)"),
        ("required_gate_coverage_audit", True, "all required gates listed in closeout(모든 필수 게이트가 종료 기록에 있음)", "present", rel(GATE_AUDIT), "connects gates to completion claim(게이트를 완료 주장과 연결)"),
    ]
    return [
        {"gate_id": gate_id, "status": "passed" if passed else "failed", "evidence_path": evidence, "observed": observed, "expected": expected, "effect": effect, "claim_boundary": CLAIM_BOUNDARY}
        for gate_id, passed, observed, expected, evidence, effect in checks
    ]


def make_final(summary: Mapping[str, Any], boundary_failed: int, parity_failed: int) -> dict[str, Any]:
    hh_final = read_json(HH_FINAL)
    return {
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "stage_id": STAGE_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_action": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
        "primary_family": "experiment_execution",
        "primary_skill": "obsidian-run-evidence-system",
        "support_skills": "obsidian-data-integrity;obsidian-model-validation;obsidian-artifact-lineage;obsidian-claim-discipline",
        "new_training": "not_run",
        "mt5_execution": "not_run",
        "threshold_tuning": "not_run",
        "lot_optimization": "not_run",
        "candidate_selection": "not_run",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "runtime_authority": "not_claimed",
        "goal_achieve": "not_claimed",
        "missing_inputs": len(fail_if_missing(INPUT_FILES)),
        "hh_next_action": hh_final.get("next_action", ""),
        "hh_failed_gate_rows": sum(1 for row in read_csv(HH_GATES) if row.get("status") != "passed"),
        "feature_boundary_failed_rows": boundary_failed,
        "parity_precision_failed_rows": parity_failed,
        "measurement_scope": "input_materialization_no_kpi(no new KPI, 입력 물질화 새 KPI 없음)",
        "management_state": "run folder, manifest, receipts, registries updated(실행 폴더/목록/영수증/등록부 갱신)",
        "judgment_class": "exploratory_materialization(탐색 물질화)",
        "scoreboard": "structural_scout(구조 탐색)",
        "parity_level": "P2_model_input_parity_closed_by_input_schema_only(P2 모델 입력 스키마 한정)",
        "wfo_status": "not_applicable(해당 없음)",
        "registry_update_required": "yes",
        "negative_memory_required": "yes",
        "hard_gate_applicable": "no",
        "evidence_boundary": "scout-only(정찰 전용)",
        **dict(summary),
    }


def build_receipts(final: Mapping[str, Any], artifacts: Sequence[Path]) -> list[Path]:
    created_at = now_utc()
    base = {
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "stage_id": STAGE_ID,
        "created_at_utc": created_at,
        "status": final["status"],
        "claim_boundary": CLAIM_BOUNDARY,
    }
    receipts: list[tuple[Path, Mapping[str, Any]]] = [
        (
            DATA_RECEIPT,
            {
                **base,
                "receipt_type": "data_integrity(데이터 무결성)",
                "data_source": rel(BASE_FRAME),
                "time_axis": f"timestamp ordered; duplicates from cost_policy_id expansion(시각 순서, 비용 정책 확장 중복); {final['first_timestamp']} to {final['last_timestamp']}",
                "sample_scope": f"US100 M5 train-only rows={final['rows']}; Tier A inner holdout expansion(Tier A 내부 보류 확장)",
                "missing_or_duplicate_check": "duplicates named and allowed only by training expansion(중복은 학습 확장으로만 허용)",
                "feature_label_boundary": "allowed feature set preserved; HH weights excluded from model features(허용 피처 보존, HH 가중치는 모델 피처 제외)",
                "split_boundary": "train-only materialization, no MT5 execution(학습 전용 물질화, MT5 실행 없음)",
                "leakage_risk": "sample weights must not become hidden target(표본 가중치 숨은 목표화 금지)",
                "data_hash_or_identity": aw.sha256_file(TRAIN_ONLY_REPAIR_FRAME) if path_exists(TRAIN_ONLY_REPAIR_FRAME) else "",
                "integrity_judgment": "usable_with_boundary(경계 있는 사용 가능)",
            },
        ),
        (
            MODEL_RECEIPT,
            {
                **base,
                "receipt_type": "model_validation(모델 검증)",
                "model_family": "future LightGBM multiclass to ONNX(향후 라이트GBM 다중분류에서 온엑스)",
                "target_and_label": f"label_class {final['task_target_label_class_rows']}/{final['task_seed_rows']}",
                "split_method": "existing train/inner holdout boundary inherited(기존 학습/내부 보류 경계 상속)",
                "selection_metric": "not selected in HI(HI에서 선택 없음)",
                "secondary_metrics": "future net, PF, expectancy, DD, recovery, trade balance, parity(향후 순수익/PF/기대값/낙폭/회복/거래 균형/동등성)",
                "threshold_policy": "fixed argmax, no threshold tuning(고정 argmax, 임계값 조정 없음)",
                "overfit_risk": "positive seed reuse can overfit unless future MT5 agrees(긍정 씨앗 재사용은 향후 MT5 동의 없으면 과적합 위험)",
                "calibration_risk": "probabilities are runtime precision evidence, not authority(확률은 런타임 정밀도 근거이지 권위 아님)",
                "comparison_baseline": "HG all-negative MT5 probe(HG 전부 음수 MT5 탐침)",
                "validation_judgment": "exploratory(탐색)",
            },
        ),
        (
            RUNTIME_RECEIPT,
            {
                **base,
                "receipt_type": "runtime_parity(런타임 동등성)",
                "known_differences": f"parent_probability_mismatch_rows={final['hh_probability_mismatch_rows']}",
                "parity_level": final["parity_level"],
                "future_requirement": "future runtime probe must reach probability_mismatch=0(향후 런타임 탐침 확률 불일치 0 필요)",
                "evidence": [rel(PARITY_PRECISION_AUDIT), rel(HG_PARITY)],
            },
        ),
        (
            RUN_EVIDENCE_RECEIPT,
            {
                **base,
                "receipt_type": "run_evidence_system(실행 근거 시스템)",
                "measurement_scope": final["measurement_scope"],
                "management_state": final["management_state"],
                "judgment_class": final["judgment_class"],
                "scoreboard": final["scoreboard"],
                "parity_level": final["parity_level"],
                "wfo_status": final["wfo_status"],
                "registry_update_required": final["registry_update_required"],
                "negative_memory_required": final["negative_memory_required"],
                "hard_gate_applicable": final["hard_gate_applicable"],
                "evidence_boundary": final["evidence_boundary"],
            },
        ),
        (
            PERFORMANCE_RECEIPT,
            {
                **base,
                "receipt_type": "performance_attribution(성과 귀속)",
                "negative_memory": f"HG best_net={final['hh_best_net_profit']};prob_mismatch={final['hh_probability_mismatch_rows']}",
                "positive_seed": f"GA={final['hh_ga_seed_net']};GI={final['hh_gi_seed_net']}",
                "materialized_weights": list(NEW_WEIGHT_COLUMNS),
                "evidence": [rel(WEIGHT_AUDIT), rel(POSITIVE_SEED_MATERIALIZATION), rel(NEGATIVE_CONTROL_MATERIALIZATION)],
            },
        ),
        (
            JUDGMENT_RECEIPT,
            {
                **base,
                "receipt_type": "result_judgment(결과 판정)",
                "result_subject": RUN_ID,
                "evidence_available": [rel(TRAIN_ONLY_REPAIR_FRAME), rel(WEIGHT_AUDIT), rel(TARGET_CONTRACT_AUDIT)],
                "evidence_missing": "new training, ONNX export, MT5 runtime probe, forward/replay authority(새 학습, ONNX 내보내기, MT5 런타임 탐침, 전진/재생 권위)",
                "judgment_label": "exploratory_materialization(탐색 물질화)",
                "next_condition": NEXT_RUN_ID,
            },
        ),
        (
            CLAIM_RECEIPT,
            {
                **base,
                "receipt_type": "claim_discipline(주장 규율)",
                "forbidden_claims": "selected, operating_promotion, runtime_authority, Goal Achieve(선택, 운영 승격, 런타임 권위, 목표 달성)",
                "claim_guard": "all forbidden claims remain not_claimed/not_run(모든 금지 주장은 not_claimed/not_run)",
            },
        ),
        (
            LINEAGE_RECEIPT,
            {
                **base,
                "receipt_type": "artifact_lineage(산출물 계보)",
                "source_inputs": [rel(path) for path in INPUT_FILES],
                "producer": rel(Path(__file__)),
                "consumer": NEXT_RUN_ID,
                "artifact_paths": [rel(path) for path in artifacts],
                "artifact_hashes": {rel(path): aw.sha256_file(path) for path in artifacts if path_exists(path) and aw.io_path(path).is_file()},
                "registry_links": [rel(he.RUN_REGISTRY), rel(he.ALPHA_LEDGER), rel(he.STAGE_LEDGER), rel(he.ARTIFACT_REGISTRY)],
                "availability": "generated_with_manifest(목록과 함께 생성)",
                "lineage_judgment": "connected_with_boundary(경계 있는 연결)",
            },
        ),
    ]
    return [write_json(path, payload) for path, payload in receipts]


def write_report(final: Mapping[str, Any]) -> Path:
    text = f"""# run337HI Post Runtime Probe Repair Inputs(run337HI 사후 런타임 탐침 수리 입력)

Action(행동): HA train-only frame(HA 학습 전용 프레임)에 HH activation/cost/session/regime/parity weights(HH 활성화/비용/세션/국면/동등성 가중치)를 물질화했다. Effect(효과): `{final['rows']}` rows(행), `{final['feature_count']}` model features(모델 피처), `{final['new_weight_count']}` new weights(새 가중치)를 HJ review(HJ 검토)로 넘겼다.

## Judgment(판정)

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- claim_boundary(주장 경계): `{final['claim_boundary']}`

## Data Integrity(데이터 무결성)

- data_source(데이터 원천): `{rel(BASE_FRAME)}`
- time_axis(시간축): `{final['first_timestamp']}` to `{final['last_timestamp']}`
- feature_count(피처 수): `{final['feature_count']}`
- nonfinite_weight_rows(비유한 가중치 행): `{final['nonfinite_weight_rows']}`
- feature_boundary_failed(피처 경계 실패): `{final['feature_boundary_failed_rows']}`

## Model Validation(모델 검증)

- target_contract(목표 계약): `label_class {final['task_target_label_class_rows']}/{final['task_seed_rows']}`
- threshold_policy(임계값 정책): fixed argmax(고정 argmax), no tuning(조정 없음)
- validation_judgment(검증 판정): exploratory materialization(탐색 물질화)

## Runtime Boundary(런타임 경계)

- parent_probability_mismatch(부모 확률 불일치): `{final['hh_probability_mismatch_rows']}`
- parity_precision_failed(동등성 정밀도 실패): `{final['parity_precision_failed_rows']}`
- parity_level(동등성 단계): `{final['parity_level']}`

## Gate Result(게이트 결과)

- gates(게이트): `{final['passed_gates']}/{final['gate_rows']}`
- failed_gates(실패 게이트): `{','.join(final['failed_gates']) if final['failed_gates'] else 'none'}`

Action(행동): 이 run(실행)은 training(학습), MT5 execution(MT5 실행), candidate selection(후보 선택)을 하지 않았다. Effect(효과): 운영 가능 모델 주장을 만들지 않고 HJ review(HJ 검토) 조건만 닫았다.
"""
    return aw.write_text_lossless(REPORT_PATH, text, True)


def write_decision(final: Mapping[str, Any]) -> Path:
    text = f"""# Decision(결정): Stage337 run337HI

- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- judgment(판정): `{final['judgment']}`
- effect(효과): HH design(HH 설계)을 train-only materialized evidence(학습 전용 물질화 근거)로 바꾸고 HJ review(HJ 검토)를 연다.
- forbidden_claim(금지 주장): Forward Passed(전진 통과), runtime authority(런타임 권위), operating promotion(운영 승격), Goal Achieve(목표 달성).
"""
    return aw.write_text_lossless(DECISION_DOC, text, True)


def update_docs(final: Mapping[str, Any]) -> list[Path]:
    artifacts: list[Path] = []
    workspace, workspace_bom = aw.read_text_lossless(he.WORKSPACE_STATE)
    workspace = re.sub(r"^current_run_id:.*$", f"current_run_id: {final['next_action']}", workspace, count=1, flags=re.M)
    workspace = re.sub(r"^updated_on:.*$", f"updated_on: '{TODAY}'", workspace, count=1, flags=re.M)
    focus = (
        "- >-\n"
        f"  Stage337 run337HI focus complete(337단계 337HI 초점 완료): post-runtime repair inputs(사후 런타임 수리 입력)을 `{final['status']}`로 물질화했다. "
        f"Effect(효과): rows(행) `{final['rows']}`, new weights(새 가중치) `{final['new_weight_count']}`, target contract(목표 계약) `{final['task_target_label_class_rows']}/{final['task_seed_rows']}`를 만들고 `{final['next_action']}`을 열었다. Forward/Goal(전진/목표)은 주장하지 않는다.\n"
    )
    if "Stage337 run337HI focus complete" in workspace:
        workspace = re.sub(r"- >-\n  Stage337 run337HI focus complete.*?(?=\n- >-|\n[a-zA-Z_]+:|$)", focus.rstrip(), workspace, count=1, flags=re.S)
    else:
        workspace = workspace.replace("current_focus:\n", "current_focus:\n" + focus, 1)
    artifacts.append(aw.write_text_lossless(he.WORKSPACE_STATE, workspace, workspace_bom))

    current, current_bom = aw.read_text_lossless(he.CURRENT_STATE)
    for field_name, value in {
        "current_run": f"`{final['next_action']}`",
        "status": f"`{final['status']}`",
        "decision": f"`{final['decision']}`",
        "latest_completed_run": f"`{RUN_ID}`",
        "next_action": f"`{final['next_action']}`",
        "claim_boundary": f"`{CLAIM_BOUNDARY}`",
    }.items():
        current = fb.replace_bullet_field(current, field_name, value)
    section = f"""## run337HI Post Runtime Probe Repair Inputs

Action(행동): run337HI(337HI 실행)은 HH design(HH 설계)을 train-only input frame(학습 전용 입력 프레임)과 HH sample weights(HH 표본 가중치)로 물질화했다.
Effect(효과): rows(행) `{final['rows']}`, features(피처) `{final['feature_count']}`, weights(가중치) `{final['new_weight_count']}`, target contract(목표 계약) `label_class {final['task_target_label_class_rows']}/{final['task_seed_rows']}`를 만들었다.

Boundary(경계): training(학습), MT5 execution(MT5 실행), candidate selection(후보 선택), Forward/Goal(전진/목표)은 주장하지 않는다.
Next(다음): `{final['next_action']}`.
"""
    current = fb.upsert_section_before(current, "## run337HH Post Runtime Probe Repair Design", section, "run337HI Post Runtime Probe Repair Inputs")
    artifacts.append(aw.write_text_lossless(he.CURRENT_STATE, current, current_bom))

    selection = f"""# Stage337 Selection Status(337단계 선택 상태)

- latest_run(최신 실행): `{RUN_ID}`
- latest_decision(최신 결정): `{final['decision']}`
- current_run(현재 실행): `{final['next_action']}`
- rebuild_status(재구축 상태): `{final['status']}`
- rows(행): `{final['rows']}`
- feature_count(피처 수): `{final['feature_count']}`
- new_weight_count(새 가중치 수): `{final['new_weight_count']}`
- target_contract(목표 계약): `label_class {final['task_target_label_class_rows']}/{final['task_seed_rows']}`
- probability_mismatch(확률 불일치): `{final['hh_probability_mismatch_rows']}`
- positive_seed_net(긍정 씨앗 순수익): `GA {final['hh_ga_seed_net']} / GI {final['hh_gi_seed_net']}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{final['next_action']}`
- effect(효과): HI materialization(물질화)은 HJ review(HJ 검토) 가능한 training-ready evidence(학습 준비 근거)만 만들고 운영 선택은 하지 않는다.
"""
    artifacts.append(aw.write_text_lossless(he.SELECTED_STATUS, selection, True))

    brief, brief_bom = aw.read_text_lossless(he.STAGE_BRIEF)
    brief_entry = (
        f"- {TODAY}: run337HI(337HI 실행) `{final['status']}`. "
        f"Effect(효과): rows `{final['rows']}`, new weights `{final['new_weight_count']}`, target contract `label_class {final['task_target_label_class_rows']}/{final['task_seed_rows']}`를 만들고 `{final['next_action']}`을 열었다. Forward/Goal(전진/목표)은 주장하지 않는다."
    )
    artifacts.append(aw.write_text_lossless(he.STAGE_BRIEF, fb.upsert_single_line(brief, "run337HI(337HI 실행)", brief_entry), brief_bom))

    changelog, changelog_bom = aw.read_text_lossless(he.CHANGELOG)
    changelog_entry = (
        f"- {TODAY}: Stage337 run337HI(337HI 실행) `{final['status']}`. "
        f"Effect(효과): post-runtime repair train-only inputs(사후 런타임 수리 학습 전용 입력)을 물질화하고 `{final['next_action']}`을 열었다."
    )
    artifacts.append(aw.write_text_lossless(he.CHANGELOG, fb.upsert_single_line(changelog, "Stage337 run337HI", changelog_entry), changelog_bom))
    return artifacts


def update_registers(final: Mapping[str, Any]) -> list[Path]:
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "post_runtime_probe_repair_input_materialization",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "notes": f"rows={final['rows']};features={final['feature_count']};weights={final['new_weight_count']};target_label_class={final['task_target_label_class_rows']}/{final['task_seed_rows']};next_action={final['next_action']};goal_achieve_not_claimed.",
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__input_materialization",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "input_materialization",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "post_runtime_probe_repair_input_materialization(사후 런타임 탐침 수리 입력 물질화)",
        "tier_scope": "Tier A train-only materialization(Tier A 학습 전용 물질화)",
        "kpi_scope": "input_materialization_no_training_no_mt5(입력 물질화, 학습/MT5 없음)",
        "scoreboard_lane": "experiment_execution",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "primary_kpi": f"rows={final['rows']};features={final['feature_count']};weights={final['new_weight_count']}",
        "guardrail_kpi": "target_contract_guarded;no_selection;no_forward;no_goal",
        "external_verification_status": "out_of_scope_by_claim",
        "notes": f"decision={final['decision']};next_action={final['next_action']};goal_achieve_not_claimed.",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__input_materialization",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "experiment_execution_data_integrity_model_validation",
        "evidence_scope": "HH design plus HA train-only base frame",
        "kpi_scope": "input_materialization_no_operating_claim",
        "status": final["status"],
        "judgment": final["judgment"],
        "claim_boundary": CLAIM_BOUNDARY,
        "path": rel(REPORT_PATH),
        "notes": f"gates={final['passed_gates']}/{final['gate_rows']};next_action={final['next_action']};goal_achieve_not_claimed",
        "decision": final["decision"],
        "run_key": f"{RUN_ID}__input_materialization",
        "family": "post_runtime_probe_repair_input_materialization",
        "question": "can HH post-runtime repair design become safe train-only inputs(HH 사후 런타임 수리 설계가 시점 안전 학습 전용 입력이 될 수 있는가)",
        "metric_scope": "rows_features_weights_target_contract",
        "primary_artifact": rel(TRAIN_ONLY_REPAIR_FRAME),
        "report_path": rel(REPORT_PATH),
        "next_action": final["next_action"],
    }
    return [
        fb.upsert_csv_worktree(he.RUN_REGISTRY, aw.RUN_REGISTRY_COLUMNS, run_row, "run_id"),
        fb.upsert_csv_worktree(he.ALPHA_LEDGER, aw.ALPHA_LEDGER_COLUMNS, alpha_row, "ledger_row_id"),
        fb.upsert_csv_worktree(he.STAGE_LEDGER, aw.STAGE_LEDGER_COLUMNS, stage_row, "ledger_row_id"),
    ]


def update_artifact_registry(paths: Sequence[Path]) -> Path:
    columns, rows = aw.read_csv_table(he.ARTIFACT_REGISTRY, prefer_head=False)
    columns = list(columns or aw.ARTIFACT_COLUMNS)
    for column in aw.ARTIFACT_COLUMNS:
        if column not in columns:
            columns.append(column)
    for extra in ("artifact_path", "claim_boundary"):
        if extra not in columns:
            columns.append(extra)
    rows = [row for row in rows if not str(row.get("artifact_id", "")).startswith(f"{RUN_ID}::") and str(row.get("run_id", "")) != RUN_ID]
    created_at = now_utc()
    seen: set[str] = set()
    for path in paths:
        if not path_exists(path) or not aw.io_path(path).is_file():
            continue
        artifact_path = rel(path)
        artifact_id = f"{RUN_ID}::{artifact_path}"
        if artifact_id in seen:
            continue
        seen.add(artifact_id)
        row = {
            "artifact_id": artifact_id,
            "artifact_type": path.suffix.lstrip(".") or "file",
            "path": artifact_path,
            "sha256": aw.sha256_file(path),
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": created_at,
            "notes": STATUS,
            "artifact_path": artifact_path,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        rows.append({column: row.get(column, "") for column in columns})
    return write_csv(he.ARTIFACT_REGISTRY, columns, rows)


def main() -> int:
    aw.io_path(RUN_DIR).mkdir(parents=True, exist_ok=True)
    missing = fail_if_missing(INPUT_FILES)
    if missing:
        print(json.dumps({"run_id": RUN_ID, "status": "blocked_missing_inputs", "missing": [rel(path) for path in missing]}, ensure_ascii=False, indent=2))
        return 1

    frame = pd.read_parquet(aw.io_path(BASE_FRAME))
    frame, margin, precision_risk = materialize_weights(frame)
    base_features = read_csv(BASE_FEATURES)
    allowed_features = [row["feature_name"] for row in base_features]
    task_rows = materialize_task_seeds()
    weight_rows = weight_audit(frame)
    summary = build_summary(frame, allowed_features, weight_rows, task_rows)
    allowed_rows = allowed_feature_rows(base_features)
    feature_boundary = feature_boundary_rows(allowed_features, frame, summary)
    target_audit = target_contract_audit(task_rows)
    parity_audit = parity_precision_audit(frame, margin, precision_risk)
    positive_rows = [dict(row) for row in read_csv(HH_POSITIVE_SEED)]
    negative_rows = [dict(row) for row in read_csv(HH_NEGATIVE)]
    release_rows = [dict(row) for row in read_csv(HH_RELEASE)]
    queue_rows = review_queue()
    summary["feature_boundary_failed_rows"] = sum(1 for row in feature_boundary if row.get("status") != "passed")
    summary["parity_precision_failed_rows"] = sum(1 for row in parity_audit if row.get("status") != "passed")
    summary["review_queue_rows"] = len(queue_rows)

    final = make_final(summary, summary["feature_boundary_failed_rows"], summary["parity_precision_failed_rows"])
    artifacts = [
        write_csv(MATERIALIZATION_SOURCE_MAP, SOURCE_COLUMNS, source_map()),
        write_csv(ALLOWED_FEATURE_SET, list(base_features[0].keys()) if base_features else ("feature_name",), allowed_rows),
        write_csv(WEIGHT_RECIPE_MATRIX, WEIGHT_RECIPE_COLUMNS, weight_recipes()),
        write_csv(WEIGHT_AUDIT, WEIGHT_AUDIT_COLUMNS, weight_rows),
        write_csv(TARGET_CONTRACT_AUDIT, AUDIT_COLUMNS, target_audit),
        write_csv(PARITY_PRECISION_AUDIT, AUDIT_COLUMNS, parity_audit),
        write_csv(FEATURE_LABEL_BOUNDARY, AUDIT_COLUMNS, feature_boundary),
        write_csv(POSITIVE_SEED_MATERIALIZATION, hh.PLAN_COLUMNS, positive_rows),
        write_csv(NEGATIVE_CONTROL_MATERIALIZATION, hh.PLAN_COLUMNS, negative_rows),
        write_csv(RELEASE_GATE_MATERIALIZATION, hh.RELEASE_COLUMNS, release_rows),
        write_csv(TRAINING_TASK_SEEDS, TASK_SEED_COLUMNS, task_rows),
        write_csv(HJ_QUEUE, QUEUE_COLUMNS, queue_rows),
    ]
    aw.io_path(TRAIN_ONLY_REPAIR_FRAME.parent).mkdir(parents=True, exist_ok=True)
    frame.to_parquet(aw.io_path(TRAIN_ONLY_REPAIR_FRAME), index=False)
    artifacts.insert(0, TRAIN_ONLY_REPAIR_FRAME)

    gates = build_gates(final)
    final["gate_rows"] = len(gates)
    final["passed_gates"] = sum(1 for row in gates if row["status"] == "passed")
    final["failed_gates"] = [row["gate_id"] for row in gates if row["status"] != "passed"]
    artifacts.extend(
        [
            write_csv(GATE_AUDIT, GATE_COLUMNS, gates),
            write_json(FINAL_DECISION, final),
            write_json(
                RUN_MANIFEST,
                {
                    "run_id": RUN_ID,
                    "parent_run_id": PARENT_RUN_ID,
                    "next_run_id": NEXT_RUN_ID,
                    "inputs": [rel(path) for path in INPUT_FILES],
                    "outputs": [rel(path) for path in OUTPUT_FILES],
                    "producer": rel(Path(__file__)),
                    "claim_boundary": CLAIM_BOUNDARY,
                },
            ),
        ]
    )
    artifacts.extend(build_receipts(final, artifacts))
    artifacts.extend([write_report(final), write_decision(final)])
    artifacts.extend(update_docs(final))
    artifacts.extend(update_registers(final))
    artifacts.append(update_artifact_registry(artifacts))
    print(
        json.dumps(
            json_ready(
                {
                    "run_id": RUN_ID,
                    "status": final["status"],
                    "rows": final["rows"],
                    "feature_count": final["feature_count"],
                    "new_weight_count": final["new_weight_count"],
                    "target_contract": f"{final['task_target_label_class_rows']}/{final['task_seed_rows']} label_class",
                    "gates": f"{final['passed_gates']}/{final['gate_rows']}",
                    "next_action": final["next_action"],
                    "goal_achieve": "not_claimed",
                }
            ),
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )
    return 0 if not final["failed_gates"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
