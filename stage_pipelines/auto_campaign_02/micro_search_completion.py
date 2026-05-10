from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any, Mapping, Sequence

import pandas as pd

from foundation.control_plane.ledger import io_path
from foundation.features.independent_alpha_campaign import (
    STAGE_TOPICS,
    apply_candidate_to_table,
    build_broad_candidate_grid,
    build_micro_candidate_grid,
    build_stage_model_context,
)
from stage_pipelines.auto_campaign_02.independent_runtime_probe import (
    BLOCKED_JUDGMENT,
    CAMPAIGN_ID,
    CAMPAIGN_PACKET_ROOT,
    FINAL_STAGE_BOUNDARY,
    actual_mt5_output_complete,
    build_arg_parser,
    build_common_table,
    build_mt5_candidate_summary,
    create_promotion_packet,
    dataframe_to_csv,
    evaluate_micro_search_gate,
    evaluate_promotion_candidate_gate,
    final_judgment,
    merge_results,
    packet_root,
    prepare_candidate_batch,
    run_one_stage,
    run_root,
    save_frame,
    stage_root,
    stage_validation_commands,
    update_campaign_progress,
    update_current_truth,
    write_campaign_open_packet,
    write_campaign_summary,
    write_ledgers,
    write_packet_files,
    write_run_files,
    write_stage_docs,
)


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(io_path(path).read_text(encoding="utf-8"))


def read_csv_dicts(path: Path) -> list[dict[str, Any]]:
    with io_path(path).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def dedupe_rows(rows: Sequence[Mapping[str, Any]], key_fields: Sequence[str]) -> list[dict[str, Any]]:
    ordered: dict[tuple[str, ...], dict[str, Any]] = {}
    for row in rows:
        key = tuple(str(row.get(field, "")) for field in key_fields)
        ordered[key] = dict(row)
    return list(ordered.values())


def completed_result_from_artifacts(stage_number: int) -> dict[str, Any]:
    topic = STAGE_TOPICS[stage_number]
    root = run_root(topic)
    kpi_record = read_json(root / "kpi_record.json")
    manifest = read_json(root / "run_manifest.json")
    handoff = read_json(root / "mt5/handoff_manifest.json")
    runtime_gate = read_json(packet_root(topic) / "runtime_evidence_gate.json")
    python_summary = read_csv_dicts(root / "tables/python_candidate_summary.csv")
    candidate_specs = read_csv_dicts(root / "tables/candidate_grid.csv")
    attempts = dedupe_rows(manifest.get("attempts", []), ("attempt_name",))
    kpi_records = dedupe_rows(kpi_record.get("mt5_kpi_records", []), ("record_view", "tier_scope", "split"))
    execution_results = dedupe_rows(runtime_gate.get("execution_results", []), ("attempt_name",))
    execution_by_name = {str(item.get("attempt_name")): dict(item) for item in execution_results}
    for attempt in attempts:
        attempt_name = str(attempt.get("attempt_name", ""))
        if not attempt_name:
            continue
        if attempt_name in execution_by_name:
            execution_by_name[attempt_name].setdefault("candidate_id", attempt.get("candidate_id", ""))
            execution_by_name[attempt_name].setdefault("candidate_token", attempt.get("candidate_token", ""))
            continue
        execution_by_name[attempt_name] = {
            "attempt_name": attempt_name,
            "candidate_id": attempt.get("candidate_id", ""),
            "candidate_token": attempt.get("candidate_token", ""),
            "split": attempt.get("split", ""),
            "status": "completed_from_existing_kpi_record",
        }
    return {
        "stage_id": topic.stage_id,
        "stage_number": topic.stage_number,
        "run_id": topic.run_id,
        "run_number": topic.run_number,
        "run_root": root,
        "attempts": attempts,
        "common_copies": handoff.get("common_copies", []),
        "execution_results": list(execution_by_name.values()),
        "strategy_tester_reports": runtime_gate.get("strategy_tester_reports", []),
        "mt5_kpi_records": kpi_records,
        "python_candidate_summary": python_summary,
        "candidate_specs": candidate_specs,
        "compile": runtime_gate.get("compile", {}),
        "external_verification_status": "completed" if runtime_gate.get("status") == "passed" else "blocked",
        "model_family": "single_discrete_signal_score_table",
        "feature_set_id": "campaign02_topic_specific_closed_bar_signal",
        "label_id": "label_v1_fwd12_m5_logret_train_q33_3class",
        "split_contract": "split_v1_calendar_train_20220901_20241231_val_20250101_20250930_oos_20251001_20260413",
        "stage_inheritance": "none_prior_stages_negative_memory_only",
    }


def artifacts_for_stage(topic, base_lineage: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return [
        *base_lineage,
        {"path": str((run_root(topic) / "models/topic_model_context.json").relative_to(Path.cwd())), "role": "model_training_manifest", "artifact_kind": "model artifact", "affects": "model candidate signal"},
        {"role": "candidate_grid", "path": str((run_root(topic) / "tables/candidate_grid.csv").relative_to(Path.cwd())).replace("\\", "/"), "artifact_kind": "candidate sweep table", "affects": "candidate signal"},
        {"role": "candidate_signal_table", "path": str((run_root(topic) / "tables/candidate_signal_table.parquet").relative_to(Path.cwd())).replace("\\", "/"), "artifact_kind": "intermediate", "affects": "candidate signal entry"},
        {"role": "mt5_handoff_manifest", "path": str((run_root(topic) / "mt5/handoff_manifest.json").relative_to(Path.cwd())).replace("\\", "/"), "artifact_kind": "MT5 handoff", "affects": "runtime"},
        {"role": "mt5_result_import_summary", "path": str((run_root(topic) / "mt5/mt5_result_import_summary.json").relative_to(Path.cwd())).replace("\\", "/"), "artifact_kind": "imported result", "affects": "KPI report"},
        {"role": "review_packet", "path": str((stage_root(topic) / f"03_reviews/{topic.run_id}_packet.md").relative_to(Path.cwd())).replace("\\", "/"), "artifact_kind": "report", "affects": "report-only context"},
    ]


def update_stage_after_micro(
    stage_number: int,
    common: pd.DataFrame,
    route_coverage: Mapping[str, Any],
    base_lineage: Sequence[Mapping[str, Any]],
    args: argparse.Namespace,
) -> dict[str, Any]:
    topic = STAGE_TOPICS[stage_number]
    context = build_stage_model_context(common, topic)
    broad_specs = build_broad_candidate_grid(topic)
    broad_result = completed_result_from_artifacts(stage_number)
    all_existing_rows = build_mt5_candidate_summary(
        topic,
        broad_result.get("mt5_kpi_records", []),
        broad_result.get("python_candidate_summary", []),
        broad_result.get("execution_results", []),
    )
    broad_rows = [row for row in all_existing_rows if str(row.get("candidate_id", "")).startswith("c")]
    micro_gate = evaluate_micro_search_gate(broad_rows)
    existing_micro = any(str(item.get("candidate_id", "")).startswith("m") for item in broad_result.get("candidate_specs", [])) or any(
        str(item.get("candidate_id", "")).startswith("m") for item in broad_result.get("attempts", [])
    )
    result = broad_result
    all_specs = list(broad_specs)
    broad_frames = {spec.candidate_id: apply_candidate_to_table(common, topic, spec, context) for spec in broad_specs}
    all_frames = dict(broad_frames)
    if micro_gate.get("status") == "passed":
        micro_specs = build_micro_candidate_grid(topic, str(micro_gate["best_candidate"]), broad_specs)
        all_specs.extend(micro_specs)
        if existing_micro:
            all_frames.update({spec.candidate_id: apply_candidate_to_table(common, topic, spec, context) for spec in micro_specs})
        else:
            micro_batch = prepare_candidate_batch(topic, micro_specs, common, context, Path(args.common_files_root))
            all_frames.update(micro_batch["frames"])
            micro_prepared = {**micro_batch, "candidate_specs": [spec.as_dict() for spec in micro_specs]}
            micro_result = run_one_micro_batch(topic, micro_prepared, route_coverage, args)
            result = merge_results(topic, broad_result, micro_result)
    save_frame(run_root(topic) / "tables/candidate_signal_table.parquet", pd.concat(all_frames.values(), ignore_index=True))
    dataframe_to_csv(run_root(topic) / "tables/candidate_grid.csv", [spec.as_dict() for spec in all_specs])
    mt5_rows = build_mt5_candidate_summary(topic, result.get("mt5_kpi_records", []), result.get("python_candidate_summary", []), result.get("execution_results", []))
    micro_gate = evaluate_micro_search_gate(mt5_rows)
    promotion_gate = evaluate_promotion_candidate_gate(mt5_rows)
    promotion_packet = create_promotion_packet(topic, promotion_gate, mt5_rows)
    judgment = final_judgment(result, promotion_gate, mt5_rows)
    result["judgment"] = judgment
    artifacts = artifacts_for_stage(topic, base_lineage)
    write_run_files(topic, result, mt5_rows, micro_gate, promotion_gate, promotion_packet, judgment, artifacts)
    ledger_payload = write_ledgers(topic, result, judgment, artifacts)
    write_stage_docs(topic, result, mt5_rows, micro_gate, promotion_gate, promotion_packet, judgment, artifacts)
    write_packet_files(topic, result, mt5_rows, micro_gate, promotion_gate, promotion_packet, judgment, ledger_payload, stage_validation_commands(topic))
    update_current_truth(topic, result, judgment, micro_gate, promotion_gate)
    best_val, _worst_val = best_by_split(mt5_rows, "validation_is")
    best_oos, _worst_oos = best_by_split(mt5_rows, "oos")
    return {
        "stage_number": topic.stage_number,
        "stage_id": topic.stage_id,
        "run_id": topic.run_id,
        "packet_id": topic.packet_id,
        "judgment": judgment,
        "mt5_attempt_count": len(result.get("attempts", [])),
        "mt5_kpi_record_count": len(result.get("mt5_kpi_records", [])),
        "micro_search_gate": micro_gate,
        "promotion_candidate_gate": promotion_gate,
        "promotion_candidate_packet": promotion_packet,
        "best_validation": best_val,
        "best_oos": best_oos,
        "run_root": str((run_root(topic)).relative_to(Path.cwd())).replace("\\", "/"),
        "packet_root": str((packet_root(topic)).relative_to(Path.cwd())).replace("\\", "/"),
        "actual_mt5_artifact_exists": actual_mt5_output_complete(result),
    }


def run_one_micro_batch(topic, prepared: Mapping[str, Any], route_coverage: Mapping[str, Any], args: argparse.Namespace) -> dict[str, Any]:
    from stage_pipelines.auto_campaign_02.independent_runtime_probe import execute_or_block

    return execute_or_block(topic, prepared, route_coverage, args)


def best_by_split(rows: Sequence[Mapping[str, Any]], split: str) -> tuple[Mapping[str, Any] | None, Mapping[str, Any] | None]:
    from stage_pipelines.auto_campaign_02.independent_runtime_probe import best_worst

    return best_worst(rows, split)


def build_arg_parser_for_completion() -> argparse.ArgumentParser:
    parser = build_arg_parser()
    parser.description = "Complete AUTO-CAMPAIGN-02 micro-search where corrected broad gates pass."
    parser.set_defaults(stages="43,44,45,46,47")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_arg_parser_for_completion().parse_args(argv)
    stage_numbers = [int(item.strip()) for item in str(args.stages).split(",") if item.strip()]
    write_campaign_open_packet()
    common, route_coverage, base_lineage = build_common_table()
    stage_results = []
    validation_commands = []
    for stage_number in stage_numbers:
        result = update_stage_after_micro(stage_number, common, route_coverage, base_lineage, args)
        stage_results.append(result)
        validation_commands.extend(stage_validation_commands(STAGE_TOPICS[stage_number]))
        update_campaign_progress(stage_results)
        if result.get("judgment") == BLOCKED_JUDGMENT:
            update_campaign_progress(stage_results, status="blocked", blocked_stage=stage_number)
            break
    summary = write_campaign_summary(stage_results, validation_commands)
    update_campaign_progress(stage_results, status=summary["campaign_judgment"])
    return 0 if not str(summary["campaign_judgment"]).startswith("campaign_blocked") else 2


if __name__ == "__main__":
    raise SystemExit(main())
