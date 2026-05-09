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
from stage_pipelines.stage35 import atlas_model, common, worthwhile_variants
from stage_pipelines.stage35 import candidate_config as cfg


def _window_dates(frame: pd.DataFrame) -> tuple[str, str]:
    if frame.empty:
        raise RuntimeError("empty stress frame")
    timestamps = pd.to_datetime(frame["timestamp"], utc=True)
    return timestamps.min().strftime("%Y.%m.%d"), (timestamps.max() + pd.Timedelta(days=1)).strftime("%Y.%m.%d")


def _stress_specs() -> list[dict[str, Any]]:
    specs: list[dict[str, Any]] = []
    for hold in cfg.HOLD_VALUES:
        specs.append({"stress_id": f"validation_h{hold}", "source_split": "validation", "stress": "base_hold", "max_hold_bars": hold})
        specs.append({"stress_id": f"oos_h{hold}", "source_split": "oos", "stress": "base_hold", "max_hold_bars": hold})
    specs.extend(
        [
            {"stress_id": "oos_no_oct2025_h12", "source_split": "oos", "stress": "no_oct2025", "max_hold_bars": 12},
            {"stress_id": "oos_first_half_h12", "source_split": "oos", "stress": "first_half", "max_hold_bars": 12},
            {"stress_id": "oos_second_half_h12", "source_split": "oos", "stress": "second_half", "max_hold_bars": 12},
        ]
    )
    return specs


def _apply_stress(frame: pd.DataFrame, stress: str) -> pd.DataFrame:
    work = frame.copy()
    timestamps = pd.to_datetime(work["timestamp"], utc=True)
    if stress == "no_oct2025":
        return work.loc[~timestamps.dt.strftime("%Y-%m").eq("2025-10")].copy()
    if stress in {"first_half", "second_half"}:
        ordered = timestamps.sort_values().reset_index(drop=True)
        if ordered.empty:
            return work.iloc[0:0].copy()
        midpoint = ordered.iloc[len(ordered) // 2]
        mask = timestamps.le(midpoint) if stress == "first_half" else timestamps.gt(midpoint)
        return work.loc[mask].copy()
    return work


def build_candidates() -> tuple[pd.DataFrame, list[dict[str, Any]]]:
    frame, variants = worthwhile_variants.build_variants()
    by_id = {str(row["variant_id"]): row for row in variants}
    missing = [candidate for candidate in cfg.CANDIDATE_IDS if candidate not in by_id]
    if missing:
        raise RuntimeError(f"missing candidate variants: {missing}")
    candidates: list[dict[str, Any]] = []
    for rank, candidate_id in enumerate(cfg.CANDIDATE_IDS, start=1):
        row = dict(by_id[candidate_id])
        row["candidate_rank"] = rank
        row["source_run_id"] = cfg.SOURCE_RUN_ID
        candidates.append(row)
    return frame, candidates


def materialize_runtime_inputs(frame: pd.DataFrame, candidates: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    common_root = common_run_root(cfg.STAGE_NUMBER, cfg.RUN_ID)
    common_copies: list[dict[str, Any]] = []
    model_outputs: dict[str, dict[str, Any]] = {}
    for direction in sorted({str(row["direction"]) for row in candidates}):
        model_path = cfg.RUN_ROOT / "models" / f"{direction}_constant_score_table.csv"
        model_outputs[direction] = atlas_model.write_constant_score_table(model_path, direction)
        common_copies.append(copy_to_common(model_path, f"{common_root}/models/{model_path.name}", COMMON_FILES_ROOT_DEFAULT))

    stress_outputs: list[dict[str, Any]] = []
    skipped_empty_features: list[dict[str, Any]] = []
    for candidate in candidates:
        candidate_id = str(candidate["variant_id"])
        mask = worthwhile_variants.variant_mask(frame, candidate_id)
        for spec in _stress_specs():
            source_split = str(spec["source_split"])
            selected = frame.loc[frame["split"].astype(str).eq(source_split) & mask, ["timestamp", "split", *cfg.FEATURE_ORDER]].copy()
            selected = _apply_stress(selected, str(spec["stress"]))
            selected["variant_id"] = candidate_id
            selected["stress_id"] = str(spec["stress_id"])
            selected["max_hold_bars"] = int(spec["max_hold_bars"])
            output = cfg.RUN_ROOT / "features" / f"{candidate_id}_{spec['stress_id']}_features.csv"
            export = mt5.export_mt5_feature_matrix_csv(
                selected,
                cfg.FEATURE_ORDER,
                output,
                metadata_columns=("variant_id", "stress_id", "max_hold_bars"),
            )
            if selected.empty:
                export["tester_window_from_date"] = None
                export["tester_window_to_date"] = None
            else:
                export["tester_window_from_date"], export["tester_window_to_date"] = _window_dates(selected)
            export.update(
                {
                    "variant_id": candidate_id,
                    "family": candidate["family"],
                    "direction": candidate["direction"],
                    "candidate_rank": candidate["candidate_rank"],
                    "stress_id": str(spec["stress_id"]),
                    "stress": str(spec["stress"]),
                    "source_split": source_split,
                    "max_hold_bars": int(spec["max_hold_bars"]),
                    "source_row_count": int(len(selected)),
                }
            )
            stress_outputs.append(export)
            common_copies.append(copy_to_common(output, f"{common_root}/features/{output.name}", COMMON_FILES_ROOT_DEFAULT))
            if int(export["source_row_count"]) <= 0:
                skipped_empty_features.append({"variant_id": candidate_id, "stress_id": spec["stress_id"], "path": export["path"]})
    return {
        "common_root": common_root,
        "model_outputs": model_outputs,
        "stress_outputs": stress_outputs,
        "skipped_empty_features": skipped_empty_features,
        "common_copies": common_copies,
        "known_runtime_difference": "candidate masks and stress subsets are precomputed in Python and handed to MT5 by feature-row omission; this is runtime_probe, not native runtime authority.",
    }


def build_attempts(runtime_inputs: Mapping[str, Any], candidates: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    attempts: list[dict[str, Any]] = []
    common_root = str(runtime_inputs["common_root"])
    by_candidate = {str(row["variant_id"]): row for row in candidates}
    for feature in runtime_inputs["stress_outputs"]:
        if int(feature.get("source_row_count") or 0) <= 0:
            continue
        candidate_id = str(feature["variant_id"])
        candidate = by_candidate[candidate_id]
        direction = str(candidate["direction"])
        model_file = Path(str(runtime_inputs["model_outputs"][direction]["path"])).name
        feature_file = Path(str(feature["path"])).name
        stress_id = str(feature["stress_id"])
        attempts.append(
            attempt_payload(
                run_root=cfg.RUN_ROOT,
                run_id=cfg.RUN_ID,
                stage_number=cfg.STAGE_NUMBER,
                exploration_label=cfg.EXPLORATION_LABEL,
                attempt_name=f"tier_a_{candidate_id}_{stress_id}",
                tier=mt5.TIER_A,
                split=stress_id,
                model_path=f"{common_root}/models/{model_file}",
                model_id=f"{cfg.RUN_ID}_{candidate_id}_{direction}_constant",
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
                record_view_prefix=f"mt5_tier_a_candidate_{candidate_id}",
                max_hold_bars=int(feature["max_hold_bars"]),
                common_root=common_root,
                close_on_flat_signal=True,
            )
        )
    return attempts


def normalize_records(records: Sequence[Mapping[str, Any]], candidates: Sequence[Mapping[str, Any]], stress_outputs: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    by_candidate = {str(row["variant_id"]): row for row in candidates}
    candidate_ids = sorted(by_candidate, key=len, reverse=True)
    by_stress = {(str(row["variant_id"]), str(row["stress_id"])): row for row in stress_outputs}
    out: list[dict[str, Any]] = []
    for record in records:
        current = dict(record)
        view = str(current.get("record_view", ""))
        stress_id = str(current.get("split", ""))
        candidate_id = next((candidate for candidate in candidate_ids if candidate in view), "unknown")
        candidate = by_candidate.get(candidate_id, {})
        stress = by_stress.get((candidate_id, stress_id), {})
        current["source_variant_id"] = candidate_id
        current["candidate_rank"] = candidate.get("candidate_rank")
        current["source_family"] = candidate.get("family")
        current["state_direction"] = candidate.get("direction")
        current["stress_id"] = stress_id
        current["stress"] = stress.get("stress")
        current["max_hold_bars"] = stress.get("max_hold_bars")
        current["topic_read"] = "stage35_candidate_four_deep_dive_runtime_probe"
        metrics = dict(current.get("metrics", {})) if isinstance(current.get("metrics"), Mapping) else {}
        metrics["route_role"] = "tier_only_total"
        metrics["source_variant_id"] = candidate_id
        metrics["state_direction"] = candidate.get("direction")
        metrics["stress_id"] = stress_id
        metrics["stress"] = stress.get("stress")
        metrics["max_hold_bars"] = stress.get("max_hold_bars")
        current["route_role"] = "tier_only_total"
        current["metrics"] = metrics
        out.append(current)
    return out


def execute_or_block(prepared: Mapping[str, Any], args: argparse.Namespace, candidates: Sequence[Mapping[str, Any]], stress_outputs: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    if bool(args.reuse_existing_result):
        manifest = common.read_json(cfg.RUN_ROOT / "run_manifest.json")
        kpi_record = common.read_json(cfg.RUN_ROOT / "kpi_record.json")
        runtime_probe = manifest.get("runtime_probe", {}) if isinstance(manifest, Mapping) else {}
        return {
            **dict(prepared),
            "compile": runtime_probe.get("compile", {}),
            "execution_results": runtime_probe.get("execution_results", []),
            "strategy_tester_reports": runtime_probe.get("strategy_tester_reports", []),
            "mt5_kpi_records": normalize_records(kpi_record.get("mt5_kpi_records", []), candidates, stress_outputs),
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
    result["mt5_kpi_records"] = normalize_records(result.get("mt5_kpi_records", []), candidates, stress_outputs)
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


__all__ = [
    "METAEDITOR_PATH_DEFAULT",
    "TERMINAL_PATH_DEFAULT",
    "build_attempts",
    "build_candidates",
    "execute_or_block",
    "materialize_runtime_inputs",
    "normalize_records",
    "write_normalized_kpi",
]
