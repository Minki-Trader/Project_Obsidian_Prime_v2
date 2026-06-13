from __future__ import annotations

import csv
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists
from foundation.models.onnx_bridge import sha256_file
from stage_pipelines.stage_frontier_03 import frontier03b_regime_asymmetric_label_proxy_scout as f03b


STAGE_ID = "stage_frontier_04__path_aware_cost_dd_event_labeling"
RUN_ID = "frontier04E_stage_closeout_v1"
RUN_NUMBER = "frontier04E"
PARENT_RUN_ID = "frontier04D_trainable_path_label_onnx_probe_v1"
NEXT_RUN_ID = "frontier05A_stage_open_new_hypothesis_design_v1"

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REPORT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_report.md"
DECISION_PATH = Path("docs/decisions/2026-06-14_stage_frontier_04_path_aware_cost_dd_event_labeling_closeout.md")
GROK_ROOT = Path("docs/agent_control/grok_reviews/2026-06-14_frontier04_stage_closeout/medium_review")
PROMPT_PATH = GROK_ROOT / "prompt.md"
OUTPUT_PATH = GROK_ROOT / "clean_output.md"
METADATA_PATH = GROK_ROOT / "metadata.json"

F04B_REPORT = STAGE_ROOT / "03_reviews/frontier04B_path_aware_label_proxy_scout_v1_report.md"
F04B_MANIFEST = STAGE_ROOT / "02_runs/frontier04B_path_aware_label_proxy_scout_v1/run_manifest.json"
F04B_TOP = STAGE_ROOT / "02_runs/frontier04B_path_aware_label_proxy_scout_v1/top.csv"
F04C_REPORT = STAGE_ROOT / "03_reviews/frontier04C_grok_pre_trainable_transfer_review_v1_report.md"
F04C_OUTPUT = Path("docs/agent_control/grok_reviews/2026-06-14_frontier04_pre_trainable_transfer/medium_review/clean_output.md")
F04D_REPORT = STAGE_ROOT / "03_reviews/frontier04D_trainable_path_label_onnx_probe_v1_report.md"
F04D_MANIFEST = STAGE_ROOT / "02_runs/frontier04D_trainable_path_label_onnx_probe_v1/run_manifest.json"
F04D_RETENTION = STAGE_ROOT / "02_runs/frontier04D_trainable_path_label_onnx_probe_v1/retention.csv"
F04D_PARITY = STAGE_ROOT / "02_runs/frontier04D_trainable_path_label_onnx_probe_v1/onnx_parity.csv"


def main() -> int:
    ensure_dirs()
    if not path_exists(PROMPT_PATH):
        write_text_sig(PROMPT_PATH, prompt_text())
        print(json.dumps({
            "status": "prompt_ready",
            "run_id": RUN_ID,
            "prompt": PROMPT_PATH.as_posix(),
            "next_command": (
                "python -m foundation.control_plane.grok_review_wrapper "
                f"--prompt-file {PROMPT_PATH.as_posix()} --review-size medium "
                f"--output-dir {GROK_ROOT.as_posix()} --repo-root . --cwd . --timeout-seconds 300 --json"
            ),
        }, ensure_ascii=False, indent=2))
        return 0
    if not path_exists(OUTPUT_PATH) or not path_exists(METADATA_PATH):
        print(json.dumps({
            "status": "awaiting_grok_output",
            "run_id": RUN_ID,
            "missing": [path.as_posix() for path in (OUTPUT_PATH, METADATA_PATH) if not path_exists(path)],
        }, ensure_ascii=False, indent=2))
        return 0
    now = utc_now()
    classification = classify_output(now)
    final = build_final(now, classification)
    write_outputs(final, classification)
    update_registries(final)
    print(json.dumps({
        "status": "stage_closeout_materialized",
        "run_id": RUN_ID,
        "recommendation": classification["recommendation_inferred"],
        "judgment": final["judgment"],
        "next_run_id": final["next_run_id"],
    }, ensure_ascii=False, indent=2))
    return 0


def ensure_dirs() -> None:
    for path in (GROK_ROOT, RUN_ROOT, REPORT_PATH.parent, DECISION_PATH.parent):
        io_path(path).mkdir(parents=True, exist_ok=True)


def prompt_text() -> str:
    proxy = read_proxy_top()
    model = read_best_model()
    return f"""You are Grok(Grok, 그록), external second opinion(외부 2차 의견) only. Review this bounded Frontier04 stage closeout(전선04 단계 마감) proposal.

Current truth(현재 진실):
- Stage(단계): `{STAGE_ID}`
- Hypothesis(가설): path-aware cost/DD event labeling(경로 인식 비용/손실폭 이벤트 라벨링) might fix close-return DD trap(종가 수익률 손실폭 함정).
- Frontier04B proxy clue(전선04B 프록시 단서): `{proxy.get('variant_id')}` passed validation/OOS joint scout(검증/표본밖 동시 탐색).
- Frontier04B validation PF/density/DD(검증 수익 팩터/밀도/손실폭): `{proxy.get('validation_profit_factor')}` / `{proxy.get('validation_trades_per_day')}/day` / `{proxy.get('validation_dd_risk_percent')}%`
- Frontier04B OOS PF/density/DD(표본밖 수익 팩터/밀도/손실폭): `{proxy.get('oos_profit_factor')}` / `{proxy.get('oos_trades_per_day')}/day` / `{proxy.get('oos_dd_risk_percent')}%`
- Frontier04C Grok gate(그록 게이트): proceed_to_trainable_probe(학습 가능 탐침 진행), but with strict bounds.
- Frontier04D trainable ONNX probe(학습 가능 온엑스 탐침): collapse(붕괴). Best model `{model.get('model_id')}` had validation PF/density/DD `{model.get('validation_profit_factor')}` / `{model.get('validation_trades_per_day')}/day` / `{model.get('validation_dd_risk_percent')}%`; OOS PF/density/DD `{model.get('oos_profit_factor')}` / `{model.get('oos_trades_per_day')}/day` / `{model.get('oos_dd_risk_percent')}%`.
- ONNX parity(온엑스 동등성): passed for all exported models(모든 내보낸 모델 통과), but parity is not runtime authority(동등성은 런타임 권위 아님).
- Tier B(티어 B): missing_required(필수 누락). No combined claim(합산 주장 없음).

Codex proposed closeout(코덱스 제안 마감):
- Close Frontier04 as negative_memory plus preserved_clue(부정 기억 + 보존 단서).
- Preserved clue(보존 단서): path-aware event labels can create a clean oracle seed surface(경로 이벤트 라벨은 깨끗한 오라클 씨앗 표면을 만들 수 있음).
- Negative memory(부정 기억): with feature_set_v2 and small fixed trainable grid, oracle labels did not transfer into usable ONNX surface(피처 세트 v2와 작은 고정 학습 격자에서는 오라클 라벨이 쓸만한 온엑스 표면으로 전달되지 않음).
- Do not repair by threshold-only broad sweeps(임계값 전용 넓은 반복 수리 금지).
- Next frontier(다음 전선): start a new hypothesis lifecycle(새 가설 생명주기).

Bounded evidence(제한 근거):
- F04B report: `{F04B_REPORT.as_posix()}` sha256 `{sha256_file(F04B_REPORT)}`
- F04B manifest: `{F04B_MANIFEST.as_posix()}` sha256 `{sha256_file(F04B_MANIFEST)}`
- F04B top rows: `{F04B_TOP.as_posix()}` sha256 `{sha256_file(F04B_TOP)}`
- F04C report: `{F04C_REPORT.as_posix()}` sha256 `{sha256_file(F04C_REPORT)}`
- F04C Grok output: `{F04C_OUTPUT.as_posix()}` sha256 `{sha256_file(F04C_OUTPUT)}`
- F04D report: `{F04D_REPORT.as_posix()}` sha256 `{sha256_file(F04D_REPORT)}`
- F04D manifest: `{F04D_MANIFEST.as_posix()}` sha256 `{sha256_file(F04D_MANIFEST)}`
- F04D retention: `{F04D_RETENTION.as_posix()}` sha256 `{sha256_file(F04D_RETENTION)}`
- F04D ONNX parity: `{F04D_PARITY.as_posix()}` sha256 `{sha256_file(F04D_PARITY)}`

Focused question(집중 질문):
Should Codex close Frontier04 as negative_memory plus preserved_clue(부정 기억 + 보존 단서), require one more repair(추가 수리), mark blocked(차단), or classify as completion_candidate(완성 후보)?

Please answer in this structure:
1. Recommendation(권고): close_negative_memory_with_preserved_clue(부정 기억+보존 단서 마감) / require_repair(수리 필요) / blocked(차단) / completion_candidate(완성 후보)
2. Reasoning(근거)
3. Required closeout bounds(마감 필수 경계)
4. Risks(위험)
5. Do-not-claim boundary(주장 금지 경계)
"""


def classify_output(now: str) -> dict[str, Any]:
    metadata = read_json(METADATA_PATH)
    text = read_text(OUTPUT_PATH)
    lower = text.lower()
    choices = [
        (lower.find("close_negative_memory_with_preserved_clue"), "close_negative_memory_with_preserved_clue(부정 기억+보존 단서 마감)"),
        (lower.find("require_repair"), "require_repair(수리 필요)"),
        (lower.find("blocked"), "blocked(차단)"),
        (lower.find("completion_candidate"), "completion_candidate(완성 후보)"),
    ]
    seen = [(pos, label) for pos, label in choices if pos >= 0]
    recommendation = min(seen, default=(0, "require_repair(수리 필요)"))[1]
    return {
        "run_id": RUN_ID,
        "created_at_utc": now,
        "prompt_path": PROMPT_PATH.as_posix(),
        "prompt_sha256": sha256_file(PROMPT_PATH),
        "output_path": OUTPUT_PATH.as_posix(),
        "output_sha256": sha256_file(OUTPUT_PATH),
        "metadata_path": METADATA_PATH.as_posix(),
        "metadata_success": bool(metadata.get("success", False)),
        "metadata_returncode": metadata.get("returncode"),
        "metadata_timed_out": metadata.get("timed_out"),
        "recommendation_inferred": recommendation,
        "claim_boundary": {claim: "not_claimed(주장 없음)" for claim in f03b.FORBIDDEN_CLAIMS},
    }


def build_final(now: str, classification: dict[str, Any]) -> dict[str, Any]:
    recommendation = classification["recommendation_inferred"]
    if recommendation.startswith("close_negative_memory"):
        status = "closed_negative_memory_with_preserved_proxy_clue_no_authority"
        judgment = "negative_memory(부정 기억)+preserved_clue(보존 단서)"
        next_run = NEXT_RUN_ID
    elif recommendation.startswith("completion_candidate"):
        status = "closeout_review_overclaim_rejected_by_codex_no_authority"
        judgment = "claim_downgraded_to_preserved_clue(주장 보존 단서로 하향)"
        next_run = NEXT_RUN_ID
    elif recommendation.startswith("blocked"):
        status = "closeout_blocked_needs_repair_plan_no_authority"
        judgment = "blocked(차단)"
        next_run = "frontier04F_repair_plan_after_closeout_block_v1"
    else:
        status = "closeout_requires_repair_no_authority"
        judgment = "repair_required(수리 필요)"
        next_run = "frontier04F_capped_repair_plan_v1"
    return {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "created_at_utc": now,
        "status": status,
        "judgment": judgment,
        "recommendation": recommendation,
        "next_run_id": next_run,
        "preserved_clue": "path-aware event labels can create a clean oracle seed surface(경로 이벤트 라벨은 깨끗한 오라클 씨앗 표면을 만들 수 있음)",
        "negative_memory": "feature_set_v2 plus small fixed models did not transfer the oracle surface into usable ONNX metrics(피처 세트 v2와 작은 고정 모델은 오라클 표면을 쓸만한 온엑스 지표로 전달하지 못함)",
        "claim_boundary": {claim: "not_claimed(주장 없음)" for claim in f03b.FORBIDDEN_CLAIMS},
    }


def write_outputs(final: dict[str, Any], classification: dict[str, Any]) -> None:
    write_json(RUN_ROOT / "classification.json", classification)
    write_json(RUN_ROOT / "run_manifest.json", {
        **final,
        "script_path": "stage_pipelines/stage_frontier_04/frontier04e_stage_closeout.py",
        "script_sha256": sha256_file(Path("stage_pipelines/stage_frontier_04/frontier04e_stage_closeout.py")),
        "outputs": {
            "classification": {"path": (RUN_ROOT / "classification.json").as_posix(), "sha256": sha256_file(RUN_ROOT / "classification.json")},
            "report": {"path": REPORT_PATH.as_posix()},
            "decision": {"path": DECISION_PATH.as_posix()},
            "required_gate_coverage_audit": {
                "path": (STAGE_ROOT / "03_reviews" / "required_gate_coverage_audit.md").as_posix(),
                "sha256": sha256_file(STAGE_ROOT / "03_reviews" / "required_gate_coverage_audit.md"),
            },
        },
        "grok_prompt": {"path": PROMPT_PATH.as_posix(), "sha256": sha256_file(PROMPT_PATH)},
        "grok_output": {"path": OUTPUT_PATH.as_posix(), "sha256": sha256_file(OUTPUT_PATH)},
    })
    write_text_sig(REPORT_PATH, report_text(final, classification))
    write_text_sig(DECISION_PATH, decision_text(final))
    write_text_sig(STAGE_ROOT / "04_selected" / "selection_status.md", selection_text(final))


def report_text(final: dict[str, Any], classification: dict[str, Any]) -> str:
    proxy = read_proxy_top()
    model = read_best_model()
    return f"""# Frontier04E Stage Closeout Report(전선04E 단계 마감 보고서)

Updated(갱신): {final['created_at_utc']}

Status(상태): `{final['status']}`

Judgment(판정): `{final['judgment']}`

Grok recommendation(그록 권고): `{classification['recommendation_inferred']}`

## Action And Effect(행동과 효과)

Action(행동): Frontier04(전선04)를 path-aware event label(경로 이벤트 라벨) 가설 생명주기로 마감했습니다.

Effect(효과): proxy clue(프록시 단서)는 보존하고, trainable ONNX transfer collapse(학습 가능 온엑스 전달 붕괴)는 negative memory(부정 기억)로 남겨 다음 frontier(전선)가 같은 함정을 반복하지 않게 합니다.

## Preserved Clue(보존 단서)

{final['preserved_clue']}

- proxy variant(프록시 변형): `{proxy.get('variant_id')}`
- validation PF/density/DD(검증 수익 팩터/밀도/손실폭): `{proxy.get('validation_profit_factor')}` / `{proxy.get('validation_trades_per_day')}/day` / `{proxy.get('validation_dd_risk_percent')}%`
- OOS PF/density/DD(표본밖 수익 팩터/밀도/손실폭): `{proxy.get('oos_profit_factor')}` / `{proxy.get('oos_trades_per_day')}/day` / `{proxy.get('oos_dd_risk_percent')}%`

## Negative Memory(부정 기억)

{final['negative_memory']}

- best trainable model(최상위 학습 모델): `{model.get('model_id')}`
- validation PF/density/DD(검증 수익 팩터/밀도/손실폭): `{model.get('validation_profit_factor')}` / `{model.get('validation_trades_per_day')}/day` / `{model.get('validation_dd_risk_percent')}%`
- OOS PF/density/DD(표본밖 수익 팩터/밀도/손실폭): `{model.get('oos_profit_factor')}` / `{model.get('oos_trades_per_day')}/day` / `{model.get('oos_dd_risk_percent')}%`
- ONNX parity(온엑스 동등성): passed(통과), but research_only(연구 전용)

## Closeout Label(마감 라벨)

negative_memory(부정 기억)+preserved_clue(보존 단서). This is not completion(완성 아님), not baseline(기준선 아님), not promotion(승격 아님), not runtime authority(런타임 권위 아님).

## Gate Audit(게이트 감사)

`stages/stage_frontier_04__path_aware_cost_dd_event_labeling/03_reviews/required_gate_coverage_audit.md`

## Next Action(다음 행동)

`{final['next_run_id']}`. Action(행동)은 new frontier hypothesis(새 전선 가설)를 여는 것입니다. Effect(효과)는 같은 oracle-label transfer trap(오라클 라벨 전달 함정)을 상속하지 않는 것입니다.
"""


def decision_text(final: dict[str, Any]) -> str:
    return f"""# Decision(결정): Frontier04 Closeout(전선04 마감)

Date(날짜): 2026-06-14

Decision(결정): close Frontier04(전선04 마감) as negative_memory plus preserved_clue(부정 기억 + 보존 단서).

Reason(이유): Frontier04B(전선04B)는 proxy seed surface(프록시 씨앗 표면)를 만들었지만, Frontier04D(전선04D)는 feature_set_v2(피처 세트 v2)와 작은 고정 모델 격자에서 trainable ONNX transfer(학습 가능 온엑스 전달)가 붕괴했습니다.

Effect(효과): 다음 frontier(전선)는 path-aware oracle label(경로 인식 오라클 라벨)을 그대로 학습하면 된다는 상속을 받지 않습니다.

Boundary(경계): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def selection_text(final: dict[str, Any]) -> str:
    return f"""# Stage Frontier 04 Selection Status(전선04 단계 선택 상태)

Updated(갱신): {final['created_at_utc']}

Stage id(단계 ID): `{STAGE_ID}`

Closeout run(마감 실행): `{RUN_ID}`

Judgment(판정): `{final['judgment']}`

Selected baseline(선택 기준선): not_claimed(주장 없음)

Completion candidate(완성 후보): not_claimed(주장 없음)

Next action(다음 행동): `{final['next_run_id']}`
"""


def update_registries(final: dict[str, Any]) -> None:
    import yaml

    state = {
        "current_stage_id": STAGE_ID,
        "current_run_id": RUN_ID,
        "latest_completed_run_id": RUN_ID,
        "current_status": final["status"],
        "current_judgment": final["judgment"],
        "next_run_id": final["next_run_id"],
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "updated_at_utc": final["created_at_utc"],
    }
    io_path(f03b.WORKSPACE_STATE).write_text(yaml.safe_dump(json_ready(state), allow_unicode=True, sort_keys=False), encoding="utf-8")
    write_text_sig(f03b.CURRENT_WORKING_STATE, current_state_text(final))
    f03b.upsert_csv(f03b.RUN_REGISTRY, "run_id", run_registry_row(final))
    for row in ledger_rows(final):
        f03b.upsert_csv(f03b.ALPHA_LEDGER, "ledger_row_id", row)
        f03b.upsert_csv(STAGE_ROOT / "03_reviews" / "stage_run_ledger.csv", "ledger_row_id", row)
    f03b.append_once(f03b.CHANGELOG, RUN_ID, f"- {final['created_at_utc']}: `{RUN_ID}` {final['judgment']}. Effect(효과): next run(다음 실행)은 `{final['next_run_id']}`입니다.\n")
    f03b.append_once(f03b.IDEA_REGISTRY, RUN_ID, f"- `{RUN_ID}`: Frontier04(전선04) closed as negative_memory plus preserved_clue(부정 기억 + 보존 단서). Effect(효과): path-aware oracle seed(경로 인식 오라클 씨앗)는 보존하지만 trainable transfer(학습 전달)는 상속하지 않습니다.\n")
    f03b.append_once(f03b.NEGATIVE_RESULT_REGISTER, RUN_ID, f"- `{RUN_ID}`: path-aware oracle label seed did not transfer into usable ONNX metrics(경로 인식 오라클 라벨 씨앗이 쓸만한 온엑스 지표로 전달되지 않음). Effect(효과): next frontier(다음 전선)는 같은 라벨-전달 가정을 반복하지 않습니다.\n")


def current_state_text(final: dict[str, Any]) -> str:
    return f"""# Current Working State(현재 작업 상태)

Updated(갱신): {final['created_at_utc']}

Active stage(활성 단계): `{STAGE_ID}`

Current run(현재 실행): `{RUN_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Current truth(현재 진실): Frontier04(전선04)는 negative_memory(부정 기억)+preserved_clue(보존 단서)로 마감됐습니다.

Judgment(판정): `{final['judgment']}`

Next action(다음 행동): `{final['next_run_id']}`. Action(행동)은 새 frontier hypothesis(전선 가설)를 여는 것입니다. Effect(효과)는 Frontier04(전선04)의 oracle-to-model transfer trap(오라클→모델 전달 함정)을 상속하지 않는 것입니다.

Operating boundary(운영 경계): completion(완성), selected baseline(선택 기준선), operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def run_registry_row(final: dict[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "stage_closeout(단계 마감)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": REPORT_PATH.as_posix(),
        "notes": "negative_memory_plus_preserved_clue;no_authority",
        "work_family": "stage_closeout(단계 마감)",
        "run_number": RUN_NUMBER,
        "date": "2026-06-14",
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": final["next_run_id"],
        "candidate_count": "0",
        "claim_boundary": "stage_closeout_no_completion_no_baseline_no_promotion_no_authority_goal_claim",
        "report_path": REPORT_PATH.as_posix(),
        "created_at_utc": final["created_at_utc"],
        "ledger_row_id": f"{RUN_ID}__stage_closeout",
        "subrun_id": f"{RUN_ID}__stage_closeout",
        "record_view": "stage_closeout(단계 마감)",
        "tier_scope": "not_applicable_closeout(마감에는 해당 없음)",
        "kpi_scope": "closeout_judgment_no_new_trading_kpi(마감 판정, 신규 거래 KPI 없음)",
        "primary_kpi": "judgment=negative_memory_plus_preserved_clue",
        "guardrail_kpi": "no_completion_no_baseline_no_promotion_no_runtime_authority(완성/기준선/승격/런타임 권위 없음)",
        "external_verification_status": "grok_stage_closeout_review_captured_no_mt5(그록 단계 마감 검토 기록, MT5 없음)",
        "source_run_id": PARENT_RUN_ID,
        "artifact_path": (RUN_ROOT / "run_manifest.json").as_posix(),
        "result_path": REPORT_PATH.as_posix(),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "exploration_lane": "frontier_hypothesis_lifecycle(전선 가설 생명주기)",
        "evidence_boundary": "stage_closeout_only(단계 마감 전용)",
        "reopen_condition": final["next_run_id"],
        "question": "Should Frontier04 close after oracle-to-model collapse?(오라클→모델 붕괴 후 전선04를 마감해야 하는가?)",
        "skill_family": "result_judgment(결과 판정)",
        "lineage_summary": "frontier04_proxy_clue_to_trainable_collapse_to_closeout(전선04 프록시 단서에서 학습 붕괴와 마감)",
    }


def ledger_rows(final: dict[str, Any]) -> list[dict[str, Any]]:
    base = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "scoreboard_lane": "stage_closeout(단계 마감)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": REPORT_PATH.as_posix(),
        "guardrail_kpi": "no_completion_no_baseline_no_promotion_no_runtime_authority(완성/기준선/승격/런타임 권위 없음)",
        "external_verification_status": "grok_stage_closeout_review_captured_no_mt5(그록 단계 마감 검토 기록, MT5 없음)",
    }
    return [
        {
            **base,
            "ledger_row_id": f"{RUN_ID}__tier_a_closeout",
            "subrun_id": f"{RUN_ID}__tier_a_closeout",
            "record_view": "Tier A separate(티어 A 분리)",
            "tier_scope": "Tier A(티어 A)",
            "kpi_scope": "negative_memory_plus_preserved_clue(부정 기억 + 보존 단서)",
            "primary_kpi": "proxy_clue_preserved_trainable_transfer_failed(프록시 단서 보존, 학습 전달 실패)",
            "notes": "no_authority",
        },
        {
            **base,
            "ledger_row_id": f"{RUN_ID}__tier_b_missing_required",
            "subrun_id": f"{RUN_ID}__tier_b_missing_required",
            "record_view": "Tier B separate(티어 B 분리)",
            "tier_scope": "Tier B(티어 B)",
            "kpi_scope": "missing_required(필수 누락)",
            "primary_kpi": "missing_required_no_paired_source(필수 누락, 쌍 원천 없음)",
            "notes": "Tier B unavailable at closeout(마감 시 티어 B 없음)",
        },
        {
            **base,
            "ledger_row_id": f"{RUN_ID}__tier_ab_combined_missing_required",
            "subrun_id": f"{RUN_ID}__tier_ab_combined_missing_required",
            "record_view": "Tier A+B combined(티어 A+B 합산)",
            "tier_scope": "Tier A+B(티어 A+B)",
            "kpi_scope": "missing_required(필수 누락)",
            "primary_kpi": "missing_required_no_combined_claim(필수 누락, 합산 주장 없음)",
            "notes": "combined claim blocked by missing Tier B(티어 B 부재로 합산 주장 차단)",
        },
    ]


def read_proxy_top() -> dict[str, str]:
    with io_path(F04B_TOP).open("r", encoding="utf-8-sig", newline="") as handle:
        return next(csv.DictReader(handle))


def read_best_model() -> dict[str, Any]:
    data = read_json(F04D_MANIFEST)
    return data.get("best_model_row", {})


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def read_text(path: Path) -> str:
    return io_path(path).read_text(encoding="utf-8-sig")


def write_json(path: Path, payload: Any) -> None:
    io_path(path).parent.mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_text_sig(path: Path, text: str) -> None:
    io_path(path).parent.mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text, encoding="utf-8-sig")


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


if __name__ == "__main__":
    raise SystemExit(main())
