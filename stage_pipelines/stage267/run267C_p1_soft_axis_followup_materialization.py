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
from stage_pipelines.stage267 import historical_stress_2024_probe as input_probe
from stage_pipelines.stage267 import run267C_p0_mt5_variant_materialization as p0


STAGE_ID = input_probe.STAGE_ID
RUN_ID = p0.RUN_ID
RUN_NUMBER = p0.RUN_NUMBER
CLAIM_BOUNDARY = p0.CLAIM_BOUNDARY
STAGE_ROOT = p0.STAGE_ROOT
RUN_ROOT = p0.RUN_ROOT
P1_ROOT = RUN_ROOT / "p1_soft_axis_followup"
REVIEWS_ROOT = p0.REVIEWS_ROOT
RUN267B_HIST_ROOT = p0.RUN267B_HIST_ROOT
STAGE_LEDGER_PATH = p0.STAGE_LEDGER_PATH
ARTIFACT_REGISTRY_PATH = p0.ARTIFACT_REGISTRY_PATH
BASE_FEATURE_MANIFEST_PATH = p0.BASE_FEATURE_MANIFEST_PATH

DESIGN_MATRIX_PATH = P1_ROOT / "p1_soft_axis_design_matrix.csv"
FEATURE_VARIANT_MANIFEST_PATH = P1_ROOT / "feature_variant_manifest.csv"
ATTEMPT_MANIFEST_PATH = P1_ROOT / "attempts.csv"
RESULT_PATH = P1_ROOT / "p1_soft_axis_materialization.json"
VARIANT_MANIFEST_PATH = P1_ROOT / "p1_soft_axis_variant_manifest.json"
REPORT_PATH = REVIEWS_ROOT / "stage267_run267C_p1_soft_axis_followup_materialization_report.md"
PRODUCER_PATH = Path("stage_pipelines/stage267/run267C_p1_soft_axis_followup_materialization.py")

RUN_REGISTRY_PATH = p0.RUN_REGISTRY_PATH
PROJECT_LEDGER_PATH = p0.PROJECT_LEDGER_PATH
CURRENT_WORKING_STATE_PATH = p0.CURRENT_WORKING_STATE_PATH
WORKSPACE_STATE_PATH = p0.WORKSPACE_STATE_PATH
SELECTION_STATUS_PATH = p0.SELECTION_STATUS_PATH
REVIEW_INDEX_PATH = p0.REVIEW_INDEX_PATH

STATUS = "run267C_p1_soft_axis_followup_materialized_execution_pending"
NEXT_ACTION = "run267C_execute_p1_soft_axis_followup_mt5_batch"
PERIOD_LABEL = p0.PERIOD_LABEL
COMMON_ROOT = "OPV2/s267c/run267C_p1"
SOURCE_SIGNAL_COLUMN = p0.SOURCE_SIGNAL_COLUMN


@dataclass(frozen=True)
class SoftAxisVariant:
    variant_id: str
    short_id: str
    source_p0_axis: str
    design_links: str
    weakness_axis: str
    materialization_rule: str
    intent: str
    priority: str
    predicate: Callable[[Mapping[str, Any]], bool]


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


def append_after_anchor(text: str, anchor: str, line: str) -> str:
    if line in text:
        return text
    if anchor not in text:
        raise ValueError(f"Missing anchor: {anchor}")
    return text.replace(anchor, f"{anchor}\n{line}", 1)


def finite_float(value: Any) -> float | None:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return number if math.isfinite(number) else None


def adx_bucket(value: Any) -> str:
    number = finite_float(value)
    if number is None:
        return "feature_missing"
    if 20.0 <= number < 25.0:
        return "adx_20_25"
    if number < 20.0:
        return "adx_lt20"
    if number < 30.0:
        return "adx_25_30"
    return "adx_gte30"


def source_context(source: pd.DataFrame, atr_edge: float, vol_edges: tuple[float, float] | None) -> dict[str, dict[str, Any]]:
    rows: dict[str, dict[str, Any]] = {}
    for record in source.to_dict("records"):
        timestamp = pd.Timestamp(record["timestamp"])
        key = timestamp.strftime("%Y.%m.%d %H:%M:%S")
        atr_ratio = finite_float(record.get("atr_14_over_atr_50"))
        rows[key] = {
            "bar_time_server": key,
            "timestamp_utc": timestamp.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "month": timestamp.strftime("%Y-%m"),
            "hour_utc": timestamp.hour,
            "session_slice": p0.session_slice(record.get("minutes_from_cash_open")),
            "volatility_regime": p0.volatility_regime(record.get("historical_vol_20"), vol_edges),
            "adx_14": finite_float(record.get("adx_14")),
            "adx_bucket": adx_bucket(record.get("adx_14")),
            "atr_14_over_atr_50": atr_ratio,
            "atr_compression_low": atr_ratio is not None and atr_ratio <= atr_edge,
            "di_spread_14": finite_float(record.get("di_spread_14")),
        }
    return rows


def soft_axis_variants() -> tuple[SoftAxisVariant, ...]:
    return (
        SoftAxisVariant(
            variant_id="p1_late_adx20_25_soft_filter",
            short_id="lateadx",
            source_p0_axis="lateblk",
            design_links="p0_late_session_entry_block_probe;adx_20_25_weak_bucket",
            weakness_axis="late_session_plus_adx_20_25",
            materialization_rule="entry signal(진입 신호)을 late session(후반 세션)이면서 ADX 20-25(추세 강도 20-25)인 행에서만 flat(무거래)으로 바꾼다.",
            intent="late-session hard block(후반 세션 강제 차단)을 더 좁은 trend-strength feature(추세 강도 피처) 조건으로 바꾼다.",
            priority="P1",
            predicate=lambda row: row.get("session_slice") == "late" and row.get("adx_bucket") == "adx_20_25",
        ),
        SoftAxisVariant(
            variant_id="p1_late_hour21_soft_filter",
            short_id="late21",
            source_p0_axis="lateblk",
            design_links="p0_late_session_entry_block_probe;late_hour_21_signal_supply",
            weakness_axis="late_session_plus_hour_21",
            materialization_rule="entry signal(진입 신호)을 late session(후반 세션)이면서 UTC hour 21(협정세계시 21시)인 행에서만 flat(무거래)으로 바꾼다.",
            intent="late-session block(후반 세션 차단)을 전체 세션 규칙이 아니라 실제 진입 신호가 있는 후반 시간대 단서로 줄인다.",
            priority="P1",
            predicate=lambda row: row.get("session_slice") == "late" and row.get("hour_utc") == 21,
        ),
        SoftAxisVariant(
            variant_id="p1_vol_low_adx20_25_soft_filter",
            short_id="vlowadx",
            source_p0_axis="vollowblk",
            design_links="p0_vol_low_entry_block_probe;adx_20_25_weak_bucket",
            weakness_axis="vol_low_plus_adx_20_25",
            materialization_rule="entry signal(진입 신호)을 vol_low(낮은 변동성)이면서 ADX 20-25(추세 강도 20-25)인 행에서만 flat(무거래)으로 바꾼다.",
            intent="vol-low hard block(낮은 변동성 강제 차단)을 trend-strength interaction(추세 강도 상호작용)으로 좁힌다.",
            priority="P1",
            predicate=lambda row: row.get("volatility_regime") == "vol_low" and row.get("adx_bucket") == "adx_20_25",
        ),
        SoftAxisVariant(
            variant_id="p1_atr_compression_replacement_filter",
            short_id="atrcomp",
            source_p0_axis="vollowblk",
            design_links="p0_vol_low_entry_block_probe;similar_replacement_atr_14_over_atr_50",
            weakness_axis="atr_compression_replacement",
            materialization_rule="entry signal(진입 신호)을 ATR 14/50 compression(ATR 14/50 압축) 하위 33% 행에서만 flat(무거래)으로 바꾼다.",
            intent="historical_vol_20(20봉 역사 변동성)에 우연히 붙은 것인지 ATR ratio(ATR 비율) 대체축으로 확인한다.",
            priority="P1",
            predicate=lambda row: bool(row.get("atr_compression_low")),
        ),
        SoftAxisVariant(
            variant_id="p1_late_vol_low_intersection_filter",
            short_id="latevlow",
            source_p0_axis="lateblk+vollowblk",
            design_links="p0_late_session_entry_block_probe;p0_vol_low_entry_block_probe",
            weakness_axis="late_session_plus_vol_low",
            materialization_rule="entry signal(진입 신호)을 late session(후반 세션)이면서 vol_low(낮은 변동성)인 교집합 행에서만 flat(무거래)으로 바꾼다.",
            intent="세션 약점과 낮은 변동성 약점이 같은 시장 구조인지 교집합으로 확인한다.",
            priority="P1",
            predicate=lambda row: row.get("session_slice") == "late" and row.get("volatility_regime") == "vol_low",
        ),
    )


def feature_manifest_by_candidate() -> dict[str, dict[str, str]]:
    return {row["candidate_id"]: row for row in read_csv_rows(BASE_FEATURE_MANIFEST_PATH)}


def transform_feature_file(
    source_feature_path: Path,
    destination: Path,
    variant: SoftAxisVariant,
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
    matched_rows = 0
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
            should_block = bool(variant.predicate(context_row))
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
            matched_rows += 1
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
        "matched_rows": matched_rows,
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
    variants: Sequence[SoftAxisVariant],
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
                magic = 26740000 + variant_index * 1000 + candidate_index * 100 + role_index
                payload = attempt_payload(
                    run_root=P1_ROOT,
                    run_id=RUN_ID,
                    stage_number=267,
                    exploration_label=f"stage267_BaselineRacing__{variant.variant_id}",
                    attempt_name=f"{spec.alias}_{variant.short_id}_{attempt_token}_2024",
                    tier=tier,
                    split=PERIOD_LABEL,
                    model_path=str(model_exports[key]["common_path"]),
                    model_id=f"{RUN_ID}_{spec.candidate_id}_{variant.variant_id}_soft_axis_2024",
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
                payload["followup_variant_id"] = variant.variant_id
                payload["source_p0_axis"] = variant.source_p0_axis
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
                "followup_variant_id": attempt.get("followup_variant_id"),
                "source_p0_axis": attempt.get("source_p0_axis"),
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


def build_design_rows(feature_rows: Sequence[Mapping[str, Any]], variants: Sequence[SoftAxisVariant]) -> list[dict[str, Any]]:
    variant_by_id = {variant.variant_id: variant for variant in variants}
    rows: list[dict[str, Any]] = []
    for row in feature_rows:
        variant = variant_by_id[str(row["followup_variant_id"])]
        rows.append(
            {
                "candidate_id": row.get("candidate_id"),
                "candidate_alias": row.get("candidate_alias"),
                "candidate_role": row.get("candidate_role"),
                "followup_variant_id": variant.variant_id,
                "source_p0_axis": variant.source_p0_axis,
                "design_links": variant.design_links,
                "weakness_axis": variant.weakness_axis,
                "materialization_rule": variant.materialization_rule,
                "intent": variant.intent,
                "priority": variant.priority,
                "matched_rows": row.get("matched_rows"),
                "blocked_signal_rows": row.get("blocked_signal_rows"),
                "signal_retention": row.get("signal_retention"),
                "feature_file": row.get("feature_file"),
                "model_file": row.get("model_file"),
                "common_feature_path": row.get("common_feature_path"),
                "common_model_path": row.get("common_model_path"),
                "next_evidence": "MT5 Strategy Tester(전략 테스터) Tier A and Tier A+B batch execution pending(묶음 실행 대기)",
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
        "row_id": "stage267_run267C_p1_soft_axis_followup_materialization",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "view": "p1_soft_axis_followup_materialization",
        "tier_scope": "Tier A and Tier A+B historical 2024 soft-axis attempts planned",
        "scoreboard": "experiment_materialization",
        "status": STATUS,
        "judgment": "materialized_not_yet_mt5_evaluated_no_candidate_selection",
        "evidence_boundary": "feature_set_ini_materialization_only_no_mt5_kpi",
        "report_path": rel(REPORT_PATH),
        "notes": "P1 soft-axis follow-up variants materialized from P0 hard-block evidence; selected candidate none.",
    }
    rows = read_csv_rows(STAGE_LEDGER_PATH)
    merged = [item for item in rows if item.get("row_id") != row["row_id"]]
    merged.append(row)
    write_csv(
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
            "lane": "baseline_candidate_racing_p1_soft_axis_followup_materialization",
            "status": STATUS,
            "judgment": "materialized_not_yet_mt5_evaluated_no_candidate_selection",
            "path": rel(REPORT_PATH),
            "notes": f"feature_variants={len(feature_rows)};attempts={len(attempts)};next_action={NEXT_ACTION};selected_candidate=none;onnx_readiness=not_claimed.",
        },
        ("run_id", "stage_id", "lane", "status", "judgment", "path", "notes"),
    )
    upsert_simple_csv(
        PROJECT_LEDGER_PATH,
        "ledger_row_id",
        {
            "ledger_row_id": f"{RUN_ID}__p1_soft_axis_followup_materialization",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "p1_soft_axis_followup_materialization",
            "parent_run_id": RUN_ID,
            "record_view": "p1_soft_axis_followup_materialization",
            "tier_scope": "Tier A and Tier A+B historical 2024 soft-axis attempts planned",
            "kpi_scope": "materialization_only",
            "scoreboard_lane": "experiment_materialization",
            "status": STATUS,
            "judgment": "materialized_not_yet_mt5_evaluated_no_candidate_selection",
            "path": rel(REPORT_PATH),
            "primary_kpi": f"feature_variants={len(feature_rows)};attempts={len(attempts)}",
            "guardrail_kpi": "selected_candidate=none;onnx_readiness=not_claimed;mt5_execution=pending",
            "external_verification_status": "out_of_scope_by_claim",
            "notes": f"Next action: {NEXT_ACTION}.",
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
        ("stage267_run267C_p1_soft_axis_materializer", "producer_script", PRODUCER_PATH, "Builds run267C P1 soft-axis follow-up MT5 variants."),
        ("stage267_run267C_p1_soft_axis_manifest", "run_manifest", VARIANT_MANIFEST_PATH, "Run267C P1 soft-axis variant manifest."),
        ("stage267_run267C_p1_soft_axis_design_matrix", "variant_design_matrix", DESIGN_MATRIX_PATH, "P1 soft-axis design matrix linked to P0 review."),
        ("stage267_run267C_p1_soft_axis_feature_manifest", "feature_variant_manifest", FEATURE_VARIANT_MANIFEST_PATH, "Feature/model/common file manifest for P1 variants."),
        ("stage267_run267C_p1_soft_axis_attempt_manifest", "attempt_manifest", ATTEMPT_MANIFEST_PATH, "MT5 set/ini attempt manifest for P1 variants."),
        ("stage267_run267C_p1_soft_axis_materialization_result", "review_result", RESULT_PATH, "JSON payload for P1 soft-axis materialization."),
        ("stage267_run267C_p1_soft_axis_materialization_report", "review_report", REPORT_PATH, "User-facing P1 soft-axis materialization report."),
    )
    rows = read_csv_rows(ARTIFACT_REGISTRY_PATH)
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
    write_csv(
        ARTIFACT_REGISTRY_PATH,
        merged,
        ("artifact_id", "artifact_type", "path", "sha256", "stage_id", "run_id", "created_at_utc", "notes"),
    )


def update_current_truth_docs() -> None:
    report_line = "- Stage267(267단계) run267C P1 soft-axis follow-up materialization(P1 부드러운 축 후속 물질화): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267C_p1_soft_axis_followup_materialization_report.md`"

    current_text = io_path(CURRENT_WORKING_STATE_PATH).read_text(encoding="utf-8-sig")
    current_text = replace_once(
        current_text,
        "- status(상태): `stage267_run267C_p0_mt5_full_batch_review_completed`",
        f"- status(상태): `{STATUS}`",
    )
    current_text = append_after_anchor(
        current_text,
        "- Stage267(267단계) run267C P0 MT5 full batch review(우선순위 0 MT5 전체 묶음 검토): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267C_p0_mt5_full_batch_review.md`",
        report_line,
    )
    current_text = replace_once(
        current_text,
        "- action(행동): run267C(267C 실행) P0 MT5 full batch review(우선순위 0 MT5 전체 묶음 검토)를 `30`개 KPI(핵심 성과 지표) 기준으로 수행했다.",
        "- action(행동): run267C(267C 실행) P0 hard block(강제 차단) 근거를 P1 soft-axis follow-up(P1 부드러운 축 후속) feature CSV(피처 표), model copy(모델 복사), set/ini(설정/초기화) 변형으로 물질화했다.",
    )
    current_text = replace_once(
        current_text,
        "- effect(효과): hard block(강제 차단) 숫자를 후보 해결책으로 오해하지 않고, soft feature(부드러운 피처), similar replacement(유사 대체), adapter variant(어댑터 변형) 후속 설계로 넘긴다.",
        "- effect(효과): vol-low(낮은 변동성), late session(후반 세션), ATR compression(ATR 압축), ADX 20-25(추세 강도 20-25)를 좁은 진단 변형으로 만들어 실제 MT5 batch(묶음 실행) 직전 상태로 옮겼다.",
    )
    current_text = replace_once(
        current_text,
        "- next_action(다음 행동): `run267C_design_p0_axis_followup_feature_engineering_variants`. Effect(효과): 강제 차단으로 확인한 약점 축을 soft feature(부드러운 피처), similar replacement(유사 대체), adapter variant(어댑터 변형)로 바꿔 다시 시험한다.",
        f"- next_action(다음 행동): `{NEXT_ACTION}`. Effect(효과): P1 soft-axis(부드러운 축) 변형이 hard block(강제 차단)보다 덜 깨지는지 실제 MT5 Strategy Tester(전략 테스터)로 확인한다.",
    )
    write_md(CURRENT_WORKING_STATE_PATH, current_text)

    selection_text = io_path(SELECTION_STATUS_PATH).read_text(encoding="utf-8-sig")
    selection_text = replace_once(
        selection_text,
        "- stage_status(단계 상태): `run267C_p0_mt5_full_batch_review_completed`",
        f"- stage_status(단계 상태): `{STATUS}`",
    )
    selection_text = append_after_anchor(
        selection_text,
        "- run267C_p0_mt5_full_batch_review(267C 우선순위 0 MT5 전체 묶음 검토): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267C_p0_mt5_full_batch_review.md`",
        "- run267C_p1_soft_axis_followup_materialization(267C P1 부드러운 축 후속 물질화): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267C_p1_soft_axis_followup_materialization_report.md`",
    )
    selection_text = replace_once(
        selection_text,
        "- next_action(다음 행동): `run267C_design_p0_axis_followup_feature_engineering_variants`",
        f"- next_action(다음 행동): `{NEXT_ACTION}`",
    )
    selection_text = replace_once(
        selection_text,
        "Run267C(267C 실행)는 P0 MT5 full batch review(우선순위 0 MT5 전체 묶음 검토)를 완료했다.",
        "Run267C(267C 실행)는 P1 soft-axis follow-up materialization(P1 부드러운 축 후속 물질화)을 완료했다.",
    )
    selection_text = replace_once(
        selection_text,
        "Effect(효과): 선택 후보(selected candidate, 선택 후보)는 계속 없고, 다음은 hard block(강제 차단)을 soft feature(부드러운 피처), similar replacement(유사 대체), adapter variant(어댑터 변형)으로 바꾸는 후속 설계다.",
        "Effect(효과): 선택 후보(selected candidate, 선택 후보)는 계속 없고, 다음은 P1 변형의 MT5 Strategy Tester(전략 테스터) 실행이다.",
    )
    write_md(SELECTION_STATUS_PATH, selection_text)

    review_text = io_path(REVIEW_INDEX_PATH).read_text(encoding="utf-8-sig")
    review_text = replace_once(
        review_text,
        "- status(상태): `run267C_p0_mt5_full_batch_review_completed`",
        f"- status(상태): `{STATUS}`",
    )
    review_text = append_after_anchor(
        review_text,
        "- run267C_p0_mt5_full_batch_review(267C 우선순위 0 MT5 전체 묶음 검토): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267C_p0_mt5_full_batch_review.md`",
        "- run267C_p1_soft_axis_followup_materialization(267C P1 부드러운 축 후속 물질화): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267C_p1_soft_axis_followup_materialization_report.md`",
    )
    review_text = replace_once(
        review_text,
        "Run267C(267C 실행)는 반사실 선별 이후 P0 MT5 full batch review(우선순위 0 MT5 전체 묶음 검토)를 완료했다.",
        "Run267C(267C 실행)는 P0 MT5 full batch review(우선순위 0 MT5 전체 묶음 검토) 이후 P1 soft-axis follow-up materialization(P1 부드러운 축 후속 물질화)을 완료했다.",
    )
    review_text = replace_once(
        review_text,
        "Effect(효과): Stage267(267단계)는 후보 선택(selected candidate, 선택 후보), ONNX readiness(ONNX 준비), runtime authority(런타임 권위)를 주장하지 않고, `run267C_design_p0_axis_followup_feature_engineering_variants`로 넘어간다.",
        f"Effect(효과): Stage267(267단계)는 후보 선택(selected candidate, 선택 후보), ONNX readiness(ONNX 준비), runtime authority(런타임 권위)를 주장하지 않고, `{NEXT_ACTION}`로 넘어간다.",
    )
    write_md(REVIEW_INDEX_PATH, review_text)

    workspace_text = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    workspace_text = replace_once(
        workspace_text,
        "Stage267(267단계) run267C(267C 실행) P0 MT5 full batch review(우선순위 0 MT5 전체 묶음 검토) completed(완료).",
        "Stage267(267단계) run267C(267C 실행) P1 soft-axis follow-up materialization(P1 부드러운 축 후속 물질화) completed(완료).",
    )
    workspace_text = replace_once(
        workspace_text,
        "Effect(효과): `30`개 attempt(시도)를 실제 MT5 Strategy Tester(전략 테스터)로 확인했고, `30`개 KPI(핵심 성과 지표)를 확보했지만 selected candidate(선택 후보)나 ONNX readiness(ONNX 준비)는 주장하지 않는다.",
        "Effect(효과): P1 feature variant(피처 변형) 25개와 MT5 set/ini(설정/초기화) attempt(시도) 50개를 만들었지만 selected candidate(선택 후보)나 ONNX readiness(ONNX 준비)는 주장하지 않는다.",
    )
    workspace_text = replace_once(
        workspace_text,
        "Next action(다음 행동)는 `run267C_design_p0_axis_followup_feature_engineering_variants`이다.",
        f"Next action(다음 행동)는 `{NEXT_ACTION}`이다.",
    )
    workspace_text = replace_once(
        workspace_text,
        "active_run267C_p0_mt5_full_batch_review_completed(267C 우선순위 0 MT5 전체 묶음 검토 후 후속 설계 활성).",
        "active_run267C_p1_soft_axis_followup_materialized_execution_pending(267C P1 부드러운 축 후속 물질화 완료 후 실행 대기 활성).",
    )
    write_md(WORKSPACE_STATE_PATH, workspace_text)


def report_markdown(result: Mapping[str, Any], design_rows: Sequence[Mapping[str, Any]], variants: Sequence[SoftAxisVariant]) -> str:
    axis_rows: list[str] = []
    seen: set[str] = set()
    for row in design_rows:
        variant_id = str(row.get("followup_variant_id", ""))
        if variant_id in seen:
            continue
        seen.add(variant_id)
        axis_rows.append(
            f"| `{variant_id}` | `{row.get('source_p0_axis')}` | {row.get('materialization_rule')} | {row.get('intent')} |"
        )
    candidate_rows = sorted(design_rows, key=lambda row: (str(row.get("candidate_alias")), str(row.get("followup_variant_id"))))
    lines = [
        "# Stage267 Run267C P1 Soft-Axis Follow-up Materialization(267단계 267C P1 부드러운 축 후속 물질화)",
        "",
        f"- action(행동): `{result['feature_variant_count']}`개 feature variant(피처 변형)와 `{result['attempt_count']}`개 MT5 attempt(메타트레이더5 시도)를 만들었다.",
        "- effect(효과): P0 hard block(강제 차단)을 그대로 채택하지 않고, late session(후반 세션), vol-low(낮은 변동성), ADX(추세 강도), ATR compression(ATR 압축) 상호작용으로 좁혀 다음 MT5 실행 준비를 끝냈다.",
        f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
        "",
        "## Experiment Design(실험 설계)",
        "",
        "- hypothesis(가설): P0 broad hard block(넓은 강제 차단)의 개선은 일부 약점 regime(국면)에 집중되어 있으며, 좁은 soft-axis feature(부드러운 축 피처)로 바꾸면 거래 수 붕괴를 줄이면서 DD(drawdown, 손실폭)를 낮출 수 있다.",
        "- decision_use(결정 사용처): 어떤 축을 실제 Adapter(어댑터) 후보로 확장할지 고른다.",
        f"- comparison_baseline(비교 기준): `{rel(RUN267B_HIST_ROOT / 'mt5_kpi_summary.csv')}` and `{rel(p0.VARIANT_ROOT / 'p0_mt5_full_batch_candidate_variant_summary.csv')}`.",
        "- control_variables(고정 변수): 후보군, model CSV(모델 표), MT5 EA(메타트레이더5 전문가 자문), 기간, threshold(임계값), trade management(거래 관리)를 유지한다.",
        "- changed_variables(변경 변수): entry signal(진입 신호)을 좁은 P1 약점 조건에서만 flat(무거래)으로 바꾼다.",
        "- sample_scope(표본 범위): US100 M5 Tier A historical 2024 train-era stress(학습 기간 과거 압박)와 Tier A+B routed total(라우팅 합산) 실행 계획.",
        "- success_criteria(성공 기준): P1 MT5 실행에서 P0보다 거래 수 비용이 작고, run267B보다 DD(손실폭), PF(수익 팩터), recovery(회복)가 개선되는 축을 찾는다.",
        "- failure_criteria(실패 기준): P1 축이 trade count collapse(거래 수 붕괴)를 만들거나, DD(손실폭)를 줄이지 못하거나, 특정 달력 규칙으로만 설명된다.",
        "- invalid_conditions(무효 조건): feature order mismatch(피처 순서 불일치), timestamp mismatch(시각 불일치), common file copy missing(공용 파일 복사 누락), MT5 output missing(MT5 출력 누락).",
        "- stop_conditions(중단 조건): 한 축이 두 번 연속 hard block(강제 차단)과 같은 과차단으로 보이면 repair loop(수리 반복)를 열지 않고 failure memory(실패 기억)로 닫는다.",
        "- evidence_plan(근거 계획): attempts.csv(시도 목록), feature_variant_manifest.csv(피처 변형 목록), p1 MT5 KPI summary(P1 핵심 성과 지표 요약), backtest forensics(백테스트 포렌식), full batch review(전체 묶음 검토)를 요구한다.",
        "",
        "## P1 Axes(P1 축)",
        "",
        "| followup variant(후속 변형) | source P0 axis(원천 P0 축) | materialization rule(물질화 규칙) | intent(의도) |",
        "| --- | --- | --- | --- |",
        *axis_rows,
        "",
        "## Candidate Signal Cost(후보별 신호 비용)",
        "",
        "| candidate(후보) | variant(변형) | matched rows(조건 행) | blocked signals(차단 신호) | kept signals(유지 신호) | retention(유지율) |",
        "| --- | --- | ---: | ---: | ---: | ---: |",
    ]
    for row in candidate_rows:
        lines.append(
            f"| `{row.get('candidate_alias')}` | `{row.get('followup_variant_id')}` | {row.get('matched_rows')} | {row.get('blocked_signal_rows')} | {row.get('kept_signal_rows')} | {csv_value(row.get('signal_retention'))} |"
        )
    lines.extend(
        [
            "",
            "## Boundary(경계)",
            "",
            "- 이 결과는 materialization(물질화)이다. Effect(효과): MT5 KPI(핵심 성과 지표)가 아직 없으므로 후보 선택이나 ONNX readiness(ONNX 준비)를 주장하지 않는다.",
            "- direct July rule(직접 7월 규칙)은 만들지 않았다. Effect(효과): 달력 overfit(과적합)을 피하고, vol/session/trend proxy(변동성/세션/추세 대리 피처)로 검증한다.",
            "- selected_candidate(선택 후보): `none`.",
            "- ONNX readiness(ONNX 준비): `not_claimed`.",
            f"- next_action(다음 행동): `{NEXT_ACTION}`.",
        ]
    )
    return "\n".join(lines)


def materialize(common_files_root: Path = COMMON_FILES_ROOT_DEFAULT) -> dict[str, Any]:
    created_at = utc_now()
    source, source_info = input_probe.build_2024_source_frame()
    volatility_edges = p0.load_volatility_edges()
    atr_edge = float(pd.to_numeric(source["atr_14_over_atr_50"], errors="coerce").quantile(0.33))
    context = source_context(source, atr_edge, volatility_edges)
    variants = soft_axis_variants()
    specs = input_probe.candidate_specs()
    base_features = feature_manifest_by_candidate()
    if len(base_features) != len(specs):
        raise RuntimeError("base feature manifest does not cover all Stage267 candidates")

    feature_rows: list[dict[str, Any]] = []
    common_copies: list[dict[str, Any]] = []
    feature_exports: dict[tuple[str, str], dict[str, Any]] = {}
    model_exports: dict[tuple[str, str], dict[str, Any]] = {}

    for variant in variants:
        for spec in specs:
            base = base_features[spec.candidate_id]
            local_root = P1_ROOT / variant.short_id / spec.alias
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
                    "followup_variant_id": variant.variant_id,
                    "source_p0_axis": variant.source_p0_axis,
                    "design_links": variant.design_links,
                    "weakness_axis": variant.weakness_axis,
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
                    "matched_rows": feature_row["matched_rows"],
                    "total_signal_rows": feature_row["total_signal_rows"],
                    "long_signal_rows": feature_row["long_signal_rows"],
                    "short_signal_rows": feature_row["short_signal_rows"],
                    "blocked_signal_rows": feature_row["blocked_signal_rows"],
                    "blocked_long_signal_rows": feature_row["blocked_long_signal_rows"],
                    "blocked_short_signal_rows": feature_row["blocked_short_signal_rows"],
                    "kept_signal_rows": feature_row["kept_signal_rows"],
                    "signal_retention": feature_row["signal_retention"],
                    "context_missing_rows": feature_row["context_missing_rows"],
                    "feature_encoding": "utf-8_no_bom_runtime_header_safe",
                }
            )

    attempts = build_attempts(specs, variants, feature_exports, model_exports)
    design_rows = build_design_rows(feature_rows, variants)
    result = {
        "status": STATUS,
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "created_at_utc": created_at,
        "source_info": source_info,
        "atr_compression_edge_q33": atr_edge,
        "volatility_edges": volatility_edges,
        "followup_variant_count": len(variants),
        "feature_variant_count": len(feature_rows),
        "attempt_count": len(attempts),
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
        "next_action": NEXT_ACTION,
        "outputs": {
            "design_matrix": rel(DESIGN_MATRIX_PATH),
            "feature_variant_manifest": rel(FEATURE_VARIANT_MANIFEST_PATH),
            "attempt_manifest": rel(ATTEMPT_MANIFEST_PATH),
            "report": rel(REPORT_PATH),
        },
    }

    write_csv(
        FEATURE_VARIANT_MANIFEST_PATH,
        feature_rows,
        (
            "candidate_id",
            "candidate_alias",
            "candidate_role",
            "followup_variant_id",
            "source_p0_axis",
            "design_links",
            "weakness_axis",
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
            "matched_rows",
            "total_signal_rows",
            "long_signal_rows",
            "short_signal_rows",
            "blocked_signal_rows",
            "blocked_long_signal_rows",
            "blocked_short_signal_rows",
            "kept_signal_rows",
            "signal_retention",
            "context_missing_rows",
            "feature_encoding",
        ),
    )
    write_csv(
        DESIGN_MATRIX_PATH,
        design_rows,
        (
            "candidate_id",
            "candidate_alias",
            "candidate_role",
            "followup_variant_id",
            "source_p0_axis",
            "design_links",
            "weakness_axis",
            "materialization_rule",
            "intent",
            "priority",
            "matched_rows",
            "blocked_signal_rows",
            "signal_retention",
            "feature_file",
            "model_file",
            "common_feature_path",
            "common_model_path",
            "next_evidence",
        ),
    )
    write_csv(
        ATTEMPT_MANIFEST_PATH,
        attempt_rows(attempts),
        (
            "candidate_id",
            "candidate_alias",
            "candidate_role",
            "followup_variant_id",
            "source_p0_axis",
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
            "hypothesis": "P1 soft-axis filters can keep part of the P0 drawdown repair while reducing broad hard-block trade removal.",
            "decision_use": "Choose which weakness axes deserve MT5 execution and later adapter development.",
            "comparison_baseline": [rel(RUN267B_HIST_ROOT / "mt5_kpi_summary.csv"), rel(p0.VARIANT_ROOT / "p0_mt5_full_batch_candidate_variant_summary.csv")],
            "control_variables": [
                "candidate pool remains the five Stage267 research baseline candidates",
                "model CSV files are copied from run267B historical_2024 inputs",
                "MT5 EA entrypoint and trade management settings stay unchanged",
                "period stays 2024 train-era historical stress, not OOS",
            ],
            "changed_variables": [variant.variant_id for variant in variants],
            "sample_scope": "US100 M5 Tier A 2024 train-era historical stress feature rows, with Tier A and Tier A+B tester attempts planned",
            "success_criteria": "P1 variants reduce drawdown versus run267B with lower trade-count cost than P0 hard blocks.",
            "failure_criteria": "P1 variants collapse trade supply, fail to reduce drawdown, or only reproduce a calendar-specific artifact.",
            "invalid_conditions": "Feature order mismatch, missing common-file copy, timestamp mismatch, or missing MT5 output.",
            "stop_conditions": "If an axis remains broad hard-block only after this pass, close it as failure memory or redesign from a different feature family.",
            "soft_axis_variants": [variant.__dict__ | {"predicate": variant.materialization_rule} for variant in variants],
            "feature_variants": feature_rows,
            "attempts": attempts,
            "common_copies": common_copies,
        },
    )
    write_md(REPORT_PATH, report_markdown(result, design_rows, variants))
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
                "followup_variant_count": result["followup_variant_count"],
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
