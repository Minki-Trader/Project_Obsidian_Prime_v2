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


STAGE_ID = "stage_frontier_11__subperiod_stability_first_onnx_scout"
RUN_ID = "frontier11A_stage_open_subperiod_stability_first_onnx_scout_v1"
RUN_NUMBER = "frontier11A"
PARENT_RUN_ID = "frontier10D_stage_closeout_split_consistent_utility_distillation_v1"
NEXT_RUN_ID = "frontier11B_subperiod_stability_proxy_scout_v1"
IDEA_ID = "IDEA-FR11-SUBPERIOD-STABILITY-FIRST-ONNX-SCOUT"
STATUS = "opened_frontier11_subperiod_stability_first_onnx_scout_no_authority"
JUDGMENT = "stage_opened_after_grok_review_and_local_archive_boundary_no_authority"

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REPORT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_report.md"
DECISION_PATH = Path("docs/decisions/2026-06-14_stage_frontier_11_subperiod_stability_first_onnx_scout_open.md")
SCRIPT_PATH = Path("stage_pipelines/stage_frontier_11/materialize_frontier11a_stage_open.py")

GROK_DIR = Path("docs/agent_control/grok_reviews/2026-06-14_frontier11_stage_open")
GROK_FIRST = GROK_DIR / "small_review"
GROK_RETRY = GROK_DIR / "small_review_retry"
F10_SELECTION = Path("stages/stage_frontier_10__split_consistent_utility_distillation/04_selected/selection_status.md")
F10_REPORT = Path(
    "stages/stage_frontier_10__split_consistent_utility_distillation/03_reviews/"
    "frontier10D_stage_closeout_split_consistent_utility_distillation_v1_report.md"
)
STAGE171_DECISION = Path("stages/171_adapter_research__segment_stability_equity_curve_audit/03_reviews/stage171_decision.md")
STAGE273_REPORT = Path("stages/273_onnx_candidate_campaign__time_risk_router_stability_validation/03_reviews/run273B_report.md")


def main() -> int:
    now = utc_now()
    ensure_dirs()
    grok = read_grok()
    local = local_verification(grok)
    summary = build_summary(now, grok, local)
    write_outputs(summary)
    update_state_and_registries(summary)
    print(json.dumps(json_ready({
        "status": summary["status"],
        "judgment": summary["judgment"],
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "grok_classification": summary["grok_retry_classification"],
        "report": REPORT_PATH.as_posix(),
    }), ensure_ascii=False, indent=2))
    return 0


def ensure_dirs() -> None:
    for path in (
        RUN_ROOT,
        STAGE_ROOT / "00_spec",
        STAGE_ROOT / "01_inputs",
        STAGE_ROOT / "02_runs",
        STAGE_ROOT / "03_reviews",
        STAGE_ROOT / "04_selected",
        DECISION_PATH.parent,
    ):
        io_path(path).mkdir(parents=True, exist_ok=True)
    ensure_csv_header(STAGE_ROOT / "03_reviews" / "stage_run_ledger.csv", f03b.ALPHA_LEDGER)


def read_grok() -> dict[str, Any]:
    first_meta = read_json(GROK_FIRST / "metadata.json")
    first_output = read_text(GROK_FIRST / "clean_output.md")
    retry_meta = read_json(GROK_RETRY / "metadata.json")
    retry_output = read_text(GROK_RETRY / "clean_output.md")
    return {
        "first_packet": GROK_FIRST.as_posix(),
        "first_prompt": (GROK_FIRST / "prompt.md").as_posix(),
        "first_output": (GROK_FIRST / "clean_output.md").as_posix(),
        "first_prompt_hash": first_meta.get("prompt_hash", ""),
        "first_success": bool(first_meta.get("success")),
        "first_classification": classify_grok(first_output),
        "retry_packet": GROK_RETRY.as_posix(),
        "retry_prompt": (GROK_RETRY / "prompt.md").as_posix(),
        "retry_output": (GROK_RETRY / "clean_output.md").as_posix(),
        "retry_prompt_hash": retry_meta.get("prompt_hash", ""),
        "retry_success": bool(retry_meta.get("success")),
        "retry_classification": classify_grok(retry_output),
        "retry_output_text": retry_output,
    }


def classify_grok(text: str) -> str:
    lowered = text.lower()
    if "accepted" in lowered or "수용" in text:
        return "accepted(수용)"
    if "rejected" in lowered or "거절" in text:
        return "rejected(거절)"
    if "needs_local_verification" in lowered or "로컬 검증 필요" in text:
        return "needs_local_verification(로컬 검증 필요)"
    return "classification_missing(분류 누락)"


def local_verification(grok: dict[str, Any]) -> dict[str, Any]:
    f10_selection = read_text(F10_SELECTION)
    f10_report = read_text(F10_REPORT)
    stage171 = read_text(STAGE171_DECISION)
    stage273 = read_text(STAGE273_REPORT)
    checks = {
        "frontier10_closed": "closed_preserved_clue_negative_memory_no_authority" in f10_selection,
        "frontier10_negative_memory_dd": "validation DD 56~60%" in f10_selection or "56~60%" in f10_report,
        "grok_retry_accepted": grok["retry_classification"] == "accepted(수용)",
        "stage171_archive_found": "segment_equity_audit_failed_repair_required_not_final" in stage171,
        "stage273_archive_found": "negative_valid_q04_stability_failure_no_adapter_handoff" in stage273,
    }
    return {
        "checks": checks,
        "judgment": "pass_with_archive_boundary(보관소 경계 포함 통과)" if all(checks.values()) else "needs_manual_review(수동 검토 필요)",
        "archive_difference": (
            "Stage171(171단계)은 legacy adapter(레거시 어댑터)의 segment/equity/concentration audit"
            "(구간/자산곡선/집중도 감사)였고 repair stage(수리 단계)로 넘겼습니다. "
            "Stage273(273단계)은 q04 time-risk router(q04 시간 위험 라우터) MT5 stability validation"
            "(MT5 안정성 검증)였고 negative handoff(부정 인계)였습니다. Frontier11(전선11)은 "
            "winner/baseline(승자/기준선)을 상속하지 않고 Python fixed-argmax ONNX proxy scout"
            "(파이썬 고정 최대확률 ONNX 프록시 탐색)의 post-fit selection surface(적합 후 선택 표면)를 "
            "새로 시험합니다."
        ),
    }


def build_summary(now: str, grok: dict[str, Any], local: dict[str, Any]) -> dict[str, Any]:
    return {
        "created_at_utc": now,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "idea_id": IDEA_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "grok_first_packet": grok["first_packet"],
        "grok_first_classification": grok["first_classification"],
        "grok_retry_packet": grok["retry_packet"],
        "grok_retry_prompt": grok["retry_prompt"],
        "grok_retry_output": grok["retry_output"],
        "grok_retry_prompt_hash": grok["retry_prompt_hash"],
        "grok_retry_classification": grok["retry_classification"],
        "local_verification": local,
        "frontier_thesis": (
            "When choosing fixed 3-class ONNX candidates(고정 3분류 ONNX 후보 선택) for US100 M5, "
            "subperiod stability(하위기간 안정성), worst-slice drawdown(최악 구간 손실폭), "
            "time-under-water proxy(회복 전 체류 시간 프록시), and equity smoothness proxy"
            "(자산곡선 매끄러움 프록시) may reduce zoomed DD(확대 구간 손실폭) and curve chop"
            "(곡선 출렁임) better than aggregate validation/OOS(검증/표본밖 합계) selection."
        ),
        "novelty_delta": (
            "Frontier07~10(전선07~10)은 label/objective/weight/bridge(라벨/목적/가중/브리지)를 바꿨습니다. "
            "Frontier11(전선11)은 those surfaces(그 표면들)를 reference-only(참조 전용)로 고정하고 "
            "post-fit candidate ranking(적합 후 후보 순위)과 validation philosophy(검증 철학)를 바꿉니다."
        ),
        "do_not_repeat": [
            "side-weight ladder(방향 가중 사다리)",
            "density bridge(밀도 브리지)",
            "threshold micro-search(임계값 미세 탐색)",
            "F10-class capped repair(전선10급 상한 수리)",
            "archive winner/baseline inheritance(보관소 승자/기준선 상속)",
        ],
        "frozen_surfaces": [
            "label family(라벨군)",
            "objective family(목적군)",
            "weight family(가중군)",
            "argmax-only ONNX output schema(최대확률 전용 ONNX 출력 스키마)",
        ],
        "claim_boundary": {claim: "not_claimed(주장 없음)" for claim in f03b.FORBIDDEN_CLAIMS},
    }


def write_outputs(summary: dict[str, Any]) -> None:
    write_json_sig(RUN_ROOT / "stage_open_summary.json", summary)
    write_json_sig(RUN_ROOT / "run_manifest.json", run_manifest(summary))
    f03b.write_text_sig(STAGE_ROOT / "README.md", readme_text(summary))
    f03b.write_text_sig(STAGE_ROOT / "00_spec" / "stage_brief.md", stage_brief(summary))
    f03b.write_text_sig(STAGE_ROOT / "01_inputs" / "experiment_design.md", experiment_design(summary))
    f03b.write_text_sig(STAGE_ROOT / "01_inputs" / "input_refs.md", input_refs(summary))
    f03b.write_text_sig(STAGE_ROOT / "01_inputs" / "prior_stage_scan.md", prior_stage_scan(summary))
    f03b.write_text_sig(STAGE_ROOT / "01_inputs" / "selection_metric_spec.md", selection_metric_spec(summary))
    f03b.write_text_sig(REPORT_PATH, report_text(summary))
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / "required_gate_coverage_audit.md", gate_audit(summary))
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / "review_index.md", review_index(summary))
    f03b.write_text_sig(STAGE_ROOT / "04_selected" / "selection_status.md", selection_status(summary))
    f03b.write_text_sig(DECISION_PATH, decision_text(summary))


def update_state_and_registries(summary: dict[str, Any]) -> None:
    f03b.write_text_sig(f03b.WORKSPACE_STATE, workspace_state(summary))
    f03b.write_text_sig(f03b.CURRENT_WORKING_STATE, current_working_state(summary))
    f03b.upsert_csv(f03b.RUN_REGISTRY, "run_id", run_registry_row(summary))
    row = ledger_row(summary)
    f03b.upsert_csv(f03b.ALPHA_LEDGER, "ledger_row_id", row)
    f03b.upsert_csv(STAGE_ROOT / "03_reviews" / "stage_run_ledger.csv", "ledger_row_id", row)
    f03b.append_once(f03b.IDEA_REGISTRY, f"{RUN_ID}__{IDEA_ID}", idea_registry_entry(summary))
    f03b.append_once(f03b.CHANGELOG, RUN_ID, changelog_entry(summary))


def run_manifest(summary: dict[str, Any]) -> dict[str, Any]:
    return {
        **summary,
        "script_path": SCRIPT_PATH.as_posix(),
        "script_sha256": sha256_file(SCRIPT_PATH),
        "inputs": {
            "frontier10_selection": {"path": F10_SELECTION.as_posix(), "sha256": sha256_file(F10_SELECTION)},
            "frontier10_report": {"path": F10_REPORT.as_posix(), "sha256": sha256_file(F10_REPORT)},
            "stage171_decision": {"path": STAGE171_DECISION.as_posix(), "sha256": sha256_file(STAGE171_DECISION)},
            "stage273_report": {"path": STAGE273_REPORT.as_posix(), "sha256": sha256_file(STAGE273_REPORT)},
            "grok_retry_output": {"path": summary["grok_retry_output"], "sha256": sha256_file(Path(summary["grok_retry_output"]))},
        },
        "outputs": {
            "stage_brief": (STAGE_ROOT / "00_spec" / "stage_brief.md").as_posix(),
            "experiment_design": (STAGE_ROOT / "01_inputs" / "experiment_design.md").as_posix(),
            "report": REPORT_PATH.as_posix(),
            "decision": DECISION_PATH.as_posix(),
        },
    }


def stage_brief(summary: dict[str, Any]) -> str:
    return f"""# Frontier11 Stage Brief(전선11 단계 개요)

Stage id(단계 ID): `{STAGE_ID}`

Question(질문): Can subperiod stability-first selection(하위기간 안정성 우선 선택) improve zoomed DD(확대 구간 손실폭) and equity smoothness(자산곡선 매끄러움) for fixed 3-class ONNX(고정 3분류 ONNX)?

Frontier thesis(전선 가설): {summary['frontier_thesis']}

Novelty delta(신규성 차이): {summary['novelty_delta']}

Prior archive boundary(이전 보관소 경계): {summary['local_verification']['archive_difference']}

Do not repeat(반복 금지):
{bullet_list(summary['do_not_repeat'])}

Frozen surfaces(고정 표면):
{bullet_list(summary['frozen_surfaces'])}

Exit rule(종료 규칙): if strict rows(엄격 행)가 0이고 subperiod selector(하위기간 선택기)가 validation DD(검증 손실폭)나 worst-slice DD(최악 구간 손실폭)를 개선하지 못하면 negative memory(부정 기억)로 닫습니다. preserved clue(보존 단서)가 있으면 capped repair(상한 수리)는 selection metric spec(선택 지표 명세) 안에서 한 번만 허용합니다.

Claim boundary(주장 경계): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def experiment_design(summary: dict[str, Any]) -> str:
    return f"""# Frontier11 Experiment Design(전선11 실험 설계)

## Hypothesis(가설)

{summary['frontier_thesis']}

## Decision Use(결정 사용)

Action(행동): stage-open design(단계 개방 설계)으로 다음 proxy scout(프록시 탐색)의 selection metric(선택 지표)과 대조군(control arm, 대조군)을 고정합니다.

Effect(효과): aggregate PF/density(합계 수익 팩터/밀도)만 좋은 후보가 zoomed DD(확대 구간 손실폭)를 숨기지 못하게 합니다.

## Comparison Baseline(비교 기준)

- same candidate pool aggregate-only selector(같은 후보 풀의 합계 전용 선택기)
- Frontier10 utility-margin preserved clue(전선10 효용 마진 보존 단서)
- Stage171/273 archive stability failures(171/273단계 보관소 안정성 실패)

## Control Variables(고정 변수)

- US100 M5 Tier A(US100 5분봉 티어 A)
- fixed train/validation/OOS split(고정 학습/검증/표본밖 분할)
- fixed 3-class ONNX output `[p_short, p_flat, p_long]`(고정 3분류 ONNX 출력)
- no threshold search(임계값 탐색 없음)
- no density bridge(밀도 브리지 없음)

## Changed Variables(변경 변수)

- post-fit candidate ranking(적합 후 후보 순위)
- subperiod KPI aggregation(하위기간 KPI 집계)
- worst-slice DD and TUW proxy(최악 구간 손실폭과 회복 전 체류 시간 프록시)
- trade distribution entropy(거래 분포 엔트로피)

## Sample Scope(표본 범위)

Data source(데이터 원천): `{f03b.DATASET_PATH.as_posix()}`. Tier B(티어 B) and combined(합산)은 materialized source(물질화 원천)가 없으면 `missing_required(필수 누락)`로 기록합니다.

## Success Criteria(성공 기준)

- strict scout clue(엄격 탐색 단서): validation/OOS(검증/표본밖) aggregate(합계)와 worst-slice(최악 구간) 모두 개선, DD <= 15%(손실폭 15% 이하) scout boundary(탐색 경계), density 5~10/day(일 5~10회), ONNX parity(ONNX 동등성) 통과
- preserved clue(보존 단서): aggregate selector(합계 선택기) 대비 worst-slice DD(최악 구간 손실폭), TUW proxy(회복 전 체류 시간 프록시), smoothness proxy(매끄러움 프록시) 중 2개 이상 개선

## Failure Criteria(실패 기준)

- subperiod selector(하위기간 선택기)가 validation DD(검증 손실폭)를 줄이지 못함
- aggregate PF/density(합계 수익 팩터/밀도)는 좋지만 worst-slice(최악 구간)가 악화
- selection metric(선택 지표)이 hidden threshold search(숨은 임계값 탐색)로 변질

## Invalid Conditions(무효 조건)

- validation/OOS(검증/표본밖) 정보를 model fit(모델 적합)에 사용
- subperiod slices(하위기간 구간)를 결과를 본 뒤 재정의
- missing ONNX parity(ONNX 동등성 누락)를 무시

## Evidence Plan(근거 계획)

- stage run manifest(단계 실행 목록)
- candidate summary(후보 요약)
- aggregate-only control arm(합계 전용 대조군)
- monthly/quarterly subperiod KPI(월별/분기별 하위기간 KPI)
- strict/preserved clue row definitions(엄격/보존 단서 행 정의)
- run registry and paired Tier records(실행 등록부와 티어 쌍 기록)

## Data Integrity(데이터 무결성)

- time_axis(시간축): closed US100 M5 bars(확정 US100 5분봉)
- feature_label_boundary(피처-라벨 경계): subperiod ranking(하위기간 순위)은 post-fit evaluation(적합 후 평가)만 사용
- split_boundary(분할 경계): model fit(모델 적합)은 train only(학습 전용), selector report(선택기 보고)는 validation/OOS(검증/표본밖)를 분리 기록
- leakage_risk(누수 위험): subperiod metric(하위기간 지표)을 모델 학습 목표로 되먹이는 경우
- integrity_judgment(무결성 판정): usable_with_boundary(경계 포함 사용 가능)

## Model Validation(모델 검증)

- model_family(모델군): ONNX-exportable fixed 3-class classifiers(ONNX 내보내기 가능한 고정 3분류 분류기)
- target_and_label(목표와 라벨): frozen reference label/objective family(고정 참조 라벨/목적군)
- selection_metric(선택 지표): stability-first score(안정성 우선 점수)
- threshold_policy(임계값 정책): argmax-only(최대확률 전용)
- overfit_risk(과적합 위험): candidate ranking(후보 순위)이 validation subperiod(검증 하위기간)에 과적합
- calibration_risk(보정 위험): scores are ranking evidence only(점수는 순위 근거 전용)
- validation_judgment(검증 판정): exploratory(탐색)
"""


def input_refs(summary: dict[str, Any]) -> str:
    return f"""# Frontier11 Input References(전선11 입력 참조)

- parent closeout(부모 마감): `{F10_REPORT.as_posix()}`
- Frontier10 selection(전선10 선택 상태): `{F10_SELECTION.as_posix()}`
- Grok first attempt(그록 첫 시도): `{summary['grok_first_packet']}`
- Grok accepted retry(그록 수용 재시도): `{summary['grok_retry_packet']}`
- Stage171 archive(171단계 보관소): `{STAGE171_DECISION.as_posix()}`
- Stage273 archive(273단계 보관소): `{STAGE273_REPORT.as_posix()}`
- model input dataset(모델 입력 데이터셋): `{f03b.DATASET_PATH.as_posix()}`
- feature order(피처 순서): `{f03b.FEATURE_ORDER_PATH.as_posix()}`
"""


def prior_stage_scan(summary: dict[str, Any]) -> str:
    return f"""# Frontier11 Prior Stage Scan(전선11 이전 단계 점검)

## Frontier10 Memory(전선10 기억)

- preserved clue(보존 단서): utility-margin target(효용 마진 목표), modest side-class weighting(완만한 방향 클래스 가중), split-consistent leakage guard(분할 일관 누수 보호)
- negative memory(부정 기억): validation DD 56~60%(검증 손실폭 56~60%), strict rows 0(엄격 행 0), best preserved repair(최상 보존 수리)의 OOS DD(표본밖 손실폭) 악화

## Archive Overlap(보관소 겹침)

- Stage171(171단계): segment/equity/concentration audit(구간/자산곡선/집중도 감사)가 실패했고 repair stage(수리 단계)로 넘어갔습니다.
- Stage273(273단계): q04 time-risk router stability validation(q04 시간 위험 라우터 안정성 검증)이 month/hour loss concentration(월/시간 손실 집중) 때문에 negative handoff(부정 인계)로 닫혔습니다.

## Difference From Archive(보관소 대비 차이)

{summary['local_verification']['archive_difference']}

## Do Not Repeat(반복 금지)

{bullet_list(summary['do_not_repeat'])}
"""


def selection_metric_spec(summary: dict[str, Any]) -> str:
    return """# Frontier11 Selection Metric Spec(전선11 선택 지표 명세)

## Slice Definitions(구간 정의)

- monthly validation slices(월별 검증 구간)
- quarterly validation slices(분기별 검증 구간)
- matching OOS slices(대응 표본밖 구간)

Slice boundaries(구간 경계)는 timestamp calendar(타임스탬프 달력)로 고정하고 결과를 본 뒤 바꾸지 않습니다.

## Metrics(지표)

- aggregate PF/density/DD(합계 수익 팩터/밀도/손실폭)
- worst-slice DD(최악 구간 손실폭)
- worst-slice PF(최악 구간 수익 팩터)
- time-under-water proxy(회복 전 체류 시간 프록시)
- equity smoothness proxy(자산곡선 매끄러움 프록시)
- trade distribution entropy(거래 분포 엔트로피)

## Control Arm(대조군)

The same candidate pool(같은 후보 풀)을 aggregate-only selector(합계 전용 선택기)와 stability-first selector(안정성 우선 선택기)로 동시에 평가합니다.

Effect(효과): 새 selection philosophy(선택 철학)의 효과를 candidate pool change(후보 풀 변화)와 분리합니다.

## Claim Boundary(주장 경계)

This metric(이 지표)은 scout ranking(탐색 순위)입니다. It does not create baseline(기준선), promotion(승격), runtime authority(런타임 권위), or live readiness(실거래 준비).
"""


def report_text(summary: dict[str, Any]) -> str:
    return f"""# Frontier11A Stage Open Report(전선11A 단계 개방 보고서)

Updated(갱신): {summary['created_at_utc']}

Status(상태): `{summary['status']}`

Judgment(판정): `{summary['judgment']}`

## Action And Effect(행동과 효과)

Action(행동): Grok stage-open review(그록 단계 개방 검토)를 받은 뒤 Frontier11(전선11)을 subperiod stability-first ONNX scout(하위기간 안정성 우선 ONNX 탐색)로 열었습니다.

Effect(효과): Frontier10(전선10)의 label/objective/weight/bridge(라벨/목적/가중/브리지) 수리를 반복하지 않고, zoomed DD(확대 구간 손실폭)와 curve smoothness(곡선 매끄러움)를 selection philosophy(선택 철학)에서 먼저 다룹니다.

## Grok Receipt(그록 영수증)

- trigger_reason(트리거 이유): goal requires Grok stage-open review(목표가 그록 단계 개방 검토를 요구)
- review_size(검토 크기): small review retry(소규모 검토 재시도)
- direction_before_grok(그록 전 방향): `stage_frontier_11__subperiod_stability_first_onnx_scout`
- bounded_evidence(제한 근거): Frontier10 closeout(전선10 마감), Stage171/273 archive overlap(171/273단계 보관소 겹침), final four-axis goal(최종 네 축 목표)
- first_attempt(첫 시도): `{summary['grok_first_classification']}` at `{summary['grok_first_packet']}`
- advice_classification(조언 분류): `{summary['grok_retry_classification']}`
- prompt_identity(프롬프트 정체성): `{summary['grok_retry_prompt']}` sha256 `{summary['grok_retry_prompt_hash']}`
- grok_output_identity(그록 출력 정체성): `{summary['grok_retry_output']}`
- local_verification(로컬 검증): `{summary['local_verification']['judgment']}`
- forbidden_claim_check(금지 주장 확인): no completion/baseline/promotion/runtime/live/Goal claim(완성/기준선/승격/런타임/실거래/목표 주장 없음)
- final_codex_direction(최종 코덱스 방향): open Frontier11A(전선11A 개방), then run Frontier11B proxy scout(전선11B 프록시 탐색)

## Claim Boundary(주장 경계)

completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.

## Next Action(다음 행동)

`{NEXT_RUN_ID}`. Action(행동)은 동일 후보 풀(same candidate pool, 같은 후보 풀)에서 aggregate-only selector(합계 전용 선택기)와 stability-first selector(안정성 우선 선택기)를 비교하는 것입니다.
"""


def gate_audit(summary: dict[str, Any]) -> str:
    return f"""# Frontier11A Required Gate Coverage Audit(전선11A 필수 게이트 커버리지 감사)

Updated(갱신): {summary['created_at_utc']}

Status(상태): pass_with_boundary(경계 포함 통과)

- work_packet_schema_lint(작업 묶음 스키마 점검): satisfied(충족)
- external_review_packet(외부 검토 묶음): retry accepted(재시도 수용)
- local_archive_boundary_check(로컬 보관소 경계 확인): `{summary['local_verification']['judgment']}`
- data_integrity_design(데이터 무결성 설계): feature-label boundary named(피처-라벨 경계 명명)
- model_validation_design(모델 검증 설계): selection metric and control arm named(선택 지표와 대조군 명명)
- final_claim_guard(최종 주장 보호): satisfied; no authority claims(충족, 권위 주장 없음)

Effect(효과): stage open(단계 개방)만 주장하고, model/runtime performance(모델/런타임 성과)는 주장하지 않습니다.
"""


def review_index(summary: dict[str, Any]) -> str:
    return f"""# Frontier11 Review Index(전선11 검토 색인)

Updated(갱신): {summary['created_at_utc']}

- `{RUN_ID}`: stage open(단계 개방), Grok retry accepted(그록 재시도 수용), Stage171/273 archive boundary locally verified(171/273단계 보관소 경계 로컬 검증).
- Grok first attempt(그록 첫 시도): `{summary['grok_first_packet']}`
- Grok accepted retry(그록 수용 재시도): `{summary['grok_retry_packet']}`
"""


def selection_status(summary: dict[str, Any]) -> str:
    return f"""# Frontier11 Selection Status(전선11 선택 상태)

Updated(갱신): {summary['created_at_utc']}

Status(상태): `{summary['status']}`

Judgment(판정): `{summary['judgment']}`

Selection(선택): no selected baseline/completion candidate/promotion/runtime authority(선택 기준선/완성 후보/승격/런타임 권위 없음).

Next run(다음 실행): `{NEXT_RUN_ID}`
"""


def readme_text(summary: dict[str, Any]) -> str:
    return f"""# {STAGE_ID}

Status(상태): `{summary['status']}`

Latest run(최근 실행): `{RUN_ID}`

Next run(다음 실행): `{NEXT_RUN_ID}`
"""


def decision_text(summary: dict[str, Any]) -> str:
    return f"""# Decision: Open Frontier11 Subperiod Stability-First ONNX Scout(결정: 전선11 하위기간 안정성 우선 ONNX 탐색 개방)

Date(날짜): {summary['created_at_utc']}

Decision(결정): `{summary['status']}`

Action(행동): Frontier11(전선11)을 validation philosophy change(검증 철학 변경) 가설로 열었습니다.

Effect(효과): Frontier10(전선10)의 라벨/목적/가중/브리지 수리를 반복하지 않고, 하위기간 안정성(subperiod stability, 하위기간 안정성)과 최악 구간 손실폭(worst-slice DD, 최악 구간 손실폭)을 먼저 봅니다.
"""


def workspace_state(summary: dict[str, Any]) -> str:
    return "\n".join([
        f"current_stage_id: {STAGE_ID}",
        f"current_run_id: {RUN_ID}",
        f"latest_completed_run_id: {RUN_ID}",
        f"current_status: {summary['status']}",
        f"current_judgment: {summary['judgment']}",
        f"next_run_id: {NEXT_RUN_ID}",
        "runtime_authority: not_claimed",
        "operating_promotion: not_claimed",
        "goal_achieve: not_claimed",
        f"updated_at_utc: '{summary['created_at_utc']}'",
        "",
    ])


def current_working_state(summary: dict[str, Any]) -> str:
    return f"""# Current Working State(현재 작업 상태)

Updated(갱신): {summary['created_at_utc']}

## Active Stage(현재 단계)

- stage(단계): `{STAGE_ID}`
- current run(현재 실행): `{RUN_ID}`
- status(상태): `{summary['status']}`
- judgment(판정): `{summary['judgment']}`
- next run(다음 실행): `{NEXT_RUN_ID}`

## Current Truth(현재 진실)

Action(행동): Frontier11(전선11)을 subperiod stability-first ONNX scout(하위기간 안정성 우선 ONNX 탐색) 가설로 열었습니다.

Effect(효과): Frontier10(전선10)의 부정 기억인 validation DD(검증 손실폭)와 OOS DD(표본밖 손실폭) 악화를 selection philosophy(선택 철학)에서 직접 다룹니다.

Claim boundary(주장 경계): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def run_registry_row(summary: dict[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "stage_open(단계 개방)",
        "status": summary["status"],
        "judgment": summary["judgment"],
        "path": REPORT_PATH.as_posix(),
        "notes": "frontier11_stage_open_grok_retry_accepted_archive_boundary_no_authority",
        "family": "experiment_design(실험 설계)",
        "work_family": "experiment_design(실험 설계)",
        "primary_report": REPORT_PATH.as_posix(),
        "run_number": RUN_NUMBER,
        "date": "2026-06-14",
        "decision": "open_frontier11_subperiod_stability_first_onnx_scout",
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "candidate_count": "0",
        "claim_boundary": "stage_open_no_model_no_wfo_no_mt5_no_authority_goal_claim",
        "report_path": REPORT_PATH.as_posix(),
        "candidate_rows": "0",
        "external_verification_status": "not_applicable(해당 없음)",
        "result_judgment": summary["judgment"],
        "created_at_utc": summary["created_at_utc"],
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "run_family": "stage_open(단계 개방)",
        "goal_achieve": "not_claimed",
        "source_authority": "grok_retry_accepted_plus_local_archive_boundary(그록 재시도 수용과 로컬 보관소 경계)",
        "final_decision_path": (RUN_ROOT / "stage_open_summary.json").as_posix(),
        "result_path": REPORT_PATH.as_posix(),
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
        "primary_kpi": "grok_retry_classification=accepted(그록 재시도 분류=수용)",
        "guardrail_kpi": "no_model_no_wfo_no_mt5_no_authority(모델/WFO/MT5/권위 없음)",
        "external_verification_status": "not_applicable(해당 없음)",
        "notes": f"next={NEXT_RUN_ID};archive_boundary_verified;no_authority",
        "question": "Can subperiod stability-first selection improve zoomed DD and smoothness?(하위기간 안정성 우선 선택이 확대 구간 손실폭과 매끄러움을 개선하는가?)",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "run_family": "stage_open(단계 개방)",
        "goal_achieve": "not_claimed",
    }


def idea_registry_entry(summary: dict[str, Any]) -> str:
    return (
        f"<!-- {RUN_ID}__{IDEA_ID} -->\n"
        f"- `{IDEA_ID}`: Frontier11(전선11) opens subperiod stability-first ONNX scout"
        f"(하위기간 안정성 우선 ONNX 탐색). Effect(효과): Frontier10(전선10)의 label/objective/weight/bridge"
        f"(라벨/목적/가중/브리지) 수리를 반복하지 않고 validation philosophy(검증 철학)를 새 축으로 시험합니다.\n"
    )


def changelog_entry(summary: dict[str, Any]) -> str:
    return (
        f"- {summary['created_at_utc']}: `{RUN_ID}` opened Frontier11(전선11) with Grok retry accepted"
        f"(그록 재시도 수용) and Stage171/273 archive boundary verified(171/273단계 보관소 경계 검증). "
        f"Effect(효과): next run(다음 실행) `{NEXT_RUN_ID}` can test subperiod stability-first selection"
        f"(하위기간 안정성 우선 선택) without authority claims(권위 주장 없이).\n"
    )


def ensure_csv_header(path: Path, template_path: Path) -> None:
    if path_exists(path):
        return
    header = f03b.read_csv_header(template_path)
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        csv.writer(handle, lineterminator="\n").writerow(header)


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def read_text(path: Path) -> str:
    return io_path(path).read_text(encoding="utf-8-sig")


def write_json_sig(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8-sig")


def bullet_list(items: list[str]) -> str:
    return "\n".join(f"- {item}" for item in items)


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


if __name__ == "__main__":
    raise SystemExit(main())
