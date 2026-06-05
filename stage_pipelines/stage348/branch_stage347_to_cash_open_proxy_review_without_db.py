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

SOURCE_STAGE_ID = "347_cash_open_asymmetric_source__long_short_head_design"
NEW_STAGE_ID = "348_cash_open_proxy_review__long_oos_gap_short_carry_triage"
SOURCE_STAGE_DIR = ROOT / "stages" / SOURCE_STAGE_ID
NEW_STAGE_DIR = ROOT / "stages" / NEW_STAGE_ID

RUN_NUMBER = "run348A"
RUN_ID = "run348A_branch_stage347_to_cash_open_proxy_review_without_db_v1"
PARENT_RUN_ID = "run347C_train_cash_open_asymmetric_source_proxy_models_without_db_v1"
SUPERSEDED_RUN_ID = "run347D_review_cash_open_asymmetric_source_proxy_training_without_db_v1"
NEXT_RUN_ID = "run348B_review_cash_open_asymmetric_proxy_training_without_db_v1"
SOURCE_PACKAGE_RUN_ID = "run344N_materialize_cash_open_long_quality_short_carry_decomposition_package_without_db_v1"
SOURCE_RUNTIME_RUN_ID = "run345B_execute_cash_open_long_quality_short_carry_decomposition_mt5_probe_without_db_v1"

STATUS = "completed_stage348A_branch_from_stage347_proxy_review_scaffolded_no_selection"
JUDGMENT = "stage_branch_completed_stage347_overweight_proxy_training_handoff_to_stage348_review_no_operating_claim"
DECISION = "stage348A_open_run348B_review_cash_open_asymmetric_proxy_training"
CLAIM_BOUNDARY = (
    "state_sync_stage_branch_proxy_review_handoff_only_no_new_training_no_mt5_execution_"
    "no_candidate_selection_no_forward_pass_no_live_readiness_no_operating_promotion_"
    "no_runtime_authority_no_goal_claim"
)

RUN_DIR = NEW_STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = NEW_STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEW_DIR / "run348A_stage_branch_from_stage347_proxy_review.md"
REVIEW_INDEX = REVIEW_DIR / "review_index.md"
STAGE_BRIEF = NEW_STAGE_DIR / "00_spec" / "stage_brief.md"
STAGE_README = NEW_STAGE_DIR / "README.md"
INPUT_REFS = NEW_STAGE_DIR / "01_inputs" / "input_refs.md"
INPUT_MANIFEST = NEW_STAGE_DIR / "01_inputs" / "stage348_input_manifest.csv"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"
SELECTION_STATUS = NEW_STAGE_DIR / "04_selected" / "selection_status.md"

SOURCE_RUN_DIR = SOURCE_STAGE_DIR / "02_runs" / "run347C"
SOURCE_FINAL_DECISION = SOURCE_RUN_DIR / "final_decision.json"
SOURCE_GATE_AUDIT = SOURCE_RUN_DIR / "required_gate_coverage_audit.csv"
SOURCE_SCORECARD = SOURCE_RUN_DIR / "model_training_scorecard.csv"
SOURCE_PROBE_QUEUE = SOURCE_RUN_DIR / "probe_priority_queue.csv"
SOURCE_THRESHOLD_SCREEN = SOURCE_RUN_DIR / "proxy_threshold_screen.csv"
SOURCE_MODEL_MANIFEST = SOURCE_RUN_DIR / "model_artifact_manifest.csv"
SOURCE_FEATURE_ORDER = SOURCE_RUN_DIR / "feature_order.csv"
SOURCE_LABEL_SPLIT = SOURCE_RUN_DIR / "label_split_distribution.csv"
SOURCE_ONNX_SMOKE = SOURCE_RUN_DIR / "onnx_parity_smoke.csv"
SOURCE_TRAINING_SUMMARY = SOURCE_RUN_DIR / "training_summary.csv"
SOURCE_REPORT = SOURCE_STAGE_DIR / "03_reviews" / "run347C_cash_open_asymmetric_source_proxy_training.md"
SOURCE_SELECTION_STATUS = SOURCE_STAGE_DIR / "04_selected" / "selection_status.md"
SOURCE_STAGE_BRIEF = SOURCE_STAGE_DIR / "00_spec" / "stage_brief.md"
SOURCE_REVIEW_INDEX = SOURCE_STAGE_DIR / "03_reviews" / "review_index.md"

BRANCH_HANDOFF = RUN_DIR / "stage347_to_stage348_branch_handoff.csv"
COMPACT_SCORE_SUMMARY = RUN_DIR / "run347C_compact_score_summary.csv"
REVIEW_SEED_SURFACE = RUN_DIR / "stage348_review_seed_surface.csv"
NEGATIVE_MEMORY_SEED = RUN_DIR / "stage348_negative_memory_seed.csv"
NEXT_REVIEW_QUEUE = RUN_DIR / "run348B_review_queue.csv"
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
IDEA_REGISTRY = ROOT / "docs" / "registers" / "idea_registry.md"
NEGATIVE_RESULT_REGISTER = ROOT / "docs" / "registers" / "negative_result_register.md"
ROOT_CHANGELOG = ROOT / "CHANGELOG.md"
WORKSPACE_CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage348A_branch_stage347_to_cash_open_proxy_review.md"

SOURCE_INPUTS = [
    (SOURCE_FINAL_DECISION, "run347C final decision(347C 최종 결정)"),
    (SOURCE_GATE_AUDIT, "run347C gate audit(347C 게이트 감사)"),
    (SOURCE_SCORECARD, "proxy model scorecard(프록시 모델 점수표)"),
    (SOURCE_PROBE_QUEUE, "proxy probe priority queue(프록시 탐침 우선순위 대기열)"),
    (SOURCE_THRESHOLD_SCREEN, "proxy threshold screen(프록시 임계값 선별)"),
    (SOURCE_MODEL_MANIFEST, "model artifact manifest(모델 산출물 목록)"),
    (SOURCE_FEATURE_ORDER, "feature order(피처 순서)"),
    (SOURCE_LABEL_SPLIT, "label split distribution(라벨 분할 분포)"),
    (SOURCE_ONNX_SMOKE, "ONNX smoke record(온엑스 점검 기록)"),
    (SOURCE_TRAINING_SUMMARY, "training summary(학습 요약)"),
    (SOURCE_REPORT, "run347C report(347C 보고서)"),
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


def write_bom_text(path: Path, text: str) -> None:
    ensure_parent(path)
    with open(fs_path(path), "w", encoding="utf-8-sig", newline="\n") as handle:
        handle.write(text.rstrip() + "\n")


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


def append_text_once(path: Path, marker: str, text: str) -> None:
    current = read_text(path) if exists(path) else ""
    if marker in current:
        return
    next_text = f"{current.rstrip()}\n\n{text.strip()}\n" if current.strip() else text.strip() + "\n"
    write_bom_text(path, next_text)


def source_gate_passed() -> bool:
    _fields, rows = read_csv_rows(required(SOURCE_GATE_AUDIT))
    return bool(rows) and all(row.get("status") == "passed" for row in rows)


def to_float(row: Mapping[str, str], key: str) -> float:
    try:
        return float(row.get(key, ""))
    except (TypeError, ValueError):
        return 0.0


def build_compact_score_summary() -> list[dict[str, Any]]:
    _fields, rows = read_csv_rows(required(SOURCE_SCORECARD))
    compact: list[dict[str, Any]] = []
    for row in rows:
        head = row.get("head", "")
        split = row.get("split", "")
        if split not in {"validation", "test", "all"}:
            continue
        if head not in {"allocator", "long_head", "short_head"}:
            continue
        compact.append(
            {
                "model_family": row.get("model_family", ""),
                "head": head,
                "split": split,
                "rows": row.get("rows", ""),
                "positive_rows": row.get("positive_rows", ""),
                "long_rows": row.get("long_rows", ""),
                "short_rows": row.get("short_rows", ""),
                "predicted_positive_rows": row.get("predicted_positive_rows", ""),
                "predicted_long_rows": row.get("predicted_long_rows", ""),
                "predicted_short_rows": row.get("predicted_short_rows", ""),
                "macro_f1": row.get("macro_f1", ""),
                "f1_positive": row.get("f1_positive", ""),
                "precision_positive": row.get("precision_positive", ""),
                "recall_positive": row.get("recall_positive", ""),
                "short_recall": row.get("short_recall", ""),
                "long_recall": row.get("long_recall", ""),
                "review_use": "review_seed_only(검토 씨앗 전용)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(COMPACT_SCORE_SUMMARY, compact)
    return compact


def best_allocator_test(compact: Sequence[Mapping[str, Any]]) -> Mapping[str, Any]:
    candidates = [row for row in compact if row.get("head") == "allocator" and row.get("split") == "test"]
    if not candidates:
        return {}
    return max(candidates, key=lambda row: to_float(row, "macro_f1"))


def build_review_seed_surface() -> list[dict[str, Any]]:
    _fields, rows = read_csv_rows(required(SOURCE_PROBE_QUEUE))
    keep = [
        "queue_rank",
        "model_family",
        "split",
        "allocator_rule",
        "signal_rows",
        "predicted_long_rows",
        "predicted_short_rows",
        "teacher_hit_rows",
        "teacher_long_hit_rows",
        "teacher_short_hit_rows",
        "teacher_precision",
        "long_short_balance",
        "source_mt5_hit_expectancy_upper_bound",
    ]
    surface: list[dict[str, Any]] = []
    for row in rows[:10]:
        out = {key: row.get(key, "") for key in keep}
        out["seed_surface_role"] = "proxy_review_seed_not_selection(프록시 검토 씨앗, 선정 아님)"
        out["allowed_use"] = "triage_only_before_mt5_runtime_probe(MT5 런타임 탐침 전 분류 전용)"
        out["forbidden_use"] = "MT5_KPI_substitute_or_operating_claim(MT5 핵심 성과 지표 대체 또는 운영 주장)"
        out["claim_boundary"] = CLAIM_BOUNDARY
        surface.append(out)
    write_csv(REVIEW_SEED_SURFACE, surface)
    return surface


def build_handoff(final: Mapping[str, Any], compact: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    best_test = best_allocator_test(compact)
    rows = [
        {
            "handoff_id": "stage347_to_stage348_proxy_review",
            "source_stage_id": SOURCE_STAGE_ID,
            "new_stage_id": NEW_STAGE_ID,
            "source_run_id": PARENT_RUN_ID,
            "branch_run_id": RUN_ID,
            "superseded_planned_run_id": SUPERSEDED_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "source_rows": final.get("rows", ""),
            "feature_count": final.get("feature_count", ""),
            "trained_model_artifacts": final.get("trained_model_artifacts", ""),
            "onnx_allocator_smoke_passes": final.get("onnx_allocator_smoke_passes", ""),
            "long_oos_positive_labels": final.get("long_oos_positive_labels", ""),
            "best_test_allocator_family_by_macro_f1": best_test.get("model_family", ""),
            "best_test_allocator_macro_f1": best_test.get("macro_f1", ""),
            "best_test_allocator_predicted_short_rows": best_test.get("predicted_short_rows", ""),
            "best_test_allocator_predicted_long_rows": best_test.get("predicted_long_rows", ""),
            "branch_reason": "Stage347(347단계)이 설계/물질화/학습까지 안고 있어 무거워졌고, 다음 질문은 review/triage(검토/분류)이기 때문이다.",
            "effect": "Stage348(348단계)이 proxy score(프록시 점수)를 MT5 KPI(MT5 핵심 성과 지표)로 오해하지 않고 좁게 검토한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    write_csv(BRANCH_HANDOFF, rows)
    return rows


def build_negative_memory(final: Mapping[str, Any], compact: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    best_test = best_allocator_test(compact)
    rows = [
        {
            "memory_id": "NR-ST348A-LONG-OOS-MISSING",
            "source_run_id": PARENT_RUN_ID,
            "subject": "long OOS positive labels(롱 표본외 양성 라벨)",
            "finding": f"long_oos_positive_labels={final.get('long_oos_positive_labels', '')}",
            "judgment": "valid_constraint_not_model_failure(유효 제약, 모델 사망 아님)",
            "effect": "Stage348(348단계)에서는 long quality(롱 품질)를 운영 주장이나 후보 선정 근거로 쓰지 않는다.",
            "reopen_condition": "새 split(분할) 또는 label source(라벨 원천)에서 validation/test long positive(검증/테스트 롱 양성)가 생길 때",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "memory_id": "NR-ST348A-PROXY-NOT-MT5-KPI",
            "source_run_id": PARENT_RUN_ID,
            "subject": "proxy expected value(프록시 예상값)",
            "finding": "proxy queue(프록시 대기열)는 teacher reconstruction(교사 재구성)만 보여준다.",
            "judgment": "usable_for_signal_sanity_only(신호 점검 전용으로만 사용 가능)",
            "effect": "Stage348(348단계)는 MT5 runtime probe(MT5 런타임 탐침) 전에는 순수익/PF(수익 팩터) 주장을 만들지 않는다.",
            "reopen_condition": "runtime package(런타임 패키지)와 MT5 replay/probe(MT5 재생/탐침)가 같은 신호를 확인할 때",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "memory_id": "NR-ST348A-ALLOCATOR-TEST-FLAT-RISK",
            "source_run_id": PARENT_RUN_ID,
            "subject": "allocator test behavior(배분기 테스트 행동)",
            "finding": (
                "best_test_allocator="
                + str(best_test.get("model_family", ""))
                + ";macro_f1="
                + str(best_test.get("macro_f1", ""))
                + ";predicted_short="
                + str(best_test.get("predicted_short_rows", ""))
                + ";predicted_long="
                + str(best_test.get("predicted_long_rows", ""))
            ),
            "judgment": "requires_review_before_probe_packaging(탐침 포장 전 검토 필요)",
            "effect": "Stage348(348단계)는 all-split(전체 분할) 신호를 바로 runtime candidate(런타임 후보)로 올리지 않는다.",
            "reopen_condition": "test/validation split(테스트/검증 분할)에서 거래 공급과 hit quality(적중 품질)가 같이 확인될 때",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    write_csv(NEGATIVE_MEMORY_SEED, rows)
    return rows


def build_review_queue() -> list[dict[str, Any]]:
    rows = [
        {
            "queue_id": "q01_long_oos_gap_judgment",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "action": "Judge long OOS gap(롱 표본외 공백)을 selection blocker(선정 차단 조건)로 분리한다.",
            "effect": "long head(롱 헤드)를 폐기하지 않고, 운영 주장에 쓰지 않는 경계만 둔다.",
            "required_inputs": f"{rel(COMPACT_SCORE_SUMMARY)};{rel(NEGATIVE_MEMORY_SEED)}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "q02_short_carry_reconstruction_triage",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "action": "Check whether short carry(숏 기여) reconstruction(재구성)이 runtime probe seed(런타임 탐침 씨앗)로 쓸 수 있는지 본다.",
            "effect": "Stage347(347단계)의 긍정 단서를 short side(숏 방향) 중심으로 작게 검토한다.",
            "required_inputs": f"{rel(SOURCE_SCORECARD)};{rel(REVIEW_SEED_SURFACE)}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "q03_onnx_smoke_boundary",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P1",
            "action": "Separate ONNX smoke(온엑스 점검) from runtime parity(런타임 동등성).",
            "effect": "온엑스 파일이 있어도 MT5 실행 의미가 닫힌 것으로 말하지 않는다.",
            "required_inputs": f"{rel(SOURCE_MODEL_MANIFEST)};{rel(SOURCE_ONNX_SMOKE)}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "q04_proxy_to_mt5_probe_usability",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P1",
            "action": "Decide the smallest MT5 runtime probe(MT5 런타임 탐침) package shape if review allows it.",
            "effect": "다음 작업이 다시 거대한 학습으로 가지 않고, 좁은 runtime verification(런타임 검증) 후보만 남긴다.",
            "required_inputs": f"{rel(BRANCH_HANDOFF)};{rel(REVIEW_SEED_SURFACE)}",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    write_csv(NEXT_REVIEW_QUEUE, rows)
    return rows


def write_input_manifest() -> list[dict[str, Any]]:
    rows = []
    for path, label in SOURCE_INPUTS:
        path_exists = exists(path)
        rows.append(
            {
                "input_label": label,
                "input_path": rel(path),
                "exists": str(path_exists).lower(),
                "sha256": sha256_file(path) if path_exists else "",
                "copy_policy": "referenced_not_copied(참조만 하고 복사하지 않음)",
                "consumer": NEXT_RUN_ID,
                "effect": "Stage348(348단계)은 Stage347(347단계) 산출물을 가볍게 참조한다.",
            }
        )
    write_csv(INPUT_MANIFEST, rows)
    return rows


def write_stage_docs(final: Mapping[str, Any]) -> None:
    stage_brief = f"""# Stage348 Cash-Open Proxy Review(348단계 현금장 프록시 검토)

## Stage ID(단계 ID)

`{NEW_STAGE_ID}`

## Question(질문)

Can run347C proxy training(347C 프록시 학습)을 long OOS gap(롱 표본외 공백)과 short carry clue(숏 기여 단서)로 분류해, MT5 runtime probe(MT5 런타임 탐침)로 보낼 만한 가장 작은 seed(씨앗)만 남길 수 있는가?

## Source Inputs(원천 입력)

- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{PARENT_RUN_ID}`
- superseded_run(대체된 실행): `{SUPERSEDED_RUN_ID}`
- branch_run(분기 실행): `{RUN_ID}`
- source_rows(원천 행): `{final.get("rows", "")}`
- feature_count(피처 수): `{final.get("feature_count", "")}`
- trained_model_artifacts(학습 모델 산출물): `{final.get("trained_model_artifacts", "")}`
- onnx_smoke_passes(온엑스 점검 통과): `{final.get("onnx_allocator_smoke_passes", "")}`
- long_oos_positive_labels(롱 표본외 양성 라벨): `{final.get("long_oos_positive_labels", "")}`

## Scope(범위)

Stage348(348단계)은 review/triage(검토/분류) 전용이다. New training(새 학습), MT5 execution(MT5 실행), candidate selection(후보 선정)은 이 분기 실행의 범위가 아니다.

## Exit Condition(종료 조건)

run348B(348B 실행)는 proxy queue(프록시 대기열)를 `probe seed(탐침 씨앗)`, `repair condition(수리 조건)`, `negative memory(부정 기억)`, `blocked retry condition(차단 재시도 조건)` 중 하나로 분류해야 한다.

## Claim Boundary(주장 경계)

`{CLAIM_BOUNDARY}`
"""
    input_refs = f"""# Stage348 Input References(348단계 입력 참조)

## Primary Inputs(주 입력)

- final_decision(최종 결정): `{rel(SOURCE_FINAL_DECISION)}`
- scorecard(점수표): `{rel(SOURCE_SCORECARD)}`
- probe_queue(탐침 대기열): `{rel(SOURCE_PROBE_QUEUE)}`
- model_manifest(모델 목록): `{rel(SOURCE_MODEL_MANIFEST)}`
- onnx_smoke(온엑스 점검): `{rel(SOURCE_ONNX_SMOKE)}`

## Branch Outputs(분기 출력)

- branch_handoff(분기 인계): `{rel(BRANCH_HANDOFF)}`
- compact_score_summary(경량 점수 요약): `{rel(COMPACT_SCORE_SUMMARY)}`
- review_seed_surface(검토 씨앗 표면): `{rel(REVIEW_SEED_SURFACE)}`
- negative_memory_seed(부정 기억 씨앗): `{rel(NEGATIVE_MEMORY_SEED)}`
- review_queue(검토 대기열): `{rel(NEXT_REVIEW_QUEUE)}`

Effect(효과): Stage348(348단계)은 Stage347(347단계)의 무거운 학습 산출물을 재생산하지 않고 필요한 표만 읽는다.
"""
    selection = f"""# Stage348 Selection Status(348단계 선정 상태)

- active_stage(현재 단계): `{NEW_STAGE_ID}`
- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- selected_model(선정 모델): `none(없음)`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{PARENT_RUN_ID}`
- source_rows(원천 행): `{final.get("rows", "")}`
- trained_model_artifacts(학습 모델 산출물): `{final.get("trained_model_artifacts", "")}`
- onnx_allocator_smoke_passes(온엑스 배분기 점검 통과): `{final.get("onnx_allocator_smoke_passes", "")}`
- long_oos_status(롱 표본외 상태): `missing_positive_labels(양성 라벨 없음)`
- runtime_authority(런타임 권위): `not_claimed(주장 없음)`
- operating_promotion(운영 승격): `not_claimed(주장 없음)`
- Goal Achieve(목표 달성): `not_claimed(주장 없음)`

Effect(효과): Stage348(348단계)은 review/triage(검토/분류)만 담당하고 selection(선정)은 주장하지 않는다.
"""
    report = f"""# run348A Stage Branch From Stage347 Proxy Review(348A 단계 분기)

## Result(결과)

- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_run(다음 실행): `{NEXT_RUN_ID}`
- superseded_run(대체된 실행): `{SUPERSEDED_RUN_ID}`

Action(행동): Stage347(347단계)의 run347D review(347D 검토)를 Stage348(348단계) run348B(348B 실행)로 분기했다.
Effect(효과): Stage347(347단계)은 design/materialization/proxy training(설계/물질화/프록시 학습) 산출물 단계로 가볍게 멈추고, 검토는 새 stage(단계)에서 좁게 시작한다.

## Evidence(근거)

- source_final(원천 최종): `{rel(SOURCE_FINAL_DECISION)}`
- branch_handoff(분기 인계): `{rel(BRANCH_HANDOFF)}`
- compact_score_summary(경량 점수 요약): `{rel(COMPACT_SCORE_SUMMARY)}`
- review_queue(검토 대기열): `{rel(NEXT_REVIEW_QUEUE)}`
- gates(게이트): `{rel(GATE_AUDIT)}`

## Claim Boundary(주장 경계)

`{CLAIM_BOUNDARY}`
"""
    decision = f"""# 2026-06-01 Stage348A Branch Decision(348A 분기 결정)

- decision(결정): `{DECISION}`
- from(출발): `{SOURCE_STAGE_ID}` / `{PARENT_RUN_ID}`
- to(도착): `{NEW_STAGE_ID}` / `{NEXT_RUN_ID}`
- superseded_planned_run(대체된 예정 실행): `{SUPERSEDED_RUN_ID}`
- reason(이유): Stage347(347단계)이 design/materialization/proxy training(설계/물질화/프록시 학습)까지 안고 있어 무거워졌고, 다음 질문은 proxy review/triage(프록시 검토/분류)라는 별도 topic pivot(주제 전환)이기 때문이다.

Action(행동): Stage348(348단계)을 열고 run348B(348B 실행)를 review packet(검토 묶음)으로 둔다.
Effect(효과): run347C proxy training(347C 프록시 학습)은 source truth(원천 진실)로 보존하고, 검토는 새 stage(단계)에서 작게 시작한다.

claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
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

Stage348(348단계)은 Stage347(347단계)의 proxy training(프록시 학습) 산출물을 검토 전용으로 받았다. 다음 run348B(348B 실행)는 long OOS gap(롱 표본외 공백), short carry reconstruction(숏 기여 재구성), ONNX smoke boundary(온엑스 점검 경계), MT5 probe usability(MT5 탐침 활용 가능성)를 판정한다.

## Claim Boundary(주장 경계)

`{CLAIM_BOUNDARY}`

No new training(새 학습 없음), no MT5 execution(MT5 실행 없음), no candidate selection(후보 선정 없음), no forward pass(전진 통과 없음), no live readiness(실거래 준비 없음), no operating promotion(운영 승격 없음), no runtime authority(런타임 권위 없음), no Goal Achieve(목표 달성 없음).
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
    source_selection = f"""# Stage 347 Selection Status(347단계 선정 상태)

- active_stage_at_handoff(인계 당시 단계): `{SOURCE_STAGE_ID}`
- latest_completed_run(최근 완료 실행): `{PARENT_RUN_ID}`
- branched_to_stage(분기된 단계): `{NEW_STAGE_ID}`
- branch_run(분기 실행): `{RUN_ID}`
- next_active_run(다음 활성 실행): `{NEXT_RUN_ID}`
- superseded_planned_run(대체된 예정 실행): `{SUPERSEDED_RUN_ID}`
- selected_model(선정 모델): `none(없음)`
- trained_model_artifacts(학습 모델 산출물): `{final.get("trained_model_artifacts", "")}`
- onnx_allocator_smoke_passes(온엑스 배분기 점검 통과): `{final.get("onnx_allocator_smoke_passes", "")}`
- long_oos_status(롱 표본외 상태): `missing_positive_labels(양성 라벨 없음)`
- runtime_authority(런타임 권위): `not_claimed(주장 없음)`
- operating_promotion(운영 승격): `not_claimed(주장 없음)`
- Goal Achieve(목표 달성): `not_claimed(주장 없음)`

Effect(효과): Stage347(347단계)은 proxy training/screen(프록시 학습/선별) 산출물을 보존하고, review(검토)는 Stage348(348단계)로 넘겼다.
"""
    write_bom_text(STAGE_BRIEF, stage_brief)
    write_bom_text(STAGE_README, stage_brief)
    write_bom_text(INPUT_REFS, input_refs)
    write_bom_text(SELECTION_STATUS, selection)
    write_bom_text(REPORT_PATH, report)
    write_bom_text(DECISION_DOC, decision)
    write_bom_text(CURRENT_WORKING_STATE, current)
    write_bom_text(WORKSPACE_STATE, workspace)
    write_bom_text(ROOT_SELECTION_STATUS, selection)
    write_bom_text(SOURCE_SELECTION_STATUS, source_selection)
    write_bom_text(
        REVIEW_INDEX,
        f"""# Stage348 Review Index(348단계 검토 색인)

## run348A Stage Branch(348A 단계 분기)

- report(보고서): `{rel(REPORT_PATH)}`
- final_decision(최종 결정): `{rel(FINAL_DECISION)}`
- next_run(다음 실행): `{NEXT_RUN_ID}`
- effect(효과): Stage347(347단계)의 무거운 proxy training review(프록시 학습 검토)를 Stage348(348단계)로 분기했다.
""",
    )
    append_text_once(
        SOURCE_STAGE_BRIEF,
        "## run348A Proxy Review Branch(348A 프록시 검토 분기)",
        f"""## run348A Proxy Review Branch(348A 프록시 검토 분기)

- branch_run(분기 실행): `{RUN_ID}`
- next_stage(다음 단계): `{NEW_STAGE_ID}`
- next_run(다음 실행): `{NEXT_RUN_ID}`
- action(행동): run347D review(347D 검토)를 Stage348(348단계)로 넘겼다.
- effect(효과): Stage347(347단계)은 설계/물질화/학습 산출물까지만 보존하고, 검토 무게는 새 stage(단계)로 분리한다.
""",
    )
    append_text_once(
        SOURCE_REVIEW_INDEX,
        "run348A_branch_stage347_to_cash_open_proxy_review",
        f"""## run348A Proxy Review Branch(348A 프록시 검토 분기)

- from(출발): `{SOURCE_STAGE_ID}` / `{PARENT_RUN_ID}`
- to(도착): `{NEW_STAGE_ID}` / `{NEXT_RUN_ID}`
- effect(효과): Stage347(347단계)의 review(검토) 부담을 Stage348(348단계)로 분리했다.
""",
    )


def write_receipts(input_rows: Sequence[Mapping[str, Any]]) -> None:
    receipt_time = now_utc()
    source_inputs = [row["input_path"] for row in input_rows if row.get("exists") == "true"]
    write_json(
        STAGE_TRANSITION_RECEIPT,
        {
            "run_id": RUN_ID,
            "status": "passed",
            "source_stage_id": SOURCE_STAGE_ID,
            "new_stage_id": NEW_STAGE_ID,
            "source_run_id": PARENT_RUN_ID,
            "superseded_planned_run_id": SUPERSEDED_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "decision": DECISION,
            "effect": "Stage347 review(347단계 검토)를 Stage348(348단계)로 분기했다.",
            "created_at_utc": receipt_time,
        },
    )
    write_json(
        LINEAGE_RECEIPT,
        {
            "run_id": RUN_ID,
            "source_inputs": source_inputs,
            "producer": rel(Path("stage_pipelines/stage348/branch_stage347_to_cash_open_proxy_review_without_db.py")),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [
                rel(BRANCH_HANDOFF),
                rel(COMPACT_SCORE_SUMMARY),
                rel(REVIEW_SEED_SURFACE),
                rel(NEGATIVE_MEMORY_SEED),
                rel(NEXT_REVIEW_QUEUE),
                rel(REPORT_PATH),
                rel(FINAL_DECISION),
            ],
            "artifact_hashes": "recorded_in_artifact_registry(산출물 등록부에 기록)",
            "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(ARTIFACT_REGISTRY), rel(STAGE_LEDGER)],
            "availability": "tracked(추적됨)",
            "lineage_judgment": "connected_with_boundary(경계 포함 연결)",
            "claim_boundary": CLAIM_BOUNDARY,
            "created_at_utc": receipt_time,
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            "run_id": RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
            "training": "not_run",
            "mt5_execution": "not_run",
            "candidate_selection": "not_claimed",
            "forward_pass": "not_claimed",
            "live_readiness": "not_claimed",
            "operating_promotion": "not_claimed",
            "runtime_authority": "not_claimed",
            "goal_achieve": "not_claimed",
            "allowed_claim": "state_sync_stage_branch_and_proxy_review_handoff_only(상태 동기화 단계 분기와 프록시 검토 인계 전용)",
            "created_at_utc": receipt_time,
        },
    )


def write_gates(input_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    all_inputs_exist = all(row.get("exists") == "true" for row in input_rows)
    rows = [
        {
            "gate_id": "user_requested_stage_branch_recorded",
            "status": "passed",
            "evidence_path": rel(REPORT_PATH),
            "effect": "User request(사용자 요청)에 따라 Stage347(347단계)을 Stage348(348단계)로 분기했다.",
        },
        {
            "gate_id": "source_run347C_gates_passed",
            "status": "passed" if source_gate_passed() else "failed",
            "evidence_path": rel(SOURCE_GATE_AUDIT),
            "effect": "분기 원천인 run347C(347C 실행)의 gate(게이트)를 확인했다.",
        },
        {
            "gate_id": "input_manifest_all_sources_visible",
            "status": "passed" if all_inputs_exist else "failed",
            "evidence_path": rel(INPUT_MANIFEST),
            "effect": "Stage348(348단계)이 참조할 원천 산출물 가시성을 확인했다.",
        },
        {
            "gate_id": "new_stage_structure_created",
            "status": "passed" if exists(STAGE_BRIEF) and exists(INPUT_REFS) and exists(SELECTION_STATUS) else "failed",
            "evidence_path": rel(STAGE_BRIEF),
            "effect": "Stage348(348단계)의 필수 폴더와 문서를 만들었다.",
        },
        {
            "gate_id": "handoff_and_review_queue_written",
            "status": "passed" if exists(BRANCH_HANDOFF) and exists(NEXT_REVIEW_QUEUE) else "failed",
            "evidence_path": f"{rel(BRANCH_HANDOFF)};{rel(NEXT_REVIEW_QUEUE)}",
            "effect": "다음 run348B(348B 실행)의 검토 범위를 작게 만들었다.",
        },
        {
            "gate_id": "state_sync_audit",
            "status": "passed" if exists(WORKSPACE_STATE) and exists(CURRENT_WORKING_STATE) else "failed",
            "evidence_path": rel(WORKSPACE_STATE),
            "effect": "current truth(현재 진실)를 Stage348(348단계)로 동기화했다.",
        },
        {
            "gate_id": "final_claim_guard",
            "status": "passed",
            "evidence_path": rel(CLAIM_RECEIPT),
            "effect": "selection/promotion/runtime authority/Goal(선정/승격/런타임 권위/목표)을 주장하지 않았다.",
        },
        {
            "gate_id": "required_gate_coverage_audit_written",
            "status": "passed",
            "evidence_path": rel(GATE_AUDIT),
            "effect": "required gate coverage audit(필수 게이트 커버리지 감사)를 기록했다.",
        },
    ]
    gate_rows = [{**row, "claim_boundary": CLAIM_BOUNDARY} for row in rows]
    write_csv(GATE_AUDIT, gate_rows, ["gate_id", "status", "evidence_path", "effect", "claim_boundary"])
    return gate_rows


def ledger_rows(final: Mapping[str, Any], gate_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
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
        "source_package_run_id": SOURCE_PACKAGE_RUN_ID,
        "rows": final.get("rows", ""),
        "feature_count": final.get("feature_count", ""),
        "candidate_model_id": "none(없음)",
    }
    return [
        {
            **base,
            "ledger_row_id": f"{RUN_ID}__Tier A",
            "subrun_id": "Tier A",
            "view": "Tier A separate(Tier A 분리)",
            "record_view": "Tier A separate(Tier A 분리)",
            "tier": "Tier A",
            "tier_scope": "Tier A",
            "metric_scope": "stage_branch_handoff_proxy_training_review",
            "kpi_scope": "stage_branch_handoff_proxy_training_review",
            "primary_kpi": f"rows={final.get('rows', '')};models={final.get('trained_model_artifacts', '')};onnx_smoke_passes={final.get('onnx_allocator_smoke_passes', '')}",
            "guardrail_kpi": f"long_oos_positive_labels={final.get('long_oos_positive_labels', '')};no_mt5_execution",
            "external_verification_status": "out_of_scope_by_claim(주장 범위 밖)",
            "result_status": "stage_branch_opened_no_selection(단계 분기 완료, 선정 없음)",
            "notes": "Stage347(347단계) proxy review(프록시 검토)를 Stage348(348단계)로 분리했다.",
        },
        {
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
            "notes": "Tier B(티어 B)는 이번 branch(분기) 범위에 없다.",
        },
        {
            **base,
            "ledger_row_id": f"{RUN_ID}__Tier A+B",
            "subrun_id": "Tier A+B",
            "view": "Tier A+B combined(Tier A+B 합산)",
            "record_view": "Tier A+B combined(Tier A+B 합산)",
            "tier": "Tier A+B",
            "tier_scope": "Tier A+B",
            "metric_scope": "same_as_tier_a_until_tier_b_available",
            "kpi_scope": "same_as_tier_a_until_tier_b_available",
            "primary_kpi": "same_as_tier_a_until_tier_b_available",
            "guardrail_kpi": "Tier B missing_required(Tier B 필수 누락)",
            "external_verification_status": "out_of_scope_by_claim(주장 범위 밖)",
            "result_status": "same_as_tier_a_until_tier_b_available",
            "notes": "combined(합산)는 Tier B(티어 B) 부재 때문에 Tier A(티어 A) 경계와 같다.",
        },
    ]


def write_registries(final: Mapping[str, Any], gate_rows: Sequence[Mapping[str, Any]]) -> None:
    rows = ledger_rows(final, gate_rows)
    write_csv(STAGE_LEDGER, rows, LEDGER_COLUMNS)
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], rows)
    run_row = {
        "run_id": RUN_ID,
        "stage_id": NEW_STAGE_ID,
        "lane": "state_sync_stage_branch(상태 동기화 단계 분기)",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(FINAL_DECISION),
        "notes": "Stage347 review(347단계 검토)를 Stage348(348단계)로 분기, no selection(선정 없음).",
        "family": "state_sync(상태 동기화)",
        "primary_report": rel(REPORT_PATH),
        "run_number": RUN_NUMBER,
        "date": TODAY,
        "decision": DECISION,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "rows": final.get("rows", ""),
        "gate_passes": sum(1 for row in gate_rows if row.get("status") == "passed"),
        "gate_total": len(gate_rows),
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "primary_artifact": rel(FINAL_DECISION),
        "candidate_model_id": "none(없음)",
        "result_status": "stage_branch_opened_no_selection(단계 분기 완료, 선정 없음)",
        "feature_count": final.get("feature_count", ""),
        "source_package_run_id": SOURCE_PACKAGE_RUN_ID,
    }
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], [run_row])
    artifact_paths = [
        FINAL_DECISION,
        RUN_MANIFEST,
        GATE_AUDIT,
        BRANCH_HANDOFF,
        COMPACT_SCORE_SUMMARY,
        REVIEW_SEED_SURFACE,
        NEGATIVE_MEMORY_SEED,
        NEXT_REVIEW_QUEUE,
        INPUT_MANIFEST,
        STAGE_TRANSITION_RECEIPT,
        LINEAGE_RECEIPT,
        CLAIM_RECEIPT,
        REPORT_PATH,
        DECISION_DOC,
        STAGE_BRIEF,
        INPUT_REFS,
        SELECTION_STATUS,
    ]
    artifact_rows = [
        {
            "artifact_id": f"{RUN_ID}__{path.stem}",
            "artifact_type": f"{path.stem}(산출물)",
            "path": rel(path),
            "artifact_path": rel(path),
            "sha256": sha256_file(path),
            "stage_id": NEW_STAGE_ID,
            "run_id": RUN_ID,
            "created_at": TODAY,
            "created_at_utc": now_utc(),
            "claim_boundary": CLAIM_BOUNDARY,
            "notes": "Stage348 branch artifact(348단계 분기 산출물).",
        }
        for path in artifact_paths
        if exists(path)
    ]
    append_or_replace_csv(ARTIFACT_REGISTRY, ["artifact_id"], artifact_rows)


def write_register_notes() -> None:
    marker = f"run348A {RUN_ID}"
    append_text_once(
        IDEA_REGISTRY,
        marker,
        f"""## {TODAY} Stage348 Proxy Review Triage Seed(프록시 검토 분류 씨앗)

- idea(아이디어): run347C proxy training(347C 프록시 학습)을 바로 후보로 올리지 않고, long OOS gap(롱 표본외 공백)과 short carry reconstruction(숏 기여 재구성)을 분리해 가장 작은 MT5 probe seed(MT5 탐침 씨앗)만 남긴다.
- source(원천): `{PARENT_RUN_ID}`
- next_run(다음 실행): `{NEXT_RUN_ID}`
- effect(효과): Stage347(347단계)의 무거운 학습 산출물을 다시 끌고 다니지 않고 review/triage(검토/분류) 질문으로 전환한다.
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
    )
    append_text_once(
        NEGATIVE_RESULT_REGISTER,
        marker,
        f"""## {TODAY} run348A Proxy Review Constraint Memory(프록시 검토 제약 기억)

- source_run(원천 실행): `{PARENT_RUN_ID}`
- constraint(제약): long OOS positive labels(롱 표본외 양성 라벨)이 `0`이라 long quality(롱 품질)를 OOS(`out-of-sample`, 표본외) 근거로 주장할 수 없다.
- proxy_boundary(프록시 경계): proxy expected value(프록시 예상값)는 signal sanity check(신호 점검)이고 MT5 KPI(MT5 핵심 성과 지표)가 아니다.
- effect(효과): run348B(348B 실행)는 선정(selection, 선정)이 아니라 review/triage(검토/분류)로만 닫아야 한다.
- evidence(근거): `{rel(NEGATIVE_MEMORY_SEED)}`
""",
    )


def write_changelog() -> None:
    marker = f"run348A {RUN_ID}"
    text = f"""## {TODAY} run348A Stage Branch(348A 단계 분기)

- action(행동): Stage347(347단계)의 run347D review(347D 검토)를 Stage348(348단계) run348B로 분기했다.
- effect(효과): Stage347(347단계)은 proxy training(프록시 학습) 산출물까지만 보존하고, review/triage(검토/분류)는 새 stage(단계)에서 작게 시작한다.
- boundary(경계): training/MT5 execution/selection/runtime authority/Goal Achieve(학습/MT5 실행/선정/런타임 권위/목표 달성)는 주장하지 않는다.
"""
    append_text_once(WORKSPACE_CHANGELOG, marker, text)
    append_text_once(ROOT_CHANGELOG, marker, text)


def write_final(final: Mapping[str, Any], compact: Sequence[Mapping[str, Any]], gate_rows: Sequence[Mapping[str, Any]]) -> None:
    best_test = best_allocator_test(compact)
    payload = {
        "run_id": RUN_ID,
        "stage_id": NEW_STAGE_ID,
        "parent_stage_id": SOURCE_STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "superseded_planned_run_id": SUPERSEDED_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "claim_boundary": CLAIM_BOUNDARY,
        "source_rows": final.get("rows", ""),
        "source_feature_count": final.get("feature_count", ""),
        "source_trained_model_artifacts": final.get("trained_model_artifacts", ""),
        "source_onnx_allocator_smoke_passes": final.get("onnx_allocator_smoke_passes", ""),
        "source_long_oos_positive_labels": final.get("long_oos_positive_labels", ""),
        "best_test_allocator_family_by_macro_f1": best_test.get("model_family", ""),
        "best_test_allocator_macro_f1": best_test.get("macro_f1", ""),
        "best_test_allocator_predicted_short_rows": best_test.get("predicted_short_rows", ""),
        "best_test_allocator_predicted_long_rows": best_test.get("predicted_long_rows", ""),
        "gate_passes": sum(1 for row in gate_rows if row.get("status") == "passed"),
        "gate_total": len(gate_rows),
        "training": "not_run",
        "mt5_execution": "not_run",
        "candidate_selection": "not_claimed",
        "forward_passed": "not_claimed",
        "live_readiness": "not_claimed",
        "operating_promotion": "not_claimed",
        "runtime_authority": "not_claimed",
        "goal_achieve": "not_claimed",
    }
    write_json(FINAL_DECISION, payload)


def write_manifest() -> None:
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "stage_id": NEW_STAGE_ID,
            "parent_stage_id": SOURCE_STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "superseded_planned_run_id": SUPERSEDED_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "producer": rel(Path("stage_pipelines/stage348/branch_stage347_to_cash_open_proxy_review_without_db.py")),
            "inputs": [rel(path) for path, _label in SOURCE_INPUTS],
            "outputs": [
                rel(INPUT_MANIFEST),
                rel(BRANCH_HANDOFF),
                rel(COMPACT_SCORE_SUMMARY),
                rel(REVIEW_SEED_SURFACE),
                rel(NEGATIVE_MEMORY_SEED),
                rel(NEXT_REVIEW_QUEUE),
                rel(STAGE_TRANSITION_RECEIPT),
                rel(LINEAGE_RECEIPT),
                rel(CLAIM_RECEIPT),
                rel(GATE_AUDIT),
                rel(FINAL_DECISION),
                rel(REPORT_PATH),
                rel(DECISION_DOC),
                rel(STAGE_BRIEF),
                rel(INPUT_REFS),
                rel(SELECTION_STATUS),
            ],
            "claim_boundary": CLAIM_BOUNDARY,
            "created_at_utc": now_utc(),
        },
    )


def validate(gate_rows: Sequence[Mapping[str, Any]]) -> None:
    required_outputs = [
        STAGE_BRIEF,
        INPUT_REFS,
        INPUT_MANIFEST,
        SELECTION_STATUS,
        REPORT_PATH,
        REVIEW_INDEX,
        DECISION_DOC,
        FINAL_DECISION,
        RUN_MANIFEST,
        GATE_AUDIT,
        WORKSPACE_STATE,
        CURRENT_WORKING_STATE,
        BRANCH_HANDOFF,
        COMPACT_SCORE_SUMMARY,
        REVIEW_SEED_SURFACE,
        NEGATIVE_MEMORY_SEED,
        NEXT_REVIEW_QUEUE,
    ]
    missing = [rel(path) for path in required_outputs if not exists(path)]
    if missing:
        raise FileNotFoundError("missing generated output(생성 출력 누락): " + ", ".join(missing))
    if any(row.get("status") != "passed" for row in gate_rows):
        raise RuntimeError("run348A required gate audit failed(348A 필수 게이트 감사 실패)")
    for label, path in [
        ("workspace", WORKSPACE_STATE),
        ("current", CURRENT_WORKING_STATE),
        ("selection", SELECTION_STATUS),
        ("root_selection", ROOT_SELECTION_STATUS),
    ]:
        if NEW_STAGE_ID not in read_text(path):
            raise RuntimeError(f"{label} missing active Stage348(348단계 누락)")
    final = read_json(FINAL_DECISION)
    forbidden = ["operating_promotion", "runtime_authority", "goal_achieve"]
    for key in forbidden:
        if final.get(key) != "not_claimed":
            raise RuntimeError(f"forbidden claim raised(금지 주장 발생): {key}={final.get(key)}")


def main() -> None:
    for path in [
        NEW_STAGE_DIR / "00_spec",
        NEW_STAGE_DIR / "01_inputs",
        NEW_STAGE_DIR / "02_runs",
        RUN_DIR,
        REVIEW_DIR,
        NEW_STAGE_DIR / "04_selected",
        DECISION_DOC.parent,
    ]:
        os.makedirs(fs_path(path), exist_ok=True)
    for path, _label in SOURCE_INPUTS:
        required(path)
    final = read_json(required(SOURCE_FINAL_DECISION))
    compact = build_compact_score_summary()
    input_rows = write_input_manifest()
    build_handoff(final, compact)
    build_review_seed_surface()
    build_negative_memory(final, compact)
    build_review_queue()
    write_stage_docs(final)
    write_receipts(input_rows)
    gate_rows = write_gates(input_rows)
    write_final(final, compact, gate_rows)
    write_manifest()
    write_registries(final, gate_rows)
    write_register_notes()
    write_changelog()
    validate(gate_rows)
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "new_stage_id": NEW_STAGE_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "next_run_id": NEXT_RUN_ID,
                "gate_passes": sum(1 for row in gate_rows if row["status"] == "passed"),
                "gate_total": len(gate_rows),
                "source_rows": final.get("rows", ""),
                "source_onnx_allocator_smoke_passes": final.get("onnx_allocator_smoke_passes", ""),
                "source_long_oos_positive_labels": final.get("long_oos_positive_labels", ""),
                "goal_achieve": "not_claimed",
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
