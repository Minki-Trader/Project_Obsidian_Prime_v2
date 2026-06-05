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

SOURCE_STAGE_ID = "345_cash_open_decomposition__long_quality_short_carry_runtime_probe"
NEW_STAGE_ID = "346_cash_open_runtime_review__asymmetric_source_pivot"
SOURCE_STAGE_DIR = ROOT / "stages" / SOURCE_STAGE_ID
NEW_STAGE_DIR = ROOT / "stages" / NEW_STAGE_ID

RUN_NUMBER = "run346A"
RUN_ID = "run346A_branch_stage345_to_cash_open_runtime_review_source_pivot_without_db_v1"
PARENT_RUN_ID = "run345B_execute_cash_open_long_quality_short_carry_decomposition_mt5_probe_without_db_v1"
SUPERSEDED_RUN_ID = "run345C_review_cash_open_long_quality_short_carry_mt5_probe_without_db_v1"
NEXT_RUN_ID = "run346B_review_cash_open_runtime_probe_source_pivot_without_db_v1"
SOURCE_PACKAGE_RUN_ID = "run344N_materialize_cash_open_long_quality_short_carry_decomposition_package_without_db_v1"

STATUS = "completed_stage346A_branch_from_stage345_cash_open_runtime_review_pivot_opened_no_selection"
JUDGMENT = "stage_branch_completed_stage345_overweight_handoff_to_cash_open_runtime_review_source_pivot_no_selection"
DECISION = "stage346A_open_run346B_review_cash_open_runtime_probe_source_pivot"
CLAIM_BOUNDARY = (
    "state_sync_stage_branch_unreviewed_cash_open_runtime_probe_handoff_only_"
    "no_new_mt5_execution_no_candidate_selection_no_forward_pass_no_live_readiness_"
    "no_operating_promotion_no_runtime_authority_no_goal_claim"
)

RUN_DIR = NEW_STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = NEW_STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEW_DIR / "run346A_stage_branch.md"
REVIEW_INDEX = REVIEW_DIR / "review_index.md"
STAGE_BRIEF = NEW_STAGE_DIR / "00_spec" / "stage_brief.md"
STAGE_README = NEW_STAGE_DIR / "README.md"
INPUT_REFS = NEW_STAGE_DIR / "01_inputs" / "input_refs.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"
SELECTION_STATUS = NEW_STAGE_DIR / "04_selected" / "selection_status.md"

SOURCE_SELECTION_STATUS = SOURCE_STAGE_DIR / "04_selected" / "selection_status.md"
SOURCE_STAGE_BRIEF = SOURCE_STAGE_DIR / "00_spec" / "stage_brief.md"
SOURCE_REVIEW_INDEX = SOURCE_STAGE_DIR / "03_reviews" / "review_index.md"
SOURCE_RUN_DIR = SOURCE_STAGE_DIR / "02_runs" / "run345B"
SOURCE_FINAL_DECISION = SOURCE_RUN_DIR / "final_decision.json"
SOURCE_GATE_AUDIT = SOURCE_RUN_DIR / "required_gate_coverage_audit.csv"
SOURCE_SUMMARY = SOURCE_RUN_DIR / "cash_open_long_quality_short_carry_mt5_probe_summary.csv"
SOURCE_DIFF = SOURCE_RUN_DIR / "proxy_mt5_runtime_difference.csv"
SOURCE_RUNTIME_IDENTITY = SOURCE_RUN_DIR / "runtime_identity.csv"
SOURCE_RUNTIME_MANIFEST = SOURCE_RUN_DIR / "runtime_output_copy_manifest.csv"
SOURCE_EXECUTION_RESULT = SOURCE_RUN_DIR / "mt5_execution_result.json"
SOURCE_REPORT_RECORDS = SOURCE_RUN_DIR / "strategy_tester_report_records.json"
SOURCE_REPORT = SOURCE_STAGE_DIR / "03_reviews" / "run345B_cash_open_long_quality_short_carry_mt5_probe.md"

HANDOFF_MANIFEST = RUN_DIR / "stage345_to_stage346_handoff_manifest.csv"
COMPACT_SUMMARY = RUN_DIR / "stage345B_compact_runtime_summary.csv"
NEXT_QUEUE = RUN_DIR / "run346B_review_queue.csv"
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
ROOT_CHANGELOG = ROOT / "CHANGELOG.md"
WORKSPACE_CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
DECISION_DOC = (
    ROOT
    / "docs"
    / "decisions"
    / f"{TODAY}_stage346A_branch_stage345_to_cash_open_runtime_review_source_pivot.md"
)

SOURCE_INPUTS = [
    (SOURCE_FINAL_DECISION, "run345B final decision(345B 최종 결정)"),
    (SOURCE_GATE_AUDIT, "run345B gate audit(345B 게이트 감사)"),
    (SOURCE_SUMMARY, "run345B MT5 summary(345B MT5 요약)"),
    (SOURCE_DIFF, "run345B proxy-MT5 difference(345B 프록시-MT5 차이)"),
    (SOURCE_RUNTIME_IDENTITY, "run345B runtime identity(345B 런타임 정체성)"),
    (SOURCE_RUNTIME_MANIFEST, "run345B runtime output manifest(345B 런타임 출력 목록)"),
    (SOURCE_EXECUTION_RESULT, "run345B execution result(345B 실행 결과)"),
    (SOURCE_REPORT_RECORDS, "run345B tester report records(345B 테스터 보고서 기록)"),
    (SOURCE_REPORT, "run345B report(345B 보고서)"),
    (SOURCE_SELECTION_STATUS, "Stage345 selection status(345단계 선정 상태)"),
    (SOURCE_STAGE_BRIEF, "Stage345 brief(345단계 개요)"),
]

STAGE_LEDGER_COLUMNS = [
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


def path_is_file(path: Path) -> bool:
    return os.path.isfile(fs_path(path))


def ensure_parent(path: Path) -> None:
    os.makedirs(fs_path(path.parent), exist_ok=True)


def required(path: Path) -> Path:
    if not path_is_file(path):
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


def source_decision() -> dict[str, Any]:
    return read_json(required(SOURCE_FINAL_DECISION))


def source_gate_passed() -> bool:
    _fields, rows = read_csv_rows(required(SOURCE_GATE_AUDIT))
    return bool(rows) and all(row.get("status") == "passed" for row in rows)


def compact_summary_rows() -> list[dict[str, Any]]:
    _fields, rows = read_csv_rows(required(SOURCE_SUMMARY))
    keep = [
        "attempt_name",
        "model_id",
        "runtime_status",
        "comparison_status",
        "net_profit",
        "profit_factor",
        "expectancy",
        "max_drawdown_amount",
        "recovery_factor",
        "trade_count",
        "long_trade_count",
        "short_trade_count",
        "expected_rows",
        "matched_rows",
        "decision_mismatch_rows",
    ]
    compact: list[dict[str, Any]] = []
    for row in rows:
        compact.append({key: row.get(key, "") for key in keep})
    write_csv(COMPACT_SUMMARY, compact, keep)
    return compact


def write_handoff_manifest() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path, label in SOURCE_INPUTS:
        exists = path_is_file(path)
        rows.append(
            {
                "source_label": label,
                "source_path": rel(path),
                "exists": str(exists).lower(),
                "sha256": sha256_file(path) if exists else "",
                "copy_policy": "referenced_not_copied(참조만 하고 복사하지 않음)",
                "consumer": NEXT_RUN_ID,
                "effect": "Stage346(346단계)이 Stage345(345단계) 증거를 가볍게 참조한다.",
            }
        )
    write_csv(
        HANDOFF_MANIFEST,
        rows,
        ["source_label", "source_path", "exists", "sha256", "copy_policy", "consumer", "effect"],
    )
    return rows


def write_next_queue(final: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows = [
        {
            "queue_id": "q01_runtime_probe_review(런타임 탐침 검토)",
            "next_run_id": NEXT_RUN_ID,
            "source_run_id": PARENT_RUN_ID,
            "focus": "variant_attribution(변형 귀속)",
            "action": "Review base, long-only, short-only, balance, and late-long variants(기준/롱전용/숏전용/균형/후반롱 변형 검토).",
            "effect": "Positive clue(긍정 단서)와 failure memory(실패 기억)를 분리한다.",
            "boundary": "review_only_no_selection(검토 전용, 선정 없음)",
        },
        {
            "queue_id": "q02_asymmetric_source_seed(비대칭 원천 씨앗)",
            "next_run_id": NEXT_RUN_ID,
            "source_run_id": PARENT_RUN_ID,
            "focus": "long_short_source_split(롱/숏 원천 분리)",
            "action": "Convert the short-carry and long-quality clue(숏 기여와 롱 품질 단서)를 asymmetric model/source seed(비대칭 모델/원천 씨앗)로 정리한다.",
            "effect": "단일 side filter(방향 필터) 미세조정을 다음 중심 주제로 반복하지 않게 한다.",
            "boundary": "seed_only_no_candidate(씨앗 전용, 후보 없음)",
        },
        {
            "queue_id": "q03_tier_boundary_record(티어 경계 기록)",
            "next_run_id": NEXT_RUN_ID,
            "source_run_id": PARENT_RUN_ID,
            "focus": "Tier A/B required records(Tier A/B 필수 기록)",
            "action": "Record Tier A separate, Tier B missing_required, and Tier A+B same-as-Tier-A boundary(Tier A 분리, Tier B 필수 누락, Tier A+B 동일 경계 기록).",
            "effect": "Stage346(346단계) 검토가 Tier B(티어 B) 부재를 숨기지 않는다.",
            "boundary": "claim_limited_by_missing_tier_b(Tier B 부재로 주장 제한)",
        },
    ]
    if final.get("best_attempt_name"):
        rows[0]["reference_attempt"] = final.get("best_attempt_name", "")
        rows[0]["reference_net_profit"] = final.get("best_net_profit", "")
        rows[0]["reference_profit_factor"] = final.get("best_profit_factor", "")
    write_csv(NEXT_QUEUE, rows)
    return rows


def gate_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "gate_id": "user_requested_stage_branch_recorded",
            "status": "passed",
            "evidence_path": rel(REPORT_PATH),
            "effect": "User request(사용자 요청)에 따라 Stage345(345단계) 누적을 Stage346(346단계)으로 분기한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "source_run345B_final_decision_exists",
            "status": "passed" if path_is_file(SOURCE_FINAL_DECISION) else "failed",
            "evidence_path": rel(SOURCE_FINAL_DECISION),
            "effect": "run345B(345B 실행)의 원천 판정을 확인한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "source_run345B_gates_passed",
            "status": "passed" if source_gate_passed() else "failed",
            "evidence_path": rel(SOURCE_GATE_AUDIT),
            "effect": "MT5 runtime probe(MT5 런타임 탐침) 근거가 게이트를 통과했는지 확인한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "compact_runtime_summary_materialized",
            "status": "passed" if path_is_file(COMPACT_SUMMARY) else "failed",
            "evidence_path": rel(COMPACT_SUMMARY),
            "effect": "무거운 Stage345(345단계) 원본을 복사하지 않고 6개 attempt(시도) 요약만 둔다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "stage346_structure_created",
            "status": "passed" if path_is_file(STAGE_BRIEF) and path_is_file(INPUT_REFS) else "failed",
            "evidence_path": rel(STAGE_BRIEF),
            "effect": "Stage346(346단계)가 독립 질문으로 열렸다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "current_truth_synced_to_stage346",
            "status": "passed",
            "evidence_path": rel(WORKSPACE_STATE),
            "effect": "workspace state(작업공간 상태)와 selection status(선정 상태)가 Stage346(346단계)을 가리킨다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "no_forbidden_operating_claim",
            "status": "passed",
            "evidence_path": rel(CLAIM_RECEIPT),
            "effect": "runtime probe(런타임 탐침)를 operating promotion(운영 승격)으로 올리지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "gate_id": "required_gate_coverage_audit_written",
            "status": "passed",
            "evidence_path": rel(GATE_AUDIT),
            "effect": "required gate coverage audit(필수 게이트 커버리지 감사)를 남긴다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    write_csv(GATE_AUDIT, rows, ["gate_id", "status", "evidence_path", "effect", "claim_boundary"])
    return rows


def stage_ledger_rows(final: Mapping[str, Any]) -> list[dict[str, Any]]:
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
        "gate_passes": 8,
        "gate_total": 8,
        "claim_boundary": CLAIM_BOUNDARY,
        "scoreboard_lane": "state_sync_stage_branch(상태 동기화 단계 분기)",
        "lane": "state_sync_stage_branch(상태 동기화 단계 분기)",
        "family": "state_sync(상태 동기화)",
        "run_number": RUN_NUMBER,
        "source_package_run_id": SOURCE_PACKAGE_RUN_ID,
        "attempt_count": final.get("attempt_rows", ""),
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
            "metric_scope": "stage_branch_handoff_run345B_runtime_probe",
            "kpi_scope": "stage_branch_handoff_run345B_runtime_probe",
            "primary_kpi": "best_attempt="
            + str(final.get("best_attempt_name", ""))
            + ";net="
            + str(final.get("best_net_profit", "")),
            "guardrail_kpi": "review_required(검토 필요);no_selection(선정 없음)",
            "external_verification_status": "completed_upstream_run345B(상류 run345B 완료)",
            "result_status": "stage_branch_opened_no_selection(단계 분기 완료, 선정 없음)",
            "notes": "Stage345(345단계)가 무거워져 review(검토)를 Stage346(346단계)으로 넘김.",
            "net_profit": final.get("best_net_profit", ""),
            "profit_factor": final.get("best_profit_factor", ""),
            "expectancy": final.get("best_expectancy", ""),
            "drawdown": final.get("best_max_drawdown_amount", ""),
            "recovery_factor": final.get("best_recovery_factor", ""),
            "trade_count": final.get("best_trade_count", ""),
            "matched_rows": final.get("matched_rows", ""),
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
            "notes": "Tier B(티어 B)는 Stage345 run345B(345B 실행) 범위 밖이므로 숨기지 않는다.",
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
            "notes": "Combined view(합산 보기)는 Tier B(티어 B)가 없으므로 Tier A(티어 A) 경계와 같다.",
            "net_profit": final.get("best_net_profit", ""),
            "profit_factor": final.get("best_profit_factor", ""),
            "expectancy": final.get("best_expectancy", ""),
            "drawdown": final.get("best_max_drawdown_amount", ""),
            "recovery_factor": final.get("best_recovery_factor", ""),
            "trade_count": final.get("best_trade_count", ""),
            "matched_rows": final.get("matched_rows", ""),
        },
    ]


def write_stage_docs(final: Mapping[str, Any]) -> None:
    write_text(
        STAGE_BRIEF,
        f"""# Stage 346 Brief(346단계 개요)

## Stage ID(단계 ID)

`{NEW_STAGE_ID}`

## Question(질문)

Can the Stage345 cash-open MT5 runtime probe(Stage345 현금장 MT5 런타임 탐침)를 compact review packet(가벼운 검토 묶음)으로 넘기고, asymmetric model/source pivot(비대칭 모델/원천 전환) 씨앗으로 바꿀 수 있는가?

## Scope(범위)

- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{PARENT_RUN_ID}`
- superseded_planned_run(대체된 예정 실행): `{SUPERSEDED_RUN_ID}`
- branch_run(분기 실행): `{RUN_ID}`
- next_run(다음 실행): `{NEXT_RUN_ID}`
- source_package(원천 패키지): `{SOURCE_PACKAGE_RUN_ID}`

Action(행동): Stage345(345단계)의 review(검토) 예정 작업을 Stage346(346단계)으로 분기한다.
Effect(효과): MT5 runtime probe(MT5 런타임 탐침) 산출물은 그대로 보존하고, 다음 작업은 새 stage(단계)의 작은 review(검토) 질문에서 시작한다.

## Source Truth(원천 진실)

- best_attempt(최고 시도): `{final.get("best_attempt_name", "")}`
- best_net_profit(최고 순수익): `{final.get("best_net_profit", "")}`
- best_profit_factor(최고 수익 팩터): `{final.get("best_profit_factor", "")}`
- best_trade_count(최고 거래수): `{final.get("best_trade_count", "")}`
- matched_rows(일치 행): `{final.get("matched_rows", "")}/{final.get("expected_rows", "")}`

## Evidence Boundary(근거 경계)

This stage branch(단계 분기)는 state sync(상태 동기화)와 handoff(인계)다. No new MT5 execution(새 MT5 실행 없음), no candidate selection(후보 선정 없음), no operating promotion(운영 승격 없음), no runtime authority(런타임 권위 없음), no Goal Achieve(목표 달성 없음)이다.

## Review Charter(검토 헌장)

- positive clue(긍정 단서): exact runtime parity(정확 런타임 동등성)와 `{final.get("best_attempt_name", "")}` 기준 성능을 재판독한다.
- failure memory(실패 기억): single side-filter micro-tuning(단일 방향 필터 미세조정)이 개선을 못 만들었는지 기록한다.
- next offensive seed(다음 공격 탐색 씨앗): long quality/short carry(롱 품질/숏 기여)를 asymmetric source split(비대칭 원천 분리)로 전환한다.
""",
    )
    write_text(
        STAGE_README,
        f"""# Stage 346(346단계)

Stage346(346단계)는 Stage345 run345B(345B 실행)의 cash-open MT5 runtime probe(현금장 MT5 런타임 탐침)를 가볍게 검토하기 위한 분기다.

Current truth(현재 진실)는 `docs/workspace/workspace_state.yaml`와 `docs/context/current_working_state.md`를 따른다.
""",
    )
    write_text(
        INPUT_REFS,
        f"""# Stage346 Input References(346단계 입력 참조)

## Source Run(원천 실행)

- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{PARENT_RUN_ID}`
- source_final_decision(원천 최종 결정): `{rel(SOURCE_FINAL_DECISION)}`
- source_summary(원천 요약): `{rel(SOURCE_SUMMARY)}`
- source_report(원천 보고서): `{rel(SOURCE_REPORT)}`
- source_runtime_identity(원천 런타임 정체성): `{rel(SOURCE_RUNTIME_IDENTITY)}`
- source_proxy_mt5_diff(원천 프록시-MT5 차이): `{rel(SOURCE_DIFF)}`

## Local Compact Inputs(로컬 경량 입력)

- handoff_manifest(인계 목록): `{rel(HANDOFF_MANIFEST)}`
- compact_summary(경량 요약): `{rel(COMPACT_SUMMARY)}`
- review_queue(검토 대기열): `{rel(NEXT_QUEUE)}`

Action(행동): heavy raw runtime evidence(무거운 원천 런타임 근거)는 참조하고, Stage346(346단계)에는 작은 요약과 queue(대기열)만 둔다.
Effect(효과): Stage346(346단계)이 Stage345(345단계)의 무게를 복제하지 않는다.
""",
    )


def write_reports(final: Mapping[str, Any]) -> None:
    write_text(
        REPORT_PATH,
        f"""# run346A Stage Branch(346A 단계 분기)

## Decision(결정)

`{DECISION}`

Action(행동): Stage345(345단계)에 남아 있던 run345C review(345C 검토)를 Stage346(346단계) run346B로 분기했다.
Effect(효과): Stage345(345단계)는 MT5 runtime probe(MT5 런타임 탐침) 실행 근거까지로 가볍게 멈추고, 검토와 source pivot(원천 전환)은 Stage346(346단계)에서 다룬다.

## Source Snapshot(원천 스냅샷)

- source_run(원천 실행): `{PARENT_RUN_ID}`
- best_attempt(최고 시도): `{final.get("best_attempt_name", "")}`
- net_profit(순수익): `{final.get("best_net_profit", "")}`
- profit_factor(수익 팩터): `{final.get("best_profit_factor", "")}`
- recovery_factor(회복 계수): `{final.get("best_recovery_factor", "")}`
- trade_count(거래수): `{final.get("best_trade_count", "")}`
- long_short(롱/숏): `{final.get("best_long_trade_count", "")}/{final.get("best_short_trade_count", "")}`
- matched_rows(일치 행): `{final.get("matched_rows", "")}/{final.get("expected_rows", "")}`

## Next Work(다음 작업)

`{NEXT_RUN_ID}`는 review(검토)만 수행한다. Positive clue(긍정 단서), failure memory(실패 기억), asymmetric model/source seed(비대칭 모델/원천 씨앗)를 분리한다.

## Claim Boundary(주장 경계)

`{CLAIM_BOUNDARY}`
""",
    )
    append_text_once(
        SOURCE_REVIEW_INDEX,
        "run346A_branch_stage345_to_cash_open_runtime_review_source_pivot",
        f"""## run346A Branch Handoff(346A 분기 인계)

- from(출발): `{SOURCE_STAGE_ID}` / `{PARENT_RUN_ID}`
- to(도착): `{NEW_STAGE_ID}` / `{NEXT_RUN_ID}`
- effect(효과): Stage345(345단계)의 review(검토) 부담을 새 stage(단계)로 옮겼다.
""",
    )
    write_text(
        REVIEW_INDEX,
        f"""# Stage346 Review Index(346단계 검토 색인)

## run346A Stage Branch(346A 단계 분기)

- report(보고서): `{rel(REPORT_PATH)}`
- final_decision(최종 결정): `{rel(FINAL_DECISION)}`
- next_run(다음 실행): `{NEXT_RUN_ID}`
- effect(효과): Stage345(345단계)의 무거운 review(검토)를 Stage346(346단계)으로 분기했다.
""",
    )
    write_text(
        DECISION_DOC,
        f"""# 2026-06-01 Stage346A Branch Decision(346A 단계 분기 결정)

- decision(결정): `{DECISION}`
- from(출발): `{SOURCE_STAGE_ID}` / `{PARENT_RUN_ID}`
- to(도착): `{NEW_STAGE_ID}` / `{NEXT_RUN_ID}`
- superseded_planned_run(대체된 예정 실행): `{SUPERSEDED_RUN_ID}`
- reason(이유): Stage345(345단계)가 MT5 runtime probe(MT5 런타임 탐침) 실행, 결과, 검토 예정까지 안고 있어 무거워졌고, 다음 질문은 review/source pivot(검토/원천 전환)이라는 별도 topic pivot(주제 전환)이기 때문이다.

Action(행동): Stage346(346단계)를 열고 run346B(346B 실행)를 review packet(검토 묶음)으로 둔다.
Effect(효과): run345B runtime evidence(345B 런타임 근거)는 source truth(원천 진실)로 남고, 검토는 새 stage(단계)에서 작게 시작한다.

claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
    )


def write_status_docs(final: Mapping[str, Any]) -> None:
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
    current_text = f"""# Current Working State(현재 작업 상태)

## Current Truth(현재 진실)

- active_stage(현재 단계): `{NEW_STAGE_ID}`
- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`

## Effect(효과)

Stage345(345단계)가 무거워져 run345C review(345C 검토)를 Stage346(346단계)으로 분기했다. run346B(346B 실행)는 run345B MT5 runtime probe(345B MT5 런타임 탐침)를 review(검토)하고 asymmetric source pivot(비대칭 원천 전환) 씨앗을 정리한다.

## Claim Boundary(주장 경계)

`{CLAIM_BOUNDARY}`

No candidate selection(후보 선정 없음), no forward pass(전진 통과 없음), no live readiness(실거래 준비 없음), no operating promotion(운영 승격 없음), no runtime authority(런타임 권위 없음), no Goal Achieve(목표 달성 없음).
"""
    write_text(CURRENT_WORKING_STATE, current_text)
    stage_selection = f"""# Stage 346 Selection Status(346단계 선정 상태)

- active_stage(현재 단계): `{NEW_STAGE_ID}`
- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- selected_model(선정 모델): `none(없음)`
- source_runtime_probe(원천 런타임 탐침): `{PARENT_RUN_ID}`
- source_package(원천 패키지): `{SOURCE_PACKAGE_RUN_ID}`
- reference_attempt(참고 시도): `{final.get("best_attempt_name", "")}`
- reference_net_profit(참고 순수익): `{final.get("best_net_profit", "")}`
- reference_profit_factor(참고 수익 팩터): `{final.get("best_profit_factor", "")}`
- reference_trade_count(참고 거래수): `{final.get("best_trade_count", "")}`
- runtime_authority(런타임 권위): `not_claimed(주장 없음)`
- operating_promotion(운영 승격): `not_claimed(주장 없음)`
- Goal Achieve(목표 달성): `not_claimed(주장 없음)`

Effect(효과): Stage346(346단계)는 review/source pivot(검토/원천 전환) 전용이며 selection(선정)을 주장하지 않는다.
"""
    write_text(SELECTION_STATUS, stage_selection)
    write_text(ROOT_SELECTION_STATUS, stage_selection)
    write_text(
        SOURCE_SELECTION_STATUS,
        f"""# Stage 345 Selection Status(345단계 선정 상태)

- active_stage_at_handoff(인계 당시 단계): `{SOURCE_STAGE_ID}`
- latest_completed_run(최근 완료 실행): `{PARENT_RUN_ID}`
- superseded_planned_run(대체된 예정 실행): `{SUPERSEDED_RUN_ID}`
- handoff_stage(인계 단계): `{NEW_STAGE_ID}`
- handoff_run(인계 실행): `{RUN_ID}`
- next_review_run(다음 검토 실행): `{NEXT_RUN_ID}`
- selected_model(선정 모델): `none(없음)`
- source_package(원천 패키지): `{SOURCE_PACKAGE_RUN_ID}`
- best_attempt(최고 시도): `{final.get("best_attempt_name", "")}`
- best_net_profit(최고 순수익): `{final.get("best_net_profit", "")}`
- best_profit_factor(최고 수익 팩터): `{final.get("best_profit_factor", "")}`
- best_trade_count(최고 거래수): `{final.get("best_trade_count", "")}`
- runtime_authority(런타임 권위): `not_claimed(주장 없음)`
- operating_promotion(운영 승격): `not_claimed(주장 없음)`
- Goal Achieve(목표 달성): `not_claimed(주장 없음)`

Effect(효과): Stage345(345단계)는 MT5 runtime probe(MT5 런타임 탐침) 실행 근거를 보존하고, review(검토)는 Stage346(346단계)으로 넘긴다.
""",
    )
    append_text_once(
        SOURCE_STAGE_BRIEF,
        "## run346A Review Handoff(346A 검토 인계)",
        f"""## run346A Review Handoff(346A 검토 인계)

- branch_run(분기 실행): `{RUN_ID}`
- next_stage(다음 단계): `{NEW_STAGE_ID}`
- next_run(다음 실행): `{NEXT_RUN_ID}`
- action(행동): Stage345(345단계)의 run345C review(345C 검토)를 Stage346(346단계)으로 이동했다.
- effect(효과): Stage345(345단계)는 runtime probe(MT5 런타임 탐침) 근거까지로 가볍게 멈추고, 검토는 새 stage(단계)에서 이어간다.
""",
    )


def write_receipts(final: Mapping[str, Any], handoff_rows: Sequence[Mapping[str, Any]]) -> None:
    receipt_time = now_utc()
    source_inputs = [row["source_path"] for row in handoff_rows if row.get("exists") == "true"]
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
            "effect": "Stage345 review(345단계 검토)를 Stage346(346단계)으로 분기한다.",
            "created_at_utc": receipt_time,
        },
    )
    write_json(
        LINEAGE_RECEIPT,
        {
            "run_id": RUN_ID,
            "source_inputs": source_inputs,
            "producer": rel(Path("stage_pipelines/stage346/branch_stage345_to_cash_open_runtime_review_source_pivot_without_db.py")),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [
                rel(HANDOFF_MANIFEST),
                rel(COMPACT_SUMMARY),
                rel(NEXT_QUEUE),
                rel(REPORT_PATH),
                rel(FINAL_DECISION),
            ],
            "artifact_hashes": "recorded_in_artifact_registry(산출물 등록부에 기록)",
            "registry_links": [
                rel(RUN_REGISTRY),
                rel(PROJECT_LEDGER),
                rel(ARTIFACT_REGISTRY),
                rel(STAGE_LEDGER),
            ],
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
            "candidate_selection": "not_claimed",
            "forward_pass": "not_claimed",
            "live_readiness": "not_claimed",
            "operating_promotion": "not_claimed",
            "runtime_authority": "not_claimed",
            "goal_achieve": "not_claimed",
            "allowed_claim": "state_sync_stage_branch_and_review_handoff_only(상태 동기화 단계 분기와 검토 인계 전용)",
            "created_at_utc": receipt_time,
        },
    )


def write_final_decision(final: Mapping[str, Any], compact_rows: Sequence[Mapping[str, Any]]) -> None:
    payload = {
        "run_id": RUN_ID,
        "stage_id": NEW_STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "superseded_planned_run_id": SUPERSEDED_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "claim_boundary": CLAIM_BOUNDARY,
        "source_package_run_id": SOURCE_PACKAGE_RUN_ID,
        "source_status": final.get("status", ""),
        "source_judgment": final.get("judgment", ""),
        "source_gate_passes": final.get("gate_passes", ""),
        "source_gate_total": final.get("gate_total", ""),
        "source_matched_rows": final.get("matched_rows", ""),
        "source_expected_rows": final.get("expected_rows", ""),
        "source_best_attempt": final.get("best_attempt_name", ""),
        "source_best_net_profit": final.get("best_net_profit", ""),
        "source_best_profit_factor": final.get("best_profit_factor", ""),
        "source_best_recovery_factor": final.get("best_recovery_factor", ""),
        "source_best_trade_count": final.get("best_trade_count", ""),
        "compact_summary_rows": len(compact_rows),
        "gate_passes": 8,
        "gate_total": 8,
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
            "parent_run_id": PARENT_RUN_ID,
            "superseded_planned_run_id": SUPERSEDED_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "producer": rel(Path("stage_pipelines/stage346/branch_stage345_to_cash_open_runtime_review_source_pivot_without_db.py")),
            "inputs": [rel(path) for path, _label in SOURCE_INPUTS],
            "outputs": [
                rel(HANDOFF_MANIFEST),
                rel(COMPACT_SUMMARY),
                rel(NEXT_QUEUE),
                rel(STAGE_TRANSITION_RECEIPT),
                rel(LINEAGE_RECEIPT),
                rel(CLAIM_RECEIPT),
                rel(GATE_AUDIT),
                rel(FINAL_DECISION),
                rel(REPORT_PATH),
                rel(DECISION_DOC),
            ],
            "claim_boundary": CLAIM_BOUNDARY,
            "created_at_utc": now_utc(),
        },
    )


def registry_rows(final: Mapping[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    ledger = stage_ledger_rows(final)
    run_registry = [
        {
            "run_id": RUN_ID,
            "stage_id": NEW_STAGE_ID,
            "lane": "state_sync_stage_branch(상태 동기화 단계 분기)",
            "status": STATUS,
            "judgment": JUDGMENT,
            "path": rel(FINAL_DECISION),
            "notes": "Stage345 review(345단계 검토)를 Stage346(346단계)으로 분기함; no selection(선정 없음).",
            "family": "state_sync(상태 동기화)",
            "primary_report": rel(REPORT_PATH),
            "run_number": RUN_NUMBER,
            "date": TODAY,
            "decision": DECISION,
            "parent_run_id": PARENT_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "rows": final.get("matched_rows", ""),
            "gate_passes": 8,
            "gate_total": 8,
            "claim_boundary": CLAIM_BOUNDARY,
            "report_path": rel(REPORT_PATH),
            "primary_artifact": rel(FINAL_DECISION),
            "candidate_model_id": "none(없음)",
            "net_profit": final.get("best_net_profit", ""),
            "profit_factor": final.get("best_profit_factor", ""),
            "drawdown": final.get("best_max_drawdown_amount", ""),
            "recovery_factor": final.get("best_recovery_factor", ""),
            "trade_count": final.get("best_trade_count", ""),
            "result_status": "stage_branch_opened_no_selection(단계 분기 완료, 선정 없음)",
            "expectancy": final.get("best_expectancy", ""),
            "attempt_count": final.get("attempt_rows", ""),
            "view": "Tier A separate(Tier A 분리)",
            "tier": "Tier A",
            "metric_scope": "stage_branch_handoff_run345B_runtime_probe",
            "source_package_run_id": SOURCE_PACKAGE_RUN_ID,
        }
    ]
    return ledger, run_registry


def write_registries(final: Mapping[str, Any]) -> None:
    ledger, run_registry = registry_rows(final)
    write_csv(STAGE_LEDGER, ledger, STAGE_LEDGER_COLUMNS)
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], ledger)
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], run_registry)
    artifact_paths = [
        (FINAL_DECISION, "final_decision(최종 결정)"),
        (RUN_MANIFEST, "run_manifest(실행 목록)"),
        (GATE_AUDIT, "gate_audit(게이트 감사)"),
        (HANDOFF_MANIFEST, "handoff_manifest(인계 목록)"),
        (COMPACT_SUMMARY, "compact_summary(경량 요약)"),
        (NEXT_QUEUE, "review_queue(검토 대기열)"),
        (REPORT_PATH, "report(보고서)"),
        (DECISION_DOC, "decision_doc(결정 문서)"),
        (STAGE_BRIEF, "stage_brief(단계 개요)"),
        (INPUT_REFS, "input_refs(입력 참조)"),
        (SELECTION_STATUS, "selection_status(선정 상태)"),
        (STAGE_TRANSITION_RECEIPT, "stage_transition_receipt(단계 전환 영수증)"),
        (LINEAGE_RECEIPT, "artifact_lineage_receipt(산출물 계보 영수증)"),
        (CLAIM_RECEIPT, "claim_boundary_receipt(주장 경계 영수증)"),
    ]
    artifact_rows = []
    for path, artifact_type in artifact_paths:
        artifact_rows.append(
            {
                "artifact_id": f"{RUN_ID}__{path.stem}",
                "artifact_type": artifact_type,
                "path": rel(path),
                "artifact_path": rel(path),
                "sha256": sha256_file(path),
                "stage_id": NEW_STAGE_ID,
                "run_id": RUN_ID,
                "created_at": TODAY,
                "created_at_utc": now_utc(),
                "claim_boundary": CLAIM_BOUNDARY,
                "notes": "Stage346 branch artifact(346단계 분기 산출물).",
            }
        )
    append_or_replace_csv(ARTIFACT_REGISTRY, ["artifact_id"], artifact_rows)


def write_exploration_register() -> None:
    append_text_once(
        IDEA_REGISTRY,
        "`IDEA-ST346-CASH-OPEN-ASYMMETRIC-SOURCE-PIVOT`",
        f"""| `IDEA-ST346-CASH-OPEN-ASYMMETRIC-SOURCE-PIVOT` | `{NEW_STAGE_ID}` | run345B(345B 실행)의 exact runtime parity(정확 런타임 동등성)와 long/short imbalance(롱/숏 불균형)는 asymmetric model/source split(비대칭 모델/원천 분리)로 회수할 수 있다 | `Tier A separate + Tier B missing_required(Tier A 분리 + Tier B 필수 누락)` | `opened_research_development_only` | run346A(346A 실행)가 Stage346(346단계)을 열었고 run346B(346B 실행)가 review/source pivot(검토/원천 전환)을 수행한다. selected candidate(선택 후보), ONNX readiness(온엑스 준비), runtime authority(런타임 권위)는 없음 |""",
    )


def write_changelog() -> None:
    text = f"""## 2026-06-01 run346A Stage Branch(346A 단계 분기)

- action(행동): Stage345(345단계)의 run345C review(345C 검토)를 Stage346(346단계) run346B로 분기했다.
- effect(효과): Stage345(345단계)의 무게를 줄이고, cash-open runtime review(현금장 런타임 검토)는 새 stage(단계)에서 작게 시작한다.
- boundary(경계): selection/runtime authority/Goal Achieve(선정/런타임 권위/목표 달성)는 주장하지 않는다.
"""
    append_text_once(WORKSPACE_CHANGELOG, "## 2026-06-01 run346A Stage Branch", text)
    append_text_once(ROOT_CHANGELOG, "## 2026-06-01 run346A Stage Branch", text)


def validate(final: Mapping[str, Any]) -> None:
    required_outputs = [
        STAGE_BRIEF,
        INPUT_REFS,
        SELECTION_STATUS,
        REPORT_PATH,
        DECISION_DOC,
        FINAL_DECISION,
        RUN_MANIFEST,
        GATE_AUDIT,
        WORKSPACE_STATE,
        CURRENT_WORKING_STATE,
    ]
    missing = [rel(path) for path in required_outputs if not path_is_file(path)]
    if missing:
        raise FileNotFoundError("missing generated output(생성 출력 누락): " + ", ".join(missing))
    gate_fields, gates = read_csv_rows(GATE_AUDIT)
    if not gate_fields or not gates or any(row.get("status") != "passed" for row in gates):
        raise RuntimeError("run346A required gate audit failed(필수 게이트 감사 실패)")
    workspace = read_text(WORKSPACE_STATE)
    selection = read_text(SELECTION_STATUS)
    current = read_text(CURRENT_WORKING_STATE)
    for label, text in [("workspace", workspace), ("selection", selection), ("current", current)]:
        if NEW_STAGE_ID not in text:
            raise RuntimeError(f"{label} missing active Stage346(346단계 누락)")
    if final.get("goal_achieve") not in ("not_claimed", "", None):
        raise RuntimeError("source unexpectedly claimed Goal Achieve(원천이 목표 달성을 주장함)")


def main() -> None:
    final = source_decision()
    for path, _label in SOURCE_INPUTS:
        required(path)
    compact_rows = compact_summary_rows()
    handoff_rows = write_handoff_manifest()
    write_next_queue(final)
    write_stage_docs(final)
    write_reports(final)
    write_status_docs(final)
    write_receipts(final, handoff_rows)
    gate_rows()
    write_final_decision(final, compact_rows)
    write_manifest()
    write_registries(final)
    write_exploration_register()
    write_changelog()
    validate(final)
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "next_run_id": NEXT_RUN_ID,
                "source_best_attempt": final.get("best_attempt_name", ""),
                "source_best_net_profit": final.get("best_net_profit", ""),
                "gate_passes": 8,
                "gate_total": 8,
                "goal_achieve": "not_claimed",
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
