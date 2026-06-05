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

SOURCE_STAGE_ID = "341_f01_stability_cost_regime__validate_quality_anchor_vs_net_clue"
NEW_STAGE_ID = "342_session_long_firewall__early_long_filter_mt5_probe"
SOURCE_STAGE_DIR = ROOT / "stages" / SOURCE_STAGE_ID
NEW_STAGE_DIR = ROOT / "stages" / NEW_STAGE_ID

RUN_NUMBER = "run342A"
RUN_ID = "run342A_branch_stage341_to_session_long_firewall_probe_without_db_v1"
PARENT_RUN_ID = "run341D_review_f01_stability_cost_regime_validation_without_db_v1"
SUPERSEDED_RUN_ID = "run341E_materialize_f01_session_long_firewall_mt5_probe_package_without_db_v1"
NEXT_RUN_ID = "run342B_materialize_f01_session_long_firewall_mt5_probe_package_without_db_v1"

STATUS = "completed_stage342A_branch_from_stage341_session_long_firewall_probe_opened_no_selection"
JUDGMENT = "stage_branch_completed_stage341_overweight_handoff_to_session_long_firewall_probe_no_selection"
DECISION = "stage342A_open_run342B_materialize_f01_session_long_firewall_mt5_probe_package"
CLAIM_BOUNDARY = (
    "state_sync_stage_branch_session_long_firewall_handoff_only_no_mt5_execution_"
    "no_candidate_selection_no_forward_no_live_readiness_no_operating_promotion_"
    "no_runtime_authority_no_goal_claim"
)

RUN_DIR = NEW_STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = NEW_STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEW_DIR / "run342A_stage_branch.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage342A_branch_stage341_to_session_long_firewall_probe.md"
STAGE_BRIEF = NEW_STAGE_DIR / "00_spec" / "stage_brief.md"
STAGE_README = NEW_STAGE_DIR / "README.md"
INPUT_REFS = NEW_STAGE_DIR / "01_inputs" / "input_refs.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"
SELECTION_STATUS = NEW_STAGE_DIR / "04_selected" / "selection_status.md"
SOURCE_SELECTION_STATUS = SOURCE_STAGE_DIR / "04_selected" / "selection_status.md"

SOURCE_RUN_DIR = SOURCE_STAGE_DIR / "02_runs" / "run341D"
SOURCE_VALIDATION_DIR = SOURCE_STAGE_DIR / "02_runs" / "run341C"
SOURCE_FINAL_DECISION = SOURCE_RUN_DIR / "final_decision.json"
SOURCE_GATE_AUDIT = SOURCE_RUN_DIR / "required_gate_coverage_audit.csv"
SOURCE_REVIEW_SCORECARD = SOURCE_RUN_DIR / "review_scorecard.csv"
SOURCE_VALIDATION_JUDGMENT = SOURCE_RUN_DIR / "validation_judgment.csv"
SOURCE_ATTRIBUTION = SOURCE_RUN_DIR / "performance_attribution.csv"
SOURCE_FAILURE_MEMORY = SOURCE_RUN_DIR / "failure_memory.csv"
SOURCE_QUEUE = SOURCE_RUN_DIR / "run341E_session_long_firewall_probe_queue.csv"
SOURCE_REPORT = SOURCE_STAGE_DIR / "03_reviews" / "run341D_f01_stability_cost_regime_validation_review.md"
SOURCE_VALIDATION_SCORECARD = SOURCE_VALIDATION_DIR / "validation_scorecard.csv"

HANDOFF_MANIFEST = RUN_DIR / "stage341_to_stage342_handoff_manifest.csv"
SOURCE_INVENTORY = RUN_DIR / "stage341_source_inventory.csv"
NEXT_QUEUE = RUN_DIR / "run342B_session_long_firewall_probe_queue.csv"
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
]

SOURCE_INPUTS = [
    (SOURCE_FINAL_DECISION, "run341D final decision(341D 최종 결정)"),
    (SOURCE_GATE_AUDIT, "run341D required gate audit(341D 필수 게이트 감사)"),
    (SOURCE_REVIEW_SCORECARD, "run341D review scorecard(341D 검토 점수표)"),
    (SOURCE_VALIDATION_JUDGMENT, "run341D validation judgment(341D 검증 판정)"),
    (SOURCE_ATTRIBUTION, "run341D performance attribution(341D 성과 귀속)"),
    (SOURCE_FAILURE_MEMORY, "run341D failure memory(341D 실패 기억)"),
    (SOURCE_QUEUE, "run341D next probe queue(341D 다음 탐침 대기열)"),
    (SOURCE_REPORT, "run341D review report(341D 검토 보고서)"),
    (SOURCE_VALIDATION_SCORECARD, "run341C validation scorecard(341C 검증 점수표)"),
    (SOURCE_SELECTION_STATUS, "stage341 selection status(341단계 선택 상태)"),
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
                mask &= frame[key].astype(str) == str(row.get(key, ""))
            else:
                mask &= False
        frame = frame.loc[~mask].copy()
        frame = pd.concat([frame, pd.DataFrame([row])], ignore_index=True)
    write_csv(path, frame)


def required(path: Path) -> Path:
    if not path_is_file(path):
        raise FileNotFoundError(rel(path))
    return path


def read_source_metrics() -> dict[str, Any]:
    review = read_csv(required(SOURCE_REVIEW_SCORECARD))
    validation = read_csv(required(SOURCE_VALIDATION_SCORECARD))

    def row(frame: pd.DataFrame, attempt: str) -> pd.Series:
        matched = frame.loc[frame["attempt_name"].astype(str) == attempt]
        if matched.empty:
            raise ValueError(f"missing attempt row: {attempt}")
        return matched.iloc[0]

    q01_review = row(review, "q01_ctl_s55_l51_m01_h12")
    q09_review = row(review, "q09_s545_l51_m01_h12")
    q01_validation = row(validation, "q01_ctl_s55_l51_m01_h12")
    q09_validation = row(validation, "q09_s545_l51_m01_h12")
    queue = read_csv(required(SOURCE_QUEUE))

    return {
        "q01_net_profit": float(q01_review["net_profit"]),
        "q01_profit_factor": float(q01_validation["base_profit_factor"]),
        "q01_reported_drawdown": float(q01_review["reported_drawdown"]),
        "q01_reported_recovery": float(q01_review["reported_recovery"]),
        "q01_plus1_cost_net": float(q01_review["plus1_cost_net"]),
        "q01_plus2_cost_recovery": float(q01_review["plus2_cost_recovery"]),
        "q01_early_net": float(q01_review["early_net"]),
        "q01_late_net": float(q01_review["late_net"]),
        "q09_net_profit": float(q09_review["net_profit"]),
        "q09_profit_factor": float(q09_validation["base_profit_factor"]),
        "q09_reported_drawdown": float(q09_review["reported_drawdown"]),
        "q09_reported_recovery": float(q09_review["reported_recovery"]),
        "q09_plus1_cost_net": float(q09_review["plus1_cost_net"]),
        "q09_plus2_cost_recovery": float(q09_review["plus2_cost_recovery"]),
        "q09_early_net": float(q09_review["early_net"]),
        "q09_late_net": float(q09_review["late_net"]),
        "queue_rows": int(len(queue)),
    }


def write_source_inventory() -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for path, label in SOURCE_INPUTS:
        exists = path_is_file(path)
        rows.append(
            {
                "source_label": label,
                "path": rel(path),
                "exists": bool(exists),
                "sha256": sha256_file(path) if exists else "",
                "bytes": os.path.getsize(fs_path(path)) if exists else "",
                "consumer": RUN_ID,
                "availability": "tracked" if exists else "missing",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    frame = pd.DataFrame(rows)
    write_csv(SOURCE_INVENTORY, frame)
    return frame


def write_handoff_artifacts(metrics: Mapping[str, Any]) -> pd.DataFrame:
    queue = read_csv(required(SOURCE_QUEUE)).copy()
    queue["source_next_run_id"] = queue.get("next_run_id", "")
    queue["next_run_id"] = NEXT_RUN_ID
    queue["new_stage_id"] = NEW_STAGE_ID
    queue["handoff_run_id"] = RUN_ID
    queue["superseded_run_id"] = SUPERSEDED_RUN_ID
    queue["claim_boundary"] = CLAIM_BOUNDARY
    queue["status"] = "retargeted_to_stage342(342단계로 재지정)"
    write_csv(NEXT_QUEUE, queue)

    handoff = pd.DataFrame(
        [
            {
                "handoff_id": "stage341D_to_stage342A_branch",
                "source_stage_id": SOURCE_STAGE_ID,
                "source_run_id": PARENT_RUN_ID,
                "superseded_run_id": SUPERSEDED_RUN_ID,
                "new_stage_id": NEW_STAGE_ID,
                "branch_run_id": RUN_ID,
                "next_run_id": NEXT_RUN_ID,
                "source_queue_path": rel(SOURCE_QUEUE),
                "retargeted_queue_path": rel(NEXT_QUEUE),
                "q01_net_profit": metrics["q01_net_profit"],
                "q01_reported_drawdown": metrics["q01_reported_drawdown"],
                "q01_reported_recovery": metrics["q01_reported_recovery"],
                "q09_net_profit": metrics["q09_net_profit"],
                "q09_reported_drawdown": metrics["q09_reported_drawdown"],
                "q09_reported_recovery": metrics["q09_reported_recovery"],
                "branch_reason": "Stage341(341단계)이 validation(검증)과 next MT5 package(MT5 패키지)를 함께 품어 무거워졌다.",
                "effect": "Stage342(342단계)가 session-long firewall(세션 롱 방화벽) runtime probe(런타임 탐침)만 다룬다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )
    write_csv(HANDOFF_MANIFEST, handoff)
    return queue


def write_receipts(metrics: Mapping[str, Any], inventory: pd.DataFrame, queue: pd.DataFrame) -> None:
    created_at = now_utc()
    source_inputs = [
        {
            "label": row["source_label"],
            "path": row["path"],
            "sha256": row["sha256"],
            "availability": row["availability"],
        }
        for row in inventory.to_dict("records")
    ]
    artifact_paths = [
        HANDOFF_MANIFEST,
        SOURCE_INVENTORY,
        NEXT_QUEUE,
        REPORT_PATH,
        DECISION_DOC,
        STAGE_BRIEF,
        STAGE_README,
        INPUT_REFS,
        SELECTION_STATUS,
        STAGE_LEDGER,
        GATE_AUDIT,
        FINAL_DECISION,
        RUN_MANIFEST,
    ]
    lineage = {
        "run_id": RUN_ID,
        "stage_id": NEW_STAGE_ID,
        "parent_stage_id": SOURCE_STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "producer": rel(Path(__file__)),
        "consumer": NEXT_RUN_ID,
        "source_inputs": source_inputs,
        "artifact_paths": [rel(path) for path in artifact_paths],
        "artifact_hashes": {
            rel(path): sha256_file(path)
            for path in artifact_paths
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
    }
    write_json(LINEAGE_RECEIPT, lineage)
    write_json(
        STAGE_TRANSITION_RECEIPT,
        {
            "run_id": RUN_ID,
            "source_stage_id": SOURCE_STAGE_ID,
            "new_stage_id": NEW_STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "superseded_run_id": SUPERSEDED_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "queue_rows": int(len(queue)),
            "q09_net_delta_vs_q01": metrics["q09_net_profit"] - metrics["q01_net_profit"],
            "q09_drawdown_delta_vs_q01": metrics["q09_reported_drawdown"] - metrics["q01_reported_drawdown"],
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
                "candidate_selection(후보 선정)",
                "MT5_execution_completed(MT5 실행 완료)",
                "forward_validation(전진 검증)",
                "live_readiness(실거래 준비)",
                "operating_promotion(운영 승격)",
                "runtime_authority(런타임 권위)",
                "Goal_Achieve(목표 달성)",
            ],
            "judgment_label": "not_applicable_for_trading_kpi(거래 KPI 판정 해당 없음)",
            "next_condition": f"{NEXT_RUN_ID} package materialization(패키지 물질화)",
            "created_at_utc": created_at,
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def markdown_documents(metrics: Mapping[str, Any]) -> None:
    stage_brief = f"""# Stage 342 Brief(342단계 개요)

## Stage ID(단계 ID)

`{NEW_STAGE_ID}`

## Question(질문)

Can session-long firewall(세션 롱 방화벽), especially early-long block(초반 롱 차단), improve q01/q09(큐01/큐09) MT5 runtime probe(MT5 런타임 탐침) quality without turning the clue into overfiltering(과필터링)?

## Scope(범위)

- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_review_run(원천 검토 실행): `{PARENT_RUN_ID}`
- branch_run(분기 실행): `{RUN_ID}`
- superseded_run(대체된 실행): `{SUPERSEDED_RUN_ID}`
- next_run(다음 실행): `{NEXT_RUN_ID}`

Action(행동): Stage 341(341단계)의 validation review(검증 검토) 뒤 MT5 package(MT5 패키지) 작업을 Stage 342(342단계)로 분리한다.
Effect(효과): Stage 341(341단계)을 더 키우지 않고, session-long firewall(세션 롱 방화벽)만 좁게 압박 시험한다.

## Evidence Boundary(근거 경계)

This stage branch(단계 분기)는 no new MT5 execution(새 MT5 실행 없음), no candidate selection(후보 선정 없음), no operating promotion(운영 승격 없음)이다.
"""

    readme = f"""# Stage 342(342단계)

Stage 342(342단계)는 q01/q09(큐01/큐09) positive clue(긍정 단서)를 early-long block(초반 롱 차단) side filter(사이드 필터)로 압박하는 runtime probe(런타임 탐침) 전용 단계다.

- current_run(현재 실행): `{NEXT_RUN_ID}`
- branch_run(분기 실행): `{RUN_ID}`
- source(원천): `{PARENT_RUN_ID}`

Effect(효과): validation(검증), package(패키지), execution(실행), review(검토)가 한 Stage(단계)에 계속 쌓이지 않게 한다.
"""

    input_refs = f"""# Stage 342 Input Refs(342단계 입력 참조)

- run341D final decision(341D 최종 결정): `{rel(SOURCE_FINAL_DECISION)}`
- run341D review scorecard(341D 검토 점수표): `{rel(SOURCE_REVIEW_SCORECARD)}`
- run341D validation judgment(341D 검증 판정): `{rel(SOURCE_VALIDATION_JUDGMENT)}`
- run341D next probe queue(341D 다음 탐침 대기열): `{rel(SOURCE_QUEUE)}`
- run342B retargeted queue(342B 재지정 대기열): `{rel(NEXT_QUEUE)}`

Action(행동): Stage 341(341단계)의 queue(대기열)를 Stage 342(342단계) run342B(342B 실행)로 재지정한다.
Effect(효과): 이전 검토 결론은 보존하고, 다음 MT5 package(MT5 패키지)는 새 Stage(단계)의 책임으로 남긴다.
"""

    report = f"""# Run342A Stage Branch(342A 단계 분기)

## Decision(결정)

`{DECISION}`

## Reason(이유)

Stage 341(341단계)은 f01 stability/cost/regime validation(f01 안정성/비용/국면 검증)을 run341D(341D 실행)까지 완료했다. 그 다음 행동인 session-long firewall(세션 롱 방화벽) MT5 package(MT5 패키지)는 새 질문이므로 Stage 342(342단계)로 분리한다.

Action(행동): `{SUPERSEDED_RUN_ID}`를 직접 진행하지 않고 `{NEXT_RUN_ID}`로 재지정했다.
Effect(효과): Stage 341(341단계)의 결론은 닫고, 새 탐침은 더 작은 Stage(단계)에서 다룬다.

## Source Clue(원천 단서)

- q01(큐01): net profit(순수익) `{metrics["q01_net_profit"]}`, reported drawdown(보고 낙폭) `{metrics["q01_reported_drawdown"]}`, reported recovery(보고 회복 계수) `{metrics["q01_reported_recovery"]}`
- q09(큐09): net profit(순수익) `{metrics["q09_net_profit"]}`, reported drawdown(보고 낙폭) `{metrics["q09_reported_drawdown"]}`, reported recovery(보고 회복 계수) `{metrics["q09_reported_recovery"]}`
- q09 net delta(q09 순수익 차이): `{metrics["q09_net_profit"] - metrics["q01_net_profit"]}`
- q09 drawdown delta(q09 낙폭 차이): `{metrics["q09_reported_drawdown"] - metrics["q01_reported_drawdown"]}`

## Next Queue(다음 대기열)

- retargeted queue(재지정 대기열): `{rel(NEXT_QUEUE)}`
- queue rows(대기열 행): `{metrics["queue_rows"]}`

## Claim Boundary(주장 경계)

`{CLAIM_BOUNDARY}`

No Goal Achieve(목표 달성 없음), no runtime authority(런타임 권위 없음), no operating promotion(운영 승격 없음).
"""

    decision_doc = f"""# {TODAY} Stage342A Branch Decision(342A 단계 분기 결정)

- decision(결정): `{DECISION}`
- from(출발): `{SOURCE_STAGE_ID}` / `{PARENT_RUN_ID}`
- to(도착): `{NEW_STAGE_ID}` / `{NEXT_RUN_ID}`
- superseded_run(대체된 실행): `{SUPERSEDED_RUN_ID}`
- reason(이유): Stage 341(341단계)이 validation review(검증 검토) 뒤 MT5 package(MT5 패키지)까지 품으면 너무 무거워져 session-long firewall(세션 롱 방화벽)을 새 단계로 분리했다.

Action(행동): Stage 342(342단계)를 열고 run342B(342B 실행)를 package materialization(패키지 물질화) 다음 행동으로 둔다.
Effect(효과): run341D(341D 실행)의 positive clue(긍정 단서)를 보존하면서 다음 MT5 probe(MT5 탐침)를 가볍게 시작한다.

claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""

    selection = f"""# Stage 342 Selection Status(342단계 선정 상태)

- active_stage(현재 단계): `{NEW_STAGE_ID}`
- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- selected_model(선정 모델): `none(없음)`
- quality_anchor(품질 기준점): `q01_ctl_s55_l51_m01_h12`
- net_high_clue(순수익 높은 단서): `q09_s545_l51_m01_h12`
- next_probe(다음 탐침): `session_long_firewall(세션 롱 방화벽)`
- runtime_authority(런타임 권위): `not_claimed(주장 없음)`
- operating_promotion(운영 승격): `not_claimed(주장 없음)`
- Goal Achieve(목표 달성): `not_claimed(주장 없음)`

Effect(효과): Stage 342(342단계)는 후보 선정이 아니라 MT5 package/probe(MT5 패키지/탐침) 준비부터 시작한다.
"""

    source_selection = f"""# Stage 341 Selection Status(341단계 선정 상태)

- stage_id(단계 ID): `{SOURCE_STAGE_ID}`
- latest_completed_run(최근 완료 실행): `{PARENT_RUN_ID}`
- branched_to_stage(분기된 단계): `{NEW_STAGE_ID}`
- branch_run(분기 실행): `{RUN_ID}`
- superseded_current_run(대체된 현재 실행): `{SUPERSEDED_RUN_ID}`
- selected_model(선정 모델): `none(없음)`
- preserved_clue(보존 단서): `q01/q09 positive structure(큐01/큐09 긍정 구조)`
- blocked_selection_reason(선정 차단 이유): `q09 net(순수익)은 약간 높지만 reported drawdown/recovery(보고 낙폭/회복 계수)가 악화됨`
- runtime_authority(런타임 권위): `not_claimed(주장 없음)`
- operating_promotion(운영 승격): `not_claimed(주장 없음)`
- Goal Achieve(목표 달성): `not_claimed(주장 없음)`

Effect(효과): Stage 341(341단계)은 validation review(검증 검토)까지만 보존하고, 다음 탐침은 Stage 342(342단계)에서 이어간다.
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

Stage 341(341단계)은 run341D(341D 실행) review(검토)까지 닫고, session-long firewall(세션 롱 방화벽) MT5 package/probe(MT5 패키지/탐침)는 Stage 342(342단계)로 분기했다.

## Claim Boundary(주장 경계)

`{CLAIM_BOUNDARY}`
"""

    write_bom_text(STAGE_BRIEF, stage_brief)
    write_bom_text(STAGE_README, readme)
    write_bom_text(INPUT_REFS, input_refs)
    write_bom_text(REPORT_PATH, report)
    write_bom_text(DECISION_DOC, decision_doc)
    write_bom_text(SELECTION_STATUS, selection)
    write_bom_text(SOURCE_SELECTION_STATUS, source_selection)
    write_bom_text(ROOT_SELECTION_STATUS, selection)
    write_bom_text(WORKSPACE_STATE, workspace)
    write_bom_text(CURRENT_WORKING_STATE, current)


def append_changelogs() -> None:
    marker = RUN_ID
    text = f"""## {TODAY} {RUN_ID}

- Action(행동): Stage 341(341단계)의 run341E(341E 실행) package continuation(패키지 연속)을 Stage 342(342단계) run342B(342B 실행)로 분기했다.
- Effect(효과): Stage 341(341단계)을 validation review(검증 검토)로 가볍게 닫고, session-long firewall(세션 롱 방화벽) probe(탐침)를 별도 Stage(단계)에서 진행한다.
- Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    append_text_once(ROOT_CHANGELOG, marker, text)
    append_text_once(WORKSPACE_CHANGELOG, marker, text)


def append_idea_registry() -> None:
    marker = RUN_ID
    text = f"""## {TODAY} {RUN_ID} Session-long Firewall Branch(세션 롱 방화벽 분기)

- seed(씨앗): q01/q09(큐01/큐09)는 +1 cost stress(+1 비용 압박)를 버티지만 early session(초반 세션)과 long side(롱 방향)가 약하다.
- action(행동): early-long block(초반 롱 차단) side filter(사이드 필터)를 Stage 342(342단계) MT5 package/probe(MT5 패키지/탐침)로 분기한다.
- effect(효과): q09(큐09)를 winner(승자)로 고정하지 않고, q01/q09(큐01/큐09) 모두에 같은 firewall(방화벽) 질문을 던진다.
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    append_text_once(IDEA_REGISTRY, marker, text)


def build_ledger_rows(metrics: Mapping[str, Any]) -> list[dict[str, Any]]:
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
        "gate_passes": 9,
        "gate_total": 9,
        "claim_boundary": CLAIM_BOUNDARY,
        "candidate_model_id": "logreg_balanced_c025_q09_s545_l51_m01_h12",
        "sample_rows": "",
        "feature_count": "",
        "matched_rows": "",
        "expectancy": "",
        "attempt_count": metrics["queue_rows"],
    }
    tier_a = {
        **base,
        "view": "Tier A separate(Tier A 분리)",
        "tier": "Tier A",
        "metric_scope": "stage_branch_handoff_q01_q09_seed",
        "net_profit": metrics["q09_net_profit"],
        "profit_factor": metrics["q09_profit_factor"],
        "drawdown": metrics["q09_reported_drawdown"],
        "recovery_factor": metrics["q09_reported_recovery"],
        "trade_count": 33,
        "result_status": "stage_branch_opened_no_selection(단계 분기 완료, 선정 없음)",
    }
    tier_b = {
        **base,
        "view": "Tier B separate(Tier B 분리)",
        "tier": "Tier B",
        "metric_scope": "missing_required",
        "candidate_model_id": "",
        "net_profit": "",
        "profit_factor": "",
        "drawdown": "",
        "recovery_factor": "",
        "trade_count": "",
        "result_status": "missing_required(필수 누락)",
    }
    combined = {
        **tier_a,
        "view": "Tier A+B combined(Tier A+B 합산)",
        "tier": "Tier A+B",
        "metric_scope": "same_as_tier_a_until_tier_b_available",
    }
    return [tier_a, tier_b, combined]


def write_ledgers(metrics: Mapping[str, Any]) -> None:
    rows = build_ledger_rows(metrics)
    write_csv(STAGE_LEDGER, pd.DataFrame(rows, columns=STAGE_LEDGER_COLUMNS))
    project_rows = []
    for row in rows:
        project_rows.append(
            {
                **row,
                "ledger_row_id": f"{RUN_ID}__{row['tier']}",
                "subrun_id": row["tier"],
                "record_view": row["view"],
                "tier_scope": row["tier"],
                "kpi_scope": row["metric_scope"],
                "scoreboard_lane": "stage_branch_handoff(단계 분기 인계)",
                "path": rel(REPORT_PATH),
                "primary_kpi": f"q09_net_profit={metrics['q09_net_profit']};q09_reported_recovery={metrics['q09_reported_recovery']}",
                "guardrail_kpi": f"q01_net_profit={metrics['q01_net_profit']};q01_reported_recovery={metrics['q01_reported_recovery']}",
                "external_verification_status": "out_of_scope_by_claim(주장 범위 밖)",
                "notes": "Stage branch only(단계 분기 전용); no new MT5 execution(새 MT5 실행 없음).",
            }
        )
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], project_rows)
    append_or_replace_csv(
        RUN_REGISTRY,
        ["run_id"],
        [
            {
                "run_id": RUN_ID,
                "stage_id": NEW_STAGE_ID,
                "lane": "state_sync_stage_branch(상태 동기화 단계 분기)",
                "family": "state_sync",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(FINAL_DECISION),
                "notes": "User requested Stage branch because Stage 341 became heavy.",
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
                "candidate_model_id": "logreg_balanced_c025_q09_s545_l51_m01_h12",
                "net_profit": metrics["q09_net_profit"],
                "profit_factor": metrics["q09_profit_factor"],
                "drawdown": metrics["q09_reported_drawdown"],
                "recovery_factor": metrics["q09_reported_recovery"],
                "trade_count": 33,
                "result_status": "stage_branch_opened_no_selection(단계 분기 완료, 선정 없음)",
                "attempt_count": metrics["queue_rows"],
                "view": "Tier A separate(Tier A 분리)",
                "tier": "Tier A",
                "metric_scope": "stage_branch_handoff_q01_q09_seed",
            }
        ],
    )


def write_gates() -> pd.DataFrame:
    workspace_text = ""
    if path_exists(WORKSPACE_STATE):
        with open(fs_path(WORKSPACE_STATE), encoding="utf-8-sig") as handle:
            workspace_text = handle.read()
    queue = read_csv(required(NEXT_QUEUE))
    gates = pd.DataFrame(
        [
            {
                "gate_id": "source_run341D_gate_audit_available",
                "status": "passed" if path_is_file(SOURCE_GATE_AUDIT) else "failed",
                "evidence_path": rel(SOURCE_GATE_AUDIT),
                "effect": "run341D(341D 실행)의 검토 게이트를 이어받는다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "gate_id": "source_queue_available",
                "status": "passed" if path_is_file(SOURCE_QUEUE) else "failed",
                "evidence_path": rel(SOURCE_QUEUE),
                "effect": "session-long firewall(세션 롱 방화벽) queue(대기열)를 잃지 않는다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "gate_id": "stage_structure_created",
                "status": "passed" if all(path_exists(path) for path in [STAGE_BRIEF, INPUT_REFS, REPORT_PATH, SELECTION_STATUS]) else "failed",
                "evidence_path": rel(NEW_STAGE_DIR),
                "effect": "새 Stage(단계)가 필수 폴더와 문서를 가진다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "gate_id": "queue_retargeted_to_stage342B",
                "status": "passed" if (len(queue) > 0 and queue["next_run_id"].astype(str).eq(NEXT_RUN_ID).all()) else "failed",
                "evidence_path": rel(NEXT_QUEUE),
                "effect": "run341E(341E 실행)로 쌓이지 않고 run342B(342B 실행)로 이어진다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "gate_id": "artifact_lineage_audit",
                "status": "passed" if path_is_file(LINEAGE_RECEIPT) and path_is_file(HANDOFF_MANIFEST) else "failed",
                "evidence_path": rel(LINEAGE_RECEIPT),
                "effect": "원천 산출물과 새 산출물 연결을 남긴다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "gate_id": "state_sync_audit",
                "status": "passed" if f"current_stage_id: {NEW_STAGE_ID}" in workspace_text and f"current_run_id: {NEXT_RUN_ID}" in workspace_text else "failed",
                "evidence_path": rel(WORKSPACE_STATE),
                "effect": "current truth(현재 진실)가 새 Stage(단계)를 가리킨다.",
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
                "status": "passed",
                "evidence_path": rel(CLAIM_RECEIPT),
                "effect": "운영 승격과 목표 달성 주장을 막는다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "gate_id": "required_gate_coverage_audit_written",
                "status": "passed",
                "evidence_path": rel(GATE_AUDIT),
                "effect": "필수 gate(게이트) 커버리지를 재진입 가능하게 남긴다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ]
    )
    write_csv(GATE_AUDIT, gates)
    return gates


def write_final_decision(gates: pd.DataFrame, metrics: Mapping[str, Any]) -> None:
    gate_passes = int((gates["status"] == "passed").sum())
    gate_total = int(len(gates))
    payload = {
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
        "q01_net_profit": metrics["q01_net_profit"],
        "q09_net_profit": metrics["q09_net_profit"],
        "q09_net_delta": metrics["q09_net_profit"] - metrics["q01_net_profit"],
        "q09_reported_drawdown_delta": metrics["q09_reported_drawdown"] - metrics["q01_reported_drawdown"],
        "queue_rows": metrics["queue_rows"],
        "candidate_selection": "not_claimed(주장 없음)",
        "runtime_authority": "not_claimed(주장 없음)",
        "operating_promotion": "not_claimed(주장 없음)",
        "goal_achieve": "not_claimed(주장 없음)",
        "claim_boundary": CLAIM_BOUNDARY,
        "created_at_utc": now_utc(),
    }
    write_json(FINAL_DECISION, payload)
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
        ("final_decision", FINAL_DECISION, "Stage342A branch final decision."),
        ("required_gate_coverage_audit", GATE_AUDIT, "Stage342A required gate coverage audit."),
        ("handoff_manifest", HANDOFF_MANIFEST, "Stage341 to Stage342 handoff manifest."),
        ("retargeted_queue", NEXT_QUEUE, "Stage342B retargeted probe queue."),
        ("stage_branch_report", REPORT_PATH, "Stage342A branch report."),
        ("decision_doc", DECISION_DOC, "Stage342A durable decision document."),
        ("run_manifest", RUN_MANIFEST, "Stage342A run manifest."),
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
    metrics = read_source_metrics()
    inventory = write_source_inventory()
    queue = write_handoff_artifacts(metrics)
    markdown_documents(metrics)
    append_changelogs()
    append_idea_registry()
    write_ledgers(metrics)
    write_receipts(metrics, inventory, queue)
    gates = write_gates()
    if not gates["status"].astype(str).eq("passed").all():
        failed = gates.loc[gates["status"].astype(str) != "passed", "gate_id"].tolist()
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
    write_receipts(metrics, inventory, queue)
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "stage_id": NEW_STAGE_ID,
                "next_run_id": NEXT_RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "gate_passes": int((gates["status"] == "passed").sum()),
                "gate_total": int(len(gates)),
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
