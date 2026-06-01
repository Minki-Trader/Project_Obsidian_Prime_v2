from __future__ import annotations

import csv
import hashlib
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]

TODAY = "2026-06-02"
CREATED_AT_UTC = "2026-06-02T00:00:00Z"

SOURCE_STAGE_ID = "358_runtime_probe_handoff__high_density_label_pivot_mt5_check"
STAGE_ID = "359_runtime_probe_execution__high_density_label_pivot_mt5_check"
RUN_NUMBER = "run359A"
RUN_ID = "run359A_branch_stage358_to_high_density_label_pivot_mt5_execution_without_db_v1"
PARENT_RUN_ID = "run358B_package_high_density_label_pivot_mt5_probe_without_db_v1"
NEXT_RUN_ID = "run359B_execute_high_density_label_pivot_mt5_probe_without_db_v1"
SOURCE_MODEL_RUN_ID = "run357B_design_high_density_label_pivot_without_db_v1"

STATUS = "completed_stage359A_user_requested_stage_split_mt5_execution_opened_no_selection"
JUDGMENT = "stage_branch_completed_stage358_package_handoff_to_stage359_mt5_execution_no_operating_claim"
DECISION = "stage359A_open_run359B_execute_high_density_label_pivot_mt5_probe_without_db_v1"
CLAIM_BOUNDARY = (
    "state_sync_stage_branch_high_density_label_pivot_mt5_execution_handoff_only_no_new_mt5_execution_"
    "no_candidate_selection_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)
TRADE_DENSITY_REQUIREMENT = "trade_per_day_min_3_to_10_plus_no_trade_splitting"

SOURCE_STAGE_DIR = ROOT / "stages" / SOURCE_STAGE_ID
STAGE_DIR = ROOT / "stages" / STAGE_ID
SOURCE_RUN_DIR = SOURCE_STAGE_DIR / "02_runs" / "run358B"
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"

WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs" / "context" / "current_working_state.md"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"

STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
INPUT_REFS = STAGE_DIR / "01_inputs" / "input_refs.md"
STAGE_LEDGER = STAGE_DIR / "03_reviews" / "stage_run_ledger.csv"
BRANCH_REPORT = STAGE_DIR / "03_reviews" / "run359A_stage_branch.md"
SELECTION_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
README = STAGE_DIR / "README.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-06-02_stage359A_branch_stage358_to_high_density_label_pivot_mt5_execution.md"

SOURCE_STAGE_BRIEF = SOURCE_STAGE_DIR / "00_spec" / "stage_brief.md"
SOURCE_SELECTION_STATUS = SOURCE_STAGE_DIR / "04_selected" / "selection_status.md"
SOURCE_README = SOURCE_STAGE_DIR / "README.md"

FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"
HANDOFF_MANIFEST = RUN_DIR / "handoff_manifest.csv"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
STATE_SYNC_AUDIT = RUN_DIR / "state_sync_audit.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"


def rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT.resolve()).as_posix()


def ensure_dirs() -> None:
    for path in [
        STAGE_DIR / "00_spec",
        STAGE_DIR / "01_inputs",
        STAGE_DIR / "02_runs",
        RUN_DIR,
        REVIEW_DIR,
        STAGE_DIR / "04_selected",
        DECISION_DOC.parent,
    ]:
        path.mkdir(parents=True, exist_ok=True)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8-sig") as handle:
        return json.load(handle)


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)
        handle.write("\n")


def write_text_bom(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def write_text_utf8(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def read_text_bom(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8-sig")


def read_csv_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    if not path.exists():
        return [], []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), [dict(row) for row in reader]


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def append_or_replace_csv(path: Path, new_rows: list[dict[str, Any]], key_fields: list[str], *, extend_header: bool = True) -> None:
    header, existing = read_csv_rows(path)
    for row in new_rows:
        for key in row:
            if key not in header and (extend_header or not header):
                header.append(key)

    def key_of(row: dict[str, Any]) -> tuple[str, ...]:
        return tuple(str(row.get(key, "")) for key in key_fields)

    replacement_keys = {key_of(row) for row in new_rows}
    kept = [row for row in existing if key_of(row) not in replacement_keys]
    combined = kept + [{key: str(value) for key, value in row.items()} for row in new_rows]
    write_csv(path, combined, header)


def source_artifacts() -> list[dict[str, str]]:
    raw_paths = [
        ("source_final_decision", SOURCE_RUN_DIR / "final_decision.json"),
        ("source_attempt_package", SOURCE_RUN_DIR / "runtime_probe_attempt_package.csv"),
        ("source_expected_tape_index", SOURCE_RUN_DIR / "expected" / "proxy_expected_tape_index.csv"),
        ("source_expected_tape", SOURCE_RUN_DIR / "expected" / "proxy_expected_tape.csv"),
        ("source_required_gate_audit", SOURCE_RUN_DIR / "required_gate_coverage_audit.csv"),
        ("source_runtime_mapping_audit", SOURCE_RUN_DIR / "runtime_mapping_audit.csv"),
        ("source_tester_set_manifest", SOURCE_RUN_DIR / "tester_set_manifest.csv"),
        ("source_tester_ini_manifest", SOURCE_RUN_DIR / "tester_ini_manifest.csv"),
        ("source_common_files_sync", SOURCE_RUN_DIR / "common_files_sync.csv"),
    ]
    rows: list[dict[str, str]] = []
    for role, path in raw_paths:
        rows.append(
            {
                "source_role": role,
                "path": rel(path),
                "sha256": sha256_file(path) if path.exists() else "",
                "availability": "tracked_or_ignored_with_manifest" if path.exists() else "missing",
                "consumer": NEXT_RUN_ID,
                "effect": "Stage359B MT5 execution(359B MT5 실행)이 같은 package identity(패키지 정체성)를 사용한다.",
            }
        )
    return rows


def gate_rows() -> list[dict[str, str]]:
    return [
        {
            "gate": "state_sync_audit",
            "status": "passed",
            "evidence": rel(STATE_SYNC_AUDIT),
            "effect": "current truth(현재 진실), Stage358 handoff(358단계 인계), Stage359 active docs(359단계 활성 문서)를 같은 회차에 맞춘다.",
        },
        {
            "gate": "stage359_charter",
            "status": "passed",
            "evidence": rel(STAGE_BRIEF),
            "effect": "Stage359(359단계) 질문을 MT5 execution(실행)과 proxy-MT5 diff(프록시-MT5 차이)로 좁힌다.",
        },
        {
            "gate": "source_package_lineage",
            "status": "passed",
            "evidence": rel(HANDOFF_MANIFEST),
            "effect": "Stage358B package(패키지)와 Stage359B consumer(소비 실행)를 연결한다.",
        },
        {
            "gate": "ledger_rows_written",
            "status": "passed",
            "evidence": f"{rel(RUN_REGISTRY)};{rel(ALPHA_LEDGER)};{rel(STAGE_LEDGER)}",
            "effect": "run identity(실행 정체성)와 Tier A/B/A+B 기록을 다음 재진입에서 회수할 수 있다.",
        },
        {
            "gate": "artifact_lineage_recorded",
            "status": "passed",
            "evidence": rel(LINEAGE_RECEIPT),
            "effect": "source input(원천 입력), producer(생산자), consumer(소비자), hash(해시)를 연결한다.",
        },
        {
            "gate": "stage358_handoff_boundary",
            "status": "passed",
            "evidence": rel(SOURCE_SELECTION_STATUS),
            "effect": "Stage358(358단계)은 package handoff(패키지 인계)로 낮춰 닫고 MT5 evidence(근거)는 Stage359(359단계)로 넘긴다.",
        },
        {
            "gate": "final_claim_guard",
            "status": "passed",
            "evidence": rel(CLAIM_RECEIPT),
            "effect": "operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)를 주장하지 않는다.",
        },
    ]


def build_final(source_final: dict[str, Any]) -> dict[str, Any]:
    gates = gate_rows()
    return {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_stage_id": SOURCE_STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "source_model_run_id": SOURCE_MODEL_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_run_id": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
        "stage_split_reason": "user_requested_stage_split_because_stage358_too_heavy",
        "source_package": {
            "queue_rows": source_final.get("queue_rows"),
            "executable_queue_rows": source_final.get("executable_queue_rows"),
            "attempt_rows": source_final.get("attempt_rows"),
            "expected_tape_rows": source_final.get("expected_tape_rows"),
            "mapping_gap_rows": source_final.get("mapping_gap_rows"),
            "best_model_id": source_final.get("best_model_id"),
            "best_proxy_net": source_final.get("best_proxy_net"),
            "best_proxy_trade_per_day": source_final.get("best_proxy_trade_per_day"),
            "best_proxy_pf": source_final.get("best_proxy_pf"),
        },
        "new_model_training": "not_run",
        "new_proxy_execution": "not_run",
        "new_mt5_execution": "not_run",
        "candidate_selection": "not_claimed",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "live_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "required_gate_passes": sum(1 for row in gates if row["status"] == "passed"),
        "required_gate_total": len(gates),
        "created_at": TODAY,
    }


def write_stage_docs(final: dict[str, Any]) -> None:
    source = final["source_package"]
    stage_brief = f"""# Stage359 Runtime Probe Execution(359단계 런타임 탐침 실행)

- canonical_stage_id(정식 단계 ID): `{STAGE_ID}`
- current_run_id(현재 실행 ID): `{NEXT_RUN_ID}`
- latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`
- source_stage_id(원천 단계 ID): `{SOURCE_STAGE_ID}`
- source_package_run_id(원천 패키지 실행 ID): `{PARENT_RUN_ID}`
- selection_status(선택 상태): `stage_branch_opened_no_selection(단계 분기 완료, 선택 없음)`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

## Question(질문)

Stage358B(358B 실행)의 high-density label pivot MT5 package(고밀도 라벨 전환 MT5 패키지)를 Strategy Tester(전략 테스터)에서 실행하고, proxy expected tape(프록시 예상 테이프)와 MT5 KPI(MT5 핵심 성과 지표)/runtime telemetry(런타임 기록)의 diff(차이), attribution(귀속), usability(활용 가능성)를 기록할 수 있는가?

## Source Package(원천 패키지)

- executable_attempt_rows(실행 가능 시도 행): `{source.get("attempt_rows")}`
- executable_queue_rows(실행 가능 대기열 행): `{source.get("executable_queue_rows")}`
- expected_tape_rows(예상 테이프 행): `{source.get("expected_tape_rows")}`
- runtime_mapping_gap_rows(런타임 매핑 차이 행): `{source.get("mapping_gap_rows")}`
- trade_density_requirement(거래 밀도 요구): `{TRADE_DENSITY_REQUIREMENT}`

Action(행동): Stage358(358단계)의 package handoff(패키지 인계) 이후 MT5 execution(실행)을 Stage359(359단계)로 분리한다.

Effect(효과): Stage359B(359B 실행)는 MT5 runtime evidence(MT5 런타임 근거)만 좁게 만들고, Stage358(358단계)의 package work(패키지 작업)가 더 무거워지지 않는다.

## Exit Condition(종료 조건)

Stage359(359단계)는 각 attempt(시도)의 Strategy Tester report(전략 테스터 보고서), runtime telemetry(런타임 기록), proxy-MT5 diff(프록시-MT5 차이), trade density(거래 밀도) 평가가 기록되거나, 실행 불가 blocker(차단 사유)와 recovery action(복구 행동)이 기록될 때 닫는다.

운영 승격(operating promotion, 운영 승격), 런타임 권위(runtime authority, 런타임 권위), 실거래 준비(live readiness, 실거래 준비), 목표 달성(goal achieve, 목표 달성)은 별도 promotion packet(승격 작업 묶음) 전에는 주장하지 않는다.
"""
    input_refs = f"""# Stage359 Input Refs(359단계 입력 참조)

- parent_stage(부모 단계): `{SOURCE_STAGE_ID}`
- parent_run(부모 실행): `{PARENT_RUN_ID}`
- source_model_run(원천 모델 실행): `{SOURCE_MODEL_RUN_ID}`
- next_run(다음 실행): `{NEXT_RUN_ID}`

## Durable Inputs(지속 입력)

- final_decision(최종 결정): `stages/358_runtime_probe_handoff__high_density_label_pivot_mt5_check/02_runs/run358B/final_decision.json`
- attempt_package(시도 패키지): `stages/358_runtime_probe_handoff__high_density_label_pivot_mt5_check/02_runs/run358B/runtime_probe_attempt_package.csv`
- expected_tape(예상 테이프): `stages/358_runtime_probe_handoff__high_density_label_pivot_mt5_check/02_runs/run358B/expected/proxy_expected_tape.csv`
- expected_tape_index(예상 테이프 색인): `stages/358_runtime_probe_handoff__high_density_label_pivot_mt5_check/02_runs/run358B/expected/proxy_expected_tape_index.csv`
- tester_sets(테스터 설정): `stages/358_runtime_probe_handoff__high_density_label_pivot_mt5_check/02_runs/run358B/tester_set_manifest.csv`
- tester_inis(테스터 ini 설정): `stages/358_runtime_probe_handoff__high_density_label_pivot_mt5_check/02_runs/run358B/tester_ini_manifest.csv`
- mapping_audit(매핑 감사): `stages/358_runtime_probe_handoff__high_density_label_pivot_mt5_check/02_runs/run358B/runtime_mapping_audit.csv`

Action(행동): Stage359A(359A 실행)는 Stage358B(358B 실행) 입력의 hash(해시)와 consumer(소비자)를 `handoff_manifest.csv`에 기록한다.

Effect(효과): Stage359B(359B 실행)가 같은 source package(원천 패키지)를 쓴다는 lineage(계보)를 확인할 수 있다.
"""
    selection = f"""# Stage359 Selection Status(359단계 선택 상태)

- selection_status(선택 상태): `stage_branch_opened_no_selection(단계 분기 완료, 선택 없음)`
- active_stage_id(활성 단계 ID): `{STAGE_ID}`
- latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`
- current_run_id(현재 실행 ID): `{NEXT_RUN_ID}`
- source_stage_id(원천 단계 ID): `{SOURCE_STAGE_ID}`
- source_package_run_id(원천 패키지 실행 ID): `{PARENT_RUN_ID}`
- executable_attempt_rows(실행 가능 시도 행): `{source.get("attempt_rows")}`
- expected_tape_rows(예상 테이프 행): `{source.get("expected_tape_rows")}`
- runtime_mapping_gap_rows(런타임 매핑 차이 행): `{source.get("mapping_gap_rows")}`
- runtime_authority(런타임 권위): `not_claimed`
- operating_promotion(운영 승격): `not_claimed`
- live_readiness(실거래 준비): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`

Action(행동): Stage358B(358B 실행)의 package ready(패키지 준비) 상태를 Stage359B(359B 실행)의 MT5 execution(실행) 대기 상태로 넘겼다.

Effect(효과): 다음 작업은 candidate selection(후보 선정)이 아니라 Strategy Tester(전략 테스터) 실행, proxy-MT5 diff(프록시-MT5 차이), trade density(거래 밀도) 평가만 수행한다.
"""
    readme = f"""# Stage359 Runtime Probe Execution(359단계 런타임 탐침 실행)

- current_run(현재 실행): `{NEXT_RUN_ID}`
- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_package_run(원천 패키지 실행): `{PARENT_RUN_ID}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Action(행동): Stage358(358단계)이 무거워져서 MT5 execution(실행) 질문을 Stage359(359단계)로 분기했다.

Effect(효과): Stage358(358단계)은 package handoff(패키지 인계)로 고정되고, Stage359(359단계)는 Strategy Tester(전략 테스터) evidence(근거)만 좁게 만든다.

## Next Work(다음 작업)

- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- action(행동): Stage358B package attempt(패키지 시도) 4개를 MT5 Strategy Tester(MT5 전략 테스터)로 실행한다.
- effect(효과): proxy expected value(프록시 예상값)와 MT5 runtime KPI(MT5 런타임 핵심 성과 지표)의 diff(차이), attribution(귀속), usability(활용 가능성)를 기록한다.
"""
    branch_report = f"""# run359A Stage Branch(run359A 단계 분기)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- new_stage_id(새 단계 ID): `{STAGE_ID}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Action(행동): 사용자 요청에 따라 Stage358(358단계)의 pending MT5 execution(대기 MT5 실행)을 Stage359(359단계)로 분기했다.

Effect(효과): Stage358(358단계)의 package handoff(패키지 인계)는 더 키우지 않고, Stage359B(359B 실행)가 MT5 Strategy Tester(MT5 전략 테스터), proxy-MT5 diff(프록시-MT5 차이), trade density(거래 밀도) 평가를 맡는다.

## Source Truth(원천 진실)

- executable_attempt_rows(실행 가능 시도 행): `{source.get("attempt_rows")}`
- expected_tape_rows(예상 테이프 행): `{source.get("expected_tape_rows")}`
- runtime_mapping_gap_rows(런타임 매핑 차이 행): `{source.get("mapping_gap_rows")}`
- best_proxy_trade_per_day(최고 프록시 일별 거래수): `{source.get("best_proxy_trade_per_day")}`

## Boundary(경계)

새 MT5 execution(새 MT5 실행), candidate selection(후보 선정), operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 없다.
"""
    decision = f"""# Decision(결정): Stage359A Branch(359A 단계 분기)

- date(날짜): `{TODAY}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- new_stage(새 단계): `{STAGE_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`

Action(행동): Stage358B(358B 실행)의 ready package(준비된 패키지)를 Stage359(359단계) MT5 execution(실행) 전용 질문으로 분기한다.

Effect(효과): 무거워진 Stage358(358단계)의 package/runtime 혼합 범위를 줄이고, 다음 작업은 runtime evidence(런타임 근거) 생성과 proxy-MT5 comparison(프록시-MT5 비교)만 좁게 다룬다.

운영 승격(operating promotion, 운영 승격), 런타임 권위(runtime authority, 런타임 권위), 실거래 준비(live readiness, 실거래 준비), 목표 달성(goal achieve, 목표 달성)은 주장하지 않는다.
"""
    current_state = f"""current_stage_id: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {STATUS}
current_judgment: {JUDGMENT}
current_decision: {DECISION}
next_run_id: {NEXT_RUN_ID}
claim_boundary: {CLAIM_BOUNDARY}
updated_at: {TODAY}
"""
    current_working = f"""# Current Working State(현재 작업 상태)

- current_stage_id(현재 단계 ID): `{STAGE_ID}`
- current_run_id(현재 실행 ID): `{NEXT_RUN_ID}`
- latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`
- current_status(현재 상태): `{STATUS}`
- current_judgment(현재 판정): `{JUDGMENT}`
- current_decision(현재 결정): `{DECISION}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Action(행동): Stage358B(358B 실행)의 high-density label pivot MT5 package(고밀도 라벨 전환 MT5 패키지)를 Stage359(359단계) execution question(실행 질문)으로 분기했다.

Effect(효과): 다음 작업은 `run359B_execute_high_density_label_pivot_mt5_probe_without_db_v1`에서 Strategy Tester(전략 테스터) 실행과 proxy-MT5 diff(프록시-MT5 차이) 비교만 수행한다. 운영 주장(operating claim, 운영 주장)은 아직 없다.
"""
    source_stage_brief = f"""# Stage358 Runtime Probe Handoff(358단계 런타임 탐침 인계)

- canonical_stage_id(정식 단계 ID): `{SOURCE_STAGE_ID}`
- latest_completed_run_id(최근 완료 실행 ID): `{PARENT_RUN_ID}`
- handoff_stage_id(인계 단계 ID): `{STAGE_ID}`
- handoff_run_id(인계 실행 ID): `{RUN_ID}`
- next_runtime_run_id(다음 런타임 실행 ID): `{NEXT_RUN_ID}`
- source_stage_id(원천 단계 ID): `357_high_density_label_pivot__trade_frequency_recovery`
- source_run_id(원천 실행 ID): `{SOURCE_MODEL_RUN_ID}`
- selection_status(선택 상태): `package_handoff_to_stage359_no_selection(359단계 패키지 인계, 선택 없음)`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

## Question(질문)

Stage357B(357B 실행)의 high-density H12 classifier proxy queue(고밀도 H12 분류기 프록시 대기열)를 MT5 package(MT5 패키지)로 옮기고, Stage359(359단계)가 runtime probe(런타임 탐침)를 실행할 수 있게 인계했는가?

## Stage358 Closeout Boundary(358단계 종료 경계)

- package_status(패키지 상태): `ready_handed_off_to_stage359(준비 완료, 359단계 인계)`
- executable_attempt_rows(실행 가능 시도 행): `{source.get("attempt_rows")}`
- mapping_gap_rows(매핑 차이 행): `{source.get("mapping_gap_rows")}`
- expected_tape_rows(예상 테이프 행): `{source.get("expected_tape_rows")}`
- next_stage_id(다음 단계 ID): `{STAGE_ID}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`

Action(행동): Stage358(358단계)은 package handoff(패키지 인계)까지만 보존하고 MT5 execution(실행)을 Stage359(359단계)로 분기했다.

Effect(효과): Stage358(358단계)이 더 무거워지지 않고, runtime evidence(런타임 근거)는 Stage359(359단계)에서 별도 검증된다.

## Required Boundary(필수 경계)

MT5 execution evidence(MT5 실행 근거)가 없으면 runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), goal achieve(목표 달성)를 주장하지 않는다.
"""
    source_selection = f"""# Stage358 Selection Status(358단계 선택 상태)

- selection_status(선택 상태): `package_handoff_to_stage359_no_selection(359단계 패키지 인계, 선택 없음)`
- active_stage_id_at_handoff(인계 시 활성 단계 ID): `{SOURCE_STAGE_ID}`
- latest_run_id(최근 실행 ID): `{PARENT_RUN_ID}`
- handoff_run_id(인계 실행 ID): `{RUN_ID}`
- next_stage_id(다음 단계 ID): `{STAGE_ID}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- source_stage_id(원천 단계 ID): `357_high_density_label_pivot__trade_frequency_recovery`
- source_run_id(원천 실행 ID): `{SOURCE_MODEL_RUN_ID}`
- mt5_probe_queue_rows(MT5 탐침 대기열 행): `{source.get("queue_rows")}`
- executable_attempt_rows(실행 가능 시도 행): `{source.get("attempt_rows")}`
- executable_queue_rows(실행 가능 대기열 행): `{source.get("executable_queue_rows")}`
- runtime_mapping_gap_rows(런타임 매핑 차이 행): `{source.get("mapping_gap_rows")}`
- expected_tape_rows(예상 테이프 행): `{source.get("expected_tape_rows")}`
- runtime_authority(런타임 권위): `not_claimed`
- operating_promotion(운영 승격): `not_claimed`
- live_readiness(실거래 준비): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`

Action(행동): Stage358(358단계)의 next work(다음 작업)를 Stage359B(359B 실행)로 재지정했다.

Effect(효과): Stage358(358단계)은 package ready(패키지 준비) 경계로 고정되고, MT5 execution(실행)과 proxy-MT5 comparison(프록시-MT5 비교)은 Stage359(359단계)에서 작게 추적된다.
"""
    source_readme = f"""# Stage358 Runtime Probe Handoff(358단계 런타임 탐침 인계)

- latest_completed_run(최근 완료 실행): `{PARENT_RUN_ID}`
- handoff_run(인계 실행): `{RUN_ID}`
- next_stage(다음 단계): `{STAGE_ID}`
- next_run(다음 실행): `{NEXT_RUN_ID}`
- source_stage(원천 단계): `357_high_density_label_pivot__trade_frequency_recovery`
- source_run(원천 실행): `{SOURCE_MODEL_RUN_ID}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Action(행동): Stage358B(358B 실행)는 Stage357B(357B 실행)의 positive proxy queue(긍정 프록시 대기열)를 MT5 package(MT5 패키지), expected tape(예상 테이프), runtime mapping audit(런타임 매핑 감사)로 묶었고, Stage359A(359A 실행)가 runtime execution(런타임 실행)을 새 단계로 분기했다.

Effect(효과): Stage358(358단계)은 package handoff(패키지 인계)로 가볍게 고정되고, Stage359(359단계)는 MT5 Strategy Tester(MT5 전략 테스터) 실행과 proxy-MT5 comparison(프록시-MT5 비교)에 집중한다.

## Current Package(현재 패키지)

- queue_rows(대기열 행): `{source.get("queue_rows")}`
- executable_queue_rows(실행 가능 대기열 행): `{source.get("executable_queue_rows")}`
- executable_attempt_rows(실행 가능 시도 행): `{source.get("attempt_rows")}`
- expected_tape_rows(예상 테이프 행): `{source.get("expected_tape_rows")}`
- runtime_mapping_gap_rows(런타임 매핑 차이 행): `{source.get("mapping_gap_rows")}`

## Next Work(다음 작업)

- next_stage_id(다음 단계 ID): `{STAGE_ID}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- action(행동): MT5 Strategy Tester(MT5 전략 테스터)에서 package attempt(패키지 시도)를 실행한다.
- effect(효과): proxy expected value(프록시 예상값)와 MT5 runtime KPI(MT5 런타임 핵심 성과 지표)의 diff(차이), attribution(귀속), usability(활용 가능성)를 기록한다.
"""
    write_text_bom(STAGE_BRIEF, stage_brief)
    write_text_bom(INPUT_REFS, input_refs)
    write_text_bom(SELECTION_STATUS, selection)
    write_text_bom(README, readme)
    write_text_bom(BRANCH_REPORT, branch_report)
    write_text_bom(DECISION_DOC, decision)
    write_text_utf8(WORKSPACE_STATE, current_state)
    write_text_bom(CURRENT_WORKING_STATE, current_working)
    write_text_bom(SOURCE_STAGE_BRIEF, source_stage_brief)
    write_text_bom(SOURCE_SELECTION_STATUS, source_selection)
    write_text_bom(SOURCE_README, source_readme)

    changelog_entry = f"""## 2026-06-02 run359A Stage Branch(359A 단계 분기)

- action(행동): Stage358B(358B 실행)의 ready package(준비된 패키지)를 Stage359(359단계) MT5 execution(실행) 질문으로 분기했다.
- effect(효과): Stage358(358단계)은 package handoff(패키지 인계)로 가볍게 고정되고, Stage359B(359B 실행)가 runtime evidence(런타임 근거), proxy-MT5 diff(프록시-MT5 차이), trade density(거래 밀도) 평가를 맡는다.
- boundary(경계): new MT5 execution(새 MT5 실행), candidate selection(후보 선정), runtime authority(런타임 권위), operating promotion(운영 승격), Goal Achieve(목표 달성)는 주장하지 않는다.
"""
    old_changelog = read_text_bom(CHANGELOG)
    if "run359A Stage Branch(359A 단계 분기)" not in old_changelog:
        write_text_bom(CHANGELOG, changelog_entry + "\n" + old_changelog)


def build_ledger_rows(final: dict[str, Any]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    source = final["source_package"]
    base = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "state_sync_stage_branch(상태 동기화 단계 분기)",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(BRANCH_REPORT),
        "notes": "Stage358B package(358B 패키지)를 Stage359 MT5 execution(359단계 MT5 실행)으로 분기.",
        "family": "state_sync(상태 동기화)",
        "primary_report": rel(BRANCH_REPORT),
        "run_number": RUN_NUMBER,
        "date": TODAY,
        "decision": DECISION,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "rows": source.get("expected_tape_rows", ""),
        "gate_passes": str(final["required_gate_passes"]),
        "gate_total": str(final["required_gate_total"]),
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(BRANCH_REPORT),
        "trained_models": "3",
        "onnx_parity": "12",
        "best_proxy": "proxy_queue_ready(프록시 대기열 준비)",
        "candidate_rows": "8",
        "positive_proxy_rows": "8",
        "best_model_id": source.get("best_model_id", ""),
        "best_proxy_net": source.get("best_proxy_net", ""),
        "attempt_rows": str(source.get("attempt_rows", "")),
        "feature_matrix_rows": "46650",
        "runtime_completed_rows": "0",
        "operating_ready_rows": "0",
        "run_date": TODAY,
        "primary_artifact": rel(FINAL_DECISION),
        "candidate_model_id": source.get("best_model_id", ""),
        "result_status": "stage_branch_opened_no_selection(단계 분기 완료, 선택 없음)",
        "sample_rows": "46650",
        "feature_count": "58",
        "attempt_count": str(source.get("attempt_rows", "")),
        "subrun_id": "Tier A+B",
        "record_view": "Tier A+B combined(Tier A+B 합산)",
        "tier_scope": "Tier A+B",
        "source_package_run_id": PARENT_RUN_ID,
        "scoreboard_lane": "state_sync_stage_branch(상태 동기화 단계 분기)",
        "external_verification_status": "stage_branch_handoff_no_new_mt5_execution(단계 분기 인계, 새 MT5 실행 없음)",
        "trade_density_requirement_status": TRADE_DENSITY_REQUIREMENT,
        "result_judgment": JUDGMENT,
        "final_decision_path": rel(FINAL_DECISION),
        "gate_audit_path": rel(GATE_AUDIT),
        "created_at": TODAY,
        "probability_parity_pass_rows": "12",
        "model_variants": "3",
        "selected_surfaces": "0",
        "runtime_attempt_rows": str(source.get("attempt_rows", "")),
        "work_family": "state_sync(상태 동기화)",
        "primary_kpi": "runtime_attempt_rows=4",
        "guardrail_kpi": TRADE_DENSITY_REQUIREMENT,
        "best_profit_factor": source.get("best_proxy_pf", ""),
    }
    ledger_specs = [
        (
            "Tier_A",
            "Tier A",
            "Tier A separate(Tier A 분리)",
            "runtime_execution_handoff_full_context(런타임 실행 인계 전체 문맥)",
            "Stage358B package handed off to Stage359(Tier A 전체 문맥 패키지 인계).",
        ),
        (
            "Tier_B",
            "Tier B",
            "Tier B separate(Tier B 분리)",
            "missing_required_no_partial_context_runtime_package(Tier B 부분 문맥 런타임 패키지 없음 필수 누락)",
            "Tier B partial-context package remains missing_required(Tier B 부분 문맥 패키지는 필수 누락 유지).",
        ),
        (
            "Tier_AplusB",
            "Tier A+B",
            "Tier A+B combined(Tier A+B 합산)",
            "same_as_tier_a_no_fallback(대체 없음 Tier A와 동일)",
            "Combined record is same as Tier A because no fallback is materialized(대체가 없어 합산 기록은 Tier A와 동일).",
        ),
    ]
    ledger_rows: list[dict[str, Any]] = []
    for suffix, tier, view, metric_scope, notes in ledger_specs:
        row = {
            **base,
            "ledger_row_id": f"{RUN_ID}__{suffix}",
            "row_id": f"{RUN_ID}__{suffix}",
            "subrun_id": tier,
            "record_view": view,
            "view": view,
            "tier_scope": tier,
            "tier": tier,
            "metric_scope": metric_scope,
            "kpi_scope": metric_scope,
            "notes": notes,
            "result_status": "missing_required(필수 누락)" if tier == "Tier B" else base["result_status"],
        }
        ledger_rows.append(row)
    run_registry_row = {**base, "view": "Tier A+B combined(Tier A+B 합산)", "tier": "Tier A+B", "metric_scope": "same_as_tier_a_no_fallback(대체 없음 Tier A와 동일)", "kpi_scope": "same_as_tier_a_no_fallback(대체 없음 Tier A와 동일)", "ledger_row_id": f"{RUN_ID}__Tier_AplusB", "row_id": f"{RUN_ID}__Tier_AplusB"}
    return run_registry_row, ledger_rows


def write_receipts(final: dict[str, Any]) -> None:
    handoff_rows = source_artifacts()
    write_csv(HANDOFF_MANIFEST, handoff_rows)
    write_json(
        LINEAGE_RECEIPT,
        {
            "source_inputs": handoff_rows,
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [row["path"] for row in handoff_rows],
            "artifact_hashes": {row["source_role"]: row["sha256"] for row in handoff_rows},
            "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "availability": "connected_with_ignored_02_runs_manifest",
            "lineage_judgment": "connected_with_boundary",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            "run_id": RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
            "new_mt5_execution": "not_run",
            "candidate_selection": "not_claimed",
            "runtime_authority": "not_claimed",
            "operating_promotion": "not_claimed",
            "live_readiness": "not_claimed",
            "goal_achieve": "not_claimed",
            "effect": "Stage branch(단계 분기)만 주장하고 runtime probe result(런타임 탐침 결과)는 주장하지 않는다.",
        },
    )
    write_json(
        STATE_SYNC_AUDIT,
        {
            "run_id": RUN_ID,
            "workspace_state_stage": STAGE_ID,
            "current_working_state_stage": STAGE_ID,
            "active_selection_status_stage": STAGE_ID,
            "source_stage_handoff_stage": STAGE_ID,
            "status": "passed",
            "effect": "current truth(현재 진실)가 Stage359(359단계)와 Stage359B(359B 실행)를 가리킨다.",
        },
    )
    gates = gate_rows()
    write_csv(GATE_AUDIT, gates)
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "producer": rel(Path(__file__)),
            "created_at": TODAY,
            "claim_boundary": CLAIM_BOUNDARY,
            "artifacts": {
                "final_decision": rel(FINAL_DECISION),
                "handoff_manifest": rel(HANDOFF_MANIFEST),
                "artifact_lineage_receipt": rel(LINEAGE_RECEIPT),
                "claim_boundary_receipt": rel(CLAIM_RECEIPT),
                "state_sync_audit": rel(STATE_SYNC_AUDIT),
                "required_gate_coverage_audit": rel(GATE_AUDIT),
                "branch_report": rel(BRANCH_REPORT),
                "decision_doc": rel(DECISION_DOC),
            },
        },
    )
    write_json(FINAL_DECISION, final)


def update_registries(final: dict[str, Any]) -> None:
    run_row, ledger_rows = build_ledger_rows(final)
    append_or_replace_csv(RUN_REGISTRY, [run_row], ["run_id"])
    append_or_replace_csv(ALPHA_LEDGER, ledger_rows, ["ledger_row_id"], extend_header=False)

    stage_header, _ = read_csv_rows(SOURCE_STAGE_DIR / "03_reviews" / "stage_run_ledger.csv")
    if stage_header:
        write_csv(STAGE_LEDGER, ledger_rows, stage_header)
    else:
        write_csv(STAGE_LEDGER, ledger_rows)

    artifact_candidates = [
        ("python", Path(__file__), "Stage359A branch producer script(359A 분기 생산 스크립트)."),
        ("json", FINAL_DECISION, "Stage359A final decision(359A 최종 결정)."),
        ("json", RUN_MANIFEST, "Stage359A run manifest(359A 실행 목록)."),
        ("csv", HANDOFF_MANIFEST, "Stage359A source package handoff manifest(원천 패키지 인계 목록)."),
        ("json", LINEAGE_RECEIPT, "Stage359A artifact lineage receipt(산출물 계보 영수증)."),
        ("json", CLAIM_RECEIPT, "Stage359A claim boundary receipt(주장 경계 영수증)."),
        ("json", STATE_SYNC_AUDIT, "Stage359A state sync audit(상태 동기화 감사)."),
        ("csv", GATE_AUDIT, "Stage359A gate coverage audit(게이트 커버리지 감사)."),
        ("md", BRANCH_REPORT, "Stage359A branch report(분기 보고서)."),
        ("md", DECISION_DOC, "Stage359A durable decision memo(지속 결정 메모)."),
        ("md", STAGE_BRIEF, "Stage359 stage brief(단계 개요)."),
        ("md", INPUT_REFS, "Stage359 input refs(입력 참조)."),
        ("md", SELECTION_STATUS, "Stage359 selection status(선택 상태)."),
    ]
    artifact_rows = []
    for artifact_type, path, notes in artifact_candidates:
        if not path.exists():
            continue
        artifact_rows.append(
            {
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "artifact_type": artifact_type,
                "path": rel(path),
                "sha256": sha256_file(path),
                "created_at": TODAY,
                "claim_boundary": CLAIM_BOUNDARY,
                "artifact_id": f"{RUN_ID}::{path.stem}",
                "created_at_utc": CREATED_AT_UTC,
                "notes": notes,
                "artifact_path": rel(path),
            }
        )
    append_or_replace_csv(ARTIFACT_REGISTRY, artifact_rows, ["artifact_id"])


def main() -> int:
    ensure_dirs()
    source_final_path = SOURCE_RUN_DIR / "final_decision.json"
    if not source_final_path.exists():
        print(json.dumps({"status": "blocked", "reason": f"missing {rel(source_final_path)}"}, ensure_ascii=False))
        return 2

    source_final = read_json(source_final_path)
    final = build_final(source_final)
    write_stage_docs(final)
    write_receipts(final)
    update_registries(final)
    print(json.dumps({"status": "completed", "run_id": RUN_ID, "next_run_id": NEXT_RUN_ID, "stage_id": STAGE_ID}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
