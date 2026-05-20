from __future__ import annotations

import csv
import json
import math
import shutil
import sys
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Callable, Mapping, Sequence

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists, sha256_file_lf_normalized
from foundation.control_plane.mt5_tier_balance_completion import COMMON_FILES_ROOT_DEFAULT, attempt_payload, copy_to_common
from foundation.control_plane.mt5_trade_attribution import FEATURE_FRAME_PATH, _quantile_edges
from stage_pipelines.stage267 import historical_stress_2024_probe as input_probe


STAGE_ID = input_probe.STAGE_ID
RUN_ID = "run267C_stage267_execute_prioritized_ablation_replacement_variants_v1"
RUN_NUMBER = "run267C"
PACKET_ID = input_probe.PACKET_ID
CLAIM_BOUNDARY = input_probe.CLAIM_BOUNDARY
STAGE_ROOT = input_probe.STAGE_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER
VARIANT_ROOT = RUN_ROOT / "p0_mt5_variants"
REVIEWS_ROOT = input_probe.REVIEWS_ROOT
RUN267B_HIST_ROOT = input_probe.HIST_ROOT
STAGE_LEDGER_PATH = input_probe.STAGE_LEDGER_PATH
ARTIFACT_REGISTRY_PATH = input_probe.ARTIFACT_REGISTRY_PATH

BASE_FEATURE_MANIFEST_PATH = RUN267B_HIST_ROOT / "features.csv"
BASE_TRIAGE_PATH = RUN_ROOT / "candidate_counterfactual_triage_summary.csv"
BASE_COUNTERFACTUAL_PATH = RUN_ROOT / "weak_slice_counterfactual_kpi.csv"
VARIANT_DESIGN_MATRIX_PATH = VARIANT_ROOT / "p0_variant_design_matrix.csv"
FEATURE_VARIANT_MANIFEST_PATH = VARIANT_ROOT / "feature_variant_manifest.csv"
ATTEMPT_MANIFEST_PATH = VARIANT_ROOT / "attempts.csv"
RESULT_PATH = VARIANT_ROOT / "p0_mt5_variant_materialization.json"
VARIANT_MANIFEST_PATH = VARIANT_ROOT / "p0_mt5_variant_manifest.json"
REPORT_PATH = REVIEWS_ROOT / "stage267_run267C_p0_mt5_variant_materialization_report.md"
PRODUCER_PATH = Path("stage_pipelines/stage267/run267C_p0_mt5_variant_materialization.py")

RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
PROJECT_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
CURRENT_WORKING_STATE_PATH = Path("docs/context/current_working_state.md")
WORKSPACE_STATE_PATH = Path("docs/workspace/workspace_state.yaml")
SELECTION_STATUS_PATH = STAGE_ROOT / "04_selected" / "selection_status.md"
REVIEW_INDEX_PATH = REVIEWS_ROOT / "review_index.md"

STATUS = "stage267_run267C_p0_mt5_variant_materialized_execution_pending"
NEXT_ACTION = "run267C_execute_p0_mt5_variant_smoke_or_batch"
PERIOD_LABEL = input_probe.PERIOD_LABEL
COMMON_ROOT = "OPV2/s267c/run267C_p0"
SOURCE_SIGNAL_COLUMN = input_probe.SOURCE_SIGNAL_COLUMN


@dataclass(frozen=True)
class DiagnosticVariant:
    variant_id: str
    short_id: str
    source_intervention: str
    design_links: str
    weakness_axis: str
    weakness_bucket: str
    materialization_rule: str
    intent: str
    priority: str
    block_predicate: Callable[[Mapping[str, Any]], bool]


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    item = Path(path)
    try:
        return item.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return item.as_posix()


def csv_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, float):
        if math.isinf(value):
            return "inf"
        if not math.isfinite(value):
            return ""
        return f"{value:.12g}"
    if isinstance(value, (list, tuple)):
        return ";".join(str(item) for item in value)
    return str(value)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path_exists(path):
        return []
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: csv_value(row.get(column)) for column in columns})


def write_runtime_feature_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: csv_value(row.get(column)) for column in columns})


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(
        json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def replace_once(text: str, old: str, new: str) -> str:
    if old not in text:
        if new in text:
            return text
        raise ValueError(f"Missing text for replacement: {old}")
    return text.replace(old, new, 1)


def replace_any_once(text: str, olds: Sequence[str], new: str) -> str:
    if new in text:
        return text
    for old in olds:
        if old in text:
            return text.replace(old, new, 1)
    raise ValueError(f"Missing text for replacement options: {olds[0]}")


def append_line_after_anchor(text: str, anchor: str, line: str) -> str:
    if line in text:
        return text
    if anchor not in text:
        raise ValueError(f"Missing anchor: {anchor}")
    return text.replace(anchor, f"{anchor}\n{line}", 1)


def session_slice(minutes: Any) -> str:
    try:
        value = float(minutes)
    except (TypeError, ValueError):
        return "feature_missing"
    if not math.isfinite(value):
        return "feature_missing"
    if value > 0.0 and value <= 110.0:
        return "early"
    if value > 110.0 and value <= 220.0:
        return "mid"
    if value > 220.0 and value <= 330.0:
        return "late"
    return "outside_cash_session"


def volatility_regime(value: Any, edges: tuple[float, float] | None) -> str:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return "feature_missing"
    if not math.isfinite(number) or edges is None:
        return "feature_missing"
    low, high = edges
    if number <= low:
        return "vol_low"
    if number <= high:
        return "vol_mid"
    return "vol_high"


def load_volatility_edges() -> tuple[float, float] | None:
    frame = pd.read_parquet(io_path(REPO_ROOT / FEATURE_FRAME_PATH), columns=["historical_vol_20"])
    return _quantile_edges(frame["historical_vol_20"])


def source_context_by_bar_time(source: pd.DataFrame, volatility_edges: tuple[float, float] | None) -> dict[str, dict[str, Any]]:
    context: dict[str, dict[str, Any]] = {}
    for record in source.to_dict("records"):
        timestamp = pd.Timestamp(record["timestamp"])
        key = timestamp.strftime("%Y.%m.%d %H:%M:%S")
        context[key] = {
            "bar_time_server": key,
            "timestamp_utc": timestamp.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "month": timestamp.strftime("%Y-%m"),
            "weekday": timestamp.day_name(),
            "session_slice": session_slice(record.get("minutes_from_cash_open")),
            "volatility_regime": volatility_regime(record.get("historical_vol_20"), volatility_edges),
        }
    return context


def diagnostic_variants() -> tuple[DiagnosticVariant, ...]:
    return (
        DiagnosticVariant(
            variant_id="p0_july2024_entry_block_probe",
            short_id="julyblk",
            source_intervention="cf_remove_2024_07",
            design_links="d05_july_2024_holdout_stress",
            weakness_axis="month",
            weakness_bucket="2024-07",
            materialization_rule="entry signal(진입 신호)을 source bar month(원천 봉 월)이 2024-07(2024년 7월)이면 flat(무거래)으로 바꿈",
            intent="calendar holdout diagnostic(달력 보류 진단), repair(수리) 아님",
            priority="P0",
            block_predicate=lambda row: row.get("month") == "2024-07",
        ),
        DiagnosticVariant(
            variant_id="p0_late_session_entry_block_probe",
            short_id="lateblk",
            source_intervention="cf_remove_late_session",
            design_links="d07_late_session_interaction_engineering",
            weakness_axis="session_slice",
            weakness_bucket="late",
            materialization_rule="entry signal(진입 신호)을 source bar session_slice(원천 봉 세션 구간)가 late(후반)이면 flat(무거래)으로 바꿈",
            intent="late-session hard block(후반 세션 강제 차단) negative control(부정 대조군), engineering(엔지니어링) 전 진단",
            priority="P0",
            block_predicate=lambda row: row.get("session_slice") == "late",
        ),
        DiagnosticVariant(
            variant_id="p0_vol_low_entry_block_probe",
            short_id="vollowblk",
            source_intervention="cf_remove_vol_low",
            design_links="d01_vol_low_volatility_bandwidth_ablation;d02_vol_low_atr_to_historical_vol_replacement",
            weakness_axis="volatility_regime",
            weakness_bucket="vol_low",
            materialization_rule="entry signal(진입 신호)을 source bar volatility_regime(원천 봉 변동성 구간)가 vol_low(낮은 변동성)이면 flat(무거래)으로 바꿈",
            intent="vol_low cost diagnostic(낮은 변동성 비용 진단), candidate solution(후보 해결책) 아님",
            priority="P0",
            block_predicate=lambda row: row.get("volatility_regime") == "vol_low",
        ),
    )


def candidate_role_map() -> dict[str, str]:
    return {spec.candidate_id: spec.role for spec in input_probe.candidate_specs()}


def feature_manifest_by_candidate() -> dict[str, dict[str, str]]:
    return {row["candidate_id"]: row for row in read_csv_rows(BASE_FEATURE_MANIFEST_PATH)}


def triage_read_by_candidate_intervention() -> dict[tuple[str, str], dict[str, str]]:
    rows = read_csv_rows(BASE_COUNTERFACTUAL_PATH)
    return {(row.get("candidate_id", ""), row.get("intervention_id", "")): row for row in rows}


def transform_feature_file(
    source_feature_path: Path,
    destination: Path,
    variant: DiagnosticVariant,
    context: Mapping[str, Mapping[str, Any]],
) -> dict[str, Any]:
    rows = read_csv_rows(source_feature_path)
    if not rows:
        raise RuntimeError(f"empty source feature file: {source_feature_path}")
    columns = list(rows[0].keys())
    if SOURCE_SIGNAL_COLUMN not in columns:
        raise RuntimeError(f"missing source signal column: {source_feature_path}")

    transformed: list[dict[str, Any]] = []
    total_signal_rows = 0
    long_signal_rows = 0
    short_signal_rows = 0
    blocked_rows = 0
    blocked_signal_rows = 0
    blocked_long_signal_rows = 0
    blocked_short_signal_rows = 0
    context_missing_rows = 0
    for row in rows:
        current = dict(row)
        key = str(row.get("bar_time_server", ""))
        context_row = context.get(key)
        if context_row is None:
            context_missing_rows += 1
            should_block = False
        else:
            should_block = bool(variant.block_predicate(context_row))
        try:
            signal = int(round(float(row.get(SOURCE_SIGNAL_COLUMN) or 0.0)))
        except (TypeError, ValueError):
            signal = 0
        if signal != 0:
            total_signal_rows += 1
            if signal > 0:
                long_signal_rows += 1
            else:
                short_signal_rows += 1
        if should_block:
            blocked_rows += 1
            if signal != 0:
                blocked_signal_rows += 1
                if signal > 0:
                    blocked_long_signal_rows += 1
                else:
                    blocked_short_signal_rows += 1
            current[SOURCE_SIGNAL_COLUMN] = "0"
        transformed.append(current)

    write_runtime_feature_csv(destination, transformed, columns)
    kept_signal_rows = total_signal_rows - blocked_signal_rows
    return {
        "rows": len(rows),
        "source_feature_file": rel(source_feature_path),
        "feature_file": rel(destination),
        "feature_sha256": sha256_file_lf_normalized(destination),
        "feature_order": ";".join(columns[1:]),
        "feature_order_hash": input_probe.ordered_hash(tuple(columns[1:])),
        "total_signal_rows": total_signal_rows,
        "long_signal_rows": long_signal_rows,
        "short_signal_rows": short_signal_rows,
        "blocked_rows": blocked_rows,
        "blocked_signal_rows": blocked_signal_rows,
        "blocked_long_signal_rows": blocked_long_signal_rows,
        "blocked_short_signal_rows": blocked_short_signal_rows,
        "kept_signal_rows": kept_signal_rows,
        "signal_retention": kept_signal_rows / total_signal_rows if total_signal_rows else None,
        "context_missing_rows": context_missing_rows,
    }


def copy_model(source_model_path: Path, destination: Path) -> dict[str, Any]:
    if not path_exists(source_model_path):
        raise FileNotFoundError(source_model_path)
    io_path(destination.parent).mkdir(parents=True, exist_ok=True)
    shutil.copy2(io_path(source_model_path), io_path(destination))
    return {
        "source_model_file": rel(source_model_path),
        "model_file": rel(destination),
        "model_sha256": sha256_file_lf_normalized(destination),
    }


def build_attempts(
    specs: Sequence[Any],
    variants: Sequence[DiagnosticVariant],
    feature_exports: Mapping[tuple[str, str], Mapping[str, Any]],
    model_exports: Mapping[tuple[str, str], Mapping[str, Any]],
) -> list[dict[str, Any]]:
    attempts: list[dict[str, Any]] = []
    for variant_index, variant in enumerate(variants, start=1):
        for candidate_index, spec in enumerate(specs, start=1):
            key = (spec.candidate_id, variant.variant_id)
            for role_index, (tier, attempt_role, prefix, attempt_token) in enumerate(
                (
                    (input_probe.mt5.TIER_A, "tier_only_total", f"mt5_ta_{spec.alias}_{variant.short_id}", "ta"),
                    (input_probe.mt5.TIER_AB, "routed_total", f"mt5_rt_{spec.alias}_{variant.short_id}", "rt"),
                ),
                start=1,
            ):
                magic = 26730000 + variant_index * 1000 + candidate_index * 100 + role_index
                payload = attempt_payload(
                    run_root=VARIANT_ROOT,
                    run_id=RUN_ID,
                    stage_number=267,
                    exploration_label=f"stage267_BaselineRacing__{variant.variant_id}",
                    attempt_name=f"{spec.alias}_{variant.short_id}_{attempt_token}_2024",
                    tier=tier,
                    split=PERIOD_LABEL,
                    model_path=str(model_exports[key]["common_path"]),
                    model_id=f"{RUN_ID}_{spec.candidate_id}_{variant.variant_id}_entry_adapter_2024",
                    model_backend="ebm_table",
                    feature_path=str(feature_exports[key]["common_path"]),
                    feature_count=3,
                    feature_order_hash=str(feature_exports[key]["feature_order_hash"]),
                    short_threshold=spec.variant.short_threshold,
                    long_threshold=spec.variant.long_threshold,
                    min_margin=0.0,
                    invert_signal=False,
                    from_date="2024.01.02",
                    to_date="2025.01.01",
                    primary_active_tier="tier_a",
                    attempt_role=attempt_role,
                    record_view_prefix=prefix,
                    max_hold_bars=spec.variant.max_hold_bars,
                    common_root=f"{COMMON_ROOT}/{variant.short_id}/{spec.alias}",
                    fallback_enabled=False,
                    close_on_flat_signal=spec.variant.close_on_flat_signal,
                    reverse_on_opposite_signal=spec.variant.reverse_on_opposite_signal,
                    close_only_on_opposite_signal=spec.variant.close_only_on_opposite_signal,
                    extra_set_values=input_probe.base_extra_set_values(spec, magic),
                )
                payload["candidate_id"] = spec.candidate_id
                payload["candidate_alias"] = spec.alias
                payload["candidate_role"] = spec.role
                payload["diagnostic_variant_id"] = variant.variant_id
                payload["source_intervention"] = variant.source_intervention
                payload["design_links"] = variant.design_links
                attempts.append(payload)
    return attempts


def attempt_rows(attempts: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for attempt in attempts:
        rows.append(
            {
                "candidate_id": attempt.get("candidate_id"),
                "candidate_alias": attempt.get("candidate_alias"),
                "candidate_role": attempt.get("candidate_role"),
                "diagnostic_variant_id": attempt.get("diagnostic_variant_id"),
                "source_intervention": attempt.get("source_intervention"),
                "design_links": attempt.get("design_links"),
                "attempt_name": attempt.get("attempt_name"),
                "tier": attempt.get("tier"),
                "split": attempt.get("split"),
                "attempt_role": attempt.get("attempt_role"),
                "record_view_prefix": attempt.get("record_view_prefix"),
                "set_path": attempt.get("set", {}).get("path"),
                "set_sha256": attempt.get("set", {}).get("sha256"),
                "ini_path": attempt.get("ini", {}).get("path"),
                "ini_sha256": attempt.get("ini", {}).get("sha256"),
                "common_telemetry_path": attempt.get("common_telemetry_path"),
                "common_summary_path": attempt.get("common_summary_path"),
                "fallback_enabled": attempt.get("fallback_enabled", False),
                "execution_status": "not_executed",
            }
        )
    return rows


def build_design_matrix(
    feature_rows: Sequence[Mapping[str, Any]],
    variants: Sequence[DiagnosticVariant],
    triage_reads: Mapping[tuple[str, str], Mapping[str, str]],
) -> list[dict[str, Any]]:
    variant_by_id = {variant.variant_id: variant for variant in variants}
    rows: list[dict[str, Any]] = []
    for row in feature_rows:
        variant = variant_by_id[str(row["diagnostic_variant_id"])]
        triage = triage_reads.get((str(row["candidate_id"]), variant.source_intervention), {})
        rows.append(
            {
                "candidate_id": row.get("candidate_id"),
                "candidate_alias": row.get("candidate_alias"),
                "candidate_role": row.get("candidate_role"),
                "diagnostic_variant_id": variant.variant_id,
                "source_intervention": variant.source_intervention,
                "design_links": variant.design_links,
                "weakness_axis": variant.weakness_axis,
                "weakness_bucket": variant.weakness_bucket,
                "intent": variant.intent,
                "priority": variant.priority,
                "materialization_rule": variant.materialization_rule,
                "baseline_trade_count": triage.get("baseline_trade_count"),
                "baseline_net_profit": triage.get("baseline_net_profit"),
                "counterfactual_read": triage.get("counterfactual_read"),
                "counterfactual_trade_retention": triage.get("trade_retention"),
                "feature_signal_retention": row.get("signal_retention"),
                "blocked_signal_rows": row.get("blocked_signal_rows"),
                "kept_signal_rows": row.get("kept_signal_rows"),
                "mt5_execution_status": "pending",
                "selected_candidate": "none",
                "onnx_readiness": "not_claimed",
            }
        )
    return rows


def upsert_simple_csv(path: Path, key: str, row: Mapping[str, Any], columns: Sequence[str]) -> None:
    rows = read_csv_rows(path)
    merged = [item for item in rows if item.get(key) != row.get(key)]
    merged.append(row)
    write_csv(path, merged, columns)


def upsert_stage_ledger() -> None:
    row = {
        "row_id": "stage267_run267C_p0_mt5_variant_materialization",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "view": "p0_mt5_variant_materialization",
        "tier_scope": "Tier A and Tier A+B historical 2024 diagnostic attempts planned",
        "scoreboard": "experiment_materialization",
        "status": "completed_input_materialized_mt5_execution_pending",
        "judgment": "materialized_not_yet_mt5_evaluated_no_candidate_selection",
        "evidence_boundary": "set_ini_feature_variant_manifest_only_no_mt5_kpi_yet",
        "report_path": rel(REPORT_PATH),
        "notes": "P0 diagnostic MT5 variants materialized from run267C counterfactual triage; selected candidate none.",
    }
    rows = input_probe.read_csv_rows(STAGE_LEDGER_PATH)
    merged = [item for item in rows if item.get("row_id") != row["row_id"]]
    merged.append(row)
    input_probe.write_csv(
        STAGE_LEDGER_PATH,
        merged,
        (
            "row_id",
            "stage_id",
            "run_id",
            "view",
            "tier_scope",
            "scoreboard",
            "status",
            "judgment",
            "evidence_boundary",
            "report_path",
            "notes",
        ),
    )


def upsert_run_registers(feature_rows: Sequence[Mapping[str, Any]], attempts: Sequence[Mapping[str, Any]]) -> None:
    upsert_simple_csv(
        RUN_REGISTRY_PATH,
        "run_id",
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "lane": "baseline_candidate_racing_p0_mt5_variant_materialization",
            "status": STATUS,
            "judgment": "materialized_not_yet_mt5_evaluated_no_candidate_selection",
            "path": rel(REPORT_PATH),
            "notes": "P0 diagnostic MT5 variants materialized from weak-slice triage; no MT5 KPI yet and no operating meaning.",
        },
        ("run_id", "stage_id", "lane", "status", "judgment", "path", "notes"),
    )
    upsert_simple_csv(
        PROJECT_LEDGER_PATH,
        "ledger_row_id",
        {
            "ledger_row_id": f"{RUN_ID}__p0_mt5_variant_materialization",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "p0_mt5_variant_materialization",
            "parent_run_id": RUN_ID,
            "record_view": "p0_mt5_variant_materialization",
            "tier_scope": "Tier A and Tier A+B historical 2024 diagnostic attempts planned",
            "kpi_scope": "set_ini_feature_materialization",
            "scoreboard_lane": "experiment_materialization",
            "status": "completed_input_materialized_mt5_execution_pending",
            "judgment": "materialized_not_yet_mt5_evaluated_no_candidate_selection",
            "path": rel(REPORT_PATH),
            "primary_kpi": f"feature_variants={len(feature_rows)};attempts={len(attempts)}",
            "guardrail_kpi": "selected_candidate=none;onnx_readiness=not_claimed;mt5_execution=pending",
            "external_verification_status": "out_of_scope_by_claim",
            "notes": "Feature CSV, model copy, set and ini files materialized only; actual MT5 tester execution is next.",
        },
        (
            "ledger_row_id",
            "stage_id",
            "run_id",
            "subrun_id",
            "parent_run_id",
            "record_view",
            "tier_scope",
            "kpi_scope",
            "scoreboard_lane",
            "status",
            "judgment",
            "path",
            "primary_kpi",
            "guardrail_kpi",
            "external_verification_status",
            "notes",
        ),
    )


def upsert_artifacts(created_at: str) -> None:
    entries = (
        ("stage267_run267C_p0_mt5_variant_materializer", "producer_script", PRODUCER_PATH, "Builds run267C P0 diagnostic MT5 variants."),
        ("stage267_run267C_p0_variant_manifest", "run_manifest", VARIANT_MANIFEST_PATH, "Run267C P0 MT5 variant manifest."),
        ("stage267_run267C_p0_design_matrix", "variant_design_matrix", VARIANT_DESIGN_MATRIX_PATH, "P0 variant design matrix linked to counterfactual triage."),
        ("stage267_run267C_p0_feature_variant_manifest", "feature_variant_manifest", FEATURE_VARIANT_MANIFEST_PATH, "Feature/model/common file manifest for P0 variants."),
        ("stage267_run267C_p0_attempt_manifest", "attempt_manifest", ATTEMPT_MANIFEST_PATH, "MT5 set/ini attempt manifest for P0 variants."),
        ("stage267_run267C_p0_materialization_result", "review_result", RESULT_PATH, "JSON payload for P0 MT5 variant materialization."),
        ("stage267_run267C_p0_materialization_report", "review_report", REPORT_PATH, "User-facing P0 MT5 variant materialization report."),
    )
    rows = input_probe.read_csv_rows(ARTIFACT_REGISTRY_PATH)
    new_rows: list[dict[str, Any]] = []
    for artifact_id, artifact_type, path, notes in entries:
        new_rows.append(
            {
                "artifact_id": artifact_id,
                "artifact_type": artifact_type,
                "path": rel(path),
                "sha256": sha256_file_lf_normalized(path) if path_exists(path) else "missing",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": created_at,
                "notes": notes,
            }
        )
    replacement = {row["artifact_id"]: row for row in new_rows}
    merged = [row for row in rows if row.get("artifact_id") not in replacement]
    merged.extend(new_rows)
    input_probe.write_csv(
        ARTIFACT_REGISTRY_PATH,
        merged,
        ("artifact_id", "artifact_type", "path", "sha256", "stage_id", "run_id", "created_at_utc", "notes"),
    )


def update_current_truth_docs() -> None:
    current_text = io_path(CURRENT_WORKING_STATE_PATH).read_text(encoding="utf-8-sig")
    current_text = replace_any_once(
        current_text,
        (
            "- status(상태): `stage267_run267C_weak_slice_counterfactual_triage_completed_mt5_variants_pending`",
            "- status(상태): `stage267_run267C_p0_mt5_variant_smoke_blocked`",
        ),
        f"- status(상태): `{STATUS}`",
    )
    current_text = append_line_after_anchor(
        current_text,
        "- Stage267(267단계) run267C weak-slice counterfactual triage(약점 구간 반사실 선별): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267C_weak_slice_counterfactual_triage_report.md`",
        "- Stage267(267단계) run267C P0 MT5 variant materialization(우선순위 0 MT5 변형 물질화): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267C_p0_mt5_variant_materialization_report.md`",
    )
    current_text = replace_any_once(
        current_text,
        (
            "- action(행동): run267B(267B 실행) 2024 routed trade records(라우팅 거래 기록)로 weak-slice counterfactual triage(약점 구간 반사실 선별)를 실행했다.",
            "- action(행동): run267C(267C 실행) P0 MT5 smoke execution(우선순위 0 MT5 스모크 실행)을 `1`개 attempt(시도)로 수행했다.",
        ),
        "- action(행동): run267C(267C 실행) 반사실 선별에서 나온 P0(우선순위 0) 축을 MT5 set/ini(설정/초기화)와 feature CSV(피처 표) 진단 변형으로 물질화했다.",
    )
    current_text = replace_any_once(
        current_text,
        (
            "- effect(효과): naive filter(단순 필터)로 좋아 보이는 축과 trade count collapse(거래 수 붕괴)를 일으키는 축을 분리해, 다음 MT5 variant(MT5 변형) 물질화 우선순위를 좁혔다.",
            "- effect(효과): `0`개 KPI(핵심 성과 지표) 기록을 확보했지만 full P0 batch(전체 우선순위 0 묶음)와 후보 선택은 아직 아니다.",
        ),
        "- effect(효과): July 2024(2024년 7월), late session(후반 세션), vol_low(낮은 변동성) hard block(강제 차단)을 실제 테스터 입력으로 만들었지만, 이것은 후보 해결책이 아니라 진단 실행 대기 상태다.",
    )
    current_text = replace_any_once(
        current_text,
        (
            "- next_action(다음 행동): `run267C_materialize_p0_mt5_variants_from_counterfactual_triage`. Effect(효과): counterfactual(반사실)로 좁힌 P0(우선순위 0) 축을 실제 MT5 rerun(MT5 재실행) 후보로 만든다.",
            "- next_action(다음 행동): `run267C_repair_p0_mt5_smoke_execution_blocker`. Effect(효과): 좁은 MT5 smoke(스모크) 결과를 먼저 검토하고, 전체 batch(묶음 실행)로 넓힐지 blocker(차단 원인)를 고칠지 결정한다.",
        ),
        f"- next_action(다음 행동): `{NEXT_ACTION}`. Effect(효과): 물질화된 P0(우선순위 0) 변형을 좁은 MT5 Strategy Tester(전략 테스터) 실행으로 검증해 반사실 착시와 실제 런타임 결과를 분리한다.",
    )
    write_md(CURRENT_WORKING_STATE_PATH, current_text)

    selection_text = io_path(SELECTION_STATUS_PATH).read_text(encoding="utf-8-sig")
    selection_text = replace_any_once(
        selection_text,
        (
            "- stage_status(단계 상태): `run267C_weak_slice_counterfactual_triage_completed_mt5_variants_pending`",
            "- stage_status(단계 상태): `run267C_p0_mt5_variant_smoke_blocked`",
        ),
        "- stage_status(단계 상태): `run267C_p0_mt5_variant_materialized_execution_pending`",
    )
    selection_text = append_line_after_anchor(
        selection_text,
        "- run267C_counterfactual_triage(267C 반사실 선별): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267C_weak_slice_counterfactual_triage_report.md`",
        "- run267C_p0_mt5_variant_materialization(267C 우선순위 0 MT5 변형 물질화): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267C_p0_mt5_variant_materialization_report.md`",
    )
    selection_text = replace_any_once(
        selection_text,
        (
            "- next_action(다음 행동): `run267C_materialize_p0_mt5_variants_from_counterfactual_triage`",
            "- next_action(다음 행동): `run267C_repair_p0_mt5_smoke_execution_blocker`",
        ),
        f"- next_action(다음 행동): `{NEXT_ACTION}`",
    )
    selection_text = replace_any_once(
        selection_text,
        (
            "Run267C(267C 실행)는 run267B(267B 실행)의 routed trade records(라우팅 거래 기록)로 weak-slice counterfactual triage(약점 구간 반사실 선별)를 완료했다.",
            "Run267C(267C 실행)는 P0 MT5 smoke execution(우선순위 0 MT5 스모크 실행)을 좁게 수행했다.",
        ),
        "Run267C(267C 실행)는 weak-slice counterfactual triage(약점 구간 반사실 선별)에 이어 P0 MT5 variant materialization(우선순위 0 MT5 변형 물질화)을 완료했다.",
    )
    selection_text = replace_any_once(
        selection_text,
        (
            "Effect(효과): 선택 후보(selected candidate, 선택 후보)는 계속 없고, 다음은 실제 MT5 variant(MT5 변형) 물질화다.",
            "Effect(효과): 선택 후보(selected candidate, 선택 후보)는 계속 없고, 다음은 스모크 결과 검토 또는 실행 차단 복구다.",
        ),
        "Effect(효과): 선택 후보(selected candidate, 선택 후보)는 계속 없고, 다음은 물질화된 진단 변형의 MT5 Strategy Tester(전략 테스터) 실행이다.",
    )
    write_md(SELECTION_STATUS_PATH, selection_text)

    review_text = io_path(REVIEW_INDEX_PATH).read_text(encoding="utf-8-sig")
    review_text = replace_any_once(
        review_text,
        (
            "- status(상태): `run267C_weak_slice_counterfactual_triage_completed_mt5_variants_pending`",
            "- status(상태): `run267C_p0_mt5_variant_smoke_blocked`",
        ),
        "- status(상태): `run267C_p0_mt5_variant_materialized_execution_pending`",
    )
    review_text = append_line_after_anchor(
        review_text,
        "- run267C_weak_slice_counterfactual_triage(267C 약점 구간 반사실 선별): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267C_weak_slice_counterfactual_triage_report.md`",
        "- run267C_p0_mt5_variant_materialization(267C 우선순위 0 MT5 변형 물질화): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267C_p0_mt5_variant_materialization_report.md`",
    )
    review_text = replace_once(
        review_text,
        "Run267C(267C 실행)는 run267B(267B 실행)의 2024 routed trade records(라우팅 거래 기록)로 weak-slice counterfactual triage(약점 구간 반사실 선별)를 완료했다.",
        "Run267C(267C 실행)는 반사실 선별 이후 P0 MT5 variant materialization(우선순위 0 MT5 변형 물질화)을 완료했다.",
    )
    review_text = replace_any_once(
        review_text,
        (
            "Effect(효과): Stage267(267단계)는 후보 선택(selected candidate, 선택 후보), ONNX readiness(ONNX 준비), runtime authority(런타임 권위)를 주장하지 않고, `run267C_materialize_p0_mt5_variants_from_counterfactual_triage`로 넘어간다.",
            "Effect(효과): Stage267(267단계)는 후보 선택(selected candidate, 선택 후보), ONNX readiness(ONNX 준비), runtime authority(런타임 권위)를 주장하지 않고, `run267C_repair_p0_mt5_smoke_execution_blocker`로 넘어간다.",
        ),
        f"Effect(효과): Stage267(267단계)는 후보 선택(selected candidate, 선택 후보), ONNX readiness(ONNX 준비), runtime authority(런타임 권위)를 주장하지 않고, `{NEXT_ACTION}`로 넘어간다.",
    )
    write_md(REVIEW_INDEX_PATH, review_text)

    workspace_text = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    workspace_text = replace_any_once(
        workspace_text,
        (
            "Stage267(267단계) run267C(267C 실행) weak-slice counterfactual triage(약점 구간 반사실 선별) completed(완료).",
            "Stage267(267단계) run267C(267C 실행) P0 MT5 smoke execution(우선순위 0 MT5 스모크 실행) `blocked`.",
        ),
        "Stage267(267단계) run267C(267C 실행) P0 MT5 variant materialization(우선순위 0 MT5 변형 물질화) completed(완료).",
    )
    workspace_text = replace_any_once(
        workspace_text,
        (
            "Effect(효과): run267B(267B 실행) trade records(거래 기록)를 이용해 naive weak-slice filter(단순 약점 구간 필터)가 후보 개선처럼 보이는지 먼저 분리했지만 selected candidate(선택 후보)나 ONNX readiness(ONNX 준비)는 주장하지 않는다.",
            "Effect(효과): `1`개 attempt(시도)를 실제 MT5 Strategy Tester(전략 테스터)로 좁게 확인했고, `0`개 KPI(핵심 성과 지표)를 확보했지만 selected candidate(선택 후보)나 ONNX readiness(ONNX 준비)는 주장하지 않는다.",
        ),
        "Effect(효과): July 2024(2024년 7월), late session(후반 세션), vol_low(낮은 변동성) 진단 변형 15개와 MT5 set/ini(설정/초기화) attempt(시도) 30개를 만들었지만 selected candidate(선택 후보)나 ONNX readiness(ONNX 준비)는 주장하지 않는다.",
    )
    workspace_text = replace_any_once(
        workspace_text,
        (
            "Next action(다음 행동)는 `run267C_materialize_p0_mt5_variants_from_counterfactual_triage`이다.",
            "Next action(다음 행동)는 `run267C_repair_p0_mt5_smoke_execution_blocker`이다.",
        ),
        f"Next action(다음 행동)는 `{NEXT_ACTION}`이다.",
    )
    workspace_text = replace_any_once(
        workspace_text,
        (
            "active_run267C_weak_slice_counterfactual_triage_completed_mt5_variants_pending(267C 약점 구간 반사실 선별 완료 후 MT5 변형 대기 활성).",
            "active_run267C_p0_mt5_variant_smoke_blocked(267C 우선순위 0 MT5 스모크 실행 후 검토 활성).",
        ),
        "active_run267C_p0_mt5_variant_materialized_execution_pending(267C 우선순위 0 MT5 변형 물질화 완료 후 실행 대기 활성).",
    )
    write_md(WORKSPACE_STATE_PATH, workspace_text)


def build_report(
    result: Mapping[str, Any],
    design_rows: Sequence[Mapping[str, Any]],
    feature_rows: Sequence[Mapping[str, Any]],
) -> str:
    variant_count = result["diagnostic_variant_count"]
    feature_count = result["feature_variant_count"]
    attempt_count = result["attempt_count"]
    avg_retention = sum(float(row.get("signal_retention") or 0.0) for row in feature_rows) / max(len(feature_rows), 1)
    lines = [
        "# Stage267 Run267C P0 MT5 Variant Materialization(267단계 267C 우선순위 0 MT5 변형 물질화)",
        "",
        "- action(행동): run267C(267C 실행) 반사실 선별에서 나온 P0(우선순위 0) 축을 feature CSV(피처 표), model copy(모델 복사), set/ini(설정/초기화)로 물질화했다.",
        "- effect(효과): 다음 MT5 Strategy Tester(전략 테스터) 실행이 말로 된 계획이 아니라 고정된 파일 정체성(file identity, 파일 정체성)을 가진 attempt(시도)로 이어진다.",
        f"- diagnostic_variants(진단 변형): `{variant_count}`",
        f"- feature_variants(피처 변형): `{feature_count}`",
        f"- mt5_attempts(MT5 시도): `{attempt_count}`",
        f"- average_signal_retention(평균 신호 유지율): `{avg_retention:.4f}`",
        f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
        "",
        "## What Was Materialized(물질화 내용)",
        "",
        "| variant(변형) | source(원천) | rule(규칙) | intent(의도) |",
        "| --- | --- | --- | --- |",
    ]
    seen: set[str] = set()
    for row in design_rows:
        variant_id = str(row.get("diagnostic_variant_id"))
        if variant_id in seen:
            continue
        seen.add(variant_id)
        lines.append(
            f"| `{variant_id}` | `{row.get('source_intervention')}` | {row.get('materialization_rule')} | `{row.get('intent')}` |"
        )
    lines.extend(
        [
            "",
            "## Candidate Signal Cost(후보별 신호 비용)",
            "",
            "| candidate(후보) | variant(변형) | blocked signals(차단 신호) | kept signals(유지 신호) | retention(유지율) | counterfactual read(반사실 판독) |",
            "| --- | --- | ---: | ---: | ---: | --- |",
        ]
    )
    for row in design_rows:
        lines.append(
            f"| `{row.get('candidate_alias')}` | `{row.get('diagnostic_variant_id')}` | {row.get('blocked_signal_rows')} | {row.get('kept_signal_rows')} | {row.get('feature_signal_retention')} | `{row.get('counterfactual_read')}` |"
        )
    lines.extend(
        [
            "",
            "## Boundary(경계)",
            "",
            "- 이 결과는 MT5 input materialization(MT5 입력 물질화)이다. Effect(효과): 아직 MT5 KPI(MT5 핵심 성과 지표), balance/equity curve(잔액/평가금 곡선), trade quality(거래 품질)를 새로 측정하지 않았다.",
            "- July block(7월 차단), late-session block(후반 세션 차단), vol-low block(낮은 변동성 차단)은 diagnostic hard block(진단용 강제 차단)이다. Effect(효과): 후보 해결책이나 Adapter(어댑터) 구조 승인이 아니다.",
            "- selected_candidate(선택 후보): `none`.",
            "- ONNX readiness(ONNX 준비): `not_claimed`.",
            "",
            "## Next(다음)",
            "",
            f"- next_action(다음 행동): `{NEXT_ACTION}`.",
            "- effect(효과): 실제 MT5 Strategy Tester(전략 테스터) 결과가 반사실 선별과 같은 방향인지 확인하고, 착시 또는 과차단이면 failure memory(실패 기억)로 닫는다.",
        ]
    )
    return "\n".join(lines)


def materialize(common_files_root: Path = COMMON_FILES_ROOT_DEFAULT) -> dict[str, Any]:
    created_at = utc_now()
    source, source_info = input_probe.build_2024_source_frame()
    volatility_edges = load_volatility_edges()
    context = source_context_by_bar_time(source, volatility_edges)
    variants = diagnostic_variants()
    specs = input_probe.candidate_specs()
    base_features = feature_manifest_by_candidate()
    triage_reads = triage_read_by_candidate_intervention()

    if len(base_features) != len(specs):
        raise RuntimeError("base feature manifest does not cover all Stage267 candidates")
    if not read_csv_rows(BASE_TRIAGE_PATH):
        raise RuntimeError("run267C counterfactual triage summary is missing")

    feature_rows: list[dict[str, Any]] = []
    common_copies: list[dict[str, Any]] = []
    feature_exports: dict[tuple[str, str], dict[str, Any]] = {}
    model_exports: dict[tuple[str, str], dict[str, Any]] = {}

    for variant in variants:
        for spec in specs:
            base = base_features[spec.candidate_id]
            local_root = VARIANT_ROOT / variant.short_id / spec.alias
            feature_path = local_root / "features" / f"{spec.alias}_{variant.short_id}.csv"
            model_path = local_root / "models" / f"{spec.alias}_{variant.short_id}_model.csv"
            feature_row = transform_feature_file(Path(base["feature_file"]), feature_path, variant, context)
            model_row = copy_model(Path(base["model_file"]), model_path)
            common_feature_path = f"{COMMON_ROOT}/{variant.short_id}/{spec.alias}/features/{feature_path.name}"
            common_model_path = f"{COMMON_ROOT}/{variant.short_id}/{spec.alias}/models/{model_path.name}"
            feature_copy = copy_to_common(feature_path, common_feature_path, common_files_root)
            model_copy = copy_to_common(model_path, common_model_path, common_files_root)
            common_copies.extend((feature_copy, model_copy))
            key = (spec.candidate_id, variant.variant_id)
            feature_exports[key] = {
                **feature_row,
                "common_path": common_feature_path,
                "common_sha256": feature_copy["sha256"],
            }
            model_exports[key] = {
                **model_row,
                "common_path": common_model_path,
                "common_sha256": model_copy["sha256"],
            }
            feature_rows.append(
                {
                    "candidate_id": spec.candidate_id,
                    "candidate_alias": spec.alias,
                    "candidate_role": spec.role,
                    "diagnostic_variant_id": variant.variant_id,
                    "source_intervention": variant.source_intervention,
                    "design_links": variant.design_links,
                    "weakness_axis": variant.weakness_axis,
                    "weakness_bucket": variant.weakness_bucket,
                    "priority": variant.priority,
                    "intent": variant.intent,
                    "source_feature_file": feature_row["source_feature_file"],
                    "feature_file": feature_row["feature_file"],
                    "feature_sha256": feature_row["feature_sha256"],
                    "common_feature_path": common_feature_path,
                    "common_feature_sha256": feature_copy["sha256"],
                    "model_file": model_row["model_file"],
                    "model_sha256": model_row["model_sha256"],
                    "common_model_path": common_model_path,
                    "common_model_sha256": model_copy["sha256"],
                    "feature_order": feature_row["feature_order"],
                    "feature_order_hash": feature_row["feature_order_hash"],
                    "rows": feature_row["rows"],
                    "total_signal_rows": feature_row["total_signal_rows"],
                    "blocked_signal_rows": feature_row["blocked_signal_rows"],
                    "blocked_long_signal_rows": feature_row["blocked_long_signal_rows"],
                    "blocked_short_signal_rows": feature_row["blocked_short_signal_rows"],
                    "kept_signal_rows": feature_row["kept_signal_rows"],
                    "signal_retention": feature_row["signal_retention"],
                    "context_missing_rows": feature_row["context_missing_rows"],
                }
            )

    attempts = build_attempts(specs, variants, feature_exports, model_exports)
    design_rows = build_design_matrix(feature_rows, variants, triage_reads)
    result = {
        "created_at_utc": created_at,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "packet_id": PACKET_ID,
        "status": STATUS,
        "claim_boundary": CLAIM_BOUNDARY,
        "source_info": source_info,
        "volatility_edges_source": rel(REPO_ROOT / FEATURE_FRAME_PATH),
        "volatility_edges": list(volatility_edges) if volatility_edges else None,
        "source_counterfactual_triage": rel(BASE_COUNTERFACTUAL_PATH),
        "source_triage_summary": rel(BASE_TRIAGE_PATH),
        "diagnostic_variant_count": len(variants),
        "candidate_count": len(specs),
        "feature_variant_count": len(feature_rows),
        "attempt_count": len(attempts),
        "execution_status": "not_executed_input_materialized_only",
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "outputs": {
            "variant_manifest": rel(VARIANT_MANIFEST_PATH),
            "variant_design_matrix": rel(VARIANT_DESIGN_MATRIX_PATH),
            "feature_variant_manifest": rel(FEATURE_VARIANT_MANIFEST_PATH),
            "attempt_manifest": rel(ATTEMPT_MANIFEST_PATH),
            "result": rel(RESULT_PATH),
            "report": rel(REPORT_PATH),
        },
        "latest_judgment": {
            "result_subject": "run267C P0 MT5 variant materialization",
            "evidence_available": [
                rel(VARIANT_MANIFEST_PATH),
                rel(VARIANT_DESIGN_MATRIX_PATH),
                rel(FEATURE_VARIANT_MANIFEST_PATH),
                rel(ATTEMPT_MANIFEST_PATH),
                rel(REPORT_PATH),
            ],
            "evidence_missing": [
                "actual MT5 tester execution",
                "new MT5 KPI summary",
                "new trade records and time-slice KPI",
                "balance/equity curve visual review",
                "full feature ablation and similar replacement retraining",
                "Adapter validation",
                "ONNX parity",
            ],
            "judgment_label": "materialized_not_yet_mt5_evaluated",
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": NEXT_ACTION,
        },
        "next_action": NEXT_ACTION,
    }

    write_csv(
        FEATURE_VARIANT_MANIFEST_PATH,
        feature_rows,
        (
            "candidate_id",
            "candidate_alias",
            "candidate_role",
            "diagnostic_variant_id",
            "source_intervention",
            "design_links",
            "weakness_axis",
            "weakness_bucket",
            "priority",
            "intent",
            "source_feature_file",
            "feature_file",
            "feature_sha256",
            "common_feature_path",
            "common_feature_sha256",
            "model_file",
            "model_sha256",
            "common_model_path",
            "common_model_sha256",
            "feature_order",
            "feature_order_hash",
            "rows",
            "total_signal_rows",
            "blocked_signal_rows",
            "blocked_long_signal_rows",
            "blocked_short_signal_rows",
            "kept_signal_rows",
            "signal_retention",
            "context_missing_rows",
        ),
    )
    write_csv(
        VARIANT_DESIGN_MATRIX_PATH,
        design_rows,
        (
            "candidate_id",
            "candidate_alias",
            "candidate_role",
            "diagnostic_variant_id",
            "source_intervention",
            "design_links",
            "weakness_axis",
            "weakness_bucket",
            "intent",
            "priority",
            "materialization_rule",
            "baseline_trade_count",
            "baseline_net_profit",
            "counterfactual_read",
            "counterfactual_trade_retention",
            "feature_signal_retention",
            "blocked_signal_rows",
            "kept_signal_rows",
            "mt5_execution_status",
            "selected_candidate",
            "onnx_readiness",
        ),
    )
    write_csv(
        ATTEMPT_MANIFEST_PATH,
        attempt_rows(attempts),
        (
            "candidate_id",
            "candidate_alias",
            "candidate_role",
            "diagnostic_variant_id",
            "source_intervention",
            "design_links",
            "attempt_name",
            "tier",
            "split",
            "attempt_role",
            "record_view_prefix",
            "set_path",
            "set_sha256",
            "ini_path",
            "ini_sha256",
            "common_telemetry_path",
            "common_summary_path",
            "fallback_enabled",
            "execution_status",
        ),
    )
    write_json(RESULT_PATH, result)
    write_json(
        VARIANT_MANIFEST_PATH,
        {
            **result,
            "hypothesis": "P0 weak-slice hard-block probes reveal whether run267C counterfactual improvements survive actual MT5 tester materialization before deeper feature engineering.",
            "decision_use": "Choose which P0 axes deserve actual MT5 execution and which should be recorded as over-pruned or calendar/session fragile.",
            "comparison_baseline": rel(RUN267B_HIST_ROOT / "mt5_kpi_summary.csv"),
            "control_variables": [
                "candidate pool remains the five baseline research candidates",
                "source model tables are copied from run267B historical_2024 inputs",
                "MT5 EA entrypoint and trade management settings stay unchanged",
                "period stays 2024 train-era historical stress, not OOS",
            ],
            "changed_variables": [
                "entry signal is set to flat for July 2024 bars",
                "entry signal is set to flat for late-session bars",
                "entry signal is set to flat for vol_low bars",
            ],
            "sample_scope": "US100 M5 Tier A 2024 train-era historical stress feature rows, with Tier A and Tier A+B tester attempts planned",
            "success_criteria": "Materialized attempts keep traceable feature order, hashes, set/ini identity, and no selected candidate claim before MT5 KPI exists.",
            "failure_criteria": "Signal hard-block variants collapse supply or cannot be expressed without changing EA/runtime logic.",
            "invalid_conditions": "Feature order mismatch, missing common-file copy, missing source triage, or period mislabeled as OOS.",
            "stop_conditions": "If MT5 execution confirms over-pruning or calendar-only dependence, close the axis as failure memory rather than opening a long repair loop.",
            "diagnostic_variants": [variant.__dict__ | {"block_predicate": variant.materialization_rule} for variant in variants],
            "feature_variants": feature_rows,
            "attempts": attempts,
            "common_copies": common_copies,
            "feature_exports": {f"{key[0]}::{key[1]}": value for key, value in feature_exports.items()},
            "model_exports": {f"{key[0]}::{key[1]}": value for key, value in model_exports.items()},
        },
    )
    write_md(REPORT_PATH, build_report(result, design_rows, feature_rows))
    upsert_stage_ledger()
    upsert_run_registers(feature_rows, attempts)
    update_current_truth_docs()
    upsert_artifacts(created_at)
    return result


def main() -> int:
    result = materialize()
    print(
        json.dumps(
            {
                "status": result["status"],
                "diagnostic_variant_count": result["diagnostic_variant_count"],
                "feature_variant_count": result["feature_variant_count"],
                "attempt_count": result["attempt_count"],
                "next_action": result["next_action"],
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
