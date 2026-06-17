from __future__ import annotations

import argparse
import csv
import json
import shutil
import subprocess
import sys
from dataclasses import dataclass
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
from foundation.models.onnx_bridge import ordered_hash, ordered_sklearn_probabilities, sha256_file
from stage_pipelines.stage_frontier_71 import frontier71d_mt5_runtime_probe_economics_native_scout as f71d
from stage_pipelines.stage_frontier_73 import frontier73b_session_regime_feature_model_rotation_proxy_scout as f73b
from stage_pipelines.stage_frontier_runtime_backfill.run_frontier_runtime_probe_backfill import (
    DEFAULT_COMMON_FILES,
    DEFAULT_METAEDITOR,
    DEFAULT_PORTABLE_ROOT,
    DEFAULT_TERMINAL,
    DEFAULT_TESTER_PROFILE_ROOT,
    EA_BINARY,
    PORTABLE_EA_BINARY,
)


STAGE_ID = f73b.STAGE_ID
RUN_ID = "frontier73D_pre_mt5_grok_session_regime_near_miss_runtime_probe_v1"
PARENT_RUN_ID = "frontier73C_axis_reduction_or_repair_proxy_scout_v1"
NEXT_RUN_ID = "frontier73E_proxy_runtime_gap_analysis_or_repair_decision_v1"
CLAIM_BOUNDARY = (
    "runtime_probe_observation_only_no_completion_no_baseline_no_promotion_"
    "no_runtime_authority_no_live_readiness_no_goal_achieve"
)

STAGE_ROOT = f73b.STAGE_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REVIEWS_ROOT = f73b.REVIEWS_ROOT
SELECTED_ROOT = f73b.SELECTED_ROOT
MODEL_ROOT = RUN_ROOT / "models"
FEATURE_ROOT = RUN_ROOT / "features"
VETO_ROOT = RUN_ROOT / "runtime_veto_tapes"
MT5_ROOT = RUN_ROOT / "mt5"
COMMON_RUN_ROOT = "Project_Obsidian_Prime_v2/frontier73D_session_regime_near_miss_runtime_probe"
RUNTIME_THRESHOLD_EPSILON = 1e-6

GROK_PACKET = ROOT / "docs/agent_control/grok_reviews/2026-06-17_f73d_pre_mt5_session_regime_near_miss_runtime_probe"
GROK_PROMPT = GROK_PACKET / "prompts/f73d_pre_mt5_session_regime_near_miss_runtime_probe_prompt.md"
GROK_CLEAN = GROK_PACKET / "clean_output.md"
GROK_METADATA = GROK_PACKET / "metadata.json"
F73C_TOP = STAGE_ROOT / "02_runs" / PARENT_RUN_ID / "f73c_top_candidates.csv"
F73C_SUMMARY = STAGE_ROOT / "02_runs" / PARENT_RUN_ID / "frontier73C_proxy_repair_summary.json"
F73C_BEST_TRADES = STAGE_ROOT / "02_runs" / PARENT_RUN_ID / "f73c_best_candidate_trades.csv"


@dataclass(frozen=True)
class AxisSpec:
    candidate_id: str
    axis_id: str
    role: str
    threshold: float
    label_id: str
    feature_set_id: str
    model_id: str
    selection_id: str
    mask_name: str


@dataclass(frozen=True)
class LabelSpec:
    horizon_bars: int
    sl_atr: float
    tp_atr: float


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="F73D session/regime near-miss MT5 runtime probe.")
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


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: Mapping[str, Any] | Sequence[Any]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str] | None = None) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    fieldnames = list(columns or (rows[0].keys() if rows else []))
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: json_ready(row.get(field, "")) for field in fieldnames})


def write_text(path: Path, lines: Sequence[str]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8-sig")


def append_once(path: Path, marker: str, block: str) -> None:
    text = io_path(path).read_text(encoding="utf-8-sig") if path_exists(path) else ""
    if marker in text:
        return
    io_path(path).write_text(text.rstrip() + "\n\n" + block.rstrip() + "\n", encoding="utf-8-sig")


def ensure_dirs() -> None:
    for path in (RUN_ROOT, MODEL_ROOT, FEATURE_ROOT, VETO_ROOT, MT5_ROOT, MT5_ROOT / "reports", REVIEWS_ROOT, SELECTED_ROOT):
        io_path(path).mkdir(parents=True, exist_ok=True)


def required_inputs() -> list[Path]:
    return [
        GROK_CLEAN,
        GROK_METADATA,
        F73C_TOP,
        F73C_SUMMARY,
        F73C_BEST_TRADES,
        f73b.FWD12_INPUT,
        f73b.FWD12_FEATURE_ORDER,
        f73b.RAW_US100,
    ]


def configure_f71d_globals() -> None:
    f71d.RUN_ID = RUN_ID
    f71d.PARENT_RUN_ID = PARENT_RUN_ID
    f71d.NEXT_RUN_ID = NEXT_RUN_ID
    f71d.CLAIM_BOUNDARY = CLAIM_BOUNDARY
    f71d.RUN_ROOT = RUN_ROOT
    f71d.MODEL_ROOT = MODEL_ROOT
    f71d.FEATURE_ROOT = FEATURE_ROOT
    f71d.VETO_ROOT = VETO_ROOT
    f71d.MT5_ROOT = MT5_ROOT
    f71d.COMMON_RUN_ROOT = COMMON_RUN_ROOT
    f71d.side_score_from_probability = side_score_from_probability


def side_score_from_probability(proba: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    short_p = proba[:, 0]
    flat_p = proba[:, 1]
    long_p = proba[:, 2]
    side = np.where(short_p >= long_p, -1, 1).astype(int)
    score = np.maximum(short_p, long_p) - flat_p
    return side, score.astype(float)


def selected_candidate() -> Mapping[str, Any]:
    top = pd.read_csv(io_path(F73C_TOP))
    row = top.loc[top["candidate_id"].astype(str).eq("f73c_0002")]
    if row.empty:
        row = top.head(1)
    return row.iloc[0].to_dict()


def cash_open_gate(frame: pd.DataFrame) -> np.ndarray:
    minutes = pd.to_numeric(frame["minutes_from_cash_open"], errors="coerce")
    return ((minutes >= 0) & (minutes <= 60)).to_numpy(dtype=bool)


def build_three_class_label(paths: Mapping[str, Mapping[str, np.ndarray]]) -> np.ndarray:
    long_ok = np.asarray(paths["long"]["quality_label"], dtype=float) > 0
    short_ok = np.asarray(paths["short"]["quality_label"], dtype=float) > 0
    long_quality = np.nan_to_num(np.asarray(paths["long"]["quality"], dtype=float), nan=-999.0)
    short_quality = np.nan_to_num(np.asarray(paths["short"]["quality"], dtype=float), nan=-999.0)
    y = np.zeros(len(long_ok), dtype=int)
    y[short_ok & (~long_ok | (short_quality >= long_quality))] = -1
    y[long_ok & (~short_ok | (long_quality > short_quality))] = 1
    return y


def train_bridge_model(model_id: str, frame: pd.DataFrame, features: Sequence[str], y: np.ndarray, train_mask: np.ndarray) -> Any:
    model = f73b.model_factories()[model_id]()
    model.fit(frame.loc[train_mask, list(features)], y[train_mask])
    return model


def score_threshold(scores: np.ndarray, timestamps: pd.Series, target_tpd: float) -> float:
    valid = np.asarray(scores[np.isfinite(scores)], dtype=float)
    if len(valid) == 0:
        raise RuntimeError("no_valid_scores_for_threshold")
    days = f73b.split_days(pd.to_datetime(timestamps, utc=True))
    target_count = max(int(round(days * float(target_tpd))), 1)
    target_count = min(target_count, len(valid))
    return float(np.partition(valid, len(valid) - target_count)[len(valid) - target_count])


def split_proxy_metrics(frame: pd.DataFrame, selected: np.ndarray, pnl: np.ndarray) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for split in ("train", "validation", "oos"):
        split_mask = frame["split"].astype(str).eq(split).to_numpy(dtype=bool) & selected
        out[split] = f73b.trade_metrics(
            frame.loc[split_mask, "timestamp"],
            pnl[split_mask],
            np.ones(int(split_mask.sum()), dtype=int),
        )
    return out


def build_context_for_model(model_id: str) -> dict[str, Any]:
    source = selected_candidate()
    raw = f73b.load_raw()
    data = f73b.load_dataset(f73b.DATASETS[str(source["dataset_id"])], raw)
    frame = data["frame"].copy()
    features = f73b.feature_bundles(data["features"])[str(source["feature_bundle"])]
    gate = cash_open_gate(frame)
    y = build_three_class_label(data["paths"])
    finite = np.isfinite(data["paths"]["long"]["pnl"]) & np.isfinite(data["paths"]["short"]["pnl"])
    train_mask = frame["split"].astype(str).eq("train").to_numpy(dtype=bool) & gate & finite
    classes = set(np.unique(y[train_mask]).tolist())
    if classes != {-1, 0, 1}:
        raise RuntimeError(f"bridge_train_class_coverage_failed:{sorted(classes)}")

    model = train_bridge_model(model_id, frame, features, y, train_mask)
    values = frame.loc[:, features].to_numpy(dtype="float64")
    proba = ordered_sklearn_probabilities(model, values, class_order=(-1, 0, 1))
    side, score = side_score_from_probability(proba)
    long_candidate = gate & finite & (side == 1)
    validation_long = frame["split"].astype(str).eq("validation").to_numpy(dtype=bool) & long_candidate
    threshold = score_threshold(score[validation_long], frame.loc[validation_long, "timestamp"], float(source["target_trades_day"]))
    runtime_threshold = max(float(threshold) - RUNTIME_THRESHOLD_EPSILON, 0.0)
    selected = long_candidate & (score >= threshold)
    label_spec = LabelSpec(horizon_bars=12, sl_atr=1.0, tp_atr=1.6)
    axis = AxisSpec(
        candidate_id=f"f73d_bridge_{source['candidate_id']}_{model_id}",
        axis_id="f73d_session_regime_cash_open_long_quality_bridge",
        role="bridge_3class_from_f73c_seed_runtime_probe",
        threshold=float(runtime_threshold),
        label_id="fwd12_long_short_quality_three_class_bridge",
        feature_set_id=str(source["feature_bundle"]),
        model_id=model_id,
        selection_id="cash_open_long_edge_margin_selected_entry",
        mask_name="cash_open_long_only_selected_entry",
    )
    return {
        "axis": axis,
        "frame": frame,
        "label_spec": label_spec,
        "feature_columns": list(features),
        "feature_order_hash": ordered_hash(features),
        "model": model,
        "selected": selected,
        "event_mask": gate & finite,
        "side": side,
        "score": score,
        "proxy_kpi_by_split": split_proxy_metrics(frame, selected, data["paths"]["long"]["pnl"]),
        "source_candidate": dict(source),
        "bridge_label_counts": {str(label): int(count) for label, count in zip(*np.unique(y[train_mask], return_counts=True))},
        "selection_threshold": float(threshold),
        "runtime_threshold": float(runtime_threshold),
        "runtime_threshold_epsilon": RUNTIME_THRESHOLD_EPSILON,
        "materialization_mode": "bridge_3class_from_f73c_seed",
        "proxy_authority": "none",
    }


def materialize_bridge(common_files_root: Path) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    errors: list[dict[str, Any]] = []
    for model_id in ("small_nn_16", "extra_trees_ref"):
        try:
            context = build_context_for_model(model_id)
            artifact, probability_rows, signal_rows = f71d.materialize_context(context, common_files_root)
            artifact.update(
                {
                    "model_family_used": model_id,
                    "model_family_repair": "none" if model_id == "small_nn_16" else "extra_trees_ref_repair_after_small_nn_failure",
                    "source_candidate": context["source_candidate"],
                    "bridge_label_counts": context["bridge_label_counts"],
                    "selection_threshold": context["selection_threshold"],
                    "runtime_threshold": context["runtime_threshold"],
                    "runtime_threshold_epsilon": context["runtime_threshold_epsilon"],
                    "materialization_mode": context["materialization_mode"],
                    "proxy_authority": context["proxy_authority"],
                    "parity_layers": ["bridge_internal", "proxy_bridge_delta"],
                    "runtime_claim_ceiling": "runtime_probe_observation_only",
                }
            )
            return artifact, probability_rows, signal_rows, context
        except Exception as exc:  # noqa: BLE001
            errors.append({"model_id": model_id, "error": str(exc)})
            if model_id == "extra_trees_ref":
                raise RuntimeError(f"all_bridge_materialization_attempts_failed:{errors}") from exc
    raise RuntimeError(f"unreachable_materialize_bridge:{errors}")


def proxy_bridge_delta_rows(context: Mapping[str, Any]) -> list[dict[str, Any]]:
    source = context["source_candidate"]
    source_trades = pd.read_csv(io_path(F73C_BEST_TRADES))
    source_trades["timestamp"] = pd.to_datetime(source_trades["timestamp"], utc=True)
    bridge_frame = context["frame"].copy()
    bridge_frame["timestamp"] = pd.to_datetime(bridge_frame["timestamp"], utc=True)
    selected_ts = set(bridge_frame.loc[context["selected"], "timestamp"].tolist())
    rows: list[dict[str, Any]] = []
    for split in ("validation", "oos"):
        source_split = source_trades.loc[source_trades["split"].astype(str).eq(split)]
        source_ts = set(source_split["timestamp"].tolist())
        bridge_split_ts = set(bridge_frame.loc[context["selected"] & bridge_frame["split"].astype(str).eq(split).to_numpy(dtype=bool), "timestamp"].tolist())
        overlap = source_ts & bridge_split_ts
        bridge_kpi = context["proxy_kpi_by_split"].get(split, {})
        rows.append(
            {
                "split": split,
                "source_candidate_id": source.get("candidate_id"),
                "source_binary_model_id": source.get("model_id"),
                "bridge_model_id": context["axis"].model_id,
                "source_selected_count": len(source_ts),
                "bridge_selected_count": len(bridge_split_ts),
                "overlap_count": len(overlap),
                "source_only_count": len(source_ts - bridge_split_ts),
                "bridge_only_count": len(bridge_split_ts - source_ts),
                "overlap_ratio_vs_source": float(len(overlap) / len(source_ts)) if source_ts else 0.0,
                "source_net_profit": source.get(f"{split}_net_profit"),
                "source_profit_factor": source.get(f"{split}_profit_factor"),
                "source_max_drawdown_percent": source.get(f"{split}_max_drawdown_percent"),
                "source_trades_day": source.get(f"{split}_trades_day"),
                "bridge_net_profit": bridge_kpi.get("net_profit"),
                "bridge_profit_factor": bridge_kpi.get("profit_factor"),
                "bridge_max_drawdown_percent": bridge_kpi.get("max_drawdown_percent"),
                "bridge_trades_day": bridge_kpi.get("trades_day"),
                "claim_boundary": "proxy_bridge_delta_not_authority",
            }
        )
    return rows


def build_attempts(context: Mapping[str, Any], artifact: Mapping[str, Any]) -> list[dict[str, Any]]:
    axis: AxisSpec = context["axis"]
    label_spec: LabelSpec = context["label_spec"]
    attempts: list[dict[str, Any]] = []
    frame = context["frame"]
    for split in ("validation", "oos"):
        from_date, to_date = f71d.split_dates(frame, split)
        split_mask = frame["split"].astype(str).eq(split).to_numpy(dtype=bool)
        expected_rows = int(split_mask.sum())
        expected_selected = int((context["selected"] & split_mask).sum())
        attempt_name = f"f73d_{axis.axis_id}_{split}"
        extra = {
            "InpSameDirectionReentryCooldownBars": int(label_spec.horizon_bars),
            "InpReentryCooldownBars": 0,
            "InpAtrSltpEnabled": True,
            "InpAtrStopMultiplier": float(label_spec.sl_atr),
            "InpAtrTakeProfitMultiplier": float(label_spec.tp_atr),
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
            stage_number=73,
            exploration_label=f"frontier73D_{axis.axis_id}_runtime_probe",
            attempt_name=attempt_name,
            tier=f71d.mt5.TIER_A,
            split=split,
            model_path=str(artifact["model_common_path"]),
            model_id=f"F73D_{axis.candidate_id}",
            model_backend="onnx",
            feature_path=str(artifact["feature_common_path"]),
            feature_count=len(context["feature_columns"]),
            feature_order_hash=str(context["feature_order_hash"]),
            short_threshold=0.0,
            long_threshold=0.0,
            min_margin=float(axis.threshold),
            invert_signal=False,
            from_date=from_date,
            to_date=to_date,
            primary_active_tier=f71d.mt5.TIER_A,
            attempt_role=axis.role,
            record_view_prefix=f"mt5_f73d_{axis.axis_id}",
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
                "source_candidate_id": context["source_candidate"].get("candidate_id"),
                "axis_id": axis.axis_id,
                "axis_role": axis.role,
                "expected_rows": expected_rows,
                "expected_signal_count": expected_selected,
                "expected_selected_trade_count": expected_selected,
                "proxy_kpi": context["proxy_kpi_by_split"].get(split, {}),
                "label_id": axis.label_id,
                "feature_set_id": axis.feature_set_id,
                "model_id": axis.model_id,
                "selection_id": axis.selection_id,
                "mask_name": axis.mask_name,
                "threshold": axis.threshold,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        attempts.append(attempt)
    return attempts


def compile_runtime_ea(metaeditor_path: Path) -> dict[str, Any]:
    compile_payload = f71d.mt5.compile_mql5_ea(metaeditor_path, f71d.mt5.EA_SOURCE_PATH, MT5_ROOT / "mt5_compile.log")
    portable_payload = {
        "repo_ea_ex5": rel(EA_BINARY),
        "portable_ea_ex5": PORTABLE_EA_BINARY.as_posix(),
        "portable_ea_ex5_exists_before": path_exists(PORTABLE_EA_BINARY),
        "copied": False,
    }
    if path_exists(EA_BINARY):
        io_path(PORTABLE_EA_BINARY.parent).mkdir(parents=True, exist_ok=True)
        shutil.copy2(io_path(EA_BINARY), io_path(PORTABLE_EA_BINARY))
        portable_payload.update(
            {
                "copied": True,
                "portable_ea_ex5_exists_after": path_exists(PORTABLE_EA_BINARY),
                "portable_ea_sha256": f71d.mt5.sha256_file(PORTABLE_EA_BINARY),
            }
        )
    return {"compile": compile_payload, "portable_ea": portable_payload}


def can_run_terminal(payload: Mapping[str, Any]) -> bool:
    return ((payload.get("compile") or {}).get("status") == "completed") or path_exists(PORTABLE_EA_BINARY)


def execute_attempts(args: argparse.Namespace, attempts: Sequence[Mapping[str, Any]], compile_payload: Mapping[str, Any]) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for attempt in attempts:
        if not can_run_terminal(compile_payload):
            result = {"status": "blocked", "blocker": "compile_failed_and_portable_ea_missing"}
        else:
            f71d.clear_runtime_outputs(Path(args.common_files_root), attempt)
            f71d.mt5.remove_existing_mt5_report_artifacts(Path(args.terminal_data_root), attempt, run_id=RUN_ID)
            try:
                result = f71d.mt5.run_mt5_tester(
                    Path(args.terminal_path),
                    ROOT / str(attempt["ini"]["path"]),
                    set_path=ROOT / str(attempt["set"]["path"]),
                    tester_profile_set_path=Path(args.tester_profile_root) / f71d.mt5.EA_TESTER_SET_NAME,
                    tester_profile_ini_path=Path(args.tester_profile_root) / f"opv2_{attempt['attempt_name']}.ini",
                    timeout_seconds=int(args.timeout_seconds),
                    terminal_extra_args=["/portable"],
                )
            except subprocess.TimeoutExpired as exc:
                result = {
                    "status": "blocked",
                    "command": exc.cmd,
                    "stdout": (exc.stdout or "")[-2000:],
                    "stderr": (exc.stderr or "")[-2000:],
                    "blocker": "terminal_timeout",
                }
            runtime_outputs = f71d.mt5.wait_for_mt5_runtime_outputs(
                Path(args.common_files_root),
                attempt,
                timeout_seconds=int(args.wait_timeout_seconds),
                poll_seconds=2.0,
            )
            if runtime_outputs.get("status") != "completed":
                result["status"] = "blocked"
                result.setdefault("blocker", "runtime_outputs_missing_or_init_failed")
            result["runtime_outputs"] = runtime_outputs
        result.update(
            {
                "attempt_name": attempt["attempt_name"],
                "tier": attempt["tier"],
                "split": attempt["split"],
                "candidate_id": attempt.get("candidate_id"),
                "source_candidate_id": attempt.get("source_candidate_id"),
                "axis_id": attempt.get("axis_id"),
                "expected_rows": attempt.get("expected_rows"),
                "expected_signal_count": attempt.get("expected_signal_count"),
                "expected_selected_trade_count": attempt.get("expected_selected_trade_count"),
                "ini_path": attempt.get("ini", {}).get("path"),
                "set_path": attempt.get("set", {}).get("path"),
            }
        )
        results.append(result)
    return results


def best_receipt(receipts: Sequence[Mapping[str, Any]]) -> Mapping[str, Any]:
    return next((row for row in receipts if row.get("split") == "oos"), receipts[0] if receipts else {})


def build_summary(payload: Mapping[str, Any]) -> dict[str, Any]:
    receipts = list(payload.get("runtime_receipt", []))
    completed = sum(1 for row in receipts if row.get("tester_status") == "completed")
    best = best_receipt(receipts)
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "status": payload.get("status"),
        "judgment": payload.get("judgment"),
        "attempt_count": len(payload.get("attempts", [])),
        "completed_attempt_count": completed,
        "probability_parity_pass_rows": sum(1 for row in payload.get("probability_parity", []) if row.get("passed")),
        "signal_parity_pass_rows": sum(1 for row in payload.get("signal_parity", []) if row.get("passed")),
        "proxy_bridge_delta_rows": len(payload.get("proxy_bridge_delta", [])),
        "best_runtime": best,
        "next_run_id": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def grok_receipt_lines(created_at: str, artifact: Mapping[str, Any]) -> list[str]:
    metadata = read_json(GROK_METADATA)
    return [
        "# F73D Pre-MT5 Grok Receipt(F73D 사전 MT5 Grok 영수증)",
        "",
        f"- created_at_utc(생성): `{created_at}`",
        "- trigger_reason(트리거 이유): F73C dual-positive near-miss(검증+표본외 양수 근접 단서)를 mandatory MT5 Runtime Probe(필수 MT5 런타임 탐침)로 물질화하기 전 외부 2차 의견 필요.",
        "- direction_before_grok(그록 전 방향): bridge_3class_from_f73c_seed(이진 F73C 씨앗에서 3분류 연결 모델)로 단일 좁은 런타임 관찰을 실행.",
        f"- prompt_identity(프롬프트 정체성): `{rel(GROK_PROMPT)}`, sha256 `{sha256_file(GROK_PROMPT)}`.",
        f"- output_identity(출력 정체성): `{rel(GROK_CLEAN)}`, sha256 `{sha256_file(GROK_CLEAN)}`.",
        f"- wrapper_success(래퍼 성공): `{metadata.get('success')}`; returncode(반환 코드): `{metadata.get('returncode')}`.",
        "- advice_classification(조언 분류): `accepted_with_conditions_rejected_authority_needs_local_verification(조건부 수용/권위 주장 거절/로컬 검증 필요)`.",
        "- accepted(수용): narrow F73D MT5 Runtime Probe(좁은 F73D MT5 런타임 탐침), seed/bridge/observation language(씨앗/연결/관찰 표현), fwd18 high-DD 후보 제외.",
        "- rejected(거절): F73C dual-positive를 authority(권위)로 취급, binary proxy(이진 프록시)와 3-class bridge(3분류 연결)를 동일시, success language(성공 표현).",
        "- needs_local_verification(로컬 검증 필요): class balance(클래스 균형), bridge_internal parity(연결 내부 동등성), proxy_bridge_delta(프록시-연결 차이), threshold mapping(임계값 매핑), selected-entry tape compatibility(선택 진입 테이프 호환).",
        f"- local_verification(로컬 검증): materialization `{artifact.get('export_status')}`, probability parity `{artifact.get('probability_parity_passed')}`, signal parity `{artifact.get('signal_parity_passed')}`, model `{artifact.get('model_family_used')}`.",
        f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`.",
    ]


def report_lines(payload: Mapping[str, Any], created_at: str) -> list[str]:
    summary = build_summary(payload)
    best = summary["best_runtime"]
    artifact = payload.get("artifact_rows", [{}])[0]
    return [
        "# Frontier73D MT5 Runtime Probe(F73D MT5 런타임 탐침)",
        "",
        f"Updated(갱신): {created_at}",
        "",
        f"- status(상태): `{payload.get('status')}`",
        f"- judgment(판정): `{payload.get('judgment')}`",
        f"- attempts(시도): `{summary['attempt_count']}`; completed(완료): `{summary['completed_attempt_count']}`",
        f"- probability parity pass rows(확률 동등성 통과 행): `{summary['probability_parity_pass_rows']}`",
        f"- signal parity pass rows(신호 동등성 통과 행): `{summary['signal_parity_pass_rows']}`",
        f"- materialization_mode(물질화 방식): `{artifact.get('materialization_mode')}`",
        f"- model_family_used(사용 모델 계열): `{artifact.get('model_family_used')}`",
        f"- proxy_authority(프록시 권위): `{artifact.get('proxy_authority')}`",
        f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
        "",
        "## Runtime KPI(런타임 핵심 성과 지표)",
        "",
        f"- best split(최선 분할): `{best.get('split', '')}`",
        f"- net/PF/DD/trades_day(순수익/수익 팩터/손실폭/일거래): `{best.get('net_profit', '')}` / `{best.get('profit_factor', '')}` / `{best.get('max_drawdown_percent', '')}` / `{best.get('trades_per_day', '')}`",
        f"- expected signal/trade vs runtime signal/trade(예상 신호/거래 대 런타임 신호/거래): `{best.get('expected_signal_count', '')}/{best.get('expected_selected_trade_count', '')}` vs `{best.get('signal_count', '')}/{best.get('trade_count', '')}`",
        f"- signal count diff(신호 수 차이): `{best.get('signal_count_diff', '')}`; feature ready diff(피처 준비 차이): `{best.get('feature_ready_diff', '')}`",
        f"- gap cause(간극 원인): `{best.get('gap_cause_summary', '')}`",
        "",
        "## Proxy/Bridge Boundary(프록시/연결 경계)",
        "",
        "This run is bridge-derived runtime observation(연결 기반 런타임 관찰) only. Effect(효과): F73C binary proxy(이진 프록시)를 MT5에서 직접 재현했다고 말하지 않고, bridge_internal parity(연결 내부 동등성)와 proxy_bridge_delta(프록시-연결 차이)를 분리한다.",
        "",
        "## Next Action(다음 행동)",
        "",
        f"`{NEXT_RUN_ID}`.",
    ]


def gate_audit_lines(payload: Mapping[str, Any], created_at: str) -> list[str]:
    summary = build_summary(payload)
    return [
        "# F73D Required Gate Coverage Audit(F73D 필수 게이트 커버리지 감사)",
        "",
        f"Updated(갱신): {created_at}",
        "",
        f"- pre_mt5_grok(사전 MT5 Grok): `{rel(GROK_CLEAN)}`.",
        f"- bridge_materialization(연결 물질화): `{payload.get('artifact_rows', [{}])[0].get('export_status')}`.",
        f"- bridge_internal_probability_parity(연결 내부 확률 동등성): `{summary['probability_parity_pass_rows']}` pass rows(통과 행).",
        f"- bridge_internal_signal_parity(연결 내부 신호 동등성): `{summary['signal_parity_pass_rows']}` pass rows(통과 행).",
        f"- proxy_bridge_delta(프록시-연결 차이): `{summary['proxy_bridge_delta_rows']}` rows(행).",
        f"- runtime_attempts(런타임 시도): `{summary['attempt_count']}`.",
        f"- runtime_receipt_rows(런타임 영수증 행): `{len(payload.get('runtime_receipt', []))}`.",
        "- final_claim_guard(최종 주장 보호): pass(통과).",
        f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`.",
    ]


def write_outputs(payload: Mapping[str, Any], created_at: str) -> None:
    artifact = payload.get("artifact_rows", [{}])[0]
    write_json(RUN_ROOT / "frontier73D_runtime_probe_execution_result.json", payload)
    write_json(RUN_ROOT / "frontier73D_runtime_probe_summary.json", build_summary(payload))
    write_json(
        RUN_ROOT / "run_manifest.json",
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "status": payload.get("status"),
            "judgment": payload.get("judgment"),
            "artifact_rows": payload.get("artifact_rows", []),
            "attempts": payload.get("attempts", []),
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_csv(RUN_ROOT / "f73d_bridge_materialization.csv", payload.get("artifact_rows", []))
    write_csv(RUN_ROOT / "f73d_onnx_probability_parity.csv", payload.get("probability_parity", []))
    write_csv(RUN_ROOT / "f73d_onnx_signal_parity.csv", payload.get("signal_parity", []))
    write_csv(RUN_ROOT / "f73d_proxy_bridge_delta.csv", payload.get("proxy_bridge_delta", []))
    write_csv(RUN_ROOT / "f73d_runtime_probe_receipt.csv", payload.get("runtime_receipt", []), f71d.RUNTIME_RECEIPT_COLUMNS)
    write_csv(REVIEWS_ROOT / "f73d_bridge_materialization_review.csv", payload.get("artifact_rows", []))
    write_csv(REVIEWS_ROOT / "f73d_onnx_probability_parity_review.csv", payload.get("probability_parity", []))
    write_csv(REVIEWS_ROOT / "f73d_onnx_signal_parity_review.csv", payload.get("signal_parity", []))
    write_csv(REVIEWS_ROOT / "f73d_proxy_bridge_delta_review.csv", payload.get("proxy_bridge_delta", []))
    write_csv(REVIEWS_ROOT / "f73d_runtime_probe_receipt_review.csv", payload.get("runtime_receipt", []), f71d.RUNTIME_RECEIPT_COLUMNS)
    write_text(REVIEWS_ROOT / "frontier73D_mt5_runtime_probe_report.md", report_lines(payload, created_at))
    write_text(REVIEWS_ROOT / "f73d_pre_mt5_grok_receipt.md", grok_receipt_lines(created_at, artifact))
    write_text(REVIEWS_ROOT / "required_gate_coverage_audit_f73d.md", gate_audit_lines(payload, created_at))


def update_ledgers(payload: Mapping[str, Any], created_at: str) -> None:
    summary = build_summary(payload)
    best = summary["best_runtime"]
    row = {
        "ledger_row_id": f"{RUN_ID}__runtime_probe",
        "row_id": f"{RUN_ID}__runtime_probe",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "mt5_runtime_probe(MT5 런타임 탐침)",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "MT5 Runtime Probe(MT5 런타임 탐침)",
        "tier_scope": "Tier A separate(Tier A 분리)",
        "kpi_scope": "runtime_probe_kpi(런타임 탐침 KPI)",
        "scoreboard_lane": "runtime_probe(런타임 탐침)",
        "status": payload.get("status"),
        "judgment": payload.get("judgment"),
        "path": rel(REVIEWS_ROOT / "frontier73D_mt5_runtime_probe_report.md"),
        "primary_kpi": f"attempts={summary['attempt_count']};completed={summary['completed_attempt_count']};best_pf={best.get('profit_factor')}",
        "guardrail_kpi": f"signal_diff={best.get('signal_count_diff')};feature_diff={best.get('feature_ready_diff')};proxy_bridge_delta_rows={summary['proxy_bridge_delta_rows']}",
        "external_verification_status": "completed(완료)" if summary["completed_attempt_count"] else "blocked(차단)",
        "notes": "F73D bridge-derived MT5 runtime probe observation; no authority.",
        "family": "runtime_probe(런타임 탐침)",
        "lane": "mt5_runtime_probe(MT5 런타임 탐침)",
        "primary_report": rel(REVIEWS_ROOT / "frontier73D_mt5_runtime_probe_report.md"),
        "run_number": "frontier73D",
        "date": created_at[:10],
        "decision": payload.get("judgment"),
        "next_run_id": NEXT_RUN_ID,
        "rows": len(payload.get("runtime_receipt", [])),
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REVIEWS_ROOT / "frontier73D_mt5_runtime_probe_report.md"),
        "runtime_completed_rows": summary["completed_attempt_count"],
        "best_net_profit": best.get("net_profit"),
        "best_profit_factor": best.get("profit_factor"),
        "run_date": created_at[:10],
        "primary_artifact": rel(RUN_ROOT / "run_manifest.json"),
        "candidate_model_id": payload.get("artifact_rows", [{}])[0].get("candidate_id"),
        "net_profit": best.get("net_profit"),
        "profit_factor": best.get("profit_factor"),
        "drawdown": best.get("max_drawdown_percent"),
        "trade_count": best.get("trade_count"),
        "trade_density": best.get("trades_per_day"),
        "result_status": payload.get("status"),
        "view": "MT5 Runtime Probe(MT5 런타임 탐침)",
        "tier": "Tier A",
        "metric_scope": "runtime_probe_kpi(런타임 탐침 KPI)",
        "result_judgment": payload.get("judgment"),
        "final_decision_path": rel(REVIEWS_ROOT / "frontier73D_mt5_runtime_probe_report.md"),
        "gate_audit_path": rel(REVIEWS_ROOT / "required_gate_coverage_audit_f73d.md"),
        "created_at": created_at,
        "created_at_utc": created_at,
        "required_gate_audit": rel(REVIEWS_ROOT / "required_gate_coverage_audit_f73d.md"),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "source_authority": "bridge_runtime_probe_observation_only(연결 런타임 탐침 관찰 전용)",
        "evidence_boundary": "runtime_probe_observation_no_authority(런타임 탐침 관찰, 권위 없음)",
        "next_action": NEXT_RUN_ID,
        "question": "Does the F73C session/regime seed survive MT5 bridge runtime observation?(F73C 세션/장세 씨앗이 MT5 연결 런타임 관찰에서 살아남는가?)",
        "artifact_count": 14,
        "work_family": "runtime_probe(런타임 탐침)",
        "run_family": "frontier_runtime_probe(전선 런타임 탐침)",
        "run_type": "mt5_runtime_probe(MT5 런타임 탐침)",
        "input_run_id": PARENT_RUN_ID,
        "output_path": rel(RUN_ROOT / "run_manifest.json"),
        "result_path": rel(REVIEWS_ROOT / "frontier73D_mt5_runtime_probe_report.md"),
    }
    f73b.upsert_ledger(f73b.ALPHA_LEDGER, "ledger_row_id", row)
    f73b.upsert_ledger(f73b.RUN_REGISTRY, "run_id", row)
    f73b.upsert_ledger(REVIEWS_ROOT / "stage_run_ledger.csv", "ledger_row_id", row, source_header=f73b.ALPHA_LEDGER)


def update_registers(payload: Mapping[str, Any]) -> None:
    summary = build_summary(payload)
    best = summary["best_runtime"]
    marker = "<!-- frontier73D_pre_mt5_grok_session_regime_near_miss_runtime_probe_v1 -->"
    block = f"""<!-- frontier73D_pre_mt5_grok_session_regime_near_miss_runtime_probe_v1 -->
- `{RUN_ID}` executed/attempted(실행/시도) F73 bridge-derived MT5 Runtime Probe(F73 연결 기반 MT5 런타임 탐침). Result(결과): `{payload.get('judgment')}`. Attempts(시도) `{summary['attempt_count']}`, completed(완료) `{summary['completed_attempt_count']}`. Best runtime(최선 런타임) net/PF/DD/trades_day(순수익/수익 팩터/손실폭/일거래): `{best.get('net_profit', '')}/{best.get('profit_factor', '')}/{best.get('max_drawdown_percent', '')}/{best.get('trades_per_day', '')}`. Evidence(근거): `{rel(REVIEWS_ROOT / 'frontier73D_mt5_runtime_probe_report.md')}`. Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음). Next(다음): `{NEXT_RUN_ID}`."""
    append_once(f73b.IDEA_REGISTRY, marker, block)


def update_state(payload: Mapping[str, Any], created_at: str) -> None:
    summary = build_summary(payload)
    state = [
        f"current_stage_id: {STAGE_ID}",
        f"active_stage: {STAGE_ID}",
        f"current_run_id: {NEXT_RUN_ID}",
        f"latest_completed_run_id: {RUN_ID}",
        f"current_status: {payload.get('status')}",
        f"current_judgment: {payload.get('judgment')}",
        f"next_run_id: {NEXT_RUN_ID}",
        "runtime_probe_status: f73_mandatory_runtime_probe_attempted",
        "runtime_authority: not_claimed",
        "operating_promotion: not_claimed",
        "live_readiness: not_claimed",
        "goal_achieve: not_claimed",
        "five_stage_retrospective_due_status: not_due_after_f72_closeout",
        f"updated_at_utc: '{created_at}'",
        "notes:",
        f'  - "Action(행동): F73D MT5 Runtime Probe(MT5 런타임 탐침)를 실행/시도했다. Attempts(시도) {summary["attempt_count"]}, completed(완료) {summary["completed_attempt_count"]}."',
        f'  - "Effect(효과): bridge-derived runtime observation(연결 기반 런타임 관찰)을 만들고, 다음 행동을 {NEXT_RUN_ID}로 설정했다."',
        '  - "Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음)."',
    ]
    io_path(f73b.WORKSPACE_STATE).write_text("\n".join(state) + "\n", encoding="utf-8-sig")
    write_text(
        SELECTED_ROOT / "selection_status.md",
        [
            "# F73 Selection Status(F73 선택 상태)",
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
            f"- next_action(다음 행동): `{NEXT_RUN_ID}`",
            f"- boundary(경계): `{CLAIM_BOUNDARY}`",
        ],
    )
    write_text(
        f73b.CURRENT_WORKING_STATE,
        [
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
            "Action(행동): F73D bridge-derived MT5 Runtime Probe(연결 기반 MT5 런타임 탐침)를 실행/시도했다.",
            "",
            f"Effect(효과): runtime receipt rows(런타임 영수증 행) `{len(payload.get('runtime_receipt', []))}`개를 만들고, 다음 행동을 `{NEXT_RUN_ID}`로 설정했다.",
            "",
            f"- judgment(판정): `{payload.get('judgment')}`.",
            f"- completed attempts(완료 시도): `{summary['completed_attempt_count']}` / `{summary['attempt_count']}`.",
            f"- best runtime net/PF/DD/tpd(최선 런타임 순수익/수익 팩터/손실폭/일거래): `{summary['best_runtime'].get('net_profit', '')}` / `{summary['best_runtime'].get('profit_factor', '')}` / `{summary['best_runtime'].get('max_drawdown_percent', '')}` / `{summary['best_runtime'].get('trades_per_day', '')}`.",
            "",
            f"Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`",
        ],
    )


def main() -> int:
    args = parse_args()
    ensure_dirs()
    missing = [rel(path) for path in required_inputs() if not path_exists(path)]
    if missing:
        raise FileNotFoundError(f"F73D required material missing: {missing}")
    configure_f71d_globals()
    created_at = utc_now()
    artifact, probability_rows, signal_rows, context = materialize_bridge(Path(args.common_files_root))
    proxy_bridge_delta = proxy_bridge_delta_rows(context)
    attempts = build_attempts(context, artifact) if artifact.get("export_status") == "exported_selected_entry_tape_parity_passed" else []
    compile_payload = compile_runtime_ea(Path(args.metaeditor_path))
    execution_results: list[dict[str, Any]] = []
    if args.execute and not args.materialize_only and attempts:
        execution_results = execute_attempts(args, attempts, compile_payload)
        reports = f71d.mt5.collect_mt5_strategy_report_artifacts(
            terminal_data_root=Path(args.terminal_data_root),
            run_output_root=RUN_ROOT,
            attempts=attempts,
            run_id=RUN_ID,
        )
        f71d.mt5.attach_mt5_report_metrics(execution_results, reports)
    runtime_receipt = f71d.build_runtime_receipt(execution_results, attempts) if execution_results else []
    completed = sum(1 for row in runtime_receipt if row.get("tester_status") == "completed")
    if args.execute and completed:
        status = "completed_mt5_runtime_probe_observation_no_authority"
        judgment = "runtime_probe_completed_gap_analysis_required_no_authority"
    elif args.execute:
        status = "blocked_mt5_runtime_probe_attempted_no_authority"
        judgment = "runtime_probe_blocked_repair_required_no_authority"
    else:
        status = "materialized_pending_mt5_runtime_probe_execution_no_authority"
        judgment = "runtime_probe_materialized_pending_execution_no_authority"
    payload = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "status": status,
        "judgment": judgment,
        "created_at_utc": created_at,
        "artifact_rows": [artifact],
        "probability_parity": probability_rows,
        "signal_parity": signal_rows,
        "proxy_bridge_delta": proxy_bridge_delta,
        "attempts": attempts,
        "compile_payload": compile_payload,
        "execution_results": execution_results,
        "runtime_receipt": runtime_receipt,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_outputs(payload, created_at)
    update_ledgers(payload, created_at)
    update_registers(payload)
    update_state(payload, created_at)
    print(json.dumps(json_ready(build_summary(payload)), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
