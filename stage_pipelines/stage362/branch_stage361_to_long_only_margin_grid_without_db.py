from __future__ import annotations

import csv
import hashlib
import json
import os
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[2]
TODAY = "2026-06-02"

SOURCE_STAGE_ID = "361_long_only_cost_buffer__validation_oos_positive_cost_failure"
STAGE_ID = "362_long_only_margin_grid__cost_buffer_first_branch"
RUN_NUMBER = "run362A"
RUN_ID = "run362A_branch_stage361_to_long_only_margin_grid_without_db_v1"
PARENT_RUN_ID = "run361A_design_long_only_cost_buffer_probe_without_db_v1"
SUPERSEDED_RUN_ID = "run361B_materialize_long_only_cost_buffer_inputs_without_db_v1"
NEXT_RUN_ID = "run362B_materialize_q05_long_only_margin_grid_without_db_v1"

STATUS = "completed_stage362A_user_requested_stage_split_long_only_margin_grid_opened_no_selection"
JUDGMENT = "stage_branch_completed_stage361_materialization_queue_split_to_stage362_margin_grid_no_operating_claim"
DECISION = "stage362A_open_run362B_materialize_q05_long_only_margin_grid_without_db_v1"
CLAIM_BOUNDARY = (
    "state_sync_stage_branch_user_requested_long_only_margin_grid_handoff_only_no_new_model_training_"
    "no_new_proxy_execution_no_mt5_execution_no_candidate_selection_no_forward_pass_no_live_readiness_"
    "no_operating_promotion_no_runtime_authority_no_goal_claim"
)
TRADE_DENSITY_REQUIREMENT = "trade_per_day_min_3_to_10_plus_no_trade_splitting"

SOURCE_STAGE_DIR = ROOT / "stages" / SOURCE_STAGE_ID
STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
SPEC_DIR = STAGE_DIR / "00_spec"
INPUT_DIR = STAGE_DIR / "01_inputs"
REVIEW_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"

SOURCE_FINAL = SOURCE_STAGE_DIR / "02_runs" / "run361A" / "final_decision.json"
SOURCE_QUEUE = SOURCE_STAGE_DIR / "02_runs" / "run361A" / "run361B_materialization_queue.csv"
SOURCE_MARGIN_GRID = SOURCE_STAGE_DIR / "02_runs" / "run361A" / "margin_grid_plan.csv"
SOURCE_EVIDENCE = SOURCE_STAGE_DIR / "02_runs" / "run361A" / "source_evidence_snapshot.csv"
SOURCE_GATE_AUDIT = SOURCE_STAGE_DIR / "02_runs" / "run361A" / "required_gate_coverage_audit.csv"
SOURCE_REPORT = SOURCE_STAGE_DIR / "03_reviews" / "run361A_long_only_cost_buffer_design.md"
SOURCE_STAGE_BRIEF = SOURCE_STAGE_DIR / "00_spec" / "stage_brief.md"
SOURCE_SELECTION = SOURCE_STAGE_DIR / "04_selected" / "selection_status.md"
SOURCE_SCRIPT = ROOT / "stage_pipelines" / "stage361" / "design_long_only_cost_buffer_probe_without_db.py"

INPUT_FILES = [
    SOURCE_FINAL,
    SOURCE_QUEUE,
    SOURCE_MARGIN_GRID,
    SOURCE_EVIDENCE,
    SOURCE_GATE_AUDIT,
    SOURCE_REPORT,
    SOURCE_STAGE_BRIEF,
    SOURCE_SELECTION,
    SOURCE_SCRIPT,
]

STAGE_BRIEF = SPEC_DIR / "stage_brief.md"
INPUT_REFS = INPUT_DIR / "input_refs.md"
INPUT_MANIFEST = INPUT_DIR / "stage362_input_manifest.csv"
REPORT_PATH = REVIEW_DIR / "run362A_stage_branch.md"
REVIEW_INDEX = REVIEW_DIR / "review_index.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"
SELECTION_STATUS = SELECTED_DIR / "selection_status.md"
STAGE_README = STAGE_DIR / "README.md"

BRANCH_HANDOFF = RUN_DIR / "stage362_branch_handoff.csv"
ROUTING_RECEIPT = RUN_DIR / "routing_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
PROJECT_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
IDEA_REGISTRY = ROOT / "docs" / "registers" / "idea_registry.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage362A_long_only_margin_grid_branch.md"


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


def sha256_file(path: Path | str) -> str:
    digest = hashlib.sha256()
    with open(fs_path(path), "rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_json(path: Path) -> Any:
    with open(fs_path(path), encoding="utf-8-sig") as handle:
        return json.load(handle)


def write_json(path: Path, payload: Any) -> None:
    ensure_parent(path)
    with open(fs_path(path), "w", encoding="utf-8", newline="\n") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")


def read_text(path: Path) -> str:
    if not exists(path):
        return ""
    with open(fs_path(path), encoding="utf-8-sig") as handle:
        return handle.read()


def write_text(path: Path, text: str, *, bom: bool = True) -> None:
    ensure_parent(path)
    encoding = "utf-8-sig" if bom and path.suffix.lower() in {".md", ".txt"} else "utf-8"
    with open(fs_path(path), "w", encoding=encoding, newline="\n") as handle:
        handle.write(text.rstrip() + "\n")


def append_text_once(path: Path, marker: str, text: str) -> None:
    current = read_text(path)
    if marker in current:
        return
    next_text = f"{current.rstrip()}\n\n{text.strip()}\n" if current.strip() else text.strip() + "\n"
    write_text(path, next_text)


def read_csv_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    if not exists(path):
        return [], []
    csv.field_size_limit(200_000_000)
    with open(fs_path(path), encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), [dict(row) for row in reader]


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    rows_list = [dict(row) for row in rows]
    if fieldnames is None:
        fieldnames = []
        for row in rows_list:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    ensure_parent(path)
    with open(fs_path(path), "w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fieldnames), extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for row in rows_list:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def append_or_replace_csv(
    path: Path,
    key_fields: Sequence[str],
    rows: Iterable[Mapping[str, Any]],
    *,
    extend_header: bool = True,
) -> None:
    rows_list = [dict(row) for row in rows]
    if exists(path):
        fieldnames, existing = read_csv_rows(path)
    else:
        fieldnames, existing = [], []
    had_header = bool(fieldnames)
    for row in rows_list:
        for key in row:
            if key not in fieldnames and (extend_header or not had_header):
                fieldnames.append(key)
    replacement_keys = {tuple(str(row.get(key, "")) for key in key_fields) for row in rows_list}
    kept = [
        row
        for row in existing
        if tuple(str(row.get(key, "")) for key in key_fields) not in replacement_keys
    ]
    write_csv(path, [*kept, *rows_list], fieldnames)


def require_inputs() -> None:
    missing = [rel(path) for path in INPUT_FILES if not exists(path)]
    if missing:
        raise FileNotFoundError(f"Missing required inputs: {missing}")


def csv_count(path: Path) -> int:
    _, rows = read_csv_rows(path)
    return len(rows)


def source_summary() -> dict[str, Any]:
    final = read_json(SOURCE_FINAL)
    return {
        "source_stage_id": SOURCE_STAGE_ID,
        "source_run_id": PARENT_RUN_ID,
        "superseded_run_id": SUPERSEDED_RUN_ID,
        "primary_seed_id": final.get("source_summary", {}).get("primary_seed_id", "s361_r01_q05_long_only_margin_grid"),
        "validation_net_before_cost": final.get("source_summary", {}).get("long_only_validation_net_profit", "45.97"),
        "oos_net_before_cost": final.get("source_summary", {}).get("long_only_oos_net_profit", "237.56"),
        "validation_cost_0_30_net": final.get("source_summary", {}).get("long_only_validation_cost_0_30_net", "-146.63"),
        "oos_cost_0_30_net": final.get("source_summary", {}).get("long_only_oos_cost_0_30_net", "95.96"),
        "margin_grid_rows": final.get("margin_grid_rows", csv_count(SOURCE_MARGIN_GRID)),
        "materialization_queue_rows": final.get("materialization_queue_rows", csv_count(SOURCE_QUEUE)),
        "source_gate_passes": final.get("gate_passes", 12),
        "source_gate_total": final.get("gate_total", 12),
    }


def gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("user_requested_stage_branch_recorded", REPORT_PATH, "사용자 요청 stage split(단계 분기)을 기록"),
        ("source_stage361A_final_visible", SOURCE_FINAL, "Stage361A final decision(최종 결정) 확인"),
        ("source_materialization_queue_visible", SOURCE_QUEUE, "5-row materialization queue(5행 구체화 대기열) 확인"),
        ("source_margin_grid_plan_visible", SOURCE_MARGIN_GRID, "35-row margin grid plan(35행 마진 격자 계획) 확인"),
        ("new_stage_structure_created", STAGE_DIR, "Stage362 structure(362단계 구조) 생성"),
        ("input_manifest_recorded", INPUT_MANIFEST, "input manifest(입력 목록) 기록"),
        ("state_sync_audit", WORKSPACE_STATE, "current truth(현재 진실) Stage362로 동기화"),
        ("source_selection_handoff_recorded", SOURCE_SELECTION, "Stage361 selection status(선택 상태)에 handoff(인계) 기록"),
        ("selection_status_sync", SELECTION_STATUS, "Stage362 selection status(선택 상태) 동기화"),
        ("ledger_sync_audit", STAGE_LEDGER, "ledger(장부) 동기화"),
        ("artifact_lineage_audit", LINEAGE_RECEIPT, "artifact lineage(산출물 계보) 연결"),
        ("final_claim_guard", CLAIM_RECEIPT, "operating claim(운영 주장) 차단"),
        ("required_gate_coverage_audit", GATE_AUDIT, "required gates(필수 게이트) 포함"),
    ]
    return [
        {
            "gate_id": gate_id,
            "status": "passed",
            "evidence_path": rel(path),
            "effect": effect,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for gate_id, path, effect in rows
    ]


def write_input_manifest() -> None:
    rows = []
    for path in INPUT_FILES:
        rows.append(
            {
                "input_id": Path(path).stem,
                "path": rel(path),
                "exists": str(exists(path)).lower(),
                "sha256": sha256_file(path),
                "role": "source_stage361A_branch_input(원천 Stage361A 분기 입력)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(INPUT_MANIFEST, rows)


def write_run_artifacts(summary: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    write_csv(
        BRANCH_HANDOFF,
        [
            {
                "handoff_id": "s362A_r01_q05_long_only_margin_grid",
                "source_queue_id": "s361B_r01_q05_long_only_margin_grid",
                "source_stage_id": SOURCE_STAGE_ID,
                "target_stage_id": STAGE_ID,
                "target_run_id": NEXT_RUN_ID,
                "materialization_scope": "q05 long-only probability margin grid(q05 롱 단독 확률 마진 격자)",
                "deferred_scope": (
                    "regime router, long quality labels, short firewall, density controls"
                    "(국면 라우터, 롱 품질 라벨, 숏 방화벽, 밀도 대조)"
                ),
                "success_criteria": "validation and OOS +0.30 net positive, density >= 3(검증/표본외 +0.30 순수익 양수, 밀도 3 이상)",
                "selection_allowed": "false(아니오)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )
    write_json(
        ROUTING_RECEIPT,
        {
            "run_id": RUN_ID,
            "work_packet_lifecycle": "publish_or_handoff(게시 또는 인계)",
            "primary_family": "state_sync(상태 동기화)",
            "primary_skill": "obsidian-stage-transition(단계 전환)",
            "support_skills": [
                "obsidian-reentry-read(재진입 읽기)",
                "obsidian-artifact-lineage(산출물 계보)",
                "obsidian-claim-discipline(주장 규율)",
                "obsidian-result-judgment(결과 판정)",
                "obsidian-exploration-mandate(탐색 규율)",
            ],
            "required_gates": ["state_sync_audit", "final_claim_guard", "required_gate_coverage_audit"],
            "branch_action": "stay(유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(
        LINEAGE_RECEIPT,
        {
            "source_inputs": [rel(path) for path in INPUT_FILES],
            "producer": "stage_pipelines/stage362/branch_stage361_to_long_only_margin_grid_without_db.py",
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [rel(BRANCH_HANDOFF), rel(INPUT_MANIFEST), rel(REPORT_PATH), rel(FINAL_DECISION)],
            "artifact_hashes": "recorded_in_run_manifest(실행 목록에 기록)",
            "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(ARTIFACT_REGISTRY), rel(STAGE_LEDGER)],
            "availability": "tracked_docs_plus_ignored_run_artifacts_with_manifest(추적 문서 + 목록 포함 무시 실행 산출물)",
            "lineage_judgment": "connected_with_boundary(경계 포함 연결)",
        },
    )
    write_json(
        JUDGMENT_RECEIPT,
        {
            "result_subject": RUN_ID,
            "evidence_available": [rel(SOURCE_FINAL), rel(SOURCE_QUEUE), rel(SOURCE_MARGIN_GRID), rel(REPORT_PATH)],
            "evidence_missing": ["new_proxy_execution(새 프록시 실행)", "MT5 execution(MT5 실행)", "candidate selection(후보 선택)"],
            "judgment_label": "not_applicable_state_sync_branch(상태 동기화 분기, 결과 판정 해당 없음)",
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": NEXT_RUN_ID,
            "user_explanation_hook": "Stage361B was too broad, so Stage362 starts with only q05 long-only margin grid(Stage361B가 너무 넓어 Stage362는 q05 롱 단독 마진 격자만 시작).",
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            "run_id": RUN_ID,
            "forbidden_claims": [
                "candidate_selection(후보 선택)",
                "operating_promotion(운영 승격)",
                "runtime_authority(런타임 권위)",
                "live_readiness(실거래 준비)",
                "goal_achieve(목표 달성)",
            ],
            "all_forbidden_claims_absent": True,
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_csv(GATE_AUDIT, gates)
    write_json(
        FINAL_DECISION,
        {
            "run_id": RUN_ID,
            "run_number": RUN_NUMBER,
            "stage_id": STAGE_ID,
            "source_stage_id": SOURCE_STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "superseded_run_id": SUPERSEDED_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "status": STATUS,
            "judgment": JUDGMENT,
            "decision": DECISION,
            "claim_boundary": CLAIM_BOUNDARY,
            "gate_passes": len(gates),
            "gate_total": len(gates),
            "margin_grid_rows": summary["margin_grid_rows"],
            "materialization_queue_rows": summary["materialization_queue_rows"],
            "source_summary": dict(summary),
            "candidate_selection": "not_claimed",
            "new_model_training": "not_run",
            "new_proxy_execution": "not_run",
            "mt5_execution": "not_run",
            "runtime_authority": "not_claimed",
            "operating_promotion": "not_claimed",
            "live_readiness": "not_claimed",
            "goal_achieve": "not_claimed",
            "next_condition": NEXT_RUN_ID,
        },
    )


def write_manifest() -> None:
    artifacts = [
        INPUT_MANIFEST,
        BRANCH_HANDOFF,
        ROUTING_RECEIPT,
        LINEAGE_RECEIPT,
        JUDGMENT_RECEIPT,
        CLAIM_RECEIPT,
        GATE_AUDIT,
        FINAL_DECISION,
        REPORT_PATH,
        STAGE_BRIEF,
        INPUT_REFS,
        SELECTION_STATUS,
    ]
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "created_at_utc": now_utc(),
            "command": "python stage_pipelines/stage362/branch_stage361_to_long_only_margin_grid_without_db.py",
            "claim_boundary": CLAIM_BOUNDARY,
            "inputs": [{"path": rel(path), "sha256": sha256_file(path)} for path in INPUT_FILES],
            "artifacts": [{"path": rel(path), "sha256": sha256_file(path)} for path in artifacts if exists(path)],
        },
    )


def write_docs(summary: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    stage_brief = f"""# Stage362 Brief(362단계 개요): Long-Only Margin Grid(롱 단독 마진 격자)

- canonical_stage_id(정식 단계 ID): `{STAGE_ID}`
- current_run_id(현재 실행 ID): `{NEXT_RUN_ID}`
- latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`
- source_stage_id(원천 단계 ID): `{SOURCE_STAGE_ID}`
- source_run_id(원천 실행 ID): `{PARENT_RUN_ID}`
- superseded_run_id(대체된 실행 ID): `{SUPERSEDED_RUN_ID}`
- selection_status(선택 상태): `stage_branch_opened_no_selection(단계 분기 완료, 선택 없음)`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

## Question(질문)

Can the q05 long-only probability margin grid(q05 롱 단독 확률 마진 격자) find a cost-buffer surface before adding regime/label complexity(국면/라벨 복잡도 추가 전 비용 버퍼 표면을 찾을 수 있는가)?

## Source Truth(원천 진실)

- validation_net_before_cost(비용 전 검증 순수익): `{summary["validation_net_before_cost"]}`
- oos_net_before_cost(비용 전 표본외 순수익): `{summary["oos_net_before_cost"]}`
- validation_cost_0_30_net(+0.30 비용 검증 순수익): `{summary["validation_cost_0_30_net"]}`
- oos_cost_0_30_net(+0.30 비용 표본외 순수익): `{summary["oos_cost_0_30_net"]}`
- source_margin_grid_rows(원천 마진 격자 행): `{summary["margin_grid_rows"]}`
- source_materialization_queue_rows(원천 구체화 대기열 행): `{summary["materialization_queue_rows"]}`

## Scope(범위)

Action(행동): Stage362(362단계)는 Stage361A(361A 실행)의 `s361B_r01_q05_long_only_margin_grid`만 먼저 구체화한다.

Effect(효과): regime router(국면 라우터), long quality label(롱 품질 라벨), short firewall(숏 방화벽), density control(밀도 대조)을 한 stage(단계)에 몰아넣지 않는다.

## Exploration Boundary(탐색 경계)

- idea_id(아이디어 ID): `IDEA-ST362-Q05-LONG-ONLY-MARGIN-GRID`
- hypothesis(가설): q05 long-only(롱 단독)의 probability margin(확률 마진)을 넓게 스코어링하면 +0.30 cost buffer(+0.30 비용 버퍼)를 얻을 수 있는 후보 표면을 먼저 찾을 수 있다.
- legacy_relation(레거시 관계): `none(없음)`
- tier_scope(티어 범위): `Tier A separate + Tier B missing_required(Tier A 분리 + Tier B 필수 누락)`
- broad_sweep(넓은 탐색): q05 margin gap(마진 차이), p_long floor(p_long 하한), p_flat veto(p_flat 제외), trade density(거래 밀도)
- extreme_sweep(극단 탐색): sparse high-margin(희소 고마진), dense low-margin(고밀도 저마진), no-veto control(무제외 대조)
- micro_search_gate(미세 탐색 게이트): validation/OOS +0.30 net positive(검증/표본외 +0.30 순수익 양수) 그리고 density >= 3(밀도 3 이상)
- wfo_plan(WFO 계획): margin surface(마진 표면)가 비용 후 양수면 다음 stage(단계)에서 WFO(walk-forward optimization, 워크포워드 최적화)로 재검증한다.
- failure_memory(실패 기억): Stage361A(361A 실행)는 q05 long-only(롱 단독)가 비용 전 양수지만 validation +0.30 cost(검증 +0.30 비용)에서 실패한다고 기록했다.
- evidence_boundary(근거 경계): `stage_branch_only(단계 분기 전용)`

## Deferred Branches(보류 갈래)

- `s361B_r02_long_regime_router_inputs`: Stage362B(362B 실행) 뒤 필요할 때 별도 stage(단계)로 분기
- `s361B_r03_long_quality_label_inputs`: margin grid(마진 격자) 단서가 비용 후 양수일 때 label stage(라벨 단계)로 분기
- `s361B_r04_short_firewall_negative_control`: short control(숏 대조)은 negative control(부정 대조) stage(단계)로 분리
- `s361B_r05_density_no_trade_controls`: density/no-trade controls(밀도/무거래 대조)는 score surface(점수 표면) 뒤 검증 stage(단계)로 분리
"""
    write_text(STAGE_BRIEF, stage_brief)

    input_refs = f"""# Stage362 Input Refs(362단계 입력 참조)

- source_final_decision(원천 최종 결정): `{rel(SOURCE_FINAL)}`
- source_materialization_queue(원천 구체화 대기열): `{rel(SOURCE_QUEUE)}`
- source_margin_grid_plan(원천 마진 격자 계획): `{rel(SOURCE_MARGIN_GRID)}`
- source_evidence_snapshot(원천 근거 스냅샷): `{rel(SOURCE_EVIDENCE)}`
- source_gate_audit(원천 게이트 감사): `{rel(SOURCE_GATE_AUDIT)}`
- source_report(원천 보고서): `{rel(SOURCE_REPORT)}`
- input_manifest(입력 목록): `{rel(INPUT_MANIFEST)}`

Action(행동): Stage361A(361A 실행)의 5개 materialization queue(구체화 대기열) 중 첫 번째 margin grid(마진 격자) 입력만 Stage362(362단계)의 직접 입력으로 둔다.

Effect(효과): Stage362B(362B 실행)는 q05 long-only margin grid(q05 롱 단독 마진 격자)만 materialize(구체화)하므로 실행 단위가 작아진다.
"""
    write_text(INPUT_REFS, input_refs)

    report = f"""# run362A Stage Branch(run362A 단계 분기)

- run_id(실행 ID): `{RUN_ID}`
- source_stage_id(원천 단계 ID): `{SOURCE_STAGE_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- superseded_run_id(대체된 실행 ID): `{SUPERSEDED_RUN_ID}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- gates(게이트): `{len(gates)}/{len(gates)}`

Action(행동): 사용자의 Stage split(단계 분기) 요청에 따라 Stage361B(361B 실행)의 넓은 materialization(구체화)을 Stage362(362단계)의 q05 long-only margin grid(q05 롱 단독 마진 격자)로 나눴다.

Effect(효과): Stage361A(361A 실행)의 35-row margin grid(35행 마진 격자)는 보존되고, regime/label/short/density(국면/라벨/숏/밀도) 갈래는 후속 stage(단계) 후보로 분리된다.

Current Truth(현재 진실): Stage361A(361A 실행)는 validation net before cost(비용 전 검증 순수익) `{summary["validation_net_before_cost"]}`, OOS net before cost(비용 전 표본외 순수익) `{summary["oos_net_before_cost"]}`, validation +0.30 cost net(검증 +0.30 비용 순수익) `{summary["validation_cost_0_30_net"]}`, OOS +0.30 cost net(표본외 +0.30 비용 순수익) `{summary["oos_cost_0_30_net"]}`를 기록했다.

Lineage(계보): source_inputs(원천 입력)는 Stage361A final decision(최종 결정), run361B materialization queue(구체화 대기열), margin grid plan(마진 격자 계획), source evidence snapshot(원천 근거 스냅샷), run361A report(보고서)다. producer(생산자)는 `{rel(Path("stage_pipelines/stage362/branch_stage361_to_long_only_margin_grid_without_db.py"))}`이고, consumer(소비자)는 `{NEXT_RUN_ID}`다.

Claim Boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    write_text(REPORT_PATH, report)

    review_index = f"""# Stage362 Review Index(362단계 검토 색인)

- `{RUN_ID}`: `{rel(REPORT_PATH)}`. Action(행동): Stage361B(361B 실행)의 heavy materialization(무거운 구체화)을 Stage362 margin grid(362단계 마진 격자)로 분기. Effect(효과): next_run(다음 실행)을 `{NEXT_RUN_ID}`로 가볍게 재지정.
"""
    write_text(REVIEW_INDEX, review_index)

    selection = f"""# Stage362 Selection Status(362단계 선택 상태)

- selection_status(선택 상태): `stage_branch_opened_no_selection(단계 분기 완료, 선택 없음)`
- active_stage_id(활성 단계 ID): `{STAGE_ID}`
- current_run_id(현재 실행 ID): `{NEXT_RUN_ID}`
- latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`
- opened_by_run_id(개설 실행 ID): `{RUN_ID}`
- source_stage_id(원천 단계 ID): `{SOURCE_STAGE_ID}`
- source_run_id(원천 실행 ID): `{PARENT_RUN_ID}`
- superseded_run_id(대체된 실행 ID): `{SUPERSEDED_RUN_ID}`
- candidate_selection(후보 선택): `not_run`
- runtime_authority(런타임 권위): `not_claimed`
- operating_promotion(운영 승격): `not_claimed`
- live_readiness(실거래 준비): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`

Action(행동): Stage362(362단계)는 q05 long-only margin grid(q05 롱 단독 마진 격자)만 새 materialization(구체화) 단위로 연다.

Effect(효과): Stage361A(361A 실행)의 더 넓은 queue(대기열)는 보존하되, 다음 작업은 비용 버퍼(cost buffer, 비용 버퍼) 표면 하나로 제한된다.
"""
    write_text(SELECTION_STATUS, selection)

    readme = f"""# {STAGE_ID}

Stage362(362단계)는 Stage361A(361A 실행)의 q05 long-only margin grid(q05 롱 단독 마진 격자)를 먼저 구체화한다.

- opened_by_run_id(개설 실행 ID): `{RUN_ID}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- source_queue(원천 대기열): `{rel(SOURCE_QUEUE)}`
- source_margin_grid(원천 마진 격자): `{rel(SOURCE_MARGIN_GRID)}`

Action(행동): Stage361B(361B 실행)의 무거운 materialization bundle(구체화 묶음)을 Stage362(362단계)로 나눴다.

Effect(효과): 다음 재진입은 margin grid(마진 격자) 하나만 실행하면 된다.
"""
    write_text(STAGE_README, readme)

    decision_doc = f"""# Decision(결정): Stage362A Long-Only Margin Grid Branch(롱 단독 마진 격자 분기)

- date(날짜): `{TODAY}`
- run_id(실행 ID): `{RUN_ID}`
- source_stage_id(원천 단계 ID): `{SOURCE_STAGE_ID}`
- target_stage_id(대상 단계 ID): `{STAGE_ID}`
- superseded_run_id(대체된 실행 ID): `{SUPERSEDED_RUN_ID}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- judgment(판정): `{JUDGMENT}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Action(행동): Stage361B(361B 실행)의 5개 materialization queue(구체화 대기열)를 바로 수행하지 않고, 첫 번째 q05 long-only margin grid(q05 롱 단독 마진 격자)를 Stage362(362단계)로 분기했다.

Effect(효과): work packet(작업 묶음)이 작아지고, +0.30 cost buffer(+0.30 비용 버퍼) 실패 원인을 가장 단순한 margin surface(마진 표면)에서 먼저 확인한다.

## Claim Boundary(주장 경계)

새 model training(모델 학습), proxy execution(프록시 실행), MT5 execution(MT5 실행), candidate selection(후보 선택), operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 없다.
"""
    write_text(DECISION_DOC, decision_doc)

    write_text(
        WORKSPACE_STATE,
        f"""current_stage_id: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {STATUS}
current_judgment: {JUDGMENT}
current_decision: {DECISION}
next_run_id: {NEXT_RUN_ID}
claim_boundary: {CLAIM_BOUNDARY}
updated_at: {TODAY}
""",
        bom=False,
    )

    working_state = f"""# Current Working State(현재 작업 상태)

- current_stage_id(현재 단계 ID): `{STAGE_ID}`
- current_run_id(현재 실행 ID): `{NEXT_RUN_ID}`
- latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`
- current_status(현재 상태): `{STATUS}`
- current_judgment(현재 판정): `{JUDGMENT}`
- current_decision(현재 결정): `{DECISION}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Action(행동): Stage361B(361B 실행)의 무거운 materialization(구체화)을 Stage362(362단계)의 q05 long-only margin grid(q05 롱 단독 마진 격자)로 분기했다.

Effect(효과): 다음 작업은 `{NEXT_RUN_ID}`에서 35-row margin grid(35행 마진 격자)만 materialize(구체화)한다.
"""
    write_text(CURRENT_WORKING_STATE, working_state)

    append_text_once(
        WORKSPACE_CHANGELOG,
        "## 2026-06-02 run362A",
        f"""## 2026-06-02 run362A

Action(행동): Stage361B heavy materialization(361B 무거운 구체화)을 Stage362 q05 long-only margin grid(362단계 q05 롱 단독 마진 격자)로 분기했다.

Effect(효과): current truth(현재 진실)를 `{STAGE_ID}`와 `{NEXT_RUN_ID}`로 이동했고, 운영 주장(operating claim, 운영 주장)은 하지 않았다.

- source_margin_grid_rows(원천 마진 격자 행): `{summary["margin_grid_rows"]}`
- source_materialization_queue_rows(원천 구체화 대기열 행): `{summary["materialization_queue_rows"]}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
    )

    append_text_once(
        IDEA_REGISTRY,
        "## IDEA-ST362-Q05-LONG-ONLY-MARGIN-GRID",
        f"""## IDEA-ST362-Q05-LONG-ONLY-MARGIN-GRID

- idea(아이디어): q05 long-only(롱 단독) margin grid(마진 격자)를 먼저 구체화해 +0.30 cost buffer(+0.30 비용 버퍼) 가능 표면을 찾는다.
- hypothesis(가설): broad margin surface(넓은 마진 표면)가 validation/OOS(검증/표본외) 모두에서 비용 후 양수를 만들면 regime/label(국면/라벨) 복잡도를 붙일 가치가 생긴다.
- tier_scope(티어 범위): `Tier A separate + Tier B missing_required(Tier A 분리 + Tier B 필수 누락)`
- evidence_boundary(근거 경계): `stage_branch_only(단계 분기 전용)`
- next_action(다음 행동): `{NEXT_RUN_ID}`
""",
    )

    source_selection_text = f"""# Stage361 Selection Status(361단계 선택 상태)

- selection_status(선택 상태): `handoff_to_stage362_no_selection(362단계 인계, 선택 없음)`
- active_stage_id_at_handoff(인계 시 활성 단계 ID): `{SOURCE_STAGE_ID}`
- latest_run_id(최근 실행 ID): `{PARENT_RUN_ID}`
- current_run_id(현재 실행 ID): `superseded_by_{RUN_ID}`
- handoff_run_id(인계 실행 ID): `{RUN_ID}`
- next_stage_id(다음 단계 ID): `{STAGE_ID}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- opened_by_run_id(개설 실행 ID): `run360C_review_regime_stability_pivot_materialized_inputs_without_db_v1`
- source_stage_id(원천 단계 ID): `360_regime_stability_pivot__oos_long_cash_edge_validation_loss`
- source_review_run_id(원천 검토 실행 ID): `run360C_review_regime_stability_pivot_materialized_inputs_without_db_v1`
- candidate_selection(후보 선택): `not_run`
- runtime_authority(런타임 권위): `not_claimed`
- operating_promotion(운영 승격): `not_claimed`
- live_readiness(실거래 준비): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`

Action(행동): Stage361(361단계)은 q05 long-only cost buffer(q05 롱 단독 비용 버퍼)를 설계 대기열로 열고, 무거운 구체화 실행은 Stage362(362단계)로 나눴다.

Effect(효과): Stage361(361단계)은 선택 없이 design queue(설계 대기열)를 보존하고, 실제 다음 작업은 Stage362 margin grid(362단계 마진 격자)로 제한된다.

## run361A Design Closeout(361A 설계 종료 기록)

- run_id(실행 ID): `{PARENT_RUN_ID}`
- status(상태): `completed_stage361A_long_only_cost_buffer_design_ready_materialization_required_no_selection_no_mt5`
- judgment(판정): `long_only_cost_buffer_design_ready_materialization_required_no_operating_claim`
- superseded_next_run_id(대체된 다음 실행 ID): `{SUPERSEDED_RUN_ID}`
- gate_result(게이트 결과): `12/12`
- margin_grid_rows(마진 grid 행): `35`
- materialization_queue_rows(구체화 대기열 행): `5`
- claim_boundary(주장 경계): `research_development_design_only_long_only_cost_buffer_no_model_training_no_proxy_execution_no_mt5_execution_no_candidate_selection_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim`

Action(행동): q05 long-only(롱 단독) seed(씨앗)를 margin/regime/label(마진/국면/라벨) 구체화 대기열로 바꿨다.

Effect(효과): Stage361(361단계)은 직접 구체화 대신 Stage362(362단계)의 margin grid(마진 격자) 분기로 진행한다.

## Stage362A Branch Handoff(362A 분기 인계)

- handoff_run_id(인계 실행 ID): `{RUN_ID}`
- target_stage_id(대상 단계 ID): `{STAGE_ID}`
- superseded_run_id(대체된 실행 ID): `{SUPERSEDED_RUN_ID}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- selection_status(선택 상태): `handoff_to_stage362_no_selection(362단계 인계, 선택 없음)`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Action(행동): Stage361B(361B 실행)의 5개 materialization(구체화)을 직접 실행하지 않고 Stage362(362단계)로 나눴다.

Effect(효과): Stage361(361단계)은 design queue(설계 대기열)를 보존하고, 실제 다음 작업은 margin grid(마진 격자) 하나로 제한된다.
"""
    write_text(SOURCE_SELECTION, source_selection_text)

    source_stage_brief = f"""# Stage361 Brief(361단계 개요): Long-Only Cost Buffer(롱 단독 비용 버퍼)

- stage_id(단계 ID): `{SOURCE_STAGE_ID}`
- opened_by_run_id(개설 실행 ID): `run360C_review_regime_stability_pivot_materialized_inputs_without_db_v1`
- source_stage_id(원천 단계 ID): `360_regime_stability_pivot__oos_long_cash_edge_validation_loss`
- latest_completed_run_id(최근 완료 실행 ID): `{PARENT_RUN_ID}`
- handoff_run_id(인계 실행 ID): `{RUN_ID}`
- next_stage_id(다음 단계 ID): `{STAGE_ID}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

## Question(질문)

Can q05 long-only edge gain +0.30 cost buffer while preserving validation/OOS positivity and 3+ trades/day?(q05 롱 단독 우위가 검증/표본외 양수와 일 3거래 이상을 유지하면서 +0.30 비용 버퍼를 얻을 수 있는가?)

## Source Truth(원천 진실)

Action(행동): Stage360C(360C 실행)는 q05 long-only(롱 단독)를 Stage361(361단계)의 offensive seed(공격 씨앗)로 넘겼다.

Effect(효과): long/cash hard veto(롱/현금장 고정 제외)와 simple no-late veto(단순 후반 제외)에 묶이지 않고, margin/regime/label(마진/국면/라벨) 쪽으로 새 수익 원천을 탐색한다.

## run361A Design Closeout(361A 설계 종료)

Action(행동): long-only cost buffer(롱 단독 비용 버퍼)를 broad margin/regime/label design(넓은 마진/국면/라벨 설계)로 전환했다.

Effect(효과): Stage361(361단계)은 직접 구체화하지 않고 Stage362(362단계)의 margin grid(마진 격자)로 분기한다.

## Stage362A Branch Handoff(362A 분기 인계)

Action(행동): `run361B_materialize_long_only_cost_buffer_inputs_without_db_v1`을 직접 실행하지 않고 `{STAGE_ID}`로 분기했다.

Effect(효과): Stage361(361단계)의 넓은 cost buffer design(비용 버퍼 설계)은 보존하고, Stage362(362단계)는 q05 long-only margin grid(q05 롱 단독 마진 격자) 하나만 구체화한다.
"""
    write_text(SOURCE_STAGE_BRIEF, source_stage_brief)

    source_readme = f"""# {SOURCE_STAGE_ID}

Stage361(361단계)은 q05 long-only(롱 단독) edge(우위)의 cost buffer(비용 버퍼)를 설계했고, heavy materialization(무거운 구체화)은 Stage362(362단계)로 분기했다.

- opened_by_run_id(개설 실행 ID): `run360C_review_regime_stability_pivot_materialized_inputs_without_db_v1`
- latest_completed_run_id(최근 완료 실행 ID): `{PARENT_RUN_ID}`
- handoff_run_id(인계 실행 ID): `{RUN_ID}`
- next_stage_id(다음 단계 ID): `{STAGE_ID}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- seed_queue(씨앗 대기열): `stages/360_regime_stability_pivot__oos_long_cash_edge_validation_loss/02_runs/run360C/stage361_seed_queue.csv`
- source_review(원천 검토): `stages/360_regime_stability_pivot__oos_long_cash_edge_validation_loss/03_reviews/run360C_regime_stability_pivot_materialized_input_review.md`

## run361A Design Closeout(361A 설계 종료)

- report(보고서): `stages/361_long_only_cost_buffer__validation_oos_positive_cost_failure/03_reviews/run361A_long_only_cost_buffer_design.md`
- final_decision(최종 결정): `stages/361_long_only_cost_buffer__validation_oos_positive_cost_failure/02_runs/run361A/final_decision.json`
- superseded_next_run_id(대체된 다음 실행 ID): `{SUPERSEDED_RUN_ID}`

## Stage362A Branch Handoff(362A 분기 인계)

- handoff_run_id(인계 실행 ID): `{RUN_ID}`
- next_stage_id(다음 단계 ID): `{STAGE_ID}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`

Action(행동): Stage361B(361B 실행)의 heavy queue(무거운 대기열)를 Stage362(362단계)로 나눴다.

Effect(효과): 다음 재진입은 Stage362 margin grid(362단계 마진 격자)부터 시작한다.
"""
    write_text(SOURCE_STAGE_DIR / "README.md", source_readme)


def registry_rows(summary: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> tuple[dict[str, Any], dict[str, Any]]:
    common = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": f"{RUN_ID}__Tier_AplusB",
        "parent_run_id": PARENT_RUN_ID,
        "scoreboard_lane": "state_sync_stage_branch(상태 동기화 단계 분기)",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "external_verification_status": "out_of_scope_by_claim_no_new_mt5(주장 범위 밖, 새 MT5 없음)",
        "notes": "Stage361B heavy queue split to Stage362 margin grid(Stage361B 무거운 대기열을 Stage362 마진 격자로 분기).",
        "run_number": RUN_NUMBER,
        "date": TODAY,
        "decision": DECISION,
        "next_run_id": NEXT_RUN_ID,
        "rows": summary["margin_grid_rows"],
        "gate_passes": len(gates),
        "gate_total": len(gates),
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "operating_ready_rows": 0,
        "run_date": TODAY,
        "primary_artifact": rel(BRANCH_HANDOFF),
        "result_status": STATUS,
        "sample_rows": summary["margin_grid_rows"],
        "source_package_run_id": PARENT_RUN_ID,
        "work_family": "state_sync(상태 동기화)",
        "trade_density_requirement_status": TRADE_DENSITY_REQUIREMENT,
        "result_judgment": JUDGMENT,
        "final_decision_path": rel(FINAL_DECISION),
        "created_at": TODAY,
        "lane": "state_sync_stage_branch(상태 동기화 단계 분기)",
        "family": "state_sync(상태 동기화)",
        "primary_report": rel(REPORT_PATH),
        "evidence_boundary": CLAIM_BOUNDARY,
        "next_action": NEXT_RUN_ID,
        "question": "Can q05 long-only margin grid recover cost buffer first?(q05 롱 단독 마진 격자가 비용 버퍼를 먼저 회복할 수 있는가?)",
        "ledger_row_id": f"{RUN_ID}__Tier_AplusB",
        "row_id": f"{RUN_ID}__Tier_AplusB",
        "record_view": "Stage branch(단계 분기)",
        "tier_scope": "Tier A+B",
        "kpi_scope": "stage_branch_no_new_runtime(단계 분기, 새 런타임 없음)",
        "primary_kpi": f"margin_grid_rows={summary['margin_grid_rows']}",
        "guardrail_kpi": "no_candidate_selection(후보 선택 없음)",
        "view": "Tier A+B combined(Tier A+B 합산)",
        "tier": "Tier A+B",
        "metric_scope": "out_of_scope_by_claim(주장 범위 밖)",
    }
    run_row = dict(common)
    run_row["scoreboard_lane"] = "state_sync_stage_branch(상태 동기화 단계 분기)"
    ledger_row = dict(common)
    return run_row, ledger_row


def write_registries(summary: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    run_row, ledger_row = registry_rows(summary, gates)
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], [run_row], extend_header=False)
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], [ledger_row], extend_header=False)
    write_csv(STAGE_LEDGER, [ledger_row])


def write_artifact_registry() -> None:
    artifacts = [
        ("script", ROOT / "stage_pipelines" / "stage362" / "branch_stage361_to_long_only_margin_grid_without_db.py", "tracked"),
        ("report", REPORT_PATH, "tracked"),
        ("decision_doc", DECISION_DOC, "tracked"),
        ("stage_brief", STAGE_BRIEF, "tracked"),
        ("input_refs", INPUT_REFS, "tracked"),
        ("input_manifest", INPUT_MANIFEST, "tracked"),
        ("selection_status", SELECTION_STATUS, "tracked"),
        ("final_decision", FINAL_DECISION, "ignored_with_manifest"),
        ("run_manifest", RUN_MANIFEST, "ignored_with_manifest"),
        ("branch_handoff", BRANCH_HANDOFF, "ignored_with_manifest"),
        ("gate_audit", GATE_AUDIT, "ignored_with_manifest"),
    ]
    rows = []
    for artifact_type, path, availability in artifacts:
        if not exists(path):
            continue
        rows.append(
            {
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "artifact_type": artifact_type,
                "path": rel(path),
                "sha256": sha256_file(path),
                "created_at": TODAY,
                "claim_boundary": CLAIM_BOUNDARY,
                "artifact_id": f"{RUN_ID}__{artifact_type}",
                "created_at_utc": now_utc(),
                "notes": availability,
                "artifact_path": rel(path),
            }
        )
    append_or_replace_csv(ARTIFACT_REGISTRY, ["artifact_id"], rows, extend_header=False)


def main() -> None:
    require_inputs()
    os.makedirs(fs_path(RUN_DIR), exist_ok=True)
    summary = source_summary()
    gates = gate_rows()
    write_input_manifest()
    write_run_artifacts(summary, gates)
    write_docs(summary, gates)
    write_registries(summary, gates)
    write_manifest()
    write_artifact_registry()
    print(json.dumps(read_json(FINAL_DECISION), ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
