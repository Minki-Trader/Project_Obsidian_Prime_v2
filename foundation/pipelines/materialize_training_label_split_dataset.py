from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
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


MATERIALIZER_VERSION = "fpmarkets_v2_stage03_training_label_split_v1"
DEFAULT_SOURCE_DATASET_ID = "dataset_fpmarkets_v2_us100_m5_20220901_20260413_cashopen_fullcash_valid_freeze01"
DEFAULT_TRAINING_DATASET_ID = (
    "training_fpmarkets_v2_us100_m5_label_v1_fwd12_m5_logret_train_q33_3class_split_v1"
)
DEFAULT_FEATURES_PATH = Path("data/processed/datasets") / DEFAULT_SOURCE_DATASET_ID / "features.parquet"
DEFAULT_SOURCE_SUMMARY_PATH = Path("data/processed/datasets") / DEFAULT_SOURCE_DATASET_ID / "dataset_summary.json"
DEFAULT_RAW_ROOT = Path("data/raw/mt5_bars/m5")
DEFAULT_OUTPUT_ROOT = Path("data/processed/training_datasets/label_v1_fwd12_split_v1")
DEFAULT_RUN_OUTPUT_ROOT = (
    Path("stages/03_training_dataset__label_split_contract/02_runs")
    / "20260425_label_v1"
)
LABEL_CONTRACT_VERSION = "docs/contracts/training_label_split_contract_fpmarkets_v2.md@2026-04-25"
TRAINING_FEATURE_CONTRACT_VERSION = "docs/contracts/feature_calculation_spec_fpmarkets_v2.md@2026-04-24"
TRAINING_PARSER_CONTRACT_VERSION = "docs/contracts/python_feature_parser_spec_fpmarkets_v2.md@2026-04-24"
TIME_AXIS_POLICY_VERSION = "docs/contracts/time_axis_policy_fpmarkets_v2.md@2026-04-24"
LABEL_ID = "label_v1_fwd12_m5_logret_train_q33_3class"
SPLIT_ID = "split_v1_calendar_train_20220901_20241231_val_20250101_20250930_oos_20251001_20260413"
RUN_ID = "20260425_label_v1_fwd12_split_v1_materialization"
STAGE_ID = "03_training_dataset__label_split_contract"
US100_SYMBOL = "US100"


@dataclass(frozen=True)
class TrainingLabelSplitSpec:
    label_id: str = LABEL_ID
    split_id: str = SPLIT_ID
    horizon_bars: int = 12
    bar_minutes: int = 5
    threshold_source_split: str = "train"
    threshold_abs_quantile: float = 0.33
    train_start_utc: pd.Timestamp = pd.Timestamp("2022-09-01T00:00:00Z")
    validation_start_utc: pd.Timestamp = pd.Timestamp("2025-01-01T00:00:00Z")
    oos_start_utc: pd.Timestamp = pd.Timestamp("2025-10-01T00:00:00Z")
    window_end_inclusive_utc: pd.Timestamp = pd.Timestamp("2026-04-13T23:55:00Z")
    max_cash_session_minutes: int = 390

    @property
    def horizon_minutes(self) -> int:
        return self.horizon_bars * self.bar_minutes

    @property
    def max_label_start_minutes_from_cash_open(self) -> int:
        return self.max_cash_session_minutes - self.horizon_minutes


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Materialize the Stage 03 training label/split dataset.")
    parser.add_argument("--source-dataset-id", default=DEFAULT_SOURCE_DATASET_ID)
    parser.add_argument("--training-dataset-id", default=DEFAULT_TRAINING_DATASET_ID)
    parser.add_argument("--features-path", default=str(DEFAULT_FEATURES_PATH))
    parser.add_argument("--source-summary-path", default=str(DEFAULT_SOURCE_SUMMARY_PATH))
    parser.add_argument("--raw-root", default=str(DEFAULT_RAW_ROOT))
    parser.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    parser.add_argument("--run-output-root", default=str(DEFAULT_RUN_OUTPUT_ROOT))
    parser.add_argument("--run-id", default=RUN_ID)
    parser.add_argument("--stage-id", default=STAGE_ID)
    return parser.parse_args()


def _iso_timestamp(value: pd.Timestamp) -> str:
    return pd.Timestamp(value).tz_convert("UTC").isoformat()


def _json_ready(value: Any) -> Any:
    if isinstance(value, pd.Timestamp):
        return _iso_timestamp(value)
    if isinstance(value, dict):
        return {key: _json_ready(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_json_ready(item) for item in value]
    return value


def load_feature_dataset(features_path: Path) -> pd.DataFrame:
    frame = pd.read_parquet(features_path)
    required_columns = {"timestamp", "symbol", *FEATURE_ORDER}
    missing = required_columns.difference(frame.columns)
    if missing:
        raise RuntimeError(f"Feature dataset is missing columns: {sorted(missing)}")
    frame["timestamp"] = pd.to_datetime(frame["timestamp"], utc=True)
    if frame["timestamp"].duplicated().any():
        raise RuntimeError("Feature dataset contains duplicate timestamps.")
    if not frame["timestamp"].is_monotonic_increasing:
        raise RuntimeError("Feature dataset timestamps are not monotonic increasing.")
    return frame


def find_us100_raw_csv(raw_root: Path) -> Path:
    symbol_dir = raw_root / US100_SYMBOL
    candidates = sorted(symbol_dir.glob("*.csv"))
    if len(candidates) != 1:
        raise RuntimeError(f"Expected exactly one US100 raw CSV under {symbol_dir}, found {len(candidates)}")
    return candidates[0]


def load_us100_close_series(raw_root: Path) -> pd.DataFrame:
    raw_csv = find_us100_raw_csv(raw_root)
    raw = pd.read_csv(raw_csv, usecols=["time_close_unix", "close"])
    raw["timestamp"] = pd.to_datetime(raw["time_close_unix"], unit="s", utc=True)
    raw = raw[["timestamp", "close"]].drop_duplicates("timestamp").sort_values("timestamp")
    if raw["timestamp"].duplicated().any():
        raise RuntimeError("US100 raw close source contains duplicate timestamps.")
    if not raw["timestamp"].is_monotonic_increasing:
        raise RuntimeError("US100 raw close source timestamps are not monotonic increasing.")
    return raw


def build_label_candidates(
    feature_frame: pd.DataFrame,
    raw_close_frame: pd.DataFrame,
    spec: TrainingLabelSplitSpec,
) -> pd.DataFrame:
    if "minutes_from_cash_open" not in feature_frame.columns:
        raise RuntimeError("Feature dataset is missing minutes_from_cash_open.")

    raw_close = raw_close_frame.rename(columns={"close": "current_close"}).set_index("timestamp")
    future_close = raw_close.rename(columns={"current_close": "future_close"})

    working = feature_frame.copy()
    working["future_timestamp"] = working["timestamp"] + pd.Timedelta(minutes=spec.horizon_minutes)
    working = working.merge(raw_close, left_on="timestamp", right_index=True, how="left")
    working = working.merge(future_close, left_on="future_timestamp", right_index=True, how="left")
    working["future_log_return_12"] = np.log(working["future_close"] / working["current_close"])

    labelable_mask = working["minutes_from_cash_open"].le(spec.max_label_start_minutes_from_cash_open)
    labelable_mask &= working["current_close"].notna()
    labelable_mask &= working["future_close"].notna()
    labelable = working.loc[labelable_mask].copy()
    labelable = labelable.sort_values("timestamp").reset_index(drop=True)
    if labelable.empty:
        raise RuntimeError("No labelable rows found for the selected label contract.")
    return labelable


def assign_split(frame: pd.DataFrame, spec: TrainingLabelSplitSpec) -> pd.Series:
    split = pd.Series("oos", index=frame.index, dtype="object")
    split.loc[frame["timestamp"] < spec.validation_start_utc] = "train"
    split.loc[
        (frame["timestamp"] >= spec.validation_start_utc) & (frame["timestamp"] < spec.oos_start_utc)
    ] = "validation"
    return split


def compute_train_threshold(labelable: pd.DataFrame, spec: TrainingLabelSplitSpec) -> float:
    train_mask = labelable["timestamp"] < spec.validation_start_utc
    train_returns = labelable.loc[train_mask, "future_log_return_12"].astype("float64")
    if train_returns.empty:
        raise RuntimeError("Training split is empty; cannot derive label threshold.")
    threshold = float(train_returns.abs().quantile(spec.threshold_abs_quantile))
    if not np.isfinite(threshold) or threshold <= 0:
        raise RuntimeError(f"Invalid label threshold: {threshold}")
    return threshold


def assign_label_classes(frame: pd.DataFrame, threshold: float) -> pd.DataFrame:
    labeled = frame.copy()
    returns = labeled["future_log_return_12"].astype("float64")
    labeled["label"] = "flat"
    labeled.loc[returns > threshold, "label"] = "long"
    labeled.loc[returns < -threshold, "label"] = "short"
    labeled["label_class"] = labeled["label"].map({"short": 0, "flat": 1, "long": 2}).astype("int8")
    return labeled


def _class_distribution(frame: pd.DataFrame) -> dict[str, int]:
    counts = frame["label"].value_counts().to_dict()
    return {label: int(counts.get(label, 0)) for label in ("short", "flat", "long")}


def _split_summary(frame: pd.DataFrame) -> dict[str, dict[str, object]]:
    payload: dict[str, dict[str, object]] = {}
    for split_name in ("train", "validation", "oos"):
        split_frame = frame.loc[frame["split"].eq(split_name)]
        payload[split_name] = {
            "rows": int(len(split_frame)),
            "first_timestamp": _iso_timestamp(split_frame["timestamp"].min()) if len(split_frame) else None,
            "last_timestamp": _iso_timestamp(split_frame["timestamp"].max()) if len(split_frame) else None,
            "class_distribution": _class_distribution(split_frame) if len(split_frame) else {"short": 0, "flat": 0, "long": 0},
        }
    return payload


def build_training_dataset(
    feature_frame: pd.DataFrame,
    raw_close_frame: pd.DataFrame,
    spec: TrainingLabelSplitSpec,
) -> tuple[pd.DataFrame, dict[str, object]]:
    labelable = build_label_candidates(feature_frame, raw_close_frame, spec)
    threshold = compute_train_threshold(labelable, spec)
    labeled = assign_label_classes(labelable, threshold)
    labeled["split"] = assign_split(labeled, spec)
    labeled["label_id"] = spec.label_id
    labeled["split_id"] = spec.split_id
    labeled["horizon_bars"] = spec.horizon_bars
    labeled["horizon_minutes"] = spec.horizon_minutes

    export_columns = [
        "timestamp",
        "symbol",
        *FEATURE_ORDER,
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
    export = labeled.loc[:, export_columns].copy()
    export[FEATURE_ORDER] = export[FEATURE_ORDER].astype("float32")
    export["future_log_return_12"] = export["future_log_return_12"].astype("float32")
    export["horizon_bars"] = export["horizon_bars"].astype("int16")
    export["horizon_minutes"] = export["horizon_minutes"].astype("int16")

    summary = {
        "label_id": spec.label_id,
        "split_id": spec.split_id,
        "horizon_bars": spec.horizon_bars,
        "horizon_minutes": spec.horizon_minutes,
        "threshold_source_split": spec.threshold_source_split,
        "threshold_abs_quantile": spec.threshold_abs_quantile,
        "threshold_log_return": threshold,
        "max_label_start_minutes_from_cash_open": spec.max_label_start_minutes_from_cash_open,
        "class_id_map": {"short": 0, "flat": 1, "long": 2},
        "split_boundaries": {
            "train_start_utc": spec.train_start_utc,
            "validation_start_utc": spec.validation_start_utc,
            "oos_start_utc": spec.oos_start_utc,
            "window_end_inclusive_utc": spec.window_end_inclusive_utc,
        },
        "rows": int(len(export)),
        "source_feature_rows": int(len(feature_frame)),
        "excluded_for_missing_or_out_of_session_future": int(len(feature_frame) - len(export)),
        "split_summary": _split_summary(labeled),
        "all_class_distribution": _class_distribution(labeled),
    }
    return export, summary


def write_training_outputs(
    *,
    output_root: Path,
    run_output_root: Path,
    training_dataset_id: str,
    source_dataset_id: str,
    source_summary_path: Path,
    features_path: Path,
    raw_root: Path,
    training_frame: pd.DataFrame,
    summary: dict[str, object],
    run_id: str = RUN_ID,
    stage_id: str = STAGE_ID,
) -> dict[str, object]:
    output_root.mkdir(parents=True, exist_ok=True)
    run_output_root.mkdir(parents=True, exist_ok=True)

    current_feature_hash = feature_order_hash()
    if current_feature_hash != EXPECTED_FEATURE_ORDER_HASH:
        raise RuntimeError(
            f"Feature order hash mismatch: {current_feature_hash} != {EXPECTED_FEATURE_ORDER_HASH}"
        )

    training_path = output_root / "training_dataset.parquet"
    summary_path = output_root / "training_dataset_summary.json"
    label_contract_path = output_root / "label_contract.json"
    split_manifest_path = output_root / "split_manifest.json"
    feature_order_path = output_root / "feature_order.txt"
    debug_rows_path = output_root / "sample_debug_rows.csv"

    training_frame.to_parquet(training_path, index=False)
    feature_order_path.write_text("\n".join(FEATURE_ORDER), encoding="utf-8")

    contract_payload = {
        "training_dataset_id": training_dataset_id,
        "source_dataset_id": source_dataset_id,
        "materializer_version": MATERIALIZER_VERSION,
        "label_contract_version": LABEL_CONTRACT_VERSION,
        "feature_contract_version": TRAINING_FEATURE_CONTRACT_VERSION,
        "parser_contract_version": TRAINING_PARSER_CONTRACT_VERSION,
        "time_axis_policy_version": TIME_AXIS_POLICY_VERSION,
        "feature_order_hash": current_feature_hash,
        **summary,
    }
    summary_path.write_text(json.dumps(_json_ready(contract_payload), indent=2), encoding="utf-8")

    label_contract_payload = {
        key: contract_payload[key]
        for key in (
            "training_dataset_id",
            "source_dataset_id",
            "label_contract_version",
            "label_id",
            "horizon_bars",
            "horizon_minutes",
            "threshold_source_split",
            "threshold_abs_quantile",
            "threshold_log_return",
            "class_id_map",
            "max_label_start_minutes_from_cash_open",
        )
    }
    label_contract_path.write_text(json.dumps(_json_ready(label_contract_payload), indent=2), encoding="utf-8")

    split_manifest_payload = {
        "training_dataset_id": training_dataset_id,
        "split_id": summary["split_id"],
        "split_boundaries": summary["split_boundaries"],
        "split_summary": summary["split_summary"],
    }
    split_manifest_path.write_text(json.dumps(_json_ready(split_manifest_payload), indent=2), encoding="utf-8")

    debug_columns = [
        "timestamp",
        "future_timestamp",
        "future_log_return_12",
        "label",
        "label_class",
        "split",
        "minutes_from_cash_open",
    ]
    training_frame.loc[:, debug_columns].head(200).to_csv(debug_rows_path, index=False)

    training_hash = sha256_file(training_path)
    summary_hash = sha256_file(summary_path)
    label_contract_hash = sha256_file(label_contract_path)
    split_manifest_hash = sha256_file(split_manifest_path)

    raw_csv = find_us100_raw_csv(raw_root)
    run_manifest = {
        "run_id": run_id,
        "stage_id": stage_id,
        "lane": "evidence",
        "status": "reviewed",
        "command": (
            "python foundation/pipelines/materialize_training_label_split_dataset.py "
            f"--source-dataset-id {source_dataset_id} --training-dataset-id {training_dataset_id}"
        ),
        "inputs": [
            str(features_path.as_posix()),
            str(source_summary_path.as_posix()),
            str(raw_csv.as_posix()),
            LABEL_CONTRACT_VERSION.split("@")[0],
        ],
        "outputs": [
            str(training_path.as_posix()),
            str(summary_path.as_posix()),
            str(label_contract_path.as_posix()),
            str(split_manifest_path.as_posix()),
        ],
        "judgment_boundary": (
            "Evidence run only. This fixes and materializes the first default training label and split; "
            "it does not train a model, prove alpha quality, close runtime authority, or claim operating promotion."
        ),
        "external_verification_status": "not_applicable",
    }
    (run_output_root / "run_manifest.json").write_text(json.dumps(run_manifest, indent=2), encoding="utf-8")

    kpi_record = {
        "run_id": run_id,
        "scoreboard": "structural_scout",
        "measurement": {
            "training_rows": summary["rows"],
            "split_summary": summary["split_summary"],
            "threshold_log_return": summary["threshold_log_return"],
            "feature_order_hash": current_feature_hash,
        },
        "judgment": "positive",
        "external_verification_status": "not_applicable",
    }
    (run_output_root / "kpi_record.json").write_text(json.dumps(_json_ready(kpi_record), indent=2), encoding="utf-8")

    run_summary = {
        "run_id": run_id,
        "training_dataset_id": training_dataset_id,
        "source_dataset_id": source_dataset_id,
        "rows": summary["rows"],
        "threshold_log_return": summary["threshold_log_return"],
        "split_summary": summary["split_summary"],
        "hashes": {
            "training_dataset_sha256": training_hash,
            "training_dataset_summary_sha256": summary_hash,
            "label_contract_sha256": label_contract_hash,
            "split_manifest_sha256": split_manifest_hash,
        },
    }
    (run_output_root / "summary.json").write_text(
        json.dumps(_json_ready(run_summary), indent=2),
        encoding="utf-8",
    )
    (run_output_root / "result_summary.md").write_text(
        render_result_summary(run_summary),
        encoding="utf-8-sig",
    )

    return {
        "training_dataset_id": training_dataset_id,
        "output_root": str(output_root.as_posix()),
        "run_output_root": str(run_output_root.as_posix()),
        "training_dataset_path": str(training_path.as_posix()),
        "training_dataset_summary_path": str(summary_path.as_posix()),
        "label_contract_path": str(label_contract_path.as_posix()),
        "split_manifest_path": str(split_manifest_path.as_posix()),
        "hashes": run_summary["hashes"],
    }


def render_result_summary(run_summary: dict[str, object]) -> str:
    split_summary = run_summary["split_summary"]
    lines = [
        "# Training Label/Split Materialization",
        "",
        "## 판독(Read, 판독)",
        "",
        f"`{run_summary['run_id']}` 실행(run, 실행)은 training label(학습 라벨)과 split contract(분할 계약)를 물질화했다.",
        "",
        "쉽게 말하면, 모델에게 줄 첫 시험지의 정답 기준과 연습/검증/표본외 구간을 실제 파일로 만들었다.",
        "",
        "## 핵심 수치(Key Numbers, 핵심 수치)",
        "",
        f"- training_dataset_id(학습 데이터셋 ID): `{run_summary['training_dataset_id']}`",
        f"- source_dataset_id(원천 데이터셋 ID): `{run_summary['source_dataset_id']}`",
        f"- rows(행 수): `{run_summary['rows']}`",
        f"- threshold_log_return(로그수익률 임계값): `{run_summary['threshold_log_return']}`",
    ]
    for split_name in ("train", "validation", "oos"):
        split = split_summary[split_name]
        dist = split["class_distribution"]
        lines.append(
            f"- {split_name}: `{split['rows']}` rows, short/flat/long = "
            f"`{dist['short']}/{dist['flat']}/{dist['long']}`"
        )
    lines.extend(
        [
            "",
            "## 경계(Boundary, 경계)",
            "",
            "이 실행(run, 실행)은 evidence(근거) 실행이다. model training(모델 학습), alpha quality(알파 품질), runtime authority(런타임 권위), operating promotion(운영 승격)을 주장하지 않는다.",
        ]
    )
    return "\n".join(lines) + "\n"


def materialize_training_label_split_dataset(
    *,
    source_dataset_id: str,
    training_dataset_id: str,
    features_path: Path,
    source_summary_path: Path,
    raw_root: Path,
    output_root: Path,
    run_output_root: Path,
    spec: TrainingLabelSplitSpec | None = None,
    run_id: str = RUN_ID,
    stage_id: str = STAGE_ID,
) -> dict[str, object]:
    active_spec = spec or TrainingLabelSplitSpec()
    feature_frame = load_feature_dataset(features_path)
    raw_close_frame = load_us100_close_series(raw_root)
    training_frame, summary = build_training_dataset(feature_frame, raw_close_frame, active_spec)
    return write_training_outputs(
        output_root=output_root,
        run_output_root=run_output_root,
        training_dataset_id=training_dataset_id,
        source_dataset_id=source_dataset_id,
        source_summary_path=source_summary_path,
        features_path=features_path,
        raw_root=raw_root,
        training_frame=training_frame,
        summary=summary,
        run_id=run_id,
        stage_id=stage_id,
    )


def main() -> int:
    args = parse_args()
    payload = materialize_training_label_split_dataset(
        source_dataset_id=args.source_dataset_id,
        training_dataset_id=args.training_dataset_id,
        features_path=Path(args.features_path),
        source_summary_path=Path(args.source_summary_path),
        raw_root=Path(args.raw_root),
        output_root=Path(args.output_root),
        run_output_root=Path(args.run_output_root),
        run_id=args.run_id,
        stage_id=args.stage_id,
    )
    print(json.dumps(_json_ready({"status": "ok", **payload}), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
