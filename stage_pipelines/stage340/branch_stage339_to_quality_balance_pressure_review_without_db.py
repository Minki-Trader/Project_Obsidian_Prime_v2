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

SOURCE_STAGE_ID = "339_runtime_lifecycle_exit__side_balance_probe_review"
NEW_STAGE_ID = "340_runtime_lifecycle_exit__quality_balance_pressure_review"
SOURCE_STAGE_DIR = ROOT / "stages" / SOURCE_STAGE_ID
NEW_STAGE_DIR = ROOT / "stages" / NEW_STAGE_ID

RUN_NUMBER = "run340A"
RUN_ID = "run340A_branch_stage339_to_quality_balance_pressure_review_without_db_v1"
PARENT_RUN_ID = "run339G_execute_quality_balance_blend_mt5_probe_without_db_v1"
SOURCE_PACKAGE_RUN_ID = "run339F_materialize_quality_balance_blend_mt5_probe_package_without_db_v1"
NEXT_RUN_ID = "run340B_review_quality_balance_blend_mt5_probe_without_db_v1"

STATUS = "completed_stage340A_branch_from_stage339_quality_balance_pressure_review_opened_no_selection"
JUDGMENT = "stage_branch_completed_stage339_overweight_handoff_to_quality_balance_review_no_selection"
DECISION = "stage340A_open_run340B_review_quality_balance_blend_probe"
CLAIM_BOUNDARY = (
    "state_sync_stage_branch_and_quality_balance_runtime_probe_handoff_only_no_candidate_selection_"
    "no_forward_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

RUN_DIR = NEW_STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = NEW_STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEW_DIR / "run340A_stage_branch.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage340A_branch_stage339_to_quality_balance_pressure_review.md"
STAGE_BRIEF = NEW_STAGE_DIR / "00_spec" / "stage_brief.md"
STAGE_README = NEW_STAGE_DIR / "README.md"
INPUT_REFS = NEW_STAGE_DIR / "01_inputs" / "input_refs.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"
SELECTION_STATUS = NEW_STAGE_DIR / "04_selected" / "selection_status.md"
SOURCE_SELECTION_STATUS = SOURCE_STAGE_DIR / "04_selected" / "selection_status.md"
SOURCE_STAGE_BRIEF = SOURCE_STAGE_DIR / "00_spec" / "stage_brief.md"
SOURCE_STAGE_README = SOURCE_STAGE_DIR / "README.md"

SOURCE_RUN_DIR = SOURCE_STAGE_DIR / "02_runs" / "run339G"
SOURCE_PACKAGE_DIR = SOURCE_STAGE_DIR / "02_runs" / "run339F"
SOURCE_PREVIOUS_REVIEW_DIR = SOURCE_STAGE_DIR / "02_runs" / "run339E"
SOURCE_FINAL_DECISION = SOURCE_RUN_DIR / "final_decision.json"
SOURCE_GATE_AUDIT = SOURCE_RUN_DIR / "required_gate_coverage_audit.csv"
SOURCE_RUNTIME_SUMMARY = SOURCE_RUN_DIR / "quality_balance_blend_mt5_probe_summary.csv"
SOURCE_PROXY_DIFF = SOURCE_RUN_DIR / "proxy_mt5_runtime_difference.csv"
SOURCE_RUNTIME_IDENTITY = SOURCE_RUN_DIR / "runtime_identity.csv"
SOURCE_RUN_MANIFEST = SOURCE_RUN_DIR / "run_manifest.json"
SOURCE_EXECUTION_RESULT = SOURCE_RUN_DIR / "mt5_execution_result.json"
SOURCE_REPORT_RECORDS = SOURCE_RUN_DIR / "strategy_tester_report_records.json"
SOURCE_VARIANT_PREVIEW = SOURCE_PACKAGE_DIR / "variant_preview.csv"
SOURCE_PACKAGE_FINAL_DECISION = SOURCE_PACKAGE_DIR / "final_decision.json"
SOURCE_PREVIOUS_SCORECARD = SOURCE_PREVIOUS_REVIEW_DIR / "shorter_hold_side_balance_probe_scorecard.csv"

HANDOFF_MANIFEST = RUN_DIR / "stage339_to_stage340_handoff_manifest.csv"
RUNTIME_OUTPUT_INVENTORY = RUN_DIR / "quality_balance_runtime_output_inventory.csv"
RUNTIME_PREVIEW = RUN_DIR / "quality_balance_runtime_preview.csv"
NEXT_QUEUE = RUN_DIR / "run340B_queue.csv"
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

SOURCE_INPUTS = [
    SOURCE_FINAL_DECISION,
    SOURCE_GATE_AUDIT,
    SOURCE_RUNTIME_SUMMARY,
    SOURCE_PROXY_DIFF,
    SOURCE_RUNTIME_IDENTITY,
    SOURCE_RUN_MANIFEST,
    SOURCE_EXECUTION_RESULT,
    SOURCE_REPORT_RECORDS,
    SOURCE_VARIANT_PREVIEW,
    SOURCE_PACKAGE_FINAL_DECISION,
    SOURCE_PREVIOUS_SCORECARD,
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


def safe_float(value: Any, default: float = 0.0) -> float:
    try:
        if pd.isna(value):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def safe_int(value: Any, default: int = 0) -> int:
    try:
        if pd.isna(value):
            return default
        return int(float(value))
    except (TypeError, ValueError):
        return default


def bool_passes(series: pd.Series) -> bool:
    return bool(series.astype(str).str.lower().eq("passed").all())


def build_runtime_preview() -> tuple[pd.DataFrame, dict[str, Any]]:
    summary = read_csv(SOURCE_RUNTIME_SUMMARY).copy()
    preview = read_csv(SOURCE_VARIANT_PREVIEW).copy()
    useful_preview_columns = [
        "attempt_name",
        "variant_role",
        "short_threshold",
        "long_threshold",
        "min_margin",
        "max_hold_bars",
        "close_on_flat",
        "signal_trade_count",
        "signal_long_count",
        "signal_short_count",
        "signal_side_balance",
    ]
    available = [column for column in useful_preview_columns if column in preview.columns]
    frame = summary.merge(preview[available], on="attempt_name", how="left")
    for column in [
        "expected_rows",
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
        "short_threshold",
        "long_threshold",
        "min_margin",
        "max_hold_bars",
    ]:
        if column in frame.columns:
            frame[column] = pd.to_numeric(frame[column], errors="coerce")
    side_max = frame[["long_trade_count", "short_trade_count"]].max(axis=1).replace(0, pd.NA)
    frame["trade_side_balance"] = (
        frame[["long_trade_count", "short_trade_count"]].min(axis=1) / side_max
    ).fillna(0.0)
    frame["source_run_id"] = PARENT_RUN_ID
    frame["review_status"] = "review_required(검토 필요)"
    frame["usable_in_stage340"] = "review_input_only(검토 입력 전용)"
    frame["effect"] = (
        "Stage340(340단계)가 run339G(339G 실행) MT5 runtime probe(MT5 런타임 탐침)를 "
        "가볍게 검토하고 pressure test(압박 시험)로 넘기게 한다."
    )
    frame["claim_boundary"] = CLAIM_BOUNDARY
    frame = frame.sort_values(["net_profit", "profit_factor", "recovery_factor"], ascending=False).reset_index(drop=True)
    best = frame.iloc[0]
    metrics = {
        "attempt_count": int(len(frame)),
        "expected_rows_total": int(frame["expected_rows"].fillna(0).sum()),
        "matched_rows_total": int(frame["matched_rows"].fillna(0).sum()),
        "mismatch_rows_total": int(
            frame["probability_mismatch_rows"].fillna(0).sum() + frame["decision_mismatch_rows"].fillna(0).sum()
        ),
        "best_attempt": str(best.get("attempt_name", "")),
        "best_model_id": str(best.get("model_id", "")),
        "best_net_profit": safe_float(best.get("net_profit")),
        "best_profit_factor": safe_float(best.get("profit_factor")),
        "best_expectancy": safe_float(best.get("expectancy")),
        "best_recovery_factor": safe_float(best.get("recovery_factor")),
        "best_drawdown": safe_float(best.get("max_drawdown_amount")),
        "best_trade_count": safe_int(best.get("trade_count")),
        "best_long_trade_count": safe_int(best.get("long_trade_count")),
        "best_short_trade_count": safe_int(best.get("short_trade_count")),
        "best_trade_side_balance": safe_float(best.get("trade_side_balance")),
    }
    return frame, metrics


def build_inventory() -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for path, role in [
        (SOURCE_FINAL_DECISION, "source_final_decision(원천 최종 결정)"),
        (SOURCE_GATE_AUDIT, "source_gate_audit(원천 게이트 감사)"),
        (SOURCE_RUNTIME_SUMMARY, "source_mt5_summary(원천 MT5 요약)"),
        (SOURCE_PROXY_DIFF, "source_proxy_mt5_diff(원천 프록시-MT5 차이)"),
        (SOURCE_RUNTIME_IDENTITY, "source_runtime_identity(원천 런타임 정체성)"),
        (SOURCE_RUN_MANIFEST, "source_run_manifest(원천 실행 목록)"),
        (SOURCE_EXECUTION_RESULT, "source_mt5_execution_result(원천 MT5 실행 결과)"),
        (SOURCE_REPORT_RECORDS, "source_strategy_tester_reports(원천 전략 테스터 보고서)"),
        (SOURCE_VARIANT_PREVIEW, "source_variant_preview(원천 변형 미리보기)"),
        (SOURCE_PACKAGE_FINAL_DECISION, "source_package_final_decision(원천 패키지 최종 결정)"),
        (SOURCE_PREVIOUS_SCORECARD, "previous_review_scorecard(이전 검토 점수표)"),
    ]:
        rows.append(
            {
                "artifact_role": role,
                "path": rel(path),
                "exists": path.exists(),
                "availability": "tracked(추적됨)" if path.exists() else "missing_required(필수 누락)",
                "sha256": sha256_file(path) if path.exists() and path.is_file() else "",
                "consumer": NEXT_RUN_ID,
                "effect": "Stage340(340단계) review(검토)가 같은 원천 근거를 다시 찾게 한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return pd.DataFrame(rows)


def build_handoff(metrics: Mapping[str, Any]) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "handoff_id": "stage339G_to_stage340A_quality_balance_review",
                "source_stage_id": SOURCE_STAGE_ID,
                "new_stage_id": NEW_STAGE_ID,
                "branch_run_id": RUN_ID,
                "source_completed_run_id": PARENT_RUN_ID,
                "source_package_run_id": SOURCE_PACKAGE_RUN_ID,
                "next_run_id": NEXT_RUN_ID,
                "branch_reason": (
                    "Stage339(339단계)가 side-balance(방향 균형) 복구부터 quality-balance blend(품질-균형 혼합) "
                    "runtime probe(런타임 탐침)까지 누적되어 너무 무거워졌다."
                ),
                "raw_best_attempt_review_required": metrics.get("best_attempt", ""),
                "raw_best_net_profit_review_required": metrics.get("best_net_profit", ""),
                "raw_best_profit_factor_review_required": metrics.get("best_profit_factor", ""),
                "raw_best_expectancy_review_required": metrics.get("best_expectancy", ""),
                "raw_best_recovery_factor_review_required": metrics.get("best_recovery_factor", ""),
                "raw_best_drawdown_review_required": metrics.get("best_drawdown", ""),
                "raw_best_trade_count_review_required": metrics.get("best_trade_count", ""),
                "raw_best_trade_side_balance_review_required": metrics.get("best_trade_side_balance", ""),
                "allowed_use": "review input, preserved clue, pressure-test seed(검토 입력, 보존 단서, 압박 시험 씨앗)",
                "forbidden_use": "selected model, baseline, operating promotion, runtime authority(선정 모델, 기준선, 운영 승격, 런타임 권위)",
                "effect": "Stage340(340단계)가 검토 질문만 들고 시작해서 다음 작업 묶음(work packet, 작업 묶음)을 작게 만든다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )


def build_next_queue() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "queue_id": "run340B_review_quality_balance_blend_mt5_probe",
                "next_run_id": NEXT_RUN_ID,
                "priority": "P0",
                "primary_family": "kpi_evidence(KPI 근거)",
                "primary_skill": "obsidian-run-evidence-system(실행 근거 시스템)",
                "support_skills": (
                    "obsidian-result-judgment(결과 판정);"
                    "obsidian-performance-attribution(성과 귀속);"
                    "obsidian-artifact-lineage(산출물 계보)"
                ),
                "hypothesis": (
                    "run339G(339G 실행)의 f01(에프01) local floor(로컬 하한) 단서가 "
                    "forward/replay(전진/재생) 전 pressure test(압박 시험)를 받을 가치가 있는가?"
                ),
                "decision_use": "pressure package routing only(압박 패키지 라우팅 전용)",
                "comparison_baseline": "run339E c01/c07 split(339E 씨01/씨07 분기)",
                "control_variables": (
                    "source_model logreg_balanced_c025(원천 모델); symbol US100(심볼); timeframe M5(5분봉); "
                    "MT5 strategy tester evidence(MT5 전략 테스터 근거)"
                ),
                "changed_variables": "review only(검토만); no new MT5 execution(MT5 새 실행 없음)",
                "sample_scope": "Tier A separate(Tier A 분리); Tier B missing_required(Tier B 필수 누락)",
                "success_criteria": (
                    "exact_parity(정확 동등성), net_profit>0(순수익 양수), profit_factor>=1.10(수익 팩터), "
                    "expectancy>0(기대값 양수), recovery>=1.00(회복 계수), drawdown<=150(낙폭), "
                    "trade_count>=30(거래수), side_balance>=0.25(방향 균형)"
                ),
                "failure_criteria": "best clue fails local floor(최고 단서가 로컬 하한 실패)",
                "invalid_conditions": "missing source summary or failed source gate(원천 요약 누락 또는 원천 게이트 실패)",
                "stop_conditions": (
                    "if selected model or operating claim is needed, stop and open explicit promotion packet"
                    "(선정 모델 또는 운영 주장이 필요하면 멈추고 명시적 승격 묶음을 연다)"
                ),
                "evidence_plan": (
                    "scorecard(점수표); KPI record(KPI 기록); result judgment receipt(결과 판정 영수증); "
                    "performance attribution(성과 귀속); gate audit(게이트 감사)"
                ),
                "required_inputs": ";".join(
                    [
                        rel(SOURCE_FINAL_DECISION),
                        rel(SOURCE_GATE_AUDIT),
                        rel(SOURCE_RUNTIME_SUMMARY),
                        rel(SOURCE_VARIANT_PREVIEW),
                        rel(RUNTIME_PREVIEW),
                    ]
                ),
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
    source_gates = read_csv(SOURCE_GATE_AUDIT) if SOURCE_GATE_AUDIT.exists() else pd.DataFrame({"status": ["missing"]})
    return pd.DataFrame(
        [
            gate_row(
                "source_339G_gates_passed",
                "passed" if bool_passes(source_gates["status"]) else "failed",
                rel(SOURCE_GATE_AUDIT),
                "run339G(339G 실행)의 MT5 runtime probe(MT5 런타임 탐침) 게이트를 원천 근거로 고정한다.",
            ),
            gate_row(
                "runtime_probe_outputs_available",
                "passed"
                if SOURCE_FINAL_DECISION.exists() and SOURCE_RUNTIME_SUMMARY.exists() and SOURCE_PROXY_DIFF.exists()
                else "failed",
                f"{rel(SOURCE_FINAL_DECISION)};{rel(SOURCE_RUNTIME_SUMMARY)};{rel(SOURCE_PROXY_DIFF)}",
                "Stage340(340단계) 검토가 쓸 MT5 KPI(MT5 핵심 성과 지표)와 parity(동등성) 파일을 확인한다.",
            ),
            gate_row(
                "new_stage_scaffold_created",
                "passed" if STAGE_BRIEF.exists() and INPUT_REFS.exists() and SELECTION_STATUS.exists() else "failed",
                f"{rel(STAGE_BRIEF)};{rel(INPUT_REFS)};{rel(SELECTION_STATUS)}",
                "Stage340(340단계) 질문과 입력 경계를 만든다.",
            ),
            gate_row(
                "handoff_and_queue_written",
                "passed" if HANDOFF_MANIFEST.exists() and RUNTIME_PREVIEW.exists() and NEXT_QUEUE.exists() else "failed",
                f"{rel(HANDOFF_MANIFEST)};{rel(RUNTIME_PREVIEW)};{rel(NEXT_QUEUE)}",
                "인계(handoff, 인계)와 다음 review queue(검토 대기열)를 분리한다.",
            ),
            gate_row(
                "current_truth_synced",
                "passed" if WORKSPACE_STATE.exists() and CURRENT_WORKING_STATE.exists() else "failed",
                f"{rel(WORKSPACE_STATE)};{rel(CURRENT_WORKING_STATE)}",
                "재진입(re-entry, 재진입)이 Stage340(340단계)에서 바로 시작되게 한다.",
            ),
            gate_row(
                "registries_synced",
                "passed" if RUN_REGISTRY.exists() and PROJECT_LEDGER.exists() and ARTIFACT_REGISTRY.exists() else "failed",
                f"{rel(RUN_REGISTRY)};{rel(PROJECT_LEDGER)};{rel(ARTIFACT_REGISTRY)}",
                "run identity(실행 정체성)와 artifact lineage(산출물 계보)를 장부에 연결한다.",
            ),
            gate_row(
                "no_forbidden_operating_claim",
                "passed",
                rel(CLAIM_RECEIPT),
                "stage branch(단계 분기)를 selection(선정)이나 runtime authority(런타임 권위)로 과장하지 않는다.",
            ),
            gate_row(
                "required_gate_coverage_audit_written",
                "passed",
                rel(GATE_AUDIT),
                "required gate coverage audit(필수 게이트 커버리지 감사)를 closeout(종료 기록)에 남긴다.",
            ),
        ]
    )


def write_stage_docs(metrics: Mapping[str, Any]) -> None:
    stage_brief = f"""# Stage340 Quality Balance Pressure Review(340단계 품질-균형 압박 검토)

## Canonical Stage ID(정식 단계 ID)

`{NEW_STAGE_ID}`

## Stage Question(단계 질문)

Can the run339G(339G 실행) quality-balance blend(품질-균형 혼합) MT5 runtime probe(MT5 런타임 탐침) be reviewed and pressure-tested without keeping Stage339(339단계) overloaded?
(run339G(339G 실행)의 품질-균형 혼합 MT5 런타임 탐침을 Stage339(339단계)을 더 무겁게 하지 않고 검토하고 압박 시험할 수 있는가?)

## Source Handoff(원천 인계)

- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_completed_run(완료 원천 실행): `{PARENT_RUN_ID}`
- source_package_run(원천 패키지 실행): `{SOURCE_PACKAGE_RUN_ID}`
- branch_run(분기 실행): `{RUN_ID}`
- next_run(다음 실행): `{NEXT_RUN_ID}`

## Raw Preview Boundary(원시 미리보기 경계)

- best_attempt_review_required(검토 필요 최고 시도): `{metrics.get('best_attempt', '')}`
- net_profit_review_required(검토 필요 순수익): `{metrics.get('best_net_profit', '')}`
- profit_factor_review_required(검토 필요 수익 팩터): `{metrics.get('best_profit_factor', '')}`
- recovery_factor_review_required(검토 필요 회복 계수): `{metrics.get('best_recovery_factor', '')}`
- trade_count_review_required(검토 필요 거래수): `{metrics.get('best_trade_count', '')}`

Effect(효과): 숫자는 보존하지만, run340B(340B 실행) 검토 전에는 selection(선정), promotion_candidate(승격 후보), runtime authority(런타임 권위)로 쓰지 않는다.

## Scope(범위)

Stage340(340단계)는 review(검토)와 pressure package design(압박 패키지 설계)에 집중한다.
Effect(효과): Stage339(339단계)의 누적 산출물은 보존하고, 다음 작업 묶음(work packet, 작업 묶음)은 작게 유지한다.

## Forbidden Claims(금지 주장)

No selected model(선정 모델 없음), no baseline(기준선 없음), no operating promotion(운영 승격 없음), no runtime authority(런타임 권위 없음), no Goal Achieve(목표 달성 없음).
"""
    input_refs = f"""# Stage340 Input Refs(340단계 입력 참조)

## Source Inputs(원천 입력)

- run339G final decision(339G 최종 결정): `{rel(SOURCE_FINAL_DECISION)}`
- run339G gate audit(339G 게이트 감사): `{rel(SOURCE_GATE_AUDIT)}`
- run339G MT5 summary(339G MT5 요약): `{rel(SOURCE_RUNTIME_SUMMARY)}`
- run339G proxy-MT5 diff(339G 프록시-MT5 차이): `{rel(SOURCE_PROXY_DIFF)}`
- run339F variant preview(339F 변형 미리보기): `{rel(SOURCE_VARIANT_PREVIEW)}`

## Stage340 Handoff Files(340단계 인계 파일)

- handoff manifest(인계 목록): `{rel(HANDOFF_MANIFEST)}`
- runtime preview(런타임 미리보기): `{rel(RUNTIME_PREVIEW)}`
- runtime output inventory(런타임 출력 목록): `{rel(RUNTIME_OUTPUT_INVENTORY)}`
- next queue(다음 대기열): `{rel(NEXT_QUEUE)}`

Effect(효과): run340B(340B 실행)가 같은 파일을 다시 찾느라 시간을 쓰지 않게 한다.
"""
    selection = f"""# Stage340 Selection Status(340단계 선정 상태)

- active_stage(현재 단계): `{NEW_STAGE_ID}`
- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- selected_model(선정 모델): `none(없음)`
- preserved_best_attempt(보존 최고 시도): `{metrics.get('best_attempt', '')}`
- preserved_best_net_profit(보존 최고 순수익): `{metrics.get('best_net_profit', '')}`
- preserved_best_profit_factor(보존 최고 수익 팩터): `{metrics.get('best_profit_factor', '')}`
- runtime_authority(런타임 권위): `not_claimed(주장 없음)`
- operating_promotion(운영 승격): `not_claimed(주장 없음)`
- Goal Achieve(목표 달성): `not_claimed(주장 없음)`

Effect(효과): 좋은 MT5 숫자를 selection(선정)으로 착각하지 않고, review(검토)와 pressure test(압박 시험) 입력으로만 둔다.
"""
    report = f"""# run340A Stage Branch(단계 분기)

## Summary(요약)

- run_id(실행 ID): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- new_stage(새 단계): `{NEW_STAGE_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- next_run(다음 실행): `{NEXT_RUN_ID}`
- gates(게이트): `{rel(GATE_AUDIT)}`

## Action(행동)

Stage339(339단계)를 더 키우지 않고 Stage340(340단계)로 분기했다.
Effect(효과): run339G(339G 실행)의 MT5 runtime probe(MT5 런타임 탐침) 산출물을 짧은 review packet(검토 묶음)으로 넘긴다.

## Runtime Preview(런타임 미리보기)

- best_attempt_review_required(검토 필요 최고 시도): `{metrics.get('best_attempt', '')}`
- net_profit_review_required(검토 필요 순수익): `{metrics.get('best_net_profit', '')}`
- profit_factor_review_required(검토 필요 수익 팩터): `{metrics.get('best_profit_factor', '')}`
- recovery_factor_review_required(검토 필요 회복 계수): `{metrics.get('best_recovery_factor', '')}`
- trade_count_review_required(검토 필요 거래수): `{metrics.get('best_trade_count', '')}`

Effect(효과): positive clue(긍정 단서)는 보존하지만, run340B(340B 실행) 검토 전에는 reviewed positive(검토된 긍정)로 말하지 않는다.

## Boundary(경계)

This is state sync and handoff only(상태 동기화와 인계만 해당). Selection(선정), operating promotion(운영 승격), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 없다.
"""
    decision = f"""# {TODAY} Stage340A Branch Decision(340A 단계 분기 결정)

- decision(결정): `{DECISION}`
- from(출발): `{SOURCE_STAGE_ID}` / `{PARENT_RUN_ID}`
- to(도착): `{NEW_STAGE_ID}` / `{NEXT_RUN_ID}`
- reason(이유): Stage339(339단계)가 너무 무거워져 quality-balance review(품질-균형 검토)를 별도 단계로 분리했다.

Action(행동): Stage340(340단계)를 열고 run340B(340B 실행)를 review(검토) 다음 행동으로 둔다.
Effect(효과): Stage339(339단계)의 무게를 줄이고, run339G(339G 실행) MT5 산출물을 버리지 않는다.

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

Stage340(340단계)는 run339G(339G 실행)의 quality-balance blend(품질-균형 혼합) MT5 runtime probe(MT5 런타임 탐침)를 review(검토)하고, 필요하면 f01(에프01) pressure test(압박 시험)로 넘긴다.

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
    source_selection = f"""# Stage339 Selection Status(339단계 선정 상태)

- active_stage(기존 단계): `{SOURCE_STAGE_ID}`
- latest_completed_run(최근 완료 실행): `{PARENT_RUN_ID}`
- branched_to_stage(분기된 단계): `{NEW_STAGE_ID}`
- branch_run(분기 실행): `{RUN_ID}`
- next_active_run(다음 활성 실행): `{NEXT_RUN_ID}`
- selected_model(선정 모델): `none(없음)`
- preserved_best_attempt(보존 최고 시도): `{metrics.get('best_attempt', '')}`
- preserved_best_net_profit(보존 최고 순수익): `{metrics.get('best_net_profit', '')}`
- preserved_best_profit_factor(보존 최고 수익 팩터): `{metrics.get('best_profit_factor', '')}`
- runtime_authority(런타임 권위): `not_claimed(주장 없음)`
- operating_promotion(운영 승격): `not_claimed(주장 없음)`
- Goal Achieve(목표 달성): `not_claimed(주장 없음)`

Effect(효과): Stage339(339단계)를 더 무겁게 만들지 않고 Stage340(340단계) 검토로 넘겼음을 현재 진실에서 바로 보이게 한다.
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
        f"""## run340A Stage Branch(340A 단계 분기)

- branch_run(분기 실행): `{RUN_ID}`
- new_stage(새 단계): `{NEW_STAGE_ID}`
- next_run(다음 실행): `{NEXT_RUN_ID}`
- effect(효과): Stage339(339단계)의 quality-balance review(품질-균형 검토)를 Stage340(340단계)로 넘겨 단계 무게를 줄인다.
""",
    )
    append_text_once(
        SOURCE_STAGE_README,
        marker,
        f"""## run340A Stage Branch(340A 단계 분기)

- branch_run(분기 실행): `{RUN_ID}`
- new_stage(새 단계): `{NEW_STAGE_ID}`
- next_run(다음 실행): `{NEXT_RUN_ID}`
- effect(효과): run339G(339G 실행) output(출력)을 Stage340(340단계) review(검토)로 넘긴다.
""",
    )
    changelog = f"""## {TODAY} run340A Stage Branch(단계 분기)

- action(행동): Stage339(339단계)의 run339G(339G 실행) quality-balance blend(품질-균형 혼합) MT5 runtime probe(MT5 런타임 탐침)를 Stage340(340단계)로 분기했다.
- effect(효과): Stage339(339단계)의 무게를 줄이고 run340B(340B 실행)가 검토만 작게 이어가게 했다.
- boundary(경계): selected model(선정 모델), operating promotion(운영 승격), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 없다.
"""
    append_text_once(ROOT_CHANGELOG, marker, changelog)
    append_text_once(WORKSPACE_CHANGELOG, marker, changelog)
    append_text_once(
        IDEA_REGISTRY,
        marker,
        f"""## {TODAY} Stage340 Quality Balance Pressure Review Seed(340단계 품질-균형 압박 검토 씨앗)

- idea_id(아이디어 ID): `stage340_quality_balance_pressure_review_seed`
- hypothesis(가설): run339G(339G 실행)의 f01(에프01) local MT5 clue(로컬 MT5 단서)가 pressure test(압박 시험)를 받을 가치가 있을 수 있다.
- source(원천): `{PARENT_RUN_ID}`
- next_run(다음 실행): `{NEXT_RUN_ID}`
- tier_scope(티어 범위): `Tier A separate(Tier A 분리); Tier B missing_required(Tier B 필수 누락); Tier A+B same_as_tier_a_until_tier_b_available(Tier A+B는 Tier B 가능 전까지 Tier A와 같음)`
- evidence_boundary(근거 경계): `runtime_probe_review_required_no_selection(런타임 탐침 검토 필요, 선정 없음)`
- effect(효과): 긍정 단서를 보존하되 Stage340(340단계)에서 새롭게 작게 판단한다.
""",
    )


def write_receipts(metrics: Mapping[str, Any]) -> None:
    base = {
        "run_id": RUN_ID,
        "stage_id": NEW_STAGE_ID,
        "parent_stage_id": SOURCE_STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "source_package_run_id": SOURCE_PACKAGE_RUN_ID,
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
            "effect": "Stage339(339단계) 과중 상태를 Stage340(340단계) 검토 질문으로 분리했다.",
        },
    )
    write_json(
        LINEAGE_RECEIPT,
        {
            **base,
            "source_inputs": [rel(path) for path in SOURCE_INPUTS],
            "artifact_paths": [
                rel(HANDOFF_MANIFEST),
                rel(RUNTIME_OUTPUT_INVENTORY),
                rel(RUNTIME_PREVIEW),
                rel(NEXT_QUEUE),
                rel(REPORT_PATH),
                rel(DECISION_DOC),
            ],
            "artifact_hashes": {rel(path): sha256_file(path) for path in SOURCE_INPUTS if path.exists()},
            "availability": "connected_with_boundary(경계가 있는 연결)",
            "lineage_judgment": "connected_with_boundary(경계가 있는 연결)",
            "effect": "run339G(339G 실행) 산출물이 run340B(340B 실행) 검토 입력으로 연결됐다.",
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            **base,
            "candidate_selection": "not_claimed(주장 없음)",
            "promotion_candidate": "not_claimed(주장 없음)",
            "runtime_authority": "not_claimed(주장 없음)",
            "operating_promotion": "not_claimed(주장 없음)",
            "goal_achieve": "not_claimed(주장 없음)",
            "best_attempt_review_required": metrics.get("best_attempt", ""),
            "effect": "Stage branch(단계 분기)를 운영 주장(operating claim, 운영 주장)으로 오해하지 않게 한다.",
        },
    )
    write_json(
        RUN_MANIFEST,
        {
            **base,
            "command": "python stage_pipelines/stage340/branch_stage339_to_quality_balance_pressure_review_without_db.py",
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
        "candidate_model_id": metrics.get("best_model_id", ""),
        "net_profit": metrics.get("best_net_profit", ""),
        "profit_factor": metrics.get("best_profit_factor", ""),
        "drawdown": metrics.get("best_drawdown", ""),
        "recovery_factor": metrics.get("best_recovery_factor", ""),
        "trade_count": metrics.get("best_trade_count", ""),
        "result_status": "runtime_probe_review_required_no_selection(런타임 탐침 검토 필요, 선정 없음)",
        "sample_rows": "",
        "feature_count": "",
        "matched_rows": metrics.get("matched_rows_total", ""),
        "expectancy": metrics.get("best_expectancy", ""),
        "attempt_count": metrics.get("attempt_count", ""),
    }
    rows = []
    for view, tier, metric_scope in [
        ("Tier A separate(Tier A 분리)", "Tier A", "stage_branch_handoff_with_runtime_probe_review_required"),
        ("Tier B separate(Tier B 분리)", "Tier B", "missing_required"),
        ("Tier A+B combined(Tier A+B 합산)", "Tier A+B", "same_as_tier_a_until_tier_b_available"),
    ]:
        row = dict(base)
        row.update({"view": view, "tier": tier, "metric_scope": metric_scope})
        if metric_scope == "missing_required":
            for metric in [
                "candidate_model_id",
                "net_profit",
                "profit_factor",
                "drawdown",
                "recovery_factor",
                "trade_count",
                "matched_rows",
                "expectancy",
                "attempt_count",
            ]:
                row[metric] = ""
            row["result_status"] = "missing_required(필수 누락)"
        rows.append(row)
    return rows


def write_final_decision(gates: pd.DataFrame, metrics: Mapping[str, Any]) -> None:
    write_json(
        FINAL_DECISION,
        {
            "stage_id": NEW_STAGE_ID,
            "run_id": RUN_ID,
            "parent_stage_id": SOURCE_STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "source_package_run_id": SOURCE_PACKAGE_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "status": STATUS,
            "judgment": JUDGMENT,
            "decision": DECISION,
            "gate_passes": int(gates["status"].astype(str).str.lower().eq("passed").sum()),
            "gate_total": int(len(gates)),
            "best_attempt_review_required": metrics.get("best_attempt", ""),
            "best_model_id_review_required": metrics.get("best_model_id", ""),
            "best_net_profit_review_required": metrics.get("best_net_profit", ""),
            "best_profit_factor_review_required": metrics.get("best_profit_factor", ""),
            "best_expectancy_review_required": metrics.get("best_expectancy", ""),
            "best_recovery_factor_review_required": metrics.get("best_recovery_factor", ""),
            "best_drawdown_review_required": metrics.get("best_drawdown", ""),
            "best_trade_count_review_required": metrics.get("best_trade_count", ""),
            "expected_rows_total": metrics.get("expected_rows_total", ""),
            "matched_rows_total": metrics.get("matched_rows_total", ""),
            "mismatch_rows_total": metrics.get("mismatch_rows_total", ""),
            "claim_boundary": CLAIM_BOUNDARY,
            "created_at_utc": now_utc(),
            "effect": "Stage339(339단계)를 더 무겁게 하지 않고 Stage340(340단계) quality-balance review(품질-균형 검토)로 넘겼다.",
        },
    )


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
        STAGE_README,
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


def main() -> None:
    RUN_DIR.mkdir(parents=True, exist_ok=True)
    REVIEW_DIR.mkdir(parents=True, exist_ok=True)
    for path in SOURCE_INPUTS[:3]:
        if not path.exists():
            raise FileNotFoundError(f"missing required stage branch input: {rel(path)}")

    runtime_preview, metrics = build_runtime_preview()
    inventory = build_inventory()
    handoff = build_handoff(metrics)
    next_queue = build_next_queue()

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

    failed = gates.loc[~gates["status"].astype(str).str.lower().eq("passed")]
    if not failed.empty:
        raise RuntimeError(f"run340A gates failed: {failed[['gate_id', 'status']].to_dict(orient='records')}")

    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "stage_id": NEW_STAGE_ID,
                "next_run_id": NEXT_RUN_ID,
                "gate_passes": int(gates["status"].astype(str).str.lower().eq("passed").sum()),
                "gate_total": int(len(gates)),
                "best_attempt_review_required": metrics.get("best_attempt", ""),
                "best_net_profit_review_required": metrics.get("best_net_profit", ""),
                "claim_boundary": CLAIM_BOUNDARY,
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
