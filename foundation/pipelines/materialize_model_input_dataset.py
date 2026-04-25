from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd


REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.pipelines.materialize_fpmarkets_v2_dataset import (  # noqa: E402
    EXPECTED_FEATURE_ORDER_HASH,
    FEATURE_ORDER,
    feature_order_hash,
    sha256_file,
)


MATERIALIZER_VERSION = "fpmarkets_v2_stage04_model_input_feature_set_v1"
STAGE_ID = "04_model_input_readiness__weights_parity_feature_audit"
RUN_ID = "20260425_model_input_feature_set_v1_no_placeholder_top3_weights"
MODE_QUARANTINE_PLACEHOLDER = "quarantine_placeholder_top3_v1"
MODE_MT5_PRICE_PROXY_58 = "mt5_price_proxy_58_v1"
DEFAULT_SOURCE_TRAINING_DATASET_ID = (
    "training_fpmarkets_v2_us100_m5_label_v1_fwd12_m5_logret_train_q33_3class_split_v1"
)
DEFAULT_SOURCE_TRAINING_DATASET_ID_58 = "training_fpmarkets_v2_us100_m5_label_v1_fwd12_split_v1_proxyw58"
DEFAULT_MODEL_INPUT_DATASET_ID = (
    "model_input_fpmarkets_v2_us100_m5_label_v1_fwd12_split_v1_feature_set_v1_no_placeholder_top3_weights"
)
DEFAULT_MODEL_INPUT_DATASET_ID_58 = (
    "model_input_fpmarkets_v2_us100_m5_label_v1_fwd12_split_v1_proxyw58_feature_set_v2"
)
FEATURE_SET_ID = "feature_set_v1_no_placeholder_top3_weight_features"
FEATURE_SET_ID_58 = "feature_set_v2_mt5_price_proxy_top3_weights_58_features"
WEIGHT_PLACEHOLDER_STATUS = "placeholder_equal_weight"
WEIGHT_PRICE_PROXY_STATUS = "mt5_price_proxy_top3_weights_v1"
MODEL_INPUT_POLICY_ID = "model_input_v1_quarantine_placeholder_top3_weight_features"
MODEL_INPUT_POLICY_ID_58 = "model_input_v2_include_mt5_price_proxy_top3_weight_features"
DEFAULT_TRAINING_DATASET_PATH = Path("data/processed/training_datasets/label_v1_fwd12_split_v1/training_dataset.parquet")
DEFAULT_TRAINING_SUMMARY_PATH = Path(
    "data/processed/training_datasets/label_v1_fwd12_split_v1/training_dataset_summary.json"
)
DEFAULT_TRAINING_DATASET_PATH_58 = Path(
    "data/processed/training_datasets/label_v1_fwd12_split_v1_proxyw58/training_dataset.parquet"
)
DEFAULT_TRAINING_SUMMARY_PATH_58 = Path(
    "data/processed/training_datasets/label_v1_fwd12_split_v1_proxyw58/training_dataset_summary.json"
)
DEFAULT_OUTPUT_ROOT = Path("data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v1")
DEFAULT_RUN_OUTPUT_ROOT = Path("stages") / STAGE_ID / "02_runs" / "20260425_model_input_feature_set_v1"
DEFAULT_OUTPUT_ROOT_58 = Path("data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58")
DEFAULT_RUN_OUTPUT_ROOT_58 = Path("stages") / STAGE_ID / "02_runs" / "20260425_mi_v2_proxy58"
MODEL_INPUT_CONTRACT_VERSION = "docs/contracts/model_input_feature_set_contract_fpmarkets_v2.md@2026-04-25"
TRAINING_LABEL_SPLIT_CONTRACT_VERSION = "docs/contracts/training_label_split_contract_fpmarkets_v2.md@2026-04-25"

QUARANTINED_FEATURES = (
    "top3_weighted_return_1",
    "us100_minus_top3_weighted_return_1",
)
LABEL_AND_SPLIT_COLUMNS = [
    "future_timestamp",
    "future_log_return_12",
    "label",
    "label_class",
    "label_id",
    "split",
    "split_id",
    "horizon_bars",
    "horizon_minutes",
]
IDENTITY_COLUMNS = ["timestamp", "symbol"]
MODEL_INPUT_FEATURE_ORDER = [name for name in FEATURE_ORDER if name not in set(QUARANTINED_FEATURES)]


@dataclass(frozen=True)
class ModelInputModeConfig:
    mode: str
    run_id: str
    materializer_version: str
    feature_set_id: str
    model_input_policy_id: str
    weight_source_status: str
    feature_order: list[str]
    quarantined_features: tuple[str, ...]
    judgment: str
    result_title: str
    result_intro: str
    boundary: str
    quarantine_reason: str
    first_baseline_policy: str
    reopen_condition: str


def model_input_mode_config(mode: str) -> ModelInputModeConfig:
    if mode == MODE_QUARANTINE_PLACEHOLDER:
        return ModelInputModeConfig(
            mode=mode,
            run_id=RUN_ID,
            materializer_version=MATERIALIZER_VERSION,
            feature_set_id=FEATURE_SET_ID,
            model_input_policy_id=MODEL_INPUT_POLICY_ID,
            weight_source_status=WEIGHT_PLACEHOLDER_STATUS,
            feature_order=MODEL_INPUT_FEATURE_ORDER,
            quarantined_features=QUARANTINED_FEATURES,
            judgment="positive_quarantine_materialized",
            result_title="Stage 04 Model-Input Feature Set v1",
            result_intro=(
                "이 실행(run, 실행)은 placeholder top3 weight features(임시 top3 가중치 피처)를 제외한 "
                "첫 model-input dataset(모델 입력 데이터셋)을 물질화했다."
            ),
            boundary=(
                "Evidence run(근거 실행) only(한정). placeholder top3 weight features(임시 top3 가중치 피처)를 "
                "격리한 첫 model-input dataset(모델 입력 데이터셋)을 물질화하지만, model training(모델 학습), "
                "alpha quality(알파 품질), runtime authority(런타임 권위), operating promotion(운영 승격)을 주장하지 않는다."
            ),
            quarantine_reason=(
                "top3 basket weight source is marked placeholder_equal_weight; first model input excludes "
                "the dependent features until real or proxy monthly weights or an explicit experimental opt-in exists."
            ),
            first_baseline_policy="exclude_from_model_input",
            reopen_condition="real or proxy monthly top3 weights or explicit experimental opt-in decision",
        )
    if mode == MODE_MT5_PRICE_PROXY_58:
        return ModelInputModeConfig(
            mode=mode,
            run_id="20260425_model_input_feature_set_v2_mt5_price_proxy_58",
            materializer_version="fpmarkets_v2_stage04_model_input_feature_set_v2_mt5_price_proxy_58",
            feature_set_id=FEATURE_SET_ID_58,
            model_input_policy_id=MODEL_INPUT_POLICY_ID_58,
            weight_source_status=WEIGHT_PRICE_PROXY_STATUS,
            feature_order=list(FEATURE_ORDER),
            quarantined_features=(),
            judgment="positive_58_feature_price_proxy_model_input_materialized",
            result_title="Stage 04 Model-Input Feature Set v2 MT5 Price-Proxy 58",
            result_intro=(
                "이 실행(run, 실행)은 MT5 price-proxy monthly weights(MT5 가격 대리 월별 가중치)로 "
                "top3 weight features(top3 가중치 피처)를 복구한 58-feature model-input dataset(58개 피처 모델 입력 데이터셋)을 물질화했다."
            ),
            boundary=(
                "Evidence run(근거 실행) only(한정). MT5 price-proxy top3 weights(MT5 가격 대리 top3 가중치)를 "
                "쓴 58-feature model-input dataset(58개 피처 모델 입력 데이터셋)을 물질화하지만, actual NDX/QQQ weights"
                "(실제 NDX/QQQ 가중치), model training(모델 학습), alpha quality(알파 품질), runtime authority(런타임 권위), "
                "operating promotion(운영 승격)을 주장하지 않는다."
            ),
            quarantine_reason=(
                "No features are quarantined in this mode. top3 weight features are included with "
                "MT5 price-proxy monthly weights, not actual NDX/QQQ weights."
            ),
            first_baseline_policy="include_all_58_features_with_mt5_price_proxy_weights",
            reopen_condition="actual NDX/QQQ top3 weights can supersede this proxy through a later contract decision",
        )
    raise ValueError(f"Unsupported model input mode: {mode}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Materialize a Stage 04 model-input dataset.")
    parser.add_argument(
        "--mode",
        choices=(MODE_QUARANTINE_PLACEHOLDER, MODE_MT5_PRICE_PROXY_58),
        default=MODE_QUARANTINE_PLACEHOLDER,
    )
    parser.add_argument("--source-training-dataset-id", default=None)
    parser.add_argument("--model-input-dataset-id", default=None)
    parser.add_argument("--training-dataset-path", default=None)
    parser.add_argument("--training-summary-path", default=None)
    parser.add_argument("--output-root", default=None)
    parser.add_argument("--run-output-root", default=None)
    return parser.parse_args()


def ordered_hash(names: list[str] | tuple[str, ...]) -> str:
    import hashlib

    payload = "\n".join(names).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _json_ready(value: Any) -> Any:
    if isinstance(value, pd.Timestamp):
        return value.tz_convert("UTC").isoformat() if value.tzinfo else value.isoformat()
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
    return value


def load_training_dataset(training_dataset_path: Path) -> pd.DataFrame:
    if not training_dataset_path.exists():
        raise RuntimeError(f"Training dataset does not exist: {training_dataset_path}")
    frame = pd.read_parquet(training_dataset_path)
    required_columns = set(IDENTITY_COLUMNS + FEATURE_ORDER + LABEL_AND_SPLIT_COLUMNS)
    missing = required_columns.difference(frame.columns)
    if missing:
        raise RuntimeError(f"Training dataset is missing columns: {sorted(missing)}")
    frame["timestamp"] = pd.to_datetime(frame["timestamp"], utc=True)
    frame["future_timestamp"] = pd.to_datetime(frame["future_timestamp"], utc=True)
    if frame["timestamp"].duplicated().any():
        raise RuntimeError("Training dataset contains duplicate timestamps.")
    if not frame["timestamp"].is_monotonic_increasing:
        raise RuntimeError("Training dataset timestamps are not monotonic increasing.")
    return frame


def _class_distribution(frame: pd.DataFrame) -> dict[str, int]:
    counts = frame["label"].value_counts().to_dict()
    return {label: int(counts.get(label, 0)) for label in ("short", "flat", "long")}


def _split_summary(frame: pd.DataFrame) -> dict[str, dict[str, object]]:
    payload: dict[str, dict[str, object]] = {}
    for split_name in ("train", "validation", "oos"):
        split_frame = frame.loc[frame["split"].eq(split_name)]
        payload[split_name] = {
            "rows": int(len(split_frame)),
            "first_timestamp": split_frame["timestamp"].min() if len(split_frame) else None,
            "last_timestamp": split_frame["timestamp"].max() if len(split_frame) else None,
            "class_distribution": _class_distribution(split_frame)
            if len(split_frame)
            else {"short": 0, "flat": 0, "long": 0},
        }
    return payload


def _validate_feature_values(frame: pd.DataFrame, feature_order: list[str]) -> None:
    feature_values = frame.loc[:, feature_order].to_numpy(dtype="float64", copy=False)
    if not np.isfinite(feature_values).all():
        raise RuntimeError("Model-input feature set contains NaN or infinite values.")


def build_model_input_dataset(
    training_frame: pd.DataFrame,
    mode: str = MODE_QUARANTINE_PLACEHOLDER,
) -> tuple[pd.DataFrame, dict[str, object]]:
    config = model_input_mode_config(mode)
    current_feature_hash = feature_order_hash()
    if current_feature_hash != EXPECTED_FEATURE_ORDER_HASH:
        raise RuntimeError(
            f"Feature order hash mismatch: {current_feature_hash} != {EXPECTED_FEATURE_ORDER_HASH}"
        )

    missing_features = [name for name in config.feature_order if name not in training_frame.columns]
    if missing_features:
        raise RuntimeError(f"Training dataset is missing model-input features: {missing_features}")

    missing_quarantined = [name for name in config.quarantined_features if name not in training_frame.columns]
    if missing_quarantined:
        raise RuntimeError(f"Cannot quarantine missing features: {missing_quarantined}")

    export_columns = IDENTITY_COLUMNS + config.feature_order + LABEL_AND_SPLIT_COLUMNS
    model_input = training_frame.loc[:, export_columns].copy()
    _validate_feature_values(model_input, config.feature_order)

    for feature_name in config.quarantined_features:
        if feature_name in model_input.columns:
            raise RuntimeError(f"Quarantined feature leaked into model input: {feature_name}")

    summary = {
        "mode": config.mode,
        "run_id": config.run_id,
        "feature_set_id": config.feature_set_id,
        "model_input_policy_id": config.model_input_policy_id,
        "source_feature_order_hash": current_feature_hash,
        "included_feature_order_hash": ordered_hash(config.feature_order),
        "source_feature_count": len(FEATURE_ORDER),
        "included_feature_count": len(config.feature_order),
        "quarantined_feature_count": len(config.quarantined_features),
        "quarantined_features": list(config.quarantined_features),
        "restored_features": [name for name in QUARANTINED_FEATURES if name in config.feature_order],
        "quarantine_reason": config.quarantine_reason,
        "weight_source_status": config.weight_source_status,
        "rows": int(len(model_input)),
        "split_summary": _split_summary(model_input),
        "all_class_distribution": _class_distribution(model_input),
    }
    return model_input, summary


def write_model_input_outputs(
    *,
    output_root: Path,
    run_output_root: Path,
    source_training_dataset_id: str,
    model_input_dataset_id: str,
    training_dataset_path: Path,
    training_summary_path: Path,
    model_input_frame: pd.DataFrame,
    summary: dict[str, object],
) -> dict[str, object]:
    config = model_input_mode_config(str(summary["mode"]))
    output_root.mkdir(parents=True, exist_ok=True)
    run_output_root.mkdir(parents=True, exist_ok=True)

    model_input_path = output_root / "model_input_dataset.parquet"
    summary_path = output_root / "model_input_summary.json"
    feature_set_manifest_path = output_root / "feature_set_manifest.json"
    quarantine_manifest_path = output_root / "quarantine_manifest.json"
    feature_order_path = output_root / "model_input_feature_order.txt"
    debug_rows_path = output_root / "sample_debug_rows.csv"

    model_input_frame.to_parquet(model_input_path, index=False)
    feature_order_path.write_text("\n".join(config.feature_order), encoding="utf-8")

    manifest_payload = {
        "model_input_dataset_id": model_input_dataset_id,
        "source_training_dataset_id": source_training_dataset_id,
        "materializer_version": config.materializer_version,
        "model_input_contract_version": MODEL_INPUT_CONTRACT_VERSION,
        "training_label_split_contract_version": TRAINING_LABEL_SPLIT_CONTRACT_VERSION,
        "source_training_dataset_path": str(training_dataset_path.as_posix()),
        "source_training_summary_path": str(training_summary_path.as_posix()),
        **summary,
    }
    summary_path.write_text(json.dumps(_json_ready(manifest_payload), indent=2), encoding="utf-8")

    feature_set_manifest = {
        "feature_set_id": summary["feature_set_id"],
        "model_input_dataset_id": model_input_dataset_id,
        "source_training_dataset_id": source_training_dataset_id,
        "included_feature_order": config.feature_order,
        "included_feature_order_hash": summary["included_feature_order_hash"],
        "source_feature_order_hash": summary["source_feature_order_hash"],
        "source_feature_count": summary["source_feature_count"],
        "included_feature_count": summary["included_feature_count"],
    }
    feature_set_manifest_path.write_text(json.dumps(feature_set_manifest, indent=2), encoding="utf-8")

    quarantine_manifest = {
        "model_input_policy_id": config.model_input_policy_id,
        "weight_source_status": config.weight_source_status,
        "quarantined_features": list(config.quarantined_features),
        "restored_features": summary["restored_features"],
        "quarantine_reason": summary["quarantine_reason"],
        "first_baseline_policy": config.first_baseline_policy,
        "reopen_condition": config.reopen_condition,
    }
    quarantine_manifest_path.write_text(json.dumps(quarantine_manifest, indent=2), encoding="utf-8")

    debug_columns = ["timestamp", "label", "label_class", "split", *config.feature_order[:8]]
    model_input_frame.loc[:, debug_columns].head(200).to_csv(debug_rows_path, index=False)

    model_input_hash = sha256_file(model_input_path)
    summary_hash = sha256_file(summary_path)
    feature_set_manifest_hash = sha256_file(feature_set_manifest_path)
    quarantine_manifest_hash = sha256_file(quarantine_manifest_path)

    run_manifest = {
        "run_id": config.run_id,
        "stage_id": STAGE_ID,
        "lane": "evidence",
        "status": "reviewed",
        "command": f"python foundation/pipelines/materialize_model_input_dataset.py --mode {config.mode}",
        "inputs": [
            str(training_dataset_path.as_posix()),
            str(training_summary_path.as_posix()),
            MODEL_INPUT_CONTRACT_VERSION.split("@")[0],
        ],
        "outputs": [
            str(model_input_path.as_posix()),
            str(summary_path.as_posix()),
            str(feature_set_manifest_path.as_posix()),
            str(quarantine_manifest_path.as_posix()),
        ],
        "judgment_boundary": config.boundary,
        "external_verification_status": "not_applicable",
    }
    (run_output_root / "run_manifest.json").write_text(json.dumps(run_manifest, indent=2), encoding="utf-8")

    kpi_record = {
        "run_id": config.run_id,
        "scoreboard": "structural_scout",
        "measurement": {
            "rows": summary["rows"],
            "source_feature_count": summary["source_feature_count"],
            "included_feature_count": summary["included_feature_count"],
            "quarantined_feature_count": summary["quarantined_feature_count"],
            "included_feature_order_hash": summary["included_feature_order_hash"],
            "split_summary": summary["split_summary"],
        },
        "judgment": config.judgment,
        "external_verification_status": "not_applicable",
    }
    (run_output_root / "kpi_record.json").write_text(json.dumps(_json_ready(kpi_record), indent=2), encoding="utf-8")

    run_summary = {
        "run_id": config.run_id,
        "model_input_dataset_id": model_input_dataset_id,
        "source_training_dataset_id": source_training_dataset_id,
        "rows": summary["rows"],
        "source_feature_count": summary["source_feature_count"],
        "included_feature_count": summary["included_feature_count"],
        "quarantined_features": list(config.quarantined_features),
        "restored_features": summary["restored_features"],
        "weight_source_status": config.weight_source_status,
        "result_title": config.result_title,
        "result_intro": config.result_intro,
        "boundary": config.boundary,
        "split_summary": summary["split_summary"],
        "hashes": {
            "model_input_dataset_sha256": model_input_hash,
            "model_input_summary_sha256": summary_hash,
            "feature_set_manifest_sha256": feature_set_manifest_hash,
            "quarantine_manifest_sha256": quarantine_manifest_hash,
        },
    }
    (run_output_root / "summary.json").write_text(json.dumps(_json_ready(run_summary), indent=2), encoding="utf-8")
    (run_output_root / "result_summary.md").write_text(render_result_summary(run_summary), encoding="utf-8-sig")

    return {
        "model_input_dataset_id": model_input_dataset_id,
        "output_root": str(output_root.as_posix()),
        "run_output_root": str(run_output_root.as_posix()),
        "model_input_dataset_path": str(model_input_path.as_posix()),
        "model_input_summary_path": str(summary_path.as_posix()),
        "feature_set_manifest_path": str(feature_set_manifest_path.as_posix()),
        "quarantine_manifest_path": str(quarantine_manifest_path.as_posix()),
        "hashes": run_summary["hashes"],
    }


def render_result_summary(run_summary: dict[str, object]) -> str:
    quarantined = ", ".join(run_summary["quarantined_features"]) if run_summary["quarantined_features"] else "none"
    restored = ", ".join(run_summary["restored_features"]) if run_summary["restored_features"] else "none"
    lines = [
        f"# {run_summary['result_title']}",
        "",
        str(run_summary["result_intro"]),
        "",
        "## Key Numbers",
        "",
        f"- model_input_dataset_id: `{run_summary['model_input_dataset_id']}`",
        f"- source_training_dataset_id: `{run_summary['source_training_dataset_id']}`",
        f"- rows(행 수): `{run_summary['rows']}`",
        f"- source_feature_count(원천 피처 수): `{run_summary['source_feature_count']}`",
        f"- included_feature_count(포함 피처 수): `{run_summary['included_feature_count']}`",
        f"- weight_source_status(가중치 원천 상태): `{run_summary['weight_source_status']}`",
        f"- quarantined_features(격리 피처): `{quarantined}`",
        f"- restored_features(복구 피처): `{restored}`",
        "",
        "## Boundary",
        "",
        str(run_summary["boundary"]),
    ]
    return "\n".join(lines) + "\n"


def materialize_model_input_dataset(
    *,
    source_training_dataset_id: str,
    model_input_dataset_id: str,
    training_dataset_path: Path,
    training_summary_path: Path,
    output_root: Path,
    run_output_root: Path,
    mode: str = MODE_QUARANTINE_PLACEHOLDER,
) -> dict[str, object]:
    training_frame = load_training_dataset(training_dataset_path)
    model_input_frame, summary = build_model_input_dataset(training_frame, mode=mode)
    return write_model_input_outputs(
        output_root=output_root,
        run_output_root=run_output_root,
        source_training_dataset_id=source_training_dataset_id,
        model_input_dataset_id=model_input_dataset_id,
        training_dataset_path=training_dataset_path,
        training_summary_path=training_summary_path,
        model_input_frame=model_input_frame,
        summary=summary,
    )


def main() -> None:
    args = parse_args()
    default_model_input_dataset_id = (
        DEFAULT_MODEL_INPUT_DATASET_ID_58 if args.mode == MODE_MT5_PRICE_PROXY_58 else DEFAULT_MODEL_INPUT_DATASET_ID
    )
    default_source_training_dataset_id = (
        DEFAULT_SOURCE_TRAINING_DATASET_ID_58
        if args.mode == MODE_MT5_PRICE_PROXY_58
        else DEFAULT_SOURCE_TRAINING_DATASET_ID
    )
    default_training_dataset_path = (
        DEFAULT_TRAINING_DATASET_PATH_58 if args.mode == MODE_MT5_PRICE_PROXY_58 else DEFAULT_TRAINING_DATASET_PATH
    )
    default_training_summary_path = (
        DEFAULT_TRAINING_SUMMARY_PATH_58 if args.mode == MODE_MT5_PRICE_PROXY_58 else DEFAULT_TRAINING_SUMMARY_PATH
    )
    default_output_root = DEFAULT_OUTPUT_ROOT_58 if args.mode == MODE_MT5_PRICE_PROXY_58 else DEFAULT_OUTPUT_ROOT
    default_run_output_root = DEFAULT_RUN_OUTPUT_ROOT_58 if args.mode == MODE_MT5_PRICE_PROXY_58 else DEFAULT_RUN_OUTPUT_ROOT
    payload = materialize_model_input_dataset(
        source_training_dataset_id=args.source_training_dataset_id or default_source_training_dataset_id,
        model_input_dataset_id=args.model_input_dataset_id or default_model_input_dataset_id,
        training_dataset_path=Path(args.training_dataset_path) if args.training_dataset_path else default_training_dataset_path,
        training_summary_path=Path(args.training_summary_path) if args.training_summary_path else default_training_summary_path,
        output_root=Path(args.output_root) if args.output_root else default_output_root,
        run_output_root=Path(args.run_output_root) if args.run_output_root else default_run_output_root,
        mode=args.mode,
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
