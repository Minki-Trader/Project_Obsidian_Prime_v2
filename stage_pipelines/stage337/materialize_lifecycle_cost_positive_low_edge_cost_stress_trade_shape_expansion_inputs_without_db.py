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
    design_lifecycle_cost_positive_low_edge_cost_stress_trade_shape_expansion_without_db as iu,
)


aw = iu.aw

TODAY = "2026-06-01"
STAGE_ID = iu.STAGE_ID
STAGE_DIR = iu.STAGE_DIR
RUN_NUMBER = "run337IV"
RUN_ID = "run337IV_materialize_lifecycle_cost_positive_low_edge_cost_stress_trade_shape_expansion_inputs_without_db_v1"
PARENT_RUN_ID = iu.RUN_ID
NEXT_RUN_ID = "run337IW_review_lifecycle_cost_positive_low_edge_cost_stress_trade_shape_expansion_inputs_without_db_v1"
STATUS = "completed_stage337IV_positive_low_edge_expansion_inputs_materialized_no_training_no_selection"
JUDGMENT = "timestamp_safe_positive_low_edge_expansion_inputs_materialized_review_required"
DECISION = "stage337IV_open_run337IW_review_positive_low_edge_expansion_inputs"
CLAIM_BOUNDARY = (
    "research_development_input_materialization_only_no_model_training_no_threshold_tuning_no_lot_optimization_"
    "no_candidate_selection_no_mt5_execution_no_forward_passed_no_forward_failed_no_live_readiness_"
    "no_operating_promotion_no_runtime_authority_no_goal_achieve"
)

RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEW_DIR / "run337IV_positive_low_edge_expansion_inputs.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage337IV_positive_low_edge_expansion_inputs.md"

RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
PROJECT_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
STAGE_LEDGER = STAGE_DIR / "03_reviews" / "stage_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs" / "context" / "current_working_state.md"
SELECTION_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
STAGE_BRIEF = STAGE_DIR / "README.md"
ROOT_CHANGELOG = ROOT / "CHANGELOG.md"
WORKSPACE_CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"

BASE_INPUT_FRAME = iu.it.isr.ir.iq.ip.io_review.inr.IN_INPUT_FRAME
BASE_ALLOWED_FEATURES = iu.it.isr.ir.iq.ip.io_review.inr.IN_ALLOWED_FEATURES

IV_INPUT_FRAME = RUN_DIR / "iv_positive_low_edge_expansion_input_frame.parquet"
IV_ALLOWED_FEATURES = RUN_DIR / "iv_allowed_model_feature_set.csv"
IV_SOURCE_MAP = RUN_DIR / "iv_source_map.csv"
IV_WEIGHT_RECIPE = RUN_DIR / "iv_weight_recipe_matrix.csv"
IV_WEIGHT_AUDIT = RUN_DIR / "iv_weight_audit.csv"
IV_FEATURE_BOUNDARY = RUN_DIR / "iv_feature_label_boundary_audit.csv"
IV_TASK_SEEDS = RUN_DIR / "run337IW_training_task_seed_matrix.csv"
IV_TIER_RECORDS = RUN_DIR / "iv_tier_records.csv"
IV_RUNTIME_COMPARISON_PLAN = RUN_DIR / "iv_runtime_comparison_plan.csv"
IW_QUEUE = RUN_DIR / "run337IW_input_review_queue.csv"
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

IV_WEIGHT_COLUMNS = (
    "iv_cost_stress_survival_buffer_weight",
    "iv_density_margin_entropy_throttle_weight",
    "iv_lifecycle_exit_hold_compression_weight",
    "iv_drawdown_regime_firewall_weight",
    "iv_side_net_long_rescue_weight",
    "iv_equity_curve_smoothness_weight",
    "iv_blended_cost_lifecycle_side_quality_weight",
)
IV_TARGET_COLUMNS = (
    "iv_label_class_cost_stress_fwd18",
    "iv_valid_cost_stress_fwd18",
)
FORBIDDEN_FEATURE_TOKENS = (
    "label",
    "future",
    "target",
    "mt5",
    "profit",
    "expectancy",
    "recovery",
)
FORBIDDEN_FEATURE_SUFFIXES = ("_weight", "_sample_weight")

INPUT_FILES = (
    iu.FINAL_DECISION,
    iu.GATE_AUDIT,
    iu.DESIGN_MATRIX,
    iu.ATTRIBUTION_MATRIX,
    iu.EXPERIMENT_CONTRACT,
    iu.FEATURE_LABEL_TRADE_CONTRACT,
    iu.COST_STRESS_CONTRACT,
    iu.RUNTIME_PARITY_GUARD,
    iu.TIER_PAIR_CONTRACT,
    iu.MATERIALIZATION_QUEUE,
    BASE_INPUT_FRAME,
    BASE_ALLOWED_FEATURES,
)
OUTPUT_FILES = (
    IV_INPUT_FRAME,
    IV_ALLOWED_FEATURES,
    IV_SOURCE_MAP,
    IV_WEIGHT_RECIPE,
    IV_WEIGHT_AUDIT,
    IV_FEATURE_BOUNDARY,
    IV_TASK_SEEDS,
    IV_TIER_RECORDS,
    IV_RUNTIME_COMPARISON_PLAN,
    IW_QUEUE,
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
    target = path if len(str(path)) < 240 else io(path)
    frame.to_csv(target, index=False, encoding="utf-8-sig", lineterminator="\n")
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
        return float(value)
    except (TypeError, ValueError):
        return default


def num(frame: pd.DataFrame, column: str, default: float = 0.0) -> pd.Series:
    if column not in frame.columns:
        return pd.Series(default, index=frame.index, dtype="float64")
    return pd.to_numeric(frame[column], errors="coerce").replace([np.inf, -np.inf], np.nan).fillna(default)


def rank01(values: pd.Series | np.ndarray) -> pd.Series:
    series = pd.Series(values).replace([np.inf, -np.inf], np.nan).astype("float64")
    if series.notna().sum() == 0:
        return pd.Series(0.5, index=series.index, dtype="float64")
    return series.rank(pct=True).fillna(0.5).astype("float64")


def clip_weight(values: pd.Series | np.ndarray, lower: float = 0.10, upper: float = 12.0) -> pd.Series:
    series = pd.Series(values).replace([np.inf, -np.inf], np.nan).fillna(1.0).astype("float64")
    return series.clip(lower=lower, upper=upper)


def feature_hash(features: Sequence[str]) -> str:
    return hashlib.sha256("\n".join(features).encode("utf-8")).hexdigest()


def passed_status(series: pd.Series) -> pd.Series:
    return series.astype(str).str.lower().isin(["pass", "passed", "true", "1", "yes"])


def forbidden_feature_violations(features: Sequence[str]) -> list[str]:
    violations = []
    train_only = {column.lower() for column in [*IV_WEIGHT_COLUMNS, *IV_TARGET_COLUMNS]}
    for feature in features:
        lowered = feature.lower()
        token_hit = any(token in lowered for token in FORBIDDEN_FEATURE_TOKENS)
        weight_hit = lowered in train_only or any(lowered.endswith(suffix) for suffix in FORBIDDEN_FEATURE_SUFFIXES)
        if token_hit or weight_hit:
            violations.append(feature)
    return violations


def cost_stress_label(frame: pd.DataFrame) -> pd.DataFrame:
    f18 = num(frame, "hx_future_log_return_18", np.nan)
    valid18 = num(frame, "hx_valid_fwd18", 0).astype(int).eq(1) & f18.notna()
    label = np.select([f18 > 0.0010, f18 < -0.0010], [2, 0], default=1).astype(int)
    label = pd.Series(label, index=frame.index)
    label.loc[~valid18] = -1
    frame["iv_label_class_cost_stress_fwd18"] = label.astype(int).to_numpy()
    frame["iv_valid_cost_stress_fwd18"] = valid18.astype(int).to_numpy()
    return frame


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
    return margin, entropy


def materialize_frame() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, dict[str, Any]]:
    frame = pd.read_parquet(io(BASE_INPUT_FRAME)).copy()
    allowed = read_csv(BASE_ALLOWED_FEATURES).copy()
    feature_col = "feature_name" if "feature_name" in allowed.columns else allowed.columns[0]
    features = [str(item) for item in allowed[feature_col].dropna().tolist()]
    missing_features = [feature for feature in features if feature not in frame.columns]
    if missing_features:
        raise ValueError(f"missing allowed features: {missing_features}")

    frame = cost_stress_label(frame)
    f6 = num(frame, "hx_future_log_return_6", np.nan)
    f18 = num(frame, "hx_future_log_return_18", np.nan)
    f24 = num(frame, "hx_future_log_return_24", np.nan)
    label18 = num(frame, "hx_label_class_fwd18", -1).astype(int)
    cost_label = num(frame, "iv_label_class_cost_stress_fwd18", -1).astype(int)
    abs6 = f6.abs().fillna(0.0)
    abs18 = f18.abs().fillna(0.0)
    abs24 = f24.abs().fillna(0.0)
    sign6 = np.sign(f6.fillna(0.0))
    sign18 = np.sign(f18.fillna(0.0))
    sign24 = np.sign(f24.fillna(0.0))
    sign_consistency = pd.Series(
        ((sign6 == sign18) & (sign18 == sign24) & (sign18 != 0)).astype("float64"),
        index=frame.index,
    )
    conflict = pd.Series(((sign6 != sign18) & (sign6 != 0) & (sign18 != 0)).astype("float64"), index=frame.index)
    vol_pressure = (
        rank01(num(frame, "historical_vol_5_over_20").abs())
        + rank01(num(frame, "atr_14_over_atr_50").abs())
        + rank01(num(frame, "hl_zscore_50").abs())
    ) / 3.0
    session_edge = (
        num(frame, "is_first_30m_after_open").clip(0, 1)
        + num(frame, "is_last_30m_before_cash_close").clip(0, 1)
        + num(frame, "is_us_cash_open").clip(0, 1) * 0.25
    )
    class_counts = label18[label18.isin([0, 1, 2])].value_counts().to_dict()
    class_weight = label18.map(lambda value: 1.0 / max(class_counts.get(int(value), 1), 1)).astype("float64")
    class_weight = (class_weight / class_weight.mean()).replace([np.inf, -np.inf], np.nan).fillna(1.0)
    probability_margin, probability_entropy = probability_context(frame)
    low_margin_rate = rank01(num(frame, "low_margin_rate", 0.0))
    drawdown_pressure = rank01(num(frame, "drawdown_pressure_norm", 0.0))
    worst_forward = pd.Series(np.maximum.reduce([(-f6).fillna(0.0), (-f18).fillna(0.0), (-f24).fillna(0.0)]), index=frame.index)
    edge_cost18 = (abs18 - 0.0010).clip(lower=0.0)
    edge_cost24 = (abs24 - 0.0012).clip(lower=0.0)

    frame["iv_cost_stress_survival_buffer_weight"] = clip_weight(
        0.45
        + 5.5 * rank01(edge_cost18)
        + 2.0 * cost_label.ne(1).astype("float64")
        + 1.5 * rank01(edge_cost24)
    ).to_numpy()
    frame["iv_density_margin_entropy_throttle_weight"] = clip_weight(
        0.35
        + 4.0 * rank01(probability_margin)
        + 2.0 * (1.0 - rank01(probability_entropy))
        + 1.5 * rank01(abs18)
        - 1.3 * low_margin_rate
    ).to_numpy()
    frame["iv_lifecycle_exit_hold_compression_weight"] = clip_weight(
        0.60
        + 3.2 * rank01(abs6)
        + 1.8 * sign_consistency
        - 1.2 * conflict
        + 1.2 * rank01((abs6 - abs18).abs())
    ).to_numpy()
    frame["iv_drawdown_regime_firewall_weight"] = clip_weight(
        0.55 + 2.5 * drawdown_pressure + 2.0 * vol_pressure + 1.2 * session_edge + 1.8 * rank01(abs18 * (0.5 + vol_pressure))
    ).to_numpy()
    frame["iv_side_net_long_rescue_weight"] = clip_weight(
        0.70
        + 3.2 * label18.eq(2).astype("float64") * rank01(f18.clip(lower=0.0).fillna(0.0))
        + 2.0 * label18.eq(0).astype("float64") * rank01((-f18).clip(lower=0.0).fillna(0.0))
        + 1.2 * class_weight
    ).to_numpy()
    frame["iv_equity_curve_smoothness_weight"] = clip_weight(
        0.55 + 2.4 * rank01(worst_forward.clip(lower=0.0)) + 2.0 * rank01(abs18) + 1.2 * vol_pressure
    ).to_numpy()
    frame["iv_blended_cost_lifecycle_side_quality_weight"] = clip_weight(
        frame[list(IV_WEIGHT_COLUMNS[:-1])].mean(axis=1) * 1.12
    ).to_numpy()

    allowed["claim_boundary"] = CLAIM_BOUNDARY
    allowed["iv_usage"] = "allowed_model_input_for_run337IW_review_and_later_training(337IW 검토와 이후 학습 허용 입력)"
    ensure_parent(IV_INPUT_FRAME)
    frame.to_parquet(io(IV_INPUT_FRAME), index=False)
    write_csv(IV_ALLOWED_FEATURES, allowed)

    source_map = pd.DataFrame(
        [
            {
                "source_id": "base_in_input_frame",
                "source_path": rel(BASE_INPUT_FRAME),
                "source_type": "parquet",
                "exists": exists(BASE_INPUT_FRAME),
                "sha256": sha(BASE_INPUT_FRAME),
                "effect": "IN 입력 프레임을 이어받아 양수 낮은 엣지 확장용 학습 전용 가중치를 추가한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "source_id": "iu_design_matrix",
                "source_path": rel(iu.DESIGN_MATRIX),
                "source_type": "csv",
                "exists": exists(iu.DESIGN_MATRIX),
                "sha256": sha(iu.DESIGN_MATRIX),
                "effect": "IU 설계 축을 실제 입력 생성 규칙으로 연결한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "source_id": "iu_cost_stress_contract",
                "source_path": rel(iu.COST_STRESS_CONTRACT),
                "source_type": "csv",
                "exists": exists(iu.COST_STRESS_CONTRACT),
                "sha256": sha(iu.COST_STRESS_CONTRACT),
                "effect": "비용 압박 설계를 학습 전용 라벨과 가중치로 연결한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ]
    )
    recipe = pd.DataFrame(
        [
            {
                "weight_column": column,
                "source_columns": "hx_future_log_return_6;hx_future_log_return_18;hx_future_log_return_24;hx_label_class_fwd18;probability_context;timestamp-known context",
                "lower_bound": 0.10,
                "upper_bound": 12.0,
                "train_only_formula": "rank/label/probability-pressure formula; never allowed as model feature(순위/라벨/확률 압박 공식, 모델 피처 금지)",
                "effect": "IU 확장 축을 학습 표본 압력으로 바꾼다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
            for column in IV_WEIGHT_COLUMNS
        ]
    )
    audit_rows = []
    for column in IV_WEIGHT_COLUMNS:
        values = pd.to_numeric(frame[column], errors="coerce")
        audit_rows.append(
            {
                "weight_column": column,
                "rows": int(len(values)),
                "weight_min": float(values.min()),
                "weight_mean": float(values.mean()),
                "weight_max": float(values.max()),
                "nonfinite_rows": int((~np.isfinite(values.to_numpy(dtype="float64"))).sum()),
                "max_saturation_rate": float((values >= 12.0).mean()),
                "short_label_mean": float(values[label18 == 0].mean()) if (label18 == 0).any() else 0.0,
                "flat_label_mean": float(values[label18 == 1].mean()) if (label18 == 1).any() else 0.0,
                "long_label_mean": float(values[label18 == 2].mean()) if (label18 == 2).any() else 0.0,
                "effect": "가중치 분포가 유한하고 과포화되지 않았는지 확인한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    weight_audit = pd.DataFrame(audit_rows)
    forbidden_violations = forbidden_feature_violations(features)
    feature_boundary = pd.DataFrame(
        [
            {
                "audit_id": "allowed_feature_count",
                "status": "passed" if len(features) == 58 else "failed",
                "observed": len(features),
                "expected": 58,
                "evidence": rel(IV_ALLOWED_FEATURES),
                "effect": "모델 입력 피처 수를 기존 58개로 고정한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "audit_id": "new_weights_excluded_from_features",
                "status": "passed" if not set(IV_WEIGHT_COLUMNS).intersection(set(features)) else "failed",
                "observed": ";".join(sorted(set(IV_WEIGHT_COLUMNS).intersection(set(features)))),
                "expected": "none(없음)",
                "evidence": rel(IV_ALLOWED_FEATURES),
                "effect": "학습 전용 가중치가 모델 피처로 새지 않게 한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "audit_id": "new_labels_excluded_from_features",
                "status": "passed" if not set(IV_TARGET_COLUMNS).intersection(set(features)) else "failed",
                "observed": ";".join(sorted(set(IV_TARGET_COLUMNS).intersection(set(features)))),
                "expected": "none(없음)",
                "evidence": rel(IV_ALLOWED_FEATURES),
                "effect": "학습 라벨이 모델 피처로 새지 않게 한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "audit_id": "forbidden_feature_tokens",
                "status": "passed" if not forbidden_violations else "failed",
                "observed": ";".join(forbidden_violations),
                "expected": "none(없음)",
                "evidence": rel(IV_ALLOWED_FEATURES),
                "effect": "future/label/MT5 관련 열이 피처로 들어가지 않게 한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ]
    )
    cost_valid = frame["iv_valid_cost_stress_fwd18"].astype(int).eq(1)
    cost_counts = frame.loc[cost_valid, "iv_label_class_cost_stress_fwd18"].value_counts().to_dict()
    timestamp = pd.to_datetime(frame["timestamp"], utc=True, errors="coerce") if "timestamp" in frame.columns else pd.Series(pd.NaT, index=frame.index)
    summary = {
        "rows": int(len(frame)),
        "columns": int(len(frame.columns)),
        "feature_count": int(len(features)),
        "feature_order_hash": feature_hash(features),
        "new_weight_count": len(IV_WEIGHT_COLUMNS),
        "new_target_count": len(IV_TARGET_COLUMNS),
        "weight_nonfinite_rows": int(weight_audit["nonfinite_rows"].sum()),
        "max_weight_saturation_rate": float(weight_audit["max_saturation_rate"].max()),
        "timestamp_min": str(timestamp.min()),
        "timestamp_max": str(timestamp.max()),
        "cost_stress_valid_rows": int(cost_valid.sum()),
        "cost_stress_class_count": int(len(cost_counts)),
        "cost_stress_class_counts_json": json.dumps({str(k): int(v) for k, v in sorted(cost_counts.items())}, ensure_ascii=False, sort_keys=True),
        "source_input_frame": rel(BASE_INPUT_FRAME),
        "allowed_features": rel(IV_ALLOWED_FEATURES),
        "input_frame": rel(IV_INPUT_FRAME),
    }
    return frame, allowed, source_map, recipe, weight_audit, feature_boundary, summary


def task_seeds() -> pd.DataFrame:
    common = {
        "input_frame": rel(IV_INPUT_FRAME),
        "allowed_features": rel(IV_ALLOWED_FEATURES),
        "required_guard": "drop invalid rows; no threshold tuning; review before training(무효 행 제외, 임계값 조정 없음, 학습 전 검토)",
        "forbidden_use": "candidate selection, MT5 claim, runtime authority(후보 선택, MT5 주장, 런타임 권위)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    rows = [
        {
            "task_id": "iv_iu001_cost_stress_fwd18_xgboost",
            "repair_family": "cost stress survival buffer(비용 압박 생존 완충)",
            "target_column": "iv_label_class_cost_stress_fwd18",
            "valid_column": "iv_valid_cost_stress_fwd18",
            "sample_weight_column": "iv_cost_stress_survival_buffer_weight",
            "model_family": "XGBoost(엑스지부스트)_multiclass",
            "model_config_id": "xgboost_fwd18_cost_stress_survival_buffer",
            "base_clue_model_id": "ip_in_im007_lifecycle_cost_blend_fwd18_xgboost",
            "expected_effect": "비용 압박 뒤에도 남는 두꺼운 edge(우위)를 찾는다.",
        },
        {
            "task_id": "iv_iu002_density_entropy_fwd18_lgbm",
            "repair_family": "density margin entropy throttle(밀도 마진 엔트로피 제한)",
            "target_column": "hx_label_class_fwd18",
            "valid_column": "hx_valid_fwd18",
            "sample_weight_column": "iv_density_margin_entropy_throttle_weight",
            "model_family": "LightGBM(라이트GBM)_multiclass",
            "model_config_id": "lgbm_fwd18_density_entropy_throttle",
            "base_clue_model_id": "ip_in_im007_lifecycle_cost_blend_fwd18_xgboost",
            "expected_effect": "저마진 고밀도 신호를 줄이고 확률 품질을 높인다.",
        },
        {
            "task_id": "iv_iu003_lifecycle_fwd6_lgbm",
            "repair_family": "lifecycle exit hold compression(생명주기 청산 보유 압축)",
            "target_column": "hx_label_class_fwd6",
            "valid_column": "hx_valid_fwd6",
            "sample_weight_column": "iv_lifecycle_exit_hold_compression_weight",
            "model_family": "LightGBM(라이트GBM)_multiclass",
            "model_config_id": "lgbm_fwd6_lifecycle_exit_hold_compression",
            "base_clue_model_id": "ip_in_im007_lifecycle_cost_blend_fwd18_xgboost",
            "expected_effect": "보유 생명주기를 짧게 압축해 낙폭 대비 회복을 개선한다.",
        },
        {
            "task_id": "iv_iu004_drawdown_regime_fwd18_extratrees",
            "repair_family": "drawdown regime firewall(낙폭 국면 방화벽)",
            "target_column": "hx_label_class_fwd18",
            "valid_column": "hx_valid_fwd18",
            "sample_weight_column": "iv_drawdown_regime_firewall_weight",
            "model_family": "ExtraTrees(엑스트라트리스)_multiclass",
            "model_config_id": "extratrees_fwd18_drawdown_regime_firewall",
            "base_clue_model_id": "ip_in_im007_lifecycle_cost_blend_fwd18_xgboost",
            "expected_effect": "변동성과 세션 취약 구간에서 손실 연속성을 줄인다.",
        },
        {
            "task_id": "iv_iu005_side_net_fwd18_xgboost",
            "repair_family": "side net long rescue(방향 순수익 롱 구조 수리)",
            "target_column": "hx_label_class_fwd18",
            "valid_column": "hx_valid_fwd18",
            "sample_weight_column": "iv_side_net_long_rescue_weight",
            "model_family": "XGBoost(엑스지부스트)_multiclass",
            "model_config_id": "xgboost_fwd18_side_net_long_rescue",
            "base_clue_model_id": "ip_in_im007_lifecycle_cost_blend_fwd18_xgboost",
            "expected_effect": "롱/숏 방향 순수익 비대칭을 줄인다.",
        },
        {
            "task_id": "iv_iu006_equity_smooth_fwd24_lgbm",
            "repair_family": "equity curve smoothness proxy(수익곡선 매끄러움 프록시)",
            "target_column": "hx_label_class_fwd24",
            "valid_column": "hx_valid_fwd24",
            "sample_weight_column": "iv_equity_curve_smoothness_weight",
            "model_family": "LightGBM(라이트GBM)_multiclass",
            "model_config_id": "lgbm_fwd24_equity_curve_smoothness",
            "base_clue_model_id": "ip_in_im007_lifecycle_cost_blend_fwd18_xgboost",
            "expected_effect": "긴 보유 손실 꼬리를 줄여 수익곡선 품질을 압박한다.",
        },
        {
            "task_id": "iv_iu007_blended_quality_fwd18_xgboost",
            "repair_family": "blended cost lifecycle side quality(비용/생명주기/방향 품질 혼합)",
            "target_column": "iv_label_class_cost_stress_fwd18",
            "valid_column": "iv_valid_cost_stress_fwd18",
            "sample_weight_column": "iv_blended_cost_lifecycle_side_quality_weight",
            "model_family": "XGBoost(엑스지부스트)_multiclass",
            "model_config_id": "xgboost_fwd18_blended_cost_lifecycle_side_quality",
            "base_clue_model_id": "ip_in_im007_lifecycle_cost_blend_fwd18_xgboost",
            "expected_effect": "비용, 생명주기, 방향 품질을 동시에 압박한다.",
        },
    ]
    return pd.DataFrame([{**row, **common} for row in rows])


def support_plans() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    tiers = pd.DataFrame(
        [
            {
                "tier_view": "Tier A separate(Tier A 분리)",
                "status": "materialized",
                "evidence": rel(IV_INPUT_FRAME),
                "effect": "전체 문맥 표본 입력을 물질화했다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "tier_view": "Tier B separate(Tier B 분리)",
                "status": "missing_required",
                "evidence": rel(IV_TIER_RECORDS),
                "effect": "부분 문맥 표본 누락을 생략하지 않는다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "tier_view": "Tier A+B combined(Tier A+B 합산)",
                "status": "missing_required",
                "evidence": rel(IV_TIER_RECORDS),
                "effect": "합산 입력이 없음을 명시한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ]
    )
    runtime = pd.DataFrame(
        [
            {
                "plan_id": "positive_low_edge_candidates_require_mt5_probe",
                "requirement": "Any later proxy-positive ONNX candidate must be compared with MT5 runtime probe(이후 프록시 양성 ONNX 후보는 MT5 런타임 탐침 비교 필수).",
                "evidence": rel(iu.RUNTIME_PARITY_GUARD),
                "effect": "프록시 KPI(핵심 성과 지표)가 MT5 KPI(MT5 핵심 성과 지표)를 대체하지 못하게 한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )
    queue = pd.DataFrame(
        [
            {
                "next_run_id": NEXT_RUN_ID,
                "parent_run_id": RUN_ID,
                "queued_task": "review_positive_low_edge_expansion_inputs(양수 낮은 엣지 확장 입력 검토)",
                "required_inputs": f"{rel(IV_INPUT_FRAME)};{rel(IV_WEIGHT_AUDIT)};{rel(IV_FEATURE_BOUNDARY)};{rel(IV_TASK_SEEDS)}",
                "expected_outputs": "eligibility matrix and training queue(적격성 행렬과 학습 대기열)",
                "blocked_if_missing": "input frame, finite weights, task seeds(입력 프레임, 유한 가중치, 작업 씨앗)",
                "effect": "학습 전에 입력 경계와 가중치 분포를 검토한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )
    return tiers, runtime, queue


def gate_row(gate: str, status: str, evidence: str, observed: Any, expected: Any, effect: str) -> dict[str, Any]:
    return {
        "gate_id": gate,
        "status": status,
        "evidence_path": evidence,
        "observed": observed,
        "expected": expected,
        "effect": effect,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def make_gates(summary: Mapping[str, Any], feature_boundary: pd.DataFrame, weight_audit: pd.DataFrame, tasks: pd.DataFrame) -> pd.DataFrame:
    parent_gates = read_csv(iu.GATE_AUDIT)
    no_forbidden = (
        summary["candidate_selection"] == "not_run"
        and summary["model_training"] == "not_run"
        and summary["mt5_execution"] == "not_run"
        and summary["forward_passed"] == "not_claimed"
        and summary["forward_failed"] == "not_claimed"
        and summary["goal_achieve"] == "not_claimed"
        and summary["runtime_authority"] == "not_claimed"
        and summary["operating_promotion"] == "not_claimed"
    )
    return pd.DataFrame(
        [
            gate_row(
                "parent_iu_gates_passed",
                "passed" if passed_status(parent_gates["status"]).all() else "failed",
                rel(iu.GATE_AUDIT),
                f"{int(passed_status(parent_gates['status']).sum())}/{len(parent_gates)}",
                "all passed(전부 통과)",
                "IU 설계 gate(게이트)가 통과된 뒤 입력을 만든다.",
            ),
            gate_row(
                "source_input_loaded",
                "passed" if exists(IV_INPUT_FRAME) and summary["rows"] >= 87600 else "failed",
                rel(IV_INPUT_FRAME),
                summary["rows"],
                ">=87600",
                "기존 IN 입력 프레임을 손실 없이 이어받는다.",
            ),
            gate_row(
                "allowed_feature_boundary_preserved",
                "passed" if feature_boundary["status"].astype(str).eq("passed").all() else "failed",
                rel(IV_FEATURE_BOUNDARY),
                f"feature_count={summary['feature_count']}",
                "58 and no forbidden(58개와 금지 없음)",
                "모델 피처 58개와 금지 토큰 경계를 지킨다.",
            ),
            gate_row(
                "new_weights_finite",
                "passed" if summary["weight_nonfinite_rows"] == 0 else "failed",
                rel(IV_WEIGHT_AUDIT),
                summary["weight_nonfinite_rows"],
                "0",
                "새 학습 전용 가중치가 모두 유한하다.",
            ),
            gate_row(
                "weight_saturation_controlled",
                "passed" if summary["max_weight_saturation_rate"] <= 0.05 else "failed",
                rel(IV_WEIGHT_AUDIT),
                summary["max_weight_saturation_rate"],
                "<=0.05",
                "가중치 상한 포화가 5% 이하인지 확인한다.",
            ),
            gate_row(
                "cost_stress_label_valid",
                "passed" if summary["cost_stress_valid_rows"] > 85000 and summary["cost_stress_class_count"] == 3 else "failed",
                rel(IV_INPUT_FRAME),
                f"valid={summary['cost_stress_valid_rows']};classes={summary['cost_stress_class_counts_json']}",
                "valid>85000 and classes=3(유효 85000 초과와 클래스 3개)",
                "비용 압박 라벨이 학습 가능한 분포인지 확인한다.",
            ),
            gate_row(
                "task_seed_matrix_written",
                "passed" if exists(IV_TASK_SEEDS) and len(tasks) >= 7 else "failed",
                rel(IV_TASK_SEEDS),
                len(tasks),
                ">=7",
                "다음 검토/학습용 작업 씨앗을 만든다.",
            ),
            gate_row(
                "tier_pair_records_written",
                "passed" if exists(IV_TIER_RECORDS) and len(read_csv(IV_TIER_RECORDS)) == 3 else "failed",
                rel(IV_TIER_RECORDS),
                len(read_csv(IV_TIER_RECORDS)) if exists(IV_TIER_RECORDS) else 0,
                "3",
                "Tier A/B/combined(티어 A/B/합산) 기록을 남긴다.",
            ),
            gate_row(
                "runtime_comparison_plan_written",
                "passed" if exists(IV_RUNTIME_COMPARISON_PLAN) else "failed",
                rel(IV_RUNTIME_COMPARISON_PLAN),
                exists(IV_RUNTIME_COMPARISON_PLAN),
                "true",
                "프록시 양성은 MT5 런타임 비교로 이어지게 한다.",
            ),
            gate_row(
                "next_review_queue_opened",
                "passed" if exists(IW_QUEUE) else "failed",
                rel(IW_QUEUE),
                exists(IW_QUEUE),
                "true",
                "IW input review(입력 검토)를 연다.",
            ),
            gate_row(
                "no_forbidden_operating_claim",
                "passed" if no_forbidden else "failed",
                rel(CLAIM_RECEIPT),
                "not_claimed",
                "not_claimed",
                "학습, MT5 실행, 선택, 운영 주장을 하지 않는다.",
            ),
            gate_row(
                "required_gate_coverage_audit_written",
                "passed",
                rel(GATE_AUDIT),
                "written",
                "written",
                "gate coverage(게이트 커버리지)를 closeout(종료 기록)에 연결한다.",
            ),
        ]
    )


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


def artifact_paths() -> list[Path]:
    return [
        IV_INPUT_FRAME,
        IV_ALLOWED_FEATURES,
        IV_SOURCE_MAP,
        IV_WEIGHT_RECIPE,
        IV_WEIGHT_AUDIT,
        IV_FEATURE_BOUNDARY,
        IV_TASK_SEEDS,
        IV_TIER_RECORDS,
        IV_RUNTIME_COMPARISON_PLAN,
        IW_QUEUE,
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
        Path(__file__),
    ]


def update_artifact_registry(paths: Sequence[Path]) -> None:
    registry = read_csv(ARTIFACT_REGISTRY) if exists(ARTIFACT_REGISTRY) else pd.DataFrame()
    required = ["stage_id", "run_id", "artifact_type", "path", "sha256", "created_at", "claim_boundary"]
    for column in required:
        if column not in registry.columns:
            registry[column] = ""
    rows = []
    for path in paths:
        if exists(path) and io(path).is_file():
            rows.append(
                {
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "artifact_type": "report" if path.suffix.lower() == ".md" else path.suffix.lower().lstrip("."),
                    "path": rel(path),
                    "sha256": sha(path),
                    "created_at": TODAY,
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    if rows:
        new_paths = {row["path"] for row in rows}
        registry = registry.loc[~registry["path"].astype(str).isin(new_paths)].copy()
        registry = pd.concat([registry, pd.DataFrame(rows)], ignore_index=True)
        columns = list(dict.fromkeys(required + list(registry.columns)))
        write_csv(ARTIFACT_REGISTRY, registry[columns])


def write_receipts(summary: Mapping[str, Any], gates: pd.DataFrame) -> None:
    base = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "created_at_utc": now_utc(),
        "status": STATUS,
        "judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(
        RUN_EVIDENCE_RECEIPT,
        {
            **base,
            "measurement_scope": "input materialization only(입력 물질화 전용)",
            "scoreboard": "structural_scout(구조 탐색)",
            "parity_level": "P1_dataset_feature_aligned(P1 데이터/피처 정렬)",
            "effect": "학습 전 입력 정체성을 고정한다.",
        },
    )
    write_json(
        DATA_RECEIPT,
        {
            **base,
            "data_source": rel(BASE_INPUT_FRAME),
            "time_axis": "bar close timestamp UTC inherited from IN(봉 마감 UTC 시각 상속)",
            "sample_scope": f"rows={summary['rows']}; {summary['timestamp_min']} to {summary['timestamp_max']}",
            "missing_or_duplicate_check": "timestamp column inherited; duplicate audit deferred to IW review(timestamp 열 상속, 중복 감사는 IW 검토에서 수행)",
            "feature_label_boundary": "new labels and weights are train-only and excluded from allowed model features(새 라벨과 가중치는 학습 전용이며 모델 피처 제외)",
            "split_boundary": "no new split; source row order inherited for later inner split(새 분할 없음, 이후 내부 분할용 원천 행 순서 상속)",
            "leakage_risk": "future returns used only for labels/weights and excluded from feature set(미래 수익은 라벨/가중치 전용이며 피처 제외)",
            "data_hash_or_identity": sha(IV_INPUT_FRAME) if exists(IV_INPUT_FRAME) else "missing",
            "integrity_judgment": "usable_with_boundary(경계 조건부 사용 가능)",
        },
    )
    write_json(
        MODEL_RECEIPT,
        {
            **base,
            "model_family": "not_trained",
            "target_and_label": "task seeds only(작업 씨앗 전용)",
            "threshold_policy": "not_applicable_no_threshold_tuning(해당 없음, 임계값 조정 없음)",
            "validation_judgment": "exploratory_input_materialization(탐색 입력 물질화)",
        },
    )
    write_json(
        PERFORMANCE_RECEIPT,
        {
            **base,
            "source_positive_low_edge": "IT MT5 exact parity positive low edge(IT MT5 정확 동등성 양수 낮은 엣지)",
            "new_weight_count": summary["new_weight_count"],
            "cost_stress_valid_rows": summary["cost_stress_valid_rows"],
            "max_weight_saturation_rate": summary["max_weight_saturation_rate"],
            "effect": "낮은 수익 구조를 비용/생명주기/방향/수익곡선 압박 입력으로 변환했다.",
        },
    )
    write_json(
        JUDGMENT_RECEIPT,
        {
            **base,
            "decision": DECISION,
            "next_run_id": NEXT_RUN_ID,
            "gate_passes": int(gates["status"].astype(str).eq("passed").sum()),
            "gate_total": int(len(gates)),
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            **base,
            "candidate_selection": "not_run",
            "model_training": "not_run",
            "mt5_execution": "not_run",
            "forward_passed": "not_claimed",
            "forward_failed": "not_claimed",
            "runtime_authority": "not_claimed",
            "operating_promotion": "not_claimed",
            "goal_achieve": "not_claimed",
        },
    )
    write_json(
        LINEAGE_RECEIPT,
        {
            **base,
            "source_inputs": [rel(path) for path in INPUT_FILES],
            "input_frame": rel(IV_INPUT_FRAME),
            "task_seed_matrix": rel(IV_TASK_SEEDS),
            "consumer": NEXT_RUN_ID,
            "artifact_hashes": {rel(path): sha(path) for path in artifact_paths() if exists(path)},
            "effect": "IU 설계와 IW 검토를 산출물 계보로 연결한다.",
        },
    )


def write_final(summary: Mapping[str, Any], gates: pd.DataFrame, tasks: pd.DataFrame) -> dict[str, Any]:
    final = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_action": NEXT_RUN_ID,
        "candidate_selection": "not_run",
        "model_training": "not_run",
        "mt5_execution": "not_run",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "live_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "task_seed_rows": int(len(tasks)),
        "gate_passes": int(gates["status"].astype(str).eq("passed").sum()),
        "gate_total": int(len(gates)),
        "claim_boundary": CLAIM_BOUNDARY,
        **dict(summary),
    }
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
    report = f"""# run337IV Positive Low-Edge Expansion Inputs(run337IV 양수 낮은 엣지 확장 입력)

## Summary(요약)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- judgment(판정): `{JUDGMENT}`
- gates(게이트): `{final['gate_passes']}/{final['gate_total']}`
- rows(행): `{final['rows']}`
- feature_count(피처 수): `{final['feature_count']}`
- new_weight_count(새 가중치 수): `{final['new_weight_count']}`
- task_seed_rows(작업 씨앗 행): `{final['task_seed_rows']}`
- cost_stress_valid_rows(비용 압박 유효 행): `{final['cost_stress_valid_rows']}`
- max_weight_saturation_rate(최대 가중치 포화율): `{final['max_weight_saturation_rate']}`

## Action(행동)

IU design(IU 설계)을 받아 train-only weight(학습 전용 가중치) 7개, cost-stress label(비용 압박 라벨), task seed(작업 씨앗) 7개를 만들었다.
Effect(효과): positive low-edge(MT5 양수 낮은 엣지) 단서를 비용/생명주기/밀도/방향/수익곡선 압박 학습 입력으로 바꾼다.

## Boundary(경계)

No model training(모델 학습 없음), no MT5 execution(MT5 실행 없음), no selected model(선정 모델 없음), no runtime authority(런타임 권위 없음), no Goal Achieve(목표 달성 없음).

## Next(다음)

`{NEXT_RUN_ID}`에서 input review(입력 검토)를 수행한다.
"""
    decision = f"""# {TODAY} Stage337IV Decision(337IV 결정)

- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- evidence(근거): `{rel(IV_INPUT_FRAME)}`, `{rel(IV_WEIGHT_AUDIT)}`, `{rel(IV_TASK_SEEDS)}`

Action(행동): timestamp-safe(시점 안전) 양수 낮은 엣지 확장 입력을 물질화했다.
Effect(효과): 다음 단계는 학습이 아니라 입력 적격성 검토로 닫힌다.

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

IV materialization(IV 물질화)은 새 비용 압박 라벨과 학습 전용 가중치, task seed(작업 씨앗)를 만들었다.
효과는 IW review(IW 검토)가 모델 학습 전에 누출, 포화, 피처 경계를 확인하게 하는 것이다.

## Claim Boundary(주장 경계)

`{CLAIM_BOUNDARY}`
"""
    selection = f"""# Stage337 Selection Status(337단계 선택 상태)

- latest_run(최신 실행): `{RUN_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- selected_model(선정 모델): `none(없음)`
- probe_priority_model(탐침 우선 모델): `ip_in_im007_lifecycle_cost_blend_fwd18_xgboost`
- latest_judgment(최신 판정): `positive_low_edge_inputs_materialized_review_required(양수 낮은 엣지 입력 물질화, 검토 필요)`
- runtime_authority(런타임 권위): `not_claimed(주장 안 함)`
- operating_promotion(운영 승격): `not_claimed(주장 안 함)`
- live_readiness(실거래 준비): `not_claimed(주장 안 함)`
- goal_achieve(목표 달성): `not_claimed(주장 안 함)`

Effect(효과): 입력 물질화를 모델 선정이나 운영 승격으로 오해하지 않게 한다.
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
    write_bom_text(WORKSPACE_STATE, workspace)
    marker = f"run337IV {RUN_ID}"
    append_text_once(
        STAGE_BRIEF,
        marker,
        f"""## run337IV Positive Low-Edge Expansion Inputs(양수 낮은 엣지 확장 입력)

- run_id(실행 ID): `{RUN_ID}`
- judgment(판정): `{JUDGMENT}`
- rows(행): `{final['rows']}`
- task_seed_rows(작업 씨앗 행): `{final['task_seed_rows']}`
- next(다음): `{NEXT_RUN_ID}`
- effect(효과): 비용 압박 라벨과 학습 전용 가중치 7개를 만들었다.
""",
    )
    changelog_entry = f"""## {TODAY} run337IV Positive Low-Edge Expansion Inputs(양수 낮은 엣지 확장 입력)

- action(행동): IU 설계에서 train-only weight(학습 전용 가중치), cost-stress label(비용 압박 라벨), task seed(작업 씨앗)를 물질화했다.
- effect(효과): 다음 IW input review(입력 검토)가 누출과 포화를 확인할 수 있게 했다.
- boundary(경계): model training(모델 학습), MT5 execution(MT5 실행), selected model(선정 모델), Goal Achieve(목표 달성)는 없음.
"""
    append_text_once(ROOT_CHANGELOG, marker, changelog_entry)
    append_text_once(WORKSPACE_CHANGELOG, marker, changelog_entry)


def update_registers(final: Mapping[str, Any]) -> None:
    base = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "run_date": TODAY,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_run_id": NEXT_RUN_ID,
        "primary_artifact": rel(FINAL_DECISION),
        "report_path": rel(REPORT_PATH),
        "gate_passes": final["gate_passes"],
        "gate_total": final["gate_total"],
        "claim_boundary": CLAIM_BOUNDARY,
    }
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], base)
    rows = [
        {
            **base,
            "view": "Tier A separate(Tier A 분리)",
            "tier": "Tier A",
            "metric_scope": "input_materialization",
            "rows": final["rows"],
            "feature_count": final["feature_count"],
            "task_seed_rows": final["task_seed_rows"],
            "result_status": "inputs_materialized_review_required",
        },
        {
            **base,
            "view": "Tier B separate(Tier B 분리)",
            "tier": "Tier B",
            "metric_scope": "missing_required",
            "result_status": "missing_required",
        },
        {
            **base,
            "view": "Tier A+B combined(Tier A+B 합산)",
            "tier": "Tier A+B",
            "metric_scope": "missing_required",
            "result_status": "missing_required",
        },
    ]
    for row in rows:
        append_or_replace_csv(PROJECT_LEDGER, ["run_id", "view"], row)
        append_or_replace_csv(STAGE_LEDGER, ["run_id", "view"], row)


def main() -> None:
    for path in [RUN_DIR, REVIEW_DIR, DECISION_DOC.parent]:
        io(path).mkdir(parents=True, exist_ok=True)
    missing = [rel(path) for path in INPUT_FILES if not exists(path)]
    if missing:
        raise FileNotFoundError(f"missing required input files: {missing}")
    _frame, _allowed, source_map, recipe, weight_audit, feature_boundary, summary = materialize_frame()
    tasks = task_seeds()
    tiers, runtime_plan, queue = support_plans()
    write_csv(IV_SOURCE_MAP, source_map)
    write_csv(IV_WEIGHT_RECIPE, recipe)
    write_csv(IV_WEIGHT_AUDIT, weight_audit)
    write_csv(IV_FEATURE_BOUNDARY, feature_boundary)
    write_csv(IV_TASK_SEEDS, tasks)
    write_csv(IV_TIER_RECORDS, tiers)
    write_csv(IV_RUNTIME_COMPARISON_PLAN, runtime_plan)
    write_csv(IW_QUEUE, queue)
    working_summary = {
        **summary,
        "candidate_selection": "not_run",
        "model_training": "not_run",
        "mt5_execution": "not_run",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
    }
    gates = make_gates(working_summary, feature_boundary, weight_audit, tasks)
    write_csv(GATE_AUDIT, gates)
    write_receipts(working_summary, gates)
    final = write_final(working_summary, gates, tasks)
    write_docs(final)
    update_registers(final)
    update_artifact_registry(artifact_paths())
    failed = gates.loc[~gates["status"].astype(str).eq("passed")]
    if not failed.empty:
        raise RuntimeError(f"IV gates failed: {failed[['gate_id', 'status']].to_dict(orient='records')}")
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "rows": final["rows"],
                "feature_count": final["feature_count"],
                "new_weight_count": final["new_weight_count"],
                "task_seed_rows": final["task_seed_rows"],
                "cost_stress_valid_rows": final["cost_stress_valid_rows"],
                "max_weight_saturation_rate": final["max_weight_saturation_rate"],
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
