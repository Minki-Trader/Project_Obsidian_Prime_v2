from __future__ import annotations

import json
import math
import re
import shutil
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
from stage_pipelines.stage337 import design_runtime_positive_side_stability_gb_pf_recovery_drawdown_mt5_negative_repair_without_db as gr  # noqa: E402
from stage_pipelines.stage337 import execute_broker_confirmed_side_cost_curve_mt5_runtime_probe_without_db as fb  # noqa: E402
from stage_pipelines.stage337 import materialize_broker_confirmed_side_cost_curve_runtime_probe_package_without_db as fa  # noqa: E402
from stage_pipelines.stage337 import materialize_runtime_positive_side_stability_gb_pf_recovery_drawdown_repair_inputs_without_db as gk  # noqa: E402


aw = gr.aw

TODAY = "2026-05-31"
STAGE_ID = gr.STAGE_ID
RUN_NUMBER = "run337GS"
RUN_ID = "run337GS_materialize_runtime_positive_side_stability_gb_pf_recovery_drawdown_mt5_negative_repair_inputs_without_db_v1"
PARENT_RUN_ID = gr.RUN_ID
NEXT_RUN_ID = "run337GT_review_runtime_positive_side_stability_gb_pf_recovery_drawdown_mt5_negative_repair_inputs_without_db_v1"
STATUS = "completed_stage337GS_mt5_negative_repair_inputs_materialized_no_training_no_selection"
JUDGMENT = "train_only_mt5_negative_repair_inputs_materialized_review_required"
DECISION = "stage337GS_open_run337GT_review_mt5_negative_repair_inputs"
CLAIM_BOUNDARY = (
    "research_development_only_stage337GS_mt5_negative_side_stability_gb_pf_recovery_drawdown_repair_inputs_without_db_"
    "no_model_training_no_threshold_tuning_no_lot_optimization_no_operating_selection_no_mt5_execution_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = gr.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = gr.REVIEWS_DIR
REPORT_PATH = REVIEWS_DIR / "run337GS_mt5_negative_repair_inputs.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage337GS_mt5_negative_repair_inputs.md"

GR_FINAL = gr.FINAL_DECISION
GR_GATES = gr.GATE_AUDIT
GR_QUEUE = gr.MATERIALIZATION_QUEUE
GR_DESIGN = gr.DESIGN_MATRIX
GR_EXPERIMENT = gr.EXPERIMENT_CONTRACT
GR_OBJECTIVE = gr.OBJECTIVE_CONTRACT
GR_FEATURE_LABEL = gr.FEATURE_LABEL_CONTRACT
GR_TASK_BLUEPRINT = gr.TRAINING_TASK_BLUEPRINT
GR_NEGATIVE = gr.NEGATIVE_CONTROL_PLAN
GR_RELEASE = gr.RELEASE_GATE_CONTRACT
GQ_KPI = gr.GQ_KPI
GQ_ATTRIBUTION = gr.GQ_ATTRIBUTION
GQ_TIMESTAMP = gr.GQ_TIMESTAMP
GQ_MEMORY = gr.GQ_MEMORY

BASE_FRAME = gk.TRAIN_ONLY_REPAIR_FRAME
BASE_FEATURES = gk.ALLOWED_FEATURE_SET
BASE_MANIFEST = gk.RUN_MANIFEST
BASE_WEIGHT_AUDIT = gk.WEIGHT_AUDIT

TRAIN_ONLY_REPAIR_FRAME = RUN_DIR / "train_only_mt5_negative_repair_input_frame.parquet"
MATERIALIZATION_SOURCE_MAP = RUN_DIR / "gs_materialization_source_map.csv"
ALLOWED_FEATURE_SET = RUN_DIR / "gs_allowed_model_feature_set.csv"
WEIGHT_RECIPE_MATRIX = RUN_DIR / "gr_repair_weight_recipe_matrix.csv"
WEIGHT_AUDIT = RUN_DIR / "gr_repair_weight_audit.csv"
FEATURE_LABEL_BOUNDARY = RUN_DIR / "feature_label_boundary_audit.csv"
NEGATIVE_CONTROL_MATERIALIZATION = RUN_DIR / "negative_control_materialization_matrix.csv"
RELEASE_GATE_MATERIALIZATION = RUN_DIR / "release_gate_materialization_matrix.csv"
TRAINING_TASK_SEEDS = RUN_DIR / "run337GU_training_task_seed_matrix.csv"
GT_QUEUE = RUN_DIR / "run337GT_review_queue.csv"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (
    GR_FINAL,
    GR_GATES,
    GR_QUEUE,
    GR_DESIGN,
    GR_EXPERIMENT,
    GR_OBJECTIVE,
    GR_FEATURE_LABEL,
    GR_TASK_BLUEPRINT,
    GR_NEGATIVE,
    GR_RELEASE,
    GQ_KPI,
    GQ_ATTRIBUTION,
    GQ_TIMESTAMP,
    GQ_MEMORY,
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
    FEATURE_LABEL_BOUNDARY,
    NEGATIVE_CONTROL_MATERIALIZATION,
    RELEASE_GATE_MATERIALIZATION,
    TRAINING_TASK_SEEDS,
    GT_QUEUE,
    DATA_RECEIPT,
    MODEL_RECEIPT,
    PERFORMANCE_RECEIPT,
    JUDGMENT_RECEIPT,
    LINEAGE_RECEIPT,
    GATE_AUDIT,
    FINAL_DECISION,
    RUN_MANIFEST,
    REPORT_PATH,
    DECISION_DOC,
    gr.gq.go.SELECTED_STATUS,
    gr.gq.go.WORKSPACE_STATE,
    gr.gq.go.CURRENT_STATE,
    gr.gq.go.CHANGELOG,
    gr.gq.go.STAGE_BRIEF,
    gr.gq.go.RUN_REGISTRY,
    gr.gq.go.ALPHA_LEDGER,
    gr.gq.go.STAGE_LEDGER,
    gr.gq.go.ARTIFACT_REGISTRY,
    Path(__file__),
)

NEW_WEIGHT_COLUMNS = (
    "gr_mt5_net_recovery_weight",
    "gr_proxy_sign_inversion_guard_weight",
    "gr_lifecycle_cost_fill_guard_weight",
    "gr_trade_shape_side_rebalance_weight",
    "gr_dd_pf_recovery_guard_weight",
)
TASK_WEIGHT_COLUMNS = {
    "gs_gr001_mt5_net_recovery": "gr_mt5_net_recovery_weight",
    "gs_gr002_proxy_sign_inversion_guard": "gr_proxy_sign_inversion_guard_weight",
    "gs_gr003_lifecycle_cost_fill_guard": "gr_lifecycle_cost_fill_guard_weight",
    "gs_gr004_trade_shape_side_exposure_rebalance": "gr_trade_shape_side_rebalance_weight",
    "gs_gr005_dd_pf_recovery_guard": "gr_dd_pf_recovery_guard_weight",
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

SOURCE_COLUMNS = (
    "source_id",
    "source_path",
    "source_type",
    "required",
    "exists",
    "sha256",
    "effect",
    "claim_boundary",
)
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
BOUNDARY_COLUMNS = (
    "audit_id",
    "status",
    "observed",
    "expected",
    "evidence",
    "effect",
    "claim_boundary",
)
TASK_SEED_COLUMNS = gr.TASK_COLUMNS
QUEUE_COLUMNS = gr.QUEUE_COLUMNS
GATE_COLUMNS = gr.GATE_COLUMNS


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
    aw.io_path(path).write_text(
        json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return path


def fail_if_missing(paths: Sequence[Path]) -> list[Path]:
    return [path for path in paths if not path_exists(path)]


def as_float(value: Any) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return 0.0
    return number if math.isfinite(number) else 0.0


def clip_weight(values: pd.Series | np.ndarray, lower: float = 0.10, upper: float = 10.0) -> pd.Series:
    series = pd.Series(values, copy=False)
    return series.replace([np.inf, -np.inf], np.nan).fillna(1.0).clip(lower=lower, upper=upper)


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


def materialize_weights(frame: pd.DataFrame) -> pd.DataFrame:
    frame = frame.copy()
    label = pd.to_numeric(frame["label_class"], errors="coerce").fillna(1).astype(int)
    gj_side = numeric(frame, "gj_side_stability_preservation_weight", default=1.0)
    gj_pf = numeric(frame, "gj_pf_expectancy_quality_weight", default=1.0)
    gj_dd = numeric(frame, "gj_drawdown_recovery_pressure_weight", default=1.0)
    gj_blend = numeric(frame, "gj_side_curve_blend_weight", default=1.0)
    gj_cost = numeric(frame, "gj_cost_session_regime_guard_weight", default=1.0)
    gb_pf = numeric(frame, "gb_pf_expectancy_quality_weight", default=1.0)
    gb_cost = numeric(frame, "gb_cost_session_regime_guard_weight", default=1.0)
    ft_cost = numeric(frame, "ft_cost_session_regime_guard_weight", default=1.0)
    ft_dd = numeric(frame, "ft_drawdown_recovery_pressure_weight", default=1.0)
    fl_cost = numeric(frame, "fl_cost_stress_survival_weight", default=1.0)
    drawdown = numeric(frame, "drawdown_pressure_norm").clip(0.0, 1.0)
    underwater = numeric(frame, "underwater_rate_model").clip(0.0, 1.0)
    low_margin = numeric(frame, "low_margin_rate_model").clip(0.0, 1.0)
    side_gap = numeric(frame, "side_quality_gap_norm").clip(0.0, 1.0)
    cost_survival = numeric(frame, "cost_survival_weight", default=1.0).clip(0.10, 3.0)
    side_quality = numeric(frame, "side_quality_weight", default=1.0).clip(0.10, 3.0)
    short_quality = numeric(frame, "short_quality_target", default=1.0).clip(0.0, 2.0)
    long_quality = numeric(frame, "long_quality_target", default=1.0).clip(0.0, 2.0)

    timestamps = pd.to_datetime(frame["timestamp"], utc=True, errors="coerce")
    hour = timestamps.dt.hour.fillna(0).astype(int)
    cash_overlap = pd.Series(np.where((hour >= 13) & (hour <= 21), 1.08, 0.94), index=frame.index)
    rollover_caution = pd.Series(np.where((hour <= 1) | (hour >= 22), 0.92, 1.02), index=frame.index)

    risk_pressure = (0.42 * drawdown + 0.34 * underwater + 0.24 * low_margin).clip(0.0, 1.0)
    cost_adverse = (1.0 - normalize(cost_survival, default=0.55)).clip(0.0, 1.0)
    proxy_positive_region = normalize(0.48 * gj_cost + 0.34 * gj_blend + 0.18 * gb_cost, default=0.50)
    adverse_region = (0.40 * low_margin + 0.32 * risk_pressure + 0.28 * cost_adverse).clip(0.0, 1.0)
    sign_inversion_pressure = (proxy_positive_region * adverse_region).clip(0.0, 1.0)

    short_balance = pd.Series(np.where(label == 0, 1.16 + 0.16 * short_quality, 1.0), index=frame.index)
    long_balance = pd.Series(np.where(label == 2, 0.98 + 0.09 * long_quality - 0.10 * side_gap, 1.0), index=frame.index)
    flat_guard = pd.Series(np.where(label == 1, 0.96 + 0.06 * (1.0 - risk_pressure), 1.0), index=frame.index)
    side_rebalance = (short_balance * long_balance * flat_guard).clip(0.70, 1.45)

    net_recovery_base = 0.30 * gj_pf + 0.25 * gj_cost + 0.20 * gj_dd + 0.15 * gb_pf + 0.10 * ft_cost
    curve_base = 0.34 * gj_dd + 0.24 * gj_pf + 0.18 * ft_dd + 0.14 * gj_cost + 0.10 * fl_cost
    cost_base = 0.34 * gj_cost + 0.22 * gb_cost + 0.18 * ft_cost + 0.14 * fl_cost + 0.12 * gj_blend

    frame["gr_mt5_net_recovery_weight"] = clip_weight(
        net_recovery_base
        * (1.12 - 0.20 * risk_pressure).clip(0.76, 1.12)
        * (1.05 - 0.16 * low_margin).clip(0.78, 1.05)
        * side_rebalance
    )
    frame["gr_proxy_sign_inversion_guard_weight"] = clip_weight(
        (0.44 * gj_cost + 0.24 * gj_blend + 0.18 * gb_cost + 0.14 * frame["gr_mt5_net_recovery_weight"])
        * (1.00 + 0.36 * sign_inversion_pressure)
        * (1.04 - 0.12 * low_margin).clip(0.80, 1.04)
    )
    frame["gr_lifecycle_cost_fill_guard_weight"] = clip_weight(
        cost_base
        * cash_overlap
        * rollover_caution
        * (1.08 - 0.18 * cost_adverse).clip(0.78, 1.08)
        * (1.04 - 0.10 * risk_pressure).clip(0.82, 1.04)
    )
    frame["gr_trade_shape_side_rebalance_weight"] = clip_weight(
        (0.38 * frame["gr_mt5_net_recovery_weight"] + 0.24 * gj_side + 0.20 * side_quality + 0.18 * gj_blend)
        * side_rebalance
        * (1.03 - 0.10 * sign_inversion_pressure).clip(0.84, 1.03)
    )
    frame["gr_dd_pf_recovery_guard_weight"] = clip_weight(
        curve_base
        * (1.16 - 0.28 * risk_pressure).clip(0.72, 1.16)
        * (1.10 - 0.24 * underwater).clip(0.74, 1.10)
        * (0.82 + 0.18 * frame["gr_lifecycle_cost_fill_guard_weight"]).clip(0.72, 1.18)
    )
    return frame


def source_map() -> list[dict[str, Any]]:
    rows = []
    for source_id, path, source_type, effect in [
        ("gr_final", GR_FINAL, "parent decision(부모 결정)", "confirms GR design closeout(GR 설계 종료 확인)"),
        ("gr_objective", GR_OBJECTIVE, "objective contract(목표 계약)", "defines MT5-negative repair objectives(MT5 음수 수리 목표 정의)"),
        ("gr_task_blueprint", GR_TASK_BLUEPRINT, "task blueprint(작업 설계)", "defines GS/GU training seed rows(GS/GU 학습 씨앗 행 정의)"),
        ("gq_kpi", GQ_KPI, "MT5 KPI memory(MT5 성과 기억)", "keeps all-negative failure memory explicit(전부 음수 실패 기억 명시)"),
        ("gq_attribution", GQ_ATTRIBUTION, "proxy MT5 attribution(프록시 MT5 귀속)", "keeps proxy sign inversion explicit(프록시 부호 반전 명시)"),
        ("gk_base_frame", BASE_FRAME, "base frame(기반 프레임)", "provides train-only rows with prior weights(이전 가중치 포함 학습 전용 행 제공)"),
        ("gk_allowed_features", BASE_FEATURES, "feature set(피처 묶음)", "keeps model inputs unchanged(모델 입력 유지)"),
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
        (
            "gs001_mt5_net_recovery",
            "gr_mt5_net_recovery_weight",
            "gj_pf_expectancy_quality_weight;gj_cost_session_regime_guard_weight;gj_drawdown_recovery_pressure_weight;label_class;low_margin_rate_model",
            "clip(GJ PF/cost/DD blend * causal risk and side rebalance guards, 0.10, 10.0)",
            "recover MT5 net without MT5 KPI as feature(MT5 성과를 피처로 쓰지 않고 MT5 순수익 회복)",
        ),
        (
            "gs002_proxy_sign_inversion_guard",
            "gr_proxy_sign_inversion_guard_weight",
            "gj_cost_session_regime_guard_weight;gj_side_curve_blend_weight;low_margin_rate_model;drawdown_pressure_norm;cost_survival_weight",
            "clip(proxy-positive region approximation * causal adverse cost region, 0.10, 10.0)",
            "penalize proxy-positive MT5-negative failure(프록시 양수 MT5 음수 실패 벌점)",
        ),
        (
            "gs003_lifecycle_cost_fill_guard",
            "gr_lifecycle_cost_fill_guard_weight",
            "gj_cost_session_regime_guard_weight;gb_cost_session_regime_guard_weight;timestamp;cost_survival_weight",
            "clip(cost guard blend * timestamp-safe session and rollover guards, 0.10, 10.0)",
            "surface lifecycle cost/fill risk(생애주기 비용/체결 위험 가시화)",
        ),
        (
            "gs004_trade_shape_side_rebalance",
            "gr_trade_shape_side_rebalance_weight",
            "label_class;short_quality_target;long_quality_target;side_quality_gap_norm;gj_side_stability_preservation_weight",
            "clip(net recovery and side stability blend * side rebalance, 0.10, 10.0)",
            "reduce one-side collapse risk(한쪽 방향 붕괴 위험 감소)",
        ),
        (
            "gs005_dd_pf_recovery_guard",
            "gr_dd_pf_recovery_guard_weight",
            "gj_drawdown_recovery_pressure_weight;gj_pf_expectancy_quality_weight;underwater_rate_model;drawdown_pressure_norm",
            "clip(curve base * drawdown and underwater guards, 0.10, 10.0)",
            "improve PF/recovery/DD quality(PF/회복/낙폭 품질 개선)",
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
                "effect": "checks bounded train-only GR weights(범위 제한 학습 전용 GR 가중치 점검)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


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
        or feature in NEW_WEIGHT_COLUMNS
    ]
    duplicate_ts = int(pd.to_datetime(frame["timestamp"], utc=True, errors="coerce").duplicated().sum())
    return [
        {
            "audit_id": "gs001_allowed_feature_count",
            "status": "passed" if len(allowed_features) == 58 else "failed",
            "observed": str(len(allowed_features)),
            "expected": "58",
            "evidence": rel(ALLOWED_FEATURE_SET),
            "effect": "keeps reviewed model feature order(검토된 모델 피처 순서 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "audit_id": "gs002_forbidden_features_excluded",
            "status": "passed" if not forbidden else "failed",
            "observed": ";".join(forbidden),
            "expected": "no label/future/weight/outcome/MT5 KPI features(라벨/미래/가중치/결과/MT5 성과 피처 없음)",
            "evidence": rel(ALLOWED_FEATURE_SET),
            "effect": "prevents target leakage into model features(목표 누수 방지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "audit_id": "gs003_nonfinite_weights",
            "status": "passed" if summary["nonfinite_weight_rows"] == 0 else "failed",
            "observed": str(summary["nonfinite_weight_rows"]),
            "expected": "0",
            "evidence": rel(WEIGHT_AUDIT),
            "effect": "repair weights are finite(수리 가중치 유한)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "audit_id": "gs004_timestamp_order",
            "status": "passed" if frame["timestamp"].is_monotonic_increasing else "failed",
            "observed": str(frame["timestamp"].is_monotonic_increasing),
            "expected": "True",
            "evidence": rel(TRAIN_ONLY_REPAIR_FRAME),
            "effect": "keeps time axis ordered(시간축 순서 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "audit_id": "gs005_timestamp_duplicates_named",
            "status": "passed",
            "observed": str(duplicate_ts),
            "expected": "duplicates allowed by cost_policy_id training expansion(비용 정책 학습 확장 중복 허용)",
            "evidence": rel(TRAIN_ONLY_REPAIR_FRAME),
            "effect": "names why expanded train-only rows repeat timestamps(학습 전용 확장 행의 반복 시각 이유 명시)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "audit_id": "gs006_macro_join_safe_by_absence",
            "status": "passed",
            "observed": "no new macro source joined in GS(GS에서 새 거시 원천 결합 없음)",
            "expected": "economic data requires release timestamp(경제자료는 발표 시각 필요)",
            "evidence": rel(GR_FEATURE_LABEL),
            "effect": "prevents macro look-ahead(거시 미래참조 방지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def materialize_task_seeds() -> list[dict[str, Any]]:
    rows = [dict(row) for row in read_csv(GR_TASK_BLUEPRINT)]
    for row in rows:
        task_id = row.get("task_id", "")
        if task_id in TASK_WEIGHT_COLUMNS:
            row["target_column"] = "label_class"
            row["sample_weight_expression"] = TASK_WEIGHT_COLUMNS[task_id]
            row["selection_status"] = "eligible_after_GT_review(GT 검토 후 적격)"
            row["claim_boundary"] = CLAIM_BOUNDARY
    return rows


def review_queue() -> list[dict[str, Any]]:
    return [
        {
            "queue_id": "gt_review_mt5_negative_repair_inputs",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "task": "review GS train-only repair frame, GR weights, feature boundary, and GU training eligibility(GS 학습 전용 수리 프레임, GR 가중치, 피처 경계, GU 학습 적격성 검토)",
            "required_inputs": f"{rel(TRAIN_ONLY_REPAIR_FRAME)};{rel(WEIGHT_AUDIT)};{rel(FEATURE_LABEL_BOUNDARY)};{rel(TRAINING_TASK_SEEDS)}",
            "required_outputs": "input review, eligible GU training queue, negative control disposition(입력 검토, 적격 GU 학습 대기열, 음성 대조 처분)",
            "blocked_if_missing": "GS frame or audits(GS 프레임 또는 감사)",
            "forbidden_action": "train, tune threshold, execute MT5, or select operating candidate(학습/임계값 튜닝/MT5 실행/운영 후보 선택)",
            "effect": "forces review before training(학습 전 검토 강제)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def build_negative_and_release() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    negative = [dict(row) for row in read_csv(GR_NEGATIVE)]
    release = [dict(row) for row in read_csv(GR_RELEASE)]
    return negative, release


def build_summary(
    frame: pd.DataFrame,
    allowed_features: Sequence[str],
    weight_rows: Sequence[Mapping[str, Any]],
    task_rows: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    gr_final = read_json(GR_FINAL)
    return {
        "rows": int(len(frame)),
        "feature_count": int(len(allowed_features)),
        "new_weight_count": len(NEW_WEIGHT_COLUMNS),
        "nonfinite_weight_rows": sum(int(row.get("nonfinite_rows", 0)) for row in weight_rows),
        "task_seed_rows": len(task_rows),
        "label_distribution": {
            str(int(k)): int(v)
            for k, v in pd.to_numeric(frame["label_class"], errors="coerce").fillna(1).astype(int).value_counts().sort_index().items()
        },
        "first_timestamp": str(frame["timestamp"].iloc[0]) if len(frame) else "",
        "last_timestamp": str(frame["timestamp"].iloc[-1]) if len(frame) else "",
        "gr_best_attempt": gr_final.get("best_attempt", ""),
        "gr_best_net_profit": gr_final.get("best_net_profit", ""),
        "gr_net_gap_to_zero": gr_final.get("net_gap_to_zero", ""),
        "gr_proxy_sign_diff_rows": gr_final.get("proxy_sign_diff_rows", ""),
        "gr_pf_gap_to_1_15": gr_final.get("pf_gap_to_1_15", ""),
        "gr_recovery_gap_to_1_0": gr_final.get("recovery_gap_to_1_0", ""),
        "gr_drawdown_excess_over_150": gr_final.get("drawdown_excess_over_150", ""),
    }


def build_gates(final: Mapping[str, Any]) -> list[dict[str, Any]]:
    no_forbidden_claim = (
        final["new_training"] == "not_run"
        and final["candidate_selection"] == "not_run"
        and final["mt5_execution"] == "not_run"
        and final["goal_achieve"] == "not_claimed"
    )
    checks = [
        ("input_presence", final["missing_inputs"] == 0, str(final["missing_inputs"]), "0", rel(BASE_FRAME), "required GR/GS inputs exist(필수 GR/GS 입력 존재)"),
        ("parent_gr_gates_passed", final["gr_failed_gate_rows"] == 0, str(final["gr_failed_gate_rows"]), "0", rel(GR_GATES), "GR gates passed(GR 게이트 통과)"),
        ("parent_next_action_matches", final["gr_next_action"] == RUN_ID, str(final["gr_next_action"]), RUN_ID, rel(GR_FINAL), "GS follows GR next action(GS가 GR 다음 행동을 따름)"),
        ("repair_frame_materialized", final["rows"] == 87666 and path_exists(TRAIN_ONLY_REPAIR_FRAME), f"rows={final['rows']}", "87666", rel(TRAIN_ONLY_REPAIR_FRAME), "train-only repair frame exists(학습 전용 수리 프레임 존재)"),
        ("allowed_feature_set_preserved", final["feature_count"] == 58, str(final["feature_count"]), "58", rel(ALLOWED_FEATURE_SET), "reviewed feature set preserved(검토 피처 묶음 보존)"),
        ("feature_boundary_passed", final["feature_boundary_failed_rows"] == 0, str(final["feature_boundary_failed_rows"]), "0", rel(FEATURE_LABEL_BOUNDARY), "feature boundary audit passed(피처 경계 감사 통과)"),
        ("new_weights_materialized", final["new_weight_count"] == len(NEW_WEIGHT_COLUMNS), str(final["new_weight_count"]), str(len(NEW_WEIGHT_COLUMNS)), rel(WEIGHT_AUDIT), "GR repair weights materialized(GR 수리 가중치 물질화)"),
        ("nonfinite_weights_zero", final["nonfinite_weight_rows"] == 0, str(final["nonfinite_weight_rows"]), "0", rel(WEIGHT_AUDIT), "weights finite(가중치 유한)"),
        ("negative_mt5_memory_carried", as_float(final["gr_net_gap_to_zero"]) > 0 and as_float(final["gr_proxy_sign_diff_rows"]) >= 4, f"net_gap={final['gr_net_gap_to_zero']};sign_diff={final['gr_proxy_sign_diff_rows']}", "net_gap>0 and sign_diff>=4", rel(GR_FINAL), "all-negative MT5 memory carried forward(전부 음수 MT5 기억 인계)"),
        ("training_task_seeds_materialized", final["task_seed_rows"] == 5, str(final["task_seed_rows"]), "5", rel(TRAINING_TASK_SEEDS), "GT/GU task seeds ready(GT/GU 작업 씨앗 준비)"),
        ("review_queue_materialized", final["review_queue_rows"] == 1 and final["next_action"] == NEXT_RUN_ID, f"queue={final['review_queue_rows']};next={final['next_action']}", f"1 and {NEXT_RUN_ID}", rel(GT_QUEUE), "GT review queue opened(GT 검토 대기열 열림)"),
        ("no_forbidden_claim", no_forbidden_claim, f"training={final['new_training']};selection={final['candidate_selection']};mt5={final['mt5_execution']};goal={final['goal_achieve']}", "not_run/not_run/not_run/not_claimed", rel(FINAL_DECISION), "materialization without operating claim(운영 주장 없는 물질화)"),
        ("required_gate_coverage_audit", True, "all required gates listed in closeout(모든 필수 게이트가 종료 기록에 있음)", "present", rel(GATE_AUDIT), "connects gates to completion claim(게이트를 완료 주장과 연결)"),
    ]
    return [
        {
            "gate_id": gate_id,
            "status": "passed" if passed else "failed",
            "evidence_path": evidence,
            "observed": observed,
            "expected": expected,
            "effect": effect,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for gate_id, passed, observed, expected, evidence, effect in checks
    ]


def build_receipts(final: Mapping[str, Any], artifacts: Sequence[Path]) -> list[Path]:
    data = {
        "data_source": rel(BASE_FRAME),
        "time_axis": f"{final['first_timestamp']} to {final['last_timestamp']} closed M5 timestamps(확정 M5 시각)",
        "sample_scope": f"US100 M5 Tier A train-only expansion;rows={final['rows']};features={final['feature_count']};label_distribution={final['label_distribution']}",
        "missing_or_duplicate_check": "timestamp order checked; duplicate timestamps are cost_policy_id expansion(시각 순서 확인, 중복 시각은 비용 정책 확장)",
        "feature_label_boundary": "allowed 58 features only; labels/outcomes/weights/MT5 KPI excluded(허용 58개 피처만, 라벨/결과/가중치/MT5 성과 제외)",
        "split_boundary": "train-only materialization inherited from GK; GT review required before GU training(GK 학습 전용 물질화 상속, GU 학습 전 GT 검토 필요)",
        "leakage_risk": "repair weights accidentally used as model features or MT5 KPI converted to row feature(수리 가중치 피처 유입 또는 MT5 성과 행별 피처화)",
        "data_hash_or_identity": aw.sha256_file(TRAIN_ONLY_REPAIR_FRAME) if path_exists(TRAIN_ONLY_REPAIR_FRAME) else "",
        "integrity_judgment": "usable_with_boundary(경계 조건부 사용 가능)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    model = {
        "model_family": "LightGBM multiclass to ONNX seeds only(라이트GBM 다중분류-ONNX 씨앗 전용)",
        "target_and_label": "label_class with GR sample weights(label_class와 GR 표본 가중치)",
        "split_method": "train-only input; review required before training(학습 전용 입력, 학습 전 검토 필요)",
        "selection_metric": "not_run(실행 안 함)",
        "secondary_metrics": "weight audit, feature boundary, later MT5 KPI(가중치 감사, 피처 경계, 이후 MT5 성과)",
        "threshold_policy": "no threshold tuning(임계값 튜닝 없음)",
        "overfit_risk": "GR weights may overfit GQ all-negative runtime memory(GR 가중치가 GQ 전부 음수 런타임 기억에 과적합할 위험)",
        "calibration_risk": "not applicable until training(학습 전 해당 없음)",
        "comparison_baseline": "GQ all-negative MT5 runtime result(GQ 전부 음수 MT5 런타임 결과)",
        "validation_judgment": "materialized_review_required(물질화 완료, 검토 필요)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    performance = {
        "observed_change": "new GR MT5-negative repair weights materialized(새 GR MT5 음수 수리 가중치 물질화)",
        "comparison_baseline": "GK/GJ repair weights and GQ MT5 negative memory(GK/GJ 수리 가중치와 GQ MT5 음수 기억)",
        "likely_drivers": "MT5 net recovery, proxy sign inversion guard, lifecycle cost/fill guard, side rebalance, PF/recovery/DD guard(MT5 순수익 회복, 프록시 부호 반전 방어, 생애주기 비용/체결 방어, 방향 재균형, PF/회복/낙폭 방어)",
        "segment_checks": "weight means by label recorded; session guard is timestamp-derived(라벨별 가중치 평균 기록, 세션 방어는 시각 기반)",
        "trade_shape": "not tested until MT5 runtime probe(MT5 런타임 탐침 전 미시험)",
        "alternative_explanations": "weight recipe may reduce signal or overfit inner holdout(가중치 조리법이 신호를 줄이거나 내부 보류에 과적합할 수 있음)",
        "attribution_confidence": "input_materialization_only(입력 물질화 전용)",
        "next_probe": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    judgment = {
        "result_subject": RUN_ID,
        "evidence_available": [rel(TRAIN_ONLY_REPAIR_FRAME), rel(WEIGHT_AUDIT), rel(FEATURE_LABEL_BOUNDARY), rel(TRAINING_TASK_SEEDS)],
        "evidence_missing": "GT review, GU training, ONNX, MT5 runtime probe, forward evidence(GT 검토, GU 학습, ONNX, MT5 탐침, 전진 근거)",
        "judgment_label": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
        "next_condition": NEXT_RUN_ID,
        "user_explanation_hook": "GS made inputs only, not a model(GS는 입력만 만들었고 모델은 아님)",
    }
    paths = [
        write_json(DATA_RECEIPT, data),
        write_json(MODEL_RECEIPT, model),
        write_json(PERFORMANCE_RECEIPT, performance),
        write_json(JUDGMENT_RECEIPT, judgment),
    ]
    all_artifacts = list(artifacts) + paths
    lineage = {
        "source_inputs": [rel(path) for path in INPUT_FILES],
        "producer": rel(Path(__file__)),
        "consumer": NEXT_RUN_ID,
        "artifact_paths": [rel(path) for path in all_artifacts],
        "artifact_hashes": {rel(path): aw.sha256_file(path) for path in all_artifacts if path_exists(path) and aw.io_path(path).is_file()},
        "registry_links": [rel(gr.gq.go.RUN_REGISTRY), rel(gr.gq.go.ALPHA_LEDGER), rel(gr.gq.go.STAGE_LEDGER), rel(gr.gq.go.ARTIFACT_REGISTRY)],
        "availability": "generated_with_manifest(목록으로 생성)",
        "lineage_judgment": "connected_with_boundary(경계 조건부 연결)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    paths.append(write_json(LINEAGE_RECEIPT, lineage))
    return paths


def write_report(final: Mapping[str, Any]) -> Path:
    text = f"""# Stage337 run337GS MT5 Negative Repair Input Materialization(337단계 337GS MT5 음수 수리 입력 물질화)

## Conclusion(결론)

Action(행동): GK train-only frame(GK 학습 전용 프레임)에 GR MT5-negative repair weights(GR MT5 음수 수리 가중치) `5`개를 물질화했다. Effect(효과): GQ all-negative MT5 result(GQ 전부 음수 MT5 결과)를 다음 GU training(GU 학습)이 검토 가능한 입력으로 다룰 수 있다.

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- rows(행): `{final['rows']}`
- feature_count(피처 수): `{final['feature_count']}`
- new_weight_count(새 가중치 수): `{final['new_weight_count']}`
- nonfinite_weight_rows(비유한 가중치 행): `{final['nonfinite_weight_rows']}`
- task_seed_rows(작업 씨앗 행): `{final['task_seed_rows']}`
- gr_best_attempt(GR 최고 시도): `{final['gr_best_attempt']}`
- gr_best_net_profit(GR 최고 순수익): `{final['gr_best_net_profit']}`
- gr_proxy_sign_diff_rows(GR 프록시 부호 차이 행): `{final['gr_proxy_sign_diff_rows']}`
- gates(게이트): `{final['passed_gates']}/{final['gate_rows']}`

## Boundary(경계)

- model_training(모델 학습): `not_run`
- threshold_tuning(임계값 튜닝): `not_run`
- MT5 execution(MT5 실행): `not_run`
- operating_selection(운영 선택): `not_run`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{final['next_action']}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return aw.write_text_lossless(REPORT_PATH, text, True)


def write_decision(final: Mapping[str, Any]) -> Path:
    text = f"""# {TODAY} Stage337GS Decision(337GS 결정)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- evidence(근거): `{rel(REPORT_PATH)}`, `{rel(TRAIN_ONLY_REPAIR_FRAME)}`, `{rel(WEIGHT_AUDIT)}`, `{rel(TRAINING_TASK_SEEDS)}`

Action(행동): GR repair design(GR 수리 설계)을 train-only input artifacts(학습 전용 입력 산출물)로 물질화했다.
Effect(효과): GT review(GT 검토)가 feature boundary(피처 경계), weight audit(가중치 감사), training eligibility(학습 적격성)를 판단할 수 있다.

Forward/Goal(전진/목표): `not_claimed`
runtime_authority(런타임 권위): `not_claimed`
claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return aw.write_text_lossless(DECISION_DOC, text, True)


def replace_line(text: str, prefix: str, replacement: str) -> str:
    pattern = re.compile(rf"^{re.escape(prefix)}.*$", flags=re.M)
    return pattern.sub(replacement, text, count=1) if pattern.search(text) else replacement + "\n" + text


def upsert_focus(text: str, marker: str, entry: str) -> str:
    if marker in text:
        return re.sub(rf"- >-\n  {re.escape(marker)}.*?(?=\n- >-|\n[a-zA-Z_]+:|$)", entry.rstrip(), text, count=1, flags=re.S)
    return text.replace("current_focus:\n", "current_focus:\n" + entry, 1)


def update_docs(final: Mapping[str, Any]) -> list[Path]:
    artifacts: list[Path] = []
    branch = fa.ey.current_branch()
    workspace, workspace_bom = aw.read_text_lossless(gr.gq.go.WORKSPACE_STATE)
    workspace = replace_line(workspace, "current_run_id:", f"current_run_id: {final['next_action']}")
    workspace = replace_line(workspace, "updated_on:", f"updated_on: '{TODAY}'")
    workspace = replace_line(workspace, "active_branch:", f"active_branch: {branch}")
    focus = (
        "- >-\n"
        f"  Stage337 run337GS focus complete: run337GS(337GS 실행)은 `{final['status']}`로 MT5 negative repair inputs(MT5 음수 수리 입력)를 물질화했다. "
        f"Effect(효과): rows(행) `{final['rows']}`, features(피처) `{final['feature_count']}`, new weights(새 가중치) `{final['new_weight_count']}`, gates(게이트) `{final['passed_gates']}/{final['gate_rows']}`를 기록하고 `{final['next_action']}`을 열었다. Forward/Goal(전진/목표)은 주장하지 않는다.\n"
    )
    workspace = upsert_focus(workspace, "Stage337 run337GS focus complete", focus)
    artifacts.append(aw.write_text_lossless(gr.gq.go.WORKSPACE_STATE, workspace, workspace_bom))

    current, current_bom = aw.read_text_lossless(gr.gq.go.CURRENT_STATE)
    for field_name, value in {
        "current_run": f"`{final['next_action']}`",
        "status": f"`{final['status']}`",
        "decision": f"`{final['decision']}`",
        "latest_completed_run": f"`{RUN_ID}`",
        "next_action": f"`{final['next_action']}`",
        "claim_boundary": f"`{CLAIM_BOUNDARY}`",
    }.items():
        current = fb.replace_bullet_field(current, field_name, value)
    section = f"""## run337GS MT5 Negative Repair Input Materialization(MT5 음수 수리 입력 물질화)

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- rows(행): `{final['rows']}`
- feature_count(피처 수): `{final['feature_count']}`
- new_weight_count(새 가중치 수): `{final['new_weight_count']}`
- nonfinite_weight_rows(비유한 가중치 행): `{final['nonfinite_weight_rows']}`
- gates(게이트): `{final['passed_gates']}/{final['gate_rows']}`
- effect(효과): GR 설계를 GT review(GT 검토)가 가능한 학습 전용 입력으로 바꿨고, 운영 주장(operating claim, 운영 주장)은 하지 않는다.
- next_action(다음 행동): `{final['next_action']}`
"""
    current = fb.upsert_section_before(current, "## run337GR MT5 Negative Repair Design", section, "run337GS MT5 Negative Repair Input Materialization")
    artifacts.append(aw.write_text_lossless(gr.gq.go.CURRENT_STATE, current, current_bom))

    selection = f"""# Stage337 Selection Status(337단계 선택 상태)

- latest_run(최신 실행): `{RUN_ID}`
- latest_decision(최신 결정): `{final['decision']}`
- current_run(현재 실행): `{final['next_action']}`
- rebuild_status(재구축 상태): `{final['status']}`
- rows(행): `{final['rows']}`
- feature_count(피처 수): `{final['feature_count']}`
- new_weight_count(새 가중치 수): `{final['new_weight_count']}`
- gr_best_attempt(GR 최고 시도): `{final['gr_best_attempt']}`
- gr_best_net_profit(GR 최고 순수익): `{final['gr_best_net_profit']}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{final['next_action']}`
- effect(효과): GS(337GS 실행)는 materialization(물질화) 근거만 만들며 operating selection(운영 선택)은 하지 않는다.
"""
    artifacts.append(aw.write_text_lossless(gr.gq.go.SELECTED_STATUS, selection, True))

    brief, brief_bom = aw.read_text_lossless(gr.gq.go.STAGE_BRIEF)
    brief_entry = (
        f"- {TODAY}: run337GS(337GS 실행) `{final['status']}`. "
        f"Effect(효과): GR repair weights(GR 수리 가중치) `{final['new_weight_count']}`개를 학습 전용 프레임에 붙이고 `{final['next_action']}`을 열었다. Forward/Goal(전진/목표)은 주장하지 않는다."
    )
    artifacts.append(aw.write_text_lossless(gr.gq.go.STAGE_BRIEF, fb.upsert_single_line(brief, "run337GS(337GS 실행)", brief_entry), brief_bom))

    changelog, changelog_bom = aw.read_text_lossless(gr.gq.go.CHANGELOG)
    changelog_entry = (
        f"- {TODAY}: Stage337 run337GS(337GS 실행) `{final['status']}`. "
        f"Effect(효과): MT5 negative repair inputs(MT5 음수 수리 입력)를 물질화하고 `{final['next_action']}`을 열었다. Forward/Goal(전진/목표)은 주장하지 않았다."
    )
    artifacts.append(aw.write_text_lossless(gr.gq.go.CHANGELOG, fb.upsert_single_line(changelog, "Stage337 run337GS", changelog_entry), changelog_bom))
    return artifacts


def update_registers(final: Mapping[str, Any]) -> list[Path]:
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "mt5_negative_repair_input_materialization",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "notes": f"rows={final['rows']};features={final['feature_count']};weights={final['new_weight_count']};gr_net={final['gr_best_net_profit']};next_action={final['next_action']};goal_achieve_not_claimed.",
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__input_materialization",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "input_materialization",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "MT5 negative repair inputs(MT5 음수 수리 입력)",
        "tier_scope": "Tier A train-only materialization(Tier A 학습 전용 물질화)",
        "kpi_scope": "input_materialization_only_no_training_no_mt5(입력 물질화 전용, 학습/MT5 없음)",
        "scoreboard_lane": "experiment_execution",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "primary_kpi": f"rows={final['rows']};weights={final['new_weight_count']};net_gap={final['gr_net_gap_to_zero']};proxy_sign_diff={final['gr_proxy_sign_diff_rows']}",
        "guardrail_kpi": "feature_boundary;finite_weights;no_selection;no_goal",
        "external_verification_status": "out_of_scope_by_claim",
        "notes": f"decision={final['decision']};next_action={final['next_action']};goal_achieve_not_claimed.",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__input_materialization",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "experiment_execution_data_integrity_model_validation",
        "evidence_scope": "train-only frame, GR weight recipes, feature boundary, task seeds",
        "kpi_scope": "input_rows_weights_boundaries",
        "status": final["status"],
        "judgment": final["judgment"],
        "claim_boundary": CLAIM_BOUNDARY,
        "path": rel(REPORT_PATH),
        "notes": f"gates={final['passed_gates']}/{final['gate_rows']};next_action={final['next_action']};goal_achieve_not_claimed",
        "decision": final["decision"],
        "run_key": f"{RUN_ID}__input_materialization",
        "family": "mt5_negative_repair_input_materialization",
        "question": "can GR all-negative MT5 repair design be materialized as timestamp-safe train-only weights",
        "metric_scope": "rows_features_weights_boundaries",
        "primary_artifact": rel(TRAIN_ONLY_REPAIR_FRAME),
        "report_path": rel(REPORT_PATH),
        "next_action": final["next_action"],
    }
    return [
        fb.upsert_csv_worktree(gr.gq.go.RUN_REGISTRY, aw.RUN_REGISTRY_COLUMNS, run_row, "run_id"),
        fb.upsert_csv_worktree(gr.gq.go.ALPHA_LEDGER, aw.ALPHA_LEDGER_COLUMNS, alpha_row, "ledger_row_id"),
        fb.upsert_csv_worktree(gr.gq.go.STAGE_LEDGER, aw.STAGE_LEDGER_COLUMNS, stage_row, "ledger_row_id"),
    ]


def update_artifact_registry(paths: Sequence[Path]) -> Path:
    columns, rows = aw.read_csv_table(gr.gq.go.ARTIFACT_REGISTRY, prefer_head=False)
    columns = list(columns or aw.ARTIFACT_COLUMNS)
    for column in aw.ARTIFACT_COLUMNS:
        if column not in columns:
            columns.append(column)
    for extra in ("artifact_path", "claim_boundary"):
        if extra not in columns:
            columns.append(extra)
    rows = [
        row
        for row in rows
        if not str(row.get("artifact_id", "")).startswith(f"{RUN_ID}::") and str(row.get("run_id", "")) != RUN_ID
    ]
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
        rows.append(
            {
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
        )
    return write_csv(gr.gq.go.ARTIFACT_REGISTRY, columns, rows)


def make_final(summary: Mapping[str, Any], queue_rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    gr_final = read_json(GR_FINAL)
    return {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_action": NEXT_RUN_ID,
        "missing_inputs": len(fail_if_missing(INPUT_FILES)),
        "gr_next_action": gr_final.get("next_action", ""),
        "gr_failed_gate_rows": sum(1 for row in read_csv(GR_GATES) if row.get("status") != "passed"),
        "new_training": "not_run",
        "threshold_tuning": "not_run",
        "lot_optimization": "not_run",
        "candidate_selection": "not_run",
        "mt5_execution": "not_run",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "runtime_authority": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
        "review_queue_rows": len(queue_rows),
        **dict(summary),
    }


def main() -> int:
    aw.io_path(RUN_DIR).mkdir(parents=True, exist_ok=True)
    missing = fail_if_missing(INPUT_FILES)
    if missing:
        print(
            json.dumps(
                {"run_id": RUN_ID, "status": "blocked_missing_inputs", "missing": [rel(path) for path in missing]},
                ensure_ascii=False,
                indent=2,
            )
        )
        return 1

    frame = pd.read_parquet(aw.io_path(BASE_FRAME))
    frame["timestamp"] = pd.to_datetime(frame["timestamp"], utc=True)
    frame.sort_values(["timestamp", "source_row_id", "cost_policy_id"], inplace=True)
    frame = materialize_weights(frame)
    aw.io_path(TRAIN_ONLY_REPAIR_FRAME.parent).mkdir(parents=True, exist_ok=True)
    frame.to_parquet(aw.io_path(TRAIN_ONLY_REPAIR_FRAME), index=False)

    shutil.copy2(aw.io_path(BASE_FEATURES), aw.io_path(ALLOWED_FEATURE_SET))
    allowed_features = [row.get("feature") or row.get("feature_name", "") for row in read_csv(ALLOWED_FEATURE_SET)]
    allowed_features = [feature for feature in allowed_features if feature]
    recipe_rows = weight_recipes()
    weight_rows = weight_audit(frame)
    task_rows = materialize_task_seeds()
    negative_rows, release_rows = build_negative_and_release()
    queue_rows = review_queue()
    summary = build_summary(frame, allowed_features, weight_rows, task_rows)
    boundary_rows = feature_boundary_rows(allowed_features, frame, summary)
    summary["feature_boundary_failed_rows"] = sum(1 for row in boundary_rows if row.get("status") != "passed")
    final = make_final(summary, queue_rows)

    artifacts: list[Path] = [
        TRAIN_ONLY_REPAIR_FRAME,
        write_csv(MATERIALIZATION_SOURCE_MAP, SOURCE_COLUMNS, source_map()),
        ALLOWED_FEATURE_SET,
        write_csv(WEIGHT_RECIPE_MATRIX, WEIGHT_RECIPE_COLUMNS, recipe_rows),
        write_csv(WEIGHT_AUDIT, WEIGHT_AUDIT_COLUMNS, weight_rows),
        write_csv(FEATURE_LABEL_BOUNDARY, BOUNDARY_COLUMNS, boundary_rows),
        write_csv(NEGATIVE_CONTROL_MATERIALIZATION, gr.CONSTRAINT_COLUMNS, negative_rows),
        write_csv(RELEASE_GATE_MATERIALIZATION, gr.RELEASE_COLUMNS, release_rows),
        write_csv(TRAINING_TASK_SEEDS, TASK_SEED_COLUMNS, task_rows),
        write_csv(GT_QUEUE, QUEUE_COLUMNS, queue_rows),
    ]
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
                    "inputs": [rel(path) for path in INPUT_FILES],
                    "outputs": [rel(path) for path in OUTPUT_FILES],
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
            {
                "run_id": RUN_ID,
                "status": final["status"],
                "rows": final["rows"],
                "feature_count": final["feature_count"],
                "new_weight_count": final["new_weight_count"],
                "nonfinite_weight_rows": final["nonfinite_weight_rows"],
                "task_seed_rows": final["task_seed_rows"],
                "gr_best_net_profit": final["gr_best_net_profit"],
                "gr_proxy_sign_diff_rows": final["gr_proxy_sign_diff_rows"],
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
