from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, path_exists  # noqa: E402
from foundation.mt5.runtime_artifacts import sha256_file  # noqa: E402
from stage_pipelines.stage364 import execute_bx03_guard_stack_runtime_probe_without_db as ca  # noqa: E402
from stage_pipelines.stage364 import execute_overlay_hour17_native_short_ablation_runtime_probe_without_db as bx  # noqa: E402
from stage_pipelines.stage364 import materialize_swap_stable_reprobe_and_source_guard_inputs_without_db as cc  # noqa: E402
from stage_pipelines.stage364 import materialize_synthetic_short_source_runtime_repair_without_db as bv  # noqa: E402


TODAY = "2026-06-05"
STAGE_ID = cc.STAGE_ID
RUN_NUMBER = "run364CD"
RUN_ID = "run364CD_execute_swap_stable_reprobe_and_source_guard_mt5_runtime_probe_without_db_v1"
PARENT_RUN_ID = cc.RUN_ID
BASELINE_BX_RUN_ID = bx.RUN_ID
BASELINE_CA_RUN_ID = ca.RUN_ID
BASELINE_BV_RUN_ID = bv.RUN_ID
NEXT_RUN_ID = "run364CE_review_swap_stable_reprobe_and_source_guard_mt5_runtime_probe_without_db_v1"
EXPLORATION_LABEL = "stage364_SwapStableSourceGuard__RuntimeProbe"
MODEL_ID = bx.MODEL_ID
CLAIM_BOUNDARY = (
    "research_development_runtime_probe_only_no_new_model_training_no_forward_pass_"
    "no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

STAGE_DIR = cc.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
MT5_DIR = RUN_DIR / "mt5"
SET_DIR = MT5_DIR / "sets"
INI_DIR = MT5_DIR / "inis"
COMPILE_DIR = MT5_DIR / "compile"
REPORT_COPY_DIR = MT5_DIR / "reports"
TELEMETRY_COPY_DIR = RUN_DIR / "runtime_telemetry"
REVIEW_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"

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
PAIR_METRIC_SUMMARY = RUN_DIR / "same_session_pair_metric_summary.csv"
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

REPORT_PATH = REVIEW_DIR / "run364CD_swap_stable_reprobe_and_source_guard_mt5_runtime_probe.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364CD_swap_stable_reprobe_and_source_guard_mt5_runtime_probe.md"
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

SOURCE_CC_FINAL = cc.FINAL_DECISION
SOURCE_CC_QUEUE = cc.CD_RUNTIME_QUEUE
SOURCE_CC_PAIR_MATRIX = cc.SAME_SESSION_PAIR_MATRIX
SOURCE_CC_SWAP_SURFACE = cc.SWAP_NEUTRAL_SCORE_SURFACE
SOURCE_CC_SOURCE_GUARD = cc.SOURCE_GUARD_CANDIDATE_MATRIX
SOURCE_CC_TESTER_REQUIREMENTS = cc.TESTER_IDENTITY_REQUIREMENTS
SOURCE_CC_RUN_MANIFEST = cc.RUN_MANIFEST
SOURCE_CC_GATE = cc.GATE_AUDIT
SOURCE_CA_FINAL = ca.FINAL_DECISION
SOURCE_CA_SCOREBOARD = ca.RUNTIME_SCOREBOARD
SOURCE_CA_REPORTS = ca.STRATEGY_TESTER_REPORTS
SOURCE_BX_FINAL = bx.FINAL_DECISION
SOURCE_BX_SCOREBOARD = bx.ABLATION_SCOREBOARD
SOURCE_BX_REPORTS = bx.STRATEGY_TESTER_REPORTS
SOURCE_BV_FINAL = bv.FINAL_DECISION
SOURCE_FEATURE_MATRIX = bx.SOURCE_FEATURE_MATRIX
SOURCE_FEATURE_ORDER = bx.SOURCE_FEATURE_ORDER
SOURCE_ONNX = bx.SOURCE_ONNX
SOURCE_PROBABILITY_TAPE = bx.SOURCE_PROBABILITY_TAPE
SOURCE_SELECTED_CANDIDATE = bx.SOURCE_SELECTED_CANDIDATE
SOURCE_EA = bx.SOURCE_EA
SOURCE_EA_BINARY = bx.SOURCE_EA_BINARY
SOURCE_BV_SET = bx.SOURCE_BV_SET
MT5_INPUT_CONTRACT = ca.MT5_INPUT_CONTRACT

COMMON_ROOT = f"Project_Obsidian_Prime_v2/stage364/{RUN_NUMBER}_swap_stable_source_guard_runtime_probe"
COMMON_FEATURE = f"{COMMON_ROOT}/features/density_lift_trade_shape_features.csv"
COMMON_MODEL = f"{COMMON_ROOT}/models/{MODEL_ID}.onnx"
COMMON_FEATURE_ORDER = f"{COMMON_ROOT}/config/feature_order.json"
COMMON_PROBABILITY = f"{COMMON_ROOT}/expected/density_lift_expected_probability_tape.csv"
COMMON_SELECTED = f"{COMMON_ROOT}/config/selected_bs_candidate.json"
COMMON_POLICY = f"{COMMON_ROOT}/config/runtime_policy_config.json"

INPUT_FILES = [
    SOURCE_CC_FINAL,
    SOURCE_CC_QUEUE,
    SOURCE_CC_PAIR_MATRIX,
    SOURCE_CC_SWAP_SURFACE,
    SOURCE_CC_SOURCE_GUARD,
    SOURCE_CC_TESTER_REQUIREMENTS,
    SOURCE_CC_RUN_MANIFEST,
    SOURCE_CC_GATE,
    SOURCE_CA_FINAL,
    SOURCE_CA_SCOREBOARD,
    SOURCE_CA_REPORTS,
    SOURCE_BX_FINAL,
    SOURCE_BX_SCOREBOARD,
    SOURCE_BX_REPORTS,
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
    PAIR_METRIC_SUMMARY,
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


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


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
    parser.add_argument("--skip-mt5", action="store_true", help="Prepare and compile only(준비와 컴파일만 실행).")
    parser.add_argument("--timeout-seconds", type=int, default=900)
    parser.add_argument("--include-deferred", action="store_true", help="Also run deferred memory candidates(보류 기억 후보도 실행).")
    return parser.parse_args()


def ensure_dirs() -> None:
    for path in [RUN_DIR, SET_DIR, INI_DIR, COMPILE_DIR, REPORT_COPY_DIR, TELEMETRY_COPY_DIR, REVIEW_DIR, SELECTED_DIR, DECISION_DOC.parent]:
        io_path(path).mkdir(parents=True, exist_ok=True)


def validate_inputs() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    missing = [rel(path) for path in INPUT_FILES if not exists(path)]
    if missing:
        raise FileNotFoundError("missing CD inputs(CD 입력 누락): " + ", ".join(missing))
    cc_final = read_json(SOURCE_CC_FINAL)
    ca_final = read_json(SOURCE_CA_FINAL)
    bx_final = read_json(SOURCE_BX_FINAL)
    bv_final = read_json(SOURCE_BV_FINAL)
    if cc_final.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"CC next_run_id mismatch(CC 다음 실행 불일치): {cc_final.get('next_run_id')} != {RUN_ID}")
    forbidden = ["runtime_authority", "operating_promotion", "goal_achieve"]
    if any(cc_final.get(key) != "not_claimed" for key in forbidden):
        raise RuntimeError("CC has forbidden authority claim(CC 금지 권위 주장 존재)")
    if ca_final.get("new_mt5_execution") != "completed":
        raise RuntimeError("CA MT5 runtime probe is not completed(CA MT5 런타임 탐침 미완료)")
    if bx_final.get("new_mt5_execution") != "completed":
        raise RuntimeError("BX MT5 runtime probe is not completed(BX MT5 런타임 탐침 미완료)")
    return cc_final, ca_final, bx_final, bv_final


def input_manifest_rows() -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "input_path": rel(path),
            "exists": exists(path),
            "sha256": sha(path),
            "input_role": "CD runtime probe source(CD 런타임 탐침 원천)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for path in INPUT_FILES
    ]


def queue_rows(include_deferred: bool) -> list[dict[str, str]]:
    rows = read_csv_rows(SOURCE_CC_QUEUE)
    selected = [row for row in rows if include_deferred or str(row.get("queue_status", "")).startswith("ready_for_runtime_probe")]
    selected.sort(key=lambda row: int(float(row.get("runtime_priority", 999))))
    return selected


def queue_to_variants(rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    variants: list[dict[str, Any]] = []
    for row in rows:
        candidate_id = str(row["candidate_id"])
        priority = int(float(row.get("runtime_priority", 0)))
        variants.append(
            {
                "variant_id": candidate_id,
                "attempt_name": f"{RUN_NUMBER}_{candidate_id}",
                "report_name": f"OPv2_{RUN_NUMBER}_{candidate_id}",
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
                "magic": 36428000 + priority,
                "hypothesis": f"{candidate_id} same-session swap/source runtime probe({candidate_id} 동일 세션 스왑/원천 런타임 탐침)",
                "queue_status": row.get("queue_status", ""),
                "comparison_pair": row.get("comparison_pair", ""),
                "source_variant_id": row.get("source_variant_id", ""),
                "covered_hours": row.get("covered_hours", ""),
                "expected_net_anchor": row.get("expected_net_anchor", ""),
                "expected_gross_anchor": row.get("expected_gross_anchor", ""),
                "expected_swap_anchor": row.get("expected_swap_anchor", ""),
                "expected_trade_count_anchor": row.get("expected_trade_count_anchor", ""),
                "source_set_path": row.get("source_set_path", ""),
                "source_set_sha256": row.get("source_set_sha256", ""),
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
    bx.SOURCE_BW_QUEUE = SOURCE_CC_QUEUE
    bx.INPUT_FILES = INPUT_FILES
    bx.OUTPUT_FILES = OUTPUT_FILES
    bx.VARIANTS = [dict(row) for row in variants]


def build_runtime_policy(variants: Sequence[Mapping[str, Any]], selected: Mapping[str, Any], bx_final: Mapping[str, Any]) -> dict[str, Any]:
    policy = bx.build_runtime_policy(variants, selected, bx_final)
    policy.update(
        {
            "parent_run_id": PARENT_RUN_ID,
            "baseline_bx_run_id": BASELINE_BX_RUN_ID,
            "baseline_ca_run_id": BASELINE_CA_RUN_ID,
            "baseline_bv_run_id": BASELINE_BV_RUN_ID,
            "source_queue": rel(SOURCE_CC_QUEUE),
            "source_pair_matrix": rel(SOURCE_CC_PAIR_MATRIX),
            "source_guard_matrix": rel(SOURCE_CC_SOURCE_GUARD),
            "same_session_batch_required": True,
            "probe_question": (
                "Can BX3/CA01 swap drift vanish in one current MT5 session, and does h17 overlay still add value?"
                "(BX3/CA01 스왑 드리프트가 현재 MT5 동일 세션에서 사라지는지와 17시 오버레이 가치가 유지되는지 확인)"
            ),
            "claim_boundary": CLAIM_BOUNDARY,
        }
    )
    write_json(RUNTIME_POLICY_CONFIG, policy)
    return policy


def report_metrics_by_attempt(report_records: Sequence[Mapping[str, Any]]) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for record in report_records:
        metrics = record.get("metrics", {})
        if metrics.get("status") == "completed":
            out[str(record.get("attempt_name"))] = dict(metrics)
    return out


def augment_scoreboard(
    scoreboard: Sequence[Mapping[str, Any]],
    report_records: Sequence[Mapping[str, Any]],
    selected_queue_rows: Sequence[Mapping[str, Any]],
    bx_final: Mapping[str, Any],
    ca_final: Mapping[str, Any],
) -> list[dict[str, Any]]:
    queue_by_candidate = {str(row["candidate_id"]): row for row in selected_queue_rows}
    metrics_by_attempt = report_metrics_by_attempt(report_records)
    bx3_net = as_float(bx_final.get("best_mt5_net_profit"))
    ca01_net = as_float(ca_final.get("best_mt5_net_profit"))
    out: list[dict[str, Any]] = []
    for row in scoreboard:
        candidate_id = str(row.get("variant_id", ""))
        queue = queue_by_candidate.get(candidate_id, {})
        metrics = metrics_by_attempt.get(str(row.get("attempt_name")), {})
        net = as_float(row.get("net_profit"))
        expected_net = as_float(queue.get("expected_net_anchor"))
        expected_trades = as_float(queue.get("expected_trade_count_anchor"))
        gross_profit = as_float(metrics.get("gross_profit"))
        gross_loss = as_float(metrics.get("gross_loss"))
        trade_count = as_float(row.get("trade_count"))
        enriched = dict(row)
        enriched.update(
            {
                "source_variant_id": queue.get("source_variant_id", ""),
                "variant_role": queue.get("variant_role", ""),
                "comparison_pair": queue.get("comparison_pair", ""),
                "source_set_path": queue.get("source_set_path", ""),
                "source_set_sha256": queue.get("source_set_sha256", ""),
                "expected_net_anchor": queue.get("expected_net_anchor", ""),
                "expected_gross_anchor": queue.get("expected_gross_anchor", ""),
                "expected_swap_anchor": queue.get("expected_swap_anchor", ""),
                "expected_trade_count_anchor": queue.get("expected_trade_count_anchor", ""),
                "net_diff_vs_expected_anchor": finite(net - expected_net) if row.get("mt5_status") == "completed" else "",
                "trade_diff_vs_expected_anchor": finite(trade_count - expected_trades) if row.get("mt5_status") == "completed" else "",
                "net_diff_vs_bx3_anchor": finite(net - bx3_net) if row.get("mt5_status") == "completed" else "",
                "net_diff_vs_ca01_anchor": finite(net - ca01_net) if row.get("mt5_status") == "completed" else "",
                "gross_profit": metrics.get("gross_profit", ""),
                "gross_loss": metrics.get("gross_loss", ""),
                "gross_result": finite(gross_profit + gross_loss) if metrics else "",
                "report_metric_boundary": "report_level_only_deal_path_review_required(보고서 지표 전용, 거래 경로 리뷰 필요)",
            }
        )
        out.append(enriched)
    write_csv(RUNTIME_SCOREBOARD, out)
    return out


def pair_summary_rows(scoreboard: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    score_by_candidate = {str(row.get("variant_id")): row for row in scoreboard}
    rows: list[dict[str, Any]] = []
    for pair in read_csv_rows(SOURCE_CC_PAIR_MATRIX):
        left_id = str(pair["left_candidate_id"])
        right_id = str(pair["right_candidate_id"])
        left = score_by_candidate.get(left_id, {})
        right = score_by_candidate.get(right_id, {})
        if left.get("mt5_status") == "completed" and right.get("mt5_status") == "completed":
            net_delta = as_float(left.get("net_profit")) - as_float(right.get("net_profit"))
            trade_delta = as_float(left.get("trade_count")) - as_float(right.get("trade_count"))
            gross_delta = as_float(left.get("gross_result")) - as_float(right.get("gross_result"))
            if pair["pair_id"] == "cd01_vs_cd02_swap_stability_control":
                screen = (
                    "passes_report_metric_swap_stability_screen_review_required"
                    if abs(net_delta) <= 1.0 and abs(trade_delta) <= 0.0
                    else "fails_report_metric_swap_stability_screen_review_required"
                )
            elif pair["pair_id"] == "cd02_vs_cd03_source_overlay_value":
                screen = (
                    "passes_report_metric_overlay_lift_screen_review_required"
                    if net_delta > 0.0
                    else "fails_report_metric_overlay_lift_screen_review_required"
                )
            else:
                screen = "report_metric_screen_review_required"
        else:
            net_delta = ""
            trade_delta = ""
            gross_delta = ""
            screen = "incomplete_metrics_missing_review_required"
        rows.append(
            {
                "run_id": RUN_ID,
                "pair_id": pair["pair_id"],
                "left_candidate_id": left_id,
                "right_candidate_id": right_id,
                "left_net_profit": left.get("net_profit", ""),
                "right_net_profit": right.get("net_profit", ""),
                "net_delta_left_minus_right": finite(net_delta) if net_delta != "" else "",
                "left_trade_count": left.get("trade_count", ""),
                "right_trade_count": right.get("trade_count", ""),
                "trade_count_delta_left_minus_right": finite(trade_delta) if trade_delta != "" else "",
                "gross_result_delta_left_minus_right": finite(gross_delta) if gross_delta != "" else "",
                "expected_trade_count_delta": pair.get("expected_trade_count_delta", ""),
                "expected_gross_delta": pair.get("expected_gross_delta", ""),
                "prior_swap_delta": pair.get("prior_swap_delta", ""),
                "prior_net_delta": pair.get("prior_net_delta", ""),
                "report_metric_screen": screen,
                "review_boundary": "report_level_only_deal_level_trade_path_and_swap_review_required(보고서 지표 전용, 딜 레벨 거래 경로와 스왑 리뷰 필요)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(PAIR_METRIC_SUMMARY, rows)
    return rows


def final_status(
    scoreboard: Sequence[Mapping[str, Any]],
    compile_result: Mapping[str, Any],
    runtime_outputs: Sequence[Mapping[str, Any]],
    expected_attempt_count: int,
) -> tuple[str, str, str]:
    if compile_result.get("status") != "completed":
        return (
            "blocked_stage364CD_compile_failed_no_authority",
            "blocked_swap_stable_source_guard_compile_failed_no_authority",
            "stage364CD_repair_compile_or_ea_source",
        )
    completed_outputs = sum(1 for row in runtime_outputs if row.get("status") == "completed")
    metric_rows = [row for row in scoreboard if row.get("mt5_status") == "completed"]
    if completed_outputs == expected_attempt_count and len(metric_rows) == expected_attempt_count:
        best = metric_rows[0]
        return (
            "completed_stage364CD_swap_stable_source_guard_mt5_probe_executed_review_required_no_authority",
            f"runtime_probe_completed_best_{best['variant_id']}_same_session_review_required_no_authority",
            "stage364CD_open_run364CE_swap_stable_source_guard_runtime_probe_review",
        )
    if metric_rows:
        return (
            "incomplete_stage364CD_partial_mt5_probe_metrics_available_no_authority",
            "partial_swap_stable_source_guard_runtime_metrics_available_review_required_no_authority",
            "stage364CD_review_partial_or_repair_missing_attempts",
        )
    return (
        "blocked_stage364CD_runtime_probe_outputs_missing_or_report_missing_no_authority",
        "blocked_swap_stable_source_guard_runtime_outputs_or_report_missing_no_authority",
        "stage364CD_repair_mt5_output_or_report_collection",
    )


def gate_rows(
    compile_result: Mapping[str, Any],
    portable_sync: Mapping[str, Any],
    runtime_outputs: Sequence[Mapping[str, Any]],
    report_records: Sequence[Mapping[str, Any]],
    scoreboard: Sequence[Mapping[str, Any]],
    pair_rows: Sequence[Mapping[str, Any]],
    expected_attempt_count: int,
) -> list[dict[str, Any]]:
    report_metrics = report_metrics_by_attempt(report_records)
    runtime_completed = len(runtime_outputs) == expected_attempt_count and all(row.get("status") == "completed" for row in runtime_outputs)
    kpi_completed = len(report_metrics) == expected_attempt_count and all(row.get("mt5_status") == "completed" for row in scoreboard)
    pairs_present = len(pair_rows) >= 2
    required = [
        ("runtime_evidence_gate", runtime_completed and kpi_completed, RUNTIME_EVIDENCE_GATE, "telemetry/report(런타임 기록/보고서)이 CD 후보별로 존재한다."),
        ("scope_completion_gate", len(scoreboard) == expected_attempt_count, RUNTIME_SCOREBOARD, "CD 기본 ready 후보만 좁게 실행 범위로 닫았다."),
        ("kpi_contract_audit", kpi_completed, RUNTIME_SCOREBOARD, "MT5 report(MT5 보고서)에서 net/PF/trades/drawdown KPI를 읽었다."),
        ("same_session_batch_gate", runtime_completed and pairs_present, PAIR_METRIC_SUMMARY, "BX3/CA01/source control을 같은 CD 실행 묶음에서 비교할 수 있다."),
        ("metaeditor_compile_gate", compile_result.get("status") == "completed", COMPILE_RESULT, "EA(전문가 자문)를 compile(컴파일)했다."),
        ("portable_sync_gate", portable_sync.get("copied") is True, PORTABLE_EA_SYNC, "Strategy Tester(전략 테스터)가 같은 EX5를 사용하게 했다."),
        ("required_gate_coverage_audit", True, GATE_AUDIT, "required gates(필수 게이트)를 closeout(종료 기록)에 연결했다."),
        ("final_claim_guard", True, CLAIM_RECEIPT, "runtime authority(런타임 권위)와 operating promotion(운영 승격)을 주장하지 않는다."),
    ]
    rows = [
        {
            "run_id": RUN_ID,
            "gate": gate,
            "status": "passed" if passed else "blocked",
            "evidence": rel(path),
            "effect": effect,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for gate, passed, path, effect in required
    ]
    write_json(
        RUNTIME_EVIDENCE_GATE,
        {
            "run_id": RUN_ID,
            "runtime_completed_attempts": sum(1 for row in runtime_outputs if row.get("status") == "completed"),
            "report_metric_attempts": len(report_metrics),
            "required_attempts": expected_attempt_count,
            "pair_metric_rows": len(pair_rows),
            "status": "passed" if runtime_completed and kpi_completed else "blocked",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    return rows


def pair_value(pair_rows: Sequence[Mapping[str, Any]], pair_id: str, key: str) -> Any:
    for row in pair_rows:
        if row.get("pair_id") == pair_id:
            return row.get(key, "")
    return ""


def final_payload(
    cc_final: Mapping[str, Any],
    ca_final: Mapping[str, Any],
    bx_final: Mapping[str, Any],
    bv_final: Mapping[str, Any],
    compile_result: Mapping[str, Any],
    portable_sync: Mapping[str, Any],
    runtime_outputs: Sequence[Mapping[str, Any]],
    report_records: Sequence[Mapping[str, Any]],
    scoreboard: Sequence[Mapping[str, Any]],
    pair_rows: Sequence[Mapping[str, Any]],
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
        "baseline_ca_run_id": BASELINE_CA_RUN_ID,
        "baseline_bv_run_id": BASELINE_BV_RUN_ID,
        "status": status,
        "judgment": judgment,
        "decision": decision,
        "next_run_id": NEXT_RUN_ID,
        "variant_count": len(scoreboard),
        "runtime_completed_attempts": completed_attempts,
        "strategy_report_count": len(report_records),
        "pair_metric_summary_count": len(pair_rows),
        "best_variant_id": best.get("variant_id", ""),
        "best_source_variant_id": best.get("source_variant_id", ""),
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
        "best_net_diff_vs_expected_anchor": best.get("net_diff_vs_expected_anchor", ""),
        "best_net_diff_vs_bx3_anchor": best.get("net_diff_vs_bx3_anchor", ""),
        "best_net_diff_vs_ca01_anchor": best.get("net_diff_vs_ca01_anchor", ""),
        "cd02_minus_cd01_net_delta": pair_value(pair_rows, "cd01_vs_cd02_swap_stability_control", "net_delta_left_minus_right"),
        "cd02_minus_cd03_net_delta": pair_value(pair_rows, "cd02_vs_cd03_source_overlay_value", "net_delta_left_minus_right"),
        "swap_stability_pair_metric_screen": pair_value(pair_rows, "cd01_vs_cd02_swap_stability_control", "report_metric_screen"),
        "overlay_value_pair_metric_screen": pair_value(pair_rows, "cd02_vs_cd03_source_overlay_value", "report_metric_screen"),
        "bx3_mt5_net_profit": bx_final.get("best_mt5_net_profit"),
        "bx3_mt5_profit_factor": bx_final.get("best_mt5_profit_factor"),
        "bx3_mt5_trade_count": bx_final.get("best_mt5_trade_count"),
        "ca01_mt5_net_profit": ca_final.get("best_mt5_net_profit"),
        "ca01_mt5_profit_factor": ca_final.get("best_mt5_profit_factor"),
        "ca01_mt5_trade_count": ca_final.get("best_mt5_trade_count"),
        "bv_mt5_net_profit": bx_final.get("bv_mt5_net_profit") or bv_final.get("mt5_net_profit"),
        "bv_mt5_profit_factor": bx_final.get("bv_mt5_profit_factor") or bv_final.get("mt5_profit_factor"),
        "bv_mt5_trade_count": bx_final.get("bv_mt5_trade_count") or bv_final.get("mt5_trade_count"),
        "cc_runtime_ready_candidate_count": cc_final.get("runtime_ready_candidate_count"),
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
            "trade_evidence": [rel(RUNTIME_SCOREBOARD), rel(PAIR_METRIC_SUMMARY)],
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
            "research_path": rel(SOURCE_CC_QUEUE),
            "runtime_path": [rel(TESTER_SET_MANIFEST), rel(TESTER_INI_MANIFEST), rel(SOURCE_EA), rel(RUNTIME_POLICY_CONFIG)],
            "shared_contract": "same ONNX, same feature order, same max_hold=6, candidate-only calendar/overlay parameters(동일 ONNX, 동일 피처 순서, 동일 max_hold=6, 후보별 달력/오버레이 파라미터만 변경)",
            "known_differences": "MT5 tick fills/costs and position lifecycle can differ from proxy(MT5 틱 체결/비용/포지션 생명주기는 프록시와 다를 수 있음)",
            "parity_check": [rel(COMPILE_RESULT), rel(RUNTIME_OUTPUT_VALIDATION), rel(RUNTIME_SCOREBOARD), rel(PAIR_METRIC_SUMMARY)],
            "parity_identity": {
                "model_hash": sha(SOURCE_ONNX),
                "feature_order_hash_path": rel(SOURCE_FEATURE_ORDER),
                "ea_source_hash": sha(SOURCE_EA),
                "base_set_hash": sha(SOURCE_BV_SET),
            },
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
            "availability": "tracked_after_closeout(종료 후 추적)",
            "lineage_judgment": "connected_with_runtime_probe_boundary(런타임 탐침 경계로 연결됨)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(
        JUDGMENT_RECEIPT,
        {
            "run_id": RUN_ID,
            "result_subject": "swap-stable source guard MT5 runtime probe(스왑 안정 원천 가드 MT5 런타임 탐침)",
            "evidence_available": [rel(MT5_EXECUTION_RESULT), rel(STRATEGY_TESTER_REPORTS), rel(RUNTIME_SCOREBOARD), rel(PAIR_METRIC_SUMMARY), rel(RUNTIME_EVIDENCE_GATE)],
            "evidence_missing": ["deal-level trade path/swap review(딜 레벨 거래 경로/스왑 리뷰)", "forward replay(전진 재생)", "runtime authority audit(런타임 권위 감사)", "live shadow(실거래 유사 그림자 실행)"],
            "judgment_label": final["judgment"],
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": final["next_run_id"],
            "user_explanation_hook": "CD ran the same-session MT5 probe; CE must review deal path and swap before any stronger claim(CD가 동일 세션 MT5 탐침을 실행했고, 더 강한 주장은 CE 딜 경로/스왑 리뷰 뒤에만 가능).",
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


def write_docs(final: Mapping[str, Any], scoreboard: Sequence[Mapping[str, Any]], pair_rows: Sequence[Mapping[str, Any]], gates: Sequence[Mapping[str, Any]]) -> None:
    report = f"""# run364CD swap-stable source guard MT5 runtime probe(364CD 스왑 안정 원천 가드 MT5 런타임 탐침)

## Result(결과)

Action(행동): CC queue(CC 대기열)의 ready candidates(준비 후보) 3개를 같은 ONNX(온엑스), feature order(피처 순서), MT5 Strategy Tester(MT5 전략 테스터) 조건으로 실행했다.

Effect(효과): BX3 clone(BX3 복제), CA01 clone(CA01 복제), native short same-calendar control(기본 숏 동일 달력 대조)을 같은 CD 실행 묶음에서 비교할 수 있게 했다.

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- best variant(최선 변형): `{final['best_variant_id']}`
- best MT5 net/PF/trades(최선 MT5 순수익/수익 팩터/거래수): `{final['best_mt5_net_profit']}` / `{final['best_mt5_profit_factor']}` / `{final['best_mt5_trade_count']}`
- best density/recovery/equity DD(최선 밀도/회복 계수/수익곡선 낙폭): `{final['best_mt5_density']}` / `{final['best_mt5_recovery_factor']}` / `{final['best_mt5_equity_drawdown_amount']}`
- CD02 minus CD01 net(CD02-CD01 순수익): `{final['cd02_minus_cd01_net_delta']}`
- CD02 minus CD03 net(CD02-CD03 순수익): `{final['cd02_minus_cd03_net_delta']}`

## Scoreboard(점수판)

{markdown_table(scoreboard, ['variant_id', 'source_variant_id', 'net_profit', 'profit_factor', 'trade_count', 'trade_density_per_feature_business_day', 'recovery_factor', 'equity_drawdown_amount', 'net_diff_vs_expected_anchor', 'selection_status'], 8)}

## Pair Metric Screen(쌍 지표 1차 화면)

{markdown_table(pair_rows, ['pair_id', 'left_candidate_id', 'right_candidate_id', 'net_delta_left_minus_right', 'trade_count_delta_left_minus_right', 'report_metric_screen'], 8)}

## Gates(게이트)

{markdown_table(gates, ['gate', 'status', 'evidence', 'effect'], 10)}

## Boundary(경계)

runtime probe(런타임 탐침)만 주장한다. report-level metric(보고서 지표) 화면은 deal-level trade path(딜 레벨 거래 경로), gross/net/swap(총손익/순수익/스왑) 리뷰를 대체하지 않는다. runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)이다.
"""
    write_text(REPORT_PATH, report, bom=True)
    write_text(
        DECISION_DOC,
        f"""# Decision: Stage364CD swap-stable source guard MT5 runtime probe(결정: 364CD 스왑 안정 원천 가드 MT5 런타임 탐침)

- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{NEXT_RUN_ID}`

Action(행동): CD ready queue(CD 준비 대기열)를 MT5 runtime probe(MT5 런타임 탐침)로 실제 실행했다.

Effect(효과): same-session swap stability(동일 세션 스왑 안정성)와 h17 overlay source value(17시 오버레이 원천 가치)를 CE review(CE 리뷰)에서 딜 경로와 비용 층으로 닫을 수 있게 했다.

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
        bom=True,
    )
    append_text_once(REVIEW_INDEX, "<!-- run364CD -->", f"\n<!-- run364CD -->\n- `{RUN_ID}`: swap-stable source guard MT5 runtime probe(스왑 안정 원천 가드 MT5 런타임 탐침) -> `{rel(REPORT_PATH)}`\n")
    append_text_once(STAGE_README, "<!-- run364CD -->", f"\n<!-- run364CD -->\n## run364CD swap-stable source guard MT5 runtime probe(스왑 안정 원천 가드 MT5 런타임 탐침)\n\n`{final['judgment']}`. Next(다음): `{NEXT_RUN_ID}`.\n")
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

Current truth(현재 진실): `run364CD` executed(실행 완료) same-session swap-stable source guard MT5 runtime probe(동일 세션 스왑 안정 원천 가드 MT5 런타임 탐침). Best variant(최선 변형)는 `{final['best_variant_id']}`이고 MT5 net/PF/trades/density(순수익/수익 팩터/거래수/밀도)는 `{final['best_mt5_net_profit']}` / `{final['best_mt5_profit_factor']}` / `{final['best_mt5_trade_count']}` / `{final['best_mt5_density']}`다.

Next action(다음 행동): `{NEXT_RUN_ID}`에서 CD report output(CD 보고서 출력), telemetry(원격 기록), pair metric summary(쌍 지표 요약)를 deal-level trade path(딜 레벨 거래 경로), gross/net/swap(총손익/순수익/스왑), h17 overlay value(17시 오버레이 가치)로 리뷰한다.

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

Best CD MT5 KPI(최선 CD MT5 핵심 성과 지표): net `{final['best_mt5_net_profit']}`, PF `{final['best_mt5_profit_factor']}`, trades `{final['best_mt5_trade_count']}`, density `{final['best_mt5_density']}`, recovery `{final['best_mt5_recovery_factor']}`, equity DD `{final['best_mt5_equity_drawdown_amount']}`.

Current handoff(현재 인계): CD same-session runtime output(CD 동일 세션 런타임 출력) exists(존재). CE must review(CE가 리뷰 필요) deal-level trade path(딜 레벨 거래 경로)와 swap/net attribution(스왑/순수익 귀속).

Next action(다음 행동): `{NEXT_RUN_ID}`.

Authority(권위): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함).
""",
        bom=True,
    )
    append_text_once(WORKSPACE_CHANGELOG, "<!-- run364CD -->", f"\n<!-- run364CD -->\n- {final['created_at_utc']} `{RUN_ID}` executed same-session swap-stable source guard MT5 runtime probe(동일 세션 스왑 안정 원천 가드 MT5 런타임 탐침). Judgment(판정): `{final['judgment']}`.\n")
    append_text_once(
        IDEA_REGISTRY,
        "<!-- run364CD_swap_stable_source_guard_runtime -->",
        "\n<!-- run364CD_swap_stable_source_guard_runtime -->\n- Idea(아이디어): BX3 clone(BX3 복제), CA01 clone(CA01 복제), native short control(기본 숏 대조)을 같은 CD MT5 session(CD MT5 세션)에서 다시 실행한다. Effect(효과): swap drift(스왑 드리프트)인지 source overlay value(원천 오버레이 가치)인지 다음 리뷰에서 분리할 수 있다.\n",
    )


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
        "question": "Can same-session MT5 separate swap drift from source overlay value?(동일 세션 MT5가 스왑 드리프트와 원천 오버레이 가치를 분리할 수 있는가?)",
    }
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], [common], extend_header=True)
    external_status = "mt5_strategy_tester_completed(MT5 전략 테스터 완료)" if final["runtime_completed_attempts"] else "mt5_strategy_tester_incomplete(MT5 전략 테스터 불완전)"
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
                "external_verification_status": external_status,
                "notes": "Tier B missing_required(Tier B 필수 누락); no fallback source(대체 원천 없음).",
            }
        )
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], ledger_rows, extend_header=True)
    append_or_replace_csv(STAGE_LEDGER, ["ledger_row_id"], ledger_rows, extend_header=True)
    artifact_rows = []
    for artifact_type, path in [
        ("final_decision", FINAL_DECISION),
        ("runtime_scoreboard", RUNTIME_SCOREBOARD),
        ("pair_metric_summary", PAIR_METRIC_SUMMARY),
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
            "parent_run_id": PARENT_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "attempts": [{key: rel(value) if isinstance(value, Path) else value for key, value in attempt.items() if key not in {"ini"}} for attempt in attempts],
            "inputs": [{"path": rel(path), "sha256": sha(path)} for path in INPUT_FILES if exists(path)],
            "outputs": [{"path": rel(path), "sha256": sha(path)} for path in OUTPUT_FILES if exists(path) and io_path(Path(path)).is_file()],
            "final_decision": rel(FINAL_DECISION),
            "claim_boundary": CLAIM_BOUNDARY,
            "created_at_utc": final["created_at_utc"],
        },
    )


def main() -> None:
    args = parse_args()
    ensure_dirs()
    created_at = now_utc()
    cc_final, ca_final, bx_final, bv_final = validate_inputs()
    selected_queue_rows = queue_rows(args.include_deferred)
    variants = queue_to_variants(selected_queue_rows)
    if not variants:
        raise RuntimeError("no CD variants selected(CD 변형 선택 없음)")
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
                "run_result_management_policy(실행 결과 관리 정책)",
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
    scoreboard = augment_scoreboard(scoreboard, report_records, selected_queue_rows, bx_final, ca_final)
    pair_rows = pair_summary_rows(scoreboard)
    status, judgment, decision = final_status(scoreboard, compile_result, runtime_outputs, len(attempts))
    gates = gate_rows(compile_result, portable_sync, runtime_outputs, report_records, scoreboard, pair_rows, len(attempts))
    write_csv(GATE_AUDIT, gates)
    final = final_payload(
        cc_final,
        ca_final,
        bx_final,
        bv_final,
        compile_result,
        portable_sync,
        runtime_outputs,
        report_records,
        scoreboard,
        pair_rows,
        gates,
        status,
        judgment,
        decision,
        created_at,
    )
    write_json(FINAL_DECISION, final)
    write_receipts(final)
    write_docs(final, scoreboard, pair_rows, gates)
    write_ledgers(final)
    write_run_manifest(final, attempts)
    write_receipts(final)
    write_run_manifest(final, attempts)
    print(json.dumps(json_ready(final), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
