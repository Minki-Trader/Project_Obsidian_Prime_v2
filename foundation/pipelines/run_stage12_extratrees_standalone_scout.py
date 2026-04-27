from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.metrics import accuracy_score, balanced_accuracy_score, f1_score, log_loss

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.models.baseline_training import (  # noqa: E402
    LABEL_NAMES,
    LABEL_ORDER,
    load_feature_order,
    validate_model_input_frame,
)


STAGE_ID = "12_model_family_challenge__extratrees_training_effect"
RUN_ID = "run03B_et_standalone_fwd12_v1"
RUN_NUMBER = "run03B"
EXPLORATION_LABEL = "stage12_Model__ExtraTreesStandaloneFwd12"
MODEL_FAMILY = "sklearn_extratreesclassifier_multiclass"
MODEL_INPUT_DATASET_ID = "model_input_fpmarkets_v2_us100_m5_label_v1_fwd12_split_v1_proxyw58_feature_set_v2"
FEATURE_SET_ID = "feature_set_v2_mt5_price_proxy_top3_weights_58_features"
FEATURE_ORDER_HASH = "fa06973c24462298ea38d84528b07ca0adf357e506f3bfeea02eb0d5691ab8e2"
THRESHOLD_METHOD = "standalone_validation_nonflat_confidence_q90"
CONFIDENCE_QUANTILE = 0.90

DEFAULT_MODEL_INPUT_PATH = ROOT / (
    "data/processed/model_inputs/"
    "label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_dataset.parquet"
)
DEFAULT_FEATURE_ORDER_PATH = DEFAULT_MODEL_INPUT_PATH.with_name("model_input_feature_order.txt")
STAGE_ROOT = ROOT / "stages" / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_lines(lines: list[str]) -> str:
    payload = "\n".join(lines).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_text(path: Path, text: str, *, bom: bool = False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8-sig" if bom else "utf-8")


def class_distribution(values: np.ndarray) -> dict[str, int]:
    counts = pd.Series(values.astype("int64")).value_counts().to_dict()
    return {LABEL_NAMES[label]: int(counts.get(label, 0)) for label in LABEL_ORDER}


def ordered_predict_proba(model: ExtraTreesClassifier, values: np.ndarray) -> np.ndarray:
    raw = np.asarray(model.predict_proba(values), dtype="float64")
    ordered = np.zeros((raw.shape[0], len(LABEL_ORDER)), dtype="float64")
    class_to_index = {int(label): index for index, label in enumerate(model.classes_)}
    for output_index, label in enumerate(LABEL_ORDER):
        if label in class_to_index:
            ordered[:, output_index] = raw[:, class_to_index[label]]
    return ordered


def train_model(frame: pd.DataFrame, feature_order: list[str]) -> ExtraTreesClassifier:
    train = frame.loc[frame["split"].astype(str).eq("train")]
    x_train = train.loc[:, feature_order].to_numpy(dtype="float64", copy=False)
    y_train = train["label_class"].astype("int64").to_numpy()
    return ExtraTreesClassifier(
        n_estimators=700,
        max_features="sqrt",
        min_samples_leaf=20,
        class_weight="balanced",
        random_state=23,
        n_jobs=-1,
    ).fit(x_train, y_train)


def evaluate_model(
    model: ExtraTreesClassifier,
    frame: pd.DataFrame,
    feature_order: list[str],
) -> tuple[dict[str, Any], pd.DataFrame]:
    metrics: dict[str, Any] = {}
    prediction_parts: list[pd.DataFrame] = []

    for split_name in ("train", "validation", "oos"):
        split_frame = frame.loc[frame["split"].astype(str).eq(split_name)].copy()
        x_values = split_frame.loc[:, feature_order].to_numpy(dtype="float64", copy=False)
        y_true = split_frame["label_class"].astype("int64").to_numpy()
        probabilities = ordered_predict_proba(model, x_values)
        y_pred = np.asarray(LABEL_ORDER, dtype="int64")[probabilities.argmax(axis=1)]

        metrics[split_name] = {
            "rows": int(len(split_frame)),
            "accuracy": float(accuracy_score(y_true, y_pred)),
            "balanced_accuracy": float(balanced_accuracy_score(y_true, y_pred)),
            "macro_f1": float(f1_score(y_true, y_pred, labels=LABEL_ORDER, average="macro")),
            "log_loss": float(log_loss(y_true, probabilities, labels=LABEL_ORDER)),
            "true_class_distribution": class_distribution(y_true),
            "predicted_class_distribution": class_distribution(y_pred),
            "mean_probability": {
                f"p_{LABEL_NAMES[label]}": float(probabilities[:, index].mean())
                for index, label in enumerate(LABEL_ORDER)
            },
        }

        prediction_parts.append(
            pd.DataFrame(
                {
                    "timestamp": pd.to_datetime(split_frame["timestamp"], utc=True).to_numpy(),
                    "symbol": split_frame["symbol"].astype(str).to_numpy(),
                    "split": split_name,
                    "label": split_frame["label"].astype(str).to_numpy(),
                    "label_class": y_true,
                    "predicted_label_class": y_pred,
                    "predicted_label": [LABEL_NAMES[int(value)] for value in y_pred],
                    "p_short": probabilities[:, 0],
                    "p_flat": probabilities[:, 1],
                    "p_long": probabilities[:, 2],
                }
            )
        )

    predictions = pd.concat(prediction_parts, ignore_index=True)
    probs = predictions[["p_short", "p_flat", "p_long"]].to_numpy(dtype="float64", copy=False)
    metrics["probability_checks"] = {
        "finite": bool(np.isfinite(probs).all()),
        "row_sum_max_abs_error": float(np.abs(probs.sum(axis=1) - 1.0).max()),
    }
    return metrics, predictions


def apply_standalone_signal_rule(predictions: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, Any]]:
    scored = predictions.copy()
    scored["nonflat_confidence"] = scored[["p_short", "p_long"]].max(axis=1)
    scored["predicted_nonflat_class"] = np.where(scored["p_short"] >= scored["p_long"], 0, 2)

    validation = scored.loc[scored["split"].astype(str).eq("validation")]
    validation_nonflat = validation.loc[validation["predicted_label_class"].isin([0, 2])]
    if validation_nonflat.empty:
        threshold = float("nan")
    else:
        threshold = float(validation_nonflat["nonflat_confidence"].quantile(CONFIDENCE_QUANTILE))

    scored["standalone_threshold"] = threshold
    scored["decision_class"] = 1
    mask = scored["predicted_label_class"].isin([0, 2]) & scored["nonflat_confidence"].ge(threshold)
    scored.loc[mask, "decision_class"] = scored.loc[mask, "predicted_nonflat_class"].astype("int64")
    scored["decision_label"] = scored["decision_class"].map(LABEL_NAMES)
    scored["is_signal"] = scored["decision_class"].isin([0, 2])
    scored["directional_correct"] = scored["is_signal"] & (
        scored["decision_class"].astype("int64") == scored["label_class"].astype("int64")
    )

    rule = {
        "threshold_method": THRESHOLD_METHOD,
        "confidence_quantile": CONFIDENCE_QUANTILE,
        "nonflat_confidence_threshold": threshold,
        "selection_split": "validation",
        "decision_policy": "predict short or long only when predicted non-flat class confidence is at or above the validation q90 threshold",
        "inherited_from_stage10_or_stage11": False,
    }
    return scored, rule


def signal_metrics(scored: pd.DataFrame) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "rows": int(len(scored)),
        "signal_count": int(scored["is_signal"].sum()),
        "short_count": int(scored["decision_class"].eq(0).sum()),
        "long_count": int(scored["decision_class"].eq(2).sum()),
        "signal_coverage": float(scored["is_signal"].mean()) if len(scored) else None,
        "directional_correct_count": int(scored["directional_correct"].sum()),
        "directional_hit_rate": (
            float(scored.loc[scored["is_signal"], "directional_correct"].mean())
            if bool(scored["is_signal"].any())
            else None
        ),
        "by_split": {},
    }
    for split_name in ("train", "validation", "oos"):
        split = scored.loc[scored["split"].astype(str).eq(split_name)]
        signals = split.loc[split["is_signal"]]
        payload["by_split"][split_name] = {
            "rows": int(len(split)),
            "signal_count": int(len(signals)),
            "short_count": int(signals["decision_class"].eq(0).sum()),
            "long_count": int(signals["decision_class"].eq(2).sum()),
            "signal_coverage": float(len(signals) / len(split)) if len(split) else None,
            "directional_correct_count": int(signals["directional_correct"].sum()) if len(signals) else 0,
            "directional_hit_rate": (
                float(signals["directional_correct"].mean()) if len(signals) else None
            ),
        }
    return payload


def feature_importance_frame(model: ExtraTreesClassifier, feature_order: list[str]) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "feature": feature_order,
            "importance": np.asarray(model.feature_importances_, dtype="float64"),
        }
    ).sort_values(["importance", "feature"], ascending=[False, True])


def csv_upsert(path: Path, rows: list[dict[str, str]], key: str, fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    existing: list[dict[str, str]] = []
    if path.exists():
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            for row in reader:
                existing.append({name: row.get(name, "") for name in fieldnames})

    by_key = {row.get(key, ""): row for row in existing if row.get(key, "")}
    for row in rows:
        by_key[row[key]] = {name: str(row.get(name, "")) for name in fieldnames}

    ordered_keys = [row.get(key, "") for row in existing if row.get(key, "")]
    for row in rows:
        if row[key] not in ordered_keys:
            ordered_keys.append(row[key])

    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for item_key in ordered_keys:
            writer.writerow(by_key[item_key])


def update_registries(
    summary: dict[str, Any],
    signal: dict[str, Any],
    scored_path: Path,
    summary_path: Path,
) -> None:
    run_registry_path = ROOT / "docs/registers/run_registry.csv"
    run_registry_fields = ["run_id", "stage_id", "lane", "status", "judgment", "path", "notes"]
    run03a_path = f"stages/{STAGE_ID}/02_runs/run03A_extratrees_fwd18_inverse_context_scout_v1"
    csv_upsert(
        run_registry_path,
        [
            {
                "run_id": "run03A_extratrees_fwd18_inverse_context_scout_v1",
                "stage_id": STAGE_ID,
                "lane": "alpha_model_family_challenger",
                "status": "invalid_for_standalone_scope",
                "judgment": "invalid_scope_mismatch_for_requested_standalone_stage12",
                "path": run03a_path,
                "notes": "RUN03A reused Stage 10/11 comparison and Stage 11 context surface; keep only as superseded scope-mismatch evidence, not standalone Stage 12 evidence.",
            },
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "standalone_model_family_training_effect",
                "status": "completed",
                "judgment": summary["judgment"],
                "path": rel(RUN_ROOT),
                "notes": (
                    "model_family=sklearn_extratreesclassifier_multiclass;"
                    f"dataset_id={MODEL_INPUT_DATASET_ID};"
                    f"threshold_method={THRESHOLD_METHOD};"
                    f"validation_signal_count={signal['by_split']['validation']['signal_count']};"
                    f"validation_hit_rate={signal['by_split']['validation']['directional_hit_rate']};"
                    f"oos_signal_count={signal['by_split']['oos']['signal_count']};"
                    f"oos_hit_rate={signal['by_split']['oos']['directional_hit_rate']};"
                    "stage10_11_inheritance=false;external_verification=out_of_scope_by_claim;"
                    "boundary=python_standalone_training_effect_only"
                ),
            },
        ],
        key="run_id",
        fieldnames=run_registry_fields,
    )

    ledger_fields = [
        "ledger_row_id",
        "stage_id",
        "run_id",
        "subrun_id",
        "parent_run_id",
        "record_view",
        "tier_scope",
        "kpi_scope",
        "scoreboard_lane",
        "status",
        "judgment",
        "path",
        "primary_kpi",
        "guardrail_kpi",
        "external_verification_status",
        "notes",
    ]
    ledger_rows = [
        {
            "ledger_row_id": f"{RUN_ID}__python_tier_a_standalone",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "python_tier_a_standalone",
            "parent_run_id": RUN_ID,
            "record_view": "python_tier_a_standalone",
            "tier_scope": "Tier A",
            "kpi_scope": "standalone_model_training_signal_probability",
            "scoreboard_lane": "standalone_structural_scout",
            "status": "completed",
            "judgment": summary["judgment"],
            "path": rel(scored_path),
            "primary_kpi": (
                f"rows={signal['rows']};signal_count={signal['signal_count']};"
                f"coverage={signal['signal_coverage']};hit_rate={signal['directional_hit_rate']};"
                f"validation_signals={signal['by_split']['validation']['signal_count']};"
                f"oos_signals={signal['by_split']['oos']['signal_count']}"
            ),
            "guardrail_kpi": (
                f"stage10_11_inheritance=false;threshold_method={THRESHOLD_METHOD};"
                f"feature_order_hash={FEATURE_ORDER_HASH};model_family={MODEL_FAMILY}"
            ),
            "external_verification_status": "out_of_scope_by_claim",
            "notes": "Standalone Tier A full-context Python structural scout; no Stage 10/11 threshold, context, session, or comparison baseline used.",
        },
        {
            "ledger_row_id": f"{RUN_ID}__python_tier_b_separate",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "python_tier_b_separate",
            "parent_run_id": RUN_ID,
            "record_view": "python_tier_b_separate",
            "tier_scope": "Tier B",
            "kpi_scope": "paired_tier_record_boundary",
            "scoreboard_lane": "standalone_structural_scout",
            "status": "not_produced",
            "judgment": "out_of_scope_by_claim_standalone_tier_a_only",
            "path": rel(summary_path),
            "primary_kpi": "missing_required=out_of_scope_by_claim",
            "guardrail_kpi": "reason=standalone_full_context_training_effect_no_partial_context_fallback_claim",
            "external_verification_status": "out_of_scope_by_claim",
            "notes": "Required paired-tier record is present as boundary; Tier B was not used because the standalone claim is Tier A full-context only.",
        },
        {
            "ledger_row_id": f"{RUN_ID}__python_tier_ab_combined",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "python_tier_ab_combined",
            "parent_run_id": RUN_ID,
            "record_view": "python_tier_ab_combined",
            "tier_scope": "Tier A+B",
            "kpi_scope": "paired_tier_record_boundary",
            "scoreboard_lane": "standalone_structural_scout",
            "status": "not_produced",
            "judgment": "out_of_scope_by_claim_standalone_tier_a_only",
            "path": rel(summary_path),
            "primary_kpi": "missing_required=out_of_scope_by_claim",
            "guardrail_kpi": "reason=no_tier_b_fallback_or_routed_total_claim_in_standalone_run",
            "external_verification_status": "out_of_scope_by_claim",
            "notes": "Required combined record is present as boundary; no synthetic combined result is claimed.",
        },
    ]
    for suffix in ("python_tier_a_separate", "python_tier_b_separate", "python_tier_ab_combined"):
        ledger_rows.append(
            {
                "ledger_row_id": f"run03A_extratrees_fwd18_inverse_context_scout_v1__{suffix}",
                "stage_id": STAGE_ID,
                "run_id": "run03A_extratrees_fwd18_inverse_context_scout_v1",
                "subrun_id": suffix,
                "parent_run_id": "run03A_extratrees_fwd18_inverse_context_scout_v1",
                "record_view": suffix,
                "tier_scope": "scope_mismatch",
                "kpi_scope": "superseded_scope_mismatch",
                "scoreboard_lane": "not_standalone_evidence",
                "status": "invalid_for_standalone_scope",
                "judgment": "invalid_scope_mismatch_for_requested_standalone_stage12",
                "path": run03a_path,
                "primary_kpi": "not_used_for_standalone_stage12",
                "guardrail_kpi": "reason=used_stage10_11_comparison_and_stage11_context_surface",
                "external_verification_status": "out_of_scope_by_claim",
                "notes": "Superseded by RUN03B standalone design.",
            }
        )

    csv_upsert(ROOT / "docs/registers/alpha_run_ledger.csv", ledger_rows, "ledger_row_id", ledger_fields)
    csv_upsert(STAGE_ROOT / "03_reviews/stage_run_ledger.csv", ledger_rows, "ledger_row_id", ledger_fields)


def write_stage_docs(
    summary: dict[str, Any],
    signal: dict[str, Any],
    threshold_rule: dict[str, Any],
    paths: dict[str, str],
) -> None:
    stage_brief = f"""# Stage 12 Standalone ExtraTrees Training Effect

## 질문(Question, 질문)

Stage 12(12단계)는 Stage 10/11(10/11단계)을 계승하지 않는 standalone(단독) 새 모델 실험이다.

효과(effect, 효과): 기존 run(실행), threshold(임계값), context gate(문맥 제한), session slice(세션 구간), comparison baseline(비교 기준선)을 가져오지 않고 ExtraTrees(엑스트라 트리) 자체 학습 효과만 본다.

## 범위(Scope, 범위)

- model family(모델 계열): `ExtraTreesClassifier(엑스트라 트리 분류기)`
- dataset(데이터셋): `{MODEL_INPUT_DATASET_ID}`
- label(라벨): fwd12(60분) canonical foundation label(정식 기반 라벨)
- feature set(피처 묶음): `{FEATURE_SET_ID}`
- threshold method(임계값 방식): `{THRESHOLD_METHOD}`

## 명시적 비계승(Explicit Non-Inheritance, 명시적 비계승)

- Stage 10(10단계) threshold(임계값): not used(미사용)
- Stage 10(10단계) session slice(세션 구간): not used(미사용)
- Stage 11(11단계) LightGBM(라이트GBM) surface(표면): not used(미사용)
- Stage 11(11단계) fwd18 inverse context(fwd18 역방향 문맥): not used(미사용)

## 경계(Boundary, 경계)

Python structural scout(파이썬 구조 탐침)만 주장한다. MT5 runtime_probe(MT5 런타임 탐침), alpha quality(알파 품질), live readiness(실거래 준비), operating promotion(운영 승격)은 주장하지 않는다.
"""
    plan = f"""# RUN03B Standalone ExtraTrees Plan

## Intake(인입)

- active stage(활성 단계): `{STAGE_ID}`
- run_id(실행 ID): `{RUN_ID}`
- standalone rule(단독 규칙): Stage 10/11(10/11단계) run artifact(실행 산출물)와 기준선(baseline, 기준선)을 쓰지 않는다.

## Experiment Design(실험 설계)

- hypothesis(가설): ExtraTrees(엑스트라 트리)를 foundation model input(기반 모델 입력)에 단독 학습하면 새 확률 표면(probability surface, 확률 표면)과 신호 밀도(signal density, 신호 밀도)를 볼 수 있다.
- decision_use(결정 용도): Stage 12(12단계)에서 standalone(단독) 새 모델 축을 더 팔 가치가 있는지 판단한다.
- comparison_baseline(비교 기준): `none(없음)`
- control_variables(통제 변수): `US100`, `M5`, canonical fwd12 label/split(정식 fwd12 라벨/분할), 58 feature MT5 price-proxy input(58개 피처 MT5 가격 대리 입력)
- changed_variables(변경 변수): model family(모델 계열) = `ExtraTreesClassifier(엑스트라 트리 분류기)`
- sample_scope(표본 범위): Tier A full-context(Tier A 전체 문맥) Python data(파이썬 데이터)
- success_criteria(성공 기준): validation/OOS(검증/표본외)에서 충분한 standalone signals(단독 신호)와 hit rate(적중률)
- failure_criteria(실패 기준): OOS(표본외) hit rate(적중률)가 약하거나 신호가 과하게 적음
- invalid_conditions(무효 조건): feature hash(피처 해시) 불일치, split(분할) 누락, 비유한값(non-finite, 비유한값)
- stop_conditions(중지 조건): MT5(메타트레이더5) 없이 운영 의미(operational meaning, 운영 의미)를 주장하지 않는다.
- evidence_plan(근거 계획): manifest(목록), KPI(핵심 성과 지표), predictions(예측), ledgers(장부), result summary(결과 요약)
"""
    correction = """# RUN03A Scope Correction

RUN03A(실행 03A)는 Stage 10/11(10/11단계) comparison reference(비교 기준)와 Stage 11(11단계) context surface(문맥 표면)를 사용했다.

효과(effect, 효과): 사용자 의도인 standalone Stage 12(단독 12단계)와 맞지 않으므로, RUN03A(실행 03A)는 `invalid_for_standalone_scope(단독 범위 무효)`로 낮춘다.

RUN03B(실행 03B)가 standalone(단독) 재실행 근거다.
"""
    packet = f"""# RUN03B Standalone ExtraTrees Packet

- run_id(실행 ID): `{RUN_ID}`
- model family(모델 계열): `{MODEL_FAMILY}`
- threshold method(임계값 방식): `{THRESHOLD_METHOD}`
- nonflat confidence threshold(비평탄 확신 임계값): `{threshold_rule['nonflat_confidence_threshold']}`
- boundary(경계): `Python structural scout(파이썬 구조 탐침)` only(전용)

## Result Read(결과 판독)

| split(분할) | rows(행) | signals(신호) | coverage(비율) | hit rate(적중률) |
|---|---:|---:|---:|---:|
| train(학습) | `{signal['by_split']['train']['rows']}` | `{signal['by_split']['train']['signal_count']}` | `{signal['by_split']['train']['signal_coverage']}` | `{signal['by_split']['train']['directional_hit_rate']}` |
| validation(검증) | `{signal['by_split']['validation']['rows']}` | `{signal['by_split']['validation']['signal_count']}` | `{signal['by_split']['validation']['signal_coverage']}` | `{signal['by_split']['validation']['directional_hit_rate']}` |
| OOS(표본외) | `{signal['by_split']['oos']['rows']}` | `{signal['by_split']['oos']['signal_count']}` | `{signal['by_split']['oos']['signal_coverage']}` | `{signal['by_split']['oos']['directional_hit_rate']}` |

## Judgment(판정)

`{summary['judgment']}`

효과(effect, 효과): 이번 판정은 ExtraTrees(엑스트라 트리) standalone(단독) 학습 효과에만 붙는다. Stage 10/11(10/11단계) 계승 판정이 아니다.

## Paths(경로)

- manifest(목록): `{paths['manifest']}`
- KPI(핵심 성과 지표): `{paths['kpi']}`
- summary(요약): `{paths['summary']}`
- predictions(예측): `{paths['predictions']}`
"""
    selection = f"""# Selection Status

## 현재 판독(Current Read, 현재 판독)

- stage(단계): `{STAGE_ID}`
- status(상태): `active_standalone_structural_scout_open(단독 구조 탐침 활성)`
- current run(현재 실행): `{RUN_ID}`
- current model family(현재 모델 계열): `{MODEL_FAMILY}`
- current operating reference(현재 운영 기준): `none(없음)`
- selected promotion candidate(선택 승격 후보): `none(없음)`

## RUN03A Correction(RUN03A 정정)

RUN03A(실행 03A)는 Stage 10/11(10/11단계) 표면을 끌고 왔으므로 standalone evidence(단독 근거)가 아니다.

## RUN03B Standalone(RUN03B 단독)

- validation signals(검증 신호): `{signal['by_split']['validation']['signal_count']}`
- validation hit rate(검증 적중률): `{signal['by_split']['validation']['directional_hit_rate']}`
- OOS signals(표본외 신호): `{signal['by_split']['oos']['signal_count']}`
- OOS hit rate(표본외 적중률): `{signal['by_split']['oos']['directional_hit_rate']}`
- external verification status(외부 검증 상태): `out_of_scope_by_claim(주장 범위 밖)`

효과(effect, 효과): Stage 12(12단계)는 단독 실험으로 다시 잡혔고, RUN03B(실행 03B)가 현재 기준 산출물이다.
"""
    result_summary = f"""# RUN03B Standalone ExtraTrees Result Summary

RUN03B(실행 03B)는 Stage 10/11(10/11단계)을 계승하지 않는 standalone(단독) ExtraTrees(엑스트라 트리) 학습 효과 탐침이다.

| split(분할) | macro F1(매크로 F1) | signals(신호) | hit rate(적중률) |
|---|---:|---:|---:|
| validation(검증) | `{summary['model_metrics']['validation']['macro_f1']}` | `{signal['by_split']['validation']['signal_count']}` | `{signal['by_split']['validation']['directional_hit_rate']}` |
| OOS(표본외) | `{summary['model_metrics']['oos']['macro_f1']}` | `{signal['by_split']['oos']['signal_count']}` | `{signal['by_split']['oos']['directional_hit_rate']}` |

판정(judgment, 판정): `{summary['judgment']}`

효과(effect, 효과): 모델은 학습됐고 독립 신호 규칙도 만들어졌지만, MT5 runtime_probe(MT5 런타임 탐침)나 운영 의미(operational meaning, 운영 의미)는 아직 없다.
"""

    write_text(STAGE_ROOT / "00_spec/stage_brief.md", stage_brief, bom=True)
    write_text(STAGE_ROOT / "00_spec/run03B_standalone_extratrees_plan.md", plan, bom=True)
    write_text(STAGE_ROOT / "03_reviews/run03A_scope_correction.md", correction, bom=True)
    write_text(STAGE_ROOT / "03_reviews/run03B_standalone_extratrees_packet.md", packet, bom=True)
    write_text(STAGE_ROOT / "04_selected/selection_status.md", selection, bom=True)
    write_text(RUN_ROOT / "reports/result_summary.md", result_summary, bom=True)


def run(args: argparse.Namespace) -> dict[str, Any]:
    for path in (
        RUN_ROOT / "models",
        RUN_ROOT / "predictions",
        RUN_ROOT / "reports",
        RUN_ROOT / "feature_importance",
        STAGE_ROOT / "00_spec",
        STAGE_ROOT / "03_reviews",
        STAGE_ROOT / "04_selected",
    ):
        path.mkdir(parents=True, exist_ok=True)

    feature_order = load_feature_order(args.feature_order_path)
    feature_hash = sha256_lines(feature_order)
    if feature_hash != FEATURE_ORDER_HASH:
        raise RuntimeError(f"Feature order hash mismatch: {feature_hash} != {FEATURE_ORDER_HASH}")

    frame = pd.read_parquet(args.model_input_path)
    validate_model_input_frame(frame, feature_order)

    model = train_model(frame, feature_order)
    model_metrics, predictions = evaluate_model(model, frame, feature_order)
    scored, threshold_rule = apply_standalone_signal_rule(predictions)
    signal = signal_metrics(scored)

    model_path = RUN_ROOT / "models/model.joblib"
    feature_order_path = RUN_ROOT / "models/features.txt"
    predictions_path = RUN_ROOT / "predictions/preds.parquet"
    scored_path = RUN_ROOT / "predictions/scored.parquet"
    importance_path = RUN_ROOT / "feature_importance/fi.csv"
    threshold_path = RUN_ROOT / "threshold_rule.json"
    manifest_path = RUN_ROOT / "run_manifest.json"
    kpi_path = RUN_ROOT / "kpi_record.json"
    summary_path = RUN_ROOT / "summary.json"

    joblib.dump(model, model_path)
    write_text(feature_order_path, "\n".join(feature_order) + "\n")
    predictions.to_parquet(predictions_path, index=False)
    scored.to_parquet(scored_path, index=False)
    feature_importance_frame(model, feature_order).to_csv(importance_path, index=False)
    write_json(threshold_path, threshold_rule)

    judgment = "inconclusive_standalone_extratrees_training_effect"
    if (
        signal["by_split"]["validation"]["signal_count"] >= 50
        and signal["by_split"]["oos"]["signal_count"] >= 30
        and (signal["by_split"]["validation"]["directional_hit_rate"] or 0.0) > 0.45
        and (signal["by_split"]["oos"]["directional_hit_rate"] or 0.0) > 0.45
    ):
        judgment = "positive_standalone_structural_scout_candidate_not_runtime"
    elif (
        signal["by_split"]["validation"]["signal_count"] > 0
        and signal["by_split"]["oos"]["signal_count"] > 0
        and (signal["by_split"]["oos"]["directional_hit_rate"] or 0.0) < 0.40
    ):
        judgment = "negative_standalone_extratrees_signal_quality"

    artifacts = [
        {"role": "model", "path": rel(model_path), "sha256": sha256_file(model_path)},
        {"role": "feature_order", "path": rel(feature_order_path), "sha256": sha256_file(feature_order_path)},
        {"role": "predictions", "path": rel(predictions_path), "sha256": sha256_file(predictions_path)},
        {"role": "scored_predictions", "path": rel(scored_path), "sha256": sha256_file(scored_path)},
        {"role": "feature_importance", "path": rel(importance_path), "sha256": sha256_file(importance_path)},
        {"role": "threshold_rule", "path": rel(threshold_path), "sha256": sha256_file(threshold_path)},
    ]
    summary = {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "status": "completed",
        "judgment": judgment,
        "exploration_label": EXPLORATION_LABEL,
        "model_family": MODEL_FAMILY,
        "standalone_scope": True,
        "stage10_11_inheritance": False,
        "model_input_dataset_id": MODEL_INPUT_DATASET_ID,
        "feature_set_id": FEATURE_SET_ID,
        "feature_order_hash": feature_hash,
        "model_metrics": model_metrics,
        "signal_metrics": signal,
        "threshold_rule": threshold_rule,
        "tier_records": {
            "tier_a_separate": {"status": "completed", "metrics": signal},
            "tier_b_separate": {
                "status": "not_produced",
                "judgment": "out_of_scope_by_claim_standalone_tier_a_only",
            },
            "tier_ab_combined": {
                "status": "not_produced",
                "judgment": "out_of_scope_by_claim_standalone_tier_a_only",
            },
        },
        "external_verification_status": "out_of_scope_by_claim",
        "artifacts": artifacts,
        "result_judgment": {
            "result_subject": "Stage 12 RUN03B standalone ExtraTrees training effect scout",
            "evidence_available": "Tier A full-context Python model metrics, standalone confidence signal rule, predictions, feature importance, ledgers",
            "evidence_missing": "Tier B partial-context model, combined routed view, MT5 Strategy Tester output, trading-risk execution KPI",
            "judgment_label": judgment,
            "claim_boundary": "standalone Python structural training effect only; no Stage 10/11 inheritance and no runtime or operating claim",
            "next_condition": "only create a new run if the standalone threshold or model design is intentionally changed before any MT5 runtime_probe",
            "user_explanation_hook": "새 모델은 단독으로 학습했지만 아직 거래 실행 효과는 보지 않았다.",
        },
    }

    write_json(kpi_path, {"run_id": RUN_ID, "kpi_scope": "standalone_model_training_effect", **summary})
    write_json(summary_path, summary)
    manifest = {
        "identity": {
            "run_id": RUN_ID,
            "run_number": RUN_NUMBER,
            "stage_id": STAGE_ID,
            "exploration_label": EXPLORATION_LABEL,
            "model_family": MODEL_FAMILY,
            "status": "completed",
            "judgment": judgment,
        },
        "experiment_design": {
            "hypothesis": "ExtraTrees standalone model training can be evaluated without Stage 10/11 thresholds, context gates, session slices, or comparison baselines.",
            "decision_use": "Decide whether the standalone model family deserves more standalone design work.",
            "comparison_baseline": None,
            "control_variables": {
                "symbol": "US100",
                "timeframe": "M5",
                "dataset": MODEL_INPUT_DATASET_ID,
                "feature_set": FEATURE_SET_ID,
            },
            "changed_variables": {"model_family": MODEL_FAMILY},
            "sample_scope": "Tier A full-context fwd12 split v1 Python model input",
            "success_criteria": "sufficient validation/OOS standalone signals with non-fragile directional hit rate",
            "failure_criteria": "weak OOS hit rate or sparse/unstable standalone signals",
            "invalid_conditions": "feature hash mismatch, missing split, non-finite features",
            "stop_conditions": "no MT5 or operating claim without external verification",
            "evidence_plan": "manifest, KPI record, summary, predictions, feature importance, ledgers",
        },
        "non_inheritance_guardrail": {
            "stage10_threshold_used": False,
            "stage10_session_slice_used": False,
            "stage11_lightgbm_surface_used": False,
            "stage11_fwd18_inverse_context_used": False,
            "comparison_reference_used": False,
        },
        "paths": {
            "kpi_record": rel(kpi_path),
            "summary": rel(summary_path),
            "result_summary": rel(RUN_ROOT / "reports/result_summary.md"),
        },
        "artifacts": artifacts,
    }
    write_json(manifest_path, manifest)

    paths = {
        "manifest": rel(manifest_path),
        "kpi": rel(kpi_path),
        "summary": rel(summary_path),
        "predictions": rel(scored_path),
    }
    write_stage_docs(summary, signal, threshold_rule, paths)
    update_registries(summary, signal, scored_path, summary_path)
    return {
        "status": "ok",
        "run_id": RUN_ID,
        "judgment": judgment,
        "summary_path": rel(summary_path),
        "signal_metrics": signal,
        "stage10_11_inheritance": False,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Stage 12 standalone ExtraTrees scout.")
    parser.add_argument("--model-input-path", default=str(DEFAULT_MODEL_INPUT_PATH))
    parser.add_argument("--feature-order-path", default=str(DEFAULT_FEATURE_ORDER_PATH))
    return parser.parse_args()


def main() -> None:
    print(json.dumps(run(parse_args()), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
