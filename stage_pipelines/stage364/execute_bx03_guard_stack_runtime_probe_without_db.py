from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, path_exists  # noqa: E402
from foundation.mt5.runtime_artifacts import sha256_file  # noqa: E402
from stage_pipelines.stage364 import execute_overlay_hour17_native_short_ablation_runtime_probe_without_db as bx  # noqa: E402
from stage_pipelines.stage364 import materialize_bx03_december_late_session_guard_inputs_without_db as bz  # noqa: E402
from stage_pipelines.stage364 import materialize_synthetic_short_source_runtime_repair_without_db as bv  # noqa: E402


TODAY = "2026-06-05"
STAGE_ID = bz.STAGE_ID
RUN_NUMBER = "run364CA"
RUN_ID = "run364CA_execute_bx03_guard_stack_runtime_probe_without_db_v1"
PARENT_RUN_ID = bz.RUN_ID
BASELINE_BX_RUN_ID = bx.RUN_ID
BASELINE_BV_RUN_ID = bv.RUN_ID
NEXT_RUN_ID = "run364CB_review_bx03_guard_stack_runtime_probe_without_db_v1"
EXPLORATION_LABEL = "stage364_BX3GuardStack__RuntimeProbe"
MODEL_ID = bx.MODEL_ID
CLAIM_BOUNDARY = (
    "research_development_runtime_probe_only_no_new_model_training_no_forward_pass_"
    "no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

STAGE_DIR = bz.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
MT5_DIR = RUN_DIR / "mt5"
SET_DIR = MT5_DIR / "sets"
INI_DIR = MT5_DIR / "inis"
COMPILE_DIR = MT5_DIR / "compile"
REPORT_COPY_DIR = MT5_DIR / "reports"
TELEMETRY_COPY_DIR = RUN_DIR / "runtime_telemetry"
REVIEW_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"
SPEC_DIR = STAGE_DIR / "00_spec"

INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
RUNTIME_POLICY_CONFIG = RUN_DIR / "runtime_policy_config.json"
COMMON_FILES_SYNC = RUN_DIR / "common_files_sync.csv"
TESTER_SET_MANIFEST = RUN_DIR / "tester_set_manifest.csv"
TESTER_INI_MANIFEST = RUN_DIR / "tester_ini_manifest.csv"
TESTER_IDENTITY_CONTRACT = RUN_DIR / "tester_identity_contract.csv"
RUNTIME_PARITY_CONTRACT = RUN_DIR / "runtime_parity_contract.csv"
COMPILE_RESULT = RUN_DIR / "mt5_compile_result.json"
COMPILE_LOG = COMPILE_DIR / "ObsidianPrimeV2_RuntimeProbeEA_compile.log"
PORTABLE_EA_SYNC = RUN_DIR / "portable_ea_sync.json"
RUNTIME_PROBE_ATTEMPT_PACKAGE = RUN_DIR / "runtime_probe_attempt_package.csv"
TERMINAL_PROCESS_AUDIT = RUN_DIR / "terminal_process_audit.json"
MT5_EXECUTION_RESULT = RUN_DIR / "mt5_execution_result.json"
RUNTIME_OUTPUT_VALIDATION = RUN_DIR / "runtime_output_validation.json"
STRATEGY_TESTER_REPORTS = RUN_DIR / "strategy_tester_report_records.json"
RUNTIME_OUTPUT_COPY = RUN_DIR / "runtime_output_copy_manifest.csv"
RUNTIME_SCOREBOARD = RUN_DIR / "runtime_probe_scoreboard.csv"
PROXY_MT5_DIFF = RUN_DIR / "proxy_mt5_runtime_difference.csv"
RUNTIME_EVIDENCE_GATE = RUN_DIR / "runtime_evidence_gate.json"
BACKTEST_RECEIPT = RUN_DIR / "backtest_forensics_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / "run364CA_bx03_guard_stack_runtime_probe.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364CA_bx03_guard_stack_runtime_probe.md"
REVIEW_INDEX = REVIEW_DIR / "review_index.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"
STAGE_README = STAGE_DIR / "README.md"
SELECTION_STATUS = SELECTED_DIR / "selection_status.md"

WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
PROJECT_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
IDEA_REGISTRY = ROOT / "docs" / "registers" / "idea_registry.md"

SOURCE_BZ_FINAL = bz.FINAL_DECISION
SOURCE_BZ_QUEUE = bz.RUNTIME_ATTEMPT_QUEUE
SOURCE_BZ_MATRIX = bz.GUARD_CANDIDATE_MATRIX
SOURCE_BZ_PROXY_IMPACT = bz.GUARD_CANDIDATE_PROXY_IMPACT
SOURCE_BZ_GATE = bz.GATE_AUDIT
SOURCE_BX_FINAL = bx.FINAL_DECISION
SOURCE_BX_SCOREBOARD = bx.ABLATION_SCOREBOARD
SOURCE_BV_FINAL = bv.FINAL_DECISION
SOURCE_FEATURE_MATRIX = bx.SOURCE_FEATURE_MATRIX
SOURCE_FEATURE_ORDER = bx.SOURCE_FEATURE_ORDER
SOURCE_ONNX = bx.SOURCE_ONNX
SOURCE_PROBABILITY_TAPE = bx.SOURCE_PROBABILITY_TAPE
SOURCE_SELECTED_CANDIDATE = bx.SOURCE_SELECTED_CANDIDATE
SOURCE_EA = bx.SOURCE_EA
SOURCE_EA_BINARY = bx.SOURCE_EA_BINARY
SOURCE_BV_SET = bx.SOURCE_BV_SET
MT5_INPUT_CONTRACT = bx.MT5_INPUT_CONTRACT

COMMON_ROOT = f"Project_Obsidian_Prime_v2/stage364/{RUN_NUMBER}_bx03_guard_stack_runtime_probe"
COMMON_FEATURE = f"{COMMON_ROOT}/features/density_lift_trade_shape_features.csv"
COMMON_MODEL = f"{COMMON_ROOT}/models/{MODEL_ID}.onnx"
COMMON_FEATURE_ORDER = f"{COMMON_ROOT}/config/feature_order.json"
COMMON_PROBABILITY = f"{COMMON_ROOT}/expected/density_lift_expected_probability_tape.csv"
COMMON_SELECTED = f"{COMMON_ROOT}/config/selected_bs_candidate.json"
COMMON_POLICY = f"{COMMON_ROOT}/config/runtime_policy_config.json"

INPUT_FILES = [
    SOURCE_BZ_FINAL,
    SOURCE_BZ_QUEUE,
    SOURCE_BZ_MATRIX,
    SOURCE_BZ_PROXY_IMPACT,
    SOURCE_BZ_GATE,
    SOURCE_BX_FINAL,
    SOURCE_BX_SCOREBOARD,
    SOURCE_BV_FINAL,
    SOURCE_FEATURE_MATRIX,
    SOURCE_FEATURE_ORDER,
    SOURCE_ONNX,
    SOURCE_PROBABILITY_TAPE,
    SOURCE_SELECTED_CANDIDATE,
    SOURCE_EA,
    SOURCE_BV_SET,
    MT5_INPUT_CONTRACT,
]

OUTPUT_FILES = [
    INPUT_MANIFEST,
    WORK_PACKET,
    RUNTIME_POLICY_CONFIG,
    COMMON_FILES_SYNC,
    TESTER_SET_MANIFEST,
    TESTER_INI_MANIFEST,
    TESTER_IDENTITY_CONTRACT,
    RUNTIME_PARITY_CONTRACT,
    COMPILE_RESULT,
    COMPILE_LOG,
    PORTABLE_EA_SYNC,
    RUNTIME_PROBE_ATTEMPT_PACKAGE,
    TERMINAL_PROCESS_AUDIT,
    MT5_EXECUTION_RESULT,
    RUNTIME_OUTPUT_VALIDATION,
    STRATEGY_TESTER_REPORTS,
    RUNTIME_OUTPUT_COPY,
    RUNTIME_SCOREBOARD,
    PROXY_MT5_DIFF,
    RUNTIME_EVIDENCE_GATE,
    BACKTEST_RECEIPT,
    RUNTIME_RECEIPT,
    LINEAGE_RECEIPT,
    JUDGMENT_RECEIPT,
    CLAIM_RECEIPT,
    GATE_AUDIT,
    FINAL_DECISION,
    RUN_MANIFEST,
    REPORT_PATH,
    DECISION_DOC,
    REVIEW_INDEX,
    STAGE_LEDGER,
    STAGE_README,
    SELECTION_STATUS,
    WORKSPACE_STATE,
    CURRENT_WORKING_STATE,
    WORKSPACE_CHANGELOG,
    RUN_REGISTRY,
    PROJECT_LEDGER,
    ARTIFACT_REGISTRY,
    IDEA_REGISTRY,
    Path(__file__),
]


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    return bx.rel(path)


def exists(path: Path | str) -> bool:
    return path_exists(Path(path))


def sha(path: Path | str) -> str:
    candidate = Path(path)
    return sha256_file(candidate) if exists(candidate) and io_path(candidate).is_file() else ""


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: Any) -> None:
    bx.write_json(path, json_ready(payload))


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    bx.write_csv(path, rows, fieldnames)


def write_text(path: Path, text: str, *, bom: bool = True) -> None:
    bx.write_text(path, text, bom=bom)


def append_text_once(path: Path, marker: str, text: str) -> None:
    bx.append_text_once(path, marker, text)


def append_or_replace_csv(path: Path, key_fields: Sequence[str], rows: Sequence[Mapping[str, Any]], *, extend_header: bool = True) -> None:
    bx.append_or_replace_csv(path, key_fields, rows, extend_header=extend_header)


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
        except (TypeError, ValueError):
            pass
    if isinstance(value, float):
        return value if math.isfinite(value) else None
    return value


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        if value in ("", None):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def finite(value: Any, digits: int = 10) -> float | str:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return ""
    if not math.isfinite(number):
        return "inf" if number > 0 else "-inf"
    return round(number, digits)


def markdown_table(rows: Sequence[Mapping[str, Any]], columns: Sequence[str], limit: int = 12) -> str:
    if not rows:
        return "_none(없음)_"
    shown = list(rows)[:limit]
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join(["---"] * len(columns)) + " |"
    body = ["| " + " | ".join(str(row.get(col, "")).replace("|", "\\|") for col in columns) + " |" for row in shown]
    return "\n".join([header, sep, *body])


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skip-mt5", action="store_true", help="Prepare and compile only(준비와 컴파일만 수행).")
    parser.add_argument("--timeout-seconds", type=int, default=900)
    parser.add_argument("--include-deferred", action="store_true", help="Also run deferred proxy-negative controls(보류된 프록시 부정 대조도 실행).")
    return parser.parse_args()


def ensure_dirs() -> None:
    for path in [RUN_DIR, SET_DIR, INI_DIR, COMPILE_DIR, REPORT_COPY_DIR, TELEMETRY_COPY_DIR, REVIEW_DIR, SELECTED_DIR, DECISION_DOC.parent]:
        io_path(path).mkdir(parents=True, exist_ok=True)


def validate_inputs() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    missing = [rel(path) for path in INPUT_FILES if not exists(path)]
    if missing:
        raise FileNotFoundError("missing CA inputs(CA 입력 누락): " + ", ".join(missing))
    bz_final = read_json(SOURCE_BZ_FINAL)
    bx_final = read_json(SOURCE_BX_FINAL)
    bv_final = read_json(SOURCE_BV_FINAL)
    if bz_final.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"BZ next_run_id mismatch(BZ 다음 실행 불일치): {bz_final.get('next_run_id')} != {RUN_ID}")
    forbidden = ["runtime_authority", "operating_promotion", "goal_achieve"]
    if any(bz_final.get(key) != "not_claimed" for key in forbidden):
        raise RuntimeError("BZ has forbidden authority claim(BZ 금지 권위 주장 존재)")
    return bz_final, bx_final, bv_final


def input_manifest_rows() -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "input_path": rel(path),
            "exists": exists(path),
            "sha256": sha(path),
            "input_role": "CA runtime probe source(CA 런타임 탐침 원천)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for path in INPUT_FILES
    ]


def queue_to_variants(include_deferred: bool) -> list[dict[str, Any]]:
    rows = list(csv.DictReader(io_path(SOURCE_BZ_QUEUE).open("r", encoding="utf-8-sig", newline="")))
    selected = [row for row in rows if include_deferred or str(row.get("queue_status", "")).startswith("ready_for_runtime_probe")]
    selected.sort(key=lambda row: int(float(row.get("runtime_priority", 999))))
    variants: list[dict[str, Any]] = []
    for row in selected:
        candidate_id = str(row["candidate_id"])
        short_id = candidate_id.replace("ca", "")
        attempt_name = f"run364CA_{candidate_id}"
        variants.append(
            {
                "variant_id": candidate_id,
                "attempt_name": attempt_name,
                "report_name": f"OPv2_run364CA_{candidate_id}",
                "split": f"validation_oos_{candidate_id}",
                "synthetic_enabled": str(row.get("synthetic_enabled", "")).lower() == "true",
                "synthetic_hours": row.get("synthetic_hours", ""),
                "synthetic_p_short_min": as_float(row.get("synthetic_p_short_min"), 0.4375),
                "synthetic_margin_vs_long_min": as_float(row.get("synthetic_margin_vs_long_min"), 0.075),
                "calendar_enabled": str(row.get("calendar_enabled", "")).lower() == "true",
                "calendar_side": row.get("calendar_side", "long"),
                "calendar_month": int(float(row.get("calendar_month") or 0)),
                "calendar_start_hour": int(float(row.get("calendar_start_hour") or 0)),
                "calendar_end_hour": int(float(row.get("calendar_end_hour") or 24)),
                "magic": 36427000 + int(float(row.get("runtime_priority", 0))),
                "hypothesis": f"{candidate_id} guard stack runtime probe({candidate_id} 가드 묶음 런타임 탐침)",
                "queue_status": row.get("queue_status", ""),
                "covered_hours": row.get("covered_hours", ""),
                "proxy_estimable": row.get("proxy_estimable", ""),
                "estimated_net": row.get("estimated_net", ""),
                "estimated_density": row.get("estimated_density", ""),
                "short_id": short_id,
            }
        )
    return variants


def patch_bx_runtime_globals(variants: Sequence[Mapping[str, Any]]) -> None:
    bx.__file__ = str(Path(__file__))
    bx.TODAY = TODAY
    bx.RUN_NUMBER = RUN_NUMBER
    bx.RUN_ID = RUN_ID
    bx.PARENT_RUN_ID = PARENT_RUN_ID
    bx.BASELINE_RUN_ID = BASELINE_BV_RUN_ID
    bx.NEXT_RUN_ID = NEXT_RUN_ID
    bx.EXPLORATION_LABEL = EXPLORATION_LABEL
    bx.CLAIM_BOUNDARY = CLAIM_BOUNDARY
    bx.RUN_DIR = RUN_DIR
    bx.MT5_DIR = MT5_DIR
    bx.SET_DIR = SET_DIR
    bx.INI_DIR = INI_DIR
    bx.COMPILE_DIR = COMPILE_DIR
    bx.REPORT_COPY_DIR = REPORT_COPY_DIR
    bx.TELEMETRY_COPY_DIR = TELEMETRY_COPY_DIR
    bx.INPUT_MANIFEST = INPUT_MANIFEST
    bx.WORK_PACKET = WORK_PACKET
    bx.RUNTIME_POLICY_CONFIG = RUNTIME_POLICY_CONFIG
    bx.COMMON_FILES_SYNC = COMMON_FILES_SYNC
    bx.TESTER_SET_MANIFEST = TESTER_SET_MANIFEST
    bx.TESTER_INI_MANIFEST = TESTER_INI_MANIFEST
    bx.TESTER_IDENTITY_CONTRACT = TESTER_IDENTITY_CONTRACT
    bx.RUNTIME_PARITY_CONTRACT = RUNTIME_PARITY_CONTRACT
    bx.COMPILE_RESULT = COMPILE_RESULT
    bx.COMPILE_LOG = COMPILE_LOG
    bx.PORTABLE_EA_SYNC = PORTABLE_EA_SYNC
    bx.RUNTIME_PROBE_ATTEMPT_PACKAGE = RUNTIME_PROBE_ATTEMPT_PACKAGE
    bx.TERMINAL_PROCESS_AUDIT = TERMINAL_PROCESS_AUDIT
    bx.MT5_EXECUTION_RESULT = MT5_EXECUTION_RESULT
    bx.RUNTIME_OUTPUT_VALIDATION = RUNTIME_OUTPUT_VALIDATION
    bx.STRATEGY_TESTER_REPORTS = STRATEGY_TESTER_REPORTS
    bx.RUNTIME_OUTPUT_COPY = RUNTIME_OUTPUT_COPY
    bx.ABLATION_SCOREBOARD = RUNTIME_SCOREBOARD
    bx.PROXY_MT5_DIFF = PROXY_MT5_DIFF
    bx.RUNTIME_EVIDENCE_GATE = RUNTIME_EVIDENCE_GATE
    bx.BACKTEST_RECEIPT = BACKTEST_RECEIPT
    bx.RUNTIME_RECEIPT = RUNTIME_RECEIPT
    bx.LINEAGE_RECEIPT = LINEAGE_RECEIPT
    bx.JUDGMENT_RECEIPT = JUDGMENT_RECEIPT
    bx.CLAIM_RECEIPT = CLAIM_RECEIPT
    bx.GATE_AUDIT = GATE_AUDIT
    bx.FINAL_DECISION = FINAL_DECISION
    bx.RUN_MANIFEST = RUN_MANIFEST
    bx.REPORT_PATH = REPORT_PATH
    bx.DECISION_DOC = DECISION_DOC
    bx.COMMON_ROOT = COMMON_ROOT
    bx.COMMON_FEATURE = COMMON_FEATURE
    bx.COMMON_MODEL = COMMON_MODEL
    bx.COMMON_FEATURE_ORDER = COMMON_FEATURE_ORDER
    bx.COMMON_PROBABILITY = COMMON_PROBABILITY
    bx.COMMON_SELECTED = COMMON_SELECTED
    bx.COMMON_POLICY = COMMON_POLICY
    bx.INPUT_FILES = INPUT_FILES
    bx.OUTPUT_FILES = OUTPUT_FILES
    bx.VARIANTS = [dict(row) for row in variants]


def build_runtime_policy(variants: Sequence[Mapping[str, Any]], selected: Mapping[str, Any], bx_final: Mapping[str, Any]) -> dict[str, Any]:
    policy = bx.build_runtime_policy(variants, selected, bx_final)
    policy["parent_run_id"] = PARENT_RUN_ID
    policy["source_queue"] = rel(SOURCE_BZ_QUEUE)
    policy["probe_question"] = "Which BX3 guard stack improves MT5 KPI without density collapse?(어떤 BX3 가드 묶음이 밀도 붕괴 없이 MT5 KPI를 개선하는가?)"
    write_json(RUNTIME_POLICY_CONFIG, policy)
    return policy


def augment_scoreboard(scoreboard: Sequence[Mapping[str, Any]], bx_final: Mapping[str, Any]) -> list[dict[str, Any]]:
    bx3_net = as_float(bx_final.get("best_mt5_net_profit"))
    bx3_pf = as_float(bx_final.get("best_mt5_profit_factor"))
    bx3_trades = as_float(bx_final.get("best_mt5_trade_count"))
    bx3_recovery = as_float(bx_final.get("best_mt5_recovery_factor"))
    out = []
    for row in scoreboard:
        enriched = dict(row)
        if row.get("mt5_status") == "completed":
            enriched["net_diff_vs_bx3"] = finite(as_float(row.get("net_profit")) - bx3_net)
            enriched["pf_diff_vs_bx3"] = finite(as_float(row.get("profit_factor")) - bx3_pf)
            enriched["trade_diff_vs_bx3"] = finite(as_float(row.get("trade_count")) - bx3_trades)
            enriched["recovery_diff_vs_bx3"] = finite(as_float(row.get("recovery_factor")) - bx3_recovery)
        else:
            enriched["net_diff_vs_bx3"] = ""
            enriched["pf_diff_vs_bx3"] = ""
            enriched["trade_diff_vs_bx3"] = ""
            enriched["recovery_diff_vs_bx3"] = ""
        out.append(enriched)
    write_csv(RUNTIME_SCOREBOARD, out)
    return out


def final_status(scoreboard: Sequence[Mapping[str, Any]], compile_result: Mapping[str, Any], runtime_outputs: Sequence[Mapping[str, Any]], expected_attempt_count: int) -> tuple[str, str, str]:
    if compile_result.get("status") != "completed":
        return (
            "blocked_stage364CA_compile_failed_no_authority",
            "blocked_bx03_guard_stack_compile_failed_no_authority",
            "stage364CA_repair_compile_or_ea_source",
        )
    completed_outputs = sum(1 for row in runtime_outputs if row.get("status") == "completed")
    metric_rows = [row for row in scoreboard if row.get("mt5_status") == "completed"]
    if completed_outputs == expected_attempt_count and len(metric_rows) == expected_attempt_count:
        best = metric_rows[0]
        return (
            "completed_stage364CA_bx03_guard_stack_mt5_probe_executed_review_required_no_authority",
            f"runtime_probe_completed_best_{best['variant_id']}_review_required_no_authority",
            "stage364CA_open_run364CB_bx03_guard_stack_runtime_probe_review",
        )
    if metric_rows:
        return (
            "incomplete_stage364CA_partial_mt5_probe_metrics_available_no_authority",
            "partial_guard_stack_runtime_metrics_available_review_required_no_authority",
            "stage364CA_review_partial_or_repair_missing_attempts",
        )
    return (
        "blocked_stage364CA_runtime_probe_outputs_missing_or_report_missing_no_authority",
        "blocked_guard_stack_runtime_outputs_or_report_missing_no_authority",
        "stage364CA_repair_mt5_output_or_report_collection",
    )


def final_payload(
    bz_final: Mapping[str, Any],
    bx_final: Mapping[str, Any],
    bv_final: Mapping[str, Any],
    compile_result: Mapping[str, Any],
    portable_sync: Mapping[str, Any],
    runtime_outputs: Sequence[Mapping[str, Any]],
    report_records: Sequence[Mapping[str, Any]],
    scoreboard: Sequence[Mapping[str, Any]],
    gates: Sequence[Mapping[str, Any]],
    status: str,
    judgment: str,
    decision: str,
    created_at: str,
) -> dict[str, Any]:
    best = dict(scoreboard[0]) if scoreboard else {}
    completed_attempts = sum(1 for row in runtime_outputs if row.get("status") == "completed")
    return {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "created_at_utc": created_at,
        "parent_run_id": PARENT_RUN_ID,
        "baseline_bx_run_id": BASELINE_BX_RUN_ID,
        "baseline_bv_run_id": BASELINE_BV_RUN_ID,
        "status": status,
        "judgment": judgment,
        "decision": decision,
        "next_run_id": NEXT_RUN_ID,
        "variant_count": len(scoreboard),
        "runtime_completed_attempts": completed_attempts,
        "strategy_report_count": len(report_records),
        "best_variant_id": best.get("variant_id", ""),
        "best_mt5_net_profit": best.get("net_profit", ""),
        "best_mt5_profit_factor": best.get("profit_factor", ""),
        "best_mt5_expectancy": best.get("expectancy", ""),
        "best_mt5_trade_count": best.get("trade_count", ""),
        "best_mt5_density": best.get("trade_density_per_feature_business_day", ""),
        "best_mt5_recovery_factor": best.get("recovery_factor", ""),
        "best_mt5_equity_drawdown_amount": best.get("equity_drawdown_amount", ""),
        "best_mt5_long_trade_count": best.get("long_trade_count", ""),
        "best_mt5_short_trade_count": best.get("short_trade_count", ""),
        "best_net_diff_vs_bv": best.get("net_diff_vs_bv", ""),
        "best_net_diff_vs_bx3": best.get("net_diff_vs_bx3", ""),
        "bx3_mt5_net_profit": bx_final.get("best_mt5_net_profit"),
        "bx3_mt5_profit_factor": bx_final.get("best_mt5_profit_factor"),
        "bx3_mt5_trade_count": bx_final.get("best_mt5_trade_count"),
        "bx3_mt5_recovery_factor": bx_final.get("best_mt5_recovery_factor"),
        "bx3_mt5_equity_drawdown_amount": bx_final.get("best_mt5_equity_drawdown_amount"),
        "bv_mt5_net_profit": bx_final.get("bv_mt5_net_profit") or bv_final.get("mt5_net_profit"),
        "bv_mt5_profit_factor": bx_final.get("bv_mt5_profit_factor") or bv_final.get("mt5_profit_factor"),
        "bv_mt5_trade_count": bx_final.get("bv_mt5_trade_count") or bv_final.get("mt5_trade_count"),
        "bz_runtime_ready_candidate_count": bz_final.get("runtime_ready_candidate_count"),
        "compile_status": compile_result.get("status"),
        "portable_ea_copied": portable_sync.get("copied"),
        "gate_passes": sum(1 for row in gates if row.get("status") == "passed"),
        "gate_total": len(gates),
        "new_model_training": "not_run",
        "new_mt5_execution": "completed" if completed_attempts else "attempted_or_blocked",
        "forward_passed": "not_claimed",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "live_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def write_receipts(final: Mapping[str, Any]) -> None:
    write_json(
        BACKTEST_RECEIPT,
        {
            "run_id": RUN_ID,
            "tester_identity": rel(TESTER_IDENTITY_CONTRACT),
            "ea_identity": [rel(SOURCE_EA), rel(COMPILE_RESULT), rel(PORTABLE_EA_SYNC)],
            "report_identity": rel(STRATEGY_TESTER_REPORTS),
            "trade_evidence": rel(RUNTIME_SCOREBOARD),
            "cost_assumptions": "FPMarkets US100 M5 Strategy Tester real ticks; broker report costs used(FPMarkets US100 M5 전략 테스터 실제 틱, 브로커 보고서 비용 사용)",
            "forensic_checks": [rel(RUNTIME_OUTPUT_VALIDATION), rel(RUNTIME_EVIDENCE_GATE), rel(TESTER_IDENTITY_CONTRACT)],
            "backtest_judgment": "usable_with_boundary(경계부 사용 가능)" if final["runtime_completed_attempts"] else "blocked_or_incomplete(차단 또는 불완전)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(
        RUNTIME_RECEIPT,
        {
            "run_id": RUN_ID,
            "research_path": rel(SOURCE_BZ_QUEUE),
            "runtime_path": [rel(TESTER_SET_MANIFEST), rel(TESTER_INI_MANIFEST), rel(SOURCE_EA), rel(RUNTIME_POLICY_CONFIG)],
            "shared_contract": "same ONNX, same feature order, same max_hold=6, candidate-only calendar/overlay parameters(같은 ONNX, 같은 피처 순서, 같은 max_hold=6, 후보별 달력/오버레이 파라미터만 변경)",
            "known_differences": "MT5 tick fills/costs and position lifecycle can differ from proxy(MT5 틱 체결/비용/포지션 생명주기는 프록시와 다를 수 있음)",
            "parity_check": [rel(COMPILE_RESULT), rel(RUNTIME_OUTPUT_VALIDATION), rel(RUNTIME_SCOREBOARD)],
            "runtime_claim_boundary": "runtime_probe_only(런타임 탐침 한정)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(
        LINEAGE_RECEIPT,
        {
            "run_id": RUN_ID,
            "source_inputs": [{"path": rel(path), "sha256": sha(path)} for path in INPUT_FILES if exists(path)],
            "producer": rel(Path(__file__)),
            "consumer": final["next_run_id"],
            "artifact_paths": [rel(path) for path in OUTPUT_FILES if exists(path)],
            "artifact_hashes": {rel(path): sha(path) for path in OUTPUT_FILES if exists(path) and io_path(Path(path)).is_file()},
            "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "availability": "tracked_after_closeout(종료 후 추적됨)",
            "lineage_judgment": "connected_with_runtime_probe_boundary(런타임 탐침 경계 내 연결됨)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(
        JUDGMENT_RECEIPT,
        {
            "run_id": RUN_ID,
            "result_subject": "BX3 guard stack MT5 runtime probe(BX3 가드 묶음 MT5 런타임 탐침)",
            "evidence_available": [rel(MT5_EXECUTION_RESULT), rel(STRATEGY_TESTER_REPORTS), rel(RUNTIME_SCOREBOARD), rel(RUNTIME_EVIDENCE_GATE)],
            "evidence_missing": ["forward replay", "runtime authority audit", "live shadow"],
            "judgment_label": final["judgment"],
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": final["next_run_id"],
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            "run_id": RUN_ID,
            "allowed_claim": final["judgment"],
            "forbidden_claims": ["runtime_authority", "operating_promotion", "live_readiness", "goal_achieve"],
            "new_model_training": final["new_model_training"],
            "new_mt5_execution": final["new_mt5_execution"],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def write_docs(final: Mapping[str, Any], scoreboard: Sequence[Mapping[str, Any]], gates: Sequence[Mapping[str, Any]]) -> None:
    report = f"""# run364CA bx03 guard stack runtime probe(364CA BX3 가드 묶음 런타임 탐침)

## Result(결과)

Action(행동): BZ queue(BZ 대기열)의 ready candidates(준비 후보) 4개를 같은 ONNX(온엑스), 같은 feature order(피처 순서), 같은 MT5 Strategy Tester(MT5 전략 테스터) 조건으로 실행했다.

Effect(효과): h22-only isolation(h22 단독 분리), h21-h23 stress(h21-h23 압박), native-short same-calendar control(같은 달력 기본 숏 대조)이 BX3/BV 대비 실제 수익 구조를 바꾸는지 MT5 KPI(MT5 핵심 성과 지표)로 확인했다.

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- best variant(최선 변형): `{final['best_variant_id']}`
- best MT5 net/PF/trades(최선 MT5 순수익/수익 팩터/거래수): `{final['best_mt5_net_profit']}` / `{final['best_mt5_profit_factor']}` / `{final['best_mt5_trade_count']}`
- best density/recovery/equity DD(최선 밀도/회복/평가손익 낙폭): `{final['best_mt5_density']}` / `{final['best_mt5_recovery_factor']}` / `{final['best_mt5_equity_drawdown_amount']}`
- diff vs BX3/BV(BX3/BV 대비 차이): `{final['best_net_diff_vs_bx3']}` / `{final['best_net_diff_vs_bv']}`

## Scoreboard(점수표)

{markdown_table(scoreboard, ['variant_id', 'net_profit', 'profit_factor', 'trade_count', 'trade_density_per_feature_business_day', 'recovery_factor', 'equity_drawdown_amount', 'long_trade_count', 'short_trade_count', 'net_diff_vs_bx3', 'net_diff_vs_bv', 'selection_status'])}

## Gates(게이트)

{markdown_table(gates, ['gate', 'status', 'evidence'], 10)}

## Boundary(경계)

runtime probe(런타임 탐침)만 주장한다. runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)이다.
"""
    write_text(REPORT_PATH, report, bom=True)
    write_text(
        DECISION_DOC,
        f"""# Decision: Stage364CA bx03 guard stack runtime probe(결정: BX3 가드 묶음 런타임 탐침)

- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{NEXT_RUN_ID}`

Action(행동): BZ ready queue(BZ 준비 대기열)를 MT5 runtime probe(MT5 런타임 탐침)로 실행했다.

Effect(효과): best variant(최선 변형) `{final['best_variant_id']}`의 MT5 net/PF/trades(순수익/수익 팩터/거래수)는 `{final['best_mt5_net_profit']}` / `{final['best_mt5_profit_factor']}` / `{final['best_mt5_trade_count']}`이고, BX3 대비 net diff(순수익 차이)는 `{final['best_net_diff_vs_bx3']}`다.

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
        bom=True,
    )
    append_text_once(REVIEW_INDEX, "<!-- run364CA -->", f"\n<!-- run364CA -->\n- `{RUN_ID}`: bx03 guard stack MT5 runtime probe(BX3 가드 묶음 MT5 런타임 탐침) -> `{rel(REPORT_PATH)}`\n")
    append_text_once(STAGE_README, "<!-- run364CA -->", f"\n<!-- run364CA -->\n## run364CA bx03 guard stack runtime probe(BX3 가드 묶음 런타임 탐침)\n\n`{final['judgment']}`. Next(다음): `{NEXT_RUN_ID}`.\n")
    write_text(
        WORKSPACE_STATE,
        f"""current_stage_id: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {final['status']}
current_judgment: {final['judgment']}
next_run_id: {NEXT_RUN_ID}
runtime_authority: not_claimed
operating_promotion: not_claimed
goal_achieve: not_claimed
updated_at_utc: {final['created_at_utc']}
""",
        bom=False,
    )
    write_text(
        CURRENT_WORKING_STATE,
        f"""# Current Working State(현재 작업 상태)

Updated(갱신): {final['created_at_utc']}

Active stage(활성 단계): `{STAGE_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Current run(현재 실행): `{NEXT_RUN_ID}`

Current truth(현재 진실): `run364CA` executed(실행 완료) BX3 guard stack MT5 runtime probe(BX3 가드 묶음 MT5 런타임 탐침). Best variant(최선 변형)는 `{final['best_variant_id']}`이고 MT5 net/PF/trades/density(순수익/수익 팩터/거래수/밀도)는 `{final['best_mt5_net_profit']}` / `{final['best_mt5_profit_factor']}` / `{final['best_mt5_trade_count']}` / `{final['best_mt5_density']}`이다.

Next action(다음 행동): `{NEXT_RUN_ID}`에서 CA output(CA 출력)을 source/month/session/equity attribution(원천/월/세션/수익곡선 귀속)으로 review(검토)한다.

Operating boundary(운영 경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함).
""",
        bom=True,
    )
    write_text(
        SELECTION_STATUS,
        f"""# Stage364 selection status(선택 상태)

Updated(갱신): {final['created_at_utc']}

Current run(현재 실행): `{NEXT_RUN_ID}`
Latest completed run(최근 완료 실행): `{RUN_ID}`

Runtime probe best variant(런타임 탐침 최선 변형): `{final['best_variant_id']}`

Best MT5 KPI(최선 MT5 핵심 성과 지표): net `{final['best_mt5_net_profit']}`, PF `{final['best_mt5_profit_factor']}`, trades `{final['best_mt5_trade_count']}`, density `{final['best_mt5_density']}`, recovery `{final['best_mt5_recovery_factor']}`, equity DD `{final['best_mt5_equity_drawdown_amount']}`.

Next action(다음 행동): `{NEXT_RUN_ID}`.

Authority(권위): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함).
""",
        bom=True,
    )
    append_text_once(WORKSPACE_CHANGELOG, "<!-- run364CA -->", f"\n<!-- run364CA -->\n- {final['created_at_utc']} `{RUN_ID}` executed BX3 guard stack MT5 runtime probe(BX3 가드 묶음 MT5 런타임 탐침). Judgment(판정): `{final['judgment']}`.\n")
    append_text_once(IDEA_REGISTRY, "<!-- run364CA_bx3_guard_stack_runtime -->", f"\n<!-- run364CA_bx3_guard_stack_runtime -->\n- Idea(아이디어): December h22-only block(12월 h22 단독 차단), h21-h23 stress(h21-h23 압박), native short same-calendar control(같은 달력 기본 숏 대조)를 MT5 runtime probe(MT5 런타임 탐침)로 분리한다. Effect(효과): BX3 개선이 calendar semantics(달력 의미)인지 synthetic overlay(합성 오버레이)인지 더 선명하게 판별한다.\n")


def write_ledgers(final: Mapping[str, Any]) -> None:
    common = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "date": TODAY,
        "lane": "runtime_probe(런타임 탐침)",
        "family": "runtime_backtest(런타임 백테스트)",
        "status": final["status"],
        "judgment": final["judgment"],
        "decision": final["decision"],
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "rows": final["variant_count"],
        "gate_passes": final["gate_passes"],
        "gate_total": final["gate_total"],
        "claim_boundary": CLAIM_BOUNDARY,
        "path": rel(FINAL_DECISION),
        "report_path": rel(REPORT_PATH),
        "primary_report": rel(REPORT_PATH),
        "primary_artifact": rel(FINAL_DECISION),
        "result_status": final["status"],
        "net_profit": final["best_mt5_net_profit"],
        "profit_factor": final["best_mt5_profit_factor"],
        "expectancy": final["best_mt5_expectancy"],
        "trade_count": final["best_mt5_trade_count"],
        "trade_density_per_feature_day": final["best_mt5_density"],
        "recovery_factor": final["best_mt5_recovery_factor"],
        "max_drawdown_amount": final["best_mt5_equity_drawdown_amount"],
        "long_trade_count": final["best_mt5_long_trade_count"],
        "short_trade_count": final["best_mt5_short_trade_count"],
        "trade_density_requirement_status": "passed_density_floor(밀도 하한 통과)" if as_float(final["best_mt5_density"]) >= 3.0 else "failed_density_floor(밀도 하한 실패)",
        "result_judgment": final["judgment"],
        "final_decision_path": rel(FINAL_DECISION),
        "gate_audit_path": rel(GATE_AUDIT),
        "created_at": final["created_at_utc"],
        "work_family": "runtime_backtest(런타임 백테스트)",
        "evidence_boundary": "runtime_probe_only(런타임 탐침 한정)",
        "next_action": NEXT_RUN_ID,
        "question": "Which BX3 guard stack improves MT5 KPI without density collapse?(어떤 BX3 가드 묶음이 밀도 붕괴 없이 MT5 KPI를 개선하는가?)",
    }
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], [common], extend_header=True)
    ledger_rows = []
    for view, tier, scope in [
        ("Tier A used(Tier A 사용)", "Tier A", "runtime_probe"),
        ("Tier B fallback used(Tier B 대체 사용)", "Tier B", "missing_required"),
        ("actual routed total(실제 라우팅 전체)", "Tier A+B", "runtime_probe"),
    ]:
        ledger_rows.append(
            {
                **common,
                "ledger_row_id": f"{RUN_ID}::{tier.replace(' ', '_').replace('+', 'B')}",
                "record_view": view,
                "tier_scope": tier,
                "kpi_scope": scope,
                "view": view,
                "tier": tier,
                "metric_scope": scope,
                "external_verification_status": "mt5_strategy_tester_completed(MT5 전략 테스터 완료)" if final["runtime_completed_attempts"] else "mt5_strategy_tester_incomplete(MT5 전략 테스터 불완전)",
                "notes": "Tier B missing_required(Tier B 필수 누락); no fallback source(대체 원천 없음).",
            }
        )
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], ledger_rows, extend_header=True)
    append_or_replace_csv(STAGE_LEDGER, ["ledger_row_id"], ledger_rows, extend_header=True)
    artifact_rows = []
    for artifact_type, path in [
        ("final_decision", FINAL_DECISION),
        ("runtime_scoreboard", RUNTIME_SCOREBOARD),
        ("mt5_execution_result", MT5_EXECUTION_RESULT),
        ("strategy_tester_reports", STRATEGY_TESTER_REPORTS),
        ("runtime_output_validation", RUNTIME_OUTPUT_VALIDATION),
        ("report", REPORT_PATH),
        ("script", Path(__file__)),
        ("gate_audit", GATE_AUDIT),
    ]:
        artifact_rows.append(
            {
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "artifact_type": artifact_type,
                "path": rel(path),
                "sha256": sha(path),
                "created_at": final["created_at_utc"],
                "claim_boundary": CLAIM_BOUNDARY,
                "artifact_id": f"{RUN_NUMBER}_{artifact_type}",
                "created_at_utc": final["created_at_utc"],
                "notes": "runtime probe artifact(런타임 탐침 산출물)",
                "artifact_path": rel(path),
            }
        )
    append_or_replace_csv(ARTIFACT_REGISTRY, ["artifact_id"], artifact_rows, extend_header=True)


def write_run_manifest(final: Mapping[str, Any], attempts: Sequence[Mapping[str, Any]]) -> None:
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "producer": rel(Path(__file__)),
            "attempts": [{key: rel(value) if isinstance(value, Path) else value for key, value in attempt.items() if key not in {"ini"}} for attempt in attempts],
            "inputs": [{"path": rel(path), "sha256": sha(path)} for path in INPUT_FILES if exists(path)],
            "outputs": [{"path": rel(path), "sha256": sha(path)} for path in OUTPUT_FILES if exists(path) and io_path(Path(path)).is_file()],
            "final_decision": rel(FINAL_DECISION),
            "next_run_id": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
            "created_at_utc": final["created_at_utc"],
        },
    )


def main() -> None:
    args = parse_args()
    ensure_dirs()
    created_at = now_utc()
    bz_final, bx_final, bv_final = validate_inputs()
    variants = queue_to_variants(args.include_deferred)
    if not variants:
        raise RuntimeError("no CA variants selected(CA 변형 선택 없음)")
    patch_bx_runtime_globals(variants)
    write_csv(INPUT_MANIFEST, input_manifest_rows())
    write_json(
        WORK_PACKET,
        {
            "run_id": RUN_ID,
            "primary_family": "runtime_backtest(런타임 백테스트)",
            "primary_skill": "obsidian-runtime-parity(런타임 동등성)",
            "support_skills": [
                "obsidian-backtest-forensics(백테스트 포렌식)",
                "obsidian-artifact-lineage(산출물 계보)",
                "obsidian-result-judgment(결과 판정)",
            ],
            "required_gates": ["runtime_evidence_gate", "scope_completion_gate", "kpi_contract_audit", "required_gate_coverage_audit", "final_claim_guard"],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    selected = read_json(SOURCE_SELECTED_CANDIDATE)
    build_runtime_policy(variants, selected, bx_final)
    bx.materialize_common_files()
    attempts = bx.materialize_attempts(variants)
    compile_result, portable_sync = bx.compile_and_sync()
    _results, runtime_outputs, report_records, _copy_rows = bx.execute_mt5(args, attempts, compile_result, portable_sync)
    scoreboard, _diff_rows = bx.build_scoreboard(attempts, report_records, runtime_outputs, bx_final, bv_final)
    scoreboard = augment_scoreboard(scoreboard, bx_final)
    status, judgment, decision = final_status(scoreboard, compile_result, runtime_outputs, len(attempts))
    gates = bx.gate_rows(compile_result, portable_sync, runtime_outputs, report_records, scoreboard, len(attempts))
    write_csv(GATE_AUDIT, gates)
    final = final_payload(bz_final, bx_final, bv_final, compile_result, portable_sync, runtime_outputs, report_records, scoreboard, gates, status, judgment, decision, created_at)
    write_json(FINAL_DECISION, final)
    write_receipts(final)
    write_docs(final, scoreboard, gates)
    write_ledgers(final)
    write_run_manifest(final, attempts)
    write_receipts(final)
    write_run_manifest(final, attempts)
    print(json.dumps(json_ready(final), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
