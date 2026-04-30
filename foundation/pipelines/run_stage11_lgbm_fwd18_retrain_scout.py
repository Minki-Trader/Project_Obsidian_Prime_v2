from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Mapping

import pandas as pd


REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.alpha import scout_runner as scout  # noqa: E402
from foundation.pipelines import run_stage11_lgbm_training_method_scout as run02a  # noqa: E402
from foundation.pipelines.materialize_model_input_dataset import (  # noqa: E402
    MODE_MT5_PRICE_PROXY_58,
    build_model_input_dataset,
    model_input_mode_config,
)
from foundation.pipelines.materialize_training_label_split_dataset import (  # noqa: E402
    MATERIALIZER_VERSION,
    LABEL_CONTRACT_VERSION,
    TIME_AXIS_POLICY_VERSION,
    TRAINING_FEATURE_CONTRACT_VERSION,
    TRAINING_PARSER_CONTRACT_VERSION,
    TrainingLabelSplitSpec,
    build_training_dataset,
    load_feature_dataset,
    load_us100_close_series,
)
from foundation.pipelines.materialize_fpmarkets_v2_dataset import (  # noqa: E402
    EXPECTED_FEATURE_ORDER_HASH,
    FEATURE_ORDER,
    feature_order_hash,
)


STAGE_ID = "11_alpha_robustness__wfo_label_horizon_sensitivity"
RUN_NUMBER = "run02W"
RUN_ID = "run02W_lgbm_fwd18_retrain_v1"
EXPLORATION_LABEL = "stage11_LabelHorizon__LGBMFwd18Retrain"
SOURCE_DATASET_ID = "dataset_fpmarkets_v2_us100_m5_20220901_20260413_cashopen_fullcash_proxyw58"
TRAINING_DATASET_ID = "training_fpmarkets_v2_us100_m5_label_v1_fwd18_split_v1_proxyw58"
MODEL_INPUT_DATASET_ID = "model_input_fpmarkets_v2_us100_m5_label_v1_fwd18_split_v1_proxyw58_feature_set_v2"
DEFAULT_FEATURES_PATH = Path("data/processed/datasets") / SOURCE_DATASET_ID / "features.parquet"
DEFAULT_SOURCE_SUMMARY_PATH = Path("data/processed/datasets") / SOURCE_DATASET_ID / "dataset_summary.json"
DEFAULT_RAW_ROOT = Path("data/raw/mt5_bars/m5")
DEFAULT_TRAINING_OUTPUT_ROOT = Path("data/processed/training_datasets/label_v1_fwd18_split_v1_proxyw58")
DEFAULT_MODEL_INPUT_OUTPUT_ROOT = Path("data/processed/model_inputs/label_v1_fwd18_split_v1_feature_set_v2_mt5_price_proxy_58")
DEFAULT_RUN_OUTPUT_ROOT = Path("stages") / STAGE_ID / "02_runs" / RUN_ID
DEFAULT_COMMON_FILES_ROOT = Path.home() / "AppData/Roaming/MetaQuotes/Terminal/Common/Files"
DEFAULT_TERMINAL_DATA_ROOT = REPO_ROOT.parents[2]
DEFAULT_TESTER_PROFILE_ROOT = REPO_ROOT.parents[1] / "Profiles" / "Tester"
DECISION_SURFACE_ID = "run02W_lgbm_fwd18_retrain_short0600_long0450_margin000_hold9_slice200_220"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Stage 11 RUN02W LGBM fwd18 retrain scout.")
    parser.add_argument("--features-path", default=str(DEFAULT_FEATURES_PATH))
    parser.add_argument("--source-summary-path", default=str(DEFAULT_SOURCE_SUMMARY_PATH))
    parser.add_argument("--raw-root", default=str(DEFAULT_RAW_ROOT))
    parser.add_argument("--training-output-root", default=str(DEFAULT_TRAINING_OUTPUT_ROOT))
    parser.add_argument("--model-input-output-root", default=str(DEFAULT_MODEL_INPUT_OUTPUT_ROOT))
    parser.add_argument("--run-output-root", default=str(DEFAULT_RUN_OUTPUT_ROOT))
    parser.add_argument("--attempt-mt5", action="store_true")
    parser.add_argument("--common-files-root", default=str(DEFAULT_COMMON_FILES_ROOT))
    parser.add_argument("--terminal-data-root", default=str(DEFAULT_TERMINAL_DATA_ROOT))
    parser.add_argument("--tester-profile-root", default=str(DEFAULT_TESTER_PROFILE_ROOT))
    parser.add_argument("--terminal-path", default=r"C:\Program Files\MetaTrader 5\terminal64.exe")
    parser.add_argument("--metaeditor-path", default=r"C:\Program Files\MetaTrader 5\MetaEditor64.exe")
    return parser.parse_args()


def write_json(path: Path, payload: Mapping[str, Any]) -> None:
    scout._io_path(path.parent).mkdir(parents=True, exist_ok=True)
    scout._io_path(path).write_text(
        json.dumps(scout._json_ready(payload), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def materialize_fwd18_training_inputs(
    *,
    features_path: Path,
    source_summary_path: Path,
    raw_root: Path,
    training_output_root: Path,
    model_input_output_root: Path,
    run_output_root: Path,
) -> dict[str, Any]:
    spec = TrainingLabelSplitSpec(
        label_id="label_v1_fwd18_m5_logret_train_q33_3class",
        horizon_bars=18,
    )
    current_feature_hash = feature_order_hash()
    if current_feature_hash != EXPECTED_FEATURE_ORDER_HASH:
        raise RuntimeError(f"Feature order hash mismatch: {current_feature_hash} != {EXPECTED_FEATURE_ORDER_HASH}")

    feature_frame = load_feature_dataset(features_path)
    raw_close_frame = load_us100_close_series(raw_root)
    training_frame, training_summary = build_training_dataset(feature_frame, raw_close_frame, spec)

    scout._io_path(training_output_root).mkdir(parents=True, exist_ok=True)
    training_path = training_output_root / "training_dataset.parquet"
    training_summary_path = training_output_root / "training_dataset_summary.json"
    label_contract_path = training_output_root / "label_contract.json"
    split_manifest_path = training_output_root / "split_manifest.json"
    feature_order_path = training_output_root / "feature_order.txt"

    training_frame.to_parquet(scout._io_path(training_path), index=False)
    scout._io_path(feature_order_path).write_text("\n".join(FEATURE_ORDER) + "\n", encoding="utf-8")
    training_contract = {
        "training_dataset_id": TRAINING_DATASET_ID,
        "source_dataset_id": SOURCE_DATASET_ID,
        "materializer_version": MATERIALIZER_VERSION,
        "label_contract_version": LABEL_CONTRACT_VERSION,
        "feature_contract_version": TRAINING_FEATURE_CONTRACT_VERSION,
        "parser_contract_version": TRAINING_PARSER_CONTRACT_VERSION,
        "time_axis_policy_version": TIME_AXIS_POLICY_VERSION,
        "feature_order_hash": current_feature_hash,
        **training_summary,
    }
    write_json(training_summary_path, training_contract)
    write_json(
        label_contract_path,
        {
            key: training_contract[key]
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
        },
    )
    write_json(
        split_manifest_path,
        {
            "training_dataset_id": TRAINING_DATASET_ID,
            "split_id": training_summary["split_id"],
            "split_boundaries": training_summary["split_boundaries"],
            "split_summary": training_summary["split_summary"],
        },
    )

    model_input_frame, model_input_summary = build_model_input_dataset(training_frame, mode=MODE_MT5_PRICE_PROXY_58)
    model_input_config = model_input_mode_config(MODE_MT5_PRICE_PROXY_58)
    scout._io_path(model_input_output_root).mkdir(parents=True, exist_ok=True)
    model_input_path = model_input_output_root / "model_input_dataset.parquet"
    model_input_summary_path = model_input_output_root / "model_input_summary.json"
    model_input_feature_order_path = model_input_output_root / "model_input_feature_order.txt"
    feature_set_manifest_path = model_input_output_root / "feature_set_manifest.json"

    model_input_frame.to_parquet(scout._io_path(model_input_path), index=False)
    scout._io_path(model_input_feature_order_path).write_text(
        "\n".join(model_input_config.feature_order) + "\n",
        encoding="utf-8",
    )
    model_input_contract = {
        "model_input_dataset_id": MODEL_INPUT_DATASET_ID,
        "source_training_dataset_id": TRAINING_DATASET_ID,
        "source_training_dataset_path": training_path.as_posix(),
        "source_training_summary_path": training_summary_path.as_posix(),
        **model_input_summary,
    }
    write_json(model_input_summary_path, model_input_contract)
    write_json(
        feature_set_manifest_path,
        {
            "feature_set_id": model_input_summary["feature_set_id"],
            "model_input_dataset_id": MODEL_INPUT_DATASET_ID,
            "source_training_dataset_id": TRAINING_DATASET_ID,
            "included_feature_order": model_input_config.feature_order,
            "included_feature_order_hash": model_input_summary["included_feature_order_hash"],
            "source_feature_order_hash": model_input_summary["source_feature_order_hash"],
            "source_feature_count": model_input_summary["source_feature_count"],
            "included_feature_count": model_input_summary["included_feature_count"],
        },
    )

    input_manifest_path = run_output_root / "inputs" / "fwd18_input_manifest.json"
    write_json(
        input_manifest_path,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "source_dataset_id": SOURCE_DATASET_ID,
            "features_path": features_path.as_posix(),
            "source_summary_path": source_summary_path.as_posix(),
            "raw_root": raw_root.as_posix(),
            "label_spec": {
                "label_id": spec.label_id,
                "horizon_bars": spec.horizon_bars,
                "horizon_minutes": spec.horizon_minutes,
                "threshold_abs_quantile": spec.threshold_abs_quantile,
                "threshold_log_return": training_summary["threshold_log_return"],
            },
            "training_dataset": {
                "dataset_id": TRAINING_DATASET_ID,
                "path": training_path.as_posix(),
                "summary_path": training_summary_path.as_posix(),
                "rows": training_summary["rows"],
                "sha256": scout.sha256_file(training_path),
            },
            "model_input_dataset": {
                "dataset_id": MODEL_INPUT_DATASET_ID,
                "path": model_input_path.as_posix(),
                "summary_path": model_input_summary_path.as_posix(),
                "rows": model_input_summary["rows"],
                "feature_order_path": model_input_feature_order_path.as_posix(),
                "sha256": scout.sha256_file(model_input_path),
            },
            "boundary": (
                "Stage 11 exploratory relabel/retrain input. "
                "This does not replace the default fwd12 contract."
            ),
        },
    )
    return {
        "label_spec": spec,
        "training_dataset_path": training_path,
        "training_summary_path": training_summary_path,
        "training_summary": training_summary,
        "model_input_path": model_input_path,
        "model_input_summary_path": model_input_summary_path,
        "model_input_feature_order_path": model_input_feature_order_path,
        "model_input_feature_set_id": model_input_config.feature_set_id,
        "input_manifest_path": input_manifest_path,
    }


def main() -> int:
    args = parse_args()
    run_output_root = Path(args.run_output_root)
    input_payload = materialize_fwd18_training_inputs(
        features_path=Path(args.features_path),
        source_summary_path=Path(args.source_summary_path),
        raw_root=Path(args.raw_root),
        training_output_root=Path(args.training_output_root),
        model_input_output_root=Path(args.model_input_output_root),
        run_output_root=run_output_root,
    )
    tier_a_rule = scout.threshold_rule_from_values(
        threshold_id="short0.600_long0.450_margin0.000",
        short_threshold=0.600,
        long_threshold=0.450,
        min_margin=0.000,
    )
    tier_b_rule = scout.threshold_rule_from_values(
        threshold_id="short0.600_long0.450_margin0.000",
        short_threshold=0.600,
        long_threshold=0.450,
        min_margin=0.000,
    )
    payload = run02a.run_stage11_lgbm_training_method_scout(
        model_input_path=input_payload["model_input_path"],
        feature_order_path=input_payload["model_input_feature_order_path"],
        tier_b_model_input_path=run02a.DEFAULT_TIER_B_MODEL_INPUT_PATH,
        tier_b_feature_order_path=run02a.DEFAULT_TIER_B_FEATURE_ORDER_PATH,
        raw_root=Path(args.raw_root),
        training_summary_path=input_payload["training_summary_path"],
        run_output_root=run_output_root,
        common_files_root=Path(args.common_files_root),
        terminal_data_root=Path(args.terminal_data_root),
        tester_profile_root=Path(args.tester_profile_root),
        terminal_path=Path(args.terminal_path),
        metaeditor_path=Path(args.metaeditor_path),
        run_id=RUN_ID,
        run_number=RUN_NUMBER,
        exploration_label=EXPLORATION_LABEL,
        config=run02a.LgbmTrainingConfig(random_seed=18),
        session_slice_id=run02a.RUN01Y_REFERENCE["session_slice_id"],
        max_hold_bars=run02a.RUN01Y_REFERENCE["max_hold_bars"],
        tier_a_rule=tier_a_rule,
        tier_b_rule=tier_b_rule,
        attempt_mt5=bool(args.attempt_mt5),
        label_spec=input_payload["label_spec"],
        tier_a_model_input_dataset_id=MODEL_INPUT_DATASET_ID,
        tier_a_feature_set_id=input_payload["model_input_feature_set_id"],
        decision_surface_id=DECISION_SURFACE_ID,
        selection_policy="reuse_run01Y_threshold_surface_for_fwd18_label_horizon_retrain_probe",
        run_registry_lane="alpha_label_horizon_retrain_scout",
        judgment_prefix="label_horizon_fwd18_retrain_scout",
        hypothesis=(
            "RUN02T indicated that the RUN02S signal surface aligns better with fwd18 labels than fwd12 labels; "
            "RUN02W retrains LightGBM on fwd18 labels and checks whether the runtime surface improves."
        ),
    )
    payload["input_materialization"] = {
        "training_dataset_path": input_payload["training_dataset_path"].as_posix(),
        "training_summary_path": input_payload["training_summary_path"].as_posix(),
        "model_input_path": input_payload["model_input_path"].as_posix(),
        "model_input_summary_path": input_payload["model_input_summary_path"].as_posix(),
        "input_manifest_path": input_payload["input_manifest_path"].as_posix(),
    }
    print(json.dumps(scout._json_ready(payload), ensure_ascii=False, indent=2))
    return 0 if payload["status"] == "ok" else 1


if __name__ == "__main__":
    raise SystemExit(main())
