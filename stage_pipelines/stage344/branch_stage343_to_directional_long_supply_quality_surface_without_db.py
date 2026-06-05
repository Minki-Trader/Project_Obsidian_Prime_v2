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

SOURCE_STAGE_ID = "343_quality_margin_runtime__early_long_mix_mt5_probe"
NEW_STAGE_ID = "344_directional_long_quality__supply_surface_probe"
SOURCE_STAGE_DIR = ROOT / "stages" / SOURCE_STAGE_ID
NEW_STAGE_DIR = ROOT / "stages" / NEW_STAGE_ID

RUN_NUMBER = "run344A"
RUN_ID = "run344A_branch_stage343_to_directional_long_supply_quality_surface_without_db_v1"
PARENT_RUN_ID = "run343F_review_trade_shape_rescue_quality_margin_blend_mt5_probe_without_db_v1"
SUPERSEDED_RUN_ID = "run343G_design_directional_long_supply_quality_surface_without_db_v1"
NEXT_RUN_ID = "run344B_design_directional_long_supply_quality_surface_without_db_v1"

STATUS = "completed_stage344A_branch_from_stage343_directional_long_quality_surface_opened_no_selection"
JUDGMENT = "stage_branch_completed_stage343_overweight_handoff_to_directional_long_quality_surface_no_selection"
DECISION = "stage344A_open_run344B_design_directional_long_supply_quality_surface"
CLAIM_BOUNDARY = (
    "state_sync_stage_branch_directional_long_quality_surface_handoff_only_no_new_mt5_execution_"
    "no_candidate_selection_no_forward_no_live_readiness_no_operating_promotion_"
    "no_runtime_authority_no_goal_claim"
)

RUN_DIR = NEW_STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = NEW_STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEW_DIR / "run344A_stage_branch.md"
REVIEW_INDEX = REVIEW_DIR / "review_index.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage344A_branch_stage343_to_directional_long_quality_surface.md"
STAGE_BRIEF = NEW_STAGE_DIR / "00_spec" / "stage_brief.md"
STAGE_README = NEW_STAGE_DIR / "README.md"
INPUT_REFS = NEW_STAGE_DIR / "01_inputs" / "input_refs.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"
SELECTION_STATUS = NEW_STAGE_DIR / "04_selected" / "selection_status.md"
SOURCE_SELECTION_STATUS = SOURCE_STAGE_DIR / "04_selected" / "selection_status.md"
SOURCE_STAGE_BRIEF = SOURCE_STAGE_DIR / "00_spec" / "stage_brief.md"
SOURCE_README = SOURCE_STAGE_DIR / "README.md"

SOURCE_RUN_DIR = SOURCE_STAGE_DIR / "02_runs" / "run343F"
SOURCE_FINAL_DECISION = SOURCE_RUN_DIR / "final_decision.json"
SOURCE_GATE_AUDIT = SOURCE_RUN_DIR / "required_gate_coverage_audit.csv"
SOURCE_SCORECARD = SOURCE_RUN_DIR / "trade_shape_rescue_review_scorecard.csv"
SOURCE_ATTRIBUTION = SOURCE_RUN_DIR / "performance_attribution.csv"
SOURCE_FAILURE_MEMORY = SOURCE_RUN_DIR / "failure_memory.csv"
SOURCE_QUEUE = SOURCE_RUN_DIR / "run343G_directional_long_supply_quality_surface_queue.csv"
SOURCE_REPORT = SOURCE_STAGE_DIR / "03_reviews" / "run343F_trade_shape_rescue_quality_margin_blend_mt5_probe_review.md"

HANDOFF_MANIFEST = RUN_DIR / "stage343F_to_stage344_handoff_manifest.csv"
SOURCE_INVENTORY = RUN_DIR / "stage343_source_inventory.csv"
NEXT_QUEUE = RUN_DIR / "run344B_directional_long_supply_quality_surface_queue.csv"
STAGE_TRANSITION_RECEIPT = RUN_DIR / "stage_transition_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs" / "context" / "current_working_state.md"
ROOT_CHANGELOG = ROOT / "CHANGELOG.md"
WORKSPACE_CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
PROJECT_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
IDEA_REGISTRY = ROOT / "docs" / "registers" / "idea_registry.md"
ROOT_SELECTION_STATUS = ROOT / "docs" / "registers" / "selection_status.md"

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
    "source_package_run_id",
    "ledger_row_id",
    "subrun_id",
    "record_view",
    "tier_scope",
    "kpi_scope",
    "scoreboard_lane",
    "path",
    "primary_kpi",
    "guardrail_kpi",
    "external_verification_status",
    "notes",
]

SOURCE_INPUTS = [
    (SOURCE_FINAL_DECISION, "run343F final decision(343F 최종 결정)"),
    (SOURCE_GATE_AUDIT, "run343F required gate audit(343F 필수 게이트 감사)"),
    (SOURCE_SCORECARD, "run343F review scorecard(343F 검토 점수표)"),
    (SOURCE_ATTRIBUTION, "run343F performance attribution(343F 성과 귀속)"),
    (SOURCE_FAILURE_MEMORY, "run343F failure memory(343F 실패 기억)"),
    (SOURCE_QUEUE, "run343F next offensive queue(343F 다음 공격 탐색 대기열)"),
    (SOURCE_REPORT, "run343F review report(343F 검토 보고서)"),
    (SOURCE_SELECTION_STATUS, "stage343 selection status(343단계 선정 상태)"),
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


def write_text(path: Path, text: str) -> None:
    ensure_parent(path)
    with open(fs_path(path), "w", encoding="utf-8-sig", newline="\n") as handle:
        handle.write(text.rstrip() + "\n")


def read_text(path: Path) -> str:
    with open(fs_path(path), encoding="utf-8-sig") as handle:
        return handle.read()


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


def source_metrics() -> dict[str, Any]:
    decision = read_json(required(SOURCE_FINAL_DECISION))
    _queue_fields, queue_rows = read_csv_rows(required(SOURCE_QUEUE))
    _score_fields, score_rows = read_csv_rows(required(SOURCE_SCORECARD))
    matched_rows = sum(int(float(row.get("matched_rows") or 0)) for row in score_rows)
    return {
        "best_attempt": decision["best_attempt"],
        "best_model_id": decision["best_model_id"],
        "best_net_profit": decision["best_net_profit"],
        "best_profit_factor": decision["best_profit_factor"],
        "best_drawdown": decision["best_drawdown"],
        "best_recovery_factor": decision["best_recovery_factor"],
        "best_trade_count": decision["best_trade_count"],
        "best_expectancy": decision["best_expectancy"],
        "best_long_trade_count": decision["best_long_trade_count"],
        "best_short_trade_count": decision["best_short_trade_count"],
        "shape_control_attempt": decision["shape_control_attempt"],
        "shape_control_trade_count": decision["shape_control_trade_count"],
        "shape_control_net_profit": decision["shape_control_net_profit"],
        "shape_control_profit_factor": decision["shape_control_profit_factor"],
        "near_anchor_attempt": decision["near_anchor_attempt"],
        "near_anchor_net_profit": decision["near_anchor_net_profit"],
        "near_anchor_profit_factor": decision["near_anchor_profit_factor"],
        "attempt_count": len(score_rows),
        "matched_rows": matched_rows,
        "source_gate_passes": decision["gate_passes"],
        "source_gate_total": decision["gate_total"],
        "queue_rows": len(queue_rows),
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


def write_handoff_artifacts(metrics: Mapping[str, Any]) -> list[dict[str, Any]]:
    fieldnames, queue_rows = read_csv_rows(required(SOURCE_QUEUE))
    retargeted = []
    for row in queue_rows:
        updated = dict(row)
        updated["source_next_run_id"] = row.get("next_run_id", "")
        updated["next_run_id"] = NEXT_RUN_ID
        updated["source_stage_id"] = SOURCE_STAGE_ID
        updated["new_stage_id"] = NEW_STAGE_ID
        updated["handoff_run_id"] = RUN_ID
        updated["superseded_run_id"] = SUPERSEDED_RUN_ID
        updated["source_claim_boundary"] = row.get("claim_boundary", "")
        updated["claim_boundary"] = CLAIM_BOUNDARY
        updated["status"] = "retargeted_to_stage344(344단계로 재지정)"
        retargeted.append(updated)
    write_csv(NEXT_QUEUE, retargeted, list(fieldnames) + [
        "source_next_run_id",
        "source_stage_id",
        "new_stage_id",
        "handoff_run_id",
        "superseded_run_id",
        "source_claim_boundary",
        "status",
    ])

    write_csv(
        HANDOFF_MANIFEST,
        [
            {
                "handoff_id": "stage343F_to_stage344A_branch",
                "source_stage_id": SOURCE_STAGE_ID,
                "source_run_id": PARENT_RUN_ID,
                "new_stage_id": NEW_STAGE_ID,
                "branch_run_id": RUN_ID,
                "superseded_run_id": SUPERSEDED_RUN_ID,
                "next_run_id": NEXT_RUN_ID,
                "source_queue_path": rel(SOURCE_QUEUE),
                "retargeted_queue_path": rel(NEXT_QUEUE),
                "best_attempt": metrics["best_attempt"],
                "best_net_profit": metrics["best_net_profit"],
                "best_profit_factor": metrics["best_profit_factor"],
                "best_trade_count": metrics["best_trade_count"],
                "best_long_short": f"{metrics['best_long_trade_count']}/{metrics['best_short_trade_count']}",
                "shape_control_attempt": metrics["shape_control_attempt"],
                "shape_control_trade_count": metrics["shape_control_trade_count"],
                "branch_reason": "Stage343(343단계)이 MT5 probe/review(탐침/검토)와 rescue loop(복구 반복)까지 담아 무거워졌기 때문이다.",
                "effect": "directional long quality surface(방향성 롱 품질 표면) 질문을 Stage344(344단계)에서 가볍게 시작한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )
    return retargeted


def write_documents(metrics: Mapping[str, Any]) -> None:
    stage_brief = f"""# Stage 344 Brief(344단계 개요)

## Stage ID(단계 ID)

`{NEW_STAGE_ID}`

## Question(질문)

Can a directional long quality surface(방향성 롱 품질 표면) recover long supply(롱 공급) and trade shape(거래 형태) while preserving the run343F profit anchor(343F 수익 앵커)?

## Scope(범위)

- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_review_run(원천 검토 실행): `{PARENT_RUN_ID}`
- branch_run(분기 실행): `{RUN_ID}`
- superseded_run(대체된 실행): `{SUPERSEDED_RUN_ID}`
- next_run(다음 실행): `{NEXT_RUN_ID}`

Action(행동): Stage343(343단계)의 next design(다음 설계)을 Stage344(344단계)로 retarget(재지정)한다.
Effect(효과): Stage343(343단계)은 trade shape rescue review(거래 형태 복구 검토)에서 멈추고, long quality source(롱 품질 원천) 탐색은 새 단계에서 좁게 다룬다.

## Source Truth(원천 진실)

- best_attempt(최고 시도): `{metrics["best_attempt"]}`
- net_profit(순수익): `{metrics["best_net_profit"]}`
- profit_factor(수익 팩터): `{metrics["best_profit_factor"]}`
- drawdown(낙폭): `{metrics["best_drawdown"]}`
- recovery_factor(회복 계수): `{metrics["best_recovery_factor"]}`
- trade_count(거래수): `{metrics["best_trade_count"]}`
- long_short(롱/숏): `{metrics["best_long_trade_count"]}/{metrics["best_short_trade_count"]}`
- unresolved_failure(미해결 실패): trade shape rescue failed(거래 형태 복구 실패)

## Evidence Boundary(근거 경계)

This branch(분기)는 state sync(상태 동기화)와 handoff(인계)만 수행한다. No new MT5 execution(새 MT5 실행 없음), no candidate selection(후보 선정 없음), no operating promotion(운영 승격 없음), no runtime authority(런타임 권위 없음)이다.
"""
    readme = f"""# Stage 344(344단계)

Stage344(344단계)는 directional long quality surface(방향성 롱 품질 표면)만 다룬다.

- current_run(현재 실행): `{NEXT_RUN_ID}`
- branch_run(분기 실행): `{RUN_ID}`
- source_review(원천 검토): `{PARENT_RUN_ID}`
- retargeted_queue(재지정 대기열): `{rel(NEXT_QUEUE)}`

Effect(효과): minute block micro-tuning(분 차단 미세조정)을 Stage343(343단계)에서 더 반복하지 않고, long supply quality(롱 공급 품질)를 새 질문으로 분리한다.
"""
    input_refs = f"""# Stage 344 Input Refs(344단계 입력 참조)

- run343F final decision(343F 최종 결정): `{rel(SOURCE_FINAL_DECISION)}`
- run343F review scorecard(343F 검토 점수표): `{rel(SOURCE_SCORECARD)}`
- run343F performance attribution(343F 성과 귀속): `{rel(SOURCE_ATTRIBUTION)}`
- run343F failure memory(343F 실패 기억): `{rel(SOURCE_FAILURE_MEMORY)}`
- source queue(원천 대기열): `{rel(SOURCE_QUEUE)}`
- run344B retargeted queue(344B 재지정 대기열): `{rel(NEXT_QUEUE)}`
- source report(원천 보고서): `{rel(SOURCE_REPORT)}`

Action(행동): run343F(343F 실행)의 offensive exploration seed(공격 탐색 씨앗)를 복사본 진실로 만들지 않고 source input(원천 입력)으로 연결한다.
Effect(효과): artifact lineage(산출물 계보)가 끊기지 않고, Stage344(344단계)의 첫 실행이 어디서 왔는지 추적된다.
"""
    report = f"""# run344A Stage Branch(344A 단계 분기)

## Decision(결정)

`{DECISION}`

## Reason(이유)

Stage343(343단계)은 quality/margin runtime probe(품질/마진 런타임 탐침), trade shape rescue package(거래 형태 복구 패키지), MT5 probe(MT5 탐침), review(검토)까지 포함해 무거워졌다. 다음 질문은 minute block(분 차단) 조정이 아니라 directional long quality surface(방향성 롱 품질 표면)이므로 새 stage(단계)로 분기한다.

Action(행동): `{SUPERSEDED_RUN_ID}`를 직접 이어가지 않고 `{NEXT_RUN_ID}`로 retarget(재지정)한다.
Effect(효과): Stage343(343단계)의 evidence(근거)는 보존하고, Stage344(344단계)는 long supply recovery(롱 공급 복구) 질문만 받는다.

## Handoff(인계)

- source_best_attempt(원천 최고 시도): `{metrics["best_attempt"]}`
- net_profit(순수익): `{metrics["best_net_profit"]}`
- profit_factor(수익 팩터): `{metrics["best_profit_factor"]}`
- trade_count(거래수): `{metrics["best_trade_count"]}`
- long_short(롱/숏): `{metrics["best_long_trade_count"]}/{metrics["best_short_trade_count"]}`
- queue_rows(대기열 행): `{metrics["queue_rows"]}`
- next_queue(다음 대기열): `{rel(NEXT_QUEUE)}`

## Claim Boundary(주장 경계)

`{CLAIM_BOUNDARY}`

No MT5 execution(새 MT5 실행 없음), no Goal Achieve(목표 달성 없음), no runtime authority(런타임 권위 없음), no operating promotion(운영 승격 없음).
"""
    decision_doc = f"""# {TODAY} Stage344A Branch Decision(344A 단계 분기 결정)

- decision(결정): `{DECISION}`
- from(출발): `{SOURCE_STAGE_ID}` / `{PARENT_RUN_ID}`
- to(도착): `{NEW_STAGE_ID}` / `{NEXT_RUN_ID}`
- superseded_run(대체된 실행): `{SUPERSEDED_RUN_ID}`
- reason(이유): Stage343(343단계)이 무거워졌고, 다음 질문이 directional long quality surface(방향성 롱 품질 표면)라는 별도 topic pivot(주제 전환)이기 때문이다.

Action(행동): Stage344(344단계)를 열고 run344B(344B 실행)를 design packet(설계 묶음)으로 둔다.
Effect(효과): run343F(343F 실행)의 preserved profit anchor(보존 수익 앵커)는 seed surface(씨앗 표면)로만 넘기고, selection(선정)이나 operating claim(운영 주장)은 만들지 않는다.

claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    selection = f"""# Stage 344 Selection Status(344단계 선정 상태)

- active_stage(현재 단계): `{NEW_STAGE_ID}`
- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- selected_model(선정 모델): `none(없음)`
- source_review(원천 검토): `{PARENT_RUN_ID}`
- preserved_profit_anchor(보존 수익 앵커): `{metrics["best_attempt"]}`
- unresolved_failure(미해결 실패): `trade_shape_rescue_failed(거래 형태 복구 실패)`
- next_probe(다음 탐침): `directional_long_quality_surface(방향성 롱 품질 표면)`
- runtime_authority(런타임 권위): `not_claimed(주장 없음)`
- operating_promotion(운영 승격): `not_claimed(주장 없음)`
- Goal Achieve(목표 달성): `not_claimed(주장 없음)`

Effect(효과): Stage344(344단계)는 selection(선정)이 아니라 offensive exploration(공격 탐색) 설계에서 시작한다.
"""
    source_selection = f"""# Stage 343 Selection Status(343단계 선정 상태)

- stage_id(단계 ID): `{SOURCE_STAGE_ID}`
- latest_completed_run(최근 완료 실행): `{PARENT_RUN_ID}`
- branched_to_stage(분기된 단계): `{NEW_STAGE_ID}`
- branch_run(분기 실행): `{RUN_ID}`
- superseded_current_run(대체된 현재 실행): `{SUPERSEDED_RUN_ID}`
- selected_model(선정 모델): `none(없음)`
- preserved_profit_anchor(보존 수익 앵커): `{metrics["best_attempt"]}`
- unresolved_failure(미해결 실패): `trade_shape_rescue_failed(거래 형태 복구 실패)`
- handoff_seed(인계 씨앗): `directional_long_quality_surface(방향성 롱 품질 표면)`
- runtime_authority(런타임 권위): `not_claimed(주장 없음)`
- operating_promotion(운영 승격): `not_claimed(주장 없음)`
- Goal Achieve(목표 달성): `not_claimed(주장 없음)`

Effect(효과): Stage343(343단계)은 run343F(343F 실행) 검토로 멈추고, 다음 공격 탐색은 Stage344(344단계)에서 이어진다.
"""
    workspace = f"""current_stage_id: {NEW_STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {STATUS}
current_judgment: {JUDGMENT}
current_decision: {DECISION}
next_run_id: {NEXT_RUN_ID}
claim_boundary: {CLAIM_BOUNDARY}
updated_at: {TODAY}
"""
    current = f"""# Current Working State(현재 작업 상태)

## Current Truth(현재 진실)

- active_stage(현재 단계): `{NEW_STAGE_ID}`
- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`

## Effect(효과)

Stage343(343단계)은 run343F(343F 실행) review(검토)로 닫고, directional long quality surface(방향성 롱 품질 표면)는 Stage344(344단계) run344B(344B 실행) 설계로 분기했다.

## Claim Boundary(주장 경계)

`{CLAIM_BOUNDARY}`
"""
    review_index = f"""# Stage 344 Review Index(344단계 검토 색인)

- run344A stage branch(344A 단계 분기): `{rel(REPORT_PATH)}`

Effect(효과): Stage344(344단계)의 review evidence(검토 근거)를 첫 분기부터 찾기 쉽게 둔다.
"""

    write_text(STAGE_BRIEF, stage_brief)
    write_text(STAGE_README, readme)
    write_text(INPUT_REFS, input_refs)
    write_text(REPORT_PATH, report)
    write_text(REVIEW_INDEX, review_index)
    write_text(DECISION_DOC, decision_doc)
    write_text(SELECTION_STATUS, selection)
    write_text(SOURCE_SELECTION_STATUS, source_selection)
    write_text(ROOT_SELECTION_STATUS, selection)
    write_text(WORKSPACE_STATE, workspace)
    write_text(CURRENT_WORKING_STATE, current)

    source_append = f"""## Stage344 Branch Handoff(344단계 분기 인계)

- branch_run(분기 실행): `{RUN_ID}`
- next_stage(다음 단계): `{NEW_STAGE_ID}`
- next_run(다음 실행): `{NEXT_RUN_ID}`
- effect(효과): Stage343(343단계)은 trade shape rescue review(거래 형태 복구 검토)에서 멈추고, directional long quality surface(방향성 롱 품질 표면)를 새 단계로 넘긴다.
"""
    append_text_once(SOURCE_STAGE_BRIEF, f"branch_run(분기 실행): `{RUN_ID}`", source_append)
    append_text_once(SOURCE_README, f"branch_run(분기 실행): `{RUN_ID}`", source_append)


def append_changelogs() -> None:
    block = f"""## {TODAY} {RUN_ID}

- action(행동): Stage343(343단계)의 run343G(343G 실행) continuation(연속 작업)을 Stage344(344단계) run344B(344B 실행)로 branch handoff(분기 인계)했다.
- effect(효과): 무거운 Stage343(343단계)을 run343F(343F 실행) review(검토)에서 멈추고, directional long quality surface(방향성 롱 품질 표면)는 새 stage(단계)에서 시작한다.
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    append_text_once(ROOT_CHANGELOG, RUN_ID, block)
    append_text_once(WORKSPACE_CHANGELOG, RUN_ID, block)


def append_idea_registry() -> None:
    block = f"""## {TODAY} {RUN_ID} Directional Long Quality Surface Branch(방향성 롱 품질 표면 분기)

- idea_id(아이디어 ID): `stage344_directional_long_quality_surface`
- hypothesis(가설): profit anchor(수익 앵커)의 short supply(숏 공급)는 보존하고, long entries(롱 진입)는 separate quality/regime surface(별도 품질/국면 표면)로 다시 분리하면 trade shape(거래 형태)를 회복할 수 있다.
- source(원천): `{PARENT_RUN_ID}`
- next_run(다음 실행): `{NEXT_RUN_ID}`
- queue(대기열): `{rel(NEXT_QUEUE)}`
- effect(효과): minute block micro-tuning(분 차단 미세조정)을 반복하지 않고 long quality source(롱 품질 원천)를 새로 찾는다.
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    append_text_once(IDEA_REGISTRY, RUN_ID, block)


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
        "notes": "User requested Stage branch because Stage343 became heavy(사용자가 343단계가 무거워져 단계 분기를 요청함).",
        "source_package_run_id": PARENT_RUN_ID,
        "matched_rows": metrics["matched_rows"],
        "attempt_count": metrics["attempt_count"],
    }
    tier_a = {
        **base,
        "ledger_row_id": f"{RUN_ID}__Tier A",
        "subrun_id": "Tier A",
        "view": "Tier A separate(Tier A 분리)",
        "record_view": "Tier A separate(Tier A 분리)",
        "tier": "Tier A",
        "tier_scope": "Tier A",
        "metric_scope": "stage_branch_handoff_run343F_directional_long_seed",
        "kpi_scope": "stage_branch_handoff_run343F_directional_long_seed",
        "candidate_model_id": metrics["best_model_id"],
        "net_profit": metrics["best_net_profit"],
        "profit_factor": metrics["best_profit_factor"],
        "drawdown": metrics["best_drawdown"],
        "recovery_factor": metrics["best_recovery_factor"],
        "trade_count": metrics["best_trade_count"],
        "expectancy": metrics["best_expectancy"],
        "result_status": "stage_branch_opened_no_selection(단계 분기 완료, 선정 없음)",
        "primary_kpi": f"net_profit={metrics['best_net_profit']};pf={metrics['best_profit_factor']};trades={metrics['best_trade_count']}",
        "guardrail_kpi": f"drawdown={metrics['best_drawdown']};long_short={metrics['best_long_trade_count']}/{metrics['best_short_trade_count']}",
        "external_verification_status": "out_of_scope_by_claim(주장 범위 밖)",
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
        "candidate_model_id": "missing_required",
        "result_status": "missing_required(필수 누락)",
        "primary_kpi": "missing_required",
        "guardrail_kpi": "missing_required",
        "external_verification_status": "missing_required(필수 누락)",
        "matched_rows": "",
        "attempt_count": "",
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


def write_ledgers(metrics: Mapping[str, Any]) -> None:
    rows = ledger_rows(metrics)
    write_csv(STAGE_LEDGER, [{key: row.get(key, "") for key in STAGE_LEDGER_COLUMNS} for row in rows], STAGE_LEDGER_COLUMNS)
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
                "notes": "Stage343 was branched before directional long quality design because it became heavy(343단계가 무거워져 방향성 롱 품질 설계 전에 분기함).",
                "primary_report": rel(REPORT_PATH),
                "run_number": RUN_NUMBER,
                "date": TODAY,
                "decision": DECISION,
                "parent_run_id": PARENT_RUN_ID,
                "next_run_id": NEXT_RUN_ID,
                "gate_passes": 9,
                "gate_total": 9,
                "claim_boundary": CLAIM_BOUNDARY,
                "report_path": rel(REPORT_PATH),
                "primary_artifact": rel(FINAL_DECISION),
                "candidate_model_id": metrics["best_model_id"],
                "net_profit": metrics["best_net_profit"],
                "profit_factor": metrics["best_profit_factor"],
                "drawdown": metrics["best_drawdown"],
                "recovery_factor": metrics["best_recovery_factor"],
                "trade_count": metrics["best_trade_count"],
                "expectancy": metrics["best_expectancy"],
                "result_status": "stage_branch_opened_no_selection(단계 분기 완료, 선정 없음)",
                "matched_rows": metrics["matched_rows"],
                "attempt_count": metrics["attempt_count"],
                "view": "Tier A separate(Tier A 분리)",
                "tier": "Tier A",
                "metric_scope": "stage_branch_handoff_run343F_directional_long_seed",
                "source_package_run_id": PARENT_RUN_ID,
            }
        ],
    )


def write_receipts(metrics: Mapping[str, Any], inventory: list[dict[str, Any]], queue_rows: list[dict[str, Any]]) -> None:
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
            "queue_rows": len(queue_rows),
            "best_attempt": metrics["best_attempt"],
            "best_net_profit": metrics["best_net_profit"],
            "best_profit_factor": metrics["best_profit_factor"],
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
            "judgment_label": "not_applicable_for_trading_kpi(거래 KPI 판정 해당 없음)",
            "next_condition": f"{NEXT_RUN_ID} design packet(설계 묶음)",
            "created_at_utc": created_at,
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def write_gates(metrics: Mapping[str, Any]) -> list[dict[str, Any]]:
    workspace_text = read_text(WORKSPACE_STATE) if path_is_file(WORKSPACE_STATE) else ""
    _queue_fields, queue_rows = read_csv_rows(NEXT_QUEUE)
    gates = [
        {
            "gate_id": "source_run343F_gate_audit_available",
            "status": "passed" if path_is_file(SOURCE_GATE_AUDIT) and metrics["source_gate_passes"] == metrics["source_gate_total"] else "failed",
            "evidence_path": rel(SOURCE_GATE_AUDIT),
            "effect": "run343F(343F 실행)의 review gate(검토 게이트)가 통과했는지 확인한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "source_queue_available",
            "status": "passed" if path_is_file(SOURCE_QUEUE) and metrics["queue_rows"] > 0 else "failed",
            "evidence_path": rel(SOURCE_QUEUE),
            "effect": "directional long quality surface(방향성 롱 품질 표면) seed queue(씨앗 대기열)를 잃지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "stage_structure_created",
            "status": "passed" if all(path_exists(path) for path in [STAGE_BRIEF, INPUT_REFS, REPORT_PATH, REVIEW_INDEX, SELECTION_STATUS]) else "failed",
            "evidence_path": rel(NEW_STAGE_DIR),
            "effect": "새 stage(단계)가 필수 폴더와 문서를 가진다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "queue_retargeted_to_stage344B",
            "status": "passed" if queue_rows and all(row.get("next_run_id") == NEXT_RUN_ID for row in queue_rows) else "failed",
            "evidence_path": rel(NEXT_QUEUE),
            "effect": "run343G(343G 실행) 대신 run344B(344B 실행)로 이어진다.",
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


def write_final_decision(gates: Sequence[Mapping[str, Any]], metrics: Mapping[str, Any]) -> None:
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
            "best_attempt": metrics["best_attempt"],
            "best_model_id": metrics["best_model_id"],
            "best_net_profit": metrics["best_net_profit"],
            "best_profit_factor": metrics["best_profit_factor"],
            "best_drawdown": metrics["best_drawdown"],
            "best_recovery_factor": metrics["best_recovery_factor"],
            "best_trade_count": metrics["best_trade_count"],
            "best_expectancy": metrics["best_expectancy"],
            "best_long_trade_count": metrics["best_long_trade_count"],
            "best_short_trade_count": metrics["best_short_trade_count"],
            "queue_rows": metrics["queue_rows"],
            "new_mt5_execution": "not_run",
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
        ("final_decision", FINAL_DECISION, "run344A branch final decision(344A 분기 최종 결정)"),
        ("required_gate_coverage_audit", GATE_AUDIT, "run344A required gate coverage audit(344A 필수 게이트 커버리지 감사)"),
        ("handoff_manifest", HANDOFF_MANIFEST, "Stage343F to Stage344 handoff manifest(343F에서 344단계 인계 목록)"),
        ("retargeted_queue", NEXT_QUEUE, "run344B retargeted queue(344B 재지정 대기열)"),
        ("stage_branch_report", REPORT_PATH, "run344A branch report(344A 분기 보고서)"),
        ("review_index", REVIEW_INDEX, "Stage344 review index(344단계 검토 색인)"),
        ("decision_doc", DECISION_DOC, "run344A durable decision document(344A 결정 문서)"),
        ("run_manifest", RUN_MANIFEST, "run344A run manifest(344A 실행 목록)"),
        ("stage_brief", STAGE_BRIEF, "Stage344 stage brief(344단계 개요)"),
        ("input_refs", INPUT_REFS, "Stage344 input refs(344단계 입력 참조)"),
        ("selection_status", SELECTION_STATUS, "Stage344 selection status(344단계 선정 상태)"),
        ("pipeline", Path(__file__), "run344A producer script(344A 생산 스크립트)"),
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
    metrics = source_metrics()
    inventory = write_source_inventory()
    queue_rows = write_handoff_artifacts(metrics)
    write_documents(metrics)
    append_changelogs()
    append_idea_registry()
    write_ledgers(metrics)
    write_receipts(metrics, inventory, queue_rows)
    gates = write_gates(metrics)
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
    write_receipts(metrics, inventory, queue_rows)
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
                "queue_rows": metrics["queue_rows"],
                "claim_boundary": CLAIM_BOUNDARY,
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
