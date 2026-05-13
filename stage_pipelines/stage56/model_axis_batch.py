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

import joblib
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.control_plane.ledger import json_ready  # noqa: E402
from foundation.control_plane.mt5_trade_attribution import MarketData  # noqa: E402
from foundation.models.baseline_training import load_feature_order, validate_model_input_frame  # noqa: E402
from foundation.models.onnx_bridge import sha256_file  # noqa: E402
from stage_pipelines.stage56 import deep_repair_suite as deep  # noqa: E402
from stage_pipelines.stage56 import reopen_optimization_batch as reopen  # noqa: E402


STAGE_ID = "56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection"
RUN_NUMBER = "run50K"
PARENT_RUN_ID = "run50K_stage56_model_axis_density_repair_v1"
PACKET_ID = "stage56_run50K_model_axis_density_repair_v1"
EXPLORATION_LABEL = "stage56_BaseEngine__ModelAxisDensityRepair"
STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
REPORT_PATH = REVIEWS_ROOT / "run50K_reopen_batch.md"
RESULTS_CSV_PATH = REVIEWS_ROOT / "run50K_summary.csv"
AUDIT_CSV_PATH = REVIEWS_ROOT / "run50K_audit.csv"
AGGREGATE_SUMMARY_PATH = Path("docs/agent_control/packets") / PACKET_ID / "aggregate_summary.json"
RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
STAGE_RUN_LEDGER_PATH = REVIEWS_ROOT / "stage_run_ledger.csv"
PROJECT_ALPHA_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")


@dataclass(frozen=True)
class ModelAxisVariant:
    variant_id: str
    base_id: str
    group: str
    model_spec_id: str
    c_value: float
    class_weight: str | None
    flat_sample_weight: float | None
    nonflat_sample_weight: float | None
    train_start_utc: str | None
    tier_a_short_threshold: float
    tier_a_long_threshold: float
    tier_a_min_margin: float
    tier_b_short_threshold: float
    tier_b_long_threshold: float
    tier_b_min_margin: float
    max_hold_bars: int
    routed_fallback_enabled: bool
    reentry_cooldown_bars: int = 0
    entry_transition_only: bool = False
    entry_transition_rearm_min_confidence_delta: float = 0.0
    side_filter_id: str | None = None
    side_filter_enabled: bool = False
    tier_a_side_filter_feature_index: int = -1
    tier_b_side_filter_feature_index: int = -1
    block_short_feature_range: bool = False
    block_short_feature_min: float = 0.0
    block_short_feature_max: float = 0.0
    block_long_feature_range: bool = False
    block_long_feature_min: float = 0.0
    block_long_feature_max: float = 0.0
    session_slice_id: str | None = None
    tier_b_allowed_subtypes: tuple[str, ...] = ()
    notes: str = ""

    def to_deep_variant(self) -> deep.RepairVariant:
        return deep.RepairVariant(
            self.variant_id,
            self.group,
            self.tier_a_short_threshold,
            self.tier_a_long_threshold,
            self.tier_a_min_margin,
            self.tier_b_short_threshold,
            self.tier_b_long_threshold,
            self.tier_b_min_margin,
            self.max_hold_bars,
            session_slice_id=self.session_slice_id,
            tier_b_allowed_subtypes=self.tier_b_allowed_subtypes,
            notes=self.notes,
        )


DEFAULT_VARIANTS: tuple[ModelAxisVariant, ...] = (
    ModelAxisVariant(
        "nf150_h10_s420l360_aonly",
        "nf150_h10_s420l360",
        "model_axis_nonflat_weight_aonly",
        "logreg_nonflat_weight_c050_flat070_nonflat150",
        0.50,
        None,
        0.70,
        1.50,
        None,
        0.420,
        0.360,
        0.0,
        0.450,
        0.450,
        0.0,
        10,
        False,
        notes="non-flat sample weighting with hold10 to test real density without Tier B damage",
    ),
    ModelAxisVariant(
        "nf150_h10_s420l360_b045",
        "nf150_h10_s420l360",
        "model_axis_nonflat_weight_tier_b_comparison",
        "logreg_nonflat_weight_c050_flat070_nonflat150",
        0.50,
        None,
        0.70,
        1.50,
        None,
        0.420,
        0.360,
        0.0,
        0.450,
        0.450,
        0.0,
        10,
        True,
        notes="matched A-only/A+B comparison for Tier B disablement under non-flat weighted model",
    ),
    ModelAxisVariant(
        "nf150_h10_s400l300_aonly",
        "nf150_h10_s400l300",
        "model_axis_nonflat_weight_aonly",
        "logreg_nonflat_weight_c050_flat070_nonflat150",
        0.50,
        None,
        0.70,
        1.50,
        None,
        0.400,
        0.300,
        0.0,
        0.450,
        0.450,
        0.0,
        10,
        False,
        notes="stronger density pressure under non-flat weighted model and hold10",
    ),
    ModelAxisVariant(
        "recent24_h10_s400l300_aonly",
        "recent24_h10_s400l300",
        "model_axis_recent_train_aonly",
        "logreg_recent2024_balanced_c050",
        0.50,
        "balanced",
        None,
        None,
        "2024-01-01T00:00:00Z",
        0.400,
        0.300,
        0.0,
        0.450,
        0.450,
        0.0,
        10,
        False,
        notes="recent train-only logistic model to test session/weather drift without validation/OOS leakage",
    ),
)


def _configure_globals() -> None:
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


def _write_json(path: Path, payload: Mapping[str, Any]) -> None:
    target = reopen._project_path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str]) -> None:
    target = reopen._project_path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: row.get(column, "") for column in columns})


def _select_variants(
    *,
    selected_ids: Iterable[str] | None,
    selected_groups: Iterable[str] | None,
    max_variants: int | None,
) -> tuple[ModelAxisVariant, ...]:
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


def _split_values(values: Sequence[str]) -> tuple[str, ...]:
    parts: list[str] = []
    for value in values:
        parts.extend(part.strip() for part in str(value).split(",") if part.strip())
    return tuple(parts)


def _train_source_model(variant: ModelAxisVariant, *, force: bool) -> Path:
    model_root = RUN_ROOT / variant.variant_id / "source_model"
    model_path = model_root / "tier_a_model.joblib"
    meta_path = model_root / "source_model_manifest.json"
    if model_path.exists() and meta_path.exists() and not force:
        return model_path

    frame = pd.read_parquet(reopen._project_path(deep.logreg_scout.DEFAULT_MODEL_INPUT_PATH))
    feature_order = load_feature_order(reopen._project_path(deep.logreg_scout.DEFAULT_FEATURE_ORDER_PATH))
    validate_model_input_frame(frame, feature_order)
    train_frame = frame.loc[frame["split"].astype(str).eq("train")].copy()
    if variant.train_start_utc:
        train_start = pd.Timestamp(variant.train_start_utc)
        timestamps = pd.to_datetime(train_frame["timestamp"], utc=True)
        train_frame = train_frame.loc[timestamps >= train_start].copy()
    if train_frame.empty:
        raise RuntimeError(f"Training frame is empty for variant {variant.variant_id}")

    values = train_frame.loc[:, feature_order].to_numpy(dtype="float64", copy=False)
    labels = train_frame["label_class"].astype("int64").to_numpy()
    classifier = LogisticRegression(
        max_iter=3000,
        random_state=5601,
        solver="lbfgs",
        class_weight=variant.class_weight,
        C=float(variant.c_value),
    )
    model = Pipeline(steps=[("scaler", StandardScaler()), ("classifier", classifier)])
    fit_kwargs: dict[str, Any] = {}
    if variant.flat_sample_weight is not None and variant.nonflat_sample_weight is not None:
        fit_kwargs["classifier__sample_weight"] = np.where(
            labels == 1,
            float(variant.flat_sample_weight),
            float(variant.nonflat_sample_weight),
        )
    model.fit(values, labels, **fit_kwargs)

    target_root = reopen._project_path(model_root)
    target_root.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, reopen._project_path(model_path))
    manifest = {
        "variant_id": variant.variant_id,
        "model_spec_id": variant.model_spec_id,
        "model_family": "sklearn_logistic_regression_multiclass_model_axis",
        "source": "Stage56 run50K model-axis Tier A source model",
        "feature_order_path": deep.logreg_scout.DEFAULT_FEATURE_ORDER_PATH.as_posix(),
        "feature_count": len(feature_order),
        "training_rows": int(len(train_frame)),
        "train_start_utc": variant.train_start_utc,
        "c_value": float(variant.c_value),
        "class_weight": variant.class_weight,
        "flat_sample_weight": variant.flat_sample_weight,
        "nonflat_sample_weight": variant.nonflat_sample_weight,
        "class_counts": {
            str(key): int(value)
            for key, value in train_frame["label_class"].astype("int64").value_counts().sort_index().items()
        },
        "model_path": model_path.as_posix(),
        "model_sha256": sha256_file(model_path),
        "created_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "boundary": "stage56_model_axis_research_only_no_operating_claim",
    }
    _write_json(meta_path, manifest)
    return model_path


def _run_variant(
    variant: ModelAxisVariant,
    *,
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
    if summary_path.exists() and not force:
        summary = deep._read_json(summary_path)
        return {
            "status": "skipped_existing",
            "variant_id": variant.variant_id,
            "run_id": variant.to_deep_variant().run_id,
            "summary_path": summary_path.as_posix(),
            "external_verification_status": summary.get("external_verification_status"),
        }

    source_model_path = _train_source_model(variant, force=force)
    reopen._project_path(run_output_root / "reports").mkdir(parents=True, exist_ok=True)
    deep_variant = variant.to_deep_variant()
    deep._configure_stage56_identity(deep_variant, run_output_root)
    tier_a_rule = deep.logreg_scout.threshold_rule_from_values(
        threshold_id=deep_variant.tier_a_threshold_id,
        short_threshold=variant.tier_a_short_threshold,
        long_threshold=variant.tier_a_long_threshold,
        min_margin=variant.tier_a_min_margin,
    )
    tier_b_rule = deep.logreg_scout.threshold_rule_from_values(
        threshold_id=deep_variant.tier_b_threshold_id,
        short_threshold=variant.tier_b_short_threshold,
        long_threshold=variant.tier_b_long_threshold,
        min_margin=variant.tier_b_min_margin,
    )
    result = deep.logreg_scout.run_stage10_logreg_mt5_scout(
        model_input_path=deep.logreg_scout.DEFAULT_MODEL_INPUT_PATH,
        feature_order_path=deep.logreg_scout.DEFAULT_FEATURE_ORDER_PATH,
        tier_b_model_input_path=deep.logreg_scout.DEFAULT_TIER_B_MODEL_INPUT_PATH,
        tier_b_feature_order_path=deep.logreg_scout.DEFAULT_TIER_B_FEATURE_ORDER_PATH,
        raw_root=deep.logreg_scout.DEFAULT_RAW_ROOT,
        training_summary_path=deep.logreg_scout.DEFAULT_TRAINING_SUMMARY_PATH,
        stage07_model_path=source_model_path,
        run_output_root=run_output_root,
        common_files_root=common_files_root,
        terminal_data_root=terminal_data_root,
        tester_profile_root=tester_profile_root,
        max_hold_bars=variant.max_hold_bars,
        tier_a_threshold_rule=tier_a_rule,
        tier_b_threshold_rule=tier_b_rule,
        routed_fallback_enabled=variant.routed_fallback_enabled,
        session_slice_id=variant.session_slice_id,
        tier_b_fallback_allowed_subtypes=variant.tier_b_allowed_subtypes or None,
        attempt_mt5=attempt_mt5,
        terminal_path=terminal_path,
        metaeditor_path=metaeditor_path,
        reentry_cooldown_bars=variant.reentry_cooldown_bars,
        entry_transition_only=variant.entry_transition_only,
        entry_transition_rearm_min_confidence_delta=variant.entry_transition_rearm_min_confidence_delta,
        side_filter_id=variant.side_filter_id,
        side_filter_enabled=variant.side_filter_enabled,
        tier_a_side_filter_feature_index=variant.tier_a_side_filter_feature_index,
        tier_b_side_filter_feature_index=variant.tier_b_side_filter_feature_index,
        block_short_feature_range=variant.block_short_feature_range,
        block_short_feature_min=variant.block_short_feature_min,
        block_short_feature_max=variant.block_short_feature_max,
        block_long_feature_range=variant.block_long_feature_range,
        block_long_feature_min=variant.block_long_feature_min,
        block_long_feature_max=variant.block_long_feature_max,
    )
    result["variant_id"] = variant.variant_id
    result["variant_spec"] = {
        "group": variant.group,
        "base_id": variant.base_id,
        "model_spec_id": variant.model_spec_id,
        "source_model_path": source_model_path.as_posix(),
        "routed_fallback_enabled": variant.routed_fallback_enabled,
        "reentry_cooldown_bars": variant.reentry_cooldown_bars,
        "entry_transition_only": variant.entry_transition_only,
        "entry_transition_rearm_min_confidence_delta": variant.entry_transition_rearm_min_confidence_delta,
        "tier_a_short_threshold": variant.tier_a_short_threshold,
        "tier_a_long_threshold": variant.tier_a_long_threshold,
        "tier_a_min_margin": variant.tier_a_min_margin,
        "tier_b_short_threshold": variant.tier_b_short_threshold,
        "tier_b_long_threshold": variant.tier_b_long_threshold,
        "tier_b_min_margin": variant.tier_b_min_margin,
        "max_hold_bars": variant.max_hold_bars,
        "side_filter_id": variant.side_filter_id,
        "side_filter_enabled": variant.side_filter_enabled,
        "tier_a_side_filter_feature_index": variant.tier_a_side_filter_feature_index,
        "tier_b_side_filter_feature_index": variant.tier_b_side_filter_feature_index,
        "block_short_feature_range": variant.block_short_feature_range,
        "block_short_feature_min": variant.block_short_feature_min,
        "block_short_feature_max": variant.block_short_feature_max,
        "block_long_feature_range": variant.block_long_feature_range,
        "block_long_feature_min": variant.block_long_feature_min,
        "block_long_feature_max": variant.block_long_feature_max,
    }
    return result


def _augment_rows(rows: list[dict[str, Any]], variants: Sequence[ModelAxisVariant]) -> None:
    reopen._augment_rows(rows, variants)
    by_id = {variant.variant_id: variant for variant in variants}
    for row in rows:
        variant = by_id.get(str(row.get("variant_id") or ""))
        row["model_spec_id"] = "" if variant is None else variant.model_spec_id
        row["train_start_utc"] = "" if variant is None or variant.train_start_utc is None else variant.train_start_utc
        row["class_weight"] = "" if variant is None or variant.class_weight is None else variant.class_weight
        row["flat_sample_weight"] = "" if variant is None or variant.flat_sample_weight is None else variant.flat_sample_weight
        row["nonflat_sample_weight"] = "" if variant is None or variant.nonflat_sample_weight is None else variant.nonflat_sample_weight
        row["c_value"] = "" if variant is None else variant.c_value
        row["reentry_cooldown_bars"] = "" if variant is None else variant.reentry_cooldown_bars
        row["entry_transition_only"] = "" if variant is None else variant.entry_transition_only
        row["entry_transition_rearm_min_confidence_delta"] = "" if variant is None else variant.entry_transition_rearm_min_confidence_delta
        row["side_filter_id"] = "" if variant is None or variant.side_filter_id is None else variant.side_filter_id
        row["side_filter_enabled"] = "" if variant is None else variant.side_filter_enabled
        row["tier_a_side_filter_feature_index"] = "" if variant is None else variant.tier_a_side_filter_feature_index
        row["tier_b_side_filter_feature_index"] = "" if variant is None else variant.tier_b_side_filter_feature_index
        row["block_short_feature_range"] = "" if variant is None else variant.block_short_feature_range
        row["block_short_feature_min"] = "" if variant is None else variant.block_short_feature_min
        row["block_short_feature_max"] = "" if variant is None else variant.block_short_feature_max
        row["block_long_feature_range"] = "" if variant is None else variant.block_long_feature_range
        row["block_long_feature_min"] = "" if variant is None else variant.block_long_feature_min
        row["block_long_feature_max"] = "" if variant is None else variant.block_long_feature_max


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Stage56 model-axis MT5 density repair batch.")
    parser.add_argument("--attempt-mt5", action="store_true")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--continue-on-error", action="store_true", default=True)
    parser.add_argument("--variant-id", action="append", default=[])
    parser.add_argument("--groups", action="append", default=[])
    parser.add_argument("--max-variants", type=int)
    parser.add_argument("--cost-stress-per-trade", type=float, default=0.50)
    parser.add_argument("--common-files-root", default=str(deep.logreg_scout.DEFAULT_COMMON_FILES_ROOT))
    parser.add_argument("--terminal-data-root", default=str(deep.logreg_scout.DEFAULT_TERMINAL_DATA_ROOT))
    parser.add_argument("--tester-profile-root", default=str(deep.logreg_scout.DEFAULT_TESTER_PROFILE_ROOT))
    parser.add_argument("--terminal-path", default=r"C:\Program Files\MetaTrader 5\terminal64.exe")
    parser.add_argument("--metaeditor-path", default=r"C:\Program Files\MetaTrader 5\MetaEditor64.exe")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    _configure_globals()
    args = parse_args(argv)
    variants = _select_variants(
        selected_ids=_split_values(args.variant_id),
        selected_groups=_split_values(args.groups),
        max_variants=args.max_variants,
    )
    deep_variants = tuple(variant.to_deep_variant() for variant in variants)
    results: list[dict[str, Any]] = []
    for variant in variants:
        try:
            result = _run_variant(
                variant,
                attempt_mt5=bool(args.attempt_mt5),
                common_files_root=Path(args.common_files_root),
                terminal_data_root=Path(args.terminal_data_root),
                tester_profile_root=Path(args.tester_profile_root),
                terminal_path=Path(args.terminal_path),
                metaeditor_path=Path(args.metaeditor_path),
                force=bool(args.force),
            )
        except Exception as exc:  # pragma: no cover - long MT5 batches must keep evidence.
            error_path = RUN_ROOT / variant.variant_id / "error.json"
            _write_json(
                error_path,
                {
                    "variant_id": variant.variant_id,
                    "run_id": variant.to_deep_variant().run_id,
                    "error": str(exc),
                    "traceback": traceback.format_exc(),
                    "created_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
                },
            )
            result = {
                "status": "error",
                "variant_id": variant.variant_id,
                "run_id": variant.to_deep_variant().run_id,
                "external_verification_status": "blocked",
                "error": str(exc),
                "error_path": error_path.as_posix(),
            }
            if not args.continue_on_error:
                results.append(result)
                break
        results.append(dict(result))

    rows = deep._summary_rows(results, deep_variants)
    _augment_rows(rows, variants)
    market_data = MarketData.load(REPO_ROOT)
    reference_audits, reference_capture = reopen._reference_capture_by_split(
        market_data,
        float(args.cost_stress_per_trade),
    )
    audit_rows = reference_audits + reopen._audit_rows(
        rows,
        market_data=market_data,
        cost_stress_per_trade=float(args.cost_stress_per_trade),
        reference_capture=reference_capture,
    )
    final_read = reopen._selected_read(rows, audit_rows)
    _write_csv(RESULTS_CSV_PATH, rows, SUMMARY_COLUMNS)
    _write_csv(AUDIT_CSV_PATH, audit_rows, reopen.AUDIT_COLUMNS)
    reopen._write_report(rows, audit_rows, final_read, attempt_mt5=bool(args.attempt_mt5))
    reopen._write_progress_log(rows, audit_rows, final_read)
    ledger_payload = reopen._write_parent_rows(rows, final_read)
    reopen._write_aggregate_summary(results, rows, audit_rows, final_read, ledger_payload)
    print(
        json.dumps(
            {
                "status": "ok",
                "run_id": PARENT_RUN_ID,
                "selected_research_baseline": final_read.get("selected_research_baseline") or "none",
                "final_read": final_read.get("stage56_judgment"),
                "stage56_remains_open": bool(final_read.get("stage56_remains_open")),
                "results_csv_path": RESULTS_CSV_PATH.as_posix(),
                "audit_csv_path": AUDIT_CSV_PATH.as_posix(),
                "aggregate_summary_path": AGGREGATE_SUMMARY_PATH.as_posix(),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


SUMMARY_COLUMNS = tuple(
    list(reopen.SUMMARY_COLUMNS[:-4])
    + [
        "model_spec_id",
        "train_start_utc",
        "class_weight",
        "flat_sample_weight",
        "nonflat_sample_weight",
        "c_value",
        "reentry_cooldown_bars",
        "entry_transition_only",
        "entry_transition_rearm_min_confidence_delta",
        "side_filter_id",
        "side_filter_enabled",
        "tier_a_side_filter_feature_index",
        "tier_b_side_filter_feature_index",
        "block_short_feature_range",
        "block_short_feature_min",
        "block_short_feature_max",
        "block_long_feature_range",
        "block_long_feature_min",
        "block_long_feature_max",
    ]
    + list(reopen.SUMMARY_COLUMNS[-4:])
)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
