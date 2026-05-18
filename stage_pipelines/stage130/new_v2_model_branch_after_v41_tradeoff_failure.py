from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import time
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
    execute_prepared_run,
    parse_ini,
)
from foundation.mt5 import runtime_support as mt5  # noqa: E402
from stage_pipelines.stage56 import baseline_adapter_repair_batch as repair  # noqa: E402
from stage_pipelines.stage56 import independent_event_source_route_branch as aw  # noqa: E402
from stage_pipelines.stage58 import risk_atr_integration as s58  # noqa: E402
from stage_pipelines.stage59d import source_lifecycle_or_demote as engine  # noqa: E402


STAGE56_ID = "56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection"
SOURCE_STAGE129_ID = "129_adapter_research__v41_quality_density_followup_review"
STAGE_ID = "130_adapter_research__new_v2_model_branch_after_v41_tradeoff_failure"
RUN_NUMBER = "run130A"
RUN_ID = "run130A_stage130_new_v2_model_branch_after_v41_tradeoff_failure_v1"
PACKET_ID = "stage130_new_v2_model_branch_after_v41_tradeoff_failure_v1"
PARENT_RUN_ID = "run129A_stage129_v41_quality_density_followup_review_v1"
SOURCE_ADAPTER_ID = "stage129_v41_tradeoff_failure_memory"
SOURCE_STAGE129_CLOSEOUT_COMMIT = "8f721f71a71d8ac7f990c4412ca47cef2a23c3da"
SOURCE_STAGE129_LATEST_COMMIT = "645bc9d14e14e91cd4ef8392a50e51cce89a1a15"
NEXT_STAGE_ID = "131_adapter_research__new_v2_model_branch_followup_review"
NEXT_RUN_ID = "run131A_stage131_new_v2_model_branch_followup_review_v1"
NEXT_PACKET_ID = "stage131_new_v2_model_branch_followup_review_v1"
TARGET_SURFACE = "legacy_34d_kpi_lesson_only_no_legacy_inheritance"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment"
)

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
SELECTED_ROOT = STAGE_ROOT / "04_selected"
SPEC_ROOT = STAGE_ROOT / "00_spec"
INPUT_ROOT = STAGE_ROOT / "01_inputs"
PACKET_ROOT = Path("docs/agent_control/packets") / PACKET_ID
NEXT_STAGE_ROOT = Path("stages") / NEXT_STAGE_ID

SOURCE_STAGE_ROOT = Path("stages") / STAGE56_ID
RUN50BN_ROOT = SOURCE_STAGE_ROOT / "02_runs/run50BN"
RUN50BN_MODEL = RUN50BN_ROOT / "models/stage56_context_timed_event_signal_discrete_score_table.csv"
RUN50BN_SUMMARY = SOURCE_STAGE_ROOT / "03_reviews/run50BN_summary.csv"
RUN50BN_AUDIT = SOURCE_STAGE_ROOT / "03_reviews/run50BN_audit.csv"
RUN50BN_SOURCE_SUMMARY = SOURCE_STAGE_ROOT / "03_reviews/run50BN_source_summary.csv"
SOURCE_STAGE129_DECISION = Path("stages") / SOURCE_STAGE129_ID / "03_reviews/stage129_decision.md"
SOURCE_STAGE129_REPORT = Path("stages") / SOURCE_STAGE129_ID / "03_reviews/stage129_quality_density_followup_review.md"
SOURCE_STAGE129_GAP = Path("stages") / SOURCE_STAGE129_ID / "03_reviews/stage129_stage128_34d_gap_summary.csv"

RUN50BN_SIGNAL = "stage56_context_et_event_signal"
COMMON_ROOT = f"OPV2/stage130/{RUN_NUMBER}"
MIN_MARGIN = 0.0

REPORT_PATH = REVIEWS_ROOT / "stage130_new_v2_model_branch_report.md"
SUMMARY_JSON_PATH = REVIEWS_ROOT / "stage130_new_v2_model_branch_summary.json"
SUMMARY_CSV_PATH = REVIEWS_ROOT / "stage130_new_v2_model_branch_summary.csv"
SEGMENT_KPI_PATH = REVIEWS_ROOT / "stage130_segment_kpi_summary.csv"
EQUITY_AUDIT_PATH = REVIEWS_ROOT / "stage130_equity_curve_audit.md"
RISK_ATR_TELEMETRY_PATH = REVIEWS_ROOT / "stage130_risk_atr_telemetry.csv"
DECISION_PATH = REVIEWS_ROOT / "stage130_decision.md"
AUDIT_CSV_PATH = REVIEWS_ROOT / "stage130_trade_audit.csv"
STAGE_LEDGER_PATH = REVIEWS_ROOT / "stage_run_ledger.csv"
RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
PROJECT_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
ARTIFACT_REGISTRY_PATH = Path("docs/registers/artifact_registry.csv")
WORKSPACE_STATE_PATH = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE_PATH = Path("docs/context/current_working_state.md")
CHANGELOG_PATH = Path("docs/workspace/changelog.md")

LEGACY_34D = {
    "profit_factor": 1.583157,
    "net_profit": 987.60,
    "max_drawdown_percent": 12.909136,
    "trade_count": 404,
}

VARIANTS = (
    repair.RepairVariant(
        adapter_id="s130_v42_veto_sd2_h2_mr03_wideatr",
        label="run50BN_v42_veto_conflict_threshold55_risk3pct_wide_atr_sd2",
        atr_enabled=True,
        model_risk_enabled=True,
        fixed_lot=0.25,
        atr_stop_multiplier=2.5,
        atr_take_profit_multiplier=3.5,
        model_risk_max_pct=0.03,
        same_direction_reentry_cooldown_bars=2,
        short_threshold=0.55,
        long_threshold=0.55,
        reverse_on_opposite_signal=False,
        close_only_on_opposite_signal=True,
        max_hold_bars=2,
        notes="Stage130 bounded new branch: run50BN v42 veto-conflict source with same ATR/risk shell.",
    ),
    repair.RepairVariant(
        adapter_id="s130_v43_direction_sd2_h2_mr03_wideatr",
        label="run50BN_v43_direction_threshold55_risk3pct_wide_atr_sd2",
        atr_enabled=True,
        model_risk_enabled=True,
        fixed_lot=0.25,
        atr_stop_multiplier=2.5,
        atr_take_profit_multiplier=3.5,
        model_risk_max_pct=0.03,
        same_direction_reentry_cooldown_bars=2,
        short_threshold=0.55,
        long_threshold=0.55,
        reverse_on_opposite_signal=False,
        close_only_on_opposite_signal=True,
        max_hold_bars=2,
        notes="Stage130 bounded new branch: run50BN v43 direction source with same ATR/risk shell.",
    ),
    repair.RepairVariant(
        adapter_id="s130_v44_topup_veto_sd2_h2_mr03_wideatr",
        label="run50BN_v44_topup_veto_conflict_threshold55_risk3pct_wide_atr_sd2",
        atr_enabled=True,
        model_risk_enabled=True,
        fixed_lot=0.25,
        atr_stop_multiplier=2.5,
        atr_take_profit_multiplier=3.5,
        model_risk_max_pct=0.03,
        same_direction_reentry_cooldown_bars=2,
        short_threshold=0.55,
        long_threshold=0.55,
        reverse_on_opposite_signal=False,
        close_only_on_opposite_signal=True,
        max_hold_bars=2,
        notes="Stage130 bounded new branch: run50BN v44 top-up veto source with same ATR/risk shell.",
    ),
    repair.RepairVariant(
        adapter_id="s130_v45_withb_veto_sd2_h2_mr03_wideatr",
        label="run50BN_v45_with_b_veto_conflict_threshold55_risk3pct_wide_atr_sd2",
        atr_enabled=True,
        model_risk_enabled=True,
        fixed_lot=0.25,
        atr_stop_multiplier=2.5,
        atr_take_profit_multiplier=3.5,
        model_risk_max_pct=0.03,
        same_direction_reentry_cooldown_bars=2,
        short_threshold=0.55,
        long_threshold=0.55,
        reverse_on_opposite_signal=False,
        close_only_on_opposite_signal=True,
        max_hold_bars=2,
        notes="Stage130 bounded new branch: run50BN v45 source includes Tier B labels but runtime keeps Tier B disabled.",
    ),
)

SOURCE_ANCHORS = {
    "s130_v42_veto_sd2_h2_mr03_wideatr": ("v42_v22_midcov_et40_veto_conflict_h2c0_no_b", "x02"),
    "s130_v43_direction_sd2_h2_mr03_wideatr": ("v43_v22_midcov_et40_direction_h2c0_no_b", "x03"),
    "s130_v44_topup_veto_sd2_h2_mr03_wideatr": ("v44_v22_topup_et40_veto_conflict_h2c0_no_b", "x04"),
    "s130_v45_withb_veto_sd2_h2_mr03_wideatr": ("v45_v22_midcov_et40_veto_conflict_h2c0_with_b", "x05"),
}


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    candidate = Path(str(path))
    try:
        return io_path(candidate).resolve().relative_to(io_path(REPO_ROOT).resolve()).as_posix()
    except ValueError:
        return candidate.as_posix()


def csv_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, float):
        return f"{value:.10f}"
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(json_ready(value), ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return str(value)


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
        for row in rows:
            writer.writerow({column: csv_value(row.get(column)) for column in columns})


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def upsert_csv_rows_retry(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]], *, key: str) -> dict[str, Any]:
    last_error: OSError | None = None
    for attempt in range(3):
        try:
            return upsert_csv_rows(path, columns, rows, key=key)
        except OSError as exc:
            last_error = exc
            time.sleep(0.5 * (attempt + 1))
    assert last_error is not None
    raise last_error


def source_specs() -> dict[str, dict[str, Any]]:
    specs: dict[str, dict[str, Any]] = {}
    for variant in VARIANTS:
        anchor, token = SOURCE_ANCHORS[variant.adapter_id]
        root = RUN50BN_ROOT / anchor
        specs[variant.adapter_id] = {
            "label": anchor,
            "run_root": RUN50BN_ROOT,
            "variant_root": root,
            "anchor": anchor,
            "model": RUN50BN_MODEL,
            "signal_column": RUN50BN_SIGNAL,
            "validation_ini": root / "mt5" / f"{token}_ta_val.ini",
            "oos_ini": root / "mt5" / f"{token}_ta_oos.ini",
            "source_note": f"Stage56 run50BN {anchor} source, reused only as v2-native research input.",
        }
    return specs


def configure_reused_engine() -> None:
    engine.STAGE59_ID = STAGE_ID
    engine.NEXT_REPAIR_STAGE_ID = NEXT_STAGE_ID
    engine.RUN_NUMBER = RUN_NUMBER
    engine.RUN_ID = RUN_ID
    engine.PACKET_ID = PACKET_ID
    engine.PARENT_RUN_ID = PARENT_RUN_ID
    engine.SOURCE_ADAPTER_ID = SOURCE_ADAPTER_ID
    engine.DEVELOPMENT_ANCHOR = "run50BN_v42_v45_source_family"
    engine.BACKUP_ANCHOR = "none"
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
    engine.STAGE59_VARIANTS = VARIANTS
    engine.SOURCE_SPECS = source_specs()
    engine.MODEL_RISK_MIN_PCT = {variant.adapter_id: 0.005 for variant in VARIANTS}

    repair.STAGE_ID = STAGE_ID
    repair.RUN_NUMBER = RUN_NUMBER
    repair.RUN_ID = RUN_ID
    repair.RUN_ROOT = RUN_ROOT
    repair.REPAIR_VARIANTS = VARIANTS
    s58.STAGE58_ID = STAGE_ID
    s58.RUN_NUMBER = RUN_NUMBER
    s58.RUN_ID = RUN_ID
    s58.PACKET_ID = PACKET_ID
    s58.PARENT_RUN_ID = PARENT_RUN_ID
    s58.RUN_ROOT = RUN_ROOT
    s58.REVIEWS_ROOT = REVIEWS_ROOT
    s58.STAGE58_VARIANTS = VARIANTS
    s58.COMMON_ROOT = COMMON_ROOT


def build_attempts(inputs: Mapping[str, Any]) -> list[dict[str, Any]]:
    attempts: list[dict[str, Any]] = []
    for variant_index, variant in enumerate(VARIANTS, start=1):
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
                magic = 13013000 + variant_index * 100 + (1 if split == "validation_is" else 50) + role_index
                attempts.append(
                    attempt_payload(
                        run_root=variant_root,
                        run_id=RUN_ID,
                        stage_number=130,
                        exploration_label="stage130_BaselineAdapter__NewV2ModelBranchAfterV41TradeoffFailure",
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
    return execute_prepared_run(
        prepared,
        terminal_path=Path(args.terminal_path),
        metaeditor_path=Path(args.metaeditor_path),
        terminal_data_root=Path(args.terminal_data_root),
        common_files_root=Path(args.common_files_root),
        tester_profile_root=Path(args.tester_profile_root),
        timeout_seconds=int(args.timeout_seconds),
    )


def load_existing_result() -> dict[str, Any]:
    manifest = RUN_ROOT / "run_manifest.json"
    kpi = RUN_ROOT / "kpi_record.json"
    if not path_exists(manifest) or not path_exists(kpi):
        raise FileNotFoundError("Stage130 existing run_manifest.json or kpi_record.json is missing")
    payload = json.loads(io_path(manifest).read_text(encoding="utf-8-sig"))
    payload.update(json.loads(io_path(kpi).read_text(encoding="utf-8-sig")))
    return payload


def best_variant(summary_rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    return engine.best_repaired_variant(summary_rows)


def failure_reasons(summary_rows: Sequence[Mapping[str, Any]], segment_rows: Sequence[Mapping[str, Any]], external: str) -> list[str]:
    if external != "completed":
        return ["mt5_external_verification_not_completed"]
    reasons = list(engine.repair_failure_reasons(summary_rows, segment_rows))
    best = best_variant(summary_rows)
    val = best.get("validation") if isinstance(best.get("validation"), Mapping) else {}
    oos = best.get("oos") if isinstance(best.get("oos"), Mapping) else {}
    val_net = s58.as_float(val.get("net_profit"), 0.0) or 0.0
    oos_net = s58.as_float(oos.get("net_profit"), 0.0) or 0.0
    val_pf = s58.as_float(val.get("profit_factor"), 0.0) or 0.0
    oos_pf = s58.as_float(oos.get("profit_factor"), 0.0) or 0.0
    if val_net < LEGACY_34D["net_profit"]:
        reasons.append("validation_net_below_legacy_34d_target")
    if val_pf < LEGACY_34D["profit_factor"]:
        reasons.append("validation_pf_below_legacy_34d_target")
    if oos_net <= 0.0 or oos_pf < 1.10:
        reasons.append("oos_not_strong_enough_for_confirmation")
    return sorted(set(reasons))


def decide(summary_rows: Sequence[Mapping[str, Any]], segment_rows: Sequence[Mapping[str, Any]], external: str) -> str:
    reasons = failure_reasons(summary_rows, segment_rows, external)
    if not reasons:
        return "proceed_to_stage131_new_branch_confirmation"
    return "continue_new_v2_model_branch_repair_in_stage131_due_to_34d_gap"


def metric(row: Mapping[str, Any], key: str) -> float:
    return s58.as_float(row.get(key), 0.0) or 0.0


def line_table(summary_rows: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        "| adapter(어댑터) | split(구간) | PF(수익 팩터) | net(순손익) | DD%(드로다운 비율) | trades(거래 수) | 34D net gap(34D 순손익 차이) |",
        "|---|---|---:|---:|---:|---:|---:|",
    ]
    for row in summary_rows:
        if row.get("view") != "actual_routed_total":
            continue
        net = metric(row, "net_profit")
        lines.append(
            "| {adapter} | {split} | {pf:.2f} | {net:.2f} | {dd:.2f} | {trades:.0f} | {gap:.2f} |".format(
                adapter=row.get("adapter_id", ""),
                split=row.get("split", ""),
                pf=metric(row, "profit_factor"),
                net=net,
                dd=metric(row, "max_drawdown_percent"),
                trades=metric(row, "trade_count"),
                gap=net - LEGACY_34D["net_profit"],
            )
        )
    return "\n".join(lines)


def report_markdown(summary_rows: Sequence[Mapping[str, Any]], segment_rows: Sequence[Mapping[str, Any]], decision: str, external: str) -> str:
    best = best_variant(summary_rows)
    reasons = failure_reasons(summary_rows, segment_rows, external)
    return f"""# Stage130 New V2 Model Branch Report(130단계 새 v2 모델 분기 보고서)

- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- external_verification_status(외부 검증 상태): `{external}`
- decision(판정): `{decision}`
- boundary(주장 경계): `{BOUNDARY}`

## Bounded Question(경계 질문)

Can unused run50BN v42-v45 v2 source families(미사용 run50BN v42-v45 v2 원천 계열)가 failed v41 quality-density surface(실패한 v41 품질-밀도 표면)보다 나은 새 BaselineAdapter(기준선 어댑터) 분기 후보가 될 수 있는가?

## KPI Table(KPI 표)

{line_table(summary_rows)}

## Read(판독)

- best_candidate(최선 후보): `{best.get("adapter_id", "none")}`
- failure_or_gap_reasons(실패 또는 차이 이유): `{";".join(reasons) if reasons else "none"}`
- segment_kpi_summary(구간 KPI 요약): `{rel(SEGMENT_KPI_PATH)}`
- equity_curve_audit(자금 곡선 감사): `{rel(EQUITY_AUDIT_PATH)}`
- risk_atr_telemetry(위험/ATR 원격측정): `{rel(RISK_ATR_TELEMETRY_PATH)}`

Effect(효과): Stage130(130단계)은 새 v2 원천 계열을 같은 ATR SL/TP(ATR 손절/익절)와 model-controlled risk%(모델 제어 위험 비율) 조건에서 비교했다. 이 단계 종료는 전체 목표 완료가 아니며, deployment(배포), live readiness(실거래 준비), runtime authority(런타임 권위)를 뜻하지 않는다.
"""


def decision_markdown(summary_rows: Sequence[Mapping[str, Any]], segment_rows: Sequence[Mapping[str, Any]], decision: str, external: str) -> str:
    best = best_variant(summary_rows)
    reasons = failure_reasons(summary_rows, segment_rows, external)
    return f"""# Stage130 Decision(130단계 판정)

decision(판정): `{decision}`

Stage130(130단계)는 v41 surface(브이41 표면) 수리를 중단하고 run50BN v42-v45 source family(run50BN v42-v45 원천 계열)를 새 v2-native branch(브이투 고유 분기) 후보로 측정했다. Effect(효과): 성공/실패를 숨기지 않고 Stage131(131단계) 입력으로 넘긴다.

## Evidence(근거)

- report(보고서): `{rel(REPORT_PATH)}`
- summary_json(요약 JSON): `{rel(SUMMARY_JSON_PATH)}`
- summary_csv(요약 CSV): `{rel(SUMMARY_CSV_PATH)}`
- segment_kpi(구간 KPI): `{rel(SEGMENT_KPI_PATH)}`
- equity_audit(자금 곡선 감사): `{rel(EQUITY_AUDIT_PATH)}`
- risk_atr_telemetry(위험/ATR 원격측정): `{rel(RISK_ATR_TELEMETRY_PATH)}`
- external_verification_status(외부 검증 상태): `{external}`

## Reason(이유)

- best_candidate(최선 후보): `{best.get("adapter_id", "none")}`
- failure_or_gap_reasons(실패 또는 차이 이유): `{";".join(reasons) if reasons else "none"}`

## Next(다음)

next_stage_or_branch(다음 단계/분기): `{NEXT_STAGE_ID}`

Stage130 closeout(130단계 종료)는 overall goal completion(전체 목표 완료)이 아니다. Effect(효과): 34D KPI(34D 핵심 성과 지표) 차이를 계속 줄이기 위해 Stage131(131단계)로 넘긴다.

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), overall goal complete(전체 목표 완료).
"""


def equity_audit_markdown(summary_rows: Sequence[Mapping[str, Any]], segment_rows: Sequence[Mapping[str, Any]]) -> str:
    flagged = [
        row
        for row in segment_rows
        if row.get("quality_flag") and row.get("quality_flag") != "acceptable_measurement_only"
    ]
    lines = [
        "# Stage130 Equity Curve Audit(130단계 자금 곡선 감사)",
        "",
        f"- flagged_segment_rows(표시된 구간 행): `{len(flagged)}`",
        "- read(판독): final net(최종 순손익)만 보지 않고 validation/OOS(검증/미래구간), drawdown(드로다운), cost expectancy(비용 기대값), MFE/MAE(최대 유리/불리 이동)를 같이 본다.",
        "- effect(효과): 한 번의 spike(급등)나 late flatline(후반 정체)에 기대는 후보를 Stage131(131단계)에서 다시 압박한다.",
        "",
    ]
    for row in flagged[:30]:
        lines.append(
            f"- `{row.get('adapter_id')}` `{row.get('split')}` `{row.get('segment_type')}` `{row.get('segment')}`: `{row.get('quality_flag')}`"
        )
    return "\n".join(lines) + "\n"


def write_run_identity(result: Mapping[str, Any]) -> None:
    variant_payload = [
        {
            **variant.__dict__,
            "source_anchor": engine.source_anchor_for_variant(variant),
            "signal_column": engine.signal_column_for_variant(variant),
            "feature_order_hash": engine.feature_order_hash_for_variant(variant),
        }
        for variant in VARIANTS
    ]
    write_json(
        RUN_ROOT / "run_manifest.json",
        {
            "run_id": RUN_ID,
            "packet_id": PACKET_ID,
            "stage_id": STAGE_ID,
            "stage_number": 130,
            "run_number": RUN_NUMBER,
            "bounded_question": "Can unused run50BN v42-v45 v2 source families produce a better new BaselineAdapter branch than the failed v41 quality-density surface?",
            "source_stage129_decision": rel(SOURCE_STAGE129_DECISION),
            "source_stage129_closeout_commit": SOURCE_STAGE129_CLOSEOUT_COMMIT,
            "source_stage129_latest_commit": SOURCE_STAGE129_LATEST_COMMIT,
            "target_surface": TARGET_SURFACE,
            "variants": variant_payload,
            "attempts": result.get("attempts", []),
            "common_copies": result.get("common_copies", []),
            "compile": result.get("compile", {}),
            "external_verification_status": result.get("external_verification_status"),
            "judgment": result.get("judgment"),
            "claim_boundary": BOUNDARY,
            "overall_goal_complete": False,
        },
    )
    write_json(
        RUN_ROOT / "kpi_record.json",
        {
            "run_id": RUN_ID,
            "packet_id": PACKET_ID,
            "stage_id": STAGE_ID,
            "mt5_kpi_records": result.get("mt5_kpi_records", []),
            "strategy_tester_reports": result.get("strategy_tester_reports", []),
            "execution_results": result.get("execution_results", []),
            "external_verification_status": result.get("external_verification_status"),
            "judgment": result.get("judgment"),
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
    rows: list[dict[str, Any]] = []
    for path in paths:
        if path_exists(path):
            rows.append(
                {
                    "artifact_id": f"{RUN_ID}__{path.name}",
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "artifact_type": "stage130_new_v2_model_branch_evidence",
                    "path": rel(path),
                    "sha256": sha256_file_lf_normalized(path),
                    "hash_policy": "lf_normalized_text" if path.suffix.lower() in {".csv", ".json", ".md"} else "raw_file",
                    "created_at_utc": created,
                    "notes": "Stage130 bounded new v2 model branch artifact.",
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
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "artifact_type": "mt5_strategy_tester_report",
                    "path": rel(report_path),
                    "sha256": sha256_file_lf_normalized(report_path),
                    "hash_policy": "raw_file",
                    "created_at_utc": created,
                    "notes": "Actual Stage130 MT5 Strategy Tester HTML report.",
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
    best = best_variant(summary_rows)
    val = best.get("validation") if isinstance(best.get("validation"), Mapping) else {}
    oos = best.get("oos") if isinstance(best.get("oos"), Mapping) else {}
    status = "completed" if external == "completed" else "blocked"
    run_payload = upsert_csv_rows_retry(
        RUN_REGISTRY_PATH,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "baseline_adapter_new_v2_model_branch",
                "status": status,
                "judgment": decision,
                "path": rel(DECISION_PATH),
                "notes": ledger_pairs(
                    (
                        ("target_surface", TARGET_SURFACE),
                        ("best_candidate", best.get("adapter_id")),
                        ("validation_net", val.get("net_profit")),
                        ("oos_net", oos.get("net_profit")),
                        ("boundary", BOUNDARY),
                    )
                ),
            }
        ],
        key="run_id",
    )
    ledger_rows = build_mt5_alpha_ledger_rows(
        run_id=RUN_ID,
        stage_id=STAGE_ID,
        mt5_kpi_records=result.get("mt5_kpi_records", []),
        run_output_root=RUN_ROOT,
        external_verification_status=external,
    )
    ledger_rows.append(
        {
            "ledger_row_id": f"{RUN_ID}__aggregate_new_v2_model_branch",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "aggregate_new_v2_model_branch",
            "parent_run_id": PARENT_RUN_ID,
            "record_view": "new_v2_model_branch",
            "tier_scope": "Tier A+B",
            "kpi_scope": "baseline_adapter_research",
            "scoreboard_lane": "runtime_probe",
            "status": status,
            "judgment": decision,
            "path": rel(DECISION_PATH),
            "primary_kpi": ledger_pairs(
                (
                    ("best_candidate", best.get("adapter_id")),
                    ("validation_net", val.get("net_profit")),
                    ("oos_net", oos.get("net_profit")),
                    ("validation_pf", val.get("profit_factor")),
                    ("oos_pf", oos.get("profit_factor")),
                )
            ),
            "guardrail_kpi": ledger_pairs(
                (
                    ("failure_reasons", failure_reasons(summary_rows, segment_rows, external)),
                    ("atr_sltp", "measured"),
                    ("model_controlled_risk_pct", "measured"),
                    ("overall_goal_complete", False),
                )
            ),
            "external_verification_status": external,
            "notes": "Stage130 bounded v2-native branch; not final package completion.",
        }
    )
    stage_payload = upsert_csv_rows_retry(STAGE_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, ledger_rows, key="ledger_row_id")
    project_payload = upsert_csv_rows_retry(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, ledger_rows, key="ledger_row_id")
    artifact_payload = upsert_csv_rows_retry(ARTIFACT_REGISTRY_PATH, aw.ARTIFACT_COLUMNS, list(artifacts), key="artifact_id")
    return {"run_registry": run_payload, "stage_ledger": stage_payload, "project_alpha_ledger": project_payload, "artifact_registry": artifact_payload}


def write_required_outputs(
    result: Mapping[str, Any],
    summary_rows: Sequence[Mapping[str, Any]],
    risk_rows: Sequence[Mapping[str, Any]],
    segment_rows: Sequence[Mapping[str, Any]],
    decision: str,
    ledger_payload: Mapping[str, Any],
) -> None:
    external = str(result.get("external_verification_status") or "blocked")
    reasons = failure_reasons(summary_rows, segment_rows, external)
    best = best_variant(summary_rows)
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
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "packet_id": PACKET_ID,
            "target_surface": TARGET_SURFACE,
            "source_stage129_decision": rel(SOURCE_STAGE129_DECISION),
            "source_stage129_closeout_commit": SOURCE_STAGE129_CLOSEOUT_COMMIT,
            "source_stage129_latest_commit": SOURCE_STAGE129_LATEST_COMMIT,
            "variants": [
                {
                    **variant.__dict__,
                    "source_anchor": engine.source_anchor_for_variant(variant),
                    "signal_column": engine.signal_column_for_variant(variant),
                    "feature_order_hash": engine.feature_order_hash_for_variant(variant),
                }
                for variant in VARIANTS
            ],
            "legacy_34d_target": LEGACY_34D,
            "external_verification_status": external,
            "decision": decision,
            "best_candidate": best,
            "failure_or_gap_reasons": reasons,
            "required_outputs": {
                "report": rel(REPORT_PATH),
                "summary_json": rel(SUMMARY_JSON_PATH),
                "summary_csv": rel(SUMMARY_CSV_PATH),
                "segment_kpi_summary": rel(SEGMENT_KPI_PATH),
                "equity_curve_audit": rel(EQUITY_AUDIT_PATH),
                "risk_atr_telemetry": rel(RISK_ATR_TELEMETRY_PATH),
                "stage130_decision": rel(DECISION_PATH),
            },
            "ledger_payload": ledger_payload,
            "claim_boundary": BOUNDARY,
            "overall_goal_complete": False,
        },
    )


def write_packet_files(
    result: Mapping[str, Any],
    summary_rows: Sequence[Mapping[str, Any]],
    segment_rows: Sequence[Mapping[str, Any]],
    risk_rows: Sequence[Mapping[str, Any]],
    decision: str,
    ledger_payload: Mapping[str, Any],
) -> None:
    external = str(result.get("external_verification_status") or "blocked")
    reasons = failure_reasons(summary_rows, segment_rows, external)
    best = best_variant(summary_rows)
    files = {
        "routing_receipt.json": {
            "packet_id": PACKET_ID,
            "primary_family": "adapter_development",
            "primary_skill": "obsidian-model-validation",
            "support_skills": ["obsidian-backtest-forensics", "obsidian-performance-attribution", "obsidian-result-judgment"],
            "required_gates": [
                "experiment_design_receipt",
                "runtime_evidence_gate",
                "kpi_contract_audit",
                "result_judgment_gate",
                "artifact_lineage_audit",
                "final_claim_guard",
            ],
            "status": "completed",
        },
        "experiment_design_receipt.json": {
            "hypothesis": "Unused run50BN v42-v45 v2 source families may produce a better BaselineAdapter branch after v41 quality-density tradeoff failure.",
            "decision_use": "route the branch to Stage131 confirmation or repair; do not claim deployment or final package completion.",
            "comparison_baseline": "Stage129 failure memory and legacy 34D KPI target as lesson-only measurement surface.",
            "control_variables": ["US100", "M5", "split_v1", "Tier B disabled at runtime", "wide ATR bracket", "3% model-controlled risk cap", "ONNX deferred"],
            "changed_variables": ["run50BN source family v42", "run50BN source family v43", "run50BN source family v44", "run50BN source family v45"],
            "success_criteria": ["validation PF/net reaches 34D target", "OOS remains positive and credible", "ATR/risk telemetry present", "no severe segment flags"],
            "failure_criteria": ["34D KPI gap remains", "OOS weak or damaged", "risk/ATR telemetry missing", "segment instability remains"],
            "stop_condition": "four bounded source-family variants only",
            "status": "completed",
        },
        "runtime_evidence_gate.json": {"external_verification_status": external, "mt5_reports": result.get("strategy_tester_reports", []), "status": external},
        "kpi_contract_audit.json": {"summary_rows": len(summary_rows), "segment_rows": len(segment_rows), "risk_rows": len(risk_rows), "status": "completed"},
        "result_judgment_gate.json": {
            "result_subject": RUN_ID,
            "judgment_label": decision,
            "failure_or_gap_reasons": reasons,
            "best_candidate": best.get("adapter_id", "none"),
            "claim_boundary": BOUNDARY,
            "status": "passed_with_boundary",
        },
        "artifact_lineage_audit.json": {
            "source_inputs": [rel(SOURCE_STAGE129_DECISION), rel(SOURCE_STAGE129_REPORT), rel(SOURCE_STAGE129_GAP), rel(RUN50BN_SUMMARY), rel(RUN50BN_AUDIT), rel(RUN50BN_SOURCE_SUMMARY), rel(RUN50BN_MODEL)],
            "consumers": [rel(REPORT_PATH), rel(DECISION_PATH), rel(SUMMARY_JSON_PATH)],
            "ledger_links": ledger_payload,
        },
        "final_claim_guard.json": {
            "overall_goal_complete": False,
            "deployment_claim": False,
            "live_readiness_claim": False,
            "runtime_authority_claim": False,
            "production_baseline_claim": False,
            "operating_reference_claim": False,
            "operating_promotion_claim": False,
            "status": "passed",
        },
        "required_gate_coverage_audit.json": {
            "required_gates": [
                "experiment_design_receipt",
                "runtime_evidence_gate",
                "kpi_contract_audit",
                "result_judgment_gate",
                "artifact_lineage_audit",
                "final_claim_guard",
            ],
            "covered_by": [
                "experiment_design_receipt.json",
                "runtime_evidence_gate.json",
                "kpi_contract_audit.json",
                "result_judgment_gate.json",
                "artifact_lineage_audit.json",
                "final_claim_guard.json",
            ],
            "status": "completed",
        },
        "aggregate_summary.json": {
            "packet_id": PACKET_ID,
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "decision": decision,
            "external_verification_status": external,
            "best_candidate": best.get("adapter_id", "none"),
            "required_outputs": {
                "report": rel(REPORT_PATH),
                "summary_json": rel(SUMMARY_JSON_PATH),
                "summary_csv": rel(SUMMARY_CSV_PATH),
                "segment_kpi_summary": rel(SEGMENT_KPI_PATH),
                "equity_curve_audit": rel(EQUITY_AUDIT_PATH),
                "risk_atr_telemetry": rel(RISK_ATR_TELEMETRY_PATH),
                "stage130_decision": rel(DECISION_PATH),
            },
            "claim_boundary": BOUNDARY,
            "overall_goal_complete": False,
        },
    }
    for name, payload in files.items():
        write_json(PACKET_ROOT / name, payload)


def write_stage_docs(decision: str) -> None:
    write_md(
        SPEC_ROOT / "stage_brief.md",
        f"""# {STAGE_ID}

Stage130(130단계)는 Stage129(129단계) 판정대로 current v41 surface(현재 브이41 표면) 수리를 멈추고 새 v2-native model branch(브이투 고유 모델 분기)를 측정했다.

## Bounded Question(경계 질문)

Unused run50BN v42-v45 v2 source families(미사용 run50BN v42-v45 v2 원천 계열)가 failed v41 quality-density surface(실패한 v41 품질-밀도 표면)보다 나은 새 BaselineAdapter(기준선 어댑터) 분기 후보가 될 수 있는가?

Effect(효과): Stage130(130단계)는 source family(원천 계열)만 바꿔 같은 ATR/risk(ATR/위험) 껍질에서 비교하고, 수리나 최종화는 Stage131(131단계)로 넘긴다.

## Boundary(경계)

`{BOUNDARY}`
""",
    )
    write_md(
        INPUT_ROOT / "input_refs.md",
        f"""# Stage130 Input References(130단계 입력 참조)

- source_stage129_decision(129단계 원천 판정): `{rel(SOURCE_STAGE129_DECISION)}`
- source_stage129_report(129단계 보고서): `{rel(SOURCE_STAGE129_REPORT)}`
- source_stage129_gap(129단계 34D 차이): `{rel(SOURCE_STAGE129_GAP)}`
- source_stage129_closeout_commit(129단계 종료 커밋): `{SOURCE_STAGE129_CLOSEOUT_COMMIT}`
- source_stage129_latest_commit(129단계 최신 커밋): `{SOURCE_STAGE129_LATEST_COMMIT}`
- run50BN_summary(run50BN 요약): `{rel(RUN50BN_SUMMARY)}`
- run50BN_audit(run50BN 감사): `{rel(RUN50BN_AUDIT)}`
- run50BN_source_summary(run50BN 원천 요약): `{rel(RUN50BN_SOURCE_SUMMARY)}`
- run50BN_model(run50BN 모델): `{rel(RUN50BN_MODEL)}`

Effect(효과): 레거시 34D(legacy 34D, 레거시 34D)는 lesson-only KPI target(교훈 전용 핵심 성과 지표 목표)로만 쓰고, 입력은 v2 산출물로 제한한다.
""",
    )
    write_md(
        SELECTED_ROOT / "selection_status.md",
        f"""# Stage130 Selection Status(130단계 선택 상태)

- stage_status(단계 상태): `closed_bounded_new_v2_model_branch`
- current_packet(현재 작업 묶음): `{PACKET_ID}`
- current_run(현재 실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE129_ID}`
- source_decision(원천 판정): `open_new_v2_model_branch_in_stage130_after_v41_quality_density_tradeoff_failure`
- stage130_decision(130단계 판정): `{decision}`
- next_stage_or_branch(다음 단계/분기): `{NEXT_STAGE_ID}`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- selected_research_baseline(선택 연구 기준): `none`
- claim_boundary(주장 경계): `{BOUNDARY}`

Effect(효과): Stage130(130단계)는 근거를 보존하고, 34D KPI(34D 핵심 성과 지표) 차이는 Stage131(131단계)에서 계속 줄인다.
""",
    )
    write_md(
        REVIEWS_ROOT / "review_index.md",
        f"""# Stage130 Review Index(130단계 검토 색인)

- report(보고서): `{rel(REPORT_PATH)}`
- summary_json(요약 JSON): `{rel(SUMMARY_JSON_PATH)}`
- summary_csv(요약 CSV): `{rel(SUMMARY_CSV_PATH)}`
- segment_kpi(구간 KPI): `{rel(SEGMENT_KPI_PATH)}`
- equity_curve_audit(자금 곡선 감사): `{rel(EQUITY_AUDIT_PATH)}`
- risk_atr_telemetry(위험/ATR 원격측정): `{rel(RISK_ATR_TELEMETRY_PATH)}`
- decision(판정): `{rel(DECISION_PATH)}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "00_spec/stage_brief.md",
        f"""# {NEXT_STAGE_ID}

Stage131(131단계)는 Stage130(130단계)의 새 v2 source branch(브이투 원천 분기) 결과를 보고 후속 수리 또는 확인을 좁게 진행한다.

## Bounded Question(경계 질문)

Stage130(130단계) best candidate(최선 후보)를 34D KPI(34D 핵심 성과 지표)에 더 가깝게 만들 수 있는 최소한의 bounded repair(경계 수리) 또는 confirmation(확인)은 무엇인가?

Effect(효과): Stage131(131단계)는 Stage130(130단계)을 반복하지 않고, 최선 후보의 차이만 좁게 줄인다.

## Boundary(경계)

`{BOUNDARY}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "01_inputs/input_refs.md",
        f"""# Stage131 Input References(131단계 입력 참조)

- stage130_decision(130단계 판정): `{rel(DECISION_PATH)}`
- stage130_report(130단계 보고서): `{rel(REPORT_PATH)}`
- stage130_summary(130단계 요약): `{rel(SUMMARY_CSV_PATH)}`
- stage130_segment_kpi(130단계 구간 KPI): `{rel(SEGMENT_KPI_PATH)}`
- stage130_risk_atr_telemetry(130단계 위험/ATR 원격측정): `{rel(RISK_ATR_TELEMETRY_PATH)}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "03_reviews/review_index.md",
        """# Stage131 Review Index(131단계 검토 색인)

Stage131(131단계)는 planned(계획) 상태다. Effect(효과): Stage130(130단계) 결과를 다음 bounded repair(경계 수리) 입력으로 연결한다.
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "04_selected/selection_status.md",
        f"""# Stage131 Selection Status(131단계 선택 상태)

- stage_status(단계 상태): `active_planned_from_stage130`
- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- source_stage(원천 단계): `{STAGE_ID}`
- source_decision(원천 판정): `{decision}`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- selected_research_baseline(선택 연구 기준): `none`
- claim_boundary(주장 경계): `{BOUNDARY}`
""",
    )


def update_current_truth(decision: str, summary_rows: Sequence[Mapping[str, Any]], external: str) -> None:
    best = best_variant(summary_rows)
    val = best.get("validation") if isinstance(best.get("validation"), Mapping) else {}
    oos = best.get("oos") if isinstance(best.get("oos"), Mapping) else {}
    current_state = f"""# Current Working State(현재 작업 상태)

- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- active_stage(활성 단계): `{NEXT_STAGE_ID}`
- selected_research_baseline(선택 연구 기준): `none`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- adapter_under_review(검토 중 어댑터): `stage131_followup_from_{best.get("adapter_id", "stage130_none")}`
- status(상태): `stage130_closed_{decision}_stage131_open_planned`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage130(130단계)는 run50BN v42-v45 source family(run50BN v42-v45 원천 계열)를 같은 ATR/risk(ATR/위험) 조건에서 측정하고 종료했다. Effect(효과): v41 surface(브이41 표면) 수리를 계속하지 않고, best candidate(최선 후보)를 Stage131(131단계) 입력으로 넘긴다.

## Latest Stage130 Evidence(최신 130단계 근거)

- run(실행): `{RUN_ID}`
- decision(판정): `{decision}`
- external_verification_status(외부 검증 상태): `{external}`
- best_candidate(최선 후보): `{best.get("adapter_id", "none")}`
- validation_pf_net(검증 수익팩터/순손익): `{val.get("profit_factor", "")}` / `{val.get("net_profit", "")}`
- oos_pf_net(미래구간 수익팩터/순손익): `{oos.get("profit_factor", "")}` / `{oos.get("net_profit", "")}`
- report(보고서): `{rel(REPORT_PATH)}`
- summary(요약): `{rel(SUMMARY_CSV_PATH)}`
- decision_path(판정 경로): `{rel(DECISION_PATH)}`

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준선), legacy_inheritance(레거시 상속), overall_goal_complete(전체 목표 완료).
"""
    write_md(CURRENT_WORKING_STATE_PATH, current_state)

    if path_exists(WORKSPACE_STATE_PATH):
        text = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    else:
        text = ""
    text = re.sub(r"^current_run_id:.*$", f"current_run_id: {NEXT_RUN_ID}", text, count=1, flags=re.MULTILINE)
    text = re.sub(r"^active_stage:.*$", f"active_stage: {NEXT_STAGE_ID}", text, count=1, flags=re.MULTILINE)
    focus = f"""current_focus:
- >-
  Stage130(130단계) closed(종료) as `{decision}` and Stage131(131단계) `{NEXT_STAGE_ID}` is active_planned(활성 계획). Effect(효과): 새 v2 source branch(브이투 원천 분기)의 best candidate(최선 후보)를 34D KPI(34D 핵심 성과 지표) 차이 축소 작업으로 넘긴다.
- >-
  Stage130 evidence(130단계 근거)는 `{rel(REPORT_PATH)}`, `{rel(SUMMARY_CSV_PATH)}`, `{rel(SEGMENT_KPI_PATH)}`에 있다. Effect(효과): KPI(핵심 성과 지표), segment(구간), risk/ATR telemetry(위험/ATR 원격측정)를 한 묶음으로 추적한다.
- >-
  Target surface(목표 표면)는 `{TARGET_SURFACE}`이고 legacy 34D(레거시 34D)는 lesson-only KPI target(교훈 전용 핵심 성과 지표 목표)이다. Effect(효과): v2-native research(브이투 고유 연구)만 계속한다.

"""
    if re.search(r"(?ms)^current_focus:\r?\n.*?(?=\r?\nstage\d+_)", text):
        text = re.sub(r"(?ms)^current_focus:\r?\n.*?(?=\r?\nstage\d+_)", focus, text, count=1)
    else:
        text = text.rstrip() + "\n" + focus
    block = f"""
stage130_new_v2_model_branch_after_v41_tradeoff_failure:
  packet_id: {PACKET_ID}
  stage_id: {STAGE_ID}
  status: closed_bounded_new_v2_model_branch
  current_run_id: {RUN_ID}
  source_stage: {SOURCE_STAGE129_ID}
  decision: {decision}
  report_path: {rel(REPORT_PATH)}
  decision_path: {rel(DECISION_PATH)}
  next_action: {NEXT_RUN_ID}
  boundary: {BOUNDARY}

stage131_new_v2_model_branch_followup_review:
  packet_id: {NEXT_PACKET_ID}
  stage_id: {NEXT_STAGE_ID}
  status: active_planned_from_stage130
  current_run_id: {NEXT_RUN_ID}
  source_stage: {STAGE_ID}
  source_decision: {decision}
  next_action: run_stage131_bounded_followup
  boundary: {BOUNDARY}
"""
    text = re.sub(r"(?ms)\nstage130_new_v2_model_branch_after_v41_tradeoff_failure:.*?(?=\nstage\d+_|$)", "\n", text)
    text = re.sub(r"(?ms)\nstage131_new_v2_model_branch_followup_review:.*?(?=\nstage\d+_|$)", "\n", text)
    text = text.rstrip() + "\n" + block
    io_path(WORKSPACE_STATE_PATH).write_text(text, encoding="utf-8-sig")


def append_changelog(decision: str) -> None:
    entry = (
        f"\n## {utc_now()} Stage130 new v2 model branch closeout(130단계 새 v2 모델 분기 종료)\n\n"
        f"- action(행동): closed(종료) `{STAGE_ID}` with decision(판정) `{decision}`.\n"
        f"- effect(효과): v42-v45 v2 source families(v42-v45 v2 원천 계열) evidence(근거)를 보존하고 Stage131(131단계)로 넘겼다.\n"
        f"- boundary(주장 경계): `{BOUNDARY}`.\n"
    )
    existing = io_path(CHANGELOG_PATH).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG_PATH) else ""
    io_path(CHANGELOG_PATH).write_text(existing.rstrip() + entry, encoding="utf-8-sig")


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Stage130 bounded new v2 model branch after v41 tradeoff failure.")
    parser.add_argument("--terminal-path", default=str(TERMINAL_PATH_DEFAULT))
    parser.add_argument("--metaeditor-path", default=str(METAEDITOR_PATH_DEFAULT))
    parser.add_argument("--terminal-data-root", default=str(TERMINAL_DATA_ROOT_DEFAULT))
    parser.add_argument("--common-files-root", default=str(COMMON_FILES_ROOT_DEFAULT))
    parser.add_argument("--tester-profile-root", default=str(TESTER_PROFILE_ROOT_DEFAULT))
    parser.add_argument("--timeout-seconds", type=int, default=900)
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
            "stage_id": STAGE_ID,
            "stage_number": 130,
            "run_number": RUN_NUMBER,
            "run_root": RUN_ROOT,
            "packet_id": PACKET_ID,
            "attempts": attempts,
            "common_copies": inputs["common_copies"],
            "feature_exports": inputs["feature_exports"],
            "model_artifacts": inputs["model_exports"],
            "route_coverage": engine.route_coverage(),
            "model_family": "baseline_adapter_stage130_run50bn_v42_v45_source_branch_ebm_table",
            "feature_set_id": "stage130_run50bn_v42_v45_source_family_discrete_signal",
            "label_id": "label_v1_fwd12_m5_logret_train_q33_3class",
            "split_contract": "split_v1_calendar_train_20220901_20241231_val_20250101_20250930_oos_20251001_20260413",
            "claim_boundary": BOUNDARY,
            "overall_goal_complete": False,
        }
        result = execute_or_materialize(prepared, args)
    audit_rows = s58.audit_rows_for_result(result, float(args.cost_stress_per_trade)) if result.get("mt5_kpi_records") else []
    risk_rows = s58.risk_rows_from_result(result)
    summary_rows = s58.build_summary_rows(result, audit_rows, risk_rows)
    segment_rows = s58.segment_kpi_rows(summary_rows)
    external = str(result.get("external_verification_status") or "blocked")
    decision = decide(summary_rows, segment_rows, external)
    write_run_identity(result)
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
                    "best_candidate": best_variant(summary_rows),
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
