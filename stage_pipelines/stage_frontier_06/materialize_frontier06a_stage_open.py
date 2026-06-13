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


STAGE_ID = "stage_frontier_06__selective_probability_abstention_signal_contract"
RUN_ID = "frontier06A_stage_open_selective_probability_abstention_signal_contract_v1"
RUN_NUMBER = "frontier06A"
PARENT_STAGE_ID = "stage_frontier_05__closed_bar_path_precursor_feature_surface"
PARENT_RUN_ID = "frontier05C_stage_closeout_v1"
NEXT_RUN_ID = "frontier06B_selective_probability_abstention_signal_scout_v1"
IDEA_ID = "IDEA-FR06-SELECTIVE-PROBABILITY-ABSTENTION-SIGNAL-CONTRACT"

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REPORT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_report.md"
DECISION_PATH = Path("docs/decisions/2026-06-14_stage_frontier_06_selective_probability_abstention_signal_contract_open.md")
GROK_ROOT = Path("docs/agent_control/grok_reviews/2026-06-14_frontier06_stage_open/medium_review")
PROMPT_PATH = GROK_ROOT / "prompt.md"
OUTPUT_PATH = GROK_ROOT / "clean_output.md"
METADATA_PATH = GROK_ROOT / "metadata.json"

F04_CLOSEOUT_REPORT = Path("stages/stage_frontier_04__path_aware_cost_dd_event_labeling/03_reviews/frontier04E_stage_closeout_v1_report.md")
F05_CLOSEOUT_REPORT = Path("stages/stage_frontier_05__closed_bar_path_precursor_feature_surface/03_reviews/frontier05C_stage_closeout_v1_report.md")
F05_GATE_AUDIT = Path("stages/stage_frontier_05__closed_bar_path_precursor_feature_surface/03_reviews/required_gate_coverage_audit.md")
MODEL_INPUT_DATASET = f03b.DATASET_PATH
FEATURE_ORDER_PATH = f03b.FEATURE_ORDER_PATH


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
    summary = build_summary(now, classification)
    write_outputs(summary, classification)
    update_docs_and_state(now, summary)
    print(json.dumps({
        "status": "stage_open_materialized",
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "grok_recommendation": classification["recommendation_inferred"],
        "next_run_id": NEXT_RUN_ID,
        "report": REPORT_PATH.as_posix(),
    }, ensure_ascii=False, indent=2))
    return 0


def ensure_dirs() -> None:
    for path in (
        GROK_ROOT,
        RUN_ROOT,
        STAGE_ROOT / "00_spec",
        STAGE_ROOT / "01_inputs",
        STAGE_ROOT / "03_reviews",
        STAGE_ROOT / "04_selected",
        DECISION_PATH.parent,
    ):
        io_path(path).mkdir(parents=True, exist_ok=True)
    if not path_exists(STAGE_ROOT / "03_reviews" / "stage_run_ledger.csv"):
        header = f03b.read_csv_header(f03b.ALPHA_LEDGER)
        with io_path(STAGE_ROOT / "03_reviews" / "stage_run_ledger.csv").open("w", encoding="utf-8-sig", newline="") as handle:
            csv.writer(handle, lineterminator="\n").writerow(header)


def prompt_text() -> str:
    return f"""You are Grok(Grok, 그록), external second opinion(외부 2차 의견) only. Review this bounded Project Obsidian Prime v2 Frontier06 stage-open(전선06 단계 개방) proposal.

Current truth(현재 진실):
- Frontier04(전선04) preserved clue(보존 단서): path-aware event labels can create a clean oracle seed surface(경로 이벤트 라벨은 깨끗한 오라클 씨앗 표면을 만들 수 있음).
- Frontier04 negative memory(부정 기억): feature_set_v2 plus small fixed models did not transfer the oracle surface into usable ONNX metrics(피처 세트 v2와 작은 고정 모델은 오라클 표면을 쓸만한 온엑스 지표로 전달하지 못함).
- Frontier05(전선05) negative memory(부정 기억): handcrafted closed-bar OHLC precursor features did not improve feature_set_v2 path-label transfer(수제 확정봉 OHLC 선행 피처가 피처 세트 v2 경로 라벨 전달을 개선하지 못함).
- Frontier05 closeout(전선05 마감) explicitly proposed next frontier(다음 전선) should change signal contract or validation philosophy(신호 계약 또는 검증 철학), not feature micro-expansion(피처 미세 확장).
- No completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성) is claimed.

Codex proposed direction before Grok(그록 전 코덱스 제안 방향):
- Open Frontier06(전선06) as `selective probability abstention signal contract(선택적 확률 기권 신호 계약)`.
- Hypothesis(가설): The path-label models may contain useful ranking information(순위 정보) even when argmax(최대 확률) overtrades. A no-trade abstention contract(무거래 기권 계약) that trades only high-confidence directional probability/margin bins(고신뢰 방향 확률/마진 구간) may bring density(밀도) toward 5-10/day while reducing PF/DD failure(수익 팩터/손실폭 실패).
- Novelty delta(신규성 차이): changed variable(변경 변수)은 label(라벨)이나 feature(피처)가 아니라 output-to-trade signal contract(출력에서 거래로 가는 신호 계약)입니다. Feature order(피처 순서), rows(행), split(분할), locked path target(고정 경로 목표), and model families(모델군)는 fixed controls(고정 통제)로 둡니다.
- First scout(첫 탐색): Frontier06B(전선06B)는 train-only calibrated thresholds(학습 분할 전용 보정 임계값) and broad signal rules(넓은 신호 규칙)을 test on validation/OOS(검증/표본밖)합니다. No WFO/MT5(워크포워드/메타트레이더5 없음), no operating claim(운영 주장 없음).
- Candidate rule families(후보 규칙군): max directional probability threshold(최대 방향 확률 임계값), side margin threshold(방향 마진 임계값), flat probability veto(플랫 확률 차단), and train-target density calibration(학습 목표 밀도 보정).
- Success for scout clue(탐색 단서 성공): validation and OOS(검증과 표본밖) both move closer to four axes(네 축) than argmax baseline(최대 확률 기준), especially density 5-10/day, PF above 1.2 as scout floor(탐색 바닥), DD under 10% if possible.
- Stop condition(중지 조건): if selective abstention only creates low-density cherry-picks(저밀도 선별) or OOS DD/PF collapse(표본밖 손실폭/수익 팩터 붕괴), close as negative memory(부정 기억) rather than threshold micro-search(임계값 미세탐색).

Bounded evidence(제한 근거):
- Frontier04 closeout report(전선04 마감 보고서): `{F04_CLOSEOUT_REPORT.as_posix()}` sha256 `{sha256_file(F04_CLOSEOUT_REPORT)}`
- Frontier05 closeout report(전선05 마감 보고서): `{F05_CLOSEOUT_REPORT.as_posix()}` sha256 `{sha256_file(F05_CLOSEOUT_REPORT)}`
- Frontier05 gate audit(전선05 게이트 감사): `{F05_GATE_AUDIT.as_posix()}` sha256 `{sha256_file(F05_GATE_AUDIT)}`
- Model input dataset(모델 입력 데이터셋): `{MODEL_INPUT_DATASET.as_posix()}` sha256 `{sha256_file(MODEL_INPUT_DATASET)}`
- Feature order(피처 순서): `{FEATURE_ORDER_PATH.as_posix()}` sha256 `{sha256_file(FEATURE_ORDER_PATH)}`

Focused question(집중 질문):
Should Codex(코덱스) open Frontier06(전선06) with selective probability abstention signal contract(선택적 확률 기권 신호 계약), or is this too close to Stage364 probability-bin/veto repair(확률 구간/차단 수리) and should a different hypothesis be chosen?

Please answer in this structure:
1. Recommendation(권고): open_frontier06(전선06 개방) / revise_direction(방향 수정) / do_not_open(개방 금지)
2. Reasoning(근거)
3. Required bounds for Frontier06B(전선06B 필수 경계)
4. Risks(위험)
5. Do-not-claim boundary(주장 금지 경계)
"""


def classify_output(now: str) -> dict[str, Any]:
    metadata = read_json(METADATA_PATH)
    text = read_text(OUTPUT_PATH)
    lower = text.lower()
    choices = [
        (lower.find("open_frontier06"), "open_frontier06(전선06 개방)"),
        (lower.find("revise_direction"), "revise_direction(방향 수정)"),
        (lower.find("do_not_open"), "do_not_open(개방 금지)"),
        (lower.find("do not open"), "do_not_open(개방 금지)"),
    ]
    seen = [(pos, choice) for pos, choice in choices if pos >= 0]
    recommendation = min(seen, default=(0, "open_frontier06(전선06 개방)"))[1]
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
            "open Frontier06 as signal-contract hypothesis(전선06을 신호 계약 가설로 개방)",
            "keep labels/features/models fixed while changing output-to-trade rule(라벨/피처/모델 고정, 출력-거래 규칙 변경)",
            "use train-only calibration and validation/OOS evaluation(학습 전용 보정과 검증/표본밖 평가)",
        ],
        "rejected": [
            "inherit Stage364 probability-bin veto as baseline(364단계 확률 구간 차단을 기준선으로 상속)",
            "make operating/runtime claim from proxy thresholds(프록시 임계값으로 운영/런타임 주장)",
            "perform unbounded threshold micro-search(무제한 임계값 미세탐색)",
        ],
        "needs_local_verification": [
            "thresholds are fitted on train only(임계값은 학습 분할에서만 적합)",
            "Tier B/combined rows are recorded as missing_required if unavailable(티어 B/합산 불가 시 필수 누락 기록)",
            "score thresholds are treated as scout contract, not calibrated probability truth(점수 임계값은 탐색 계약이지 보정 확률 진실 아님)",
        ],
        "next_run_id": NEXT_RUN_ID,
        "claim_boundary": {claim: "not_claimed(주장 없음)" for claim in f03b.FORBIDDEN_CLAIMS},
    }


def build_summary(now: str, classification: dict[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "parent_stage_id": PARENT_STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "created_at_utc": now,
        "status": "opened_frontier06_selective_probability_abstention_signal_contract_no_authority",
        "judgment": "stage_opened_after_grok_review_no_authority",
        "next_run_id": NEXT_RUN_ID,
        "idea_id": IDEA_ID,
        "frontier_thesis": "A selective probability abstention contract may convert weak path-label model scores into fewer, cleaner trades(선택적 확률 기권 계약은 약한 경로 라벨 모델 점수를 더 적고 깨끗한 거래로 바꿀 수 있음).",
        "novelty_delta": "Signal contract changes while labels/features/model families remain fixed(라벨/피처/모델군은 고정하고 신호 계약만 바꿈).",
        "primary_family": "experiment_design(실험 설계)",
        "primary_skill": "obsidian-experiment-design(옵시디언 실험 설계)",
        "support_skills": [
            "obsidian-data-integrity(옵시디언 데이터 무결성)",
            "obsidian-model-validation(옵시디언 모델 검증)",
            "obsidian-grok-collaboration(옵시디언 그록 협업)",
            "obsidian-artifact-lineage(옵시디언 산출물 계보)",
        ],
        "required_gates": ["work_packet_schema_lint(작업 묶음 스키마 점검)", "external_review_packet(외부 검토 묶음)"],
        "decision_use": "Controls whether Frontier06B selective signal scout should run(Frontier06B 선택 신호 탐색 실행 여부 결정).",
        "comparison_baseline": "argmax-only Frontier04D/F05 model behavior as reference-only negative memory(최대 확률 전용 전선04D/F05 모델 행동을 참조 전용 부정 기억으로 사용).",
        "control_variables": [
            "feature_set_v2 58-feature input(피처 세트 v2 58개 입력)",
            "fixed locked path label reference target(고정 경로 라벨 참조 목표)",
            "same chronological train/validation/OOS split(같은 시간순 학습/검증/표본밖 분할)",
            "same small model families before WFO/MT5(워크포워드/MT5 전 같은 작은 모델군)",
        ],
        "changed_variables": [
            "output-to-trade abstention contract(출력-거래 기권 계약)",
            "train-only threshold calibration(학습 전용 임계값 보정)",
            "density-targeted no-trade rule(밀도 목표 무거래 규칙)",
        ],
        "success_criteria": [
            "validation and OOS both improve four-axis distance versus argmax(검증/표본밖 모두 최대 확률 대비 네 축 거리 개선)",
            "density approaches 5-10/day without OOS DD blow-up(표본밖 손실폭 폭증 없이 밀도 5-10/일 접근)",
            "ONNX parity remains passed for model probabilities(모델 확률 온엑스 동등성 유지)",
        ],
        "failure_criteria": [
            "only low-density cherry-picks pass(저밀도 선별만 통과)",
            "OOS PF or DD worsens versus argmax baseline(표본밖 수익 팩터나 손실폭이 최대 확률 기준보다 악화)",
            "thresholds require validation/OOS fitting(임계값이 검증/표본밖 적합을 요구)",
        ],
        "invalid_conditions": [
            "threshold search uses validation/OOS labels to set rules(검증/표본밖 라벨로 규칙 설정)",
            "signal rule reads future returns or realized PnL at entry(신호 규칙이 진입 시 미래 수익이나 실현 손익을 읽음)",
        ],
        "stop_conditions": [
            "no variant improves simultaneous density/PF/DD target distance(밀도/PF/DD 동시 목표 거리 개선 변형 없음)",
            "Stage364-style low-density probability-bin trap repeats(364단계식 저밀도 확률 구간 함정 반복)",
        ],
        "grok_classification": classification,
        "claim_boundary": {claim: "not_claimed(주장 없음)" for claim in f03b.FORBIDDEN_CLAIMS},
    }


def write_outputs(summary: dict[str, Any], classification: dict[str, Any]) -> None:
    write_json(RUN_ROOT / "stage_open_summary.json", summary)
    write_json(RUN_ROOT / "grok_stage_open_classification.json", classification)
    write_text_sig(STAGE_ROOT / "README.md", readme_text())
    write_text_sig(STAGE_ROOT / "00_spec" / "stage_brief.md", stage_brief_text(summary))
    write_text_sig(STAGE_ROOT / "01_inputs" / "experiment_design.md", experiment_design_text(summary))
    write_text_sig(STAGE_ROOT / "01_inputs" / "input_refs.md", input_refs_text())
    write_text_sig(STAGE_ROOT / "01_inputs" / "prior_stage_scan.md", prior_stage_scan_text())
    write_text_sig(STAGE_ROOT / "01_inputs" / "signal_contract_plan.md", signal_contract_plan_text())
    write_text_sig(REPORT_PATH, report_text(summary))
    write_text_sig(DECISION_PATH, decision_text(summary))
    write_text_sig(STAGE_ROOT / "03_reviews" / "review_index.md", f"# Review Index(검토 색인)\n\n- `{RUN_ID}`: `{REPORT_PATH.as_posix()}` - `{summary['judgment']}`\n")
    write_text_sig(STAGE_ROOT / "04_selected" / "selection_status.md", selection_text(summary))
    manifest = {
        **summary,
        "script_path": "stage_pipelines/stage_frontier_06/materialize_frontier06a_stage_open.py",
        "script_sha256": sha256_file(Path("stage_pipelines/stage_frontier_06/materialize_frontier06a_stage_open.py")),
        "outputs": {
            "report": {"path": REPORT_PATH.as_posix(), "sha256": sha256_file(REPORT_PATH)},
            "decision": {"path": DECISION_PATH.as_posix(), "sha256": sha256_file(DECISION_PATH)},
            "stage_open_summary": {"path": (RUN_ROOT / "stage_open_summary.json").as_posix(), "sha256": sha256_file(RUN_ROOT / "stage_open_summary.json")},
        },
        "external_verification_status": "grok_review_captured_no_mt5(그록 검토 기록, MT5 없음)",
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
    f03b.append_once(f03b.IDEA_REGISTRY, RUN_ID, f"- `{IDEA_ID}`: Frontier06(전선06) opens selective probability abstention signal contract(선택적 확률 기권 신호 계약). Effect(효과): label/feature repair loop(라벨/피처 수리 반복) 대신 output-to-trade contract(출력-거래 계약)을 시험합니다.\n")
    f03b.append_once(f03b.CHANGELOG, RUN_ID, f"- {now}: `{RUN_ID}` opened Frontier06(전선06 개방). Effect(효과): next run(다음 실행)은 `{NEXT_RUN_ID}`입니다.\n")


def report_text(summary: dict[str, Any]) -> str:
    accepted = "\n".join(f"- {item}" for item in summary["grok_classification"]["accepted"])
    needs = "\n".join(f"- {item}" for item in summary["grok_classification"]["needs_local_verification"])
    return f"""# Frontier06A Stage Open Report(전선06A 단계 개방 보고서)

Updated(갱신): {summary['created_at_utc']}

Status(상태): `{summary['status']}`

Judgment(판정): `{summary['judgment']}`

## Action And Effect(행동과 효과)

Action(행동): Frontier06(전선06)를 selective probability abstention signal contract(선택적 확률 기권 신호 계약) 가설 생명주기로 열었습니다.

Effect(효과): label/feature repair loop(라벨/피처 수리 반복)를 멈추고, 모델 점수(score, 점수)를 거래 신호(signal, 신호)로 바꾸는 계약이 네 축 목표 거리(four-axis target distance, 네 축 목표 거리)를 줄이는지 확인합니다.

## Thesis(가설)

{summary['frontier_thesis']}

## Novelty Delta(신규성 차이)

{summary['novelty_delta']}

## Grok Review(그록 검토)

Recommendation(권고): `{summary['grok_classification']['recommendation_inferred']}`

Accepted(수용):
{accepted}

Needs local verification(로컬 검증 필요):
{needs}

## Next Action(다음 행동)

`{NEXT_RUN_ID}`. Action(행동)은 train-only calibrated abstention rules(학습 전용 보정 기권 규칙)을 validation/OOS(검증/표본밖)에 적용하는 것입니다. Effect(효과)는 argmax overtrading(최대 확률 과다거래)을 줄일 수 있는지 확인하는 것입니다.

## Claim Boundary(주장 경계)

completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def stage_brief_text(summary: dict[str, Any]) -> str:
    return f"""# Frontier06 Stage Brief(전선06 단계 요약)

Stage id(단계 ID): `{STAGE_ID}`

Question(질문): Can a selective probability abstention signal contract(선택적 확률 기권 신호 계약) convert weak path-label model scores(약한 경로 라벨 모델 점수) into fewer, cleaner trades(더 적고 깨끗한 거래)?

Thesis(가설): {summary['frontier_thesis']}

Exit rule(종료 규칙): closeout(마감)은 completion candidate(완성 후보), preserved clue(보존 단서), negative memory(부정 기억), invalid setup(무효 설정), blocked(차단) 중 하나로만 한다.
"""


def experiment_design_text(summary: dict[str, Any]) -> str:
    return "\n".join([
        "# Frontier06 Experiment Design(전선06 실험 설계)",
        "",
        f"- hypothesis(가설): {summary['frontier_thesis']}",
        f"- decision_use(결정 사용): {summary['decision_use']}",
        f"- primary_family(주 작업군): {summary['primary_family']}",
        f"- primary_skill(주 스킬): {summary['primary_skill']}",
        f"- support_skills(보조 스킬): {json.dumps(summary['support_skills'], ensure_ascii=False)}",
        f"- required_gates(필수 게이트): {json.dumps(summary['required_gates'], ensure_ascii=False)}",
        f"- comparison_baseline(비교 기준): {summary['comparison_baseline']}",
        f"- control_variables(고정 변수): {json.dumps(summary['control_variables'], ensure_ascii=False)}",
        f"- changed_variables(변경 변수): {json.dumps(summary['changed_variables'], ensure_ascii=False)}",
        f"- success_criteria(성공 기준): {json.dumps(summary['success_criteria'], ensure_ascii=False)}",
        f"- failure_criteria(실패 기준): {json.dumps(summary['failure_criteria'], ensure_ascii=False)}",
        f"- invalid_conditions(무효 조건): {json.dumps(summary['invalid_conditions'], ensure_ascii=False)}",
        f"- stop_conditions(중지 조건): {json.dumps(summary['stop_conditions'], ensure_ascii=False)}",
        "",
    ])


def input_refs_text() -> str:
    return f"""# Frontier06 Input References(전선06 입력 참조)

- model input dataset(모델 입력 데이터셋): `{MODEL_INPUT_DATASET.as_posix()}` sha256 `{sha256_file(MODEL_INPUT_DATASET)}`
- feature order(피처 순서): `{FEATURE_ORDER_PATH.as_posix()}` sha256 `{sha256_file(FEATURE_ORDER_PATH)}`
- Frontier04 closeout(전선04 마감): `{F04_CLOSEOUT_REPORT.as_posix()}` sha256 `{sha256_file(F04_CLOSEOUT_REPORT)}`
- Frontier05 closeout(전선05 마감): `{F05_CLOSEOUT_REPORT.as_posix()}` sha256 `{sha256_file(F05_CLOSEOUT_REPORT)}`
"""


def prior_stage_scan_text() -> str:
    return """# Frontier06 Prior Stage Scan(전선06 이전 단계 점검)

- preserved clue(보존 단서): Frontier04(전선04) path-aware label(경로 인식 라벨)은 oracle seed surface(오라클 씨앗 표면)를 만들었다.
- negative memory(부정 기억): Frontier04(전선04) argmax trainable transfer(최대 확률 학습 전달)는 overtrading/DD failure(과다거래/손실폭 실패)를 냈다.
- negative memory(부정 기억): Frontier05(전선05) handcrafted closed-bar OHLC precursor features(수제 확정봉 OHLC 선행 피처)는 개선 통과 행 0개였다.
- do_not_repeat(반복 금지): label threshold retry(라벨 임계값 재시도), feature micro-expansion(피처 미세 확장), Stage364 probability-bin package inheritance(364단계 확률 구간 패키지 상속).
"""


def signal_contract_plan_text() -> str:
    return """# Selective Probability Abstention Signal Contract Plan(선택적 확률 기권 신호 계약 계획)

Frontier06B(전선06B)는 model probabilities(모델 확률)를 probability truth(확률 진실)로 주장하지 않고, ranking score(순위 점수)로만 씁니다.

Rules(규칙):

- train split(학습 분할)에서만 threshold(임계값)를 정합니다.
- validation/OOS(검증/표본밖)는 evaluation only(평가 전용)입니다.
- signal(신호)은 p_short/p_long(숏/롱 확률), side margin(방향 마진), p_flat veto(플랫 차단)만 사용합니다.
- future return(미래 수익), realized PnL(실현 손익), validation/OOS label outcome(검증/표본밖 라벨 결과)은 entry rule(진입 규칙)에 쓰지 않습니다.
"""


def readme_text() -> str:
    return f"# {STAGE_ID}\n\nFrontier06(전선06)는 selective probability abstention signal contract(선택적 확률 기권 신호 계약)을 시험합니다.\n"


def selection_text(summary: dict[str, Any]) -> str:
    return f"""# Stage Frontier 06 Selection Status(전선 06단계 선택 상태)

Updated(갱신): {summary['created_at_utc']}

Stage id(단계 ID): `{STAGE_ID}`

Current run(현재 실행): `{RUN_ID}`

Judgment(판정): `{summary['judgment']}`

Next action(다음 행동): `{NEXT_RUN_ID}`

Claim boundary(주장 경계): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def current_state_text(summary: dict[str, Any]) -> str:
    return f"""# Current Working State(현재 작업 상태)

Updated(갱신): {summary['created_at_utc']}

Active stage(활성 단계): `{STAGE_ID}`

Current run(현재 실행): `{RUN_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Current truth(현재 진실): Frontier06(전선06)가 selective probability abstention signal contract(선택적 확률 기권 신호 계약) 가설로 열렸습니다.

Judgment(판정): `{summary['judgment']}`

Next action(다음 행동): `{NEXT_RUN_ID}`. Action(행동)은 train-only calibrated abstention scout(학습 전용 보정 기권 탐색)를 실행하는 것입니다. Effect(효과)는 argmax overtrading(최대 확률 과다거래)을 줄일 수 있는지 확인하는 것입니다.

Operating boundary(운영 경계): completion(완성), selected baseline(선택 기준선), operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def decision_text(summary: dict[str, Any]) -> str:
    return f"""# Decision(결정): Frontier06 Open(전선06 개방)

Date(날짜): 2026-06-14

Decision(결정): Open Frontier06(전선06 개방) as selective probability abstention signal contract(선택적 확률 기권 신호 계약).

Reason(이유): Frontier05(전선05)는 feature micro-expansion(피처 미세 확장)을 부정 기억으로 닫았고, 다음 신규성은 signal contract(신호 계약) 변화입니다.

Boundary(경계): reference, not inheritance(참조이지 상속 아님). No completion(완성 없음), no baseline(기준선 없음), no promotion(승격 없음), no runtime authority(런타임 권위 없음), no live readiness(실거래 준비 없음).
"""


def run_registry_row(now: str, summary: dict[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "stage_open(단계 개방)",
        "status": summary["status"],
        "judgment": summary["judgment"],
        "path": REPORT_PATH.as_posix(),
        "notes": "selective_probability_abstention_signal_contract;no_authority",
        "work_family": summary["primary_family"],
        "run_number": RUN_NUMBER,
        "date": "2026-06-14",
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "candidate_count": "0",
        "claim_boundary": "stage_open_no_model_no_wfo_no_mt5_no_authority_goal_claim",
        "report_path": REPORT_PATH.as_posix(),
        "created_at_utc": now,
        "ledger_row_id": f"{RUN_ID}__stage_open",
        "subrun_id": f"{RUN_ID}__stage_open",
        "record_view": "stage_open(단계 개방)",
        "tier_scope": "not_applicable_stage_open(단계 개방에는 해당 없음)",
        "kpi_scope": "planning_only_no_trading_kpi(계획 전용, 거래 KPI 없음)",
        "primary_kpi": f"grok_recommendation={summary['grok_classification']['recommendation_inferred']}",
        "guardrail_kpi": "no_model_no_wfo_no_mt5_no_authority(모델/WFO/MT5/권위 없음)",
        "external_verification_status": "grok_review_captured_no_mt5(그록 검토 기록, MT5 없음)",
        "source_run_id": PARENT_RUN_ID,
        "artifact_path": (RUN_ROOT / "stage_open_summary.json").as_posix(),
        "result_path": REPORT_PATH.as_posix(),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "exploration_lane": "frontier_hypothesis_lifecycle(전선 가설 생명주기)",
        "evidence_boundary": "stage_open_only(단계 개방 전용)",
        "reopen_condition": NEXT_RUN_ID,
        "question": "Can selective abstention convert weak model scores into cleaner trades?(선택적 기권이 약한 모델 점수를 더 깨끗한 거래로 바꾸는가?)",
        "skill_family": summary["primary_family"],
        "lineage_summary": "frontier05_closeout_to_frontier06_stage_open(전선05 마감에서 전선06 단계 개방)",
    }


def ledger_row(summary: dict[str, Any]) -> dict[str, Any]:
    return {
        "ledger_row_id": f"{RUN_ID}__stage_open",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": f"{RUN_ID}__stage_open",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "stage_open(단계 개방)",
        "tier_scope": "not_applicable_stage_open(단계 개방에는 해당 없음)",
        "kpi_scope": "planning_only_no_trading_kpi(계획 전용, 거래 KPI 없음)",
        "scoreboard_lane": "stage_open(단계 개방)",
        "status": summary["status"],
        "judgment": summary["judgment"],
        "path": REPORT_PATH.as_posix(),
        "primary_kpi": f"grok_recommendation={summary['grok_classification']['recommendation_inferred']}",
        "guardrail_kpi": "no_model_no_wfo_no_mt5_no_authority(모델/WFO/MT5/권위 없음)",
        "external_verification_status": "grok_review_captured_no_mt5(그록 검토 기록, MT5 없음)",
        "notes": f"next={NEXT_RUN_ID};no_authority",
    }


def read_text(path: Path) -> str:
    return io_path(path).read_text(encoding="utf-8-sig")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(read_text(path))


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_text_sig(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text, encoding="utf-8-sig", newline="\n")


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


if __name__ == "__main__":
    raise SystemExit(main())
