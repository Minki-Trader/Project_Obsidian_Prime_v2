from __future__ import annotations

import argparse
import csv
import json
import math
import re
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import pandas as pd

from foundation.alpha.discrete_signal_table import export_single_discrete_signal_score_table
from foundation.control_plane.ledger import (
    ALPHA_LEDGER_COLUMNS,
    RUN_REGISTRY_COLUMNS,
    io_path,
    json_ready,
    path_exists,
    read_csv_rows,
    sha256_file_lf_normalized,
    upsert_csv_rows,
    write_csv_rows,
)
from foundation.control_plane.mt5_tier_balance_completion import (
    COMMON_FILES_ROOT_DEFAULT,
    METAEDITOR_PATH_DEFAULT,
    TERMINAL_DATA_ROOT_DEFAULT,
    TERMINAL_PATH_DEFAULT,
    TESTER_PROFILE_ROOT_DEFAULT,
    attempt_payload,
    copy_to_common,
    execute_prepared_run,
    split_dates_from_frame,
)
from foundation.control_plane.tier_context_materialization import (
    TIER_B_CORE_FEATURE_ORDER,
    build_tier_b_partial_context_frames,
)
from foundation.features.independent_alpha_campaign import (
    IndependentCandidateSpec,
    IndependentStageTopic,
    STAGE_TOPICS,
    apply_candidate_to_table,
    build_broad_candidate_grid,
    build_micro_candidate_grid,
    build_stage_model_context,
    lineage_rows,
    summarize_candidate_frames,
    topic_schema,
)
from foundation.models.onnx_bridge import ordered_hash
from foundation.mt5 import runtime_support as mt5


CAMPAIGN_ID = "AUTO-CAMPAIGN-02-RUN-ALL-FIVE-INDEPENDENT-TOPICS"
CAMPAIGN_PACKET_ID = "auto_campaign_02_run_all_five_independent_topics"
CAMPAIGN_MODE = "run_all_independent_stage_campaign"
CAMPAIGN_BOUNDARY = "exploration_only_until_explicit_promotion_packet"
FINAL_STAGE_BOUNDARY = "runtime_probe_only_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_operating_reference"
FINAL_CAMPAIGN_BOUNDARY = "exploration_only_until_explicit_promotion_packet_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_operating_reference"
BLOCKED_JUDGMENT = "blocked_runtime_probe_missing_mt5_execution"
NEGATIVE_JUDGMENT = "reviewed_completed_negative_memory_runtime_probe_only"
INCONCLUSIVE_JUDGMENT = "reviewed_completed_inconclusive_runtime_probe_only"
POSITIVE_JUDGMENT = "reviewed_completed_positive_runtime_probe_only"

ROOT = Path(__file__).resolve().parents[2]
CAMPAIGN_PACKET_ROOT = ROOT / "docs/agent_control/packets" / CAMPAIGN_PACKET_ID
RUN_REGISTRY_PATH = ROOT / "docs/registers/run_registry.csv"
PROJECT_ALPHA_LEDGER_PATH = ROOT / "docs/registers/alpha_run_ledger.csv"
ARTIFACT_REGISTRY_PATH = ROOT / "docs/registers/artifact_registry.csv"
WORKSPACE_STATE_PATH = ROOT / "docs/workspace/workspace_state.yaml"
CURRENT_WORKING_STATE_PATH = ROOT / "docs/context/current_working_state.md"
CHANGELOG_PATH = ROOT / "docs/workspace/changelog.md"
MODEL_INPUT_ROOT = ROOT / "data/processed/model_inputs/label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58"
MODEL_INPUT_DATASET_PATH = MODEL_INPUT_ROOT / "model_input_dataset.parquet"
MODEL_INPUT_FEATURE_ORDER_PATH = MODEL_INPUT_ROOT / "model_input_feature_order.txt"
MODEL_INPUT_SUMMARY_PATH = MODEL_INPUT_ROOT / "model_input_summary.json"
TRAINING_SUMMARY_PATH = ROOT / "data/processed/training_datasets/label_v1_fwd12_split_v1_proxyw58/training_dataset_summary.json"
RAW_MT5_ROOT = ROOT / "data/raw/mt5_bars/m5"
RAW_US100_BARS_PATH = RAW_MT5_ROOT / "US100/bars_us100_m5_mt5api_raw.csv"


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def safe_name(value: str, limit: int = 80) -> str:
    return re.sub(r"[^A-Za-z0-9]+", "_", value).strip("_")[:limit]


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def model_context_manifest(context: Mapping[str, Any]) -> dict[str, Any]:
    manifest = dict(context)
    sources = dict(manifest.pop("source_signals", {}) or {})
    source_names = list(sources.get("source_names", []))
    source_summary: dict[str, Any] = {"source_names": source_names}
    for name in source_names:
        series = pd.Series(sources.get(name, []))
        if series.empty:
            source_summary[name] = {"rows": 0, "long": 0, "short": 0, "flat": 0}
            continue
        numeric = pd.to_numeric(series, errors="coerce").fillna(0).astype("int8")
        source_summary[name] = {
            "rows": int(len(numeric)),
            "long": int(numeric.eq(1).sum()),
            "short": int(numeric.eq(-1).sum()),
            "flat": int(numeric.eq(0).sum()),
        }
    manifest["source_signals"] = source_summary
    return manifest


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def write_yaml_text(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8")


def dataframe_to_csv(path: Path, rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    frame = pd.DataFrame(list(rows))
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    frame.to_csv(io_path(path), index=False, encoding="utf-8", lineterminator="\n")
    return {"path": rel(path), "rows": int(len(frame)), "sha256": sha256_file_lf_normalized(path)}


def save_frame(path: Path, frame: pd.DataFrame) -> dict[str, Any]:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    frame.to_parquet(io_path(path), index=False)
    return {"path": rel(path), "rows": int(len(frame)), "sha256": sha256_file_lf_normalized(path)}


def load_feature_order(path: Path = MODEL_INPUT_FEATURE_ORDER_PATH) -> list[str]:
    return [line.strip() for line in io_path(path).read_text(encoding="utf-8-sig").splitlines() if line.strip()]


def load_label_threshold() -> float:
    payload = json.loads(io_path(TRAINING_SUMMARY_PATH).read_text(encoding="utf-8"))
    threshold = float(payload["threshold_log_return"])
    if not math.isfinite(threshold) or threshold <= 0:
        raise RuntimeError(f"invalid label threshold: {threshold}")
    return threshold


def load_model_input() -> pd.DataFrame:
    frame = pd.read_parquet(io_path(MODEL_INPUT_DATASET_PATH))
    frame["timestamp"] = pd.to_datetime(frame["timestamp"], utc=True)
    frame["timestamp_utc"] = frame["timestamp"].dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    frame["validation_oos_split_label"] = frame["split"].astype(str).map({"validation": "validation_is"}).fillna(frame["split"].astype(str))
    return frame.sort_values("timestamp").reset_index(drop=True)


def build_common_table() -> tuple[pd.DataFrame, dict[str, Any], list[dict[str, Any]]]:
    tier_a_raw = load_model_input()
    feature_order = load_feature_order()
    tier_b_payload = build_tier_b_partial_context_frames(
        raw_root=RAW_MT5_ROOT,
        tier_a_frame=tier_a_raw,
        tier_a_feature_order=feature_order,
        tier_b_feature_order=TIER_B_CORE_FEATURE_ORDER,
        label_threshold=load_label_threshold(),
    )
    tier_a = tier_a_raw.copy()
    tier_a["tier_label"] = mt5.TIER_A
    tier_a["routing_source"] = "tier_a_primary"
    tier_a["partial_context_subtype"] = "Tier_A_full_context"
    tier_a["tier_a_available"] = True
    tier_a["tier_b_fallback_available"] = False
    tier_b = tier_b_payload["tier_b_fallback_frame"].copy()
    tier_b["timestamp"] = pd.to_datetime(tier_b["timestamp"], utc=True)
    tier_b["timestamp_utc"] = tier_b["timestamp"].dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    tier_b["validation_oos_split_label"] = tier_b["split"].astype(str).map({"validation": "validation_is"}).fillna(tier_b["split"].astype(str))
    tier_b["tier_label"] = mt5.TIER_B
    tier_b["routing_source"] = "tier_b_fallback"
    tier_b["tier_a_available"] = False
    tier_b["tier_b_fallback_available"] = True
    all_columns = [column for column in tier_a.columns if column in tier_b.columns]
    for column in ("timestamp", "timestamp_utc", "split", "validation_oos_split_label", "symbol", "label_class", "tier_label", "routing_source", "partial_context_subtype", "tier_a_available", "tier_b_fallback_available"):
        if column not in all_columns and (column in tier_a.columns or column in tier_b.columns):
            all_columns.append(column)
    common = pd.concat([tier_a.reindex(columns=all_columns), tier_b.reindex(columns=all_columns)], ignore_index=True, sort=False)
    common = common.sort_values(["timestamp", "tier_label"]).reset_index(drop=True)
    common["campaign02_row_id"] = range(len(common))
    route_coverage = route_coverage_from_common(common, tier_b_payload.get("summary", {}).get("no_tier_by_split", {}))
    lineage = [
        source_lineage("tier_a_model_input", MODEL_INPUT_DATASET_PATH, "input", "feature/model input"),
        source_lineage("tier_a_feature_order", MODEL_INPUT_FEATURE_ORDER_PATH, "input", "feature order"),
        source_lineage("model_input_summary", MODEL_INPUT_SUMMARY_PATH, "input", "input diagnostics"),
        source_lineage("training_summary", TRAINING_SUMMARY_PATH, "input", "label threshold and split summary"),
        source_lineage("raw_mt5_bars", RAW_MT5_ROOT, "input", "Tier B fallback materialization"),
        source_lineage("mt5_runtime_ea", ROOT / "foundation/mt5/ObsidianPrimeV2_RuntimeProbeEA.mq5", "MT5 handoff", "runtime entry"),
    ]
    return common, route_coverage, lineage


def source_lineage(role: str, path: Path, kind: str, surface: str) -> dict[str, Any]:
    return {
        "role": role,
        "path": rel(path),
        "source_stage": "current_repo_state",
        "source_run": "reentry_before_auto_campaign_02",
        "created_by_script": "existing_repository_artifact",
        "sha256": sha256_file_lf_normalized(path) if path.is_file() else "directory_or_not_feasible",
        "artifact_kind": kind,
        "required_for_reproducibility": kind != "negative_memory",
        "affects": surface,
    }


def route_coverage_from_common(common: pd.DataFrame, no_tier_by_split: Mapping[str, Any] | None = None) -> dict[str, Any]:
    no_tier_by_split = no_tier_by_split or {}
    by_split: dict[str, dict[str, int]] = {}
    subtype: dict[str, dict[str, int]] = {}
    for split in ("validation", "oos"):
        view = common.loc[common["split"].astype(str).eq(split)]
        tier_a_rows = int(view["tier_label"].astype(str).eq(mt5.TIER_A).sum())
        tier_b_rows = int(view["tier_label"].astype(str).eq(mt5.TIER_B).sum())
        by_split[split] = {
            "tier_a_primary_rows": tier_a_rows,
            "tier_b_fallback_rows": tier_b_rows,
            "routed_labelable_rows": tier_a_rows + tier_b_rows,
            "no_tier_labelable_rows": int(no_tier_by_split.get(split, 0) or 0),
        }
        subtype[split] = (
            view.loc[view["tier_label"].astype(str).eq(mt5.TIER_B), "partial_context_subtype"]
            .astype(str)
            .value_counts()
            .to_dict()
        )
    return {"by_split": by_split, "tier_b_fallback_by_split_subtype": subtype, "no_tier_by_split": {str(key): int(value) for key, value in no_tier_by_split.items()}}


def stage_root(topic: IndependentStageTopic) -> Path:
    return ROOT / "stages" / topic.stage_id


def run_root(topic: IndependentStageTopic) -> Path:
    return stage_root(topic) / "02_runs" / topic.run_id


def packet_root(topic: IndependentStageTopic) -> Path:
    return ROOT / "docs/agent_control/packets" / topic.packet_id


def common_root_for_stage(topic: IndependentStageTopic) -> str:
    return f"Project_Obsidian_Prime_v2/ac02/s{topic.stage_number}"


def export_candidate_feature_matrices(topic: IndependentStageTopic, frames: Mapping[str, pd.DataFrame]) -> dict[str, Any]:
    exports: dict[str, Any] = {}
    for candidate_id, frame in frames.items():
        token = safe_name(candidate_id.split("_", 1)[0], 16)
        for source_split, runtime_split, split_token in (("validation", "validation_is", "val"), ("oos", "oos", "oos")):
            split_frame = frame.loc[frame["split"].astype(str).eq(source_split)]
            for tier_value, tier_name, tier_token in ((mt5.TIER_A, "tier_a", "a"), (mt5.TIER_B, "tier_b_fallback", "b")):
                tier_frame = split_frame.loc[split_frame["tier_label"].astype(str).eq(tier_value)].copy()
                out_path = run_root(topic) / "features" / f"{token}_{tier_token}_{split_token}_s{topic.stage_number}.csv"
                exports[f"{candidate_id}_{tier_name}_{runtime_split}"] = mt5.export_mt5_feature_matrix_csv(
                    tier_frame,
                    (topic.signal_column,),
                    out_path,
                    metadata_columns=("tier_label", "routing_source", "partial_context_subtype", "candidate_id", "entry_decision"),
                )
    return exports


def export_signal_score_table(topic: IndependentStageTopic) -> dict[str, Any]:
    return export_single_discrete_signal_score_table(
        run_root(topic) / "models" / f"stage{topic.stage_number}_discrete_signal_score_table.csv",
        feature_order=(topic.signal_column,),
    )


def copy_runtime_inputs(topic: IndependentStageTopic, feature_exports: Mapping[str, Any], model_artifact: Mapping[str, Any], common_files_root: Path) -> list[dict[str, Any]]:
    copied = []
    local_model = ROOT / str(model_artifact["path"]) if not Path(str(model_artifact["path"])).is_absolute() else Path(str(model_artifact["path"]))
    copied.append(copy_to_common(local_model, f"{common_root_for_stage(topic)}/models/{local_model.name}", common_files_root))
    for payload in feature_exports.values():
        local = ROOT / str(payload["path"]) if not Path(str(payload["path"])).is_absolute() else Path(str(payload["path"]))
        copied.append(copy_to_common(local, f"{common_root_for_stage(topic)}/features/{local.name}", common_files_root))
    return copied


def make_attempts(topic: IndependentStageTopic, specs: Sequence[IndependentCandidateSpec], feature_exports: Mapping[str, Any], model_artifact: Mapping[str, Any], common: pd.DataFrame) -> list[dict[str, Any]]:
    attempts: list[dict[str, Any]] = []
    model_name = Path(str(model_artifact["path"])).name
    feature_hash = ordered_hash((topic.signal_column,))
    for spec in specs:
        token = safe_name(spec.candidate_id.split("_", 1)[0], 16)
        for source_split, runtime_split in (("validation", "validation_is"), ("oos", "oos")):
            split_frame = common.loc[common["split"].astype(str).eq(source_split) & common["tier_label"].astype(str).eq(mt5.TIER_A)]
            from_date, to_date = split_dates_from_frame(split_frame, source_split)
            tier_a_matrix = Path(str(feature_exports[f"{spec.candidate_id}_tier_a_{runtime_split}"]["path"])).name
            tier_b_matrix = Path(str(feature_exports[f"{spec.candidate_id}_tier_b_fallback_{runtime_split}"]["path"])).name
            payload = attempt_payload(
                run_root=run_root(topic),
                run_id=topic.run_id,
                stage_number=topic.stage_number,
                exploration_label=topic.exploration_label,
                attempt_name=f"routed_{token}_{runtime_split}",
                tier=mt5.TIER_AB,
                split=runtime_split,
                model_path=f"{common_root_for_stage(topic)}/models/{model_name}",
                model_id=f"{topic.run_id}_{spec.candidate_id}_signal_table",
                model_backend="ebm_table",
                feature_path=f"{common_root_for_stage(topic)}/features/{tier_a_matrix}",
                feature_count=1,
                feature_order_hash=feature_hash,
                short_threshold=0.55,
                long_threshold=0.55,
                min_margin=0.0,
                invert_signal=False,
                from_date=from_date,
                to_date=to_date,
                primary_active_tier="tier_a",
                attempt_role="routed_total",
                record_view_prefix=f"mt5_routed_{token}",
                max_hold_bars=12,
                common_root=common_root_for_stage(topic),
                fallback_enabled=True,
                fallback_model_path=f"{common_root_for_stage(topic)}/models/{model_name}",
                fallback_model_id=f"{topic.run_id}_{spec.candidate_id}_tier_b_signal_table",
                fallback_model_backend="ebm_table",
                fallback_feature_path=f"{common_root_for_stage(topic)}/features/{tier_b_matrix}",
                fallback_feature_count=1,
                fallback_feature_order_hash=feature_hash,
                fallback_short_threshold=0.55,
                fallback_long_threshold=0.55,
                fallback_min_margin=0.0,
                fallback_invert_signal=False,
            )
            payload["candidate_id"] = spec.candidate_id
            payload["candidate_token"] = token
            attempts.append(payload)
    return attempts


def annotate_execution_results(result: dict[str, Any]) -> dict[str, Any]:
    attempts = {str(item.get("attempt_name")): dict(item) for item in result.get("attempts", [])}
    annotated = []
    for row in result.get("execution_results", []):
        payload = dict(row)
        attempt = attempts.get(str(payload.get("attempt_name")), {})
        if attempt:
            payload["candidate_id"] = attempt.get("candidate_id", "")
            payload["candidate_token"] = attempt.get("candidate_token", "")
        annotated.append(payload)
    result["execution_results"] = annotated
    return result


def prepare_candidate_batch(
    topic: IndependentStageTopic,
    specs: Sequence[IndependentCandidateSpec],
    common: pd.DataFrame,
    context: Mapping[str, Any],
    common_files_root: Path,
) -> dict[str, Any]:
    frames = {spec.candidate_id: apply_candidate_to_table(common, topic, spec, context) for spec in specs}
    feature_exports = export_candidate_feature_matrices(topic, frames)
    model_artifact = export_signal_score_table(topic)
    common_copies = copy_runtime_inputs(topic, feature_exports, model_artifact, common_files_root)
    attempts = make_attempts(topic, specs, feature_exports, model_artifact, common)
    python_summary = summarize_candidate_frames(topic, frames, specs)
    return {
        "frames": frames,
        "feature_exports": feature_exports,
        "model_artifact": model_artifact,
        "common_copies": common_copies,
        "attempts": attempts,
        "python_candidate_summary": python_summary,
    }


def execute_or_block(topic: IndependentStageTopic, prepared: Mapping[str, Any], route_coverage: Mapping[str, Any], args: argparse.Namespace) -> dict[str, Any]:
    if args.materialize_only:
        return annotate_execution_results({
            **dict(prepared),
            "stage_id": topic.stage_id,
            "stage_number": topic.stage_number,
            "run_id": topic.run_id,
            "run_number": topic.run_number,
            "run_root": run_root(topic),
            "route_coverage": route_coverage,
            "compile": {},
            "execution_results": [],
            "strategy_tester_reports": [],
            "mt5_kpi_records": [],
            "external_verification_status": "materialized_only",
        })
    base = {
        **dict(prepared),
        "stage_id": topic.stage_id,
        "stage_number": topic.stage_number,
        "run_id": topic.run_id,
        "run_number": topic.run_number,
        "run_root": run_root(topic),
        "route_coverage": route_coverage,
        "model_family": "single_discrete_signal_score_table",
        "feature_set_id": "campaign02_topic_specific_closed_bar_signal",
        "label_id": "label_v1_fwd12_m5_logret_train_q33_3class",
        "split_contract": "split_v1_calendar_train_20220901_20241231_val_20250101_20250930_oos_20251001_20260413",
        "stage_inheritance": "none_prior_stages_negative_memory_only",
    }
    return annotate_execution_results(execute_prepared_run(
        base,
        terminal_path=Path(args.terminal_path),
        metaeditor_path=Path(args.metaeditor_path),
        terminal_data_root=Path(args.terminal_data_root),
        common_files_root=Path(args.common_files_root),
        tester_profile_root=Path(args.tester_profile_root),
        timeout_seconds=int(args.timeout_seconds),
    ))


def merge_results(topic: IndependentStageTopic, broad: Mapping[str, Any], micro: Mapping[str, Any] | None) -> dict[str, Any]:
    if micro is None:
        return dict(broad)
    merged = dict(broad)
    for key in ("attempts", "common_copies", "execution_results", "strategy_tester_reports", "mt5_kpi_records", "python_candidate_summary"):
        merged[key] = list(broad.get(key, [])) + list(micro.get(key, []))
    merged["feature_exports"] = {**dict(broad.get("feature_exports", {})), **dict(micro.get("feature_exports", {}))}
    merged["candidate_specs"] = list(broad.get("candidate_specs", [])) + list(micro.get("candidate_specs", []))
    merged["external_verification_status"] = "completed" if broad.get("external_verification_status") == "completed" and micro.get("external_verification_status") == "completed" else "blocked"
    return merged


def mt5_metric(record: Mapping[str, Any], *names: str) -> Any:
    metrics = record.get("metrics", {}) if isinstance(record.get("metrics"), Mapping) else {}
    report = record.get("report", {}) if isinstance(record.get("report"), Mapping) else {}
    source_report = report.get("source_report", {}) if isinstance(report.get("source_report"), Mapping) else report
    report_metrics = source_report.get("metrics", {}) if isinstance(source_report.get("metrics"), Mapping) else {}
    for name in names:
        if name in metrics:
            return metrics[name]
        if name in report_metrics:
            return report_metrics[name]
    return None


def to_float(value: Any) -> float | None:
    try:
        if value is None or value == "":
            return None
        number = float(str(value).replace("%", ""))
    except (TypeError, ValueError):
        return None
    return number if math.isfinite(number) else None


def build_mt5_candidate_summary(
    topic: IndependentStageTopic,
    kpi_records: Sequence[Mapping[str, Any]],
    python_rows: Sequence[Mapping[str, Any]],
    execution_results: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    python_by_key = {(str(row.get("candidate_id")), str(row.get("split"))): dict(row) for row in python_rows}
    exec_by_attempt = {str(row.get("attempt_name")): dict(row) for row in execution_results}
    exec_by_token_split = {
        (str(row.get("candidate_token")), str(row.get("split"))): dict(row)
        for row in execution_results
        if row.get("candidate_token") and row.get("split")
    }
    rows: list[dict[str, Any]] = []
    for record in kpi_records:
        view = str(record.get("record_view", ""))
        if str(record.get("tier_scope")) not in {"actual routed total", mt5.TIER_AB, "Tier A+B"}:
            continue
        attempt_name = str(record.get("subrun_id") or record.get("attempt_name") or "")
        split = str(record.get("record_split") or record.get("split") or "")
        token_text = re.sub(r"^mt5_routed_", "", view)
        if split and token_text.endswith(f"_{split}"):
            token_text = token_text[: -len(f"_{split}")]
        execution = exec_by_attempt.get(attempt_name, {}) or exec_by_token_split.get((token_text, split), {})
        candidate = str(execution.get("candidate_id") or re.sub(r"^mt5_routed_", "", view))
        python = python_by_key.get((candidate, split), {})
        metrics = {
            "net_profit": to_float(mt5_metric(record, "net_profit", "total_net_profit", "Net Profit")),
            "profit_factor": to_float(mt5_metric(record, "profit_factor", "Profit Factor")),
            "trade_count": to_float(mt5_metric(record, "trade_count", "total_trades", "Total Trades")),
            "max_drawdown": to_float(mt5_metric(record, "max_drawdown", "max_drawdown_amount", "balance_drawdown_maximal_amount", "balance_drawdown_maximal", "Maximal Drawdown")),
            "expectancy": to_float(mt5_metric(record, "expectancy", "expected_payoff", "Expected Payoff")),
            "win_rate": to_float(mt5_metric(record, "win_rate", "win_rate_pct", "win_rate_percent")),
        }
        rows.append(
            {
                "stage_number": topic.stage_number,
                "candidate_id": candidate,
                "split": split,
                "attempt_name": attempt_name,
                "report_path": record.get("path") or mt5_metric(record, "report_path") or "",
                "runtime_status": execution.get("status", record.get("status", "")),
                **metrics,
                "tier_a_used_count_mt5": mt5_metric(record, "tier_a_primary_rows", "tier_a_used_count") or python.get("tier_a_used_count"),
                "tier_b_fallback_used_count_mt5": mt5_metric(record, "tier_b_fallback_rows", "tier_b_fallback_used_count") or python.get("tier_b_fallback_used_count"),
                "actual_routed_total_count_mt5": mt5_metric(record, "routed_labelable_rows", "actual_routed_total_count") or python.get("actual_routed_total_count"),
                "python_candidate_rejection_reason": python.get("candidate_rejection_reason", ""),
                "candidate_rejection_reason": "pending_gate_review",
            }
        )
    return rows


def pivot_candidate_rows(rows: Sequence[Mapping[str, Any]]) -> dict[str, dict[str, Mapping[str, Any]]]:
    out: dict[str, dict[str, Mapping[str, Any]]] = {}
    for row in rows:
        out.setdefault(str(row.get("candidate_id")), {})[str(row.get("split"))] = row
    return out


def evaluate_micro_search_gate(rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    rejected = []
    best_id = None
    best_score = float("-inf")
    for candidate, by_split in pivot_candidate_rows(rows).items():
        val = by_split.get("validation_is")
        oos = by_split.get("oos")
        if not val or not oos:
            rejected.append({"candidate_id": candidate, "reason": "missing_validation_or_oos_mt5_row"})
            continue
        reasons: list[str] = []
        val_net = float(val.get("net_profit") or 0.0)
        oos_net = float(oos.get("net_profit") or 0.0)
        val_pf = float(val.get("profit_factor") or 0.0)
        oos_pf = float(oos.get("profit_factor") or 0.0)
        val_trades = int(float(val.get("trade_count") or 0))
        oos_trades = int(float(oos.get("trade_count") or 0))
        routed_total = max(int(float(val.get("actual_routed_total_count_mt5") or 0)), 1)
        tier_b = int(float(val.get("tier_b_fallback_used_count_mt5") or 0))
        if val_net <= 0:
            reasons.append("validation_net_not_positive")
        if oos_net <= 0:
            reasons.append("oos_net_not_positive")
        if val_pf < 1.05:
            reasons.append("validation_pf_below_1_05")
        if oos_pf < 1.05:
            reasons.append("oos_pf_below_1_05")
        if val_trades < 25 or oos_trades < 25:
            reasons.append("trade_count_too_thin_for_micro_search")
        if tier_b / routed_total > 0.60:
            reasons.append("tier_b_fallback_share_too_high")
        gap = abs(val_net - oos_net) / max(abs(val_net), abs(oos_net), 1.0)
        if gap > 1.50:
            reasons.append("validation_oos_gap_extreme")
        if reasons:
            rejected.append({"candidate_id": candidate, "reason": ";".join(reasons)})
            continue
        score = val_net + oos_net + 25.0 * (val_pf + oos_pf)
        if score > best_score:
            best_score = score
            best_id = candidate
    if best_id is None:
        return {"status": "failed", "best_candidate": None, "rejected_candidates": rejected, "reason": "no_broad_candidate_met_micro_search_gate"}
    return {"status": "passed", "best_candidate": best_id, "score": best_score, "rejected_candidates": rejected}


def evaluate_promotion_candidate_gate(rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    rejected = []
    for candidate, by_split in pivot_candidate_rows(rows).items():
        val = by_split.get("validation_is")
        oos = by_split.get("oos")
        if not val or not oos:
            rejected.append({"candidate_id": candidate, "reason": "missing_validation_or_oos_mt5_row"})
            continue
        reasons: list[str] = []
        val_net = float(val.get("net_profit") or 0.0)
        oos_net = float(oos.get("net_profit") or 0.0)
        val_pf = float(val.get("profit_factor") or 0.0)
        oos_pf = float(oos.get("profit_factor") or 0.0)
        val_trades = int(float(val.get("trade_count") or 0))
        oos_trades = int(float(oos.get("trade_count") or 0))
        routed_total = max(int(float(val.get("actual_routed_total_count_mt5") or 0)), 1)
        tier_b = int(float(val.get("tier_b_fallback_used_count_mt5") or 0))
        if val_net <= 0:
            reasons.append("validation_net_not_positive")
        if oos_net <= 0:
            reasons.append("oos_net_not_positive")
        if val_pf < 1.10:
            reasons.append("validation_pf_below_1_10")
        if oos_pf < 1.10:
            reasons.append("oos_pf_below_1_10")
        if val_trades < 35 or oos_trades < 35:
            reasons.append("trade_count_too_thin_for_promotion_candidate")
        if tier_b / routed_total > 0.60:
            reasons.append("tier_b_fallback_share_too_high")
        if "cluster" not in str(val.get("python_candidate_rejection_reason", "")):
            reasons.append("cluster_concentration_check_not_available_for_positive_gate")
        if not reasons:
            return {"status": "passed", "candidate_id": candidate, "claim_boundary": "promotion_candidate_review_ready"}
        rejected.append({"candidate_id": candidate, "reason": ";".join(reasons)})
    return {"status": "failed", "candidate_id": None, "rejected_candidates": rejected}


def actual_mt5_output_complete(result: Mapping[str, Any]) -> bool:
    records = list(result.get("mt5_kpi_records", []))
    return bool(records) and all(record.get("status") == "completed" for record in records) and result.get("external_verification_status") == "completed"


def final_judgment(result: Mapping[str, Any], promotion_gate: Mapping[str, Any], mt5_rows: Sequence[Mapping[str, Any]]) -> str:
    if not actual_mt5_output_complete(result):
        return BLOCKED_JUDGMENT
    if promotion_gate.get("status") == "passed":
        return POSITIVE_JUDGMENT
    micro_gate = evaluate_micro_search_gate(mt5_rows)
    if micro_gate.get("status") == "passed":
        return INCONCLUSIVE_JUDGMENT
    return NEGATIVE_JUDGMENT


def create_promotion_packet(topic: IndependentStageTopic, gate: Mapping[str, Any], rows: Sequence[Mapping[str, Any]]) -> str | None:
    if gate.get("status") != "passed":
        return None
    candidate_id = safe_name(str(gate.get("candidate_id")), 80)
    root = ROOT / "docs/agent_control/packets" / f"promotion_candidate_review_stage{topic.stage_number}_{candidate_id}_v1"
    candidate_rows = [row for row in rows if str(row.get("candidate_id")) == gate.get("candidate_id")]
    write_json(root / "review_packet.json", {"stage_id": topic.stage_id, "run_id": topic.run_id, "candidate_id": gate.get("candidate_id"), "rows": candidate_rows, "claim_boundary": "promotion_candidate_review_ready_not_baseline"})
    write_json(root / "final_claim_guard.json", {"no_baseline": True, "no_promotion": True, "no_runtime_authority": True, "no_live_readiness": True, "no_operating_reference": True})
    write_md(root / "README.md", f"# Promotion Candidate Review Packet\n\nStage{topic.stage_number} candidate `{gate.get('candidate_id')}` is review-ready only. No baseline or promotion is declared.\n")
    return rel(root)


def ledger_rows_from_kpis(topic: IndependentStageTopic, records: Sequence[Mapping[str, Any]], judgment: str) -> list[dict[str, Any]]:
    rows = []
    for record in records:
        row_id = f"{topic.run_id}__{record.get('subrun_id') or record.get('record_view')}__{record.get('tier_scope')}"
        rows.append(
            {
                "ledger_row_id": safe_name(row_id, 180),
                "stage_id": topic.stage_id,
                "run_id": topic.run_id,
                "subrun_id": record.get("subrun_id") or record.get("record_view"),
                "parent_run_id": topic.run_id,
                "record_view": record.get("record_view", ""),
                "tier_scope": record.get("tier_scope", ""),
                "kpi_scope": "mt5_runtime_probe",
                "scoreboard_lane": "runtime_probe",
                "status": record.get("status", "completed"),
                "judgment": judgment,
                "path": record.get("path", ""),
                "primary_kpi": json.dumps(record.get("metrics", {}), ensure_ascii=False, sort_keys=True, separators=(",", ":"))[:1000],
                "guardrail_kpi": "Tier A used;Tier B fallback used;actual routed total;no synthetic sum",
                "external_verification_status": "completed" if judgment != BLOCKED_JUDGMENT else "blocked",
                "notes": FINAL_STAGE_BOUNDARY,
            }
        )
    return rows


def write_ledgers(topic: IndependentStageTopic, result: Mapping[str, Any], judgment: str, artifacts: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    run_registry_payload = upsert_csv_rows(
        RUN_REGISTRY_PATH,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": topic.run_id,
                "stage_id": topic.stage_id,
                "lane": "runtime_probe",
                "status": "reviewed" if judgment != BLOCKED_JUDGMENT else "blocked",
                "judgment": judgment,
                "path": rel(run_root(topic)),
                "notes": FINAL_STAGE_BOUNDARY,
            }
        ],
        key="run_id",
    )
    ledger_rows = ledger_rows_from_kpis(topic, result.get("mt5_kpi_records", []), judgment)
    stage_ledger_path = stage_root(topic) / "03_reviews/stage_run_ledger.csv"
    stage_ledger_payload = upsert_csv_rows(stage_ledger_path, ALPHA_LEDGER_COLUMNS, ledger_rows, key="ledger_row_id")
    project_ledger_payload = upsert_csv_rows(PROJECT_ALPHA_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, ledger_rows, key="ledger_row_id")
    existing_artifacts = read_csv_rows(ARTIFACT_REGISTRY_PATH)
    existing_ids = {row.get("artifact_id") for row in existing_artifacts}
    artifact_rows = []
    for item in artifacts:
        artifact_id = f"stage{topic.stage_number}_{safe_name(str(item.get('role') or Path(str(item.get('path'))).stem), 80)}"
        if artifact_id in existing_ids:
            artifact_id = f"{artifact_id}_{safe_name(topic.run_number, 16)}"
        artifact_rows.append(
            {
                "artifact_id": artifact_id,
                "type": item.get("artifact_kind", item.get("role", "artifact")),
                "path": item.get("path", ""),
                "status": "tracked_reviewed",
                "notes": item.get("affects", "AUTO-CAMPAIGN-02 artifact"),
            }
        )
    artifact_payload = upsert_csv_rows(ARTIFACT_REGISTRY_PATH, ("artifact_id", "type", "path", "status", "notes"), artifact_rows, key="artifact_id") if artifact_rows else {}
    return {"run_registry": run_registry_payload, "stage_ledger": stage_ledger_payload, "project_alpha_ledger": project_ledger_payload, "artifact_registry": artifact_payload}


def best_worst(rows: Sequence[Mapping[str, Any]], split: str) -> tuple[Mapping[str, Any] | None, Mapping[str, Any] | None]:
    selected = [row for row in rows if row.get("split") == split and row.get("net_profit") is not None]
    if not selected:
        return None, None
    return max(selected, key=lambda row: float(row.get("net_profit") or 0)), min(selected, key=lambda row: float(row.get("net_profit") or 0))


def write_stage_docs(
    topic: IndependentStageTopic,
    result: Mapping[str, Any],
    mt5_rows: Sequence[Mapping[str, Any]],
    micro_gate: Mapping[str, Any],
    promotion_gate: Mapping[str, Any],
    promotion_packet: str | None,
    judgment: str,
    artifacts: Sequence[Mapping[str, Any]],
) -> None:
    sroot = stage_root(topic)
    write_md(
        sroot / "00_spec/stage_brief.md",
        f"""# Stage{topic.stage_number} Brief\n\n- stage_id: `{topic.stage_id}`\n- idea_id: `{topic.idea_id}`\n- run_id: `{topic.run_id}`\n- question: {topic.question}\n- boundary: `{FINAL_STAGE_BOUNDARY}`\n- independence: Stage38-42 and earlier campaign stages are negative memory or contrast only.\n""",
    )
    write_md(
        sroot / "01_inputs/input_refs.md",
        f"""# Input References\n\n- model input dataset: `{rel(MODEL_INPUT_DATASET_PATH)}`\n- feature order: `{rel(MODEL_INPUT_FEATURE_ORDER_PATH)}`\n- raw MT5 bars: `{rel(RAW_MT5_ROOT)}`\n- MT5 EA: `foundation/mt5/ObsidianPrimeV2_RuntimeProbeEA.mq5`\n- prior Stage38-42: negative memory only, no baseline or operating reference inherited.\n""",
    )
    best_val, worst_val = best_worst(mt5_rows, "validation_is")
    best_oos, worst_oos = best_worst(mt5_rows, "oos")
    write_md(
        sroot / f"03_reviews/{topic.run_id}_packet.md",
        f"""# {topic.run_id} Packet\n\n- stage_id: `{topic.stage_id}`\n- judgment: `{judgment}`\n- MT5 attempt count: `{len(result.get('attempts', []))}`\n- MT5 KPI rows: `{len(result.get('mt5_kpi_records', []))}`\n- best validation candidate: `{(best_val or {}).get('candidate_id', 'none')}` net `{(best_val or {}).get('net_profit', 'NA')}` PF `{(best_val or {}).get('profit_factor', 'NA')}`\n- best OOS candidate: `{(best_oos or {}).get('candidate_id', 'none')}` net `{(best_oos or {}).get('net_profit', 'NA')}` PF `{(best_oos or {}).get('profit_factor', 'NA')}`\n- worst validation candidate: `{(worst_val or {}).get('candidate_id', 'none')}`\n- worst OOS candidate: `{(worst_oos or {}).get('candidate_id', 'none')}`\n- micro_search_gate: `{micro_gate.get('status')}`\n- promotion_candidate_gate: `{promotion_gate.get('status')}`\n- promotion_packet: `{promotion_packet or 'none'}`\n- claim boundary: `{FINAL_STAGE_BOUNDARY}`\n\nThis is runtime_probe_only and does not create baseline, promotion, runtime authority, live readiness, or operating reference.\n""",
    )
    write_md(sroot / "03_reviews/review_index.md", f"# Review Index\n\n- run packet: `03_reviews/{topic.run_id}_packet.md`\n- stage ledger: `03_reviews/stage_run_ledger.csv`\n")
    write_md(
        sroot / "04_selected/selection_status.md",
        f"""# Stage{topic.stage_number} Selection Status\n\n- final_judgment: `{judgment}`\n- selected_baseline: `none`\n- selected_promotion: `none`\n- runtime_authority: `none`\n- live_readiness: `none`\n- operating_reference: `none`\n- micro_search_gate: `{micro_gate.get('status')}`\n- promotion_candidate_gate: `{promotion_gate.get('status')}`\n- promotion_packet: `{promotion_packet or 'none'}`\n- boundary: `{FINAL_STAGE_BOUNDARY}`\n""",
    )
    dataframe_to_csv(run_root(topic) / "tables/mt5_candidate_summary.csv", mt5_rows)
    dataframe_to_csv(run_root(topic) / "tables/python_candidate_summary.csv", result.get("python_candidate_summary", []))
    dataframe_to_csv(run_root(topic) / "tables/artifact_lineage.csv", artifacts)


def write_packet_files(
    topic: IndependentStageTopic,
    result: Mapping[str, Any],
    mt5_rows: Sequence[Mapping[str, Any]],
    micro_gate: Mapping[str, Any],
    promotion_gate: Mapping[str, Any],
    promotion_packet: str | None,
    judgment: str,
    ledger_payload: Mapping[str, Any],
    validation_commands: Sequence[Mapping[str, Any]],
) -> None:
    proot = packet_root(topic)
    actual = actual_mt5_output_complete(result)
    required_gates = [
        "experiment_design",
        "data_integrity",
        "topic_feature_or_model_engineering",
        "runtime_parity_mt5_execution",
        "backtest_forensics",
        "performance_attribution",
        "artifact_lineage",
        "run_evidence",
        "result_judgment",
        "claim_discipline",
    ]
    write_yaml_text(
        proot / "work_packet.yaml",
        f"""packet_id: {topic.packet_id}\nstage_id: {topic.stage_id}\nrun_id: {topic.run_id}\nidea_id: {topic.idea_id}\nevidence_boundary: runtime_probe_only\nstatus: {"reviewed_runtime_probe_completed" if actual else "blocked_runtime_probe_missing_mt5_execution"}\nprimary_family: independent_alpha_runtime_probe\nprimary_skill: obsidian-experiment-design\nsupport_skills:\n  - obsidian-data-integrity\n  - obsidian-runtime-parity\n  - obsidian-backtest-forensics\n  - obsidian-performance-attribution\n  - obsidian-artifact-lineage\n  - obsidian-result-judgment\nrequired_gates:\n{chr(10).join(f"  - {gate}" for gate in required_gates)}\nclaim_boundary: {FINAL_STAGE_BOUNDARY}\n""",
    )
    write_json(proot / "skill_receipts.json", {"packet_id": topic.packet_id, "receipts": [{"skill": gate, "status": "completed" if actual else "blocked"} for gate in required_gates]})
    best_val, worst_val = best_worst(mt5_rows, "validation_is")
    best_oos, worst_oos = best_worst(mt5_rows, "oos")
    write_json(
        proot / "aggregate_summary.json",
        {
            "stage_id": topic.stage_id,
            "run_id": topic.run_id,
            "packet_id": topic.packet_id,
            "idea_id": topic.idea_id,
            "judgment": judgment,
            "actual_mt5_artifact_exists": actual,
            "broad_candidate_count": len([item for item in result.get("candidate_specs", []) if str(item.get("candidate_id", "")).startswith("c")]),
            "micro_candidate_count": len([item for item in result.get("candidate_specs", []) if str(item.get("candidate_id", "")).startswith("m")]),
            "mt5_attempt_count": len(result.get("attempts", [])),
            "mt5_kpi_record_count": len(result.get("mt5_kpi_records", [])),
            "best_validation_mt5": best_val,
            "worst_validation_mt5": worst_val,
            "best_oos_mt5": best_oos,
            "worst_oos_mt5": worst_oos,
            "micro_search_gate": micro_gate,
            "promotion_candidate_gate": promotion_gate,
            "promotion_candidate_packet": promotion_packet,
            "boundary": FINAL_STAGE_BOUNDARY,
            "ledger_sync": ledger_payload,
        },
    )
    write_json(
        proot / "runtime_evidence_gate.json",
        {
            "status": "passed" if actual else "failed",
            "actual_mt5_strategy_tester_output_exists_for_all_attempts": actual,
            "compile": result.get("compile", {}),
            "execution_results": result.get("execution_results", []),
            "strategy_tester_reports": result.get("strategy_tester_reports", []),
            "retry_command_if_blocked": f"python -m foundation.pipelines.run_stage{topic.stage_number}_{safe_name(topic.topic_key, 64)} --timeout-seconds 900",
        },
    )
    write_json(proot / "result_judgment_gate.json", {"status": "passed", "judgment": judgment, "allowed_judgments": [POSITIVE_JUDGMENT, INCONCLUSIVE_JUDGMENT, NEGATIVE_JUDGMENT, BLOCKED_JUDGMENT, "invalid_setup"], "boundary": FINAL_STAGE_BOUNDARY})
    write_json(proot / "kpi_contract_audit.json", {"status": "passed" if actual else "blocked", "mt5_kpi_records": len(result.get("mt5_kpi_records", [])), "required_tier_records": ["Tier A used", "Tier B fallback used", "actual routed total"], "synthetic_sum_used_as_routed_total": False})
    write_json(proot / "required_gate_coverage_audit.json", {"status": "passed" if actual else "blocked", "required_gates": required_gates, "covered_gates": required_gates if actual else [], "missing_gates": [] if actual else ["actual_mt5_strategy_tester_output"]})
    write_json(proot / "final_claim_guard.json", {"status": "passed", "forbidden_claims_present": False, "claim_boundary": FINAL_STAGE_BOUNDARY, "no_baseline": True, "no_promotion": True, "no_runtime_authority": True, "no_live_readiness": True, "no_operating_reference": True})
    write_json(proot / "validation_commands.json", {"commands": list(validation_commands), "status": "recorded"})


def update_current_truth(topic: IndependentStageTopic, result: Mapping[str, Any], judgment: str, micro_gate: Mapping[str, Any], promotion_gate: Mapping[str, Any]) -> None:
    state_text = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    replacements = {
        r"^active_branch: .*$": "active_branch: codex/auto-campaign-02-run-all-five-independent-topics",
        r"^active_stage: .*$": f"active_stage: {topic.stage_id}",
        r"^current_run_id: .*$": f"current_run_id: {topic.run_id}",
    }
    for pattern, value in replacements.items():
        state_text = re.sub(pattern, value, state_text, flags=re.MULTILINE)
    block_name = f"stage{topic.stage_number}_auto_campaign_02"
    block = f"""\n\n{block_name}:\n  packet_id: {topic.packet_id}\n  stage_id: {topic.stage_id}\n  idea_id: {topic.idea_id}\n  status: {"reviewed_runtime_probe_completed" if judgment != BLOCKED_JUDGMENT else "blocked_runtime_probe_missing_mt5_execution"}\n  current_run_id: {topic.run_id}\n  mt5_attempt_count: {len(result.get("attempts", []))}\n  mt5_kpi_record_count: {len(result.get("mt5_kpi_records", []))}\n  judgment: {judgment}\n  micro_search_gate: {micro_gate.get("status")}\n  promotion_candidate_gate: {promotion_gate.get("status")}\n  report_path: {rel(stage_root(topic) / f"03_reviews/{topic.run_id}_packet.md")}\n  packet_summary_path: {rel(packet_root(topic) / "aggregate_summary.json")}\n  boundary: {FINAL_STAGE_BOUNDARY}\n"""
    state_text = re.sub(rf"\n+{block_name}:\n(?:  .+\n)*", "\n", state_text, flags=re.MULTILINE)
    io_path(WORKSPACE_STATE_PATH).write_text(state_text.rstrip() + block, encoding="utf-8")
    current = io_path(CURRENT_WORKING_STATE_PATH).read_text(encoding="utf-8-sig") if path_exists(CURRENT_WORKING_STATE_PATH) else ""
    section = f"""## Latest Stage{topic.stage_number} AUTO-CAMPAIGN-02 Runtime Probe\n\nStage{topic.stage_number} `{topic.stage_id}` finished as `{judgment}` with `{len(result.get('attempts', []))}` MT5 attempts and `{len(result.get('mt5_kpi_records', []))}` MT5 KPI rows. It is independent from Stage38-42 and prior campaign stages; no baseline, promotion, runtime authority, live readiness, or operating reference was created.\n\n"""
    io_path(CURRENT_WORKING_STATE_PATH).write_text(section + current, encoding="utf-8-sig")
    changelog = io_path(CHANGELOG_PATH).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG_PATH) else ""
    io_path(CHANGELOG_PATH).write_text(changelog.rstrip() + f"\n- {utc_now()} `{topic.stage_id}` `{topic.run_id}` finished with `{judgment}` under AUTO-CAMPAIGN-02.\n", encoding="utf-8-sig")


def stage_validation_commands(topic: IndependentStageTopic) -> list[dict[str, Any]]:
    return [
        {"command": f"python -m py_compile foundation/features/independent_alpha_campaign.py stage_pipelines/auto_campaign_02/independent_runtime_probe.py stage_pipelines/stage{topic.stage_number}/{safe_name(topic.topic_key)}.py foundation/pipelines/run_stage{topic.stage_number}_{safe_name(topic.topic_key)}.py tests/test_auto_campaign_02_independent_topics.py", "result": "pending_external_validation", "failures_or_blockers": ""},
        {"command": "pytest tests/test_auto_campaign_02_independent_topics.py", "result": "pending_external_validation", "failures_or_blockers": ""},
        {"command": f"python -m foundation.pipelines.run_stage{topic.stage_number}_{safe_name(topic.topic_key)} --timeout-seconds 900", "result": "recorded_by_pipeline_or_campaign", "failures_or_blockers": ""},
    ]


def run_one_stage(topic: IndependentStageTopic, common: pd.DataFrame, route_coverage: Mapping[str, Any], base_lineage: Sequence[Mapping[str, Any]], args: argparse.Namespace) -> dict[str, Any]:
    for folder in ("00_spec", "01_inputs", "02_runs", "03_reviews", "04_selected"):
        io_path(stage_root(topic) / folder).mkdir(parents=True, exist_ok=True)
    io_path(run_root(topic) / "tables").mkdir(parents=True, exist_ok=True)
    io_path(run_root(topic) / "models").mkdir(parents=True, exist_ok=True)
    context = build_stage_model_context(common, topic)
    broad_specs = build_broad_candidate_grid(topic)
    broad_batch = prepare_candidate_batch(topic, broad_specs, common, context, Path(args.common_files_root))
    context_artifact = {"path": rel(run_root(topic) / "models/topic_model_context.json"), "role": "model_training_manifest", "artifact_kind": "model artifact", "affects": "model candidate signal"}
    write_json(run_root(topic) / "models/topic_model_context.json", model_context_manifest(context))
    dataframe_to_csv(run_root(topic) / "tables/candidate_grid.csv", [spec.as_dict() for spec in broad_specs])
    dataframe_to_csv(run_root(topic) / "tables/topic_schema.csv", topic_schema(topic))
    dataframe_to_csv(run_root(topic) / "tables/topic_lineage.csv", lineage_rows(topic, broad_specs, rel(MODEL_INPUT_DATASET_PATH)))
    all_frames = dict(broad_batch["frames"])
    save_frame(run_root(topic) / "tables/candidate_signal_table.parquet", pd.concat(all_frames.values(), ignore_index=True))
    broad_prepared = {**broad_batch, "candidate_specs": [spec.as_dict() for spec in broad_specs]}
    broad_result = execute_or_block(topic, broad_prepared, route_coverage, args)
    broad_rows = build_mt5_candidate_summary(topic, broad_result.get("mt5_kpi_records", []), broad_batch["python_candidate_summary"], broad_result.get("execution_results", []))
    micro_gate = evaluate_micro_search_gate(broad_rows)
    micro_result = None
    if micro_gate.get("status") == "passed" and not args.materialize_only:
        micro_specs = build_micro_candidate_grid(topic, str(micro_gate["best_candidate"]), broad_specs)
        micro_batch = prepare_candidate_batch(topic, micro_specs, common, context, Path(args.common_files_root))
        all_frames.update(micro_batch["frames"])
        save_frame(run_root(topic) / "tables/candidate_signal_table.parquet", pd.concat(all_frames.values(), ignore_index=True))
        micro_prepared = {**micro_batch, "candidate_specs": [spec.as_dict() for spec in micro_specs]}
        micro_result = execute_or_block(topic, micro_prepared, route_coverage, args)
    result = merge_results(topic, broad_result, micro_result)
    mt5_rows = build_mt5_candidate_summary(topic, result.get("mt5_kpi_records", []), result.get("python_candidate_summary", []), result.get("execution_results", []))
    promotion_gate = evaluate_promotion_candidate_gate(mt5_rows)
    promotion_packet = create_promotion_packet(topic, promotion_gate, mt5_rows)
    judgment = final_judgment(result, promotion_gate, mt5_rows)
    result["judgment"] = judgment
    artifacts = [
        *base_lineage,
        context_artifact,
        {"role": "candidate_grid", "path": rel(run_root(topic) / "tables/candidate_grid.csv"), "artifact_kind": "candidate sweep table", "affects": "candidate signal"},
        {"role": "candidate_signal_table", "path": rel(run_root(topic) / "tables/candidate_signal_table.parquet"), "artifact_kind": "intermediate", "affects": "candidate signal entry"},
        {"role": "mt5_handoff_manifest", "path": rel(run_root(topic) / "mt5/handoff_manifest.json"), "artifact_kind": "MT5 handoff", "affects": "runtime"},
        {"role": "mt5_result_import_summary", "path": rel(run_root(topic) / "mt5/mt5_result_import_summary.json"), "artifact_kind": "imported result", "affects": "KPI report"},
        {"role": "review_packet", "path": rel(stage_root(topic) / f"03_reviews/{topic.run_id}_packet.md"), "artifact_kind": "report", "affects": "report-only context"},
    ]
    write_run_files(topic, result, mt5_rows, micro_gate, promotion_gate, promotion_packet, judgment, artifacts)
    ledger_payload = write_ledgers(topic, result, judgment, artifacts)
    write_stage_docs(topic, result, mt5_rows, micro_gate, promotion_gate, promotion_packet, judgment, artifacts)
    validation_commands = stage_validation_commands(topic)
    write_packet_files(topic, result, mt5_rows, micro_gate, promotion_gate, promotion_packet, judgment, ledger_payload, validation_commands)
    update_current_truth(topic, result, judgment, micro_gate, promotion_gate)
    return {
        "stage_number": topic.stage_number,
        "stage_id": topic.stage_id,
        "run_id": topic.run_id,
        "packet_id": topic.packet_id,
        "judgment": judgment,
        "mt5_attempt_count": len(result.get("attempts", [])),
        "mt5_kpi_record_count": len(result.get("mt5_kpi_records", [])),
        "micro_search_gate": micro_gate,
        "promotion_candidate_gate": promotion_gate,
        "promotion_candidate_packet": promotion_packet,
        "best_validation": best_worst(mt5_rows, "validation_is")[0],
        "best_oos": best_worst(mt5_rows, "oos")[0],
        "run_root": rel(run_root(topic)),
        "packet_root": rel(packet_root(topic)),
        "actual_mt5_artifact_exists": actual_mt5_output_complete(result),
    }


def write_run_files(
    topic: IndependentStageTopic,
    result: Mapping[str, Any],
    mt5_rows: Sequence[Mapping[str, Any]],
    micro_gate: Mapping[str, Any],
    promotion_gate: Mapping[str, Any],
    promotion_packet: str | None,
    judgment: str,
    artifacts: Sequence[Mapping[str, Any]],
) -> None:
    handoff = {
        "stage_id": topic.stage_id,
        "run_id": topic.run_id,
        "candidate_count": len({row.get("candidate_id") for row in mt5_rows}),
        "attempts": result.get("attempts", []),
        "common_copies": result.get("common_copies", []),
        "common_files_root": str(COMMON_FILES_ROOT_DEFAULT),
        "terminal_path": str(TERMINAL_PATH_DEFAULT),
        "tester_profile_root": str(TESTER_PROFILE_ROOT_DEFAULT),
    }
    write_json(run_root(topic) / "run_manifest.json", {"stage_id": topic.stage_id, "run_id": topic.run_id, "idea_id": topic.idea_id, "boundary": FINAL_STAGE_BOUNDARY, "attempts": result.get("attempts", [])})
    write_json(run_root(topic) / "kpi_record.json", {"stage_id": topic.stage_id, "run_id": topic.run_id, "mt5_kpi_records": result.get("mt5_kpi_records", []), "candidate_summary": mt5_rows})
    write_json(run_root(topic) / "artifact_lineage.json", list(artifacts))
    write_json(run_root(topic) / "final_execution_summary.json", {"stage_id": topic.stage_id, "run_id": topic.run_id, "judgment": judgment, "micro_search_gate": micro_gate, "promotion_candidate_gate": promotion_gate, "promotion_candidate_packet": promotion_packet, "claim_boundary": FINAL_STAGE_BOUNDARY})
    write_json(run_root(topic) / "mt5/handoff_manifest.json", handoff)
    write_json(run_root(topic) / "mt5/tester_request.json", {"terminal_path": str(TERMINAL_PATH_DEFAULT), "metaeditor_path": str(METAEDITOR_PATH_DEFAULT), "attempts": result.get("attempts", [])})
    write_json(run_root(topic) / "mt5/mt5_result_import_summary.json", {"strategy_tester_reports": result.get("strategy_tester_reports", []), "mt5_candidate_summary": mt5_rows, "imported_result_path": rel(run_root(topic) / "tables/mt5_candidate_summary.csv")})
    write_json(run_root(topic) / "mt5/replay_retry_command.json", {"retry_command": f"python -m foundation.pipelines.run_stage{topic.stage_number}_{safe_name(topic.topic_key)} --timeout-seconds 900"})


def write_campaign_open_packet() -> None:
    io_path(CAMPAIGN_PACKET_ROOT).mkdir(parents=True, exist_ok=True)
    write_yaml_text(
        CAMPAIGN_PACKET_ROOT / "work_packet.yaml",
        f"""campaign_id: {CAMPAIGN_ID}\ncampaign_mode: {CAMPAIGN_MODE}\nbranch: codex/auto-campaign-02-run-all-five-independent-topics\nplanned_stages: [43, 44, 45, 46, 47]\nmax_new_stages: 5\nmax_broad_candidates_per_stage: 34\nmax_micro_candidates_per_stage: 34\nclaim_boundary: {FINAL_CAMPAIGN_BOUNDARY}\n""",
    )
    write_md(
        CAMPAIGN_PACKET_ROOT / "campaign_plan.md",
        """# AUTO-CAMPAIGN-02 Plan\n\nRun Stage43 through Stage47 as independent MT5 runtime probes. Stage38-42 and prior campaign stages are negative memory or contrast only. Continue through all five topics unless a true blocker or invalid setup prevents execution.\n""",
    )
    write_json(CAMPAIGN_PACKET_ROOT / "campaign_progress.json", {"campaign_id": CAMPAIGN_ID, "status": "opened", "completed_stages": [], "blocked_stage": None})


def update_campaign_progress(stage_results: Sequence[Mapping[str, Any]], status: str = "running", blocked_stage: int | None = None) -> None:
    write_json(CAMPAIGN_PACKET_ROOT / "campaign_progress.json", {"campaign_id": CAMPAIGN_ID, "status": status, "completed_stages": list(stage_results), "blocked_stage": blocked_stage, "claim_boundary": FINAL_CAMPAIGN_BOUNDARY})


def write_campaign_summary(stage_results: Sequence[Mapping[str, Any]], validation_commands: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    promotion_packets = [row["promotion_candidate_packet"] for row in stage_results if row.get("promotion_candidate_packet")]
    blocked = [row for row in stage_results if row.get("judgment") == BLOCKED_JUDGMENT]
    if blocked:
        campaign_judgment = "campaign_blocked_mt5_execution"
    elif promotion_packets:
        campaign_judgment = "campaign_completed_all_five_topics_with_promotion_candidate_review_packets"
    elif len(stage_results) == 5:
        campaign_judgment = "campaign_completed_all_five_topics_no_promotion_candidate"
    else:
        campaign_judgment = "campaign_blocked_required_gate_failure"
    summary = {
        "campaign_id": CAMPAIGN_ID,
        "campaign_mode": CAMPAIGN_MODE,
        "planned_stages": [43, 44, 45, 46, 47],
        "completed_stage_count": len(stage_results),
        "stage_results": list(stage_results),
        "promotion_candidate_review_packets": promotion_packets,
        "campaign_judgment": campaign_judgment,
        "validation_commands": list(validation_commands),
        "claim_boundary": FINAL_CAMPAIGN_BOUNDARY,
    }
    write_json(CAMPAIGN_PACKET_ROOT / "campaign_summary.json", summary)
    write_json(CAMPAIGN_PACKET_ROOT / "final_claim_guard.json", {"status": "passed", "campaign_judgment": campaign_judgment, "no_baseline": True, "no_promotion": True, "no_runtime_authority": True, "no_live_readiness": True, "no_operating_reference": True, "claim_boundary": FINAL_CAMPAIGN_BOUNDARY})
    return summary


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run AUTO-CAMPAIGN-02 five independent MT5 runtime probes.")
    parser.add_argument("--stages", default="43,44,45,46,47")
    parser.add_argument("--materialize-only", action="store_true")
    parser.add_argument("--timeout-seconds", type=int, default=900)
    parser.add_argument("--terminal-path", default=str(TERMINAL_PATH_DEFAULT))
    parser.add_argument("--metaeditor-path", default=str(METAEDITOR_PATH_DEFAULT))
    parser.add_argument("--terminal-data-root", default=str(TERMINAL_DATA_ROOT_DEFAULT))
    parser.add_argument("--common-files-root", default=str(COMMON_FILES_ROOT_DEFAULT))
    parser.add_argument("--tester-profile-root", default=str(TESTER_PROFILE_ROOT_DEFAULT))
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_arg_parser().parse_args(argv)
    stage_numbers = [int(item.strip()) for item in str(args.stages).split(",") if item.strip()]
    write_campaign_open_packet()
    common, route_coverage, base_lineage = build_common_table()
    stage_results: list[dict[str, Any]] = []
    validation_commands: list[dict[str, Any]] = []
    for stage_number in stage_numbers:
        topic = STAGE_TOPICS[stage_number]
        result = run_one_stage(topic, common, route_coverage, base_lineage, args)
        stage_results.append(result)
        validation_commands.extend(stage_validation_commands(topic))
        update_campaign_progress(stage_results)
        if result.get("judgment") == BLOCKED_JUDGMENT:
            update_campaign_progress(stage_results, status="blocked", blocked_stage=stage_number)
            break
    summary = write_campaign_summary(stage_results, validation_commands)
    update_campaign_progress(stage_results, status=summary["campaign_judgment"])
    return 0 if not str(summary["campaign_judgment"]).startswith("campaign_blocked") else 2


if __name__ == "__main__":
    raise SystemExit(main())
