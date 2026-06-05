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
    design_runtime_negative_collapse_cost_stress_trade_shape_repair_without_db as jc,
)
from stage_pipelines.stage337 import (  # noqa: E402
    materialize_lifecycle_cost_positive_low_edge_cost_stress_trade_shape_expansion_inputs_without_db as iv,
)


aw = jc.aw

TODAY = "2026-06-01"
STAGE_ID = jc.STAGE_ID
STAGE_DIR = jc.STAGE_DIR
RUN_NUMBER = "run337JD"
RUN_ID = "run337JD_materialize_runtime_negative_collapse_cost_stress_trade_shape_repair_inputs_without_db_v1"
PARENT_RUN_ID = jc.RUN_ID
NEXT_RUN_ID = "run337JE_review_runtime_negative_collapse_cost_stress_trade_shape_repair_inputs_without_db_v1"
STATUS = "completed_stage337JD_runtime_negative_collapse_repair_inputs_materialized_no_training_no_selection"
JUDGMENT = "timestamp_safe_runtime_negative_collapse_repair_inputs_materialized_review_required"
DECISION = "stage337JD_open_run337JE_review_runtime_negative_collapse_repair_inputs"
CLAIM_BOUNDARY = (
    "research_development_input_materialization_only_no_model_training_no_threshold_tuning_no_lot_optimization_"
    "no_candidate_selection_no_mt5_execution_no_forward_passed_no_forward_failed_no_live_readiness_"
    "no_operating_promotion_no_runtime_authority_no_goal_achieve"
)

RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEW_DIR / "run337JD_runtime_negative_collapse_repair_inputs.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage337JD_runtime_negative_collapse_repair_inputs.md"

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

BASE_INPUT_FRAME = iv.IV_INPUT_FRAME
BASE_ALLOWED_FEATURES = iv.IV_ALLOWED_FEATURES

JD_INPUT_FRAME = RUN_DIR / "jd_runtime_negative_collapse_repair_input_frame.parquet"
JD_ALLOWED_FEATURES = RUN_DIR / "jd_allowed_model_feature_set.csv"
JD_SOURCE_MAP = RUN_DIR / "jd_source_map.csv"
JD_WEIGHT_RECIPE = RUN_DIR / "jd_weight_recipe_matrix.csv"
JD_WEIGHT_AUDIT = RUN_DIR / "jd_weight_audit.csv"
JD_FEATURE_BOUNDARY = RUN_DIR / "jd_feature_label_boundary_audit.csv"
JD_TASK_SEEDS = RUN_DIR / "run337JE_training_task_seed_matrix.csv"
JD_TIER_RECORDS = RUN_DIR / "jd_tier_records.csv"
JD_RUNTIME_COMPARISON_PLAN = RUN_DIR / "jd_runtime_comparison_plan.csv"
JE_QUEUE = RUN_DIR / "run337JE_input_review_queue.csv"
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

JD_WEIGHT_COLUMNS = (
    "jd_runtime_pnl_proxy_weight",
    "jd_entry_margin_entropy_throttle_weight",
    "jd_side_long_rescue_short_preserve_weight",
    "jd_lifecycle_exit_drawdown_compression_weight",
    "jd_cost_buffer_survival_weight",
    "jd_order_churn_exposure_penalty_weight",
    "jd_session_regime_loss_firewall_weight",
    "jd_blended_runtime_negative_repair_weight",
)
JD_TARGET_COLUMNS = (
    "jd_label_class_runtime_pnl_fwd18",
    "jd_valid_runtime_pnl_fwd18",
)
FORBIDDEN_FEATURE_TOKENS = (
    "label",
    "future",
    "target",
    "mt5",
    "profit",
    "expectancy",
    "recovery",
    "telemetry",
)
FORBIDDEN_FEATURE_SUFFIXES = ("_weight", "_sample_weight")

INPUT_FILES = (
    jc.FINAL_DECISION,
    jc.GATE_AUDIT,
    jc.DESIGN_MATRIX,
    jc.ATTRIBUTION_MATRIX,
    jc.EXPERIMENT_CONTRACT,
    jc.DATA_INTEGRITY_CONTRACT,
    jc.FEATURE_LABEL_TRADE_CONTRACT,
    jc.RUNTIME_PARITY_GUARD,
    jc.TIER_PAIR_CONTRACT,
    jc.MATERIALIZATION_QUEUE,
    BASE_INPUT_FRAME,
    BASE_ALLOWED_FEATURES,
)
OUTPUT_FILES = (
    JD_INPUT_FRAME,
    JD_ALLOWED_FEATURES,
    JD_SOURCE_MAP,
    JD_WEIGHT_RECIPE,
    JD_WEIGHT_AUDIT,
    JD_FEATURE_BOUNDARY,
    JD_TASK_SEEDS,
    JD_TIER_RECORDS,
    JD_RUNTIME_COMPARISON_PLAN,
    JE_QUEUE,
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


def display_path(path: Path | str) -> str:
    value = Path(path)
    try:
        if str(value.resolve()).lower().startswith(str(ROOT.resolve()).lower()):
            return rel(value)
    except OSError:
        pass
    return value.as_posix()


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
    train_only = {column.lower() for column in [*JD_WEIGHT_COLUMNS, *JD_TARGET_COLUMNS]}
    for feature in features:
        lowered = feature.lower()
        token_hit = any(token in lowered for token in FORBIDDEN_FEATURE_TOKENS)
        weight_hit = lowered in train_only or any(lowered.endswith(suffix) for suffix in FORBIDDEN_FEATURE_SUFFIXES)
        if token_hit or weight_hit:
            violations.append(feature)
    return violations


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


def runtime_pnl_label(frame: pd.DataFrame) -> pd.DataFrame:
    f18 = num(frame, "hx_future_log_return_18", np.nan)
    valid18 = num(frame, "hx_valid_fwd18", 0).astype(int).eq(1) & f18.notna()
    vol_pressure = (
        rank01(num(frame, "historical_vol_5_over_20").abs())
        + rank01(num(frame, "atr_14_over_atr_50").abs())
        + rank01(num(frame, "hl_zscore_50").abs())
    ) / 3.0
    low_margin = rank01(num(frame, "low_margin_rate", 0.0))
    buffer = 0.0010 + 0.00055 * vol_pressure + 0.00045 * low_margin
    label = np.select([f18 > buffer, f18 < -buffer], [2, 0], default=1).astype(int)
    label = pd.Series(label, index=frame.index)
    label.loc[~valid18] = -1
    frame["jd_label_class_runtime_pnl_fwd18"] = label.astype(int).to_numpy()
    frame["jd_valid_runtime_pnl_fwd18"] = valid18.astype(int).to_numpy()
    return frame


def materialize_frame() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, dict[str, Any]]:
    parent = read_json(jc.FINAL_DECISION)
    frame = pd.read_parquet(io(BASE_INPUT_FRAME)).copy()
    allowed = read_csv(BASE_ALLOWED_FEATURES).copy()
    feature_col = "feature_name" if "feature_name" in allowed.columns else allowed.columns[0]
    features = [str(item) for item in allowed[feature_col].dropna().tolist()]
    missing_features = [feature for feature in features if feature not in frame.columns]
    if missing_features:
        raise ValueError(f"missing allowed features: {missing_features}")

    frame = runtime_pnl_label(frame)
    f6 = num(frame, "hx_future_log_return_6", np.nan)
    f18 = num(frame, "hx_future_log_return_18", np.nan)
    f24 = num(frame, "hx_future_log_return_24", np.nan)
    label18 = num(frame, "hx_label_class_fwd18", -1).astype(int)
    runtime_label = num(frame, "jd_label_class_runtime_pnl_fwd18", -1).astype(int)
    abs6 = f6.abs().fillna(0.0)
    abs18 = f18.abs().fillna(0.0)
    abs24 = f24.abs().fillna(0.0)
    sign6 = np.sign(f6.fillna(0.0))
    sign18 = np.sign(f18.fillna(0.0))
    sign24 = np.sign(f24.fillna(0.0))
    sign_consistency = pd.Series(((sign6 == sign18) & (sign18 == sign24) & (sign18 != 0)).astype("float64"), index=frame.index)
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
    probability_margin, probability_entropy = probability_context(frame)
    low_margin = rank01(num(frame, "low_margin_rate", 0.0))
    drawdown_pressure = rank01(num(frame, "drawdown_pressure_norm", 0.0))
    cost_adverse = rank01(num(frame, "gz_cost_adverse_risk", num(frame, "low_margin_rate", 0.0)))
    churn_pressure = rank01(num(frame, "gz_trade_churn_pressure", 0.0) + num(frame, "hh_trade_churn_pressure", 0.0))
    worst_forward = pd.Series(np.maximum.reduce([(-f6).fillna(0.0), (-f18).fillna(0.0), (-f24).fillna(0.0)]), index=frame.index)
    cost_edge = (abs18 - (0.0010 + 0.0004 * vol_pressure + 0.0004 * low_margin)).clip(lower=0.0)
    long_good = label18.eq(2).astype("float64") * rank01(f18.clip(lower=0.0).fillna(0.0))
    short_good = label18.eq(0).astype("float64") * rank01((-f18).clip(lower=0.0).fillna(0.0))

    frame["jd_runtime_pnl_proxy_weight"] = clip_weight(
        0.35 + 5.0 * rank01(cost_edge) + 2.0 * runtime_label.ne(1).astype("float64") + 1.5 * rank01(probability_margin) - 1.2 * low_margin
    ).to_numpy()
    frame["jd_entry_margin_entropy_throttle_weight"] = clip_weight(
        0.30 + 4.5 * rank01(probability_margin) + 2.5 * (1.0 - rank01(probability_entropy)) + 1.5 * rank01(abs18) - 1.4 * low_margin
    ).to_numpy()
    frame["jd_side_long_rescue_short_preserve_weight"] = clip_weight(
        0.60 + 3.3 * long_good + 2.5 * short_good + 1.2 * runtime_label.ne(1).astype("float64") + 0.8 * sign_consistency
    ).to_numpy()
    frame["jd_lifecycle_exit_drawdown_compression_weight"] = clip_weight(
        0.55 + 3.2 * rank01(abs6) + 2.0 * sign_consistency - 1.4 * conflict + 1.8 * rank01(worst_forward.clip(lower=0.0))
    ).to_numpy()
    frame["jd_cost_buffer_survival_weight"] = clip_weight(
        0.35 + 5.0 * rank01(cost_edge) + 2.5 * cost_adverse + 1.5 * runtime_label.ne(1).astype("float64")
    ).to_numpy()
    frame["jd_order_churn_exposure_penalty_weight"] = clip_weight(
        0.45 + 4.0 * (1.0 - churn_pressure) + 2.0 * rank01(probability_margin) + 1.2 * runtime_label.ne(1).astype("float64")
    ).to_numpy()
    frame["jd_session_regime_loss_firewall_weight"] = clip_weight(
        0.50 + 2.4 * vol_pressure + 2.2 * drawdown_pressure + 1.3 * session_edge + 1.5 * rank01(abs18 * (0.5 + vol_pressure))
    ).to_numpy()
    frame["jd_blended_runtime_negative_repair_weight"] = clip_weight(
        frame[list(JD_WEIGHT_COLUMNS[:-1])].mean(axis=1) * 1.10
    ).to_numpy()

    allowed["claim_boundary"] = CLAIM_BOUNDARY
    allowed["jd_usage"] = "allowed_model_input_for_run337JE_review_and_later_training(337JE 검토와 이후 학습 허용 입력)"
    ensure_parent(JD_INPUT_FRAME)
    frame.to_parquet(io(JD_INPUT_FRAME), index=False)
    write_csv(JD_ALLOWED_FEATURES, allowed)

    source_map = pd.DataFrame(
        [
            {"source_id": "base_iv_input_frame", "source_path": rel(BASE_INPUT_FRAME), "exists": exists(BASE_INPUT_FRAME), "sha256": sha(BASE_INPUT_FRAME), "effect": "IV 입력 frame(프레임)을 이어받아 JD train-only(학습 전용) 라벨/가중치를 추가한다.", "claim_boundary": CLAIM_BOUNDARY},
            {"source_id": "jc_design_matrix", "source_path": rel(jc.DESIGN_MATRIX), "exists": exists(jc.DESIGN_MATRIX), "sha256": sha(jc.DESIGN_MATRIX), "effect": "JC 설계 축을 실제 입력 생성 규칙으로 연결한다.", "claim_boundary": CLAIM_BOUNDARY},
            {"source_id": "jb_runtime_failure_memory", "source_path": rel(jc.jb.FAILURE_MEMORY_AND_NEXT_SEED), "exists": exists(jc.jb.FAILURE_MEMORY_AND_NEXT_SEED), "sha256": sha(jc.jb.FAILURE_MEMORY_AND_NEXT_SEED), "effect": "MT5 음성 붕괴 실패 기억을 학습 제약으로 연결한다.", "claim_boundary": CLAIM_BOUNDARY},
        ]
    )
    recipe = pd.DataFrame(
        [
            {
                "weight_column": column,
                "source_columns": "hx_future_log_return_6;hx_future_log_return_18;hx_future_log_return_24;probability_context;cost/drawdown/churn/session pretrade context",
                "lower_bound": 0.10,
                "upper_bound": 12.0,
                "train_only_formula": "rank/label/cost/lifecycle formula; never allowed as model feature(순위/라벨/비용/생명주기 공식, 모델 피처 금지)",
                "effect": "JC 설계를 학습 표본 압력으로 바꾼다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
            for column in JD_WEIGHT_COLUMNS
        ]
    )
    audit_rows = []
    for column in JD_WEIGHT_COLUMNS:
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

    feature_violations = forbidden_feature_violations(features)
    feature_boundary = pd.DataFrame(
        [
            {"check_id": "jd_allowed_feature_count", "status": "passed" if len(features) == 58 else "failed", "observed": len(features), "expected": 58, "evidence": rel(JD_ALLOWED_FEATURES), "effect": "기존 pretrade feature(사전거래 피처) 수를 유지한다.", "claim_boundary": CLAIM_BOUNDARY},
            {"check_id": "jd_missing_allowed_features", "status": "passed" if not missing_features else "failed", "observed": ";".join(missing_features), "expected": "none(없음)", "evidence": rel(JD_INPUT_FRAME), "effect": "허용 feature(피처)가 모두 frame(프레임)에 있는지 확인한다.", "claim_boundary": CLAIM_BOUNDARY},
            {"check_id": "jd_no_train_only_feature_leakage", "status": "passed" if not feature_violations else "failed", "observed": ";".join(feature_violations), "expected": "none(없음)", "evidence": rel(JD_ALLOWED_FEATURES), "effect": "label/weight/MT5(라벨/가중치/MT5) 누수를 막는다.", "claim_boundary": CLAIM_BOUNDARY},
            {"check_id": "jd_target_columns_train_only", "status": "passed" if set(JD_TARGET_COLUMNS).issubset(frame.columns) else "failed", "observed": ";".join([c for c in JD_TARGET_COLUMNS if c in frame.columns]), "expected": ";".join(JD_TARGET_COLUMNS), "evidence": rel(JD_INPUT_FRAME), "effect": "새 target(목표)을 학습 전용으로 만든다.", "claim_boundary": CLAIM_BOUNDARY},
        ]
    )
    tasks = pd.DataFrame(
        [
            {"task_id": "jd_jc001_runtime_pnl_fwd18_xgboost", "repair_family": "runtime PnL proxy(런타임 손익 프록시)", "target_column": "jd_label_class_runtime_pnl_fwd18", "valid_column": "jd_valid_runtime_pnl_fwd18", "sample_weight_column": "jd_runtime_pnl_proxy_weight", "model_family": "XGBoost(엑스지부스트)_multiclass", "model_config_id": "xgboost_fwd18_runtime_pnl_proxy", "base_clue_model_id": "ix_iv_iu001_cost_stress_fwd18_xgboost", "expected_effect": "MT5 손익 형태를 proxy(프록시)에 가깝게 반영한다."},
            {"task_id": "jd_jc002_entry_throttle_fwd18_lgbm", "repair_family": "entry throttle(진입 제한)", "target_column": "jd_label_class_runtime_pnl_fwd18", "valid_column": "jd_valid_runtime_pnl_fwd18", "sample_weight_column": "jd_entry_margin_entropy_throttle_weight", "model_family": "LightGBM(라이트GBM)_multiclass", "model_config_id": "lgbm_fwd18_entry_margin_entropy", "base_clue_model_id": "ix_iv_iu001_cost_stress_fwd18_xgboost", "expected_effect": "약한 진입을 줄여 비용 붕괴를 낮춘다."},
            {"task_id": "jd_jc003_side_repair_fwd18_extratrees", "repair_family": "side net repair(방향 순수익 수리)", "target_column": "hx_label_class_fwd18", "valid_column": "hx_valid_fwd18", "sample_weight_column": "jd_side_long_rescue_short_preserve_weight", "model_family": "ExtraTrees(엑스트라트리즈)_multiclass", "model_config_id": "extratrees_fwd18_side_repair", "base_clue_model_id": "ix_iv_iu001_cost_stress_fwd18_xgboost", "expected_effect": "약한 롱과 강한 숏을 분리한다."},
            {"task_id": "jd_jc004_lifecycle_exit_fwd6_xgboost", "repair_family": "lifecycle exit(생명주기 청산)", "target_column": "hx_label_class_fwd6", "valid_column": "hx_valid_fwd6", "sample_weight_column": "jd_lifecycle_exit_drawdown_compression_weight", "model_family": "XGBoost(엑스지부스트)_multiclass", "model_config_id": "xgboost_fwd6_lifecycle_exit", "base_clue_model_id": "ix_iv_iu001_cost_stress_fwd18_xgboost", "expected_effect": "보유 손실과 낙폭을 줄인다."},
            {"task_id": "jd_jc005_cost_buffer_fwd18_lgbm", "repair_family": "cost buffer(비용 버퍼)", "target_column": "jd_label_class_runtime_pnl_fwd18", "valid_column": "jd_valid_runtime_pnl_fwd18", "sample_weight_column": "jd_cost_buffer_survival_weight", "model_family": "LightGBM(라이트GBM)_multiclass", "model_config_id": "lgbm_fwd18_cost_buffer", "base_clue_model_id": "ix_iv_iu001_cost_stress_fwd18_xgboost", "expected_effect": "비용을 견디는 edge(우위)만 남긴다."},
            {"task_id": "jd_jc006_order_churn_fwd18_extratrees", "repair_family": "order churn(주문 회전)", "target_column": "jd_label_class_runtime_pnl_fwd18", "valid_column": "jd_valid_runtime_pnl_fwd18", "sample_weight_column": "jd_order_churn_exposure_penalty_weight", "model_family": "ExtraTrees(엑스트라트리즈)_multiclass", "model_config_id": "extratrees_fwd18_order_churn", "base_clue_model_id": "ix_iv_iu001_cost_stress_fwd18_xgboost", "expected_effect": "잦은 재진입 비용을 줄인다."},
            {"task_id": "jd_jc007_session_regime_fwd18_xgboost", "repair_family": "session regime firewall(세션/국면 방화벽)", "target_column": "hx_label_class_fwd18", "valid_column": "hx_valid_fwd18", "sample_weight_column": "jd_session_regime_loss_firewall_weight", "model_family": "XGBoost(엑스지부스트)_multiclass", "model_config_id": "xgboost_fwd18_session_regime", "base_clue_model_id": "ix_iv_iu001_cost_stress_fwd18_xgboost", "expected_effect": "국면별 손실 군집을 줄인다."},
            {"task_id": "jd_jc008_blended_repair_fwd18_lgbm", "repair_family": "blended runtime repair(혼합 런타임 수리)", "target_column": "jd_label_class_runtime_pnl_fwd18", "valid_column": "jd_valid_runtime_pnl_fwd18", "sample_weight_column": "jd_blended_runtime_negative_repair_weight", "model_family": "LightGBM(라이트GBM)_multiclass", "model_config_id": "lgbm_fwd18_blended_runtime_repair", "base_clue_model_id": "ix_iv_iu001_cost_stress_fwd18_xgboost", "expected_effect": "단일 축 과적합을 줄인다."},
        ]
    )
    tasks["input_frame"] = rel(JD_INPUT_FRAME)
    tasks["allowed_features"] = rel(JD_ALLOWED_FEATURES)
    tasks["required_guard"] = "drop invalid rows; no threshold tuning; review before training(무효 행 제외, 임계값 조정 없음, 학습 전 검토)"
    tasks["forbidden_use"] = "candidate selection, MT5 claim, runtime authority(후보 선택, MT5 주장, 런타임 권위)"
    tasks["claim_boundary"] = CLAIM_BOUNDARY

    tier_records = pd.DataFrame(
        [
            {"view": "Tier A separate(Tier A 분리)", "tier": "Tier A", "status": "materialized", "evidence_path": rel(JD_INPUT_FRAME), "rows": len(frame), "claim_boundary": CLAIM_BOUNDARY},
            {"view": "Tier B separate(Tier B 분리)", "tier": "Tier B", "status": "missing_required", "evidence_path": rel(JD_TIER_RECORDS), "rows": "", "claim_boundary": CLAIM_BOUNDARY},
            {"view": "Tier A+B combined(Tier A+B 합산)", "tier": "Tier A+B", "status": "missing_required", "evidence_path": rel(JD_TIER_RECORDS), "rows": "", "claim_boundary": CLAIM_BOUNDARY},
        ]
    )
    runtime_plan = pd.DataFrame(
        [
            {
                "plan_id": "jd_proxy_mt5_runtime_required",
                "requirement": "proxy-positive candidates must be compared with MT5 runtime probe(프록시 양성 후보는 MT5 런타임 탐침과 비교 필수)",
                "proxy_does_not_replace_mt5": True,
                "expected_next_runtime_step": "training review -> runtime package -> MT5 probe(학습 검토 -> 런타임 패키지 -> MT5 탐침)",
                "effect": "proxy(프록시) 수익을 MT5 KPI(MT5 핵심 성과 지표)로 착각하지 않게 한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )
    queue = pd.DataFrame(
        [
            {
                "queue_id": "je_review_runtime_negative_collapse_repair_inputs",
                "next_run_id": NEXT_RUN_ID,
                "parent_run_id": RUN_ID,
                "required_inputs": f"{rel(JD_INPUT_FRAME)};{rel(JD_WEIGHT_AUDIT)};{rel(JD_FEATURE_BOUNDARY)};{rel(JD_TASK_SEEDS)}",
                "required_outputs": "input review matrix and task eligibility(입력 검토 행렬과 작업 적격성)",
                "forbidden_action": "start training before review(검토 전 학습 시작)",
                "effect": "JD 산출물을 학습 전 검토로 넘긴다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )
    summary = {
        "rows": int(len(frame)),
        "columns": int(len(frame.columns)),
        "feature_count": int(len(features)),
        "feature_order_hash": feature_hash(features),
        "missing_feature_count": int(len(missing_features)),
        "feature_boundary_failures": int((feature_boundary["status"] != "passed").sum()),
        "weight_count": int(len(JD_WEIGHT_COLUMNS)),
        "weight_nonfinite_rows": int(weight_audit["nonfinite_rows"].sum()),
        "max_weight_saturation_rate": float(weight_audit["max_saturation_rate"].max()),
        "target_valid_rows": int(num(frame, "jd_valid_runtime_pnl_fwd18").sum()),
        "target_class_count": int(num(frame, "jd_label_class_runtime_pnl_fwd18").loc[lambda s: s.isin([0, 1, 2])].nunique()),
        "target_class_counts": {str(k): int(v) for k, v in frame["jd_label_class_runtime_pnl_fwd18"].value_counts().sort_index().to_dict().items()},
        "task_seed_rows": int(len(tasks)),
        "tier_record_rows": int(len(tier_records)),
        "runtime_plan_rows": int(len(runtime_plan)),
        "input_frame": rel(JD_INPUT_FRAME),
        "allowed_features": rel(JD_ALLOWED_FEATURES),
        "next_action": NEXT_RUN_ID,
    }
    return source_map, recipe, weight_audit, feature_boundary, tasks, tier_records, runtime_plan, queue, summary


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


def make_gates(summary: Mapping[str, Any]) -> pd.DataFrame:
    parent_gates = read_csv(jc.GATE_AUDIT)
    return pd.DataFrame(
        [
            gate_row("parent_jc_gates_passed", "passed" if passed_status(parent_gates["status"]).all() else "failed", rel(jc.GATE_AUDIT), "all passed", "all passed", "JC 설계 통과 뒤 물질화한다."),
            gate_row("input_frame_written", "passed" if exists(JD_INPUT_FRAME) and summary["rows"] >= 87600 else "failed", rel(JD_INPUT_FRAME), summary["rows"], ">=87600", "입력 frame(프레임)을 손실 없이 생성한다."),
            gate_row("allowed_feature_count_preserved", "passed" if summary["feature_count"] == 58 else "failed", rel(JD_ALLOWED_FEATURES), summary["feature_count"], 58, "기존 58개 pretrade feature(사전거래 피처)를 유지한다."),
            gate_row("feature_boundary_passed", "passed" if summary["feature_boundary_failures"] == 0 else "failed", rel(JD_FEATURE_BOUNDARY), summary["feature_boundary_failures"], 0, "feature/label boundary(피처/라벨 경계)를 지킨다."),
            gate_row("weight_columns_materialized", "passed" if summary["weight_count"] == len(JD_WEIGHT_COLUMNS) else "failed", rel(JD_WEIGHT_AUDIT), summary["weight_count"], len(JD_WEIGHT_COLUMNS), "학습 전용 가중치를 모두 만든다."),
            gate_row("weights_finite", "passed" if summary["weight_nonfinite_rows"] == 0 else "failed", rel(JD_WEIGHT_AUDIT), summary["weight_nonfinite_rows"], 0, "비유한 가중치를 막는다."),
            gate_row("weight_saturation_controlled", "passed" if summary["max_weight_saturation_rate"] <= 0.20 else "failed", rel(JD_WEIGHT_AUDIT), summary["max_weight_saturation_rate"], "<=0.20", "가중치 과포화를 막는다."),
            gate_row("runtime_pnl_label_distribution", "passed" if summary["target_valid_rows"] > 85000 and summary["target_class_count"] == 3 else "failed", rel(JD_INPUT_FRAME), f"valid={summary['target_valid_rows']};classes={summary['target_class_count']}", "valid>85000;classes=3", "새 runtime PnL label(런타임 손익 라벨)이 학습 가능한지 확인한다."),
            gate_row("task_seeds_written", "passed" if exists(JD_TASK_SEEDS) and summary["task_seed_rows"] >= 8 else "failed", rel(JD_TASK_SEEDS), summary["task_seed_rows"], ">=8", "다음 학습 후보를 충분히 연다."),
            gate_row("tier_pair_records_written", "passed" if exists(JD_TIER_RECORDS) and summary["tier_record_rows"] == 3 else "failed", rel(JD_TIER_RECORDS), summary["tier_record_rows"], 3, "Tier A/B 기록을 생략하지 않는다."),
            gate_row("runtime_comparison_plan_written", "passed" if exists(JD_RUNTIME_COMPARISON_PLAN) and summary["runtime_plan_rows"] >= 1 else "failed", rel(JD_RUNTIME_COMPARISON_PLAN), summary["runtime_plan_rows"], ">=1", "proxy-MT5 비교 필수 조건을 남긴다."),
            gate_row("review_queue_written", "passed" if exists(JE_QUEUE) else "failed", rel(JE_QUEUE), exists(JE_QUEUE), "true", "JE 입력 검토로 연결한다."),
            gate_row("required_gate_coverage_audit_written", "passed", rel(GATE_AUDIT), "written", "written", "gate coverage(게이트 커버리지)를 closeout(종료 기록)에 연결한다."),
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
    return list(OUTPUT_FILES)


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
                    "path": display_path(path),
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
    write_json(RUN_EVIDENCE_RECEIPT, {**base, "input_frame": rel(JD_INPUT_FRAME), "task_seed_matrix": rel(JD_TASK_SEEDS), "gate_passes": int(gates["status"].astype(str).eq("passed").sum()), "gate_total": int(len(gates)), "effect": "JD 입력 산출물을 JE review(JE 검토)로 넘긴다."})
    write_json(DATA_RECEIPT, {**base, "data_source": rel(BASE_INPUT_FRAME), "time_axis": "UTC closed-bar timestamp(UTC 봉 마감 시각)", "sample_scope": "Tier A full-context plus missing_required Tier B(Tier A 전체 문맥, Tier B 필수 누락)", "missing_or_duplicate_check": rel(JD_FEATURE_BOUNDARY), "feature_label_boundary": rel(JD_FEATURE_BOUNDARY), "split_boundary": "source_row_id ordered inner split(source_row_id 순서 내부 분할)", "leakage_risk": "train-only labels/weights leaking into allowed features(학습 전용 라벨/가중치가 허용 피처로 누수)", "data_hash_or_identity": sha(JD_INPUT_FRAME) if exists(JD_INPUT_FRAME) else "missing", "integrity_judgment": "usable_with_boundary(경계 조건부 사용 가능)"})
    write_json(MODEL_RECEIPT, {**base, "model_family": "XGBoost/LightGBM/ExtraTrees planned(엑스지부스트/라이트지비엠/엑스트라트리즈 예정)", "task_seed_rows": summary["task_seed_rows"], "feature_count": summary["feature_count"], "feature_order_hash": summary["feature_order_hash"], "threshold_policy": "no threshold tuning(임계값 조정 없음)", "validation_judgment": "input_materialized_review_required(입력 물질화, 검토 필요)"})
    write_json(PERFORMANCE_RECEIPT, {**base, "observed_change": "runtime negative collapse repair inputs materialized(런타임 음성 붕괴 수리 입력 물질화)", "comparison_baseline": rel(jc.FINAL_DECISION), "likely_drivers": "runtime PnL label, entry throttle, side repair, lifecycle, cost buffer, churn, regime(런타임 손익 라벨/진입 제한/방향 수리/생명주기/비용 버퍼/회전/국면)", "segment_checks": "not_run_until_review_or_training(검토/학습 전 미실행)", "trade_shape": "task seeds encode trade-shape pressure(작업 씨앗이 거래 형태 압박을 반영)", "attribution_confidence": "not_applicable_input_only(입력 전용 해당 없음)", "next_probe": NEXT_RUN_ID})
    write_json(JUDGMENT_RECEIPT, {**base, "decision": DECISION, "next_run_id": NEXT_RUN_ID, "result_class": "input_materialization_review_required(입력 물질화, 검토 필요)", "gate_passes": int(gates["status"].astype(str).eq("passed").sum()), "gate_total": int(len(gates))})
    write_json(CLAIM_RECEIPT, {**base, "candidate_selection": "not_run", "forward_passed": "not_claimed", "forward_failed": "not_claimed", "goal_achieve": "not_claimed", "runtime_authority": "not_claimed", "operating_promotion": "not_claimed", "live_readiness": "not_claimed"})
    write_json(LINEAGE_RECEIPT, {**base, "source_inputs": [rel(path) for path in INPUT_FILES], "producer": rel(Path(__file__)), "consumer": NEXT_RUN_ID, "artifact_paths": [display_path(path) for path in artifact_paths() if exists(path)], "artifact_hashes": {display_path(path): sha(path) for path in artifact_paths() if exists(path) and io(path).is_file()}, "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)], "availability": "generated_with_manifest(목록과 해시 생성)", "lineage_judgment": "connected_with_boundary(경계 조건부 연결)"})


def write_final(summary: Mapping[str, Any], gates: pd.DataFrame) -> dict[str, Any]:
    final = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_action": NEXT_RUN_ID,
        "candidate_selection": "not_run",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "live_readiness": "not_claimed",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "gate_passes": int(gates["status"].astype(str).eq("passed").sum()),
        "gate_total": int(len(gates)),
        "claim_boundary": CLAIM_BOUNDARY,
        **dict(summary),
    }
    write_json(FINAL_DECISION, final)
    write_json(RUN_MANIFEST, {"run_id": RUN_ID, "stage_id": STAGE_ID, "created_at": TODAY, "created_at_utc": now_utc(), "script": rel(Path(__file__)), "inputs": [rel(path) for path in INPUT_FILES], "outputs": [display_path(path) for path in OUTPUT_FILES if exists(path)], "claim_boundary": CLAIM_BOUNDARY})
    return final


def write_docs(final: Mapping[str, Any]) -> None:
    report = f"""# run337JD Runtime Negative Collapse Repair Inputs(run337JD 런타임 음성 붕괴 수리 입력)

## Summary(요약)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- judgment(판정): `{JUDGMENT}`
- gates(게이트): `{final['gate_passes']}/{final['gate_total']}`
- rows(행): `{final['rows']}`
- feature_count(피처 수): `{final['feature_count']}`
- weight_count(가중치 수): `{final['weight_count']}`
- target_valid_rows(목표 유효 행): `{final['target_valid_rows']}`
- task_seed_rows(작업 씨앗 행): `{final['task_seed_rows']}`

## Action(행동)

JC design(JC 설계)을 JD input frame(JD 입력 프레임), train-only label/weight(학습 전용 라벨/가중치), task seed(작업 씨앗)로 물질화했다.
Effect(효과): MT5 negative collapse(MT5 음성 붕괴)를 다음 JE review(JE 검토)와 JF training(JF 학습)의 실제 입력으로 넘긴다.

## Boundary(경계)

No model training(모델 학습 없음), no MT5 execution(MT5 실행 없음), no candidate selection(후보 선택 없음), no runtime authority(런타임 권위 없음), no Goal Achieve(목표 달성 없음).
"""
    decision = f"""# {TODAY} Stage337JD Decision(337JD 결정)

- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- evidence(근거): `{rel(JD_INPUT_FRAME)}`, `{rel(JD_WEIGHT_AUDIT)}`, `{rel(JD_TASK_SEEDS)}`

Action(행동): runtime PnL label(런타임 손익 라벨)과 8개 repair weight(수리 가중치)를 만들었다.
Effect(효과): proxy(프록시) 양성 후보가 MT5(메타트레이더5) 손실 구조를 무시하지 않도록 학습 전 입력을 바꿨다.

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

JD materialization(JD 물질화)은 런타임 음성 붕괴 수리 설계를 timestamp-safe(시점 안전) 학습 입력으로 만들었다.

## Claim Boundary(주장 경계)

`{CLAIM_BOUNDARY}`
"""
    selection = f"""# Stage337 Selection Status(337단계 선택 상태)

- latest_run(최신 실행): `{RUN_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- selected_model(선택 모델): `none(없음)`
- latest_judgment(최신 판정): `runtime_negative_collapse_repair_inputs_materialized(런타임 음성 붕괴 수리 입력 물질화)`
- runtime_authority(런타임 권위): `not_claimed(주장 없음)`
- operating_promotion(운영 승격): `not_claimed(주장 없음)`
- live_readiness(실거래 준비): `not_claimed(주장 없음)`
- goal_achieve(목표 달성): `not_claimed(주장 없음)`

Effect(효과): 입력 물질화를 선택이나 운영 승격으로 오해하지 않게 한다.
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
    marker = f"run337JD {RUN_ID}"
    append_text_once(STAGE_BRIEF, marker, f"""## run337JD Runtime Negative Collapse Repair Inputs(런타임 음성 붕괴 수리 입력)

- run_id(실행 ID): `{RUN_ID}`
- judgment(판정): `{JUDGMENT}`
- task_seed_rows(작업 씨앗 행): `{final['task_seed_rows']}`
- next(다음): `{NEXT_RUN_ID}`
- effect(효과): JC 설계를 학습 전용 입력 산출물로 만들었다.
""")
    append_text_once(ROOT_CHANGELOG, marker, f"""## {TODAY} run337JD Runtime Negative Collapse Repair Inputs(런타임 음성 붕괴 수리 입력)

- action(행동): JD input frame(JD 입력 프레임), 8개 weight(가중치), 8개 task seed(작업 씨앗)를 만들었다.
- effect(효과): MT5 negative collapse(MT5 음성 붕괴)를 다음 JE input review(JE 입력 검토)로 넘겼다.
- boundary(경계): selected model(선택 모델), MT5 execution(MT5 실행), Goal Achieve(목표 달성)는 없다.
""")
    append_text_once(WORKSPACE_CHANGELOG, marker, f"""## {TODAY} run337JD Runtime Negative Collapse Repair Inputs(런타임 음성 붕괴 수리 입력)

- action(행동): JD input frame(JD 입력 프레임), 8개 weight(가중치), 8개 task seed(작업 씨앗)를 만들었다.
- effect(효과): MT5 negative collapse(MT5 음성 붕괴)를 다음 JE input review(JE 입력 검토)로 넘겼다.
- boundary(경계): selected model(선택 모델), MT5 execution(MT5 실행), Goal Achieve(목표 달성)는 없다.
""")


def update_registers(final: Mapping[str, Any]) -> None:
    base = {"stage_id": STAGE_ID, "run_id": RUN_ID, "parent_run_id": PARENT_RUN_ID, "run_date": TODAY, "status": STATUS, "judgment": JUDGMENT, "decision": DECISION, "next_run_id": NEXT_RUN_ID, "primary_artifact": rel(FINAL_DECISION), "report_path": rel(REPORT_PATH), "gate_passes": final["gate_passes"], "gate_total": final["gate_total"], "claim_boundary": CLAIM_BOUNDARY}
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], base)
    rows = [
        {**base, "view": "Tier A separate(Tier A 분리)", "tier": "Tier A", "metric_scope": "input_materialization", "rows": final["rows"], "feature_count": final["feature_count"], "task_seed_rows": final["task_seed_rows"], "result_status": JUDGMENT},
        {**base, "view": "Tier B separate(Tier B 분리)", "tier": "Tier B", "metric_scope": "missing_required", "result_status": "missing_required"},
        {**base, "view": "Tier A+B combined(Tier A+B 합산)", "tier": "Tier A+B", "metric_scope": "missing_required", "result_status": "missing_required"},
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
    source_map, recipe, weight_audit, feature_boundary, tasks, tier_records, runtime_plan, queue, summary = materialize_frame()
    write_csv(JD_SOURCE_MAP, source_map)
    write_csv(JD_WEIGHT_RECIPE, recipe)
    write_csv(JD_WEIGHT_AUDIT, weight_audit)
    write_csv(JD_FEATURE_BOUNDARY, feature_boundary)
    write_csv(JD_TASK_SEEDS, tasks)
    write_csv(JD_TIER_RECORDS, tier_records)
    write_csv(JD_RUNTIME_COMPARISON_PLAN, runtime_plan)
    write_csv(JE_QUEUE, queue)
    gates = make_gates(summary)
    write_csv(GATE_AUDIT, gates)
    write_receipts(summary, gates)
    final = write_final(summary, gates)
    write_docs(final)
    update_registers(final)
    update_artifact_registry(artifact_paths())
    failed = gates.loc[~gates["status"].astype(str).eq("passed")]
    if not failed.empty:
        raise RuntimeError(f"JD gates failed: {failed[['gate_id', 'status']].to_dict(orient='records')}")
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "rows": final["rows"],
                "feature_count": final["feature_count"],
                "task_seed_rows": final["task_seed_rows"],
                "target_class_counts": final["target_class_counts"],
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
