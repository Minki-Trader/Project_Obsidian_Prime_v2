from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import os
import shutil
import subprocess
import sys
import time
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import numpy as np
import onnx
import onnxruntime as ort
import pandas as pd
from onnx import TensorProto, helper


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.mt5_kpi_records import TIER_A, build_mt5_kpi_records  # noqa: E402
from foundation.control_plane.mt5_tier_balance_completion import (  # noqa: E402
    COMMON_FILES_ROOT_DEFAULT,
    METAEDITOR_PATH_DEFAULT,
    TERMINAL_DATA_ROOT_DEFAULT,
    TERMINAL_PATH_DEFAULT,
    TESTER_PROFILE_ROOT_DEFAULT,
)
from foundation.models.onnx_bridge import ordered_hash  # noqa: E402
from foundation.mt5 import runtime_support as mt5  # noqa: E402


STAGE_ID = "333_overfit_guard__timestamp_safe_pocket_veto_materialization"
RUN_NUMBER = "run333E"
RUN_ID = "run333E_runtime_probe_queue_or_failure_memory_from_screen_v1"
PARENT_RUN_ID = "run333D_screen_guarded_payload_cost_curve_and_pocket_risk_v1"
NEXT_COMPLETED = "run333F_review_signal_replay_mt5_forensics_and_packaging_boundary_v1"
NEXT_BLOCKED = "repair_run333E_signal_replay_runtime_blocker_then_rerun"
STATUS_COMPLETED = "completed_signal_payload_runtime_replay_mt5_probe_no_forward_decision"
STATUS_BLOCKED = "blocked_signal_payload_runtime_replay_mt5_probe_no_completed_runtime"
STATUS_MATERIALIZED = "materialized_signal_payload_runtime_replay_contract_no_external_runtime_execution"
JUDGMENT_COMPLETED = "signal_payload_runtime_probe_completed_research_only_no_goal_achieve"
JUDGMENT_BLOCKED = "signal_payload_runtime_probe_blocked_requires_runtime_repair_no_goal_achieve"
DECISION_COMPLETED = "stage333E_signal_payload_mt5_evidence_available_review_required_no_selection"
DECISION_BLOCKED = "stage333E_signal_payload_runtime_probe_blocked_no_pass_fail_judgment"
CLAIM_BOUNDARY = (
    "research_development_only_signal_payload_runtime_replay_bridge_no_threshold_retuning_"
    "no_lot_optimization_no_candidate_model_update_no_candidate_selection_no_forward_passed_"
    "no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)

COMMON_ROOT = "Project_Obsidian_Prime_v2/stage333/run333E_signal_payload_runtime_replay"
EXPLORATION_LABEL = "stage333_Runtime__SignalPayloadReplayBridge"
SPLIT_LABEL = "raw_forward_signal_payload_replay"
MAX_HOLD_BARS = 12
FIXED_LOT = 0.1
FEATURE_NAMES = ["p_short", "p_flat", "p_long"]
FEATURE_ORDER_HASH = ordered_hash(FEATURE_NAMES)
TODAY = "2026-05-26"

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REPLAY_DIR = RUN_DIR / "signal_replay_bridge"
ONNX_DIR = RUN_DIR / "onnx"
MT5_DIR = RUN_DIR / "mt5"
REVIEWS_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"

RUN330B_DIR = ROOT / "stages" / "330_onnx_rebuild__forward_safe_non_identity_surface_robustness" / "02_runs" / "run330B"
RUN330E_DIR = ROOT / "stages" / "330_onnx_rebuild__forward_safe_non_identity_surface_robustness" / "02_runs" / "run330E"
RUN332E_DIR = ROOT / "stages" / "332_overfit_guard__failure_memory_forward_research_handoff" / "02_runs" / "run332E"
RUN333C_DIR = STAGE_DIR / "02_runs" / "run333C"
RUN333D_DIR = STAGE_DIR / "02_runs" / "run333D"

RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
STAGE_LEDGER = REVIEWS_DIR / "stage_run_ledger.csv"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
SELECTION_STATUS = SELECTED_DIR / "selection_status.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-26_stage333E_signal_payload_runtime_probe_or_block.md"


def io_path(path: Path) -> Path:
    resolved = path.resolve()
    if os.name == "nt":
        text = str(resolved)
        if len(text) > 240 and not text.startswith("\\\\?\\"):
            return Path("\\\\?\\" + text)
    return resolved


def path_exists(path: Path) -> bool:
    try:
        return io_path(path).exists()
    except OSError:
        return False


def rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with io_path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def json_ready(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): json_ready(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_ready(item) for item in value]
    if isinstance(value, Path):
        return rel(value)
    if isinstance(value, pd.Timestamp):
        return value.isoformat()
    if hasattr(value, "item"):
        try:
            return json_ready(value.item())
        except Exception:
            return str(value)
    if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
        return None
    return value


def csv_value(value: Any) -> Any:
    if value is None:
        return ""
    if isinstance(value, float):
        if math.isnan(value) or math.isinf(value):
            return ""
        return round(value, 10)
    if isinstance(value, pd.Timestamp):
        if value.tzinfo is not None:
            value = value.tz_convert("UTC").tz_localize(None)
        return value.strftime("%Y-%m-%d %H:%M:%S")
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(json_ready(value), ensure_ascii=False, sort_keys=True)
    return value


def write_csv(path: Path, columns: Sequence[str], rows: Iterable[Mapping[str, Any]]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: csv_value(row.get(column)) for column in columns})
    return path


def write_json(path: Path, payload: Any) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8") as handle:
        json.dump(json_ready(payload), handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    return path


def write_text(path: Path, text: str, *, encoding: str = "utf-8") -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding=encoding, newline="\n") as handle:
        handle.write(text)
    return path


def write_md(path: Path, text: str) -> Path:
    return write_text(path, text.strip() + "\n", encoding="utf-8-sig")


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path_exists(path):
        return []
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def read_text_lossless(path: Path) -> tuple[str, bool]:
    raw = io_path(path).read_bytes()
    return raw.decode("utf-8-sig"), raw.startswith(b"\xef\xbb\xbf")


def write_text_lossless(path: Path, text: str, had_bom: bool) -> Path:
    encoding = "utf-8-sig" if had_bom else "utf-8"
    with io_path(path).open("w", encoding=encoding, newline="\n") as handle:
        handle.write(text)
    return path


def replace_prefix_line(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            return "\n".join(lines) + ("\n" if text.endswith("\n") else "")
    return text.rstrip() + "\n" + replacement + "\n"


def replace_line_containing(text: str, marker: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if marker in line:
            lines[index] = replacement
            return "\n".join(lines) + ("\n" if text.endswith("\n") else "")
    return text


def append_if_missing(path: Path, marker: str, block: str) -> Path:
    text, had_bom = read_text_lossless(path)
    if marker not in text:
        text = text.rstrip() + "\n\n" + block.strip() + "\n"
        write_text_lossless(path, text, had_bom)
    return path


def upsert_csv(path: Path, keys: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    existing: list[dict[str, Any]] = []
    fieldnames: list[str] = []
    if path_exists(path):
        with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = list(reader.fieldnames or [])
            existing = [dict(row) for row in reader]
    for row in rows:
        for key in row.keys():
            if key not in fieldnames:
                fieldnames.append(key)
    indexed = {tuple(str(row.get(key, "")) for key in keys): dict(row) for row in existing}
    for row in rows:
        indexed[tuple(str(row.get(key, "")) for key in keys)] = dict(row)
    return write_csv(path, fieldnames, indexed.values())


def mt5_value(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, float):
        return f"{value:.12g}"
    return str(value)


def write_set(path: Path, values: Mapping[str, Any]) -> dict[str, Any]:
    lines = ["; generated_by=stage_pipelines.stage333.runtime_probe_queue_or_failure_memory_from_screen"]
    lines.extend(f"{key}={mt5_value(value)}" for key, value in values.items())
    write_text(path, "\n".join(lines) + "\n")
    return {"path": rel(path), "sha256": sha256_file(path), "format": "mt5_set", "parameter_count": len(values)}


def write_ini(path: Path, values: Mapping[str, Any]) -> dict[str, Any]:
    lines = ["[Tester]"]
    lines.extend(f"{key}={mt5_value(value)}" for key, value in values.items())
    write_text(path, "\n".join(lines) + "\n")
    return {"path": rel(path), "sha256": sha256_file(path), "format": "mt5_tester_ini", "tester": dict(values)}


def copy_to_common(local_path: Path, common_files_root: Path, common_path: str) -> dict[str, Any]:
    destination = common_files_root / Path(common_path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(io_path(local_path), io_path(destination))
    return {
        "source": rel(local_path),
        "common_path": common_path,
        "absolute_path": destination.as_posix(),
        "sha256": sha256_file(destination),
    }


def make_identity_probability_onnx(path: Path) -> dict[str, Any]:
    path.parent.mkdir(parents=True, exist_ok=True)
    input_info = helper.make_tensor_value_info("input", TensorProto.FLOAT, [None, 3])
    output_info = helper.make_tensor_value_info("probabilities", TensorProto.FLOAT, [None, 3])
    node = helper.make_node("Identity", inputs=["input"], outputs=["probabilities"])
    graph = helper.make_graph([node], "stage333_signal_payload_identity_probability_bridge", [input_info], [output_info])
    model = helper.make_model(
        graph,
        producer_name="stage333_signal_payload_runtime_replay_bridge",
        opset_imports=[helper.make_operatorsetid("", 12)],
    )
    model.ir_version = 7
    onnx.checker.check_model(model)
    onnx.save(model, io_path(path))
    return {"path": rel(path), "sha256": sha256_file(path), "format": "onnx_identity_probability_bridge", "feature_count": 3}


def decision_signal(p_short: float, p_flat: float, p_long: float, threshold: float) -> int:
    short_margin = p_short - max(p_flat, p_long)
    long_margin = p_long - max(p_flat, p_short)
    short_ok = p_short >= 0.0 and short_margin >= threshold
    long_ok = p_long >= 0.0 and long_margin >= threshold
    if long_ok and (not short_ok or p_long >= p_short):
        return 1
    if short_ok:
        return -1
    return 0


def tester_dates(timestamps: pd.Series) -> tuple[str, str]:
    parsed = pd.to_datetime(timestamps, utc=True)
    start = parsed.min().date()
    end = parsed.max().date() + timedelta(days=1)
    return start.strftime("%Y.%m.%d"), end.strftime("%Y.%m.%d")


def load_single_queue() -> dict[str, str]:
    rows = read_csv_rows(RUN333D_DIR / "runtime_probe_branch_queue.csv")
    if len(rows) != 1:
        raise RuntimeError(f"run333D runtime probe queue expected 1 row, found {len(rows)}")
    return rows[0]


def load_payload_manifest(queue_id: str) -> dict[str, str]:
    rows = [row for row in read_csv_rows(RUN333C_DIR / "payload_manifest.csv") if row.get("queue_id") == queue_id]
    if len(rows) != 1:
        raise RuntimeError(f"run333C payload_manifest row expected 1 for {queue_id}, found {len(rows)}")
    return rows[0]


def load_source_prediction(source_artifact: str) -> tuple[pd.DataFrame, dict[str, str]]:
    rows = [
        row
        for row in read_csv_rows(RUN330B_DIR / "signal_payload_manifest.csv")
        if row.get("artifact_slug") == source_artifact and row.get("view_id") == "raw_forward"
    ]
    if len(rows) != 1:
        raise RuntimeError(f"run330B raw_forward source manifest expected 1 row for {source_artifact}, found {len(rows)}")
    manifest = rows[0]
    prediction = pd.read_parquet(io_path(ROOT / manifest["prediction_path"]))
    prediction["timestamp"] = pd.to_datetime(prediction["timestamp"], utc=True)
    return prediction.sort_values("timestamp").reset_index(drop=True), manifest


def build_replay_frame(queue: Mapping[str, str], payload_manifest: Mapping[str, str]) -> tuple[pd.DataFrame, dict[str, Any]]:
    prediction, source_manifest = load_source_prediction(str(queue["source_artifact"]))
    scored_path = ROOT / str(payload_manifest["scored_payload_path"])
    signal_path = ROOT / str(payload_manifest["signal_payload_path"])
    scored = pd.read_csv(io_path(scored_path))
    scored["timestamp"] = pd.to_datetime(scored["timestamp_utc"], utc=True)
    scored = scored.sort_values("timestamp").reset_index(drop=True)

    merged = prediction.merge(
        scored[["timestamp", "view_signal_allowed_flag", "guard_score_valid_flag", "guard_score_missing_flag"]],
        on="timestamp",
        how="left",
        validate="one_to_one",
    )
    if len(merged) != len(prediction):
        raise RuntimeError("prediction/scored merge changed row count")
    if merged["view_signal_allowed_flag"].isna().any():
        raise RuntimeError("scored payload missing timestamps required for replay bridge")

    allowed = pd.to_numeric(merged["view_signal_allowed_flag"], errors="coerce").fillna(0).astype(int) == 1
    source_nonflat = pd.to_numeric(merged["signal"], errors="coerce").fillna(0).astype(int) != 0
    forced_flat = source_nonflat & ~allowed
    p_short = pd.to_numeric(merged["p_short"], errors="coerce").astype("float64")
    p_flat = pd.to_numeric(merged["p_flat"], errors="coerce").astype("float64")
    p_long = pd.to_numeric(merged["p_long"], errors="coerce").astype("float64")
    p_short.loc[forced_flat] = 0.0
    p_flat.loc[forced_flat] = 1.0
    p_long.loc[forced_flat] = 0.0
    threshold = float(source_manifest["threshold"])
    replay_signal = [
        decision_signal(float(a), float(b), float(c), threshold)
        for a, b, c in zip(p_short.to_numpy(), p_flat.to_numpy(), p_long.to_numpy(), strict=True)
    ]
    replay = pd.DataFrame(
        {
            "timestamp": merged["timestamp"],
            "bar_time_server": merged["timestamp"].dt.strftime("%Y.%m.%d %H:%M:%S"),
            "timestamp_utc": merged["timestamp"].dt.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "row_index": np.arange(len(merged), dtype="int64"),
            "p_short": p_short.astype("float32"),
            "p_flat": p_flat.astype("float32"),
            "p_long": p_long.astype("float32"),
            "source_signal": pd.to_numeric(merged["signal"], errors="coerce").fillna(0).astype(int),
            "replay_signal": replay_signal,
            "view_signal_allowed_flag": allowed.astype(int),
            "forced_flat_by_guard": forced_flat.astype(int),
            "guard_score_valid_flag": pd.to_numeric(merged["guard_score_valid_flag"], errors="coerce").fillna(0).astype(int),
            "guard_score_missing_flag": pd.to_numeric(merged["guard_score_missing_flag"], errors="coerce").fillna(0).astype(int),
        }
    )
    nonfinite = ~np.isfinite(replay[FEATURE_NAMES].to_numpy(dtype="float64"))
    if bool(nonfinite.any()):
        raise RuntimeError("replay probability bridge contains non-finite values")

    signal_payload = pd.read_csv(io_path(signal_path))
    signal_payload["timestamp"] = pd.to_datetime(signal_payload["timestamp"], utc=True)
    expected = replay.loc[replay["replay_signal"] != 0, ["timestamp", "replay_signal"]].copy()
    actual = signal_payload[["timestamp", "signal_direction"]].copy()
    actual["signal_direction"] = pd.to_numeric(actual["signal_direction"], errors="coerce").astype(int)
    matched = (
        len(expected) == len(actual)
        and expected["timestamp"].reset_index(drop=True).equals(actual["timestamp"].reset_index(drop=True))
        and expected["replay_signal"].reset_index(drop=True).equals(actual["signal_direction"].reset_index(drop=True))
    )
    diagnostics = {
        "source_prediction_path": source_manifest["prediction_path"],
        "source_prediction_sha256": source_manifest["prediction_sha256"],
        "source_signal_payload_path": source_manifest["signal_payload_path"],
        "source_signal_payload_sha256": source_manifest["signal_payload_sha256"],
        "guarded_signal_payload_path": payload_manifest["signal_payload_path"],
        "guarded_signal_payload_sha256": payload_manifest["signal_payload_sha256"],
        "scored_payload_path": payload_manifest["scored_payload_path"],
        "scored_payload_sha256": payload_manifest["scored_payload_sha256"],
        "rows": int(len(replay)),
        "source_signal_rows": int(source_nonflat.sum()),
        "guarded_signal_rows": int(len(actual)),
        "replay_nonflat_rows": int((replay["replay_signal"] != 0).sum()),
        "forced_flat_rows": int(forced_flat.sum()),
        "threshold": threshold,
        "signal_payload_parity_matched": bool(matched),
        "first_timestamp": replay["timestamp"].min().isoformat(),
        "last_timestamp": replay["timestamp"].max().isoformat(),
        "candidate_id": str(prediction["candidate_id"].iloc[0]),
        "artifact_slug": str(prediction["artifact_slug"].iloc[0]),
        "feature_set_id": str(prediction["feature_set_id"].iloc[0]),
        "model_id": str(prediction["model_id"].iloc[0]),
    }
    if not matched:
        raise RuntimeError("runtime replay feature bridge does not reproduce guarded signal payload exactly")
    return replay, diagnostics


def write_replay_feature_csv(path: Path, replay: pd.DataFrame) -> dict[str, Any]:
    payload = replay[["bar_time_server", "timestamp_utc", "row_index", *FEATURE_NAMES]].copy()
    path.parent.mkdir(parents=True, exist_ok=True)
    payload.to_csv(io_path(path), index=False, encoding="utf-8", float_format="%.10g", lineterminator="\n")
    return {
        "path": rel(path),
        "sha256": sha256_file(path),
        "rows": int(len(payload)),
        "feature_count": len(FEATURE_NAMES),
        "feature_order_hash": FEATURE_ORDER_HASH,
        "format": "probability_identity_bridge_features_all_runtime_rows",
    }


def onnxruntime_identity_check(onnx_path: Path, replay: pd.DataFrame) -> dict[str, Any]:
    session = ort.InferenceSession(str(io_path(onnx_path)), providers=["CPUExecutionProvider"])
    input_name = session.get_inputs()[0].name
    sample = replay[FEATURE_NAMES].head(25).to_numpy(dtype=np.float32)
    outputs = session.run(None, {input_name: sample})[0]
    max_abs_diff = float(np.max(np.abs(outputs - sample))) if len(sample) else 0.0
    return {
        "provider": "onnxruntime_CPUExecutionProvider",
        "sample_rows": int(len(sample)),
        "input_name": input_name,
        "output_shape": list(outputs.shape),
        "max_abs_diff": max_abs_diff,
        "status": "completed" if max_abs_diff <= 1e-7 else "blocked",
    }


def build_failure_memory(decision_rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for row in decision_rows:
        decision = str(row.get("screen_decision", ""))
        if decision == "screen_survived_proxy_guard_runtime_probe_design_only":
            continue
        if decision == "baseline_reference_not_candidate":
            memory_type = "baseline_reference_not_candidate"
        else:
            memory_type = "failure_memory_no_candidate_language"
        output.append(
            {
                "queue_id": row.get("queue_id"),
                "thesis_id": row.get("thesis_id"),
                "source_artifact": row.get("source_artifact"),
                "scoring_mode": row.get("scoring_mode"),
                "screen_decision": decision,
                "memory_type": memory_type,
                "net_profit": row.get("net_profit"),
                "profit_factor": row.get("profit_factor"),
                "max_drawdown": row.get("max_drawdown"),
                "cost2_pf": row.get("cost2_pf"),
                "rolling20_min_net": row.get("rolling20_min_net"),
                "rolling40_min_net": row.get("rolling40_min_net"),
                "reuse_rule": "do_not_promote_from_proxy_screen;only_reopen_if_new_runtime_or_nonretuned_guard_evidence_exists",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return output


def materialize_attempt(common_files_root: Path) -> tuple[dict[str, Any], list[dict[str, Any]], list[Path]]:
    queue = load_single_queue()
    payload_manifest = load_payload_manifest(str(queue["queue_id"]))
    replay, diagnostics = build_replay_frame(queue, payload_manifest)

    replay_feature_path = REPLAY_DIR / "m48_breadth_soft_veto_probability_bridge_features.csv"
    replay_export = write_replay_feature_csv(replay_feature_path, replay)
    replay_audit_path = RUN_DIR / "signal_replay_preflight_audit.csv"
    write_csv(
        replay_audit_path,
        [
            "queue_id",
            "source_artifact",
            "rows",
            "source_signal_rows",
            "guarded_signal_rows",
            "replay_nonflat_rows",
            "forced_flat_rows",
            "threshold",
            "signal_payload_parity_matched",
            "first_timestamp",
            "last_timestamp",
            "claim_boundary",
        ],
        [
            {
                **diagnostics,
                "queue_id": queue["queue_id"],
                "source_artifact": queue["source_artifact"],
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )

    onnx_path = ONNX_DIR / "signal_payload_identity_probability_bridge.onnx"
    bridge_onnx = make_identity_probability_onnx(onnx_path)
    onnx_check = onnxruntime_identity_check(onnx_path, replay)
    onnx_check_path = RUN_DIR / "identity_bridge_onnxruntime_check.json"
    write_json(onnx_check_path, onnx_check)
    if onnx_check["status"] != "completed":
        raise RuntimeError("identity bridge ONNX runtime check failed")

    feature_common_path = f"{COMMON_ROOT}/features/{replay_feature_path.name}"
    model_common_path = f"{COMMON_ROOT}/models/{onnx_path.name}"
    feature_copy = copy_to_common(replay_feature_path, common_files_root, feature_common_path)
    model_copy = copy_to_common(onnx_path, common_files_root, model_common_path)
    from_date, to_date = tester_dates(replay["timestamp"])
    attempt_name = "m48_breadth_soft_veto_replay"
    telemetry = f"{COMMON_ROOT}/telemetry/{attempt_name}_telemetry.csv"
    summary = f"{COMMON_ROOT}/telemetry/{attempt_name}_summary.csv"
    report_name = f"Project_Obsidian_Prime_v2_run333E_{attempt_name}"
    threshold = float(diagnostics["threshold"])
    set_values = {
        "InpRunId": RUN_ID,
        "InpExplorationLabel": EXPLORATION_LABEL,
        "InpTierLabel": TIER_A,
        "InpPrimaryActiveTier": "tier_a_signal_payload_replay_bridge",
        "InpSplitLabel": SPLIT_LABEL,
        "InpMainSymbol": "US100",
        "InpTimeframe": 5,
        "InpModelPath": model_common_path,
        "InpModelId": f"{RUN_ID}_identity_probability_bridge_not_candidate",
        "InpModelBackend": "onnx",
        "InpModelUseCommonFiles": "true",
        "InpFeatureCsvPath": feature_common_path,
        "InpFeatureCount": len(FEATURE_NAMES),
        "InpFeatureCsvUseCommonFiles": "true",
        "InpFeatureRequireTimestampMatch": "true",
        "InpFeatureAllowLatestFallback": "false",
        "InpFeatureStrictHeader": "true",
        "InpCsvTimestampIsBarClose": "true",
        "InpFeatureOrderHash": FEATURE_ORDER_HASH,
        "InpFallbackEnabled": "false",
        "InpFallbackFeatureCsvPath": feature_common_path,
        "InpFallbackFeatureCount": len(FEATURE_NAMES),
        "InpFallbackModelPath": model_common_path,
        "InpFallbackModelId": f"{RUN_ID}_identity_probability_bridge_not_candidate",
        "InpFallbackModelBackend": "onnx",
        "InpFallbackFeatureOrderHash": FEATURE_ORDER_HASH,
        "InpTelemetryCsvPath": telemetry,
        "InpSummaryCsvPath": summary,
        "InpTelemetryUseCommonFiles": "true",
        "InpShortThreshold": 0.0,
        "InpLongThreshold": 0.0,
        "InpMinMargin": threshold,
        "InpInvertSignal": "false",
        "InpFallbackShortThreshold": 0.0,
        "InpFallbackLongThreshold": 0.0,
        "InpFallbackMinMargin": threshold,
        "InpFallbackInvertSignal": "false",
        "InpAllowTrading": "true",
        "InpFixedLot": FIXED_LOT,
        "InpCloseOnFlatSignal": "false",
        "InpReverseOnOppositeSignal": "true",
        "InpCloseOnlyOnOppositeSignal": "false",
        "InpMaxHoldBars": MAX_HOLD_BARS,
        "InpMaxConcurrentPositions": 1,
        "InpReentryCooldownBars": 0,
        "InpSameDirectionReentryCooldownBars": 0,
        "InpAtrSltpEnabled": "false",
        "InpModelRiskSizingEnabled": "false",
        "InpMagic": 3330501,
    }
    set_payload = write_set(MT5_DIR / f"{attempt_name}.set", set_values)
    ini_payload = write_ini(
        MT5_DIR / f"{attempt_name}.ini",
        {
            "Expert": r"Project_Obsidian_Prime_v2\foundation\mt5\ObsidianPrimeV2_RuntimeProbeEA.ex5",
            "Symbol": "US100",
            "Period": "M5",
            "Model": 4,
            "Deposit": 500,
            "Leverage": "1:100",
            "Optimization": 0,
            "ExecutionMode": 0,
            "ForwardMode": 0,
            "UseLocal": 1,
            "UseRemote": 0,
            "UseCloud": 0,
            "ReplaceReport": 1,
            "ShutdownTerminal": 1,
            "FromDate": from_date,
            "ToDate": to_date,
            "Report": report_name,
            "ExpertParameters": mt5.EA_TESTER_SET_NAME,
        },
    )
    attempt = {
        "attempt_name": attempt_name,
        "queue_id": queue["queue_id"],
        "thesis_id": queue["thesis_id"],
        "source_artifact": queue["source_artifact"],
        "scoring_mode": queue["scoring_mode"],
        "candidate_id": diagnostics["candidate_id"],
        "artifact_slug": diagnostics["artifact_slug"],
        "feature_set_id": diagnostics["feature_set_id"],
        "model_id": diagnostics["model_id"],
        "tier": TIER_A,
        "split": SPLIT_LABEL,
        "attempt_role": "signal_payload_runtime_replay_bridge_not_candidate_model",
        "record_view_prefix": "signal_payload_replay",
        "routing_mode": "tier_a_signal_payload_replay_no_fallback",
        "signal_policy": "run333C guarded signal payload replayed through identity probability bridge; no threshold retuning",
        "from_date": from_date,
        "to_date": to_date,
        "decision_threshold": threshold,
        "feature_order_hash": FEATURE_ORDER_HASH,
        "feature_export": replay_export,
        "identity_onnx": bridge_onnx,
        "feature_copy": feature_copy,
        "model_copy": model_copy,
        "set": set_payload,
        "ini": ini_payload,
        "common_feature_path": feature_common_path,
        "common_model_path": model_common_path,
        "common_telemetry_path": telemetry,
        "common_summary_path": summary,
        "report_name": report_name,
        "preflight": diagnostics,
        "onnxruntime_check": onnx_check,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    materialization_rows = [
        {
            "queue_id": queue["queue_id"],
            "attempt_name": attempt_name,
            "bridge_type": "identity_probability_bridge_not_candidate_model",
            "feature_count": len(FEATURE_NAMES),
            "feature_order_hash": FEATURE_ORDER_HASH,
            "rows": diagnostics["rows"],
            "source_signal_rows": diagnostics["source_signal_rows"],
            "guarded_signal_rows": diagnostics["guarded_signal_rows"],
            "forced_flat_rows": diagnostics["forced_flat_rows"],
            "threshold": threshold,
            "feature_csv_path": replay_export["path"],
            "feature_csv_sha256": replay_export["sha256"],
            "identity_onnx_path": bridge_onnx["path"],
            "identity_onnx_sha256": bridge_onnx["sha256"],
            "set_path": set_payload["path"],
            "set_sha256": set_payload["sha256"],
            "ini_path": ini_payload["path"],
            "ini_sha256": ini_payload["sha256"],
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    artifacts = [replay_feature_path, replay_audit_path, onnx_path, onnx_check_path, MT5_DIR / f"{attempt_name}.set", MT5_DIR / f"{attempt_name}.ini"]
    return attempt, materialization_rows, artifacts


def clear_runtime_outputs(common_files_root: Path, attempt: Mapping[str, Any]) -> None:
    for key in ("common_telemetry_path", "common_summary_path"):
        path = common_files_root / Path(str(attempt[key]))
        if path_exists(path):
            io_path(path).unlink()


def terminal_runtime_output_snapshot(common_files_root: Path, attempt: Mapping[str, Any], *, status: str, wait_status: str) -> dict[str, Any]:
    payload = mt5.validate_mt5_runtime_outputs(common_files_root, attempt)
    payload["status"] = status
    payload["wait_status"] = wait_status
    return payload


def detect_running_terminal_processes(terminal_path: Path) -> dict[str, Any]:
    command = [
        "powershell",
        "-NoProfile",
        "-Command",
        (
            "Get-CimInstance Win32_Process -Filter \"name = 'terminal64.exe'\" | "
            "Select-Object ProcessId,ExecutablePath,CommandLine | ConvertTo-Json -Compress"
        ),
    ]
    proc = subprocess.run(command, text=True, capture_output=True, timeout=30)
    processes: list[dict[str, Any]] = []
    if proc.stdout.strip():
        parsed = json.loads(proc.stdout)
        if isinstance(parsed, dict):
            processes = [parsed]
        elif isinstance(parsed, list):
            processes = parsed
    target = str(terminal_path).lower()
    matching = []
    for item in processes:
        executable = str(item.get("ExecutablePath") or item.get("executable_path") or "").lower()
        if not executable or executable == target:
            matching.append(item)
    return {
        "status": "running" if matching else "not_running",
        "command": command,
        "returncode": proc.returncode,
        "processes": processes,
        "matching_processes": matching,
    }


def execute_attempt(
    attempt: Mapping[str, Any],
    *,
    terminal_path: Path,
    metaeditor_path: Path,
    terminal_data_root: Path,
    common_files_root: Path,
    tester_profile_root: Path,
    timeout_seconds: int,
    runtime_timeout_seconds: int,
    terminal_extra_args: Sequence[str],
) -> dict[str, Any]:
    compile_payload = mt5.compile_mql5_ea(metaeditor_path, mt5.EA_SOURCE_PATH, MT5_DIR / "mt5_compile.log")
    terminal_process_probe = detect_running_terminal_processes(terminal_path)
    execution_results: list[dict[str, Any]] = []
    if compile_payload.get("status") == "completed":
        clear_runtime_outputs(common_files_root, attempt)
        mt5.remove_existing_mt5_report_artifacts(terminal_data_root, attempt, run_id=RUN_ID)
        tester_profile_ini_path = tester_profile_root / f"opv2_s333e_{attempt['attempt_name']}.ini"
        if terminal_process_probe.get("status") == "running":
            result = {
                "status": "blocked",
                "command": [str(terminal_path), *terminal_extra_args, f"/config:{tester_profile_ini_path}"],
                "returncode": None,
                "blocker": "terminal_already_running_config_not_applied",
                "blocker_explanation": "running terminal64.exe can absorb /config without applying tester configuration",
                "terminal_process_probe": terminal_process_probe,
                "runtime_outputs": terminal_runtime_output_snapshot(
                    common_files_root,
                    attempt,
                    status="blocked",
                    wait_status="skipped_terminal_already_running",
                ),
            }
        else:
            try:
                result = mt5.run_mt5_tester(
                    terminal_path,
                    ROOT / str(attempt["ini"]["path"]),
                    set_path=ROOT / str(attempt["set"]["path"]),
                    tester_profile_set_path=tester_profile_root / mt5.EA_TESTER_SET_NAME,
                    tester_profile_ini_path=tester_profile_ini_path,
                    timeout_seconds=timeout_seconds,
                    terminal_extra_args=terminal_extra_args,
                )
            except subprocess.TimeoutExpired as exc:
                result = {
                    "status": "blocked",
                    "command": exc.cmd,
                    "returncode": None,
                    "blocker": "terminal_timeout",
                    "timeout_seconds": timeout_seconds,
                }
            except Exception as exc:  # pragma: no cover
                result = {
                    "status": "blocked",
                    "command": [],
                    "returncode": None,
                    "blocker": f"terminal_exception:{type(exc).__name__}",
                    "error": str(exc),
                }
            result["runtime_outputs"] = mt5.wait_for_mt5_runtime_outputs(
                common_files_root,
                attempt,
                timeout_seconds=runtime_timeout_seconds,
                poll_seconds=2.0,
            )
            if result["runtime_outputs"].get("status") != "completed":
                result["status"] = "blocked"
        result.update(
            {
                "attempt_name": attempt.get("attempt_name"),
                "queue_id": attempt.get("queue_id"),
                "thesis_id": attempt.get("thesis_id"),
                "candidate_id": attempt.get("candidate_id"),
                "artifact_slug": attempt.get("artifact_slug"),
                "feature_set_id": attempt.get("feature_set_id"),
                "model_id": attempt.get("model_id"),
                "tier": attempt.get("tier"),
                "split": attempt.get("split"),
                "attempt_role": attempt.get("attempt_role"),
                "routing_mode": attempt.get("routing_mode"),
                "signal_policy": attempt.get("signal_policy"),
                "ini_path": attempt.get("ini", {}).get("path"),
                "set_path": attempt.get("set", {}).get("path"),
            }
        )
        execution_results.append(result)
    report_records = mt5.collect_mt5_strategy_report_artifacts(
        terminal_data_root=terminal_data_root,
        run_output_root=RUN_DIR,
        attempts=[attempt],
        run_id=RUN_ID,
    )
    mt5.attach_mt5_report_metrics(execution_results, report_records)
    return {
        "compile": compile_payload,
        "terminal_process_probe": terminal_process_probe,
        "terminal_extra_args": list(terminal_extra_args),
        "execution_results": execution_results,
        "strategy_tester_reports": report_records,
        "mt5_kpi_records": build_mt5_kpi_records(execution_results),
    }


def runtime_blockers(execution_result: Mapping[str, Any]) -> list[str]:
    blockers = {
        str(row.get("blocker"))
        for row in execution_result.get("execution_results", [])
        if row.get("blocker")
    }
    compile_status = execution_result.get("compile", {}).get("status")
    if compile_status and compile_status != "completed":
        blockers.add(f"compile_{compile_status}")
    return sorted(blockers)


def copy_runtime_telemetry_artifacts(common_files_root: Path, attempt: Mapping[str, Any]) -> list[Path]:
    copied: list[Path] = []
    output_dir = RUN_DIR / "runtime_telemetry"
    output_dir.mkdir(parents=True, exist_ok=True)
    for key in ("common_telemetry_path", "common_summary_path"):
        source = common_files_root / Path(str(attempt[key]))
        if path_exists(source):
            destination = output_dir / source.name
            shutil.copy2(io_path(source), io_path(destination))
            copied.append(destination)
    return copied


def summary_rows(attempt: Mapping[str, Any], execution_result: Mapping[str, Any]) -> list[dict[str, Any]]:
    result = execution_result.get("execution_results", [{}])[0] if execution_result.get("execution_results") else {}
    runtime = result.get("runtime_outputs", {})
    report = result.get("strategy_tester_report", {})
    metrics = report.get("metrics", {}) if isinstance(report, Mapping) else {}
    return [
        {
            "attempt_name": attempt["attempt_name"],
            "queue_id": attempt["queue_id"],
            "thesis_id": attempt["thesis_id"],
            "source_artifact": attempt["source_artifact"],
            "scoring_mode": attempt["scoring_mode"],
            "tester_status": result.get("status", "not_attempted"),
            "runtime_status": runtime.get("status", "not_attempted"),
            "report_status": report.get("status", "not_attempted") if isinstance(report, Mapping) else "not_attempted",
            "returncode": result.get("returncode", ""),
            "blocker": result.get("blocker", ""),
            "feature_ready_count": runtime.get("last_summary", {}).get("feature_ready_count", ""),
            "model_ok_count": runtime.get("last_summary", {}).get("model_ok_count", ""),
            "order_attempt_count": runtime.get("last_summary", {}).get("order_attempt_count", ""),
            "order_fill_count": runtime.get("last_summary", {}).get("order_fill_count", ""),
            "net_profit": metrics.get("net_profit", ""),
            "profit_factor": metrics.get("profit_factor", ""),
            "trade_count": metrics.get("trade_count", ""),
            "common_summary_path": attempt["common_summary_path"],
            "common_telemetry_path": attempt["common_telemetry_path"],
            "report_name": attempt["report_name"],
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def classify(execution_result: Mapping[str, Any], materialize_only: bool) -> tuple[str, str, str, str]:
    if materialize_only:
        return STATUS_MATERIALIZED, JUDGMENT_BLOCKED, DECISION_BLOCKED, NEXT_BLOCKED
    completed = sum(1 for row in execution_result.get("execution_results", []) if row.get("status") == "completed")
    if completed:
        return STATUS_COMPLETED, JUDGMENT_COMPLETED, DECISION_COMPLETED, NEXT_COMPLETED
    return STATUS_BLOCKED, JUDGMENT_BLOCKED, DECISION_BLOCKED, NEXT_BLOCKED


def write_run_outputs(
    generated_at_utc: str,
    attempt: Mapping[str, Any],
    materialization_rows: Sequence[Mapping[str, Any]],
    materialized_artifacts: Sequence[Path],
    execution_result: Mapping[str, Any],
    status: str,
    judgment: str,
    decision: str,
    next_action: str,
    args: argparse.Namespace,
) -> list[Path]:
    artifacts: list[Path] = list(materialized_artifacts)
    compile_log = MT5_DIR / "mt5_compile.log"
    if path_exists(compile_log):
        artifacts.append(compile_log)
    artifacts.extend(copy_runtime_telemetry_artifacts(Path(args.common_files_root), attempt))
    completed_count = sum(1 for row in execution_result.get("execution_results", []) if row.get("status") == "completed")
    blockers = runtime_blockers(execution_result)

    materialization_path = RUN_DIR / "runtime_probe_handoff_manifest.csv"
    execution_path = RUN_DIR / "execution_result.json"
    attempt_path = RUN_DIR / "mt5_probe_attempts.json"
    summary_path = RUN_DIR / "mt5_runtime_probe_summary.csv"
    kpi_path = RUN_DIR / "mt5_kpi_records.json"
    failure_path = RUN_DIR / "failure_memory_from_screen.csv"
    result_path = RUN_DIR / "result_judgment.csv"
    runtime_receipt = RUN_DIR / "runtime_parity_receipt.json"
    backtest_receipt = RUN_DIR / "backtest_forensics_receipt.json"
    data_receipt = RUN_DIR / "data_integrity_receipt.json"
    lineage_receipt = RUN_DIR / "artifact_lineage_receipt.json"
    model_receipt = RUN_DIR / "model_validation_receipt.json"
    attribution_receipt = RUN_DIR / "performance_attribution_receipt.json"
    experiment_receipt = RUN_DIR / "experiment_design_receipt.json"
    gate_path = RUN_DIR / "required_gate_coverage_audit.csv"
    manifest_path = RUN_DIR / "run_manifest.json"

    decision_rows = read_csv_rows(RUN333D_DIR / "branch_screen_decision.csv")
    failure_rows = build_failure_memory(decision_rows)
    artifacts.extend(
        [
            write_csv(
                materialization_path,
                [
                    "queue_id",
                    "attempt_name",
                    "bridge_type",
                    "feature_count",
                    "feature_order_hash",
                    "rows",
                    "source_signal_rows",
                    "guarded_signal_rows",
                    "forced_flat_rows",
                    "threshold",
                    "feature_csv_path",
                    "feature_csv_sha256",
                    "identity_onnx_path",
                    "identity_onnx_sha256",
                    "set_path",
                    "set_sha256",
                    "ini_path",
                    "ini_sha256",
                    "claim_boundary",
                ],
                materialization_rows,
            ),
            write_json(attempt_path, [attempt]),
            write_json(execution_path, execution_result),
            write_csv(
                summary_path,
                [
                    "attempt_name",
                    "queue_id",
                    "thesis_id",
                    "source_artifact",
                    "scoring_mode",
                    "tester_status",
                    "runtime_status",
                    "report_status",
                    "returncode",
                    "blocker",
                    "feature_ready_count",
                    "model_ok_count",
                    "order_attempt_count",
                    "order_fill_count",
                    "net_profit",
                    "profit_factor",
                    "trade_count",
                    "common_summary_path",
                    "common_telemetry_path",
                    "report_name",
                    "claim_boundary",
                ],
                summary_rows(attempt, execution_result),
            ),
            write_json(kpi_path, execution_result.get("mt5_kpi_records", [])),
            write_csv(
                failure_path,
                [
                    "queue_id",
                    "thesis_id",
                    "source_artifact",
                    "scoring_mode",
                    "screen_decision",
                    "memory_type",
                    "net_profit",
                    "profit_factor",
                    "max_drawdown",
                    "cost2_pf",
                    "rolling20_min_net",
                    "rolling40_min_net",
                    "reuse_rule",
                    "claim_boundary",
                ],
                failure_rows,
            ),
        ]
    )

    artifacts.append(
        write_csv(
            result_path,
            [
                "run_id",
                "status",
                "judgment",
                "decision",
                "forward_passed",
                "forward_failed",
                "forward_blocked",
                "goal_achieve",
                "next_action",
                "claim_boundary",
            ],
            [
                {
                    "run_id": RUN_ID,
                    "status": status,
                    "judgment": judgment,
                    "decision": decision,
                    "forward_passed": "not_claimed",
                    "forward_failed": "not_claimed",
                    "forward_blocked": "not_claimed",
                    "goal_achieve": "not_claimed",
                    "next_action": next_action,
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            ],
        )
    )
    artifacts.append(
        write_json(
            runtime_receipt,
            {
                "research_path": rel(Path(__file__)),
                "runtime_path": rel(ROOT / mt5.EA_SOURCE_PATH),
                "shared_contract": {
                    "signal_payload": attempt["preflight"]["guarded_signal_payload_path"],
                    "bridge_features": attempt["feature_export"],
                    "bridge_model": "identity ONNX probability bridge; not a candidate model",
                    "threshold": attempt["decision_threshold"],
                    "risk_lot": f"fixed lot {FIXED_LOT}, max hold {MAX_HOLD_BARS}, no ATR SLTP, no model risk sizing",
                    "time_axis": "bar close UTC timestamp, InpCsvTimestampIsBarClose=true",
                },
                "known_differences": [
                    "The MT5 run replays a frozen signal payload through an identity bridge instead of proving a packaged guarded ONNX model.",
                    "This is runtime_probe, not runtime_authority.",
                ],
                "parity_check": {
                    "signal_payload_preflight": rel(RUN_DIR / "signal_replay_preflight_audit.csv"),
                    "onnxruntime_identity_check": rel(RUN_DIR / "identity_bridge_onnxruntime_check.json"),
                    "mt5_summary": rel(summary_path),
                },
                "parity_identity": {
                    "module_hashes": mt5.mt5_runtime_module_hashes(),
                    "feature_order_hash": FEATURE_ORDER_HASH,
                    "identity_onnx_sha256": attempt["identity_onnx"]["sha256"],
                    "set_sha256": attempt["set"]["sha256"],
                    "ini_sha256": attempt["ini"]["sha256"],
                    "compile": execution_result.get("compile", {}),
                    "terminal_process_probe": execution_result.get("terminal_process_probe", {}),
                    "completed_attempt_count": completed_count,
                    "runtime_blockers": blockers,
                },
                "runtime_claim_boundary": "runtime_probe_research_only_no_runtime_authority",
            },
        )
    )
    artifacts.append(
        write_json(
            backtest_receipt,
            {
                "tester_identity": {
                    "terminal": str(args.terminal_path),
                    "terminal_extra_args": execution_result.get("terminal_extra_args", []),
                    "broker_terminal_data_root": str(args.terminal_data_root),
                    "terminal_process_probe": execution_result.get("terminal_process_probe", {}),
                    "symbol": "US100",
                    "timeframe": "M5",
                    "deposit": 500,
                    "leverage": "1:100",
                    "modeling_mode": "Every tick based on real ticks / MT5 model=4",
                    "date_range": f"{attempt['from_date']}..{attempt['to_date']}",
                },
                "ea_identity": {
                    "entrypoint": rel(ROOT / mt5.EA_SOURCE_PATH),
                    "module_hashes": mt5.mt5_runtime_module_hashes(),
                    "set_file": attempt["set"],
                    "identity_onnx": attempt["identity_onnx"],
                },
                "report_identity": execution_result.get("strategy_tester_reports", []),
                "trade_evidence": execution_result.get("mt5_kpi_records", []),
                "cost_assumptions": {
                    "spread": "broker tester setting, not overwritten by run333E",
                    "commission": "broker tester setting, not overwritten by run333E",
                    "slippage": "InpDeviationPoints=default_or_set_file_value",
                    "swap": "broker tester setting",
                },
                "forensic_checks": [
                    "MetaEditor compile attempted before tester run.",
                    "Runtime telemetry and summary files checked after tester run.",
                    "Strategy Tester report copied when MT5 emits it.",
                ],
                "backtest_judgment": "usable_with_boundary" if completed_count else "blocked",
            },
        )
    )
    artifacts.append(
        write_json(
            data_receipt,
            {
                "data_source": {
                    "source_prediction": attempt["preflight"]["source_prediction_path"],
                    "scored_payload": attempt["preflight"]["scored_payload_path"],
                    "guarded_signal_payload": attempt["preflight"]["guarded_signal_payload_path"],
                },
                "time_axis": "UTC bar-close timestamp; MT5 tester set uses FromDate/ToDate around the same bar-close span.",
                "sample_scope": {
                    "symbol": "US100",
                    "timeframe": "M5",
                    "rows": attempt["preflight"]["rows"],
                    "start": attempt["preflight"]["first_timestamp"],
                    "end": attempt["preflight"]["last_timestamp"],
                },
                "missing_or_duplicate_check": "prediction/scored payload one-to-one timestamp merge and signal payload exact replay parity completed",
                "feature_label_boundary": "no labels or future returns consumed; only frozen prediction probabilities and predeclared guard flags are replayed",
                "split_boundary": "post-2026-04-14 raw forward replay scope",
                "leakage_risk": "guard feature came from Stage333 timestamp-safe materialization; breadth missing rows remain a boundary",
                "data_hash_or_identity": {
                    "feature_csv_sha256": attempt["feature_export"]["sha256"],
                    "guarded_signal_payload_sha256": attempt["preflight"]["guarded_signal_payload_sha256"],
                },
                "integrity_judgment": "usable_with_boundary",
            },
        )
    )
    artifacts.append(
        write_json(
            model_receipt,
            {
                "model_family": "identity_probability_bridge_not_candidate_model",
                "target_and_label": "no training target; bridge passes p_short/p_flat/p_long from frozen signal payload replay frame",
                "split_method": "runtime_probe",
                "selection_metric": "none",
                "secondary_metrics": "signal payload parity; MT5 tester forensics if available",
                "threshold_policy": "fixed train-only threshold inherited from run330B source artifact",
                "overfit_risk": "bridge is not trained, but the guarded signal branch remains proxy-screen-selected and needs packaging-boundary review",
                "calibration_risk": "probabilities are replayed values, not recalibrated",
                "comparison_baseline": "run330E m48_plain_rf source MT5 reference and run333D proxy cost/curve screen",
                "validation_judgment": "exploratory_runtime_probe_only",
            },
        )
    )
    artifacts.append(
        write_json(
            attribution_receipt,
            {
                "observed_change": "run333D survivor reduced source signal rows through guarded soft veto before run333E runtime replay",
                "comparison_baseline": "m48_plain raw-forward source signal and run330E m48_plain_rf MT5 reference",
                "likely_drivers": "bounded breadth divergence guard forced source nonflat rows flat without threshold retuning",
                "segment_checks": "run333D proxy cost/curve/regime slices exist; run333E adds MT5 tester telemetry if completed",
                "trade_shape": summary_rows(attempt, execution_result)[0],
                "alternative_explanations": "identity bridge is signal replay, not a packaged guarded ONNX; broker tester costs remain terminal-controlled",
                "attribution_confidence": "medium" if completed_count else "inconclusive",
                "next_probe": NEXT_COMPLETED if completed_count else NEXT_BLOCKED,
            },
        )
    )
    artifacts.append(
        write_json(
            experiment_receipt,
            {
                "hypothesis": "The sole run333D survivor deserves a narrow MT5 signal-replay probe before any packaging or failure-memory decision.",
                "decision_use": "Decide whether to review MT5 runtime evidence or record runtime blocker/failure memory.",
                "comparison_baseline": "run333D proxy screen and run330E m48_plain_rf source MT5 reference.",
                "control_variables": "source probabilities, fixed threshold, fixed lot, max hold, no ATR SLTP, no model risk sizing.",
                "changed_variables": "guarded signal payload is replayed through an identity probability bridge.",
                "sample_scope": "US100 M5 raw forward after 2026-04-14 through available run330B forward frame.",
                "success_criteria": "preflight exact signal parity plus MT5 report/telemetry/summary emitted.",
                "failure_criteria": "preflight mismatch, compile failure, terminal/config failure, missing telemetry, or missing Strategy Tester report.",
                "invalid_conditions": "threshold retune, lot optimization, trained bridge model, or missing timestamp identity.",
                "stop_conditions": "stop at runtime probe boundary; do not claim Forward Passed/Failed or Goal Achieve.",
                "evidence_plan": [rel(materialization_path), rel(summary_path), rel(runtime_receipt), rel(backtest_receipt)],
            },
        )
    )
    artifacts.append(
        write_json(
            lineage_receipt,
            {
                "source_inputs": {
                    "run333D_runtime_queue": rel(RUN333D_DIR / "runtime_probe_branch_queue.csv"),
                    "run333D_screen_decisions": rel(RUN333D_DIR / "branch_screen_decision.csv"),
                    "run333C_payload_manifest": rel(RUN333C_DIR / "payload_manifest.csv"),
                    "run330B_source_prediction_manifest": rel(RUN330B_DIR / "signal_payload_manifest.csv"),
                    "run332E_runtime_contract": rel(RUN332E_DIR / "runtime_probe_readiness_matrix.csv"),
                },
                "producer": rel(Path(__file__)),
                "consumer": next_action,
                "artifact_paths": [rel(path) for path in artifacts if path_exists(path)],
                "artifact_hashes": {rel(path): sha256_file(path) for path in artifacts if path_exists(path) and not io_path(path).is_dir()},
                "registry_links": {
                    "run_registry": rel(RUN_REGISTRY),
                    "alpha_ledger": rel(ALPHA_LEDGER),
                    "stage_ledger": rel(STAGE_LEDGER),
                    "artifact_registry": rel(ARTIFACT_REGISTRY),
                },
                "availability": "tracked",
                "lineage_judgment": "connected_with_boundary",
            },
        )
    )
    artifacts.append(
        write_csv(
            gate_path,
            ["gate_name", "status", "evidence_path", "effect"],
            [
                {
                    "gate_name": "data_integrity",
                    "status": "completed",
                    "evidence_path": rel(data_receipt),
                    "effect": "timestamp and signal replay identity is checked before MT5 execution",
                },
                {
                    "gate_name": "model_validation",
                    "status": "completed_with_boundary",
                    "evidence_path": rel(model_receipt),
                    "effect": "identity bridge is recorded as non-candidate and non-trained",
                },
                {
                    "gate_name": "runtime_parity",
                    "status": "completed" if completed_count else "blocked",
                    "evidence_path": rel(runtime_receipt),
                    "effect": "signal payload to MT5 handoff is either executed or blocked with identity",
                },
                {
                    "gate_name": "backtest_forensics",
                    "status": "usable_with_boundary" if completed_count else "blocked",
                    "evidence_path": rel(backtest_receipt),
                    "effect": "tester identity, report path, and cost assumptions are recorded",
                },
                {
                    "gate_name": "artifact_lineage",
                    "status": "completed",
                    "evidence_path": rel(lineage_receipt),
                    "effect": "source queue, bridge files, reports, and next consumer are connected",
                },
                {
                    "gate_name": "result_judgment",
                    "status": "completed",
                    "evidence_path": rel(result_path),
                    "effect": "Forward Passed/Failed and Goal Achieve are not claimed",
                },
            ],
        )
    )
    artifacts.append(
        write_json(
            manifest_path,
            {
                "stage_id": STAGE_ID,
                "run_number": RUN_NUMBER,
                "run_id": RUN_ID,
                "parent_run_id": PARENT_RUN_ID,
                "generated_at_utc": generated_at_utc,
                "status": status,
                "judgment": judgment,
                "decision": decision,
                "next_action": next_action,
                "attempt": attempt,
                "execution_result_path": rel(execution_path),
                "runtime_blockers": blockers,
                "claim_boundary": CLAIM_BOUNDARY,
            },
        )
    )
    return artifacts


def write_reports(status: str, judgment: str, decision: str, next_action: str, execution_result: Mapping[str, Any], artifacts: Sequence[Path]) -> list[Path]:
    completed_count = sum(1 for row in execution_result.get("execution_results", []) if row.get("status") == "completed")
    blockers = runtime_blockers(execution_result)
    report_path = REVIEWS_DIR / "run333E_signal_payload_runtime_probe_or_block.md"
    decision_doc = DECISION_DOC
    md = f"""
# run333E Signal Payload Runtime Probe Or Block(333E 신호 페이로드 런타임 탐침 또는 차단)

- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{status}`
- judgment(판정): `{judgment}`
- decision(결정): `{decision}`
- completed_mt5_attempts(완료 MT5 시도): `{completed_count}`
- runtime_blockers(런타임 차단 사유): `{';'.join(blockers) if blockers else 'none'}`
- next_action(다음 행동): `{next_action}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

## What Changed(무엇이 바뀌었나)

run333D(333D 실행)의 유일한 survivor(생존 분기) `pv_m48_breadth_reintroduction_control__soft_veto`를 signal payload replay bridge(신호 페이로드 재생 연결기)로 물질화했다.
Effect(효과): MT5(메타트레이더5)는 기존 ONNX(온엑스) 모델 패키지를 증명하는 것이 아니라, frozen signal payload(고정 신호 페이로드)가 tester execution(테스터 실행)에서 어떤 결과를 내는지 좁게 확인한다.

## Evidence(근거)

- handoff_manifest(인계 목록): `{rel(RUN_DIR / "runtime_probe_handoff_manifest.csv")}`
- preflight_audit(사전 점검): `{rel(RUN_DIR / "signal_replay_preflight_audit.csv")}`
- mt5_summary(MT5 요약): `{rel(RUN_DIR / "mt5_runtime_probe_summary.csv")}`
- execution_result(실행 결과): `{rel(RUN_DIR / "execution_result.json")}`
- runtime_parity_receipt(런타임 동등성 영수증): `{rel(RUN_DIR / "runtime_parity_receipt.json")}`
- backtest_forensics_receipt(백테스트 포렌식 영수증): `{rel(RUN_DIR / "backtest_forensics_receipt.json")}`
- failure_memory(실패 기억): `{rel(RUN_DIR / "failure_memory_from_screen.csv")}`

## Boundary(경계)

Forward Passed(전진 통과), Forward Failed(전진 실패), runtime authority(런타임 권위), operating promotion(운영 승격), deployment(배포), Goal Achieve(목표 달성)는 주장하지 않는다.
"""
    decision_md = f"""
# Stage333E Decision(333E 결정)

- decision_subject(결정 대상): run333D(333D 실행) survivor(생존 분기)의 MT5 signal replay(신호 재생) 가능성
- decision(결정): `{decision}`
- status(상태): `{status}`
- next_condition(다음 조건): `{next_action}`
- effect(효과): proxy screen(대리 선별) 결과를 바로 후보 선택으로 올리지 않고, MT5(메타트레이더5) runtime evidence(런타임 근거) 또는 blocker(차단 사유)로 분리한다.
- forbidden_claims(금지 주장): Forward Passed/Failed(전진 통과/실패), live readiness(실거래 준비), deployment(배포), operating promotion(운영 승격), runtime authority(런타임 권위), Goal Achieve(목표 달성)
"""
    return [write_md(report_path, md), write_md(decision_doc, decision_md), *list(artifacts)]


def update_selection_status(status: str, judgment: str, next_action: str) -> Path:
    if not path_exists(SELECTION_STATUS):
        SELECTED_DIR.mkdir(parents=True, exist_ok=True)
        write_md(SELECTION_STATUS, "# Stage333 Selection Status(333단계 선택 상태)\n")
    text, had_bom = read_text_lossless(SELECTION_STATUS)
    replacements = {
        "- stage_status(": f"- stage_status(단계 상태): `{status}`",
        "- current_run(": f"- current_run(현재 실행): `{RUN_ID}`",
        "- next_action(": f"- next_action(다음 행동): `{next_action}`",
        "- effect(": f"- effect(효과): run333E(333E 실행)는 signal payload replay bridge(신호 페이로드 재생 연결기)를 만들고 MT5(메타트레이더5) runtime probe(런타임 탐침)를 시도했으며, Goal Achieve(목표 달성)는 주장하지 않는다.",
    }
    for prefix, replacement in replacements.items():
        text = replace_prefix_line(text, prefix, replacement)
    for key in (
        "- Forward Passed(전진 통과): `not_claimed`",
        "- Forward Failed(전진 실패): `not_claimed`",
        "- live_readiness(실거래 준비): `not_claimed`",
        "- deployment(배포): `not_claimed`",
        "- operating_promotion(운영 승격): `not_claimed`",
        "- runtime_authority(런타임 권위): `not_claimed`",
        "- goal_achieve(목표 달성): `not_claimed`",
    ):
        if key.split(":")[0] not in text:
            text = text.rstrip() + "\n" + key + "\n"
    write_text_lossless(SELECTION_STATUS, text, had_bom)
    return SELECTION_STATUS


def update_current_truth(status: str, judgment: str, next_action: str) -> list[Path]:
    artifacts: list[Path] = []
    if path_exists(WORKSPACE_STATE):
        text, had_bom = read_text_lossless(WORKSPACE_STATE)
        text = replace_prefix_line(text, "current_run_id:", f"current_run_id: {next_action}")
        text = replace_prefix_line(text, "updated_on:", f"updated_on: '{TODAY}'")
        focus_line = (
            f"  Stage333(333단계) run333E(333E 실행)는 `{status}`로 signal payload runtime replay bridge"
            f"(신호 페이로드 런타임 재생 연결기)를 만들고 MT5(메타트레이더5) 실행을 시도했다. Effect(효과): "
            f"`{judgment}`이며 Forward Passed/Failed(전진 통과/실패), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 없다."
        )
        marker = "Stage333(333단계) run333E(333E 실행)"
        if marker not in text:
            text = text.replace("current_focus:\n", "current_focus:\n- >-\n" + focus_line + "\n", 1)
        else:
            text = replace_line_containing(text, marker, focus_line)
        write_text_lossless(WORKSPACE_STATE, text, had_bom)
        artifacts.append(WORKSPACE_STATE)
    if path_exists(CURRENT_STATE):
        text, had_bom = read_text_lossless(CURRENT_STATE)
        text = replace_prefix_line(text, "- current_run(", f"- current_run(현재 실행): `{next_action}`")
        text = replace_prefix_line(text, "- status(", f"- status(상태): `{status}`")
        text = replace_prefix_line(text, "- decision(", f"- decision(판정): `{judgment}`")
        text = replace_prefix_line(text, "- next_action(", f"- next_action(다음 행동): `{next_action}`")
        text = replace_prefix_line(text, "- claim_boundary(", f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`")
        marker = "run333E_summary(333E 요약)"
        summary_line = (
            f"- {marker}: signal payload runtime replay bridge(신호 페이로드 런타임 재생 연결기)를 `{status}`로 처리했다. "
            f"Effect(효과): MT5(메타트레이더5) runtime evidence(런타임 근거) 또는 blocker(차단 사유)를 남기고, "
            f"Forward Passed/Failed(전진 통과/실패)와 Goal Achieve(목표 달성)는 주장하지 않는다."
        )
        if marker not in text:
            text = text.replace("- run333D_summary", summary_line + "\n- run333D_summary", 1)
        else:
            text = replace_line_containing(text, marker, summary_line)
        write_text_lossless(CURRENT_STATE, text, had_bom)
        artifacts.append(CURRENT_STATE)
    if path_exists(CHANGELOG):
        append_if_missing(
            CHANGELOG,
            RUN_ID,
            f"""
## {TODAY} - {RUN_ID}

- status(상태): `{status}`
- effect(효과): run333D(333D 실행)의 survivor(생존 분기)를 signal payload replay bridge(신호 페이로드 재생 연결기)로 MT5(메타트레이더5)에 넘기는 근거를 만들었다.
- boundary(경계): Goal Achieve(목표 달성), Forward Passed/Failed(전진 통과/실패), runtime authority(런타임 권위)는 주장하지 않는다.
""",
        )
        artifacts.append(CHANGELOG)
    return artifacts


def infer_artifact_type(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix == ".csv":
        return "csv"
    if suffix == ".json":
        return "json"
    if suffix == ".md":
        return "report"
    if suffix == ".onnx":
        return "onnx_bridge_not_candidate"
    if suffix in {".set", ".ini"}:
        return "mt5_config"
    if suffix in {".htm", ".html", ".png"}:
        return "mt5_report"
    return suffix.lstrip(".") or "file"


def update_registers(generated_at_utc: str, status: str, judgment: str, decision: str, next_action: str, artifacts: Sequence[Path]) -> None:
    report_path = REVIEWS_DIR / "run333E_signal_payload_runtime_probe_or_block.md"
    upsert_csv(
        RUN_REGISTRY,
        ["run_id"],
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "run_number": RUN_NUMBER,
                "parent_run_id": PARENT_RUN_ID,
                "status": status,
                "judgment": judgment,
                "decision": decision,
                "created_at_utc": generated_at_utc,
                "updated_at_utc": generated_at_utc,
                "summary": "Stage333E signal payload runtime replay bridge; no Forward Passed/Failed or Goal Achieve claim.",
                "report_path": rel(report_path),
                "next_action": next_action,
            }
        ],
    )
    upsert_csv(
        ALPHA_LEDGER,
        ["ledger_row_id"],
        [
            {
                "ledger_row_id": f"{RUN_ID}__signal_payload_runtime_replay",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": RUN_NUMBER,
                "parent_run_id": PARENT_RUN_ID,
                "record_view": "signal_payload_runtime_replay_or_block",
                "tier_scope": "raw_forward_signal_payload_scope",
                "kpi_scope": "mt5_runtime_probe_and_tester_output_or_block",
                "scoreboard_lane": "runtime_parity",
                "status": status,
                "judgment": judgment,
                "path": rel(report_path),
                "primary_kpi": "completed_mt5_signal_replay_attempt_count",
                "guardrail_kpi": "no_threshold_retuning;selected_candidate=none;goal_achieve_not_claimed",
                "external_verification_status": "attempted_or_blocked_recorded_in_run_manifest",
                "notes": f"decision={decision};next_action={next_action}.",
            }
        ],
    )
    upsert_csv(
        STAGE_LEDGER,
        ["row_id"],
        [
            {
                "row_id": f"{RUN_ID}__signal_payload_runtime_replay",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "view": "signal_payload_runtime_replay_or_block",
                "tier_scope": "raw_forward_signal_payload_scope",
                "scoreboard": "mt5_runtime_probe_and_forensics",
                "status": status,
                "judgment": judgment,
                "evidence_boundary": CLAIM_BOUNDARY,
                "report_path": rel(report_path),
                "notes": "no_candidate_selection;no_forward_pass_fail;goal_achieve_not_claimed.",
                "decision": decision,
            }
        ],
    )
    artifact_rows: list[dict[str, Any]] = []
    for artifact in artifacts:
        if not path_exists(artifact) or io_path(artifact).is_dir():
            continue
        artifact_rows.append(
            {
                "artifact_id": f"{RUN_ID}__{artifact.stem}__{artifact.suffix.lstrip('.').lower() or 'file'}".replace("-", "_"),
                "artifact_type": infer_artifact_type(artifact),
                "path": rel(artifact),
                "sha256": sha256_file(artifact),
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": generated_at_utc,
                "notes": "Stage333E signal payload runtime probe or block artifact; no Forward Passed/Failed claim.",
            }
        )
    upsert_csv(ARTIFACT_REGISTRY, ["path", "run_id"], artifact_rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Stage333E signal payload runtime probe or record a block.")
    parser.add_argument("--terminal-path", default=str(TERMINAL_PATH_DEFAULT))
    parser.add_argument("--metaeditor-path", default=str(METAEDITOR_PATH_DEFAULT))
    parser.add_argument("--terminal-data-root", default=str(TERMINAL_DATA_ROOT_DEFAULT))
    parser.add_argument("--common-files-root", default=str(COMMON_FILES_ROOT_DEFAULT))
    parser.add_argument("--tester-profile-root", default=str(TESTER_PROFILE_ROOT_DEFAULT))
    parser.add_argument("--timeout-seconds", type=int, default=900)
    parser.add_argument("--runtime-timeout-seconds", type=int, default=180)
    parser.add_argument("--terminal-extra-arg", action="append", default=[])
    parser.add_argument("--materialize-only", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    generated_at_utc = utc_now()
    for directory in (RUN_DIR, REPLAY_DIR, ONNX_DIR, MT5_DIR, REVIEWS_DIR, SELECTED_DIR):
        directory.mkdir(parents=True, exist_ok=True)
    common_files_root = Path(args.common_files_root)
    attempt, materialization_rows, materialized_artifacts = materialize_attempt(common_files_root)
    if args.materialize_only:
        execution_result: dict[str, Any] = {
            "compile": {"status": "not_attempted_materialize_only"},
            "terminal_process_probe": {},
            "terminal_extra_args": list(args.terminal_extra_arg or []),
            "execution_results": [],
            "strategy_tester_reports": [],
            "mt5_kpi_records": [],
        }
    else:
        execution_result = execute_attempt(
            attempt,
            terminal_path=Path(args.terminal_path),
            metaeditor_path=Path(args.metaeditor_path),
            terminal_data_root=Path(args.terminal_data_root),
            common_files_root=common_files_root,
            tester_profile_root=Path(args.tester_profile_root),
            timeout_seconds=int(args.timeout_seconds),
            runtime_timeout_seconds=int(args.runtime_timeout_seconds),
            terminal_extra_args=list(args.terminal_extra_arg or []),
        )
    status, judgment, decision, next_action = classify(execution_result, args.materialize_only)
    artifacts = write_run_outputs(
        generated_at_utc,
        attempt,
        materialization_rows,
        materialized_artifacts,
        execution_result,
        status,
        judgment,
        decision,
        next_action,
        args,
    )
    artifacts = write_reports(status, judgment, decision, next_action, execution_result, artifacts)
    artifacts.extend([update_selection_status(status, judgment, next_action), *update_current_truth(status, judgment, next_action)])
    update_registers(generated_at_utc, status, judgment, decision, next_action, [*artifacts, Path(__file__)])
    print(
        json.dumps(
            {
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "status": status,
                "judgment": judgment,
                "decision": decision,
                "completed_attempt_count": sum(1 for row in execution_result.get("execution_results", []) if row.get("status") == "completed"),
                "runtime_blockers": runtime_blockers(execution_result),
                "selected_candidate": "none",
                "forward_passed": "not_claimed",
                "forward_failed": "not_claimed",
                "goal_achieve": "not_claimed",
                "next_action": next_action,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
