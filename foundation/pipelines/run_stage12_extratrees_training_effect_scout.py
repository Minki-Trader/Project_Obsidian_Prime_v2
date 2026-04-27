"""Superseded RUN03A Stage 12 scout.

This script is kept only to reproduce the invalid_for_standalone_scope RUN03A
artifact. It uses Stage 10/11 comparison/context framing and must not be used
as standalone Stage 12 evidence. Use run_stage12_extratrees_standalone_scout.py
for the current standalone experiment.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Mapping, Sequence

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.metrics import accuracy_score, balanced_accuracy_score, f1_score, log_loss


REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.control_plane import alpha_run_ledgers  # noqa: E402
from foundation.control_plane.ledger import (  # noqa: E402
    RUN_REGISTRY_COLUMNS,
    ledger_pairs,
    upsert_csv_rows,
)
from foundation.models.baseline_training import validate_model_input_frame  # noqa: E402
from foundation.pipelines import run_stage10_logreg_mt5_scout as scout  # noqa: E402


STAGE_ID = "12_model_family_challenge__extratrees_training_effect"
RUN_ID = "run03A_extratrees_fwd18_inverse_context_scout_v1"
RUN_NUMBER = "run03A"
EXPLORATION_LABEL = "stage12_Model__ExtraTreesFwd18InverseContext"
MODEL_FAMILY = "sklearn_extratreesclassifier_multiclass"

DEFAULT_MODEL_INPUT_PATH = Path(
    "data/processed/model_inputs/label_v1_fwd18_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_dataset.parquet"
)
DEFAULT_FEATURE_ORDER_PATH = DEFAULT_MODEL_INPUT_PATH.with_name("model_input_feature_order.txt")
DEFAULT_TIER_B_REFERENCE_MODEL_INPUT_PATH = Path(
    "data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v1/model_input_dataset.parquet"
)
DEFAULT_TIER_B_REFERENCE_FEATURE_ORDER_PATH = DEFAULT_TIER_B_REFERENCE_MODEL_INPUT_PATH.with_name(
    "model_input_feature_order.txt"
)
DEFAULT_RAW_ROOT = Path("data/raw/mt5_bars/m5")
DEFAULT_TRAINING_SUMMARY_PATH = Path(
    "data/processed/training_datasets/label_v1_fwd18_split_v1_proxyw58/training_dataset_summary.json"
)
DEFAULT_RUN_OUTPUT_ROOT = Path("stages") / STAGE_ID / "02_runs" / RUN_ID
PROJECT_ALPHA_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
STAGE_RUN_LEDGER_PATH = Path("stages") / STAGE_ID / "03_reviews" / "stage_run_ledger.csv"
RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")

RUN01Y_REFERENCE = {
    "run_id": "run01Y_logreg_a_base_no_fallback_hold9_session_mid_second_overlap_200_220_v1",
    "model_family": "sklearn_logistic_regression_multiclass",
    "stage_id": "10_alpha_scout__default_split_model_threshold_scan",
    "threshold_id": "short0.600_long0.450_margin0.000",
    "session_slice_id": "mid_second_overlap_200_220",
    "max_hold_bars": 9,
    "validation_mt5_net_profit": 318.48,
    "validation_mt5_profit_factor": 3.88,
    "oos_mt5_net_profit": 313.14,
    "oos_mt5_profit_factor": 3.99,
    "boundary": "comparison_scoreboard_only_not_operating_reference",
}
RUN02Z_REFERENCE = {
    "run_id": "run02Z_lgbm_fwd18_inverse_rank_context_v1",
    "model_family": "lightgbm_lgbmclassifier_multiclass",
    "stage_id": "11_alpha_robustness__wfo_label_horizon_sensitivity",
    "selected_surface": "fwd18_inverse_rank_di_spread_abs_lte8_adx_lte25_hold9_slice200_220",
    "validation_mt5_net_profit": 386.06,
    "validation_mt5_profit_factor": 7.25,
    "validation_trades": 9,
    "oos_mt5_net_profit": 352.63,
    "oos_mt5_profit_factor": 52.03,
    "oos_trades": 5,
    "boundary": "tiny_sample_runtime_probe_not_promotion",
}


@dataclass(frozen=True)
class ExtraTreesTrainingConfig:
    model_family: str = MODEL_FAMILY
    random_seed: int = 1203
    n_estimators: int = 600
    min_samples_leaf: int = 60
    min_samples_split: int = 120
    max_features: str = "sqrt"
    bootstrap: bool = False
    class_weight: str | None = "balanced"
    n_jobs: int = -1


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Stage 12 ExtraTrees model-family training effect scout.")
    parser.add_argument("--model-input-path", default=str(DEFAULT_MODEL_INPUT_PATH))
    parser.add_argument("--feature-order-path", default=str(DEFAULT_FEATURE_ORDER_PATH))
    parser.add_argument("--tier-b-reference-model-input-path", default=str(DEFAULT_TIER_B_REFERENCE_MODEL_INPUT_PATH))
    parser.add_argument("--tier-b-reference-feature-order-path", default=str(DEFAULT_TIER_B_REFERENCE_FEATURE_ORDER_PATH))
    parser.add_argument("--raw-root", default=str(DEFAULT_RAW_ROOT))
    parser.add_argument("--training-summary-path", default=str(DEFAULT_TRAINING_SUMMARY_PATH))
    parser.add_argument("--run-output-root", default=str(DEFAULT_RUN_OUTPUT_ROOT))
    parser.add_argument("--run-id", default=RUN_ID)
    parser.add_argument("--run-number", default=RUN_NUMBER)
    parser.add_argument("--session-slice-id", default="mid_second_overlap_200_220")
    parser.add_argument("--max-hold-bars", type=int, default=9)
    parser.add_argument("--rank-quantile", type=float, default=0.96)
    parser.add_argument("--tier-a-min-margin", type=float, default=0.12)
    parser.add_argument("--tier-b-min-margin", type=float, default=0.08)
    parser.add_argument("--parity-rows", type=int, default=128)
    return parser.parse_args()


def _io_path(path: Path) -> Path:
    return scout._io_path(path)


def write_json(path: Path, payload: Mapping[str, Any]) -> None:
    scout.write_json(path, payload)


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(_io_path(path).read_text(encoding="utf-8-sig"))


def write_text_bom(path: Path, text: str) -> None:
    _io_path(path.parent).mkdir(parents=True, exist_ok=True)
    _io_path(path).write_text(text, encoding="utf-8-sig")


def fwd18_label_spec() -> scout.TrainingLabelSplitSpec:
    return scout.TrainingLabelSplitSpec(
        label_id="label_v1_fwd18_m5_logret_train_q33_3class",
        horizon_bars=18,
    )


def train_extratrees_model(
    frame: pd.DataFrame,
    feature_order: Sequence[str],
    config: ExtraTreesTrainingConfig,
) -> ExtraTreesClassifier:
    validate_model_input_frame(frame, list(feature_order))
    train_frame = frame.loc[frame["split"].astype(str).eq("train")]
    x_train = train_frame.loc[:, list(feature_order)].to_numpy(dtype="float64", copy=False)
    y_train = train_frame["label_class"].astype("int64").to_numpy()
    missing_labels = sorted(set(scout.LABEL_ORDER).difference(set(y_train)))
    if missing_labels:
        raise RuntimeError(f"Train split is missing label classes: {missing_labels}")
    model = ExtraTreesClassifier(
        n_estimators=config.n_estimators,
        random_state=config.random_seed,
        min_samples_leaf=config.min_samples_leaf,
        min_samples_split=config.min_samples_split,
        max_features=config.max_features,
        bootstrap=config.bootstrap,
        class_weight=config.class_weight,
        n_jobs=config.n_jobs,
    )
    return model.fit(x_train, y_train)


def ordered_probabilities(model: Any, frame: pd.DataFrame, feature_order: Sequence[str]) -> np.ndarray:
    values = frame.loc[:, list(feature_order)].to_numpy(dtype="float64", copy=False)
    return scout.ordered_sklearn_probabilities(model, values)


def classification_metrics(model: Any, frame: pd.DataFrame, feature_order: Sequence[str]) -> dict[str, Any]:
    validate_model_input_frame(frame, list(feature_order))
    metrics: dict[str, Any] = {}
    for split_name in ("train", "validation", "oos"):
        split = frame.loc[frame["split"].astype(str).eq(split_name)]
        x_values = split.loc[:, list(feature_order)].to_numpy(dtype="float64", copy=False)
        y_true = split["label_class"].astype("int64").to_numpy()
        probabilities = scout.ordered_sklearn_probabilities(model, x_values)
        y_pred = np.asarray(scout.LABEL_ORDER, dtype="int64")[probabilities.argmax(axis=1)]
        metrics[split_name] = {
            "rows": int(len(split)),
            "accuracy": float(accuracy_score(y_true, y_pred)),
            "balanced_accuracy": float(balanced_accuracy_score(y_true, y_pred)),
            "macro_f1": float(f1_score(y_true, y_pred, labels=scout.LABEL_ORDER, average="macro")),
            "log_loss": float(log_loss(y_true, probabilities, labels=scout.LABEL_ORDER)),
            "predicted_class_distribution": {
                scout.LABEL_NAMES[label]: int((y_pred == label).sum()) for label in scout.LABEL_ORDER
            },
            "true_class_distribution": {
                scout.LABEL_NAMES[label]: int((y_true == label).sum()) for label in scout.LABEL_ORDER
            },
            "mean_probability": {
                name: float(probabilities[:, index].mean())
                for index, name in enumerate(scout.PROBABILITY_COLUMNS)
            },
        }
    return metrics


def quantile_threshold_id(prefix: str, quantile: float, short_threshold: float, long_threshold: float, margin: float) -> str:
    return (
        f"{prefix}_rankq{quantile:.3f}_short{short_threshold:.3f}"
        f"_long{long_threshold:.3f}_margin{margin:.3f}"
    )


def quantile_rule(
    frame: pd.DataFrame,
    *,
    quantile: float,
    min_margin: float,
    prefix: str,
) -> scout.ThresholdRule:
    validation = frame.loc[frame["split"].astype(str).eq("validation")]
    if validation.empty:
        raise RuntimeError(f"Cannot select rank threshold from empty validation frame for {prefix}.")
    short_threshold = float(validation["p_short"].quantile(quantile))
    long_threshold = float(validation["p_long"].quantile(quantile))
    return scout.ThresholdRule(
        threshold_id=quantile_threshold_id(prefix, quantile, short_threshold, long_threshold, min_margin),
        short_threshold=short_threshold,
        long_threshold=long_threshold,
        min_margin=min_margin,
    )


def invert_signal_decisions(decisions: pd.DataFrame) -> pd.DataFrame:
    inverted = decisions.copy()
    short_mask = inverted["decision_label_class"].eq(0)
    long_mask = inverted["decision_label_class"].eq(2)
    inverted.loc[short_mask, "decision_label_class"] = 2
    inverted.loc[short_mask, "decision_label"] = scout.LABEL_NAMES[2]
    inverted.loc[long_mask, "decision_label_class"] = 0
    inverted.loc[long_mask, "decision_label"] = scout.LABEL_NAMES[0]
    signal_mask = short_mask | long_mask
    inverted.loc[signal_mask, "threshold_id"] = inverted.loc[signal_mask, "threshold_id"].astype(str) + "_inverse"
    return inverted


def probability_frame(model: Any, frame: pd.DataFrame, feature_order: Sequence[str]) -> pd.DataFrame:
    probabilities = ordered_probabilities(model, frame, feature_order)
    columns = [
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
            "adx_14",
            "di_spread_14",
            "minutes_from_cash_open",
        )
        if name in frame.columns
    ]
    result = frame.loc[:, columns].reset_index(drop=True).copy()
    for index, column in enumerate(scout.PROBABILITY_COLUMNS):
        result[column] = probabilities[:, index]
    result["probability_row_sum"] = probabilities.sum(axis=1)
    return result


def apply_context_gate(frame: pd.DataFrame) -> pd.DataFrame:
    required = {"adx_14", "di_spread_14"}
    missing = sorted(required.difference(frame.columns))
    if missing:
        raise RuntimeError(f"Context gate requires missing columns: {missing}")
    mask = frame["adx_14"].astype("float64").le(25.0)
    mask &= frame["di_spread_14"].astype("float64").abs().le(8.0)
    return frame.loc[mask].copy().reset_index(drop=True)


def build_rank_prediction_frame(prob_frame: pd.DataFrame, rule: scout.ThresholdRule) -> pd.DataFrame:
    decisions = scout.apply_threshold_rule(prob_frame.loc[:, list(scout.PROBABILITY_COLUMNS)], rule)
    decisions = invert_signal_decisions(decisions)
    identity = prob_frame.drop(columns=list(scout.PROBABILITY_COLUMNS), errors="ignore").reset_index(drop=True)
    return pd.concat([identity, decisions], axis=1)


def signal_metrics(frame: pd.DataFrame) -> dict[str, Any]:
    if frame.empty:
        return {
            "rows": 0,
            "signal_count": 0,
            "short_count": 0,
            "long_count": 0,
            "signal_coverage": 0.0,
            "directional_hit_rate": None,
            "by_split": {},
            "probability_row_sum_max_abs_error": None,
        }
    decision = frame["decision_label_class"].astype("int64")
    signal_mask = decision.ne(scout.DECISION_CLASS_NO_TRADE)
    labels = frame["label_class"].astype("int64")
    signal_count = int(signal_mask.sum())
    correct = decision.loc[signal_mask].eq(labels.loc[signal_mask])
    by_split: dict[str, Any] = {}
    for split_name, split in frame.groupby(frame["split"].astype(str)):
        split_decision = split["decision_label_class"].astype("int64")
        split_signal = split_decision.ne(scout.DECISION_CLASS_NO_TRADE)
        split_labels = split["label_class"].astype("int64")
        split_correct = split_decision.loc[split_signal].eq(split_labels.loc[split_signal])
        by_split[split_name] = {
            "rows": int(len(split)),
            "signal_count": int(split_signal.sum()),
            "short_count": int(split_decision.eq(0).sum()),
            "long_count": int(split_decision.eq(2).sum()),
            "signal_coverage": float(split_signal.mean()) if len(split) else 0.0,
            "directional_hit_rate": float(split_correct.mean()) if int(split_signal.sum()) else None,
            "directional_correct_count": int(split_correct.sum()) if int(split_signal.sum()) else 0,
        }
    probabilities = frame.loc[:, list(scout.PROBABILITY_COLUMNS)].to_numpy(dtype="float64", copy=False)
    return {
        "rows": int(len(frame)),
        "signal_count": signal_count,
        "short_count": int(decision.eq(0).sum()),
        "long_count": int(decision.eq(2).sum()),
        "signal_coverage": float(signal_count / len(frame)) if len(frame) else 0.0,
        "directional_hit_rate": float(correct.mean()) if signal_count else None,
        "directional_correct_count": int(correct.sum()) if signal_count else 0,
        "by_split": by_split,
        "probability_row_sum_max_abs_error": float(np.abs(probabilities.sum(axis=1) - 1.0).max()),
        "mean_probability": {
            column: float(frame[column].astype("float64").mean()) for column in scout.PROBABILITY_COLUMNS
        },
        "partial_context_subtype_counts": frame.get("partial_context_subtype", pd.Series(dtype="object")).value_counts().to_dict(),
    }


def rank_quantile_sweep(
    prob_frame: pd.DataFrame,
    *,
    tier_name: str,
    quantiles: Sequence[float] = (0.80, 0.85, 0.90, 0.94, 0.96, 0.98, 0.99),
    margins: Sequence[float] = (0.00, 0.02, 0.05, 0.08, 0.12),
) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    validation = prob_frame.loc[prob_frame["split"].astype(str).eq("validation")]
    eval_frame = apply_context_gate(prob_frame)
    prefix = "tier_a" if tier_name == scout.TIER_A else "tier_b"
    for quantile in quantiles:
        for margin in margins:
            rule = quantile_rule(validation, quantile=quantile, min_margin=margin, prefix=prefix)
            pred = build_rank_prediction_frame(eval_frame, rule)
            metrics = signal_metrics(pred)
            validation_metrics = metrics["by_split"].get("validation", {})
            oos_metrics = metrics["by_split"].get("oos", {})
            rows.append(
                {
                    "tier": tier_name,
                    "quantile": quantile,
                    "min_margin": margin,
                    "threshold_id": rule.threshold_id,
                    "short_threshold": rule.short_threshold,
                    "long_threshold": rule.long_threshold,
                    "context_gate": "di_spread_abs_lte8_adx_lte25",
                    "invert_decisions": True,
                    "rows": metrics["rows"],
                    "signal_count": metrics["signal_count"],
                    "signal_coverage": metrics["signal_coverage"],
                    "directional_hit_rate": metrics["directional_hit_rate"],
                    "validation_signal_count": validation_metrics.get("signal_count"),
                    "validation_hit_rate": validation_metrics.get("directional_hit_rate"),
                    "oos_signal_count": oos_metrics.get("signal_count"),
                    "oos_hit_rate": oos_metrics.get("directional_hit_rate"),
                }
            )
    return pd.DataFrame(rows)


def selected_threshold_id(
    *,
    tier_a_rule: scout.ThresholdRule,
    tier_b_rule: scout.ThresholdRule,
    max_hold_bars: int,
    session_slice_id: str,
) -> str:
    return (
        f"a_{tier_a_rule.threshold_id}__b_{tier_b_rule.threshold_id}"
        f"__hold{max_hold_bars}__slice_{session_slice_id}"
        "__model_extratrees_rank_target_inverse__ctx_di_spread_abs_lte8_adx_lte25"
    )


def build_python_ledger_rows(
    *,
    run_id: str,
    tier_records: Mapping[str, Mapping[str, Any]],
    selected_threshold: str,
    predictions_root: Path,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for record_view, record in tier_records.items():
        metrics = record["metrics"]
        tier_scope = record["tier_scope"]
        rows.append(
            {
                "ledger_row_id": f"{run_id}__python_{record_view}",
                "stage_id": STAGE_ID,
                "run_id": run_id,
                "subrun_id": f"python_{record_view}",
                "parent_run_id": run_id,
                "record_view": f"python_{record_view}",
                "tier_scope": tier_scope,
                "kpi_scope": "signal_probability_rank_target_threshold",
                "scoreboard_lane": "structural_scout",
                "status": "completed",
                "judgment": "inconclusive_extratrees_rank_context_payload",
                "path": (predictions_root / f"{record_view}_predictions.parquet").as_posix(),
                "primary_kpi": ledger_pairs(
                    (
                        ("rows", metrics.get("rows")),
                        ("signal_count", metrics.get("signal_count")),
                        ("coverage", metrics.get("signal_coverage")),
                        ("hit_rate", metrics.get("directional_hit_rate")),
                        ("validation_signals", metrics.get("by_split", {}).get("validation", {}).get("signal_count")),
                        ("oos_signals", metrics.get("by_split", {}).get("oos", {}).get("signal_count")),
                    )
                ),
                "guardrail_kpi": ledger_pairs(
                    (
                        ("prob_sum_err", metrics.get("probability_row_sum_max_abs_error")),
                        ("selected_threshold", selected_threshold),
                        ("model_family", MODEL_FAMILY),
                        ("subtype_counts", metrics.get("partial_context_subtype_counts")),
                    )
                ),
                "external_verification_status": "out_of_scope_by_claim",
                "notes": "Python structural scout only; no MT5 trading PnL is claimed.",
            }
        )
    return rows


def materialize_run_registry_row(
    *,
    run_id: str,
    run_output_root: Path,
    combined_metrics: Mapping[str, Any],
    selected_threshold: str,
) -> dict[str, Any]:
    validation = combined_metrics.get("by_split", {}).get("validation", {})
    oos = combined_metrics.get("by_split", {}).get("oos", {})
    row = {
        "run_id": run_id,
        "stage_id": STAGE_ID,
        "lane": "alpha_model_family_challenger",
        "status": "payload_only",
        "judgment": "inconclusive_extratrees_structural_scout_payload",
        "path": run_output_root.as_posix(),
        "notes": ledger_pairs(
            (
                ("model_family", MODEL_FAMILY),
                ("comparison_reference", RUN02Z_REFERENCE["run_id"]),
                ("selected_threshold", selected_threshold),
                ("validation_signal_count", validation.get("signal_count")),
                ("validation_hit_rate", validation.get("directional_hit_rate")),
                ("oos_signal_count", oos.get("signal_count")),
                ("oos_hit_rate", oos.get("directional_hit_rate")),
                ("external_verification", "out_of_scope_by_claim"),
                ("boundary", "python_structural_scout_only"),
            )
        ),
    }
    return upsert_csv_rows(RUN_REGISTRY_PATH, RUN_REGISTRY_COLUMNS, [row], key="run_id")


def materialize_stage_docs(
    *,
    run_id: str,
    run_output_root: Path,
    selected_threshold: str,
    tier_records: Mapping[str, Mapping[str, Any]],
) -> dict[str, str]:
    stage_root = Path("stages") / STAGE_ID
    stage_brief_path = stage_root / "00_spec" / "stage_brief.md"
    plan_path = stage_root / "00_spec" / "run03A_extratrees_training_effect_plan.md"
    input_refs_path = stage_root / "01_inputs" / "input_references.md"
    packet_path = stage_root / "03_reviews" / "run03A_extratrees_training_effect_packet.md"
    selection_status_path = stage_root / "04_selected" / "selection_status.md"

    combined = tier_records["tier_ab_combined"]["metrics"]
    validation = combined["by_split"].get("validation", {})
    oos = combined["by_split"].get("oos", {})
    stage_brief = f"""# Stage 12 Model Family Challenge: ExtraTrees Training Effect

## 질문(Question, 질문)

Stage 10(10단계)의 logistic regression(로지스틱 회귀)과 Stage 11(11단계)의 LightGBM(라이트GBM)이 아닌 새 모델 계열(model family, 모델 계열)을 학습하면, Stage 11(11단계)의 fwd18 inverse-rank context(fwd18 역방향 순위 문맥) 단서가 구조적으로 달라지는가?

## 범위(Scope, 범위)

- new model family(새 모델 계열): `ExtraTreesClassifier(엑스트라 트리 분류기)`
- label horizon(라벨 예측수평선): `fwd18(90분)`
- session slice(세션 구간): `200 < minutes_from_cash_open <= 220`
- context gate(문맥 제한): `abs(di_spread_14) <= 8`, `adx_14 <= 25`
- Tier A separate(Tier A 분리), Tier B separate(Tier B 분리), Tier A+B combined(Tier A+B 합산)

## 범위 밖(Not In Scope, 범위 밖)

- alpha quality(알파 품질)
- live readiness(실거래 준비)
- operating promotion(운영 승격)
- runtime authority expansion(런타임 권위 확장)

## 종료 조건(Exit Condition, 종료 조건)

새 모델 학습 효과(new model training effect, 새 모델 학습 효과)가 Stage 10/11(10/11단계) 기준과 비교해 유지, 약화, 무효, 또는 MT5 runtime_probe(MT5 런타임 탐침) 후보 중 하나로 정리되면 닫을 수 있다.
"""
    plan = f"""# RUN03A ExtraTrees Training Effect Plan

## Intake(인입)

- active stage(활성 단계): `{STAGE_ID}`
- run_id(실행 ID): `{run_id}`
- comparison baseline(비교 기준): `{RUN02Z_REFERENCE['run_id']}`
- claim boundary(주장 경계): `Python structural scout(파이썬 구조 탐침)` only(전용)

## Router(라우터)

- phase_plan(단계 계획): design(설계) -> code(코드) -> Python run(파이썬 실행) -> evidence recording(근거 기록) -> result judgment(결과 판정)
- skills_considered(검토한 스킬): `obsidian-reentry-read`, `obsidian-experiment-design`, `obsidian-data-integrity`, `obsidian-environment-reproducibility`, `obsidian-model-validation`, `obsidian-result-judgment`
- skills_selected(선택한 스킬): 위 전부
- skills_not_used(쓰지 않은 스킬): `obsidian-runtime-parity(런타임 동등성)`는 이번 run(실행)이 MT5 runtime_probe(MT5 런타임 탐침)를 주장하지 않아서 제외
- final_answer_filter(최종 답변 필터): 결론, 수치, 아직 아닌 것, 다음 조건만 짧게 말한다.

## Experiment Design(실험 설계)

- hypothesis(가설): ExtraTreesClassifier(엑스트라 트리 분류기)는 LightGBM(라이트GBM)과 다른 비선형 분할을 만들기 때문에 fwd18 inverse-rank context(fwd18 역방향 순위 문맥)의 신호 밀도와 hit rate(적중률)를 바꿀 수 있다.
- decision_use(결정 용도): Stage 12(12단계)에서 MT5 runtime_probe(MT5 런타임 탐침)로 넘길 새 모델 표면이 있는지 판단한다.
- comparison_baseline(비교 기준): `RUN02Z(실행 02Z)` LightGBM fwd18 inverse-rank context MT5 runtime_probe(런타임 탐침)
- control_variables(통제 변수): `US100`, `M5`, fwd18 label(90분 라벨), split v1(분할 v1), `200-220` session slice(세션 구간), `ADX<=25`, `abs(DI spread)<=8`, inverse decision(역방향 판정), hold(보유) `9`
- changed_variables(변경 변수): model family(모델 계열)만 `LightGBM`에서 `ExtraTreesClassifier`로 변경
- sample_scope(표본 범위): Tier A/Tier B/Tier A+B context-filtered(문맥 필터) validation/OOS(검증/표본외)
- success_criteria(성공 기준): validation/OOS(검증/표본외) 모두에서 충분한 signal count(신호 수)와 방향 hit rate(방향 적중률)가 생겨 MT5 runtime_probe(MT5 런타임 탐침) 후보가 된다.
- failure_criteria(실패 기준): signal count(신호 수)가 너무 작거나 validation/OOS(검증/표본외) hit rate(적중률)가 동시에 약하다.
- invalid_conditions(무효 조건): feature order hash(피처 순서 해시) 불일치, label/split(라벨/분할) 누락, ONNX parity(ONNX 동등성) 실패
- stop_conditions(중지 조건): Python structural scout(파이썬 구조 탐침)만으로 운영 의미(operational meaning, 운영 의미)를 주장하지 않는다.
- evidence_plan(근거 계획): `run_manifest.json`, `kpi_record.json`, `summary.json`, `result_summary.md`, stage/project ledgers(단계/프로젝트 장부)
"""
    input_refs = f"""# Stage 12 Input References

- Tier A model input(Tier A 모델 입력): `{DEFAULT_MODEL_INPUT_PATH.as_posix()}`
- Tier A feature order(Tier A 피처 순서): `{DEFAULT_FEATURE_ORDER_PATH.as_posix()}`
- training summary(학습 요약): `{DEFAULT_TRAINING_SUMMARY_PATH.as_posix()}`
- raw root(원천 루트): `{DEFAULT_RAW_ROOT.as_posix()}`
- comparison reference(비교 기준): `{RUN02Z_REFERENCE['run_id']}`
"""
    packet = f"""# RUN03A ExtraTrees Training Effect Packet

- run_id(실행 ID): `{run_id}`
- stage(단계): `{STAGE_ID}`
- model family(모델 계열): `{MODEL_FAMILY}`
- selected threshold(선택 임계값): `{selected_threshold}`
- boundary(경계): `Python structural scout(파이썬 구조 탐침)` only(전용)

## Result Read(결과 판독)

| view(보기) | rows(행) | signals(신호) | coverage(비율) | validation hit(검증 적중률) | OOS hit(표본외 적중률) |
|---|---:|---:|---:|---:|---:|
| Tier A separate(Tier A 분리) | `{tier_records['tier_a_separate']['metrics']['rows']}` | `{tier_records['tier_a_separate']['metrics']['signal_count']}` | `{tier_records['tier_a_separate']['metrics']['signal_coverage']}` | `{tier_records['tier_a_separate']['metrics']['by_split'].get('validation', {}).get('directional_hit_rate')}` | `{tier_records['tier_a_separate']['metrics']['by_split'].get('oos', {}).get('directional_hit_rate')}` |
| Tier B separate(Tier B 분리) | `{tier_records['tier_b_separate']['metrics']['rows']}` | `{tier_records['tier_b_separate']['metrics']['signal_count']}` | `{tier_records['tier_b_separate']['metrics']['signal_coverage']}` | `{tier_records['tier_b_separate']['metrics']['by_split'].get('validation', {}).get('directional_hit_rate')}` | `{tier_records['tier_b_separate']['metrics']['by_split'].get('oos', {}).get('directional_hit_rate')}` |
| Tier A+B combined(Tier A+B 합산) | `{combined['rows']}` | `{combined['signal_count']}` | `{combined['signal_coverage']}` | `{validation.get('directional_hit_rate')}` | `{oos.get('directional_hit_rate')}` |

## Judgment(판정)

`RUN03A(실행 03A)`는 ExtraTrees(엑스트라 트리) 학습 효과를 Python structural scout(파이썬 구조 탐침)로 기록했다. 효과(effect, 효과)는 Stage 11(11단계)의 LightGBM(라이트GBM) 단서와 다른 모델 확률 표면(probability surface, 확률 표면)을 비교할 수 있게 한 것이다.

아직 MT5 runtime_probe(MT5 런타임 탐침), alpha quality(알파 품질), live readiness(실거래 준비), promotion_candidate(승격 후보)는 아니다.

## Artifact Paths(산출물 경로)

- run manifest(실행 목록): `{(run_output_root / 'run_manifest.json').as_posix()}`
- kpi record(KPI 기록): `{(run_output_root / 'kpi_record.json').as_posix()}`
- summary(요약): `{(run_output_root / 'summary.json').as_posix()}`
- result summary(결과 요약): `{(run_output_root / 'reports' / 'result_summary.md').as_posix()}`
"""
    selection = f"""# Selection Status

## 현재 판독(Current Read, 현재 판독)

- stage(단계): `{STAGE_ID}`
- status(상태): `active_structural_scout_open(구조 탐침 활성)`
- current run(현재 실행): `{run_id}`
- current model family(현재 모델 계열): `{MODEL_FAMILY}`
- current operating reference(현재 운영 기준): `none(없음)`
- selected promotion candidate(선택 승격 후보): `none(없음)`

## 현재 RUN03A(Current RUN03A, 현재 실행 03A)

- selected threshold(선택 임계값): `{selected_threshold}`
- Tier A+B combined signals(Tier A+B 합산 신호): `{combined['signal_count']}`
- validation hit rate(검증 적중률): `{validation.get('directional_hit_rate')}`
- OOS hit rate(표본외 적중률): `{oos.get('directional_hit_rate')}`
- external verification status(외부 검증 상태): `out_of_scope_by_claim(주장 범위 밖)`

효과(effect, 효과): Stage 12(12단계)는 열렸고, 첫 run(실행)은 새 모델 학습 효과를 Python structural scout(파이썬 구조 탐침)로 남겼다. MT5 runtime_probe(MT5 런타임 탐침)는 아직 하지 않았다.
"""
    write_text_bom(stage_brief_path, stage_brief)
    write_text_bom(plan_path, plan)
    write_text_bom(input_refs_path, input_refs)
    write_text_bom(packet_path, packet)
    write_text_bom(selection_status_path, selection)
    return {
        "stage_brief_path": stage_brief_path.as_posix(),
        "plan_path": plan_path.as_posix(),
        "input_refs_path": input_refs_path.as_posix(),
        "packet_path": packet_path.as_posix(),
        "selection_status_path": selection_status_path.as_posix(),
    }


def write_result_summary(
    path: Path,
    *,
    run_id: str,
    selected_threshold: str,
    model_metrics: Mapping[str, Any],
    tier_records: Mapping[str, Mapping[str, Any]],
    onnx_parity: Mapping[str, Any],
) -> None:
    combined = tier_records["tier_ab_combined"]["metrics"]
    validation = combined["by_split"].get("validation", {})
    oos = combined["by_split"].get("oos", {})
    lines = [
        "# Stage 12 RUN03A ExtraTrees Training Effect Scout",
        "",
        f"- run_id(실행 ID): `{run_id}`",
        f"- model family(모델 계열): `{MODEL_FAMILY}`",
        f"- selected threshold(선택 임계값): `{selected_threshold}`",
        f"- ONNX parity(ONNX 동등성): `{onnx_parity.get('passed')}`",
        "",
        "## Model Metrics(모델 지표)",
        "",
        f"- Tier A validation macro_f1(Tier A 검증 매크로 F1): `{model_metrics['tier_a']['validation']['macro_f1']}`",
        f"- Tier A OOS macro_f1(Tier A 표본외 매크로 F1): `{model_metrics['tier_a']['oos']['macro_f1']}`",
        f"- Tier B validation macro_f1(Tier B 검증 매크로 F1): `{model_metrics['tier_b']['validation']['macro_f1']}`",
        f"- Tier B OOS macro_f1(Tier B 표본외 매크로 F1): `{model_metrics['tier_b']['oos']['macro_f1']}`",
        "",
        "## Context Signal Read(문맥 신호 판독)",
        "",
        "| view(보기) | rows(행) | signals(신호) | coverage(비율) | validation hit(검증 적중률) | OOS hit(표본외 적중률) |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for view, label in (
        ("tier_a_separate", "Tier A separate(Tier A 분리)"),
        ("tier_b_separate", "Tier B separate(Tier B 분리)"),
        ("tier_ab_combined", "Tier A+B combined(Tier A+B 합산)"),
    ):
        metrics = tier_records[view]["metrics"]
        lines.append(
            f"| {label} | `{metrics['rows']}` | `{metrics['signal_count']}` | "
            f"`{metrics['signal_coverage']}` | "
            f"`{metrics['by_split'].get('validation', {}).get('directional_hit_rate')}` | "
            f"`{metrics['by_split'].get('oos', {}).get('directional_hit_rate')}` |"
        )
    lines.extend(
        [
            "",
            "## 비교 기준(Comparison, 비교)",
            "",
            f"- RUN01Y(실행 01Y) LogReg(로지스틱 회귀) MT5 OOS(표본외): `{RUN01Y_REFERENCE['oos_mt5_net_profit']} / PF {RUN01Y_REFERENCE['oos_mt5_profit_factor']}`",
            f"- RUN02Z(실행 02Z) LightGBM(라이트GBM) MT5 OOS(표본외): `{RUN02Z_REFERENCE['oos_mt5_net_profit']} / PF {RUN02Z_REFERENCE['oos_mt5_profit_factor']} / {RUN02Z_REFERENCE['oos_trades']} trades(거래)`",
            f"- RUN03A(실행 03A) ExtraTrees(엑스트라 트리) Python OOS(표본외): `{oos.get('signal_count')}` signals(신호), hit rate(적중률) `{oos.get('directional_hit_rate')}`",
            "",
            "## Boundary(경계)",
            "",
            "이 실행(run, 실행)은 Python structural scout(파이썬 구조 탐침)이다. MT5 runtime_probe(MT5 런타임 탐침), alpha quality(알파 품질), live readiness(실거래 준비), operating promotion(운영 승격)을 주장하지 않는다.",
        ]
    )
    write_text_bom(path, "\n".join(lines) + "\n")


def run_stage12_extratrees_training_effect_scout(
    *,
    model_input_path: Path,
    feature_order_path: Path,
    tier_b_reference_model_input_path: Path,
    tier_b_reference_feature_order_path: Path,
    raw_root: Path,
    training_summary_path: Path,
    run_output_root: Path,
    run_id: str,
    run_number: str,
    session_slice_id: str,
    max_hold_bars: int,
    rank_quantile: float,
    tier_a_min_margin: float,
    tier_b_min_margin: float,
    parity_rows: int,
) -> dict[str, Any]:
    if max_hold_bars != 9:
        raise RuntimeError("RUN03A keeps max_hold_bars fixed at 9 for model-family comparison.")

    config = ExtraTreesTrainingConfig()
    tier_a_feature_order = scout.load_feature_order(feature_order_path)
    tier_a_feature_hash = scout.ordered_hash(tier_a_feature_order)
    if tier_a_feature_hash != scout.FEATURE_ORDER_HASH:
        raise RuntimeError(f"Feature order hash mismatch: {tier_a_feature_hash} != {scout.FEATURE_ORDER_HASH}")

    reference_tier_b_features = scout.load_feature_order(tier_b_reference_feature_order_path)
    tier_b_feature_order = list(scout.TIER_B_CORE_FEATURE_ORDER)
    missing_core = sorted(set(tier_b_feature_order).difference(reference_tier_b_features))
    if missing_core:
        raise RuntimeError(f"Tier B core feature order is missing reference features: {missing_core}")
    tier_b_feature_hash = scout.ordered_hash(tier_b_feature_order)

    label_threshold = scout.load_label_threshold(training_summary_path)
    tier_a_frame = pd.read_parquet(_io_path(model_input_path))
    tier_a_frame["timestamp"] = pd.to_datetime(tier_a_frame["timestamp"], utc=True)
    tier_a_frame["route_role"] = scout.ROUTE_ROLE_A_PRIMARY
    tier_a_frame["partial_context_subtype"] = "Tier_A_full_context"
    tier_a_frame["missing_feature_group_mask"] = "none"
    tier_a_frame["available_feature_group_mask"] = "macro|constituent|basket"
    tier_a_frame["tier_a_primary_available"] = True
    tier_a_frame["tier_a_full_feature_ready"] = True
    tier_a_frame["tier_b_core_ready"] = True

    tier_b_context = scout.build_tier_b_partial_context_frames(
        raw_root=raw_root,
        tier_a_frame=tier_a_frame,
        tier_a_feature_order=tier_a_feature_order,
        tier_b_feature_order=tier_b_feature_order,
        label_threshold=label_threshold,
        label_spec=fwd18_label_spec(),
    )
    tier_b_training_frame = tier_b_context["tier_b_training_frame"]
    tier_b_frame = tier_b_context["tier_b_fallback_frame"]
    no_tier_frame = tier_b_context["no_tier_frame"]
    route_coverage_base = tier_b_context["summary"]

    _io_path(run_output_root).mkdir(parents=True, exist_ok=True)
    models_root = run_output_root / "models"
    predictions_root = run_output_root / "predictions"
    sweeps_root = run_output_root / "sweeps"
    reports_root = run_output_root / "reports"
    _io_path(models_root).mkdir(parents=True, exist_ok=True)
    _io_path(predictions_root).mkdir(parents=True, exist_ok=True)
    _io_path(sweeps_root).mkdir(parents=True, exist_ok=True)

    tier_a_model = train_extratrees_model(tier_a_frame, tier_a_feature_order, config)
    tier_b_model = train_extratrees_model(tier_b_training_frame, tier_b_feature_order, config)
    model_metrics = {
        "tier_a": classification_metrics(tier_a_model, tier_a_frame, tier_a_feature_order),
        "tier_b": classification_metrics(tier_b_model, tier_b_training_frame, tier_b_feature_order),
    }

    session_slice = scout.session_slice_payload(session_slice_id)
    tier_a_session = scout.apply_session_slice(tier_a_frame, session_slice)
    tier_b_session = scout.apply_session_slice(tier_b_frame, session_slice)
    no_tier_session = scout.apply_session_slice(no_tier_frame, session_slice)

    tier_a_prob_session = probability_frame(tier_a_model, tier_a_session, tier_a_feature_order)
    tier_b_prob_session = probability_frame(tier_b_model, tier_b_session, tier_b_feature_order)
    tier_a_rule = quantile_rule(
        tier_a_prob_session,
        quantile=rank_quantile,
        min_margin=tier_a_min_margin,
        prefix="tier_a",
    )
    tier_b_rule = quantile_rule(
        tier_b_prob_session,
        quantile=rank_quantile,
        min_margin=tier_b_min_margin,
        prefix="tier_b",
    )
    selected = selected_threshold_id(
        tier_a_rule=tier_a_rule,
        tier_b_rule=tier_b_rule,
        max_hold_bars=max_hold_bars,
        session_slice_id=session_slice_id,
    )

    tier_a_context = apply_context_gate(tier_a_prob_session)
    tier_b_context_eval = apply_context_gate(tier_b_prob_session)
    no_tier_context = apply_context_gate(no_tier_session) if not no_tier_session.empty else no_tier_session.copy()
    route_coverage = scout.build_eval_route_coverage_summary(
        base_summary=route_coverage_base,
        tier_a_eval_frame=tier_a_context,
        tier_b_eval_frame=tier_b_context_eval,
        no_tier_eval_frame=no_tier_context,
        session_slice=session_slice,
    )
    route_coverage["context_gate"] = "di_spread_abs_lte8_adx_lte25"
    route_coverage["note"] = "Session and context filtered structural scout rows; no MT5 PnL."

    tier_a_predictions = build_rank_prediction_frame(tier_a_context, tier_a_rule)
    tier_b_predictions = build_rank_prediction_frame(tier_b_context_eval, tier_b_rule)
    tier_a_predictions[scout.TIER_COLUMN] = scout.TIER_A
    tier_b_predictions[scout.TIER_COLUMN] = scout.TIER_B
    tier_a_predictions["feature_count"] = len(tier_a_feature_order)
    tier_b_predictions["feature_count"] = len(tier_b_feature_order)
    tier_a_predictions["feature_order_hash"] = tier_a_feature_hash
    tier_b_predictions["feature_order_hash"] = tier_b_feature_hash
    combined_predictions = pd.concat([tier_a_predictions, tier_b_predictions], ignore_index=True)

    paths = {
        "tier_a_separate": predictions_root / "tier_a_separate_predictions.parquet",
        "tier_b_separate": predictions_root / "tier_b_separate_predictions.parquet",
        "tier_ab_combined": predictions_root / "tier_ab_combined_predictions.parquet",
        "tier_a_predictions": predictions_root / "tier_a_predictions.parquet",
        "tier_b_predictions": predictions_root / "tier_b_predictions.parquet",
        "no_tier_route_rows": predictions_root / "no_tier_route_rows.parquet",
        "route_coverage_summary": predictions_root / "route_coverage_summary.json",
    }
    tier_a_predictions.to_parquet(_io_path(paths["tier_a_separate"]), index=False)
    tier_b_predictions.to_parquet(_io_path(paths["tier_b_separate"]), index=False)
    combined_predictions.to_parquet(_io_path(paths["tier_ab_combined"]), index=False)
    tier_a_predictions.to_parquet(_io_path(paths["tier_a_predictions"]), index=False)
    tier_b_predictions.to_parquet(_io_path(paths["tier_b_predictions"]), index=False)
    no_tier_context.to_parquet(_io_path(paths["no_tier_route_rows"]), index=False)
    write_json(paths["route_coverage_summary"], route_coverage)

    sweep_a = rank_quantile_sweep(tier_a_prob_session, tier_name=scout.TIER_A)
    sweep_b = rank_quantile_sweep(tier_b_prob_session, tier_name=scout.TIER_B)
    sweep_combined = pd.concat([sweep_a, sweep_b], ignore_index=True)
    sweep_paths = {
        "tier_a": sweeps_root / "rank_quantile_sweep_tier_a.csv",
        "tier_b": sweeps_root / "rank_quantile_sweep_tier_b.csv",
        "combined": sweeps_root / "rank_quantile_sweep_combined.csv",
    }
    sweep_a.to_csv(_io_path(sweep_paths["tier_a"]), index=False)
    sweep_b.to_csv(_io_path(sweep_paths["tier_b"]), index=False)
    sweep_combined.to_csv(_io_path(sweep_paths["combined"]), index=False)

    tier_records = {
        "tier_a_separate": {"tier_scope": scout.TIER_A, "metrics": signal_metrics(tier_a_predictions)},
        "tier_b_separate": {"tier_scope": scout.TIER_B, "metrics": signal_metrics(tier_b_predictions)},
        "tier_ab_combined": {"tier_scope": scout.TIER_AB, "metrics": signal_metrics(combined_predictions)},
    }

    tier_a_model_path = models_root / "tier_a_extratrees_58_model.joblib"
    tier_b_model_path = models_root / "tier_b_extratrees_core42_model.joblib"
    tier_a_feature_order_path = models_root / "tier_a_58_feature_order.txt"
    tier_b_feature_order_path = models_root / "tier_b_core42_feature_order.txt"
    joblib.dump(tier_a_model, _io_path(tier_a_model_path))
    joblib.dump(tier_b_model, _io_path(tier_b_model_path))
    _io_path(tier_a_feature_order_path).write_text("\n".join(tier_a_feature_order) + "\n", encoding="utf-8")
    _io_path(tier_b_feature_order_path).write_text("\n".join(tier_b_feature_order) + "\n", encoding="utf-8")

    tier_a_onnx_path = models_root / "tier_a_extratrees_58_model.onnx"
    tier_b_onnx_path = models_root / "tier_b_extratrees_core42_model.onnx"
    tier_a_onnx_export = scout.export_sklearn_to_onnx_zipmap_disabled(
        tier_a_model,
        tier_a_onnx_path,
        feature_count=len(tier_a_feature_order),
    )
    tier_b_onnx_export = scout.export_sklearn_to_onnx_zipmap_disabled(
        tier_b_model,
        tier_b_onnx_path,
        feature_count=len(tier_b_feature_order),
    )
    tier_a_parity_values = tier_a_session.loc[:, tier_a_feature_order].to_numpy(dtype="float64", copy=False)[
        : max(1, min(parity_rows, len(tier_a_session)))
    ]
    tier_b_parity_values = tier_b_session.loc[:, tier_b_feature_order].to_numpy(dtype="float64", copy=False)[
        : max(1, min(parity_rows, len(tier_b_session)))
    ]
    tier_a_onnx_parity = scout.check_onnxruntime_probability_parity(tier_a_model, tier_a_onnx_path, tier_a_parity_values)
    tier_b_onnx_parity = scout.check_onnxruntime_probability_parity(tier_b_model, tier_b_onnx_path, tier_b_parity_values)
    onnx_parity = {
        "passed": bool(tier_a_onnx_parity["passed"] and tier_b_onnx_parity["passed"]),
        "tier_a": tier_a_onnx_parity,
        "tier_b": tier_b_onnx_parity,
    }

    ledger_rows = build_python_ledger_rows(
        run_id=run_id,
        tier_records=tier_records,
        selected_threshold=selected,
        predictions_root=predictions_root,
    )
    ledger_payload = alpha_run_ledgers.materialize_alpha_ledgers(
        stage_run_ledger_path=STAGE_RUN_LEDGER_PATH,
        project_alpha_ledger_path=PROJECT_ALPHA_LEDGER_PATH,
        rows=ledger_rows,
    )
    run_registry_payload = materialize_run_registry_row(
        run_id=run_id,
        run_output_root=run_output_root,
        combined_metrics=tier_records["tier_ab_combined"]["metrics"],
        selected_threshold=selected,
    )

    stage_docs = materialize_stage_docs(
        run_id=run_id,
        run_output_root=run_output_root,
        selected_threshold=selected,
        tier_records=tier_records,
    )

    artifacts = [
        {"role": "tier_a_extratrees_model", "path": tier_a_model_path.as_posix(), "format": "joblib", "sha256": scout.sha256_file(tier_a_model_path)},
        {"role": "tier_b_extratrees_model", "path": tier_b_model_path.as_posix(), "format": "joblib", "sha256": scout.sha256_file(tier_b_model_path)},
        {"role": "tier_a_feature_order", "path": tier_a_feature_order_path.as_posix(), "format": "txt", "sha256": scout.sha256_file(tier_a_feature_order_path)},
        {"role": "tier_b_feature_order", "path": tier_b_feature_order_path.as_posix(), "format": "txt", "sha256": scout.sha256_file(tier_b_feature_order_path)},
        {"role": "tier_a_onnx_model", **tier_a_onnx_export, "format": "onnx"},
        {"role": "tier_b_onnx_model", **tier_b_onnx_export, "format": "onnx"},
        {"role": "onnx_probability_parity", "parity": onnx_parity},
        {"role": "tier_a_predictions", "path": paths["tier_a_predictions"].as_posix(), "format": "parquet", "sha256": scout.sha256_file(paths["tier_a_predictions"])},
        {"role": "tier_b_predictions", "path": paths["tier_b_predictions"].as_posix(), "format": "parquet", "sha256": scout.sha256_file(paths["tier_b_predictions"])},
        {"role": "tier_ab_combined_predictions", "path": paths["tier_ab_combined"].as_posix(), "format": "parquet", "sha256": scout.sha256_file(paths["tier_ab_combined"])},
        {"role": "route_coverage_summary", "path": paths["route_coverage_summary"].as_posix(), "format": "json", "sha256": scout.sha256_file(paths["route_coverage_summary"])},
        {"role": "rank_quantile_sweep_tier_a", "path": sweep_paths["tier_a"].as_posix(), "format": "csv", "sha256": scout.sha256_file(sweep_paths["tier_a"])},
        {"role": "rank_quantile_sweep_tier_b", "path": sweep_paths["tier_b"].as_posix(), "format": "csv", "sha256": scout.sha256_file(sweep_paths["tier_b"])},
        {"role": "rank_quantile_sweep_combined", "path": sweep_paths["combined"].as_posix(), "format": "csv", "sha256": scout.sha256_file(sweep_paths["combined"])},
        {"role": "stage_run_ledger", **ledger_payload["stage_run_ledger"]},
        {"role": "project_alpha_run_ledger", **ledger_payload["project_alpha_run_ledger"]},
        {"role": "project_run_registry", **run_registry_payload},
        {"role": "stage_docs", "paths": stage_docs},
    ]

    manifest = {
        "identity": {
            "run_id": run_id,
            "run_number": run_number,
            "stage_id": STAGE_ID,
            "exploration_label": EXPLORATION_LABEL,
            "model_family": MODEL_FAMILY,
            "lane": "alpha_model_family_challenger",
            "scoreboard_lane": "structural_scout",
            "status": "completed_payload",
            "judgment": "inconclusive_extratrees_structural_scout_payload",
        },
        "hypothesis": (
            "ExtraTrees can produce a different fwd18 inverse-rank context probability surface than "
            "Stage 10 LogReg and Stage 11 LightGBM while the label, split, session, context, and hold stay fixed."
        ),
        "comparison_references": {
            "stage10": RUN01Y_REFERENCE,
            "stage11": RUN02Z_REFERENCE,
        },
        "experiment_design": {
            "decision_use": "Decide whether a non-LightGBM model-family surface deserves an MT5 runtime_probe.",
            "control_variables": {
                "symbol": "US100",
                "timeframe": "M5",
                "label": "label_v1_fwd18_m5_logret_train_q33_3class",
                "split": "split_v1_calendar_train_20220901_20241231_val_20250101_20250930_oos_20251001_20260413",
                "session_slice_id": session_slice_id,
                "context_gate": "abs(di_spread_14)<=8 and adx_14<=25",
                "decision_mode": "inverse_rank",
                "max_hold_bars": max_hold_bars,
            },
            "changed_variables": {"model_family": MODEL_FAMILY},
            "success_criteria": "Enough validation and OOS structural signals with non-fragile directional hit rates.",
            "failure_criteria": "Too few signals or validation/OOS hit rates that do not support an MT5 runtime_probe.",
            "invalid_conditions": "Feature hash mismatch, missing split, non-finite features, or ONNX parity failure.",
            "stop_conditions": "No operating or promotion claim without MT5 Strategy Tester evidence.",
        },
        "data_integrity": {
            "data_source": model_input_path.as_posix(),
            "time_axis": "broker-derived bar close timestamp normalized as UTC for Python artifacts",
            "sample_scope": "Tier A 58-feature full-context and Tier B core42 partial-context rows in fwd18 split v1",
            "split_boundary": "train < 2025-01-01; validation 2025-01-01..2025-09-30; OOS >= 2025-10-01",
            "feature_label_boundary": "features are closed-bar inputs; fwd18 label uses future close only as target",
            "leakage_risk": "validation-selected rank thresholds can overfit; this run is structural only",
            "data_hash_or_identity": {
                "tier_a_model_input_sha256": scout.sha256_file(model_input_path),
                "tier_a_feature_order_hash": tier_a_feature_hash,
                "tier_b_feature_order_hash": tier_b_feature_hash,
            },
            "integrity_judgment": "usable_with_boundary",
        },
        "model_validation": {
            "model_family": MODEL_FAMILY,
            "target_and_label": "3-class short/flat/long fwd18 log-return label",
            "split_method": "fixed chronological train/validation/OOS",
            "selection_metric": "validation rank quantile threshold with structural directional hit read",
            "secondary_metrics": ["macro_f1", "balanced_accuracy", "signal_count", "signal_coverage", "OOS hit_rate"],
            "threshold_policy": "rank quantile q0.96, inverse signal, context filtered",
            "overfit_risk": "threshold and context inherited from Stage 11; model-family testing still adds multiple-testing risk",
            "calibration_risk": "ExtraTrees probabilities are used as ranks, not calibrated probabilities",
            "comparison_baseline": RUN02Z_REFERENCE["run_id"],
            "validation_judgment": "exploratory",
        },
        "environment_reproducibility": {
            "execution_environment": "local Windows PowerShell with repository Python environment",
            "dependency_surface": "sklearn, pandas, numpy, pyarrow, joblib, skl2onnx, onnxruntime",
            "entry_command": "python foundation/pipelines/run_stage12_extratrees_training_effect_scout.py",
            "local_assumptions": "raw MT5 CSVs and processed fwd18 model input already exist in workspace",
            "clean_checkout_status": "reproducible_with_setup",
            "recovery_instruction": "regenerate fwd18 model input artifacts before rerunning if processed data is missing",
            "reproducibility_judgment": "reproducible_with_setup",
        },
        "threshold": {
            "rank_quantile": rank_quantile,
            "tier_a_rule": scout.threshold_rule_payload(tier_a_rule),
            "tier_b_rule": scout.threshold_rule_payload(tier_b_rule),
            "selected_threshold_id": selected,
            "decision_mode": "inverse",
            "context_gate": "di_spread_abs_lte8_adx_lte25",
        },
        "route_coverage": route_coverage,
        "model_metrics": model_metrics,
        "tier_records": tier_records,
        "onnx_probability_parity": onnx_parity,
        "external_verification_status": "out_of_scope_by_claim",
        "artifacts": artifacts,
        "result_judgment": {
            "result_subject": "Stage 12 RUN03A ExtraTrees fwd18 inverse-rank context structural scout",
            "evidence_available": "Python predictions, model metrics, ONNX parity, rank sweeps, ledgers",
            "evidence_missing": "MT5 Strategy Tester output and trading-risk execution KPI",
            "judgment_label": "inconclusive_extratrees_structural_scout_payload",
            "claim_boundary": "new model training effect observed structurally; no runtime or operating claim",
            "next_condition": "run a narrow MT5 runtime_probe only if the structural read is worth external verification",
            "user_explanation_hook": "새 모델은 학습됐지만 아직 거래 실행 효과는 보지 않았다.",
        },
    }
    kpi_record = {
        "run_id": run_id,
        "stage_id": STAGE_ID,
        "scoreboard_lane": "structural_scout",
        "kpi_scope": "model_training_signal_probability_rank_context",
        "model_metrics": model_metrics,
        "signal": tier_records,
        "threshold": manifest["threshold"],
        "route_coverage": route_coverage,
        "onnx_probability_parity": onnx_parity,
        "external_verification_status": "out_of_scope_by_claim",
        "judgment": manifest["result_judgment"],
    }

    manifest_path = run_output_root / "run_manifest.json"
    kpi_path = run_output_root / "kpi_record.json"
    summary_path = run_output_root / "summary.json"
    result_summary_path = reports_root / "result_summary.md"
    write_json(manifest_path, manifest)
    write_json(kpi_path, kpi_record)
    summary = {
        "run_id": run_id,
        "stage_id": STAGE_ID,
        "status": "completed_payload",
        "judgment": "inconclusive_extratrees_structural_scout_payload",
        "selected_threshold_id": selected,
        "model_family": MODEL_FAMILY,
        "model_metrics": model_metrics,
        "tier_records": tier_records,
        "onnx_probability_parity": onnx_parity,
        "external_verification_status": "out_of_scope_by_claim",
        "paths": {
            "run_manifest": manifest_path.as_posix(),
            "kpi_record": kpi_path.as_posix(),
            "summary": summary_path.as_posix(),
            "result_summary": result_summary_path.as_posix(),
            **stage_docs,
        },
    }
    write_json(summary_path, summary)
    write_result_summary(
        result_summary_path,
        run_id=run_id,
        selected_threshold=selected,
        model_metrics=model_metrics,
        tier_records=tier_records,
        onnx_parity=onnx_parity,
    )

    return {
        "status": "ok",
        "run_id": run_id,
        "stage_id": STAGE_ID,
        "selected_threshold_id": selected,
        "summary_path": summary_path.as_posix(),
        "result_summary_path": result_summary_path.as_posix(),
        "manifest_path": manifest_path.as_posix(),
        "kpi_path": kpi_path.as_posix(),
        "combined_signal_metrics": tier_records["tier_ab_combined"]["metrics"],
        "onnx_probability_parity": onnx_parity,
        "external_verification_status": "out_of_scope_by_claim",
    }


def main() -> int:
    args = parse_args()
    payload = run_stage12_extratrees_training_effect_scout(
        model_input_path=Path(args.model_input_path),
        feature_order_path=Path(args.feature_order_path),
        tier_b_reference_model_input_path=Path(args.tier_b_reference_model_input_path),
        tier_b_reference_feature_order_path=Path(args.tier_b_reference_feature_order_path),
        raw_root=Path(args.raw_root),
        training_summary_path=Path(args.training_summary_path),
        run_output_root=Path(args.run_output_root),
        run_id=args.run_id,
        run_number=args.run_number,
        session_slice_id=args.session_slice_id,
        max_hold_bars=args.max_hold_bars,
        rank_quantile=args.rank_quantile,
        tier_a_min_margin=args.tier_a_min_margin,
        tier_b_min_margin=args.tier_b_min_margin,
        parity_rows=args.parity_rows,
    )
    print(json.dumps(scout._json_ready(payload), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
