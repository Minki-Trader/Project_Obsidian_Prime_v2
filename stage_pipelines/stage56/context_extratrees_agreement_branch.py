from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.control_plane.ledger import io_path, path_exists, sha256_file_lf_normalized  # noqa: E402
from stage_pipelines.stage56 import context_timed_opportunity_source_branch as ctx  # noqa: E402
from stage_pipelines.stage56 import context_timed_v22_density_topup_branch as be  # noqa: E402
from stage_pipelines.stage56 import independent_event_source_route_branch as aw  # noqa: E402


RUN_NUMBER = "run50BN"
PARENT_RUN_ID = "run50BN_stage56_context_extratrees_agreement_v1"
PACKET_ID = "stage56_run50BN_context_extratrees_agreement_v1"
EXPLORATION_LABEL = "stage56_BaseEngine__ContextExtraTreesAgreement"
REPORT_PATH = ctx.REVIEWS_ROOT / "run50BN_context_extratrees_agreement.md"
RESULTS_CSV_PATH = ctx.REVIEWS_ROOT / "run50BN_summary.csv"
AUDIT_CSV_PATH = ctx.REVIEWS_ROOT / "run50BN_audit.csv"
SOURCE_SUMMARY_CSV_PATH = ctx.REVIEWS_ROOT / "run50BN_source_summary.csv"
PACKET_ROOT = Path("docs/agent_control/packets") / PACKET_ID
AGGREGATE_SUMMARY_PATH = PACKET_ROOT / "aggregate_summary.json"
RUN_ROOT = ctx.STAGE_ROOT / "02_runs" / RUN_NUMBER
COMMON_ROOT = f"Project_Obsidian_Prime_v2/stage56/{RUN_NUMBER}_context_extratrees_agreement"
SIGNAL_COLUMN = "stage56_context_et_event_signal"
WORKSPACE_BLOCK_KEY = "stage56_run50bn_context_extratrees_agreement:"

RUN50BH_PRED_ROOT = (
    ctx.STAGE_ROOT
    / "02_runs"
    / "run50BH"
    / "et40h6_r001_a"
    / "predictions"
)
RUN50BH_SUMMARY = ctx.REVIEWS_ROOT / "run50BH_summary.csv"
RUN50BH_AUDIT = ctx.REVIEWS_ROOT / "run50BH_audit.csv"
RUN50BE_SUMMARY = ctx.REVIEWS_ROOT / "run50BE_summary.csv"
RUN50BE_AUDIT = ctx.REVIEWS_ROOT / "run50BE_audit.csv"


DEFAULT_VARIANTS = (
    ctx.ContextTimedVariant(
        "v41_v22_midcov_et40_agree_h2c0_no_b",
        "v22_midcov_et40_agreement",
        40,
        be.bd.W40_ESOL_MIDCOV_RULES,
        2,
        0,
        False,
        "Run50BE v30 context entries are kept only when run50BH ExtraTrees agrees on direction; Tier B disabled.",
        "context_et40_agree",
    ),
    ctx.ContextTimedVariant(
        "v42_v22_midcov_et40_veto_conflict_h2c0_no_b",
        "v22_midcov_et40_conflict_veto",
        40,
        be.bd.W40_ESOL_MIDCOV_RULES,
        2,
        0,
        False,
        "Run50BE v30 context entries are kept unless run50BH ExtraTrees explicitly disagrees; Tier B disabled.",
        "context_et40_veto_conflict",
    ),
    ctx.ContextTimedVariant(
        "v43_v22_midcov_et40_direction_h2c0_no_b",
        "v22_midcov_et40_direction_override",
        40,
        be.bd.W40_ESOL_MIDCOV_RULES,
        2,
        0,
        False,
        "Run50BE v30 context timing is used as the opportunity clock, while run50BH ExtraTrees supplies direction when non-flat.",
        "context_timing_et40_direction",
    ),
    ctx.ContextTimedVariant(
        "v44_v22_topup_et40_veto_conflict_h2c0_no_b",
        "v22_topup_et40_conflict_veto",
        40,
        be.V22_SLOT3_5_8_TOPUP,
        2,
        0,
        False,
        "Higher-coverage v22 slot 3/5/8 top-up uses ExtraTrees as a conflict veto; Tier B disabled.",
        "context_et40_veto_conflict",
    ),
    ctx.ContextTimedVariant(
        "v45_v22_midcov_et40_veto_conflict_h2c0_with_b",
        "v22_midcov_et40_tier_b_audit",
        40,
        be.bd.W40_ESOL_MIDCOV_RULES,
        2,
        0,
        True,
        "Matched Tier B fallback audit for the ExtraTrees conflict-veto context branch.",
        "context_et40_veto_conflict",
    ),
    ctx.ContextTimedVariant(
        "v46_v22_midcov_plus_et40_slotfill_h2c0_no_b",
        "v22_midcov_et40_slot_fill",
        40,
        be.bd.W40_ESOL_MIDCOV_RULES,
        2,
        0,
        False,
        "Run50BE v30 context source remains primary; context-flat slots can be filled once by ExtraTrees direction.",
        "context_plus_et40_slot_fill",
    ),
    ctx.ContextTimedVariant(
        "v47_v22_topup_plus_et40_slotfill_h2c0_no_b",
        "v22_topup_et40_slot_fill",
        40,
        be.V22_SLOT3_5_8_TOPUP,
        2,
        0,
        False,
        "Higher-coverage v22 slot 3/5/8 source remains primary; context-flat slots can be filled once by ExtraTrees direction.",
        "context_plus_et40_slot_fill",
    ),
)


_ORIGINAL_BUILD_VARIANT_FRAME = ctx.build_variant_frame


def _et_signal_from_decision(value: Any) -> int:
    try:
        label = int(value)
    except (TypeError, ValueError):
        return 0
    if label == 0:
        return -1
    if label == 2:
        return 1
    return 0


def load_et40_predictions() -> pd.DataFrame:
    frames = []
    for tier_name, path in (
        ("Tier A", RUN50BH_PRED_ROOT / "tier_a_predictions.parquet"),
        ("Tier B", RUN50BH_PRED_ROOT / "tier_b_predictions.parquet"),
    ):
        frame = pd.read_parquet(io_path(path))
        frame = frame.copy()
        frame["timestamp"] = pd.to_datetime(frame["timestamp"], utc=True)
        frame["split"] = frame["split"].astype(str)
        frame["tier_label"] = tier_name
        frame["et40_signal"] = frame["decision_label_class"].map(_et_signal_from_decision).astype("int8")
        frame["et40_decision_label"] = frame["decision_label"].astype(str)
        frames.append(
            frame[
                [
                    "timestamp",
                    "split",
                    "tier_label",
                    "et40_signal",
                    "et40_decision_label",
                    "decision_probability",
                    "decision_margin",
                    "p_short",
                    "p_flat",
                    "p_long",
                ]
            ].rename(
                columns={
                    "decision_probability": "et40_decision_probability",
                    "decision_margin": "et40_decision_margin",
                    "p_short": "et40_p_short",
                    "p_flat": "et40_p_flat",
                    "p_long": "et40_p_long",
                }
            )
        )
    return pd.concat(frames, ignore_index=True)


def _slot_fill_signal(frame: pd.DataFrame, base_signal: pd.Series, et_signal: pd.Series, slot_width_minutes: int) -> pd.Series:
    signal = base_signal.copy()
    timestamp = pd.to_datetime(frame["timestamp"], utc=True)
    minutes = pd.to_numeric(frame["minutes_from_cash_open"], errors="coerce")
    slots = np.floor(minutes / float(slot_width_minutes))
    fill_mask = signal.eq(0) & et_signal.ne(0) & minutes.between(0, 389, inclusive="both")
    fill_frame = pd.DataFrame(
        {
            "timestamp": timestamp,
            "split": frame["split"].astype(str),
            "date": timestamp.dt.strftime("%Y-%m-%d"),
            "tier_label": frame["tier_label"].astype(str),
            "slot": slots,
        },
        index=frame.index,
    ).loc[fill_mask]
    fill_index = (
        fill_frame.sort_values("timestamp")
        .groupby(["split", "date", "tier_label", "slot"], sort=False)
        .head(1)
        .index
    )
    signal.loc[fill_index] = et_signal.loc[fill_index]
    return signal.astype("int8")


def combine_context_et_signals(frame: pd.DataFrame, mode: str, slot_width_minutes: int) -> pd.Series:
    context_signal = pd.to_numeric(frame["context_signal_raw"], errors="coerce").fillna(0).astype("int8")
    et_signal = pd.to_numeric(frame["et40_signal"], errors="coerce").fillna(0).astype("int8")
    context_nonflat = context_signal.ne(0)
    et_nonflat = et_signal.ne(0)
    agree = context_nonflat & et_signal.eq(context_signal)
    conflict = context_nonflat & et_nonflat & et_signal.ne(context_signal)
    if mode == "context_et40_agree":
        signal = np.where(agree, context_signal, 0)
    elif mode == "context_et40_veto_conflict":
        signal = np.where(context_nonflat & ~conflict, context_signal, 0)
    elif mode == "context_timing_et40_direction":
        signal = np.where(context_nonflat & et_nonflat, et_signal, 0)
    elif mode == "context_plus_et40_slot_fill":
        return _slot_fill_signal(frame, context_signal, et_signal, slot_width_minutes)
    else:
        raise ValueError(f"unknown composite mode: {mode}")
    return pd.Series(signal, index=frame.index, dtype="int8")


def build_variant_frame(common: pd.DataFrame, variant: ctx.ContextTimedVariant) -> pd.DataFrame:
    frame = _ORIGINAL_BUILD_VARIANT_FRAME(common, variant)
    frame["timestamp"] = pd.to_datetime(frame["timestamp"], utc=True)
    frame["context_signal_raw"] = pd.to_numeric(frame[ctx.SIGNAL_COLUMN], errors="coerce").fillna(0).astype("int8")
    et_predictions = load_et40_predictions()
    frame = frame.merge(et_predictions, on=["timestamp", "split", "tier_label"], how="left")
    frame["et40_signal"] = pd.to_numeric(frame["et40_signal"], errors="coerce").fillna(0).astype("int8")
    frame["et40_agrees_context"] = frame["context_signal_raw"].ne(0) & frame["et40_signal"].eq(frame["context_signal_raw"])
    frame["et40_conflicts_context"] = (
        frame["context_signal_raw"].ne(0)
        & frame["et40_signal"].ne(0)
        & frame["et40_signal"].ne(frame["context_signal_raw"])
    )
    frame[ctx.SIGNAL_COLUMN] = combine_context_et_signals(frame, variant.composite_mode, variant.slot_width_minutes)
    frame["entry_decision"] = frame[ctx.SIGNAL_COLUMN].map({-1: "short", 0: "flat", 1: "long"}).fillna("flat")
    frame["primary_source"] = "run50BE_v22_context_timed"
    frame["secondary_source"] = "run50BH_et40h6_r001_a_extratrees"
    return frame


def source_summary_rows(variant: ctx.ContextTimedVariant, frame: pd.DataFrame) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for split in ("train", "validation", "oos"):
        for tier in (ctx.mt5.TIER_A, ctx.mt5.TIER_B):
            view = frame.loc[frame["split"].astype(str).eq(split) & frame["tier_label"].astype(str).eq(tier)]
            final_signal = pd.to_numeric(view[ctx.SIGNAL_COLUMN], errors="coerce").fillna(0).astype("int8")
            context_signal = pd.to_numeric(view["context_signal_raw"], errors="coerce").fillna(0).astype("int8")
            et_signal = pd.to_numeric(view["et40_signal"], errors="coerce").fillna(0).astype("int8")
            rows.append(
                {
                    "variant_id": variant.variant_id,
                    "split": split,
                    "tier": tier,
                    "composite_mode": variant.composite_mode,
                    "rows": int(len(view)),
                    "context_nonflat": int(context_signal.ne(0).sum()),
                    "et40_nonflat": int(et_signal.ne(0).sum()),
                    "context_et40_agree": int((context_signal.ne(0) & et_signal.eq(context_signal)).sum()),
                    "context_et40_conflict": int((context_signal.ne(0) & et_signal.ne(0) & et_signal.ne(context_signal)).sum()),
                    "final_nonflat": int(final_signal.ne(0).sum()),
                    "final_long": int(final_signal.eq(1).sum()),
                    "final_short": int(final_signal.eq(-1).sum()),
                }
            )
    return rows


def build_variant_frames(
    variants: Sequence[ctx.ContextTimedVariant],
    common: pd.DataFrame,
) -> tuple[dict[str, pd.DataFrame], list[dict[str, Any]], list[dict[str, Any]]]:
    frames: dict[str, pd.DataFrame] = {}
    summary_rows: list[dict[str, Any]] = []
    lineage = aw.source_lineage_entries()
    for role, path, affects in (
        ("run50BH_frontier_summary", RUN50BH_SUMMARY, "ExtraTrees OOS PF/net frontier and same-move failure memory"),
        ("run50BH_frontier_audit", RUN50BH_AUDIT, "same-move and cooldown survival audit for ExtraTrees anchor"),
        ("run50BE_context_summary", RUN50BE_SUMMARY, "context-timed low same-move real-density clue"),
        ("run50BE_context_audit", RUN50BE_AUDIT, "context-timed MFE and cooldown audit"),
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
            "et40_signal",
            "et40_decision_label",
            "et40_decision_probability",
            "et40_decision_margin",
            "et40_agrees_context",
            "et40_conflicts_context",
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


def write_report(rows: Sequence[Mapping[str, Any]], audit_rows: Sequence[Mapping[str, Any]], result: Mapping[str, Any]) -> None:
    best = ctx.best_row(rows) or {}
    lines = [
        "# Stage56 run50BN Context ExtraTrees Agreement(문맥 ExtraTrees 합의)",
        "",
        f"- run_id(실행 ID): `{PARENT_RUN_ID}`",
        f"- packet_id(작업 묶음 ID): `{PACKET_ID}`",
        "- selected_research_baseline(선택 연구 기준선): `none`",
        f"- external_verification_status(외부 검증 상태): `{result.get('external_verification_status')}`",
        f"- claim_boundary(주장 경계): `{ctx.BOUNDARY}`",
        "",
        "Action(행동): run50BE context-timed(문맥/시간) source(원천)를 기회 시계(opportunity clock, 기회 시계)로 두고, run50BH ExtraTrees(엑스트라트리스)를 방향 합의/충돌 veto(거부)로 붙여 실제 MT5 validation/OOS(검증/표본외)를 실행했다.",
        "Effect(효과): same-move density(동일 이동 밀도)를 낮춘 context route(문맥 라우트)에 ExtraTrees OOS quality(표본외 품질)가 붙는지 확인한다.",
        "",
        "## Best Read(최선 판독)",
        "",
        f"- best_variant(최선 변형): `{best.get('variant_id', 'none')}`",
        f"- validation/OOS trades/day(검증/표본외 일 거래): `{fmt(best.get('routed_validation_trades_per_day'))}` / `{fmt(best.get('routed_oos_trades_per_day'))}`",
        f"- validation/OOS PF(검증/표본외 수익 팩터): `{fmt(best.get('routed_validation_pf'))}` / `{fmt(best.get('routed_oos_pf'))}`",
        f"- validation/OOS net(검증/표본외 순손익): `{fmt(best.get('routed_validation_net'))}` / `{fmt(best.get('routed_oos_net'))}`",
        f"- failure_reasons(실패 이유): `{best.get('failure_reasons', '')}`",
        "",
        "| variant | mode | fallback | val day | oos day | val PF | oos PF | val net | oos net | same val/oos | cooldown day val/oos | failures |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in rows:
        lines.append(
            "| {variant} | {mode} | {fallback} | {vday} | {oday} | {vpf} | {opf} | {vnet} | {onet} | {samev}/{sameo} | {coolv}/{coolo} | {fail} |".format(
                variant=row.get("variant_id", ""),
                mode=row.get("composite_mode", ""),
                fallback=row.get("routed_fallback_enabled", ""),
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
    lines.extend(
        [
            "",
            "## Tier Views(티어 보기)",
            "",
            "| variant | Tier A val/OOS net | Tier B-only val/OOS net | routed val/OOS net |",
            "|---|---:|---:|---:|",
        ]
    )
    for row in rows:
        lines.append(
            "| {variant} | {ta} / {tao} | {tb} / {tbo} | {rv} / {ro} |".format(
                variant=row.get("variant_id", ""),
                ta=fmt(row.get("tier_a_validation_net")),
                tao=fmt(row.get("tier_a_oos_net")),
                tb=fmt(row.get("tier_b_validation_net")),
                tbo=fmt(row.get("tier_b_oos_net")),
                rv=fmt(row.get("routed_validation_net")),
                ro=fmt(row.get("routed_oos_net")),
            )
        )
    lines.extend(
        [
            "",
            "## Audit Summary(감사 요약)",
            "",
            "| variant | split | MFE capture | same move | cooldown day | cost-stressed exp |",
            "|---|---|---:|---:|---:|---:|",
        ]
    )
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
    lines.extend(
        [
            "",
            "Judgment(판정): `in_progress_no_selected_research_baseline`.",
            "Effect(효과): run50BN(실행50BN)은 progress evidence(진행 근거)이며 Stage56(56단계)은 계속 open(열림)이다.",
        ]
    )
    ctx.write_md(REPORT_PATH, "\n".join(lines))


def append_progress(best: Mapping[str, Any]) -> None:
    existing = io_path(ctx.PROGRESS_LOG_PATH).read_text(encoding="utf-8-sig") if path_exists(ctx.PROGRESS_LOG_PATH) else ""
    entry = f"""

## {ctx.utc_now()} run50BN Context ExtraTrees Agreement(문맥 ExtraTrees 합의)

- action(행동): context-timed(문맥/시간) source(원천)와 run50BH ExtraTrees(엑스트라트리스)를 합의/충돌 veto(거부) 방식으로 결합해 actual MT5 validation/OOS(실제 MT5 검증/표본외)를 실행했다.
- effect(효과): low same-move(낮은 동일 이동) 구조에 OOS quality(표본외 품질)를 붙일 수 있는지 확인했다.
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
    focus = (
        f"- >-\n"
        f"  Stage56(56단계) `{ctx.STAGE_ID}`: run50BN(실행50BN) context ExtraTrees agreement(문맥 ExtraTrees 합의) 완료; "
        f"best_variant(현재 최선 변형)는 `{best.get('variant_id', 'none')}`이고 validation/OOS(검증/표본외) "
        f"trades/day(일 거래 수) `{fmt(best.get('routed_validation_trades_per_day'))}` / `{fmt(best.get('routed_oos_trades_per_day'))}`, "
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
        "  next_action: evaluate_context_extratrees_failure_or_open_new_model_branch\n"
    )
    path.write_text(text.rstrip() + "\n" + block, encoding="utf-8-sig")


def update_current_truth(rows: Sequence[Mapping[str, Any]]) -> None:
    best = ctx.best_row(rows) or {}
    best_id = best.get("variant_id", "none")
    failures = best.get("failure_reasons", "")
    val_day = fmt(best.get("routed_validation_trades_per_day"))
    oos_day = fmt(best.get("routed_oos_trades_per_day"))
    val_pf = fmt(best.get("routed_validation_pf"))
    oos_pf = fmt(best.get("routed_oos_pf"))
    val_net = fmt(best.get("routed_validation_net"))
    oos_net = fmt(best.get("routed_oos_net"))
    ctx.write_md(
        ctx.CURRENT_WORKING_STATE_PATH,
        f"""# Current Working State(현재 작업 상태)

- current_packet(현재 작업 묶음): `{PACKET_ID}`
- current run(현재 실행): `{PARENT_RUN_ID}`
- active stage(활성 단계): `{ctx.STAGE_ID}`
- selected_research_baseline(선택 연구 기준선): `none`
- status(상태): active_in_progress(활성 진행 중)
- terminal_condition(종료 조건): useful BaselineAdapter(유용한 기준선 어댑터) hard condition(강한 완료 조건) not_satisfied(미충족)

Stage56(56단계)은 unfinished optimization campaign(미완 최적화 캠페인)으로 계속 열려 있다. Effect(효과): run50BN(실행50BN)은 context-timed(문맥/시간) source(원천)의 real-density clue(실제 밀도 단서)와 run50BH ExtraTrees(엑스트라트리스)의 OOS quality(표본외 품질)를 결합한 MT5 validation/OOS(검증/표본외) 근거다.

## Latest Evidence(최신 근거)

- latest_batch(최신 묶음): `{PARENT_RUN_ID}`
- best_variant(현재 최선 변형): `{best_id}`
- selected_research_baseline(선택 연구 기준선): `none`
- validation/OOS trades/day(검증/표본외 일 거래): `{val_day}` / `{oos_day}`
- validation/OOS PF(검증/표본외 수익 팩터): `{val_pf}` / `{oos_pf}`
- validation/OOS net(검증/표본외 순손익): `{val_net}` / `{oos_net}`
- latest_failure(최신 실패): `{failures}`
- current_frontier_candidate_preserved(현재 최전선 후보 보존): `run50BH/et40h6_r001_a`

## Current Bottleneck(현재 병목)

- run50BN judgment(실행50BN 판정): selected_research_baseline(선택 연구 기준선)은 `none`이다. Effect(효과): failure_reasons(실패 이유) `{failures}` 때문에 hard condition(강한 완료 조건)을 통과하지 못했다.
- next_hypothesis_branch(다음 가설 분기): `evaluate_context_extratrees_failure_or_open_new_model_branch`

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

## Latest Run50BN Intermediate Evidence(최신 50BN 중간 근거)

- packet(묶음): `{PACKET_ID}`
- report(보고서): `{REPORT_PATH.as_posix()}`
- summary_csv(요약 CSV): `{RESULTS_CSV_PATH.as_posix()}`
- audit_csv(감사 CSV): `{AUDIT_CSV_PATH.as_posix()}`
- aggregate_summary(합산 요약): `{AGGREGATE_SUMMARY_PATH.as_posix()}`

Best read(최선 판독) `{best_id}` validation/OOS(검증/표본외) trades/day(일 거래) `{val_day}` / `{oos_day}`, PF(수익 팩터) `{val_pf}` / `{oos_pf}`, net(순손익) `{val_net}` / `{oos_net}`이다.

Failure(실패): `{failures}`. Effect(효과): selected_research_baseline(선택 연구 기준선)을 만들지 않고 Stage56(56단계)을 계속 open(열림)으로 둔다.
""",
    )
    append_progress(best)
    update_workspace_state(best)


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
    ctx.write_report = write_report
    ctx.append_progress = append_progress
    ctx.update_workspace_state = update_workspace_state
    ctx.update_current_truth = update_current_truth


def main(argv: list[str] | None = None) -> int:
    patch_context()
    return ctx.main(argv)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
