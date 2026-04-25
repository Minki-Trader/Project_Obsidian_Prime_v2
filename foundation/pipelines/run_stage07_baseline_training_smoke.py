from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

import joblib
import numpy as np
import pandas as pd


REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.models.baseline_training import (  # noqa: E402
    BaselineTrainingConfig,
    LABEL_NAMES,
    LABEL_ORDER,
    coefficient_importance,
    evaluate_model,
    load_feature_order,
    train_baseline_model,
)


RUN_ID = "20260425_stage07_baseline_training_smoke_v1"
STAGE_ID = "07_model_training_baseline__contract_preprocessing_smoke"
MODEL_INPUT_DATASET_ID = "model_input_fpmarkets_v2_us100_m5_label_v1_fwd12_split_v1_proxyw58_feature_set_v2"
FEATURE_SET_ID = "feature_set_v2_mt5_price_proxy_top3_weights_58_features"
MODEL_ARTIFACT_ID = "model_fpmarkets_v2_stage07_logreg_smoke_v1"
DEFAULT_MODEL_INPUT_PATH = Path(
    "data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/model_input_dataset.parquet"
)
DEFAULT_MODEL_INPUT_SUMMARY_PATH = DEFAULT_MODEL_INPUT_PATH.with_name("model_input_summary.json")
DEFAULT_FEATURE_ORDER_PATH = DEFAULT_MODEL_INPUT_PATH.with_name("model_input_feature_order.txt")
DEFAULT_STAGE06_REPORT_PATH = Path(
    "stages/06_runtime_parity__python_mt5_runtime_authority/02_runs/"
    "20260425_stage06_runtime_parity_closed_v1/runtime_parity_report.json"
)
DEFAULT_RUN_OUTPUT_ROOT = Path("stages") / STAGE_ID / "02_runs" / RUN_ID
FEATURE_ORDER_HASH = "fa06973c24462298ea38d84528b07ca0adf357e506f3bfeea02eb0d5691ab8e2"
TRAINING_CONTRACT_VERSION = "docs/contracts/training_label_split_contract_fpmarkets_v2.md@2026-04-25"
MODEL_INPUT_CONTRACT_VERSION = "docs/contracts/model_input_feature_set_contract_fpmarkets_v2.md@2026-04-25"
RUNTIME_PARITY_CONTRACT_VERSION = "docs/contracts/runtime_parity_and_artifact_identity_contract_fpmarkets_v2.md@2026-04-25"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Stage 07 baseline model training smoke.")
    parser.add_argument("--model-input-path", default=str(DEFAULT_MODEL_INPUT_PATH))
    parser.add_argument("--model-input-summary-path", default=str(DEFAULT_MODEL_INPUT_SUMMARY_PATH))
    parser.add_argument("--feature-order-path", default=str(DEFAULT_FEATURE_ORDER_PATH))
    parser.add_argument("--stage06-report-path", default=str(DEFAULT_STAGE06_REPORT_PATH))
    parser.add_argument("--run-output-root", default=str(DEFAULT_RUN_OUTPUT_ROOT))
    parser.add_argument("--random-seed", type=int, default=7)
    parser.add_argument("--max-iter", type=int, default=2000)
    return parser.parse_args()


def _io_path(path: Path) -> Path:
    resolved = path.resolve()
    if sys.platform == "win32":
        text = str(resolved)
        if not text.startswith("\\\\?\\"):
            return Path("\\\\?\\" + text)
    return resolved


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with _io_path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def ordered_hash(names: list[str]) -> str:
    return hashlib.sha256("\n".join(names).encode("utf-8")).hexdigest()


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(_io_path(path).read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    _io_path(path.parent).mkdir(parents=True, exist_ok=True)
    _io_path(path).write_text(json.dumps(_json_ready(payload), indent=2), encoding="utf-8")


def write_md(path: Path, text: str) -> None:
    _io_path(path.parent).mkdir(parents=True, exist_ok=True)
    _io_path(path).write_text(text, encoding="utf-8-sig")


def _json_ready(value: Any) -> Any:
    if isinstance(value, pd.Timestamp):
        return value.isoformat()
    if isinstance(value, dict):
        return {key: _json_ready(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_json_ready(item) for item in value]
    if isinstance(value, tuple):
        return [_json_ready(item) for item in value]
    if isinstance(value, np.integer):
        return int(value)
    if isinstance(value, np.floating):
        return float(value)
    if isinstance(value, np.bool_):
        return bool(value)
    return value


def split_summary(frame: pd.DataFrame) -> dict[str, dict[str, Any]]:
    payload: dict[str, dict[str, Any]] = {}
    for split_name in ("train", "validation", "oos"):
        split_frame = frame.loc[frame["split"].astype(str).eq(split_name)]
        payload[split_name] = {
            "rows": int(len(split_frame)),
            "first_timestamp": pd.to_datetime(split_frame["timestamp"], utc=True).min(),
            "last_timestamp": pd.to_datetime(split_frame["timestamp"], utc=True).max(),
        }
    return payload


def preprocessing_policy_markdown(config: BaselineTrainingConfig, feature_count: int) -> str:
    return "\n".join(
        [
            "# Stage 07 Preprocessing Policy",
            "",
            "## 정책(Policy, 정책)",
            "",
            "- scaler(스케일러): `StandardScaler` fitted on train split only(학습 분할에만 적합)",
            "- imputation(결측 대체): `none`; finite feature values required(유한 피처값 필요)",
            f"- feature count(피처 수): `{feature_count}`",
            f"- feature order hash(피처 순서 해시): `{FEATURE_ORDER_HASH}`",
            "- label order(라벨 순서): `[short, flat, long]` as classes `[0, 1, 2]`",
            f"- model family(모델 계열): `{config.model_family}`",
            f"- random seed(난수 시드): `{config.random_seed}`",
            "",
            "## 효과(Effect, 효과)",
            "",
            "이 정책(policy, 정책)은 validation/OOS(검증/표본외) 정보를 scaler(스케일러)에 섞지 않는다.",
            "효과(effect, 효과)는 baseline smoke training(기준선 스모크 학습)이 재현 가능한 전처리 계약(preprocessing contract, 전처리 계약)을 갖는 것이다.",
            "",
            "## 경계(Boundary, 경계)",
            "",
            "이 정책은 pipeline smoke(처리 흐름 스모크)를 위한 것이다. alpha quality(알파 품질), live readiness(실거래 준비), operating promotion(운영 승격)을 주장하지 않는다.",
            "",
        ]
    )


def result_summary_markdown(summary: dict[str, Any]) -> str:
    metrics = summary["metrics"]
    lines = [
        "# Stage 07 Baseline Training Smoke v1",
        "",
        f"- run_id(실행 ID): `{summary['run_id']}`",
        f"- judgment(판정): `{summary['judgment']}`",
        f"- model_artifact_id(모델 산출물 ID): `{summary['model_artifact_id']}`",
        f"- model family(모델 계열): `{summary['model_family']}`",
        f"- feature count(피처 수): `{summary['feature_count']}`",
        f"- feature order hash(피처 순서 해시): `{summary['feature_order_hash']}`",
        "",
        "## Metrics(지표)",
        "",
    ]
    for split_name in ("train", "validation", "oos"):
        split_metrics = metrics[split_name]
        lines.append(
            "- "
            f"{split_name}: rows(행 수)=`{split_metrics['rows']}`, "
            f"accuracy(정확도)=`{split_metrics['accuracy']:.6f}`, "
            f"macro_f1(매크로 F1)=`{split_metrics['macro_f1']:.6f}`, "
            f"log_loss(로그 손실)=`{split_metrics['log_loss']:.6f}`"
        )
    lines.extend(
        [
            "",
            "## Boundary(경계)",
            "",
            "이 실행(run, 실행)은 Python-side training smoke(파이썬 측 학습 스모크)다.",
            "효과(effect, 효과)는 model input(모델 입력), preprocessing policy(전처리 정책), model artifact identity(모델 산출물 정체성), KPI record(KPI 기록)를 한 실행 근거(run evidence, 실행 근거)로 묶는 것이다.",
            "",
            "이 결과(result, 결과)는 alpha quality(알파 품질), live readiness(실거래 준비), operating promotion(운영 승격)을 주장하지 않는다.",
            "",
        ]
    )
    return "\n".join(lines)


def run_stage07_baseline_training_smoke(
    *,
    model_input_path: Path,
    model_input_summary_path: Path,
    feature_order_path: Path,
    stage06_report_path: Path,
    run_output_root: Path,
    random_seed: int,
    max_iter: int,
) -> dict[str, Any]:
    feature_order = load_feature_order(feature_order_path)
    feature_hash = ordered_hash(feature_order)
    if feature_hash != FEATURE_ORDER_HASH:
        raise RuntimeError(f"Feature order hash mismatch: {feature_hash} != {FEATURE_ORDER_HASH}")

    frame = pd.read_parquet(model_input_path)
    frame["timestamp"] = pd.to_datetime(frame["timestamp"], utc=True)
    model_input_summary = read_json(model_input_summary_path)
    stage06_report = read_json(stage06_report_path)

    _io_path(run_output_root).mkdir(parents=True, exist_ok=True)
    model_path = run_output_root / "model.joblib"
    predictions_path = run_output_root / "predictions.parquet"
    metrics_path = run_output_root / "metrics.json"
    feature_importance_path = run_output_root / "feature_importance.csv"
    preprocessing_policy_path = run_output_root / "preprocessing_policy.md"
    preprocessing_policy_json_path = run_output_root / "preprocessing_policy.json"
    training_contract_path = run_output_root / "training_run_contract.json"
    model_schema_path = run_output_root / "model_input_schema.json"
    model_manifest_path = run_output_root / "model_artifact_manifest.json"
    summary_path = run_output_root / "summary.json"
    run_manifest_path = run_output_root / "run_manifest.json"
    kpi_record_path = run_output_root / "kpi_record.json"
    result_summary_path = run_output_root / "result_summary.md"

    config = BaselineTrainingConfig(random_seed=random_seed, max_iter=max_iter)
    model = train_baseline_model(frame, feature_order, config)
    metrics, predictions = evaluate_model(model, frame, feature_order)
    importance = coefficient_importance(model, feature_order)

    joblib.dump(model, _io_path(model_path))
    predictions.to_parquet(_io_path(predictions_path), index=False)
    importance.to_csv(_io_path(feature_importance_path), index=False)

    preprocessing_policy = {
        "policy_id": "stage07_preprocessing_policy_v1_train_only_standard_scaler",
        "scaler": config.scaler,
        "fit_scope": "train_split_only",
        "imputation": config.imputation,
        "feature_count": len(feature_order),
        "feature_order_hash": feature_hash,
        "label_order": [LABEL_NAMES[label] for label in LABEL_ORDER],
        "label_class_order": LABEL_ORDER,
        "leakage_boundary": "validation_and_oos_not_used_for_scaler_fit",
    }
    write_json(preprocessing_policy_json_path, preprocessing_policy)
    write_md(preprocessing_policy_path, preprocessing_policy_markdown(config, len(feature_order)))

    training_contract = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "training_contract_id": "stage07_training_run_contract_v1",
        "model_input_dataset_id": MODEL_INPUT_DATASET_ID,
        "feature_set_id": FEATURE_SET_ID,
        "model_artifact_id": MODEL_ARTIFACT_ID,
        "model_family": config.model_family,
        "preprocessing_policy_id": preprocessing_policy["policy_id"],
        "split_use": {
            "train": "fit_scaler_and_model",
            "validation": "smoke_metric_report_only",
            "oos": "smoke_metric_report_only",
        },
        "output_schema": {
            "type": "probs3",
            "order": ["p_short", "p_flat", "p_long"],
        },
        "contracts": [
            TRAINING_CONTRACT_VERSION,
            MODEL_INPUT_CONTRACT_VERSION,
            RUNTIME_PARITY_CONTRACT_VERSION,
        ],
        "boundary": "pipeline_smoke_not_alpha_quality_or_operating_promotion",
    }
    write_json(training_contract_path, training_contract)

    model_schema = {
        "model_input_dataset_id": MODEL_INPUT_DATASET_ID,
        "feature_count": len(feature_order),
        "feature_order": feature_order,
        "feature_order_hash": feature_hash,
        "label_class_order": LABEL_ORDER,
        "probability_output_order": ["p_short", "p_flat", "p_long"],
        "split_summary": split_summary(frame),
    }
    write_json(model_schema_path, model_schema)

    input_hashes = {
        "model_input_dataset_sha256": sha256_file(model_input_path),
        "model_input_summary_sha256": sha256_file(model_input_summary_path),
        "feature_order_sha256": sha256_file(feature_order_path),
        "stage06_runtime_parity_report_sha256": sha256_file(stage06_report_path),
    }

    model_manifest = {
        "artifact_id": MODEL_ARTIFACT_ID,
        "artifact_role": "baseline_training_smoke_model",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "model_path": model_path.as_posix(),
        "model_family": config.model_family,
        "model_format": "joblib_sklearn_pipeline",
        "feature_count": len(feature_order),
        "feature_order_hash": feature_hash,
        "preprocessing_policy_path": preprocessing_policy_json_path.as_posix(),
        "training_contract_path": training_contract_path.as_posix(),
        "model_input_schema_path": model_schema_path.as_posix(),
        "probability_output_order": ["p_short", "p_flat", "p_long"],
        "required_input_hashes": input_hashes,
        "boundary": "model artifact identity for training smoke only; not alpha quality or operating promotion",
    }
    write_json(model_manifest_path, model_manifest)

    output_hashes = {
        "model_joblib_sha256": sha256_file(model_path),
        "predictions_sha256": sha256_file(predictions_path),
        "metrics_sha256": None,
        "model_artifact_manifest_sha256": sha256_file(model_manifest_path),
        "training_run_contract_sha256": sha256_file(training_contract_path),
        "preprocessing_policy_json_sha256": sha256_file(preprocessing_policy_json_path),
    }

    probability_checks = metrics["probability_checks"]
    passed = bool(probability_checks["finite"] and probability_checks["row_sum_max_abs_error"] <= 1e-12)
    judgment = "positive_baseline_training_smoke_passed" if passed else "invalid_baseline_training_smoke_failed"

    summary = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "model_training_smoke",
        "status": "reviewed" if passed else "invalid",
        "judgment": judgment,
        "model_artifact_id": MODEL_ARTIFACT_ID,
        "model_family": config.model_family,
        "feature_count": len(feature_order),
        "feature_order_hash": feature_hash,
        "model_input_dataset_id": MODEL_INPUT_DATASET_ID,
        "feature_set_id": FEATURE_SET_ID,
        "stage06_runtime_state": stage06_report.get("runtime_state"),
        "stage06_external_verification_status": stage06_report.get("external_verification_status"),
        "model_input_rows": int(len(frame)),
        "model_input_summary_rows": int(model_input_summary.get("rows", -1)),
        "metrics": metrics,
        "input_hashes": input_hashes,
        "output_hashes": output_hashes,
        "external_verification_status": "not_applicable",
        "boundary": "Python-side baseline training smoke only; not alpha quality, live readiness, or operating promotion.",
    }
    write_json(metrics_path, metrics)
    output_hashes["metrics_sha256"] = sha256_file(metrics_path)
    summary["output_hashes"] = output_hashes
    write_json(summary_path, summary)
    write_md(result_summary_path, result_summary_markdown(summary))

    outputs = [
        model_path,
        predictions_path,
        metrics_path,
        feature_importance_path,
        preprocessing_policy_path,
        preprocessing_policy_json_path,
        training_contract_path,
        model_schema_path,
        model_manifest_path,
        summary_path,
        result_summary_path,
    ]
    run_manifest = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "model_training_smoke",
        "status": summary["status"],
        "command": "python foundation/pipelines/run_stage07_baseline_training_smoke.py",
        "inputs": [
            model_input_path.as_posix(),
            model_input_summary_path.as_posix(),
            feature_order_path.as_posix(),
            stage06_report_path.as_posix(),
        ],
        "outputs": [path.as_posix() for path in outputs],
        "judgment": judgment,
        "judgment_boundary": summary["boundary"],
        "external_verification_status": "not_applicable",
    }
    write_json(run_manifest_path, run_manifest)

    kpi_record = {
        "run_id": RUN_ID,
        "scoreboard": "structural_scout",
        "measurement_scope": "baseline_training_pipeline_smoke",
        "judgment": judgment,
        "external_verification_status": "not_applicable",
        "measurement": {
            "model_input_rows": int(len(frame)),
            "feature_count": len(feature_order),
            "feature_order_hash": feature_hash,
            "model_artifact_id": MODEL_ARTIFACT_ID,
            "metrics": metrics,
            "probability_output_order": ["p_short", "p_flat", "p_long"],
        },
        "boundary": summary["boundary"],
    }
    write_json(kpi_record_path, kpi_record)

    payload = {
        "status": "ok" if passed else "failed",
        "run_id": RUN_ID,
        "judgment": judgment,
        "run_output_root": run_output_root.as_posix(),
        "model_artifact_id": MODEL_ARTIFACT_ID,
        "model_path": model_path.as_posix(),
        "summary_path": summary_path.as_posix(),
        "result_summary_path": result_summary_path.as_posix(),
    }
    return payload


def main() -> int:
    args = parse_args()
    payload = run_stage07_baseline_training_smoke(
        model_input_path=Path(args.model_input_path),
        model_input_summary_path=Path(args.model_input_summary_path),
        feature_order_path=Path(args.feature_order_path),
        stage06_report_path=Path(args.stage06_report_path),
        run_output_root=Path(args.run_output_root),
        random_seed=args.random_seed,
        max_iter=args.max_iter,
    )
    print(json.dumps(payload, indent=2))
    return 0 if payload["status"] == "ok" else 1


if __name__ == "__main__":
    raise SystemExit(main())
