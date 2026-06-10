from __future__ import annotations

import csv
import hashlib
import json
import sys
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path
from stage_pipelines.stage364 import execute_h17_short_quality_risk_scale_mt5_runtime_probe_without_db as base
from stage_pipelines.stage364 import materialize_h17_short_source_expansion_runtime_package_without_db as pkg


RUN_NUMBER = "run364DG"
RUN_ID = "run364DG_execute_h17_short_source_expansion_mt5_runtime_probe_without_db_v1"
PARENT_RUN_ID = pkg.RUN_ID
NEXT_RUN_ID = "run364DH_review_h17_short_source_expansion_mt5_runtime_probe_without_db_v1"

STATUS_COMPLETED = "completed_stage364DG_h17_short_source_expansion_mt5_probe_outputs_available_review_required_no_authority"
STATUS_BLOCKED = "blocked_stage364DG_h17_short_source_expansion_mt5_probe_attempt_recorded_repair_required_no_authority"
JUDGMENT_COMPLETED = "mt5_runtime_probe_outputs_available_dd05_short_source_proxy_diff_review_required_no_authority"
JUDGMENT_BLOCKED = "mt5_runtime_probe_attempt_recorded_dd05_outputs_missing_or_failed_repair_required_no_authority"
DECISION_COMPLETED = "stage364DG_open_run364DH_review_h17_short_source_expansion_mt5_runtime_probe"
DECISION_BLOCKED = "stage364DG_open_run364DH_repair_or_review_h17_short_source_expansion_mt5_runtime_probe"
CLAIM_BOUNDARY = (
    "research_development_mt5_runtime_probe_attempt_only_short_source_expansion_"
    "no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

STAGE_DIR = pkg.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
MT5_DIR = RUN_DIR / "mt5"
TELEMETRY_COPY_DIR = RUN_DIR / "runtime_telemetry"
REPORT_COPY_DIR = MT5_DIR / "reports"
REVIEW_DIR = STAGE_DIR / "03_reviews"
SPEC_DIR = STAGE_DIR / "00_spec"
SELECTED_DIR = STAGE_DIR / "04_selected"

TERMINAL_PROCESS_AUDIT = RUN_DIR / "terminal_process_audit.json"
MT5_EXECUTION_RESULT = RUN_DIR / "mt5_execution_result.json"
STRATEGY_TESTER_REPORTS = RUN_DIR / "strategy_tester_report_records.json"
EXECUTION_SUMMARY = RUN_DIR / "h17_short_source_expansion_mt5_probe_summary.csv"
PROXY_MT5_DIFF = RUN_DIR / "proxy_mt5_runtime_difference.csv"
RUNTIME_OUTPUT_COPY = RUN_DIR / "runtime_output_copy_manifest.csv"
RUNTIME_IDENTITY = RUN_DIR / "runtime_identity.csv"
EXPECTED_KPI_SUMMARY = RUN_DIR / "expected_kpi_summary.csv"
RUNTIME_PROBE_ATTEMPT_PACKAGE = RUN_DIR / "runtime_probe_attempt_package.csv"
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

REPORT_PATH = REVIEW_DIR / "run364DG_h17_short_source_expansion_mt5_runtime_probe.md"
DECISION_DOC = pkg.ROOT / "docs" / "decisions" / "2026-06-06_stage364DG_h17_short_source_expansion_mt5_runtime_probe.md"
REVIEW_INDEX = REVIEW_DIR / "review_index.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"
STAGE_BRIEF = SPEC_DIR / "stage_brief.md"
SELECTION_STATUS = SELECTED_DIR / "selection_status.md"
STAGE_README = STAGE_DIR / "README.md"
WORKSPACE_STATE = pkg.ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = pkg.ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_CHANGELOG = pkg.ROOT / "docs" / "workspace" / "changelog.md"
RUN_REGISTRY = pkg.ROOT / "docs" / "registers" / "run_registry.csv"
PROJECT_LEDGER = pkg.ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = pkg.ROOT / "docs" / "registers" / "artifact_registry.csv"
IDEA_REGISTRY = pkg.ROOT / "docs" / "registers" / "idea_registry.md"

INPUT_FILES = [
    pkg.FINAL_DECISION,
    pkg.GATE_AUDIT,
    pkg.RUNTIME_PROBE_ATTEMPT_PACKAGE,
    pkg.RUN364DG_EXECUTION_QUEUE,
    pkg.TESTER_SET_MANIFEST,
    pkg.TESTER_INI_MANIFEST,
    pkg.TESTER_IDENTITY_CONTRACT,
    pkg.RUNTIME_POLICY_CONFIG,
    pkg.RUNTIME_PARITY_CONTRACT,
    pkg.EXPECTED_KPI_SUMMARY,
    pkg.RUN_MANIFEST,
    pkg.SOURCE_ONNX,
    pkg.PORTABLE_EA_EX5,
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
    Path(__file__),
]


def rel(path: Path | str) -> str:
    target = Path(path)
    try:
        return target.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return target.as_posix()


def exists(path: Path | str) -> bool:
    return io_path(Path(path)).exists()


def sha(path: Path | str) -> str:
    raw = io_path(Path(path)).read_bytes()
    return hashlib.sha256(raw.replace(b"\r\n", b"\n")).hexdigest()


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
        except (AttributeError, ValueError, TypeError):
            pass
    if isinstance(value, float) and value != value:
        return None
    return value


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(io_path(path), encoding="utf-8-sig").fillna("")


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    materialized = [{str(key): json_ready(value) for key, value in row.items()} for row in rows]
    if fieldnames is None:
        fieldnames = []
        for row in materialized:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fieldnames), extrasaction="ignore")
        writer.writeheader()
        for row in materialized:
            writer.writerow(row)


def write_text(path: Path, text: str, *, bom: bool = True) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    encoding = "utf-8-sig" if bom else "utf-8"
    io_path(path).write_text(text, encoding=encoding)


def append_text_once(path: Path, marker: str, text: str) -> None:
    existing = io_path(path).read_text(encoding="utf-8-sig") if exists(path) else ""
    if marker in existing:
        return
    write_text(path, existing.rstrip() + "\n" + text.lstrip(), bom=True)


def append_or_replace_csv(path: Path, key_fields: Sequence[str], rows: Sequence[Mapping[str, Any]], *, extend_header: bool = True) -> None:
    materialized = [{str(key): json_ready(value) for key, value in row.items()} for row in rows]
    existing_rows: list[dict[str, Any]] = []
    fieldnames: list[str] = []
    if exists(path):
        with io_path(path).open("r", newline="", encoding="utf-8-sig") as handle:
            reader = csv.DictReader(handle)
            fieldnames = list(reader.fieldnames or [])
            existing_rows = [dict(row) for row in reader]
    if not fieldnames:
        for row in materialized:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    elif extend_header:
        for row in materialized:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)

    def row_key(row: Mapping[str, Any]) -> tuple[str, ...]:
        return tuple(str(row.get(key, "")) for key in key_fields)

    replacement = {row_key(row): row for row in materialized}
    kept = [row for row in existing_rows if row_key(row) not in replacement]
    write_csv(path, [*kept, *materialized], fieldnames)


def replace_prefixed_lines(path: Path, replacements: Mapping[str, str], *, bom: bool = True) -> None:
    lines = io_path(path).read_text(encoding="utf-8-sig").splitlines() if exists(path) else []
    replaced: set[str] = set()
    next_lines: list[str] = []
    for line in lines:
        match = next((prefix for prefix in replacements if line.startswith(prefix)), None)
        if match is None:
            next_lines.append(line)
            continue
        next_lines.append(replacements[match])
        replaced.add(match)
    for prefix, replacement in replacements.items():
        if prefix not in replaced:
            next_lines.append(replacement)
    write_text(path, "\n".join(next_lines).rstrip() + "\n", bom=bom)


def configure_base() -> None:
    base.pkg = pkg
    base.rel = rel
    base.exists = exists
    base.sha = sha
    base.json_ready = json_ready
    base.read_json = read_json
    base.write_json = write_json
    base.read_csv = read_csv
    base.write_csv = write_csv
    base.write_text = write_text
    base.append_text_once = append_text_once
    base.append_or_replace_csv = append_or_replace_csv
    base.replace_prefixed_lines = replace_prefixed_lines
    base.markdown_table = markdown_table
    base.RUN_NUMBER = RUN_NUMBER
    base.RUN_ID = RUN_ID
    base.PARENT_RUN_ID = PARENT_RUN_ID
    base.NEXT_RUN_ID = NEXT_RUN_ID
    base.STATUS_COMPLETED = STATUS_COMPLETED
    base.STATUS_BLOCKED = STATUS_BLOCKED
    base.JUDGMENT_COMPLETED = JUDGMENT_COMPLETED
    base.JUDGMENT_BLOCKED = JUDGMENT_BLOCKED
    base.DECISION_COMPLETED = DECISION_COMPLETED
    base.DECISION_BLOCKED = DECISION_BLOCKED
    base.CLAIM_BOUNDARY = CLAIM_BOUNDARY
    base.STAGE_ID = pkg.STAGE_ID
    base.STAGE_DIR = STAGE_DIR
    base.RUN_DIR = RUN_DIR
    base.MT5_DIR = MT5_DIR
    base.TELEMETRY_COPY_DIR = TELEMETRY_COPY_DIR
    base.REPORT_COPY_DIR = REPORT_COPY_DIR
    base.REVIEW_DIR = REVIEW_DIR
    base.SPEC_DIR = SPEC_DIR
    base.SELECTED_DIR = SELECTED_DIR
    for name, value in {
        "TERMINAL_PROCESS_AUDIT": TERMINAL_PROCESS_AUDIT,
        "MT5_EXECUTION_RESULT": MT5_EXECUTION_RESULT,
        "STRATEGY_TESTER_REPORTS": STRATEGY_TESTER_REPORTS,
        "EXECUTION_SUMMARY": EXECUTION_SUMMARY,
        "PROXY_MT5_DIFF": PROXY_MT5_DIFF,
        "RUNTIME_OUTPUT_COPY": RUNTIME_OUTPUT_COPY,
        "RUNTIME_IDENTITY": RUNTIME_IDENTITY,
        "EXPECTED_KPI_SUMMARY": EXPECTED_KPI_SUMMARY,
        "RUNTIME_PROBE_ATTEMPT_PACKAGE": RUNTIME_PROBE_ATTEMPT_PACKAGE,
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
    }.items():
        setattr(base, name, value)
    base.INPUT_FILES = INPUT_FILES
    base.OUTPUT_FILES = OUTPUT_FILES
    base.write_docs = write_docs
    base.write_ledgers = write_ledgers


def markdown_table(rows: Sequence[Mapping[str, Any]], columns: Sequence[str], limit: int = 12) -> str:
    return pkg.markdown_table(rows, columns, limit=limit)


def write_docs(final: Mapping[str, Any], summaries: Sequence[Mapping[str, Any]], proxy_rows: Sequence[Mapping[str, Any]], gates: Sequence[Mapping[str, Any]]) -> None:
    report = f"""# run364DG h17 short-source expansion MT5 runtime probe(17시 숏 원천 확장 MT5 런타임 탐침)

Updated(갱신): {final['created_at_utc']}

## Current Truth(현재 진실)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- judgment(판정): `{final['judgment']}`
- mt5_execution(MT5 실행): `{final['mt5_execution']}`
- runtime_authority(런타임 권위): `not_claimed`

## Action/Effect(행동/효과)

Action(행동): DF package(DF 패키지) `dd05_h17_21_short_source_m050_ex_aug`를 MT5 Strategy Tester(MT5 전략 테스터)로 실행 시도하고 telemetry/report(원격측정/보고서)를 수집했습니다.

Effect(효과): proxy expected value(프록시 기대값)와 실제 MT5 output(MT5 출력)을 분리해 `{NEXT_RUN_ID}`에서 diff(차이), attribution(귀속), usability(활용 가능성)를 검토할 수 있게 했습니다.

## Execution Summary(실행 요약)

{markdown_table(summaries, ['attempt_name', 'tester_status', 'runtime_status', 'report_status', 'net_profit', 'profit_factor', 'trade_count', 'long_trade_count', 'short_trade_count', 'blocker', 'comparison_status'])}

## Proxy vs MT5(프록시 대 MT5)

{markdown_table(proxy_rows, ['attempt_name', 'expected_net_profit', 'actual_mt5_net_profit', 'net_profit_diff_actual_minus_expected', 'expected_trade_count', 'actual_mt5_trade_count', 'trade_count_diff_actual_minus_expected', 'expected_profit_factor', 'actual_mt5_profit_factor', 'comparison_status'])}

## Gates(게이트)

{markdown_table(gates, ['gate', 'status', 'evidence', 'effect'])}

## Boundary(경계)

This run(이번 실행)은 runtime probe attempt(런타임 탐침 시도)입니다. forward pass(전진 통과), live readiness(실거래 준비), operating promotion(운영 승격), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 모두 `not_claimed(주장 안 함)`입니다.
"""
    pkg.write_text(REPORT_PATH, report, bom=True)
    pkg.write_text(
        DECISION_DOC,
        f"""# Stage364DG decision(결정): h17 short-source expansion MT5 runtime probe

- date(날짜): 2026-06-06
- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{final['decision']}`
- judgment(판정): `{final['judgment']}`
- runtime_completed_rows(런타임 완료 행): `{final['runtime_completed_rows']}`
- usable_report_rows(사용 가능 보고서 행): `{final['usable_report_rows']}`
- actual MT5 net/PF/trades(실제 MT5 순수익/수익 팩터/거래수): `{final['actual_mt5_net_profit']}` / `{final['actual_mt5_profit_factor']}` / `{final['actual_mt5_trade_count']}`
- next action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): DH에서 proxy/MT5 diff(프록시/MT5 차이), equity DD(수익곡선 낙폭), side balance(방향 균형)를 검토합니다.
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
        bom=True,
    )
    pkg.append_text_once(REVIEW_INDEX, f"run364DG__{RUN_ID}", f"\n- run364DG__{RUN_ID}: [{REPORT_PATH.name}]({REPORT_PATH.name}) - dd05 short-source expansion MT5 runtime probe(dd05 숏 원천 확장 MT5 런타임 탐침), next `{NEXT_RUN_ID}`.\n")
    pkg.append_text_once(STAGE_BRIEF, f"run364DG__{RUN_ID}", f"\n## run364DG MT5 Runtime Probe(MT5 런타임 탐침)\n\nAction(행동): DD05 package(DD05 패키지)를 Strategy Tester(전략 테스터)로 실행 시도했습니다.\n\nEffect(효과): `{NEXT_RUN_ID}`에서 proxy/MT5 diff(프록시/MT5 차이)를 검토할 수 있습니다.\n")
    pkg.append_text_once(STAGE_README, f"run364DG__{RUN_ID}", f"\n<!-- run364DG__{RUN_ID} -->\n## run364DG MT5 runtime probe(MT5 런타임 탐침)\n\n`dd05_h17_21_short_source_m050_ex_aug` probe(탐침) attempted(시도). Next(다음): `{NEXT_RUN_ID}`.\n")
    pkg.replace_prefixed_lines(
        STAGE_BRIEF,
        {
            "- current_run_id(현재 실행 ID):": f"- current_run_id(현재 실행 ID): `{NEXT_RUN_ID}`",
            "- latest_completed_run_id(최근 완료 실행 ID):": f"- latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`",
            "- selection_status(선택 상태):": f"- selection_status(선택 상태): `{final['status']}`",
            "- claim_boundary(주장 경계):": f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
        },
        bom=True,
    )
    pkg.write_text(WORKSPACE_STATE, f"""current_stage_id: {pkg.STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {final['status']}
current_judgment: {final['judgment']}
next_run_id: {NEXT_RUN_ID}
runtime_authority: not_claimed
operating_promotion: not_claimed
goal_achieve: not_claimed
updated_at_utc: {final['created_at_utc']}
""", bom=False)
    pkg.write_text(CURRENT_WORKING_STATE, f"""# Current Working State(현재 작업 상태)

Updated(갱신): {final['created_at_utc']}

Active stage(활성 단계): `{pkg.STAGE_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Current run(현재 실행): `{NEXT_RUN_ID}`

Current truth(현재 진실): `run364DG` executed/attempted(실행/시도) DD05 short-source expansion MT5 runtime probe(DD05 숏 원천 확장 MT5 런타임 탐침). runtime_completed_rows(런타임 완료 행)는 `{final['runtime_completed_rows']}`, usable_report_rows(사용 가능 보고서 행)는 `{final['usable_report_rows']}`, actual MT5 net/PF/trades(실제 MT5 순수익/수익 팩터/거래수)는 `{final['actual_mt5_net_profit']}` / `{final['actual_mt5_profit_factor']}` / `{final['actual_mt5_trade_count']}`입니다.

Next action(다음 행동): `{NEXT_RUN_ID}`에서 proxy/MT5 diff(프록시/MT5 차이), equity DD(수익곡선 낙폭), side balance(방향 균형), cost stress(비용 압박)를 review(검토)합니다.

Operating boundary(운영 경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""", bom=True)
    pkg.write_text(SELECTION_STATUS, f"""# Stage364 selection status(선택 상태)

Updated(갱신): {final['created_at_utc']}

Current run(현재 실행): `{NEXT_RUN_ID}`
Latest completed run(최근 완료 실행): `{RUN_ID}`

Latest MT5 runtime probe(최근 MT5 런타임 탐침): `{RUN_ID}`.

Actual MT5 net/PF/trades(실제 MT5 순수익/수익 팩터/거래수): `{final['actual_mt5_net_profit']}` / `{final['actual_mt5_profit_factor']}` / `{final['actual_mt5_trade_count']}`.

Expected proxy net/PF/trades(예상 프록시 순수익/수익 팩터/거래수): `{final['expected_net_profit']}` / `{final['expected_profit_factor']}` / `{final['expected_trade_count']}`.

Authority(권위): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""", bom=True)
    pkg.append_text_once(WORKSPACE_CHANGELOG, f"run364DG__{RUN_ID}", f"\n<!-- run364DG__{RUN_ID} -->\n- {final['created_at_utc']} `{RUN_ID}` attempted DD05 short-source expansion MT5 runtime probe(DD05 숏 원천 확장 MT5 런타임 탐침); judgment `{final['judgment']}`; no authority claim(권위 주장 없음).\n")
    pkg.append_text_once(IDEA_REGISTRY, f"run364DG__{RUN_ID}", f"\n<!-- run364DG__{RUN_ID} -->\n- `{RUN_ID}`: DD05 short-source expansion(DD05 숏 원천 확장)을 MT5 runtime probe(MT5 런타임 탐침)로 실행 시도했습니다.\n")


def write_ledgers(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    common = {
        "stage_id": pkg.STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "run_number": RUN_NUMBER,
        "date": "2026-06-06",
        "status": final["status"],
        "judgment": final["judgment"],
        "decision": final["decision"],
        "next_run_id": NEXT_RUN_ID,
        "rows": final["outputs_available_rows"],
        "gate_passes": sum(1 for row in gates if row["status"] == "passed"),
        "gate_total": len(gates),
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": pkg.rel(REPORT_PATH),
        "final_decision_path": pkg.rel(FINAL_DECISION),
        "gate_audit_path": pkg.rel(GATE_AUDIT),
        "created_at": final["created_at_utc"],
        "work_family": "runtime_backtest(런타임 백테스트)",
        "scoreboard_lane": "runtime_probe(런타임 탐침)",
        "external_verification_status": final["external_verification_status"],
        "evidence_boundary": "mt5_runtime_probe_no_authority(MT5 런타임 탐침, 권위 없음)",
        "question": "Does DD05 short-source expansion survive MT5 runtime probing?(DD05 숏 원천 확장이 MT5 런타임 탐침에서 버티는가?)",
        "next_action": NEXT_RUN_ID,
        "net_profit": final["actual_mt5_net_profit"],
        "profit_factor": final["actual_mt5_profit_factor"],
        "expectancy": final["actual_mt5_expectancy"],
        "trade_count": final["actual_mt5_trade_count"],
        "long_trade_count": final["actual_long_trade_count"],
        "short_trade_count": final["actual_short_trade_count"],
        "max_drawdown_amount": final["actual_drawdown"],
        "recovery_factor": final["actual_recovery_factor"],
        "result_judgment": final["judgment"],
        "path": pkg.rel(FINAL_DECISION),
        "primary_report": pkg.rel(REPORT_PATH),
        "primary_artifact": pkg.rel(EXECUTION_SUMMARY),
        "primary_kpi": f"mt5_net={final['actual_mt5_net_profit']};pf={final['actual_mt5_profit_factor']};trades={final['actual_mt5_trade_count']}",
        "guardrail_kpi": "runtime_authority=not_claimed;operating_promotion=not_claimed",
    }
    ledger_rows = []
    for suffix, record_view, tier_scope, status in [
        ("tier_a_used", "Tier A used(Tier A 사용)", "Tier A", final["status"]),
        ("tier_b_fallback_missing_required", "Tier B fallback used(Tier B 대체 사용)", "Tier B", "missing_required_no_fallback_source(필수 누락, 대체 원천 없음)"),
        ("actual_routed_total", "actual routed total(실제 라우팅 전체)", "Tier A+B", final["status"]),
    ]:
        row = {**common, "ledger_row_id": f"{RUN_ID}__{suffix}", "subrun_id": f"{RUN_ID}__{suffix}", "row_id": f"{RUN_ID}__{suffix}", "record_view": record_view, "tier_scope": tier_scope, "kpi_scope": "DG MT5 runtime probe(DG MT5 런타임 탐침)", "status": status, "view": record_view, "tier": tier_scope, "metric_scope": "mt5_runtime_probe(MT5 런타임 탐침)"}
        if suffix == "tier_b_fallback_missing_required":
            for key in ["net_profit", "profit_factor", "expectancy", "trade_count", "long_trade_count", "short_trade_count", "max_drawdown_amount", "recovery_factor"]:
                row[key] = ""
        ledger_rows.append(row)
    pkg.append_or_replace_csv(STAGE_LEDGER, ["ledger_row_id"], ledger_rows, extend_header=True)
    pkg.append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], ledger_rows, extend_header=True)
    pkg.append_or_replace_csv(RUN_REGISTRY, ["run_id"], [common], extend_header=True)
    base.repair_run_registry_line_endings(RUN_ID)


def main() -> None:
    configure_base()
    base.main()


if __name__ == "__main__":
    main()
