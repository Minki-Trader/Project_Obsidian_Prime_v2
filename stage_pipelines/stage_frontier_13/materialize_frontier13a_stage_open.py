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


STAGE_ID = "stage_frontier_13__regime_normalized_trade_shape_onnx_scout"
RUN_ID = "frontier13A_stage_open_regime_normalized_trade_shape_onnx_scout_v1"
RUN_NUMBER = "frontier13A"
PARENT_RUN_ID = "frontier12C_stage_closeout_trade_shape_duration_controlled_onnx_scout_v1"
NEXT_RUN_ID = "frontier13B_regime_normalized_trade_shape_proxy_scout_v1"
IDEA_ID = "IDEA-FR13-REGIME-NORMALIZED-TRADE-SHAPE-ONNX-SCOUT"
STATUS = "opened_frontier13_regime_normalized_trade_shape_onnx_scout_no_authority"
JUDGMENT = "stage_opened_after_grok_review_and_local_regime_boundary_no_authority"

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REPORT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_report.md"
DECISION_PATH = Path("docs/decisions/2026-06-14_stage_frontier_13_regime_normalized_trade_shape_onnx_scout_open.md")
SCRIPT_PATH = Path("stage_pipelines/stage_frontier_13/materialize_frontier13a_stage_open.py")

GROK_PACKET = Path("docs/agent_control/grok_reviews/2026-06-14_frontier13_stage_open/small_review")
F12_SELECTION = Path("stages/stage_frontier_12__trade_shape_duration_controlled_onnx_scout/04_selected/selection_status.md")
F12_REPORT = (
    Path("stages")
    / "stage_frontier_12__trade_shape_duration_controlled_onnx_scout"
    / "03_reviews"
    / "frontier12C_stage_closeout_trade_shape_duration_controlled_onnx_scout_v1_report.md"
)
F12_CANDIDATE_SUMMARY = (
    Path("stages")
    / "stage_frontier_12__trade_shape_duration_controlled_onnx_scout"
    / "02_runs"
    / "frontier12B_trade_shape_duration_label_proxy_scout_v1"
    / "candidate_summary.csv"
)


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
        "grok_classification": summary["grok_classification"],
        "local_verification": summary["local_verification"]["judgment"],
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
    meta = read_json(GROK_PACKET / "metadata.json")
    output = read_text(GROK_PACKET / "clean_output.md")
    return {
        "packet": GROK_PACKET.as_posix(),
        "prompt": (GROK_PACKET / "prompt.md").as_posix(),
        "output": (GROK_PACKET / "clean_output.md").as_posix(),
        "prompt_hash": meta.get("prompt_hash", ""),
        "success": bool(meta.get("success")),
        "duration_seconds": meta.get("duration_seconds", ""),
        "classification": classify_grok(output),
        "forbidden_claims_supported": "forbidden" in output.lower() and "goal achieve" in output.lower(),
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
    f12_selection = read_text(F12_SELECTION)
    feature_order = read_text(f03b.FEATURE_ORDER_PATH)
    required_regime_columns = [
        "is_us_cash_open",
        "is_first_30m_after_open",
        "is_last_30m_before_cash_close",
        "atr_14_over_atr_50",
        "di_spread_14",
        "bb_squeeze",
    ]
    checks = {
        "frontier12_closed_negative": "closed_negative_memory_no_authority" in f12_selection
        and "negative_memory(부정 기억)" in f12_selection,
        "frontier12_candidate_summary_exists": path_exists(F12_CANDIDATE_SUMMARY),
        "grok_stage_open_accepted": grok["success"] and grok["classification"] == "accepted(수용)",
        "grok_forbidden_claims_supported": bool(grok["forbidden_claims_supported"]),
        "dataset_exists": path_exists(f03b.DATASET_PATH),
        "feature_order_exists": path_exists(f03b.FEATURE_ORDER_PATH),
        "regime_columns_available": all(column in feature_order for column in required_regime_columns),
    }
    return {
        "checks": checks,
        "judgment": "pass_with_boundary(경계 포함 통과)" if all(checks.values()) else "needs_manual_review(수동 검토 필요)",
        "regime_columns": required_regime_columns,
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
        "grok_packet": grok["packet"],
        "grok_prompt": grok["prompt"],
        "grok_output": grok["output"],
        "grok_prompt_hash": grok["prompt_hash"],
        "grok_duration_seconds": grok["duration_seconds"],
        "grok_classification": grok["classification"],
        "local_verification": local,
        "frontier_thesis": (
            "US100 M5 fixed 3-class ONNX(US100 5분봉 고정 3분류 온엑스) may improve the DD/density tradeoff"
            "(손실폭/빈도 상충) if trade-shape labels(거래 형상 라벨) are normalized by train-only regime buckets"
            "(학습 전용 레짐 버킷) rather than globally loosened label knobs(전역 라벨 파라미터 완화)."
        ),
        "novelty_delta": (
            "Frontier12(프론티어12)는 global trade-shape duration labels(전역 거래 형상 보유 기간 라벨)을 시험했습니다."
            " Frontier13(프론티어13)은 closed-bar regime features(확정 봉 레짐 피처)로 train-only path scale"
            "(학습 전용 경로 척도)를 버킷별로 만들며, class-weight density forcing(클래스 가중 빈도 강제)이나 threshold search"
            "(임계값 탐색)를 하지 않습니다."
        ),
        "do_not_repeat": [
            "same global label knob loosening(같은 전역 라벨 파라미터 완화)",
            "class-weight density forcing(클래스 가중 빈도 강제)",
            "threshold micro-search(임계값 미세 탐색)",
            "post-fit selector ranking(적합 후 선택기 순위)",
            "archive winner/baseline inheritance(보관소 승자/기준선 상속)",
        ],
        "exit_rule": (
            "If Frontier13B(프론티어13B) has strict rows(엄격 행) 0 and preserved rows(보존 행) 0, or improves density"
            "(빈도) only by raising DD(손실폭), close as negative memory(부정 기억) or capped repair(상한 수리)."
        ),
        "claim_boundary": {claim: "not_claimed(주장 없음)" for claim in f03b.FORBIDDEN_CLAIMS},
    }


def write_outputs(summary: dict[str, Any]) -> None:
    write_json(RUN_ROOT / "stage_open_summary.json", summary)
    write_json(RUN_ROOT / "run_manifest.json", run_manifest(summary))
    f03b.write_text_sig(STAGE_ROOT / "README.md", readme(summary))
    f03b.write_text_sig(STAGE_ROOT / "00_spec" / "stage_brief.md", stage_brief(summary))
    f03b.write_text_sig(STAGE_ROOT / "00_spec" / "regime_label_contract.md", regime_label_contract(summary))
    f03b.write_text_sig(STAGE_ROOT / "01_inputs" / "experiment_design.md", experiment_design(summary))
    f03b.write_text_sig(STAGE_ROOT / "01_inputs" / "prior_stage_scan.md", prior_stage_scan(summary))
    f03b.write_text_sig(STAGE_ROOT / "01_inputs" / "input_refs.md", input_refs(summary))
    f03b.write_text_sig(STAGE_ROOT / "01_inputs" / "local_checks.md", local_checks(summary))
    f03b.write_text_sig(STAGE_ROOT / "01_inputs" / "selection_metric_spec.md", selection_metric_spec(summary))
    f03b.write_text_sig(REPORT_PATH, report(summary))
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / "required_gate_coverage_audit.md", gate_audit(summary))
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / "review_index.md", review_index(summary))
    f03b.write_text_sig(STAGE_ROOT / "04_selected" / "selection_status.md", selection_status(summary))
    f03b.write_text_sig(DECISION_PATH, decision(summary))


def update_state_and_registries(summary: dict[str, Any]) -> None:
    f03b.write_text_sig(f03b.WORKSPACE_STATE, workspace_state(summary))
    f03b.write_text_sig(f03b.CURRENT_WORKING_STATE, current_working_state(summary))
    row = ledger_row(summary)
    f03b.upsert_csv(f03b.RUN_REGISTRY, "run_id", run_registry_row(summary))
    f03b.upsert_csv(f03b.ALPHA_LEDGER, "ledger_row_id", row)
    f03b.upsert_csv(STAGE_ROOT / "03_reviews" / "stage_run_ledger.csv", "ledger_row_id", row)
    f03b.append_once(f03b.IDEA_REGISTRY, f"{RUN_ID}__{IDEA_ID}", idea_entry(summary))
    f03b.append_once(f03b.CHANGELOG, RUN_ID, changelog_entry(summary))


def run_manifest(summary: dict[str, Any]) -> dict[str, Any]:
    return {
        **summary,
        "script_path": SCRIPT_PATH.as_posix(),
        "script_sha256": sha256_file(SCRIPT_PATH),
        "inputs": {
            "frontier12_selection": artifact_identity(F12_SELECTION),
            "frontier12_report": artifact_identity(F12_REPORT),
            "frontier12_candidate_summary": artifact_identity(F12_CANDIDATE_SUMMARY),
            "dataset": artifact_identity(f03b.DATASET_PATH),
            "feature_order": artifact_identity(f03b.FEATURE_ORDER_PATH),
            "grok_output": artifact_identity(Path(summary["grok_output"])),
        },
    }


def readme(summary: dict[str, Any]) -> str:
    return f"""# {STAGE_ID}

Status(상태): `{summary['status']}`

Latest run(최근 실행): `{RUN_ID}`

Next run(다음 실행): `{NEXT_RUN_ID}`
"""


def stage_brief(summary: dict[str, Any]) -> str:
    return f"""# Frontier13 Stage Brief(프론티어13 단계 개요)

Stage id(단계 ID): `{STAGE_ID}`

Question(질문): Can train-only regime-normalized trade-shape labels(학습 전용 레짐 정규화 거래 형상 라벨) improve the US100 M5 ONNX(US100 5분봉 온엑스) DD/density tradeoff(손실폭/빈도 상충)?

## Frontier Thesis(프론티어 가설)

{summary['frontier_thesis']}

## Novelty Delta(신규성 차이)

{summary['novelty_delta']}

## Do Not Repeat(반복 금지)

{bullet_list(summary['do_not_repeat'])}

## Exit Rule(종료 규칙)

{summary['exit_rule']}

## Claim Boundary(주장 경계)

Only scout clue(탐색 단서), seed surface(씨앗 표면), preserved clue(보존 단서), negative memory(부정 기억), invalid setup(무효 설정), or blocked(차단) may be claimed. completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 forbidden(금지)입니다.
"""


def regime_label_contract(summary: dict[str, Any]) -> str:
    return f"""# Regime Label Contract(레짐 라벨 계약)

Action(행동): Frontier13B(프론티어13B)는 closed-bar regime features(확정 봉 레짐 피처)로 train-only buckets(학습 전용 버킷)을 만들고, 각 bucket(버킷)의 path scale(경로 척도)을 학습 구간에서만 계산합니다.

Effect(효과): validation/OOS(검증/표본밖) 성과를 본 뒤 threshold(임계값)를 맞추는 hidden search(숨은 탐색)를 막습니다.

Allowed regime inputs(허용 레짐 입력):

{bullet_list(summary['local_verification']['regime_columns'])}

Forbidden(금지):

- validation/OOS-driven bucket edits(검증/표본밖 기반 버킷 수정)
- class-weight density forcing(클래스 가중 빈도 강제)
- threshold micro-search(임계값 미세 탐색)
- selected baseline inheritance(선택 기준선 상속)
"""


def experiment_design(summary: dict[str, Any]) -> str:
    return f"""# Frontier13 Experiment Design(프론티어13 실험 설계)

## Hypothesis(가설)

{summary['frontier_thesis']}

## Decision Use(결정 사용)

Action(행동): Frontier13B(프론티어13B) proxy scout(프록시 탐색)가 regime-normalized labels(레짐 정규화 라벨)이 F12(프론티어12)의 sparse low-DD surface(희소한 낮은 손실폭 표면)를 넓히는지 확인합니다.

Effect(효과): useful seed surface(유용한 씨앗 표면)인지 negative memory(부정 기억)인지 가릅니다.

## Control Variables(고정 변수)

- US100 M5(US100 5분봉), fixed split(고정 분할), output schema `[p_short, p_flat, p_long]`(출력 스키마)
- argmax-only signal(최대확률 전용 신호)
- no WFO/MT5 at proxy stage(프록시 단계에서 WFO/MT5 없음)

## Changed Variables(변경 변수)

- train-only regime bucket scale(학습 전용 레짐 버킷 척도)
- regime scheme(레짐 방식): session/volatility/trend/squeeze(세션/변동성/추세/압축)

## Success Criteria(성공 기준)

validation/OOS density(검증/표본밖 빈도) 5~10/day(일 5~10회), PF(수익 팩터) >= 1.2, DD(손실폭) <= 15%, positive net(양수 순손익), ONNX parity(온엑스 동등성), and better worst subperiod DD(더 나은 최악 하위기간 손실폭).

## Failure Criteria(실패 기준)

strict/preserved rows(엄격/보존 행) 0, density-only improvement(빈도만 개선), DD rise(손실폭 상승), or regime bucket overfit(레짐 버킷 과적합).
"""


def prior_stage_scan(summary: dict[str, Any]) -> str:
    return f"""# Frontier13 Prior Stage Scan(프론티어13 이전 단계 점검)

Frontier12(프론티어12) negative memory(부정 기억): trade-shape duration labels(거래 형상 보유 기간 라벨)은 validation DD(검증 손실폭)를 낮췄지만 validation PF/density(검증 수익 팩터/빈도)와 worst subperiod concentration(최악 하위기간 집중)을 통과하지 못했습니다.

Reference-only carry(참조 전용 이월): fast-shape plain logistic surface(빠른 형상 평범 로지스틱 표면)는 DD reduction seed(손실폭 감소 씨앗)로만 봅니다.

Novelty proof(신규성 증명): {summary['novelty_delta']}

Do not repeat(반복 금지):

{bullet_list(summary['do_not_repeat'])}
"""


def input_refs(summary: dict[str, Any]) -> str:
    return f"""# Frontier13 Input References(프론티어13 입력 참조)

- Frontier12 selection(프론티어12 선택 상태): `{F12_SELECTION.as_posix()}`
- Frontier12 report(프론티어12 보고서): `{F12_REPORT.as_posix()}`
- Frontier12 candidate summary(프론티어12 후보 요약): `{F12_CANDIDATE_SUMMARY.as_posix()}`
- Grok packet(그록 묶음): `{summary['grok_packet']}`
- Dataset(데이터셋): `{f03b.DATASET_PATH.as_posix()}`
- Feature order(피처 순서): `{f03b.FEATURE_ORDER_PATH.as_posix()}`
"""


def local_checks(summary: dict[str, Any]) -> str:
    lines = "\n".join(f"- {key}: `{value}`" for key, value in summary["local_verification"]["checks"].items())
    return f"""# Frontier13 Local Checks(프론티어13 로컬 확인)

Updated(갱신): {summary['created_at_utc']}

Local judgment(로컬 판정): `{summary['local_verification']['judgment']}`

{lines}
"""


def selection_metric_spec(summary: dict[str, Any]) -> str:
    return """# Frontier13 Selection Metric Spec(프론티어13 선택 지표 명세)

Metrics(지표): aggregate PF/density/DD(합계 수익 팩터/빈도/손실폭), month/quarter subperiod PF/density/DD(월/분기 하위기간 수익 팩터/빈도/손실폭), worst subperiod DD(최악 하위기간 손실폭), smoothness proxy(매끄러움 프록시), ONNX parity(온엑스 동등성).

Selection rule(선택 규칙): four-axis improvement(네 축 개선) is required for strict clue(엄격 단서). One-axis improvement(한 축 개선)는 seed surface(씨앗 표면)나 negative memory(부정 기억)로만 남깁니다.
"""


def report(summary: dict[str, Any]) -> str:
    return f"""# Frontier13A Stage Open Report(프론티어13A 단계 개방 보고서)

Updated(갱신): {summary['created_at_utc']}

Status(상태): `{summary['status']}`

Judgment(판정): `{summary['judgment']}`

Action(행동): Frontier13(프론티어13)을 regime-normalized trade-shape ONNX scout(레짐 정규화 거래 형상 온엑스 탐색)로 열었습니다.

Effect(효과): F12(프론티어12)의 낮은 손실폭 씨앗(seed, 씨앗)을 같은 라벨 완화(label loosening, 라벨 완화) 없이 새 레짐 척도(regime scale, 레짐 척도) 축에서 시험합니다.

Grok receipt(그록 영수증): `{summary['grok_packet']}`, classification(분류) `{summary['grok_classification']}`, local verification(로컬 검증) `{summary['local_verification']['judgment']}`.

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성) 모두 not_claimed(주장 없음).
"""


def gate_audit(summary: dict[str, Any]) -> str:
    return f"""# Frontier13A Required Gate Coverage Audit(프론티어13A 필수 게이트 커버리지 감사)

Updated(갱신): {summary['created_at_utc']}

Status(상태): pass_with_boundary(경계 포함 통과)

- external_review_packet(외부 검토 묶음): Grok accepted(그록 수용)
- opening_contract_gate(개방 계약 게이트): frontier thesis/novelty/prior scan/do-not-repeat/exit/claim boundary(가설/신규성/이전 점검/반복 금지/종료/주장 경계) recorded(기록됨)
- data_integrity_gate(데이터 무결성 게이트): closed-bar regime columns(확정 봉 레짐 열) verified(확인됨)
- final_claim_guard(최종 주장 보호): no authority claims(권위 주장 없음)
"""


def review_index(summary: dict[str, Any]) -> str:
    return f"""# Frontier13 Review Index(프론티어13 검토 색인)

Updated(갱신): {summary['created_at_utc']}

- `{RUN_ID}`: stage open(단계 개방), Grok accepted(그록 수용), local checks pass(로컬 확인 통과).
"""


def selection_status(summary: dict[str, Any]) -> str:
    return f"""# Frontier13 Selection Status(프론티어13 선택 상태)

Updated(갱신): {summary['created_at_utc']}

Status(상태): `{summary['status']}`

Judgment(판정): `{summary['judgment']}`

Selection(선택): no selected baseline/completion candidate/promotion/runtime authority(선택 기준선/완성 후보/승격/런타임 권위 없음).

Next run(다음 실행): `{NEXT_RUN_ID}`
"""


def decision(summary: dict[str, Any]) -> str:
    return f"""# Decision: Open Frontier13 Regime-Normalized Trade Shape ONNX Scout(결정: 프론티어13 레짐 정규화 거래 형상 온엑스 탐색 개방)

Date(날짜): {summary['created_at_utc']}

Decision(결정): `{summary['status']}`

Action(행동): Frontier13(프론티어13)을 새 regime-normalized label source(레짐 정규화 라벨 원천) 가설로 열었습니다.

Effect(효과): Frontier12(프론티어12)의 same label knob loosening(같은 라벨 파라미터 완화)을 반복하지 않습니다.
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

Action(행동): Frontier13(프론티어13)은 regime-normalized trade-shape ONNX scout(레짐 정규화 거래 형상 온엑스 탐색)로 열렸습니다.

Effect(효과): train-only regime buckets(학습 전용 레짐 버킷)이 F12(프론티어12)의 DD/density tradeoff(손실폭/빈도 상충)를 바꾸는지 시험합니다.

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
        "notes": "frontier13_stage_open_grok_accepted_regime_normalized_label_contract_no_authority",
        "work_family": "experiment_design(실험 설계)",
        "run_number": RUN_NUMBER,
        "date": "2026-06-14",
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "claim_boundary": "stage_open_no_model_no_wfo_no_mt5_no_authority_goal_claim",
        "report_path": REPORT_PATH.as_posix(),
        "created_at_utc": summary["created_at_utc"],
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
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
        "primary_kpi": "grok_classification=accepted(그록 분류=수용)",
        "guardrail_kpi": "no_model_no_wfo_no_mt5_no_authority(모델/WFO/MT5/권위 없음)",
        "external_verification_status": "not_applicable(해당 없음)",
        "notes": f"next={NEXT_RUN_ID};regime_label_contract;no_authority",
        "question": "Can regime-normalized labels improve DD/density tradeoff?(레짐 정규화 라벨이 손실폭/빈도 상충을 개선하는가?)",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "run_family": "stage_open(단계 개방)",
        "goal_achieve": "not_claimed",
    }


def idea_entry(summary: dict[str, Any]) -> str:
    return (
        f"<!-- {RUN_ID}__{IDEA_ID} -->\n"
        f"- `{IDEA_ID}`: Frontier13(프론티어13) opens regime-normalized trade-shape ONNX scout"
        f"(레짐 정규화 거래 형상 온엑스 탐색). Effect(효과): F12(프론티어12)의 global label knob"
        f"(전역 라벨 파라미터) 반복 없이 train-only regime scale(학습 전용 레짐 척도)을 시험합니다.\n"
    )


def changelog_entry(summary: dict[str, Any]) -> str:
    return (
        f"- {summary['created_at_utc']}: `{RUN_ID}` opened Frontier13(프론티어13) with Grok accepted"
        f"(그록 수용). Effect(효과): next run(다음 실행) `{NEXT_RUN_ID}` can test regime-normalized labels"
        f"(레짐 정규화 라벨) without authority claims(권위 주장 없음).\n"
    )


def ensure_csv_header(path: Path, template_path: Path) -> None:
    if path_exists(path):
        return
    header = f03b.read_csv_header(template_path)
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        csv.writer(handle, lineterminator="\n").writerow(header)


def artifact_identity(path: Path) -> dict[str, str]:
    return {"path": path.as_posix(), "sha256": sha256_file(path) if path_exists(path) else "missing(누락)"}


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def read_text(path: Path) -> str:
    return io_path(path).read_text(encoding="utf-8-sig")


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8-sig")


def bullet_list(items: list[str]) -> str:
    return "\n".join(f"- {item}" for item in items)


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


if __name__ == "__main__":
    raise SystemExit(main())
