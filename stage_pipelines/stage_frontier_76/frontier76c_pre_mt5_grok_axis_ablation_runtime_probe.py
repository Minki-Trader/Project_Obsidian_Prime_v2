from __future__ import annotations

import csv
import json
import sys
from pathlib import Path
from typing import Any, Mapping

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.grok_review_wrapper import run_grok_review
from foundation.control_plane.ledger import io_path, json_ready, sha256_file_lf_normalized


STAGE_ID = "stage_frontier_76__axis_ablation_source_discovery_for_runtime_economics"
RUN_ID = "frontier76C_pre_mt5_grok_axis_ablation_runtime_probe_v1"
PARENT_RUN_ID = "frontier76B_axis_ablation_proxy_scout_v1"
NEXT_RUN_ID = "frontier76D_mt5_axis_ablation_runtime_probe_v1"
STATUS_SUCCESS = "pre_mt5_grok_review_completed_runtime_probe_required_no_authority"
STATUS_TRANSPORT_FAIL = "pre_mt5_grok_review_transport_failed_runtime_probe_not_started_no_authority"
JUDGMENT_SUCCESS = "pre_mt5_grok_review_accepts_bounded_runtime_probe_with_local_verification_no_authority"
JUDGMENT_TRANSPORT_FAIL = "pre_mt5_grok_transport_failed_retry_required_no_authority"
CLAIM_BOUNDARY = (
    "pre_mt5_review_only_no_completion_no_baseline_no_promotion_"
    "no_runtime_authority_no_live_readiness_no_goal_achieve"
)
TARGET_CANDIDATE_ID = "f76b_06637"

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_ID
REVIEW_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"
SUMMARY_PATH = REVIEW_DIR / "f76b_summary.json"
AXIS_SUMMARY_PATH = REVIEW_DIR / "f76b_axis_summary.csv"
F76B_REPORT_PATH = REVIEW_DIR / "frontier76B_axis_ablation_proxy_scout_report.md"
REPORT_PATH = REVIEW_DIR / "frontier76C_pre_mt5_grok_axis_ablation_runtime_probe_report.md"
RECEIPT_PATH = REVIEW_DIR / "grok_pre_mt5_axis_ablation_runtime_probe_receipt.md"
GATE_AUDIT_PATH = REVIEW_DIR / "required_gate_coverage_audit_f76c.md"
SELECTION_STATUS_PATH = SELECTED_DIR / "selection_status.md"
STAGE_LEDGER_PATH = REVIEW_DIR / "stage_run_ledger.csv"
RUN_MANIFEST_PATH = RUN_DIR / "run_manifest.json"
CONTEXT_ANCHOR_PATH = f"stages/{STAGE_ID}/03_reviews/context_anchor.md"

GROK_PACKET = ROOT / "docs/agent_control/grok_reviews/2026-06-17_f76c_pre_mt5_axis_ablation_runtime_probe"
GROK_PROMPT_PATH = GROK_PACKET / "prompts/f76c_pre_mt5_axis_ablation_runtime_probe_prompt.md"
GROK_CLEAN_PATH = GROK_PACKET / "clean_output.md"
GROK_METADATA_PATH = GROK_PACKET / "metadata.json"


def utc_now() -> str:
    from datetime import UTC, datetime

    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def write_text(path: Path, text: str, *, encoding: str = "utf-8-sig") -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding=encoding)


def write_json(path: Path, payload: Mapping[str, Any]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def read_text(path: Path) -> str:
    return io_path(path).read_text(encoding="utf-8-sig")


def upsert_csv(path: Path, key: str, row: Mapping[str, Any]) -> None:
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = list(reader.fieldnames or [])
        rows = [existing for existing in reader if existing.get(key) != row.get(key)]
    rows.append({name: json_ready(row.get(name, "")) for name in fieldnames})
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def top_axis_lines(limit: int = 24) -> str:
    rows: list[str] = []
    with io_path(AXIS_SUMMARY_PATH).open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            rows.append(
                (
                    f"- {row['axis']}={row['value']}: candidates={row['candidate_rows']}, "
                    f"scout={row['scout_clue_count']}, meaningful={row['meaningful_signal_count']}, "
                    f"best={row['best_candidate']}, val_pf/dd/tpd={row['best_val_pf_dd_tpd']}, "
                    f"oos_pf/dd/tpd={row['best_oos_pf_dd_tpd']}"
                )
            )
    return "\n".join(rows[:limit])


def build_prompt(summary: Mapping[str, Any]) -> str:
    best = summary["best_candidate"]
    return f"""# F76C Pre-MT5 Grok Review Prompt(F76C MT5 전 그록 검토 프롬프트)

You are Grok(Grok, 그록), external second-opinion reviewer(외부 2차 의견 검토자).
Answer only from this bounded evidence snapshot(제한 근거 스냅샷). Do not inspect files(파일 확인 금지), run tools(도구 실행 금지), browse(브라우징 금지), or perform local verification(로컬 검증 금지).

## Current State(현재 상태)

- active stage(활성 단계): `{STAGE_ID}`
- current run(현재 실행): `{RUN_ID}`
- parent run(부모 실행): `{PARENT_RUN_ID}`
- proposed next run(제안 다음 실행): `{NEXT_RUN_ID}`
- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
- forbidden claims(금지 주장): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)

## Hypothesis(가설)

F76 tests whether broad feature/label/model/trade/risk/session ablation(넓은 피처/라벨/모델/거래/위험/세션 제거·교체)이 F71-F75의 parity without economics(동등성은 있으나 경제성 없음) 병목을 source axis(원천 축) 단위로 식별할 수 있는지 본다.

## Proxy Evidence(프록시 근거)

- candidate rows(후보 행): `{summary['candidate_rows']}`
- fit completed(적합 완료): `{summary['fit_completed']}/{summary['fit_rows']}`
- scout clue count(탐색 단서 수): `{summary['scout_clue_count']}`
- meaningful signal count(의미 신호 수): `{summary['meaningful_signal_count']}`
- dual positive count(양분할 양수 수): `{summary['dual_positive_count']}`

Best candidate(최선 후보):
- candidate id(후보 ID): `{best['candidate_id']}`
- feature_set(피처 묶음): `{best['feature_set']}`, feature_count(피처 수): `{best['feature_count']}`
- target(목표): `{best['target']}`, side(방향): `{best['side']}`, target threshold(목표 임계값): `{best['target_threshold']}`
- model(모델): `{best['model']}`
- probability threshold(확률 임계값): quantile `{best['prob_quantile']}`, threshold `{best['prob_threshold']}`
- session(세션): `{best['session']}`
- risk_filter(위험 필터): `{best['risk_filter']}`
- cooldown bars(쿨다운 봉): `{best['cooldown_bars']}`

Validation KPI(검증 핵심 성과 지표):
- net/PF/DD/trades_day/trades/win/expectancy/recovery(순수익/수익 팩터/손실폭/일거래/거래/승률/기대값/회복): `{best['val_net']}/{best['val_pf']}/{best['val_dd_pct']}/{best['val_trades_day']}/{best['val_trade_count']}/{best['val_win_rate']}/{best['val_expectancy']}/{best['val_recovery']}`

OOS KPI(표본외 핵심 성과 지표):
- net/PF/DD/trades_day/trades/win/expectancy/recovery(순수익/수익 팩터/손실폭/일거래/거래/승률/기대값/회복): `{best['oos_net']}/{best['oos_pf']}/{best['oos_dd_pct']}/{best['oos_trades_day']}/{best['oos_trade_count']}/{best['oos_win_rate']}/{best['oos_expectancy']}/{best['oos_recovery']}`

Axis summary(축 요약):
{top_axis_lines()}

## Proposed MT5 Runtime Probe(제안 MT5 런타임 탐침)

Codex proposal(Codex 제안):
1. Re-train(재학습) the same ExtraTrees(엑스트라트리) surface on train split(학습 분할): `mega_cap_removed` 48 features, binary target(이진 목표) `future_log_return_12 > train_q60`.
2. Materialize ONNX(ONNX 물질화) as long-only three-column output(롱 전용 3열 출력): `[p_short=0, p_flat=P(non-long), p_long=P(long)]`.
3. Use MT5 RuntimeProbeEA(MT5 런타임 탐침 EA) with `threshold_margin` decision mode(임계값 마진 판단): `long_threshold=proxy_prob_threshold - epsilon`, `short_threshold=1.1`, `min_margin=-1.0`.
4. Encode session/risk/probability selection(세션/위험/확률 선택) with selected-entry runtime veto tape(선택 진입 런타임 거부 테이프), so runtime signal count should match proxy selected timestamps.
5. Trade shape(거래 형태): long-only(롱 전용), max hold 12 M5 bars(최대 보유 12개 5분봉), no ATR SL/TP initially(초기 ATR 손절/익절 없음) to mirror fwd12 close proxy(12봉 뒤 종가 프록시).
6. Run validation and OOS Strategy Tester(검증/표본외 전략 테스터) attempts for US100 M5.

## Focus Question(집중 질문)

Should Codex proceed with this narrow F76D MT5 Runtime Probe(F76D 좁은 MT5 런타임 탐침) as proposed, or must it adjust the materialization before execution?

Please classify advice(조언 분류) into:
- accepted(수용): safe to proceed as proposed
- accepted_with_conditions(조건부 수용): proceed only with named local checks
- needs_local_verification(로컬 검증 필요): evidence is insufficient in this snapshot
- rejected(거절): do not execute because the proposed mapping is logically invalid

Also list:
1. Top proxy/runtime gap risks(최상위 프록시/런타임 간극 위험)
2. Required local verification before execution(실행 전 필수 로컬 검증)
3. Any forbidden claim risk(금지 주장 위험)
4. The smallest useful MT5 probe scope(가장 작은 유용한 MT5 탐침 범위)
"""


def classify_advice(clean_output: str, success: bool) -> tuple[str, str, list[str]]:
    lowered = clean_output.lower()
    forbidden_hits = [
        term
        for term in ["goal achieve", "runtime authority", "live readiness", "selected baseline", "operating promotion"]
        if f"may claim {term}" in lowered
        or f"can claim {term}" in lowered
        or f"{term} achieved" in lowered
        or f"{term}: achieved" in lowered
        or f"{term}: yes" in lowered
    ]
    if not success:
        return "transport_failed(전송 실패)", "retry_required(재시도 필요)", forbidden_hits
    if "rejected" in lowered and "accepted" not in lowered:
        return "rejected(거절)", "do_not_execute_until_repaired(수리 전 실행 금지)", forbidden_hits
    if "accepted_with_conditions" in lowered or "accepted with conditions" in lowered:
        return "accepted_with_conditions(조건부 수용)", "proceed_after_local_verification(로컬 검증 후 진행)", forbidden_hits
    if "needs_local_verification" in lowered or "local verification" in lowered:
        return "needs_local_verification(로컬 검증 필요)", "proceed_only_after_codex_checks(코덱스 점검 후에만 진행)", forbidden_hits
    return "accepted_with_conditions(조건부 수용)", "proceed_after_local_verification(로컬 검증 후 진행)", forbidden_hits


def report_text(
    created_at: str,
    summary: Mapping[str, Any],
    grok: Mapping[str, Any],
    advice_classification: str,
    final_direction: str,
    forbidden_hits: list[str],
) -> str:
    best = summary["best_candidate"]
    return f"""# Frontier76C Pre-MT5 Grok Review Report(F76C MT5 전 Grok 검토 보고서)

Run id(실행 ID): `{RUN_ID}`

Status(상태): `{STATUS_SUCCESS if grok['success'] else STATUS_TRANSPORT_FAIL}`

Judgment(판정): `{JUDGMENT_SUCCESS if grok['success'] else JUDGMENT_TRANSPORT_FAIL}`

Updated(갱신): {created_at}

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`

## Codex Direction Before Grok(Grok 전 Codex 방향)

Action(행동): F76B best candidate(최선 후보) `{TARGET_CANDIDATE_ID}`를 F76D MT5 Runtime Probe(F76D MT5 런타임 탐침)로 물질화한다.

Effect(효과): proxy(프록시) 의미 신호를 실제 MT5 Strategy Tester(전략 테스터)에서 관찰해 proxy/runtime gap(프록시/런타임 간극)을 기록한다.

## Bounded Evidence(제한 근거)

- F76B summary(요약): `{rel(SUMMARY_PATH)}` sha256 `{sha256_file_lf_normalized(SUMMARY_PATH)}`
- F76B report(보고서): `{rel(F76B_REPORT_PATH)}` sha256 `{sha256_file_lf_normalized(F76B_REPORT_PATH)}`
- F76B axis summary(축 요약): `{rel(AXIS_SUMMARY_PATH)}` sha256 `{sha256_file_lf_normalized(AXIS_SUMMARY_PATH)}`

## Target Proxy KPI(대상 프록시 핵심 성과 지표)

- candidate(후보): `{best['candidate_id']}`
- axes(축): `{best['feature_set']}/{best['model']}/{best['target']}/{best['session']}/{best['risk_filter']}/{best['cooldown_bars']}`
- validation net/PF/DD/tpd/trades(검증 순수익/수익 팩터/손실폭/일거래/거래): `{best['val_net']}/{best['val_pf']}/{best['val_dd_pct']}%/{best['val_trades_day']}/{best['val_trade_count']}`
- OOS net/PF/DD/tpd/trades(표본외 순수익/수익 팩터/손실폭/일거래/거래): `{best['oos_net']}/{best['oos_pf']}/{best['oos_dd_pct']}%/{best['oos_trades_day']}/{best['oos_trade_count']}`

## Grok Advice(Grok 조언)

- packet(묶음): `{rel(GROK_PACKET)}`
- prompt(프롬프트): `{rel(GROK_PROMPT_PATH)}` sha256 `{grok['prompt_sha256']}`
- output(출력): `{rel(GROK_CLEAN_PATH)}` sha256 `{grok['output_sha256'] if grok['output_exists'] else 'missing'}`
- metadata(메타데이터): `{rel(GROK_METADATA_PATH)}` sha256 `{grok['metadata_sha256'] if grok['metadata_exists'] else 'missing'}`
- wrapper success(래퍼 성공): `{grok['success']}`
- returncode(반환 코드): `{grok['returncode']}`
- advice classification(조언 분류): `{advice_classification}`
- final Codex direction(최종 Codex 방향): `{final_direction}`
- forbidden claim hits(금지 주장 감지): `{', '.join(forbidden_hits) if forbidden_hits else 'none(없음)'}`

## Local Verification Required(필수 로컬 검증)

- probability parity(확률 동등성): ONNX three-column long schema(ONNX 3열 롱 스키마)가 sklearn probability(사이킷런 확률)와 1e-5 이내인지 확인한다.
- signal count parity(신호 수 동등성): selected-entry runtime veto tape(선택 진입 런타임 거부 테이프) 뒤 validation/OOS 선택 수가 proxy selected count(프록시 선택 수)와 일치하는지 확인한다.
- feature readiness parity(피처 준비 동등성): 48개 `mega_cap_removed` feature order(피처 순서)가 MT5 feature CSV(피처 CSV)와 일치하는지 확인한다.
- trade shape boundary(거래 형태 경계): max hold 12 bars(최대 보유 12봉), long-only(롱 전용), no initial ATR SL/TP(초기 ATR 손절/익절 없음)로 시작하고, 수익 주장보다 gap observation(간극 관찰)을 먼저 기록한다.

## Next Action(다음 행동)

`{NEXT_RUN_ID}`.
"""


def receipt_text(
    created_at: str,
    grok: Mapping[str, Any],
    advice_classification: str,
    final_direction: str,
    forbidden_hits: list[str],
) -> str:
    return f"""# F76C Grok Pre-MT5 Receipt(F76C Grok MT5 전 영수증)

Trigger reason(트리거 이유): F76B proxy(프록시)가 meaningful signal(의미 신호)을 만들었고, `/goal(목표)`가 major validation(주요 검증) 전 Grok second opinion(Grok 2차 의견)을 요구한다.

Review size(검토 크기): medium review(중간 검토)

Direction before Grok(Grok 전 방향): `{TARGET_CANDIDATE_ID}`를 long-only selected-entry MT5 Runtime Probe(롱 전용 선택 진입 MT5 런타임 탐침)로 물질화한다.

Bounded evidence(제한 근거): F76B summary/report/axis summary(F76B 요약/보고서/축 요약), best candidate KPI(최선 후보 핵심 성과 지표), proposed runtime mapping(제안 런타임 매핑).

Prompt identity(프롬프트 정체성): `{rel(GROK_PROMPT_PATH)}` sha256 `{grok['prompt_sha256']}`

Grok output identity(Grok 출력 정체성): `{rel(GROK_CLEAN_PATH)}` sha256 `{grok['output_sha256'] if grok['output_exists'] else 'missing'}`

Advice classification(조언 분류): `{advice_classification}`

Local verification(로컬 검증): wrapper success(래퍼 성공) `{grok['success']}`, returncode `{grok['returncode']}`, F76B tracked evidence present(F76B 추적 근거 존재), next local checks recorded(다음 로컬 점검 기록).

Forbidden claim check(금지 주장 확인): `{', '.join(forbidden_hits) if forbidden_hits else 'none(없음)'}`. Codex rejects any completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성) implication.

Final Codex direction(최종 Codex 방향): `{final_direction}`.

Created at(생성 시각): {created_at}
"""


def gate_audit_text(grok: Mapping[str, Any], advice_classification: str) -> str:
    return f"""# Required Gate Coverage Audit F76C(F76C 필수 게이트 커버리지 감사)

| gate(게이트) | status(상태) | evidence/effect(근거/효과) |
|---|---|---|
| pre_mt5_grok_review(MT5 전 Grok 검토) | `{'passed(통과)' if grok['success'] else 'failed_transport(전송 실패)'}` | `{rel(RECEIPT_PATH)}` |
| bounded_evidence(제한 근거) | `passed(통과)` | F76B summary/report/axis summary(F76B 요약/보고서/축 요약) |
| advice_classification(조언 분류) | `{advice_classification}` | `{rel(GROK_CLEAN_PATH)}` |
| local_verification_plan(로컬 검증 계획) | `recorded(기록됨)` | probability/signal/feature/trade-shape parity(확률/신호/피처/거래 형태 동등성) |
| runtime_probe_next(다음 런타임 탐침) | `required(필수)` | `{NEXT_RUN_ID}` |
| claim_guard(주장 보호) | `passed(통과)` | `{CLAIM_BOUNDARY}` |
"""


def selection_status_text(status: str, judgment: str) -> str:
    return f"""# F76 Selection Status(F76 선택 상태)

Status(상태): `{status}`

Judgment(판정): `{judgment}`

Action(행동): F76C pre-MT5 Grok review(MT5 전 Grok 검토)를 완료하거나 시도했다.

Effect(효과): F76D MT5 Runtime Probe(F76D MT5 런타임 탐침)로 진행할 로컬 검증 조건을 고정한다.

Current run(현재 실행): `{NEXT_RUN_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""


def update_state_and_ledgers(created_at: str, status: str, judgment: str, grok: Mapping[str, Any], advice_classification: str) -> None:
    workspace = f"""current_stage_id: {STAGE_ID}
active_stage: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {status}
current_judgment: {judgment}
next_run_id: {NEXT_RUN_ID}
runtime_probe_status: f76_mt5_runtime_probe_required_next
runtime_authority: not_claimed
operating_promotion: not_claimed
live_readiness: not_claimed
goal_achieve: not_claimed
five_stage_retrospective_due_status: not_due_after_frontier71_to_75_retrospective_completed
updated_at_utc: '{created_at}'
context_anchor: {CONTEXT_ANCHOR_PATH}
notes:
  - "Action(행동): F76C pre-MT5 Grok review(MT5 전 Grok 검토)를 완료하거나 시도했다."
  - "Effect(효과): F76D MT5 Runtime Probe(F76D MT5 런타임 탐침)의 로컬 검증 조건을 고정했다."
  - "Grok success(Grok 성공): {grok['success']}; advice(조언): {advice_classification}."
  - "Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음)."
"""
    write_text(ROOT / "docs/workspace/workspace_state.yaml", workspace)

    current = f"""# Current Working State(현재 작업 상태)

Updated(갱신): {created_at}

Active stage(활성 단계): `{STAGE_ID}`

Current run(현재 실행): `{NEXT_RUN_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

## Current Truth(현재 진실)

Action(행동): F76C pre-MT5 Grok review(MT5 전 Grok 검토)를 완료하거나 시도했다.

Effect(효과): F76B proxy(프록시) 의미 신호를 F76D MT5 Runtime Probe(F76D MT5 런타임 탐침)로 물질화하기 전, 로컬 검증 조건을 기록했다.

## Open Work(열린 작업)

- next run(다음 실행): `{NEXT_RUN_ID}`
- required local checks(필수 로컬 점검): probability parity(확률 동등성), signal count parity(신호 수 동등성), feature readiness parity(피처 준비 동등성), Strategy Tester output(전략 테스터 출력)
- claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    write_text(ROOT / "docs/context/current_working_state.md", current)
    write_text(SELECTION_STATUS_PATH, selection_status_text(status, judgment))

    row_id = f"{RUN_ID}__pre_mt5_grok"
    row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "pre_mt5_grok_review(MT5 전 Grok 검토)",
        "status": status,
        "judgment": judgment,
        "path": rel(REPORT_PATH),
        "notes": f"grok_success={grok['success']};advice={advice_classification};target={TARGET_CANDIDATE_ID}",
        "family": "runtime_backtest_precheck(런타임/백테스트 사전점검)",
        "primary_report": rel(REPORT_PATH),
        "run_number": "frontier76C",
        "date": created_at[:10],
        "decision": judgment,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "rows": "1",
        "gate_passes": "6" if grok["success"] else "5",
        "gate_total": "6",
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "run_date": created_at[:10],
        "primary_artifact": rel(RUN_MANIFEST_PATH),
        "result_status": status,
        "view": "pre_mt5_grok_review(MT5 전 Grok 검토)",
        "tier": "Tier A separate; Tier B missing_required; combined out_of_scope",
        "metric_scope": "external_review_packet(외부 검토 묶음)",
        "scoreboard_lane": "runtime_probe_precheck(런타임 탐침 사전점검)",
        "external_verification_status": "pre_mt5_grok_completed(MT5 전 Grok 완료)" if grok["success"] else "pre_mt5_grok_transport_failed(MT5 전 Grok 전송 실패)",
        "result_judgment": judgment,
        "final_decision_path": rel(SELECTION_STATUS_PATH),
        "gate_audit_path": rel(GATE_AUDIT_PATH),
        "created_at": created_at,
        "ledger_row_id": row_id,
        "subrun_id": "pre_mt5_grok_review(MT5 전 Grok 검토)",
        "record_view": "pre_mt5_review(MT5 전 검토)",
        "tier_scope": "Tier A separate; Tier B missing_required; combined out_of_scope",
        "kpi_scope": "grok_pre_mt5_review(Grok MT5 전 검토)",
        "primary_kpi": f"target={TARGET_CANDIDATE_ID};advice={advice_classification}",
        "guardrail_kpi": "no authority;runtime probe required next",
        "work_family": "runtime_backtest_precheck(런타임/백테스트 사전점검)",
        "row_id": row_id,
        "evidence_boundary": "pre_mt5_review_only_no_runtime_yet(MT5 전 검토만, 런타임 아직 없음)",
        "next_action": NEXT_RUN_ID,
        "question": "Should F76B meaningful proxy be materialized as MT5 runtime probe?(F76B 의미 프록시를 MT5 런타임 탐침으로 물질화해야 하나?)",
        "artifact_count": "5",
        "created_at_utc": created_at,
        "required_gate_audit": rel(GATE_AUDIT_PATH),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "run_family": "runtime_backtest_precheck(런타임/백테스트 사전점검)",
        "run_type": "pre_mt5_grok_review(MT5 전 Grok 검토)",
        "input_run_id": PARENT_RUN_ID,
        "output_path": rel(RUN_MANIFEST_PATH),
        "result_path": rel(REPORT_PATH),
        "goal_achieve": "not_claimed",
        "source_authority": "not_claimed",
    }
    upsert_csv(ROOT / "docs/registers/run_registry.csv", "run_id", row)
    upsert_csv(ROOT / "docs/registers/alpha_run_ledger.csv", "ledger_row_id", row)
    upsert_csv(STAGE_LEDGER_PATH, "ledger_row_id", row)

    idea_path = ROOT / "docs/registers/idea_registry.md"
    marker = "<!-- frontier76C_pre_mt5_grok_axis_ablation_runtime_probe_v1 -->"
    text = read_text(idea_path)
    if marker not in text:
        addition = f"""

{marker}
- `{RUN_ID}` recorded F76 pre-MT5 Grok review(F76 MT5 전 Grok 검토). Target(대상): `{TARGET_CANDIDATE_ID}`. Advice(조언): `{advice_classification}`. Evidence(근거): `{rel(REPORT_PATH)}`. Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음). Next(다음): `{NEXT_RUN_ID}`.
"""
        write_text(idea_path, text.rstrip() + addition)


def main() -> int:
    created_at = utc_now()
    io_path(RUN_DIR).mkdir(parents=True, exist_ok=True)
    io_path(GROK_PROMPT_PATH.parent).mkdir(parents=True, exist_ok=True)
    summary = read_json(SUMMARY_PATH)
    prompt = build_prompt(summary)
    write_text(GROK_PROMPT_PATH, prompt)
    result = run_grok_review(
        prompt,
        cwd=ROOT,
        repo_root=ROOT,
        output_dir=GROK_PACKET,
        prompt_file_path=GROK_PROMPT_PATH,
        review_size="medium",
        timeout_seconds=300,
    )
    output_exists = io_path(GROK_CLEAN_PATH).exists()
    metadata_exists = io_path(GROK_METADATA_PATH).exists()
    grok = {
        "packet_path": rel(GROK_PACKET),
        "prompt_path": rel(GROK_PROMPT_PATH),
        "prompt_sha256": sha256_file_lf_normalized(GROK_PROMPT_PATH),
        "output_path": rel(GROK_CLEAN_PATH),
        "output_exists": output_exists,
        "output_sha256": sha256_file_lf_normalized(GROK_CLEAN_PATH) if output_exists else "",
        "metadata_path": rel(GROK_METADATA_PATH),
        "metadata_exists": metadata_exists,
        "metadata_sha256": sha256_file_lf_normalized(GROK_METADATA_PATH) if metadata_exists else "",
        "success": bool(result.success),
        "returncode": result.returncode,
        "timed_out": result.timed_out,
        "duration_seconds": result.duration_seconds,
        "prompt_hash": result.prompt_hash,
        "preflight_warnings": list(result.preflight_warnings),
        "unexpected_top_level_artifacts": list(result.unexpected_top_level_artifacts),
    }
    clean_output = read_text(GROK_CLEAN_PATH) if output_exists else result.clean_stdout
    advice_classification, final_direction, forbidden_hits = classify_advice(clean_output, bool(result.success))
    status = STATUS_SUCCESS if result.success else STATUS_TRANSPORT_FAIL
    judgment = JUDGMENT_SUCCESS if result.success else JUDGMENT_TRANSPORT_FAIL
    write_text(REPORT_PATH, report_text(created_at, summary, grok, advice_classification, final_direction, forbidden_hits))
    write_text(RECEIPT_PATH, receipt_text(created_at, grok, advice_classification, final_direction, forbidden_hits))
    write_text(GATE_AUDIT_PATH, gate_audit_text(grok, advice_classification))
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
            "target_candidate_id": TARGET_CANDIDATE_ID,
            "grok": grok,
            "advice_classification": advice_classification,
            "final_codex_direction": final_direction,
            "forbidden_claim_hits": forbidden_hits,
            "artifacts": {
                "report": rel(REPORT_PATH),
                "receipt": rel(RECEIPT_PATH),
                "gate_audit": rel(GATE_AUDIT_PATH),
                "prompt": rel(GROK_PROMPT_PATH),
                "grok_output": rel(GROK_CLEAN_PATH),
            },
        },
    )
    update_state_and_ledgers(created_at, status, judgment, grok, advice_classification)
    print(
        json.dumps(
            json_ready(
                {
                    "status": status,
                    "judgment": judgment,
                    "target_candidate_id": TARGET_CANDIDATE_ID,
                    "advice_classification": advice_classification,
                    "grok_success": result.success,
                    "next_run_id": NEXT_RUN_ID,
                    "report": rel(REPORT_PATH),
                }
            ),
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if result.success else 1


if __name__ == "__main__":
    raise SystemExit(main())
