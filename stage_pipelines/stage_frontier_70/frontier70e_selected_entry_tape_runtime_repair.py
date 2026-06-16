from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import joblib
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists
from foundation.control_plane.mt5_tier_balance_completion import attempt_payload
from foundation.models.onnx_bridge import check_onnxruntime_probability_parity, export_sklearn_to_onnx_zipmap_disabled
from foundation.mt5 import runtime_support as mt5
from stage_pipelines.stage_frontier_70 import frontier70d_label_regime_stability_runtime_probe as f70d
from stage_pipelines.stage_frontier_runtime_backfill.run_frontier_runtime_probe_backfill import (
    DEFAULT_COMMON_FILES,
    DEFAULT_METAEDITOR,
    DEFAULT_PORTABLE_ROOT,
    DEFAULT_TERMINAL,
    DEFAULT_TESTER_PROFILE_ROOT,
    EA_BINARY,
    PORTABLE_EA_BINARY,
)


STAGE_ID = f70d.STAGE_ID
RUN_ID = "frontier70E_selected_entry_tape_runtime_repair_v1"
PARENT_RUN_ID = f70d.RUN_ID
NEXT_RUN_ID = "frontier70F_stage_closeout_regime_specific_asymmetric_value_exit_model_rotation_v1"

STAGE_ROOT = f70d.STAGE_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REVIEWS_ROOT = f70d.REVIEWS_ROOT
MODEL_ROOT = RUN_ROOT / "models"
FEATURE_ROOT = RUN_ROOT / "features"
VETO_ROOT = RUN_ROOT / "runtime_veto_tapes"
MT5_ROOT = RUN_ROOT / "mt5"
COMMON_RUN_ROOT = "Project_Obsidian_Prime_v2/frontier70E_selected_entry_tape_runtime_repair"
GROK_PACKET_ROOT = ROOT / "docs/agent_control/grok_reviews/2026-06-17_f70e_pre_repair_selected_entry_runtime_probe"
GROK_PROMPT = GROK_PACKET_ROOT / "prompts/f70e_pre_repair_selected_entry_runtime_probe_prompt.md"
GROK_CLEAN = GROK_PACKET_ROOT / "outputs/clean_output.md"
GROK_METADATA = GROK_PACKET_ROOT / "outputs/metadata.json"

CLAIM_BOUNDARY = (
    "runtime_repair_observation_only_no_completion_no_baseline_no_promotion_"
    "no_runtime_authority_no_live_readiness_no_goal_achieve"
)
STATUS_MATERIALIZED = "materialized_selected_entry_tape_repair_pending_mt5_no_authority"
STATUS_COMPLETED = "completed_selected_entry_tape_runtime_repair_observation_no_authority"
STATUS_BLOCKED = "blocked_selected_entry_tape_runtime_repair_attempted_no_authority"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="F70E selected-entry RuntimeVetoTape repair probe.")
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--materialize-only", action="store_true")
    parser.add_argument("--timeout-seconds", type=int, default=600)
    parser.add_argument("--wait-timeout-seconds", type=int, default=300)
    parser.add_argument("--terminal-path", default=str(DEFAULT_TERMINAL))
    parser.add_argument("--metaeditor-path", default=str(DEFAULT_METAEDITOR))
    parser.add_argument("--common-files-root", default=str(DEFAULT_COMMON_FILES))
    parser.add_argument("--tester-profile-root", default=str(DEFAULT_TESTER_PROFILE_ROOT))
    parser.add_argument("--terminal-data-root", default=str(DEFAULT_PORTABLE_ROOT))
    return parser.parse_args()


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def ensure_dirs() -> None:
    for path in (RUN_ROOT, MODEL_ROOT, FEATURE_ROOT, VETO_ROOT, MT5_ROOT, MT5_ROOT / "reports", REVIEWS_ROOT, STAGE_ROOT / "04_selected"):
        io_path(path).mkdir(parents=True, exist_ok=True)


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def selected_mask_full(context: Mapping[str, Any]) -> np.ndarray:
    frame = context["frame"]
    selected = np.zeros(len(frame), dtype=bool)
    for split_payload in context["split_payload"].values():
        indices = np.asarray(split_payload["indices"], dtype=int)
        selected[indices] = np.asarray(split_payload["selected_mask"], dtype=bool)
    return selected


def write_selected_entry_tape(context: Mapping[str, Any], output_path: Path) -> dict[str, Any]:
    frame: pd.DataFrame = context["frame"]
    selected = selected_mask_full(context)
    event_mask = np.asarray(context["selection"].mask_name and f70d.f70b.mask_for(frame, context["selection"].mask_name), dtype=bool)
    payload = pd.DataFrame()
    timestamps = pd.to_datetime(frame["timestamp"], utc=True)
    payload["bar_time_server"] = timestamps.dt.strftime("%Y.%m.%d %H:%M:%S")
    payload["timestamp_utc"] = timestamps.dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    payload["entry_veto"] = np.where(selected, 0, 1).astype(int)
    payload["selected_entry"] = selected.astype(int)
    payload["event_active"] = event_mask.astype(int)
    payload["split"] = frame["split"].astype(str).to_numpy()
    io_path(output_path.parent).mkdir(parents=True, exist_ok=True)
    payload.to_csv(io_path(output_path), index=False, encoding="utf-8", lineterminator="\n")
    return {
        "path": output_path.as_posix(),
        "sha256": f70d.sha256_file(output_path),
        "rows": int(len(payload)),
        "selected_entry_rows": int(selected.sum()),
        "event_active_rows": int(event_mask.sum()),
        "veto_rows": int((~selected).sum()),
        "format": "runtime_veto_tape_entry_veto_outside_proxy_selected_non_overlap_entries",
    }


def export_context_artifacts(context: Mapping[str, Any]) -> dict[str, Any]:
    axis = context["axis"]
    feature_columns = list(context["feature_columns"])
    estimator = context["estimator"]
    model_path = MODEL_ROOT / f"{axis.candidate_id}.joblib"
    onnx_path = MODEL_ROOT / f"{axis.candidate_id}.onnx"
    feature_order_path = MODEL_ROOT / f"{axis.candidate_id}_feature_order.txt"
    feature_csv_path = FEATURE_ROOT / f"{axis.candidate_id}_features.csv"
    veto_path = VETO_ROOT / f"{axis.candidate_id}_selected_entry_runtime_veto_tape.csv"
    io_path(feature_order_path).write_text("\n".join(feature_columns) + "\n", encoding="utf-8")
    joblib.dump(estimator, io_path(model_path))
    export_meta = export_sklearn_to_onnx_zipmap_disabled(
        estimator,
        onnx_path,
        feature_count=len(feature_columns),
        target_opset=12,
        drop_label_output=True,
    )
    feature_meta = mt5.export_mt5_feature_matrix_csv(context["frame"], feature_columns, feature_csv_path, metadata_columns=("split",))
    veto_meta = write_selected_entry_tape(context, veto_path)
    return {
        "candidate_id": axis.candidate_id,
        "axis_id": axis.axis_id,
        "role": axis.role,
        "model_path": rel(model_path),
        "model_sha256": f70d.sha256_file(model_path),
        "onnx_path": rel(onnx_path),
        "onnx_sha256": f70d.sha256_file(onnx_path),
        "feature_order_path": rel(feature_order_path),
        "feature_order_sha256": f70d.sha256_file(feature_order_path),
        "feature_csv_path": rel(feature_csv_path),
        "feature_csv_sha256": f70d.sha256_file(feature_csv_path),
        "runtime_veto_tape_path": rel(veto_path),
        "runtime_veto_tape_sha256": f70d.sha256_file(veto_path),
        "onnx_export": export_meta,
        "feature_csv": feature_meta,
        "runtime_veto_tape": veto_meta,
        "feature_order_hash": context["feature_order_hash"],
        "threshold": context["threshold"],
    }


def selected_signal_parity_rows(context: Mapping[str, Any], artifact: Mapping[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    axis = context["axis"]
    onnx_path = ROOT / str(artifact["onnx_path"])
    estimator = context["estimator"]
    feature_columns = list(context["feature_columns"])
    probability_rows: list[dict[str, Any]] = []
    signal_rows: list[dict[str, Any]] = []
    for split_name in f70d.ALL_SPLITS:
        split_payload = context["split_payload"][split_name]
        split_frame: pd.DataFrame = split_payload["frame"]
        values = split_frame.loc[:, feature_columns].to_numpy(dtype="float64")
        probability = check_onnxruntime_probability_parity(
            estimator,
            onnx_path,
            values[: min(len(values), 2048)],
            class_order=(-1, 0, 1),
            tolerance=1e-5,
        )
        probability_rows.append({"candidate_id": axis.candidate_id, "axis_id": axis.axis_id, "split": split_name, **probability})
        onnx_proba = f70d.onnx_probabilities(onnx_path, values)
        onnx_side, onnx_score = f70d.side_score_from_probabilities(onnx_proba)
        sklearn_side = np.asarray(split_payload["side"], dtype=int)
        sklearn_score = np.asarray(split_payload["score"], dtype=float)
        selected = np.asarray(split_payload["selected_mask"], dtype=bool)
        threshold = float(context["threshold"])
        sklearn_signal = selected & (sklearn_score >= threshold)
        onnx_signal = selected & (onnx_score >= threshold)
        signal_rows.append(
            {
                "candidate_id": axis.candidate_id,
                "axis_id": axis.axis_id,
                "split": split_name,
                "rows": int(len(split_frame)),
                "selected_entry_rows": int(selected.sum()),
                "sklearn_signal_count": int(sklearn_signal.sum()),
                "onnx_signal_count": int(onnx_signal.sum()),
                "signal_count_diff": int(onnx_signal.sum() - sklearn_signal.sum()),
                "signal_mismatch_count": int((onnx_signal != sklearn_signal).sum()),
                "side_mismatch_on_signal_count": int(((onnx_side != sklearn_side) & (onnx_signal | sklearn_signal)).sum()),
                "max_score_abs_diff": float(np.abs(onnx_score - sklearn_score).max()) if len(onnx_score) else 0.0,
                "threshold": threshold,
                "passed": bool(
                    int((onnx_signal != sklearn_signal).sum()) == 0
                    and int(((onnx_side != sklearn_side) & (onnx_signal | sklearn_signal)).sum()) == 0
                ),
            }
        )
    return probability_rows, signal_rows


def materialize_candidates(common_files_root: Path, contexts: Sequence[Mapping[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    artifact_rows: list[dict[str, Any]] = []
    probability_rows: list[dict[str, Any]] = []
    signal_rows: list[dict[str, Any]] = []
    local_verification: list[dict[str, Any]] = [
        {"check_name": "grok_clean_output_exists", "status": "passed" if path_exists(GROK_CLEAN) else "failed", "detail": rel(GROK_CLEAN), "effect": "pre-repair Grok review evidence is present"},
        {"check_name": "grok_metadata_exists", "status": "passed" if path_exists(GROK_METADATA) else "failed", "detail": rel(GROK_METADATA), "effect": "Grok wrapper metadata is present"},
    ]
    for context in contexts:
        axis = context["axis"]
        try:
            artifact = export_context_artifacts(context)
            probability, signal = selected_signal_parity_rows(context, artifact)
            probability_ok = all(row.get("passed") for row in probability)
            signal_ok = all(row.get("passed") for row in signal)
            artifact["export_status"] = "exported_selected_entry_tape_parity_passed" if probability_ok and signal_ok else "exported_selected_entry_tape_parity_failed"
            artifact["probability_parity_passed"] = probability_ok
            artifact["signal_parity_passed"] = signal_ok
            artifact["candidate_id_match"] = context["candidate_id_match"]
            if probability_ok and signal_ok:
                model_common = f"{COMMON_RUN_ROOT}/models/{Path(str(artifact['onnx_path'])).name}"
                feature_common = f"{COMMON_RUN_ROOT}/features/{Path(str(artifact['feature_csv_path'])).name}"
                veto_common = f"{COMMON_RUN_ROOT}/runtime_veto_tapes/{Path(str(artifact['runtime_veto_tape_path'])).name}"
                artifact["model_common_path"] = model_common
                artifact["feature_common_path"] = feature_common
                artifact["runtime_veto_tape_common_path"] = veto_common
                artifact["model_common_copy"] = mt5.copy_to_common_files(common_files_root, ROOT / str(artifact["onnx_path"]), model_common)
                artifact["feature_common_copy"] = mt5.copy_to_common_files(common_files_root, ROOT / str(artifact["feature_csv_path"]), feature_common)
                artifact["runtime_veto_tape_common_copy"] = mt5.copy_to_common_files(common_files_root, ROOT / str(artifact["runtime_veto_tape_path"]), veto_common)
            probability_rows.extend(probability)
            signal_rows.extend(signal)
            local_verification.append({"check_name": f"{axis.candidate_id}_selected_entry_tape_parity", "status": "passed" if probability_ok and signal_ok else "failed", "detail": artifact["export_status"], "effect": "selected-entry tape preserves model signal meaning"})
        except Exception as exc:  # noqa: BLE001
            artifact = {
                "candidate_id": axis.candidate_id,
                "axis_id": axis.axis_id,
                "role": axis.role,
                "export_status": "export_or_selected_tape_parity_failed",
                "export_error": f"{type(exc).__name__}: {exc}",
                "probability_parity_passed": False,
                "signal_parity_passed": False,
            }
            local_verification.append({"check_name": f"{axis.candidate_id}_selected_entry_tape_export", "status": "failed", "detail": artifact["export_error"], "effect": "repair blocker recorded"})
        artifact_rows.append(artifact)
    return artifact_rows, probability_rows, signal_rows, local_verification


def build_attempts(contexts: Sequence[Mapping[str, Any]], artifacts: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    context_by_candidate = {context["axis"].candidate_id: context for context in contexts}
    attempts: list[dict[str, Any]] = []
    for artifact in artifacts:
        if artifact.get("export_status") != "exported_selected_entry_tape_parity_passed":
            continue
        context = context_by_candidate[str(artifact["candidate_id"])]
        axis = context["axis"]
        label_spec = context["label_spec"]
        threshold = float(context["threshold"])
        for split_name in f70d.SPLITS:
            split_payload = context["split_payload"][split_name]
            start, end = f70d.split_dates(context["frame"], split_name)
            selected_count = int(np.asarray(split_payload["selected_mask"], dtype=bool).sum())
            attempt_name = f"f70e_{f70d.safe_name(axis.axis_id, 24)}_{axis.candidate_id[-6:]}_{split_name}"
            extra = {
                "InpSameDirectionReentryCooldownBars": int(label_spec.horizon_bars),
                "InpReentryCooldownBars": 0,
                "InpAtrSltpEnabled": True,
                "InpAtrStopMultiplier": float(label_spec.base_tp_atr * 0.85),
                "InpAtrTakeProfitMultiplier": float(label_spec.base_tp_atr * 1.25),
                "InpAtrMinStopPoints": 1.0,
                "InpAtrMinTakeProfitPoints": 1.0,
                "InpDecisionMode": "edge_margin",
                "InpFallbackDecisionMode": "edge_margin",
                "InpRuntimeVetoTapeEnabled": True,
                "InpRuntimeVetoTapePath": str(artifact["runtime_veto_tape_common_path"]),
                "InpRuntimeVetoTapeUseCommonFiles": True,
                "InpRuntimeVetoTapeDelimiter": ",",
            }
            attempt = attempt_payload(
                run_root=RUN_ROOT,
                run_id=RUN_ID,
                stage_number=70,
                exploration_label=f"frontier70E_{axis.axis_id}_selected_entry_repair",
                attempt_name=attempt_name,
                tier=mt5.TIER_A,
                split=split_name,
                model_path=str(artifact["model_common_path"]),
                model_id=f"F70E_{axis.candidate_id}_{axis.axis_id}",
                model_backend="onnx",
                feature_path=str(artifact["feature_common_path"]),
                feature_count=int(len(context["feature_columns"])),
                feature_order_hash=str(context["feature_order_hash"]),
                short_threshold=0.0,
                long_threshold=0.0,
                min_margin=threshold,
                invert_signal=False,
                from_date=start,
                to_date=end,
                primary_active_tier=mt5.TIER_A,
                attempt_role=f"f70e_selected_entry_{axis.role}",
                record_view_prefix=f"mt5_f70e_{f70d.safe_name(axis.axis_id, 24)}_{axis.candidate_id[-6:]}",
                max_hold_bars=int(label_spec.horizon_bars),
                common_root=COMMON_RUN_ROOT,
                close_on_flat_signal=False,
                reverse_on_opposite_signal=True,
                close_only_on_opposite_signal=False,
                extra_set_values=extra,
            )
            attempt.update(
                {
                    "candidate_id": axis.candidate_id,
                    "axis_id": axis.axis_id,
                    "axis_role": axis.role,
                    "expected_rows": split_payload["expected_rows"],
                    "expected_signal_count": selected_count,
                    "expected_selected_trade_count": selected_count,
                    "proxy_kpi": split_payload["proxy_kpi"],
                    "label_id": axis.label_id,
                    "feature_set_id": axis.feature_set_id,
                    "model_id": axis.model_id,
                    "selection_id": axis.selection_id,
                    "mask_name": "selected_entry_only",
                    "threshold": threshold,
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
            attempts.append(attempt)
    return attempts


def compile_runtime_ea(metaeditor_path: Path) -> dict[str, Any]:
    compile_payload = mt5.compile_mql5_ea(metaeditor_path, mt5.EA_SOURCE_PATH, MT5_ROOT / "mt5_compile.log")
    portable_payload = {
        "repo_ea_ex5": rel(EA_BINARY),
        "portable_ea_ex5": PORTABLE_EA_BINARY.as_posix(),
        "portable_ea_ex5_exists_before": path_exists(PORTABLE_EA_BINARY),
        "copied": False,
    }
    if path_exists(EA_BINARY):
        io_path(PORTABLE_EA_BINARY.parent).mkdir(parents=True, exist_ok=True)
        shutil.copy2(io_path(EA_BINARY), io_path(PORTABLE_EA_BINARY))
        portable_payload.update({"copied": True, "portable_ea_ex5_exists_after": path_exists(PORTABLE_EA_BINARY), "portable_ea_sha256": mt5.sha256_file(PORTABLE_EA_BINARY)})
    return {"compile": compile_payload, "portable_ea": portable_payload}


def can_run_terminal(compile_payload: Mapping[str, Any]) -> bool:
    compile_status = ((compile_payload.get("compile") or {}).get("status"))
    return compile_status == "completed" or path_exists(PORTABLE_EA_BINARY)


def execute_attempts(args: argparse.Namespace, attempts: Sequence[Mapping[str, Any]], compile_payload: Mapping[str, Any]) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for attempt in attempts:
        if not can_run_terminal(compile_payload):
            result = {"status": "blocked", "blocker": "compile_failed_and_portable_ea_missing"}
        else:
            f70d.clear_runtime_outputs(Path(args.common_files_root), attempt)
            mt5.remove_existing_mt5_report_artifacts(Path(args.terminal_data_root), attempt, run_id=RUN_ID)
            try:
                result = mt5.run_mt5_tester(
                    Path(args.terminal_path),
                    ROOT / str(attempt["ini"]["path"]),
                    set_path=ROOT / str(attempt["set"]["path"]),
                    tester_profile_set_path=Path(args.tester_profile_root) / mt5.EA_TESTER_SET_NAME,
                    tester_profile_ini_path=Path(args.tester_profile_root) / f"opv2_{attempt['attempt_name']}.ini",
                    timeout_seconds=int(args.timeout_seconds),
                    terminal_extra_args=["/portable"],
                )
            except subprocess.TimeoutExpired as exc:
                result = {"status": "blocked", "command": exc.cmd, "returncode": None, "stdout": (exc.stdout or "")[-2000:], "stderr": (exc.stderr or "")[-2000:], "blocker": "terminal_timeout"}
            runtime_outputs = mt5.wait_for_mt5_runtime_outputs(Path(args.common_files_root), attempt, timeout_seconds=int(args.wait_timeout_seconds), poll_seconds=2.0)
            if runtime_outputs.get("status") != "completed":
                result["status"] = "blocked"
                result.setdefault("blocker", "runtime_outputs_missing_or_init_failed")
            result["runtime_outputs"] = runtime_outputs
        result.update({"attempt_name": attempt["attempt_name"], "tier": attempt["tier"], "split": attempt["split"], "attempt_role": attempt.get("attempt_role"), "record_view_prefix": attempt.get("record_view_prefix"), "candidate_id": attempt.get("candidate_id"), "axis_id": attempt.get("axis_id"), "expected_rows": attempt.get("expected_rows"), "expected_signal_count": attempt.get("expected_signal_count"), "expected_selected_trade_count": attempt.get("expected_selected_trade_count"), "ini_path": attempt.get("ini", {}).get("path"), "set_path": attempt.get("set", {}).get("path")})
        results.append(result)
    return results


def build_summary(payload: Mapping[str, Any]) -> dict[str, Any]:
    receipts = list(payload.get("runtime_receipt") or [])
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "status": payload.get("status"),
        "judgment": payload.get("judgment"),
        "axis_count": len(payload.get("axis_contexts", [])),
        "attempt_count": len(payload.get("attempts", [])),
        "completed_attempt_count": sum(1 for row in receipts if row.get("tester_status") == "completed"),
        "exported_count": sum(1 for row in payload.get("artifact_rows", []) if row.get("export_status") == "exported_selected_entry_tape_parity_passed"),
        "runtime_receipt_rows": len(receipts),
        "next_action": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def grok_identity() -> dict[str, Any]:
    return {
        "packet_root": rel(GROK_PACKET_ROOT),
        "prompt_path": rel(GROK_PROMPT),
        "clean_output_path": rel(GROK_CLEAN),
        "metadata_path": rel(GROK_METADATA),
        "prompt_sha256": f70d.sha256_file(GROK_PROMPT) if path_exists(GROK_PROMPT) else "",
        "clean_output_sha256": f70d.sha256_file(GROK_CLEAN) if path_exists(GROK_CLEAN) else "",
        "advice_classification": "accepted_selected_entry_repair_needs_local_verification",
    }


def run_manifest(payload: Mapping[str, Any], created_at: str) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "created_at_utc": created_at,
        "status": payload.get("status"),
        "judgment": payload.get("judgment"),
        "claim_boundary": CLAIM_BOUNDARY,
        "producer": "stage_pipelines/stage_frontier_70/frontier70e_selected_entry_tape_runtime_repair.py",
        "grok_packet": grok_identity(),
        "repair_boundary": "single-variable RuntimeVetoTape change from regime mask to proxy selected non-overlap entries",
        "axis_specs": [axis.__dict__ for axis in f70d.AXES],
        "artifact_rows": payload.get("artifact_rows", []),
        "attempts": payload.get("attempts", []),
        "summary": build_summary(payload),
        "next_action": NEXT_RUN_ID,
    }


def report_lines(payload: Mapping[str, Any], created_at: str) -> list[str]:
    lines = [
        "# F70E Selected-Entry Tape Runtime Repair(F70E 선택 진입 테이프 런타임 수리)",
        "",
        f"Updated(갱신): {created_at}",
        "",
        "Action(행동): F70D와 같은 모델/피처/임계값을 유지하고 RuntimeVetoTape(런타임 차단 테이프)만 proxy selected non-overlap entries(프록시 선택 비중첩 진입)로 바꿔 MT5 Runtime Probe(MT5 런타임 탐침)를 다시 실행했다.",
        "",
        "Effect(효과): trade_lifecycle_gap_after_signal_parity(신호 동등성 이후 거래 생명주기 간극)가 줄어드는지 관찰한다.",
        "",
        f"- status(상태): `{payload.get('status')}`",
        f"- judgment(판정): `{payload.get('judgment')}`",
        f"- Grok advice(그록 조언): `{grok_identity()['advice_classification']}`",
        f"- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`",
        "",
        "## Runtime KPI(런타임 핵심 성과 지표)",
        "",
        "| axis(축) | split(분할) | net(순수익) | PF(수익 팩터) | DD%(손실폭) | trades(거래) | trades/day(일거래) | expected selected(예상 선택) | signal diff(신호 차이) | feature diff(피처 차이) | gap cause(간극 원인) |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in payload.get("runtime_receipt", []):
        lines.append(
            "| `{axis}` | `{split}` | `{net}` | `{pf}` | `{dd}` | `{trades}` | `{tpd}` | `{expected}` | `{sig}` | `{feat}` | `{gap}` |".format(
                axis=row.get("axis_id"),
                split=row.get("split"),
                net=f70d.fmt(row.get("net_profit")),
                pf=f70d.fmt(row.get("profit_factor")),
                dd=f70d.fmt(row.get("max_drawdown_percent")),
                trades=f70d.fmt(row.get("trade_count")),
                tpd=f70d.fmt(row.get("trades_per_day")),
                expected=f70d.fmt(row.get("expected_selected_trade_count")),
                sig=f70d.fmt(row.get("signal_count_diff")),
                feat=f70d.fmt(row.get("feature_ready_diff")),
                gap=row.get("gap_cause_summary", ""),
            )
        )
    lines.extend(["", f"Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`"])
    return lines


def write_outputs(payload: Mapping[str, Any], created_at: str) -> None:
    f70d.write_json(RUN_ROOT / "frontier70E_runtime_repair_execution_result.json", payload)
    f70d.write_json(RUN_ROOT / "frontier70E_runtime_repair_summary.json", build_summary(payload))
    f70d.write_json(RUN_ROOT / "run_manifest.json", run_manifest(payload, created_at))
    f70d.write_json(RUN_ROOT / "f70e_grok_review_classification.json", grok_identity())
    f70d.write_csv(RUN_ROOT / "f70e_candidate_axis_materialization.csv", payload.get("artifact_rows", []))
    f70d.write_csv(RUN_ROOT / "f70e_onnx_signal_parity.csv", payload.get("signal_parity", []))
    f70d.write_csv(RUN_ROOT / "f70e_runtime_probe_receipt.csv", payload.get("runtime_receipt", []), f70d.RUNTIME_RECEIPT_COLUMNS)
    f70d.write_csv(RUN_ROOT / "f70e_gap_classification.csv", payload.get("gap_classification", []), f70d.GAP_COLUMNS)
    f70d.write_csv(RUN_ROOT / "f70e_local_verification.csv", payload.get("local_verification", []))
    f70d.write_csv(REVIEWS_ROOT / "f70e_candidate_axis_materialization_review.csv", payload.get("artifact_rows", []))
    f70d.write_csv(REVIEWS_ROOT / "f70e_onnx_signal_parity_review.csv", payload.get("signal_parity", []))
    f70d.write_csv(REVIEWS_ROOT / "f70e_runtime_probe_receipt_review.csv", payload.get("runtime_receipt", []), f70d.RUNTIME_RECEIPT_COLUMNS)
    f70d.write_csv(REVIEWS_ROOT / "f70e_gap_classification_review.csv", payload.get("gap_classification", []), f70d.GAP_COLUMNS)
    f70d.write_md(REVIEWS_ROOT / "frontier70E_selected_entry_tape_runtime_repair_report.md", report_lines(payload, created_at))
    f70d.write_md(REVIEWS_ROOT / "required_gate_coverage_audit_f70e.md", gate_audit_lines(payload, created_at))
    f70d.write_md(REVIEWS_ROOT / "f70e_pre_repair_grok_receipt.md", grok_receipt_lines(created_at))


def gate_audit_lines(payload: Mapping[str, Any], created_at: str) -> list[str]:
    summary = build_summary(payload)
    return [
        "# F70E Required Gate Coverage Audit(F70E 필수 게이트 커버리지 감사)",
        "",
        f"- updated_at_utc(갱신): `{created_at}`",
        f"- Grok pre-repair review(그록 수리 전 검토): `{rel(GROK_CLEAN)}`.",
        f"- exported/parity passed(내보내기/동등성 통과): `{summary['exported_count']}`.",
        f"- MT5 attempts(MT5 시도): `{summary['attempt_count']}`.",
        f"- completed attempts(완료 시도): `{summary['completed_attempt_count']}`.",
        "- runtime_authority(런타임 권위): `not_claimed(주장 없음)`.",
        "- Goal Achieve(목표 달성): `not_claimed(주장 없음)`.",
    ]


def grok_receipt_lines(created_at: str) -> list[str]:
    return [
        "# F70E Pre-Repair Grok Receipt(F70E 수리 전 그록 영수증)",
        "",
        f"- created_at_utc(생성): `{created_at}`",
        "- trigger_reason(트리거 이유): MT5 Runtime Probe repair(MT5 런타임 탐침 수리) 전 second opinion(2차 의견).",
        f"- prompt_identity(프롬프트 정체성): `{rel(GROK_PROMPT)}`, sha256 `{f70d.sha256_file(GROK_PROMPT) if path_exists(GROK_PROMPT) else ''}`.",
        f"- grok_output_identity(그록 출력 정체성): `{rel(GROK_CLEAN)}`, sha256 `{f70d.sha256_file(GROK_CLEAN) if path_exists(GROK_CLEAN) else ''}`.",
        "- advice_classification(조언 분류): `accepted(수용)` plus `needs_local_verification(로컬 검증 필요)` for selected-entry tape materialization fidelity(선택 진입 테이프 물질화 충실도).",
        "- accepted(수용): single-variable RuntimeVetoTape semantics repair(단일 변수 런타임 차단 테이프 의미 수리).",
        "- guardrail(보호 조건): no threshold/model sweep(임계값/모델 탐색 없음), same two axes(같은 두 축), close F70 after F70E unless a new explicit hypothesis is opened(새 명시 가설 없으면 F70E 뒤 마감).",
        f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`.",
    ]


def best_receipt(payload: Mapping[str, Any]) -> Mapping[str, Any]:
    receipts = [row for row in payload.get("runtime_receipt", []) if row.get("split") == "oos"]
    if not receipts:
        receipts = list(payload.get("runtime_receipt", []))
    return max(receipts, key=lambda row: f70d.as_float(row.get("profit_factor")) or -999.0) if receipts else {}


def update_state_and_ledgers(payload: Mapping[str, Any], created_at: str) -> None:
    summary = build_summary(payload)
    best = best_receipt(payload)
    row = {
        "ledger_row_id": f"{RUN_ID}__runtime_repair",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "selected_entry_tape_runtime_repair(선택 진입 테이프 런타임 수리)",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "mt5_runtime_repair_observation(MT5 런타임 수리 관찰)",
        "tier_scope": "Tier A separate(Tier A 분리)",
        "kpi_scope": "runtime_repair_kpi_and_proxy_gap(런타임 수리 KPI와 프록시 간극)",
        "scoreboard_lane": "runtime_probe(런타임 탐침)",
        "status": payload.get("status"),
        "judgment": payload.get("judgment"),
        "path": rel(REVIEWS_ROOT / "frontier70E_selected_entry_tape_runtime_repair_report.md"),
        "primary_kpi": f"attempts={summary['attempt_count']};completed_attempts={summary['completed_attempt_count']};exported={summary['exported_count']}",
        "guardrail_kpi": "single_variable_tape_repair;no threshold/model sweep",
        "external_verification_status": "completed(완료)" if summary["completed_attempt_count"] else "blocked(차단)",
        "run_number": "frontier70E",
        "date": created_at[:10],
        "decision": "proceed_to_f70_stage_closeout_review",
        "next_run_id": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REVIEWS_ROOT / "frontier70E_selected_entry_tape_runtime_repair_report.md"),
        "trained_models": summary["axis_count"],
        "onnx_parity": summary["exported_count"],
        "best_proxy": best.get("candidate_id", ""),
        "candidate_rows": summary["axis_count"],
        "best_model_id": best.get("axis_id", ""),
        "run_date": created_at[:10],
        "primary_artifact": rel(RUN_ROOT / "frontier70E_runtime_repair_execution_result.json"),
        "net_profit": f70d.fmt(best.get("net_profit")),
        "profit_factor": f70d.fmt(best.get("profit_factor")),
        "drawdown": f70d.fmt(best.get("max_drawdown_percent")),
        "trade_count": f70d.fmt(best.get("trade_count")),
        "result_status": payload.get("status"),
        "family": "runtime_validation(런타임 검증)",
        "primary_report": rel(REVIEWS_ROOT / "frontier70E_selected_entry_tape_runtime_repair_report.md"),
        "attempt_count": summary["attempt_count"],
        "row_id": f"{RUN_ID}__runtime_repair",
        "evidence_boundary": "runtime_repair_observation_only(런타임 수리 관찰 전용)",
        "work_family": "runtime_validation(런타임 검증)",
        "evidence_scope": "mt5_runtime_repair(MT5 런타임 수리)",
        "run_key": RUN_ID,
        "question": "Does selected-entry tape align runtime trades with proxy selected entries?(선택 진입 테이프가 런타임 거래를 프록시 선택 진입과 맞추는가)",
        "next_action": NEXT_RUN_ID,
        "result_judgment": payload.get("judgment"),
        "final_decision_path": rel(REVIEWS_ROOT / "frontier70E_selected_entry_tape_runtime_repair_report.md"),
        "created_at": created_at,
        "gate_audit_path": rel(REVIEWS_ROOT / "required_gate_coverage_audit_f70e.md"),
        "created_at_utc": created_at,
        "required_gate_audit": rel(REVIEWS_ROOT / "required_gate_coverage_audit_f70e.md"),
        "kpi_summary": f"attempts={summary['attempt_count']};completed={summary['completed_attempt_count']};runtime_rows={summary['runtime_receipt_rows']}",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "trade_density": f70d.fmt(best.get("trades_per_day")),
        "source_authority": "runtime_repair_observation_no_authority(런타임 수리 관찰, 권위 없음)",
        "goal_achieve": "not_claimed",
        "run_family": "frontier_runtime_repair(전선 런타임 수리)",
        "run_type": "selected_entry_tape_runtime_repair(선택 진입 테이프 런타임 수리)",
        "input_run_id": PARENT_RUN_ID,
        "output_path": rel(RUN_ROOT / "frontier70E_runtime_repair_execution_result.json"),
        "result_path": rel(REVIEWS_ROOT / "frontier70E_selected_entry_tape_runtime_repair_report.md"),
        "selected_net_profit": f70d.fmt(best.get("net_profit")),
        "selected_profit_factor": f70d.fmt(best.get("profit_factor")),
        "selected_trade_density": f70d.fmt(best.get("trades_per_day")),
        "max_drawdown_percent": f70d.fmt(best.get("max_drawdown_percent")),
        "strict_joint_pass_count": 0,
    }
    f70d.upsert_ledger(REVIEWS_ROOT / "stage_run_ledger.csv", "ledger_row_id", row, source_header=ROOT / "docs/registers/alpha_run_ledger.csv")
    f70d.upsert_ledger(ROOT / "docs/registers/alpha_run_ledger.csv", "ledger_row_id", row)
    f70d.upsert_ledger(ROOT / "docs/registers/run_registry.csv", "run_id", row)
    write_state(payload, created_at, summary, best)


def write_state(payload: Mapping[str, Any], created_at: str, summary: Mapping[str, Any], best: Mapping[str, Any]) -> None:
    workspace_lines = [
        f"current_stage_id: {STAGE_ID}",
        f"active_stage: {STAGE_ID}",
        f"current_run_id: {NEXT_RUN_ID}",
        f"latest_completed_run_id: {RUN_ID}",
        f"current_status: {payload.get('status')}",
        f"current_judgment: {payload.get('judgment')}",
        f"next_stage_id: {STAGE_ID}",
        f"next_run_id: {NEXT_RUN_ID}",
        "runtime_probe_status: f70_runtime_repair_probe_completed_observation_no_authority(F70 런타임 수리 탐침 완료 관찰, 권위 없음)",
        "runtime_authority: not_claimed",
        "operating_promotion: not_claimed",
        "live_readiness: not_claimed",
        "goal_achieve: not_claimed",
        "five_stage_retrospective_due_status: due_at_f70_closeout",
        f"updated_at_utc: '{created_at}'",
        "notes:",
        f'  - "F70E action(행동): selected-entry RuntimeVetoTape repair(선택 진입 런타임 차단 테이프 수리)를 실행했다."',
        f'  - "Effect(효과): attempts(시도) `{summary["attempt_count"]}`, completed_attempts(완료 시도) `{summary["completed_attempt_count"]}`, runtime_receipt_rows(런타임 영수증 행) `{summary["runtime_receipt_rows"]}`를 기록했다."',
        f'  - "Representative runtime OOS net/PF/DD/trades_day(대표 런타임 표본외 순수익/수익 팩터/손실폭/일거래): `{f70d.fmt(best.get("net_profit"))}/{f70d.fmt(best.get("profit_factor"))}/{f70d.fmt(best.get("max_drawdown_percent"))}/{f70d.fmt(best.get("trades_per_day"))}`."',
        f'  - "Next action(다음 행동): `{NEXT_RUN_ID}`에서 Grok closeout review(그록 마감 검토)와 F70 closeout(마감)을 진행한다."',
        '  - "Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음)."',
    ]
    io_path(ROOT / "docs/workspace/workspace_state.yaml").write_text("\n".join(workspace_lines) + "\n", encoding="utf-8-sig")
    current_lines = [
        "# Current Working State(현재 작업 상태)",
        "",
        f"Updated(갱신): {created_at}",
        "",
        f"Active stage(활성 단계): `{STAGE_ID}`",
        f"Current run(현재 실행): `{NEXT_RUN_ID}`",
        f"Latest completed run(최근 완료 실행): `{RUN_ID}`",
        "",
        "## Current Truth(현재 진실)",
        "",
        "Action(행동): F70E selected-entry tape runtime repair(F70E 선택 진입 테이프 런타임 수리)를 실행했다.",
        "",
        "Effect(효과): F70D의 거래 과잉이 proxy selected entries(프록시 선택 진입)와 runtime entries(런타임 진입)의 의미 차이 때문인지 확인할 근거를 만들었다.",
        "",
        f"- status(상태): `{payload.get('status')}`.",
        f"- judgment(판정): `{payload.get('judgment')}`.",
        f"- attempts/completed(시도/완료): `{summary['attempt_count']}` / `{summary['completed_attempt_count']}`.",
        f"- representative OOS net/PF/DD/trades_day(대표 표본외 순수익/수익 팩터/손실폭/일거래): `{f70d.fmt(best.get('net_profit'))}` / `{f70d.fmt(best.get('profit_factor'))}` / `{f70d.fmt(best.get('max_drawdown_percent'))}` / `{f70d.fmt(best.get('trades_per_day'))}`.",
        "",
        f"Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`",
    ]
    f70d.write_md(ROOT / "docs/context/current_working_state.md", current_lines)
    selection_lines = [
        "# F70 Selection Status(F70 선택 상태)",
        "",
        f"- stage(단계): `{STAGE_ID}`",
        f"- current_run(현재 실행): `{NEXT_RUN_ID}`",
        f"- latest_completed_run(최근 완료 실행): `{RUN_ID}`",
        f"- status(상태): `{payload.get('status')}`",
        f"- judgment(판정): `{payload.get('judgment')}`",
        "- selected_baseline(선택 기준선): `not_claimed(주장 없음)`",
        "- runtime_authority(런타임 권위): `not_claimed(주장 없음)`",
        "- operating_promotion(운영 승격): `not_claimed(주장 없음)`",
        "- live_readiness(실거래 준비): `not_claimed(주장 없음)`",
        "- Goal Achieve(목표 달성): `not_claimed(주장 없음)`",
        f"- completed_action(완료 행동): `{RUN_ID}` selected-entry tape runtime repair(선택 진입 테이프 런타임 수리).",
        f"- report(보고서): `stages/{STAGE_ID}/03_reviews/frontier70E_selected_entry_tape_runtime_repair_report.md`",
        f"- next_action(다음 행동): `{NEXT_RUN_ID}`.",
        f"- boundary(경계): `{CLAIM_BOUNDARY}`.",
    ]
    f70d.write_md(STAGE_ROOT / "04_selected" / "selection_status.md", selection_lines)
    f70d.append_once(
        ROOT / "docs/registers/idea_registry.md",
        f"{RUN_ID} executed",
        f"""### {RUN_ID}

- {RUN_ID} executed(실행): selected-entry RuntimeVetoTape repair(선택 진입 런타임 차단 테이프 수리)를 MT5 Runtime Probe(MT5 런타임 탐침)로 실행했다. Status(상태): `{payload.get('status')}`. Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음). Next(다음): `{NEXT_RUN_ID}`.
""",
    )


def main() -> int:
    args = parse_args()
    ensure_dirs()
    created_at = utc_now()
    contexts = f70d.build_axis_contexts()
    artifact_rows, probability_rows, signal_rows, local_verification = materialize_candidates(Path(args.common_files_root), contexts)
    attempts = build_attempts(contexts, artifact_rows)
    payload: dict[str, Any] = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "created_at_utc": created_at,
        "status": STATUS_MATERIALIZED,
        "judgment": "selected_entry_tape_repair_materialized_pending_mt5_no_authority",
        "claim_boundary": CLAIM_BOUNDARY,
        "grok_packet": grok_identity(),
        "axis_contexts": [{"axis": context["axis"].__dict__, "threshold": context["threshold"], "candidate_id_match": context["candidate_id_match"]} for context in contexts],
        "artifact_rows": artifact_rows,
        "probability_parity": probability_rows,
        "signal_parity": signal_rows,
        "local_verification": local_verification,
        "attempts": attempts,
        "execution_results": [],
        "strategy_tester_reports": [],
        "mt5_kpi_records": [],
        "runtime_receipt": [],
        "gap_classification": [],
    }
    if args.materialize_only or not args.execute:
        write_outputs(payload, created_at)
        print(json.dumps(json_ready({"status": payload["status"], "attempt_count": len(attempts)}), ensure_ascii=False, indent=2))
        return 0

    compile_payload = compile_runtime_ea(Path(args.metaeditor_path))
    payload["compile_payload"] = compile_payload
    execution_results = execute_attempts(args, attempts, compile_payload)
    report_records = mt5.collect_mt5_strategy_report_artifacts(terminal_data_root=Path(args.terminal_data_root), run_output_root=RUN_ROOT, attempts=attempts, run_id=RUN_ID)
    mt5.attach_mt5_report_metrics(execution_results, report_records)
    kpi_records = mt5.build_mt5_kpi_records(execution_results)
    receipt_rows = f70d.build_runtime_receipt(execution_results, attempts)
    for row in receipt_rows:
        row["run_id"] = RUN_ID
        row["claim_boundary"] = CLAIM_BOUNDARY
    gap_rows = [gap for receipt in receipt_rows for gap in f70d.build_gap_classification(receipt)]
    for row in gap_rows:
        row["run_id"] = RUN_ID
        row["claim_boundary"] = CLAIM_BOUNDARY
    execution_completed = bool(execution_results) and any(row.get("status") == "completed" for row in execution_results)
    report_completed = bool(kpi_records)
    payload.update(
        {
            "status": STATUS_COMPLETED if execution_completed and report_completed else STATUS_BLOCKED,
            "judgment": "selected_entry_tape_runtime_repair_observation_recorded_no_authority" if execution_completed and report_completed else "selected_entry_tape_runtime_repair_blocked_no_authority",
            "execution_results": execution_results,
            "strategy_tester_reports": report_records,
            "mt5_kpi_records": kpi_records,
            "runtime_receipt": receipt_rows,
            "gap_classification": gap_rows,
        }
    )
    write_outputs(payload, created_at)
    update_state_and_ledgers(payload, created_at)
    print(json.dumps(json_ready({"status": payload["status"], "judgment": payload["judgment"], "attempt_count": len(attempts), "completed_attempt_count": build_summary(payload)["completed_attempt_count"], "runtime_receipt_rows": len(receipt_rows), "next_action": NEXT_RUN_ID}), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
