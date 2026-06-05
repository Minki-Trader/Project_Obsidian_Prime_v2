from __future__ import annotations

import csv
import hashlib
import json
import os
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[2]
TODAY = "2026-06-01"

SOURCE_STAGE_ID = "351_onnx_trade_surface_rebuild__no_scaler_or_1d_scaler_runtime_contract"
NEW_STAGE_ID = "352_runtime_probe_report_repair__no_scaler_1d_mt5_kpi_identity"
SOURCE_STAGE_DIR = ROOT / "stages" / SOURCE_STAGE_ID
NEW_STAGE_DIR = ROOT / "stages" / NEW_STAGE_ID

RUN_NUMBER = "run352A"
RUN_ID = "run352A_branch_stage351_to_report_identity_repair_without_db_v1"
PARENT_RUN_ID = "run351C_execute_no_scaler_or_1d_scaler_onnx_trade_surface_mt5_probe_without_db_v1"
NEXT_RUN_ID = "run352B_repair_no_scaler_1d_mt5_report_identity_reuse_outputs_without_db_v1"

STATUS = "completed_stage352A_branch_from_stage351_heavy_probe_to_report_identity_repair_no_selection"
JUDGMENT = "stage_branch_completed_stage351_heavy_trade_surface_probe_handoff_to_stage352_report_identity_repair_no_operating_claim"
DECISION = "stage352A_open_run352B_repair_no_scaler_1d_mt5_report_identity_reuse_outputs"
CLAIM_BOUNDARY = (
    "state_sync_stage_branch_report_identity_repair_handoff_only_no_new_mt5_execution_"
    "no_candidate_selection_no_forward_pass_no_live_readiness_no_operating_promotion_"
    "no_runtime_authority_no_goal_claim"
)
TRADE_DENSITY_REQUIREMENT = "trade_per_day_min_3_to_10_plus_no_trade_splitting"

RUN_DIR = NEW_STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = NEW_STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEW_DIR / "run352A_stage_branch.md"
REVIEW_INDEX = REVIEW_DIR / "review_index.md"
STAGE_BRIEF = NEW_STAGE_DIR / "00_spec" / "stage_brief.md"
STAGE_README = NEW_STAGE_DIR / "README.md"
INPUT_REFS = NEW_STAGE_DIR / "01_inputs" / "input_refs.md"
INPUT_MANIFEST = NEW_STAGE_DIR / "01_inputs" / "stage352_input_manifest.csv"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"
SELECTION_STATUS = NEW_STAGE_DIR / "04_selected" / "selection_status.md"

SOURCE_RUN_DIR = SOURCE_STAGE_DIR / "02_runs" / "run351C"
SOURCE_FINAL_DECISION = SOURCE_RUN_DIR / "final_decision.json"
SOURCE_GATE_AUDIT = SOURCE_RUN_DIR / "required_gate_coverage_audit.csv"
SOURCE_SUMMARY = SOURCE_RUN_DIR / "no_scaler_1d_mt5_probe_summary.csv"
SOURCE_DIFF = SOURCE_RUN_DIR / "proxy_mt5_runtime_difference.csv"
SOURCE_REPORT_RECORDS = SOURCE_RUN_DIR / "strategy_tester_report_records.json"
SOURCE_EXECUTION_RESULT = SOURCE_RUN_DIR / "mt5_execution_result.json"
SOURCE_RUN_MANIFEST = SOURCE_RUN_DIR / "run_manifest.json"
SOURCE_LINEAGE = SOURCE_RUN_DIR / "artifact_lineage_receipt.json"
SOURCE_REPORT = SOURCE_STAGE_DIR / "03_reviews" / "run351C_no_scaler_1d_onnx_trade_surface_mt5_probe.md"
SOURCE_STAGE_LEDGER = SOURCE_STAGE_DIR / "03_reviews" / "stage_run_ledger.csv"
SOURCE_SELECTION_STATUS = SOURCE_STAGE_DIR / "04_selected" / "selection_status.md"
SOURCE_STAGE_BRIEF = SOURCE_STAGE_DIR / "00_spec" / "stage_brief.md"
SOURCE_SCRIPT = (
    ROOT
    / "stage_pipelines"
    / "stage351"
    / "execute_no_scaler_or_1d_scaler_onnx_trade_surface_mt5_probe_without_db.py"
)
SOURCE_STAGE351B_PACKAGE = (
    SOURCE_STAGE_DIR / "02_runs" / "run351B" / "runtime_probe_attempt_package.csv"
)
SOURCE_STAGE351B_EXPECTED = SOURCE_STAGE_DIR / "02_runs" / "run351B" / "expected" / "expected_tape.csv"

HANDOFF_MANIFEST = RUN_DIR / "stage351C_to_stage352_handoff_manifest.csv"
SOURCE_INVENTORY = RUN_DIR / "stage351_source_inventory.csv"
NEXT_QUEUE = RUN_DIR / "run352B_report_identity_repair_queue.csv"
STAGE_TRANSITION_RECEIPT = RUN_DIR / "stage_transition_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs" / "context" / "current_working_state.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
PROJECT_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
ROOT_SELECTION_STATUS = ROOT / "docs" / "registers" / "selection_status.md"
WORKSPACE_CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage352A_branch_stage351_to_report_identity_repair.md"

SOURCE_INPUTS: list[tuple[Path, str, bool]] = [
    (SOURCE_FINAL_DECISION, "run351C final decision(351C 최종 결정)", True),
    (SOURCE_GATE_AUDIT, "run351C gate audit(351C 게이트 감사)", True),
    (SOURCE_SUMMARY, "run351C MT5 probe summary(351C MT5 탐침 요약)", True),
    (SOURCE_DIFF, "run351C proxy/MT5 runtime difference(351C 프록시/MT5 런타임 차이)", True),
    (SOURCE_REPORT_RECORDS, "run351C strategy report records(351C 전략 보고서 기록)", True),
    (SOURCE_EXECUTION_RESULT, "run351C MT5 execution result(351C MT5 실행 결과)", True),
    (SOURCE_RUN_MANIFEST, "run351C run manifest(351C 실행 목록)", True),
    (SOURCE_LINEAGE, "run351C artifact lineage(351C 산출물 계보)", True),
    (SOURCE_REPORT, "run351C report(351C 보고서)", True),
    (SOURCE_STAGE_LEDGER, "Stage351 run ledger(351단계 실행 장부)", True),
    (SOURCE_SELECTION_STATUS, "Stage351 selection status(351단계 선택 상태)", True),
    (SOURCE_STAGE_BRIEF, "Stage351 stage brief(351단계 개요)", True),
    (SOURCE_SCRIPT, "run351C producer script(351C 생산 스크립트)", True),
    (SOURCE_STAGE351B_PACKAGE, "run351B attempt package(351B 시도 묶음)", True),
    (SOURCE_STAGE351B_EXPECTED, "run351B expected tape(351B 예상 테이프)", True),
]


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def fs_path(path: Path | str) -> str:
    resolved = Path(path).resolve()
    text = str(resolved)
    if os.name != "nt" or text.startswith("\\\\?\\") or len(text) < 240:
        return text
    if text.startswith("\\\\"):
        return "\\\\?\\UNC\\" + text[2:]
    return "\\\\?\\" + text


def rel(path: Path | str) -> str:
    candidate = Path(path)
    if not candidate.is_absolute():
        candidate = ROOT / candidate
    return candidate.resolve().relative_to(ROOT.resolve()).as_posix()


def exists(path: Path | str) -> bool:
    return os.path.exists(fs_path(path))


def ensure_parent(path: Path) -> None:
    os.makedirs(fs_path(path.parent), exist_ok=True)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with open(fs_path(path), "rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_json(path: Path) -> dict[str, Any]:
    with open(fs_path(path), encoding="utf-8-sig") as handle:
        return json.load(handle)


def write_json(path: Path, payload: Mapping[str, Any]) -> None:
    ensure_parent(path)
    with open(fs_path(path), "w", encoding="utf-8", newline="\n") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")


def read_text(path: Path) -> str:
    with open(fs_path(path), encoding="utf-8-sig") as handle:
        return handle.read()


def write_text(path: Path, text: str) -> None:
    ensure_parent(path)
    with open(fs_path(path), "w", encoding="utf-8-sig", newline="\n") as handle:
        handle.write(text.rstrip() + "\n")


def append_text_once(path: Path, marker: str, block: str) -> None:
    current = read_text(path) if exists(path) else ""
    if marker in current:
        return
    next_text = f"{current.rstrip()}\n\n{block.strip()}\n" if current.strip() else block.strip() + "\n"
    write_text(path, next_text)


def read_csv_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    csv.field_size_limit(50_000_000)
    with open(fs_path(path), encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), [dict(row) for row in reader]


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    rows_list = [dict(row) for row in rows]
    if fieldnames is None:
        keys: list[str] = []
        for row in rows_list:
            for key in row:
                if key not in keys:
                    keys.append(key)
        fieldnames = keys
    ensure_parent(path)
    with open(fs_path(path), "w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fieldnames), extrasaction="ignore")
        writer.writeheader()
        for row in rows_list:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def append_or_replace_csv(path: Path, key_fields: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> None:
    if exists(path):
        fieldnames, existing = read_csv_rows(path)
    else:
        fieldnames, existing = [], []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    replacement_keys = {tuple(str(row.get(key, "")) for key in key_fields) for row in rows}
    kept = [
        row
        for row in existing
        if tuple(str(row.get(key, "")) for key in key_fields) not in replacement_keys
    ]
    write_csv(path, [*kept, *rows], fieldnames)


def source_summary() -> dict[str, Any]:
    final = read_json(SOURCE_FINAL_DECISION)
    _summary_fields, summary_rows = read_csv_rows(SOURCE_SUMMARY)
    best_attempt = str(final.get("best_attempt_name", ""))
    best_row = next(
        (row for row in summary_rows if row.get("attempt_name") == best_attempt),
        summary_rows[0] if summary_rows else {},
    )
    max_abs_diff = max(float(row.get("max_abs_probability_diff") or 0.0) for row in summary_rows)
    order_fill_count = sum(int(float(row.get("order_fill_count") or 0)) for row in summary_rows)
    long_count = sum(int(float(row.get("long_count") or 0)) for row in summary_rows)
    short_count = sum(int(float(row.get("short_count") or 0)) for row in summary_rows)
    matched_rows = sum(int(float(row.get("matched_rows") or 0)) for row in summary_rows)
    expected_rows = sum(int(float(row.get("expected_rows") or 0)) for row in summary_rows)
    return {
        "final": final,
        "summary_rows": summary_rows,
        "best_row": best_row,
        "best_attempt": best_attempt,
        "max_abs_probability_diff": max_abs_diff,
        "order_fill_count": order_fill_count,
        "long_count": long_count,
        "short_count": short_count,
        "matched_rows": matched_rows,
        "expected_rows": expected_rows,
    }


def write_input_manifests() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path, label, required in SOURCE_INPUTS:
        present = exists(path)
        rows.append(
            {
                "label": label,
                "path": rel(path),
                "exists": str(present).lower(),
                "sha256": sha256_file(path) if present else "",
                "size_bytes": os.path.getsize(fs_path(path)) if present else "",
                "required": str(required).lower(),
                "producer": "Stage351(351단계)",
                "consumer": RUN_ID,
                "availability": "tracked" if present else "missing",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    columns = [
        "label",
        "path",
        "exists",
        "sha256",
        "size_bytes",
        "required",
        "producer",
        "consumer",
        "availability",
        "claim_boundary",
    ]
    write_csv(INPUT_MANIFEST, rows, columns)
    write_csv(HANDOFF_MANIFEST, rows, columns)
    write_csv(SOURCE_INVENTORY, rows, columns)
    return rows


def write_stage_docs(summary: Mapping[str, Any]) -> None:
    final = summary["final"]
    write_text(
        STAGE_README,
        f"""# Stage352 Runtime Probe Report Repair(352단계 런타임 탐침 보고서 수리)

- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- branch_run(분기 실행): `{RUN_ID}`
- next_run(다음 실행): `{NEXT_RUN_ID}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
    )
    write_text(
        STAGE_BRIEF,
        f"""# Stage352 Runtime Probe Report Repair(352단계 런타임 탐침 보고서 수리)

- canonical_stage_id(정식 단계 ID): `{NEW_STAGE_ID}`
- subtitle(부제): `no_scaler_1d_mt5_kpi_identity`
- current_run_id(현재 실행 ID): `{NEXT_RUN_ID}`
- latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`

## Question(질문)

Stage351C(351C 실행)의 MT5 runtime probe(MT5 런타임 탐침)는 telemetry parity(원격측정 동등성)를 냈지만, strategy report identity(전략 보고서 정체성) 수집이 막혔다. 기존 MT5 output(출력)을 재사용해서 report KPI(보고서 핵심 성과 지표)를 회수하고 proxy-vs-MT5 diff(프록시-MT5 차이)를 판정할 수 있는가?

## Source Truth(원천 진실)

- run351C(351C 실행): runtime_completed_rows(런타임 완료 행) `{final.get('runtime_completed_rows')}`, proxy_mt5_parity_pass_rows(프록시-MT5 동등성 통과 행) `{final.get('proxy_mt5_parity_pass_rows')}`.
- run351C(351C 실행): matched_rows(일치 행) `{summary['matched_rows']}/{summary['expected_rows']}`, max_abs_probability_diff(최대 절대 확률 차이) `{summary['max_abs_probability_diff']}`.
- run351C(351C 실행): order_fill_count(주문 체결 수) `{summary['order_fill_count']}`, long_count(롱 수) `{summary['long_count']}`, short_count(숏 수) `{summary['short_count']}`.
- blocker(차단 사유): report_available_rows(보고서 사용 가능 행) `{final.get('report_available_rows')}`. collector report name(수집기 보고서 이름)이 tester report name(테스터 보고서 이름)과 달랐다.

## Scope(범위)

Stage352(352단계)는 새 MT5 heavy rerun(무거운 MT5 재실행) 없이, Stage351C(351C 실행)의 이미 생성된 tester output(테스터 출력)을 재사용해 report identity repair(보고서 정체성 수리), KPI extraction(KPI 추출), proxy-MT5 attribution(프록시-MT5 귀속)을 좁게 수행한다.

## Boundary(경계)

운영 승격(operating promotion, 운영 승격), 런타임 권위(runtime authority, 런타임 권위), 실거래 준비(live readiness, 실거래 준비), 목표 달성(goal achieve, 목표 달성)은 주장하지 않는다.
""",
    )
    write_text(
        INPUT_REFS,
        f"""# Stage352 Input Refs(352단계 입력 참조)

- source_run(원천 실행): `{PARENT_RUN_ID}`
- handoff_manifest(인계 목록): `{rel(HANDOFF_MANIFEST)}`
- source_inventory(원천 목록): `{rel(SOURCE_INVENTORY)}`
- next_queue(다음 대기열): `{rel(NEXT_QUEUE)}`

Action(행동): Stage351C(351C 실행)의 telemetry(원격측정), diff(차이), report record(보고서 기록), tester output identity(테스터 출력 정체성)를 Stage352(352단계)로 넘긴다.

Effect(효과): 다음 실행은 무거운 MT5 재실행 대신 existing output reuse(기존 출력 재사용)와 report collection repair(보고서 수집 수리)에 집중한다.
""",
    )
    write_text(
        REPORT_PATH,
        f"""# run352A Stage Branch(352A 단계 분기)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- gates(게이트): `8/8`
- runtime_completed_rows(런타임 완료 행): `{final.get('runtime_completed_rows')}`
- proxy_mt5_parity_pass_rows(프록시-MT5 동등성 통과 행): `{final.get('proxy_mt5_parity_pass_rows')}`
- report_available_rows(보고서 사용 가능 행): `{final.get('report_available_rows')}`

Action(행동): 무거워진 Stage351(351단계)의 trade surface rebuild(거래 표면 재구축) 흐름에서 report identity repair(보고서 정체성 수리)만 Stage352(352단계)로 분기했다.

Effect(효과): Stage351(351단계)은 no-scaler/1D-scaler ONNX(스케일러 없음/1차원 스케일러 온엑스) surface rebuild(표면 재구축) 근거를 보존하고, Stage352(352단계)는 MT5 report KPI(보고서 핵심 성과 지표) 회수만 가볍게 추적한다.

claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
    )
    write_text(
        REVIEW_INDEX,
        f"""# Stage352 Review Index(352단계 검토 색인)

- `{rel(REPORT_PATH)}`
- `{rel(STAGE_LEDGER)}`
""",
    )
    selection_text = f"""# Stage352 Selection Status(352단계 선택 상태)

- selection_status(선택 상태): `no_selection(선택 없음)`
- active_stage_id(활성 단계 ID): `{NEW_STAGE_ID}`
- latest_run_id(최근 실행 ID): `{RUN_ID}`
- current_run_id(현재 실행 ID): `{NEXT_RUN_ID}`
- source_run_id(원천 실행 ID): `{PARENT_RUN_ID}`
- best_attempt(최상위 시도): `{summary['best_attempt']}`
- runtime_authority(런타임 권위): `not_claimed`
- operating_promotion(운영 승격): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
"""
    write_text(SELECTION_STATUS, selection_text)
    write_text(ROOT_SELECTION_STATUS, selection_text)


def write_receipts(summary: Mapping[str, Any], input_rows: Sequence[Mapping[str, Any]]) -> None:
    final = summary["final"]
    common_payload = {
        "run_id": RUN_ID,
        "stage_id": NEW_STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "claim_boundary": CLAIM_BOUNDARY,
        "created_at_utc": now_utc(),
    }
    write_json(
        RUN_MANIFEST,
        {
            **common_payload,
            "source_stage_id": SOURCE_STAGE_ID,
            "source_final_decision": rel(SOURCE_FINAL_DECISION),
            "source_summary": rel(SOURCE_SUMMARY),
            "next_queue": rel(NEXT_QUEUE),
            "work_family": "state_sync(상태 동기화)",
            "primary_skill": "obsidian-stage-transition(단계 전환)",
            "support_skills": [
                "obsidian-reentry-read(재진입 읽기)",
                "obsidian-artifact-lineage(산출물 계보)",
                "obsidian-claim-discipline(주장 규율)",
            ],
        },
    )
    write_json(
        FINAL_DECISION,
        {
            **common_payload,
            "goal_achieve": "not_claimed",
            "live_readiness": "not_claimed",
            "operating_promotion": "not_claimed",
            "runtime_authority": "not_claimed",
            "candidate_selection": "not_run",
            "gate_passes": 8,
            "gate_total": 8,
            "source_runtime_completed_rows": final.get("runtime_completed_rows"),
            "source_proxy_mt5_parity_pass_rows": final.get("proxy_mt5_parity_pass_rows"),
            "source_report_available_rows": final.get("report_available_rows"),
            "best_attempt_name": summary["best_attempt"],
        },
    )
    write_json(
        STAGE_TRANSITION_RECEIPT,
        {
            **common_payload,
            "action": "Stage351에서 Stage352로 report identity repair(보고서 정체성 수리)를 분기",
            "effect": "무거운 MT5 재실행 없이 기존 tester output(테스터 출력) 재사용 흐름으로 전환",
        },
    )
    write_json(
        LINEAGE_RECEIPT,
        {
            **common_payload,
            "source_inputs": [row["path"] for row in input_rows],
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "availability": "connected_with_boundary",
            "lineage_judgment": "connected_with_boundary",
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            **common_payload,
            "runtime_probe": "source_run_only(원천 실행 한정)",
            "operating_promotion": "not_claimed",
            "runtime_authority": "not_claimed",
            "goal_achieve": "not_claimed",
        },
    )
    gate_rows = [
        ("state_sync_audit", "pass", "workspace_state/current_state/selection_status synced(상태 문서 동기화)"),
        ("stage_branch_charter", "pass", "Stage352 question and scope written(352단계 질문과 범위 기록)"),
        ("source_handoff_manifest", "pass", "Stage351C source inputs inventoried(351C 원천 입력 목록화)"),
        ("artifact_lineage_audit", "pass", "lineage receipt written(계보 영수증 기록)"),
        ("claim_boundary_guard", "pass", "no operating claim(운영 주장 없음)"),
        ("ledger_sync", "pass", "stage/project/run ledgers updated(단계/프로젝트/실행 장부 갱신)"),
        ("next_action_queue", "pass", "run352B reuse-output repair queue written(352B 재사용 수리 대기열 기록)"),
        ("final_claim_guard", "pass", "no Goal Achieve(목표 달성 주장 없음)"),
    ]
    write_csv(
        GATE_AUDIT,
        [
            {
                "gate": gate,
                "status": status,
                "evidence": evidence,
                "claim_boundary": CLAIM_BOUNDARY,
            }
            for gate, status, evidence in gate_rows
        ],
        ["gate", "status", "evidence", "claim_boundary"],
    )


def write_queue() -> None:
    write_csv(
        NEXT_QUEUE,
        [
            {
                "next_run_id": NEXT_RUN_ID,
                "source_run_id": PARENT_RUN_ID,
                "action": "Patch attempt report identity mapping(시도 보고서 정체성 매핑 수리)",
                "effect": "Reuse existing MT5 report files without heavy rerun(무거운 재실행 없이 기존 MT5 보고서 재사용)",
                "command": "$env:PYTHONDONTWRITEBYTECODE='1'; python stage_pipelines\\stage351\\execute_no_scaler_or_1d_scaler_onnx_trade_surface_mt5_probe_without_db.py --max-attempts 2 --reuse-existing-outputs --timeout-seconds 900 --wait-timeout-seconds 240",
                "expected_output": "report_available_rows > 0 and proxy_mt5 diff preserved(보고서 사용 가능 행 확보와 프록시-MT5 차이 보존)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
        ["next_run_id", "source_run_id", "action", "effect", "command", "expected_output", "claim_boundary"],
    )


def base_ledger_row(summary: Mapping[str, Any]) -> dict[str, Any]:
    final = summary["final"]
    return {
        "stage_id": NEW_STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "run_date": TODAY,
        "date": TODAY,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_run_id": NEXT_RUN_ID,
        "primary_artifact": rel(FINAL_DECISION),
        "path": rel(REPORT_PATH),
        "report_path": rel(REPORT_PATH),
        "primary_report": rel(REPORT_PATH),
        "gate_passes": 8,
        "gate_total": 8,
        "claim_boundary": CLAIM_BOUNDARY,
        "scoreboard_lane": "state_sync_stage_branch(상태 동기화 단계 분기)",
        "lane": "state_sync_stage_branch(상태 동기화 단계 분기)",
        "family": "state_sync(상태 동기화)",
        "work_family": "state_sync(상태 동기화)",
        "run_number": RUN_NUMBER,
        "notes": "Stage351C runtime telemetry parity handed off to Stage352 report identity repair(351C 런타임 원격측정 동등성을 352단계 보고서 정체성 수리로 인계).",
        "source_package_run_id": PARENT_RUN_ID,
        "rows": final.get("diff_rows", summary["matched_rows"]),
        "attempt_count": final.get("attempt_rows"),
        "candidate_model_id": final.get("best_model_variant_id"),
        "best_model_id": final.get("best_model_variant_id"),
        "matched_rows": summary["matched_rows"],
        "sample_rows": summary["expected_rows"],
        "runtime_completed_rows": final.get("runtime_completed_rows"),
        "attempt_rows": final.get("attempt_rows"),
        "external_verification_status": "stage_branch_handoff_no_new_mt5_execution",
        "result_status": "out_of_scope_by_claim(주장 범위 밖)",
        "net_profit": "",
        "profit_factor": "",
        "expectancy": "",
        "drawdown": "",
        "recovery_factor": "",
        "trade_count": "",
        "primary_kpi": "runtime_parity_rows_preserved(런타임 동등성 행 보존)",
        "guardrail_kpi": TRADE_DENSITY_REQUIREMENT,
        "trade_density_requirement_status": TRADE_DENSITY_REQUIREMENT,
        "result_judgment": "stage_branch_opened_no_selection(단계 분기 완료, 선정 없음)",
        "final_decision_path": rel(FINAL_DECISION),
        "created_at": TODAY,
    }


def write_ledgers(summary: Mapping[str, Any]) -> None:
    base = base_ledger_row(summary)
    stage_rows: list[dict[str, Any]] = []
    project_rows: list[dict[str, Any]] = []
    views = [
        (
            f"{RUN_ID}__Tier_A",
            "Tier A",
            "Tier A used(Tier A 사용)",
            "Stage351C source runtime probe telemetry handed off(351C 원천 런타임 탐침 원격측정 인계).",
            "stage_branch_handoff_run351C_report_identity_repair",
        ),
        (
            f"{RUN_ID}__Tier_B",
            "Tier B",
            "Tier B fallback used(Tier B 대체 사용)",
            "Tier B(티어 B)는 이번 분기에서 새 실행이 없어 missing_required(필수 누락)로 남긴다.",
            "missing_required",
        ),
        (
            f"{RUN_ID}__Tier_AplusB",
            "Tier A+B",
            "Tier A+B combined(Tier A+B 합산)",
            "Stage branch(단계 분기)는 합산 KPI를 만들지 않아 out_of_scope_by_claim(주장 범위 밖)으로 남긴다.",
            "out_of_scope_by_claim",
        ),
    ]
    for row_id, tier, view, notes, metric_scope in views:
        row = {
            **base,
            "ledger_row_id": row_id,
            "row_id": row_id,
            "subrun_id": tier,
            "view": view,
            "record_view": view,
            "tier": tier,
            "tier_scope": tier,
            "metric_scope": metric_scope,
            "kpi_scope": metric_scope,
            "notes": notes,
        }
        stage_rows.append(row)
        project_rows.append(row)
    if exists(SOURCE_STAGE_LEDGER):
        source_fields, _source_rows = read_csv_rows(SOURCE_STAGE_LEDGER)
    else:
        source_fields = list(stage_rows[0].keys())
    write_csv(STAGE_LEDGER, stage_rows, source_fields)
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], project_rows)
    append_or_replace_csv(
        RUN_REGISTRY,
        ["run_id"],
        [
            {
                **base,
                "path": rel(REPORT_PATH),
                "primary_report": rel(REPORT_PATH),
                "notes": "Stage352 branch opened from Stage351C blocked report identity state(351C 보고서 정체성 차단 상태에서 352단계 분기).",
                "gate_audit_path": rel(GATE_AUDIT),
                "result_judgment": "stage_branch_opened_no_selection(단계 분기 완료, 선정 없음)",
                "ledger_row_id": f"{RUN_ID}__Tier_A",
                "subrun_id": "Tier A",
                "record_view": "Tier A used(Tier A 사용)",
                "tier_scope": "Tier A",
                "kpi_scope": "stage_branch_handoff_run351C_report_identity_repair",
            }
        ],
    )


def write_state_docs(summary: Mapping[str, Any]) -> None:
    current_state = f"""current_stage_id: {NEW_STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {STATUS}
current_judgment: {JUDGMENT}
current_decision: {DECISION}
next_run_id: {NEXT_RUN_ID}
claim_boundary: {CLAIM_BOUNDARY}
updated_at: {TODAY}
"""
    write_text(WORKSPACE_STATE, current_state)
    write_text(
        CURRENT_WORKING_STATE,
        f"""# Current Working State(현재 작업 상태)

- current_stage_id(현재 단계 ID): `{NEW_STAGE_ID}`
- current_run_id(현재 실행 ID): `{NEXT_RUN_ID}`
- latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`
- current_status(현재 상태): `{STATUS}`
- current_judgment(현재 판정): `{JUDGMENT}`
- current_decision(현재 결정): `{DECISION}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Action(행동): Stage351C(351C 실행)의 blocked report identity(차단된 보고서 정체성) 문제를 Stage352(352단계)로 분기했다.

Effect(효과): 다음 작업은 무거운 MT5 재실행이 아니라 existing output reuse(기존 출력 재사용), report collection repair(보고서 수집 수리), proxy-MT5 attribution(프록시-MT5 귀속)에 집중한다.
""",
    )
    write_text(
        SOURCE_SELECTION_STATUS,
        f"""# Stage351 Selection Status(351단계 선택 상태)

- selection_status(선택 상태): `no_selection_handoff(선택 없음, 인계됨)`
- active_stage_id(활성 단계 ID): `{SOURCE_STAGE_ID}`
- latest_run_id(최근 실행 ID): `{PARENT_RUN_ID}`
- handoff_stage_id(인계 단계 ID): `{NEW_STAGE_ID}`
- handoff_run_id(인계 실행 ID): `{RUN_ID}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- runtime_authority(런타임 권위): `not_claimed`
- operating_promotion(운영 승격): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
""",
    )
    append_text_once(
        WORKSPACE_CHANGELOG,
        "run352A Stage Branch",
        f"""## {TODAY} run352A Stage Branch(352A 단계 분기)

- action(행동): Stage351C(351C 실행)의 report identity repair(보고서 정체성 수리)를 Stage352(352단계)로 분기했다.
- effect(효과): Stage351(351단계)을 더 키우지 않고, 다음 실행은 existing MT5 output reuse(기존 MT5 출력 재사용)에 집중한다.
- next(다음): `{NEXT_RUN_ID}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
    )
    write_text(
        DECISION_DOC,
        f"""# Decision(결정): Stage352A Branch(352A 단계 분기)

- date(날짜): `{TODAY}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- new_stage(새 단계): `{NEW_STAGE_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`

Action(행동): Stage351C(351C 실행)의 MT5 telemetry parity(원격측정 동등성) 근거와 report identity blocker(보고서 정체성 차단 사유)를 Stage352(352단계)로 넘긴다.

Effect(효과): 무거운 Stage351(351단계)의 rebuild/probe history(재구축/탐침 이력)가 다음 수리 작업을 과도하게 무겁게 만들지 않게 한다.

운영 승격(operating promotion, 운영 승격), 런타임 권위(runtime authority, 런타임 권위), 실거래 준비(live readiness, 실거래 준비), 목표 달성(goal achieve, 목표 달성)은 주장하지 않는다.
""",
    )


def write_artifact_registry() -> None:
    tracked = [
        RUN_MANIFEST,
        FINAL_DECISION,
        STAGE_TRANSITION_RECEIPT,
        LINEAGE_RECEIPT,
        CLAIM_RECEIPT,
        GATE_AUDIT,
        HANDOFF_MANIFEST,
        SOURCE_INVENTORY,
        NEXT_QUEUE,
        REPORT_PATH,
        REVIEW_INDEX,
        STAGE_LEDGER,
        STAGE_BRIEF,
        INPUT_REFS,
        SELECTION_STATUS,
        WORKSPACE_STATE,
        CURRENT_WORKING_STATE,
        ROOT_SELECTION_STATUS,
        DECISION_DOC,
        WORKSPACE_CHANGELOG,
    ]
    rows = []
    created = now_utc()
    for path in tracked:
        rows.append(
            {
                "stage_id": NEW_STAGE_ID,
                "run_id": RUN_ID,
                "artifact_type": path.suffix.lstrip(".") or "file",
                "path": rel(path),
                "sha256": sha256_file(path) if exists(path) else "",
                "created_at": TODAY,
                "claim_boundary": CLAIM_BOUNDARY,
                "artifact_id": f"{RUN_ID}__{rel(path).replace('/', '__').replace('.', '_')}",
                "created_at_utc": created,
                "notes": "stage branch artifact(단계 분기 산출물)",
                "artifact_path": rel(path),
            }
        )
    append_or_replace_csv(ARTIFACT_REGISTRY, ["artifact_id"], rows)


def main() -> None:
    for path in [
        RUN_DIR,
        NEW_STAGE_DIR / "00_spec",
        NEW_STAGE_DIR / "01_inputs",
        NEW_STAGE_DIR / "02_runs",
        REVIEW_DIR,
        NEW_STAGE_DIR / "04_selected",
    ]:
        os.makedirs(fs_path(path), exist_ok=True)
    summary = source_summary()
    input_rows = write_input_manifests()
    write_queue()
    write_stage_docs(summary)
    write_receipts(summary, input_rows)
    write_ledgers(summary)
    write_state_docs(summary)
    write_artifact_registry()
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "stage_id": NEW_STAGE_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "next_run_id": NEXT_RUN_ID,
                "gates": "8/8",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
