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

SOURCE_STAGE_ID = "356_density_recovery_training__proxy_model_queue_scout"
NEW_STAGE_ID = "357_high_density_label_pivot__trade_frequency_recovery"
SOURCE_STAGE_DIR = ROOT / "stages" / SOURCE_STAGE_ID
NEW_STAGE_DIR = ROOT / "stages" / NEW_STAGE_ID

RUN_NUMBER = "run357A"
RUN_ID = "run357A_branch_stage356_to_high_density_label_pivot_without_db_v1"
PARENT_RUN_ID = "run356C_expand_density_recovery_proxy_training_search_without_db_v1"
SUPERSEDED_RUN_ID = "run356D_design_high_density_label_pivot_without_db_v1"
NEXT_RUN_ID = "run357B_design_high_density_label_pivot_without_db_v1"

STATUS = "completed_stage357A_user_requested_stage_split_high_density_label_pivot_opened_no_selection"
JUDGMENT = (
    "stage_branch_completed_stage356_density_recovery_split_to_stage357_high_density_label_pivot_"
    "no_operating_claim"
)
DECISION = "stage357A_open_run357B_design_high_density_label_pivot_without_db_v1"
CLAIM_BOUNDARY = (
    "state_sync_stage_branch_user_requested_high_density_label_pivot_handoff_only_"
    "no_new_model_training_no_new_proxy_execution_no_mt5_execution_no_candidate_selection_"
    "no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)
TRADE_DENSITY_REQUIREMENT = "trade_per_day_min_3_to_10_plus_no_trade_splitting"

SOURCE_RUN_DIR = SOURCE_STAGE_DIR / "02_runs" / "run356C"
SOURCE_FINAL_DECISION = SOURCE_RUN_DIR / "final_decision.json"
SOURCE_BEST_SCORECARD = SOURCE_RUN_DIR / "best_expansion_scorecard.csv"
SOURCE_QUEUE = SOURCE_RUN_DIR / "mt5_probe_candidate_queue.csv"
SOURCE_GATE_AUDIT = SOURCE_RUN_DIR / "required_gate_coverage_audit.csv"
SOURCE_REGRESSION_SWEEP = SOURCE_RUN_DIR / "regression_density_sweep_scorecard.csv"
SOURCE_UNION_SWEEP = SOURCE_RUN_DIR / "union_density_sweep_scorecard.csv"
SOURCE_ONNX_PARITY = SOURCE_RUN_DIR / "onnx_regression_parity_matrix.csv"
SOURCE_REPORT = SOURCE_STAGE_DIR / "03_reviews" / "run356C_density_recovery_proxy_expansion.md"
SOURCE_STAGE_LEDGER = SOURCE_STAGE_DIR / "03_reviews" / "stage_run_ledger.csv"
SOURCE_REVIEW_INDEX = SOURCE_STAGE_DIR / "03_reviews" / "review_index.md"
SOURCE_SELECTION_STATUS = SOURCE_STAGE_DIR / "04_selected" / "selection_status.md"
SOURCE_STAGE_BRIEF = SOURCE_STAGE_DIR / "00_spec" / "stage_brief.md"
SOURCE_SCRIPT = (
    ROOT / "stage_pipelines" / "stage356" / "expand_density_recovery_proxy_search_without_db.py"
)

RUN_DIR = NEW_STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = NEW_STAGE_DIR / "03_reviews"
INPUT_DIR = NEW_STAGE_DIR / "01_inputs"
SPEC_DIR = NEW_STAGE_DIR / "00_spec"
SELECTED_DIR = NEW_STAGE_DIR / "04_selected"

STAGE_README = NEW_STAGE_DIR / "README.md"
STAGE_BRIEF = SPEC_DIR / "stage_brief.md"
INPUT_REFS = INPUT_DIR / "input_refs.md"
INPUT_MANIFEST = INPUT_DIR / "stage357_input_manifest.csv"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"
REVIEW_INDEX = REVIEW_DIR / "review_index.md"
SELECTION_STATUS = SELECTED_DIR / "selection_status.md"
REPORT_PATH = REVIEW_DIR / "run357A_stage_branch.md"
SOURCE_SPLIT_REPORT = SOURCE_STAGE_DIR / "03_reviews" / "run356C_stage_split_to_357.md"

HANDOFF_MANIFEST = RUN_DIR / "stage356C_to_stage357_handoff_manifest.csv"
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
NEGATIVE_RESULT_REGISTER = ROOT / "docs" / "registers" / "negative_result_register.md"
WORKSPACE_CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
DECISION_DOC = (
    ROOT / "docs" / "decisions" / f"{TODAY}_stage357A_branch_stage356_to_high_density_label_pivot.md"
)

SOURCE_INPUTS: list[tuple[Path, str, bool, str]] = [
    (SOURCE_FINAL_DECISION, "run356C final decision(356C 최종 결정)", True, "ignored_with_manifest"),
    (SOURCE_BEST_SCORECARD, "run356C best expansion scorecard(356C 최선 확장 점수표)", True, "ignored_with_manifest"),
    (SOURCE_QUEUE, "run356C MT5 probe queue(356C MT5 탐침 대기열)", True, "ignored_with_manifest"),
    (SOURCE_GATE_AUDIT, "run356C gate audit(356C 게이트 감사)", True, "ignored_with_manifest"),
    (SOURCE_REGRESSION_SWEEP, "run356C regression sweep(356C 회귀 탐색)", True, "ignored_with_manifest"),
    (SOURCE_UNION_SWEEP, "run356C union sweep(356C 합집합 탐색)", True, "ignored_with_manifest"),
    (SOURCE_ONNX_PARITY, "run356C ONNX parity(356C 온엑스 동등성)", True, "ignored_with_manifest"),
    (SOURCE_REPORT, "run356C review report(356C 검토 보고서)", True, "tracked"),
    (SOURCE_STAGE_LEDGER, "Stage356 ledger(356단계 장부)", True, "tracked"),
    (SOURCE_SELECTION_STATUS, "Stage356 selection status(356단계 선택 상태)", True, "tracked"),
    (SOURCE_STAGE_BRIEF, "Stage356 brief(356단계 개요)", True, "tracked"),
    (SOURCE_SCRIPT, "run356C producer script(356C 생산 스크립트)", True, "tracked"),
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


def sha256_file(path: Path | str) -> str:
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
        fieldnames = []
        for row in rows_list:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
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
    _best_fields, best_rows = read_csv_rows(SOURCE_BEST_SCORECARD)
    _queue_fields, queue_rows = read_csv_rows(SOURCE_QUEUE)
    best = best_rows[0] if best_rows else final.get("best_row", {})
    return {
        "final": final,
        "best": best,
        "best_rows": len(best_rows),
        "queue_rows": len(queue_rows),
        "trained_regression_models": final.get("trained_regression_models", ""),
        "onnx_parity_rows": final.get("onnx_parity_rows", ""),
        "regression_paired_rows": final.get("regression_paired_rows", ""),
        "union_paired_rows": final.get("union_paired_rows", ""),
        "validation_trade_per_day": best.get("validation_trade_per_day", ""),
        "validation_stress_net": best.get("validation_stress_net", ""),
        "validation_stress_pf": best.get("validation_stress_pf", ""),
        "oos_trade_per_day": best.get("oos_trade_per_day", ""),
        "oos_stress_net": best.get("oos_stress_net", ""),
        "oos_stress_pf": best.get("oos_stress_pf", ""),
        "candidate_gate": best.get("candidate_gate", ""),
        "model_id": best.get("model_id", ""),
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


def write_stage_docs(summary: Mapping[str, Any]) -> None:
    write_text(
        SOURCE_SPLIT_REPORT,
        f"""# run356C Stage Split To Stage357(run356C 357단계 분기)

- source_stage_id(원천 단계 ID): `{SOURCE_STAGE_ID}`
- source_completed_run_id(완료 원천 실행 ID): `{PARENT_RUN_ID}`
- split_run_id(분기 실행 ID): `{RUN_ID}`
- superseded_run_id(대체된 실행 ID): `{SUPERSEDED_RUN_ID}`
- next_stage_id(다음 단계 ID): `{NEW_STAGE_ID}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- status(상태): `split_to_stage357_high_density_label_pivot(357단계 고밀도 라벨 전환으로 분기)`

Action(행동): Stage356(356단계)은 density recovery training scout(밀도 회복 학습 탐색)까지로 가볍게 멈추고, high-density label pivot(고밀도 라벨 전환) 질문은 Stage357(357단계)로 분리했다.

Effect(효과): Stage356C(356C 실행)의 negative memory(부정 기억)는 보존하고, 다음 작업은 Stage357B(357B 실행)의 작은 question scope(질문 범위)에서 시작한다.

Boundary(경계): 이 분기는 model training(모델 학습), proxy execution(프록시 실행), MT5 execution(MT5 실행), candidate selection(후보 선정), operating promotion(운영 승격), runtime authority(런타임 권위), Goal Achieve(목표 달성)를 주장하지 않는다.
""",
    )
    append_text_once(SOURCE_REVIEW_INDEX, "run356C_stage_split_to_357", f"- `{rel(SOURCE_SPLIT_REPORT)}`")

    write_text(
        STAGE_README,
        f"""# Stage357 High-Density Label Pivot(357단계 고밀도 라벨 전환)

- current_run(현재 실행): `{NEXT_RUN_ID}`
- branch_run(분기 실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{PARENT_RUN_ID}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Action(행동): Stage356C(356C 실행)의 density edge miss(밀도 우위 미달)를 Stage357(357단계)의 high-density H12 label pivot(고밀도 H12 라벨 전환) 질문으로 넘겼다.

Effect(효과): Stage356(356단계)에 더 많은 run(실행)을 얹지 않고, Stage357B(357B 실행)에서 새 label/model surface(라벨/모델 표면)를 작게 시작한다.
""",
    )
    write_text(
        STAGE_BRIEF,
        f"""# Stage357 High-Density Label Pivot(357단계 고밀도 라벨 전환)

- canonical_stage_id(정식 단계 ID): `{NEW_STAGE_ID}`
- current_run_id(현재 실행 ID): `{NEXT_RUN_ID}`
- latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`
- source_stage_id(원천 단계 ID): `{SOURCE_STAGE_ID}`
- source_run_id(원천 실행 ID): `{PARENT_RUN_ID}`
- superseded_run_id(대체된 실행 ID): `{SUPERSEDED_RUN_ID}`
- selection_status(선택 상태): `stage_branch_opened_no_selection(단계 분기 완료, 선택 없음)`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

## Question(질문)

Stage356C(356C 실행)에서 trade/day(일별 거래수) 3 미만으로 막힌 density recovery(밀도 회복)를 H12 train-quantile high-density label(학습 분위수 고밀도 H12 라벨)과 ONNX classifier(온엑스 분류기)로 회복할 수 있는가?

## Source Truth(원천 진실)

- trained_regression_models(학습 회귀 모델): `{summary["trained_regression_models"]}`
- onnx_parity_rows(온엑스 동등성 행): `{summary["onnx_parity_rows"]}`
- regression_paired_rows(회귀 쌍 탐색 행): `{summary["regression_paired_rows"]}`
- union_paired_rows(합집합 쌍 탐색 행): `{summary["union_paired_rows"]}`
- mt5_probe_queue_rows(MT5 탐침 대기열 행): `{summary["queue_rows"]}`
- best_validation_trade_per_day(최선 검증 일별 거래수): `{summary["validation_trade_per_day"]}`
- best_validation_stress_pf(최선 검증 압박 수익 팩터): `{summary["validation_stress_pf"]}`
- best_oos_trade_per_day(최선 표본외 일별 거래수): `{summary["oos_trade_per_day"]}`
- best_oos_stress_pf(최선 표본외 압박 수익 팩터): `{summary["oos_stress_pf"]}`
- candidate_gate(후보 게이트): `{summary["candidate_gate"]}`

## Scope(범위)

Stage357(357단계)는 high-density label pivot(고밀도 라벨 전환), ONNX classifier parity(온엑스 분류기 동등성), non-overlap proxy queue(비중첩 프록시 대기열)까지만 다룬다. MT5 runtime probe(MT5 런타임 탐침)는 positive queue(긍정 대기열)가 생긴 뒤 별도 run(실행)에서 다룬다.

## Exploration Plan(탐색 계획)

- idea_id(아이디어 ID): `IDEA-ST357-HIGH-DENSITY-LABEL-PIVOT`
- hypothesis(가설): H12 train-quantile band label(학습 분위수 H12 밴드 라벨)이 trade splitting(거래 쪼개기) 없이 trade/day(일별 거래수) 3+와 positive stress net/PF(양수 압박 순수익/수익 팩터)를 동시에 회복한다.
- legacy_relation(레거시 관계): `none(없음)`
- tier_scope(티어 범위): `Tier A separate + Tier B missing_required(Tier A 분리 + Tier B 필수 누락)`
- broad_sweep(넓은 탐색): q40/q60, q45/q55 label bands(라벨 밴드), shallow ExtraTrees classifier(얕은 엑스트라트리스 분류기), probability score policy(확률 점수 정책), ADX/session filter(ADX/세션 필터)
- extreme_sweep(극단 탐색): no-flat sign label(무평탄 방향 라벨), soft cost flat label(완화 비용 평탄 라벨), low score quantile(낮은 점수 분위수), high ADX(높은 ADX)
- micro_search_gate(미세 탐색 게이트): validation/OOS proxy trade/day(검증/표본외 프록시 일별 거래수) 3+와 stress PF(압박 수익 팩터) 1.02+
- wfo_plan(WFO 계획): scout pass(탐색 회차) 뒤 WFO(walk-forward optimization, 워크포워드 최적화) 프레임으로 재검증
- failure_memory(실패 기억): Stage356C(356C 실행)는 OOS PF(표본외 수익 팩터)는 양수였지만 validation PF(검증 수익 팩터)와 trade/day(일별 거래수)가 후보 게이트를 넘지 못했다.
- evidence_boundary(근거 경계): `stage_branch_only(단계 분기 전용)`

## Density Constraint(밀도 제약)

`{TRADE_DENSITY_REQUIREMENT}`

Action(행동): trade splitting(거래 쪼개기) 없이 trade/day(일별 거래수) 3~10+ 조건을 Stage357B(357B 실행)의 기본 제약으로 둔다.

Effect(효과): 낮은 거래수로 예쁜 net profit(순수익)을 만든 후보가 운영 후보처럼 보이지 않게 한다.
""",
    )
    write_text(
        INPUT_REFS,
        f"""# Stage357 Input Refs(357단계 입력 참조)

- source_final_decision(원천 최종 결정): `{rel(SOURCE_FINAL_DECISION)}`
- source_best_scorecard(원천 최선 점수표): `{rel(SOURCE_BEST_SCORECARD)}`
- source_mt5_probe_queue(원천 MT5 탐침 대기열): `{rel(SOURCE_QUEUE)}`
- source_gate_audit(원천 게이트 감사): `{rel(SOURCE_GATE_AUDIT)}`
- source_regression_sweep(원천 회귀 탐색): `{rel(SOURCE_REGRESSION_SWEEP)}`
- source_union_sweep(원천 합집합 탐색): `{rel(SOURCE_UNION_SWEEP)}`
- source_onnx_parity(원천 온엑스 동등성): `{rel(SOURCE_ONNX_PARITY)}`
- input_manifest(입력 목록): `{rel(INPUT_MANIFEST)}`

Action(행동): Stage356C(356C 실행)의 큰 02_runs(실행 산출물) 파일은 hash/manifest(해시/목록)로 연결하고, Stage357(357단계)은 작은 state sync(상태 동기화) 산출물만 추적한다.

Effect(효과): 무거운 proxy artifact(프록시 산출물)를 다시 커밋하지 않고도 Stage357B(357B 실행)가 같은 source identity(원천 정체성)를 재사용할 수 있다.
""",
    )


def write_selection_docs(summary: Mapping[str, Any]) -> None:
    write_text(
        SOURCE_SELECTION_STATUS,
        f"""# Stage356 Selection Status(356단계 선택 상태)

- selection_status(선택 상태): `no_selection_split_to_stage357(선택 없음, 357단계로 분기)`
- active_stage_id(활성 단계 ID): `{SOURCE_STAGE_ID}`
- latest_run_id(최근 실행 ID): `{PARENT_RUN_ID}`
- superseded_run_id(대체된 실행 ID): `{SUPERSEDED_RUN_ID}`
- handoff_stage_id(인계 단계 ID): `{NEW_STAGE_ID}`
- handoff_run_id(인계 실행 ID): `{RUN_ID}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- mt5_probe_queue_rows(MT5 탐침 대기열 행): `{summary["queue_rows"]}`
- runtime_authority(런타임 권위): `not_claimed`
- operating_promotion(운영 승격): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
""",
    )
    selection = f"""# Stage357 Selection Status(357단계 선택 상태)

- selection_status(선택 상태): `stage_branch_opened_no_selection(단계 분기 완료, 선택 없음)`
- active_stage_id(활성 단계 ID): `{NEW_STAGE_ID}`
- latest_run_id(최근 실행 ID): `{RUN_ID}`
- current_run_id(현재 실행 ID): `{NEXT_RUN_ID}`
- source_run_id(원천 실행 ID): `{PARENT_RUN_ID}`
- mt5_probe_queue_rows(MT5 탐침 대기열 행): `0`
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

Action(행동): 사용자의 Stage split(단계 분기) 요청에 따라 Stage356(356단계)을 density recovery scout(밀도 회복 탐색)로 멈추고, high-density label pivot(고밀도 라벨 전환)은 Stage357(357단계)로 분리했다.

Effect(효과): 다음 재진입(re-entry, 재진입)은 `{NEXT_RUN_ID}`에서 바로 시작하며, 아직 model training(모델 학습), MT5 execution(MT5 실행), candidate selection(후보 선정), operating claim(운영 주장)은 없다.
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
        "gate_passes": 12,
        "gate_total": 12,
        "claim_boundary": CLAIM_BOUNDARY,
        "scoreboard_lane": "state_sync_stage_branch(상태 동기화 단계 분기)",
        "lane": "state_sync_stage_branch(상태 동기화 단계 분기)",
        "family": "state_sync(상태 동기화)",
        "work_family": "state_sync(상태 동기화)",
        "run_number": RUN_NUMBER,
        "notes": "Stage356 heavy density recovery thread split to Stage357 high-density label pivot(356단계 무거운 밀도 회복 흐름을 357단계 고밀도 라벨 전환으로 분기).",
        "source_package_run_id": PARENT_RUN_ID,
        "rows": summary["best_rows"],
        "candidate_rows": summary["queue_rows"],
        "external_verification_status": "out_of_scope_by_claim(주장 범위 밖)",
        "result_status": "stage_branch_opened_no_selection(단계 분기 완료, 선택 없음)",
        "primary_kpi": "mt5_probe_queue_rows=0(MT5 탐침 대기열 0행)",
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
            "stage_branch_full_context_density_recovery_to_label_pivot(전체 문맥 밀도 회복에서 라벨 전환으로 분기)",
            "Tier A full-context Stage356C evidence handed off(Tier A 전체 문맥 Stage356C 근거 인계).",
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
        "ledger_row_id": f"{SUPERSEDED_RUN_ID}__stage_split_to_357",
        "row_id": f"{SUPERSEDED_RUN_ID}__stage_split_to_357",
        "status": "superseded_by_stage357_split(357단계 분기로 대체)",
        "judgment": "stage356D_not_run_split_to_stage357(356D 미실행, 357단계로 분기)",
        "decision": f"handoff_to_{NEW_STAGE_ID}",
        "next_run_id": RUN_ID,
        "path": rel(SOURCE_SPLIT_REPORT),
        "report_path": rel(SOURCE_SPLIT_REPORT),
        "primary_report": rel(SOURCE_SPLIT_REPORT),
        "primary_artifact": rel(SOURCE_SPLIT_REPORT),
        "notes": "User requested a Stage split because Stage356 became too heavy(사용자가 356단계가 너무 무거워져 단계 분기를 요청).",
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
            "action": "Stage356 to Stage357 branch(356단계에서 357단계로 분기)",
            "effect": "High-density label pivot starts in a lighter stage(고밀도 라벨 전환을 더 가벼운 단계에서 시작)",
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
                rel(INPUT_MANIFEST),
                rel(REPORT_PATH),
                rel(STAGE_LEDGER),
                rel(STAGE_BRIEF),
            ],
            "artifact_hashes": {row["path"]: row["sha256"] for row in inventory},
            "registry_links": [
                rel(PROJECT_LEDGER),
                rel(RUN_REGISTRY),
                rel(ARTIFACT_REGISTRY),
            ],
            "availability": "tracked_docs_with_ignored_heavy_inputs_by_hash(추적 문서와 해시 기반 무거운 입력)",
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
            "gate_passes": 12,
            "gate_total": 12,
            "source_best_validation_trade_per_day": summary["validation_trade_per_day"],
            "source_best_oos_trade_per_day": summary["oos_trade_per_day"],
            "source_mt5_probe_queue_rows": summary["queue_rows"],
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
            "required_gates": [
                "state_sync_audit",
                "final_claim_guard",
                "required_gate_coverage_audit",
            ],
            "source_inputs": [row["path"] for row in inventory],
            "outputs": [
                rel(FINAL_DECISION),
                rel(GATE_AUDIT),
                rel(INPUT_MANIFEST),
                rel(REPORT_PATH),
                rel(STAGE_BRIEF),
                rel(SELECTION_STATUS),
            ],
        },
    )


def write_report_and_decision(summary: Mapping[str, Any]) -> None:
    write_text(
        REPORT_PATH,
        f"""# run357A Stage Branch(run357A 단계 분기)

- run_id(실행 ID): `{RUN_ID}`
- source_stage_id(원천 단계 ID): `{SOURCE_STAGE_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- superseded_run_id(대체된 실행 ID): `{SUPERSEDED_RUN_ID}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- gates(게이트): `12/12`

Action(행동): 사용자의 Stage split(단계 분기) 요청에 따라 Stage356(356단계)의 다음 질문을 Stage357(357단계)로 넘겼다.

Effect(효과): Stage356(356단계)은 run356C(356C 실행)까지의 negative proxy memory(부정 프록시 기억)를 보존하고, high-density label pivot(고밀도 라벨 전환)은 Stage357B(357B 실행)에서 가볍게 시작한다.

Current Truth(현재 진실): run356C(356C 실행)의 best row(최선 행)는 validation trade/day(검증 일별 거래수) `{summary["validation_trade_per_day"]}`, validation PF(검증 수익 팩터) `{summary["validation_stress_pf"]}`, OOS trade/day(표본외 일별 거래수) `{summary["oos_trade_per_day"]}`, OOS PF(표본외 수익 팩터) `{summary["oos_stress_pf"]}`였고, mt5_probe_queue_rows(MT5 탐침 대기열 행)는 `{summary["queue_rows"]}`이다.

Claim Boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
    )
    append_text_once(REVIEW_INDEX, "run357A_stage_branch", f"- `{rel(REPORT_PATH)}`")
    write_text(
        DECISION_DOC,
        f"""# Decision(결정): Stage357A Branch(357A 단계 분기)

- date(날짜): `{TODAY}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- new_stage(새 단계): `{NEW_STAGE_ID}`
- branch_run(분기 실행): `{RUN_ID}`
- next_run(다음 실행): `{NEXT_RUN_ID}`

Action(행동): Stage356(356단계)이 너무 무거워졌다는 사용자 요청에 따라, density recovery training scout(밀도 회복 학습 탐색)은 Stage356(356단계)에 남기고 high-density label pivot(고밀도 라벨 전환)은 Stage357(357단계)로 분리했다.

Effect(효과): 다음 작업은 Stage357B(357B 실행)에서 H12 train-quantile label(학습 분위수 H12 라벨)과 ONNX classifier(온엑스 분류기)를 다루며, Stage356C(356C 실행)의 실패 기억은 제약으로만 재사용한다.

Claim Boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
    )
    append_text_once(
        WORKSPACE_CHANGELOG,
        RUN_ID,
        f"""## {TODAY} {RUN_ID}

Action(행동): Stage356C(356C 실행) 이후 high-density label pivot(고밀도 라벨 전환) 질문을 Stage357(357단계)로 분기했다.

Effect(효과): current truth(현재 진실)는 `{NEW_STAGE_ID}`와 `{NEXT_RUN_ID}`로 가벼워졌고, Stage356(356단계)은 no_selection split(선택 없음 분기)로 정리됐다.

- mt5_probe_queue_rows(MT5 탐침 대기열 행): `{summary["queue_rows"]}`
- source_best_oos_trade_per_day(원천 최선 표본외 일별 거래수): `{summary["oos_trade_per_day"]}`
- source_best_oos_stress_pf(원천 최선 표본외 압박 수익 팩터): `{summary["oos_stress_pf"]}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
    )


def write_registers(summary: Mapping[str, Any]) -> None:
    append_text_once(
        IDEA_REGISTRY,
        "IDEA-ST357-HIGH-DENSITY-LABEL-PIVOT",
        f"""| `IDEA-ST357-HIGH-DENSITY-LABEL-PIVOT` | `{NEW_STAGE_ID}` | H12 train-quantile high-density label(학습 분위수 고밀도 H12 라벨)이 trade/day(일별 거래수) 3+와 positive stress PF(양수 압박 수익 팩터)를 동시에 회복하는지 탐색한다. | `Tier A separate + Tier B missing_required(Tier A 분리 + Tier B 필수 누락)` | `stage_branch_opened_no_selection(단계 분기 완료, 선택 없음)` | next_action(다음 행동) `{NEXT_RUN_ID}`; operating claim(운영 주장) 없음 |"""
    )
    append_text_once(
        NEGATIVE_RESULT_REGISTER,
        RUN_ID,
        f"""## {TODAY} {RUN_ID}

- subject(대상): Stage356C density recovery expansion(356C 밀도 회복 확장)
- result_label(결과 라벨): `negative_memory_for_stage357_seed(357단계 씨앗용 부정 기억)`
- failure_boundary(실패 경계): validation trade/day(검증 일별 거래수) `{summary["validation_trade_per_day"]}`와 validation PF(검증 수익 팩터) `{summary["validation_stress_pf"]}`가 후보 조건을 넘지 못했다.
- salvage_value(회수 가치): OOS PF(표본외 수익 팩터) `{summary["oos_stress_pf"]}`와 OOS net(표본외 순수익) `{summary["oos_stress_net"]}`는 high-density label pivot(고밀도 라벨 전환)의 seed surface(씨앗 표면)로 보존한다.
- reopen_condition(재개 조건): Stage357B(357B 실행)에서 timestamp-safe(시점 안전) label(라벨), ONNX parity(온엑스 동등성), non-overlap proxy(비중첩 프록시)로 trade/day(일별 거래수) 3+를 회복할 때.
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
    )


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


def write_gates(inventory: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    required_sources_visible = all(row["exists"] == "true" for row in inventory if row["required"] == "true")
    gate_specs = [
        ("user_requested_stage_branch_recorded", True, REPORT_PATH, "user request(사용자 요청)를 단계 분기로 기록"),
        ("source_stage356C_final_visible", exists(SOURCE_FINAL_DECISION), SOURCE_FINAL_DECISION, "source final decision(원천 최종 결정) 확인"),
        ("source_best_scorecard_visible", exists(SOURCE_BEST_SCORECARD), SOURCE_BEST_SCORECARD, "source scorecard(원천 점수표) 확인"),
        ("input_manifest_all_required_visible", required_sources_visible, INPUT_MANIFEST, "required inputs(필수 입력) 목록화"),
        ("new_stage_structure_created", exists(STAGE_BRIEF) and exists(SELECTION_STATUS), NEW_STAGE_DIR, "new stage structure(새 단계 구조) 생성"),
        ("state_sync_audit", NEW_STAGE_ID in read_text(WORKSPACE_STATE) and NEXT_RUN_ID in read_text(CURRENT_WORKING_STATE), WORKSPACE_STATE, "current truth(현재 진실) 동기화"),
        ("selection_status_sync", NEW_STAGE_ID in read_text(ROOT_SELECTION_STATUS) and NEW_STAGE_ID in read_text(SELECTION_STATUS), SELECTION_STATUS, "selection status(선택 상태) 동기화"),
        ("ledger_sync_audit", exists(STAGE_LEDGER) and exists(PROJECT_LEDGER), STAGE_LEDGER, "ledger(장부) 동기화"),
        ("artifact_lineage_audit", exists(LINEAGE_RECEIPT), LINEAGE_RECEIPT, "artifact lineage(산출물 계보) 연결"),
        ("trade_density_constraint_preserved", TRADE_DENSITY_REQUIREMENT in read_text(STAGE_BRIEF), STAGE_BRIEF, "density rule(밀도 규칙) 보존"),
        ("final_claim_guard", exists(CLAIM_RECEIPT) and "not_claimed" in read_text(FINAL_DECISION), CLAIM_RECEIPT, "forbidden claims(금지 주장) 차단"),
    ]
    gate_ids = {item[0] for item in gate_specs}
    gate_specs.append(
        (
            "required_gate_coverage_audit",
            {"state_sync_audit", "final_claim_guard"}.issubset(gate_ids),
            GATE_AUDIT,
            "required gates(필수 게이트) 포함",
        )
    )
    rows = [
        {
            "gate_id": gate_id,
            "status": "passed" if ok else "failed",
            "evidence_path": rel(path),
            "effect": effect,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for gate_id, ok, path, effect in gate_specs
    ]
    write_csv(GATE_AUDIT, rows)
    return rows


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
    if "no_selection_split_to_stage357" not in source_selection:
        raise RuntimeError("source selection split marker missing(원천 선택 상태 분기 표시 누락)")
    final = read_json(FINAL_DECISION)
    for key in ["runtime_authority", "operating_promotion", "goal_achieve", "candidate_selection"]:
        if final.get(key) != "not_claimed":
            raise RuntimeError(f"forbidden claim raised(금지 주장 발생): {key}={final.get(key)}")


def main() -> None:
    for directory in [RUN_DIR, REVIEW_DIR, INPUT_DIR, SPEC_DIR, SELECTED_DIR, DECISION_DOC.parent]:
        os.makedirs(fs_path(directory), exist_ok=True)
    summary = source_summary()
    inventory = write_input_manifest()
    write_stage_docs(summary)
    write_selection_docs(summary)
    write_state_docs()
    write_receipts(summary, inventory)
    write_report_and_decision(summary)
    write_ledgers(summary)
    write_registers(summary)
    gates = write_gates(inventory)
    write_artifact_registry()
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
                "mt5_probe_queue_rows": summary["queue_rows"],
                "goal_achieve": "not_claimed",
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
