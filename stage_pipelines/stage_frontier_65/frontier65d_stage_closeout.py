from __future__ import annotations

import argparse
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists  # noqa: E402
from foundation.models.onnx_bridge import sha256_file  # noqa: E402
from stage_pipelines.stage_frontier_03 import frontier03b_regime_asymmetric_label_proxy_scout as f03b  # noqa: E402
from stage_pipelines.stage_frontier_64 import frontier64c_handoff_verification as f64c  # noqa: E402
from stage_pipelines.stage_frontier_65 import frontier65_gap_attribution as f65b  # noqa: E402
from stage_pipelines.stage_frontier_65 import frontier65c_targeted_sltp_runtime_probe as f65c  # noqa: E402


STAGE_ID = f65b.STAGE_ID
RUN_ID = "frontier65D_stage_closeout_runtime_semantics_gap_attribution_v1"
RUN_NUMBER = "frontier65D"
PARENT_RUN_ID = f65c.RUN_ID
NEXT_STAGE_ID = "stage_frontier_66__runtime_unit_aligned_exit_economics_pf_source_after_semantics_gap"
NEXT_RUN_ID = "frontier66A_stage_open_runtime_unit_aligned_exit_economics_pf_source_v1"

STAGE_ROOT = f65b.STAGE_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
SELECTED_ROOT = STAGE_ROOT / "04_selected"

GROK_PACKET = Path("docs/agent_control/grok_reviews/2026-06-16_frontier65_stage_closeout_review/small_review")
GROK_PROMPT = GROK_PACKET / "prompt.md"
GROK_CLEAN_OUTPUT = GROK_PACKET / "clean_output.md"
GROK_METADATA = GROK_PACKET / "metadata.json"

F65B_FINAL = f65b.RUN_B_ROOT / "gap_attribution_summary.json"
F65C_FINAL = f65c.RUN_ROOT / "final_decision.json"
F65C_GAP_REPORT = REVIEWS_ROOT / "proxy_runtime_gap_after_unit_adjustment_report.md"
F65C_RUNTIME_REPORT = REVIEWS_ROOT / "runtime_probe_unit_adjusted_report.md"
COMPILE_RESULT = Path("docs/agent_control/runtime_probe_backfill/frontier_runtime_backfill_mt5_compile_result.json")
COMPILE_LOG = Path("docs/agent_control/runtime_probe_backfill/frontier_runtime_backfill_mt5_compile.log")

CLOSEOUT_STATUS = (
    "closed_preserved_clue_sltp_unit_semantics_supported_economics_incomplete_no_authority"
    "(마감, 보존 단서, 손절/익절 단위 의미 지원, 경제성 불완전, 권위 없음)"
)
CLOSEOUT_JUDGMENT = (
    "preserved_clue_sltp_unit_semantics_supported_but_economics_incomplete_no_authority"
    "(보존 단서, 손절/익절 단위 의미 지원, 그러나 경제성 불완전, 권위 없음)"
)
CLOSEOUT_LABEL = "preserved_clue(보존 단서)"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Close Frontier65 runtime semantics gap attribution stage.")
    parser.add_argument("--write-closeout-prompt-only", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    ensure_dirs()
    if args.write_closeout_prompt_only:
        f03b.write_text_sig(GROK_PROMPT, closeout_prompt(load_local_context(require_grok=False)))
        print(json.dumps({"status": "wrote_closeout_prompt", "prompt": GROK_PROMPT.as_posix()}, ensure_ascii=False, indent=2))
        return 0

    created_at = utc_now()
    context = load_local_context(require_grok=True)
    final = build_final(created_at, context)
    write_artifacts(final)
    update_registers(final)
    print(
        json.dumps(
            json_ready(
                {
                    "status": final["status"],
                    "judgment": final["judgment"],
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "next_stage_id": NEXT_STAGE_ID,
                    "next_run_id": NEXT_RUN_ID,
                }
            ),
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


def ensure_dirs() -> None:
    for path in (RUN_ROOT, REVIEWS_ROOT, SELECTED_ROOT, GROK_PACKET):
        io_path(path).mkdir(parents=True, exist_ok=True)


def load_local_context(require_grok: bool) -> dict[str, Any]:
    required = [F65B_FINAL, F65C_FINAL, F65C_GAP_REPORT, F65C_RUNTIME_REPORT]
    if require_grok:
        required.extend([GROK_PROMPT, GROK_CLEAN_OUTPUT, GROK_METADATA])
    missing = [path.as_posix() for path in required if not path_exists(path)]
    if missing:
        raise FileNotFoundError(f"F65D closeout evidence missing(F65D 마감 근거 누락): {missing}")
    context: dict[str, Any] = {
        "f65b_final": read_json(F65B_FINAL),
        "f65c_final": read_json(F65C_FINAL),
        "f65c_gap_report": read_text(F65C_GAP_REPORT),
        "f65c_runtime_report": read_text(F65C_RUNTIME_REPORT),
        "compile_result": read_json(COMPILE_RESULT) if path_exists(COMPILE_RESULT) else {},
        "compile_log_hash": sha256_file(COMPILE_LOG) if path_exists(COMPILE_LOG) else "",
    }
    if require_grok:
        context.update(
            {
                "grok_clean": read_text(GROK_CLEAN_OUTPUT),
                "grok_metadata": read_json(GROK_METADATA),
            }
        )
    return context


def build_final(created_at: str, context: Mapping[str, Any]) -> dict[str, Any]:
    f65b_final = dict(context["f65b_final"])
    f65c_final = dict(context["f65c_final"])
    runtime_rows = list(f65c_final.get("runtime_rows", []))
    gap_rows = list(f65c_final.get("proxy_runtime_gap_rows", []))
    diagnostics = dict(f65c_final.get("post_run_diagnostics", {}))
    grok_clean = str(context.get("grok_clean", ""))
    grok_metadata = dict(context.get("grok_metadata", {}))
    return {
        "created_at_utc": created_at,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "parent_run_id": PARENT_RUN_ID,
        "next_stage_id": NEXT_STAGE_ID,
        "next_run_id": NEXT_RUN_ID,
        "status": CLOSEOUT_STATUS,
        "judgment": CLOSEOUT_JUDGMENT,
        "closeout_label": CLOSEOUT_LABEL,
        "hypothesis": (
            "runtime_semantics_gap_after_hazard_gate_failure"
            "(해저드 게이트 실패 뒤 런타임 의미 차이)"
        ),
        "result_subject": "F65 proxy-runtime gap attribution(F65 프록시-런타임 차이 귀속)",
        "evidence_available": [
            F65B_FINAL.as_posix(),
            F65C_FINAL.as_posix(),
            F65C_RUNTIME_REPORT.as_posix(),
            F65C_GAP_REPORT.as_posix(),
            GROK_CLEAN_OUTPUT.as_posix(),
        ],
        "evidence_missing": [
            "runtime-unit-aligned proxy rebuild(런타임 단위 정렬 프록시 재구축)",
            "PF/DD parity closure(PF/DD 동등성 폐쇄)",
            "completion four-axis review(완성 네 축 검토)",
        ],
        "claim_boundary": (
            "runtime_probe_observation_and_preserved_clue_only_no_completion_no_baseline_no_promotion_"
            "no_runtime_authority_no_live_readiness_no_goal_achieve"
            "(런타임 탐침 관찰과 보존 단서만, 완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음)"
        ),
        "primary_clue": (
            "sltp_unit_semantics_gap_between_proxy_price_units_and_mt5_points"
            "(프록시 가격 단위와 MT5 포인트 손절/익절 의미 차이)"
        ),
        "decision_gap_read": (
            "raw adapter signal(원 어댑터 신호), runtime veto tape(런타임 차단 테이프), "
            "entry transition gate(진입 전환 게이트)가 signal count gap(신호 수 차이)을 설명한다."
        ),
        "economics_gap_read": (
            "SL/TP unit adjustment(손절/익절 단위 보정)은 exit shape(청산 형태)를 크게 개선했지만 "
            "PF/DD economics(PF/DD 경제성)는 아직 불완전하다."
        ),
        "runtime_rows": runtime_rows,
        "proxy_runtime_gap_rows": gap_rows,
        "diagnostics": diagnostics,
        "f65b_primary_attribution_clue": f65b_final.get("primary_attribution_clue"),
        "grok_closeout_classification": classify_grok(grok_clean),
        "grok_metadata": grok_metadata,
        "compile_result": context.get("compile_result", {}),
        "compile_log_hash": context.get("compile_log_hash", ""),
        "artifact_hashes": artifact_hashes(),
        "local_verification": local_verification_summary(f65c_final, diagnostics),
        "next_condition": (
            "F66 should lock point/price unit contract(F66은 포인트/가격 단위 계약 고정) and rebuild "
            "runtime-aligned exit economics(런타임 정렬 청산 경제성) before new PF source(새 PF 원천) claims."
        ),
    }


def local_verification_summary(f65c_final: Mapping[str, Any], diagnostics: Mapping[str, Any]) -> dict[str, Any]:
    rows = {str(row.get("split")): dict(row) for row in f65c_final.get("runtime_rows", [])}
    exit_rows = {str(row.get("split")): dict(row) for row in diagnostics.get("exit_shape_delta_rows", [])}
    return {
        "runtime_probe_completed": all(str(row.get("runtime_status")) == "completed" for row in rows.values()),
        "report_completed": all(str(row.get("report_status")) == "completed" for row in rows.values()),
        "feature_ready_diff": {split: row.get("feature_ready_diff") for split, row in rows.items()},
        "validation_pf_dd_density": {
            "profit_factor": rows.get("validation_is", {}).get("profit_factor"),
            "max_drawdown_percent": rows.get("validation_is", {}).get("max_drawdown_percent"),
            "runtime_trades_per_day": rows.get("validation_is", {}).get("runtime_trades_per_day"),
        },
        "oos_pf_dd_density": {
            "profit_factor": rows.get("oos", {}).get("profit_factor"),
            "max_drawdown_percent": rows.get("oos", {}).get("max_drawdown_percent"),
            "runtime_trades_per_day": rows.get("oos", {}).get("runtime_trades_per_day"),
        },
        "exit_shape_delta": exit_rows,
        "forbidden_claims": {
            "completion": "not_claimed(주장 없음)",
            "baseline": "not_claimed(주장 없음)",
            "promotion": "not_claimed(주장 없음)",
            "runtime_authority": "not_claimed(주장 없음)",
            "live_readiness": "not_claimed(주장 없음)",
            "goal_achieve": "not_claimed(주장 없음)",
        },
    }


def closeout_prompt(context: Mapping[str, Any]) -> str:
    f65c_final = dict(context["f65c_final"])
    rows = {str(row.get("split")): dict(row) for row in f65c_final.get("runtime_rows", [])}
    diagnostics = dict(f65c_final.get("post_run_diagnostics", {}))
    exit_rows = {str(row.get("split")): dict(row) for row in diagnostics.get("exit_shape_delta_rows", [])}
    return f"""Frontier65 stage closeout review(전선65 단계 마감 검토)입니다.

Please answer only from this bounded snapshot(제한 스냅샷). Do not inspect files(파일 확인 금지), run tools(도구 실행 금지), browse(브라우징 금지), or perform local verification(로컬 검증 금지). If evidence is insufficient, say `needs_local_verification(로컬 검증 필요)`.

## Codex Direction Before Grok(그록 전 코덱스 방향)

- Proposed closeout label(제안 마감 라벨): `preserved_clue(보존 단서)`.
- Proposed judgment(제안 판정): `{CLOSEOUT_JUDGMENT}`.
- Claim boundary(주장 경계): runtime_probe_observation(런타임 탐침 관찰) and preserved clue(보존 단서) only. No completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음).
- Proposed next stage(제안 다음 단계): `{NEXT_STAGE_ID}` / `{NEXT_RUN_ID}`.

## F65B Attribution Snapshot(F65B 귀속 스냅샷)

- feature_ready_diff(피처 준비 차이): validation/OOS `0/0`.
- Signal layer(신호 층): raw adapter(원 어댑터) `5269/4206`, runtime veto(런타임 차단) `1196/881`, expected after veto(차단 후 예상) `4073/3325`, entry transition block(진입 전환 차단) `2973/2483`, actual non-flat(실제 비관망) `1100/842`, fills(체결) `1098/838`.
- Economic layer before unit adjustment(단위 보정 전 경제성 층): validation/OOS MT5 PF `0.35/0.70`, MT5 DD `28.23/7.92`, proxy PF `1.07267/1.10808`, proxy DD `4.31916/3.15376`.
- Primary clue(주요 단서): `sltp_unit_semantics_gap_between_proxy_price_units_and_mt5_points(프록시 가격 단위와 MT5 포인트 손절/익절 의미 차이)`.

## F65C Targeted MT5 Runtime Probe(F65C 표적 MT5 런타임 탐침)

Action(행동): keep F64D direction adapter ONNX(방향 어댑터 온엑스), feature matrix(피처 행렬), runtime veto tape(런타임 차단 테이프), and entry transition gate(진입 전환 게이트), then multiply ATR SL/TP point thresholds(ATR 손절/익절 포인트 문턱값) by `100`.

Effect(효과): test only whether SL/TP unit semantics(손절/익절 단위 의미) caused the exit-shape gap(청산 형태 차이).

| split(분할) | PF(수익 팩터) | DD%(손실폭) | trades/day(일 거래) | signal diff(신호 차이) | feature diff(피처 차이) |
|---|---:|---:|---:|---:|---:|
| validation_is | {rows.get('validation_is', {}).get('profit_factor')} | {rows.get('validation_is', {}).get('max_drawdown_percent')} | {rows.get('validation_is', {}).get('runtime_trades_per_day')} | {rows.get('validation_is', {}).get('signal_count_diff')} | {rows.get('validation_is', {}).get('feature_ready_diff')} |
| oos | {rows.get('oos', {}).get('profit_factor')} | {rows.get('oos', {}).get('max_drawdown_percent')} | {rows.get('oos', {}).get('runtime_trades_per_day')} | {rows.get('oos', {}).get('signal_count_diff')} | {rows.get('oos', {}).get('feature_ready_diff')} |

Exit shape delta(청산 형태 변화):

- validation_is: stop rate(손절률) `79.51% -> {pct(exit_rows.get('validation_is', {}).get('stop_rate_unit_adjusted'))}`, close_max_hold rate(최대보유 청산률) `0.00% -> {pct(exit_rows.get('validation_is', {}).get('close_max_hold_rate_unit_adjusted'))}`, median hold(중앙 보유) `600 sec(초)`.
- oos: stop rate(손절률) `67.54% -> {pct(exit_rows.get('oos', {}).get('stop_rate_unit_adjusted'))}`, close_max_hold rate(최대보유 청산률) `0.00% -> {pct(exit_rows.get('oos', {}).get('close_max_hold_rate_unit_adjusted'))}`, median hold(중앙 보유) `600 sec(초)`.

## Codex Read(코덱스 판독)

- Supported clue(지원된 단서): unit adjustment(단위 보정)이 exit shape(청산 형태)를 proxy-like maxhold behavior(프록시 유사 최대보유 행동) 쪽으로 크게 이동시켰다.
- Still incomplete(아직 불완전): validation PF(검증 수익 팩터) is below `1`, validation/OOS DD(검증/OOS 손실폭) are `21.83/14.66`, so four-axis target(네 축 목표)은 닫히지 않았다.
- Proposed closeout(제안 마감): `preserved_clue(보존 단서)`, not negative memory(부정 기억), not completion candidate(완성 후보).

## Review Request(검토 요청)

1. Classification(분류): `accepted(수용)`, `rejected(거절)`, or `needs_local_verification(로컬 검증 필요)`.
2. Is preserved clue(보존 단서) the correct closeout label?
3. Is F66 next-stage direction(다음 단계 방향) reasonable: runtime-unit-aligned exit economics(런타임 단위 정렬 청산 경제성) before new PF source(새 PF 원천)?
4. Forbidden claims check(금지 주장 확인): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성).
"""


def write_artifacts(final: Mapping[str, Any]) -> None:
    write_json(RUN_ROOT / "stage_closeout_decision.json", final)
    f03b.write_text_sig(REVIEWS_ROOT / "stage_closeout_report.md", stage_closeout_report(final))
    f03b.write_text_sig(REVIEWS_ROOT / "runD_report.md", run_d_report(final))
    f03b.write_text_sig(REVIEWS_ROOT / "grok_stage_closeout_receipt.md", grok_receipt_text(final))
    f03b.write_text_sig(REVIEWS_ROOT / "required_gate_coverage_audit.md", gate_audit_text(final))
    f03b.write_text_sig(REVIEWS_ROOT / "review_index.md", review_index_text(final))
    f03b.write_text_sig(SELECTED_ROOT / "selection_status.md", selection_status_text(final))
    write_json(SELECTED_ROOT / "selection_status.json", selection_status_json(final))
    f03b.write_text_sig(f03b.WORKSPACE_STATE, workspace_state_text(final))
    f03b.write_text_sig(f03b.CURRENT_WORKING_STATE, current_working_state_text(final))


def stage_closeout_report(final: Mapping[str, Any]) -> str:
    rows = {str(row.get("split")): dict(row) for row in final.get("runtime_rows", [])}
    exit_rows = {str(row.get("split")): dict(row) for row in final.get("diagnostics", {}).get("exit_shape_delta_rows", [])}
    return f"""# F65 Stage Closeout(F65 단계 마감)

Updated(갱신): `{final['created_at_utc']}`

- closeout_label(마감 라벨): `{final['closeout_label']}`
- judgment(판정): `{final['judgment']}`
- next_stage(다음 단계): `{NEXT_STAGE_ID}`
- next_run(다음 실행): `{NEXT_RUN_ID}`

## Action And Effect(행동과 효과)

Action(행동): F65B proxy-runtime attribution(프록시-런타임 귀속), F65C targeted MT5 runtime probe(표적 MT5 런타임 탐침), Grok closeout review(그록 마감 검토)를 묶어 stage(단계)를 닫았다.

Effect(효과): SL/TP unit semantics(손절/익절 단위 의미)는 reusable clue(재사용 단서)로 보존하고, economics gap(PF/DD 경제성 차이)은 미해결로 남겨 다음 stage(단계)가 새 가설로 시작하게 했다.

## What Caused The Proxy-Runtime Gap(프록시-런타임 차이 발생 지점)

- Signal count gap(신호 수 차이): raw adapter(원 어댑터)에서 runtime veto tape(런타임 차단 테이프)와 entry transition gate(진입 전환 게이트)를 지나며 압축됐다. validation/OOS는 raw `5269/4206`, veto `1196/881`, entry transition block `2973/2483`, actual non-flat `1100/842`로 맞물린다.
- Residual signal diff(잔여 신호 차이): F65C signal_count_diff(신호 수 차이) `-2199/-1892`는 F66에서 open attribution(열린 귀속)으로 남긴다. Effect(효과): F65 closeout(마감)이 exit semantics clue(청산 의미 단서)를 넘어 signal layer closure(신호 층 폐쇄)로 과장되지 않는다.
- Feature/data gap(피처/데이터 차이): feature_ready_diff(피처 준비 차이)가 validation/OOS `0/0`이라 1순위 원인이 아니다.
- Fill/reject gap(체결/거절 차이): F65B 기준 fills(체결) `1098/838`, invalid stops(무효 손절) `2/4`로 작다.
- Exit economics gap(청산 경제성 차이): proxy(프록시)는 price units(가격 단위)로 손절/익절을 계산했고, MT5는 points(포인트)로 해석했다. 이 단위 의미 차이가 exit shape(청산 형태)를 크게 바꿨다.

## Runtime Probe Observation(런타임 탐침 관찰)

| split(분할) | PF(수익 팩터) | DD%(손실폭) | trades/day(일 거래) | signal diff(신호 차이) | density gap(빈도 차이) |
|---|---:|---:|---:|---:|---:|
| validation_is | {rows.get('validation_is', {}).get('profit_factor')} | {rows.get('validation_is', {}).get('max_drawdown_percent')} | {rows.get('validation_is', {}).get('runtime_trades_per_day')} | {rows.get('validation_is', {}).get('signal_count_diff')} | {gap_value(final, 'validation_is', 'density_gap_mt5_minus_proxy_unit_adjusted')} |
| oos | {rows.get('oos', {}).get('profit_factor')} | {rows.get('oos', {}).get('max_drawdown_percent')} | {rows.get('oos', {}).get('runtime_trades_per_day')} | {rows.get('oos', {}).get('signal_count_diff')} | {gap_value(final, 'oos', 'density_gap_mt5_minus_proxy_unit_adjusted')} |

## Exit Shape Evidence(청산 형태 근거)

| split(분할) | F64E stop%(기존 손절률) | F65C stop%(보정 손절률) | F64E maxhold%(기존 최대보유률) | F65C close_max_hold%(보정 최대보유 청산률) |
|---|---:|---:|---:|---:|
| validation_is | {pct(exit_rows.get('validation_is', {}).get('f64e_mt5_stop_rate'))} | {pct(exit_rows.get('validation_is', {}).get('stop_rate_unit_adjusted'))} | {pct(exit_rows.get('validation_is', {}).get('f64e_mt5_maxhold_rate'))} | {pct(exit_rows.get('validation_is', {}).get('close_max_hold_rate_unit_adjusted'))} |
| oos | {pct(exit_rows.get('oos', {}).get('f64e_mt5_stop_rate'))} | {pct(exit_rows.get('oos', {}).get('stop_rate_unit_adjusted'))} | {pct(exit_rows.get('oos', {}).get('f64e_mt5_maxhold_rate'))} | {pct(exit_rows.get('oos', {}).get('close_max_hold_rate_unit_adjusted'))} |

## Closeout Judgment(마감 판정)

F65는 `preserved_clue(보존 단서)`로 마감한다.

unit-semantics clue(단위 의미 단서)는 supported(지원)된다. 이유는 unit-adjusted MT5 runtime probe(단위 보정 MT5 런타임 탐침)가 stop rate(손절률)를 낮추고 maxhold behavior(최대보유 행동)를 크게 늘렸기 때문이다. 하지만 completion candidate(완성 후보)는 아니다. validation PF(검증 수익 팩터)는 `{rows.get('validation_is', {}).get('profit_factor')}`, OOS PF(OOS 수익 팩터)는 `{rows.get('oos', {}).get('profit_factor')}`, DD(손실폭)는 `{rows.get('validation_is', {}).get('max_drawdown_percent')}/{rows.get('oos', {}).get('max_drawdown_percent')}`로 아직 높다.

## Do-Not-Repeat Note(반복 금지 메모)

explicit unit contract(명시 단위 계약) 없이 proxy price-unit exits(프록시 가격 단위 청산)와 MT5 point exits(MT5 포인트 청산)를 비교하지 않는다. Effect(효과): later frontier stages(다음 전선 단계들)가 fake PF gap(가짜 PF 차이)을 signal edge(신호 우위)처럼 읽지 않게 한다.

## Artifact Lineage(산출물 계보)

- source_inputs(원천 입력): F64D direction adapter ONNX(방향 어댑터 온엑스), F64D runtime veto tape(런타임 차단 테이프), F64E MT5 runtime probe(MT5 런타임 탐침), F65B attribution summary(귀속 요약), F65C final decision(최종 결정), Grok closeout review(그록 마감 검토).
- producer(생산자): `frontier65_gap_attribution.py`, `frontier65c_targeted_sltp_runtime_probe.py`, `frontier65d_stage_closeout.py`, MT5 Strategy Tester(MT5 전략 테스터).
- consumer(소비자): F65 closeout reports(마감 보고서), run registry(실행 등록부), alpha ledger(알파 장부), stage ledger(단계 장부), F66 stage-open(다음 단계 개방).
- artifact_paths(산출물 경로): `{F65B_FINAL.as_posix()}`, `{F65C_FINAL.as_posix()}`, `{F65C_RUNTIME_REPORT.as_posix()}`, `{F65C_GAP_REPORT.as_posix()}`, `{(REVIEWS_ROOT / 'stage_closeout_report.md').as_posix()}`.
- artifact_hashes(산출물 해시): F65B `{hash_value(final, 'f65b_final')}`, F65C `{hash_value(final, 'f65c_final')}`, Grok clean output(그록 정리 출력) `{hash_value(final, 'grok_clean')}`, compile log(컴파일 로그) `{final.get('compile_log_hash', '')}`.
- registry_links(장부 연결): `docs/registers/run_registry.csv`, `docs/registers/alpha_run_ledger.csv`, `{(REVIEWS_ROOT / 'stage_run_ledger.csv').as_posix()}`.
- availability(가용성): durable reports tracked(지속 보고서 추적됨); `02_runs` outputs(실행 산출물)는 ignored_with_manifest(목록 기반 추적 제외)이며 command reproduction(명령 재현)으로 연결된다.
- reproduction_commands(재현 명령): `python -m stage_pipelines.stage_frontier_65.frontier65_gap_attribution`, `python -m stage_pipelines.stage_frontier_65.frontier65c_targeted_sltp_runtime_probe --timeout-seconds 900 --wait-timeout-seconds 240`, `python -m stage_pipelines.stage_frontier_65.frontier65d_stage_closeout`.
- lineage_judgment(계보 판정): `connected_with_boundary(경계 있는 연결)`.

## Boundary(경계)

completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 모두 not_claimed(주장 없음)이다.
"""


def run_d_report(final: Mapping[str, Any]) -> str:
    return f"""# F65D Closeout Run Report(F65D 마감 실행 보고서)

- run(실행): `{RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- Grok closeout(그록 마감): `{final['grok_closeout_classification']}`
- next_stage(다음 단계): `{NEXT_STAGE_ID}`

Action(행동): F65 closeout(마감)을 문서, 장부, selection status(선택 상태), workspace state(작업공간 상태)에 반영했다.

Effect(효과): stage(단계)가 preserved clue(보존 단서)로 닫히고, F66은 새 hypothesis lifecycle(가설 생명주기)로 시작할 수 있다.
"""


def grok_receipt_text(final: Mapping[str, Any]) -> str:
    metadata = dict(final.get("grok_metadata", {}))
    clean_hash = sha256_file(GROK_CLEAN_OUTPUT) if path_exists(GROK_CLEAN_OUTPUT) else ""
    return f"""# F65 Grok Stage Closeout Receipt(F65 그록 단계 마감 영수증)

- trigger_reason(트리거 이유): stage closeout(단계 마감) requires Grok second opinion(그록 2차 의견).
- review_size(검토 크기): `small review(소규모 검토)`.
- direction_before_grok(그록 전 방향): close as preserved clue(보존 단서로 마감), no authority(권위 없음), next F66 runtime-unit-aligned exit economics(다음 F66 런타임 단위 정렬 청산 경제성).
- bounded_evidence(제한 근거): F65B attribution(F65B 귀속), F65C MT5 runtime probe(F65C MT5 런타임 탐침), exit shape delta(청산 형태 변화), forbidden claim guard(금지 주장 보호).
- prompt(프롬프트): `{GROK_PROMPT.as_posix()}`
- prompt_sha256(프롬프트 해시): `{metadata.get('prompt_hash')}`
- clean_output(정리 출력): `{GROK_CLEAN_OUTPUT.as_posix()}`
- clean_output_sha256(정리 출력 해시): `{clean_hash}`
- advice_classification(조언 분류): `{final['grok_closeout_classification']}`
- local_verification(로컬 검증): F65C final_decision(최종 결정), MT5 reports(MT5 보고서), exit-shape diagnostics(청산 형태 진단), workspace registers(작업공간 장부)를 읽어 `{final['judgment']}`로 낮춰 반영했다.
- forbidden_claim_check(금지 주장 확인): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성) all not_claimed(모두 주장 없음).
- final_codex_direction(최종 코덱스 방향): F65 closed as preserved clue(보존 단서로 마감), F66 begins new hypothesis(새 가설 시작).
"""


def gate_audit_text(final: Mapping[str, Any]) -> str:
    return f"""# F65 Required Gate Coverage Audit(F65 필수 게이트 커버리지 감사)

- stage_open_grok_review(단계 개방 그록 검토): `accepted(수용)`
- proxy_runtime_gap_attribution(프록시-런타임 차이 귀속): `frontier65B_proxy_runtime_gap_attribution_scout_v1`
- pre_mt5_grok_review(비싼 MT5 전 그록 검토): `accepted_with_local_verification(수용, 로컬 검증 포함)`
- targeted_mt5_runtime_probe(표적 MT5 런타임 탐침): `frontier65C_targeted_sltp_unit_runtime_probe_v1` / `runtime_probe_observation_unit_adjusted_sltp_no_authority(런타임 탐침 관찰, 단위 보정 손절/익절, 권위 없음)`
- proxy_runtime_gap_after_unit_adjustment(단위 보정 후 프록시-런타임 차이): `recorded(기록됨)`
- stage_closeout_grok_review(단계 마감 그록 검토): `{final['grok_closeout_classification']}`
- stage_closeout(단계 마감): `{RUN_ID}` / `{final['closeout_label']}`
- final_claim_guard(최종 주장 보호): forbidden claims(금지 주장) 모두 not_claimed(주장 없음).
- next_stage(다음 단계): `{NEXT_STAGE_ID}` / `{NEXT_RUN_ID}`
"""


def review_index_text(final: Mapping[str, Any]) -> str:
    return f"""# F65 Review Index(F65 검토 색인)

- `runA_report.md`: stage open report(단계 개방 보고서)
- `grok_stage_open_receipt.md`: Grok stage-open receipt(그록 단계 개방 영수증)
- `runB_report.md`: proxy-runtime gap attribution scout(프록시-런타임 차이 귀속 탐색)
- `proxy_runtime_gap_attribution_report.md`: gap attribution report(차이 귀속 보고서)
- `runtime_probe_unit_adjusted_report.md`: F65C MT5 runtime probe report(F65C MT5 런타임 탐침 보고서)
- `proxy_runtime_gap_after_unit_adjustment_report.md`: unit-adjusted gap report(단위 보정 차이 보고서)
- `grok_pre_mt5_unit_probe_receipt.md`: Grok pre-MT5 receipt(비싼 MT5 전 그록 영수증)
- `grok_stage_closeout_receipt.md`: Grok stage-closeout receipt(그록 단계 마감 영수증)
- `stage_closeout_report.md`: stage closeout report(단계 마감 보고서)
- `runD_report.md`: F65D closeout run report(F65D 마감 실행 보고서)
- `required_gate_coverage_audit.md`: required gate coverage audit(필수 게이트 커버리지 감사)
- `stage_run_ledger.csv`: stage-local run ledger(단계 내부 실행 장부)

Current closeout(현재 마감): `{final['judgment']}`
"""


def selection_status_text(final: Mapping[str, Any]) -> str:
    return f"""# F65 Selection Status(F65 선택 상태)

- stage(단계): `{STAGE_ID}`
- current_run(현재 실행): `{RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- closeout_label(마감 라벨): `{final['closeout_label']}`
- preserved_clue(보존 단서): `{final['primary_clue']}`
- stage_closeout_report(단계 마감 보고서): `{(REVIEWS_ROOT / 'stage_closeout_report.md').as_posix()}`
- next_stage(다음 단계): `{NEXT_STAGE_ID}`
- next_run(다음 실행): `{NEXT_RUN_ID}`
- boundary(경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 not_claimed(주장 없음).
"""


def selection_status_json(final: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "stage_id": STAGE_ID,
        "current_run_id": RUN_ID,
        "status": final["status"],
        "judgment": final["judgment"],
        "closeout_label": final["closeout_label"],
        "preserved_clue": final["primary_clue"],
        "stage_closeout_report": (REVIEWS_ROOT / "stage_closeout_report.md").as_posix(),
        "next_stage_id": NEXT_STAGE_ID,
        "next_run_id": NEXT_RUN_ID,
        "claim_boundary": final["claim_boundary"],
    }


def workspace_state_text(final: Mapping[str, Any]) -> str:
    return f"""current_stage_id: {STAGE_ID}
active_stage: {STAGE_ID}
current_run_id: {RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {final['status']}
current_judgment: {final['judgment']}
next_stage_id: {NEXT_STAGE_ID}
next_run_id: {NEXT_RUN_ID}
runtime_probe_status: runtime_probe_observation_no_authority
runtime_authority: not_claimed
operating_promotion: not_claimed
live_readiness: not_claimed
goal_achieve: not_claimed
updated_at_utc: '{final['created_at_utc']}'
notes:
  - "F65 closed(마감): preserved clue(보존 단서) is SL/TP unit semantics gap(손절/익절 단위 의미 차이)."
  - "F65C runtime probe(런타임 탐침): validation PF=0.97 DD=21.83 trades/day=5.4426; OOS PF=1.11 DD=14.66 trades/day=5.8168."
  - "No completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성) claimed(주장 없음)."
"""


def current_working_state_text(final: Mapping[str, Any]) -> str:
    return f"""# Current Working State(현재 작업 상태)

Frontier65(F65, 전선 65단계)는 preserved clue(보존 단서)로 마감됐다.

- stage(단계): `{STAGE_ID}`
- current_run(현재 실행): `{RUN_ID}`
- judgment(판정): `{final['judgment']}`
- preserved_clue(보존 단서): `{final['primary_clue']}`
- next_stage(다음 단계): `{NEXT_STAGE_ID}`
- next_run(다음 실행): `{NEXT_RUN_ID}`

Action(행동): F65B attribution(귀속)과 F65C targeted MT5 runtime probe(표적 MT5 런타임 탐침)를 stage closeout(단계 마감)으로 묶었다.

Effect(효과): proxy-runtime gap(프록시-런타임 차이)의 주요 발생 지점을 SL/TP unit semantics(손절/익절 단위 의미)와 entry transition compression(진입 전환 압축)으로 분리했고, 아직 PF/DD economics(PF/DD 경제성)는 불완전하다고 낮춰 기록했다.

Claim boundary(주장 경계): runtime_probe_observation(런타임 탐침 관찰)과 preserved clue(보존 단서)까지만 말한다. completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 주장하지 않는다.
"""


def update_registers(final: Mapping[str, Any]) -> None:
    f64c.upsert_csv(f03b.RUN_REGISTRY, "run_id", run_registry_row(final))
    f64c.upsert_csv(f03b.ALPHA_LEDGER, "ledger_row_id", ledger_row(final))
    f64c.upsert_csv(STAGE_ROOT / "03_reviews" / "stage_run_ledger.csv", "ledger_row_id", ledger_row(final))
    f64c.append_once(f03b.CHANGELOG, RUN_ID, changelog_entry(final))
    f64c.append_once(f03b.IDEA_REGISTRY, RUN_ID, idea_entry(final))


def run_registry_row(final: Mapping[str, Any]) -> dict[str, Any]:
    oos = row_by_split(final.get("runtime_rows", []), "oos")
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "stage_closeout_preserved_clue(단계 마감, 보존 단서)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": (REVIEWS_ROOT / "stage_closeout_report.md").as_posix(),
        "notes": f"closeout_label={final['closeout_label']};next_stage={NEXT_STAGE_ID};oos_pf={oos.get('profit_factor')};oos_dd={oos.get('max_drawdown_percent')}",
        "family": "result_judgment(결과 판정)",
        "primary_report": (REVIEWS_ROOT / "stage_closeout_report.md").as_posix(),
        "run_number": RUN_NUMBER,
        "date": final["created_at_utc"][:10],
        "decision": final["judgment"],
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "claim_boundary": final["claim_boundary"],
        "report_path": (REVIEWS_ROOT / "stage_closeout_report.md").as_posix(),
        "profit_factor": oos.get("profit_factor", ""),
        "drawdown": oos.get("max_drawdown_percent", ""),
        "trade_count": oos.get("trade_count", ""),
        "view": "stage_closeout(단계 마감)",
        "tier": "not_applicable_closeout(마감 해당 없음)",
        "metric_scope": "runtime_probe_observation_closeout(런타임 탐침 관찰 마감)",
        "external_verification_status": "completed(완료)",
        "result_judgment": final["judgment"],
        "created_at": final["created_at_utc"],
        "created_at_utc": final["created_at_utc"],
        "required_gate_audit": (REVIEWS_ROOT / "required_gate_coverage_audit.md").as_posix(),
        "runtime_authority": "not_claimed(주장 없음)",
        "operating_promotion": "not_claimed(주장 없음)",
        "run_family": "frontier_stage_closeout(전선 단계 마감)",
        "run_type": "stage_closeout(단계 마감)",
        "input_run_id": PARENT_RUN_ID,
        "output_path": (RUN_ROOT / "stage_closeout_decision.json").as_posix(),
        "result_path": (RUN_ROOT / "stage_closeout_decision.json").as_posix(),
        "selected_profit_factor": oos.get("profit_factor", ""),
        "selected_trade_density": oos.get("runtime_trades_per_day", ""),
        "goal_achieve": "not_claimed(주장 없음)",
        "source_authority": "reference_not_inheritance(참조이지 상속 아님)",
        "trade_density": oos.get("runtime_trades_per_day", ""),
        "max_drawdown_percent": oos.get("max_drawdown_percent", ""),
    }


def ledger_row(final: Mapping[str, Any]) -> dict[str, Any]:
    oos = row_by_split(final.get("runtime_rows", []), "oos")
    row = run_registry_row(final)
    row.update(
        {
            "ledger_row_id": f"{RUN_ID}__stage_closeout",
            "subrun_id": f"{RUN_ID}__stage_closeout",
            "record_view": "stage_closeout(단계 마감)",
            "tier_scope": "not_applicable_closeout(마감 해당 없음)",
            "kpi_scope": "stage_closeout_runtime_probe_observation(단계 마감 런타임 탐침 관찰)",
            "scoreboard_lane": "stage_closeout(단계 마감)",
            "primary_kpi": f"oos_pf={oos.get('profit_factor')};oos_density={oos.get('runtime_trades_per_day')};oos_dd={oos.get('max_drawdown_percent')}",
            "guardrail_kpi": "preserved_clue_no_completion_no_authority(보존 단서, 완성/권위 없음)",
        }
    )
    return row


def changelog_entry(final: Mapping[str, Any]) -> str:
    return f"""
## {final['created_at_utc'][:10]} Frontier65 Closeout(F65 마감)

- action(행동): `{RUN_ID}`로 F65 proxy-runtime gap attribution(프록시-런타임 차이 귀속)을 closeout(마감)했다.
- effect(효과): SL/TP unit semantics(손절/익절 단위 의미)를 preserved clue(보존 단서)로 남기고 `{NEXT_STAGE_ID}`를 다음 새 가설 stage(단계)로 열 준비를 했다.
- boundary(경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 주장하지 않는다.
"""


def idea_entry(final: Mapping[str, Any]) -> str:
    return f"""
## {RUN_ID}

- Stage(단계): `{STAGE_ID}`
- Idea(아이디어): proxy-runtime gap(프록시-런타임 차이)은 signal path(신호 경로)와 exit unit semantics(청산 단위 의미)를 분리해야 한다.
- Result(결과): `{final['judgment']}`
- Preserved clue(보존 단서): `{final['primary_clue']}`
- Evidence(근거): `{(REVIEWS_ROOT / 'stage_closeout_report.md').as_posix()}` and `{(REVIEWS_ROOT / 'runtime_probe_unit_adjusted_report.md').as_posix()}`.
- Next(다음): `{NEXT_STAGE_ID}` / `{NEXT_RUN_ID}`
- Boundary(경계): runtime_probe_observation(런타임 탐침 관찰) and preserved clue(보존 단서) only; no authority(권위 없음).
"""


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def read_text(path: Path) -> str:
    return io_path(path).read_text(encoding="utf-8-sig")


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8-sig")


def classify_grok(clean: str) -> str:
    lower = clean.lower()
    if "rejected" in lower:
        return "rejected(거절)"
    if "accepted" in lower and "needs_local_verification" in lower:
        return "accepted_with_local_verification(수용, 로컬 검증 포함)"
    if "accepted" in lower:
        return "accepted(수용)"
    return "needs_local_verification(로컬 검증 필요)"


def row_by_split(rows: Sequence[Mapping[str, Any]], split: str) -> dict[str, Any]:
    for row in rows:
        if str(row.get("split")) == split:
            return dict(row)
    return {}


def gap_value(final: Mapping[str, Any], split: str, key: str) -> Any:
    row = row_by_split(final.get("proxy_runtime_gap_rows", []), split)
    return row.get(key, "")


def artifact_hashes() -> dict[str, str]:
    paths = {
        "f65b_final": F65B_FINAL,
        "f65c_final": F65C_FINAL,
        "grok_clean": GROK_CLEAN_OUTPUT,
        "grok_prompt": GROK_PROMPT,
        "compile_result": COMPILE_RESULT,
    }
    return {key: sha256_file(path) for key, path in paths.items() if path_exists(path)}


def hash_value(final: Mapping[str, Any], key: str) -> str:
    return str(dict(final.get("artifact_hashes", {})).get(key, ""))


def pct(value: Any) -> str:
    try:
        return f"{float(value) * 100.0:.2f}%"
    except (TypeError, ValueError):
        return "n/a"


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


if __name__ == "__main__":
    raise SystemExit(main())
