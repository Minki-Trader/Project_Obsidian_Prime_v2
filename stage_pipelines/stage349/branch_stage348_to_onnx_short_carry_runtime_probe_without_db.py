from __future__ import annotations

import csv
import hashlib
import json
import os
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[2]
TODAY = "2026-06-01"

SOURCE_STAGE_ID = "348_cash_open_proxy_review__long_oos_gap_short_carry_triage"
NEW_STAGE_ID = "349_onnx_short_carry_runtime__execute_mt5_probe"
SOURCE_STAGE_DIR = ROOT / "stages" / SOURCE_STAGE_ID
NEW_STAGE_DIR = ROOT / "stages" / NEW_STAGE_ID

RUN_NUMBER = "run349A"
RUN_ID = "run349A_branch_stage348_to_onnx_short_carry_runtime_probe_without_db_v1"
PARENT_RUN_ID = "run348C_materialize_onnx_deployable_short_carry_probe_package_without_db_v1"
SUPERSEDED_RUN_ID = "run348D_execute_onnx_deployable_short_carry_mt5_probe_without_db_v1"
NEXT_RUN_ID = "run349B_execute_onnx_deployable_short_carry_mt5_probe_without_db_v1"

STATUS = "completed_stage349A_branch_from_stage348_onnx_short_carry_runtime_probe_opened_no_selection"
JUDGMENT = "stage_branch_completed_stage348_overweight_package_handoff_to_stage349_runtime_probe_no_operating_claim"
DECISION = "stage349A_open_run349B_execute_onnx_deployable_short_carry_mt5_probe"
CLAIM_BOUNDARY = (
    "state_sync_stage_branch_onnx_short_carry_runtime_probe_handoff_only_"
    "no_new_mt5_execution_no_candidate_selection_no_forward_pass_no_live_readiness_"
    "no_operating_promotion_no_runtime_authority_no_goal_claim"
)
TRADE_DENSITY_REQUIREMENT = "trade_per_day_min_3_to_10_plus_no_trade_splitting"

RUN_DIR = NEW_STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = NEW_STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEW_DIR / "run349A_stage_branch.md"
REVIEW_INDEX = REVIEW_DIR / "review_index.md"
STAGE_BRIEF = NEW_STAGE_DIR / "00_spec" / "stage_brief.md"
STAGE_README = NEW_STAGE_DIR / "README.md"
INPUT_REFS = NEW_STAGE_DIR / "01_inputs" / "input_refs.md"
INPUT_MANIFEST = NEW_STAGE_DIR / "01_inputs" / "stage349_input_manifest.csv"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"
SELECTION_STATUS = NEW_STAGE_DIR / "04_selected" / "selection_status.md"

SOURCE_RUN_DIR = SOURCE_STAGE_DIR / "02_runs" / "run348C"
SOURCE_FINAL_DECISION = SOURCE_RUN_DIR / "final_decision.json"
SOURCE_GATE_AUDIT = SOURCE_RUN_DIR / "required_gate_coverage_audit.csv"
SOURCE_ATTEMPT_PACKAGE = SOURCE_RUN_DIR / "runtime_probe_attempt_package.csv"
SOURCE_QUEUE = SOURCE_RUN_DIR / "run348D_queue.csv"
SOURCE_EXPECTED_TAPE = SOURCE_RUN_DIR / "expected" / "expected_tape.csv"
SOURCE_EXPECTED_INDEX = SOURCE_RUN_DIR / "expected_tape_index.csv"
SOURCE_RUNTIME_PARITY = SOURCE_RUN_DIR / "runtime_parity_contract.csv"
SOURCE_TESTER_IDENTITY = SOURCE_RUN_DIR / "tester_identity_contract.csv"
SOURCE_MAPPING_AUDIT = SOURCE_RUN_DIR / "runtime_mapping_audit.csv"
SOURCE_PROXY_COMPARISON = SOURCE_RUN_DIR / "proxy_mt5_comparison_contract.csv"
SOURCE_COMMON_SYNC = SOURCE_RUN_DIR / "common_files_sync.csv"
SOURCE_MODEL_MANIFEST = SOURCE_RUN_DIR / "model_handoff_manifest.csv"
SOURCE_SET_MANIFEST = SOURCE_RUN_DIR / "tester_set_manifest.csv"
SOURCE_INI_MANIFEST = SOURCE_RUN_DIR / "tester_ini_manifest.csv"
SOURCE_REPORT = SOURCE_STAGE_DIR / "03_reviews" / "run348C_onnx_deployable_short_carry_probe_package.md"
SOURCE_SELECTION_STATUS = SOURCE_STAGE_DIR / "04_selected" / "selection_status.md"
SOURCE_REVIEW_INDEX = SOURCE_STAGE_DIR / "03_reviews" / "review_index.md"
SOURCE_STAGE_BRIEF = SOURCE_STAGE_DIR / "00_spec" / "stage_brief.md"

HANDOFF_MANIFEST = RUN_DIR / "stage348C_to_stage349_handoff_manifest.csv"
SOURCE_INVENTORY = RUN_DIR / "stage348_source_inventory.csv"
NEXT_QUEUE = RUN_DIR / "run349B_onnx_short_carry_mt5_probe_queue.csv"
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
ROOT_CHANGELOG = ROOT / "CHANGELOG.md"
WORKSPACE_CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage349A_branch_stage348_to_onnx_short_carry_runtime_probe.md"

SOURCE_INPUTS = [
    (SOURCE_FINAL_DECISION, "run348C final decision(348C 최종 결정)"),
    (SOURCE_GATE_AUDIT, "run348C required gate audit(348C 필수 게이트 감사)"),
    (SOURCE_ATTEMPT_PACKAGE, "run348C runtime probe package(348C 런타임 탐침 패키지)"),
    (SOURCE_QUEUE, "run348D source queue(348D 원천 대기열)"),
    (SOURCE_EXPECTED_TAPE, "expected tape(예상 테이프)"),
    (SOURCE_EXPECTED_INDEX, "expected tape index(예상 테이프 인덱스)"),
    (SOURCE_RUNTIME_PARITY, "runtime parity contract(런타임 동등성 계약)"),
    (SOURCE_TESTER_IDENTITY, "tester identity contract(테스터 정체성 계약)"),
    (SOURCE_MAPPING_AUDIT, "runtime mapping audit(런타임 매핑 감사)"),
    (SOURCE_PROXY_COMPARISON, "proxy MT5 comparison contract(프록시 MT5 비교 계약)"),
    (SOURCE_COMMON_SYNC, "common files sync(공용 파일 동기화)"),
    (SOURCE_MODEL_MANIFEST, "model handoff manifest(모델 인계 목록)"),
    (SOURCE_SET_MANIFEST, "tester set manifest(테스터 set 목록)"),
    (SOURCE_INI_MANIFEST, "tester ini manifest(테스터 ini 목록)"),
    (SOURCE_REPORT, "run348C package report(348C 패키지 보고서)"),
]

LEDGER_COLUMNS = [
    "stage_id",
    "run_id",
    "parent_run_id",
    "run_date",
    "date",
    "status",
    "judgment",
    "decision",
    "next_run_id",
    "primary_artifact",
    "path",
    "report_path",
    "primary_report",
    "gate_passes",
    "gate_total",
    "claim_boundary",
    "scoreboard_lane",
    "lane",
    "family",
    "run_number",
    "notes",
    "source_package_run_id",
    "rows",
    "attempt_count",
    "feature_count",
    "candidate_model_id",
    "ledger_row_id",
    "subrun_id",
    "view",
    "record_view",
    "tier",
    "tier_scope",
    "metric_scope",
    "kpi_scope",
    "primary_kpi",
    "guardrail_kpi",
    "external_verification_status",
    "result_status",
    "net_profit",
    "profit_factor",
    "expectancy",
    "drawdown",
    "recovery_factor",
    "trade_count",
    "matched_rows",
    "sample_rows",
]


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def fs_path(path: Path | str) -> str:
    candidate = Path(path)
    resolved = candidate.resolve()
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


def required(path: Path) -> Path:
    if not exists(path):
        raise FileNotFoundError(f"missing required input(필수 입력 누락): {rel(path)}")
    return path


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


def write_plain_text(path: Path, text: str) -> None:
    ensure_parent(path)
    with open(fs_path(path), "w", encoding="utf-8", newline="\n") as handle:
        handle.write(text.rstrip() + "\n")


def append_text_once(path: Path, marker: str, text: str) -> None:
    current = read_text(path) if exists(path) else ""
    if marker in current:
        return
    next_text = f"{current.rstrip()}\n\n{text.strip()}\n" if current.strip() else text.strip() + "\n"
    write_text(path, next_text)


def read_csv_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    csv.field_size_limit(10_000_000)
    with open(fs_path(path), encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), [dict(row) for row in reader]


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
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


def append_or_replace_csv(path: Path, key_columns: Sequence[str], rows: Iterable[Mapping[str, Any]]) -> None:
    rows_list = [dict(row) for row in rows]
    if exists(path):
        fieldnames, existing = read_csv_rows(path)
    else:
        fieldnames, existing = [], []
    for row in rows_list:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    replacement_keys = {tuple(str(row.get(key, "")) for key in key_columns) for row in rows_list}
    kept = [
        row
        for row in existing
        if tuple(str(row.get(key, "")) for key in key_columns) not in replacement_keys
    ]
    write_csv(path, kept + rows_list, fieldnames)


def unique_fieldnames(*groups: Sequence[str]) -> list[str]:
    fields: list[str] = []
    for group in groups:
        for field in group:
            if field not in fields:
                fields.append(field)
    return fields


def source_gate_passed() -> bool:
    _fields, rows = read_csv_rows(required(SOURCE_GATE_AUDIT))
    return bool(rows) and all(row.get("status") == "passed" for row in rows)


def source_summary() -> dict[str, Any]:
    decision = read_json(required(SOURCE_FINAL_DECISION))
    _queue_fields, queue_rows = read_csv_rows(required(SOURCE_QUEUE))
    _attempt_fields, attempt_rows = read_csv_rows(required(SOURCE_ATTEMPT_PACKAGE))
    return {
        "source_status": decision["status"],
        "source_judgment": decision["judgment"],
        "source_decision": decision["decision"],
        "source_gate_passes": int(decision["gate_passes"]),
        "source_gate_total": int(decision["gate_total"]),
        "attempt_count": int(decision.get("attempt_count") or len(attempt_rows)),
        "queue_rows": len(queue_rows),
        "expected_rows": int(decision.get("expected_rows") or 0),
        "feature_rows": int(decision.get("feature_rows") or 0),
        "feature_count": int(decision.get("feature_count") or 0),
        "missing_mt5_contract_feature_count": int(decision.get("missing_mt5_contract_feature_count") or 0),
        "cash_open_partial_mapping_attempts": int(decision.get("cash_open_partial_mapping_attempts") or 0),
        "proxy_ea_expected_mismatch_rows": int(decision.get("proxy_ea_expected_mismatch_rows") or 0),
        "common_sync_missing": int(decision.get("common_sync_missing") or 0),
        "model_hash_matched_rows": int(decision.get("model_hash_matched_rows") or 0),
        "source_package_run_id": decision.get("source_package_run_id", ""),
        "source_training_run_id": decision.get("source_training_run_id", ""),
        "source_runtime_run_id": decision.get("source_runtime_run_id", ""),
    }


def write_source_inventory() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path, label in SOURCE_INPUTS:
        path_exists = exists(path)
        rows.append(
            {
                "source_label": label,
                "path": rel(path),
                "exists": str(path_exists).lower(),
                "sha256": sha256_file(path) if path_exists else "",
                "bytes": os.path.getsize(fs_path(path)) if path_exists else "",
                "consumer": RUN_ID,
                "availability": "tracked" if path_exists else "missing",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(INPUT_MANIFEST, rows)
    write_csv(SOURCE_INVENTORY, rows)
    return rows


def write_handoff_artifacts(summary: Mapping[str, Any]) -> list[dict[str, Any]]:
    queue_fields, queue_rows = read_csv_rows(required(SOURCE_QUEUE))
    extras = [
        "source_queue_id",
        "source_next_run_id",
        "source_stage_id",
        "new_stage_id",
        "handoff_run_id",
        "superseded_run_id",
        "retarget_status",
        "source_claim_boundary",
        "handoff_claim_boundary",
    ]
    retargeted: list[dict[str, Any]] = []
    for row in queue_rows:
        updated = dict(row)
        updated["source_queue_id"] = row.get("queue_id", "")
        updated["source_next_run_id"] = row.get("next_run_id", "")
        updated["next_run_id"] = NEXT_RUN_ID
        updated["source_stage_id"] = SOURCE_STAGE_ID
        updated["new_stage_id"] = NEW_STAGE_ID
        updated["handoff_run_id"] = RUN_ID
        updated["superseded_run_id"] = SUPERSEDED_RUN_ID
        updated["retarget_status"] = "retargeted_to_stage349(349단계로 재지정)"
        updated["source_claim_boundary"] = row.get("claim_boundary", "")
        updated["handoff_claim_boundary"] = CLAIM_BOUNDARY
        updated["claim_boundary"] = CLAIM_BOUNDARY
        retargeted.append(updated)
    write_csv(NEXT_QUEUE, retargeted, unique_fieldnames(queue_fields, extras))
    write_csv(
        HANDOFF_MANIFEST,
        [
            {
                "handoff_id": "stage348C_to_stage349A_branch",
                "source_stage_id": SOURCE_STAGE_ID,
                "source_run_id": PARENT_RUN_ID,
                "new_stage_id": NEW_STAGE_ID,
                "branch_run_id": RUN_ID,
                "superseded_run_id": SUPERSEDED_RUN_ID,
                "next_run_id": NEXT_RUN_ID,
                "source_queue_path": rel(SOURCE_QUEUE),
                "retargeted_queue_path": rel(NEXT_QUEUE),
                "attempt_count": summary["attempt_count"],
                "expected_rows": summary["expected_rows"],
                "feature_rows": summary["feature_rows"],
                "feature_count": summary["feature_count"],
                "common_sync_missing": summary["common_sync_missing"],
                "cash_open_partial_mapping_attempts": summary["cash_open_partial_mapping_attempts"],
                "branch_reason": (
                    "Stage348(348단계)이 proxy review(프록시 검토), package materialization(패키지 물질화), "
                    "runtime queue(런타임 대기열)까지 담아 무거워졌다."
                ),
                "effect": (
                    "MT5 execution(MT5 실행)은 Stage349(349단계)에서 가볍게 시작하고, "
                    "Stage348(348단계)은 package handoff(패키지 인계)까지로 멈춘다."
                ),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )
    return retargeted


def write_stage_docs(summary: Mapping[str, Any]) -> None:
    write_text(
        STAGE_BRIEF,
        f"""# Stage 349 Brief(349단계 개요)

## Stage ID(단계 ID)

`{NEW_STAGE_ID}`

## Question(질문)

Can the ONNX short-carry probe package(온엑스 숏 기여 탐침 패키지) from Stage348(348단계) be executed as an MT5 runtime probe(MT5 런타임 탐침) without making Stage348(348단계) heavier?

## Scope(범위)

- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_package_run(원천 패키지 실행): `{PARENT_RUN_ID}`
- branch_run(분기 실행): `{RUN_ID}`
- superseded_run(대체된 예정 실행): `{SUPERSEDED_RUN_ID}`
- next_run(다음 실행): `{NEXT_RUN_ID}`

Action(행동): Stage348(348단계)의 run348D runtime probe(런타임 탐침)를 run349B(349B 실행)로 retarget(재지정)한다.
Effect(효과): Stage348(348단계)은 proxy review/package handoff(프록시 검토/패키지 인계)로 가볍게 멈추고, MT5 execution(MT5 실행)은 새 stage(단계)에서 읽는다.

## Source Truth(원천 진실)

- package_status(패키지 상태): `{summary["source_status"]}`
- attempts(시도): `{summary["attempt_count"]}`
- expected_rows(예상 행): `{summary["expected_rows"]}`
- feature_rows(피처 행): `{summary["feature_rows"]}`
- feature_count(피처 수): `{summary["feature_count"]}`
- missing_mt5_contract_features(누락 MT5 계약 피처): `{summary["missing_mt5_contract_feature_count"]}`
- cash_open_partial_mapping_attempts(현금장 부분 매핑 시도): `{summary["cash_open_partial_mapping_attempts"]}`
- proxy_ea_expected_mismatch_rows(프록시-EA 예상 불일치 행): `{summary["proxy_ea_expected_mismatch_rows"]}`
- common_sync_missing(공용 동기화 누락): `{summary["common_sync_missing"]}`

## Evidence Boundary(근거 경계)

This branch(분기)는 state sync(상태 동기화)와 handoff(인계)만 수행한다. No new MT5 execution(새 MT5 실행 없음), no candidate selection(후보 선정 없음), no forward pass(전진 통과 없음), no live readiness(실거래 준비 없음), no operating promotion(운영 승격 없음), no runtime authority(런타임 권위 없음), no Goal Achieve(목표 달성 없음)이다.

## Runtime Review Constraint(런타임 검토 제약)

- trade_density_requirement(거래 밀도 요구): `{TRADE_DENSITY_REQUIREMENT}`
- meaning(의미): trade per day(일일 거래 수)는 최소 3~10 혹은 그 이상을 목표로 하되, trade splitting(거래 쪼개기)으로 수익을 나누는 방식은 금지한다.
- effect(효과): run349B(349B 실행)의 MT5 KPI(MT5 핵심 성과 지표)는 net profit(순수익)과 PF(수익 팩터)뿐 아니라 trade count(거래수), trade density(거래 밀도), expectancy(기대값)를 함께 봐야 한다.
""",
    )
    write_text(
        STAGE_README,
        f"""# Stage 349(349단계)

Stage349(349단계)는 ONNX short-carry runtime probe(온엑스 숏 기여 런타임 탐침) 실행만 얇게 맡는다.

- current_run(현재 실행): `{NEXT_RUN_ID}`
- branch_run(분기 실행): `{RUN_ID}`
- source_package(원천 패키지): `{PARENT_RUN_ID}`
- retargeted_queue(재지정 대기열): `{rel(NEXT_QUEUE)}`

Effect(효과): Stage348(348단계)의 package artifact(패키지 산출물)는 복사하지 않고 참조해 heavy artifact duplication(무거운 산출물 중복)을 줄인다.
""",
    )
    write_text(
        INPUT_REFS,
        f"""# Stage 349 Input Refs(349단계 입력 참조)

- run348C final decision(348C 최종 결정): `{rel(SOURCE_FINAL_DECISION)}`
- run348C attempt package(348C 시도 패키지): `{rel(SOURCE_ATTEMPT_PACKAGE)}`
- run348D source queue(348D 원천 대기열): `{rel(SOURCE_QUEUE)}`
- retargeted run349B queue(349B 재지정 대기열): `{rel(NEXT_QUEUE)}`
- expected tape(예상 테이프): `{rel(SOURCE_EXPECTED_TAPE)}`
- runtime parity contract(런타임 동등성 계약): `{rel(SOURCE_RUNTIME_PARITY)}`
- tester identity contract(테스터 정체성 계약): `{rel(SOURCE_TESTER_IDENTITY)}`
- runtime mapping audit(런타임 매핑 감사): `{rel(SOURCE_MAPPING_AUDIT)}`
- proxy MT5 comparison contract(프록시 MT5 비교 계약): `{rel(SOURCE_PROXY_COMPARISON)}`
- source report(원천 보고서): `{rel(SOURCE_REPORT)}`

Action(행동): Stage349(349단계)는 Stage348(348단계)의 package artifact(패키지 산출물)를 복사하지 않고 참조한다.
Effect(효과): lineage(계보)는 유지하면서 stage payload(단계 적재량)를 줄인다.
""",
    )
    write_text(
        SELECTION_STATUS,
        f"""# Stage349 Selection Status(349단계 선정 상태)

- active_stage(현재 단계): `{NEW_STAGE_ID}`
- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- selected_model(선정 모델): `none(없음)`
- source_package(원천 패키지): `{PARENT_RUN_ID}`
- packaged_attempts(패키지 시도): `{summary["attempt_count"]}`
- feature_order_boundary(피처 순서 경계): `53_feature_probe_only(53개 피처 탐침 전용)`
- trade_density_requirement(거래 밀도 요구): `{TRADE_DENSITY_REQUIREMENT}`
- runtime_queue(런타임 대기열): `{rel(NEXT_QUEUE)}`
- runtime_authority(런타임 권위): `not_claimed(주장 없음)`
- operating_promotion(운영 승격): `not_claimed(주장 없음)`
- Goal Achieve(목표 달성): `not_claimed(주장 없음)`

Effect(효과): Stage349(349단계)는 MT5 runtime probe(MT5 런타임 탐침) 실행 대기 상태만 갖고, 운영 주장(operating claim, 운영 주장)은 만들지 않는다.
""",
    )
    write_text(ROOT_SELECTION_STATUS, read_text(SELECTION_STATUS))
    write_text(
        REVIEW_INDEX,
        f"""# Stage349 Review Index(349단계 검토 색인)

- run349A stage branch(349A 단계 분기): `{rel(REPORT_PATH)}`

Effect(효과): Stage349(349단계)의 첫 근거는 branch/handoff(분기/인계)로 고정한다.
""",
    )
    write_text(
        SOURCE_SELECTION_STATUS,
        f"""# Stage348 Selection Status(348단계 선정 상태)

- active_stage_at_handoff(인계 당시 단계): `{SOURCE_STAGE_ID}`
- latest_completed_run(최근 완료 실행): `{PARENT_RUN_ID}`
- superseded_planned_run(대체된 예정 실행): `{SUPERSEDED_RUN_ID}`
- handoff_stage(인계 단계): `{NEW_STAGE_ID}`
- handoff_run(인계 실행): `{RUN_ID}`
- next_runtime_run(다음 런타임 실행): `{NEXT_RUN_ID}`
- selected_model(선정 모델): `none(없음)`
- latest_package(최근 패키지): `{PARENT_RUN_ID}`
- packaged_attempts(패키지 시도): `{summary["attempt_count"]}`
- feature_order_boundary(피처 순서 경계): `53_feature_probe_only(53개 피처 탐침 전용)`
- trade_density_requirement(거래 밀도 요구): `{TRADE_DENSITY_REQUIREMENT}`
- runtime_authority(런타임 권위): `not_claimed(주장 없음)`
- operating_promotion(운영 승격): `not_claimed(주장 없음)`
- Goal Achieve(목표 달성): `not_claimed(주장 없음)`

Effect(효과): Stage348(348단계)은 MT5 runtime execution(MT5 런타임 실행)을 더 품지 않고 Stage349(349단계)로 넘긴다.
""",
    )
    append_text_once(
        SOURCE_REVIEW_INDEX,
        RUN_ID,
        f"""- run349A stage branch handoff(349A 단계 분기 인계): `{rel(REPORT_PATH)}` / `{RUN_ID}`""",
    )
    write_text(
        SOURCE_STAGE_BRIEF,
        f"""# Stage348 Cash-Open Proxy Review(348단계 현금장 프록시 검토)

## Stage ID(단계 ID)

`{SOURCE_STAGE_ID}`

## Question(질문)

Can run347C proxy training(347C 프록시 학습)을 long OOS gap(롱 표본외 공백)과 short carry clue(숏 기여 단서)로 분류해, MT5 runtime probe(MT5 런타임 탐침)로 보낼 만한 가장 작은 seed(씨앗)만 남길 수 있는가?

## Source Inputs(원천 입력)

- source_stage(원천 단계): `347_cash_open_asymmetric_source__long_short_head_design`
- source_run(원천 실행): `run347C_train_cash_open_asymmetric_source_proxy_models_without_db_v1`
- source_package_run(원천 패키지 실행): `{summary["source_package_run_id"]}`
- branch_run(분기 실행): `run348A_branch_stage347_to_cash_open_proxy_review_without_db_v1`
- source_rows(원천 행): `{summary["feature_rows"]}`
- feature_count(피처 수): `{summary["feature_count"]}`

## Scope(범위)

Stage348(348단계)은 review/triage/package handoff(검토/분류/패키지 인계) 전용이다. MT5 execution(MT5 실행), candidate selection(후보 선정), runtime authority(런타임 권위)는 Stage349(349단계) 이후 근거가 있어야만 말한다.

## Completed Runs(완료 실행)

- run348A(348A 실행): Stage347(347단계) proxy review(프록시 검토)를 Stage348(348단계)로 분리했다.
- run348B(348B 실행): ONNX deployable short-carry seeds(온엑스 배포 가능 숏 기여 씨앗)만 다음 패키지로 넘겼다.
- run348C(348C 실행): attempts(시도) `{summary["attempt_count"]}`, expected_rows(예상 행) `{summary["expected_rows"]}`인 MT5 runtime probe package(MT5 런타임 탐침 패키지)를 만들었다.

## Stage349 Handoff(349단계 인계)

- branch_run(분기 실행): `{RUN_ID}`
- next_stage(다음 단계): `{NEW_STAGE_ID}`
- next_run(다음 실행): `{NEXT_RUN_ID}`

Action(행동): Stage348(348단계)의 run348D planned execution(예정 실행)을 Stage349 run349B(349B 실행)로 retarget(재지정)했다.
Effect(효과): Stage348(348단계)은 무거운 실행 근거 수집을 더 품지 않고, package evidence(패키지 근거)까지만 보존한다.

## Claim Boundary(주장 경계)

`{CLAIM_BOUNDARY}`
""",
    )


def write_current_truth() -> None:
    write_plain_text(
        WORKSPACE_STATE,
        f"""current_stage_id: {NEW_STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {STATUS}
current_judgment: {JUDGMENT}
current_decision: {DECISION}
next_run_id: {NEXT_RUN_ID}
claim_boundary: {CLAIM_BOUNDARY}
updated_at: {TODAY}
""",
    )
    write_text(
        CURRENT_WORKING_STATE,
        f"""# Current Working State(현재 작업 상태)

## Current Truth(현재 진실)

- active_stage(현재 단계): `{NEW_STAGE_ID}`
- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`

## Effect(효과)

Stage348(348단계)의 ONNX short-carry runtime probe package(온엑스 숏 기여 런타임 탐침 패키지)를 Stage349(349단계)로 handoff(인계)했다. run349B(349B 실행)는 실제 Strategy Tester(전략 테스터) 실행을 맡는다.

## Claim Boundary(주장 경계)

`{CLAIM_BOUNDARY}`

No new MT5 execution(새 MT5 실행 없음), no candidate selection(후보 선정 없음), no forward pass(전진 통과 없음), no live readiness(실거래 준비 없음), no operating promotion(운영 승격 없음), no runtime authority(런타임 권위 없음), no Goal Achieve(목표 달성 없음).
""",
    )


def write_report_and_decision(summary: Mapping[str, Any]) -> None:
    report = f"""# run349A Stage Branch(349A 단계 분기)

## Decision(결정)

`{DECISION}`

## Reason(이유)

Stage348(348단계)은 proxy review(프록시 검토), short-carry seed triage(숏 기여 씨앗 분류), ONNX package materialization(온엑스 패키지 물질화), run348D queue(348D 대기열)까지 담아 무거워졌다. 다음 질문은 review(검토)가 아니라 MT5 runtime execution(MT5 런타임 실행)이므로 Stage349(349단계)로 분기한다.

Action(행동): `{SUPERSEDED_RUN_ID}`를 직접 이어가지 않고 `{NEXT_RUN_ID}`로 retarget(재지정)한다.
Effect(효과): Stage348(348단계)의 evidence(근거)는 보존하고, Stage349(349단계)는 runtime evidence(런타임 근거) 수집만 받는다.

## Handoff(인계)

- source_package(원천 패키지): `{PARENT_RUN_ID}`
- attempts(시도): `{summary["attempt_count"]}`
- expected_rows(예상 행): `{summary["expected_rows"]}`
- feature_rows(피처 행): `{summary["feature_rows"]}`
- feature_count(피처 수): `{summary["feature_count"]}`
- common_sync_missing(공용 동기화 누락): `{summary["common_sync_missing"]}`
- missing_mt5_contract_features(누락 MT5 계약 피처): `{summary["missing_mt5_contract_feature_count"]}`
- cash_open_partial_mapping_attempts(현금장 부분 매핑 시도): `{summary["cash_open_partial_mapping_attempts"]}`
- next_queue(다음 대기열): `{rel(NEXT_QUEUE)}`
- trade_density_requirement(거래 밀도 요구): `{TRADE_DENSITY_REQUIREMENT}`

## Boundary(경계)

`{CLAIM_BOUNDARY}`

No new MT5 execution(새 MT5 실행 없음), no Goal Achieve(목표 달성 없음), no runtime authority(런타임 권위 없음), no operating promotion(운영 승격 없음).
"""
    write_text(REPORT_PATH, report)
    write_text(
        DECISION_DOC,
        f"""# {TODAY} Stage349A Branch Decision(349A 단계 분기 결정)

## Decision(결정)

`{DECISION}`

## Source(원천)

- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_package(원천 패키지): `{PARENT_RUN_ID}`
- superseded_run(대체 실행): `{SUPERSEDED_RUN_ID}`
- new_stage(새 단계): `{NEW_STAGE_ID}`
- next_run(다음 실행): `{NEXT_RUN_ID}`

## Action/Effect(행동/효과)

Action(행동): Stage348(348단계)의 MT5 runtime probe(MT5 런타임 탐침)를 Stage349(349단계)로 분기했다.
Effect(효과): Stage348(348단계)은 package handoff(패키지 인계)까지만 유지하고, MT5 execution evidence(MT5 실행 근거)는 Stage349(349단계)에서 수집한다.

## Claim Boundary(주장 경계)

`{CLAIM_BOUNDARY}`
""",
    )


def ledger_rows(summary: Mapping[str, Any], gate_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    gate_passes = sum(1 for row in gate_rows if row.get("status") == "passed")
    gate_total = len(gate_rows)
    base = {
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
        "gate_passes": gate_passes,
        "gate_total": gate_total,
        "claim_boundary": CLAIM_BOUNDARY,
        "scoreboard_lane": "state_sync_stage_branch(상태 동기화 단계 분기)",
        "lane": "state_sync_stage_branch(상태 동기화 단계 분기)",
        "family": "state_sync(상태 동기화)",
        "run_number": RUN_NUMBER,
        "notes": "User requested a stage branch because Stage348 became heavy(사용자가 348단계가 무거워져 단계 분기를 요청함).",
        "source_package_run_id": PARENT_RUN_ID,
        "rows": summary["expected_rows"],
        "attempt_count": summary["attempt_count"],
        "feature_count": summary["feature_count"],
        "candidate_model_id": "none(없음)",
        "sample_rows": summary["feature_rows"],
    }
    tier_a = {
        **base,
        "ledger_row_id": f"{RUN_ID}__Tier A",
        "subrun_id": "Tier A",
        "view": "Tier A separate(Tier A 분리)",
        "record_view": "Tier A separate(Tier A 분리)",
        "tier": "Tier A",
        "tier_scope": "Tier A",
        "metric_scope": "stage_branch_handoff_run348C_onnx_short_carry_runtime_package",
        "kpi_scope": "stage_branch_handoff_run348C_onnx_short_carry_runtime_package",
        "primary_kpi": f"attempts={summary['attempt_count']};expected_rows={summary['expected_rows']};feature_count={summary['feature_count']}",
        "guardrail_kpi": (
            f"feature_contract=53_vs_58;missing_mt5_contract_features={summary['missing_mt5_contract_feature_count']};"
            f"cash_open_partial_mapping_attempts={summary['cash_open_partial_mapping_attempts']};"
            f"{TRADE_DENSITY_REQUIREMENT};no_mt5_execution"
        ),
        "external_verification_status": "out_of_scope_by_claim(주장 범위 밖)",
        "result_status": "stage_branch_opened_no_selection(단계 분기 완료, 선정 없음)",
    }
    tier_b = {
        **base,
        "ledger_row_id": f"{RUN_ID}__Tier B",
        "subrun_id": "Tier B",
        "view": "Tier B separate(Tier B 분리)",
        "record_view": "Tier B separate(Tier B 분리)",
        "tier": "Tier B",
        "tier_scope": "Tier B",
        "metric_scope": "missing_required",
        "kpi_scope": "missing_required",
        "primary_kpi": "missing_required(필수 누락)",
        "guardrail_kpi": "missing_required(필수 누락)",
        "external_verification_status": "missing_required(필수 누락)",
        "result_status": "missing_required(필수 누락)",
        "rows": "",
        "attempt_count": "",
        "feature_count": "",
        "sample_rows": "",
    }
    combined = {
        **tier_a,
        "ledger_row_id": f"{RUN_ID}__Tier A+B",
        "subrun_id": "Tier A+B",
        "view": "Tier A+B combined(Tier A+B 합산)",
        "record_view": "Tier A+B combined(Tier A+B 합산)",
        "tier": "Tier A+B",
        "tier_scope": "Tier A+B",
        "metric_scope": "same_as_tier_a_until_tier_b_available",
        "kpi_scope": "same_as_tier_a_until_tier_b_available",
        "result_status": "same_as_tier_a_until_tier_b_available",
        "guardrail_kpi": "Tier B missing_required(Tier B 필수 누락);feature_contract=53_vs_58;no_mt5_execution",
    }
    return [tier_a, tier_b, combined]


def write_ledgers(summary: Mapping[str, Any], gate_rows: Sequence[Mapping[str, Any]]) -> None:
    rows = ledger_rows(summary, gate_rows)
    write_csv(STAGE_LEDGER, rows, LEDGER_COLUMNS)
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], rows)
    append_or_replace_csv(
        RUN_REGISTRY,
        ["run_id"],
        [
            {
                "run_id": RUN_ID,
                "stage_id": NEW_STAGE_ID,
                "lane": "state_sync_stage_branch(상태 동기화 단계 분기)",
                "family": "state_sync(상태 동기화)",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(FINAL_DECISION),
                "notes": "Stage348 was branched before ONNX short-carry MT5 runtime probe because it became heavy(348단계가 무거워져 온엑스 숏 기여 MT5 런타임 탐침 전에 분기함).",
                "primary_report": rel(REPORT_PATH),
                "run_number": RUN_NUMBER,
                "date": TODAY,
                "decision": DECISION,
                "parent_run_id": PARENT_RUN_ID,
                "next_run_id": NEXT_RUN_ID,
                "rows": summary["expected_rows"],
                "gate_passes": sum(1 for row in gate_rows if row.get("status") == "passed"),
                "gate_total": len(gate_rows),
                "claim_boundary": CLAIM_BOUNDARY,
                "report_path": rel(REPORT_PATH),
                "primary_artifact": rel(FINAL_DECISION),
                "candidate_model_id": "none(없음)",
                "result_status": "stage_branch_opened_no_selection(단계 분기 완료, 선정 없음)",
                "sample_rows": summary["feature_rows"],
                "feature_count": summary["feature_count"],
                "attempt_count": summary["attempt_count"],
                "view": "Tier A separate(Tier A 분리)",
                "tier": "Tier A",
                "metric_scope": "stage_branch_handoff_run348C_onnx_short_carry_runtime_package",
                "source_package_run_id": PARENT_RUN_ID,
            }
        ],
    )


def write_receipts(summary: Mapping[str, Any], inventory: Sequence[Mapping[str, Any]], queue_rows: Sequence[Mapping[str, Any]]) -> None:
    created_at = now_utc()
    artifact_paths = [
        HANDOFF_MANIFEST,
        SOURCE_INVENTORY,
        NEXT_QUEUE,
        STAGE_TRANSITION_RECEIPT,
        LINEAGE_RECEIPT,
        CLAIM_RECEIPT,
        GATE_AUDIT,
        FINAL_DECISION,
        RUN_MANIFEST,
        REPORT_PATH,
        REVIEW_INDEX,
        DECISION_DOC,
        STAGE_BRIEF,
        INPUT_REFS,
        SELECTION_STATUS,
        STAGE_LEDGER,
    ]
    existing_hashes = {rel(path): sha256_file(path) for path in artifact_paths if exists(path)}
    write_json(
        STAGE_TRANSITION_RECEIPT,
        {
            "run_id": RUN_ID,
            "source_stage_id": SOURCE_STAGE_ID,
            "new_stage_id": NEW_STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "superseded_run_id": SUPERSEDED_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "queue_rows": len(queue_rows),
            "attempt_count": summary["attempt_count"],
            "expected_rows": summary["expected_rows"],
            "judgment": JUDGMENT,
            "decision": DECISION,
            "created_at_utc": created_at,
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(
        LINEAGE_RECEIPT,
        {
            "run_id": RUN_ID,
            "stage_id": NEW_STAGE_ID,
            "source_inputs": list(inventory),
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [rel(path) for path in artifact_paths],
            "artifact_hashes": existing_hashes,
            "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "availability": "tracked",
            "lineage_judgment": "connected_with_boundary",
            "claim_boundary": CLAIM_BOUNDARY,
            "created_at_utc": created_at,
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            "run_id": RUN_ID,
            "allowed_claim": "state sync and stage branch handoff only(상태 동기화와 단계 분기 인계만)",
            "forbidden_claims": [
                "new_MT5_execution_completed(새 MT5 실행 완료)",
                "candidate_selection(후보 선정)",
                "forward_validation(전진 검증)",
                "live_readiness(실거래 준비)",
                "operating_promotion(운영 승격)",
                "runtime_authority(런타임 권위)",
                "Goal_Achieve(목표 달성)",
            ],
            "next_condition": f"{NEXT_RUN_ID} MT5 runtime probe(MT5 런타임 탐침)",
            "trade_density_requirement": TRADE_DENSITY_REQUIREMENT,
            "created_at_utc": created_at,
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def write_final_decision(summary: Mapping[str, Any], gate_rows: Sequence[Mapping[str, Any]]) -> None:
    gate_passes = sum(1 for row in gate_rows if row.get("status") == "passed")
    gate_total = len(gate_rows)
    write_json(
        FINAL_DECISION,
        {
            "stage_id": NEW_STAGE_ID,
            "run_id": RUN_ID,
            "parent_stage_id": SOURCE_STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "superseded_run_id": SUPERSEDED_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "status": STATUS,
            "judgment": JUDGMENT,
            "decision": DECISION,
            "source_status": summary["source_status"],
            "source_judgment": summary["source_judgment"],
            "attempt_count": summary["attempt_count"],
            "expected_rows": summary["expected_rows"],
            "feature_rows": summary["feature_rows"],
            "feature_count": summary["feature_count"],
            "missing_mt5_contract_feature_count": summary["missing_mt5_contract_feature_count"],
            "cash_open_partial_mapping_attempts": summary["cash_open_partial_mapping_attempts"],
            "proxy_ea_expected_mismatch_rows": summary["proxy_ea_expected_mismatch_rows"],
            "common_sync_missing": summary["common_sync_missing"],
            "trade_density_requirement": TRADE_DENSITY_REQUIREMENT,
            "gate_passes": gate_passes,
            "gate_total": gate_total,
            "new_mt5_execution": "not_run",
            "external_verification_status": "out_of_scope_by_claim(주장 범위 밖)",
            "candidate_selection": "not_claimed",
            "forward_passed": "not_claimed",
            "runtime_authority": "not_claimed",
            "operating_promotion": "not_claimed",
            "goal_achieve": "not_claimed",
            "claim_boundary": CLAIM_BOUNDARY,
            "created_at_utc": now_utc(),
        },
    )
    write_json(
        RUN_MANIFEST,
        {
            "stage_id": NEW_STAGE_ID,
            "run_id": RUN_ID,
            "run_number": RUN_NUMBER,
            "work_family": "state_sync(상태 동기화)",
            "primary_action": "stage_branch(단계 분기)",
            "producer": rel(Path(__file__)),
            "inputs": [rel(path) for path, _label in SOURCE_INPUTS],
            "outputs": [
                rel(FINAL_DECISION),
                rel(GATE_AUDIT),
                rel(HANDOFF_MANIFEST),
                rel(NEXT_QUEUE),
                rel(REPORT_PATH),
                rel(DECISION_DOC),
                rel(STAGE_BRIEF),
                rel(INPUT_REFS),
                rel(SELECTION_STATUS),
            ],
            "next_run_id": NEXT_RUN_ID,
            "trade_density_requirement": TRADE_DENSITY_REQUIREMENT,
            "claim_boundary": CLAIM_BOUNDARY,
            "created_at_utc": now_utc(),
        },
    )


def write_gates(summary: Mapping[str, Any], inventory: Sequence[Mapping[str, Any]], queue_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    workspace_text = read_text(WORKSPACE_STATE) if exists(WORKSPACE_STATE) else ""
    current_text = read_text(CURRENT_WORKING_STATE) if exists(CURRENT_WORKING_STATE) else ""
    selection_text = read_text(SELECTION_STATUS) if exists(SELECTION_STATUS) else ""
    all_inputs_exist = all(row.get("exists") == "true" for row in inventory)
    gates = [
        {
            "gate_id": "user_requested_stage_branch_recorded",
            "status": "passed",
            "evidence_path": rel(REPORT_PATH),
            "effect": "사용자 요청(user request, 사용자 요청)에 따라 Stage348(348단계)을 Stage349(349단계)로 분기했다.",
        },
        {
            "gate_id": "source_run348C_gates_passed",
            "status": "passed" if source_gate_passed() else "failed",
            "evidence_path": rel(SOURCE_GATE_AUDIT),
            "effect": "분기 원천(source, 원천)인 run348C(348C 실행)의 gate(게이트)를 확인했다.",
        },
        {
            "gate_id": "input_manifest_all_sources_visible",
            "status": "passed" if all_inputs_exist else "failed",
            "evidence_path": rel(INPUT_MANIFEST),
            "effect": "Stage349(349단계)가 참조할 source artifact(원천 산출물) 가시성을 확인했다.",
        },
        {
            "gate_id": "new_stage_structure_created",
            "status": (
                "passed"
                if all(exists(path) for path in [STAGE_BRIEF, INPUT_REFS, SELECTION_STATUS, REVIEW_INDEX, REPORT_PATH])
                else "failed"
            ),
            "evidence_path": rel(NEW_STAGE_DIR),
            "effect": "새 stage(단계)의 필수 폴더와 문서를 만들었다.",
        },
        {
            "gate_id": "queue_retargeted_to_run349B",
            "status": "passed" if queue_rows and all(row.get("next_run_id") == NEXT_RUN_ID for row in queue_rows) else "failed",
            "evidence_path": rel(NEXT_QUEUE),
            "effect": "run348D(348D 실행) 대기열을 run349B(349B 실행)로 재지정했다.",
        },
        {
            "gate_id": "trade_density_constraint_recorded",
            "status": (
                "passed"
                if TRADE_DENSITY_REQUIREMENT in read_text(STAGE_BRIEF)
                and TRADE_DENSITY_REQUIREMENT in read_text(SELECTION_STATUS)
                else "failed"
            ),
            "evidence_path": f"{rel(STAGE_BRIEF)};{rel(SELECTION_STATUS)}",
            "effect": "trade per day(일일 거래 수)와 no trade splitting(거래 쪼개기 금지)을 다음 런타임 검토 기준으로 고정했다.",
        },
        {
            "gate_id": "state_sync_audit",
            "status": (
                "passed"
                if NEW_STAGE_ID in workspace_text
                and NEXT_RUN_ID in workspace_text
                and NEW_STAGE_ID in current_text
                and NEW_STAGE_ID in selection_text
                else "failed"
            ),
            "evidence_path": f"{rel(WORKSPACE_STATE)};{rel(CURRENT_WORKING_STATE)};{rel(SELECTION_STATUS)}",
            "effect": "current truth(현재 진실)가 Stage349(349단계)를 가리키게 동기화했다.",
        },
        {
            "gate_id": "artifact_lineage_audit",
            "status": "passed" if exists(HANDOFF_MANIFEST) and exists(SOURCE_INVENTORY) else "failed",
            "evidence_path": rel(HANDOFF_MANIFEST),
            "effect": "source input(원천 입력)과 branch artifact(분기 산출물)의 계보를 연결했다.",
        },
        {
            "gate_id": "ledger_sync_audit",
            "status": "pending_until_ledgers_written",
            "evidence_path": rel(STAGE_LEDGER),
            "effect": "stage/project ledger(단계/프로젝트 장부)에 분기 실행을 찾을 수 있어야 한다.",
        },
        {
            "gate_id": "final_claim_guard",
            "status": "passed" if exists(CLAIM_RECEIPT) else "failed",
            "evidence_path": rel(CLAIM_RECEIPT),
            "effect": "운영 승격(operating promotion, 운영 승격)과 목표 달성(Goal Achieve, 목표 달성) 주장을 막았다.",
        },
        {
            "gate_id": "required_gate_coverage_audit_written",
            "status": "passed",
            "evidence_path": rel(GATE_AUDIT),
            "effect": "required gate coverage audit(필수 게이트 커버리지 감사)을 기록했다.",
        },
    ]
    first_pass = [{**gate, "claim_boundary": CLAIM_BOUNDARY} for gate in gates]
    write_csv(GATE_AUDIT, first_pass, ["gate_id", "status", "evidence_path", "effect", "claim_boundary"])
    return first_pass


def finalize_gates(gates: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for gate in gates:
        row = dict(gate)
        if row.get("gate_id") == "ledger_sync_audit":
            row["status"] = "passed" if exists(STAGE_LEDGER) and exists(PROJECT_LEDGER) and exists(RUN_REGISTRY) else "failed"
        rows.append(row)
    write_csv(GATE_AUDIT, rows, ["gate_id", "status", "evidence_path", "effect", "claim_boundary"])
    return rows


def write_artifact_registry() -> None:
    artifacts = [
        ("final_decision", FINAL_DECISION, "run349A branch final decision(349A 분기 최종 결정)"),
        ("required_gate_coverage_audit", GATE_AUDIT, "run349A gate audit(349A 게이트 감사)"),
        ("handoff_manifest", HANDOFF_MANIFEST, "Stage348C to Stage349 handoff manifest(348C에서 349단계 인계 목록)"),
        ("source_inventory", SOURCE_INVENTORY, "Stage349 source inventory(349단계 원천 목록)"),
        ("retargeted_queue", NEXT_QUEUE, "run349B retargeted queue(349B 재지정 대기열)"),
        ("stage_transition_receipt", STAGE_TRANSITION_RECEIPT, "stage transition receipt(단계 전환 영수증)"),
        ("artifact_lineage_receipt", LINEAGE_RECEIPT, "artifact lineage receipt(산출물 계보 영수증)"),
        ("claim_boundary_receipt", CLAIM_RECEIPT, "claim boundary receipt(주장 경계 영수증)"),
        ("stage_branch_report", REPORT_PATH, "run349A branch report(349A 분기 보고서)"),
        ("decision_doc", DECISION_DOC, "run349A durable decision document(349A 결정 문서)"),
        ("run_manifest", RUN_MANIFEST, "run349A run manifest(349A 실행 목록)"),
        ("stage_brief", STAGE_BRIEF, "Stage349 stage brief(349단계 개요)"),
        ("input_refs", INPUT_REFS, "Stage349 input refs(349단계 입력 참조)"),
        ("selection_status", SELECTION_STATUS, "Stage349 selection status(349단계 선정 상태)"),
        ("pipeline", Path(__file__), "run349A producer script(349A 생산 스크립트)"),
    ]
    rows = [
        {
            "stage_id": NEW_STAGE_ID,
            "run_id": RUN_ID,
            "artifact_type": artifact_type,
            "path": rel(path),
            "sha256": sha256_file(path) if exists(path) else "",
            "created_at": TODAY,
            "claim_boundary": CLAIM_BOUNDARY,
            "artifact_id": f"{RUN_ID}__{rel(path).replace('/', '__').replace('.', '_')}",
            "created_at_utc": now_utc(),
            "notes": notes,
            "artifact_path": rel(path),
        }
        for artifact_type, path, notes in artifacts
    ]
    append_or_replace_csv(ARTIFACT_REGISTRY, ["artifact_id"], rows)


def append_changelogs() -> None:
    block = f"""## {TODAY} {RUN_ID}

Action(행동): Stage348(348단계)의 run348D MT5 runtime probe(MT5 런타임 탐침)를 Stage349(349단계) run349B로 retarget(재지정)했다.
Effect(효과): Stage348(348단계)은 package handoff(패키지 인계)까지로 가볍게 멈추고, runtime evidence(런타임 근거)는 Stage349(349단계)에서 수집한다.

- next_stage(다음 단계): `{NEW_STAGE_ID}`
- next_run(다음 실행): `{NEXT_RUN_ID}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    append_text_once(ROOT_CHANGELOG, RUN_ID, block)
    append_text_once(WORKSPACE_CHANGELOG, RUN_ID, block)


def validate(gate_rows: Sequence[Mapping[str, Any]]) -> None:
    missing = [
        rel(path)
        for path in [
            STAGE_BRIEF,
            INPUT_REFS,
            INPUT_MANIFEST,
            SELECTION_STATUS,
            REVIEW_INDEX,
            REPORT_PATH,
            DECISION_DOC,
            FINAL_DECISION,
            RUN_MANIFEST,
            GATE_AUDIT,
            WORKSPACE_STATE,
            CURRENT_WORKING_STATE,
            HANDOFF_MANIFEST,
            NEXT_QUEUE,
            STAGE_LEDGER,
        ]
        if not exists(path)
    ]
    if missing:
        raise FileNotFoundError("missing generated output(생성 출력 누락): " + ", ".join(missing))
    failed = [row["gate_id"] for row in gate_rows if row.get("status") != "passed"]
    if failed:
        write_json(
            RUN_DIR / "self_correction_plan.json",
            {
                "run_id": RUN_ID,
                "failed_gates": failed,
                "mode": "plan_only(계획 전용)",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        )
        raise RuntimeError("run349A required gate audit failed(349A 필수 게이트 감사 실패): " + ", ".join(failed))
    for label, path in [
        ("workspace", WORKSPACE_STATE),
        ("current", CURRENT_WORKING_STATE),
        ("selection", SELECTION_STATUS),
        ("root_selection", ROOT_SELECTION_STATUS),
    ]:
        if NEW_STAGE_ID not in read_text(path):
            raise RuntimeError(f"{label} missing active Stage349(349단계 누락)")
    final = read_json(FINAL_DECISION)
    for key in ["runtime_authority", "operating_promotion", "goal_achieve"]:
        if final.get(key) != "not_claimed":
            raise RuntimeError(f"forbidden claim raised(금지 주장 발생): {key}={final.get(key)}")


def main() -> None:
    for directory in [
        NEW_STAGE_DIR / "00_spec",
        NEW_STAGE_DIR / "01_inputs",
        RUN_DIR,
        REVIEW_DIR,
        NEW_STAGE_DIR / "04_selected",
        DECISION_DOC.parent,
    ]:
        os.makedirs(fs_path(directory), exist_ok=True)
    for path, _label in SOURCE_INPUTS:
        required(path)
    summary = source_summary()
    inventory = write_source_inventory()
    queue_rows = write_handoff_artifacts(summary)
    write_stage_docs(summary)
    write_current_truth()
    write_report_and_decision(summary)
    write_receipts(summary, inventory, queue_rows)
    gates = write_gates(summary, inventory, queue_rows)
    write_ledgers(summary, gates)
    gates = finalize_gates(gates)
    write_ledgers(summary, gates)
    write_final_decision(summary, gates)
    write_receipts(summary, inventory, queue_rows)
    write_artifact_registry()
    append_changelogs()
    validate(gates)
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "new_stage_id": NEW_STAGE_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "next_run_id": NEXT_RUN_ID,
                "gate_passes": sum(1 for row in gates if row["status"] == "passed"),
                "gate_total": len(gates),
                "attempt_count": summary["attempt_count"],
                "expected_rows": summary["expected_rows"],
                "feature_count": summary["feature_count"],
                "goal_achieve": "not_claimed",
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
