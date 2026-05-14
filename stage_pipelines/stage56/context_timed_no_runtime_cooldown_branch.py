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


RUN_NUMBER = "run50BB"
PARENT_RUN_ID = "run50BB_stage56_context_timed_no_runtime_cooldown_v1"
PACKET_ID = "stage56_run50BB_context_timed_no_runtime_cooldown_v1"
EXPLORATION_LABEL = "stage56_BaseEngine__ContextTimedNoRuntimeCooldown"
REPORT_PATH = ctx.REVIEWS_ROOT / "run50BB_context_timed_no_runtime_cooldown.md"
RESULTS_CSV_PATH = ctx.REVIEWS_ROOT / "run50BB_summary.csv"
AUDIT_CSV_PATH = ctx.REVIEWS_ROOT / "run50BB_audit.csv"
SOURCE_SUMMARY_CSV_PATH = ctx.REVIEWS_ROOT / "run50BB_source_summary.csv"
PACKET_ROOT = Path("docs/agent_control/packets") / PACKET_ID
AGGREGATE_SUMMARY_PATH = PACKET_ROOT / "aggregate_summary.json"
RUN_ROOT = ctx.STAGE_ROOT / "02_runs" / RUN_NUMBER
COMMON_ROOT = f"Project_Obsidian_Prime_v2/stage56/{RUN_NUMBER}_context_timed_no_runtime_cooldown"


def _variant(base: ctx.ContextTimedVariant, variant_id: str, group: str, fallback: bool, notes: str) -> ctx.ContextTimedVariant:
    return ctx.ContextTimedVariant(
        variant_id=variant_id,
        group=group,
        slot_width_minutes=base.slot_width_minutes,
        rules=base.rules,
        max_hold_bars=base.max_hold_bars,
        reentry_cooldown_bars=0,
        routed_fallback_enabled=fallback,
        notes=notes,
        composite_mode=base.composite_mode + "_no_runtime_cooldown",
    )


BASE = {variant.variant_id: variant for variant in ctx.DEFAULT_VARIANTS}
DEFAULT_VARIANTS = (
    _variant(
        BASE["v11_slot30_dense_control_h2c12_with_b"],
        "v13_slot30_dense_control_h2c0_with_b",
        "slot30_dense_no_runtime_cooldown_tier_b_probe",
        True,
        "Same dense context source as run50BA v11 but runtime re-entry cooldown disabled; audit still records same-move cooldown survival.",
    ),
    _variant(
        BASE["v12_slot30_early_mid_bias_h2c12_no_b"],
        "v14_slot30_early_mid_bias_h2c0_no_b",
        "slot30_early_mid_no_runtime_cooldown",
        False,
        "Early/mid/late bias source without runtime cooldown to test density recovery while Tier B remains disabled.",
    ),
    _variant(
        BASE["v10_slot30_cycle_quality_h2c12_no_b"],
        "v15_slot30_cycle_quality_h2c0_no_b",
        "slot30_quality_no_runtime_cooldown",
        False,
        "Quality stricter context cycle without runtime cooldown to test cost-stressed expectancy under higher route count.",
    ),
    _variant(
        BASE["v09_slot30_cycle_dense_h2c12_no_b"],
        "v16_slot30_cycle_dense_h2c0_no_b",
        "slot30_cycle_dense_no_runtime_cooldown",
        False,
        "Side-spaced dense cycle without runtime cooldown to test whether audit cooldown still preserves enough OOS density.",
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
        "# Stage56 run50BB Context-Timed No Runtime Cooldown(문맥/시간 런타임 쿨다운 없음)",
        "",
        f"- run_id(실행 ID): `{PARENT_RUN_ID}`",
        f"- packet_id(묶음 ID): `{PACKET_ID}`",
        "- selected_research_baseline(선택 연구 기준선): `none`",
        f"- external_verification_status(외부 검증 상태): `{result.get('external_verification_status')}`",
        f"- claim_boundary(주장 경계): `{ctx.BOUNDARY}`",
        "",
        "Action(행동): run50BA(실행50BA)의 same context/time source(같은 문맥/시간 원천)에서 runtime re-entry cooldown(런타임 재진입 쿨다운)을 0으로 낮추고 actual MT5 validation/OOS(실제 MT5 검증/표본외)를 실행했다.",
        "Effect(효과): runtime cooldown(런타임 쿨다운)이 밀도를 죽였는지와 audit cooldown(감사 쿨다운) 뒤에도 real density(실제 밀도)가 살아남는지를 분리한다.",
        "",
        "## Best Read(최선 판독)",
        "",
        f"- best_variant(최선 변형): `{best.get('variant_id', 'none')}`",
        f"- validation/OOS trades/day(검증/표본외 일 거래): `{ctx.fmt(best.get('routed_validation_trades_per_day'))}` / `{ctx.fmt(best.get('routed_oos_trades_per_day'))}`",
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
            "Effect(효과): run50BB(실행50BB)는 progress evidence(진행 근거)이며 Stage56(56단계)는 계속 open(열림)이다.",
        ]
    )
    ctx.write_md(REPORT_PATH, "\n".join(lines))


def append_progress(best: Mapping[str, Any]) -> None:
    existing = io_path(ctx.PROGRESS_LOG_PATH).read_text(encoding="utf-8-sig") if path_exists(ctx.PROGRESS_LOG_PATH) else ""
    entry = f"""

## {ctx.utc_now()} run50BB Context-Timed No Runtime Cooldown(문맥/시간 런타임 쿨다운 없음)

- action(행동): runtime re-entry cooldown(런타임 재진입 쿨다운)을 0으로 낮추고 audit cooldown(감사 쿨다운)을 별도 기록했다.
- effect(효과): actual density(실제 밀도)가 execution setting(실행 설정) 때문에 눌렸는지 확인했다.
- best_variant(현재 최선 변형): `{best.get('variant_id', 'none')}`
- validation/OOS trades/day(검증/표본외 일 거래): `{ctx.fmt(best.get('routed_validation_trades_per_day'))}` / `{ctx.fmt(best.get('routed_oos_trades_per_day'))}`
- validation/OOS PF(검증/표본외 수익 팩터): `{ctx.fmt(best.get('routed_validation_pf'))}` / `{ctx.fmt(best.get('routed_oos_pf'))}`
- validation/OOS net(검증/표본외 순손익): `{ctx.fmt(best.get('routed_validation_net'))}` / `{ctx.fmt(best.get('routed_oos_net'))}`
- decision(결정): selected_research_baseline(선택 연구 기준선)=`none`; failure_reasons(실패 사유)=`{best.get('failure_reasons', '')}`.
"""
    ctx.write_md(ctx.PROGRESS_LOG_PATH, existing.rstrip() + entry)


def update_workspace_state(best: Mapping[str, Any]) -> None:
    path = io_path(ctx.WORKSPACE_STATE_PATH)
    text = path.read_text(encoding="utf-8-sig")
    text = re.sub(r"^current_run_id: .*$", f"current_run_id: {PARENT_RUN_ID}", text, count=1, flags=re.MULTILINE)
    focus = (
        f"- Stage56(56단계) `{ctx.STAGE_ID}`: run50BB(실행50BB) context-timed no-runtime-cooldown(문맥/시간 런타임 쿨다운 없음) 완료; "
        f"best_variant(현재 최선 변형)은 `{best.get('variant_id', 'none')}`이고 validation/OOS(검증/표본외) trades/day(일 거래 수) "
        f"`{ctx.fmt(best.get('routed_validation_trades_per_day'))}` / `{ctx.fmt(best.get('routed_oos_trades_per_day'))}`, "
        f"PF(수익 팩터) `{ctx.fmt(best.get('routed_validation_pf'))}` / `{ctx.fmt(best.get('routed_oos_pf'))}`, "
        f"net(순손익) `{ctx.fmt(best.get('routed_validation_net'))}` / `{ctx.fmt(best.get('routed_oos_net'))}`이며 selected_research_baseline(선택 연구 기준선)은 `none`이다. "
        f"Effect(효과): `{best.get('failure_reasons', '')}` 때문에 hard condition(강한 완료 조건)을 통과하지 못해 Stage56(56단계)을 계속 open(열림)으로 둔다."
    )
    text = re.sub(r"current_focus:\n", f"current_focus:\n{focus}\n", text, count=1)
    block = (
        "\nstage56_run50bb_context_timed_no_runtime_cooldown:\n"
        f"  packet_id: {PACKET_ID}\n"
        f"  current_run_id: {PARENT_RUN_ID}\n"
        f"  best_variant: {best.get('variant_id', 'none')}\n"
        "  selected_research_baseline: none\n"
        f"  failure_reasons: {best.get('failure_reasons', '')}\n"
        "  boundary: research_baseline_selection_only_no_operating_claim\n"
        "  next_action: density_recovered_audit_or_new_model_branch\n"
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

Stage56(56단계)는 unfinished optimization campaign(미완성 최적화 캠페인)으로 계속 열린다. Effect(효과): run50BB(실행50BB)는 runtime cooldown(런타임 쿨다운)을 제거했을 때 context-timed source(문맥/시간 원천)의 real density(실제 밀도)가 살아나는지 확인한 중간 근거다.

## Latest Evidence(최신 근거)

- latest_batch(최신 묶음): `{PARENT_RUN_ID}`
- best_variant(현재 최선 변형): `{best_id}`
- selected_research_baseline(선택 연구 기준선): `none`
- validation/OOS trades/day(검증/표본외 일 거래): `{val_day}` / `{oos_day}`
- validation/OOS PF(검증/표본외 수익 팩터): `{val_pf}` / `{oos_pf}`
- validation/OOS net(검증/표본외 순손익): `{val_net}` / `{oos_net}`

## Current Bottleneck(현재 병목)

- run50BB judgment(실행50BB 판정): selected_research_baseline(선택 연구 기준선)은 `none`이다. Effect(효과): failure_reasons(실패 사유) `{failures}` 때문에 hard condition(강한 완료 조건)을 통과하지 못했다.
- next_hypothesis_branch(다음 가설 분기): `density_recovered_audit_or_new_model_branch`

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

## Latest Run50BB Intermediate Evidence(최신 50BB 중간 근거)

- packet(묶음): `{PACKET_ID}`
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
