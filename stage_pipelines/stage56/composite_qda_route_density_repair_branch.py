from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.control_plane.ledger import (  # noqa: E402
    ALPHA_LEDGER_COLUMNS,
    RUN_REGISTRY_COLUMNS,
    ledger_pairs,
    path_exists,
    sha256_file_lf_normalized,
    upsert_csv_rows,
)
from stage_pipelines.stage56 import composite_route_after_qda_batch as batch  # noqa: E402


RUN_NUMBER = "run50AU"
PARENT_RUN_ID = "run50AU_stage56_composite_qda_route_density_repair_v1"
PACKET_ID = "stage56_run50AU_composite_qda_route_density_repair_v1"
EXPLORATION_LABEL = "stage56_BaseEngine__CompositeQdaRouteDensityRepair"
RUN_ROOT = batch.STAGE_ROOT / "02_runs" / RUN_NUMBER
REPORT_PATH = batch.REVIEWS_ROOT / "run50AU_composite_qda_route_density_repair.md"
RESULTS_CSV_PATH = batch.REVIEWS_ROOT / "run50AU_summary.csv"
AUDIT_CSV_PATH = batch.REVIEWS_ROOT / "run50AU_audit.csv"
AGGREGATE_SUMMARY_PATH = Path("docs/agent_control/packets") / PACKET_ID / "aggregate_summary.json"
ARTIFACT_COLUMNS = (
    "artifact_id",
    "artifact_type",
    "path",
    "sha256",
    "stage_id",
    "run_id",
    "created_at_utc",
    "notes",
)


@dataclass(frozen=True)
class RouteRepairVariant:
    variant_id: str
    group: str
    secondary_variant_id: str
    secondary_source_run_id: str
    secondary_source_variant_id: str
    secondary_source_axis: str
    route_mode: str
    use_on_primary_flat: bool
    use_on_low_confidence: bool
    primary_low_confidence_max: float
    secondary_short_threshold: float
    secondary_long_threshold: float
    secondary_min_margin: float
    primary_max_hold_bars: int
    primary_reentry_cooldown_bars: int
    entry_transition_only: bool
    entry_transition_rearm_min_confidence_delta: float
    notes: str

    @property
    def run_id(self) -> str:
        return f"{RUN_NUMBER}_{self.variant_id}_composite_route_density_repair_v1"

    @property
    def secondary_root(self) -> Path:
        return batch.STAGE_ROOT / "02_runs/run50AI" / self.secondary_variant_id


def _variant(
    variant_id: str,
    group: str,
    *,
    secondary_threshold: float,
    hold_bars: int = 8,
    cooldown_bars: int = 0,
    rearm_delta: float = 0.030,
    notes: str,
) -> RouteRepairVariant:
    return RouteRepairVariant(
        variant_id=variant_id,
        group=group,
        secondary_variant_id="qda_q85_aonly_bdisabled",
        secondary_source_run_id="run09O_qda_reg015_q85_coverage_followup_v1",
        secondary_source_variant_id="v25_reg015_q85",
        secondary_source_axis="stage16_qda_coverage_q85_threshold_repair",
        route_mode=(
            "primary_flat_secondary_qda_threshold_repair"
            f"_s{int(round(secondary_threshold * 1000)):03d}"
            f"_h{hold_bars}_c{cooldown_bars}_r{int(round(rearm_delta * 1000)):03d}"
        ),
        use_on_primary_flat=True,
        use_on_low_confidence=False,
        primary_low_confidence_max=0.0,
        secondary_short_threshold=secondary_threshold,
        secondary_long_threshold=secondary_threshold,
        secondary_min_margin=0.0,
        primary_max_hold_bars=hold_bars,
        primary_reentry_cooldown_bars=cooldown_bars,
        entry_transition_only=True,
        entry_transition_rearm_min_confidence_delta=rearm_delta,
        notes=notes,
    )


DEFAULT_VARIANTS: tuple[RouteRepairVariant, ...] = (
    _variant(
        "qda85_s850_flat_trans_r030_h8",
        "qda85_flat_transition_threshold_repair",
        secondary_threshold=0.850,
        notes="QDA q85 secondary threshold 0.850 under primary-flat/no-position with transition re-entry guard.",
    ),
    _variant(
        "qda85_s800_flat_trans_r030_h8",
        "qda85_flat_transition_threshold_repair",
        secondary_threshold=0.800,
        notes="QDA q85 secondary threshold 0.800 tests whether lower threshold creates real OOS density without low-confidence handoff damage.",
    ),
    _variant(
        "qda85_s750_flat_trans_r030_h8",
        "qda85_flat_transition_threshold_repair",
        secondary_threshold=0.750,
        notes="Aggressive QDA q85 threshold 0.750; boundary test for density cliff and cost-stress damage.",
    ),
    _variant(
        "qda85_s850_flat_trans_r030_h6",
        "qda85_flat_transition_hold_compression",
        secondary_threshold=0.850,
        hold_bars=6,
        notes="Hold-6 lifecycle compression with QDA 0.850 to test whether density can recover without fixed cooldown.",
    ),
    _variant(
        "qda85_s800_flat_trans_r030_h6",
        "qda85_flat_transition_hold_compression",
        secondary_threshold=0.800,
        hold_bars=6,
        notes="Hold-6 with QDA 0.800; broad density-pressure branch.",
    ),
    _variant(
        "qda85_s800_flat_trans_r060_h8",
        "qda85_flat_stricter_rearm_guard",
        secondary_threshold=0.800,
        rearm_delta=0.060,
        notes="Stricter rearm guard tests whether QDA threshold repair is mainly same-move split trading.",
    ),
)


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _rule_with_primary_overrides(rule: Mapping[str, Any], variant: RouteRepairVariant) -> dict[str, Any]:
    updated = dict(rule)
    updated["max_hold_bars"] = int(variant.primary_max_hold_bars)
    updated["reentry_cooldown_bars"] = int(variant.primary_reentry_cooldown_bars)
    return updated


def _rule_with_secondary_overrides(rule: Mapping[str, Any], variant: RouteRepairVariant) -> dict[str, Any]:
    updated = dict(rule)
    updated["short_threshold"] = float(variant.secondary_short_threshold)
    updated["long_threshold"] = float(variant.secondary_long_threshold)
    updated["min_margin"] = float(variant.secondary_min_margin)
    updated["max_hold_bars"] = int(variant.primary_max_hold_bars)
    updated["reentry_cooldown_bars"] = int(variant.primary_reentry_cooldown_bars)
    return updated


def _transition_set_values(variant: RouteRepairVariant) -> dict[str, Any]:
    return {
        "InpEntryTransitionOnly": bool(variant.entry_transition_only),
        "InpEntryTransitionRearmMinConfidenceDelta": float(variant.entry_transition_rearm_min_confidence_delta),
    }


def _make_attempts(
    variant: RouteRepairVariant,
    artifacts: Mapping[str, Any],
) -> tuple[list[dict[str, Any]], dict[str, Any], dict[str, Any], dict[str, Any]]:
    primary_rule = _rule_with_primary_overrides(batch._source_rule_values(batch.NF200S25B_ROOT), variant)
    secondary_rule = _rule_with_secondary_overrides(batch._source_rule_values(variant.secondary_root), variant)
    route_coverage = batch._route_coverage(variant, artifacts)
    attempts: list[dict[str, Any]] = []
    run_root = RUN_ROOT / variant.variant_id

    for split in ("validation_is", "oos"):
        from_date, to_date = batch._source_split_dates(batch.NF200S25B_ROOT, split)
        feature = artifacts["features"][split]
        split_magic = 0 if split == "validation_is" else 1
        common_root = str(artifacts["common_root"])
        base_kwargs = {
            "run_root": run_root,
            "run_id": variant.run_id,
            "stage_number": batch.STAGE_NUMBER,
            "exploration_label": f"{EXPLORATION_LABEL}__{variant.variant_id}",
            "split": split,
            "from_date": from_date,
            "to_date": to_date,
            "common_root": common_root,
            "close_on_flat_signal": bool(primary_rule["close_on_flat_signal"]),
            "reverse_on_opposite_signal": bool(primary_rule["reverse_on_opposite_signal"]),
            "close_only_on_opposite_signal": bool(primary_rule["close_only_on_opposite_signal"]),
        }
        primary_extra = {
            "InpMagic": 1006000 + split_magic,
            "InpReentryCooldownBars": int(primary_rule["reentry_cooldown_bars"]),
            "InpSideFilterEnabled": bool(primary_rule["side_filter_enabled"]),
            "InpSideFilterFeatureIndex": int(primary_rule["side_filter_feature_index"]),
            "InpFallbackSideFilterFeatureIndex": -1,
            "InpBlockShortFeatureRange": bool(primary_rule["block_short_feature_range"]),
            "InpBlockShortFeatureMin": float(primary_rule["block_short_feature_min"]),
            "InpBlockShortFeatureMax": float(primary_rule["block_short_feature_max"]),
            "InpBlockLongFeatureRange": bool(primary_rule["block_long_feature_range"]),
            "InpBlockLongFeatureMin": float(primary_rule["block_long_feature_min"]),
            "InpBlockLongFeatureMax": float(primary_rule["block_long_feature_max"]),
            **_transition_set_values(variant),
        }
        secondary_extra = {
            "InpMagic": 1006010 + split_magic,
            "InpReentryCooldownBars": int(primary_rule["reentry_cooldown_bars"]),
            "InpSideFilterEnabled": False,
            "InpSideFilterFeatureIndex": -1,
            "InpFallbackSideFilterFeatureIndex": -1,
            **_transition_set_values(variant),
        }
        routed_extra = {
            "InpMagic": 1006020 + split_magic,
            "InpReentryCooldownBars": int(primary_rule["reentry_cooldown_bars"]),
            "InpSideFilterEnabled": bool(primary_rule["side_filter_enabled"]),
            "InpSideFilterFeatureIndex": int(primary_rule["side_filter_feature_index"]),
            "InpFallbackSideFilterFeatureIndex": -1,
            "InpBlockShortFeatureRange": bool(primary_rule["block_short_feature_range"]),
            "InpBlockShortFeatureMin": float(primary_rule["block_short_feature_min"]),
            "InpBlockShortFeatureMax": float(primary_rule["block_short_feature_max"]),
            "InpBlockLongFeatureRange": bool(primary_rule["block_long_feature_range"]),
            "InpBlockLongFeatureMin": float(primary_rule["block_long_feature_min"]),
            "InpBlockLongFeatureMax": float(primary_rule["block_long_feature_max"]),
            "InpFallbackUseOnPrimaryFlat": bool(variant.use_on_primary_flat),
            "InpFallbackPrimaryFlatRequiresNoPosition": True,
            "InpFallbackUseOnPrimaryLowConfidence": bool(variant.use_on_low_confidence),
            "InpFallbackPrimaryMaxConfidence": float(variant.primary_low_confidence_max),
            "InpFallbackLowConfidenceRequiresNoPosition": True,
            **_transition_set_values(variant),
        }

        attempts.append(
            batch.attempt_payload(
                **base_kwargs,
                attempt_name=f"tier_a_only_{split}",
                tier=batch.mt5.TIER_A,
                model_path=str(artifacts["models"]["primary"]["common_path"]),
                model_id=f"{variant.run_id}_nf200s25b_primary",
                model_backend="onnx",
                feature_path=str(feature["primary_common_path"]),
                feature_count=int(primary_rule["feature_count"]),
                feature_order_hash=str(primary_rule["feature_order_hash"]),
                short_threshold=float(primary_rule["short_threshold"]),
                long_threshold=float(primary_rule["long_threshold"]),
                min_margin=float(primary_rule["min_margin"]),
                invert_signal=bool(primary_rule["invert_signal"]),
                primary_active_tier="tier_a",
                attempt_role="tier_only_total",
                record_view_prefix="mt5_tier_a_only",
                max_hold_bars=int(primary_rule["max_hold_bars"]),
                extra_set_values=primary_extra,
            )
        )
        attempts.append(
            batch.attempt_payload(
                **base_kwargs,
                attempt_name=f"secondary_only_{split}",
                tier=batch.mt5.TIER_B,
                model_path=str(artifacts["models"]["secondary"]["common_path"]),
                model_id=f"{variant.run_id}_{variant.secondary_variant_id}_secondary",
                model_backend="onnx",
                feature_path=str(feature["secondary_common_path"]),
                feature_count=int(secondary_rule["feature_count"]),
                feature_order_hash=str(secondary_rule["feature_order_hash"]),
                short_threshold=float(secondary_rule["short_threshold"]),
                long_threshold=float(secondary_rule["long_threshold"]),
                min_margin=float(secondary_rule["min_margin"]),
                invert_signal=bool(secondary_rule["invert_signal"]),
                primary_active_tier="tier_b_fallback",
                attempt_role="secondary_coverage_only_total",
                record_view_prefix="mt5_tier_b_fallback_only",
                max_hold_bars=int(primary_rule["max_hold_bars"]),
                extra_set_values=secondary_extra,
            )
        )
        routed = batch.attempt_payload(
            **base_kwargs,
            attempt_name=f"routed_{split}",
            tier=batch.mt5.TIER_AB,
            model_path=str(artifacts["models"]["primary"]["common_path"]),
            model_id=f"{variant.run_id}_nf200s25b_primary",
            model_backend="onnx",
            feature_path=str(feature["primary_common_path"]),
            feature_count=int(primary_rule["feature_count"]),
            feature_order_hash=str(primary_rule["feature_order_hash"]),
            short_threshold=float(primary_rule["short_threshold"]),
            long_threshold=float(primary_rule["long_threshold"]),
            min_margin=float(primary_rule["min_margin"]),
            invert_signal=bool(primary_rule["invert_signal"]),
            primary_active_tier="tier_a",
            attempt_role="routed_total",
            record_view_prefix="mt5_routed_total",
            max_hold_bars=int(primary_rule["max_hold_bars"]),
            fallback_enabled=True,
            fallback_model_path=str(artifacts["models"]["secondary"]["common_path"]),
            fallback_model_id=f"{variant.run_id}_{variant.secondary_variant_id}_secondary",
            fallback_model_backend="onnx",
            fallback_feature_path=str(feature["secondary_common_path"]),
            fallback_feature_count=int(secondary_rule["feature_count"]),
            fallback_feature_order_hash=str(secondary_rule["feature_order_hash"]),
            fallback_short_threshold=float(secondary_rule["short_threshold"]),
            fallback_long_threshold=float(secondary_rule["long_threshold"]),
            fallback_min_margin=float(secondary_rule["min_margin"]),
            fallback_invert_signal=bool(secondary_rule["invert_signal"]),
            extra_set_values=routed_extra,
        )
        routed["routing_mode"] = batch.mt5.ROUTING_MODE_A_B_FALLBACK
        routed["routing_detail"] = f"nf200s25b_primary_qda_secondary_density_repair:{variant.route_mode}"
        attempts.append(routed)

    for attempt in attempts:
        attempt.update(
            {
                "variant_id": variant.variant_id,
                "primary_reference_variant": "nf200s25b",
                "secondary_source_variant": variant.secondary_variant_id,
                "secondary_source_axis": variant.secondary_source_axis,
                "composite_route_mode": variant.route_mode,
                "partial_context_tier_b_status": "disabled",
            }
        )
    return attempts, route_coverage, primary_rule, secondary_rule


def _write_report(
    rows: Sequence[Mapping[str, Any]],
    audit_rows: Sequence[Mapping[str, Any]],
    final_read: Mapping[str, Any],
) -> None:
    best = final_read.get("best_variant") if isinstance(final_read.get("best_variant"), Mapping) else {}
    lines = [
        f"# {PARENT_RUN_ID}(Stage56 56단계 QDA 합성 라우트 밀도 수정)",
        "",
        f"- packet_id(작업 묶음 ID): `{PACKET_ID}`",
        "- stage_status(단계 상태): `active_in_progress(활성 진행 중)`",
        f"- selected_research_baseline(선택 연구 기준선): `{final_read.get('selected_research_baseline') or 'none'}`",
        "- boundary(주장 경계): `progress_checkpoint(진행 점검); no live_readiness(실거래 준비 아님); no runtime_authority(런타임 권위 아님)`",
        "",
        "## Hypothesis(가설)",
        "",
        "Action(행동): nf200s25b(비평탄 200 가중 로지스틱) primary(우선)를 유지하고 QDA(이차 판별 분석) secondary(보조)를 primary flat/no-position(우선 관망/무포지션) 구간에만 낮은 threshold(문턱값)로 붙였다.",
        "Effect(효과): 기존 low-confidence handoff(낮은 신뢰도 인계)가 primary(우선) 좋은 진입을 망가뜨렸는지 피하면서, OOS density(표본외 밀도)가 실제 추가 기회로 늘어나는지 본다.",
        "",
        "## Variant Results(변형 결과)",
        "",
        "| variant(변형) | mode(방식) | val/day(검증 일 거래) | OOS/day(표본외 일 거래) | val PF(검증 수익 팩터) | OOS PF(표본외 수익 팩터) | val net(검증 순손익) | OOS net(표본외 순손익) | judgment(판정) |",
        "|---|---|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in rows:
        lines.append(
            "| {variant} | {mode} | {vpd} | {opd} | {vpf} | {opf} | {vn} | {on} | `{judgment}` |".format(
                variant=row.get("variant_id", ""),
                mode=row.get("composite_route_mode", ""),
                vpd=row.get("routed_validation_trades_per_day", ""),
                opd=row.get("routed_oos_trades_per_day", ""),
                vpf=row.get("routed_validation_profit_factor", ""),
                opf=row.get("routed_oos_profit_factor", ""),
                vn=row.get("routed_validation_net_profit", ""),
                on=row.get("routed_oos_net_profit", ""),
                judgment=row.get("judgment", ""),
            )
        )
    lines.extend(
        [
            "",
            "## Same-Move Audit(동일 이동 감사)",
            "",
            "| variant(변형) | split(분할) | trades/day(일 거래) | cost exp(비용 압박 기대값) | same-move(동일 이동 비율) | 12bar density(12봉 후 밀도) | survives(생존) |",
            "|---|---|---:|---:|---:|---:|---|",
        ]
    )
    for row in audit_rows:
        if str(row.get("variant_id")) in {"d390h10_reference", "nf200s25b_reference"}:
            continue
        lines.append(
            "| {variant} | {split} | {day} | {cse} | {same} | {cool} | {survives} |".format(
                variant=row.get("variant_id", ""),
                split=row.get("split", ""),
                day=batch._format(row.get("trades_per_day")),
                cse=batch._format(row.get("cost_stressed_expectancy")),
                same=batch._format(row.get("same_move_reentry_ratio")),
                cool=batch._format(row.get("trades_per_day_after_cooldown")),
                survives=row.get("density_gain_survives_12bar_cooldown", ""),
            )
        )
    lines.extend(
        [
            "",
            "## Read(판독)",
            "",
            f"- best_variant(현재 최선 변형): `{best.get('variant_id') or 'none'}`",
            f"- selected_research_baseline(선택 연구 기준선): `{final_read.get('selected_research_baseline') or 'none'}`",
            f"- stage56_remains_open(56단계 계속 열림): `{bool(final_read.get('stage56_remains_open'))}`",
            f"- reason(이유): {final_read.get('reason')}",
            "- next_hypothesis_branch(다음 가설 가지): `evaluate_run50AU_then_pivot_or_repair`",
        ]
    )
    if final_read.get("best_variant_failed_checks"):
        lines.extend(["", "## Best Failed Checks(최선 변형 실패 조건)", ""])
        for check in final_read.get("best_variant_failed_checks", []):
            lines.append(f"- `{check.get('check')}`: {check.get('reason')}")
    batch._write_bom_text(REPORT_PATH, "\n".join(lines))


def _write_progress_log(
    rows: Sequence[Mapping[str, Any]],
    _audit_rows: Sequence[Mapping[str, Any]],
    final_read: Mapping[str, Any],
) -> None:
    best = final_read.get("best_variant") if isinstance(final_read.get("best_variant"), Mapping) else {}
    lines = [
        "# Stage56 Reopen Goal Progress Log(56단계 재개 목표 진행 기록)",
        "",
        "- packet_id(작업 묶음 ID): `stage56_reopen_goal_v1`",
        "- stage_status(단계 상태): `active_in_progress(활성 진행 중)`",
        f"- latest_batch(최신 묶음): `{PARENT_RUN_ID}`",
        f"- selected_research_baseline(선택 연구 기준선): `{final_read.get('selected_research_baseline') or 'none'}`",
        "- terminal_condition(종료 조건): useful BaselineAdapter(유용한 기준선 어댑터) hard condition(강한 완료 조건) satisfied(충족)",
        "",
        "## Current Read(현재 판독)",
        "",
        f"- best_variant(현재 최선 변형): `{best.get('variant_id') or 'none'}`",
        f"- validation/OOS trades/day(검증/표본외 일 거래): `{best.get('routed_validation_trades_per_day') or ''}` / `{best.get('routed_oos_trades_per_day') or ''}`",
        f"- validation/OOS PF(검증/표본외 수익 팩터): `{best.get('routed_validation_profit_factor') or ''}` / `{best.get('routed_oos_profit_factor') or ''}`",
        f"- validation/OOS net(검증/표본외 순손익): `{best.get('routed_validation_net_profit') or ''}` / `{best.get('routed_oos_net_profit') or ''}`",
        "- action(행동): QDA(이차 판별 분석) secondary(보조) threshold(문턱값)와 transition re-entry(전환 재진입)를 실제 MT5(메타트레이더5) validation/OOS(검증/표본외)로 시험했다.",
        "- effect(효과): ExtraTrees(엑스트라트리스) branch(분기) 실패 뒤, OOS density(표본외 밀도)가 진짜 추가 기회인지 route source(라우트 원천) 축에서 다시 확인한다.",
        "",
        "## Attempted Variants(시도 변형)",
        "",
        "| variant(변형) | val/day(검증 일 거래) | OOS/day(표본외 일 거래) | val PF(검증 PF) | OOS PF(표본외 PF) | val net(검증 순손익) | OOS net(표본외 순손익) |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for row in rows:
        lines.append(
            "| {variant} | {vpd} | {opd} | {vpf} | {opf} | {vn} | {on} |".format(
                variant=row.get("variant_id", ""),
                vpd=row.get("routed_validation_trades_per_day", ""),
                opd=row.get("routed_oos_trades_per_day", ""),
                vpf=row.get("routed_validation_profit_factor", ""),
                opf=row.get("routed_oos_profit_factor", ""),
                vn=row.get("routed_validation_net_profit", ""),
                on=row.get("routed_oos_net_profit", ""),
            )
        )
    batch._write_bom_text(batch.PROGRESS_LOG_PATH, "\n".join(lines))


def _write_selection_status(final_read: Mapping[str, Any]) -> None:
    best = final_read.get("best_variant") if isinstance(final_read.get("best_variant"), Mapping) else {}
    text = f"""# Stage56 Selection Status(56단계 선택 상태)

- stage_status(단계 상태): `active_in_progress`
- latest_run_id(최신 실행 ID): `{PARENT_RUN_ID}`
- current run(현재 실행): `{PARENT_RUN_ID}`
- current_judgment(현재 판정): `{final_read.get('stage56_judgment')}`
- selected_research_baseline(선택 연구 기준선): `{final_read.get('selected_research_baseline') or 'none'}`
- prior_stronger_candidate_intermediate(이전 강화 후보 중간 근거): `d390h10_logreg_deep_repair_suite`
- latest_batch_best_variant_intermediate(최신 묶음 최선 변형 중간 근거): `{best.get('variant_id') or 'none'}`

## Latest Run50AU Intermediate Evidence(최신 50AU 중간 근거)

- packet(묶음): `{PACKET_ID}`
- report(보고서): `{REPORT_PATH.as_posix()}`
- summary_csv(요약 CSV): `{RESULTS_CSV_PATH.as_posix()}`
- audit_csv(감사 CSV): `{AUDIT_CSV_PATH.as_posix()}`
- aggregate_summary(합산 요약): `{AGGREGATE_SUMMARY_PATH.as_posix()}`

Run50AU(실행50AU)는 QDA composite route density repair(QDA 합성 라우트 밀도 수정) 묶음이다. Effect(효과): selected_research_baseline(선택 연구 기준선)이 없으면 Stage56(56단계)은 계속 open(열림)이다.
"""
    batch._write_bom_text(batch.SELECTION_STATUS_PATH, text)


def _write_current_working_state(final_read: Mapping[str, Any]) -> None:
    best = final_read.get("best_variant") if isinstance(final_read.get("best_variant"), Mapping) else {}
    text = f"""# Current Working State(현재 작업 상태)

- current_packet(현재 작업 묶음): `{PACKET_ID}`
- current run(현재 실행): `{PARENT_RUN_ID}`
- active stage(활성 단계): `{batch.STAGE_ID}`
- selected_research_baseline(선택 연구 기준선): `{final_read.get('selected_research_baseline') or 'none'}`
- status(상태): active_in_progress(활성 진행 중)
- terminal_condition(종료 조건): useful BaselineAdapter(유용한 기준선 어댑터) hard condition(강한 완료 조건) satisfied(충족)

Stage56(56단계)은 unfinished optimization campaign(미완 최적화 캠페인)으로 계속 열려 있다. Effect(효과): run50AU(실행50AU)는 QDA composite route density repair(QDA 합성 라우트 밀도 수정)를 실제 MT5 validation/OOS(검증/표본외)로 확인하는 중간 근거다.

## Latest Evidence(최신 근거)

- latest_batch(최신 묶음): `{PARENT_RUN_ID}`
- best_variant(현재 최선 변형): `{best.get('variant_id') or 'none'}`
- selected_research_baseline(선택 연구 기준선): `{final_read.get('selected_research_baseline') or 'none'}`
- validation/OOS trades/day(검증/표본외 일 거래): `{best.get('routed_validation_trades_per_day') or ''}` / `{best.get('routed_oos_trades_per_day') or ''}`
- validation/OOS PF(검증/표본외 수익 팩터): `{best.get('routed_validation_profit_factor') or ''}` / `{best.get('routed_oos_profit_factor') or ''}`
- validation/OOS net(검증/표본외 순손익): `{best.get('routed_validation_net_profit') or ''}` / `{best.get('routed_oos_net_profit') or ''}`

Forbidden claims(금지 주장): live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(운영 기준선), reviewed_closed(검토 종료).
"""
    batch._write_bom_text(batch.CURRENT_WORKING_STATE_PATH, text)


def _update_workspace_state(final_read: Mapping[str, Any]) -> None:
    path = batch._project_path(batch.WORKSPACE_STATE_PATH)
    text = path.read_text(encoding="utf-8-sig") if path.exists() else ""
    lines = [line for line in text.splitlines() if not line.startswith("current_run_id:")]
    lines.insert(0, f"current_run_id: {PARENT_RUN_ID}")
    text = "\n".join(lines)
    marker = "current_focus:\n"
    focus = (
        "current_focus:\n"
        f"- Stage56(56단계) `{batch.STAGE_ID}`: run50AU(실행50AU) QDA composite route density repair(QDA 합성 라우트 밀도 수정) 완료; "
        f"selected_research_baseline(선택 연구 기준선)은 `{final_read.get('selected_research_baseline') or 'none'}`이다. "
        "Effect(효과): QDA threshold(문턱값)와 transition re-entry(전환 재진입)가 OOS density(표본외 밀도)를 실제 기회로 살리는지 기록한다.\n"
    )
    if marker in text:
        before, _sep, after = text.partition(marker)
        tail_lines = [line for line in after.splitlines() if not line.startswith("- Stage56(")]
        text = before + focus + "\n".join(tail_lines).rstrip() + "\n"
    else:
        text = text.rstrip() + "\n" + focus
    path.write_text(text, encoding="utf-8-sig")


def _ledger_parent_row(rows: Sequence[Mapping[str, Any]], final_read: Mapping[str, Any]) -> dict[str, Any]:
    best = final_read.get("best_variant") if isinstance(final_read.get("best_variant"), Mapping) else {}
    completed_count = sum(1 for row in rows if row.get("external_verification_status") == "completed")
    return {
        "ledger_row_id": f"{PARENT_RUN_ID}__parent_review",
        "stage_id": batch.STAGE_ID,
        "run_id": PARENT_RUN_ID,
        "subrun_id": "parent_review",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "stage56_composite_qda_route_density_repair_parent_review",
        "tier_scope": "Tier A primary; QDA secondary; partial-context Tier B disabled",
        "kpi_scope": "stage56_selected_research_baseline_search",
        "scoreboard_lane": "runtime_probe",
        "status": "completed" if completed_count else "blocked",
        "judgment": str(final_read.get("stage56_judgment")),
        "path": REPORT_PATH.as_posix(),
        "primary_kpi": ledger_pairs(
            (
                ("selected_research_baseline", final_read.get("selected_research_baseline") or "none"),
                ("best_variant", best.get("variant_id")),
                ("routed_validation_trades_per_day", best.get("routed_validation_trades_per_day")),
                ("routed_oos_trades_per_day", best.get("routed_oos_trades_per_day")),
                ("routed_validation_pf", best.get("routed_validation_profit_factor")),
                ("routed_oos_pf", best.get("routed_oos_profit_factor")),
                ("routed_validation_net", best.get("routed_validation_net_profit")),
                ("routed_oos_net", best.get("routed_oos_net_profit")),
            )
        ),
        "guardrail_kpi": ledger_pairs(
            (
                ("valid_new_actual_mt5_routed_variants", len(rows)),
                ("terminal_condition", "useful_baselineadapter_hard_condition_only"),
                ("stage56_remains_open", bool(final_read.get("stage56_remains_open"))),
                ("partial_context_tier_b_disabled", True),
                ("secondary_route_source", "qda_q85_threshold_repair"),
            )
        ),
        "external_verification_status": "completed" if completed_count else "blocked",
        "notes": "bounded_composite_qda_route_density_repair_no_closeout_no_operating_claim",
    }


def _write_ledgers(rows: Sequence[Mapping[str, Any]], final_read: Mapping[str, Any]) -> dict[str, Any]:
    parent_row = _ledger_parent_row(rows, final_read)
    stage_payload = upsert_csv_rows(batch.STAGE_RUN_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, [parent_row], key="ledger_row_id")
    project_payload = upsert_csv_rows(batch.PROJECT_ALPHA_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, [parent_row], key="ledger_row_id")
    registry_payload = upsert_csv_rows(
        batch.RUN_REGISTRY_PATH,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": PARENT_RUN_ID,
                "stage_id": batch.STAGE_ID,
                "lane": "stage56_composite_qda_route_density_repair",
                "status": parent_row["status"],
                "judgment": str(final_read.get("stage56_judgment")),
                "path": REPORT_PATH.as_posix(),
                "notes": ledger_pairs(
                    (
                        ("valid_new_actual_mt5_routed_variants", len(rows)),
                        ("selected_research_baseline", final_read.get("selected_research_baseline") or "none"),
                        ("stage56_remains_open", bool(final_read.get("stage56_remains_open"))),
                        ("boundary", "bounded_composite_qda_route_density_repair_no_closeout_no_operating_claim"),
                    )
                ),
            }
        ],
        key="run_id",
    )
    return {
        "stage_run_ledger": stage_payload,
        "project_alpha_run_ledger": project_payload,
        "run_registry": registry_payload,
    }


def _write_aggregate_summary(
    results: Sequence[Mapping[str, Any]],
    rows: Sequence[Mapping[str, Any]],
    audit_rows: Sequence[Mapping[str, Any]],
    final_read: Mapping[str, Any],
    ledger_payload: Mapping[str, Any],
) -> None:
    payload = {
        "packet_id": PACKET_ID,
        "stage_id": batch.STAGE_ID,
        "run_id": PARENT_RUN_ID,
        "created_at_utc": _utc_now(),
        "status": "completed" if any(row.get("external_verification_status") == "completed" for row in rows) else "blocked",
        "valid_new_actual_mt5_routed_variant_count": len(rows),
        "valid_new_actual_mt5_routed_variant_limit": 6,
        "selected_research_baseline": final_read.get("selected_research_baseline") or "none",
        "final_read": final_read,
        "variant_rows": [dict(row) for row in rows],
        "audit_rows": [dict(row) for row in audit_rows],
        "variant_payloads": [dict(result) for result in results],
        "source_context": {
            "primary_reference": "nf200s25b",
            "secondary_reference": "qda_q85_aonly_bdisabled",
            "prior_run50AJ_summary": "docs/agent_control/packets/stage56_run50AJ_composite_route_after_qda_v1/aggregate_summary.json",
            "stage56_status": "active_in_progress",
        },
        "artifacts": {
            "report_path": REPORT_PATH.as_posix(),
            "results_csv_path": RESULTS_CSV_PATH.as_posix(),
            "audit_csv_path": AUDIT_CSV_PATH.as_posix(),
            "progress_log_path": batch.PROGRESS_LOG_PATH.as_posix(),
            "selection_status_path": batch.SELECTION_STATUS_PATH.as_posix(),
            "workspace_state_path": batch.WORKSPACE_STATE_PATH.as_posix(),
            "current_working_state_path": batch.CURRENT_WORKING_STATE_PATH.as_posix(),
            "ledger_payload": dict(ledger_payload),
        },
        "artifact_hashes": {
            "report_sha256": sha256_file_lf_normalized(REPORT_PATH) if path_exists(REPORT_PATH) else None,
            "results_csv_sha256": sha256_file_lf_normalized(RESULTS_CSV_PATH) if path_exists(RESULTS_CSV_PATH) else None,
            "audit_csv_sha256": sha256_file_lf_normalized(AUDIT_CSV_PATH) if path_exists(AUDIT_CSV_PATH) else None,
            "progress_log_sha256": sha256_file_lf_normalized(batch.PROGRESS_LOG_PATH) if path_exists(batch.PROGRESS_LOG_PATH) else None,
            "selection_status_sha256": sha256_file_lf_normalized(batch.SELECTION_STATUS_PATH) if path_exists(batch.SELECTION_STATUS_PATH) else None,
            "current_working_state_sha256": sha256_file_lf_normalized(batch.CURRENT_WORKING_STATE_PATH) if path_exists(batch.CURRENT_WORKING_STATE_PATH) else None,
            "workspace_state_sha256": sha256_file_lf_normalized(batch.WORKSPACE_STATE_PATH) if path_exists(batch.WORKSPACE_STATE_PATH) else None,
        },
        "boundary": "research_baseline_selection_only_no_closeout_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference",
    }
    batch._write_json(AGGREGATE_SUMMARY_PATH, payload)


def _write_artifact_registry(final_read: Mapping[str, Any]) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    artifacts = (
        ("aggregate_summary", AGGREGATE_SUMMARY_PATH),
        ("review_packet", REPORT_PATH),
        ("summary_csv", RESULTS_CSV_PATH),
        ("audit_csv", AUDIT_CSV_PATH),
        ("progress_log", batch.PROGRESS_LOG_PATH),
        ("current_working_state", batch.CURRENT_WORKING_STATE_PATH),
        ("workspace_state", batch.WORKSPACE_STATE_PATH),
        ("selection_status", batch.SELECTION_STATUS_PATH),
        ("stage_run_ledger", batch.STAGE_RUN_LEDGER_PATH),
        ("project_alpha_run_ledger", batch.PROJECT_ALPHA_LEDGER_PATH),
        ("run_registry", batch.RUN_REGISTRY_PATH),
    )
    for role, path in artifacts:
        if not path_exists(path):
            continue
        rows.append(
            {
                "artifact_id": f"{PARENT_RUN_ID}__{role}",
                "artifact_type": role,
                "path": path.as_posix(),
                "sha256": sha256_file_lf_normalized(path),
                "stage_id": batch.STAGE_ID,
                "run_id": PARENT_RUN_ID,
                "created_at_utc": _utc_now(),
                "notes": ledger_pairs(
                    (
                        ("selected_research_baseline", final_read.get("selected_research_baseline") or "none"),
                        ("boundary", "stage56_run50AU_progress_checkpoint"),
                    )
                ),
            }
        )
    return upsert_csv_rows(batch.ARTIFACT_REGISTRY_PATH, ARTIFACT_COLUMNS, rows, key="artifact_id")


def _select_variants(selected_ids: Iterable[str] | None, max_variants: int | None) -> tuple[RouteRepairVariant, ...]:
    selected = list(DEFAULT_VARIANTS)
    if selected_ids:
        wanted = {variant_id.strip() for variant_id in selected_ids if variant_id.strip()}
        selected = [variant for variant in selected if variant.variant_id in wanted]
        missing = sorted(wanted.difference(variant.variant_id for variant in selected))
        if missing:
            raise ValueError(f"Unknown variant ids: {missing}")
    if max_variants is not None:
        selected = selected[: int(max_variants)]
    if len(selected) > 6:
        raise ValueError("This bounded batch allows at most 6 valid actual MT5 routed variants.")
    return tuple(selected)


def _configure_batch() -> None:
    batch.RUN_NUMBER = RUN_NUMBER
    batch.PARENT_RUN_ID = PARENT_RUN_ID
    batch.PACKET_ID = PACKET_ID
    batch.EXPLORATION_LABEL = EXPLORATION_LABEL
    batch.RUN_ROOT = RUN_ROOT
    batch.REPORT_PATH = REPORT_PATH
    batch.RESULTS_CSV_PATH = RESULTS_CSV_PATH
    batch.AUDIT_CSV_PATH = AUDIT_CSV_PATH
    batch.AGGREGATE_SUMMARY_PATH = AGGREGATE_SUMMARY_PATH
    batch.DEFAULT_VARIANTS = DEFAULT_VARIANTS  # type: ignore[assignment]
    batch._make_attempts = _make_attempts  # type: ignore[assignment]


def main(argv: list[str] | None = None) -> int:
    _configure_batch()
    args = batch.parse_args(argv)
    variants = _select_variants(batch._split_values(args.variant_id), args.max_variants)
    results: list[dict[str, Any]] = []
    for variant in variants:
        try:
            result = batch._run_variant(
                variant,  # type: ignore[arg-type]
                attempt_mt5=bool(args.attempt_mt5),
                common_files_root=Path(args.common_files_root),
                terminal_data_root=Path(args.terminal_data_root),
                tester_profile_root=Path(args.tester_profile_root),
                terminal_path=Path(args.terminal_path),
                metaeditor_path=Path(args.metaeditor_path),
                timeout_seconds=int(args.timeout_seconds),
                force=bool(args.force),
            )
        except Exception as exc:  # pragma: no cover
            error_path = RUN_ROOT / variant.variant_id / "error.json"
            batch._write_json(
                error_path,
                {
                    "variant_id": variant.variant_id,
                    "run_id": variant.run_id,
                    "error": str(exc),
                    "created_at_utc": _utc_now(),
                },
            )
            result = {
                "status": "error",
                "variant_id": variant.variant_id,
                "run_id": variant.run_id,
                "external_verification_status": "blocked",
                "error": str(exc),
                "error_path": error_path.as_posix(),
            }
            if not args.continue_on_error:
                results.append(result)
                break
        results.append(dict(result))

    rows = batch._summary_rows(results, variants)  # type: ignore[arg-type]
    market_data = batch.MarketData.load(batch.REPO_ROOT)
    reference_audits, reference_capture = batch._reference_capture_by_split(market_data, float(args.cost_stress_per_trade))
    audit_rows = reference_audits + batch._audit_rows(
        rows,
        market_data=market_data,
        cost_stress_per_trade=float(args.cost_stress_per_trade),
        reference_capture=reference_capture,
    )
    final_read = batch._selected_read(rows, audit_rows)
    batch._write_csv(RESULTS_CSV_PATH, rows, batch.SUMMARY_COLUMNS)
    batch._write_csv(AUDIT_CSV_PATH, audit_rows, batch.reopen.AUDIT_COLUMNS)
    _write_report(rows, audit_rows, final_read)
    _write_progress_log(rows, audit_rows, final_read)
    _write_selection_status(final_read)
    _write_current_working_state(final_read)
    _update_workspace_state(final_read)
    ledger_payload = _write_ledgers(rows, final_read)
    _write_aggregate_summary(results, rows, audit_rows, final_read, ledger_payload)
    artifact_payload = _write_artifact_registry(final_read)
    print(
        json.dumps(
            {
                "status": "ok",
                "run_id": PARENT_RUN_ID,
                "valid_new_actual_mt5_routed_variant_count": len(rows),
                "selected_research_baseline": final_read.get("selected_research_baseline") or "none",
                "final_read": final_read.get("stage56_judgment"),
                "stage56_remains_open": bool(final_read.get("stage56_remains_open")),
                "results_csv_path": RESULTS_CSV_PATH.as_posix(),
                "audit_csv_path": AUDIT_CSV_PATH.as_posix(),
                "aggregate_summary_path": AGGREGATE_SUMMARY_PATH.as_posix(),
                "artifact_registry": artifact_payload,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
