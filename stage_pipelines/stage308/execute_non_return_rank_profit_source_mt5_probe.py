from __future__ import annotations

import csv
import hashlib
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.models.onnx_bridge import ordered_hash  # noqa: E402
from stage_pipelines.stage298 import execute_profit_scale_edge_amplification_mt5_probe as runner  # noqa: E402


STAGE_ID = "308_onnx_candidate_campaign__non_return_rank_profit_source_rebuild"
RUN_ID = "run308B_execute_non_return_rank_profit_source_mt5_probe_v1"
RUN_NUMBER = "run308B"
SOURCE_RUN_ID = "run308A_design_non_return_rank_profit_source_rebuild_packet_v1"
PARENT_RUN_ID = "run307C_review_post_trade_shape_scale_mt5_probe_v1"
STATUS_PREPARED = "prepared_non_return_rank_profit_source_mt5_probe_no_runtime_kpi"
UPDATED_ON = "2026-05-24"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_"
    "no_deployment_no_onnx_until_candidate_package_gate"
)
EXPLORATION_LABEL = "stage308_Model__NonReturnRankProfitSourceReplay"
SIGNAL_COLUMN = "run308b_route_signal"
FEATURE_ORDER = (SIGNAL_COLUMN,)
COMMON_ROOT = "Project_Obsidian_Prime_v2/stage308/run308B_non_return_rank_profit_source"

STAGE_ROOT = ROOT / "stages" / STAGE_ID
RUN308A = STAGE_ROOT / "02_runs" / "run308A"
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER
REVIEWS = STAGE_ROOT / "03_reviews"
SELECTED = STAGE_ROOT / "04_selected" / "selection_status.md"
REVIEW_INDEX = REVIEWS / "review_index.md"
STAGE_LEDGER = REVIEWS / "stage_run_ledger.csv"
FEATURE_DIR = RUN_ROOT / "features"
MODEL_DIR = RUN_ROOT / "models"
MT5_DIR = RUN_ROOT / "mt5"
MT5_QUEUE = RUN308A / "mt5_probe_queue.csv"
SOURCE_MANIFEST = RUN308A / "candidate_payload_manifest.csv"
SOURCE_RUN_MANIFEST = RUN308A / "run_manifest.json"
SOURCE_REPORT = REVIEWS / "run308A_materialization.md"
PRODUCER = Path("stage_pipelines/stage308/execute_non_return_rank_profit_source_mt5_probe.py")

ATTEMPT_SUMMARY = RUN_ROOT / "attempt_summary.csv"
RUNTIME_SUPPLY = RUN_ROOT / "runtime_supply_matrix.csv"
EXECUTION_RESULT = RUN_ROOT / "execution_result.json"
MT5_KPI_SUMMARY = RUN_ROOT / "mt5_kpi_summary.csv"
RUNTIME_PARITY_RECEIPT = RUN_ROOT / "runtime_parity_receipt.json"
RESULT_JUDGMENT = RUN_ROOT / "result_judgment.csv"
GATE_AUDIT = RUN_ROOT / "required_gate_coverage_audit.csv"
RUN_MANIFEST = RUN_ROOT / "run_manifest.json"
LINEAGE = RUN_ROOT / "artifact_lineage_receipt.json"
REPORT = REVIEWS / "run308B_mt5_probe.md"

RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"


def safe_upsert_rows(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]], key: str) -> None:
    base = runner.prev.e295.e294.base.base
    try:
        base.upsert_rows(path, columns, rows, key=key)
        return
    except OSError:
        pass
    target = base.io_path(path)
    existing: list[dict[str, str]] = []
    if base.path_exists(path):
        with target.open(newline="", encoding="utf-8-sig") as handle:
            existing = [dict(row) for row in csv.DictReader(handle)]
    new_keys = {str(row.get(key, "")) for row in rows}
    merged: list[dict[str, Any]] = [row for row in existing if str(row.get(key, "")) not in new_keys]
    merged.extend(dict(row) for row in rows)
    base.io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with target.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), extrasaction="ignore")
        writer.writeheader()
        for row in merged:
            writer.writerow({column: row.get(column, "") for column in columns})


def float_value(value: Any, default: float = 0.0) -> float:
    try:
        if value is None or str(value).strip() == "":
            return default
        return float(value)
    except Exception:
        return default


def extra_set_values(queue_row: Mapping[str, str]) -> dict[str, Any]:
    return {
        "InpFixedLot": float_value(queue_row.get("fixed_lot"), 0.10),
        "InpEntryTransitionOnly": False,
        "InpReentryCooldownBars": 0,
        "InpSameDirectionReentryCooldownBars": runner.prev.e295.e294.int_value(queue_row.get("same_direction_reentry_cooldown_bars"), 0),
        "InpAtrSltpEnabled": runner.prev.e295.e294.bool_value(queue_row.get("atr_sltp_enabled")),
        "InpAtrPeriod": runner.prev.e295.e294.int_value(queue_row.get("atr_period"), 14),
        "InpAtrStopMultiplier": float_value(queue_row.get("atr_stop_multiplier"), 0.0),
        "InpAtrTakeProfitMultiplier": float_value(queue_row.get("atr_take_profit_multiplier"), 0.0),
        "InpAtrMinStopPoints": float_value(queue_row.get("atr_min_stop_points"), 0.0),
        "InpAtrMaxStopPoints": float_value(queue_row.get("atr_max_stop_points"), 0.0),
        "InpAtrMinTakeProfitPoints": float_value(queue_row.get("atr_min_take_profit_points"), 0.0),
        "InpAtrMaxTakeProfitPoints": float_value(queue_row.get("atr_max_take_profit_points"), 0.0),
        "InpExitRiskOverlayEnabled": runner.prev.e295.e294.bool_value(queue_row.get("exit_risk_overlay_enabled")),
        "InpExitRiskCloseLongFeatureIndex": runner.prev.e295.e294.int_value(queue_row.get("exit_risk_close_long_feature_index"), -1),
        "InpExitRiskCloseShortFeatureIndex": runner.prev.e295.e294.int_value(queue_row.get("exit_risk_close_short_feature_index"), -1),
        "InpExitRiskCloseThreshold": float_value(queue_row.get("exit_risk_close_threshold"), 0.5),
        "InpExitRiskMinHoldBars": runner.prev.e295.e294.int_value(queue_row.get("exit_risk_min_hold_bars"), 0),
        "InpExitRiskMaxHoldFeatureIndex": runner.prev.e295.e294.int_value(queue_row.get("exit_risk_max_hold_feature_index"), -1),
        "InpModelRiskSizingEnabled": runner.prev.e295.e294.bool_value(queue_row.get("model_risk_sizing_enabled")),
        "InpModelRiskMinPct": float_value(queue_row.get("model_risk_min_pct"), 0.006),
        "InpModelRiskMaxPct": float_value(queue_row.get("model_risk_max_pct"), 0.020),
        "InpModelRiskConfidenceFloor": float_value(queue_row.get("model_risk_confidence_floor"), 0.54),
        "InpModelRiskConfidenceCeiling": float_value(queue_row.get("model_risk_confidence_ceiling"), 0.99),
        "InpModelRiskFallbackLot": float_value(queue_row.get("model_risk_fallback_lot"), 0.10),
    }


def attach_identity(attempt: dict[str, Any], queue_row: Mapping[str, str], max_hold: int, close_on_flat: bool, same_reentry: int) -> None:
    runner.prev.e295.e294.base.base.attach_attempt_identity(attempt, queue_row)
    attempt["stage308_branch_id"] = queue_row.get("materialized_branch_id", "")
    attempt["stage307_branch_id"] = queue_row.get("stage307_branch_id", "")
    attempt["stage306_branch_id"] = queue_row.get("stage306_branch_id", "")
    attempt["stage305_branch_id"] = queue_row.get("stage305_branch_id", "")
    attempt["stage303_branch_id"] = queue_row.get("stage303_branch_id", "")
    attempt["stage301_branch_id"] = queue_row.get("stage301_branch_id", "")
    attempt["stage293_branch_id"] = queue_row.get("stage293_branch_id", "")
    attempt["stage291_branch_id"] = queue_row.get("stage291_branch_id", "")
    attempt["stage290_branch_id"] = queue_row.get("stage290_branch_id", "")
    attempt["max_hold_bars"] = max_hold
    attempt["close_on_flat_signal"] = close_on_flat
    attempt["same_direction_reentry_cooldown_bars"] = same_reentry
    attempt["fixed_lot"] = queue_row.get("fixed_lot", "")
    attempt["atr_stop_multiplier"] = queue_row.get("atr_stop_multiplier", "")
    attempt["atr_take_profit_multiplier"] = queue_row.get("atr_take_profit_multiplier", "")
    attempt["model_risk_max_pct"] = queue_row.get("model_risk_max_pct", "")


def build_all_attempts(
    queue_rows: Sequence[Mapping[str, str]],
    feature_exports: Mapping[str, Any],
    split_frames: Mapping[str, Any],
    model_artifact: Mapping[str, Any],
    *,
    include_routed: bool,
) -> list[dict[str, Any]]:
    attempts: list[dict[str, Any]] = []
    model_name = Path(str(model_artifact["path"])).name
    feature_hash = ordered_hash(FEATURE_ORDER)
    for queue_row in queue_rows:
        materialized_id = str(queue_row["materialized_branch_id"])
        token = runner.prev.e295.e294.base.base.variant_token(queue_row, 44)
        max_hold = runner.prev.e295.e294.int_value(queue_row.get("max_hold_bars"), 4)
        close_on_flat = runner.prev.e295.e294.bool_value(queue_row.get("close_on_flat_signal"))
        same_reentry = runner.prev.e295.e294.int_value(queue_row.get("same_direction_reentry_cooldown_bars"), 0)
        extras = extra_set_values(queue_row)
        for runtime_split, split_token in (("validation_is", "val"), ("oos", "oos")):
            for tier_key, tier_label, tier_token in (
                ("tier_a", runner.prev.e295.e294.base.mt5.TIER_A, "tier_a"),
                ("tier_b", runner.prev.e295.e294.base.mt5.TIER_B, "tier_b"),
            ):
                key = f"{materialized_id}__{tier_key}__{runtime_split}"
                frame = split_frames[key]
                from_date, to_date = runner.prev.e295.e294.base.base.split_dates(frame)
                feature_name = Path(str(feature_exports[key]["path"])).name
                attempt = runner.prev.e295.e294.base.base.attempt_payload(
                    run_root=RUN_ROOT,
                    run_id=RUN_ID,
                    stage_number=308,
                    exploration_label=EXPLORATION_LABEL,
                    attempt_name=f"{token}_{tier_token}_{split_token}",
                    tier=tier_label,
                    split=runtime_split,
                    model_path=f"{COMMON_ROOT}/models/{model_name}",
                    model_id=f"{RUN_ID}_{token}_{tier_token}_route_signal_table",
                    model_backend="ebm_table",
                    feature_path=f"{COMMON_ROOT}/features/{feature_name}",
                    feature_count=len(FEATURE_ORDER),
                    feature_order_hash=feature_hash,
                    short_threshold=0.55,
                    long_threshold=0.55,
                    min_margin=0.0,
                    invert_signal=False,
                    from_date=from_date,
                    to_date=to_date,
                    primary_active_tier=tier_key,
                    attempt_role="tier_only_total" if tier_key == "tier_a" else "tier_b_fallback_only_total",
                    record_view_prefix=f"mt5_{token}_{tier_token}",
                    max_hold_bars=max_hold,
                    common_root=COMMON_ROOT,
                    close_on_flat_signal=close_on_flat,
                    reverse_on_opposite_signal=True,
                    close_only_on_opposite_signal=False,
                    extra_set_values=extras,
                )
                attach_identity(attempt, queue_row, max_hold, close_on_flat, same_reentry)
                attempt["signal_policy"] = "stage308 non-return-rank profit source route_signal_value -1/0/+1 through single-feature table"
                attempts.append(attempt)
            if include_routed:
                tier_a_key = f"{materialized_id}__tier_a__{runtime_split}"
                tier_b_key = f"{materialized_id}__tier_b__{runtime_split}"
                tier_a_frame = split_frames[tier_a_key]
                from_date, to_date = runner.prev.e295.e294.base.base.split_dates(tier_a_frame)
                tier_a_feature = Path(str(feature_exports[tier_a_key]["path"])).name
                tier_b_feature = Path(str(feature_exports[tier_b_key]["path"])).name
                attempt = runner.prev.e295.e294.base.base.attempt_payload(
                    run_root=RUN_ROOT,
                    run_id=RUN_ID,
                    stage_number=308,
                    exploration_label=EXPLORATION_LABEL,
                    attempt_name=f"{token}_routed_{split_token}",
                    tier=runner.prev.e295.e294.base.mt5.TIER_AB,
                    split=runtime_split,
                    model_path=f"{COMMON_ROOT}/models/{model_name}",
                    model_id=f"{RUN_ID}_{token}_tier_a_route_signal_table",
                    model_backend="ebm_table",
                    feature_path=f"{COMMON_ROOT}/features/{tier_a_feature}",
                    feature_count=len(FEATURE_ORDER),
                    feature_order_hash=feature_hash,
                    short_threshold=0.55,
                    long_threshold=0.55,
                    min_margin=0.0,
                    invert_signal=False,
                    from_date=from_date,
                    to_date=to_date,
                    primary_active_tier="tier_a",
                    attempt_role="actual_routed_total",
                    record_view_prefix=f"mt5_{token}_actual_routed",
                    max_hold_bars=max_hold,
                    common_root=COMMON_ROOT,
                    fallback_enabled=True,
                    fallback_model_path=f"{COMMON_ROOT}/models/{model_name}",
                    fallback_model_id=f"{RUN_ID}_{token}_tier_b_route_signal_table",
                    fallback_model_backend="ebm_table",
                    fallback_feature_path=f"{COMMON_ROOT}/features/{tier_b_feature}",
                    fallback_feature_count=len(FEATURE_ORDER),
                    fallback_feature_order_hash=feature_hash,
                    fallback_short_threshold=0.55,
                    fallback_long_threshold=0.55,
                    fallback_min_margin=0.0,
                    fallback_invert_signal=False,
                    close_on_flat_signal=close_on_flat,
                    reverse_on_opposite_signal=True,
                    close_only_on_opposite_signal=False,
                    extra_set_values=extras,
                )
                attach_identity(attempt, queue_row, max_hold, close_on_flat, same_reentry)
                attempt["signal_policy"] = "Tier A primary + Tier B fallback stage308 non-return-rank profit source route_signal_value"
                attempts.append(attempt)
    return attempts


def classify_status(result: Mapping[str, Any], materialize_only: bool) -> tuple[str, str, str, str]:
    execution_results = list(result.get("execution_results", []))
    kpis = list(result.get("mt5_kpi_records", []))
    planned = int(result.get("planned_attempt_count", len(result.get("attempts", []))) or 0)
    limited = len(execution_results) < planned
    if materialize_only:
        return (
            STATUS_PREPARED,
            "non_return_rank_profit_source_runtime_probe_prepared_no_external_execution",
            "out_of_scope_by_claim_materialize_only",
            "run308B_execute_non_return_rank_profit_source_mt5_probe_external_check",
        )
    completed_exec = sum(1 for item in execution_results if item.get("status") == "completed")
    if planned and completed_exec >= planned and len(kpis) >= planned:
        return (
            "completed_non_return_rank_profit_source_mt5_probe_no_selection",
            "runtime_probe_completed_requires_profit_scale_curve_review_no_selection",
            "completed",
            "run308C_review_non_return_rank_profit_source_mt5_probe",
        )
    if kpis:
        return (
            "partial_non_return_rank_profit_source_mt5_probe_no_selection",
            "runtime_probe_partial_requires_continuation_or_review_no_selection",
            "partial_or_blocked",
            "run308B_continue_non_return_rank_profit_source_mt5_probe" if limited else "run308C_review_with_runtime_gaps",
        )
    return (
        "blocked_non_return_rank_profit_source_mt5_probe_no_kpi",
        "runtime_probe_blocked_no_kpi_no_selection",
        "blocked_or_invalid",
        "run308B_repair_or_block_non_return_rank_profit_source_mt5_probe",
    )


def report_markdown(result: Mapping[str, Any], status: str, judgment: str, external_status: str, next_action: str) -> str:
    attempts = list(result.get("attempts", []))
    execution_results = list(result.get("execution_results", []))
    kpis = list(result.get("mt5_kpi_records", []))
    completed = sum(1 for item in execution_results if item.get("status") == "completed")
    blocked = sum(1 for item in execution_results if item.get("status") == "blocked")
    return "\n".join(
        [
            "# run308B Non-Return-Rank Profit Source MT5 Probe(308B 비수익순위 수익 원천 MT5 탐침)",
            "",
            f"- run_id(실행 ID): `{RUN_ID}`",
            f"- stage_id(단계 ID): `{STAGE_ID}`",
            f"- source_run(원천 실행): `{SOURCE_RUN_ID}`",
            f"- status(상태): `{status}`",
            f"- judgment(판정): `{judgment}`",
            f"- external_verification_status(외부 검증 상태): `{external_status}`",
            f"- attempts(시도): `{len(execution_results)}/{len(attempts)}`",
            f"- completed_attempts(완료 시도): `{completed}`",
            f"- blocked_attempts(차단 시도): `{blocked}`",
            f"- mt5_kpi_records(MT5 KPI 기록): `{len(kpis)}`",
            f"- feature_order(피처 순서): `{'|'.join(FEATURE_ORDER)}`",
            "- selected_candidate(선택 후보): `none`",
            "- Adapter package(어댑터 패키지): `none`",
            "- ONNX readiness(온엑스 준비): `not_claimed`",
            "- Goal Achieve(목표 달성): `not_claimed`",
            f"- next_action(다음 행동): `{next_action}`",
            "",
            "Effect(효과): run308A(308A 실행)의 route_signal_value(경로 신호)를 실제 MT5 tester(MT5 테스터)에 넣어 trade count(거래 수), net profit(순수익), PF(수익 팩터), DD(drawdown, 손실폭), recovery(회복)를 확인했다.",
            "",
            f"`{BOUNDARY}`",
        ]
    )


def upsert_ledgers(result: Mapping[str, Any], status: str, judgment: str, external_status: str, next_action: str) -> None:
    attempt_count = len(result.get("attempts", []))
    kpi_count = len(result.get("mt5_kpi_records", []))
    safe_upsert_rows(
        RUN_REGISTRY,
        runner.prev.e295.e294.base.base.RUN_REGISTRY_COLUMNS,
        [{"run_id": RUN_ID, "stage_id": STAGE_ID, "lane": "non_return_rank_profit_source_mt5_probe", "status": status, "judgment": judgment, "path": runner.prev.e295.e294.base.base.rel(REPORT), "notes": f"attempts={attempt_count};mt5_kpi_records={kpi_count};selected_candidate=none;onnx_readiness=not_claimed;next_action={next_action}."}],
        key="run_id",
    )
    safe_upsert_rows(
        ALPHA_LEDGER,
        runner.prev.e295.e294.base.base.ALPHA_LEDGER_COLUMNS,
        [
            {
                "ledger_row_id": f"{RUN_ID}__mt5_probe",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": RUN_NUMBER,
                "parent_run_id": SOURCE_RUN_ID,
                "record_view": "non_return_rank_profit_source_mt5_probe",
                "tier_scope": "Tier A used/Tier B fallback stress/actual routed total",
                "kpi_scope": "runtime_probe",
                "scoreboard_lane": "non_return_rank_profit_source",
                "status": status,
                "judgment": judgment,
                "path": runner.prev.e295.e294.base.base.rel(REPORT),
                "primary_kpi": f"attempts={attempt_count};mt5_kpi_records={kpi_count}",
                "guardrail_kpi": "selected_candidate=none;onnx_readiness=not_claimed",
                "external_verification_status": external_status,
                "notes": f"next_action={next_action}.",
            }
        ],
        key="ledger_row_id",
    )
    safe_upsert_rows(
        STAGE_LEDGER,
        runner.prev.e295.e294.base.STAGE_LEDGER_COLUMNS,
        [{"row_id": f"{RUN_ID}__mt5_probe", "stage_id": STAGE_ID, "run_id": RUN_ID, "view": "non_return_rank_profit_source_mt5_probe", "tier_scope": "Tier A used/Tier B fallback stress/actual routed total", "scoreboard": "runtime_probe", "status": status, "judgment": judgment, "evidence_boundary": "runtime_probe_no_candidate_no_onnx", "report_path": runner.prev.e295.e294.base.base.rel(REPORT), "notes": f"attempts={attempt_count};mt5_kpi_records={kpi_count}."}],
        key="row_id",
    )


def update_artifact_registry(paths: Sequence[Path], created_at: str) -> None:
    rows = [
        {
            "artifact_id": f"{RUN_ID}__{hashlib.sha1(runner.prev.e295.e294.base.base.rel(path).encode('utf-8')).hexdigest()[:12]}",
            "artifact_type": "stage308_non_return_rank_profit_source_mt5_artifact",
            "path": runner.prev.e295.e294.base.base.rel(path),
            "sha256": runner.prev.e295.e294.base.base.sha256_file_lf_normalized(path),
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": created_at,
            "notes": "run308B non-return-rank profit source MT5 probe",
        }
        for path in paths
        if runner.prev.e295.e294.base.base.path_exists(path)
    ]
    safe_upsert_rows(ARTIFACT_REGISTRY, runner.prev.e295.e294.base.ARTIFACT_COLUMNS, rows, "artifact_id")


def replace_first_prefix(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + replacement + "\n"


def safe_write_md(path: Path, text: str) -> None:
    base = runner.prev.e295.e294.base.base
    try:
        base.write_md(path, text)
        return
    except OSError:
        pass
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def update_docs(status: str, judgment: str, next_action: str, kpi_count: int, attempt_count: int) -> None:
    selected = runner.prev.e295.e294.base.base.io_path(SELECTED).read_text(encoding="utf-8-sig") if runner.prev.e295.e294.base.base.path_exists(SELECTED) else ""
    selected = replace_first_prefix(selected, "- stage_status(", f"- stage_status(단계 상태): `{status}`")
    selected = replace_first_prefix(selected, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    selected = replace_first_prefix(selected, "- next_action(", f"- next_action(다음 행동): `{next_action}`")
    selected = runner.prev.e295.e294.base.base.append_once(selected, "run308B_report", f"- run308B_report(308B 보고서): `{runner.prev.e295.e294.base.base.rel(REPORT)}`")
    selected = runner.prev.e295.e294.base.base.append_once(selected, "run308B_execution_result", f"- run308B_execution_result(308B 실행 결과): `{runner.prev.e295.e294.base.base.rel(EXECUTION_RESULT)}`")
    safe_write_md(SELECTED, selected)

    review_index = runner.prev.e295.e294.base.base.io_path(REVIEW_INDEX).read_text(encoding="utf-8-sig") if runner.prev.e295.e294.base.base.path_exists(REVIEW_INDEX) else "# Stage308 Review Index(308단계 검토 색인)\n"
    review_index = runner.prev.e295.e294.base.base.append_once(
        review_index,
        "run308B_report",
        f"- run308B_report(308B 보고서): `{runner.prev.e295.e294.base.base.rel(REPORT)}`\n- run308B_execution_result(308B 실행 결과): `{runner.prev.e295.e294.base.base.rel(EXECUTION_RESULT)}`\n- run308B_mt5_kpi_summary(308B MT5 KPI 요약): `{runner.prev.e295.e294.base.base.rel(MT5_KPI_SUMMARY)}`",
    )
    safe_write_md(REVIEW_INDEX, review_index)

    current = runner.prev.e295.e294.base.base.io_path(CURRENT_STATE).read_text(encoding="utf-8-sig") if runner.prev.e295.e294.base.base.path_exists(CURRENT_STATE) else ""
    current = replace_first_prefix(current, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_first_prefix(current, "- status(", f"- status(상태): `{status}`")
    current = replace_first_prefix(current, "- next_action(", f"- next_action(다음 행동): `{next_action}`")
    current = runner.prev.e295.e294.base.base.append_once(
        current,
        "run308B_summary",
        f"- run308B_summary(308B 요약): non-return-rank profit source MT5 probe(비수익순위 수익 원천 MT5 탐침)를 실행했다. Effect(효과): attempts(시도) `{attempt_count}`개와 MT5 KPI records(MT5 KPI 기록) `{kpi_count}`개를 만들었고 선택 후보/Adapter(어댑터)/ONNX(온엑스)는 주장하지 않는다.",
    )
    safe_write_md(CURRENT_STATE, current)

    workspace = runner.prev.e295.e294.base.base.io_path(WORKSPACE_STATE).read_text(encoding="utf-8-sig") if runner.prev.e295.e294.base.base.path_exists(WORKSPACE_STATE) else ""
    workspace = runner.prev.e295.e294.base.base.replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    workspace = runner.prev.e295.e294.base.base.replace_line_prefix(workspace, "updated_on:", f"updated_on: '{UPDATED_ON}'")
    focus = (
        f"- >-\n"
        f"  Stage308(308단계) run308B(308B 실행) non-return-rank profit source MT5 probe(비수익순위 수익 원천 MT5 탐침) `{RUN_ID}`. "
        f"Effect(효과): attempts(시도) `{attempt_count}`개와 MT5 KPI records(MT5 KPI 기록) `{kpi_count}`개를 기록했고 selected candidate(선택 후보), Adapter package(어댑터 패키지), ONNX readiness(온엑스 준비)는 주장하지 않는다.\n"
    )
    workspace = runner.prev.e295.e294.base.base.prepend_focus(workspace, focus, RUN_ID)
    safe_write_md(WORKSPACE_STATE, workspace)

    changelog = runner.prev.e295.e294.base.base.io_path(CHANGELOG).read_text(encoding="utf-8-sig") if runner.prev.e295.e294.base.base.path_exists(CHANGELOG) else "# Changelog(변경 기록)\n"
    changelog = runner.prev.e295.e294.base.base.append_once(
        changelog,
        RUN_ID,
        f"## {UPDATED_ON} run308B Non-return-rank profit source MT5 probe(308B 비수익순위 수익 원천 MT5 탐침)\n\n"
        f"- status(상태): `{status}`\n"
        f"- judgment(판정): `{judgment}`\n"
        f"- effect(효과): attempts(시도) `{attempt_count}`개와 MT5 KPI records(MT5 KPI 기록) `{kpi_count}`개를 기록했다.\n"
        f"- boundary(경계): selected candidate(선택 후보), Adapter package(어댑터 패키지), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 `none/not_claimed`다.\n",
    )
    safe_write_md(CHANGELOG, changelog)


def configure_runner() -> None:
    replacements: dict[str, Any] = {
        "STAGE_ID": STAGE_ID,
        "RUN_ID": RUN_ID,
        "RUN_NUMBER": RUN_NUMBER,
        "SOURCE_RUN_ID": SOURCE_RUN_ID,
        "PARENT_RUN_ID": PARENT_RUN_ID,
        "STATUS_PREPARED": STATUS_PREPARED,
        "UPDATED_ON": UPDATED_ON,
        "BOUNDARY": BOUNDARY,
        "EXPLORATION_LABEL": EXPLORATION_LABEL,
        "SIGNAL_COLUMN": SIGNAL_COLUMN,
        "FEATURE_ORDER": FEATURE_ORDER,
        "COMMON_ROOT": COMMON_ROOT,
        "STAGE_ROOT": STAGE_ROOT,
        "RUN298A": RUN308A,
        "RUN_ROOT": RUN_ROOT,
        "REVIEWS": REVIEWS,
        "SELECTED": SELECTED,
        "REVIEW_INDEX": REVIEW_INDEX,
        "STAGE_LEDGER": STAGE_LEDGER,
        "FEATURE_DIR": FEATURE_DIR,
        "MODEL_DIR": MODEL_DIR,
        "MT5_DIR": MT5_DIR,
        "MT5_QUEUE": MT5_QUEUE,
        "SOURCE_MANIFEST": SOURCE_MANIFEST,
        "SOURCE_RUN_MANIFEST": SOURCE_RUN_MANIFEST,
        "SOURCE_REPORT": SOURCE_REPORT,
        "PRODUCER": PRODUCER,
        "ATTEMPT_SUMMARY": ATTEMPT_SUMMARY,
        "RUNTIME_SUPPLY": RUNTIME_SUPPLY,
        "EXECUTION_RESULT": EXECUTION_RESULT,
        "MT5_KPI_SUMMARY": MT5_KPI_SUMMARY,
        "RUNTIME_PARITY_RECEIPT": RUNTIME_PARITY_RECEIPT,
        "RESULT_JUDGMENT": RESULT_JUDGMENT,
        "GATE_AUDIT": GATE_AUDIT,
        "RUN_MANIFEST": RUN_MANIFEST,
        "LINEAGE": LINEAGE,
        "REPORT": REPORT,
        "RUN_REGISTRY": RUN_REGISTRY,
        "ALPHA_LEDGER": ALPHA_LEDGER,
        "ARTIFACT_REGISTRY": ARTIFACT_REGISTRY,
        "CURRENT_STATE": CURRENT_STATE,
        "WORKSPACE_STATE": WORKSPACE_STATE,
        "CHANGELOG": CHANGELOG,
        "attach_identity": attach_identity,
        "build_all_attempts": build_all_attempts,
        "classify_status": classify_status,
        "report_markdown": report_markdown,
        "upsert_ledgers": upsert_ledgers,
        "update_artifact_registry": update_artifact_registry,
        "update_docs": update_docs,
    }
    for name, value in replacements.items():
        setattr(runner, name, value)


def main(argv: Sequence[str] | None = None) -> None:
    configure_runner()
    runner.main(sys.argv[1:] if argv is None else argv)


if __name__ == "__main__":
    main()
