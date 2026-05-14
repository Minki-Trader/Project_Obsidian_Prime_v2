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
from stage_pipelines.stage56 import context_extratrees_agreement_branch as bn  # noqa: E402
from stage_pipelines.stage56 import context_timed_opportunity_source_branch as ctx  # noqa: E402


RUN_NUMBER = "run50BP"
PARENT_RUN_ID = "run50BP_stage56_extratrees_slot_lifecycle_v1"
PACKET_ID = "stage56_run50BP_extratrees_slot_lifecycle_v1"
EXPLORATION_LABEL = "stage56_BaseEngine__ExtraTreesSlotLifecycle"
REPORT_PATH = ctx.REVIEWS_ROOT / "run50BP_extratrees_slot_lifecycle.md"
RESULTS_CSV_PATH = ctx.REVIEWS_ROOT / "run50BP_summary.csv"
AUDIT_CSV_PATH = ctx.REVIEWS_ROOT / "run50BP_audit.csv"
SOURCE_SUMMARY_CSV_PATH = ctx.REVIEWS_ROOT / "run50BP_source_summary.csv"
PACKET_ROOT = Path("docs/agent_control/packets") / PACKET_ID
AGGREGATE_SUMMARY_PATH = PACKET_ROOT / "aggregate_summary.json"
RUN_ROOT = ctx.STAGE_ROOT / "02_runs" / RUN_NUMBER
COMMON_ROOT = f"Project_Obsidian_Prime_v2/stage56/{RUN_NUMBER}_extratrees_slot_lifecycle"
SIGNAL_COLUMN = "stage56_et40_slot_lifecycle_signal"
WORKSPACE_BLOCK_KEY = "stage56_run50bp_extratrees_slot_lifecycle:"
RUN50BH_SUMMARY = ctx.REVIEWS_ROOT / "run50BH_summary.csv"
RUN50BH_AUDIT = ctx.REVIEWS_ROOT / "run50BH_audit.csv"
RUN50BN_SUMMARY = ctx.REVIEWS_ROOT / "run50BN_summary.csv"
RUN50BO_SUMMARY = ctx.REVIEWS_ROOT / "run50BO_summary.csv"


DEFAULT_VARIANTS = (
    ctx.ContextTimedVariant(
        "v54_et40_slot20_first_h2c0_no_b",
        "et40_slot20_first",
        20,
        (),
        2,
        0,
        False,
        "Use the first non-flat run50BH ExtraTrees signal in each 20-minute cash-session slot.",
        "et40_slot_first",
    ),
    ctx.ContextTimedVariant(
        "v55_et40_slot25_first_h2c0_no_b",
        "et40_slot25_first",
        25,
        (),
        2,
        0,
        False,
        "Use the first non-flat run50BH ExtraTrees signal in each 25-minute cash-session slot.",
        "et40_slot_first",
    ),
    ctx.ContextTimedVariant(
        "v56_et40_slot30_first_h2c0_no_b",
        "et40_slot30_first",
        30,
        (),
        2,
        0,
        False,
        "Use the first non-flat run50BH ExtraTrees signal in each 30-minute cash-session slot.",
        "et40_slot_first",
    ),
    ctx.ContextTimedVariant(
        "v57_et40_slot25_prob035_h2c0_no_b",
        "et40_slot25_probability_floor",
        25,
        (),
        2,
        0,
        False,
        "Use the first run50BH ExtraTrees signal with decision probability >= 0.35 in each 25-minute slot.",
        "et40_slot_prob035",
    ),
    ctx.ContextTimedVariant(
        "v58_et40_slot30_prob035_h2c0_no_b",
        "et40_slot30_probability_floor",
        30,
        (),
        2,
        0,
        False,
        "Use the first run50BH ExtraTrees signal with decision probability >= 0.35 in each 30-minute slot.",
        "et40_slot_prob035",
    ),
    ctx.ContextTimedVariant(
        "v59_et40_slot25_first_h1c0_no_b",
        "et40_slot25_hold1",
        25,
        (),
        1,
        0,
        False,
        "Use 25-minute slot lifecycle with hold1 to test cooldown survival after shorter exposure.",
        "et40_slot_first",
    ),
)


def _probability_floor(mode: str) -> float:
    if mode == "et40_slot_prob035":
        return 0.35
    return 0.0


def build_variant_frame(common: pd.DataFrame, variant: ctx.ContextTimedVariant) -> pd.DataFrame:
    frame = common.copy()
    frame["timestamp"] = pd.to_datetime(frame["timestamp"], utc=True)
    predictions = bn.load_et40_predictions()
    frame = frame.merge(predictions, on=["timestamp", "split", "tier_label"], how="left")
    frame["et40_signal"] = pd.to_numeric(frame["et40_signal"], errors="coerce").fillna(0).astype("int8")
    frame["et40_decision_probability"] = pd.to_numeric(frame["et40_decision_probability"], errors="coerce").fillna(0.0)
    minutes = pd.to_numeric(frame["minutes_from_cash_open"], errors="coerce")
    timestamp = pd.to_datetime(frame["timestamp"], utc=True)
    frame["slot_width_minutes"] = int(variant.slot_width_minutes)
    frame["slot_index"] = np.floor(minutes / float(variant.slot_width_minutes))
    frame["slot_date"] = timestamp.dt.strftime("%Y-%m-%d")
    frame[SIGNAL_COLUMN] = np.zeros(len(frame), dtype="int8")
    signal_mask = (
        frame["et40_signal"].ne(0)
        & minutes.between(0, 389, inclusive="both")
        & frame["et40_decision_probability"].ge(_probability_floor(variant.composite_mode))
    )
    first_index = (
        frame.loc[signal_mask]
        .sort_values("timestamp")
        .groupby(["split", "slot_date", "tier_label", "slot_index"], sort=False)
        .head(1)
        .index
    )
    frame.loc[first_index, SIGNAL_COLUMN] = frame.loc[first_index, "et40_signal"].astype("int8")
    frame["variant_id"] = variant.variant_id
    frame["primary_source"] = "run50BH_et40h6_r001_a_extratrees"
    frame["secondary_source"] = "slot_lifecycle_spacing"
    frame["composite_mode"] = variant.composite_mode
    frame["context_rule_id"] = "et40_slot_first"
    frame["context_slot"] = frame["slot_index"]
    frame["context_slot_width_minutes"] = int(variant.slot_width_minutes)
    frame["entry_decision"] = frame[SIGNAL_COLUMN].map({-1: "short", 0: "flat", 1: "long"}).fillna("flat")
    return frame


def source_summary_rows(variant: ctx.ContextTimedVariant, frame: pd.DataFrame) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for split in ("train", "validation", "oos"):
        for tier in (ctx.mt5.TIER_A, ctx.mt5.TIER_B):
            view = frame.loc[frame["split"].astype(str).eq(split) & frame["tier_label"].astype(str).eq(tier)]
            signal = pd.to_numeric(view[SIGNAL_COLUMN], errors="coerce").fillna(0).astype("int8")
            et_signal = pd.to_numeric(view["et40_signal"], errors="coerce").fillna(0).astype("int8")
            rows.append(
                {
                    "variant_id": variant.variant_id,
                    "split": split,
                    "tier": tier,
                    "composite_mode": variant.composite_mode,
                    "slot_width_minutes": int(variant.slot_width_minutes),
                    "max_hold_bars": int(variant.max_hold_bars),
                    "rows": int(len(view)),
                    "et40_nonflat": int(et_signal.ne(0).sum()),
                    "slot_signal_nonflat": int(signal.ne(0).sum()),
                    "slot_signal_long": int(signal.eq(1).sum()),
                    "slot_signal_short": int(signal.eq(-1).sum()),
                    "probability_floor": _probability_floor(variant.composite_mode),
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
        ("run50BH_frontier_summary", RUN50BH_SUMMARY, "ExtraTrees dense quality source"),
        ("run50BH_frontier_audit", RUN50BH_AUDIT, "same-move failure memory for unrestricted ExtraTrees"),
        ("run50BN_slotfill_summary", RUN50BN_SUMMARY, "slot-fill density/PF/net frontier with same-move failure"),
        ("run50BO_cooldown_summary", RUN50BO_SUMMARY, "same-direction cooldown repair failure memory"),
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
        (SIGNAL_COLUMN,),
        path,
        metadata_columns=(
            "variant_id",
            "primary_source",
            "secondary_source",
            "composite_mode",
            "slot_width_minutes",
            "slot_index",
            "et40_signal",
            "et40_decision_label",
            "et40_decision_probability",
            "et40_decision_margin",
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
        "# Stage56 run50BP ExtraTrees Slot Lifecycle(ExtraTrees 슬롯 생명주기)",
        "",
        f"- run_id(실행 ID): `{PARENT_RUN_ID}`",
        f"- packet_id(작업 묶음 ID): `{PACKET_ID}`",
        "- selected_research_baseline(선택 연구 기준선): `none`",
        f"- external_verification_status(외부 검증 상태): `{result.get('external_verification_status')}`",
        f"- claim_boundary(주장 경계): `{ctx.BOUNDARY}`",
        "",
        "Action(행동): run50BH ExtraTrees(엑스트라트리스)에서 각 cash-session slot(정규장 슬롯)의 첫 non-flat(비중립) 신호만 MT5에 전달했다.",
        "Effect(효과): density(밀도)를 사후 쿨다운으로 깎지 않고 source construction(원천 구성) 단계에서 real opportunity spacing(실제 기회 간격)을 만든다.",
        "",
        "## Best Read(최선 판독)",
        "",
        f"- best_variant(최선 변형): `{best.get('variant_id', 'none')}`",
        f"- validation/OOS trades/day(검증/표본외 일 거래): `{fmt(best.get('routed_validation_trades_per_day'))}` / `{fmt(best.get('routed_oos_trades_per_day'))}`",
        f"- validation/OOS PF(검증/표본외 수익 팩터): `{fmt(best.get('routed_validation_pf'))}` / `{fmt(best.get('routed_oos_pf'))}`",
        f"- validation/OOS net(검증/표본외 순손익): `{fmt(best.get('routed_validation_net'))}` / `{fmt(best.get('routed_oos_net'))}`",
        f"- failure_reasons(실패 이유): `{best.get('failure_reasons', '')}`",
        "",
        "| variant | slot | hold | val day | oos day | val PF | oos PF | val net | oos net | same val/oos | cooldown day val/oos | failures |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in rows:
        lines.append(
            "| {variant} | {slot} | {hold} | {vday} | {oday} | {vpf} | {opf} | {vnet} | {onet} | {samev}/{sameo} | {coolv}/{coolo} | {fail} |".format(
                variant=row.get("variant_id", ""),
                slot=row.get("slot_width_minutes", ""),
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
    lines.extend(["", "Judgment(판정): `in_progress_no_selected_research_baseline`."])
    ctx.write_md(REPORT_PATH, "\n".join(lines))


def append_progress(best: Mapping[str, Any]) -> None:
    existing = io_path(ctx.PROGRESS_LOG_PATH).read_text(encoding="utf-8-sig") if path_exists(ctx.PROGRESS_LOG_PATH) else ""
    entry = f"""

## {ctx.utc_now()} run50BP ExtraTrees Slot Lifecycle(ExtraTrees 슬롯 생명주기)

- action(행동): run50BH ExtraTrees(엑스트라트리스)를 20/25/30-minute slot lifecycle(분 슬롯 생명주기)로 재구성해 actual MT5 validation/OOS(실제 MT5 검증/표본외)를 실행했다.
- effect(효과): same-move density(동일 이동 밀도)를 cooldown(쿨다운)이 아니라 source spacing(원천 간격)으로 줄일 수 있는지 확인했다.
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
        f"  Stage56(56단계) `{ctx.STAGE_ID}`: run50BP(실행50BP) ExtraTrees slot lifecycle(ExtraTrees 슬롯 생명주기) 완료; "
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
        "  next_action: evaluate_slot_lifecycle_failure_or_open_new_model_branch\n"
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

Stage56(56단계)은 unfinished optimization campaign(미완 최적화 캠페인)으로 계속 열려 있다. Effect(효과): run50BP(실행50BP)는 ExtraTrees(엑스트라트리스)를 시간 슬롯 생명주기(time-slot lifecycle, 시간 슬롯 생명주기) 원천으로 재구성한 MT5 validation/OOS(검증/표본외) 근거다.

## Latest Evidence(최신 근거)

- latest_batch(최신 묶음): `{PARENT_RUN_ID}`
- best_variant(현재 최선 변형): `{best_id}`
- selected_research_baseline(선택 연구 기준선): `none`
- validation/OOS trades/day(검증/표본외 일 거래): `{val_day}` / `{oos_day}`
- validation/OOS PF(검증/표본외 수익 팩터): `{val_pf}` / `{oos_pf}`
- validation/OOS net(검증/표본외 순손익): `{val_net}` / `{oos_net}`
- latest_failure(최신 실패): `{failures}`

## Current Bottleneck(현재 병목)

- run50BP judgment(실행50BP 판정): selected_research_baseline(선택 연구 기준선)은 `none`이다. Effect(효과): failure_reasons(실패 이유) `{failures}` 때문에 hard condition(강한 완료 조건)을 통과하지 못했다.
- next_hypothesis_branch(다음 가설 분기): `evaluate_slot_lifecycle_failure_or_open_new_model_branch`

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

## Latest Run50BP Intermediate Evidence(최신 50BP 중간 근거)

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
