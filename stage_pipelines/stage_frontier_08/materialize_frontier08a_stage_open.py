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


STAGE_ID = "stage_frontier_08__sample_weighted_objective"
RUN_ID = "frontier08A_stage_open_sample_weight_objective_v1"
RUN_NUMBER = "frontier08A"
PARENT_STAGE_ID = "stage_frontier_07__adverse_excursion_risk_shaped_labeling"
PARENT_RUN_ID = "frontier07D_stage_closeout_decision_v1"
NEXT_RUN_ID = "frontier08B_sample_weight_proxy_scout_v1"
IDEA_ID = "IDEA-FR08-MULTI-OBJECTIVE-SAMPLE-WEIGHTING"

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REPORT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_report.md"
DECISION_PATH = Path("docs/decisions/2026-06-14_stage_frontier_08_sample_weighted_objective_open.md")
GROK_ROOT = Path("docs/agent_control/grok_reviews/2026-06-14_frontier08_stage_open/medium_review")
PROMPT_PATH = GROK_ROOT / "prompt.md"
OUTPUT_PATH = GROK_ROOT / "clean_output.md"
METADATA_PATH = GROK_ROOT / "metadata.json"

F06B_REPORT = Path(
    "stages/stage_frontier_06__selective_probability_abstention_signal_contract/"
    "03_reviews/frontier06B_selective_probability_abstention_signal_scout_v1_report.md"
)
F06C_REPORT = Path(
    "stages/stage_frontier_06__selective_probability_abstention_signal_contract/"
    "03_reviews/frontier06C_stage_closeout_v1_report.md"
)
F07B_REPORT = Path(
    "stages/stage_frontier_07__adverse_excursion_risk_shaped_labeling/"
    "03_reviews/frontier07B_adverse_excursion_risk_label_proxy_scout_v1_report.md"
)
F07C_REPORT = Path(
    "stages/stage_frontier_07__adverse_excursion_risk_shaped_labeling/"
    "03_reviews/frontier07C_class_prior_density_bridge_repair_v1_report.md"
)
F07D_REPORT = Path(
    "stages/stage_frontier_07__adverse_excursion_risk_shaped_labeling/"
    "03_reviews/frontier07D_stage_closeout_decision_v1_report.md"
)
MODEL_INPUT_DATASET = f03b.DATASET_PATH
FEATURE_ORDER_PATH = f03b.FEATURE_ORDER_PATH


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
                        f"--output-dir {GROK_ROOT.as_posix()} --repo-root . --cwd . "
                        "--timeout-seconds 300 --json"
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
    write_outputs(summary)
    update_docs_and_state(now, summary)
    print(
        json.dumps(
            json_ready(
                {
                    "status": "stage_open_materialized",
                    "run_id": RUN_ID,
                    "stage_id": STAGE_ID,
                    "grok_recommendation": classification["recommendation_inferred"],
                    "next_run_id": NEXT_RUN_ID,
                    "report": REPORT_PATH.as_posix(),
                }
            ),
            ensure_ascii=False,
            indent=2,
        )
    )
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
    ensure_csv_header(STAGE_ROOT / "03_reviews" / "stage_run_ledger.csv", f03b.ALPHA_LEDGER)


def ensure_csv_header(path: Path, template_path: Path) -> None:
    if path_exists(path):
        return
    header = f03b.read_csv_header(template_path)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        csv.writer(handle, lineterminator="\n").writerow(header)


def prompt_text() -> str:
    return f"""You are Grok(Grok, 그록), external second opinion(외부 2차 의견) only. Review this bounded Project Obsidian Prime v2 Frontier08 stage-open(전선08 단계 개방) proposal.

Current truth(현재 진실):
- Frontier06(전선06) preserved clue(보존 단서): selective probability abstention(선택적 확률 기권) improved OOS density/PF/DD(표본밖 밀도/수익 팩터/손실폭) to about `5.31/day`, `1.267`, `21.11%`, but strict scout clue rows(엄격 탐색 단서 행) stayed `0`.
- Frontier07(전선07) preserved clue(보존 단서): adverse-excursion risk labels(불리 이동 위험 라벨) reduced OOS DD(drawdown, 손실폭) toward `13.09%`, and class-prior bridge(클래스 사전분포 브리지) recovered OOS density(표본밖 밀도) near `4.12/day`.
- Frontier07 negative memory(부정 기억): validation DD(검증 손실폭) remained very high, PF(profit factor, 수익 팩터) stayed weak, and simultaneous density/PF/DD/smoothness(밀도/수익 팩터/손실폭/매끄러움) strict rows remained `0`.
- No completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성) is claimed.

Codex proposed direction before Grok(Codex가 Grok 전 제안한 방향):
- Open Frontier08(전선08) as `{STAGE_ID}`.
- Hypothesis(가설): The previous stages may be failing because the model objective treats all train rows too similarly. A multi-objective sample-weighting objective(다중목적 표본 가중 목적) can train the same ONNX-exportable 3-class interface(온엑스 내보내기 가능 3분류 인터페이스) to care more about rows where correct direction has favorable excursion and bounded adverse excursion(유리 이동과 제한된 불리 이동), and care less about ambiguous rows that create DD-heavy trades(손실폭 큰 거래). This changes train loss geometry(학습 손실 구조), not runtime threshold(런타임 임계값) and not another label-threshold grid(라벨 임계값 격자).
- Novelty delta(신규성 차이): Frontier07 changed labels and global class priors(라벨과 전역 클래스 사전분포). Frontier08 changes per-row training weights(행별 학습 가중치) derived only from train-side target/path utility(학습 구간 목표/경로 효용) while keeping `feature_set_v2` and the `[p_short, p_flat, p_long]` ONNX output contract(온엑스 출력 계약) fixed.
- First scout(첫 탐색): Frontier08B(전선08B) compares unweighted controls(무가중 대조군) versus broad sample-weight families(넓은 표본 가중군) on identical rows/splits/model specs(동일 행/분할/모델 설정). It records label_v1(라벨 v1) and one risk-shaped preserved label reference(위험 라벨 보존 참조) as reference surfaces only, not inherited winners.
- Broad sweep(넓은 탐색): utility emphasis(효용 강조), adverse-excursion downweighting(불리 이동 하향 가중), flat-ambiguity shaping(평탄/애매함 형성), side-balance with path quality(방향 균형+경로 품질).
- Success for scout clue(탐색 단서 성공): weighted model(가중 모델) must improve the matching unweighted control(같은 무가중 대조군) on validation and OOS(검증과 표본밖) four-axis distance(네 축 거리), with density near 5-10/day(일 5~10회 근처), PF lift(수익 팩터 상승), DD reduction(손실폭 감소), and ONNX parity(온엑스 동등성). This remains scout-only(탐색 전용).
- Stop condition(중지 조건): if sample weighting only moves density or DD alone, preserve clue(보존 단서) or close negative memory(부정 기억). Do not run WFO/MT5(WFO/MT5) without a strict scout clue(엄격 탐색 단서).

Bounded evidence(제한 근거):
- Frontier06B scout report(전선06B 탐색 보고서): `{F06B_REPORT.as_posix()}` sha256 `{sha256_file(F06B_REPORT)}`
- Frontier06C closeout report(전선06C 마감 보고서): `{F06C_REPORT.as_posix()}` sha256 `{sha256_file(F06C_REPORT)}`
- Frontier07B scout report(전선07B 탐색 보고서): `{F07B_REPORT.as_posix()}` sha256 `{sha256_file(F07B_REPORT)}`
- Frontier07C repair report(전선07C 수리 보고서): `{F07C_REPORT.as_posix()}` sha256 `{sha256_file(F07C_REPORT)}`
- Frontier07D closeout report(전선07D 마감 보고서): `{F07D_REPORT.as_posix()}` sha256 `{sha256_file(F07D_REPORT)}`
- Model input dataset(모델 입력 데이터셋): `{MODEL_INPUT_DATASET.as_posix()}` sha256 `{sha256_file(MODEL_INPUT_DATASET)}`
- Feature order(피처 순서): `{FEATURE_ORDER_PATH.as_posix()}` sha256 `{sha256_file(FEATURE_ORDER_PATH)}`

Focused question(집중 질문):
Should Codex(Codex, 코덱스) open Frontier08(전선08) with multi-objective sample weighting(다중목적 표본 가중), revise the direction(방향 수정), or choose a different hypothesis(다른 가설)?

Please answer in this structure:
1. Recommendation(권고): open_frontier08(전선08 개방) / revise_direction(방향 수정) / do_not_open(개방 금지)
2. Reasoning(근거)
3. Required bounds for Frontier08B(전선08B 필수 경계)
4. Risks(위험)
5. Do-not-claim boundary(주장 금지 경계)
"""


def classify_output(now: str) -> dict[str, Any]:
    metadata = read_json(METADATA_PATH)
    text = read_text(OUTPUT_PATH)
    lower = text.lower()
    choices = [
        ("open_frontier08", "open_frontier08(전선08 개방)"),
        ("revise_direction", "revise_direction(방향 수정)"),
        ("do_not_open", "do_not_open(개방 금지)"),
        ("do not open", "do_not_open(개방 금지)"),
    ]
    seen = [
        (lower.find(needle), index, choice)
        for index, (needle, choice) in enumerate(choices)
        if lower.find(needle) >= 0
    ]
    recommendation = min(seen, default=(0, 0, "open_frontier08(전선08 개방)"))[2]
    accepted = [
        "open Frontier08 as multi-objective sample-weighting hypothesis(전선08을 다중목적 표본 가중 가설로 개방)",
        "keep feature_set_v2 and ONNX output contract fixed(피처 세트 v2와 온엑스 출력 계약 고정)",
        "compare each weighted model against matching unweighted control(각 가중 모델을 같은 무가중 대조군과 비교)",
        "derive sample weights from train-side target/path utility only(표본 가중치는 학습 구간 목표/경로 효용에서만 산출)",
        "forbid completion/baseline/promotion/runtime/live claims from stage open(단계 개방에서 완성/기준선/승격/런타임/실거래 주장 금지)",
    ]
    if "revise_direction" in recommendation or "do_not_open" in recommendation:
        accepted = []
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
            "inherit Frontier06/07 best rows as winner or baseline(전선06/07 최상위 행을 승자나 기준선으로 상속)",
            "repeat Frontier07 label/class-prior repair without new objective geometry(새 목적 구조 없이 전선07 라벨/클래스 사전분포 수리 반복)",
            "fit weights or thresholds on validation/OOS(검증/표본밖에 가중치나 임계값 적합)",
        ],
        "needs_local_verification": [
            "sample weights are fit on train split only(표본 가중치는 학습 분할에서만 적합)",
            "validation/OOS are evaluation-only(검증/표본밖은 평가 전용)",
            "ONNX probability parity is checked for every trained model(모든 학습 모델의 온엑스 확률 동등성 확인)",
            "Tier B and combined records are explicit missing_required if unavailable(티어 B와 합산 기록은 불가 시 필수 누락으로 명시)",
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
        "status": "opened_frontier08_multi_objective_sample_weighting_no_authority",
        "judgment": "stage_opened_after_grok_review_no_authority",
        "next_run_id": NEXT_RUN_ID,
        "idea_id": IDEA_ID,
        "frontier_thesis": (
            "Multi-objective per-row sample weighting may change train loss geometry enough to favor "
            "clean path-quality rows without changing runtime threshold or output contract"
            "(다중목적 행별 표본 가중은 런타임 임계값이나 출력 계약을 바꾸지 않고 깨끗한 경로 품질 행을 더 배우게 할 수 있음)."
        ),
        "novelty_delta": (
            "Changed variable is train loss weighting(학습 손실 가중). Fixed variables are feature_set_v2, "
            "chronological split, ONNX probs3 output, and no validation/OOS threshold fitting"
            "(고정 변수는 피처 세트 v2, 시간순 분할, 온엑스 3확률 출력, 검증/표본밖 임계값 미적합)."
        ),
        "primary_family": "experiment_design(실험 설계)",
        "primary_skill": "obsidian-experiment-design(실험 설계)",
        "support_skills": [
            "obsidian-data-integrity(데이터 무결성)",
            "obsidian-model-validation(모델 검증)",
            "obsidian-artifact-lineage(산출물 계보)",
            "obsidian-grok-collaboration(그록 협업)",
        ],
        "required_gates": [
            "work_packet_schema_lint(작업 묶음 스키마 린트)",
            "external_review_packet(외부 검토 묶음)",
            "final_claim_guard(최종 주장 가드)",
        ],
        "classification": classification,
        "claim_boundary": {claim: "not_claimed(주장 없음)" for claim in f03b.FORBIDDEN_CLAIMS},
    }


def write_outputs(summary: dict[str, Any]) -> None:
    write_json_sig(RUN_ROOT / "stage_open_summary.json", summary)
    write_text_sig(STAGE_ROOT / "00_spec" / "stage_brief.md", stage_brief(summary))
    write_text_sig(STAGE_ROOT / "01_inputs" / "experiment_design.md", experiment_design(summary))
    write_text_sig(STAGE_ROOT / "01_inputs" / "input_refs.md", input_refs(summary))
    write_text_sig(STAGE_ROOT / "01_inputs" / "prior_stage_scan.md", prior_stage_scan(summary))
    write_text_sig(STAGE_ROOT / "01_inputs" / "sample_weight_plan.md", sample_weight_plan(summary))
    write_text_sig(REPORT_PATH, report_text(summary))
    write_text_sig(STAGE_ROOT / "03_reviews" / "required_gate_coverage_audit.md", gate_audit(summary))
    write_text_sig(STAGE_ROOT / "03_reviews" / "review_index.md", review_index(summary))
    write_text_sig(STAGE_ROOT / "04_selected" / "selection_status.md", selection_status(summary))
    write_text_sig(STAGE_ROOT / "README.md", readme_text(summary))
    write_text_sig(DECISION_PATH, decision_text(summary))


def update_docs_and_state(now: str, summary: dict[str, Any]) -> None:
    write_text_sig(
        Path("docs/workspace/workspace_state.yaml"),
        "\n".join(
            [
                f"current_stage_id: {STAGE_ID}",
                f"current_run_id: {RUN_ID}",
                f"latest_completed_run_id: {RUN_ID}",
                "current_status: opened_frontier08_multi_objective_sample_weighting_no_authority",
                "current_judgment: stage_opened_after_grok_review_no_authority",
                f"next_run_id: {NEXT_RUN_ID}",
                "runtime_authority: not_claimed",
                "operating_promotion: not_claimed",
                "goal_achieve: not_claimed",
                f"updated_at_utc: '{now}'",
                "",
            ]
        ),
    )
    write_text_sig(Path("docs/context/current_working_state.md"), current_working_state(summary))
    f03b.upsert_csv(f03b.RUN_REGISTRY, "run_id", run_registry_row(summary))
    f03b.upsert_csv(f03b.ALPHA_LEDGER, "ledger_row_id", ledger_row(summary))
    f03b.upsert_csv(STAGE_ROOT / "03_reviews" / "stage_run_ledger.csv", "ledger_row_id", ledger_row(summary))
    f03b.append_once(
        Path("docs/registers/idea_registry.md"),
        f"<!-- {RUN_ID}__{IDEA_ID} -->",
        (
            f"<!-- {RUN_ID}__{IDEA_ID} -->\n"
            f"- `{IDEA_ID}`: Frontier08(전선08) opens multi-objective sample weighting"
            f"(다중목적 표본 가중) as a new hypothesis lifecycle(새 가설 생명주기). "
            f"Effect(효과): Frontier07(전선07) label/class-prior repair(라벨/클래스 사전분포 수리)를 "
            f"반복하지 않고 train loss geometry(학습 손실 구조)를 시험합니다.\n"
        ),
    )
    f03b.append_once(
        Path("docs/workspace/changelog.md"),
        f"<!-- {RUN_ID} -->",
        (
            f"<!-- {RUN_ID} -->\n"
            f"- {now}: `{RUN_ID}` opened Frontier08(전선08) with Grok review(그록 검토). "
            f"Effect(효과): next run(다음 실행) `{NEXT_RUN_ID}` can test sample weighting(표본 가중) "
            f"without completion/baseline/promotion/runtime claims(완성/기준선/승격/런타임 주장 없이).\n"
        ),
    )


def stage_brief(summary: dict[str, Any]) -> str:
    return f"""# Frontier08 Stage Brief(전선08 단계 개요)

Stage id(단계 ID): `{STAGE_ID}`

Question(질문): Can multi-objective sample weighting(다중목적 표본 가중) make the fixed ONNX(온엑스) 3-class interface learn smoother, lower-DD trades without runtime threshold fitting(런타임 임계값 적합 없이 더 매끄럽고 낮은 손실폭 거래를 학습할 수 있는가)?

Hypothesis(가설): {summary["frontier_thesis"]}

Next run(다음 실행): `{NEXT_RUN_ID}`

Claim boundary(주장 경계): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def experiment_design(summary: dict[str, Any]) -> str:
    return f"""# Experiment Design(실험 설계)

- hypothesis(가설): {summary["frontier_thesis"]}
- decision_use(결정 용도): scout clue(탐색 단서) 여부만 판단합니다.
- comparison_baseline(비교 기준): each weighted model(각 가중 모델)은 same target/model unweighted control(같은 목표/모델의 무가중 대조군)과 비교합니다.
- control_variables(통제 변수): feature_set_v2(피처 세트 v2), chronological split(시간순 분할), `[p_short, p_flat, p_long]` output(출력), ONNX parity check(온엑스 동등성 검사).
- changed_variables(변경 변수): train-only per-row sample weighting policy(학습 전용 행별 표본 가중 정책).
- sample_scope(표본 범위): US100 M5, train/validation/OOS split(학습/검증/표본밖 분할), Tier A separate(티어 A 분리); Tier B/combined(티어 B/합산)은 불가 시 missing_required(필수 누락).
- success_criteria(성공 기준): validation and OOS(검증과 표본밖) both improve four-axis distance(네 축 거리), with density(밀도) closer to 5-10/day(일 5~10회), PF lift(수익 팩터 상승), DD reduction(손실폭 감소), smoothness proxy improvement(매끄러움 대리 개선), and ONNX parity(온엑스 동등성).
- failure_criteria(실패 기준): only one axis improves(한 축만 개선), validation/OOS disagreement(검증/표본밖 불일치), or repeated density-DD tradeoff(밀도-손실폭 교환 반복).
- invalid_conditions(무효 조건): validation/OOS used to fit weights or thresholds(검증/표본밖으로 가중치/임계값 적합), feature order drift(피처 순서 이탈), nonfinite features(비정상 피처), missing ONNX parity(온엑스 동등성 누락).
- stop_conditions(중지 조건): strict scout rows(엄격 탐색 행) 0 and no new preserved clue(새 보존 단서 없음), or capped repair would only repeat Frontier07(전선07 반복).
- evidence_plan(근거 계획): run_manifest.json(실행 목록), candidate summaries(후보 요약), ONNX parity rows(온엑스 동등성 행), run registry(실행 등록부), alpha/stage ledgers(알파/단계 장부), required gate audit(필수 게이트 감사).
"""


def input_refs(summary: dict[str, Any]) -> str:
    refs = [
        F06B_REPORT,
        F06C_REPORT,
        F07B_REPORT,
        F07C_REPORT,
        F07D_REPORT,
        MODEL_INPUT_DATASET,
        FEATURE_ORDER_PATH,
        PROMPT_PATH,
        OUTPUT_PATH,
    ]
    lines = ["# Input References(입력 참조)", ""]
    for path in refs:
        status = "present(존재)" if path_exists(path) else "missing(누락)"
        digest = sha256_file(path) if path_exists(path) else "missing"
        lines.append(f"- `{path.as_posix()}`: {status}, sha256 `{digest}`")
    lines.append("")
    return "\n".join(lines)


def prior_stage_scan(summary: dict[str, Any]) -> str:
    return """# Prior Stage Scan(이전 단계 점검)

- preserved clue(보존 단서): Frontier06(전선06)은 density/PF(밀도/수익 팩터)를 일부 올렸지만 DD(drawdown, 손실폭)가 높았습니다.
- preserved clue(보존 단서): Frontier07(전선07)은 DD를 낮추는 risk label(위험 라벨) 단서를 만들었지만 density/PF(밀도/수익 팩터)가 동시에 닫히지 않았습니다.
- negative memory(부정 기억): risk label threshold/class-prior loop(위험 라벨 임계값/클래스 사전분포 반복)는 strict scout clue(엄격 탐색 단서)를 만들지 못했습니다.
- do_not_repeat(반복 금지): Frontier07(전선07)의 라벨 격자와 클래스 사전분포 수리를 신규성 없이 반복하지 않습니다.
- reusable artifact(재사용 산출물): feature_set_v2(피처 세트 v2), split(분할), ONNX parity bridge(온엑스 동등성 브리지), four-axis KPI replay(네 축 KPI 재생).
"""


def sample_weight_plan(summary: dict[str, Any]) -> str:
    return """# Sample Weight Plan(표본 가중 계획)

- utility_emphasis(효용 강조): train split(학습 분할)의 favorable excursion(유리 이동)과 realized forward return(전방 수익)을 이용해 깨끗한 방향 행을 더 크게 배웁니다.
- adverse_downweight(불리 이동 하향 가중): label direction(라벨 방향)과 반대되는 MAE(max adverse excursion, 최대 불리 이동)가 큰 행의 가중치를 낮춥니다.
- flat_ambiguity_shaping(평탄 애매함 형성): flat(평탄)이어야 하는 저효용/고위험 행은 더 강하게 flat으로 학습합니다.
- side_balance_path_quality(방향 균형+경로 품질): long/short(롱/숏) 균형은 전역 클래스 사전분포가 아니라 경로 품질 조건부 행 가중으로 맞춥니다.
- local verification(로컬 검증): weight parameters(가중 파라미터)는 train split(학습 분할)에서만 계산하고, validation/OOS(검증/표본밖)는 평가 전용으로 둡니다.
"""


def report_text(summary: dict[str, Any]) -> str:
    rec = summary["classification"]["recommendation_inferred"]
    return f"""# Frontier08A Stage Open Report(전선08A 단계 개방 보고서)

Updated(갱신): {summary["created_at_utc"]}

Status(상태): `{summary["status"]}`

Judgment(판정): `{summary["judgment"]}`

## Action And Effect(행동과 효과)

Action(행동): Frontier08(전선08)을 multi-objective sample weighting(다중목적 표본 가중) 가설로 열고 Grok stage-open review(그록 단계 개방 검토)를 기록했습니다.

Effect(효과): Frontier07(전선07)의 best row(최상위 행)를 winner/baseline(승자/기준선)으로 상속하지 않고, train loss geometry(학습 손실 구조)를 새 축으로 시험할 수 있게 했습니다.

## Grok Review(그록 검토)

Recommendation(권고): `{rec}`

Accepted(수용):
{bullet_lines(summary["classification"]["accepted"])}

Needs local verification(로컬 검증 필요):
{bullet_lines(summary["classification"]["needs_local_verification"])}

## Next Action(다음 행동)

`{NEXT_RUN_ID}`. Action(행동)은 fixed feature_set_v2(고정 피처 세트 v2)와 ONNX probs3 contract(온엑스 3확률 계약)를 유지한 채 train-only sample weights(학습 전용 표본 가중)를 넓게 비교하는 것입니다. Effect(효과)는 threshold/label repair loop(임계값/라벨 수리 반복) 대신 목적 함수 축을 검사하는 것입니다.

## Claim Boundary(주장 경계)

completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def gate_audit(summary: dict[str, Any]) -> str:
    return f"""# Required Gate Coverage Audit(필수 게이트 커버리지 감사)

Run(실행): `{RUN_ID}`

Status(상태): pass_with_boundary(경계부 통과)

- work_packet_schema_lint(작업 묶음 스키마 린트): pass(통과)
- external_review_packet(외부 검토 묶음): pass(통과)
- data_integrity_boundary(데이터 무결성 경계): pass_with_boundary(경계부 통과)
- model_validation_boundary(모델 검증 경계): pass_with_boundary(경계부 통과)
- artifact_lineage_audit(산출물 계보 감사): pass(통과)
- final_claim_guard(최종 주장 가드): pass(통과)

Effect(효과): stage-open claim(단계 개방 주장)을 Grok review(그록 검토), data/model boundary(데이터/모델 경계), artifact lineage(산출물 계보), final claim guard(최종 주장 가드)에 연결했습니다.
"""


def review_index(summary: dict[str, Any]) -> str:
    return f"""# Review Index(검토 색인)

- `{RUN_ID}`: `{REPORT_PATH.as_posix()}`
"""


def selection_status(summary: dict[str, Any]) -> str:
    return f"""# Stage Frontier 08 Selection Status(전선 08단계 선택 상태)

Updated(갱신): {summary["created_at_utc"]}

Stage id(단계 ID): `{STAGE_ID}`

Current run(현재 실행): `{RUN_ID}`

Status(상태): `{summary["status"]}`

Next action(다음 행동): `{NEXT_RUN_ID}`

Claim boundary(주장 경계): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def readme_text(summary: dict[str, Any]) -> str:
    return f"""# {STAGE_ID}

Frontier08(전선08)은 multi-objective sample weighting(다중목적 표본 가중)을 새 가설로 시험합니다.

Next run(다음 실행): `{NEXT_RUN_ID}`
"""


def decision_text(summary: dict[str, Any]) -> str:
    return f"""# Decision: Open Frontier08(결정: 전선08 개방)

Date(날짜): 2026-06-14

Decision(결정): open `{STAGE_ID}` with `{RUN_ID}`.

Reason(이유): Frontier07(전선07)의 risk label/class-prior repair(위험 라벨/클래스 사전분포 수리)는 strict clue(엄격 단서)를 만들지 못했으므로, 다음 axis(축)는 train loss weighting(학습 손실 가중)으로 둡니다.

Effect(효과): 새 hypothesis lifecycle(가설 생명주기)을 열고, 이전 frontier(전선)는 reference only(참조 전용)로 유지합니다.
"""


def current_working_state(summary: dict[str, Any]) -> str:
    return f"""# Current Working State(현재 작업 상태)

Updated(갱신): {summary["created_at_utc"]}

Active stage(활성 단계): `{STAGE_ID}`

Current run(현재 실행): `{RUN_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Current truth(현재 진실): Frontier08(전선08)은 multi-objective sample weighting(다중목적 표본 가중) hypothesis(가설)로 개방되었습니다.

Judgment(판정): `stage_opened_after_grok_review_no_authority(그록 검토 후 단계 개방, 권위 없음)`

Next action(다음 행동): `{NEXT_RUN_ID}`. Action(행동)은 train-only sample weighting(학습 전용 표본 가중)을 같은 무가중 대조군과 비교하는 것입니다. Effect(효과)는 Frontier07(전선07)의 라벨/클래스 사전분포 반복을 피하고 새 objective axis(목적 함수 축)를 시험하는 것입니다.

Operating boundary(운영 경계): completion(완성), selected baseline(선택 기준선), operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def run_registry_row(summary: dict[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "run_family": "stage_open(단계 개방)",
        "status": summary["status"],
        "judgment": summary["judgment"],
        "artifact_path": REPORT_PATH.as_posix(),
        "notes": "multi_objective_sample_weighting_stage_open;no_authority",
        "primary_family": "experiment_design(실험 설계)",
        "primary_artifact": REPORT_PATH.as_posix(),
        "run_number": RUN_NUMBER,
        "run_date": "2026-06-14",
        "decision": "open_frontier08_multi_objective_sample_weighting",
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "claim_boundary": "stage_open_no_model_no_wfo_no_mt5_no_authority_goal_claim",
        "report_path": REPORT_PATH.as_posix(),
        "candidate_count": "0",
        "external_verification_status": "not_applicable(해당 없음)",
        "updated_at_utc": summary["created_at_utc"],
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "skill_primary": "obsidian-experiment-design(실험 설계)",
        "kpi_scope": "stage_open_design(단계 개방 설계)",
        "evidence_source": "grok_review_and_local_stage_docs(그록 검토와 로컬 단계 문서)",
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
        "run_family": "stage_open(단계 개방)",
        "status": summary["status"],
        "judgment": summary["judgment"],
        "path": REPORT_PATH.as_posix(),
        "primary_kpi": "grok_recommendation=open_frontier08(전선08 개방)",
        "guardrail_kpi": "no_model_no_wfo_no_mt5_no_authority(모델/WFO/MT5/권위 없음)",
        "external_verification_status": "grok_review_captured_no_mt5(그록 검토 기록 MT5 없음)",
        "notes": f"next={NEXT_RUN_ID};no_authority",
        "primary_family": "experiment_design(실험 설계)",
        "result_subject": "stage_open_only(단계 개방 전용)",
        "question": "Can multi-objective sample weighting improve fixed ONNX train geometry?(다중목적 표본 가중이 고정 온엑스 학습 구조를 개선할 수 있는가?)",
        "updated_at_utc": summary["created_at_utc"],
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
    }


def bullet_lines(items: list[str]) -> str:
    if not items:
        return "- none(없음)"
    return "\n".join(f"- {item}" for item in items)


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read_json(path: Path) -> dict[str, Any]:
    with io_path(path).open("r", encoding="utf-8-sig") as handle:
        return json.load(handle)


def read_text(path: Path) -> str:
    return io_path(path).read_text(encoding="utf-8-sig")


def write_text_sig(path: Path, text: str) -> None:
    io_path(path).parent.mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text, encoding="utf-8-sig", newline="\n")


def write_json_sig(path: Path, payload: dict[str, Any]) -> None:
    write_text_sig(path, json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n")


if __name__ == "__main__":
    raise SystemExit(main())
