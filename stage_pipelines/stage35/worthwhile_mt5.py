from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any, Mapping, Sequence

import pandas as pd

from foundation.control_plane import mt5_kpi_recorder, mt5_trade_attribution
from foundation.control_plane.mt5_tier_balance_completion import (
    COMMON_FILES_ROOT_DEFAULT,
    METAEDITOR_PATH_DEFAULT,
    TERMINAL_DATA_ROOT_DEFAULT,
    TERMINAL_PATH_DEFAULT,
    TESTER_PROFILE_ROOT_DEFAULT,
    attempt_payload,
    common_run_root,
    copy_to_common,
    execute_prepared_run,
)
from foundation.mt5 import runtime_support as mt5
from stage_pipelines.stage35 import atlas_model, common
from stage_pipelines.stage35 import worthwhile_config as cfg
from stage_pipelines.stage35 import worthwhile_variants


def _runtime_split(split_name: str) -> str:
    return "validation_is" if split_name == "validation" else split_name


def materialize_runtime_inputs(frame: pd.DataFrame, variants: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    common_root = common_run_root(cfg.STAGE_NUMBER, cfg.RUN_ID)
    common_copies: list[dict[str, Any]] = []
    model_outputs: dict[str, dict[str, Any]] = {}
    for direction in sorted({str(row["direction"]) for row in variants}):
        model_path = cfg.RUN_ROOT / "models" / f"{direction}_constant_score_table.csv"
        model_outputs[direction] = atlas_model.write_constant_score_table(model_path, direction)
        common_copies.append(copy_to_common(model_path, f"{common_root}/models/{model_path.name}", COMMON_FILES_ROOT_DEFAULT))

    feature_outputs: dict[str, dict[str, dict[str, Any]]] = {}
    skipped_empty_features: list[dict[str, Any]] = []
    for variant in variants:
        variant_id = str(variant["variant_id"])
        mask = worthwhile_variants.variant_mask(frame, variant_id)
        feature_outputs[variant_id] = {}
        for split_name in variant["splits"]:
            split_label = _runtime_split(str(split_name))
            selected = frame.loc[frame["split"].astype(str).eq(str(split_name)) & mask, ["timestamp", "split", *cfg.FEATURE_ORDER]].copy()
            selected["variant_id"] = variant_id
            output = cfg.RUN_ROOT / "features" / f"{variant_id}_{split_label}_features.csv"
            export = mt5.export_mt5_feature_matrix_csv(selected, cfg.FEATURE_ORDER, output, metadata_columns=("variant_id",))
            export["tester_window_from_date"], export["tester_window_to_date"] = common.split_dates(frame, str(split_name))
            export["source_row_count"] = int(len(selected))
            feature_outputs[variant_id][split_label] = export
            common_copies.append(copy_to_common(output, f"{common_root}/features/{output.name}", COMMON_FILES_ROOT_DEFAULT))
            if int(export["source_row_count"]) <= 0:
                skipped_empty_features.append({"variant_id": variant_id, "split": split_label, "path": export["path"]})
    return {
        "common_root": common_root,
        "model_outputs": model_outputs,
        "feature_outputs": feature_outputs,
        "skipped_empty_features": skipped_empty_features,
        "common_copies": common_copies,
        "known_runtime_difference": "variant masks are precomputed in Python and handed to MT5 by feature-row omission; this is runtime_probe, not native runtime authority.",
    }


def build_attempts(runtime_inputs: Mapping[str, Any], variants: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    attempts: list[dict[str, Any]] = []
    common_root = str(runtime_inputs["common_root"])
    for variant in variants:
        variant_id = str(variant["variant_id"])
        direction = str(variant["direction"])
        model_file = Path(str(runtime_inputs["model_outputs"][direction]["path"])).name
        for split in runtime_inputs["feature_outputs"][variant_id]:
            feature = runtime_inputs["feature_outputs"][variant_id][split]
            if int(feature.get("source_row_count") or 0) <= 0:
                continue
            feature_file = Path(str(feature["path"])).name
            attempts.append(
                attempt_payload(
                    run_root=cfg.RUN_ROOT,
                    run_id=cfg.RUN_ID,
                    stage_number=cfg.STAGE_NUMBER,
                    exploration_label=cfg.EXPLORATION_LABEL,
                    attempt_name=f"tier_a_{variant_id}_{split}",
                    tier=mt5.TIER_A,
                    split=split,
                    model_path=f"{common_root}/models/{model_file}",
                    model_id=f"{cfg.RUN_ID}_{variant_id}_{direction}_constant",
                    model_backend="ebm_table",
                    feature_path=f"{common_root}/features/{feature_file}",
                    feature_count=len(cfg.FEATURE_ORDER),
                    feature_order_hash=cfg.FEATURE_ORDER_HASH,
                    short_threshold=0.55,
                    long_threshold=0.55,
                    min_margin=0.05,
                    invert_signal=False,
                    from_date=str(feature["tester_window_from_date"]),
                    to_date=str(feature["tester_window_to_date"]),
                    primary_active_tier="tier_a",
                    attempt_role="tier_only_total",
                    record_view_prefix=f"mt5_tier_a_deep_{variant_id}",
                    max_hold_bars=cfg.MAX_HOLD_BARS,
                    common_root=common_root,
                    close_on_flat_signal=True,
                )
            )
    return attempts


def normalize_records(records: Sequence[Mapping[str, Any]], variants: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    by_variant = {str(row["variant_id"]): row for row in variants}
    variant_ids = sorted(by_variant, key=len, reverse=True)
    out: list[dict[str, Any]] = []
    for record in records:
        current = dict(record)
        view = str(current.get("record_view", ""))
        variant_id = next((variant for variant in variant_ids if variant in view), "unknown")
        variant = by_variant.get(variant_id, {})
        current["source_variant_id"] = variant_id
        current["source_family"] = variant.get("family")
        current["state_direction"] = variant.get("direction")
        current["topic_read"] = "stage35_worthwhile_deep_sweep_runtime_probe"
        metrics = dict(current.get("metrics", {})) if isinstance(current.get("metrics"), Mapping) else {}
        metrics["route_role"] = "tier_only_total"
        metrics["source_variant_id"] = variant_id
        metrics["state_direction"] = variant.get("direction")
        current["route_role"] = "tier_only_total"
        current["metrics"] = metrics
        out.append(current)
    return out


def execute_or_block(prepared: Mapping[str, Any], args: argparse.Namespace, variants: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    if bool(args.reuse_existing_result):
        manifest = common.read_json(cfg.RUN_ROOT / "run_manifest.json")
        kpi_record = common.read_json(cfg.RUN_ROOT / "kpi_record.json")
        runtime_probe = manifest.get("runtime_probe", {}) if isinstance(manifest, Mapping) else {}
        return {
            **dict(prepared),
            "compile": runtime_probe.get("compile", {}),
            "execution_results": runtime_probe.get("execution_results", []),
            "strategy_tester_reports": runtime_probe.get("strategy_tester_reports", []),
            "mt5_kpi_records": normalize_records(kpi_record.get("mt5_kpi_records", []), variants),
            "external_verification_status": kpi_record.get("external_verification_status"),
            "judgment": kpi_record.get("judgment"),
        }
    if bool(args.materialize_only):
        return {
            **dict(prepared),
            "compile": {"status": "not_attempted_materialize_only"},
            "execution_results": [],
            "strategy_tester_reports": [],
            "mt5_kpi_records": [],
            "external_verification_status": "not_attempted_materialize_only",
            "judgment": "not_attempted_materialize_only",
        }
    try:
        result = execute_prepared_run(
            prepared,
            terminal_path=Path(args.terminal_path),
            metaeditor_path=Path(args.metaeditor_path),
            terminal_data_root=TERMINAL_DATA_ROOT_DEFAULT,
            common_files_root=COMMON_FILES_ROOT_DEFAULT,
            tester_profile_root=TESTER_PROFILE_ROOT_DEFAULT,
            timeout_seconds=int(args.timeout_seconds),
        )
    except Exception as exc:
        return {
            **dict(prepared),
            "compile": {"status": "exception_or_not_completed"},
            "execution_results": [],
            "strategy_tester_reports": [],
            "mt5_kpi_records": [],
            "external_verification_status": "blocked",
            "judgment": cfg.JUDGMENT_BLOCKED,
            "failure": {"type": type(exc).__name__, "message": str(exc)},
        }
    completed = result.get("external_verification_status") == "completed"
    result = dict(result)
    result["judgment"] = cfg.JUDGMENT_COMPLETED if completed else cfg.JUDGMENT_BLOCKED
    result["mt5_kpi_records"] = normalize_records(result.get("mt5_kpi_records", []), variants)
    return result


def write_normalized_kpi() -> dict[str, Any]:
    inventory = [{"run_id": cfg.RUN_ID, "stage_id": cfg.STAGE_ID, "idea_id": cfg.RUN_NUMBER, "path": common.rel(cfg.RUN_ROOT)}]
    records, summary_rows, missing, parser_errors = mt5_kpi_recorder.build_normalized_records(common.ROOT, inventory)
    enriched: list[dict[str, Any]] = list(records)
    trade_rows: list[dict[str, Any]] = []
    trade_summary: list[dict[str, Any]] = []
    trade_errors: list[dict[str, Any]] = []
    if records:
        market_data = mt5_trade_attribution.MarketData.load(common.ROOT)
        enriched, trade_rows, trade_summary, trade_errors = mt5_trade_attribution.enrich_records(records, common.ROOT, market_data)
    common.write_json(cfg.PACKET_ROOT / "normalized_kpi_records.json", records)
    common.write_json(cfg.PACKET_ROOT / "normalized_kpi_summary.json", summary_rows)
    common.write_json(cfg.PACKET_ROOT / "normalized_kpi_missing_runs.json", missing)
    common.write_json(cfg.PACKET_ROOT / "normalized_kpi_parser_errors.json", parser_errors)
    common.write_json(cfg.PACKET_ROOT / "enriched_kpi_records.json", enriched)
    common.write_json(cfg.PACKET_ROOT / "trade_level_records.json", trade_rows)
    common.write_json(cfg.PACKET_ROOT / "trade_attribution_summary.json", trade_summary)
    common.write_json(cfg.PACKET_ROOT / "trade_attribution_parser_errors.json", trade_errors)
    return {
        "normalized_records": len(records),
        "normalized_summary_rows": len(summary_rows),
        "missing_runs": len(missing),
        "parser_errors": len(parser_errors),
        "trade_attribution_records": len(trade_summary),
        "trade_level_rows": len(trade_rows),
        "trade_parser_errors": len(trade_errors),
    }
