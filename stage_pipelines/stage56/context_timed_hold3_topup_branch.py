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
from stage_pipelines.stage56 import context_timed_v22_density_topup_branch as be  # noqa: E402


RUN_NUMBER = "run50BG"
PARENT_RUN_ID = "run50BG_stage56_context_timed_hold3_topup_v1"
PACKET_ID = "stage56_run50BG_context_timed_hold3_topup_v1"
EXPLORATION_LABEL = "stage56_BaseEngine__ContextTimedHold3Topup"
REPORT_PATH = ctx.REVIEWS_ROOT / "run50BG_context_timed_hold3_topup.md"
RESULTS_CSV_PATH = ctx.REVIEWS_ROOT / "run50BG_summary.csv"
AUDIT_CSV_PATH = ctx.REVIEWS_ROOT / "run50BG_audit.csv"
SOURCE_SUMMARY_CSV_PATH = ctx.REVIEWS_ROOT / "run50BG_source_summary.csv"
PACKET_ROOT = Path("docs/agent_control/packets") / PACKET_ID
AGGREGATE_SUMMARY_PATH = PACKET_ROOT / "aggregate_summary.json"
RUN_ROOT = ctx.STAGE_ROOT / "02_runs" / RUN_NUMBER
COMMON_ROOT = f"Project_Obsidian_Prime_v2/stage56/{RUN_NUMBER}_context_timed_hold3_topup"
WORKSPACE_BLOCK_KEY = "stage56_run50bg_context_timed_hold3_topup:"


DEFAULT_VARIANTS = (
    ctx.ContextTimedVariant(
        "v36_v22_midcov_h3c0_no_b_control",
        "hold3_midcov_control",
        40,
        bd.W40_ESOL_MIDCOV_RULES,
        3,
        0,
        False,
        "Run50BF v35 control replay: hold3 with Tier B disabled.",
        "v22_midcov_h3_c0_no_b_control",
    ),
    ctx.ContextTimedVariant(
        "v37_v22_slot8_relax_h3c0_no_b",
        "hold3_slot8_topup",
        40,
        be.V22_SLOT8_TOPUP,
        3,
        0,
        False,
        "Hold3 version of run50BE slot8 top-up; tests whether MFE capture repairs OOS quality without Tier B damage.",
        "v22_slot8_relax_h3_c0_no_b",
    ),
    ctx.ContextTimedVariant(
        "v38_v22_slot3_8_relax_h3c0_no_b",
        "hold3_slot3_8_topup",
        40,
        be.V22_SLOT3_8_TOPUP,
        3,
        0,
        False,
        "Hold3 version of run50BE slots 3+8 top-up; tests quality-preserving density recovery.",
        "v22_slot3_8_relax_h3_c0_no_b",
    ),
    ctx.ContextTimedVariant(
        "v39_v22_slot5_8_relax_h3c0_no_b",
        "hold3_slot5_8_topup",
        40,
        be.V22_SLOT5_8_TOPUP,
        3,
        0,
        False,
        "Hold3 version of run50BE slots 5+8 top-up; tests whether long-side slot repair survives OOS.",
        "v22_slot5_8_relax_h3_c0_no_b",
    ),
    ctx.ContextTimedVariant(
        "v40_v22_slot3_5_8_relax_h3c0_no_b",
        "hold3_slot3_5_8_topup",
        40,
        be.V22_SLOT3_5_8_TOPUP,
        3,
        0,
        False,
        "Hold3 version of run50BE slots 3+5+8 top-up; tests maximum Tier-A-only density recovery before new model branch.",
        "v22_slot3_5_8_relax_h3_c0_no_b",
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
        "# Stage56 run50BG Context-Timed Hold3 Top-Up(문맥/시간 3봉 보유 보강)",
        "",
        f"- run_id(실행 ID): `{PARENT_RUN_ID}`",
        f"- packet_id(작업 묶음 ID): `{PACKET_ID}`",
        "- selected_research_baseline(선택 연구 기준선): `none`",
        f"- external_verification_status(외부 검증 상태): `{result.get('external_verification_status')}`",
        f"- claim_boundary(주장 경계): `{ctx.BOUNDARY}`",
        "",
        "Action(행동): run50BF(실행50BF) v35의 hold3(3봉 보유) 품질 단서에 run50BE(실행50BE) slot top-up(슬롯 보강)을 붙여 actual MT5 validation/OOS(실제 MT5 검증/표본외)를 실행했다.",
        "Effect(효과): raw Tier B fallback(원시 티어B 대체) 없이 OOS density(표본외 밀도)가 5/day(일 5회)를 넘고 PF/net/cost stress(수익 팩터/순손익/비용 압박)가 살아남는지 확인한다.",
        "",
        "## Best Read(최선 판독)",
        "",
        f"- best_variant(현재 최선 변형): `{best.get('variant_id', 'none')}`",
        f"- validation/OOS trades/day(검증/표본외 일 거래 수): `{ctx.fmt(best.get('routed_validation_trades_per_day'))}` / `{ctx.fmt(best.get('routed_oos_trades_per_day'))}`",
        f"- validation/OOS PF(검증/표본외 수익 팩터): `{ctx.fmt(best.get('routed_validation_pf'))}` / `{ctx.fmt(best.get('routed_oos_pf'))}`",
        f"- validation/OOS net(검증/표본외 순손익): `{ctx.fmt(best.get('routed_validation_net'))}` / `{ctx.fmt(best.get('routed_oos_net'))}`",
        f"- failure_reasons(실패 사유): `{best.get('failure_reasons', '')}`",
        "",
        "| variant | fallback | hold | val day | oos day | val PF | oos PF | val net | oos net | same val/oos | cooldown day val/oos | failures |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in rows:
        lines.append(
            "| {variant} | {fallback} | {hold} | {vday} | {oday} | {vpf} | {opf} | {vnet} | {onet} | {samev}/{sameo} | {coolv}/{coolo} | {fail} |".format(
                variant=row.get("variant_id", ""),
                fallback=row.get("routed_fallback_enabled", ""),
                hold=row.get("max_hold_bars", ""),
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

## {ctx.utc_now()} run50BG Context-Timed Hold3 Top-Up(문맥/시간 3봉 보유 보강)

- action(행동): hold3(3봉 보유) control(대조군)과 slot top-up(슬롯 보강)을 actual MT5 validation/OOS(실제 MT5 검증/표본외)에서 비교했다.
- effect(효과): Tier B(티어B)를 끈 상태에서 실제 밀도(real density, 실제 밀도)와 품질(quality, 품질)이 동시에 회복되는지 확인했다.
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
    text = "\n".join(line for line in text.splitlines() if not (line.startswith("- Stage56") and "run50BG(" in line)) + "\n"
    focus = (
        f"- Stage56(56단계) `{ctx.STAGE_ID}`: run50BG(실행50BG) context-timed hold3 top-up(문맥/시간 3봉 보유 보강) 완료; "
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
        "  next_action: decide_hold3_topup_or_open_new_model_branch\n"
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

Stage56(56단계)는 unfinished optimization campaign(미완성 최적화 캠페인)으로 계속 열린다. Effect(효과): run50BG(실행50BG)는 hold3(3봉 보유)와 slot top-up(슬롯 보강)이 Tier B(티어B) 없이 OOS density/PF/cost(표본외 밀도/수익 팩터/비용)를 동시에 살리는지 확인한 중간 근거다.

## Latest Evidence(최신 근거)

- latest_batch(최신 묶음): `{PARENT_RUN_ID}`
- best_variant(현재 최선 변형): `{best_id}`
- selected_research_baseline(선택 연구 기준선): `none`
- validation/OOS trades/day(검증/표본외 일 거래 수): `{val_day}` / `{oos_day}`
- validation/OOS PF(검증/표본외 수익 팩터): `{val_pf}` / `{oos_pf}`
- validation/OOS net(검증/표본외 순손익): `{val_net}` / `{oos_net}`

## Current Bottleneck(현재 병목)

- run50BG judgment(실행50BG 판정): selected_research_baseline(선택 연구 기준선)은 `none`이다. Effect(효과): failure_reasons(실패 사유) `{failures}` 때문에 hard condition(강한 완료 조건)을 통과하지 못했다.
- next_hypothesis_branch(다음 가설 분기): `decide_hold3_topup_or_open_new_model_branch`

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

## Latest Run50BG Intermediate Evidence(최신 50BG 중간 근거)

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
