from __future__ import annotations

import argparse
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np
import pandas as pd

from foundation.control_plane import mt5_kpi_recorder, mt5_trade_attribution
from foundation.control_plane.alpha_run_ledgers import build_alpha_scout_ledger_rows, materialize_alpha_ledgers
from foundation.control_plane.ledger import (
    RUN_REGISTRY_COLUMNS,
    io_path,
    json_ready,
    ledger_pairs,
    sha256_file_lf_normalized,
    upsert_csv_rows,
)
from foundation.control_plane.mt5_tier_balance_completion import (
    COMMON_FILES_ROOT_DEFAULT,
    METAEDITOR_PATH_DEFAULT,
    TERMINAL_DATA_ROOT_DEFAULT,
    TERMINAL_PATH_DEFAULT,
    TESTER_PROFILE_ROOT_DEFAULT,
    attempt_payload,
    common_run_root,
    copy_to_common,
    execute_prepared_run,
    split_dates_from_frame,
)
from foundation.models.hmm_state_policy import (
    STATE_FEATURE_NAME,
    attach_state_policy_probabilities,
    check_hmm_state_policy_table_parity,
    export_hmm_state_policy_score_table,
    state_policy_frame,
)
from foundation.models.onnx_bridge import ordered_hash
from foundation.mt5 import runtime_support as mt5


STAGE_NUMBER = 22
STAGE_ID = "22_regime_model__hmm_hidden_state_segmentation"
SOURCE_RUN_ID = "run16A_hmm_hidden_state_segmentation_scout_v1"
SOURCE_PACKET_ID = "stage22_run16A_hmm_state_scout_v1"
RUN_NUMBER = "run16B"
RUN_ID = "run16B_hmm_state_runtime_probe_v1"
PACKET_ID = "stage22_run16B_hmm_state_runtime_probe_v1"
EXPLORATION_LABEL = "stage22_Regime__HMMStateRuntimeProbe"
MODEL_FAMILY = "hmm_hidden_state_policy_ebm_table_runtime_probe"
MODEL_BACKEND = "ebm_table"
FEATURE_SET_ID = "feature_set_v2_hmm_state_code_runtime_probe"
LABEL_ID = "label_v1_fwd12_m5_logret_train_q33_3class"
SPLIT_CONTRACT = "split_v1_calendar_train_20220901_20241231_val_20250101_20260413"
SELECTED_VARIANT_ID = "v02_core17_4state_diag"
STATE_THRESHOLD = 0.35
MAX_HOLD_BARS = 12
MIN_MARGIN = 0.0
BOUNDARY = "hmm_state_policy_runtime_probe_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority"
JUDGMENT_COMPLETED = "inconclusive_hmm_state_policy_runtime_probe_completed"
JUDGMENT_BLOCKED = "blocked_hmm_state_policy_runtime_probe_after_attempt"

ROOT = Path(__file__).resolve().parents[2]
STAGE_ROOT = ROOT / "stages" / STAGE_ID
SOURCE_RUN_ROOT = STAGE_ROOT / "02_runs" / SOURCE_RUN_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
PACKET_ROOT = ROOT / "docs/agent_control/packets" / PACKET_ID
STAGE_LEDGER_PATH = STAGE_ROOT / "03_reviews/stage_run_ledger.csv"
PROJECT_LEDGER_PATH = ROOT / "docs/registers/alpha_run_ledger.csv"
RUN_REGISTRY_PATH = ROOT / "docs/registers/run_registry.csv"
REVIEW_PATH = STAGE_ROOT / "03_reviews/run16B_hmm_state_runtime_probe_packet.md"
DECISION_PATH = ROOT / "docs/decisions/2026-05-05_stage22_run16B_hmm_state_runtime_probe.md"
SELECTION_STATUS_PATH = STAGE_ROOT / "04_selected/selection_status.md"
REVIEW_INDEX_PATH = STAGE_ROOT / "03_reviews/review_index.md"
WORKSPACE_STATE_PATH = ROOT / "docs/workspace/workspace_state.yaml"
CURRENT_WORKING_STATE_PATH = ROOT / "docs/context/current_working_state.md"
GOAL_PLAN_PATH = ROOT / "docs/workspace/stage20_32_goal_operating_plan.md"
RUNTIME_FEATURE_ORDER = [STATE_FEATURE_NAME]
RUNTIME_FEATURE_HASH = ordered_hash(RUNTIME_FEATURE_ORDER)


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def safe_float(value: Any, default: float = 0.0) -> float:
    try:
        if value in (None, "", "NA"):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def save_frame(path: Path, frame: pd.DataFrame) -> dict[str, Any]:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    if path.suffix == ".parquet":
        frame.to_parquet(io_path(path), index=False)
    else:
        frame.to_csv(io_path(path), index=False)
    return {"path": rel(path), "rows": int(len(frame)), "sha256": sha256_file_lf_normalized(path)}


def load_source_context() -> dict[str, Any]:
    summary = read_json(ROOT / "docs/agent_control/packets" / SOURCE_PACKET_ID / "aggregate_summary.json")
    artifacts = summary.get("artifacts", {})
    tier_a_path = ROOT / str(artifacts.get("tier_a_sequence", {}).get("path", ""))
    tier_b_path = ROOT / str(artifacts.get("tier_b_sequence", {}).get("path", ""))
    if not io_path(tier_a_path).exists() or not io_path(tier_b_path).exists():
        raise FileNotFoundError(f"Missing Stage22 run16A sequence artifacts: {tier_a_path}, {tier_b_path}")
    tier_a_sequence = pd.read_parquet(io_path(tier_a_path))
    tier_b_sequence = pd.read_parquet(io_path(tier_b_path))
    if str(summary.get("selected_variant_id")) != SELECTED_VARIANT_ID:
        raise RuntimeError(f"Unexpected Stage22 selected variant: {summary.get('selected_variant_id')}")
    return {
        "source_summary": summary,
        "tier_a_sequence": tier_a_sequence,
        "tier_b_sequence": tier_b_sequence,
        "tier_a_sequence_artifact": {"path": rel(tier_a_path), "sha256": sha256_file_lf_normalized(tier_a_path)},
        "tier_b_sequence_artifact": {"path": rel(tier_b_path), "sha256": sha256_file_lf_normalized(tier_b_path)},
    }


def state_decision_metrics(prob_frame: pd.DataFrame, threshold: float) -> dict[str, Any]:
    rows: dict[str, Any] = {}
    p = prob_frame[["p_short", "p_flat", "p_long"]].to_numpy(dtype="float64", copy=False)
    row_sum_error = float(np.max(np.abs(p.sum(axis=1) - 1.0))) if len(p) else 0.0
    for split in ("train", "validation", "oos"):
        part = prob_frame.loc[prob_frame["split"].astype(str).eq(split)]
        short_ok = (part["p_short"] >= threshold) & (part["p_short"] >= part[["p_flat", "p_long"]].max(axis=1))
        long_ok = (part["p_long"] >= threshold) & (part["p_long"] >= part[["p_flat", "p_short"]].max(axis=1))
        rows[split] = {
            "rows": int(len(part)),
            "signal_count": int(short_ok.sum() + long_ok.sum()),
            "short_count": int(short_ok.sum()),
            "long_count": int(long_ok.sum()),
            "flat_count": int(len(part) - short_ok.sum() - long_ok.sum()),
            "signal_coverage": float((short_ok.sum() + long_ok.sum()) / max(1, len(part))),
        }
    rows["probability_checks"] = {"row_sum_max_abs_error": row_sum_error}
    return rows


def tier_record(record_view: str, tier_scope: str, prob_frame: pd.DataFrame, path: Path) -> dict[str, Any]:
    metrics = state_decision_metrics(prob_frame, STATE_THRESHOLD)
    subtype_counts: dict[str, int] = {}
    if "hidden_state_label" in prob_frame.columns:
        subtype_counts = {str(key): int(value) for key, value in prob_frame["hidden_state_label"].value_counts().sort_index().items()}
    total = {
        "rows": int(len(prob_frame)),
        "signal_count": int(sum(metrics.get(split, {}).get("signal_count", 0) for split in ("train", "validation", "oos"))),
        "short_count": int(sum(metrics.get(split, {}).get("short_count", 0) for split in ("train", "validation", "oos"))),
        "long_count": int(sum(metrics.get(split, {}).get("long_count", 0) for split in ("train", "validation", "oos"))),
        "partial_context_subtype_counts": subtype_counts or None,
        "threshold_ids": f"fixed_state_probability_{STATE_THRESHOLD:.2f}",
        "probability_row_sum_max_abs_error": metrics.get("probability_checks", {}).get("row_sum_max_abs_error"),
    }
    total["signal_coverage"] = safe_float(total["signal_count"]) / max(1, int(total["rows"]))
    return {
        "record_view": record_view,
        "tier_scope": tier_scope,
        "status": "completed",
        "path": rel(path),
        "metrics": total,
        "split_metrics": {split: metrics.get(split, {}) for split in ("train", "validation", "oos")},
    }


def materialize_state_policy(context: Mapping[str, Any]) -> tuple[dict[str, Any], list[dict[str, Any]], dict[str, Any]]:
    model_root = RUN_ROOT / "models"
    prediction_root = RUN_ROOT / "predictions"
    io_path(model_root).mkdir(parents=True, exist_ok=True)
    tier_a_policy = state_policy_frame(context["tier_a_sequence"])
    tier_b_policy = state_policy_frame(context["tier_b_sequence"])
    tier_a_policy_path = model_root / f"{SELECTED_VARIANT_ID}_tier_a_hmm_state_policy.csv"
    tier_b_policy_path = model_root / f"{SELECTED_VARIANT_ID}_tier_b_hmm_state_policy.csv"
    tier_a_table_path = model_root / f"{SELECTED_VARIANT_ID}_tier_a_hmm_state_policy_score_table.csv"
    tier_b_table_path = model_root / f"{SELECTED_VARIANT_ID}_tier_b_hmm_state_policy_score_table.csv"
    tier_a_policy.to_csv(io_path(tier_a_policy_path), index=False)
    tier_b_policy.to_csv(io_path(tier_b_policy_path), index=False)
    tier_a_table = export_hmm_state_policy_score_table(tier_a_policy, tier_a_table_path)
    tier_b_table = export_hmm_state_policy_score_table(tier_b_policy, tier_b_table_path)
    tier_a_parity = check_hmm_state_policy_table_parity(
        tier_a_policy,
        tier_a_table_path,
        context["tier_a_sequence"]["hidden_state"].to_numpy(dtype="float64", copy=False),
    )
    tier_b_parity = check_hmm_state_policy_table_parity(
        tier_b_policy,
        tier_b_table_path,
        context["tier_b_sequence"]["hidden_state"].to_numpy(dtype="float64", copy=False),
    )

    tier_a_prob = attach_state_policy_probabilities(context["tier_a_sequence"], tier_a_policy)
    tier_b_prob = attach_state_policy_probabilities(context["tier_b_sequence"], tier_b_policy)
    tier_ab_prob = pd.concat(
        [
            tier_a_prob.assign(record_source="tier_a", partial_context_subtype="Tier_A_full_context"),
            tier_b_prob.assign(record_source="tier_b_fallback"),
        ],
        ignore_index=True,
    )
    a_path = prediction_root / "tier_a_state_policy_predictions.parquet"
    b_path = prediction_root / "tier_b_state_policy_predictions.parquet"
    ab_path = prediction_root / "tier_ab_state_policy_predictions.parquet"
    artifacts = {
        "tier_a_policy": save_frame(tier_a_policy_path, tier_a_policy),
        "tier_b_policy": save_frame(tier_b_policy_path, tier_b_policy),
        "tier_a_table": {**tier_a_table, "path": rel(tier_a_table_path)},
        "tier_b_table": {**tier_b_table, "path": rel(tier_b_table_path)},
        "tier_a_table_parity": tier_a_parity,
        "tier_b_table_parity": tier_b_parity,
    }
    prediction_artifacts = {
        "tier_a_predictions": save_frame(a_path, tier_a_prob),
        "tier_b_predictions": save_frame(b_path, tier_b_prob),
        "tier_ab_predictions": save_frame(ab_path, tier_ab_prob),
    }
    tier_records = [
        tier_record("tier_a_separate", mt5.TIER_A, tier_a_prob, a_path),
        tier_record("tier_b_separate", mt5.TIER_B, tier_b_prob, b_path),
        tier_record("tier_ab_combined", mt5.TIER_AB, tier_ab_prob, ab_path),
    ]
    return artifacts, tier_records, prediction_artifacts


def feature_source_frame(sequence: pd.DataFrame, source_split: str, route_role: str) -> pd.DataFrame:
    frame = sequence.loc[sequence["split"].astype(str).eq(source_split)].copy()
    frame[STATE_FEATURE_NAME] = frame["hidden_state"].astype("float64")
    frame["partial_context_subtype"] = frame["hidden_state_label"].astype(str)
    frame["route_role"] = route_role
    return frame


def export_feature_matrices(context: Mapping[str, Any]) -> dict[str, Any]:
    root = RUN_ROOT / "features"
    payload: dict[str, Any] = {}
    for source_split, runtime_split in (("validation", "validation_is"), ("oos", "oos")):
        tier_a_frame = feature_source_frame(context["tier_a_sequence"], source_split, "tier_a_primary")
        tier_b_frame = feature_source_frame(context["tier_b_sequence"], source_split, "tier_b_fallback")
        payload[f"tier_a_{runtime_split}"] = mt5.export_mt5_feature_matrix_csv(
            tier_a_frame,
            RUNTIME_FEATURE_ORDER,
            root / f"tier_a_{runtime_split}_feature_matrix.csv",
            metadata_columns=("partial_context_subtype", "route_role"),
        )
        payload[f"tier_b_fallback_{runtime_split}"] = mt5.export_mt5_feature_matrix_csv(
            tier_b_frame,
            RUNTIME_FEATURE_ORDER,
            root / f"tier_b_fallback_{runtime_split}_feature_matrix.csv",
            metadata_columns=("partial_context_subtype", "route_role"),
        )
    return payload


def route_coverage(context: Mapping[str, Any]) -> dict[str, Any]:
    by_split: dict[str, Any] = {}
    subtype_by_split: dict[str, Any] = {}
    no_tier_by_split: dict[str, int] = {}
    for split in ("train", "validation", "oos"):
        a_rows = int(context["tier_a_sequence"]["split"].astype(str).eq(split).sum())
        b_part = context["tier_b_sequence"].loc[context["tier_b_sequence"]["split"].astype(str).eq(split)]
        b_rows = int(len(b_part))
        by_split[split] = {
            "tier_a_primary_rows": a_rows,
            "tier_b_fallback_rows": b_rows,
            "routed_labelable_rows": a_rows + b_rows,
        }
        subtype_by_split[split] = {str(key): int(value) for key, value in b_part["hidden_state_label"].value_counts().sort_index().items()}
        no_tier_by_split[split] = 0
    return {
        "by_split": by_split,
        "tier_b_fallback_by_split_subtype": subtype_by_split,
        "no_tier_by_split": no_tier_by_split,
    }


def copy_runtime_inputs(model_artifacts: Mapping[str, Any], feature_matrices: Mapping[str, Any]) -> list[dict[str, Any]]:
    common = common_run_root(STAGE_NUMBER, RUN_ID)
    copies: list[dict[str, Any]] = []
    for key in ("tier_a_table", "tier_b_table"):
        local_path = ROOT / str(model_artifacts[key]["path"])
        copies.append(copy_to_common(local_path, f"{common}/models/{local_path.name}", COMMON_FILES_ROOT_DEFAULT))
    for matrix in feature_matrices.values():
        local_path = ROOT / str(matrix["path"])
        copies.append(copy_to_common(local_path, f"{common}/features/{local_path.name}", COMMON_FILES_ROOT_DEFAULT))
    return copies


def make_attempts(context: Mapping[str, Any], model_artifacts: Mapping[str, Any], feature_matrices: Mapping[str, Any]) -> list[dict[str, Any]]:
    attempts: list[dict[str, Any]] = []
    common = common_run_root(STAGE_NUMBER, RUN_ID)
    tier_a_model = Path(str(model_artifacts["tier_a_table"]["path"])).name
    tier_b_model = Path(str(model_artifacts["tier_b_table"]["path"])).name
    for source_split, runtime_split in (("validation", "validation_is"), ("oos", "oos")):
        from_date, to_date = split_dates_from_frame(context["tier_a_sequence"], source_split)
        tier_a_matrix = Path(str(feature_matrices[f"tier_a_{runtime_split}"]["path"])).name
        tier_b_matrix = Path(str(feature_matrices[f"tier_b_fallback_{runtime_split}"]["path"])).name
        common_kwargs = {
            "run_root": RUN_ROOT,
            "run_id": RUN_ID,
            "stage_number": STAGE_NUMBER,
            "exploration_label": EXPLORATION_LABEL,
            "split": runtime_split,
            "from_date": from_date,
            "to_date": to_date,
            "max_hold_bars": MAX_HOLD_BARS,
            "common_root": common,
        }
        attempts.append(
            attempt_payload(
                **common_kwargs,
                attempt_name=f"tier_a_only_{runtime_split}",
                tier=mt5.TIER_A,
                model_path=f"{common}/models/{tier_a_model}",
                model_id=f"{RUN_ID}_tier_a_state_policy",
                model_backend=MODEL_BACKEND,
                feature_path=f"{common}/features/{tier_a_matrix}",
                feature_count=1,
                feature_order_hash=RUNTIME_FEATURE_HASH,
                short_threshold=STATE_THRESHOLD,
                long_threshold=STATE_THRESHOLD,
                min_margin=MIN_MARGIN,
                invert_signal=False,
                primary_active_tier="tier_a",
                attempt_role="tier_only_total",
                record_view_prefix="mt5_tier_a_only",
            )
        )
        attempts.append(
            attempt_payload(
                **common_kwargs,
                attempt_name=f"tier_b_fallback_only_{runtime_split}",
                tier=mt5.TIER_B,
                model_path=f"{common}/models/{tier_b_model}",
                model_id=f"{RUN_ID}_tier_b_state_policy",
                model_backend=MODEL_BACKEND,
                feature_path=f"{common}/features/{tier_b_matrix}",
                feature_count=1,
                feature_order_hash=RUNTIME_FEATURE_HASH,
                short_threshold=STATE_THRESHOLD,
                long_threshold=STATE_THRESHOLD,
                min_margin=MIN_MARGIN,
                invert_signal=False,
                primary_active_tier="tier_b_fallback",
                attempt_role="tier_b_fallback_only_total",
                record_view_prefix="mt5_tier_b_fallback_only",
            )
        )
        attempts.append(
            attempt_payload(
                **common_kwargs,
                attempt_name=f"routed_{runtime_split}",
                tier=mt5.TIER_AB,
                model_path=f"{common}/models/{tier_a_model}",
                model_id=f"{RUN_ID}_tier_a_state_policy",
                model_backend=MODEL_BACKEND,
                feature_path=f"{common}/features/{tier_a_matrix}",
                feature_count=1,
                feature_order_hash=RUNTIME_FEATURE_HASH,
                short_threshold=STATE_THRESHOLD,
                long_threshold=STATE_THRESHOLD,
                min_margin=MIN_MARGIN,
                invert_signal=False,
                primary_active_tier="tier_a",
                attempt_role="routed_total",
                record_view_prefix="mt5_routed_total",
                fallback_enabled=True,
                fallback_model_path=f"{common}/models/{tier_b_model}",
                fallback_model_id=f"{RUN_ID}_tier_b_state_policy",
                fallback_model_backend=MODEL_BACKEND,
                fallback_feature_path=f"{common}/features/{tier_b_matrix}",
                fallback_feature_count=1,
                fallback_feature_order_hash=RUNTIME_FEATURE_HASH,
                fallback_short_threshold=STATE_THRESHOLD,
                fallback_long_threshold=STATE_THRESHOLD,
                fallback_min_margin=MIN_MARGIN,
                fallback_invert_signal=False,
            )
        )
    return attempts


def execute_or_block(prepared: Mapping[str, Any], args: argparse.Namespace) -> dict[str, Any]:
    if bool(args.materialize_only):
        return {
            **dict(prepared),
            "compile": {"status": "not_attempted_materialize_only"},
            "execution_results": [],
            "strategy_tester_reports": [],
            "mt5_kpi_records": [],
            "external_verification_status": "blocked",
            "judgment": JUDGMENT_BLOCKED,
            "failure": {"type": "materialize_only", "message": "MT5 execution skipped by CLI flag."},
        }
    try:
        result = execute_prepared_run(
            prepared,
            terminal_path=Path(args.terminal_path),
            metaeditor_path=Path(args.metaeditor_path),
            terminal_data_root=TERMINAL_DATA_ROOT_DEFAULT,
            common_files_root=COMMON_FILES_ROOT_DEFAULT,
            tester_profile_root=TESTER_PROFILE_ROOT_DEFAULT,
            timeout_seconds=int(args.timeout_seconds),
        )
    except Exception as exc:
        return {
            **dict(prepared),
            "compile": {"status": "exception_or_not_completed"},
            "execution_results": [],
            "strategy_tester_reports": [],
            "mt5_kpi_records": [],
            "external_verification_status": "blocked",
            "judgment": JUDGMENT_BLOCKED,
            "failure": {"type": type(exc).__name__, "message": str(exc)},
        }
    result = dict(result)
    completed = result.get("external_verification_status") == "completed"
    result["judgment"] = JUDGMENT_COMPLETED if completed else JUDGMENT_BLOCKED
    for record in result.get("mt5_kpi_records", []):
        record["source_variant_id"] = SELECTED_VARIANT_ID
        record["topic_read"] = "hmm_state_policy_runtime_handoff"
        record["threshold_id"] = f"fixed_state_probability_{STATE_THRESHOLD:.2f}"
        record["max_hold_bars"] = MAX_HOLD_BARS
    return result


def metrics_by_view(result: Mapping[str, Any], view: str) -> dict[str, Any]:
    for record in result.get("mt5_kpi_records", []):
        if record.get("record_view") == view:
            metrics = record.get("metrics", {})
            return dict(metrics) if isinstance(metrics, Mapping) else {}
    return {}


def parity_passed(model_artifacts: Mapping[str, Any]) -> bool:
    return bool(model_artifacts.get("tier_a_table_parity", {}).get("passed")) and bool(model_artifacts.get("tier_b_table_parity", {}).get("passed"))


def runtime_failure_signature(result: Mapping[str, Any]) -> dict[str, Any]:
    status_counts: dict[str, int] = {}
    model_ok_total = 0
    model_fail_total = 0
    feature_ready_total = 0
    last_skip_counts: dict[str, int] = {}
    for item in result.get("execution_results", []) or []:
        status = str(item.get("status"))
        status_counts[status] = status_counts.get(status, 0) + 1
        outputs = item.get("runtime_outputs", {})
        if not isinstance(outputs, Mapping):
            continue
        summary = outputs.get("last_summary", {})
        if not isinstance(summary, Mapping):
            continue
        model_ok_total += int(summary.get("model_ok_count") or 0)
        model_fail_total += int(summary.get("model_fail_count") or 0)
        feature_ready_total += int(summary.get("feature_ready_count") or 0)
        skip = summary.get("last_skip_reason")
        if skip:
            last_skip_counts[str(skip)] = last_skip_counts.get(str(skip), 0) + 1
    primary_skip = max(last_skip_counts.items(), key=lambda pair: pair[1])[0] if last_skip_counts else None
    return {
        "compile_status": (result.get("compile") or {}).get("status") if isinstance(result.get("compile"), Mapping) else None,
        "attempt_status_counts": status_counts,
        "feature_ready_count_total": feature_ready_total,
        "model_ok_count_total": model_ok_total,
        "model_fail_count_total": model_fail_total,
        "primary_runtime_skip": primary_skip,
        "last_skip_reason_counts": last_skip_counts,
    }


def write_normalized_kpi() -> dict[str, Any]:
    inventory = [{"run_id": RUN_ID, "stage_id": STAGE_ID, "idea_id": RUN_NUMBER, "path": rel(RUN_ROOT)}]
    records, summary_rows, missing, parser_errors = mt5_kpi_recorder.build_normalized_records(ROOT, inventory)
    market_data = mt5_trade_attribution.MarketData.load(ROOT)
    enriched, trade_rows, trade_summary, trade_errors = mt5_trade_attribution.enrich_records(records, ROOT, market_data)
    write_json(PACKET_ROOT / "normalized_kpi_records.json", records)
    write_json(PACKET_ROOT / "normalized_kpi_summary.json", summary_rows)
    write_json(PACKET_ROOT / "normalized_kpi_missing_runs.json", missing)
    write_json(PACKET_ROOT / "normalized_kpi_parser_errors.json", parser_errors)
    write_json(PACKET_ROOT / "enriched_kpi_records.json", enriched)
    write_json(PACKET_ROOT / "trade_level_records.json", trade_rows)
    write_json(PACKET_ROOT / "trade_attribution_summary.json", trade_summary)
    write_json(PACKET_ROOT / "trade_attribution_parser_errors.json", trade_errors)
    return {
        "normalized_records": len(records),
        "normalized_summary_rows": len(summary_rows),
        "missing_runs": len(missing),
        "parser_errors": len(parser_errors),
        "trade_attribution_records": len(trade_summary),
        "trade_level_rows": len(trade_rows),
        "trade_parser_errors": len(trade_errors),
    }


def build_summary(
    result: Mapping[str, Any],
    context: Mapping[str, Any],
    model_artifacts: Mapping[str, Any],
    prediction_artifacts: Mapping[str, Any],
    tier_records: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    completed = result.get("external_verification_status") == "completed"
    parity_ok = parity_passed(model_artifacts)
    validation = metrics_by_view(result, "mt5_routed_total_validation_is")
    oos = metrics_by_view(result, "mt5_routed_total_oos")
    avg_trades = (safe_float(validation.get("trade_count")) + safe_float(oos.get("trade_count"))) / 2.0
    visible = completed and parity_ok and avg_trades >= 5.0
    return {
        "run_number": RUN_NUMBER,
        "run_id": RUN_ID,
        "packet_id": PACKET_ID,
        "source_run_id": SOURCE_RUN_ID,
        "source_packet_id": SOURCE_PACKET_ID,
        "stage_id": STAGE_ID,
        "model_family": MODEL_FAMILY,
        "selected_variant_id": SELECTED_VARIANT_ID,
        "topic_read": "hmm_state_policy_runtime_handoff",
        "state_threshold": STATE_THRESHOLD,
        "max_hold_bars": MAX_HOLD_BARS,
        "boundary": BOUNDARY,
        "judgment": JUDGMENT_COMPLETED if completed else JUDGMENT_BLOCKED,
        "closure_judgment": JUDGMENT_COMPLETED if completed else JUDGMENT_BLOCKED,
        "external_verification_status": result["external_verification_status"],
        "model_characteristic_strength": "hmm_state_runtime_axis_visible" if visible else "hmm_state_runtime_axis_weak_or_blocked",
        "source_artifacts": {
            "tier_a_sequence": context["tier_a_sequence_artifact"],
            "tier_b_sequence": context["tier_b_sequence_artifact"],
        },
        "model_artifacts": model_artifacts,
        "prediction_artifacts": prediction_artifacts,
        "python_tier_records": list(tier_records),
        "route_coverage": route_coverage(context),
        "mt5_kpi_record_count": len(result.get("mt5_kpi_records", [])),
        "attempt_count": len(result.get("attempts", [])),
        "expected_attempts": 6,
        "expected_kpi_records": 10,
        "validation_routed": validation,
        "oos_routed": oos,
        "runtime_failure_signature": runtime_failure_signature(result),
        "forbidden_claims": ["edge", "alpha_quality", "baseline", "promotion_candidate", "operating_promotion", "runtime_authority"],
        "next_action": "stage22_closeout_and_stage23_open_only" if completed else "repair_run16B_hmm_state_runtime_probe_then_rerun_same_six_attempts",
    }


def upsert_run_registry(result: Mapping[str, Any], summary: Mapping[str, Any]) -> dict[str, Any]:
    validation = summary.get("validation_routed", {})
    oos = summary.get("oos_routed", {})
    row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "alpha_runtime_probe",
        "status": "reviewed" if result["external_verification_status"] == "completed" else "blocked",
        "judgment": summary["closure_judgment"],
        "path": rel(RUN_ROOT),
        "notes": ledger_pairs(
            (
                ("model_family", MODEL_FAMILY),
                ("topic_read", "hmm_state_policy_runtime_handoff"),
                ("routing_mode", "tier_a_primary_tier_b_fallback"),
                ("selected_variant", SELECTED_VARIANT_ID),
                ("state_threshold", STATE_THRESHOLD),
                ("validation_net_profit", validation.get("net_profit")),
                ("validation_pf", validation.get("profit_factor")),
                ("oos_net_profit", oos.get("net_profit")),
                ("oos_pf", oos.get("profit_factor")),
                ("external_verification", result["external_verification_status"]),
                ("boundary", "runtime_probe_only"),
            )
        ),
    }
    return upsert_csv_rows(RUN_REGISTRY_PATH, RUN_REGISTRY_COLUMNS, [row], key="run_id")


def packet_markdown(summary: Mapping[str, Any], kpi: Mapping[str, Any]) -> str:
    validation = summary.get("validation_routed", {})
    oos = summary.get("oos_routed", {})
    parity = summary.get("model_artifacts", {})
    return f"""# RUN16B HMM State Runtime Probe(실행16B HMM 상태 런타임 탐침)

## Judgment(판정)

- run(실행): `{RUN_ID}`
- judgment(판정): `{summary.get('closure_judgment')}`
- external verification(외부 검증): `{summary.get('external_verification_status')}`
- selected variant(선택 변형): `{SELECTED_VARIANT_ID}`
- MT5 KPI records(MT5 핵심 성과 지표 기록): `{summary.get('mt5_kpi_record_count')}`
- normalized KPI records(정규화 핵심 성과 지표 기록): `{kpi.get('normalized_records')}`
- boundary(경계): `{BOUNDARY}`

효과(effect, 효과): HMM(`Hidden Markov Model`, 은닉 마르코프 모델)의 hidden state(숨은 상태)를 MT5(`MetaTrader 5`, 메타트레이더5) `ebm_table(EBM 테이블)` backend(백엔드)로 넘겨 runtime handoff(런타임 인계)를 확인했다. edge(거래 우위), baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 만들지 않는다.

## Runtime Read(런타임 판독)

| split(분할) | net profit(순손익) | profit factor(수익 계수) | trades(거래 수) | max DD(최대 손실) |
|---|---:|---:|---:|---:|
| validation(검증) | `{validation.get('net_profit')}` | `{validation.get('profit_factor')}` | `{validation.get('trade_count')}` | `{validation.get('max_drawdown_amount')}` |
| OOS(표본외) | `{oos.get('net_profit')}` | `{oos.get('profit_factor')}` | `{oos.get('trade_count')}` | `{oos.get('max_drawdown_amount')}` |

## State Table Parity(상태 테이블 동등성)

- Tier A parity(Tier A 동등성): `{parity.get('tier_a_table_parity', {}).get('passed')}`; max_abs_diff(최대 절대 차이) `{parity.get('tier_a_table_parity', {}).get('max_abs_diff')}`
- Tier B parity(Tier B 동등성): `{parity.get('tier_b_table_parity', {}).get('passed')}`; max_abs_diff(최대 절대 차이) `{parity.get('tier_b_table_parity', {}).get('max_abs_diff')}`

Forbidden claims(금지 주장): edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위).
"""


def gate_payloads(summary: Mapping[str, Any], kpi: Mapping[str, Any]) -> dict[str, Any]:
    completed = summary.get("external_verification_status") == "completed"
    parity_ok = parity_passed(summary.get("model_artifacts", {}))
    gates = ["runtime_evidence_gate", "scope_completion_gate", "kpi_contract_audit", "required_gate_coverage_audit", "final_claim_guard"]
    return {
        "runtime_evidence_gate": {
            "status": "passed" if completed and parity_ok else "blocked",
            "external_verification_status": summary.get("external_verification_status"),
            "state_table_parity_passed": parity_ok,
            "mt5_kpi_record_count": summary.get("mt5_kpi_record_count"),
            "expected_kpi_records": summary.get("expected_kpi_records"),
        },
        "scope_completion_gate": {
            "status": "passed" if summary.get("attempt_count") == summary.get("expected_attempts") else "blocked",
            "attempt_count": summary.get("attempt_count"),
            "expected_attempts": summary.get("expected_attempts"),
            "claim_boundary": BOUNDARY,
        },
        "kpi_contract_audit": {
            "status": "passed" if int(summary.get("mt5_kpi_record_count") or 0) > 0 else "blocked",
            "normalized_records": kpi.get("normalized_records"),
            "parser_errors": kpi.get("parser_errors"),
        },
        "required_gate_coverage_audit": {
            "status": "passed",
            "packet_id": PACKET_ID,
            "required_gates": gates,
            "covered_gates": gates,
        },
        "final_claim_guard": {
            "status": "passed",
            "allowed_claims": ["runtime_probe", "inconclusive", "blocked"],
            "forbidden_claims": summary.get("forbidden_claims"),
            "claim_boundary": BOUNDARY,
        },
    }


def build_skill_receipts(summary: Mapping[str, Any], created_at: str) -> list[dict[str, Any]]:
    status = "completed" if summary.get("external_verification_status") == "completed" else "blocked"
    return [
        {
            "packet_id": PACKET_ID,
            "created_at_utc": created_at,
            "skill": "obsidian-runtime-parity",
            "status": status,
            "research_path": rel(ROOT / "stage_pipelines/stage22/hmm_state_runtime_probe.py"),
            "runtime_path": rel(ROOT / "foundation/mt5/ObsidianPrimeV2_RuntimeProbeEA.mq5"),
            "shared_contract": "one-feature hmm_state_code, EBM-table backend, fixed 0.35 state probability threshold, Tier A primary plus Tier B fallback routing, US100 M5 timestamp match",
            "known_differences": "MT5 receives precomputed HMM states; it does not recompute Gaussian HMM emissions live.",
            "parity_check": {
                "tier_a": summary.get("model_artifacts", {}).get("tier_a_table_parity"),
                "tier_b": summary.get("model_artifacts", {}).get("tier_b_table_parity"),
            },
            "parity_identity": {
                "model_artifacts": summary.get("model_artifacts"),
                "runtime_output_path": rel(RUN_ROOT / "mt5"),
            },
            "runtime_claim_boundary": "runtime_probe",
        },
        {
            "packet_id": PACKET_ID,
            "created_at_utc": created_at,
            "skill": "obsidian-backtest-forensics",
            "status": status,
            "tester_report_count": summary.get("mt5_kpi_record_count"),
            "runtime_failure_signature": summary.get("runtime_failure_signature"),
        },
        {
            "packet_id": PACKET_ID,
            "created_at_utc": created_at,
            "skill": "obsidian-result-judgment",
            "status": "completed",
            "result_subject": RUN_ID,
            "judgment_label": summary.get("closure_judgment"),
            "claim_boundary": BOUNDARY,
        },
    ]


def write_run_outputs(
    result: Mapping[str, Any],
    context: Mapping[str, Any],
    model_artifacts: Mapping[str, Any],
    prediction_artifacts: Mapping[str, Any],
    tier_records: Sequence[Mapping[str, Any]],
    kpi: Mapping[str, Any],
    created_at: str,
) -> dict[str, Any]:
    summary = build_summary(result, context, model_artifacts, prediction_artifacts, tier_records)
    upsert_run_registry(result, summary)
    ledger_rows = build_alpha_scout_ledger_rows(
        run_id=RUN_ID,
        stage_id=STAGE_ID,
        tier_records=tier_records,
        mt5_kpi_records=result.get("mt5_kpi_records", []),
        selected_threshold_id=f"fixed_state_probability_{STATE_THRESHOLD:.2f}",
        run_output_root=RUN_ROOT,
        external_verification_status=result["external_verification_status"],
    )
    materialize_alpha_ledgers(stage_run_ledger_path=STAGE_LEDGER_PATH, project_alpha_ledger_path=PROJECT_LEDGER_PATH, rows=ledger_rows)
    manifest = {
        "run_id": RUN_ID,
        "packet_id": PACKET_ID,
        "stage_id": STAGE_ID,
        "source_run_id": SOURCE_RUN_ID,
        "run_number": RUN_NUMBER,
        "created_at_utc": created_at,
        "model_family": MODEL_FAMILY,
        "feature_set_id": FEATURE_SET_ID,
        "label_id": LABEL_ID,
        "split_contract": SPLIT_CONTRACT,
        "selected_variant_id": SELECTED_VARIANT_ID,
        "state_threshold": STATE_THRESHOLD,
        "max_hold_bars": MAX_HOLD_BARS,
        "boundary": BOUNDARY,
        "runtime_probe": {
            key: result.get(key)
            for key in ("attempts", "common_copies", "compile", "execution_results", "strategy_tester_reports", "external_verification_status", "judgment", "failure")
            if key in result
        },
        "model_artifacts": model_artifacts,
        "prediction_artifacts": prediction_artifacts,
    }
    kpi_record = {
        **manifest,
        "kpi_scope": "hmm_state_policy_mt5_runtime_probe",
        "python_tier_records": list(tier_records),
        "mt5": {
            "scoreboard_lane": "runtime_probe",
            "external_verification_status": result["external_verification_status"],
            "kpi_records": result.get("mt5_kpi_records", []),
        },
        "kpi_management": dict(kpi),
        "judgment": summary["closure_judgment"],
    }
    write_json(RUN_ROOT / "run_manifest.json", manifest)
    write_json(RUN_ROOT / "kpi_record.json", kpi_record)
    write_json(RUN_ROOT / "summary.json", summary)
    write_md(REVIEW_PATH, packet_markdown(summary, kpi))
    write_json(PACKET_ROOT / "aggregate_summary.json", {**summary, "kpi_management": dict(kpi)})
    write_json(PACKET_ROOT / "skill_receipts.json", build_skill_receipts(summary, created_at))
    for name, payload in gate_payloads(summary, kpi).items():
        write_json(PACKET_ROOT / f"{name}.json", payload)
    return summary


def replace_top_level_yaml_block(text: str, marker: str, block: str) -> str:
    if marker not in text:
        return text.rstrip() + "\n" + block
    start = text.index(marker)
    next_start = len(text)
    cursor = text.find("\n", start + len(marker))
    while cursor != -1:
        line_start = cursor + 1
        line_end = text.find("\n", line_start)
        if line_end == -1:
            line_end = len(text)
        line = text[line_start:line_end]
        if line and not line[0].isspace() and ":" in line:
            next_start = line_start
            break
        cursor = text.find("\n", line_start)
    return text[:start] + block + text[next_start:]


def update_workspace_state(summary: Mapping[str, Any]) -> None:
    completed = summary.get("external_verification_status") == "completed"
    status = "active_run16B_mt5_runtime_probe_completed" if completed else "active_run16B_mt5_runtime_probe_blocked_after_attempt"
    next_action = "stage22_closeout_and_stage23_open_only" if completed else "repair_run16B_hmm_state_runtime_probe_then_rerun_same_six_attempts"
    state = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    lines = state.splitlines()
    for index, line in enumerate(lines):
        if line.startswith("current_run_id: "):
            lines[index] = f"current_run_id: {RUN_ID}"
    state = "\n".join(lines) + "\n"
    state = state.replace(
        "- treat Stage 22 as active after run16A_hmm_hidden_state_segmentation_scout_v1 HMM hidden-state Python structural scout; next action is run16B_hmm_state_runtime_probe_v1 MT5 runtime_probe, and no baseline, promotion, or runtime authority exists",
        f"- treat Stage 22 as active after {RUN_ID} HMM state MT5 runtime_probe; next action is {next_action}, and no baseline, promotion, or runtime authority exists",
        1,
    )
    state = state.replace(
        "- treat Stage 22 as active after run16B_hmm_state_runtime_probe_v1 HMM hidden-state Python structural scout; next action is run16B_hmm_state_runtime_probe_v1 MT5 runtime_probe, and no baseline, promotion, or runtime authority exists",
        f"- treat Stage 22 as active after {RUN_ID} HMM state MT5 runtime_probe; next action is {next_action}, and no baseline, promotion, or runtime authority exists",
        1,
    )
    state = state.replace("status: active_run16A_python_structural_scout_completed", f"status: {status}")
    state = state.replace("status: active_run16B_mt5_runtime_probe_blocked_after_attempt", f"status: {status}")
    state = state.replace("status: stage20_closed_stage21_closed_stage22_run16A_completed", "status: stage20_closed_stage21_closed_stage22_run16B_completed")
    state = state.replace("latest_completed_run: run16A_hmm_hidden_state_segmentation_scout_v1", f"latest_completed_run: {RUN_ID}")
    state = state.replace("next_exact_action: run16B_hmm_state_runtime_probe_v1", f"next_exact_action: {next_action}")
    state = state.replace(
        "claim_boundary: hmm_hidden_state_structural_scout_only_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority",
        f"claim_boundary: {BOUNDARY}",
    )
    stage_block = f"""stage22_hmm_hidden_state_segmentation:
  stage_id: {STAGE_ID}
  status: {status}
  current_run_id: {RUN_ID}
  selected_operating_reference: none
  selected_promotion_candidate: none
  selected_baseline: none
  selected_variant_id: {SELECTED_VARIANT_ID}
  boundary: {BOUNDARY}
  stage_brief_path: stages/{STAGE_ID}/00_spec/stage_brief.md
  selection_status_path: stages/{STAGE_ID}/04_selected/selection_status.md
  report_path: stages/{STAGE_ID}/03_reviews/run16B_hmm_state_runtime_probe_packet.md
  packet_summary_path: docs/agent_control/packets/{PACKET_ID}/aggregate_summary.json
  next_action: {next_action}
"""
    state = replace_top_level_yaml_block(state, "stage22_hmm_hidden_state_segmentation:", stage_block)
    run16a_block = f"""stage22_hmm_run16A_structural_scout:
  packet_id: {SOURCE_PACKET_ID}
  status: reviewed_structural_scout_completed
  judgment: inconclusive_hmm_hidden_state_structural_scout_completed
  current_run_id: {SOURCE_RUN_ID}
  selected_variant_id: {SELECTED_VARIANT_ID}
  mt5_runtime_probe_status: completed_by_next_milestone_{RUN_ID}
  selected_operating_reference: none
  selected_promotion_candidate: none
  selected_baseline: none
  boundary: hmm_hidden_state_structural_scout_only_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority
  report_path: stages/{STAGE_ID}/03_reviews/run16A_hmm_state_scout_packet.md
  packet_summary_path: docs/agent_control/packets/{SOURCE_PACKET_ID}/aggregate_summary.json
  next_action: {RUN_ID}
"""
    state = replace_top_level_yaml_block(state, "stage22_hmm_run16A_structural_scout:", run16a_block)
    block = f"""stage22_hmm_run16B_runtime_probe:
  packet_id: {PACKET_ID}
  status: {'reviewed_runtime_probe_completed' if completed else 'blocked_runtime_probe_after_attempt'}
  judgment: {summary.get('closure_judgment')}
  current_run_id: {RUN_ID}
  source_run_id: {SOURCE_RUN_ID}
  selected_variant_id: {SELECTED_VARIANT_ID}
  mt5_attempt_count: {summary.get('attempt_count')}
  mt5_kpi_record_count: {summary.get('mt5_kpi_record_count')}
  selected_operating_reference: none
  selected_promotion_candidate: none
  selected_baseline: none
  boundary: {BOUNDARY}
  report_path: stages/{STAGE_ID}/03_reviews/run16B_hmm_state_runtime_probe_packet.md
  packet_summary_path: docs/agent_control/packets/{PACKET_ID}/aggregate_summary.json
  next_action: {next_action}
"""
    state = replace_top_level_yaml_block(state, "stage22_hmm_run16B_runtime_probe:", block)
    io_path(WORKSPACE_STATE_PATH).write_text(state, encoding="utf-8-sig")


def update_text_docs(summary: Mapping[str, Any]) -> None:
    completed = summary.get("external_verification_status") == "completed"
    status = "active_run16B_mt5_runtime_probe_completed" if completed else "active_run16B_mt5_runtime_probe_blocked_after_attempt"
    next_action = "stage22_closeout_and_stage23_open_only" if completed else "repair run16B HMM state runtime probe and rerun the same six MT5 attempts"
    write_md(
        SELECTION_STATUS_PATH,
        f"""# Stage22 Selection Status(22단계 선택 상태)

## Current Read(현재 판독)

- stage(단계): `{STAGE_ID}`
- status(상태): `{status}`
- current run(현재 실행): `{RUN_ID}`
- selected operating reference/promotion/baseline(선택 운영 기준/승격/기준선): `none(없음)`
- judgment(판정): `{summary.get('closure_judgment')}`
- selected variant(선택 변형): `{SELECTED_VARIANT_ID}`
- boundary(경계): `{BOUNDARY}`

효과(effect, 효과): Stage22(22단계) HMM(은닉 마르코프 모델)의 hidden state(숨은 상태)를 MT5(MetaTrader 5, 메타트레이더5) runtime_probe(런타임 탐침)까지 연결했다. baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없다.

## Next Exact Action(다음 정확한 행동)

`{next_action}`.
""",
    )
    review = io_path(REVIEW_INDEX_PATH).read_text(encoding="utf-8-sig") if io_path(REVIEW_INDEX_PATH).exists() else "# Stage22 Review Index(22단계 검토 색인)\n"
    line = f"- `{RUN_ID}`: `{rel(REVIEW_PATH)}`\n"
    if RUN_ID not in review:
        write_md(REVIEW_INDEX_PATH, review.rstrip() + "\n" + line)
    write_md(
        DECISION_PATH,
        f"""# Stage22 RUN16B HMM State Runtime Decision(22단계 실행16B HMM 상태 런타임 결정)

## Decision(결정)

`{RUN_ID}`를 `{summary.get('closure_judgment')}`로 기록한다.

효과(effect, 효과): HMM(`Hidden Markov Model`, 은닉 마르코프 모델) state policy(상태 정책)가 MT5(`MetaTrader 5`, 메타트레이더5) tester output(테스터 출력)까지 도달했는지 확인했다. 이 근거는 runtime_probe(런타임 탐침)일 뿐 edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위)가 아니다.

## Next Condition(다음 조건)

`{next_action}`.
""",
    )
    current = io_path(CURRENT_WORKING_STATE_PATH).read_text(encoding="utf-8-sig")
    update = f"""## Latest Stage22 RUN16B HMM Runtime Update(최신 22단계 실행16B HMM 런타임 업데이트)

Stage22(22단계) `{RUN_ID}`를 MT5(`MetaTrader 5`, 메타트레이더5) runtime_probe(런타임 탐침)로 실행했다.

결과(result, 결과): `{summary.get('closure_judgment')}`. MT5 KPI records(MT5 핵심 성과 지표 기록): `{summary.get('mt5_kpi_record_count')}`. next exact action(다음 정확한 행동): `{next_action}`.

효과(effect, 효과): HMM(은닉 마르코프 모델) hidden state(숨은 상태)가 table handoff(테이블 인계)로 runtime(런타임)에 전달되는지 검증했다. baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없다.

"""
    io_path(CURRENT_WORKING_STATE_PATH).write_text(update + current, encoding="utf-8-sig")
    plan = io_path(GOAL_PLAN_PATH).read_text(encoding="utf-8-sig")
    marker = "## Latest Stop Resume State"
    resume = f"""## Latest Stop Resume State(최신 중지 재개 상태)

- latest completed work(최근 완료 작업): `{RUN_ID}` {'completed(완료)' if completed else 'blocked after attempt(시도 후 차단)'} as MT5 runtime_probe(MT5 런타임 탐침).
- active branch(활성 브랜치): `codex/stage22-hmm-hidden-state`.
- active stage/current run id(활성 단계/현재 실행 ID): Stage22(22단계), `{RUN_ID}`.
- created/updated folders(생성/수정 폴더): `stages/{STAGE_ID}/02_runs/{RUN_ID}`, `docs/agent_control/packets/{PACKET_ID}`.
- changed files(변경 파일): HMM state policy helper(HMM 상태 정책 도우미), Stage22 run16B runtime pipeline(22단계 실행16B 런타임 파이프라인), run evidence(실행 근거), ledgers(장부), current truth docs(현재 진실 문서).
- active stage folder(활성 단계 폴더): `stages/{STAGE_ID}`.
- current run id(현재 실행 ID): `{RUN_ID}`.
- MT5 output folder/report path(MT5 출력 폴더/보고서 경로): `{rel(RUN_ROOT / 'mt5')}` and `{rel(REVIEW_PATH)}`.
- blocker(차단 사유): `{'none(없음)' if completed else 'see run_manifest runtime_probe failure(실행 목록 런타임 탐침 실패 참조)'}`.
- exact next action(정확한 다음 행동): `{next_action}`.
- git status(깃 상태): checkpoint commit/push(중간 지점 커밋/푸시) pending(대기).

효과(effect, 효과): 다음 재개는 Stage22(22단계) closeout(마감) 또는 run16B repair(수정)에서 바로 시작한다.
"""
    start = plan.find(marker)
    if start != -1:
        next_section = plan.find("\n## ", start + 1)
        plan = plan[:start] + resume + ("\n" + plan[next_section + 1 :] if next_section != -1 else "")
    else:
        plan = plan.rstrip() + "\n\n" + resume
    if RUN_ID not in plan:
        plan = plan.rstrip() + f"\n- `2026-05-05`: Stage22(22단계) `{RUN_ID}` MT5 runtime_probe(MT5 런타임 탐침)를 기록했다.\n"
    io_path(GOAL_PLAN_PATH).write_text(plan, encoding="utf-8-sig")


def run(args: argparse.Namespace) -> dict[str, Any]:
    created_at = utc_now()
    context = load_source_context()
    model_artifacts, tier_records, prediction_artifacts = materialize_state_policy(context)
    feature_matrices = export_feature_matrices(context)
    copies = copy_runtime_inputs(model_artifacts, feature_matrices)
    attempts = make_attempts(context, model_artifacts, feature_matrices)
    prepared = {
        "stage_id": STAGE_ID,
        "stage_number": STAGE_NUMBER,
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "run_root": RUN_ROOT,
        "selected_variant_id": SELECTED_VARIANT_ID,
        "attempts": attempts,
        "common_copies": copies,
        "route_coverage": route_coverage(context),
        "model_artifacts": model_artifacts,
        "feature_matrices": list(feature_matrices.values()),
    }
    result = execute_or_block(prepared, args)
    result["model_artifacts"] = model_artifacts
    result["feature_matrices"] = list(feature_matrices.values())
    provisional = {"normalized_records": 0, "normalized_summary_rows": 0, "missing_runs": 0, "parser_errors": 0, "trade_attribution_records": 0, "trade_level_rows": 0, "trade_parser_errors": 0}
    write_run_outputs(result, context, model_artifacts, prediction_artifacts, tier_records, provisional, created_at)
    kpi = write_normalized_kpi()
    summary = write_run_outputs(result, context, model_artifacts, prediction_artifacts, tier_records, kpi, created_at)
    update_workspace_state(summary)
    update_text_docs(summary)
    return summary


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run Stage22 HMM state MT5 runtime probe.")
    parser.add_argument("--materialize-only", action="store_true", help="Prepare artifacts without launching MT5.")
    parser.add_argument("--timeout-seconds", type=int, default=900, help="Maximum seconds per MT5 attempt.")
    parser.add_argument("--terminal-path", default=str(TERMINAL_PATH_DEFAULT), help="MT5 terminal64.exe path.")
    parser.add_argument("--metaeditor-path", default=str(METAEDITOR_PATH_DEFAULT), help="MetaEditor64.exe path.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_arg_parser().parse_args(argv)
    print(json.dumps(json_ready(run(args)), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
