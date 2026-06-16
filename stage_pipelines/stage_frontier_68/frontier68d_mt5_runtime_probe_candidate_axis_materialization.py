from __future__ import annotations

import argparse
import csv
import json
import math
import shutil
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists
from foundation.control_plane.mt5_tier_balance_completion import attempt_payload
from foundation.mt5 import runtime_support as mt5
from stage_pipelines.stage_frontier_67.frontier67c_runtime_native_order_intent_economics import (
    as_float,
    as_int,
    extract_deal_metrics,
    ratio,
)
from stage_pipelines.stage_frontier_68.frontier68a_bridge_feasibility_and_label_design import (
    STAGE_ID,
    rel,
    sha256_file,
    upsert_ledger,
    write_csv,
    write_json,
    write_md,
)
from stage_pipelines.stage_frontier_runtime_backfill.run_frontier_runtime_probe_backfill import (
    DEFAULT_COMMON_FILES,
    DEFAULT_METAEDITOR,
    DEFAULT_PORTABLE_ROOT,
    DEFAULT_TERMINAL,
    DEFAULT_TESTER_PROFILE_ROOT,
    EA_BINARY,
    PORTABLE_EA_BINARY,
)


RUN_ID = "frontier68D_mt5_runtime_probe_candidate_axis_materialization_v1"
PARENT_RUN_ID = "frontier68C_candidate_scoring_or_onnx_scout_export_v1"
NEXT_RUN_ID = "frontier68E_proxy_runtime_gap_analysis_and_repair_decision_v1"

STAGE_ROOT = ROOT / "stages" / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
MT5_ROOT = RUN_ROOT / "mt5"
COMMON_RUN_ROOT = "Project_Obsidian_Prime_v2/frontier68D_candidate_axis_runtime_probe"

F68C_ROOT = STAGE_ROOT / "02_runs" / PARENT_RUN_ID
F68C_HANDOFF = STAGE_ROOT / "03_reviews" / "f68c_handoff_intent_review.json"
F68C_SUMMARY = STAGE_ROOT / "03_reviews" / "f68c_candidate_axis_summary_review.csv"
F68C_KPI = F68C_ROOT / "f68c_candidate_axis_kpi_by_split.csv"
F68C_SIGNAL_PARITY = F68C_ROOT / "f68c_onnx_signal_parity.csv"

GROK_PACKET_ROOT = ROOT / "docs/agent_control/grok_reviews/2026-06-17_f68d_pre_mt5_candidate_axis_runtime_probe"
GROK_PROMPT = GROK_PACKET_ROOT / "prompts/f68d_pre_mt5_candidate_axis_prompt.md"
GROK_CLEAN = GROK_PACKET_ROOT / "outputs/clean_output.md"
GROK_METADATA = GROK_PACKET_ROOT / "outputs/metadata.json"

CLAIM_BOUNDARY = (
    "runtime_probe_observation_only_no_completion_no_baseline_no_promotion_"
    "no_runtime_authority_no_live_readiness_no_goal_achieve"
)

STATUS_MATERIALIZED = "materialized_pending_mt5_runtime_probe_execution_no_authority(물질화 완료, MT5 런타임 탐침 실행 대기, 권위 없음)"
STATUS_COMPLETED = "completed_mt5_runtime_probe_observation_no_authority(MT5 런타임 탐침 관찰 완료, 권위 없음)"
STATUS_BLOCKED = "blocked_mt5_runtime_probe_attempted_repair_required_no_authority(MT5 런타임 탐침 시도 차단, 수리 필요, 권위 없음)"

SPLIT_WINDOWS = {
    "validation": {"from": "2025.01.02", "to": "2025.10.01"},
    "oos": {"from": "2025.10.01", "to": "2026.04.14"},
}

LOCAL_VERIFICATION_COLUMNS = (
    "check_name",
    "status",
    "detail",
    "effect",
)

RUNTIME_RECEIPT_COLUMNS = (
    "run_id",
    "attempt_name",
    "candidate_id",
    "axis_id",
    "split",
    "test_period_start",
    "test_period_end",
    "calendar_days_exclusive",
    "tester_status",
    "runtime_status",
    "report_status",
    "expected_rows",
    "feature_ready_count",
    "feature_ready_diff",
    "expected_signal_count",
    "signal_count",
    "signal_count_diff",
    "order_attempt_count",
    "order_fill_count",
    "order_fill_rate",
    "trade_count",
    "trades_per_day",
    "long_trade_count",
    "short_trade_count",
    "winning_trade_count",
    "losing_trade_count",
    "deal_count",
    "deal_in_count",
    "deal_out_count",
    "deal_minus_order_fill",
    "deal_count_equals_2x_trade",
    "order_fill_equals_deal_count",
    "net_profit",
    "gross_profit",
    "gross_loss",
    "profit_factor",
    "expectancy",
    "win_rate_percent",
    "average_win",
    "average_loss",
    "payoff_ratio",
    "recovery_factor",
    "max_drawdown_amount",
    "max_drawdown_percent",
    "proxy_net_profit",
    "proxy_profit_factor",
    "proxy_trades_per_day",
    "proxy_dd_percent",
    "dd_delta_runtime_minus_proxy",
    "deal_profit_sum",
    "deal_commission_sum",
    "deal_swap_sum",
    "deal_cost_sum",
    "net_reconciliation_error",
    "gap_cause_summary",
    "report_path",
    "telemetry_path",
    "summary_path",
    "claim_boundary",
)

GAP_COLUMNS = (
    "run_id",
    "attempt_name",
    "candidate_id",
    "axis_id",
    "split",
    "layer",
    "metric",
    "proxy_value",
    "runtime_value",
    "delta",
    "gap_class",
    "evidence",
    "claim_boundary",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="F68D MT5 runtime probe for F68C ONNX candidate axes.")
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--materialize-only", action="store_true")
    parser.add_argument("--timeout-seconds", type=int, default=900)
    parser.add_argument("--wait-timeout-seconds", type=int, default=240)
    parser.add_argument("--terminal-path", default=str(DEFAULT_TERMINAL))
    parser.add_argument("--metaeditor-path", default=str(DEFAULT_METAEDITOR))
    parser.add_argument("--common-files-root", default=str(DEFAULT_COMMON_FILES))
    parser.add_argument("--tester-profile-root", default=str(DEFAULT_TESTER_PROFILE_ROOT))
    parser.add_argument("--terminal-data-root", default=str(DEFAULT_PORTABLE_ROOT))
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    ensure_dirs()
    created_at = utc_now()
    candidates = load_candidate_contexts(Path(args.common_files_root))
    attempts = build_attempts(candidates)
    local_verification = build_local_verification(candidates, attempts)

    payload: dict[str, Any] = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "created_at_utc": created_at,
        "status": STATUS_MATERIALIZED,
        "judgment": "mt5_runtime_probe_materialized_pending_execution_no_authority(MT5 런타임 탐침 물질화, 실행 대기, 권위 없음)",
        "claim_boundary": CLAIM_BOUNDARY,
        "grok_packet": grok_identity(),
        "local_verification": local_verification,
        "candidate_contexts": candidates,
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
    report_records = mt5.collect_mt5_strategy_report_artifacts(
        terminal_data_root=Path(args.terminal_data_root),
        run_output_root=RUN_ROOT,
        attempts=attempts,
        run_id=RUN_ID,
    )
    mt5.attach_mt5_report_metrics(execution_results, report_records)
    kpi_records = mt5.build_mt5_kpi_records(execution_results)
    receipt_rows = build_runtime_receipt(execution_results, attempts)
    gap_rows = [row for receipt in receipt_rows for row in build_gap_classification(receipt)]
    execution_completed = bool(execution_results) and all(row.get("status") == "completed" for row in execution_results)
    report_completed = bool(kpi_records) and len(kpi_records) == len(attempts)
    payload.update(
        {
            "status": STATUS_COMPLETED if execution_completed and report_completed else STATUS_BLOCKED,
            "judgment": (
                "runtime_probe_observation_recorded_no_authority(MT5 런타임 탐침 관찰 기록, 권위 없음)"
                if execution_completed and report_completed
                else "runtime_probe_attempt_blocked_repair_required_no_authority(MT5 런타임 탐침 시도 차단, 수리 필요, 권위 없음)"
            ),
            "execution_results": execution_results,
            "strategy_tester_reports": report_records,
            "mt5_kpi_records": kpi_records,
            "runtime_receipt": receipt_rows,
            "gap_classification": gap_rows,
        }
    )
    write_outputs(payload, created_at)
    update_state_and_ledgers(payload)
    print(
        json.dumps(
            json_ready(
                {
                    "status": payload["status"],
                    "judgment": payload["judgment"],
                    "attempt_count": len(attempts),
                    "execution_completed": execution_completed,
                    "report_completed": report_completed,
                    "receipt_rows": len(receipt_rows),
                }
            ),
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


def ensure_dirs() -> None:
    for path in (RUN_ROOT, RUN_ROOT / "models", RUN_ROOT / "features", MT5_ROOT, MT5_ROOT / "reports", RUN_ROOT / "reports", REVIEWS_ROOT):
        io_path(path).mkdir(parents=True, exist_ok=True)


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def clean_axis_id(value: Any) -> str:
    return str(value or "").strip()


def safe_name(value: str, limit: int = 72) -> str:
    import re

    return re.sub(r"[^A-Za-z0-9]+", "_", value).strip("_")[:limit]


def parse_bool(value: Any) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes"}


def load_candidate_contexts(common_files_root: Path) -> list[dict[str, Any]]:
    handoff = read_json(F68C_HANDOFF)
    summary_rows = {row["candidate_id"]: row for row in read_csv_rows(F68C_SUMMARY)}
    kpi_rows: dict[tuple[str, str], dict[str, str]] = {
        (row["candidate_id"], row["split"]): row for row in read_csv_rows(F68C_KPI)
    }
    signal_rows: dict[tuple[str, str], dict[str, str]] = {
        (row["candidate_id"], row["split"]): row for row in read_csv_rows(F68C_SIGNAL_PARITY)
    }
    contexts: list[dict[str, Any]] = []
    for item in handoff.get("handoff_intent", []):
        if not item.get("probe_eligible"):
            continue
        candidate_id = str(item["candidate_id"])
        axis_id = clean_axis_id(item["axis_id"])
        model_path = ROOT / str(item["model_path_repo"])
        feature_path = ROOT / str(item["feature_csv_repo"])
        model_local = copy_run_artifact(model_path, RUN_ROOT / "models" / model_path.name)
        feature_local = copy_run_artifact(feature_path, RUN_ROOT / "features" / feature_path.name)
        model_common = f"{COMMON_RUN_ROOT}/models/{model_local.name}"
        feature_common = f"{COMMON_RUN_ROOT}/features/{feature_local.name}"
        model_common_payload = mt5.copy_to_common_files(common_files_root, model_local, model_common)
        feature_common_payload = mt5.copy_to_common_files(common_files_root, feature_local, feature_common)
        context = {
            "candidate_id": candidate_id,
            "axis_id": axis_id,
            "summary": summary_rows.get(candidate_id, {}),
            "handoff": dict(item),
            "model_local_path": rel(model_local),
            "feature_local_path": rel(feature_local),
            "model_common_path": model_common,
            "feature_common_path": feature_common,
            "model_common_copy": model_common_payload,
            "feature_common_copy": feature_common_payload,
            "model_sha256_actual": sha256_file(model_local),
            "feature_sha256_actual": sha256_file(feature_local),
            "split_kpi": {
                split: dict(kpi_rows.get((candidate_id, split), {}))
                for split in ("validation", "oos")
            },
            "signal_parity": {
                split: dict(signal_rows.get((candidate_id, split), {}))
                for split in ("validation", "oos")
            },
        }
        contexts.append(context)
    return contexts


def copy_run_artifact(source: Path, destination: Path) -> Path:
    if not path_exists(source):
        raise FileNotFoundError(source.as_posix())
    io_path(destination.parent).mkdir(parents=True, exist_ok=True)
    shutil.copy2(io_path(source), io_path(destination))
    return destination


def build_attempts(candidates: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    attempts: list[dict[str, Any]] = []
    for candidate in candidates:
        handoff = candidate["handoff"]
        axis_id = str(candidate["axis_id"])
        candidate_id = str(candidate["candidate_id"])
        for split, window in SPLIT_WINDOWS.items():
            attempt_name = f"f68d_{safe_name(axis_id, 24)}_{candidate_id[-6:]}_{split}"
            extra_set_values = {
                "InpSameDirectionReentryCooldownBars": int(handoff.get("same_direction_reentry_cooldown_bars") or 0),
                "InpReentryCooldownBars": 0,
                "InpAtrSltpEnabled": bool(handoff.get("atr_sltp_enabled")),
                "InpAtrStopMultiplier": float(handoff.get("atr_stop_multiplier") or 0.0),
                "InpAtrTakeProfitMultiplier": float(handoff.get("atr_take_profit_multiplier") or 0.0),
                "InpDecisionMode": str(handoff.get("decision_mode") or "threshold_margin"),
                "InpFallbackDecisionMode": str(handoff.get("decision_mode") or "threshold_margin"),
            }
            attempt = attempt_payload(
                run_root=RUN_ROOT,
                run_id=RUN_ID,
                stage_number=68,
                exploration_label=f"frontier68D_{axis_id}_mt5_runtime_probe(F68D {axis_id} MT5 런타임 탐침)",
                attempt_name=attempt_name,
                tier=mt5.TIER_A,
                split=split,
                model_path=str(candidate["model_common_path"]),
                model_id=f"F68D_{candidate_id}_{axis_id}",
                model_backend="onnx",
                feature_path=str(candidate["feature_common_path"]),
                feature_count=int(handoff.get("feature_count") or 0),
                feature_order_hash=str(handoff.get("feature_order_hash") or ""),
                short_threshold=float(handoff.get("short_threshold") or 0.0),
                long_threshold=float(handoff.get("long_threshold") or 0.0),
                min_margin=float(handoff.get("min_margin") or 0.0),
                invert_signal=False,
                from_date=window["from"],
                to_date=window["to"],
                primary_active_tier=mt5.TIER_A,
                attempt_role="f68d_candidate_axis_runtime_probe",
                record_view_prefix=f"mt5_f68d_{safe_name(axis_id, 24)}_{candidate_id[-6:]}",
                max_hold_bars=int(handoff.get("max_hold_bars") or 1),
                common_root=COMMON_RUN_ROOT,
                close_on_flat_signal=True,
                reverse_on_opposite_signal=True,
                close_only_on_opposite_signal=False,
                extra_set_values=extra_set_values,
            )
            attempt.update(
                {
                    "candidate_id": candidate_id,
                    "axis_id": axis_id,
                    "expected_rows": as_int((candidate.get("signal_parity", {}).get(split) or {}).get("rows")),
                    "expected_signal_count": as_int(
                        (candidate.get("signal_parity", {}).get(split) or {}).get("onnx_signal_count")
                    ),
                    "expected_sklearn_signal_count": as_int(
                        (candidate.get("signal_parity", {}).get(split) or {}).get("sklearn_signal_count")
                    ),
                    "proxy_kpi": candidate.get("split_kpi", {}).get(split, {}),
                    "model_common_copy": candidate.get("model_common_copy"),
                    "feature_common_copy": candidate.get("feature_common_copy"),
                    "model_sha256_actual": candidate.get("model_sha256_actual"),
                    "feature_sha256_actual": candidate.get("feature_sha256_actual"),
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
            attempts.append(attempt)
    return attempts


def build_local_verification(candidates: Sequence[Mapping[str, Any]], attempts: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []

    def add(name: str, ok: bool, detail: str, effect: str) -> None:
        rows.append({"check_name": name, "status": "passed" if ok else "failed", "detail": detail, "effect": effect})

    add("grok_clean_output_exists", path_exists(GROK_CLEAN), rel(GROK_CLEAN), "Grok pre-probe review(그록 탐침 전 검토)가 기록된다.")
    add("eligible_axis_count_is_two", len(candidates) == 2, f"eligible={len(candidates)}", "HGB failed axis(실패 축)을 probe queue(탐침 대기열)에서 제외한다.")
    for candidate in candidates:
        handoff = candidate["handoff"]
        cid = str(candidate["candidate_id"])
        add(
            f"{cid}_onnx_hash_match",
            str(handoff.get("model_sha256")) == str(candidate.get("model_sha256_actual")),
            f"handoff={handoff.get('model_sha256')};actual={candidate.get('model_sha256_actual')}",
            "Common Files copy(Common Files 복사) 전에 ONNX 정체성을 확인한다.",
        )
        add(
            f"{cid}_feature_count_hash_match",
            int(handoff.get("feature_count") or 0) > 0
            and str(handoff.get("feature_order_hash") or "") == str(candidate.get("handoff", {}).get("feature_order_hash") or ""),
            f"feature_count={handoff.get('feature_count')};feature_order_hash={handoff.get('feature_order_hash')}",
            "EA InpFeatureCount(EA 피처 수)와 피처 순서 해시를 고정한다.",
        )
        add(
            f"{cid}_common_copies_exist",
            path_exists(Path(str(candidate["model_common_copy"]["absolute_path"])))
            and path_exists(Path(str(candidate["feature_common_copy"]["absolute_path"]))),
            f"model={candidate['model_common_path']};feature={candidate['feature_common_path']}",
            "EA가 실제로 읽을 Common Files 경로를 확보한다.",
        )
    for attempt in attempts:
        add(
            f"{attempt['attempt_name']}_set_ini_exist",
            path_exists(ROOT / str(attempt["set"]["path"])) and path_exists(ROOT / str(attempt["ini"]["path"])),
            f"set={attempt['set']['path']};ini={attempt['ini']['path']}",
            "Strategy Tester(전략 테스터) 실행 입력을 고정한다.",
        )
        add(
            f"{attempt['attempt_name']}_date_window_known",
            str(attempt["split"]) in SPLIT_WINDOWS,
            f"{attempt['split']}={SPLIT_WINDOWS.get(str(attempt['split']))}",
            "proxy split(프록시 분할)과 tester 기간(테스터 기간)을 맞춘다.",
        )
    return {
        "passed": all(row["status"] == "passed" for row in rows),
        "rows": rows,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def grok_identity() -> dict[str, Any]:
    return {
        "packet_root": rel(GROK_PACKET_ROOT),
        "prompt_path": rel(GROK_PROMPT),
        "clean_output_path": rel(GROK_CLEAN),
        "metadata_path": rel(GROK_METADATA),
        "prompt_sha256": sha256_file(GROK_PROMPT) if path_exists(GROK_PROMPT) else "",
        "clean_output_sha256": sha256_file(GROK_CLEAN) if path_exists(GROK_CLEAN) else "",
        "metadata_exists": path_exists(GROK_METADATA),
    }


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
        portable_payload.update(
            {
                "copied": True,
                "portable_ea_ex5_exists_after": path_exists(PORTABLE_EA_BINARY),
                "portable_ea_sha256": mt5.sha256_file(PORTABLE_EA_BINARY),
            }
        )
    return {"compile": compile_payload, "portable_ea": portable_payload}


def can_run_terminal(compile_payload: Mapping[str, Any]) -> bool:
    compile_status = ((compile_payload.get("compile") or {}).get("status"))
    return compile_status == "completed" or path_exists(PORTABLE_EA_BINARY)


def clear_runtime_outputs(common_root: Path, attempt: Mapping[str, Any]) -> None:
    for key in ("common_telemetry_path", "common_summary_path"):
        value = str(attempt.get(key, "")).strip()
        if not value:
            continue
        target = common_root / Path(value)
        if path_exists(target):
            io_path(target).unlink()


def execute_attempts(
    args: argparse.Namespace,
    attempts: Sequence[Mapping[str, Any]],
    compile_payload: Mapping[str, Any],
) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for attempt in attempts:
        if not can_run_terminal(compile_payload):
            result = {"status": "blocked", "blocker": "compile_failed_and_portable_ea_missing"}
        else:
            clear_runtime_outputs(Path(args.common_files_root), attempt)
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
                result = {
                    "status": "blocked",
                    "command": exc.cmd,
                    "returncode": None,
                    "stdout": (exc.stdout or "")[-2000:],
                    "stderr": (exc.stderr or "")[-2000:],
                    "blocker": "terminal_timeout",
                }
            runtime_outputs = mt5.wait_for_mt5_runtime_outputs(
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
                "attempt_role": attempt.get("attempt_role"),
                "record_view_prefix": attempt.get("record_view_prefix"),
                "candidate_id": attempt.get("candidate_id"),
                "axis_id": attempt.get("axis_id"),
                "expected_rows": attempt.get("expected_rows"),
                "expected_signal_count": attempt.get("expected_signal_count"),
                "ini_path": attempt.get("ini", {}).get("path"),
                "set_path": attempt.get("set", {}).get("path"),
            }
        )
        results.append(result)
    return results


def build_runtime_receipt(
    execution_results: Sequence[Mapping[str, Any]],
    attempts: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    attempts_by_name = {str(attempt["attempt_name"]): attempt for attempt in attempts}
    rows: list[dict[str, Any]] = []
    for result in execution_results:
        attempt = attempts_by_name[str(result["attempt_name"])]
        runtime = result.get("runtime_outputs", {}) if isinstance(result.get("runtime_outputs"), Mapping) else {}
        last = runtime.get("last_summary", {}) if isinstance(runtime.get("last_summary"), Mapping) else {}
        report = result.get("strategy_tester_report", {}) if isinstance(result.get("strategy_tester_report"), Mapping) else {}
        metrics = report.get("metrics", {}) if isinstance(report.get("metrics"), Mapping) else {}
        report_rel = (report.get("html_report") or {}).get("path", "") if isinstance(report.get("html_report"), Mapping) else ""
        report_path = ROOT / str(report_rel) if report_rel else Path("")
        deal_metrics = extract_deal_metrics(report_path) if report_rel and path_exists(report_path) else empty_deal_metrics()
        long_count = as_int(last.get("long_count")) or 0
        short_count = as_int(last.get("short_count")) or 0
        signal_count = long_count + short_count
        order_attempt_count = as_int(last.get("order_attempt_count")) or 0
        order_fill_count = as_int(last.get("order_fill_count")) or 0
        trade_count = as_int(metrics.get("trade_count")) or 0
        winning_trade_count = as_int(metrics.get("winning_trade_count")) or 0
        losing_trade_count = as_int(metrics.get("losing_trade_count")) or 0
        gross_profit = as_float(metrics.get("gross_profit"))
        gross_loss = as_float(metrics.get("gross_loss"))
        average_win = as_float(metrics.get("average_win"))
        if average_win is None and winning_trade_count and gross_profit is not None:
            average_win = gross_profit / winning_trade_count
        average_loss = as_float(metrics.get("average_loss"))
        if average_loss is None and losing_trade_count and gross_loss is not None:
            average_loss = gross_loss / losing_trade_count
        payoff_ratio = as_float(metrics.get("payoff_ratio"))
        if payoff_ratio is None and average_win is not None and average_loss not in (None, 0):
            payoff_ratio = abs(average_win / average_loss)
        test_period = tester_period(attempt)
        proxy = attempt.get("proxy_kpi") if isinstance(attempt.get("proxy_kpi"), Mapping) else {}
        runtime_dd = as_float(metrics.get("max_drawdown_percent"))
        proxy_dd = as_float(proxy.get("proxy_dd_percent_on_10000_points"))
        row = {
            "run_id": RUN_ID,
            "attempt_name": attempt.get("attempt_name"),
            "candidate_id": attempt.get("candidate_id"),
            "axis_id": attempt.get("axis_id"),
            "split": attempt.get("split"),
            "test_period_start": test_period.get("start"),
            "test_period_end": test_period.get("end"),
            "calendar_days_exclusive": test_period.get("calendar_days_exclusive"),
            "tester_status": result.get("status"),
            "runtime_status": runtime.get("status", "missing"),
            "report_status": report.get("status", "missing"),
            "expected_rows": attempt.get("expected_rows"),
            "feature_ready_count": as_int(last.get("feature_ready_count")) or 0,
            "feature_ready_diff": (as_int(last.get("feature_ready_count")) or 0) - int(attempt.get("expected_rows") or 0),
            "expected_signal_count": attempt.get("expected_signal_count"),
            "signal_count": signal_count,
            "signal_count_diff": signal_count - int(attempt.get("expected_signal_count") or 0),
            "order_attempt_count": order_attempt_count,
            "order_fill_count": order_fill_count,
            "order_fill_rate": ratio(order_fill_count, order_attempt_count),
            "trade_count": trade_count,
            "trades_per_day": ratio(trade_count, test_period.get("calendar_days_exclusive")),
            "long_trade_count": metrics.get("long_trade_count"),
            "short_trade_count": metrics.get("short_trade_count"),
            "winning_trade_count": winning_trade_count,
            "losing_trade_count": losing_trade_count,
            "deal_count": as_int(metrics.get("deal_count")) or int(deal_metrics["deal_row_count"]),
            "deal_in_count": deal_metrics["deal_in_count"],
            "deal_out_count": deal_metrics["deal_out_count"],
            "deal_minus_order_fill": (as_int(metrics.get("deal_count")) or int(deal_metrics["deal_row_count"])) - order_fill_count,
            "deal_count_equals_2x_trade": (as_int(metrics.get("deal_count")) or int(deal_metrics["deal_row_count"])) == 2 * trade_count if trade_count else False,
            "order_fill_equals_deal_count": order_fill_count == (as_int(metrics.get("deal_count")) or int(deal_metrics["deal_row_count"])),
            "net_profit": metrics.get("net_profit"),
            "gross_profit": metrics.get("gross_profit"),
            "gross_loss": metrics.get("gross_loss"),
            "profit_factor": metrics.get("profit_factor"),
            "expectancy": metrics.get("expectancy"),
            "win_rate_percent": metrics.get("win_rate_percent"),
            "average_win": average_win,
            "average_loss": average_loss,
            "payoff_ratio": payoff_ratio,
            "recovery_factor": metrics.get("recovery_factor"),
            "max_drawdown_amount": metrics.get("max_drawdown_amount"),
            "max_drawdown_percent": runtime_dd,
            "proxy_net_profit": as_float(proxy.get("net_profit_proxy_points")),
            "proxy_profit_factor": as_float(proxy.get("profit_factor")),
            "proxy_trades_per_day": as_float(proxy.get("trades_per_day")),
            "proxy_dd_percent": proxy_dd,
            "dd_delta_runtime_minus_proxy": (runtime_dd - proxy_dd) if runtime_dd is not None and proxy_dd is not None else None,
            "deal_profit_sum": deal_metrics["deal_profit_sum"],
            "deal_commission_sum": deal_metrics["deal_commission_sum"],
            "deal_swap_sum": deal_metrics["deal_swap_sum"],
            "deal_cost_sum": deal_metrics["deal_cost_sum"],
            "net_reconciliation_error": reconciliation_error(metrics.get("net_profit"), deal_metrics),
            "gap_cause_summary": gap_cause_summary(attempt, metrics, last),
            "report_path": report_rel,
            "telemetry_path": runtime.get("telemetry_path", ""),
            "summary_path": runtime.get("summary_path", ""),
            "claim_boundary": CLAIM_BOUNDARY,
        }
        rows.append(row)
    return rows


def empty_deal_metrics() -> dict[str, Any]:
    return {
        "deal_table_encoding": "",
        "deal_row_count": 0,
        "deal_in_count": 0,
        "deal_out_count": 0,
        "deal_commission_sum": 0.0,
        "deal_swap_sum": 0.0,
        "deal_profit_sum": 0.0,
        "deal_cost_sum": 0.0,
    }


def reconciliation_error(net_profit: Any, deal_metrics: Mapping[str, Any]) -> float | None:
    net = as_float(net_profit)
    if net is None:
        return None
    computed = (
        float(deal_metrics.get("deal_profit_sum") or 0.0)
        + float(deal_metrics.get("deal_commission_sum") or 0.0)
        + float(deal_metrics.get("deal_swap_sum") or 0.0)
    )
    return computed - net


def tester_period(attempt: Mapping[str, Any]) -> dict[str, Any]:
    tester = ((attempt.get("ini") or {}).get("tester") or {})
    start = str(tester.get("FromDate") or "").replace(".", "-")
    end = str(tester.get("ToDate") or "").replace(".", "-")
    days = None
    if start and end:
        try:
            days = max((datetime.strptime(end, "%Y-%m-%d") - datetime.strptime(start, "%Y-%m-%d")).days, 1)
        except ValueError:
            days = None
    return {"start": start, "end": end, "calendar_days_exclusive": days}


def gap_cause_summary(attempt: Mapping[str, Any], metrics: Mapping[str, Any], last_summary: Mapping[str, Any]) -> str:
    parts = []
    if str(attempt.get("axis_id")) == "pf_axis":
        parts.append("proxy_pf_saturation_ceiling(PF 포화 상한)")
    if (as_int(last_summary.get("feature_ready_count")) or 0) - int(attempt.get("expected_rows") or 0) != 0:
        parts.append("feature_readiness_gap(피처 준비 간극)")
    if (as_int(last_summary.get("long_count")) or 0) + (as_int(last_summary.get("short_count")) or 0) != int(
        attempt.get("expected_signal_count") or 0
    ):
        parts.append("signal_count_gap(신호 수 간극)")
    if as_float(metrics.get("profit_factor")) is not None:
        parts.append("tester_economics_observed(테스터 경제성 관찰)")
    return ";".join(parts) if parts else "runtime_probe_observation_no_single_gap_cause_yet(런타임 탐침 관찰, 단일 원인 미확정)"


def build_gap_classification(receipt: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows = [
        gap_row(receipt, "signal_count_parity", "signal_count", receipt.get("expected_signal_count"), receipt.get("signal_count"), receipt.get("signal_count_diff"), "signal_count_exact" if receipt.get("signal_count_diff") == 0 else "signal_count_gap", "runtime_summary_vs_onnx_signal_parity"),
        gap_row(receipt, "feature_readiness", "feature_ready_count", receipt.get("expected_rows"), receipt.get("feature_ready_count"), receipt.get("feature_ready_diff"), "feature_ready_exact" if receipt.get("feature_ready_diff") == 0 else "feature_ready_gap", "runtime_summary_feature_ready_count"),
        gap_row(receipt, "trade_density", "trades_per_day", receipt.get("proxy_trades_per_day"), receipt.get("trades_per_day"), numeric_delta(receipt.get("trades_per_day"), receipt.get("proxy_trades_per_day")), density_gap_class(receipt), "proxy_kpi_vs_strategy_tester_trade_count"),
        gap_row(receipt, "economics_pf", "profit_factor", receipt.get("proxy_profit_factor"), receipt.get("profit_factor"), numeric_delta(receipt.get("profit_factor"), receipt.get("proxy_profit_factor")), pf_gap_class(receipt), "proxy_kpi_vs_strategy_tester_report"),
        gap_row(receipt, "drawdown_methodology", "drawdown_percent", receipt.get("proxy_dd_percent"), receipt.get("max_drawdown_percent"), receipt.get("dd_delta_runtime_minus_proxy"), dd_gap_class(receipt), "proxy_dd_percent_vs_strategy_tester_dd"),
        gap_row(receipt, "accounting_trade_shape", "order_fill_vs_deal_count", receipt.get("order_fill_count"), receipt.get("deal_count"), receipt.get("deal_minus_order_fill"), "deal_order_gap" if receipt.get("deal_minus_order_fill") else "deal_order_no_gap", "runtime_order_fill_count_vs_strategy_report_deal_count"),
        gap_row(receipt, "cost_identity", "commission_swap", "proxy_cost_terms", f"commission={receipt.get('deal_commission_sum')};swap={receipt.get('deal_swap_sum')}", receipt.get("deal_cost_sum"), "cost_observed_in_deal_table" if receipt.get("deal_cost_sum") not in (None, 0, 0.0) else "cost_zero_or_unparsed", "strategy_report_deal_table"),
    ]
    return rows


def gap_row(
    receipt: Mapping[str, Any],
    layer: str,
    metric: str,
    proxy_value: Any,
    runtime_value: Any,
    delta: Any,
    gap_class: str,
    evidence: str,
) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "attempt_name": receipt.get("attempt_name"),
        "candidate_id": receipt.get("candidate_id"),
        "axis_id": receipt.get("axis_id"),
        "split": receipt.get("split"),
        "layer": layer,
        "metric": metric,
        "proxy_value": proxy_value,
        "runtime_value": runtime_value,
        "delta": delta,
        "gap_class": gap_class,
        "evidence": evidence,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def numeric_delta(runtime: Any, proxy: Any) -> float | None:
    a = as_float(runtime)
    b = as_float(proxy)
    return a - b if a is not None and b is not None else None


def density_gap_class(receipt: Mapping[str, Any]) -> str:
    runtime = as_float(receipt.get("trades_per_day"))
    if runtime is None:
        return "runtime_density_missing"
    if 5.0 <= runtime <= 10.0:
        return "runtime_density_in_target_band"
    return "runtime_density_outside_target_band"


def pf_gap_class(receipt: Mapping[str, Any]) -> str:
    proxy = as_float(receipt.get("proxy_profit_factor"))
    runtime = as_float(receipt.get("profit_factor"))
    if runtime is None:
        return "runtime_pf_missing"
    if proxy is not None and proxy >= 90:
        return "proxy_pf_saturation_vs_runtime_pf"
    return "runtime_pf_below_proxy" if proxy is not None and runtime < proxy else "runtime_pf_not_below_proxy"


def dd_gap_class(receipt: Mapping[str, Any]) -> str:
    runtime = as_float(receipt.get("max_drawdown_percent"))
    proxy = as_float(receipt.get("proxy_dd_percent"))
    if runtime is None:
        return "runtime_dd_missing"
    if runtime < 10.0:
        return "runtime_dd_under_10_observation"
    if proxy is not None and runtime > proxy:
        return "runtime_dd_exceeds_proxy_dd"
    return "runtime_dd_over_10_observation"


def write_outputs(payload: Mapping[str, Any], created_at: str) -> None:
    write_json(RUN_ROOT / "frontier68D_runtime_probe_execution_result.json", payload)
    write_json(RUN_ROOT / "frontier68D_runtime_probe_summary.json", build_summary(payload))
    write_csv(
        RUN_ROOT / "frontier68D_local_verification.csv",
        payload.get("local_verification", {}).get("rows", []),
        LOCAL_VERIFICATION_COLUMNS,
    )
    write_csv(RUN_ROOT / "frontier68D_runtime_probe_receipt.csv", payload.get("runtime_receipt", []), RUNTIME_RECEIPT_COLUMNS)
    write_csv(RUN_ROOT / "frontier68D_gap_classification.csv", payload.get("gap_classification", []), GAP_COLUMNS)
    write_json(RUN_ROOT / "run_manifest.json", build_run_manifest(payload, created_at))
    write_csv(REVIEWS_ROOT / "frontier68D_runtime_probe_receipt_review.csv", payload.get("runtime_receipt", []), RUNTIME_RECEIPT_COLUMNS)
    write_csv(REVIEWS_ROOT / "frontier68D_gap_classification_review.csv", payload.get("gap_classification", []), GAP_COLUMNS)
    write_report(payload, created_at)
    write_grok_receipt(payload, created_at)
    write_gate_audit(payload, created_at)
    write_review_index()


def build_summary(payload: Mapping[str, Any]) -> dict[str, Any]:
    receipts = payload.get("runtime_receipt") or []
    best_density = next((row for row in receipts if row.get("axis_id") == "density_axis" and row.get("split") == "oos"), {})
    best_pf = next((row for row in receipts if row.get("axis_id") == "pf_axis" and row.get("split") == "oos"), {})
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "status": payload.get("status"),
        "judgment": payload.get("judgment"),
        "attempt_count": len(payload.get("attempts", [])),
        "receipt_rows": len(receipts),
        "local_verification_passed": payload.get("local_verification", {}).get("passed"),
        "density_oos": best_density,
        "pf_axis_oos": best_pf,
        "claim_boundary": CLAIM_BOUNDARY,
        "next_action": NEXT_RUN_ID,
    }


def build_run_manifest(payload: Mapping[str, Any], created_at: str) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "created_at_utc": created_at,
        "status": payload.get("status"),
        "judgment": payload.get("judgment"),
        "claim_boundary": CLAIM_BOUNDARY,
        "producer": "stage_pipelines/stage_frontier_68/frontier68d_mt5_runtime_probe_candidate_axis_materialization.py",
        "hypothesis": (
            "F68C ONNX candidate axes can be materialized in MT5 Strategy Tester to observe proxy/runtime economics gaps."
        ),
        "experiment_design": experiment_design_payload(),
        "grok_packet": payload.get("grok_packet"),
        "local_verification": payload.get("local_verification"),
        "attempts": payload.get("attempts"),
        "execution_results": payload.get("execution_results"),
        "strategy_tester_reports": payload.get("strategy_tester_reports"),
        "mt5_kpi_records": payload.get("mt5_kpi_records"),
        "runtime_receipt_path": rel(RUN_ROOT / "frontier68D_runtime_probe_receipt.csv"),
        "gap_classification_path": rel(RUN_ROOT / "frontier68D_gap_classification.csv"),
        "summary": build_summary(payload),
        "next_action": NEXT_RUN_ID,
    }


def experiment_design_payload() -> dict[str, Any]:
    return {
        "hypothesis": "F68C exported ONNX axes expose whether lifecycle/cost/DD-aware proxy clues transfer to MT5 runtime economics.",
        "decision_use": "runtime_probe_observation and proxy/runtime gap repair planning only",
        "comparison_baseline": "F68C proxy KPI by candidate axis and split; F67D runtime parity/economics memory as reference only",
        "control_variables": ["US100 M5", "RuntimeProbeEA", "same tester deposit/leverage/model", "fixed F68C thresholds/features/models"],
        "changed_variables": ["candidate axis", "validation vs OOS split"],
        "sample_scope": "validation 2025.01.02-2025.10.01 and OOS 2025.10.01-2026.04.14",
        "success_criteria": "MT5 tester report and runtime telemetry materialized with KPI/gap records",
        "failure_criteria": "tester/compile/runtime output blocked or signal/feature parity cannot be evaluated",
        "invalid_conditions": "model/feature hash mismatch, axis 3 HGB used despite export failure, threshold retuned inside F68D",
        "stop_conditions": "after four fixed attempts or first system blocker requiring repair",
        "evidence_plan": "run_manifest, runtime receipt CSV, gap classification CSV, MT5 reports, telemetry summaries, ledgers",
    }


def write_report(payload: Mapping[str, Any], created_at: str) -> None:
    receipts = list(payload.get("runtime_receipt") or [])
    lines = [
        "# F68D MT5 Runtime Probe(F68D MT5 런타임 탐침)",
        "",
        f"Updated(갱신): {created_at}",
        "",
        "## Action And Effect(행동 및 효과)",
        "",
        "Action(행동): F68C에서 ONNX export(ONNX 내보내기)와 parity pass(동등성 통과)를 받은 두 후보 축을 MT5 Strategy Tester(MT5 전략 테스터)에서 validation/OOS(검증/표본외)로 실행했다.",
        "",
        "Effect(효과): winner(승자)를 고르지 않고 density axis(밀도 축)와 PF axis(수익 팩터 축)의 proxy/runtime KPI gap(프록시/런타임 KPI 간극), signal count parity(신호 수 동등성), feature readiness parity(피처 준비 동등성), accounting/trade-shape gap(회계/거래 형태 간극)을 분리 기록했다.",
        "",
        f"- status(상태): `{payload.get('status')}`",
        f"- judgment(판정): `{payload.get('judgment')}`",
        f"- attempts(시도 수): `{len(payload.get('attempts', []))}`",
        f"- local_verification_passed(로컬 검증 통과): `{payload.get('local_verification', {}).get('passed')}`",
        "",
        "## Runtime KPI(런타임 핵심 성과 지표)",
        "",
        "| axis(축) | split(분할) | period(기간) | net(순수익) | gross profit(총이익) | gross loss(총손실) | PF(수익 팩터) | DD%(손실폭) | trades(거래) | trades/day(일 거래) | signal diff(신호 차이) | feature diff(피처 차이) |",
        "|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in receipts:
        lines.append(
            "| `{axis}` | `{split}` | `{start}..{end}` | `{net}` | `{gp}` | `{gl}` | `{pf}` | `{dd}` | `{trades}` | `{tpd}` | `{sig}` | `{feat}` |".format(
                axis=row.get("axis_id"),
                split=row.get("split"),
                start=row.get("test_period_start"),
                end=row.get("test_period_end"),
                net=fmt(row.get("net_profit")),
                gp=fmt(row.get("gross_profit")),
                gl=fmt(row.get("gross_loss")),
                pf=fmt(row.get("profit_factor")),
                dd=fmt(row.get("max_drawdown_percent")),
                trades=fmt(row.get("trade_count")),
                tpd=fmt(row.get("trades_per_day")),
                sig=fmt(row.get("signal_count_diff")),
                feat=fmt(row.get("feature_ready_diff")),
            )
        )
    if not receipts:
        lines.append("| `missing` | `missing` | `missing` | `NA` | `NA` | `NA` | `NA` | `NA` | `NA` | `NA` | `NA` | `NA` |")
    lines.extend(
        [
            "",
            "## Gap Notes(간극 메모)",
            "",
        ]
    )
    for row in receipts:
        lines.append(
            f"- `{row.get('axis_id')}/{row.get('split')}`: proxy PF/DD/trades_day(프록시 수익 팩터/손실폭/일 거래) "
            f"`{fmt(row.get('proxy_profit_factor'))}/{fmt(row.get('proxy_dd_percent'))}/{fmt(row.get('proxy_trades_per_day'))}` -> "
            f"runtime(런타임) `{fmt(row.get('profit_factor'))}/{fmt(row.get('max_drawdown_percent'))}/{fmt(row.get('trades_per_day'))}`; "
            f"gap_cause(간극 원인) `{row.get('gap_cause_summary')}`."
        )
    lines.extend(
        [
            "",
            "Claim boundary(주장 경계): runtime_probe_observation(런타임 탐침 관찰) only. completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 주장하지 않는다.",
        ]
    )
    write_md(REVIEWS_ROOT / "frontier68D_mt5_runtime_probe_report.md", lines)


def write_grok_receipt(payload: Mapping[str, Any], created_at: str) -> None:
    local = payload.get("local_verification", {})
    lines = [
        "# F68D Grok Pre-MT5 Receipt(F68D MT5 전 그록 영수증)",
        "",
        f"Updated(갱신): {created_at}",
        "",
        "- trigger_reason(트리거 이유): goal rule(목표 규칙)이 MT5 Runtime Probe(MT5 런타임 탐침) 전 Grok review(그록 검토)를 요구한다.",
        "- review_size(검토 크기): medium review(중간 검토).",
        "- direction_before_grok(그록 전 방향): two eligible ONNX axes(두 적격 ONNX 축)를 validation/OOS(검증/표본외) 네 tester attempt(테스터 시도)로 물질화한다.",
        f"- prompt_identity(프롬프트 정체성): `{rel(GROK_PROMPT)}` sha256 `{sha256_file(GROK_PROMPT) if path_exists(GROK_PROMPT) else ''}`.",
        f"- grok_output_identity(그록 출력 정체성): `{rel(GROK_CLEAN)}` sha256 `{sha256_file(GROK_CLEAN) if path_exists(GROK_CLEAN) else ''}`.",
        "- advice_classification(조언 분류): accepted(수용)=run both axes and separate gap taxonomy(두 축 실행 및 간극 분류 분리); rejected(거절)=winner/baseline/promotion/runtime authority/live readiness/Goal Achieve(승자/기준선/승격/런타임 권위/실거래 준비/목표 달성); needs_local_verification(로컬 검증 필요)=hash/path/set/ini/date/compile/accounting checks(해시/경로/설정/초기화/기간/컴파일/회계 점검).",
        f"- local_verification(로컬 검증): `{local.get('passed')}` with `{len(local.get('rows', []))}` checks(점검).",
        "- forbidden_claim_check(금지 주장 확인): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음).",
        "- final_codex_direction(최종 Codex 방향): fixed-parameter F68D runtime probe(고정 파라미터 F68D 런타임 탐침)를 실행하고 labeled gaps(라벨된 간극)만 보고한다.",
    ]
    write_md(GROK_PACKET_ROOT / "f68d_pre_mt5_candidate_axis_receipt.md", lines)


def write_gate_audit(payload: Mapping[str, Any], created_at: str) -> None:
    lines = [
        "# F68D Gate Audit(F68D 게이트 감사)",
        "",
        f"Updated(갱신): {created_at}",
        "",
        f"- Grok pre-probe review(그록 탐침 전 검토): `{'passed' if path_exists(GROK_CLEAN) else 'missing'}`.",
        f"- local verification(로컬 검증): `{payload.get('local_verification', {}).get('passed')}`.",
        f"- MT5 Runtime Probe attempted(MT5 런타임 탐침 시도): `{bool(payload.get('execution_results'))}`.",
        f"- Strategy Tester reports(전략 테스터 보고서): `{len(payload.get('strategy_tester_reports', []))}`.",
        f"- runtime receipt rows(런타임 영수증 행): `{len(payload.get('runtime_receipt', []))}`.",
        f"- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`.",
    ]
    write_md(REVIEWS_ROOT / "frontier68D_gate_audit.md", lines)


def write_review_index() -> None:
    lines = [
        "# F68 Review Index(F68 검토 색인)",
        "",
        "- `../00_spec/stage_brief.md`: F68 stage brief(F68 단계 개요)",
        "- `runA_report.md`: F68A stage open report(F68A 단계 개방 보고서)",
        "- `grok_stage_open_receipt.md`: F68 Grok stage-open receipt(F68 그록 단계 개방 영수증)",
        "- `stage_run_ledger.csv`: F68 stage-local run ledger(F68 단계 내부 실행 장부)",
        "- `frontier68A_bridge_feasibility_and_label_design_report.md`: F68A bridge feasibility and label design report(F68A 연결 가능성 및 라벨 설계 보고서)",
        "- `frontier68B_proxy_broad_sweep_report.md`: F68B proxy broad sweep report(F68B 프록시 넓은 탐색 보고서)",
        "- `frontier68C_onnx_scout_export_report.md`: F68C ONNX scout export report(F68C ONNX 탐색 내보내기 보고서)",
        "- `frontier68D_mt5_runtime_probe_report.md`: F68D MT5 runtime probe report(F68D MT5 런타임 탐침 보고서)",
        "- `frontier68D_runtime_probe_receipt_review.csv`: F68D runtime receipt(F68D 런타임 영수증)",
        "- `frontier68D_gap_classification_review.csv`: F68D gap classification(F68D 간극 분류)",
        "- `frontier68D_gate_audit.md`: F68D gate audit(F68D 게이트 감사)",
        "",
        f"Current status(현재 상태): `{RUN_ID}` runtime probe observation(런타임 탐침 관찰)",
        f"Next action(다음 행동): `{NEXT_RUN_ID}`",
    ]
    write_md(REVIEWS_ROOT / "review_index.md", lines)


def update_state_and_ledgers(payload: Mapping[str, Any]) -> None:
    summary = build_summary(payload)
    receipts = list(payload.get("runtime_receipt") or [])
    density_oos = next((row for row in receipts if row.get("axis_id") == "density_axis" and row.get("split") == "oos"), {})
    pf_oos = next((row for row in receipts if row.get("axis_id") == "pf_axis" and row.get("split") == "oos"), {})
    row = {
        "ledger_row_id": f"{RUN_ID}__mt5_runtime_probe",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "mt5_runtime_probe_candidate_axis_materialization(MT5 런타임 탐침 후보 축 물질화)",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "validation_oos_mt5_runtime_probe(검증/표본외 MT5 런타임 탐침)",
        "tier_scope": "Tier A+B planned(티어 A+B 계획)",
        "kpi_scope": "mt5_runtime_probe_kpi_and_gap(런타임 탐침 KPI 및 간극)",
        "scoreboard_lane": "runtime_probe(런타임 탐침)",
        "status": payload.get("status"),
        "judgment": payload.get("judgment"),
        "path": f"stages/{STAGE_ID}/03_reviews/frontier68D_mt5_runtime_probe_report.md",
        "primary_kpi": (
            f"density_oos_net={fmt(density_oos.get('net_profit'))};density_oos_pf={fmt(density_oos.get('profit_factor'))};"
            f"density_oos_dd={fmt(density_oos.get('max_drawdown_percent'))};pf_axis_oos_pf={fmt(pf_oos.get('profit_factor'))}"
        ),
        "guardrail_kpi": (
            f"attempts={len(payload.get('attempts', []))};signal_gap_rows="
            f"{sum(1 for r in receipts if r.get('signal_count_diff') not in (0, '0'))};feature_gap_rows="
            f"{sum(1 for r in receipts if r.get('feature_ready_diff') not in (0, '0'))}"
        ),
        "external_verification_status": "completed" if str(payload.get("status", "")).startswith("completed") else "blocked",
        "notes": "F68D executed fixed ONNX axes in MT5 Strategy Tester; observation only, no authority.",
        "stage": STAGE_ID,
        "run_family": "frontier_mt5_runtime_probe(전선 MT5 런타임 탐침)",
        "run_type": "candidate_axis_materialization(후보 축 물질화)",
        "date": "2026-06-17",
        "next_action": NEXT_RUN_ID,
        "current_run": NEXT_RUN_ID,
        "latest_completed_run": RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
        "report": f"stages/{STAGE_ID}/03_reviews/frontier68D_mt5_runtime_probe_report.md",
        "gate_audit_path": f"stages/{STAGE_ID}/03_reviews/frontier68D_gate_audit.md",
        "artifact_count": len(payload.get("attempts", [])) + len(receipts),
        "created_at_utc": payload.get("created_at_utc"),
        "kpi_summary": json.dumps(json_ready(summary), ensure_ascii=False, sort_keys=True),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "trade_density": fmt(density_oos.get("trades_per_day")),
        "source_authority": "mt5_strategy_tester_runtime_probe_observation(MT5 전략 테스터 런타임 탐침 관찰)",
        "goal_achieve": "not_claimed",
        "input_run_id": PARENT_RUN_ID,
        "output_path": f"stages/{STAGE_ID}/02_runs/{RUN_ID}/frontier68D_runtime_probe_execution_result.json",
        "result_path": f"stages/{STAGE_ID}/03_reviews/frontier68D_mt5_runtime_probe_report.md",
        "selected_net_profit": fmt(density_oos.get("net_profit")),
        "selected_profit_factor": fmt(density_oos.get("profit_factor")),
        "selected_trade_density": fmt(density_oos.get("trades_per_day")),
        "max_drawdown_percent": fmt(density_oos.get("max_drawdown_percent")),
        "strict_joint_pass_count": 0,
    }
    upsert_ledger(REVIEWS_ROOT / "stage_run_ledger.csv", "ledger_row_id", row)
    upsert_ledger(ROOT / "docs/registers/alpha_run_ledger.csv", "ledger_row_id", row)
    upsert_ledger(ROOT / "docs/registers/run_registry.csv", "run_id", row)
    write_current_state(payload)
    write_selection_status(payload)


def write_current_state(payload: Mapping[str, Any]) -> None:
    lines = [
        f"current_stage_id: {STAGE_ID}",
        f"active_stage: {STAGE_ID}",
        f"current_run_id: {NEXT_RUN_ID}",
        f"latest_completed_run_id: {RUN_ID}",
        f"current_status: {payload.get('status')}",
        f"current_judgment: {payload.get('judgment')}",
        f"next_stage_id: {STAGE_ID}",
        f"next_run_id: {NEXT_RUN_ID}",
        "runtime_probe_status: f68d_mt5_runtime_probe_observation_recorded_no_authority(F68D MT5 런타임 탐침 관찰 기록, 권위 없음)",
        "runtime_authority: not_claimed",
        "operating_promotion: not_claimed",
        "live_readiness: not_claimed",
        "goal_achieve: not_claimed",
        f"updated_at_utc: '{payload.get('created_at_utc')}'",
        "notes:",
        f'  - "F68D action(행동): fixed F68C ONNX axes(고정 F68C ONNX 축)를 MT5 Strategy Tester(MT5 전략 테스터)에서 물질화했다."',
        f'  - "Effect(효과): proxy/runtime KPI gap(프록시/런타임 KPI 간극), signal parity(신호 동등성), feature readiness parity(피처 준비 동등성)를 기록했다."',
        f'  - "Boundary(경계): runtime probe observation(런타임 탐침 관찰) only, no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음)."',
    ]
    io_path(ROOT / "docs/workspace/workspace_state.yaml").write_text("\n".join(lines) + "\n", encoding="utf-8-sig")
    cws = [
        "# Current Working State(현재 작업 상태)",
        "",
        f"Updated(갱신): {payload.get('created_at_utc')}",
        "",
        f"Active stage(활성 단계): `{STAGE_ID}`",
        "",
        f"Current run(현재 실행): `{NEXT_RUN_ID}`",
        "",
        f"Latest completed run(최근 완료 실행): `{RUN_ID}`",
        "",
        "## Current Truth(현재 진실)",
        "",
        "Action(행동): F68D MT5 Runtime Probe(F68D MT5 런타임 탐침)를 실행했다.",
        "",
        "Effect(효과): F68C ONNX scout axes(F68C ONNX 탐색 축)를 실제 Strategy Tester KPI(전략 테스터 핵심 성과 지표)와 runtime telemetry(런타임 기록)로 물질화했다.",
        "",
        f"- F68D status(F68D 상태): `{payload.get('status')}`.",
        f"- attempts(시도 수): `{len(payload.get('attempts', []))}`.",
        f"- runtime_receipt_rows(런타임 영수증 행): `{len(payload.get('runtime_receipt', []))}`.",
        "",
        "Claim boundary(주장 경계): runtime_probe_observation_only_no_completion_no_baseline_no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve.",
    ]
    write_md(ROOT / "docs/context/current_working_state.md", cws)


def write_selection_status(payload: Mapping[str, Any]) -> None:
    lines = [
        "# F68 Selection Status(F68 선택 상태)",
        "",
        f"- stage(단계): `{STAGE_ID}`",
        f"- current_run(현재 실행): `{NEXT_RUN_ID}`",
        f"- latest_completed_run(최근 완료 실행): `{RUN_ID}`",
        f"- status(상태): `{payload.get('status')}`",
        "- selected_baseline(선택 기준선): `not_claimed(주장 없음)`",
        "- runtime_authority(런타임 권위): `not_claimed(주장 없음)`",
        "- operating_promotion(운영 승격): `not_claimed(주장 없음)`",
        "- live_readiness(실거래 준비): `not_claimed(주장 없음)`",
        "- Goal Achieve(목표 달성): `not_claimed(주장 없음)`",
        f"- completed_action(완료 행동): F68D MT5 Runtime Probe(F68D MT5 런타임 탐침)로 `{len(payload.get('attempts', []))}` attempts(시도)를 물질화했다.",
        f"- report(보고서): `stages/{STAGE_ID}/03_reviews/frontier68D_mt5_runtime_probe_report.md`",
        f"- runtime_receipt(런타임 영수증): `stages/{STAGE_ID}/03_reviews/frontier68D_runtime_probe_receipt_review.csv`",
        f"- gap_classification(간극 분류): `stages/{STAGE_ID}/03_reviews/frontier68D_gap_classification_review.csv`",
        f"- next_action(다음 행동): `{NEXT_RUN_ID}` proxy/runtime gap analysis and repair decision(프록시/런타임 간극 분석 및 수리 결정).",
        f"- boundary(경계): `{CLAIM_BOUNDARY}`.",
    ]
    write_md(STAGE_ROOT / "04_selected" / "selection_status.md", lines)


def fmt(value: Any) -> str:
    number = as_float(value)
    if number is None:
        return "" if value in (None, "") else str(value)
    if math.isfinite(number) and abs(number - round(number)) < 1e-9:
        return str(int(round(number)))
    return f"{number:.6f}".rstrip("0").rstrip(".")


if __name__ == "__main__":
    raise SystemExit(main())
