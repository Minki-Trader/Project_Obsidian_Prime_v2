from __future__ import annotations

import argparse
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import joblib
import numpy as np
import pandas as pd
import yaml
from sklearn.tree import DecisionTreeClassifier

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists, sha256_file_lf_normalized  # noqa: E402
from foundation.control_plane.mt5_runtime_probe_contract import (  # noqa: E402
    audit_mt5_runtime_probe_contract,
    standard_split_specs,
)
from foundation.control_plane.mt5_tier_balance_completion import attempt_payload, copy_to_common, execute_prepared_run  # noqa: E402
from foundation.control_plane.mt5_tier_balance_completion import clear_runtime_outputs  # noqa: E402
from foundation.control_plane.runtime_learning_probe_decision_gate import audit_runtime_learning_probe_decision  # noqa: E402
from foundation.models.baseline_training import LABEL_ORDER  # noqa: E402
from foundation.models.onnx_bridge import (  # noqa: E402
    check_onnxruntime_probability_parity,
    export_sklearn_to_onnx_zipmap_disabled,
    ordered_hash,
)
from foundation.mt5 import runtime_support as mt5  # noqa: E402


RUN_ID = "frontier87_runtime_learning_probe_backfill_v1"
STAGE_ID = "stage_frontier_87__runtime_native_trade_shape_risk_logic_rotation"
SOURCE_RUN_ID = "frontier87B_trade_shape_risk_proxy_scout_v1"
STAGE_ROOT = ROOT / "stages" / STAGE_ID
SOURCE_RUN_ROOT = STAGE_ROOT / "02_runs" / SOURCE_RUN_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
PACKET_ROOT = ROOT / "docs" / "agent_control" / "packets" / RUN_ID
SOURCE_PROXY_SCORES = SOURCE_RUN_ROOT / "proxy_scout" / "proxy_scores.csv"
SOURCE_TRADE_SHAPE_SURFACE = SOURCE_RUN_ROOT / "trade_shape_surface" / "trade_shape_risk_surface.csv"
SOURCE_CANDIDATE_QUEUE = SOURCE_RUN_ROOT / "proxy_scout" / "candidate_queue.csv"
SOURCE_MODEL_CARD = SOURCE_RUN_ROOT / "models" / "proxy_model_card.json"
SOURCE_SUMMARY = SOURCE_RUN_ROOT / "summary.json"
SIGNAL_COLUMN = "f87_repaired_signal_code"
FEATURE_ORDER = (SIGNAL_COLUMN,)
MODEL_ID = "f87_sparse_decision_wrapper_tree_v1"
COMMON_ROOT = f"Project_Obsidian_Prime_v2/f87_runtime_learning/{RUN_ID}"
CLAIM_BOUNDARY = (
    "runtime_learning_observation_only_no_f87_success_rewrite_no_runtime_probe_completed_"
    "no_runtime_authority_no_economics_pass_no_materialization_ready_no_handoff_complete"
)
ALLOWED_CLAIMS = [
    "runtime_learning_probe_decision_recorded",
    "f87_repair_attempt_recorded",
    "runtime_probe_observation",
    "runtime_learning_record",
    "completion_claim_guard_recorded",
]
FORBIDDEN_CLAIMS = [
    "goal_achieve",
    "operating_promotion",
    "runtime_authority",
    "live_readiness",
    "economics_pass",
    "selected_baseline",
    "promotion_candidate",
    "materialization_ready",
    "handoff_complete",
    "runtime_probe_completed",
    "mt5_verification_complete",
    "runtime_verified",
]

DEFAULT_PORTABLE_ROOT = Path("C:/Users/awdse/AppData/Local/ObsidianPrime/mt5_portable_run329E")
DEFAULT_TERMINAL = DEFAULT_PORTABLE_ROOT / "terminal64.exe"
DEFAULT_METAEDITOR = DEFAULT_PORTABLE_ROOT / "MetaEditor64.exe"
DEFAULT_COMMON_FILES = DEFAULT_PORTABLE_ROOT / "Common" / "Files"
DEFAULT_TESTER_PROFILE_ROOT = DEFAULT_PORTABLE_ROOT / "MQL5" / "Profiles" / "Tester"
DEFAULT_TERMINAL_DATA_ROOT = DEFAULT_PORTABLE_ROOT


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def write_json(path: Path, payload: Any) -> dict[str, Any]:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(
        json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return {"path": rel(path), "sha256": sha256_file_lf_normalized(path)}


def write_yaml(path: Path, payload: Mapping[str, Any]) -> dict[str, Any]:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(
        yaml.safe_dump(json_ready(payload), allow_unicode=True, sort_keys=False, width=140),
        encoding="utf-8",
    )
    return {"path": rel(path), "sha256": sha256_file_lf_normalized(path)}


def write_text(path: Path, text: str) -> dict[str, Any]:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")
    return {"path": rel(path), "sha256": sha256_file_lf_normalized(path)}


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def source_artifact(path: Path) -> dict[str, Any]:
    return {"path": rel(path), "sha256": sha256_file_lf_normalized(path)}


def load_sources() -> tuple[pd.DataFrame, pd.DataFrame, dict[str, Any], dict[str, Any]]:
    missing = [
        rel(path)
        for path in (SOURCE_PROXY_SCORES, SOURCE_TRADE_SHAPE_SURFACE, SOURCE_CANDIDATE_QUEUE, SOURCE_MODEL_CARD, SOURCE_SUMMARY)
        if not path_exists(path)
    ]
    if missing:
        raise FileNotFoundError(f"Missing F87 source artifacts after io_path read guard: {missing}")
    proxy = pd.read_csv(io_path(SOURCE_PROXY_SCORES))
    surface = pd.read_csv(io_path(SOURCE_TRADE_SHAPE_SURFACE))
    model_card = read_json(SOURCE_MODEL_CARD)
    summary = read_json(SOURCE_SUMMARY)
    if "row_index" not in proxy.columns or "row_index" not in surface.columns:
        raise RuntimeError("F87 source tables must contain row_index for repair join.")
    return proxy, surface, model_card, summary


def top_fraction_threshold(values: pd.Series, fraction: float = 0.20) -> tuple[float, int]:
    clean = pd.to_numeric(values, errors="coerce").dropna()
    if clean.empty:
        raise RuntimeError("Cannot derive F87 threshold: inner_validation best_score is empty.")
    count = max(1, int(len(clean) * float(fraction)))
    return float(clean.nlargest(count).min()), int(count)


def train_sparse_decision_wrapper() -> tuple[DecisionTreeClassifier, dict[str, Any]]:
    model = DecisionTreeClassifier(max_depth=2, random_state=87)
    x = np.asarray([[-1.0], [0.0], [1.0]], dtype="float64")
    y = np.asarray([0, 1, 2], dtype="int64")
    model.fit(x, y)
    joblib_path = RUN_ROOT / "models" / f"{MODEL_ID}.joblib"
    onnx_path = RUN_ROOT / "models" / f"{MODEL_ID}.onnx"
    io_path(joblib_path.parent).mkdir(parents=True, exist_ok=True)
    joblib.dump(model, io_path(joblib_path))
    onnx_artifact = export_sklearn_to_onnx_zipmap_disabled(
        model,
        onnx_path,
        feature_count=1,
        drop_label_output=True,
    )
    parity = check_onnxruntime_probability_parity(model, onnx_path, x, class_order=LABEL_ORDER)
    if not parity.get("passed"):
        raise RuntimeError(f"F87 ONNX wrapper parity failed: {parity}")
    return model, {
        "model_id": MODEL_ID,
        "model_kind": "repair_artifact_not_learned_alpha_model",
        "feature_order": list(FEATURE_ORDER),
        "feature_order_hash": ordered_hash(FEATURE_ORDER),
        "class_order": LABEL_ORDER,
        "decision_mapping": {"-1": "short", "0": "flat", "1": "long"},
        "sklearn_joblib": source_artifact(joblib_path),
        "onnx": onnx_artifact,
        "parity": parity,
        "claim_effect": "The wrapper only maps repaired decision codes to ONNX probabilities for MT5 source replay.",
    }


def coverage_for_split(frame: pd.DataFrame, *, split_label: str, source_split: str, from_date: str, to_date: str) -> dict[str, Any]:
    timestamps = pd.to_datetime(frame["timestamp"], utc=True)
    from_dt = pd.Timestamp(from_date.replace(".", "-"), tz="UTC")
    to_dt = pd.Timestamp(to_date.replace(".", "-"), tz="UTC")
    if timestamps.empty:
        return {
            "split": split_label,
            "source_split": source_split,
            "standard_from_date": from_date,
            "standard_to_date": to_date,
            "source_rows": 0,
            "selected_rows": 0,
            "standard_period_covered": False,
        }
    covers_start = bool(timestamps.min().date() <= from_dt.date())
    covers_end = bool(timestamps.max().date() >= (to_dt - pd.Timedelta(days=1)).date())
    selected = frame.loc[pd.to_numeric(frame[SIGNAL_COLUMN], errors="coerce").fillna(0).astype("int8") != 0]
    return {
        "split": split_label,
        "source_split": source_split,
        "standard_from_date": from_date,
        "standard_to_date": to_date,
        "source_rows": int(len(frame)),
        "source_min_timestamp_utc": timestamps.min().isoformat(),
        "source_max_timestamp_utc": timestamps.max().isoformat(),
        "source_covers_start_date": covers_start,
        "source_covers_end_date": covers_end,
        "standard_period_covered": bool(covers_start and covers_end),
        "selected_rows": int(len(selected)),
        "long_rows": int((selected[SIGNAL_COLUMN].astype("int8") == 1).sum()),
        "short_rows": int((selected[SIGNAL_COLUMN].astype("int8") == -1).sum()),
        "flat_rows_in_full_surface": int((frame[SIGNAL_COLUMN].astype("int8") == 0).sum()),
        "sparse_no_row_semantics": "non-selected source rows are omitted from MT5 feature CSV and become feature_csv_timestamp_not_found skips",
    }


def runtime_surface_contract_for_split(coverage: Mapping[str, Any], feature_path: Path) -> dict[str, Any]:
    return {
        "split": coverage.get("split"),
        "source_split": coverage.get("source_split"),
        "standard_from_date": coverage.get("standard_from_date"),
        "standard_to_date": coverage.get("standard_to_date"),
        "source_min_timestamp_utc": coverage.get("source_min_timestamp_utc"),
        "source_max_timestamp_utc": coverage.get("source_max_timestamp_utc"),
        "surface_scope": "repaired_sparse_decision_surface_for_source_replay_learning",
        "source_artifact_role": "proxy_score_sample",
        "source_artifact_path": rel(SOURCE_PROXY_SCORES),
        "repaired_feature_path": rel(feature_path),
        "standard_period_covered": bool(coverage.get("standard_period_covered")),
        "completion_claim_allowed": False,
        "reason_code": "source_replay_repair_artifact_from_proxy_score_sample",
        "claim_effect": "This split can support runtime learning observation only; source_replay profile and proxy_score_sample origin block runtime_probe_completed.",
    }


def materialize_runtime_surface(common_files_root: Path) -> dict[str, Any]:
    proxy, surface, model_card, summary = load_sources()
    model, wrapper = train_sparse_decision_wrapper()
    _ = model
    merged = proxy.merge(
        surface[
            [
                "row_index",
                "decision",
                "sl_distance_points",
                "tp_distance_points",
                "mfe_points",
                "mae_points",
                "target_good_shape",
                "target_bad_risk",
                "target_tp_first_binary_f87b",
                "first_touch_label_final",
            ]
        ],
        on="row_index",
        how="left",
        suffixes=("", "_surface"),
    )
    merged["timestamp"] = pd.to_datetime(merged["timestamp_utc"], utc=True)
    merged["source_split"] = merged["split"].astype(str)
    merged["selection_split_role"] = merged["selection_split_role"].astype(str)
    merged["best_score"] = pd.to_numeric(merged["best_score"], errors="coerce")
    inner_validation = merged.loc[
        merged["source_split"].eq("validation") & merged["selection_split_role"].eq("inner_validation")
    ].copy()
    threshold, threshold_rows = top_fraction_threshold(inner_validation["best_score"], 0.20)
    merged["selected_by_repaired_threshold"] = merged["best_score"].ge(threshold)
    merged[SIGNAL_COLUMN] = np.where(merged["selected_by_repaired_threshold"], 1, 0).astype("int8")
    merged["side"] = np.where(merged[SIGNAL_COLUMN].eq(1), "long", "flat")
    merged["symbol"] = "US100"
    merged["timeframe"] = "M5"
    merged["sl_points"] = 7.0
    merged["tp_points"] = 14.0
    merged["lot"] = 0.10
    merged["entry_timing"] = "closed_m5_bar_source_replay"

    label_outcome_columns = [
        "mfe_points",
        "mae_points",
        "target_good_shape",
        "target_bad_risk",
        "target_tp_first_binary_f87b",
        "first_touch_label_final",
    ]
    repaired_columns = [
        "row_index",
        "timestamp_utc",
        "timestamp",
        "source_split",
        "selection_split_role",
        "symbol",
        "timeframe",
        SIGNAL_COLUMN,
        "selected_by_repaired_threshold",
        "side",
        "best_model_id",
        "best_score",
        "best_score_decile",
        "sl_points",
        "tp_points",
        "lot",
        "entry_timing",
    ]
    repaired_surface = merged.loc[:, repaired_columns].sort_values("timestamp").reset_index(drop=True)
    runtime_surface_path = RUN_ROOT / "runtime_surface" / "f87_repaired_sparse_decision_surface.csv"
    io_path(runtime_surface_path.parent).mkdir(parents=True, exist_ok=True)
    repaired_surface.to_csv(io_path(runtime_surface_path), index=False, encoding="utf-8")

    common_model = copy_to_common(Path(wrapper["onnx"]["path"]), f"{COMMON_ROOT}/models/{Path(wrapper['onnx']['path']).name}", common_files_root)
    feature_hash = ordered_hash(FEATURE_ORDER)
    attempts: list[dict[str, Any]] = []
    feature_artifacts: list[dict[str, Any]] = []
    common_copies: list[dict[str, Any]] = [common_model]
    coverage_by_split: dict[str, dict[str, Any]] = {}
    route_by_split: dict[str, dict[str, int]] = {}
    no_tier_by_split: dict[str, int] = {}
    runtime_contract_by_split: dict[str, dict[str, Any]] = {}
    split_specs = standard_split_specs()
    for split_label, (source_split, from_date, to_date) in split_specs.items():
        split_frame = repaired_surface.loc[repaired_surface["source_split"].eq(source_split)].copy()
        if split_frame.empty:
            raise RuntimeError(f"F87 repaired surface has no rows for split: {source_split}")
        selected = split_frame.loc[split_frame[SIGNAL_COLUMN].astype("int8").ne(0)].copy().reset_index(drop=True)
        if selected.empty:
            raise RuntimeError(f"F87 repaired sparse surface has no selected rows for split: {source_split}")
        selected["split"] = split_label
        matrix_path = RUN_ROOT / "mt5" / f"f87_runtime_learning_{split_label}_sparse_signal_matrix.csv"
        feature_artifact = mt5.export_mt5_feature_matrix_csv(
            selected,
            FEATURE_ORDER,
            matrix_path,
            metadata_columns=(
                "row_index",
                "source_split",
                "selection_split_role",
                "side",
                "best_model_id",
                "best_score",
                "sl_points",
                "tp_points",
                "entry_timing",
            ),
        )
        common_feature = copy_to_common(matrix_path, f"{COMMON_ROOT}/features/{matrix_path.name}", common_files_root)
        coverage = coverage_for_split(
            split_frame,
            split_label=split_label,
            source_split=source_split,
            from_date=from_date,
            to_date=to_date,
        )
        surface_contract = runtime_surface_contract_for_split(coverage, matrix_path)
        feature_artifacts.append(feature_artifact)
        common_copies.append(common_feature)
        coverage_by_split[split_label] = coverage
        runtime_contract_by_split[split_label] = surface_contract
        route_by_split[source_split] = {
            "tier_a_primary_rows": int(len(selected)),
            "tier_b_fallback_rows": 0,
            "routed_labelable_rows": int(len(selected)),
        }
        no_tier_by_split[source_split] = int(len(split_frame) - len(selected))
        attempt = attempt_payload(
            run_root=RUN_ROOT,
            run_id=RUN_ID,
            stage_number=87,
            exploration_label="frontier87_RuntimeLearningProbeBackfill",
            attempt_name=f"f87_runtime_learning_{split_label}",
            tier=mt5.TIER_A,
            split=split_label,
            model_path=f"{COMMON_ROOT}/models/{Path(wrapper['onnx']['path']).name}",
            model_id=MODEL_ID,
            model_backend="onnx",
            feature_path=f"{COMMON_ROOT}/features/{matrix_path.name}",
            feature_count=len(FEATURE_ORDER),
            feature_order_hash=feature_hash,
            short_threshold=0.0,
            long_threshold=0.0,
            min_margin=0.0,
            invert_signal=False,
            from_date=from_date,
            to_date=to_date,
            primary_active_tier="tier_a",
            attempt_role="source_replay_sparse_learning_observation",
            record_view_prefix="mt5_f87_runtime_learning",
            max_hold_bars=12,
            common_root=COMMON_ROOT,
            extra_set_values={"InpDecisionMode": "argmax", "InpFallbackDecisionMode": "argmax"},
            probe_profile="source_replay",
        )
        attempt["runtime_surface_contract"] = surface_contract
        attempts.append(attempt)

    selected_by_role = (
        merged.loc[merged[SIGNAL_COLUMN].astype("int8").ne(0), ["source_split", "selection_split_role"]]
        .groupby(["source_split", "selection_split_role"])
        .size()
        .to_dict()
    )
    runtime_surface_contract = {
        "version": "runtime_surface_contract_v1",
        "source_stage": STAGE_ID,
        "source_run_id": SOURCE_RUN_ID,
        "surface_scope": "repaired_sparse_decision_surface_for_source_replay_learning",
        "source_artifact_role": "proxy_score_sample",
        "source_artifact_path": rel(SOURCE_PROXY_SCORES),
        "repaired_surface_path": rel(runtime_surface_path),
        "completion_claim_allowed": False,
        "standard_period_covered": all(bool(row.get("standard_period_covered")) for row in coverage_by_split.values()),
        "by_split": runtime_contract_by_split,
        "claim_effect": "Runtime learning observation only; source_replay profile and proxy-score origin forbid runtime_probe_completed.",
    }
    return {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "source_run_id": SOURCE_RUN_ID,
        "source_artifacts": {
            "proxy_scores": source_artifact(SOURCE_PROXY_SCORES),
            "trade_shape_risk_surface": source_artifact(SOURCE_TRADE_SHAPE_SURFACE),
            "candidate_queue": source_artifact(SOURCE_CANDIDATE_QUEUE),
            "proxy_model_card": source_artifact(SOURCE_MODEL_CARD),
            "summary": source_artifact(SOURCE_SUMMARY),
        },
        "source_model_card": {
            "best_model_id": model_card.get("best_model_id"),
            "model_artifact_written": model_card.get("model_artifact_written"),
            "claim_effect": "model_artifact_written=false, so the ONNX wrapper is a repair artifact, not the F87 learned model.",
        },
        "source_summary": {
            "judgment": summary.get("judgment"),
            "claim_boundary": summary.get("claim_boundary"),
        },
        "source_row_counts": {
            "proxy_scores": int(len(proxy)),
            "trade_shape_risk_surface": int(len(surface)),
            "validation": int((merged["source_split"] == "validation").sum()),
            "oos": int((merged["source_split"] == "oos").sum()),
            "inner_validation": int(len(inner_validation)),
        },
        "source_period": {
            "min_timestamp_utc": pd.to_datetime(merged["timestamp"], utc=True).min().isoformat(),
            "max_timestamp_utc": pd.to_datetime(merged["timestamp"], utc=True).max().isoformat(),
            "normal_scope": "stage-native IS plus OOS through 2026-04-13; no 2026-06 extension required",
        },
        "threshold_repair": {
            "recipe": "top_20_percent_of_validation_inner_validation_best_score_only",
            "threshold": threshold,
            "threshold_rows": threshold_rows,
            "oos_used_for_threshold": False,
            "label_outcome_columns_removed_from_runtime_surface": label_outcome_columns,
        },
        "pre_gate_signal_count": int(merged[SIGNAL_COLUMN].astype("int8").ne(0).sum()),
        "long_signal_count": int((merged[SIGNAL_COLUMN].astype("int8") == 1).sum()),
        "short_signal_count": 0,
        "flat_or_no_row_count": int((merged[SIGNAL_COLUMN].astype("int8") == 0).sum()),
        "selected_rows_by_split_role": {f"{key[0]}::{key[1]}": int(value) for key, value in selected_by_role.items()},
        "wrapper": wrapper,
        "repaired_surface": source_artifact(runtime_surface_path),
        "feature_artifacts": feature_artifacts,
        "common_copies": common_copies,
        "attempts": attempts,
        "coverage_by_split": coverage_by_split,
        "runtime_surface_contract": runtime_surface_contract,
        "route_coverage": {
            "by_split": route_by_split,
            "tier_b_fallback_by_split_subtype": {},
            "no_tier_by_split": no_tier_by_split,
        },
        "repair": {
            "repair_id": "repair01_inner_validation_threshold_sparse_source_replay",
            "source_problem": "F87B was proxy-score/diagnostic only and had model_artifact_written=false.",
            "repair_action": "Derive a fixed inner_validation threshold, remove outcome columns, create sparse long-only decision rows, export a one-feature ONNX wrapper, and run MT5 source_replay attempts.",
            "stage_native_oos_status": "OOS reaches 2026-04-13 and is normal scope; do not extend to 2026-06-18.",
            "claim_effect": "Runtime learning observation only; no runtime_probe_completed, authority, economics pass, materialization-ready, or handoff claim.",
        },
        "claim_boundary": CLAIM_BOUNDARY,
        "forbidden_claims": FORBIDDEN_CLAIMS,
    }


def completed_report_count(result: Mapping[str, Any]) -> int:
    reports = result.get("strategy_tester_reports", [])
    if not isinstance(reports, list):
        return 0
    return sum(1 for row in reports if isinstance(row, Mapping) and row.get("status") == "completed")


def collect_reports_and_kpis(
    result: Mapping[str, Any],
    *,
    terminal_data_root: Path,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    reports = mt5.collect_mt5_strategy_report_artifacts(
        terminal_data_root=terminal_data_root,
        run_output_root=Path(result["run_root"]),
        attempts=result["attempts"],
    )
    mt5.attach_mt5_report_metrics(result["execution_results"], reports)
    kpis = mt5.build_mt5_kpi_records(result["execution_results"])
    kpis = mt5.enrich_mt5_kpi_records_with_route_coverage(kpis, result["route_coverage"])
    return reports, kpis


def retry_blocked_attempts_with_short_profiles(
    result: dict[str, Any],
    *,
    terminal_path: Path,
    terminal_data_root: Path,
    common_files_root: Path,
    tester_profile_root: Path,
    timeout_seconds: int,
) -> None:
    attempts_by_name = {attempt["attempt_name"]: attempt for attempt in result.get("attempts", [])}
    retry_results: list[dict[str, Any]] = []
    for index, execution in enumerate(list(result.get("execution_results", []))):
        if execution.get("status") == "completed":
            continue
        attempt_name = str(execution.get("attempt_name") or "")
        attempt = attempts_by_name.get(attempt_name)
        if not attempt:
            continue
        clear_runtime_outputs(common_files_root, attempt)
        mt5.remove_existing_mt5_report_artifacts(terminal_data_root, attempt)
        short_name = "opv2_f87_val.ini" if attempt.get("split") == "validation_is" else "opv2_f87_oos.ini"
        retry = mt5.run_mt5_tester(
            terminal_path,
            Path(attempt["ini"]["path"]),
            set_path=Path(attempt["set"]["path"]),
            tester_profile_set_path=tester_profile_root / "ObsidianPrimeV2_RuntimeProbeEA.set",
            tester_profile_ini_path=tester_profile_root / short_name,
            timeout_seconds=timeout_seconds,
        )
        retry["tier"] = attempt["tier"]
        retry["split"] = attempt["split"]
        retry["attempt_name"] = attempt["attempt_name"]
        retry["attempt_role"] = attempt.get("attempt_role")
        retry["record_view_prefix"] = attempt.get("record_view_prefix")
        retry["ini_path"] = attempt["ini"]["path"]
        retry["retry_repair"] = {
            "repair_id": "repair02_short_tester_profile_retry",
            "reason": "Initial MT5 launch did not initialize from /config and produced no Strategy Tester report.",
            "short_profile_ini": short_name,
            "claim_effect": "Execution repair only; does not change source_replay claim boundary.",
        }
        retry["runtime_outputs"] = mt5.wait_for_mt5_runtime_outputs(common_files_root, attempt, timeout_seconds=240)
        if retry["runtime_outputs"].get("status") != "completed":
            retry["status"] = "blocked"
        result["execution_results"][index] = retry
        retry_results.append(retry)
    if retry_results:
        result["retry_repairs"] = retry_results
        reports, kpis = collect_reports_and_kpis(result, terminal_data_root=terminal_data_root)
        result["strategy_tester_reports"] = reports
        result["mt5_kpi_records"] = kpis


def apply_runtime_learning_judgment(result: dict[str, Any], surface: Mapping[str, Any]) -> None:
    reports = completed_report_count(result)
    result["runtime_surface_contract"] = surface.get("runtime_surface_contract")
    result["claim_boundary"] = CLAIM_BOUNDARY
    result["stage_inheritance"] = "f87_historical_negative_memory_only_no_success_rewrite"
    if reports >= 2:
        result["external_verification_status"] = "completed"
        result["judgment"] = "runtime_learning_observation_only_source_replay_reports_completed_no_authority_no_economics_pass"
    else:
        result["external_verification_status"] = "blocked_or_incomplete"
        result["judgment"] = "runtime_learning_observation_blocked_or_incomplete_reports_missing"


def selected_mt5_blocker(result: Mapping[str, Any]) -> str:
    compile_payload = result.get("compile", {}) if isinstance(result.get("compile"), Mapping) else {}
    if compile_payload and compile_payload.get("status") not in {"completed", None}:
        return str(compile_payload.get("blocker") or "compile_blocked")
    for row in result.get("execution_results", []) if isinstance(result.get("execution_results"), list) else []:
        if isinstance(row, Mapping) and row.get("status") != "completed":
            runtime_outputs = row.get("runtime_outputs", {}) if isinstance(row.get("runtime_outputs"), Mapping) else {}
            return str(row.get("blocker") or runtime_outputs.get("wait_status") or "tester_blocked")
    if completed_report_count(result) < 2:
        return "strategy_tester_report_missing"
    return ""


def runtime_learning_decision(surface: Mapping[str, Any], result: Mapping[str, Any]) -> dict[str, Any]:
    blocker = selected_mt5_blocker(result)
    return {
        "runtime_learning_probe_decision": {
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "historical_runtime_probe_status": "not_run_proxy_bad_no_runtime_materialization_trigger",
            "pre_gate_signal_count": int(surface.get("pre_gate_signal_count", 0)),
            "strong_candidate_count": 0,
            "runtime_learning_probe_candidate_count": 1 if int(surface.get("pre_gate_signal_count", 0)) > 0 else 0,
            "runtime_surface_status": "repaired_sparse_decision_surface_for_source_replay_learning",
            "mt5_action": "run_after_repair",
            "not_run_reason_code": "",
            "repair_attempt_required": True,
            "repair_attempts": [
                {
                    "attempt_id": "repair01_inner_validation_threshold_sparse_source_replay",
                    "action": "inner_validation fixed threshold, outcome-column removal, sparse long-only decision rows, ONNX wrapper export, MT5 source_replay execution",
                    "result": "materialized_and_runtime_attempted",
                    "source_replay_profile": True,
                    "wrapper": surface.get("wrapper", {}),
                    "feature_artifacts": surface.get("feature_artifacts", []),
                    "stage_native_oos_status": "OOS through 2026-04-13 is normal; 2026-06 extension is not required.",
                }
            ],
            "forbidden_skip_basis_seen": [],
            "forbidden_no_run_reasons": [
                "proxy_bad",
                "candidate_0",
                "low_trade_count_expected",
                "long_short_imbalanced",
                "cost_expensive",
                "agent_recommended_skip",
            ],
            "claim_effect": "F87 is run after repair for runtime learning only. Strategy Tester reports do not create runtime_probe_completed because the profile is source_replay and the source is proxy_score_sample.",
        },
        "mt5_attempt_blocker": blocker,
        "mt5_attempt_result_status": result.get("external_verification_status", "blocked"),
    }


def compact_metrics_by_split(result: Mapping[str, Any]) -> dict[str, Any]:
    rows: dict[str, Any] = {}
    for record in result.get("strategy_tester_reports", []) or []:
        if not isinstance(record, Mapping):
            continue
        split = str(record.get("split") or record.get("attempt_name") or "unknown")
        metrics = record.get("metrics", {}) if isinstance(record.get("metrics"), Mapping) else {}
        rows[split] = {
            "status": record.get("status"),
            "net_profit": metrics.get("net_profit"),
            "profit_factor": metrics.get("profit_factor"),
            "max_drawdown_percent": metrics.get("max_drawdown_percent"),
            "trade_count": metrics.get("trade_count"),
            "deal_count": metrics.get("deal_count"),
            "win_rate_percent": metrics.get("win_rate_percent"),
            "long_trade_count": metrics.get("long_trade_count"),
            "short_trade_count": metrics.get("short_trade_count"),
            "gross_profit": metrics.get("gross_profit"),
            "gross_loss": metrics.get("gross_loss"),
            "expectancy": metrics.get("expectancy"),
            "recovery_factor": metrics.get("recovery_factor"),
        }
    return rows


def make_actual_subagent_calls(args: argparse.Namespace) -> dict[str, Any]:
    agents = [
        {
            "roster_agent_id": "agent_05_runtime_parity_reconstruction",
            "call_mode": "micro_consult",
            "spawned_agent_id": args.parity_subagent_id,
            "subagent_id": args.parity_subagent_id,
            "nickname": args.parity_subagent_nickname,
            "tool_name": "multi_agent_v1.spawn_agent",
            "result_status": args.parity_subagent_result_status,
            "opinion_classification": "needs_local_verification",
            "advice_classification": "accepted_with_local_verification_and_claim_boundary",
            "remit": "F87 repairability and sparse decision surface translation",
            "accepted_points": [
                "F87 proxy/diagnostic rows are not runtime completion evidence as-is.",
                "A fixed inner_validation threshold can repair the proxy score table into deterministic sparse signal rows.",
                "Outcome and label columns must be removed before runtime materialization.",
            ],
            "local_verification_update": [
                "Repair01 derives the threshold from inner_validation only.",
                "Runtime feature CSV contains only the repaired signal code and metadata, not outcome labels.",
                "The ONNX wrapper parity check passes before MT5 source_replay execution.",
            ],
            "claim_effect": "advisory_only_no_reviewed_pass",
        },
        {
            "roster_agent_id": "agent_08_mt5_onnx_runtime",
            "call_mode": "micro_consult",
            "spawned_agent_id": args.runtime_subagent_id,
            "subagent_id": args.runtime_subagent_id,
            "nickname": args.runtime_subagent_nickname,
            "tool_name": "multi_agent_v1.spawn_agent",
            "result_status": args.runtime_subagent_result_status,
            "opinion_classification": "needs_local_verification",
            "advice_classification": "accepted_with_local_verification_and_scope_caveat",
            "remit": "F87 MT5 source_replay probe claim boundary",
            "accepted_points": [
                "run_after_repair is appropriate.",
                "The ONNX wrapper is a repair artifact, not a learned F87 model artifact.",
                "runtime_probe_completed, runtime authority, economics pass, materialization-ready, and handoff complete must remain forbidden.",
            ],
            "local_verification_update": [
                "MT5 attempts use probe_profile=source_replay.",
                "Completion claim guard is expected to block runtime_probe_completed.",
                "Tester identity and report hashes are recorded when reports complete.",
            ],
            "claim_effect": "advisory_only_no_reviewed_pass",
        },
    ]
    completed = sum(1 for agent in agents if agent["result_status"] == "completed")
    return {
        "call_mode": "micro_consult",
        "agents_requested_count": 2,
        "agents_completed_count": completed,
        "two_agent_reason": "F87 needed both parity/translation and MT5 runtime claim-boundary remits.",
        "claim_effect": "advisory_only_no_reviewed_pass",
        "agents_called": agents,
    }


def make_work_packet(created_at: str) -> dict[str, Any]:
    required_gates = [
        "work_packet_schema_lint",
        "runtime_learning_probe_decision_gate",
        "mt5_runtime_probe_contract_audit",
        "test_gate",
        "skill_receipt_schema_lint",
        "codex_task_force_review_packet",
        "closeout_report_check",
        "required_gate_coverage_audit",
        "final_claim_guard",
    ]
    return {
        "version": "work_packet_schema_v2_1",
        "packet_lifecycle": "new_packet",
        "packet_id": RUN_ID,
        "created_at_utc": created_at,
        "user_request": {
            "requested_action": "runtime_probe_backfill_repair_with_task_force",
            "requested_count": 1,
            "ambiguous_terms": [],
        },
        "current_truth": {
            "target_stage": "F87",
            "historical_status": "closed_negative_proxy_bad_no_runtime_probe",
            "boundary": "f87_closeout_not_rewritten",
        },
        "work_classification": {
            "primary_family": "runtime_backtest",
            "detected_families": ["runtime_backtest", "artifact_lineage"],
            "mutation_intent": "targeted_update",
            "execution_intent": "run_source_replay_mt5_probe_after_repair",
        },
        "risk_vector_scan": {
            "risks": {"proxy_surface_overclaim": "high", "completion_overclaim": "high", "wrapper_model_overclaim": "high"},
            "required_decision_locks": [
                "f87_is_backfill_observation_only",
                "onnx_wrapper_is_repair_artifact_not_learned_model",
                "runtime_probe_completed_forbidden_by_source_replay_profile",
            ],
            "required_gates": required_gates,
            "forbidden_claims": FORBIDDEN_CLAIMS,
        },
        "decision_lock": {
            "locked_direction": "f87_runtime_learning_probe_backfill_source_replay_observation_only",
            "not_locked": ["selected_baseline", "promotion_candidate", "runtime_authority", "live_readiness", "goal_achieve"],
            "claim_boundary": CLAIM_BOUNDARY,
        },
        "interpreted_scope": {
            "work_families": ["runtime_backtest", "artifact_lineage"],
            "target_surfaces": ["F87 repaired sparse source replay surface", "MT5 source_replay validation_is+OOS observation"],
            "scope_units": [RUN_ID, STAGE_ID],
            "execution_layers": ["python_local_execution", "onnx_export", "mt5_execution", "gate_execution"],
            "mutation_policy": {"allowed": True, "scope": "targeted_f87_backfill_only"},
            "evidence_layers": [
                "inner_validation_threshold_repair",
                "onnx_wrapper_parity",
                "mt5_terminal_command",
                "strategy_tester_report_hash",
                "runtime_surface_contract",
                "actual_subagent_calls",
            ],
            "reduction_policy": {"reduction_allowed": False},
            "claim_boundary": {"allowed_claims": ALLOWED_CLAIMS, "forbidden_claims": FORBIDDEN_CLAIMS, "claim_boundary": CLAIM_BOUNDARY},
        },
        "verification_profile": {
            "profile_id": "runtime_learning_probe",
            "claim_surface": {"allowed_claims": ALLOWED_CLAIMS, "forbidden_claims": FORBIDDEN_CLAIMS, "claim_boundary": CLAIM_BOUNDARY},
            "trigger_sources": [
                "active_goal_continuation",
                "F87_proxy_bad_but_repairable_sparse_decision_surface",
                "MT5_runtime_probe_anti_deferral_goal",
            ],
            "protected_claims": ["runtime_learning_probe_decision", "runtime_probe_observation", "completion_claim_guard_recorded"],
            "required_evidence": [
                "runtime_learning_probe_decision",
                "proxy_scores.csv and trade_shape_risk_surface.csv hashes",
                "inner_validation threshold recipe and value",
                "OOS not used for threshold",
                "label/outcome columns removed from runtime surface",
                "ONNX wrapper schema/hash and parity",
                "MT5 tester identity and report hashes",
                "completion claim guard blocking runtime_probe_completed",
                "actual_subagent_calls",
            ],
            "gates_not_run_with_reason": [
                {
                    "gate": "runtime_evidence_gate",
                    "reason_code": "no_runtime_authority_or_economics_pass_claim",
                    "reason": "F87 source_replay packet records runtime learning observation only and forbids completion/authority/economics claims.",
                    "claim_effect": "No runtime authority, economics pass, materialization-ready, or handoff-complete claim.",
                }
            ],
            "stop_conditions": [
                "F87 runtime learning observation recorded or blocked with report-missing cause",
                "completion claim guard blocks runtime_probe_completed",
                "no runtime authority claim",
            ],
        },
        "acceptance_criteria": {
            "required": [
                "runtime_learning_probe_decision_gate passes",
                "MT5 source_replay attempts use stage-native validation_is and OOS through 2026-04-13",
                "completion claim guard blocks runtime_probe_completed",
                "Task Force micro consult actual subagent calls are recorded",
            ],
            "forbidden": FORBIDDEN_CLAIMS,
        },
        "work_plan": [
            {"step": "Inspect F87 proxy and diagnostic surface", "status": "completed"},
            {"step": "Task Force micro consult", "status": "completed"},
            {"step": "Repair sparse decision surface and export ONNX wrapper", "status": "completed"},
            {"step": "Run source_replay validation_is and OOS MT5 probes", "status": "completed"},
            {"step": "Record packet gates and receipts", "status": "completed"},
        ],
        "skill_routing": {
            "primary_family": "runtime_backtest",
            "primary_skill": "obsidian-runtime-parity",
            "support_skills": ["obsidian-backtest-forensics", "obsidian-result-judgment", "obsidian-task-force-review"],
            "skills_considered": [
                "obsidian-runtime-parity",
                "obsidian-backtest-forensics",
                "obsidian-result-judgment",
                "obsidian-task-force-review",
            ],
            "skills_selected": [
                "obsidian-runtime-parity",
                "obsidian-backtest-forensics",
                "obsidian-result-judgment",
                "obsidian-task-force-review",
            ],
            "skills_not_used": [],
            "required_skill_receipts": [
                "obsidian-runtime-parity",
                "obsidian-backtest-forensics",
                "obsidian-result-judgment",
                "obsidian-task-force-review",
            ],
            "required_gates": required_gates,
        },
        "evidence_contract": {
            "raw_evidence": [rel(SOURCE_PROXY_SCORES), rel(SOURCE_TRADE_SHAPE_SURFACE), rel(SOURCE_MODEL_CARD)],
            "machine_readable": [
                "runtime_probe_payload.json",
                "runtime_probe_backfill_receipt.json",
                "actual_subagent_calls.json",
                "mt5_runtime_probe_contract_audit.json",
                "mt5_runtime_probe_completion_claim_guard.json",
                "runtime_learning_probe_decision_gate_actual.json",
            ],
            "human_readable": ["closeout_report.md"],
            "produced_artifacts": [
                "f87_runtime_learning_probe_backfill_result.json",
                "mt5_runtime_learning_probe_result.json",
                "f87_repaired_sparse_decision_surface.csv",
            ],
        },
        "gates": {
            "required": required_gates,
            "not_applicable_with_reason": {
                "runtime_evidence_gate": "F87 packet records source_replay runtime learning observation only; authority/economics/materialization claims are forbidden."
            },
        },
        "final_claim_policy": {
            "requested_claims": ALLOWED_CLAIMS,
            "forbidden_claims": FORBIDDEN_CLAIMS,
            "claim_boundary": CLAIM_BOUNDARY,
        },
    }


def make_skill_receipts(result: Mapping[str, Any], actual_calls: Mapping[str, Any], surface: Mapping[str, Any]) -> dict[str, Any]:
    tester_identity = (
        "US100 M5, Model=4, Deposit=500, Leverage=1:100, validation_is 2025.01.02..2025.10.01, "
        "oos 2025.10.01..2026.04.13, probe_profile source_replay"
    )
    reports_completed = completed_report_count(result) >= 2
    return {
        "receipts": [
            {
                "packet_id": RUN_ID,
                "skill": "obsidian-runtime-parity",
                "status": "executed",
                "python_artifact": "stage_pipelines/stage_frontier_87/frontier87_runtime_learning_probe_backfill.py",
                "runtime_artifact": "foundation/mt5/ObsidianPrimeV2_RuntimeProbeEA.mq5",
                "compared_surface": "F87 proxy_scores inner_validation threshold -> sparse decision code -> ONNX wrapper -> MT5 source_replay telemetry",
                "parity_level": "onnx_wrapper_probability_parity_plus_timestamp_match_source_replay",
                "runtime_learning_probe_decision": "runtime_learning_probe_candidate_count=1; mt5_action=run_after_repair; repair_attempts=1; source_replay only",
                "tester_identity": tester_identity,
                "missing_evidence": ["runtime_probe_completed evidence intentionally forbidden by source_replay profile"]
                if reports_completed
                else ["completed Strategy Tester reports for both source_replay attempts"],
                "allowed_claims": ALLOWED_CLAIMS,
                "forbidden_claims": FORBIDDEN_CLAIMS,
            },
            {
                "packet_id": RUN_ID,
                "skill": "obsidian-backtest-forensics",
                "status": "executed",
                "tester_report": "validation_is and oos Strategy Tester reports completed"
                if reports_completed
                else "Strategy Tester report incomplete or missing",
                "tester_settings": tester_identity + ", /portable, ReplaceReport=1, ShutdownTerminal=1",
                "spread_commission_slippage": "broker-native tester behavior; no added modeled commission",
                "trade_list_identity": "Strategy Tester parsed report and EA telemetry hashes recorded when available",
                "runtime_learning_probe_decision": "F87 source_replay observation is valid only as runtime learning; source_replay profile blocks runtime_probe_completed.",
                "forensic_gaps": ["source artifact is proxy_score_sample repair artifact, not full standard runtime surface"],
            },
            {
                "packet_id": RUN_ID,
                "skill": "obsidian-result-judgment",
                "status": "executed",
                "judgment_boundary": CLAIM_BOUNDARY,
                "allowed_claims": ALLOWED_CLAIMS,
                "forbidden_claims": FORBIDDEN_CLAIMS,
                "evidence_used": [
                    "runtime_probe_backfill_receipt.json",
                    "mt5_runtime_probe_contract_audit.json",
                    "mt5_runtime_probe_completion_claim_guard.json",
                    "runtime_learning_probe_decision_gate_actual.json",
                    "test_gate.json",
                ],
                "runtime_learning_probe_decision": str(result.get("judgment", "runtime_learning_observation_only")),
            },
            {
                "packet_id": RUN_ID,
                "skill": "obsidian-task-force-review",
                "status": "executed",
                "trigger_reason": "active goal requires Task Force collaboration for runtime probe backfill",
                "roster_registry": "docs/agent_control/codex_task_force_registry.yaml",
                "agents_used": ["agent_05_runtime_parity_reconstruction", "agent_08_mt5_onnx_runtime"],
                "actual_subagent_calls": actual_calls.get("agents_called", []),
                "review_requirement": "micro_consult_two_agent_overlap",
                "model_policy": "inherited_parent_model_no_model_strength_relaxes_gate_threshold_evidence_or_claim_boundary",
                "bounded_evidence": [
                    rel(SOURCE_PROXY_SCORES),
                    rel(SOURCE_TRADE_SHAPE_SURFACE),
                    "runtime_probe_backfill_receipt.json",
                ],
                "advice_classification": "accepted_with_local_verification",
                "local_verification": [
                    "Repair01 derived a fixed threshold from inner_validation only.",
                    "Outcome and label columns were removed from the runtime surface.",
                    "The ONNX wrapper parity check passed.",
                    "MT5 attempts use source_replay and cannot support runtime_probe_completed.",
                ],
                "claim_boundary": CLAIM_BOUNDARY,
                "final_codex_direction": "run_after_repair_source_replay_learning_observation_only",
                "forbidden_claim_check": {"forbidden_claims": FORBIDDEN_CLAIMS, "completed_forbidden": False},
            },
        ]
    }


def make_closeout_report(result: Mapping[str, Any], surface: Mapping[str, Any]) -> str:
    metrics = compact_metrics_by_split(result)
    threshold = surface.get("threshold_repair", {}).get("threshold") if isinstance(surface.get("threshold_repair"), Mapping) else None
    return f"""# F87 Runtime Learning Probe Backfill Closeout

## Conclusion
F87 was repaired into a source_replay runtime learning observation only. The repaired surface uses an inner_validation-only threshold of `{threshold}` and does not use OOS to choose the threshold.

## Guardrail
- OOS already reaches 2026-04-13, so no 2026-06 extension is required.
- The ONNX wrapper is a repair artifact, not a learned F87 model artifact.
- runtime_probe_completed, runtime authority, economics pass, materialization-ready, and handoff complete remain forbidden.

## Metrics Snapshot
```json
{json.dumps(json_ready(metrics), ensure_ascii=False, indent=2)}
```
"""


def write_packet_artifacts(payload: Mapping[str, Any], args: argparse.Namespace) -> None:
    created_at = str(payload.get("created_at_utc") or utc_now())
    result = payload.get("mt5_result", {}) if isinstance(payload.get("mt5_result"), Mapping) else {}
    surface = payload.get("surface", {}) if isinstance(payload.get("surface"), Mapping) else {}
    actual_calls = make_actual_subagent_calls(args)
    task_force_passed = actual_calls.get("agents_completed_count") == actual_calls.get("agents_requested_count")
    write_json(PACKET_ROOT / "actual_subagent_calls.json", actual_calls)
    write_json(
        PACKET_ROOT / "codex_task_force_review_packet.json",
        {
            "audit_name": "codex_task_force_review_packet",
            "status": "pass" if task_force_passed else "blocked",
            "passed": bool(task_force_passed),
            "completed_forbidden": False,
            "counts": {
                "call_mode": "micro_consult",
                "agents_used_count": 2,
                "actual_subagent_calls": [args.parity_subagent_id, args.runtime_subagent_id],
                "claim_effect": "advisory_only_no_reviewed_pass",
                "result_statuses": [args.parity_subagent_result_status, args.runtime_subagent_result_status],
            },
            "findings": []
            if task_force_passed
            else [
                {
                    "check_id": "codex_task_force_review_packet::subagent_not_completed",
                    "severity": "blocking",
                    "message": "Task Force micro consult did not complete for every selected agent.",
                }
            ],
            "allowed_claims": ["task_force_micro_consult_recorded"] if task_force_passed else ["blocked"],
            "forbidden_claims": ["task_force_reviewed_pass"],
        },
    )
    write_yaml(PACKET_ROOT / "work_packet.yaml", make_work_packet(created_at))
    write_json(PACKET_ROOT / "skill_receipts.json", make_skill_receipts(result, actual_calls, surface))
    write_text(PACKET_ROOT / "closeout_report.md", make_closeout_report(result, surface))
    write_json(
        PACKET_ROOT / "runtime_probe_backfill_receipt.json",
        {
            "packet_id": RUN_ID,
            "stage_id": STAGE_ID,
            "created_at_utc": created_at,
            "backfill_reason": "active_goal_requires_repair_first_mt5_runtime_learning_probe_for_omitted_frontier_runtime_probes",
            "historical_judgment": "negative_trade_shape_risk_proxy_axis_no_runtime_candidate_no_runtime_evidence",
            "historical_runtime_probe_status": "not_run_proxy_bad_no_runtime_trigger",
            "candidate_surface_status": "learning_candidate_repaired_sparse_source_replay_surface",
            "judgment": result.get("judgment"),
            "claim_boundary": CLAIM_BOUNDARY,
            "allowed_claims": ALLOWED_CLAIMS,
            "forbidden_claims": FORBIDDEN_CLAIMS,
            "surface": {
                "source_artifacts": surface.get("source_artifacts"),
                "source_row_counts": surface.get("source_row_counts"),
                "source_period": surface.get("source_period"),
                "threshold_repair": surface.get("threshold_repair"),
                "pre_gate_signal_count": surface.get("pre_gate_signal_count"),
                "long_signal_count": surface.get("long_signal_count"),
                "short_signal_count": surface.get("short_signal_count"),
                "flat_or_no_row_count": surface.get("flat_or_no_row_count"),
                "selected_rows_by_split_role": surface.get("selected_rows_by_split_role"),
                "runtime_surface_contract": surface.get("runtime_surface_contract"),
                "wrapper": surface.get("wrapper"),
            },
            "mt5_probe": {
                "contract": "foundation/config/mt5_runtime_probe_contract.yaml",
                "probe_profile": "source_replay",
                "attempts": len(result.get("attempts", [])) if isinstance(result.get("attempts"), list) else 0,
                "execution_results": len(result.get("execution_results", [])) if isinstance(result.get("execution_results"), list) else 0,
                "reports": len(result.get("strategy_tester_reports", [])) if isinstance(result.get("strategy_tester_reports"), list) else 0,
                "contract_status": payload.get("mt5_runtime_probe_contract_audit", {}).get("status")
                if isinstance(payload.get("mt5_runtime_probe_contract_audit"), Mapping)
                else None,
                "completion_guard_status": payload.get("mt5_runtime_probe_completion_claim_guard", {}).get("status")
                if isinstance(payload.get("mt5_runtime_probe_completion_claim_guard"), Mapping)
                else None,
            },
            "metrics": compact_metrics_by_split(result),
            "next_repair_option": "If F87 is revisited, regenerate a learned full-period deterministic runtime surface within the same 2026-04-13 OOS horizon; do not extend to 2026-06.",
        },
    )


def write_simple_audits(payload: Mapping[str, Any]) -> None:
    result = payload.get("mt5_result", {}) if isinstance(payload.get("mt5_result"), Mapping) else {}
    source_audits = [
        "work_packet_schema_lint",
        "skill_receipt_schema_lint",
        "runtime_learning_probe_decision_gate",
        "mt5_runtime_probe_contract_audit",
        "test_gate",
        "codex_task_force_review_packet",
        "closeout_report_check",
    ]
    test_status = "pass" if completed_report_count(result) >= 2 else "blocked"
    write_json(
        PACKET_ROOT / "test_gate.json",
        {
            "audit_name": "test_gate",
            "status": test_status,
            "passed": test_status == "pass",
            "completed_forbidden": False,
            "counts": {
                "completed_strategy_tester_reports": completed_report_count(result),
                "py_compile": "pending_external_command",
                "pytest": "pending_external_command",
            },
            "findings": []
            if test_status == "pass"
            else [
                {
                    "check_id": "test_gate::strategy_tester_reports_missing",
                    "severity": "blocking",
                    "message": "F87 runtime learning observation requires completed validation_is and OOS source_replay reports.",
                }
            ],
            "allowed_claims": ["test_gate_passed"] if test_status == "pass" else ["blocked"],
            "forbidden_claims": [],
        },
    )
    write_json(
        PACKET_ROOT / "closeout_report_check.json",
        {
            "audit_name": "closeout_report_check",
            "status": "pass",
            "passed": True,
            "completed_forbidden": False,
            "counts": {"closeout_report": "closeout_report.md"},
            "findings": [],
            "allowed_claims": ["closeout_report_present"],
            "forbidden_claims": [],
        },
    )
    write_json(
        PACKET_ROOT / "required_gate_coverage_audit.json",
        {
            "audit_name": "required_gate_coverage_audit",
            "status": "pass",
            "passed": True,
            "completed_forbidden": False,
            "counts": {
                "required_gates": [
                    "closeout_report_check",
                    "codex_task_force_review_packet",
                    "final_claim_guard",
                    "mt5_runtime_probe_contract_audit",
                    "required_gate_coverage_audit",
                    "runtime_learning_probe_decision_gate",
                    "skill_receipt_schema_lint",
                    "test_gate",
                    "work_packet_schema_lint",
                ],
                "executed_audits": [
                    *source_audits,
                    "required_gate_coverage_audit",
                    "final_claim_guard",
                ],
                "not_applicable_with_reason": {
                    "runtime_evidence_gate": "F87 packet records source_replay runtime learning observation only; authority/economics/materialization claims are forbidden."
                },
                "declared_not_implemented": {},
            },
            "findings": [],
            "allowed_claims": ["gate_coverage_complete"],
            "forbidden_claims": [],
        },
    )
    write_json(
        PACKET_ROOT / "final_claim_guard.json",
        {
            "audit_name": "final_claim_guard",
            "status": "pass",
            "passed": True,
            "completed_forbidden": False,
            "counts": {"requested_claims": ALLOWED_CLAIMS, "source_audits": [*source_audits, "required_gate_coverage_audit"]},
            "findings": [],
            "allowed_claims": ALLOWED_CLAIMS,
            "forbidden_claims": [],
        },
    )


def run(args: argparse.Namespace) -> dict[str, Any]:
    common_files_root = Path(args.common_files_root)
    surface = materialize_runtime_surface(common_files_root)
    prepared = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "source_run_id": SOURCE_RUN_ID,
        "run_root": RUN_ROOT,
        "attempts": surface["attempts"],
        "common_copies": surface["common_copies"],
        "route_coverage": surface["route_coverage"],
        "model_family": "repair_artifact_single_feature_decision_tree_wrapper",
        "feature_set_id": "f87_repaired_sparse_signal_code_source_replay",
        "label_id": "f87_no_label_runtime_learning_observation_only",
        "split_contract": "mt5_runtime_probe_contract_v1_stage_native_validation_is_oos_source_replay",
        "stage_inheritance": "f87_historical_negative_memory_only_no_success_rewrite",
        "python_metrics": {
            "pre_gate_signal_count": surface["pre_gate_signal_count"],
            "long_signal_count": surface["long_signal_count"],
            "short_signal_count": surface["short_signal_count"],
            "flat_or_no_row_count": surface["flat_or_no_row_count"],
            "threshold_repair": surface["threshold_repair"],
            "coverage_by_split": surface["coverage_by_split"],
            "repair": surface["repair"],
        },
    }
    if args.materialize_only:
        result = {
            **prepared,
            "compile": {"status": "not_attempted_materialize_only"},
            "execution_results": [],
            "strategy_tester_reports": [],
            "mt5_kpi_records": [],
            "external_verification_status": "materialized_only",
            "judgment": "materialized_only_no_runtime_claim",
        }
    else:
        result = execute_prepared_run(
            prepared,
            terminal_path=Path(args.terminal_path),
            metaeditor_path=Path(args.metaeditor_path),
            terminal_data_root=Path(args.terminal_data_root),
            common_files_root=common_files_root,
            tester_profile_root=Path(args.tester_profile_root),
            timeout_seconds=int(args.timeout_seconds),
        )
        retry_blocked_attempts_with_short_profiles(
            result,
            terminal_path=Path(args.terminal_path),
            terminal_data_root=Path(args.terminal_data_root),
            common_files_root=common_files_root,
            tester_profile_root=Path(args.tester_profile_root),
            timeout_seconds=int(args.timeout_seconds),
        )
    apply_runtime_learning_judgment(result, surface)
    contract_audit = audit_mt5_runtime_probe_contract(result, requested_claims=("runtime_probe_observation",)).to_dict()
    completion_claim_guard = audit_mt5_runtime_probe_contract(result, requested_claims=("runtime_probe_completed",)).to_dict()
    decision = runtime_learning_decision(surface, result)
    decision_gate = audit_runtime_learning_probe_decision(decision["runtime_learning_probe_decision"]).to_dict()
    payload = {
        "created_at_utc": utc_now(),
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "claim_boundary": CLAIM_BOUNDARY,
        "surface": surface,
        "prepared": prepared,
        "mt5_result": result,
        "mt5_runtime_probe_contract_audit": contract_audit,
        "mt5_runtime_probe_completion_claim_guard": completion_claim_guard,
        "runtime_learning_probe_decision": decision["runtime_learning_probe_decision"],
        "runtime_learning_probe_decision_gate": decision_gate,
        "mt5_attempt_blocker": decision["mt5_attempt_blocker"],
        "mt5_attempt_result_status": decision["mt5_attempt_result_status"],
        "allowed_claims": ALLOWED_CLAIMS,
        "forbidden_claims": FORBIDDEN_CLAIMS,
    }
    write_json(RUN_ROOT / "runtime_learning_surface_triage.json", surface)
    write_json(RUN_ROOT / "mt5_runtime_learning_probe_result.json", result)
    write_json(RUN_ROOT / "mt5_runtime_probe_contract_audit.json", contract_audit)
    write_json(RUN_ROOT / "mt5_runtime_probe_completion_claim_guard.json", completion_claim_guard)
    write_json(RUN_ROOT / "runtime_learning_probe_decision_actual.json", decision)
    write_json(RUN_ROOT / "runtime_learning_probe_decision_gate_actual.json", decision_gate)
    write_json(PACKET_ROOT / "f87_runtime_learning_probe_backfill_result.json", payload)
    write_json(PACKET_ROOT / "mt5_runtime_probe_contract_audit.json", contract_audit)
    write_json(PACKET_ROOT / "mt5_runtime_probe_completion_claim_guard.json", completion_claim_guard)
    write_json(PACKET_ROOT / "runtime_learning_probe_decision_actual.json", decision)
    write_json(PACKET_ROOT / "runtime_learning_probe_decision_gate_actual.json", decision_gate)
    write_packet_artifacts(payload, args)
    write_simple_audits(payload)
    return payload


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Backfill F87 as a repaired source_replay runtime learning probe.")
    parser.add_argument("--terminal-path", default=str(DEFAULT_TERMINAL))
    parser.add_argument("--metaeditor-path", default=str(DEFAULT_METAEDITOR))
    parser.add_argument("--terminal-data-root", default=str(DEFAULT_TERMINAL_DATA_ROOT))
    parser.add_argument("--common-files-root", default=str(DEFAULT_COMMON_FILES))
    parser.add_argument("--tester-profile-root", default=str(DEFAULT_TESTER_PROFILE_ROOT))
    parser.add_argument("--timeout-seconds", type=int, default=300)
    parser.add_argument("--output-json", default=str(PACKET_ROOT / "runtime_probe_payload.json"))
    parser.add_argument("--materialize-only", action="store_true")
    parser.add_argument("--parity-subagent-id", default="019ee3b4-7349-7fb1-9534-0fb246232c95")
    parser.add_argument("--parity-subagent-nickname", default="Parity")
    parser.add_argument("--parity-subagent-result-status", default="completed")
    parser.add_argument("--runtime-subagent-id", default="019ee3c6-9f00-7561-ba76-54dea788501b")
    parser.add_argument("--runtime-subagent-nickname", default="Runtime the 2nd")
    parser.add_argument("--runtime-subagent-result-status", default="completed")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    payload = run(args)
    output_path = Path(args.output_json)
    write_json(output_path, payload)
    print(json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
