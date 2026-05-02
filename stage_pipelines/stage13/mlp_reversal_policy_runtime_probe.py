from __future__ import annotations

import argparse
import csv
import json
import math
import shutil
from collections import Counter, defaultdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

from foundation.control_plane.alpha_run_ledgers import build_mt5_alpha_ledger_rows, materialize_alpha_ledgers
from foundation.control_plane.ledger import RUN_REGISTRY_COLUMNS, io_path, json_ready, ledger_pairs, sha256_file_lf_normalized, upsert_csv_rows
from foundation.control_plane.mt5_tier_balance_completion import (
    COMMON_FILES_ROOT_DEFAULT,
    ROOT,
    TERMINAL_DATA_ROOT_DEFAULT,
    TERMINAL_PATH_DEFAULT,
    TESTER_PROFILE_ROOT_DEFAULT,
    attempt_payload,
    common_run_root,
    copy_to_common,
    execute_prepared_run,
)
from foundation.mt5 import runtime_support as mt5
from foundation.mt5.trade_report import parse_mt5_trade_report, pair_deals_into_trades


STAGE_NUMBER = 13
STAGE_ID = "13_model_family_challenge__mlp_training_effect"
RUN_NUMBER = "run04I"
RUN_ID = "run04I_mlp_reversal_policy_runtime_probe_v1"
PACKET_ID = "stage13_run04I_mlp_reversal_policy_runtime_probe_packet_v1"
SOURCE_RUN_ID = "run04F_mlp_direction_asymmetry_runtime_probe_v1"
SOURCE_ATTRIBUTION_RUN_ID = "run04H_mlp_direction_collision_attribution_v1"
EXPLORATION_LABEL = "stage13_MLPDirection__ReversalPolicy"
BOUNDARY = "reversal_policy_runtime_probe_only_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority"
STAGE_ROOT = ROOT / "stages" / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
PACKET_ROOT = RUN_ROOT / "packet"
SOURCE_ROOT = STAGE_ROOT / "02_runs" / SOURCE_RUN_ID
STAGE_LEDGER_PATH = STAGE_ROOT / "03_reviews/stage_run_ledger.csv"
PROJECT_LEDGER_PATH = ROOT / "docs/registers/alpha_run_ledger.csv"
RUN_REGISTRY_PATH = ROOT / "docs/registers/run_registry.csv"
REVIEW_PATH = STAGE_ROOT / "03_reviews/run04I_mlp_reversal_policy_runtime_probe_packet.md"
DECISION_PATH = ROOT / "docs/decisions/2026-05-02_stage13_mlp_reversal_policy_runtime_probe.md"
SELECTION_STATUS_PATH = STAGE_ROOT / "04_selected/selection_status.md"
REVIEW_INDEX_PATH = STAGE_ROOT / "03_reviews/review_index.md"
WORKSPACE_STATE_PATH = ROOT / "docs/workspace/workspace_state.yaml"
CURRENT_STATE_PATH = ROOT / "docs/context/current_working_state.md"
CHANGELOG_PATH = ROOT / "docs/workspace/changelog.md"
NO_SIGNAL_THRESHOLD = 1.01
MAX_HOLD_BARS = 9

POLICIES = (
    {
        "policy_id": "immediate_reverse",
        "label": "opposite_signal_immediate_reverse",
        "record_prefix": "mt5_tier_a_both_immediate_reverse",
        "reverse_on_opposite_signal": True,
        "close_only_on_opposite_signal": False,
    },
    {
        "policy_id": "close_only",
        "label": "opposite_signal_close_only",
        "record_prefix": "mt5_tier_a_both_close_only",
        "reverse_on_opposite_signal": False,
        "close_only_on_opposite_signal": True,
    },
)

SUMMARY_COLUMNS = (
    "policy_id",
    "split",
    "record_view",
    "net_profit",
    "profit_factor",
    "max_drawdown",
    "trade_count",
    "long_trade_count",
    "short_trade_count",
    "reverse_open_count",
    "close_on_opposite_count",
    "close_max_hold_count",
    "same_direction_hold_count",
    "external_status",
    "report_path",
)

ACTION_COLUMNS = ("policy_id", "split", "exec_action", "count")
SIDE_COLUMNS = ("policy_id", "split", "side", "trade_count", "net_profit", "avg_profit", "loss_count", "largest_loss")
DELTA_COLUMNS = ("split", "metric", "immediate_reverse", "close_only", "close_only_minus_reverse", "interpretation")


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def repo_path(value: str | Path) -> Path:
    path = Path(str(value))
    return path if path.is_absolute() else ROOT / path


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: csv_value(row.get(column)) for column in columns})


def csv_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, float):
        if not math.isfinite(value):
            return ""
        return f"{value:.6g}"
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(json_ready(value), ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return str(json_ready(value))


def copy_file(source: Path, destination: Path) -> dict[str, Any]:
    io_path(destination.parent).mkdir(parents=True, exist_ok=True)
    shutil.copy2(io_path(source), io_path(destination))
    return {"source": rel(source), "path": rel(destination), "sha256": sha256_file_lf_normalized(destination)}


def source_manifest() -> dict[str, Any]:
    return read_json(SOURCE_ROOT / "run_manifest.json")


def source_kpi() -> dict[str, Any]:
    return read_json(SOURCE_ROOT / "kpi_record.json")


def threshold_payload() -> dict[str, Any]:
    source = read_json(SOURCE_ROOT / "thresholds/threshold_handoff.json")
    payload = {
        "source_run_id": SOURCE_RUN_ID,
        "threshold_source_run_id": source.get("threshold_source_run_id"),
        "threshold_id": source.get("threshold_id", "q90_m000"),
        "tier_a_threshold": float(source["tier_a_threshold"]),
        "tier_b_fallback_threshold": float(source["tier_b_fallback_threshold"]),
        "no_signal_threshold": NO_SIGNAL_THRESHOLD,
        "min_margin": float(source.get("min_margin", 0.0)),
        "threshold_policy": "RUN04F q90 threshold reused for opposite-signal policy runtime probe without optimization",
        "boundary": "policy_probe_only_not_selected_threshold",
    }
    path = RUN_ROOT / "thresholds/threshold_handoff.json"
    write_json(path, payload)
    return {**payload, "path": rel(path), "sha256": sha256_file_lf_normalized(path)}


def materialize_source_inputs(manifest: Mapping[str, Any]) -> tuple[dict[str, Any], dict[str, Any], list[dict[str, Any]]]:
    source_model = repo_path(manifest["model_artifacts"]["tier_a_onnx"]["path"])
    model_copy = copy_file(source_model, RUN_ROOT / "models" / source_model.name)
    matrices: dict[str, Any] = {}
    for item in manifest["feature_matrices"]:
        path = repo_path(item["path"])
        if "tier_a_validation_is" in path.name:
            matrices["tier_a_validation_is"] = {**copy_file(path, RUN_ROOT / "features" / path.name), "feature_count": item["feature_count"], "feature_order_hash": item["feature_order_hash"]}
        if "tier_a_oos" in path.name:
            matrices["tier_a_oos"] = {**copy_file(path, RUN_ROOT / "features" / path.name), "feature_count": item["feature_count"], "feature_order_hash": item["feature_order_hash"]}
    common = common_run_root(STAGE_NUMBER, RUN_ID)
    common_copies = [copy_to_common(repo_path(model_copy["path"]), f"{common}/models/{source_model.name}", COMMON_FILES_ROOT_DEFAULT)]
    for matrix in matrices.values():
        common_copies.append(copy_to_common(repo_path(matrix["path"]), f"{common}/features/{Path(matrix['path']).name}", COMMON_FILES_ROOT_DEFAULT))
    return model_copy, matrices, common_copies


def source_dates(manifest: Mapping[str, Any], split: str) -> tuple[str, str]:
    for attempt in manifest["attempts"]:
        if attempt.get("split") == split:
            tester = attempt["ini"]["tester"]
            return str(tester["FromDate"]), str(tester["ToDate"])
    raise RuntimeError(f"missing source dates for {split}")


def make_attempts(
    *,
    manifest: Mapping[str, Any],
    model_copy: Mapping[str, Any],
    matrices: Mapping[str, Mapping[str, Any]],
    threshold: Mapping[str, Any],
) -> list[dict[str, Any]]:
    common = common_run_root(STAGE_NUMBER, RUN_ID)
    attempts: list[dict[str, Any]] = []
    for split in ("validation_is", "oos"):
        from_date, to_date = source_dates(manifest, split)
        matrix = matrices[f"tier_a_{split}"]
        for policy in POLICIES:
            attempt = attempt_payload(
                run_root=RUN_ROOT,
                run_id=RUN_ID,
                stage_number=STAGE_NUMBER,
                exploration_label=EXPLORATION_LABEL,
                attempt_name=f"tier_a_both_{policy['policy_id']}_{split}",
                tier=mt5.TIER_A,
                split=split,
                model_path=f"{common}/models/{Path(model_copy['path']).name}",
                model_id=f"{RUN_ID}_tier_a_both_{policy['policy_id']}",
                feature_path=f"{common}/features/{Path(matrix['path']).name}",
                feature_count=int(matrix["feature_count"]),
                feature_order_hash=str(matrix["feature_order_hash"]),
                short_threshold=float(threshold["tier_a_threshold"]),
                long_threshold=float(threshold["tier_a_threshold"]),
                min_margin=float(threshold["min_margin"]),
                invert_signal=False,
                from_date=from_date,
                to_date=to_date,
                primary_active_tier="tier_a",
                attempt_role="tier_only_total",
                record_view_prefix=str(policy["record_prefix"]),
                max_hold_bars=MAX_HOLD_BARS,
                common_root=common,
                reverse_on_opposite_signal=bool(policy["reverse_on_opposite_signal"]),
                close_only_on_opposite_signal=bool(policy["close_only_on_opposite_signal"]),
            )
            attempt["policy_id"] = policy["policy_id"]
            attempt["policy_label"] = policy["label"]
            attempts.append(attempt)
    return attempts


def execute_or_materialize(prepared: Mapping[str, Any], args: argparse.Namespace) -> dict[str, Any]:
    if args.materialize_only:
        return {**dict(prepared), "compile": {"status": "not_attempted_materialize_only"}, "execution_results": [], "strategy_tester_reports": [], "mt5_kpi_records": [], "external_verification_status": "blocked", "judgment": "blocked_materialize_only_no_mt5_execution"}
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
        return {**dict(prepared), "compile": {"status": "exception_or_not_completed"}, "execution_results": [], "strategy_tester_reports": [], "mt5_kpi_records": [], "external_verification_status": "blocked", "judgment": "blocked_reversal_policy_runtime_probe", "failure": {"type": type(exc).__name__, "message": str(exc)}}
    result = dict(result)
    result["judgment"] = "inconclusive_reversal_policy_runtime_probe_completed" if result.get("external_verification_status") == "completed" else "blocked_reversal_policy_runtime_probe"
    return result


def read_telemetry(path_value: str) -> list[dict[str, str]]:
    path = COMMON_FILES_ROOT_DEFAULT / Path(path_value)
    if not io_path(path).exists():
        return []
    rows: list[dict[str, str]] = []
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.reader(handle)
        header = next(reader)
        for raw in reader:
            if len(raw) < len(header):
                raw = raw + [""] * (len(header) - len(raw))
            row = dict(zip(header, raw[: len(header)]))
            if row.get("record_type") == "cycle":
                rows.append(row)
    return rows


def analyze_telemetry(attempts: Sequence[Mapping[str, Any]]) -> tuple[list[dict[str, Any]], dict[str, Counter[str]]]:
    action_rows: list[dict[str, Any]] = []
    counters: dict[str, Counter[str]] = {}
    for attempt in attempts:
        counter = Counter(row.get("exec_action", "") for row in read_telemetry(str(attempt["common_telemetry_path"])))
        key = str(attempt["attempt_name"])
        counters[key] = counter
        for action, count in sorted(counter.items()):
            action_rows.append({"policy_id": attempt["policy_id"], "split": attempt["split"], "exec_action": action, "count": count})
    return action_rows, counters


def analyze_trades(records: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for record in records:
        metrics = record.get("metrics", {})
        report_path = metrics.get("report_path")
        if not report_path:
            continue
        trades = pair_deals_into_trades(parse_mt5_trade_report(Path(str(report_path)))["deals"])
        policy_id = policy_from_record(str(record["record_view"]))
        for side, direction in (("long", "buy"), ("short", "sell")):
            values = [float(trade.net_profit) for trade in trades if trade.direction == direction]
            rows.append({"policy_id": policy_id, "split": record["split"], "side": side, "trade_count": len(values), "net_profit": sum(values), "avg_profit": mean(values), "loss_count": sum(1 for value in values if value < 0.0), "largest_loss": min(values) if values else None})
    return rows


def build_policy_summary(result: Mapping[str, Any], attempts: Sequence[Mapping[str, Any]], counters: Mapping[str, Counter[str]]) -> list[dict[str, Any]]:
    by_attempt = {str(attempt["attempt_name"]): attempt for attempt in attempts}
    rows: list[dict[str, Any]] = []
    for record in result.get("mt5_kpi_records", []):
        metrics = record.get("metrics", {})
        policy_id = policy_from_record(str(record["record_view"]))
        attempt_name = f"tier_a_both_{policy_id}_{record['split']}"
        actions = counters.get(attempt_name, Counter())
        rows.append(
            {
                "policy_id": policy_id,
                "split": record.get("split"),
                "record_view": record.get("record_view"),
                "net_profit": metrics.get("net_profit"),
                "profit_factor": metrics.get("profit_factor"),
                "max_drawdown": metrics.get("max_drawdown_amount"),
                "trade_count": metrics.get("trade_count"),
                "long_trade_count": metrics.get("long_trade_count"),
                "short_trade_count": metrics.get("short_trade_count"),
                "reverse_open_count": actions.get("reverse_open_long", 0) + actions.get("reverse_open_short", 0),
                "close_on_opposite_count": actions.get("close_on_opposite", 0),
                "close_max_hold_count": actions.get("close_max_hold", 0),
                "same_direction_hold_count": actions.get("hold_same_direction", 0),
                "external_status": record.get("status"),
                "report_path": metrics.get("report_path") or by_attempt.get(attempt_name, {}).get("ini", {}).get("path"),
            }
        )
    return rows


def build_delta_rows(policy_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    by_split_policy = {(row["split"], row["policy_id"]): row for row in policy_rows}
    for split in ("validation_is", "oos"):
        reverse = by_split_policy.get((split, "immediate_reverse"), {})
        close = by_split_policy.get((split, "close_only"), {})
        for metric in ("net_profit", "profit_factor", "max_drawdown", "trade_count"):
            rev = as_float(reverse.get(metric))
            clo = as_float(close.get(metric))
            delta = None if rev is None or clo is None else clo - rev
            rows.append({"split": split, "metric": metric, "immediate_reverse": rev, "close_only": clo, "close_only_minus_reverse": delta, "interpretation": interpretation(metric, delta)})
    return rows


def write_ledgers(result: Mapping[str, Any], threshold: Mapping[str, Any], delta_rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    rows = [
        scope_row("Tier B", "tier_b_out_of_scope", threshold),
        scope_row("Tier A+B", "tier_abb_out_of_scope", threshold),
    ]
    rows.extend(
        build_mt5_alpha_ledger_rows(
            run_id=RUN_ID,
            stage_id=STAGE_ID,
            mt5_kpi_records=result.get("mt5_kpi_records", []),
            run_output_root=Path(rel(RUN_ROOT)),
            external_verification_status=str(result.get("external_verification_status")),
        )
    )
    for row in delta_rows:
        if row["metric"] == "net_profit":
            rows.append(
                {
                    "ledger_row_id": f"{RUN_ID}__policy_delta_{row['split']}",
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "subrun_id": f"policy_delta_{row['split']}",
                    "parent_run_id": RUN_ID,
                    "record_view": f"policy_delta_{row['split']}",
                    "tier_scope": "Tier A",
                    "kpi_scope": "opposite_signal_policy_delta",
                    "scoreboard_lane": "runtime_probe",
                    "status": "completed",
                    "judgment": "inconclusive_reversal_policy_delta",
                    "path": rel(RUN_ROOT / "policy_delta_summary.csv"),
                    "primary_kpi": ledger_pairs((("reverse_net", row["immediate_reverse"]), ("close_only_net", row["close_only"]), ("delta", row["close_only_minus_reverse"]))),
                    "guardrail_kpi": ledger_pairs((("threshold_id", threshold["threshold_id"]), ("boundary", "policy_probe_only"))),
                    "external_verification_status": str(result.get("external_verification_status")),
                    "notes": "Close-only minus immediate-reverse under same RUN04F model and q90 threshold.",
                }
            )
    ledger_outputs = materialize_alpha_ledgers(stage_run_ledger_path=STAGE_LEDGER_PATH, project_alpha_ledger_path=PROJECT_LEDGER_PATH, rows=rows)
    registry_output = upsert_csv_rows(
        RUN_REGISTRY_PATH,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "reversal_policy_runtime_probe",
                "status": "reviewed" if result.get("external_verification_status") == "completed" else "payload_only",
                "judgment": result.get("judgment"),
                "path": rel(RUN_ROOT),
                "notes": ledger_pairs((("source_run", SOURCE_RUN_ID), ("threshold_id", threshold["threshold_id"]), ("policies", "immediate_reverse;close_only"), ("external_verification", result.get("external_verification_status")), ("boundary", "runtime_probe_only"))),
            }
        ],
        key="run_id",
    )
    return {"ledger_outputs": ledger_outputs, "run_registry_output": registry_output}


def scope_row(tier_scope: str, suffix: str, threshold: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "ledger_row_id": f"{RUN_ID}__{suffix}",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": suffix,
        "parent_run_id": RUN_ID,
        "record_view": suffix,
        "tier_scope": tier_scope,
        "kpi_scope": "claim_scope_boundary",
        "scoreboard_lane": "runtime_probe",
        "status": "completed",
        "judgment": "out_of_scope_by_claim_reversal_policy_probe",
        "path": threshold["path"],
        "primary_kpi": ledger_pairs((("source_run", SOURCE_RUN_ID), ("threshold_id", threshold["threshold_id"]))),
        "guardrail_kpi": ledger_pairs((("boundary", "tier_a_both_policy_only"),)),
        "external_verification_status": "out_of_scope_by_claim",
        "notes": "RUN04I compares Tier A both-direction opposite-signal policy only.",
    }


def build_summary(
    *,
    created_at: str,
    manifest: Mapping[str, Any],
    threshold: Mapping[str, Any],
    model_copy: Mapping[str, Any],
    matrices: Mapping[str, Mapping[str, Any]],
    prepared: Mapping[str, Any],
    result: Mapping[str, Any],
) -> dict[str, Any]:
    action_rows, counters = analyze_telemetry(prepared["attempts"])
    policy_rows = build_policy_summary(result, prepared["attempts"], counters)
    side_rows = analyze_trades(result.get("mt5_kpi_records", []))
    delta_rows = build_delta_rows(policy_rows)
    ledgers = write_ledgers(result, threshold, delta_rows)
    summary = {
        "packet_id": PACKET_ID,
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "run_number": RUN_NUMBER,
        "source_run_id": SOURCE_RUN_ID,
        "source_attribution_run_id": SOURCE_ATTRIBUTION_RUN_ID,
        "created_at_utc": created_at,
        "external_verification_status": result.get("external_verification_status"),
        "judgment": result.get("judgment"),
        "boundary": BOUNDARY,
        "threshold": threshold,
        "source_model_spec": manifest.get("spec", {}),
        "model_artifact": model_copy,
        "feature_matrices": matrices,
        "policy_summary": policy_rows,
        "telemetry_action_summary": action_rows,
        "side_summary": side_rows,
        "policy_delta_summary": delta_rows,
        "ledger_outputs": ledgers,
        "failure": result.get("failure"),
    }
    write_csv(RUN_ROOT / "policy_runtime_summary.csv", SUMMARY_COLUMNS, policy_rows)
    write_csv(RUN_ROOT / "telemetry_action_summary.csv", ACTION_COLUMNS, action_rows)
    write_csv(RUN_ROOT / "policy_side_summary.csv", SIDE_COLUMNS, side_rows)
    write_csv(RUN_ROOT / "policy_delta_summary.csv", DELTA_COLUMNS, delta_rows)
    return summary


def write_run_files(summary: Mapping[str, Any], prepared: Mapping[str, Any], result: Mapping[str, Any]) -> None:
    manifest = {
        "run_id": RUN_ID,
        "packet_id": PACKET_ID,
        "stage_id": STAGE_ID,
        "run_number": RUN_NUMBER,
        "source_run_id": SOURCE_RUN_ID,
        "source_attribution_run_id": SOURCE_ATTRIBUTION_RUN_ID,
        "model_family": "sklearn_mlpclassifier_reversal_policy_probe",
        "exploration_label": EXPLORATION_LABEL,
        "stage_inheritance": "independent_no_stage10_11_12_run_baseline_seed_or_reference",
        "boundary": BOUNDARY,
        "attempts": prepared["attempts"],
        "common_copies": prepared["common_copies"],
        "compile": result.get("compile", {}),
        "execution_results": result.get("execution_results", []),
        "strategy_tester_reports": result.get("strategy_tester_reports", []),
        "external_verification_status": result.get("external_verification_status"),
        "judgment": result.get("judgment"),
    }
    kpi = {
        "run_id": RUN_ID,
        "packet_id": PACKET_ID,
        "stage_id": STAGE_ID,
        "threshold": summary["threshold"],
        "mt5": {"scoreboard_lane": "runtime_probe", "external_verification_status": result.get("external_verification_status"), "kpi_records": result.get("mt5_kpi_records", [])},
        "policy_summary": summary["policy_summary"],
        "policy_delta_summary": summary["policy_delta_summary"],
        "judgment": result.get("judgment"),
        "boundary": BOUNDARY,
    }
    write_json(RUN_ROOT / "run_manifest.json", manifest)
    write_json(RUN_ROOT / "kpi_record.json", kpi)
    write_json(RUN_ROOT / "summary.json", summary)
    write_json(PACKET_ROOT / "skill_receipts.json", skill_receipts(summary))
    write_json(PACKET_ROOT / "command_result.json", {"run_id": RUN_ID, "summary": summary})
    write_md(PACKET_ROOT / "work_packet.md", work_packet_markdown(summary))
    report = report_markdown(summary)
    write_md(RUN_ROOT / "reports/result_summary.md", report)
    write_md(REVIEW_PATH, report)
    write_md(DECISION_PATH, decision_markdown(summary))
    sync_docs(summary)


def report_markdown(summary: Mapping[str, Any]) -> str:
    rows = summary["policy_summary"]
    delta = summary["policy_delta_summary"]
    oos_net = next((row for row in delta if row["split"] == "oos" and row["metric"] == "net_profit"), {})
    lines = [
        f"# {RUN_ID} 결과 요약(Result Summary, 결과 요약)",
        "",
        f"- status(상태): `{summary['external_verification_status']}`",
        f"- judgment(판정): `{summary['judgment']}`",
        f"- source run(원천 실행): `{SOURCE_RUN_ID}`",
        f"- boundary(경계): `{BOUNDARY}`",
        f"- OOS net delta(표본외 순수익 차이, close-only minus reverse): `{fmt(oos_net.get('close_only_minus_reverse'))}`",
        "",
        "## Policy KPI(정책 핵심 지표)",
        "",
        "| policy(정책) | split(분할) | net(순수익) | PF(수익 팩터) | DD(손실) | trades(거래 수) | long/short(매수/매도) | reverse(반전) | close opposite(반대 신호 청산) |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in rows:
        lines.append(f"| {row['policy_id']} | {row['split']} | {fmt(row['net_profit'])} | {fmt(row['profit_factor'])} | {fmt(row['max_drawdown'])} | {row['trade_count']} | {row['long_trade_count']}/{row['short_trade_count']} | {row['reverse_open_count']} | {row['close_on_opposite_count']} |")
    lines.extend(["", "## Delta(차이)", "", "| split(분할) | metric(지표) | reverse(즉시 반전) | close-only(청산만) | delta(차이) |", "|---|---|---:|---:|---:|"])
    for row in delta:
        lines.append(f"| {row['split']} | {row['metric']} | {fmt(row['immediate_reverse'])} | {fmt(row['close_only'])} | {fmt(row['close_only_minus_reverse'])} |")
    lines.extend(["", "효과(effect, 효과): 같은 MLP(다층 퍼셉트론) 모델과 q90 threshold(q90 임계값)에서 opposite signal policy(반대 신호 정책)만 바꿨으므로, 차이는 정책 민감도 단서로만 읽는다. alpha quality(알파 품질), baseline(기준선), promotion(승격)은 아니다."])
    return "\n".join(lines)


def decision_markdown(summary: Mapping[str, Any]) -> str:
    oos_net = next((row for row in summary["policy_delta_summary"] if row["split"] == "oos" and row["metric"] == "net_profit"), {})
    return "\n".join(
        [
            "# 2026-05-02 Stage13 MLP Reversal Policy Runtime Probe",
            "",
            f"- run(실행): `{RUN_ID}`",
            f"- source(원천): `{SOURCE_RUN_ID}`",
            "- comparison(비교): immediate reverse(즉시 반전) vs close-only(청산만)",
            f"- OOS close-only minus reverse(표본외 청산만-즉시반전): `{fmt(oos_net.get('close_only_minus_reverse'))}`",
            f"- boundary(경계): `{BOUNDARY}`",
            "",
            "효과(effect, 효과): 다음 탐색에서 양방향 정책을 유지할지, 청산만을 보조 단서로 남길지 결정할 수 있다.",
        ]
    )


def work_packet_markdown(summary: Mapping[str, Any]) -> str:
    return "\n".join(
        [
            f"# {PACKET_ID}",
            "",
            "- primary_family(주 작업군): `runtime_probe(런타임 탐침)`",
            "- primary_skill(주 스킬): `obsidian-runtime-parity(런타임 동등성)`",
            "- hypothesis(가설): RUN04H(실행 04H)의 both(양방향) 손상은 immediate reverse(즉시 반전)보다 close-only(청산만)에서 완화될 수 있다.",
            "- controls(고정값): RUN04F(실행 04F) MLP(다층 퍼셉트론) ONNX(온닉스), Tier A(티어 A) feature matrix(피처 행렬), q90 threshold(q90 임계값), max hold 9 bars(최대 보유 9봉).",
            "- changed_variables(변경값): `InpReverseOnOppositeSignal`, `InpCloseOnlyOnOppositeSignal`.",
            f"- boundary(경계): `{BOUNDARY}`",
            "",
            "효과(effect, 효과): 정책 차이를 외부 MT5(메타트레이더5) tester output(테스터 출력)으로 남긴다.",
        ]
    )


def skill_receipts(summary: Mapping[str, Any]) -> list[dict[str, Any]]:
    status = "completed" if summary["external_verification_status"] == "completed" else "blocked"
    return [
        {"packet_id": PACKET_ID, "skill": "obsidian-experiment-design", "status": status, "hypothesis": "Close-only opposite-signal policy may reduce both-direction reversal damage.", "baseline": "Immediate reverse policy using RUN04F model and q90 threshold.", "changed_variables": ["InpReverseOnOppositeSignal", "InpCloseOnlyOnOppositeSignal"], "invalid_conditions": ["missing MT5 report", "EA compile failure", "telemetry missing"], "evidence_plan": [rel(RUN_ROOT / "policy_runtime_summary.csv"), rel(RUN_ROOT / "policy_delta_summary.csv")]},
        {"packet_id": PACKET_ID, "skill": "obsidian-runtime-parity", "status": status, "python_artifact": summary["model_artifact"]["source"], "runtime_artifact": summary["model_artifact"]["path"], "compared_surface": "Same ONNX and feature CSV with two MT5 execution policies.", "parity_level": "runtime_probe", "tester_identity": "MT5 Strategy Tester US100 M5 model 4 deposit 500 leverage 1:100", "missing_evidence": [] if status == "completed" else ["completed MT5 reports"], "allowed_claims": ["runtime_probe_completed"], "forbidden_claims": ["runtime_authority", "promotion", "baseline"]},
        {"packet_id": PACKET_ID, "skill": "obsidian-backtest-forensics", "status": status, "tester_report": rel(RUN_ROOT / "mt5/reports"), "tester_settings": rel(RUN_ROOT / "mt5"), "spread_commission_slippage": "Same tester profile as RUN04F; no new cost model.", "trade_list_identity": "Four MT5 reports and common telemetry CSV files.", "forensic_gaps": [] if status == "completed" else ["blocked external verification"]},
        {"packet_id": PACKET_ID, "skill": "obsidian-artifact-lineage", "status": status, "source_inputs": [rel(SOURCE_ROOT / "run_manifest.json"), rel(SOURCE_ROOT / "kpi_record.json")], "produced_artifacts": [rel(RUN_ROOT / "summary.json"), rel(RUN_ROOT / "policy_runtime_summary.csv"), rel(REVIEW_PATH)], "raw_evidence": [rel(RUN_ROOT / "mt5/reports")], "machine_readable": [rel(RUN_ROOT / "kpi_record.json"), rel(RUN_ROOT / "policy_delta_summary.csv")], "human_readable": [rel(REVIEW_PATH), rel(DECISION_PATH)], "hashes_or_missing_reasons": "run_manifest and copied source artifacts record hashes", "lineage_boundary": BOUNDARY},
        {"packet_id": PACKET_ID, "skill": "obsidian-result-judgment", "status": status, "judgment_boundary": summary["judgment"], "allowed_claims": ["opposite_signal_policy_runtime_probe"], "forbidden_claims": ["alpha_quality", "baseline", "promotion", "runtime_authority"], "evidence_used": [rel(RUN_ROOT / "policy_runtime_summary.csv"), rel(RUN_ROOT / "policy_delta_summary.csv")]},
    ]


def sync_docs(summary: Mapping[str, Any]) -> None:
    state = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    state = state.replace("active_run04H_mlp_direction_collision_attribution", "active_run04I_mlp_reversal_policy_runtime_probe")
    block = (
        "stage13_mlp_reversal_policy_runtime_probe:\n"
        f"  run_id: {RUN_ID}\n"
        f"  status: {summary['external_verification_status']}\n"
        f"  judgment: {summary['judgment']}\n"
        f"  boundary: {BOUNDARY}\n"
        f"  source_run_id: {SOURCE_RUN_ID}\n"
        f"  report_path: {rel(REVIEW_PATH)}\n"
    )
    if "stage13_mlp_reversal_policy_runtime_probe:" not in state:
        state = state.replace("stage01_raw_m5_inventory:\n", block + "stage01_raw_m5_inventory:\n")
    io_path(WORKSPACE_STATE_PATH).write_text(state, encoding="utf-8")

    current = io_path(CURRENT_STATE_PATH).read_text(encoding="utf-8-sig")
    current = current.replace("current run(현재 실행): `run04H_mlp_direction_collision_attribution_v1`", f"current run(현재 실행): `{RUN_ID}`")
    latest = f"Stage13(13단계)의 현재 실행(current run, 현재 실행)은 `{RUN_ID}`이고, immediate reverse(즉시 반전)와 close-only(청산만) opposite signal policy(반대 신호 정책)를 MT5(메타트레이더5)에서 비교했다.\n\n효과(effect, 효과): RUN04H(실행 04H)에서 보인 reversal damage(반전 손상)를 정책 차이로 확인했다."
    marker = "## 쉬운 설명(Plain Read, 쉬운 설명)"
    if marker in current and "## Latest Stage 13 Update" in current:
        head = current.split("## Latest Stage 13 Update", 1)[0]
        after = current.split(marker, 1)[1]
        current = head + "## Latest Stage 13 Update(최신 Stage 13 업데이트)\n\n" + latest + "\n" + marker + after
    io_path(CURRENT_STATE_PATH).write_text(current, encoding="utf-8-sig")

    write_md(
        SELECTION_STATUS_PATH,
        "\n".join(
            [
                "# Stage 13 Selection Status",
                "",
                "## Current Read(현재 판독)",
                "",
                f"- stage(단계): `{STAGE_ID}`",
                "- status(상태): `reviewed_reversal_policy_runtime_probe_completed(반전 정책 런타임 탐침 검토 완료)`",
                "- model family(모델 계열): `MLPClassifier(다층 퍼셉트론 분류기)`",
                "- exploration depth(탐색 깊이): `opposite_signal_policy_only(반대 신호 정책만)`",
                f"- current run(현재 실행): `{RUN_ID}`",
                "- selected operating reference/promotion/baseline(선택 운영 기준/승격/기준선): `none(없음)`",
                f"- external verification status(외부 검증 상태): `{summary['external_verification_status']}`",
                f"- judgment(판정): `{summary['judgment']}`",
            ]
        ),
    )
    review = io_path(REVIEW_INDEX_PATH).read_text(encoding="utf-8-sig")
    if RUN_ID not in review:
        review = review.rstrip() + f"\n- `{RUN_ID}`: `{summary['judgment']}`, report(보고서) `{rel(REVIEW_PATH)}`\n"
    io_path(REVIEW_INDEX_PATH).write_text(review, encoding="utf-8-sig")
    changelog = io_path(CHANGELOG_PATH).read_text(encoding="utf-8-sig")
    line = f"\n- 2026-05-02: Added `{RUN_ID}` reversal policy runtime probe(반전 정책 런타임 탐침); no alpha quality(알파 품질), baseline(기준선), or promotion(승격) claim.\n"
    if RUN_ID not in changelog:
        changelog += line
    io_path(CHANGELOG_PATH).write_text(changelog, encoding="utf-8-sig")


def policy_from_record(record_view: str) -> str:
    return "close_only" if "close_only" in record_view else "immediate_reverse"


def as_float(value: Any) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def mean(values: Sequence[float]) -> float | None:
    return sum(values) / len(values) if values else None


def fmt(value: Any) -> str:
    number = as_float(value)
    return "NA" if number is None else f"{number:.2f}"


def interpretation(metric: str, delta: float | None) -> str:
    if delta is None:
        return "missing"
    if metric == "max_drawdown":
        return "lower_is_better" if delta < 0 else "higher_drawdown"
    if metric in {"net_profit", "profit_factor"}:
        return "close_only_better" if delta > 0 else "immediate_reverse_better"
    return "count_delta"


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Stage13 MLP reversal policy runtime probe.")
    parser.add_argument("--materialize-only", action="store_true")
    parser.add_argument("--timeout-seconds", type=int, default=900)
    parser.add_argument("--terminal-path", default=str(TERMINAL_PATH_DEFAULT))
    parser.add_argument("--metaeditor-path", default=r"C:\Program Files\MetaTrader 5\MetaEditor64.exe")
    args = parser.parse_args(argv)
    created_at = utc_now()
    manifest = source_manifest()
    threshold = threshold_payload()
    model_copy, matrices, common_copies = materialize_source_inputs(manifest)
    attempts = make_attempts(manifest=manifest, model_copy=model_copy, matrices=matrices, threshold=threshold)
    prepared = {"run_id": RUN_ID, "run_root": RUN_ROOT.as_posix(), "stage_id": STAGE_ID, "source_run_id": SOURCE_RUN_ID, "attempts": attempts, "common_copies": common_copies, "feature_matrices": list(matrices.values()), "route_coverage": source_kpi().get("tier_b_context_summary", {})}
    result = execute_or_materialize(prepared, args)
    summary = build_summary(created_at=created_at, manifest=manifest, threshold=threshold, model_copy=model_copy, matrices=matrices, prepared=prepared, result=result)
    write_run_files(summary, prepared, result)
    print(json.dumps(json_ready(summary), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
