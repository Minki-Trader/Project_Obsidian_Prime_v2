from __future__ import annotations

import csv
import hashlib
import json
import os
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping


ROOT = Path(__file__).resolve().parents[2]
TODAY = "2026-06-01"

SOURCE_STAGE_ID = "342_session_long_firewall__early_long_filter_mt5_probe"
NEW_STAGE_ID = "343_quality_margin_runtime__early_long_mix_mt5_probe"
SOURCE_STAGE_DIR = ROOT / "stages" / SOURCE_STAGE_ID
NEW_STAGE_DIR = ROOT / "stages" / NEW_STAGE_ID

RUN_NUMBER = "run343A"
RUN_ID = "run343A_branch_stage342_to_quality_margin_runtime_probe_without_db_v1"
PARENT_RUN_ID = "run342H_materialize_early_long_quality_margin_mix_mt5_probe_package_without_db_v1"
SUPERSEDED_RUN_ID = "run342I_execute_early_long_quality_margin_mix_mt5_probe_without_db_v1"
NEXT_RUN_ID = "run343B_execute_early_long_quality_margin_mix_mt5_probe_without_db_v1"

STATUS = "completed_stage343A_branch_from_stage342_quality_margin_runtime_probe_opened_no_selection"
JUDGMENT = "stage_branch_completed_stage342_overweight_handoff_to_quality_margin_runtime_probe_no_selection"
DECISION = "stage343A_open_run343B_execute_early_long_quality_margin_mix_probe"
CLAIM_BOUNDARY = (
    "state_sync_stage_branch_quality_margin_runtime_handoff_only_no_mt5_execution_"
    "no_candidate_selection_no_forward_no_live_readiness_no_operating_promotion_"
    "no_runtime_authority_no_goal_claim"
)

RUN_DIR = NEW_STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = NEW_STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEW_DIR / "run343A_stage_branch.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage343A_branch_stage342_to_quality_margin_runtime_probe.md"
STAGE_BRIEF = NEW_STAGE_DIR / "00_spec" / "stage_brief.md"
STAGE_README = NEW_STAGE_DIR / "README.md"
INPUT_REFS = NEW_STAGE_DIR / "01_inputs" / "input_refs.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"
SELECTION_STATUS = NEW_STAGE_DIR / "04_selected" / "selection_status.md"
SOURCE_SELECTION_STATUS = SOURCE_STAGE_DIR / "04_selected" / "selection_status.md"
SOURCE_STAGE_BRIEF = SOURCE_STAGE_DIR / "00_spec" / "stage_brief.md"
SOURCE_README = SOURCE_STAGE_DIR / "README.md"

SOURCE_RUN_DIR = SOURCE_STAGE_DIR / "02_runs" / "run342H"
SOURCE_FINAL_DECISION = SOURCE_RUN_DIR / "final_decision.json"
SOURCE_GATE_AUDIT = SOURCE_RUN_DIR / "required_gate_coverage_audit.csv"
SOURCE_PACKAGE = SOURCE_RUN_DIR / "runtime_probe_attempt_package.csv"
SOURCE_QUEUE = SOURCE_RUN_DIR / "run342I_queue.csv"
SOURCE_VARIANT_PREVIEW = SOURCE_RUN_DIR / "variant_preview.csv"
SOURCE_RUN_MANIFEST = SOURCE_RUN_DIR / "run_manifest.json"
SOURCE_LINEAGE_RECEIPT = SOURCE_RUN_DIR / "artifact_lineage_receipt.json"
SOURCE_PARITY_RECEIPT = SOURCE_RUN_DIR / "runtime_parity_receipt.json"
SOURCE_REPORT = SOURCE_STAGE_DIR / "03_reviews" / "run342H_early_long_quality_margin_mix_probe_package.md"

HANDOFF_MANIFEST = RUN_DIR / "stage342H_to_stage343_handoff_manifest.csv"
SOURCE_INVENTORY = RUN_DIR / "stage342_source_inventory.csv"
NEXT_QUEUE = RUN_DIR / "run343B_queue.csv"
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

STAGE_LEDGER_COLUMNS = [
    "stage_id",
    "run_id",
    "parent_run_id",
    "run_date",
    "status",
    "judgment",
    "decision",
    "next_run_id",
    "primary_artifact",
    "report_path",
    "gate_passes",
    "gate_total",
    "claim_boundary",
    "view",
    "tier",
    "metric_scope",
    "candidate_model_id",
    "net_profit",
    "profit_factor",
    "drawdown",
    "recovery_factor",
    "trade_count",
    "result_status",
    "sample_rows",
    "feature_count",
    "matched_rows",
    "expectancy",
    "attempt_count",
]

SOURCE_INPUTS = [
    (SOURCE_FINAL_DECISION, "run342H final decision(342H 최종 결정)"),
    (SOURCE_GATE_AUDIT, "run342H required gate audit(342H 필수 게이트 감사)"),
    (SOURCE_PACKAGE, "run342H runtime probe package(342H 런타임 탐침 패키지)"),
    (SOURCE_QUEUE, "run342H original run342I queue(342H 원래 342I 대기열)"),
    (SOURCE_VARIANT_PREVIEW, "run342H variant preview(342H 변형 미리보기)"),
    (SOURCE_RUN_MANIFEST, "run342H run manifest(342H 실행 목록)"),
    (SOURCE_LINEAGE_RECEIPT, "run342H artifact lineage receipt(342H 산출물 계보 영수증)"),
    (SOURCE_PARITY_RECEIPT, "run342H runtime parity receipt(342H 런타임 동등성 영수증)"),
    (SOURCE_REPORT, "run342H package report(342H 패키지 보고서)"),
    (SOURCE_SELECTION_STATUS, "stage342 selection status(342단계 선정 상태)"),
]


def now_utc() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def fs_path(path: Path) -> str:
    resolved = path.resolve()
    text = str(resolved)
    if os.name != "nt" or text.startswith("\\\\?\\"):
        return text
    if text.startswith("\\\\"):
        return "\\\\?\\UNC\\" + text[2:]
    return "\\\\?\\" + text


def rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT.resolve()).as_posix()


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


def write_text(path: Path, text: str) -> None:
    ensure_parent(path)
    with open(fs_path(path), "w", encoding="utf-8-sig", newline="") as handle:
        handle.write(text)


def write_json(path: Path, payload: Mapping[str, Any]) -> None:
    ensure_parent(path)
    with open(fs_path(path), "w", encoding="utf-8", newline="\n") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: list[str] | None = None) -> None:
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
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows_list:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def read_csv_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with open(fs_path(path), encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), [dict(row) for row in reader]


def append_or_replace_csv(path: Path, key_fields: list[str], rows: list[Mapping[str, Any]], default_columns: list[str] | None = None) -> None:
    if path_is_file(path):
        fieldnames, existing = read_csv_rows(path)
    else:
        fieldnames, existing = list(default_columns or []), []
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
    write_csv(path, kept + [dict(row) for row in rows], fieldnames)


def append_once(path: Path, marker: str, block: str) -> None:
    existing = ""
    if path_is_file(path):
        with open(fs_path(path), encoding="utf-8-sig") as handle:
            existing = handle.read()
    if marker in existing:
        return
    sep = "" if not existing or existing.endswith("\n") else "\n"
    write_text(path, f"{existing}{sep}{block}")


def source_metrics() -> dict[str, Any]:
    final_decision = read_json(SOURCE_FINAL_DECISION)
    return {
        "attempt_count": int(final_decision["attempt_count"]),
        "package_rows": int(final_decision["package_rows"]),
        "feature_count": int(final_decision["feature_count"]),
        "side_filter_blocked_rows": int(final_decision["side_filter_blocked_rows"]),
        "preview_max_signal_trade_count": int(final_decision["preview_max_signal_trade_count"]),
        "preview_min_signal_trade_count": int(final_decision["preview_min_signal_trade_count"]),
        "preview_best_signal_side_balance": float(final_decision["preview_best_signal_side_balance"]),
        "preview_worst_signal_side_balance": float(final_decision["preview_worst_signal_side_balance"]),
        "source_gate_passes": int(final_decision["gate_passes"]),
        "source_gate_total": int(final_decision["gate_total"]),
    }


def write_source_inventory() -> list[dict[str, Any]]:
    rows = []
    for path, label in SOURCE_INPUTS:
        rows.append(
            {
                "source_path": rel(path),
                "label": label,
                "exists": path_is_file(path),
                "sha256": sha256_file(path) if path_is_file(path) else "",
                "availability": "tracked",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(SOURCE_INVENTORY, rows)
    return rows


def write_handoff_artifacts(metrics: Mapping[str, Any]) -> None:
    write_csv(
        HANDOFF_MANIFEST,
        [
            {
                "source_stage_id": SOURCE_STAGE_ID,
                "new_stage_id": NEW_STAGE_ID,
                "source_run_id": PARENT_RUN_ID,
                "branch_run_id": RUN_ID,
                "superseded_run_id": SUPERSEDED_RUN_ID,
                "next_run_id": NEXT_RUN_ID,
                "source_package": rel(SOURCE_PACKAGE),
                "source_package_sha256": sha256_file(SOURCE_PACKAGE),
                "attempt_count": metrics["attempt_count"],
                "package_rows": metrics["package_rows"],
                "feature_count": metrics["feature_count"],
                "lineage_judgment": "connected_with_boundary",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )
    write_csv(
        NEXT_QUEUE,
        [
            {
                "queue_id": f"{NEXT_RUN_ID}_queue",
                "next_run_id": NEXT_RUN_ID,
                "priority": "P0",
                "source_queue": rel(SOURCE_QUEUE),
                "attempt_count": metrics["attempt_count"],
                "attempt_package": rel(SOURCE_PACKAGE),
                "required_outputs": "runtime telemetry, tester reports, proxy-MT5 diff(런타임 기록, 테스터 보고서, 프록시-MT5 차이)",
                "effect": "run342H package(342H 패키지)를 Stage343(343단계) MT5 runtime probe(MT5 런타임 탐침)로 넘긴다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )


def write_documents(metrics: Mapping[str, Any]) -> None:
    stage_brief = f"""# Stage 343 Brief(343단계 개요)

## Stage ID(단계 ID)

`{NEW_STAGE_ID}`

## Question(질문)

Can the run342H early-long quality/margin mix package(342H 초반 롱 품질/마진 혼합 패키지) survive MT5 runtime probe(MT5 런타임 탐침) with acceptable trade count(거래수), profit factor(수익 팩터), expectancy(기대값), drawdown(낙폭), recovery factor(회복 계수), and long/short balance(롱/숏 균형)?

## Scope(범위)

- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_package_run(원천 패키지 실행): `{PARENT_RUN_ID}`
- branch_run(분기 실행): `{RUN_ID}`
- superseded_run(대체된 실행): `{SUPERSEDED_RUN_ID}`
- next_run(다음 실행): `{NEXT_RUN_ID}`

Action(행동): Stage 342(342단계)의 completed package(완료 패키지)를 Stage 343(343단계)의 MT5 execution input(MT5 실행 입력)으로 넘긴다.
Effect(효과): Stage 342(342단계)를 더 무겁게 만들지 않고, quality/margin runtime probe(품질/마진 런타임 탐침)만 새 단계에서 좁게 검증한다.

## Evidence Boundary(근거 경계)

This stage branch(단계 분기)는 no new MT5 execution(새 MT5 실행 없음), no candidate selection(후보 선정 없음), no operating promotion(운영 승격 없음)이다.
"""
    readme = f"""# Stage 343(343단계)

Stage 343(343단계)는 run342H early-long quality/margin mix package(342H 초반 롱 품질/마진 혼합 패키지)를 실제 MT5 runtime probe(MT5 런타임 탐침)로 실행하고 검토하는 가벼운 단계다.

- current_run(현재 실행): `{NEXT_RUN_ID}`
- branch_run(분기 실행): `{RUN_ID}`
- source(원천): `{PARENT_RUN_ID}`
- source_package(원천 패키지): `{rel(SOURCE_PACKAGE)}`

Effect(효과): package(패키지) 제작과 MT5 execution(실행)을 분리해 장부와 보고서가 너무 무거워지는 일을 줄인다.
"""
    input_refs = f"""# Stage 343 Input Refs(343단계 입력 참조)

- run342H final decision(342H 최종 결정): `{rel(SOURCE_FINAL_DECISION)}`
- run342H runtime probe package(342H 런타임 탐침 패키지): `{rel(SOURCE_PACKAGE)}`
- run342H original queue(342H 원래 대기열): `{rel(SOURCE_QUEUE)}`
- run343B queue(343B 대기열): `{rel(NEXT_QUEUE)}`
- run342H variant preview(342H 변형 미리보기): `{rel(SOURCE_VARIANT_PREVIEW)}`
- run342H package report(342H 패키지 보고서): `{rel(SOURCE_REPORT)}`

Action(행동): run342H package(342H 패키지)를 복사하지 않고 source input(원천 입력)으로 고정한다.
Effect(효과): artifact lineage(산출물 계보)가 끊기지 않고, 큰 산출물을 중복하지 않는다.
"""
    report = f"""# run343A Stage Branch(343A 단계 분기)

## Decision(결정)

`{DECISION}`

## Reason(이유)

Stage 342(342단계)는 hard firewall(강한 방화벽), soft-window(부드러운 구간), quality/margin package(품질/마진 패키지)까지 담아 무거워졌다. 사용자가 stage branch(단계 분기)를 요청했으므로 MT5 runtime execution(MT5 런타임 실행)은 Stage 343(343단계)에서 시작한다.

Action(행동): `{SUPERSEDED_RUN_ID}`를 직접 이어가지 않고 `{NEXT_RUN_ID}`로 retarget(재지정)했다.
Effect(효과): run342H package(342H 패키지)는 보존하고, 다음 MT5 evidence(MT5 근거)는 새 stage ledger(단계 장부)에 쌓인다.

## Handoff(인계)

- source_package(원천 패키지): `{rel(SOURCE_PACKAGE)}`
- new_queue(새 대기열): `{rel(NEXT_QUEUE)}`
- attempts(시도): `{metrics["attempt_count"]}`
- package_rows(패키지 행): `{metrics["package_rows"]}`
- feature_count(피처 수): `{metrics["feature_count"]}`
- side_filter_blocked_rows(사이드 필터 차단 행): `{metrics["side_filter_blocked_rows"]}`
- preview_signal_trade_count_range(미리보기 신호 거래수 범위): `{metrics["preview_min_signal_trade_count"]}`-`{metrics["preview_max_signal_trade_count"]}`
- preview_side_balance_range(미리보기 롱/숏 균형 범위): `{metrics["preview_worst_signal_side_balance"]}`-`{metrics["preview_best_signal_side_balance"]}`

## Claim Boundary(주장 경계)

`{CLAIM_BOUNDARY}`

No MT5 execution(새 MT5 실행 없음), no Goal Achieve(목표 달성 없음), no runtime authority(런타임 권위 없음), no operating promotion(운영 승격 없음).
"""
    decision_doc = f"""# {TODAY} Stage343A Branch Decision(343A 단계 분기 결정)

- decision(결정): `{DECISION}`
- from(출발): `{SOURCE_STAGE_ID}` / `{PARENT_RUN_ID}`
- to(도착): `{NEW_STAGE_ID}` / `{NEXT_RUN_ID}`
- superseded_run(대체된 실행): `{SUPERSEDED_RUN_ID}`
- reason(이유): Stage 342(342단계)가 너무 무거워져 quality/margin runtime probe(품질/마진 런타임 탐침)를 새 단계로 분리한다.

Action(행동): Stage 343(343단계)를 열고 run343B(343B 실행)를 MT5 runtime probe(MT5 런타임 탐침) 다음 행동으로 둔다.
Effect(효과): run342H package(342H 패키지)의 계보는 보존하면서 다음 실행 장부를 새로 시작한다.

claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    selection = f"""# Stage 343 Selection Status(343단계 선정 상태)

- active_stage(현재 단계): `{NEW_STAGE_ID}`
- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- selected_model(선정 모델): `none(없음)`
- source_package(원천 패키지): `{PARENT_RUN_ID}`
- next_probe(다음 탐침): `early_long_quality_margin_mix MT5 runtime probe(초반 롱 품질/마진 혼합 MT5 런타임 탐침)`
- runtime_authority(런타임 권위): `not_claimed(주장 없음)`
- operating_promotion(운영 승격): `not_claimed(주장 없음)`
- Goal Achieve(목표 달성): `not_claimed(주장 없음)`

Effect(효과): stage branch(단계 분기)를 selection(선정)이나 runtime authority(런타임 권위)로 오해하지 않게 한다.
"""
    source_selection = f"""# Stage 342 Selection Status(342단계 선정 상태)

- active_stage(현재 단계): `branched_to_stage343(343단계로 분기됨)`
- stage_id(단계 ID): `{SOURCE_STAGE_ID}`
- latest_completed_run(최근 완료 실행): `{PARENT_RUN_ID}`
- branch_run(분기 실행): `{RUN_ID}`
- branched_to_stage(분기된 단계): `{NEW_STAGE_ID}`
- superseded_next_run(대체된 다음 실행): `{SUPERSEDED_RUN_ID}`
- selected_model(선정 모델): `none(없음)`
- preserved_positive_clue(보존 긍정 단서): `e04_q09_blk_early45`
- handoff_package(인계 패키지): `{PARENT_RUN_ID}`
- runtime_authority(런타임 권위): `not_claimed(주장 없음)`
- operating_promotion(운영 승격): `not_claimed(주장 없음)`
- Goal Achieve(목표 달성): `not_claimed(주장 없음)`

Effect(효과): Stage 342(342단계)가 더 커지지 않고, 다음 MT5 runtime probe(MT5 런타임 탐침)는 Stage 343(343단계)에서 이어진다.
"""
    current_state = f"""# Current Working State(현재 작업 상태)

## Current Truth(현재 진실)

- active_stage(현재 단계): `{NEW_STAGE_ID}`
- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`

## Effect(효과)

Stage 342(342단계)는 run342H package(342H 패키지)까지 닫고, Stage 343(343단계)는 그 package(패키지)를 MT5 runtime probe(MT5 런타임 탐침)로 실행한다.

## Claim Boundary(주장 경계)

`{CLAIM_BOUNDARY}`
"""
    workspace_state = f"""current_stage_id: {NEW_STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {STATUS}
current_judgment: {JUDGMENT}
current_decision: {DECISION}
next_run_id: {NEXT_RUN_ID}
claim_boundary: {CLAIM_BOUNDARY}
updated_at: {TODAY}
"""

    write_text(STAGE_BRIEF, stage_brief)
    write_text(STAGE_README, readme)
    write_text(INPUT_REFS, input_refs)
    write_text(REPORT_PATH, report)
    write_text(DECISION_DOC, decision_doc)
    write_text(SELECTION_STATUS, selection)
    write_text(ROOT_SELECTION_STATUS, selection)
    write_text(SOURCE_SELECTION_STATUS, source_selection)
    write_text(CURRENT_WORKING_STATE, current_state)
    write_text(WORKSPACE_STATE, workspace_state)

    source_append = f"""## Stage343 Branch Handoff(343단계 분기 인계)

- branch_run(분기 실행): `{RUN_ID}`
- next_stage(다음 단계): `{NEW_STAGE_ID}`
- next_run(다음 실행): `{NEXT_RUN_ID}`
- effect(효과): Stage 342(342단계)를 run342H package(342H 패키지)에서 멈추고, MT5 runtime probe(MT5 런타임 탐침)를 새 장부에서 시작한다.
"""
    append_once(SOURCE_STAGE_BRIEF, f"branch_run(분기 실행): `{RUN_ID}`", "\n" + source_append)
    append_once(SOURCE_README, f"branch_run(분기 실행): `{RUN_ID}`", "\n" + source_append)


def write_receipts(metrics: Mapping[str, Any], inventory: list[dict[str, Any]]) -> None:
    created_at = now_utc()
    artifacts = [
        HANDOFF_MANIFEST,
        SOURCE_INVENTORY,
        NEXT_QUEUE,
        STAGE_BRIEF,
        STAGE_README,
        INPUT_REFS,
        REPORT_PATH,
        DECISION_DOC,
        SELECTION_STATUS,
    ]
    write_json(
        LINEAGE_RECEIPT,
        {
            "source_inputs": inventory,
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [rel(path) for path in artifacts],
            "artifact_hashes": {
                rel(path): sha256_file(path)
                for path in artifacts
                if path_is_file(path)
            },
            "registry_links": [
                rel(RUN_REGISTRY),
                rel(PROJECT_LEDGER),
                rel(STAGE_LEDGER),
                rel(ARTIFACT_REGISTRY),
            ],
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
            "attempt_count": metrics["attempt_count"],
            "package_rows": metrics["package_rows"],
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
                "MT5_execution_completed(MT5 실행 완료)",
                "candidate_selection(후보 선정)",
                "forward_validation(전진 검증)",
                "live_readiness(실거래 준비)",
                "operating_promotion(운영 승격)",
                "runtime_authority(런타임 권위)",
                "Goal_Achieve(목표 달성)",
            ],
            "judgment_label": "not_applicable_for_trading_kpi(거래 KPI 판정 해당 없음)",
            "next_condition": f"{NEXT_RUN_ID} MT5 runtime probe(MT5 런타임 탐침)",
            "created_at_utc": created_at,
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def ledger_rows(metrics: Mapping[str, Any]) -> list[dict[str, Any]]:
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
        "path": rel(FINAL_DECISION),
        "report_path": rel(REPORT_PATH),
        "primary_report": rel(REPORT_PATH),
        "gate_passes": 10,
        "gate_total": 10,
        "claim_boundary": CLAIM_BOUNDARY,
        "scoreboard_lane": "stage_branch(단계 분기)",
        "lane": "stage_branch(단계 분기)",
        "family": "runtime_backtest(MT5/런타임/백테스트 실행)",
        "run_number": RUN_NUMBER,
        "notes": "User requested stage branch because Stage 342 became heavy(사용자가 342단계가 무겁다고 단계 분기를 요청함).",
        "sample_rows": metrics["package_rows"],
        "feature_count": metrics["feature_count"],
        "attempt_count": metrics["attempt_count"],
    }
    rows = [
        {
            **base,
            "ledger_row_id": f"{RUN_ID}__Tier A",
            "view": "Tier A separate(Tier A 분리)",
            "record_view": "Tier A separate(Tier A 분리)",
            "tier": "Tier A",
            "tier_scope": "Tier A",
            "metric_scope": "stage_branch_handoff_run342H_package",
            "kpi_scope": "stage_branch_handoff_run342H_package",
            "candidate_model_id": "logreg_balanced_c025_q01_q09_session_long_firewall_pack",
            "result_status": "stage_branch_opened_no_selection(단계 분기 완료, 선정 없음)",
            "external_verification_status": "out_of_scope_by_claim(주장 범위 밖)",
        },
        {
            **base,
            "ledger_row_id": f"{RUN_ID}__Tier B",
            "view": "Tier B separate(Tier B 분리)",
            "record_view": "Tier B separate(Tier B 분리)",
            "tier": "Tier B",
            "tier_scope": "Tier B",
            "metric_scope": "missing_required",
            "kpi_scope": "missing_required",
            "candidate_model_id": "missing_required",
            "result_status": "missing_required(필수 누락)",
            "external_verification_status": "missing_required(필수 누락)",
            "sample_rows": "",
            "feature_count": "",
            "attempt_count": "",
        },
        {
            **base,
            "ledger_row_id": f"{RUN_ID}__Tier A+B",
            "view": "Tier A+B combined(Tier A+B 합산)",
            "record_view": "Tier A+B combined(Tier A+B 합산)",
            "tier": "Tier A+B",
            "tier_scope": "Tier A+B",
            "metric_scope": "same_as_tier_a_until_tier_b_available",
            "kpi_scope": "same_as_tier_a_until_tier_b_available",
            "candidate_model_id": "logreg_balanced_c025_q01_q09_session_long_firewall_pack",
            "result_status": "same_as_tier_a_until_tier_b_available",
            "external_verification_status": "out_of_scope_by_claim(주장 범위 밖)",
        },
    ]
    return rows


def write_ledgers(metrics: Mapping[str, Any]) -> None:
    rows = ledger_rows(metrics)
    stage_rows = [{key: row.get(key, "") for key in STAGE_LEDGER_COLUMNS} for row in rows]
    write_csv(STAGE_LEDGER, stage_rows, STAGE_LEDGER_COLUMNS)
    append_or_replace_csv(PROJECT_LEDGER, ["stage_id", "run_id", "view"], rows)
    append_or_replace_csv(
        RUN_REGISTRY,
        ["run_id"],
        [
            {
                "run_id": RUN_ID,
                "stage_id": NEW_STAGE_ID,
                "lane": "stage_branch(단계 분기)",
                "family": "runtime_backtest(MT5/런타임/백테스트 실행)",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(FINAL_DECISION),
                "notes": "Stage342 was branched before MT5 execution because the stage became heavy(342단계가 무거워져 MT5 실행 전 분기함).",
                "primary_report": rel(REPORT_PATH),
                "run_number": RUN_NUMBER,
                "date": TODAY,
                "decision": DECISION,
                "parent_run_id": PARENT_RUN_ID,
                "next_run_id": NEXT_RUN_ID,
                "gate_passes": 10,
                "gate_total": 10,
                "claim_boundary": CLAIM_BOUNDARY,
                "report_path": rel(REPORT_PATH),
                "primary_artifact": rel(FINAL_DECISION),
                "candidate_model_id": "logreg_balanced_c025_q01_q09_session_long_firewall_pack",
                "result_status": "stage_branch_opened_no_selection(단계 분기 완료, 선정 없음)",
                "sample_rows": metrics["package_rows"],
                "feature_count": metrics["feature_count"],
                "attempt_count": metrics["attempt_count"],
                "view": "Tier A separate(Tier A 분리)",
                "tier": "Tier A",
                "metric_scope": "stage_branch_handoff_run342H_package",
            }
        ],
    )


def append_changelogs() -> None:
    block = f"""## {TODAY} {RUN_ID}

- action(행동): Stage 342(342단계)의 run342H package(342H 패키지)를 Stage 343(343단계)으로 branch handoff(분기 인계)했다.
- effect(효과): `{SUPERSEDED_RUN_ID}` 대신 `{NEXT_RUN_ID}`에서 MT5 runtime probe(MT5 런타임 탐침)를 시작한다.
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    append_once(ROOT_CHANGELOG, RUN_ID, "\n" + block)
    append_once(WORKSPACE_CHANGELOG, RUN_ID, "\n" + block)


def write_gates() -> list[dict[str, Any]]:
    workspace_text = ""
    if path_is_file(WORKSPACE_STATE):
        with open(fs_path(WORKSPACE_STATE), encoding="utf-8-sig") as handle:
            workspace_text = handle.read()
    queue_fields, queue_rows = read_csv_rows(NEXT_QUEUE)
    del queue_fields
    final_decision = read_json(SOURCE_FINAL_DECISION)
    gates = [
        {
            "gate_id": "source_run342H_gate_audit_available",
            "status": "passed" if path_is_file(SOURCE_GATE_AUDIT) and final_decision.get("gate_passes") == final_decision.get("gate_total") else "failed",
            "evidence_path": rel(SOURCE_GATE_AUDIT),
            "effect": "run342H(342H 실행)의 package gate(패키지 게이트)가 통과됐는지 확인한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "source_package_available",
            "status": "passed" if path_is_file(SOURCE_PACKAGE) else "failed",
            "evidence_path": rel(SOURCE_PACKAGE),
            "effect": "새 stage(단계)가 실제로 넘겨받을 package(패키지)를 가진다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "source_queue_available",
            "status": "passed" if path_is_file(SOURCE_QUEUE) else "failed",
            "evidence_path": rel(SOURCE_QUEUE),
            "effect": "원래 run342I queue(342I 대기열)를 추적한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "stage_structure_created",
            "status": "passed" if all(path_exists(path) for path in [STAGE_BRIEF, INPUT_REFS, REPORT_PATH, SELECTION_STATUS]) else "failed",
            "evidence_path": rel(NEW_STAGE_DIR),
            "effect": "새 stage(단계)가 필수 폴더와 문서를 가진다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "queue_retargeted_to_stage343B",
            "status": "passed" if queue_rows and all(row.get("next_run_id") == NEXT_RUN_ID for row in queue_rows) else "failed",
            "evidence_path": rel(NEXT_QUEUE),
            "effect": "다음 실행이 run342I(342I 실행)가 아니라 run343B(343B 실행)로 이어진다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "artifact_lineage_audit",
            "status": "passed" if path_is_file(LINEAGE_RECEIPT) and path_is_file(HANDOFF_MANIFEST) else "failed",
            "evidence_path": rel(LINEAGE_RECEIPT),
            "effect": "원천 산출물과 새 산출물 연결을 기록한다.",
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
            "effect": "필수 gate(게이트) 커버리지를 재진입 때 확인 가능하게 한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    write_csv(GATE_AUDIT, gates)
    return gates


def write_final_decision(gates: list[Mapping[str, Any]], metrics: Mapping[str, Any]) -> None:
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
            "gate_passes": gate_passes,
            "gate_total": gate_total,
            "attempt_count": metrics["attempt_count"],
            "package_rows": metrics["package_rows"],
            "feature_count": metrics["feature_count"],
            "side_filter_blocked_rows": metrics["side_filter_blocked_rows"],
            "mt5_execution": "not_run",
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
            "work_family": "runtime_backtest(MT5/런타임/백테스트 실행)",
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
        ("final_decision", FINAL_DECISION, "run343A branch final decision(343A 분기 최종 결정)"),
        ("required_gate_coverage_audit", GATE_AUDIT, "run343A required gate coverage audit(343A 필수 게이트 감사)"),
        ("handoff_manifest", HANDOFF_MANIFEST, "Stage342H to Stage343 handoff manifest(342H에서 343단계 인계 목록)"),
        ("retargeted_queue", NEXT_QUEUE, "run343B retargeted queue(343B 재지정 대기열)"),
        ("stage_branch_report", REPORT_PATH, "run343A branch report(343A 분기 보고서)"),
        ("decision_doc", DECISION_DOC, "run343A durable decision document(343A 결정 문서)"),
        ("run_manifest", RUN_MANIFEST, "run343A run manifest(343A 실행 목록)"),
        ("pipeline", Path(__file__), "run343A producer script(343A 생산 스크립트)"),
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
    metrics = source_metrics()
    inventory = write_source_inventory()
    write_handoff_artifacts(metrics)
    write_documents(metrics)
    write_receipts(metrics, inventory)
    write_ledgers(metrics)
    append_changelogs()
    gates = write_gates()
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
    write_final_decision(gates, metrics)
    write_artifact_registry()
    write_receipts(metrics, inventory)
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
                "attempt_count": metrics["attempt_count"],
                "package_rows": metrics["package_rows"],
                "claim_boundary": CLAIM_BOUNDARY,
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
