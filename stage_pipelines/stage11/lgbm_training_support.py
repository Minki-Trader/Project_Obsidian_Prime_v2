from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Mapping, Sequence

import joblib
import numpy as np
import pandas as pd
from lightgbm import LGBMClassifier
from sklearn.metrics import accuracy_score, balanced_accuracy_score, f1_score, log_loss


REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.models.baseline_training import LABEL_NAMES, LABEL_ORDER, validate_model_input_frame  # noqa: E402
from foundation.alpha import scout_runner as scout  # noqa: E402
from foundation.control_plane import alpha_run_ledgers  # noqa: E402
from foundation.control_plane.ledger import (  # noqa: E402
    ledger_pairs as _ledger_pairs,
    upsert_csv_rows as _upsert_csv_rows,
)


STAGE_ID = "11_alpha_robustness__wfo_label_horizon_sensitivity"
RUN_NUMBER = "run02A"
RUN_ID = "run02A_lgbm_training_method_scout_v1"
EXPLORATION_LABEL = "stage11_Model__LightGBMTrainingMethodScout"
MODEL_FAMILY = "lightgbm_lgbmclassifier_multiclass"
MODEL_INPUT_DATASET_ID = "model_input_fpmarkets_v2_us100_m5_label_v1_fwd12_split_v1_proxyw58_feature_set_v2"
FEATURE_SET_ID = "feature_set_v2_mt5_price_proxy_top3_weights_58_features"
DEFAULT_MODEL_INPUT_PATH = Path(
    "data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_dataset.parquet"
)
DEFAULT_FEATURE_ORDER_PATH = DEFAULT_MODEL_INPUT_PATH.with_name("model_input_feature_order.txt")
DEFAULT_TIER_B_MODEL_INPUT_PATH = Path(
    "data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v1/model_input_dataset.parquet"
)
DEFAULT_TIER_B_FEATURE_ORDER_PATH = DEFAULT_TIER_B_MODEL_INPUT_PATH.with_name("model_input_feature_order.txt")
DEFAULT_RAW_ROOT = Path("data/raw/mt5_bars/m5")
DEFAULT_TRAINING_SUMMARY_PATH = Path(
    "data/processed/training_datasets/label_v1_fwd12_split_v1_proxyw58/training_dataset_summary.json"
)
DEFAULT_RUN_OUTPUT_ROOT = Path("stages") / STAGE_ID / "02_runs" / RUN_ID
DEFAULT_COMMON_FILES_ROOT = Path.home() / "AppData/Roaming/MetaQuotes/Terminal/Common/Files"
DEFAULT_TERMINAL_DATA_ROOT = REPO_ROOT.parents[2]
DEFAULT_TESTER_PROFILE_ROOT = REPO_ROOT.parents[1] / "Profiles" / "Tester"
STAGE_RUN_LEDGER_PATH = Path("stages") / STAGE_ID / "03_reviews" / "stage_run_ledger.csv"
PROJECT_ALPHA_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
DECISION_SURFACE_ID = "run01Y_threshold_surface_short0600_long0450_margin000_hold9_slice200_220"
RUN01Y_REFERENCE = {
    "run_id": "run01Y_logreg_a_base_no_fallback_hold9_session_mid_second_overlap_200_220_v1",
    "model_family": "sklearn_logistic_regression_multiclass",
    "stage_id": "10_alpha_scout__default_split_model_threshold_scan",
    "threshold_id": "short0.600_long0.450_margin0.000",
    "session_slice_id": "mid_second_overlap_200_220",
    "max_hold_bars": 9,
    "routing_mode": "tier_a_primary_no_fallback",
    "validation_mt5_net_profit": 318.48,
    "validation_mt5_profit_factor": 3.88,
    "oos_mt5_net_profit": 313.14,
    "oos_mt5_profit_factor": 3.99,
    "boundary": "comparison_scoreboard_only_not_operating_reference",
}


@dataclass(frozen=True)
class LgbmTrainingConfig:
    model_family: str = MODEL_FAMILY
    random_seed: int = 11
    n_estimators: int = 300
    learning_rate: float = 0.035
    num_leaves: int = 31
    max_depth: int = -1
    min_child_samples: int = 80
    subsample: float = 0.85
    colsample_bytree: float = 0.85
    reg_alpha: float = 0.0
    reg_lambda: float = 1.0
    class_weight: str | None = None
    n_jobs: int = -1


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Stage 11 RUN02A LightGBM training-method scout.")
    parser.add_argument("--model-input-path", default=str(DEFAULT_MODEL_INPUT_PATH))
    parser.add_argument("--feature-order-path", default=str(DEFAULT_FEATURE_ORDER_PATH))
    parser.add_argument("--tier-b-model-input-path", default=str(DEFAULT_TIER_B_MODEL_INPUT_PATH))
    parser.add_argument("--tier-b-feature-order-path", default=str(DEFAULT_TIER_B_FEATURE_ORDER_PATH))
    parser.add_argument("--raw-root", default=str(DEFAULT_RAW_ROOT))
    parser.add_argument("--training-summary-path", default=str(DEFAULT_TRAINING_SUMMARY_PATH))
    parser.add_argument("--run-output-root", default=str(DEFAULT_RUN_OUTPUT_ROOT))
    parser.add_argument("--run-id", default=RUN_ID)
    parser.add_argument("--run-number", default=RUN_NUMBER)
    parser.add_argument("--exploration-label", default=EXPLORATION_LABEL)
    parser.add_argument("--random-seed", type=int, default=11)
    parser.add_argument("--n-estimators", type=int, default=300)
    parser.add_argument("--learning-rate", type=float, default=0.035)
    parser.add_argument("--num-leaves", type=int, default=31)
    parser.add_argument("--max-depth", type=int, default=-1)
    parser.add_argument("--min-child-samples", type=int, default=80)
    parser.add_argument("--subsample", type=float, default=0.85)
    parser.add_argument("--colsample-bytree", type=float, default=0.85)
    parser.add_argument("--reg-alpha", type=float, default=0.0)
    parser.add_argument("--reg-lambda", type=float, default=1.0)
    parser.add_argument("--class-weight", choices=("balanced", "none"), default="none")
    parser.add_argument("--session-slice-id", default="mid_second_overlap_200_220")
    parser.add_argument("--max-hold-bars", type=int, default=9)
    parser.add_argument("--tier-a-short-threshold", type=float, default=0.600)
    parser.add_argument("--tier-a-long-threshold", type=float, default=0.450)
    parser.add_argument("--tier-a-min-margin", type=float, default=0.000)
    parser.add_argument("--tier-b-short-threshold", type=float, default=0.600)
    parser.add_argument("--tier-b-long-threshold", type=float, default=0.450)
    parser.add_argument("--tier-b-min-margin", type=float, default=0.000)
    parser.add_argument("--attempt-mt5", action="store_true")
    parser.add_argument("--common-files-root", default=str(DEFAULT_COMMON_FILES_ROOT))
    parser.add_argument("--terminal-data-root", default=str(DEFAULT_TERMINAL_DATA_ROOT))
    parser.add_argument("--tester-profile-root", default=str(DEFAULT_TESTER_PROFILE_ROOT))
    parser.add_argument("--terminal-path", default=r"C:\Program Files\MetaTrader 5\terminal64.exe")
    parser.add_argument("--metaeditor-path", default=r"C:\Program Files\MetaTrader 5\MetaEditor64.exe")
    return parser.parse_args()


def _io_path(path: Path) -> Path:
    return scout._io_path(path)


def _json_ready(value: Any) -> Any:
    return scout._json_ready(value)


def write_json(path: Path, payload: Mapping[str, Any]) -> None:
    scout.write_json(path, payload)


def train_lgbm_model(frame: pd.DataFrame, feature_order: Sequence[str], config: LgbmTrainingConfig) -> LGBMClassifier:
    validate_model_input_frame(frame, list(feature_order))
    train_frame = frame.loc[frame["split"].astype(str).eq("train")]
    X_train = train_frame.loc[:, list(feature_order)].astype("float64")
    y_train = train_frame["label_class"].astype("int64").to_numpy()
    missing_train_labels = sorted(set(LABEL_ORDER).difference(set(y_train)))
    if missing_train_labels:
        raise RuntimeError(f"Train split is missing label classes: {missing_train_labels}")

    model = LGBMClassifier(
        objective="multiclass",
        num_class=len(LABEL_ORDER),
        n_estimators=config.n_estimators,
        learning_rate=config.learning_rate,
        num_leaves=config.num_leaves,
        max_depth=config.max_depth,
        min_child_samples=config.min_child_samples,
        subsample=config.subsample,
        colsample_bytree=config.colsample_bytree,
        reg_alpha=config.reg_alpha,
        reg_lambda=config.reg_lambda,
        class_weight=config.class_weight,
        random_state=config.random_seed,
        n_jobs=config.n_jobs,
        verbosity=-1,
    )
    return model.fit(X_train, y_train)


def ordered_probabilities(model: Any, frame: pd.DataFrame, feature_order: Sequence[str]) -> np.ndarray:
    values = frame.loc[:, list(feature_order)].astype("float64")
    raw = np.asarray(model.predict_proba(values), dtype="float64")
    classes = [int(value) for value in model.classes_]
    class_to_index = {label: index for index, label in enumerate(classes)}
    ordered = np.zeros((raw.shape[0], len(LABEL_ORDER)), dtype="float64")
    for output_index, label in enumerate(LABEL_ORDER):
        if int(label) not in class_to_index:
            raise ValueError(f"Model is missing class {label}; cannot build fixed probability order.")
        ordered[:, output_index] = raw[:, class_to_index[int(label)]]
    return ordered


def export_lgbm_to_onnx_zipmap_disabled(
    model: Any,
    output_path: Path,
    *,
    feature_count: int,
    input_name: str = "float_input",
    target_opset: int = 12,
) -> dict[str, Any]:
    from onnxmltools.convert import convert_lightgbm
    from onnxmltools.convert.common.data_types import FloatTensorType

    onnx_model = convert_lightgbm(
        model,
        initial_types=[(input_name, FloatTensorType([None, int(feature_count)]))],
        target_opset=target_opset,
        zipmap=False,
    )
    non_tensor_outputs = [
        output.name for output in onnx_model.graph.output if output.type.WhichOneof("value") != "tensor_type"
    ]
    if non_tensor_outputs:
        raise RuntimeError(f"ONNX export produced non-tensor outputs, zipmap may be enabled: {non_tensor_outputs}")

    _io_path(output_path.parent).mkdir(parents=True, exist_ok=True)
    _io_path(output_path).write_bytes(onnx_model.SerializeToString())
    outputs = [
        {
            "name": output.name,
            "value_type": output.type.WhichOneof("value"),
            "shape": scout._onnx_output_shape(output),
        }
        for output in onnx_model.graph.output
    ]
    probability_outputs = [
        item["name"]
        for item in outputs
        if len(item["shape"]) == 2 and item["shape"][-1] in {len(LABEL_ORDER), "N"}
    ]
    return {
        "path": output_path.as_posix(),
        "sha256": scout.sha256_file(output_path),
        "input_name": input_name,
        "target_opset": target_opset,
        "zipmap_disabled": True,
        "outputs": outputs,
        "probability_output_name": probability_outputs[0] if probability_outputs else outputs[-1]["name"],
    }


def check_lgbm_onnxruntime_probability_parity(
    model: Any,
    onnx_path: Path,
    frame: pd.DataFrame,
    feature_order: Sequence[str],
    *,
    tolerance: float = 1e-2,
) -> dict[str, Any]:
    import onnxruntime as ort

    classes = [int(value) for value in model.classes_]
    if classes != [int(label) for label in LABEL_ORDER]:
        raise ValueError(f"Model class order {classes} does not match expected class order {list(LABEL_ORDER)}.")
    X_frame = frame.loc[:, list(feature_order)].astype("float32")
    raw_expected = np.asarray(model.predict_proba(X_frame), dtype="float64")
    class_to_index = {label: index for index, label in enumerate(classes)}
    expected = np.zeros((raw_expected.shape[0], len(LABEL_ORDER)), dtype="float64")
    for output_index, label in enumerate(LABEL_ORDER):
        expected[:, output_index] = raw_expected[:, class_to_index[int(label)]]
    session = ort.InferenceSession(str(_io_path(onnx_path)), providers=["CPUExecutionProvider"])
    input_name = session.get_inputs()[0].name
    outputs = session.run(None, {input_name: X_frame.to_numpy(dtype="float32", copy=False)})
    actual = scout._find_probability_output(outputs, len(LABEL_ORDER))
    diff = np.abs(actual - expected)
    row_sum_error = np.abs(actual.sum(axis=1) - 1.0)
    return {
        "passed": bool(float(diff.max()) <= tolerance),
        "rows": int(len(X_frame)),
        "class_order": [int(label) for label in LABEL_ORDER],
        "tolerance": float(tolerance),
        "max_abs_diff": float(diff.max()),
        "mean_abs_diff": float(diff.mean()),
        "onnx_row_sum_max_abs_error": float(row_sum_error.max()) if len(row_sum_error) else 0.0,
        "input_name": input_name,
        "output_names": [output.name for output in session.get_outputs()],
    }


def classification_metrics(model: Any, frame: pd.DataFrame, feature_order: Sequence[str]) -> dict[str, Any]:
    payload: dict[str, Any] = {}
    for split_name in ("train", "validation", "oos"):
        split_frame = frame.loc[frame["split"].astype(str).eq(split_name)]
        y_true = split_frame["label_class"].astype("int64").to_numpy()
        probabilities = ordered_probabilities(model, split_frame, feature_order)
        y_pred = np.asarray(LABEL_ORDER, dtype="int64")[probabilities.argmax(axis=1)]
        payload[split_name] = {
            "rows": int(len(split_frame)),
            "accuracy": float(accuracy_score(y_true, y_pred)),
            "balanced_accuracy": float(balanced_accuracy_score(y_true, y_pred)),
            "macro_f1": float(f1_score(y_true, y_pred, labels=LABEL_ORDER, average="macro")),
            "log_loss": float(log_loss(y_true, probabilities, labels=LABEL_ORDER)),
            "predicted_class_distribution": {
                LABEL_NAMES[label]: int((y_pred == label).sum()) for label in LABEL_ORDER
            },
            "mean_probability": {
                name: float(probabilities[:, index].mean())
                for index, name in enumerate(scout.PROBABILITY_COLUMNS)
            },
        }
    return payload


def build_lgbm_prediction_frame(
    model: Any,
    frame: pd.DataFrame,
    feature_order: Sequence[str],
    rule: scout.ThresholdRule,
) -> pd.DataFrame:
    probabilities = ordered_probabilities(model, frame, feature_order)
    decisions = scout.apply_threshold_rule(probabilities, rule)
    identity_columns = [
        name
        for name in (
            "timestamp",
            "symbol",
            "split",
            "label",
            "label_class",
            "route_role",
            "partial_context_subtype",
            "missing_feature_group_mask",
            "available_feature_group_mask",
            "tier_a_primary_available",
            "tier_a_full_feature_ready",
            "tier_b_core_ready",
            "context_reject_reason",
        )
        if name in frame.columns
    ]
    result = frame.loc[:, identity_columns].reset_index(drop=True).copy()
    return pd.concat([result, decisions], axis=1)


def build_python_alpha_ledger_rows(
    *,
    run_id: str,
    tier_records: Sequence[Mapping[str, Any]],
    selected_threshold_id: str,
    model_family: str,
) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for record in tier_records:
        record_view = str(record.get("record_view"))
        metrics = record.get("metrics", {})
        row_view = f"python_{record_view}"
        rows.append(
            {
                "ledger_row_id": f"{run_id}__{row_view}",
                "stage_id": STAGE_ID,
                "run_id": run_id,
                "subrun_id": row_view,
                "parent_run_id": run_id,
                "record_view": row_view,
                "tier_scope": str(record.get("tier_scope")),
                "kpi_scope": "signal_probability_threshold",
                "scoreboard_lane": "structural_scout",
                "status": scout._ledger_status(record.get("status")),
                "judgment": "inconclusive_training_method_scout_payload",
                "path": scout._ledger_path(record.get("path")),
                "primary_kpi": _ledger_pairs(
                    (
                        ("rows", metrics.get("rows")),
                        ("signal_coverage", metrics.get("signal_coverage")),
                        ("signal_count", metrics.get("signal_count")),
                        ("short", metrics.get("short_count")),
                        ("long", metrics.get("long_count")),
                    )
                ),
                "guardrail_kpi": _ledger_pairs(
                    (
                        ("prob_sum_err", metrics.get("probability_row_sum_max_abs_error")),
                        ("selected_threshold", selected_threshold_id),
                        ("model_family", model_family),
                        ("subtype_counts", metrics.get("partial_context_subtype_counts")),
                    )
                ),
                "external_verification_status": "out_of_scope_by_claim",
                "notes": (
                    "Tier B partial-context fallback-only Python view."
                    if record.get("tier_scope") == scout.TIER_B
                    else "Tier A plus Tier B combined Python view; not MT5 routed PnL."
                    if record.get("tier_scope") == scout.TIER_AB
                    else "Tier A full-context primary Python view."
                ),
            }
        )
    return rows


def materialize_ledgers(rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    return alpha_run_ledgers.materialize_alpha_ledgers(
        stage_run_ledger_path=STAGE_RUN_LEDGER_PATH,
        project_alpha_ledger_path=PROJECT_ALPHA_LEDGER_PATH,
        rows=rows,
    )


def materialize_run_registry_row(
    *,
    run_id: str,
    run_output_root: Path,
    route_coverage: Mapping[str, Any],
    tier_records: Sequence[Mapping[str, Any]],
    model_family: str,
    decision_surface_id: str = DECISION_SURFACE_ID,
    lane: str = "alpha_training_method_scout",
    judgment_prefix: str = "training_method_scout",
    external_verification_status: str = "out_of_scope_by_claim",
    mt5_kpi_records: Sequence[Mapping[str, Any]] = (),
    session_slice_id: str = RUN01Y_REFERENCE["session_slice_id"],
    max_hold_bars: int = RUN01Y_REFERENCE["max_hold_bars"],
) -> dict[str, Any]:
    by_view = {str(record.get("record_view")): record.get("metrics", {}) for record in tier_records}
    by_mt5_view = {str(record.get("record_view")): record.get("metrics", {}) for record in mt5_kpi_records}
    validation = by_mt5_view.get("mt5_routed_total_validation_is", {})
    oos = by_mt5_view.get("mt5_routed_total_oos", {})
    notes = _ledger_pairs(
        (
            ("model_family", model_family),
            ("comparison_reference", RUN01Y_REFERENCE["run_id"]),
            ("decision_surface", decision_surface_id),
            ("session_slice", session_slice_id),
            ("max_hold_bars", max_hold_bars),
            ("tier_b_fallback_rows", route_coverage.get("tier_b_fallback_rows")),
            ("no_tier_labelable_rows", route_coverage.get("no_tier_labelable_rows")),
            ("tier_a_signal_coverage", by_view.get("tier_a_separate", {}).get("signal_coverage")),
            ("tier_b_signal_coverage", by_view.get("tier_b_separate", {}).get("signal_coverage")),
            ("combined_signal_coverage", by_view.get("tier_ab_combined", {}).get("signal_coverage")),
            ("validation_net_profit", validation.get("net_profit")),
            ("validation_pf", validation.get("profit_factor")),
            ("validation_b_fallback_used", validation.get("tier_b_fallback_used_count")),
            ("oos_net_profit", oos.get("net_profit")),
            ("oos_pf", oos.get("profit_factor")),
            ("oos_b_fallback_used", oos.get("tier_b_fallback_used_count")),
            ("external_verification", external_verification_status),
            (
                "boundary",
                "mt5_runtime_probe_only"
                if external_verification_status == "completed"
                else "mt5_runtime_probe_attempted_blocked"
                if external_verification_status == "blocked"
                else "python_side_training_method_scout_only",
            ),
        )
    )
    row = {
        "run_id": run_id,
        "stage_id": STAGE_ID,
        "lane": lane,
        "status": "reviewed",
        "judgment": (
            f"inconclusive_{judgment_prefix}_mt5_runtime_probe_completed"
            if external_verification_status == "completed"
            else f"inconclusive_{judgment_prefix}_mt5_runtime_probe_blocked"
            if external_verification_status == "blocked"
            else f"inconclusive_python_side_{judgment_prefix}"
        ),
        "path": run_output_root.as_posix(),
        "notes": notes,
    }
    return _upsert_csv_rows(RUN_REGISTRY_PATH, scout.RUN_REGISTRY_COLUMNS, [row], key="run_id")


def build_mt5_alpha_ledger_rows(
    *,
    run_id: str,
    mt5_kpi_records: Sequence[Mapping[str, Any]],
    run_output_root: Path,
    external_verification_status: str,
) -> list[dict[str, str]]:
    return alpha_run_ledgers.build_mt5_alpha_ledger_rows(
        run_id=run_id,
        stage_id=STAGE_ID,
        mt5_kpi_records=mt5_kpi_records,
        run_output_root=run_output_root,
        external_verification_status=external_verification_status,
        tier_b=scout.TIER_B,
    )


def write_result_summary(
    *,
    path: Path,
    run_id: str,
    tier_records: Sequence[Mapping[str, Any]],
    selected_threshold_id: str,
    route_coverage: Mapping[str, Any],
    model_metrics: Mapping[str, Any],
) -> None:
    by_view = {str(record.get("record_view")): record.get("metrics", {}) for record in tier_records}

    def metric(view: str, key: str) -> Any:
        return by_view.get(view, {}).get(key)

    lines = [
        "# Stage 11 RUN02A LightGBM Training Method Scout",
        "",
        f"- run_id(실행 ID): `{run_id}`",
        f"- model family(모델 계열): `{MODEL_FAMILY}`",
        f"- comparison reference(비교 기준): `{RUN01Y_REFERENCE['run_id']}`",
        f"- selected threshold(선택 임계값): `{selected_threshold_id}`",
        f"- session slice(세션 구간): `{RUN01Y_REFERENCE['session_slice_id']}`",
        f"- max hold bars(최대 보유 봉): `{RUN01Y_REFERENCE['max_hold_bars']}`",
        f"- external verification status(외부 검증 상태): `out_of_scope_by_claim(주장 범위 밖)`",
        "",
        "## Python Signal Views(파이썬 신호 보기)",
        "",
        "| view(보기) | rows(행) | signal coverage(신호 비율) | signal count(신호 수) | short/long(숏/롱) |",
        "|---|---:|---:|---:|---:|",
        (
            f"| Tier A separate(Tier A 분리) | `{metric('tier_a_separate', 'rows')}` | "
            f"`{metric('tier_a_separate', 'signal_coverage')}` | "
            f"`{metric('tier_a_separate', 'signal_count')}` | "
            f"`{metric('tier_a_separate', 'short_count')}/{metric('tier_a_separate', 'long_count')}` |"
        ),
        (
            f"| Tier B-only(Tier B 단독) | `{metric('tier_b_separate', 'rows')}` | "
            f"`{metric('tier_b_separate', 'signal_coverage')}` | "
            f"`{metric('tier_b_separate', 'signal_count')}` | "
            f"`{metric('tier_b_separate', 'short_count')}/{metric('tier_b_separate', 'long_count')}` |"
        ),
        (
            f"| Tier A+B combined(Tier A+B 합산) | `{metric('tier_ab_combined', 'rows')}` | "
            f"`{metric('tier_ab_combined', 'signal_coverage')}` | "
            f"`{metric('tier_ab_combined', 'signal_count')}` | "
            f"`{metric('tier_ab_combined', 'short_count')}/{metric('tier_ab_combined', 'long_count')}` |"
        ),
        "",
        "## Model Metrics(모델 지표)",
        "",
        f"- Tier A validation macro_f1(Tier A 검증 매크로 F1): `{model_metrics['tier_a']['validation']['macro_f1']}`",
        f"- Tier A OOS macro_f1(Tier A 표본외 매크로 F1): `{model_metrics['tier_a']['oos']['macro_f1']}`",
        f"- Tier B validation macro_f1(Tier B 검증 매크로 F1): `{model_metrics['tier_b']['validation']['macro_f1']}`",
        f"- Tier B OOS macro_f1(Tier B 표본외 매크로 F1): `{model_metrics['tier_b']['oos']['macro_f1']}`",
        "",
        "## Route Coverage(라우팅 범위)",
        "",
        f"- Tier A primary rows(Tier A 우선 행): `{route_coverage.get('tier_a_primary_rows')}`",
        f"- Tier B fallback rows(Tier B 대체 행): `{route_coverage.get('tier_b_fallback_rows')}`",
        f"- no_tier labelable rows(티어 없음 라벨 가능 행): `{route_coverage.get('no_tier_labelable_rows')}`",
        f"- Tier B subtype counts(Tier B 하위유형 수): `{route_coverage.get('tier_b_fallback_by_subtype')}`",
        "",
        "## Boundary(경계)",
        "",
        "이 실행(run, 실행)은 Python-side training-method scout(파이썬 측 학습방법 탐색)이다. "
        "효과(effect, 효과)는 LightGBM(라이트GBM)이 같은 입력과 같은 decision surface(의사결정 표면)에서 "
        "신호 분포를 어떻게 바꾸는지 보는 것이다.",
        "",
        "이 실행은 MT5 runtime probe(MT5 런타임 탐침), alpha quality(알파 품질), "
        "live readiness(실거래 준비), operating promotion(운영 승격)을 주장하지 않는다.",
        "",
    ]
    _io_path(path.parent).mkdir(parents=True, exist_ok=True)
    _io_path(path).write_text("\n".join(lines), encoding="utf-8-sig")


def write_result_summary(
    *,
    path: Path,
    run_id: str,
    tier_records: Sequence[Mapping[str, Any]],
    selected_threshold_id: str,
    route_coverage: Mapping[str, Any],
    model_metrics: Mapping[str, Any],
    external_verification_status: str = "out_of_scope_by_claim",
    mt5_kpi_records: Sequence[Mapping[str, Any]] = (),
    session_slice_id: str = RUN01Y_REFERENCE["session_slice_id"],
    max_hold_bars: int = RUN01Y_REFERENCE["max_hold_bars"],
) -> None:
    by_view = {str(record.get("record_view")): record.get("metrics", {}) for record in tier_records}
    by_mt5_view = {str(record.get("record_view")): record.get("metrics", {}) for record in mt5_kpi_records}

    def metric(view: str, key: str) -> Any:
        return by_view.get(view, {}).get(key)

    def mt5_metric(view: str, key: str) -> Any:
        return by_mt5_view.get(view, {}).get(key)

    lines = [
        "# Stage 11 RUN02A LightGBM Training Method Scout",
        "",
        f"- run_id(실행 ID): `{run_id}`",
        f"- model family(모델 계열): `{MODEL_FAMILY}`",
        f"- comparison reference(비교 기준): `{RUN01Y_REFERENCE['run_id']}`",
        f"- selected threshold(선택 임계값): `{selected_threshold_id}`",
        f"- session slice(시간 구간): `{session_slice_id}`",
        f"- max hold bars(최대 보유 봉 수): `{max_hold_bars}`",
        f"- external verification status(외부 검증 상태): `{external_verification_status}`",
        "",
        "## Python Signal Views(파이썬 신호 보기)",
        "",
        "| view(보기) | rows(행) | signal coverage(신호 비율) | signal count(신호 수) | short/long(숏/롱) |",
        "|---|---:|---:|---:|---:|",
        (
            f"| Tier A separate(Tier A 분리) | `{metric('tier_a_separate', 'rows')}` | "
            f"`{metric('tier_a_separate', 'signal_coverage')}` | "
            f"`{metric('tier_a_separate', 'signal_count')}` | "
            f"`{metric('tier_a_separate', 'short_count')}/{metric('tier_a_separate', 'long_count')}` |"
        ),
        (
            f"| Tier B-only(Tier B 단독) | `{metric('tier_b_separate', 'rows')}` | "
            f"`{metric('tier_b_separate', 'signal_coverage')}` | "
            f"`{metric('tier_b_separate', 'signal_count')}` | "
            f"`{metric('tier_b_separate', 'short_count')}/{metric('tier_b_separate', 'long_count')}` |"
        ),
        (
            f"| Tier A+B combined(Tier A+B 합산) | `{metric('tier_ab_combined', 'rows')}` | "
            f"`{metric('tier_ab_combined', 'signal_coverage')}` | "
            f"`{metric('tier_ab_combined', 'signal_count')}` | "
            f"`{metric('tier_ab_combined', 'short_count')}/{metric('tier_ab_combined', 'long_count')}` |"
        ),
        "",
        "## Model Metrics(모델 지표)",
        "",
        f"- Tier A validation macro_f1(Tier A 검증 매크로 F1): `{model_metrics['tier_a']['validation']['macro_f1']}`",
        f"- Tier A OOS macro_f1(Tier A 표본외 매크로 F1): `{model_metrics['tier_a']['oos']['macro_f1']}`",
        f"- Tier B validation macro_f1(Tier B 검증 매크로 F1): `{model_metrics['tier_b']['validation']['macro_f1']}`",
        f"- Tier B OOS macro_f1(Tier B 표본외 매크로 F1): `{model_metrics['tier_b']['oos']['macro_f1']}`",
        "",
        "## Route Coverage(라우팅 범위)",
        "",
        f"- Tier A primary rows(Tier A 우선 행): `{route_coverage.get('tier_a_primary_rows')}`",
        f"- Tier B fallback rows(Tier B 대체 행): `{route_coverage.get('tier_b_fallback_rows')}`",
        f"- no_tier labelable rows(티어 없음 라벨 가능 행): `{route_coverage.get('no_tier_labelable_rows')}`",
        f"- Tier B subtype counts(Tier B 하위유형 수): `{route_coverage.get('tier_b_fallback_by_subtype')}`",
        "",
        "## MT5 Runtime Probe(MT5 런타임 탐침)",
        "",
        f"- MT5 KPI records(MT5 핵심 성과 지표 기록): `{len(mt5_kpi_records)}`",
        f"- validation routed net/PF(검증 라우팅 순수익/수익 팩터): `{mt5_metric('mt5_routed_total_validation_is', 'net_profit')}` / `{mt5_metric('mt5_routed_total_validation_is', 'profit_factor')}`",
        f"- OOS routed net/PF(표본외 라우팅 순수익/수익 팩터): `{mt5_metric('mt5_routed_total_oos', 'net_profit')}` / `{mt5_metric('mt5_routed_total_oos', 'profit_factor')}`",
        f"- validation Tier B fallback used(검증 Tier B 대체 사용): `{mt5_metric('mt5_routed_total_validation_is', 'tier_b_fallback_used_count')}`",
        f"- OOS Tier B fallback used(표본외 Tier B 대체 사용): `{mt5_metric('mt5_routed_total_oos', 'tier_b_fallback_used_count')}`",
        "",
        "## Boundary(경계)",
        "",
        "이 실행(run, 실행)은 training-method scout(학습방법 탐색)와 좁은 MT5 runtime probe(MT5 런타임 탐침)다.",
        "효과(effect, 효과)는 LightGBM(라이트GBM)이 같은 decision surface(의사결정 표면)에서 신호와 런타임 거래를 어떻게 바꾸는지 보는 것이다.",
        "",
        "이 실행은 alpha quality(알파 품질), live readiness(실거래 준비), operating promotion(운영 승격)을 주장하지 않는다.",
        "",
    ]
    _io_path(path.parent).mkdir(parents=True, exist_ok=True)
    _io_path(path).write_text("\n".join(lines), encoding="utf-8-sig")


