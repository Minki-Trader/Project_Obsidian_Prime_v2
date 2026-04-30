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
from foundation.alpha import scout_runner as scout  # noqa: E402


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


