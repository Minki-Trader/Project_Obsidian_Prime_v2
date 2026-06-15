from __future__ import annotations

import argparse
import csv
import json
import math
import os
import shutil
import subprocess
import sys
import time
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import joblib
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.alpha import scout_runner as scout  # noqa: E402
from foundation.control_plane.ledger import io_path, json_ready, path_exists  # noqa: E402
from foundation.models.onnx_bridge import ordered_hash, ordered_sklearn_probabilities  # noqa: E402
from foundation.mt5 import runtime_support as mt5  # noqa: E402
from stage_pipelines.stage_frontier_04 import frontier04d_trainable_path_label_onnx_probe as f04d  # noqa: E402
from stage_pipelines.stage_frontier_07 import frontier07b_adverse_excursion_risk_label_proxy_scout as f07b  # noqa: E402


BACKFILL_RUN_SUFFIX = "runtime_probe_backfill_v1"
PROJECT_LEDGER = Path("docs/registers/alpha_run_ledger.csv")
PROJECT_MANIFEST = Path("docs/agent_control/runtime_probe_backfill/frontier_runtime_probe_backfill_manifest.csv")
PROJECT_SUMMARY = Path("docs/agent_control/runtime_probe_backfill/frontier_runtime_probe_backfill_summary.md")
GROK_REVIEW = Path(
    "docs/agent_control/grok_reviews/2026-06-15_frontier_runtime_probe_backfill_pre_mt5/small_review/clean_output.md"
)

DEFAULT_PORTABLE_ROOT = Path("C:/Users/awdse/AppData/Local/ObsidianPrime/mt5_portable_run329E")
DEFAULT_TERMINAL = DEFAULT_PORTABLE_ROOT / "terminal64.exe"
DEFAULT_METAEDITOR = DEFAULT_PORTABLE_ROOT / "MetaEditor64.exe"
DEFAULT_COMMON_FILES = DEFAULT_PORTABLE_ROOT / "Common" / "Files"
DEFAULT_TESTER_PROFILE_ROOT = DEFAULT_PORTABLE_ROOT / "MQL5" / "Profiles" / "Tester"
DEFAULT_TERMINAL_DATA_ROOT = DEFAULT_PORTABLE_ROOT
EA_SOURCE = ROOT / mt5.EA_SOURCE_PATH
EA_BINARY = ROOT / "foundation" / "mt5" / "ObsidianPrimeV2_RuntimeProbeEA.ex5"
PORTABLE_EA_BINARY = (
    DEFAULT_PORTABLE_ROOT
    / "MQL5"
    / "Experts"
    / "Project_Obsidian_Prime_v2"
    / "foundation"
    / "mt5"
    / "ObsidianPrimeV2_RuntimeProbeEA.ex5"
)

CLAIM_BOUNDARY = (
    "runtime_probe_backfill_observation_only_no_completion_no_baseline_no_promotion_"
    "no_runtime_authority_no_live_readiness_no_goal_achieve"
)


@dataclass(frozen=True)
class CandidateSpec:
    stage_num: int
    stage_id: str
    parent_run_id: str
    source_run_id: str
    candidate_id: str
    model_id: str
    model_path: Path
    onnx_path: Path
    decision_mode: str
    short_threshold: float
    long_threshold: float
    min_margin: float
    max_hold_bars: int
    cooldown_bars: int
    source_contract: str
    source_note: str

    @property
    def run_number(self) -> str:
        return f"frontier{self.stage_num:02d}Z"

    @property
    def run_id(self) -> str:
        return f"frontier{self.stage_num:02d}Z_{BACKFILL_RUN_SUFFIX}"

    @property
    def run_root(self) -> Path:
        return Path("stages") / self.stage_id / "02_runs" / self.run_id

    @property
    def mt5_root(self) -> Path:
        return self.run_root / "mt5"

    @property
    def feature_root(self) -> Path:
        return self.run_root / "feature_matrices"

    @property
    def telemetry_copy_root(self) -> Path:
        return self.run_root / "runtime_telemetry"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Retroactive frontier MT5 runtime probe backfill.")
    parser.add_argument("--terminal-path", default=str(DEFAULT_TERMINAL))
    parser.add_argument("--metaeditor-path", default=str(DEFAULT_METAEDITOR))
    parser.add_argument("--common-files-root", default=str(DEFAULT_COMMON_FILES))
    parser.add_argument("--tester-profile-root", default=str(DEFAULT_TESTER_PROFILE_ROOT))
    parser.add_argument("--terminal-data-root", default=str(DEFAULT_TERMINAL_DATA_ROOT))
    parser.add_argument("--timeout-seconds", type=int, default=900)
    parser.add_argument("--wait-timeout-seconds", type=int, default=240)
    parser.add_argument("--stages", default="")
    parser.add_argument("--preflight-only", action="store_true")
    parser.add_argument("--materialize-only", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    selected = parse_stage_filter(args.stages)
    created_at = utc_now()
    full, _raw, source_integrity = f07b.load_training_packet()
    feature_order = f04d.read_feature_order()
    feature_hash = ordered_hash(feature_order)

    discovery = discover_all_candidates(selected)
    executable_specs: list[CandidateSpec] = []
    manifest_rows: list[dict[str, Any]] = []
    for stage_num in range(1, 50):
        if selected and stage_num not in selected:
            continue
        stage_dir = stage_dir_for_num(stage_num)
        if stage_dir is None:
            continue
        entry = discovery.get(stage_num, {"classification": "invalid_setup_no_runtime_material"})
        spec = entry.get("candidate")
        if isinstance(spec, CandidateSpec):
            preflight = preflight_candidate(spec, feature_order, feature_hash)
            manifest_rows.append(manifest_row(stage_num, spec.stage_id, entry["classification"], preflight, spec))
            if preflight["status"] == "executable_candidate_after_preflight":
                executable_specs.append(spec)
            elif args.preflight_only or not has_backfill_status(spec.stage_id):
                write_stage_status(stage_num, spec.stage_id, created_at, entry["classification"], preflight, spec, [])
                upsert_backfill_status_ledger(stage_num, spec.stage_id, created_at, entry["classification"], preflight, spec, [])
        else:
            preflight = {
                "status": entry.get("classification", "invalid_setup_no_runtime_material"),
                "reason": entry.get("reason", "no recoverable runtime candidate"),
                "checks": entry.get("checks", {}),
            }
            manifest_rows.append(manifest_row(stage_num, stage_dir.name, preflight["status"], preflight, None))
            if args.preflight_only or not has_backfill_status(stage_dir.name):
                write_stage_status(stage_num, stage_dir.name, created_at, preflight["status"], preflight, None, [])
                upsert_backfill_status_ledger(stage_num, stage_dir.name, created_at, preflight["status"], preflight, None, [])

    write_csv(PROJECT_MANIFEST, manifest_rows)
    if args.preflight_only:
        write_project_summary(created_at, manifest_rows, preflight_only=True)
        print(json.dumps(json_ready({"status": "preflight_completed", "manifest": PROJECT_MANIFEST.as_posix()}), ensure_ascii=False, indent=2))
        return 0

    compile_payload = compile_runtime_ea(Path(args.metaeditor_path))
    terminal_probe = terminal_processes()
    all_run_summaries: list[dict[str, Any]] = []
    for spec in executable_specs:
        run_summary = execute_spec(
            spec=spec,
            args=args,
            created_at=created_at,
            full=full,
            feature_order=feature_order,
            feature_hash=feature_hash,
            source_integrity=source_integrity,
            compile_payload=compile_payload,
            terminal_probe=terminal_probe,
        )
        all_run_summaries.append(run_summary)
        preflight = {
            "status": run_summary["classification"],
            "reason": run_summary.get("reason", ""),
            "checks": run_summary.get("preflight_checks", {}),
        }
        write_stage_status(spec.stage_num, spec.stage_id, created_at, run_summary["classification"], preflight, spec, run_summary["runtime_rows"])
        upsert_backfill_status_ledger(
            spec.stage_num,
            spec.stage_id,
            created_at,
            run_summary["classification"],
            preflight,
            spec,
            run_summary["runtime_rows"],
        )

    write_project_summary(created_at, manifest_rows, preflight_only=False, run_summaries=all_run_summaries)
    print(
        json.dumps(
            json_ready(
                {
                    "status": "completed_with_records",
                    "executable_count": len(executable_specs),
                    "run_count": len(all_run_summaries),
                    "manifest": PROJECT_MANIFEST.as_posix(),
                    "summary": PROJECT_SUMMARY.as_posix(),
                }
            ),
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


def parse_stage_filter(raw: str) -> set[int]:
    values: set[int] = set()
    for piece in raw.split(","):
        piece = piece.strip()
        if not piece:
            continue
        if "-" in piece:
            lo, hi = piece.split("-", 1)
            values.update(range(int(lo), int(hi) + 1))
        else:
            values.add(int(piece))
    return values


def discover_all_candidates(selected: set[int]) -> dict[int, dict[str, Any]]:
    out: dict[int, dict[str, Any]] = {}
    for stage_num in range(1, 50):
        if selected and stage_num not in selected:
            continue
        stage = stage_dir_for_num(stage_num)
        if stage is None:
            continue
        if stage_num == 1:
            out[stage_num] = {
                "classification": "out_of_scope_by_claim",
                "reason": "archive/governance stage without model runtime material",
            }
            continue
        if stage_num in (16, 17) and existing_mt5_reports(stage):
            out[stage_num] = {
                "classification": "completed_existing_verify_only",
                "reason": "existing MT5 runtime probe reports found",
                "checks": {"report_count": len(existing_mt5_reports(stage))},
            }
            continue
        spec = discover_candidate(stage_num, stage)
        if spec is None:
            out[stage_num] = classify_no_candidate(stage_num, stage)
        else:
            out[stage_num] = {"classification": "candidate_found_pending_preflight", "candidate": spec}
    return out


def discover_candidate(stage_num: int, stage: Path) -> CandidateSpec | None:
    if stage_num == 2:
        return discover_f02(stage_num, stage)
    if stage_num == 3:
        return discover_f03(stage_num, stage)
    if stage_num == 4:
        return discover_f04(stage_num, stage)
    if stage_num == 5:
        return discover_f05(stage_num, stage)
    if stage_num == 6:
        return discover_f06(stage_num, stage)
    if 7 <= stage_num <= 15:
        return discover_best_row_candidate(stage_num, stage)
    if stage_num in (18, 19):
        return discover_best_row_candidate(stage_num, stage)
    return None


def classify_no_candidate(stage_num: int, stage: Path) -> dict[str, Any]:
    token = runtime_blocker_token(stage)
    onnx_count = len(list_files(stage, ".onnx"))
    if token:
        return {
            "classification": "invalid_setup_no_runtime_material",
            "reason": token,
            "checks": {"onnx_count": onnx_count, "closeout_blocker_token": token},
        }
    if onnx_count:
        return {
            "classification": "missing_artifact_blocked",
            "reason": "ONNX exists but no unambiguous EA-compatible candidate contract was recovered",
            "checks": {"onnx_count": onnx_count},
        }
    return {
        "classification": "invalid_setup_no_runtime_material",
        "reason": "no ONNX, joblib, or runtime handoff candidate recovered",
        "checks": {"onnx_count": 0},
    }


def discover_f02(stage_num: int, stage: Path) -> CandidateSpec | None:
    manifest = stage / "02_runs/frontier02C_trainable_onnx_seed_surface_design_v1/run_manifest.json"
    if not path_exists(manifest):
        return None
    payload = read_json(manifest)
    row = payload.get("best_validation_rank", {})
    model_id = str(row.get("candidate_model_id", ""))
    if not model_id:
        return None
    return spec_from_paths(
        stage_num,
        stage,
        parent_run_id="frontier02F_stage_closeout_preserved_clue_negative_memory_v1",
        source_run_id="frontier02C_trainable_onnx_seed_surface_design_v1",
        candidate_id=str(row.get("candidate_id", model_id)),
        model_id=model_id,
        model_path=stage / f"02_runs/frontier02C_trainable_onnx_seed_surface_design_v1/models/{model_id}.pkl",
        onnx_path=stage / f"02_runs/frontier02C_trainable_onnx_seed_surface_design_v1/models/{model_id}.onnx",
        decision_mode="threshold_margin",
        short_threshold=float(row.get("probability_threshold", 0.34)),
        long_threshold=float(row.get("probability_threshold", 0.34)),
        min_margin=float(row.get("probability_margin", 0.0)),
        max_hold_bars=int(row.get("hold_bars", 12) or 12),
        cooldown_bars=int(row.get("cooldown_bars", 0) or 0),
        source_contract="probability_threshold_margin",
        source_note="F02C preserved ONNX seed surface",
    )


def discover_f03(stage_num: int, stage: Path) -> CandidateSpec | None:
    manifest = stage / "02_runs/frontier03E_bounded_two_teacher_density_repair_v1/run_manifest.json"
    if not path_exists(manifest):
        return None
    payload = read_json(manifest)
    model_id = str(payload.get("best_model_id", ""))
    table = payload.get("model_table", [])
    model_row = next((row for row in table if str(row.get("candidate_model_id")) == model_id), {})
    onnx_path = model_row.get("onnx_path")
    model_path = model_row.get("model_path")
    if not model_id or not onnx_path:
        return None
    return spec_from_paths(
        stage_num,
        stage,
        parent_run_id="frontier03G_stage_closeout_v1",
        source_run_id="frontier03E_bounded_two_teacher_density_repair_v1",
        candidate_id=str(payload.get("best_candidate_id", model_id)),
        model_id=model_id,
        model_path=Path(str(model_path)) if model_path else Path(str(onnx_path)).with_suffix(".pkl"),
        onnx_path=Path(str(onnx_path)),
        decision_mode="threshold_margin",
        short_threshold=float(payload.get("best_probability_threshold", 0.4)),
        long_threshold=float(payload.get("best_probability_threshold", 0.4)),
        min_margin=float(payload.get("best_probability_margin", 0.04)),
        max_hold_bars=12,
        cooldown_bars=int(payload.get("best_cooldown_bars", 0) or 0),
        source_contract="probability_threshold_margin",
        source_note="F03E preserved two-teacher repair clue",
    )


def discover_f04(stage_num: int, stage: Path) -> CandidateSpec | None:
    manifest = stage / "02_runs/frontier04D_trainable_path_label_onnx_probe_v1/run_manifest.json"
    if not path_exists(manifest):
        return None
    payload = read_json(manifest)
    model_id = str(payload.get("best_model_id", ""))
    model_row = payload.get("best_model_row", {})
    return spec_from_paths(
        stage_num,
        stage,
        parent_run_id="frontier04E_stage_closeout_v1",
        source_run_id="frontier04D_trainable_path_label_onnx_probe_v1",
        candidate_id=model_id,
        model_id=model_id,
        model_path=stage / f"02_runs/frontier04D_trainable_path_label_onnx_probe_v1/models/{model_id}.joblib",
        onnx_path=stage / f"02_runs/frontier04D_trainable_path_label_onnx_probe_v1/models/{model_id}.onnx",
        decision_mode="argmax",
        short_threshold=0.0,
        long_threshold=0.0,
        min_margin=0.0,
        max_hold_bars=int(model_row.get("hold_bars", 12) or 12),
        cooldown_bars=0,
        source_contract="argmax_only_no_threshold",
        source_note="F04D best trainable path-label model",
    )


def discover_f05(stage_num: int, stage: Path) -> CandidateSpec | None:
    manifest = stage / "02_runs/frontier05C_stage_closeout_v1/run_manifest.json"
    if not path_exists(manifest):
        return None
    payload = read_json(manifest)
    row = payload.get("best_reference_row", {})
    model_id = str(row.get("model_id", ""))
    if not model_id:
        return None
    return spec_from_paths(
        stage_num,
        stage,
        parent_run_id="frontier05C_stage_closeout_v1",
        source_run_id="frontier05B_closed_bar_path_precursor_feature_scout_v1",
        candidate_id=f"frontier05_reference_v2_only__{model_id}",
        model_id=model_id,
        model_path=stage / f"02_runs/frontier05B_closed_bar_path_precursor_feature_scout_v1/models/v2_only/{model_id}.joblib",
        onnx_path=stage / f"02_runs/frontier05B_closed_bar_path_precursor_feature_scout_v1/models/v2_only/{model_id}.onnx",
        decision_mode="argmax",
        short_threshold=0.0,
        long_threshold=0.0,
        min_margin=0.0,
        max_hold_bars=12,
        cooldown_bars=0,
        source_contract="argmax_reference_surface",
        source_note="F05 closeout reference model, base v2 feature order",
    )


def discover_f06(stage_num: int, stage: Path) -> CandidateSpec | None:
    manifest = stage / "02_runs/frontier06C_stage_closeout_v1/run_manifest.json"
    if not path_exists(manifest):
        return None
    payload = read_json(manifest)
    row = payload.get("best_rule_row", {})
    model_id = str(row.get("model_id", ""))
    score_threshold = float(row.get("score_threshold", 0.0) or 0.0)
    if not model_id:
        return None
    return spec_from_paths(
        stage_num,
        stage,
        parent_run_id="frontier06C_stage_closeout_v1",
        source_run_id="frontier06B_selective_probability_abstention_signal_scout_v1",
        candidate_id=str(row.get("rule_id", model_id)),
        model_id=model_id,
        model_path=stage / f"02_runs/frontier06B_selective_probability_abstention_signal_scout_v1/models/{model_id}.joblib",
        onnx_path=stage / f"02_runs/frontier06B_selective_probability_abstention_signal_scout_v1/models/{model_id}.onnx",
        decision_mode="edge_margin",
        short_threshold=0.0,
        long_threshold=0.0,
        min_margin=score_threshold,
        max_hold_bars=12,
        cooldown_bars=0,
        source_contract="directional_margin_score_threshold_mapped_to_edge_margin",
        source_note="F06 score threshold mapped to RuntimeProbeEA edge_margin mode",
    )


def discover_best_row_candidate(stage_num: int, stage: Path) -> CandidateSpec | None:
    row_payload = latest_best_row_payload(stage)
    if row_payload is None:
        return None
    path, row = row_payload
    contract = str(row.get("signal_contract", ""))
    if stage_num == 18 and "lifecycle_exit" in contract:
        return None
    model_id = str(row.get("model_instance_id") or row.get("best_model_id") or row.get("model_id") or "")
    if not model_id:
        return None
    onnx_path = row.get("onnx_path") or row.get("source_onnx")
    model_path = row.get("joblib_path") or row.get("model_path") or row.get("source_model")
    if not onnx_path:
        matches = exact_file_by_stem(stage, model_id, ".onnx")
        if len(matches) == 1:
            onnx_path = matches[0].as_posix()
    if not model_path:
        matches = exact_file_by_stem(stage, model_id, ".joblib") + exact_file_by_stem(stage, model_id, ".pkl")
        if len(matches) == 1:
            model_path = matches[0].as_posix()
    if not onnx_path or not model_path:
        return None
    decision_mode = "argmax"
    short_threshold = 0.0
    long_threshold = 0.0
    min_margin = 0.0
    if "edge_margin" in contract:
        decision_mode = "edge_margin"
        min_margin = float(row.get("threshold_value", 0.0) or 0.0)
    if "score_threshold" in contract:
        return None
    max_hold = int(row.get("hold_bars", 12) or 12)
    target_id = str(row.get("target_id", ""))
    parsed_hold = parse_hold_bars(target_id)
    if parsed_hold:
        max_hold = parsed_hold
    return spec_from_paths(
        stage_num,
        stage,
        parent_run_id=parent_run_id_from_stage(stage),
        source_run_id=path.parent.name,
        candidate_id=str(row.get("candidate_id") or model_id),
        model_id=model_id,
        model_path=Path(str(model_path)),
        onnx_path=Path(str(onnx_path)),
        decision_mode=decision_mode,
        short_threshold=short_threshold,
        long_threshold=long_threshold,
        min_margin=min_margin,
        max_hold_bars=max_hold,
        cooldown_bars=int(row.get("cooldown_bars", 0) or 0),
        source_contract=contract or decision_mode,
        source_note=f"best_candidate_row from {path.as_posix()}",
    )


def spec_from_paths(
    stage_num: int,
    stage: Path,
    *,
    parent_run_id: str,
    source_run_id: str,
    candidate_id: str,
    model_id: str,
    model_path: Path,
    onnx_path: Path,
    decision_mode: str,
    short_threshold: float,
    long_threshold: float,
    min_margin: float,
    max_hold_bars: int,
    cooldown_bars: int,
    source_contract: str,
    source_note: str,
) -> CandidateSpec:
    return CandidateSpec(
        stage_num=stage_num,
        stage_id=stage.name,
        parent_run_id=parent_run_id,
        source_run_id=source_run_id,
        candidate_id=candidate_id,
        model_id=model_id,
        model_path=to_repo_path(model_path),
        onnx_path=to_repo_path(onnx_path),
        decision_mode=decision_mode,
        short_threshold=float(short_threshold),
        long_threshold=float(long_threshold),
        min_margin=float(min_margin),
        max_hold_bars=int(max_hold_bars),
        cooldown_bars=int(cooldown_bars),
        source_contract=source_contract,
        source_note=source_note,
    )


def preflight_candidate(spec: CandidateSpec, feature_order: Sequence[str], feature_hash: str) -> dict[str, Any]:
    checks: dict[str, Any] = {
        "onnx_exists": path_exists(ROOT / spec.onnx_path),
        "model_exists": path_exists(ROOT / spec.model_path),
        "feature_order_hash": feature_hash,
        "feature_count": len(feature_order),
        "decision_mode": spec.decision_mode,
        "source_contract": spec.source_contract,
        "closeout_blocker_token": runtime_blocker_token(Path("stages") / spec.stage_id),
    }
    if spec.stage_num in (18, 19) and checks["closeout_blocker_token"]:
        return {"status": "invalid_setup_no_runtime_material", "reason": checks["closeout_blocker_token"], "checks": checks}
    if not checks["onnx_exists"] or not checks["model_exists"]:
        return {"status": "missing_artifact_blocked", "reason": "model or ONNX artifact missing", "checks": checks}
    if spec.decision_mode not in {"argmax", "threshold_margin", "edge_margin"}:
        return {"status": "invalid_setup_unsupported_signal_contract", "reason": "decision mode not supported by RuntimeProbeEA", "checks": checks}
    if spec.min_margin < 0.0:
        return {"status": "invalid_setup_unsupported_signal_contract", "reason": "negative margin/score threshold is not EA-compatible", "checks": checks}
    try:
        model = joblib.load(io_path(ROOT / spec.model_path))
        n_features = int(getattr(model, "n_features_in_", len(feature_order)))
        checks["model_n_features_in"] = n_features
    except Exception as exc:
        return {"status": "blocked_preflight_model_load_failed", "reason": str(exc), "checks": checks}
    if int(checks["model_n_features_in"]) != len(feature_order):
        return {
            "status": "invalid_setup_feature_order_mismatch",
            "reason": "model feature count does not match canonical runtime feature order",
            "checks": checks,
        }
    return {"status": "executable_candidate_after_preflight", "reason": "all preflight checks passed", "checks": checks}


def execute_spec(
    *,
    spec: CandidateSpec,
    args: argparse.Namespace,
    created_at: str,
    full: pd.DataFrame,
    feature_order: Sequence[str],
    feature_hash: str,
    source_integrity: Mapping[str, Any],
    compile_payload: Mapping[str, Any],
    terminal_probe: Mapping[str, Any],
) -> dict[str, Any]:
    ensure_run_dirs(spec)
    model = joblib.load(io_path(ROOT / spec.model_path))
    split_payload = build_split_payload(spec, full, feature_order, model)
    attempts = materialize_attempts(spec, split_payload, feature_order, feature_hash, Path(args.common_files_root))
    write_json(spec.run_root / "source_truth_snapshot.json", source_snapshot(spec, source_integrity, split_payload))
    write_json(spec.mt5_root / "mt5_compile_result.json", compile_payload)
    write_json(spec.run_root / "terminal_process_audit.json", terminal_probe)
    write_csv(spec.run_root / "mt5_runtime_probe_attempt_package.csv", flatten_attempt_rows(attempts))

    execution_results: list[dict[str, Any]] = []
    report_records: list[dict[str, Any]] = []
    if args.materialize_only:
        for attempt in attempts:
            execution_results.append(blocked_result(spec, attempt, "not_run_materialize_only"))
    else:
        compile_status = (compile_payload.get("compile") or {}).get("status")
        can_run = compile_status == "completed" or path_exists(PORTABLE_EA_BINARY)
        if not can_run:
            for attempt in attempts:
                execution_results.append(blocked_result(spec, attempt, "compile_blocked_and_no_portable_ex5_fallback"))
        elif terminal_probe.get("status") != "no_terminal64_process":
            for attempt in attempts:
                execution_results.append(blocked_result(spec, attempt, "target_portable_terminal_already_running"))
        else:
            for attempt in attempts:
                remove_runtime_outputs(Path(args.common_files_root), attempt)
                mt5.remove_existing_mt5_report_artifacts(Path(args.terminal_data_root), attempt, run_id=spec.run_id)
                try:
                    tester_result = mt5.run_mt5_tester(
                        Path(args.terminal_path),
                        ROOT / str(attempt["ini"]["path"]),
                        set_path=ROOT / str(attempt["set"]["path"]),
                        tester_profile_set_path=Path(args.tester_profile_root) / mt5.EA_TESTER_SET_NAME,
                        tester_profile_ini_path=Path(args.tester_profile_root) / str(attempt["ini_name"]),
                        timeout_seconds=int(args.timeout_seconds),
                        terminal_extra_args=["/portable"],
                    )
                except subprocess.TimeoutExpired as exc:
                    tester_result = {
                        "status": "blocked",
                        "command": exc.cmd,
                        "returncode": None,
                        "stdout": tail_text(exc.stdout),
                        "stderr": tail_text(exc.stderr),
                        "blocker": "terminal_timeout",
                    }
                runtime_outputs = mt5.wait_for_mt5_runtime_outputs(
                    Path(args.common_files_root),
                    attempt,
                    timeout_seconds=int(args.wait_timeout_seconds),
                    poll_seconds=2.0,
                )
                if runtime_outputs.get("status") != "completed":
                    tester_result["status"] = "blocked"
                    tester_result.setdefault("blocker", "runtime_outputs_missing_or_init_failed")
                result = {
                    **tester_result,
                    "runtime_outputs": runtime_outputs,
                    "attempt_name": attempt["attempt_name"],
                    "tier": attempt["tier"],
                    "split": attempt["split"],
                    "record_view_prefix": attempt["record_view_prefix"],
                    "attempt_role": attempt["attempt_role"],
                    "candidate_id": spec.candidate_id,
                    "model_id": spec.model_id,
                    "ini_path": attempt["ini"]["path"],
                    "set_path": attempt["set"]["path"],
                    "common_model_path": attempt["common_model_path"],
                    "common_feature_matrix_path": attempt["common_feature_matrix_path"],
                }
                write_json(spec.mt5_root / f"{attempt['attempt_name']}_tester_execution.json", result)
                execution_results.append(result)
            report_records = mt5.collect_mt5_strategy_report_artifacts(
                terminal_data_root=Path(args.terminal_data_root),
                run_output_root=spec.run_root,
                attempts=attempts,
                run_id=spec.run_id,
            )
            mt5.attach_mt5_report_metrics(execution_results, report_records)

    copied_runtime = copy_runtime_outputs(Path(args.common_files_root), spec, attempts)
    execution_payload = {
        "compile_payload": compile_payload,
        "terminal_probe": terminal_probe,
        "execution_results": execution_results,
        "report_records": report_records,
        "copied_runtime_outputs": copied_runtime,
        "created_at_utc": created_at,
    }
    write_json(spec.run_root / "mt5_execution_result.json", execution_payload)
    write_json(spec.run_root / "strategy_tester_report_records.json", report_records)
    runtime_rows = build_runtime_summary_rows(spec, attempts, execution_payload, split_payload)
    classification = "runtime_probe_backfill_observation_no_authority"
    if not any(row.get("runtime_status") == "completed" and row.get("report_status") == "completed" for row in runtime_rows):
        classification = "blocked_attempt_failed"
    final = {
        "run_id": spec.run_id,
        "stage_id": spec.stage_id,
        "status": classification,
        "judgment": "runtime_probe_observation(런타임 탐침 관찰)" if classification != "blocked_attempt_failed" else "blocked_attempt_failed(시도 실패 차단)",
        "candidate": candidate_payload(spec),
        "runtime_rows": runtime_rows,
        "claim_boundary": claim_boundary_payload(),
        "created_at_utc": created_at,
    }
    write_json(spec.run_root / "final_decision.json", final)
    write_json(spec.run_root / "run_manifest.json", final)
    write_stage_report(spec, created_at, final, runtime_rows)
    return {
        "stage_num": spec.stage_num,
        "stage_id": spec.stage_id,
        "run_id": spec.run_id,
        "classification": classification,
        "runtime_rows": runtime_rows,
        "preflight_checks": preflight_candidate(spec, feature_order, feature_hash).get("checks", {}),
        "reason": final["judgment"],
    }


def build_split_payload(spec: CandidateSpec, full: pd.DataFrame, feature_order: Sequence[str], model: Any) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    rows_for_expected: list[dict[str, Any]] = []
    for runtime_split, source_split in (("validation_is", "validation"), ("oos", "oos")):
        frame = full.loc[full["split"].astype(str).eq(source_split)].copy()
        frame["timestamp"] = pd.to_datetime(frame["timestamp"], utc=True)
        matrix = frame.loc[:, list(feature_order)].astype("float64").to_numpy()
        probabilities = ordered_sklearn_probabilities(model, matrix, class_order=f04d.LABEL_ORDER)
        signal = signal_from_probabilities(probabilities, spec)
        feature_path = spec.feature_root / f"{spec.run_id}_{runtime_split}_features.csv"
        feature_export = mt5.export_mt5_feature_matrix_csv(frame, feature_order, feature_path, metadata_columns=("raw_index",))
        expected = expected_signal_summary(spec, frame, signal, runtime_split)
        rows_for_expected.append(expected)
        out[runtime_split] = {
            "source_split": source_split,
            "frame": frame,
            "probabilities": probabilities,
            "signal": signal,
            "feature_export": feature_export,
            "expected": expected,
            "from_date": split_date_range(frame)[0],
            "to_date": split_date_range(frame)[1],
        }
    write_csv(spec.run_root / "expected_signal_summary.csv", rows_for_expected)
    return out


def signal_from_probabilities(probabilities: np.ndarray, spec: CandidateSpec) -> np.ndarray:
    p_short = probabilities[:, 0]
    p_flat = probabilities[:, 1]
    p_long = probabilities[:, 2]
    if spec.decision_mode == "argmax":
        idx = probabilities.argmax(axis=1)
        return np.where(idx == 0, -1, np.where(idx == 2, 1, 0)).astype("int8")
    if spec.decision_mode == "edge_margin":
        short_side = p_short >= p_long
        direction_probability = np.where(short_side, p_short, p_long)
        edge_margin = direction_probability - p_flat
        selected = (direction_probability >= np.where(short_side, spec.short_threshold, spec.long_threshold)) & (
            edge_margin >= spec.min_margin
        )
        return np.where(selected, np.where(short_side, -1, 1), 0).astype("int8")
    short_margin = p_short - np.maximum(p_flat, p_long)
    long_margin = p_long - np.maximum(p_flat, p_short)
    short_ok = (p_short >= spec.short_threshold) & (short_margin >= spec.min_margin)
    long_ok = (p_long >= spec.long_threshold) & (long_margin >= spec.min_margin)
    signal = np.zeros(len(probabilities), dtype="int8")
    signal[long_ok & (~short_ok | (p_long >= p_short))] = 1
    signal[short_ok & ~(long_ok & (p_long >= p_short))] = -1
    return signal


def materialize_attempts(
    spec: CandidateSpec,
    split_payload: Mapping[str, Mapping[str, Any]],
    feature_order: Sequence[str],
    feature_hash: str,
    common_files_root: Path,
) -> list[dict[str, Any]]:
    identity = scout.RunIdentity(
        stage_id=spec.stage_id,
        stage_number=spec.stage_num,
        run_number=spec.run_number,
        run_id=spec.run_id,
        exploration_label=f"frontier{spec.stage_num:02d}_runtime_probe_backfill(전선{spec.stage_num:02d} 런타임 탐침 소급)",
        common_run_root=f"Project_Obsidian_Prime_v2/frontier{spec.stage_num:02d}Z_runtime_probe_backfill",
    )
    rule = scout.ThresholdRule(
        threshold_id=f"{spec.run_id}_{spec.decision_mode}",
        short_threshold=spec.short_threshold,
        long_threshold=spec.long_threshold,
        min_margin=spec.min_margin,
    )
    mt5.copy_to_common_files(common_files_root, ROOT / spec.onnx_path, scout.common_ref("models", spec.onnx_path.name, context=identity))
    attempts: list[dict[str, Any]] = []
    for runtime_split, payload in split_payload.items():
        attempt_name = f"frontier{spec.stage_num:02d}z_tier_a_{runtime_split}"
        mt5.copy_to_common_files(
            common_files_root,
            ROOT / str(payload["feature_export"]["path"]),
            scout.common_ref("features", Path(str(payload["feature_export"]["path"])).name, context=identity),
        )
        attempt = scout.materialize_mt5_attempt_files(
            run_output_root=spec.run_root,
            tier_name=scout.TIER_A,
            split_name=runtime_split,
            local_onnx_path=ROOT / spec.onnx_path,
            local_feature_matrix_path=ROOT / str(payload["feature_export"]["path"]),
            rule=rule,
            feature_count=len(feature_order),
            feature_order_hash=feature_hash,
            from_date=str(payload["from_date"]),
            to_date=str(payload["to_date"]),
            stem_prefix=attempt_name,
            record_view_prefix=f"mt5_frontier{spec.stage_num:02d}z_tier_a",
            attempt_role="tier_a_runtime_probe_backfill",
            decision_mode=spec.decision_mode,
            max_hold_bars=spec.max_hold_bars,
            reentry_cooldown_bars=spec.cooldown_bars,
            context=identity,
        )
        attempt.update(
            {
                "attempt_name": attempt_name,
                "candidate_id": spec.candidate_id,
                "model_id": spec.model_id,
                "source_run_id": spec.source_run_id,
                "decision_mode": spec.decision_mode,
                "ini_name": scout.mt5_short_profile_ini_name(scout.TIER_A, runtime_split, context=identity),
            }
        )
        attempts.append(attempt)
    return attempts


def compile_runtime_ea(metaeditor_path: Path) -> dict[str, Any]:
    compile_payload = mt5.compile_mql5_ea(metaeditor_path, EA_SOURCE, PROJECT_MANIFEST.parent / "frontier_runtime_backfill_mt5_compile.log")
    portable_payload = sync_portable_ea()
    payload = {"compile": compile_payload, "portable_ea": portable_payload}
    write_json(PROJECT_MANIFEST.parent / "frontier_runtime_backfill_mt5_compile_result.json", payload)
    return payload


def sync_portable_ea() -> dict[str, Any]:
    payload = {
        "repo_ea_ex5": EA_BINARY.as_posix(),
        "portable_ea_ex5": PORTABLE_EA_BINARY.as_posix(),
        "portable_ea_ex5_exists": path_exists(PORTABLE_EA_BINARY),
        "copied": False,
    }
    if path_exists(EA_BINARY):
        io_path(PORTABLE_EA_BINARY.parent).mkdir(parents=True, exist_ok=True)
        shutil.copy2(io_path(EA_BINARY), io_path(PORTABLE_EA_BINARY))
        payload["copied"] = True
        payload["portable_ea_ex5_exists"] = path_exists(PORTABLE_EA_BINARY)
        payload["portable_ea_sha256"] = mt5.sha256_file(PORTABLE_EA_BINARY)
    return payload


def terminal_processes() -> dict[str, Any]:
    try:
        import psutil  # type: ignore
    except Exception:
        return {"status": "psutil_unavailable_assume_clear"}
    rows = []
    for proc in psutil.process_iter(["pid", "name", "exe", "cmdline"]):
        try:
            name = str(proc.info.get("name") or "").lower()
            exe = str(proc.info.get("exe") or "")
            if name == "terminal64.exe" and str(DEFAULT_PORTABLE_ROOT).lower() in exe.lower():
                rows.append({"pid": proc.info.get("pid"), "exe": exe, "cmdline": proc.info.get("cmdline")})
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return {"status": "no_terminal64_process" if not rows else "terminal64_process_found", "processes": rows}


def build_runtime_summary_rows(
    spec: CandidateSpec,
    attempts: Sequence[Mapping[str, Any]],
    execution_payload: Mapping[str, Any],
    split_payload: Mapping[str, Mapping[str, Any]],
) -> list[dict[str, Any]]:
    result_by_attempt = {str(row.get("attempt_name")): row for row in execution_payload.get("execution_results", [])}
    rows: list[dict[str, Any]] = []
    for attempt in attempts:
        result = dict(result_by_attempt.get(str(attempt["attempt_name"]), {}))
        runtime = result.get("runtime_outputs", {}) if isinstance(result.get("runtime_outputs"), Mapping) else {}
        last_summary = runtime.get("last_summary", {}) if isinstance(runtime.get("last_summary"), Mapping) else {}
        report = result.get("strategy_tester_report", {}) if isinstance(result.get("strategy_tester_report"), Mapping) else {}
        metrics = report.get("metrics", {}) if isinstance(report.get("metrics"), Mapping) else {}
        expected = split_payload[str(attempt["split"])]["expected"]
        rows.append(
            {
                "stage_id": spec.stage_id,
                "run_id": spec.run_id,
                "attempt_name": attempt["attempt_name"],
                "split": attempt["split"],
                "tester_status": result.get("status", "missing"),
                "tester_returncode": result.get("returncode", ""),
                "runtime_status": runtime.get("status", "missing"),
                "runtime_wait_status": runtime.get("wait_status", ""),
                "report_status": report.get("status", "missing"),
                "model_ok_count": as_int(last_summary.get("model_ok_count")),
                "feature_ready_count": as_int(last_summary.get("feature_ready_count")),
                "mt5_long_count": as_int(last_summary.get("long_count")),
                "mt5_short_count": as_int(last_summary.get("short_count")),
                "mt5_flat_count": as_int(last_summary.get("flat_count")),
                "mt5_order_attempt_count": as_int(last_summary.get("order_attempt_count")),
                "mt5_order_fill_count": as_int(last_summary.get("order_fill_count")),
                "expected_rows": int(expected["rows"]),
                "expected_signal_count": int(expected["signal_count"]),
                "expected_long_count": int(expected["long_count"]),
                "expected_short_count": int(expected["short_count"]),
                "expected_flat_count": int(expected["flat_count"]),
                "signal_count_diff": as_int(last_summary.get("long_count")) + as_int(last_summary.get("short_count")) - int(expected["signal_count"]),
                "long_count_diff": as_int(last_summary.get("long_count")) - int(expected["long_count"]),
                "short_count_diff": as_int(last_summary.get("short_count")) - int(expected["short_count"]),
                "feature_ready_diff": as_int(last_summary.get("feature_ready_count")) - int(expected["rows"]),
                "net_profit": metrics.get("net_profit"),
                "profit_factor": metrics.get("profit_factor"),
                "trade_count": metrics.get("trade_count"),
                "max_drawdown_percent": metrics.get("max_drawdown_percent"),
                "recovery_factor": metrics.get("recovery_factor"),
                "blocker": result.get("blocker", ""),
            }
        )
    write_csv(spec.run_root / "mt5_runtime_probe_summary.csv", rows)
    return rows


def upsert_backfill_status_ledger(
    stage_num: int,
    stage_id: str,
    created_at: str,
    classification: str,
    preflight: Mapping[str, Any],
    spec: CandidateSpec | None,
    runtime_rows: Sequence[Mapping[str, Any]],
) -> None:
    stage_ledger = Path("stages") / stage_id / "03_reviews" / "stage_run_ledger.csv"
    ensure_stage_ledger(stage_ledger)
    rows = ledger_rows(stage_num, stage_id, created_at, classification, preflight, spec, runtime_rows)
    for row in rows:
        upsert_csv(PROJECT_LEDGER, "ledger_row_id", row)
        upsert_csv(stage_ledger, "ledger_row_id", row)


def ledger_rows(
    stage_num: int,
    stage_id: str,
    created_at: str,
    classification: str,
    preflight: Mapping[str, Any],
    spec: CandidateSpec | None,
    runtime_rows: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    run_id = spec.run_id if spec else f"frontier{stage_num:02d}Z_runtime_probe_backfill_status_v1"
    parent_run_id = spec.parent_run_id if spec else parent_run_id_from_stage(Path("stages") / stage_id)
    report_path = (
        Path("stages") / stage_id / "03_reviews" / f"{run_id}_report.md"
        if spec
        else Path("stages") / stage_id / "03_reviews" / "runtime_probe_backfill_status.md"
    )
    base = {
        "stage_id": stage_id,
        "run_id": run_id,
        "parent_run_id": parent_run_id,
        "scoreboard_lane": "runtime_probe_backfill(런타임 탐침 소급)",
        "status": classification,
        "judgment": judgment_for_classification(classification),
        "path": report_path.as_posix(),
        "guardrail_kpi": "no_authority_no_goal_claim(권위/목표 주장 없음)",
        "external_verification_status": "mt5_runtime_probe_backfill_recorded(MT5 런타임 탐침 소급 기록)",
        "claim_boundary": CLAIM_BOUNDARY,
        "created_at_utc": created_at,
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "run_family": "runtime_backfill(런타임 소급)",
        "run_type": "mt5_runtime_probe_backfill(MT5 런타임 탐침 소급)",
    }
    if not runtime_rows:
        return [
            {
                **base,
                "ledger_row_id": f"{run_id}__status",
                "subrun_id": f"{run_id}__status",
                "record_view": "runtime_probe_backfill_status(런타임 탐침 소급 상태)",
                "tier_scope": "missing_required_or_verify_only(필수 누락 또는 확인 전용)",
                "kpi_scope": "status_record(상태 기록)",
                "primary_kpi": str(preflight.get("reason", classification)),
                "notes": json.dumps(json_ready(preflight.get("checks", {})), ensure_ascii=False, sort_keys=True),
            }
        ]
    rows: list[dict[str, Any]] = []
    for item in runtime_rows:
        split = str(item.get("split", "unknown"))
        rows.append(
            {
                **base,
                "ledger_row_id": f"{run_id}__tier_a_{split}",
                "subrun_id": f"{run_id}__tier_a_{split}",
                "record_view": f"Tier A separate {split}(티어 A 분리 {split})",
                "tier_scope": "Tier A(티어 A)",
                "kpi_scope": "mt5_runtime_probe_backfill_observation(MT5 런타임 탐침 소급 관찰)",
                "primary_kpi": runtime_row_kpi(item),
                "notes": f"candidate={spec.candidate_id if spec else ''};signal_diff={item.get('signal_count_diff')};blocker={item.get('blocker','')}",
                "net_profit": item.get("net_profit"),
                "profit_factor": item.get("profit_factor"),
                "trade_count": item.get("trade_count"),
                "max_drawdown_percent": item.get("max_drawdown_percent"),
                "drawdown": item.get("max_drawdown_percent"),
                "recovery_factor": item.get("recovery_factor"),
            }
        )
    rows.append(
        {
            **base,
            "ledger_row_id": f"{run_id}__tier_b_missing_required",
            "subrun_id": f"{run_id}__tier_b_missing_required",
            "record_view": "Tier B separate(티어 B 분리)",
            "tier_scope": "Tier B(티어 B)",
            "kpi_scope": "missing_required(필수 누락)",
            "primary_kpi": "missing_required_no_tier_b_runtime_backfill(필수 누락, 티어 B 소급 런타임 없음)",
            "notes": "Tier B was not materialized for this retro probe(티어 B는 이번 소급 탐침에서 물질화되지 않음)",
        }
    )
    rows.append(
        {
            **base,
            "ledger_row_id": f"{run_id}__tier_ab_missing_required",
            "subrun_id": f"{run_id}__tier_ab_missing_required",
            "record_view": "Tier A+B combined(티어 A+B 합산)",
            "tier_scope": "Tier A+B(티어 A+B)",
            "kpi_scope": "missing_required(필수 누락)",
            "primary_kpi": "missing_required_no_combined_runtime_backfill(필수 누락, 합산 소급 런타임 없음)",
            "notes": "Combined routed probe was not materialized in this retro packet(이번 소급 묶음에서 합산 라우팅 탐침은 물질화되지 않음)",
        }
    )
    return rows


def write_stage_status(
    stage_num: int,
    stage_id: str,
    created_at: str,
    classification: str,
    preflight: Mapping[str, Any],
    spec: CandidateSpec | None,
    runtime_rows: Sequence[Mapping[str, Any]],
) -> None:
    review_dir = Path("stages") / stage_id / "03_reviews"
    selected_dir = Path("stages") / stage_id / "04_selected"
    io_path(review_dir).mkdir(parents=True, exist_ok=True)
    io_path(selected_dir).mkdir(parents=True, exist_ok=True)
    payload = {
        "stage_num": stage_num,
        "stage_id": stage_id,
        "created_at_utc": created_at,
        "classification": classification,
        "judgment": judgment_for_classification(classification),
        "preflight": preflight,
        "candidate": candidate_payload(spec) if spec else None,
        "runtime_rows": list(runtime_rows),
        "claim_boundary": claim_boundary_payload(),
        "grok_pre_mt5_review": GROK_REVIEW.as_posix(),
    }
    write_json(review_dir / "runtime_probe_backfill_status.json", payload)
    text = stage_status_text(payload)
    write_text_sig(review_dir / "runtime_probe_backfill_status.md", text)
    append_once(selected_dir / "selection_status.md", "runtime_probe_backfill_status", "\n" + text)


def write_stage_report(spec: CandidateSpec, created_at: str, final: Mapping[str, Any], runtime_rows: Sequence[Mapping[str, Any]]) -> None:
    path = Path("stages") / spec.stage_id / "03_reviews" / f"{spec.run_id}_report.md"
    lines = [
        f"# Frontier{spec.stage_num:02d} Runtime Probe Backfill(전선{spec.stage_num:02d} 런타임 탐침 소급)",
        "",
        f"Updated(갱신): {created_at}",
        "",
        f"Status(상태): `{final['status']}`",
        "",
        f"Judgment(판정): `{final['judgment']}`",
        "",
        "Action(행동): existing candidate ONNX(기존 후보 온엑스)를 MT5 runtime probe(MT5 런타임 탐침)로 실행했습니다.",
        "",
        "Effect(효과): proxy-only gap(프록시 전용 공백)을 실제 tester KPI(테스터 지표) 관찰로 보강하되 authority(권위)는 만들지 않습니다.",
        "",
        "| split(분할) | runtime(런타임) | report(보고서) | PF(수익 팩터) | DD%(손실폭) | trades(거래) | signal diff(신호 차이) |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for row in runtime_rows:
        lines.append(
            f"| `{row.get('split')}` | `{row.get('runtime_status')}` | `{row.get('report_status')}` | "
            f"{fmt(row.get('profit_factor'))} | {fmt(row.get('max_drawdown_percent'))} | {fmt(row.get('trade_count'))} | {row.get('signal_count_diff')} |"
        )
    lines.extend(
        [
            "",
            f"Candidate(후보): `{spec.candidate_id}`",
            f"Decision mode(결정 방식): `{spec.decision_mode}`",
            "",
            "Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 모두 not_claimed(주장 없음)입니다.",
            "",
        ]
    )
    write_text_sig(path, "\n".join(lines))


def write_project_summary(
    created_at: str,
    manifest_rows: Sequence[Mapping[str, Any]],
    *,
    preflight_only: bool,
    run_summaries: Sequence[Mapping[str, Any]] | None = None,
) -> None:
    counts: dict[str, int] = {}
    for row in manifest_rows:
        status = str(row.get("preflight_status") or row.get("classification") or "unknown")
        counts[status] = counts.get(status, 0) + 1
    lines = [
        "# Frontier Runtime Probe Backfill Summary(전선 런타임 탐침 소급 요약)",
        "",
        f"Updated(갱신): {created_at}",
        "",
        f"Mode(모드): {'preflight only(사전 점검만)' if preflight_only else 'MT5 executed where executable(MT5 실행 가능 대상 실행)'}",
        "",
        "Action(행동): frontier stage(전선 단계)별 누락 MT5 runtime probe(MT5 런타임 탐침)를 소급 점검했습니다.",
        "",
        "Effect(효과): 실제 실행 가능한 후보는 backtest KPI(백테스트 지표)로 보강하고, 실행 불가 단계는 blocker(차단 사유)를 장부에 남겼습니다.",
        "",
        "## Counts(집계)",
        "",
    ]
    for key, value in sorted(counts.items()):
        lines.append(f"- `{key}`: {value}")
    if run_summaries:
        lines.extend(["", "## MT5 Runs(MT5 실행)", ""])
        for run in run_summaries:
            lines.append(f"- `{run.get('run_id')}`: `{run.get('classification')}`")
    lines.extend(
        [
            "",
            "Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 모두 not_claimed(주장 없음)입니다.",
            "",
        ]
    )
    write_text_sig(PROJECT_SUMMARY, "\n".join(lines))


def stage_status_text(payload: Mapping[str, Any]) -> str:
    lines = [
        f"# Runtime Probe Backfill Status(런타임 탐침 소급 상태)",
        "",
        f"Updated(갱신): {payload['created_at_utc']}",
        "",
        f"Status(상태): `{payload['classification']}`",
        "",
        f"Judgment(판정): `{payload['judgment']}`",
        "",
        "Action(행동): omitted MT5 runtime probe(누락된 MT5 런타임 탐침)를 소급 점검했습니다.",
        "",
        "Effect(효과): 실행 가능 후보는 실제 tester KPI(테스터 지표)로 보강하고, 불가능한 후보는 blocker(차단 사유)를 남깁니다.",
        "",
        f"Reason(사유): `{payload.get('preflight', {}).get('reason', '')}`",
        "",
        "Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 모두 not_claimed(주장 없음)입니다.",
        "",
    ]
    return "\n".join(lines)


def has_backfill_status(stage_id: str) -> bool:
    return path_exists(Path("stages") / stage_id / "03_reviews" / "runtime_probe_backfill_status.json")


def manifest_row(
    stage_num: int,
    stage_id: str,
    classification: str,
    preflight: Mapping[str, Any],
    spec: CandidateSpec | None,
) -> dict[str, Any]:
    checks = preflight.get("checks", {}) if isinstance(preflight.get("checks"), Mapping) else {}
    return {
        "stage_num": stage_num,
        "stage_id": stage_id,
        "classification": classification,
        "preflight_status": preflight.get("status", classification),
        "reason": preflight.get("reason", ""),
        "candidate_id": spec.candidate_id if spec else "",
        "model_id": spec.model_id if spec else "",
        "onnx_path": spec.onnx_path.as_posix() if spec else "",
        "model_path": spec.model_path.as_posix() if spec else "",
        "decision_mode": spec.decision_mode if spec else "",
        "source_contract": spec.source_contract if spec else "",
        "closeout_blocker_token": checks.get("closeout_blocker_token", ""),
        "onnx_exists": checks.get("onnx_exists", ""),
        "model_exists": checks.get("model_exists", ""),
        "model_n_features_in": checks.get("model_n_features_in", ""),
        "feature_count": checks.get("feature_count", ""),
    }


def expected_signal_summary(spec: CandidateSpec, frame: pd.DataFrame, signal: np.ndarray, runtime_split: str) -> dict[str, Any]:
    timestamps = pd.to_datetime(frame["timestamp"], utc=True).reset_index(drop=True)
    days = count_scope_days(timestamps) if len(timestamps) else 0
    return {
        "stage_id": spec.stage_id,
        "run_id": spec.run_id,
        "split": runtime_split,
        "rows": int(len(frame)),
        "days_in_scope": int(days),
        "decision_mode": spec.decision_mode,
        "signal_count": int((signal != 0).sum()),
        "long_count": int((signal == 1).sum()),
        "short_count": int((signal == -1).sum()),
        "flat_count": int((signal == 0).sum()),
        "expected_density_per_day": float((signal != 0).sum() / days) if days else 0.0,
    }


def count_scope_days(timestamps: pd.Series) -> int:
    local_dates = pd.to_datetime(timestamps, utc=True).dt.tz_convert("America/New_York").dt.date
    return int(local_dates.nunique())


def source_snapshot(
    spec: CandidateSpec,
    source_integrity: Mapping[str, Any],
    split_payload: Mapping[str, Mapping[str, Any]],
) -> dict[str, Any]:
    return {
        "candidate": candidate_payload(spec),
        "source_integrity": source_integrity,
        "split_rows": {name: payload["expected"] for name, payload in split_payload.items()},
        "effect": "Runtime probe backfill source truth(런타임 탐침 소급 원천 진실)을 고정합니다.",
    }


def copy_runtime_outputs(common_files_root: Path, spec: CandidateSpec, attempts: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    io_path(spec.telemetry_copy_root).mkdir(parents=True, exist_ok=True)
    for attempt in attempts:
        for artifact_kind, key in (("telemetry", "common_telemetry_path"), ("summary", "common_summary_path")):
            source = common_files_root / Path(str(attempt.get(key, "")))
            destination = spec.telemetry_copy_root / f"{attempt['attempt_name']}_{artifact_kind}.csv"
            row = {
                "attempt_name": attempt["attempt_name"],
                "artifact_kind": artifact_kind,
                "source_path": source.as_posix(),
                "repo_path": destination.as_posix(),
                "status": "missing",
                "sha256": "",
            }
            if path_exists(source):
                shutil.copy2(io_path(source), io_path(destination))
                row["status"] = "copied"
                row["sha256"] = mt5.sha256_file(destination)
            rows.append(row)
    write_csv(spec.run_root / "runtime_output_copy_manifest.csv", rows)
    return rows


def blocked_result(spec: CandidateSpec, attempt: Mapping[str, Any], blocker: str) -> dict[str, Any]:
    return {
        "attempt_name": attempt.get("attempt_name"),
        "tier": attempt.get("tier"),
        "split": attempt.get("split"),
        "record_view_prefix": attempt.get("record_view_prefix"),
        "attempt_role": attempt.get("attempt_role"),
        "candidate_id": spec.candidate_id,
        "model_id": spec.model_id,
        "status": "blocked",
        "blocker": blocker,
        "runtime_outputs": {"status": "blocked", "blocker": blocker},
    }


def remove_runtime_outputs(common_files_root: Path, attempt: Mapping[str, Any]) -> None:
    for key in ("common_telemetry_path", "common_summary_path"):
        path = common_files_root / Path(str(attempt.get(key, "")))
        if path_exists(path):
            io_path(path).unlink()


def ensure_run_dirs(spec: CandidateSpec) -> None:
    for path in (spec.run_root, spec.mt5_root, spec.feature_root, spec.telemetry_copy_root, Path("stages") / spec.stage_id / "03_reviews"):
        io_path(path).mkdir(parents=True, exist_ok=True)


def ensure_stage_ledger(stage_ledger: Path) -> None:
    if path_exists(stage_ledger):
        return
    header = read_csv_header(PROJECT_LEDGER)
    io_path(stage_ledger.parent).mkdir(parents=True, exist_ok=True)
    with io_path(stage_ledger).open("w", encoding="utf-8-sig", newline="") as handle:
        csv.writer(handle, lineterminator="\n").writerow(header)


def latest_best_row_payload(stage: Path) -> tuple[Path, dict[str, Any]] | None:
    rows: list[tuple[Path, dict[str, Any]]] = []
    for path in all_json_paths(stage):
        try:
            payload = read_json(path)
        except Exception:
            continue
        row = payload.get("best_candidate_row")
        if isinstance(row, dict):
            rows.append((path, row))
    return rows[-1] if rows else None


def parent_run_id_from_stage(stage: Path) -> str:
    manifests = [path for path in all_json_paths(stage) if path.name == "run_manifest.json"]
    if not manifests:
        return ""
    try:
        return str(read_json(manifests[-1]).get("run_id", manifests[-1].parent.name))
    except Exception:
        return manifests[-1].parent.name


def all_json_paths(stage: Path) -> list[Path]:
    paths: list[Path] = []
    for dirpath, _dirnames, filenames in os.walk(io_path(stage)):
        for filename in filenames:
            if filename in {"final_decision.json", "run_manifest.json", "closeout_summary.json"}:
                paths.append(Path(str(Path(dirpath) / filename).replace("\\\\?\\", "")))
    return sorted(paths)


def runtime_blocker_token(stage: Path) -> str:
    tokens = [
        "runtime_probe_ineligible",
        "no_runtime_handoff_candidate",
        "no_seed_or_runtime_candidate",
        "no_scout_seed_or_runtime_candidate",
        "proxy_not_materialized",
    ]
    chunks: list[str] = []
    selected_json = stage / "04_selected/selection_status.json"
    if path_exists(selected_json):
        try:
            selected_payload = read_json(selected_json)
            selected_token = str(selected_payload.get("runtime_probe_status") or "")
            if selected_token:
                return selected_token
        except Exception:
            pass
    selected = stage / "04_selected/selection_status.md"
    if path_exists(selected):
        chunks.append(io_path(selected).read_text(encoding="utf-8-sig", errors="ignore"))
    for path in all_json_paths(stage):
        try:
            chunks.append(json.dumps(read_json(path), ensure_ascii=False))
        except Exception:
            continue
    text = "\n".join(chunks)
    lower = text.lower()
    for token in tokens:
        idx = lower.find(token)
        if idx >= 0:
            return text[idx : idx + 220].replace("\n", " ")
    return ""


def existing_mt5_reports(stage: Path) -> list[Path]:
    reports: list[Path] = []
    for dirpath, _dirnames, filenames in os.walk(io_path(stage)):
        for filename in filenames:
            if filename.lower().endswith((".htm", ".html")) and ("mt5" in dirpath.lower() or "report" in dirpath.lower()):
                reports.append(Path(str(Path(dirpath) / filename).replace("\\\\?\\", "")))
    return reports


def list_files(stage: Path, suffix: str) -> list[Path]:
    rows: list[Path] = []
    for dirpath, _dirnames, filenames in os.walk(io_path(stage)):
        for filename in filenames:
            if filename.lower().endswith(suffix):
                rows.append(Path(str(Path(dirpath) / filename).replace("\\\\?\\", "")))
    return rows


def exact_file_by_stem(stage: Path, stem: str, suffix: str) -> list[Path]:
    return [path for path in list_files(stage, suffix) if path.stem == stem]


def stage_dir_for_num(stage_num: int) -> Path | None:
    matches = sorted((ROOT / "stages").glob(f"stage_frontier_{stage_num:02d}__*"))
    return matches[0].relative_to(ROOT) if matches else None


def to_repo_path(path: Path) -> Path:
    if path.is_absolute():
        try:
            return path.resolve().relative_to(ROOT.resolve())
        except ValueError:
            return path
    return path


def parse_hold_bars(text: str) -> int | None:
    import re

    match = re.search(r"(?:^|_)h(\d+)(?:_|$)", text)
    return int(match.group(1)) if match else None


def split_date_range(frame: pd.DataFrame) -> tuple[str, str]:
    timestamps = pd.to_datetime(frame["timestamp"], utc=True)
    if timestamps.empty:
        raise RuntimeError("empty split frame")
    return timestamps.min().strftime("%Y.%m.%d"), (timestamps.max() + pd.Timedelta(days=1)).strftime("%Y.%m.%d")


def claim_boundary_payload() -> dict[str, str]:
    return {
        "completion": "not_claimed(주장 없음)",
        "selected_baseline": "not_claimed(주장 없음)",
        "operating_promotion": "not_claimed(주장 없음)",
        "runtime_authority": "not_claimed(주장 없음)",
        "live_readiness": "not_claimed(주장 없음)",
        "goal_achieve": "not_claimed(주장 없음)",
    }


def candidate_payload(spec: CandidateSpec | None) -> dict[str, Any] | None:
    if spec is None:
        return None
    return {
        "candidate_id": spec.candidate_id,
        "model_id": spec.model_id,
        "model_path": spec.model_path.as_posix(),
        "onnx_path": spec.onnx_path.as_posix(),
        "decision_mode": spec.decision_mode,
        "short_threshold": spec.short_threshold,
        "long_threshold": spec.long_threshold,
        "min_margin": spec.min_margin,
        "max_hold_bars": spec.max_hold_bars,
        "cooldown_bars": spec.cooldown_bars,
        "source_contract": spec.source_contract,
        "source_note": spec.source_note,
    }


def judgment_for_classification(classification: str) -> str:
    mapping = {
        "runtime_probe_backfill_observation_no_authority": "runtime_probe_observation(런타임 탐침 관찰)",
        "blocked_attempt_failed": "blocked_attempt_failed(시도 실패 차단)",
        "completed_existing_verify_only": "completed_existing_verify_only(기존 완료 확인 전용)",
        "invalid_setup_no_runtime_material": "invalid_setup_no_runtime_material(런타임 재료 없음 무효 설정)",
        "missing_artifact_blocked": "missing_artifact_blocked(산출물 누락 차단)",
        "out_of_scope_by_claim": "out_of_scope_by_claim(주장 범위 밖)",
    }
    return mapping.get(classification, classification)


def runtime_row_kpi(row: Mapping[str, Any]) -> str:
    return (
        f"{row.get('split')}:status={row.get('runtime_status')}/{row.get('report_status')};"
        f"pf={fmt(row.get('profit_factor'))};dd={fmt(row.get('max_drawdown_percent'))};"
        f"trades={fmt(row.get('trade_count'))};signal_diff={row.get('signal_count_diff')}"
    )


def flatten_attempt_rows(attempts: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for attempt in attempts:
        rows.append(
            {
                "attempt_name": attempt.get("attempt_name"),
                "tier": attempt.get("tier"),
                "split": attempt.get("split"),
                "set_path": attempt.get("set", {}).get("path"),
                "ini_path": attempt.get("ini", {}).get("path"),
                "common_model_path": attempt.get("common_model_path"),
                "common_feature_matrix_path": attempt.get("common_feature_matrix_path"),
                "common_telemetry_path": attempt.get("common_telemetry_path"),
                "common_summary_path": attempt.get("common_summary_path"),
            }
        )
    return rows


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    materialized = [dict(row) for row in rows]
    if fieldnames is None:
        fieldnames = []
        for row in materialized:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    write_csv_atomic(path, list(fieldnames), materialized)


def upsert_csv(path: Path, key: str, row: Mapping[str, Any]) -> None:
    header = read_csv_header(path)
    existing_rows: list[dict[str, str]] = []
    with writable_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        existing_rows.extend(dict(item) for item in csv.DictReader(handle))
    normalized = {column: stringify(row.get(column, "")) for column in header}
    replaced = False
    for index, existing in enumerate(existing_rows):
        if existing.get(key) == normalized.get(key):
            existing_rows[index] = normalized
            replaced = True
            break
    if not replaced:
        existing_rows.append(normalized)
    write_csv_atomic(path, header, existing_rows)


def write_csv_atomic(path: Path, fieldnames: Sequence[str], rows: Iterable[Mapping[str, Any]]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    materialized = [dict(row) for row in rows]
    tmp_path = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    try:
        with writable_path(tmp_path).open("w", encoding="utf-8-sig", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(fieldnames), extrasaction="ignore", lineterminator="\n")
            writer.writeheader()
            for item in materialized:
                writer.writerow({column: stringify(item.get(column, "")) for column in fieldnames})
        last_error: OSError | None = None
        for attempt in range(24):
            try:
                os.replace(writable_path(tmp_path), writable_path(path))
                last_error = None
                break
            except OSError as replace_error:
                last_error = replace_error
                try:
                    write_csv_in_place(path, fieldnames, materialized)
                    last_error = None
                    break
                except OSError as in_place_error:
                    last_error = in_place_error
                    if attempt < 23:
                        time.sleep(0.5)
        if last_error is not None:
            raise last_error
    finally:
        try:
            writable_path(tmp_path).unlink()
        except FileNotFoundError:
            pass


def write_csv_in_place(path: Path, fieldnames: Sequence[str], rows: Iterable[Mapping[str, Any]]) -> None:
    with writable_path(path).open("r+", encoding="utf-8-sig", newline="") as handle:
        handle.seek(0)
        handle.truncate(0)
        writer = csv.DictWriter(handle, fieldnames=list(fieldnames), extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for item in rows:
            writer.writerow({column: stringify(item.get(column, "")) for column in fieldnames})


def read_csv_header(path: Path) -> list[str]:
    with writable_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return next(csv.reader(handle))


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    writable_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8-sig")


def read_json(path: Path) -> Any:
    return json.loads(writable_path(path).read_text(encoding="utf-8-sig"))


def write_text_sig(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    writable_path(path).write_text(text, encoding="utf-8-sig", newline="\n")


def append_once(path: Path, marker: str, text: str) -> None:
    existing = writable_path(path).read_text(encoding="utf-8-sig") if path_exists(path) else ""
    if marker in existing:
        return
    if existing and not existing.endswith("\n"):
        existing += "\n"
    write_text_sig(path, existing + f"\n<!-- {marker} -->\n" + text)


def stringify(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(json_ready(value), ensure_ascii=False, sort_keys=True)
    if isinstance(value, float):
        return "" if not math.isfinite(value) else str(value)
    return str(value)


def as_int(value: Any) -> int:
    try:
        if value is None or str(value).strip() == "":
            return 0
        return int(round(float(value)))
    except (TypeError, ValueError):
        return 0


def fmt(value: Any) -> str:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return "n/a"
    if not math.isfinite(number):
        return "n/a"
    return f"{number:.6g}"


def tail_text(value: Any, limit: int = 4000) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="ignore")[-limit:]
    return str(value)[-limit:]


def writable_path(path: Path) -> Path:
    resolved = path.resolve()
    if os.name == "nt" and len(str(resolved)) < 240:
        return resolved
    return io_path(path)


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


if __name__ == "__main__":
    raise SystemExit(main())
