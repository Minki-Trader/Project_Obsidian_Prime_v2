from __future__ import annotations

import csv
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from stage_pipelines.stage337 import (  # noqa: E402
    design_runtime_positive_low_pf_drawdown_side_balance_repair_without_db as ie,
)


aw = ie.aw

TODAY = "2026-06-01"
STAGE_ID = ie.STAGE_ID
STAGE_DIR = ie.STAGE_DIR
RUN_NUMBER = "run337IF"
RUN_ID = "run337IF_materialize_runtime_positive_low_pf_drawdown_side_balance_repair_inputs_without_db_v1"
PARENT_RUN_ID = ie.RUN_ID
NEXT_RUN_ID = "run337IG_review_runtime_positive_low_pf_drawdown_side_balance_repair_inputs_without_db_v1"
STATUS = "completed_stage337IF_runtime_positive_low_pf_drawdown_side_balance_repair_inputs_materialized_no_training_no_selection"
JUDGMENT = "timestamp_safe_runtime_positive_repair_inputs_materialized_review_required"
DECISION = "stage337IF_open_run337IG_runtime_positive_low_pf_drawdown_side_balance_repair_input_review"
CLAIM_BOUNDARY = (
    "research_development_input_materialization_only_no_model_training_no_threshold_tuning_no_lot_optimization_"
    "no_candidate_selection_no_mt5_execution_no_forward_passed_no_forward_failed_no_live_readiness_"
    "no_operating_promotion_no_runtime_authority_no_goal_achieve"
)

RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEW_DIR / "run337IF_repair_inputs.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage337IF_runtime_positive_repair_inputs.md"

WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs" / "context" / "current_working_state.md"
SELECTION_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
STAGE_BRIEF = STAGE_DIR / "README.md"
CHANGELOG = ROOT / "CHANGELOG.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
PROJECT_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
STAGE_LEDGER = STAGE_DIR / "03_reviews" / "stage_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"

IE_FINAL = ie.FINAL_DECISION
IE_GATES = ie.GATE_AUDIT
IE_QUEUE = ie.IF_QUEUE
IE_DESIGN = ie.DESIGN_MATRIX
IE_ATTRIBUTION = ie.PERFORMANCE_ATTRIBUTION
IE_EXPERIMENT = ie.EXPERIMENT_CONTRACT
IE_FEATURE_CONTRACT = ie.FEATURE_LABEL_TRADE_CONTRACT
IE_TIER_CONTRACT = ie.TIER_PAIR_CONTRACT
IE_PARITY_GUARD = ie.RUNTIME_PARITY_GUARD
IE_COST_CONTRACT = ie.COST_STRESS_CONTRACT
ID_KPI = ie.ID_KPI
ID_DIFF = ie.ID_DIFF
HX_FRAME = STAGE_DIR / "02_runs" / "run337HX" / "hx_input_frame.parquet"
HX_ALLOWED_FEATURES = STAGE_DIR / "02_runs" / "run337HX" / "hx_allowed_model_feature_set.csv"
HZ_FEATURE_SCHEMA = STAGE_DIR / "02_runs" / "run337HZ" / "hz_allowed_feature_schema.json"
HZ_MODEL_MANIFEST = STAGE_DIR / "02_runs" / "run337HZ" / "trained_model_manifest.csv"
IA_POSITIVE_MATRIX = STAGE_DIR / "02_runs" / "run337IA" / "ia_positive_proxy_candidate_matrix.csv"

IF_INPUT_FRAME = RUN_DIR / "if_runtime_positive_repair_input_frame.parquet"
IF_SOURCE_MAP = RUN_DIR / "if_materialization_source_map.csv"
IF_ALLOWED_FEATURES = RUN_DIR / "if_allowed_model_feature_set.csv"
IF_WEIGHT_RECIPE = RUN_DIR / "if_weight_recipe_matrix.csv"
IF_WEIGHT_AUDIT = RUN_DIR / "if_weight_audit.csv"
IF_FEATURE_BOUNDARY = RUN_DIR / "if_feature_label_boundary_audit.csv"
IF_TIER_RECORDS = RUN_DIR / "if_tier_record_plan.csv"
IF_RUNTIME_PARITY_PLAN = RUN_DIR / "if_runtime_parity_guard_plan.csv"
IF_COST_STRESS_PLAN = RUN_DIR / "if_cost_stress_plan.csv"
IF_TASK_SEEDS = RUN_DIR / "run337IG_training_task_seed_matrix.csv"
IG_QUEUE = RUN_DIR / "run337IG_review_queue.csv"
RUN_EVIDENCE_RECEIPT = RUN_DIR / "run_evidence_receipt.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (
    IE_FINAL,
    IE_GATES,
    IE_QUEUE,
    IE_DESIGN,
    IE_ATTRIBUTION,
    IE_EXPERIMENT,
    IE_FEATURE_CONTRACT,
    IE_TIER_CONTRACT,
    IE_PARITY_GUARD,
    IE_COST_CONTRACT,
    ID_KPI,
    ID_DIFF,
    HX_FRAME,
    HX_ALLOWED_FEATURES,
    HZ_FEATURE_SCHEMA,
    HZ_MODEL_MANIFEST,
    IA_POSITIVE_MATRIX,
)
OUTPUT_FILES = (
    IF_INPUT_FRAME,
    IF_SOURCE_MAP,
    IF_ALLOWED_FEATURES,
    IF_WEIGHT_RECIPE,
    IF_WEIGHT_AUDIT,
    IF_FEATURE_BOUNDARY,
    IF_TIER_RECORDS,
    IF_RUNTIME_PARITY_PLAN,
    IF_COST_STRESS_PLAN,
    IF_TASK_SEEDS,
    IG_QUEUE,
    RUN_EVIDENCE_RECEIPT,
    DATA_RECEIPT,
    MODEL_RECEIPT,
    PERFORMANCE_RECEIPT,
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
    STAGE_BRIEF,
    CHANGELOG,
    RUN_REGISTRY,
    PROJECT_LEDGER,
    STAGE_LEDGER,
    ARTIFACT_REGISTRY,
    Path(__file__),
)

NEW_WEIGHT_COLUMNS = (
    "if_side_net_stability_weight",
    "if_drawdown_cluster_control_weight",
    "if_pf_recovery_trade_shape_weight",
    "if_cost_stress_survival_weight",
    "if_runtime_positive_repair_blend_weight",
)
FORBIDDEN_FEATURE_TOKENS = (
    "label",
    "future",
    "target",
    "net_profit",
    "profit_factor",
    "recovery",
    "drawdown",
    "expectancy",
    "proxy",
    "mt5",
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
AUDIT_COLUMNS = (
    "audit_id",
    "status",
    "observed",
    "expected",
    "evidence",
    "effect",
    "claim_boundary",
)
TASK_COLUMNS = (
    "task_id",
    "repair_family",
    "target_column",
    "valid_column",
    "sample_weight_column",
    "model_family",
    "model_config_id",
    "base_clue_model_id",
    "input_frame",
    "allowed_features",
    "required_guard",
    "expected_effect",
    "forbidden_use",
    "claim_boundary",
)
QUEUE_COLUMNS = (
    "queue_id",
    "source_run_id",
    "next_run_id",
    "task",
    "required_inputs",
    "expected_outputs",
    "blocked_if_missing",
    "effect",
    "claim_boundary",
)
GATE_COLUMNS = (
    "gate_id",
    "status",
    "observed",
    "expected",
    "evidence_path",
    "effect",
    "claim_boundary",
)


def now_utc() -> str:
    return datetime.now(tz=UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    return aw.rel(path)


def io(path: Path) -> Path:
    return aw.io_path(path)


def exists(path: Path) -> bool:
    return io(path).exists()


def ensure_parent(path: Path) -> None:
    io(path.parent).mkdir(parents=True, exist_ok=True)


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(io(path).read_text(encoding="utf-8-sig"))


def read_csv_frame(path: Path) -> pd.DataFrame:
    return pd.read_csv(io(path))


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> Path:
    ensure_parent(path)
    with io(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: row.get(column, "") for column in columns})
    return path


def write_frame_csv(path: Path, frame: pd.DataFrame) -> Path:
    ensure_parent(path)
    frame.to_csv(io(path), index=False, encoding="utf-8-sig", lineterminator="\n")
    return path


def write_json(path: Path, payload: Mapping[str, Any] | Sequence[Any]) -> Path:
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
        if pd.isna(value):
            return default
        number = float(value)
    except (TypeError, ValueError):
        return default
    return number if np.isfinite(number) else default


def numeric(frame: pd.DataFrame, column: str, default: float = 0.0) -> pd.Series:
    if column not in frame.columns:
        return pd.Series(default, index=frame.index, dtype="float64")
    return (
        pd.to_numeric(frame[column], errors="coerce")
        .replace([np.inf, -np.inf], np.nan)
        .fillna(default)
        .astype("float64")
    )


def norm01(series: pd.Series) -> pd.Series:
    clean = pd.to_numeric(series, errors="coerce").replace([np.inf, -np.inf], np.nan)
    low = clean.quantile(0.05)
    high = clean.quantile(0.95)
    if not np.isfinite(low) or not np.isfinite(high) or high <= low:
        return pd.Series(0.0, index=series.index)
    return ((clean - low) / (high - low)).clip(0.0, 1.0).fillna(0.0)


def clip_weight(values: pd.Series | np.ndarray, lower: float = 0.10, upper: float = 12.0) -> pd.Series:
    return pd.Series(values).replace([np.inf, -np.inf], np.nan).fillna(1.0).clip(lower, upper)


def missing_inputs(paths: Sequence[Path]) -> list[str]:
    return [rel(path) for path in paths if not exists(path)]


def materialize_frame(base: pd.DataFrame) -> pd.DataFrame:
    frame = base.copy()
    if "timestamp" in frame.columns:
        frame["timestamp"] = pd.to_datetime(frame["timestamp"], utc=True)
    sort_cols = [column for column in ("timestamp", "source_row_id", "cost_policy_id") if column in frame.columns]
    if sort_cols:
        frame = frame.sort_values(sort_cols).reset_index(drop=True)

    label = numeric(frame, "hx_label_class_fwd18", default=1.0).astype(int)
    active = label.isin([0, 2])
    long_mask = label.eq(2)
    short_mask = label.eq(0)
    flat_mask = label.eq(1)

    base_weight = numeric(frame, "fl_runtime_blend_repair_weight", default=1.0).clip(0.20, 8.0)
    side_quality = numeric(frame, "side_quality_weight", default=1.0).clip(0.10, 5.0)
    side_gap = numeric(frame, "side_quality_gap_norm", default=0.0).clip(0.0, 1.0)
    drawdown = numeric(frame, "drawdown_pressure_norm", default=0.0).clip(0.0, 1.0)
    underwater = numeric(frame, "underwater_rate_model", default=0.0).clip(0.0, 1.0)
    low_margin = numeric(frame, "low_margin_rate_model", default=0.0).clip(0.0, 1.0)
    cost_survival = numeric(frame, "cost_survival_weight", default=1.0).clip(0.10, 5.0)
    abs_future = norm01(numeric(frame, "hx_future_log_return_18", default=0.0).abs())
    volatility = norm01(numeric(frame, "historical_vol_20", default=0.0))
    trend = norm01(numeric(frame, "adx_14", default=0.0))
    open_close = (
        numeric(frame, "is_first_30m_after_open", default=0.0)
        + numeric(frame, "is_last_30m_before_cash_close", default=0.0)
    ).clip(0.0, 1.0)
    risk_pressure = (0.45 * drawdown + 0.35 * underwater + 0.20 * low_margin).clip(0.0, 1.0)

    side_factor = pd.Series(1.0, index=frame.index, dtype="float64")
    side_factor.loc[long_mask] = 1.28 + 0.22 * (1.0 - risk_pressure.loc[long_mask])
    side_factor.loc[short_mask] = 0.88 + 0.18 * side_quality.loc[short_mask].clip(0.0, 1.0)
    side_factor.loc[flat_mask] = 0.92 + 0.16 * risk_pressure.loc[flat_mask]
    frame["if_side_net_stability_weight"] = clip_weight(base_weight * side_factor * (1.0 + 0.20 * side_gap))

    drawdown_factor = (1.30 - 0.70 * risk_pressure + 0.20 * open_close).clip(0.35, 1.45)
    drawdown_factor = drawdown_factor.where(active, 0.95 + 0.20 * risk_pressure)
    frame["if_drawdown_cluster_control_weight"] = clip_weight(base_weight * drawdown_factor)

    pf_factor = (1.0 + 0.55 * abs_future + 0.20 * trend - 0.35 * low_margin).clip(0.45, 1.60)
    pf_factor = pf_factor.where(active, 0.82 + 0.18 * (1.0 - risk_pressure))
    frame["if_pf_recovery_trade_shape_weight"] = clip_weight(base_weight * pf_factor)

    cost_factor = (cost_survival * (1.20 - 0.45 * low_margin - 0.20 * volatility)).clip(0.35, 1.40)
    frame["if_cost_stress_survival_weight"] = clip_weight(base_weight * cost_factor)

    frame["if_runtime_positive_repair_blend_weight"] = clip_weight(
        0.28 * frame["if_side_net_stability_weight"]
        + 0.26 * frame["if_drawdown_cluster_control_weight"]
        + 0.26 * frame["if_pf_recovery_trade_shape_weight"]
        + 0.20 * frame["if_cost_stress_survival_weight"]
    )
    return frame


def source_map(frame: pd.DataFrame) -> list[dict[str, Any]]:
    sources = [
        ("ie_final", IE_FINAL, "parent decision(부모 결정)", "IE가 IF를 연 사실을 확인한다."),
        ("ie_design", IE_DESIGN, "design matrix(설계 행렬)", "수리 축을 물질화 입력으로 연결한다."),
        ("ie_attribution", IE_ATTRIBUTION, "performance attribution(성과 귀속)", "약점별 수리 가중치 근거를 보존한다."),
        ("hx_frame", HX_FRAME, "base train-only frame(기반 학습 전용 프레임)", "기존 시점 안전 학습 프레임을 재사용한다."),
        ("hx_allowed_features", HX_ALLOWED_FEATURES, "allowed features(허용 피처)", "새 가중치가 모델 피처로 들어가지 않게 한다."),
        ("hz_model_manifest", HZ_MODEL_MANIFEST, "model manifest(모델 목록)", "정확 동등 ExtraTrees 단서와 보조 LGBM 단서를 추적한다."),
        ("id_kpi", ID_KPI, "runtime KPI judgment(런타임 핵심 성과 지표 판정)", "양수 순익과 약점 수치를 보존한다."),
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
            "source_id": "if_frame_rows",
            "source_path": rel(IF_INPUT_FRAME),
            "source_type": "generated frame(생성 프레임)",
            "required": True,
            "exists": True,
            "sha256": sha(IF_INPUT_FRAME) if exists(IF_INPUT_FRAME) else "",
            "effect": f"{len(frame)} rows(행) 물질화 결과를 기록한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    )
    return rows


def allowed_features_copy() -> pd.DataFrame:
    allowed = read_csv_frame(HX_ALLOWED_FEATURES).copy()
    if "feature_name" not in allowed.columns:
        allowed = allowed.rename(columns={allowed.columns[0]: "feature_name"})
    allowed["if_usage"] = "allowed_model_input_for_run337IG(337IG 허용 모델 입력)"
    allowed["claim_boundary"] = CLAIM_BOUNDARY
    return allowed


def weight_recipes() -> list[dict[str, Any]]:
    return [
        {
            "recipe_id": "if001_side_net_stability",
            "materialized_column": "if_side_net_stability_weight",
            "source_columns": "hx_label_class_fwd18;side_quality_weight;side_quality_gap_norm;fl_runtime_blend_repair_weight",
            "train_only_formula": "long label boost, short damping, flat risk guard(롱 라벨 강화, 숏 완화, 관망 위험 보호)",
            "lower_bound": "0.10",
            "upper_bound": "12.0",
            "expected_effect": "롱/숏 균형과 PF(수익 팩터)를 동시에 압박한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "recipe_id": "if002_drawdown_cluster_control",
            "materialized_column": "if_drawdown_cluster_control_weight",
            "source_columns": "drawdown_pressure_norm;underwater_rate_model;low_margin_rate_model;session flags(세션 플래그)",
            "train_only_formula": "downweight high drawdown risk and preserve flat guard(높은 낙폭 위험 완화와 관망 보호)",
            "lower_bound": "0.10",
            "upper_bound": "12.0",
            "expected_effect": "손실 군집을 줄이는 후보를 만든다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "recipe_id": "if003_pf_recovery_trade_shape",
            "materialized_column": "if_pf_recovery_trade_shape_weight",
            "source_columns": "hx_future_log_return_18;adx_14;low_margin_rate_model",
            "train_only_formula": "reward active edge and penalize low-margin churn(활성 우위 보상과 낮은 마진 회전 벌점)",
            "lower_bound": "0.10",
            "upper_bound": "12.0",
            "expected_effect": "PF(수익 팩터)와 recovery(회복)를 같이 올릴 후보를 만든다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "recipe_id": "if004_cost_stress_survival",
            "materialized_column": "if_cost_stress_survival_weight",
            "source_columns": "cost_survival_weight;low_margin_rate_model;historical_vol_20",
            "train_only_formula": "cost survival times low-margin and volatility guard(비용 생존 가중치와 낮은 마진/변동성 보호)",
            "lower_bound": "0.10",
            "upper_bound": "12.0",
            "expected_effect": "비용 압박에서 무너지는 거래를 줄인다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "recipe_id": "if005_runtime_positive_repair_blend",
            "materialized_column": "if_runtime_positive_repair_blend_weight",
            "source_columns": ";".join(NEW_WEIGHT_COLUMNS[:-1]),
            "train_only_formula": "weighted average of four repair weights(네 수리 가중치의 가중 평균)",
            "lower_bound": "0.10",
            "upper_bound": "12.0",
            "expected_effect": "양수 순익 단서를 보존하면서 복합 약점을 수리한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def weight_audit(frame: pd.DataFrame) -> list[dict[str, Any]]:
    label = numeric(frame, "hx_label_class_fwd18", default=1.0).astype(int)
    rows = []
    for column in NEW_WEIGHT_COLUMNS:
        values = numeric(frame, column, default=np.nan)
        rows.append(
            {
                "weight_column": column,
                "rows": len(values),
                "weight_min": float(values.min()),
                "weight_mean": float(values.mean()),
                "weight_max": float(values.max()),
                "nonfinite_rows": int((~np.isfinite(values.to_numpy())).sum()),
                "short_label_mean": float(values[label == 0].mean()),
                "flat_label_mean": float(values[label == 1].mean()),
                "long_label_mean": float(values[label == 2].mean()),
                "effect": "학습 전용 가중치가 유한하고 방향별로 기록된다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def feature_boundary_rows(allowed: pd.DataFrame, frame: pd.DataFrame) -> list[dict[str, Any]]:
    features = allowed["feature_name"].astype(str).tolist()
    forbidden = []
    for feature in features:
        lowered = feature.lower()
        hits = [token for token in FORBIDDEN_FEATURE_TOKENS if token in lowered]
        if lowered.startswith("if_") or lowered.endswith("_weight"):
            hits.append("generated_weight(생성 가중치)")
        if hits:
            forbidden.append(f"{feature}:{'|'.join(hits)}")
    duplicate_timestamps = 0
    if {"timestamp", "cost_policy_id"}.issubset(frame.columns):
        duplicate_timestamps = int(frame.duplicated(["timestamp", "cost_policy_id"]).sum())
    monotonic = True
    if "timestamp" in frame.columns:
        monotonic = bool(pd.to_datetime(frame["timestamp"], utc=True).is_monotonic_increasing)
    return [
        {
            "audit_id": "if001_allowed_feature_count",
            "status": "passed" if len(features) == 58 else "failed",
            "observed": len(features),
            "expected": "58",
            "evidence": rel(IF_ALLOWED_FEATURES),
            "effect": "HZ와 같은 모델 피처 순서를 유지한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "audit_id": "if002_forbidden_features_excluded",
            "status": "passed" if not forbidden else "failed",
            "observed": ";".join(forbidden),
            "expected": "no generated weights, labels, futures, proxy, MT5 KPI(생성 가중치/라벨/미래/프록시/MT5 KPI 없음)",
            "evidence": rel(IF_ALLOWED_FEATURES),
            "effect": "수리 가중치와 미래 목표가 모델 입력으로 새지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "audit_id": "if003_timestamp_order",
            "status": "passed" if monotonic else "failed",
            "observed": str(monotonic),
            "expected": "True",
            "evidence": rel(IF_INPUT_FRAME),
            "effect": "시간축 순서를 보존한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "audit_id": "if004_duplicate_timestamp_cost_policy_rows",
            "status": "passed" if duplicate_timestamps == 0 else "failed",
            "observed": duplicate_timestamps,
            "expected": "0",
            "evidence": rel(IF_INPUT_FRAME),
            "effect": "동일 비용 정책 안 중복 시점 입력을 막는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def tier_records(frame: pd.DataFrame) -> list[dict[str, Any]]:
    return [
        {
            "audit_id": "if_tier_a_separate",
            "status": "materialized",
            "observed": len(frame),
            "expected": "Tier A separate(Tier A 분리)",
            "evidence": rel(IF_INPUT_FRAME),
            "effect": "전체 문맥 표본을 학습 전용 입력으로 보존한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "audit_id": "if_tier_b_separate",
            "status": "missing_required",
            "observed": 0,
            "expected": "Tier B separate(Tier B 분리)",
            "evidence": rel(IE_TIER_CONTRACT),
            "effect": "부분 문맥 표본 공백을 숨기지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "audit_id": "if_tier_ab_combined",
            "status": "missing_required",
            "observed": 0,
            "expected": "Tier A+B combined(Tier A+B 합산)",
            "evidence": rel(IE_TIER_CONTRACT),
            "effect": "합산 결과를 합성 합계로 오해하지 않게 한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def runtime_parity_plan() -> list[dict[str, Any]]:
    return [
        {
            "audit_id": "if_parity_primary_exact_extratrees",
            "status": "planned_guard",
            "observed": "hz_hx_hw003_model_family_extratrees_fwd18",
            "expected": "exact parity primary(정확 동등 우선)",
            "evidence": rel(ID_KPI),
            "effect": "정확 동등 후보를 다음 학습/검토의 우선 경로로 둔다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "audit_id": "if_parity_secondary_lgbm_mismatch",
            "status": "repair_required",
            "observed": rel(ID_DIFF),
            "expected": "probability mismatch separated(확률 불일치 분리)",
            "evidence": rel(ID_DIFF),
            "effect": "보조 LGBM 확률 차이를 숨기지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def cost_stress_plan() -> list[dict[str, Any]]:
    return [
        {
            "audit_id": "if_cost_stress_proxy_mt5_compare",
            "status": "planned",
            "observed": "IF materialization only(IF 물질화 전용)",
            "expected": "compare proxy EV with MT5 runtime after training(학습 뒤 프록시 예상값과 MT5 런타임 비교)",
            "evidence": rel(IE_COST_CONTRACT),
            "effect": "비용 압박이 MT5 KPI를 대체하지 않게 한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def task_seeds() -> list[dict[str, Any]]:
    base_inputs = rel(IF_INPUT_FRAME)
    features = rel(IF_ALLOWED_FEATURES)
    common_guard = "drop invalid fwd18 rows; no threshold tuning; review before training(무효 fwd18 행 제외, 임계값 조정 없음, 학습 전 검토)"
    return [
        {
            "task_id": "if_ie001_side_net_fwd18_extratrees",
            "repair_family": "side net stabilization(방향별 순익 안정화)",
            "target_column": "hx_label_class_fwd18",
            "valid_column": "hx_valid_fwd18",
            "sample_weight_column": "if_side_net_stability_weight",
            "model_family": "ExtraTrees(엑스트라트리스)_multiclass",
            "model_config_id": "extratrees_fwd18_exact_parity_preservation",
            "base_clue_model_id": "hz_hx_hw003_model_family_extratrees_fwd18",
            "input_frame": base_inputs,
            "allowed_features": features,
            "required_guard": common_guard,
            "expected_effect": "정확 동등 ExtraTrees(엑스트라트리스) 단서를 방향 균형 수리로 보존한다.",
            "forbidden_use": "candidate selection, MT5 claim, runtime authority(후보 선택, MT5 주장, 런타임 권위)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "task_id": "if_ie002_drawdown_fwd18_lgbm",
            "repair_family": "drawdown cluster control(낙폭 군집 제어)",
            "target_column": "hx_label_class_fwd18",
            "valid_column": "hx_valid_fwd18",
            "sample_weight_column": "if_drawdown_cluster_control_weight",
            "model_family": "LightGBM(라이트GBM)_multiclass",
            "model_config_id": "lgbm_fwd18_drawdown_cluster_control",
            "base_clue_model_id": "hz_hx_hw003_model_family_extratrees_fwd18",
            "input_frame": base_inputs,
            "allowed_features": features,
            "required_guard": common_guard,
            "expected_effect": "낙폭 군집을 낮추는 학습 후보를 만든다.",
            "forbidden_use": "candidate selection, MT5 claim, runtime authority(후보 선택, MT5 주장, 런타임 권위)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "task_id": "if_ie003_pf_recovery_fwd18_lgbm",
            "repair_family": "PF recovery trade shape(수익 팩터 회복 거래 형태)",
            "target_column": "hx_label_class_fwd18",
            "valid_column": "hx_valid_fwd18",
            "sample_weight_column": "if_pf_recovery_trade_shape_weight",
            "model_family": "LightGBM(라이트GBM)_multiclass",
            "model_config_id": "lgbm_fwd18_pf_recovery_trade_shape",
            "base_clue_model_id": "hz_hx_hw003_model_family_extratrees_fwd18",
            "input_frame": base_inputs,
            "allowed_features": features,
            "required_guard": common_guard,
            "expected_effect": "낮은 PF(수익 팩터)와 recovery(회복)를 동시에 수리한다.",
            "forbidden_use": "candidate selection, MT5 claim, runtime authority(후보 선택, MT5 주장, 런타임 권위)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "task_id": "if_ie003_pf_recovery_fwd18_xgboost",
            "repair_family": "PF recovery trade shape(수익 팩터 회복 거래 형태)",
            "target_column": "hx_label_class_fwd18",
            "valid_column": "hx_valid_fwd18",
            "sample_weight_column": "if_runtime_positive_repair_blend_weight",
            "model_family": "XGBoost(엑스지부스트)_multiclass",
            "model_config_id": "xgboost_fwd18_runtime_positive_repair_blend",
            "base_clue_model_id": "hz_hx_hw003_model_family_extratrees_fwd18",
            "input_frame": base_inputs,
            "allowed_features": features,
            "required_guard": common_guard,
            "expected_effect": "다른 model family(모델 계열)로 수익 구조 수리를 압박한다.",
            "forbidden_use": "candidate selection, MT5 claim, runtime authority(후보 선택, MT5 주장, 런타임 권위)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "task_id": "if_ie006_cost_stress_fwd18_lgbm",
            "repair_family": "cost stress consistency(비용 압박 일관성)",
            "target_column": "hx_label_class_fwd18",
            "valid_column": "hx_valid_fwd18",
            "sample_weight_column": "if_cost_stress_survival_weight",
            "model_family": "LightGBM(라이트GBM)_multiclass",
            "model_config_id": "lgbm_fwd18_cost_stress_survival",
            "base_clue_model_id": "hz_hx_hw003_model_family_extratrees_fwd18",
            "input_frame": base_inputs,
            "allowed_features": features,
            "required_guard": common_guard,
            "expected_effect": "비용 압박에서 PF(수익 팩터)가 무너지지 않는지 본다.",
            "forbidden_use": "candidate selection, MT5 claim, runtime authority(후보 선택, MT5 주장, 런타임 권위)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "task_id": "if_ie003_active_flat_repair_lgbm",
            "repair_family": "active flat trade-shape repair(활성/관망 거래 형태 수리)",
            "target_column": "hx_active_flat_label",
            "valid_column": "hx_valid_fwd18",
            "sample_weight_column": "if_runtime_positive_repair_blend_weight",
            "model_family": "LightGBM(라이트GBM)_binary",
            "model_config_id": "lgbm_active_flat_runtime_positive_repair",
            "base_clue_model_id": "hz_hx_hw001_fwd6_label_horizon_lgbm",
            "input_frame": base_inputs,
            "allowed_features": features,
            "required_guard": common_guard,
            "expected_effect": "저품질 거래 밀도를 active/flat(활성/관망) 단계에서 줄인다.",
            "forbidden_use": "candidate selection, MT5 claim, runtime authority(후보 선택, MT5 주장, 런타임 권위)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def review_queue() -> list[dict[str, Any]]:
    return [
        {
            "queue_id": "if_to_ig_input_review",
            "source_run_id": RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "task": "review_runtime_positive_repair_inputs_before_training(학습 전 런타임 양수 수리 입력 검토)",
            "required_inputs": f"{rel(IF_INPUT_FRAME)};{rel(IF_WEIGHT_AUDIT)};{rel(IF_FEATURE_BOUNDARY)};{rel(IF_TIER_RECORDS)};{rel(IF_TASK_SEEDS)}",
            "expected_outputs": "training eligibility(학습 적격성); leakage audit(누출 감사); run337IH training queue(337IH 학습 대기열)",
            "blocked_if_missing": "IF frame, weights, feature boundary, task seeds(IF 프레임/가중치/피처 경계/작업 씨앗)",
            "effect": "학습 전 검토를 강제한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def build_summary(frame: pd.DataFrame, weights: Sequence[Mapping[str, Any]], tasks: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    feature_schema = read_json(HZ_FEATURE_SCHEMA)
    id_kpi = read_csv_frame(ID_KPI)
    best = id_kpi.sort_values("net_profit", ascending=False).iloc[0].to_dict()
    return {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_action": NEXT_RUN_ID,
        "primary_family": "experiment_execution",
        "primary_skill": "obsidian-run-evidence-system",
        "support_skills": [
            "obsidian-experiment-design",
            "obsidian-data-integrity",
            "obsidian-model-validation",
            "obsidian-artifact-lineage",
            "obsidian-claim-discipline",
        ],
        "rows": int(len(frame)),
        "columns": int(len(frame.columns)),
        "feature_count": int(feature_schema.get("feature_count", 0)),
        "new_weight_count": len(NEW_WEIGHT_COLUMNS),
        "nonfinite_weight_rows": sum(int(row.get("nonfinite_rows", 0)) for row in weights),
        "task_seed_rows": len(tasks),
        "timestamp_min": str(frame["timestamp"].min()) if "timestamp" in frame.columns and len(frame) else "",
        "timestamp_max": str(frame["timestamp"].max()) if "timestamp" in frame.columns and len(frame) else "",
        "cost_policies": sorted(frame["cost_policy_id"].astype(str).unique().tolist()) if "cost_policy_id" in frame.columns else [],
        "best_source_model_id": str(best.get("model_id", "")),
        "best_source_net_profit": as_float(best.get("net_profit")),
        "best_source_profit_factor": as_float(best.get("profit_factor")),
        "best_source_recovery_factor": as_float(best.get("recovery_factor")),
        "best_source_max_drawdown_amount": as_float(best.get("max_drawdown_amount")),
        "candidate_selection": "not_run",
        "model_training": "not_run",
        "mt5_execution": "not_run",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def build_gates(summary: Mapping[str, Any], feature_rows: Sequence[Mapping[str, Any]], tier_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    ie_final = read_json(IE_FINAL)
    ie_gates = read_csv_frame(IE_GATES)
    ie_queue = read_csv_frame(IE_QUEUE)
    ie_passed = ie_gates["status"].astype(str).str.lower().isin(["pass", "passed"]).all()
    feature_pass = all(row.get("status") == "passed" for row in feature_rows)
    tier_names = {row.get("expected") for row in tier_rows}
    forbidden_clear = all(
        str(summary.get(key)) in {"not_run", "not_claimed"}
        for key in (
            "candidate_selection",
            "model_training",
            "mt5_execution",
            "forward_passed",
            "forward_failed",
            "runtime_authority",
            "operating_promotion",
            "goal_achieve",
        )
    )
    checks = [
        (
            "parent_ie_gates_passed",
            bool(ie_passed),
            f"{int(ie_gates['status'].astype(str).str.lower().isin(['pass', 'passed']).sum())}/{len(ie_gates)}",
            "all passed(모두 통과)",
            rel(IE_GATES),
            "IE 설계가 통과한 뒤에만 IF를 물질화한다.",
        ),
        (
            "parent_next_action_matches_if",
            str(ie_final.get("next_action")) == RUN_ID and ie_queue["next_run_id"].astype(str).eq(RUN_ID).any(),
            f"final={ie_final.get('next_action')}",
            RUN_ID,
            rel(IE_QUEUE),
            "IE 대기열이 IF를 가리키는지 확인한다.",
        ),
        (
            "source_inputs_present",
            not missing_inputs(INPUT_FILES),
            len(missing_inputs(INPUT_FILES)),
            "0",
            rel(IF_SOURCE_MAP),
            "필수 원천 산출물이 모두 있는지 확인한다.",
        ),
        (
            "input_frame_materialized",
            exists(IF_INPUT_FRAME) and summary["rows"] > 0,
            summary["rows"],
            ">0",
            rel(IF_INPUT_FRAME),
            "학습 전용 입력 프레임을 만든다.",
        ),
        (
            "new_weights_finite",
            summary["nonfinite_weight_rows"] == 0,
            summary["nonfinite_weight_rows"],
            "0",
            rel(IF_WEIGHT_AUDIT),
            "새 IF 가중치가 유한한지 확인한다.",
        ),
        (
            "feature_boundary_passed",
            feature_pass,
            "passed" if feature_pass else "failed",
            "passed",
            rel(IF_FEATURE_BOUNDARY),
            "새 가중치와 미래 목표가 피처에 들어가지 않는다.",
        ),
        (
            "tier_records_present",
            tier_names
            == {"Tier A separate(Tier A 분리)", "Tier B separate(Tier B 분리)", "Tier A+B combined(Tier A+B 합산)"},
            ";".join(sorted(str(item) for item in tier_names)),
            "Tier A/B/A+B",
            rel(IF_TIER_RECORDS),
            "티어 쌍 기록을 생략하지 않는다.",
        ),
        (
            "tier_b_missing_required_named",
            any(row.get("audit_id") == "if_tier_b_separate" and row.get("status") == "missing_required" for row in tier_rows),
            "missing_required",
            "missing_required",
            rel(IF_TIER_RECORDS),
            "Tier B 누락을 명시한다.",
        ),
        (
            "task_seed_matrix_opened",
            summary["task_seed_rows"] >= 6,
            summary["task_seed_rows"],
            ">=6",
            rel(IF_TASK_SEEDS),
            "다음 검토용 작업 씨앗을 만든다.",
        ),
        (
            "next_review_queue_opened",
            exists(IG_QUEUE) and summary["next_action"] == NEXT_RUN_ID,
            summary["next_action"],
            NEXT_RUN_ID,
            rel(IG_QUEUE),
            "학습 전 IG 검토를 연다.",
        ),
        (
            "no_forbidden_operating_claim",
            forbidden_clear,
            "not_run/not_claimed",
            "not_run/not_claimed",
            rel(CLAIM_RECEIPT),
            "학습, MT5, 후보 선택, 운영 주장을 금지한다.",
        ),
        (
            "required_gate_coverage_audit",
            True,
            "all required gates listed(필수 게이트 모두 기록)",
            "present(존재)",
            rel(GATE_AUDIT),
            "완료 주장을 게이트 근거와 연결한다.",
        ),
    ]
    return [
        {
            "gate_id": gate_id,
            "status": "passed" if passed else "failed",
            "observed": observed,
            "expected": expected,
            "evidence_path": evidence,
            "effect": effect,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for gate_id, passed, observed, expected, evidence, effect in checks
    ]


def write_receipts(summary: Mapping[str, Any], artifacts: Sequence[Path]) -> list[Path]:
    base = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "created_at_utc": now_utc(),
        "status": STATUS,
        "judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    receipts = [
        (
            RUN_EVIDENCE_RECEIPT,
            {
                **base,
                "measurement_scope": "input materialization only; no KPI measurement(입력 물질화 전용, KPI 측정 없음)",
                "management_state": "run folder, manifest, report, registries updated(실행 폴더/목록/보고서/등록부 갱신)",
                "judgment_class": "inconclusive_materialization_only(물질화 전용 불충분)",
                "scoreboard": "diagnostic_special(진단 특수)",
                "parity_level": "P0_unverified_runtime; P2 prior ONNX evidence only(P0 런타임 미검증, P2 기존 ONNX 근거만)",
                "wfo_status": "not_applicable(해당 없음)",
                "registry_update_required": "yes(예)",
                "negative_memory_required": "no(아니오)",
                "hard_gate_applicable": "no(아니오)",
                "evidence_boundary": "scout-only materialization(탐색 전용 물질화)",
            },
        ),
        (
            DATA_RECEIPT,
            {
                **base,
                "data_source": [rel(HX_FRAME), rel(HX_ALLOWED_FEATURES)],
                "time_axis": "timestamp is UTC closed-bar/as-of input(타임스탬프는 UTC 확정봉/시점 기준 입력)",
                "sample_scope": f"FPMarkets US100 M5 Tier A train-only rows={summary['rows']}; Tier B missing_required(FPMarkets US100 M5 Tier A 학습 전용 행={summary['rows']}, Tier B 필수 누락)",
                "missing_or_duplicate_check": rel(IF_FEATURE_BOUNDARY),
                "feature_label_boundary": "new if_* weights and hx_* labels are excluded from allowed features(새 if_* 가중치와 hx_* 라벨은 허용 피처에서 제외)",
                "split_boundary": "no split in IF; review before training(IF에서 분할 없음, 학습 전 검토)",
                "leakage_risk": "target-aware weights must stay train-only(목표 인식 가중치는 학습 전용이어야 함)",
                "data_hash_or_identity": {rel(IF_INPUT_FRAME): sha(IF_INPUT_FRAME)},
                "integrity_judgment": "usable_with_boundary(경계 조건부 사용 가능)",
            },
        ),
        (
            MODEL_RECEIPT,
            {
                **base,
                "model_family": "not_trained; task seeds only(미학습, 작업 씨앗 전용)",
                "target_and_label": "hx_label_class_fwd18 and hx_active_flat_label existing target columns(기존 목표 열)",
                "split_method": "not_run(미실행)",
                "selection_metric": "none(없음)",
                "secondary_metrics": "PF/recovery/drawdown/side/cost planned(PF/회복/낙폭/방향/비용 예정)",
                "threshold_policy": "fixed inherited labels; no threshold tuning(고정 상속 라벨, 임계값 조정 없음)",
                "overfit_risk": "multiple repair weights require IG review(복수 수리 가중치는 IG 검토 필요)",
                "calibration_risk": "not evaluated until training(학습 전 평가 없음)",
                "comparison_baseline": rel(ID_KPI),
                "validation_judgment": "exploratory_materialization(탐색 물질화)",
            },
        ),
        (
            PERFORMANCE_RECEIPT,
            {
                **base,
                "observed_change": "new IF weights materialized(새 IF 가중치 물질화)",
                "comparison_baseline": "ID runtime KPI and HX/HZ training inputs(ID 런타임 KPI와 HX/HZ 학습 입력)",
                "likely_drivers": "side balance, drawdown risk, PF recovery, cost stress(방향 균형, 낙폭 위험, PF 회복, 비용 압박)",
                "segment_checks": rel(IF_WEIGHT_AUDIT),
                "trade_shape": "planned for later proxy/MT5 review(향후 프록시/MT5 검토 예정)",
                "alternative_explanations": "weights may reduce signal or overfit train-only labels(가중치가 신호를 줄이거나 학습 전용 라벨에 과적합 가능)",
                "attribution_confidence": "materialization_only(물질화 전용)",
                "next_probe": NEXT_RUN_ID,
            },
        ),
        (
            JUDGMENT_RECEIPT,
            {
                **base,
                "result_subject": RUN_ID,
                "evidence_available": [rel(IF_INPUT_FRAME), rel(IF_WEIGHT_AUDIT), rel(IF_TASK_SEEDS)],
                "evidence_missing": "IG review, training, ONNX, proxy score, MT5 runtime probe(IG 검토, 학습, ONNX, 프록시 점수, MT5 런타임 탐침)",
                "judgment_label": JUDGMENT,
                "next_condition": NEXT_RUN_ID,
            },
        ),
        (
            CLAIM_RECEIPT,
            {
                **base,
                "candidate_selection": "not_run(미실행)",
                "model_training": "not_run(미실행)",
                "mt5_execution": "not_run(미실행)",
                "forward_passed": "not_claimed(미주장)",
                "forward_failed": "not_claimed(미주장)",
                "runtime_authority": "not_claimed(미주장)",
                "operating_promotion": "not_claimed(미주장)",
                "goal_achieve": "not_claimed(미주장)",
            },
        ),
    ]
    paths = [write_json(path, payload) for path, payload in receipts]
    lineage = {
        **base,
        "source_inputs": [rel(path) for path in INPUT_FILES],
        "producer": rel(Path(__file__)),
        "consumer": NEXT_RUN_ID,
        "artifact_paths": [rel(path) for path in list(artifacts) + paths],
        "artifact_hashes": {
            rel(path): sha(path)
            for path in list(artifacts) + paths
            if exists(path) and io(path).is_file()
        },
        "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
        "availability": "generated_with_manifest(목록과 함께 생성)",
        "lineage_judgment": "connected_with_boundary(경계 조건부 연결)",
    }
    paths.append(write_json(LINEAGE_RECEIPT, lineage))
    return paths


def make_final(summary: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    failed = [row["gate_id"] for row in gates if row["status"] != "passed"]
    final = dict(summary)
    final.update({"gate_rows": len(gates), "passed_gates": len(gates) - len(failed), "failed_gates": failed})
    return final


def write_report(final: Mapping[str, Any]) -> Path:
    text = f"""# run337IF Runtime Positive Repair Inputs(run337IF 런타임 양수 수리 입력)

## Summary(요약)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- gates(게이트): `{final['passed_gates']}/{final['gate_rows']}`
- rows(행): `{final['rows']}`
- feature_count(피처 수): `{final['feature_count']}`
- new_weight_count(새 가중치 수): `{final['new_weight_count']}`
- task_seed_rows(작업 씨앗 행): `{final['task_seed_rows']}`
- source_net_profit(원천 순수익): `{final['best_source_net_profit']}`
- source_profit_factor(원천 수익 팩터): `{final['best_source_profit_factor']}`
- source_drawdown(원천 낙폭): `{final['best_source_max_drawdown_amount']}`

## Action(행동)

IE design(IE 설계)을 IF train-only repair inputs(IF 학습 전용 수리 입력)으로 물질화했다.
Effect(효과): side/PF/recovery/drawdown/cost/parity(방향/PF/회복/낙폭/비용/동등성) 수리를 학습 전 검토 가능한 파일로 넘긴다.

## Boundary(경계)

No model training(모델 학습 없음), no MT5 execution(MT5 실행 없음), no candidate selection(후보 선택 없음), no runtime authority(런타임 권위 없음), no Goal Achieve(목표 달성 없음).

## Tier Records(티어 기록)

Tier A separate(Tier A 분리)는 materialized(물질화)다. Tier B separate(Tier B 분리)와 Tier A+B combined(Tier A+B 합산)는 `missing_required(필수 누락)`이다.

## Next(다음)

`{NEXT_RUN_ID}`에서 leakage(누출), feature boundary(피처 경계), tier records(티어 기록), training eligibility(학습 적격성)를 검토한다.
"""
    return write_bom_text(REPORT_PATH, text)


def write_decision(final: Mapping[str, Any]) -> Path:
    text = f"""# {TODAY} Stage337IF Decision(337IF 결정)

- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- evidence(근거): `{rel(IF_INPUT_FRAME)}`, `{rel(IF_WEIGHT_AUDIT)}`, `{rel(IF_TASK_SEEDS)}`

Action(행동): runtime positive repair design(런타임 양수 수리 설계)을 train-only materialized inputs(학습 전용 물질화 입력)로 만들었다.
Effect(효과): 다음 IG review(IG 검토)가 학습 전에 누출과 가중치 위험을 막을 수 있다.

claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return write_bom_text(DECISION_DOC, text)


def update_docs(final: Mapping[str, Any]) -> list[Path]:
    artifacts = []
    artifacts.append(
        write_bom_text(
            WORKSPACE_STATE,
            f"""current_stage_id: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {STATUS}
current_judgment: {JUDGMENT}
current_decision: {DECISION}
next_run_id: {NEXT_RUN_ID}
claim_boundary: {CLAIM_BOUNDARY}
updated_at: {TODAY}
""",
        )
    )
    artifacts.append(
        write_bom_text(
            CURRENT_WORKING_STATE,
            f"""# Current Working State(현재 작업 상태)

## Current Truth(현재 진실)

- active_stage(현재 단계): `{STAGE_ID}`
- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`

## Effect(효과)

IF materialization(IF 물질화)은 IE repair design(IE 수리 설계)을 학습 전용 입력으로 만들었다.
효과는 IG review(IG 검토)가 feature leakage(피처 누출), weight risk(가중치 위험), tier gap(티어 공백)을 먼저 막게 하는 것이다.

## Claim Boundary(주장 경계)

`{CLAIM_BOUNDARY}`
""",
        )
    )
    artifacts.append(
        write_bom_text(
            SELECTION_STATUS,
            f"""# Stage337 Selection Status(337단계 선택 상태)

- latest_run(최신 실행): `{RUN_ID}`
- latest_decision(최신 결정): `{DECISION}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- rebuild_status(재구축 상태): `{STATUS}`
- rows(행): `{final['rows']}`
- feature_count(피처 수): `{final['feature_count']}`
- new_weight_count(새 가중치 수): `{final['new_weight_count']}`
- task_seed_rows(작업 씨앗 행): `{final['task_seed_rows']}`
- candidate_selection(후보 선택): `not_run`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- operating_promotion(운영 승격): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): IF materialization(IF 물질화)은 입력만 만들고 모델 선택은 하지 않는다.
""",
        )
    )
    artifacts.append(
        write_bom_text(
            STAGE_BRIEF,
            f"""# {STAGE_ID}

Latest completed run(최근 완료 실행): `{RUN_ID}`

IF materialization(IF 물질화)은 runtime-positive repair inputs(런타임 양수 수리 입력) `{final['rows']}` rows(행)를 만들었다.
Effect(효과): `{NEXT_RUN_ID}`에서 학습 전 안전성을 검토할 수 있다.

No selected model(선택 모델 없음), no MT5 execution(MT5 실행 없음), no Goal Achieve(목표 달성 없음).
""",
        )
    )
    existing = io(CHANGELOG).read_text(encoding="utf-8-sig") if exists(CHANGELOG) else "# Changelog(변경 기록)\n"
    entry = (
        f"\n## {TODAY} - {RUN_ID}\n\n"
        f"- Action(행동): IE repair design(IE 수리 설계)을 IF train-only inputs(IF 학습 전용 입력) `{final['rows']}` rows(행)로 물질화했다.\n"
        f"- Effect(효과): `run337IG` 검토가 학습 전 leakage/tier/weight(누출/티어/가중치) 위험을 확인하게 됐다.\n"
    )
    if RUN_ID not in existing:
        artifacts.append(write_bom_text(CHANGELOG, existing.rstrip() + "\n" + entry))
    else:
        artifacts.append(CHANGELOG)
    return artifacts


def read_csv_dicts(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    if not exists(path):
        return [], []
    with io(path).open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), [dict(row) for row in reader]


def write_csv_dicts(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> Path:
    ensure_parent(path)
    with io(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: row.get(column, "") for column in columns})
    return path


def upsert_csv(path: Path, row: Mapping[str, Any], key: str) -> Path:
    columns, rows = read_csv_dicts(path)
    if not columns:
        columns = list(row.keys())
    for column in row:
        if column not in columns:
            columns.append(column)
    rows = [existing for existing in rows if str(existing.get(key, "")) != str(row.get(key, ""))]
    rows.append(dict(row))
    return write_csv_dicts(path, columns, rows)


def update_registers(final: Mapping[str, Any]) -> list[Path]:
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "runtime_positive_repair_input_materialization",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "notes": f"rows={final['rows']};features={final['feature_count']};weights={final['new_weight_count']};tasks={final['task_seed_rows']};next_action={NEXT_RUN_ID};goal_achieve_not_claimed.",
        "family": "experiment_execution",
        "primary_report": rel(REPORT_PATH),
        "run_number": RUN_NUMBER,
        "date": TODAY,
        "decision": DECISION,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "rows": final["rows"],
        "gate_passes": final["passed_gates"],
        "gate_total": final["gate_rows"],
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__input_materialization",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "runtime_positive_repair_input_materialization",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "runtime_positive_repair_inputs(런타임 양수 수리 입력)",
        "tier_scope": "Tier A separate materialized, Tier B missing_required, Tier A+B missing_required(Tier A 분리 물질화, Tier B 필수 누락, Tier A+B 필수 누락)",
        "kpi_scope": "input_materialization_only_no_training_no_mt5(입력 물질화 전용, 학습/MT5 없음)",
        "scoreboard_lane": "experiment_execution",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "primary_kpi": f"rows={final['rows']};weights={final['new_weight_count']};tasks={final['task_seed_rows']}",
        "guardrail_kpi": "feature_boundary;finite_weights;no_selection;no_goal",
        "external_verification_status": "out_of_scope_by_claim(주장 범위 밖)",
        "notes": f"decision={DECISION};next_action={NEXT_RUN_ID};claim_boundary={CLAIM_BOUNDARY}",
        "run_number": RUN_NUMBER,
        "date": TODAY,
        "decision": DECISION,
        "next_run_id": NEXT_RUN_ID,
        "rows": final["rows"],
        "gate_passes": final["passed_gates"],
        "gate_total": final["gate_rows"],
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__input_materialization",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "experiment_execution",
        "evidence_scope": "IE design, HX frame, HZ schema, ID runtime KPI(IE 설계, HX 프레임, HZ 스키마, ID 런타임 KPI)",
        "kpi_scope": "input_rows_weights_boundaries",
        "status": STATUS,
        "judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
        "path": rel(REPORT_PATH),
        "notes": f"gates={final['passed_gates']}/{final['gate_rows']};next_action={NEXT_RUN_ID};goal_achieve_not_claimed",
        "decision": DECISION,
        "run_key": f"{RUN_ID}__input_materialization",
        "family": "runtime_positive_repair_input_materialization",
        "question": "can runtime-positive weak KPI evidence become timestamp-safe repair inputs(런타임 양수 약한 KPI 근거를 시점 안전 수리 입력으로 바꿀 수 있는가)",
        "metric_scope": "rows_features_weights_boundaries",
        "primary_artifact": rel(IF_INPUT_FRAME),
        "report_path": rel(REPORT_PATH),
        "next_action": NEXT_RUN_ID,
        "run_number": RUN_NUMBER,
        "date": TODAY,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "rows": final["rows"],
        "gate_passes": final["passed_gates"],
        "gate_total": final["gate_rows"],
    }
    return [
        upsert_csv(RUN_REGISTRY, run_row, "run_id"),
        upsert_csv(PROJECT_LEDGER, alpha_row, "ledger_row_id"),
        upsert_csv(STAGE_LEDGER, stage_row, "ledger_row_id"),
    ]


def update_artifact_registry(paths: Sequence[Path]) -> Path:
    columns, rows = read_csv_dicts(ARTIFACT_REGISTRY)
    if not columns:
        columns = [
            "stage_id",
            "run_id",
            "artifact_type",
            "path",
            "sha256",
            "created_at",
            "claim_boundary",
            "artifact_id",
            "created_at_utc",
            "notes",
            "artifact_path",
        ]
    for column in (
        "stage_id",
        "run_id",
        "artifact_type",
        "path",
        "sha256",
        "created_at",
        "claim_boundary",
        "artifact_id",
        "created_at_utc",
        "notes",
        "artifact_path",
    ):
        if column not in columns:
            columns.append(column)
    rows = [
        row
        for row in rows
        if str(row.get("run_id", "")) != RUN_ID and not str(row.get("artifact_id", "")).startswith(f"{RUN_ID}::")
    ]
    created_at = now_utc()
    seen: set[str] = set()
    for path in paths:
        if not exists(path) or not io(path).is_file():
            continue
        artifact_path = rel(path)
        artifact_id = f"{RUN_ID}::{artifact_path}"
        if artifact_id in seen:
            continue
        seen.add(artifact_id)
        rows.append(
            {
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "artifact_type": path.suffix.lstrip(".") or "file",
                "path": artifact_path,
                "sha256": sha(path),
                "created_at": TODAY,
                "claim_boundary": CLAIM_BOUNDARY,
                "artifact_id": artifact_id,
                "created_at_utc": created_at,
                "notes": STATUS,
                "artifact_path": artifact_path,
            }
        )
    return write_csv_dicts(ARTIFACT_REGISTRY, columns, rows)


def main() -> int:
    io(RUN_DIR).mkdir(parents=True, exist_ok=True)
    missing = missing_inputs(INPUT_FILES)
    if missing:
        print(json.dumps({"run_id": RUN_ID, "status": "blocked_missing_inputs", "missing": missing}, ensure_ascii=False, indent=2))
        return 1

    base = pd.read_parquet(io(HX_FRAME))
    frame = materialize_frame(base)
    ensure_parent(IF_INPUT_FRAME)
    frame.to_parquet(io(IF_INPUT_FRAME), index=False)

    allowed = allowed_features_copy()
    write_frame_csv(IF_ALLOWED_FEATURES, allowed)
    weights = weight_audit(frame)
    features = feature_boundary_rows(allowed, frame)
    tiers = tier_records(frame)
    parity = runtime_parity_plan()
    costs = cost_stress_plan()
    tasks = task_seeds()
    queue = review_queue()
    summary = build_summary(frame, weights, tasks)

    artifacts: list[Path] = [
        IF_INPUT_FRAME,
        write_csv(IF_SOURCE_MAP, SOURCE_COLUMNS, source_map(frame)),
        IF_ALLOWED_FEATURES,
        write_csv(IF_WEIGHT_RECIPE, WEIGHT_RECIPE_COLUMNS, weight_recipes()),
        write_csv(IF_WEIGHT_AUDIT, WEIGHT_AUDIT_COLUMNS, weights),
        write_csv(IF_FEATURE_BOUNDARY, AUDIT_COLUMNS, features),
        write_csv(IF_TIER_RECORDS, AUDIT_COLUMNS, tiers),
        write_csv(IF_RUNTIME_PARITY_PLAN, AUDIT_COLUMNS, parity),
        write_csv(IF_COST_STRESS_PLAN, AUDIT_COLUMNS, costs),
        write_csv(IF_TASK_SEEDS, TASK_COLUMNS, tasks),
        write_csv(IG_QUEUE, QUEUE_COLUMNS, queue),
    ]
    gates = build_gates(summary, features, tiers)
    final = make_final(summary, gates)
    artifacts.extend(
        [
            write_csv(GATE_AUDIT, GATE_COLUMNS, gates),
            write_json(FINAL_DECISION, final),
            write_json(
                RUN_MANIFEST,
                {
                    "run_id": RUN_ID,
                    "stage_id": STAGE_ID,
                    "parent_run_id": PARENT_RUN_ID,
                    "created_at": TODAY,
                    "script": rel(Path(__file__)),
                    "inputs": [rel(path) for path in INPUT_FILES],
                    "outputs": [rel(path) for path in OUTPUT_FILES],
                    "claim_boundary": CLAIM_BOUNDARY,
                },
            ),
        ]
    )
    artifacts.extend(write_receipts(final, artifacts))
    artifacts.extend([write_report(final), write_decision(final)])
    artifacts.extend(update_docs(final))
    artifacts.extend(update_registers(final))
    artifacts.append(update_artifact_registry(artifacts + [Path(__file__)]))

    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": final["status"],
                "judgment": final["judgment"],
                "rows": final["rows"],
                "feature_count": final["feature_count"],
                "new_weight_count": final["new_weight_count"],
                "task_seed_rows": final["task_seed_rows"],
                "gates": f"{final['passed_gates']}/{final['gate_rows']}",
                "next_action": final["next_action"],
                "goal_achieve": final["goal_achieve"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if not final["failed_gates"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
