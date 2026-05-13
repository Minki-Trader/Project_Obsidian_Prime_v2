from __future__ import annotations

import argparse
import csv
import json
import sys
import traceback
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.alpha import scout_runner as scout  # noqa: E402
from foundation.control_plane.ledger import json_ready, ledger_pairs, sha256_file_lf_normalized, upsert_csv_rows  # noqa: E402
from foundation.control_plane.mt5_trade_attribution import MarketData  # noqa: E402
from foundation.pipelines.materialize_fpmarkets_v2_dataset import (  # noqa: E402
    EXPECTED_FEATURE_ORDER_HASH,
    FEATURE_ORDER,
    feature_order_hash,
)
from foundation.pipelines.materialize_model_input_dataset import (  # noqa: E402
    MODE_MT5_PRICE_PROXY_58,
    build_model_input_dataset,
    model_input_mode_config,
)
from foundation.pipelines.materialize_training_label_split_dataset import (  # noqa: E402
    LABEL_CONTRACT_VERSION,
    MATERIALIZER_VERSION,
    TIME_AXIS_POLICY_VERSION,
    TRAINING_FEATURE_CONTRACT_VERSION,
    TRAINING_PARSER_CONTRACT_VERSION,
    TrainingLabelSplitSpec,
    build_training_dataset,
    load_feature_dataset,
    load_us100_close_series,
)
from stage_pipelines.stage11 import lgbm_training_method_scout as lgbm_scout  # noqa: E402
from stage_pipelines.stage11 import lgbm_training_support as lgbm_support  # noqa: E402
from stage_pipelines.stage56 import deep_repair_suite as deep  # noqa: E402
from stage_pipelines.stage56 import reopen_optimization_batch as reopen  # noqa: E402


STAGE_ID = "56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection"
STAGE_NUMBER = 56
RUN_NUMBER = "run50AM"
PARENT_RUN_ID = "run50AM_stage56_lgbm_fwd6_density_branch_v1"
PACKET_ID = "stage56_run50AM_lgbm_fwd6_density_branch_v1"
EXPLORATION_LABEL = "stage56_BaseEngine__LGBMFwd6DensityBranch"
STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
REPORT_PATH = REVIEWS_ROOT / "run50AM_reopen_batch.md"
RESULTS_CSV_PATH = REVIEWS_ROOT / "run50AM_summary.csv"
AUDIT_CSV_PATH = REVIEWS_ROOT / "run50AM_audit.csv"
AGGREGATE_SUMMARY_PATH = Path("docs/agent_control/packets") / PACKET_ID / "aggregate_summary.json"
RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
STAGE_RUN_LEDGER_PATH = REVIEWS_ROOT / "stage_run_ledger.csv"
PROJECT_ALPHA_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
ARTIFACT_REGISTRY_PATH = Path("docs/registers/artifact_registry.csv")
CURRENT_STATE_PATH = Path("docs/workspace/workspace_state.yaml")
CURRENT_CONTEXT_PATH = Path("docs/context/current_working_state.md")

SOURCE_DATASET_ID = "dataset_fpmarkets_v2_us100_m5_20220901_20260413_cashopen_fullcash_proxyw58"
TRAINING_DATASET_ID = "training_fpmarkets_v2_us100_m5_label_v1_fwd6_split_v1_proxyw58_stage56_run50AM"
MODEL_INPUT_DATASET_ID = "model_input_fpmarkets_v2_us100_m5_label_v1_fwd6_split_v1_proxyw58_feature_set_v2_stage56_run50AM"
DEFAULT_FEATURES_PATH = Path("data/processed/datasets") / SOURCE_DATASET_ID / "features.parquet"
DEFAULT_SOURCE_SUMMARY_PATH = Path("data/processed/datasets") / SOURCE_DATASET_ID / "dataset_summary.json"
DEFAULT_RAW_ROOT = Path("data/raw/mt5_bars/m5")
INPUT_ROOT = RUN_ROOT / "_inputs"
TRAINING_OUTPUT_ROOT = INPUT_ROOT / "label_v1_fwd6_split_v1_proxyw58"
MODEL_INPUT_OUTPUT_ROOT = INPUT_ROOT / "label_v1_fwd6_split_v1_feature_set_v2_mt5_price_proxy_58"
DEFAULT_COMMON_FILES_ROOT = Path.home() / "AppData/Roaming/MetaQuotes/Terminal/Common/Files"
DEFAULT_TERMINAL_DATA_ROOT = REPO_ROOT.parents[2]
DEFAULT_TESTER_PROFILE_ROOT = REPO_ROOT.parents[1] / "Profiles" / "Tester"


@dataclass(frozen=True)
class LgbmFwd6Variant:
    variant_id: str
    group: str
    tier_a_short_threshold: float
    tier_a_long_threshold: float
    tier_b_short_threshold: float
    tier_b_long_threshold: float
    max_hold_bars: int
    random_seed: int
    n_estimators: int = 220
    learning_rate: float = 0.035
    num_leaves: int = 31
    min_child_samples: int = 80
    reg_lambda: float = 1.0
    class_weight: str | None = None
    invert_signal: bool = False
    fallback_invert_signal: bool = False
    tier_a_min_margin: float = 0.0
    tier_b_min_margin: float = 0.0
    session_slice_id: str | None = None
    notes: str = ""

    @property
    def run_id(self) -> str:
        return f"{RUN_NUMBER}_{self.variant_id}_lgbm_fwd6_v1"

    @property
    def base_id(self) -> str:
        return self.variant_id

    @property
    def tier_a_rule(self) -> scout.ThresholdRule:
        return scout.threshold_rule_from_values(
            threshold_id=_threshold_id(f"{self.variant_id}_a", self.tier_a_short_threshold, self.tier_a_long_threshold),
            short_threshold=self.tier_a_short_threshold,
            long_threshold=self.tier_a_long_threshold,
            min_margin=self.tier_a_min_margin,
        )

    @property
    def tier_b_rule(self) -> scout.ThresholdRule:
        return scout.threshold_rule_from_values(
            threshold_id=_threshold_id(f"{self.variant_id}_b", self.tier_b_short_threshold, self.tier_b_long_threshold),
            short_threshold=self.tier_b_short_threshold,
            long_threshold=self.tier_b_long_threshold,
            min_margin=self.tier_b_min_margin,
        )


DEFAULT_VARIANTS: tuple[LgbmFwd6Variant, ...] = (
    LgbmFwd6Variant(
        "lgbm6_s048l045_h4_b060",
        "short_horizon_density_asym",
        0.480,
        0.450,
        0.600,
        0.600,
        4,
        606,
        notes="fwd6 LGBM with long-friendlier threshold, hold4, strict Tier B to avoid hidden fallback damage",
    ),
    LgbmFwd6Variant(
        "lgbm6_s045l045_h4_b060",
        "short_horizon_density_symmetric",
        0.450,
        0.450,
        0.600,
        0.600,
        4,
        607,
        notes="fwd6 LGBM high-density threshold, hold4, strict Tier B damage check",
    ),
    LgbmFwd6Variant(
        "lgbm6_s050l045_h4_b060",
        "short_horizon_short_firewall",
        0.500,
        0.450,
        0.600,
        0.600,
        4,
        608,
        notes="fwd6 LGBM short-side confidence firewall with long-side density retained",
    ),
    LgbmFwd6Variant(
        "lgbm6_s048l045_h6_b060",
        "short_horizon_hold6_quality",
        0.480,
        0.450,
        0.600,
        0.600,
        6,
        609,
        notes="fwd6 LGBM hold6 quality comparison against hold4 density branch",
    ),
)


SUMMARY_COLUMNS = tuple(
    list(reopen.SUMMARY_COLUMNS[:-4])
    + [
        "model_family",
        "label_horizon_bars",
        "lgbm_random_seed",
        "lgbm_n_estimators",
        "lgbm_learning_rate",
        "lgbm_num_leaves",
        "lgbm_min_child_samples",
        "lgbm_reg_lambda",
        "lgbm_class_weight",
        "invert_signal",
        "fallback_invert_signal",
    ]
    + list(reopen.SUMMARY_COLUMNS[-4:])
)


def _threshold_id(prefix: str, short_threshold: float, long_threshold: float) -> str:
    short_bp = int(round(short_threshold * 1000))
    long_bp = int(round(long_threshold * 1000))
    return f"stage56_{prefix}_s{short_bp:03d}_l{long_bp:03d}_m000"


def _project_path(path: Path) -> Path:
    resolved = path if path.is_absolute() else REPO_ROOT / path
    if sys.platform == "win32":
        text = str(resolved)
        if not text.startswith("\\\\?\\"):
            return Path("\\\\?\\" + text)
    return resolved


def _read_json(path: Path) -> Any:
    return json.loads(_project_path(path).read_text(encoding="utf-8-sig"))


def _write_json(path: Path, payload: Mapping[str, Any]) -> None:
    target = _project_path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str]) -> None:
    target = _project_path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: row.get(column, "") for column in columns})


def _write_bom_text(path: Path, text: str) -> None:
    target = _project_path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def _float(value: Any, default: float = 0.0) -> float:
    try:
        if value == "":
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def _metric(summary: Mapping[str, Any], view: str, key: str) -> Any:
    for record in summary.get("mt5_kpi_records", []):
        if record.get("record_view") == view:
            metrics = record.get("metrics", {})
            if isinstance(metrics, Mapping):
                return metrics.get(key)
    return None


def _record(summary: Mapping[str, Any], view: str) -> Mapping[str, Any]:
    for record in summary.get("mt5_kpi_records", []):
        if record.get("record_view") == view:
            metrics = record.get("metrics", {})
            return metrics if isinstance(metrics, Mapping) else {}
    return {}


def _configure_external_modules() -> None:
    for module in (deep, reopen):
        module.RUN_NUMBER = RUN_NUMBER
        module.PARENT_RUN_ID = PARENT_RUN_ID
        module.PACKET_ID = PACKET_ID
        module.EXPLORATION_LABEL = EXPLORATION_LABEL
        module.RUN_ROOT = RUN_ROOT
        module.REPORT_PATH = REPORT_PATH
        module.RESULTS_CSV_PATH = RESULTS_CSV_PATH
        module.AUDIT_CSV_PATH = AUDIT_CSV_PATH
        module.AGGREGATE_SUMMARY_PATH = AGGREGATE_SUMMARY_PATH
        module.STAGE_RUN_LEDGER_PATH = STAGE_RUN_LEDGER_PATH
        module.PROJECT_ALPHA_LEDGER_PATH = PROJECT_ALPHA_LEDGER_PATH
        module.RUN_REGISTRY_PATH = RUN_REGISTRY_PATH
    for module in (lgbm_support, lgbm_scout):
        module.STAGE_ID = STAGE_ID
        module.STAGE_RUN_LEDGER_PATH = STAGE_RUN_LEDGER_PATH
        module.PROJECT_ALPHA_LEDGER_PATH = PROJECT_ALPHA_LEDGER_PATH
        module.RUN_REGISTRY_PATH = RUN_REGISTRY_PATH
        module.MODEL_INPUT_DATASET_ID = MODEL_INPUT_DATASET_ID
        module.FEATURE_SET_ID = model_input_mode_config(MODE_MT5_PRICE_PROXY_58).feature_set_id


def _set_hold_reference(max_hold_bars: int) -> None:
    for module in (lgbm_support, lgbm_scout):
        module.RUN01Y_REFERENCE["max_hold_bars"] = int(max_hold_bars)
        module.RUN01Y_REFERENCE["session_slice_id"] = "full_cash_session"
        module.RUN01Y_REFERENCE["run_id"] = "stage56_lgbm_fwd6_density_branch_local_reference"


def _materialize_fwd6_inputs(
    *,
    features_path: Path,
    source_summary_path: Path,
    raw_root: Path,
    force: bool,
) -> dict[str, Any]:
    training_path = TRAINING_OUTPUT_ROOT / "training_dataset.parquet"
    training_summary_path = TRAINING_OUTPUT_ROOT / "training_dataset_summary.json"
    model_input_path = MODEL_INPUT_OUTPUT_ROOT / "model_input_dataset.parquet"
    model_input_summary_path = MODEL_INPUT_OUTPUT_ROOT / "model_input_summary.json"
    model_input_feature_order_path = MODEL_INPUT_OUTPUT_ROOT / "model_input_feature_order.txt"
    input_manifest_path = INPUT_ROOT / "fwd6_input_manifest.json"
    if (
        not force
        and _project_path(training_path).exists()
        and _project_path(training_summary_path).exists()
        and _project_path(model_input_path).exists()
        and _project_path(model_input_feature_order_path).exists()
    ):
        return {
            "training_dataset_path": training_path,
            "training_summary_path": training_summary_path,
            "training_summary": _read_json(training_summary_path),
            "model_input_path": model_input_path,
            "model_input_summary_path": model_input_summary_path,
            "model_input_feature_order_path": model_input_feature_order_path,
            "input_manifest_path": input_manifest_path,
            "label_spec": TrainingLabelSplitSpec(label_id="label_v1_fwd6_m5_logret_train_q33_3class", horizon_bars=6),
            "model_input_feature_set_id": model_input_mode_config(MODE_MT5_PRICE_PROXY_58).feature_set_id,
            "status": "reused_existing",
        }

    spec = TrainingLabelSplitSpec(
        label_id="label_v1_fwd6_m5_logret_train_q33_3class",
        horizon_bars=6,
    )
    current_feature_hash = feature_order_hash()
    if current_feature_hash != EXPECTED_FEATURE_ORDER_HASH:
        raise RuntimeError(f"Feature order hash mismatch: {current_feature_hash} != {EXPECTED_FEATURE_ORDER_HASH}")

    feature_frame = load_feature_dataset(features_path)
    raw_close_frame = load_us100_close_series(raw_root)
    training_frame, training_summary = build_training_dataset(feature_frame, raw_close_frame, spec)
    model_input_frame, model_input_summary = build_model_input_dataset(training_frame, mode=MODE_MT5_PRICE_PROXY_58)
    model_input_config = model_input_mode_config(MODE_MT5_PRICE_PROXY_58)

    _project_path(TRAINING_OUTPUT_ROOT).mkdir(parents=True, exist_ok=True)
    training_frame.to_parquet(_project_path(training_path), index=False)
    _project_path(TRAINING_OUTPUT_ROOT / "feature_order.txt").write_text("\n".join(FEATURE_ORDER) + "\n", encoding="utf-8")
    training_contract = {
        "training_dataset_id": TRAINING_DATASET_ID,
        "source_dataset_id": SOURCE_DATASET_ID,
        "source_summary_path": source_summary_path.as_posix(),
        "materializer_version": MATERIALIZER_VERSION,
        "label_contract_version": LABEL_CONTRACT_VERSION,
        "feature_contract_version": TRAINING_FEATURE_CONTRACT_VERSION,
        "parser_contract_version": TRAINING_PARSER_CONTRACT_VERSION,
        "time_axis_policy_version": TIME_AXIS_POLICY_VERSION,
        "feature_order_hash": current_feature_hash,
        **training_summary,
    }
    _write_json(training_summary_path, training_contract)
    _write_json(
        TRAINING_OUTPUT_ROOT / "label_contract.json",
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
    _write_json(
        TRAINING_OUTPUT_ROOT / "split_manifest.json",
        {
            "training_dataset_id": TRAINING_DATASET_ID,
            "split_id": training_summary["split_id"],
            "split_boundaries": training_summary["split_boundaries"],
            "split_summary": training_summary["split_summary"],
        },
    )

    _project_path(MODEL_INPUT_OUTPUT_ROOT).mkdir(parents=True, exist_ok=True)
    model_input_frame.to_parquet(_project_path(model_input_path), index=False)
    _project_path(model_input_feature_order_path).write_text(
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
    _write_json(model_input_summary_path, model_input_contract)
    _write_json(
        MODEL_INPUT_OUTPUT_ROOT / "feature_set_manifest.json",
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
    _write_json(
        input_manifest_path,
        {
            "run_id": PARENT_RUN_ID,
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
                "Stage56 exploratory fwd6 relabel branch. "
                "This does not replace the default fwd12 project contract."
            ),
        },
    )
    return {
        "training_dataset_path": training_path,
        "training_summary_path": training_summary_path,
        "training_summary": training_contract,
        "model_input_path": model_input_path,
        "model_input_summary_path": model_input_summary_path,
        "model_input_feature_order_path": model_input_feature_order_path,
        "input_manifest_path": input_manifest_path,
        "label_spec": spec,
        "model_input_feature_set_id": model_input_config.feature_set_id,
        "status": "materialized",
    }


def _select_variants(
    *,
    selected_ids: Iterable[str] | None,
    selected_groups: Iterable[str] | None,
    max_variants: int | None,
) -> tuple[LgbmFwd6Variant, ...]:
    selected = list(DEFAULT_VARIANTS)
    if selected_groups:
        wanted_groups = {group.strip() for group in selected_groups if group.strip()}
        selected = [variant for variant in selected if variant.group in wanted_groups]
    if selected_ids:
        wanted = {variant_id.strip() for variant_id in selected_ids if variant_id.strip()}
        selected = [variant for variant in selected if variant.variant_id in wanted]
        missing = sorted(wanted.difference(variant.variant_id for variant in selected))
        if missing:
            raise ValueError(f"Unknown variant ids: {missing}")
    if max_variants is not None:
        selected = selected[: int(max_variants)]
    if not selected:
        raise ValueError("At least one variant is required.")
    return tuple(selected)


def _run_variant(
    variant: LgbmFwd6Variant,
    *,
    input_payload: Mapping[str, Any],
    attempt_mt5: bool,
    common_files_root: Path,
    terminal_data_root: Path,
    tester_profile_root: Path,
    terminal_path: Path,
    metaeditor_path: Path,
    force: bool,
) -> dict[str, Any]:
    run_output_root = RUN_ROOT / variant.variant_id
    summary_path = run_output_root / "summary.json"
    if _project_path(summary_path).exists() and not force:
        summary = _read_json(summary_path)
        return {
            "status": "skipped_existing",
            "variant_id": variant.variant_id,
            "run_id": variant.run_id,
            "summary_path": summary_path.as_posix(),
            "external_verification_status": summary.get("external_verification_status"),
        }

    _set_hold_reference(variant.max_hold_bars)
    config = lgbm_support.LgbmTrainingConfig(
        random_seed=variant.random_seed,
        n_estimators=variant.n_estimators,
        learning_rate=variant.learning_rate,
        num_leaves=variant.num_leaves,
        min_child_samples=variant.min_child_samples,
        reg_lambda=variant.reg_lambda,
        class_weight=variant.class_weight,
    )
    payload = lgbm_scout.run_stage11_lgbm_training_method_scout(
        model_input_path=Path(input_payload["model_input_path"]),
        feature_order_path=_project_path(Path(input_payload["model_input_feature_order_path"])),
        tier_b_model_input_path=lgbm_support.DEFAULT_TIER_B_MODEL_INPUT_PATH,
        tier_b_feature_order_path=lgbm_support.DEFAULT_TIER_B_FEATURE_ORDER_PATH,
        raw_root=DEFAULT_RAW_ROOT,
        training_summary_path=Path(input_payload["training_summary_path"]),
        run_output_root=run_output_root,
        common_files_root=common_files_root,
        terminal_data_root=terminal_data_root,
        tester_profile_root=tester_profile_root,
        terminal_path=terminal_path,
        metaeditor_path=metaeditor_path,
        run_id=variant.run_id,
        run_number=RUN_NUMBER,
        exploration_label=f"{EXPLORATION_LABEL}__{variant.variant_id}",
        config=config,
        session_slice_id=variant.session_slice_id,
        max_hold_bars=variant.max_hold_bars,
        tier_a_rule=variant.tier_a_rule,
        tier_b_rule=variant.tier_b_rule,
        invert_signal=variant.invert_signal,
        fallback_invert_signal=variant.fallback_invert_signal,
        attempt_mt5=attempt_mt5,
        label_spec=input_payload["label_spec"],
        tier_a_model_input_dataset_id=MODEL_INPUT_DATASET_ID,
        tier_a_feature_set_id=input_payload["model_input_feature_set_id"],
        decision_surface_id=(
            f"{variant.variant_id}_fwd6_s{int(variant.tier_a_short_threshold * 1000)}"
            f"_l{int(variant.tier_a_long_threshold * 1000)}_hold{variant.max_hold_bars}"
        ),
        selection_policy="stage56_fwd6_lgbm_density_branch_threshold_probe",
        run_registry_lane="stage56_lgbm_fwd6_density_branch",
        judgment_prefix="stage56_lgbm_fwd6_density_branch",
        hypothesis=variant.notes,
    )
    payload["variant_id"] = variant.variant_id
    payload["summary_path"] = summary_path.as_posix()
    return payload


def _row_from_summary(variant: LgbmFwd6Variant, summary_path: Path) -> dict[str, Any]:
    summary = _read_json(summary_path)
    route_coverage = summary.get("route_coverage", {})
    row = {
        "variant_id": variant.variant_id,
        "group": variant.group,
        "run_id": variant.run_id,
        "external_verification_status": summary.get("external_verification_status", ""),
        "threshold_id": summary.get("selected_threshold_id", ""),
        "tier_a_short_threshold": variant.tier_a_short_threshold,
        "tier_a_long_threshold": variant.tier_a_long_threshold,
        "tier_a_min_margin": variant.tier_a_min_margin,
        "tier_b_short_threshold": variant.tier_b_short_threshold,
        "tier_b_long_threshold": variant.tier_b_long_threshold,
        "tier_b_min_margin": variant.tier_b_min_margin,
        "max_hold_bars": variant.max_hold_bars,
        "session_slice_id": variant.session_slice_id or "",
        "tier_b_allowed_subtypes": "",
        "base_id": variant.base_id,
        "routed_fallback_enabled": "true",
        "model_family": summary.get("model_family", lgbm_support.MODEL_FAMILY),
        "label_horizon_bars": 6,
        "lgbm_random_seed": variant.random_seed,
        "lgbm_n_estimators": variant.n_estimators,
        "lgbm_learning_rate": variant.learning_rate,
        "lgbm_num_leaves": variant.num_leaves,
        "lgbm_min_child_samples": variant.min_child_samples,
        "lgbm_reg_lambda": variant.reg_lambda,
        "lgbm_class_weight": variant.class_weight or "",
        "invert_signal": str(bool(variant.invert_signal)).lower(),
        "fallback_invert_signal": str(bool(variant.fallback_invert_signal)).lower(),
        "judgment": summary.get("judgment", ""),
        "error": "",
        "summary_path": summary_path.as_posix(),
        "notes": variant.notes,
        "route_coverage_by_split": json.dumps(route_coverage.get("by_split", {}), ensure_ascii=False, sort_keys=True),
    }
    for prefix, view in (
        ("tier_a_validation", "mt5_tier_a_only_validation_is"),
        ("tier_a_oos", "mt5_tier_a_only_oos"),
        ("tier_b_validation", "mt5_tier_b_fallback_only_validation_is"),
        ("tier_b_oos", "mt5_tier_b_fallback_only_oos"),
        ("routed_validation", "mt5_routed_total_validation_is"),
        ("routed_oos", "mt5_routed_total_oos"),
    ):
        record = _record(summary, view)
        row[f"{prefix}_closed_trades"] = record.get("trade_count")
        row[f"{prefix}_net_profit"] = record.get("net_profit")
        row[f"{prefix}_profit_factor"] = record.get("profit_factor")
        if prefix.startswith("routed_"):
            days = reopen.VALIDATION_DAYS if "validation" in prefix else reopen.OOS_DAYS
            row[f"{prefix}_trades_per_day"] = (
                _float(record.get("trade_count")) / days if record.get("trade_count") is not None else ""
            )
            row[f"{prefix}_drawdown"] = record.get("max_drawdown_amount")
            row[f"{prefix}_short_trades"] = record.get("short_trade_count")
            row[f"{prefix}_long_trades"] = record.get("long_trade_count")
            row[f"{prefix}_report_path"] = record.get("report_path", "")
            row[f"{prefix}_aggregation"] = record.get("aggregation", "")
    row["routed_validation_b_fallback_bars"] = _metric(summary, "mt5_routed_total_validation_is", "tier_b_fallback_used_count")
    row["routed_oos_b_fallback_bars"] = _metric(summary, "mt5_routed_total_oos", "tier_b_fallback_used_count")
    return row


def _write_artifact_registry(final_read: Mapping[str, Any]) -> dict[str, Any]:
    rows: list[dict[str, str]] = []
    artifacts = (
        (f"{RUN_NUMBER}_aggregate_summary", AGGREGATE_SUMMARY_PATH),
        (f"{RUN_NUMBER}_summary_csv", RESULTS_CSV_PATH),
        (f"{RUN_NUMBER}_audit_csv", AUDIT_CSV_PATH),
        (f"{RUN_NUMBER}_review_packet", REPORT_PATH),
        ("stage56_progress_log", reopen.PROGRESS_LOG_PATH),
    )
    for role, path in artifacts:
        if not _project_path(path).exists():
            continue
        rows.append(
            {
                "artifact_id": f"{PARENT_RUN_ID}__{role}",
                "artifact_type": role,
                "path": path.as_posix(),
                "sha256": sha256_file_lf_normalized(path),
                "stage_id": STAGE_ID,
                "run_id": PARENT_RUN_ID,
                "created_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
                "notes": ledger_pairs(
                    (
                        ("selected_research_baseline", final_read.get("selected_research_baseline") or "none"),
                        ("boundary", "stage56_lgbm_fwd6_density_branch_progress_checkpoint"),
                    )
                ),
            }
        )
    if not rows:
        return {"status": "no_artifacts"}
    return upsert_csv_rows(ARTIFACT_REGISTRY_PATH, ("artifact_id", "artifact_type", "path", "sha256", "stage_id", "run_id", "created_at_utc", "notes"), rows, key="artifact_id")


def _update_current_truth(rows: Sequence[Mapping[str, Any]], final_read: Mapping[str, Any]) -> None:
    best = final_read.get("best_variant")
    best_map = best if isinstance(best, Mapping) else {}
    best_id = best_map.get("variant_id") or "none"
    _write_bom_text(
        CURRENT_CONTEXT_PATH,
        "\n".join(
            [
                "# Current Working State(현재 작업 상태)",
                "",
                f"- current_packet(현재 작업 묶음): `{PACKET_ID}`",
                f"- current run(현재 실행): `{PARENT_RUN_ID}`",
                f"- active stage(활성 단계): `{STAGE_ID}`",
                "- selected_research_baseline(선택 연구 기준선): `none`",
                "- status(상태): active_in_progress(활성 진행 중)",
                "- terminal_condition(종료 조건): useful BaselineAdapter(유용한 기준선 어댑터) hard condition(강한 완료 조건) satisfied(충족)",
                "",
                "Stage56(56단계)은 unfinished optimization campaign(미완 최적화 캠페인)으로 계속 열려 있다. Effect(효과): run50AM(실행50AM)은 fwd6 LGBM(6봉 LightGBM) separate model branch(별도 모델 분기)를 실제 MT5 validation/OOS(검증/표본외)로 확인하는 중간 근거다.",
                "",
                "## Latest Evidence(최신 근거)",
                "",
                f"- latest_batch(최신 묶음): `{PARENT_RUN_ID}`",
                f"- selected_research_baseline(선택 연구 기준선): `{final_read.get('selected_research_baseline') or 'none'}`",
                f"- best_variant(현재 최선 변형): `{best_id}`",
                f"- stage56_remains_open(56단계 계속 열림): `{bool(final_read.get('stage56_remains_open'))}`",
                "- forbidden claims(금지 주장): live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(운영 기준선), reviewed_closed(검토 종료)",
                "",
                "## Current Bottleneck(현재 병목)",
                "",
                "- OOS density(표본외 밀도), cost-stressed expectancy(비용 압박 기대값), same-move split re-entry(동일 이동 분할 재진입), and route coverage(라우팅 커버리지).",
                "- next_hypothesis_branch(다음 가설 분기): `continue_or_demote_lgbm_fwd6_after_same_move_and_cost_audit`",
            ]
        ),
    )
    state_text = _project_path(CURRENT_STATE_PATH).read_text(encoding="utf-8-sig")
    replacement = f"current_run_id: {PARENT_RUN_ID}"
    lines = state_text.splitlines()
    if lines and lines[0].startswith("current_run_id:"):
        lines[0] = replacement
    else:
        lines.insert(0, replacement)
    note = (
        f"Stage56(56단계) `{STAGE_ID}`: {PARENT_RUN_ID}(현재 실행 묶음) 완료; "
        f"best_variant(현재 최선 변형)는 `{best_id}`, selected_research_baseline(선택 연구 기준선)은 `none`이다. "
        "Effect(효과): latest BaselineAdapter research evidence(최신 기준선 어댑터 연구 근거)를 current_focus"
        "(현재 초점)에 보존한다."
    )
    try:
        focus_index = lines.index("current_focus:")
    except ValueError:
        lines.extend(["current_focus:"])
        focus_index = len(lines) - 1
    lines.insert(focus_index + 1, f"  {note}")
    lines.insert(focus_index + 1, "- >-")
    _write_bom_text(CURRENT_STATE_PATH, "\n".join(lines))


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Stage56 LGBM fwd6 density branch.")
    parser.add_argument("--features-path", default=str(DEFAULT_FEATURES_PATH))
    parser.add_argument("--source-summary-path", default=str(DEFAULT_SOURCE_SUMMARY_PATH))
    parser.add_argument("--raw-root", default=str(DEFAULT_RAW_ROOT))
    parser.add_argument("--variant-id", action="append", default=[])
    parser.add_argument("--variant-group", action="append", default=[])
    parser.add_argument("--max-variants", type=int, default=None)
    parser.add_argument("--attempt-mt5", action="store_true")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--common-files-root", default=str(DEFAULT_COMMON_FILES_ROOT))
    parser.add_argument("--terminal-data-root", default=str(DEFAULT_TERMINAL_DATA_ROOT))
    parser.add_argument("--tester-profile-root", default=str(DEFAULT_TESTER_PROFILE_ROOT))
    parser.add_argument("--terminal-path", default=r"C:\Program Files\MetaTrader 5\terminal64.exe")
    parser.add_argument("--metaeditor-path", default=r"C:\Program Files\MetaTrader 5\MetaEditor64.exe")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    _configure_external_modules()
    variants = _select_variants(
        selected_ids=args.variant_id,
        selected_groups=args.variant_group,
        max_variants=args.max_variants,
    )
    input_payload = _materialize_fwd6_inputs(
        features_path=Path(args.features_path),
        source_summary_path=Path(args.source_summary_path),
        raw_root=Path(args.raw_root),
        force=bool(args.force),
    )
    results: list[dict[str, Any]] = []
    rows: list[dict[str, Any]] = []
    for variant in variants:
        try:
            result = _run_variant(
                variant,
                input_payload=input_payload,
                attempt_mt5=bool(args.attempt_mt5),
                common_files_root=Path(args.common_files_root),
                terminal_data_root=Path(args.terminal_data_root),
                tester_profile_root=Path(args.tester_profile_root),
                terminal_path=Path(args.terminal_path),
                metaeditor_path=Path(args.metaeditor_path),
                force=bool(args.force),
            )
            results.append(result)
            summary_path = RUN_ROOT / variant.variant_id / "summary.json"
            rows.append(_row_from_summary(variant, summary_path))
        except Exception as exc:  # pragma: no cover - batch evidence must preserve failures.
            results.append(
                {
                    "status": "exception",
                    "variant_id": variant.variant_id,
                    "run_id": variant.run_id,
                    "error": str(exc),
                    "traceback": traceback.format_exc(),
                }
            )
            rows.append(
                {
                    "variant_id": variant.variant_id,
                    "group": variant.group,
                    "run_id": variant.run_id,
                    "external_verification_status": "blocked",
                    "threshold_id": "",
                    "tier_a_short_threshold": variant.tier_a_short_threshold,
                    "tier_a_long_threshold": variant.tier_a_long_threshold,
                    "tier_a_min_margin": variant.tier_a_min_margin,
                    "tier_b_short_threshold": variant.tier_b_short_threshold,
                    "tier_b_long_threshold": variant.tier_b_long_threshold,
                    "tier_b_min_margin": variant.tier_b_min_margin,
                    "max_hold_bars": variant.max_hold_bars,
                    "session_slice_id": variant.session_slice_id or "",
                    "tier_b_allowed_subtypes": "",
                    "base_id": variant.base_id,
                    "routed_fallback_enabled": "true",
                    "judgment": "blocked_stage56_lgbm_fwd6_density_branch_exception",
                    "error": str(exc),
                    "summary_path": (RUN_ROOT / variant.variant_id / "summary.json").as_posix(),
                    "notes": variant.notes,
                }
            )

    market_data = MarketData.load(REPO_ROOT)
    reference_audits, reference_capture = reopen._reference_capture_by_split(market_data, cost_stress_per_trade=0.50)
    audit_rows = reference_audits + reopen._audit_rows(
        rows,
        market_data=market_data,
        cost_stress_per_trade=0.50,
        reference_capture=reference_capture,
    )
    final_read = reopen._selected_read(rows, audit_rows)
    _write_csv(RESULTS_CSV_PATH, rows, SUMMARY_COLUMNS)
    _write_csv(AUDIT_CSV_PATH, audit_rows, reopen.AUDIT_COLUMNS)
    reopen._write_report(rows, audit_rows, final_read, attempt_mt5=bool(args.attempt_mt5))
    reopen._write_progress_log(rows, audit_rows, final_read)
    ledger_payload = reopen._write_parent_rows(rows, final_read)
    reopen._write_aggregate_summary(results, rows, audit_rows, final_read, ledger_payload)
    artifact_payload = _write_artifact_registry(final_read)
    _update_current_truth(rows, final_read)
    input_materialization = {
        key: value
        for key, value in input_payload.items()
        if key != "label_spec"
    }
    input_materialization["label_spec"] = {
        "label_id": input_payload["label_spec"].label_id,
        "horizon_bars": input_payload["label_spec"].horizon_bars,
        "horizon_minutes": input_payload["label_spec"].horizon_minutes,
        "threshold_abs_quantile": input_payload["label_spec"].threshold_abs_quantile,
    }
    print(
        json.dumps(
            json_ready(
                {
                    "status": "ok",
                    "packet_id": PACKET_ID,
                    "run_id": PARENT_RUN_ID,
                    "variant_count": len(rows),
                    "selected_research_baseline": final_read.get("selected_research_baseline") or "none",
                    "best_variant": (final_read.get("best_variant") or {}).get("variant_id")
                    if isinstance(final_read.get("best_variant"), Mapping)
                    else None,
                    "stage56_remains_open": final_read.get("stage56_remains_open"),
                    "results_csv_path": RESULTS_CSV_PATH.as_posix(),
                    "audit_csv_path": AUDIT_CSV_PATH.as_posix(),
                    "aggregate_summary_path": AGGREGATE_SUMMARY_PATH.as_posix(),
                    "artifact_registry": artifact_payload,
                    "input_materialization": input_materialization,
                }
            ),
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
