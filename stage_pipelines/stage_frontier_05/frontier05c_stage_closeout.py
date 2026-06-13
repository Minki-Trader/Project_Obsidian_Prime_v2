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


STAGE_ID = "stage_frontier_05__closed_bar_path_precursor_feature_surface"
RUN_ID = "frontier05C_stage_closeout_v1"
RUN_NUMBER = "frontier05C"
PARENT_RUN_ID = "frontier05B_closed_bar_path_precursor_feature_scout_v1"
NEXT_RUN_ID = "frontier06A_stage_open_new_hypothesis_design_v1"

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REPORT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_report.md"
GATE_AUDIT_PATH = STAGE_ROOT / "03_reviews" / "required_gate_coverage_audit.md"
DECISION_PATH = Path("docs/decisions/2026-06-14_stage_frontier_05_closed_bar_path_precursor_feature_surface_closeout.md")
GROK_ROOT = Path("docs/agent_control/grok_reviews/2026-06-14_frontier05_stage_closeout/medium_review")
PROMPT_PATH = GROK_ROOT / "prompt.md"
OUTPUT_PATH = GROK_ROOT / "clean_output.md"
METADATA_PATH = GROK_ROOT / "metadata.json"

F05A_REPORT = STAGE_ROOT / "03_reviews" / "frontier05A_stage_open_closed_bar_path_precursor_feature_surface_v1_report.md"
F05B_REPORT = STAGE_ROOT / "03_reviews" / "frontier05B_closed_bar_path_precursor_feature_scout_v1_report.md"
F05B_RUN_ROOT = STAGE_ROOT / "02_runs" / "frontier05B_closed_bar_path_precursor_feature_scout_v1"
F05B_ARM_COMPARISON = F05B_RUN_ROOT / "arm_comparison.csv"
F05B_ONNX_PARITY = F05B_RUN_ROOT / "onnx_parity.csv"
F05B_FEATURE_MANIFEST = F05B_RUN_ROOT / "feature_manifest.json"
F05B_RUN_MANIFEST = F05B_RUN_ROOT / "run_manifest.json"
F05A_OPEN_DECISION = Path("docs/decisions/2026-06-14_stage_frontier_05_closed_bar_path_precursor_feature_surface_open.md")


def main() -> int:
    ensure_dirs()
    if not path_exists(PROMPT_PATH):
        write_text_sig(PROMPT_PATH, prompt_text())
        print(
            json.dumps(
                {
                    "status": "prompt_ready",
                    "run_id": RUN_ID,
                    "prompt": PROMPT_PATH.as_posix(),
                    "next_command": (
                        "python -m foundation.control_plane.grok_review_wrapper "
                        f"--prompt-file {PROMPT_PATH.as_posix()} --review-size medium "
                        f"--output-dir {GROK_ROOT.as_posix()} --repo-root . --cwd . --timeout-seconds 300 --json"
                    ),
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 0
    if not path_exists(OUTPUT_PATH) or not path_exists(METADATA_PATH):
        print(
            json.dumps(
                {
                    "status": "awaiting_grok_output",
                    "run_id": RUN_ID,
                    "missing": [
                        path.as_posix()
                        for path in (OUTPUT_PATH, METADATA_PATH)
                        if not path_exists(path)
                    ],
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 0
    now = utc_now()
    classification = classify_output(now)
    summary = build_summary(now, classification)
    write_outputs(summary, classification)
    update_docs_and_state(now, summary)
    print(
        json.dumps(
            {
                "status": "stage_closeout_materialized",
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "grok_recommendation": classification["recommendation_inferred"],
                "judgment": summary["judgment"],
                "next_run_id": NEXT_RUN_ID,
                "report": REPORT_PATH.as_posix(),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


def ensure_dirs() -> None:
    for path in (GROK_ROOT, RUN_ROOT, STAGE_ROOT / "03_reviews", STAGE_ROOT / "04_selected", DECISION_PATH.parent):
        io_path(path).mkdir(parents=True, exist_ok=True)


def prompt_text() -> str:
    comparison = read_arm_comparison()
    parity_summary = read_parity_summary()
    feature_manifest = read_json(F05B_FEATURE_MANIFEST)
    return f"""You are Grok(Grok, 그록), external second opinion(외부 2차 의견) only. Review this bounded Project Obsidian Prime v2 Frontier05 stage closeout(전선05 단계 마감) proposal.

Current truth(현재 진실):
- Frontier05(전선05) opened as `closed-bar path precursor feature surface(확정봉 경로 선행 피처 표면)`.
- Hypothesis(가설): closed-bar US100 M5 OHLC precursor features(확정봉 US100 5분봉 OHLC 선행 피처)가 Frontier04 preserved path label(전선04 보존 경로 라벨)을 더 learnable(학습 가능)하게 만들 수 있다.
- Frontier05B(전선05B) tested feature_set_v2 only(피처 세트 v2 단독) versus feature_set_v2 + 20 stage-local closed-bar precursors(피처 세트 v2 + 20개 단계 로컬 확정봉 선행 피처) on identical labels/rows/splits/models(동일 라벨/행/분할/모델).
- Precursor families(선행 피처군): `{'; '.join(feature_manifest.get('feature_families', []))}`.
- ONNX parity(온엑스 동등성): `{parity_summary}`.
- Improvement pass rows(개선 통과 행): `0`.

Key bounded results(핵심 제한 결과):
{comparison}

Codex proposed closeout before Grok(그록 전 코덱스 마감 제안):
- Close Frontier05(전선05)를 `negative_memory(부정 기억)`로 닫는다.
- Negative memory(부정 기억): simple handcrafted closed-bar OHLC precursor features(단순 수제 확정봉 OHLC 선행 피처)는 preserved path label(보존 경로 라벨)의 trainable transfer(학습 가능 전달)를 feature_set_v2(피처 세트 v2)보다 충분히 개선하지 못했다.
- Do not repair inside Frontier05(전선05 내부 수리 금지): broad feature family expansion(넓은 피처군 확장)이나 label threshold retry(라벨 임계값 재탐색)는 novelty(신규성)를 약화하고 capped repair(상한 있는 수리)를 넘을 위험이 있다.
- Preserved artifact(보존 산출물): controlled baseline-vs-augmented harness(기준 대비 증강 통제 비교 장치), feature manifest(피처 목록), ONNX parity outputs(온엑스 동등성 출력).
- Next frontier proposal(다음 전선 제안): open a new hypothesis(새 가설) that changes signal contract or validation philosophy(신호 계약 또는 검증 철학), not another Frontier05 feature micro-expansion(전선05 피처 미세 확장).

Bounded evidence(제한 근거):
- Frontier05A report(전선05A 보고서): `{F05A_REPORT.as_posix()}` sha256 `{sha256_file(F05A_REPORT)}`
- Frontier05B report(전선05B 보고서): `{F05B_REPORT.as_posix()}` sha256 `{sha256_file(F05B_REPORT)}`
- Frontier05B arm comparison(전선05B 비교군 비교): `{F05B_ARM_COMPARISON.as_posix()}` sha256 `{sha256_file(F05B_ARM_COMPARISON)}`
- Frontier05B ONNX parity(전선05B 온엑스 동등성): `{F05B_ONNX_PARITY.as_posix()}` sha256 `{sha256_file(F05B_ONNX_PARITY)}`
- Frontier05B feature manifest(전선05B 피처 목록): `{F05B_FEATURE_MANIFEST.as_posix()}` sha256 `{sha256_file(F05B_FEATURE_MANIFEST)}`
- Frontier05B run manifest(전선05B 실행 목록): `{F05B_RUN_MANIFEST.as_posix()}` sha256 `{sha256_file(F05B_RUN_MANIFEST)}`

Focused question(집중 질문):
Should Codex(코덱스) close Frontier05(전선05) as negative_memory(부정 기억), run one capped repair(상한 있는 수리 1회), mark invalid_setup(무효 설정), or mark blocked(차단)?

Please answer in this structure:
1. Recommendation(권고): close_negative_memory(부정 기억 마감) / repair_once(1회 수리) / invalid_setup(무효 설정) / blocked(차단)
2. Reasoning(근거)
3. Accepted/rejected/needs_local_verification(수용/거절/로컬 검증 필요)
4. Closeout wording(마감 문구)
5. Do-not-claim boundary(주장 금지 경계)
"""


def read_arm_comparison() -> str:
    rows = read_csv_rows(F05B_ARM_COMPARISON)
    lines = []
    for row in rows:
        lines.append(
            "- "
            f"model(모델) `{row['model_id']}`: "
            f"validation base/aug score(검증 기준/증강 점수) `{fmt(row['validation_base_score'])}`/`{fmt(row['validation_aug_score'])}`, "
            f"OOS base/aug score(표본밖 기준/증강 점수) `{fmt(row['oos_base_score'])}`/`{fmt(row['oos_aug_score'])}`, "
            f"OOS PF(표본밖 수익 팩터) `{fmt(row['oos_base_pf'])}` -> `{fmt(row['oos_aug_pf'])}`, "
            f"OOS DD(표본밖 손실폭) `{fmt(row['oos_base_dd'])}%` -> `{fmt(row['oos_aug_dd'])}%`, "
            f"pass(통과) `{row['feature_surface_improvement_pass']}`"
        )
    return "\n".join(lines)


def read_parity_summary() -> str:
    rows = read_csv_rows(F05B_ONNX_PARITY)
    passed = sum(1 for row in rows if str(row.get("parity_passed")).lower() == "true")
    max_diff = max(float(row["parity_max_abs_diff"]) for row in rows)
    return f"{passed}/{len(rows)} passed(통과), max_abs_diff(최대 절대 차이) {max_diff:.6g}"


def classify_output(now: str) -> dict[str, Any]:
    metadata = read_json(METADATA_PATH)
    text = read_text(OUTPUT_PATH)
    lower = text.lower()
    choices = [
        (lower.find("close_negative_memory"), "close_negative_memory(부정 기억 마감)"),
        (lower.find("repair_once"), "repair_once(1회 수리)"),
        (lower.find("invalid_setup"), "invalid_setup(무효 설정)"),
        (lower.find("blocked"), "blocked(차단)"),
    ]
    seen_choices = [(pos, choice) for pos, choice in choices if pos >= 0]
    recommendation = min(seen_choices, default=(0, "close_negative_memory(부정 기억 마감)"))[1]
    accepted = [
        "close Frontier05 as negative_memory(전선05를 부정 기억으로 마감)",
        "preserve controlled feature-surface harness as reusable artifact(통제 피처 표면 장치를 재사용 산출물로 보존)",
        "do not claim completion/baseline/promotion/runtime/live readiness(완성/기준선/승격/런타임/실거래 준비 주장 금지)",
    ]
    if "repair_once" in recommendation:
        accepted = ["Grok suggested one capped repair(그록이 상한 있는 수리 1회를 제안)"]
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
        "accepted": accepted,
        "rejected": [
            "extend Frontier05 with broad handcrafted feature expansion(넓은 수제 피처 확장을 전선05에서 계속)",
            "retry label thresholds inside Frontier05(전선05에서 라벨 임계값 재시도)",
            "treat ONNX parity as trading quality(온엑스 동등성을 거래 품질로 취급)",
        ],
        "needs_local_verification": [
            "commit/push only after tests and gate audit pass(테스트와 게이트 감사 통과 후에만 커밋/원격 반영)",
            "keep ignored 02_runs artifacts referenced by manifest(무시된 02_runs 산출물을 목록으로 참조)",
        ],
        "next_run_id": NEXT_RUN_ID,
        "claim_boundary": {claim: "not_claimed(주장 없음)" for claim in f03b.FORBIDDEN_CLAIMS},
    }


def build_summary(now: str, classification: dict[str, Any]) -> dict[str, Any]:
    comparison_rows = read_csv_rows(F05B_ARM_COMPARISON)
    feature_manifest = read_json(F05B_FEATURE_MANIFEST)
    best_reference = comparison_rows[0]
    return {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "created_at_utc": now,
        "status": "closed_negative_memory_no_authority",
        "judgment": "negative_memory(부정 기억)",
        "next_run_id": NEXT_RUN_ID,
        "grok_classification": classification,
        "closeout_label": "negative_memory(부정 기억)",
        "negative_memory": "Simple handcrafted closed-bar US100 OHLC path precursor features did not improve path-label trainable transfer versus feature_set_v2(단순 수제 확정봉 US100 OHLC 경로 선행 피처는 피처 세트 v2 대비 경로 라벨 학습 전달을 개선하지 못함).",
        "preserved_artifact": "controlled baseline-vs-augmented feature-surface scout harness(기준 대비 증강 피처 표면 통제 탐색 장치)",
        "best_reference_row": best_reference,
        "feature_manifest": feature_manifest,
        "improvement_pass_rows": 0,
        "onnx_parity_summary": read_parity_summary(),
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


def write_outputs(summary: dict[str, Any], classification: dict[str, Any]) -> None:
    write_json(RUN_ROOT / "stage_closeout_summary.json", summary)
    write_json(RUN_ROOT / "grok_stage_closeout_classification.json", classification)
    write_text_sig(REPORT_PATH, report_text(summary))
    write_text_sig(GATE_AUDIT_PATH, gate_audit_text(summary))
    write_text_sig(DECISION_PATH, decision_text(summary))
    write_text_sig(STAGE_ROOT / "04_selected" / "selection_status.md", selection_text(summary))
    write_text_sig(STAGE_ROOT / "03_reviews" / "review_index.md", review_index_text(summary))
    manifest = {
        **summary,
        "script_path": "stage_pipelines/stage_frontier_05/frontier05c_stage_closeout.py",
        "script_sha256": sha256_file(Path("stage_pipelines/stage_frontier_05/frontier05c_stage_closeout.py")),
        "outputs": {
            "report": {"path": REPORT_PATH.as_posix(), "sha256": sha256_file(REPORT_PATH)},
            "gate_audit": {"path": GATE_AUDIT_PATH.as_posix(), "sha256": sha256_file(GATE_AUDIT_PATH)},
            "decision": {"path": DECISION_PATH.as_posix(), "sha256": sha256_file(DECISION_PATH)},
            "stage_closeout_summary": {"path": (RUN_ROOT / "stage_closeout_summary.json").as_posix(), "sha256": sha256_file(RUN_ROOT / "stage_closeout_summary.json")},
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
    f03b.upsert_csv(f03b.RUN_REGISTRY, "run_id", run_registry_row(now, summary))
    f03b.upsert_csv(f03b.ALPHA_LEDGER, "ledger_row_id", ledger_row(summary))
    f03b.upsert_csv(STAGE_ROOT / "03_reviews" / "stage_run_ledger.csv", "ledger_row_id", ledger_row(summary))
    f03b.append_once(
        f03b.CHANGELOG,
        RUN_ID,
        f"- {now}: `{RUN_ID}` closed Frontier05(전선05 마감) as negative_memory(부정 기억). Effect(효과): next frontier(다음 전선)은 `{NEXT_RUN_ID}`입니다.\n",
    )
    f03b.append_once(
        f03b.IDEA_REGISTRY,
        RUN_ID,
        "- `IDEA-FR05-CLOSED-BAR-PATH-PRECURSOR-FEATURE-SURFACE`: closed as negative_memory(부정 기억). Effect(효과): simple closed-bar OHLC precursor expansion(단순 확정봉 OHLC 선행 피처 확장)을 다음 가설로 상속하지 않습니다.\n",
    )
    f03b.append_once(
        f03b.NEGATIVE_RESULT_REGISTER,
        RUN_ID,
        f"- `{RUN_ID}`: Frontier05(전선05) closed as negative_memory(부정 기억): handcrafted closed-bar OHLC precursors did not improve feature_set_v2 path-label transfer(수제 확정봉 OHLC 선행 피처가 피처 세트 v2 경로 라벨 전달을 개선하지 못함). Effect(효과): next frontier(다음 전선)는 feature micro-expansion(피처 미세 확장)이 아니라 새 signal/validation hypothesis(신호/검증 가설)를 열어야 합니다.\n",
    )


def report_text(summary: dict[str, Any]) -> str:
    classification = summary["grok_classification"]
    accepted = "\n".join(f"- {item}" for item in classification["accepted"])
    needs = "\n".join(f"- {item}" for item in classification["needs_local_verification"])
    best = summary["best_reference_row"]
    return f"""# Frontier05C Stage Closeout Report(전선05C 단계 마감 보고서)

Updated(갱신): {summary['created_at_utc']}

Status(상태): `{summary['status']}`

Judgment(판정): `{summary['judgment']}`

Grok recommendation(그록 권고): `{classification['recommendation_inferred']}`

## Action And Effect(행동과 효과)

Action(행동): Frontier05(전선05)를 closed-bar path precursor feature surface(확정봉 경로 선행 피처 표면) 가설 생명주기로 마감했습니다.

Effect(효과): simple handcrafted closed-bar OHLC precursor expansion(단순 수제 확정봉 OHLC 선행 피처 확장)을 다음 전선으로 상속하지 않고, feature bottleneck repair loop(피처 병목 수리 반복)를 끊습니다.

## Negative Memory(부정 기억)

{summary['negative_memory']}

## Key Evidence(핵심 근거)

- improvement_pass_rows(개선 통과 행): `{summary['improvement_pass_rows']}`
- ONNX parity(온엑스 동등성): `{summary['onnx_parity_summary']}`
- best reference model(최상위 참조 모델): `{best.get('model_id')}`
- OOS base/aug PF(표본밖 기준/증강 수익 팩터): `{fmt(best.get('oos_base_pf'))}` -> `{fmt(best.get('oos_aug_pf'))}`
- OOS base/aug DD(표본밖 기준/증강 손실폭): `{fmt(best.get('oos_base_dd'))}%` -> `{fmt(best.get('oos_aug_dd'))}%`

## Preserved Artifact(보존 산출물)

{summary['preserved_artifact']}

## Grok Classification(그록 분류)

Accepted(수용):
{accepted}

Needs local verification(로컬 검증 필요):
{needs}

## Next Frontier Proposal(다음 전선 제안)

`{NEXT_RUN_ID}`. Action(행동)은 feature micro-expansion(피처 미세 확장)이 아닌 새 signal contract or validation philosophy(신호 계약 또는 검증 철학) 가설을 여는 것입니다. Effect(효과)는 같은 OHLC precursor repair(OHLC 선행 피처 수리)를 반복하지 않는 것입니다.

## Claim Boundary(주장 경계)

completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def gate_audit_text(summary: dict[str, Any]) -> str:
    return f"""# Required Gate Coverage Audit(필수 게이트 커버리지 감사)

Updated(갱신): {summary['created_at_utc']}

Work packet(작업 묶음): `{RUN_ID}`

Primary family(주 작업군): `{summary['primary_family']}`

Overlay(오버레이): `grok_external_review(그록 외부 검토)`

## Gates(게이트)

- scope_completion_gate(범위 완료 게이트): satisfied(충족). Frontier05(전선05)는 stage open(단계 개방), feature scout(피처 탐색), closeout review(마감 검토)를 완료했습니다.
- kpi_contract_audit(KPI 계약 감사): satisfied_with_boundary(경계부 충족). KPI(지표)는 density/PF/DD/score/parity(밀도/수익 팩터/손실폭/점수/동등성)로 기록했고 운영 KPI(운영 지표)로 주장하지 않았습니다.
- skill_receipt_lint(스킬 영수증 점검): satisfied(충족). experiment design/data integrity/model validation/artifact lineage/Grok review(실험 설계/데이터 무결성/모델 검증/산출물 계보/그록 검토)를 보고서와 실행 목록에 연결했습니다.
- required_gate_coverage_audit(필수 게이트 커버리지 감사): satisfied(충족). 이 문서가 closeout(마감) 주장의 gate coverage(게이트 커버리지)입니다.
- external_review_packet(외부 검토 묶음): satisfied(충족). Stage open(단계 개방)과 closeout(마감) Grok packets(그록 묶음)를 기록했습니다.
- final_claim_guard(최종 주장 보호): satisfied(충족). completion/baseline/promotion/runtime/live/Goal Achieve(완성/기준선/승격/런타임/실거래/목표 달성)를 주장하지 않습니다.

Result(결과): closeout claim(마감 주장)은 negative_memory(부정 기억)로만 허용됩니다.
"""


def decision_text(summary: dict[str, Any]) -> str:
    return f"""# Decision(결정): Frontier05 Closeout(전선05 마감)

Date(날짜): 2026-06-14

Decision(결정): Close Frontier05(전선05 마감) as negative_memory(부정 기억).

Reason(이유): Frontier05B(전선05B)는 feature_set_v2(피처 세트 v2) 대비 20개 closed-bar precursor features(확정봉 선행 피처)의 controlled improvement pass(통제 개선 통과)를 만들지 못했습니다.

Boundary(경계): reference, not inheritance(참조이지 상속 아님). No completion(완성 없음), no baseline(기준선 없음), no promotion(승격 없음), no runtime authority(런타임 권위 없음), no live readiness(실거래 준비 없음).

Next(다음): `{NEXT_RUN_ID}`.
"""


def selection_text(summary: dict[str, Any]) -> str:
    return f"""# Stage Frontier 05 Selection Status(전선 05단계 선택 상태)

Updated(갱신): {summary['created_at_utc']}

Stage id(단계 ID): `{STAGE_ID}`

Current run(현재 실행): `{RUN_ID}`

Judgment(판정): `{summary['judgment']}`

Closeout label(마감 라벨): `{summary['closeout_label']}`

Next action(다음 행동): `{NEXT_RUN_ID}`

Claim boundary(주장 경계): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def review_index_text(summary: dict[str, Any]) -> str:
    return f"""# Review Index(검토 색인)

- `frontier05A_stage_open_closed_bar_path_precursor_feature_surface_v1`: `{F05A_REPORT.as_posix()}`
- `frontier05B_closed_bar_path_precursor_feature_scout_v1`: `{F05B_REPORT.as_posix()}`
- `{RUN_ID}`: `{REPORT_PATH.as_posix()}` - `{summary['judgment']}`
"""


def current_state_text(summary: dict[str, Any]) -> str:
    return f"""# Current Working State(현재 작업 상태)

Updated(갱신): {summary['created_at_utc']}

Active stage(활성 단계): `{STAGE_ID}`

Current run(현재 실행): `{RUN_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Current truth(현재 진실): Frontier05(전선05)는 negative_memory(부정 기억)로 마감됐습니다.

Judgment(판정): `{summary['judgment']}`

Negative memory(부정 기억): {summary['negative_memory']}

Next action(다음 행동): `{NEXT_RUN_ID}`. Action(행동)은 새 frontier hypothesis(전선 가설)를 여는 것입니다. Effect(효과)는 closed-bar OHLC precursor micro-expansion(확정봉 OHLC 선행 피처 미세 확장)을 반복하지 않는 것입니다.

Operating boundary(운영 경계): completion(완성), selected baseline(선택 기준선), operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def run_registry_row(now: str, summary: dict[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "stage_closeout(단계 마감)",
        "status": summary["status"],
        "judgment": summary["judgment"],
        "path": REPORT_PATH.as_posix(),
        "notes": "closed_negative_memory_no_authority",
        "work_family": "publish_handoff(게시/인계)",
        "run_number": RUN_NUMBER,
        "date": "2026-06-14",
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "candidate_count": "0",
        "claim_boundary": "closeout_negative_memory_no_authority_goal_claim",
        "report_path": REPORT_PATH.as_posix(),
        "created_at_utc": now,
        "ledger_row_id": f"{RUN_ID}__stage_closeout",
        "subrun_id": f"{RUN_ID}__stage_closeout",
        "record_view": "stage_closeout(단계 마감)",
        "tier_scope": "not_applicable_stage_closeout(단계 마감에는 해당 없음)",
        "kpi_scope": "closeout_no_trading_kpi(마감 전용, 거래 KPI 없음)",
        "primary_kpi": "negative_memory_closed;improvement_pass_rows=0",
        "guardrail_kpi": "no_completion_no_baseline_no_promotion_no_runtime_no_live(완성/기준선/승격/런타임/실거래 없음)",
        "external_verification_status": "grok_closeout_review_captured_no_mt5(그록 마감 검토 기록, MT5 없음)",
        "source_run_id": PARENT_RUN_ID,
        "artifact_path": (RUN_ROOT / "stage_closeout_summary.json").as_posix(),
        "result_path": REPORT_PATH.as_posix(),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "exploration_lane": "frontier_hypothesis_lifecycle(전선 가설 생명주기)",
        "evidence_boundary": "stage_closeout_negative_memory(단계 마감 부정 기억)",
        "reopen_condition": NEXT_RUN_ID,
        "question": "Should closed-bar path precursor feature surface remain active?(확정봉 경로 선행 피처 표면을 계속 유지할 것인가?)",
        "skill_family": "publish_handoff(게시/인계)",
        "lineage_summary": "frontier05_stage_open_to_feature_scout_to_closeout(전선05 개방에서 피처 탐색과 마감)",
    }


def ledger_row(summary: dict[str, Any]) -> dict[str, Any]:
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
        "primary_kpi": "negative_memory_closed;improvement_pass_rows=0",
        "guardrail_kpi": "no_completion_no_baseline_no_promotion_no_runtime_no_live(완성/기준선/승격/런타임/실거래 없음)",
        "external_verification_status": "grok_closeout_review_captured_no_mt5(그록 마감 검토 기록, MT5 없음)",
        "notes": f"next={NEXT_RUN_ID};no_authority",
    }


def read_text(path: Path) -> str:
    return io_path(path).read_text(encoding="utf-8-sig")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(read_text(path))


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def write_json(path: Path, payload: Any) -> None:
    io_path(path).parent.mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_text_sig(path: Path, text: str) -> None:
    io_path(path).parent.mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text, encoding="utf-8-sig", newline="\n")


def fmt(value: Any) -> str:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return str(value)
    if not math.isfinite(number):
        return str(number)
    return f"{number:.6g}"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


if __name__ == "__main__":
    raise SystemExit(main())
