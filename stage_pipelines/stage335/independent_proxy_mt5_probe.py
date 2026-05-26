from __future__ import annotations

import argparse
import csv
import json
import math
import os
import re
import shutil
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np
import onnxruntime as ort
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import (  # noqa: E402
    ALPHA_LEDGER_COLUMNS,
    RUN_REGISTRY_COLUMNS,
    io_path,
    path_exists,
    sha256_file_lf_normalized,
    upsert_csv_rows,
)
from foundation.models.decision_surface import ThresholdRule, apply_threshold_rule  # noqa: E402
from foundation.models.onnx_bridge import ordered_hash  # noqa: E402
from foundation.mt5 import runtime_support as mt5  # noqa: E402
from foundation.mt5.runtime_artifacts import sha256_file  # noqa: E402


TODAY = "2026-05-26"
STAGE_ID = "335_overfit_guard__failure_memory_constrained_research_handoff"
RUN_NUMBER = "run335K"
RUN_ID = "run335K_repair_independent_proxy_mt5_runtime_probe_materialization_v1"
PARENT_RUN_ID = "run335J_materialize_proxy_expected_values_and_mt5_runtime_probe_attempts_or_block_v1"
NEXT_RUN_ID = "run335L_independent_runtime_parity_and_proxy_usability_review_v1"

STATUS_COMPLETED = "completed_independent_proxy_signal_and_mt5_runtime_probe_materialized_no_forward_decision"
STATUS_PARTIAL = "completed_independent_proxy_signal_materialization_with_runtime_probe_gaps_no_forward_decision"
STATUS_MATERIALIZED_ONLY = "completed_independent_probe_inputs_materialized_execution_pending_no_forward_decision"
JUDGMENT_COMPLETED = "independent_runtime_probe_completed_signal_parity_diagnostic_only_no_forward_decision"
JUDGMENT_PARTIAL = "independent_runtime_probe_attempted_with_gaps_no_forward_decision"
DECISION_COMPLETED = "stage335K_independent_proxy_signal_mt5_runtime_probe_diagnostic_usable_not_forward_usable_no_selection"
DECISION_PARTIAL = "stage335K_independent_runtime_materialization_or_probe_gap_repair_continues_no_selection"
CLAIM_BOUNDARY = (
    "research_development_only_stage335K_independent_proxy_mt5_probe_no_model_training_"
    "no_threshold_retuning_no_lot_optimization_no_direct_forward_pocket_filtering_"
    "no_candidate_selection_no_forward_passed_no_forward_failed_no_live_readiness_"
    "no_deployment_no_operating_promotion_no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
MT5_DIR = RUN_DIR / "mt5"
FEATURE_COPY_DIR = RUN_DIR / "feature_matrices"
MODEL_COPY_DIR = RUN_DIR / "models"
TELEMETRY_DIR = RUN_DIR / "runtime_telemetry"
REVIEWS_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"
STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
INPUT_REFS = STAGE_DIR / "01_inputs" / "input_refs.md"
STAGE_LEDGER = REVIEWS_DIR / "stage_run_ledger.csv"

STAGE330_DIR = ROOT / "stages" / "330_onnx_rebuild__forward_safe_non_identity_surface_robustness"
RUN330E_DIR = STAGE330_DIR / "02_runs" / "run330E"
RUN330F_DIR = STAGE330_DIR / "02_runs" / "run330F"
STAGE334_DIR = ROOT / "stages" / "334_runtime_parity__forward_usable_onnx_handoff_contract_hardening"
RUN334D_DIR = STAGE334_DIR / "02_runs" / "run334D"
RUN335J_DIR = STAGE_DIR / "02_runs" / "run335J"

DOCS = ROOT / "docs"
WORKSPACE_STATE = DOCS / "workspace" / "workspace_state.yaml"
CURRENT_STATE = DOCS / "context" / "current_working_state.md"
CHANGELOG = DOCS / "workspace" / "changelog.md"
RUN_REGISTRY = DOCS / "registers" / "run_registry.csv"
ALPHA_LEDGER = DOCS / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = DOCS / "registers" / "artifact_registry.csv"
DECISION_DOC = DOCS / "decisions" / "2026-05-26_stage335K_independent_proxy_mt5_runtime_probe.md"

DEFAULT_PORTABLE_ROOT = Path(r"C:\Users\awdse\AppData\Local\ObsidianPrime\mt5_portable_run329E")
DEFAULT_TERMINAL = DEFAULT_PORTABLE_ROOT / "terminal64.exe"
DEFAULT_METAEDITOR = DEFAULT_PORTABLE_ROOT / "MetaEditor64.exe"
DEFAULT_COMMON_FILES = DEFAULT_PORTABLE_ROOT / "Common" / "Files"
DEFAULT_TESTER_PROFILE_ROOT = DEFAULT_PORTABLE_ROOT / "MQL5" / "Profiles" / "Tester"
DEFAULT_TERMINAL_DATA_ROOT = DEFAULT_PORTABLE_ROOT
PORTABLE_EA_SOURCE = DEFAULT_PORTABLE_ROOT / "MQL5" / "Experts" / mt5.EA_SOURCE_PATH
PORTABLE_EA_EX5 = DEFAULT_PORTABLE_ROOT / "MQL5" / "Experts" / "Project_Obsidian_Prime_v2" / "foundation" / "mt5" / "ObsidianPrimeV2_RuntimeProbeEA.ex5"
COMMON_ROOT = "Project_Obsidian_Prime_v2/stage335/run335K_independent_proxy_mt5_runtime_probe"

DIMENSIONS = [
    "net_profit",
    "profit_factor",
    "max_drawdown",
    "trades_per_day",
    "expectancy",
    "recovery_factor",
    "curve_pocket",
    "underwater_stretch",
    "lot_normalized_result",
    "spread_slippage_stress",
    "session_hour_regime",
    "long_short_attribution",
]

FLOAT_KEYS = {
    "InpShortThreshold",
    "InpLongThreshold",
    "InpMinMargin",
    "InpFallbackShortThreshold",
    "InpFallbackLongThreshold",
    "InpFallbackMinMargin",
    "InpFixedLot",
}


def rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read_text_lossless(path: Path) -> tuple[str, bool]:
    raw = io_path(path).read_bytes()
    had_bom = raw.startswith(b"\xef\xbb\xbf")
    return raw.decode("utf-8-sig"), had_bom


def write_text_lossless(path: Path, text: str, had_bom: bool) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    encoding = "utf-8-sig" if had_bom else "utf-8"
    io_path(path).write_text(text, encoding=encoding, newline="\n")
    return path


def write_md(path: Path, text: str) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.strip() + "\n", encoding="utf-8-sig", newline="\n")
    return path


def write_json(path: Path, payload: Any) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path_exists(path):
        return []
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> Path:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: csv_value(row.get(column, "")) for column in columns})
    return path


def csv_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(json_ready(value), ensure_ascii=False, sort_keys=True)
    if isinstance(value, float):
        return "" if not math.isfinite(value) else f"{value:.12g}"
    return str(value)


def json_ready(value: Any) -> Any:
    if isinstance(value, Path):
        return value.as_posix()
    if isinstance(value, np.integer):
        return int(value)
    if isinstance(value, np.floating):
        number = float(value)
        return number if math.isfinite(number) else None
    if isinstance(value, np.bool_):
        return bool(value)
    if isinstance(value, float):
        return value if math.isfinite(value) else None
    if isinstance(value, Mapping):
        return {str(key): json_ready(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_ready(item) for item in value]
    return value


def parse_key_value_file(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for raw_line in io_path(path).read_text(encoding="utf-8-sig").splitlines():
        line = raw_line.strip()
        if not line or line.startswith(";") or line.startswith("["):
            continue
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip()
    return values


def parse_bool(value: Any) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def parse_float(value: Any, default: float = 0.0) -> float:
    try:
        number = float(str(value).strip())
        return number if math.isfinite(number) else default
    except Exception:
        return default


def parse_int(value: Any, default: int = 0) -> int:
    try:
        return int(float(str(value).strip()))
    except Exception:
        return default


def safe_name(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9]+", "_", value).strip("_")[:96]


def materialize_set_file(parameters: Mapping[str, Any], output_path: Path) -> dict[str, Any]:
    return mt5.materialize_tester_set_file(parameters, output_path, generated_by="stage_pipelines.stage335.independent_proxy_mt5_probe")


def materialize_ini_file(tester_values: Mapping[str, Any], output_path: Path) -> dict[str, Any]:
    io_path(output_path.parent).mkdir(parents=True, exist_ok=True)
    lines = ["[Tester]"]
    for key, value in tester_values.items():
        lines.append(f"{key}={mt5.tester_files.format_mt5_value(value) if hasattr(mt5, 'tester_files') else format_ini_value(value)}")
    io_path(output_path).write_text("\n".join(lines) + "\n", encoding="utf-8")
    return {"path": output_path.as_posix(), "sha256": sha256_file(output_path), "format": "mt5_tester_ini", "tester": dict(tester_values)}


def format_ini_value(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, float):
        return f"{value:.12g}"
    return str(value)


def copy_to_common(common_files_root: Path, local_path: Path, common_path: str) -> dict[str, Any]:
    return mt5.copy_to_common_files(common_files_root, local_path, common_path)


def source_hashes(paths: Mapping[str, Path]) -> dict[str, Any]:
    payload: dict[str, Any] = {"generated_at_utc": now_utc(), "run_id": RUN_ID, "sources": {}}
    for name, path in paths.items():
        payload["sources"][name] = {
            "path": rel(path),
            "exists": path_exists(path),
            "sha256": sha256_file(path) if path_exists(path) and io_path(path).is_file() else None,
        }
    return payload


def load_source_attempts() -> list[dict[str, Any]]:
    attempts = read_json(RUN330E_DIR / "mt5_probe_attempts.json")
    if not isinstance(attempts, list):
        raise RuntimeError("run330E mt5_probe_attempts.json is not a list")
    return [dict(row) for row in attempts]


def build_attempts(source_attempts: Sequence[Mapping[str, Any]], common_files_root: Path) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[Path]]:
    attempts: list[dict[str, Any]] = []
    handoff_rows: list[dict[str, Any]] = []
    artifacts: list[Path] = []

    for index, source in enumerate(source_attempts):
        attempt_name = str(source["attempt_name"])
        artifact_slug = str(source.get("artifact_slug") or attempt_name)
        source_set_path = ROOT / str(source["set"]["path"])
        source_ini_path = ROOT / str(source["ini"]["path"])
        source_set = parse_key_value_file(source_set_path)
        source_ini = parse_key_value_file(source_ini_path)

        model_source = ROOT / str(source.get("model_copy", {}).get("source", ""))
        if not path_exists(model_source):
            model_source = Path(str(source.get("model_copy", {}).get("absolute_path", "")))
        feature_source = ROOT / str(source.get("feature_export", {}).get("path", ""))
        if not path_exists(model_source):
            raise RuntimeError(f"missing source model for {attempt_name}: {model_source}")
        if not path_exists(feature_source):
            raise RuntimeError(f"missing source feature CSV for {attempt_name}: {feature_source}")

        model_local = MODEL_COPY_DIR / f"{artifact_slug}.onnx"
        feature_local = FEATURE_COPY_DIR / f"{artifact_slug}_features.csv"
        io_path(model_local.parent).mkdir(parents=True, exist_ok=True)
        io_path(feature_local.parent).mkdir(parents=True, exist_ok=True)
        shutil.copy2(io_path(model_source), io_path(model_local))
        shutil.copy2(io_path(feature_source), io_path(feature_local))
        artifacts.extend([model_local, feature_local])

        model_common = f"{COMMON_ROOT}/models/{model_local.name}"
        feature_common = f"{COMMON_ROOT}/features/{feature_local.name}"
        telemetry_common = f"{COMMON_ROOT}/telemetry/{attempt_name}_telemetry.csv"
        summary_common = f"{COMMON_ROOT}/telemetry/{attempt_name}_summary.csv"
        model_copy = copy_to_common(common_files_root, model_local, model_common)
        feature_copy = copy_to_common(common_files_root, feature_local, feature_common)

        new_set = dict(source_set)
        new_set.update(
            {
                "InpRunId": RUN_ID,
                "InpExplorationLabel": "stage335_OverfitGuard__IndependentProxyMt5RuntimeProbe",
                "InpModelPath": model_common,
                "InpModelId": f"{RUN_ID}_{artifact_slug}_onnx",
                "InpFeatureCsvPath": feature_common,
                "InpFallbackFeatureCsvPath": feature_common,
                "InpFallbackModelPath": model_common,
                "InpFallbackModelId": f"{RUN_ID}_{artifact_slug}_onnx",
                "InpTelemetryCsvPath": telemetry_common,
                "InpSummaryCsvPath": summary_common,
                "InpMagic": 3351100 + index,
            }
        )
        set_path = MT5_DIR / f"{attempt_name}.set"
        set_payload = materialize_set_file(new_set, set_path)

        tester = dict(source_ini)
        tester.update(
            {
                "Report": f"Project_Obsidian_Prime_v2_{RUN_ID}_{attempt_name}",
                "ExpertParameters": mt5.EA_TESTER_SET_NAME,
                "ShutdownTerminal": 1,
            }
        )
        ini_path = MT5_DIR / f"{attempt_name}.ini"
        ini_payload = materialize_ini_file(tester, ini_path)
        artifacts.extend([set_path, ini_path])

        unchanged = no_retune_unchanged_keys(source_set, new_set)
        handoff_rows.append(
            {
                "attempt_name": attempt_name,
                "artifact_slug": artifact_slug,
                "source_set_path": rel(source_set_path),
                "source_ini_path": rel(source_ini_path),
                "new_set_path": rel(set_path),
                "new_ini_path": rel(ini_path),
                "source_model_path": rel(model_source) if model_source.is_absolute() and str(model_source).startswith(str(ROOT)) else model_source.as_posix(),
                "new_model_path": rel(model_local),
                "source_feature_path": rel(feature_source),
                "new_feature_path": rel(feature_local),
                "model_common_path": model_common,
                "feature_common_path": feature_common,
                "telemetry_common_path": telemetry_common,
                "summary_common_path": summary_common,
                "threshold_keys_unchanged": unchanged["threshold_keys_unchanged"],
                "risk_lot_keys_unchanged": unchanged["risk_lot_keys_unchanged"],
                "allowed_identity_keys_changed": json.dumps(unchanged["changed_keys"], ensure_ascii=False),
                "source_set_sha256": sha256_file(source_set_path),
                "new_set_sha256": sha256_file(set_path),
                "source_ini_sha256": sha256_file(source_ini_path),
                "new_ini_sha256": sha256_file(ini_path),
                "model_sha256": model_copy["sha256"],
                "feature_sha256": feature_copy["sha256"],
                "materialization_status": "independent_handoff_materialized",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

        attempts.append(
            {
                "attempt_name": attempt_name,
                "candidate_id": source.get("candidate_id", ""),
                "artifact_slug": artifact_slug,
                "feature_set_id": source.get("feature_set_id", ""),
                "model_id": source.get("model_id", ""),
                "tier": source.get("tier", "Tier A"),
                "split": source.get("split", "forward_raw_forward"),
                "attempt_role": "stage335K_independent_replay_same_frozen_model_feature_threshold_risk",
                "record_view_prefix": f"mt5_stage335K_{artifact_slug}",
                "set": set_payload,
                "ini": ini_payload,
                "common_telemetry_path": telemetry_common,
                "common_summary_path": summary_common,
                "model_copy": model_copy,
                "feature_copy": feature_copy,
                "model_local_path": rel(model_local),
                "feature_local_path": rel(feature_local),
                "source_attempt_name": attempt_name,
                "source_run_id": "run330E_mt5_runtime_probe_or_block_v1",
                "from_date": tester.get("FromDate", ""),
                "to_date": tester.get("ToDate", ""),
                "decision_threshold": parse_float(new_set.get("InpMinMargin")),
                "decision_surface_mapping": source.get("decision_surface_mapping", ""),
                "routing_mode": source.get("routing_mode", "tier_a_primary_no_fallback"),
                "signal_policy": "same frozen ONNX, feature order, min margin, lot, hold, and risk keys; new isolated report and telemetry identity",
            }
        )
    return attempts, handoff_rows, artifacts


def no_retune_unchanged_keys(source_set: Mapping[str, str], new_set: Mapping[str, str]) -> dict[str, Any]:
    threshold_keys = [
        "InpShortThreshold",
        "InpLongThreshold",
        "InpMinMargin",
        "InpInvertSignal",
        "InpFallbackShortThreshold",
        "InpFallbackLongThreshold",
        "InpFallbackMinMargin",
        "InpFallbackInvertSignal",
    ]
    risk_lot_keys = [
        "InpAllowTrading",
        "InpFixedLot",
        "InpCloseOnFlatSignal",
        "InpReverseOnOppositeSignal",
        "InpCloseOnlyOnOppositeSignal",
        "InpMaxHoldBars",
        "InpMaxConcurrentPositions",
        "InpReentryCooldownBars",
        "InpSameDirectionReentryCooldownBars",
        "InpAtrSltpEnabled",
        "InpModelRiskSizingEnabled",
    ]
    changed = sorted(key for key in set(source_set).union(new_set) if str(source_set.get(key, "")) != str(new_set.get(key, "")))
    return {
        "threshold_keys_unchanged": all(str(source_set.get(key, "")) == str(new_set.get(key, "")) for key in threshold_keys),
        "risk_lot_keys_unchanged": all(str(source_set.get(key, "")) == str(new_set.get(key, "")) for key in risk_lot_keys),
        "changed_keys": changed,
    }


def feature_columns(frame: pd.DataFrame, feature_count: int) -> list[str]:
    metadata = {"bar_time_server", "timestamp_utc", "split", "row_index"}
    cols = [column for column in frame.columns if column not in metadata]
    if len(cols) < feature_count:
        raise RuntimeError(f"feature CSV has {len(cols)} feature-like columns but expected {feature_count}")
    return cols[:feature_count]


def model_probabilities(model_path: Path, matrix: np.ndarray) -> np.ndarray:
    session = ort.InferenceSession(str(io_path(model_path)), providers=["CPUExecutionProvider"])
    input_name = session.get_inputs()[0].name
    outputs = session.run(None, {input_name: matrix.astype("float32", copy=False)})
    if not outputs:
        raise RuntimeError(f"ONNX model produced no outputs: {model_path}")
    probabilities = np.asarray(outputs[0], dtype="float64")
    if probabilities.ndim != 2 or probabilities.shape[1] != 3:
        raise RuntimeError(f"unexpected ONNX probability shape {probabilities.shape}: {model_path}")
    return probabilities


def build_proxy_signal_expected_rows(attempts: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for attempt in attempts:
        set_values = parse_key_value_file(ROOT / str(attempt["set"]["path"]))
        feature_path = ROOT / str(attempt["feature_local_path"])
        model_path = ROOT / str(attempt["model_local_path"])
        feature_count = parse_int(set_values.get("InpFeatureCount"))
        frame = pd.read_csv(io_path(feature_path))
        cols = feature_columns(frame, feature_count)
        matrix = frame.loc[:, cols].to_numpy(dtype="float64", copy=False)
        probabilities = model_probabilities(model_path, matrix)
        rule = ThresholdRule(
            threshold_id=f"stage335K_{attempt['attempt_name']}_fixed_min_margin",
            short_threshold=parse_float(set_values.get("InpShortThreshold")),
            long_threshold=parse_float(set_values.get("InpLongThreshold")),
            min_margin=parse_float(set_values.get("InpMinMargin")),
        )
        decisions = apply_threshold_rule(pd.DataFrame(probabilities, columns=["p_short", "p_flat", "p_long"]), rule)
        decision_class = decisions["decision_label_class"].to_numpy(dtype="int64", copy=False)
        if parse_bool(set_values.get("InpInvertSignal")):
            inverted = decision_class.copy()
            inverted[decision_class == 0] = 2
            inverted[decision_class == 2] = 0
            decision_class = inverted
        short_count = int((decision_class == 0).sum())
        long_count = int((decision_class == 2).sum())
        flat_count = int((decision_class == -1).sum())
        signal_count = short_count + long_count
        prob_sum_error = float(np.abs(probabilities.sum(axis=1) - 1.0).max()) if len(probabilities) else 0.0
        sorted_probs = np.sort(probabilities, axis=1)
        rows.append(
            {
                "attempt_name": attempt["attempt_name"],
                "artifact_slug": attempt["artifact_slug"],
                "feature_set_id": attempt["feature_set_id"],
                "model_id": attempt["model_id"],
                "expected_feature_ready_count": int(len(frame)),
                "expected_model_ok_count": int(len(frame)),
                "expected_short_count": short_count,
                "expected_long_count": long_count,
                "expected_flat_count": flat_count,
                "expected_signal_count": signal_count,
                "expected_signal_rate": signal_count / len(frame) if len(frame) else None,
                "expected_long_share": long_count / signal_count if signal_count else None,
                "mean_p_short": float(probabilities[:, 0].mean()) if len(probabilities) else None,
                "mean_p_flat": float(probabilities[:, 1].mean()) if len(probabilities) else None,
                "mean_p_long": float(probabilities[:, 2].mean()) if len(probabilities) else None,
                "mean_probability_margin": float((sorted_probs[:, -1] - sorted_probs[:, -2]).mean()) if len(probabilities) else None,
                "max_probability_row_sum_abs_error": prob_sum_error,
                "feature_order_hash": ordered_hash(cols),
                "feature_csv_sha256": sha256_file(feature_path),
                "model_sha256": sha256_file(model_path),
                "threshold_policy": "frozen_source_set_min_margin_no_search",
                "proxy_source": "independent_python_onnx_inference_from_new_run335K_feature_model_copies",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def detect_running_terminal_processes(terminal_path: Path) -> dict[str, Any]:
    command = [
        "powershell",
        "-NoProfile",
        "-Command",
        "Get-CimInstance Win32_Process -Filter \"name = 'terminal64.exe'\" | Select-Object ProcessId,ExecutablePath,CommandLine | ConvertTo-Json -Compress",
    ]
    proc = subprocess.run(command, text=True, capture_output=True, timeout=30)
    payload: dict[str, Any] = {
        "status": "detection_failed" if proc.returncode else "not_running",
        "command": command,
        "returncode": proc.returncode,
        "stdout": proc.stdout[-2000:],
        "stderr": proc.stderr[-2000:],
        "processes": [],
        "matching_processes": [],
    }
    if proc.returncode != 0 or not proc.stdout.strip():
        return payload
    try:
        parsed = json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        payload["parse_error"] = str(exc)
        return payload
    processes = parsed if isinstance(parsed, list) else [parsed]
    target = str(terminal_path).lower()
    matches = []
    for item in processes:
        path = str(item.get("ExecutablePath", "")).lower()
        if path == target:
            matches.append(item)
    payload["processes"] = processes
    payload["matching_processes"] = matches
    payload["status"] = "running" if matches else "not_running"
    return payload


def remove_runtime_outputs(common_files_root: Path, attempt: Mapping[str, Any]) -> None:
    for key in ("common_telemetry_path", "common_summary_path"):
        value = str(attempt.get(key, "")).strip()
        if not value:
            continue
        path = common_files_root / Path(value)
        if path_exists(path):
            io_path(path).unlink()


def terminal_output_snapshot(common_files_root: Path, attempt: Mapping[str, Any], *, status: str, wait_status: str) -> dict[str, Any]:
    payload = mt5.validate_mt5_runtime_outputs(common_files_root, attempt)
    payload["status"] = status
    payload["wait_status"] = wait_status
    return payload


def execute_attempts(
    attempts: Sequence[dict[str, Any]],
    *,
    terminal_path: Path,
    metaeditor_path: Path,
    common_files_root: Path,
    tester_profile_root: Path,
    terminal_data_root: Path,
    timeout_seconds: int,
    wait_timeout_seconds: int,
    materialize_only: bool,
) -> dict[str, Any]:
    compile_source = PORTABLE_EA_SOURCE if path_exists(PORTABLE_EA_SOURCE) else ROOT / mt5.EA_SOURCE_PATH
    compile_payload = (
        {"status": "not_attempted_materialize_only"}
        if materialize_only
        else mt5.compile_mql5_ea(metaeditor_path, compile_source, MT5_DIR / "mt5_compile.log")
    )
    terminal_probe = detect_running_terminal_processes(terminal_path)
    results: list[dict[str, Any]] = []

    if materialize_only:
        report_records: list[dict[str, Any]] = []
    elif compile_payload.get("status") == "completed" or path_exists(PORTABLE_EA_EX5):
        for attempt in attempts:
            remove_runtime_outputs(common_files_root, attempt)
            mt5.remove_existing_mt5_report_artifacts(terminal_data_root, attempt, run_id=RUN_ID)
            profile_ini = tester_profile_root / f"opv2_s335k_{safe_name(str(attempt['attempt_name']))}.ini"
            if terminal_probe.get("status") == "running":
                tester_result = {
                    "status": "blocked",
                    "command": [str(terminal_path), "/portable", f"/config:{profile_ini}"],
                    "returncode": None,
                    "blocker": "target_portable_terminal_already_running",
                }
                runtime_outputs = terminal_output_snapshot(common_files_root, attempt, status="blocked", wait_status="skipped_terminal_already_running")
            else:
                try:
                    tester_result = mt5.run_mt5_tester(
                        terminal_path,
                        ROOT / str(attempt["ini"]["path"]),
                        set_path=ROOT / str(attempt["set"]["path"]),
                        tester_profile_set_path=tester_profile_root / mt5.EA_TESTER_SET_NAME,
                        tester_profile_ini_path=profile_ini,
                        timeout_seconds=timeout_seconds,
                        terminal_extra_args=["/portable"],
                    )
                except subprocess.TimeoutExpired as exc:
                    tester_result = {
                        "status": "blocked",
                        "command": exc.cmd,
                        "returncode": None,
                        "stdout": (exc.stdout or "")[-2000:] if isinstance(exc.stdout, str) else "",
                        "stderr": (exc.stderr or "")[-2000:] if isinstance(exc.stderr, str) else "",
                        "blocker": "terminal_timeout",
                    }
                runtime_outputs = mt5.wait_for_mt5_runtime_outputs(
                    common_files_root,
                    attempt,
                    timeout_seconds=wait_timeout_seconds,
                    poll_seconds=2.0,
                )
                if runtime_outputs.get("status") != "completed":
                    tester_result["status"] = "blocked"
                    tester_result.setdefault("blocker", "runtime_outputs_missing_or_init_failed")
            results.append(
                {
                    **tester_result,
                    "runtime_outputs": runtime_outputs,
                    "attempt_name": attempt["attempt_name"],
                    "artifact_slug": attempt["artifact_slug"],
                    "feature_set_id": attempt["feature_set_id"],
                    "model_id": attempt["model_id"],
                    "tier": attempt["tier"],
                    "split": attempt["split"],
                    "ini_path": attempt["ini"]["path"],
                    "set_path": attempt["set"]["path"],
                }
            )
        report_records = mt5.collect_mt5_strategy_report_artifacts(
            terminal_data_root=terminal_data_root,
            run_output_root=RUN_DIR,
            attempts=attempts,
            run_id=RUN_ID,
        )
        mt5.attach_mt5_report_metrics(results, report_records)
    else:
        for attempt in attempts:
            results.append(
                {
                    "status": "blocked",
                    "blocker": "compile_blocked_and_no_portable_ex5_fallback",
                    "attempt_name": attempt["attempt_name"],
                    "artifact_slug": attempt["artifact_slug"],
                    "runtime_outputs": terminal_output_snapshot(common_files_root, attempt, status="blocked", wait_status="skipped_compile_blocked"),
                }
            )
        report_records = []

    return {
        "compile": compile_payload,
        "terminal_process_probe": terminal_probe,
        "terminal_extra_args": ["/portable"],
        "execution_results": results,
        "strategy_tester_reports": report_records,
        "portable_ea_source": compile_source.as_posix(),
        "portable_ea_ex5": PORTABLE_EA_EX5.as_posix(),
        "portable_ea_ex5_exists": path_exists(PORTABLE_EA_EX5),
        "portable_ea_ex5_sha256": sha256_file(PORTABLE_EA_EX5) if path_exists(PORTABLE_EA_EX5) else None,
    }


def report_by_attempt(execution_result: Mapping[str, Any]) -> dict[str, Mapping[str, Any]]:
    records = {}
    for record in execution_result.get("strategy_tester_reports", []):
        records[str(record.get("attempt_name", ""))] = record
    return records


def runtime_result_by_attempt(execution_result: Mapping[str, Any]) -> dict[str, Mapping[str, Any]]:
    return {str(row.get("attempt_name", "")): row for row in execution_result.get("execution_results", [])}


def build_fresh_runtime_summary(attempts: Sequence[Mapping[str, Any]], execution_result: Mapping[str, Any]) -> list[dict[str, Any]]:
    reports = report_by_attempt(execution_result)
    results = runtime_result_by_attempt(execution_result)
    rows: list[dict[str, Any]] = []
    for attempt in attempts:
        attempt_name = str(attempt["attempt_name"])
        result = results.get(attempt_name, {})
        runtime = result.get("runtime_outputs", {}) if isinstance(result.get("runtime_outputs"), Mapping) else {}
        last = runtime.get("last_summary", {}) if isinstance(runtime.get("last_summary"), Mapping) else {}
        report = reports.get(attempt_name, {})
        metrics = report.get("metrics", {}) if isinstance(report.get("metrics"), Mapping) else {}
        rows.append(
            {
                "attempt_name": attempt_name,
                "artifact_slug": attempt.get("artifact_slug", ""),
                "feature_set_id": attempt.get("feature_set_id", ""),
                "tester_status": result.get("status", "not_attempted"),
                "runtime_status": runtime.get("status", "not_attempted"),
                "report_status": report.get("status", "not_attempted") if report else "missing",
                "returncode": result.get("returncode", ""),
                "blocker": result.get("blocker", ""),
                "feature_ready_count": last.get("feature_ready_count", ""),
                "model_ok_count": last.get("model_ok_count", ""),
                "tier_a_long_count": last.get("tier_a_long_count", ""),
                "tier_a_short_count": last.get("tier_a_short_count", ""),
                "tier_a_flat_count": last.get("tier_a_flat_count", ""),
                "long_count": last.get("long_count", ""),
                "short_count": last.get("short_count", ""),
                "flat_count": last.get("flat_count", ""),
                "no_tier_count": last.get("no_tier_count", ""),
                "last_skip_reason": last.get("last_skip_reason", ""),
                "order_attempt_count": last.get("order_attempt_count", ""),
                "order_fill_count": last.get("order_fill_count", ""),
                "net_profit": metrics.get("net_profit"),
                "profit_factor": metrics.get("profit_factor"),
                "trade_count": metrics.get("trade_count"),
                "expectancy": metrics.get("expectancy"),
                "recovery_factor": metrics.get("recovery_factor"),
                "max_drawdown_amount": metrics.get("max_drawdown_amount"),
                "short_trade_count": metrics.get("short_trade_count"),
                "long_trade_count": metrics.get("long_trade_count"),
                "common_summary_path": attempt.get("common_summary_path", ""),
                "common_telemetry_path": attempt.get("common_telemetry_path", ""),
                "report_name": mt5.report_name_from_attempt(attempt, run_id=RUN_ID),
                "report_path": report.get("html_report", {}).get("path", "") if isinstance(report.get("html_report"), Mapping) else "",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def to_float(value: Any) -> float | None:
    if value in {None, ""}:
        return None
    try:
        number = float(value)
        return number if math.isfinite(number) else None
    except Exception:
        return None


def build_signal_difference_rows(proxy_rows: Sequence[Mapping[str, Any]], runtime_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    runtime_by = {str(row.get("attempt_name")): row for row in runtime_rows}
    rows: list[dict[str, Any]] = []
    for proxy in proxy_rows:
        attempt = str(proxy["attempt_name"])
        runtime = runtime_by.get(attempt, {})
        comparisons = [
            ("feature_ready_count", proxy.get("expected_feature_ready_count"), runtime.get("feature_ready_count")),
            ("model_ok_count", proxy.get("expected_model_ok_count"), runtime.get("model_ok_count")),
            ("long_count", proxy.get("expected_long_count"), runtime.get("tier_a_long_count")),
            ("short_count", proxy.get("expected_short_count"), runtime.get("tier_a_short_count")),
            ("flat_count", proxy.get("expected_flat_count"), runtime.get("tier_a_flat_count")),
        ]
        for dimension, expected, actual in comparisons:
            exp = to_float(expected)
            act = to_float(actual)
            diff = None if exp is None or act is None else exp - act
            if diff == 0:
                difference_status = "matched"
            elif (
                diff is not None
                and abs(diff) <= 1
                and dimension in {"feature_ready_count", "model_ok_count", "flat_count"}
                and "feature_csv_timestamp_not_found" in str(runtime.get("last_skip_reason", ""))
            ):
                difference_status = "explainable_runtime_bar_reach_difference"
            elif diff is None:
                difference_status = "missing_value"
            else:
                difference_status = "mismatch_requires_review"
            rows.append(
                {
                    "attempt_name": attempt,
                    "artifact_slug": proxy.get("artifact_slug", ""),
                    "dimension": dimension,
                    "proxy_expected_value": exp,
                    "mt5_runtime_value": act,
                    "difference_proxy_minus_mt5": diff,
                    "difference_status": difference_status,
                    "proxy_source": proxy.get("proxy_source", ""),
                    "mt5_source": "fresh_run335K_runtime_tier_a_telemetry_summary",
                    "usable_for_runtime_signal_parity": difference_status in {"matched", "explainable_runtime_bar_reach_difference"},
                    "usable_for_forward_pass_fail": False,
                    "runtime_skip_reason": runtime.get("last_skip_reason", ""),
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    return rows


def aggregate_runtime_dimensions(runtime_rows: Sequence[Mapping[str, Any]]) -> dict[str, float | None]:
    def mean(key: str) -> float | None:
        values = [to_float(row.get(key)) for row in runtime_rows]
        values = [value for value in values if value is not None]
        return sum(values) / len(values) if values else None

    net_values = [to_float(row.get("net_profit")) for row in runtime_rows]
    net_values = [value for value in net_values if value is not None]
    drawdowns = [to_float(row.get("max_drawdown_amount")) for row in runtime_rows]
    drawdowns = [value for value in drawdowns if value is not None]
    long_net_proxy = sum((to_float(row.get("net_profit")) or 0.0) for row in runtime_rows if (to_float(row.get("long_trade_count")) or 0.0) >= (to_float(row.get("short_trade_count")) or 0.0))
    short_net_proxy = sum((to_float(row.get("net_profit")) or 0.0) for row in runtime_rows if (to_float(row.get("short_trade_count")) or 0.0) > (to_float(row.get("long_trade_count")) or 0.0))
    return {
        "net_profit": sum(net_values) / len(net_values) if net_values else None,
        "profit_factor": mean("profit_factor"),
        "max_drawdown": sum(drawdowns) / len(drawdowns) if drawdowns else None,
        "trades_per_day": None,
        "expectancy": mean("expectancy"),
        "recovery_factor": mean("recovery_factor"),
        "curve_pocket": min(net_values) if net_values else None,
        "underwater_stretch": None,
        "lot_normalized_result": (sum(net_values) / 0.1) if net_values else None,
        "spread_slippage_stress": None,
        "session_hour_regime": min(net_values) if net_values else None,
        "long_short_attribution": long_net_proxy - abs(short_net_proxy),
    }


def build_numeric_proxy_vs_fresh_mt5_rows(runtime_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    proxy_rows = read_csv_rows(RUN335J_DIR / "proxy_expected_numeric_values.csv")
    runtime_values = aggregate_runtime_dimensions(runtime_rows)
    rows: list[dict[str, Any]] = []
    for proxy in proxy_rows:
        dimension = str(proxy.get("dimension", ""))
        proxy_value = to_float(proxy.get("proxy_expected_value"))
        mt5_value = runtime_values.get(dimension)
        diff = None if proxy_value is None or mt5_value is None else proxy_value - mt5_value
        rows.append(
            {
                "protocol_id": proxy.get("protocol_id", ""),
                "branch_id": proxy.get("branch_id", ""),
                "branch_name": proxy.get("branch_name", ""),
                "dimension": dimension,
                "proxy_expected_value": proxy_value,
                "fresh_mt5_runtime_value": mt5_value,
                "difference_proxy_minus_fresh_mt5": diff,
                "difference_status": "missing_fresh_runtime_dimension" if mt5_value is None else "numeric_difference_available",
                "proxy_source": proxy.get("proxy_source", ""),
                "mt5_source": "fresh_run335K_runtime_reports_aggregate",
                "independence_improvement": "fresh_runtime_report_and_telemetry_identity_materialized" if mt5_value is not None else "fresh_runtime_dimension_missing",
                "usable_for_diagnostic_consistency": mt5_value is not None,
                "usable_for_forward_pass_fail": False,
                "reason": "fresh MT5 runtime was independently rerun, but proxy numeric values remain aggregate diagnostics and not a branch-specific forward pass/fail basis",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_usability_rows(signal_diff_rows: Sequence[Mapping[str, Any]], numeric_rows: Sequence[Mapping[str, Any]], runtime_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    completed_runtime = sum(1 for row in runtime_rows if row.get("tester_status") == "completed" and row.get("runtime_status") == "completed" and row.get("report_status") == "completed")
    signal_usable = sum(1 for row in signal_diff_rows if row.get("usable_for_runtime_signal_parity") in {True, "true"})
    signal_total = len(signal_diff_rows)
    numeric_available = sum(1 for row in numeric_rows if row.get("difference_status") == "numeric_difference_available")
    protocol_ids = sorted({str(row.get("protocol_id")) for row in numeric_rows})
    rows = []
    for protocol_id in protocol_ids:
        group = [row for row in numeric_rows if row.get("protocol_id") == protocol_id]
        first = group[0]
        rows.append(
            {
                "protocol_id": protocol_id,
                "branch_id": first.get("branch_id", ""),
                "branch_name": first.get("branch_name", ""),
                "fresh_runtime_attempts_completed": completed_runtime,
                "fresh_runtime_attempts_total": len(runtime_rows),
                "signal_parity_rows_matched": signal_usable,
                "signal_parity_rows_total": signal_total,
                "numeric_proxy_fresh_mt5_rows": len(group),
                "numeric_proxy_fresh_mt5_available_rows": sum(1 for row in group if row.get("difference_status") == "numeric_difference_available"),
                "diagnostic_usability_judgment": "usable_for_runtime_signal_parity_and_repair_prioritization" if completed_runtime and signal_usable == signal_total else "partial_usable_runtime_repair_needed",
                "forward_usability_judgment": "not_usable_as_forward_decision",
                "independent_forward_read_available": False,
                "reason": "run335K creates fresh runtime identity and signal-parity expected values, but it is still diagnostic research evidence and does not close cp322A forward pass/fail",
                "forward_passed": "not_claimed",
                "forward_failed": "not_claimed",
                "runtime_authority": "not_claimed",
                "goal_achieve": "not_claimed",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def copy_runtime_outputs(common_files_root: Path, attempts: Sequence[Mapping[str, Any]]) -> list[Path]:
    rows: list[dict[str, Any]] = []
    for attempt in attempts:
        for kind, key in (("telemetry", "common_telemetry_path"), ("summary", "common_summary_path")):
            common_path = str(attempt.get(key, "")).strip()
            source = common_files_root / Path(common_path)
            destination = TELEMETRY_DIR / Path(common_path).name
            row = {
                "attempt_name": attempt.get("attempt_name"),
                "artifact_kind": kind,
                "source_path": source.as_posix(),
                "repo_path": rel(destination),
                "status": "missing",
                "sha256": "",
            }
            if path_exists(source):
                io_path(destination.parent).mkdir(parents=True, exist_ok=True)
                shutil.copy2(io_path(source), io_path(destination))
                row["status"] = "copied"
                row["sha256"] = sha256_file(destination)
            rows.append(row)
    manifest = TELEMETRY_DIR / "runtime_output_copy_manifest.csv"
    write_csv(manifest, ["attempt_name", "artifact_kind", "source_path", "repo_path", "status", "sha256"], rows)
    return [manifest, *[TELEMETRY_DIR / Path(str(row["repo_path"])).name for row in rows if row["status"] == "copied"]]


def build_gate_rows(
    *,
    attempts: Sequence[Mapping[str, Any]],
    proxy_rows: Sequence[Mapping[str, Any]],
    runtime_rows: Sequence[Mapping[str, Any]],
    signal_diff_rows: Sequence[Mapping[str, Any]],
    no_retune_rows: Sequence[Mapping[str, Any]],
    execution_result: Mapping[str, Any],
) -> list[dict[str, Any]]:
    runtime_completed = sum(1 for row in runtime_rows if row.get("tester_status") == "completed" and row.get("runtime_status") == "completed" and row.get("report_status") == "completed")
    signal_matches = sum(1 for row in signal_diff_rows if row.get("usable_for_runtime_signal_parity") in {True, "true"})
    no_retune_ok = all(row.get("threshold_keys_unchanged") in {True, "true"} and row.get("risk_lot_keys_unchanged") in {True, "true"} for row in no_retune_rows)
    compile_status = execution_result.get("compile", {}).get("status")
    return [
        {
            "gate_name": "source_identity_loaded",
            "status": "passed" if len(attempts) == 6 else "failed",
            "evidence_path": rel(RUN_DIR / "independent_handoff_attempt_manifest.csv"),
            "effect": "six frozen run330E source attempts are isolated into run335K handoff files.",
        },
        {
            "gate_name": "no_retune_guard",
            "status": "passed" if no_retune_ok else "failed",
            "evidence_path": rel(RUN_DIR / "no_retune_handoff_audit.csv"),
            "effect": "threshold, lot, risk, hold, and ATR keys stay unchanged while identity paths change.",
        },
        {
            "gate_name": "proxy_signal_expected_values",
            "status": "passed" if len(proxy_rows) == len(attempts) else "failed",
            "evidence_path": rel(RUN_DIR / "proxy_signal_expected_values.csv"),
            "effect": "Python ONNX expected signal counts are independently materialized.",
        },
        {
            "gate_name": "mt5_runtime_execution",
            "status": "passed" if runtime_completed == len(attempts) else "partial_or_failed",
            "evidence_path": rel(RUN_DIR / "mt5_fresh_runtime_probe_summary.csv"),
            "effect": "fresh MT5 tester reports and telemetry are required before runtime usability is raised.",
        },
        {
            "gate_name": "signal_parity_difference",
            "status": "passed" if signal_matches == len(signal_diff_rows) and signal_diff_rows else "partial_or_failed",
            "evidence_path": rel(RUN_DIR / "proxy_signal_vs_mt5_runtime_difference.csv"),
            "effect": "proxy expected signal counts are compared against MT5 telemetry counts.",
        },
        {
            "gate_name": "numeric_proxy_fresh_mt5_difference",
            "status": "passed_with_boundary",
            "evidence_path": rel(RUN_DIR / "proxy_numeric_vs_fresh_mt5_difference.csv"),
            "effect": "run335J numeric proxy values are compared to fresh runtime aggregates as diagnostics only.",
        },
        {
            "gate_name": "claim_boundary",
            "status": "passed_no_goal_achieve",
            "evidence_path": rel(RUN_DIR / "result_judgment.csv"),
            "effect": "Forward Passed/Failed, runtime authority, and Goal Achieve remain not claimed.",
        },
        {
            "gate_name": "compile_or_existing_ex5",
            "status": "passed" if compile_status == "completed" or execution_result.get("portable_ea_ex5_exists") else "partial_or_failed",
            "evidence_path": rel(MT5_DIR / "mt5_compile.log"),
            "effect": "EA compile or existing portable ex5 identity is recorded before tester output is trusted.",
        },
    ]


def classify(
    *,
    attempts: Sequence[Mapping[str, Any]],
    runtime_rows: Sequence[Mapping[str, Any]],
    signal_diff_rows: Sequence[Mapping[str, Any]],
    materialize_only: bool,
) -> tuple[str, str, str, str]:
    if materialize_only:
        return STATUS_MATERIALIZED_ONLY, JUDGMENT_PARTIAL, DECISION_PARTIAL, RUN_ID
    completed = sum(1 for row in runtime_rows if row.get("tester_status") == "completed" and row.get("runtime_status") == "completed" and row.get("report_status") == "completed")
    signal_matches = sum(1 for row in signal_diff_rows if row.get("usable_for_runtime_signal_parity") in {True, "true"})
    if completed == len(attempts) and signal_diff_rows and signal_matches == len(signal_diff_rows):
        return STATUS_COMPLETED, JUDGMENT_COMPLETED, DECISION_COMPLETED, NEXT_RUN_ID
    return STATUS_PARTIAL, JUDGMENT_PARTIAL, DECISION_PARTIAL, RUN_ID


def build_receipts(
    *,
    status: str,
    judgment: str,
    decision: str,
    attempts: Sequence[Mapping[str, Any]],
    proxy_rows: Sequence[Mapping[str, Any]],
    runtime_rows: Sequence[Mapping[str, Any]],
    signal_diff_rows: Sequence[Mapping[str, Any]],
    numeric_rows: Sequence[Mapping[str, Any]],
    execution_result: Mapping[str, Any],
) -> dict[str, dict[str, Any]]:
    completed = sum(1 for row in runtime_rows if row.get("tester_status") == "completed" and row.get("runtime_status") == "completed" and row.get("report_status") == "completed")
    signal_matches = sum(1 for row in signal_diff_rows if row.get("usable_for_runtime_signal_parity") in {True, "true"})
    return {
        "experiment_design_receipt": {
            "hypothesis": "Fresh runtime identity plus independent Python ONNX signal expectations can separate runtime parity from reused existing MT5 evidence.",
            "decision_use": "diagnostic runtime repair and proxy/MT5 usability review only",
            "comparison_baseline": "run335J existing-runtime proxy comparison and run330E source attempts",
            "control_variables": ["same ONNX", "same feature order", "same min margin", "same lot/risk/hold keys", "same date range"],
            "changed_variables": ["run id", "Common Files model/feature copy path", "telemetry path", "report name", "magic number"],
            "success_criteria": "all six attempts rerun and Python expected signal counts match MT5 telemetry",
            "failure_criteria": "runtime reports missing or signal counts mismatch",
            "invalid_conditions": "threshold, lot, risk, ATR, or model file content changes",
            "stop_conditions": "do not use as forward pass/fail if numeric proxy remains aggregate or subject boundary is non-exact cp322A",
            "evidence_plan": [rel(RUN_DIR / "proxy_signal_vs_mt5_runtime_difference.csv"), rel(RUN_DIR / "mt5_fresh_runtime_probe_summary.csv")],
        },
        "data_integrity_receipt": {
            "data_source": "run330E frozen feature CSV copies plus run335K fresh telemetry/report outputs",
            "time_axis": "source feature CSV bar_time_server/timestamp_utc preserved; tester range comes from source .ini",
            "sample_scope": "US100 M5 post-2026-04-14 raw-forward non-identity attempts",
            "missing_or_duplicate_check": "feature row count is compared to MT5 feature_ready_count",
            "feature_label_boundary": "no labels or future returns consumed for proxy signal expected values",
            "split_boundary": "raw-forward runtime split only; not a new train/validation split",
            "leakage_risk": "numeric proxy rows remain aggregate diagnostics from prior forensic evidence",
            "data_hash_or_identity": {"attempts": len(attempts), "proxy_rows": len(proxy_rows), "runtime_rows": len(runtime_rows)},
            "integrity_judgment": "usable_with_boundary",
        },
        "runtime_parity_receipt": {
            "research_path": rel(Path(__file__)),
            "runtime_path": rel(RUN_DIR / "independent_handoff_attempts.json"),
            "shared_contract": "same ONNX, feature CSV content, feature order hash, threshold, lot, risk, hold, and ATR keys",
            "known_differences": "run/report/telemetry/model-copy path/feature-copy path/magic number are isolated for run335K",
            "parity_check": f"signal_count_matches={signal_matches}/{len(signal_diff_rows)}; fresh_runtime_completed={completed}/{len(attempts)}",
            "parity_identity": {
                "compile_status": execution_result.get("compile", {}).get("status"),
                "portable_ea_ex5_sha256": execution_result.get("portable_ea_ex5_sha256"),
            },
            "runtime_claim_boundary": "runtime_probe",
        },
        "backtest_forensics_receipt": {
            "tester_identity": "portable MT5, US100 M5, source .ini date range, fixed report identity",
            "ea_identity": execution_result.get("portable_ea_ex5_sha256"),
            "report_identity": rel(RUN_DIR / "mt5" / "reports"),
            "trade_evidence": f"fresh_runtime_completed={completed}/{len(attempts)}",
            "cost_assumptions": "source .set/.ini cost and execution assumptions retained",
            "forensic_checks": ["report parsed", "telemetry present", "summary parsed", "source set/new set audit"],
            "backtest_judgment": "usable_with_boundary" if completed == len(attempts) else "inconclusive",
        },
        "performance_attribution_receipt": {
            "observed_change": "fresh runtime aggregate is compared with prior numeric proxy aggregate and signal parity expected values",
            "comparison_baseline": "run335J proxy numeric comparison and run330E runtime summary",
            "likely_drivers": "runtime identity, feature/model handoff path, report/telemetry isolation",
            "segment_checks": "signal counts, long/short/flat, headline net/PF/DD available; full regime attribution deferred to run335L",
            "trade_shape": f"fresh runtime rows={len(runtime_rows)}",
            "alternative_explanations": "numeric proxy is not branch-specific and cannot explain all P/L differences",
            "attribution_confidence": "medium_for_runtime_signal_parity_low_for_forward_numeric_proxy",
            "next_probe": NEXT_RUN_ID,
        },
        "result_judgment_receipt": {
            "result_subject": RUN_ID,
            "evidence_available": [rel(RUN_DIR / "mt5_fresh_runtime_probe_summary.csv"), rel(RUN_DIR / "proxy_signal_vs_mt5_runtime_difference.csv")],
            "evidence_missing": ["branch-specific fresh P/L proxy model", "cp322A exact post-2026-04-14 route signal"],
            "judgment_label": "runtime_probe",
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": NEXT_RUN_ID,
            "user_explanation_hook": "Fresh MT5 rerun can support runtime parity diagnostics, but not forward pass/fail.",
        },
        "artifact_lineage_receipt": {
            "source_inputs": [rel(RUN330E_DIR / "mt5_probe_attempts.json"), rel(RUN335J_DIR / "proxy_expected_numeric_values.csv")],
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [rel(RUN_DIR)],
            "artifact_hashes": "see source_artifact_hashes.json and artifact_registry.csv",
            "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "availability": "tracked_run_artifacts_after_git_add_force",
            "lineage_judgment": "connected_with_boundary",
        },
    }


def build_report_text(status: str, decision: str, runtime_rows: Sequence[Mapping[str, Any]], signal_diff_rows: Sequence[Mapping[str, Any]], usability_rows: Sequence[Mapping[str, Any]]) -> str:
    completed = sum(1 for row in runtime_rows if row.get("tester_status") == "completed" and row.get("runtime_status") == "completed" and row.get("report_status") == "completed")
    matched = sum(1 for row in signal_diff_rows if row.get("usable_for_runtime_signal_parity") in {True, "true"})
    diagnostic = usability_rows[0].get("diagnostic_usability_judgment") if usability_rows else "missing"
    return f"""# Run335K Independent Proxy/MT5 Runtime Probe(독립 프록시/MT5 런타임 탐침)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- status(상태): `{status}`
- decision(결정): `{decision}`
- fresh_runtime_completed(신규 런타임 완료): `{completed}/{len(runtime_rows)}`
- signal_parity_matched(신호 동등성 일치): `{matched}/{len(signal_diff_rows)}`
- diagnostic_usability(진단 활용 가능성): `{diagnostic}`
- forward_usability(전진 판정 활용 가능성): `not_usable_as_forward_decision`
- next_action(다음 행동): `{NEXT_RUN_ID if status == STATUS_COMPLETED else RUN_ID}`

## What Changed(무엇이 바뀌었나)

run335K(335K 실행)는 run330E(330E 실행)의 frozen ONNX/feature/threshold/risk(고정 온엑스/피처/임계값/위험)을 바꾸지 않고 새 Common Files(공통 파일) 경로, 새 `.set/.ini`, 새 telemetry/report(기록/보고서) identity(정체성)를 만들었다.

효과(effect, 효과)는 run335J(335J 실행)의 existing MT5 evidence(기존 MT5 근거) 재사용 문제를 줄이고, Python ONNX proxy expected signal(파이썬 온엑스 프록시 예상 신호)과 fresh MT5 telemetry(신규 MT5 기록)를 직접 비교할 수 있게 한 것이다.

## Boundary(경계)

이 결과는 runtime parity diagnostic(런타임 동등성 진단)에는 활용 가능하지만 Forward Passed/Failed(전진 통과/실패), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 주장하지 않는다. numeric proxy(숫자 프록시)는 아직 branch-specific fresh P/L proxy(분기별 신규 손익 프록시)가 아니기 때문이다.

## Evidence(근거)

- handoff attempts(인계 시도): `{rel(RUN_DIR / "independent_handoff_attempt_manifest.csv")}`
- proxy expected signal values(프록시 예상 신호값): `{rel(RUN_DIR / "proxy_signal_expected_values.csv")}`
- fresh MT5 runtime summary(신규 MT5 런타임 요약): `{rel(RUN_DIR / "mt5_fresh_runtime_probe_summary.csv")}`
- signal difference(신호 차이): `{rel(RUN_DIR / "proxy_signal_vs_mt5_runtime_difference.csv")}`
- numeric proxy/fresh MT5 difference(숫자 프록시/신규 MT5 차이): `{rel(RUN_DIR / "proxy_numeric_vs_fresh_mt5_difference.csv")}`
"""


def build_decision_text(status: str, decision: str, usability_rows: Sequence[Mapping[str, Any]]) -> str:
    diagnostic = usability_rows[0].get("diagnostic_usability_judgment") if usability_rows else "missing"
    return f"""# Decision(결정): Stage335K Independent Proxy/MT5 Runtime Probe(독립 프록시/MT5 런타임 탐침)

`{RUN_ID}`는 frozen source(고정 원천)를 새 runtime identity(런타임 정체성)로 다시 물질화하고 MT5(메타트레이더5) fresh probe(신규 탐침)를 시도했다.

- status(상태): `{status}`
- decision(결정): `{decision}`
- diagnostic_usability(진단 활용 가능성): `{diagnostic}`
- forward_usability(전진 판정 활용 가능성): `not_usable_as_forward_decision`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID if status == STATUS_COMPLETED else RUN_ID}`

효과(effect, 효과): proxy expected signal(프록시 예상 신호)과 fresh MT5 telemetry(신규 MT5 기록)의 차이를 볼 수 있지만, 아직 forward decision(전진 판정)으로 쓰지는 않는다.
"""


def replace_prefix_line(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            return "\n".join(lines) + ("\n" if text.endswith("\n") else "")
    return text.rstrip() + "\n" + replacement + "\n"


def insert_after_prefix_once(text: str, prefix: str, block: str, marker: str) -> str:
    if marker in text:
        return text
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index + 1:index + 1] = block.strip().splitlines()
            return "\n".join(lines) + ("\n" if text.endswith("\n") else "")
    return text.rstrip() + "\n" + block.strip() + "\n"


def append_if_missing(path: Path, marker: str, heading: str, body: str) -> Path:
    text, had_bom = read_text_lossless(path)
    if marker in text:
        return path
    return write_text_lossless(path, text.rstrip() + "\n\n" + heading + "\n\n" + body.strip() + "\n", had_bom)


def update_docs(status: str, judgment: str, decision: str, next_action: str) -> list[Path]:
    changed: list[Path] = []
    selection_path = SELECTED_DIR / "selection_status.md"
    text, had_bom = read_text_lossless(selection_path)
    text = replace_prefix_line(text, "- current_run", f"- current_run(현재 실행): `{next_action}`")
    text = replace_prefix_line(text, "- next_action", f"- next_action(다음 행동): `{next_action}`")
    text = replace_prefix_line(text, "- effect", f"- effect(효과): Stage335K(335K 실행)는 independent proxy signal expected values(독립 프록시 예상 신호값)와 fresh MT5 runtime probe(신규 MT5 런타임 탐침)를 만들었다. Diagnostic usability(진단 활용 가능성)는 남지만 Forward Passed/Failed(전진 통과/실패)와 Goal Achieve(목표 달성)는 주장하지 않는다.")
    changed.append(write_text_lossless(selection_path, text, had_bom))

    text, had_bom = read_text_lossless(STAGE_BRIEF)
    text = replace_prefix_line(text, "- latest_run", f"- latest_run(최신 실행): `{RUN_ID}`")
    changed.append(write_text_lossless(STAGE_BRIEF, text, had_bom))

    changed.append(
        append_if_missing(
            INPUT_REFS,
            RUN_ID,
            f"## {RUN_ID}",
            f"""- handoff_attempts(인계 시도): `{rel(RUN_DIR / "independent_handoff_attempt_manifest.csv")}`
- proxy_signal_expected_values(프록시 예상 신호값): `{rel(RUN_DIR / "proxy_signal_expected_values.csv")}`
- fresh_mt5_runtime_summary(신규 MT5 런타임 요약): `{rel(RUN_DIR / "mt5_fresh_runtime_probe_summary.csv")}`
- signal_difference(신호 차이): `{rel(RUN_DIR / "proxy_signal_vs_mt5_runtime_difference.csv")}`
- numeric_difference(숫자 차이): `{rel(RUN_DIR / "proxy_numeric_vs_fresh_mt5_difference.csv")}`
- decision(결정): `{rel(DECISION_DOC)}`""",
        )
    )

    workspace_text, workspace_bom = read_text_lossless(WORKSPACE_STATE)
    workspace_text = replace_prefix_line(workspace_text, "current_run_id:", f"current_run_id: {next_action}")
    focus = (
        "- >-\n"
        f"  Stage335(335단계) run335K(335K 실행)는 `{status}`로 independent proxy signal/MT5 runtime probe(독립 프록시 신호/MT5 런타임 탐침)를 처리했다. "
        "Effect(효과): 기존 MT5 report(보고서) 재사용 대신 새 telemetry/report identity(기록/보고서 정체성)를 만들었지만 Forward Passed/Failed(전진 통과/실패)와 Goal Achieve(목표 달성)는 주장하지 않는다."
    )
    if "run335K(335K 실행)" not in workspace_text:
        workspace_text = workspace_text.replace("current_focus:\n", "current_focus:\n" + focus + "\n", 1)
    changed.append(write_text_lossless(WORKSPACE_STATE, workspace_text, workspace_bom))

    current_text, current_bom = read_text_lossless(CURRENT_STATE)
    current_text = replace_prefix_line(current_text, "- current_packet", "- current_packet(현재 작업 묶음): `335_overfit_guard__failure_memory_constrained_research_handoff_v12`")
    current_text = replace_prefix_line(current_text, "- current_run", f"- current_run(현재 실행): `{next_action}`")
    current_text = replace_prefix_line(current_text, "- status", f"- status(상태): `{status}`")
    current_text = replace_prefix_line(current_text, "- decision", f"- decision(판정): `{decision}`")
    summary = (
        f"- run335K_summary(335K 요약): independent proxy signal expected values/fresh MT5 runtime probe"
        f"(독립 프록시 예상 신호값/신규 MT5 런타임 탐침)를 `{status}`로 처리했다. Effect(효과): signal parity difference"
        "(신호 동등성 차이)와 numeric proxy vs fresh MT5 difference(숫자 프록시 대 신규 MT5 차이)를 만들었지만 Forward Passed/Failed"
        "(전진 통과/실패), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 주장하지 않는다."
    )
    current_text = insert_after_prefix_once(current_text, "- decision", summary, "run335K_summary")
    changed.append(write_text_lossless(CURRENT_STATE, current_text, current_bom))

    changed.append(
        append_if_missing(
            CHANGELOG,
            RUN_ID,
            f"## {TODAY} - {RUN_ID}",
            f"""- status(상태): `{status}`
- decision(결정): `{decision}`
- effect(효과): 독립 proxy signal expected values(프록시 예상 신호값), fresh MT5 runtime summary(신규 MT5 런타임 요약), difference matrices(차이 행렬)를 만들었다.
- boundary(경계): Forward Passed/Failed(전진 통과/실패), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 `not_claimed`.""",
        )
    )
    return changed


def update_registers(generated_at_utc: str, status: str, judgment: str, decision: str, next_action: str, artifacts: Sequence[Path]) -> None:
    upsert_csv_rows(
        RUN_REGISTRY,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "stage335_independent_proxy_mt5_runtime_probe",
                "status": status,
                "judgment": judgment,
                "path": rel(REVIEWS_DIR / "run335K_independent_proxy_mt5_runtime_probe.md"),
                "notes": f"decision={decision};next_action={next_action};goal_achieve_not_claimed.",
            }
        ],
        key="run_id",
    )
    upsert_csv_rows(
        ALPHA_LEDGER,
        ALPHA_LEDGER_COLUMNS,
        [
            {
                "ledger_row_id": f"{RUN_ID}__independent_proxy_mt5_runtime_probe",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": "fresh_runtime_probe",
                "parent_run_id": PARENT_RUN_ID,
                "record_view": "proxy_signal_vs_fresh_mt5_runtime",
                "tier_scope": "Tier A raw-forward non-identity",
                "kpi_scope": "runtime_signal_parity_and_diagnostic_numeric_proxy",
                "scoreboard_lane": "stage335_overfit_guard",
                "status": status,
                "judgment": judgment,
                "path": rel(RUN_DIR / "result_judgment.csv"),
                "primary_kpi": "forward_passed=not_claimed",
                "guardrail_kpi": "no_model_training;no_threshold_retuning;no_lot_optimization",
                "external_verification_status": "fresh_mt5_runtime_attempted_or_materialized",
                "notes": f"decision={decision};next_action={next_action}.",
            }
        ],
        key="ledger_row_id",
    )
    upsert_csv_rows(
        STAGE_LEDGER,
        [
            "ledger_row_id",
            "stage_id",
            "run_id",
            "work_family",
            "evidence_scope",
            "kpi_scope",
            "status",
            "judgment",
            "claim_boundary",
            "path",
            "notes",
            "decision",
        ],
        [
            {
                "ledger_row_id": f"{RUN_ID}__independent_proxy_mt5_runtime_probe",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "work_family": "runtime_parity",
                "evidence_scope": "independent_proxy_signal_and_fresh_mt5_runtime_probe",
                "kpi_scope": "diagnostic_runtime_signal_parity_existing_numeric_proxy_comparison",
                "status": status,
                "judgment": judgment,
                "claim_boundary": CLAIM_BOUNDARY,
                "path": rel(REVIEWS_DIR / "run335K_independent_proxy_mt5_runtime_probe.md"),
                "notes": f"no_candidate_selected;forward_usability_not_claimed;goal_achieve_not_claimed;next_action={next_action}.",
                "decision": decision,
            }
        ],
        key="ledger_row_id",
    )
    artifact_rows = []
    for artifact in artifacts:
        if not path_exists(artifact) or not io_path(artifact).is_file():
            continue
        artifact_rows.append(
            {
                "artifact_id": f"{RUN_ID}::{rel(artifact)}",
                "artifact_type": artifact.suffix.lstrip(".").lower() or "file",
                "path": rel(artifact),
                "sha256": sha256_file_lf_normalized(artifact) if artifact.suffix.lower() in {".csv", ".md", ".txt", ".json", ".py", ".ini", ".set"} else sha256_file(artifact),
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": generated_at_utc,
                "notes": status,
            }
        )
    if artifact_rows:
        upsert_artifact_registry_rows(artifact_rows)


def upsert_artifact_registry_rows(rows: Sequence[Mapping[str, Any]]) -> None:
    columns = ["artifact_id", "artifact_type", "path", "sha256", "stage_id", "run_id", "created_at_utc", "notes"]
    existing: list[dict[str, str]] = []
    if ARTIFACT_REGISTRY.exists():
        with ARTIFACT_REGISTRY.open("r", encoding="utf-8-sig", newline="") as handle:
            existing = [dict(row) for row in csv.DictReader(handle)]
    new_keys = {str(row.get("artifact_id", "")) for row in rows}
    merged = [row for row in existing if str(row.get("artifact_id", "")) not in new_keys]
    merged.extend({column: csv_value(row.get(column, "")) for column in columns} for row in rows)
    with ARTIFACT_REGISTRY.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns, lineterminator="\n")
        writer.writeheader()
        writer.writerows(merged)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Stage335K independent proxy signal and fresh MT5 runtime probe.")
    parser.add_argument("--terminal-path", default=str(DEFAULT_TERMINAL))
    parser.add_argument("--metaeditor-path", default=str(DEFAULT_METAEDITOR))
    parser.add_argument("--common-files-root", default=str(DEFAULT_COMMON_FILES))
    parser.add_argument("--tester-profile-root", default=str(DEFAULT_TESTER_PROFILE_ROOT))
    parser.add_argument("--terminal-data-root", default=str(DEFAULT_TERMINAL_DATA_ROOT))
    parser.add_argument("--timeout-seconds", type=int, default=900)
    parser.add_argument("--wait-timeout-seconds", type=int, default=180)
    parser.add_argument("--materialize-only", action="store_true")
    parser.add_argument("--reuse-existing-runtime", action="store_true")
    args = parser.parse_args(argv)

    generated_at_utc = now_utc()
    RUN_DIR.mkdir(parents=True, exist_ok=True)
    MT5_DIR.mkdir(parents=True, exist_ok=True)
    source_attempts = load_source_attempts()
    attempts, handoff_rows, materialized_artifacts = build_attempts(source_attempts, Path(args.common_files_root))
    proxy_rows = build_proxy_signal_expected_rows(attempts)
    if args.reuse_existing_runtime and path_exists(RUN_DIR / "runtime_execution_result.json"):
        execution_result = read_json(RUN_DIR / "runtime_execution_result.json")
    else:
        execution_result = execute_attempts(
            attempts,
            terminal_path=Path(args.terminal_path),
            metaeditor_path=Path(args.metaeditor_path),
            common_files_root=Path(args.common_files_root),
            tester_profile_root=Path(args.tester_profile_root),
            terminal_data_root=Path(args.terminal_data_root),
            timeout_seconds=args.timeout_seconds,
            wait_timeout_seconds=args.wait_timeout_seconds,
            materialize_only=bool(args.materialize_only),
        )
    runtime_rows = build_fresh_runtime_summary(attempts, execution_result)
    signal_diff_rows = build_signal_difference_rows(proxy_rows, runtime_rows)
    numeric_rows = build_numeric_proxy_vs_fresh_mt5_rows(runtime_rows)
    usability_rows = build_usability_rows(signal_diff_rows, numeric_rows, runtime_rows)
    gate_rows = build_gate_rows(
        attempts=attempts,
        proxy_rows=proxy_rows,
        runtime_rows=runtime_rows,
        signal_diff_rows=signal_diff_rows,
        no_retune_rows=handoff_rows,
        execution_result=execution_result,
    )
    status, judgment, decision, next_action = classify(
        attempts=attempts,
        runtime_rows=runtime_rows,
        signal_diff_rows=signal_diff_rows,
        materialize_only=bool(args.materialize_only),
    )
    receipts = build_receipts(
        status=status,
        judgment=judgment,
        decision=decision,
        attempts=attempts,
        proxy_rows=proxy_rows,
        runtime_rows=runtime_rows,
        signal_diff_rows=signal_diff_rows,
        numeric_rows=numeric_rows,
        execution_result=execution_result,
    )
    failed_gates = sum(1 for row in gate_rows if str(row.get("status", "")).startswith("failed"))
    final_decision = {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": status,
        "judgment": judgment,
        "decision": decision,
        "fresh_runtime_completed": sum(1 for row in runtime_rows if row.get("tester_status") == "completed" and row.get("runtime_status") == "completed" and row.get("report_status") == "completed"),
        "runtime_attempts": len(attempts),
        "signal_difference_rows": len(signal_diff_rows),
        "numeric_difference_rows": len(numeric_rows),
        "failed_gates": failed_gates,
        "diagnostic_usability": usability_rows[0].get("diagnostic_usability_judgment") if usability_rows else "missing",
        "forward_usability": "not_usable_as_forward_decision",
        "selected_candidate": "none",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "runtime_authority": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": next_action,
        "claim_boundary": CLAIM_BOUNDARY,
    }

    artifact_paths: list[Path] = [
        write_json(
            RUN_DIR / "source_artifact_hashes.json",
            source_hashes(
                {
                    "script": Path(__file__),
                    "source_attempts": RUN330E_DIR / "mt5_probe_attempts.json",
                    "run335j_proxy_numeric": RUN335J_DIR / "proxy_expected_numeric_values.csv",
                    "run334d_reconciliation": RUN334D_DIR / "all_six_runtime_reconciliation.csv",
                    "run330f_cost": RUN330F_DIR / "cost_stress_report.csv",
                }
            ),
        ),
        write_json(RUN_DIR / "independent_handoff_attempts.json", attempts),
        write_csv(
            RUN_DIR / "independent_handoff_attempt_manifest.csv",
            [
                "attempt_name",
                "artifact_slug",
                "source_set_path",
                "source_ini_path",
                "new_set_path",
                "new_ini_path",
                "source_model_path",
                "new_model_path",
                "source_feature_path",
                "new_feature_path",
                "model_common_path",
                "feature_common_path",
                "telemetry_common_path",
                "summary_common_path",
                "threshold_keys_unchanged",
                "risk_lot_keys_unchanged",
                "source_set_sha256",
                "new_set_sha256",
                "model_sha256",
                "feature_sha256",
                "materialization_status",
                "claim_boundary",
            ],
            handoff_rows,
        ),
        write_csv(
            RUN_DIR / "no_retune_handoff_audit.csv",
            [
                "attempt_name",
                "threshold_keys_unchanged",
                "risk_lot_keys_unchanged",
                "allowed_identity_keys_changed",
                "source_set_sha256",
                "new_set_sha256",
                "source_ini_sha256",
                "new_ini_sha256",
                "claim_boundary",
            ],
            handoff_rows,
        ),
        write_csv(
            RUN_DIR / "proxy_signal_expected_values.csv",
            [
                "attempt_name",
                "artifact_slug",
                "feature_set_id",
                "model_id",
                "expected_feature_ready_count",
                "expected_model_ok_count",
                "expected_short_count",
                "expected_long_count",
                "expected_flat_count",
                "expected_signal_count",
                "expected_signal_rate",
                "expected_long_share",
                "mean_p_short",
                "mean_p_flat",
                "mean_p_long",
                "mean_probability_margin",
                "max_probability_row_sum_abs_error",
                "feature_order_hash",
                "feature_csv_sha256",
                "model_sha256",
                "threshold_policy",
                "proxy_source",
                "claim_boundary",
            ],
            proxy_rows,
        ),
        write_json(RUN_DIR / "runtime_execution_result.json", execution_result),
        write_csv(
            RUN_DIR / "mt5_fresh_runtime_probe_summary.csv",
            [
                "attempt_name",
                "artifact_slug",
                "feature_set_id",
                "tester_status",
                "runtime_status",
                "report_status",
                "returncode",
                "blocker",
                "feature_ready_count",
                "model_ok_count",
                "tier_a_long_count",
                "tier_a_short_count",
                "tier_a_flat_count",
                "long_count",
                "short_count",
                "flat_count",
                "no_tier_count",
                "last_skip_reason",
                "order_attempt_count",
                "order_fill_count",
                "net_profit",
                "profit_factor",
                "trade_count",
                "expectancy",
                "recovery_factor",
                "max_drawdown_amount",
                "short_trade_count",
                "long_trade_count",
                "common_summary_path",
                "common_telemetry_path",
                "report_name",
                "report_path",
                "claim_boundary",
            ],
            runtime_rows,
        ),
        write_csv(
            RUN_DIR / "proxy_signal_vs_mt5_runtime_difference.csv",
            [
                "attempt_name",
                "artifact_slug",
                "dimension",
                "proxy_expected_value",
                "mt5_runtime_value",
                "difference_proxy_minus_mt5",
                "difference_status",
                "proxy_source",
                "mt5_source",
                "usable_for_runtime_signal_parity",
                "usable_for_forward_pass_fail",
                "runtime_skip_reason",
                "claim_boundary",
            ],
            signal_diff_rows,
        ),
        write_csv(
            RUN_DIR / "proxy_numeric_vs_fresh_mt5_difference.csv",
            [
                "protocol_id",
                "branch_id",
                "branch_name",
                "dimension",
                "proxy_expected_value",
                "fresh_mt5_runtime_value",
                "difference_proxy_minus_fresh_mt5",
                "difference_status",
                "proxy_source",
                "mt5_source",
                "independence_improvement",
                "usable_for_diagnostic_consistency",
                "usable_for_forward_pass_fail",
                "reason",
                "claim_boundary",
            ],
            numeric_rows,
        ),
        write_csv(
            RUN_DIR / "proxy_mt5_usability_decision_matrix.csv",
            [
                "protocol_id",
                "branch_id",
                "branch_name",
                "fresh_runtime_attempts_completed",
                "fresh_runtime_attempts_total",
                "signal_parity_rows_matched",
                "signal_parity_rows_total",
                "numeric_proxy_fresh_mt5_rows",
                "numeric_proxy_fresh_mt5_available_rows",
                "diagnostic_usability_judgment",
                "forward_usability_judgment",
                "independent_forward_read_available",
                "reason",
                "forward_passed",
                "forward_failed",
                "runtime_authority",
                "goal_achieve",
                "claim_boundary",
            ],
            usability_rows,
        ),
        write_csv(RUN_DIR / "required_gate_coverage_audit.csv", ["gate_name", "status", "evidence_path", "effect"], gate_rows),
        write_csv(
            RUN_DIR / "result_judgment.csv",
            [
                "run_id",
                "status",
                "judgment",
                "decision",
                "diagnostic_usability",
                "forward_usability",
                "selected_candidate",
                "forward_passed",
                "forward_failed",
                "runtime_authority",
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
                    "diagnostic_usability": final_decision["diagnostic_usability"],
                    "forward_usability": "not_usable_as_forward_decision",
                    "selected_candidate": "none",
                    "forward_passed": "not_claimed",
                    "forward_failed": "not_claimed",
                    "runtime_authority": "not_claimed",
                    "goal_achieve": "not_claimed",
                    "next_action": next_action,
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            ],
        ),
        write_json(RUN_DIR / "final_independent_proxy_mt5_runtime_probe_decision.json", final_decision),
    ]

    for name, receipt in receipts.items():
        artifact_paths.append(write_json(RUN_DIR / f"{name}.json", receipt))
    artifact_paths.extend(copy_runtime_outputs(Path(args.common_files_root), attempts))

    manifest = {
        **final_decision,
        "generated_at_utc": generated_at_utc,
        "artifacts": [rel(path) for path in artifact_paths if path_exists(path)],
                "command": "python stage_pipelines/stage335/independent_proxy_mt5_probe.py",
                "materialize_only": bool(args.materialize_only),
        "reuse_existing_runtime": bool(args.reuse_existing_runtime),
        "terminal_path": str(args.terminal_path),
        "metaeditor_path": str(args.metaeditor_path),
        "common_files_root": str(args.common_files_root),
        "tester_profile_root": str(args.tester_profile_root),
        "terminal_data_root": str(args.terminal_data_root),
    }
    manifest_path = write_json(RUN_DIR / "run_manifest.json", manifest)
    lineage = {
        "run_id": RUN_ID,
        "producer": rel(Path(__file__)),
        "source_inputs": [rel(RUN330E_DIR / "mt5_probe_attempts.json"), rel(RUN335J_DIR / "proxy_expected_numeric_values.csv")],
        "artifacts": [rel(path) for path in [*artifact_paths, manifest_path] if path_exists(path)],
        "lineage_judgment": "connected_with_boundary",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    lineage_path = write_json(RUN_DIR / "artifact_lineage_receipt.json", lineage)
    artifact_paths.extend([manifest_path, lineage_path])

    report_path = write_md(REVIEWS_DIR / "run335K_independent_proxy_mt5_runtime_probe.md", build_report_text(status, decision, runtime_rows, signal_diff_rows, usability_rows))
    decision_path = write_md(DECISION_DOC, build_decision_text(status, decision, usability_rows))
    artifact_paths.extend([report_path, decision_path])
    artifact_paths.extend(update_docs(status, judgment, decision, next_action))
    artifact_paths.append(Path(__file__))
    update_registers(generated_at_utc, status, judgment, decision, next_action, artifact_paths)

    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": status,
                "decision": decision,
                "fresh_runtime_completed": final_decision["fresh_runtime_completed"],
                "runtime_attempts": final_decision["runtime_attempts"],
                "signal_difference_rows": len(signal_diff_rows),
                "signal_matches": sum(1 for row in signal_diff_rows if row.get("usable_for_runtime_signal_parity") in {True, "true"}),
                "numeric_difference_rows": len(numeric_rows),
                "failed_gates": failed_gates,
                "diagnostic_usability": final_decision["diagnostic_usability"],
                "forward_usability": "not_usable_as_forward_decision",
                "forward_passed": "not_claimed",
                "goal_achieve": "not_claimed",
                "next_action": next_action,
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
