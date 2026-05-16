from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.control_plane.alpha_run_ledgers import build_mt5_alpha_ledger_rows  # noqa: E402
from foundation.control_plane.ledger import (  # noqa: E402
    ALPHA_LEDGER_COLUMNS,
    RUN_REGISTRY_COLUMNS,
    io_path,
    json_ready,
    ledger_pairs,
    path_exists,
    sha256_file_lf_normalized,
    upsert_csv_rows,
)
from foundation.control_plane.mt5_tier_balance_completion import (  # noqa: E402
    COMMON_FILES_ROOT_DEFAULT,
    METAEDITOR_PATH_DEFAULT,
    TERMINAL_DATA_ROOT_DEFAULT,
    TERMINAL_PATH_DEFAULT,
    TESTER_PROFILE_ROOT_DEFAULT,
    attempt_payload,
    parse_ini,
)
from foundation.mt5 import runtime_support as mt5  # noqa: E402
from stage_pipelines.stage56 import baseline_adapter_repair_batch as repair  # noqa: E402
from stage_pipelines.stage58 import risk_atr_integration as s58  # noqa: E402
from stage_pipelines.stage59d import source_lifecycle_or_demote as engine  # noqa: E402
from stage_pipelines.stage59y import new_model_branch_from_stage59x as checkpoint  # noqa: E402


STAGE56_ID = "56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection"
SOURCE_STAGE59AK_ID = "59AK_adapter_repair__bounded_followup_from_stage59aj"
STAGE59AL_ID = "59AL_adapter_repair__bounded_followup_from_stage59ak"
RUN_NUMBER = "run59AG"
RUN_ID = "run59AG_stage59al_bounded_followup_from_stage59ak_v1"
PACKET_ID = "stage59al_bounded_followup_from_stage59ak_v1"
PARENT_RUN_ID = "run59AF_stage59ak_bounded_followup_from_stage59aj_v1"
SOURCE_ADAPTER_ID = "s59ak_v48_thr58_sd2_h2_mr03_wideatr"
DEVELOPMENT_ANCHOR = "v64_v47_ctxgap14_refill_etfw_h2_no_b"
BACKUP_ANCHOR = "v60_v47_et_stable_damage_firewall_h2c0_no_b"
SOURCE_STAGE59AK_PUSHED_COMMIT = "0d034fa525a71911ecb538a24af106a2c9bdf209"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment"
)

STAGE_ROOT = Path("stages") / STAGE59AL_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
SELECTED_ROOT = STAGE_ROOT / "04_selected"
SPEC_ROOT = STAGE_ROOT / "00_spec"
INPUT_ROOT = STAGE_ROOT / "01_inputs"
PACKET_ROOT = Path("docs/agent_control/packets") / PACKET_ID
PARTIALS_ROOT = RUN_ROOT / "partials"

SOURCE_STAGE_ROOT = Path("stages") / STAGE56_ID
RUN50BO_ROOT = SOURCE_STAGE_ROOT / "02_runs/run50BO"
RUN50BO_MODEL = RUN50BO_ROOT / "models/stage56_context_timed_event_signal_discrete_score_table.csv"
RUN50BO_SUMMARY = SOURCE_STAGE_ROOT / "03_reviews/run50BO_summary.csv"
RUN50BO_AUDIT = SOURCE_STAGE_ROOT / "03_reviews/run50BO_audit.csv"
RUN50BO_SOURCE_SUMMARY = SOURCE_STAGE_ROOT / "03_reviews/run50BO_source_summary.csv"
SOURCE_STAGE59AK_DECISION = Path("stages") / SOURCE_STAGE59AK_ID / "03_reviews/stage59ak_decision.md"
SOURCE_STAGE59AK_REPORT = Path("stages") / SOURCE_STAGE59AK_ID / "03_reviews/bounded_followup_from_stage59aj_report.md"
SOURCE_STAGE59AK_SUMMARY = Path("stages") / SOURCE_STAGE59AK_ID / "03_reviews/bounded_followup_summary.csv"

RUN50BO_SIGNAL = "stage56_context_et_event_signal"
COMMON_ROOT = f"Project_Obsidian_Prime_v2/stage59al/{RUN_NUMBER}"
MIN_MARGIN = 0.0

REPORT_PATH = REVIEWS_ROOT / "bracket_followup_from_stage59ak_report.md"
SUMMARY_JSON_PATH = REVIEWS_ROOT / "bounded_followup_summary.json"
SUMMARY_CSV_PATH = REVIEWS_ROOT / "bounded_followup_summary.csv"
SEGMENT_KPI_PATH = REVIEWS_ROOT / "bounded_followup_segment_kpi_summary.csv"
EQUITY_AUDIT_PATH = REVIEWS_ROOT / "bounded_followup_equity_curve_audit.md"
RISK_ATR_TELEMETRY_PATH = REVIEWS_ROOT / "bounded_followup_risk_atr_telemetry.csv"
DECISION_PATH = REVIEWS_ROOT / "stage59al_decision.md"
AUDIT_CSV_PATH = REVIEWS_ROOT / "stage59al_trade_audit.csv"
STAGE_LEDGER_PATH = REVIEWS_ROOT / "stage_run_ledger.csv"
RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
PROJECT_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
ARTIFACT_REGISTRY_PATH = Path("docs/registers/artifact_registry.csv")
WORKSPACE_STATE_PATH = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE_PATH = Path("docs/context/current_working_state.md")
CHANGELOG_PATH = Path("docs/workspace/changelog.md")

STAGE59AL_VARIANTS = (
    repair.RepairVariant(
        adapter_id="s59al_v48_sl20_tp30_sd2_mr03",
        label="run50BO_v48_midcov_slotfill_sd2_h2_threshold55_risk3pct_atr20_30",
        atr_enabled=True,
        model_risk_enabled=True,
        fixed_lot=0.25,
        atr_stop_multiplier=2.0,
        atr_take_profit_multiplier=3.0,
        model_risk_max_pct=0.03,
        same_direction_reentry_cooldown_bars=2,
        short_threshold=0.55,
        long_threshold=0.55,
        reverse_on_opposite_signal=False,
        close_only_on_opposite_signal=True,
        max_hold_bars=2,
        notes="Stage59AL bounded bracket repair: Stage59AK v48 source with ATR 2.0 SL / 3.0 TP, same-direction cooldown2, and 3% model risk cap.",
    ),
    repair.RepairVariant(
        adapter_id="s59al_v48_sl20_tp40_sd2_mr03",
        label="run50BO_v48_midcov_slotfill_sd2_h2_threshold55_risk3pct_atr20_40",
        atr_enabled=True,
        model_risk_enabled=True,
        fixed_lot=0.25,
        atr_stop_multiplier=2.0,
        atr_take_profit_multiplier=4.0,
        model_risk_max_pct=0.03,
        same_direction_reentry_cooldown_bars=2,
        short_threshold=0.55,
        long_threshold=0.55,
        reverse_on_opposite_signal=False,
        close_only_on_opposite_signal=True,
        max_hold_bars=2,
        notes="Stage59AL bounded bracket repair: Stage59AK v48 source with ATR 2.0 SL / 4.0 TP, same-direction cooldown2, and 3% model risk cap.",
    ),
    repair.RepairVariant(
        adapter_id="s59al_v48_sl18_tp32_sd2_mr03",
        label="run50BO_v48_midcov_slotfill_sd2_h2_threshold55_risk3pct_atr18_32",
        atr_enabled=True,
        model_risk_enabled=True,
        fixed_lot=0.25,
        atr_stop_multiplier=1.8,
        atr_take_profit_multiplier=3.2,
        model_risk_max_pct=0.03,
        same_direction_reentry_cooldown_bars=2,
        short_threshold=0.55,
        long_threshold=0.55,
        reverse_on_opposite_signal=False,
        close_only_on_opposite_signal=True,
        max_hold_bars=2,
        notes="Stage59AL bounded bracket repair: Stage59AK v48 source with ATR 1.8 SL / 3.2 TP, same-direction cooldown2, and 3% model risk cap.",
    ),
)

SOURCE_ANCHORS = {
    "s59al_v48_sl20_tp30_sd2_mr03": ("v48_midcov_slotfill_sd2_h2c0_no_b", "x01"),
    "s59al_v48_sl20_tp40_sd2_mr03": ("v48_midcov_slotfill_sd2_h2c0_no_b", "x01"),
    "s59al_v48_sl18_tp32_sd2_mr03": ("v48_midcov_slotfill_sd2_h2c0_no_b", "x01"),
}


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    candidate = Path(str(path))
    try:
        return io_path(candidate).resolve().relative_to(io_path(REPO_ROOT).resolve()).as_posix()
    except ValueError:
        return candidate.as_posix()


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    engine.write_csv(path, rows)


def source_specs() -> dict[str, dict[str, Any]]:
    specs: dict[str, dict[str, Any]] = {}
    for variant in STAGE59AL_VARIANTS:
        anchor, token = SOURCE_ANCHORS[variant.adapter_id]
        root = RUN50BO_ROOT / anchor
        specs[variant.adapter_id] = {
            "label": anchor,
            "run_root": RUN50BO_ROOT,
            "variant_root": root,
            "anchor": anchor,
            "model": RUN50BO_MODEL,
            "signal_column": RUN50BO_SIGNAL,
            "validation_ini": root / "mt5" / f"{token}_ta_val.ini",
            "oos_ini": root / "mt5" / f"{token}_ta_oos.ini",
            "source_note": f"Stage56 run50BO {anchor} same-direction cooldown source",
        }
    return specs


def configure_reused_engine() -> None:
    engine.STAGE59_ID = STAGE59AL_ID
    engine.NEXT_REPAIR_STAGE_ID = "59AM_adapter_repair__bounded_followup_from_stage59al"
    engine.RUN_NUMBER = RUN_NUMBER
    engine.RUN_ID = RUN_ID
    engine.PACKET_ID = PACKET_ID
    engine.PARENT_RUN_ID = PARENT_RUN_ID
    engine.SOURCE_ADAPTER_ID = SOURCE_ADAPTER_ID
    engine.DEVELOPMENT_ANCHOR = DEVELOPMENT_ANCHOR
    engine.BACKUP_ANCHOR = BACKUP_ANCHOR
    engine.BOUNDARY = BOUNDARY
    engine.STAGE_ROOT = STAGE_ROOT
    engine.RUN_ROOT = RUN_ROOT
    engine.REVIEWS_ROOT = REVIEWS_ROOT
    engine.SELECTED_ROOT = SELECTED_ROOT
    engine.SPEC_ROOT = SPEC_ROOT
    engine.INPUT_ROOT = INPUT_ROOT
    engine.PACKET_ROOT = PACKET_ROOT
    engine.COMMON_ROOT = COMMON_ROOT
    engine.REPORT_PATH = REPORT_PATH
    engine.SUMMARY_JSON_PATH = SUMMARY_JSON_PATH
    engine.SUMMARY_CSV_PATH = SUMMARY_CSV_PATH
    engine.SEGMENT_KPI_PATH = SEGMENT_KPI_PATH
    engine.EQUITY_AUDIT_PATH = EQUITY_AUDIT_PATH
    engine.RISK_ATR_TELEMETRY_PATH = RISK_ATR_TELEMETRY_PATH
    engine.DECISION_PATH = DECISION_PATH
    engine.AUDIT_CSV_PATH = AUDIT_CSV_PATH
    engine.STAGE_LEDGER_PATH = STAGE_LEDGER_PATH
    engine.RUN_REGISTRY_PATH = RUN_REGISTRY_PATH
    engine.PROJECT_LEDGER_PATH = PROJECT_LEDGER_PATH
    engine.ARTIFACT_REGISTRY_PATH = ARTIFACT_REGISTRY_PATH
    engine.WORKSPACE_STATE_PATH = WORKSPACE_STATE_PATH
    engine.CURRENT_WORKING_STATE_PATH = CURRENT_WORKING_STATE_PATH
    engine.CHANGELOG_PATH = CHANGELOG_PATH
    engine.STAGE59_VARIANTS = STAGE59AL_VARIANTS
    engine.SOURCE_SPECS = source_specs()
    engine.MODEL_RISK_MIN_PCT = {variant.adapter_id: 0.005 for variant in STAGE59AL_VARIANTS}

    repair.STAGE_ID = STAGE59AL_ID
    repair.RUN_NUMBER = RUN_NUMBER
    repair.RUN_ID = RUN_ID
    repair.RUN_ROOT = RUN_ROOT
    repair.REPAIR_VARIANTS = STAGE59AL_VARIANTS
    s58.STAGE58_ID = STAGE59AL_ID
    s58.RUN_NUMBER = RUN_NUMBER
    s58.RUN_ID = RUN_ID
    s58.PACKET_ID = PACKET_ID
    s58.PARENT_RUN_ID = PARENT_RUN_ID
    s58.RUN_ROOT = RUN_ROOT
    s58.REVIEWS_ROOT = REVIEWS_ROOT
    s58.STAGE58_VARIANTS = STAGE59AL_VARIANTS
    s58.COMMON_ROOT = COMMON_ROOT
    checkpoint.PARTIALS_ROOT = PARTIALS_ROOT


def build_attempts(inputs: Mapping[str, Any]) -> list[dict[str, Any]]:
    attempts: list[dict[str, Any]] = []
    for variant_index, variant in enumerate(STAGE59AL_VARIANTS, start=1):
        variant_root = RUN_ROOT / variant.adapter_id
        for split in ("validation_is", "oos"):
            date_values = parse_ini(engine.source_attempt_ini(split, variant))
            split_token = "val" if split == "validation_is" else "oos"
            for role_index, (tier, attempt_role, prefix, attempt_token) in enumerate(
                (
                    (mt5.TIER_A, "tier_only_total", f"mt5_tier_a_only_{variant.adapter_id}", "ta"),
                    (mt5.TIER_AB, "routed_total", f"mt5_routed_{variant.adapter_id}", "rt"),
                ),
                start=1,
            ):
                magic = 59059000 + variant_index * 100 + (1 if split == "validation_is" else 50) + role_index
                attempts.append(
                    attempt_payload(
                        run_root=variant_root,
                        run_id=RUN_ID,
                        stage_number=59,
                        exploration_label="stage59AL_BaselineAdapter__BracketFollowupFromStage59AK",
                        attempt_name=f"{variant.adapter_id}_{attempt_token}_{split_token}",
                        tier=tier,
                        split=split,
                        model_path=str(inputs["model_exports"][variant.adapter_id]["common_path"]),
                        model_id=f"{RUN_ID}_{variant.adapter_id}_entry_adapter",
                        model_backend="ebm_table",
                        feature_path=str(inputs["feature_exports"][variant.adapter_id][split]["common_path"]),
                        feature_count=1,
                        feature_order_hash=engine.feature_order_hash_for_variant(variant),
                        short_threshold=variant.short_threshold,
                        long_threshold=variant.long_threshold,
                        min_margin=MIN_MARGIN,
                        invert_signal=False,
                        from_date=str(date_values["FromDate"]),
                        to_date=str(date_values["ToDate"]),
                        primary_active_tier="tier_a",
                        attempt_role=attempt_role,
                        record_view_prefix=prefix,
                        max_hold_bars=variant.max_hold_bars,
                        common_root=f"{COMMON_ROOT}/{variant.adapter_id}",
                        fallback_enabled=False,
                        close_on_flat_signal=variant.close_on_flat_signal,
                        reverse_on_opposite_signal=variant.reverse_on_opposite_signal,
                        close_only_on_opposite_signal=variant.close_only_on_opposite_signal,
                        extra_set_values=engine.extra_set_values(variant, magic),
                    )
                )
    return attempts


def execute_or_materialize(prepared: Mapping[str, Any], args: argparse.Namespace) -> dict[str, Any]:
    if args.materialize_only:
        return {
            **dict(prepared),
            "compile": {"status": "not_attempted_materialize_only"},
            "execution_results": [],
            "strategy_tester_reports": [],
            "mt5_kpi_records": [],
            "external_verification_status": "blocked",
            "judgment": "materialized_only_no_mt5_evidence",
        }
    return checkpoint.execute_prepared_run_checkpointed(prepared, args)


def load_existing_result() -> dict[str, Any]:
    manifest = RUN_ROOT / "run_manifest.json"
    kpi = RUN_ROOT / "kpi_record.json"
    if not path_exists(manifest) or not path_exists(kpi):
        raise FileNotFoundError("Stage59AL existing run_manifest.json or kpi_record.json is missing")
    payload = json.loads(io_path(manifest).read_text(encoding="utf-8-sig"))
    payload.update(json.loads(io_path(kpi).read_text(encoding="utf-8-sig")))
    return payload


def next_stage_for_decision(decision: str) -> str:
    if decision == "proceed_to_stage60_onnx_hardening":
        return "60_adapter_onnx__hardening_runtime_reproduction"
    if decision == "open_new_model_branch":
        return "59AM_adapter_repair__new_model_branch_from_stage59al"
    if decision == "demote_current_adapter_and_select_backup":
        return "59AM_adapter_repair__demotion_from_stage59al"
    return "59AM_adapter_repair__bounded_followup_from_stage59al"


def decide_stage(summary_rows: Sequence[Mapping[str, Any]], segment_rows: Sequence[Mapping[str, Any]], external: str) -> str:
    if external != "completed":
        return "continue_repair_in_new_bounded_stage"
    reasons = engine.repair_failure_reasons(summary_rows, segment_rows)
    if not reasons:
        return "proceed_to_stage60_onnx_hardening"
    best = engine.best_repaired_variant(summary_rows)
    val = best.get("validation", {})
    oos = best.get("oos", {})
    val_pf = s58.as_float(val.get("profit_factor"), 0.0) or 0.0
    oos_pf = s58.as_float(oos.get("profit_factor"), 0.0) or 0.0
    val_net = s58.as_float(val.get("net_profit"), 0.0) or 0.0
    oos_net = s58.as_float(oos.get("net_profit"), 0.0) or 0.0
    if val_pf >= 1.05 and oos_pf >= 1.10 and val_net > 0 and oos_net > 0:
        return "continue_repair_in_new_bounded_stage"
    return "open_new_model_branch"


def line_table(summary_rows: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        "| adapter(어댑터) | split(구간) | PF(수익 팩터) | net(순손익) | DD(손실폭) | cost exp(비용 기대값) | risk max(위험 최대) | SL/TP(SL/TP) |",
        "|---|---|---:|---:|---:|---:|---:|---|",
    ]
    for row in summary_rows:
        if row.get("view") != "actual_routed_total":
            continue
        lines.append(
            "| {adapter} | {split} | {pf} | {net} | {dd} | {cost} | {risk} | {sl}/{tp} |".format(
                adapter=row.get("adapter_id", ""),
                split=row.get("split", ""),
                pf=row.get("profit_factor", ""),
                net=row.get("net_profit", ""),
                dd=row.get("max_drawdown_amount", ""),
                cost=row.get("cost_stressed_expectancy", ""),
                risk=row.get("max_actual_risk_pct_after_floor", ""),
                sl=row.get("avg_open_sl_points", ""),
                tp=row.get("avg_open_tp_points", ""),
            )
        )
    return "\n".join(lines)


def report_markdown(summary_rows: Sequence[Mapping[str, Any]], segment_rows: Sequence[Mapping[str, Any]], decision: str, external: str) -> str:
    best = engine.best_repaired_variant(summary_rows)
    reasons = engine.repair_failure_reasons(summary_rows, segment_rows) if external == "completed" else ["external_verification_not_completed"]
    return f"""# Stage59AL Bounded Followup Report(59AL단계 한정 후속 보고서)

- stage(단계): `{STAGE59AL_ID}`
- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE59AK_ID}`
- external_verification_status(외부 검증 상태): `{external}`
- decision(판정): `{decision}`
- boundary(경계): `{BOUNDARY}`

## Bounded Question(경계 질문)

Can a bounded ATR bracket repair(한정 ATR 브래킷 수리) improve the Stage59AK v48 adapter(Stage59AK v48 어댑터) without damaging validation/OOS(검증/표본외), risk behavior(위험 동작), segment KPI(구간 KPI), or equity behavior(자금 곡선 동작)?

## Result Table(결과 표)

{line_table(summary_rows)}

## Read(판독)

- best_repaired_adapter(최선 수리 어댑터): `{best.get("adapter_id", "none")}`
- failure_reasons(실패/약점 이유): `{";".join(reasons) if reasons else "none"}`
- segment_kpi_summary(구간 KPI 요약): `{rel(SEGMENT_KPI_PATH)}`
- equity_curve_audit(자금 곡선 감사): `{rel(EQUITY_AUDIT_PATH)}`
- risk_atr_telemetry(위험/ATR 텔레메트리): `{rel(RISK_ATR_TELEMETRY_PATH)}`

Effect(효과): Stage59AL(59AL단계)는 Stage59AK v48 source(Stage59AK v48 원천)의 ATR bracket(ATR 브래킷) 약점을 좁게 수리하지만, final adapter completion(최종 어댑터 완료)이나 ONNX hardening(ONNX 경화) 시작을 자동으로 만들지 않는다.

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), overall goal complete(전체 목표 완료).
"""


def decision_markdown(summary_rows: Sequence[Mapping[str, Any]], segment_rows: Sequence[Mapping[str, Any]], decision: str, external: str) -> str:
    best = engine.best_repaired_variant(summary_rows)
    reasons = engine.repair_failure_reasons(summary_rows, segment_rows) if external == "completed" else ["external_verification_not_completed"]
    next_stage = next_stage_for_decision(decision)
    return f"""# Stage59AL Decision(59AL단계 판정)

decision(판정): `{decision}`

Stage59AL(59AL단계)는 Stage59AK(59AK단계)의 v48 후보를 ATR bracket bounded repair(ATR 브래킷 한정 수리)로 기록한다. Effect(효과): Stage59AK의 약점이 수리되는지 다음 bounded stage(경계 다음 단계)의 입력 근거로 넘긴다.

## Evidence(근거)

- report(보고서): `{rel(REPORT_PATH)}`
- repaired_adapter_summary(수리 어댑터 요약): `{rel(SUMMARY_CSV_PATH)}`
- repaired_segment_kpi_summary(수리 구간 KPI 요약): `{rel(SEGMENT_KPI_PATH)}`
- repaired_equity_curve_audit(수리 자금 곡선 감사): `{rel(EQUITY_AUDIT_PATH)}`
- repaired_risk_atr_telemetry(수리 위험/ATR 텔레메트리): `{rel(RISK_ATR_TELEMETRY_PATH)}`
- external_verification_status(외부 검증 상태): `{external}`

## Reason(이유)

- best_repaired_adapter(최선 수리 어댑터): `{best.get("adapter_id", "none")}`
- failure_reasons(실패/약점 이유): `{";".join(reasons) if reasons else "none"}`

## Next(다음)

next_stage_or_branch(다음 단계/분기): `{next_stage}`

Stage59AL closeout(59AL단계 종료)는 overall goal completion(전체 목표 완료)이 아니다. Effect(효과): Stage60 ONNX(60단계 ONNX)는 adapter quality(어댑터 품질)가 강할 때만 열린다.

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), overall goal complete(전체 목표 완료).
"""


def equity_audit_markdown(summary_rows: Sequence[Mapping[str, Any]], segment_rows: Sequence[Mapping[str, Any]]) -> str:
    flagged = [
        row
        for row in segment_rows
        if row.get("quality_flag") and row.get("quality_flag") != "acceptable_measurement_only"
    ]
    lines = [
        "# Stage59AL Equity Curve Audit(59AL단계 자금 곡선 감사)",
        "",
        f"- flagged_segment_rows(표시된 구간 행): `{len(flagged)}`",
        "- read(판독): Stage59AL(59AL단계)는 final net(최종 순손익)만 보지 않고 chronological third(시간순 3분할), PF(수익 팩터), MFE capture(MFE 포착), drawdown(손실폭)을 함께 본다.",
        "",
        "Effect(효과): single spike dependence(단일 급등 의존)나 late flatline risk(후반 정체 위험)를 다음 단계 판단에 남긴다.",
    ]
    for row in flagged[:24]:
        lines.append(
            f"- `{row.get('adapter_id')}` `{row.get('split')}` `{row.get('segment_type')}` `{row.get('segment')}`: `{row.get('quality_flag')}`"
        )
    return "\n".join(lines) + "\n"


def write_required_outputs(
    result: Mapping[str, Any],
    summary_rows: Sequence[Mapping[str, Any]],
    risk_rows: Sequence[Mapping[str, Any]],
    segment_rows: Sequence[Mapping[str, Any]],
    decision: str,
    ledger_payload: Mapping[str, Any],
) -> None:
    external = str(result.get("external_verification_status") or "blocked")
    reasons = engine.repair_failure_reasons(summary_rows, segment_rows) if external == "completed" else ["external_verification_not_completed"]
    best = engine.best_repaired_variant(summary_rows)
    write_csv(SUMMARY_CSV_PATH, summary_rows)
    write_csv(SEGMENT_KPI_PATH, segment_rows)
    write_csv(RISK_ATR_TELEMETRY_PATH, risk_rows)
    write_md(REPORT_PATH, report_markdown(summary_rows, segment_rows, decision, external))
    write_md(EQUITY_AUDIT_PATH, equity_audit_markdown(summary_rows, segment_rows))
    write_md(DECISION_PATH, decision_markdown(summary_rows, segment_rows, decision, external))
    write_json(
        SUMMARY_JSON_PATH,
        {
            "created_at_utc": utc_now(),
            "stage_id": STAGE59AL_ID,
            "run_id": RUN_ID,
            "packet_id": PACKET_ID,
            "source_stage59ak_decision": rel(SOURCE_STAGE59AK_DECISION),
            "source_stage59ak_pushed_commit": SOURCE_STAGE59AK_PUSHED_COMMIT,
            "source_adapter": SOURCE_ADAPTER_ID,
            "variants": [
                {
                    **variant.__dict__,
                    "source_anchor": engine.source_anchor_for_variant(variant),
                    "signal_column": engine.signal_column_for_variant(variant),
                    "feature_order_hash": engine.feature_order_hash_for_variant(variant),
                }
                for variant in STAGE59AL_VARIANTS
            ],
            "external_verification_status": external,
            "decision": decision,
            "best_repaired_variant": best,
            "failure_reasons": reasons,
            "required_outputs": {
                "adapter_repair_report": rel(REPORT_PATH),
                "repaired_adapter_summary_json": rel(SUMMARY_JSON_PATH),
                "repaired_adapter_summary_csv": rel(SUMMARY_CSV_PATH),
                "repaired_segment_kpi_summary": rel(SEGMENT_KPI_PATH),
                "repaired_equity_curve_audit": rel(EQUITY_AUDIT_PATH),
                "repaired_risk_atr_telemetry": rel(RISK_ATR_TELEMETRY_PATH),
                "stage59al_decision": rel(DECISION_PATH),
            },
            "ledger_payload": ledger_payload,
            "claim_boundary": BOUNDARY,
            "overall_goal_complete": False,
        },
    )


def artifact_rows(result: Mapping[str, Any]) -> list[dict[str, Any]]:
    created = utc_now()
    paths = [
        REPORT_PATH,
        SUMMARY_JSON_PATH,
        SUMMARY_CSV_PATH,
        SEGMENT_KPI_PATH,
        EQUITY_AUDIT_PATH,
        RISK_ATR_TELEMETRY_PATH,
        DECISION_PATH,
        AUDIT_CSV_PATH,
        STAGE_LEDGER_PATH,
        RUN_ROOT / "run_manifest.json",
        RUN_ROOT / "kpi_record.json",
    ]
    for name in (
        "routing_receipt.json",
        "experiment_design_receipt.json",
        "runtime_evidence_gate.json",
        "kpi_contract_audit.json",
        "result_judgment_gate.json",
        "artifact_lineage_audit.json",
        "final_claim_guard.json",
        "required_gate_coverage_audit.json",
        "aggregate_summary.json",
    ):
        paths.append(PACKET_ROOT / name)
    rows: list[dict[str, Any]] = []
    for path in paths:
        if path_exists(path):
            rows.append(
                {
                    "artifact_id": f"{RUN_ID}__{path.name}",
                    "artifact_type": "stage59al_bounded_followup_evidence",
                    "path": rel(path),
                    "sha256": sha256_file_lf_normalized(path),
                    "stage_id": STAGE59AL_ID,
                    "run_id": RUN_ID,
                    "created_at_utc": created,
                    "notes": "Stage59AL bounded ATR bracket repair artifact.",
                }
            )
    for report in result.get("strategy_tester_reports", []):
        html = report.get("html_report", {}) if isinstance(report.get("html_report"), Mapping) else {}
        raw_path = report.get("path") or html.get("path")
        if not raw_path:
            continue
        report_path = Path(str(raw_path))
        if path_exists(report_path) and io_path(report_path).is_file():
            rows.append(
                {
                    "artifact_id": f"{RUN_ID}__mt5_report__{report_path.stem}",
                    "artifact_type": "mt5_strategy_tester_report",
                    "path": rel(report_path),
                    "sha256": sha256_file_lf_normalized(report_path),
                    "stage_id": STAGE59AL_ID,
                    "run_id": RUN_ID,
                    "created_at_utc": created,
                    "notes": "Actual Stage59AL MT5 Strategy Tester HTML report.",
                }
            )
    return rows


def write_ledgers(
    result: Mapping[str, Any],
    summary_rows: Sequence[Mapping[str, Any]],
    segment_rows: Sequence[Mapping[str, Any]],
    decision: str,
    artifacts: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    external = str(result.get("external_verification_status") or "blocked")
    best = engine.best_repaired_variant(summary_rows)
    reasons = engine.repair_failure_reasons(summary_rows, segment_rows) if external == "completed" else ["external_verification_not_completed"]
    mt5_rows = build_mt5_alpha_ledger_rows(
        run_id=RUN_ID,
        stage_id=STAGE59AL_ID,
        mt5_kpi_records=result.get("mt5_kpi_records", []),
        run_output_root=RUN_ROOT,
        external_verification_status=external,
    )
    aggregate = {
        "ledger_row_id": f"{RUN_ID}__aggregate_bounded_followup_from_stage59ak",
        "stage_id": STAGE59AL_ID,
        "run_id": RUN_ID,
        "subrun_id": "aggregate_bounded_followup_from_stage59ak",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "bounded_followup_from_stage59ak",
        "tier_scope": "Tier A+B",
        "kpi_scope": "baseline_adapter_repair",
        "scoreboard_lane": "runtime_probe",
        "status": "completed" if external == "completed" else "blocked",
        "judgment": decision,
        "path": rel(DECISION_PATH),
        "primary_kpi": ledger_pairs(
            [
                ("best_repaired_adapter", best.get("adapter_id", "none")),
                ("validation_net", (best.get("validation") or {}).get("net_profit")),
                ("oos_net", (best.get("oos") or {}).get("net_profit")),
                ("validation_pf", (best.get("validation") or {}).get("profit_factor")),
                ("oos_pf", (best.get("oos") or {}).get("profit_factor")),
            ]
        ),
        "guardrail_kpi": ledger_pairs(
            [
                ("failure_reasons", reasons),
                ("atr_sltp", "measured"),
                ("model_controlled_risk_pct", "measured"),
                ("overall_goal_complete", 0),
            ]
        ),
        "external_verification_status": external,
        "notes": "Stage59AL bounded ATR bracket followup from Stage59AK evidence; not final package completion.",
    }
    ledger_rows = [*mt5_rows, aggregate]
    run_payload = upsert_csv_rows(
        RUN_REGISTRY_PATH,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE59AL_ID,
                "lane": "baseline_adapter_bounded_followup_from_stage59ak",
                "status": "completed" if external == "completed" else "blocked",
                "judgment": decision,
                "path": rel(DECISION_PATH),
                "notes": ledger_pairs(
                    [
                        ("best_repaired_adapter", best.get("adapter_id", "none")),
                        ("boundary", BOUNDARY),
                    ]
                ),
            }
        ],
        key="run_id",
    )
    stage_payload = upsert_csv_rows(STAGE_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, ledger_rows, key="ledger_row_id")
    project_payload = upsert_csv_rows(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, ledger_rows, key="ledger_row_id")
    artifact_payload = upsert_csv_rows(
        ARTIFACT_REGISTRY_PATH,
        ("artifact_id", "artifact_type", "path", "sha256", "stage_id", "run_id", "created_at_utc", "notes"),
        list(artifacts),
        key="artifact_id",
    )
    return {
        "run_registry": run_payload,
        "stage_ledger": stage_payload,
        "project_alpha_ledger": project_payload,
        "artifact_registry": artifact_payload,
    }


def write_packet_files(
    result: Mapping[str, Any],
    summary_rows: Sequence[Mapping[str, Any]],
    segment_rows: Sequence[Mapping[str, Any]],
    risk_rows: Sequence[Mapping[str, Any]],
    decision: str,
    ledger_payload: Mapping[str, Any],
) -> None:
    external = str(result.get("external_verification_status") or "blocked")
    best = engine.best_repaired_variant(summary_rows)
    reasons = engine.repair_failure_reasons(summary_rows, segment_rows) if external == "completed" else ["external_verification_not_completed"]
    files = {
        "routing_receipt.json": {
            "packet_id": PACKET_ID,
            "primary_family": "runtime_backtest",
            "primary_skill": "obsidian-runtime-parity",
            "support_skills": ["obsidian-experiment-design", "obsidian-result-judgment", "obsidian-artifact-lineage"],
            "required_gates": ["runtime_evidence_gate", "kpi_contract_audit", "result_judgment_gate", "artifact_lineage_audit", "final_claim_guard"],
            "status": "completed",
        },
        "experiment_design_receipt.json": {
            "hypothesis": "A bounded ATR bracket repair on the Stage59AK v48 source may improve post-ATR/risk BaselineAdapter behavior.",
            "decision_use": "Proceed to ONNX only if full adapter quality is strong; otherwise continue bounded repair or open another source branch.",
            "comparison_baseline": "Stage59AK v48 source branch evidence and prior Stage59Y v64 branch evidence",
            "control_variables": ["US100 M5", "split_v1", "Tier B disabled", "wide ATR bracket", "3% model risk cap", "ONNX deferred"],
            "changed_variables": ["ATR stop multiplier", "ATR take-profit multiplier"],
            "sample_scope": "MT5 validation 2025-01-02..2025-10-01 and OOS 2025-10-01..2026-04-13",
            "success_criteria": ["validation/OOS net positive", "validation/OOS PF >= 1.10", "cost-stressed expectancy positive", "ATR/risk telemetry present", "no severe segment flags"],
            "failure_criteria": ["PF < 1.10", "cost-stressed expectancy <= 0", "missing risk or ATR telemetry", "weak segment flags"],
            "invalid_conditions": ["missing MT5 reports", "missing source feature files", "runtime output mismatch"],
            "stop_conditions": "three bounded Stage59AK v48 ATR bracket variants only",
            "evidence_plan": [rel(REPORT_PATH), rel(SUMMARY_CSV_PATH), rel(SEGMENT_KPI_PATH), rel(RISK_ATR_TELEMETRY_PATH), rel(DECISION_PATH)],
            "status": "completed",
        },
        "runtime_evidence_gate.json": {"external_verification_status": external, "mt5_reports": result.get("strategy_tester_reports", []), "status": external},
        "kpi_contract_audit.json": {"summary_rows": len(summary_rows), "segment_rows": len(segment_rows), "risk_rows": len(risk_rows), "status": "completed"},
        "result_judgment_gate.json": {
            "result_subject": RUN_ID,
            "judgment_label": decision,
            "failure_reasons": reasons,
            "best_repaired_adapter": best.get("adapter_id", "none"),
            "claim_boundary": BOUNDARY,
            "status": "passed_with_boundary",
        },
        "artifact_lineage_audit.json": {
            "source_inputs": [rel(SOURCE_STAGE59AK_DECISION), rel(SOURCE_STAGE59AK_REPORT), rel(SOURCE_STAGE59AK_SUMMARY), rel(RUN50BO_SUMMARY), rel(RUN50BO_AUDIT), rel(RUN50BO_SOURCE_SUMMARY), rel(RUN50BO_MODEL)],
            "producer": "stage_pipelines/stage59al/bracket_followup_from_stage59ak.py",
            "consumers": [rel(REPORT_PATH), rel(DECISION_PATH), rel(SUMMARY_JSON_PATH)],
            "ledger_links": ledger_payload,
            "lineage_judgment": "connected_with_boundary",
            "status": "completed",
        },
        "final_claim_guard.json": {
            "overall_goal_complete": False,
            "deployment_claim": False,
            "live_readiness_claim": False,
            "runtime_authority_claim": False,
            "production_baseline_claim": False,
            "operating_promotion_claim": False,
            "operating_reference_claim": False,
            "status": "completed",
        },
        "required_gate_coverage_audit.json": {
            "required_gates": ["runtime_evidence_gate", "kpi_contract_audit", "result_judgment_gate", "artifact_lineage_audit", "final_claim_guard"],
            "covered_by": ["runtime_evidence_gate.json", "kpi_contract_audit.json", "result_judgment_gate.json", "artifact_lineage_audit.json", "final_claim_guard.json"],
            "status": "completed",
        },
        "aggregate_summary.json": {
            "packet_id": PACKET_ID,
            "stage_id": STAGE59AL_ID,
            "run_id": RUN_ID,
            "decision": decision,
            "best_repaired_adapter": best.get("adapter_id", "none"),
            "failure_reasons": reasons,
            "external_verification_status": external,
            "overall_goal_complete": False,
            "claim_boundary": BOUNDARY,
            "next_stage_or_branch": next_stage_for_decision(decision),
            "required_outputs": {
                "adapter_repair_report": rel(REPORT_PATH),
                "repaired_adapter_summary_json": rel(SUMMARY_JSON_PATH),
                "repaired_adapter_summary_csv": rel(SUMMARY_CSV_PATH),
                "repaired_segment_kpi_summary": rel(SEGMENT_KPI_PATH),
                "repaired_equity_curve_audit": rel(EQUITY_AUDIT_PATH),
                "repaired_risk_atr_telemetry": rel(RISK_ATR_TELEMETRY_PATH),
                "stage59al_decision": rel(DECISION_PATH),
            },
        },
    }
    for name, payload in files.items():
        write_json(PACKET_ROOT / name, payload)


def write_stage_docs(decision: str) -> None:
    next_stage = next_stage_for_decision(decision)
    next_stage_number = next_stage.split("_", 1)[0]
    write_md(
        SPEC_ROOT / "stage_brief.md",
        f"""# 59AL Brief(59AL단계 개요)

- stage_id(단계 ID): `{STAGE59AL_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE59AK_ID}`
- source_decision(원천 판정): `continue_repair_in_new_bounded_stage`
- bounded_question(경계 질문): `Can bounded ATR bracket variants improve the Stage59AK v48 adapter without damaging validation/OOS, risk behavior, segment KPI, or equity behavior?`
- stage_status(단계 상태): `closed_bounded_followup_from_stage59ak`
- boundary(경계): `{BOUNDARY}`

59AL(59AL단계)는 Stage59AK v48 source(Stage59AK v48 원천)를 ATR bracket repair(ATR 브래킷 수리)로 측정했다. Effect(효과): Stage60 ONNX(60단계 ONNX)는 품질 근거가 강할 때만 열린다.
""",
    )
    write_md(
        INPUT_ROOT / "input_refs.md",
        f"""# 59AL Input References(59AL단계 입력 참조)

- stage59ak_decision(59AK단계 판정): `{rel(SOURCE_STAGE59AK_DECISION)}`
- stage59ak_report(59AK단계 보고서): `{rel(SOURCE_STAGE59AK_REPORT)}`
- run50BO_summary(50BO 실행 요약): `{rel(RUN50BO_SUMMARY)}`
- run50BO_audit(50BO 실행 감사): `{rel(RUN50BO_AUDIT)}`
- run50BO_source_summary(50BO 원천 요약): `{rel(RUN50BO_SOURCE_SUMMARY)}`
- run50BO_model(50BO 모델): `{rel(RUN50BO_MODEL)}`
- source_stage59ak_pushed_commit(원천 59AK단계 푸시 커밋): `{SOURCE_STAGE59AK_PUSHED_COMMIT}`
""",
    )
    write_md(
        SELECTED_ROOT / "selection_status.md",
        f"""# 59AL Selection Status(59AL단계 선택 상태)

- stage_status(단계 상태): `closed_bounded_followup_from_stage59ak`
- source_stage(원천 단계): `{SOURCE_STAGE59AK_ID}`
- source_decision(원천 판정): `continue_repair_in_new_bounded_stage`
- stage59al_decision(59AL단계 판정): `{decision}`
- next_stage_or_branch(다음 단계/분기): `{next_stage}`
- selected_research_baseline(선택 연구 기준선): `none`
- claim_boundary(주장 경계): `{BOUNDARY}`

Effect(효과): Stage59AL(59AL단계)는 Stage59AK v48 repair(Stage59AK v48 수리) 결과를 보존하지만 final package(최종 패키지)나 operating claim(운영 주장)을 만들지 않는다.
""",
    )
    write_md(
        REVIEWS_ROOT / "review_index.md",
        f"""# Stage59AL Review Index(59AL단계 검토 색인)

- bounded_followup_report(한정 후속 보고서): `{rel(REPORT_PATH)}`
- bounded_followup_summary(한정 후속 요약): `{rel(SUMMARY_CSV_PATH)}`
- bounded_followup_segment_kpi(한정 후속 구간 KPI): `{rel(SEGMENT_KPI_PATH)}`
- bounded_followup_equity_curve_audit(한정 후속 자금 곡선 감사): `{rel(EQUITY_AUDIT_PATH)}`
- bounded_followup_risk_atr_telemetry(한정 후속 위험/ATR 텔레메트리): `{rel(RISK_ATR_TELEMETRY_PATH)}`
- stage59al_decision(59AL단계 판정): `{rel(DECISION_PATH)}`
""",
    )
    next_root = Path("stages") / next_stage
    write_md(
        next_root / "00_spec/stage_brief.md",
        f"""# {next_stage_number} Brief({next_stage_number}단계 개요)

- stage_id(단계 ID): `{next_stage}`
- source_stage(원천 단계): `{STAGE59AL_ID}`
- source_decision(원천 판정): `{decision}`
- bounded_question(경계 질문): `Use the Stage59AL decision to choose the next bounded repair, demotion, or source branch without starting ONNX early.`
- boundary(경계): `{BOUNDARY}`

{next_stage_number}({next_stage_number}단계)는 Stage59AL(59AL단계)의 판정 이후 단계다. Effect(효과): 한 단계 결과를 전체 목표 완료로 착각하지 않고 다음 bounded step(경계 다음 단계)만 연다.
""",
    )
    write_md(
        next_root / "01_inputs/input_refs.md",
        f"""# {next_stage_number} Input References({next_stage_number}단계 입력 참조)

- stage59al_decision(59AL단계 판정): `{rel(DECISION_PATH)}`
- bounded_followup_report(한정 후속 보고서): `{rel(REPORT_PATH)}`
- bounded_followup_summary(한정 후속 요약): `{rel(SUMMARY_CSV_PATH)}`
- bounded_followup_segment_kpi(한정 후속 구간 KPI): `{rel(SEGMENT_KPI_PATH)}`
- bounded_followup_risk_atr_telemetry(한정 후속 위험/ATR 텔레메트리): `{rel(RISK_ATR_TELEMETRY_PATH)}`
""",
    )
    write_md(next_root / "03_reviews/review_index.md", f"# {next_stage_number} Review Index({next_stage_number}단계 검토 색인)\n\n{next_stage_number}({next_stage_number}단계)는 planned(계획) 상태다.\n")
    write_md(
        next_root / "04_selected/selection_status.md",
        f"""# {next_stage_number} Selection Status({next_stage_number}단계 선택 상태)

- stage_status(단계 상태): `active_planned_from_stage59al`
- source_stage(원천 단계): `{STAGE59AL_ID}`
- source_decision(원천 판정): `{decision}`
- selected_research_baseline(선택 연구 기준선): `none`
- claim_boundary(주장 경계): `{BOUNDARY}`

Effect(효과): {next_stage_number}({next_stage_number}단계)는 Stage59AL(59AL단계)의 남은 질문을 다음 bounded question(경계 질문)으로만 다룬다.
""",
    )


def update_current_truth(decision: str, summary_rows: Sequence[Mapping[str, Any]], external: str) -> None:
    best = engine.best_repaired_variant(summary_rows)
    next_stage = next_stage_for_decision(decision)
    next_packet = (
        "stage60_onnx_hardening_v1"
        if decision == "proceed_to_stage60_onnx_hardening"
        else "stage59am_new_model_branch_from_stage59al_v1"
        if decision == "open_new_model_branch"
        else "stage59am_demotion_from_stage59al_v1"
        if decision == "demote_current_adapter_and_select_backup"
        else "stage59am_bounded_followup_from_stage59al_v1"
    )
    next_run = (
        "run60A_stage60_onnx_hardening_v1"
        if decision == "proceed_to_stage60_onnx_hardening"
        else "run59AH_stage59am_new_model_branch_from_stage59al_v1"
        if decision == "open_new_model_branch"
        else "run59AH_stage59am_demotion_from_stage59al_v1"
        if decision == "demote_current_adapter_and_select_backup"
        else "run59AH_stage59am_bounded_followup_from_stage59al_v1"
    )
    write_md(
        CURRENT_WORKING_STATE_PATH,
        f"""# Current Working State(현재 작업 상태)

- current_packet(현재 작업 묶음): `{next_packet}`
- current_run(현재 실행): `{next_run}`
- active_stage(활성 단계): `{next_stage}`
- selected_research_baseline(선택 연구 기준선): `none`
- development_anchor(개발 기준점): `{DEVELOPMENT_ANCHOR}`
- backup_anchor(예비 기준점): `{BACKUP_ANCHOR}`
- adapter_under_review(검토 중 어댑터): `{best.get("adapter_id", "none")}`
- status(상태): `stage59al_closed_{decision}`
- claim_boundary(주장 경계): research/development only(연구/개발 전용)

Stage59AL(59AL단계) closed(종료) as bounded ATR bracket repair(ATR 브래킷 한정 수리). Effect(효과): Stage59AK v48 source(Stage59AK v48 원천)를 ATR/risk(ATR/위험) 조건으로 좁게 수리했지만 overall goal complete(전체 목표 완료)는 아니다.

## Latest Stage59AL Evidence(최신 59AL단계 근거)

- run(실행): `{RUN_ID}`
- decision(판정): `{decision}`
- best_repaired_adapter(최선 수리 어댑터): `{best.get("adapter_id", "none")}`
- external_verification_status(외부 검증 상태): `{external}`
- next_stage_or_branch(다음 단계/분기): `{next_stage}`
- report(보고서): `{rel(REPORT_PATH)}`
- stage59al_decision(59AL단계 판정): `{rel(DECISION_PATH)}`

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준선), overall_goal_complete(전체 목표 완료).
""",
    )
    text = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    text = re.sub(r"^current_run_id: .*$", f"current_run_id: {next_run}", text, count=1, flags=re.MULTILINE)
    text = re.sub(r"^updated_on: .*$", "updated_on: '2026-05-16'", text, count=1, flags=re.MULTILINE)
    text = re.sub(r"^active_stage: .*$", f"active_stage: {next_stage}", text, count=1, flags=re.MULTILINE)
    focus = (
        "current_focus:\n"
        f"- >-\n"
        f"  Stage59AL(59AL단계) `{STAGE59AL_ID}` closed(종료) as ATR bracket repair(ATR 브래킷 수리); decision(판정)=`{decision}`. "
        f"Effect(효과): best adapter(최선 어댑터) `{best.get('adapter_id', 'none')}` evidence(근거)를 보존하고 전체 목표 완료로 올리지 않는다.\n"
        f"- >-\n"
        f"  Next stage_or_branch(다음 단계/분기) `{next_stage}` is active/planned(활성/계획). Effect(효과): Stage60 ONNX(60단계 ONNX)는 품질 근거가 강할 때만 열린다.\n"
    )
    text = re.sub(r"current_focus:\n(?:- >-\n(?:  .*\n)+)+", focus, text, count=1)
    block = f"""

stage59al_bounded_followup_from_stage59ak:
  packet_id: {PACKET_ID}
  stage_id: {STAGE59AL_ID}
  status: closed_bounded_followup_from_stage59ak
  current_run_id: {RUN_ID}
  best_repaired_adapter: {best.get("adapter_id", "none")}
  source_stage59ak_pushed_commit: {SOURCE_STAGE59AK_PUSHED_COMMIT}
  decision: {decision}
  next_stage_or_branch: {next_stage}
  report_path: {rel(DECISION_PATH)}
  packet_summary_path: {rel(PACKET_ROOT / "aggregate_summary.json")}
  external_verification_status: {external}
  boundary: {BOUNDARY}
"""
    if "stage59al_bounded_followup_from_stage59ak:" in text:
        text = re.sub(r"\nstage59al_bounded_followup_from_stage59ak:\n(?:  .*\n)*", block, text, count=1)
    else:
        text += block
    io_path(WORKSPACE_STATE_PATH).write_text(text, encoding="utf-8-sig")


def append_changelog(decision: str) -> None:
    entry = (
        "\n## 2026-05-16 - Stage59AL bounded bracket followup from Stage59AK closeout(59AL단계 Stage59AK 기반 브래킷 후속 종료)\n\n"
        f"- run(실행): `{RUN_ID}`\n"
        f"- decision(판정): `{decision}`\n"
        "- effect(효과): Stage59AK v48 source(Stage59AK v48 원천)를 ATR bracket repair(ATR 브래킷 수리)로 측정하고 다음 bounded stage(경계 다음 단계) 조건을 남겼다.\n"
    )
    existing = io_path(CHANGELOG_PATH).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG_PATH) else ""
    if f"- run(실행): `{RUN_ID}`" not in existing:
        io_path(CHANGELOG_PATH).write_text(existing.rstrip() + entry, encoding="utf-8-sig")

def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Stage59AL bounded ATR bracket followup from Stage59AK.")
    parser.add_argument("--terminal-path", default=str(TERMINAL_PATH_DEFAULT))
    parser.add_argument("--metaeditor-path", default=str(METAEDITOR_PATH_DEFAULT))
    parser.add_argument("--terminal-data-root", default=str(TERMINAL_DATA_ROOT_DEFAULT))
    parser.add_argument("--common-files-root", default=str(COMMON_FILES_ROOT_DEFAULT))
    parser.add_argument("--tester-profile-root", default=str(TESTER_PROFILE_ROOT_DEFAULT))
    parser.add_argument("--timeout-seconds", type=int, default=120)
    parser.add_argument("--runtime-output-timeout-seconds", type=int, default=180)
    parser.add_argument("--attempt-name-contains", default="")
    parser.add_argument("--attempt-offset", type=int, default=0)
    parser.add_argument("--attempt-limit", type=int)
    parser.add_argument("--resume-partials", action="store_true")
    parser.add_argument("--skip-compile", action="store_true")
    parser.add_argument("--materialize-only", action="store_true")
    parser.add_argument("--finalize-existing", action="store_true")
    parser.add_argument("--cost-stress-per-trade", type=float, default=0.3)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    configure_reused_engine()
    args = parse_args(argv or sys.argv[1:])
    if args.finalize_existing:
        result = load_existing_result()
    else:
        inputs = engine.prepare_inputs(Path(args.common_files_root))
        attempts = build_attempts(inputs)
        prepared = {
            "run_id": RUN_ID,
            "stage_id": STAGE59AL_ID,
            "stage_number": 59,
            "run_number": RUN_NUMBER,
            "run_root": RUN_ROOT,
            "packet_id": PACKET_ID,
            "attempts": attempts,
            "common_copies": inputs["common_copies"],
            "feature_exports": inputs["feature_exports"],
            "model_artifacts": inputs["model_exports"],
            "route_coverage": engine.route_coverage(),
            "model_family": "baseline_adapter_stage59al_stage59ak_v48_atr_bracket_ebm_table",
            "feature_set_id": "stage59al_stage59ak_v48_atr_bracket_discrete_signal",
            "label_id": "label_v1_fwd12_m5_logret_train_q33_3class",
            "split_contract": "split_v1_calendar_train_20220901_20241231_val_20250101_20250930_oos_20251001_20260413",
            "claim_boundary": BOUNDARY,
        }
        result = execute_or_materialize(prepared, args)
    audit_rows = s58.audit_rows_for_result(result, float(args.cost_stress_per_trade)) if result.get("mt5_kpi_records") else []
    risk_rows = s58.risk_rows_from_result(result)
    summary_rows = s58.build_summary_rows(result, audit_rows, risk_rows)
    segment_rows = s58.segment_kpi_rows(summary_rows)
    external = str(result.get("external_verification_status") or "blocked")
    decision = decide_stage(summary_rows, segment_rows, external)
    engine.write_run_identity(result)
    write_csv(AUDIT_CSV_PATH, audit_rows)
    artifacts = artifact_rows(result)
    ledger_payload = write_ledgers(result, summary_rows, segment_rows, decision, artifacts)
    write_required_outputs(result, summary_rows, risk_rows, segment_rows, decision, ledger_payload)
    artifacts = artifact_rows(result)
    ledger_payload = write_ledgers(result, summary_rows, segment_rows, decision, artifacts)
    payload = json.loads(io_path(SUMMARY_JSON_PATH).read_text(encoding="utf-8-sig"))
    payload["ledger_payload"] = ledger_payload
    write_json(SUMMARY_JSON_PATH, payload)
    write_packet_files(result, summary_rows, segment_rows, risk_rows, decision, ledger_payload)
    write_stage_docs(decision)
    update_current_truth(decision, summary_rows, external)
    append_changelog(decision)
    print(
        json.dumps(
            json_ready(
                {
                    "status": "ok" if external == "completed" else "blocked",
                    "run_id": RUN_ID,
                    "decision": decision,
                    "best_repaired_variant": engine.best_repaired_variant(summary_rows),
                    "summary_json": rel(SUMMARY_JSON_PATH),
                    "decision_path": rel(DECISION_PATH),
                }
            ),
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
