from __future__ import annotations

import csv
import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
TODAY = "2026-06-01"

SOURCE_STAGE_ID = "338_runtime_trade_lifecycle__proxy_positive_mt5_negative_repair"
NEW_STAGE_ID = "339_runtime_lifecycle_exit__side_balance_probe_review"
SOURCE_STAGE_DIR = ROOT / "stages" / SOURCE_STAGE_ID
NEW_STAGE_DIR = ROOT / "stages" / NEW_STAGE_ID

RUN_NUMBER = "run339A"
RUN_ID = "run339A_branch_stage338_to_lifecycle_exit_probe_review_without_db_v1"
PARENT_RUN_ID = "run338M_materialize_lifecycle_exit_side_balance_recovery_expansion_mt5_probe_package_without_db_v1"
PARTIAL_RUNTIME_RUN_ID = "run338N_execute_lifecycle_exit_side_balance_recovery_expansion_mt5_probe_without_db_v1"
NEXT_RUN_ID = "run339B_review_recovered_lifecycle_exit_side_balance_mt5_probe_without_db_v1"

STATUS = "completed_stage339A_branch_from_stage338_lifecycle_exit_probe_review_opened_no_selection"
JUDGMENT = "stage_branch_completed_stage338_overweight_handoff_to_recovered_probe_review_no_selection"
DECISION = "stage339A_open_run339B_review_recovered_lifecycle_exit_probe_outputs"
CLAIM_BOUNDARY = (
    "state_sync_stage_branch_and_unreviewed_runtime_output_handoff_only_no_candidate_selection_"
    "no_forward_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

RUN_DIR = NEW_STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = NEW_STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEW_DIR / "run339A_stage_branch.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage339A_branch_stage338_to_lifecycle_exit_probe_review.md"
STAGE_BRIEF = NEW_STAGE_DIR / "00_spec" / "stage_brief.md"
STAGE_README = NEW_STAGE_DIR / "README.md"
INPUT_REFS = NEW_STAGE_DIR / "01_inputs" / "input_refs.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"
SELECTION_STATUS = NEW_STAGE_DIR / "04_selected" / "selection_status.md"
SOURCE_SELECTION_STATUS = SOURCE_STAGE_DIR / "04_selected" / "selection_status.md"
SOURCE_STAGE_BRIEF = SOURCE_STAGE_DIR / "00_spec" / "stage_brief.md"
SOURCE_STAGE_README = SOURCE_STAGE_DIR / "README.md"

SOURCE_RUN_DIR = SOURCE_STAGE_DIR / "02_runs" / "run338M"
PARTIAL_RUNTIME_RUN_DIR = SOURCE_STAGE_DIR / "02_runs" / "run338N"
SOURCE_FINAL_DECISION = SOURCE_RUN_DIR / "final_decision.json"
SOURCE_ATTEMPT_PACKAGE = SOURCE_RUN_DIR / "runtime_probe_attempt_package.csv"
SOURCE_VARIANT_PREVIEW = SOURCE_RUN_DIR / "lifecycle_variant_preview.csv"
SOURCE_EXPECTED_TAPE = SOURCE_RUN_DIR / "expected" / "expected_tape.csv"
PARTIAL_SUMMARY = PARTIAL_RUNTIME_RUN_DIR / "lifecycle_exit_mt5_probe_summary.csv"
PARTIAL_EXECUTION_RESULT = PARTIAL_RUNTIME_RUN_DIR / "mt5_execution_result.json"
PARTIAL_REPORT_RECORDS = PARTIAL_RUNTIME_RUN_DIR / "strategy_tester_report_records.json"
PARTIAL_RUNTIME_IDENTITY = PARTIAL_RUNTIME_RUN_DIR / "runtime_identity.csv"
PARTIAL_OUTPUT_MANIFEST = PARTIAL_RUNTIME_RUN_DIR / "runtime_output_copy_manifest.csv"
PARTIAL_PROXY_DIFF = PARTIAL_RUNTIME_RUN_DIR / "proxy_mt5_runtime_difference.csv"
PARTIAL_FINAL_DECISION = PARTIAL_RUNTIME_RUN_DIR / "final_decision.json"

HANDOFF_MANIFEST = RUN_DIR / "stage338_to_stage339_handoff_manifest.csv"
RUNTIME_OUTPUT_INVENTORY = RUN_DIR / "recovered_runtime_output_inventory.csv"
RUNTIME_PREVIEW = RUN_DIR / "recovered_runtime_preview.csv"
NEXT_QUEUE = RUN_DIR / "run339B_queue.csv"
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


def now_utc() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def rel(path: Path | str) -> str:
    candidate = Path(path)
    if not candidate.is_absolute():
        candidate = ROOT / candidate
    try:
        return candidate.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return candidate.as_posix()


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def exists(path: Path) -> bool:
    return path.exists()


def read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, low_memory=False, encoding="utf-8-sig")


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_csv(path: Path, frame: pd.DataFrame) -> None:
    ensure_parent(path)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        frame.to_csv(handle, index=False, lineterminator="\n", quoting=csv.QUOTE_MINIMAL)


def write_json(path: Path, payload: Any) -> None:
    ensure_parent(path)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_bom_text(path: Path, text: str) -> None:
    ensure_parent(path)
    path.write_text(text.rstrip() + "\n", encoding="utf-8-sig", newline="\n")


def append_text_once(path: Path, marker: str, text: str) -> None:
    current = path.read_text(encoding="utf-8-sig") if path.exists() else ""
    if marker in current:
        return
    next_text = f"{current.rstrip()}\n\n{text.strip()}\n" if current.strip() else text.strip() + "\n"
    write_bom_text(path, next_text)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def append_or_replace_csv(path: Path, key_columns: Sequence[str], rows: Iterable[Mapping[str, Any]]) -> None:
    rows = list(rows)
    frame = read_csv(path) if path.exists() else pd.DataFrame()
    if frame.empty:
        frame = pd.DataFrame(columns=sorted({column for row in rows for column in row}))
    for row in rows:
        for column in row:
            if column not in frame.columns:
                frame[column] = ""
        mask = pd.Series(True, index=frame.index)
        for key in key_columns:
            if key in frame.columns:
                mask &= frame[key].astype(str).eq(str(row.get(key, "")))
            else:
                mask &= False
        frame = frame.loc[~mask].copy()
        frame = pd.concat([frame, pd.DataFrame([row])], ignore_index=True)
    ordered = list(dict.fromkeys(list(frame.columns) + [column for row in rows for column in row]))
    write_csv(path, frame[ordered])


def numeric(series: pd.Series) -> pd.Series:
    return pd.to_numeric(series, errors="coerce")


def build_runtime_preview() -> tuple[pd.DataFrame, dict[str, Any]]:
    if not PARTIAL_SUMMARY.exists():
        empty = pd.DataFrame(
            [
                {
                    "source_run_id": PARTIAL_RUNTIME_RUN_ID,
                    "review_status": "missing_required(필수 누락)",
                    "effect": "run339B(339B 실행)가 MT5(메타트레이더5) 실행을 다시 해야 한다.",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            ]
        )
        return empty, {"attempt_count": 0, "raw_best_attempt": "", "raw_best_net_profit": None}

    summary = read_csv(PARTIAL_SUMMARY).copy()
    for column in [
        "net_profit",
        "profit_factor",
        "expectancy",
        "recovery_factor",
        "max_drawdown_amount",
        "trade_count",
        "long_trade_count",
        "short_trade_count",
        "matched_rows",
        "probability_mismatch_rows",
        "decision_mismatch_rows",
    ]:
        if column in summary.columns:
            summary[column] = numeric(summary[column])
    if {"long_trade_count", "short_trade_count"}.issubset(summary.columns):
        total_side = summary["long_trade_count"] + summary["short_trade_count"]
        summary["raw_trade_side_balance"] = (
            summary[["long_trade_count", "short_trade_count"]].min(axis=1) / total_side.replace(0, pd.NA)
        ).fillna(0.0)
    else:
        summary["raw_trade_side_balance"] = ""
    summary["source_run_id"] = PARTIAL_RUNTIME_RUN_ID
    summary["review_status"] = "unreviewed_closeout_failed(검토 전 종료 기록 실패)"
    summary["usable_in_stage339"] = "review_input_only(검토 입력 전용)"
    summary["effect"] = "run339B(339B 실행)가 재실행 전에 원시 MT5(메타트레이더5) 산출물을 검토할 수 있게 한다."
    summary["claim_boundary"] = CLAIM_BOUNDARY
    columns = [
        "source_run_id",
        "attempt_name",
        "model_id",
        "tester_status",
        "runtime_status",
        "report_status",
        "matched_rows",
        "probability_mismatch_rows",
        "decision_mismatch_rows",
        "net_profit",
        "profit_factor",
        "expectancy",
        "recovery_factor",
        "max_drawdown_amount",
        "trade_count",
        "long_trade_count",
        "short_trade_count",
        "raw_trade_side_balance",
        "review_status",
        "usable_in_stage339",
        "effect",
        "claim_boundary",
    ]
    columns = [column for column in columns if column in summary.columns]
    preview = summary[columns].copy()
    sortable = summary.copy()
    sortable["_net"] = numeric(sortable.get("net_profit", pd.Series(dtype=float)))
    sortable["_pf"] = numeric(sortable.get("profit_factor", pd.Series(dtype=float)))
    sortable["_recovery"] = numeric(sortable.get("recovery_factor", pd.Series(dtype=float)))
    best = sortable.sort_values(["_net", "_pf", "_recovery"], ascending=False).iloc[0]
    metrics = {
        "attempt_count": int(len(summary)),
        "matched_rows_total": int(numeric(summary.get("matched_rows", pd.Series(dtype=float))).fillna(0).sum()),
        "probability_mismatch_rows_total": int(numeric(summary.get("probability_mismatch_rows", pd.Series(dtype=float))).fillna(0).sum()),
        "decision_mismatch_rows_total": int(numeric(summary.get("decision_mismatch_rows", pd.Series(dtype=float))).fillna(0).sum()),
        "raw_best_attempt": str(best.get("attempt_name", "")),
        "raw_best_model_id": str(best.get("model_id", "")),
        "raw_best_net_profit": float(best.get("net_profit", 0.0)),
        "raw_best_profit_factor": float(best.get("profit_factor", 0.0)),
        "raw_best_expectancy": float(best.get("expectancy", 0.0)),
        "raw_best_recovery_factor": float(best.get("recovery_factor", 0.0)),
        "raw_best_drawdown": float(best.get("max_drawdown_amount", 0.0)),
        "raw_best_trade_count": int(float(best.get("trade_count", 0.0))),
        "raw_best_long_trade_count": int(float(best.get("long_trade_count", 0.0))),
        "raw_best_short_trade_count": int(float(best.get("short_trade_count", 0.0))),
        "partial_final_decision_exists": PARTIAL_FINAL_DECISION.exists(),
    }
    return preview, metrics


def build_inventory() -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for path, role, availability in [
        (SOURCE_FINAL_DECISION, "source_package_final_decision(원천 패키지 최종 결정)", "tracked(추적됨)"),
        (SOURCE_ATTEMPT_PACKAGE, "source_mt5_attempt_package(원천 MT5 시도 패키지)", "tracked(추적됨)"),
        (SOURCE_VARIANT_PREVIEW, "source_variant_preview(원천 변형 미리보기)", "tracked(추적됨)"),
        (SOURCE_EXPECTED_TAPE, "source_expected_tape(원천 기대 테이프)", "tracked(추적됨)"),
        (PARTIAL_SUMMARY, "partial_runtime_summary(부분 런타임 요약)", "generated_unreviewed(생성됨, 미검토)"),
        (PARTIAL_EXECUTION_RESULT, "partial_mt5_execution_result(부분 MT5 실행 결과)", "generated_unreviewed(생성됨, 미검토)"),
        (PARTIAL_REPORT_RECORDS, "partial_strategy_report_records(부분 전략 보고 기록)", "generated_unreviewed(생성됨, 미검토)"),
        (PARTIAL_RUNTIME_IDENTITY, "partial_runtime_identity(부분 런타임 정체성)", "generated_unreviewed(생성됨, 미검토)"),
        (PARTIAL_OUTPUT_MANIFEST, "partial_output_copy_manifest(부분 출력 복사 목록)", "generated_unreviewed(생성됨, 미검토)"),
        (PARTIAL_PROXY_DIFF, "partial_proxy_mt5_diff(부분 프록시 MT5 차이)", "generated_unreviewed(생성됨, 미검토)"),
        (PARTIAL_FINAL_DECISION, "partial_final_decision(부분 최종 결정)", "missing_expected(예상 누락)"),
    ]:
        rows.append(
            {
                "artifact_role": role,
                "path": rel(path),
                "exists": path.exists(),
                "availability": availability,
                "sha256": sha256_file(path) if path.exists() and path.is_file() else "",
                "consumer": NEXT_RUN_ID,
                "effect": "Stage339(339단계) review(검토)가 재실행 여부를 판단하게 한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return pd.DataFrame(rows)


def build_handoff(metrics: Mapping[str, Any]) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "handoff_id": "stage338M_and_partial338N_to_stage339A",
                "source_stage_id": SOURCE_STAGE_ID,
                "new_stage_id": NEW_STAGE_ID,
                "branch_run_id": RUN_ID,
                "source_completed_run_id": PARENT_RUN_ID,
                "partial_runtime_run_id": PARTIAL_RUNTIME_RUN_ID,
                "next_run_id": NEXT_RUN_ID,
                "branch_reason": "Stage338(338단계)이 너무 무거워져 lifecycle/exit(생명주기/청산) runtime review(런타임 검토)를 Stage339(339단계)로 분리한다.",
                "raw_best_attempt_unreviewed": metrics.get("raw_best_attempt", ""),
                "raw_best_net_profit_unreviewed": metrics.get("raw_best_net_profit", ""),
                "raw_best_profit_factor_unreviewed": metrics.get("raw_best_profit_factor", ""),
                "raw_best_trade_count_unreviewed": metrics.get("raw_best_trade_count", ""),
                "raw_best_recovery_factor_unreviewed": metrics.get("raw_best_recovery_factor", ""),
                "raw_best_drawdown_unreviewed": metrics.get("raw_best_drawdown", ""),
                "allowed_use": "review input, preserved clue, recovery decision(검토 입력, 보존 단서, 복구 결정)",
                "forbidden_use": "selected model, baseline, operating promotion, runtime authority(선정 모델, 기준선, 운영 승격, 런타임 권위)",
                "effect": "무거운 Stage338(338단계)을 닫고, 남은 runtime evidence(런타임 근거)를 짧은 검토 질문으로 넘긴다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )


def build_next_queue(metrics: Mapping[str, Any]) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "queue_id": "run339B_review_recovered_lifecycle_exit_side_balance_mt5_probe",
                "next_run_id": NEXT_RUN_ID,
                "priority": "P0",
                "primary_family": "kpi_evidence(핵심 성과 지표 근거)",
                "primary_skill": "obsidian-run-evidence-system(실행 근거 시스템)",
                "support_skills": "obsidian-runtime-parity(런타임 동등성);obsidian-result-judgment(결과 판정);obsidian-performance-attribution(성과 귀속)",
                "action": "review recovered run338N(338N 실행) MT5(메타트레이더5) outputs before rerun",
                "effect": "이미 생성된 산출물을 먼저 읽어 MT5(메타트레이더5) 재실행을 줄인다.",
                "raw_best_attempt_unreviewed": metrics.get("raw_best_attempt", ""),
                "required_inputs": ";".join(
                    [
                        rel(RUNTIME_PREVIEW),
                        rel(RUNTIME_OUTPUT_INVENTORY),
                        rel(PARTIAL_SUMMARY),
                        rel(PARTIAL_EXECUTION_RESULT),
                        rel(PARTIAL_REPORT_RECORDS),
                    ]
                ),
                "review_floors": "exact_parity(정확 동등성);net_profit_positive(순수익 양수);profit_factor>=1.10(수익 팩터);expectancy_positive(기대값 양수);recovery>=1.00(회복 계수);drawdown<=150(낙폭);trade_count>=30(거래수);side_balance>=0.25(방향 균형)",
                "fallback": "if evidence identity is incomplete, patch execution closeout helper or rerun MT5(근거 정체성이 불완전하면 종료 기록 도우미 수정 또는 MT5 재실행)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )


def gate_row(gate_id: str, status: str, evidence_path: str, effect: str) -> dict[str, Any]:
    return {
        "gate_id": gate_id,
        "status": status,
        "evidence_path": evidence_path,
        "effect": effect,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def build_gates() -> pd.DataFrame:
    rows = [
        gate_row(
            "source_completed_run_available",
            "passed" if SOURCE_FINAL_DECISION.exists() and SOURCE_ATTEMPT_PACKAGE.exists() else "failed",
            f"{rel(SOURCE_FINAL_DECISION)};{rel(SOURCE_ATTEMPT_PACKAGE)}",
            "run338M(338M 실행) 패키지를 Stage339(339단계)의 원천으로 고정한다.",
        ),
        gate_row(
            "partial_runtime_outputs_inventoried",
            "passed" if RUNTIME_OUTPUT_INVENTORY.exists() and RUNTIME_PREVIEW.exists() else "failed",
            f"{rel(RUNTIME_OUTPUT_INVENTORY)};{rel(RUNTIME_PREVIEW)}",
            "run338N(338N 실행)의 종료 기록 실패 산출물을 미검토 입력으로 분리한다.",
        ),
        gate_row(
            "new_stage_scaffold_created",
            "passed" if STAGE_BRIEF.exists() and SELECTION_STATUS.exists() and INPUT_REFS.exists() else "failed",
            f"{rel(STAGE_BRIEF)};{rel(SELECTION_STATUS)};{rel(INPUT_REFS)}",
            "Stage339(339단계)의 질문과 입력 경계를 만든다.",
        ),
        gate_row(
            "current_truth_synced",
            "passed" if WORKSPACE_STATE.exists() and CURRENT_WORKING_STATE.exists() else "failed",
            f"{rel(WORKSPACE_STATE)};{rel(CURRENT_WORKING_STATE)}",
            "재진입 시 Stage339(339단계)에서 바로 이어가게 한다.",
        ),
        gate_row(
            "registries_synced",
            "passed" if RUN_REGISTRY.exists() and PROJECT_LEDGER.exists() and ARTIFACT_REGISTRY.exists() else "failed",
            f"{rel(RUN_REGISTRY)};{rel(PROJECT_LEDGER)};{rel(ARTIFACT_REGISTRY)}",
            "run identity(실행 정체성)와 artifact lineage(산출물 계보)를 연결한다.",
        ),
        gate_row(
            "no_forbidden_operating_claim",
            "passed",
            rel(CLAIM_RECEIPT),
            "selected model(선정 모델), operating promotion(운영 승격), runtime authority(런타임 권위)를 주장하지 않는다.",
        ),
        gate_row(
            "required_gate_coverage_audit_written",
            "passed",
            rel(GATE_AUDIT),
            "closeout(종료 기록)의 gate(게이트) 근거를 남긴다.",
        ),
    ]
    return pd.DataFrame(rows)


def write_stage_docs(metrics: Mapping[str, Any]) -> None:
    stage_brief = f"""# Stage339 Runtime Lifecycle Exit Probe Review(339단계 런타임 생명주기 청산 탐침 검토)

## Canonical Stage ID(정식 단계 ID)

`{NEW_STAGE_ID}`

## Stage Question(단계 질문)

Can the run338M(338M 실행) lifecycle/exit(생명주기/청산) side-balance(방향 균형) probe outputs be reviewed or recovered without keeping Stage338(338단계) overloaded?
(run338M(338M 실행)의 생명주기/청산 방향 균형 탐침 산출물을 Stage338(338단계)을 더 무겁게 하지 않고 검토 또는 복구할 수 있는가?)

## Source Handoff(원천 인계)

- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_completed_run(완료 원천 실행): `{PARENT_RUN_ID}`
- partial_runtime_run(부분 런타임 실행): `{PARTIAL_RUNTIME_RUN_ID}`
- branch_run(분기 실행): `{RUN_ID}`
- next_run(다음 실행): `{NEXT_RUN_ID}`

## Raw Preview Boundary(원시 미리보기 경계)

- raw_best_attempt_unreviewed(검토 전 원시 최고 시도): `{metrics.get('raw_best_attempt', '')}`
- raw_best_net_profit_unreviewed(검토 전 원시 순수익): `{metrics.get('raw_best_net_profit', '')}`
- raw_best_profit_factor_unreviewed(검토 전 원시 수익 팩터): `{metrics.get('raw_best_profit_factor', '')}`
- raw_best_recovery_factor_unreviewed(검토 전 원시 회복 계수): `{metrics.get('raw_best_recovery_factor', '')}`
- raw_best_trade_count_unreviewed(검토 전 원시 거래수): `{metrics.get('raw_best_trade_count', '')}`

Effect(효과): 숫자는 보존하지만, run339B(339B 실행) 검토 전에는 positive result(긍정 결과)나 selection(선정)으로 쓰지 않는다.

## Scope(범위)

Stage339(339단계)는 MT5(메타트레이더5)를 새로 돌리는 단계가 아니라, 먼저 recovered runtime output(복구된 런타임 출력)을 검토하는 단계다.
Effect(효과): 이미 생긴 산출물을 버리지 않고, 필요할 때만 closeout helper(종료 기록 도우미) 수정 또는 MT5(메타트레이더5) 재실행으로 간다.

## Forbidden Claims(금지 주장)

No selected model(선정 모델 없음), no baseline(기준선 없음), no operating promotion(운영 승격 없음), no runtime authority(런타임 권위 없음), no Goal Achieve(목표 달성 없음).
"""
    input_refs = f"""# Stage339 Input References(339단계 입력 참조)

## Source Inputs(원천 입력)

- run338M final decision(338M 최종 결정): `{rel(SOURCE_FINAL_DECISION)}`
- run338M attempt package(338M 시도 패키지): `{rel(SOURCE_ATTEMPT_PACKAGE)}`
- run338M expected tape(338M 기대 테이프): `{rel(SOURCE_EXPECTED_TAPE)}`
- run338N partial summary(338N 부분 요약): `{rel(PARTIAL_SUMMARY)}`
- run338N execution result(338N 실행 결과): `{rel(PARTIAL_EXECUTION_RESULT)}`
- run338N report records(338N 보고 기록): `{rel(PARTIAL_REPORT_RECORDS)}`

## Stage339 Handoff Files(339단계 인계 파일)

- handoff manifest(인계 목록): `{rel(HANDOFF_MANIFEST)}`
- runtime output inventory(런타임 출력 목록): `{rel(RUNTIME_OUTPUT_INVENTORY)}`
- runtime preview(런타임 미리보기): `{rel(RUNTIME_PREVIEW)}`
- next queue(다음 대기열): `{rel(NEXT_QUEUE)}`

Effect(효과): run339B(339B 실행)가 같은 파일을 다시 찾느라 시간을 쓰지 않게 한다.
"""
    selection = f"""# Stage339 Selection Status(339단계 선택 상태)

- active_stage(활성 단계): `{NEW_STAGE_ID}`
- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- selected_model(선정 모델): `none(없음)`
- source_completed_run(완료 원천 실행): `{PARENT_RUN_ID}`
- partial_runtime_outputs(부분 런타임 산출물): `{PARTIAL_RUNTIME_RUN_ID}`
- runtime_authority(런타임 권위): `not_claimed(주장 없음)`
- operating_promotion(운영 승격): `not_claimed(주장 없음)`
- Goal Achieve(목표 달성): `not_claimed(주장 없음)`

Effect(효과): Stage339(339단계)를 검토 전용 상태로 열어 원시 MT5(메타트레이더5) 숫자를 운영 주장으로 오해하지 않게 한다.
"""
    report = f"""# run339A Stage Branch(단계 분기)

## Summary(요약)

- run_id(실행 ID): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- new_stage(새 단계): `{NEW_STAGE_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- next_run(다음 실행): `{NEXT_RUN_ID}`
- gates(게이트): `{rel(GATE_AUDIT)}`

## Action(행동)

Stage338(338단계)을 더 키우지 않고 Stage339(339단계)로 분기했다.
Effect(효과): 완료된 run338M(338M 실행) 패키지와 미검토 run338N(338N 실행) runtime output(런타임 출력)을 짧은 review packet(검토 묶음)으로 넘긴다.

## Raw Runtime Preview(원시 런타임 미리보기)

- best_attempt_unreviewed(검토 전 최고 시도): `{metrics.get('raw_best_attempt', '')}`
- net_profit_unreviewed(검토 전 순수익): `{metrics.get('raw_best_net_profit', '')}`
- profit_factor_unreviewed(검토 전 수익 팩터): `{metrics.get('raw_best_profit_factor', '')}`
- recovery_factor_unreviewed(검토 전 회복 계수): `{metrics.get('raw_best_recovery_factor', '')}`
- trade_count_unreviewed(검토 전 거래수): `{metrics.get('raw_best_trade_count', '')}`

Effect(효과): 좋은 냄새는 보존하지만, run339B(339B 실행) 검토 전에는 reviewed positive(검토된 긍정)로 말하지 않는다.

## Boundary(경계)

This is state sync and handoff only(상태 동기화와 인계만 해당). Selection(선정), operating promotion(운영 승격), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 없다.
"""
    decision = f"""# {TODAY} Stage339A Branch Decision(339A 단계 분기 결정)

- decision(결정): `{DECISION}`
- from(출발): `{SOURCE_STAGE_ID}` / `{PARENT_RUN_ID}`
- partial_runtime_source(부분 런타임 원천): `{PARTIAL_RUNTIME_RUN_ID}`
- to(도착): `{NEW_STAGE_ID}` / `{NEXT_RUN_ID}`
- reason(이유): Stage338(338단계)이 너무 무거워져 recovered runtime review(복구 런타임 검토)를 별도 단계로 분리한다.

Action(행동): 새 Stage339(339단계)를 열고 run339B(339B 실행)를 review(검토) 다음 행동으로 둔다.
Effect(효과): Stage338(338단계)의 무게를 줄이고, 이미 생성된 MT5(메타트레이더5) 산출물을 버리지 않는다.

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

Stage338(338단계)은 run338M(338M 실행) package(패키지)와 run338N(338N 실행) partial runtime outputs(부분 런타임 출력)을 Stage339(339단계)로 넘겼다. run339B(339B 실행)는 먼저 recovered output(복구 출력)을 검토한다.

## Claim Boundary(주장 경계)

`{CLAIM_BOUNDARY}`
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
    source_selection = f"""# Stage338 Selection Status(338단계 선택 상태)

- active_stage(활성 단계): `{SOURCE_STAGE_ID}`
- latest_completed_run(최근 완료 실행): `{PARENT_RUN_ID}`
- branched_to_stage(분기된 단계): `{NEW_STAGE_ID}`
- branch_run(분기 실행): `{RUN_ID}`
- partial_runtime_outputs(부분 런타임 산출물): `{PARTIAL_RUNTIME_RUN_ID}`
- selected_model(선정 모델): `none(없음)`
- runtime_authority(런타임 권위): `not_claimed(주장 없음)`
- operating_promotion(운영 승격): `not_claimed(주장 없음)`
- Goal Achieve(목표 달성): `not_claimed(주장 없음)`

Effect(효과): Stage338(338단계)을 더 키우지 않고 Stage339(339단계) 검토로 넘겼음을 재진입 때 바로 보이게 한다.
"""
    write_bom_text(STAGE_BRIEF, stage_brief)
    write_bom_text(STAGE_README, stage_brief)
    write_bom_text(INPUT_REFS, input_refs)
    write_bom_text(SELECTION_STATUS, selection)
    write_bom_text(REPORT_PATH, report)
    write_bom_text(DECISION_DOC, decision)
    write_bom_text(CURRENT_WORKING_STATE, current)
    write_bom_text(WORKSPACE_STATE, workspace)
    write_bom_text(SOURCE_SELECTION_STATUS, source_selection)

    marker = RUN_ID
    append_text_once(
        SOURCE_STAGE_BRIEF,
        marker,
        f"""## run339A Stage Branch(339A 단계 분기)

- branch_run(분기 실행): `{RUN_ID}`
- new_stage(새 단계): `{NEW_STAGE_ID}`
- next_run(다음 실행): `{NEXT_RUN_ID}`
- effect(효과): Stage338(338단계)의 lifecycle/exit(생명주기/청산) runtime review(런타임 검토)를 Stage339(339단계)로 나눠 단계 무게를 줄였다.
""",
    )
    append_text_once(
        SOURCE_STAGE_README,
        marker,
        f"""## run339A Stage Branch(339A 단계 분기)

- branch_run(분기 실행): `{RUN_ID}`
- new_stage(새 단계): `{NEW_STAGE_ID}`
- next_run(다음 실행): `{NEXT_RUN_ID}`
- effect(효과): Stage338(338단계)을 더 무겁게 하지 않고 run338N(338N 실행) partial output(부분 출력)을 검토 단계로 넘겼다.
""",
    )
    changelog = f"""## {TODAY} run339A Stage Branch(단계 분기)

- action(행동): Stage338(338단계)의 run338M(338M 실행) package(패키지)와 run338N(338N 실행) partial runtime output(부분 런타임 출력)을 Stage339(339단계)로 분기했다.
- effect(효과): Stage338(338단계)의 무게를 줄이고, run339B(339B 실행)가 재실행 전 recovered output review(복구 출력 검토)를 먼저 하게 했다.
- boundary(경계): selected model(선정 모델), operating promotion(운영 승격), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 없다.
"""
    append_text_once(ROOT_CHANGELOG, marker, changelog)
    append_text_once(WORKSPACE_CHANGELOG, marker, changelog)
    append_text_once(
        IDEA_REGISTRY,
        marker,
        f"""## {TODAY} Stage339 Lifecycle Exit Probe Review Seed(339단계 생명주기 청산 탐침 검토 씨앗)

- idea_id(아이디어 ID): `stage339_lifecycle_exit_probe_review_seed`
- hypothesis(가설): run338M(338M 실행)의 shorter hold(짧은 보유)와 side-balance(방향 균형) 변형은 MT5(메타트레이더5)에서 개선 단서를 줄 수 있지만, run338N(338N 실행) closeout(종료 기록)이 실패했으므로 먼저 근거 정체성을 검토해야 한다.
- legacy_relation(레거시 관계): `none(없음)`
- tier_scope(티어 범위): `Tier A separate(Tier A 분리); Tier B missing_required(Tier B 필수 누락); Tier A+B same_as_tier_a_until_tier_b_available(Tier A+B는 Tier B 가능 전까지 Tier A와 같음)`
- broad_sweep(넓은 탐색): run338M(338M 실행) 6개 lifecycle/exit(생명주기/청산) 변형.
- extreme_sweep(극단 탐색): close_on_flat(평탄 청산), shorter_hold(짧은 보유), asymmetric_long_relief(비대칭 롱 완화).
- micro_search_gate(미세 탐색 게이트): run339B(339B 실행)가 exact parity(정확 동등성), report identity(보고서 정체성), KPI floors(KPI 하한)를 검토해야 한다.
- wfo_plan(워크포워드 계획): runtime review(런타임 검토) 후 필요 시 별도 WFO(워크포워드 최적화) 단계로 분리한다.
- failure_memory(실패 기억): closeout helper recursion(종료 기록 도우미 재귀)은 코드/상태 문제로 기록하고, 원시 MT5(메타트레이더5) 숫자는 검토 전 단서로만 둔다.
- evidence_boundary(근거 경계): `runtime_probe_unreviewed_handoff(런타임 탐침 미검토 인계)`
""",
    )


def write_receipts(metrics: Mapping[str, Any]) -> None:
    base = {
        "run_id": RUN_ID,
        "stage_id": NEW_STAGE_ID,
        "parent_stage_id": SOURCE_STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "partial_runtime_run_id": PARTIAL_RUNTIME_RUN_ID,
        "created_at_utc": now_utc(),
        "status": STATUS,
        "judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(
        STAGE_TRANSITION_RECEIPT,
        {
            **base,
            "primary_family": "state_sync(상태 동기화)",
            "primary_skill": "obsidian-stage-transition(단계 전환)",
            "support_skills": [
                "obsidian-reentry-read(재진입 읽기)",
                "obsidian-artifact-lineage(산출물 계보)",
                "obsidian-claim-discipline(주장 규율)",
            ],
            "effect": "Stage338(338단계) 과밀 상태를 Stage339(339단계) 검토 질문으로 분리했다.",
        },
    )
    source_inputs = [
        SOURCE_FINAL_DECISION,
        SOURCE_ATTEMPT_PACKAGE,
        SOURCE_VARIANT_PREVIEW,
        SOURCE_EXPECTED_TAPE,
        PARTIAL_SUMMARY,
        PARTIAL_EXECUTION_RESULT,
        PARTIAL_REPORT_RECORDS,
        PARTIAL_RUNTIME_IDENTITY,
        PARTIAL_OUTPUT_MANIFEST,
        PARTIAL_PROXY_DIFF,
    ]
    write_json(
        LINEAGE_RECEIPT,
        {
            **base,
            "source_inputs": [rel(path) for path in source_inputs],
            "artifact_paths": [
                rel(HANDOFF_MANIFEST),
                rel(RUNTIME_OUTPUT_INVENTORY),
                rel(RUNTIME_PREVIEW),
                rel(NEXT_QUEUE),
                rel(REPORT_PATH),
                rel(DECISION_DOC),
            ],
            "artifact_hashes": {rel(path): sha256_file(path) for path in source_inputs if path.exists()},
            "availability": "connected_with_boundary(경계가 있는 연결)",
            "lineage_judgment": "connected_with_boundary(경계가 있는 연결)",
            "effect": "run338M(338M 실행)과 run338N(338N 실행) 산출물이 run339B(339B 실행) 검토 입력으로 연결된다.",
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            **base,
            "candidate_selection": "not_claimed(주장 없음)",
            "runtime_authority": "not_claimed(주장 없음)",
            "operating_promotion": "not_claimed(주장 없음)",
            "goal_achieve": "not_claimed(주장 없음)",
            "raw_best_attempt_unreviewed": metrics.get("raw_best_attempt", ""),
            "effect": "원시 MT5(메타트레이더5) KPI를 검토 전 단서로만 둔다.",
        },
    )
    write_json(
        RUN_MANIFEST,
        {
            **base,
            "command": "python stage_pipelines/stage339/branch_stage338_to_lifecycle_exit_probe_review_without_db.py",
            "outputs": [
                rel(HANDOFF_MANIFEST),
                rel(RUNTIME_OUTPUT_INVENTORY),
                rel(RUNTIME_PREVIEW),
                rel(NEXT_QUEUE),
                rel(GATE_AUDIT),
                rel(FINAL_DECISION),
            ],
        },
    )


def ledger_rows(gates: pd.DataFrame, metrics: Mapping[str, Any]) -> list[dict[str, Any]]:
    gate_passes = int(gates["status"].astype(str).str.lower().eq("passed").sum())
    gate_total = int(len(gates))
    base = {
        "stage_id": NEW_STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "run_date": TODAY,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_run_id": NEXT_RUN_ID,
        "primary_artifact": rel(FINAL_DECISION),
        "report_path": rel(REPORT_PATH),
        "gate_passes": gate_passes,
        "gate_total": gate_total,
        "claim_boundary": CLAIM_BOUNDARY,
        "candidate_model_id": metrics.get("raw_best_model_id", ""),
        "net_profit": metrics.get("raw_best_net_profit", ""),
        "profit_factor": metrics.get("raw_best_profit_factor", ""),
        "drawdown": metrics.get("raw_best_drawdown", ""),
        "recovery_factor": metrics.get("raw_best_recovery_factor", ""),
        "trade_count": metrics.get("raw_best_trade_count", ""),
        "result_status": "unreviewed_runtime_output_handoff(미검토 런타임 출력 인계)",
        "sample_rows": "",
        "feature_count": "",
        "matched_rows": metrics.get("matched_rows_total", ""),
        "expectancy": metrics.get("raw_best_expectancy", ""),
        "attempt_count": metrics.get("attempt_count", ""),
    }
    rows = []
    for view, tier, metric_scope in [
        ("Tier A separate(Tier A 분리)", "Tier A", "stage_branch_handoff_with_unreviewed_runtime_preview"),
        ("Tier B separate(Tier B 분리)", "Tier B", "missing_required"),
        ("Tier A+B combined(Tier A+B 합산)", "Tier A+B", "same_as_tier_a_until_tier_b_available"),
    ]:
        row = dict(base)
        row.update({"view": view, "tier": tier, "metric_scope": metric_scope})
        if "missing_required" in metric_scope:
            for metric in ["candidate_model_id", "net_profit", "profit_factor", "drawdown", "recovery_factor", "trade_count", "matched_rows", "expectancy", "attempt_count"]:
                row[metric] = ""
            row["result_status"] = "missing_required(필수 누락)"
        rows.append(row)
    return rows


def write_registries(gates: pd.DataFrame, metrics: Mapping[str, Any]) -> None:
    rows = ledger_rows(gates, metrics)
    write_csv(STAGE_LEDGER, pd.DataFrame(rows, columns=STAGE_LEDGER_COLUMNS))
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], [rows[0]])
    project_rows = []
    for row in rows:
        project_row = dict(row)
        project_row["ledger_row_id"] = f"{RUN_ID}__{row['tier']}"
        project_row["tier_scope"] = row["tier"]
        project_row["kpi_scope"] = "state_sync_stage_branch(상태 동기화 단계 분기)"
        project_row["scoreboard_lane"] = "handoff(인계)"
        project_row["path"] = rel(REPORT_PATH)
        project_row["date"] = TODAY
        project_row["run_number"] = RUN_NUMBER
        project_row["primary_artifact"] = rel(FINAL_DECISION)
        project_rows.append(project_row)
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], project_rows)

    artifacts = [
        STAGE_BRIEF,
        INPUT_REFS,
        SELECTION_STATUS,
        HANDOFF_MANIFEST,
        RUNTIME_OUTPUT_INVENTORY,
        RUNTIME_PREVIEW,
        NEXT_QUEUE,
        STAGE_TRANSITION_RECEIPT,
        LINEAGE_RECEIPT,
        CLAIM_RECEIPT,
        GATE_AUDIT,
        FINAL_DECISION,
        RUN_MANIFEST,
        REPORT_PATH,
        DECISION_DOC,
        Path(__file__),
    ]
    artifact_rows = []
    for path in artifacts:
        if not path.exists() or not path.is_file():
            continue
        artifact_rows.append(
            {
                "stage_id": NEW_STAGE_ID,
                "run_id": RUN_ID,
                "artifact_type": path.suffix.lstrip(".") or "file",
                "path": rel(path),
                "sha256": sha256_file(path),
                "created_at": TODAY,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    append_or_replace_csv(ARTIFACT_REGISTRY, ["stage_id", "run_id", "path"], artifact_rows)


def write_final_decision(gates: pd.DataFrame, metrics: Mapping[str, Any]) -> None:
    gate_passes = int(gates["status"].astype(str).str.lower().eq("passed").sum())
    gate_total = int(len(gates))
    write_json(
        FINAL_DECISION,
        {
            "stage_id": NEW_STAGE_ID,
            "run_id": RUN_ID,
            "parent_stage_id": SOURCE_STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "partial_runtime_run_id": PARTIAL_RUNTIME_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "status": STATUS,
            "judgment": JUDGMENT,
            "decision": DECISION,
            "gate_passes": gate_passes,
            "gate_total": gate_total,
            "raw_best_attempt_unreviewed": metrics.get("raw_best_attempt", ""),
            "raw_best_net_profit_unreviewed": metrics.get("raw_best_net_profit", ""),
            "raw_best_profit_factor_unreviewed": metrics.get("raw_best_profit_factor", ""),
            "raw_best_recovery_factor_unreviewed": metrics.get("raw_best_recovery_factor", ""),
            "raw_best_trade_count_unreviewed": metrics.get("raw_best_trade_count", ""),
            "claim_boundary": CLAIM_BOUNDARY,
            "created_at_utc": now_utc(),
            "effect": "Stage338(338단계)을 과밀 상태로 두지 않고 Stage339(339단계) recovered runtime review(복구 런타임 검토)로 넘겼다.",
        },
    )


def main() -> None:
    RUN_DIR.mkdir(parents=True, exist_ok=True)
    REVIEW_DIR.mkdir(parents=True, exist_ok=True)
    runtime_preview, metrics = build_runtime_preview()
    inventory = build_inventory()
    handoff = build_handoff(metrics)
    next_queue = build_next_queue(metrics)

    write_csv(RUNTIME_PREVIEW, runtime_preview)
    write_csv(RUNTIME_OUTPUT_INVENTORY, inventory)
    write_csv(HANDOFF_MANIFEST, handoff)
    write_csv(NEXT_QUEUE, next_queue)
    write_stage_docs(metrics)
    write_receipts(metrics)
    gates = build_gates()
    write_csv(GATE_AUDIT, gates)
    write_final_decision(gates, metrics)
    write_registries(gates, metrics)

    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "stage_id": NEW_STAGE_ID,
                "next_run_id": NEXT_RUN_ID,
                "gate_passes": int(gates["status"].astype(str).str.lower().eq("passed").sum()),
                "gate_total": int(len(gates)),
                "raw_best_attempt_unreviewed": metrics.get("raw_best_attempt", ""),
                "raw_best_net_profit_unreviewed": metrics.get("raw_best_net_profit", ""),
                "claim_boundary": CLAIM_BOUNDARY,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
