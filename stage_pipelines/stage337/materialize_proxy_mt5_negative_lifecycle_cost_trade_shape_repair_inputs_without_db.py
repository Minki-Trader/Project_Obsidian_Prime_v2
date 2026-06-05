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
    design_proxy_mt5_negative_lifecycle_cost_trade_shape_repair_without_db as im,
)


aw = im.aw

TODAY = "2026-06-01"
STAGE_ID = im.STAGE_ID
STAGE_DIR = im.STAGE_DIR
RUN_NUMBER = "run337IN"
RUN_ID = "run337IN_materialize_proxy_mt5_negative_lifecycle_cost_trade_shape_repair_inputs_without_db_v1"
PARENT_RUN_ID = im.RUN_ID
NEXT_RUN_ID = "run337IO_review_proxy_mt5_negative_lifecycle_cost_trade_shape_repair_inputs_without_db_v1"
STATUS = "completed_stage337IN_lifecycle_cost_trade_shape_repair_inputs_materialized_no_training_no_selection"
JUDGMENT = "timestamp_safe_lifecycle_cost_trade_shape_repair_inputs_materialized_review_required"
DECISION = "stage337IN_open_run337IO_review_lifecycle_cost_trade_shape_repair_inputs"
CLAIM_BOUNDARY = (
    "research_development_input_materialization_only_no_model_training_no_threshold_tuning_no_lot_optimization_"
    "no_candidate_selection_no_mt5_execution_no_forward_passed_no_forward_failed_no_live_readiness_"
    "no_operating_promotion_no_runtime_authority_no_goal_achieve"
)

RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEW_DIR / "run337IN_lifecycle_cost_repair_inputs.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage337IN_lifecycle_cost_trade_shape_repair_inputs.md"

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

BASE_INPUT_FRAME = STAGE_DIR / "02_runs" / "run337IF" / "if_runtime_positive_repair_input_frame.parquet"
BASE_ALLOWED_FEATURES = STAGE_DIR / "02_runs" / "run337IF" / "if_allowed_model_feature_set.csv"

IN_INPUT_FRAME = RUN_DIR / "in_lifecycle_cost_trade_shape_repair_input_frame.parquet"
IN_ALLOWED_FEATURES = RUN_DIR / "in_allowed_model_feature_set.csv"
IN_SOURCE_MAP = RUN_DIR / "in_materialization_source_map.csv"
IN_WEIGHT_RECIPE = RUN_DIR / "in_weight_recipe_matrix.csv"
IN_WEIGHT_AUDIT = RUN_DIR / "in_weight_audit.csv"
IN_FEATURE_BOUNDARY = RUN_DIR / "in_feature_label_boundary_audit.csv"
IN_TIER_RECORDS = RUN_DIR / "in_tier_record_plan.csv"
IN_RUNTIME_COMPARISON_PLAN = RUN_DIR / "in_runtime_comparison_plan.csv"
IN_TASK_SEEDS = RUN_DIR / "run337IO_training_task_seed_matrix.csv"
IO_QUEUE = RUN_DIR / "run337IO_review_queue.csv"
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

NEW_WEIGHT_COLUMNS = (
    "in_lifecycle_exit_compression_weight",
    "in_density_margin_throttle_weight",
    "in_cost_survival_edge_weight",
    "in_side_net_consistency_weight",
    "in_drawdown_session_regime_weight",
    "in_active_flat_reentry_weight",
    "in_lifecycle_cost_blend_weight",
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
FORBIDDEN_FEATURE_SUFFIXES = ("_weight", "_sample_weight")

INPUT_FILES = (
    im.FINAL_DECISION,
    im.GATE_AUDIT,
    im.DESIGN_MATRIX,
    im.ATTRIBUTION_MATRIX,
    im.EXPERIMENT_CONTRACT,
    im.FEATURE_LABEL_CONTRACT,
    im.RUNTIME_REUSE_CONTRACT,
    im.TIER_PAIR_CONTRACT,
    im.MATERIALIZATION_QUEUE,
    BASE_INPUT_FRAME,
    BASE_ALLOWED_FEATURES,
)
OUTPUT_FILES = (
    IN_INPUT_FRAME,
    IN_ALLOWED_FEATURES,
    IN_SOURCE_MAP,
    IN_WEIGHT_RECIPE,
    IN_WEIGHT_AUDIT,
    IN_FEATURE_BOUNDARY,
    IN_TIER_RECORDS,
    IN_RUNTIME_COMPARISON_PLAN,
    IN_TASK_SEEDS,
    IO_QUEUE,
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
    return pd.read_csv(io(path))


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


def rank01(values: pd.Series) -> pd.Series:
    clean = pd.to_numeric(values, errors="coerce").replace([np.inf, -np.inf], np.nan)
    if clean.notna().sum() == 0:
        return pd.Series(0.5, index=values.index, dtype="float64")
    return clean.rank(pct=True).fillna(0.5).astype("float64")


def clip_weight(values: pd.Series | np.ndarray, lower: float = 0.10, upper: float = 12.0) -> pd.Series:
    series = pd.Series(values).replace([np.inf, -np.inf], np.nan).fillna(1.0).astype("float64")
    return series.clip(lower=lower, upper=upper)


def feature_hash(features: Sequence[str]) -> str:
    return hashlib.sha256("\n".join(features).encode("utf-8")).hexdigest()


def forbidden_feature_violations(features: Sequence[str]) -> list[str]:
    violations = []
    train_only_weights = {column.lower() for column in NEW_WEIGHT_COLUMNS}
    for feature in features:
        lowered = feature.lower()
        token_hit = any(token in lowered for token in FORBIDDEN_FEATURE_TOKENS)
        weight_hit = lowered in train_only_weights or any(lowered.endswith(suffix) for suffix in FORBIDDEN_FEATURE_SUFFIXES)
        if token_hit or weight_hit:
            violations.append(feature)
    return violations


def materialize_frame() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, dict[str, Any]]:
    frame = pd.read_parquet(io(BASE_INPUT_FRAME)).copy()
    allowed = read_csv(BASE_ALLOWED_FEATURES).copy()
    feature_col = "feature_name" if "feature_name" in allowed.columns else allowed.columns[0]
    features = [str(item) for item in allowed[feature_col].dropna().tolist()]
    missing_features = [feature for feature in features if feature not in frame.columns]
    if missing_features:
        raise ValueError(f"missing allowed features: {missing_features}")

    f6 = num(frame, "hx_future_log_return_6")
    f18 = num(frame, "hx_future_log_return_18")
    f24 = num(frame, "hx_future_log_return_24")
    label18 = num(frame, "hx_label_class_fwd18", -1).astype(int)
    active = num(frame, "hx_active_flat_label", 0).astype(int)
    edge6 = f6.abs()
    edge18 = f18.abs()
    edge24 = f24.abs()
    sign6 = np.sign(f6)
    sign18 = np.sign(f18)
    conflict = pd.Series((sign6 != sign18) & (sign6 != 0) & (sign18 != 0), index=frame.index).astype("float64")
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
    class_counts = label18.value_counts().to_dict()
    class_weight = label18.map(lambda x: 1.0 / max(class_counts.get(int(x), 1), 1)).astype("float64")
    class_weight = class_weight / class_weight.mean()
    transition = active.ne(active.shift(1).fillna(active.iloc[0])).astype("float64")
    low_margin = rank01(num(frame, "low_margin_rate"))
    prob_margin = rank01(num(frame, "gz_probability_margin", 0.0).abs())

    frame["in_lifecycle_exit_compression_weight"] = clip_weight(
        0.70 + 3.2 * rank01((edge6 - edge18).abs()) + 2.2 * conflict + 1.2 * rank01((edge24 - edge18).abs())
    ).to_numpy()
    frame["in_density_margin_throttle_weight"] = clip_weight(
        0.55 + 6.0 * rank01(edge18) + 1.5 * (label18 != 1).astype("float64") + 1.2 * prob_margin - 1.5 * low_margin
    ).to_numpy()
    frame["in_cost_survival_edge_weight"] = clip_weight(
        0.45 + 7.0 * rank01(edge18) + 2.0 * (edge18 > edge18.quantile(0.75)).astype("float64")
    ).to_numpy()
    frame["in_side_net_consistency_weight"] = clip_weight(
        0.70 + 1.8 * class_weight + 3.2 * rank01(edge18) + 1.2 * (label18 != 1).astype("float64")
    ).to_numpy()
    frame["in_drawdown_session_regime_weight"] = clip_weight(
        0.65 + 3.0 * vol_pressure + 1.3 * session_edge + 2.5 * rank01(edge18 * (0.5 + vol_pressure))
    ).to_numpy()
    frame["in_active_flat_reentry_weight"] = clip_weight(
        0.70 + 3.5 * transition + 3.0 * (active == 1).astype("float64") * rank01(edge18) + 1.0 * (active == 0).astype("float64")
    ).to_numpy()
    frame["in_lifecycle_cost_blend_weight"] = clip_weight(
        frame[list(NEW_WEIGHT_COLUMNS[:-1])].mean(axis=1) * 1.15
    ).to_numpy()

    allowed["claim_boundary"] = CLAIM_BOUNDARY
    allowed["in_usage"] = "allowed_model_input_for_run337IO_review_and_run337IP_training(337IO 검토와 337IP 학습 허용 입력)"
    ensure_parent(IN_INPUT_FRAME)
    frame.to_parquet(io(IN_INPUT_FRAME), index=False)
    write_csv(IN_ALLOWED_FEATURES, allowed)

    source_map = pd.DataFrame(
        [
            {
                "source_id": "base_input_frame",
                "source_path": rel(BASE_INPUT_FRAME),
                "source_type": "parquet",
                "exists": exists(BASE_INPUT_FRAME),
                "sha256": sha(BASE_INPUT_FRAME),
                "effect": "IF 입력 프레임을 이어받아 새 학습 전용 가중치를 추가한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "source_id": "im_design_matrix",
                "source_path": rel(im.DESIGN_MATRIX),
                "source_type": "csv",
                "exists": exists(im.DESIGN_MATRIX),
                "sha256": sha(im.DESIGN_MATRIX),
                "effect": "IM 설계 축을 실제 입력 생성 규칙으로 연결한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ]
    )
    recipe = pd.DataFrame(
        [
            {
                "weight_column": column,
                "source_columns": "hx_future_log_return_6;hx_future_log_return_18;hx_future_log_return_24;hx_label_class_fwd18;hx_active_flat_label;timestamp-known context",
                "lower_bound": 0.10,
                "upper_bound": 12.0,
                "train_only_formula": "rank/label-weight formula; never allowed as model feature(순위/라벨 가중 공식, 모델 피처 금지)",
                "effect": "IM 수리 축을 학습 표본 압력으로 바꾼다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
            for column in NEW_WEIGHT_COLUMNS
        ]
    )
    audit_rows = []
    for column in NEW_WEIGHT_COLUMNS:
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
                "evidence": rel(IN_ALLOWED_FEATURES),
                "effect": "모델 입력 피처 수를 기존 58개로 고정한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "audit_id": "new_weights_excluded_from_features",
                "status": "passed" if not set(NEW_WEIGHT_COLUMNS).intersection(set(features)) else "failed",
                "observed": ";".join(sorted(set(NEW_WEIGHT_COLUMNS).intersection(set(features)))),
                "expected": "none(없음)",
                "evidence": rel(IN_ALLOWED_FEATURES),
                "effect": "학습 전용 가중치가 모델 피처로 새지 않게 한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "audit_id": "forbidden_feature_tokens",
                "status": "passed" if not forbidden_violations else "failed",
                "observed": ";".join(forbidden_violations),
                "expected": "none(없음)",
                "evidence": rel(IN_ALLOWED_FEATURES),
                "effect": "future/label/MT5 관련 열이 피처로 들어가지 않게 한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ]
    )
    summary = {
        "rows": int(len(frame)),
        "columns": int(len(frame.columns)),
        "feature_count": int(len(features)),
        "feature_order_hash": feature_hash(features),
        "new_weight_count": len(NEW_WEIGHT_COLUMNS),
        "weight_nonfinite_rows": int(weight_audit["nonfinite_rows"].sum()),
        "max_weight_saturation_rate": float(weight_audit["max_saturation_rate"].max()),
        "timestamp_min": str(pd.to_datetime(frame["timestamp"], utc=True).min()),
        "timestamp_max": str(pd.to_datetime(frame["timestamp"], utc=True).max()),
    }
    return frame, allowed, source_map, recipe, weight_audit, feature_boundary, summary


def task_seeds() -> pd.DataFrame:
    common = {
        "input_frame": rel(IN_INPUT_FRAME),
        "allowed_features": rel(IN_ALLOWED_FEATURES),
        "required_guard": "drop invalid rows; no threshold tuning; review before training(무효 행 제외, 임계값 조정 없음, 학습 전 검토)",
        "forbidden_use": "candidate selection, MT5 claim, runtime authority(후보 선택, MT5 주장, 런타임 권위)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    rows = [
        {
            "task_id": "in_im001_lifecycle_fwd6_lgbm",
            "repair_family": "lifecycle exit compression(생명주기 청산 압축)",
            "target_column": "hx_label_class_fwd6",
            "valid_column": "hx_valid_fwd6",
            "sample_weight_column": "in_lifecycle_exit_compression_weight",
            "model_family": "LightGBM(라이트GBM)_multiclass",
            "model_config_id": "lgbm_fwd6_lifecycle_exit_compression",
            "base_clue_model_id": "ih_if_ie003_pf_recovery_fwd18_xgboost",
            "expected_effect": "짧은 보유 생명주기 후보를 만든다.",
        },
        {
            "task_id": "in_im002_density_fwd18_lgbm",
            "repair_family": "density margin throttle(밀도 마진 제한)",
            "target_column": "hx_label_class_fwd18",
            "valid_column": "hx_valid_fwd18",
            "sample_weight_column": "in_density_margin_throttle_weight",
            "model_family": "LightGBM(라이트GBM)_multiclass",
            "model_config_id": "lgbm_fwd18_density_margin_throttle",
            "base_clue_model_id": "ih_if_ie003_pf_recovery_fwd18_xgboost",
            "expected_effect": "약한 edge(우위) 신호를 줄이는 후보를 만든다.",
        },
        {
            "task_id": "in_im003_cost_survival_fwd18_xgboost",
            "repair_family": "cost survival edge(비용 생존 우위)",
            "target_column": "hx_label_class_fwd18",
            "valid_column": "hx_valid_fwd18",
            "sample_weight_column": "in_cost_survival_edge_weight",
            "model_family": "XGBoost(엑스지부스트)_multiclass",
            "model_config_id": "xgboost_fwd18_cost_survival_edge",
            "base_clue_model_id": "ih_if_ie003_pf_recovery_fwd18_xgboost",
            "expected_effect": "비용에 견디는 두꺼운 edge(우위)를 찾는다.",
        },
        {
            "task_id": "in_im004_side_consistency_fwd18_extratrees",
            "repair_family": "side net consistency(방향 순수익 일관성)",
            "target_column": "hx_label_class_fwd18",
            "valid_column": "hx_valid_fwd18",
            "sample_weight_column": "in_side_net_consistency_weight",
            "model_family": "ExtraTrees(엑스트라트리스)_multiclass",
            "model_config_id": "extratrees_fwd18_side_net_consistency",
            "base_clue_model_id": "ih_if_ie003_pf_recovery_fwd18_xgboost",
            "expected_effect": "롱/숏 손실 비대칭을 줄이는 후보를 만든다.",
        },
        {
            "task_id": "in_im005_drawdown_session_fwd18_lgbm",
            "repair_family": "drawdown session regime(낙폭 세션 국면)",
            "target_column": "hx_label_class_fwd18",
            "valid_column": "hx_valid_fwd18",
            "sample_weight_column": "in_drawdown_session_regime_weight",
            "model_family": "LightGBM(라이트GBM)_multiclass",
            "model_config_id": "lgbm_fwd18_drawdown_session_regime",
            "base_clue_model_id": "ih_if_ie003_pf_recovery_fwd18_xgboost",
            "expected_effect": "낙폭/세션 취약 구간을 줄이는 후보를 만든다.",
        },
        {
            "task_id": "in_im006_active_flat_reentry_lgbm",
            "repair_family": "active flat reentry(활성/관망 재진입)",
            "target_column": "hx_active_flat_label",
            "valid_column": "hx_valid_fwd18",
            "sample_weight_column": "in_active_flat_reentry_weight",
            "model_family": "LightGBM(라이트GBM)_binary",
            "model_config_id": "lgbm_active_flat_reentry_shape",
            "base_clue_model_id": "ih_if_ie003_pf_recovery_fwd18_xgboost",
            "expected_effect": "활성/관망 전환과 재진입 비용을 줄이는 후보를 만든다.",
        },
        {
            "task_id": "in_im007_lifecycle_cost_blend_fwd18_xgboost",
            "repair_family": "lifecycle cost blend(생명주기 비용 혼합)",
            "target_column": "hx_label_class_fwd18",
            "valid_column": "hx_valid_fwd18",
            "sample_weight_column": "in_lifecycle_cost_blend_weight",
            "model_family": "XGBoost(엑스지부스트)_multiclass",
            "model_config_id": "xgboost_fwd18_lifecycle_cost_blend",
            "base_clue_model_id": "ih_if_ie003_pf_recovery_fwd18_xgboost",
            "expected_effect": "생명주기/비용/방향 수리를 함께 압박한다.",
        },
    ]
    return pd.DataFrame([{**row, **common} for row in rows])


def support_plans() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    tiers = pd.DataFrame(
        [
            {
                "tier_view": "Tier A separate(Tier A 분리)",
                "status": "materialized",
                "evidence": rel(IN_INPUT_FRAME),
                "effect": "전체 문맥 표본 입력을 물질화했다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "tier_view": "Tier B separate(Tier B 분리)",
                "status": "missing_required",
                "evidence": rel(IN_TIER_RECORDS),
                "effect": "부분 문맥 표본 누락을 생략하지 않는다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "tier_view": "Tier A+B combined(Tier A+B 합산)",
                "status": "missing_required",
                "evidence": rel(IN_TIER_RECORDS),
                "effect": "합산 입력이 없음을 명시한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ]
    )
    runtime = pd.DataFrame(
        [
            {
                "plan_id": "proxy_positive_requires_mt5_probe",
                "requirement": "Any later proxy-positive ONNX candidate must be compared with MT5 runtime probe(이후 프록시 양성 ONNX 후보는 MT5 런타임 탐침 비교 필수).",
                "evidence": rel(im.RUNTIME_REUSE_CONTRACT),
                "effect": "프록시 KPI가 MT5 KPI를 대체하지 못하게 한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )
    queue = pd.DataFrame(
        [
            {
                "next_run_id": NEXT_RUN_ID,
                "parent_run_id": RUN_ID,
                "queued_task": "review_lifecycle_cost_trade_shape_repair_inputs",
                "required_inputs": f"{rel(IN_INPUT_FRAME)};{rel(IN_WEIGHT_AUDIT)};{rel(IN_FEATURE_BOUNDARY)};{rel(IN_TASK_SEEDS)}",
                "expected_outputs": "eligibility matrix and training queue(적격성 행렬과 학습 대기열)",
                "blocked_if_missing": "input frame, finite weights, task seeds(입력 프레임, 유한 가중치, 작업 씨앗)",
                "effect": "학습 전에 입력 경계와 가중치 분포를 검토한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )
    return tiers, runtime, queue


def gate_row(gate: str, status: str, evidence: str, effect: str) -> dict[str, Any]:
    return {
        "gate_id": gate,
        "status": status,
        "evidence_path": evidence,
        "effect": effect,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def make_gates(summary: Mapping[str, Any], feature_boundary: pd.DataFrame, weight_audit: pd.DataFrame, tasks: pd.DataFrame) -> pd.DataFrame:
    parent_gates = read_csv(im.GATE_AUDIT)
    return pd.DataFrame(
        [
            gate_row(
                "parent_im_gates_passed",
                "passed" if parent_gates["status"].astype(str).str.lower().isin(["pass", "passed"]).all() else "failed",
                rel(im.GATE_AUDIT),
                "IM 설계 gate(게이트)가 통과된 뒤 입력을 만든다.",
            ),
            gate_row(
                "input_frame_materialized",
                "passed" if exists(IN_INPUT_FRAME) and summary["rows"] > 0 else "failed",
                rel(IN_INPUT_FRAME),
                "수리 입력 프레임을 생성했다.",
            ),
            gate_row(
                "allowed_feature_boundary_preserved",
                "passed" if feature_boundary["status"].astype(str).eq("passed").all() else "failed",
                rel(IN_FEATURE_BOUNDARY),
                "모델 피처 58개와 금지 토큰 경계를 지켰다.",
            ),
            gate_row(
                "new_weights_finite",
                "passed" if summary["weight_nonfinite_rows"] == 0 else "failed",
                rel(IN_WEIGHT_AUDIT),
                "새 학습 전용 가중치가 모두 유한하다.",
            ),
            gate_row(
                "weight_saturation_controlled",
                "passed" if summary["max_weight_saturation_rate"] <= 0.05 else "failed",
                rel(IN_WEIGHT_AUDIT),
                "가중치 상한 포화가 5% 이하인지 확인한다.",
            ),
            gate_row(
                "task_seed_matrix_written",
                "passed" if exists(IN_TASK_SEEDS) and len(tasks) >= 7 else "failed",
                rel(IN_TASK_SEEDS),
                "다음 검토/학습용 작업 씨앗을 만든다.",
            ),
            gate_row(
                "tier_pair_records_written",
                "passed" if exists(IN_TIER_RECORDS) else "failed",
                rel(IN_TIER_RECORDS),
                "Tier A/B/combined(티어 A/B/합산) 기록을 남긴다.",
            ),
            gate_row(
                "runtime_comparison_plan_written",
                "passed" if exists(IN_RUNTIME_COMPARISON_PLAN) else "failed",
                rel(IN_RUNTIME_COMPARISON_PLAN),
                "프록시 양성은 MT5 런타임 비교로 이어지게 한다.",
            ),
            gate_row(
                "next_review_queue_opened",
                "passed" if exists(IO_QUEUE) else "failed",
                rel(IO_QUEUE),
                "IO input review(입력 검토)를 연다.",
            ),
            gate_row(
                "no_forbidden_operating_claim",
                "passed",
                rel(CLAIM_RECEIPT),
                "학습, MT5 실행, 선택, 운영 주장을 하지 않는다.",
            ),
            gate_row(
                "required_gate_coverage_audit_written",
                "passed",
                rel(GATE_AUDIT),
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
        IN_INPUT_FRAME,
        IN_ALLOWED_FEATURES,
        IN_SOURCE_MAP,
        IN_WEIGHT_RECIPE,
        IN_WEIGHT_AUDIT,
        IN_FEATURE_BOUNDARY,
        IN_TIER_RECORDS,
        IN_RUNTIME_COMPARISON_PLAN,
        IN_TASK_SEEDS,
        IO_QUEUE,
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
            "time_axis": "bar close timestamp UTC inherited from IF(봉 마감 UTC 시각 상속)",
            "sample_scope": f"rows={summary['rows']}; {summary['timestamp_min']} to {summary['timestamp_max']}",
            "feature_label_boundary": "new weights are train-only and excluded from allowed model features(새 가중치는 학습 전용이며 모델 피처 제외)",
            "leakage_risk": "MT5 holdout result leakage guarded by feature boundary audit(MT5 보류 결과 누출은 피처 경계 감사로 차단)",
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
            "source_failure": "IL proxy-positive to MT5-negative exact parity(IL 프록시 양성에서 MT5 음수 정확 동등성)",
            "new_weight_count": summary["new_weight_count"],
            "max_weight_saturation_rate": summary["max_weight_saturation_rate"],
            "effect": "성과 실패를 학습 전용 가중치로 변환했다.",
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
            "input_frame": rel(IN_INPUT_FRAME),
            "task_seed_matrix": rel(IN_TASK_SEEDS),
            "consumer": NEXT_RUN_ID,
            "effect": "IM 설계와 IO 검토를 산출물 계보로 연결한다.",
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
    report = f"""# run337IN Lifecycle Cost Repair Inputs(run337IN 생명주기 비용 수리 입력)

## Summary(요약)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- judgment(판정): `{JUDGMENT}`
- gates(게이트): `{final['gate_passes']}/{final['gate_total']}`
- rows(행): `{final['rows']}`
- feature_count(피처 수): `{final['feature_count']}`
- new_weight_count(새 가중치 수): `{final['new_weight_count']}`
- task_seed_rows(작업 씨앗 행): `{final['task_seed_rows']}`
- max_weight_saturation_rate(최대 가중치 포화율): `{final['max_weight_saturation_rate']}`

## Action(행동)

IM design(설계)을 받아 train-only weight(학습 전용 가중치) 7개와 task seed(작업 씨앗) 7개를 만들었다.
Effect(효과): lifecycle/cost/side/drawdown(생명주기/비용/방향/낙폭) 수리 후보를 학습 전 검토할 수 있게 했다.

## Boundary(경계)

No model training(모델 학습 없음), no MT5 execution(MT5 실행 없음), no selected model(선정 모델 없음), no Goal Achieve(목표 달성 없음).

## Next(다음)

`{NEXT_RUN_ID}`에서 input review(입력 검토)를 수행한다.
"""
    decision = f"""# {TODAY} Stage337IN Decision(337IN 결정)

- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- evidence(근거): `{rel(IN_INPUT_FRAME)}`, `{rel(IN_WEIGHT_AUDIT)}`, `{rel(IN_TASK_SEEDS)}`

Action(행동): timestamp-safe(시점 안전) 수리 입력을 물질화했다.
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

IN materialization(입력 물질화)은 새 수리 가중치와 task seed(작업 씨앗)를 만들었다.
효과는 IO review(검토)가 모델 학습 전에 누출, 포화, 피처 경계를 확인하게 하는 것이다.

## Claim Boundary(주장 경계)

`{CLAIM_BOUNDARY}`
"""
    selection = f"""# Stage337 Selection Status(337단계 선택 상태)

- latest_run(최신 실행): `{RUN_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- selected_model(선정 모델): `none(없음)`
- repair_status(수리 상태): `inputs_materialized_review_required(입력 물질화, 검토 필요)`
- runtime_authority(런타임 권위): `not_claimed(주장 안 함)`
- operating_promotion(운영 승격): `not_claimed(주장 안 함)`
- goal_achieve(목표 달성): `not_claimed(주장 안 함)`

Effect(효과): 입력 물질화를 모델 선정으로 오해하지 않게 한다.
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
    marker = f"run337IN {RUN_ID}"
    append_text_once(
        STAGE_BRIEF,
        marker,
        f"""## run337IN Lifecycle Cost Repair Inputs(생명주기 비용 수리 입력)

- run_id(실행 ID): `{RUN_ID}`
- judgment(판정): `{JUDGMENT}`
- next(다음): `{NEXT_RUN_ID}`
- effect(효과): 시점 안전 수리 가중치 7개와 학습 작업 씨앗 7개를 만들었다.
""",
    )
    changelog_entry = f"""## {TODAY} run337IN Lifecycle Cost Repair Inputs(생명주기 비용 수리 입력)

- action(행동): IM 설계에서 train-only weight(학습 전용 가중치)와 task seed(작업 씨앗)를 물질화했다.
- effect(효과): 다음 IO input review(입력 검토)가 누출과 포화를 확인할 수 있게 했다.
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
    write_csv(IN_SOURCE_MAP, source_map)
    write_csv(IN_WEIGHT_RECIPE, recipe)
    write_csv(IN_WEIGHT_AUDIT, weight_audit)
    write_csv(IN_FEATURE_BOUNDARY, feature_boundary)
    write_csv(IN_TIER_RECORDS, tiers)
    write_csv(IN_RUNTIME_COMPARISON_PLAN, runtime_plan)
    write_csv(IN_TASK_SEEDS, tasks)
    write_csv(IO_QUEUE, queue)
    gates = make_gates(summary, feature_boundary, weight_audit, tasks)
    write_csv(GATE_AUDIT, gates)
    write_receipts(summary, gates)
    final = write_final(summary, gates, tasks)
    write_docs(final)
    update_registers(final)
    update_artifact_registry(artifact_paths())
    failed = gates.loc[~gates["status"].astype(str).eq("passed")]
    if not failed.empty:
        raise RuntimeError(f"IN gates failed: {failed[['gate_id', 'status']].to_dict(orient='records')}")
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
