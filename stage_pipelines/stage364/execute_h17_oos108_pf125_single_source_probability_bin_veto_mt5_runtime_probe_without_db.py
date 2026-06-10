from __future__ import annotations

import argparse
import json
import math
import shutil
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, json_ready  # noqa: E402
from stage_pipelines.stage364 import execute_h17_oos108_pf125_probability_bin_veto_mt5_runtime_probe_without_db as hk  # noqa: E402
from stage_pipelines.stage364 import materialize_h17_oos108_pf125_single_source_probability_bin_veto_runtime_package_without_db as pkg  # noqa: E402
from stage_pipelines.stage364.review_pf_pass_density_restore_offensive_scout_without_db import repair_run_registry_line_endings  # noqa: E402


TODAY = "2026-06-09"
STAGE_ID = pkg.STAGE_ID
RUN_NUMBER = "run364HP"
RUN_ID = "run364HP_execute_h17_oos108_pf125_single_source_probability_bin_veto_mt5_runtime_probe_without_db_v1"
PARENT_RUN_ID = pkg.RUN_ID
NEXT_RUN_ID = "run364HQ_review_h17_oos108_pf125_single_source_probability_bin_veto_mt5_runtime_probe_without_db_v1"

STATUS_COMPLETED = "completed_stage364HP_single_source_probability_bin_veto_mt5_probe_outputs_available_review_required_no_authority"
STATUS_BLOCKED = "blocked_stage364HP_single_source_probability_bin_veto_mt5_probe_attempt_recorded_repair_required_no_authority"
JUDGMENT_COMPLETED = "mt5_runtime_probe_outputs_available_single_source_probability_bin_veto_proxy_diff_review_required_no_authority"
JUDGMENT_BLOCKED = "mt5_runtime_probe_attempt_recorded_single_source_probability_bin_veto_outputs_missing_or_failed_repair_required_no_authority"
DECISION_COMPLETED = "stage364HP_open_run364HQ_review_single_source_probability_bin_veto_mt5_runtime_probe"
DECISION_BLOCKED = "stage364HP_open_run364HQ_repair_or_review_single_source_probability_bin_veto_mt5_runtime_probe"
CLAIM_BOUNDARY = (
    "research_development_mt5_runtime_probe_attempt_only_single_source_probability_bin_veto_"
    "no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

BASEPKG = pkg.hj.basepkg
MODEL_ID = pkg.MODEL_ID
CANDIDATE_ID = "single_source_probability_bin_veto"

STAGE_DIR = pkg.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
MT5_DIR = RUN_DIR / "mt5"
TELEMETRY_COPY_DIR = RUN_DIR / "runtime_telemetry"
REPORT_COPY_DIR = MT5_DIR / "reports"
REVIEW_DIR = STAGE_DIR / "03_reviews"
SPEC_DIR = STAGE_DIR / "00_spec"
SELECTED_DIR = STAGE_DIR / "04_selected"

RUNTIME_PROBE_ATTEMPT_PACKAGE = RUN_DIR / "runtime_probe_attempt_package.csv"
TERMINAL_PROCESS_AUDIT = RUN_DIR / "terminal_process_audit.json"
MT5_EXECUTION_RESULT = RUN_DIR / "mt5_execution_result.json"
STRATEGY_TESTER_REPORTS = RUN_DIR / "strategy_tester_report_records.json"
EXECUTION_SUMMARY = RUN_DIR / "single_source_probability_bin_veto_mt5_probe_summary.csv"
PROXY_MT5_DIFF = RUN_DIR / "proxy_mt5_runtime_difference.csv"
RUNTIME_OUTPUT_COPY = RUN_DIR / "runtime_output_copy_manifest.csv"
RUNTIME_IDENTITY = RUN_DIR / "runtime_identity.csv"
EXPECTED_KPI_SUMMARY = RUN_DIR / "expected_kpi_summary.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
BACKTEST_RECEIPT = RUN_DIR / "backtest_forensics_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / "run364HP_single_source_probability_bin_veto_mt5_runtime_probe.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364HP_single_source_probability_bin_veto_mt5_runtime_probe.md"
REVIEW_INDEX = REVIEW_DIR / "review_index.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"
STAGE_BRIEF = SPEC_DIR / "stage_brief.md"
SELECTION_STATUS = SELECTED_DIR / "selection_status.md"
STAGE_README = STAGE_DIR / "README.md"

WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
PROJECT_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
IDEA_REGISTRY = ROOT / "docs" / "registers" / "idea_registry.md"
NEGATIVE_REGISTER = ROOT / "docs" / "registers" / "negative_result_register.md"

INPUT_FILES = [
    pkg.FINAL_DECISION,
    pkg.GATE_AUDIT,
    pkg.RUNTIME_PROBE_ATTEMPT_PACKAGE,
    pkg.TESTER_SET_MANIFEST,
    pkg.TESTER_INI_MANIFEST,
    pkg.RUNTIME_POLICY_CONFIG,
    pkg.TESTER_IDENTITY_CONTRACT,
    pkg.PROXY_MT5_COMPARISON_CONTRACT,
    pkg.RUNTIME_PARITY_CONTRACT,
    pkg.EXPECTED_KPI_SUMMARY,
    pkg.RUNTIME_REPRESENTATION_AUDIT,
    pkg.COMMON_FILES_SYNC,
    pkg.RUN_MANIFEST,
    pkg.FEATURE_ORDER_CONTRACT,
    pkg.FEATURE_MATRIX,
    pkg.MT5_ONNX,
    pkg.PORTABLE_EA_EX5,
    Path(__file__),
]

OUTPUT_FILES = [
    RUNTIME_PROBE_ATTEMPT_PACKAGE,
    TERMINAL_PROCESS_AUDIT,
    MT5_EXECUTION_RESULT,
    STRATEGY_TESTER_REPORTS,
    EXECUTION_SUMMARY,
    PROXY_MT5_DIFF,
    RUNTIME_OUTPUT_COPY,
    RUNTIME_IDENTITY,
    EXPECTED_KPI_SUMMARY,
    WORK_PACKET,
    BACKTEST_RECEIPT,
    RUNTIME_RECEIPT,
    PERFORMANCE_RECEIPT,
    JUDGMENT_RECEIPT,
    LINEAGE_RECEIPT,
    CLAIM_RECEIPT,
    GATE_AUDIT,
    FINAL_DECISION,
    RUN_MANIFEST,
    REPORT_PATH,
    DECISION_DOC,
    REVIEW_INDEX,
    STAGE_LEDGER,
    STAGE_BRIEF,
    SELECTION_STATUS,
    STAGE_README,
    WORKSPACE_STATE,
    CURRENT_WORKING_STATE,
    WORKSPACE_CHANGELOG,
    RUN_REGISTRY,
    PROJECT_LEDGER,
    ARTIFACT_REGISTRY,
    IDEA_REGISTRY,
    NEGATIVE_REGISTER,
    Path(__file__),
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Stage364HP single-source probability-bin veto MT5 runtime probe.")
    parser.add_argument("--terminal-path", default=str(BASEPKG.DEFAULT_TERMINAL))
    parser.add_argument("--common-files-root", default=str(BASEPKG.DEFAULT_COMMON_FILES))
    parser.add_argument("--tester-profile-root", default=str(BASEPKG.DEFAULT_TESTER_PROFILE_ROOT))
    parser.add_argument("--terminal-data-root", default=str(BASEPKG.DEFAULT_PORTABLE_ROOT))
    parser.add_argument("--timeout-seconds", type=int, default=900)
    parser.add_argument("--wait-timeout-seconds", type=int, default=240)
    parser.add_argument("--reuse-existing-execution", action="store_true")
    return parser.parse_args()


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    resolved = Path(path).resolve()
    try:
        return resolved.relative_to(ROOT).as_posix()
    except ValueError:
        return resolved.as_posix()


def exists(path: Path | str) -> bool:
    return pkg.exists(path)


def sha(path: Path | str) -> str:
    return pkg.sha(path)


def fs_path(path: Path | str) -> str:
    return str(io_path(path))


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(io_path(path), encoding="utf-8-sig").fillna("")


def write_json(path: Path, payload: Any) -> None:
    pkg.write_json(path, payload)


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    pkg.write_csv(path, rows, fieldnames)


def write_text(path: Path, text: str, *, bom: bool = True) -> None:
    pkg.write_text(path, text, bom=bom)


def append_text_once(path: Path, marker: str, text: str) -> None:
    pkg.append_text_once(path, marker, text)


def append_or_replace_csv(path: Path, key_fields: Sequence[str], rows: Sequence[Mapping[str, Any]], *, extend_header: bool = True) -> None:
    try:
        pkg.append_or_replace_csv(path, key_fields, rows, extend_header=extend_header)
    except TypeError:
        pkg.append_or_replace_csv(path, key_fields, rows)


def replace_prefixed_lines(path: Path, replacements: Mapping[str, str], *, bom: bool = True) -> None:
    pkg.replace_prefixed_lines(path, replacements, bom=bom)


def finite(value: Any, digits: int = 10) -> float | str:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return ""
    if not math.isfinite(number):
        return ""
    return round(number, digits)


def float_or_nan(value: Any) -> float:
    try:
        if value in ("", None):
            return math.nan
        return float(value)
    except (TypeError, ValueError):
        return math.nan


def parse_set_values(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for raw in io_path(path).read_text(encoding="utf-8-sig").splitlines():
        line = raw.strip()
        if not line or line.startswith(";") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip()
    return values


def validate_parent() -> dict[str, Any]:
    missing = [rel(path) for path in INPUT_FILES if path != Path(__file__) and not exists(path)]
    if missing:
        raise FileNotFoundError("missing HP inputs(HP 입력 누락): " + ", ".join(missing))
    parent = read_json(pkg.FINAL_DECISION)
    if parent.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"HO next_run_id mismatch(HO 다음 실행 ID 불일치): {parent.get('next_run_id')} != {RUN_ID}")
    gates = read_csv(pkg.GATE_AUDIT)
    if gates.empty or any(gates["status"].astype(str) != "passed"):
        raise RuntimeError("HO gate audit(HO 게이트 감사)가 모두 passed(통과)가 아닙니다.")
    if not parent.get("compile_log_zero_errors") or not parent.get("portable_ea_copied"):
        raise RuntimeError("HO compile/sync(HO 컴파일/동기화)가 HP MT5 runtime probe(HP MT5 런타임 탐침)에 충분하지 않습니다.")
    forbidden = [parent.get("runtime_authority"), parent.get("operating_promotion"), parent.get("goal_achieve")]
    if any(value != "not_claimed" for value in forbidden):
        raise RuntimeError("HO parent(HO 상위 실행)에 금지된 authority claim(권위 주장)이 있습니다.")
    return parent


def terminal_processes() -> dict[str, Any]:
    command = [
        "powershell",
        "-NoProfile",
        "-Command",
        "Get-CimInstance Win32_Process -Filter \"name = 'terminal64.exe'\" | Select-Object ProcessId,ExecutablePath,CommandLine | ConvertTo-Json -Compress",
    ]
    proc = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, timeout=30)
    payload: Any = []
    if proc.stdout.strip():
        try:
            payload = json.loads(proc.stdout)
            if isinstance(payload, Mapping):
                payload = [payload]
        except json.JSONDecodeError:
            payload = proc.stdout.strip()
    return {
        "command": command,
        "returncode": proc.returncode,
        "stdout": proc.stdout[-2000:],
        "stderr": proc.stderr[-2000:],
        "processes": payload,
        "status": "no_terminal64_process" if not payload else "terminal64_process_present",
        "effect": "terminal64.exe process(터미널 프로세스) 충돌을 먼저 확인합니다. 효과는 기존 MT5 session(MT5 세션)을 덮어쓰지 않는 것입니다.",
    }


def write_work_packet() -> None:
    write_json(
        WORK_PACKET,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "primary_family": "runtime_backtest(런타임 백테스트)",
            "primary_skill": "obsidian-runtime-parity(런타임 동등성)",
            "support_skills": [
                "obsidian-backtest-forensics(백테스트 포렌식)",
                "obsidian-artifact-lineage(산출물 계보)",
                "obsidian-performance-attribution(성과 귀속)",
                "obsidian-result-judgment(결과 판정)",
            ],
            "required_gates": [
                "tester_execution_attempt_gate",
                "runtime_output_gate",
                "strategy_report_gate",
                "proxy_mt5_diff_gate",
                "runtime_parity_boundary_gate",
                "receipt_coverage_gate",
                "required_gate_coverage_audit",
                "final_claim_guard",
            ],
            "claim_boundary": CLAIM_BOUNDARY,
            "effect": "HP work packet(HP 작업 묶음)은 MT5 execution(MT5 실행), output collection(출력 수집), proxy diff(프록시 차이), judgment(판정)을 한 묶음으로 닫습니다.",
        },
    )


def enrich_attempts(parent: Mapping[str, Any]) -> list[dict[str, Any]]:
    source_rows = read_csv(pkg.RUNTIME_PROBE_ATTEMPT_PACKAGE).to_dict("records")
    enriched: list[dict[str, Any]] = []
    for row in source_rows:
        attempt = dict(row)
        ini_path = str(attempt.get("ini_path") or attempt.get("tester_ini") or "")
        set_path = str(attempt.get("set_path") or attempt.get("tester_set") or "")
        set_values = parse_set_values(ROOT / set_path)
        report_name = str(attempt.get("report_name") or parent.get("report_name") or "Project_Obsidian_Prime_v2_run364HP_single_source_probability_bin_veto_runtime_probe")
        attempt.update(
            {
                "source_package_run_id": attempt.get("run_id", PARENT_RUN_ID),
                "run_id": RUN_ID,
                "parent_run_id": PARENT_RUN_ID,
                "next_run_id": NEXT_RUN_ID,
                "tier": "Tier A single-source(Tier A 단일 원천)",
                "split": str(attempt.get("split") or "validation_oos"),
                "ini_path": ini_path,
                "set_path": set_path,
                "ini_name": Path(ini_path).name,
                "set_name": Path(set_path).name,
                "report_name": report_name,
                "model_id": MODEL_ID,
                "candidate_id": CANDIDATE_ID,
                "primary_model_id": MODEL_ID,
                "fallback_model_id": "",
                "common_telemetry_path": set_values.get("InpTelemetryCsvPath", ""),
                "common_summary_path": set_values.get("InpSummaryCsvPath", ""),
                "ini": {"tester": {"Report": report_name}},
                "set": {"path": set_path},
                "execution_run_id": RUN_ID,
                "effect": "HO package(HO 패키지)를 실제 MT5 runtime probe(MT5 런타임 탐침) 입력으로 고정합니다. 효과는 single-source(단일 원천) 패키지와 HP 실행 기록을 분리 추적하는 것입니다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        enriched.append(attempt)
    if not enriched:
        raise RuntimeError("runtime_probe_attempt_package(런타임 탐침 시도 패키지)가 비어 있습니다.")
    write_csv(RUNTIME_PROBE_ATTEMPT_PACKAGE, enriched)
    return enriched


def copy_runtime_outputs(common_files_root: Path, attempts: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for attempt in attempts:
        attempt_name = str(attempt["attempt_name"])
        for key, suffix in [("common_telemetry_path", "telemetry"), ("common_summary_path", "summary")]:
            source = common_files_root / Path(str(attempt.get(key, "")))
            target = TELEMETRY_COPY_DIR / f"{attempt_name}_{suffix}.csv"
            source_exists = exists(source)
            copied = False
            if source_exists:
                io_path(target.parent).mkdir(parents=True, exist_ok=True)
                shutil.copy2(fs_path(source), fs_path(target))
                copied = True
            rows.append(
                {
                    "copy_id": f"{attempt_name}::{suffix}",
                    "attempt_name": attempt_name,
                    "source_path": source.as_posix(),
                    "target_path": rel(target),
                    "source_exists": source_exists,
                    "copied": copied,
                    "exists": exists(target),
                    "sha256": sha(target) if exists(target) else "",
                    "effect": "runtime telemetry(런타임 기록)를 HP run folder(HP 실행 폴더)에 고정합니다. 효과는 MT5 출력 근거를 다음 review(검토)에서 재사용할 수 있게 하는 것입니다.",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    write_csv(RUNTIME_OUTPUT_COPY, rows)
    return rows


def expected_oos_total(expected_rows: Sequence[Mapping[str, Any]]) -> Mapping[str, Any]:
    for row in expected_rows:
        if str(row.get("view", "")).startswith("split_total") and str(row.get("split")) == "oos":
            return row
    for row in expected_rows:
        if str(row.get("split")) == "oos":
            return row
    return expected_rows[0] if expected_rows else {}


def build_proxy_diff(expected_rows: Sequence[Mapping[str, Any]], summaries: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    expected = expected_oos_total(expected_rows)
    rows: list[dict[str, Any]] = []
    for summary in summaries:
        expected_net = float_or_nan(expected.get("net_profit"))
        actual_net = float_or_nan(summary.get("net_profit"))
        expected_trades = float_or_nan(expected.get("trade_count"))
        actual_trades = float_or_nan(summary.get("trade_count"))
        expected_pf = float_or_nan(expected.get("profit_factor"))
        actual_pf = float_or_nan(summary.get("profit_factor"))
        expected_expectancy = float_or_nan(expected.get("expectancy"))
        actual_expectancy = float_or_nan(summary.get("expectancy"))
        rows.append(
            {
                "attempt_name": summary.get("attempt_name", ""),
                "candidate_id": summary.get("candidate_id", ""),
                "model_id": summary.get("model_id", ""),
                "expected_source_view": expected.get("view", ""),
                "expected_source_split": expected.get("split", ""),
                "expected_net_profit": finite(expected_net),
                "actual_mt5_net_profit": finite(actual_net),
                "net_profit_diff_actual_minus_expected": finite(actual_net - expected_net) if math.isfinite(expected_net) and math.isfinite(actual_net) else "",
                "expected_profit_factor": finite(expected_pf),
                "actual_mt5_profit_factor": finite(actual_pf),
                "profit_factor_diff_actual_minus_expected": finite(actual_pf - expected_pf) if math.isfinite(expected_pf) and math.isfinite(actual_pf) else "",
                "expected_trade_count": finite(expected_trades, 0),
                "actual_mt5_trade_count": finite(actual_trades, 0),
                "trade_count_diff_actual_minus_expected": finite(actual_trades - expected_trades, 0) if math.isfinite(expected_trades) and math.isfinite(actual_trades) else "",
                "expected_trade_density": expected.get("trade_density", ""),
                "scaled_density_estimate_from_hl_ratio": read_json(pkg.FINAL_DECISION).get("expected_runtime_density_estimate_from_hl_ratio", ""),
                "expected_expectancy": finite(expected_expectancy),
                "actual_mt5_expectancy": finite(actual_expectancy),
                "expectancy_diff_actual_minus_expected": finite(actual_expectancy - expected_expectancy) if math.isfinite(expected_expectancy) and math.isfinite(actual_expectancy) else "",
                "actual_long_trade_count": summary.get("long_trade_count", ""),
                "actual_short_trade_count": summary.get("short_trade_count", ""),
                "actual_drawdown": summary.get("max_drawdown_amount", ""),
                "actual_recovery_factor": summary.get("recovery_factor", ""),
                "runtime_status": summary.get("runtime_status", ""),
                "report_status": summary.get("report_status", ""),
                "comparison_status": summary.get("comparison_status", ""),
                "diff_boundary": "proxy expected value(프록시 예상값)는 MT5 KPI(MT5 핵심 성과 지표)를 대체하지 않습니다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(PROXY_MT5_DIFF, rows)
    return rows


def density_boundary(parent: Mapping[str, Any]) -> str:
    direct_density = float_or_nan(parent.get("expected_oos_trade_density"))
    scaled_density = float_or_nan(parent.get("expected_runtime_density_estimate_from_hl_ratio"))
    if math.isfinite(direct_density) and direct_density < 3 and math.isfinite(scaled_density) and scaled_density >= 3:
        return "direct_proxy_below_goal_scaled_estimate_requires_mt5_measurement(직접 프록시 미달, 스케일 추정 MT5 측정 필요)"
    if math.isfinite(direct_density) and direct_density < 3:
        return "direct_proxy_below_goal_not_operating_candidate(직접 프록시 목표 미달, 운영 후보 아님)"
    return "direct_proxy_density_meets_minimum_proxy_only(직접 프록시 밀도 최소 통과, 프록시 전용)"


def build_final(
    args: argparse.Namespace,
    parent: Mapping[str, Any],
    attempts: Sequence[Mapping[str, Any]],
    execution_results: Sequence[Mapping[str, Any]],
    report_records: Sequence[Mapping[str, Any]],
    summaries: Sequence[Mapping[str, Any]],
    proxy_rows: Sequence[Mapping[str, Any]],
    copy_rows: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    outputs_available = hk.output_available_count(summaries)
    runtime_completed = sum(1 for row in summaries if row.get("runtime_status") == "completed")
    usable_reports = hk.usable_report_count(report_records)
    status = STATUS_COMPLETED if outputs_available else STATUS_BLOCKED
    judgment = JUDGMENT_COMPLETED if outputs_available else JUDGMENT_BLOCKED
    decision = DECISION_COMPLETED if outputs_available else DECISION_BLOCKED
    summary = summaries[0] if summaries else {}
    proxy_row = proxy_rows[0] if proxy_rows else {}
    first_execution = execution_results[0] if execution_results else {}
    return {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "stage_id": STAGE_ID,
        "status": status,
        "judgment": judgment,
        "decision": decision,
        "created_at_utc": now_utc(),
        "claim_boundary": CLAIM_BOUNDARY,
        "candidate_id": summary.get("candidate_id", CANDIDATE_ID),
        "model_id": parent.get("model_id", MODEL_ID),
        "attempt_count": len(attempts),
        "runtime_completed_rows": runtime_completed,
        "usable_report_rows": usable_reports,
        "outputs_available_rows": outputs_available,
        "runtime_output_copy_rows": len(copy_rows),
        "terminal_path": str(args.terminal_path),
        "common_files_root": str(args.common_files_root),
        "tester_profile_root": str(args.tester_profile_root),
        "terminal_data_root": str(args.terminal_data_root),
        "tester_first_status": summary.get("tester_status", first_execution.get("status", "")),
        "tester_first_blocker": summary.get("blocker", first_execution.get("blocker", "")),
        "expected_net_profit": proxy_row.get("expected_net_profit", parent.get("expected_oos_net", "")),
        "actual_mt5_net_profit": proxy_row.get("actual_mt5_net_profit", summary.get("net_profit", "")),
        "net_profit_diff_actual_minus_expected": proxy_row.get("net_profit_diff_actual_minus_expected", ""),
        "expected_trade_count": proxy_row.get("expected_trade_count", parent.get("expected_oos_trade_count", "")),
        "actual_mt5_trade_count": proxy_row.get("actual_mt5_trade_count", summary.get("trade_count", "")),
        "trade_count_diff_actual_minus_expected": proxy_row.get("trade_count_diff_actual_minus_expected", ""),
        "expected_profit_factor": proxy_row.get("expected_profit_factor", parent.get("expected_oos_profit_factor", "")),
        "actual_mt5_profit_factor": proxy_row.get("actual_mt5_profit_factor", summary.get("profit_factor", "")),
        "expected_expectancy": proxy_row.get("expected_expectancy", parent.get("expected_oos_expectancy", "")),
        "actual_mt5_expectancy": proxy_row.get("actual_mt5_expectancy", summary.get("expectancy", "")),
        "expectancy_diff_actual_minus_expected": proxy_row.get("expectancy_diff_actual_minus_expected", ""),
        "actual_long_trade_count": proxy_row.get("actual_long_trade_count", summary.get("long_trade_count", "")),
        "actual_short_trade_count": proxy_row.get("actual_short_trade_count", summary.get("short_trade_count", "")),
        "actual_drawdown": proxy_row.get("actual_drawdown", summary.get("max_drawdown_amount", "")),
        "actual_recovery_factor": proxy_row.get("actual_recovery_factor", summary.get("recovery_factor", "")),
        "report_path": summary.get("report_path", ""),
        "comparison_status": summary.get("comparison_status", ""),
        "mt5_execution": "attempted(시도)",
        "external_verification_status": "mt5_runtime_probe_attempted_outputs_available(런타임 탐침 시도, 출력 있음)" if outputs_available else "mt5_runtime_probe_attempted_outputs_missing_or_blocked(런타임 탐침 시도, 출력 누락 또는 차단)",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "live_readiness": "not_claimed",
        "expected_oos_trade_density": parent.get("expected_oos_trade_density", ""),
        "expected_runtime_density_estimate_from_hl_ratio": parent.get("expected_runtime_density_estimate_from_hl_ratio", ""),
        "goal_density_boundary": density_boundary(parent),
        "report_file": rel(REPORT_PATH),
        "final_decision": rel(FINAL_DECISION),
    }


def gate_rows(final: Mapping[str, Any], *, receipts_written: bool) -> list[dict[str, Any]]:
    runtime_ok = int(final.get("runtime_completed_rows") or 0) > 0
    report_ok = int(final.get("usable_report_rows") or 0) > 0
    outputs_available = int(final.get("outputs_available_rows") or 0) > 0
    receipt_paths = [BACKTEST_RECEIPT, RUNTIME_RECEIPT, PERFORMANCE_RECEIPT, JUDGMENT_RECEIPT, LINEAGE_RECEIPT, CLAIM_RECEIPT]
    gates = [
        ("tester_execution_attempt_gate", exists(MT5_EXECUTION_RESULT), MT5_EXECUTION_RESULT, "MT5 Strategy Tester(MT5 전략 테스터) 실행 시도 또는 차단 사유를 기록합니다."),
        ("runtime_output_gate", runtime_ok, RUNTIME_OUTPUT_COPY, "runtime telemetry(런타임 기록)와 summary(요약)를 확인합니다."),
        ("strategy_report_gate", report_ok, STRATEGY_TESTER_REPORTS, "Strategy Tester report(전략 테스터 보고서)에서 KPI(핵심 성과 지표)를 파싱합니다."),
        ("proxy_mt5_diff_gate", outputs_available, PROXY_MT5_DIFF, "proxy expected value(프록시 예상값)와 MT5 KPI(MT5 핵심 성과 지표)를 분리합니다."),
        ("runtime_parity_boundary_gate", True, RUNTIME_RECEIPT, "runtime probe(런타임 탐침)를 runtime authority(런타임 권위)로 승격하지 않습니다."),
        ("receipt_coverage_gate", receipts_written and all(exists(path) for path in receipt_paths), RUNTIME_RECEIPT, "필수 receipt(영수증)를 덮었습니다."),
        ("required_gate_coverage_audit", exists(GATE_AUDIT), GATE_AUDIT, "필수 gate(게이트)를 closeout(종료 기록)에 연결합니다."),
        ("final_claim_guard", exists(CLAIM_RECEIPT), CLAIM_RECEIPT, "Goal Achieve(목표 달성), operating promotion(운영 승격), runtime authority(런타임 권위)를 모두 막습니다."),
    ]
    return [
        {
            "run_id": RUN_ID,
            "gate": gate,
            "status": "passed" if passed else "blocked",
            "evidence": rel(evidence),
            "effect": effect,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for gate, passed, evidence, effect in gates
    ]


def write_receipts(final: Mapping[str, Any]) -> None:
    base = {"run_id": RUN_ID, "stage_id": STAGE_ID, "created_at_utc": final["created_at_utc"], "claim_boundary": CLAIM_BOUNDARY}
    write_json(
        BACKTEST_RECEIPT,
        {
            **base,
            "tester_identity": rel(pkg.TESTER_IDENTITY_CONTRACT),
            "ea_identity": {
                "ea_entrypoint": "foundation/mt5/ObsidianPrimeV2_RuntimeProbeEA.mq5",
                "module_hashes": read_json(pkg.FINAL_DECISION).get("runtime_module_hashes", []),
                "set_manifest": rel(pkg.TESTER_SET_MANIFEST),
                "ini_manifest": rel(pkg.TESTER_INI_MANIFEST),
                "model_hash": read_json(pkg.FINAL_DECISION).get("mt5_onnx_sha256", ""),
            },
            "report_identity": rel(STRATEGY_TESTER_REPORTS),
            "trade_evidence": rel(EXECUTION_SUMMARY),
            "cost_assumptions": "tester identity contract(테스터 정체성 계약) 기준이며 report review(보고서 검토)에서 비용 차이를 다시 확인해야 합니다.",
            "forensic_checks": [rel(MT5_EXECUTION_RESULT), rel(STRATEGY_TESTER_REPORTS), rel(RUNTIME_OUTPUT_COPY), rel(PROXY_MT5_DIFF)],
            "backtest_judgment": "usable_with_boundary(경계 포함 사용 가능)" if int(final.get("usable_report_rows") or 0) else "blocked_or_inconclusive(차단 또는 불충분)",
        },
    )
    write_json(
        RUNTIME_RECEIPT,
        {
            **base,
            "research_path": rel(pkg.RUNTIME_POLICY_CONFIG),
            "runtime_path": [rel(pkg.RUNTIME_PROBE_ATTEMPT_PACKAGE), rel(pkg.TESTER_SET_MANIFEST), rel(pkg.TESTER_INI_MANIFEST)],
            "shared_contract": rel(pkg.RUNTIME_PARITY_CONTRACT),
            "known_differences": "single-source route(단일 원천 라우트)라 Tier B fallback(Tier B 대체)은 disabled(비활성)입니다.",
            "parity_check": [rel(EXECUTION_SUMMARY), rel(PROXY_MT5_DIFF)],
            "parity_identity": rel(RUNTIME_IDENTITY),
            "runtime_claim_boundary": "runtime_probe(런타임 탐침), not authority(권위 아님)",
        },
    )
    write_json(
        PERFORMANCE_RECEIPT,
        {
            **base,
            "expected_vs_actual": rel(PROXY_MT5_DIFF),
            "attribution_scope": "proxy-vs-MT5 first pass(프록시 대 MT5 1차 비교)",
            "judgment": final["judgment"],
            "goal_density_boundary": final["goal_density_boundary"],
        },
    )
    write_json(
        JUDGMENT_RECEIPT,
        {
            **base,
            "result_subject": RUN_ID,
            "evidence_available": [rel(EXECUTION_SUMMARY), rel(PROXY_MT5_DIFF), rel(STRATEGY_TESTER_REPORTS), rel(RUNTIME_OUTPUT_COPY)],
            "evidence_missing": ["forward/replay evidence(전진/재생 근거)", "runtime authority closure(런타임 권위 종료)", "reviewed HQ judgment(HQ 검토 판정)"],
            "judgment_label": final["judgment"],
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": NEXT_RUN_ID,
            "user_explanation_hook": "HP checks whether HO package survives MT5, not whether it is live-ready(HP는 HO 패키지가 MT5에서 버티는지 확인하며 실거래 준비 선언이 아님).",
        },
    )
    write_json(
        LINEAGE_RECEIPT,
        {
            **base,
            "source_inputs": [{"path": rel(path), "sha256": sha(path)} for path in INPUT_FILES if exists(path)],
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [rel(path) for path in OUTPUT_FILES if exists(path)],
            "artifact_hashes": {rel(path): sha(path) for path in OUTPUT_FILES if exists(path) and io_path(path).is_file()},
            "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "lineage_judgment": "connected_with_runtime_probe_boundary(런타임 탐침 경계 포함 연결)",
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            **base,
            "mt5_execution": "attempted(시도)",
            "runtime_authority": "not_claimed",
            "operating_promotion": "not_claimed",
            "live_readiness": "not_claimed",
            "goal_achieve": "not_claimed",
            "effect": "MT5 runtime probe(MT5 런타임 탐침)를 operating claim(운영 주장)으로 승격하지 않습니다.",
        },
    )
    write_csv(
        RUNTIME_IDENTITY,
        [
            {
                "run_id": RUN_ID,
                "parent_run_id": PARENT_RUN_ID,
                "attempt_count": final["attempt_count"],
                "terminal_path": final["terminal_path"],
                "candidate_id": final.get("candidate_id", ""),
                "model_id": final.get("model_id", ""),
                "source_package": rel(pkg.FINAL_DECISION),
                "runtime_module_hash_count": len(read_json(pkg.FINAL_DECISION).get("runtime_module_hashes", [])),
                "set_manifest": rel(pkg.TESTER_SET_MANIFEST),
                "ini_manifest": rel(pkg.TESTER_INI_MANIFEST),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )


def markdown_table(rows: Sequence[Mapping[str, Any]], columns: Sequence[str], limit: int = 12) -> str:
    if not rows:
        return "_none(없음)_"
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join(["---"] * len(columns)) + " |"]
    for row in rows[:limit]:
        lines.append("| " + " | ".join(str(row.get(col, "")).replace("|", "\\|").replace("\n", " ") for col in columns) + " |")
    return "\n".join(lines)


def write_docs(final: Mapping[str, Any], summaries: Sequence[Mapping[str, Any]], proxy_rows: Sequence[Mapping[str, Any]], gates: Sequence[Mapping[str, Any]]) -> None:
    report = f"""# run364HP Single-Source Probability-Bin Veto MT5 Runtime Probe(단일 원천 확률 구간 거부 MT5 런타임 탐침)

Updated(갱신): {final['created_at_utc']}

## Current Truth(현재 진실)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(상위 실행 ID): `{PARENT_RUN_ID}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- model(모델): `{final['model_id']}`
- judgment(판정): `{final['judgment']}`
- mt5_execution(MT5 실행): `{final['mt5_execution']}`
- tester_first_status(첫 테스터 상태): `{final['tester_first_status']}`
- tester_first_blocker(첫 테스터 차단): `{final['tester_first_blocker']}`
- runtime_authority(런타임 권위): `not_claimed(주장 안 함)`

## Action/Effect(행동/효과)

Action(행동): HO single-source package(HO 단일 원천 패키지)의 FJ ONNX(FJ 온엑스), feature CSV(피처 CSV), probability-bin veto(확률 구간 거부), set/ini(설정/초기화 파일)를 MT5 Strategy Tester(MT5 전략 테스터)로 실행 시도했습니다.

Effect(효과): proxy expected value(프록시 예상값)와 MT5 output(MT5 출력)을 분리해 `{NEXT_RUN_ID}`에서 diff(차이), attribution(귀속), usability(활용 가능성)를 검토할 수 있습니다.

## Execution Summary(실행 요약)

{markdown_table(summaries, ['attempt_name', 'tester_status', 'runtime_status', 'report_status', 'net_profit', 'profit_factor', 'trade_count', 'long_trade_count', 'short_trade_count', 'blocker', 'comparison_status'])}

## Proxy vs MT5(프록시 대 MT5)

{markdown_table(proxy_rows, ['attempt_name', 'expected_net_profit', 'actual_mt5_net_profit', 'net_profit_diff_actual_minus_expected', 'expected_trade_count', 'actual_mt5_trade_count', 'trade_count_diff_actual_minus_expected', 'expected_profit_factor', 'actual_mt5_profit_factor', 'comparison_status'])}

## Gates(게이트)

{markdown_table(gates, ['gate', 'status', 'evidence', 'effect'])}

## Boundary(경계)

This run(이번 실행)은 runtime probe attempt(런타임 탐침 시도)입니다. forward pass(전진 통과), live readiness(실거래 준비), operating promotion(운영 승격), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 모두 `not_claimed(주장 안 함)`입니다.
"""
    write_text(REPORT_PATH, report, bom=True)
    write_text(
        DECISION_DOC,
        f"""# Stage364HP decision(결정): single-source probability-bin veto MT5 runtime probe(단일 원천 확률 구간 거부 MT5 런타임 탐침)

- date(날짜): {TODAY}
- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{final['decision']}`
- judgment(판정): `{final['judgment']}`
- runtime_completed_rows(런타임 완료 행): `{final['runtime_completed_rows']}`
- usable_report_rows(사용 가능 보고서 행): `{final['usable_report_rows']}`
- actual MT5 net/PF/trades(실제 MT5 순수익/수익 팩터/거래수): `{final['actual_mt5_net_profit']}` / `{final['actual_mt5_profit_factor']}` / `{final['actual_mt5_trade_count']}`
- expected proxy net/PF/trades(예상 프록시 순수익/수익 팩터/거래수): `{final['expected_net_profit']}` / `{final['expected_profit_factor']}` / `{final['expected_trade_count']}`
- density boundary(밀도 경계): `{final['goal_density_boundary']}`
- next action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): HQ에서 proxy/MT5 diff(프록시 대 MT5 차이)를 검토하거나, 출력이 없으면 repair plan(수정 계획)을 세웁니다.
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
        bom=True,
    )
    append_text_once(REVIEW_INDEX, f"run364HP__{RUN_ID}", f"\n- run364HP__{RUN_ID}: [{REPORT_PATH.name}]({REPORT_PATH.name}) - single-source probability-bin veto MT5 runtime probe(단일 원천 확률 구간 거부 MT5 런타임 탐침), next `{NEXT_RUN_ID}`.\n")
    append_text_once(STAGE_BRIEF, f"run364HP__{RUN_ID}", f"\n<!-- run364HP__{RUN_ID} -->\n\n## run364HP Single-Source MT5 Runtime Probe(단일 원천 MT5 런타임 탐침)\n\nAction(행동): HO single-source probability-bin veto package(HO 단일 원천 확률 구간 거부 패키지)를 Strategy Tester(전략 테스터)로 실행 시도했습니다.\n\nEffect(효과): `{NEXT_RUN_ID}`에서 proxy/MT5 diff(프록시 대 MT5 차이) 또는 blocker(차단 원인)를 검토할 수 있습니다.\n")
    append_text_once(STAGE_README, f"run364HP__{RUN_ID}", f"\n<!-- run364HP__{RUN_ID} -->\n## run364HP MT5 runtime probe(MT5 런타임 탐침)\n\nSingle-source probability-bin veto(단일 원천 확률 구간 거부) probe(탐침) attempted(시도). Next(다음): `{NEXT_RUN_ID}`.\n")
    replace_prefixed_lines(
        STAGE_BRIEF,
        {
            "- current_run_id": f"- current_run_id(현재 실행 ID): `{NEXT_RUN_ID}`",
            "- latest_completed_run_id": f"- latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`",
            "- selection_status": f"- selection_status(선택 상태): `{final['status']}`",
            "- claim_boundary": f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
        },
        bom=True,
    )
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

Current truth(현재 진실): `run364HP` attempted(시도) the HO single-source probability-bin veto MT5 runtime probe(HO 단일 원천 확률 구간 거부 MT5 런타임 탐침). runtime_completed_rows(런타임 완료 행)는 `{final['runtime_completed_rows']}`, usable_report_rows(사용 가능 보고서 행)는 `{final['usable_report_rows']}`, actual MT5 net/PF/trades(실제 MT5 순수익/수익 팩터/거래수)는 `{final['actual_mt5_net_profit']}` / `{final['actual_mt5_profit_factor']}` / `{final['actual_mt5_trade_count']}`입니다.

Density boundary(밀도 경계): `{final['goal_density_boundary']}`. Direct proxy density(직접 프록시 밀도)는 `{final['expected_oos_trade_density']}`이고 scaled density estimate(스케일 밀도 추정)는 `{final['expected_runtime_density_estimate_from_hl_ratio']}`입니다.

Next action(다음 행동): `{NEXT_RUN_ID}`에서 proxy/MT5 diff(프록시 대 MT5 차이), runtime output(런타임 출력), blocker(차단 원인)를 review(검토)합니다.

Operating boundary(운영 경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""",
        bom=True,
    )
    write_text(
        SELECTION_STATUS,
        f"""# Stage364 selection status(선택 상태)

Updated(갱신): {final['created_at_utc']}

Current run(현재 실행): `{NEXT_RUN_ID}`
Latest completed run(최근 완료 실행): `{RUN_ID}`

Latest MT5 runtime probe(최근 MT5 런타임 탐침): `{RUN_ID}`.

Model(모델): `{final['model_id']}`

Actual MT5 net/PF/trades(실제 MT5 순수익/수익 팩터/거래수): `{final['actual_mt5_net_profit']}` / `{final['actual_mt5_profit_factor']}` / `{final['actual_mt5_trade_count']}`.

Expected proxy net/PF/density/trades(예상 프록시 순수익/수익 팩터/밀도/거래수): `{final['expected_net_profit']}` / `{final['expected_profit_factor']}` / `{final['expected_oos_trade_density']}` / `{final['expected_trade_count']}`.

Density boundary(밀도 경계): `{final['goal_density_boundary']}`.

Authority(권위): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""",
        bom=True,
    )
    append_text_once(WORKSPACE_CHANGELOG, f"run364HP__{RUN_ID}", f"\n<!-- run364HP__{RUN_ID} -->\n- {final['created_at_utc']} `{RUN_ID}` attempted single-source probability-bin veto MT5 runtime probe(단일 원천 확률 구간 거부 MT5 런타임 탐침 시도); judgment(판정) `{final['judgment']}`; no authority claim(권위 주장 없음).\n")
    append_text_once(IDEA_REGISTRY, f"run364HP__{RUN_ID}", f"\n<!-- run364HP__{RUN_ID} -->\n- `{RUN_ID}`: FJ single-source probability-bin veto(FJ 단일 원천 확률 구간 거부)를 MT5 runtime probe(MT5 런타임 탐침)로 실행 시도했습니다. Effect(효과): proxy clue(프록시 단서)를 MT5 KPI(MT5 핵심 성과 지표)와 비교할 입력을 만들었습니다.\n")
    append_text_once(NEGATIVE_REGISTER, f"run364HP__no_authority__{RUN_ID}", f"\n<!-- run364HP__no_authority__{RUN_ID} -->\n- `{RUN_ID}`: MT5 runtime probe(MT5 런타임 탐침)는 authority(권위) 없음. Effect(효과): 운영 주장 대신 HQ review(HQ 검토)로 넘깁니다.\n")


def write_ledgers(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    common = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "run_number": RUN_NUMBER,
        "date": TODAY,
        "status": final["status"],
        "judgment": final["judgment"],
        "decision": final["decision"],
        "next_run_id": NEXT_RUN_ID,
        "rows": final["outputs_available_rows"],
        "gate_passes": sum(1 for row in gates if row["status"] == "passed"),
        "gate_total": len(gates),
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "final_decision_path": rel(FINAL_DECISION),
        "gate_audit_path": rel(GATE_AUDIT),
        "created_at": final["created_at_utc"],
        "created_at_utc": final["created_at_utc"],
        "work_family": "runtime_backtest(런타임 백테스트)",
        "scoreboard_lane": "runtime_probe(런타임 탐침)",
        "external_verification_status": final["external_verification_status"],
        "evidence_boundary": "mt5_runtime_probe_no_authority(MT5 런타임 탐침, 권위 없음)",
        "question": "Does the FJ single-source probability-bin veto package survive MT5 runtime probing?(FJ 단일 원천 확률 구간 거부 패키지가 MT5 런타임 탐침에서 버티는가?)",
        "next_action": NEXT_RUN_ID,
        "net_profit": final["actual_mt5_net_profit"],
        "profit_factor": final["actual_mt5_profit_factor"],
        "expectancy": final["actual_mt5_expectancy"],
        "trade_count": final["actual_mt5_trade_count"],
        "long_trade_count": final["actual_long_trade_count"],
        "short_trade_count": final["actual_short_trade_count"],
        "max_drawdown_amount": final["actual_drawdown"],
        "recovery_factor": final["actual_recovery_factor"],
        "expected_net_profit": final["expected_net_profit"],
        "expected_profit_factor": final["expected_profit_factor"],
        "expected_trade_count": final["expected_trade_count"],
        "expected_trade_density": final["expected_oos_trade_density"],
        "scaled_density_estimate": final["expected_runtime_density_estimate_from_hl_ratio"],
        "result_judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "primary_artifact": rel(EXECUTION_SUMMARY),
        "candidate_model_id": final["model_id"],
    }
    ledger_rows = []
    for suffix, record_view, tier_scope, row_status in [
        ("tier_a_used", "Tier A used(Tier A 사용)", "Tier A", final["status"]),
        ("tier_b_fallback_used", "Tier B fallback used(Tier B 대체 사용)", "Tier B", "missing_required(필수 누락)"),
        ("actual_routed_total", "actual routed total(실제 라우팅 전체)", "Tier A+B", final["status"]),
    ]:
        row = {
            **common,
            "ledger_row_id": f"{RUN_ID}__{suffix}",
            "subrun_id": f"{RUN_ID}__{suffix}",
            "row_id": f"{RUN_ID}__{suffix}",
            "record_view": record_view,
            "tier_scope": tier_scope,
            "status": row_status,
            "view": record_view,
            "tier": tier_scope,
            "kpi_scope": "HP MT5 runtime probe(HP MT5 런타임 탐침)",
            "metric_scope": "mt5_runtime_probe(MT5 런타임 탐침)",
            "route_attribution_boundary": "single_source_tier_b_missing_required(단일 원천이라 Tier B 필수 누락)",
        }
        if suffix == "tier_b_fallback_used":
            for key in ["net_profit", "profit_factor", "expectancy", "trade_count", "long_trade_count", "short_trade_count", "max_drawdown_amount", "recovery_factor"]:
                row[key] = ""
        ledger_rows.append(row)
    append_or_replace_csv(STAGE_LEDGER, ["ledger_row_id"], ledger_rows, extend_header=True)
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], ledger_rows, extend_header=True)
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], [{**common, "lane": "runtime_probe(런타임 탐침)", "primary_report": rel(REPORT_PATH)}], extend_header=True)
    artifact_rows = []
    for path in OUTPUT_FILES:
        if exists(path) and io_path(path).is_file():
            artifact_rows.append(
                {
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "artifact_type": "script" if path == Path(__file__) else ("report" if path.suffix.lower() == ".md" else ("json" if path.suffix.lower() == ".json" else "csv")),
                    "path": rel(path),
                    "artifact_path": rel(path),
                    "sha256": sha(path),
                    "created_at": final["created_at_utc"],
                    "created_at_utc": final["created_at_utc"],
                    "claim_boundary": CLAIM_BOUNDARY,
                    "artifact_id": f"{RUN_ID}__{path.stem}",
                    "notes": "HP single-source probability-bin veto MT5 runtime probe artifact(HP 단일 원천 확률 구간 거부 MT5 런타임 탐침 산출물)",
                }
            )
    append_or_replace_csv(ARTIFACT_REGISTRY, ["artifact_id"], artifact_rows, extend_header=True)
    repair_run_registry_line_endings(RUN_ID)


def install_hk_runtime_globals() -> None:
    overrides = {
        "pkg": pkg,
        "TODAY": TODAY,
        "STAGE_ID": STAGE_ID,
        "RUN_NUMBER": RUN_NUMBER,
        "RUN_ID": RUN_ID,
        "PARENT_RUN_ID": PARENT_RUN_ID,
        "NEXT_RUN_ID": NEXT_RUN_ID,
        "STATUS_COMPLETED": STATUS_COMPLETED,
        "STATUS_BLOCKED": STATUS_BLOCKED,
        "JUDGMENT_COMPLETED": JUDGMENT_COMPLETED,
        "JUDGMENT_BLOCKED": JUDGMENT_BLOCKED,
        "DECISION_COMPLETED": DECISION_COMPLETED,
        "DECISION_BLOCKED": DECISION_BLOCKED,
        "CLAIM_BOUNDARY": CLAIM_BOUNDARY,
        "STAGE_DIR": STAGE_DIR,
        "RUN_DIR": RUN_DIR,
        "MT5_DIR": MT5_DIR,
        "TELEMETRY_COPY_DIR": TELEMETRY_COPY_DIR,
        "REPORT_COPY_DIR": REPORT_COPY_DIR,
        "REVIEW_DIR": REVIEW_DIR,
        "SPEC_DIR": SPEC_DIR,
        "SELECTED_DIR": SELECTED_DIR,
        "RUNTIME_PROBE_ATTEMPT_PACKAGE": RUNTIME_PROBE_ATTEMPT_PACKAGE,
        "TERMINAL_PROCESS_AUDIT": TERMINAL_PROCESS_AUDIT,
        "MT5_EXECUTION_RESULT": MT5_EXECUTION_RESULT,
        "STRATEGY_TESTER_REPORTS": STRATEGY_TESTER_REPORTS,
        "EXECUTION_SUMMARY": EXECUTION_SUMMARY,
        "PROXY_MT5_DIFF": PROXY_MT5_DIFF,
        "RUNTIME_OUTPUT_COPY": RUNTIME_OUTPUT_COPY,
        "RUNTIME_IDENTITY": RUNTIME_IDENTITY,
        "EXPECTED_KPI_SUMMARY": EXPECTED_KPI_SUMMARY,
        "WORK_PACKET": WORK_PACKET,
        "BACKTEST_RECEIPT": BACKTEST_RECEIPT,
        "RUNTIME_RECEIPT": RUNTIME_RECEIPT,
        "PERFORMANCE_RECEIPT": PERFORMANCE_RECEIPT,
        "JUDGMENT_RECEIPT": JUDGMENT_RECEIPT,
        "LINEAGE_RECEIPT": LINEAGE_RECEIPT,
        "CLAIM_RECEIPT": CLAIM_RECEIPT,
        "GATE_AUDIT": GATE_AUDIT,
        "FINAL_DECISION": FINAL_DECISION,
        "RUN_MANIFEST": RUN_MANIFEST,
        "REPORT_PATH": REPORT_PATH,
        "DECISION_DOC": DECISION_DOC,
        "REVIEW_INDEX": REVIEW_INDEX,
        "STAGE_LEDGER": STAGE_LEDGER,
        "STAGE_BRIEF": STAGE_BRIEF,
        "SELECTION_STATUS": SELECTION_STATUS,
        "STAGE_README": STAGE_README,
        "WORKSPACE_STATE": WORKSPACE_STATE,
        "CURRENT_WORKING_STATE": CURRENT_WORKING_STATE,
        "WORKSPACE_CHANGELOG": WORKSPACE_CHANGELOG,
        "RUN_REGISTRY": RUN_REGISTRY,
        "PROJECT_LEDGER": PROJECT_LEDGER,
        "ARTIFACT_REGISTRY": ARTIFACT_REGISTRY,
        "IDEA_REGISTRY": IDEA_REGISTRY,
        "NEGATIVE_REGISTER": NEGATIVE_REGISTER,
        "INPUT_FILES": INPUT_FILES,
        "OUTPUT_FILES": OUTPUT_FILES,
    }
    for key, value in overrides.items():
        setattr(hk, key, value)
    hk.parse_args = parse_args
    hk.validate_parent = validate_parent
    hk.terminal_processes = terminal_processes
    hk.write_work_packet = write_work_packet
    hk.enrich_attempts = enrich_attempts
    hk.copy_runtime_outputs = copy_runtime_outputs
    hk.build_proxy_diff = build_proxy_diff
    hk.build_final = build_final
    hk.gate_rows = gate_rows
    hk.write_receipts = write_receipts
    hk.markdown_table = markdown_table
    hk.write_docs = write_docs
    hk.write_ledgers = write_ledgers


def main() -> None:
    install_hk_runtime_globals()
    hk.main()


if __name__ == "__main__":
    main()
