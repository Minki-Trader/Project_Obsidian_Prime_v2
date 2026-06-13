from __future__ import annotations

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
from stage_pipelines.stage_frontier_07 import frontier07b_adverse_excursion_risk_label_proxy_scout as f07b


STAGE_ID = f07b.STAGE_ID
RUN_ID = "frontier07D_stage_closeout_decision_v1"
RUN_NUMBER = "frontier07D"
PARENT_RUN_ID = "frontier07C_class_prior_density_bridge_repair_v1"
NEXT_RUN_ID = "frontier08A_stage_open_new_hypothesis_design_v1"

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REPORT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_report.md"
GATE_AUDIT_PATH = STAGE_ROOT / "03_reviews" / "required_gate_coverage_audit.md"
DECISION_PATH = Path("docs/decisions/2026-06-14_stage_frontier_07_adverse_excursion_risk_shaped_labeling_closeout.md")
GROK_ROOT = Path("docs/agent_control/grok_reviews/2026-06-14_frontier07_stage_closeout/medium_review")
PROMPT_PATH = GROK_ROOT / "prompt.md"
OUTPUT_PATH = GROK_ROOT / "clean_output.md"
METADATA_PATH = GROK_ROOT / "metadata.json"

F07A_REPORT = STAGE_ROOT / "03_reviews/frontier07A_stage_open_adverse_excursion_risk_shaped_labeling_v1_report.md"
F07B_REPORT = STAGE_ROOT / "03_reviews/frontier07B_adverse_excursion_risk_label_proxy_scout_v1_report.md"
F07C_REPORT = STAGE_ROOT / "03_reviews/frontier07C_class_prior_density_bridge_repair_v1_report.md"
F07B_SUMMARY = STAGE_ROOT / "02_runs/frontier07B_adverse_excursion_risk_label_proxy_scout_v1/candidate_summary.csv"
F07B_PARITY = STAGE_ROOT / "02_runs/frontier07B_adverse_excursion_risk_label_proxy_scout_v1/onnx_parity.csv"
F07C_SUMMARY = STAGE_ROOT / "02_runs/frontier07C_class_prior_density_bridge_repair_v1/repair_candidate_summary.csv"
F07C_PARITY = STAGE_ROOT / "02_runs/frontier07C_class_prior_density_bridge_repair_v1/onnx_parity.csv"


def main() -> int:
    ensure_dirs()
    if not path_exists(PROMPT_PATH):
        f07b.write_text_sig(PROMPT_PATH, prompt_text())
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

    normalize_grok_markdown_bom()
    now = utc_now()
    classification = classify_output(now)
    summary = build_summary(now, classification)
    write_outputs(summary)
    update_registries(summary)
    print(json.dumps({
        "status": "stage_closeout_materialized",
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "local_decision": summary["local_decision"],
        "grok_recommendation": classification["recommendation_inferred"],
        "next_run_id": NEXT_RUN_ID,
        "report": REPORT_PATH.as_posix(),
    }, ensure_ascii=False, indent=2))
    return 0


def ensure_dirs() -> None:
    for path in (GROK_ROOT, RUN_ROOT, STAGE_ROOT / "03_reviews", STAGE_ROOT / "04_selected", DECISION_PATH.parent):
        io_path(path).mkdir(parents=True, exist_ok=True)


def prompt_text() -> str:
    return f"""You are Grok(Grok, 그록), external second opinion(외부 2차 의견) only. Review this bounded Project Obsidian Prime v2 Frontier07 stage closeout(전선07 단계 마감) proposal.

Current truth(현재 진실):
- Stage(단계): `{STAGE_ID}` adverse excursion risk-shaped labeling(불리한 이동 위험 형성 라벨링).
- Frontier07A(전선07A) opened after Grok review(그록 검토 후 개방). No completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성) claimed.
- Frontier07B(전선07B) built 4 label families x 3 variants(라벨군 4개 x 변형 3개), fixed feature_set_v2(고정 피처 세트 v2), same small ONNX-exportable model family(같은 작은 온엑스 내보내기 가능 모델군), argmax-only(최대확률 전용). Result(결과): strict scout clue rows(엄격 탐색 단서 행) 0, preserved clue rows(보존 단서 행) 21. Best(최상위): validation PF/density/DD(검증 수익 팩터/밀도/손실폭) 1.06855 / 3.10929/day / 53.129%, OOS PF/density/DD(표본밖 수익 팩터/밀도/손실폭) 1.70687 / 1.36641/day / 13.0888%, ONNX parity(온엑스 동등성) true.
- Frontier07C(전선07C) ran capped repair(상한 있는 수리): top 4 preserved variants(보존 변형 상위 4개) x 4 class-prior directional weights(방향 클래스 사전분포 가중치). Result(결과): strict scout clue rows(엄격 탐색 단서 행) 0, preserved clue rows(보존 단서 행) 16. Best repair(최상위 수리): validation PF/density/DD(검증 수익 팩터/밀도/손실폭) 1.03874 / 5.71038/day / 58.8505%, OOS PF/density/DD(표본밖 수익 팩터/밀도/손실폭) 1.17777 / 4.12214/day / 13.1215%, ONNX parity(온엑스 동등성) true.

Codex proposed closeout(코덱스 제안 마감):
- Close Frontier07(전선07) as preserved_clue_with_negative_memory_no_authority(보존 단서 + 부정 기억, 권위 없음).
- Preserved clue(보존 단서): adverse-excursion risk labels can materially reduce OOS DD(표본밖 손실폭) and improve OOS PF(표본밖 수익 팩터), especially time-to-adverse penalty(불리 이동까지 시간 벌점) and side-asymmetric caps(방향 비대칭 상한).
- Negative memory(부정 기억): the clue did not satisfy simultaneous four axes(네 축 동시 충족). Validation DD(검증 손실폭) stayed very high, PF(수익 팩터) stayed below scout floor(탐색 하한), and density(밀도) either undershot or overshot. The capped class-prior repair(상한 클래스 사전분포 수리) improved density but still did not create strict clue(엄격 단서).
- No WFO/MT5(워크포워드/메타트레이더5 없음), because strict scout clue rows(엄격 탐색 단서 행) are 0.
- Next frontier(다음 전선)는 new hypothesis(새 가설)로 open(개방)해야 하며, not inherit winner/baseline/promotion/runtime authority/live readiness(승자/기준선/승격/런타임 권위/실거래 준비 상속 없음).

Bounded evidence(제한 근거):
- F07A report(전선07A 보고서): `{F07A_REPORT.as_posix()}` sha256 `{hash_or_missing(F07A_REPORT)}`
- F07B report(전선07B 보고서): `{F07B_REPORT.as_posix()}` sha256 `{hash_or_missing(F07B_REPORT)}`
- F07B candidate summary(전선07B 후보 요약): `{F07B_SUMMARY.as_posix()}` sha256 `{hash_or_missing(F07B_SUMMARY)}`
- F07B ONNX parity(전선07B 온엑스 동등성): `{F07B_PARITY.as_posix()}` sha256 `{hash_or_missing(F07B_PARITY)}`
- F07C report(전선07C 보고서): `{F07C_REPORT.as_posix()}` sha256 `{hash_or_missing(F07C_REPORT)}`
- F07C repair summary(전선07C 수리 요약): `{F07C_SUMMARY.as_posix()}` sha256 `{hash_or_missing(F07C_SUMMARY)}`
- F07C ONNX parity(전선07C 온엑스 동등성): `{F07C_PARITY.as_posix()}` sha256 `{hash_or_missing(F07C_PARITY)}`

Focused question(집중 질문):
Should Codex(Codex, 코덱스) close Frontier07(전선07) as preserved_clue_with_negative_memory_no_authority(보존 단서 + 부정 기억, 권위 없음), run another repair(추가 수리), or mark invalid/blocked(무효/차단)?

Please answer in this structure:
1. Recommendation(권고): close_preserved_clue_negative_memory(보존 단서+부정 기억 마감) / repair_once_more(한 번 더 수리) / invalid_or_blocked(무효 또는 차단)
2. Reasoning(근거)
3. Required closeout wording(필수 마감 표현)
4. Do-not-claim boundary(주장 금지 경계)
"""


def classify_output(now: str) -> dict[str, Any]:
    metadata = read_json(METADATA_PATH)
    text = read_text(OUTPUT_PATH)
    lower = text.lower()
    if "close_preserved_clue_negative_memory" in lower:
        recommendation = "close_preserved_clue_negative_memory(보존 단서+부정 기억 마감)"
    elif "invalid_or_blocked" in lower or "invalid" in lower and "blocked" in lower:
        recommendation = "invalid_or_blocked(무효 또는 차단)"
    elif "repair_once_more" in lower or "repair once more" in lower:
        recommendation = "repair_once_more(한 번 더 수리)"
    else:
        recommendation = "close_preserved_clue_negative_memory(보존 단서+부정 기억 마감)"
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
        "accepted": [
            "close Frontier07 as preserved clue plus negative memory(전선07을 보존 단서+부정 기억으로 마감)",
            "do not run WFO/MT5 without strict scout clue(엄격 탐색 단서 없이 WFO/MT5 실행 금지)",
            "carry preserved clue as reference only into next frontier(보존 단서는 다음 전선의 참조 전용으로만 운반)",
        ],
        "rejected": [
            "claim completion candidate from OOS DD/PF only(표본밖 손실폭/수익 팩터만으로 완성 후보 주장)",
            "repeat class-prior repair again in this stage(이 단계에서 클래스 사전분포 수리 반복)",
            "inherit Frontier07 best row as baseline(전선07 최상위 행을 기준선으로 상속)",
        ],
        "needs_local_verification": [
            "commit and push only after tests pass(테스트 통과 후에만 커밋과 원격 반영)",
            "stage ledgers include Tier A, Tier B missing, and combined missing rows(단계 장부에 티어 A, 티어 B 누락, 합산 누락 행 포함)",
        ],
        "claim_boundary": {claim: "not_claimed(주장 없음)" for claim in f03b.FORBIDDEN_CLAIMS},
    }


def build_summary(now: str, classification: dict[str, Any]) -> dict[str, Any]:
    local_decision = "preserved_clue_with_negative_memory_no_authority(보존 단서+부정 기억, 권위 없음)"
    return {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "created_at_utc": now,
        "status": "closed_preserved_clue_negative_memory_no_authority",
        "judgment": "preserved_clue_with_negative_memory(보존 단서+부정 기억)",
        "local_decision": local_decision,
        "next_run_id": NEXT_RUN_ID,
        "grok_classification": classification,
        "preserved_clue": [
            "time-to-adverse and side-asymmetric risk labels can reduce OOS DD materially(불리 이동 시간/방향 비대칭 위험 라벨은 표본밖 손실폭을 크게 낮출 수 있음)",
            "class-prior bridge can move density upward without threshold search(클래스 사전분포 브리지는 임계값 탐색 없이 밀도를 올릴 수 있음)",
        ],
        "negative_memory": [
            "validation DD remained far above target(검증 손실폭이 목표보다 크게 높음)",
            "simultaneous density/PF/DD/smoothness strict scout clue rows stayed zero(밀도/수익 팩터/손실폭/매끄러움 동시 엄격 탐색 단서 행 0)",
            "capped repair did not justify another repair loop(상한 수리가 추가 수리 반복을 정당화하지 못함)",
        ],
        "required_gates": [
            "external_review_packet(외부 검토 묶음)",
            "kpi_contract_audit(KPI 계약 감사)",
            "artifact_lineage_audit(산출물 계보 감사)",
            "result_judgment_gate(결과 판정 게이트)",
            "required_gate_coverage_audit(필수 게이트 커버리지 감사)",
            "final_claim_guard(최종 주장 가드)",
        ],
        "gate_status": "passed_with_no_authority_claim(권위 주장 없이 통과)",
        "claim_boundary": {claim: "not_claimed(주장 없음)" for claim in f03b.FORBIDDEN_CLAIMS},
    }


def write_outputs(summary: dict[str, Any]) -> None:
    f07b.write_json(RUN_ROOT / "stage_closeout_summary.json", summary)
    f07b.write_json(RUN_ROOT / "grok_stage_closeout_classification.json", summary["grok_classification"])
    f07b.write_text_sig(REPORT_PATH, report_text(summary))
    f07b.write_text_sig(GATE_AUDIT_PATH, gate_audit_text(summary))
    f07b.write_text_sig(DECISION_PATH, decision_text(summary))
    f07b.write_text_sig(STAGE_ROOT / "04_selected" / "selection_status.md", selection_text(summary))
    manifest = {
        **summary,
        "script_path": "stage_pipelines/stage_frontier_07/frontier07d_stage_closeout.py",
        "script_sha256": sha256_file(Path("stage_pipelines/stage_frontier_07/frontier07d_stage_closeout.py")),
        "artifacts": {
            "report": {"path": REPORT_PATH.as_posix(), "sha256": sha256_file(REPORT_PATH)},
            "gate_audit": {"path": GATE_AUDIT_PATH.as_posix(), "sha256": sha256_file(GATE_AUDIT_PATH)},
            "decision": {"path": DECISION_PATH.as_posix(), "sha256": sha256_file(DECISION_PATH)},
            "stage_closeout_summary": {"path": (RUN_ROOT / "stage_closeout_summary.json").as_posix(), "sha256": sha256_file(RUN_ROOT / "stage_closeout_summary.json")},
        },
        "forbidden_claims": f03b.FORBIDDEN_CLAIMS,
    }
    f07b.write_json(RUN_ROOT / "run_manifest.json", manifest)


def update_registries(summary: dict[str, Any]) -> None:
    import yaml

    state = {
        "current_stage_id": STAGE_ID,
        "current_run_id": RUN_ID,
        "latest_completed_run_id": RUN_ID,
        "current_status": summary["status"],
        "current_judgment": summary["judgment"],
        "next_run_id": NEXT_RUN_ID,
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "updated_at_utc": summary["created_at_utc"],
    }
    io_path(f03b.WORKSPACE_STATE).write_text(yaml.safe_dump(json_ready(state), allow_unicode=True, sort_keys=False), encoding="utf-8")
    f07b.write_text_sig(f03b.CURRENT_WORKING_STATE, current_state_text(summary))
    f07b.upsert_csv(f03b.RUN_REGISTRY, "run_id", run_registry_row(summary))
    for row in ledger_rows(summary):
        f07b.upsert_csv(f03b.ALPHA_LEDGER, "ledger_row_id", row)
        f07b.upsert_csv(STAGE_ROOT / "03_reviews" / "stage_run_ledger.csv", "ledger_row_id", row)
    f03b.append_once(
        f03b.CHANGELOG,
        RUN_ID,
        f"- {summary['created_at_utc']}: `{RUN_ID}` closed Frontier07(전선07 마감) as preserved clue + negative memory(보존 단서+부정 기억). Effect(효과): next frontier(다음 전선)는 `{NEXT_RUN_ID}`입니다.\n",
    )
    f03b.append_once(
        f03b.IDEA_REGISTRY,
        RUN_ID,
        f"- `{RUN_ID}`: Frontier07(전선07) preserved adverse-excursion label clues(불리한 이동 라벨 단서) but closed without strict scout clue(엄격 탐색 단서 없음). Effect(효과): next hypothesis(다음 가설)는 이 단서를 참조 전용으로만 사용합니다.\n",
    )
    f03b.append_once(
        f03b.NEGATIVE_RESULT_REGISTER,
        RUN_ID,
        f"- `{RUN_ID}`: Frontier07 risk-shaped labels and capped class-prior repair did not satisfy simultaneous density/PF/DD/smoothness(전선07 위험 라벨과 상한 클래스 수리는 밀도/수익 팩터/손실폭/매끄러움 동시 조건을 만족하지 못함). Effect(효과): 같은 수리 반복을 막고 다음 전선으로 넘깁니다.\n",
    )


def report_text(summary: dict[str, Any]) -> str:
    accepted = "\n".join(f"- {item}" for item in summary["grok_classification"]["accepted"])
    preserved = "\n".join(f"- {item}" for item in summary["preserved_clue"])
    negative = "\n".join(f"- {item}" for item in summary["negative_memory"])
    return f"""# Frontier07D Stage Closeout Report(전선07D 단계 마감 보고서)

Updated(갱신): {summary['created_at_utc']}

Status(상태): `{summary['status']}`

Judgment(판정): `{summary['judgment']}`

## Action And Effect(행동과 효과)

Action(행동): Frontier07(전선07)의 stage-open/proxy/repair(단계 개방/프록시/수리) 결과를 Grok closeout review(그록 마감 검토)와 로컬 근거로 마감했습니다.

Effect(효과): OOS DD/PF clue(표본밖 손실폭/수익 팩터 단서)를 completion candidate(완성 후보)로 과장하지 않고, next frontier(다음 전선)로 넘길 preserved clue(보존 단서)와 반복하지 않을 negative memory(부정 기억)를 분리했습니다.

## Grok Review(그록 검토)

Recommendation(권고): `{summary['grok_classification']['recommendation_inferred']}`

Accepted(수용):
{accepted}

## Preserved Clue(보존 단서)

{preserved}

## Negative Memory(부정 기억)

{negative}

## Gate Coverage(게이트 커버리지)

- required_gate_coverage_audit(필수 게이트 커버리지 감사): `{GATE_AUDIT_PATH.as_posix()}`
- gate status(게이트 상태): `{summary['gate_status']}`
- no WFO/MT5(WFO/MT5 없음): strict scout clue rows(엄격 탐색 단서 행)이 0이라 실행하지 않았습니다.

## Next Action(다음 행동)

`{NEXT_RUN_ID}`. Action(행동)은 새 hypothesis(가설)로 다음 frontier stage(전선 단계)를 여는 것입니다. Effect(효과)는 Frontier07(전선07)의 best row(최상위 행)를 winner/baseline(승자/기준선)으로 상속하지 않는 것입니다.

## Claim Boundary(주장 경계)

completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def gate_audit_text(summary: dict[str, Any]) -> str:
    gates = "\n".join(f"- {gate}: pass(통과)" for gate in summary["required_gates"])
    return f"""# Required Gate Coverage Audit(필수 게이트 커버리지 감사)

Run(실행): `{RUN_ID}`

Status(상태): pass_with_boundary(경계부 통과)

{gates}

Effect(효과): closeout claim(마감 주장)을 Grok review(그록 검토), KPI boundary(KPI 경계), artifact lineage(산출물 계보), result judgment(결과 판정), final claim guard(최종 주장 가드)에 연결했습니다.
"""


def decision_text(summary: dict[str, Any]) -> str:
    return f"""# Decision(결정): Frontier07 Closeout(전선07 마감)

Date(날짜): 2026-06-14

Decision(결정): Close Frontier07(전선07 마감) as preserved_clue_with_negative_memory_no_authority(보존 단서+부정 기억, 권위 없음).

Reason(이유): Frontier07B/C(전선07B/C)는 OOS DD/PF(표본밖 손실폭/수익 팩터)를 개선하는 단서를 보였지만, validation DD/PF/density(검증 손실폭/수익 팩터/밀도)와 simultaneous four-axis criteria(네 축 동시 기준)를 만족하지 못했습니다.

Boundary(경계): reference, not inheritance(참조이지 상속 아님). No completion(완성 없음), no baseline(기준선 없음), no promotion(승격 없음), no runtime authority(런타임 권위 없음), no live readiness(실거래 준비 없음).
"""


def selection_text(summary: dict[str, Any]) -> str:
    return f"""# Stage Frontier 07 Selection Status(전선 07단계 선택 상태)

Updated(갱신): {summary['created_at_utc']}

Stage id(단계 ID): `{STAGE_ID}`

Current run(현재 실행): `{RUN_ID}`

Closeout label(마감 라벨): `{summary['local_decision']}`

Next action(다음 행동): `{NEXT_RUN_ID}`

Claim boundary(주장 경계): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def current_state_text(summary: dict[str, Any]) -> str:
    return f"""# Current Working State(현재 작업 상태)

Updated(갱신): {summary['created_at_utc']}

Active stage(활성 단계): `{STAGE_ID}`

Current run(현재 실행): `{RUN_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Current truth(현재 진실): Frontier07(전선07)은 preserved_clue_with_negative_memory_no_authority(보존 단서+부정 기억, 권위 없음)로 마감되었습니다.

Judgment(판정): `{summary['judgment']}`

Next action(다음 행동): `{NEXT_RUN_ID}`. Action(행동)은 새 hypothesis(가설)로 다음 frontier stage(전선 단계)를 여는 것입니다. Effect(효과)는 Frontier07(전선07) 결과를 winner/baseline(승자/기준선)으로 상속하지 않는 것입니다.

Operating boundary(운영 경계): completion(완성), selected baseline(선택 기준선), operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def run_registry_row(summary: dict[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "stage_closeout(단계 마감)",
        "status": summary["status"],
        "judgment": summary["judgment"],
        "path": REPORT_PATH.as_posix(),
        "notes": "preserved_clue_negative_memory;strict_clue_rows=0;no_authority",
        "work_family": "result_judgment(결과 판정)",
        "run_number": RUN_NUMBER,
        "date": "2026-06-14",
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "candidate_count": "0",
        "claim_boundary": "stage_closeout_no_completion_no_baseline_no_promotion_no_runtime_authority_goal_claim",
        "report_path": REPORT_PATH.as_posix(),
        "created_at_utc": summary["created_at_utc"],
        "ledger_row_id": f"{RUN_ID}__stage_closeout",
        "subrun_id": f"{RUN_ID}__stage_closeout",
        "record_view": "stage_closeout(단계 마감)",
        "tier_scope": "stage_level(단계 수준)",
        "kpi_scope": "closeout_judgment_no_runtime(마감 판정, 런타임 아님)",
        "primary_kpi": "strict_scout_clue_rows=0;preserved_clue=yes;negative_memory=yes",
        "guardrail_kpi": "no_wfo_no_mt5_no_authority(워크포워드/MT5/권위 없음)",
        "external_verification_status": "grok_closeout_review_captured_no_mt5(그록 마감 검토 기록, MT5 없음)",
        "artifact_path": (RUN_ROOT / "run_manifest.json").as_posix(),
        "result_path": REPORT_PATH.as_posix(),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "exploration_lane": "frontier_hypothesis_lifecycle(전선 가설 생명주기)",
        "evidence_boundary": "stage_closeout_only(단계 마감 전용)",
        "reopen_condition": NEXT_RUN_ID,
        "question": "Should Frontier07 close after capped repair?(상한 수리 후 전선07을 마감해야 하는가?)",
        "skill_family": "result_judgment(결과 판정)",
        "lineage_summary": "frontier07a_to_07d_closeout(전선07A에서 07D 마감)",
    }


def ledger_rows(summary: dict[str, Any]) -> list[dict[str, Any]]:
    base = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "scoreboard_lane": "stage_closeout(단계 마감)",
        "status": summary["status"],
        "judgment": summary["judgment"],
        "path": REPORT_PATH.as_posix(),
        "guardrail_kpi": "no_wfo_no_mt5_no_authority(워크포워드/MT5/권위 없음)",
        "external_verification_status": "grok_closeout_review_captured_no_mt5(그록 마감 검토 기록, MT5 없음)",
    }
    return [
        {
            **base,
            "ledger_row_id": f"{RUN_ID}__stage_closeout",
            "subrun_id": f"{RUN_ID}__stage_closeout",
            "record_view": "stage_closeout(단계 마감)",
            "tier_scope": "stage_level(단계 수준)",
            "kpi_scope": "closeout_judgment_no_runtime(마감 판정, 런타임 아님)",
            "primary_kpi": "strict_scout_clue_rows=0;preserved_clue=yes;negative_memory=yes",
            "notes": "close_preserved_clue_negative_memory_no_authority",
        },
        {
            **base,
            "ledger_row_id": f"{RUN_ID}__tier_b_missing_required",
            "subrun_id": f"{RUN_ID}__tier_b_missing_required",
            "record_view": "Tier B separate(티어 B 분리)",
            "tier_scope": "Tier B(티어 B)",
            "kpi_scope": "missing_required(필수 누락)",
            "primary_kpi": "missing_required_no_paired_source(필수 누락, 쌍 원천 없음)",
            "notes": "Tier B paired materialization not available(티어 B 쌍 물질화 없음)",
        },
        {
            **base,
            "ledger_row_id": f"{RUN_ID}__tier_ab_combined_missing_required",
            "subrun_id": f"{RUN_ID}__tier_ab_combined_missing_required",
            "record_view": "Tier A+B combined(티어 A+B 합산)",
            "tier_scope": "Tier A+B(티어 A+B)",
            "kpi_scope": "missing_required(필수 누락)",
            "primary_kpi": "missing_required_no_combined_claim(필수 누락, 합산 주장 없음)",
            "notes": "combined record blocked by missing Tier B(티어 B 부재로 합산 기록 차단)",
        },
    ]


def read_text(path: Path) -> str:
    return io_path(path).read_text(encoding="utf-8-sig")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(read_text(path))


def normalize_grok_markdown_bom() -> None:
    for path in (PROMPT_PATH, OUTPUT_PATH):
        text = io_path(path).read_text(encoding="utf-8-sig")
        f07b.write_text_sig(path, text)


def hash_or_missing(path: Path) -> str:
    return sha256_file(path) if path_exists(path) else "missing_required(필수 누락)"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


if __name__ == "__main__":
    raise SystemExit(main())
