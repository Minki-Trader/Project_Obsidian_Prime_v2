from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists
from stage_pipelines.stage_frontier_71 import frontier71d_mt5_runtime_probe_economics_native_scout as f71d
from stage_pipelines.stage_frontier_77 import frontier77d_mt5_lifecycle_negative_control_runtime_probe as runtime_base
from stage_pipelines.stage_frontier_78 import frontier78b_execution_calibrated_density_contract_pnl_proxy_scout as f78b
from stage_pipelines.stage_frontier_runtime_backfill.run_frontier_runtime_probe_backfill import (
    DEFAULT_COMMON_FILES,
    DEFAULT_METAEDITOR,
    DEFAULT_PORTABLE_ROOT,
    DEFAULT_TERMINAL,
    DEFAULT_TESTER_PROFILE_ROOT,
)


STAGE_ID = f78b.STAGE_ID
RUN_ID = "frontier78D_mt5_execution_calibrated_negative_control_runtime_probe_v1"
PARENT_RUN_ID = "frontier78C_pre_mt5_grok_execution_calibrated_negative_control_runtime_probe_v1"
NEXT_RUN_ID = "frontier78E_proxy_runtime_gap_analysis_and_repair_decision_v1"
COMMON_RUN_ROOT = "Project_Obsidian_Prime_v2/frontier78D_mt5_execution_calibrated_negative_control_runtime_probe"
THRESHOLD_EPSILON = 1e-7
RUNTIME_CANDIDATE_PREFIX = "f78d_runtime"
SLTP_POINT_SCALE = 100.0
TRADE_SHAPE_LABEL = "short_only_max_hold_18_cd6_fixed_tp26_sl16_price_units_2600_1600_points"
RUN_SHORT_LABEL = "F78D"
ATTEMPT_PREFIX = "f78d_execution_calibrated_negative_control"
EXPLORATION_LABEL = "frontier78D_execution_calibrated_negative_control_runtime_probe"
ATTEMPT_ROLE = "execution_calibrated_negative_control_runtime_probe"
RECORD_VIEW_PREFIX = "mt5_f78d_execution_calibrated_negative_control"
CLAIM_BOUNDARY = (
    "negative_control_runtime_probe_observation_only_no_completion_no_baseline_"
    "no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_ID
MODEL_DIR = RUN_DIR / "models"
FEATURE_DIR = RUN_DIR / "features"
VETO_DIR = RUN_DIR / "runtime_veto_tapes"
MT5_DIR = RUN_DIR / "mt5"
REVIEW_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"

TARGET_SELECTION_PATH = REVIEW_DIR / "f78c_runtime_materialization_target_selection.json"
REPORT_PATH = REVIEW_DIR / "frontier78D_mt5_execution_calibrated_negative_control_runtime_probe_report.md"
GATE_AUDIT_PATH = REVIEW_DIR / "required_gate_coverage_audit_f78d.md"
SUMMARY_PATH = REVIEW_DIR / "f78d_mt5_execution_calibrated_runtime_probe_summary.json"
RUNTIME_PARITY_PATH = REVIEW_DIR / "f78d_runtime_parity_receipt.json"
BACKTEST_FORENSICS_PATH = REVIEW_DIR / "f78d_backtest_forensics_receipt.json"
RUN_MANIFEST_PATH = RUN_DIR / "run_manifest.json"
CONTEXT_ANCHOR_PATH = f"stages/{STAGE_ID}/03_reviews/context_anchor.md"

WORKSPACE_STATE = ROOT / "docs/workspace/workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs/context/current_working_state.md"
RUN_REGISTRY = ROOT / "docs/registers/run_registry.csv"
ALPHA_LEDGER = ROOT / "docs/registers/alpha_run_ledger.csv"
IDEA_REGISTRY = ROOT / "docs/registers/idea_registry.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"

SCRIPT_REL = "stage_pipelines/stage_frontier_78/frontier78d_mt5_execution_calibrated_negative_control_runtime_probe.py"


def configure_runtime_base() -> None:
    runtime_base.STAGE_ID = STAGE_ID
    runtime_base.RUN_ID = RUN_ID
    runtime_base.PARENT_RUN_ID = PARENT_RUN_ID
    runtime_base.NEXT_RUN_ID = NEXT_RUN_ID
    runtime_base.COMMON_RUN_ROOT = COMMON_RUN_ROOT
    runtime_base.THRESHOLD_EPSILON = THRESHOLD_EPSILON
    runtime_base.RUNTIME_CANDIDATE_PREFIX = RUNTIME_CANDIDATE_PREFIX
    runtime_base.SLTP_POINT_SCALE = SLTP_POINT_SCALE
    runtime_base.TRADE_SHAPE_LABEL = TRADE_SHAPE_LABEL
    runtime_base.RUN_SHORT_LABEL = RUN_SHORT_LABEL
    runtime_base.ATTEMPT_PREFIX = ATTEMPT_PREFIX
    runtime_base.EXPLORATION_LABEL = EXPLORATION_LABEL
    runtime_base.ATTEMPT_ROLE = ATTEMPT_ROLE
    runtime_base.RECORD_VIEW_PREFIX = RECORD_VIEW_PREFIX
    runtime_base.CLAIM_BOUNDARY = CLAIM_BOUNDARY
    runtime_base.STAGE_DIR = STAGE_DIR
    runtime_base.RUN_DIR = RUN_DIR
    runtime_base.MODEL_DIR = MODEL_DIR
    runtime_base.FEATURE_DIR = FEATURE_DIR
    runtime_base.VETO_DIR = VETO_DIR
    runtime_base.MT5_DIR = MT5_DIR
    runtime_base.REVIEW_DIR = REVIEW_DIR
    runtime_base.SELECTED_DIR = SELECTED_DIR
    runtime_base.TARGET_SELECTION_PATH = TARGET_SELECTION_PATH
    runtime_base.REPORT_PATH = REPORT_PATH
    runtime_base.GATE_AUDIT_PATH = GATE_AUDIT_PATH
    runtime_base.SUMMARY_PATH = SUMMARY_PATH
    runtime_base.RUN_MANIFEST_PATH = RUN_MANIFEST_PATH
    runtime_base.CONTEXT_ANCHOR_PATH = CONTEXT_ANCHOR_PATH


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="F78D MT5 execution-calibrated negative-control runtime probe.")
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--materialize-only", action="store_true")
    parser.add_argument("--include-oos", action="store_true")
    parser.add_argument("--timeout-seconds", type=int, default=600)
    parser.add_argument("--wait-timeout-seconds", type=int, default=300)
    parser.add_argument("--terminal-path", default=str(DEFAULT_TERMINAL))
    parser.add_argument("--metaeditor-path", default=str(DEFAULT_METAEDITOR))
    parser.add_argument("--common-files-root", default=str(DEFAULT_COMMON_FILES))
    parser.add_argument("--tester-profile-root", default=str(DEFAULT_TESTER_PROFILE_ROOT))
    parser.add_argument("--terminal-data-root", default=str(DEFAULT_PORTABLE_ROOT))
    return parser.parse_args()


def now_utc() -> str:
    return f78b.utc_now()


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def write_text(path: Path, text: str, *, encoding: str = "utf-8-sig") -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding=encoding)


def write_json(path: Path, payload: Mapping[str, Any] | Sequence[Any]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8-sig")


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str] | None = None) -> None:
    rows = list(rows)
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    fieldnames = list(columns or (rows[0].keys() if rows else ["empty"]))
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({name: json_ready(row.get(name, "")) for name in fieldnames})


def upsert_csv(path: Path, key: str, row: Mapping[str, Any], source_header: Path | None = None) -> None:
    if path_exists(path):
        with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = list(reader.fieldnames or [])
            rows = list(reader)
    elif source_header is not None and path_exists(source_header):
        with io_path(source_header).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = list(reader.fieldnames or [])
        rows = []
    else:
        fieldnames = list(row.keys())
        rows = []
    for field in row:
        if field not in fieldnames:
            fieldnames.append(field)
    rows = [existing for existing in rows if existing.get(key) != row.get(key)]
    rows.append({field: json_ready(row.get(field, "")) for field in fieldnames})
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def ensure_dirs() -> None:
    configure_runtime_base()
    runtime_base.ensure_dirs()
    for path in (REVIEW_DIR, SELECTED_DIR):
        io_path(path).mkdir(parents=True, exist_ok=True)


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def as_int(value: Any, default: int = 0) -> int:
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return default


def target_row() -> dict[str, Any]:
    payload = read_json(TARGET_SELECTION_PATH)
    target = dict(payload.get("runtime_materialization_target") or {})
    if target.get("candidate_id") != "f78b_02234":
        raise RuntimeError(f"target_lock_failed:{target.get('candidate_id')}")
    if target.get("model") != "logistic_l2_balanced":
        raise RuntimeError(f"target_model_lock_failed:{target.get('model')}")
    if str(target.get("side")) != "short":
        raise RuntimeError(f"target_side_lock_failed:{target.get('side')}")
    return target


def normalized_proxy_kpi(metrics: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "net_profit": metrics.get("net"),
        "gross_profit": metrics.get("gross_profit"),
        "gross_loss": metrics.get("gross_loss"),
        "profit_factor": metrics.get("pf"),
        "max_drawdown_percent": metrics.get("dd_pct"),
        "trade_count": metrics.get("trade_count"),
        "trades_day": metrics.get("calendar_trades_day"),
        "calendar_trades_day": metrics.get("calendar_trades_day"),
        "active_trades_day": metrics.get("active_trades_day"),
        "calendar_days": metrics.get("calendar_days"),
        "active_days": metrics.get("active_days"),
        "win_rate": metrics.get("win_rate"),
        "average_win": metrics.get("avg_win"),
        "average_loss": metrics.get("avg_loss"),
        "payoff_ratio": metrics.get("payoff"),
        "expectancy": metrics.get("expectancy"),
        "recovery_factor": metrics.get("recovery"),
        "avg_hold_bars": metrics.get("avg_hold_bars"),
        "avg_mae_contract": metrics.get("avg_mae_contract"),
        "avg_spread_cost_contract": metrics.get("avg_spread_cost_contract"),
        "max_consecutive_loss": metrics.get("max_consecutive_loss"),
        "time_under_water_trades": metrics.get("time_under_water_trades"),
    }


def build_context(target: Mapping[str, Any]) -> dict[str, Any]:
    frame, raw, features = f78b.load_inputs()
    indices = f78b.entry_indices_next_bar(frame, raw)
    spec = next(item for item in f78b.contract_specs() if item.name == str(target["label_name"]))
    outcome = f78b.compute_contract_outcome(raw, indices, spec)
    label = f78b.make_label(frame, outcome, spec)
    train_valid = (frame["split"] == "train").to_numpy() & np.asarray(outcome["valid"], dtype=bool)
    feature_columns = f78b.feature_sets(features)[str(target["feature_set"])]
    if len(feature_columns) != as_int(target.get("feature_count")):
        raise RuntimeError(f"feature_count_lock_failed:{len(feature_columns)}:{target.get('feature_count')}")
    train_matrix_raw = frame.loc[train_valid, feature_columns].replace([np.inf, -np.inf], np.nan)
    med = train_matrix_raw.median(numeric_only=True).fillna(0.0)
    train_matrix = train_matrix_raw.fillna(med).astype(float)
    y_train = label[train_valid]
    model = f78b.model_builders()[str(target["model"])]()
    model.fit(train_matrix, y_train)
    train_probs = f78b.probability(model, train_matrix)
    threshold = float(np.quantile(train_probs, as_float(target.get("prob_quantile"))))
    if abs(threshold - as_float(target.get("prob_threshold"))) > 1e-10:
        raise RuntimeError(f"prob_threshold_drift:{threshold}:{target.get('prob_threshold')}")
    clean_frame = runtime_base.cleaned_full_frame(frame, train_valid, feature_columns)
    binary_proba = runtime_base.f74e.binary_probabilities(model, clean_frame.loc[:, feature_columns])
    score = binary_proba[:, 1]
    thresholds = f78b.risk_thresholds(frame)
    selected_global = np.zeros(len(clean_frame), dtype=bool)
    raw_signal_global = np.zeros(len(clean_frame), dtype=bool)
    event_filter_global = np.zeros(len(clean_frame), dtype=bool)
    proxy_kpi_by_split: dict[str, dict[str, Any]] = {}
    reproduction_rows: list[dict[str, Any]] = []
    cooldown_bars = as_int(target.get("cooldown_bars"))
    for split, prefix in (("validation", "val"), ("oos", "oos")):
        split_mask = clean_frame["split"].astype(str).eq(split).to_numpy(dtype=bool)
        split_df = clean_frame.loc[split_mask].reset_index(drop=True)
        split_outcome = {key: np.asarray(value)[split_mask] for key, value in outcome.items()}
        valid = np.asarray(split_outcome["valid"], dtype=bool)
        event_filter = valid & f78b.session_mask(split_df, str(target["session"])) & f78b.risk_mask(split_df, str(target["risk_filter"]), spec.side, thresholds)
        raw_signal = (score[split_mask] >= threshold) & event_filter
        selected = f78b.lifecycle_select(raw_signal, np.asarray(split_outcome["exit_offset"], dtype=int), cooldown_bars)
        metrics = f78b.contract_kpi(split_df, selected, split_outcome)
        proxy_kpi_by_split[split] = normalized_proxy_kpi(metrics)
        selected_global[split_mask] = selected
        raw_signal_global[split_mask] = raw_signal
        event_filter_global[split_mask] = event_filter
        raw_key = f"{split}_raw_signal_count"
        lifecycle_key = f"{split}_lifecycle_trade_count"
        if split == "validation":
            raw_key = "validation_raw_signal_count"
            lifecycle_key = "validation_lifecycle_trade_count"
        reproduction_rows.append(
            {
                "split": split,
                "source_candidate_id": target.get("candidate_id"),
                "source_net_profit": target.get(f"{prefix}_net"),
                "source_profit_factor": target.get(f"{prefix}_pf"),
                "source_max_drawdown_percent": target.get(f"{prefix}_dd_pct"),
                "source_trades_day": target.get(f"{prefix}_calendar_trades_day"),
                "source_trade_count": target.get(f"{prefix}_trade_count"),
                "source_raw_signal_count": target.get(raw_key),
                "source_lifecycle_trade_count": target.get(lifecycle_key),
                "reproduced_net_profit": metrics["net"],
                "reproduced_profit_factor": metrics["pf"],
                "reproduced_max_drawdown_percent": metrics["dd_pct"],
                "reproduced_trades_day": metrics["calendar_trades_day"],
                "reproduced_active_trades_day": metrics["active_trades_day"],
                "reproduced_trade_count": metrics["trade_count"],
                "reproduced_raw_signal_count": int(raw_signal.sum()),
                "reproduced_lifecycle_trade_count": int(selected.sum()),
                "count_diff": int(metrics["trade_count"]) - as_int(target.get(f"{prefix}_trade_count")),
                "raw_signal_count_diff": int(raw_signal.sum()) - as_int(target.get(raw_key)),
                "lifecycle_trade_count_diff": int(selected.sum()) - as_int(target.get(lifecycle_key)),
                "net_diff": float(metrics["net"]) - as_float(target.get(f"{prefix}_net")),
                "pf_diff": float(metrics["pf"]) - as_float(target.get(f"{prefix}_pf")),
                "dd_diff": float(metrics["dd_pct"]) - as_float(target.get(f"{prefix}_dd_pct")),
                "passed": bool(
                    int(metrics["trade_count"]) == as_int(target.get(f"{prefix}_trade_count"))
                    and int(raw_signal.sum()) == as_int(target.get(raw_key))
                    and int(selected.sum()) == as_int(target.get(lifecycle_key))
                    and abs(float(metrics["net"]) - as_float(target.get(f"{prefix}_net"))) <= 1e-6
                    and abs(float(metrics["pf"]) - as_float(target.get(f"{prefix}_pf"))) <= 1e-9
                ),
            }
        )
    return {
        "target": dict(target),
        "frame": clean_frame,
        "spec": spec,
        "features": list(feature_columns),
        "feature_order_hash": runtime_base.ordered_hash(feature_columns),
        "model": model,
        "binary_proba": binary_proba,
        "score": score,
        "threshold": threshold,
        "runtime_threshold": threshold - THRESHOLD_EPSILON,
        "selected": selected_global,
        "raw_signal": raw_signal_global,
        "event_filter": event_filter_global,
        "proxy_kpi_by_split": proxy_kpi_by_split,
        "reproduction_rows": reproduction_rows,
        "known_differences": [
            "Python proxy(파이썬 프록시) uses next-bar open path simulation(다음 봉 시가 경로 시뮬레이션).",
            "MT5 runtime(MT5 런타임) uses EA feature timestamp matching(EA 피처 시각 매칭) and broker tester fills(브로커 테스터 체결).",
            "Fixed TP/SL(고정 익절/손절)은 price units(가격 단위) 26/16을 broker points(브로커 포인트) 2600/1600으로 변환한다.",
        ],
    }


def materialize(context: Mapping[str, Any], common_files_root: Path) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    artifact, probability, signal, feature_parity = runtime_base.materialize(context, common_files_root)
    artifact.update(
        {
            "blocked_best_candidate_id": "",
            "materialization_mode": "short_binary_onnx_three_column_execution_calibrated_negative_control",
            "surrogate_boundary": "best_proxy_candidate_exportable_no_surrogate_substitution",
            "source_proxy_run_id": f78b.RUN_ID,
            "pre_mt5_grok_run_id": PARENT_RUN_ID,
            "trade_shape": TRADE_SHAPE_LABEL,
            "tp_price_units": context["target"].get("tp_price_units"),
            "sl_price_units": context["target"].get("sl_price_units"),
            "tp_broker_points": context["target"].get("tp_broker_points"),
            "sl_broker_points": context["target"].get("sl_broker_points"),
            "cooldown_bars_proxy": context["target"].get("cooldown_bars"),
            "runtime_cooldown_bars": 0,
            "runtime_cooldown_reason": "selected-entry veto tape(선택 진입 거부 테이프)가 proxy cooldown(프록시 쿨다운)을 이미 반영한다.",
        }
    )
    return artifact, probability, signal, feature_parity


def build_attempts(context: Mapping[str, Any], artifact: Mapping[str, Any], *, include_oos: bool) -> list[dict[str, Any]]:
    attempts: list[dict[str, Any]] = []
    spec = context["spec"]
    target = context["target"]
    splits = ("validation", "oos") if include_oos else ("validation",)
    for split in splits:
        from_date, to_date = f71d.split_dates(context["frame"], split)
        split_mask = context["frame"]["split"].astype(str).eq(split).to_numpy(dtype=bool)
        expected_selected = int((context["selected"] & split_mask).sum())
        attempt_name = f"{ATTEMPT_PREFIX}_{split}"
        extra = {
            "InpSameDirectionReentryCooldownBars": 0,
            "InpReentryCooldownBars": 0,
            "InpAtrSltpEnabled": True,
            "InpAtrStopMultiplier": 1.0,
            "InpAtrTakeProfitMultiplier": 1.0,
            "InpAtrMinStopPoints": float(target.get("sl_broker_points", spec.sl_price_units * SLTP_POINT_SCALE)),
            "InpAtrMaxStopPoints": float(target.get("sl_broker_points", spec.sl_price_units * SLTP_POINT_SCALE)),
            "InpAtrMinTakeProfitPoints": float(target.get("tp_broker_points", spec.tp_price_units * SLTP_POINT_SCALE)),
            "InpAtrMaxTakeProfitPoints": float(target.get("tp_broker_points", spec.tp_price_units * SLTP_POINT_SCALE)),
            "InpDecisionMode": "threshold_margin",
            "InpFallbackDecisionMode": "threshold_margin",
            "InpRuntimeVetoTapeEnabled": True,
            "InpRuntimeVetoTapePath": str(artifact["runtime_veto_tape_common_path"]),
            "InpRuntimeVetoTapeUseCommonFiles": True,
            "InpRuntimeVetoTapeDelimiter": ",",
        }
        attempt = runtime_base.attempt_payload(
            run_root=RUN_DIR,
            run_id=RUN_ID,
            stage_number=78,
            exploration_label=EXPLORATION_LABEL,
            attempt_name=attempt_name,
            tier=f71d.mt5.TIER_A,
            split=split,
            model_path=str(artifact["model_common_path"]),
            model_id=f"{RUN_SHORT_LABEL}_{artifact['candidate_id']}",
            model_backend="onnx",
            feature_path=str(artifact["feature_common_path"]),
            feature_count=len(context["features"]),
            feature_order_hash=str(context["feature_order_hash"]),
            short_threshold=float(context["runtime_threshold"]),
            long_threshold=1.1,
            min_margin=-1.0,
            invert_signal=False,
            from_date=from_date,
            to_date=to_date,
            primary_active_tier=f71d.mt5.TIER_A,
            attempt_role=ATTEMPT_ROLE,
            record_view_prefix=RECORD_VIEW_PREFIX,
            max_hold_bars=int(spec.hold_bars),
            common_root=COMMON_RUN_ROOT,
            close_on_flat_signal=False,
            reverse_on_opposite_signal=True,
            close_only_on_opposite_signal=False,
            extra_set_values=extra,
        )
        attempt.update(
            {
                "candidate_id": artifact["candidate_id"],
                "source_candidate_id": artifact["source_candidate_id"],
                "axis_id": "short_h18_tp26_sl16_contract_core_logistic_all_none_cd6_q72",
                "expected_rows": int(split_mask.sum()),
                "expected_signal_count": expected_selected,
                "expected_selected_trade_count": expected_selected,
                "proxy_kpi": context["proxy_kpi_by_split"].get(split, {}),
                "runtime_threshold": float(context["runtime_threshold"]),
                "threshold_epsilon": THRESHOLD_EPSILON,
                "claim_boundary": CLAIM_BOUNDARY,
                "trade_shape": artifact["trade_shape"],
                "source_label_name": target.get("label_name"),
                "feature_set": target.get("feature_set"),
                "model_family": target.get("model"),
                "session": target.get("session"),
                "risk_filter": target.get("risk_filter"),
                "proxy_cooldown_bars": target.get("cooldown_bars"),
                "runtime_cooldown_bars": 0,
                "runtime_probe_scope": "validation_first" if not include_oos else "validation_and_oos",
            }
        )
        attempts.append(attempt)
    return attempts


def best_receipt(receipts: Sequence[Mapping[str, Any]]) -> Mapping[str, Any]:
    completed = [row for row in receipts if row.get("tester_status") == "completed"]
    rows = completed or list(receipts)
    return next((row for row in rows if row.get("split") == "validation"), rows[0] if rows else {})


def build_summary(payload: Mapping[str, Any]) -> dict[str, Any]:
    receipts = list(payload.get("runtime_receipt", []))
    probability = list(payload.get("probability_parity", []))
    signal = list(payload.get("signal_parity", []))
    feature = list(payload.get("feature_readiness_parity", []))
    reproduction = list(payload.get("source_reproduction", []))
    completed = sum(1 for row in receipts if row.get("tester_status") == "completed")
    best = best_receipt(receipts)
    artifact = (payload.get("artifact_rows") or [{}])[0]
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "status": payload.get("status"),
        "judgment": payload.get("judgment"),
        "candidate_id": artifact.get("candidate_id", f"{RUNTIME_CANDIDATE_PREFIX}_f78b_02234"),
        "source_candidate_id": artifact.get("source_candidate_id", "f78b_02234"),
        "attempt_count": len(payload.get("attempts", [])),
        "completed_attempt_count": completed,
        "probability_parity_pass_rows": sum(1 for row in probability if row.get("passed")),
        "signal_parity_pass_rows": sum(1 for row in signal if row.get("passed")),
        "feature_readiness_pass_rows": sum(1 for row in feature if row.get("feature_readiness_parity")),
        "source_reproduction_pass_rows": sum(1 for row in reproduction if row.get("passed")),
        "best_runtime": best,
        "claim_boundary": CLAIM_BOUNDARY,
        "next_run_id": NEXT_RUN_ID,
    }


def runtime_parity_receipt(payload: Mapping[str, Any]) -> dict[str, Any]:
    artifact = (payload.get("artifact_rows") or [{}])[0]
    attempts = list(payload.get("attempts", []))
    return {
        "research_path": SCRIPT_REL,
        "runtime_path": {
            "ea": f71d.mt5.EA_SOURCE_PATH.as_posix(),
            "model_common_path": artifact.get("model_common_path", ""),
            "feature_common_path": artifact.get("feature_common_path", ""),
            "runtime_veto_tape_common_path": artifact.get("runtime_veto_tape_common_path", ""),
            "attempt_set_paths": [attempt.get("set", {}).get("path", "") for attempt in attempts],
            "attempt_ini_paths": [attempt.get("ini", {}).get("path", "") for attempt in attempts],
        },
        "shared_contract": {
            "symbol": "US100",
            "timeframe": "M5",
            "candidate_id": artifact.get("source_candidate_id", ""),
            "feature_count": artifact.get("feature_csv", {}).get("feature_count", ""),
            "feature_order_hash": artifact.get("feature_csv", {}).get("feature_order_hash", ""),
            "short_threshold": artifact.get("short_threshold", ""),
            "long_threshold": artifact.get("long_threshold", ""),
            "trade_shape": artifact.get("trade_shape", TRADE_SHAPE_LABEL),
            "tp_broker_points": artifact.get("tp_broker_points", ""),
            "sl_broker_points": artifact.get("sl_broker_points", ""),
        },
        "known_differences": [
            "Proxy P/L(프록시 손익)는 F77 runtime-observed scale(F77 런타임 관찰 배율)을 쓴다.",
            "MT5 tester(MT5 테스터)는 broker execution semantics(브로커 체결 의미)를 쓴다.",
            "F78D default scope(F78D 기본 범위)는 validation split first(검증 분할 우선)다.",
        ],
        "parity_check": {
            "probability_parity": payload.get("probability_parity", []),
            "signal_count_parity": payload.get("signal_parity", []),
            "feature_readiness_parity": payload.get("feature_readiness_parity", []),
            "source_reproduction": payload.get("source_reproduction", []),
        },
        "parity_identity": {
            "model_sha256": artifact.get("patched_onnx_sha256", ""),
            "feature_csv_sha256": artifact.get("feature_csv_sha256", ""),
            "veto_tape_sha256": artifact.get("runtime_veto_tape_sha256", ""),
            "compile_payload": payload.get("compile_payload", {}),
        },
        "runtime_claim_boundary": "runtime_probe",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def backtest_forensics_receipt(payload: Mapping[str, Any]) -> dict[str, Any]:
    artifact = (payload.get("artifact_rows") or [{}])[0]
    attempts = list(payload.get("attempts", []))
    receipt = list(payload.get("runtime_receipt", []))
    return {
        "tester_identity": {
            "terminal": str(DEFAULT_TERMINAL),
            "broker_symbol": "US100",
            "timeframe": "M5",
            "deposit": 500,
            "leverage": "1:100",
            "modeling_mode": "Every tick based on real ticks setting value 4 from tester ini(테스터 ini 값 4)",
            "spread": "tester/broker default captured in report if available(보고서 가능 시 캡처)",
            "date_ranges": [{"split": attempt.get("split"), "from": attempt.get("ini", {}).get("tester", {}).get("FromDate"), "to": attempt.get("ini", {}).get("tester", {}).get("ToDate")} for attempt in attempts],
        },
        "ea_identity": {
            "ea_source": f71d.mt5.EA_SOURCE_PATH.as_posix(),
            "compile_payload": payload.get("compile_payload", {}),
            "set_paths": [attempt.get("set", {}).get("path", "") for attempt in attempts],
            "model_path": artifact.get("patched_onnx_path", ""),
            "model_sha256": artifact.get("patched_onnx_sha256", ""),
            "feature_order_hash": artifact.get("feature_order_hash", ""),
        },
        "report_identity": {
            "runtime_receipt_path": rel(RUN_DIR / "f78d_runtime_receipt.csv"),
            "execution_results_path": rel(RUN_DIR / "f78d_execution_results.json"),
            "summary_path": rel(SUMMARY_PATH),
        },
        "trade_evidence": receipt,
        "cost_assumptions": {
            "spread": "raw proxy includes spread_cost_contract(원시 프록시 스프레드 비용 포함); tester uses broker/tester execution(테스터는 브로커/테스터 체결 사용)",
            "commission": "report parser value if present(보고서 파서 값이 있으면 사용)",
            "slippage": "not explicitly controlled in this probe(이번 탐침에서 명시 제어 없음)",
            "swap": "report parser value if present(보고서 파서 값이 있으면 사용)",
        },
        "forensic_checks": {
            "output_path_recorded": bool(receipt),
            "settings_paths_recorded": bool(attempts),
            "runtime_outputs_recorded": bool(payload.get("execution_results", [])),
        },
        "backtest_judgment": "usable_with_boundary" if any(row.get("tester_status") == "completed" for row in receipt) else "inconclusive",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def report_text(payload: Mapping[str, Any], created_at: str) -> str:
    summary = build_summary(payload)
    best = summary["best_runtime"]
    target = (payload.get("target") or {})
    lines = [
        "# Frontier78D MT5 Execution-Calibrated Negative-Control Runtime Probe Report(F78D MT5 실행 보정 부정 대조 런타임 탐침 보고서)",
        "",
        f"Updated(갱신): {created_at}",
        "",
        f"- status(상태): `{payload.get('status')}`",
        f"- judgment(판정): `{payload.get('judgment')}`",
        "- source candidate(원천 후보): `f78b_02234`",
        f"- target axes(대상 축): `{target.get('label_name')}/{target.get('feature_set')}/{target.get('model')}/{target.get('session')}/{target.get('risk_filter')}/cd{target.get('cooldown_bars')}`",
        f"- attempts/completed(시도/완료): `{summary['attempt_count']}/{summary['completed_attempt_count']}`",
        f"- probability/signal/feature/reproduction parity pass(확률/신호/피처/재현 동등성 통과): `{summary['probability_parity_pass_rows']}/{summary['signal_parity_pass_rows']}/{summary['feature_readiness_pass_rows']}/{summary['source_reproduction_pass_rows']}`",
        f"- best runtime net/PF/DD/tpd(최선 런타임 순수익/수익 팩터/손실폭/일 거래): `{best.get('net_profit', '')}/{best.get('profit_factor', '')}/{best.get('max_drawdown_percent', '')}/{best.get('trades_per_day', '')}`",
        f"- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`",
        "",
        "## Proxy Expectation(프록시 예상)",
        "",
        f"- validation proxy(검증 프록시): net/PF/DD/calendar_tpd/trades(순수익/수익 팩터/손실폭/달력일 거래/거래) `{target.get('val_net')}/{target.get('val_pf')}/{target.get('val_dd_pct')}/{target.get('val_calendar_trades_day')}/{target.get('val_trade_count')}`",
        f"- OOS proxy(표본외 프록시): net/PF/DD/calendar_tpd/trades(순수익/수익 팩터/손실폭/달력일 거래/거래) `{target.get('oos_net')}/{target.get('oos_pf')}/{target.get('oos_dd_pct')}/{target.get('oos_calendar_trades_day')}/{target.get('oos_trade_count')}`",
        f"- signal count proxy(신호 수 프록시): validation raw/selected(검증 원시/선택) `{target.get('validation_raw_signal_count')}/{target.get('validation_lifecycle_trade_count')}`, OOS raw/selected(표본외 원시/선택) `{target.get('oos_raw_signal_count')}/{target.get('oos_lifecycle_trade_count')}`",
        "",
        "## Runtime KPI(런타임 핵심 성과 지표)",
        "",
        "| split/view(분할/보기) | period(기간) | net(순수익) | gross profit(총이익) | gross loss(총손실) | PF(수익 팩터) | DD%(손실폭) | trades(거래) | trades/day(일 거래) | win%(승률) | avg win(평균 이익) | avg loss(평균 손실) | payoff(손익비) | expectancy(기대값) | recovery(회복) | signal diff(신호 차이) | feature diff(피처 차이) | gap cause(간극 원인) |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in payload.get("runtime_receipt", []):
        period = f"{row.get('test_period_start', '')}..{row.get('test_period_end', '')}"
        lines.append(
            "| `{split}` | `{period}` | `{net}` | `{gp}` | `{gl}` | `{pf}` | `{dd}` | `{trades}` | `{tpd}` | `{win}` | `{avgw}` | `{avgl}` | `{payoff}` | `{exp}` | `{rec}` | `{sig}` | `{feat}` | `{gap}` |".format(
                split=row.get("split"),
                period=period,
                net=row.get("net_profit", ""),
                gp=row.get("gross_profit", ""),
                gl=row.get("gross_loss", ""),
                pf=row.get("profit_factor", ""),
                dd=row.get("max_drawdown_percent", ""),
                trades=row.get("trade_count", ""),
                tpd=row.get("trades_per_day", ""),
                win=row.get("win_rate_percent", ""),
                avgw=row.get("average_win", ""),
                avgl=row.get("average_loss", ""),
                payoff=row.get("payoff_ratio", ""),
                exp=row.get("expectancy", ""),
                rec=row.get("recovery_factor", ""),
                sig=row.get("signal_count_diff", ""),
                feat=row.get("feature_ready_diff", ""),
                gap=row.get("gap_cause_summary", ""),
            )
        )
    if not payload.get("runtime_receipt"):
        lines.append("| `missing(누락)` | `n/a` |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | `runtime output not completed(런타임 출력 미완료)` |")
    lines.extend(
        [
            "",
            "## Probe Boundary(탐침 경계)",
            "",
            "Action(행동): F78C에서 조건부 수용된 `f78b_02234`를 MT5 Strategy Tester(MT5 전략 테스터)로 물질화했다.",
            "",
            "Effect(효과): proxy/runtime gap analysis(프록시/런타임 간극 분석)와 repair decision(수리 결정)에 쓸 실제 런타임 관찰값을 만든다.",
            "",
            "## Next Action(다음 행동)",
            "",
            f"`{NEXT_RUN_ID}`.",
        ]
    )
    return "\n".join(lines)


def gate_audit_text(payload: Mapping[str, Any], created_at: str) -> str:
    summary = build_summary(payload)
    return f"""# Required Gate Coverage Audit F78D(F78D 필수 게이트 커버리지 감사)

Updated(갱신): {created_at}

| gate(게이트) | status(상태) | evidence/effect(근거/효과) |
|---|---|---|
| F78C Grok accepted with conditions(F78C Grok 조건부 수용) | `passed(통과)` | `stages/{STAGE_ID}/03_reviews/grok_pre_mt5_execution_calibrated_negative_control_runtime_probe_receipt.md` |
| target lock(대상 고정) | `passed(통과)` | `f78b_02234`, `logistic_l2_balanced` |
| source reproduction(원천 재현) | `{summary['source_reproduction_pass_rows']}/2` | validation/OOS proxy KPI reproduction(검증/표본외 프록시 KPI 재현) |
| probability parity(확률 동등성) | `{summary['probability_parity_pass_rows']}/3` | ONNX short schema(ONNX 숏 스키마) |
| signal count parity(신호 수 동등성) | `{summary['signal_parity_pass_rows']}/3` | selected-entry veto tape(선택 진입 거부 테이프) |
| feature readiness parity(피처 준비 동등성) | `{summary['feature_readiness_pass_rows']}/1` | 33 feature CSV(33개 피처 CSV) |
| MT5 runtime probe(MT5 런타임 탐침) | `{summary['completed_attempt_count']}/{summary['attempt_count']}` | Strategy Tester attempts(전략 테스터 시도) |
| runtime parity receipt(런타임 동등성 영수증) | `recorded(기록됨)` | `{rel(RUNTIME_PARITY_PATH)}` |
| backtest forensics receipt(백테스트 포렌식 영수증) | `recorded(기록됨)` | `{rel(BACKTEST_FORENSICS_PATH)}` |
| final claim guard(최종 주장 보호) | `passed(통과)` | `{CLAIM_BOUNDARY}` |
"""


def ledger_row(payload: Mapping[str, Any], created_at: str) -> dict[str, Any]:
    summary = build_summary(payload)
    best = summary["best_runtime"]
    row_id = f"{RUN_ID}__runtime_probe"
    return {
        "ledger_row_id": row_id,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "runtime_probe(런타임 탐침)",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "Tier A MT5 Runtime Probe(Tier A MT5 런타임 탐침)",
        "tier_scope": "Tier A separate; Tier B missing_required; combined out_of_scope",
        "kpi_scope": "runtime_probe_kpi(런타임 탐침 KPI)",
        "scoreboard_lane": "runtime_probe(런타임 탐침)",
        "status": payload.get("status"),
        "judgment": payload.get("judgment"),
        "path": rel(REPORT_PATH),
        "primary_kpi": f"net={best.get('net_profit', '')};pf={best.get('profit_factor', '')};dd={best.get('max_drawdown_percent', '')};tpd={best.get('trades_per_day', '')}",
        "guardrail_kpi": f"signal_diff={best.get('signal_count_diff', '')};feature_diff={best.get('feature_ready_diff', '')};candidate=f78b_02234",
        "external_verification_status": "completed(완료)" if summary["completed_attempt_count"] else "blocked_or_materialized_pending(차단 또는 물질화 대기)",
        "notes": f"attempts={summary['attempt_count']};completed={summary['completed_attempt_count']};candidate=f78d_runtime_f78b_02234",
        "lane": "mt5_runtime_probe(MT5 런타임 탐침)",
        "family": "runtime_backtest(런타임 백테스트)",
        "primary_report": rel(REPORT_PATH),
        "run_number": "frontier78D",
        "date": created_at[:10],
        "decision": payload.get("judgment"),
        "next_run_id": NEXT_RUN_ID,
        "rows": str(summary["attempt_count"]),
        "gate_passes": str(summary["probability_parity_pass_rows"] + summary["signal_parity_pass_rows"] + summary["feature_readiness_pass_rows"] + summary["source_reproduction_pass_rows"] + summary["completed_attempt_count"]),
        "gate_total": "11",
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "run_date": created_at[:10],
        "primary_artifact": rel(RUN_MANIFEST_PATH),
        "result_status": payload.get("status"),
        "view": "MT5 Runtime Probe(MT5 런타임 탐침)",
        "tier": "Tier A separate; Tier B missing_required; combined out_of_scope",
        "metric_scope": "runtime_probe_kpi(런타임 탐침 KPI)",
        "result_judgment": payload.get("judgment"),
        "final_decision_path": rel(SELECTED_DIR / "selection_status.md"),
        "gate_audit_path": rel(GATE_AUDIT_PATH),
        "created_at": created_at,
        "work_family": "runtime_backtest(런타임 백테스트)",
        "row_id": row_id,
        "evidence_boundary": "runtime_probe_observation_no_authority(런타임 탐침 관찰, 권위 없음)",
        "next_action": NEXT_RUN_ID,
        "question": "Does execution-calibrated contract P/L proxy survive MT5 runtime?(실행 보정 계약 손익 프록시가 MT5 런타임에서 유지되는가?)",
        "artifact_count": "14",
        "created_at_utc": created_at,
        "required_gate_audit": rel(GATE_AUDIT_PATH),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "run_family": "runtime_backtest(런타임 백테스트)",
        "run_type": "mt5_execution_calibrated_negative_control_runtime_probe",
        "input_run_id": PARENT_RUN_ID,
        "output_path": rel(RUN_MANIFEST_PATH),
        "result_path": rel(REPORT_PATH),
        "goal_achieve": "not_claimed",
        "source_authority": "runtime_probe_observation_only(런타임 탐침 관찰 전용)",
        "net_profit": best.get("net_profit", ""),
        "profit_factor": best.get("profit_factor", ""),
        "drawdown": best.get("max_drawdown_percent", ""),
        "trade_count": best.get("trade_count", ""),
        "trade_density": best.get("trades_per_day", ""),
        "expectancy": best.get("expectancy", ""),
        "recovery_factor": best.get("recovery_factor", ""),
        "runtime_completed_rows": summary["completed_attempt_count"],
        "probability_parity_pass_rows": summary["probability_parity_pass_rows"],
    }


def update_ledgers(payload: Mapping[str, Any], created_at: str) -> None:
    row = ledger_row(payload, created_at)
    upsert_csv(RUN_REGISTRY, "run_id", row)
    upsert_csv(ALPHA_LEDGER, "ledger_row_id", row)
    upsert_csv(STAGE_LEDGER, "ledger_row_id", row, source_header=ALPHA_LEDGER)


def update_registers_and_state(payload: Mapping[str, Any], created_at: str) -> None:
    summary = build_summary(payload)
    best = summary["best_runtime"]
    marker = "<!-- frontier78D_mt5_execution_calibrated_negative_control_runtime_probe_v1 -->"
    text = io_path(IDEA_REGISTRY).read_text(encoding="utf-8-sig")
    if marker not in text:
        addition = f"""

{marker}
- `{RUN_ID}` executed/attempted(실행/시도) F78 MT5 execution-calibrated negative-control runtime probe(F78 MT5 실행 보정 부정 대조 런타임 탐침). Source candidate(원천 후보): `f78b_02234`. Attempts/completed(시도/완료): `{summary['attempt_count']}/{summary['completed_attempt_count']}`. Best runtime net/PF/DD/tpd(최선 런타임 순수익/수익 팩터/손실폭/일 거래): `{best.get('net_profit', '')}/{best.get('profit_factor', '')}/{best.get('max_drawdown_percent', '')}/{best.get('trades_per_day', '')}`. Evidence(근거): `{rel(REPORT_PATH)}`. Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음). Next(다음): `{NEXT_RUN_ID}`.
"""
        write_text(IDEA_REGISTRY, text.rstrip() + addition)
    state = f"""current_stage_id: {STAGE_ID}
active_stage: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {payload.get('status')}
current_judgment: {payload.get('judgment')}
next_run_id: {NEXT_RUN_ID}
runtime_probe_status: f78_mandatory_runtime_probe_attempted
runtime_authority: not_claimed
operating_promotion: not_claimed
live_readiness: not_claimed
goal_achieve: not_claimed
five_stage_retrospective_due_status: not_due_after_f77_closeout_2_of_5
updated_at_utc: '{created_at}'
context_anchor: {CONTEXT_ANCHOR_PATH}
notes:
  - "Action(행동): F78D MT5 Runtime Probe(MT5 런타임 탐침)를 실행/시도했다."
  - "Effect(효과): F78E proxy/runtime gap analysis(프록시/런타임 간극 분석)와 repair decision(수리 결정)에 필요한 근거를 만들었다."
  - "Best runtime(최선 런타임): net/PF/DD/tpd {best.get('net_profit', '')}/{best.get('profit_factor', '')}/{best.get('max_drawdown_percent', '')}/{best.get('trades_per_day', '')}."
  - "Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음)."
"""
    write_text(WORKSPACE_STATE, state)
    current = f"""# Current Working State(현재 작업 상태)

Updated(갱신): {created_at}

Active stage(활성 단계): `{STAGE_ID}`

Current run(현재 실행): `{NEXT_RUN_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

## Current Truth(현재 진실)

Action(행동): F78D MT5 Runtime Probe(MT5 런타임 탐침)를 실행/시도했다.

Effect(효과): F78B execution-calibrated proxy(실행 보정 프록시)를 Strategy Tester(전략 테스터) 근거로 물질화했고, 다음 F78E gap analysis(간극 분석)의 입력을 만들었다.

## Runtime Result(런타임 결과)

- attempts/completed(시도/완료): `{summary['attempt_count']}/{summary['completed_attempt_count']}`
- probability/signal/feature/reproduction parity(확률/신호/피처/재현 동등성): `{summary['probability_parity_pass_rows']}/{summary['signal_parity_pass_rows']}/{summary['feature_readiness_pass_rows']}/{summary['source_reproduction_pass_rows']}`
- best runtime net/PF/DD/tpd(최선 런타임 순수익/수익 팩터/손실폭/일 거래): `{best.get('net_profit', '')}/{best.get('profit_factor', '')}/{best.get('max_drawdown_percent', '')}/{best.get('trades_per_day', '')}`

## Open Work(열린 작업)

- next run(다음 실행): `{NEXT_RUN_ID}`
- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    write_text(CURRENT_WORKING_STATE, current)
    selection = f"""# F78 Selection Status(F78 선택 상태)

Updated(갱신): {created_at}

Status(상태): `{payload.get('status')}`

Judgment(판정): `{payload.get('judgment')}`

Action(행동): F78D MT5 Runtime Probe(MT5 런타임 탐침)를 실행/시도했다.

Effect(효과): 다음 실행은 F78E proxy/runtime gap analysis(프록시/런타임 간극 분석)와 repair decision(수리 결정)이다.

Current run(현재 실행): `{NEXT_RUN_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    write_text(SELECTED_DIR / "selection_status.md", selection)


def build_payload(
    *,
    created_at: str,
    target: Mapping[str, Any],
    artifact: Mapping[str, Any],
    probability: Sequence[Mapping[str, Any]],
    signal: Sequence[Mapping[str, Any]],
    feature_parity: Sequence[Mapping[str, Any]],
    reproduction_rows: Sequence[Mapping[str, Any]],
    attempts: Sequence[Mapping[str, Any]],
    compile_payload: Mapping[str, Any],
    execution_results: Sequence[Mapping[str, Any]],
    runtime_receipt: Sequence[Mapping[str, Any]],
    status: str,
    judgment: str,
    include_oos: bool,
) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "status": status,
        "judgment": judgment,
        "created_at_utc": created_at,
        "target": dict(target),
        "include_oos": include_oos,
        "artifact_rows": [artifact],
        "probability_parity": list(probability),
        "signal_parity": list(signal),
        "feature_readiness_parity": list(feature_parity),
        "source_reproduction": list(reproduction_rows),
        "attempts": list(attempts),
        "compile_payload": compile_payload,
        "execution_results": list(execution_results),
        "runtime_receipt": list(runtime_receipt),
        "runtime_parity_receipt": rel(RUNTIME_PARITY_PATH),
        "backtest_forensics_receipt": rel(BACKTEST_FORENSICS_PATH),
        "claim_boundary": CLAIM_BOUNDARY,
    }


def main() -> int:
    args = parse_args()
    ensure_dirs()
    created_at = now_utc()
    target = target_row()
    context = build_context(target)
    artifact, probability, signal, feature_parity = materialize(context, Path(args.common_files_root))
    attempts = build_attempts(context, artifact, include_oos=bool(args.include_oos)) if artifact.get("export_status") == "negative_control_parity_passed" else []
    compile_payload = runtime_base.compile_runtime_ea(Path(args.metaeditor_path))
    execution_results: list[dict[str, Any]] = []
    if args.execute and not args.materialize_only and attempts:
        execution_results = runtime_base.execute_attempts(args, attempts, compile_payload)
        reports = f71d.mt5.collect_mt5_strategy_report_artifacts(
            terminal_data_root=Path(args.terminal_data_root),
            run_output_root=RUN_DIR,
            attempts=attempts,
            run_id=RUN_ID,
        )
        f71d.mt5.attach_mt5_report_metrics(execution_results, reports)
    f71d.RUN_ID = RUN_ID
    f71d.CLAIM_BOUNDARY = CLAIM_BOUNDARY
    runtime_receipt = f71d.build_runtime_receipt(execution_results, attempts) if execution_results else []
    completed = sum(1 for row in runtime_receipt if row.get("tester_status") == "completed")
    if artifact.get("export_status") != "negative_control_parity_passed":
        status = "materialization_parity_failed_runtime_probe_not_started_no_authority"
        judgment = "runtime_materialization_invalid_repair_required_no_authority"
    elif args.execute and completed:
        status = "completed_mt5_execution_calibrated_negative_control_runtime_probe_observation_no_authority"
        judgment = "runtime_probe_completed_gap_analysis_required_no_authority"
    elif args.execute:
        status = "blocked_mt5_execution_calibrated_runtime_probe_attempted_no_authority"
        judgment = "runtime_probe_blocked_or_missing_output_repair_required_no_authority"
    else:
        status = "materialized_pending_mt5_runtime_probe_execution_no_authority"
        judgment = "runtime_probe_materialized_pending_execution_no_authority"
    payload = build_payload(
        created_at=created_at,
        target=target,
        artifact=artifact,
        probability=probability,
        signal=signal,
        feature_parity=feature_parity,
        reproduction_rows=context["reproduction_rows"],
        attempts=attempts,
        compile_payload=compile_payload,
        execution_results=execution_results,
        runtime_receipt=runtime_receipt,
        status=status,
        judgment=judgment,
        include_oos=bool(args.include_oos),
    )
    runtime_parity = runtime_parity_receipt(payload)
    backtest_forensics = backtest_forensics_receipt(payload)
    write_json(RUNTIME_PARITY_PATH, runtime_parity)
    write_json(BACKTEST_FORENSICS_PATH, backtest_forensics)
    payload["runtime_parity"] = runtime_parity
    payload["backtest_forensics"] = backtest_forensics
    write_json(RUN_MANIFEST_PATH, payload)
    summary = build_summary(payload)
    write_json(SUMMARY_PATH, summary)
    write_csv(RUN_DIR / "f78d_probability_parity.csv", probability)
    write_csv(RUN_DIR / "f78d_signal_parity.csv", signal)
    write_csv(RUN_DIR / "f78d_feature_readiness_parity.csv", feature_parity)
    write_csv(RUN_DIR / "f78d_source_reproduction.csv", context["reproduction_rows"])
    write_csv(RUN_DIR / "f78d_runtime_receipt.csv", runtime_receipt, f71d.RUNTIME_RECEIPT_COLUMNS)
    write_json(RUN_DIR / "f78d_execution_results.json", execution_results)
    write_text(REPORT_PATH, report_text(payload, created_at))
    write_text(GATE_AUDIT_PATH, gate_audit_text(payload, created_at))
    update_ledgers(payload, created_at)
    update_registers_and_state(payload, created_at)
    print(
        json.dumps(
            {
                "status": status,
                "judgment": judgment,
                "attempt_count": summary["attempt_count"],
                "completed_attempt_count": summary["completed_attempt_count"],
                "parity": {
                    "probability": summary["probability_parity_pass_rows"],
                    "signal": summary["signal_parity_pass_rows"],
                    "feature": summary["feature_readiness_pass_rows"],
                    "reproduction": summary["source_reproduction_pass_rows"],
                },
                "best_runtime": summary["best_runtime"],
                "report": rel(REPORT_PATH),
                "next_run_id": NEXT_RUN_ID,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
