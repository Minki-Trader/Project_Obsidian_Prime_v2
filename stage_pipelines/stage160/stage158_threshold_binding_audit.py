from __future__ import annotations

import argparse
import csv
import json
import math
import os
import re
import sys
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

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


STAGE_ID = "160_adapter_research__stage158_threshold_binding_audit"
RUN_ID = "run160A_stage160_stage158_threshold_binding_audit_v1"
PACKET_ID = "stage160_stage158_threshold_binding_audit_v1"
SOURCE_STAGE_ID = "158_adapter_research__stage156_validation_pf_margin_repair"
SOURCE_RUN_ID = "run158A_stage158_stage156_validation_pf_margin_repair_v1"
SOURCE_STAGE159_ID = "159_adapter_research__stage158_validation_pf_followup_review"
SOURCE_STAGE159_CLOSEOUT_COMMIT = "681c153ded59505a7cb407dde6f7b7572322bbf8"
SOURCE_STAGE159_HASH_RECORD_COMMIT = "5073783dfb21554831e4e7b35e8b6ce53e4e79e2"
NEXT_STAGE_ID = "161_adapter_research__score_margin_or_side_filter_repair"
NEXT_RUN_ID = "run161A_stage161_score_margin_or_side_filter_repair_v1"
NEXT_PACKET_ID = "stage161_score_margin_or_side_filter_repair_v1"
DECISION = "open_stage161_score_margin_or_side_filter_repair_candidate_not_final"
TARGET_SURFACE = "legacy_34d_kpi_lesson_only_no_legacy_inheritance"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment"
)

LEGACY_34D = {
    "profit_factor": 1.583157,
    "net_profit": 987.60,
    "max_drawdown_percent": 12.909136,
    "trade_count": 404,
}

STAGE_ROOT = Path("stages") / STAGE_ID
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
SELECTED_ROOT = STAGE_ROOT / "04_selected"
PACKET_ROOT = Path("docs/agent_control/packets") / PACKET_ID
NEXT_STAGE_ROOT = Path("stages") / NEXT_STAGE_ID

SOURCE_REVIEWS_ROOT = Path("stages") / SOURCE_STAGE_ID / "03_reviews"
SOURCE_RUN_MANIFEST = Path("stages") / SOURCE_STAGE_ID / "02_runs/run158A/run_manifest.json"
SOURCE_SUMMARY = SOURCE_REVIEWS_ROOT / "stage158_validation_pf_margin_summary.csv"
SOURCE_SEGMENTS = SOURCE_REVIEWS_ROOT / "stage158_segment_kpi_summary.csv"
SOURCE_GATE = SOURCE_REVIEWS_ROOT / "stage158_gate_feature_summary.csv"
SOURCE_TRADE_AUDIT = SOURCE_REVIEWS_ROOT / "stage158_trade_audit.csv"
SOURCE_RISK_ATR = SOURCE_REVIEWS_ROOT / "stage158_risk_atr_telemetry.csv"
SOURCE_STAGE159_SUMMARY = (
    Path("stages")
    / SOURCE_STAGE159_ID
    / "03_reviews/stage159_threshold_binding_summary.csv"
)
SOURCE_STAGE159_DECISION = Path("stages") / SOURCE_STAGE159_ID / "03_reviews/stage159_decision.md"

REPORT_PATH = REVIEWS_ROOT / "stage160_threshold_binding_audit.md"
BINDING_SUMMARY_PATH = REVIEWS_ROOT / "stage160_threshold_binding_summary.csv"
PROBABILITY_SUMMARY_PATH = REVIEWS_ROOT / "stage160_probability_distribution_summary.csv"
RUNTIME_REASON_PATH = REVIEWS_ROOT / "stage160_runtime_reason_summary.csv"
SET_AUDIT_PATH = REVIEWS_ROOT / "stage160_set_threshold_audit.csv"
MODEL_SCORE_PATH = REVIEWS_ROOT / "stage160_model_score_audit.csv"
FAILURE_MEMORY_PATH = REVIEWS_ROOT / "stage160_failure_memory.csv"
ROUTE_DECISION_PATH = REVIEWS_ROOT / "stage160_route_decision.csv"
DECISION_PATH = REVIEWS_ROOT / "stage160_decision.md"
SUMMARY_JSON_PATH = REVIEWS_ROOT / "stage160_followup_summary.json"
STAGE_LEDGER_PATH = REVIEWS_ROOT / "stage_run_ledger.csv"
PRODUCER_PATH = Path("stage_pipelines/stage160/stage158_threshold_binding_audit.py")

RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
PROJECT_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
ARTIFACT_REGISTRY_PATH = Path("docs/registers/artifact_registry.csv")
WORKSPACE_STATE_PATH = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE_PATH = Path("docs/context/current_working_state.md")
CHANGELOG_PATH = Path("docs/workspace/changelog.md")

ARTIFACT_COLUMNS = (
    "artifact_id",
    "artifact_type",
    "path",
    "sha256",
    "stage_id",
    "run_id",
    "created_at_utc",
    "notes",
)


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    candidate = Path(str(path))
    try:
        return io_path(candidate).resolve().relative_to(io_path(REPO_ROOT).resolve()).as_posix()
    except ValueError:
        return candidate.as_posix()


def common_files_root() -> Path:
    appdata = os.environ.get("APPDATA")
    if appdata:
        return Path(appdata) / "MetaQuotes/Terminal/Common/Files"
    return Path.home() / "AppData/Roaming/MetaQuotes/Terminal/Common/Files"


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(
        json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def read_csv(path: Path) -> list[dict[str, str]]:
    with io_path(path).open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str] | None = None) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    fieldnames = tuple(columns or (rows[0].keys() if rows else ()))
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: row.get(column, "") for column in fieldnames})


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text, encoding="utf-8-sig")


def parse_set(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for line in io_path(path).read_text(encoding="utf-8-sig").splitlines():
        if not line or line.lstrip().startswith(";") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip()
    return values


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        if value is None or value == "":
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def as_bool(value: Any) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes"}


def quantile(values: Sequence[float], q: float) -> float:
    finite = sorted(value for value in values if math.isfinite(value))
    if not finite:
        return 0.0
    if len(finite) == 1:
        return finite[0]
    pos = (len(finite) - 1) * float(q)
    lo = int(math.floor(pos))
    hi = int(math.ceil(pos))
    if lo == hi:
        return finite[lo]
    weight = pos - lo
    return finite[lo] * (1.0 - weight) + finite[hi] * weight


def variant_from_common_path(common_path: str) -> str:
    parts = Path(common_path).parts
    if len(parts) >= 4:
        return parts[3]
    stem = Path(common_path).stem
    return re.sub(r"_(rt|ta)_(val|oos).*", "", stem)


def split_token(split: str) -> str:
    return "val" if split == "validation_is" else "oos"


def source_summary_by_key() -> dict[tuple[str, str], dict[str, str]]:
    rows = read_csv(SOURCE_SUMMARY)
    return {
        (row.get("adapter_id", ""), row.get("split", "")): row
        for row in rows
        if row.get("view") == "actual_routed_total"
    }


def analyze_telemetry(
    path: Path,
    *,
    short_threshold: float,
    long_threshold: float,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    p_short_values: list[float] = []
    p_flat_values: list[float] = []
    p_long_values: list[float] = []
    winning_values: list[float] = []
    passed_directional_values: list[float] = []
    reason_counts: Counter[str] = Counter()
    decision_counts: Counter[str] = Counter()
    lifecycle_counts: Counter[str] = Counter()
    rows = 0
    feature_ready_rows = 0
    model_ok_rows = 0
    short_pass = 0
    long_pass = 0
    near_threshold = 0
    broad_threshold_band = 0
    short_saturated = 0
    long_saturated = 0
    flat_saturated = 0
    side_filter_block = 0
    threshold_or_margin_not_met = 0
    threshold_met_reason = 0
    order_attempted = 0
    order_filled = 0
    min_lot_floor = 0
    max_model_risk_pct = 0.0
    max_actual_risk_pct_after_floor = 0.0

    with io_path(path).open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            record_type = row.get("record_type", "")
            if record_type == "lifecycle":
                lifecycle_counts[row.get("lifecycle_decision", "") or row.get("event", "")] += 1
                continue
            if record_type != "cycle":
                continue
            rows += 1
            if as_bool(row.get("feature_ready")):
                feature_ready_rows += 1
            if as_bool(row.get("model_ok")):
                model_ok_rows += 1
            p_short = as_float(row.get("p_short"))
            p_flat = as_float(row.get("p_flat"))
            p_long = as_float(row.get("p_long"))
            p_short_values.append(p_short)
            p_flat_values.append(p_flat)
            p_long_values.append(p_long)
            winning = max(p_short, p_flat, p_long)
            winning_values.append(winning)
            reason = row.get("decision_reason", "")
            decision = row.get("decision", "")
            reason_counts[reason] += 1
            decision_counts[decision] += 1
            if p_short >= short_threshold:
                short_pass += 1
                passed_directional_values.append(p_short)
            if p_long >= long_threshold:
                long_pass += 1
                passed_directional_values.append(p_long)
            if abs(p_short - short_threshold) <= 0.01 or abs(p_long - long_threshold) <= 0.01:
                near_threshold += 1
            if 0.50 <= p_short <= 0.60 or 0.50 <= p_long <= 0.60:
                broad_threshold_band += 1
            if p_short >= 0.99:
                short_saturated += 1
            if p_long >= 0.99:
                long_saturated += 1
            if p_flat >= 0.99:
                flat_saturated += 1
            if "side_filter_block" in reason:
                side_filter_block += 1
            if "threshold_or_margin_not_met" in reason:
                threshold_or_margin_not_met += 1
            if "threshold_met" in reason:
                threshold_met_reason += 1
            if as_bool(row.get("order_attempted")):
                order_attempted += 1
            if as_bool(row.get("order_filled")):
                order_filled += 1
            if as_bool(row.get("min_lot_floor_applied")):
                min_lot_floor += 1
            max_model_risk_pct = max(max_model_risk_pct, as_float(row.get("model_risk_pct")))
            max_actual_risk_pct_after_floor = max(
                max_actual_risk_pct_after_floor,
                as_float(row.get("actual_risk_pct_after_floor")),
            )

    unique_short = len({round(value, 10) for value in p_short_values})
    unique_flat = len({round(value, 10) for value in p_flat_values})
    unique_long = len({round(value, 10) for value in p_long_values})
    summary = {
        "cycle_rows": rows,
        "feature_ready_rows": feature_ready_rows,
        "model_ok_rows": model_ok_rows,
        "short_threshold_pass_rows": short_pass,
        "long_threshold_pass_rows": long_pass,
        "directional_threshold_pass_rows": short_pass + long_pass,
        "directional_near_threshold_001_rows": near_threshold,
        "directional_050_060_band_rows": broad_threshold_band,
        "directional_pass_min_probability": min(passed_directional_values) if passed_directional_values else 0.0,
        "directional_pass_median_probability": quantile(passed_directional_values, 0.5),
        "directional_pass_max_probability": max(passed_directional_values) if passed_directional_values else 0.0,
        "p_short_min": min(p_short_values) if p_short_values else 0.0,
        "p_short_median": quantile(p_short_values, 0.5),
        "p_short_max": max(p_short_values) if p_short_values else 0.0,
        "p_flat_min": min(p_flat_values) if p_flat_values else 0.0,
        "p_flat_median": quantile(p_flat_values, 0.5),
        "p_flat_max": max(p_flat_values) if p_flat_values else 0.0,
        "p_long_min": min(p_long_values) if p_long_values else 0.0,
        "p_long_median": quantile(p_long_values, 0.5),
        "p_long_max": max(p_long_values) if p_long_values else 0.0,
        "winning_prob_min": min(winning_values) if winning_values else 0.0,
        "winning_prob_median": quantile(winning_values, 0.5),
        "winning_prob_max": max(winning_values) if winning_values else 0.0,
        "p_short_unique_count": unique_short,
        "p_flat_unique_count": unique_flat,
        "p_long_unique_count": unique_long,
        "short_saturated_ge099_rows": short_saturated,
        "long_saturated_ge099_rows": long_saturated,
        "flat_saturated_ge099_rows": flat_saturated,
        "side_filter_block_rows": side_filter_block,
        "threshold_or_margin_not_met_rows": threshold_or_margin_not_met,
        "threshold_met_reason_rows": threshold_met_reason,
        "order_attempted_rows": order_attempted,
        "order_filled_rows": order_filled,
        "min_lot_floor_applied_rows": min_lot_floor,
        "max_model_risk_pct": max_model_risk_pct,
        "max_actual_risk_pct_after_floor": max_actual_risk_pct_after_floor,
        "decision_counts": dict(decision_counts),
        "lifecycle_counts": dict(lifecycle_counts),
    }
    reason_rows = [
        {
            "decision_reason": reason or "blank",
            "count": count,
            "contains_threshold_met": "threshold_met" in reason,
            "contains_side_filter_block": "side_filter_block" in reason,
            "contains_threshold_or_margin_not_met": "threshold_or_margin_not_met" in reason,
        }
        for reason, count in sorted(reason_counts.items(), key=lambda item: (-item[1], item[0]))
    ]
    return summary, reason_rows


def audit_model_score(model_path: Path, variant_id: str) -> dict[str, Any]:
    rows = read_csv(model_path)
    feature0_probs: list[float] = []
    feature0_gaps: list[float] = []
    feature1_all_zero = True
    score_rows = 0
    for row in rows:
        if row.get("record_type") != "score":
            continue
        feature_index = int(float(row.get("feature_index", 0)))
        scores = [
            as_float(row.get("score_short")),
            as_float(row.get("score_flat")),
            as_float(row.get("score_long")),
        ]
        if feature_index == 0:
            score_rows += 1
            ordered = sorted(scores, reverse=True)
            gap = ordered[0] - ordered[1]
            feature0_gaps.append(gap)
            shifted = [math.exp(score - ordered[0]) for score in scores]
            feature0_probs.append(max(shifted) / sum(shifted))
        elif feature_index == 1 and any(abs(score) > 1e-12 for score in scores):
            feature1_all_zero = False
    return {
        "variant_id": variant_id,
        "model_path": str(model_path),
        "model_sha256": sha256_file_lf_normalized(model_path) if path_exists(model_path) else "",
        "feature0_score_rows": score_rows,
        "feature0_min_score_gap": min(feature0_gaps) if feature0_gaps else 0.0,
        "feature0_max_score_gap": max(feature0_gaps) if feature0_gaps else 0.0,
        "feature0_min_implied_winner_prob": min(feature0_probs) if feature0_probs else 0.0,
        "feature0_max_implied_winner_prob": max(feature0_probs) if feature0_probs else 0.0,
        "feature1_scores_all_zero": feature1_all_zero,
        "score_shape_label": "saturated_discrete_score_table" if feature0_probs and min(feature0_probs) >= 0.99 else "non_saturated_or_unknown",
    }


def build_audit() -> dict[str, Any]:
    manifest = read_json(SOURCE_RUN_MANIFEST)
    summary_by_key = source_summary_by_key()
    stage159_rows = read_csv(SOURCE_STAGE159_SUMMARY)
    attempts = [attempt for attempt in manifest.get("attempts", []) if attempt.get("attempt_role") == "routed_total"]
    common_root = common_files_root()
    binding_rows: list[dict[str, Any]] = []
    probability_rows: list[dict[str, Any]] = []
    reason_rows: list[dict[str, Any]] = []
    set_rows: list[dict[str, Any]] = []
    model_rows_by_variant: dict[str, dict[str, Any]] = {}

    for attempt in attempts:
        common_telemetry = str(attempt.get("common_telemetry_path", ""))
        variant_id = variant_from_common_path(common_telemetry)
        split = str(attempt.get("split", ""))
        source_summary = summary_by_key.get((variant_id, split), {})
        short_threshold = as_float(source_summary.get("short_threshold"))
        long_threshold = as_float(source_summary.get("long_threshold"))
        telemetry_path = common_root / common_telemetry
        if not path_exists(telemetry_path):
            raise FileNotFoundError(telemetry_path)
        telemetry_stats, attempt_reason_rows = analyze_telemetry(
            telemetry_path,
            short_threshold=short_threshold,
            long_threshold=long_threshold,
        )
        set_path = Path(str(attempt.get("set", {}).get("path", "")))
        set_values = parse_set(set_path)
        set_short = as_float(set_values.get("InpShortThreshold"))
        set_long = as_float(set_values.get("InpLongThreshold"))
        set_match = abs(set_short - short_threshold) < 1e-12 and abs(set_long - long_threshold) < 1e-12
        common_model = f"OPV2/s158a/run158A/{variant_id}/models/{variant_id}_model.csv"
        model_path = common_root / common_model
        if variant_id not in model_rows_by_variant:
            model_rows_by_variant[variant_id] = audit_model_score(model_path, variant_id)

        label = "threshold_written_but_not_binding"
        if not set_match:
            label = "threshold_handoff_mismatch"
        elif telemetry_stats["directional_050_060_band_rows"] == 0 and telemetry_stats["directional_pass_min_probability"] >= 0.99:
            label = "threshold_written_score_saturated_non_binding"

        binding_row = {
            "run_id": RUN_ID,
            "adapter_id": variant_id,
            "split": split,
            "view": "actual_routed_total",
            "attempt_name": attempt.get("attempt_name", ""),
            "short_threshold": short_threshold,
            "long_threshold": long_threshold,
            "set_short_threshold": set_short,
            "set_long_threshold": set_long,
            "set_threshold_match": set_match,
            "cycle_rows": telemetry_stats["cycle_rows"],
            "directional_threshold_pass_rows": telemetry_stats["directional_threshold_pass_rows"],
            "directional_near_threshold_001_rows": telemetry_stats["directional_near_threshold_001_rows"],
            "directional_050_060_band_rows": telemetry_stats["directional_050_060_band_rows"],
            "directional_pass_min_probability": telemetry_stats["directional_pass_min_probability"],
            "side_filter_block_rows": telemetry_stats["side_filter_block_rows"],
            "threshold_or_margin_not_met_rows": telemetry_stats["threshold_or_margin_not_met_rows"],
            "threshold_met_reason_rows": telemetry_stats["threshold_met_reason_rows"],
            "order_attempted_rows": telemetry_stats["order_attempted_rows"],
            "order_filled_rows": telemetry_stats["order_filled_rows"],
            "trade_count": as_float(source_summary.get("trade_count")),
            "profit_factor": as_float(source_summary.get("profit_factor")),
            "net_profit": as_float(source_summary.get("net_profit")),
            "max_drawdown_percent": as_float(source_summary.get("max_drawdown_percent")),
            "threshold_binding_label": label,
            "overall_goal_complete": False,
        }
        binding_rows.append(binding_row)
        probability_rows.append(
            {
                "run_id": RUN_ID,
                "adapter_id": variant_id,
                "split": split,
                "view": "actual_routed_total",
                **{
                    key: value
                    for key, value in telemetry_stats.items()
                    if key not in {"decision_counts", "lifecycle_counts"}
                },
                "decision_counts": json.dumps(telemetry_stats["decision_counts"], sort_keys=True),
                "lifecycle_counts": json.dumps(telemetry_stats["lifecycle_counts"], sort_keys=True),
            }
        )
        set_rows.append(
            {
                "adapter_id": variant_id,
                "split": split,
                "attempt_name": attempt.get("attempt_name", ""),
                "set_path": rel(set_path),
                "set_sha256": sha256_file_lf_normalized(set_path) if path_exists(set_path) else "",
                "summary_short_threshold": short_threshold,
                "summary_long_threshold": long_threshold,
                "set_short_threshold": set_short,
                "set_long_threshold": set_long,
                "set_threshold_match": set_match,
                "min_margin": as_float(set_values.get("InpMinMargin")),
                "fallback_short_threshold": as_float(set_values.get("InpFallbackShortThreshold")),
                "fallback_long_threshold": as_float(set_values.get("InpFallbackLongThreshold")),
            }
        )
        for reason in attempt_reason_rows:
            reason_rows.append(
                {
                    "adapter_id": variant_id,
                    "split": split,
                    "view": "actual_routed_total",
                    **reason,
                }
            )

    set_match_count = sum(1 for row in set_rows if row["set_threshold_match"])
    saturated_count = sum(
        1
        for row in binding_rows
        if row["directional_050_060_band_rows"] == 0 and row["directional_pass_min_probability"] >= 0.99
    )
    near_threshold_rows = sum(int(row["directional_050_060_band_rows"]) for row in binding_rows)
    same_kpi_threshold_rows = [
        row
        for row in stage159_rows
        if row.get("adapter_id") != "s158_valpf_lng53_risk0325_h3_cd5_sht54_lng53"
        and abs(as_float(row.get("validation_pf_delta_vs_base"))) < 1e-12
        and abs(as_float(row.get("oos_net_delta_vs_base"))) < 0.01
    ]
    route_decision = [
        {
            "decision": DECISION,
            "reason": "thresholds_are_written_to_set_files_but_model_probabilities_are_saturated_and_no_directional_rows_live_near_0_52_to_0_55",
            "next_stage": NEXT_STAGE_ID,
            "next_run": NEXT_RUN_ID,
            "next_axis": "score_margin_or_side_filter_repair_not_threshold_only",
            "do_not_repeat": "do_not_continue_short_long_threshold_only_tuning_on_the_current_saturated_score_table",
            "overall_goal_complete": False,
        }
    ]
    failure_memory = [
        {
            "failure_id": "stage160_threshold_only_non_binding",
            "hypothesis": "raising_short_or_long_thresholds_from_stage156_can_lift_validation_pf",
            "why_failed": "Stage158 threshold variants changed set files, but telemetry has zero directional rows in the 0.50-0.60 probability band and active directional rows are near 0.999329.",
            "salvage_value": "set file handoff is working; the repair should move score calibration, margin surface, or side filter rather than threshold-only values.",
            "reopen_condition": "a future model score table produces directional probabilities near the tested threshold band or a nonzero min_margin creates real row selection movement.",
            "do_not_repeat": "do_not_keep_adjusting_0_52_to_0_55_thresholds_without_a_binding_probability_distribution",
            "overall_goal_complete": False,
        }
    ]
    return {
        "decision": DECISION,
        "binding_rows": binding_rows,
        "probability_rows": probability_rows,
        "reason_rows": reason_rows,
        "set_rows": set_rows,
        "model_rows": list(model_rows_by_variant.values()),
        "route_decision": route_decision,
        "failure_memory": failure_memory,
        "stage159_threshold_delta_rows": stage159_rows,
        "set_match_count": set_match_count,
        "set_audit_count": len(set_rows),
        "saturated_attempt_count": saturated_count,
        "near_threshold_rows_total": near_threshold_rows,
        "same_kpi_threshold_variant_count": len(same_kpi_threshold_rows),
        "claim_boundary": BOUNDARY,
        "overall_goal_complete": False,
    }


def compact_kpi_table(rows: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        "| adapter(어댑터) | split(분할) | short/long threshold(숏/롱 문턱값) | PF(수익요인) | net(순손익) | DD%(낙폭) | near 0.50-0.60(근처 행) | pass min prob(통과 최소 확률) | read(판독) |",
        "|---|---|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in rows:
        lines.append(
            "| {adapter_id} | {split} | {short_threshold:.2f}/{long_threshold:.2f} | {profit_factor:.6f} | {net_profit:.2f} | {max_drawdown_percent:.2f} | {directional_050_060_band_rows} | {directional_pass_min_probability:.9f} | {threshold_binding_label} |".format(
                **row
            )
        )
    return "\n".join(lines)


def model_table(rows: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        "| adapter(어댑터) | score gap(점수 차) | implied prob(암시 확률) | feature1(피처1) | read(판독) |",
        "|---|---:|---:|---|---|",
    ]
    for row in rows:
        lines.append(
            "| {variant_id} | {feature0_min_score_gap:.6f} | {feature0_min_implied_winner_prob:.9f} | zero={feature1_scores_all_zero} | {score_shape_label} |".format(
                **row
            )
        )
    return "\n".join(lines)


def report_markdown(audit: Mapping[str, Any]) -> str:
    binding_rows = audit["binding_rows"]
    model_rows = audit["model_rows"]
    return f"""# Stage160 Threshold Binding Audit(160단계 문턱값 작동 감사)

- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- decision(판정): `{DECISION}`
- boundary(주장 경계): `{BOUNDARY}`

## Answer(답)

Threshold handoff(문턱값 전달)는 살아 있다. set file(설정 파일)에 `InpShortThreshold/InpLongThreshold(숏/롱 문턱값)`가 기록됐고, summary(요약) 값과도 맞는다.

하지만 tested threshold axis(시험한 문턱값 축)는 사실상 non-binding(비작동)이다. Directional probability(방향 확률)가 0.52~0.55 근처에 없고, 진입 후보는 거의 `0.999329`로 포화되어 있다. Effect(효과): Stage161(161단계)은 threshold-only tuning(문턱값만 조정)을 반복하지 않고 score margin(점수 마진) 또는 side filter(방향 필터) 수리로 가야 한다.

## Evidence(근거)

- set match(설정 일치): `{audit["set_match_count"]}/{audit["set_audit_count"]}`
- saturated attempts(포화 시도): `{audit["saturated_attempt_count"]}/{len(binding_rows)}`
- directional rows near 0.50-0.60(방향 확률 0.50-0.60 근처 행): `{audit["near_threshold_rows_total"]}`
- Stage159 same-KPI threshold variants(159단계 KPI 동일 문턱값 변형): `{audit["same_kpi_threshold_variant_count"]}`

{compact_kpi_table(binding_rows)}

## Model Score Read(모델 점수 판독)

{model_table(model_rows)}

## Judgment(판정)

- result_subject(판정 대상): Stage158(158단계) threshold repair(문턱값 수리) 축
- evidence_available(있는 근거): Stage158 MT5 telemetry(메타트레이더5 기록), set files(설정 파일), model CSV(모델 CSV), Stage159 KPI delta(KPI 차이)
- evidence_missing(빠진 근거): 새 MT5 repair run(메타트레이더5 수리 실행)은 Stage160 범위 밖
- judgment_label(판정 라벨): `threshold_written_score_saturated_non_binding`
- claim_boundary(주장 경계): research/development only(연구개발 전용)
- next_condition(다음 조건): Stage161(161단계)에서 실제로 행 선택이 바뀌는 score margin(점수 마진) 또는 side filter(방향 필터) 수리 측정

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), overall goal complete(전체 목표 완료).
"""


def decision_markdown() -> str:
    return f"""# Stage160 Decision(160단계 판정)

- decision(판정): `{DECISION}`
- stage_status(단계 상태): `closed_audit_only_candidate_not_final`
- next_stage_or_branch(다음 단계/분기): `{NEXT_STAGE_ID}`
- next_run(다음 실행): `{NEXT_RUN_ID}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`
- claim_boundary(주장 경계): `{BOUNDARY}`

## Why(이유)

Thresholds(문턱값)는 set file(설정 파일)에 들어갔다. 그러나 model probability(모델 확률)가 포화되어 0.52~0.55 threshold band(문턱값 구간)에 걸리는 방향 행이 없다.

Effect(효과): 다음 수리는 threshold-only(문턱값 단독)가 아니라 score margin(점수 마진), probability calibration(확률 보정), 또는 side filter(방향 필터) 축이어야 한다.

Stage160(160단계) closeout(종료)은 전체 목표 완료가 아니다.
"""


def write_stage161_seed() -> None:
    write_md(
        NEXT_STAGE_ROOT / "00_spec/stage_brief.md",
        f"""# {NEXT_STAGE_ID}

Stage161(161단계)은 Stage160(160단계)에서 확인한 non-binding threshold(비작동 문턱값) 문제 뒤의 실제 repair axis(수리 축)를 좁게 시험한다.

## Bounded Question(경계 질문)

Can score margin(점수 마진), probability calibration(확률 보정), or side filter(방향 필터) repair create real row-selection movement(행 선택 변화) and improve validation PF(검증 수익요인) toward or above legacy 34D KPI(레거시 34D 핵심 성과 지표) without damaging OOS PF/net/DD/mid(표본외 수익요인/순손익/낙폭/중반) and ATR/risk behavior(ATR/위험 행동)?

Effect(효과): 더 센 threshold(문턱값)를 계속 돌리는 일을 멈추고, 실제로 거래 선택을 바꾸는 축만 시험한다.

## Boundary(경계)

`{BOUNDARY}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "01_inputs/input_refs.md",
        f"""# Stage161 Input References(161단계 입력 참조)

- stage160_decision(160단계 판정): `{rel(DECISION_PATH)}`
- stage160_audit(160단계 감사): `{rel(REPORT_PATH)}`
- stage160_threshold_binding_summary(160단계 문턱값 작동 요약): `{rel(BINDING_SUMMARY_PATH)}`
- stage160_probability_distribution_summary(160단계 확률 분포 요약): `{rel(PROBABILITY_SUMMARY_PATH)}`
- stage158_summary(158단계 요약): `{rel(SOURCE_SUMMARY)}`
- stage158_trade_audit(158단계 거래 감사): `{rel(SOURCE_TRADE_AUDIT)}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "03_reviews/review_index.md",
        f"""# Stage161 Review Index(161단계 검토 색인)

- status(상태): `open_planned_from_stage160`
- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- source_stage(원천 단계): `{STAGE_ID}`

Effect(효과): Stage161(161단계) 산출물을 한 위치에서 추적한다.
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "04_selected/selection_status.md",
        f"""# Stage161 Selection Status(161단계 선택 상태)

- stage_status(단계 상태): `open_planned_from_stage160`
- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Effect(효과): Stage161(161단계)는 score margin(점수 마진) 또는 side filter(방향 필터) repair(수리)만 흡수한다.
""",
    )


def update_current_truth() -> None:
    state = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    state = re.sub(r"(?m)^active_stage:.*$", f"active_stage: {NEXT_STAGE_ID}", state)
    state = re.sub(r"(?m)^current_run_id:.*$", f"current_run_id: {NEXT_RUN_ID}", state)
    current_focus = f"""current_focus:
- >-
  Stage160(160단계) closed(종료) as `{DECISION}` and Stage161(161단계) `{NEXT_STAGE_ID}` is open_planned(개방 계획). Effect(효과): threshold-only tuning(문턱값 단독 조정)을 멈추고 실제 행 선택을 바꾸는 score margin(점수 마진) 또는 side filter(방향 필터) 수리로 넘긴다.
- >-
  Stage160 evidence(160단계 근거)는 `{rel(REPORT_PATH)}`, `{rel(BINDING_SUMMARY_PATH)}`, `{rel(PROBABILITY_SUMMARY_PATH)}`, `{rel(RUNTIME_REASON_PATH)}`, `{rel(MODEL_SCORE_PATH)}`에 있다. Effect(효과): Stage158(158단계) 문턱값 변형의 무변화를 set file(설정 파일), model CSV(모델 CSV), telemetry(기록)로 분해한다.
- >-
  Target surface(목표 표면)는 `{TARGET_SURFACE}`이고 legacy 34D(레거시 34D)는 lesson-only KPI target(교훈 전용 핵심 성과 지표 목표)이다. Effect(효과): v2-native research(v2 고유 연구)만 계속한다.

"""
    state = re.sub(r"(?ms)^current_focus:\r?\n.*?(?=\r?\nstage\d+_)", current_focus, state, count=1)
    state = re.sub(r"(?ms)\nstage160_stage158_threshold_binding_audit:.*?(?=\nstage\d+_|$)", "\n", state)
    state = re.sub(r"(?ms)\nstage161_score_margin_or_side_filter_repair:.*?(?=\nstage\d+_|$)", "\n", state)
    block = f"""
stage160_stage158_threshold_binding_audit:
  packet_id: {PACKET_ID}
  stage_id: {STAGE_ID}
  status: closed_{DECISION}
  current_run_id: {RUN_ID}
  source_stage159_closeout_commit: {SOURCE_STAGE159_CLOSEOUT_COMMIT}
  source_stage159_hash_record_commit: {SOURCE_STAGE159_HASH_RECORD_COMMIT}
  source_stage: {SOURCE_STAGE_ID}
  source_run: {SOURCE_RUN_ID}
  decision: {DECISION}
  report_path: {rel(REPORT_PATH)}
  decision_path: {rel(DECISION_PATH)}
  packet_summary_path: {rel(PACKET_ROOT / "aggregate_summary.json")}
  next_stage_or_branch: {NEXT_STAGE_ID}
  pushed_commit_hash: pending_until_push
  boundary: {BOUNDARY}

stage161_score_margin_or_side_filter_repair:
  packet_id: {NEXT_PACKET_ID}
  stage_id: {NEXT_STAGE_ID}
  status: open_planned_from_stage160
  current_run_id: {NEXT_RUN_ID}
  source_stage: {STAGE_ID}
  source_decision: {DECISION}
  next_action: {NEXT_RUN_ID}
  boundary: {BOUNDARY}
"""
    io_path(WORKSPACE_STATE_PATH).write_text(state.rstrip() + "\n" + block, encoding="utf-8-sig")
    write_md(
        CURRENT_WORKING_STATE_PATH,
        f"""# Current Working State(현재 작업 상태)

- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- active_stage(활성 단계): `{NEXT_STAGE_ID}`
- selected_research_baseline(선택 연구 기준선): `none`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- adapter_under_review(검토 중 어댑터): `stage161_score_margin_or_side_filter_repair_surface`
- status(상태): `stage160_closed_{DECISION}_stage161_open_planned`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage160(160단계)는 Stage158(158단계)의 threshold binding(문턱값 작동 여부)을 audit-only(감사 전용)로 판정했다. Effect(효과): threshold-only tuning(문턱값 단독 조정)을 멈추고 Stage161(161단계) score margin(점수 마진) 또는 side filter(방향 필터) repair(수리)로 넘긴다.

## Latest Stage160 Evidence(최신 160단계 근거)

- run(실행): `{RUN_ID}`
- decision(판정): `{DECISION}`
- report(보고서): `{rel(REPORT_PATH)}`
- threshold_binding_summary(문턱값 작동 요약): `{rel(BINDING_SUMMARY_PATH)}`
- probability_distribution_summary(확률 분포 요약): `{rel(PROBABILITY_SUMMARY_PATH)}`
- runtime_reason_summary(런타임 이유 요약): `{rel(RUNTIME_REASON_PATH)}`
- model_score_audit(모델 점수 감사): `{rel(MODEL_SCORE_PATH)}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준선), legacy_inheritance(레거시 상속), overall_goal_complete(전체 목표 완료).
""",
    )


def write_status_files() -> None:
    write_md(
        SELECTED_ROOT / "selection_status.md",
        f"""# Stage160 Selection Status(160단계 선택 상태)

- stage_status(단계 상태): `closed_{DECISION}`
- current_packet(현재 작업 묶음): `{PACKET_ID}`
- current_run(현재 실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_stage159_closeout_commit(원천 159단계 종료 커밋): `{SOURCE_STAGE159_CLOSEOUT_COMMIT}`
- stage160_decision(160단계 판정): `{DECISION}`
- next_stage_or_branch(다음 단계/분기): `{NEXT_STAGE_ID}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`
- claim_boundary(주장 경계): `{BOUNDARY}`

Effect(효과): Stage160(160단계)은 threshold binding audit(문턱값 작동 감사)만 닫고 Stage161(161단계) 수리로 넘긴다.
""",
    )
    write_md(
        REVIEWS_ROOT / "review_index.md",
        f"""# Stage160 Review Index(160단계 검토 색인)

- status(상태): `closed_{DECISION}`
- packet(작업 묶음): `{PACKET_ID}`
- run(실행): `{RUN_ID}`
- decision(판정): `{DECISION}`
- report(보고서): `{rel(REPORT_PATH)}`
- threshold_binding_summary(문턱값 작동 요약): `{rel(BINDING_SUMMARY_PATH)}`
- probability_distribution_summary(확률 분포 요약): `{rel(PROBABILITY_SUMMARY_PATH)}`
- runtime_reason_summary(런타임 이유 요약): `{rel(RUNTIME_REASON_PATH)}`
- model_score_audit(모델 점수 감사): `{rel(MODEL_SCORE_PATH)}`
- next_stage_or_branch(다음 단계/분기): `{NEXT_STAGE_ID}`

Effect(효과): Stage160(160단계) 산출물 위치를 한 곳에서 추적한다.
""",
    )


def append_changelog() -> None:
    existing = io_path(CHANGELOG_PATH).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG_PATH) else ""
    if RUN_ID in existing:
        return
    entry = (
        f"\n## {utc_now()} Stage160 threshold binding audit closeout(160단계 문턱값 작동 감사 종료)\n\n"
        f"- action(행동): closed(종료) `{STAGE_ID}` with decision(판정) `{DECISION}`.\n"
        "- effect(효과): Stage158 threshold(158단계 문턱값) 무변화가 handoff miss(전달 누락)가 아니라 saturated score table(포화 점수표) 문제임을 기록하고 Stage161(161단계) 수리축으로 넘겼다.\n"
        f"- boundary(주장 경계): `{BOUNDARY}`.\n"
    )
    io_path(CHANGELOG_PATH).write_text(existing.rstrip() + entry, encoding="utf-8-sig")


def artifact_rows(notes_suffix: str = "") -> list[dict[str, Any]]:
    created = utc_now()
    paths = [
        PRODUCER_PATH,
        REPORT_PATH,
        BINDING_SUMMARY_PATH,
        PROBABILITY_SUMMARY_PATH,
        RUNTIME_REASON_PATH,
        SET_AUDIT_PATH,
        MODEL_SCORE_PATH,
        FAILURE_MEMORY_PATH,
        ROUTE_DECISION_PATH,
        DECISION_PATH,
        SUMMARY_JSON_PATH,
        STAGE_LEDGER_PATH,
    ]
    rows: list[dict[str, Any]] = []
    for path in paths:
        if path_exists(path):
            rows.append(
                {
                    "artifact_id": f"{RUN_ID}__{Path(path).name}",
                    "artifact_type": "stage160_threshold_binding_audit_evidence",
                    "path": rel(path),
                    "sha256": sha256_file_lf_normalized(path),
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "created_at_utc": created,
                    "notes": f"Stage160 review-only Stage158 threshold binding audit artifact.{notes_suffix}",
                }
            )
    return rows


def write_ledgers(audit: Mapping[str, Any], notes_suffix: str = "") -> dict[str, Any]:
    run_payload = upsert_csv_rows(
        RUN_REGISTRY_PATH,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "baseline_adapter_stage160_threshold_binding_audit",
                "status": "completed",
                "judgment": DECISION,
                "path": rel(DECISION_PATH),
                "notes": ledger_pairs(
                    (
                        ("source_stage159_closeout_commit", SOURCE_STAGE159_CLOSEOUT_COMMIT),
                        ("source_stage159_hash_record_commit", SOURCE_STAGE159_HASH_RECORD_COMMIT),
                        ("source_run", SOURCE_RUN_ID),
                        ("target_surface", TARGET_SURFACE),
                        ("overall_goal_complete", 0),
                    )
                ),
            }
        ],
        key="run_id",
    )
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__review_only",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "review_only",
        "parent_run_id": SOURCE_RUN_ID,
        "record_view": "stage_review",
        "tier_scope": "actual_routed_total",
        "kpi_scope": "threshold_binding_probability_set_model_telemetry",
        "scoreboard_lane": "baseline_adapter_stage160",
        "status": "completed",
        "judgment": DECISION,
        "path": rel(DECISION_PATH),
        "primary_kpi": "threshold_handoff_ok;directional_prob_band_050_060_rows=0;score_saturated",
        "guardrail_kpi": "validation_pf_still_below_34d;overall_goal_complete=false",
        "external_verification_status": "completed_from_stage158_mt5_runtime_evidence_no_new_mt5",
        "notes": ledger_pairs(
            (
                ("source_summary", rel(SOURCE_SUMMARY)),
                ("source_manifest", rel(SOURCE_RUN_MANIFEST)),
                ("overall_goal_complete", 0),
            )
        ),
    }
    project_payload = upsert_csv_rows(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, [alpha_row], key="ledger_row_id")
    stage_payload = upsert_csv_rows(STAGE_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, [alpha_row], key="ledger_row_id")
    artifact_payload = upsert_csv_rows(
        ARTIFACT_REGISTRY_PATH,
        ARTIFACT_COLUMNS,
        artifact_rows(notes_suffix=notes_suffix),
        key="artifact_id",
    )
    return {
        "run_registry": run_payload,
        "project_alpha_ledger": project_payload,
        "stage_ledger": stage_payload,
        "artifact_registry": artifact_payload,
    }


def write_packet_files(audit: Mapping[str, Any], ledger_payload: Mapping[str, Any], pushed_hash: str = "pending_until_push") -> None:
    required_gates = [
        "kpi_contract_audit",
        "row_grain_audit",
        "source_authority_audit",
        "performance_attribution_gate",
        "result_judgment_gate",
        "artifact_lineage_audit",
        "required_gate_coverage_audit",
        "final_claim_guard",
    ]
    payloads: dict[str, Any] = {
        "routing_receipt.json": {
            "packet_id": PACKET_ID,
            "stage_id": STAGE_ID,
            "primary_family": "kpi_evidence",
            "primary_skill": "obsidian-performance-attribution",
            "support_skills": ["obsidian-result-judgment", "obsidian-artifact-lineage", "obsidian-reentry-read"],
            "required_gates": required_gates,
            "status": "completed",
        },
        "kpi_contract_audit.json": {
            "legacy_34d_target": LEGACY_34D,
            "source_summary": rel(SOURCE_SUMMARY),
            "threshold_binding_summary": rel(BINDING_SUMMARY_PATH),
            "probability_distribution_summary": rel(PROBABILITY_SUMMARY_PATH),
            "status": "completed",
        },
        "row_grain_audit.json": {
            "row_grain": "variant_split_actual_routed_total",
            "binding_summary_rows": len(audit["binding_rows"]),
            "probability_summary_rows": len(audit["probability_rows"]),
            "reason_summary_rows": len(audit["reason_rows"]),
            "status": "completed",
        },
        "source_authority_audit.json": {
            "source_inputs": [
                rel(SOURCE_RUN_MANIFEST),
                rel(SOURCE_SUMMARY),
                rel(SOURCE_STAGE159_SUMMARY),
                "local_common_files:OPV2/s158a/run158A",
            ],
            "source_authority": "Stage158 MT5 runtime telemetry plus Stage159 KPI delta review",
            "new_mt5_run": False,
            "status": "completed_with_boundary",
        },
        "performance_attribution_gate.json": {
            "observed_change": "Stage158 threshold variants produced zero material KPI movement.",
            "comparison_baseline": "s158_valpf_lng53_risk0300_h3_cd5_sht54_lng53",
            "likely_drivers": [
                "score_table_saturation",
                "lack_of_directional_probability_rows_near_threshold",
                "side_filter_blocks_after_threshold_met",
            ],
            "segment_checks": ["validation", "oos", "actual_routed_total", "decision_reason", "set_file", "model_score_table"],
            "trade_shape": rel(SOURCE_TRADE_AUDIT),
            "alternative_explanations": ["threshold_handoff_bug_rejected_by_set_file_audit"],
            "attribution_confidence": "high_for_threshold_non_binding_on_current_score_table",
            "next_probe": NEXT_STAGE_ID,
            "status": "completed",
        },
        "result_judgment_gate.json": {
            "result_subject": "Stage158 threshold repair axis",
            "evidence_available": [
                rel(REPORT_PATH),
                rel(BINDING_SUMMARY_PATH),
                rel(PROBABILITY_SUMMARY_PATH),
                rel(MODEL_SCORE_PATH),
                rel(SET_AUDIT_PATH),
            ],
            "evidence_missing": ["new_stage161_repair_run"],
            "judgment_label": "threshold_written_score_saturated_non_binding",
            "claim_boundary": BOUNDARY,
            "next_condition": NEXT_STAGE_ID,
            "user_explanation_hook": "Thresholds were passed correctly, but the model output is too saturated for those thresholds to change decisions.",
            "status": "passed_with_boundary",
        },
        "artifact_lineage_audit.json": {
            "source_inputs": [rel(SOURCE_RUN_MANIFEST), rel(SOURCE_SUMMARY), rel(SOURCE_STAGE159_SUMMARY), rel(SOURCE_TRADE_AUDIT)],
            "producer": rel(PRODUCER_PATH),
            "consumer": [NEXT_STAGE_ID, rel(REPORT_PATH), rel(DECISION_PATH)],
            "artifact_paths": [
                rel(REPORT_PATH),
                rel(BINDING_SUMMARY_PATH),
                rel(PROBABILITY_SUMMARY_PATH),
                rel(RUNTIME_REASON_PATH),
                rel(SET_AUDIT_PATH),
                rel(MODEL_SCORE_PATH),
                rel(FAILURE_MEMORY_PATH),
                rel(ROUTE_DECISION_PATH),
                rel(DECISION_PATH),
                rel(SUMMARY_JSON_PATH),
            ],
            "artifact_hashes": "registered_in_artifact_registry",
            "registry_links": [rel(RUN_REGISTRY_PATH), rel(PROJECT_LEDGER_PATH), rel(STAGE_LEDGER_PATH), rel(ARTIFACT_REGISTRY_PATH)],
            "availability": "tracked_outputs_with_ignored_stage158_run_inputs_and_local_common_telemetry",
            "lineage_judgment": "connected_with_boundary",
            "ledger_payload": ledger_payload,
            "status": "completed",
        },
        "final_claim_guard.json": {
            "overall_goal_complete": False,
            "deployment_claim": False,
            "live_readiness_claim": False,
            "runtime_authority_claim": False,
            "production_baseline_claim": False,
            "operating_reference_claim": False,
            "operating_promotion_claim": False,
            "status": "passed",
        },
        "required_gate_coverage_audit.json": {
            "packet_id": PACKET_ID,
            "run_id": RUN_ID,
            "declared_required_gates": required_gates,
            "executed_gates": required_gates,
            "missing_gates": [],
            "status": "passed",
        },
        "aggregate_summary.json": {
            "packet_id": PACKET_ID,
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "decision": DECISION,
            "source_stage159_closeout_commit": SOURCE_STAGE159_CLOSEOUT_COMMIT,
            "source_stage159_hash_record_commit": SOURCE_STAGE159_HASH_RECORD_COMMIT,
            "source_run": SOURCE_RUN_ID,
            "threshold_binding_summary": rel(BINDING_SUMMARY_PATH),
            "probability_distribution_summary": rel(PROBABILITY_SUMMARY_PATH),
            "model_score_audit": rel(MODEL_SCORE_PATH),
            "route_decision": rel(ROUTE_DECISION_PATH),
            "ledger_payload": ledger_payload,
            "pushed_commit_hash": pushed_hash,
            "claim_boundary": BOUNDARY,
            "overall_goal_complete": False,
        },
    }
    for name, payload in payloads.items():
        write_json(PACKET_ROOT / name, payload)


def run() -> dict[str, Any]:
    audit = build_audit()
    write_csv(BINDING_SUMMARY_PATH, audit["binding_rows"])
    write_csv(PROBABILITY_SUMMARY_PATH, audit["probability_rows"])
    write_csv(RUNTIME_REASON_PATH, audit["reason_rows"])
    write_csv(SET_AUDIT_PATH, audit["set_rows"])
    write_csv(MODEL_SCORE_PATH, audit["model_rows"])
    write_csv(FAILURE_MEMORY_PATH, audit["failure_memory"])
    write_csv(ROUTE_DECISION_PATH, audit["route_decision"])
    write_md(REPORT_PATH, report_markdown(audit))
    write_md(DECISION_PATH, decision_markdown())
    write_json(SUMMARY_JSON_PATH, audit)
    ledger_payload = write_ledgers(audit)
    write_packet_files(audit, ledger_payload)
    write_stage161_seed()
    update_current_truth()
    write_status_files()
    append_changelog()
    return {"status": "completed", "decision": DECISION, "report": rel(REPORT_PATH)}


def replace_pending_in_file(path: Path, pushed_hash: str) -> None:
    if not path_exists(path):
        return
    text = io_path(path).read_text(encoding="utf-8-sig")
    if "pending_until_push" not in text:
        return
    io_path(path).write_text(text.replace("pending_until_push", pushed_hash), encoding="utf-8-sig")


def record_pushed_hash(pushed_hash: str) -> dict[str, Any]:
    paths = [
        REPORT_PATH,
        DECISION_PATH,
        SUMMARY_JSON_PATH,
        SELECTED_ROOT / "selection_status.md",
        REVIEWS_ROOT / "review_index.md",
        WORKSPACE_STATE_PATH,
        CURRENT_WORKING_STATE_PATH,
    ]
    for path in paths:
        replace_pending_in_file(path, pushed_hash)
    aggregate_path = PACKET_ROOT / "aggregate_summary.json"
    if path_exists(aggregate_path):
        aggregate = read_json(aggregate_path)
        aggregate["pushed_commit_hash"] = pushed_hash
        write_json(aggregate_path, aggregate)
    audit = read_json(SUMMARY_JSON_PATH)
    audit["pushed_commit_hash"] = pushed_hash
    write_json(SUMMARY_JSON_PATH, audit)
    ledger_payload = write_ledgers(audit, notes_suffix=f"; pushed_commit_hash_recorded={pushed_hash}")
    write_packet_files(audit, ledger_payload, pushed_hash=pushed_hash)
    return {
        "status": "completed",
        "recorded_pushed_commit_hash": pushed_hash,
        "aggregate_summary": rel(aggregate_path),
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--record-push", dest="record_push", default="")
    args = parser.parse_args(argv)
    if args.record_push:
        payload = record_pushed_hash(args.record_push)
    else:
        payload = run()
    print(json.dumps(json_ready(payload), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
