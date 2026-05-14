from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists, sha256_file_lf_normalized  # noqa: E402
from stage_pipelines.stage56 import context_extratrees_agreement_branch as bn  # noqa: E402
from stage_pipelines.stage56 import context_extratrees_firewall_transition_branch as bq  # noqa: E402
from stage_pipelines.stage56 import context_timed_opportunity_source_branch as ctx  # noqa: E402
from stage_pipelines.stage56 import context_timed_v22_density_topup_branch as be  # noqa: E402


RUN_NUMBER = "run50BR"
PARENT_RUN_ID = "run50BR_stage56_context_extratrees_context_gap_refill_v1"
PACKET_ID = "stage56_run50BR_context_extratrees_context_gap_refill_v1"
EXPLORATION_LABEL = "stage56_BaseEngine__ContextExtraTreesContextGapRefill"
REPORT_PATH = ctx.REVIEWS_ROOT / "run50BR_context_extratrees_context_gap_refill.md"
RESULTS_CSV_PATH = ctx.REVIEWS_ROOT / "run50BR_summary.csv"
AUDIT_CSV_PATH = ctx.REVIEWS_ROOT / "run50BR_audit.csv"
SOURCE_SUMMARY_CSV_PATH = ctx.REVIEWS_ROOT / "run50BR_source_summary.csv"
PACKET_ROOT = Path("docs/agent_control/packets") / PACKET_ID
AGGREGATE_SUMMARY_PATH = PACKET_ROOT / "aggregate_summary.json"
RUN_ROOT = ctx.STAGE_ROOT / "02_runs" / RUN_NUMBER
COMMON_ROOT = f"Project_Obsidian_Prime_v2/stage56/{RUN_NUMBER}_context_extratrees_context_gap_refill"
SIGNAL_COLUMN = "stage56_context_gap_refill_signal"
WORKSPACE_BLOCK_KEY = "stage56_run50br_context_extratrees_context_gap_refill:"

BAD_CONTEXT_RULES = {"s8_short_hv_ge20", "s5_long_ret_le33"}


DEFAULT_VARIANTS = (
    ctx.ContextTimedVariant(
        "v64_v47_ctxgap14_refill_etfw_h2_no_b",
        "context_gap14_refill_et_firewall",
        40,
        be.V22_SLOT3_5_8_TOPUP,
        2,
        0,
        False,
        "Context primary same-direction source gap 14 bars, ET slot refill, and stable ET damage firewall.",
        "context_plus_et40_slot_fill",
    ),
    ctx.ContextTimedVariant(
        "v65_v47_ctxgap24_refill_etfw_h2_no_b",
        "context_gap24_refill_et_firewall",
        40,
        be.V22_SLOT3_5_8_TOPUP,
        2,
        0,
        False,
        "Context primary same-direction source gap 24 bars, ET slot refill, and stable ET damage firewall.",
        "context_plus_et40_slot_fill",
    ),
    ctx.ContextTimedVariant(
        "v66_v47_badctxgap24_refill_etfw_h2_no_b",
        "bad_context_gap24_refill_et_firewall",
        40,
        be.V22_SLOT3_5_8_TOPUP,
        2,
        0,
        False,
        "Only unstable context rules s8/s5 receive same-direction source gap 24 bars; ET refill remains allowed.",
        "context_plus_et40_slot_fill",
    ),
    ctx.ContextTimedVariant(
        "v67_v47_ctxgap24_refill_etfw_h4_no_b",
        "context_gap24_refill_et_firewall_hold4",
        40,
        be.V22_SLOT3_5_8_TOPUP,
        4,
        0,
        False,
        "Context primary same-direction source gap 24 bars, ET slot refill, stable ET damage firewall, and hold4.",
        "context_plus_et40_slot_fill",
    ),
)


def _context_gap_bars(variant: ctx.ContextTimedVariant) -> int:
    if "ctxgap14" in variant.variant_id:
        return 14
    if "ctxgap24" in variant.variant_id or "badctxgap24" in variant.variant_id:
        return 24
    if "ctxgap12" in variant.variant_id or "badctxgap12" in variant.variant_id:
        return 12
    return 0


def _bad_context_only(variant: ctx.ContextTimedVariant) -> bool:
    return "badctxgap" in variant.variant_id


def _slot_index(frame: pd.DataFrame, slot_width_minutes: int) -> pd.Series:
    minutes = pd.to_numeric(frame["minutes_from_cash_open"], errors="coerce")
    return np.floor(minutes / float(slot_width_minutes))


def _suppress_context_reentries(
    frame: pd.DataFrame,
    context_signal: pd.Series,
    variant: ctx.ContextTimedVariant,
) -> tuple[pd.Series, pd.Series]:
    gap_bars = _context_gap_bars(variant)
    if gap_bars <= 0:
        return context_signal.astype("int8"), pd.Series(False, index=frame.index)

    timestamp = pd.to_datetime(frame["timestamp"], utc=True)
    split = frame["split"].astype(str)
    tier = frame["tier_label"].astype(str)
    rules = frame["context_rule_id"].astype(str)
    blocked = pd.Series(False, index=frame.index)
    accepted = context_signal.copy().astype("int8")
    last_accept: dict[tuple[str, str, int], pd.Timestamp] = {}

    order = timestamp.sort_values().index
    for idx in order:
        signal = int(accepted.loc[idx])
        if signal == 0:
            continue
        if _bad_context_only(variant) and rules.loc[idx] not in BAD_CONTEXT_RULES:
            last_accept[(split.loc[idx], tier.loc[idx], signal)] = timestamp.loc[idx]
            continue
        key = (split.loc[idx], tier.loc[idx], signal)
        previous = last_accept.get(key)
        if previous is not None:
            bars_since = (timestamp.loc[idx] - previous).total_seconds() / 60.0 / 5.0
            if 0.0 <= bars_since <= float(gap_bars):
                accepted.loc[idx] = 0
                blocked.loc[idx] = True
                continue
        last_accept[key] = timestamp.loc[idx]
    return accepted.astype("int8"), blocked


def _signal_source_origin(frame: pd.DataFrame, context_signal: pd.Series) -> pd.Series:
    signal = pd.to_numeric(frame[ctx.SIGNAL_COLUMN], errors="coerce").fillna(0).astype("int8")
    et_signal = pd.to_numeric(frame["et40_signal"], errors="coerce").fillna(0).astype("int8")
    return pd.Series(
        np.where(
            context_signal.ne(0) & signal.ne(0),
            "context_primary",
            np.where(signal.ne(0) & et_signal.ne(0), "et_slotfill", "flat"),
        ),
        index=frame.index,
    )


def build_variant_frame(common: pd.DataFrame, variant: ctx.ContextTimedVariant) -> pd.DataFrame:
    frame = bn._ORIGINAL_BUILD_VARIANT_FRAME(common, variant)
    frame["timestamp"] = pd.to_datetime(frame["timestamp"], utc=True)
    raw_context = pd.to_numeric(frame[ctx.SIGNAL_COLUMN], errors="coerce").fillna(0).astype("int8")
    frame["context_signal_raw"] = raw_context
    et_predictions = bn.load_et40_predictions()
    frame = frame.merge(et_predictions, on=["timestamp", "split", "tier_label"], how="left")
    frame["et40_signal"] = pd.to_numeric(frame["et40_signal"], errors="coerce").fillna(0).astype("int8")
    context_after_gap, context_blocked = _suppress_context_reentries(frame, raw_context, variant)
    frame["context_signal_after_gap"] = context_after_gap
    frame["context_gap_blocked"] = context_blocked
    frame["context_gap_policy"] = (
        f"{'bad_context_only_' if _bad_context_only(variant) else ''}gap{_context_gap_bars(variant)}"
    )
    frame["et40_agrees_context"] = raw_context.ne(0) & frame["et40_signal"].eq(raw_context)
    frame["et40_conflicts_context"] = raw_context.ne(0) & frame["et40_signal"].ne(0) & frame["et40_signal"].ne(raw_context)
    frame[ctx.SIGNAL_COLUMN] = bn._slot_fill_signal(
        frame,
        context_after_gap,
        frame["et40_signal"],
        variant.slot_width_minutes,
    )
    signal = pd.to_numeric(frame[ctx.SIGNAL_COLUMN], errors="coerce").fillna(0).astype("int8")
    slot = _slot_index(frame, variant.slot_width_minutes)
    origin = _signal_source_origin(frame, context_after_gap)
    et_damage_blocked = origin.eq("et_slotfill") & (((slot.eq(6) & signal.eq(-1))) | (slot.eq(5) & signal.eq(1)))
    frame["source_slot40"] = slot
    frame["signal_source_origin"] = origin
    frame["firewall_rule_id"] = np.where(et_damage_blocked, "block_et_slot6_short_or_slot5_long", "none")
    frame["entry_transition_only"] = False
    if et_damage_blocked.any():
        frame.loc[et_damage_blocked, ctx.SIGNAL_COLUMN] = 0
    frame["entry_decision"] = frame[ctx.SIGNAL_COLUMN].map({-1: "short", 0: "flat", 1: "long"}).fillna("flat")
    frame["primary_source"] = "run50BE_v22_context_timed_gap_filtered"
    frame["secondary_source"] = "run50BH_et40h6_r001_a_extratrees_refill"
    return frame


def source_summary_rows(variant: ctx.ContextTimedVariant, frame: pd.DataFrame) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for split in ("train", "validation", "oos"):
        for tier in (ctx.mt5.TIER_A, ctx.mt5.TIER_B):
            view = frame.loc[frame["split"].astype(str).eq(split) & frame["tier_label"].astype(str).eq(tier)]
            final_signal = pd.to_numeric(view[ctx.SIGNAL_COLUMN], errors="coerce").fillna(0).astype("int8")
            rows.append(
                {
                    "variant_id": variant.variant_id,
                    "split": split,
                    "tier": tier,
                    "rows": int(len(view)),
                    "context_gap_policy": view["context_gap_policy"].iloc[0] if len(view) else "",
                    "context_raw_nonflat": int(pd.to_numeric(view["context_signal_raw"], errors="coerce").fillna(0).ne(0).sum()),
                    "context_after_gap_nonflat": int(pd.to_numeric(view["context_signal_after_gap"], errors="coerce").fillna(0).ne(0).sum()),
                    "context_gap_blocked": int(view["context_gap_blocked"].astype(bool).sum()),
                    "et40_nonflat": int(pd.to_numeric(view["et40_signal"], errors="coerce").fillna(0).ne(0).sum()),
                    "final_nonflat": int(final_signal.ne(0).sum()),
                    "final_long": int(final_signal.eq(1).sum()),
                    "final_short": int(final_signal.eq(-1).sum()),
                    "context_primary_nonflat": int(view["signal_source_origin"].astype(str).eq("context_primary").sum()),
                    "et_slotfill_nonflat": int(view["signal_source_origin"].astype(str).eq("et_slotfill").sum()),
                    "firewall_blocked": int(view["firewall_rule_id"].astype(str).eq("block_et_slot6_short_or_slot5_long").sum()),
                }
            )
    return rows


def build_variant_frames(
    variants: Sequence[ctx.ContextTimedVariant],
    common: pd.DataFrame,
) -> tuple[dict[str, pd.DataFrame], list[dict[str, Any]], list[dict[str, Any]]]:
    frames: dict[str, pd.DataFrame] = {}
    summary_rows: list[dict[str, Any]] = []
    lineage = bn.aw.source_lineage_entries()
    for role, path, affects in (
        ("run50BQ_transition_firewall_summary", bq.RESULTS_CSV_PATH, "transition-only failure and stable ET damage clue"),
        ("run50BQ_transition_firewall_audit", bq.AUDIT_CSV_PATH, "run50BQ same-move/cooldown evidence"),
        ("run50BN_slotfill_summary", bn.RESULTS_CSV_PATH, "slot-fill density/PF/net frontier with same-move failure"),
        ("run50BO_cooldown_summary", ctx.REVIEWS_ROOT / "run50BO_summary.csv", "global same-direction cooldown failure memory"),
    ):
        lineage.append(
            {
                "role": role,
                "path": ctx.rel(path),
                "sha256": sha256_file_lf_normalized(path) if path_exists(path) and io_path(path).is_file() else "missing",
                "artifact_kind": "prior_evidence",
                "affects": affects,
                "required_for_reproducibility": True,
            }
        )
    for variant in variants:
        frame = build_variant_frame(common, variant)
        frames[variant.variant_id] = frame
        summary_rows.extend(source_summary_rows(variant, frame))
    return frames, summary_rows, lineage


def export_feature_matrix(path: Path, frame: pd.DataFrame) -> dict[str, Any]:
    payload = ctx.mt5.export_mt5_feature_matrix_csv(
        frame,
        (ctx.SIGNAL_COLUMN,),
        path,
        metadata_columns=(
            "variant_id",
            "primary_source",
            "secondary_source",
            "composite_mode",
            "context_rule_id",
            "context_slot",
            "context_signal_raw",
            "context_signal_after_gap",
            "context_gap_policy",
            "context_gap_blocked",
            "et40_signal",
            "et40_decision_label",
            "et40_decision_probability",
            "et40_decision_margin",
            "et40_agrees_context",
            "et40_conflicts_context",
            "source_slot40",
            "signal_source_origin",
            "firewall_rule_id",
            "tier_label",
            "routing_source",
            "partial_context_subtype",
            "entry_decision",
        ),
    )
    payload["path"] = ctx.rel(Path(payload["path"]))
    return payload


def fmt(value: Any) -> str:
    return ctx.fmt(value)


def best_row(rows: Sequence[Mapping[str, Any]]) -> Mapping[str, Any] | None:
    return ctx.best_row(rows)


def write_report(rows: Sequence[Mapping[str, Any]], audit_rows: Sequence[Mapping[str, Any]], result: Mapping[str, Any]) -> None:
    best = best_row(rows) or {}
    lines = [
        "# Stage56 run50BR Context Gap Refill(문맥 간격 재채움)",
        "",
        f"- run_id(실행 ID): `{PARENT_RUN_ID}`",
        f"- packet_id(작업 묶음 ID): `{PACKET_ID}`",
        "- selected_research_baseline(선택 연구 기준선): `none`",
        f"- external_verification_status(외부 검증 상태): `{result.get('external_verification_status')}`",
        f"- claim_boundary(주장 경계): `{ctx.BOUNDARY}`",
        "",
        "Action(행동): context primary(문맥 1차) 반복 신호에만 source gap(원천 간격)을 적용하고, 빈 구간은 ET slot-fill(ExtraTrees 슬롯 채움)이 다시 채우게 했다.",
        "Effect(효과): global cooldown(전체 쿨다운) 없이 same-move density(동일 이동 밀도)를 줄일 수 있는지 실제 MT5 validation/OOS(검증/표본외)로 확인한다.",
        "",
        "## Best Read(최선 판독)",
        "",
        f"- best_variant(최선 변형): `{best.get('variant_id', 'none')}`",
        f"- validation/OOS trades/day(검증/표본외 일 거래): `{fmt(best.get('routed_validation_trades_per_day'))}` / `{fmt(best.get('routed_oos_trades_per_day'))}`",
        f"- validation/OOS PF(검증/표본외 수익 팩터): `{fmt(best.get('routed_validation_pf'))}` / `{fmt(best.get('routed_oos_pf'))}`",
        f"- validation/OOS net(검증/표본외 순손익): `{fmt(best.get('routed_validation_net'))}` / `{fmt(best.get('routed_oos_net'))}`",
        f"- failure_reasons(실패 이유): `{best.get('failure_reasons', '')}`",
        "",
        "| variant | hold | val day | oos day | val PF | oos PF | val net | oos net | same val/oos | cooldown day val/oos | failures |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in rows:
        lines.append(
            "| {variant} | {hold} | {vday} | {oday} | {vpf} | {opf} | {vnet} | {onet} | {samev}/{sameo} | {coolv}/{coolo} | {fail} |".format(
                variant=row.get("variant_id", ""),
                hold=row.get("max_hold_bars", ""),
                vday=fmt(row.get("routed_validation_trades_per_day")),
                oday=fmt(row.get("routed_oos_trades_per_day")),
                vpf=fmt(row.get("routed_validation_pf")),
                opf=fmt(row.get("routed_oos_pf")),
                vnet=fmt(row.get("routed_validation_net")),
                onet=fmt(row.get("routed_oos_net")),
                samev=fmt(row.get("routed_validation_same_move_reentry_ratio")),
                sameo=fmt(row.get("routed_oos_same_move_reentry_ratio")),
                coolv=fmt(row.get("routed_validation_trades_per_day_after_12bar_cooldown")),
                coolo=fmt(row.get("routed_oos_trades_per_day_after_12bar_cooldown")),
                fail=row.get("failure_reasons", ""),
            )
        )
    lines.extend(["", "## Audit Summary(감사 요약)", "", "| variant | split | MFE capture | same move | cooldown day | cost-stressed exp |", "|---|---|---:|---:|---:|---:|"])
    for row in audit_rows:
        variant = str(row.get("variant_id") or "")
        if not variant.startswith("v"):
            continue
        lines.append(
            "| {variant} | {split} | {mfe} | {same} | {cool} | {cse} |".format(
                variant=variant,
                split=row.get("split", ""),
                mfe=fmt(row.get("mfe_capture_ratio")),
                same=fmt(row.get("same_move_reentry_ratio")),
                cool=fmt(row.get("trades_per_day_after_cooldown")),
                cse=fmt(row.get("cost_stressed_expectancy")),
            )
        )
    lines.extend(["", "Judgment(판정): `in_progress_no_selected_research_baseline`.", "Effect(효과): run50BR(실행50BR)는 progress evidence(진행 근거)이며 Stage56(56단계)은 계속 open(열림)이다."])
    ctx.write_md(REPORT_PATH, "\n".join(lines))


def append_progress(best: Mapping[str, Any]) -> None:
    existing = io_path(ctx.PROGRESS_LOG_PATH).read_text(encoding="utf-8-sig") if path_exists(ctx.PROGRESS_LOG_PATH) else ""
    entry = f"""

## {ctx.utc_now()} run50BR Context Gap Refill(문맥 간격 재채움)

- action(행동): context primary(문맥 1차)의 same-direction repeat(동일 방향 반복)에 source gap(원천 간격)을 적용하고 ET slot-fill(ExtraTrees 슬롯 채움)로 재채움했다.
- effect(효과): density(밀도)를 global cooldown(전체 쿨다운)으로 죽이지 않고 same-move split(동일 이동 분할)을 줄일 수 있는지 확인했다.
- best_variant(현재 최선 변형): `{best.get('variant_id', 'none')}`
- validation/OOS trades/day(검증/표본외 일 거래): `{fmt(best.get('routed_validation_trades_per_day'))}` / `{fmt(best.get('routed_oos_trades_per_day'))}`
- validation/OOS PF(검증/표본외 수익 팩터): `{fmt(best.get('routed_validation_pf'))}` / `{fmt(best.get('routed_oos_pf'))}`
- validation/OOS net(검증/표본외 순손익): `{fmt(best.get('routed_validation_net'))}` / `{fmt(best.get('routed_oos_net'))}`
- decision(결정): selected_research_baseline(선택 연구 기준선)=`none`; failure_reasons(실패 이유)=`{best.get('failure_reasons', '')}`.
"""
    ctx.write_md(ctx.PROGRESS_LOG_PATH, existing.rstrip() + entry)


def _remove_workspace_block(text: str, block_key: str) -> str:
    lines = text.splitlines(keepends=True)
    output: list[str] = []
    index = 0
    while index < len(lines):
        if lines[index].startswith(block_key):
            index += 1
            while index < len(lines) and (not lines[index].strip() or lines[index].startswith(" ")):
                index += 1
            continue
        output.append(lines[index])
        index += 1
    return "".join(output)


def update_workspace_state(best: Mapping[str, Any]) -> None:
    path = io_path(ctx.WORKSPACE_STATE_PATH)
    text = path.read_text(encoding="utf-8-sig")
    text = re.sub(r"^current_run_id: .*$", f"current_run_id: {PARENT_RUN_ID}", text, count=1, flags=re.MULTILINE)
    focus = (
        f"- >-\n"
        f"  Stage56(56단계) `{ctx.STAGE_ID}`: run50BR(실행50BR) context gap refill(문맥 간격 재채움) 완료; "
        f"best_variant(현재 최선 변형)는 `{best.get('variant_id', 'none')}`이고 validation/OOS(검증/표본외) trades/day(일 거래 수) `{fmt(best.get('routed_validation_trades_per_day'))}` / `{fmt(best.get('routed_oos_trades_per_day'))}`, "
        f"PF(수익 팩터) `{fmt(best.get('routed_validation_pf'))}` / `{fmt(best.get('routed_oos_pf'))}`, "
        f"net(순손익) `{fmt(best.get('routed_validation_net'))}` / `{fmt(best.get('routed_oos_net'))}`이며 selected_research_baseline(선택 연구 기준선)은 `none`이다. "
        f"Effect(효과): `{best.get('failure_reasons', '')}` 때문에 hard condition(강한 완료 조건)을 통과하지 못해 Stage56(56단계)을 계속 open(열림)으로 둔다."
    )
    text = re.sub(r"current_focus:\n", f"current_focus:\n{focus}\n", text, count=1)
    text = _remove_workspace_block(text, WORKSPACE_BLOCK_KEY)
    block = (
        f"\n{WORKSPACE_BLOCK_KEY}\n"
        f"  packet_id: {PACKET_ID}\n"
        f"  current_run_id: {PARENT_RUN_ID}\n"
        f"  best_variant: {best.get('variant_id', 'none')}\n"
        "  selected_research_baseline: none\n"
        f"  failure_reasons: {best.get('failure_reasons', '')}\n"
        "  boundary: research_baseline_selection_only_no_operating_claim\n"
        "  next_action: evaluate_context_gap_refill_or_open_new_model_source_branch\n"
    )
    path.write_text(text.rstrip() + "\n" + block, encoding="utf-8-sig")


def update_current_truth(rows: Sequence[Mapping[str, Any]]) -> None:
    best = best_row(rows) or {}
    best_id = best.get("variant_id", "none")
    failures = best.get("failure_reasons", "")
    ctx.write_md(
        ctx.CURRENT_WORKING_STATE_PATH,
        f"""# Current Working State(현재 작업 상태)

- current_packet(현재 작업 묶음): `{PACKET_ID}`
- current run(현재 실행): `{PARENT_RUN_ID}`
- active stage(활성 단계): `{ctx.STAGE_ID}`
- selected_research_baseline(선택 연구 기준선): `none`
- status(상태): active_in_progress(활성 진행 중)
- terminal_condition(종료 조건): useful BaselineAdapter(유용한 기준선 어댑터) hard condition(강한 완료 조건) not_satisfied(미충족)

Stage56(56단계)은 unfinished optimization campaign(미완 최적화 캠페인)으로 계속 열려 있다. Effect(효과): run50BR(실행50BR)는 context source gap(문맥 원천 간격)과 ET refill(ExtraTrees 재채움)을 실제 MT5 validation/OOS(검증/표본외)로 시험한 근거다.

## Latest Evidence(최신 근거)

- latest_batch(최신 묶음): `{PARENT_RUN_ID}`
- best_variant(현재 최선 변형): `{best_id}`
- selected_research_baseline(선택 연구 기준선): `none`
- validation/OOS trades/day(검증/표본외 일 거래): `{fmt(best.get('routed_validation_trades_per_day'))}` / `{fmt(best.get('routed_oos_trades_per_day'))}`
- validation/OOS PF(검증/표본외 수익 팩터): `{fmt(best.get('routed_validation_pf'))}` / `{fmt(best.get('routed_oos_pf'))}`
- validation/OOS net(검증/표본외 순손익): `{fmt(best.get('routed_validation_net'))}` / `{fmt(best.get('routed_oos_net'))}`
- latest_failure(최신 실패): `{failures}`

## Current Bottleneck(현재 병목)

- run50BR judgment(실행50BR 판정): selected_research_baseline(선택 연구 기준선)은 `none`이다. Effect(효과): failure_reasons(실패 이유) `{failures}` 때문에 hard condition(강한 완료 조건)을 통과하지 못했다.
- next_hypothesis_branch(다음 가설 분기): `evaluate_context_gap_refill_or_open_new_model_source_branch`

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

## Latest Run50BR Intermediate Evidence(최신 50BR 중간 근거)

- packet(묶음): `{PACKET_ID}`
- report(보고서): `{REPORT_PATH.as_posix()}`
- summary_csv(요약 CSV): `{RESULTS_CSV_PATH.as_posix()}`
- audit_csv(감사 CSV): `{AUDIT_CSV_PATH.as_posix()}`
- aggregate_summary(합산 요약): `{AGGREGATE_SUMMARY_PATH.as_posix()}`

Best read(최선 판독) `{best_id}` validation/OOS(검증/표본외) trades/day(일 거래) `{fmt(best.get('routed_validation_trades_per_day'))}` / `{fmt(best.get('routed_oos_trades_per_day'))}`, PF(수익 팩터) `{fmt(best.get('routed_validation_pf'))}` / `{fmt(best.get('routed_oos_pf'))}`, net(순손익) `{fmt(best.get('routed_validation_net'))}` / `{fmt(best.get('routed_oos_net'))}`이다.

Failure(실패): `{failures}`. Effect(효과): selected_research_baseline(선택 연구 기준선)을 만들지 않고 Stage56(56단계)을 계속 open(열림)으로 둔다.
""",
    )
    append_progress(best)
    update_workspace_state(best)


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str] | None = None) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    if columns is None:
        ordered: list[str] = []
        for row in rows:
            for key in row:
                if key not in ordered:
                    ordered.append(key)
        columns = tuple(ordered)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        writer.writerows([json_ready(row) for row in rows])


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
    ctx.SIGNAL_COLUMN = SIGNAL_COLUMN
    ctx.DEFAULT_VARIANTS = DEFAULT_VARIANTS
    ctx.__file__ = __file__
    ctx.build_variant_frame = build_variant_frame
    ctx.build_variant_frames = build_variant_frames
    ctx.source_summary_rows = source_summary_rows
    ctx.export_feature_matrix = export_feature_matrix
    ctx.build_attempts = bq.build_attempts
    ctx.write_report = write_report
    ctx.append_progress = append_progress
    ctx.update_workspace_state = update_workspace_state
    ctx.update_current_truth = update_current_truth
    ctx.write_csv = write_csv


def main(argv: list[str] | None = None) -> int:
    patch_context()
    return ctx.main(argv)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
