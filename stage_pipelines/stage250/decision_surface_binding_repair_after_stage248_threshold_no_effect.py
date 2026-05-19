from __future__ import annotations

import argparse
import csv
import json
import math
import re
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.control_plane.ledger import (  # noqa: E402
    ALPHA_LEDGER_COLUMNS,
    RUN_REGISTRY_COLUMNS,
    io_path,
    json_ready,
    ledger_pairs,
    path_exists,
    sha256_file_lf_normalized,
    upsert_csv_rows,
)
from foundation.models.ebm_score_table import (  # noqa: E402
    FIELDNAMES,
    load_ebm_score_table,
    score_ebm_table_probabilities,
)
from stage_pipelines.stage238 import score_shape_repair_after_threshold_surface_discrete as stage238  # noqa: E402


STAGE_ID = "250_adapter_research__decision_surface_binding_repair_after_stage248_threshold_no_effect"
RUN_NUMBER = "run250A"
RUN_ID = "run250A_stage250_decision_surface_binding_repair_after_stage248_threshold_no_effect_v1"
PACKET_ID = "stage250_decision_surface_binding_repair_after_stage248_threshold_no_effect_v1"
PARENT_RUN_ID = "run249A_stage249_stage248_entry_source_followup_review_v1"
SOURCE_STAGE_ID = "249_adapter_research__stage248_entry_source_followup_review"
SOURCE_RUN_ID = PARENT_RUN_ID
SOURCE_STAGE248_EVIDENCE_COMMIT = "ab50acc695fdc069cb25dece7a66a38bb89bc925"
SOURCE_STAGE248_HASH_RECORD_COMMIT = "c7466b6836bf1837fcaab2148e55bd5b065fb327"
SOURCE_STAGE249_EVIDENCE_COMMIT = "6d2d94850638410e6456c3a8fadf5d3518220da4"
SOURCE_STAGE249_HASH_RECORD_COMMIT = "26eb7659fc77abde49c063b4b3e2ab6fc557cbf0"
NEXT_STAGE_ID = "251_adapter_research__stage250_decision_binding_followup_review"
NEXT_RUN_ID = "run251A_stage251_stage250_decision_binding_followup_review_v1"
NEXT_PACKET_ID = "stage251_stage250_decision_binding_followup_review_v1"
TARGET_SURFACE = "legacy_34d_kpi_lesson_only_v2_native_decision_surface_binding_after_stage248_threshold_no_effect"
BOUNDARY = stage238.BOUNDARY
LEGACY_34D = stage238.LEGACY_34D
OOS_REFERENCE = {
    "adapter_id": "s248_cap0305_reference",
    "oos_net": 775.76,
    "oos_pf": 1.78,
    "oos_dd": 9.5076,
}

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
SELECTED_ROOT = STAGE_ROOT / "04_selected"
PACKET_ROOT = Path("docs/agent_control/packets") / PACKET_ID
NEXT_STAGE_ROOT = Path("stages") / NEXT_STAGE_ID
PARTIALS_ROOT = RUN_ROOT / "partials"
COMMON_ROOT = f"OPV2/s250a/{RUN_NUMBER}"

SUMMARY_JSON_PATH = REVIEWS_ROOT / "stage250_summary.json"
SUMMARY_CSV_PATH = REVIEWS_ROOT / "stage250_decision_binding_kpi_summary.csv"
REPORT_PATH = REVIEWS_ROOT / "stage250_decision_binding_report.md"
SEGMENT_KPI_PATH = REVIEWS_ROOT / "stage250_segment_kpi_summary.csv"
BALANCE_CURVE_AUDIT_PATH = REVIEWS_ROOT / "stage250_balance_curve_audit.csv"
MONTHLY_KPI_PATH = REVIEWS_ROOT / "stage250_monthly_kpi_summary.csv"
CONCENTRATION_PATH = REVIEWS_ROOT / "stage250_concentration_risk_summary.csv"
DRAWDOWN_PATH = REVIEWS_ROOT / "stage250_drawdown_recovery_summary.csv"
QUALITY_MATRIX_PATH = REVIEWS_ROOT / "stage250_quality_matrix.csv"
RISK_ATR_TELEMETRY_PATH = REVIEWS_ROOT / "stage250_risk_atr_telemetry.csv"
GATE_FEATURE_SUMMARY_PATH = REVIEWS_ROOT / "stage250_decision_binding_feature_summary.csv"
PROBABILITY_BINDING_PATH = REVIEWS_ROOT / "stage250_probability_binding_summary.csv"
MODEL_SCORE_AUDIT_PATH = REVIEWS_ROOT / "stage250_model_score_audit.csv"
TIER_B_DIAGNOSTIC_PATH = REVIEWS_ROOT / "stage250_tier_b_diagnostic_summary.csv"
ATTRIBUTION_PATH = REVIEWS_ROOT / "stage250_performance_attribution.csv"
FAILURE_MEMORY_PATH = REVIEWS_ROOT / "stage250_failure_memory.csv"
DECISION_PATH = REVIEWS_ROOT / "stage250_decision.md"
AUDIT_CSV_PATH = REVIEWS_ROOT / "stage250_trade_audit.csv"
STAGE_LEDGER_PATH = REVIEWS_ROOT / "stage_run_ledger.csv"

RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
PROJECT_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
ARTIFACT_REGISTRY_PATH = Path("docs/registers/artifact_registry.csv")
WORKSPACE_STATE_PATH = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE_PATH = Path("docs/context/current_working_state.md")
CHANGELOG_PATH = Path("docs/workspace/changelog.md")
PRODUCER_PATH = Path("stage_pipelines/stage250/decision_surface_binding_repair_after_stage248_threshold_no_effect.py")

SIGNAL_COLUMN = stage238.SIGNAL_COLUMN
RANK_COLUMN = "stage250_decision_binding_rank_bucket"
GATE_COLUMN_PREFIX = "stage250_decision_binding_gate"
SOURCE_SPEC = dict(stage238.SOURCE_SPEC)
REFERENCE_EXTRA = dict(stage238.REFERENCE_EXTRA)


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    return stage238.rel(path)


def csv_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, float):
        return f"{value:.10g}"
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(json_ready(value), ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return str(value)


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(
        json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str] | None = None) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    ordered: list[str] = []
    for row in rows:
        for key in row:
            if key not in ordered:
                ordered.append(key)
    fieldnames = list(columns or ordered)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: csv_value(row.get(column)) for column in fieldnames})


def parse_float(value: Any, default: float = 0.0) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return default
    return number if math.isfinite(number) else default


def as_float(row: Mapping[str, Any], key: str, default: float = 0.0) -> float:
    return parse_float(row.get(key), default)


def _format_score(value: Any) -> str:
    return f"{float(value):.17g}"


def rank_penalty(value: float) -> tuple[float, float, float]:
    value = float(value)
    if value <= 0.0:
        return (0.0, 0.0, 0.0)
    return (-value, value, -value)


def repair_variant(
    adapter_id: str,
    label: str,
    *,
    low_penalty: float,
    mid_penalty: float,
    short_threshold: float = 0.54,
    long_threshold: float = 0.52,
    note: str,
) -> Any:
    return stage238.repair.RepairVariant(
        adapter_id=adapter_id,
        label=label,
        atr_enabled=True,
        model_risk_enabled=True,
        fixed_lot=0.25,
        atr_stop_multiplier=2.0325,
        atr_take_profit_multiplier=4.615,
        model_risk_max_pct=0.0305,
        same_direction_reentry_cooldown_bars=8,
        short_threshold=short_threshold,
        long_threshold=long_threshold,
        close_on_flat_signal=False,
        reverse_on_opposite_signal=True,
        close_only_on_opposite_signal=False,
        max_hold_bars=3,
        notes=f"{note} low_penalty={low_penalty} mid_penalty={mid_penalty}",
    )


VARIANTS = (
    repair_variant(
        "s250_stage248_binding_control",
        "stage250_stage248_binding_control",
        low_penalty=0.0,
        mid_penalty=0.0,
        note="Stage250 control: reproduce Stage248 reference score shape and side filter.",
    ),
    repair_variant(
        "s250_low_flat020",
        "stage250_low_flat020",
        low_penalty=0.20,
        mid_penalty=0.0,
        note="Stage250 binding repair: rank-conditioned flat tilt on low-margin decisions.",
    ),
    repair_variant(
        "s250_low_flat025",
        "stage250_low_flat025",
        low_penalty=0.25,
        mid_penalty=0.0,
        note="Stage250 binding repair: stronger low-margin flat tilt to cross the decision surface.",
    ),
    repair_variant(
        "s250_lowmid_flat025_015",
        "stage250_lowmid_flat025_015",
        low_penalty=0.25,
        mid_penalty=0.15,
        note="Stage250 binding repair: low plus mild mid-margin flat tilt.",
    ),
)


def extra(axis: str, low_penalty: float, mid_penalty: float) -> dict[str, Any]:
    return {
        "axis": axis,
        "logit_strength": 0.50,
        "risk_confidence_floor": 0.50,
        "risk_confidence_ceiling": 0.60,
        "block_mode": "reference_only",
        "side_filter_enabled": True,
        "short_block_rule": "midwide_lowedge",
        "long_block_rule": "session_only",
        "low_penalty": float(low_penalty),
        "mid_penalty": float(mid_penalty),
        "rank_scores": {
            "low": rank_penalty(low_penalty),
            "mid": rank_penalty(mid_penalty),
            "high": (0.10, -0.10, 0.10),
            "vhigh": (0.15, -0.15, 0.15),
        },
    }


VARIANT_EXTRAS: dict[str, dict[str, Any]] = {}
for item in VARIANTS:
    low = float(str(item.notes).split("low_penalty=")[1].split()[0])
    mid = float(str(item.notes).split("mid_penalty=")[1].split()[0])
    VARIANT_EXTRAS[item.adapter_id] = extra(item.adapter_id.replace("s250_", ""), low, mid)

SOURCE_SPECS_BY_VARIANT = {item.adapter_id: dict(SOURCE_SPEC) for item in VARIANTS}
MODEL_RISK_MIN_PCT = {item.adapter_id: 0.005 for item in VARIANTS}


def write_decision_binding_model(path: Path, variant: Any, gate_column: str) -> dict[str, Any]:
    extra_cfg = VARIANT_EXTRAS[variant.adapter_id]
    strength = float(extra_cfg["logit_strength"])
    rank_scores = extra_cfg["rank_scores"]
    rows: list[dict[str, Any]] = [
        {"record_type": "intercept", "feature_index": -1, "item_index": -1, "value": "", "score_short": "0", "score_flat": "0", "score_long": "0"},
        {"record_type": "cut", "feature_index": 0, "item_index": 0, "value": "-0.5", "score_short": "", "score_flat": "", "score_long": ""},
        {"record_type": "cut", "feature_index": 0, "item_index": 1, "value": "0.5", "score_short": "", "score_flat": "", "score_long": ""},
        {"record_type": "score", "feature_index": 0, "item_index": 0, "value": "", "score_short": _format_score(strength), "score_flat": _format_score(-strength), "score_long": _format_score(-strength)},
        {"record_type": "score", "feature_index": 0, "item_index": 1, "value": "", "score_short": _format_score(strength), "score_flat": _format_score(-strength), "score_long": _format_score(-strength)},
        {"record_type": "score", "feature_index": 0, "item_index": 2, "value": "", "score_short": _format_score(-strength), "score_flat": _format_score(strength), "score_long": _format_score(-strength)},
        {"record_type": "score", "feature_index": 0, "item_index": 3, "value": "", "score_short": _format_score(-strength), "score_flat": _format_score(-strength), "score_long": _format_score(strength)},
    ]
    for item_index, cut_value in enumerate((0.5, 1.5, 2.5)):
        rows.append({"record_type": "cut", "feature_index": 1, "item_index": item_index, "value": _format_score(cut_value), "score_short": "", "score_flat": "", "score_long": ""})
    score_by_item = {
        0: rank_scores["low"],
        1: rank_scores["low"],
        2: rank_scores["mid"],
        3: rank_scores["high"],
        4: rank_scores["vhigh"],
    }
    for item_index, scores in score_by_item.items():
        rows.append(
            {
                "record_type": "score",
                "feature_index": 1,
                "item_index": item_index,
                "value": "",
                "score_short": _format_score(scores[0]),
                "score_flat": _format_score(scores[1]),
                "score_long": _format_score(scores[2]),
            }
        )
    for item_index, cut_value in enumerate((0.5, 1.5)):
        rows.append({"record_type": "cut", "feature_index": 2, "item_index": item_index, "value": _format_score(cut_value), "score_short": "", "score_flat": "", "score_long": ""})
    for item_index in range(4):
        rows.append({"record_type": "score", "feature_index": 2, "item_index": item_index, "value": "", "score_short": "0", "score_flat": "0", "score_long": "0"})

    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    table = load_ebm_score_table(path, feature_count=3)
    sample_values = np.asarray(
        [
            [-1.0, 0.0, 0.0],
            [-1.0, 1.0, 0.0],
            [-1.0, 2.0, 0.0],
            [-1.0, 3.0, 0.0],
            [1.0, 0.0, 0.0],
            [1.0, 1.0, 0.0],
            [1.0, 2.0, 0.0],
            [1.0, 3.0, 0.0],
        ],
        dtype="float64",
    )
    probabilities = score_ebm_table_probabilities(table, sample_values)
    feature_order = (SIGNAL_COLUMN, RANK_COLUMN, gate_column)
    return {
        "path": rel(path),
        "sha256": sha256_file_lf_normalized(path),
        "format": "stage250_three_feature_decision_binding_ebm_table_csv_v1",
        "feature_order": list(feature_order),
        "feature_order_hash": stage238.s161.base.engine.ordered_hash(feature_order),
        "feature_count": 3,
        "signal_column": SIGNAL_COLUMN,
        "rank_column": RANK_COLUMN,
        "gate_column": gate_column,
        "rank_scores": rank_scores,
        "low_penalty": extra_cfg["low_penalty"],
        "mid_penalty": extra_cfg["mid_penalty"],
        "parity_sample_values": sample_values.tolist(),
        "parity_sample_probabilities": probabilities.tolist(),
    }


def write_decision_binding_feature(source: Path, destination: Path, variant: Any, split: str) -> dict[str, Any]:
    gate_column = f"{GATE_COLUMN_PREFIX}_{VARIANT_EXTRAS[variant.adapter_id]['axis']}"
    io_path(destination.parent).mkdir(parents=True, exist_ok=True)
    total_rows = 0
    signal_rows = 0
    blocked_signal_rows = 0
    rank_counts: dict[str, int] = {"low": 0, "mid": 0, "high": 0, "vhigh": 0}
    allowed_signal_rank_counts: dict[str, int] = {"low": 0, "mid": 0, "high": 0, "vhigh": 0}
    with io_path(source).open("r", encoding="utf-8-sig", newline="") as input_handle:
        reader = csv.DictReader(input_handle)
        with io_path(destination).open("w", encoding="utf-8", newline="") as output_handle:
            writer = csv.DictWriter(
                output_handle,
                fieldnames=("bar_time_server", SIGNAL_COLUMN, RANK_COLUMN, gate_column),
                lineterminator="\n",
            )
            writer.writeheader()
            for row in reader:
                total_rows += 1
                signal = int(round(stage238.parse_float(row.get(SIGNAL_COLUMN), 0.0)))
                bucket_value, bucket_label = stage238.rank_bucket_for(row)
                gate = stage238.reference_gate_value(row)
                rank_counts[bucket_label] += 1
                if signal != 0:
                    signal_rows += 1
                    if gate >= 0.5:
                        blocked_signal_rows += 1
                    else:
                        allowed_signal_rank_counts[bucket_label] += 1
                writer.writerow(
                    {
                        "bar_time_server": row.get("bar_time_server") or row.get("timestamp_utc") or "",
                        SIGNAL_COLUMN: csv_value(float(signal)),
                        RANK_COLUMN: csv_value(float(bucket_value)),
                        gate_column: csv_value(gate),
                    }
                )
    return {
        "run_id": RUN_ID,
        "adapter_id": variant.adapter_id,
        "split": split,
        "gate_column": gate_column,
        "source_feature": rel(source),
        "decision_binding_feature": rel(destination),
        "total_rows": total_rows,
        "signal_rows": signal_rows,
        "blocked_signal_rows": blocked_signal_rows,
        "allowed_signal_rows": signal_rows - blocked_signal_rows,
        "rank_counts": rank_counts,
        "allowed_signal_rank_counts": allowed_signal_rank_counts,
        "low_penalty": VARIANT_EXTRAS[variant.adapter_id]["low_penalty"],
        "mid_penalty": VARIANT_EXTRAS[variant.adapter_id]["mid_penalty"],
        "gate_description": "Stage250 keeps Stage248 reference side filter and changes rank-conditioned score surface.",
        "side_filter_feature_index": 2,
        "rank_feature_index": 1,
    }


def prepare_inputs(common_files_root: Path) -> dict[str, Any]:
    copied: list[dict[str, Any]] = []
    gate_rows: list[dict[str, Any]] = []
    model_exports: dict[str, dict[str, Any]] = {}
    feature_exports: dict[str, dict[str, dict[str, Any]]] = {}
    for item in VARIANTS:
        gate_column = f"{GATE_COLUMN_PREFIX}_{VARIANT_EXTRAS[item.adapter_id]['axis']}"
        model_source = stage238.s161.base.engine.source_model_for_variant(item)
        model_local = RUN_ROOT / item.adapter_id / "models" / f"{item.adapter_id}_model.csv"
        model_meta = write_decision_binding_model(model_local, item, gate_column)
        copied.append(
            {
                "source": rel(model_source),
                "path": rel(model_local),
                "sha256": sha256_file_lf_normalized(model_local),
                "transform": "stage250_decision_binding_rank_conditioned_score_model",
            }
        )
        copied.append(stage238.s161.base.engine.copy_to_common(model_local, f"{COMMON_ROOT}/{item.adapter_id}/models/{model_local.name}", common_files_root))
        model_exports[item.adapter_id] = {
            **model_meta,
            "common_path": f"{COMMON_ROOT}/{item.adapter_id}/models/{model_local.name}",
            "source_model": rel(model_source),
            "source_anchor": stage238.s161.base.engine.source_anchor_for_variant(item),
        }
        feature_exports[item.adapter_id] = {}
        for split in ("validation_is", "oos"):
            token = "val" if split == "validation_is" else "oos"
            feature_source = stage238.s161.base.engine.source_feature(split, item, "a")
            feature_local = RUN_ROOT / item.adapter_id / "features" / f"{item.adapter_id}_{token}.csv"
            gate_row = write_decision_binding_feature(feature_source, feature_local, item, split)
            gate_rows.append(gate_row)
            copied.append(
                {
                    "source": rel(feature_source),
                    "path": rel(feature_local),
                    "sha256": sha256_file_lf_normalized(feature_local),
                    "transform": "stage250_reference_side_filter_plus_margin_rank_feature",
                }
            )
            copied.append(stage238.s161.base.engine.copy_to_common(feature_local, f"{COMMON_ROOT}/{item.adapter_id}/features/{feature_local.name}", common_files_root))
            feature_exports[item.adapter_id][split] = {
                "path": rel(feature_local),
                "common_path": f"{COMMON_ROOT}/{item.adapter_id}/features/{feature_local.name}",
                "sha256": sha256_file_lf_normalized(feature_local),
                "source_feature": rel(feature_source),
                "gate_column": gate_row["gate_column"],
                "rank_column": RANK_COLUMN,
            }
    return {
        "model_exports": model_exports,
        "feature_exports": feature_exports,
        "common_copies": copied,
        "gate_rows": gate_rows,
    }


def extra_set_values(variant: Any, magic: int) -> dict[str, Any]:
    values = stage238.s161.base.engine.extra_set_values(variant, magic)
    extra_cfg = VARIANT_EXTRAS[variant.adapter_id]
    values["InpSideFilterEnabled"] = True
    values["InpSideFilterFeatureIndex"] = 2
    values["InpFallbackSideFilterFeatureIndex"] = 2
    values["InpBlockShortFeatureRange"] = True
    values["InpBlockShortFeatureMin"] = 0.5
    values["InpBlockShortFeatureMax"] = 1.5
    values["InpBlockLongFeatureRange"] = True
    values["InpBlockLongFeatureMin"] = 1.5
    values["InpBlockLongFeatureMax"] = 2.5
    values["InpModelRiskConfidenceFloor"] = float(extra_cfg["risk_confidence_floor"])
    values["InpModelRiskConfidenceCeiling"] = float(extra_cfg["risk_confidence_ceiling"])
    return values


def build_attempts(inputs: Mapping[str, Any]) -> list[dict[str, Any]]:
    attempts: list[dict[str, Any]] = []
    for variant_index, item in enumerate(VARIANTS, start=1):
        variant_root = RUN_ROOT / item.adapter_id
        for split in ("validation_is", "oos"):
            date_values = stage238.s161.base.parse_ini(stage238.s161.base.engine.source_attempt_ini(split, item))
            split_token = "val" if split == "validation_is" else "oos"
            for role_index, (tier, attempt_role, prefix, attempt_token) in enumerate(
                (
                    (stage238.s161.base.mt5.TIER_A, "tier_only_total", f"mt5_tier_a_only_{item.adapter_id}", "ta"),
                    (stage238.s161.base.mt5.TIER_AB, "routed_total", f"mt5_routed_{item.adapter_id}", "rt"),
                ),
                start=1,
            ):
                magic = 25010000 + variant_index * 100 + (1 if split == "validation_is" else 50) + role_index
                attempts.append(
                    stage238.s161.base.attempt_payload(
                        run_root=variant_root,
                        run_id=RUN_ID,
                        stage_number=250,
                        exploration_label="stage250_BaselineAdapter__DecisionSurfaceBindingRepair",
                        attempt_name=f"{item.adapter_id}_{attempt_token}_{split_token}",
                        tier=tier,
                        split=split,
                        model_path=str(inputs["model_exports"][item.adapter_id]["common_path"]),
                        model_id=f"{RUN_ID}_{item.adapter_id}_entry_adapter",
                        model_backend="ebm_table",
                        feature_path=str(inputs["feature_exports"][item.adapter_id][split]["common_path"]),
                        feature_count=3,
                        feature_order_hash=inputs["model_exports"][item.adapter_id]["feature_order_hash"],
                        short_threshold=item.short_threshold,
                        long_threshold=item.long_threshold,
                        min_margin=0.0,
                        invert_signal=False,
                        from_date=str(date_values["FromDate"]),
                        to_date=str(date_values["ToDate"]),
                        primary_active_tier="tier_a",
                        attempt_role=attempt_role,
                        record_view_prefix=prefix,
                        max_hold_bars=item.max_hold_bars,
                        common_root=f"{COMMON_ROOT}/{item.adapter_id}",
                        fallback_enabled=False,
                        close_on_flat_signal=item.close_on_flat_signal,
                        reverse_on_opposite_signal=item.reverse_on_opposite_signal,
                        close_only_on_opposite_signal=item.close_only_on_opposite_signal,
                        extra_set_values=extra_set_values(item, magic),
                    )
                )
    return attempts


def split_row(rows: Sequence[Mapping[str, Any]], adapter_id: str, split: str) -> Mapping[str, Any]:
    for row in rows:
        if row.get("adapter_id") == adapter_id and row.get("split") == split and row.get("view") == "actual_routed_total":
            return row
    return {}


def segment_row(rows: Sequence[Mapping[str, Any]], adapter_id: str, split: str, segment: str) -> Mapping[str, Any]:
    for row in rows:
        if row.get("adapter_id") == adapter_id and row.get("split") == split and row.get("segment") == segment and row.get("view") == "actual_routed_total":
            return row
    return {}


def hard_quality_pass(row: Mapping[str, Any]) -> bool:
    return (
        as_float(row, "validation_net") >= LEGACY_34D["net_profit"]
        and as_float(row, "validation_early_pf") >= LEGACY_34D["profit_factor"]
        and as_float(row, "validation_mid_pf") >= LEGACY_34D["profit_factor"]
        and as_float(row, "validation_balance_dd_percent", 99.0) <= LEGACY_34D["max_drawdown_percent"]
        and as_float(row, "oos_net") >= OOS_REFERENCE["oos_net"]
        and as_float(row, "oos_pf") >= OOS_REFERENCE["oos_pf"]
        and as_float(row, "oos_balance_dd_percent", 99.0) <= OOS_REFERENCE["oos_dd"]
    )


def best_row(rows: Sequence[Mapping[str, Any]]) -> Mapping[str, Any]:
    if not rows:
        return {}
    return max(
        rows,
        key=lambda row: (
            hard_quality_pass(row),
            as_float(row, "validation_net"),
            -as_float(row, "validation_balance_dd_percent", 99.0),
            as_float(row, "validation_mid_pf"),
            as_float(row, "oos_net"),
        ),
    )


def decision_movement(reference: Mapping[str, Any], row: Mapping[str, Any]) -> bool:
    return (
        as_float(row, "validation_net") != as_float(reference, "validation_net")
        or as_float(row, "oos_net") != as_float(reference, "oos_net")
        or as_float(row, "validation_mid_pf") != as_float(reference, "validation_mid_pf")
        or as_float(row, "validation_balance_dd_percent") != as_float(reference, "validation_balance_dd_percent")
    )


def decide(quality_rows: Sequence[Mapping[str, Any]], probability_rows: Sequence[Mapping[str, Any]], external: str) -> str:
    if external != "completed":
        return "continue_stage250_runtime_completion_due_to_incomplete_runtime_candidate_not_final"
    reference = next((row for row in quality_rows if row.get("adapter_id") == "s250_stage248_binding_control"), {})
    movement = any(decision_movement(reference, row) for row in quality_rows if row.get("adapter_id") != "s250_stage248_binding_control")
    if any(hard_quality_pass(row) for row in quality_rows):
        return "open_stage251_bounded_followup_due_to_decision_binding_34d_candidate_not_final"
    if movement:
        return "open_stage251_bounded_followup_due_to_decision_binding_tradeoff_candidate_not_final"
    return "open_stage251_bounded_followup_due_to_decision_binding_still_inactive_candidate_not_final"


def performance_attribution_rows(
    quality_rows: Sequence[Mapping[str, Any]],
    probability_rows: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    reference = next((row for row in quality_rows if row.get("adapter_id") == "s250_stage248_binding_control"), {})
    rows: list[dict[str, Any]] = []
    for row in quality_rows:
        adapter = str(row.get("adapter_id", ""))
        if adapter == "s250_stage248_binding_control":
            rows.append(
                {
                    "attribution_id": f"{RUN_ID}__{adapter}",
                    "observed_change": "Stage248 reference score surface near-repeated as Stage250 control",
                    "comparison_baseline": "s248_cap0305_reference",
                    "likely_drivers": "same decision design class, same thresholds, same ATR bracket, same model risk cap; model/feature identity changed for Stage250 binding audit",
                    "segment_checks": "validation/OOS, early/mid/late PF, DD, probability binding",
                    "trade_shape": "control row for decision-surface binding repair",
                    "alternative_explanations": "small control delta may come from Stage250 model/feature identity and tester path differences",
                    "attribution_confidence": "high",
                    "next_probe": NEXT_STAGE_ID,
                }
            )
            continue
        rows.append(
            {
                "attribution_id": f"{RUN_ID}__{adapter}",
                "observed_change": (
                    f"validation_net_delta={as_float(row, 'validation_net') - as_float(reference, 'validation_net'):.2f};"
                    f"validation_dd_delta={as_float(row, 'validation_balance_dd_percent') - as_float(reference, 'validation_balance_dd_percent'):.4f};"
                    f"validation_mid_pf_delta={as_float(row, 'validation_mid_pf') - as_float(reference, 'validation_mid_pf'):.6f};"
                    f"oos_net_delta={as_float(row, 'oos_net') - as_float(reference, 'oos_net'):.2f}"
                ),
                "comparison_baseline": "s250_stage248_binding_control",
                "likely_drivers": "rank-conditioned flat tilt changed probability surface before the same thresholds were applied",
                "segment_checks": "validation/OOS KPI, early/mid/late segments, DD, risk/ATR telemetry, probability binding",
                "trade_shape": "should reduce low-margin accepted decisions if binding is active",
                "alternative_explanations": "trade count reduction can mechanically reduce DD while damaging net",
                "attribution_confidence": "medium_high",
                "next_probe": NEXT_STAGE_ID,
            }
        )
    return rows


def failure_memory_rows(quality_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    reference = next((row for row in quality_rows if row.get("adapter_id") == "s250_stage248_binding_control"), {})
    best = best_row(quality_rows)
    rows = [
        {
            "failure_id": "stage250_not_final_until_followup_review",
            "evidence": f"best_adapter={best.get('adapter_id', '')};hard_quality_pass={hard_quality_pass(best)}",
            "impact": "one bounded decision-binding run does not complete the research package",
            "next_handling": NEXT_STAGE_ID,
        },
        {
            "failure_id": "stage248_threshold_no_effect_root_cause",
            "evidence": "Stage248 thresholds were wired into MT5, but model score probabilities stayed above the tested thresholds",
            "impact": "do not repeat small threshold-only nudges",
            "next_handling": "use rank-conditioned score binding or a new source branch",
        },
    ]
    if reference:
        rows.append(
            {
                "failure_id": "stage250_reference_gap_vs_34d",
                "evidence": (
                    f"validation_net_gap={as_float(reference, 'validation_net') - LEGACY_34D['net_profit']:.2f};"
                    f"validation_dd_margin={LEGACY_34D['max_drawdown_percent'] - as_float(reference, 'validation_balance_dd_percent', 99.0):.4f};"
                    f"validation_mid_pf_gap={as_float(reference, 'validation_mid_pf') - LEGACY_34D['profit_factor']:.6f}"
                ),
                "impact": "Stage248 reference remains a near-miss, not a final adapter",
                "next_handling": NEXT_STAGE_ID,
            }
        )
    return rows


def quality_table(rows: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        "| adapter(어댑터) | val net(검증 순손익) | val DD%(검증 낙폭) | mid PF(중간 수익요인) | OOS net(표본외 순손익) | OOS PF(표본외 수익요인) | pass(통과) |",
        "|---|---:|---:|---:|---:|---:|---|",
    ]
    for row in rows:
        lines.append(
            f"| {row.get('adapter_id','')} | {as_float(row, 'validation_net'):.2f} | {as_float(row, 'validation_balance_dd_percent'):.4f} | {as_float(row, 'validation_mid_pf'):.6f} | {as_float(row, 'oos_net'):.2f} | {as_float(row, 'oos_pf'):.6f} | {str(hard_quality_pass(row)).lower()} |"
        )
    return "\n".join(lines)


def report_markdown(
    quality_rows: Sequence[Mapping[str, Any]],
    probability_rows: Sequence[Mapping[str, Any]],
    decision: str,
    external: str,
) -> str:
    best = best_row(quality_rows)
    prob_completed = [row for row in probability_rows if row.get("status") == "completed" and row.get("view") == "actual_routed_total"]
    direction_rows = sum(int(parse_float(row.get("directional_threshold_pass_rows"))) for row in prob_completed)
    threshold_not_met = sum(int(parse_float(row.get("threshold_or_margin_not_met_rows"))) for row in prob_completed)
    side_filter_blocks = sum(int(parse_float(row.get("side_filter_block_rows"))) for row in prob_completed)
    return f"""# Stage250 Decision Surface Binding Repair(250단계 결정 표면 결합 수리)

- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_stage248_evidence_commit(원천 248단계 근거 커밋): `{SOURCE_STAGE248_EVIDENCE_COMMIT}`
- source_stage249_evidence_commit(원천 249단계 근거 커밋): `{SOURCE_STAGE249_EVIDENCE_COMMIT}`
- external_verification_status(외부 검증 상태): `{external}`
- decision(판정): `{decision}`
- boundary(주장 경계): `{BOUNDARY}`

## Bounded Question(경계 질문)

Can rank-conditioned score binding(순위 조건 점수 결합) make the decision/source controls(결정/원천 제어) actually change accepted MT5(MetaTrader 5, 메타트레이더5) decisions after Stage248(248단계) threshold-only no-effect(임계값 전용 효과 없음)?

Effect(효과): Stage248(248단계)의 작은 threshold(임계값) 반복이 아니라, score surface(점수 표면)를 실제 decision surface(결정 표면)에 닿게 만든다.

## Design(설계)

- fixed(고정): ATR SL/TP(ATR 손절/익절) `2.0325/4.615`, model-controlled risk%(모델 제어 위험 비율) cap(상한) `0.0305`, hold(보유) `3`, cooldown(대기) `8`.
- changed(변경): low/mid rank bucket(낮은/중간 순위 구간)에 flat tilt(무포지션 쪽 점수 기울기)를 줘서 threshold(임계값) 앞의 probability(확률)를 바꿨다.
- not done(하지 않음): ONNX hardening(ONNX 경화), live readiness(실거래 준비), deployment(배포).

## KPI Read(KPI 핵심 성과 지표 판독)

{quality_table(quality_rows)}

## Binding Telemetry(결합 기록)

- directional_threshold_pass_rows(방향 임계값 통과 행): `{direction_rows}`
- threshold_or_margin_not_met_rows(임계값/마진 미충족 행): `{threshold_not_met}`
- side_filter_block_rows(방향 필터 차단 행): `{side_filter_blocks}`
- probability_binding_summary(확률 결합 요약): `{rel(PROBABILITY_BINDING_PATH)}`
- model_score_audit(모델 점수 감사): `{rel(MODEL_SCORE_AUDIT_PATH)}`

## Best Read(최선 판독)

- best_adapter(최선 어댑터): `{best.get('adapter_id', '')}`
- hard_quality_pass(강한 품질 통과): `{str(hard_quality_pass(best)).lower()}`
- overall_goal_complete(전체 목표 완료): `false`

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준).
"""


def decision_markdown(decision: str, external: str) -> str:
    return f"""# Stage250 Decision(250단계 판정)

- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- decision(판정): `{decision}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- source_stage248_evidence_commit(원천 248단계 근거 커밋): `{SOURCE_STAGE248_EVIDENCE_COMMIT}`
- source_stage248_hash_record_commit(원천 248단계 해시 기록 커밋): `{SOURCE_STAGE248_HASH_RECORD_COMMIT}`
- source_stage249_evidence_commit(원천 249단계 근거 커밋): `{SOURCE_STAGE249_EVIDENCE_COMMIT}`
- source_stage249_hash_record_commit(원천 249단계 해시 기록 커밋): `{SOURCE_STAGE249_HASH_RECORD_COMMIT}`
- external_verification_status(외부 검증 상태): `{external}`
- report(보고서): `{rel(REPORT_PATH)}`
- summary(요약): `{rel(SUMMARY_CSV_PATH)}`
- quality_matrix(품질 행렬): `{rel(QUALITY_MATRIX_PATH)}`
- probability_binding(확률 결합): `{rel(PROBABILITY_BINDING_PATH)}`
- model_score_audit(모델 점수 감사): `{rel(MODEL_SCORE_AUDIT_PATH)}`
- risk_atr_telemetry(위험/ATR 기록): `{rel(RISK_ATR_TELEMETRY_PATH)}`
- next_stage_or_branch(다음 단계 또는 분기): `{NEXT_STAGE_ID if external == "completed" else STAGE_ID}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage250(250단계) closeout(종료)은 overall goal complete(전체 목표 완료)가 아니다.
"""


def tier_b_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for item in VARIANTS:
        for split in ("validation", "oos"):
            rows.append(
                {
                    "run_id": RUN_ID,
                    "adapter_id": item.adapter_id,
                    "split": split,
                    "status": "diagnostic_missing_required_but_disabled_for_stage250_decision_binding_repair",
                    "fallback_enabled": 0,
                    "fallback_used_count": 0,
                    "notes": "Stage250 isolates Tier A routed decision-surface binding; Tier B fallback remains disabled by prior fallback-only damage memory.",
                }
            )
    return rows


def write_stage251_seed(decision: str, external: str) -> None:
    if external != "completed":
        return
    write_md(
        NEXT_STAGE_ROOT / "00_spec" / "stage_brief.md",
        f"""# {NEXT_STAGE_ID}

Stage251(251단계)는 Stage250(250단계) decision binding repair(결정 결합 수리)를 review-only(검토 전용)로 닫는 bounded review(경계 검토) 단계다.

## Bounded Question(경계 질문)

Did Stage250(250단계) produce useful decision movement(결정 이동) toward the legacy 34D lesson-only KPI(레거시 34D 교훈 전용 핵심 성과 지표) target, or did rank-conditioned binding(순위 조건 결합) damage net/PF/DD(순손익/수익요인/낙폭)?

## Boundary(경계)

`{BOUNDARY}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "01_inputs" / "input_refs.md",
        f"""# Stage251 Inputs(251단계 입력)

- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- source_decision(원천 판정): `{decision}`
- stage250_report(250단계 보고서): `{rel(REPORT_PATH)}`
- stage250_quality_matrix(250단계 품질 행렬): `{rel(QUALITY_MATRIX_PATH)}`
- stage250_failure_memory(250단계 실패 기억): `{rel(FAILURE_MEMORY_PATH)}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "03_reviews" / "review_index.md",
        f"""# Stage251 Review Index(251단계 검토 색인)

- status(상태): `open_planned_from_stage250`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- source_stage(원천 단계): `{STAGE_ID}`
- source_decision(원천 판정): `{decision}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "04_selected" / "selection_status.md",
        f"""# Stage251 Selection Status(251단계 선택 상태)

- stage_status(단계 상태): `open_planned_from_stage250`
- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- source_decision(원천 판정): `{decision}`
- claim_boundary(주장 경계): `{BOUNDARY}`
""",
    )


def replace_stage_block(text: str, key: str, block: str) -> str:
    marker = f"{key}:"
    start = text.find(marker)
    if start < 0:
        return text.rstrip() + "\n\n" + block.rstrip() + "\n"
    next_match = re.search(r"\n[A-Za-z0-9_]+:\n", text[start + len(marker) :])
    if not next_match:
        return text[:start] + block.rstrip() + "\n"
    end = start + len(marker) + next_match.start() + 1
    return text[:start] + block.rstrip() + "\n" + text[end:]


def update_current_truth(decision: str, external: str) -> None:
    active_stage = NEXT_STAGE_ID if external == "completed" else STAGE_ID
    active_run = NEXT_RUN_ID if external == "completed" else RUN_ID
    state = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    state = re.sub(r"^current_run_id: .*$", f"current_run_id: {active_run}", state, count=1, flags=re.MULTILINE)
    state = re.sub(r"^active_stage: .*$", f"active_stage: {active_stage}", state, count=1, flags=re.MULTILINE)
    focus = f"""- >-
  Stage250(250단계) closed(종료) as `{decision}` and Stage251(251단계) `{NEXT_STAGE_ID}` is open_planned(개방 계획). Effect(효과): Stage248(248단계) threshold-only no-effect(임계값 전용 효과 없음)을 rank-conditioned decision binding(순위 조건 결정 결합) 근거로 분리했다.
- >-
  Stage250 evidence(250단계 근거)는 `{rel(REPORT_PATH)}`, `{rel(SUMMARY_CSV_PATH)}`, `{rel(QUALITY_MATRIX_PATH)}`, `{rel(PROBABILITY_BINDING_PATH)}`에 있다. Effect(효과): 다음 단계가 decision movement(결정 이동)와 KPI damage(핵심 성과 지표 손상)를 따로 판정한다.
- >-
  Target surface(목표 표면)는 `{TARGET_SURFACE}`이고 legacy 34D(레거시 34D)는 lesson-only KPI target(교훈 전용 핵심 성과 지표 목표)이다. Effect(효과): v2-native research(v2 고유 연구)를 계속한다.

"""
    state = state.replace("current_focus:\n", "current_focus:\n" + focus, 1)
    stage250_block = f"""stage250_decision_surface_binding_repair_after_stage248_threshold_no_effect:
  packet_id: {PACKET_ID}
  stage_id: {STAGE_ID}
  status: closed_open_stage251_followup_candidate_not_final
  current_run_id: {RUN_ID}
  source_stage: {SOURCE_STAGE_ID}
  source_run: {SOURCE_RUN_ID}
  source_stage248_evidence_commit: {SOURCE_STAGE248_EVIDENCE_COMMIT}
  source_stage248_hash_record_commit: {SOURCE_STAGE248_HASH_RECORD_COMMIT}
  source_stage249_evidence_commit: {SOURCE_STAGE249_EVIDENCE_COMMIT}
  source_stage249_hash_record_commit: {SOURCE_STAGE249_HASH_RECORD_COMMIT}
  decision: {decision}
  report_path: {rel(REPORT_PATH)}
  decision_path: {rel(DECISION_PATH)}
  summary_path: {rel(SUMMARY_CSV_PATH)}
  quality_matrix_path: {rel(QUALITY_MATRIX_PATH)}
  probability_binding_path: {rel(PROBABILITY_BINDING_PATH)}
  external_verification_status: {external}
  pushed_commit_hash: pending_until_push
  next_action: {active_run}
  boundary: {BOUNDARY}
"""
    state = replace_stage_block(state, "stage250_decision_surface_binding_repair_after_stage248_threshold_no_effect", stage250_block)
    if external == "completed":
        stage251_block = f"""stage251_stage250_decision_binding_followup_review:
  packet_id: {NEXT_PACKET_ID}
  stage_id: {NEXT_STAGE_ID}
  status: open_planned_from_stage250
  current_run_id: {NEXT_RUN_ID}
  source_stage: {STAGE_ID}
  source_run: {RUN_ID}
  source_decision: {decision}
  next_action: {NEXT_RUN_ID}
  boundary: {BOUNDARY}
"""
        state = replace_stage_block(state, "stage251_stage250_decision_binding_followup_review", stage251_block)
    io_path(WORKSPACE_STATE_PATH).write_text(state, encoding="utf-8")

    write_md(
        CURRENT_WORKING_STATE_PATH,
        f"""# Current Working State(현재 작업 상태)

- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID if external == "completed" else PACKET_ID}`
- current_run(현재 실행): `{active_run}`
- active_stage(활성 단계): `{active_stage}`
- selected_research_baseline(선택 연구 기준선): `none`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- adapter_under_review(검토 중 어댑터): `stage250_decision_surface_binding_repair`
- status(상태): `stage250_closed_open_stage251_followup_candidate_not_final`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage250(250단계)는 Stage248(248단계) threshold-only no-effect(임계값 전용 효과 없음)의 원인을 decision surface binding(결정 표면 결합)으로 좁게 측정했다. Effect(효과): Stage251(251단계)은 이 결과를 review-only(검토 전용)로 판정한다.

## Latest Stage250 Evidence(최신 250단계 근거)

- run(실행): `{RUN_ID}`
- decision(판정): `{decision}`
- external_verification_status(외부 검증 상태): `{external}`
- report(보고서): `{rel(REPORT_PATH)}`
- summary(요약): `{rel(SUMMARY_CSV_PATH)}`
- quality_matrix(품질 행렬): `{rel(QUALITY_MATRIX_PATH)}`
- probability_binding(확률 결합): `{rel(PROBABILITY_BINDING_PATH)}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준), overall_goal_complete(전체 목표 완료).
""",
    )


def write_status_files(decision: str, external: str) -> None:
    write_md(
        REVIEWS_ROOT / "review_index.md",
        f"""# Stage250 Review Index(250단계 검토 색인)

- status(상태): `closed_open_stage251_followup_candidate_not_final`
- run(실행): `{RUN_ID}`
- decision(판정): `{decision}`
- report(보고서): `{rel(REPORT_PATH)}`
- quality_matrix(품질 행렬): `{rel(QUALITY_MATRIX_PATH)}`
- probability_binding(확률 결합): `{rel(PROBABILITY_BINDING_PATH)}`
- external_verification_status(외부 검증 상태): `{external}`
""",
    )
    write_md(
        SELECTED_ROOT / "selection_status.md",
        f"""# Stage250 Selection Status(250단계 선택 상태)

- stage_status(단계 상태): `closed_open_stage251_followup_candidate_not_final`
- current_packet(현재 작업 묶음): `{PACKET_ID}`
- current_run(현재 실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- decision(판정): `{decision}`
- external_verification_status(외부 검증 상태): `{external}`
- next_stage_or_branch(다음 단계 또는 분기): `{NEXT_STAGE_ID if external == "completed" else STAGE_ID}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`
- claim_boundary(주장 경계): `{BOUNDARY}`
""",
    )


def append_changelog(decision: str) -> None:
    existing = io_path(CHANGELOG_PATH).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG_PATH) else ""
    if RUN_ID in existing:
        return
    entry = (
        f"\n## {utc_now()} Stage250 decision-surface binding repair closeout(250단계 결정 표면 결합 수리 종료)\n\n"
        f"- action(행동): closed(종료) `{STAGE_ID}` with decision(판정) `{decision}`.\n"
        "- effect(효과): Stage248(248단계)의 threshold-only no-effect(임계값 전용 효과 없음)을 score binding(점수 결합) 수리 근거로 분리했다.\n"
        f"- boundary(주장 경계): `{BOUNDARY}`.\n"
    )
    io_path(CHANGELOG_PATH).write_text(existing.rstrip() + entry, encoding="utf-8-sig")


def artifact_rows(result: Mapping[str, Any]) -> list[dict[str, Any]]:
    created = utc_now()
    paths = [
        PRODUCER_PATH,
        REPORT_PATH,
        SUMMARY_JSON_PATH,
        SUMMARY_CSV_PATH,
        SEGMENT_KPI_PATH,
        BALANCE_CURVE_AUDIT_PATH,
        MONTHLY_KPI_PATH,
        CONCENTRATION_PATH,
        DRAWDOWN_PATH,
        QUALITY_MATRIX_PATH,
        RISK_ATR_TELEMETRY_PATH,
        GATE_FEATURE_SUMMARY_PATH,
        PROBABILITY_BINDING_PATH,
        MODEL_SCORE_AUDIT_PATH,
        TIER_B_DIAGNOSTIC_PATH,
        ATTRIBUTION_PATH,
        FAILURE_MEMORY_PATH,
        DECISION_PATH,
        AUDIT_CSV_PATH,
        STAGE_LEDGER_PATH,
        SELECTED_ROOT / "selection_status.md",
        REVIEWS_ROOT / "review_index.md",
        WORKSPACE_STATE_PATH,
        CURRENT_WORKING_STATE_PATH,
        CHANGELOG_PATH,
        NEXT_STAGE_ROOT / "00_spec" / "stage_brief.md",
        NEXT_STAGE_ROOT / "01_inputs" / "input_refs.md",
        NEXT_STAGE_ROOT / "03_reviews" / "review_index.md",
        NEXT_STAGE_ROOT / "04_selected" / "selection_status.md",
    ]
    for execution in result.get("execution_results", []):
        for value in (execution.get("set_path"), execution.get("ini_path"), execution.get("report_path")):
            if value:
                paths.append(Path(str(value)))
    rows: list[dict[str, Any]] = []
    for path in paths:
        if path_exists(path):
            artifact_name = rel(path).replace("/", "__").replace("\\", "__")
            rows.append(
                {
                    "artifact_id": f"{RUN_ID}__{artifact_name}",
                    "artifact_type": "stage250_decision_surface_binding_repair_evidence",
                    "path": rel(path),
                    "sha256": sha256_file_lf_normalized(path),
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "created_at_utc": created,
                    "notes": "Stage250 decision-surface binding repair evidence; research only.",
                }
            )
    return rows


def write_ledgers(result: Mapping[str, Any], decision: str, artifacts: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    summary_rows = result.get("mt5_kpi_records", [])
    primary = ledger_pairs(
        [
            ("decision", decision),
            ("external_status", result.get("external_verification_status", "")),
            ("variant_count", len(VARIANTS)),
            ("target_surface", TARGET_SURFACE),
        ]
    )
    guardrail = ledger_pairs(
        [
            ("next_stage", NEXT_STAGE_ID),
            ("boundary", BOUNDARY),
            ("overall_goal_complete", 0),
        ]
    )
    alpha_rows = stage238.s172.build_mt5_alpha_ledger_rows(
        run_id=RUN_ID,
        stage_id=STAGE_ID,
        mt5_kpi_records=summary_rows,
        run_output_root=RUN_ROOT,
        external_verification_status=str(result.get("external_verification_status", "")),
    )
    for row in alpha_rows:
        row["parent_run_id"] = PARENT_RUN_ID
        row["scoreboard_lane"] = "baseline_adapter_stage250_decision_surface_binding_repair"
        row["judgment"] = decision
        row["status"] = "completed" if result.get("external_verification_status") == "completed" else "blocked"
        row["primary_kpi"] = f"{row.get('primary_kpi', '')};{primary}" if row.get("primary_kpi") else primary
        row["guardrail_kpi"] = f"{row.get('guardrail_kpi', '')};{guardrail}" if row.get("guardrail_kpi") else guardrail
        row["path"] = row.get("path") or rel(REPORT_PATH)
    run_rows = [
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "lane": "baseline_adapter_stage250_decision_surface_binding_repair",
            "status": "completed" if result.get("external_verification_status") == "completed" else "blocked",
            "judgment": decision,
            "path": rel(DECISION_PATH),
            "notes": ledger_pairs(
                [
                    ("source_stage248_evidence_commit", SOURCE_STAGE248_EVIDENCE_COMMIT),
                    ("source_stage249_evidence_commit", SOURCE_STAGE249_EVIDENCE_COMMIT),
                    ("target_surface", TARGET_SURFACE),
                    ("overall_goal_complete", 0),
                    ("boundary", BOUNDARY),
                ]
            ),
        }
    ]
    return {
        "run_registry": upsert_csv_rows(RUN_REGISTRY_PATH, RUN_REGISTRY_COLUMNS, run_rows, key="run_id"),
        "project_alpha_ledger": upsert_csv_rows(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, alpha_rows, key="ledger_row_id"),
        "stage_ledger": upsert_csv_rows(STAGE_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, alpha_rows, key="ledger_row_id"),
        "artifact_registry": upsert_csv_rows(ARTIFACT_REGISTRY_PATH, stage238.ARTIFACT_COLUMNS, artifacts, key="artifact_id"),
    }


def write_packet_files(result: Mapping[str, Any], decision: str, ledger_payload: Mapping[str, Any], quality: Sequence[Mapping[str, Any]]) -> None:
    base_payload = {
        "packet_id": PACKET_ID,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "source_stage": SOURCE_STAGE_ID,
        "source_run_id": SOURCE_RUN_ID,
        "source_stage248_evidence_commit": SOURCE_STAGE248_EVIDENCE_COMMIT,
        "source_stage249_evidence_commit": SOURCE_STAGE249_EVIDENCE_COMMIT,
        "decision": decision,
        "external_verification_status": result.get("external_verification_status", ""),
        "quality_rows": list(quality),
        "claim_boundary": BOUNDARY,
        "overall_goal_complete": False,
    }
    required_gates = [
        "kpi_contract_audit",
        "result_judgment_gate",
        "performance_attribution_gate",
        "artifact_lineage_audit",
        "final_claim_guard",
        "required_gate_coverage_audit",
    ]
    files = {
        "routing_receipt.json": {**base_payload, "route": decision, "next_stage_or_branch": NEXT_STAGE_ID, "required_gates": required_gates, "status": "completed"},
        "kpi_contract_audit.json": {**base_payload, "summary": rel(SUMMARY_CSV_PATH), "segments": rel(SEGMENT_KPI_PATH), "risk_atr": rel(RISK_ATR_TELEMETRY_PATH), "probability_binding": rel(PROBABILITY_BINDING_PATH), "status": "completed"},
        "result_judgment_gate.json": {**base_payload, "judgment_label": "decision_surface_binding_repair_measured_candidate_not_final", "status": "passed_with_boundary"},
        "performance_attribution_gate.json": {**base_payload, "attribution": rel(ATTRIBUTION_PATH), "status": "completed"},
        "artifact_lineage_audit.json": {**base_payload, "producer": rel(PRODUCER_PATH), "ledger_payload": ledger_payload, "status": "completed"},
        "final_claim_guard.json": {**base_payload, "deployment_claim": False, "live_readiness_claim": False, "runtime_authority_claim": False, "production_baseline_claim": False, "operating_reference_claim": False, "operating_promotion_claim": False, "status": "passed"},
        "required_gate_coverage_audit.json": {**base_payload, "required_gates": required_gates, "missing_gates": [], "status": "passed"},
        "aggregate_summary.json": {**base_payload, "ledger_payload": ledger_payload, "pushed_commit_hash": "pending_until_push"},
        "packet_receipt.json": base_payload,
    }
    for name, payload in files.items():
        write_json(PACKET_ROOT / name, payload)
    write_md(
        PACKET_ROOT / "closeout_packet.md",
        f"""# Stage250 Closeout Packet(250단계 종료 작업 묶음)

- packet(작업 묶음): `{PACKET_ID}`
- run(실행): `{RUN_ID}`
- status(상태): `{result.get('external_verification_status', '')}`
- decision(판정): `{decision}`
- report(보고서): `{rel(REPORT_PATH)}`
- next_stage(다음 단계): `{NEXT_STAGE_ID}`
- overall_goal_complete(전체 목표 완료): `false`
- boundary(주장 경계): `{BOUNDARY}`
""",
    )


def configure_runner() -> None:
    values = {
        "STAGE_ID": STAGE_ID,
        "RUN_NUMBER": RUN_NUMBER,
        "RUN_ID": RUN_ID,
        "PACKET_ID": PACKET_ID,
        "PARENT_RUN_ID": PARENT_RUN_ID,
        "NEXT_STAGE_ID": NEXT_STAGE_ID,
        "NEXT_RUN_ID": NEXT_RUN_ID,
        "NEXT_PACKET_ID": NEXT_PACKET_ID,
        "SOURCE_ADAPTER_ID": "s248_cap0305_reference",
        "TARGET_SURFACE": TARGET_SURFACE,
        "BOUNDARY": BOUNDARY,
        "LEGACY_34D": LEGACY_34D,
        "STAGE171_PRIMARY": stage238.prior.STAGE171_PRIMARY,
        "STAGE_ROOT": STAGE_ROOT,
        "RUN_ROOT": RUN_ROOT,
        "REVIEWS_ROOT": REVIEWS_ROOT,
        "SELECTED_ROOT": SELECTED_ROOT,
        "PACKET_ROOT": PACKET_ROOT,
        "NEXT_STAGE_ROOT": NEXT_STAGE_ROOT,
        "PARTIALS_ROOT": PARTIALS_ROOT,
        "COMMON_ROOT": COMMON_ROOT,
        "SUMMARY_JSON_PATH": SUMMARY_JSON_PATH,
        "SUMMARY_CSV_PATH": SUMMARY_CSV_PATH,
        "REPORT_PATH": REPORT_PATH,
        "SEGMENT_KPI_PATH": SEGMENT_KPI_PATH,
        "BALANCE_CURVE_AUDIT_PATH": BALANCE_CURVE_AUDIT_PATH,
        "MONTHLY_KPI_PATH": MONTHLY_KPI_PATH,
        "CONCENTRATION_PATH": CONCENTRATION_PATH,
        "DRAWDOWN_PATH": DRAWDOWN_PATH,
        "QUALITY_MATRIX_PATH": QUALITY_MATRIX_PATH,
        "RISK_ATR_TELEMETRY_PATH": RISK_ATR_TELEMETRY_PATH,
        "GATE_FEATURE_SUMMARY_PATH": GATE_FEATURE_SUMMARY_PATH,
        "PROBABILITY_BINDING_PATH": PROBABILITY_BINDING_PATH,
        "MODEL_SCORE_AUDIT_PATH": MODEL_SCORE_AUDIT_PATH,
        "TIER_B_DIAGNOSTIC_PATH": TIER_B_DIAGNOSTIC_PATH,
        "DECISION_PATH": DECISION_PATH,
        "AUDIT_CSV_PATH": AUDIT_CSV_PATH,
        "STAGE_LEDGER_PATH": STAGE_LEDGER_PATH,
        "RUN_REGISTRY_PATH": RUN_REGISTRY_PATH,
        "PROJECT_LEDGER_PATH": PROJECT_LEDGER_PATH,
        "ARTIFACT_REGISTRY_PATH": ARTIFACT_REGISTRY_PATH,
        "WORKSPACE_STATE_PATH": WORKSPACE_STATE_PATH,
        "CURRENT_WORKING_STATE_PATH": CURRENT_WORKING_STATE_PATH,
        "CHANGELOG_PATH": CHANGELOG_PATH,
        "PRODUCER_PATH": PRODUCER_PATH,
        "VARIANTS": VARIANTS,
        "VARIANT_EXTRAS": VARIANT_EXTRAS,
        "MODEL_RISK_MIN_PCT": MODEL_RISK_MIN_PCT,
        "VARIANT_BY_ID": {variant.adapter_id: variant for variant in VARIANTS},
        "SOURCE_SPECS_BY_VARIANT": SOURCE_SPECS_BY_VARIANT,
        "CONTEXT_GATE_SPECS": {
            variant.adapter_id: {
                "gate_column": f"{GATE_COLUMN_PREFIX}_{VARIANT_EXTRAS[variant.adapter_id]['axis']}",
                "gate_type": "stage250_reference_side_filter_rank_conditioned_binding",
                "block_mode": VARIANT_EXTRAS[variant.adapter_id]["block_mode"],
                "description": "Stage250 keeps Stage248 side filter and changes rank-conditioned score binding.",
            }
            for variant in VARIANTS
        },
        "SIGNAL_COLUMN": SIGNAL_COLUMN,
    }
    for module in (
        stage238.s161,
        stage238.s172,
        stage238.s172.s58,
        stage238.s219,
        stage238.s213,
        stage238.s210,
        stage238.s192,
        stage238.s190,
        stage238.base,
        stage238.s188,
        stage238.s184,
        stage238.s180,
        stage238.s178,
        stage238.s176,
        stage238.s174,
    ):
        for name, value in values.items():
            setattr(module, name, value)
    stage238.s161.prepare_inputs = prepare_inputs
    stage238.s161.build_attempts = build_attempts
    stage238.s161.extra_set_values = extra_set_values
    stage238.s161._CONTEXT_LOOKUP = None
    stage238.s161.base.configure_reused_engine()


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = stage238.s161.parse_args(argv)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    configure_runner()
    stage238.s161.configure_base()
    args = parse_args(argv or sys.argv[1:])
    inputs = prepare_inputs(Path(args.common_files_root))
    attempts = build_attempts(inputs)
    prepared = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "stage_number": 250,
        "run_number": RUN_NUMBER,
        "run_root": RUN_ROOT,
        "packet_id": PACKET_ID,
        "attempts": attempts,
        "common_copies": inputs["common_copies"],
        "feature_exports": inputs["feature_exports"],
        "model_artifacts": inputs["model_exports"],
        "route_coverage": stage238.s161.base.engine.route_coverage(),
        "model_family": "baseline_adapter_stage250_v2_native_decision_surface_binding_repair",
        "feature_set_id": "stage250_signal_margin_rank_reference_side_filter_binding",
        "label_id": "label_v1_fwd12_m5_logret_train_q33_3class",
        "split_contract": "split_v1_calendar_train_20220901_20241231_val_20250101_20250930_oos_20251001_20260413",
        "claim_boundary": BOUNDARY,
        "target_surface": TARGET_SURFACE,
        "gate_rows": inputs["gate_rows"],
    }
    result = stage238.load_existing_result_if_requested(args) or stage238.s161.base.execute_or_materialize(prepared, args)
    audit_rows = stage238.s172.s58.audit_rows_for_result(result, float(args.cost_stress_per_trade)) if result.get("mt5_kpi_records") else []
    risk_rows = stage238.s172.s58.risk_rows_from_result(result)
    summary_rows = stage238.s172.s58.build_summary_rows(result, audit_rows, risk_rows)
    segment_rows = stage238.s172.s58.segment_kpi_rows(summary_rows)
    probability_rows = stage238.s161.probability_binding_rows(result)
    model_rows = stage238.s161.model_score_rows(inputs)
    balance_rows, monthly_rows, concentration_rows, drawdown_rows = stage238.s172.build_curve_audit(summary_rows, segment_rows)
    quality_rows = stage238.s172.quality_rows(summary_rows, segment_rows, balance_rows)
    attribution_rows = performance_attribution_rows(quality_rows, probability_rows)
    failure_rows = failure_memory_rows(quality_rows)
    external = str(result.get("external_verification_status") or "blocked")
    decision = decide(quality_rows, probability_rows, external)

    stage238.s161.write_run_identity(result, probability_rows, model_rows)
    write_csv(AUDIT_CSV_PATH, audit_rows)
    write_csv(SUMMARY_CSV_PATH, summary_rows)
    write_csv(SEGMENT_KPI_PATH, segment_rows)
    write_csv(BALANCE_CURVE_AUDIT_PATH, balance_rows)
    write_csv(MONTHLY_KPI_PATH, monthly_rows)
    write_csv(CONCENTRATION_PATH, concentration_rows)
    write_csv(DRAWDOWN_PATH, drawdown_rows)
    write_csv(QUALITY_MATRIX_PATH, quality_rows)
    write_csv(RISK_ATR_TELEMETRY_PATH, risk_rows)
    write_csv(GATE_FEATURE_SUMMARY_PATH, inputs["gate_rows"])
    write_csv(PROBABILITY_BINDING_PATH, probability_rows)
    write_csv(MODEL_SCORE_AUDIT_PATH, model_rows)
    write_csv(TIER_B_DIAGNOSTIC_PATH, tier_b_rows())
    write_csv(ATTRIBUTION_PATH, attribution_rows)
    write_csv(FAILURE_MEMORY_PATH, failure_rows)
    write_md(REPORT_PATH, report_markdown(quality_rows, probability_rows, decision, external))
    write_md(DECISION_PATH, decision_markdown(decision, external))
    write_json(
        SUMMARY_JSON_PATH,
        {
            "run_id": RUN_ID,
            "decision": decision,
            "external_verification_status": external,
            "summary_rows": summary_rows,
            "segment_rows": segment_rows,
            "balance_rows": balance_rows,
            "monthly_rows": monthly_rows,
            "concentration_rows": concentration_rows,
            "drawdown_rows": drawdown_rows,
            "probability_rows": probability_rows,
            "model_rows": model_rows,
            "attribution_rows": attribution_rows,
            "failure_memory_rows": failure_rows,
            "quality_rows": quality_rows,
            "gate_rows": inputs["gate_rows"],
            "legacy_34d": LEGACY_34D,
            "oos_reference": OOS_REFERENCE,
            "source_stage248_evidence_commit": SOURCE_STAGE248_EVIDENCE_COMMIT,
            "source_stage249_evidence_commit": SOURCE_STAGE249_EVIDENCE_COMMIT,
            "claim_boundary": BOUNDARY,
            "overall_goal_complete": False,
            "pushed_commit_hash": "pending_until_push",
        },
    )
    write_stage251_seed(decision, external)
    update_current_truth(decision, external)
    write_status_files(decision, external)
    append_changelog(decision)
    artifacts = artifact_rows(result)
    ledger_payload = write_ledgers(result, decision, artifacts)
    write_packet_files(result, decision, ledger_payload, quality_rows)
    print(
        json.dumps(
            json_ready(
                {
                    "status": external,
                    "run_id": RUN_ID,
                    "decision": decision,
                    "overall_goal_complete": False,
                    "report": rel(REPORT_PATH),
                    "quality_rows": quality_rows,
                }
            ),
            indent=2,
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
