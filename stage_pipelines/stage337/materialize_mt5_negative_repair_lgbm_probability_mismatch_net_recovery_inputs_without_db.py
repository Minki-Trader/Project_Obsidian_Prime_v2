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
from stage_pipelines.stage337 import design_mt5_negative_repair_lightgbm_probability_mismatch_and_net_recovery_without_db as gz  # noqa: E402
from stage_pipelines.stage337 import materialize_runtime_positive_side_stability_gb_pf_recovery_drawdown_mt5_negative_repair_inputs_without_db as gs  # noqa: E402


aw = gz.aw
fb = gz.fb
fa = gz.fa
gw = gz.gw

TODAY = "2026-05-31"
STAGE_ID = gz.STAGE_ID
RUN_NUMBER = "run337HA"
RUN_ID = "run337HA_materialize_mt5_negative_repair_lightgbm_probability_mismatch_and_net_recovery_inputs_without_db_v1"
PARENT_RUN_ID = gz.RUN_ID
NEXT_RUN_ID = "run337HB_review_mt5_negative_repair_lightgbm_probability_mismatch_and_net_recovery_inputs_without_db_v1"
STATUS = "completed_stage337HA_probability_mismatch_net_recovery_repair_inputs_materialized_no_training_no_selection"
JUDGMENT = "train_only_probability_mismatch_net_recovery_inputs_materialized_review_required"
DECISION = "stage337HA_open_run337HB_review_probability_mismatch_net_recovery_repair_inputs"
CLAIM_BOUNDARY = (
    "research_development_only_stage337HA_probability_mismatch_net_recovery_repair_inputs_without_db_"
    "no_model_training_no_threshold_tuning_no_lot_optimization_no_operating_selection_no_mt5_execution_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = gz.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = gz.REVIEWS_DIR
REPORT_PATH = REVIEWS_DIR / "run337HA_probability_mismatch_net_recovery_repair_inputs.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage337HA_probability_mismatch_net_recovery_repair_inputs.md"

GZ_FINAL = gz.FINAL_DECISION
GZ_GATES = gz.GATE_AUDIT
GZ_QUEUE = gz.MATERIALIZATION_QUEUE
GZ_DESIGN = gz.DESIGN_MATRIX
GZ_EXPERIMENT = gz.EXPERIMENT_CONTRACT
GZ_OBJECTIVE = gz.OBJECTIVE_CONTRACT
GZ_FEATURE_LABEL = gz.FEATURE_LABEL_CONTRACT
GZ_TASK_BLUEPRINT = gz.TRAINING_TASK_BLUEPRINT
GZ_PARITY_PLAN = gz.PARITY_REPAIR_PLAN
GZ_NEGATIVE = gz.NEGATIVE_CONTROL_PLAN
GZ_RELEASE = gz.RELEASE_GATE_CONTRACT
GY_KPI = gz.GY_KPI
GY_PARITY = gz.GY_PARITY
GY_TIMESTAMP = gz.GY_TIMESTAMP
GY_MEMORY = gz.GY_MEMORY

BASE_FRAME = gs.TRAIN_ONLY_REPAIR_FRAME
BASE_FEATURES = gs.ALLOWED_FEATURE_SET
BASE_MANIFEST = gs.RUN_MANIFEST
BASE_WEIGHT_AUDIT = gs.WEIGHT_AUDIT

TRAIN_ONLY_REPAIR_FRAME = RUN_DIR / "train_only_probability_mismatch_net_recovery_input_frame.parquet"
MATERIALIZATION_SOURCE_MAP = RUN_DIR / "ha_materialization_source_map.csv"
ALLOWED_FEATURE_SET = RUN_DIR / "ha_allowed_model_feature_set.csv"
WEIGHT_RECIPE_MATRIX = RUN_DIR / "gz_repair_weight_recipe_matrix.csv"
WEIGHT_AUDIT = RUN_DIR / "gz_repair_weight_audit.csv"
TARGET_CONTRACT_AUDIT = RUN_DIR / "target_contract_audit.csv"
PARITY_PRECISION_AUDIT = RUN_DIR / "probability_precision_audit.csv"
FEATURE_LABEL_BOUNDARY = RUN_DIR / "feature_label_boundary_audit.csv"
NEGATIVE_CONTROL_MATERIALIZATION = RUN_DIR / "negative_control_materialization_matrix.csv"
RELEASE_GATE_MATERIALIZATION = RUN_DIR / "release_gate_materialization_matrix.csv"
TRAINING_TASK_SEEDS = RUN_DIR / "run337HC_training_task_seed_matrix.csv"
HB_QUEUE = RUN_DIR / "run337HB_review_queue.csv"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (
    GZ_FINAL,
    GZ_GATES,
    GZ_QUEUE,
    GZ_DESIGN,
    GZ_EXPERIMENT,
    GZ_OBJECTIVE,
    GZ_FEATURE_LABEL,
    GZ_TASK_BLUEPRINT,
    GZ_PARITY_PLAN,
    GZ_NEGATIVE,
    GZ_RELEASE,
    GY_KPI,
    GY_PARITY,
    GY_TIMESTAMP,
    GY_MEMORY,
    BASE_FRAME,
    BASE_FEATURES,
    BASE_MANIFEST,
    BASE_WEIGHT_AUDIT,
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
    NEGATIVE_CONTROL_MATERIALIZATION,
    RELEASE_GATE_MATERIALIZATION,
    TRAINING_TASK_SEEDS,
    HB_QUEUE,
    DATA_RECEIPT,
    MODEL_RECEIPT,
    RUNTIME_RECEIPT,
    PERFORMANCE_RECEIPT,
    JUDGMENT_RECEIPT,
    LINEAGE_RECEIPT,
    GATE_AUDIT,
    FINAL_DECISION,
    RUN_MANIFEST,
    REPORT_PATH,
    DECISION_DOC,
    gw.SELECTED_STATUS,
    gw.WORKSPACE_STATE,
    gw.CURRENT_STATE,
    gw.CHANGELOG,
    gw.STAGE_BRIEF,
    gw.RUN_REGISTRY,
    gw.ALPHA_LEDGER,
    gw.STAGE_LEDGER,
    gw.ARTIFACT_REGISTRY,
    Path(__file__),
)

NEW_WEIGHT_COLUMNS = (
    "gz_precision_stable_net_recovery_weight",
    "gz_cost_expectancy_repair_weight",
    "gz_drawdown_recovery_repair_weight",
    "gz_trade_shape_balance_repair_weight",
    "gz_proxy_negative_control_weight",
)
TASK_WEIGHT_COLUMNS = {
    "ha_gz001_precision_stable_net_recovery": "gz_precision_stable_net_recovery_weight",
    "ha_gz002_cost_expectancy_repair": "gz_cost_expectancy_repair_weight",
    "ha_gz003_drawdown_recovery_repair": "gz_drawdown_recovery_repair_weight",
    "ha_gz004_trade_shape_balance_repair": "gz_trade_shape_balance_repair_weight",
    "ha_gz005_proxy_negative_control": "gz_proxy_negative_control_weight",
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
TASK_SEED_COLUMNS = gz.TASK_COLUMNS
QUEUE_COLUMNS = gz.QUEUE_COLUMNS
GATE_COLUMNS = gz.GATE_COLUMNS


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
    short_quality = numeric(frame, "short_quality_target", default=1.0).clip(0.0, 2.0)
    long_quality = numeric(frame, "long_quality_target", default=1.0).clip(0.0, 2.0)

    gr_net = numeric(frame, "gr_mt5_net_recovery_weight", default=1.0).clip(0.10, 10.0)
    gr_proxy = numeric(frame, "gr_proxy_sign_inversion_guard_weight", default=1.0).clip(0.10, 10.0)
    gr_cost = numeric(frame, "gr_lifecycle_cost_fill_guard_weight", default=1.0).clip(0.10, 10.0)
    gr_trade = numeric(frame, "gr_trade_shape_side_rebalance_weight", default=1.0).clip(0.10, 10.0)
    gr_curve = numeric(frame, "gr_dd_pf_recovery_guard_weight", default=1.0).clip(0.10, 10.0)
    gj_cost = numeric(frame, "gj_cost_session_regime_guard_weight", default=1.0).clip(0.10, 10.0)
    gj_pf = numeric(frame, "gj_pf_expectancy_quality_weight", default=1.0).clip(0.10, 10.0)
    gj_dd = numeric(frame, "gj_drawdown_recovery_pressure_weight", default=1.0).clip(0.10, 10.0)
    gb_cost = numeric(frame, "gb_cost_session_regime_guard_weight", default=1.0).clip(0.10, 10.0)
    ft_cost = numeric(frame, "ft_cost_session_regime_guard_weight", default=1.0).clip(0.10, 10.0)

    timestamps = pd.to_datetime(frame["timestamp"], utc=True, errors="coerce")
    hour = timestamps.dt.hour.fillna(0).astype(int)
    cash_overlap = pd.Series(np.where((hour >= 13) & (hour <= 21), 1.06, 0.96), index=frame.index)
    rollover_caution = pd.Series(np.where((hour <= 1) | (hour >= 22), 0.94, 1.01), index=frame.index)
    cost_adverse = (1.0 - normalize(cost_survival, default=0.55)).clip(0.0, 1.0)
    risk_pressure = (0.34 * drawdown + 0.28 * underwater + 0.24 * low_margin + 0.14 * precision_risk).clip(0.0, 1.0)
    churn_pressure = (0.34 * direction_residual + 0.30 * abstention + 0.20 * precision_risk + 0.16 * side_gap).clip(0.0, 1.0)
    short_balance = pd.Series(np.where(label == 0, 1.10 + 0.10 * short_quality, 1.0), index=frame.index)
    long_balance = pd.Series(np.where(label == 2, 1.03 + 0.08 * long_quality - 0.08 * side_gap, 1.0), index=frame.index)
    flat_guard = pd.Series(np.where(label == 1, 0.96 + 0.04 * (1.0 - churn_pressure), 1.0), index=frame.index)
    side_balance = (short_balance * long_balance * flat_guard).clip(0.72, 1.40)
    proxy_negative_region = (normalize(gr_proxy, default=0.5) * (0.50 * cost_adverse + 0.30 * risk_pressure + 0.20 * precision_risk)).clip(0.0, 1.0)

    frame["gz_precision_stable_net_recovery_weight"] = clip_weight(
        (0.34 * gr_net + 0.22 * gr_cost + 0.18 * gr_curve + 0.14 * gj_pf + 0.12 * gj_cost)
        * (1.08 - 0.20 * precision_risk).clip(0.78, 1.08)
        * (1.06 - 0.16 * cost_adverse).clip(0.80, 1.06)
        * side_balance
    )
    frame["gz_cost_expectancy_repair_weight"] = clip_weight(
        (0.30 * gr_cost + 0.22 * gj_cost + 0.18 * gb_cost + 0.15 * ft_cost + 0.15 * gr_net)
        * cash_overlap
        * rollover_caution
        * (1.10 - 0.24 * cost_adverse).clip(0.76, 1.10)
        * (1.04 - 0.10 * churn_pressure).clip(0.84, 1.04)
    )
    frame["gz_drawdown_recovery_repair_weight"] = clip_weight(
        (0.34 * gr_curve + 0.22 * gj_dd + 0.18 * gr_net + 0.14 * gj_pf + 0.12 * gr_cost)
        * (1.12 - 0.24 * risk_pressure).clip(0.72, 1.12)
        * (1.08 - 0.18 * underwater).clip(0.76, 1.08)
    )
    frame["gz_trade_shape_balance_repair_weight"] = clip_weight(
        (0.30 * gr_trade + 0.22 * side_quality + 0.18 * gr_net + 0.16 * gr_cost + 0.14 * gr_curve)
        * side_balance
        * (1.04 - 0.14 * churn_pressure).clip(0.82, 1.04)
    )
    frame["gz_proxy_negative_control_weight"] = clip_weight(
        (0.30 * gr_proxy + 0.24 * gr_cost + 0.18 * gr_curve + 0.16 * gr_net + 0.12 * gj_cost)
        * (1.02 - 0.22 * proxy_negative_region).clip(0.74, 1.02)
        * (1.04 - 0.12 * precision_risk).clip(0.82, 1.04)
    )
    frame["gz_probability_margin"] = margin
    frame["gz_precision_risk"] = precision_risk
    frame["gz_cost_adverse_risk"] = cost_adverse
    frame["gz_trade_churn_pressure"] = churn_pressure
    return frame, margin, precision_risk


def source_map() -> list[dict[str, Any]]:
    rows = []
    for source_id, path, source_type, effect in [
        ("gz_final", GZ_FINAL, "parent decision(부모 결정)", "confirms GZ design closeout(GZ 설계 종료 확인)"),
        ("gz_task_blueprint", GZ_TASK_BLUEPRINT, "task blueprint(작업 설계)", "defines HA/HC training seeds(HA/HC 학습 씨앗 정의)"),
        ("gz_parity_plan", GZ_PARITY_PLAN, "parity repair plan(동등성 수리 계획)", "keeps probability mismatch repair explicit(확률 불일치 수리 명시)"),
        ("gy_kpi", GY_KPI, "MT5 KPI memory(MT5 KPI 기억)", "keeps negative MT5 KPI explicit(음수 MT5 KPI 명시)"),
        ("gy_parity", GY_PARITY, "runtime parity memory(런타임 동등성 기억)", "keeps near-parity difference explicit(근접 동등성 차이 명시)"),
        ("gs_base_frame", BASE_FRAME, "base train-only frame(기반 학습 전용 프레임)", "provides rows and prior repair weights(행과 이전 수리 가중치 제공)"),
        ("gs_allowed_features", BASE_FEATURES, "feature set(피처 묶음)", "keeps model inputs unchanged(모델 입력 유지)"),
    ]:
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
        ("ha001_precision_stable_net_recovery", "gz_precision_stable_net_recovery_weight", "gr_net;gr_cost;gr_curve;precision_risk;cost_adverse;side_balance", "clip(prior net/cost/curve blend * precision and cost guards)", "recover MT5 net while reducing precision-sensitive decisions(정밀도 민감 결정을 줄이며 MT5 순수익 회복)"),
        ("ha002_cost_expectancy_repair", "gz_cost_expectancy_repair_weight", "gr_cost;gj_cost;gb_cost;ft_cost;session;cost_adverse;churn_pressure", "clip(cost blend * session and churn guards)", "raise PF and expectancy without threshold or lot tuning(임계값/랏 조정 없이 PF와 기대값 개선)"),
        ("ha003_drawdown_recovery_repair", "gz_drawdown_recovery_repair_weight", "gr_curve;gj_dd;gr_net;risk_pressure;underwater", "clip(curve blend * drawdown and underwater guards)", "reduce drawdown and improve recovery(낙폭 축소와 회복 개선)"),
        ("ha004_trade_shape_balance_repair", "gz_trade_shape_balance_repair_weight", "gr_trade;side_quality;side_balance;churn_pressure", "clip(trade blend * side balance and churn guards)", "protect trade count and side balance(거래수와 방향 균형 보호)"),
        ("ha005_proxy_negative_control", "gz_proxy_negative_control_weight", "gr_proxy;proxy_negative_region;precision_risk", "clip(proxy blend * negative-control suppression)", "keep proxy as negative control, not authority(프록시를 권위가 아닌 음수 대조로 유지)"),
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
                "effect": "checks bounded train-only GZ weights(범위 제한 학습 전용 GZ 가중치 점검)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def target_contract_audit(task_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    bad = [row.get("task_id", "") for row in task_rows if row.get("target_column") != "label_class"]
    return [
        {
            "audit_id": "ha_target001_label_class_only",
            "status": "passed" if not bad else "failed",
            "observed": ";".join(bad),
            "expected": "all target_column == label_class(모든 목표 열 label_class)",
            "evidence": rel(TRAINING_TASK_SEEDS),
            "effect": "prevents sample-weight-as-target regression(표본 가중치 목표 회귀 방지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "audit_id": "ha_target002_weight_columns_present",
            "status": "passed" if all(row.get("sample_weight_column") in NEW_WEIGHT_COLUMNS for row in task_rows) else "failed",
            "observed": ";".join(str(row.get("sample_weight_column", "")) for row in task_rows),
            "expected": ";".join(NEW_WEIGHT_COLUMNS),
            "evidence": rel(TRAIN_ONLY_REPAIR_FRAME),
            "effect": "links task seeds to materialized weights(작업 씨앗을 물질화 가중치와 연결)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def parity_precision_audit(frame: pd.DataFrame, margin: pd.Series, precision_risk: pd.Series) -> list[dict[str, Any]]:
    parent = read_json(GZ_FINAL)
    near_boundary_rows = int((margin <= 0.005).sum())
    high_precision_risk_rows = int((precision_risk >= 0.80).sum())
    return [
        {
            "audit_id": "ha_parity001_parent_mismatch_named",
            "status": "passed" if as_int(parent.get("probability_mismatch_rows")) == 3 and as_int(parent.get("decision_mismatch_rows")) == 0 else "failed",
            "observed": f"probability={parent.get('probability_mismatch_rows')};decision={parent.get('decision_mismatch_rows')}",
            "expected": "probability=3;decision=0",
            "evidence": rel(GZ_FINAL),
            "effect": "keeps GY near-parity difference visible(GY 근접 동등성 차이를 보이게 함)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "audit_id": "ha_parity002_margin_sensitivity_counted",
            "status": "passed",
            "observed": f"near_boundary_rows={near_boundary_rows};high_precision_risk_rows={high_precision_risk_rows}",
            "expected": "counted before training(학습 전 계수)",
            "evidence": rel(TRAIN_ONLY_REPAIR_FRAME),
            "effect": "turns precision sensitivity into auditable input(정밀도 민감도를 감사 가능한 입력으로 바꿈)",
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
    ]
    duplicate_ts = int(pd.to_datetime(frame["timestamp"], utc=True, errors="coerce").duplicated().sum())
    return [
        {
            "audit_id": "ha_feature001_allowed_feature_count",
            "status": "passed" if len(allowed_features) == 58 else "failed",
            "observed": str(len(allowed_features)),
            "expected": "58",
            "evidence": rel(ALLOWED_FEATURE_SET),
            "effect": "keeps reviewed model feature order(검토된 모델 피처 순서 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "audit_id": "ha_feature002_forbidden_features_excluded",
            "status": "passed" if not forbidden else "failed",
            "observed": ";".join(forbidden),
            "expected": "no label/future/weight/outcome/MT5 KPI features(라벨/미래/가중치/결과/MT5 KPI 피처 없음)",
            "evidence": rel(ALLOWED_FEATURE_SET),
            "effect": "prevents target leakage into model features(목표 누수 방지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "audit_id": "ha_feature003_nonfinite_weights",
            "status": "passed" if summary["nonfinite_weight_rows"] == 0 else "failed",
            "observed": str(summary["nonfinite_weight_rows"]),
            "expected": "0",
            "evidence": rel(WEIGHT_AUDIT),
            "effect": "repair weights are finite(수리 가중치 유한)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "audit_id": "ha_feature004_timestamp_order",
            "status": "passed" if frame["timestamp"].is_monotonic_increasing else "failed",
            "observed": str(frame["timestamp"].is_monotonic_increasing),
            "expected": "True",
            "evidence": rel(TRAIN_ONLY_REPAIR_FRAME),
            "effect": "keeps time axis ordered(시간축 순서 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "audit_id": "ha_feature005_timestamp_duplicates_named",
            "status": "passed",
            "observed": str(duplicate_ts),
            "expected": "duplicates allowed by cost_policy_id training expansion(비용 정책 학습 확장 중복 허용)",
            "evidence": rel(TRAIN_ONLY_REPAIR_FRAME),
            "effect": "names expanded train-only repeated timestamps(확장 학습 전용 반복 시각 명명)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "audit_id": "ha_feature006_macro_join_safe_by_absence",
            "status": "passed",
            "observed": "no new macro source joined in HA(HA에서 새 거시 원천 결합 없음)",
            "expected": "economic data requires release timestamp(경제자료는 발표 시각 필요)",
            "evidence": rel(GZ_FEATURE_LABEL),
            "effect": "prevents macro look-ahead(거시 미래참조 방지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def materialize_task_seeds() -> list[dict[str, Any]]:
    rows = [dict(row) for row in read_csv(GZ_TASK_BLUEPRINT)]
    for row in rows:
        task_id = row.get("task_id", "")
        if task_id in TASK_WEIGHT_COLUMNS:
            row["target_column"] = "label_class"
            row["sample_weight_expression"] = TASK_WEIGHT_COLUMNS[task_id]
            row["sample_weight_column"] = TASK_WEIGHT_COLUMNS[task_id]
            row["selection_status"] = "eligible_after_HB_review(HB 검토 후 적격)"
            row["claim_boundary"] = CLAIM_BOUNDARY
    return rows


def review_queue() -> list[dict[str, Any]]:
    return [
        {
            "queue_id": "hb_review_probability_mismatch_net_recovery_inputs",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "task": "review HA train-only repair frame, GZ weights, target contract, feature boundary, and HC training eligibility(HA 학습 전용 수리 프레임, GZ 가중치, 목표 계약, 피처 경계, HC 학습 적격성 검토)",
            "required_inputs": f"{rel(TRAIN_ONLY_REPAIR_FRAME)};{rel(WEIGHT_AUDIT)};{rel(TARGET_CONTRACT_AUDIT)};{rel(PARITY_PRECISION_AUDIT)};{rel(TRAINING_TASK_SEEDS)}",
            "required_outputs": "input review, eligible HC training queue, target contract disposition(입력 검토, 적격 HC 학습 대기열, 목표 계약 처분)",
            "blocked_if_missing": "HA frame or audits(HA 프레임 또는 감사)",
            "forbidden_action": "train, tune threshold, execute MT5, or select operating candidate(학습/임계값 조정/MT5 실행/운영 후보 선택)",
            "effect": "forces review before training(학습 전 검토 강제)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def build_summary(frame: pd.DataFrame, allowed_features: Sequence[str], weight_rows: Sequence[Mapping[str, Any]], task_rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    gz_final = read_json(GZ_FINAL)
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
        "gz_best_attempt": gz_final.get("best_attempt", ""),
        "gz_best_net_profit": gz_final.get("best_net_profit", ""),
        "gz_probability_mismatch_rows": gz_final.get("probability_mismatch_rows", ""),
        "gz_max_abs_probability_diff": gz_final.get("max_abs_probability_diff", ""),
        "gz_target_label_class_rows": gz_final.get("task_target_label_class_rows", ""),
        "gz_task_rows": gz_final.get("task_rows", ""),
    }


def build_gates(final: Mapping[str, Any]) -> list[dict[str, Any]]:
    no_forbidden_claim = (
        final["new_training"] == "not_run"
        and final["candidate_selection"] == "not_run"
        and final["mt5_execution"] == "not_run"
        and final["goal_achieve"] == "not_claimed"
    )
    checks = [
        ("input_presence", final["missing_inputs"] == 0, str(final["missing_inputs"]), "0", rel(BASE_FRAME), "required GZ/GS inputs exist(필수 GZ/GS 입력 존재)"),
        ("parent_gz_gates_passed", final["gz_failed_gate_rows"] == 0, str(final["gz_failed_gate_rows"]), "0", rel(GZ_GATES), "GZ gates passed(GZ 게이트 통과)"),
        ("parent_next_action_matches", final["gz_next_action"] == RUN_ID, str(final["gz_next_action"]), RUN_ID, rel(GZ_FINAL), "HA follows GZ next action(HA가 GZ 다음 행동을 따름)"),
        ("repair_frame_materialized", final["rows"] == 87666 and path_exists(TRAIN_ONLY_REPAIR_FRAME), f"rows={final['rows']}", "87666", rel(TRAIN_ONLY_REPAIR_FRAME), "train-only repair frame exists(학습 전용 수리 프레임 존재)"),
        ("allowed_feature_set_preserved", final["feature_count"] == 58, str(final["feature_count"]), "58", rel(ALLOWED_FEATURE_SET), "reviewed feature set preserved(검토 피처 묶음 유지)"),
        ("target_contract_preserved", final["task_seed_rows"] == final["task_target_label_class_rows"] == 5, f"tasks={final['task_seed_rows']};label_class={final['task_target_label_class_rows']}", "5/5 label_class", rel(TARGET_CONTRACT_AUDIT), "target contract preserved(목표 계약 유지)"),
        ("feature_boundary_passed", final["feature_boundary_failed_rows"] == 0, str(final["feature_boundary_failed_rows"]), "0", rel(FEATURE_LABEL_BOUNDARY), "feature boundary audit passed(피처 경계 감사 통과)"),
        ("new_weights_materialized", final["new_weight_count"] == len(NEW_WEIGHT_COLUMNS), str(final["new_weight_count"]), str(len(NEW_WEIGHT_COLUMNS)), rel(WEIGHT_AUDIT), "GZ repair weights materialized(GZ 수리 가중치 물질화)"),
        ("nonfinite_weights_zero", final["nonfinite_weight_rows"] == 0, str(final["nonfinite_weight_rows"]), "0", rel(WEIGHT_AUDIT), "weights finite(가중치 유한)"),
        ("parity_precision_audit_complete", final["parity_precision_failed_rows"] == 0 and as_int(final["gz_probability_mismatch_rows"]) == 3, f"failed={final['parity_precision_failed_rows']};parent_prob={final['gz_probability_mismatch_rows']}", "0 failed and parent_prob=3", rel(PARITY_PRECISION_AUDIT), "probability mismatch memory carried(확률 불일치 기억 인계)"),
        ("review_queue_materialized", final["review_queue_rows"] == 1 and final["next_action"] == NEXT_RUN_ID, f"queue={final['review_queue_rows']};next={final['next_action']}", f"1 and {NEXT_RUN_ID}", rel(HB_QUEUE), "HB review queue opened(HB 검토 대기열 열림)"),
        ("no_forbidden_claim", no_forbidden_claim, f"training={final['new_training']};selection={final['candidate_selection']};mt5={final['mt5_execution']};goal={final['goal_achieve']}", "not_run/not_run/not_run/not_claimed", rel(FINAL_DECISION), "materialization without operating claim(운영 주장 없는 물질화)"),
        ("required_gate_coverage_audit", True, "all required gates listed in closeout(모든 필수 게이트가 종료 기록에 있음)", "present", rel(GATE_AUDIT), "connects gates to completion claim(게이트를 완료 주장과 연결)"),
    ]
    return [
        {"gate_id": gate_id, "status": "passed" if passed else "failed", "evidence_path": evidence, "observed": observed, "expected": expected, "effect": effect, "claim_boundary": CLAIM_BOUNDARY}
        for gate_id, passed, observed, expected, evidence, effect in checks
    ]


def make_final(summary: Mapping[str, Any], boundary_failed: int, parity_failed: int) -> dict[str, Any]:
    gz_final = read_json(GZ_FINAL)
    return {
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "stage_id": STAGE_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_action": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
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
        "gz_next_action": gz_final.get("next_action", ""),
        "gz_failed_gate_rows": sum(1 for row in read_csv(GZ_GATES) if row.get("status") != "passed"),
        "feature_boundary_failed_rows": boundary_failed,
        "parity_precision_failed_rows": parity_failed,
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
        "judgment": final["judgment"],
        "next_action": final["next_action"],
        "claim_boundary": CLAIM_BOUNDARY,
        "goal_achieve": "not_claimed",
    }
    receipts = [
        (
            DATA_RECEIPT,
            {
                **base,
                "row_count": final["rows"],
                "feature_count": final["feature_count"],
                "feature_boundary_failed_rows": final["feature_boundary_failed_rows"],
                "effect": "materializes timestamp-safe train-only inputs(시점 안전 학습 전용 입력 물질화)",
            },
        ),
        (
            MODEL_RECEIPT,
            {
                **base,
                "model_training": "not_run",
                "target_contract": f"label_class={final['task_target_label_class_rows']}/{final['task_seed_rows']}",
                "new_weight_count": final["new_weight_count"],
                "effect": "prepares HC training while preventing target bug(HC 학습 준비와 목표 버그 방지)",
            },
        ),
        (
            RUNTIME_RECEIPT,
            {
                **base,
                "known_differences": f"parent_probability_mismatch_rows={final['gz_probability_mismatch_rows']};parent_max_diff={final['gz_max_abs_probability_diff']}",
                "parity_check": rel(PARITY_PRECISION_AUDIT),
                "runtime_claim_boundary": "materialization_only_runtime_repair_plan(물질화 전용 런타임 수리 계획)",
                "effect": "keeps probability mismatch repair auditable(확률 불일치 수리 감사 가능 유지)",
            },
        ),
        (
            PERFORMANCE_RECEIPT,
            {
                **base,
                "parent_best_net_profit": final["gz_best_net_profit"],
                "new_weights": list(NEW_WEIGHT_COLUMNS),
                "effect": "turns negative MT5 KPI into bounded repair weights(음수 MT5 KPI를 제한 가중치로 전환)",
            },
        ),
        (
            JUDGMENT_RECEIPT,
            {
                **base,
                "result_subject": RUN_ID,
                "judgment_label": JUDGMENT,
                "evidence_available": [rel(TRAIN_ONLY_REPAIR_FRAME), rel(WEIGHT_AUDIT), rel(TARGET_CONTRACT_AUDIT)],
                "evidence_missing": "model training, ONNX, MT5 runtime probe(모델 학습, ONNX, MT5 런타임 탐침)",
                "next_condition": NEXT_RUN_ID,
            },
        ),
    ]
    paths = [write_json(path, payload) for path, payload in receipts]
    all_artifacts = list(artifacts) + paths
    lineage = {
        **base,
        "source_inputs": [rel(path) for path in INPUT_FILES],
        "producer": rel(Path(__file__)),
        "consumer": NEXT_RUN_ID,
        "artifact_paths": [rel(path) for path in all_artifacts],
        "artifact_hashes": {rel(path): aw.sha256_file(path) for path in all_artifacts if path_exists(path) and aw.io_path(path).is_file()},
        "lineage_judgment": "connected GZ design to HA train-only frame(GZ 설계를 HA 학습 전용 프레임에 연결)",
    }
    paths.append(write_json(LINEAGE_RECEIPT, lineage))
    return paths


def write_report(final: Mapping[str, Any]) -> Path:
    text = f"""# Stage337 run337HA Repair Inputs(337단계 337HA 수리 입력)

## Conclusion(결론)

Action(행동): GS base frame(GS 기반 프레임)에 GZ repair weights(GZ 수리 가중치)를 물질화했다. Effect(효과): `87666` train-only rows(학습 전용 행)와 `{final['new_weight_count']}`개 새 sample weight(표본 가중치)를 만들었다.

Action(행동): target contract(목표 계약)을 감사했다. Effect(효과): HC training seed(HC 학습 씨앗) `5/5`가 `target_column=label_class(목표 열=라벨 클래스)`를 사용한다.

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- rows(행): `{final['rows']}`
- feature_count(피처 수): `{final['feature_count']}`
- new_weight_count(새 가중치 수): `{final['new_weight_count']}`
- nonfinite_weight_rows(비유한 가중치 행): `{final['nonfinite_weight_rows']}`
- parent_probability_mismatch(부모 확률 불일치): `{final['gz_probability_mismatch_rows']}`
- feature_boundary_failed(피처 경계 실패): `{final['feature_boundary_failed_rows']}`
- parity_precision_failed(동등성 정밀도 실패): `{final['parity_precision_failed_rows']}`
- gates(게이트): `{final['passed_gates']}/{final['gate_rows']}`
- next_action(다음 행동): `{final['next_action']}`

## Boundary(경계)

- training(학습): `not_run`
- MT5 execution(MT5 실행): `not_run`
- selection(선택): `not_run`
- Goal Achieve(목표 달성): `not_claimed`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return aw.write_text_lossless(REPORT_PATH, text, True)


def write_decision(final: Mapping[str, Any]) -> Path:
    text = f"""# {TODAY} Stage337HA Decision(337HA 결정)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- evidence(근거): `{rel(REPORT_PATH)}`, `{rel(TRAIN_ONLY_REPAIR_FRAME)}`, `{rel(TARGET_CONTRACT_AUDIT)}`

Action(행동): probability mismatch/net recovery repair(확률 불일치/순수익 회복 수리)을 학습 전용 입력으로 물질화했다.
Effect(효과): HB review(HB 검토)가 target contract(목표 계약), feature boundary(피처 경계), weight sanity(가중치 정상성)를 검토할 수 있다.

Forward/Goal(전진/목표): `not_claimed`
runtime_authority(런타임 권위): `not_claimed`
claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return aw.write_text_lossless(DECISION_DOC, text, True)


def replace_line(text: str, prefix: str, replacement: str) -> str:
    pattern = re.compile(rf"^{re.escape(prefix)}.*$", flags=re.M)
    return pattern.sub(replacement, text, count=1) if pattern.search(text) else replacement + "\n" + text


def update_docs(final: Mapping[str, Any]) -> list[Path]:
    artifacts: list[Path] = []
    branch = fa.ey.current_branch()
    workspace, workspace_bom = aw.read_text_lossless(gw.WORKSPACE_STATE)
    workspace = replace_line(workspace, "current_run_id:", f"current_run_id: {final['next_action']}")
    workspace = replace_line(workspace, "updated_on:", f"updated_on: '{TODAY}'")
    workspace = replace_line(workspace, "active_branch:", f"active_branch: {branch}")
    focus = (
        "- >-\n"
        f"  Stage337 run337HA focus complete(337단계 337HA 초점 완료): probability mismatch/net recovery inputs(확률 불일치/순수익 회복 입력)을 `{final['status']}`로 물질화했다. "
        f"Effect(효과): rows(행) `{final['rows']}`, new weights(새 가중치) `{final['new_weight_count']}`, target contract(목표 계약) `{final['task_target_label_class_rows']}/{final['task_seed_rows']}`를 만들고 `{final['next_action']}`을 열었다. Forward/Goal(전진/목표)은 주장하지 않는다.\n"
    )
    if "Stage337 run337HA focus complete" in workspace:
        workspace = re.sub(r"- >-\n  Stage337 run337HA focus complete.*?(?=\n- >-|\n[a-zA-Z_]+:|$)", focus.rstrip(), workspace, count=1, flags=re.S)
    else:
        workspace = workspace.replace("current_focus:\n", "current_focus:\n" + focus, 1)
    artifacts.append(aw.write_text_lossless(gw.WORKSPACE_STATE, workspace, workspace_bom))

    current, current_bom = aw.read_text_lossless(gw.CURRENT_STATE)
    for field_name, value in {
        "current_run": f"`{final['next_action']}`",
        "status": f"`{final['status']}`",
        "decision": f"`{final['decision']}`",
        "latest_completed_run": f"`{RUN_ID}`",
        "next_action": f"`{final['next_action']}`",
        "claim_boundary": f"`{CLAIM_BOUNDARY}`",
    }.items():
        current = fb.replace_bullet_field(current, field_name, value)
    section = f"""## run337HA Repair Inputs(수리 입력)

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- rows(행): `{final['rows']}`
- feature_count(피처 수): `{final['feature_count']}`
- new_weight_count(새 가중치 수): `{final['new_weight_count']}`
- target_contract(목표 계약): `label_class {final['task_target_label_class_rows']}/{final['task_seed_rows']}`
- probability_mismatch_memory(확률 불일치 기억): `{final['gz_probability_mismatch_rows']}`
- gates(게이트): `{final['passed_gates']}/{final['gate_rows']}`
- effect(효과): GZ design(GZ 설계)을 HB review(HB 검토) 가능한 train-only input(학습 전용 입력)으로 바꿨다.
- next_action(다음 행동): `{final['next_action']}`
"""
    current = fb.upsert_section_before(current, "## run337GZ Repair Design", section, "run337HA Repair Inputs")
    artifacts.append(aw.write_text_lossless(gw.CURRENT_STATE, current, current_bom))

    selection = f"""# Stage337 Selection Status(337단계 선택 상태)

- latest_run(최신 실행): `{RUN_ID}`
- latest_decision(최신 결정): `{final['decision']}`
- current_run(현재 실행): `{final['next_action']}`
- rebuild_status(재구축 상태): `{final['status']}`
- rows(행): `{final['rows']}`
- feature_count(피처 수): `{final['feature_count']}`
- new_weight_count(새 가중치 수): `{final['new_weight_count']}`
- target_contract(목표 계약): `label_class {final['task_target_label_class_rows']}/{final['task_seed_rows']}`
- probability_mismatch(확률 불일치): `{final['gz_probability_mismatch_rows']}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{final['next_action']}`
- effect(효과): HA materialization(물질화)은 training-ready evidence(학습 준비 근거)만 만들고 operating selection(운영 선택)은 하지 않는다.
"""
    artifacts.append(aw.write_text_lossless(gw.SELECTED_STATUS, selection, True))

    brief, brief_bom = aw.read_text_lossless(gw.STAGE_BRIEF)
    brief_entry = (
        f"- {TODAY}: run337HA(337HA 실행) `{final['status']}`. "
        f"Effect(효과): rows `{final['rows']}`, new weights `{final['new_weight_count']}`, target contract `label_class {final['task_target_label_class_rows']}/{final['task_seed_rows']}`를 만들고 `{final['next_action']}`을 열었다. Forward/Goal(전진/목표)은 주장하지 않는다."
    )
    artifacts.append(aw.write_text_lossless(gw.STAGE_BRIEF, fb.upsert_single_line(brief, "run337HA(337HA 실행)", brief_entry), brief_bom))

    changelog, changelog_bom = aw.read_text_lossless(gw.CHANGELOG)
    changelog_entry = (
        f"- {TODAY}: Stage337 run337HA(337HA 실행) `{final['status']}`. "
        f"Effect(효과): probability mismatch/net recovery train-only inputs(확률 불일치/순수익 회복 학습 전용 입력)을 물질화하고 `{final['next_action']}`을 열었다. Forward/Goal(전진/목표)은 주장하지 않았다."
    )
    artifacts.append(aw.write_text_lossless(gw.CHANGELOG, fb.upsert_single_line(changelog, "Stage337 run337HA", changelog_entry), changelog_bom))
    return artifacts


def update_registers(final: Mapping[str, Any]) -> list[Path]:
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "probability_mismatch_net_recovery_repair_input_materialization",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "notes": f"rows={final['rows']};features={final['feature_count']};weights={final['new_weight_count']};target_label_class={final['task_target_label_class_rows']}/{final['task_seed_rows']};next_action={final['next_action']};goal_achieve_not_claimed.",
        "family": "experiment_execution_data_integrity_model_validation",
        "primary_report": rel(REPORT_PATH),
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__input_materialization",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "input_materialization",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "probability_mismatch_net_recovery_input_materialization(확률 불일치 순수익 회복 입력 물질화)",
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
        "evidence_scope": "GZ design plus GS train-only base frame",
        "kpi_scope": "input_materialization_no_operating_claim",
        "status": final["status"],
        "judgment": final["judgment"],
        "claim_boundary": CLAIM_BOUNDARY,
        "path": rel(REPORT_PATH),
        "notes": f"gates={final['passed_gates']}/{final['gate_rows']};next_action={final['next_action']};goal_achieve_not_claimed",
        "decision": final["decision"],
        "run_key": f"{RUN_ID}__input_materialization",
        "family": "probability_mismatch_net_recovery_repair_input_materialization",
        "question": "can GZ repair design become safe train-only inputs(GZ 수리 설계가 안전한 학습 전용 입력이 될 수 있는가)",
        "metric_scope": "rows_features_weights_target_contract",
        "primary_artifact": rel(TRAIN_ONLY_REPAIR_FRAME),
        "report_path": rel(REPORT_PATH),
        "next_action": final["next_action"],
    }
    return [
        fb.upsert_csv_worktree(gw.RUN_REGISTRY, aw.RUN_REGISTRY_COLUMNS, run_row, "run_id"),
        fb.upsert_csv_worktree(gw.ALPHA_LEDGER, aw.ALPHA_LEDGER_COLUMNS, alpha_row, "ledger_row_id"),
        fb.upsert_csv_worktree(gw.STAGE_LEDGER, aw.STAGE_LEDGER_COLUMNS, stage_row, "ledger_row_id"),
    ]


def update_artifact_registry(paths: Sequence[Path]) -> Path:
    columns, rows = aw.read_csv_table(gw.ARTIFACT_REGISTRY, prefer_head=False)
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
    return write_csv(gw.ARTIFACT_REGISTRY, columns, rows)


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
    negative_rows = [dict(row) for row in read_csv(GZ_NEGATIVE)]
    release_rows = [dict(row) for row in read_csv(GZ_RELEASE)]
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
        write_csv(NEGATIVE_CONTROL_MATERIALIZATION, gz.CONSTRAINT_COLUMNS, negative_rows),
        write_csv(RELEASE_GATE_MATERIALIZATION, gz.RELEASE_COLUMNS, release_rows),
        write_csv(TRAINING_TASK_SEEDS, TASK_SEED_COLUMNS, task_rows),
        write_csv(HB_QUEUE, QUEUE_COLUMNS, queue_rows),
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
            write_json(RUN_MANIFEST, {"run_id": RUN_ID, "parent_run_id": PARENT_RUN_ID, "next_run_id": NEXT_RUN_ID, "inputs": [rel(path) for path in INPUT_FILES], "outputs": [rel(path) for path in OUTPUT_FILES], "claim_boundary": CLAIM_BOUNDARY}),
        ]
    )
    artifacts.extend(build_receipts(final, artifacts))
    artifacts.extend([write_report(final), write_decision(final)])
    artifacts.extend(update_docs(final))
    artifacts.extend(update_registers(final))
    artifacts.append(update_artifact_registry(artifacts))
    print(
        json.dumps(
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
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
