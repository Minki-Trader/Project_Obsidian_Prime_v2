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
from foundation.models.onnx_bridge import ordered_hash  # noqa: E402
from stage_pipelines.stage56 import context_extratrees_agreement_branch as bn  # noqa: E402
from stage_pipelines.stage56 import context_timed_opportunity_source_branch as ctx  # noqa: E402
from stage_pipelines.stage56 import context_timed_v22_density_topup_branch as be  # noqa: E402


RUN_NUMBER = "run50BQ"
PARENT_RUN_ID = "run50BQ_stage56_context_extratrees_firewall_transition_v1"
PACKET_ID = "stage56_run50BQ_context_extratrees_firewall_transition_v1"
EXPLORATION_LABEL = "stage56_BaseEngine__ContextExtraTreesFirewallTransition"
REPORT_PATH = ctx.REVIEWS_ROOT / "run50BQ_context_extratrees_firewall_transition.md"
RESULTS_CSV_PATH = ctx.REVIEWS_ROOT / "run50BQ_summary.csv"
AUDIT_CSV_PATH = ctx.REVIEWS_ROOT / "run50BQ_audit.csv"
SOURCE_SUMMARY_CSV_PATH = ctx.REVIEWS_ROOT / "run50BQ_source_summary.csv"
PACKET_ROOT = Path("docs/agent_control/packets") / PACKET_ID
AGGREGATE_SUMMARY_PATH = PACKET_ROOT / "aggregate_summary.json"
RUN_ROOT = ctx.STAGE_ROOT / "02_runs" / RUN_NUMBER
COMMON_ROOT = f"Project_Obsidian_Prime_v2/stage56/{RUN_NUMBER}_context_extratrees_firewall_transition"
SIGNAL_COLUMN = "stage56_context_et_firewall_signal"
WORKSPACE_BLOCK_KEY = "stage56_run50bq_context_extratrees_firewall_transition:"


DEFAULT_VARIANTS = (
    ctx.ContextTimedVariant(
        "v60_v47_et_stable_damage_firewall_h2c0_no_b",
        "v47_et_stable_damage_firewall",
        40,
        be.V22_SLOT3_5_8_TOPUP,
        2,
        0,
        False,
        "Run50BN v47 plus ET slot-fill stable damage firewall; blocks ET slot6 short and slot5 long.",
        "context_plus_et40_slot_fill",
    ),
    ctx.ContextTimedVariant(
        "v61_v47_et_firewall_h2_transition_no_b",
        "v47_et_firewall_transition",
        40,
        be.V22_SLOT3_5_8_TOPUP,
        2,
        0,
        False,
        "Run50BN v47 plus ET stable damage firewall and entry-transition-only execution.",
        "context_plus_et40_slot_fill",
    ),
    ctx.ContextTimedVariant(
        "v62_v47_et_firewall_h4_transition_no_b",
        "v47_et_firewall_transition_hold4",
        40,
        be.V22_SLOT3_5_8_TOPUP,
        4,
        0,
        False,
        "Run50BN v47 plus ET stable damage firewall, entry-transition-only execution, and hold4.",
        "context_plus_et40_slot_fill",
    ),
    ctx.ContextTimedVariant(
        "v63_v47_et_firewall_h6_transition_no_b",
        "v47_et_firewall_transition_hold6",
        40,
        be.V22_SLOT3_5_8_TOPUP,
        6,
        0,
        False,
        "Run50BN v47 plus ET stable damage firewall, entry-transition-only execution, and hold6.",
        "context_plus_et40_slot_fill",
    ),
)


def _entry_transition_enabled(variant: ctx.ContextTimedVariant) -> bool:
    return "transition" in variant.variant_id


def _firewall_enabled(variant: ctx.ContextTimedVariant) -> bool:
    return "firewall" in variant.variant_id


def _slot_index(frame: pd.DataFrame, slot_width_minutes: int) -> pd.Series:
    minutes = pd.to_numeric(frame["minutes_from_cash_open"], errors="coerce")
    return np.floor(minutes / float(slot_width_minutes))


def _signal_source_origin(frame: pd.DataFrame) -> pd.Series:
    signal = pd.to_numeric(frame[ctx.SIGNAL_COLUMN], errors="coerce").fillna(0).astype("int8")
    context_signal = pd.to_numeric(frame["context_signal_raw"], errors="coerce").fillna(0).astype("int8")
    et_signal = pd.to_numeric(frame["et40_signal"], errors="coerce").fillna(0).astype("int8")
    return pd.Series(
        np.where(
            context_signal.ne(0),
            "context_primary",
            np.where(signal.ne(0) & et_signal.ne(0), "et_slotfill", "flat"),
        ),
        index=frame.index,
    )


def build_variant_frame(common: pd.DataFrame, variant: ctx.ContextTimedVariant) -> pd.DataFrame:
    frame = bn.build_variant_frame(common, variant)
    signal = pd.to_numeric(frame[ctx.SIGNAL_COLUMN], errors="coerce").fillna(0).astype("int8")
    slot = _slot_index(frame, variant.slot_width_minutes)
    origin = _signal_source_origin(frame)
    blocked = (
        _firewall_enabled(variant)
        & origin.eq("et_slotfill")
        & (((slot.eq(6) & signal.eq(-1))) | (slot.eq(5) & signal.eq(1)))
    )
    frame["source_slot40"] = slot
    frame["signal_source_origin"] = origin
    frame["firewall_rule_id"] = np.where(
        blocked,
        "block_et_slot6_short_or_slot5_long",
        "none",
    )
    frame["entry_transition_only"] = _entry_transition_enabled(variant)
    if blocked.any():
        frame.loc[blocked, ctx.SIGNAL_COLUMN] = 0
        frame.loc[blocked, "entry_decision"] = "flat"
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
                    "entry_transition_only": _entry_transition_enabled(variant),
                    "firewall_enabled": _firewall_enabled(variant),
                    "rows": int(len(view)),
                    "context_nonflat": int(context_signal.ne(0).sum()),
                    "et40_nonflat": int(et_signal.ne(0).sum()),
                    "final_nonflat": int(final_signal.ne(0).sum()),
                    "final_long": int(final_signal.eq(1).sum()),
                    "final_short": int(final_signal.eq(-1).sum()),
                    "context_primary_nonflat": int(
                        view["signal_source_origin"].astype(str).eq("context_primary").sum()
                    ),
                    "et_slotfill_nonflat": int(view["signal_source_origin"].astype(str).eq("et_slotfill").sum()),
                    "firewall_blocked": int(
                        view["firewall_rule_id"].astype(str).eq("block_et_slot6_short_or_slot5_long").sum()
                    ),
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
        ("run50BN_slotfill_summary", bn.RESULTS_CSV_PATH, "slot-fill frontier with cost/same-move failure"),
        ("run50BN_slotfill_audit", bn.AUDIT_CSV_PATH, "run50BN MFE, same-move, and cooldown audit"),
        ("run50BO_cooldown_summary", ctx.REVIEWS_ROOT / "run50BO_summary.csv", "same-direction cooldown failure memory"),
        ("run50BP_slot_lifecycle_summary", ctx.REVIEWS_ROOT / "run50BP_summary.csv", "pure ET slot lifecycle failure memory"),
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
            "source_slot40",
            "signal_source_origin",
            "firewall_rule_id",
            "entry_transition_only",
            "tier_label",
            "routing_source",
            "partial_context_subtype",
            "entry_decision",
        ),
    )
    payload["path"] = ctx.rel(Path(payload["path"]))
    return payload


def build_attempts(
    variants: Sequence[ctx.ContextTimedVariant],
    common: pd.DataFrame,
    feature_exports: Mapping[str, Mapping[str, Any]],
    model_artifact: Mapping[str, Any],
) -> list[dict[str, Any]]:
    attempts: list[dict[str, Any]] = []
    model_name = Path(str(model_artifact["path"])).name
    model_common = f"{ctx.COMMON_ROOT}/models/{model_name}"
    feature_hash = ordered_hash((ctx.SIGNAL_COLUMN,))
    base_extra_set_values = {
        "InpEntryTransitionRearmMinConfidenceDelta": 0.0,
        "InpAtrSltpEnabled": False,
        "InpAtrPeriod": 14,
        "InpAtrStopMultiplier": 0.0,
        "InpAtrTakeProfitMultiplier": 0.0,
    }
    for variant_index, variant in enumerate(variants, 1):
        variant_short = f"x{variant_index:02d}"
        variant_extra = {
            **base_extra_set_values,
            "InpReentryCooldownBars": int(variant.reentry_cooldown_bars),
            "InpEntryTransitionOnly": _entry_transition_enabled(variant),
        }
        for source_split, runtime_split in (("validation", "validation_is"), ("oos", "oos")):
            split_token = "val" if runtime_split == "validation_is" else "oos"
            split_frame = common.loc[
                common["split"].astype(str).eq(source_split)
                & common["tier_label"].astype(str).eq(ctx.mt5.TIER_A)
            ]
            from_date, to_date = ctx.split_dates_from_frame(split_frame, source_split)
            tier_a_matrix = Path(str(feature_exports[f"{variant.variant_id}_tier_a_{runtime_split}"]["path"])).name
            tier_b_matrix = Path(str(feature_exports[f"{variant.variant_id}_tier_b_fallback_{runtime_split}"]["path"])).name
            base_kwargs = {
                "run_root": ctx.RUN_ROOT / variant.variant_id,
                "run_id": f"{ctx.PARENT_RUN_ID}_{variant_short}",
                "stage_number": 56,
                "exploration_label": ctx.EXPLORATION_LABEL,
                "split": runtime_split,
                "model_path": model_common,
                "model_id": f"{ctx.PARENT_RUN_ID}_{variant.variant_id}_context_et_firewall_signal_table",
                "model_backend": "ebm_table",
                "feature_count": 1,
                "feature_order_hash": feature_hash,
                "short_threshold": ctx.SHORT_THRESHOLD,
                "long_threshold": ctx.LONG_THRESHOLD,
                "min_margin": ctx.MIN_MARGIN,
                "invert_signal": False,
                "from_date": from_date,
                "to_date": to_date,
                "max_hold_bars": variant.max_hold_bars,
                "common_root": ctx.COMMON_ROOT,
                "close_on_flat_signal": False,
                "reverse_on_opposite_signal": True,
                "extra_set_values": variant_extra,
            }
            for role, role_token, tier, feature_path, primary_tier, record_prefix, fallback in (
                ("tier_a_only", "ta", ctx.mt5.TIER_A, f"{ctx.COMMON_ROOT}/features/{tier_a_matrix}", "tier_a", f"mt5_tier_a_only_{variant.variant_id}", False),
                ("tier_b_fallback_only", "tb", ctx.mt5.TIER_B, f"{ctx.COMMON_ROOT}/features/{tier_b_matrix}", "tier_b_fallback", f"mt5_tier_b_fallback_only_{variant.variant_id}", False),
                ("routed", "rt", ctx.mt5.TIER_AB, f"{ctx.COMMON_ROOT}/features/{tier_a_matrix}", "tier_a", f"mt5_routed_{variant.variant_id}", True),
            ):
                payload = ctx.attempt_payload(
                    **base_kwargs,
                    attempt_name=f"{variant_short}_{role_token}_{split_token}",
                    tier=tier,
                    feature_path=feature_path,
                    primary_active_tier=primary_tier,
                    attempt_role="routed_total" if role == "routed" else "tier_only_total",
                    record_view_prefix=record_prefix,
                    fallback_enabled=variant.routed_fallback_enabled if fallback else False,
                    fallback_model_path=model_common if fallback else None,
                    fallback_model_id=f"{ctx.PARENT_RUN_ID}_{variant.variant_id}_tier_b_context_et_firewall_signal_table" if fallback else None,
                    fallback_model_backend="ebm_table" if fallback else None,
                    fallback_feature_path=f"{ctx.COMMON_ROOT}/features/{tier_b_matrix}" if fallback else None,
                    fallback_feature_count=1 if fallback else None,
                    fallback_feature_order_hash=feature_hash if fallback else None,
                    fallback_short_threshold=ctx.SHORT_THRESHOLD if fallback else None,
                    fallback_long_threshold=ctx.LONG_THRESHOLD if fallback else None,
                    fallback_min_margin=ctx.MIN_MARGIN if fallback else None,
                    fallback_invert_signal=False if fallback else None,
                )
                payload["variant_id"] = variant.variant_id
                payload["composite_mode"] = variant.composite_mode
                payload["context_rule_count"] = len(variant.rules)
                payload["entry_transition_only"] = _entry_transition_enabled(variant)
                payload["firewall_enabled"] = _firewall_enabled(variant)
                attempts.append(payload)
    return attempts


def fmt(value: Any) -> str:
    return ctx.fmt(value)


def best_row(rows: Sequence[Mapping[str, Any]]) -> Mapping[str, Any] | None:
    return ctx.best_row(rows)


def write_report(rows: Sequence[Mapping[str, Any]], audit_rows: Sequence[Mapping[str, Any]], result: Mapping[str, Any]) -> None:
    best = best_row(rows) or {}
    lines = [
        "# Stage56 run50BQ Context ExtraTrees Firewall Transition(문맥 ExtraTrees 방화벽 전환)",
        "",
        f"- run_id(실행 ID): `{PARENT_RUN_ID}`",
        f"- packet_id(작업 묶음 ID): `{PACKET_ID}`",
        "- selected_research_baseline(선택 연구 기준선): `none`",
        f"- external_verification_status(외부 검증 상태): `{result.get('external_verification_status')}`",
        f"- claim_boundary(주장 경계): `{ctx.BOUNDARY}`",
        "",
        "Action(행동): run50BN v47(실행50BN v47)의 ET slot-fill(ExtraTrees 슬롯 채움) 중 validation/OOS(검증/표본외) 양쪽 손실인 slot6 short(6번 슬롯 숏)와 slot5 long(5번 슬롯 롱)을 막고, entry-transition-only(전환 진입) 실행을 실제 MT5(메타트레이더5)로 비교했다.",
        "Effect(효과): quality lift(품질 상승)가 same-move split re-entry(동일 이동 분할 재진입)까지 줄이는지 확인한다.",
        "",
        "## Best Read(최선 판독)",
        "",
        f"- best_variant(최선 변형): `{best.get('variant_id', 'none')}`",
        f"- validation/OOS trades/day(검증/표본외 일 거래): `{fmt(best.get('routed_validation_trades_per_day'))}` / `{fmt(best.get('routed_oos_trades_per_day'))}`",
        f"- validation/OOS PF(검증/표본외 수익 팩터): `{fmt(best.get('routed_validation_pf'))}` / `{fmt(best.get('routed_oos_pf'))}`",
        f"- validation/OOS net(검증/표본외 순손익): `{fmt(best.get('routed_validation_net'))}` / `{fmt(best.get('routed_oos_net'))}`",
        f"- failure_reasons(실패 이유): `{best.get('failure_reasons', '')}`",
        "",
        "| variant | transition | hold | val day | oos day | val PF | oos PF | val net | oos net | same val/oos | cooldown day val/oos | failures |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in rows:
        transition = "transition" in str(row.get("variant_id", ""))
        lines.append(
            "| {variant} | {transition} | {hold} | {vday} | {oday} | {vpf} | {opf} | {vnet} | {onet} | {samev}/{sameo} | {coolv}/{coolo} | {fail} |".format(
                variant=row.get("variant_id", ""),
                transition=transition,
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
    lines.extend(
        [
            "",
            "Judgment(판정): `in_progress_no_selected_research_baseline`.",
            "Effect(효과): run50BQ(실행50BQ)는 progress evidence(진행 근거)이고 Stage56(56단계)은 계속 open(열림)이다.",
        ]
    )
    ctx.write_md(REPORT_PATH, "\n".join(lines))


def append_progress(best: Mapping[str, Any]) -> None:
    existing = io_path(ctx.PROGRESS_LOG_PATH).read_text(encoding="utf-8-sig") if path_exists(ctx.PROGRESS_LOG_PATH) else ""
    entry = f"""

## {ctx.utc_now()} run50BQ Context ExtraTrees Firewall Transition(문맥 ExtraTrees 방화벽 전환)

- action(행동): run50BN v47(실행50BN v47)의 stable ET damage slots(안정 ET 손상 슬롯)를 막고 transition-only entry(전환 진입)를 실제 MT5 validation/OOS(검증/표본외)로 시험했다.
- effect(효과): quality lift(품질 상승)가 same-move split re-entry(동일 이동 분할 재진입)와 cost-stressed expectancy(비용 압박 기대값)를 동시에 고치는지 확인했다.
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
        f"  Stage56(56단계) `{ctx.STAGE_ID}`: run50BQ(실행50BQ) context ExtraTrees firewall transition(문맥 ExtraTrees 방화벽 전환) 완료; "
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
        "  next_action: evaluate_transition_failure_or_open_new_source_branch\n"
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

Stage56(56단계)은 unfinished optimization campaign(미완 최적화 캠페인)으로 계속 열려 있다. Effect(효과): run50BQ(실행50BQ)는 run50BN v47(실행50BN v47)의 stable ET damage firewall(안정 ET 손상 방화벽)과 transition-only entry(전환 진입)를 실제 MT5 validation/OOS(검증/표본외)로 비교한 근거다.

## Latest Evidence(최신 근거)

- latest_batch(최신 묶음): `{PARENT_RUN_ID}`
- best_variant(현재 최선 변형): `{best_id}`
- selected_research_baseline(선택 연구 기준선): `none`
- validation/OOS trades/day(검증/표본외 일 거래): `{fmt(best.get('routed_validation_trades_per_day'))}` / `{fmt(best.get('routed_oos_trades_per_day'))}`
- validation/OOS PF(검증/표본외 수익 팩터): `{fmt(best.get('routed_validation_pf'))}` / `{fmt(best.get('routed_oos_pf'))}`
- validation/OOS net(검증/표본외 순손익): `{fmt(best.get('routed_validation_net'))}` / `{fmt(best.get('routed_oos_net'))}`
- latest_failure(최신 실패): `{failures}`

## Current Bottleneck(현재 병목)

- run50BQ judgment(실행50BQ 판정): selected_research_baseline(선택 연구 기준선)은 `none`이다. Effect(효과): failure_reasons(실패 이유) `{failures}` 때문에 hard condition(강한 완료 조건)을 통과하지 못했다.
- next_hypothesis_branch(다음 가설 분기): `evaluate_transition_failure_or_open_new_source_branch`

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

## Latest Run50BQ Intermediate Evidence(최신 50BQ 중간 근거)

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
    ctx.build_attempts = build_attempts
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
