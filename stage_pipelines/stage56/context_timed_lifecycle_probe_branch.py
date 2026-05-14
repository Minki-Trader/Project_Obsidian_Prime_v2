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
from stage_pipelines.stage56 import context_timed_quality_gated_slot_branch as bd  # noqa: E402


RUN_NUMBER = "run50BF"
PARENT_RUN_ID = "run50BF_stage56_context_timed_lifecycle_probe_v1"
PACKET_ID = "stage56_run50BF_context_timed_lifecycle_probe_v1"
EXPLORATION_LABEL = "stage56_BaseEngine__ContextTimedLifecycleProbe"
REPORT_PATH = ctx.REVIEWS_ROOT / "run50BF_context_timed_lifecycle_probe.md"
RESULTS_CSV_PATH = ctx.REVIEWS_ROOT / "run50BF_summary.csv"
AUDIT_CSV_PATH = ctx.REVIEWS_ROOT / "run50BF_audit.csv"
SOURCE_SUMMARY_CSV_PATH = ctx.REVIEWS_ROOT / "run50BF_source_summary.csv"
PACKET_ROOT = Path("docs/agent_control/packets") / PACKET_ID
AGGREGATE_SUMMARY_PATH = PACKET_ROOT / "aggregate_summary.json"
RUN_ROOT = ctx.STAGE_ROOT / "02_runs" / RUN_NUMBER
COMMON_ROOT = f"Project_Obsidian_Prime_v2/stage56/{RUN_NUMBER}_context_timed_lifecycle_probe"
WORKSPACE_BLOCK_KEY = "stage56_run50bf_context_timed_lifecycle_probe:"


DEFAULT_RULES = bd.W40_ESOL_MIDCOV_RULES

DEFAULT_VARIANTS = (
    ctx.ContextTimedVariant(
        "v31_v22_midcov_h1c0_with_b",
        "v22_lifecycle_short_hold_tier_b_probe",
        40,
        DEFAULT_RULES,
        1,
        0,
        True,
        "Run50BE v30 source with max hold 1 and Tier B fallback enabled; tests whether faster lifecycle reduces same-move/cost damage.",
        "v22_midcov_h1_c0_with_b",
    ),
    ctx.ContextTimedVariant(
        "v32_v22_midcov_h3c0_with_b",
        "v22_lifecycle_hold3_tier_b_probe",
        40,
        DEFAULT_RULES,
        3,
        0,
        True,
        "Run50BE v30 source with max hold 3 and Tier B fallback enabled; tests whether more MFE capture repairs expectancy without losing density.",
        "v22_midcov_h3_c0_with_b",
    ),
    ctx.ContextTimedVariant(
        "v33_v22_midcov_h4c0_with_b",
        "v22_lifecycle_hold4_tier_b_probe",
        40,
        DEFAULT_RULES,
        4,
        0,
        True,
        "Run50BE v30 source with max hold 4 and Tier B fallback enabled; broader hold stress for PF and cost expectancy.",
        "v22_midcov_h4_c0_with_b",
    ),
    ctx.ContextTimedVariant(
        "v34_v22_midcov_h3c2_with_b",
        "v22_lifecycle_hold3_cooldown2_tier_b_probe",
        40,
        DEFAULT_RULES,
        3,
        2,
        True,
        "Run50BE v30 source with max hold 3 and two-bar re-entry cooldown; tests real density survival after same-move reduction.",
        "v22_midcov_h3_c2_with_b",
    ),
    ctx.ContextTimedVariant(
        "v35_v22_midcov_h3c0_no_b",
        "v22_lifecycle_hold3_tier_b_disabled",
        40,
        DEFAULT_RULES,
        3,
        0,
        False,
        "Matched hold-3 source with Tier B disabled in routed path; isolates whether Tier B fallback is still hidden OOS damage.",
        "v22_midcov_h3_c0_no_b",
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
        "# Stage56 run50BF Context-Timed Lifecycle Probe(생명주기 탐침)",
        "",
        f"- run_id(실행 ID): `{PARENT_RUN_ID}`",
        f"- packet_id(작업 묶음 ID): `{PACKET_ID}`",
        "- selected_research_baseline(선택 연구 기준선): `none`",
        f"- external_verification_status(외부 검증 상태): `{result.get('external_verification_status')}`",
        f"- claim_boundary(주장 경계): `{ctx.BOUNDARY}`",
        "",
        "Action(행동): run50BE(실행50BE) v30의 source/routing(원천/라우팅)을 유지하고 max hold/re-entry cooldown(최대 보유/재진입 쿨다운)만 바꿔 actual MT5 validation/OOS(실제 MT5 검증/표본외)를 실행했다.",
        "Effect(효과): density(밀도)를 더 붙이는 대신 lifecycle(생명주기)이 PF/net/cost stress/same-move(수익 팩터/순손익/비용 압박/동일 이동)를 고칠 수 있는지 분리해 본다.",
        "",
        "## Best Read(최선 판독)",
        "",
        f"- best_variant(최선 변형): `{best.get('variant_id', 'none')}`",
        f"- validation/OOS trades/day(검증/표본외 일 거래 수): `{ctx.fmt(best.get('routed_validation_trades_per_day'))}` / `{ctx.fmt(best.get('routed_oos_trades_per_day'))}`",
        f"- validation/OOS PF(검증/표본외 수익 팩터): `{ctx.fmt(best.get('routed_validation_pf'))}` / `{ctx.fmt(best.get('routed_oos_pf'))}`",
        f"- validation/OOS net(검증/표본외 순손익): `{ctx.fmt(best.get('routed_validation_net'))}` / `{ctx.fmt(best.get('routed_oos_net'))}`",
        f"- failure_reasons(실패 사유): `{best.get('failure_reasons', '')}`",
        "",
        "| variant | fallback | hold | cooldown | val day | oos day | val PF | oos PF | val net | oos net | same val/oos | cooldown day val/oos | failures |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in rows:
        lines.append(
            "| {variant} | {fallback} | {hold} | {cooldown} | {vday} | {oday} | {vpf} | {opf} | {vnet} | {onet} | {samev}/{sameo} | {coolv}/{coolo} | {fail} |".format(
                variant=row.get("variant_id", ""),
                fallback=row.get("routed_fallback_enabled", ""),
                hold=row.get("max_hold_bars", ""),
                cooldown=row.get("reentry_cooldown_bars", ""),
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
    lines.extend(["", "Judgment(판정): `in_progress_no_selected_research_baseline`."])
    ctx.write_md(REPORT_PATH, "\n".join(lines))


def append_progress(best: Mapping[str, Any]) -> None:
    existing = io_path(ctx.PROGRESS_LOG_PATH).read_text(encoding="utf-8-sig") if path_exists(ctx.PROGRESS_LOG_PATH) else ""
    entry = f"""

## {ctx.utc_now()} run50BF Context-Timed Lifecycle Probe(생명주기 탐침)

- action(행동): run50BE(실행50BE) v30의 source/routing(원천/라우팅)을 유지하고 max hold/re-entry cooldown(최대 보유/재진입 쿨다운)을 바꿔 actual MT5 validation/OOS(실제 MT5 검증/표본외)를 실행했다.
- effect(효과): same-move/cost stress(동일 이동/비용 압박)가 lifecycle(생명주기) 문제인지 확인했다.
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
        if not (line.startswith("- Stage56") and "run50BF(" in line)
    ) + "\n"
    focus = (
        f"- Stage56(56단계) `{ctx.STAGE_ID}`: run50BF(실행50BF) context-timed lifecycle probe(문맥/시간 생명주기 탐침) 완료; "
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
        "  next_action: decide_lifecycle_repair_or_open_new_model_branch\n"
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

Stage56(56단계)는 unfinished optimization campaign(미완성 최적화 캠페인)으로 계속 열린다. Effect(효과): run50BF(실행50BF)는 run50BE(실행50BE) v30의 lifecycle(생명주기)이 OOS PF/cost/same-move(표본외 수익 팩터/비용/동일 이동)를 고칠 수 있는지 확인한 중간 근거다.

## Latest Evidence(최신 근거)

- latest_batch(최신 묶음): `{PARENT_RUN_ID}`
- best_variant(현재 최선 변형): `{best_id}`
- selected_research_baseline(선택 연구 기준선): `none`
- validation/OOS trades/day(검증/표본외 일 거래 수): `{val_day}` / `{oos_day}`
- validation/OOS PF(검증/표본외 수익 팩터): `{val_pf}` / `{oos_pf}`
- validation/OOS net(검증/표본외 순손익): `{val_net}` / `{oos_net}`

## Current Bottleneck(현재 병목)

- run50BF judgment(실행50BF 판정): selected_research_baseline(선택 연구 기준선)은 `none`이다. Effect(효과): failure_reasons(실패 사유) `{failures}` 때문에 hard condition(강한 완료 조건)을 통과하지 못했다.
- next_hypothesis_branch(다음 가설 분기): `decide_lifecycle_repair_or_open_new_model_branch`

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

## Latest Run50BF Intermediate Evidence(최신 50BF 중간 근거)

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
