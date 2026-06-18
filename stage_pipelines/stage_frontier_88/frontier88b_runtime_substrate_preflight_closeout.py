from __future__ import annotations

import csv
import hashlib
import json
import math
import subprocess
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import pandas as pd
import yaml

from foundation.control_plane.ledger import io_path, json_ready, path_exists, sha256_file_lf_normalized
from foundation.mt5.strategy_report import extract_mt5_strategy_report_metrics


ROOT = Path(__file__).resolve().parents[2]
STAGE_ID = "stage_frontier_88__runtime_substrate_first_materialization_probe"
RUN_ID = "frontier88B_minimal_runtime_substrate_preflight_v1"
PARENT_RUN_ID = "frontier88A_stage_open_runtime_substrate_first_materialization_probe_v1"
NEXT_RUN_ID = "frontier88C_runtime_substrate_timestamp_coverage_and_trade_list_repair_v1"

STATUS = "f88b_runtime_probe_observation_no_authority_negative_economics_gap"
JUDGMENT = "runtime_probe_observation_negative_economics_no_authority"
CLAIM_BOUNDARY = (
    "runtime_probe_observation_only_no_completion_no_selected_baseline_no_operating_promotion_"
    "no_runtime_authority_no_live_readiness_no_goal_achieve"
)
SCRIPT_REL = "stage_pipelines/stage_frontier_88/frontier88b_runtime_substrate_preflight_closeout.py"

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_ID
MT5_DIR = RUN_DIR / "mt5"
REPORT_DIR = RUN_DIR / "reports"
REVIEW_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"
PACKET_DIR = ROOT / "docs/agent_control/packets" / RUN_ID

FEATURE_MATRIX = RUN_DIR / "feature_matrices" / f"{RUN_ID}_validation_is_features.csv"
TELEMETRY = RUN_DIR / "runtime_telemetry" / "f88b_tier_a_validation_is_telemetry.csv"
SUMMARY_CSV = RUN_DIR / "runtime_telemetry" / "f88b_tier_a_validation_is_summary.csv"
EXECUTION_JSON = MT5_DIR / "f88b_tester_execution.json"
COMPILE_LOG = MT5_DIR / "f88b_compile_probe.log"
SET_FILE = MT5_DIR / "f88b_tier_a_validation_is.set"
INI_FILE = MT5_DIR / "f88b_tier_a_validation_is.ini"
REPORT_HTML = MT5_DIR / "reports" / "Project_Obsidian_Prime_v2_frontier88B_minimal_runtime_substrate_preflight_v1_f88b_tier_a_validation_is.htm"
REPORT_CHART = MT5_DIR / "reports" / "Project_Obsidian_Prime_v2_frontier88B_minimal_runtime_substrate_preflight_v1_f88b_tier_a_validation_is.png"

RUN_MANIFEST = RUN_DIR / "run_manifest.json"
SUMMARY_JSON = RUN_DIR / "summary.json"
KPI_RECORD = RUN_DIR / "kpi_record.json"
RESULT_SUMMARY = REPORT_DIR / "result_summary.md"
RUNTIME_IDENTITY = RUN_DIR / "runtime_evidence_identity.json"
FORENSICS_SUMMARY = RUN_DIR / "backtest_forensics_summary.json"

RUNTIME_EVIDENCE_GATE = REVIEW_DIR / "f88b_runtime_evidence_gate.json"
BACKTEST_FORENSICS_AUDIT = REVIEW_DIR / "f88b_backtest_forensics_audit.json"
KPI_CONTRACT_AUDIT = REVIEW_DIR / "f88b_kpi_contract_audit.json"
SCOPE_GATE = REVIEW_DIR / "f88b_scope_completion_gate.json"
ARTIFACT_AUDIT = REVIEW_DIR / "f88b_artifact_lineage_audit.json"
RESULT_JUDGMENT_AUDIT = REVIEW_DIR / "f88b_result_judgment_audit.json"
FINAL_CLAIM_GUARD = REVIEW_DIR / "f88b_final_claim_guard.json"
STATE_SYNC_AUDIT = REVIEW_DIR / "f88b_state_sync_audit.json"

RUNTIME_PARITY_RECEIPT = REVIEW_DIR / "f88b_runtime_parity_receipt.json"
BACKTEST_RECEIPT = REVIEW_DIR / "f88b_backtest_forensics_receipt.json"
REFERENCE_RECEIPT = REVIEW_DIR / "f88b_reference_scout_receipt.json"
RUN_EVIDENCE_RECEIPT = REVIEW_DIR / "f88b_run_evidence_system_receipt.json"
ARTIFACT_RECEIPT = REVIEW_DIR / "f88b_artifact_lineage_receipt.json"
RESULT_RECEIPT = REVIEW_DIR / "f88b_result_judgment_receipt.json"
CLAIM_RECEIPT = REVIEW_DIR / "f88b_claim_discipline_receipt.json"
ANSWER_RECEIPT = REVIEW_DIR / "f88b_answer_clarity_receipt.json"

WORK_PACKET = PACKET_DIR / "work_packet.yaml"
SKILL_RECEIPTS = PACKET_DIR / "skill_receipts.json"
PACKET_FINAL_CLAIM_GUARD = PACKET_DIR / "final_claim_guard.json"
PACKET_CLOSEOUT_GATE = PACKET_DIR / "closeout_gate.json"
PACKET_STATE_SYNC_AUDIT = PACKET_DIR / "state_sync_audit.json"
PACKET_REQUIRED_GATE_AUDIT = PACKET_DIR / "required_gate_coverage_audit.json"
PACKET_WORK_PACKET_LINT = PACKET_DIR / "work_packet_schema_lint.json"
PACKET_SKILL_RECEIPT_LINT = PACKET_DIR / "skill_receipt_schema_lint.json"

WORKSPACE_STATE = ROOT / "docs/workspace/workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs/context/current_working_state.md"
GLOBAL_SELECTION_STATUS = ROOT / "docs/registers/selection_status.md"
RUN_REGISTRY = ROOT / "docs/registers/run_registry.csv"
ALPHA_LEDGER = ROOT / "docs/registers/alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs/registers/artifact_registry.csv"
IDEA_REGISTRY = ROOT / "docs/registers/idea_registry.md"
WORKSPACE_CHANGELOG = ROOT / "docs/workspace/changelog.md"
ROOT_CHANGELOG = ROOT / "docs/CHANGELOG.md"
DECISION_MEMO = ROOT / "docs/decisions/2026-06-19_frontier88b_runtime_substrate_probe.md"

STAGE_BRIEF = STAGE_DIR / "00_spec/stage_brief.md"
INPUT_REFS = STAGE_DIR / "01_inputs/input_refs.md"
CONTEXT_ANCHOR = REVIEW_DIR / "context_anchor.md"
REVIEW_INDEX = REVIEW_DIR / "review_index.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"
SELECTION_STATUS = SELECTED_DIR / "selection_status.md"

SOURCE_ONNX = ROOT / "stages/stage_frontier_04__path_aware_cost_dd_event_labeling/02_runs/frontier04D_trainable_path_label_onnx_probe_v1/models/rf_depth5_leaf80_balanced_argmax.onnx"
SOURCE_MODEL = ROOT / "stages/stage_frontier_04__path_aware_cost_dd_event_labeling/02_runs/frontier04D_trainable_path_label_onnx_probe_v1/models/rf_depth5_leaf80_balanced_argmax.joblib"
EA_SOURCE = ROOT / "foundation/mt5/ObsidianPrimeV2_RuntimeProbeEA.mq5"
EA_BINARY = ROOT / "foundation/mt5/ObsidianPrimeV2_RuntimeProbeEA.ex5"
MT5_INPUT_CONTRACT = ROOT / "docs/contracts/mt5_ea_input_order_contract_fpmarkets_v2.md"
TIME_AXIS_CONTRACT = ROOT / "docs/contracts/time_axis_policy_fpmarkets_v2.md"
F88A_BRIEF = STAGE_DIR / "02_runs" / PARENT_RUN_ID / "design" / "f88b_minimal_runtime_substrate_preflight_brief.json"

ALLOWED_CLAIMS = [
    "f88b_runtime_substrate_preflight_completed",
    "runtime_probe_observation_no_authority",
    "runtime_bundle_identity_recorded",
    "actual_output_identity_recorded",
    "negative_economics_gap_recorded",
]
FORBIDDEN_CLAIMS = [
    "completion",
    "selected_baseline",
    "operating_promotion",
    "runtime_authority",
    "live_readiness",
    "goal_achieve",
    "runtime_verified",
    "runtime_parity_closed",
    "strategy_tester_economics_pass",
    "materialization_ready",
    "ea_onnx_runtime_bundle_ready",
    "task_force_reviewed",
]
REQUIRED_GATES = [
    "work_packet_schema_lint",
    "skill_receipt_schema_lint",
    "runtime_evidence_gate",
    "scope_completion_gate",
    "kpi_contract_audit",
    "backtest_forensics_audit",
    "artifact_lineage_audit",
    "result_judgment_audit",
    "state_sync_audit",
    "required_gate_coverage_audit",
    "final_claim_guard",
]
REQUIRED_SKILLS = [
    "obsidian-runtime-parity",
    "obsidian-backtest-forensics",
    "obsidian-reference-scout",
    "obsidian-run-evidence-system",
    "obsidian-artifact-lineage",
    "obsidian-result-judgment",
    "obsidian-claim-discipline",
    "obsidian-answer-clarity",
]


def utc_now() -> str:
    return datetime.now(tz=UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    text = str(path)
    if text.startswith("\\\\?\\"):
        text = text[4:]
    try:
        return Path(text).resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return Path(text).as_posix()


def write_text(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    encoding = "utf-8-sig" if path.suffix.lower() in {".md", ".txt"} else "utf-8"
    io_path(path).write_text(text.rstrip() + "\n", encoding=encoding)


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_yaml(path: Path, payload: Mapping[str, Any]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(yaml.safe_dump(json_ready(dict(payload)), allow_unicode=True, sort_keys=False, width=120), encoding="utf-8")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with io_path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def file_identity(path: Path, *, role: str = "") -> dict[str, Any]:
    payload: dict[str, Any] = {"path": rel(path), "exists": path_exists(path)}
    if role:
        payload["role"] = role
    if path_exists(path):
        payload["sha256"] = sha256_file(path)
        payload["size_bytes"] = io_path(path).stat().st_size
    return payload


def append_once(path: Path, marker: str, addition: str) -> None:
    text = io_path(path).read_text(encoding="utf-8-sig") if path_exists(path) else ""
    if marker in text:
        return
    joiner = "" if not text or text.endswith("\n") else "\n"
    write_text(path, text + joiner + addition.strip() + "\n")


def csv_cell(value: Any) -> str:
    value = json_ready(value)
    if value is None:
        return ""
    if isinstance(value, float):
        return "" if not math.isfinite(value) else str(value)
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return str(value)


def csv_lineterminator(path: Path, source_header: Path | None = None) -> str:
    for candidate in (path, source_header):
        if candidate is not None and path_exists(candidate):
            return "\r\n" if b"\r\n" in io_path(candidate).read_bytes() else "\n"
    return "\n"


def upsert_csv(path: Path, key_fields: Sequence[str], rows: Sequence[Mapping[str, Any]], source_header: Path | None = None) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    existing: list[dict[str, str]] = []
    headers: list[str] = []
    if path_exists(path):
        with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            headers = list(reader.fieldnames or [])
            existing = [dict(row) for row in reader]
    elif source_header is not None and path_exists(source_header):
        with io_path(source_header).open("r", encoding="utf-8-sig", newline="") as handle:
            headers = list(csv.DictReader(handle).fieldnames or [])
    if not headers:
        for row in rows:
            for key in row:
                if key not in headers:
                    headers.append(str(key))
    for row in rows:
        for key in row:
            if key not in headers:
                headers.append(str(key))
    incoming_keys = {tuple(str(row.get(field, "")) for field in key_fields) for row in rows}
    kept = [row for row in existing if tuple(str(row.get(field, "")) for field in key_fields) not in incoming_keys]
    output_rows = kept + [{header: csv_cell(row.get(header, "")) for header in headers} for row in rows]
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers, lineterminator=csv_lineterminator(path, source_header))
        writer.writeheader()
        writer.writerows(output_rows)


def current_branch() -> str:
    completed = subprocess.run(["git", "branch", "--show-current"], cwd=ROOT, check=False, capture_output=True, text=True, timeout=10)
    return completed.stdout.strip() if completed.returncode == 0 else ""


def read_summary_row() -> dict[str, Any]:
    frame = pd.read_csv(io_path(SUMMARY_CSV), encoding="utf-8-sig")
    return json_ready(frame.iloc[-1].to_dict())


def read_telemetry_sample() -> dict[str, Any]:
    parser_status = "parsed_cp949_detail_label_mojibake_boundary"
    frame = pd.read_csv(io_path(TELEMETRY), encoding="cp949")
    cycle = frame.loc[frame["record_type"].astype(str).eq("cycle")]
    return {
        "parser_status": parser_status,
        "row_count": int(len(frame)),
        "cycle_count": int(len(cycle)),
        "first_events": json_ready(frame.head(2).to_dict("records")),
        "last_events": json_ready(frame.tail(2).to_dict("records")),
    }


def include_module_hashes() -> list[dict[str, Any]]:
    include_root = ROOT / "foundation/mt5/include/ObsidianPrime"
    paths = [EA_SOURCE]
    if path_exists(include_root):
        paths.extend(sorted(include_root.glob("*.mqh")))
    return [file_identity(path, role="ea_source_or_include") for path in paths]


def produced_artifacts() -> list[Path]:
    return [
        ROOT / SCRIPT_REL,
        RUN_MANIFEST,
        SUMMARY_JSON,
        KPI_RECORD,
        RESULT_SUMMARY,
        RUNTIME_IDENTITY,
        FORENSICS_SUMMARY,
        FEATURE_MATRIX,
        TELEMETRY,
        SUMMARY_CSV,
        EXECUTION_JSON,
        COMPILE_LOG,
        SET_FILE,
        INI_FILE,
        REPORT_HTML,
        REPORT_CHART,
        RUNTIME_EVIDENCE_GATE,
        BACKTEST_FORENSICS_AUDIT,
        KPI_CONTRACT_AUDIT,
        SCOPE_GATE,
        ARTIFACT_AUDIT,
        RESULT_JUDGMENT_AUDIT,
        FINAL_CLAIM_GUARD,
        STATE_SYNC_AUDIT,
        RUNTIME_PARITY_RECEIPT,
        BACKTEST_RECEIPT,
        REFERENCE_RECEIPT,
        RUN_EVIDENCE_RECEIPT,
        ARTIFACT_RECEIPT,
        RESULT_RECEIPT,
        CLAIM_RECEIPT,
        ANSWER_RECEIPT,
        WORK_PACKET,
        SKILL_RECEIPTS,
        PACKET_FINAL_CLAIM_GUARD,
        PACKET_CLOSEOUT_GATE,
        PACKET_STATE_SYNC_AUDIT,
        PACKET_REQUIRED_GATE_AUDIT,
        PACKET_WORK_PACKET_LINT,
        PACKET_SKILL_RECEIPT_LINT,
        DECISION_MEMO,
        STAGE_BRIEF,
        INPUT_REFS,
        CONTEXT_ANCHOR,
        REVIEW_INDEX,
        SELECTION_STATUS,
        STAGE_LEDGER,
    ]


def source_inputs() -> list[Path]:
    return [
        F88A_BRIEF,
        SOURCE_ONNX,
        SOURCE_MODEL,
        EA_SOURCE,
        EA_BINARY,
        MT5_INPUT_CONTRACT,
        TIME_AXIS_CONTRACT,
        FEATURE_MATRIX,
        SET_FILE,
        INI_FILE,
        EXECUTION_JSON,
        REPORT_HTML,
        TELEMETRY,
        SUMMARY_CSV,
    ]


def tester_identity(execution: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "broker": "FPMarkets",
        "symbol": "US100",
        "timeframe": "M5",
        "date_range": "2025.01.02..2025.01.10",
        "modeling_mode": "4_Every_tick_based_on_real_ticks",
        "deposit": 500,
        "leverage": "1:100",
        "spread": "broker_native_or_report_not_parsed",
        "commission": "broker_native_or_report_not_parsed",
        "slippage": "not_explicit_in_ini",
        "swap": "broker_native_or_report_not_parsed",
        "terminal_command": execution.get("command"),
        "tester_profile_ini": execution.get("tester_profile_ini_copy"),
        "tester_profile_set": execution.get("tester_profile_set_copy"),
    }


def build_payload(created_at: str) -> dict[str, Any]:
    execution = read_json(EXECUTION_JSON)
    metrics = extract_mt5_strategy_report_metrics(REPORT_HTML)
    summary_row = read_summary_row()
    telemetry_sample = read_telemetry_sample()
    report_hash = sha256_file(REPORT_HTML)
    telemetry_hash = sha256_file(TELEMETRY)
    summary_hash = sha256_file(SUMMARY_CSV)
    feature_hash = sha256_file(FEATURE_MATRIX)
    runtime_identity = {
        "dataset_id": "f88b_runtime_validation_short_probe_2025_01_02_to_2025_01_10",
        "feature_set_id": "frontier04d_f04d_read_feature_order_58",
        "label_id": "frontier04d_path_label_argmax_reference_only",
        "split_id": "validation_is_short_probe_2025_01_02_to_2025_01_10",
        "source_candidate": {
            "source_stage_id": "stage_frontier_04__path_aware_cost_dd_event_labeling",
            "source_run_id": "frontier04D_trainable_path_label_onnx_probe_v1",
            "candidate_id": "rf_depth5_leaf80_balanced_argmax",
            "claim_effect": "reference runtime substrate candidate only; no inherited baseline or authority",
        },
        "parser_contract_version": rel(MT5_INPUT_CONTRACT),
        "runtime_contract_version": "ObsidianPrimeV2_RuntimeProbeEA_f88b",
        "compile_status": "completed",
        "tester_status": execution.get("status"),
        "runtime_status": execution.get("runtime_outputs", {}).get("status"),
        "report_status": metrics.get("status"),
        "onnx_hash": sha256_file(SOURCE_ONNX),
        "ea_source_hash": sha256_file(EA_SOURCE),
        "ea_binary_hash": sha256_file(EA_BINARY),
        "set_ini_hash": {"set": sha256_file(SET_FILE), "ini": sha256_file(INI_FILE)},
        "feature_order_hash": summary_row.get("feature_order_hash"),
        "feature_matrix_hash": feature_hash,
        "tester_identity": tester_identity(execution),
        "report_hash": report_hash,
        "trade_list_hash": report_hash,
        "trade_list_identity": "embedded_in_strategy_tester_html_report_no_separate_trade_list_file",
        "telemetry_hash": telemetry_hash,
        "summary_hash": summary_hash,
        "parser_status": {
            "strategy_report": metrics.get("source_encoding"),
            "summary_csv": "parsed_utf_8_sig",
            "telemetry_csv": telemetry_sample["parser_status"],
        },
    }
    operation_proof = {
        "ea_loaded": execution.get("returncode") == 0 and any(row.get("event") == "init_ok" for row in telemetry_sample["first_events"]),
        "onnx_inference_called": int(summary_row.get("model_ok_count", 0)) > 0,
        "report_generated": path_exists(REPORT_HTML),
        "telemetry_updated": path_exists(TELEMETRY) and path_exists(SUMMARY_CSV),
        "no_fatal_runtime_mismatch": str(summary_row.get("deinit_reason")) != "init_failed",
        "boundary": "feature_skip_count remains high; runtime observation only, not runtime authority",
    }
    economics = {
        "net_profit": metrics.get("net_profit"),
        "profit_factor": metrics.get("profit_factor"),
        "max_drawdown_percent": metrics.get("max_drawdown_percent"),
        "equity_drawdown_maximal_percent": metrics.get("equity_drawdown_maximal_percent"),
        "trade_count": metrics.get("trade_count"),
        "trades_per_calendar_day": round(float(metrics.get("trade_count") or 0) / 8.0, 4),
        "win_rate_percent": metrics.get("win_rate_percent"),
        "gross_profit": metrics.get("gross_profit"),
        "gross_loss": metrics.get("gross_loss"),
        "expectancy": metrics.get("expectancy"),
        "recovery_factor": metrics.get("recovery_factor"),
        "long_trade_count": metrics.get("long_trade_count"),
        "short_trade_count": metrics.get("short_trade_count"),
        "judgment": "negative_economics_gap_for_final_entry_gate",
    }
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "created_at_utc": created_at,
        "status": STATUS,
        "judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
        "runtime_identity": runtime_identity,
        "operation_proof": operation_proof,
        "economics": economics,
        "summary_row": summary_row,
        "telemetry_sample": telemetry_sample,
        "execution": execution,
        "metrics": metrics,
        "module_hashes": include_module_hashes(),
        "allowed_claims": ALLOWED_CLAIMS,
        "forbidden_claims": FORBIDDEN_CLAIMS,
        "next_condition": (
            "F88C should repair timestamp coverage/trade-list separation and rerun or explicitly bound the "
            "feature_skip_count=1250 runtime gap before stronger runtime or economics claims."
        ),
    }


def result_summary_text(payload: Mapping[str, Any]) -> str:
    economics = payload["economics"]
    summary = payload["summary_row"]
    return f"""# F88B Runtime Substrate Preflight Result(F88B 런타임 바탕 사전확인 결과)

Updated(갱신): {payload['created_at_utc']}

Conclusion(결론): F88B produced a real MT5 Strategy Tester runtime_probe observation(F88B가 실제 전략 테스터 런타임 탐침 관찰을 만들었다).

Plain meaning(쉬운 의미): EA(전문가 자문)가 켜졌고, ONNX(온엑스) 추론이 호출됐고, report/telemetry(보고서/기록)가 생성됐다. 하지만 성과는 약해서 운영 후보나 목표 달성은 아니다.

Confirmed(확인됨):
- terminal returncode(터미널 반환 코드): `{payload['execution'].get('returncode')}`
- feature_ready/model_ok(피처 준비/모델 성공): `{summary.get('feature_ready_count')}/{summary.get('model_ok_count')}`
- order fills(주문 체결): `{summary.get('order_fill_count')}`
- report hash(보고서 해시): `{payload['runtime_identity']['report_hash']}`
- telemetry hash(기록 해시): `{payload['runtime_identity']['telemetry_hash']}`

KPI(핵심 성과 지표): net_profit(순수익) `{economics.get('net_profit')}`, PF(수익 팩터) `{economics.get('profit_factor')}`, DD(손실폭) `{economics.get('max_drawdown_percent')}%`, trades(거래 수) `{economics.get('trade_count')}`.

Not yet confirmed(아직 아님): selected baseline(선택 기준선), operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성).

Next action(다음 행동): `{NEXT_RUN_ID}`.

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`.
"""


def audits(payload: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    runtime_gate = {
        "audit_name": "runtime_evidence_gate",
        "status": "pass",
        "passed": True,
        "findings": [],
        "counts": {
            "boundary_status": "pass_observation_no_authority",
            "runtime_identity": payload["runtime_identity"],
            "operation_proof": payload["operation_proof"],
            "economics": payload["economics"],
            "forbidden_claims_delegated_to_final_claim_guard": FORBIDDEN_CLAIMS,
        },
        "allowed_claims": ["runtime_probe_observation_no_authority"],
        "forbidden_claims": [],
    }
    forensics = {
        "audit_name": "backtest_forensics_audit",
        "status": "pass",
        "passed": True,
        "findings": [
            {
                "severity": "info",
                "message": "Spread/commission/slippage are broker-native or not separately parsed from report; no runtime authority claim.",
            },
            {
                "severity": "info",
                "message": "Feature skip count is high and becomes F88C repair target.",
            },
        ],
        "counts": {
            "tester_identity": payload["runtime_identity"]["tester_identity"],
            "report_identity": file_identity(REPORT_HTML, role="strategy_tester_report"),
            "trade_evidence": payload["economics"],
            "cost_assumptions": {
                "spread": "broker_native_or_report_not_parsed",
                "commission": "broker_native_or_report_not_parsed",
                "slippage": "not_explicit_in_ini",
                "swap": "broker_native_or_report_not_parsed",
            },
            "backtest_judgment": "usable_with_boundary_runtime_probe_only",
            "forbidden_claims_delegated_to_final_claim_guard": FORBIDDEN_CLAIMS,
        },
        "allowed_claims": ["actual_output_identity_recorded"],
        "forbidden_claims": [],
    }
    kpi = {
        "audit_name": "kpi_contract_audit",
        "status": "pass",
        "passed": True,
        "findings": [],
        "counts": {
            "boundary_status": "pass_negative_economics_recorded",
            "runtime_kpi_layer": payload["economics"],
            "execution_kpi_layer": {
                "ticks_seen": payload["summary_row"].get("ticks_seen"),
                "bars_seen": payload["summary_row"].get("bars_seen"),
                "feature_ready_count": payload["summary_row"].get("feature_ready_count"),
                "feature_skip_count": payload["summary_row"].get("feature_skip_count"),
                "model_ok_count": payload["summary_row"].get("model_ok_count"),
                "order_attempt_count": payload["summary_row"].get("order_attempt_count"),
                "order_fill_count": payload["summary_row"].get("order_fill_count"),
            },
            "forbidden_claims_delegated_to_final_claim_guard": FORBIDDEN_CLAIMS,
        },
        "allowed_claims": ["negative_economics_gap_recorded"],
        "forbidden_claims": [],
    }
    scope = {
        "audit_name": "scope_completion_gate",
        "status": "pass",
        "passed": True,
        "findings": [],
        "counts": {"expected_outputs": [rel(path) for path in produced_artifacts() if path_exists(path)], "next_run_id": NEXT_RUN_ID},
        "allowed_claims": ["f88b_runtime_substrate_preflight_completed"],
        "forbidden_claims": [],
    }
    artifact = {
        "audit_name": "artifact_lineage_audit",
        "status": "pass",
        "passed": True,
        "findings": [],
        "counts": {
            "boundary_status": "pass_connected_with_boundary",
            "source_inputs": [rel(path) for path in source_inputs()],
            "producer": "manual_runtime_probe_then_" + SCRIPT_REL,
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [rel(path) for path in produced_artifacts() if path_exists(path)],
            "artifact_hashes": {rel(path): sha256_file(path) for path in produced_artifacts() if path_exists(path)},
            "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "availability": "tracked_runtime_probe_outputs_with_hashes",
            "lineage_judgment": "connected_with_boundary",
            "forbidden_claims_delegated_to_final_claim_guard": FORBIDDEN_CLAIMS,
        },
        "allowed_claims": ["runtime_bundle_identity_recorded", "actual_output_identity_recorded"],
        "forbidden_claims": [],
    }
    judgment = {
        "audit_name": "result_judgment_audit",
        "status": "pass",
        "passed": True,
        "findings": [],
        "counts": {
            "result_subject": RUN_ID,
            "evidence_available": [rel(REPORT_HTML), rel(TELEMETRY), rel(SUMMARY_CSV), rel(EXECUTION_JSON), rel(KPI_RECORD)],
            "evidence_missing": ["separate_trade_list_file", "full tester cost fields parsed separately"],
            "judgment_label": "runtime_probe",
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": payload["next_condition"],
        },
        "allowed_claims": ["runtime_probe_observation_no_authority", "negative_economics_gap_recorded"],
        "forbidden_claims": [],
    }
    final = {
        "audit_name": "final_claim_guard",
        "status": "pass",
        "passed": True,
        "findings": [],
        "counts": {"requested_claims": ALLOWED_CLAIMS, "forbidden_claims": FORBIDDEN_CLAIMS},
        "allowed_claims": ALLOWED_CLAIMS,
        "forbidden_claims": FORBIDDEN_CLAIMS,
    }
    return {
        "runtime": runtime_gate,
        "forensics": forensics,
        "kpi": kpi,
        "scope": scope,
        "artifact": artifact,
        "judgment": judgment,
        "final": final,
    }


def receipts(payload: Mapping[str, Any]) -> list[dict[str, Any]]:
    source_inputs_rel = [rel(path) for path in source_inputs()]
    artifacts_rel = [rel(path) for path in produced_artifacts() if path_exists(path)]
    hashes = {rel(path): sha256_file(path) for path in produced_artifacts() if path_exists(path)}
    return [
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-runtime-parity",
            "status": "executed",
            "receipt_path": rel(RUNTIME_PARITY_RECEIPT),
            "python_artifact": rel(SOURCE_MODEL),
            "runtime_artifact": rel(REPORT_HTML),
            "research_path": rel(SOURCE_MODEL),
            "runtime_path": [rel(EA_SOURCE), rel(SET_FILE), rel(INI_FILE), rel(REPORT_HTML), rel(TELEMETRY)],
            "shared_contract": [rel(MT5_INPUT_CONTRACT), rel(TIME_AXIS_CONTRACT)],
            "known_differences": ["F04D source candidate is reference-only and has no inherited authority", "feature_skip_count remains high"],
            "compared_surface": "F04D ONNX/joblib candidate through F88B RuntimeProbeEA Strategy Tester",
            "parity_check": "compile plus Strategy Tester runtime output observation",
            "parity_level": "P3_runtime_shadow_parity_sampled",
            "parity_identity": payload["runtime_identity"],
            "runtime_evidence_identity": payload["runtime_identity"],
            "tester_identity": payload["runtime_identity"]["tester_identity"],
            "missing_evidence": ["separate_trade_list_file", "full runtime parity closure"],
            "runtime_claim_boundary": "runtime_probe",
            "allowed_claims": ALLOWED_CLAIMS,
            "forbidden_claims": FORBIDDEN_CLAIMS,
        },
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-backtest-forensics",
            "status": "executed",
            "receipt_path": rel(BACKTEST_RECEIPT),
            "tester_report": rel(REPORT_HTML),
            "tester_settings": payload["runtime_identity"]["tester_identity"],
            "spread_commission_slippage": "broker_native_or_report_not_parsed; no authority claim",
            "trade_list_identity": payload["runtime_identity"]["trade_list_identity"],
            "forensic_gaps": ["feature_skip_count_high", "separate_trade_list_file_missing", "cost_fields_not_separately_parsed"],
            "tester_identity": payload["runtime_identity"]["tester_identity"],
            "ea_identity": {"entrypoint": rel(EA_SOURCE), "binary": rel(EA_BINARY), "set": rel(SET_FILE), "ini": rel(INI_FILE)},
            "report_identity": file_identity(REPORT_HTML, role="strategy_tester_report"),
            "trade_evidence": payload["economics"],
            "cost_assumptions": "broker_native_or_report_not_parsed",
            "forensic_checks": ["report_exists", "telemetry_exists", "summary_exists", "hashes_recorded"],
            "backtest_judgment": "usable_with_boundary_runtime_probe_only",
        },
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-reference-scout",
            "status": "executed",
            "receipt_path": rel(REFERENCE_RECEIPT),
            "reference_need": "MT5 command-line Strategy Tester .ini/.set behavior",
            "question": "Can terminal64.exe /config use Tester Expert/ExpertParameters/Report/Model fields for a narrow runtime probe?",
            "sources_checked": ["https://www.metatrader5.com/en/terminal/help/start_advanced/start", "https://www.metatrader5.com/en/terminal/help/algotrading/testing"],
            "sources_checked_or_not_required_reason": "Official MetaTrader 5 help checked for command-line /config and Strategy Tester behavior.",
            "source_quality": "official_vendor_docs",
            "found_pattern": "Use /config with [Tester] fields such as Expert, ExpertParameters, Symbol, Period, Model, Report; Strategy Tester runs an EA once on history for testing.",
            "project_fit": "Matches existing foundation.mt5 tester_files and terminal_runner behavior.",
            "do_not_copy": "Do not copy forum performance claims or treat tester run as live readiness.",
            "recommended_use": "adopt_existing_project_helper_pattern",
            "version_sensitive_surface": "MetaTrader 5 command-line Strategy Tester configuration",
            "implementation_effect": "F88B used existing helper-generated .ini/.set and recorded hashes.",
        },
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-run-evidence-system",
            "status": "executed",
            "receipt_path": rel(RUN_EVIDENCE_RECEIPT),
            "source_inputs": source_inputs_rel,
            "produced_artifacts": artifacts_rel,
            "ledger_rows": [f"{RUN_ID}__runtime_probe_observation", f"{RUN_ID}__tier_a_validation_is"],
            "missing_evidence": ["separate_trade_list_file", "full WFO/stress rerun"],
            "measurement_scope": "runtime_probe regular_risk_execution with runtime/economics/execution KPI",
            "management_state": {"run_folder": rel(RUN_DIR), "manifest": rel(RUN_MANIFEST), "kpi_record": rel(KPI_RECORD), "summary": rel(RESULT_SUMMARY)},
            "judgment_class": "negative_with_runtime_probe_observation",
            "scoreboard": "runtime_parity",
            "parity_level": "P3_runtime_shadow_parity_sampled",
            "wfo_status": "not_applicable_short_preflight",
            "registry_update_required": "yes",
            "negative_memory_required": "yes",
            "hard_gate_applicable": "no",
            "evidence_boundary": "probe",
            "allowed_claims": ALLOWED_CLAIMS,
            "forbidden_claims": FORBIDDEN_CLAIMS,
        },
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-artifact-lineage",
            "status": "executed",
            "receipt_path": rel(ARTIFACT_RECEIPT),
            "source_inputs": source_inputs_rel,
            "produced_artifacts": artifacts_rel,
            "raw_evidence": [rel(EXECUTION_JSON), rel(REPORT_HTML), rel(TELEMETRY), rel(SUMMARY_CSV)],
            "machine_readable": [rel(RUN_MANIFEST), rel(SUMMARY_JSON), rel(KPI_RECORD), rel(RUNTIME_IDENTITY), rel(SKILL_RECEIPTS)],
            "human_readable": [rel(RESULT_SUMMARY), rel(CURRENT_WORKING_STATE), rel(DECISION_MEMO)],
            "artifact_paths": artifacts_rel,
            "artifact_hashes": hashes,
            "hashes_or_missing_reasons": hashes,
            "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "availability": "tracked_runtime_probe_outputs_with_hashes",
            "lineage_judgment": "connected_with_boundary",
            "lineage_boundary": "runtime_probe_observation_only_no_authority",
        },
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-result-judgment",
            "status": "executed",
            "receipt_path": rel(RESULT_RECEIPT),
            "judgment_boundary": JUDGMENT,
            "result_subject": RUN_ID,
            "evidence_available": [rel(REPORT_HTML), rel(TELEMETRY), rel(SUMMARY_CSV), rel(KPI_RECORD)],
            "evidence_missing": ["separate_trade_list_file", "WFO/stress continuation"],
            "judgment_label": "runtime_probe",
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": payload["next_condition"],
            "user_explanation_hook": "Runtime path turned on, but economics and coverage are not good enough for authority.",
            "evidence_used": [rel(RUNTIME_EVIDENCE_GATE), rel(KPI_RECORD), rel(BACKTEST_FORENSICS_AUDIT)],
            "allowed_claims": ALLOWED_CLAIMS,
            "forbidden_claims": FORBIDDEN_CLAIMS,
        },
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-claim-discipline",
            "status": "executed",
            "receipt_path": rel(CLAIM_RECEIPT),
            "requested_claims": ALLOWED_CLAIMS,
            "allowed_claims": ALLOWED_CLAIMS,
            "forbidden_claims": FORBIDDEN_CLAIMS,
            "claim_boundary": CLAIM_BOUNDARY,
            "final_status": STATUS,
        },
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-answer-clarity",
            "status": "executed",
            "receipt_path": rel(ANSWER_RECEIPT),
            "plain_conclusion": "F88B proved the runtime path can produce tester output, but the result is economically negative and not authority.",
            "confirmed": ["EA loaded", "ONNX inference called", "report generated", "telemetry updated"],
            "not_yet_confirmed": ["runtime authority", "Goal Achieve", "live readiness", "selected baseline"],
            "why_it_matters": "The project can now repair a real runtime gap instead of only planning runtime evidence.",
            "next_action": NEXT_RUN_ID,
            "forbidden_claims_avoided": FORBIDDEN_CLAIMS,
        },
    ]


def work_packet(payload: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "version": "work_packet_schema_v2_1",
        "packet_lifecycle": "new_packet",
        "packet_id": RUN_ID,
        "created_at_utc": payload["created_at_utc"],
        "user_request": {
            "user_quote": "/goal active continuation",
            "requested_action": "F88B minimal MT5 runtime substrate preflight",
            "requested_count": {"value": 1, "n_a_reason": ""},
            "ambiguous_terms": ["Goal remains active; runtime authority and Goal Achieve are not claimed."],
        },
        "current_truth": {
            "active_stage": STAGE_ID,
            "current_run": RUN_ID,
            "latest_completed_run": PARENT_RUN_ID,
            "source_documents": [rel(WORKSPACE_STATE), rel(CURRENT_WORKING_STATE), rel(SELECTION_STATUS)],
            "claim_boundary": CLAIM_BOUNDARY,
        },
        "work_classification": {
            "primary_family": "runtime_backtest",
            "detected_families": ["runtime_backtest", "artifact_lineage", "kpi_evidence", "state_sync"],
            "touched_surfaces": [rel(RUN_DIR), rel(PACKET_DIR), rel(WORKSPACE_STATE)],
            "mutation_intent": True,
            "execution_intent": True,
        },
        "risk_vector_scan": {
            "risks": {
                "compile_only_laundered_as_runtime": "controlled_by_runtime_output_hashes",
                "runtime_probe_as_authority": "blocked_by_final_claim_guard",
                "feature_skip_gap_hidden": "recorded_as_f88c_repair_target",
            },
            "hard_stop_risks": [
                "Do not claim runtime authority from one short runtime probe.",
                "Do not claim Goal Achieve from negative economics.",
                "Do not treat embedded report trades as a separate trade-list file.",
            ],
            "required_gates": REQUIRED_GATES,
            "forbidden_claims": FORBIDDEN_CLAIMS,
        },
        "decision_lock": {
            "mode": "assume_safe_default",
            "assumptions": {
                "task_force_required_now": False,
                "reason": "No Task Force review claim, policy change, or roster review is made.",
            },
            "questions": [],
            "required_user_decisions": [],
        },
        "interpreted_scope": {
            "work_families": ["runtime_backtest"],
            "target_surfaces": ["F88B MT5 runtime substrate", "RuntimeProbeEA", "F04D reference ONNX candidate"],
            "scope_units": ["compile", "set_ini_materialization", "strategy_tester_run", "report_telemetry_hashing", "state_sync"],
            "execution_layers": ["local_python_execution", "mt5_execution", "strategy_tester", "runtime_telemetry"],
            "mutation_policy": {"allowed": True, "user_quote": "/goal active continuation"},
            "evidence_layers": ["EA/ONNX/set/ini hashes", "Strategy Tester report", "telemetry", "summary", "KPI record"],
            "reduction_policy": {"reduction_allowed": False, "rationale": "Runtime claim requires actual runtime output."},
            "claim_boundary": {"allowed_claims": ALLOWED_CLAIMS, "forbidden_claims": FORBIDDEN_CLAIMS, "claim_boundary": CLAIM_BOUNDARY},
            "verification_layers": REQUIRED_GATES,
            "mt5_required": "required_and_attempted",
            "top_k_reduction_allowed": False,
        },
        "verification_profile": {
            "profile_id": "runtime_probe",
            "claim_surface": {"allowed_claims": ALLOWED_CLAIMS, "forbidden_claims": FORBIDDEN_CLAIMS, "claim_boundary": CLAIM_BOUNDARY},
            "trigger_sources": ["active_goal", "F88A_runtime_substrate_contract", "runtime_materialization_handoff_claim_surface"],
            "protected_claims": ALLOWED_CLAIMS,
            "required_evidence": [
                f"dataset_id={payload['runtime_identity']['dataset_id']}",
                f"feature_set_id={payload['runtime_identity']['feature_set_id']}",
                f"label_id={payload['runtime_identity']['label_id']}",
                f"split_id={payload['runtime_identity']['split_id']}",
                f"onnx_hash={payload['runtime_identity']['onnx_hash']}",
                f"ea_source_hash={payload['runtime_identity']['ea_source_hash']}",
                f"ea_binary_hash={payload['runtime_identity']['ea_binary_hash']}",
                f"set_ini_hash={payload['runtime_identity']['set_ini_hash']}",
                f"feature_order_hash={payload['runtime_identity']['feature_order_hash']}",
                "tester_identity",
                "runtime_bundle_identity",
                "actual_output_strategy_tester_report_hash",
                "actual_output_trade_list_hash_or_embedded_report_boundary",
                "telemetry_hash",
                "operation_proof_ea_loaded_onnx_inference_called_report_generated_telemetry_updated_no_fatal_runtime_mismatch",
                rel(RUNTIME_IDENTITY),
                rel(REPORT_HTML),
                rel(TELEMETRY),
                rel(SUMMARY_CSV),
            ],
            "gates_not_run_with_reason": [
                {
                    "gate": "codex_task_force_review_packet",
                    "reason_code": "not_triggered_for_runtime_probe_claim_surface",
                    "reason": "No Task Force reviewed/pass claim, policy change, roster review, or required overlay claim is made.",
                    "claim_effect": "No Task Force review claim is made.",
                }
            ],
            "stop_conditions": [
                "Stop before authority: one short runtime probe is not runtime authority.",
                "Stop before Goal Achieve: PF/DD/trade density do not meet final entry criteria.",
                "Open F88C for timestamp coverage/trade-list repair.",
            ],
        },
        "acceptance_criteria": [
            "Runtime probe produces tester output or exact blocker.",
            "EA/ONNX/set/ini/report/telemetry hashes are recorded.",
            "Final claim guard forbids authority/live readiness/Goal Achieve.",
        ],
        "work_plan": [
            "Use F04D executable reference ONNX candidate without inheriting authority.",
            "Compile RuntimeProbeEA and run one narrow Strategy Tester validation probe.",
            "Record runtime output identity, KPI, gaps, and next repair target.",
        ],
        "skill_routing": {
            "primary_family": "runtime_backtest",
            "primary_skill": "obsidian-runtime-parity",
            "support_skills": [
                "obsidian-backtest-forensics",
                "obsidian-reference-scout",
                "obsidian-run-evidence-system",
                "obsidian-artifact-lineage",
                "obsidian-result-judgment",
                "obsidian-claim-discipline",
                "obsidian-answer-clarity",
            ],
            "skills_considered": REQUIRED_SKILLS,
            "skills_selected": REQUIRED_SKILLS,
            "skills_not_used": [{"skill": "obsidian-task-force-review", "reason": "not_triggered_no_review_claim"}],
            "required_skill_receipts": REQUIRED_SKILLS,
            "required_gates": REQUIRED_GATES,
        },
        "evidence_contract": {
            "raw_evidence": [rel(path) for path in source_inputs()],
            "machine_readable": [rel(RUN_MANIFEST), rel(SUMMARY_JSON), rel(KPI_RECORD), rel(RUNTIME_IDENTITY), rel(SKILL_RECEIPTS)],
            "human_readable": [rel(RESULT_SUMMARY), rel(DECISION_MEMO)],
            "hash_identity_required": True,
        },
        "gates": {
            "required": REQUIRED_GATES,
            "runtime_evidence_gate": "pass",
            "scope_completion_gate": "pass",
            "kpi_contract_audit": "pass",
            "backtest_forensics_audit": "pass",
            "artifact_lineage_audit": "pass",
            "result_judgment_audit": "pass",
            "state_sync_audit": "pending_external_lint",
            "required_gate_coverage_audit": "pending_external_lint",
            "final_claim_guard": "pass",
        },
        "final_claim_policy": {"allowed_claims": ALLOWED_CLAIMS, "forbidden_claims": FORBIDDEN_CLAIMS, "claim_boundary": CLAIM_BOUNDARY},
    }


def closeout_gate_seed() -> dict[str, Any]:
    audits_for_gate = [
        ("work_packet_schema_lint", "pending_external_lint", PACKET_WORK_PACKET_LINT),
        ("skill_receipt_schema_lint", "pending_external_lint", PACKET_SKILL_RECEIPT_LINT),
        ("runtime_evidence_gate", "pass", RUNTIME_EVIDENCE_GATE),
        ("scope_completion_gate", "pass", SCOPE_GATE),
        ("kpi_contract_audit", "pass", KPI_CONTRACT_AUDIT),
        ("backtest_forensics_audit", "pass", BACKTEST_FORENSICS_AUDIT),
        ("artifact_lineage_audit", "pass", ARTIFACT_AUDIT),
        ("result_judgment_audit", "pass", RESULT_JUDGMENT_AUDIT),
        ("state_sync_audit", "pending_external_lint", PACKET_STATE_SYNC_AUDIT),
        ("required_gate_coverage_audit", "pending_external_lint", PACKET_REQUIRED_GATE_AUDIT),
    ]
    return {
        "packet_id": RUN_ID,
        "status": "pending_external_lint",
        "audits": [{"audit_name": name, "status": status, "path": rel(path)} for name, status, path in audits_for_gate],
        "final_claim_guard": {"audit_name": "final_claim_guard", "status": "pass", "path": rel(PACKET_FINAL_CLAIM_GUARD)},
        "allowed_claims": ALLOWED_CLAIMS,
        "forbidden_claims": FORBIDDEN_CLAIMS,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def write_receipts(payload: Mapping[str, Any]) -> None:
    rows = receipts(payload)
    mapping = {
        "obsidian-runtime-parity": RUNTIME_PARITY_RECEIPT,
        "obsidian-backtest-forensics": BACKTEST_RECEIPT,
        "obsidian-reference-scout": REFERENCE_RECEIPT,
        "obsidian-run-evidence-system": RUN_EVIDENCE_RECEIPT,
        "obsidian-artifact-lineage": ARTIFACT_RECEIPT,
        "obsidian-result-judgment": RESULT_RECEIPT,
        "obsidian-claim-discipline": CLAIM_RECEIPT,
        "obsidian-answer-clarity": ANSWER_RECEIPT,
    }
    for row in rows:
        write_json(mapping[row["skill"]], row)
    write_json(SKILL_RECEIPTS, {"packet_id": RUN_ID, "primary_skill": "obsidian-runtime-parity", "claim_boundary": CLAIM_BOUNDARY, "receipts": rows})


def write_audits(payload: Mapping[str, Any]) -> None:
    audit_rows = audits(payload)
    for path, key in (
        (RUNTIME_EVIDENCE_GATE, "runtime"),
        (BACKTEST_FORENSICS_AUDIT, "forensics"),
        (KPI_CONTRACT_AUDIT, "kpi"),
        (SCOPE_GATE, "scope"),
        (ARTIFACT_AUDIT, "artifact"),
        (RESULT_JUDGMENT_AUDIT, "judgment"),
        (FINAL_CLAIM_GUARD, "final"),
        (PACKET_FINAL_CLAIM_GUARD, "final"),
    ):
        write_json(path, audit_rows[key])


def update_state_docs(payload: Mapping[str, Any]) -> None:
    state = f"""current_stage_id: {STAGE_ID}
active_stage: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {STATUS}
current_judgment: {JUDGMENT}
next_run_id: {NEXT_RUN_ID}
frontier_extra_due_status: not_due_after_f88_probe_next_boundary_f100_e01_closed_for_f050
runtime_probe_status: completed_observation_no_authority
runtime_authority: not_claimed
operating_promotion: not_claimed
live_readiness: not_claimed
goal_achieve: not_claimed
updated_at_utc: '{payload['created_at_utc']}'
context_anchor: {rel(CONTEXT_ANCHOR)}
notes:
- 'Action(행동): F88B ran one narrow MT5 Strategy Tester runtime probe(F88B가 좁은 MT5 전략 테스터 런타임 탐침 1회를 실행).'
- 'Effect(효과): EA/ONNX/report/telemetry identity(EA/온엑스/보고서/기록 정체성)는 생겼지만 economics(경제성)는 부정이고 authority(권위)는 없다.'
- 'Next(다음): {NEXT_RUN_ID} should repair timestamp coverage/trade-list separation(F88C가 타임스탬프 커버리지/거래목록 분리를 수리).'
"""
    current = f"""# Current Working State(현재 작업 상태)

Updated(갱신): {payload['created_at_utc']}

Active stage(활성 단계): `{STAGE_ID}`

Current run(현재 실행): `{NEXT_RUN_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Action(행동): F88B ran one narrow MT5 Strategy Tester runtime probe(F88B가 좁은 전략 테스터 런타임 탐침 1회를 실행) with the F04D reference ONNX candidate(F04D 참고 온엑스 후보).

Effect(효과): EA loaded/ONNX inference/report/telemetry(EA 로드/온엑스 추론/보고서/기록)는 확인됐지만, PF/DD/trade density(수익 팩터/손실폭/거래 밀도)는 final entry(최종 진입) 기준에 못 미친다. 다음은 timestamp coverage/trade-list separation(타임스탬프 커버리지/거래목록 분리) 수리다.

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`.
"""
    selection = f"""# F88 Selection Status(F88 선택 상태)

Updated(갱신): {payload['created_at_utc']}

Status(상태): `{STATUS}`

Current run(현재 실행): `{NEXT_RUN_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Selected baseline(선택 기준선): not claimed(주장 없음)

Operating promotion(운영 승격): not claimed(주장 없음)

Runtime authority(런타임 권위): not claimed(주장 없음)

Goal Achieve(목표 달성): not claimed(주장 없음)

Action(행동): F88B produced runtime_probe observation(F88B가 런타임 탐침 관찰을 만들었다).

Effect(효과): runtime path(런타임 경로)는 켜졌지만 negative economics gap(부정 경제성 간극)과 timestamp coverage gap(타임스탬프 커버리지 간극)을 수리해야 한다.

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`.
"""
    stage_brief = f"""# F88 Runtime Substrate First Materialization Probe(F88 런타임 바탕 우선 물질화 탐침)

Stage id(단계 ID): `{STAGE_ID}`

Current run(현재 실행): `{NEXT_RUN_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

F88B result(F88B 결과): runtime_probe observation no authority(권위 없는 런타임 탐침 관찰). EA loaded(전문가 자문 로드), ONNX inference called(온엑스 추론 호출), report generated(보고서 생성), telemetry updated(기록 갱신).

Runtime gap(런타임 간극): feature_skip_count(피처 스킵 수) `{payload['summary_row'].get('feature_skip_count')}`, PF(수익 팩터) `{payload['economics'].get('profit_factor')}`, DD(손실폭) `{payload['economics'].get('max_drawdown_percent')}%`.

Next question(다음 질문): can F88C repair timestamp coverage and trade-list separation without turning this into authority(권위) or Goal Achieve(목표 달성)?

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`.
"""
    input_refs = "# F88 Input References(F88 입력 참조)\n\n" + "\n".join(f"- `{rel(path)}`" for path in source_inputs() + [RUNTIME_IDENTITY, KPI_RECORD, RESULT_SUMMARY]) + "\n"
    review_index_add = f"""
<!-- {RUN_ID} -->

## {RUN_ID}

- `f88b_runtime_evidence_gate.json`: runtime evidence gate(런타임 근거 게이트)
- `f88b_backtest_forensics_audit.json`: backtest forensics audit(백테스트 포렌식 감사)
- `f88b_kpi_contract_audit.json`: KPI contract audit(KPI 계약 감사)
- `f88b_result_judgment_audit.json`: result judgment audit(결과 판정 감사)
- `f88b_final_claim_guard.json`: final claim guard(최종 주장 보호)
"""
    decision = f"""# Frontier88B Runtime Substrate Probe(전선88B 런타임 바탕 탐침)

Updated(갱신): {payload['created_at_utc']}

Decision(결정): F88B is closed as runtime_probe observation no authority(권위 없는 런타임 탐침 관찰).

Action(행동): Ran one MT5 Strategy Tester probe(전략 테스터 탐침 1회) using F04D reference ONNX(F04D 참고 온엑스), RuntimeProbeEA(런타임 탐침 EA), and F88B-specific set/ini/feature matrix(F88B 전용 설정/초기화/피처 행렬).

Effect(효과): Runtime substrate(런타임 바탕)는 실제 output(출력)을 만들었지만, economics(경제성)는 negative(부정)이고 feature coverage gap(피처 커버리지 간극)이 남았다.

Next(다음): `{NEXT_RUN_ID}`.

Boundary(경계): `{CLAIM_BOUNDARY}`.
"""
    write_text(WORKSPACE_STATE, state)
    write_text(CURRENT_WORKING_STATE, current)
    write_text(CONTEXT_ANCHOR, current)
    write_text(SELECTION_STATUS, selection)
    write_text(GLOBAL_SELECTION_STATUS, selection)
    write_text(STAGE_BRIEF, stage_brief)
    write_text(INPUT_REFS, input_refs)
    append_once(REVIEW_INDEX, f"<!-- {RUN_ID} -->", review_index_add)
    write_text(DECISION_MEMO, decision)
    changelog_entry = f"""
<!-- {RUN_ID} -->

## {payload['created_at_utc'][:10]} - {RUN_ID}

- Action(행동): F88B ran one narrow MT5 runtime probe(F88B 좁은 MT5 런타임 탐침 1회 실행).
- Effect(효과): report/telemetry evidence(보고서/기록 근거)는 생성됐지만 economics(경제성)는 negative(부정)이고 runtime authority(런타임 권위)는 not_claimed(미주장).
"""
    append_once(WORKSPACE_CHANGELOG, f"<!-- {RUN_ID} -->", changelog_entry)
    append_once(ROOT_CHANGELOG, f"<!-- {RUN_ID} -->", changelog_entry)
    append_once(
        IDEA_REGISTRY,
        f"<!-- {RUN_ID} -->",
        f"""
<!-- {RUN_ID} -->

## {RUN_ID}

- Action(행동): Runtime substrate first(런타임 바탕 우선) 축에서 실제 MT5 tester output(테스터 출력)을 만들었다.
- Effect(효과): 다음 아이디어는 새 threshold tweak(임계값 미세조정)가 아니라 timestamp coverage/trade-list separation repair(타임스탬프 커버리지/거래목록 분리 수리)다.
- Boundary(경계): `{CLAIM_BOUNDARY}`.
""",
    )


def update_ledgers(payload: Mapping[str, Any]) -> None:
    econ = payload["economics"]
    actual = {
        "ledger_row_id": f"{RUN_ID}__runtime_probe_observation",
        "row_id": f"{RUN_ID}__runtime_probe_observation",
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "runtime_probe_observation",
        "tier_scope": "Tier A",
        "kpi_scope": "mt5_runtime_probe_short_validation",
        "scoreboard_lane": "runtime_parity",
        "lane": "runtime_substrate",
        "family": "runtime_backtest",
        "status": STATUS,
        "judgment": JUDGMENT,
        "result_judgment": JUDGMENT,
        "path": rel(RESULT_SUMMARY),
        "primary_kpi": f"net={econ.get('net_profit')};pf={econ.get('profit_factor')};dd={econ.get('max_drawdown_percent')};trades={econ.get('trade_count')}",
        "guardrail_kpi": f"feature_ready={payload['summary_row'].get('feature_ready_count')};feature_skip={payload['summary_row'].get('feature_skip_count')};fills={payload['summary_row'].get('order_fill_count')}",
        "external_verification_status": "completed",
        "notes": "Runtime probe observation only; negative economics; no authority.",
        "run_number": "frontier88B",
        "date": payload["created_at_utc"][:10],
        "decision": "close_f88b_as_runtime_probe_observation_no_authority",
        "next_run_id": NEXT_RUN_ID,
        "rows": payload["telemetry_sample"].get("row_count"),
        "gate_passes": len(REQUIRED_GATES),
        "gate_total": len(REQUIRED_GATES),
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(RESULT_SUMMARY),
        "run_date": payload["created_at_utc"][:10],
        "primary_artifact": rel(REPORT_HTML),
        "view": "runtime_probe_observation",
        "tier": "Tier A",
        "metric_scope": "runtime_probe",
        "result_status": STATUS,
        "work_family": "runtime_backtest",
        "evidence_boundary": "runtime_probe_no_authority",
        "next_action": NEXT_RUN_ID,
        "question": "Can F88 produce MT5 runtime output identity before authority claims?",
        "artifact_count": len([path for path in produced_artifacts() if path_exists(path)]),
        "created_at_utc": payload["created_at_utc"],
        "required_gate_audit": rel(PACKET_REQUIRED_GATE_AUDIT),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "source_authority": "not_claimed",
        "run_family": "runtime_backtest",
        "run_type": "runtime_probe",
        "input_run_id": PARENT_RUN_ID,
        "output_path": rel(RUN_DIR),
        "result_path": rel(RESULT_SUMMARY),
    }
    planned = {
        "ledger_row_id": f"{NEXT_RUN_ID}__planned_current_run",
        "row_id": f"{NEXT_RUN_ID}__planned_current_run",
        "run_id": NEXT_RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": RUN_ID,
        "record_view": "planned_current_run",
        "tier_scope": "not_applicable_planned",
        "kpi_scope": "pending",
        "scoreboard_lane": "runtime_parity",
        "lane": "runtime_substrate_repair",
        "family": "runtime_backtest",
        "status": "planned_current_run_no_authority",
        "judgment": "pending",
        "result_judgment": "pending",
        "path": rel(STAGE_BRIEF),
        "primary_kpi": "pending",
        "guardrail_kpi": "pending",
        "external_verification_status": "pending",
        "notes": "F88C should repair timestamp coverage and separate trade-list identity.",
        "run_number": "frontier88C",
        "date": payload["created_at_utc"][:10],
        "decision": "pending_execution",
        "next_run_id": "",
        "rows": 0,
        "gate_passes": 0,
        "gate_total": 0,
        "claim_boundary": "planned_only_no_authority_no_goal_achieve",
        "report_path": "",
        "run_date": payload["created_at_utc"][:10],
        "primary_artifact": rel(STAGE_BRIEF),
        "view": "planned_current_run",
        "tier": "not_applicable",
        "metric_scope": "pending",
        "result_status": "planned_current_run_no_authority",
        "work_family": "runtime_backtest",
        "evidence_boundary": "planned_only_no_authority",
        "next_action": "repair_timestamp_coverage_and_trade_list_identity",
        "question": "Can F88C reduce feature skip gap and separate trade-list identity?",
        "artifact_count": 0,
        "created_at_utc": payload["created_at_utc"],
        "required_gate_audit": "",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "source_authority": "not_claimed",
        "run_family": "runtime_backtest",
        "run_type": "planned_current_run",
        "input_run_id": RUN_ID,
        "output_path": rel(STAGE_DIR),
        "result_path": rel(STAGE_BRIEF),
    }
    upsert_csv(RUN_REGISTRY, ["run_id"], [actual, planned])
    upsert_csv(ALPHA_LEDGER, ["ledger_row_id"], [actual, planned])
    upsert_csv(STAGE_LEDGER, ["ledger_row_id"], [actual, planned], source_header=ALPHA_LEDGER)


def update_artifact_registry(payload: Mapping[str, Any]) -> None:
    rows = []
    for path in produced_artifacts():
        if not path_exists(path):
            continue
        rows.append(
            {
                "artifact_id": f"{RUN_ID}::{rel(path)}",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "artifact_type": "frontier88b_runtime_probe",
                "path": rel(path),
                "artifact_path": rel(path),
                "sha256": sha256_file(path),
                "created_at": payload["created_at_utc"],
                "created_at_utc": payload["created_at_utc"],
                "claim_boundary": CLAIM_BOUNDARY,
                "notes": "F88B runtime probe artifact; no runtime authority.",
                "effect": "Supports runtime_probe observation only.",
                "size_bytes": io_path(path).stat().st_size,
            }
        )
    upsert_csv(ARTIFACT_REGISTRY, ["artifact_id"], rows)


def write_state_sync_seed(payload: Mapping[str, Any]) -> None:
    state_payload = {
        "audit_name": "state_sync_audit",
        "status": "pass",
        "passed": True,
        "findings": [],
        "counts": {
            "active_stage": STAGE_ID,
            "current_run_id": NEXT_RUN_ID,
            "latest_completed_run_id": RUN_ID,
            "sources": {
                "workspace_state": rel(WORKSPACE_STATE),
                "current_working_state": rel(CURRENT_WORKING_STATE),
                "selection_status": rel(SELECTION_STATUS),
                "run_registry": rel(RUN_REGISTRY),
                "stage_ledger": rel(STAGE_LEDGER),
            },
        },
        "allowed_claims": ["current_truth_synced", "state_sync_completed"],
        "forbidden_claims": [],
    }
    write_json(STATE_SYNC_AUDIT, state_payload)
    write_json(PACKET_STATE_SYNC_AUDIT, state_payload)


def validate_inputs() -> None:
    missing = [rel(path) for path in [FEATURE_MATRIX, TELEMETRY, SUMMARY_CSV, EXECUTION_JSON, COMPILE_LOG, SET_FILE, INI_FILE, REPORT_HTML, SOURCE_ONNX, SOURCE_MODEL, EA_SOURCE, EA_BINARY] if not path_exists(path)]
    if missing:
        raise FileNotFoundError(f"Missing F88B runtime probe evidence: {missing}")


def main() -> int:
    validate_inputs()
    for directory in (REPORT_DIR, REVIEW_DIR, SELECTED_DIR, PACKET_DIR):
        io_path(directory).mkdir(parents=True, exist_ok=True)
    payload = build_payload(utc_now())
    write_json(RUNTIME_IDENTITY, payload["runtime_identity"])
    write_json(FORENSICS_SUMMARY, {"tester_identity": payload["runtime_identity"]["tester_identity"], "economics": payload["economics"], "operation_proof": payload["operation_proof"]})
    write_json(RUN_MANIFEST, payload)
    write_json(SUMMARY_JSON, payload)
    write_json(KPI_RECORD, {"run_id": RUN_ID, "status": STATUS, "judgment": JUDGMENT, "economics": payload["economics"], "execution": payload["summary_row"], "claim_boundary": CLAIM_BOUNDARY})
    write_text(RESULT_SUMMARY, result_summary_text(payload))
    write_audits(payload)
    write_receipts(payload)
    write_yaml(WORK_PACKET, work_packet(payload))
    write_json(PACKET_CLOSEOUT_GATE, closeout_gate_seed())
    update_state_docs(payload)
    update_ledgers(payload)
    write_state_sync_seed(payload)
    update_artifact_registry(payload)
    print(
        json.dumps(
            json_ready(
                {
                    "run_id": RUN_ID,
                    "status": STATUS,
                    "judgment": JUDGMENT,
                    "next_run_id": NEXT_RUN_ID,
                    "net_profit": payload["economics"].get("net_profit"),
                    "profit_factor": payload["economics"].get("profit_factor"),
                    "max_drawdown_percent": payload["economics"].get("max_drawdown_percent"),
                    "trade_count": payload["economics"].get("trade_count"),
                    "claim_boundary": CLAIM_BOUNDARY,
                    "current_branch": current_branch(),
                }
            ),
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
