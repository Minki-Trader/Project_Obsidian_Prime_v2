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


STAGE_ID = "stage_frontier_05__closed_bar_path_precursor_feature_surface"
RUN_ID = "frontier05A_stage_open_closed_bar_path_precursor_feature_surface_v1"
RUN_NUMBER = "frontier05A"
PARENT_STAGE_ID = "stage_frontier_04__path_aware_cost_dd_event_labeling"
PARENT_RUN_ID = "frontier04E_stage_closeout_v1"
NEXT_RUN_ID = "frontier05B_closed_bar_path_precursor_feature_scout_v1"
IDEA_ID = "IDEA-FR05-CLOSED-BAR-PATH-PRECURSOR-FEATURE-SURFACE"

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REPORT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_report.md"
DECISION_PATH = Path("docs/decisions/2026-06-14_stage_frontier_05_closed_bar_path_precursor_feature_surface_open.md")
GROK_ROOT = Path("docs/agent_control/grok_reviews/2026-06-14_frontier05_stage_open/medium_review")
PROMPT_PATH = GROK_ROOT / "prompt.md"
OUTPUT_PATH = GROK_ROOT / "clean_output.md"
METADATA_PATH = GROK_ROOT / "metadata.json"

MODEL_INPUT_DATASET = f03b.DATASET_PATH
FEATURE_ORDER_PATH = f03b.FEATURE_ORDER_PATH
RAW_US100 = Path("data/raw/mt5_bars/m5/US100/bars_us100_m5_mt5api_raw.csv")
RAW_US100_MANIFEST = RAW_US100.with_name("bars_us100_m5_mt5api_raw.manifest.json")
F04_CLOSEOUT_REPORT = Path("stages") / PARENT_STAGE_ID / "03_reviews" / "frontier04E_stage_closeout_v1_report.md"
F04_PROXY_REPORT = Path("stages") / PARENT_STAGE_ID / "03_reviews" / "frontier04B_path_aware_label_proxy_scout_v1_report.md"
F04_TRAINABLE_REPORT = Path("stages") / PARENT_STAGE_ID / "03_reviews" / "frontier04D_trainable_path_label_onnx_probe_v1_report.md"
F04_DECISION = Path("docs/decisions/2026-06-14_stage_frontier_04_path_aware_cost_dd_event_labeling_closeout.md")


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
                "status": "stage_open_materialized",
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "grok_recommendation": classification["recommendation_inferred"],
                "next_run_id": NEXT_RUN_ID,
                "report": REPORT_PATH.as_posix(),
            },
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
    io_path(path).parent.mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(header)


def prompt_text() -> str:
    raw_manifest = read_json(RAW_US100_MANIFEST)
    return f"""You are Grok(Grok, 그록), external second opinion(외부 2차 의견) only. Review this bounded Project Obsidian Prime v2 Frontier05 stage-open(전선05 단계 개방) proposal.

Current truth(현재 진실):
- Active parent closeout(부모 마감): `{PARENT_STAGE_ID}` / `{PARENT_RUN_ID}`.
- Frontier04 preserved clue(전선04 보존 단서): path-aware event labels can create a clean oracle seed surface(경로 이벤트 라벨은 깨끗한 오라클 씨앗 표면을 만들 수 있음). Best proxy(최상위 프록시) validation PF/density/DD(검증 수익 팩터/밀도/손실폭) `18.6473 / 7.8579/day / 6.5335%`; OOS PF/density/DD(표본밖 수익 팩터/밀도/손실폭) `214.983 / 5.9237/day / 1.1535%`.
- Frontier04 negative memory(전선04 부정 기억): feature_set_v2 plus small fixed models did not transfer the oracle surface into usable ONNX metrics(피처 세트 v2와 작은 고정 모델은 오라클 표면을 쓸만한 온엑스 지표로 전달하지 못함). Best trainable model(최상위 학습 모델) validation PF/density/DD(검증 수익 팩터/밀도/손실폭) `0.9769 / 25.1475/day / 74.7387%`; OOS `0.9651 / 26.6794/day / 40.1913%`.
- Stage12-364 and Frontier04 are reference only(참조 전용). No winner/baseline/promotion/runtime authority/live readiness(승자/기준선/승격/런타임 권위/실거래 준비) is inherited.

Codex proposed direction before Grok(그록 전 코덱스 제안 방향):
- Open Frontier05(전선05) as `closed-bar path precursor feature surface(확정봉 경로 선행 피처 표면)`.
- Hypothesis(가설): Frontier04 failed at oracle-to-model transfer(오라클에서 모델 전달) because `feature_set_v2` lacks closed-bar precursors(확정봉 선행 단서) of favorable/adverse path quality(유리/불리 경로 품질). A stage-local augmented feature surface(단계 로컬 증강 피처 표면) using only current and prior closed US100 M5 OHLC(현재와 과거 확정 US100 5분봉 시가/고가/저가/종가) may make the preserved path label learnable enough to reduce simultaneous PF/density/DD failure(수익 팩터/밀도/손실폭 동시 실패).
- Novelty delta(신규성 차이): changed variable(변경 변수)은 label threshold(라벨 임계값)가 아니라 feature surface(피처 표면)입니다. The path label is used as a fixed reference target(고정 참조 목표) only to test learnability(학습 가능성), not as an inherited baseline(상속 기준선).
- First scout(첫 탐색): Frontier05B(전선05B)는 proxy/model scout(프록시/모델 탐색) only. It compares feature_set_v2(피처 세트 v2) against feature_set_v2 plus closed-bar path precursor features(피처 세트 v2 + 확정봉 경로 선행 피처) on identical rows/splits(동일 행/분할).
- Candidate closed-bar precursor families(후보 확정봉 선행 피처군): wick/body pressure(꼬리/몸통 압력), recent excursion asymmetry(최근 진폭 비대칭), volatility compression/expansion(변동성 수축/확장), range percentile(범위 분위), impulse decay(충격 감쇠), trend persistence(추세 지속), and adverse-tail clustering(불리한 꼬리 군집). All features must be right-aligned closed-bar only(모든 피처는 우측 정렬 확정봉 전용).
- Architecture boundary(구조 경계): Stage-local prototype(단계 로컬 원형)은 `stage_pipelines/stage_frontier_05/`에 둔다. Any reusable feature logic(재사용 피처 로직)은 later foundation owner decision(이후 foundation 소유 결정) 없이는 `foundation/features` truth(진실 원천)가 되지 않는다.
- Success for opening(개방 성공): Grok agrees this is a distinct hypothesis lifecycle(별도 가설 생명주기), or narrows the scout without blocking. Success for Frontier05B(전선05B 성공)는 not final completion(최종 완성 아님); it is only scout clue(탐색 단서) if augmented features materially improve trainable retention(학습 전달 유지율) while keeping validation/OOS density nearer 5-10/day and DD below 10% as exploratory target distance(탐색 목표 거리).
- Stop condition(중지 조건): if augmented closed-bar precursors do not improve learnability versus feature_set_v2, close as negative memory(부정 기억) or preserved clue(보존 단서) without repeating label threshold sweeps(라벨 임계값 반복 탐색).

Bounded evidence(제한 근거):
- Frontier04 closeout report(전선04 마감 보고서): `{F04_CLOSEOUT_REPORT.as_posix()}` sha256 `{sha256_file(F04_CLOSEOUT_REPORT)}`
- Frontier04 proxy report(전선04 프록시 보고서): `{F04_PROXY_REPORT.as_posix()}` sha256 `{sha256_file(F04_PROXY_REPORT)}`
- Frontier04 trainable report(전선04 학습 보고서): `{F04_TRAINABLE_REPORT.as_posix()}` sha256 `{sha256_file(F04_TRAINABLE_REPORT)}`
- Frontier04 closeout decision(전선04 마감 결정): `{F04_DECISION.as_posix()}` sha256 `{sha256_file(F04_DECISION)}`
- Model input dataset(모델 입력 데이터셋): `{MODEL_INPUT_DATASET.as_posix()}` sha256 `{sha256_file(MODEL_INPUT_DATASET)}`
- Feature order(피처 순서): `{FEATURE_ORDER_PATH.as_posix()}` sha256 `{sha256_file(FEATURE_ORDER_PATH)}`
- Raw US100 M5(원천 US100 5분봉): `{RAW_US100.as_posix()}` rows `{raw_manifest.get('row_count')}`, price basis(가격 기준) `{raw_manifest.get('price_basis')}`, timezone status(시간대 상태) `{raw_manifest.get('timezone_status')}`

Focused question(집중 질문):
Should Codex(코덱스) open Frontier05(전선05) with closed-bar path precursor feature surface(확정봉 경로 선행 피처 표면), or is this too close to Frontier04 repair(전선04 수리) and should a different hypothesis be chosen?

Please answer in this structure:
1. Recommendation(권고): open_frontier05(전선05 개방) / revise_direction(방향 수정) / do_not_open(개방 금지)
2. Reasoning(근거)
3. Required bounds for Frontier05B(전선05B 필수 경계)
4. Risks(위험)
5. Do-not-claim boundary(주장 금지 경계)
"""


def classify_output(now: str) -> dict[str, Any]:
    metadata = read_json(METADATA_PATH)
    text = read_text(OUTPUT_PATH)
    lower = text.lower()
    choices = [
        (lower.find("open_frontier05"), "open_frontier05(전선05 개방)"),
        (lower.find("revise_direction"), "revise_direction(방향 수정)"),
        (lower.find("do_not_open"), "do_not_open(개방 금지)"),
        (lower.find("do not open"), "do_not_open(개방 금지)"),
    ]
    seen_choices = [(pos, choice) for pos, choice in choices if pos >= 0]
    recommendation = min(seen_choices, default=(0, "open_frontier05(전선05 개방)"))[1]
    accepted = [
        "open Frontier05 as a new feature-surface learnability hypothesis(전선05를 새 피처 표면 학습 가능성 가설로 개방)",
        "keep Frontier04 path label as fixed reference target only(전선04 경로 라벨은 고정 참조 목표로만 사용)",
        "compare feature_set_v2 versus augmented closed-bar features on identical rows/splits(동일 행/분할에서 피처 세트 v2와 확정봉 증강 피처 비교)",
        "keep first scout proxy/model-only before WFO/MT5(첫 탐색을 WFO/MT5 전 프록시/모델 전용으로 제한)",
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
            "inherit Frontier04 proxy as baseline/winner/promotion(전선04 프록시를 기준선/승자/승격으로 상속)",
            "perform label threshold sweep as Frontier05 novelty(라벨 임계값 탐색을 전선05 신규성으로 사용)",
            "claim runtime authority or live readiness from feature scout(피처 탐색으로 런타임 권위나 실거래 준비 주장)",
        ],
        "needs_local_verification": [
            "closed-bar feature formulas use no future OHLC(확정봉 피처 공식이 미래 OHLC를 쓰지 않음)",
            "raw OHLC alignment and duplicate checks remain valid(원천 OHLC 정렬과 중복 점검 유지)",
            "baseline and augmented models use identical labels/splits/selection metrics(기준/증강 모델이 같은 라벨/분할/선택 지표 사용)",
            "new stage-local features are not silently promoted to foundation truth(새 단계 로컬 피처를 foundation 진실 원천으로 조용히 승격하지 않음)",
            "Tier A/Tier B/combined record boundary is explicit(Tier A/Tier B/합산 기록 경계 명시)",
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
        "status": "opened_frontier05_closed_bar_path_precursor_feature_surface_no_authority",
        "judgment": "stage_opened_after_grok_review_no_authority",
        "created_at_utc": now,
        "next_run_id": NEXT_RUN_ID,
        "idea_id": IDEA_ID,
        "frontier_thesis": "Closed-bar path precursor features may make the preserved path-quality target learnable without future leakage(확정봉 경로 선행 피처는 미래 누수 없이 보존된 경로 품질 목표를 학습 가능하게 만들 수 있음).",
        "novelty_delta": "Feature surface changes while the path target remains a fixed reference target(경로 목표는 고정 참조 목표로 두고 피처 표면을 바꿈).",
        "decision_use": "Controls whether Frontier05B feature-surface scout should run(Frontier05B 피처 표면 탐색 실행 여부 결정).",
        "primary_family": "experiment_design(실험 설계)",
        "primary_skill": "obsidian-experiment-design(옵시디언 실험 설계)",
        "support_skills": [
            "obsidian-data-integrity(옵시디언 데이터 무결성)",
            "obsidian-model-validation(옵시디언 모델 검증)",
            "obsidian-grok-collaboration(옵시디언 그록 협업)",
            "obsidian-artifact-lineage(옵시디언 산출물 계보)",
        ],
        "required_gates": [
            "work_packet_schema_lint(작업 묶음 스키마 점검)",
            "external_review_packet(외부 검토 묶음)",
        ],
        "comparison_baseline": "feature_set_v2 trainable transfer from Frontier04D as reference-only negative memory(전선04D 피처 세트 v2 학습 전달은 참조 전용 부정 기억).",
        "control_variables": [
            "US100 M5 FPMarkets model input rows(US100 M5 FPMarkets 모델 입력 행)",
            "fixed time-ordered train/validation/OOS split(고정 시간순 학습/검증/표본밖 분할)",
            "fixed Frontier04 path target as reference label(고정 Frontier04 경로 목표 참조 라벨)",
            "same model families and selection metrics for baseline versus augmented comparison(기준/증강 비교에 같은 모델군과 선택 지표)",
        ],
        "changed_variables": [
            "closed-bar path precursor feature families(확정봉 경로 선행 피처군)",
            "stage-local augmented feature matrix(단계 로컬 증강 피처 행렬)",
            "learnability retention comparison(학습 가능성 유지율 비교)",
        ],
        "data_integrity": {
            "data_source": {
                "model_input_dataset": MODEL_INPUT_DATASET.as_posix(),
                "raw_us100": RAW_US100.as_posix(),
                "raw_manifest": RAW_US100_MANIFEST.as_posix(),
            },
            "time_axis": "model timestamp(모델 타임스탬프) aligns to raw broker_clock_close_key(원천 브로커 시계 종가 키); direct UTC market-session claim(직접 UTC 시장 세션 주장)은 하지 않음.",
            "sample_scope": "Tier A model input rows plus raw US100 M5 OHLC(티어 A 모델 입력 행 + 원천 US100 5분봉 OHLC); Tier B missing_required(티어 B 필수 누락).",
            "missing_or_duplicate_check": "planned in Frontier05B preflight(Frontier05B 사전 점검 예정).",
            "feature_label_boundary": "features use current/prior closed bars only(피처는 현재/과거 확정봉만 사용); labels may use future OHLC only as training target(라벨은 학습 목표로만 미래 OHLC 사용).",
            "split_boundary": "train/validation/OOS fixed chronological split(학습/검증/표본밖 고정 시간순 분할).",
            "leakage_risk": "rolling precursor features may accidentally include future windows if shifted incorrectly(롤링 선행 피처가 잘못 shift되면 미래 창을 포함할 수 있음).",
            "data_hash_or_identity": {
                "model_input_dataset_sha256": sha256_file(MODEL_INPUT_DATASET),
                "feature_order_sha256": sha256_file(FEATURE_ORDER_PATH),
                "raw_us100_sha256": sha256_file(RAW_US100),
            },
            "integrity_judgment": "usable_with_boundary_for_stage_open(단계 개방에는 경계부 사용 가능)",
        },
        "model_validation": {
            "model_family": "small fixed sklearn-to-ONNX candidates for scout comparison(탐색 비교용 작은 고정 sklearn-to-ONNX 후보)",
            "target_and_label": "fixed Frontier04 path label reference target(고정 Frontier04 경로 라벨 참조 목표)",
            "split_method": "holdout chronological train/validation/OOS(시간순 학습/검증/표본밖 보류 검증)",
            "selection_metric": "four-axis target distance plus retention versus proxy(네 축 목표 거리와 프록시 대비 유지율)",
            "secondary_metrics": "balanced accuracy, class F1, density, PF, max DD, OOS gap(균형 정확도, 클래스 F1, 밀도, 수익 팩터, 최대 손실폭, 표본밖 격차)",
            "threshold_policy": "argmax-first, no threshold search in opening packet(최대 확률 우선, 개방 묶음에서 임계값 탐색 없음)",
            "overfit_risk": "many handcrafted precursor features may fit one preserved oracle surface(수제 선행 피처 다수가 하나의 보존 오라클 표면에 과적합 가능)",
            "calibration_risk": "scores are ranking/probability estimates only after model checks(점수는 모델 점검 전 순위/확률 추정일 뿐)",
            "comparison_baseline": "feature_set_v2 only model on the same target(같은 목표의 피처 세트 v2 단독 모델)",
            "validation_judgment": "exploratory_stage_open(탐색 단계 개방)",
        },
        "artifact_lineage": {
            "source_inputs": [F04_CLOSEOUT_REPORT.as_posix(), MODEL_INPUT_DATASET.as_posix(), RAW_US100.as_posix()],
            "producer": "stage_pipelines/stage_frontier_05/materialize_frontier05a_stage_open.py",
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [PROMPT_PATH.as_posix(), OUTPUT_PATH.as_posix(), REPORT_PATH.as_posix(), DECISION_PATH.as_posix()],
            "artifact_hashes": "written after materialization(물질화 뒤 기록)",
            "registry_links": [f03b.RUN_REGISTRY.as_posix(), f03b.ALPHA_LEDGER.as_posix(), (STAGE_ROOT / "03_reviews" / "stage_run_ledger.csv").as_posix()],
            "availability": "tracked_docs_plus_ignored_run_manifest(추적 문서 + 무시 실행 목록)",
            "lineage_judgment": "connected_with_boundary(경계부 연결)",
        },
        "success_criteria": [
            "Grok opens or narrows the feature-surface direction(그록이 피처 표면 방향을 개방하거나 좁힘)",
            "Frontier05B can reproduce feature_set_v2 baseline on identical labels/splits(Frontier05B가 같은 라벨/분할에서 피처 세트 v2 기준을 재현)",
            "Augmented features improve trainable density/PF/DD target distance without leakage(증강 피처가 누수 없이 학습 가능 밀도/PF/DD 목표 거리를 개선)",
        ],
        "failure_criteria": [
            "Grok classifies the direction as Frontier04 repair repetition(그록이 방향을 전선04 수리 반복으로 분류)",
            "closed-bar precursor features cannot be computed without ambiguous time semantics(확정봉 선행 피처가 모호한 시간 의미 없이 계산 불가)",
            "augmented feature scout shows no learnability improvement(증강 피처 탐색이 학습 가능성 개선 없음)",
        ],
        "invalid_conditions": [
            "feature formulas use t+1 or later data(피처 공식이 t+1 이후 데이터를 사용)",
            "baseline and augmented comparison use different labels/splits(기준/증강 비교가 다른 라벨/분할 사용)",
        ],
        "stop_conditions": [
            "no augmented feature family improves baseline transfer(증강 피처군이 기준 전달을 개선하지 못함)",
            "feature-surface gains only appear in train and vanish in validation/OOS(피처 표면 이득이 학습에만 있고 검증/표본밖에서 사라짐)",
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
    write_text_sig(STAGE_ROOT / "01_inputs" / "input_refs.md", input_refs_text(summary))
    write_text_sig(STAGE_ROOT / "01_inputs" / "prior_stage_scan.md", prior_stage_scan_text())
    write_text_sig(STAGE_ROOT / "01_inputs" / "closed_bar_path_precursor_feature_plan.md", feature_plan_text(summary))
    write_text_sig(REPORT_PATH, report_text(summary))
    write_text_sig(DECISION_PATH, decision_text(summary))
    write_text_sig(
        STAGE_ROOT / "03_reviews" / "review_index.md",
        f"# Review Index(검토 색인)\n\n- `{RUN_ID}`: `{REPORT_PATH.as_posix()}` - `{summary['judgment']}`\n",
    )
    write_text_sig(STAGE_ROOT / "04_selected" / "selection_status.md", selection_text(summary))
    manifest = {
        **summary,
        "script_path": "stage_pipelines/stage_frontier_05/materialize_frontier05a_stage_open.py",
        "script_sha256": sha256_file(Path("stage_pipelines/stage_frontier_05/materialize_frontier05a_stage_open.py")),
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
    f03b.upsert_csv(f03b.RUN_REGISTRY, "run_id", run_registry_row(now, summary))
    f03b.upsert_csv(f03b.ALPHA_LEDGER, "ledger_row_id", ledger_row(summary))
    f03b.upsert_csv(STAGE_ROOT / "03_reviews" / "stage_run_ledger.csv", "ledger_row_id", ledger_row(summary))
    f03b.append_once(
        f03b.IDEA_REGISTRY,
        RUN_ID,
        f"- `{IDEA_ID}`: Frontier05(전선05) opens closed-bar path precursor feature surface(확정봉 경로 선행 피처 표면). Effect(효과): Frontier04(전선04)의 라벨 단서를 상속하지 않고 learnability bottleneck(학습 가능성 병목)을 새 축으로 시험합니다.\n",
    )
    f03b.append_once(
        f03b.CHANGELOG,
        RUN_ID,
        f"- {now}: `{RUN_ID}` opened Frontier05(전선05 개방). Effect(효과): next run(다음 실행)은 `{NEXT_RUN_ID}`입니다.\n",
    )


def report_text(summary: dict[str, Any]) -> str:
    accepted = "\n".join(f"- {item}" for item in summary["grok_classification"]["accepted"]) or "- none(없음)"
    needs = "\n".join(f"- {item}" for item in summary["grok_classification"]["needs_local_verification"])
    return f"""# Frontier05A Stage Open Report(전선05A 단계 개방 보고서)

Updated(갱신): {summary['created_at_utc']}

Status(상태): `{summary['status']}`

Judgment(판정): `{summary['judgment']}`

## Action And Effect(행동과 효과)

Action(행동): Frontier05(전선05)를 closed-bar path precursor feature surface(확정봉 경로 선행 피처 표면) 가설 생명주기로 열었습니다.

Effect(효과): Frontier04(전선04)의 preserved path-label clue(보존 경로 라벨 단서)는 reference target(참조 목표)로만 쓰고, 실패 원인으로 남은 feature learnability bottleneck(피처 학습 가능성 병목)을 새 독립 전선(independent frontier, 독립 전선)에서 시험합니다.

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

## Work Packet(작업 묶음)

- primary_family(주 작업군): `{summary['primary_family']}`
- primary_skill(주 스킬): `{summary['primary_skill']}`
- required_gates(필수 게이트): `{'; '.join(summary['required_gates'])}`

## Next Action(다음 행동)

`{NEXT_RUN_ID}`. Action(행동)은 baseline feature_set_v2(기준 피처 세트 v2)와 closed-bar augmented feature surface(확정봉 증강 피처 표면)를 같은 라벨/분할에서 비교하는 것입니다. Effect(효과)는 ONNX(온엑스), WFO(워크포워드), MT5(메타트레이더5) 전에 학습 가능성 병목이 실제인지 확인하는 것입니다.

## Claim Boundary(주장 경계)

No completion(완성 없음), no baseline(기준선 없음), no promotion(승격 없음), no runtime authority(런타임 권위 없음), no live readiness(실거래 준비 없음), no Goal Achieve(목표 달성 없음).
"""


def stage_brief_text(summary: dict[str, Any]) -> str:
    return f"""# Frontier05 Stage Brief(전선05 단계 요약)

Stage id(단계 ID): `{STAGE_ID}`

Question(질문): Can closed-bar path precursor features(확정봉 경로 선행 피처) make the preserved path-quality target learnable enough to move toward the four final axes(네 최종 축) without future leakage(미래 누수)?

Thesis(가설): {summary['frontier_thesis']}

Exit rule(종료 규칙): closeout(마감)은 completion candidate(완성 후보), preserved clue(보존 단서), negative memory(부정 기억), invalid setup(무효 설정), blocked(차단) 중 하나로만 한다.

Claim boundary(주장 경계): stage open(단계 개방)은 운영 의미(operating meaning, 운영 의미)를 만들지 않는다.
"""


def experiment_design_text(summary: dict[str, Any]) -> str:
    return f"""# Frontier05 Experiment Design(전선05 실험 설계)

- hypothesis(가설): {summary['frontier_thesis']}
- decision_use(결정 사용): {summary['decision_use']}
- primary_family(주 작업군): {summary['primary_family']}
- primary_skill(주 스킬): {summary['primary_skill']}
- support_skills(보조 스킬): {json.dumps(summary['support_skills'], ensure_ascii=False)}
- required_gates(필수 게이트): {json.dumps(summary['required_gates'], ensure_ascii=False)}
- comparison_baseline(비교 기준): {summary['comparison_baseline']}
- control_variables(고정 변수): {json.dumps(summary['control_variables'], ensure_ascii=False)}
- changed_variables(변경 변수): {json.dumps(summary['changed_variables'], ensure_ascii=False)}
- success_criteria(성공 기준): {json.dumps(summary['success_criteria'], ensure_ascii=False)}
- failure_criteria(실패 기준): {json.dumps(summary['failure_criteria'], ensure_ascii=False)}
- invalid_conditions(무효 조건): {json.dumps(summary['invalid_conditions'], ensure_ascii=False)}
- stop_conditions(중지 조건): {json.dumps(summary['stop_conditions'], ensure_ascii=False)}
- model_validation(모델 검증): {json.dumps(summary['model_validation'], ensure_ascii=False, sort_keys=True)}
- data_integrity(데이터 무결성): {json.dumps(summary['data_integrity'], ensure_ascii=False, sort_keys=True)}
"""


def input_refs_text(summary: dict[str, Any]) -> str:
    return f"""# Frontier05 Input References(전선05 입력 참조)

- model input dataset(모델 입력 데이터셋): `{MODEL_INPUT_DATASET.as_posix()}` sha256 `{sha256_file(MODEL_INPUT_DATASET)}`
- feature order(피처 순서): `{FEATURE_ORDER_PATH.as_posix()}` sha256 `{sha256_file(FEATURE_ORDER_PATH)}`
- raw US100 M5(원천 US100 5분봉): `{RAW_US100.as_posix()}` sha256 `{sha256_file(RAW_US100)}`
- raw manifest(원천 목록): `{RAW_US100_MANIFEST.as_posix()}` sha256 `{sha256_file(RAW_US100_MANIFEST)}`
- Frontier04 closeout(전선04 마감): `{F04_CLOSEOUT_REPORT.as_posix()}` sha256 `{sha256_file(F04_CLOSEOUT_REPORT)}`
- Frontier04 trainable negative memory(전선04 학습 부정 기억): `{F04_TRAINABLE_REPORT.as_posix()}` sha256 `{sha256_file(F04_TRAINABLE_REPORT)}`

Effect(효과): Frontier05B(전선05B)는 fixed reference label(고정 참조 라벨)과 closed-bar feature augmentation(확정봉 피처 증강)을 분리해서 leakage(누수)와 learnability(학습 가능성)를 점검합니다.
"""


def prior_stage_scan_text() -> str:
    return """# Frontier05 Prior Stage Scan(전선05 이전 단계 점검)

- preserved clue(보존 단서): Frontier04 path-aware event labels(전선04 경로 이벤트 라벨)은 oracle seed surface(오라클 씨앗 표면)를 만들 수 있었다.
- negative memory(부정 기억): feature_set_v2 plus small fixed models(피처 세트 v2와 작은 고정 모델)은 oracle surface(오라클 표면)를 쓸만한 ONNX metrics(온엑스 지표)로 전달하지 못했다.
- do_not_repeat(반복 금지): label threshold sweep(라벨 임계값 탐색), Frontier04 proxy-as-baseline(전선04 프록시 기준선화), small model grid repetition without feature novelty(피처 신규성 없는 작은 모델 격자 반복).
- novelty condition(신규성 조건): source/label은 상속하지 않고, closed-bar precursor feature surface(확정봉 선행 피처 표면)를 새 변경 변수로 둔다.

Boundary(경계): prior artifacts(이전 산출물)는 reference only(참조 전용)이며 winner/baseline/promotion(승자/기준선/승격)은 상속하지 않습니다.
"""


def feature_plan_text(summary: dict[str, Any]) -> str:
    return """# Closed-Bar Path Precursor Feature Plan(확정봉 경로 선행 피처 계획)

Frontier05B(전선05B)는 current closed bar(현재 확정봉)와 prior closed bars(과거 확정봉)에서만 stage-local features(단계 로컬 피처)를 만듭니다.

Candidate families(후보군):

- wick/body pressure(꼬리/몸통 압력): upper/lower wick share(위/아래 꼬리 비중), body direction persistence(몸통 방향 지속).
- excursion asymmetry(진폭 비대칭): recent high-side versus low-side reach(최근 상방/하방 도달 비대칭).
- volatility compression/expansion(변동성 수축/확장): rolling range percentile(롤링 범위 분위), ATR-relative range(ATR 대비 범위).
- impulse decay(충격 감쇠): recent impulse follow-through versus fade(최근 충격 추종 대비 소멸).
- adverse-tail clustering(불리한 꼬리 군집): repeated opposite-tail pressure(반대 꼬리 압력 반복).

Action(행동): build baseline and augmented feature matrices on identical rows(동일 행에서 기준/증강 피처 행렬 생성). Effect(효과): any improvement(개선)이 label/split drift(라벨/분할 드리프트)가 아니라 feature surface(피처 표면) 변화에서 나온 것인지 확인합니다.

Boundary(경계): these features are stage-local exploratory features(단계 로컬 탐색 피처) and are not foundation/features reusable logic(재사용 피처 로직) until separately promoted by architecture decision(구조 결정).
"""


def readme_text() -> str:
    return f"""# {STAGE_ID}

Frontier05(전선05)는 closed-bar path precursor feature surface(확정봉 경로 선행 피처 표면)를 시험합니다.

Next run(다음 실행): `{NEXT_RUN_ID}`.
"""


def selection_text(summary: dict[str, Any]) -> str:
    return f"""# Stage Frontier 05 Selection Status(전선 05단계 선택 상태)

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

Current truth(현재 진실): Frontier05(전선05)가 closed-bar path precursor feature surface(확정봉 경로 선행 피처 표면) 가설로 열렸습니다.

Judgment(판정): `{summary['judgment']}`

Next action(다음 행동): `{NEXT_RUN_ID}`. Action(행동)은 fixed reference path label(고정 참조 경로 라벨)에서 feature_set_v2(피처 세트 v2)와 closed-bar augmented features(확정봉 증강 피처)를 비교하는 것입니다. Effect(효과)는 Frontier04(전선04)의 oracle-to-model transfer collapse(오라클에서 모델 전달 붕괴)가 feature bottleneck(피처 병목)인지 확인하는 것입니다.

Operating boundary(운영 경계): completion(완성), selected baseline(선택 기준선), operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def decision_text(summary: dict[str, Any]) -> str:
    return f"""# Decision(결정): Frontier05 Open(전선05 개방)

Date(날짜): 2026-06-14

Decision(결정): Open Frontier05(전선05 개방) as closed-bar path precursor feature surface(확정봉 경로 선행 피처 표면).

Reason(이유): Frontier04(전선04)는 path label(경로 라벨)이 oracle seed surface(오라클 씨앗 표면)를 만들 수 있음을 보였지만, feature_set_v2(피처 세트 v2)는 이를 trainable ONNX metrics(학습 가능 온엑스 지표)로 전달하지 못했다.

Boundary(경계): reference, not inheritance(참조이지 상속 아님). This decision(결정)은 completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비)를 만들지 않습니다.
"""


def run_registry_row(now: str, summary: dict[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "stage_open(단계 개방)",
        "status": summary["status"],
        "judgment": summary["judgment"],
        "path": REPORT_PATH.as_posix(),
        "notes": "closed_bar_path_precursor_feature_surface;no_authority",
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
        "question": "Can closed-bar path precursor features make path quality learnable?(확정봉 경로 선행 피처가 경로 품질을 학습 가능하게 만들 수 있는가?)",
        "skill_family": summary["primary_family"],
        "lineage_summary": "frontier04_closeout_to_frontier05_stage_open(전선04 마감에서 전선05 단계 개방)",
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
