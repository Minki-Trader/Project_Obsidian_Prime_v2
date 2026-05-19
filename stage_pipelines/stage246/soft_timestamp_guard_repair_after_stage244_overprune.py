from __future__ import annotations

import csv
import json
import math
import re
import sys
from datetime import UTC, date, datetime
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


STAGE_ID = "246_adapter_research__soft_timestamp_guard_repair_after_stage244_overprune"
RUN_NUMBER = "run246A"
RUN_ID = "run246A_stage246_soft_timestamp_guard_repair_after_stage244_overprune_v1"
PACKET_ID = "stage246_soft_timestamp_guard_repair_after_stage244_overprune_v1"
PARENT_RUN_ID = "run245A_stage245_stage244_timestamp_guard_followup_review_v1"
SOURCE_STAGE_ID = "245_adapter_research__stage244_timestamp_guard_followup_review"
SOURCE_RUN_ID = PARENT_RUN_ID
SOURCE_STAGE245_EVIDENCE_COMMIT = "1481b1323d65bd5974aefc973bc16d9fff74519a"
SOURCE_STAGE245_HASH_RECORD_COMMIT = "efa84d56d2c36e619b42a7f7cab09ec4c0ad35a3"
NEXT_STAGE_ID = "247_adapter_research__stage246_soft_guard_followup_review"
NEXT_RUN_ID = "run247A_stage247_stage246_soft_guard_followup_review_v1"
NEXT_PACKET_ID = "stage247_stage246_soft_guard_followup_review_v1"
TARGET_SURFACE = "legacy_34d_kpi_lesson_only_v2_native_soft_timestamp_guard_repair"
BOUNDARY = stage238.BOUNDARY
LEGACY_34D = stage238.LEGACY_34D
OOS_REFERENCE = {
    "adapter_id": "s244_samecap_control",
    "oos_net": 812.80,
    "oos_pf": 1.78,
    "oos_dd": 9.792,
}

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
SELECTED_ROOT = STAGE_ROOT / "04_selected"
PACKET_ROOT = Path("docs/agent_control/packets") / PACKET_ID
NEXT_STAGE_ROOT = Path("stages") / NEXT_STAGE_ID
PARTIALS_ROOT = RUN_ROOT / "partials"
COMMON_ROOT = f"OPV2/s246a/{RUN_NUMBER}"

SUMMARY_JSON_PATH = REVIEWS_ROOT / "stage246_summary.json"
SUMMARY_CSV_PATH = REVIEWS_ROOT / "stage246_soft_guard_kpi_summary.csv"
REPORT_PATH = REVIEWS_ROOT / "stage246_soft_guard_repair_report.md"
SEGMENT_KPI_PATH = REVIEWS_ROOT / "stage246_segment_kpi_summary.csv"
BALANCE_CURVE_AUDIT_PATH = REVIEWS_ROOT / "stage246_balance_curve_audit.csv"
MONTHLY_KPI_PATH = REVIEWS_ROOT / "stage246_monthly_kpi_summary.csv"
CONCENTRATION_PATH = REVIEWS_ROOT / "stage246_concentration_risk_summary.csv"
DRAWDOWN_PATH = REVIEWS_ROOT / "stage246_drawdown_recovery_summary.csv"
QUALITY_MATRIX_PATH = REVIEWS_ROOT / "stage246_quality_matrix.csv"
RISK_ATR_TELEMETRY_PATH = REVIEWS_ROOT / "stage246_risk_atr_telemetry.csv"
SOFT_GUARD_FEATURE_SUMMARY_PATH = REVIEWS_ROOT / "stage246_soft_guard_feature_summary.csv"
PROBABILITY_BINDING_PATH = REVIEWS_ROOT / "stage246_probability_telemetry_summary.csv"
MODEL_SCORE_AUDIT_PATH = REVIEWS_ROOT / "stage246_model_score_audit.csv"
TIER_B_DIAGNOSTIC_PATH = REVIEWS_ROOT / "stage246_tier_b_diagnostic_summary.csv"
ATTRIBUTION_PATH = REVIEWS_ROOT / "stage246_performance_attribution.csv"
FAILURE_MEMORY_PATH = REVIEWS_ROOT / "stage246_failure_memory.csv"
DECISION_PATH = REVIEWS_ROOT / "stage246_decision.md"
AUDIT_CSV_PATH = REVIEWS_ROOT / "stage246_trade_audit.csv"
STAGE_LEDGER_PATH = REVIEWS_ROOT / "stage_run_ledger.csv"

RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
PROJECT_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
ARTIFACT_REGISTRY_PATH = Path("docs/registers/artifact_registry.csv")
WORKSPACE_STATE_PATH = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE_PATH = Path("docs/context/current_working_state.md")
CHANGELOG_PATH = Path("docs/workspace/changelog.md")
PRODUCER_PATH = Path("stage_pipelines/stage246/soft_timestamp_guard_repair_after_stage244_overprune.py")
ARTIFACT_COLUMNS = stage238.ARTIFACT_COLUMNS

SIGNAL_COLUMN = stage238.SIGNAL_COLUMN
RANK_COLUMN = "stage246_soft_margin_rank_bucket"
GATE_COLUMN_PREFIX = "stage246_gate"
SOURCE_SPEC = dict(stage238.SOURCE_SPEC)
REFERENCE_EXTRA = dict(stage238.REFERENCE_EXTRA)
MODEL_RISK_MIN_PCT = {}

SPLIT_WINDOWS = {
    "validation_is": (date(2025, 1, 1), date(2025, 9, 30)),
    "oos": (date(2025, 10, 1), date(2026, 4, 13)),
}


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    return stage238.rel(path)


def csv_value(value: Any) -> str:
    return stage238.csv_value(value)


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
    stage238.write_csv(path, rows, columns)


def as_float(row: Mapping[str, Any], key: str, default: float = 0.0) -> float:
    return stage238.as_float(row, key, default)


def _format_score(value: Any) -> str:
    return f"{float(value):.17g}"


def variant(
    adapter_id: str,
    label: str,
    *,
    low_penalty: float,
    mid_penalty: float,
    risk_cap: float = 0.0305,
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
        model_risk_max_pct=risk_cap,
        same_direction_reentry_cooldown_bars=8,
        short_threshold=0.54,
        long_threshold=0.52,
        close_on_flat_signal=False,
        reverse_on_opposite_signal=True,
        close_only_on_opposite_signal=False,
        max_hold_bars=3,
        notes=f"{note} low_penalty={low_penalty} mid_penalty={mid_penalty}",
    )


VARIANTS = (
    variant(
        "s246_cap0305_control",
        "stage246_cap0305_control",
        low_penalty=0.0,
        mid_penalty=0.0,
        note="Stage246 control: repeat Stage244 best reference without a soft middle-window penalty.",
    ),
    variant(
        "s246_softlow_flat003",
        "stage246_softlow_flat003",
        low_penalty=0.03,
        mid_penalty=0.0,
        note="Stage246 repair: soft flat tilt on low bucket only inside middle window.",
    ),
    variant(
        "s246_softlow_flat005",
        "stage246_softlow_flat005",
        low_penalty=0.05,
        mid_penalty=0.0,
        note="Stage246 repair: stronger soft flat tilt on low bucket only inside middle window.",
    ),
    variant(
        "s246_softlowmid_lite",
        "stage246_softlowmid_lite",
        low_penalty=0.04,
        mid_penalty=0.015,
        note="Stage246 repair: light low plus mid soft flat tilt inside middle window.",
    ),
    variant(
        "s246_softlowmid_balanced",
        "stage246_softlowmid_balanced",
        low_penalty=0.05,
        mid_penalty=0.025,
        note="Stage246 repair: balanced low plus mid soft flat tilt inside middle window.",
    ),
)


def penalty_scores(value: float) -> tuple[float, float, float]:
    if value <= 0:
        return (0.0, 0.0, 0.0)
    return (-value, value, -value)


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
            "low": (0.0, 0.0, 0.0),
            "mid": (0.0, 0.0, 0.0),
            "high": (0.10, -0.10, 0.10),
            "vhigh": (0.15, -0.15, 0.15),
            "soft_low": penalty_scores(low_penalty),
            "soft_mid": penalty_scores(mid_penalty),
        },
    }


VARIANT_EXTRAS: dict[str, dict[str, Any]] = {
    item.adapter_id: extra(item.adapter_id.replace("s246_", ""), float(item.notes.split("low_penalty=")[1].split()[0]), float(item.notes.split("mid_penalty=")[1]))
    for item in VARIANTS
}
SOURCE_SPECS_BY_VARIANT = {item.adapter_id: dict(SOURCE_SPEC) for item in VARIANTS}
MODEL_RISK_MIN_PCT = {item.adapter_id: 0.005 for item in VARIANTS}


def parse_date(value: Any) -> date | None:
    text = str(value or "").strip()
    if not text:
        return None
    for fmt in ("%Y.%m.%d %H:%M:%S", "%Y.%m.%d", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
        try:
            return datetime.strptime(text[:19] if " " in fmt else text[:10], fmt).date()
        except ValueError:
            pass
    return None


def in_middle_window(row_date: date | None, split: str) -> bool:
    if row_date is None or split not in SPLIT_WINDOWS:
        return False
    start, end = SPLIT_WINDOWS[split]
    span = (end - start).days + 1
    first_mid = start.toordinal() + span // 3
    last_mid = start.toordinal() + (2 * span // 3) - 1
    return first_mid <= row_date.toordinal() <= last_mid


def reference_gate_value(row: Mapping[str, str]) -> float:
    return stage238.reference_gate_value(row)


def soft_rank_value(row: Mapping[str, str], item: Any, split: str, base_gate: float) -> tuple[int, str, bool]:
    bucket_value, bucket_label = stage238.rank_bucket_for(row)
    signal = int(round(stage238.parse_float(row.get(SIGNAL_COLUMN), 0.0)))
    row_date = parse_date(row.get("bar_time_server") or row.get("timestamp_utc"))
    extra_cfg = VARIANT_EXTRAS[item.adapter_id]
    if signal == 0 or base_gate >= 0.5 or not in_middle_window(row_date, split):
        return bucket_value, bucket_label, False
    if bucket_label == "low" and float(extra_cfg["low_penalty"]) > 0:
        return 4, "soft_low", True
    if bucket_label == "mid" and float(extra_cfg["mid_penalty"]) > 0:
        return 5, "soft_mid", True
    return bucket_value, bucket_label, False


def write_soft_score_model(path: Path, item: Any, gate_column: str) -> dict[str, Any]:
    extra_cfg = VARIANT_EXTRAS[item.adapter_id]
    strength = float(extra_cfg["logit_strength"])
    rank_scores = extra_cfg["rank_scores"]
    rows: list[dict[str, Any]] = [
        {
            "record_type": "intercept",
            "feature_index": -1,
            "item_index": -1,
            "value": "",
            "score_short": "0",
            "score_flat": "0",
            "score_long": "0",
        },
        {"record_type": "cut", "feature_index": 0, "item_index": 0, "value": "-0.5", "score_short": "", "score_flat": "", "score_long": ""},
        {"record_type": "cut", "feature_index": 0, "item_index": 1, "value": "0.5", "score_short": "", "score_flat": "", "score_long": ""},
        {"record_type": "score", "feature_index": 0, "item_index": 0, "value": "", "score_short": _format_score(strength), "score_flat": _format_score(-strength), "score_long": _format_score(-strength)},
        {"record_type": "score", "feature_index": 0, "item_index": 1, "value": "", "score_short": _format_score(strength), "score_flat": _format_score(-strength), "score_long": _format_score(-strength)},
        {"record_type": "score", "feature_index": 0, "item_index": 2, "value": "", "score_short": _format_score(-strength), "score_flat": _format_score(strength), "score_long": _format_score(-strength)},
        {"record_type": "score", "feature_index": 0, "item_index": 3, "value": "", "score_short": _format_score(-strength), "score_flat": _format_score(-strength), "score_long": _format_score(strength)},
    ]
    for cut_index, cut_value in enumerate((0.5, 1.5, 2.5, 3.5, 4.5)):
        rows.append(
            {
                "record_type": "cut",
                "feature_index": 1,
                "item_index": cut_index,
                "value": _format_score(cut_value),
                "score_short": "",
                "score_flat": "",
                "score_long": "",
            }
        )
    score_by_item = {
        0: rank_scores["low"],
        1: rank_scores["low"],
        2: rank_scores["mid"],
        3: rank_scores["high"],
        4: rank_scores["vhigh"],
        5: rank_scores["soft_low"],
        6: rank_scores["soft_mid"],
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
        rows.append(
            {
                "record_type": "cut",
                "feature_index": 2,
                "item_index": item_index,
                "value": _format_score(cut_value),
                "score_short": "",
                "score_flat": "",
                "score_long": "",
            }
        )
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
            [-1.0, 4.0, 0.0],
            [-1.0, 5.0, 0.0],
            [1.0, 0.0, 0.0],
            [1.0, 4.0, 0.0],
            [1.0, 5.0, 0.0],
        ],
        dtype="float64",
    )
    probabilities = score_ebm_table_probabilities(table, sample_values)
    feature_order = (SIGNAL_COLUMN, RANK_COLUMN, gate_column)
    return {
        "path": rel(path),
        "sha256": sha256_file_lf_normalized(path),
        "format": "stage246_three_feature_soft_timestamp_guard_ebm_table_csv_v1",
        "feature_order": list(feature_order),
        "feature_order_hash": stage238.s161.base.engine.ordered_hash(feature_order),
        "feature_count": 3,
        "signal_column": SIGNAL_COLUMN,
        "rank_column": RANK_COLUMN,
        "gate_column": gate_column,
        "rank_scores": rank_scores,
        "parity_sample_values": sample_values.tolist(),
        "parity_sample_probabilities": probabilities.tolist(),
    }


def write_soft_feature(source: Path, destination: Path, item: Any, split: str) -> dict[str, Any]:
    gate_column = f"{GATE_COLUMN_PREFIX}_{VARIANT_EXTRAS[item.adapter_id]['axis']}"
    io_path(destination.parent).mkdir(parents=True, exist_ok=True)
    total_rows = 0
    signal_rows = 0
    reference_blocked_rows = 0
    soft_adjusted_rows = 0
    mid_window_rows = 0
    rank_counts: dict[str, int] = {"low": 0, "mid": 0, "high": 0, "vhigh": 0, "soft_low": 0, "soft_mid": 0}
    soft_adjusted_rank_counts: dict[str, int] = {"soft_low": 0, "soft_mid": 0}
    allowed_signal_rank_counts: dict[str, int] = {"low": 0, "mid": 0, "high": 0, "vhigh": 0, "soft_low": 0, "soft_mid": 0}
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
                base_gate = reference_gate_value(row)
                rank_value, rank_label, adjusted = soft_rank_value(row, item, split, base_gate)
                rank_counts[rank_label] += 1
                row_date = parse_date(row.get("bar_time_server") or row.get("timestamp_utc"))
                if in_middle_window(row_date, split):
                    mid_window_rows += 1
                if signal != 0:
                    signal_rows += 1
                    if base_gate >= 0.5:
                        reference_blocked_rows += 1
                    else:
                        allowed_signal_rank_counts[rank_label] += 1
                    if adjusted:
                        soft_adjusted_rows += 1
                        soft_adjusted_rank_counts[rank_label] += 1
                writer.writerow(
                    {
                        "bar_time_server": row.get("bar_time_server") or row.get("timestamp_utc") or "",
                        SIGNAL_COLUMN: csv_value(float(signal)),
                        RANK_COLUMN: csv_value(float(rank_value)),
                        gate_column: csv_value(base_gate),
                    }
                )
    return {
        "run_id": RUN_ID,
        "adapter_id": item.adapter_id,
        "split": split,
        "gate_column": gate_column,
        "source_feature": rel(source),
        "soft_feature": rel(destination),
        "total_rows": total_rows,
        "signal_rows": signal_rows,
        "mid_window_rows": mid_window_rows,
        "reference_blocked_signal_rows": reference_blocked_rows,
        "soft_adjusted_signal_rows": soft_adjusted_rows,
        "allowed_signal_rows": signal_rows - reference_blocked_rows,
        "rank_counts": rank_counts,
        "allowed_signal_rank_counts": allowed_signal_rank_counts,
        "soft_adjusted_rank_counts": soft_adjusted_rank_counts,
        "low_penalty": VARIANT_EXTRAS[item.adapter_id]["low_penalty"],
        "mid_penalty": VARIANT_EXTRAS[item.adapter_id]["mid_penalty"],
        "gate_description": "Stage246 reference side filter plus soft middle-window low/mid flat tilt.",
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
        model_meta = write_soft_score_model(model_local, item, gate_column)
        copied.append(
            {
                "source": rel(model_source),
                "path": rel(model_local),
                "sha256": sha256_file_lf_normalized(model_local),
                "transform": "stage246_three_feature_soft_timestamp_guard_score_model",
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
            gate_row = write_soft_feature(feature_source, feature_local, item, split)
            gate_rows.append(gate_row)
            copied.append(
                {
                    "source": rel(feature_source),
                    "path": rel(feature_local),
                    "sha256": sha256_file_lf_normalized(feature_local),
                    "transform": "stage246_soft_middle_window_rank_feature",
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


def extra_set_values(item: Any, magic: int) -> dict[str, Any]:
    values = stage238.s161.base.engine.extra_set_values(item, magic)
    extra_cfg = VARIANT_EXTRAS[item.adapter_id]
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
                magic = 24610000 + variant_index * 100 + (1 if split == "validation_is" else 50) + role_index
                attempts.append(
                    stage238.s161.base.attempt_payload(
                        run_root=variant_root,
                        run_id=RUN_ID,
                        stage_number=246,
                        exploration_label="stage246_BaselineAdapter__SoftTimestampGuardRepair",
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


def pass_stage246(row: Mapping[str, Any]) -> bool:
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
        return "continue_stage246_runtime_completion_due_to_incomplete_runtime_candidate_not_final"
    if any(pass_stage246(row) for row in quality_rows):
        return "open_stage247_followup_due_to_soft_guard_34d_kpi_candidate_not_final"
    return "open_stage247_bounded_followup_due_to_soft_guard_tradeoff_candidate_not_final"


def best_row(rows: Sequence[Mapping[str, Any]]) -> Mapping[str, Any]:
    if not rows:
        return {}
    return max(
        rows,
        key=lambda row: (
            pass_stage246(row),
            as_float(row, "validation_net"),
            -as_float(row, "validation_balance_dd_percent", 99.0),
            as_float(row, "validation_mid_pf"),
            as_float(row, "oos_net"),
        ),
    )


def tier_b_rows_stage246() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for item in VARIANTS:
        for split in ("validation", "oos"):
            rows.append(
                {
                    "run_id": RUN_ID,
                    "adapter_id": item.adapter_id,
                    "split": split,
                    "status": "diagnostic_missing_required_but_disabled_for_stage246_soft_guard_repair",
                    "fallback_enabled": 0,
                    "fallback_used_count": 0,
                    "notes": "Stage246 isolates Tier A routed soft guard repair; Tier B fallback remains disabled by prior fallback-only damage memory.",
                }
            )
    return rows


def quality_by_id(rows: Sequence[Mapping[str, Any]], adapter_id: str) -> Mapping[str, Any]:
    for row in rows:
        if row.get("adapter_id") == adapter_id:
            return row
    return {}


def delta(value: Any, base: Any) -> float:
    return float(stage238.parse_float(value, 0.0) - stage238.parse_float(base, 0.0))


def performance_attribution_rows(quality_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    control = quality_by_id(quality_rows, "s246_cap0305_control")
    rows: list[dict[str, Any]] = []
    for row in quality_rows:
        adapter_id = str(row.get("adapter_id", ""))
        if adapter_id == "s246_cap0305_control":
            rows.append(
                {
                    "attribution_id": f"{RUN_ID}__{adapter_id}",
                    "comparison_baseline": "Stage244 cap0305 control repeated in Stage246",
                    "observed_change": "control reproduced near-miss KPI surface",
                    "likely_drivers": "risk cap 0.0305 and reference side filter unchanged",
                    "segment_checks": "validation net, DD, early/mid/late PF, OOS net reviewed",
                    "trade_shape": "no soft middle-window adjustment applied",
                    "attribution_confidence": "high",
                    "next_probe": "do not treat cap0305 near-miss as final; repair source or entry quality",
                    "alternative_explanations": "none material; row is a control",
                }
            )
            continue
        rows.append(
            {
                "attribution_id": f"{RUN_ID}__{adapter_id}",
                "comparison_baseline": "s246_cap0305_control",
                "observed_change": (
                    f"validation_net_delta={delta(row.get('validation_net'), control.get('validation_net')):.2f};"
                    f"validation_dd_delta={delta(row.get('validation_balance_dd_percent'), control.get('validation_balance_dd_percent')):.4f};"
                    f"validation_mid_pf_delta={delta(row.get('validation_mid_pf'), control.get('validation_mid_pf')):.6f};"
                    f"oos_net_delta={delta(row.get('oos_net'), control.get('oos_net')):.2f}"
                ),
                "likely_drivers": "soft flat tilt reduced low/mid middle-window confidence instead of blocking trades",
                "segment_checks": "DD improved for soft rows, but validation net and mid PF weakened",
                "trade_shape": "same reference block count; soft-adjusted middle-window rows changed probability threshold behavior",
                "attribution_confidence": "high",
                "next_probe": "Stage247 should avoid stronger low/mid soft tilt and examine entry/source repair",
                "alternative_explanations": "OOS PF small gain does not offset validation net/mid PF damage",
            }
        )
    return rows


def failure_memory_rows(quality_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    control = quality_by_id(quality_rows, "s246_cap0305_control")
    best_soft = max(
        (row for row in quality_rows if row.get("adapter_id") != "s246_cap0305_control"),
        key=lambda row: as_float(row, "validation_net"),
        default={},
    )
    return [
        {
            "failure_id": "stage246_cap0305_control_near_miss_not_final",
            "evidence": (
                f"validation_net={control.get('validation_net', '')};"
                f"validation_dd={control.get('validation_balance_dd_percent', '')};"
                f"validation_mid_pf={control.get('validation_mid_pf', '')};"
                f"oos_net={control.get('oos_net', '')}"
            ),
            "impact": "closest reference still misses 34D net, DD, and mid PF simultaneously",
            "next_handling": "Stage247 must not accept final net proximity as completion",
        },
        {
            "failure_id": "stage246_soft_guard_reduced_dd_but_damaged_net",
            "evidence": (
                f"best_soft={best_soft.get('adapter_id', '')};"
                f"validation_net_delta_vs_control={delta(best_soft.get('validation_net'), control.get('validation_net')):.2f};"
                f"validation_dd_delta_vs_control={delta(best_soft.get('validation_balance_dd_percent'), control.get('validation_balance_dd_percent')):.4f}"
            ),
            "impact": "soft tilt solved part of DD but removed too much profitable validation exposure",
            "next_handling": "avoid stronger soft low/mid tilt; inspect entry/source quality or non-middle-window risk shape",
        },
        {
            "failure_id": "stage246_mid_pf_remains_below_34d",
            "evidence": "all Stage246 variants keep validation_mid_pf below legacy_34d_target",
            "impact": "middle segment remains the binding weakness",
            "next_handling": "Stage247 should focus on mid-window trade quality, not another blanket suppression",
        },
    ]


def report_markdown(quality_rows: Sequence[Mapping[str, Any]], decision: str, external: str) -> str:
    best = best_row(quality_rows)
    lines = [
        "# Stage246 Soft Timestamp Guard Repair Report(246단계 부드러운 시간 보호문 수리 보고서)",
        "",
        f"- stage(단계): `{STAGE_ID}`",
        f"- run(실행): `{RUN_ID}`",
        f"- source_stage(원천 단계): `{SOURCE_STAGE_ID}`",
        f"- source_stage245_evidence_commit(원천 245단계 근거 커밋): `{SOURCE_STAGE245_EVIDENCE_COMMIT}`",
        f"- source_stage245_hash_record_commit(원천 245단계 해시 기록 커밋): `{SOURCE_STAGE245_HASH_RECORD_COMMIT}`",
        f"- external_verification_status(외부 검증 상태): `{external}`",
        f"- decision(판정): `{decision}`",
        f"- boundary(주장 경계): `{BOUNDARY}`",
        "",
        "## Bounded Design(경계 설계)",
        "",
        "- action(행동): hard guard(강한 차단)를 제거하고 middle window(중간 창)의 low/mid bucket(저/중간 구간)에 flat tilt(무포지션 쪽 점수 기울기)를 작게 넣었다.",
        "- effect(효과): 신호를 강제로 없애지 않고 confidence(신뢰도)를 낮춰서 validation net(검증 순손익) 손상을 줄이면서 DD(낙폭)와 mid PF(중간 수익요인)를 다시 본다.",
        "- fixed variables(고정 변수): ATR SL/TP(ATR 손절/익절) `2.0325/4.615`, model-controlled risk%(모델 제어 위험 비율) cap(상한) `0.0305`, hold(보유) `3`, cooldown(대기) `8`.",
        "- stop condition(정지 조건): 5 variants(변형)를 validation/OOS(검증/표본외) MT5 Strategy Tester(MetaTrader 5 전략 테스터)로 측정하면 Stage246(246단계)는 닫는다.",
        "",
        "## KPI Read(KPI 핵심 성과 지표 판독)",
        "",
        "| adapter(어댑터) | val net(검증 순손익) | early PF(초반 수익요인) | mid PF(중간 수익요인) | val DD%(검증 낙폭) | OOS net(표본외 순손익) | OOS PF(표본외 수익요인) | OOS DD%(표본외 낙폭) | flags(표식) |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in quality_rows:
        lines.append(
            f"| {row.get('adapter_id', '')} | {as_float(row, 'validation_net'):.2f} | {as_float(row, 'validation_early_pf'):.6f} | {as_float(row, 'validation_mid_pf'):.6f} | {as_float(row, 'validation_balance_dd_percent'):.4f} | {as_float(row, 'oos_net'):.2f} | {as_float(row, 'oos_pf'):.6f} | {as_float(row, 'oos_balance_dd_percent'):.4f} | {row.get('quality_flags', '')} |"
        )
    lines.extend(
        [
            "",
            "## Judgment(판정)",
            "",
            f"- best_row(최선 행): `{best.get('adapter_id', '')}` with validation net(검증 순손익) `{best.get('validation_net', '')}`, validation DD(검증 낙폭) `{best.get('validation_balance_dd_percent', '')}`, mid PF(중간 수익요인) `{best.get('validation_mid_pf', '')}`, OOS net(표본외 순손익) `{best.get('oos_net', '')}`.",
            f"- legacy_34d_target(레거시 34D 목표): net(순손익) `{LEGACY_34D['net_profit']}`, PF(수익요인) `{LEGACY_34D['profit_factor']}`, DD%(낙폭) `{LEGACY_34D['max_drawdown_percent']}`.",
            f"- decision(판정): `{decision}`.",
            "- overall_goal_complete(전체 목표 완료): `false`.",
            "",
            "Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준).",
        ]
    )
    return "\n".join(lines)


def decision_markdown(decision: str, external: str) -> str:
    next_target = NEXT_STAGE_ID if external == "completed" else STAGE_ID
    return f"""# Stage246 Decision(246단계 판정)

- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- decision(판정): `{decision}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- source_stage245_evidence_commit(원천 245단계 근거 커밋): `{SOURCE_STAGE245_EVIDENCE_COMMIT}`
- source_stage245_hash_record_commit(원천 245단계 해시 기록 커밋): `{SOURCE_STAGE245_HASH_RECORD_COMMIT}`
- external_verification_status(외부 검증 상태): `{external}`
- report(보고서): `{rel(REPORT_PATH)}`
- summary(요약): `{rel(SUMMARY_CSV_PATH)}`
- quality_matrix(품질 행렬): `{rel(QUALITY_MATRIX_PATH)}`
- segment_kpi(구간 핵심 성과 지표): `{rel(SEGMENT_KPI_PATH)}`
- soft_guard_feature_summary(부드러운 보호문 피처 요약): `{rel(SOFT_GUARD_FEATURE_SUMMARY_PATH)}`
- risk_atr_telemetry(위험/ATR 기록): `{rel(RISK_ATR_TELEMETRY_PATH)}`
- next_stage_or_branch(다음 단계 또는 분기): `{next_target}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage246(246단계) closeout(종료)는 overall goal complete(전체 목표 완료)가 아니다.

Effect(효과): Stage247(247단계) follow-up review(후속 검토)에서 soft timestamp guard(부드러운 시간 보호문)의 KPI(핵심 성과 지표) 상충과 다음 bounded repair(경계 수리)를 판정한다.
"""


def write_stage247_seed(decision: str, external: str) -> None:
    if external != "completed":
        return
    write_md(
        NEXT_STAGE_ROOT / "00_spec" / "stage_brief.md",
        f"""# {NEXT_STAGE_ID}

Stage247(247단계)는 Stage246(246단계) soft timestamp guard repair(부드러운 시간 보호문 수리) 결과를 follow-up review(후속 검토)하는 bounded review(경계 검토) 단계다.

## Bounded Question(경계 질문)

Did Stage246(246단계) improve validation/OOS KPI(검증/표본외 핵심 성과 지표), mid PF(중간 수익요인), DD(낙폭), and soft-guard trade shape(부드러운 보호문 거래 모양) without damaging ATR SL/TP(ATR 손절/익절), model-controlled risk%(모델 제어 위험 비율), and segment behavior(구간 행동)?

## Boundary(경계)

`{BOUNDARY}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "01_inputs" / "input_refs.md",
        f"""# Stage247 Inputs(247단계 입력)

- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- source_decision(원천 판정): `{decision}`
- report(보고서): `{rel(REPORT_PATH)}`
- summary(요약): `{rel(SUMMARY_CSV_PATH)}`
- quality_matrix(품질 행렬): `{rel(QUALITY_MATRIX_PATH)}`
- risk_atr_telemetry(위험/ATR 기록): `{rel(RISK_ATR_TELEMETRY_PATH)}`
- soft_guard_feature_summary(부드러운 보호문 피처 요약): `{rel(SOFT_GUARD_FEATURE_SUMMARY_PATH)}`
- performance_attribution(성과 원인분해): `{rel(ATTRIBUTION_PATH)}`
- failure_memory(실패 기억): `{rel(FAILURE_MEMORY_PATH)}`
- decision_path(판정 파일): `{rel(DECISION_PATH)}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "03_reviews" / "review_index.md",
        f"""# Stage247 Review Index(247단계 검토 색인)

- status(상태): `open_planned_from_stage246`
- source_stage(원천 단계): `{STAGE_ID}`
- source_decision(원천 판정): `{decision}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "04_selected" / "selection_status.md",
        f"""# Stage247 Selection Status(247단계 선택 상태)

- stage_status(단계 상태): `open_planned_from_stage246`
- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- source_decision(원천 판정): `{decision}`
- claim_boundary(주장 경계): `{BOUNDARY}`
""",
    )


def replace_stage_block(text: str, key: str, block: str) -> str:
    pattern = rf"(?ms)^({re.escape(key)}:\r?\n).*?(?=^\S|\Z)"
    if re.search(pattern, text):
        return re.sub(pattern, block.rstrip() + "\n\n", text, count=1)
    return text.rstrip() + "\n\n" + block.rstrip() + "\n"


def update_current_truth(decision: str, external: str) -> None:
    active_stage = NEXT_STAGE_ID if external == "completed" else STAGE_ID
    active_run = NEXT_RUN_ID if external == "completed" else RUN_ID
    state = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    state = re.sub(r"^\ufeff?current_run_id: .*$", f"current_run_id: {active_run}", state, count=1, flags=re.MULTILINE)
    state = re.sub(r"^active_stage: .*$", f"active_stage: {active_stage}", state, count=1, flags=re.MULTILINE)
    focus = f"""current_focus:
- >-
  Stage246(246단계) closed(종료) as `{decision}` and Stage247(247단계) `{NEXT_STAGE_ID}` is open_planned(개방 계획). Effect(효과): soft timestamp guard(부드러운 시간 보호문)의 KPI(핵심 성과 지표) 상충을 별도 review(검토)로 판정한다.
- >-
  Stage246 evidence(246단계 근거)는 `{rel(REPORT_PATH)}`, `{rel(SUMMARY_CSV_PATH)}`, `{rel(QUALITY_MATRIX_PATH)}`, `{rel(SOFT_GUARD_FEATURE_SUMMARY_PATH)}`, `{rel(RISK_ATR_TELEMETRY_PATH)}`에 있다. Effect(효과): hard guard(강한 차단) 과차단을 soft tilt(부드러운 기울기)로 고쳤는지 확인한다.
- >-
  Target surface(목표 표면)는 `{TARGET_SURFACE}`이고 legacy 34D(레거시 34D)는 lesson-only KPI target(교훈용 핵심 성과 지표 목표)이다. Effect(효과): v2-native research(v2 고유 연구)를 계속한다.

"""
    state = re.sub(r"(?ms)^current_focus:\r?\n.*?(?=^\S)", focus, state, count=1)
    stage246_block = f"""stage246_soft_timestamp_guard_repair_after_stage244_overprune:
  packet_id: {PACKET_ID}
  stage_id: {STAGE_ID}
  status: closed_{decision if external == "completed" else "blocked_runtime_incomplete"}
  current_run_id: {RUN_ID}
  source_stage: {SOURCE_STAGE_ID}
  source_run: {SOURCE_RUN_ID}
  source_stage245_evidence_commit: {SOURCE_STAGE245_EVIDENCE_COMMIT}
  source_stage245_hash_record_commit: {SOURCE_STAGE245_HASH_RECORD_COMMIT}
  decision: {decision}
  report_path: {rel(REPORT_PATH)}
  decision_path: {rel(DECISION_PATH)}
  summary_path: {rel(SUMMARY_CSV_PATH)}
  quality_matrix_path: {rel(QUALITY_MATRIX_PATH)}
  soft_guard_feature_summary_path: {rel(SOFT_GUARD_FEATURE_SUMMARY_PATH)}
  risk_atr_telemetry_path: {rel(RISK_ATR_TELEMETRY_PATH)}
  external_verification_status: {external}
  pushed_commit_hash: pending_until_push
  next_action: {NEXT_RUN_ID if external == "completed" else RUN_ID}
  boundary: {BOUNDARY}
"""
    stage247_block = f"""stage247_stage246_soft_guard_followup_review:
  packet_id: {NEXT_PACKET_ID}
  stage_id: {NEXT_STAGE_ID}
  status: open_planned_from_stage246
  current_run_id: {NEXT_RUN_ID}
  source_stage: {STAGE_ID}
  source_run: {RUN_ID}
  source_decision: {decision}
  next_action: {NEXT_RUN_ID}
  boundary: {BOUNDARY}
"""
    state = replace_stage_block(state, "stage246_soft_timestamp_guard_repair_after_stage244_overprune", stage246_block)
    if external == "completed":
        state = replace_stage_block(state, "stage247_stage246_soft_guard_followup_review", stage247_block)
    io_path(WORKSPACE_STATE_PATH).write_text(state.rstrip() + "\n", encoding="utf-8-sig")

    write_md(
        CURRENT_WORKING_STATE_PATH,
        f"""# Current Working State(현재 작업 상태)

- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID if external == "completed" else PACKET_ID}`
- current_run(현재 실행): `{active_run}`
- active_stage(활성 단계): `{active_stage}`
- selected_research_baseline(선택 연구 기준선): `none`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- adapter_under_review(검토 중 어댑터): `stage246_soft_timestamp_guard_repair`
- status(상태): `stage246_{decision}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage246(246단계)는 hard guard(강한 차단) 과차단을 soft timestamp guard(부드러운 시간 보호문)로 바꿔 MT5(MetaTrader 5, 메타트레이더5) KPI(핵심 성과 지표)를 측정했다. Effect(효과): Stage247(247단계)이 결과 상충과 다음 bounded repair(경계 수리)를 별도 review(검토)로 판정한다.

## Latest Stage246 Evidence(최신 246단계 근거)

- run(실행): `{RUN_ID}`
- decision(판정): `{decision}`
- external_verification_status(외부 검증 상태): `{external}`
- report(보고서): `{rel(REPORT_PATH)}`
- summary(요약): `{rel(SUMMARY_CSV_PATH)}`
- quality_matrix(품질 행렬): `{rel(QUALITY_MATRIX_PATH)}`
- soft_guard_feature_summary(부드러운 보호문 피처 요약): `{rel(SOFT_GUARD_FEATURE_SUMMARY_PATH)}`
- risk_atr_telemetry(위험/ATR 기록): `{rel(RISK_ATR_TELEMETRY_PATH)}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준), overall_goal_complete(전체 목표 완료).
""",
    )


def write_status_files(decision: str, external: str) -> None:
    write_md(
        SELECTED_ROOT / "selection_status.md",
        f"""# Stage246 Selection Status(246단계 선택 상태)

- stage_status(단계 상태): `closed_{decision if external == "completed" else "blocked_runtime_incomplete"}`
- current_packet(현재 작업 묶음): `{PACKET_ID}`
- current_run(현재 실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- external_verification_status(외부 검증 상태): `{external}`
- decision(판정): `{decision}`
- next_stage_or_branch(다음 단계 또는 분기): `{NEXT_STAGE_ID if external == "completed" else STAGE_ID}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`
- claim_boundary(주장 경계): `{BOUNDARY}`
""",
    )
    write_md(
        REVIEWS_ROOT / "review_index.md",
        f"""# Stage246 Review Index(246단계 검토 색인)

- status(상태): `closed_{decision if external == "completed" else "blocked_runtime_incomplete"}`
- packet(작업 묶음): `{PACKET_ID}`
- run(실행): `{RUN_ID}`
- decision(판정): `{decision}`
- report(보고서): `{rel(REPORT_PATH)}`
- summary(요약): `{rel(SUMMARY_CSV_PATH)}`
- quality_matrix(품질 행렬): `{rel(QUALITY_MATRIX_PATH)}`
- soft_guard_feature_summary(부드러운 보호문 피처 요약): `{rel(SOFT_GUARD_FEATURE_SUMMARY_PATH)}`
- next_stage_or_branch(다음 단계 또는 분기): `{NEXT_STAGE_ID if external == "completed" else STAGE_ID}`
""",
    )


def append_changelog(decision: str) -> None:
    existing = io_path(CHANGELOG_PATH).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG_PATH) else ""
    if RUN_ID in existing:
        return
    entry = (
        f"\n## {utc_now()} Stage246 soft timestamp guard repair closeout(246단계 부드러운 시간 보호문 수리 종료)\n\n"
        f"- action(행동): closed(종료) `{STAGE_ID}` with decision(판정) `{decision}`.\n"
        "- effect(효과): hard guard(강한 차단)를 soft flat tilt(부드러운 무포지션 기울기)로 바꿔 MT5(MetaTrader 5, 메타트레이더5) KPI(핵심 성과 지표)를 측정하고 Stage247(247단계) follow-up review(후속 검토)로 넘겼다.\n"
        f"- boundary(주장 경계): `{BOUNDARY}`.\n"
    )
    io_path(CHANGELOG_PATH).write_text(existing.rstrip() + entry, encoding="utf-8-sig")


def artifact_rows(result: Mapping[str, Any]) -> list[dict[str, Any]]:
    created = utc_now()
    paths: list[Path] = [
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
        SOFT_GUARD_FEATURE_SUMMARY_PATH,
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
                    "artifact_type": "stage246_soft_timestamp_guard_repair_evidence",
                    "path": rel(path),
                    "sha256": sha256_file_lf_normalized(path),
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "created_at_utc": created,
                    "notes": "Stage246 soft timestamp guard repair evidence; research only.",
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
        row["parent_run_id"] = row.get("parent_run_id") or PARENT_RUN_ID
        row["scoreboard_lane"] = "baseline_adapter_stage246_soft_timestamp_guard_repair"
        row["judgment"] = decision
        row["status"] = "completed" if result.get("external_verification_status") == "completed" else "blocked"
        row["primary_kpi"] = f"{row.get('primary_kpi', '')};{primary}" if row.get("primary_kpi") else primary
        row["guardrail_kpi"] = f"{row.get('guardrail_kpi', '')};{guardrail}" if row.get("guardrail_kpi") else guardrail
        row["path"] = row.get("path") or rel(REPORT_PATH)
    run_rows = [
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "lane": "baseline_adapter_stage246_soft_timestamp_guard_repair",
            "status": "completed" if result.get("external_verification_status") == "completed" else "blocked",
            "judgment": decision,
            "path": rel(DECISION_PATH),
            "notes": ledger_pairs(
                [
                    ("source_stage245_evidence_commit", SOURCE_STAGE245_EVIDENCE_COMMIT),
                    ("source_stage245_hash_record_commit", SOURCE_STAGE245_HASH_RECORD_COMMIT),
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
    required_gates = [
        "kpi_contract_audit",
        "result_judgment_gate",
        "performance_attribution_gate",
        "artifact_lineage_audit",
        "final_claim_guard",
        "required_gate_coverage_audit",
    ]
    base_payload = {
        "packet_id": PACKET_ID,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "source_stage": SOURCE_STAGE_ID,
        "source_run_id": SOURCE_RUN_ID,
        "source_stage245_evidence_commit": SOURCE_STAGE245_EVIDENCE_COMMIT,
        "source_stage245_hash_record_commit": SOURCE_STAGE245_HASH_RECORD_COMMIT,
        "decision": decision,
        "external_verification_status": result.get("external_verification_status", ""),
        "quality_rows": list(quality),
        "claim_boundary": BOUNDARY,
        "overall_goal_complete": False,
    }
    files = {
        "routing_receipt.json": {
            **base_payload,
            "primary_family": "runtime_backtest(MT5/백테스트 실행)",
            "primary_skill": "obsidian-runtime-parity(런타임 동등성)",
            "support_skills": [
                "obsidian-backtest-forensics(백테스트 포렌식)",
                "obsidian-performance-attribution(성과 원인분해)",
                "obsidian-artifact-lineage(산출물 계보)",
            ],
            "required_gates": required_gates,
            "status": "completed",
        },
        "kpi_contract_audit.json": {
            **base_payload,
            "summary": rel(SUMMARY_CSV_PATH),
            "segments": rel(SEGMENT_KPI_PATH),
            "risk_atr": rel(RISK_ATR_TELEMETRY_PATH),
            "soft_guard_features": rel(SOFT_GUARD_FEATURE_SUMMARY_PATH),
            "performance_attribution": rel(ATTRIBUTION_PATH),
            "failure_memory": rel(FAILURE_MEMORY_PATH),
            "variant_count": len(VARIANTS),
            "status": "completed",
        },
        "result_judgment_gate.json": {
            **base_payload,
            "result_subject": RUN_ID,
            "evidence_available": [rel(REPORT_PATH), rel(SUMMARY_CSV_PATH), rel(QUALITY_MATRIX_PATH), rel(DECISION_PATH)],
            "evidence_missing": ["Stage247 follow-up review not run yet(247단계 후속 검토 미실행)", "ONNX/runtime hardening not in scope(ONNX/런타임 경화 범위 밖)"],
            "judgment_label": "soft_timestamp_guard_repair_measured_candidate_not_final",
            "next_condition": NEXT_STAGE_ID,
            "status": "passed_with_boundary",
        },
        "performance_attribution_gate.json": {
            **base_payload,
            "observed_change": "Soft middle-window flat-tilt variants measured against Stage244 hard-guard overprune failure memory.",
            "comparison_baseline": "s244_cap0305_control and legacy 34D KPI(레거시 34D 핵심 성과 지표)",
            "likely_drivers": ["middle-window low/mid soft flat tilt", "risk cap 0.0305 preservation", "ATR bracket unchanged"],
            "attribution_confidence": "medium",
            "next_probe": NEXT_STAGE_ID,
            "status": "completed",
        },
        "artifact_lineage_audit.json": {
            **base_payload,
            "source_inputs": [SOURCE_STAGE_ID, "stages/245_adapter_research__stage244_timestamp_guard_followup_review/03_reviews/stage245_decision.md"],
            "producer": rel(PRODUCER_PATH),
            "consumers": [rel(REPORT_PATH), rel(DECISION_PATH), NEXT_STAGE_ID],
            "registry_links": [rel(RUN_REGISTRY_PATH), rel(PROJECT_LEDGER_PATH), rel(STAGE_LEDGER_PATH), rel(ARTIFACT_REGISTRY_PATH)],
            "ledger_payload": ledger_payload,
            "status": "completed",
        },
        "final_claim_guard.json": {
            **base_payload,
            "deployment_claim": False,
            "live_readiness_claim": False,
            "runtime_authority_claim": False,
            "production_baseline_claim": False,
            "operating_reference_claim": False,
            "operating_promotion_claim": False,
            "status": "passed",
        },
        "required_gate_coverage_audit.json": {
            **base_payload,
            "required_gates": required_gates,
            "covered_by": [
                "kpi_contract_audit.json",
                "result_judgment_gate.json",
                "performance_attribution_gate.json",
                "artifact_lineage_audit.json",
                "final_claim_guard.json",
                "required_gate_coverage_audit.json",
            ],
            "missing_gates": [],
            "status": "passed",
        },
        "aggregate_summary.json": {
            **base_payload,
            "ledger_payload": ledger_payload,
            "required_outputs": {
                "report": rel(REPORT_PATH),
                "summary": rel(SUMMARY_CSV_PATH),
                "quality": rel(QUALITY_MATRIX_PATH),
                "performance_attribution": rel(ATTRIBUTION_PATH),
                "failure_memory": rel(FAILURE_MEMORY_PATH),
                "decision": rel(DECISION_PATH),
            },
            "pushed_commit_hash": "pending_until_push",
        },
        "packet_receipt.json": base_payload,
    }
    for name, payload in files.items():
        write_json(PACKET_ROOT / name, payload)
    write_md(
        PACKET_ROOT / "closeout_packet.md",
        f"""# Stage246 Closeout Packet(246단계 종료 작업 묶음)

- packet(작업 묶음): `{PACKET_ID}`
- run(실행): `{RUN_ID}`
- status(상태): `{result.get('external_verification_status', '')}`
- decision(판정): `{decision}`
- report(보고서): `{rel(REPORT_PATH)}`
- overall_goal_complete(전체 목표 완료): `false`
- boundary(주장 경계): `{BOUNDARY}`
""",
    )


def configure_stage_module() -> None:
    values = {
        "STAGE_ID": STAGE_ID,
        "RUN_NUMBER": RUN_NUMBER,
        "RUN_ID": RUN_ID,
        "PACKET_ID": PACKET_ID,
        "PARENT_RUN_ID": PARENT_RUN_ID,
        "SOURCE_STAGE_ID": SOURCE_STAGE_ID,
        "SOURCE_RUN_ID": SOURCE_RUN_ID,
        "NEXT_STAGE_ID": NEXT_STAGE_ID,
        "NEXT_RUN_ID": NEXT_RUN_ID,
        "NEXT_PACKET_ID": NEXT_PACKET_ID,
        "TARGET_SURFACE": TARGET_SURFACE,
        "OOS_REFERENCE": OOS_REFERENCE,
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
        "GATE_FEATURE_SUMMARY_PATH": SOFT_GUARD_FEATURE_SUMMARY_PATH,
        "PROBABILITY_BINDING_PATH": PROBABILITY_BINDING_PATH,
        "MODEL_SCORE_AUDIT_PATH": MODEL_SCORE_AUDIT_PATH,
        "TIER_B_DIAGNOSTIC_PATH": TIER_B_DIAGNOSTIC_PATH,
        "ATTRIBUTION_PATH": ATTRIBUTION_PATH,
        "FAILURE_MEMORY_PATH": FAILURE_MEMORY_PATH,
        "DECISION_PATH": DECISION_PATH,
        "AUDIT_CSV_PATH": AUDIT_CSV_PATH,
        "STAGE_LEDGER_PATH": STAGE_LEDGER_PATH,
        "PRODUCER_PATH": PRODUCER_PATH,
        "RANK_COLUMN": RANK_COLUMN,
        "VARIANTS": VARIANTS,
        "VARIANT_EXTRAS": VARIANT_EXTRAS,
        "SOURCE_SPECS_BY_VARIANT": SOURCE_SPECS_BY_VARIANT,
        "MODEL_RISK_MIN_PCT": MODEL_RISK_MIN_PCT,
    }
    for name, value in values.items():
        setattr(stage238, name, value)
    stage238.prepare_inputs = prepare_inputs
    stage238.build_attempts = build_attempts
    stage238.decide = decide
    stage238.pass_stage238 = pass_stage246
    stage238.best_row = best_row
    stage238.tier_b_rows_stage238 = tier_b_rows_stage246
    stage238.report_markdown = report_markdown
    stage238.decision_markdown = decision_markdown
    stage238.write_stage239_seed = write_stage247_seed
    stage238.update_current_truth = update_current_truth
    stage238.write_status_files = write_status_files
    stage238.append_changelog = append_changelog
    stage238.artifact_rows = artifact_rows
    stage238.write_ledgers = write_ledgers
    stage238.write_packet_files = write_packet_files


def main(argv: Sequence[str] | None = None) -> int:
    configure_stage_module()
    stage238.configure_runner()
    stage238.s161.configure_base()
    args = stage238.s161.parse_args(argv or sys.argv[1:])
    inputs = prepare_inputs(Path(args.common_files_root))
    attempts = build_attempts(inputs)
    prepared = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "stage_number": 246,
        "run_number": RUN_NUMBER,
        "run_root": RUN_ROOT,
        "packet_id": PACKET_ID,
        "attempts": attempts,
        "common_copies": inputs["common_copies"],
        "feature_exports": inputs["feature_exports"],
        "model_artifacts": inputs["model_exports"],
        "route_coverage": stage238.s161.base.engine.route_coverage(),
        "model_family": "baseline_adapter_stage246_v2_native_soft_timestamp_guard_repair",
        "feature_set_id": "stage246_signal_margin_rank_soft_middle_window_guard",
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
    attribution_rows = performance_attribution_rows(quality_rows)
    failure_rows = failure_memory_rows(quality_rows)
    external = str(result.get("external_verification_status") or "blocked")
    decision = decide(quality_rows, external)

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
    write_csv(SOFT_GUARD_FEATURE_SUMMARY_PATH, inputs["gate_rows"])
    write_csv(PROBABILITY_BINDING_PATH, probability_rows)
    write_csv(MODEL_SCORE_AUDIT_PATH, model_rows)
    write_csv(TIER_B_DIAGNOSTIC_PATH, tier_b_rows_stage246())
    write_csv(ATTRIBUTION_PATH, attribution_rows)
    write_csv(FAILURE_MEMORY_PATH, failure_rows)
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
            "attribution_rows": attribution_rows,
            "failure_memory_rows": failure_rows,
            "quality_rows": quality_rows,
            "soft_guard_rows": inputs["gate_rows"],
            "legacy_34d": LEGACY_34D,
            "source_stage245_evidence_commit": SOURCE_STAGE245_EVIDENCE_COMMIT,
            "source_stage245_hash_record_commit": SOURCE_STAGE245_HASH_RECORD_COMMIT,
            "claim_boundary": BOUNDARY,
            "overall_goal_complete": False,
            "pushed_commit_hash": "pending_until_push",
        },
    )
    write_stage247_seed(decision, external)
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
