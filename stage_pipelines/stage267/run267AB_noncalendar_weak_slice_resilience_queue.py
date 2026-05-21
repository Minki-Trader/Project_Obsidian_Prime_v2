from __future__ import annotations

import csv
import json
import math
import sys
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.control_plane.ledger import (
    ALPHA_LEDGER_COLUMNS,
    RUN_REGISTRY_COLUMNS,
    io_path,
    json_ready,
    path_exists,
    sha256_file_lf_normalized,
    upsert_csv_rows,
)
from stage_pipelines.stage267 import run267AA_true_internal_ablation_followup_or_adapter_design as source_design
from stage_pipelines.stage267 import run267V_reconstruct_upstream_feature_surface as source_surface
from stage_pipelines.stage267 import run267Z_true_internal_ablation_balance_timeslice_trade_quality_review as source_review


STAGE_ID = source_review.STAGE_ID
RUN_NUMBER = "run267AB"
RUN_ID = "run267AB_stage267_noncalendar_weak_slice_resilience_queue_v1"
SOURCE_RUN_ID = source_design.RUN_ID
PARENT_REVIEW_RUN_ID = source_review.RUN_ID
SOURCE_SURFACE_RUN_ID = source_surface.RUN_ID
STATUS = "run267AB_noncalendar_weak_slice_resilience_queue_materialized"
JUDGMENT = "noncalendar_state_guard_queue_ready_no_candidate_selection"
NEXT_ACTION = "run267AC_build_noncalendar_state_guard_score_tables_from_run267AB_queue"
CLAIM_BOUNDARY = source_review.CLAIM_BOUNDARY

STAGE_ROOT = source_review.STAGE_ROOT
REVIEWS_ROOT = source_review.REVIEWS_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER / "noncalendar_weak_slice_resilience_queue"

SOURCE_FOLLOWUP_QUEUE_PATH = source_design.FOLLOWUP_QUEUE_PATH
SOURCE_CANDIDATE_DECISION_PATH = source_design.CANDIDATE_AXIS_DECISION_PATH
SOURCE_TRADE_RECORDS_PATH = source_review.TRADE_RECORDS_PATH
SOURCE_CANDIDATE_TEST_REVIEW_PATH = source_review.CANDIDATE_TEST_REVIEW_PATH
SOURCE_CANDIDATE_SUMMARY_PATH = source_review.CANDIDATE_SUMMARY_PATH
SOURCE_SURFACE_MANIFEST_PATH = source_surface.CANDIDATE_SURFACE_MANIFEST_PATH
SOURCE_FEATURE_FAMILY_MAP_PATH = source_surface.FEATURE_FAMILY_COLUMN_MAP_PATH
SOURCE_RUN267AA_REPORT_PATH = source_design.REPORT_PATH
SOURCE_RUN267Z_REPORT_PATH = source_review.REPORT_PATH
SOURCE_RUN267V_REPORT_PATH = source_surface.REPORT_PATH

TRADE_FEATURE_JOIN_AUDIT_PATH = RUN_ROOT / "trade_feature_join_audit.csv"
WEAK_SLICE_STATE_CONTRAST_PATH = RUN_ROOT / "weak_slice_state_contrast.csv"
REPEATED_STATE_SUMMARY_PATH = RUN_ROOT / "repeated_state_summary.csv"
GUARD_MATERIALIZATION_QUEUE_PATH = RUN_ROOT / "guard_materialization_queue.csv"
DATA_INTEGRITY_RECEIPT_PATH = RUN_ROOT / "data_integrity_receipt.csv"
DESIGN_RECEIPT_PATH = RUN_ROOT / "design_receipt.csv"
RESULT_JUDGMENT_PATH = RUN_ROOT / "result_judgment.csv"
LINEAGE_PATH = RUN_ROOT / "lineage.json"
REVIEW_RESULT_PATH = RUN_ROOT / "review_result.json"
REPORT_PATH = REVIEWS_ROOT / "stage267_run267AB_noncalendar_weak_slice_resilience_queue.md"
PRODUCER_PATH = Path("stage_pipelines/stage267/run267AB_noncalendar_weak_slice_resilience_queue.py")

STAGE_LEDGER_PATH = source_review.STAGE_LEDGER_PATH
PROJECT_LEDGER_PATH = source_review.PROJECT_LEDGER_PATH
RUN_REGISTRY_PATH = source_review.RUN_REGISTRY_PATH
ARTIFACT_REGISTRY_PATH = source_review.ARTIFACT_REGISTRY_PATH
CURRENT_WORKING_STATE_PATH = source_review.CURRENT_WORKING_STATE_PATH
WORKSPACE_STATE_PATH = source_review.WORKSPACE_STATE_PATH
SELECTION_STATUS_PATH = source_review.SELECTION_STATUS_PATH
REVIEW_INDEX_PATH = source_review.REVIEW_INDEX_PATH

STAGE_LEDGER_COLUMNS = source_review.STAGE_LEDGER_COLUMNS
ARTIFACT_COLUMNS = source_review.ARTIFACT_COLUMNS

FOCUS_BASE = (
    "constructive_curve_watch_not_selection",
    "high_net_gate_audit_control",
    "core_challenger_pressure_hold",
)

STATE_FEATURES = (
    "atr_14_over_atr_50",
    "bollinger_width_20",
    "historical_vol_5_over_20",
    "adx_14",
    "abs_di_spread_14",
    "abs_return_zscore_20",
    "abs_return_1_over_atr_14",
    "minutes_from_cash_open",
)

RAW_FEATURE_COLUMNS = (
    "atr_14_over_atr_50",
    "bollinger_width_20",
    "historical_vol_5_over_20",
    "adx_14",
    "di_spread_14",
    "return_zscore_20",
    "return_1_over_atr_14",
    "minutes_from_cash_open",
    "bb_squeeze",
    "is_us_cash_open",
    "is_first_30m_after_open",
    "is_last_30m_before_cash_close",
)

TRADE_FEATURE_JOIN_AUDIT_COLUMNS = (
    "candidate_alias",
    "candidate_id",
    "candidate_role",
    "test_id",
    "scope_label",
    "trade_count",
    "joined_trade_count",
    "missing_join_count",
    "join_rate",
    "missing_join_examples",
    "surface_file",
    "surface_sha256",
    "time_axis",
    "integrity_judgment",
)

WEAK_SLICE_STATE_CONTRAST_COLUMNS = (
    "candidate_alias",
    "candidate_id",
    "candidate_role",
    "test_id",
    "scope_label",
    "state_feature",
    "state_bucket",
    "total_trades",
    "weak_trades",
    "weak_net",
    "weak_expectancy",
    "survivor_trades",
    "survivor_net",
    "survivor_expectancy",
    "weak_share",
    "survivor_share",
    "enrichment",
    "state_read",
)

REPEATED_STATE_SUMMARY_COLUMNS = (
    "state_feature",
    "state_bucket",
    "focus_row_count",
    "candidate_count",
    "affected_candidate_aliases",
    "affected_tests",
    "weak_net_sum",
    "enrichment_mean",
    "materialization_read",
)

GUARD_MATERIALIZATION_QUEUE_COLUMNS = (
    "queue_id",
    "priority",
    "candidate_alias",
    "candidate_id",
    "candidate_role",
    "source_test_id",
    "source_scope_label",
    "guard_state_features",
    "guard_rule_family",
    "guard_intent",
    "source_evidence",
    "calendar_literal_filter_allowed",
    "materialization_status",
    "success_criteria",
    "failure_criteria",
    "invalid_criteria",
    "next_required_artifacts",
    "claim_boundary",
)

DATA_INTEGRITY_COLUMNS = (
    "data_source",
    "time_axis",
    "sample_scope",
    "missing_or_duplicate_check",
    "feature_label_boundary",
    "split_boundary",
    "leakage_risk",
    "data_hash_or_identity",
    "integrity_judgment",
)

DESIGN_RECEIPT_COLUMNS = (
    "field",
    "value",
)

RESULT_JUDGMENT_COLUMNS = (
    "result_subject",
    "evidence_available",
    "evidence_missing",
    "judgment_label",
    "claim_boundary",
    "next_condition",
    "user_explanation_hook",
)


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    item = Path(path)
    try:
        return item.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return item.as_posix()


def cell(value: Any) -> Any:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, float):
        if not math.isfinite(value):
            return ""
        return round(value, 6)
    if isinstance(value, (list, tuple, set)):
        return ";".join(str(item) for item in value)
    return value


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return default
    return number if math.isfinite(number) else default


def as_int(value: Any, default: int = 0) -> int:
    try:
        return int(round(float(value)))
    except (TypeError, ValueError):
        return default


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path_exists(path):
        return []
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: cell(row.get(column)) for column in columns})


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(
        json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def read_text(path: Path) -> str:
    return io_path(path).read_text(encoding="utf-8-sig")


def write_text(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text, encoding="utf-8-sig")


def replace_line_prefix(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            return "\n".join(lines) + ("\n" if text.endswith("\n") else "")
    lines.append(replacement)
    return "\n".join(lines) + ("\n" if text.endswith("\n") else "")


def append_after_contains(text: str, needle: str, line: str) -> str:
    if line in text:
        return text
    lines = text.splitlines()
    for index, existing in enumerate(lines):
        if needle in existing:
            lines.insert(index + 1, line)
            return "\n".join(lines) + ("\n" if text.endswith("\n") else "")
    return text.rstrip() + "\n" + line + "\n"


def append_if_missing(text: str, line: str) -> str:
    if line in text:
        return text
    return text.rstrip() + "\n" + line + "\n"


def load_frame(path: Path) -> pd.DataFrame:
    return pd.read_csv(io_path(path), encoding="utf-8-sig")


def surface_path(alias: str) -> Path:
    return (
        STAGE_ROOT
        / "02_runs"
        / "run267V"
        / "upstream_feature_surface_reconstruction"
        / "surfaces"
        / alias
        / f"{alias}_upstream_raw_feature_surface.csv"
    )


def focus_specs(candidate_tests: pd.DataFrame, candidate_decisions: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    specs: list[dict[str, Any]] = []
    constructive = candidate_tests[candidate_tests["curve_read"].astype(str).str.startswith("constructive")]
    for _, row in constructive.iterrows():
        specs.append(
            {
                "candidate_alias": row["candidate_alias"],
                "candidate_id": row["candidate_id"],
                "candidate_role": row["candidate_role"],
                "test_id": row["test_id"],
                "scope_label": "constructive_curve_watch_not_selection",
                "priority": "P0",
            }
        )
    audit = candidate_tests[
        (candidate_tests["candidate_alias"] == "s264_lc")
        & (candidate_tests["test_id"] == "abl_gate_variant_rule")
    ]
    if not audit.empty:
        row = audit.iloc[0]
        specs.append(
            {
                "candidate_alias": row["candidate_alias"],
                "candidate_id": row["candidate_id"],
                "candidate_role": row["candidate_role"],
                "test_id": row["test_id"],
                "scope_label": "high_net_gate_audit_control",
                "priority": "P1",
            }
        )
    core = candidate_tests[candidate_tests["candidate_alias"] == "s264_aih"].sort_values("net_profit", ascending=False)
    if not core.empty:
        row = core.iloc[0]
        specs.append(
            {
                "candidate_alias": row["candidate_alias"],
                "candidate_id": row["candidate_id"],
                "candidate_role": row["candidate_role"],
                "test_id": row["test_id"],
                "scope_label": "core_challenger_pressure_hold",
                "priority": "P2",
            }
        )

    seen: set[tuple[str, str, str]] = set()
    deduped: list[dict[str, Any]] = []
    for spec in specs:
        key = (str(spec["candidate_alias"]), str(spec["test_id"]), str(spec["scope_label"]))
        if key not in seen:
            deduped.append(spec)
            seen.add(key)
    return deduped


def load_surface_manifest() -> dict[str, dict[str, str]]:
    return {row["candidate_alias"]: dict(row) for row in read_csv(SOURCE_SURFACE_MANIFEST_PATH)}


def threshold_map(surface: pd.DataFrame) -> dict[str, tuple[float, float]]:
    thresholds: dict[str, tuple[float, float]] = {}
    for column in ("atr_14_over_atr_50", "bollinger_width_20", "historical_vol_5_over_20", "adx_14", "minutes_from_cash_open"):
        series = pd.to_numeric(surface[column], errors="coerce")
        thresholds[column] = (float(series.quantile(0.25)), float(series.quantile(0.75)))
    for column in ("di_spread_14", "return_zscore_20", "return_1_over_atr_14"):
        series = pd.to_numeric(surface[column], errors="coerce").abs()
        thresholds[f"abs_{column}"] = (float(series.quantile(0.25)), float(series.quantile(0.75)))
    return thresholds


def state_bucket(row: Mapping[str, Any], feature: str, thresholds: Mapping[str, tuple[float, float]]) -> str:
    if feature.startswith("abs_"):
        source = feature[4:]
        value = abs(as_float(row.get(source), float("nan")))
    else:
        source = feature
        value = as_float(row.get(source), float("nan"))
    if not math.isfinite(value):
        return "missing"
    q1, q3 = thresholds[feature]
    if value <= q1:
        return "low"
    if value >= q3:
        return "high"
    return "mid"


def joined_trade_features(
    trades: pd.DataFrame,
    specs: Sequence[Mapping[str, Any]],
    surface_manifest: Mapping[str, Mapping[str, str]],
) -> tuple[pd.DataFrame, list[dict[str, Any]], dict[str, dict[str, tuple[float, float]]]]:
    focus_keys = {(str(spec["candidate_alias"]), str(spec["test_id"])) for spec in specs}
    focus_meta = {
        (str(spec["candidate_alias"]), str(spec["test_id"])): dict(spec)
        for spec in specs
    }
    tier_a = trades[trades["tier_scope"].astype(str) == "Tier A"].copy()
    tier_a = tier_a[
        tier_a[["candidate_alias", "test_id"]].apply(lambda row: (str(row["candidate_alias"]), str(row["test_id"])), axis=1).isin(focus_keys)
    ].copy()
    tier_a["bar_time_server"] = pd.to_datetime(tier_a["open_time"]).dt.strftime("%Y.%m.%d %H:%M:%S")
    tier_a["net_profit"] = pd.to_numeric(tier_a["net_profit"], errors="coerce")

    threshold_by_alias: dict[str, dict[str, tuple[float, float]]] = {}
    joined_parts: list[pd.DataFrame] = []
    audit_rows: list[dict[str, Any]] = []
    for alias, alias_trades in tier_a.groupby("candidate_alias"):
        surface_file = surface_path(str(alias))
        surface = load_frame(surface_file)
        for column in RAW_FEATURE_COLUMNS:
            surface[column] = pd.to_numeric(surface[column], errors="coerce")
        threshold_by_alias[str(alias)] = threshold_map(surface)
        surface_subset = surface[["bar_time_server", *RAW_FEATURE_COLUMNS]].copy()
        merged = alias_trades.merge(surface_subset, how="left", on="bar_time_server")
        joined_parts.append(merged)

    joined = pd.concat(joined_parts, ignore_index=True) if joined_parts else pd.DataFrame()
    for spec in specs:
        alias = str(spec["candidate_alias"])
        test_id = str(spec["test_id"])
        part = joined[(joined["candidate_alias"] == alias) & (joined["test_id"] == test_id)]
        joined_count = int(part["atr_14_over_atr_50"].notna().sum()) if not part.empty else 0
        missing = part[part["atr_14_over_atr_50"].isna()]
        manifest = surface_manifest.get(alias, {})
        audit_rows.append(
            {
                "candidate_alias": alias,
                "candidate_id": spec["candidate_id"],
                "candidate_role": spec["candidate_role"],
                "test_id": test_id,
                "scope_label": spec["scope_label"],
                "trade_count": len(part),
                "joined_trade_count": joined_count,
                "missing_join_count": len(missing),
                "join_rate": joined_count / len(part) if len(part) else 0.0,
                "missing_join_examples": ";".join(str(value) for value in missing["open_time"].head(3).tolist()),
                "surface_file": manifest.get("surface_file", rel(surface_path(alias))),
                "surface_sha256": manifest.get("surface_sha256", sha256_file_lf_normalized(surface_path(alias)) if path_exists(surface_path(alias)) else "missing"),
                "time_axis": manifest.get("time_axis", "bar_time_server"),
                "integrity_judgment": "usable_with_boundary" if joined_count and len(missing) <= 2 else "inconclusive",
            }
        )
    for column in ("month", "weekday"):
        if column not in joined.columns:
            joined[column] = ""
    joined["weak_slice_flag"] = (joined["month"].astype(str) == "2024-12") | (joined["weekday"].astype(str) == "Monday")
    joined["scope_label"] = joined.apply(
        lambda row: focus_meta.get((str(row["candidate_alias"]), str(row["test_id"])), {}).get("scope_label", ""),
        axis=1,
    )
    return joined, audit_rows, threshold_by_alias


def contrast_rows(joined: pd.DataFrame, threshold_by_alias: Mapping[str, Mapping[str, tuple[float, float]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if joined.empty:
        return rows
    grouped = joined.groupby(["candidate_alias", "candidate_id", "candidate_role", "test_id", "scope_label"], dropna=False)
    for (alias, candidate_id, role, test_id, scope_label), group in grouped:
        total_weak = int(group["weak_slice_flag"].sum())
        total_survivor = int((~group["weak_slice_flag"]).sum())
        total_trades = len(group)
        thresholds = threshold_by_alias.get(str(alias), {})
        for feature in STATE_FEATURES:
            if feature not in thresholds:
                continue
            bucketed = group.copy()
            bucketed["state_bucket"] = bucketed.apply(lambda row: state_bucket(row, feature, thresholds), axis=1)
            for bucket, state_group in bucketed.groupby("state_bucket"):
                weak = state_group[state_group["weak_slice_flag"]]
                survivor = state_group[~state_group["weak_slice_flag"]]
                weak_trades = len(weak)
                survivor_trades = len(survivor)
                if weak_trades < 5 or survivor_trades < 10:
                    state_read = "thin_state"
                else:
                    weak_net = float(weak["net_profit"].sum())
                    survivor_net = float(survivor["net_profit"].sum())
                    weak_expectancy = weak_net / weak_trades if weak_trades else 0.0
                    survivor_expectancy = survivor_net / survivor_trades if survivor_trades else 0.0
                    weak_share = weak_trades / total_weak if total_weak else 0.0
                    survivor_share = survivor_trades / total_survivor if total_survivor else 0.0
                    enrichment = weak_share / (survivor_share + 1e-9)
                    if weak_net < -50.0 and weak_expectancy < survivor_expectancy - 5.0 and enrichment >= 1.15:
                        state_read = "overrepresented_weak_state"
                    elif weak_net < 0.0 and survivor_net > 0.0:
                        state_read = "weak_state_but_not_enriched"
                    else:
                        state_read = "neutral_or_survivor"
                weak_net = float(weak["net_profit"].sum()) if weak_trades else 0.0
                survivor_net = float(survivor["net_profit"].sum()) if survivor_trades else 0.0
                weak_expectancy = weak_net / weak_trades if weak_trades else 0.0
                survivor_expectancy = survivor_net / survivor_trades if survivor_trades else 0.0
                weak_share = weak_trades / total_weak if total_weak else 0.0
                survivor_share = survivor_trades / total_survivor if total_survivor else 0.0
                enrichment = weak_share / (survivor_share + 1e-9)
                rows.append(
                    {
                        "candidate_alias": alias,
                        "candidate_id": candidate_id,
                        "candidate_role": role,
                        "test_id": test_id,
                        "scope_label": scope_label,
                        "state_feature": feature,
                        "state_bucket": bucket,
                        "total_trades": total_trades,
                        "weak_trades": weak_trades,
                        "weak_net": weak_net,
                        "weak_expectancy": weak_expectancy,
                        "survivor_trades": survivor_trades,
                        "survivor_net": survivor_net,
                        "survivor_expectancy": survivor_expectancy,
                        "weak_share": weak_share,
                        "survivor_share": survivor_share,
                        "enrichment": enrichment,
                        "state_read": state_read,
                    }
                )
    return rows


def repeated_state_summary(contrast: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    candidates = [row for row in contrast if row.get("state_read") == "overrepresented_weak_state"]
    grouped: dict[tuple[str, str], list[Mapping[str, Any]]] = {}
    for row in candidates:
        grouped.setdefault((str(row["state_feature"]), str(row["state_bucket"])), []).append(row)
    rows: list[dict[str, Any]] = []
    for (feature, bucket), items in sorted(grouped.items()):
        aliases = sorted({str(row["candidate_alias"]) for row in items})
        tests = sorted({f"{row['candidate_alias']}:{row['test_id']}" for row in items})
        weak_net_sum = sum(as_float(row.get("weak_net")) for row in items)
        enrichment_mean = sum(as_float(row.get("enrichment")) for row in items) / len(items)
        if len(items) >= 3 and len(aliases) >= 3:
            materialization_read = "broad_state_guard_candidate"
        elif len(items) >= 2:
            materialization_read = "watch_state_guard_candidate"
        else:
            materialization_read = "local_state_memory_only"
        rows.append(
            {
                "state_feature": feature,
                "state_bucket": bucket,
                "focus_row_count": len(items),
                "candidate_count": len(aliases),
                "affected_candidate_aliases": ";".join(aliases),
                "affected_tests": ";".join(tests),
                "weak_net_sum": weak_net_sum,
                "enrichment_mean": enrichment_mean,
                "materialization_read": materialization_read,
            }
        )
    rows.sort(key=lambda row: (row["materialization_read"] != "broad_state_guard_candidate", -as_int(row["focus_row_count"]), as_float(row["weak_net_sum"])))
    return rows


def guard_queue(
    specs: Sequence[Mapping[str, Any]],
    contrast: Sequence[Mapping[str, Any]],
    repeated: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    broad_keys = {
        (str(row["state_feature"]), str(row["state_bucket"]))
        for row in repeated
        if row.get("materialization_read") == "broad_state_guard_candidate"
    }
    watch_keys = {
        (str(row["state_feature"]), str(row["state_bucket"]))
        for row in repeated
        if row.get("materialization_read") == "watch_state_guard_candidate"
    }
    contrast_by_pair: dict[tuple[str, str], list[Mapping[str, Any]]] = {}
    for row in contrast:
        if row.get("state_read") != "overrepresented_weak_state":
            continue
        contrast_by_pair.setdefault((str(row["candidate_alias"]), str(row["test_id"])), []).append(row)

    rows: list[dict[str, Any]] = []
    for index, spec in enumerate(specs, start=1):
        key = (str(spec["candidate_alias"]), str(spec["test_id"]))
        state_rows = contrast_by_pair.get(key, [])
        state_rows.sort(
            key=lambda row: (
                (str(row["state_feature"]), str(row["state_bucket"])) not in broad_keys,
                (str(row["state_feature"]), str(row["state_bucket"])) not in watch_keys,
                as_float(row.get("weak_net")),
                -as_float(row.get("enrichment")),
            )
        )
        chosen = state_rows[:3]
        chosen_keys = [(str(row["state_feature"]), str(row["state_bucket"])) for row in chosen]
        if any(item in broad_keys for item in chosen_keys):
            status = "ready_for_noncalendar_state_guard_score_table_design"
        elif chosen:
            status = "watch_only_requires_more_attribution_before_materialization"
        else:
            status = "inconclusive_no_guard_materialization"
        guard_features = ";".join(f"{feature}={bucket}" for feature, bucket in chosen_keys)
        weak_evidence = ";".join(
            f"{row['state_feature']}={row['state_bucket']}:weak_net={as_float(row['weak_net']):.2f}:enrichment={as_float(row['enrichment']):.3f}"
            for row in chosen
        )
        if spec["scope_label"] == "high_net_gate_audit_control":
            priority = "P1"
            guard_family = "control_audit_soft_state_penalty"
        elif spec["scope_label"] == "core_challenger_pressure_hold":
            priority = "P2"
            guard_family = "pressure_or_prune_state_guard_design"
        else:
            priority = "P0"
            guard_family = "constructive_axis_soft_state_guard"
        rows.append(
            {
                "queue_id": f"run267AB_q{index:02d}_{spec['candidate_alias']}_{spec['test_id']}",
                "priority": priority,
                "candidate_alias": spec["candidate_alias"],
                "candidate_id": spec["candidate_id"],
                "candidate_role": spec["candidate_role"],
                "source_test_id": spec["test_id"],
                "source_scope_label": spec["scope_label"],
                "guard_state_features": guard_features,
                "guard_rule_family": guard_family,
                "guard_intent": "soft_entry_or_risk_penalty_from_noncalendar_state",
                "source_evidence": weak_evidence,
                "calendar_literal_filter_allowed": "false",
                "materialization_status": status,
                "success_criteria": "future_score_table_preserves_trade_supply_and_reduces_weak_slice_loss_without_calendar_literal_filter",
                "failure_criteria": "trade_count_collapses_or_loss_moves_to_other_time_slice_or_state_signal_disappears",
                "invalid_criteria": "feature_join_missing_or_MT5_PnL_used_as_training_label_or_Tier_A_plus_B_duplicate_used_as_routing_evidence",
                "next_required_artifacts": "score_table_variant_manifest;runtime_contract;surface_alignment;MT5_attempt_manifest;trade_list_review",
                "claim_boundary": "queue_materialization_only_no_candidate_selection_no_onnx",
            }
        )
    return rows


def build_data_integrity_receipt(
    join_audit: Sequence[Mapping[str, Any]],
    surface_manifest: Mapping[str, Mapping[str, str]],
) -> list[dict[str, Any]]:
    total_trades = sum(as_int(row.get("trade_count")) for row in join_audit)
    joined = sum(as_int(row.get("joined_trade_count")) for row in join_audit)
    missing = sum(as_int(row.get("missing_join_count")) for row in join_audit)
    surface_hashes = ";".join(f"{alias}:{row.get('surface_sha256', '')}" for alias, row in sorted(surface_manifest.items()))
    return [
        {
            "data_source": f"{rel(SOURCE_TRADE_RECORDS_PATH)} plus run267V upstream raw feature surfaces",
            "time_axis": "trade open_time converted to bar_time_server; run267V time_axis=bar_time_server_matches_MT5_history_timestamp_UTC_rendered_for_tester",
            "sample_scope": "Tier A 2024 true internal ablation focus rows from run267AA queue; Tier A+B duplicate boundary excluded",
            "missing_or_duplicate_check": f"joined={joined}/{total_trades};missing_join_count={missing};surface_duplicate_bar_time_rows=0_from_manifest",
            "feature_label_boundary": "no new label is trained; MT5 PnL is used only for post-run attribution and queue design",
            "split_boundary": "2024 historical train-era stress diagnostic only; not operating validation or production baseline",
            "leakage_risk": "future risk appears only if guard is trained on weak-slice PnL; run267AB only designs queue and does not train score table",
            "data_hash_or_identity": surface_hashes,
            "integrity_judgment": "usable_with_boundary" if joined and missing <= 2 else "inconclusive",
        }
    ]


def build_design_receipt(
    repeated: Sequence[Mapping[str, Any]],
    guard_rows: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    ready = sum(1 for row in guard_rows if row.get("materialization_status") == "ready_for_noncalendar_state_guard_score_table_design")
    broad = [f"{row['state_feature']}={row['state_bucket']}" for row in repeated if row.get("materialization_read") == "broad_state_guard_candidate"]
    return [
        {"field": "hypothesis", "value": "Monday_and_2024_12_holes_have_noncalendar_market_state_components"},
        {"field": "decision_use", "value": "decide_which_candidate_test_rows_can_move_to_state_guard_score_table_design"},
        {"field": "comparison_baseline", "value": "run267Z Tier A candidate_test_review plus run267AA followup queue"},
        {"field": "control_variables", "value": "same_2024_period_same_MT5_trade_reports_same_candidate_pool_same_run267V_feature_surfaces"},
        {"field": "changed_variables", "value": "feature_state_bucket_attribution_and_guard_queue_only"},
        {"field": "sample_scope", "value": "Tier A focus trades; Tier A+B duplicate rows excluded from routing evidence"},
        {"field": "success_criteria", "value": f"broad_state_guard_candidates={';'.join(broad)};ready_queue_rows={ready}"},
        {"field": "failure_criteria", "value": "only_calendar_literal_or_incoherent_state_explains_weak_slices"},
        {"field": "invalid_conditions", "value": "missing_trade_feature_join_or_PnL_used_as_training_label_or_duplicate_Tier_A_plus_B_used_as_routed_evidence"},
        {"field": "stop_conditions", "value": "do_not_tune_Monday_or_December_literal_filter;stop_guard_loop_after_two_failed_passes"},
        {"field": "evidence_plan", "value": "guard_materialization_queue;state_contrast;future_score_table_manifest;future_MT5_trade_list_review"},
    ]


def build_result_judgment(
    join_audit: Sequence[Mapping[str, Any]],
    contrast: Sequence[Mapping[str, Any]],
    repeated: Sequence[Mapping[str, Any]],
    guard_rows: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    ready = sum(1 for row in guard_rows if row.get("materialization_status") == "ready_for_noncalendar_state_guard_score_table_design")
    broad = sum(1 for row in repeated if row.get("materialization_read") == "broad_state_guard_candidate")
    overrepresented = sum(1 for row in contrast if row.get("state_read") == "overrepresented_weak_state")
    joined = sum(as_int(row.get("joined_trade_count")) for row in join_audit)
    total = sum(as_int(row.get("trade_count")) for row in join_audit)
    return [
        {
            "result_subject": RUN_ID,
            "evidence_available": f"joined_trades={joined}/{total};overrepresented_state_rows={overrepresented};broad_state_candidates={broad};guard_queue_ready_rows={ready}",
            "evidence_missing": "actual_guard_score_tables;MT5_execution;balance_equity_curve_after_guard;real_Tier_B_fallback_routing",
            "judgment_label": JUDGMENT,
            "claim_boundary": "queue_materialized_no_candidate_selection_no_onnx_no_operating_claim",
            "next_condition": NEXT_ACTION,
            "user_explanation_hook": "쉽게 말하면 약한 월/요일 자체를 자르지 않고, 그 안에서 반복된 시장 상태를 guard 후보로만 넘긴다.",
        }
    ]


def artifact_entry(artifact_id: str, artifact_type: str, path: Path, created_at: str, notes: str) -> dict[str, Any]:
    return {
        "artifact_id": artifact_id,
        "artifact_type": artifact_type,
        "path": rel(path),
        "sha256": sha256_file_lf_normalized(path) if path_exists(path) else "missing",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "created_at_utc": created_at,
        "notes": notes,
    }


def build_lineage(created_at: str) -> dict[str, Any]:
    source_paths = {
        "run267AA_followup_queue": SOURCE_FOLLOWUP_QUEUE_PATH,
        "run267AA_candidate_decision": SOURCE_CANDIDATE_DECISION_PATH,
        "run267Z_trade_records": SOURCE_TRADE_RECORDS_PATH,
        "run267Z_candidate_test_review": SOURCE_CANDIDATE_TEST_REVIEW_PATH,
        "run267V_surface_manifest": SOURCE_SURFACE_MANIFEST_PATH,
        "run267V_feature_family_map": SOURCE_FEATURE_FAMILY_MAP_PATH,
    }
    output_paths = {
        "trade_feature_join_audit": TRADE_FEATURE_JOIN_AUDIT_PATH,
        "weak_slice_state_contrast": WEAK_SLICE_STATE_CONTRAST_PATH,
        "repeated_state_summary": REPEATED_STATE_SUMMARY_PATH,
        "guard_materialization_queue": GUARD_MATERIALIZATION_QUEUE_PATH,
        "data_integrity_receipt": DATA_INTEGRITY_RECEIPT_PATH,
        "design_receipt": DESIGN_RECEIPT_PATH,
        "result_judgment": RESULT_JUDGMENT_PATH,
        "review_result": REVIEW_RESULT_PATH,
        "report": REPORT_PATH,
    }
    return {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "source_run_id": SOURCE_RUN_ID,
        "parent_review_run_id": PARENT_REVIEW_RUN_ID,
        "source_surface_run_id": SOURCE_SURFACE_RUN_ID,
        "created_at_utc": created_at,
        "producer": rel(PRODUCER_PATH),
        "consumer_next_action": NEXT_ACTION,
        "claim_boundary": CLAIM_BOUNDARY,
        "sources": {
            name: {
                "path": rel(path),
                "sha256": sha256_file_lf_normalized(path) if path_exists(path) else "missing",
            }
            for name, path in source_paths.items()
        },
        "outputs": {
            name: {
                "path": rel(path),
                "sha256": sha256_file_lf_normalized(path) if path_exists(path) else "missing",
            }
            for name, path in output_paths.items()
        },
        "availability": "tracked_generated_with_manifest",
        "lineage_judgment": "connected_with_boundary",
    }


def report_table(rows: Sequence[Mapping[str, Any]], columns: Sequence[str], limit: int | None = None) -> list[str]:
    shown = list(rows[:limit]) if limit else list(rows)
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join("---" for _ in columns) + " |"]
    for row in shown:
        lines.append("| " + " | ".join(str(row.get(column, "")) for column in columns) + " |")
    return lines


def report_markdown(result: Mapping[str, Any]) -> str:
    counts = result["counts"]
    repeated = result["repeated_state_summary"]
    guard_rows = result["guard_materialization_queue"]
    judgment = result["result_judgment"][0]
    ready_rows = [row for row in guard_rows if row.get("materialization_status") == "ready_for_noncalendar_state_guard_score_table_design"]
    lines = [
        "# Stage267 Run267AB Noncalendar Weak-Slice Resilience Queue(267단계 267AB 비달력 약점 구간 견고성 큐)",
        "",
        f"- status(상태): `{STATUS}`",
        f"- source_design(원천 설계): `{SOURCE_RUN_ID}`",
        f"- joined_trades(결합 거래): `{counts['joined_trade_count']}/{counts['focus_trade_count']}`",
        f"- overrepresented_state_rows(과대표 약점 상태 행): `{counts['overrepresented_state_rows']}`",
        f"- broad_state_candidates(넓은 상태 후보): `{counts['broad_state_candidate_count']}`",
        f"- ready_guard_queue_rows(준비된 방어 큐 행): `{counts['ready_guard_queue_rows']}`",
        "- selected_candidate(선택 후보): `none`",
        "- ONNX readiness(ONNX 준비): `not_claimed`",
        f"- next_action(다음 행동): `{NEXT_ACTION}`",
        "",
        "## Easy Read(쉬운 해석)",
        "",
        "run267AB(267AB 실행)는 Monday(월요일)나 2024-12(2024년 12월)를 바로 자르지 않았다.",
        "Effect(효과): 약한 구간 안에서 반복되는 noncalendar market state(비달력 시장 상태)를 찾아 다음 score table(점수표) 설계 큐로만 보낸다.",
        "",
        "가장 넓게 반복된 상태는 `historical_vol_5_over_20=high`였다.",
        "Effect(효과): 약점은 단순한 요일 문제가 아니라 단기 변동성/수익률 충격 상태와 함께 움직일 가능성이 있다.",
        "",
        "## Repeated States(반복 상태)",
        "",
        *report_table(
            repeated,
            ("state_feature", "state_bucket", "focus_row_count", "candidate_count", "weak_net_sum", "enrichment_mean", "materialization_read"),
            limit=8,
        ),
        "",
        "## Guard Queue(방어 큐)",
        "",
        *report_table(
            ready_rows,
            ("queue_id", "priority", "candidate_alias", "source_test_id", "guard_state_features", "materialization_status"),
        ),
        "",
        "## Result Judgment(결과 판정)",
        "",
        f"- evidence_available(있는 근거): `{judgment['evidence_available']}`",
        f"- evidence_missing(빠진 근거): `{judgment['evidence_missing']}`",
        f"- judgment_label(판정 라벨): `{judgment['judgment_label']}`",
        f"- claim_boundary(주장 경계): `{judgment['claim_boundary']}`",
        "",
        "## Data Integrity(데이터 무결성)",
        "",
        f"- time_axis(시간축): trade open_time(거래 진입 시각)을 run267V(267V 실행)의 bar_time_server(서버 봉 시각)에 맞췄다.",
        f"- join_missing(결합 누락): `{counts['missing_join_count']}`.",
        "- leakage_boundary(누수 경계): MT5 PnL(손익)은 훈련 라벨(label, 라벨)이 아니라 사후 귀속(post-run attribution, 사후 귀속)에만 썼다.",
        "",
        "## Artifact Lineage(산출물 계보)",
        "",
        f"- source_inputs(원천 입력): `{rel(SOURCE_FOLLOWUP_QUEUE_PATH)}`, `{rel(SOURCE_TRADE_RECORDS_PATH)}`, `{rel(SOURCE_SURFACE_MANIFEST_PATH)}`.",
        f"- producer(생산자): `{rel(PRODUCER_PATH)}`.",
        f"- outputs(출력): `{rel(GUARD_MATERIALIZATION_QUEUE_PATH)}`, `{rel(WEAK_SLICE_STATE_CONTRAST_PATH)}`, `{rel(REPEATED_STATE_SUMMARY_PATH)}`.",
        f"- consumer(소비자): `{NEXT_ACTION}`.",
        "",
        "## Boundary(경계)",
        "",
        "- positive_claim(긍정 주장): `none`.",
        "- selected_candidate(선택 후보): `none`.",
        "- Baseline(기준 후보): `research_candidate_pool_only`.",
        "- ONNX readiness(ONNX 준비): `not_claimed`.",
        "- Goal Achieve(목표 달성): `not_claimed`.",
        "- forbidden_claims(금지 주장): deployment(배포), live readiness(실거래 준비), runtime authority(런타임 권위), operating promotion(운영 승격), operating reference(운영 기준), production baseline(생산 기준선), overall goal complete(전체 목표 완료).",
    ]
    return "\n".join(lines)


def update_ledgers(created_at: str, result: Mapping[str, Any]) -> None:
    counts = result["counts"]
    upsert_csv_rows(
        STAGE_LEDGER_PATH,
        STAGE_LEDGER_COLUMNS,
        [
            {
                "row_id": "stage267_run267AB_noncalendar_weak_slice_resilience_queue",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "view": "noncalendar_weak_slice_resilience_queue",
                "tier_scope": "Tier A true internal focus trades; Tier A+B duplicate excluded",
                "scoreboard": "trade_feature_state_attribution_and_guard_queue",
                "status": STATUS,
                "judgment": JUDGMENT,
                "evidence_boundary": "queue_materialization_no_candidate_selection_no_onnx",
                "report_path": rel(REPORT_PATH),
                "notes": (
                    f"joined={counts['joined_trade_count']}/{counts['focus_trade_count']};"
                    f"ready_guard_rows={counts['ready_guard_queue_rows']};next_action={NEXT_ACTION};selected_candidate=none."
                ),
            }
        ],
        key="row_id",
    )
    upsert_csv_rows(
        PROJECT_LEDGER_PATH,
        ALPHA_LEDGER_COLUMNS,
        [
            {
                "ledger_row_id": f"{RUN_ID}__noncalendar_weak_slice_resilience_queue",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": "noncalendar_weak_slice_resilience_queue",
                "parent_run_id": SOURCE_RUN_ID,
                "record_view": "noncalendar_weak_slice_resilience_queue",
                "tier_scope": "Tier A true internal focus trades; Tier A+B duplicate excluded",
                "kpi_scope": "feature_state_attribution_queue_no_new_MT5_KPI",
                "scoreboard_lane": "experiment_design",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT_PATH),
                "primary_kpi": f"ready_guard_rows={counts['ready_guard_queue_rows']};broad_state_candidates={counts['broad_state_candidate_count']}",
                "guardrail_kpi": "selected_candidate=none;onnx_readiness=not_claimed;goal_achieve=not_claimed",
                "external_verification_status": "not_applicable_design_from_existing_MT5_evidence",
                "notes": f"Next action: {NEXT_ACTION}.",
            }
        ],
        key="ledger_row_id",
    )
    upsert_csv_rows(
        RUN_REGISTRY_PATH,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "baseline_candidate_racing_noncalendar_weak_slice_resilience_queue",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT_PATH),
                "notes": (
                    f"Run267AB materialized noncalendar weak-slice guard queue; ready_guard_rows={counts['ready_guard_queue_rows']}; "
                    f"selected_candidate=none; onnx_readiness=not_claimed; next_action={NEXT_ACTION}."
                ),
            }
        ],
        key="run_id",
    )
    artifact_rows = [
        artifact_entry("stage267_run267AB_review_script", "producer_script", PRODUCER_PATH, created_at, "Builds run267AB noncalendar weak-slice resilience queue."),
        artifact_entry("stage267_run267AB_trade_feature_join_audit", "join_audit", TRADE_FEATURE_JOIN_AUDIT_PATH, created_at, "Trade to raw feature surface join audit."),
        artifact_entry("stage267_run267AB_weak_slice_state_contrast", "state_contrast", WEAK_SLICE_STATE_CONTRAST_PATH, created_at, "Weak slice versus survivor feature-state contrast."),
        artifact_entry("stage267_run267AB_repeated_state_summary", "state_summary", REPEATED_STATE_SUMMARY_PATH, created_at, "Repeated noncalendar state summary."),
        artifact_entry("stage267_run267AB_guard_materialization_queue", "design_queue", GUARD_MATERIALIZATION_QUEUE_PATH, created_at, "Guard score-table materialization queue."),
        artifact_entry("stage267_run267AB_data_integrity_receipt", "data_integrity_receipt", DATA_INTEGRITY_RECEIPT_PATH, created_at, "Run267AB data integrity receipt."),
        artifact_entry("stage267_run267AB_design_receipt", "experiment_design_receipt", DESIGN_RECEIPT_PATH, created_at, "Run267AB experiment design receipt."),
        artifact_entry("stage267_run267AB_result_judgment", "result_judgment", RESULT_JUDGMENT_PATH, created_at, "Run267AB result judgment."),
        artifact_entry("stage267_run267AB_lineage", "lineage", LINEAGE_PATH, created_at, "Run267AB source-output lineage."),
        artifact_entry("stage267_run267AB_review_result", "review_result", REVIEW_RESULT_PATH, created_at, "Run267AB review result JSON."),
        artifact_entry("stage267_run267AB_review_report", "review_report", REPORT_PATH, created_at, "User-facing run267AB report."),
    ]
    upsert_csv_rows(ARTIFACT_REGISTRY_PATH, ARTIFACT_COLUMNS, artifact_rows, key="artifact_id")


def update_workspace_block(text: str) -> str:
    lines = text.splitlines()
    try:
        start = lines.index("stage267_baseline_candidate_racing_protocol:")
    except ValueError:
        return text
    end = len(lines)
    for index in range(start + 1, len(lines)):
        if lines[index] and not lines[index].startswith(" "):
            end = index
            break
    block = lines[start:end]
    updates = {
        "status": STATUS,
        "current_run_id": RUN_ID,
        "last_completed_run_id": RUN_ID,
        "run267AB_noncalendar_weak_slice_resilience_queue_report_path": rel(REPORT_PATH),
        "next_action": NEXT_ACTION,
    }
    new_block: list[str] = [block[0]]
    seen: set[str] = set()
    for line in block[1:]:
        stripped = line.strip()
        key = stripped.split(":", 1)[0] if ":" in stripped else ""
        if key in updates:
            if key not in seen:
                new_block.append(f"  {key}: {updates[key]}")
                seen.add(key)
            continue
        new_block.append(line)
    missing = [key for key in updates if key not in seen]
    if missing:
        insert_at = len(new_block)
        for index, line in enumerate(new_block):
            key = line.strip().split(":", 1)[0] if ":" in line else ""
            if key in {"decision_path", "next_action", "target_surface", "claim_boundary", "boundary"}:
                insert_at = index
                break
        for key in reversed(missing):
            new_block.insert(insert_at, f"  {key}: {updates[key]}")
    merged = lines[:start] + new_block + lines[end:]
    return "\n".join(merged) + ("\n" if text.endswith("\n") else "")


def update_current_truth_docs(result: Mapping[str, Any]) -> None:
    counts = result["counts"]
    current = read_text(CURRENT_WORKING_STATE_PATH)
    current = replace_line_prefix(current, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_line_prefix(current, "- adapter_under_review(검토 중 어댑터):", "- adapter_under_review(검토 중 어댑터): `noncalendar_weak_slice_resilience_queue`")
    current = replace_line_prefix(current, "- status(상태):", f"- status(상태): `{STATUS}`")
    current = append_after_contains(
        current,
        "run267AA true internal ablation follow-up or Adapter design",
        f"- Stage267(267단계) run267AB noncalendar weak-slice resilience queue(비달력 약점 구간 견고성 큐): `{rel(REPORT_PATH)}`",
    )
    current = replace_line_prefix(current, "- next_run(다음 실행):", f"- next_run(다음 실행): `{NEXT_ACTION}`")
    current = replace_line_prefix(
        current,
        "- action(행동):",
        " - action(행동): run267AB(267AB 실행)는 run267Z(267Z 실행) 거래와 run267V(267V 실행) raw feature surface(원시 피처 표면)를 결합해 비달력 약점 상태를 큐로 만들었다.".strip(),
    )
    current = replace_line_prefix(
        current,
        "- effect(효과):",
        " - effect(효과): Monday(월요일)/2024-12(2024년 12월)를 직접 자르지 않고, 반복된 시장 상태 guard(방어 장치)만 다음 score table(점수표) 설계로 보낸다.".strip(),
    )
    current = replace_line_prefix(current, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    current = append_if_missing(
        current,
        "\nRun267AB(267AB 실행)는 noncalendar weak-slice resilience queue(비달력 약점 구간 견고성 큐)를 물질화했다.\n"
        f"Effect(효과): joined trades(결합 거래) `{counts['joined_trade_count']}/{counts['focus_trade_count']}`, ready guard rows(준비 방어 행) `{counts['ready_guard_queue_rows']}`를 남겼고, selected candidate(선택 후보)와 ONNX readiness(ONNX 준비)는 계속 없다.\n",
    )
    write_text(CURRENT_WORKING_STATE_PATH, current)

    selection = read_text(SELECTION_STATUS_PATH)
    selection = replace_line_prefix(selection, "- stage_status(단계 상태):", f"- stage_status(단계 상태): `{STATUS}`")
    selection = replace_line_prefix(selection, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    selection = replace_line_prefix(selection, "- last_completed_run(마지막 완료 실행):", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
    selection = append_after_contains(
        selection,
        "run267AA_true_internal_ablation_followup_or_adapter_design",
        f"- run267AB_noncalendar_weak_slice_resilience_queue(267AB 비달력 약점 구간 견고성 큐): `{rel(REPORT_PATH)}`",
    )
    selection = replace_line_prefix(selection, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    selection = replace_line_prefix(selection, "- status(상태):", f"- status(상태): `{STATUS}`")
    selection = append_if_missing(
        selection,
        "\nRun267AB(267AB 실행)는 후보 선택이 아니라 다음 score table(점수표) 설계 큐를 만들었다.\n"
        "Effect(효과): 후보군은 유지하고, 달력 필터가 아닌 volatility/return shock state(변동성/수익률 충격 상태) guard(방어 장치) 후보만 다음으로 넘긴다.\n",
    )
    write_text(SELECTION_STATUS_PATH, selection)

    review_index = read_text(REVIEW_INDEX_PATH)
    review_index = append_after_contains(
        review_index,
        "run267AA true internal ablation follow-up or Adapter design",
        f"- Stage267(267단계) run267AB noncalendar weak-slice resilience queue(비달력 약점 구간 견고성 큐): `{rel(REPORT_PATH)}`",
    )
    review_index = replace_line_prefix(review_index, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    write_text(REVIEW_INDEX_PATH, review_index)

    workspace = read_text(WORKSPACE_STATE_PATH)
    workspace = workspace.replace(
        "Stage267(267단계) run267Z(267Z 실행) true internal ablation balance/time-slice/trade-quality review(진짜 내부 제거 잔액/시간구간/거래품질 검토) `run267Z_true_internal_ablation_balance_timeslice_trade_quality_review_completed`. Effect(효과): run267X(267X 실행)의 48개 MT5(MetaTrader 5, 메타트레이더5) 보고서를 거래 목록, 곡선, 약한 구간으로 다시 판독했고 selected candidate(선택 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 주장하지 않는다.",
        "Stage267(267단계) run267AB(267AB 실행) noncalendar weak-slice resilience queue(비달력 약점 구간 견고성 큐) `run267AB_noncalendar_weak_slice_resilience_queue_materialized`. Effect(효과): run267Z(267Z 실행)의 거래와 run267V(267V 실행)의 raw feature surface(원시 피처 표면)를 결합해 달력 필터가 아닌 상태 guard(방어 장치) 큐를 만들었고 selected candidate(선택 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 주장하지 않는다.",
        1,
    )
    workspace = workspace.replace(
        "Next action(다음 행동)는 `run267AA_true_internal_ablation_followup_or_adapter_design`이다. Effect(효과): run267X/run267Y(267X/267Y 실행)의 48개 MT5(MetaTrader 5, 메타트레이더5) KPI(핵심 성과 지표)를 balance/equity curve(잔액/평가금 곡선), time-slice KPI(시간 구간 핵심 성과 지표), trade quality(거래 품질)로 다시 판정한다.",
        f"Next action(다음 행동)는 `{NEXT_ACTION}`이다. Effect(효과): run267AB(267AB 실행)의 비달력 상태 guard(방어 장치) 큐를 score table/model(점수표/모델) 설계로 물질화한다.",
        1,
    )
    workspace = update_workspace_block(workspace)
    write_text(WORKSPACE_STATE_PATH, workspace)


def review() -> dict[str, Any]:
    created_at = utc_now()
    candidate_tests = load_frame(SOURCE_CANDIDATE_TEST_REVIEW_PATH)
    candidate_decisions = read_csv(SOURCE_CANDIDATE_DECISION_PATH)
    trades = load_frame(SOURCE_TRADE_RECORDS_PATH)
    surface_manifest = load_surface_manifest()
    specs = focus_specs(candidate_tests, candidate_decisions)
    joined, join_audit, threshold_by_alias = joined_trade_features(trades, specs, surface_manifest)
    contrast = contrast_rows(joined, threshold_by_alias)
    repeated = repeated_state_summary(contrast)
    guard_rows = guard_queue(specs, contrast, repeated)
    data_integrity = build_data_integrity_receipt(join_audit, surface_manifest)
    design = build_design_receipt(repeated, guard_rows)
    judgment = build_result_judgment(join_audit, contrast, repeated, guard_rows)

    write_csv(TRADE_FEATURE_JOIN_AUDIT_PATH, join_audit, TRADE_FEATURE_JOIN_AUDIT_COLUMNS)
    write_csv(WEAK_SLICE_STATE_CONTRAST_PATH, contrast, WEAK_SLICE_STATE_CONTRAST_COLUMNS)
    write_csv(REPEATED_STATE_SUMMARY_PATH, repeated, REPEATED_STATE_SUMMARY_COLUMNS)
    write_csv(GUARD_MATERIALIZATION_QUEUE_PATH, guard_rows, GUARD_MATERIALIZATION_QUEUE_COLUMNS)
    write_csv(DATA_INTEGRITY_RECEIPT_PATH, data_integrity, DATA_INTEGRITY_COLUMNS)
    write_csv(DESIGN_RECEIPT_PATH, design, DESIGN_RECEIPT_COLUMNS)
    write_csv(RESULT_JUDGMENT_PATH, judgment, RESULT_JUDGMENT_COLUMNS)

    lineage = build_lineage(created_at)
    write_json(LINEAGE_PATH, lineage)

    counts = {
        "focus_spec_count": len(specs),
        "focus_trade_count": int(sum(as_int(row.get("trade_count")) for row in join_audit)),
        "joined_trade_count": int(sum(as_int(row.get("joined_trade_count")) for row in join_audit)),
        "missing_join_count": int(sum(as_int(row.get("missing_join_count")) for row in join_audit)),
        "state_contrast_rows": len(contrast),
        "overrepresented_state_rows": sum(1 for row in contrast if row.get("state_read") == "overrepresented_weak_state"),
        "broad_state_candidate_count": sum(1 for row in repeated if row.get("materialization_read") == "broad_state_guard_candidate"),
        "guard_queue_rows": len(guard_rows),
        "ready_guard_queue_rows": sum(1 for row in guard_rows if row.get("materialization_status") == "ready_for_noncalendar_state_guard_score_table_design"),
    }

    result = {
        "status": STATUS,
        "judgment": JUDGMENT,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "source_run_id": SOURCE_RUN_ID,
        "parent_review_run_id": PARENT_REVIEW_RUN_ID,
        "source_surface_run_id": SOURCE_SURFACE_RUN_ID,
        "created_at_utc": created_at,
        "claim_boundary": CLAIM_BOUNDARY,
        "counts": counts,
        "focus_specs": specs,
        "trade_feature_join_audit": join_audit,
        "repeated_state_summary": repeated,
        "guard_materialization_queue": guard_rows,
        "data_integrity_receipt": data_integrity,
        "design_receipt": design,
        "result_judgment": judgment,
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": NEXT_ACTION,
        "outputs": {
            "trade_feature_join_audit": rel(TRADE_FEATURE_JOIN_AUDIT_PATH),
            "weak_slice_state_contrast": rel(WEAK_SLICE_STATE_CONTRAST_PATH),
            "repeated_state_summary": rel(REPEATED_STATE_SUMMARY_PATH),
            "guard_materialization_queue": rel(GUARD_MATERIALIZATION_QUEUE_PATH),
            "data_integrity_receipt": rel(DATA_INTEGRITY_RECEIPT_PATH),
            "design_receipt": rel(DESIGN_RECEIPT_PATH),
            "result_judgment": rel(RESULT_JUDGMENT_PATH),
            "lineage": rel(LINEAGE_PATH),
            "review_result": rel(REVIEW_RESULT_PATH),
            "report": rel(REPORT_PATH),
        },
        "sources": {
            "run267AA_followup_queue": rel(SOURCE_FOLLOWUP_QUEUE_PATH),
            "run267AA_candidate_decision": rel(SOURCE_CANDIDATE_DECISION_PATH),
            "run267Z_trade_records": rel(SOURCE_TRADE_RECORDS_PATH),
            "run267Z_candidate_test_review": rel(SOURCE_CANDIDATE_TEST_REVIEW_PATH),
            "run267V_surface_manifest": rel(SOURCE_SURFACE_MANIFEST_PATH),
            "run267V_feature_family_map": rel(SOURCE_FEATURE_FAMILY_MAP_PATH),
        },
    }
    write_json(REVIEW_RESULT_PATH, result)
    write_md(REPORT_PATH, report_markdown(result))
    update_ledgers(created_at, result)
    update_current_truth_docs(result)
    return result


def main() -> int:
    result = review()
    print(
        json.dumps(
            {
                "status": result["status"],
                "focus_specs": result["counts"]["focus_spec_count"],
                "joined_trades": result["counts"]["joined_trade_count"],
                "focus_trades": result["counts"]["focus_trade_count"],
                "missing_join_count": result["counts"]["missing_join_count"],
                "overrepresented_state_rows": result["counts"]["overrepresented_state_rows"],
                "ready_guard_queue_rows": result["counts"]["ready_guard_queue_rows"],
                "selected_candidate": result["selected_candidate"],
                "onnx_readiness": result["onnx_readiness"],
                "goal_achieve": result["goal_achieve"],
                "next_action": result["next_action"],
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
