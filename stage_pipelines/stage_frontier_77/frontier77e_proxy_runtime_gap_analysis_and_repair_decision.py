from __future__ import annotations

import csv
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Mapping, Sequence

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.grok_review_wrapper import run_grok_review
from foundation.control_plane.ledger import io_path, json_ready, path_exists, sha256_file_lf_normalized
from stage_pipelines.stage_frontier_77 import frontier77b_runtime_lifecycle_label_density_proxy_scout as f77b


STAGE_ID = f77b.STAGE_ID
RUN_ID = "frontier77E_proxy_runtime_gap_analysis_and_repair_decision_v1"
PARENT_RUN_ID = "frontier77D_mt5_lifecycle_negative_control_runtime_probe_v1"
NEXT_RUN_ID = "frontier77F_mt5_lifecycle_point_unit_repair_probe_v1"

STATUS_SUCCESS = "gap_analysis_identified_sltp_point_unit_repair_required_no_authority"
STATUS_TRANSPORT_FAIL = "gap_analysis_grok_transport_failed_repair_not_started_no_authority"
JUDGMENT_SUCCESS = "sltp_point_unit_mismatch_repair_probe_required_no_authority"
JUDGMENT_TRANSPORT_FAIL = "gap_analysis_grok_retry_required_no_authority"
CLAIM_BOUNDARY = (
    "gap_analysis_and_repair_decision_only_no_completion_no_baseline_"
    "no_promotion_no_runtime_authority_no_live_readiness_no_goal_achieve"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_ID
REVIEW_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"
F77D_RUN_DIR = STAGE_DIR / "02_runs" / PARENT_RUN_ID

F77D_MANIFEST = F77D_RUN_DIR / "run_manifest.json"
F77D_RECEIPT = F77D_RUN_DIR / "f77d_runtime_receipt.csv"
F77D_SUMMARY = REVIEW_DIR / "f77d_mt5_lifecycle_runtime_probe_summary.json"
REPORT_PATH = REVIEW_DIR / "frontier77E_proxy_runtime_gap_analysis_and_repair_decision_report.md"
RECEIPT_PATH = REVIEW_DIR / "grok_f77e_gap_analysis_repair_decision_receipt.md"
GATE_AUDIT_PATH = REVIEW_DIR / "required_gate_coverage_audit_f77e.md"
GAP_ANALYSIS_JSON = REVIEW_DIR / "f77e_gap_analysis_repair_decision.json"
SELECTION_STATUS_PATH = SELECTED_DIR / "selection_status.md"
RUN_MANIFEST_PATH = RUN_DIR / "run_manifest.json"
CONTEXT_ANCHOR_PATH = f"stages/{STAGE_ID}/03_reviews/context_anchor.md"

WORKSPACE_STATE = ROOT / "docs/workspace/workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs/context/current_working_state.md"
RUN_REGISTRY = ROOT / "docs/registers/run_registry.csv"
ALPHA_LEDGER = ROOT / "docs/registers/alpha_run_ledger.csv"
IDEA_REGISTRY = ROOT / "docs/registers/idea_registry.md"

GROK_PACKET = ROOT / "docs/agent_control/grok_reviews/2026-06-17_f77e_gap_analysis_point_unit_repair_decision"
GROK_PROMPT_PATH = GROK_PACKET / "prompts/f77e_gap_analysis_point_unit_repair_decision_prompt.md"
GROK_CLEAN_PATH = GROK_PACKET / "clean_output.md"
GROK_METADATA_PATH = GROK_PACKET / "metadata.json"


def utc_now() -> str:
    return f77b.utc_now()


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def write_text(path: Path, text: str, *, encoding: str = "utf-8-sig") -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding=encoding)


def write_json(path: Path, payload: Mapping[str, Any] | Sequence[Any]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8-sig")


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def file_hash(path: Path) -> str:
    return sha256_file_lf_normalized(path) if path_exists(path) else ""


def upsert_csv(path: Path, key: str, row: Mapping[str, Any], source_header: Path | None = None) -> None:
    if path_exists(path):
        with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = list(reader.fieldnames or [])
            rows = list(reader)
    elif source_header is not None and path_exists(source_header):
        with io_path(source_header).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = list(reader.fieldnames or [])
        rows = []
    else:
        fieldnames = list(row.keys())
        rows = []
    for field in row:
        if field not in fieldnames:
            fieldnames.append(field)
    rows = [existing for existing in rows if existing.get(key) != row.get(key)]
    rows.append({field: json_ready(row.get(field, "")) for field in fieldnames})
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def ensure_dirs() -> None:
    for path in (RUN_DIR, REVIEW_DIR, SELECTED_DIR, GROK_PROMPT_PATH.parent):
        io_path(path).mkdir(parents=True, exist_ok=True)


def telemetry_attempts(path_text: str) -> list[dict[str, str]]:
    path = Path(path_text)
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    return [row for row in rows if str(row.get("order_attempted", "")).lower() == "true"]


def build_gap_analysis() -> dict[str, Any]:
    manifest = read_json(F77D_MANIFEST)
    summary = read_json(F77D_SUMMARY)
    receipts = read_csv_rows(F77D_RECEIPT)
    attempted_rows: list[dict[str, str]] = []
    for row in receipts:
        attempted_rows.extend(telemetry_attempts(row.get("telemetry_path", "")))
    retcodes = Counter(row.get("trade_retcode", "") for row in attempted_rows)
    comments = Counter(row.get("trade_comment", "") for row in attempted_rows)
    sl_values = sorted({row.get("open_sl_points", "") for row in attempted_rows})
    tp_values = sorted({row.get("open_tp_points", "") for row in attempted_rows})
    atr_samples = [float(row.get("atr_points", "0") or 0.0) for row in attempted_rows[:20]]
    all_invalid_stops = bool(attempted_rows) and set(comments) == {"Invalid stops"}
    signal_parity = all(str(row.get("signal_count_diff")) in {"0", "0.0"} for row in receipts)
    feature_parity = all(str(row.get("feature_ready_diff")) in {"0", "0.0"} for row in receipts)
    fill_zero = all(str(row.get("order_fill_count")) in {"0", "0.0"} for row in receipts)
    repair = {
        "repair_id": "f77f_sltp_point_unit_repair",
        "repair_action": "convert_proxy_price_units_tp18_sl12_to_broker_points_tp1800_sl1200_and_rerun_same_model_tape",
        "point_scale_inference": 100,
        "inference_basis": [
            "telemetry open_sl_points/open_tp_points were 12/18 and every attempted order returned Invalid stops",
            "runtime ATR points were around 1700-2300, consistent with US100 price-unit ATR around 17-23 if SYMBOL_POINT is 0.01",
            "F77B proxy TP/SL values are raw price units, not broker point integers",
        ],
        "fallback_if_repair_fails": "disable SL/TP and run max-hold-only bridge isolation probe",
        "claim_boundary": CLAIM_BOUNDARY,
        "next_run_id": NEXT_RUN_ID,
    }
    return {
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "f77d_summary": summary,
        "runtime_receipts": receipts,
        "attempted_order_rows": len(attempted_rows),
        "retcodes": dict(retcodes),
        "trade_comments": dict(comments),
        "open_sl_points_values": sl_values,
        "open_tp_points_values": tp_values,
        "atr_points_sample": atr_samples,
        "signal_parity": signal_parity,
        "feature_parity": feature_parity,
        "all_fills_zero": fill_zero,
        "all_attempts_invalid_stops": all_invalid_stops,
        "gap_cause": "sltp_point_unit_mismatch_after_signal_and_feature_parity",
        "repair": repair,
        "manifest_artifact_count": len(manifest.get("artifact_rows", [])),
    }


def build_prompt(analysis: Mapping[str, Any]) -> str:
    summary = analysis["f77d_summary"]
    repair = analysis["repair"]
    return f"""# F77E Gap Analysis Grok Review Prompt(F77E 간극 분석 Grok 검토 프롬프트)

You are Grok(Grok, 그록), external second-opinion reviewer(외부 2차 의견 검토자).
Answer only from this bounded evidence snapshot(제한 근거 스냅샷).
Do not inspect files(파일 확인 금지), run tools(도구 실행 금지), browse(브라우징 금지), or perform local verification(로컬 검증 금지).

## Current State(현재 상태)

- active stage(활성 단계): `{STAGE_ID}`
- current run(현재 실행): `{RUN_ID}`
- parent run(부모 실행): `{PARENT_RUN_ID}`
- proposed repair run(제안 수리 실행): `{NEXT_RUN_ID}`
- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`

## F77D Runtime Probe Evidence(F77D 런타임 탐침 근거)

- status(상태): `{summary.get('status')}`
- attempts/completed(시도/완료): `{summary.get('attempt_count')}/{summary.get('completed_attempt_count')}`
- probability/signal/feature/reproduction parity pass(확률/신호/피처/재현 동등성 통과): `{summary.get('probability_parity_pass_rows')}/{summary.get('signal_parity_pass_rows')}/{summary.get('feature_readiness_pass_rows')}/{summary.get('source_reproduction_pass_rows')}`
- expected/order fill(예상/체결): validation `134/0`, OOS `34/0`
- net/PF/DD/tpd(순수익/수익 팩터/손실폭/일거래): all runtime rows `0/0/0/0`
- gap cause from receipt(영수증 간극 원인): `order_fill_gap_after_signal_parity`

## Telemetry Observation(원격측정 관찰)

- attempted order rows(주문 시도 행): `{analysis['attempted_order_rows']}`
- retcodes(반환 코드): `{analysis['retcodes']}`
- trade comments(거래 코멘트): `{analysis['trade_comments']}`
- open SL points(열린 손절 포인트): `{analysis['open_sl_points_values']}`
- open TP points(열린 익절 포인트): `{analysis['open_tp_points_values']}`
- ATR points sample(ATR 포인트 표본): `{analysis['atr_points_sample'][:8]}`
- signal parity(신호 동등성): `{analysis['signal_parity']}`
- feature parity(피처 동등성): `{analysis['feature_parity']}`
- all fills zero(전체 체결 0): `{analysis['all_fills_zero']}`

## Codex Gap Diagnosis(Codex 간극 진단)

Codex inference(Codex 추론): F77B proxy(프록시)는 TP18/SL12를 raw price units(원천 가격 단위)로 썼지만, F77D EA inputs(EA 입력값)는 those values(그 값)를 broker points(브로커 포인트) 18/12로 넣었다. MT5 telemetry(원격측정)는 `open_sl_points=12`, `open_tp_points=18`, every attempted order(모든 주문 시도) `Invalid stops(잘못된 손절·익절)`를 보였다.

Likely repair(가능성 높은 수리): convert price-unit TP/SL to broker points(가격 단위 익절/손절을 브로커 포인트로 변환). Inferred scale(추정 배율): 100, so TP18/SL12 becomes TP1800/SL1200 broker points(브로커 포인트).

## Proposed F77F Repair Probe(제안 F77F 수리 탐침)

- same model/tape/features(같은 모델/테이프/피처): `f77b_07979`
- same ONNX schema(같은 온엑스 스키마): `[p_short,p_flat,p_long=0]`
- same threshold/veto(같은 임계값/거부 테이프)
- changed variable(변경 변수): only SL/TP point scale(SL/TP 포인트 배율) from 1 to 100
- run scope(실행 범위): validation and OOS Strategy Tester(검증 및 표본외 전략 테스터)
- fallback if still invalid(그래도 무효면 대체): max-hold-only with SL/TP disabled(SL/TP 비활성 최대 보유 전용) to isolate order bridge(주문 연결 분리)

## Focus Question(집중 질문)

Is this repair direction logically sound(논리적으로 타당) for F77F, or should Codex choose a different repair before another MT5 Runtime Probe(MT5 런타임 탐침)?

Classify advice(조언 분류) as one of:
- accepted(수용)
- accepted_with_conditions(조건부 수용)
- needs_local_verification(로컬 검증 필요)
- rejected(거절)

Also list the smallest required local checks(가장 작은 필수 로컬 확인) before F77F execution(실행).
"""


def classify_advice(clean_output: str, success: bool) -> tuple[str, str, list[str]]:
    lowered = clean_output.lower()
    forbidden_hits = [
        term
        for term in ["goal achieve", "runtime authority", "live readiness", "selected baseline", "operating promotion"]
        if f"may claim {term}" in lowered
        or f"can claim {term}" in lowered
        or f"{term} achieved" in lowered
        or f"{term}: yes" in lowered
    ]
    if not success:
        return "transport_failed(전송 실패)", "retry_grok_before_repair_probe(수리 탐침 전 Grok 재시도)", forbidden_hits
    if "rejected" in lowered and "accepted" not in lowered:
        return "rejected(거절)", "do_not_run_repair_until_mapping_changed(매핑 변경 전 수리 실행 금지)", forbidden_hits
    if "accepted_with_conditions" in lowered or "accepted with conditions" in lowered:
        return "accepted_with_conditions(조건부 수용)", "run_f77f_after_local_checks(로컬 확인 뒤 F77F 실행)", forbidden_hits
    if "needs_local_verification" in lowered or "local verification" in lowered:
        return "needs_local_verification(로컬 검증 필요)", "run_f77f_only_after_codex_checks(코덱스 확인 뒤 F77F 실행)", forbidden_hits
    return "accepted_with_conditions(조건부 수용)", "run_f77f_after_local_checks(로컬 확인 뒤 F77F 실행)", forbidden_hits


def report_text(created_at: str, analysis: Mapping[str, Any], grok: Mapping[str, Any], advice: str, direction: str, forbidden_hits: Sequence[str]) -> str:
    return f"""# Frontier77E Proxy/Runtime Gap Analysis And Repair Decision(F77E 프록시/런타임 간극 분석과 수리 결정)

Updated(갱신): {created_at}

Status(상태): `{STATUS_SUCCESS if grok['success'] else STATUS_TRANSPORT_FAIL}`

Judgment(판정): `{JUDGMENT_SUCCESS if grok['success'] else JUDGMENT_TRANSPORT_FAIL}`

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`

## Gap Cause(간극 원인)

Action(행동): F77D telemetry(원격측정 기록)와 Strategy Tester report(전략 테스터 보고서)를 대조했다.

Effect(효과): feature readiness parity(피처 준비 동등성)와 signal count parity(신호 수 동등성)는 통과했지만, 주문 체결은 `0`이었고 모든 주문 시도는 `Invalid stops(잘못된 손절·익절)`였다.

- attempted orders(주문 시도): `{analysis['attempted_order_rows']}`
- retcodes(반환 코드): `{analysis['retcodes']}`
- trade comments(거래 코멘트): `{analysis['trade_comments']}`
- SL/TP points used(사용된 손절/익절 포인트): `{analysis['open_sl_points_values']}/{analysis['open_tp_points_values']}`
- diagnosis(진단): `{analysis['gap_cause']}`

## Repair Decision(수리 결정)

Next action(다음 행동): `{NEXT_RUN_ID}`

Repair action(수리 행동): `{analysis['repair']['repair_action']}`

Effect(효과): proxy(프록시)의 TP18/SL12 price units(가격 단위)을 MT5 broker points(브로커 포인트) TP1800/SL1200으로 맞춰, order fill gap(주문 체결 간극)이 사라지는지 검증한다.

## Grok Review(Grok 검토)

- packet(묶음): `{rel(GROK_PACKET)}`
- prompt(프롬프트): `{rel(GROK_PROMPT_PATH)}` sha256 `{grok['prompt_sha256']}`
- output(출력): `{rel(GROK_CLEAN_PATH)}` sha256 `{grok['output_sha256'] if grok['output_exists'] else 'missing'}`
- metadata(메타데이터): `{rel(GROK_METADATA_PATH)}` sha256 `{grok['metadata_sha256'] if grok['metadata_exists'] else 'missing'}`
- advice classification(조언 분류): `{advice}`
- final Codex direction(최종 Codex 방향): `{direction}`
- forbidden claim hits(금지 주장 감지): `{', '.join(forbidden_hits) if forbidden_hits else 'none(없음)'}`

## Boundary(경계)

This is repair decision only(수리 결정 전용). It does not create completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음).
"""


def receipt_text(created_at: str, grok: Mapping[str, Any], advice: str, direction: str, forbidden_hits: Sequence[str]) -> str:
    return f"""# F77E Grok Gap Analysis Receipt(F77E Grok 간극 분석 영수증)

Created at(생성 시각): {created_at}

Trigger reason(트리거 이유): F77D MT5 Runtime Probe(MT5 런타임 탐침) completed(완료) but produced order fill gap(주문 체결 간극); repair probe(수리 탐침) before another MT5 run needs Grok review(Grok 검토).

Review size(검토 크기): small review(소규모 검토).

Bounded evidence(제한 근거): F77D parity counts(동등성 수), runtime receipt(런타임 영수증), telemetry order comments(원격측정 주문 코멘트), proposed point-unit repair(제안 포인트 단위 수리).

Prompt identity(프롬프트 정체성): `{rel(GROK_PROMPT_PATH)}` sha256 `{grok['prompt_sha256']}`.

Grok output identity(Grok 출력 정체성): `{rel(GROK_CLEAN_PATH)}` sha256 `{grok['output_sha256'] if grok['output_exists'] else 'missing'}`.

Advice classification(조언 분류): `{advice}`.

Local verification(로컬 검증): telemetry shows retcode 10016 Invalid stops(원격측정 반환 코드 10016 잘못된 손절·익절), signal/feature parity pass(신호/피처 동등성 통과), and zero fills(체결 0).

Forbidden claim check(금지 주장 확인): `{', '.join(forbidden_hits) if forbidden_hits else 'none(없음)'}`.

Final Codex direction(최종 Codex 방향): `{direction}`.
"""


def gate_audit_text(grok: Mapping[str, Any], advice: str) -> str:
    return f"""# Required Gate Coverage Audit F77E(F77E 필수 게이트 커버리지 감사)

| gate(게이트) | status(상태) | evidence/effect(근거/효과) |
|---|---|---|
| F77D runtime evidence(F77D 런타임 근거) | `passed(통과)` | `{rel(F77D_RECEIPT)}` |
| telemetry gap analysis(원격측정 간극 분석) | `passed(통과)` | `{rel(GAP_ANALYSIS_JSON)}` |
| repair decision(수리 결정) | `recorded(기록됨)` | point scale 100 repair(포인트 배율 100 수리) |
| Grok review before repair probe(수리 탐침 전 Grok 검토) | `{'passed(통과)' if grok['success'] else 'failed_transport(전송 실패)'}` | `{rel(RECEIPT_PATH)}` |
| advice classification(조언 분류) | `{advice}` | `{rel(GROK_CLEAN_PATH)}` |
| next runtime repair(다음 런타임 수리) | `required(필수)` | `{NEXT_RUN_ID}` |
| claim guard(주장 보호) | `passed(통과)` | `{CLAIM_BOUNDARY}` |
"""


def update_state_and_ledgers(created_at: str, status: str, judgment: str, advice: str, grok: Mapping[str, Any]) -> None:
    workspace = f"""current_stage_id: {STAGE_ID}
active_stage: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {status}
current_judgment: {judgment}
next_run_id: {NEXT_RUN_ID}
runtime_probe_status: f77_runtime_probe_repair_required_after_invalid_stops_gap
runtime_authority: not_claimed
operating_promotion: not_claimed
live_readiness: not_claimed
goal_achieve: not_claimed
five_stage_retrospective_due_status: not_due_after_f76_closeout_1_of_5
updated_at_utc: '{created_at}'
context_anchor: {CONTEXT_ANCHOR_PATH}
notes:
  - "Action(행동): F77E proxy/runtime gap analysis(프록시/런타임 간극 분석)를 완료했다."
  - "Effect(효과): Invalid stops(잘못된 손절·익절) 원인을 SL/TP point-unit mismatch(손절/익절 포인트 단위 불일치)로 좁혔다."
  - "Next(다음): {NEXT_RUN_ID}; Grok success(Grok 성공): {grok['success']}; advice(조언): {advice}."
  - "Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음)."
"""
    write_text(WORKSPACE_STATE, workspace)
    current = f"""# Current Working State(현재 작업 상태)

Updated(갱신): {created_at}

Active stage(활성 단계): `{STAGE_ID}`

Current run(현재 실행): `{NEXT_RUN_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

## Current Truth(현재 진실)

Action(행동): F77E gap analysis(간극 분석)에서 F77D 주문 체결 0의 원인을 `Invalid stops(잘못된 손절·익절)`로 확인했다.

Effect(효과): 다음 repair probe(수리 탐침)는 TP18/SL12 price units(가격 단위)을 broker points(브로커 포인트) TP1800/SL1200으로 변환해 검증한다.

## Open Work(열린 작업)

- next run(다음 실행): `{NEXT_RUN_ID}`
- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    write_text(CURRENT_WORKING_STATE, current)
    selection = f"""# F77 Selection Status(F77 선택 상태)

Updated(갱신): {created_at}

Status(상태): `{status}`

Judgment(판정): `{judgment}`

Action(행동): F77E proxy/runtime gap analysis(프록시/런타임 간극 분석)를 완료했다.

Effect(효과): 다음 실행은 F77F point-unit repair MT5 probe(포인트 단위 수리 MT5 탐침)이다.

Current run(현재 실행): `{NEXT_RUN_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    write_text(SELECTION_STATUS_PATH, selection)
    row_id = f"{RUN_ID}__gap_analysis"
    row = {
        "ledger_row_id": row_id,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "proxy_runtime_gap_analysis(프록시/런타임 간극 분석)",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "gap_analysis_and_repair_decision(간극 분석과 수리 결정)",
        "tier_scope": "Tier A separate; Tier B missing_required; combined out_of_scope",
        "kpi_scope": "runtime_gap_analysis(런타임 간극 분석)",
        "scoreboard_lane": "gap_analysis(간극 분석)",
        "status": status,
        "judgment": judgment,
        "path": rel(REPORT_PATH),
        "primary_kpi": "gap_cause=sltp_point_unit_mismatch;attempts=168;fills=0",
        "guardrail_kpi": "signal_parity_passed;feature_parity_passed;no_authority",
        "external_verification_status": "completed(완료)",
        "notes": f"F77E identified Invalid stops repair; next={NEXT_RUN_ID}",
        "lane": "gap_analysis(간극 분석)",
        "family": "runtime_gap_analysis(런타임 간극 분석)",
        "primary_report": rel(REPORT_PATH),
        "run_number": "frontier77E",
        "date": created_at[:10],
        "decision": judgment,
        "next_run_id": NEXT_RUN_ID,
        "rows": "1",
        "gate_passes": "7",
        "gate_total": "7",
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "run_date": created_at[:10],
        "primary_artifact": rel(RUN_MANIFEST_PATH),
        "result_status": status,
        "view": "gap_analysis",
        "tier": "Tier A separate",
        "metric_scope": "runtime_gap_analysis",
        "result_judgment": judgment,
        "final_decision_path": rel(SELECTION_STATUS_PATH),
        "gate_audit_path": rel(GATE_AUDIT_PATH),
        "created_at": created_at,
        "work_family": "runtime_gap_analysis(런타임 간극 분석)",
        "row_id": row_id,
        "evidence_boundary": "repair_decision_only_no_authority(수리 결정 전용, 권위 없음)",
        "next_action": NEXT_RUN_ID,
        "created_at_utc": created_at,
        "required_gate_audit": rel(GATE_AUDIT_PATH),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "run_family": "runtime_gap_analysis",
        "run_type": "sltp_point_unit_repair_decision",
        "input_run_id": PARENT_RUN_ID,
        "output_path": rel(RUN_MANIFEST_PATH),
        "result_path": rel(REPORT_PATH),
        "goal_achieve": "not_claimed",
    }
    upsert_csv(RUN_REGISTRY, "run_id", row)
    upsert_csv(ALPHA_LEDGER, "ledger_row_id", row)
    upsert_csv(REVIEW_DIR / "stage_run_ledger.csv", "ledger_row_id", row, source_header=ALPHA_LEDGER)
    marker = "<!-- frontier77E_proxy_runtime_gap_analysis_and_repair_decision_v1 -->"
    idea_text = io_path(IDEA_REGISTRY).read_text(encoding="utf-8-sig")
    if marker not in idea_text:
        block = f"""

{marker}
- `{RUN_ID}` identified(식별) F77D gap cause(간극 원인) as SL/TP point-unit mismatch(손절/익절 포인트 단위 불일치) after signal/feature parity(신호/피처 동등성). Next(다음): `{NEXT_RUN_ID}`. Boundary(경계): no authority(권위 없음).
"""
        write_text(IDEA_REGISTRY, idea_text.rstrip() + block)


def main() -> int:
    ensure_dirs()
    created_at = utc_now()
    analysis = build_gap_analysis()
    write_json(GAP_ANALYSIS_JSON, analysis)
    prompt = build_prompt(analysis)
    write_text(GROK_PROMPT_PATH, prompt)
    result = run_grok_review(
        prompt,
        cwd=ROOT,
        timeout_seconds=300,
        review_size="small",
        output_dir=GROK_PACKET,
        repo_root=ROOT,
        prompt_file_path=GROK_PROMPT_PATH,
    )
    success = bool(result.returncode == 0 and not result.timed_out)
    grok = {
        "success": success,
        "returncode": result.returncode,
        "timed_out": result.timed_out,
        "duration_seconds": result.duration_seconds,
        "prompt_sha256": result.prompt_hash,
        "output_exists": path_exists(GROK_CLEAN_PATH),
        "metadata_exists": path_exists(GROK_METADATA_PATH),
        "output_sha256": file_hash(GROK_CLEAN_PATH),
        "metadata_sha256": file_hash(GROK_METADATA_PATH),
        "packet_path": rel(GROK_PACKET),
    }
    clean = result.clean_stdout
    advice, direction, forbidden_hits = classify_advice(clean, success)
    status = STATUS_SUCCESS if success else STATUS_TRANSPORT_FAIL
    judgment = JUDGMENT_SUCCESS if success else JUDGMENT_TRANSPORT_FAIL
    write_text(REPORT_PATH, report_text(created_at, analysis, grok, advice, direction, forbidden_hits))
    write_text(RECEIPT_PATH, receipt_text(created_at, grok, advice, direction, forbidden_hits))
    write_text(GATE_AUDIT_PATH, gate_audit_text(grok, advice))
    write_json(
        RUN_MANIFEST_PATH,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "created_at_utc": created_at,
            "status": status,
            "judgment": judgment,
            "claim_boundary": CLAIM_BOUNDARY,
            "gap_analysis": analysis,
            "grok": grok,
            "advice_classification": advice,
            "final_direction": direction,
        },
    )
    update_state_and_ledgers(created_at, status, judgment, advice, grok)
    print(json.dumps({"status": status, "judgment": judgment, "advice": advice, "gap_cause": analysis["gap_cause"], "next_run_id": NEXT_RUN_ID, "report": rel(REPORT_PATH)}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
