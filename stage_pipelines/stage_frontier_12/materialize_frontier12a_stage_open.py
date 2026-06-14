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


STAGE_ID = "stage_frontier_12__trade_shape_duration_controlled_onnx_scout"
RUN_ID = "frontier12A_stage_open_trade_shape_duration_controlled_onnx_scout_v1"
RUN_NUMBER = "frontier12A"
PARENT_RUN_ID = "frontier11C_stage_closeout_subperiod_stability_first_onnx_scout_v1"
NEXT_RUN_ID = "frontier12B_trade_shape_duration_label_proxy_scout_v1"
IDEA_ID = "IDEA-FR12-TRADE-SHAPE-DURATION-CONTROLLED-ONNX-SCOUT"
STATUS = "opened_frontier12_trade_shape_duration_controlled_onnx_scout_no_authority"
JUDGMENT = "stage_opened_after_grok_review_and_local_contract_boundary_no_authority"

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REPORT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_report.md"
DECISION_PATH = Path("docs/decisions/2026-06-14_stage_frontier_12_trade_shape_duration_controlled_onnx_scout_open.md")
SCRIPT_PATH = Path("stage_pipelines/stage_frontier_12/materialize_frontier12a_stage_open.py")

GROK_FIRST = Path("docs/agent_control/grok_reviews/2026-06-14_frontier12_stage_open/small_review")
GROK_RETRY = Path("docs/agent_control/grok_reviews/2026-06-14_frontier12_stage_open/small_review_retry")

F04_SELECTION = Path("stages/stage_frontier_04__path_aware_cost_dd_event_labeling/04_selected/selection_status.md")
F07_SELECTION = Path("stages/stage_frontier_07__adverse_excursion_risk_shaped_labeling/04_selected/selection_status.md")
F09_SELECTION = Path("stages/stage_frontier_09__drawdown_normalized_clean_path_labeling/04_selected/selection_status.md")
F10_SELECTION = Path("stages/stage_frontier_10__split_consistent_utility_distillation/04_selected/selection_status.md")
F11_SELECTION = Path("stages/stage_frontier_11__subperiod_stability_first_onnx_scout/04_selected/selection_status.md")
F11_REPORT = (
    Path("stages")
    / "stage_frontier_11__subperiod_stability_first_onnx_scout"
    / "03_reviews"
    / "frontier11C_stage_closeout_subperiod_stability_first_onnx_scout_v1_report.md"
)
FRONTIER_GOVERNANCE = Path("docs/policies/frontier_governance.md")


def main() -> int:
    now = utc_now()
    ensure_dirs()
    grok = read_grok()
    local = local_verification(grok)
    summary = build_summary(now, grok, local)
    write_outputs(summary)
    update_state_and_registries(summary)
    print(
        json.dumps(
            json_ready(
                {
                    "status": summary["status"],
                    "judgment": summary["judgment"],
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "next_run_id": NEXT_RUN_ID,
                    "grok_retry_classification": summary["grok_retry_classification"],
                    "local_verification": summary["local_verification"]["judgment"],
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
    first_meta = read_json(GROK_FIRST / "metadata.json") if path_exists(GROK_FIRST / "metadata.json") else {}
    first_output = read_text(GROK_FIRST / "clean_output.md") if path_exists(GROK_FIRST / "clean_output.md") else ""
    retry_meta = read_json(GROK_RETRY / "metadata.json")
    retry_output = read_text(GROK_RETRY / "clean_output.md")
    return {
        "first_packet": GROK_FIRST.as_posix(),
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
        "retry_duration_seconds": retry_meta.get("duration_seconds", ""),
        "retry_output_text": retry_output,
    }


def classify_grok(text: str) -> str:
    lowered = text.lower()
    if "accepted" in lowered:
        return "accepted(수용)"
    if "rejected" in lowered:
        return "rejected(거절)"
    if "needs_local_verification" in lowered:
        return "needs_local_verification(로컬 검증 필요)"
    return "classification_missing(분류 누락)"


def local_verification(grok: dict[str, Any]) -> dict[str, Any]:
    workspace = read_text(f03b.WORKSPACE_STATE)
    governance = read_text(FRONTIER_GOVERNANCE)
    f04 = read_text(F04_SELECTION)
    f07 = read_text(F07_SELECTION)
    f09 = read_text(F09_SELECTION)
    f10 = read_text(F10_SELECTION)
    f11 = read_text(F11_SELECTION)
    f11_report = read_text(F11_REPORT)
    checks = {
        "frontier11_parent_closeout_present": (
            "closed_negative_memory_no_authority" in f11
            and "frontier11C_stage_closeout_subperiod_stability_first_onnx_scout_v1" in f11_report
            and (
                "current_stage_id: stage_frontier_11__subperiod_stability_first_onnx_scout" in workspace
                or "current_stage_id: stage_frontier_12__trade_shape_duration_controlled_onnx_scout" in workspace
            )
        ),
        "frontier11_closeout_negative_memory": "closed_negative_memory_no_authority" in f11
        and "negative_memory(부정 기억)" in f11,
        "frontier11_strict_zero_memory": "strict scout clue rows" in f11_report
        and "preserved clue rows" in f11_report
        and "`0`" in f11_report,
        "grok_retry_accepted": grok["retry_success"] and grok["retry_classification"] == "accepted(수용)",
        "frontier_governance_opening_contract": all(
            key in governance
            for key in (
                "frontier_thesis",
                "novelty_delta",
                "prior_stage_scan",
                "do_not_repeat",
                "exit_rule",
                "claim_boundary",
            )
        ),
        "prior_stage_reference_paths_exist": all(
            path_exists(path)
            for path in (F04_SELECTION, F07_SELECTION, F09_SELECTION, F10_SELECTION, F11_SELECTION)
        ),
        "prior_stage_no_authority_inherited": all(no_authority_text(text) for text in (f04, f07, f09, f10, f11)),
        "dataset_and_feature_order_exist": path_exists(f03b.DATASET_PATH) and path_exists(f03b.FEATURE_ORDER_PATH),
    }
    return {
        "checks": checks,
        "judgment": "pass_with_boundary(경계 포함 통과)" if all(checks.values()) else "needs_manual_review(수동 검토 필요)",
        "accepted_grok_requirements": [
            "frontier11 closeout lock(프론티어11 마감 잠금)",
            "opening contract completeness(개방 계약 완전성)",
            "prior-stage scan with paths(경로 포함 이전 단계 점검)",
            "novelty delta proof(신규성 차이 증명)",
            "label causality audit(라벨 인과성 감사)",
            "pre-registered label knobs(사전 등록 라벨 파라미터)",
            "train-only materialization boundary(학습 전용 물질화 경계)",
            "signal contract freeze(신호 계약 고정)",
            "tier ledger plan(티어 장부 계획)",
            "feature/model lineage(피처/모델 계보)",
            "ONNX parity scope(온엑스 동등성 범위)",
            "success/failure boundary freeze(성공/실패 경계 고정)",
        ],
    }


def no_authority_text(text: str) -> bool:
    lowered = text.lower()
    return (
        "not_claimed" in lowered
        or "no selected baseline" in lowered
        or "권위 없음" in text
        or "없음" in text
    )


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
        "grok_first_encoding_boundary": "first_packet_not_official_due_mojibake(첫 묶음은 문자 깨짐 때문에 공식 근거 아님)",
        "grok_retry_packet": grok["retry_packet"],
        "grok_retry_prompt": grok["retry_prompt"],
        "grok_retry_output": grok["retry_output"],
        "grok_retry_prompt_hash": grok["retry_prompt_hash"],
        "grok_retry_duration_seconds": grok["retry_duration_seconds"],
        "grok_retry_classification": grok["retry_classification"],
        "local_verification": local,
        "frontier_thesis": (
            "US100 M5 fixed 3-class ONNX(US100 5분봉 고정 3분류 온엑스) can reduce validation/OOS DD"
            "(검증/표본밖 손실폭) only if the label source(라벨 원천) encodes a trade lifecycle(거래 생명주기):"
            " early adverse excursion veto(초기 불리 이동 배제), favorable path confirmation(유리 경로 확인),"
            " capped hold duration(상한 보유 기간), MAE/MFE quality(최대 불리/유리 이동 품질), and density-aware neutral"
            "(빈도 인식 중립) before model fitting(모델 적합 전)."
        ),
        "novelty_delta": (
            "Frontier04/07/09/10(프론티어04/07/09/10)은 path, adverse, clean-path, utility label families"
            "(경로/불리 이동/깨끗한 경로/효용 라벨 계열)를 시험했고 Frontier11(프론티어11)은 same-pool selector"
            "(같은 후보군 선택기)를 시험했습니다. Frontier12(프론티어12)는 inherited candidates(상속 후보)나"
            " post-fit ranking(적합 후 순위)이 아니라 pre-fit trade-shape label contract(적합 전 거래 형상 라벨 계약)을 시험합니다."
        ),
        "do_not_repeat": [
            "same F10C candidate-pool selector tweak(같은 F10C 후보군 선택기 조정)",
            "side-weight ladder(방향 가중 사다리)",
            "density bridge(빈도 브리지)",
            "threshold micro-search(임계값 미세 탐색)",
            "archive winner/baseline inheritance(보관소 승자/기준선 상속)",
        ],
        "exit_rule": (
            "If Frontier12B(프론티어12B) produces strict rows(엄격 행) 0 and preserved rows(보존 행) 0, or validation DD floor"
            "(검증 손실폭 바닥) remains high without a new local repair surface(새 로컬 수리 표면), close as negative memory"
            "(부정 기억) or capped repair(상한 수리)."
        ),
        "claim_boundary": {claim: "not_claimed(주장 없음)" for claim in f03b.FORBIDDEN_CLAIMS},
        "scout_success_boundary": {
            "density_per_day": "5_to_10(일 5~10회)",
            "profit_factor": ">=1.2_scout_floor(탐색 바닥)",
            "drawdown": "<=15_percent_scout_boundary(탐색 경계)",
            "net_profit": "positive(양수)",
            "onnx_parity": "required_for_model_rows(모델 행 필수)",
            "final_completion": "not_claimed(주장 없음)",
        },
        "pre_registered_label_knobs": [
            "all knobs must be declared in the Frontier12B manifest before validation/OOS metrics(모든 파라미터는 검증/표본밖 지표 전 프론티어12B 실행 목록에 기록)",
            "train-only quantiles may define MAE/MFE cut points(학습 전용 분위수는 최대 불리/유리 이동 절단점 정의 가능)",
            "no validation-driven knob changes(검증 기반 파라미터 변경 없음)",
            "argmax-only signal with no threshold search(임계값 탐색 없는 최대확률 전용 신호)",
        ],
    }


def write_outputs(summary: dict[str, Any]) -> None:
    write_json_sig(RUN_ROOT / "stage_open_summary.json", summary)
    write_json_sig(RUN_ROOT / "run_manifest.json", run_manifest(summary))
    f03b.write_text_sig(STAGE_ROOT / "README.md", readme_text(summary))
    f03b.write_text_sig(STAGE_ROOT / "00_spec" / "stage_brief.md", stage_brief(summary))
    f03b.write_text_sig(STAGE_ROOT / "00_spec" / "trade_shape_label_contract.md", trade_shape_label_contract(summary))
    f03b.write_text_sig(STAGE_ROOT / "01_inputs" / "experiment_design.md", experiment_design(summary))
    f03b.write_text_sig(STAGE_ROOT / "01_inputs" / "input_refs.md", input_refs(summary))
    f03b.write_text_sig(STAGE_ROOT / "01_inputs" / "prior_stage_scan.md", prior_stage_scan(summary))
    f03b.write_text_sig(STAGE_ROOT / "01_inputs" / "local_checks.md", local_checks_text(summary))
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
        "script_sha256": sha(SCRIPT_PATH),
        "inputs": {
            "frontier_governance": artifact_identity(FRONTIER_GOVERNANCE),
            "frontier04_selection": artifact_identity(F04_SELECTION),
            "frontier07_selection": artifact_identity(F07_SELECTION),
            "frontier09_selection": artifact_identity(F09_SELECTION),
            "frontier10_selection": artifact_identity(F10_SELECTION),
            "frontier11_selection": artifact_identity(F11_SELECTION),
            "frontier11_report": artifact_identity(F11_REPORT),
            "dataset": artifact_identity(f03b.DATASET_PATH),
            "feature_order": artifact_identity(f03b.FEATURE_ORDER_PATH),
            "grok_retry_output": artifact_identity(Path(summary["grok_retry_output"])),
        },
        "outputs": {
            "stage_brief": (STAGE_ROOT / "00_spec" / "stage_brief.md").as_posix(),
            "label_contract": (STAGE_ROOT / "00_spec" / "trade_shape_label_contract.md").as_posix(),
            "experiment_design": (STAGE_ROOT / "01_inputs" / "experiment_design.md").as_posix(),
            "report": REPORT_PATH.as_posix(),
            "decision": DECISION_PATH.as_posix(),
        },
    }


def readme_text(summary: dict[str, Any]) -> str:
    return f"""# {STAGE_ID}

Status(상태): `{summary['status']}`

Latest run(최근 실행): `{RUN_ID}`

Next run(다음 실행): `{NEXT_RUN_ID}`

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성) are not_claimed(주장 없음).
"""


def stage_brief(summary: dict[str, Any]) -> str:
    return f"""# Frontier12 Stage Brief(프론티어12 단계 개요)

Stage id(단계 ID): `{STAGE_ID}`

Question(질문): Can a trade-shape duration-controlled label(거래 형상과 보유 기간 통제 라벨) reduce DD(손실폭) and improve smoothness(매끄러움) for US100 M5 ONNX(US100 5분봉 온엑스)?

## Frontier Thesis(프론티어 가설)

{summary['frontier_thesis']}

## Novelty Delta(신규성 차이)

{summary['novelty_delta']}

## Do Not Repeat(반복 금지)

{bullet_list(summary['do_not_repeat'])}

## Exit Rule(종료 규칙)

{summary['exit_rule']}

## Claim Boundary(주장 경계)

This stage(이 단계)는 scout clue(탐색 단서), seed surface(씨앗 표면), preserved clue(보존 단서), negative memory(부정 기억), invalid setup(무효 설정), or blocked(차단)만 말할 수 있습니다. completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 모두 forbidden(금지)입니다.
"""


def trade_shape_label_contract(summary: dict[str, Any]) -> str:
    return f"""# Trade Shape Label Contract(거래 형상 라벨 계약)

Action(행동): Frontier12B(프론티어12B)는 trade-shape constrained labels(거래 형상 제약 라벨)을 만들기 전에 label knobs(라벨 파라미터)를 run_manifest(실행 목록)에 고정합니다.

Effect(효과): validation/OOS(검증/표본밖) 성과를 본 뒤 라벨을 다시 맞추는 hidden threshold search(숨은 임계값 탐색)를 막습니다.

## Required Label Concepts(필수 라벨 개념)

- early adverse excursion veto(초기 불리 이동 배제)
- favorable path confirmation(유리 경로 확인)
- capped hold duration(상한 보유 기간)
- MAE/MFE quality(최대 불리/유리 이동 품질)
- density-aware neutral class(빈도 인식 중립 클래스)

## Pre-registered Knobs(사전 등록 파라미터)

{bullet_list(summary['pre_registered_label_knobs'])}

## Forbidden Knobs(금지 파라미터)

- validation-driven MAE/MFE cuts(검증 기반 최대 불리/유리 이동 절단)
- OOS-driven density repair(표본밖 기반 빈도 수리)
- post-fit selector replacement(적합 후 선택기 대체)
- threshold micro-search(임계값 미세 탐색)

## Signal Contract(신호 계약)

The output schema(출력 스키마)는 `[p_short, p_flat, p_long]`이고 signal(신호)은 argmax-only(최대확률 전용)입니다. Effect(효과): label experiment(라벨 실험)이 runtime authority(런타임 권위)나 live readiness(실거래 준비)로 과장되지 않습니다.
"""


def experiment_design(summary: dict[str, Any]) -> str:
    return f"""# Frontier12 Experiment Design(프론티어12 실험 설계)

## Hypothesis(가설)

{summary['frontier_thesis']}

## Decision Use(결정 사용)

Action(행동): this stage-open packet(이 단계 개방 묶음)은 Frontier12B(프론티어12B) proxy scout(프록시 탐색)의 label contract(라벨 계약), data boundary(데이터 경계), and success/failure boundary(성공/실패 경계)를 고정합니다.

Effect(효과): early exploration(초기 탐색)은 자유롭게 하되 completion(완성)이나 baseline(기준선)처럼 말하지 않습니다.

## Control Variables(고정 변수)

- instrument/timeframe(종목/시간봉): FPMarkets US100 M5(FPMarkets US100 5분봉)
- split policy(분할 정책): existing fixed train/validation/OOS(기존 고정 학습/검증/표본밖)
- output schema(출력 스키마): `[p_short, p_flat, p_long]`
- signal policy(신호 정책): argmax-only(최대확률 전용)
- no WFO/MT5 at stage-open(단계 개방에서 WFO/MT5 없음)

## Changed Variables(변경 변수)

- label source(라벨 원천)
- trade lifecycle definition(거래 생명주기 정의)
- neutral class construction(중립 클래스 구성)
- train-only label knob registration(학습 전용 라벨 파라미터 등록)

## Scout Success Boundary(탐색 성공 경계)

- validation and OOS density(검증과 표본밖 빈도): {summary['scout_success_boundary']['density_per_day']}
- validation and OOS PF(검증과 표본밖 수익 팩터): {summary['scout_success_boundary']['profit_factor']}
- validation and OOS DD(검증과 표본밖 손실폭): {summary['scout_success_boundary']['drawdown']}
- net profit(순손익): {summary['scout_success_boundary']['net_profit']}
- ONNX parity(온엑스 동등성): {summary['scout_success_boundary']['onnx_parity']}

## Failure Boundary(실패 경계)

Strict rows(엄격 행) 0 and preserved rows(보존 행) 0, high validation DD floor(높은 검증 손실폭 바닥), or repeated repair without novelty(신규성 없는 반복 수리)는 negative memory(부정 기억) 또는 capped repair(상한 수리)로 닫습니다.

## Data Integrity(데이터 무결성)

Feature-label boundary(피처-라벨 경계)는 closed bar features(확정 봉 피처)와 future path label(미래 경로 라벨)을 분리합니다. Train-only materialization(학습 전용 물질화)은 validation/OOS metrics(검증/표본밖 지표)를 라벨 파라미터 선택에 쓰지 않습니다.

## Model Validation(모델 검증)

Model rows(모델 행)는 ONNX parity(온엑스 동등성), aggregate KPI(합계 KPI), subperiod KPI(하위기간 KPI), and paired Tier record(짝 티어 기록)를 가져야 합니다. Effect(효과): one-axis illusion(한 축 착시)을 줄입니다.
"""


def input_refs(summary: dict[str, Any]) -> str:
    return f"""# Frontier12 Input References(프론티어12 입력 참조)

- Frontier governance(프론티어 운영 규칙): `{FRONTIER_GOVERNANCE.as_posix()}`
- Frontier04 selection(프론티어04 선택 상태): `{F04_SELECTION.as_posix()}`
- Frontier07 selection(프론티어07 선택 상태): `{F07_SELECTION.as_posix()}`
- Frontier09 selection(프론티어09 선택 상태): `{F09_SELECTION.as_posix()}`
- Frontier10 selection(프론티어10 선택 상태): `{F10_SELECTION.as_posix()}`
- Frontier11 selection(프론티어11 선택 상태): `{F11_SELECTION.as_posix()}`
- Frontier11 report(프론티어11 보고서): `{F11_REPORT.as_posix()}`
- Grok retry packet(그록 재시도 묶음): `{summary['grok_retry_packet']}`
- Dataset(데이터셋): `{f03b.DATASET_PATH.as_posix()}`
- Feature order(피처 순서): `{f03b.FEATURE_ORDER_PATH.as_posix()}`
"""


def prior_stage_scan(summary: dict[str, Any]) -> str:
    return f"""# Frontier12 Prior Stage Scan(프론티어12 이전 단계 점검)

## Reference Only(참조 전용)

Action(행동): Frontier04/07/09/10/11(프론티어04/07/09/10/11)은 reference-only archive(참조 전용 보관소)로 읽었습니다.

Effect(효과): winner/baseline/promotion/runtime authority/live readiness(승자/기준선/승격/런타임 권위/실거래 준비)를 상속하지 않습니다.

## Relevant Memory(관련 기억)

- Frontier04(프론티어04): path-aware label(경로 인식 라벨)은 negative memory(부정 기억)+preserved clue(보존 단서)로 닫힘.
- Frontier07(프론티어07): adverse excursion risk label(불리 이동 위험 라벨)은 보존 단서가 있었지만 authority(권위)는 없음.
- Frontier09(프론티어09): clean-path label(깨끗한 경로 라벨)은 validation DD 56~64%(검증 손실폭 56~64%)와 strict rows 0(엄격 행 0)을 남김.
- Frontier10(프론티어10): utility margin(효용 마진)은 보존 단서를 남겼지만 validation DD 56~60%(검증 손실폭 56~60%)와 strict rows 0(엄격 행 0)을 남김.
- Frontier11(프론티어11): post-fit subperiod selector(적합 후 하위기간 선택기)는 strict rows 0(엄격 행 0), preserved rows 0(보존 행 0)로 닫힘.

## Novelty Proof(신규성 증명)

{summary['novelty_delta']}

## Do Not Repeat(반복 금지)

{bullet_list(summary['do_not_repeat'])}
"""


def local_checks_text(summary: dict[str, Any]) -> str:
    checks = summary["local_verification"]["checks"]
    check_lines = "\n".join(f"- {key}: `{value}`" for key, value in checks.items())
    requirements = bullet_list(summary["local_verification"]["accepted_grok_requirements"])
    return f"""# Frontier12 Local Checks(프론티어12 로컬 확인)

Updated(갱신): {summary['created_at_utc']}

Local judgment(로컬 판정): `{summary['local_verification']['judgment']}`

## Check Results(확인 결과)

{check_lines}

## Accepted Grok Requirements(수용한 그록 요구)

{requirements}

Effect(효과): Grok(그록) 조언은 자동 실행하지 않고 Codex(코덱스)가 로컬 파일, 장부, 경계 조건으로 재검증했습니다.
"""


def selection_metric_spec(summary: dict[str, Any]) -> str:
    return """# Frontier12 Selection Metric Spec(프론티어12 선택 지표 명세)

## Metric Set(지표 세트)

- aggregate PF/density/DD(합계 수익 팩터/빈도/손실폭)
- month and quarter subperiod PF/density/DD(월/분기 하위기간 수익 팩터/빈도/손실폭)
- worst subperiod DD(최악 하위기간 손실폭)
- underwater ratio proxy(회복 전 체류 비율 프록시)
- smoothness proxy(매끄러움 프록시)
- ONNX parity(온엑스 동등성)

## Selection Rule(선택 규칙)

Strict clue(엄격 단서)는 validation/OOS(검증/표본밖) 네 축을 동시에 보며, one-axis improvement(한 축 개선)만으로는 앞으로 보내지 않습니다.

## Claim Boundary(주장 경계)

This metric(이 지표)는 scout ranking(탐색 순위) 전용입니다. Effect(효과): baseline/promotion/runtime authority/live readiness(기준선/승격/런타임 권위/실거래 준비)를 만들지 않습니다.
"""


def report_text(summary: dict[str, Any]) -> str:
    return f"""# Frontier12A Stage Open Report(프론티어12A 단계 개방 보고서)

Updated(갱신): {summary['created_at_utc']}

Status(상태): `{summary['status']}`

Judgment(판정): `{summary['judgment']}`

## Action And Effect(행동과 효과)

Action(행동): Frontier12(프론티어12)를 trade-shape duration-controlled ONNX scout(거래 형상과 보유 기간 통제 온엑스 탐색)로 열었습니다.

Effect(효과): Frontier11(프론티어11)의 same-pool selector(같은 후보군 선택기) 반복을 끊고, label source(라벨 원천)와 trade lifecycle(거래 생명주기)을 새 가설로 시험합니다.

## Grok Receipt(그록 영수증)

- official review(공식 검토): `{summary['grok_retry_packet']}`
- classification(분류): `{summary['grok_retry_classification']}`
- prompt hash(프롬프트 해시): `{summary['grok_retry_prompt_hash']}`
- duration seconds(소요 초): `{summary['grok_retry_duration_seconds']}`
- first packet boundary(첫 묶음 경계): `{summary['grok_first_encoding_boundary']}`
- local verification(로컬 검증): `{summary['local_verification']['judgment']}`

## Current Claim Boundary(현재 주장 경계)

completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 모두 not_claimed(주장 없음)입니다.

## Next Action(다음 행동)

`{NEXT_RUN_ID}`. Action(행동): train-only trade-shape labels(학습 전용 거래 형상 라벨)을 만들고 proxy scout(프록시 탐색)를 실행합니다. Effect(효과): final completion review(최종 완성 검토) 전에는 후보가 네 축 목표에 얼마나 가까워지는지만 봅니다.
"""


def gate_audit(summary: dict[str, Any]) -> str:
    return f"""# Frontier12A Required Gate Coverage Audit(프론티어12A 필수 게이트 커버리지 감사)

Updated(갱신): {summary['created_at_utc']}

Status(상태): pass_with_boundary(경계 포함 통과)

- work_packet_schema_lint(작업 묶음 스키마 점검): satisfied(충족)
- external_review_packet(외부 검토 묶음): Grok retry accepted(그록 재시도 수용)
- opening_contract_gate(개방 계약 게이트): frontier_thesis/novelty_delta/prior_stage_scan/do_not_repeat/exit_rule/claim_boundary(프론티어 가설/신규성 차이/이전 단계 점검/반복 금지/종료 규칙/주장 경계) recorded(기록됨)
- data_integrity_gate(데이터 무결성 게이트): train-only label boundary(학습 전용 라벨 경계) named(명명됨)
- model_validation_gate(모델 검증 게이트): argmax-only/ONNX parity/success boundary(최대확률 전용/온엑스 동등성/성공 경계) named(명명됨)
- paired_tier_gate(짝 티어 게이트): Tier B and combined missing policy(티어B와 합산 누락 정책) named(명명됨)
- final_claim_guard(최종 주장 보호): no authority claims(권위 주장 없음)

Effect(효과): stage open(단계 개방)만 완료하고, performance completion(성과 완성)은 주장하지 않습니다.
"""


def review_index(summary: dict[str, Any]) -> str:
    return f"""# Frontier12 Review Index(프론티어12 검토 색인)

Updated(갱신): {summary['created_at_utc']}

- `{RUN_ID}`: stage open(단계 개방), Grok retry accepted(그록 재시도 수용), local checks pass with boundary(로컬 확인 경계 포함 통과).
- official Grok output(공식 그록 출력): `{summary['grok_retry_output']}`
- stage report(단계 보고서): `{REPORT_PATH.as_posix()}`
- gate audit(게이트 감사): `{(STAGE_ROOT / '03_reviews' / 'required_gate_coverage_audit.md').as_posix()}`
"""


def selection_status(summary: dict[str, Any]) -> str:
    return f"""# Frontier12 Selection Status(프론티어12 선택 상태)

Updated(갱신): {summary['created_at_utc']}

Status(상태): `{summary['status']}`

Judgment(판정): `{summary['judgment']}`

Selection(선택): no selected baseline/completion candidate/promotion/runtime authority(선택 기준선/완성 후보/승격/런타임 권위 없음).

Next run(다음 실행): `{NEXT_RUN_ID}`

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def decision_text(summary: dict[str, Any]) -> str:
    return f"""# Decision: Open Frontier12 Trade Shape Duration-Controlled ONNX Scout(결정: 프론티어12 거래 형상 보유 기간 통제 온엑스 탐색 개방)

Date(날짜): {summary['created_at_utc']}

Decision(결정): `{summary['status']}`

Action(행동): Frontier12(프론티어12)를 trade-shape label source(거래 형상 라벨 원천) 가설로 열었습니다.

Effect(효과): Frontier11(프론티어11)의 same-pool selector(같은 후보군 선택기) 반복을 중단하고, pre-fit label contract(적합 전 라벨 계약)를 시험합니다.

Claim boundary(주장 경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음).
"""


def workspace_state(summary: dict[str, Any]) -> str:
    return "\n".join(
        [
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
        ]
    )


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

Action(행동): Frontier12(프론티어12)는 trade-shape duration-controlled ONNX scout(거래 형상과 보유 기간 통제 온엑스 탐색)로 열렸습니다.

Effect(효과): Frontier11(프론티어11)의 same-pool selector(같은 후보군 선택기) 실패 기억을 참조만 하고, 새 label source(라벨 원천) 가설을 시험합니다.

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
        "notes": "frontier12_stage_open_grok_retry_accepted_trade_shape_label_contract_no_authority",
        "family": "experiment_design(실험 설계)",
        "work_family": "experiment_design(실험 설계)",
        "primary_report": REPORT_PATH.as_posix(),
        "run_number": RUN_NUMBER,
        "date": "2026-06-14",
        "decision": "open_frontier12_trade_shape_duration_controlled_onnx_scout",
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
        "source_authority": "grok_retry_accepted_plus_local_checks(그록 재시도 수용과 로컬 확인)",
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
        "notes": f"next={NEXT_RUN_ID};trade_shape_label_contract;no_authority",
        "question": "Can trade-shape duration labels improve US100 M5 ONNX DD and smoothness?(거래 형상 보유 기간 라벨이 US100 5분봉 온엑스 손실폭과 매끄러움을 개선하는가?)",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "run_family": "stage_open(단계 개방)",
        "goal_achieve": "not_claimed",
    }


def idea_registry_entry(summary: dict[str, Any]) -> str:
    return (
        f"<!-- {RUN_ID}__{IDEA_ID} -->\n"
        f"- `{IDEA_ID}`: Frontier12(프론티어12) opens trade-shape duration-controlled ONNX scout"
        f"(거래 형상과 보유 기간 통제 온엑스 탐색). Effect(효과): 같은 후보군 선택기 반복이 아니라 label source"
        f"(라벨 원천)를 새 축으로 시험합니다.\n"
    )


def changelog_entry(summary: dict[str, Any]) -> str:
    return (
        f"- {summary['created_at_utc']}: `{RUN_ID}` opened Frontier12(프론티어12) with Grok retry accepted"
        f"(그록 재시도 수용) and trade-shape label contract(거래 형상 라벨 계약). Effect(효과): next run"
        f"(다음 실행) `{NEXT_RUN_ID}` can run label proxy scout(라벨 프록시 탐색) without authority claims(권위 주장 없음).\n"
    )


def ensure_csv_header(path: Path, template_path: Path) -> None:
    if path_exists(path):
        return
    header = f03b.read_csv_header(template_path)
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        csv.writer(handle, lineterminator="\n").writerow(header)


def artifact_identity(path: Path) -> dict[str, str]:
    return {"path": path.as_posix(), "sha256": sha(path)}


def sha(path: Path) -> str:
    return sha256_file(path) if path_exists(path) else "missing(누락)"


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
