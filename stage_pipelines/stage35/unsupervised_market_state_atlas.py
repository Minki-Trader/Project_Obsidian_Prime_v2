from __future__ import annotations

import argparse
import json
from typing import Sequence

from stage_pipelines.stage35 import atlas_config as cfg
from stage_pipelines.stage35 import atlas_model, artifacts, common, mt5_probe


def build_prepared(atlas: dict, runtime_inputs: dict) -> dict:
    attempts = mt5_probe.build_attempts(runtime_inputs, atlas["selections"])
    return {
        "stage_id": cfg.STAGE_ID,
        "stage_number": cfg.STAGE_NUMBER,
        "run_id": cfg.RUN_ID,
        "run_number": cfg.RUN_NUMBER,
        "source_run_id": "stage35_new_topic_no_stage34_inheritance",
        "run_root": cfg.RUN_ROOT,
        "attempts": attempts,
        "common_copies": runtime_inputs["common_copies"],
        "route_coverage": {},
        "model_family": cfg.MODEL_FAMILY,
        "feature_set_id": cfg.FEATURE_SET_ID,
        "label_id": cfg.LABEL_ID,
        "split_contract": cfg.SPLIT_CONTRACT,
        "stage_inheritance": "topic_pivot_from_stage34_not_continuation",
        "completion_goal": "open_stage35_select_5_non_overlapping_unsupervised_atlas_topics_and_attempt_mt5_runtime_probe",
    }


def run(args: argparse.Namespace) -> dict:
    atlas = atlas_model.build_atlas()
    runtime_inputs = mt5_probe.materialize_runtime_inputs(atlas)
    prepared = build_prepared(atlas, runtime_inputs)
    result = mt5_probe.execute_or_block(prepared, args, atlas["selections"])
    summary = artifacts.build_summary(
        created_at=common.utc_now(),
        branch=common.active_branch(),
        atlas=atlas,
        runtime_inputs=runtime_inputs,
        result=result,
    )
    artifacts.write_run_files(summary, result, atlas)
    kpi = mt5_probe.write_normalized_kpi()
    summary["kpi_management"] = kpi
    summary["ledger_materialization"] = artifacts.materialize_ledgers(summary)
    common.write_json(cfg.RESULT_ROOT / "aggregate_summary.json", summary)
    common.write_json(cfg.PACKET_ROOT / "aggregate_summary.json", summary)
    artifacts.write_stage_docs(summary)
    if not args.skip_state_update:
        artifacts.update_workspace_state(summary)
        artifacts.prepend_context(summary)
        artifacts.append_changelog(summary)
    return summary


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Open Stage35 and run unsupervised market state atlas MT5 probe.")
    parser.add_argument("--terminal-path", default=str(mt5_probe.TERMINAL_PATH_DEFAULT))
    parser.add_argument("--metaeditor-path", default=str(mt5_probe.METAEDITOR_PATH_DEFAULT))
    parser.add_argument("--timeout-seconds", type=int, default=900)
    parser.add_argument("--materialize-only", action="store_true")
    parser.add_argument("--reuse-existing-result", action="store_true")
    parser.add_argument("--skip-state-update", action="store_true")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    summary = run(build_arg_parser().parse_args(argv))
    print(
        json.dumps(
            {
                "status": summary["status"],
                "judgment": summary["judgment"],
                "external_verification_status": summary["external_verification_status"],
                "mt5_attempt_count": summary["mt5_attempt_count"],
                "mt5_kpi_record_count": summary["mt5_kpi_record_count"],
                "report": summary["output_paths"]["report"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
