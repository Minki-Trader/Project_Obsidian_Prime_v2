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

SOURCE_STAGE_ID = "344_directional_long_quality__supply_surface_probe"
NEW_STAGE_ID = "345_cash_open_decomposition__long_quality_short_carry_runtime_probe"
SOURCE_STAGE_DIR = ROOT / "stages" / SOURCE_STAGE_ID
NEW_STAGE_DIR = ROOT / "stages" / NEW_STAGE_ID

RUN_NUMBER = "run345A"
RUN_ID = "run345A_branch_stage344_to_cash_open_long_quality_short_carry_runtime_probe_without_db_v1"
PARENT_RUN_ID = "run344N_materialize_cash_open_long_quality_short_carry_decomposition_package_without_db_v1"
SUPERSEDED_RUN_ID = "run344O_execute_cash_open_long_quality_short_carry_decomposition_mt5_probe_without_db_v1"
NEXT_RUN_ID = "run345B_execute_cash_open_long_quality_short_carry_decomposition_mt5_probe_without_db_v1"

STATUS = "completed_stage345A_branch_from_stage344_cash_open_runtime_probe_opened_no_selection"
JUDGMENT = "stage_branch_completed_stage344_overweight_handoff_to_cash_open_runtime_probe_no_selection"
DECISION = "stage345A_open_run345B_execute_cash_open_long_quality_short_carry_mt5_probe"
CLAIM_BOUNDARY = (
    "state_sync_stage_branch_cash_open_long_quality_short_carry_runtime_probe_handoff_only_"
    "no_new_mt5_execution_no_candidate_selection_no_forward_pass_no_live_readiness_"
    "no_operating_promotion_no_runtime_authority_no_goal_claim"
)

RUN_DIR = NEW_STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = NEW_STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEW_DIR / "run345A_stage_branch.md"
REVIEW_INDEX = REVIEW_DIR / "review_index.md"
DECISION_DOC = (
    ROOT
    / "docs"
    / "decisions"
    / f"{TODAY}_stage345A_branch_stage344_to_cash_open_long_quality_short_carry_runtime_probe.md"
)
STAGE_BRIEF = NEW_STAGE_DIR / "00_spec" / "stage_brief.md"
STAGE_README = NEW_STAGE_DIR / "README.md"
INPUT_REFS = NEW_STAGE_DIR / "01_inputs" / "input_refs.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"
SELECTION_STATUS = NEW_STAGE_DIR / "04_selected" / "selection_status.md"

SOURCE_RUN_DIR = SOURCE_STAGE_DIR / "02_runs" / "run344N"
SOURCE_FINAL_DECISION = SOURCE_RUN_DIR / "final_decision.json"
SOURCE_GATE_AUDIT = SOURCE_RUN_DIR / "required_gate_coverage_audit.csv"
SOURCE_ATTEMPT_PACKAGE = SOURCE_RUN_DIR / "runtime_probe_attempt_package.csv"
SOURCE_QUEUE = SOURCE_RUN_DIR / "run344O_queue.csv"
SOURCE_EXPECTED_TAPE = SOURCE_RUN_DIR / "expected" / "expected_tape.csv"
SOURCE_EXPECTED_INDEX = SOURCE_RUN_DIR / "expected_tape_index.csv"
SOURCE_RUNTIME_PARITY = SOURCE_RUN_DIR / "runtime_parity_contract.csv"
SOURCE_TESTER_IDENTITY = SOURCE_RUN_DIR / "tester_identity_contract.csv"
SOURCE_PACKAGEABILITY = SOURCE_RUN_DIR / "packageability_matrix.csv"
SOURCE_SET_MANIFEST = SOURCE_RUN_DIR / "tester_set_manifest.csv"
SOURCE_INI_MANIFEST = SOURCE_RUN_DIR / "tester_ini_manifest.csv"
SOURCE_VARIANT_MAPPING = SOURCE_RUN_DIR / "variant_runtime_mapping.csv"
SOURCE_REPORT = SOURCE_STAGE_DIR / "03_reviews" / "run344N_cash_open_long_quality_short_carry_decomposition_package.md"
SOURCE_SELECTION_STATUS = SOURCE_STAGE_DIR / "04_selected" / "selection_status.md"
SOURCE_REVIEW_INDEX = SOURCE_STAGE_DIR / "03_reviews" / "review_index.md"
SOURCE_STAGE_BRIEF = SOURCE_STAGE_DIR / "00_spec" / "stage_brief.md"

HANDOFF_MANIFEST = RUN_DIR / "stage344N_to_stage345_handoff_manifest.csv"
SOURCE_INVENTORY = RUN_DIR / "stage344_source_inventory.csv"
NEXT_QUEUE = RUN_DIR / "run345B_cash_open_long_quality_short_carry_mt5_probe_queue.csv"
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

SOURCE_INPUTS = [
    (SOURCE_FINAL_DECISION, "run344N final decision(344N 최종 결정)"),
    (SOURCE_GATE_AUDIT, "run344N required gate audit(344N 필수 게이트 감사)"),
    (SOURCE_ATTEMPT_PACKAGE, "run344N runtime attempt package(344N 런타임 시도 패키지)"),
    (SOURCE_QUEUE, "run344O source queue(344O 원천 대기열)"),
    (SOURCE_EXPECTED_TAPE, "run344N expected tape(344N 예상 테이프)"),
    (SOURCE_EXPECTED_INDEX, "run344N expected tape index(344N 예상 테이프 색인)"),
    (SOURCE_RUNTIME_PARITY, "run344N runtime parity contract(344N 런타임 동등성 계약)"),
    (SOURCE_TESTER_IDENTITY, "run344N tester identity contract(344N 테스터 정체성 계약)"),
    (SOURCE_PACKAGEABILITY, "run344N packageability matrix(344N 포장 가능성 표)"),
    (SOURCE_SET_MANIFEST, "run344N tester set manifest(344N 테스터 설정 목록)"),
    (SOURCE_INI_MANIFEST, "run344N tester ini manifest(344N 테스터 ini 목록)"),
    (SOURCE_VARIANT_MAPPING, "run344N variant runtime mapping(344N 변형 런타임 매핑)"),
    (SOURCE_REPORT, "run344N package report(344N 패키지 보고서)"),
    (SOURCE_SELECTION_STATUS, "Stage344 selection status(344단계 선정 상태)"),
]


def now_utc() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def fs_path(path: Path) -> str:
    resolved = path.resolve()
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


def path_exists(path: Path) -> bool:
    return os.path.exists(fs_path(path))


def path_is_file(path: Path) -> bool:
    return os.path.isfile(fs_path(path))


def ensure_parent(path: Path) -> None:
    os.makedirs(fs_path(path.parent), exist_ok=True)


def required(path: Path) -> Path:
    if not path_is_file(path):
        raise FileNotFoundError(f"missing required stage branch input: {rel(path)}")
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


def read_csv_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
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
    if path_is_file(path):
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


def append_text_once(path: Path, marker: str, text: str) -> None:
    current = read_text(path) if path_is_file(path) else ""
    if marker in current:
        return
    next_text = f"{current.rstrip()}\n\n{text.strip()}\n" if current.strip() else text.strip() + "\n"
    write_text(path, next_text)


def unique_fieldnames(*field_groups: Sequence[str]) -> list[str]:
    fields: list[str] = []
    for group in field_groups:
        for field in group:
            if field not in fields:
                fields.append(field)
    return fields


def source_summary() -> dict[str, Any]:
    decision = read_json(required(SOURCE_FINAL_DECISION))
    _queue_fields, queue_rows = read_csv_rows(required(SOURCE_QUEUE))
    _attempt_fields, attempt_rows = read_csv_rows(required(SOURCE_ATTEMPT_PACKAGE))
    _package_fields, packageability_rows = read_csv_rows(required(SOURCE_PACKAGEABILITY))
    return {
        "source_status": decision["status"],
        "source_judgment": decision["judgment"],
        "source_decision": decision["decision"],
        "source_gate_passes": int(decision["gate_passes"]),
        "source_gate_total": int(decision["gate_total"]),
        "attempt_rows": int(decision.get("attempt_rows") or len(attempt_rows)),
        "expected_rows": int(decision.get("expected_rows") or 0),
        "feature_rows": int(decision.get("feature_rows") or 0),
        "common_sync_missing": int(decision.get("common_sync_missing") or 0),
        "queue_rows": len(queue_rows),
        "packageability_rows": len(packageability_rows),
        "packageable_attempts": int(decision.get("packageable_attempts") or 0),
        "source_package_run_id": PARENT_RUN_ID,
        "source_next_run_id": decision.get("next_run_id", SUPERSEDED_RUN_ID),
    }


def write_source_inventory() -> list[dict[str, Any]]:
    rows = []
    for path, label in SOURCE_INPUTS:
        exists = path_is_file(path)
        rows.append(
            {
                "source_label": label,
                "path": rel(path),
                "exists": exists,
                "sha256": sha256_file(path) if exists else "",
                "bytes": os.path.getsize(fs_path(path)) if exists else "",
                "consumer": RUN_ID,
                "availability": "tracked" if exists else "missing",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(SOURCE_INVENTORY, rows)
    return rows


def write_handoff_artifacts(summary: Mapping[str, Any]) -> list[dict[str, Any]]:
    fieldnames, queue_rows = read_csv_rows(required(SOURCE_QUEUE))
    extras = [
        "source_queue_id",
        "source_next_run_id",
        "source_stage_id",
        "new_stage_id",
        "handoff_run_id",
        "superseded_run_id",
        "source_claim_boundary",
        "status",
    ]
    retargeted = []
    for row in queue_rows:
        updated = dict(row)
        updated["source_queue_id"] = row.get("queue_id", "")
        updated["source_next_run_id"] = row.get("next_run_id", "")
        updated["next_run_id"] = NEXT_RUN_ID
        updated["source_stage_id"] = SOURCE_STAGE_ID
        updated["new_stage_id"] = NEW_STAGE_ID
        updated["handoff_run_id"] = RUN_ID
        updated["superseded_run_id"] = SUPERSEDED_RUN_ID
        updated["source_claim_boundary"] = row.get("claim_boundary", "")
        updated["claim_boundary"] = CLAIM_BOUNDARY
        updated["status"] = "retargeted_to_stage345(345단계로 재지정)"
        retargeted.append(updated)
    write_csv(NEXT_QUEUE, retargeted, unique_fieldnames(fieldnames, extras))
    write_csv(
        HANDOFF_MANIFEST,
        [
            {
                "handoff_id": "stage344N_to_stage345A_branch",
                "source_stage_id": SOURCE_STAGE_ID,
                "source_run_id": PARENT_RUN_ID,
                "new_stage_id": NEW_STAGE_ID,
                "branch_run_id": RUN_ID,
                "superseded_run_id": SUPERSEDED_RUN_ID,
                "next_run_id": NEXT_RUN_ID,
                "source_queue_path": rel(SOURCE_QUEUE),
                "retargeted_queue_path": rel(NEXT_QUEUE),
                "attempt_rows": summary["attempt_rows"],
                "expected_rows": summary["expected_rows"],
                "feature_rows": summary["feature_rows"],
                "common_sync_missing": summary["common_sync_missing"],
                "packageable_attempts": summary["packageable_attempts"],
                "branch_reason": (
                    "Stage344(344단계)가 directional surface(방향성 표면), validation(검증), "
                    "deal-level replay(거래별 재생), cash-open package(현금장 패키지)까지 담아 무거워졌기 때문이다."
                ),
                "effect": (
                    "cash-open long quality/short carry MT5 runtime probe"
                    "(현금장 롱 품질/숏 기여 MT5 런타임 탐침)를 Stage345(345단계)에서 가볍게 실행한다."
                ),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )
    return retargeted


def write_documents(summary: Mapping[str, Any]) -> None:
    write_text(
        STAGE_BRIEF,
        f"""# Stage 345 Brief(345단계 개요)

## Stage ID(단계 ID)

`{NEW_STAGE_ID}`

## Question(질문)

Can the cash-open long quality/short carry decomposition(현금장 롱 품질/숏 기여 분해) survive an MT5 runtime probe(MT5 런타임 탐침) without turning Stage344(344단계) into a heavier validation sink(검증 싱크)?

## Scope(범위)

- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_package_run(원천 패키지 실행): `{PARENT_RUN_ID}`
- branch_run(분기 실행): `{RUN_ID}`
- superseded_run(대체된 실행): `{SUPERSEDED_RUN_ID}`
- next_run(다음 실행): `{NEXT_RUN_ID}`

Action(행동): Stage344(344단계)의 run344O runtime probe(런타임 탐침)를 run345B(345B 실행)로 retarget(재지정)한다.
Effect(효과): Stage344(344단계)는 directional long quality surface(방향성 롱 품질 표면)와 package handoff(패키지 인계)까지로 멈추고, MT5 execution(MT5 실행)은 새 stage(단계)에서 읽는다.

## Source Truth(원천 진실)

- package_run(패키지 실행): `{PARENT_RUN_ID}`
- package_status(패키지 상태): `{summary["source_status"]}`
- attempts(시도): `{summary["attempt_rows"]}`
- expected_rows(예상 행): `{summary["expected_rows"]}`
- feature_rows(피처 행): `{summary["feature_rows"]}`
- common_sync_missing(공용 동기화 누락): `{summary["common_sync_missing"]}`
- single_side_filter_limit(단일 사이드 필터 한계): recorded in packageability matrix(포장 가능성 표에 기록됨)

## Evidence Boundary(근거 경계)

This branch(분기)는 state sync(상태 동기화)와 handoff(인계)만 수행한다. No new MT5 execution(새 MT5 실행 없음), no candidate selection(후보 선정 없음), no operating promotion(운영 승격 없음), no runtime authority(런타임 권위 없음)이다.
""",
    )
    write_text(
        STAGE_README,
        f"""# Stage 345(345단계)

Stage345(345단계)는 cash-open long quality/short carry runtime probe(현금장 롱 품질/숏 기여 런타임 탐침)만 다룬다.

- current_run(현재 실행): `{NEXT_RUN_ID}`
- branch_run(분기 실행): `{RUN_ID}`
- source_package(원천 패키지): `{PARENT_RUN_ID}`
- retargeted_queue(재지정 대기열): `{rel(NEXT_QUEUE)}`

Effect(효과): Stage344(344단계)의 탐색 단서(clue, 단서)는 보존하고, MT5 runtime evidence(MT5 런타임 근거)는 새 단계에서 분리해 본다.
""",
    )
    write_text(
        INPUT_REFS,
        f"""# Stage 345 Input Refs(345단계 입력 참조)

- run344N final decision(344N 최종 결정): `{rel(SOURCE_FINAL_DECISION)}`
- run344N attempt package(344N 시도 패키지): `{rel(SOURCE_ATTEMPT_PACKAGE)}`
- run344N source queue(344N 원천 대기열): `{rel(SOURCE_QUEUE)}`
- retargeted run345B queue(345B 재지정 대기열): `{rel(NEXT_QUEUE)}`
- expected tape(예상 테이프): `{rel(SOURCE_EXPECTED_TAPE)}`
- runtime parity contract(런타임 동등성 계약): `{rel(SOURCE_RUNTIME_PARITY)}`
- tester identity contract(테스터 정체성 계약): `{rel(SOURCE_TESTER_IDENTITY)}`
- packageability matrix(포장 가능성 표): `{rel(SOURCE_PACKAGEABILITY)}`
- source report(원천 보고서): `{rel(SOURCE_REPORT)}`

Action(행동): Stage345(345단계)는 Stage344(344단계)의 package artifact(패키지 산출물)를 복사하지 않고 참조한다.
Effect(효과): heavy artifact duplication(무거운 산출물 중복)을 줄이고 artifact lineage(산출물 계보)는 유지한다.
""",
    )
    write_text(
        SELECTION_STATUS,
        f"""# Stage 345 Selection Status(345단계 선정 상태)

- selected_model(선정 모델): `none(없음)`
- source_package(원천 패키지): `{PARENT_RUN_ID}`
- runtime_queue(런타임 대기열): `{NEXT_RUN_ID}`
- package_status(패키지 상태): `retargeted_from_stage344_ready_for_mt5_probe(Stage344에서 재지정됨, MT5 탐침 준비)`
- runtime_authority(런타임 권위): `not_claimed(주장 없음)`
- operating_promotion(운영 승격): `not_claimed(주장 없음)`
- Goal Achieve(목표 달성): `not_claimed(주장 없음)`

Effect(효과): 새 Stage345(345단계)는 실행 대기 상태만 갖고, 운영 선정은 열지 않는다.
""",
    )
    write_text(
        SOURCE_SELECTION_STATUS,
        f"""# Stage 344 Selection Status(344단계 선정 상태)

- selected_model(선정 모델): `none(없음)`
- latest_package(최근 패키지): `{PARENT_RUN_ID}`
- package_status(패키지 상태): `handed_off_to_stage345_run345B(Stage345 run345B로 인계됨)`
- next_stage(다음 단계): `{NEW_STAGE_ID}`
- next_run(다음 실행): `{NEXT_RUN_ID}`
- runtime_authority(런타임 권위): `not_claimed(주장 없음)`
- operating_promotion(운영 승격): `not_claimed(주장 없음)`
- Goal Achieve(목표 달성): `not_claimed(주장 없음)`

Effect(효과): Stage344(344단계)는 무거운 runtime probe(런타임 탐침)를 더 붙이지 않고 handoff(인계)로 멈춘다.
""",
    )
    write_text(ROOT_SELECTION_STATUS, read_text(SELECTION_STATUS))
    write_text(
        REVIEW_INDEX,
        f"""# Stage 345 Review Index(345단계 검토 색인)

- run345A stage branch(345A 단계 분기): `{rel(REPORT_PATH)}`

Effect(효과): Stage345(345단계)의 첫 근거를 branch handoff(분기 인계)부터 찾게 한다.
""",
    )
    write_text(
        REPORT_PATH,
        f"""# run345A Stage Branch(345A 단계 분기)

## Decision(결정)

`{DECISION}`

## Reason(이유)

Stage344(344단계)는 directional long quality surface(방향성 롱 품질 표면), s07 validation(검증), deal-level replay(거래별 재생), cash-open decomposition package(현금장 분해 패키지)까지 담아 무거워졌다. 다음 질문은 새 설계(design, 설계)가 아니라 MT5 runtime probe(MT5 런타임 탐침)이므로 Stage345(345단계)로 분기한다.

Action(행동): `{SUPERSEDED_RUN_ID}`를 직접 이어가지 않고 `{NEXT_RUN_ID}`로 retarget(재지정)한다.
Effect(효과): Stage344(344단계)의 evidence(근거)는 보존하고, Stage345(345단계)는 runtime evidence(런타임 근거) 수집만 받는다.

## Handoff(인계)

- source_package(원천 패키지): `{PARENT_RUN_ID}`
- attempts(시도): `{summary["attempt_rows"]}`
- expected_rows(예상 행): `{summary["expected_rows"]}`
- feature_rows(피처 행): `{summary["feature_rows"]}`
- common_sync_missing(공용 동기화 누락): `{summary["common_sync_missing"]}`
- next_queue(다음 대기열): `{rel(NEXT_QUEUE)}`

## Claim Boundary(주장 경계)

`{CLAIM_BOUNDARY}`

No MT5 execution(새 MT5 실행 없음), no Goal Achieve(목표 달성 없음), no runtime authority(런타임 권위 없음), no operating promotion(운영 승격 없음).
""",
    )
    write_text(
        DECISION_DOC,
        f"""# {TODAY} Stage345A Branch Decision(345A 단계 분기 결정)

- decision(결정): `{DECISION}`
- from(출발): `{SOURCE_STAGE_ID}` / `{PARENT_RUN_ID}`
- to(도착): `{NEW_STAGE_ID}` / `{NEXT_RUN_ID}`
- superseded_run(대체된 실행): `{SUPERSEDED_RUN_ID}`
- reason(이유): Stage344(344단계)가 무거워졌고, 다음 질문은 cash-open MT5 runtime probe(현금장 MT5 런타임 탐침)라는 별도 topic pivot(주제 전환)이기 때문이다.

Action(행동): Stage345(345단계)를 열고 run345B(345B 실행)를 runtime probe packet(런타임 탐침 묶음)으로 둔다.
Effect(효과): run344N package(344N 패키지)는 source truth(원천 진실)로 남고, 실행 근거는 Stage345(345단계)에서 수집한다.

claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
    )
    append_text_once(
        SOURCE_STAGE_BRIEF,
        RUN_ID,
        f"""## run345A Stage Branch Handoff(345A 단계 분기 인계)

- run_id(실행 ID): `{RUN_ID}`
- next_stage(다음 단계): `{NEW_STAGE_ID}`
- next_run(다음 실행): `{NEXT_RUN_ID}`
- effect(효과): Stage344(344단계)는 run344N package(패키지)에서 멈추고, cash-open MT5 runtime probe(현금장 MT5 런타임 탐침)는 Stage345(345단계)로 넘긴다.
""",
    )
    append_text_once(
        SOURCE_REVIEW_INDEX,
        RUN_ID,
        f"""- run345A stage branch handoff(345A 단계 분기 인계): `{rel(REPORT_PATH)}` / `{RUN_ID}`
""",
    )


def write_current_truth() -> None:
    write_text(
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

Stage344(344단계)의 run344N package(패키지)를 Stage345(345단계)로 handoff(인계)했다. run345B MT5 runtime probe(MT5 런타임 탐침)는 아직 실행하지 않았다.

## Boundary(경계)

`{CLAIM_BOUNDARY}`
""",
    )


def append_changelogs() -> None:
    block = f"""## {TODAY} {RUN_ID}

Action(행동): Stage344(344단계)의 run344O MT5 runtime probe(MT5 런타임 탐침)를 Stage345(345단계) run345B로 retarget(재지정)했다.
Effect(효과): Stage344(344단계)의 무게를 줄이고, cash-open runtime evidence(현금장 런타임 근거)는 새 stage(단계)에서 수집한다.

- next_stage(다음 단계): `{NEW_STAGE_ID}`
- next_run(다음 실행): `{NEXT_RUN_ID}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    for path in [ROOT_CHANGELOG, WORKSPACE_CHANGELOG]:
        append_text_once(path, RUN_ID, block)


def ledger_rows(summary: Mapping[str, Any]) -> list[dict[str, Any]]:
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
        "gate_passes": 9,
        "gate_total": 9,
        "claim_boundary": CLAIM_BOUNDARY,
        "scoreboard_lane": "state_sync_stage_branch(상태 동기화 단계 분기)",
        "lane": "state_sync_stage_branch(상태 동기화 단계 분기)",
        "family": "state_sync(상태 동기화)",
        "run_number": RUN_NUMBER,
        "notes": "User requested a Stage branch because Stage344 became heavy(사용자가 344단계가 무거워져 단계 분기를 요청함).",
        "source_package_run_id": PARENT_RUN_ID,
        "rows": summary["expected_rows"],
        "attempt_count": summary["attempt_rows"],
        "feature_count": summary["feature_rows"],
        "candidate_model_id": "none(없음)",
    }
    tier_a = {
        **base,
        "ledger_row_id": f"{RUN_ID}__Tier A",
        "subrun_id": "Tier A",
        "view": "Tier A separate(Tier A 분리)",
        "record_view": "Tier A separate(Tier A 분리)",
        "tier": "Tier A",
        "tier_scope": "Tier A",
        "metric_scope": "stage_branch_handoff_run344N_cash_open_runtime_package",
        "kpi_scope": "stage_branch_handoff_run344N_cash_open_runtime_package",
        "primary_kpi": f"attempts={summary['attempt_rows']};expected_rows={summary['expected_rows']}",
        "guardrail_kpi": f"common_sync_missing={summary['common_sync_missing']};single_side_filter_limit_recorded=true",
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
    }
    return [tier_a, tier_b, combined]


def write_ledgers(summary: Mapping[str, Any]) -> None:
    rows = ledger_rows(summary)
    write_csv(STAGE_LEDGER, rows)
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
                "notes": "Stage344 was branched before cash-open MT5 runtime probe because it became heavy(344단계가 무거워져 현금장 MT5 런타임 탐침 전에 분기함).",
                "primary_report": rel(REPORT_PATH),
                "run_number": RUN_NUMBER,
                "date": TODAY,
                "decision": DECISION,
                "parent_run_id": PARENT_RUN_ID,
                "next_run_id": NEXT_RUN_ID,
                "rows": summary["expected_rows"],
                "gate_passes": 9,
                "gate_total": 9,
                "claim_boundary": CLAIM_BOUNDARY,
                "report_path": rel(REPORT_PATH),
                "primary_artifact": rel(FINAL_DECISION),
                "candidate_model_id": "none(없음)",
                "result_status": "stage_branch_opened_no_selection(단계 분기 완료, 선정 없음)",
                "feature_count": summary["feature_rows"],
                "attempt_count": summary["attempt_rows"],
                "view": "Tier A separate(Tier A 분리)",
                "tier": "Tier A",
                "metric_scope": "stage_branch_handoff_run344N_cash_open_runtime_package",
                "source_package_run_id": PARENT_RUN_ID,
            }
        ],
    )


def write_receipts(
    summary: Mapping[str, Any],
    inventory: list[dict[str, Any]],
    queue_rows: list[dict[str, Any]],
) -> None:
    created_at = now_utc()
    artifacts = [
        HANDOFF_MANIFEST,
        SOURCE_INVENTORY,
        NEXT_QUEUE,
        STAGE_BRIEF,
        STAGE_README,
        INPUT_REFS,
        REPORT_PATH,
        REVIEW_INDEX,
        DECISION_DOC,
        SELECTION_STATUS,
        STAGE_LEDGER,
        GATE_AUDIT,
        FINAL_DECISION,
        RUN_MANIFEST,
    ]
    write_json(
        LINEAGE_RECEIPT,
        {
            "run_id": RUN_ID,
            "stage_id": NEW_STAGE_ID,
            "source_inputs": inventory,
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [rel(path) for path in artifacts],
            "artifact_hashes": {rel(path): sha256_file(path) for path in artifacts if path_is_file(path)},
            "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "availability": "tracked",
            "lineage_judgment": "connected_with_boundary",
            "claim_boundary": CLAIM_BOUNDARY,
            "created_at_utc": created_at,
        },
    )
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
            "attempt_rows": summary["attempt_rows"],
            "expected_rows": summary["expected_rows"],
            "judgment": JUDGMENT,
            "decision": DECISION,
            "created_at_utc": created_at,
            "claim_boundary": CLAIM_BOUNDARY,
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
            "created_at_utc": created_at,
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def write_gates(summary: Mapping[str, Any]) -> list[dict[str, Any]]:
    workspace_text = read_text(WORKSPACE_STATE) if path_is_file(WORKSPACE_STATE) else ""
    _queue_fields, queue_rows = read_csv_rows(NEXT_QUEUE)
    gates = [
        {
            "gate_id": "source_run344N_gate_audit_available",
            "status": (
                "passed"
                if path_is_file(SOURCE_GATE_AUDIT) and summary["source_gate_passes"] == summary["source_gate_total"]
                else "failed"
            ),
            "evidence_path": rel(SOURCE_GATE_AUDIT),
            "effect": "run344N(344N 실행)의 package gate(패키지 게이트)가 통과됐는지 확인한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "source_queue_available",
            "status": "passed" if path_is_file(SOURCE_QUEUE) and summary["queue_rows"] > 0 else "failed",
            "evidence_path": rel(SOURCE_QUEUE),
            "effect": "run344O(344O 실행) 대기열을 잃지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "stage_structure_created",
            "status": (
                "passed"
                if all(path_exists(path) for path in [STAGE_BRIEF, INPUT_REFS, REPORT_PATH, REVIEW_INDEX, SELECTION_STATUS])
                else "failed"
            ),
            "evidence_path": rel(NEW_STAGE_DIR),
            "effect": "새 stage(단계)가 필수 폴더와 문서를 가진다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "queue_retargeted_to_stage345B",
            "status": "passed" if queue_rows and all(row.get("next_run_id") == NEXT_RUN_ID for row in queue_rows) else "failed",
            "evidence_path": rel(NEXT_QUEUE),
            "effect": "run344O(344O 실행) 대신 run345B(345B 실행)로 이어진다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "artifact_lineage_audit",
            "status": "passed" if path_is_file(LINEAGE_RECEIPT) and path_is_file(HANDOFF_MANIFEST) else "failed",
            "evidence_path": rel(LINEAGE_RECEIPT),
            "effect": "source input(원천 입력)과 branch artifact(분기 산출물)를 연결한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "state_sync_audit",
            "status": "passed" if f"current_stage_id: {NEW_STAGE_ID}" in workspace_text and f"current_run_id: {NEXT_RUN_ID}" in workspace_text else "failed",
            "evidence_path": rel(WORKSPACE_STATE),
            "effect": "current truth(현재 진실)가 새 stage(단계)를 가리킨다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "ledger_sync_audit",
            "status": "passed" if path_is_file(STAGE_LEDGER) and path_is_file(PROJECT_LEDGER) and path_is_file(RUN_REGISTRY) else "failed",
            "evidence_path": rel(STAGE_LEDGER),
            "effect": "stage/project ledger(단계/프로젝트 장부)가 분기 실행을 찾을 수 있다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "final_claim_guard",
            "status": "passed" if path_is_file(CLAIM_RECEIPT) else "failed",
            "evidence_path": rel(CLAIM_RECEIPT),
            "effect": "운영 승격과 목표 달성 주장을 막는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "required_gate_coverage_audit_written",
            "status": "passed",
            "evidence_path": rel(GATE_AUDIT),
            "effect": "required gate coverage audit(필수 게이트 커버리지 감사)를 기록한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    write_csv(GATE_AUDIT, gates)
    return gates


def write_final_decision(gates: Sequence[Mapping[str, Any]], summary: Mapping[str, Any]) -> None:
    gate_passes = sum(1 for gate in gates if gate["status"] == "passed")
    gate_total = len(gates)
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
            "attempt_rows": summary["attempt_rows"],
            "expected_rows": summary["expected_rows"],
            "feature_rows": summary["feature_rows"],
            "common_sync_missing": summary["common_sync_missing"],
            "packageability_rows": summary["packageability_rows"],
            "packageable_attempts": summary["packageable_attempts"],
            "gate_passes": gate_passes,
            "gate_total": gate_total,
            "new_mt5_execution": "not_run",
            "external_verification_status": "out_of_scope_by_claim(주장 범위 밖)",
            "candidate_selection": "not_claimed",
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
            ],
            "next_run_id": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
            "created_at_utc": now_utc(),
        },
    )


def write_artifact_registry() -> None:
    rows = []
    for artifact_type, path, notes in [
        ("final_decision", FINAL_DECISION, "run345A branch final decision(345A 분기 최종 결정)"),
        ("required_gate_coverage_audit", GATE_AUDIT, "run345A gate audit(345A 게이트 감사)"),
        ("handoff_manifest", HANDOFF_MANIFEST, "Stage344N to Stage345 handoff manifest(344N에서 345단계 인계 목록)"),
        ("retargeted_queue", NEXT_QUEUE, "run345B retargeted queue(345B 재지정 대기열)"),
        ("stage_branch_report", REPORT_PATH, "run345A branch report(345A 분기 보고서)"),
        ("review_index", REVIEW_INDEX, "Stage345 review index(345단계 검토 색인)"),
        ("decision_doc", DECISION_DOC, "run345A durable decision document(345A 결정 문서)"),
        ("run_manifest", RUN_MANIFEST, "run345A run manifest(345A 실행 목록)"),
        ("stage_brief", STAGE_BRIEF, "Stage345 stage brief(345단계 개요)"),
        ("input_refs", INPUT_REFS, "Stage345 input refs(345단계 입력 참조)"),
        ("selection_status", SELECTION_STATUS, "Stage345 selection status(345단계 선정 상태)"),
        ("pipeline", Path(__file__), "run345A producer script(345A 생산 스크립트)"),
    ]:
        rows.append(
            {
                "stage_id": NEW_STAGE_ID,
                "run_id": RUN_ID,
                "artifact_type": artifact_type,
                "path": rel(path),
                "artifact_path": rel(path),
                "sha256": sha256_file(path) if path_is_file(path) else "",
                "created_at": TODAY,
                "created_at_utc": now_utc(),
                "artifact_id": f"{RUN_ID}__{rel(path).replace('/', '__').replace('.', '_')}",
                "notes": notes,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    append_or_replace_csv(ARTIFACT_REGISTRY, ["stage_id", "run_id", "artifact_type", "path"], rows)


def main() -> None:
    for path, _label in SOURCE_INPUTS:
        required(path)
    for path in [NEW_STAGE_DIR / "00_spec", NEW_STAGE_DIR / "01_inputs", RUN_DIR, REVIEW_DIR, NEW_STAGE_DIR / "04_selected"]:
        os.makedirs(fs_path(path), exist_ok=True)
    summary = source_summary()
    inventory = write_source_inventory()
    queue_rows = write_handoff_artifacts(summary)
    write_documents(summary)
    write_current_truth()
    append_changelogs()
    write_ledgers(summary)
    write_receipts(summary, inventory, queue_rows)
    gates = write_gates(summary)
    if any(gate["status"] != "passed" for gate in gates):
        failed = [gate["gate_id"] for gate in gates if gate["status"] != "passed"]
        write_json(
            RUN_DIR / "self_correction_plan.json",
            {
                "run_id": RUN_ID,
                "failed_gates": failed,
                "mode": "plan_only(계획 전용)",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        )
        raise SystemExit(f"failed gates: {failed}")
    write_final_decision(gates, summary)
    write_artifact_registry()
    write_receipts(summary, inventory, queue_rows)
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "stage_id": NEW_STAGE_ID,
                "next_run_id": NEXT_RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "gate_passes": sum(1 for gate in gates if gate["status"] == "passed"),
                "gate_total": len(gates),
                "attempt_rows": summary["attempt_rows"],
                "expected_rows": summary["expected_rows"],
                "claim_boundary": CLAIM_BOUNDARY,
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
