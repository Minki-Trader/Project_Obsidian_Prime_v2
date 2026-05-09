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
from stage_pipelines.stage35 import atlas_config as cfg
from stage_pipelines.stage35 import atlas_model, common


def _split_label(split_name: str) -> str:
    return "validation_is" if split_name == "validation" else split_name


def materialize_runtime_inputs(atlas: Mapping[str, Any]) -> dict[str, Any]:
    assignments = atlas["frame"]
    common_root = common_run_root(cfg.STAGE_NUMBER, cfg.RUN_ID)
    feature_outputs: dict[str, dict[str, Any]] = {}
    model_outputs: dict[str, dict[str, Any]] = {}
    common_copies: list[dict[str, Any]] = []
    for selection in atlas["selections"]:
        topic_id = str(selection["topic_id"])
        direction = str(selection["state_direction"])
        model_path = cfg.RUN_ROOT / "models" / f"{topic_id}_{direction}_constant_score_table.csv"
        model_outputs[topic_id] = atlas_model.write_constant_score_table(model_path, direction)
        common_copies.append(copy_to_common(model_path, f"{common_root}/models/{model_path.name}", COMMON_FILES_ROOT_DEFAULT))
        feature_outputs[topic_id] = {}
        for split_name in ("validation", "oos"):
            selected = atlas_model.selected_frame(assignments, selection, split_name)
            local_path = cfg.RUN_ROOT / "features" / f"{topic_id}_{_split_label(split_name)}_state_features.csv"
            export = mt5.export_mt5_feature_matrix_csv(
                selected,
                cfg.FEATURE_ORDER,
                local_path,
                metadata_columns=(f"state_{topic_id}",),
            )
            export["tester_window_from_date"], export["tester_window_to_date"] = common.split_dates(assignments, split_name)
            export["selected_state_id"] = int(selection["selected_state_id"])
            export["state_direction"] = direction
            export["source_row_count"] = int(len(selected))
            feature_outputs[topic_id][_split_label(split_name)] = export
            common_copies.append(copy_to_common(local_path, f"{common_root}/features/{local_path.name}", COMMON_FILES_ROOT_DEFAULT))
    return {
        "common_root": common_root,
        "feature_outputs": feature_outputs,
        "model_outputs": model_outputs,
        "common_copies": common_copies,
        "known_runtime_difference": "atlas state assignment is precomputed in Python and handed to MT5 by feature-row omission; this is runtime_probe, not native runtime authority.",
    }


def build_attempts(runtime_inputs: Mapping[str, Any], selections: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    attempts: list[dict[str, Any]] = []
    common_root = str(runtime_inputs["common_root"])
    for selection in selections:
        topic_id = str(selection["topic_id"])
        direction = str(selection["state_direction"])
        model_file = Path(str(runtime_inputs["model_outputs"][topic_id]["path"])).name
        for split in ("validation_is", "oos"):
            feature = runtime_inputs["feature_outputs"][topic_id][split]
            feature_file = Path(str(feature["path"])).name
            attempts.append(
                attempt_payload(
                    run_root=cfg.RUN_ROOT,
                    run_id=cfg.RUN_ID,
                    stage_number=cfg.STAGE_NUMBER,
                    exploration_label=cfg.EXPLORATION_LABEL,
                    attempt_name=f"tier_a_{topic_id}_{split}",
                    tier=mt5.TIER_A,
                    split=split,
                    model_path=f"{common_root}/models/{model_file}",
                    model_id=f"{cfg.RUN_ID}_{topic_id}_{direction}_constant",
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
                    record_view_prefix=f"mt5_tier_a_atlas_{topic_id}",
                    max_hold_bars=cfg.MAX_HOLD_BARS,
                    common_root=common_root,
                    close_on_flat_signal=True,
                )
            )
    return attempts


def normalize_records(records: Sequence[Mapping[str, Any]], selections: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    by_topic = {str(item["topic_id"]): item for item in selections}
    out: list[dict[str, Any]] = []
    for record in records:
        current = dict(record)
        view = str(current.get("record_view", ""))
        topic_id = next((topic for topic in by_topic if topic in view), "unknown")
        selection = by_topic.get(topic_id, {})
        current["source_topic_id"] = topic_id
        current["selected_state_id"] = selection.get("selected_state_id")
        current["state_direction"] = selection.get("state_direction")
        current["topic_read"] = "stage35_unsupervised_market_state_atlas_runtime_probe"
        metrics = dict(current.get("metrics", {})) if isinstance(current.get("metrics"), Mapping) else {}
        metrics["route_role"] = "tier_only_total"
        metrics["selected_state_id"] = selection.get("selected_state_id")
        metrics["state_direction"] = selection.get("state_direction")
        current["route_role"] = "tier_only_total"
        current["metrics"] = metrics
        out.append(current)
    return out


def execute_or_block(prepared: Mapping[str, Any], args: argparse.Namespace, selections: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    if bool(args.reuse_existing_result):
        manifest = common.read_json(cfg.RUN_ROOT / "run_manifest.json")
        kpi_record = common.read_json(cfg.RUN_ROOT / "kpi_record.json")
        runtime_probe = manifest.get("runtime_probe", {}) if isinstance(manifest, Mapping) else {}
        return {
            **dict(prepared),
            "compile": runtime_probe.get("compile", {}),
            "execution_results": runtime_probe.get("execution_results", []),
            "strategy_tester_reports": runtime_probe.get("strategy_tester_reports", []),
            "mt5_kpi_records": normalize_records(kpi_record.get("mt5_kpi_records", []), selections),
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
    result["mt5_kpi_records"] = normalize_records(result.get("mt5_kpi_records", []), selections)
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

