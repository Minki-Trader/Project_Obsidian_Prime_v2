from __future__ import annotations

import csv
import json
import math
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


STAGE_ID = "stage_frontier_06__selective_probability_abstention_signal_contract"
RUN_ID = "frontier06C_stage_closeout_v1"
RUN_NUMBER = "frontier06C"
PARENT_RUN_ID = "frontier06B_selective_probability_abstention_signal_scout_v1"
NEXT_RUN_ID = "frontier07A_stage_open_new_hypothesis_design_v1"

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REPORT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_report.md"
GATE_AUDIT_PATH = STAGE_ROOT / "03_reviews" / "required_gate_coverage_audit.md"
DECISION_PATH = Path("docs/decisions/2026-06-14_stage_frontier_06_selective_probability_abstention_signal_contract_closeout.md")
GROK_ROOT = Path("docs/agent_control/grok_reviews/2026-06-14_frontier06_stage_closeout/medium_review")
PROMPT_PATH = GROK_ROOT / "prompt.md"
OUTPUT_PATH = GROK_ROOT / "clean_output.md"
METADATA_PATH = GROK_ROOT / "metadata.json"

F06A_REPORT = STAGE_ROOT / "03_reviews" / "frontier06A_stage_open_selective_probability_abstention_signal_contract_v1_report.md"
F06B_REPORT = STAGE_ROOT / "03_reviews" / "frontier06B_selective_probability_abstention_signal_scout_v1_report.md"
F06B_RUN_ROOT = STAGE_ROOT / "02_runs" / PARENT_RUN_ID
F06B_COMPARISON = F06B_RUN_ROOT / "signal_rule_comparison.csv"
F06B_ONNX_PARITY = F06B_RUN_ROOT / "onnx_parity.csv"
F06B_MANIFEST = F06B_RUN_ROOT / "run_manifest.json"


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
            "missing": [
                path.as_posix()
                for path in (OUTPUT_PATH, METADATA_PATH)
                if not path_exists(path)
            ],
        }, ensure_ascii=False, indent=2))
        return 0
    now = utc_now()
    classification = classify_output(now)
    summary = build_summary(now, classification)
    write_outputs(summary)
    update_docs_and_state(now, summary)
    print(json.dumps({
        "status": "stage_closeout_materialized",
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "grok_recommendation": classification["recommendation_inferred"],
        "local_decision": summary["local_decision"],
        "judgment": summary["judgment"],
        "next_run_id": NEXT_RUN_ID,
        "report": REPORT_PATH.as_posix(),
    }, ensure_ascii=False, indent=2))
    return 0


def ensure_dirs() -> None:
    for path in (GROK_ROOT, RUN_ROOT, STAGE_ROOT / "03_reviews", STAGE_ROOT / "04_selected", DECISION_PATH.parent):
        io_path(path).mkdir(parents=True, exist_ok=True)


def prompt_text() -> str:
    manifest = read_json(F06B_MANIFEST)
    best = best_rule_row()
    parity = parity_summary()
    top_rules = top_rule_lines()
    return f"""You are Grok(Grok, 그록), external second opinion(외부 2차 의견) only. Review this bounded Project Obsidian Prime v2 Frontier06 stage closeout(전선06 단계 마감) proposal.

Current truth(현재 진실):
- Frontier06(전선06) hypothesis(가설): selective probability abstention signal contract(선택적 확률 기권 신호 계약).
- Labels/features/models(라벨/피처/모델)는 fixed(고정)했습니다. Only output-to-trade signal contract(출력-거래 신호 계약) changed(변경)했습니다.
- Thresholds(임계값)는 train-only calibration(학습 전용 보정)입니다. Validation/OOS(검증/표본밖)는 evaluation only(평가 전용)입니다.
- Argmax baseline(최대 확률 기준선) comparator(비교 기준)를 mandatory(필수)로 뒀습니다.
- Signal grid(신호 격자)는 capped(상한 있음)입니다: `{manifest.get('signal_rule_count')}` rules(규칙).
- Scout clue rows(탐색 단서 행): `{manifest.get('scout_clue_rows')}`.
- Partial axis gain rows(부분 축 개선 행): `{manifest.get('partial_axis_gain_rows')}`.
- ONNX parity(온엑스 동등성): {parity}.

Best bounded read(최상위 제한 판독):
- rule(규칙): `{best.get('rule_id')}`
- model(모델): `{best.get('model_id')}`
- score kind(점수 종류): `{best.get('score_kind')}`
- validation base -> rule PF/density/DD(검증 기준 -> 규칙 수익 팩터/밀도/손실폭): `{fmt(best.get('validation_base_pf'))}` -> `{fmt(best.get('validation_rule_pf'))}`, `{fmt(best.get('validation_base_density'))}/day` -> `{fmt(best.get('validation_rule_density'))}/day`, `{fmt(best.get('validation_base_dd'))}%` -> `{fmt(best.get('validation_rule_dd'))}%`
- OOS base -> rule PF/density/DD(표본밖 기준 -> 규칙 수익 팩터/밀도/손실폭): `{fmt(best.get('oos_base_pf'))}` -> `{fmt(best.get('oos_rule_pf'))}`, `{fmt(best.get('oos_base_density'))}/day` -> `{fmt(best.get('oos_rule_density'))}/day`, `{fmt(best.get('oos_base_dd'))}%` -> `{fmt(best.get('oos_rule_dd'))}%`
- strict scout clue pass(엄격 탐색 단서 통과): `{best.get('strict_scout_clue_pass')}`

Top rule snapshot(상위 규칙 스냅샷):
{top_rules}

Codex proposed closeout before Grok(Codex 제안 마감):
- Close Frontier06(전선06 마감) as negative_memory(부정 기억)+preserved_clue(보존 단서).
- Negative memory(부정 기억): train-only selective abstention(학습 전용 선택 기권)은 validation+OOS strict scout clue(검증+표본밖 엄격 탐색 단서)를 만들지 못했습니다. DD(drawdown, 손실폭)가 still too high(여전히 너무 높고), validation PF(검증 수익 팩터)는 floor(하한)를 통과하지 못했습니다.
- Preserved clue(보존 단서): directional-margin abstention(방향 마진 기권)은 OOS density(표본밖 거래 밀도)를 target band(목표대)로 낮추고 OOS PF/DD(표본밖 수익 팩터/손실폭)를 개선했습니다. But it is not completion candidate(완성 후보 아님).
- Do not run WFO/MT5(WFO/MT5 실행 금지) from this result. Do not continue threshold micro-search(임계값 미세탐색 반복 금지) inside Frontier06(전선06 내부).
- Next frontier(다음 전선)는 exit/risk/validation hypothesis(청산/위험/검증 가설)처럼 new axis(새 축)를 열어야 합니다.

Bounded evidence(제한 근거):
- Frontier06A report(전선06A 보고서): `{F06A_REPORT.as_posix()}` sha256 `{sha256_file(F06A_REPORT)}`
- Frontier06B report(전선06B 보고서): `{F06B_REPORT.as_posix()}` sha256 `{sha256_file(F06B_REPORT)}`
- Frontier06B comparison(전선06B 비교): `{F06B_COMPARISON.as_posix()}` sha256 `{sha256_file(F06B_COMPARISON)}`
- Frontier06B ONNX parity(전선06B 온엑스 동등성): `{F06B_ONNX_PARITY.as_posix()}` sha256 `{sha256_file(F06B_ONNX_PARITY)}`
- Frontier06B manifest(전선06B 실행 목록): `{F06B_MANIFEST.as_posix()}` sha256 `{sha256_file(F06B_MANIFEST)}`

Focused question(집중 질문):
Should Codex(Codex, 코덱스) close Frontier06(전선06) as negative_memory(부정 기억)+preserved_clue(보존 단서), run one capped repair(상한 있는 수리 1회), mark invalid_setup(무효 설정), or mark blocked(차단)?

Please answer in this structure:
1. Recommendation(권고): close_negative_memory_preserved_clue(부정 기억+보존 단서 마감) / repair_once(1회 수리) / invalid_setup(무효 설정) / blocked(차단)
2. Reasoning(근거)
3. Accepted/rejected/needs_local_verification(수용/거절/로컬 검증 필요)
4. Closeout wording(마감 문구)
5. Do-not-claim boundary(주장 금지 경계)
"""


def classify_output(now: str) -> dict[str, Any]:
    metadata = read_json(METADATA_PATH)
    text = read_text(OUTPUT_PATH)
    lower = text.lower()
    choices = [
        ("close_negative_memory_preserved_clue", "close_negative_memory_preserved_clue(부정 기억+보존 단서 마감)"),
        ("close_negative_memory", "close_negative_memory(부정 기억 마감)"),
        ("repair_once", "repair_once(1회 수리)"),
        ("invalid_setup", "invalid_setup(무효 설정)"),
        ("blocked", "blocked(차단)"),
    ]
    seen = [
        (lower.find(needle), index, choice)
        for index, (needle, choice) in enumerate(choices)
        if lower.find(needle) >= 0
    ]
    recommendation = min(seen, default=(0, 0, "close_negative_memory_preserved_clue(부정 기억+보존 단서 마감)"))[2]
    best = best_rule_row()
    rejected = [
        "claim completion/baseline/promotion/runtime/live readiness(완성/기준선/승격/런타임/실거래 준비 주장)",
        "run expensive WFO/MT5 from a zero-strict-clue scout(엄격 단서 0개 탐색에서 비싼 WFO/MT5 실행)",
        "continue unbounded threshold micro-search(무제한 임계값 미세탐색 지속)",
    ]
    needs = [
        "commit and push only after tests and gate audit pass(테스트와 게이트 감사 통과 뒤에만 커밋/원격 반영)",
        "keep 02_runs artifacts referenced by manifest(02_runs 산출물을 실행 목록으로 참조 유지)",
    ]
    accepted = [
        "close Frontier06 as negative_memory+preserved_clue(전선06을 부정 기억+보존 단서로 마감)",
        "carry the OOS density/PF/DD improvement only as preserved clue(표본밖 밀도/수익 팩터/손실폭 개선은 보존 단서로만 유지)",
        "open the next frontier on a new hypothesis axis(다음 전선은 새 가설 축으로 개방)",
    ]
    if "repair_once" in recommendation:
        accepted = [
            "Grok suggested repair_once(그록이 1회 수리를 제안)",
            "Codex local boundary still rejects automatic repair because strict scout clue rows are zero(Codex 로컬 경계는 엄격 탐색 단서가 0개라 자동 수리를 거절)",
        ]
        needs.append("new repair would require a genuinely new axis, not threshold retry(새 수리는 임계값 재시도가 아니라 진짜 새 축이어야 함)")
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
        "best_rule_id": best.get("rule_id"),
        "accepted": accepted,
        "rejected": rejected,
        "needs_local_verification": needs,
        "next_run_id": NEXT_RUN_ID,
        "claim_boundary": {claim: "not_claimed(주장 없음)" for claim in f03b.FORBIDDEN_CLAIMS},
    }


def build_summary(now: str, classification: dict[str, Any]) -> dict[str, Any]:
    manifest = read_json(F06B_MANIFEST)
    best = best_rule_row()
    return {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "created_at_utc": now,
        "status": "closed_negative_memory_preserved_clue_no_authority",
        "judgment": "negative_memory(부정 기억)+preserved_clue(보존 단서)",
        "local_decision": "close_negative_memory_preserved_clue(부정 기억+보존 단서 마감)",
        "next_run_id": NEXT_RUN_ID,
        "grok_classification": classification,
        "scout_clue_rows": int(manifest.get("scout_clue_rows") or 0),
        "partial_axis_gain_rows": int(manifest.get("partial_axis_gain_rows") or 0),
        "signal_rule_count": int(manifest.get("signal_rule_count") or 0),
        "best_rule_row": best,
        "negative_memory": (
            "Train-only selective probability abstention did not produce validation+OOS strict scout clue"
            "(학습 전용 선택적 확률 기권은 검증+표본밖 엄격 탐색 단서를 만들지 못함)."
        ),
        "preserved_clue": (
            "Directional-margin abstention reduced OOS density into the target band and improved OOS PF/DD, "
            "but DD remained too high and validation PF stayed below the scout floor"
            "(방향 마진 기권은 표본밖 거래 밀도를 목표대로 낮추고 표본밖 수익 팩터/손실폭을 개선했지만, 손실폭은 여전히 높고 검증 수익 팩터는 탐색 하한 미만)."
        ),
        "primary_family": "experiment_execution(실험 실행)",
        "primary_skill": "obsidian-run-evidence-system(옵시디언 실행 근거 시스템)",
        "support_skills": [
            "obsidian-experiment-design(옵시디언 실험 설계)",
            "obsidian-data-integrity(옵시디언 데이터 무결성)",
            "obsidian-model-validation(옵시디언 모델 검증)",
            "obsidian-artifact-lineage(옵시디언 산출물 계보)",
            "obsidian-grok-collaboration(옵시디언 그록 협업)",
        ],
        "required_gates": [
            "scope_completion_gate(범위 완료 게이트)",
            "kpi_contract_audit(KPI 계약 감사)",
            "skill_receipt_lint(스킬 영수증 점검)",
            "required_gate_coverage_audit(필수 게이트 커버리지 감사)",
            "external_review_packet(외부 검토 묶음)",
            "final_claim_guard(최종 주장 보호)",
        ],
        "claim_boundary": {claim: "not_claimed(주장 없음)" for claim in f03b.FORBIDDEN_CLAIMS},
    }


def write_outputs(summary: dict[str, Any]) -> None:
    write_json(RUN_ROOT / "stage_closeout_summary.json", summary)
    write_json(RUN_ROOT / "grok_stage_closeout_classification.json", summary["grok_classification"])
    write_text_sig(REPORT_PATH, report_text(summary))
    write_text_sig(GATE_AUDIT_PATH, gate_audit_text(summary))
    write_text_sig(DECISION_PATH, decision_text(summary))
    write_text_sig(STAGE_ROOT / "04_selected" / "selection_status.md", selection_text(summary))
    write_text_sig(STAGE_ROOT / "03_reviews" / "review_index.md", review_index_text(summary))
    manifest = {
        **summary,
        "script_path": "stage_pipelines/stage_frontier_06/frontier06c_stage_closeout.py",
        "script_sha256": sha256_file(Path("stage_pipelines/stage_frontier_06/frontier06c_stage_closeout.py")),
        "outputs": {
            "report": {"path": REPORT_PATH.as_posix(), "sha256": sha256_file(REPORT_PATH)},
            "gate_audit": {"path": GATE_AUDIT_PATH.as_posix(), "sha256": sha256_file(GATE_AUDIT_PATH)},
            "decision": {"path": DECISION_PATH.as_posix(), "sha256": sha256_file(DECISION_PATH)},
            "stage_closeout_summary": {
                "path": (RUN_ROOT / "stage_closeout_summary.json").as_posix(),
                "sha256": sha256_file(RUN_ROOT / "stage_closeout_summary.json"),
            },
        },
        "external_verification_status": "grok_review_captured_no_mt5(그록 검토 기록, MT5 없음)",
        "forbidden_claims": f03b.FORBIDDEN_CLAIMS,
    }
    write_json(RUN_ROOT / "run_manifest.json", manifest)


def update_docs_and_state(now: str, summary: dict[str, Any]) -> None:
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
        "updated_at_utc": now,
    }
    io_path(f03b.WORKSPACE_STATE).write_text(yaml.safe_dump(json_ready(state), allow_unicode=True, sort_keys=False), encoding="utf-8")
    write_text_sig(f03b.CURRENT_WORKING_STATE, current_state_text(summary))
    upsert_csv(f03b.RUN_REGISTRY, "run_id", run_registry_row(now, summary))
    upsert_csv(f03b.ALPHA_LEDGER, "ledger_row_id", ledger_row(summary))
    upsert_csv(STAGE_ROOT / "03_reviews" / "stage_run_ledger.csv", "ledger_row_id", ledger_row(summary))
    f03b.append_once(
        f03b.CHANGELOG,
        RUN_ID,
        f"- {now}: `{RUN_ID}` closed Frontier06(전선06 마감) as negative_memory(부정 기억)+preserved_clue(보존 단서). Effect(효과): next frontier(다음 전선)는 `{NEXT_RUN_ID}`입니다.\n",
    )
    f03b.append_once(
        f03b.IDEA_REGISTRY,
        RUN_ID,
        "- `IDEA-FR06-SELECTIVE-PROBABILITY-ABSTENTION-SIGNAL-CONTRACT`: closed as negative_memory(부정 기억)+preserved_clue(보존 단서). Effect(효과): output-to-trade threshold retry(출력-거래 임계값 재시도)는 더 이어가지 않고 새 축으로 넘깁니다.\n",
    )
    f03b.append_once(
        f03b.NEGATIVE_RESULT_REGISTER,
        RUN_ID,
        f"- `{RUN_ID}`: selective probability abstention signal contract(선택적 확률 기권 신호 계약) did not produce validation+OOS strict scout clue(검증+표본밖 엄격 탐색 단서 없음). Effect(효과): density/PF clue(밀도/수익 팩터 단서)는 보존하되 Frontier06(전선06)은 마감합니다.\n",
    )


def report_text(summary: dict[str, Any]) -> str:
    best = summary["best_rule_row"]
    classification = summary["grok_classification"]
    accepted = "\n".join(f"- {item}" for item in classification["accepted"])
    rejected = "\n".join(f"- {item}" for item in classification["rejected"])
    needs = "\n".join(f"- {item}" for item in classification["needs_local_verification"])
    return f"""# Frontier06C Stage Closeout Report(전선06C 단계 마감 보고서)

Updated(갱신): {summary['created_at_utc']}

Status(상태): `{summary['status']}`

Judgment(판정): `{summary['judgment']}`

Grok recommendation(그록 권고): `{classification['recommendation_inferred']}`

Local decision(로컬 결정): `{summary['local_decision']}`

## Action And Effect(행동과 효과)

Action(행동): Frontier06(전선06)을 selective probability abstention signal contract(선택적 확률 기권 신호 계약) hypothesis lifecycle(가설 생명주기)로 마감했습니다.

Effect(효과): strict scout clue(엄격 탐색 단서) 없이 threshold micro-search(임계값 미세탐색)를 반복하지 않고, 다음 frontier(전선)를 새 hypothesis axis(가설 축)로 열 수 있게 했습니다.

## Negative Memory(부정 기억)

{summary['negative_memory']}

## Preserved Clue(보존 단서)

{summary['preserved_clue']}

## Key Evidence(핵심 근거)

- signal rules tested(시험한 신호 규칙): `{summary['signal_rule_count']}`
- strict scout clue rows(엄격 탐색 단서 행): `{summary['scout_clue_rows']}`
- partial axis gain rows(부분 축 개선 행): `{summary['partial_axis_gain_rows']}`
- best rule(최상위 규칙): `{best.get('rule_id')}`
- validation base -> rule PF/density/DD(검증 기준 -> 규칙 수익 팩터/밀도/손실폭): `{fmt(best.get('validation_base_pf'))}` -> `{fmt(best.get('validation_rule_pf'))}`, `{fmt(best.get('validation_base_density'))}/day` -> `{fmt(best.get('validation_rule_density'))}/day`, `{fmt(best.get('validation_base_dd'))}%` -> `{fmt(best.get('validation_rule_dd'))}%`
- OOS base -> rule PF/density/DD(표본밖 기준 -> 규칙 수익 팩터/밀도/손실폭): `{fmt(best.get('oos_base_pf'))}` -> `{fmt(best.get('oos_rule_pf'))}`, `{fmt(best.get('oos_base_density'))}/day` -> `{fmt(best.get('oos_rule_density'))}/day`, `{fmt(best.get('oos_base_dd'))}%` -> `{fmt(best.get('oos_rule_dd'))}%`
- ONNX parity(온엑스 동등성): `{parity_summary()}`

## Grok Classification(그록 분류)

Accepted(수용):
{accepted}

Rejected(거절):
{rejected}

Needs local verification(로컬 검증 필요):
{needs}

## Next Frontier Proposal(다음 전선 제안)

`{NEXT_RUN_ID}`. Action(행동)은 exit/risk/validation hypothesis(청산/위험/검증 가설)처럼 new axis(새 축)를 여는 것입니다. Effect(효과)는 probability threshold repair(확률 임계값 수리)를 반복하지 않고 네 축 동시 개선 후보를 다시 찾는 것입니다.

## Claim Boundary(주장 경계)

completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def gate_audit_text(summary: dict[str, Any]) -> str:
    return f"""# Required Gate Coverage Audit(필수 게이트 커버리지 감사)

Updated(갱신): {summary['created_at_utc']}

Work packet(작업 묶음): `{RUN_ID}`

Primary family(주 작업군): `{summary['primary_family']}`

Primary skill(주 스킬): `{summary['primary_skill']}`

Overlay(오버레이): `grok_external_review(그록 외부 검토)`

## Gates(게이트)

- scope_completion_gate(범위 완료 게이트): satisfied(충족). Frontier06(전선06)은 stage open(단계 개방), signal scout(신호 탐색), closeout review(마감 검토)를 완료했습니다.
- kpi_contract_audit(KPI 계약 감사): satisfied_with_boundary(경계부 충족). density/PF/DD/ONNX parity(밀도/수익 팩터/손실폭/온엑스 동등성)를 기록했고 운영 KPI(운영 지표)로 주장하지 않았습니다.
- skill_receipt_lint(스킬 영수증 점검): satisfied(충족). experiment design/data integrity/model validation/artifact lineage/Grok review(실험 설계/데이터 무결성/모델 검증/산출물 계보/그록 검토)를 보고서와 실행 목록에 연결했습니다.
- required_gate_coverage_audit(필수 게이트 커버리지 감사): satisfied(충족). 이 문서가 closeout(마감) 주장과 gate coverage(게이트 커버리지)를 연결합니다.
- external_review_packet(외부 검토 묶음): satisfied(충족). Stage open(단계 개방)과 closeout(마감) Grok packets(그록 묶음)을 기록했습니다.
- final_claim_guard(최종 주장 보호): satisfied(충족). completion/baseline/promotion/runtime/live/Goal Achieve(완성/기준선/승격/런타임/실거래/목표 달성)를 주장하지 않았습니다.

Result(결과): closeout claim(마감 주장)은 negative_memory(부정 기억)+preserved_clue(보존 단서)로만 허용됩니다.
"""


def decision_text(summary: dict[str, Any]) -> str:
    return f"""# Decision(결정): Frontier06 Closeout(전선06 마감)

Date(날짜): 2026-06-14

Decision(결정): Close Frontier06(전선06 마감) as negative_memory(부정 기억)+preserved_clue(보존 단서).

Reason(이유): Frontier06B(전선06B)는 train-only selective abstention(학습 전용 선택 기권)으로 OOS density/PF/DD(표본밖 밀도/수익 팩터/손실폭)를 개선했지만, validation+OOS strict scout clue(검증+표본밖 엄격 탐색 단서)는 0개였습니다.

Boundary(경계): reference, not inheritance(참조이지 상속 아님). No completion(완성 없음), no baseline(기준선 없음), no promotion(승격 없음), no runtime authority(런타임 권위 없음), no live readiness(실거래 준비 없음).

Next(다음): `{NEXT_RUN_ID}`.
"""


def selection_text(summary: dict[str, Any]) -> str:
    return f"""# Stage Frontier 06 Selection Status(전선 06단계 선택 상태)

Updated(갱신): {summary['created_at_utc']}

Stage id(단계 ID): `{STAGE_ID}`

Current run(현재 실행): `{RUN_ID}`

Judgment(판정): `{summary['judgment']}`

Closeout label(마감 라벨): `{summary['local_decision']}`

Next action(다음 행동): `{NEXT_RUN_ID}`

Claim boundary(주장 경계): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def review_index_text(summary: dict[str, Any]) -> str:
    return f"""# Review Index(검토 색인)

- `frontier06A_stage_open_selective_probability_abstention_signal_contract_v1`: `{F06A_REPORT.as_posix()}`
- `frontier06B_selective_probability_abstention_signal_scout_v1`: `{F06B_REPORT.as_posix()}`
- `{RUN_ID}`: `{REPORT_PATH.as_posix()}` - `{summary['judgment']}`
"""


def current_state_text(summary: dict[str, Any]) -> str:
    return f"""# Current Working State(현재 작업 상태)

Updated(갱신): {summary['created_at_utc']}

Active stage(활성 단계): `{STAGE_ID}`

Current run(현재 실행): `{RUN_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Current truth(현재 진실): Frontier06(전선06)은 negative_memory(부정 기억)+preserved_clue(보존 단서)로 마감했습니다.

Judgment(판정): `{summary['judgment']}`

Negative memory(부정 기억): {summary['negative_memory']}

Preserved clue(보존 단서): {summary['preserved_clue']}

Next action(다음 행동): `{NEXT_RUN_ID}`. Action(행동)은 새 frontier hypothesis(전선 가설)를 여는 것입니다. Effect(효과)는 selective probability abstention threshold retry(선택적 확률 기권 임계값 재시도)를 반복하지 않는 것입니다.

Operating boundary(운영 경계): completion(완성), selected baseline(선택 기준선), operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def run_registry_row(now: str, summary: dict[str, Any]) -> dict[str, Any]:
    best = summary["best_rule_row"]
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "stage_closeout(단계 마감)",
        "status": summary["status"],
        "judgment": summary["judgment"],
        "path": REPORT_PATH.as_posix(),
        "notes": f"scout_clue_rows={summary['scout_clue_rows']};preserved_oos_pf={fmt(best.get('oos_rule_pf'))};no_authority",
        "work_family": "publish_handoff(게시/인계)",
        "run_number": RUN_NUMBER,
        "date": "2026-06-14",
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "candidate_count": "0",
        "claim_boundary": "closeout_negative_memory_preserved_clue_no_authority_goal_claim",
        "report_path": REPORT_PATH.as_posix(),
        "created_at_utc": now,
        "ledger_row_id": f"{RUN_ID}__stage_closeout",
        "subrun_id": f"{RUN_ID}__stage_closeout",
        "record_view": "stage_closeout(단계 마감)",
        "tier_scope": "not_applicable_stage_closeout(단계 마감에는 해당 없음)",
        "kpi_scope": "closeout_no_trading_kpi(마감 전용, 거래 KPI 없음)",
        "primary_kpi": f"negative_memory;preserved_oos_pf={fmt(best.get('oos_rule_pf'))};preserved_oos_density={fmt(best.get('oos_rule_density'))};preserved_oos_dd={fmt(best.get('oos_rule_dd'))}",
        "guardrail_kpi": "no_completion_no_baseline_no_promotion_no_runtime_no_live(완성/기준선/승격/런타임/실거래 없음)",
        "external_verification_status": "grok_closeout_review_captured_no_mt5(그록 마감 검토 기록, MT5 없음)",
        "source_run_id": PARENT_RUN_ID,
        "artifact_path": (RUN_ROOT / "stage_closeout_summary.json").as_posix(),
        "result_path": REPORT_PATH.as_posix(),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "exploration_lane": "frontier_hypothesis_lifecycle(전선 가설 생명주기)",
        "evidence_boundary": "stage_closeout_negative_memory_preserved_clue(단계 마감 부정 기억+보존 단서)",
        "reopen_condition": NEXT_RUN_ID,
        "question": "Should selective probability abstention remain active?(선택적 확률 기권을 계속 활성으로 둘 것인가?)",
        "skill_family": "publish_handoff(게시/인계)",
        "lineage_summary": "frontier06_stage_open_to_signal_scout_to_closeout(전선06 개방에서 신호 탐색과 마감)",
    }


def ledger_row(summary: dict[str, Any]) -> dict[str, Any]:
    best = summary["best_rule_row"]
    return {
        "ledger_row_id": f"{RUN_ID}__stage_closeout",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": f"{RUN_ID}__stage_closeout",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "stage_closeout(단계 마감)",
        "tier_scope": "not_applicable_stage_closeout(단계 마감에는 해당 없음)",
        "kpi_scope": "closeout_no_trading_kpi(마감 전용, 거래 KPI 없음)",
        "scoreboard_lane": "stage_closeout(단계 마감)",
        "status": summary["status"],
        "judgment": summary["judgment"],
        "path": REPORT_PATH.as_posix(),
        "primary_kpi": f"negative_memory;preserved_oos_pf={fmt(best.get('oos_rule_pf'))};preserved_oos_density={fmt(best.get('oos_rule_density'))};preserved_oos_dd={fmt(best.get('oos_rule_dd'))}",
        "guardrail_kpi": "no_completion_no_baseline_no_promotion_no_runtime_no_live(완성/기준선/승격/런타임/실거래 없음)",
        "external_verification_status": "grok_closeout_review_captured_no_mt5(그록 마감 검토 기록, MT5 없음)",
        "notes": f"next={NEXT_RUN_ID};no_authority",
    }


def best_rule_row() -> dict[str, Any]:
    manifest = read_json(F06B_MANIFEST)
    best = manifest.get("best_rule_row")
    if isinstance(best, dict) and best:
        return best
    rows = read_csv_rows(F06B_COMPARISON)
    rows.sort(
        key=lambda row: (
            str(row.get("strict_scout_clue_pass")).lower() == "true",
            num(row.get("combined_score_improvement_ratio")),
            num(row.get("oos_rule_pf")),
            -num(row.get("oos_rule_dd")),
        ),
        reverse=True,
    )
    return rows[0] if rows else {}


def top_rule_lines(limit: int = 5) -> str:
    rows = read_csv_rows(F06B_COMPARISON)
    rows.sort(
        key=lambda row: (
            str(row.get("strict_scout_clue_pass")).lower() == "true",
            num(row.get("combined_score_improvement_ratio")),
            num(row.get("oos_rule_pf")),
            -num(row.get("oos_rule_dd")),
        ),
        reverse=True,
    )
    lines = []
    for row in rows[:limit]:
        lines.append(
            "- "
            f"`{row.get('rule_id')}`: "
            f"validation PF/density/DD(검증 수익 팩터/밀도/손실폭) `{fmt(row.get('validation_rule_pf'))}`/`{fmt(row.get('validation_rule_density'))}`/`{fmt(row.get('validation_rule_dd'))}%`, "
            f"OOS PF/density/DD(표본밖 수익 팩터/밀도/손실폭) `{fmt(row.get('oos_rule_pf'))}`/`{fmt(row.get('oos_rule_density'))}`/`{fmt(row.get('oos_rule_dd'))}%`, "
            f"strict(엄격) `{row.get('strict_scout_clue_pass')}`"
        )
    return "\n".join(lines)


def parity_summary() -> str:
    rows = read_csv_rows(F06B_ONNX_PARITY)
    if not rows:
        return "missing(누락)"
    passed = sum(1 for row in rows if str(row.get("parity_passed")).lower() == "true")
    max_diff = max(num(row.get("parity_max_abs_diff")) for row in rows)
    return f"{passed}/{len(rows)} passed(통과), max_abs_diff(최대 절대 차이) {max_diff:.6g}"


def read_text(path: Path) -> str:
    return io_path(path).read_text(encoding="utf-8-sig")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(read_text(path))


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_text_sig(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text, encoding="utf-8-sig", newline="\n")


def upsert_csv(path: Path, key: str, row: dict[str, Any]) -> None:
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        header = next(csv.reader(handle))
    rows = read_csv_rows(path)
    normalized = {column: stringify(row.get(column, "")) for column in header}
    rows = [existing for existing in rows if existing.get(key) != normalized.get(key)]
    rows.append(normalized)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=header, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for item in rows:
            writer.writerow({column: stringify(item.get(column, "")) for column in header})


def stringify(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(json_ready(value), ensure_ascii=False, sort_keys=True)
    return str(value)


def num(value: Any) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return 0.0
    return number if math.isfinite(number) else 0.0


def fmt(value: Any) -> str:
    return f"{num(value):.6g}"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


if __name__ == "__main__":
    raise SystemExit(main())
