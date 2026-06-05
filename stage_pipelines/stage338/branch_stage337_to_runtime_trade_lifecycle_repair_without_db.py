from __future__ import annotations

import csv
import hashlib
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from stage_pipelines.stage337 import (  # noqa: E402
    review_runtime_positive_low_pf_recovery_drawdown_dual_probe_repair_mt5_runtime_probe_or_repair_without_db as jr,
)


class ArtifactAccess:
    def io_path(self, path: Path | str) -> Path:
        candidate = Path(path)
        if not candidate.is_absolute():
            candidate = ROOT / candidate
        raw = str(candidate)
        if raw.startswith("\\\\?\\"):
            return Path(raw)
        if len(raw) >= 240:
            return Path("\\\\?\\" + raw)
        return candidate

    def rel(self, path: Path | str) -> str:
        candidate = Path(path)
        if not candidate.is_absolute():
            candidate = ROOT / candidate
        try:
            return candidate.resolve().relative_to(ROOT.resolve()).as_posix()
        except ValueError:
            return candidate.as_posix()

    def sha256_file(self, path: Path | str) -> str:
        digest = hashlib.sha256()
        with self.io_path(path).open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
        return digest.hexdigest()


aw = ArtifactAccess()

TODAY = "2026-06-01"
OLD_STAGE_ID = jr.STAGE_ID
NEW_STAGE_ID = "338_runtime_trade_lifecycle__proxy_positive_mt5_negative_repair"
OLD_STAGE_DIR = ROOT / "stages" / OLD_STAGE_ID
NEW_STAGE_DIR = ROOT / "stages" / NEW_STAGE_ID

RUN_NUMBER = "run338A"
RUN_ID = "run338A_branch_stage337_to_runtime_trade_lifecycle_repair_without_db_v1"
NEXT_RUN_ID = "run338B_design_runtime_trade_lifecycle_proxy_positive_mt5_negative_repair_without_db_v1"
STATUS = "completed_stage338A_branch_from_stage337_runtime_trade_lifecycle_repair_scaffolded"
JUDGMENT = "stage_branch_completed_stage337_too_heavy_topic_pivot_to_runtime_trade_lifecycle_repair"
DECISION = "stage338A_open_run338B_design_runtime_trade_lifecycle_proxy_positive_mt5_negative_repair"
CLAIM_BOUNDARY = (
    "state_sync_stage_branch_only_no_model_selection_no_training_no_mt5_execution_no_forward_"
    "no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

RUN_DIR = NEW_STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = NEW_STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEW_DIR / "run338A_stage_branch_from_stage337_runtime_trade_lifecycle_repair.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage338A_branch_from_stage337_runtime_trade_lifecycle_repair.md"
STAGE_BRIEF = NEW_STAGE_DIR / "00_spec" / "stage_brief.md"
STAGE_README = NEW_STAGE_DIR / "README.md"
INPUT_MANIFEST = NEW_STAGE_DIR / "01_inputs" / "stage338_input_manifest.csv"
STAGE_LEDGER = NEW_STAGE_DIR / "03_reviews" / "stage_run_ledger.csv"
SELECTION_STATUS = NEW_STAGE_DIR / "04_selected" / "selection_status.md"
OLD_SELECTION_STATUS = OLD_STAGE_DIR / "04_selected" / "selection_status.md"
OLD_STAGE_README = OLD_STAGE_DIR / "README.md"

BRANCH_HANDOFF = RUN_DIR / "stage337_to_stage338_branch_handoff.csv"
DESIGN_QUEUE = RUN_DIR / "run338B_design_queue.csv"
NEGATIVE_MEMORY = RUN_DIR / "stage338_negative_memory_seed.csv"
SEED_SURFACE = RUN_DIR / "stage338_seed_surface.csv"
ARTIFACT_LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
PROJECT_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
NEGATIVE_RESULT_REGISTER = ROOT / "docs" / "registers" / "negative_result_register.md"
IDEA_REGISTRY = ROOT / "docs" / "registers" / "idea_registry.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs" / "context" / "current_working_state.md"
ROOT_CHANGELOG = ROOT / "CHANGELOG.md"
WORKSPACE_CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"

INPUT_FILES = (
    jr.FINAL_DECISION,
    jr.SCORECARD,
    jr.ATTRIBUTION,
    jr.FAILURE_MEMORY,
    jr.NEXT_QUEUE,
    jr.GATE_AUDIT,
    jr.RESULT_JUDGMENT_RECEIPT,
)
OUTPUT_FILES = (
    STAGE_BRIEF,
    STAGE_README,
    INPUT_MANIFEST,
    STAGE_LEDGER,
    SELECTION_STATUS,
    OLD_SELECTION_STATUS,
    BRANCH_HANDOFF,
    DESIGN_QUEUE,
    NEGATIVE_MEMORY,
    SEED_SURFACE,
    ARTIFACT_LINEAGE_RECEIPT,
    CLAIM_RECEIPT,
    GATE_AUDIT,
    FINAL_DECISION,
    RUN_MANIFEST,
    REPORT_PATH,
    DECISION_DOC,
    WORKSPACE_STATE,
    CURRENT_WORKING_STATE,
    ROOT_CHANGELOG,
    WORKSPACE_CHANGELOG,
    RUN_REGISTRY,
    PROJECT_LEDGER,
    ARTIFACT_REGISTRY,
    NEGATIVE_RESULT_REGISTER,
    IDEA_REGISTRY,
    Path(__file__),
)


def now_utc() -> str:
    return datetime.now(tz=UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def io(path: Path | str) -> Path:
    return aw.io_path(path)


def rel(path: Path | str) -> str:
    return aw.rel(path)


def exists(path: Path | str) -> bool:
    return io(path).exists()


def ensure_parent(path: Path) -> None:
    io(path.parent).mkdir(parents=True, exist_ok=True)


def read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(io(path), low_memory=False)


def read_json(path: Path) -> Any:
    return json.loads(io(path).read_text(encoding="utf-8-sig"))


def write_csv(path: Path, frame: pd.DataFrame) -> Path:
    ensure_parent(path)
    with io(path).open("w", encoding="utf-8-sig", newline="") as handle:
        frame.to_csv(handle, index=False, lineterminator="\n", quoting=csv.QUOTE_MINIMAL)
    return path


def write_json(path: Path, payload: Any) -> Path:
    ensure_parent(path)
    io(path).write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True, default=str) + "\n", encoding="utf-8")
    return path


def write_bom_text(path: Path, text: str) -> Path:
    ensure_parent(path)
    io(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig", newline="\n")
    return path


def sha(path: Path) -> str:
    return aw.sha256_file(path)


def display_path(path: Path | str) -> str:
    value = Path(path)
    try:
        if str(value.resolve()).lower().startswith(str(ROOT.resolve()).lower()):
            return rel(value)
    except OSError:
        pass
    return value.as_posix()


def append_text_once(path: Path, marker: str, text: str) -> None:
    current = io(path).read_text(encoding="utf-8-sig") if exists(path) else ""
    if marker in current:
        return
    next_text = (current.rstrip() + "\n\n" + text.strip() + "\n") if current.strip() else text.strip() + "\n"
    write_bom_text(path, next_text)


def append_or_replace_csv(path: Path, key_columns: Iterable[str], row: Mapping[str, Any]) -> None:
    frame = read_csv(path) if exists(path) else pd.DataFrame()
    if frame.empty:
        frame = pd.DataFrame(columns=list(row.keys()))
    for column in row:
        if column not in frame.columns:
            frame[column] = ""
    mask = pd.Series(True, index=frame.index)
    for key in key_columns:
        if key in frame.columns:
            mask = mask & frame[key].astype(str).eq(str(row[key]))
        else:
            mask = mask & False
    frame = frame.loc[~mask].copy()
    frame = pd.concat([frame, pd.DataFrame([row])], ignore_index=True)
    ordered = list(dict.fromkeys(list(frame.columns) + list(row.keys())))
    write_csv(path, frame[ordered])


def build_tables() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, dict[str, Any]]:
    jr_final = read_json(jr.FINAL_DECISION)
    scorecard = read_csv(jr.SCORECARD)
    attribution = read_csv(jr.ATTRIBUTION)
    failure_memory = read_csv(jr.FAILURE_MEMORY)
    best = scorecard.sort_values(["mt5_net_profit", "mt5_profit_factor", "mt5_recovery_factor"], ascending=False).iloc[0]
    primary = scorecard.loc[scorecard["probe_role"].astype(str).eq("runtime_probe_primary_raw_top_not_selected")].iloc[0]

    handoff = pd.DataFrame(
        [
            {
                "handoff_id": "stage337JR_to_stage338A",
                "old_stage_id": OLD_STAGE_ID,
                "new_stage_id": NEW_STAGE_ID,
                "source_run_id": jr.RUN_ID,
                "branch_run_id": RUN_ID,
                "next_run_id": NEXT_RUN_ID,
                "topic_pivot": "proxy-positive signal reproduced but MT5 trade lifecycle negative(프록시 양수 신호는 재현됐지만 MT5 거래 생명주기 음수)",
                "best_less_bad_model_id": best["model_id"],
                "best_mt5_net_profit": best["mt5_net_profit"],
                "best_mt5_profit_factor": best["mt5_profit_factor"],
                "best_mt5_recovery_factor": best["mt5_recovery_factor"],
                "primary_model_id": primary["model_id"],
                "primary_mt5_net_profit": primary["mt5_net_profit"],
                "branch_reason": "Stage337(337단계)이 너무 무거워져 새 question(질문)으로 분기한다.",
                "allowed_use": "seed surface and negative memory(씨앗 표면과 부정 기억)",
                "forbidden_use": "baseline, selected model, operating promotion(기준선, 선정 모델, 운영 승격)",
                "effect": "Stage338(338단계)이 거래 생명주기 수리를 가볍게 탐색하게 한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    seed = scorecard[
        [
            "model_id",
            "probe_role",
            "model_family",
            "proxy_net_log_return_after_cost",
            "proxy_profit_factor",
            "signal_density",
            "side_balance_ratio",
            "mt5_net_profit",
            "mt5_profit_factor",
            "mt5_expectancy",
            "mt5_recovery_factor",
            "mt5_drawdown",
            "mt5_trade_count",
            "proxy_mt5_parity_ok",
            "repair_hint",
        ]
    ].copy()
    seed["seed_surface_role"] = "reference_surface_not_baseline(참고 표면, 기준선 아님)"
    seed["effect"] = "Stage338(338단계) feature/label/rule stack(피처/라벨/규칙 묶음) 설계의 출발점으로만 쓴다."
    seed["claim_boundary"] = CLAIM_BOUNDARY

    negative = failure_memory.copy()
    negative["new_stage_id"] = NEW_STAGE_ID
    negative["source_run_id"] = jr.RUN_ID
    negative["effect"] = negative["effect"].astype(str) + " Stage338(338단계)에서 반복 금지 조건으로 쓴다."
    negative["claim_boundary"] = CLAIM_BOUNDARY

    summary = {
        "best_model_id": str(best["model_id"]),
        "best_mt5_net_profit": float(best["mt5_net_profit"]),
        "best_mt5_profit_factor": float(best["mt5_profit_factor"]),
        "best_mt5_recovery_factor": float(best["mt5_recovery_factor"]),
        "best_mt5_drawdown": float(best["mt5_drawdown"]),
        "best_mt5_trade_count": int(float(best["mt5_trade_count"])),
        "primary_model_id": str(primary["model_id"]),
        "primary_mt5_net_profit": float(primary["mt5_net_profit"]),
        "source_parity_ok": bool(jr_final.get("parity_ok")),
        "source_mismatch_rows": int(jr_final.get("mismatch_rows", 0)),
        "source_attempt_rows": int(jr_final.get("attempt_rows", 0)),
    }
    return handoff, seed, negative, summary


def build_design_queue() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "queue_id": "run338B_design_runtime_trade_lifecycle_proxy_positive_mt5_negative_repair",
                "next_run_id": NEXT_RUN_ID,
                "priority": "P0",
                "primary_family": "experiment_design(실험 설계)",
                "primary_skill": "obsidian-experiment-design(옵시디언 실험 설계)",
                "support_skills": "obsidian-data-integrity(데이터 무결성);obsidian-model-validation(모델 검증);obsidian-artifact-lineage(산출물 계보)",
                "stage_question": "Can timestamp-safe trade lifecycle labels/features/rules turn proxy-reproduced signals into positive MT5 KPI?(시점 안전 거래 생명주기 라벨/피처/규칙이 재현된 신호를 양수 MT5 KPI로 바꿀 수 있는가?)",
                "required_inputs": f"{rel(SEED_SURFACE)};{rel(NEGATIVE_MEMORY)};{rel(jr.SCORECARD)};{rel(jr.ATTRIBUTION)}",
                "design_requirements": "density throttle(밀도 제한);side loss quarantine(방향 손실 격리);cost-stress objective(비용 압박 목적);drawdown corridor(낙폭 통로);session/regime split(세션/국면 분할);Tier A/B paired records(Tier A/B 쌍 기록)",
                "forbidden_action": "reuse Stage337 as a baseline or selected model(Stage337을 기준선/선정 모델로 재사용)",
                "effect": "새 stage(단계)에서 작은 설계 표면부터 다시 공격적으로 탐색한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )


def gate_row(gate: str, status: str, evidence: str, effect: str) -> dict[str, Any]:
    return {
        "gate_id": gate,
        "status": status,
        "evidence_path": evidence,
        "effect": effect,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def make_gates(summary: Mapping[str, Any]) -> pd.DataFrame:
    source_gate = read_csv(jr.GATE_AUDIT)
    return pd.DataFrame(
        [
            gate_row("source_jr_gates_passed", "passed" if source_gate["status"].astype(str).eq("passed").all() else "failed", rel(jr.GATE_AUDIT), "JR valid negative(JR 유효한 부정) 근거만 새 stage(단계)로 넘긴다."),
            gate_row("new_stage_scaffold_created", "passed" if exists(STAGE_BRIEF) and exists(SELECTION_STATUS) else "failed", f"{rel(STAGE_BRIEF)};{rel(SELECTION_STATUS)}", "Stage338(338단계) 필수 폴더와 문서를 만든다."),
            gate_row("handoff_and_seed_written", "passed" if exists(BRANCH_HANDOFF) and exists(SEED_SURFACE) and exists(NEGATIVE_MEMORY) else "failed", f"{rel(BRANCH_HANDOFF)};{rel(SEED_SURFACE)};{rel(NEGATIVE_MEMORY)}", "negative memory(부정 기억)와 seed surface(씨앗 표면)를 분리한다."),
            gate_row("design_queue_opened", "passed" if exists(DESIGN_QUEUE) else "failed", rel(DESIGN_QUEUE), "run338B design queue(설계 대기열)를 연다."),
            gate_row("current_truth_updated", "passed" if exists(WORKSPACE_STATE) else "failed", rel(WORKSPACE_STATE), "current truth(현재 진실)를 Stage338(338단계)로 옮긴다."),
            gate_row("no_forbidden_operating_claim", "passed", rel(FINAL_DECISION), "selection/promotion/runtime authority/Goal(선택/승격/런타임 권위/목표)을 주장하지 않는다."),
            gate_row("required_gate_coverage_audit_written", "passed", rel(GATE_AUDIT), "gate coverage(게이트 커버리지)를 closeout(종료 기록)에 연결한다."),
        ]
    )


def write_stage_docs(summary: Mapping[str, Any]) -> None:
    stage_brief = f"""# Stage338 Runtime Trade Lifecycle Repair(338단계 런타임 거래 생명주기 수리)

## Canonical Stage ID(정식 단계 ID)

`{NEW_STAGE_ID}`

## Stage Question(단계 질문)

Can timestamp-safe trade lifecycle labels/features/rules turn proxy-reproduced signals into positive MT5 KPI?
(시점 안전 거래 생명주기 라벨/피처/규칙이 재현된 신호를 양수 MT5 핵심 성과 지표로 바꿀 수 있는가?)

## Source Handoff(원천 인계)

- source_stage(원천 단계): `{OLD_STAGE_ID}`
- source_run(원천 실행): `{jr.RUN_ID}`
- branch_run(분기 실행): `{RUN_ID}`
- best_less_bad_model(가장 덜 나쁜 모델): `{summary['best_model_id']}`
- best_mt5_net_profit(가장 덜 나쁜 MT5 순수익): `{summary['best_mt5_net_profit']}`
- best_mt5_profit_factor(가장 덜 나쁜 MT5 수익 팩터): `{summary['best_mt5_profit_factor']}`

## Scope(범위)

Stage338(338단계)은 Stage337(337단계)의 proxy-positive MT5-negative(프록시 양수 MT5 음수) 결과를 baseline(기준선)으로 쓰지 않는다.
Effect(효과): negative memory(부정 기억)를 제약으로 삼고, trade lifecycle repair(거래 생명주기 수리)를 새 주제로 가볍게 판다.

## Required Axes(필수 축)

- density throttle(밀도 제한)
- side loss quarantine(방향 손실 격리)
- cost-stress objective(비용 압박 목적)
- drawdown corridor(낙폭 통로)
- session/regime split(세션/국면 분할)
- Tier A/B paired records(Tier A/B 쌍 기록)

## Forbidden Claims(금지 주장)

No selected model(선정 모델 없음), no baseline(기준선 없음), no runtime authority(런타임 권위 없음), no operating promotion(운영 승격 없음), no Goal Achieve(목표 달성 없음).
"""
    selection = f"""# Stage338 Selection Status(338단계 선택 상태)

- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- selected_model(선정 모델): `none(없음)`
- source_stage(원천 단계): `{OLD_STAGE_ID}`
- source_judgment(원천 판정): `valid_negative(유효한 부정)`
- seed_surface(씨앗 표면): `{rel(SEED_SURFACE)}`
- negative_memory(부정 기억): `{rel(NEGATIVE_MEMORY)}`
- runtime_authority(런타임 권위): `not_claimed(주장 없음)`
- operating_promotion(운영 승격): `not_claimed(주장 없음)`
- goal_achieve(목표 달성): `not_claimed(주장 없음)`

Effect(효과): Stage338(338단계)은 Stage337(337단계)의 무거운 산출물을 선택 모델로 끌고 오지 않는다.
"""
    report = f"""# run338A Stage Branch(단계 분기)

## Summary(요약)

- run_id(실행 ID): `{RUN_ID}`
- old_stage(이전 단계): `{OLD_STAGE_ID}`
- new_stage(새 단계): `{NEW_STAGE_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- next_run(다음 실행): `{NEXT_RUN_ID}`
- gates(게이트): see `{rel(GATE_AUDIT)}`

## Action(행동)

Stage337(337단계)의 JR valid negative(유효한 부정)를 Stage338(338단계)의 seed surface(씨앗 표면)와 negative memory(부정 기억)로 분기했다.
Effect(효과): 다음 탐색은 Stage337(337단계)의 큰 파일 더미를 계속 키우지 않고, trade lifecycle repair(거래 생명주기 수리) 질문에 집중한다.

## Boundary(경계)

이 분기는 state sync(상태 동기화)와 topic pivot(주제 전환)이다. Model selection(모델 선택), MT5 execution(MT5 실행), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 없다.
"""
    decision = f"""# {TODAY} Stage338A Branch Decision(338A 분기 결정)

- decision(결정): `{DECISION}`
- from(출발): `{OLD_STAGE_ID}` / `{jr.RUN_ID}`
- to(도착): `{NEW_STAGE_ID}` / `{NEXT_RUN_ID}`
- reason(이유): Stage337(337단계)이 너무 무거워졌고, 다음 질문은 trade lifecycle repair(거래 생명주기 수리)다.
- evidence(근거): `{rel(jr.FINAL_DECISION)}`, `{rel(jr.SCORECARD)}`, `{rel(jr.FAILURE_MEMORY)}`

Action(행동): Stage338(338단계)을 새 canonical stage(정식 단계)로 열었다.
Effect(효과): 실패 기억은 보존하고, stage scope(단계 범위)는 가볍게 만든다.

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

Stage338(338단계)은 Stage337(337단계)의 valid negative(유효한 부정)를 이어받되, 새 work packet(작업 묶음)은 trade lifecycle repair(거래 생명주기 수리) 설계부터 시작한다.

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
    old_selection = f"""# Stage337 Selection Status(337단계 선택 상태)

- latest_run(최신 실행): `{jr.RUN_ID}`
- branched_to_stage(분기된 단계): `{NEW_STAGE_ID}`
- branch_run(분기 실행): `{RUN_ID}`
- next_active_run(다음 활성 실행): `{NEXT_RUN_ID}`
- selected_model(선정 모델): `none(없음)`
- final_stage337_judgment(최종 337단계 판정): `valid_negative(유효한 부정)`
- best_runtime_probe_model(가장 덜 나쁜 런타임 탐침 모델): `{summary['best_model_id']}`
- best_mt5_net_profit(가장 덜 나쁜 MT5 순수익): `{summary['best_mt5_net_profit']}`
- runtime_authority(런타임 권위): `not_claimed(주장 없음)`
- operating_promotion(운영 승격): `not_claimed(주장 없음)`
- goal_achieve(목표 달성): `not_claimed(주장 없음)`

Effect(효과): Stage337(337단계)은 더 키우지 않고 Stage338(338단계)의 seed surface(씨앗 표면)로만 남긴다.
"""
    write_bom_text(STAGE_BRIEF, stage_brief)
    write_bom_text(STAGE_README, stage_brief)
    write_bom_text(SELECTION_STATUS, selection)
    write_bom_text(REPORT_PATH, report)
    write_bom_text(DECISION_DOC, decision)
    write_bom_text(CURRENT_WORKING_STATE, current)
    write_bom_text(WORKSPACE_STATE, workspace)
    write_bom_text(OLD_SELECTION_STATUS, old_selection)

    marker = f"run338A {RUN_ID}"
    append_text_once(
        OLD_STAGE_README,
        marker,
        f"""## run338A Stage Branch(단계 분기)

- branch_run(분기 실행): `{RUN_ID}`
- new_stage(새 단계): `{NEW_STAGE_ID}`
- next_run(다음 실행): `{NEXT_RUN_ID}`
- effect(효과): Stage337(337단계)을 더 무겁게 만들지 않고 trade lifecycle repair(거래 생명주기 수리)를 Stage338(338단계)로 분리했다.
""",
    )
    changelog = f"""## {TODAY} run338A Stage Branch(단계 분기)

- action(행동): Stage337(337단계)의 JR valid negative(유효한 부정)를 Stage338(338단계)으로 분기했다.
- effect(효과): negative memory(부정 기억)는 유지하고, 다음 설계는 `{NEXT_RUN_ID}`에서 가볍게 시작한다.
- boundary(경계): model selection(모델 선택), operating promotion(운영 승격), Goal Achieve(목표 달성)는 없다.
"""
    append_text_once(ROOT_CHANGELOG, marker, changelog)
    append_text_once(WORKSPACE_CHANGELOG, marker, changelog)
    append_text_once(
        NEGATIVE_RESULT_REGISTER,
        marker,
        f"""## {TODAY} run338A Stage Branch Negative Memory(부정 기억)

- subject(대상): Stage337 proxy-positive MT5-negative runtime probe(프록시 양수 MT5 음수 런타임 탐침)
- judgment(판정): `valid_negative(유효한 부정)`
- carried_to(이월 대상): `{NEW_STAGE_ID}`
- evidence(근거): `{rel(jr.FINAL_DECISION)}`, `{rel(jr.SCORECARD)}`, `{rel(NEGATIVE_MEMORY)}`
- effect(효과): 신호 재현 문제로 오해하지 않고 거래 생명주기 수리 제약으로 사용한다.
""",
    )
    append_text_once(
        IDEA_REGISTRY,
        marker,
        f"""## {TODAY} Stage338 Trade Lifecycle Repair Seed(거래 생명주기 수리 씨앗)

- idea(아이디어): proxy-reproduced signal(프록시 재현 신호)에 density throttle(밀도 제한), side loss quarantine(방향 손실 격리), cost-stress objective(비용 압박 목적)를 붙인다.
- source(원천): `{jr.RUN_ID}`
- next_run(다음 실행): `{NEXT_RUN_ID}`
- effect(효과): 실패를 아이디어 사망으로 닫지 않고 새 offensive exploration seed(공격 탐색 씨앗)로 보존한다.
""",
    )


def write_receipts(summary: Mapping[str, Any]) -> None:
    base = {
        "run_id": RUN_ID,
        "stage_id": NEW_STAGE_ID,
        "parent_stage_id": OLD_STAGE_ID,
        "parent_run_id": jr.RUN_ID,
        "created_at_utc": now_utc(),
        "status": STATUS,
        "judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(
        ARTIFACT_LINEAGE_RECEIPT,
        {
            **base,
            "source_inputs": [rel(path) for path in INPUT_FILES],
            "branch_outputs": [display_path(path) for path in OUTPUT_FILES if exists(path)],
            "source_artifact_hashes": {rel(path): sha(path) for path in INPUT_FILES if exists(path)},
            "effect": "Stage337(337단계) 산출물을 Stage338(338단계)의 seed surface(씨앗 표면)로 계보 연결한다.",
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            **base,
            "candidate_selection": "not_run",
            "training": "not_run",
            "mt5_execution": "not_run",
            "forward_passed": "not_claimed",
            "forward_failed": "not_claimed",
            "goal_achieve": "not_claimed",
            "runtime_authority": "not_claimed",
            "operating_promotion": "not_claimed",
            "effect": "Stage branch(단계 분기)를 운영 주장으로 오해하지 않게 한다.",
        },
    )


def write_registers(summary: Mapping[str, Any], gates: pd.DataFrame) -> None:
    base = {
        "stage_id": NEW_STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": jr.RUN_ID,
        "run_date": TODAY,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_run_id": NEXT_RUN_ID,
        "primary_artifact": rel(FINAL_DECISION),
        "report_path": rel(REPORT_PATH),
        "gate_passes": int(gates["status"].astype(str).eq("passed").sum()),
        "gate_total": int(len(gates)),
        "claim_boundary": CLAIM_BOUNDARY,
    }
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], base)
    rows = [
        {
            **base,
            "view": "Tier A separate(Tier A 분리)",
            "tier": "Tier A",
            "metric_scope": "stage_branch_handoff",
            "candidate_model_id": summary["best_model_id"],
            "net_profit": summary["best_mt5_net_profit"],
            "profit_factor": summary["best_mt5_profit_factor"],
            "drawdown": summary["best_mt5_drawdown"],
            "recovery_factor": summary["best_mt5_recovery_factor"],
            "trade_count": summary["best_mt5_trade_count"],
            "result_status": JUDGMENT,
        },
        {**base, "view": "Tier B separate(Tier B 분리)", "tier": "Tier B", "metric_scope": "missing_required", "result_status": "missing_required"},
        {**base, "view": "Tier A+B combined(Tier A+B 합산)", "tier": "Tier A+B", "metric_scope": "missing_required", "result_status": "missing_required"},
    ]
    for row in rows:
        append_or_replace_csv(PROJECT_LEDGER, ["run_id", "view"], row)
        append_or_replace_csv(STAGE_LEDGER, ["run_id", "view"], row)


def write_artifact_registry(paths: Sequence[Path]) -> None:
    if exists(ARTIFACT_REGISTRY):
        registry = read_csv(ARTIFACT_REGISTRY)
    else:
        registry = pd.DataFrame()
    required = ["stage_id", "run_id", "artifact_type", "path", "sha256", "created_at", "claim_boundary"]
    for column in required:
        if column not in registry.columns:
            registry[column] = ""
    rows = []
    for path in paths:
        if not exists(path):
            continue
        rows.append(
            {
                "stage_id": NEW_STAGE_ID,
                "run_id": RUN_ID,
                "artifact_type": path.suffix.lstrip(".") or "artifact",
                "path": display_path(path),
                "sha256": sha(path),
                "created_at": TODAY,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    if rows:
        new_paths = {row["path"] for row in rows}
        registry = registry.loc[~((registry["run_id"].astype(str) == RUN_ID) & registry["path"].astype(str).isin(new_paths))].copy()
        registry = pd.concat([registry, pd.DataFrame(rows)], ignore_index=True)
    write_csv(ARTIFACT_REGISTRY, registry[required + [c for c in registry.columns if c not in required]])


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
        io(path).mkdir(parents=True, exist_ok=True)
    missing = [rel(path) for path in INPUT_FILES if not exists(path)]
    if missing:
        raise FileNotFoundError(f"missing branch inputs: {missing}")

    handoff, seed, negative, summary = build_tables()
    write_csv(BRANCH_HANDOFF, handoff)
    write_csv(SEED_SURFACE, seed)
    write_csv(NEGATIVE_MEMORY, negative)
    write_csv(INPUT_MANIFEST, pd.DataFrame([{"input_path": rel(path), "exists": exists(path), "sha256": sha(path) if exists(path) else "", "effect": "Stage338(338단계) 인입 근거", "claim_boundary": CLAIM_BOUNDARY} for path in INPUT_FILES]))
    write_csv(DESIGN_QUEUE, build_design_queue())
    write_stage_docs(summary)
    gates = make_gates(summary)
    write_csv(GATE_AUDIT, gates)
    final = {
        "stage_id": NEW_STAGE_ID,
        "run_id": RUN_ID,
        "parent_stage_id": OLD_STAGE_ID,
        "parent_run_id": jr.RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_action": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
        "candidate_selection": "not_run",
        "training": "not_run",
        "mt5_execution": "not_run",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "gate_passes": int(gates["status"].astype(str).eq("passed").sum()),
        "gate_total": int(len(gates)),
        **summary,
    }
    write_json(FINAL_DECISION, final)
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "stage_id": NEW_STAGE_ID,
            "created_at": TODAY,
            "created_at_utc": now_utc(),
            "script": rel(Path(__file__)),
            "inputs": [rel(path) for path in INPUT_FILES],
            "outputs": [display_path(path) for path in OUTPUT_FILES if exists(path)],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_receipts(summary)
    write_registers(summary, gates)
    write_artifact_registry([path for path in OUTPUT_FILES if path != ARTIFACT_REGISTRY])

    failed = gates.loc[~gates["status"].astype(str).eq("passed")]
    if not failed.empty:
        raise RuntimeError(f"Stage338 branch gates failed: {failed[['gate_id', 'status']].to_dict(orient='records')}")

    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "new_stage_id": NEW_STAGE_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "next_run_id": NEXT_RUN_ID,
                "gate_passes": final["gate_passes"],
                "gate_total": final["gate_total"],
                "best_model_id": summary["best_model_id"],
                "best_mt5_net_profit": summary["best_mt5_net_profit"],
                "goal_achieve": "not_claimed",
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
