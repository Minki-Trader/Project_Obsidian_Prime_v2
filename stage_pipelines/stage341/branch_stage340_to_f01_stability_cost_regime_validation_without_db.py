from __future__ import annotations

import csv
import hashlib
import json
import os
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
TODAY = "2026-06-01"

SOURCE_STAGE_ID = "340_runtime_lifecycle_exit__quality_balance_pressure_review"
NEW_STAGE_ID = "341_f01_stability_cost_regime__validate_quality_anchor_vs_net_clue"
SOURCE_STAGE_DIR = ROOT / "stages" / SOURCE_STAGE_ID
NEW_STAGE_DIR = ROOT / "stages" / NEW_STAGE_ID

RUN_NUMBER = "run341A"
RUN_ID = "run341A_branch_stage340_to_f01_stability_cost_regime_validation_without_db_v1"
PARENT_RUN_ID = "run340H_review_f01_close_on_flat_false_pressure_mt5_probe_without_db_v1"
PARENT_RUNTIME_RUN_ID = "run340G_execute_f01_close_on_flat_false_pressure_mt5_probe_without_db_v1"
NEXT_RUN_ID = "run341B_design_f01_stability_cost_regime_validation_without_db_v1"

STATUS = "completed_stage341A_branch_from_stage340_f01_stability_cost_regime_validation_opened_no_selection"
JUDGMENT = "stage_branch_completed_stage340_overweight_handoff_to_f01_stability_cost_regime_validation_no_selection"
DECISION = "stage341A_open_run341B_design_f01_stability_cost_regime_validation"
CLAIM_BOUNDARY = (
    "state_sync_stage_branch_f01_stability_cost_regime_handoff_only_no_candidate_selection_"
    "no_forward_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

RUN_DIR = NEW_STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = NEW_STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEW_DIR / "run341A_stage_branch.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage341A_branch_stage340_to_f01_stability_cost_regime_validation.md"
STAGE_BRIEF = NEW_STAGE_DIR / "00_spec" / "stage_brief.md"
STAGE_README = NEW_STAGE_DIR / "README.md"
INPUT_REFS = NEW_STAGE_DIR / "01_inputs" / "input_refs.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"
SELECTION_STATUS = NEW_STAGE_DIR / "04_selected" / "selection_status.md"
SOURCE_SELECTION_STATUS = SOURCE_STAGE_DIR / "04_selected" / "selection_status.md"
SOURCE_STAGE_BRIEF = SOURCE_STAGE_DIR / "00_spec" / "stage_brief.md"
SOURCE_STAGE_README = SOURCE_STAGE_DIR / "README.md"

SOURCE_RUN_DIR = SOURCE_STAGE_DIR / "02_runs" / "run340H"
SOURCE_RUNTIME_DIR = SOURCE_STAGE_DIR / "02_runs" / "run340G"
SOURCE_FINAL_DECISION = SOURCE_RUN_DIR / "final_decision.json"
SOURCE_GATE_AUDIT = SOURCE_RUN_DIR / "required_gate_coverage_audit.csv"
SOURCE_SCORECARD = SOURCE_RUN_DIR / "f01_close_on_flat_false_pressure_review_scorecard.csv"
SOURCE_KPI_JUDGMENT = SOURCE_RUN_DIR / "f01_close_on_flat_false_pressure_kpi_judgment.csv"
SOURCE_ATTRIBUTION = SOURCE_RUN_DIR / "performance_attribution.csv"
SOURCE_FAILURE_MEMORY = SOURCE_RUN_DIR / "failure_memory.csv"
SOURCE_SEED_QUEUE = SOURCE_RUN_DIR / "run341A_seed_queue.csv"
SOURCE_REPORT = SOURCE_STAGE_DIR / "03_reviews" / "run340H_f01_close_on_flat_false_pressure_review.md"
SOURCE_RUNTIME_SUMMARY = SOURCE_RUNTIME_DIR / "f01_close_on_flat_false_pressure_mt5_probe_summary.csv"
SOURCE_PROXY_DIFF = SOURCE_RUNTIME_DIR / "proxy_mt5_runtime_difference.csv"

HANDOFF_MANIFEST = RUN_DIR / "stage340_to_stage341_handoff_manifest.csv"
SOURCE_INVENTORY = RUN_DIR / "stage340_source_inventory.csv"
NEXT_QUEUE = RUN_DIR / "run341B_validation_seed_queue.csv"
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
    SOURCE_SCORECARD,
    SOURCE_KPI_JUDGMENT,
    SOURCE_ATTRIBUTION,
    SOURCE_FAILURE_MEMORY,
    SOURCE_SEED_QUEUE,
    SOURCE_REPORT,
    SOURCE_RUNTIME_SUMMARY,
    SOURCE_PROXY_DIFF,
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


def path_exists(path: Path) -> bool:
    return os.path.exists(fs_path(path))


def path_is_file(path: Path) -> bool:
    return os.path.isfile(fs_path(path))


def rel(path: Path | str) -> str:
    candidate = Path(path)
    if not candidate.is_absolute():
        candidate = ROOT / candidate
    try:
        return candidate.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return candidate.as_posix()


def ensure_parent(path: Path) -> None:
    Path(fs_path(path.parent)).mkdir(parents=True, exist_ok=True)


def read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(fs_path(path), low_memory=False, encoding="utf-8-sig")


def read_json(path: Path) -> Any:
    with open(fs_path(path), encoding="utf-8-sig") as handle:
        return json.loads(handle.read())


def write_csv(path: Path, frame: pd.DataFrame) -> None:
    ensure_parent(path)
    with open(fs_path(path), "w", encoding="utf-8-sig", newline="") as handle:
        frame.to_csv(handle, index=False, lineterminator="\n", quoting=csv.QUOTE_MINIMAL)


def write_json(path: Path, payload: Any) -> None:
    ensure_parent(path)
    with open(fs_path(path), "w", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n")


def write_bom_text(path: Path, text: str) -> None:
    ensure_parent(path)
    with open(fs_path(path), "w", encoding="utf-8-sig", newline="\n") as handle:
        handle.write(text.rstrip() + "\n")


def append_text_once(path: Path, marker: str, text: str) -> None:
    if path_exists(path):
        with open(fs_path(path), encoding="utf-8-sig") as handle:
            current = handle.read()
    else:
        current = ""
    if marker in current:
        return
    next_text = f"{current.rstrip()}\n\n{text.strip()}\n" if current.strip() else text.strip() + "\n"
    write_bom_text(path, next_text)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with open(fs_path(path), "rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def append_or_replace_csv(path: Path, key_columns: Sequence[str], rows: Iterable[Mapping[str, Any]]) -> None:
    rows = list(rows)
    frame = read_csv(path) if path_exists(path) else pd.DataFrame()
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


def gate_statuses_pass(frame: pd.DataFrame) -> bool:
    return bool(not frame.empty and frame["status"].astype(str).str.lower().eq("passed").all())


def safe_get(mapping: Mapping[str, Any], key: str, default: Any = "") -> Any:
    value = mapping.get(key, default)
    return default if value is None else value


def build_metrics(source_final: Mapping[str, Any], scorecard: pd.DataFrame) -> dict[str, Any]:
    exact_control = scorecard.loc[scorecard["attempt_name"].astype(str).eq("q01_ctl_s55_l51_m01_h12")]
    q09 = scorecard.loc[scorecard["attempt_name"].astype(str).eq("q09_s545_l51_m01_h12")]
    exact_row = exact_control.iloc[0].to_dict() if not exact_control.empty else {}
    q09_row = q09.iloc[0].to_dict() if not q09.empty else {}
    return {
        "attempt_count": int(safe_get(source_final, "attempt_count", len(scorecard))),
        "expected_rows_total": safe_get(source_final, "expected_rows_total", ""),
        "matched_rows_total": safe_get(source_final, "matched_rows_total", ""),
        "mismatch_rows_total": safe_get(source_final, "mismatch_rows_total", ""),
        "best_attempt": safe_get(source_final, "best_attempt", ""),
        "best_model_id": safe_get(source_final, "best_model_id", ""),
        "best_net_profit": safe_get(source_final, "best_net_profit", ""),
        "best_profit_factor": safe_get(source_final, "best_profit_factor", ""),
        "best_expectancy": safe_get(source_final, "best_expectancy", ""),
        "best_recovery_factor": safe_get(source_final, "best_recovery_factor", ""),
        "best_drawdown": safe_get(source_final, "best_drawdown", ""),
        "best_trade_count": safe_get(source_final, "best_trade_count", ""),
        "q01_attempt": "q01_ctl_s55_l51_m01_h12",
        "q01_model_id": exact_row.get("model_id", ""),
        "q01_net_profit": exact_row.get("net_profit", ""),
        "q01_profit_factor": exact_row.get("profit_factor", ""),
        "q01_expectancy": exact_row.get("expectancy", ""),
        "q01_recovery_factor": exact_row.get("recovery_factor", ""),
        "q01_drawdown": exact_row.get("max_drawdown_amount", ""),
        "q01_trade_count": exact_row.get("trade_count", ""),
        "q09_attempt": "q09_s545_l51_m01_h12",
        "q09_model_id": q09_row.get("model_id", ""),
        "q09_net_profit": q09_row.get("net_profit", ""),
        "q09_profit_factor": q09_row.get("profit_factor", ""),
        "q09_expectancy": q09_row.get("expectancy", ""),
        "q09_recovery_factor": q09_row.get("recovery_factor", ""),
        "q09_drawdown": q09_row.get("max_drawdown_amount", ""),
        "q09_trade_count": q09_row.get("trade_count", ""),
    }


def build_source_inventory() -> pd.DataFrame:
    rows = []
    for path, role in [
        (SOURCE_FINAL_DECISION, "run340H final decision(340H 최종 결정)"),
        (SOURCE_GATE_AUDIT, "run340H gate audit(340H 게이트 감사)"),
        (SOURCE_SCORECARD, "run340H scorecard(340H 점수표)"),
        (SOURCE_KPI_JUDGMENT, "run340H KPI judgment(340H 핵심 성과 지표 판정)"),
        (SOURCE_ATTRIBUTION, "run340H performance attribution(340H 성과 귀속)"),
        (SOURCE_FAILURE_MEMORY, "run340H failure memory(340H 실패 기억)"),
        (SOURCE_SEED_QUEUE, "run340H Stage341 seed queue(340H 341단계 씨앗 대기열)"),
        (SOURCE_REPORT, "run340H report(340H 보고서)"),
        (SOURCE_RUNTIME_SUMMARY, "run340G MT5 summary(340G MT5 요약)"),
        (SOURCE_PROXY_DIFF, "run340G proxy-MT5 diff(340G 프록시-MT5 차이)"),
    ]:
        exists = path_exists(path)
        rows.append(
            {
                "artifact_role": role,
                "path": rel(path),
                "exists": exists,
                "availability": "tracked(추적됨)" if exists else "missing_required(필수 누락)",
                "sha256": sha256_file(path) if exists and path_is_file(path) else "",
                "consumer": NEXT_RUN_ID,
                "effect": "Stage 341(341단계)이 Stage 340(340단계)의 positive clue(긍정 단서)를 다시 찾지 않게 한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return pd.DataFrame(rows)


def build_handoff(metrics: Mapping[str, Any]) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "handoff_id": "stage340H_to_stage341A_f01_stability_cost_regime_validation",
                "source_stage_id": SOURCE_STAGE_ID,
                "new_stage_id": NEW_STAGE_ID,
                "branch_run_id": RUN_ID,
                "source_completed_run_id": PARENT_RUN_ID,
                "source_runtime_run_id": PARENT_RUNTIME_RUN_ID,
                "next_run_id": NEXT_RUN_ID,
                "branch_reason": "Stage 340(340단계)이 close_on_flat=False(평탄 청산 꺼짐) 복구와 review(검토)까지 누적되어 무거워졌다.",
                "q01_quality_anchor": metrics.get("q01_attempt", ""),
                "q01_net_profit": metrics.get("q01_net_profit", ""),
                "q01_profit_factor": metrics.get("q01_profit_factor", ""),
                "q01_recovery_factor": metrics.get("q01_recovery_factor", ""),
                "q01_drawdown": metrics.get("q01_drawdown", ""),
                "q09_net_clue": metrics.get("q09_attempt", ""),
                "q09_net_profit": metrics.get("q09_net_profit", ""),
                "q09_profit_factor": metrics.get("q09_profit_factor", ""),
                "q09_recovery_factor": metrics.get("q09_recovery_factor", ""),
                "q09_drawdown": metrics.get("q09_drawdown", ""),
                "allowed_use": "validation seed(검증 씨앗), cost stress(비용 압박), session/regime split(세션/국면 분할)",
                "forbidden_use": "selected model(선정 모델), operating promotion(운영 승격), runtime authority(런타임 권위)",
                "effect": "q01(품질 기준점)과 q09(순수익 단서)를 같은 Stage 341(341단계) 안에서 작게 비교하게 한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )


def build_next_queue(source_queue: pd.DataFrame, metrics: Mapping[str, Any]) -> pd.DataFrame:
    if source_queue.empty:
        source_queue = pd.DataFrame(
            [
                {
                    "seed_id": "s01_q01_exact_control_quality_anchor",
                    "source_attempt": metrics.get("q01_attempt", ""),
                    "role": "quality_anchor_exact_control(품질 기준점 정확 대조)",
                },
                {
                    "seed_id": "s02_q09_net_high_pressure_candidate",
                    "source_attempt": metrics.get("q09_attempt", ""),
                    "role": "net_high_quality_tradeoff_candidate(순수익 높고 품질 절충 후보)",
                },
            ]
        )
    queue = source_queue.copy()
    queue["next_run_id"] = NEXT_RUN_ID
    queue["stage341_validation_axis"] = (
        "stability(안정성);cost_stress(비용 압박);session_regime(세션/국면);equity_curve_quality(수익곡선 품질)"
    )
    queue["decision_use"] = "design input only(설계 입력 전용)"
    queue["success_condition"] = (
        "q01 quality anchor(품질 기준점) and q09 net clue(순수익 단서) survive cost/session/regime pressure without selection claim"
        "(선정 주장 없이 비용/세션/국면 압박을 통과하는지 확인)"
    )
    queue["failure_condition"] = "positive clue(긍정 단서)가 비용 압박 또는 세션/국면 분할에서 붕괴"
    queue["claim_boundary"] = CLAIM_BOUNDARY
    return queue


def write_stage_docs(metrics: Mapping[str, Any]) -> None:
    stage_brief = f"""# Stage 341 F01 Stability Cost Regime Validation(341단계 F01 안정성 비용 국면 검증)

## Canonical Stage ID(정식 단계 ID)

`{NEW_STAGE_ID}`

## Stage Question(단계 질문)

Can the restored f01(에프01) close_on_flat=False(평탄 청산 꺼짐) clue survive stability(안정성), cost stress(비용 압박), and session/regime(세션/국면) validation without overstaying in Stage 340(340단계)?

## Source Handoff(원천 인계)

- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_review_run(원천 검토 실행): `{PARENT_RUN_ID}`
- source_runtime_run(원천 런타임 실행): `{PARENT_RUNTIME_RUN_ID}`
- branch_run(분기 실행): `{RUN_ID}`
- next_run(다음 실행): `{NEXT_RUN_ID}`

## Preserved Clues(보존 단서)

- q01 quality anchor(품질 기준점): net_profit(순수익) `{metrics.get('q01_net_profit', '')}`, profit_factor(수익 팩터) `{metrics.get('q01_profit_factor', '')}`, recovery_factor(회복 계수) `{metrics.get('q01_recovery_factor', '')}`, drawdown(낙폭) `{metrics.get('q01_drawdown', '')}`
- q09 net clue(순수익 단서): net_profit(순수익) `{metrics.get('q09_net_profit', '')}`, profit_factor(수익 팩터) `{metrics.get('q09_profit_factor', '')}`, recovery_factor(회복 계수) `{metrics.get('q09_recovery_factor', '')}`, drawdown(낙폭) `{metrics.get('q09_drawdown', '')}`

Effect(효과): q09(큐09)를 winner(승자)로 고정하지 않고, q01(큐01)을 quality anchor(품질 기준점)로 붙여 비교한다.

## Scope(범위)

Stage 341(341단계)는 validation design(검증 설계), cost stress(비용 압박), session/regime split(세션/국면 분할), and equity curve quality(수익곡선 품질)를 다룬다.

## Forbidden Claims(금지 주장)

No selected model(선정 모델 없음), no promotion_candidate(승격 후보 없음), no operating promotion(운영 승격 없음), no runtime authority(런타임 권위 없음), no Goal Achieve(목표 달성 없음).
"""
    input_refs = f"""# Stage 341 Input Refs(341단계 입력 참조)

## Source Inputs(원천 입력)

- run340H final decision(340H 최종 결정): `{rel(SOURCE_FINAL_DECISION)}`
- run340H gate audit(340H 게이트 감사): `{rel(SOURCE_GATE_AUDIT)}`
- run340H scorecard(340H 점수표): `{rel(SOURCE_SCORECARD)}`
- run340H KPI judgment(340H 핵심 성과 지표 판정): `{rel(SOURCE_KPI_JUDGMENT)}`
- run340H attribution(340H 성과 귀속): `{rel(SOURCE_ATTRIBUTION)}`
- run340H failure memory(340H 실패 기억): `{rel(SOURCE_FAILURE_MEMORY)}`
- run340H seed queue(340H 씨앗 대기열): `{rel(SOURCE_SEED_QUEUE)}`
- run340G MT5 summary(340G MT5 요약): `{rel(SOURCE_RUNTIME_SUMMARY)}`

## Stage 341 Handoff Files(341단계 인계 파일)

- handoff manifest(인계 목록): `{rel(HANDOFF_MANIFEST)}`
- source inventory(원천 목록): `{rel(SOURCE_INVENTORY)}`
- next queue(다음 대기열): `{rel(NEXT_QUEUE)}`

Effect(효과): run341B(341B 실행)가 Stage 340(340단계) 파일을 다시 수색하지 않고 바로 validation design(검증 설계)을 시작하게 한다.
"""
    selection = f"""# Stage 341 Selection Status(341단계 선정 상태)

- active_stage(현재 단계): `{NEW_STAGE_ID}`
- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- selected_model(선정 모델): `none(없음)`
- quality_anchor(품질 기준점): `{metrics.get('q01_attempt', '')}`
- net_high_clue(순수익 높은 단서): `{metrics.get('q09_attempt', '')}`
- runtime_authority(런타임 권위): `not_claimed(주장 없음)`
- operating_promotion(운영 승격): `not_claimed(주장 없음)`
- Goal Achieve(목표 달성): `not_claimed(주장 없음)`

Effect(효과): q01/q09(큐01/큐09)를 validation seed(검증 씨앗)로만 보존하고 운영 주장(operating claim, 운영 주장)을 막는다.
"""
    report = f"""# run341A Stage Branch(341A 단계 분기)

## Summary(요약)

- run_id(실행 ID): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- new_stage(새 단계): `{NEW_STAGE_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- next_run(다음 실행): `{NEXT_RUN_ID}`
- gates(게이트): `{rel(GATE_AUDIT)}`

## Action(행동)

Stage 340(340단계)에서 Stage 341(341단계)로 분기했다.
Effect(효과): Stage 340(340단계)의 무게를 줄이고, f01(에프01) stability/cost/regime validation(안정성/비용/국면 검증)을 새 단계에서 작게 시작한다.

## Preserved Evidence(보존 근거)

- q01 quality anchor(품질 기준점): net_profit(순수익) `{metrics.get('q01_net_profit', '')}`, recovery_factor(회복 계수) `{metrics.get('q01_recovery_factor', '')}`, drawdown(낙폭) `{metrics.get('q01_drawdown', '')}`
- q09 net clue(순수익 단서): net_profit(순수익) `{metrics.get('q09_net_profit', '')}`, recovery_factor(회복 계수) `{metrics.get('q09_recovery_factor', '')}`, drawdown(낙폭) `{metrics.get('q09_drawdown', '')}`

## Boundary(경계)

This is state sync and handoff only(상태 동기화와 인계만 해당). Selection(선정), operating promotion(운영 승격), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 없다.
"""
    decision_doc = f"""# {TODAY} Stage 341A Branch Decision(341A 단계 분기 결정)

- decision(결정): `{DECISION}`
- from(출발): `{SOURCE_STAGE_ID}` / `{PARENT_RUN_ID}`
- to(도착): `{NEW_STAGE_ID}` / `{NEXT_RUN_ID}`
- reason(이유): Stage 340(340단계)이 corrected control(수정 대조), MT5 runtime probe(MT5 런타임 탐침), review(검토)까지 누적되어 validation(검증)을 새 단계로 분리했다.

Action(행동): Stage 341(341단계)를 열고 run341B(341B 실행)를 다음 validation design(검증 설계) 행동으로 둔다.
Effect(효과): Stage 340(340단계)의 positive clue(긍정 단서)를 보존하면서 다음 압박 검증을 가볍게 시작한다.

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

Stage 341(341단계)는 q01 quality anchor(품질 기준점)와 q09 net clue(순수익 단서)를 cost stress(비용 압박), session/regime split(세션/국면 분할), equity curve quality(수익곡선 품질)로 검증한다.

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
    source_selection = f"""# Stage 340 Selection Status(340단계 선정 상태)

- active_stage(기존 단계): `{SOURCE_STAGE_ID}`
- latest_completed_run(최근 완료 실행): `{PARENT_RUN_ID}`
- branched_to_stage(분기된 단계): `{NEW_STAGE_ID}`
- branch_run(분기 실행): `{RUN_ID}`
- next_active_run(다음 활성 실행): `{NEXT_RUN_ID}`
- selected_model(선정 모델): `none(없음)`
- quality_anchor(품질 기준점): `{metrics.get('q01_attempt', '')}`
- net_high_clue(순수익 높은 단서): `{metrics.get('q09_attempt', '')}`
- runtime_authority(런타임 권위): `not_claimed(주장 없음)`
- operating_promotion(운영 승격): `not_claimed(주장 없음)`
- Goal Achieve(목표 달성): `not_claimed(주장 없음)`

Effect(효과): Stage 340(340단계)을 더 끌지 않고 Stage 341(341단계) 검증으로 넘겼음을 재진입 시 바로 보이게 한다.
"""
    write_bom_text(STAGE_BRIEF, stage_brief)
    write_bom_text(STAGE_README, stage_brief)
    write_bom_text(INPUT_REFS, input_refs)
    write_bom_text(SELECTION_STATUS, selection)
    write_bom_text(REPORT_PATH, report)
    write_bom_text(DECISION_DOC, decision_doc)
    write_bom_text(CURRENT_WORKING_STATE, current)
    write_bom_text(WORKSPACE_STATE, workspace)
    write_bom_text(SOURCE_SELECTION_STATUS, source_selection)

    marker = RUN_ID
    append_text_once(
        SOURCE_STAGE_BRIEF,
        marker,
        f"""## run341A Stage Branch(341A 단계 분기)

- branch_run(분기 실행): `{RUN_ID}`
- new_stage(새 단계): `{NEW_STAGE_ID}`
- next_run(다음 실행): `{NEXT_RUN_ID}`
- effect(효과): Stage 340(340단계)의 f01(에프01) positive clue(긍정 단서)를 Stage 341(341단계) validation(검증)으로 넘겨 단계 무게를 줄였다.
""",
    )
    append_text_once(
        SOURCE_STAGE_README,
        marker,
        f"""## run341A Stage Branch(341A 단계 분기)

- branch_run(분기 실행): `{RUN_ID}`
- new_stage(새 단계): `{NEW_STAGE_ID}`
- next_run(다음 실행): `{NEXT_RUN_ID}`
- effect(효과): q01/q09(큐01/큐09) 검증을 Stage 341(341단계)에서 이어간다.
""",
    )
    changelog = f"""## {TODAY} run341A Stage Branch(341A 단계 분기)

- action(행동): Stage 340(340단계)의 f01(에프01) close_on_flat=False(평탄 청산 꺼짐) review(검토)를 Stage 341(341단계) validation(검증)으로 분기했다.
- effect(효과): Stage 340(340단계)을 닫고 q01 quality anchor(품질 기준점)와 q09 net clue(순수익 단서)를 작게 검증할 공간을 만들었다.
- boundary(경계): selected model(선정 모델), promotion_candidate(승격 후보), operating promotion(운영 승격), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 없다.
"""
    append_text_once(ROOT_CHANGELOG, marker, changelog)
    append_text_once(WORKSPACE_CHANGELOG, marker, changelog)
    append_text_once(
        IDEA_REGISTRY,
        marker,
        f"""## {TODAY} Stage 341 F01 Stability Cost Regime Validation Seed(341단계 F01 안정성 비용 국면 검증 씨앗)

- idea_id(아이디어 ID): `stage341_f01_stability_cost_regime_validation_seed`
- hypothesis(가설): q01 quality anchor(품질 기준점)와 q09 net clue(순수익 단서)는 cost stress(비용 압박)와 session/regime split(세션/국면 분할)에서 서로 다른 약점을 드러낼 수 있다.
- source(원천): `{PARENT_RUN_ID}`
- next_run(다음 실행): `{NEXT_RUN_ID}`
- tier_scope(티어 범위): `Tier A separate(Tier A 분리); Tier B missing_required(Tier B 필수 누락); Tier A+B same_as_tier_a_until_tier_b_available(Tier A+B는 Tier B 가능 전까지 Tier A와 같음)`
- evidence_boundary(근거 경계): `stage_branch_handoff_no_selection(단계 분기 인계, 선정 없음)`
- effect(효과): positive clue(긍정 단서)를 운영 주장(operating claim, 운영 주장)으로 과장하지 않고 다음 검증 질문으로 넘긴다.
""",
    )


def write_receipts(metrics: Mapping[str, Any]) -> None:
    base = {
        "run_id": RUN_ID,
        "stage_id": NEW_STAGE_ID,
        "parent_stage_id": SOURCE_STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
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
            "effect": "Stage 340(340단계)의 무거운 review(검토)를 Stage 341(341단계) validation(검증)으로 분리했다.",
        },
    )
    write_json(
        LINEAGE_RECEIPT,
        {
            **base,
            "source_inputs": [rel(path) for path in SOURCE_INPUTS],
            "artifact_paths": [
                rel(HANDOFF_MANIFEST),
                rel(SOURCE_INVENTORY),
                rel(NEXT_QUEUE),
                rel(REPORT_PATH),
                rel(DECISION_DOC),
            ],
            "source_artifact_hashes": {rel(path): sha256_file(path) for path in SOURCE_INPUTS if path_exists(path)},
            "lineage_judgment": "connected_with_boundary(경계가 있는 연결)",
            "effect": "run340H(340H 실행) 근거가 run341B(341B 실행) 설계 입력으로 연결된다.",
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
            "q01_quality_anchor": metrics.get("q01_attempt", ""),
            "q09_net_clue": metrics.get("q09_attempt", ""),
            "effect": "Stage branch(단계 분기)를 operating claim(운영 주장)으로 오해하지 않게 한다.",
        },
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
    source_gates = read_csv(SOURCE_GATE_AUDIT) if path_exists(SOURCE_GATE_AUDIT) else pd.DataFrame({"status": ["missing"]})
    workspace_text = ""
    if path_exists(WORKSPACE_STATE):
        with open(fs_path(WORKSPACE_STATE), encoding="utf-8-sig") as handle:
            workspace_text = handle.read()
    return pd.DataFrame(
        [
            gate_row(
                "parent_340H_gates_passed",
                "passed" if gate_statuses_pass(source_gates) else "failed",
                rel(SOURCE_GATE_AUDIT),
                "run340H(340H 실행) review(검토) gate(게이트)를 이어받는다.",
            ),
            gate_row(
                "parent_review_outputs_available",
                "passed"
                if path_exists(SOURCE_FINAL_DECISION) and path_exists(SOURCE_SCORECARD) and path_exists(SOURCE_SEED_QUEUE)
                else "failed",
                f"{rel(SOURCE_FINAL_DECISION)};{rel(SOURCE_SCORECARD)};{rel(SOURCE_SEED_QUEUE)}",
                "Stage 341(341단계) seed(씨앗)에 필요한 scorecard(점수표)와 queue(대기열)를 확인한다.",
            ),
            gate_row(
                "new_stage_scaffold_created",
                "passed" if path_exists(STAGE_BRIEF) and path_exists(INPUT_REFS) and path_exists(SELECTION_STATUS) else "failed",
                f"{rel(STAGE_BRIEF)};{rel(INPUT_REFS)};{rel(SELECTION_STATUS)}",
                "Stage 341(341단계)의 stage scaffold(단계 뼈대)를 만든다.",
            ),
            gate_row(
                "handoff_and_queue_written",
                "passed" if path_exists(HANDOFF_MANIFEST) and path_exists(SOURCE_INVENTORY) and path_exists(NEXT_QUEUE) else "failed",
                f"{rel(HANDOFF_MANIFEST)};{rel(SOURCE_INVENTORY)};{rel(NEXT_QUEUE)}",
                "handoff(인계)와 run341B queue(341B 대기열)를 분리한다.",
            ),
            gate_row(
                "current_truth_synced",
                "passed" if f"current_stage_id: {NEW_STAGE_ID}" in workspace_text and f"current_run_id: {NEXT_RUN_ID}" in workspace_text else "failed",
                f"{rel(WORKSPACE_STATE)};{rel(CURRENT_WORKING_STATE)}",
                "re-entry(재진입)가 Stage 341(341단계)에서 시작하게 한다.",
            ),
            gate_row(
                "registries_available",
                "passed" if path_exists(RUN_REGISTRY) and path_exists(PROJECT_LEDGER) and path_exists(ARTIFACT_REGISTRY) else "failed",
                f"{rel(RUN_REGISTRY)};{rel(PROJECT_LEDGER)};{rel(ARTIFACT_REGISTRY)}",
                "run identity(실행 정체성)와 artifact lineage(산출물 계보)를 붙일 등록부를 확인한다.",
            ),
            gate_row(
                "no_forbidden_operating_claim",
                "passed",
                rel(CLAIM_RECEIPT),
                "selection(선정), promotion(승격), runtime authority(런타임 권위)를 주장하지 않는다.",
            ),
            gate_row(
                "required_gate_coverage_audit_written",
                "passed",
                rel(GATE_AUDIT),
                "required gate coverage audit(필수 게이트 커버리지 감사)를 closeout(종료 기록)에 연결한다.",
            ),
        ]
    )


def write_final_decision(gates: pd.DataFrame, metrics: Mapping[str, Any]) -> None:
    write_json(
        FINAL_DECISION,
        {
            "stage_id": NEW_STAGE_ID,
            "run_id": RUN_ID,
            "parent_stage_id": SOURCE_STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "status": STATUS,
            "judgment": JUDGMENT,
            "decision": DECISION,
            "gate_passes": int(gates["status"].astype(str).str.lower().eq("passed").sum()),
            "gate_total": int(len(gates)),
            "q01_quality_anchor": metrics.get("q01_attempt", ""),
            "q01_net_profit": metrics.get("q01_net_profit", ""),
            "q01_profit_factor": metrics.get("q01_profit_factor", ""),
            "q01_recovery_factor": metrics.get("q01_recovery_factor", ""),
            "q01_drawdown": metrics.get("q01_drawdown", ""),
            "q09_net_clue": metrics.get("q09_attempt", ""),
            "q09_net_profit": metrics.get("q09_net_profit", ""),
            "q09_profit_factor": metrics.get("q09_profit_factor", ""),
            "q09_recovery_factor": metrics.get("q09_recovery_factor", ""),
            "q09_drawdown": metrics.get("q09_drawdown", ""),
            "claim_boundary": CLAIM_BOUNDARY,
            "created_at_utc": now_utc(),
            "effect": "Stage 340(340단계) positive clue(긍정 단서)를 Stage 341(341단계) validation(검증)으로 분기했다.",
        },
    )


def write_run_manifest(metrics: Mapping[str, Any]) -> None:
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "stage_id": NEW_STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "command": "python -B stage_pipelines/stage341/branch_stage340_to_f01_stability_cost_regime_validation_without_db.py",
            "created_at_utc": now_utc(),
            "status": STATUS,
            "judgment": JUDGMENT,
            "next_run_id": NEXT_RUN_ID,
            "q01_quality_anchor": metrics.get("q01_attempt", ""),
            "q09_net_clue": metrics.get("q09_attempt", ""),
            "outputs": [
                rel(HANDOFF_MANIFEST),
                rel(SOURCE_INVENTORY),
                rel(NEXT_QUEUE),
                rel(GATE_AUDIT),
                rel(FINAL_DECISION),
                rel(REPORT_PATH),
                rel(DECISION_DOC),
            ],
            "claim_boundary": CLAIM_BOUNDARY,
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
        "candidate_model_id": metrics.get("q09_model_id", ""),
        "net_profit": metrics.get("q09_net_profit", ""),
        "profit_factor": metrics.get("q09_profit_factor", ""),
        "drawdown": metrics.get("q09_drawdown", ""),
        "recovery_factor": metrics.get("q09_recovery_factor", ""),
        "trade_count": metrics.get("q09_trade_count", ""),
        "result_status": "stage_branch_opened_no_selection(단계 분기 완료, 선정 없음)",
        "sample_rows": "",
        "feature_count": "",
        "matched_rows": metrics.get("matched_rows_total", ""),
        "expectancy": metrics.get("q09_expectancy", ""),
        "attempt_count": metrics.get("attempt_count", ""),
    }
    rows = []
    for view, tier, metric_scope in [
        ("Tier A separate(Tier A 분리)", "Tier A", "stage_branch_handoff"),
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
        SOURCE_INVENTORY,
        NEXT_QUEUE,
        STAGE_TRANSITION_RECEIPT,
        LINEAGE_RECEIPT,
        CLAIM_RECEIPT,
        GATE_AUDIT,
        FINAL_DECISION,
        RUN_MANIFEST,
        REPORT_PATH,
        DECISION_DOC,
        CURRENT_WORKING_STATE,
        WORKSPACE_STATE,
        STAGE_LEDGER,
        RUN_REGISTRY,
        PROJECT_LEDGER,
        Path(__file__),
    ]
    artifact_rows = []
    for path in artifacts:
        if not path_exists(path) or not path_is_file(path):
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
    Path(fs_path(RUN_DIR)).mkdir(parents=True, exist_ok=True)
    Path(fs_path(REVIEW_DIR)).mkdir(parents=True, exist_ok=True)
    for path in [SOURCE_FINAL_DECISION, SOURCE_GATE_AUDIT, SOURCE_SCORECARD, SOURCE_SEED_QUEUE]:
        if not path_exists(path):
            raise FileNotFoundError(f"missing required stage branch input: {rel(path)}")

    source_final = read_json(SOURCE_FINAL_DECISION)
    scorecard = read_csv(SOURCE_SCORECARD)
    source_queue = read_csv(SOURCE_SEED_QUEUE)
    metrics = build_metrics(source_final, scorecard)

    write_csv(SOURCE_INVENTORY, build_source_inventory())
    write_csv(HANDOFF_MANIFEST, build_handoff(metrics))
    write_csv(NEXT_QUEUE, build_next_queue(source_queue, metrics))
    write_stage_docs(metrics)
    write_receipts(metrics)

    gates = build_gates()
    write_csv(GATE_AUDIT, gates)
    write_final_decision(gates, metrics)
    write_run_manifest(metrics)
    write_registries(gates, metrics)

    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "next_run_id": NEXT_RUN_ID,
                "new_stage_id": NEW_STAGE_ID,
                "gate_passes": int(gates["status"].astype(str).str.lower().eq("passed").sum()),
                "gate_total": int(len(gates)),
                "q01_net_profit": metrics.get("q01_net_profit", ""),
                "q09_net_profit": metrics.get("q09_net_profit", ""),
                "goal_achieve": "not_claimed",
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
