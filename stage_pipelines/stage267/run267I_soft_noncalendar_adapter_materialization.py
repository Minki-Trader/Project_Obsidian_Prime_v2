from __future__ import annotations

import csv
import json
import math
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists, sha256_file_lf_normalized
from foundation.control_plane.mt5_tier_balance_completion import COMMON_FILES_ROOT_DEFAULT, attempt_payload, copy_to_common
from foundation.models.onnx_bridge import ordered_hash
from stage_pipelines.stage267 import historical_stress_2024_probe as input_probe
from stage_pipelines.stage267 import run267H_soft_noncalendar_adapter_design as run267h


STAGE_ID = input_probe.STAGE_ID
RUN_ID = "run267I_stage267_p0_soft_noncalendar_adapter_materialization_v1"
RUN_NUMBER = "run267I"
STATUS = "run267I_p0_soft_noncalendar_adapter_materialized_execution_pending"
NEXT_ACTION = "run267I_execute_p0_soft_noncalendar_adapter_mt5_batch"
CLAIM_BOUNDARY = input_probe.CLAIM_BOUNDARY

STAGE_ROOT = input_probe.STAGE_ROOT
REVIEWS_ROOT = input_probe.REVIEWS_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER
DESIGN_ROOT = RUN_ROOT / "p0_soft_noncalendar_adapter_materialization"

INPUT_QUEUE_PATH = run267h.EXPERIMENT_QUEUE_PATH
INPUT_FEATURE_MATRIX_PATH = run267h.FEATURE_MATRIX_PATH
BASE_FEATURE_MANIFEST_PATH = input_probe.FEATURE_MANIFEST_PATH

FEATURE_MANIFEST_PATH = DESIGN_ROOT / "feature_model_manifest.csv"
RUNTIME_CONTRACT_PATH = DESIGN_ROOT / "runtime_contract.csv"
ATTEMPT_MANIFEST_PATH = DESIGN_ROOT / "attempts.csv"
SOFT_SCORE_DIAGNOSTICS_PATH = DESIGN_ROOT / "soft_score_diagnostics.csv"
RUN_MANIFEST_PATH = DESIGN_ROOT / "run_manifest.json"
LINEAGE_PATH = DESIGN_ROOT / "lineage.json"
RESULT_PATH = DESIGN_ROOT / "result.json"
REPORT_PATH = REVIEWS_ROOT / "stage267_run267I_soft_noncalendar_adapter_materialization.md"
PRODUCER_PATH = Path("stage_pipelines/stage267/run267I_soft_noncalendar_adapter_materialization.py")

STAGE_LEDGER_PATH = input_probe.STAGE_LEDGER_PATH
PROJECT_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
ARTIFACT_REGISTRY_PATH = input_probe.ARTIFACT_REGISTRY_PATH
CURRENT_WORKING_STATE_PATH = Path("docs/context/current_working_state.md")
WORKSPACE_STATE_PATH = Path("docs/workspace/workspace_state.yaml")
SELECTION_STATUS_PATH = STAGE_ROOT / "04_selected" / "selection_status.md"
REVIEW_INDEX_PATH = REVIEWS_ROOT / "review_index.md"

COMMON_ROOT = "OPV2/s267i/run267I_p0_soft_noncalendar_adapter"
PERIOD_LABEL = input_probe.PERIOD_LABEL
SOFT_FEATURE_NAME = "stage267_adx_atr_soft_score"
MODEL_MATERIALIZATION_TYPE = "research_score_table_extension_not_retrained"

CSV_MODEL_COLUMNS = ("record_type", "feature_index", "item_index", "value", "score_short", "score_flat", "score_long")
SOFT_SCORE_CUTS = (0.25, 0.50, 0.75)
SOFT_SCORE_TERMS = (
    (0.0, 0.0, 0.0),
    (-0.025, 0.05, -0.025),
    (-0.05, 0.10, -0.05),
    (-0.075, 0.15, -0.075),
    (-0.10, 0.20, -0.10),
)


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    item = Path(path)
    try:
        return item.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return item.as_posix()


def cell(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, float):
        if not math.isfinite(value):
            return ""
        return f"{value:.12g}"
    if isinstance(value, (list, tuple)):
        return ";".join(str(item) for item in value)
    return str(value)


def read_csv(path: Path) -> list[dict[str, str]]:
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
            writer.writerow({column: cell(row.get(column)) for column in columns})


def write_runtime_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
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


def upsert_csv(path: Path, key: str, rows: Sequence[Mapping[str, Any]], columns: Sequence[str]) -> None:
    existing = read_csv(path)
    replacements = {str(row[key]): row for row in rows}
    merged: list[Mapping[str, Any]] = []
    seen: set[str] = set()
    for row in existing:
        row_key = str(row.get(key, ""))
        if row_key in replacements:
            merged.append(replacements[row_key])
            seen.add(row_key)
        else:
            merged.append(row)
    for row_key, row in replacements.items():
        if row_key not in seen:
            merged.append(row)
    write_csv(path, merged, columns)


def replace_if_present(text: str, old: str, new: str) -> str:
    if old in text:
        return text.replace(old, new, 1)
    return text


def append_after(text: str, anchor: str, line: str) -> str:
    if line in text:
        return text
    if anchor not in text:
        raise ValueError(f"missing anchor: {anchor}")
    return text.replace(anchor, f"{anchor}\n{line}", 1)


def finite_float(value: Any) -> float | None:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return number if math.isfinite(number) else None


def quantile(values: Sequence[float], q: float) -> float:
    if not values:
        return 0.0
    series = pd.Series(list(values), dtype="float64")
    return float(series.quantile(float(q)))


def soft_band_adx(value: Any) -> float:
    number = finite_float(value)
    if number is None:
        return 0.0
    # Peak inside ADX 20-25(추세 강도 20-25), taper to zero outside 15-30.
    return max(0.0, min(1.0, 1.0 - abs(number - 22.5) / 7.5))


def low_atr_score(value: Any, q33: float, q67: float) -> float:
    number = finite_float(value)
    if number is None:
        return 0.0
    width = max(float(q67) - float(q33), 1.0e-9)
    return max(0.0, min(1.0, (float(q67) - number) / width))


def build_soft_context() -> tuple[dict[str, dict[str, Any]], dict[str, Any]]:
    source, source_info = input_probe.build_2024_source_frame()
    atr_values = [
        float(value)
        for value in pd.to_numeric(source.get("atr_14_over_atr_50"), errors="coerce").dropna().to_list()
    ]
    adx_values = [float(value) for value in pd.to_numeric(source.get("adx_14"), errors="coerce").dropna().to_list()]
    if not atr_values or not adx_values:
        raise RuntimeError("run267I requires adx_14 and atr_14_over_atr_50 context")
    atr_q33 = quantile(atr_values, 1 / 3)
    atr_q67 = quantile(atr_values, 2 / 3)
    context: dict[str, dict[str, Any]] = {}
    for record in source.to_dict("records"):
        timestamp = pd.Timestamp(record["timestamp"])
        key = timestamp.strftime("%Y.%m.%d %H:%M:%S")
        adx_component = soft_band_adx(record.get("adx_14"))
        atr_component = low_atr_score(record.get("atr_14_over_atr_50"), atr_q33, atr_q67)
        score = adx_component * atr_component
        context[key] = {
            "bar_time_server": key,
            "adx_14": finite_float(record.get("adx_14")),
            "atr_14_over_atr_50": finite_float(record.get("atr_14_over_atr_50")),
            "adx_20_25_soft_component": adx_component,
            "atr_low_component": atr_component,
            SOFT_FEATURE_NAME: score,
        }
    return context, {
        "source_info": source_info,
        "atr_14_over_atr_50_q33": atr_q33,
        "atr_14_over_atr_50_q67": atr_q67,
        "adx_14_q33": quantile(adx_values, 1 / 3),
        "adx_14_q67": quantile(adx_values, 2 / 3),
        "context_rows": len(context),
    }


def p0_queue_rows() -> list[dict[str, str]]:
    rows = [
        row
        for row in read_csv(INPUT_QUEUE_PATH)
        if row.get("materialization_decision") == "materialize_next"
        and row.get("feature_design") == "adx_atr_soft_score"
        and row.get("candidate_alias") in {"s264_aih", "s264_lc"}
    ]
    if len(rows) != 2:
        raise RuntimeError(f"expected 2 P0 rows from run267H, found {len(rows)}")
    lane_order = {"P0": 0, "P0_control": 1}
    return sorted(rows, key=lambda row: lane_order.get(row.get("priority_lane", ""), 99))


def base_features_by_alias() -> dict[str, dict[str, str]]:
    return {row["candidate_alias"]: row for row in read_csv(BASE_FEATURE_MANIFEST_PATH)}


def specs_by_alias() -> dict[str, Any]:
    return {spec.alias: spec for spec in input_probe.candidate_specs()}


def transform_feature_file(
    source: Path,
    destination: Path,
    context: Mapping[str, Mapping[str, Any]],
) -> tuple[dict[str, Any], dict[str, Any]]:
    rows = read_csv(source)
    if not rows:
        raise RuntimeError(f"empty source feature file: {source}")
    base_columns = list(rows[0].keys())
    if SOFT_FEATURE_NAME in base_columns:
        columns = base_columns
    else:
        columns = [*base_columns, SOFT_FEATURE_NAME]

    transformed: list[dict[str, Any]] = []
    scores: list[float] = []
    signal_scores: list[float] = []
    total_signal_rows = 0
    context_missing_rows = 0
    high_soft_score_signal_rows = 0
    for row in rows:
        current = dict(row)
        key = str(row.get("bar_time_server", ""))
        context_row = context.get(key)
        if context_row is None:
            context_missing_rows += 1
            score = 0.0
        else:
            score = float(context_row.get(SOFT_FEATURE_NAME) or 0.0)
        current[SOFT_FEATURE_NAME] = score
        scores.append(score)
        signal = int(round(float(row.get(input_probe.SOURCE_SIGNAL_COLUMN) or 0.0)))
        if signal != 0:
            total_signal_rows += 1
            signal_scores.append(score)
            if score >= 0.75:
                high_soft_score_signal_rows += 1
        transformed.append(current)

    write_runtime_csv(destination, transformed, columns)
    feature_order = tuple(columns[1:])
    diagnostics = {
        "rows": len(transformed),
        "source_feature_file": rel(source),
        "feature_file": rel(destination),
        "feature_sha256": sha256_file_lf_normalized(destination),
        "feature_order": ";".join(feature_order),
        "feature_order_hash": ordered_hash(feature_order),
        "feature_count": len(feature_order),
        "total_signal_rows": total_signal_rows,
        "context_missing_rows": context_missing_rows,
        "soft_score_min": min(scores) if scores else 0.0,
        "soft_score_q50": quantile(scores, 0.50),
        "soft_score_q80": quantile(scores, 0.80),
        "soft_score_q95": quantile(scores, 0.95),
        "soft_score_max": max(scores) if scores else 0.0,
        "signal_soft_score_q50": quantile(signal_scores, 0.50),
        "signal_soft_score_q80": quantile(signal_scores, 0.80),
        "high_soft_score_signal_rows": high_soft_score_signal_rows,
        "high_soft_score_signal_ratio": high_soft_score_signal_rows / total_signal_rows if total_signal_rows else None,
    }
    return diagnostics, {"columns": columns, "feature_order": feature_order}


def extend_score_table_model(source: Path, destination: Path, soft_feature_index: int) -> dict[str, Any]:
    if not path_exists(source):
        raise FileNotFoundError(source)
    with io_path(source).open("r", encoding="utf-8-sig", newline="") as handle:
        source_rows = list(csv.DictReader(handle))
    io_path(destination.parent).mkdir(parents=True, exist_ok=True)
    with io_path(destination).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(CSV_MODEL_COLUMNS), lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in source_rows:
            writer.writerow({column: row.get(column, "") for column in CSV_MODEL_COLUMNS})
        for index, cut in enumerate(SOFT_SCORE_CUTS):
            writer.writerow(
                {
                    "record_type": "cut",
                    "feature_index": soft_feature_index,
                    "item_index": index,
                    "value": f"{cut:.17g}",
                    "score_short": "",
                    "score_flat": "",
                    "score_long": "",
                }
            )
        for index, (score_short, score_flat, score_long) in enumerate(SOFT_SCORE_TERMS):
            writer.writerow(
                {
                    "record_type": "score",
                    "feature_index": soft_feature_index,
                    "item_index": index,
                    "value": "",
                    "score_short": f"{score_short:.17g}",
                    "score_flat": f"{score_flat:.17g}",
                    "score_long": f"{score_long:.17g}",
                }
            )
    return {
        "source_model_file": rel(source),
        "model_file": rel(destination),
        "model_sha256": sha256_file_lf_normalized(destination),
        "model_materialization_type": MODEL_MATERIALIZATION_TYPE,
        "soft_feature_index": soft_feature_index,
        "soft_score_cuts": ";".join(f"{value:.2f}" for value in SOFT_SCORE_CUTS),
        "soft_score_terms": ";".join("/".join(f"{score:.3f}" for score in row) for row in SOFT_SCORE_TERMS),
    }


def build_attempt_rows(attempts: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for attempt in attempts:
        rows.append(
            {
                "candidate_alias": attempt.get("candidate_alias"),
                "candidate_role": attempt.get("candidate_role"),
                "feature_design": attempt.get("feature_design"),
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
                "execution_status": attempt.get("execution_status", "not_executed"),
            }
        )
    return rows


def materialize_payload() -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    dict[str, Any],
]:
    queue_rows = p0_queue_rows()
    base_features = base_features_by_alias()
    specs = specs_by_alias()
    context, context_info = build_soft_context()

    feature_manifest: list[dict[str, Any]] = []
    contract_rows: list[dict[str, Any]] = []
    diagnostics_rows: list[dict[str, Any]] = []
    attempts: list[dict[str, Any]] = []
    lineage_rows: list[dict[str, Any]] = []

    for candidate_index, queue_row in enumerate(queue_rows, start=1):
        alias = str(queue_row["candidate_alias"])
        spec = specs[alias]
        base = base_features[alias]
        local_root = DESIGN_ROOT / "adxatrsoft" / alias
        feature_path = local_root / "features" / f"{alias}_adxatrsoft.csv"
        model_path = local_root / "models" / f"{alias}_adxatrsoft_model.csv"

        feature_meta, order_meta = transform_feature_file(Path(base["feature_file"]), feature_path, context)
        soft_feature_index = len(order_meta["feature_order"]) - 1
        model_meta = extend_score_table_model(Path(base["model_file"]), model_path, soft_feature_index)

        common_feature_path = f"{COMMON_ROOT}/adxatrsoft/{alias}/features/{feature_path.name}"
        common_model_path = f"{COMMON_ROOT}/adxatrsoft/{alias}/models/{model_path.name}"
        common_feature = copy_to_common(feature_path, common_feature_path, COMMON_FILES_ROOT_DEFAULT)
        common_model = copy_to_common(model_path, common_model_path, COMMON_FILES_ROOT_DEFAULT)

        manifest_row = {
            "candidate_alias": alias,
            "candidate_role": queue_row.get("candidate_role"),
            "priority_lane": queue_row.get("priority_lane"),
            "feature_design": queue_row.get("feature_design"),
            "adapter_mode": queue_row.get("adapter_mode"),
            "model_materialization_type": MODEL_MATERIALIZATION_TYPE,
            "source_feature_file": feature_meta["source_feature_file"],
            "feature_file": feature_meta["feature_file"],
            "feature_sha256": feature_meta["feature_sha256"],
            "source_model_file": model_meta["source_model_file"],
            "model_file": model_meta["model_file"],
            "model_sha256": model_meta["model_sha256"],
            "common_feature_path": common_feature_path,
            "common_feature_sha256": common_feature["sha256"],
            "common_model_path": common_model_path,
            "common_model_sha256": common_model["sha256"],
            "feature_count": feature_meta["feature_count"],
            "feature_order": feature_meta["feature_order"],
            "feature_order_hash": feature_meta["feature_order_hash"],
            "soft_feature_index": soft_feature_index,
            "soft_score_cuts": model_meta["soft_score_cuts"],
            "soft_score_terms": model_meta["soft_score_terms"],
            "rows": feature_meta["rows"],
            "total_signal_rows": feature_meta["total_signal_rows"],
            "high_soft_score_signal_rows": feature_meta["high_soft_score_signal_rows"],
            "high_soft_score_signal_ratio": feature_meta["high_soft_score_signal_ratio"],
            "context_missing_rows": feature_meta["context_missing_rows"],
            "claim_boundary": CLAIM_BOUNDARY,
        }
        feature_manifest.append(manifest_row)
        diagnostics_rows.append(
            {
                "candidate_alias": alias,
                "candidate_role": queue_row.get("candidate_role"),
                "soft_score_min": feature_meta["soft_score_min"],
                "soft_score_q50": feature_meta["soft_score_q50"],
                "soft_score_q80": feature_meta["soft_score_q80"],
                "soft_score_q95": feature_meta["soft_score_q95"],
                "soft_score_max": feature_meta["soft_score_max"],
                "signal_soft_score_q50": feature_meta["signal_soft_score_q50"],
                "signal_soft_score_q80": feature_meta["signal_soft_score_q80"],
                "high_soft_score_signal_rows": feature_meta["high_soft_score_signal_rows"],
                "high_soft_score_signal_ratio": feature_meta["high_soft_score_signal_ratio"],
                "atr_14_over_atr_50_q33": context_info["atr_14_over_atr_50_q33"],
                "atr_14_over_atr_50_q67": context_info["atr_14_over_atr_50_q67"],
                "adx_14_q33": context_info["adx_14_q33"],
                "adx_14_q67": context_info["adx_14_q67"],
            }
        )
        contract_rows.append(
            {
                "candidate_alias": alias,
                "candidate_role": queue_row.get("candidate_role"),
                "priority_lane": queue_row.get("priority_lane"),
                "shared_contract": "feature_order;score_table_csv;thresholds;MT5 runtime settings;2024 historical stress window",
                "feature_count": feature_meta["feature_count"],
                "feature_order_hash": feature_meta["feature_order_hash"],
                "model_backend": "ebm_table",
                "model_materialization_type": MODEL_MATERIALIZATION_TYPE,
                "short_threshold": spec.variant.short_threshold,
                "long_threshold": spec.variant.long_threshold,
                "min_margin": 0.0,
                "max_hold_bars": spec.variant.max_hold_bars,
                "close_on_flat_signal": spec.variant.close_on_flat_signal,
                "reverse_on_opposite_signal": spec.variant.reverse_on_opposite_signal,
                "close_only_on_opposite_signal": spec.variant.close_only_on_opposite_signal,
                "known_difference": "adds one ADX/ATR soft score feature and one small additive flat-bias model term; not a trained model replacement",
                "runtime_claim_boundary": "research_only_execution_pending_no_onnx_no_candidate_selection",
            }
        )
        lineage_rows.extend(
            [
                {
                    "candidate_alias": alias,
                    "artifact_role": "feature_csv",
                    "source_path": feature_meta["source_feature_file"],
                    "run267i_path": feature_meta["feature_file"],
                    "common_path": common_feature_path,
                    "run267i_sha256": feature_meta["feature_sha256"],
                    "common_sha256": common_feature["sha256"],
                },
                {
                    "candidate_alias": alias,
                    "artifact_role": "model_csv",
                    "source_path": model_meta["source_model_file"],
                    "run267i_path": model_meta["model_file"],
                    "common_path": common_model_path,
                    "run267i_sha256": model_meta["model_sha256"],
                    "common_sha256": common_model["sha256"],
                },
            ]
        )

        for role_index, (tier, attempt_role, prefix, attempt_token) in enumerate(
            (
                (input_probe.mt5.TIER_A, "tier_only_total", f"mt5_ta_{alias}_adxatrsoft", "ta"),
                (input_probe.mt5.TIER_AB, "routed_total", f"mt5_rt_{alias}_adxatrsoft", "rt"),
            ),
            start=1,
        ):
            magic = 26780000 + candidate_index * 100 + role_index
            payload = attempt_payload(
                run_root=DESIGN_ROOT,
                run_id=RUN_ID,
                stage_number=267,
                exploration_label="stage267_SoftNonCalendarAdapter__adxatrsoft",
                attempt_name=f"{alias}_adxatrsoft_{attempt_token}_2024",
                tier=tier,
                split=PERIOD_LABEL,
                model_path=common_model_path,
                model_id=f"{RUN_ID}_{alias}_adxatrsoft_score_table_extension_v1",
                model_backend="ebm_table",
                feature_path=common_feature_path,
                feature_count=int(feature_meta["feature_count"]),
                feature_order_hash=str(feature_meta["feature_order_hash"]),
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
                common_root=f"{COMMON_ROOT}/adxatrsoft/{alias}",
                fallback_enabled=False,
                close_on_flat_signal=spec.variant.close_on_flat_signal,
                reverse_on_opposite_signal=spec.variant.reverse_on_opposite_signal,
                close_only_on_opposite_signal=spec.variant.close_only_on_opposite_signal,
                extra_set_values=input_probe.base_extra_set_values(spec, magic),
            )
            payload.update(
                {
                    "candidate_alias": alias,
                    "candidate_role": queue_row.get("candidate_role"),
                    "feature_design": queue_row.get("feature_design"),
                    "model_materialization_type": MODEL_MATERIALIZATION_TYPE,
                    "execution_status": "not_executed",
                }
            )
            attempts.append(payload)

    return feature_manifest, contract_rows, diagnostics_rows, attempts, lineage_rows, context_info


def write_outputs(
    created_at: str,
    feature_manifest: Sequence[Mapping[str, Any]],
    contract_rows: Sequence[Mapping[str, Any]],
    diagnostics_rows: Sequence[Mapping[str, Any]],
    attempts: Sequence[Mapping[str, Any]],
    lineage_rows: Sequence[Mapping[str, Any]],
    context_info: Mapping[str, Any],
) -> dict[str, Any]:
    write_csv(
        FEATURE_MANIFEST_PATH,
        feature_manifest,
        (
            "candidate_alias",
            "candidate_role",
            "priority_lane",
            "feature_design",
            "adapter_mode",
            "model_materialization_type",
            "source_feature_file",
            "feature_file",
            "feature_sha256",
            "source_model_file",
            "model_file",
            "model_sha256",
            "common_feature_path",
            "common_feature_sha256",
            "common_model_path",
            "common_model_sha256",
            "feature_count",
            "feature_order",
            "feature_order_hash",
            "soft_feature_index",
            "soft_score_cuts",
            "soft_score_terms",
            "rows",
            "total_signal_rows",
            "high_soft_score_signal_rows",
            "high_soft_score_signal_ratio",
            "context_missing_rows",
            "claim_boundary",
        ),
    )
    write_csv(
        RUNTIME_CONTRACT_PATH,
        contract_rows,
        (
            "candidate_alias",
            "candidate_role",
            "priority_lane",
            "shared_contract",
            "feature_count",
            "feature_order_hash",
            "model_backend",
            "model_materialization_type",
            "short_threshold",
            "long_threshold",
            "min_margin",
            "max_hold_bars",
            "close_on_flat_signal",
            "reverse_on_opposite_signal",
            "close_only_on_opposite_signal",
            "known_difference",
            "runtime_claim_boundary",
        ),
    )
    write_csv(
        SOFT_SCORE_DIAGNOSTICS_PATH,
        diagnostics_rows,
        (
            "candidate_alias",
            "candidate_role",
            "soft_score_min",
            "soft_score_q50",
            "soft_score_q80",
            "soft_score_q95",
            "soft_score_max",
            "signal_soft_score_q50",
            "signal_soft_score_q80",
            "high_soft_score_signal_rows",
            "high_soft_score_signal_ratio",
            "atr_14_over_atr_50_q33",
            "atr_14_over_atr_50_q67",
            "adx_14_q33",
            "adx_14_q67",
        ),
    )
    write_csv(
        ATTEMPT_MANIFEST_PATH,
        build_attempt_rows(attempts),
        (
            "candidate_alias",
            "candidate_role",
            "feature_design",
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
    lineage = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "created_at_utc": created_at,
        "source_inputs": {
            "run267H_experiment_queue": rel(INPUT_QUEUE_PATH),
            "run267H_feature_matrix": rel(INPUT_FEATURE_MATRIX_PATH),
            "run267B_feature_manifest": rel(BASE_FEATURE_MANIFEST_PATH),
        },
        "producer": rel(PRODUCER_PATH),
        "consumer": NEXT_ACTION,
        "artifact_paths": {
            "feature_model_manifest": rel(FEATURE_MANIFEST_PATH),
            "runtime_contract": rel(RUNTIME_CONTRACT_PATH),
            "attempts": rel(ATTEMPT_MANIFEST_PATH),
            "soft_score_diagnostics": rel(SOFT_SCORE_DIAGNOSTICS_PATH),
            "run_manifest": rel(RUN_MANIFEST_PATH),
            "lineage": rel(LINEAGE_PATH),
            "result": rel(RESULT_PATH),
            "report": rel(REPORT_PATH),
        },
        "artifact_hashes": {
            "feature_model_manifest": sha256_file_lf_normalized(FEATURE_MANIFEST_PATH),
            "runtime_contract": sha256_file_lf_normalized(RUNTIME_CONTRACT_PATH),
            "attempts": sha256_file_lf_normalized(ATTEMPT_MANIFEST_PATH),
            "soft_score_diagnostics": sha256_file_lf_normalized(SOFT_SCORE_DIAGNOSTICS_PATH),
        },
        "lineage_rows": list(lineage_rows),
        "availability": "tracked_after_commit_reproducible_from_command",
        "lineage_judgment": "connected_with_boundary",
    }
    write_json(LINEAGE_PATH, lineage)
    run_manifest = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "status": STATUS,
        "created_at_utc": created_at,
        "period_label": PERIOD_LABEL,
        "candidate_aliases": [row["candidate_alias"] for row in feature_manifest],
        "feature_design": "adx_atr_soft_score",
        "model_materialization_type": MODEL_MATERIALIZATION_TYPE,
        "context_info": context_info,
        "attempts": build_attempt_rows(attempts),
        "claim_boundary": CLAIM_BOUNDARY,
        "next_action": NEXT_ACTION,
    }
    write_json(RUN_MANIFEST_PATH, run_manifest)
    result = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "status": STATUS,
        "created_at_utc": created_at,
        "candidate_count": len(feature_manifest),
        "attempt_count": len(attempts),
        "feature_count": 4,
        "model_materialization_type": MODEL_MATERIALIZATION_TYPE,
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "mt5_execution": "pending",
        "outputs": {
            "feature_model_manifest": rel(FEATURE_MANIFEST_PATH),
            "runtime_contract": rel(RUNTIME_CONTRACT_PATH),
            "attempts": rel(ATTEMPT_MANIFEST_PATH),
            "soft_score_diagnostics": rel(SOFT_SCORE_DIAGNOSTICS_PATH),
            "run_manifest": rel(RUN_MANIFEST_PATH),
            "lineage": rel(LINEAGE_PATH),
            "report": rel(REPORT_PATH),
        },
        "next_action": NEXT_ACTION,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(RESULT_PATH, result)
    write_md(REPORT_PATH, report_markdown(result, feature_manifest, diagnostics_rows, attempts))
    return result


def update_ledgers(created_at: str, result: Mapping[str, Any]) -> None:
    stage_row = {
        "row_id": "stage267_run267I_soft_noncalendar_adapter_materialization",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "view": "p0_soft_noncalendar_adapter_materialization",
        "tier_scope": "Tier A and Tier A+B historical 2024 materialization attempts planned",
        "scoreboard": "experiment_materialization",
        "status": STATUS,
        "judgment": "materialized_execution_pending_no_candidate_selection",
        "evidence_boundary": "feature_model_set_ini_materialized_no_mt5_execution",
        "report_path": rel(REPORT_PATH),
        "notes": f"candidate_count={result['candidate_count']};attempts={result['attempt_count']};next_action={NEXT_ACTION}.",
    }
    upsert_csv(
        STAGE_LEDGER_PATH,
        "row_id",
        [stage_row],
        ("row_id", "stage_id", "run_id", "view", "tier_scope", "scoreboard", "status", "judgment", "evidence_boundary", "report_path", "notes"),
    )
    run_registry_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "baseline_candidate_racing_p0_soft_adapter_materialization",
        "status": STATUS,
        "judgment": "materialized_execution_pending_no_candidate_selection",
        "path": rel(REPORT_PATH),
        "notes": f"P0 adx_atr_soft_score feature/model/set/ini materialized; next_action={NEXT_ACTION}.",
    }
    upsert_csv(
        RUN_REGISTRY_PATH,
        "run_id",
        [run_registry_row],
        ("run_id", "stage_id", "lane", "status", "judgment", "path", "notes"),
    )
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__p0_soft_noncalendar_adapter_materialization",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "p0_soft_noncalendar_adapter_materialization",
        "parent_run_id": RUN_ID,
        "record_view": "p0_soft_noncalendar_adapter_materialization",
        "tier_scope": "Tier A and Tier A+B historical 2024",
        "kpi_scope": "feature_model_set_ini_materialization",
        "scoreboard_lane": "experiment_materialization",
        "status": STATUS,
        "judgment": "materialized_execution_pending_no_candidate_selection",
        "path": rel(REPORT_PATH),
        "primary_kpi": f"candidate_count={result['candidate_count']};attempt_count={result['attempt_count']};feature_count=4",
        "guardrail_kpi": "selected_candidate=none;onnx_readiness=not_claimed;mt5_execution=pending",
        "external_verification_status": "out_of_scope_by_claim",
        "notes": f"Next action: {NEXT_ACTION}.",
    }
    upsert_csv(
        PROJECT_LEDGER_PATH,
        "ledger_row_id",
        [alpha_row],
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
    artifact_entries = (
        ("stage267_run267I_soft_adapter_materializer", "producer_script", PRODUCER_PATH, "Builds run267I P0 soft non-calendar Adapter materialization."),
        ("stage267_run267I_feature_model_manifest", "feature_model_manifest", FEATURE_MANIFEST_PATH, "Feature/model/common file manifest for run267I."),
        ("stage267_run267I_runtime_contract", "runtime_contract", RUNTIME_CONTRACT_PATH, "Runtime contract for run267I P0 variants."),
        ("stage267_run267I_attempt_manifest", "attempt_manifest", ATTEMPT_MANIFEST_PATH, "MT5 set/ini attempt manifest for run267I."),
        ("stage267_run267I_soft_score_diagnostics", "feature_diagnostics", SOFT_SCORE_DIAGNOSTICS_PATH, "Soft score diagnostics for run267I."),
        ("stage267_run267I_run_manifest", "run_manifest", RUN_MANIFEST_PATH, "Run manifest for run267I materialization."),
        ("stage267_run267I_lineage", "artifact_lineage", LINEAGE_PATH, "Feature/model lineage for run267I."),
        ("stage267_run267I_result", "result", RESULT_PATH, "JSON result for run267I materialization."),
        ("stage267_run267I_report", "review_report", REPORT_PATH, "User-facing run267I materialization report."),
    )
    artifact_rows = []
    for artifact_id, artifact_type, path, notes in artifact_entries:
        artifact_rows.append(
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
    upsert_csv(
        ARTIFACT_REGISTRY_PATH,
        "artifact_id",
        artifact_rows,
        ("artifact_id", "artifact_type", "path", "sha256", "stage_id", "run_id", "created_at_utc", "notes"),
    )


def update_current_truth_docs() -> None:
    report_line_current = (
        "- Stage267(267단계) run267I P0 soft non-calendar Adapter materialization(P0 부드러운 비달력 어댑터 물질화): "
        f"`{rel(REPORT_PATH)}`"
    )

    current = io_path(CURRENT_WORKING_STATE_PATH).read_text(encoding="utf-8-sig")
    current = replace_if_present(current, "- current_run(현재 실행): `run267H_stage267_soft_noncalendar_adapter_design_v1`", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_if_present(current, "- status(상태): `run267H_soft_noncalendar_adapter_design_completed`", f"- status(상태): `{STATUS}`")
    current = append_after(
        current,
        "- Stage267(267단계) run267H soft non-calendar Adapter design(부드러운 비달력 어댑터 설계): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267H_soft_noncalendar_adapter_design.md`",
        report_line_current,
    )
    current = replace_if_present(current, "- next_run(다음 실행): `run267I_materialize_top_soft_noncalendar_adapter_candidates`", f"- next_run(다음 실행): `{NEXT_ACTION}`")
    current = replace_if_present(
        current,
        "- action(행동): run267H(267H 실행)에서 soft feature engineering matrix(부드러운 피처 엔지니어링 행렬), Adapter surface matrix(어댑터 표면 행렬), experiment queue(실험 대기열)를 만들었다.",
        "- action(행동): run267I(267I 실행)에서 P0 후보 `s264_aih`, `s264_lc`의 `adx_atr_soft_score` feature/model/set/ini(피처/모델/설정/초기화) 묶음을 만들었다.",
    )
    current = replace_if_present(
        current,
        "- effect(효과): hard guard(강한 방어)를 반복하지 않고 `s264_aih` 핵심 후보와 `s264_lc` 방어 기준을 P0 materialization(우선 물질화) 후보로 좁힌다.",
        "- effect(효과): hard guard(강한 방어)가 아니라 부드러운 ADX/ATR 점수(soft ADX/ATR score, 부드러운 ADX/ATR 점수)를 모델 입력으로 붙여 다음 MT5(MetaTrader 5, 메타트레이더5) 실행에서 덜 깨지는지 볼 수 있게 했다.",
    )
    current = replace_if_present(
        current,
        "- next_action(다음 행동): `run267I_materialize_top_soft_noncalendar_adapter_candidates`. Effect(효과): P0 soft non-calendar Adapter(부드러운 비달력 어댑터) 후보를 실제 feature/model/set/ini(피처/모델/설정/초기화) 묶음으로 물질화할지 검증한다.",
        f"- next_action(다음 행동): `{NEXT_ACTION}`. Effect(효과): 물질화된 P0 soft non-calendar Adapter(부드러운 비달력 어댑터) 후보를 MT5(MetaTrader 5, 메타트레이더5) batch(묶음)로 실행해 거래 수, PF(수익 팩터), DD(drawdown, 손실폭), 약한 월을 검증한다.",
    )
    write_md(CURRENT_WORKING_STATE_PATH, current)

    selection = io_path(SELECTION_STATUS_PATH).read_text(encoding="utf-8-sig")
    selection = replace_if_present(selection, "- stage_status(단계 상태): `run267H_soft_noncalendar_adapter_design_completed`", f"- stage_status(단계 상태): `{STATUS}`")
    selection = replace_if_present(selection, "- current_run(현재 실행): `run267H_stage267_soft_noncalendar_adapter_design_v1`", f"- current_run(현재 실행): `{RUN_ID}`")
    selection = replace_if_present(selection, "- last_completed_run(마지막 완료 실행): `run267H_stage267_soft_noncalendar_adapter_design_v1`", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
    selection = append_after(
        selection,
        "- run267H_soft_noncalendar_adapter_design(267H 부드러운 비달력 어댑터 설계): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267H_soft_noncalendar_adapter_design.md`",
        f"- run267I_soft_noncalendar_adapter_materialization(267I 부드러운 비달력 어댑터 물질화): `{rel(REPORT_PATH)}`",
    )
    selection = replace_if_present(selection, "- next_action(다음 행동): `run267I_materialize_top_soft_noncalendar_adapter_candidates`", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    selection = replace_if_present(
        selection,
        "Run267H(267H 실행)는 soft non-calendar Adapter design(부드러운 비달력 어댑터 설계)을 완료했다.\nEffect(효과): 선택 후보(selected candidate, 선택 후보)는 계속 없고, P0 물질화 후보는 `s264_aih` core(핵심)와 `s264_lc` control(기준)의 `adx_atr_soft_score`로 좁힌다.",
        "Run267I(267I 실행)는 P0 soft non-calendar Adapter materialization(P0 부드러운 비달력 어댑터 물질화)을 완료했다.\nEffect(효과): 선택 후보(selected candidate, 선택 후보)는 계속 없고, 다음은 물질화된 `s264_aih`, `s264_lc` `adx_atr_soft_score` 묶음을 MT5(MetaTrader 5, 메타트레이더5)에서 실행해 비교한다.",
    )
    write_md(SELECTION_STATUS_PATH, selection)

    review = io_path(REVIEW_INDEX_PATH).read_text(encoding="utf-8-sig")
    review = replace_if_present(review, "- status(상태): `run267H_soft_noncalendar_adapter_design_completed`", f"- status(상태): `{STATUS}`")
    review = replace_if_present(review, "- current_run(현재 실행): `run267H_stage267_soft_noncalendar_adapter_design_v1`", f"- current_run(현재 실행): `{RUN_ID}`")
    review = replace_if_present(review, "- last_completed_run(마지막 완료 실행): `run267H_stage267_soft_noncalendar_adapter_design_v1`", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
    review = append_after(
        review,
        "- run267H_soft_noncalendar_adapter_design(267H 부드러운 비달력 어댑터 설계): `stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267H_soft_noncalendar_adapter_design.md`",
        f"- run267I_soft_noncalendar_adapter_materialization(267I 부드러운 비달력 어댑터 물질화): `{rel(REPORT_PATH)}`",
    )
    review = replace_if_present(
        review,
        "Run267H(267H 실행)는 soft non-calendar Adapter design(부드러운 비달력 어댑터 설계)을 완료했다.",
        "Run267I(267I 실행)는 P0 soft non-calendar Adapter materialization(P0 부드러운 비달력 어댑터 물질화)을 완료했다.",
    )
    review = replace_if_present(
        review,
        "Effect(효과): Stage267(267단계)는 후보 선택(selected candidate, 선택 후보)이나 ONNX readiness(ONNX 준비)를 주장하지 않고, `run267I_materialize_top_soft_noncalendar_adapter_candidates`에서 P0 soft non-calendar Adapter(우선순위 0 부드러운 비달력 어댑터) 후보 물질화를 검토한다.",
        f"Effect(효과): Stage267(267단계)는 후보 선택(selected candidate, 선택 후보)이나 ONNX readiness(ONNX 준비)를 주장하지 않고, `{NEXT_ACTION}`에서 P0 soft non-calendar Adapter(우선순위 0 부드러운 비달력 어댑터) MT5(MetaTrader 5, 메타트레이더5) 실행을 검토한다.",
    )
    write_md(REVIEW_INDEX_PATH, review)

    workspace = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    workspace = replace_if_present(workspace, "current_run_id: run267H_stage267_soft_noncalendar_adapter_design_v1", f"current_run_id: {RUN_ID}")
    workspace = replace_if_present(workspace, "  Stage267(267단계) run267H(267H 실행) soft non-calendar Adapter design(부드러운 비달력 어댑터 설계) `run267H_soft_noncalendar_adapter_design_completed`. Effect(효과): P0 materialization(우선 물질화) 후보를 `s264_aih`와 `s264_lc`의 `adx_atr_soft_score`로 좁혔지만 selected candidate(선택 후보)나 ONNX readiness(ONNX 준비)는 주장하지 않는다.", f"  Stage267(267단계) run267I(267I 실행) P0 soft non-calendar Adapter materialization(P0 부드러운 비달력 어댑터 물질화) `{STATUS}`. Effect(효과): `s264_aih`와 `s264_lc`의 `adx_atr_soft_score` feature/model/set/ini(피처/모델/설정/초기화) 묶음을 만들었지만 selected candidate(선택 후보)나 ONNX readiness(ONNX 준비)는 주장하지 않는다.")
    workspace = replace_if_present(workspace, "  Next action(다음 행동)는 `run267I_materialize_top_soft_noncalendar_adapter_candidates`이다. Effect(효과): P0 soft non-calendar Adapter(부드러운 비달력 어댑터) 후보를 실제 feature/model/set/ini(피처/모델/설정/초기화) 묶음으로 물질화할지 검증한다.", f"  Next action(다음 행동)는 `{NEXT_ACTION}`이다. Effect(효과): 물질화된 P0 soft non-calendar Adapter(부드러운 비달력 어댑터) 후보를 MT5(MetaTrader 5, 메타트레이더5) batch(묶음)로 실행해 약한 구간과 거래 품질을 본다.")
    workspace = replace_if_present(workspace, "is active_run267H_soft_noncalendar_adapter_design_completed(267H 부드러운 비달력 어댑터 설계 완료 활성)", "is active_run267I_p0_soft_noncalendar_adapter_materialized_execution_pending(267I P0 부드러운 비달력 어댑터 물질화 완료, 실행 대기 활성)")
    workspace = replace_if_present(workspace, "  status: run267H_soft_noncalendar_adapter_design_completed", f"  status: {STATUS}")
    workspace = replace_if_present(workspace, "  current_run_id: run267H_stage267_soft_noncalendar_adapter_design_v1", f"  current_run_id: {RUN_ID}")
    workspace = replace_if_present(workspace, "  last_completed_run_id: run267H_stage267_soft_noncalendar_adapter_design_v1", f"  last_completed_run_id: {RUN_ID}")
    workspace = append_after(
        workspace,
        "  run267H_soft_noncalendar_adapter_design_path: stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_run267H_soft_noncalendar_adapter_design.md",
        f"  run267I_soft_noncalendar_adapter_materialization_path: {rel(REPORT_PATH)}",
    )
    workspace = replace_if_present(workspace, "  next_action: run267I_materialize_top_soft_noncalendar_adapter_candidates", f"  next_action: {NEXT_ACTION}")
    write_md(WORKSPACE_STATE_PATH, workspace)


def report_markdown(
    result: Mapping[str, Any],
    feature_manifest: Sequence[Mapping[str, Any]],
    diagnostics_rows: Sequence[Mapping[str, Any]],
    attempts: Sequence[Mapping[str, Any]],
) -> str:
    lines = [
        "# Stage267 Run267I Soft Non-Calendar Adapter Materialization(267단계 267I 부드러운 비달력 어댑터 물질화)",
        "",
        "- action(행동): run267H(267H 실행)의 P0 queue(P0 대기열)를 받아 `s264_aih`, `s264_lc`의 `adx_atr_soft_score` feature/model/set/ini(피처/모델/설정/초기화) 묶음을 만들었다.",
        "- effect(효과): 다음 MT5(MetaTrader 5, 메타트레이더5) 실행에서 hard guard(강한 방어)가 아니라 soft score(부드러운 점수) 모델 입력이 약한 월/구간을 덜 깨뜨리는지 검증할 수 있다.",
        f"- candidate_count(후보 수): `{result['candidate_count']}`",
        f"- attempt_count(시도 수): `{result['attempt_count']}`",
        f"- feature_count(피처 수): `{result['feature_count']}`",
        f"- model_materialization_type(모델 물질화 유형): `{MODEL_MATERIALIZATION_TYPE}`",
        f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
        "",
        "## Easy Read(쉬운 판독)",
        "",
        "이번 작업은 숫자가 좋아졌다는 판정이 아니다. 실제 실행 가능한 입력 묶음을 만든 것이다.",
        "`s264_aih`는 core challenger(핵심 도전자), `s264_lc`는 defensive control(방어 기준)로 함께 물질화했다.",
        "모델은 true retrain(진짜 재학습)이 아니라 작은 additive score-table extension(가산 점수표 확장)이다. 효과는 MT5(MetaTrader 5, 메타트레이더5) 실행 전 단계에서 feature order(피처 순서), model hash(모델 해시), set/ini(설정/초기화)를 먼저 고정하는 것이다.",
        "",
        "## Materialized Candidates(물질화 후보)",
        "",
        "| lane(레인) | candidate(후보) | feature hash(피처 해시) | model hash(모델 해시) | high score signal ratio(높은 점수 신호 비율) |",
        "| --- | --- | --- | --- | --- |",
    ]
    diagnostics_by_alias = {row["candidate_alias"]: row for row in diagnostics_rows}
    for row in feature_manifest:
        diag = diagnostics_by_alias[str(row["candidate_alias"])]
        lines.append(
            "| "
            f"`{row['priority_lane']}` | `{row['candidate_alias']}` | "
            f"`{str(row['feature_sha256'])[:12]}` | `{str(row['model_sha256'])[:12]}` | "
            f"`{cell(diag.get('high_soft_score_signal_ratio'))}` |"
        )
    lines.extend(
        [
            "",
            "## Experiment Design Receipt(실험 설계 기록)",
            "",
            "- hypothesis(가설): ADX/ATR(추세 강도/ATR) 약점 문맥은 hard block(강한 차단)보다 soft model feature(부드러운 모델 피처)로 넣을 때 거래 수 붕괴를 줄일 수 있다.",
            "- decision_use(결정 용도): 다음 MT5(MetaTrader 5, 메타트레이더5) batch(묶음) 실행에서 P0 후보를 계속 밀지, branch(분기)를 닫을지 판단한다.",
            "- comparison_baseline(비교 기준): run267D atrcomp(ATR 압축), run267E Monday guard(월요일 방어), run267F adx2025/dilowq33(ADX/DI 방어), run267H design(설계).",
            "- control_variables(고정 변수): 후보 2개, 2024 historical window(2024 과거 구간), thresholds(임계값), trade management(거래 관리), MT5 EA(MetaTrader 5 Expert Advisor, 메타트레이더5 전문가 자문).",
            "- changed_variables(변경 변수): `stage267_adx_atr_soft_score` feature(피처), feature order hash(피처 순서 해시), additive score-table term(가산 점수표 항).",
            "- success_criteria(성공 기준): net/PF(순수익/수익 팩터), trade count(거래 수), DD(drawdown, 손실폭), Monday/July/chron_mid(월요일/7월/중간 구간)가 함께 덜 깨져야 한다.",
            "- failure_criteria(실패 기준): 거래 수 붕괴, DD(drawdown, 손실폭) 악화, 약한 월 미개선, 또는 P0 control(우선순위 0 기준)까지 함께 망가지면 실패다.",
            "- invalid_conditions(무효 조건): feature order mismatch(피처 순서 불일치), model hash missing(모델 해시 누락), set/ini path missing(설정/초기화 경로 누락), MT5 report missing(MT5 보고서 누락).",
            "- stop_conditions(중단 조건): 실행 후 hard guard(강한 방어)보다 낫지 않거나 약한 구간이 그대로면 ADX/ATR soft branch(부드러운 분기)를 닫거나 true retrain(진짜 재학습) 설계로 전환한다.",
            "- evidence_plan(근거 계획): attempt manifest(시도 목록), MT5 reports(MT5 보고서), trade/time-slice/curve review(거래/시간 구간/곡선 검토), artifact hashes(산출물 해시).",
            "",
            "## Artifact Lineage(산출물 계보)",
            "",
            f"- source_inputs(원천 입력): `{rel(INPUT_QUEUE_PATH)}`, `{rel(INPUT_FEATURE_MATRIX_PATH)}`, `{rel(BASE_FEATURE_MANIFEST_PATH)}`",
            f"- producer(생산자): `{rel(PRODUCER_PATH)}`",
            f"- consumer(소비자): `{NEXT_ACTION}`",
            f"- artifact_paths(산출물 경로): `{rel(FEATURE_MANIFEST_PATH)}`, `{rel(RUNTIME_CONTRACT_PATH)}`, `{rel(ATTEMPT_MANIFEST_PATH)}`, `{rel(SOFT_SCORE_DIAGNOSTICS_PATH)}`, `{rel(RUN_MANIFEST_PATH)}`, `{rel(LINEAGE_PATH)}`, `{rel(RESULT_PATH)}`",
            "- availability(가용성): tracked(추적됨) after commit; reproducible_from_command(명령으로 재생성 가능).",
            "- lineage_judgment(계보 판정): `connected_with_boundary`.",
            "",
            "## Judgment Boundary(판정 경계)",
            "",
            "- result_subject(결과 대상): `run267I_p0_soft_noncalendar_adapter_materialization`.",
            "- evidence_available(사용 가능 근거): feature/model/set/ini(피처/모델/설정/초기화) 산출물, runtime contract(런타임 계약), hash(해시), manifest(목록).",
            "- evidence_missing(빠진 근거): MT5 execution(MT5 실행), balance/equity curve(잔액/평가금 곡선), trade/time-slice KPI(거래/시간 구간 핵심 성과 지표).",
            "- judgment_label(판정 라벨): `materialized_execution_pending_no_candidate_selection`.",
            "- selected_candidate(선택 후보): `none`.",
            "- ONNX readiness(ONNX 준비): `not_claimed`.",
            f"- next_action(다음 행동): `{NEXT_ACTION}`.",
        ]
    )
    return "\n".join(lines)


def materialize() -> dict[str, Any]:
    created_at = utc_now()
    feature_manifest, contract_rows, diagnostics_rows, attempts, lineage_rows, context_info = materialize_payload()
    result = write_outputs(created_at, feature_manifest, contract_rows, diagnostics_rows, attempts, lineage_rows, context_info)
    update_ledgers(created_at, result)
    update_current_truth_docs()
    return result


def main() -> None:
    result = materialize()
    print(json.dumps(json_ready(result), ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
