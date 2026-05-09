from __future__ import annotations

import argparse
import json
from typing import Any, Mapping, Sequence

from stage_pipelines.stage35 import candidate_artifacts as artifacts
from stage_pipelines.stage35 import candidate_config as cfg
from stage_pipelines.stage35 import candidate_mt5, common


RUN_NUMBER = cfg.RUN_NUMBER
CANDIDATE_IDS = cfg.CANDIDATE_IDS


def build_prepared(runtime_inputs: Mapping[str, Any], candidates: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    attempts = candidate_mt5.build_attempts(runtime_inputs, candidates)
    return {
        "stage_id": cfg.STAGE_ID,
        "stage_number": cfg.STAGE_NUMBER,
        "run_id": cfg.RUN_ID,
        "run_number": cfg.RUN_NUMBER,
        "source_run_id": cfg.SOURCE_RUN_ID,
        "source_packet_id": cfg.SOURCE_PACKET_ID,
        "run_root": cfg.RUN_ROOT,
        "attempts": attempts,
        "common_copies": runtime_inputs["common_copies"],
        "route_coverage": {},
        "model_family": cfg.MODEL_FAMILY,
        "feature_set_id": cfg.FEATURE_SET_ID,
        "label_id": cfg.LABEL_ID,
        "split_contract": cfg.SPLIT_CONTRACT,
        "stage_inheritance": "follow_up_inside_stage35_not_stage34_continuation",
        "completion_goal": "stress_test_the_four_run29b_both_positive_stage35_candidates_with_mt5",
    }


def run(args: argparse.Namespace) -> dict[str, Any]:
    frame, candidates = candidate_mt5.build_candidates()
    runtime_inputs = candidate_mt5.materialize_runtime_inputs(frame, candidates)
    prepared = build_prepared(runtime_inputs, candidates)
    result = candidate_mt5.execute_or_block(prepared, args, candidates, runtime_inputs["stress_outputs"])
    summary = artifacts.build_summary(
        created_at=common.utc_now(),
        branch=common.active_branch(),
        candidates=candidates,
        runtime_inputs=runtime_inputs,
        result=result,
    )
    artifacts.write_run_files(summary, result)
    kpi = candidate_mt5.write_normalized_kpi()
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
    parser = argparse.ArgumentParser(description="Run Stage35 RUN29C candidate four deep-dive MT5 probe.")
    parser.add_argument("--terminal-path", default=str(candidate_mt5.TERMINAL_PATH_DEFAULT))
    parser.add_argument("--metaeditor-path", default=str(candidate_mt5.METAEDITOR_PATH_DEFAULT))
    parser.add_argument("--timeout-seconds", type=int, default=1800)
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
                "candidate_count": summary["candidate_count"],
                "planned_mt5_attempt_count": summary["planned_mt5_attempt_count"],
                "mt5_attempt_count": summary["mt5_attempt_count"],
                "mt5_kpi_record_count": summary["mt5_kpi_record_count"],
                "normalized_records": summary.get("kpi_management", {}).get("normalized_records"),
                "parser_errors": summary.get("kpi_management", {}).get("parser_errors"),
                "report": summary["output_paths"]["report"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
