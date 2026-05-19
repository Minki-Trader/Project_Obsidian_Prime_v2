from __future__ import annotations

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
from foundation.models.ebm_score_table import FIELDNAMES, load_ebm_score_table, score_ebm_table_probabilities  # noqa: E402
from stage_pipelines.stage235 import side_specific_validation_net_recovery_after_session_context_tradeoff as prior  # noqa: E402

s219 = prior.s219
s213 = prior.s213
s210 = prior.s210
s192 = prior.s192
s190 = prior.s190
base = prior.base
s188 = prior.s188
s184 = prior.s184
s180 = prior.s180
s178 = prior.s178
s176 = prior.s176
s174 = prior.s174
s172 = prior.s172
s161 = prior.s161
repair = prior.repair

STAGE_ID = "238_adapter_research__score_shape_repair_after_threshold_surface_discrete"
RUN_NUMBER = "run238A"
RUN_ID = "run238A_stage238_score_shape_repair_after_threshold_surface_discrete_v1"
PACKET_ID = "stage238_score_shape_repair_after_threshold_surface_discrete_v1"
PARENT_RUN_ID = "run237A_stage237_reference_micro_threshold_recovery_after_context_side_failure_v1"
SOURCE_STAGE_ID = "237_adapter_research__reference_micro_threshold_recovery_after_context_side_failure"
SOURCE_RUN_ID = PARENT_RUN_ID
SOURCE_STAGE237_EVIDENCE_COMMIT = "b3dc12f65905c2063fc8cac59298fabec8a1a6ce"
SOURCE_STAGE237_HASH_RECORD_COMMIT = "b2e16f262369baef1f4d990d90383cfa263d42de"
SOURCE_STAGE235_RUN_ID = "run235A_stage235_side_specific_validation_net_recovery_after_session_context_tradeoff_v1"
SOURCE_REFERENCE_ADAPTER = "s235_session_ref_h3_cd8"
NEXT_STAGE_ID = "239_adapter_research__stage238_score_shape_followup_review"
NEXT_RUN_ID = "run239A_stage239_stage238_score_shape_followup_review_v1"
NEXT_PACKET_ID = "stage239_stage238_score_shape_followup_review_v1"
TARGET_SURFACE = "legacy_34d_kpi_lesson_only_v2_native_score_shape_repair_after_threshold_surface_discrete"
BOUNDARY = prior.BOUNDARY
LEGACY_34D = prior.LEGACY_34D
OOS_REFERENCE = {
    "adapter_id": SOURCE_REFERENCE_ADAPTER,
    "oos_net": 719.48,
    "oos_pf": 1.74,
    "oos_dd": 9.2072,
}

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
SELECTED_ROOT = STAGE_ROOT / "04_selected"
PACKET_ROOT = Path("docs/agent_control/packets") / PACKET_ID
NEXT_STAGE_ROOT = Path("stages") / NEXT_STAGE_ID
PARTIALS_ROOT = RUN_ROOT / "partials"
COMMON_ROOT = f"OPV2/s238a/{RUN_NUMBER}"

SUMMARY_JSON_PATH = REVIEWS_ROOT / "stage238_summary.json"
SUMMARY_CSV_PATH = REVIEWS_ROOT / "stage238_score_shape_kpi_summary.csv"
REPORT_PATH = REVIEWS_ROOT / "stage238_score_shape_repair_report.md"
SEGMENT_KPI_PATH = REVIEWS_ROOT / "stage238_segment_kpi_summary.csv"
BALANCE_CURVE_AUDIT_PATH = REVIEWS_ROOT / "stage238_balance_curve_audit.csv"
MONTHLY_KPI_PATH = REVIEWS_ROOT / "stage238_monthly_kpi_summary.csv"
CONCENTRATION_PATH = REVIEWS_ROOT / "stage238_concentration_risk_summary.csv"
DRAWDOWN_PATH = REVIEWS_ROOT / "stage238_drawdown_recovery_summary.csv"
QUALITY_MATRIX_PATH = REVIEWS_ROOT / "stage238_quality_matrix.csv"
RISK_ATR_TELEMETRY_PATH = REVIEWS_ROOT / "stage238_risk_atr_telemetry.csv"
GATE_FEATURE_SUMMARY_PATH = REVIEWS_ROOT / "stage238_gate_feature_summary.csv"
PROBABILITY_BINDING_PATH = REVIEWS_ROOT / "stage238_probability_telemetry_summary.csv"
MODEL_SCORE_AUDIT_PATH = REVIEWS_ROOT / "stage238_model_score_audit.csv"
TIER_B_DIAGNOSTIC_PATH = REVIEWS_ROOT / "stage238_tier_b_diagnostic_summary.csv"
DECISION_PATH = REVIEWS_ROOT / "stage238_decision.md"
AUDIT_CSV_PATH = REVIEWS_ROOT / "stage238_trade_audit.csv"
STAGE_LEDGER_PATH = REVIEWS_ROOT / "stage_run_ledger.csv"

RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
PROJECT_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
ARTIFACT_REGISTRY_PATH = Path("docs/registers/artifact_registry.csv")
WORKSPACE_STATE_PATH = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE_PATH = Path("docs/context/current_working_state.md")
CHANGELOG_PATH = Path("docs/workspace/changelog.md")
PRODUCER_PATH = Path("stage_pipelines/stage238/score_shape_repair_after_threshold_surface_discrete.py")
ARTIFACT_COLUMNS = prior.ARTIFACT_COLUMNS

SIGNAL_COLUMN = s161.SIGNAL_COLUMN
RANK_COLUMN = "stage238_margin_rank_bucket"
SOURCE_SPEC = dict(s161.s158.LOW_EDGE_SOURCE_SPEC)
REFERENCE_EXTRA = dict(prior.VARIANT_EXTRAS[SOURCE_REFERENCE_ADAPTER])

VARIANTS = (
    repair.RepairVariant(
        adapter_id="s238_rank3f_neutral_ref",
        label="stage238_rank3f_neutral_ref",
        atr_enabled=True,
        model_risk_enabled=True,
        fixed_lot=0.25,
        atr_stop_multiplier=2.0325,
        atr_take_profit_multiplier=4.615,
        model_risk_max_pct=0.031375,
        same_direction_reentry_cooldown_bars=8,
        short_threshold=0.54,
        long_threshold=0.52,
        close_on_flat_signal=False,
        reverse_on_opposite_signal=True,
        close_only_on_opposite_signal=False,
        max_hold_bars=3,
        notes="Stage238 control: 3-feature neutral score shape preserving Stage235 reference side filter.",
    ),
    repair.RepairVariant(
        adapter_id="s238_lowpen015_rank3f",
        label="stage238_low_margin_penalty_015",
        atr_enabled=True,
        model_risk_enabled=True,
        fixed_lot=0.25,
        atr_stop_multiplier=2.0325,
        atr_take_profit_multiplier=4.615,
        model_risk_max_pct=0.031375,
        same_direction_reentry_cooldown_bars=8,
        short_threshold=0.54,
        long_threshold=0.52,
        close_on_flat_signal=False,
        reverse_on_opposite_signal=True,
        close_only_on_opposite_signal=False,
        max_hold_bars=3,
        notes="Stage238 repair: light low-margin directional penalty creates a weak confidence rank.",
    ),
    repair.RepairVariant(
        adapter_id="s238_lowpen025_rank3f",
        label="stage238_low_margin_penalty_025",
        atr_enabled=True,
        model_risk_enabled=True,
        fixed_lot=0.25,
        atr_stop_multiplier=2.0325,
        atr_take_profit_multiplier=4.615,
        model_risk_max_pct=0.031375,
        same_direction_reentry_cooldown_bars=8,
        short_threshold=0.54,
        long_threshold=0.52,
        close_on_flat_signal=False,
        reverse_on_opposite_signal=True,
        close_only_on_opposite_signal=False,
        max_hold_bars=3,
        notes="Stage238 repair: stronger low-margin directional penalty tests trade-quality filtering.",
    ),
    repair.RepairVariant(
        adapter_id="s238_highbonus010_rank3f",
        label="stage238_high_margin_bonus_010",
        atr_enabled=True,
        model_risk_enabled=True,
        fixed_lot=0.25,
        atr_stop_multiplier=2.0325,
        atr_take_profit_multiplier=4.615,
        model_risk_max_pct=0.031375,
        same_direction_reentry_cooldown_bars=8,
        short_threshold=0.54,
        long_threshold=0.52,
        close_on_flat_signal=False,
        reverse_on_opposite_signal=True,
        close_only_on_opposite_signal=False,
        max_hold_bars=3,
        notes="Stage238 repair: high-margin directional bonus tests risk-confidence shaping without context-axis repetition.",
    ),
)

VARIANT_EXTRAS: dict[str, dict[str, Any]] = {
    "s238_rank3f_neutral_ref": {
        "axis": "rank3f_neutral_ref",
        "logit_strength": 0.50,
        "risk_confidence_floor": 0.50,
        "risk_confidence_ceiling": 0.60,
        "block_mode": "both",
        "side_filter_enabled": True,
        "short_block_rule": "midwide_lowedge",
        "long_block_rule": "session_only",
        "rank_scores": {
            "low": (0.0, 0.0, 0.0),
            "mid": (0.0, 0.0, 0.0),
            "high": (0.0, 0.0, 0.0),
            "vhigh": (0.0, 0.0, 0.0),
        },
    },
    "s238_lowpen015_rank3f": {
        "axis": "lowpen015_rank3f",
        "logit_strength": 0.50,
        "risk_confidence_floor": 0.50,
        "risk_confidence_ceiling": 0.60,
        "block_mode": "both",
        "side_filter_enabled": True,
        "short_block_rule": "midwide_lowedge",
        "long_block_rule": "session_only",
        "rank_scores": {
            "low": (-0.15, 0.15, -0.15),
            "mid": (0.0, 0.0, 0.0),
            "high": (0.0, 0.0, 0.0),
            "vhigh": (0.0, 0.0, 0.0),
        },
    },
    "s238_lowpen025_rank3f": {
        "axis": "lowpen025_rank3f",
        "logit_strength": 0.50,
        "risk_confidence_floor": 0.50,
        "risk_confidence_ceiling": 0.60,
        "block_mode": "both",
        "side_filter_enabled": True,
        "short_block_rule": "midwide_lowedge",
        "long_block_rule": "session_only",
        "rank_scores": {
            "low": (-0.25, 0.25, -0.25),
            "mid": (0.0, 0.0, 0.0),
            "high": (0.0, 0.0, 0.0),
            "vhigh": (0.0, 0.0, 0.0),
        },
    },
    "s238_highbonus010_rank3f": {
        "axis": "highbonus010_rank3f",
        "logit_strength": 0.50,
        "risk_confidence_floor": 0.50,
        "risk_confidence_ceiling": 0.60,
        "block_mode": "both",
        "side_filter_enabled": True,
        "short_block_rule": "midwide_lowedge",
        "long_block_rule": "session_only",
        "rank_scores": {
            "low": (0.0, 0.0, 0.0),
            "mid": (0.0, 0.0, 0.0),
            "high": (0.10, -0.10, 0.10),
            "vhigh": (0.15, -0.15, 0.15),
        },
    },
}

SOURCE_SPECS_BY_VARIANT = {variant.adapter_id: dict(SOURCE_SPEC) for variant in VARIANTS}
MODEL_RISK_MIN_PCT = {variant.adapter_id: 0.005 for variant in VARIANTS}


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    return s172.rel(path)


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


def rank_bucket_for(row: Mapping[str, str]) -> tuple[int, str]:
    margin = parse_float(row.get("et40_decision_margin"), 0.0)
    if margin < 0.04:
        return 0, "low"
    if margin <= 0.0775:
        return 1, "mid"
    if margin <= 0.12:
        return 2, "high"
    return 3, "vhigh"


def reference_gate_value(row: Mapping[str, str]) -> float:
    signal = int(round(parse_float(row.get(SIGNAL_COLUMN), 0.0)))
    if signal == 0:
        return 0.0
    minutes = s174.s167_minutes_for(row)
    margin = s174.s167_margin_for(row)
    if signal > 0:
        session_hit = (
            minutes is not None
            and float(REFERENCE_EXTRA["session_min"]) <= minutes <= float(REFERENCE_EXTRA["session_max"])
        )
        if session_hit:
            return 2.0
    if signal < 0:
        wide_session = (
            minutes is not None
            and float(REFERENCE_EXTRA["wide_session_min"]) <= minutes <= float(REFERENCE_EXTRA["wide_session_max"])
        )
        wide_margin = float(REFERENCE_EXTRA["wide_margin_min"]) <= margin <= float(REFERENCE_EXTRA["wide_margin_max"])
        if wide_session or wide_margin:
            return 1.0
    return 0.0


def write_score_shape_model(path: Path, variant: repair.RepairVariant, gate_column: str) -> dict[str, Any]:
    extra = VARIANT_EXTRAS[variant.adapter_id]
    strength = float(extra["logit_strength"])
    rank_scores = extra["rank_scores"]
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
            [1.0, 0.0, 0.0],
            [1.0, 1.0, 0.0],
            [1.0, 2.0, 0.0],
        ],
        dtype="float64",
    )
    probabilities = score_ebm_table_probabilities(table, sample_values)
    feature_order = (SIGNAL_COLUMN, RANK_COLUMN, gate_column)
    return {
        "path": rel(path),
        "sha256": sha256_file_lf_normalized(path),
        "format": "stage238_three_feature_score_shape_ebm_table_csv_v1",
        "feature_order": list(feature_order),
        "feature_order_hash": s161.base.engine.ordered_hash(feature_order),
        "feature_count": 3,
        "signal_column": SIGNAL_COLUMN,
        "rank_column": RANK_COLUMN,
        "gate_column": gate_column,
        "rank_scores": rank_scores,
        "parity_sample_values": sample_values.tolist(),
        "parity_sample_probabilities": probabilities.tolist(),
    }


def write_score_shape_feature(source: Path, destination: Path, variant: repair.RepairVariant) -> dict[str, Any]:
    gate_column = f"stage238_gate_{VARIANT_EXTRAS[variant.adapter_id]['axis']}"
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
                signal = int(round(parse_float(row.get(SIGNAL_COLUMN), 0.0)))
                bucket_value, bucket_label = rank_bucket_for(row)
                gate = reference_gate_value(row)
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
        "gate_column": gate_column,
        "source_feature": rel(source),
        "score_shape_feature": rel(destination),
        "total_rows": total_rows,
        "signal_rows": signal_rows,
        "blocked_signal_rows": blocked_signal_rows,
        "allowed_signal_rows": signal_rows - blocked_signal_rows,
        "rank_counts": rank_counts,
        "allowed_signal_rank_counts": allowed_signal_rank_counts,
        "block_mode": VARIANT_EXTRAS[variant.adapter_id]["block_mode"],
        "gate_description": "Stage238 reference side filter: short blocks use Stage235 wide session or margin gate; long blocks use Stage235 session gate.",
        "side_filter_feature_index": 2,
        "rank_feature_index": 1,
    }


def load_existing_result_if_requested(args: Any) -> dict[str, Any] | None:
    if not bool(getattr(args, "resume_partials", False)):
        return None
    kpi_path = RUN_ROOT / "kpi_record.json"
    if not path_exists(kpi_path):
        return None
    with io_path(kpi_path).open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if payload.get("run_id") != RUN_ID:
        return None
    if not payload.get("mt5_kpi_records"):
        return None
    return payload


def prepare_inputs(common_files_root: Path) -> dict[str, Any]:
    copied: list[dict[str, Any]] = []
    gate_rows: list[dict[str, Any]] = []
    model_exports: dict[str, dict[str, Any]] = {}
    feature_exports: dict[str, dict[str, dict[str, Any]]] = {}
    for variant in VARIANTS:
        gate_column = f"stage238_gate_{VARIANT_EXTRAS[variant.adapter_id]['axis']}"
        model_source = s161.base.engine.source_model_for_variant(variant)
        model_local = RUN_ROOT / variant.adapter_id / "models" / f"{variant.adapter_id}_model.csv"
        model_meta = write_score_shape_model(model_local, variant, gate_column)
        copied.append(
            {
                "source": rel(model_source),
                "path": rel(model_local),
                "sha256": sha256_file_lf_normalized(model_local),
                "transform": "stage238_three_feature_score_shape_model",
            }
        )
        copied.append(s161.base.engine.copy_to_common(model_local, f"{COMMON_ROOT}/{variant.adapter_id}/models/{model_local.name}", common_files_root))
        model_exports[variant.adapter_id] = {
            **model_meta,
            "common_path": f"{COMMON_ROOT}/{variant.adapter_id}/models/{model_local.name}",
            "source_model": rel(model_source),
            "source_anchor": s161.base.engine.source_anchor_for_variant(variant),
        }
        feature_exports[variant.adapter_id] = {}
        for split in ("validation_is", "oos"):
            token = "val" if split == "validation_is" else "oos"
            feature_source = s161.base.engine.source_feature(split, variant, "a")
            feature_local = RUN_ROOT / variant.adapter_id / "features" / f"{variant.adapter_id}_{token}.csv"
            gate_row = write_score_shape_feature(feature_source, feature_local, variant)
            gate_row["split"] = split
            gate_rows.append(gate_row)
            copied.append(
                {
                    "source": rel(feature_source),
                    "path": rel(feature_local),
                    "sha256": sha256_file_lf_normalized(feature_local),
                    "transform": "stage238_margin_rank_plus_stage235_reference_gate_feature",
                }
            )
            copied.append(s161.base.engine.copy_to_common(feature_local, f"{COMMON_ROOT}/{variant.adapter_id}/features/{feature_local.name}", common_files_root))
            feature_exports[variant.adapter_id][split] = {
                "path": rel(feature_local),
                "common_path": f"{COMMON_ROOT}/{variant.adapter_id}/features/{feature_local.name}",
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


def extra_set_values(variant: repair.RepairVariant, magic: int) -> dict[str, Any]:
    values = s161.base.engine.extra_set_values(variant, magic)
    extra = VARIANT_EXTRAS[variant.adapter_id]
    values["InpSideFilterEnabled"] = True
    values["InpSideFilterFeatureIndex"] = 2
    values["InpFallbackSideFilterFeatureIndex"] = 2
    values["InpBlockShortFeatureRange"] = True
    values["InpBlockShortFeatureMin"] = 0.5
    values["InpBlockShortFeatureMax"] = 1.5
    values["InpBlockLongFeatureRange"] = True
    values["InpBlockLongFeatureMin"] = 1.5
    values["InpBlockLongFeatureMax"] = 2.5
    values["InpModelRiskConfidenceFloor"] = float(extra["risk_confidence_floor"])
    values["InpModelRiskConfidenceCeiling"] = float(extra["risk_confidence_ceiling"])
    return values


def build_attempts(inputs: Mapping[str, Any]) -> list[dict[str, Any]]:
    attempts: list[dict[str, Any]] = []
    for variant_index, variant in enumerate(VARIANTS, start=1):
        variant_root = RUN_ROOT / variant.adapter_id
        for split in ("validation_is", "oos"):
            date_values = s161.base.parse_ini(s161.base.engine.source_attempt_ini(split, variant))
            split_token = "val" if split == "validation_is" else "oos"
            for role_index, (tier, attempt_role, prefix, attempt_token) in enumerate(
                (
                    (s161.base.mt5.TIER_A, "tier_only_total", f"mt5_tier_a_only_{variant.adapter_id}", "ta"),
                    (s161.base.mt5.TIER_AB, "routed_total", f"mt5_routed_{variant.adapter_id}", "rt"),
                ),
                start=1,
            ):
                magic = 23810000 + variant_index * 100 + (1 if split == "validation_is" else 50) + role_index
                attempts.append(
                    s161.base.attempt_payload(
                        run_root=variant_root,
                        run_id=RUN_ID,
                        stage_number=238,
                        exploration_label="stage238_BaselineAdapter__ScoreShapeRepairAfterThresholdSurfaceDiscrete",
                        attempt_name=f"{variant.adapter_id}_{attempt_token}_{split_token}",
                        tier=tier,
                        split=split,
                        model_path=str(inputs["model_exports"][variant.adapter_id]["common_path"]),
                        model_id=f"{RUN_ID}_{variant.adapter_id}_entry_adapter",
                        model_backend="ebm_table",
                        feature_path=str(inputs["feature_exports"][variant.adapter_id][split]["common_path"]),
                        feature_count=3,
                        feature_order_hash=inputs["model_exports"][variant.adapter_id]["feature_order_hash"],
                        short_threshold=variant.short_threshold,
                        long_threshold=variant.long_threshold,
                        min_margin=0.0,
                        invert_signal=False,
                        from_date=str(date_values["FromDate"]),
                        to_date=str(date_values["ToDate"]),
                        primary_active_tier="tier_a",
                        attempt_role=attempt_role,
                        record_view_prefix=prefix,
                        max_hold_bars=variant.max_hold_bars,
                        common_root=f"{COMMON_ROOT}/{variant.adapter_id}",
                        fallback_enabled=False,
                        close_on_flat_signal=variant.close_on_flat_signal,
                        reverse_on_opposite_signal=variant.reverse_on_opposite_signal,
                        close_only_on_opposite_signal=variant.close_only_on_opposite_signal,
                        extra_set_values=extra_set_values(variant, magic),
                    )
                )
    return attempts


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
        "SOURCE_ADAPTER_ID": SOURCE_REFERENCE_ADAPTER,
        "TARGET_SURFACE": TARGET_SURFACE,
        "BOUNDARY": BOUNDARY,
        "LEGACY_34D": LEGACY_34D,
        "STAGE171_PRIMARY": prior.STAGE171_PRIMARY,
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
                "gate_column": f"stage238_gate_{VARIANT_EXTRAS[variant.adapter_id]['axis']}",
                "gate_type": "stage235_reference_side_filter",
                "block_mode": VARIANT_EXTRAS[variant.adapter_id]["block_mode"],
                "description": "Stage238 reuses Stage235 reference side filter while adding margin-rank score shape.",
            }
            for variant in VARIANTS
        },
        "SIGNAL_COLUMN": SIGNAL_COLUMN,
    }
    for module in (s161, s172, s172.s58, s219, s213, s210, s192, s190, base, s188, s184, s180, s178, s176, s174):
        for name, value in values.items():
            setattr(module, name, value)
    s161.prepare_inputs = prepare_inputs
    s161.build_attempts = build_attempts
    s161.extra_set_values = extra_set_values
    s161._CONTEXT_LOOKUP = None
    s161.base.configure_reused_engine()


def split_row(summary_rows: Sequence[Mapping[str, Any]], adapter_id: str, split: str) -> Mapping[str, Any]:
    for row in summary_rows:
        if row.get("adapter_id") == adapter_id and row.get("split") == split and row.get("view") == "actual_routed_total":
            return row
    return {}


def pass_stage238(row: Mapping[str, Any]) -> bool:
    return (
        as_float(row, "validation_net") >= LEGACY_34D["net_profit"]
        and as_float(row, "validation_early_pf") >= LEGACY_34D["profit_factor"]
        and as_float(row, "validation_mid_pf") >= LEGACY_34D["profit_factor"]
        and as_float(row, "validation_balance_dd_percent", 99.0) <= LEGACY_34D["max_drawdown_percent"]
        and as_float(row, "oos_net") >= OOS_REFERENCE["oos_net"]
        and as_float(row, "oos_pf") >= OOS_REFERENCE["oos_pf"]
        and as_float(row, "oos_balance_dd_percent", 99.0) <= OOS_REFERENCE["oos_dd"]
    )


def decide(quality_rows: Sequence[Mapping[str, Any]], external: str) -> str:
    if external != "completed":
        return "continue_stage238_runtime_completion_due_to_incomplete_runtime_candidate_not_final"
    if any(pass_stage238(row) for row in quality_rows):
        return "open_stage239_score_shape_followup_review_candidate_not_final"
    return "open_stage239_bounded_followup_due_to_score_shape_tradeoff_candidate_not_final"


def tier_b_rows_stage238() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for variant in VARIANTS:
        for split in ("validation", "oos"):
            rows.append(
                {
                    "run_id": RUN_ID,
                    "adapter_id": variant.adapter_id,
                    "split": split,
                    "status": "diagnostic_missing_required_but_disabled_for_stage238_score_shape_repair",
                    "fallback_enabled": 0,
                    "fallback_used_count": 0,
                    "notes": "Stage238 isolates Tier A routed score shape repair; Tier B fallback remains disabled by prior fallback-only damage memory.",
                }
            )
    return rows


def best_row(rows: Sequence[Mapping[str, Any]]) -> Mapping[str, Any]:
    if not rows:
        return {}
    return max(
        rows,
        key=lambda row: (
            pass_stage238(row),
            as_float(row, "validation_net"),
            as_float(row, "validation_early_pf"),
            as_float(row, "validation_mid_pf"),
            as_float(row, "oos_net"),
            -as_float(row, "oos_balance_dd_percent", 99.0),
        ),
    )


def kpi_table(rows: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        "| adapter(어댑터) | val net(검증 순손익) | early PF(초반 수익요인) | mid PF(중반 수익요인) | val DD%(검증 낙폭) | OOS net(표본외 순손익) | OOS PF(표본외 수익요인) | OOS DD%(표본외 낙폭) | flags(표식) |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in rows:
        lines.append(
            "| {adapter} | {val:.2f} | {early:.6f} | {mid:.6f} | {vdd:.4f} | {oos:.2f} | {opf:.6f} | {odd:.4f} | {flags} |".format(
                adapter=row.get("adapter_id", ""),
                val=as_float(row, "validation_net"),
                early=as_float(row, "validation_early_pf"),
                mid=as_float(row, "validation_mid_pf"),
                vdd=as_float(row, "validation_balance_dd_percent"),
                oos=as_float(row, "oos_net"),
                opf=as_float(row, "oos_pf"),
                odd=as_float(row, "oos_balance_dd_percent"),
                flags=row.get("quality_flags", ""),
            )
        )
    return "\n".join(lines)


def report_markdown(quality_rows: Sequence[Mapping[str, Any]], decision: str, external: str) -> str:
    best = best_row(quality_rows)
    return f"""# Stage238 Score Shape Repair Report(238단계 점수 형태 수리 보고서)

- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- source_stage237_evidence_commit(원천 237단계 근거 커밋): `{SOURCE_STAGE237_EVIDENCE_COMMIT}`
- source_stage237_hash_record_commit(원천 237단계 해시 기록 커밋): `{SOURCE_STAGE237_HASH_RECORD_COMMIT}`
- external_verification_status(외부 검증 상태): `{external}`
- decision(판정): `{decision}`
- boundary(주장 경계): `{BOUNDARY}`

## Bounded Design(경계 설계)

- hypothesis(가설): Stage235(235단계) 기준형의 binary probability(이진 확률)를 margin bucket(마진 구간) 점수로 세분화하면 34D(34D 기준) 부족분을 회복할 수 있다.
- fixed variables(고정 변수): ATR SL/TP(ATR 손절/익절) `2.0325/4.615`, model-controlled risk%(모델 제어 위험 비율) cap(상한) `0.031375`, hold(보유) `3`, same-direction cooldown(동방향 대기) `8`, Stage235 reference side filter(235단계 기준 방향 필터).
- changed variables(변경 변수): feature1(특징1) margin-rank score(마진 순위 점수)만 neutral(중립), low penalty 0.15(저마진 벌점 0.15), low penalty 0.25(저마진 벌점 0.25), high bonus 0.10(고마진 보너스 0.10)로 바꾼다.
- stop condition(정지 조건): 4개 variants(변형)를 validation/OOS(검증/표본외) MT5 Strategy Tester(MetaTrader 5 전략 테스터)로 측정하면 Stage238(238단계)은 닫는다.

Effect(효과): cashopen45(현금장 초반 45분), session width(세션 폭), short block off(숏 차단 해제) 실패 축을 반복하지 않고 score shape(점수 형태)만 본다.

## KPI Read(KPI 핵심 성과 지표 판독)

{kpi_table(quality_rows)}

## Judgment(판정)

- best_row(최선 행): `{best.get("adapter_id", "none")}` with validation net(검증 순손익) `{as_float(best, "validation_net"):.2f}`, early PF(초반 수익요인) `{as_float(best, "validation_early_pf"):.6f}`, mid PF(중반 수익요인) `{as_float(best, "validation_mid_pf"):.6f}`, OOS net(표본외 순손익) `{as_float(best, "oos_net"):.2f}`.
- decision(판정): `{decision}`.
- overall_goal_complete(전체 목표 완료): `false`.

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준선).
"""


def decision_markdown(decision: str, external: str) -> str:
    return f"""# Stage238 Decision(238단계 판정)

- decision(판정): `{decision}`
- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- source_stage237_evidence_commit(원천 237단계 근거 커밋): `{SOURCE_STAGE237_EVIDENCE_COMMIT}`
- source_stage237_hash_record_commit(원천 237단계 해시 기록 커밋): `{SOURCE_STAGE237_HASH_RECORD_COMMIT}`
- external_verification_status(외부 검증 상태): `{external}`
- report(보고서): `{rel(REPORT_PATH)}`
- summary_csv(요약 CSV): `{rel(SUMMARY_CSV_PATH)}`
- quality_matrix(품질 행렬): `{rel(QUALITY_MATRIX_PATH)}`
- segment_kpi(구간 KPI 핵심 성과 지표): `{rel(SEGMENT_KPI_PATH)}`
- balance_curve_audit(잔고 곡선 감사): `{rel(BALANCE_CURVE_AUDIT_PATH)}`
- monthly_kpi(월별 KPI 핵심 성과 지표): `{rel(MONTHLY_KPI_PATH)}`
- concentration_risk(집중 위험): `{rel(CONCENTRATION_PATH)}`
- risk_atr_telemetry(위험/ATR 기록): `{rel(RISK_ATR_TELEMETRY_PATH)}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`
- next_stage_or_branch(다음 단계 또는 분기): `{NEXT_STAGE_ID if external == 'completed' else STAGE_ID}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage238(238단계) closeout(종료)는 overall goal complete(전체 목표 완료)가 아니다.

Effect(효과): Stage239(239단계) follow-up review(후속 검토)에서 score shape repair(점수 형태 수리)의 KPI(핵심 성과 지표) 상충과 다음 수리 축을 분리 판정한다.
"""


def write_stage239_seed(decision: str, external: str) -> None:
    if external != "completed":
        return
    write_md(
        NEXT_STAGE_ROOT / "00_spec" / "stage_brief.md",
        f"""# {NEXT_STAGE_ID}

Stage239(239단계)는 Stage238(238단계) score shape repair(점수 형태 수리) 결과를 follow-up review(후속 검토)하는 bounded review(경계 검토) 단계다.

## Bounded Question(경계 질문)

Did Stage238(238단계) score shape repair(점수 형태 수리) recover validation/OOS KPI(검증/표본외 핵심 성과 지표) without damaging equity/balance curve(자본/잔고 곡선), ATR SL/TP(ATR 손절/익절), model-controlled risk%(모델 제어 위험 비율), and segment behavior(구간 행동)?

Effect(효과): Stage238(238단계) 안에서 다음 수리를 흡수하지 않고 score shape(점수 형태) 결과를 별도 review(검토)로 닫는다.

## Boundary(경계)

`{BOUNDARY}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "01_inputs" / "input_refs.md",
        f"""# Stage239 Inputs(239단계 입력)

- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- source_decision(원천 판정): `{decision}`
- report(보고서): `{rel(REPORT_PATH)}`
- summary_csv(요약 CSV): `{rel(SUMMARY_CSV_PATH)}`
- quality_matrix(품질 행렬): `{rel(QUALITY_MATRIX_PATH)}`
- decision_path(판정 파일): `{rel(DECISION_PATH)}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "03_reviews" / "review_index.md",
        f"""# Stage239 Review Index(239단계 검토 색인)

- status(상태): `open_planned_from_stage238`
- source_stage(원천 단계): `{STAGE_ID}`
- source_decision(원천 판정): `{decision}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "04_selected" / "selection_status.md",
        f"""# Stage239 Selection Status(239단계 선택 상태)

- stage_status(단계 상태): `open_planned_from_stage238`
- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- source_decision(원천 판정): `{decision}`
- claim_boundary(주장 경계): `{BOUNDARY}`
""",
    )


def update_current_truth(decision: str, external: str) -> None:
    state = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    active_stage = NEXT_STAGE_ID if external == "completed" else STAGE_ID
    active_run = NEXT_RUN_ID if external == "completed" else RUN_ID
    state = re.sub(r"^\ufeff?current_run_id: .*$", f"current_run_id: {active_run}", state, count=1, flags=re.MULTILINE)
    state = re.sub(r"^active_stage: .*$", f"active_stage: {active_stage}", state, count=1, flags=re.MULTILINE)
    focus = f"""current_focus:
- >-
  Stage238(238단계) closed(종료) as `{decision}` and Stage239(239단계) `{NEXT_STAGE_ID}` is open_planned(개방 계획). Effect(효과): score shape repair(점수 형태 수리)의 KPI(핵심 성과 지표) 상충을 별도 review(검토)로 판정한다.
- >-
  Stage238 evidence(238단계 근거)는 `{rel(REPORT_PATH)}`, `{rel(SUMMARY_CSV_PATH)}`, `{rel(QUALITY_MATRIX_PATH)}`, `{rel(MONTHLY_KPI_PATH)}`, `{rel(CONCENTRATION_PATH)}`, `{rel(RISK_ATR_TELEMETRY_PATH)}`에 있다. Effect(효과): margin rank score(마진 순위 점수)가 validation/OOS(검증/표본외)를 함께 끌어올렸는지 확인한다.
- >-
  Target surface(목표 표면)는 `{TARGET_SURFACE}`이고 legacy 34D(레거시 34D)는 lesson-only KPI target(교훈 전용 핵심 성과 지표 목표)이다. Effect(효과): v2-native research(v2 고유 연구)를 계속한다.

"""
    if re.search(r"(?ms)^current_focus:\r?\n.*?(?=\r?\nstage\d+_)", state):
        state = re.sub(r"(?ms)^current_focus:\r?\n.*?(?=\r?\nstage\d+_)", focus, state, count=1)
    else:
        state = state.rstrip() + "\n" + focus
    state = re.sub(r"(?ms)\nstage238_score_shape_repair_after_threshold_surface_discrete:.*?(?=\nstage\d+_|\Z)", "\n", state)
    state = re.sub(r"(?ms)\nstage239_stage238_score_shape_followup_review:.*?(?=\nstage\d+_|\Z)", "\n", state)
    block = f"""
stage238_score_shape_repair_after_threshold_surface_discrete:
  packet_id: {PACKET_ID}
  stage_id: {STAGE_ID}
  status: closed_{decision if external == "completed" else "blocked_runtime_incomplete"}
  current_run_id: {RUN_ID}
  source_stage: {SOURCE_STAGE_ID}
  source_run: {SOURCE_RUN_ID}
  decision: {decision}
  report_path: {rel(REPORT_PATH)}
  decision_path: {rel(DECISION_PATH)}
  summary_path: {rel(SUMMARY_CSV_PATH)}
  quality_matrix_path: {rel(QUALITY_MATRIX_PATH)}
  monthly_kpi_path: {rel(MONTHLY_KPI_PATH)}
  concentration_path: {rel(CONCENTRATION_PATH)}
  external_verification_status: {external}
  pushed_commit_hash: pending_until_push
  next_action: {NEXT_RUN_ID if external == "completed" else RUN_ID}
  boundary: {BOUNDARY}

stage239_stage238_score_shape_followup_review:
  packet_id: {NEXT_PACKET_ID}
  stage_id: {NEXT_STAGE_ID}
  status: open_planned_from_stage238
  current_run_id: {NEXT_RUN_ID}
  source_stage: {STAGE_ID}
  source_run: {RUN_ID}
  source_decision: {decision}
  next_action: {NEXT_RUN_ID}
  boundary: {BOUNDARY}
"""
    io_path(WORKSPACE_STATE_PATH).write_text(state.rstrip() + "\n" + block, encoding="utf-8-sig")
    write_md(
        CURRENT_WORKING_STATE_PATH,
        f"""# Current Working State(현재 작업 상태)

- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID if external == "completed" else PACKET_ID}`
- current_run(현재 실행): `{active_run}`
- active_stage(활성 단계): `{active_stage}`
- selected_research_baseline(선택 연구 기준선): `none`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- adapter_under_review(검토 중 어댑터): `stage238_score_shape_repair_after_threshold_surface_discrete`
- status(상태): `stage238_{decision}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage238(238단계)는 score shape repair(점수 형태 수리)를 MT5(MetaTrader 5, 메타트레이더5)로 측정했다. Effect(효과): Stage239(239단계)가 결과 상충과 다음 bounded repair(경계 수리)를 별도 review(검토)로 판정한다.

## Latest Stage238 Evidence(최신 238단계 근거)

- run(실행): `{RUN_ID}`
- decision(판정): `{decision}`
- external_verification_status(외부 검증 상태): `{external}`
- report(보고서): `{rel(REPORT_PATH)}`
- summary(요약): `{rel(SUMMARY_CSV_PATH)}`
- quality_matrix(품질 행렬): `{rel(QUALITY_MATRIX_PATH)}`
- monthly_kpi(월별 KPI 핵심 성과 지표): `{rel(MONTHLY_KPI_PATH)}`
- concentration_risk(집중 위험): `{rel(CONCENTRATION_PATH)}`
- risk_atr_telemetry(위험/ATR 기록): `{rel(RISK_ATR_TELEMETRY_PATH)}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준선), legacy_inheritance(레거시 상속), overall_goal_complete(전체 목표 완료).
""",
    )


def write_status_files(decision: str, external: str) -> None:
    status = f"closed_{decision}" if external == "completed" else "blocked_runtime_incomplete"
    write_md(
        SELECTED_ROOT / "selection_status.md",
        f"""# Stage238 Selection Status(238단계 선택 상태)

- stage_status(단계 상태): `{status}`
- current_packet(현재 작업 묶음): `{PACKET_ID}`
- current_run(현재 실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- external_verification_status(외부 검증 상태): `{external}`
- decision(판정): `{decision}`
- next_stage_or_branch(다음 단계 또는 분기): `{NEXT_STAGE_ID if external == 'completed' else STAGE_ID}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`
- claim_boundary(주장 경계): `{BOUNDARY}`
""",
    )
    write_md(
        REVIEWS_ROOT / "review_index.md",
        f"""# Stage238 Review Index(238단계 검토 색인)

- status(상태): `{status}`
- packet(작업 묶음): `{PACKET_ID}`
- run(실행): `{RUN_ID}`
- decision(판정): `{decision}`
- report(보고서): `{rel(REPORT_PATH)}`
- summary(요약): `{rel(SUMMARY_CSV_PATH)}`
- quality_matrix(품질 행렬): `{rel(QUALITY_MATRIX_PATH)}`
- segment_kpi(구간 KPI 핵심 성과 지표): `{rel(SEGMENT_KPI_PATH)}`
- balance_curve_audit(잔고 곡선 감사): `{rel(BALANCE_CURVE_AUDIT_PATH)}`
- monthly_kpi(월별 KPI 핵심 성과 지표): `{rel(MONTHLY_KPI_PATH)}`
- concentration_risk(집중 위험): `{rel(CONCENTRATION_PATH)}`
- risk_atr_telemetry(위험/ATR 기록): `{rel(RISK_ATR_TELEMETRY_PATH)}`
- next_stage_or_branch(다음 단계 또는 분기): `{NEXT_STAGE_ID if external == 'completed' else STAGE_ID}`
""",
    )


def append_changelog(decision: str) -> None:
    existing = io_path(CHANGELOG_PATH).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG_PATH) else ""
    if RUN_ID in existing:
        return
    entry = (
        f"\n## {utc_now()} Stage238 score shape repair closeout(238단계 점수 형태 수리 종료)\n\n"
        f"- action(행동): closed(종료) `{STAGE_ID}` with decision(판정) `{decision}`.\n"
        "- effect(효과): margin rank score(마진 순위 점수)를 MT5(MetaTrader 5, 메타트레이더5)로 측정하고 Stage239(239단계) follow-up review(후속 검토)로 넘겼다.\n"
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
        DECISION_PATH,
        AUDIT_CSV_PATH,
        STAGE_LEDGER_PATH,
    ]
    for execution in result.get("execution_results", []):
        for value in (execution.get("set_path"), execution.get("ini_path"), execution.get("report_path")):
            if value:
                paths.append(Path(str(value)))
    rows: list[dict[str, Any]] = []
    for path in paths:
        if path_exists(path):
            rows.append(
                {
                    "artifact_id": f"{RUN_ID}__{Path(path).name}",
                    "artifact_type": "stage238_score_shape_repair_evidence",
                    "path": rel(path),
                    "sha256": sha256_file_lf_normalized(path),
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "created_at_utc": created,
                    "notes": "Stage238 score shape repair evidence.",
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
    alpha_rows = s172.build_mt5_alpha_ledger_rows(
        run_id=RUN_ID,
        stage_id=STAGE_ID,
        mt5_kpi_records=summary_rows,
        run_output_root=RUN_ROOT,
        external_verification_status=str(result.get("external_verification_status", "")),
    )
    for row in alpha_rows:
        row["parent_run_id"] = row.get("parent_run_id") or PARENT_RUN_ID
        row["scoreboard_lane"] = "baseline_adapter_stage238_score_shape_repair"
        row["judgment"] = decision
        row["status"] = "completed" if result.get("external_verification_status") == "completed" else "blocked"
        row["primary_kpi"] = f"{row.get('primary_kpi', '')};{primary}" if row.get("primary_kpi") else primary
        row["guardrail_kpi"] = f"{row.get('guardrail_kpi', '')};{guardrail}" if row.get("guardrail_kpi") else guardrail
        row["path"] = row.get("path") or rel(REPORT_PATH)
    run_rows = [
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "lane": "baseline_adapter_stage238_score_shape_repair",
            "status": "completed" if result.get("external_verification_status") == "completed" else "blocked",
            "judgment": decision,
            "path": rel(DECISION_PATH),
            "notes": ledger_pairs(
                [
                    ("source_stage237_evidence_commit", SOURCE_STAGE237_EVIDENCE_COMMIT),
                    ("source_stage237_hash_record_commit", SOURCE_STAGE237_HASH_RECORD_COMMIT),
                    ("reference_adapter", SOURCE_REFERENCE_ADAPTER),
                    ("target_surface", TARGET_SURFACE),
                    ("overall_goal_complete", 0),
                ]
            ),
        }
    ]
    run_payload = upsert_csv_rows(RUN_REGISTRY_PATH, RUN_REGISTRY_COLUMNS, run_rows, key="run_id")
    project_payload = upsert_csv_rows(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, alpha_rows, key="ledger_row_id")
    stage_payload = upsert_csv_rows(STAGE_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, alpha_rows, key="ledger_row_id")
    artifact_payload = upsert_csv_rows(ARTIFACT_REGISTRY_PATH, ARTIFACT_COLUMNS, artifacts, key="artifact_id")
    return {
        "run_registry": run_payload,
        "project_alpha_ledger": project_payload,
        "stage_ledger": stage_payload,
        "artifact_registry": artifact_payload,
    }


def write_packet_files(result: Mapping[str, Any], decision: str, ledger_payload: Mapping[str, Any], quality: Sequence[Mapping[str, Any]]) -> None:
    base_payload = {
        "packet_id": PACKET_ID,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "source_stage": SOURCE_STAGE_ID,
        "source_run_id": SOURCE_RUN_ID,
        "decision": decision,
        "external_verification_status": result.get("external_verification_status", ""),
        "quality_rows": list(quality),
        "claim_boundary": BOUNDARY,
        "overall_goal_complete": False,
    }
    files = {
        "result_judgment_gate.json": {
            **base_payload,
            "judgment_label": "score_shape_repair_measured_candidate_not_final",
            "status": "passed_with_boundary",
        },
        "performance_attribution_gate.json": {
            **base_payload,
            "observed_change": "Margin-rank score shape variants measured against Stage235 reference gate.",
            "status": "completed",
        },
        "artifact_lineage_audit.json": {
            **base_payload,
            "producer": rel(PRODUCER_PATH),
            "consumers": [rel(REPORT_PATH), rel(DECISION_PATH), NEXT_STAGE_ID],
            "ledger_payload": ledger_payload,
            "status": "completed",
        },
        "final_claim_guard.json": {
            **base_payload,
            "overall_goal_complete": False,
            "deployment_claim": False,
            "live_readiness_claim": False,
            "runtime_authority_claim": False,
            "production_baseline_claim": False,
            "operating_reference_claim": False,
            "operating_promotion_claim": False,
            "status": "passed",
        },
        "aggregate_summary.json": {
            **base_payload,
            "required_outputs": {
                "report": rel(REPORT_PATH),
                "summary": rel(SUMMARY_CSV_PATH),
                "quality": rel(QUALITY_MATRIX_PATH),
                "decision": rel(DECISION_PATH),
            },
            "ledger_payload": ledger_payload,
            "pushed_commit_hash": "pending_until_push",
        },
        "packet_receipt.json": base_payload,
    }
    for name, payload in files.items():
        write_json(PACKET_ROOT / name, payload)
    write_md(
        PACKET_ROOT / "closeout_packet.md",
        f"""# Stage238 Closeout Packet(238단계 종료 작업 묶음)

- packet(작업 묶음): `{PACKET_ID}`
- run(실행): `{RUN_ID}`
- status(상태): `{result.get('external_verification_status', '')}`
- decision(판정): `{decision}`
- report(보고서): `{rel(REPORT_PATH)}`
- overall_goal_complete(전체 목표 완료): `false`
- boundary(주장 경계): `{BOUNDARY}`
""",
    )


def main(argv: Sequence[str] | None = None) -> int:
    configure_runner()
    s161.configure_base()
    args = s161.parse_args(argv or sys.argv[1:])
    inputs = prepare_inputs(Path(args.common_files_root))
    attempts = build_attempts(inputs)
    prepared = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "stage_number": 238,
        "run_number": RUN_NUMBER,
        "run_root": RUN_ROOT,
        "packet_id": PACKET_ID,
        "attempts": attempts,
        "common_copies": inputs["common_copies"],
        "feature_exports": inputs["feature_exports"],
        "model_artifacts": inputs["model_exports"],
        "route_coverage": s161.base.engine.route_coverage(),
        "model_family": "baseline_adapter_stage238_v2_native_score_shape_repair",
        "feature_set_id": "stage238_signal_margin_rank_plus_reference_side_filter",
        "label_id": "label_v1_fwd12_m5_logret_train_q33_3class",
        "split_contract": "split_v1_calendar_train_20220901_20241231_val_20250101_20250930_oos_20251001_20260413",
        "claim_boundary": BOUNDARY,
        "target_surface": TARGET_SURFACE,
        "gate_rows": inputs["gate_rows"],
    }
    result = load_existing_result_if_requested(args) or s161.base.execute_or_materialize(prepared, args)
    audit_rows = s172.s58.audit_rows_for_result(result, float(args.cost_stress_per_trade)) if result.get("mt5_kpi_records") else []
    risk_rows = s172.s58.risk_rows_from_result(result)
    summary_rows = s172.s58.build_summary_rows(result, audit_rows, risk_rows)
    segment_rows = s172.s58.segment_kpi_rows(summary_rows)
    probability_rows = s161.probability_binding_rows(result)
    model_rows = s161.model_score_rows(inputs)
    balance_rows, monthly_rows, concentration_rows, drawdown_rows = s172.build_curve_audit(summary_rows, segment_rows)
    quality_rows = s172.quality_rows(summary_rows, segment_rows, balance_rows)
    external = str(result.get("external_verification_status") or "blocked")
    decision = decide(quality_rows, external)

    s161.write_run_identity(result, probability_rows, model_rows)
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
    write_csv(TIER_B_DIAGNOSTIC_PATH, tier_b_rows_stage238())
    write_md(REPORT_PATH, report_markdown(quality_rows, decision, external))
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
            "quality_rows": quality_rows,
            "gate_rows": inputs["gate_rows"],
            "legacy_34d": LEGACY_34D,
            "source_stage237_evidence_commit": SOURCE_STAGE237_EVIDENCE_COMMIT,
            "source_stage237_hash_record_commit": SOURCE_STAGE237_HASH_RECORD_COMMIT,
            "claim_boundary": BOUNDARY,
            "overall_goal_complete": False,
        },
    )
    artifacts = artifact_rows(result)
    ledger_payload = write_ledgers(result, decision, artifacts)
    write_packet_files(result, decision, ledger_payload, quality_rows)
    write_stage239_seed(decision, external)
    update_current_truth(decision, external)
    write_status_files(decision, external)
    append_changelog(decision)
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
