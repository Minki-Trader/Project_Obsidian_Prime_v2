from __future__ import annotations

import json
import math
import os
import shutil
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, path_exists  # noqa: E402
from foundation.mt5.mql5_compile import compile_mql5_ea  # noqa: E402
from foundation.mt5.runtime_artifacts import mt5_runtime_module_hashes, sha256_file  # noqa: E402
from foundation.mt5.tester_files import TesterMaterializationConfig, materialize_tester_ini_file, materialize_tester_set_file  # noqa: E402
from stage_pipelines.stage364 import implement_h19_opposite_margin_runtime_guard_without_db as bj_runtime  # noqa: E402
from stage_pipelines.stage364 import prepare_density_lift_trade_shape_onnx_runtime_probe_without_db as runtime_base  # noqa: E402
from stage_pipelines.stage364 import review_late_year_short_share_stress_repair_scout_without_db as parent  # noqa: E402


TODAY = "2026-06-05"
STAGE_ID = parent.STAGE_ID
RUN_NUMBER = "run364BU"
RUN_ID = "run364BU_prepare_late_year_session_gate_mt5_precheck_without_db_v1"
PARENT_RUN_ID = parent.RUN_ID
SOURCE_RUNTIME_PROBE_RUN_ID = parent.SOURCE_RUNTIME_PROBE_RUN_ID
BASELINE_RUN_ID = parent.BASELINE_RUN_ID
NEXT_RUN_ID = "run364BV_materialize_synthetic_short_source_runtime_repair_without_db_v1"

STATUS = "blocked_stage364BU_calendar_gate_support_compiled_exact_mt5_precheck_blocked_synthetic_short_source_open_bv_no_authority"
JUDGMENT = "inconclusive_runtime_precheck_calendar_gate_supported_but_exact_mt5_blocked_synthetic_short_source_no_authority"
DECISION = "stage364BU_open_run364BV_synthetic_short_source_runtime_repair"
CLAIM_BOUNDARY = (
    "research_development_runtime_precheck_and_blocker_recovery_only_no_exact_mt5_execution_"
    "no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

ATTEMPT_NAME = "run364BU_december_h21_long_calendar_block_precheck"
REPORT_NAME = "OPv2_run364BU_dec_h21_long_calendar_block_precheck"
EXPLORATION_LABEL = "stage364_LateYearSessionGate__CalendarBlockPrecheck"

STAGE_DIR = parent.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
MT5_DIR = RUN_DIR / "mt5"
SET_DIR = MT5_DIR / "sets"
INI_DIR = MT5_DIR / "inis"
COMPILE_DIR = MT5_DIR / "compile"
REVIEW_DIR = STAGE_DIR / "03_reviews"
SPEC_DIR = STAGE_DIR / "00_spec"
SELECTED_DIR = STAGE_DIR / "04_selected"

INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
RUNTIME_GATE_SUPPORT_AUDIT = RUN_DIR / "runtime_gate_support_audit.csv"
RUNTIME_RULE_HANDOFF = RUN_DIR / "runtime_rule_handoff.json"
TESTER_SET_MANIFEST = RUN_DIR / "tester_set_manifest.csv"
TESTER_INI_MANIFEST = RUN_DIR / "tester_ini_manifest.csv"
TESTER_IDENTITY_CONTRACT = RUN_DIR / "tester_identity_contract.csv"
MT5_COMPILE_RESULT = RUN_DIR / "mt5_compile_result.json"
COMPILE_LOG = COMPILE_DIR / "ObsidianPrimeV2_RuntimeProbeEA_compile.log"
PORTABLE_EA_SYNC = RUN_DIR / "portable_ea_sync.json"
EXTERNAL_VERIFICATION_ATTEMPT = RUN_DIR / "external_verification_attempt.json"
BLOCKER_RECOVERY_LOG = RUN_DIR / "blocker_recovery_log.csv"
PROXY_MT5_DIFF_HANDOFF = RUN_DIR / "proxy_mt5_diff_handoff.csv"
RUN364BV_QUEUE = RUN_DIR / "run364BV_runtime_repair_queue.csv"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
BACKTEST_RECEIPT = RUN_DIR / "backtest_forensics_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / "run364BU_late_year_session_gate_mt5_precheck.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364BU_late_year_session_gate_mt5_precheck.md"
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
NEGATIVE_RESULT_REGISTER = ROOT / "docs" / "registers" / "negative_result_register.md"
MT5_INPUT_CONTRACT = ROOT / "docs" / "contracts" / "mt5_ea_input_order_contract_fpmarkets_v2.md"

SOURCE_SELECTED_CANDIDATE = parent.parent.SELECTED_CANDIDATE
SOURCE_SELECTED_TRADE_TAPE = parent.parent.SELECTED_TRADE_TAPE
SOURCE_SYNTHETIC_SHORT_TAPE = parent.parent.SELECTED_SYNTHETIC_SHORT_TAPE
SOURCE_PARENT_SUPPRESSED_TRADES = parent.parent.SELECTED_PARENT_SUPPRESSED_TRADES
SOURCE_BQ_SELECTED_CANDIDATE = parent.parent.bq.SELECTED_CANDIDATE
SOURCE_BQ_PROXY_MT5_DIFF = parent.parent.bq.PROXY_MT5_DIFF_PLAN
SOURCE_BK_FINAL = ROOT / "stages" / STAGE_ID / "02_runs" / "run364BK" / "final_decision.json"
SOURCE_BJ_SET = ROOT / "stages" / STAGE_ID / "02_runs" / "run364BJ" / "mt5" / "sets" / "OPv2_run364BJ.set"
SOURCE_EA = runtime_base.EA_SOURCE
SOURCE_EA_BINARY = runtime_base.EA_BINARY
PORTABLE_EA_EX5 = runtime_base.PORTABLE_EA_EX5
DEFAULT_METAEDITOR = runtime_base.DEFAULT_PORTABLE_ROOT / "MetaEditor64.exe"
DEFAULT_TERMINAL = runtime_base.DEFAULT_TERMINAL
DEFAULT_COMMON_FILES = runtime_base.DEFAULT_COMMON_FILES
DEFAULT_TESTER_PROFILE_ROOT = runtime_base.DEFAULT_TESTER_PROFILE_ROOT

COMMON_ROOT = f"Project_Obsidian_Prime_v2/stage364/{RUN_NUMBER}_late_year_session_gate_precheck"
COMMON_TELEMETRY = f"{COMMON_ROOT}/telemetry/{ATTEMPT_NAME}_telemetry.csv"
COMMON_SUMMARY = f"{COMMON_ROOT}/telemetry/{ATTEMPT_NAME}_summary.csv"

INPUT_FILES = [
    parent.FINAL_DECISION,
    parent.GATE_AUDIT,
    parent.RUN364BU_QUEUE,
    parent.PACKAGE_PRECHECK_DECISION,
    parent.PROXY_MT5_DIFF_REVIEW,
    SOURCE_SELECTED_CANDIDATE,
    SOURCE_SELECTED_TRADE_TAPE,
    SOURCE_SYNTHETIC_SHORT_TAPE,
    SOURCE_PARENT_SUPPRESSED_TRADES,
    SOURCE_BQ_SELECTED_CANDIDATE,
    SOURCE_BQ_PROXY_MT5_DIFF,
    SOURCE_BK_FINAL,
    SOURCE_BJ_SET,
    SOURCE_EA,
    MT5_INPUT_CONTRACT,
]

OUTPUT_FILES = [
    INPUT_MANIFEST,
    WORK_PACKET,
    RUNTIME_GATE_SUPPORT_AUDIT,
    RUNTIME_RULE_HANDOFF,
    TESTER_SET_MANIFEST,
    TESTER_INI_MANIFEST,
    TESTER_IDENTITY_CONTRACT,
    MT5_COMPILE_RESULT,
    COMPILE_LOG,
    PORTABLE_EA_SYNC,
    EXTERNAL_VERIFICATION_ATTEMPT,
    BLOCKER_RECOVERY_LOG,
    PROXY_MT5_DIFF_HANDOFF,
    RUN364BV_QUEUE,
    DATA_RECEIPT,
    RUNTIME_RECEIPT,
    BACKTEST_RECEIPT,
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
    NEGATIVE_RESULT_REGISTER,
    SOURCE_EA,
    MT5_INPUT_CONTRACT,
    Path(__file__),
]


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    return parent.rel(path)


def exists(path: Path | str) -> bool:
    return path_exists(Path(path))


def sha(path: Path | str) -> str:
    candidate = Path(path)
    return sha256_file(candidate) if exists(candidate) and io_path(candidate).is_file() else ""


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: Any) -> None:
    parent.write_json(path, json_ready(payload))


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    parent.write_csv(path, rows, fieldnames)


def read_rows(path: Path) -> list[dict[str, str]]:
    return parent.read_rows(path)


def write_text(path: Path, text: str, *, bom: bool = True) -> None:
    parent.write_text(path, text, bom=bom)


def append_text_once(path: Path, marker: str, text: str) -> None:
    parent.append_text_once(path, marker, text)


def append_or_replace_csv(path: Path, key_fields: Sequence[str], rows: Sequence[Mapping[str, Any]], *, extend_header: bool = True) -> None:
    parent.append_or_replace_csv(path, key_fields, rows, extend_header=extend_header)


def json_ready(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): json_ready(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_ready(item) for item in value]
    if isinstance(value, Path):
        return rel(value)
    if isinstance(value, pd.Timestamp):
        return value.isoformat()
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


def as_int(value: Any, default: int = 0) -> int:
    try:
        if value in ("", None):
            return default
        return int(float(value))
    except (TypeError, ValueError):
        return default


def markdown_table(rows: Sequence[Mapping[str, Any]], columns: Sequence[str], limit: int = 12) -> str:
    if not rows:
        return "_none(없음)_"
    shown = list(rows)[:limit]
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join(["---"] * len(columns)) + " |"
    body = ["| " + " | ".join(str(row.get(col, "")) for col in columns) + " |" for row in shown]
    return "\n".join([header, sep, *body])


def ensure_dirs() -> None:
    for path in [RUN_DIR, SET_DIR, INI_DIR, COMPILE_DIR, REVIEW_DIR, SPEC_DIR, SELECTED_DIR, DECISION_DOC.parent]:
        io_path(path).mkdir(parents=True, exist_ok=True)


def validate_inputs() -> dict[str, Any]:
    missing = [rel(path) for path in INPUT_FILES if not exists(path)]
    if missing:
        raise FileNotFoundError("missing BU inputs(BU 입력 누락): " + ", ".join(missing))
    final = read_json(parent.FINAL_DECISION)
    if final.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"BT next_run_id mismatch(BT 다음 실행 불일치): {final.get('next_run_id')} != {RUN_ID}")
    if final.get("runtime_authority") != "not_claimed" or final.get("operating_promotion") != "not_claimed":
        raise RuntimeError("BT has forbidden authority claim(BT 금지 권위 주장 존재)")
    gates = read_rows(parent.GATE_AUDIT)
    if not gates or any(row.get("status") != "passed" for row in gates):
        raise RuntimeError("BT gate audit(BT 게이트 감사)가 모두 passed(통과)가 아니다.")
    return final


def input_manifest_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in INPUT_FILES:
        rows.append(
            {
                "run_id": RUN_ID,
                "input_path": rel(path),
                "exists": exists(path),
                "sha256": sha(path),
                "input_role": "BU runtime precheck source(BU 런타임 사전점검 원천)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def parse_set_file(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for raw_line in io_path(path).read_text(encoding="utf-8-sig").splitlines():
        line = raw_line.strip()
        if not line or line.startswith(";") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip()
    return values


def source_support_texts() -> tuple[str, str]:
    return (
        io_path(SOURCE_EA).read_text(encoding="utf-8-sig"),
        io_path(MT5_INPUT_CONTRACT).read_text(encoding="utf-8-sig"),
    )


def audit_runtime_gate_support() -> list[dict[str, Any]]:
    ea_text, contract_text = source_support_texts()
    checks = [
        ("calendar_block_enabled_input", "InpCalendarBlockEnabled", ea_text, "passed", "calendar block(달력 차단) 사용 여부가 EA 입력으로 존재한다."),
        ("calendar_block_side_input", "InpCalendarBlockSide", ea_text, "passed", "long/short(롱/숏) 방향을 `.set`에서 지정할 수 있다."),
        ("calendar_block_month_input", "InpCalendarBlockMonth", ea_text, "passed", "12월 같은 month(월) 조건을 런타임에서 지정할 수 있다."),
        ("calendar_block_hour_inputs", "InpCalendarBlockStartHour", ea_text, "passed", "21-22시 같은 half-open hour range(반개구간 시간 범위)를 지정할 수 있다."),
        ("calendar_block_reason", "calendar_block:month=", ea_text, "passed", "런타임 telemetry(기록)에 차단 이유가 남는다."),
        ("calendar_contract_documented", "Runtime calendar block", contract_text, "passed", "입력 계약(input contract, 입력 계약)에 새 의미가 기록됐다."),
        ("synthetic_short_source_insertion", "synthetic_short_source_runtime_replay", ea_text, "blocked", "BQ/BS synthetic short(합성 숏) 47개를 MT5 신호 원천으로 재현하는 런타임 기능은 없다."),
        ("exact_bs_proxy_semantic", "selected_bs_synthetic_short_tape", ea_text, "blocked", "BS proxy(프록시)는 synthetic short(합성 숏) 추가와 parent long(부모 롱) 억제를 함께 쓰므로 calendar block(달력 차단)만으로 exact MT5 precheck(정확 MT5 사전점검)가 아니다."),
    ]
    rows = []
    for check_id, token, source_text, expected_status, effect in checks:
        present = token in source_text
        status = "passed" if expected_status == "passed" and present else expected_status
        if expected_status == "passed" and not present:
            status = "failed"
        rows.append(
            {
                "run_id": RUN_ID,
                "check_id": check_id,
                "token": token,
                "present": present,
                "status": status,
                "effect": effect,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(RUNTIME_GATE_SUPPORT_AUDIT, rows)
    return rows


def materialize_calendar_gate_handoff(selected: Mapping[str, Any]) -> dict[str, Any]:
    set_values = parse_set_file(SOURCE_BJ_SET)
    set_values.update(
        {
            "InpRunId": f"{RUN_ID}_{ATTEMPT_NAME}",
            "InpExplorationLabel": EXPLORATION_LABEL,
            "InpSplitLabel": "validation_oos_december_h21_calendar_block_precheck",
            "InpCalendarBlockEnabled": True,
            "InpCalendarBlockSide": "long",
            "InpCalendarBlockMonth": 12,
            "InpCalendarBlockStartHour": 21,
            "InpCalendarBlockEndHour": 22,
            "InpTelemetryCsvPath": COMMON_TELEMETRY,
            "InpSummaryCsvPath": COMMON_SUMMARY,
        }
    )
    set_path = SET_DIR / "OPv2_run364BU_calendar_gate_precheck.set"
    ini_path = INI_DIR / "OPv2_run364BU_calendar_gate_precheck.ini"
    set_payload = materialize_tester_set_file(set_values, set_path, generated_by=rel(Path(__file__)))
    ini_payload = materialize_tester_ini_file(
        TesterMaterializationConfig(
            shutdown_terminal=1,
            from_date="2025.01.01",
            to_date="2026.04.14",
            report=REPORT_NAME,
        ),
        ini_path,
        set_file_path=Path(set_path.name),
    )
    write_csv(
        TESTER_SET_MANIFEST,
        [
            {
                "run_id": RUN_ID,
                "attempt_name": ATTEMPT_NAME,
                "set_path": rel(set_path),
                "set_sha256": set_payload["sha256"],
                "parameter_count": set_payload["parameter_count"],
                "calendar_block_enabled": True,
                "calendar_block_side": "long",
                "calendar_block_month": 12,
                "calendar_block_hours": "21-22",
                "exact_mt5_precheck_status": "blocked_synthetic_short_source_missing(합성 숏 원천 누락으로 차단)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )
    write_csv(
        TESTER_INI_MANIFEST,
        [
            {
                "run_id": RUN_ID,
                "attempt_name": ATTEMPT_NAME,
                "ini_path": rel(ini_path),
                "ini_sha256": ini_payload["sha256"],
                "terminal": DEFAULT_TERMINAL.as_posix(),
                "symbol": ini_payload["tester"].get("Symbol"),
                "period": ini_payload["tester"].get("Period"),
                "model": ini_payload["tester"].get("Model"),
                "deposit": ini_payload["tester"].get("Deposit"),
                "leverage": ini_payload["tester"].get("Leverage"),
                "from_date": ini_payload["tester"].get("FromDate"),
                "to_date": ini_payload["tester"].get("ToDate"),
                "report": ini_payload["tester"].get("Report"),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )
    write_csv(
        TESTER_IDENTITY_CONTRACT,
        [
            {
                "contract_id": "tester_identity_precheck_handoff",
                "run_id": RUN_ID,
                "attempt_name": ATTEMPT_NAME,
                "terminal": DEFAULT_TERMINAL.as_posix(),
                "common_files_root": DEFAULT_COMMON_FILES.as_posix(),
                "tester_profile_root": DEFAULT_TESTER_PROFILE_ROOT.as_posix(),
                "symbol": "US100",
                "timeframe": "M5",
                "tester_model": 4,
                "deposit": 500,
                "leverage": "1:100",
                "fixed_lot": 0.1,
                "spread_cost_policy": "broker_native_real_tick_cost(브로커 실제 틱 비용)",
                "commission_policy": "broker_native_no_extra_commission_assumption(추가 커미션 가정 없음)",
                "execution_status": "not_run_exact_semantic_gap(정확 의미 차이로 미실행)",
                "effect": "tester identity(테스터 정체성)는 고정하되 KPI(핵심 성과 지표)는 주장하지 않는다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )
    handoff = {
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "selected_candidate_id": selected.get("candidate_id"),
        "selected_candidate_path": rel(SOURCE_SELECTED_CANDIDATE),
        "runtime_rule_stack": {
            "base_runtime_probe": SOURCE_RUNTIME_PROBE_RUN_ID,
            "base_set": rel(SOURCE_BJ_SET),
            "calendar_block": {
                "enabled": True,
                "side": "long",
                "month": 12,
                "start_hour": 21,
                "end_hour": 22,
                "timestamp_safety": "uses target closed M5 bar server month/hour only(대상 닫힌 5분봉 서버 월/시간만 사용)",
            },
            "synthetic_short_source": {
                "required_by_proxy": True,
                "synthetic_short_count": selected.get("synthetic_added_short_count"),
                "runtime_status": "missing(누락)",
                "blocker": "BQ/BS proxy inserts synthetic fixed-hold short trades without a runtime signal-source package(BQ/BS 프록시는 런타임 신호 원천 패키지 없이 합성 고정 보유 숏 거래를 삽입한다.)",
            },
        },
        "tester_handoff": {
            "set_path": rel(set_path),
            "set_sha256": set_payload["sha256"],
            "ini_path": rel(ini_path),
            "ini_sha256": ini_payload["sha256"],
        },
        "exact_mt5_precheck": {
            "status": "blocked(차단)",
            "reason": "calendar gate can be expressed, but synthetic short source cannot be expressed in current EA runtime(달력 게이트는 표현 가능하지만 현재 EA 런타임은 합성 숏 원천을 표현하지 못한다.)",
        },
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(RUNTIME_RULE_HANDOFF, handoff)
    return handoff


def compile_and_sync() -> tuple[dict[str, Any], dict[str, Any]]:
    result = compile_mql5_ea(DEFAULT_METAEDITOR, SOURCE_EA, COMPILE_LOG)
    write_json(MT5_COMPILE_RESULT, result)
    sync_payload = {
        "run_id": RUN_ID,
        "source_ea_binary": rel(SOURCE_EA_BINARY),
        "portable_ea_binary": PORTABLE_EA_EX5.as_posix(),
        "compile_status": result.get("status"),
        "copied": False,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    if result.get("status") == "completed" and exists(SOURCE_EA_BINARY):
        os.makedirs(io_path(PORTABLE_EA_EX5.parent), exist_ok=True)
        shutil.copy2(io_path(SOURCE_EA_BINARY), io_path(PORTABLE_EA_EX5))
        sync_payload.update(
            {
                "copied": True,
                "source_sha256": sha(SOURCE_EA_BINARY),
                "portable_sha256": sha(PORTABLE_EA_EX5),
                "effect": "compiled EA binary(컴파일된 EA 바이너리)를 portable tester(포터블 테스터)에 동기화한다.",
            }
        )
    else:
        sync_payload.update(
            {
                "blocker": result.get("blocker", "compile_failed_or_binary_missing"),
                "effect": "compile failure(컴파일 실패)나 binary missing(바이너리 누락)을 외부 검증 상태에 기록한다.",
            }
        )
    write_json(PORTABLE_EA_SYNC, sync_payload)
    return result, sync_payload


def write_blocker_and_diff(selected: Mapping[str, Any], bq_selected: Mapping[str, Any], bk_final: Mapping[str, Any], compile_result: Mapping[str, Any]) -> None:
    recovery_rows = [
        {
            "run_id": RUN_ID,
            "blocker_id": "calendar_gate_missing_before_bu",
            "status": "repaired_if_compile_completed(컴파일 완료 시 수리됨)",
            "recovery_action": "added generic calendar block inputs to EA and contract(EA와 계약에 범용 달력 차단 입력 추가)",
            "command_or_evidence": rel(SOURCE_EA),
            "failure_log": "" if compile_result.get("status") == "completed" else rel(MT5_COMPILE_RESULT),
            "next_condition": "compile_status_completed(컴파일 완료 상태)",
            "effect": "December h21 long suppression(12월 21시 롱 억제)을 `.set` parameter(설정 파라미터)로 표현할 수 있게 한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "blocker_id": "synthetic_short_source_runtime_missing",
            "status": "blocked(차단)",
            "recovery_action": "materialized exact blocker and BV repair queue(정확 차단 사유와 BV 수리 대기열 물질화)",
            "command_or_evidence": f"{rel(SOURCE_SYNTHETIC_SHORT_TAPE)}; {rel(RUNTIME_RULE_HANDOFF)}",
            "failure_log": "no EA capability for BQ/BS synthetic fixed-hold short insertion(BQ/BS 합성 고정 보유 숏 삽입 EA 기능 없음)",
            "next_condition": "runtime signal source package or model/rule bundle that emits the same short entries(같은 숏 진입을 내는 런타임 신호 원천 패키지 또는 모델/규칙 번들)",
            "effect": "proxy expected value(프록시 예상값)를 MT5 KPI(MT5 핵심 성과 지표)처럼 쓰지 않게 한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    write_csv(BLOCKER_RECOVERY_LOG, recovery_rows)
    mt5_net = as_float(bk_final.get("mt5_net_profit"), 0.0)
    mt5_pf = as_float(bk_final.get("mt5_profit_factor"), 0.0)
    mt5_trades = as_int(bk_final.get("mt5_trade_count"), 0)
    bs_net = as_float(selected.get("net_profit"), 0.0)
    bs_pf = as_float(selected.get("profit_factor"), 0.0)
    bs_trades = as_int(selected.get("trade_count"), 0)
    bq_net = as_float(bq_selected.get("net_profit"), 0.0)
    bq_pf = as_float(bq_selected.get("profit_factor"), 0.0)
    bq_trades = as_int(bq_selected.get("trade_count"), 0)
    rows = [
        {
            "run_id": RUN_ID,
            "comparison_id": "bs_proxy_vs_bk_mt5_runtime_probe",
            "proxy_candidate_id": selected.get("candidate_id"),
            "mt5_source_run_id": SOURCE_RUNTIME_PROBE_RUN_ID,
            "proxy_net_profit": bs_net,
            "mt5_net_profit": mt5_net,
            "net_diff_proxy_minus_mt5": round(bs_net - mt5_net, 10),
            "proxy_profit_factor": bs_pf,
            "mt5_profit_factor": mt5_pf,
            "profit_factor_diff_proxy_minus_mt5": round(bs_pf - mt5_pf, 10),
            "proxy_trade_count": bs_trades,
            "mt5_trade_count": mt5_trades,
            "trade_count_diff_proxy_minus_mt5": bs_trades - mt5_trades,
            "attribution": "BS proxy adds BQ synthetic short source and December h21 long suppression without exact MT5 execution(BS 프록시는 정확 MT5 실행 없이 BQ 합성 숏 원천과 12월 21시 롱 억제를 더한다.)",
            "usability": "signal_sanity_only_not_runtime_authority(신호 점검 전용, 런타임 권위 아님)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "comparison_id": "bq_proxy_vs_bk_mt5_runtime_probe",
            "proxy_candidate_id": bq_selected.get("candidate_id"),
            "mt5_source_run_id": SOURCE_RUNTIME_PROBE_RUN_ID,
            "proxy_net_profit": bq_net,
            "mt5_net_profit": mt5_net,
            "net_diff_proxy_minus_mt5": round(bq_net - mt5_net, 10),
            "proxy_profit_factor": bq_pf,
            "mt5_profit_factor": mt5_pf,
            "profit_factor_diff_proxy_minus_mt5": round(bq_pf - mt5_pf, 10),
            "proxy_trade_count": bq_trades,
            "mt5_trade_count": mt5_trades,
            "trade_count_diff_proxy_minus_mt5": bq_trades - mt5_trades,
            "attribution": "BQ proxy changed short-source insertion rules without new MT5 execution(BQ 프록시는 새 MT5 실행 없이 숏 원천 삽입 규칙을 바꿨다.)",
            "usability": "signal_sanity_only_not_runtime_authority(신호 점검 전용, 런타임 권위 아님)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "comparison_id": "exact_bs_mt5_precheck",
            "proxy_candidate_id": selected.get("candidate_id"),
            "mt5_source_run_id": "",
            "proxy_net_profit": bs_net,
            "mt5_net_profit": "",
            "net_diff_proxy_minus_mt5": "",
            "proxy_profit_factor": bs_pf,
            "mt5_profit_factor": "",
            "profit_factor_diff_proxy_minus_mt5": "",
            "proxy_trade_count": bs_trades,
            "mt5_trade_count": "",
            "trade_count_diff_proxy_minus_mt5": "",
            "attribution": "not run because exact runtime signal source is missing(정확 런타임 신호 원천 누락으로 미실행)",
            "usability": "blocked_until_runtime_signal_source_repair(런타임 신호 원천 수리 전까지 차단)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    write_csv(PROXY_MT5_DIFF_HANDOFF, rows)


def write_verification_attempt(compile_result: Mapping[str, Any], portable_sync: Mapping[str, Any]) -> None:
    payload = {
        "run_id": RUN_ID,
        "narrow_external_check": "MetaEditor compile and portable EX5 sync(메타에디터 컴파일과 포터블 EX5 동기화)",
        "compile_status": compile_result.get("status"),
        "portable_sync": portable_sync.get("copied"),
        "strategy_tester_exact_precheck": {
            "status": "not_attempted_blocked(미시도 차단)",
            "reason": "exact BS proxy requires synthetic short source runtime support(정확 BS 프록시는 합성 숏 원천 런타임 지원이 필요하다.)",
        },
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(EXTERNAL_VERIFICATION_ATTEMPT, payload)


def queue_rows() -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "queue_rank": 1,
            "queue_id": "bv01_runtime_signal_source_contract",
            "action": "define whether BQ/BS synthetic short entries can become a runtime signal source(BQ/BS 합성 숏 진입을 런타임 신호 원천으로 만들 수 있는지 정의)",
            "success_criteria": "no lookahead, no realized-PnL priority, closed M5 probability/hour only(미래참조 없음, 실현손익 우선순위 없음, 닫힌 M5 확률/시간만 사용)",
            "effect": "exact MT5 precheck(정확 MT5 사전점검)의 차단 사유를 수리 조건으로 바꾼다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "queue_rank": 2,
            "queue_id": "bv02_exact_calendar_plus_short_source_package",
            "action": "if source is valid, package calendar block plus short source for MT5 tester(원천이 유효하면 달력 차단과 숏 원천을 MT5 테스터용으로 패키지)",
            "success_criteria": "set/ini/common files and tester identity ready without KPI claim(설정/INI/공용 파일/테스터 정체성 준비, KPI 주장 없음)",
            "effect": "BU handoff(인계)를 실제 MT5 runtime probe(런타임 탐침)로 이어갈 수 있게 한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "queue_rank": 3,
            "queue_id": "bv03_reject_if_short_source_not_runtime_safe",
            "action": "reject or redesign if synthetic short source is not timestamp-safe(합성 숏 원천이 시점 안전하지 않으면 거절 또는 재설계)",
            "success_criteria": "result judgment names invalid/inconclusive/repaired path(결과 판정이 무효/불충분/수리 경로를 명명)",
            "effect": "좋은 proxy(프록시)를 운영 후보로 착각하지 않게 한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def write_receipts(final: Mapping[str, Any], selected: Mapping[str, Any], compile_result: Mapping[str, Any], handoff: Mapping[str, Any]) -> None:
    write_json(
        DATA_RECEIPT,
        {
            "run_id": RUN_ID,
            "timestamp_safety": "calendar block uses entry-known month/hour/side only(달력 차단은 진입시점에 아는 월/시간/방향만 사용)",
            "lookahead_risk": "synthetic short tape is proxy-only until runtime signal source is proven(합성 숏 테이프는 런타임 신호 원천이 입증될 때까지 프록시 전용)",
            "source_inputs": [rel(path) for path in INPUT_FILES],
            "judgment": "calendar_gate_timestamp_safe_but_exact_proxy_runtime_incomplete(달력 게이트는 시점 안전하나 정확 프록시 런타임은 미완성)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(
        RUNTIME_RECEIPT,
        {
            "run_id": RUN_ID,
            "research_path": rel(SOURCE_SELECTED_CANDIDATE),
            "runtime_path": rel(SOURCE_EA),
            "shared_contract": "calendar block uses closed M5 target month/hour and decision side(달력 차단은 닫힌 M5 대상 월/시간과 판정 방향을 사용)",
            "known_differences": [
                "synthetic short source insertion missing in runtime(합성 숏 원천 삽입 런타임 누락)",
                "exact BS proxy was not run in Strategy Tester(정확 BS 프록시는 전략 테스터에서 실행되지 않음)",
            ],
            "parity_check": "MetaEditor compile attempted; tester exact precheck blocked(메타에디터 컴파일 시도, 테스터 정확 사전점검 차단)",
            "parity_identity": {
                "module_hashes": mt5_runtime_module_hashes(),
                "compile_result": rel(MT5_COMPILE_RESULT),
                "handoff": handoff.get("tester_handoff"),
            },
            "runtime_claim_boundary": "blocked_runtime_probe_precheck_only(차단된 런타임 탐침 사전점검 전용)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(
        BACKTEST_RECEIPT,
        {
            "run_id": RUN_ID,
            "tester_identity": rel(TESTER_IDENTITY_CONTRACT),
            "ea_identity": mt5_runtime_module_hashes(),
            "report_identity": "missing_not_run(미실행으로 누락)",
            "trade_evidence": "proxy only; no exact MT5 trades(프록시 전용, 정확 MT5 거래 없음)",
            "cost_assumptions": "tester identity fixed, broker-native real-tick costs intended but not executed(테스터 정체성 고정, 브로커 실제 틱 비용 의도이나 미실행)",
            "forensic_checks": ["set_manifest", "ini_manifest", "compile_attempt", "semantic_gap_audit"],
            "backtest_judgment": "blocked(차단)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(
        JUDGMENT_RECEIPT,
        {
            "result_subject": "BS late-year session gate MT5 precheck(BS 연말 세션 게이트 MT5 사전점검)",
            "evidence_available": [rel(RUNTIME_GATE_SUPPORT_AUDIT), rel(MT5_COMPILE_RESULT), rel(PROXY_MT5_DIFF_HANDOFF), rel(BLOCKER_RECOVERY_LOG)],
            "evidence_missing": ["exact MT5 Strategy Tester output(정확 MT5 전략 테스터 출력)", "runtime synthetic short source(런타임 합성 숏 원천)"],
            "judgment_label": "inconclusive_blocked_runtime_precheck(불충분/차단 런타임 사전점검)",
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": "BV creates or rejects timestamp-safe runtime short source(BV가 시점 안전 런타임 숏 원천을 만들거나 거절)",
            "user_explanation_hook": "calendar gate is now expressible, but the profitable proxy still needs a real runtime short-source path(달력 게이트는 이제 표현 가능하지만 수익성 프록시는 실제 런타임 숏 원천 경로가 필요하다.)",
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            "run_id": RUN_ID,
            "runtime_authority": "not_claimed",
            "operating_promotion": "not_claimed",
            "live_readiness": "not_claimed",
            "goal_achieve": "not_claimed",
            "reason": "exact MT5 evidence missing and synthetic short runtime support missing(정확 MT5 근거와 합성 숏 런타임 지원 누락)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    lineage_outputs = [{"path": rel(path), "sha256": sha(path)} for path in OUTPUT_FILES if exists(path) and io_path(Path(path)).is_file()]
    write_json(
        LINEAGE_RECEIPT,
        {
            "run_id": RUN_ID,
            "source_inputs": [{"path": rel(path), "sha256": sha(path)} for path in INPUT_FILES if exists(path)],
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [row["path"] for row in lineage_outputs],
            "artifact_hashes": lineage_outputs,
            "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "availability": "tracked_after_commit_or_manifested(커밋 후 추적 또는 목록화)",
            "lineage_judgment": "connected_with_blocked_boundary(차단 경계와 함께 연결됨)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
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
            "offensive_exploration": "preserve BS proxy clue while opening runtime short-source repair(BS 프록시 단서를 보존하고 런타임 숏 원천 수리를 연다)",
            "repair_control": "calendar block support added and compiled(달력 차단 지원 추가 및 컴파일)",
            "runtime_verification": "compile attempted; exact tester blocked(컴파일 시도, 정확 테스터 차단)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def gate_rows(compile_result: Mapping[str, Any], support_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    support_ok = all(row.get("status") in {"passed", "blocked"} for row in support_rows)
    calendar_ok = all(row.get("status") == "passed" for row in support_rows if str(row.get("check_id", "")).startswith("calendar"))
    compile_ok = compile_result.get("status") == "completed"
    gates = [
        ("input_lineage_gate", True, INPUT_MANIFEST, "BU 입력과 해시(hash, 해시)를 고정한다."),
        ("runtime_calendar_gate_support", calendar_ok, RUNTIME_GATE_SUPPORT_AUDIT, "12월 21시 long(롱) 억제를 런타임 파라미터로 표현한다."),
        ("metaeditor_compile_gate", compile_ok, MT5_COMPILE_RESULT, "EA(전문가 자문) 변경이 컴파일되는지 좁게 확인한다."),
        ("tester_identity_handoff_gate", exists(TESTER_SET_MANIFEST) and exists(TESTER_INI_MANIFEST), TESTER_IDENTITY_CONTRACT, "MT5 tester(테스터) 정체성은 고정하되 실행 KPI는 주장하지 않는다."),
        ("exact_runtime_semantic_gate", False, RUNTIME_RULE_HANDOFF, "synthetic short(합성 숏) 원천이 없어 정확 BS proxy(프록시)는 아직 런타임 의미가 닫히지 않았다."),
        ("mt5_execution_gate", False, EXTERNAL_VERIFICATION_ATTEMPT, "정확 의미 차이 때문에 Strategy Tester(전략 테스터)를 KPI 근거로 실행하지 않는다."),
        ("proxy_mt5_diff_gate", True, PROXY_MT5_DIFF_HANDOFF, "proxy expected value(프록시 예상값)와 기존 MT5 KPI(MT5 핵심 성과 지표) 차이를 분리한다."),
        ("blocker_recovery_gate", True, BLOCKER_RECOVERY_LOG, "차단 사유와 복구 조건을 정확히 남긴다."),
        ("final_claim_guard", True, CLAIM_RECEIPT, "runtime authority(런타임 권위), operating promotion(운영 승격), Goal Achieve(목표 달성)를 주장하지 않는다."),
        ("required_gate_coverage_audit", support_ok and exists(GATE_AUDIT), GATE_AUDIT, "필수 gate(게이트)의 통과/차단 상태를 closeout(종료 기록)에 연결한다."),
    ]
    rows = []
    for gate, passed, evidence, effect in gates:
        status = "passed" if passed else "blocked"
        rows.append(
            {
                "run_id": RUN_ID,
                "gate": gate,
                "status": status,
                "evidence": rel(evidence),
                "effect": effect,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def final_payload(
    selected: Mapping[str, Any],
    bq_selected: Mapping[str, Any],
    bk_final: Mapping[str, Any],
    compile_result: Mapping[str, Any],
    portable_sync: Mapping[str, Any],
    gates: Sequence[Mapping[str, Any]],
    created_at: str,
) -> dict[str, Any]:
    passed = sum(1 for row in gates if row.get("status") == "passed")
    return {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "created_at_utc": created_at,
        "parent_run_id": PARENT_RUN_ID,
        "baseline_run_id": BASELINE_RUN_ID,
        "source_runtime_probe_run_id": SOURCE_RUNTIME_PROBE_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_run_id": NEXT_RUN_ID,
        "selected_candidate_id": selected.get("candidate_id"),
        "selected_net_profit": selected.get("net_profit"),
        "selected_profit_factor": selected.get("profit_factor"),
        "selected_expectancy": selected.get("expectancy"),
        "selected_trade_count": selected.get("trade_count"),
        "selected_density": selected.get("trade_density_per_business_day"),
        "selected_closed_drawdown_amount": selected.get("closed_drawdown_amount"),
        "selected_recovery_factor": selected.get("recovery_factor"),
        "selected_long_trade_count": selected.get("long_trade_count"),
        "selected_short_trade_count": selected.get("short_trade_count"),
        "selected_short_share": selected.get("short_share"),
        "selected_parent_suppressed_trade_count": selected.get("parent_suppressed_trade_count"),
        "selected_parent_suppressed_net_profit": selected.get("parent_suppressed_net_profit"),
        "selected_synthetic_added_short_count": selected.get("synthetic_added_short_count"),
        "bq_selected_candidate_id": bq_selected.get("candidate_id"),
        "bk_mt5_net_profit": bk_final.get("mt5_net_profit"),
        "bk_mt5_profit_factor": bk_final.get("mt5_profit_factor"),
        "bk_mt5_trade_count": bk_final.get("mt5_trade_count"),
        "compile_status": compile_result.get("status"),
        "portable_ea_copied": portable_sync.get("copied"),
        "external_verification_status": "blocked_exact_tester_not_run(정확 테스터 미실행 차단)",
        "exact_mt5_execution": "not_run",
        "exact_mt5_blocker": "synthetic_short_source_runtime_missing",
        "calendar_gate_support": "materialized_and_compile_checked" if compile_result.get("status") == "completed" else "materialized_compile_blocked",
        "gate_passes": passed,
        "gate_total": len(gates),
        "new_model_training": "not_run",
        "new_mt5_execution": "not_run_exact_semantic_gap",
        "forward_passed": "not_claimed",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "live_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def sync_stage_brief_header(next_run_id: str) -> None:
    if not exists(STAGE_BRIEF):
        return
    text = io_path(STAGE_BRIEF).read_text(encoding="utf-8-sig")
    lines = []
    replaced = False
    for line in text.splitlines():
        if line.startswith("Current active run("):
            lines.append(f"Current active run(현재 활성 실행): `{next_run_id}`")
            replaced = True
        else:
            lines.append(line)
    if replaced:
        write_text(STAGE_BRIEF, "\n".join(lines) + "\n", bom=True)


def write_docs(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    support_rows = read_rows(RUNTIME_GATE_SUPPORT_AUDIT)
    diff_rows = read_rows(PROXY_MT5_DIFF_HANDOFF)
    blocker_rows = read_rows(BLOCKER_RECOVERY_LOG)
    report = f"""# run364BU late-year session gate MT5 precheck(364BU 연말 세션 게이트 MT5 사전점검)

## Scope(범위)
- Parent(부모): `{PARENT_RUN_ID}`
- Candidate(후보): `{final['selected_candidate_id']}`
- New model training(새 모델 학습): `not_run(미실행)`
- Exact MT5 execution(정확 MT5 실행): `{final['exact_mt5_execution']}`
- Operating claim(운영 주장): `not_claimed(주장 없음)`

## Result(결과)
Calendar block(달력 차단)은 EA(`Expert Advisor`, 전문가 자문)와 input contract(입력 계약)에 추가했고, MetaEditor compile(메타에디터 컴파일) 상태는 `{final['compile_status']}`다. 효과(effect, 효과)는 `December h21 long suppression(12월 21시 롱 억제)`을 `.set` parameter(설정 파라미터)로 표현할 수 있게 한 것이다.

Exact MT5 precheck(정확 MT5 사전점검)는 실행하지 않았다. 이유(reason, 이유)는 BS proxy(BS 프록시)가 `synthetic short source(합성 숏 원천)` 47개를 필요로 하지만, 현재 EA runtime(EA 런타임)에 같은 숏 진입 원천을 내는 기능이 없기 때문이다. 효과(effect, 효과)는 proxy expected value(프록시 예상값)를 MT5 KPI(MT5 핵심 성과 지표)처럼 오해하지 않게 하는 것이다.

## Proxy KPI(프록시 KPI)
- net/PF/expectancy(순수익/수익 팩터/기대값): `{final['selected_net_profit']}` / `{final['selected_profit_factor']}` / `{final['selected_expectancy']}`
- trades/density(거래수/밀도): `{final['selected_trade_count']}` / `{final['selected_density']}`
- long/short(롱/숏): `{final['selected_long_trade_count']}` / `{final['selected_short_trade_count']}`
- suppressed parent trades/net(억제 부모 거래/순수익): `{final['selected_parent_suppressed_trade_count']}` / `{final['selected_parent_suppressed_net_profit']}`

## Support Audit(지원 감사)
{markdown_table(support_rows, ['check_id', 'present', 'status', 'effect'], 12)}

## Proxy vs MT5(프록시 대 MT5)
{markdown_table(diff_rows, ['comparison_id', 'proxy_net_profit', 'mt5_net_profit', 'net_diff_proxy_minus_mt5', 'proxy_trade_count', 'mt5_trade_count', 'usability'], 6)}

## Blocker Recovery(차단 복구)
{markdown_table(blocker_rows, ['blocker_id', 'status', 'recovery_action', 'next_condition'], 6)}

## Gates(게이트)
{markdown_table(gates, ['gate', 'status', 'effect'], 12)}

## Boundary(경계)
이 run(실행)은 runtime precheck(런타임 사전점검)와 blocker recovery(차단 복구)다. runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 `not_claimed(주장 없음)`이다.
"""
    write_text(REPORT_PATH, report, bom=True)
    decision_doc = f"""# {TODAY} Stage364BU decision(결정)

Decision(결정): `{final['decision']}`

Judgment(판정): `{final['judgment']}`

Action(행동): calendar block(달력 차단) 런타임 지원을 추가하고 compile(컴파일)로 좁게 검증했다. Effect(효과): 12월 21시 long(롱) 억제를 `.set` parameter(설정 파라미터)로 표현할 수 있게 됐다.

Action(행동): exact MT5 precheck(정확 MT5 사전점검)는 차단으로 닫았다. Effect(효과): synthetic short source(합성 숏 원천) 누락이 운영 주장(operating claim, 운영 주장)으로 번지는 일을 막는다.

Next(다음): `{NEXT_RUN_ID}`.

Forbidden claims(금지 주장): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성).
"""
    write_text(DECISION_DOC, decision_doc, bom=True)
    current = f"""# Current Working State(현재 작업 상태)

Updated(갱신): {final['created_at_utc']}

Active stage(활성 단계): `{STAGE_ID}`

Latest completed/closed run(최근 종료 실행): `{RUN_ID}`

Current run(현재 실행): `{NEXT_RUN_ID}`

Current truth(현재 진실): `run364BU` added calendar block(달력 차단) support to EA(`Expert Advisor`, 전문가 자문), attempted MetaEditor compile(메타에디터 컴파일), and blocked exact MT5 precheck(정확 MT5 사전점검) because synthetic short source(합성 숏 원천) is not runtime-materialized(런타임 물질화 안 됨).

Selected proxy(선택 프록시): `{final['selected_candidate_id']}` net/PF/trades(순수익/수익 팩터/거래수) `{final['selected_net_profit']}` / `{final['selected_profit_factor']}` / `{final['selected_trade_count']}`.

Next action(다음 행동): `{NEXT_RUN_ID}` should either materialize a timestamp-safe runtime short source(시점 안전 런타임 숏 원천) or reject/redesign the proxy source(프록시 원천 거절/재설계).

Operating boundary(운영 경계): no runtime authority(런타임 권위 없음), no operating promotion(운영 승격 없음), no live readiness(실거래 준비 없음), no Goal Achieve(목표 달성 없음).
"""
    write_text(CURRENT_WORKING_STATE, current, bom=True)
    workspace_state = f"""current_stage_id: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {final['status']}
current_judgment: {final['judgment']}
next_run_id: {NEXT_RUN_ID}
runtime_authority: not_claimed
operating_promotion: not_claimed
goal_achieve: not_claimed
updated_at_utc: {final['created_at_utc']}
"""
    write_text(WORKSPACE_STATE, workspace_state, bom=False)
    selection = f"""# Stage364 selection status(선택 상태)

Updated(갱신): {final['created_at_utc']}

Current run(현재 실행): `{NEXT_RUN_ID}`
Latest closed run(최근 종료 실행): `{RUN_ID}`

Selected proxy for runtime repair(런타임 수리용 선택 프록시): `{final['selected_candidate_id']}`

Proxy KPI(프록시 핵심 성과 지표): net `{final['selected_net_profit']}`, PF `{final['selected_profit_factor']}`, expectancy `{final['selected_expectancy']}`, trades `{final['selected_trade_count']}`, density `{final['selected_density']}`, long/short `{final['selected_long_trade_count']}` / `{final['selected_short_trade_count']}`.

Runtime precheck(런타임 사전점검): calendar block(달력 차단) compile `{final['compile_status']}`, exact MT5 execution(정확 MT5 실행) `not_run_exact_semantic_gap(정확 의미 차이로 미실행)`.

Open blocker(열린 차단): `synthetic_short_source_runtime_missing(합성 숏 원천 런타임 누락)`.

Next queue(다음 대기열): `{rel(RUN364BV_QUEUE)}`

Authority(권위): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함).
"""
    write_text(SELECTION_STATUS, selection, bom=True)
    sync_stage_brief_header(NEXT_RUN_ID)
    append_text_once(REVIEW_INDEX, "<!-- run364BU -->", f"\n<!-- run364BU -->\n- `{RUN_ID}`: late-year session gate MT5 precheck(연말 세션 게이트 MT5 사전점검) -> `{REPORT_PATH.relative_to(ROOT).as_posix()}`\n")
    append_text_once(STAGE_README, "<!-- run364BU -->", f"\n<!-- run364BU -->\n## run364BU late-year session gate MT5 precheck(연말 세션 게이트 MT5 사전점검)\n\n`{final['judgment']}`. Next(다음): `{NEXT_RUN_ID}`.\n")
    append_text_once(WORKSPACE_CHANGELOG, "<!-- run364BU -->", f"\n<!-- run364BU -->\n- {final['created_at_utc']} `{RUN_ID}` added calendar block support(달력 차단 지원 추가), compile-checked EA(컴파일 확인 EA), and recorded exact MT5 precheck blocker(정확 MT5 사전점검 차단 사유 기록).\n")
    append_text_once(IDEA_REGISTRY, "<!-- run364BU_late_year_session_gate -->", f"\n<!-- run364BU_late_year_session_gate -->\n- Idea(아이디어): December h21 long suppression(12월 21시 롱 억제) as runtime calendar block(런타임 달력 차단). Effect(효과): low-sample proxy repair(소표본 프록시 수리)를 `.set` parameter(설정 파라미터)로 표현한다.\n")
    append_text_once(NEGATIVE_RESULT_REGISTER, "<!-- run364BU_synthetic_short_source_blocker -->", f"\n<!-- run364BU_synthetic_short_source_blocker -->\n- Blocker memory(차단 기억): `{RUN_ID}` could not run exact MT5 precheck(정확 MT5 사전점검) because synthetic short source runtime support(합성 숏 원천 런타임 지원)가 missing(누락)이다. Effect(효과): 다음 작업은 같은 외부 검증 누락을 말로만 반복하지 않고 source materialization(원천 물질화) 또는 rejection(거절)을 해야 한다.\n")


def ledger_rows(final: Mapping[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    common = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "date": TODAY,
        "status": final["status"],
        "judgment": final["judgment"],
        "decision": final["decision"],
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "rows": 1,
        "gate_passes": final["gate_passes"],
        "gate_total": final["gate_total"],
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "primary_artifact": rel(FINAL_DECISION),
        "net_profit": final["selected_net_profit"],
        "profit_factor": final["selected_profit_factor"],
        "trade_count": final["selected_trade_count"],
        "trade_density_per_feature_day": final["selected_density"],
        "work_family": "runtime_backtest(런타임 백테스트)",
        "evidence_boundary": "runtime_precheck_blocked(런타임 사전점검 차단)",
        "result_judgment": final["judgment"],
        "final_decision_path": rel(FINAL_DECISION),
        "gate_audit_path": rel(GATE_AUDIT),
        "created_at": final["created_at_utc"],
        "next_action": NEXT_RUN_ID,
        "question": "Can BS late-year session repair be prepared for exact MT5 precheck?(BS 연말 세션 수리를 정확 MT5 사전점검으로 준비할 수 있는가?)",
    }
    run_rows = [{**common, "lane": "runtime_precheck(런타임 사전점검)", "path": rel(FINAL_DECISION)}]
    stage_rows = []
    for view, tier, scope in [
        ("Tier A used(Tier A 사용)", "Tier A", "calendar_gate_handoff_blocked_exact"),
        ("Tier B fallback used(Tier B 대체 사용)", "Tier B", "missing_required"),
        ("actual routed total(실제 라우팅 전체)", "Tier A+B", "blocked_exact_not_run"),
    ]:
        row = {
            **common,
            "ledger_row_id": f"{RUN_ID}::{tier.replace(' ', '_').replace('+', 'B')}",
            "row_id": f"{RUN_ID}::{tier.replace(' ', '_').replace('+', 'B')}",
            "record_view": view,
            "tier_scope": tier,
            "kpi_scope": scope,
            "path": rel(FINAL_DECISION),
        }
        if scope != "calendar_gate_handoff_blocked_exact":
            row.update({"net_profit": "", "profit_factor": "", "trade_count": "", "trade_density_per_feature_day": "", "notes": "No exact tester run or Tier B fallback in BU(BU에는 정확 테스터 실행 또는 Tier B 대체 없음)."})
        stage_rows.append(row)
    return run_rows, stage_rows, stage_rows


def write_ledgers(final: Mapping[str, Any]) -> None:
    run_rows, stage_rows, project_rows = ledger_rows(final)
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], run_rows, extend_header=True)
    append_or_replace_csv(STAGE_LEDGER, ["ledger_row_id"], stage_rows, extend_header=True)
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], project_rows, extend_header=True)
    bj_runtime.bd_package.repair_run_registry_line_endings(RUN_ID)


def write_artifact_registry(final: Mapping[str, Any]) -> None:
    rows = []
    for artifact_id, path, role in [
        ("stage364BU_final_decision", FINAL_DECISION, "final decision(최종 결정)"),
        ("stage364BU_runtime_rule_handoff", RUNTIME_RULE_HANDOFF, "runtime handoff(런타임 인계)"),
        ("stage364BU_gate_support_audit", RUNTIME_GATE_SUPPORT_AUDIT, "gate support audit(게이트 지원 감사)"),
        ("stage364BU_proxy_mt5_diff_handoff", PROXY_MT5_DIFF_HANDOFF, "proxy MT5 diff(프록시 MT5 차이)"),
        ("stage364BU_report", REPORT_PATH, "review report(검토 보고서)"),
    ]:
        rows.append(
            {
                "artifact_id": artifact_id,
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "path": rel(path),
                "artifact_role": role,
                "sha256": sha(path),
                "created_at_utc": final["created_at_utc"],
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    append_or_replace_csv(ARTIFACT_REGISTRY, ["artifact_id"], rows, extend_header=True)


def write_manifest(final: Mapping[str, Any]) -> None:
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "run_number": RUN_NUMBER,
            "stage_id": STAGE_ID,
            "created_at_utc": final["created_at_utc"],
            "producer": rel(Path(__file__)),
            "inputs": [{"path": rel(path), "sha256": sha(path)} for path in INPUT_FILES if exists(path)],
            "outputs": [{"path": rel(path), "sha256": sha(path)} for path in OUTPUT_FILES if exists(path) and io_path(Path(path)).is_file()],
            "external_verification_status": final["external_verification_status"],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def main() -> None:
    ensure_dirs()
    created_at = now_utc()
    validate_inputs()
    selected = read_json(SOURCE_SELECTED_CANDIDATE)
    bq_selected = read_json(SOURCE_BQ_SELECTED_CANDIDATE)
    bk_final = read_json(SOURCE_BK_FINAL)
    write_csv(INPUT_MANIFEST, input_manifest_rows())
    support_rows = audit_runtime_gate_support()
    handoff = materialize_calendar_gate_handoff(selected)
    compile_result, portable_sync = compile_and_sync()
    write_verification_attempt(compile_result, portable_sync)
    write_blocker_and_diff(selected, bq_selected, bk_final, compile_result)
    write_csv(RUN364BV_QUEUE, queue_rows())
    gates = gate_rows(compile_result, support_rows)
    write_csv(GATE_AUDIT, gates)
    final = final_payload(selected, bq_selected, bk_final, compile_result, portable_sync, gates, created_at)
    write_json(FINAL_DECISION, final)
    write_receipts(final, selected, compile_result, handoff)
    write_docs(final, gates)
    write_ledgers(final)
    write_artifact_registry(final)
    write_manifest(final)
    print(json.dumps(json_ready(final), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
