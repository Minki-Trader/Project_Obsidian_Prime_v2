from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.control_plane.ledger import io_path, path_exists  # noqa: E402
from stage_pipelines.stage56 import context_timed_opportunity_source_branch as ctx  # noqa: E402


RUN_NUMBER = "run50BD"
PARENT_RUN_ID = "run50BD_stage56_context_timed_quality_gated_slot_v1"
PACKET_ID = "stage56_run50BD_context_timed_quality_gated_slot_v1"
EXPLORATION_LABEL = "stage56_BaseEngine__ContextTimedQualityGatedSlot"
REPORT_PATH = ctx.REVIEWS_ROOT / "run50BD_context_timed_quality_gated_slot.md"
RESULTS_CSV_PATH = ctx.REVIEWS_ROOT / "run50BD_summary.csv"
AUDIT_CSV_PATH = ctx.REVIEWS_ROOT / "run50BD_audit.csv"
SOURCE_SUMMARY_CSV_PATH = ctx.REVIEWS_ROOT / "run50BD_source_summary.csv"
PACKET_ROOT = Path("docs/agent_control/packets") / PACKET_ID
AGGREGATE_SUMMARY_PATH = PACKET_ROOT / "aggregate_summary.json"
RUN_ROOT = ctx.STAGE_ROOT / "02_runs" / RUN_NUMBER
COMMON_ROOT = f"Project_Obsidian_Prime_v2/stage56/{RUN_NUMBER}_context_timed_quality_gated_slot"
WORKSPACE_BLOCK_KEY = "stage56_run50bd_context_timed_quality_gated_slot:"


def r(slot: int, side: int, feature: str, op: str, threshold: float, tag: str) -> ctx.SlotRule:
    return ctx.rule(slot, side, feature, op, threshold, tag)


W40_ESOL_HIGHCOV_RULES = (
    r(0, -1, "rsi_14", "<=", 65.39382934570312, "rsi_le65"),
    r(1, 1, "mega8_pos_breadth_1", ">=", 0.75, "breadth_ge75"),
    r(2, -1, "us100_minus_mega8_equal_return_1", ">=", -1.270301618205849e-05, "us_ge50"),
    r(3, 1, "ppo_hist_12_26_9", "<=", 0.015859955921769142, "ppo_le80"),
    r(4, -1, "return_zscore_20", ">=", 0.36213682889938353, "ret_ge67"),
    r(5, 1, "return_zscore_20", "<=", -0.39960879087448115, "ret_le33"),
    r(6, -1, "us100_minus_mega8_equal_return_1", "<=", -0.00016622118855593698, "us_le33"),
    r(7, 1, "us100_minus_mega8_equal_return_1", "<=", -0.00016668859781930221, "us_le33"),
    r(8, -1, "historical_vol_5_over_20", ">=", 0.5494561791419983, "hv_ge20"),
)

W40_ESOL_MIDCOV_RULES = (
    r(0, -1, "rsi_14", "<=", 65.39382934570312, "rsi_le65"),
    r(1, 1, "mega8_pos_breadth_1", ">=", 0.75, "breadth_ge75"),
    r(2, -1, "vix_zscore_20", ">=", -0.8863085132837295, "vix_ge20"),
    r(3, 1, "bb_position_20", "<=", 0.5108709335327148, "bb_le50"),
    r(4, -1, "return_zscore_20", ">=", 0.36213682889938353, "ret_ge67"),
    r(5, 1, "mega8_pos_breadth_1", "<=", 0.125, "breadth_le20"),
    r(6, -1, "us100_minus_mega8_equal_return_1", "<=", -0.00016622118855593698, "us_le33"),
    r(7, 1, "us100_minus_mega8_equal_return_1", "<=", -0.00016668859781930221, "us_le33"),
    r(8, -1, "atr_14_over_atr_50", ">=", 0.9167566299438477, "atr_ge20"),
)

W40_ELOS_HIGHCOV_RULES = (
    r(0, 1, "bb_position_20", ">=", 0.044257327914237976, "bb_ge20"),
    r(1, -1, "us100_minus_mega8_equal_return_1", ">=", 0.00032371724024415026, "us_ge80"),
    r(2, 1, "us100_minus_mega8_equal_return_1", "<=", -1.270301618205849e-05, "us_le50"),
    r(3, -1, "mega8_pos_breadth_1", ">=", 0.5, "breadth_ge50"),
    r(4, 1, "rsi_14", ">=", 39.77784957885742, "rsi_ge20"),
    r(5, -1, "us100_minus_mega8_equal_return_1", ">=", -2.3254584448295645e-05, "us_ge50"),
    r(6, 1, "mega8_pos_breadth_1", "<=", 0.75, "breadth_le75"),
    r(7, -1, "vix_zscore_20", "<=", 0.6118387603759766, "vix_le80"),
    r(8, 1, "historical_vol_5_over_20", "<=", 1.1267473697662354, "hv_le80"),
)

W45_ELOS_HIGHCOV_RULES = (
    r(0, 1, "bb_position_20", ">=", 0.04968422651290895, "bb_ge20"),
    r(1, -1, "rsi_14", ">=", 42.810285301208495, "rsi_ge20"),
    r(2, 1, "atr_14_over_atr_50", "<=", 1.5199575901031495, "atr_le80"),
    r(3, -1, "return_zscore_20", ">=", 0.38025635182857515, "ret_ge67"),
    r(4, 1, "us100_minus_mega8_equal_return_1", ">=", 0.00016672166020725856, "us_ge67"),
    r(5, -1, "return_zscore_20", "<=", 0.02579088695347309, "ret_le50"),
    r(6, 1, "ppo_hist_12_26_9", "<=", 0.010781209794804455, "ppo_le67"),
    r(7, -1, "mega8_pos_breadth_1", ">=", 0.5, "breadth_ge50"),
)

DEFAULT_VARIANTS = (
    ctx.ContextTimedVariant(
        "v21_w40_esol_highcov_lr2_h2c0_no_b",
        "w40_lr2_highcov_even_short_odd_long",
        40,
        W40_ESOL_HIGHCOV_RULES,
        2,
        0,
        False,
        "40-minute alternating side rules selected on train/validation 2-bar proxy with high coverage; Tier B disabled in routed path.",
        "w40_even_short_odd_long_lr2_highcov_no_runtime_cooldown",
    ),
    ctx.ContextTimedVariant(
        "v22_w40_esol_midcov_lr2_h2c0_no_b",
        "w40_lr2_midcov_even_short_odd_long",
        40,
        W40_ESOL_MIDCOV_RULES,
        2,
        0,
        False,
        "40-minute alternating side rules selected on train/validation 2-bar proxy with medium coverage; Tier B disabled in routed path.",
        "w40_even_short_odd_long_lr2_midcov_no_runtime_cooldown",
    ),
    ctx.ContextTimedVariant(
        "v23_w40_elos_highcov_lr2_h2c0_no_b",
        "w40_lr2_highcov_even_long_odd_short",
        40,
        W40_ELOS_HIGHCOV_RULES,
        2,
        0,
        False,
        "40-minute flipped alternating side rules selected on train/validation 2-bar proxy with high coverage; Tier B disabled in routed path.",
        "w40_even_long_odd_short_lr2_highcov_no_runtime_cooldown",
    ),
    ctx.ContextTimedVariant(
        "v24_w45_elos_highcov_lr2_h2c0_no_b",
        "w45_lr2_highcov_even_long_odd_short",
        45,
        W45_ELOS_HIGHCOV_RULES,
        2,
        0,
        False,
        "45-minute flipped alternating side rules selected on train/validation 2-bar proxy with high coverage; Tier B disabled in routed path.",
        "w45_even_long_odd_short_lr2_highcov_no_runtime_cooldown",
    ),
    ctx.ContextTimedVariant(
        "v25_w40_esol_highcov_lr2_h2c0_with_b",
        "w40_lr2_highcov_tier_b_damage_probe",
        40,
        W40_ESOL_HIGHCOV_RULES,
        2,
        0,
        True,
        "Matched v21 high-coverage quality-gated rules with Tier B fallback enabled to audit hidden OOS damage.",
        "w40_even_short_odd_long_lr2_highcov_no_runtime_cooldown_with_b",
    ),
)


def patch_context() -> None:
    ctx.RUN_NUMBER = RUN_NUMBER
    ctx.PARENT_RUN_ID = PARENT_RUN_ID
    ctx.PACKET_ID = PACKET_ID
    ctx.EXPLORATION_LABEL = EXPLORATION_LABEL
    ctx.RUN_ROOT = RUN_ROOT
    ctx.PACKET_ROOT = PACKET_ROOT
    ctx.REPORT_PATH = REPORT_PATH
    ctx.RESULTS_CSV_PATH = RESULTS_CSV_PATH
    ctx.AUDIT_CSV_PATH = AUDIT_CSV_PATH
    ctx.SOURCE_SUMMARY_CSV_PATH = SOURCE_SUMMARY_CSV_PATH
    ctx.AGGREGATE_SUMMARY_PATH = AGGREGATE_SUMMARY_PATH
    ctx.COMMON_ROOT = COMMON_ROOT
    ctx.DEFAULT_VARIANTS = DEFAULT_VARIANTS
    ctx.__file__ = __file__
    ctx.write_report = write_report
    ctx.append_progress = append_progress
    ctx.update_workspace_state = update_workspace_state
    ctx.update_current_truth = update_current_truth


def write_report(rows: Sequence[Mapping[str, Any]], audit_rows: Sequence[Mapping[str, Any]], result: Mapping[str, Any]) -> None:
    best = ctx.best_row(rows) or {}
    lines = [
        "# Stage56 run50BD Context-Timed Quality-Gated Slot(문맥/시간 품질 필터 슬롯)",
        "",
        f"- run_id(실행 ID): `{PARENT_RUN_ID}`",
        f"- packet_id(작업 묶음 ID): `{PACKET_ID}`",
        "- selected_research_baseline(선택 연구 기준선): `none`",
        f"- external_verification_status(외부 검증 상태): `{result.get('external_verification_status')}`",
        f"- claim_boundary(주장 경계): `{ctx.BOUNDARY}`",
        "",
        "Action(행동): run50BC(실행50BC)의 alternating slot(교대 슬롯) 구조 안에 train/validation(학습/검증) 2-bar proxy(2봉 대리 지표) 품질 조건을 넣어 actual MT5 validation/OOS(실제 MT5 검증/표본외)를 실행했다.",
        "Effect(효과): density(밀도)를 기계적으로 늘리는 대신, 실제 routed path(라우팅 경로)에서 품질 필터가 PF/net/cost stress(수익 팩터/순손익/비용 압박)를 살리는지 확인한다.",
        "",
        "## Best Read(최선 판독)",
        "",
        f"- best_variant(최선 변형): `{best.get('variant_id', 'none')}`",
        f"- validation/OOS trades/day(검증/표본외 일 거래 수): `{ctx.fmt(best.get('routed_validation_trades_per_day'))}` / `{ctx.fmt(best.get('routed_oos_trades_per_day'))}`",
        f"- validation/OOS PF(검증/표본외 수익 팩터): `{ctx.fmt(best.get('routed_validation_pf'))}` / `{ctx.fmt(best.get('routed_oos_pf'))}`",
        f"- validation/OOS net(검증/표본외 순손익): `{ctx.fmt(best.get('routed_validation_net'))}` / `{ctx.fmt(best.get('routed_oos_net'))}`",
        f"- failure_reasons(실패 사유): `{best.get('failure_reasons', '')}`",
        "",
        "## Variant Summary(변형 요약)",
        "",
        "| variant | fallback | val day | oos day | val PF | oos PF | val net | oos net | same val/oos | cooldown day val/oos | failures |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in rows:
        lines.append(
            "| {variant} | {fallback} | {vday} | {oday} | {vpf} | {opf} | {vnet} | {onet} | {samev}/{sameo} | {coolv}/{coolo} | {fail} |".format(
                variant=row.get("variant_id", ""),
                fallback=row.get("routed_fallback_enabled", ""),
                vday=ctx.fmt(row.get("routed_validation_trades_per_day")),
                oday=ctx.fmt(row.get("routed_oos_trades_per_day")),
                vpf=ctx.fmt(row.get("routed_validation_pf")),
                opf=ctx.fmt(row.get("routed_oos_pf")),
                vnet=ctx.fmt(row.get("routed_validation_net")),
                onet=ctx.fmt(row.get("routed_oos_net")),
                samev=ctx.fmt(row.get("routed_validation_same_move_reentry_ratio")),
                sameo=ctx.fmt(row.get("routed_oos_same_move_reentry_ratio")),
                coolv=ctx.fmt(row.get("routed_validation_trades_per_day_after_12bar_cooldown")),
                coolo=ctx.fmt(row.get("routed_oos_trades_per_day_after_12bar_cooldown")),
                fail=row.get("failure_reasons", ""),
            )
        )
    lines.extend(
        [
            "",
            "Judgment(판정): `in_progress_no_selected_research_baseline`.",
            "Effect(효과): run50BD(실행50BD)는 progress evidence(진행 근거)이며 Stage56(56단계)는 계속 open(열림)이다.",
        ]
    )
    ctx.write_md(REPORT_PATH, "\n".join(lines))


def append_progress(best: Mapping[str, Any]) -> None:
    existing = io_path(ctx.PROGRESS_LOG_PATH).read_text(encoding="utf-8-sig") if path_exists(ctx.PROGRESS_LOG_PATH) else ""
    entry = f"""

## {ctx.utc_now()} run50BD Context-Timed Quality-Gated Slot(문맥/시간 품질 필터 슬롯)

- action(행동): train/validation(학습/검증) 2-bar proxy(2봉 대리 지표)로 quality-gated alternating slot(품질 필터 교대 슬롯)을 만들고 actual MT5 validation/OOS(실제 MT5 검증/표본외)를 실행했다.
- effect(효과): run50BC(실행50BC)의 density(밀도) 성과가 단순 분할이 아니라 품질 있는 opportunity source(기회 원천)로 변하는지 확인했다.
- best_variant(현재 최선 변형): `{best.get('variant_id', 'none')}`
- validation/OOS trades/day(검증/표본외 일 거래 수): `{ctx.fmt(best.get('routed_validation_trades_per_day'))}` / `{ctx.fmt(best.get('routed_oos_trades_per_day'))}`
- validation/OOS PF(검증/표본외 수익 팩터): `{ctx.fmt(best.get('routed_validation_pf'))}` / `{ctx.fmt(best.get('routed_oos_pf'))}`
- validation/OOS net(검증/표본외 순손익): `{ctx.fmt(best.get('routed_validation_net'))}` / `{ctx.fmt(best.get('routed_oos_net'))}`
- decision(결정): selected_research_baseline(선택 연구 기준선)=`none`; failure_reasons(실패 사유)=`{best.get('failure_reasons', '')}`.
"""
    ctx.write_md(ctx.PROGRESS_LOG_PATH, existing.rstrip() + entry)


def _remove_workspace_blocks(text: str, block_key: str) -> str:
    lines = text.splitlines(keepends=True)
    output: list[str] = []
    i = 0
    while i < len(lines):
        if lines[i].startswith(block_key):
            i += 1
            while i < len(lines) and (not lines[i].strip() or lines[i].startswith(" ")):
                i += 1
            continue
        output.append(lines[i])
        i += 1
    return "".join(output)


def update_workspace_state(best: Mapping[str, Any]) -> None:
    path = io_path(ctx.WORKSPACE_STATE_PATH)
    text = path.read_text(encoding="utf-8-sig")
    text = re.sub(r"^current_run_id: .*$", f"current_run_id: {PARENT_RUN_ID}", text, count=1, flags=re.MULTILINE)
    text = "\n".join(
        line
        for line in text.splitlines()
        if not (
            line.startswith("- Stage56")
            and "run50BD(" in line
            and ("`0.000000` / `0.000000`" in line or "context-timed quality-gated slot" in line)
        )
    ) + "\n"
    focus = (
        f"- Stage56(56단계) `{ctx.STAGE_ID}`: run50BD(실행50BD) context-timed quality-gated slot(문맥/시간 품질 필터 슬롯) 완료; "
        f"best_variant(현재 최선 변형)은 `{best.get('variant_id', 'none')}`이고 validation/OOS(검증/표본외) trades/day(일 거래 수) "
        f"`{ctx.fmt(best.get('routed_validation_trades_per_day'))}` / `{ctx.fmt(best.get('routed_oos_trades_per_day'))}`, "
        f"PF(수익 팩터) `{ctx.fmt(best.get('routed_validation_pf'))}` / `{ctx.fmt(best.get('routed_oos_pf'))}`, "
        f"net(순손익) `{ctx.fmt(best.get('routed_validation_net'))}` / `{ctx.fmt(best.get('routed_oos_net'))}`이며 selected_research_baseline(선택 연구 기준선)은 `none`이다. "
        f"Effect(효과): `{best.get('failure_reasons', '')}` 때문에 hard condition(강한 완료 조건)을 통과하지 못해 Stage56(56단계)을 계속 open(열림)으로 둔다."
    )
    text = re.sub(r"current_focus:\n", f"current_focus:\n{focus}\n", text, count=1)
    text = _remove_workspace_blocks(text, WORKSPACE_BLOCK_KEY)
    block = (
        f"\n{WORKSPACE_BLOCK_KEY}\n"
        f"  packet_id: {PACKET_ID}\n"
        f"  current_run_id: {PARENT_RUN_ID}\n"
        f"  best_variant: {best.get('variant_id', 'none')}\n"
        "  selected_research_baseline: none\n"
        f"  failure_reasons: {best.get('failure_reasons', '')}\n"
        "  boundary: research_baseline_selection_only_no_operating_claim\n"
        "  next_action: compare_quality_gated_slots_or_open_new_model_branch\n"
    )
    path.write_text(text.rstrip() + "\n" + block, encoding="utf-8-sig")


def update_current_truth(rows: Sequence[Mapping[str, Any]]) -> None:
    best = ctx.best_row(rows) or {}
    best_id = best.get("variant_id", "none")
    failures = best.get("failure_reasons", "")
    val_day = ctx.fmt(best.get("routed_validation_trades_per_day"))
    oos_day = ctx.fmt(best.get("routed_oos_trades_per_day"))
    val_pf = ctx.fmt(best.get("routed_validation_pf"))
    oos_pf = ctx.fmt(best.get("routed_oos_pf"))
    val_net = ctx.fmt(best.get("routed_validation_net"))
    oos_net = ctx.fmt(best.get("routed_oos_net"))
    ctx.write_md(
        ctx.CURRENT_WORKING_STATE_PATH,
        f"""# Current Working State(현재 작업 상태)

- current_packet(현재 작업 묶음): `{PACKET_ID}`
- current run(현재 실행): `{PARENT_RUN_ID}`
- active stage(활성 단계): `{ctx.STAGE_ID}`
- selected_research_baseline(선택 연구 기준선): `none`
- status(상태): active_in_progress(활성 진행 중)
- terminal_condition(종료 조건): useful BaselineAdapter(유용한 기준선 어댑터) hard condition(강한 완료 조건) not_satisfied(미충족)

Stage56(56단계)는 unfinished optimization campaign(미완성 최적화 캠페인)으로 계속 열린다. Effect(효과): run50BD(실행50BD)는 quality-gated alternating slot(품질 필터 교대 슬롯)이 density(밀도)와 OOS quality(표본외 품질)를 동시에 살릴 수 있는지 확인한 중간 근거다.

## Latest Evidence(최신 근거)

- latest_batch(최신 묶음): `{PARENT_RUN_ID}`
- best_variant(현재 최선 변형): `{best_id}`
- selected_research_baseline(선택 연구 기준선): `none`
- validation/OOS trades/day(검증/표본외 일 거래 수): `{val_day}` / `{oos_day}`
- validation/OOS PF(검증/표본외 수익 팩터): `{val_pf}` / `{oos_pf}`
- validation/OOS net(검증/표본외 순손익): `{val_net}` / `{oos_net}`

## Current Bottleneck(현재 병목)

- run50BD judgment(실행50BD 판정): selected_research_baseline(선택 연구 기준선)은 `none`이다. Effect(효과): failure_reasons(실패 사유) `{failures}` 때문에 hard condition(강한 완료 조건)을 통과하지 못했다.
- next_hypothesis_branch(다음 가설 분기): `compare_quality_gated_slots_or_open_new_model_branch`

Forbidden claims(금지 주장): live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(운영 기준선), reviewed_closed(검토 종료).
""",
    )
    ctx.write_md(
        ctx.SELECTION_STATUS_PATH,
        f"""# Stage56 Selection Status(56단계 선택 상태)

- stage_status(단계 상태): `active_in_progress`
- latest_run_id(최신 실행 ID): `{PARENT_RUN_ID}`
- current run(현재 실행): `{PARENT_RUN_ID}`
- current_judgment(현재 판정): `in_progress_no_selected_research_baseline`
- selected_research_baseline(선택 연구 기준선): `none`
- latest_batch_best_variant_intermediate(최신 묶음 최선 변형 중간 근거): `{best_id}`

## Latest Run50BD Intermediate Evidence(최신 50BD 중간 근거)

- packet(작업 묶음): `{PACKET_ID}`
- report(보고서): `{REPORT_PATH.as_posix()}`
- summary_csv(요약 CSV): `{RESULTS_CSV_PATH.as_posix()}`
- audit_csv(감사 CSV): `{AUDIT_CSV_PATH.as_posix()}`
- aggregate_summary(합산 요약): `{AGGREGATE_SUMMARY_PATH.as_posix()}`

Best read(최선 판독) `{best_id}` validation/OOS(검증/표본외) trades/day(일 거래 수) `{val_day}` / `{oos_day}`, PF(수익 팩터) `{val_pf}` / `{oos_pf}`, net(순손익) `{val_net}` / `{oos_net}`이다.

Failure(실패): `{failures}`. Effect(효과): selected_research_baseline(선택 연구 기준선)을 만들지 않고 Stage56(56단계)을 계속 open(열림)으로 둔다.
""",
    )
    append_progress(best)
    update_workspace_state(best)


def main(argv: list[str] | None = None) -> int:
    patch_context()
    return ctx.main(argv)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
