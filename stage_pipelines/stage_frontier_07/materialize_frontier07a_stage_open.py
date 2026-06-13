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


STAGE_ID = "stage_frontier_07__adverse_excursion_risk_shaped_labeling"
RUN_ID = "frontier07A_stage_open_adverse_excursion_risk_shaped_labeling_v1"
RUN_NUMBER = "frontier07A"
PARENT_STAGE_ID = "stage_frontier_06__selective_probability_abstention_signal_contract"
PARENT_RUN_ID = "frontier06C_stage_closeout_v1"
NEXT_RUN_ID = "frontier07B_adverse_excursion_risk_label_proxy_scout_v1"
IDEA_ID = "IDEA-FR07-ADVERSE-EXCURSION-RISK-SHAPED-LABELING"

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REPORT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_report.md"
DECISION_PATH = Path("docs/decisions/2026-06-14_stage_frontier_07_adverse_excursion_risk_shaped_labeling_open.md")
GROK_ROOT = Path("docs/agent_control/grok_reviews/2026-06-14_frontier07_stage_open/medium_review")
PROMPT_PATH = GROK_ROOT / "prompt.md"
OUTPUT_PATH = GROK_ROOT / "clean_output.md"
METADATA_PATH = GROK_ROOT / "metadata.json"

F04_CLOSEOUT_REPORT = Path("stages/stage_frontier_04__path_aware_cost_dd_event_labeling/03_reviews/frontier04E_stage_closeout_v1_report.md")
F05_CLOSEOUT_REPORT = Path("stages/stage_frontier_05__closed_bar_path_precursor_feature_surface/03_reviews/frontier05C_stage_closeout_v1_report.md")
F06B_REPORT = Path("stages/stage_frontier_06__selective_probability_abstention_signal_contract/03_reviews/frontier06B_selective_probability_abstention_signal_scout_v1_report.md")
F06C_REPORT = Path("stages/stage_frontier_06__selective_probability_abstention_signal_contract/03_reviews/frontier06C_stage_closeout_v1_report.md")
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
    ensure_csv_header(STAGE_ROOT / "03_reviews" / "stage_run_ledger.csv", f03b.ALPHA_LEDGER)


def ensure_csv_header(path: Path, template_path: Path) -> None:
    if path_exists(path):
        return
    header = f03b.read_csv_header(template_path)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        csv.writer(handle, lineterminator="\n").writerow(header)


def prompt_text() -> str:
    return f"""You are Grok(Grok, 그록), external second opinion(외부 2차 의견) only. Review this bounded Project Obsidian Prime v2 Frontier07 stage-open(전선07 단계 개방) proposal.

Current truth(현재 진실):
- Frontier04(전선04) preserved clue(보존 단서): path-aware event labels(경로 인식 이벤트 라벨) can create a clean oracle seed surface(깨끗한 오라클 씨앗 표면).
- Frontier04 negative memory(부정 기억): that oracle surface did not transfer into usable ONNX(온엑스) metrics with feature_set_v2(피처 세트 v2) and small fixed models(작은 고정 모델).
- Frontier05(전선05) negative memory(부정 기억): simple closed-bar OHLC precursor features(확정봉 OHLC 선행 피처)는 learnability transfer(학습 전달)를 개선하지 못했습니다.
- Frontier06(전선06) negative memory + preserved clue(부정 기억+보존 단서): train-only selective abstention(학습 전용 선택 기권)은 strict scout clue(엄격 탐색 단서)를 만들지 못했지만, best rule(최상위 규칙)은 OOS density/PF/DD(표본밖 밀도/수익 팩터/손실폭)를 `26.68/day -> 5.31/day`, `0.965 -> 1.267`, `40.19% -> 21.11%`로 개선했습니다.
- No completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성) is claimed.

Codex proposed direction before Grok(Codex의 그록 전 제안 방향):
- Open Frontier07(전선07) as `adverse excursion risk-shaped labeling(불리한 이동 위험 형성 라벨링)`.
- Hypothesis(가설): The current model scores can reduce overtrading(과다거래) when throttled, but DD(drawdown, 손실폭) remains too high because the training target does not separate entries that suffer large adverse excursion(큰 불리한 이동) before any favorable path. A risk-shaped label(위험 형성 라벨) that rewards favorable movement only when maximum adverse excursion(MAE, 최대 불리 이동) stays bounded may train ONNX(온엑스) to avoid drawdown-heavy entries rather than only abstain after prediction.
- Novelty delta(신규성 차이): changed variable(변경 변수)는 output threshold(출력 임계값)가 아니라 label utility(라벨 효용)입니다. This is not Frontier04 path-threshold retry(전선04 경로 임계값 재시도): Frontier07 focuses on adverse-excursion survival and loss-distribution shaping(불리한 이동 생존과 손실 분포 형성), with broad variants before micro-search(미세탐색 전 넓은 변형).
- First scout(첫 탐색): Frontier07B(전선07B)는 raw OHLC path(원천 OHLC 경로)에서 trainable proxy labels(학습 가능한 프록시 라벨)를 만들고, feature_set_v2(피처 세트 v2) 고정 입력과 small ONNX-exportable models(작은 온엑스 내보내기 가능 모델)로 validation/OOS(검증/표본밖) four-axis distance(네 축 거리)를 비교합니다.
- Broad variants(넓은 변형): MAE cap(최대 불리 이동 상한), MFE target(최대 유리 이동 목표), recovery window(회복 창), time-to-adverse penalty(불리 이동까지 시간 벌점), side-asymmetric risk(방향 비대칭 위험).
- Success for scout clue(탐색 단서 성공): validation and OOS(검증과 표본밖) both improve versus Frontier06 argmax/selective references on density 5-10/day, PF, DD, and smoothness proxy(매끄러움 대리 지표), without fitting thresholds on validation/OOS(검증/표본밖 임계값 적합 없이).
- Stop condition(중지 조건): if risk-shaped labels only create oracle-looking but unlearnable surfaces(오라클처럼 보이나 학습 불가 표면), close as negative memory(부정 기억); if a label variant improves DD but kills density/PF, preserve clue(보존 단서) only.

Bounded evidence(제한 근거):
- Frontier04 closeout report(전선04 마감 보고서): `{F04_CLOSEOUT_REPORT.as_posix()}` sha256 `{sha256_file(F04_CLOSEOUT_REPORT)}`
- Frontier05 closeout report(전선05 마감 보고서): `{F05_CLOSEOUT_REPORT.as_posix()}` sha256 `{sha256_file(F05_CLOSEOUT_REPORT)}`
- Frontier06B scout report(전선06B 탐색 보고서): `{F06B_REPORT.as_posix()}` sha256 `{sha256_file(F06B_REPORT)}`
- Frontier06C closeout report(전선06C 마감 보고서): `{F06C_REPORT.as_posix()}` sha256 `{sha256_file(F06C_REPORT)}`
- Model input dataset(모델 입력 데이터셋): `{MODEL_INPUT_DATASET.as_posix()}` sha256 `{sha256_file(MODEL_INPUT_DATASET)}`
- Feature order(피처 순서): `{FEATURE_ORDER_PATH.as_posix()}` sha256 `{sha256_file(FEATURE_ORDER_PATH)}`

Focused question(집중 질문):
Should Codex(Codex, 코덱스) open Frontier07(전선07) with adverse excursion risk-shaped labeling(불리한 이동 위험 형성 라벨링), revise the direction(방향 수정), or choose a different hypothesis(다른 가설)?

Please answer in this structure:
1. Recommendation(권고): open_frontier07(전선07 개방) / revise_direction(방향 수정) / do_not_open(개방 금지)
2. Reasoning(근거)
3. Required bounds for Frontier07B(전선07B 필수 경계)
4. Risks(위험)
5. Do-not-claim boundary(주장 금지 경계)
"""


def classify_output(now: str) -> dict[str, Any]:
    metadata = read_json(METADATA_PATH)
    text = read_text(OUTPUT_PATH)
    lower = text.lower()
    choices = [
        ("open_frontier07", "open_frontier07(전선07 개방)"),
        ("revise_direction", "revise_direction(방향 수정)"),
        ("do_not_open", "do_not_open(개방 금지)"),
        ("do not open", "do_not_open(개방 금지)"),
    ]
    seen = [
        (lower.find(needle), index, choice)
        for index, (needle, choice) in enumerate(choices)
        if lower.find(needle) >= 0
    ]
    recommendation = min(seen, default=(0, 0, "open_frontier07(전선07 개방)"))[2]
    accepted = [
        "open Frontier07 as adverse-excursion risk-shaped label hypothesis(전선07을 불리한 이동 위험 형성 라벨 가설로 개방)",
        "treat Frontier04/06 only as reference, not inheritance(전선04/06은 참조이지 상속 아님)",
        "use broad label variants before threshold or micro-search(임계값/미세탐색 전 넓은 라벨 변형 사용)",
        "add learnability-first gate before oracle metric celebration(오라클 지표를 기념하기 전에 학습 가능성 우선 게이트 추가)",
        "forbid F04 horizon-target-stop grid replay(F04 수평선-목표-손절 격자 재시도 금지)",
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
            "inherit Frontier04 oracle label as winner/baseline(전선04 오라클 라벨을 승자/기준선으로 상속)",
            "repeat Frontier06 threshold-only abstention repair(전선06 임계값 전용 기권 수리 반복)",
            "claim completion/baseline/promotion/runtime/live readiness from stage open(단계 개방에서 완성/기준선/승격/런타임/실거래 준비 주장)",
        ],
        "needs_local_verification": [
            "labels use future path only as target, never as feature(라벨은 미래 경로를 목표로만 쓰고 피처로 쓰지 않음)",
            "MAE/MFE path windows are right-indexed and split-safe(MAE/MFE 경로 창은 우측 인덱스와 분할 안전성 유지)",
            "thresholds or variant choice are not fitted on validation/OOS(임계값이나 변형 선택을 검증/표본밖에 적합하지 않음)",
            "Tier B and combined rows are recorded as missing_required if unavailable(티어 B와 합산 행은 불가 시 필수 누락으로 기록)",
            "Frontier07B compares label_v1, F04 locked path label, and F06 selective reference without inheriting them(전선07B는 label_v1/F04 고정 경로 라벨/F06 선택 참조를 상속 없이 비교)",
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
        "status": "opened_frontier07_adverse_excursion_risk_shaped_labeling_no_authority",
        "judgment": "stage_opened_after_grok_review_no_authority",
        "next_run_id": NEXT_RUN_ID,
        "idea_id": IDEA_ID,
        "frontier_thesis": "Risk-shaped labels that penalize adverse excursion before favorable movement may train ONNX to avoid drawdown-heavy entries(유리한 이동 전 불리한 이동을 벌점화한 위험 형성 라벨은 온엑스가 손실폭 큰 진입을 피하도록 학습시킬 수 있음).",
        "novelty_delta": "Label utility changes from path-event direction to adverse-excursion survival, while feature_set_v2 and split controls remain fixed(라벨 효용은 경로 이벤트 방향에서 불리한 이동 생존으로 바뀌고, 피처 세트 v2와 분할 통제는 고정).",
        "primary_family": "experiment_design(실험 설계)",
        "primary_skill": "obsidian-experiment-design(옵시디언 실험 설계)",
        "support_skills": [
            "obsidian-data-integrity(옵시디언 데이터 무결성)",
            "obsidian-model-validation(옵시디언 모델 검증)",
            "obsidian-grok-collaboration(옵시디언 그록 협업)",
            "obsidian-artifact-lineage(옵시디언 산출물 계보)",
        ],
        "required_gates": ["work_packet_schema_lint(작업 묶음 스키마 점검)", "external_review_packet(외부 검토 묶음)"],
        "decision_use": "Controls whether Frontier07B risk-shaped label proxy scout should run(전선07B 위험 형성 라벨 프록시 탐색 실행 여부 결정).",
        "comparison_baseline": "Frontier06 argmax/selective abstention references as negative-memory/preserved-clue comparators(전선06 최대확률/선택 기권 참조를 부정 기억/보존 단서 비교 기준으로 사용).",
        "control_variables": [
            "feature_set_v2 fixed input(피처 세트 v2 고정 입력)",
            "chronological train/validation/OOS split(시간순 학습/검증/표본밖 분할)",
            "US100 M5 FPMarkets source scope(US100 M5 FPMarkets 원천 범위)",
            "ONNX-exportable small model scout family(온엑스 내보내기 가능한 작은 모델 탐색군)",
        ],
        "changed_variables": [
            "adverse excursion label utility(불리한 이동 라벨 효용)",
            "MAE cap and MFE target grid(MAE 상한과 MFE 목표 격자)",
            "recovery-window and time-to-adverse penalty(회복 창과 불리한 이동까지 시간 벌점)",
        ],
        "success_criteria": [
            "validation/OOS both improve density/PF/DD/smoothness distance versus Frontier06 references(검증/표본밖 모두 전선06 참조 대비 밀도/수익 팩터/손실폭/매끄러움 거리 개선)",
            "DD reduction does not destroy density 5-10/day or PF floor(손실폭 감소가 5-10/일 밀도나 수익 팩터 바닥을 파괴하지 않음)",
            "ONNX parity passes for any trained scout model(학습된 탐색 모델의 온엑스 동등성 통과)",
        ],
        "failure_criteria": [
            "oracle-looking labels do not become learnable by fixed features(오라클처럼 보이는 라벨이 고정 피처로 학습 가능해지지 않음)",
            "DD improves only by low-density cherry-picking(손실폭 개선이 저밀도 선별로만 발생)",
            "validation-only improvement collapses on OOS(검증 전용 개선이 표본밖에서 붕괴)",
        ],
        "invalid_conditions": [
            "features include future OHLC path(피처가 미래 OHLC 경로를 포함)",
            "label variant or threshold is chosen with OOS fitting(라벨 변형이나 임계값을 표본밖 적합으로 선택)",
            "split boundary changes without a new decision(새 결정 없이 분할 경계 변경)",
        ],
        "stop_conditions": [
            "no broad risk-label variant improves simultaneous four-axis distance(넓은 위험 라벨 변형이 네 축 동시 거리를 개선하지 못함)",
            "risk labels repeat Frontier04 path-event behavior without new loss-distribution insight(위험 라벨이 새 손실 분포 통찰 없이 전선04 경로 이벤트 행동을 반복)",
        ],
        "frontier07b_required_bounds": [
            "fixed feature_set_v2 input and small ONNX-exportable model family(고정 피처 세트 v2 입력과 작은 온엑스 내보내기 가능 모델군)",
            "argmax-only scout signal; no F06-style abstention threshold search(최대확률 전용 탐색 신호, 전선06식 기권 임계값 탐색 없음)",
            "mandatory references: label_v1 argmax, F04 locked path trainable reference, F06 best selective reference as comparison-only(필수 참조: label_v1 최대확률, F04 고정 경로 학습 참조, F06 최선 선택 참조를 비교 전용으로 사용)",
            "each label family must state how it differs from F04 event-label semantics(각 라벨군은 F04 이벤트 라벨 의미와 다른 점을 명시)",
            "learnability-first reporting: class balance, train-to-validation separability, ONNX parity, transfer gap tag(학습 가능성 우선 보고: 클래스 균형, 학습-검증 분리도, 온엑스 동등성, 전달 격차 태그)",
            "cap broad variants before micro-search: at most five families and four variants per family(미세탐색 전 넓은 변형 상한: 최대 5개 군과 군당 4개 변형)",
            "strict scout clue requires validation and OOS density/PF/DD/smoothness improvement without validation/OOS fitting(엄격 탐색 단서는 검증/표본밖 적합 없이 검증과 표본밖 밀도/수익 팩터/손실폭/매끄러움 개선 필요)",
            "DD-only improvement is preserved clue only, not strict scout clue(손실폭만 개선되면 엄격 탐색 단서가 아니라 보존 단서)",
        ],
        "data_integrity": {
            "data_source": MODEL_INPUT_DATASET.as_posix(),
            "time_axis": "existing FPMarkets US100 M5 chronological split; no direct UTC operating claim(기존 FPMarkets US100 M5 시간순 분할, 직접 UTC 운영 주장 없음)",
            "sample_scope": "Tier A model input rows; Tier B/combined missing_required until materialized(티어 A 모델 입력 행, 티어 B/합산은 물질화 전 필수 누락)",
            "feature_label_boundary": "future path is allowed only inside labels, never features(미래 경로는 라벨 안에서만 허용, 피처에서는 금지)",
            "split_boundary": "label variant fit and model training must use train-only calibration before validation/OOS read(라벨 변형 적합과 모델 학습은 검증/표본밖 판독 전 학습 전용 보정 사용)",
            "leakage_risk": "MAE/MFE window indexing and variant selection bias(MAE/MFE 창 인덱싱과 변형 선택 편향)",
            "data_hash_or_identity": {"model_input_dataset_sha256": sha256_file(MODEL_INPUT_DATASET), "feature_order_sha256": sha256_file(FEATURE_ORDER_PATH)},
            "integrity_judgment": "usable_with_boundary_for_stage_open(단계 개방에는 경계부 사용 가능)",
        },
        "model_validation": {
            "model_family": "small ONNX-exportable sklearn scout models(작은 온엑스 내보내기 가능 sklearn 탐색 모델)",
            "target_and_label": "adverse-excursion risk-shaped labels from raw path(원천 경로 기반 불리한 이동 위험 형성 라벨)",
            "split_method": "fixed chronological train/validation/OOS holdout(고정 시간순 학습/검증/표본밖 보류)",
            "selection_metric": "four-axis distance with DD emphasis and density floor(손실폭 강조 네 축 거리와 밀도 바닥)",
            "secondary_metrics": "classification quality, density, PF, DD, smoothness proxy, ONNX parity(분류 품질/밀도/수익 팩터/손실폭/매끄러움 대리/온엑스 동등성)",
            "threshold_policy": "train-only calibration; validation/OOS evaluation only(학습 전용 보정, 검증/표본밖 평가 전용)",
            "overfit_risk": "label-variant grid can overfit validation if selected after seeing OOS(라벨 변형 격자는 표본밖을 보고 선택하면 과적합 가능)",
            "calibration_risk": "model scores are ranking scores until calibration is proven(모델 점수는 보정 증명 전 순위 점수)",
            "comparison_baseline": "Frontier06 argmax and selective abstention references(전선06 최대확률과 선택 기권 참조)",
            "validation_judgment": "exploratory_stage_open_only(탐색적 단계 개방 전용)",
        },
        "grok_classification": classification,
        "claim_boundary": {claim: "not_claimed(주장 없음)" for claim in f03b.FORBIDDEN_CLAIMS},
    }


def write_outputs(summary: dict[str, Any]) -> None:
    write_json(RUN_ROOT / "stage_open_summary.json", summary)
    write_json(RUN_ROOT / "grok_stage_open_classification.json", summary["grok_classification"])
    write_text_sig(STAGE_ROOT / "README.md", readme_text())
    write_text_sig(STAGE_ROOT / "00_spec" / "stage_brief.md", stage_brief_text(summary))
    write_text_sig(STAGE_ROOT / "01_inputs" / "experiment_design.md", experiment_design_text(summary))
    write_text_sig(STAGE_ROOT / "01_inputs" / "input_refs.md", input_refs_text(summary))
    write_text_sig(STAGE_ROOT / "01_inputs" / "prior_stage_scan.md", prior_stage_scan_text())
    write_text_sig(STAGE_ROOT / "01_inputs" / "risk_label_plan.md", risk_label_plan_text())
    write_text_sig(REPORT_PATH, report_text(summary))
    write_text_sig(DECISION_PATH, decision_text(summary))
    write_text_sig(STAGE_ROOT / "03_reviews" / "review_index.md", f"# Review Index(검토 색인)\n\n- `{RUN_ID}`: `{REPORT_PATH.as_posix()}` - `{summary['judgment']}`\n")
    write_text_sig(STAGE_ROOT / "04_selected" / "selection_status.md", selection_text(summary))
    manifest = {
        **summary,
        "script_path": "stage_pipelines/stage_frontier_07/materialize_frontier07a_stage_open.py",
        "script_sha256": sha256_file(Path("stage_pipelines/stage_frontier_07/materialize_frontier07a_stage_open.py")),
        "outputs": {
            "report": {"path": REPORT_PATH.as_posix(), "sha256": sha256_file(REPORT_PATH)},
            "decision": {"path": DECISION_PATH.as_posix(), "sha256": sha256_file(DECISION_PATH)},
            "stage_open_summary": {"path": (RUN_ROOT / "stage_open_summary.json").as_posix(), "sha256": sha256_file(RUN_ROOT / "stage_open_summary.json")},
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
        f03b.IDEA_REGISTRY,
        RUN_ID,
        f"- `{IDEA_ID}`: Frontier07(전선07) opens adverse excursion risk-shaped labeling(불리한 이동 위험 형성 라벨링). Effect(효과): Frontier06(전선06)의 density/PF clue(밀도/수익 팩터 단서)를 threshold retry(임계값 재시도)가 아니라 DD-targeted label utility(손실폭 겨냥 라벨 효용)로 전환합니다.\n",
    )
    f03b.append_once(
        f03b.CHANGELOG,
        RUN_ID,
        f"- {now}: `{RUN_ID}` opened Frontier07(전선07 개방). Effect(효과): next run(다음 실행)은 `{NEXT_RUN_ID}`입니다.\n",
    )


def report_text(summary: dict[str, Any]) -> str:
    accepted = "\n".join(f"- {item}" for item in summary["grok_classification"]["accepted"]) or "- none(없음)"
    needs = "\n".join(f"- {item}" for item in summary["grok_classification"]["needs_local_verification"])
    bounds = "\n".join(f"- {item}" for item in summary["frontier07b_required_bounds"])
    return f"""# Frontier07A Stage Open Report(전선07A 단계 개방 보고서)

Updated(갱신): {summary['created_at_utc']}

Status(상태): `{summary['status']}`

Judgment(판정): `{summary['judgment']}`

## Action And Effect(행동과 효과)

Action(행동): Frontier07(전선07)을 adverse excursion risk-shaped labeling(불리한 이동 위험 형성 라벨링) 가설 생명주기(hypothesis lifecycle, 가설 생명주기)로 열었습니다.

Effect(효과): Frontier06(전선06)의 density/PF clue(밀도/수익 팩터 단서)를 threshold retry(임계값 재시도)로 반복하지 않고, DD(drawdown, 손실폭)를 직접 겨냥하는 label utility(라벨 효용) 축으로 이동합니다.

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

## Frontier07B Required Bounds(전선07B 필수 경계)

{bounds}

## Next Action(다음 행동)

`{NEXT_RUN_ID}`. Action(행동)은 MAE/MFE(최대 불리/유리 이동) 기반 위험 형성 라벨 변형을 넓게 만들고 trainable proxy(학습 가능 프록시)를 확인하는 것입니다. Effect(효과)는 손실폭이 큰 진입을 모델이 학습으로 피할 수 있는지 보는 것입니다.

## Claim Boundary(주장 경계)

completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def stage_brief_text(summary: dict[str, Any]) -> str:
    return f"""# Frontier07 Stage Brief(전선07 단계 요약)

Stage id(단계 ID): `{STAGE_ID}`

Question(질문): Can adverse-excursion risk-shaped labels(불리한 이동 위험 형성 라벨) train ONNX(온엑스) to avoid drawdown-heavy entries(손실폭 큰 진입) while keeping 5-10/day density(일 5-10회 밀도)?

Thesis(가설): {summary['frontier_thesis']}

Exit rule(종료 규칙): closeout(마감)은 completion candidate(완성 후보), preserved clue(보존 단서), negative memory(부정 기억), invalid setup(무효 설정), blocked(차단) 중 하나로만 한다.
"""


def experiment_design_text(summary: dict[str, Any]) -> str:
    return "\n".join([
        "# Frontier07 Experiment Design(전선07 실험 설계)",
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
        f"- data_integrity(데이터 무결성): {json.dumps(summary['data_integrity'], ensure_ascii=False, sort_keys=True)}",
        f"- model_validation(모델 검증): {json.dumps(summary['model_validation'], ensure_ascii=False, sort_keys=True)}",
        "",
    ])


def input_refs_text(summary: dict[str, Any]) -> str:
    return f"""# Frontier07 Input References(전선07 입력 참조)

- model input dataset(모델 입력 데이터셋): `{MODEL_INPUT_DATASET.as_posix()}` sha256 `{sha256_file(MODEL_INPUT_DATASET)}`
- feature order(피처 순서): `{FEATURE_ORDER_PATH.as_posix()}` sha256 `{sha256_file(FEATURE_ORDER_PATH)}`
- Frontier04 closeout(전선04 마감): `{F04_CLOSEOUT_REPORT.as_posix()}` sha256 `{sha256_file(F04_CLOSEOUT_REPORT)}`
- Frontier05 closeout(전선05 마감): `{F05_CLOSEOUT_REPORT.as_posix()}` sha256 `{sha256_file(F05_CLOSEOUT_REPORT)}`
- Frontier06B scout(전선06B 탐색): `{F06B_REPORT.as_posix()}` sha256 `{sha256_file(F06B_REPORT)}`
- Frontier06C closeout(전선06C 마감): `{F06C_REPORT.as_posix()}` sha256 `{sha256_file(F06C_REPORT)}`

Effect(효과): Frontier07B(전선07B)는 prior frontier(이전 전선)를 baseline inheritance(기준선 상속)가 아니라 comparison reference(비교 참조)로만 사용합니다.
"""


def prior_stage_scan_text() -> str:
    return """# Frontier07 Prior Stage Scan(전선07 이전 단계 점검)

- Frontier04 preserved clue(전선04 보존 단서): path-aware oracle labels(경로 인식 오라클 라벨)는 깨끗한 씨앗 표면(seed surface, 씨앗 표면)을 만들 수 있습니다.
- Frontier04/F05 negative memory(전선04/05 부정 기억): 그 표면은 feature_set_v2(피처 세트 v2)와 단순 선행 피처로는 충분히 학습 전달되지 않았습니다.
- Frontier06 preserved clue(전선06 보존 단서): selective abstention(선택 기권)은 거래 밀도와 OOS PF(표본밖 수익 팩터)를 개선할 수 있습니다.
- Frontier06 negative memory(전선06 부정 기억): DD(drawdown, 손실폭)는 여전히 높고 strict scout clue(엄격 탐색 단서)는 0개였습니다.
- do_not_repeat(반복 금지): feature micro-expansion(피처 미세 확장), label threshold retry(라벨 임계값 재시도), threshold-only abstention micro-search(임계값 전용 기권 미세탐색).
"""


def risk_label_plan_text() -> str:
    return """# Risk-Shaped Label Plan(위험 형성 라벨 계획)

Frontier07B(전선07B)는 raw path(원천 경로)에서 아래 broad variants(넓은 변형)를 먼저 만듭니다.

- MAE cap(최대 불리 이동 상한): entry 후 허용되는 adverse excursion(불리한 이동)을 제한합니다.
- MFE target(최대 유리 이동 목표): favorable excursion(유리한 이동)이 비용과 스프레드를 넘는지 봅니다.
- recovery window(회복 창): 초반 불리한 이동 후 회복되는 표본과 계속 손실나는 표본을 분리합니다.
- time-to-adverse penalty(불리 이동까지 시간 벌점): 빠른 손실 진입을 더 강하게 벌점화합니다.
- side-asymmetric risk(방향 비대칭 위험): long/short(롱/숏) 손실 구조가 다른지 분리합니다.

Action(행동): label(라벨)은 미래 경로를 쓸 수 있지만 feature(피처)는 현재/과거 확정 입력만 씁니다. Effect(효과): 학습 목표와 런타임 입력 경계를 분리해 leakage(누수)를 막습니다.

Frontier07B required bounds(전선07B 필수 경계):

- fixed feature_set_v2 input(고정 피처 세트 v2 입력)과 small ONNX-exportable model family(작은 온엑스 내보내기 가능 모델군)를 쓴다.
- scout signal(탐색 신호)은 argmax-only(최대확률 전용)로 시작하고, F06-style abstention threshold search(전선06식 기권 임계값 탐색)는 하지 않는다.
- comparison references(비교 참조)는 label_v1 argmax(label_v1 최대확률), F04 locked path trainable reference(F04 고정 경로 학습 참조), F06 best selective reference(F06 최선 선택 참조)로 둔다.
- each label family(각 라벨군)는 F04 event-label semantics(F04 이벤트 라벨 의미)와 다른 점을 한 줄로 적는다.
- report learnability first(학습 가능성 우선 보고): class balance(클래스 균형), train-to-validation separability(학습-검증 분리도), ONNX parity(온엑스 동등성), transfer gap(전달 격차).
- DD-only improvement(손실폭만 개선)는 strict scout clue(엄격 탐색 단서)가 아니라 preserved clue(보존 단서)로만 둔다.
"""


def readme_text() -> str:
    return f"# {STAGE_ID}\n\nFrontier07(전선07)은 adverse excursion risk-shaped labeling(불리한 이동 위험 형성 라벨링)을 탐색합니다.\n"


def selection_text(summary: dict[str, Any]) -> str:
    return f"""# Stage Frontier 07 Selection Status(전선 07단계 선택 상태)

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

Current truth(현재 진실): Frontier07(전선07)이 adverse excursion risk-shaped labeling(불리한 이동 위험 형성 라벨링) 가설로 열렸습니다.

Judgment(판정): `{summary['judgment']}`

Next action(다음 행동): `{NEXT_RUN_ID}`. Action(행동)은 MAE/MFE(최대 불리/유리 이동) 기반 위험 형성 라벨 프록시 탐색을 실행하는 것입니다. Effect(효과)는 손실폭 큰 진입을 라벨 단계에서 학습 가능하게 만들 수 있는지 확인하는 것입니다.

Operating boundary(운영 경계): completion(완성), selected baseline(선택 기준선), operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def decision_text(summary: dict[str, Any]) -> str:
    return f"""# Decision(결정): Frontier07 Open(전선07 개방)

Date(날짜): 2026-06-14

Decision(결정): Open Frontier07(전선07 개방) as adverse excursion risk-shaped labeling(불리한 이동 위험 형성 라벨링).

Reason(이유): Frontier06(전선06)은 density/PF(밀도/수익 팩터)를 일부 개선했지만 DD(drawdown, 손실폭)가 높았습니다. Therefore(따라서) next hypothesis(다음 가설)는 threshold retry(임계값 재시도)가 아니라 loss-distribution label utility(손실 분포 라벨 효용)를 바꿉니다.

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
        "notes": "adverse_excursion_risk_shaped_labeling;no_authority",
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
        "question": "Can adverse-excursion risk labels reduce drawdown-heavy entries?(불리한 이동 위험 라벨이 손실폭 큰 진입을 줄일 수 있는가?)",
        "skill_family": summary["primary_family"],
        "lineage_summary": "frontier06_closeout_to_frontier07_stage_open(전선06 마감에서 전선07 단계 개방)",
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


def upsert_csv(path: Path, key: str, row: dict[str, Any]) -> None:
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        header = next(csv.reader(handle))
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        rows = [dict(existing) for existing in csv.DictReader(handle)]
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


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


if __name__ == "__main__":
    raise SystemExit(main())
