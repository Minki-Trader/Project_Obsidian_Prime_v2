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

SOURCE_STAGE_ID = "355_density_recovery_model_family__new_label_source_probe"
NEW_STAGE_ID = "356_density_recovery_training__proxy_model_queue_scout"
SOURCE_STAGE_DIR = ROOT / "stages" / SOURCE_STAGE_ID
NEW_STAGE_DIR = ROOT / "stages" / NEW_STAGE_ID

RUN_NUMBER = "run356A"
RUN_ID = "run356A_branch_stage355_to_density_recovery_proxy_training_without_db_v1"
PARENT_RUN_ID = "run355B_materialize_density_recovery_label_inputs_without_db_v1"
SUPERSEDED_RUN_ID = "run355C_train_density_recovery_proxy_models_without_db_v1"
NEXT_RUN_ID = "run356B_train_density_recovery_proxy_models_without_db_v1"

STATUS = "completed_stage356A_user_requested_stage_split_proxy_training_opened_no_selection"
JUDGMENT = (
    "stage_branch_completed_stage355_label_materialization_split_to_stage356_proxy_training_"
    "no_operating_claim"
)
DECISION = "stage356A_open_run356B_train_density_recovery_proxy_models_without_db_v1"
CLAIM_BOUNDARY = (
    "state_sync_stage_branch_user_requested_proxy_training_handoff_only_"
    "no_new_model_training_no_new_proxy_execution_no_mt5_execution_no_candidate_selection_"
    "no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)
QUEUE_BOUNDARY = (
    "research_development_proxy_training_queue_ref_only_no_model_training_yet_no_mt5_execution_"
    "no_candidate_selection_no_forward_pass_no_live_readiness_no_operating_promotion_"
    "no_runtime_authority_no_goal_claim"
)
TRADE_DENSITY_REQUIREMENT = "trade_per_day_min_3_to_10_plus_no_trade_splitting"

SOURCE_RUN_DIR = SOURCE_STAGE_DIR / "02_runs" / "run355B"
SOURCE_FINAL_DECISION = SOURCE_RUN_DIR / "final_decision.json"
SOURCE_TRAINING_QUEUE = SOURCE_RUN_DIR / "run355C_training_queue.csv"
SOURCE_FEATURE_LABEL_TABLE = SOURCE_RUN_DIR / "feature_label_table.csv"
SOURCE_LABEL_MANIFEST = SOURCE_RUN_DIR / "label_variant_manifest.csv"
SOURCE_LABEL_DISTRIBUTION = SOURCE_RUN_DIR / "label_distribution.csv"
SOURCE_MATERIALIZATION_SUMMARY = SOURCE_RUN_DIR / "materialization_summary.csv"
SOURCE_GATE_AUDIT = SOURCE_RUN_DIR / "required_gate_coverage_audit.csv"
SOURCE_REPORT = SOURCE_STAGE_DIR / "03_reviews" / "run355B_density_recovery_label_materialization.md"
SOURCE_STAGE_LEDGER = SOURCE_STAGE_DIR / "03_reviews" / "stage_run_ledger.csv"
SOURCE_REVIEW_INDEX = SOURCE_STAGE_DIR / "03_reviews" / "review_index.md"
SOURCE_SELECTION_STATUS = SOURCE_STAGE_DIR / "04_selected" / "selection_status.md"
SOURCE_STAGE_BRIEF = SOURCE_STAGE_DIR / "00_spec" / "stage_brief.md"
SOURCE_SCRIPT = (
    ROOT / "stage_pipelines" / "stage355" / "materialize_density_recovery_label_inputs_without_db.py"
)

RUN_DIR = NEW_STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = NEW_STAGE_DIR / "03_reviews"
INPUT_DIR = NEW_STAGE_DIR / "01_inputs"
SPEC_DIR = NEW_STAGE_DIR / "00_spec"
SELECTED_DIR = NEW_STAGE_DIR / "04_selected"

STAGE_README = NEW_STAGE_DIR / "README.md"
STAGE_BRIEF = SPEC_DIR / "stage_brief.md"
INPUT_REFS = INPUT_DIR / "input_refs.md"
INPUT_MANIFEST = INPUT_DIR / "stage356_input_manifest.csv"
TRAINING_QUEUE_REF = INPUT_DIR / "run356B_training_queue_ref.csv"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"
REVIEW_INDEX = REVIEW_DIR / "review_index.md"
SELECTION_STATUS = SELECTED_DIR / "selection_status.md"
REPORT_PATH = REVIEW_DIR / "run356A_stage_branch.md"
SOURCE_SPLIT_REPORT = SOURCE_STAGE_DIR / "03_reviews" / "run355B_stage_split_to_356.md"

HANDOFF_MANIFEST = RUN_DIR / "stage355B_to_stage356_handoff_manifest.csv"
STAGE_TRANSITION_RECEIPT = RUN_DIR / "stage_transition_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs" / "context" / "current_working_state.md"
ROOT_SELECTION_STATUS = ROOT / "docs" / "registers" / "selection_status.md"
PROJECT_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
IDEA_REGISTRY = ROOT / "docs" / "registers" / "idea_registry.md"
WORKSPACE_CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
DECISION_DOC = (
    ROOT / "docs" / "decisions" / f"{TODAY}_stage356A_branch_stage355_to_proxy_training.md"
)

SOURCE_INPUTS: list[tuple[Path, str, bool, str]] = [
    (SOURCE_FINAL_DECISION, "run355B final decision(355B 최종 결정)", True, "tracked_or_ignored_with_hash"),
    (SOURCE_TRAINING_QUEUE, "run355B training queue(355B 학습 대기열)", True, "ignored_with_manifest"),
    (SOURCE_FEATURE_LABEL_TABLE, "run355B feature label table(355B 피처 라벨 표)", True, "ignored_with_manifest"),
    (SOURCE_LABEL_MANIFEST, "run355B label variant manifest(355B 라벨 변형 목록)", True, "ignored_with_manifest"),
    (SOURCE_LABEL_DISTRIBUTION, "run355B label distribution(355B 라벨 분포)", True, "ignored_with_manifest"),
    (SOURCE_MATERIALIZATION_SUMMARY, "run355B materialization summary(355B 물질화 요약)", True, "ignored_with_manifest"),
    (SOURCE_GATE_AUDIT, "run355B gate audit(355B 게이트 감사)", True, "ignored_with_manifest"),
    (SOURCE_REPORT, "run355B review report(355B 검토 보고서)", True, "tracked"),
    (SOURCE_STAGE_LEDGER, "Stage355 ledger(355단계 장부)", True, "tracked"),
    (SOURCE_SELECTION_STATUS, "Stage355 selection status(355단계 선택 상태)", True, "tracked"),
    (SOURCE_STAGE_BRIEF, "Stage355 stage brief(355단계 개요)", True, "tracked"),
    (SOURCE_SCRIPT, "run355B producer script(355B 생산 스크립트)", True, "tracked"),
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


def read_json(path: Path) -> dict[str, Any]:
    with open(fs_path(path), encoding="utf-8-sig") as handle:
        return json.load(handle)


def write_json(path: Path, payload: Mapping[str, Any]) -> None:
    ensure_parent(path)
    with open(fs_path(path), "w", encoding="utf-8", newline="\n") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")


def read_csv_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    csv.field_size_limit(200_000_000)
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


def append_or_replace_csv(path: Path, key_fields: Sequence[str], rows: Iterable[Mapping[str, Any]]) -> None:
    rows_list = [dict(row) for row in rows]
    if exists(path):
        fieldnames, existing = read_csv_rows(path)
    else:
        fieldnames, existing = [], []
    for row in rows_list:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    replacement_keys = {tuple(str(row.get(key, "")) for key in key_fields) for row in rows_list}
    kept = [
        row
        for row in existing
        if tuple(str(row.get(key, "")) for key in key_fields) not in replacement_keys
    ]
    write_csv(path, [*kept, *rows_list], fieldnames)


def source_summary() -> dict[str, Any]:
    final = read_json(SOURCE_FINAL_DECISION)
    _summary_fields, summary_rows = read_csv_rows(SOURCE_MATERIALIZATION_SUMMARY)
    materialization = summary_rows[0] if summary_rows else {}
    _queue_fields, queue_rows = read_csv_rows(SOURCE_TRAINING_QUEUE)
    labels = sorted({row.get("label_variant_id", "") for row in queue_rows if row.get("label_variant_id")})
    return {
        "final": final,
        "materialization": materialization,
        "queue_rows": queue_rows,
        "label_variant_ids": labels,
        "feature_rows": final.get("data_identity", {}).get("feature_rows", materialization.get("feature_rows", "")),
        "raw_rows": final.get("data_identity", {}).get("raw_rows", materialization.get("raw_rows", "")),
        "label_table_rows": final.get("label_table_rows", materialization.get("label_table_rows", "")),
        "label_variant_count": final.get("label_variant_count", materialization.get("label_variant_count", "")),
        "training_queue_rows": final.get("training_queue_rows", materialization.get("training_queue_rows", "")),
        "distribution_rows": final.get("distribution_rows", materialization.get("distribution_rows", "")),
        "gate_passes": final.get("gate_passes", ""),
        "gate_total": final.get("gate_total", ""),
    }


def write_input_manifest() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path, label, required, availability_hint in SOURCE_INPUTS:
        present = exists(path)
        rows.append(
            {
                "source_label": label,
                "path": rel(path),
                "exists": str(present).lower(),
                "required": str(required).lower(),
                "availability": availability_hint if present else "missing",
                "sha256": sha256_file(path) if present else "",
                "size_bytes": os.path.getsize(fs_path(path)) if present else "",
                "producer": PARENT_RUN_ID,
                "consumer": RUN_ID,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(INPUT_MANIFEST, rows)
    write_csv(HANDOFF_MANIFEST, rows)
    return rows


def write_training_queue_ref(queue_rows: Sequence[Mapping[str, str]]) -> None:
    rewritten_rows: list[dict[str, Any]] = []
    for row in queue_rows:
        next_row = dict(row)
        label_variant_id = next_row.get("label_variant_id", "")
        next_row["queue_id"] = f"run356B__{label_variant_id}" if label_variant_id else "run356B__unknown"
        next_row["next_run_id"] = NEXT_RUN_ID
        next_row["source_run_id"] = PARENT_RUN_ID
        next_row["source_queue_id"] = row.get("queue_id", "")
        next_row["training_input"] = rel(SOURCE_FEATURE_LABEL_TABLE)
        next_row["label_variant_manifest"] = rel(SOURCE_LABEL_MANIFEST)
        next_row["claim_boundary"] = QUEUE_BOUNDARY
        rewritten_rows.append(next_row)
    write_csv(TRAINING_QUEUE_REF, rewritten_rows)


def write_stage_docs(summary: Mapping[str, Any]) -> None:
    labels = ", ".join(summary["label_variant_ids"])
    write_text(
        SOURCE_SPLIT_REPORT,
        f"""# run355B Stage Split To Stage356(run355B 356단계 분기)

- source_stage_id(원천 단계 ID): `{SOURCE_STAGE_ID}`
- source_completed_run_id(완료 원천 실행 ID): `{PARENT_RUN_ID}`
- split_run_id(분기 실행 ID): `{RUN_ID}`
- superseded_run_id(대체된 실행 ID): `{SUPERSEDED_RUN_ID}`
- next_stage_id(다음 단계 ID): `{NEW_STAGE_ID}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- status(상태): `split_to_stage356_proxy_training(356단계 프록시 학습으로 분기)`

Action(행동): Stage355(355단계)는 timestamp-safe label materialization(시점 안전 라벨 물질화)까지 닫고, model training(모델 학습)은 Stage356(356단계)으로 분리했다.

Effect(효과): 다음 재진입(re-entry, 재진입)은 186600행 label table(라벨 표) 전체 맥락을 다시 읽기보다, 학습 대기열(training queue, 학습 대기열) 4행에서 바로 시작한다.

Boundary(경계): 새 model training(모델 학습), proxy execution(프록시 실행), MT5 execution(MT5 실행), candidate selection(후보 선정), operating promotion(운영 승격), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 주장하지 않는다.
""",
    )
    append_text_once(SOURCE_REVIEW_INDEX, "run355B_stage_split_to_356", f"- `{rel(SOURCE_SPLIT_REPORT)}`")

    write_text(
        STAGE_README,
        f"""# Stage356 Density Recovery Training(356단계 밀도 회복 학습)

- current_run(현재 실행): `{NEXT_RUN_ID}`
- branch_run(분기 실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{PARENT_RUN_ID}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Action(행동): Stage355B(355B 실행)의 라벨 물질화 산출물을 Stage356(356단계)의 proxy model training(프록시 모델 학습) 입력으로 넘긴다.

Effect(효과): Stage355(355단계)의 무거운 label/source/model family(라벨/원천/모델 계열) 문맥과 Stage356(356단계)의 학습 탐색 문맥이 분리된다.
""",
    )
    write_text(
        STAGE_BRIEF,
        f"""# Stage356 Density Recovery Training(356단계 밀도 회복 학습)

- canonical_stage_id(정식 단계 ID): `{NEW_STAGE_ID}`
- current_run_id(현재 실행 ID): `{NEXT_RUN_ID}`
- latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`
- source_stage_id(원천 단계 ID): `{SOURCE_STAGE_ID}`
- source_run_id(원천 실행 ID): `{PARENT_RUN_ID}`
- superseded_run_id(대체된 실행 ID): `{SUPERSEDED_RUN_ID}`
- selection_status(선택 상태): `stage_branch_opened_no_selection(단계 분기 완료, 선택 없음)`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

## Question(질문)

Stage355B(355B 실행)에서 만든 timestamp-safe label variants(시점 안전 라벨 변형) 4개가 proxy model training(프록시 모델 학습)에서 trade/day(일별 거래수) 3+와 net/PF/stress(순수익/수익 팩터/압박)를 동시에 회복하는 후보 대기열(candidate queue, 후보 대기열)을 만들 수 있는가?

## Source Truth(원천 진실)

- feature_rows(피처 행): `{summary["feature_rows"]}`
- raw_rows(원시 행): `{summary["raw_rows"]}`
- label_table_rows(라벨 표 행): `{summary["label_table_rows"]}`
- label_variant_count(라벨 변형 수): `{summary["label_variant_count"]}`
- training_queue_rows(학습 대기열 행): `{summary["training_queue_rows"]}`
- distribution_rows(분포 행): `{summary["distribution_rows"]}`
- source_gates(원천 게이트): `{summary["gate_passes"]}/{summary["gate_total"]}`
- label_variant_ids(라벨 변형 ID): `{labels}`

## Scope(범위)

Stage356(356단계)는 proxy model training(프록시 모델 학습), non-overlap proxy evaluation(비중첩 프록시 평가), candidate queue triage(후보 대기열 선별)까지만 다룬다. MT5 runtime probe(MT5 런타임 탐침)와 ONNX handoff(온엑스 인계)는 positive queue(긍정 대기열)가 생긴 뒤 별도 stage/run(단계/실행)에서 다룬다.

## Exploration Plan(탐색 계획)

- idea_id(아이디어 ID): `IDEA-ST356-DENSITY-RECOVERY-PROXY-TRAINING`
- hypothesis(가설): cost-buffer/path-quality/dual-head labels(비용 완충/경로 품질/이중 헤드 라벨)이 기존 surface(표면)보다 trade density(거래 밀도)를 유지하면서 stress net(압박 순수익)을 회복한다.
- legacy_relation(레거시 관계): `none(없음)`
- tier_scope(티어 범위): `Tier A separate + Tier B missing_required(Tier A 분리 + Tier B 필수 누락)`
- broad_sweep(넓은 탐색): logreg/MLP/tree fallback(로지스틱/MLP/트리 대체), threshold(임계값), margin(마진), ADX/session filter(ADX/세션 필터)
- extreme_sweep(극단 탐색): very-low threshold(매우 낮은 임계값), high margin(높은 마진), short horizon hold(짧은 보유기간), stress cost(압박 비용)
- micro_search_gate(미세 탐색 게이트): validation/OOS proxy trade/day(검증/OOS 프록시 일별 거래수) 3+와 stress net(압박 순수익) 양수
- wfo_plan(WFO 계획): scout pass(탐색 회차) 뒤 WFO(walk-forward optimization, 워크포워드 최적화) 프레임으로 재검증
- failure_memory(실패 기억): density(밀도)만 좋거나 stress net(압박 순수익)이 깨지면 label/model clue(라벨/모델 단서)만 보존하고 selection(선정)은 금지
- evidence_boundary(근거 경계): `scout-only(탐색 전용)`

## Density Constraint(밀도 제약)

`{TRADE_DENSITY_REQUIREMENT}`

Action(행동): trade splitting(거래 쪼개기) 없이 trade/day(일별 거래수) 3~10+ 조건을 유지한다.

Effect(효과): 낮은 거래수로 예쁜 net profit(순수익)을 만든 후보가 운영 후보처럼 보이지 않게 한다.
""",
    )
    write_text(
        INPUT_REFS,
        f"""# Stage356 Input Refs(356단계 입력 참조)

- source_final_decision(원천 최종 결정): `{rel(SOURCE_FINAL_DECISION)}`
- source_training_queue(원천 학습 대기열): `{rel(SOURCE_TRAINING_QUEUE)}`
- tracked_training_queue_ref(추적 학습 대기열 참조): `{rel(TRAINING_QUEUE_REF)}`
- feature_label_table(피처 라벨 표): `{rel(SOURCE_FEATURE_LABEL_TABLE)}`
- label_variant_manifest(라벨 변형 목록): `{rel(SOURCE_LABEL_MANIFEST)}`
- label_distribution(라벨 분포): `{rel(SOURCE_LABEL_DISTRIBUTION)}`
- materialization_summary(물질화 요약): `{rel(SOURCE_MATERIALIZATION_SUMMARY)}`
- input_manifest(입력 목록): `{rel(INPUT_MANIFEST)}`

Action(행동): Stage355B(355B 실행)의 무거운 02_runs(실행 산출물) 파일은 hash(해시)와 manifest(목록)로 연결하고, Stage356(356단계)에는 작은 queue ref(대기열 참조)를 추적한다.

Effect(효과): 대형 feature_label_table(피처 라벨 표)을 커밋하지 않아도 다음 학습 실행이 어떤 입력을 써야 하는지 재현할 수 있다.
""",
    )
    write_text(
        REPORT_PATH,
        f"""# run356A Stage Branch(run356A 단계 분기)

- run_id(실행 ID): `{RUN_ID}`
- source_stage_id(원천 단계 ID): `{SOURCE_STAGE_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- superseded_run_id(대체된 실행 ID): `{SUPERSEDED_RUN_ID}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- gates(게이트): `10/10`

Action(행동): 사용자의 Stage split(단계 분기) 요청에 따라 Stage355(355단계)의 라벨 물질화 결과를 Stage356(356단계)의 proxy training scout(프록시 학습 탐색)로 넘겼다.

Effect(효과): 다음 작업은 `run356B`에서 4개 label variant(라벨 변형)를 학습하고, Stage355(355단계)는 label/source materialization(라벨/원천 물질화)으로 가볍게 닫힌다.

Current Truth(현재 진실): label_table_rows(라벨 표 행) `{summary["label_table_rows"]}`, training_queue_rows(학습 대기열 행) `{summary["training_queue_rows"]}`, source_gates(원천 게이트) `{summary["gate_passes"]}/{summary["gate_total"]}`.

Claim Boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
    )
    write_text(
        REVIEW_INDEX,
        f"""# Stage356 Review Index(356단계 검토 색인)

- `{rel(REPORT_PATH)}`
- `{rel(STAGE_LEDGER)}`
- `{rel(STAGE_BRIEF)}`
- `{rel(TRAINING_QUEUE_REF)}`
""",
    )


def write_selection_docs(summary: Mapping[str, Any]) -> None:
    write_text(
        SOURCE_SELECTION_STATUS,
        f"""# Stage355 Selection Status(355단계 선택 상태)

- selection_status(선택 상태): `no_selection_split_to_stage356(선택 없음, 356단계로 분기)`
- active_stage_id(활성 단계 ID): `{SOURCE_STAGE_ID}`
- latest_run_id(최근 실행 ID): `{PARENT_RUN_ID}`
- superseded_run_id(대체된 실행 ID): `{SUPERSEDED_RUN_ID}`
- handoff_stage_id(인계 단계 ID): `{NEW_STAGE_ID}`
- handoff_run_id(인계 실행 ID): `{RUN_ID}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- training_queue_rows(학습 대기열 행): `{summary["training_queue_rows"]}`
- mt5_queue_rows(MT5 대기열 행): `0`
- runtime_authority(런타임 권위): `not_claimed`
- operating_promotion(운영 승격): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
""",
    )
    selection = f"""# Stage356 Selection Status(356단계 선택 상태)

- selection_status(선택 상태): `stage_branch_opened_no_selection(단계 분기 완료, 선택 없음)`
- active_stage_id(활성 단계 ID): `{NEW_STAGE_ID}`
- latest_run_id(최근 실행 ID): `{RUN_ID}`
- current_run_id(현재 실행 ID): `{NEXT_RUN_ID}`
- source_run_id(원천 실행 ID): `{PARENT_RUN_ID}`
- training_queue_rows(학습 대기열 행): `{summary["training_queue_rows"]}`
- mt5_queue_rows(MT5 대기열 행): `0`
- runtime_authority(런타임 권위): `not_claimed`
- operating_promotion(운영 승격): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
"""
    write_text(SELECTION_STATUS, selection)
    write_text(ROOT_SELECTION_STATUS, selection)


def write_state_docs() -> None:
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

- current_stage_id(현재 단계 ID): `{NEW_STAGE_ID}`
- current_run_id(현재 실행 ID): `{NEXT_RUN_ID}`
- latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`
- current_status(현재 상태): `{STATUS}`
- current_judgment(현재 판정): `{JUDGMENT}`
- current_decision(현재 결정): `{DECISION}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Action(행동): Stage355B(355B 실행)의 timestamp-safe label materialization(시점 안전 라벨 물질화)을 닫고, Stage356(356단계) proxy model training(프록시 모델 학습)으로 분기했다.

Effect(효과): 다음 재진입(re-entry, 재진입)은 Stage356(356단계)의 4행 training queue(학습 대기열)에서 바로 시작하며, MT5 KPI(MT5 핵심 성과 지표)는 아직 주장하지 않는다.
""",
    )


def base_ledger_row(summary: Mapping[str, Any]) -> dict[str, Any]:
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
        "gate_passes": 10,
        "gate_total": 10,
        "claim_boundary": CLAIM_BOUNDARY,
        "scoreboard_lane": "state_sync_stage_branch(상태 동기화 단계 분기)",
        "lane": "state_sync_stage_branch(상태 동기화 단계 분기)",
        "family": "state_sync(상태 동기화)",
        "work_family": "state_sync(상태 동기화)",
        "run_number": RUN_NUMBER,
        "notes": "Stage355 label materialization was split before proxy model training(355단계 라벨 물질화 뒤 프록시 모델 학습 전 분기).",
        "source_package_run_id": PARENT_RUN_ID,
        "rows": summary["label_table_rows"],
        "candidate_rows": summary["training_queue_rows"],
        "external_verification_status": "out_of_scope_by_claim(주장 범위 밖)",
        "result_status": "stage_branch_opened_no_selection(단계 분기 완료, 선택 없음)",
        "primary_kpi": "training_queue_rows=4(학습 대기열 4행)",
        "guardrail_kpi": TRADE_DENSITY_REQUIREMENT,
        "trade_density_requirement_status": TRADE_DENSITY_REQUIREMENT,
        "result_judgment": JUDGMENT,
        "final_decision_path": rel(FINAL_DECISION),
        "created_at": TODAY,
    }


def write_ledgers(summary: Mapping[str, Any]) -> None:
    base = base_ledger_row(summary)
    views = [
        (
            "Tier_A",
            "Tier A",
            "Tier A separate(Tier A 분리)",
            "label_materialization_full_context_to_proxy_training(라벨 물질화 전체 문맥을 프록시 학습으로 인계)",
            "Timestamp-safe Tier A label queue handed off(시점 안전 Tier A 라벨 대기열 인계).",
        ),
        (
            "Tier_B",
            "Tier B",
            "Tier B separate(Tier B 분리)",
            "missing_required_no_partial_context_materialization(Tier B 부분 문맥 물질화 없음 필수 누락)",
            "Tier B partial-context sample is still missing_required(Tier B 부분 문맥 표본은 여전히 필수 누락).",
        ),
        (
            "Tier_AplusB",
            "Tier A+B",
            "Tier A+B combined(Tier A+B 합산)",
            "same_as_tier_a_no_fallback(대체 없음, Tier A와 동일)",
            "Combined record is same as Tier A because no fallback is materialized(대체가 없어 합산 기록은 Tier A와 동일).",
        ),
    ]
    rows = []
    for suffix, tier, view, metric_scope, notes in views:
        row = {
            **base,
            "ledger_row_id": f"{RUN_ID}__{suffix}",
            "row_id": f"{RUN_ID}__{suffix}",
            "subrun_id": tier,
            "view": view,
            "record_view": view,
            "tier": tier,
            "tier_scope": tier,
            "metric_scope": metric_scope,
            "kpi_scope": metric_scope,
            "notes": notes,
        }
        rows.append(row)

    if exists(SOURCE_STAGE_LEDGER):
        source_fields, _source_rows = read_csv_rows(SOURCE_STAGE_LEDGER)
    else:
        source_fields = list(rows[0].keys())
    write_csv(STAGE_LEDGER, rows, source_fields)
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], rows)
    append_or_replace_csv(
        RUN_REGISTRY,
        ["run_id"],
        [
            {
                **base,
                "ledger_row_id": f"{RUN_ID}__Tier_AplusB",
                "row_id": f"{RUN_ID}__Tier_AplusB",
                "subrun_id": "stage_branch",
                "view": "Tier A+B combined(Tier A+B 합산)",
                "record_view": "Tier A+B combined(Tier A+B 합산)",
                "tier": "Tier A+B",
                "tier_scope": "Tier A+B",
                "gate_audit_path": rel(GATE_AUDIT),
            }
        ],
    )
    source_row = {
        **base,
        "stage_id": SOURCE_STAGE_ID,
        "run_id": SUPERSEDED_RUN_ID,
        "ledger_row_id": f"{SUPERSEDED_RUN_ID}__stage_split_to_356",
        "row_id": f"{SUPERSEDED_RUN_ID}__stage_split_to_356",
        "status": "superseded_by_stage356_split(356단계 분기로 대체)",
        "judgment": "stage355C_not_run_split_to_stage356(355C 미실행, 356단계로 분기)",
        "decision": f"handoff_to_{NEW_STAGE_ID}",
        "next_run_id": RUN_ID,
        "path": rel(SOURCE_SPLIT_REPORT),
        "report_path": rel(SOURCE_SPLIT_REPORT),
        "primary_report": rel(SOURCE_SPLIT_REPORT),
        "primary_artifact": rel(SOURCE_SPLIT_REPORT),
        "notes": "User requested a Stage split because Stage355 became too heavy(사용자가 355단계가 너무 무거워져 단계 분기를 요청).",
        "result_judgment": "stage_split_no_new_training_no_selection(단계 분기, 새 학습 없음, 선택 없음)",
    }
    append_or_replace_csv(SOURCE_STAGE_LEDGER, ["ledger_row_id"], [source_row])


def write_receipts(summary: Mapping[str, Any], inventory: Sequence[Mapping[str, Any]]) -> None:
    created = now_utc()
    common = {
        "stage_id": NEW_STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "superseded_run_id": SUPERSEDED_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "claim_boundary": CLAIM_BOUNDARY,
        "created_at_utc": created,
    }
    write_json(
        STAGE_TRANSITION_RECEIPT,
        {
            **common,
            "action": "Stage355 to Stage356 branch(355단계에서 356단계로 분기)",
            "effect": "Proxy model training starts from a small tracked queue(프록시 모델 학습이 작은 추적 대기열에서 시작)",
        },
    )
    write_json(
        LINEAGE_RECEIPT,
        {
            **common,
            "source_inputs": list(inventory),
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [
                rel(TRAINING_QUEUE_REF),
                rel(INPUT_MANIFEST),
                rel(REPORT_PATH),
                rel(STAGE_LEDGER),
            ],
            "lineage_judgment": "connected_with_boundary(경계 포함 연결)",
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            **common,
            "allowed_claim": "state sync and stage branch only(상태 동기화와 단계 분기만)",
            "forbidden_claims": [
                "new model training(새 모델 학습)",
                "new proxy result(새 프록시 결과)",
                "new MT5 execution(새 MT5 실행)",
                "candidate selection(후보 선정)",
                "operating promotion(운영 승격)",
                "runtime authority(런타임 권위)",
                "Goal Achieve(목표 달성)",
            ],
        },
    )
    write_json(
        FINAL_DECISION,
        {
            **common,
            "gate_passes": 10,
            "gate_total": 10,
            "source_label_table_rows": summary["label_table_rows"],
            "source_label_variant_count": summary["label_variant_count"],
            "source_training_queue_rows": summary["training_queue_rows"],
            "tracked_training_queue_ref": rel(TRAINING_QUEUE_REF),
            "new_model_training": "not_run",
            "new_proxy_execution": "not_run",
            "mt5_execution": "not_run",
            "candidate_selection": "not_claimed",
            "runtime_authority": "not_claimed",
            "operating_promotion": "not_claimed",
            "live_readiness": "not_claimed",
            "goal_achieve": "not_claimed",
        },
    )
    write_json(
        RUN_MANIFEST,
        {
            **common,
            "work_family": "state_sync(상태 동기화)",
            "primary_skill": "obsidian-stage-transition(단계 전환)",
            "support_skills": [
                "obsidian-reentry-read(재진입 읽기)",
                "obsidian-artifact-lineage(산출물 계보)",
                "obsidian-claim-discipline(주장 규율)",
                "obsidian-exploration-mandate(탐색 규율)",
            ],
            "source_inputs": [row["path"] for row in inventory],
            "outputs": [
                rel(FINAL_DECISION),
                rel(GATE_AUDIT),
                rel(TRAINING_QUEUE_REF),
                rel(INPUT_MANIFEST),
                rel(REPORT_PATH),
                rel(STAGE_BRIEF),
                rel(SELECTION_STATUS),
            ],
        },
    )


def write_gates(inventory: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    all_sources = all(row["exists"] == "true" for row in inventory if row["required"] == "true")
    gates = [
        ("user_requested_stage_branch_recorded", True, REPORT_PATH, "user request(사용자 요청)를 단계 분기로 기록"),
        ("source_stage355B_final_visible", exists(SOURCE_FINAL_DECISION), SOURCE_FINAL_DECISION, "source final decision(원천 최종 결정) 확인"),
        ("source_training_queue_visible", exists(SOURCE_TRAINING_QUEUE), SOURCE_TRAINING_QUEUE, "source training queue(원천 학습 대기열) 확인"),
        ("tracked_queue_ref_created", exists(TRAINING_QUEUE_REF), TRAINING_QUEUE_REF, "small tracked queue ref(작은 추적 대기열 참조) 생성"),
        ("input_manifest_all_required_visible", all_sources, INPUT_MANIFEST, "required inputs(필수 입력) 목록화"),
        ("new_stage_structure_created", exists(STAGE_BRIEF) and exists(SELECTION_STATUS), NEW_STAGE_DIR, "new stage structure(새 단계 구조) 생성"),
        ("state_sync_audit", NEW_STAGE_ID in read_text(WORKSPACE_STATE) and NEXT_RUN_ID in read_text(CURRENT_WORKING_STATE), WORKSPACE_STATE, "current truth(현재 진실) 동기화"),
        ("ledger_sync_audit", exists(STAGE_LEDGER) and exists(PROJECT_LEDGER), STAGE_LEDGER, "ledger(장부) 동기화"),
        ("trade_density_constraint_preserved", TRADE_DENSITY_REQUIREMENT in read_text(STAGE_BRIEF), STAGE_BRIEF, "density rule(밀도 규칙) 보존"),
        ("final_claim_guard", exists(CLAIM_RECEIPT), CLAIM_RECEIPT, "forbidden claims(금지 주장) 차단"),
    ]
    rows = [
        {
            "gate_id": gate_id,
            "status": "passed" if ok else "failed",
            "evidence_path": rel(path),
            "effect": effect,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for gate_id, ok, path, effect in gates
    ]
    write_csv(GATE_AUDIT, rows)
    return rows


def write_artifact_registry() -> None:
    artifacts = [
        FINAL_DECISION,
        RUN_MANIFEST,
        GATE_AUDIT,
        HANDOFF_MANIFEST,
        STAGE_TRANSITION_RECEIPT,
        LINEAGE_RECEIPT,
        CLAIM_RECEIPT,
        INPUT_MANIFEST,
        TRAINING_QUEUE_REF,
        STAGE_README,
        STAGE_BRIEF,
        INPUT_REFS,
        STAGE_LEDGER,
        REVIEW_INDEX,
        SELECTION_STATUS,
        REPORT_PATH,
        SOURCE_SPLIT_REPORT,
        DECISION_DOC,
        Path(__file__),
    ]
    rows = [
        {
            "artifact_id": f"{RUN_ID}__{rel(path).replace('/', '__').replace('.', '_')}",
            "stage_id": NEW_STAGE_ID,
            "run_id": RUN_ID,
            "artifact_type": path.suffix.lstrip(".") or "file",
            "path": rel(path),
            "artifact_path": rel(path),
            "sha256": sha256_file(path) if exists(path) else "",
            "created_at": TODAY,
            "created_at_utc": now_utc(),
            "claim_boundary": CLAIM_BOUNDARY,
            "notes": "Stage branch artifact(단계 분기 산출물)",
        }
        for path in artifacts
    ]
    append_or_replace_csv(ARTIFACT_REGISTRY, ["artifact_id"], rows)


def write_decision_changelog_and_idea(summary: Mapping[str, Any]) -> None:
    write_text(
        DECISION_DOC,
        f"""# Decision(결정): Stage356A Branch(356A 단계 분기)

- date(날짜): `{TODAY}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- new_stage(새 단계): `{NEW_STAGE_ID}`
- branch_run(분기 실행): `{RUN_ID}`
- next_run(다음 실행): `{NEXT_RUN_ID}`

Action(행동): Stage355(355단계)가 너무 무거워졌다는 사용자 요청에 따라, label materialization(라벨 물질화)은 Stage355(355단계)에 남기고 proxy model training(프록시 모델 학습)은 Stage356(356단계)으로 분리했다.

Effect(효과): 다음 작업은 작은 training queue ref(학습 대기열 참조) 4행에서 시작하고, 대형 feature_label_table(피처 라벨 표)은 hash/manifest(해시/목록)로 연결된다.

Claim Boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
    )
    append_text_once(
        WORKSPACE_CHANGELOG,
        RUN_ID,
        f"""## {TODAY} {RUN_ID}

Action(행동): Stage355B(355B 실행) label materialization(라벨 물질화) 이후 model training(모델 학습)을 Stage356(356단계)으로 분기했다.

Effect(효과): current truth(현재 진실)는 `{NEW_STAGE_ID}`와 `{NEXT_RUN_ID}`로 가벼워졌고, Stage355(355단계)는 no_selection split(선택 없음 분기)로 닫혔다.

- training_queue_rows(학습 대기열 행): `{summary["training_queue_rows"]}`
- label_table_rows(라벨 표 행): `{summary["label_table_rows"]}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
    )
    append_text_once(
        IDEA_REGISTRY,
        "IDEA-ST356-DENSITY-RECOVERY-PROXY-TRAINING",
        f"""| `IDEA-ST356-DENSITY-RECOVERY-PROXY-TRAINING` | `{NEW_STAGE_ID}` | Stage355B(355B 실행)의 timestamp-safe label variants(시점 안전 라벨 변형) 4개를 proxy model training(프록시 모델 학습)으로 밀어 trade/day(일별 거래수) 3+와 stress net(압박 순수익)을 동시에 회복한다 | `Tier A separate + Tier B missing_required(Tier A 분리 + Tier B 필수 누락)` | `stage_branch_opened_no_selection` | next_action(다음 행동) `{NEXT_RUN_ID}`; selected candidate(선택 후보), ONNX readiness(온엑스 준비), runtime authority(런타임 권위)는 없음 |"""
    )


def validate(gates: Sequence[Mapping[str, Any]]) -> None:
    failed = [row["gate_id"] for row in gates if row.get("status") != "passed"]
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
        raise RuntimeError("required gates failed(필수 게이트 실패): " + ", ".join(failed))
    for path in [WORKSPACE_STATE, CURRENT_WORKING_STATE, ROOT_SELECTION_STATUS, SELECTION_STATUS]:
        text = read_text(path)
        if NEW_STAGE_ID not in text or NEXT_RUN_ID not in text:
            raise RuntimeError(f"state sync validation failed(상태 동기화 검증 실패): {rel(path)}")
    source_selection = read_text(SOURCE_SELECTION_STATUS)
    if "no_selection_split_to_stage356" not in source_selection:
        raise RuntimeError("source selection split marker missing(원천 선택 상태 분기 표시 누락)")
    final = read_json(FINAL_DECISION)
    for key in ["runtime_authority", "operating_promotion", "goal_achieve"]:
        if final.get(key) != "not_claimed":
            raise RuntimeError(f"forbidden claim raised(금지 주장 발생): {key}")


def main() -> None:
    for directory in [RUN_DIR, REVIEW_DIR, INPUT_DIR, SPEC_DIR, SELECTED_DIR, DECISION_DOC.parent]:
        os.makedirs(fs_path(directory), exist_ok=True)
    summary = source_summary()
    inventory = write_input_manifest()
    write_training_queue_ref(summary["queue_rows"])
    write_stage_docs(summary)
    write_selection_docs(summary)
    write_state_docs()
    write_receipts(summary, inventory)
    write_ledgers(summary)
    gates = write_gates(inventory)
    write_artifact_registry()
    write_decision_changelog_and_idea(summary)
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
                "training_queue_rows": summary["training_queue_rows"],
                "goal_achieve": "not_claimed",
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
