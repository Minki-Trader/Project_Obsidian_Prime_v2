from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.alpha.discrete_signal_table import export_single_discrete_signal_score_table  # noqa: E402
from foundation.control_plane.mt5_tier_balance_completion import (  # noqa: E402
    COMMON_FILES_ROOT_DEFAULT,
    METAEDITOR_PATH_DEFAULT,
    TERMINAL_DATA_ROOT_DEFAULT,
    TERMINAL_PATH_DEFAULT,
    TESTER_PROFILE_ROOT_DEFAULT,
)
from foundation.models.onnx_bridge import ordered_hash  # noqa: E402
from foundation.mt5 import runtime_support as mt5  # noqa: E402
from stage_pipelines.stage279 import execute_or_prepare_directional_runtime_mapping_mt5_probe as base  # noqa: E402


STAGE_ID = "293_onnx_candidate_campaign__profit_scale_density_calibration_rebuild"
RUN_ID = "run293B_profit_scale_density_calibration_mt5_probe_v1"
RUN_NUMBER = "run293B"
SOURCE_RUN_ID = "run293A_design_profit_scale_density_calibration_rebuild_v1"
PARENT_RUN_ID = "run292C_review_anti_direction_meta_label_trade_simulator_mt5_probe_v1"
STATUS_PREPARED = "prepared_profit_scale_density_calibration_mt5_probe_no_runtime_kpi"
UPDATED_ON = "2026-05-24"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_"
    "no_deployment_no_onnx_until_candidate_package_gate"
)
EXPLORATION_LABEL = "stage293_Model__ProfitScaleDensityCalibrationReplay"
SIGNAL_COLUMN = "run293b_route_signal"
FEATURE_ORDER = (SIGNAL_COLUMN,)
COMMON_ROOT = "Project_Obsidian_Prime_v2/stage293/run293B_profit_scale_density_calibration"

STAGE_ROOT = ROOT / "stages" / STAGE_ID
RUN293A = STAGE_ROOT / "02_runs" / "run293A"
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER
REVIEWS = STAGE_ROOT / "03_reviews"
SELECTED = STAGE_ROOT / "04_selected" / "selection_status.md"
REVIEW_INDEX = REVIEWS / "review_index.md"
STAGE_LEDGER = REVIEWS / "stage_run_ledger.csv"
FEATURE_DIR = RUN_ROOT / "features"
MODEL_DIR = RUN_ROOT / "models"
MT5_DIR = RUN_ROOT / "mt5"
MT5_QUEUE = RUN293A / "mt5_probe_queue.csv"
SOURCE_MANIFEST = RUN293A / "candidate_payload_manifest.csv"
SOURCE_RUN_MANIFEST = RUN293A / "run_manifest.json"
SOURCE_REPORT = REVIEWS / "run293A_profit_scale_density_calibration_materialization_report.md"
PRODUCER = Path("stage_pipelines/stage293/execute_profit_scale_density_calibration_mt5_probe.py")

ATTEMPT_SUMMARY = RUN_ROOT / "attempt_summary.csv"
RUNTIME_SUPPLY = RUN_ROOT / "runtime_supply_matrix.csv"
EXECUTION_RESULT = RUN_ROOT / "execution_result.json"
MT5_KPI_SUMMARY = RUN_ROOT / "mt5_kpi_summary.csv"
RUNTIME_PARITY_RECEIPT = RUN_ROOT / "runtime_parity_receipt.json"
RESULT_JUDGMENT = RUN_ROOT / "result_judgment.csv"
GATE_AUDIT = RUN_ROOT / "required_gate_coverage_audit.csv"
RUN_MANIFEST = RUN_ROOT / "run_manifest.json"
LINEAGE = RUN_ROOT / "artifact_lineage_receipt.json"
REPORT = REVIEWS / "run293B_profit_scale_density_calibration_mt5_probe_report.md"

RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"

RESULT_COLUMNS = (
    "result_subject",
    "evidence_available",
    "evidence_missing",
    "judgment_label",
    "judgment_class",
    "claim_boundary",
    "next_condition",
    "user_explanation_hook",
)
GATE_COLUMNS = ("gate_name", "status", "evidence_path", "effect")
STAGE_LEDGER_COLUMNS = (
    "row_id",
    "stage_id",
    "run_id",
    "view",
    "tier_scope",
    "scoreboard",
    "status",
    "judgment",
    "evidence_boundary",
    "report_path",
    "notes",
)
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


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def bool_value(value: Any) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def int_value(value: Any, default: int) -> int:
    try:
        text = str(value).strip()
        return int(float(text)) if text else default
    except (TypeError, ValueError):
        return default


def configure_base() -> None:
    base.STAGE_ID = STAGE_ID
    base.RUN_ID = RUN_ID
    base.RUN_NUMBER = RUN_NUMBER
    base.SOURCE_RUN_ID = SOURCE_RUN_ID
    base.PARENT_RUN_ID = PARENT_RUN_ID
    base.STATUS_PREPARED = STATUS_PREPARED
    base.UPDATED_ON = UPDATED_ON
    base.BOUNDARY = BOUNDARY
    base.EXPLORATION_LABEL = EXPLORATION_LABEL
    base.SIGNAL_COLUMN = SIGNAL_COLUMN
    base.COMMON_ROOT = COMMON_ROOT
    base.STAGE_ROOT = STAGE_ROOT
    base.RUN279B = RUN293A
    base.RUN_ROOT = RUN_ROOT
    base.REVIEWS = REVIEWS
    base.SELECTED = SELECTED
    base.REPORT_PATH = REPORT
    base.FEATURE_DIR = FEATURE_DIR
    base.MODEL_DIR = MODEL_DIR
    base.MT5_DIR = MT5_DIR
    base.MT5_QUEUE = MT5_QUEUE
    base.RUN279B_MANIFEST = SOURCE_RUN_MANIFEST
    base.RUN279B_PAYLOAD_MANIFEST = SOURCE_MANIFEST
    base.RUN279B_SIGNAL_RECEIPT = SOURCE_MANIFEST
    base.RUN279B_REPORT = SOURCE_REPORT
    base.RUN_REGISTRY = RUN_REGISTRY
    base.ALPHA_LEDGER = ALPHA_LEDGER
    base.ARTIFACT_REGISTRY = ARTIFACT_REGISTRY
    base.STAGE_LEDGER = STAGE_LEDGER
    base.CURRENT_STATE = CURRENT_STATE
    base.WORKSPACE_STATE = WORKSPACE_STATE
    base.CHANGELOG = CHANGELOG
    base.REVIEW_INDEX = REVIEW_INDEX
    base.PRODUCER_PATH = PRODUCER
    base.ATTEMPT_SUMMARY = ATTEMPT_SUMMARY
    base.RUNTIME_SUPPLY = RUNTIME_SUPPLY
    base.EXECUTION_RESULT = EXECUTION_RESULT
    base.MT5_KPI_SUMMARY = MT5_KPI_SUMMARY
    base.RUNTIME_PARITY_RECEIPT = RUNTIME_PARITY_RECEIPT
    base.RESULT_JUDGMENT = RESULT_JUDGMENT
    base.GATE_AUDIT = GATE_AUDIT
    base.RUN_MANIFEST = RUN_MANIFEST
    base.LINEAGE_RECEIPT = LINEAGE
    base.build_all_attempts = build_all_attempts


def attach_identity(attempt: dict[str, Any], queue_row: Mapping[str, str], max_hold: int, close_on_flat: bool, same_reentry: int) -> None:
    base.attach_attempt_identity(attempt, queue_row)
    attempt["stage293_branch_id"] = queue_row.get("stage293_branch_id", "")
    attempt["stage291_branch_id"] = queue_row.get("stage291_branch_id", "")
    attempt["stage290_branch_id"] = queue_row.get("stage290_branch_id", "")
    attempt["max_hold_bars"] = max_hold
    attempt["close_on_flat_signal"] = close_on_flat
    attempt["same_direction_reentry_cooldown_bars"] = same_reentry


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
        token = base.variant_token(queue_row, 44)
        max_hold = int_value(queue_row.get("max_hold_bars"), 6)
        close_on_flat = bool_value(queue_row.get("close_on_flat_signal"))
        same_reentry = int_value(queue_row.get("same_direction_reentry_cooldown_bars"), 0)
        extra_set_values = {
            "InpEntryTransitionOnly": False,
            "InpReentryCooldownBars": 0,
            "InpSameDirectionReentryCooldownBars": same_reentry,
        }
        for runtime_split, split_token in (("validation_is", "val"), ("oos", "oos")):
            for tier_key, tier_label, tier_token in (("tier_a", mt5.TIER_A, "tier_a"), ("tier_b", mt5.TIER_B, "tier_b")):
                key = f"{materialized_id}__{tier_key}__{runtime_split}"
                frame = split_frames[key]
                from_date, to_date = base.split_dates(frame)
                feature_name = Path(str(feature_exports[key]["path"])).name
                attempt = base.attempt_payload(
                    run_root=RUN_ROOT,
                    run_id=RUN_ID,
                    stage_number=293,
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
                    extra_set_values=extra_set_values,
                )
                attach_identity(attempt, queue_row, max_hold, close_on_flat, same_reentry)
                attempt["signal_policy"] = "stage293 anti-direction/meta-simulator route_signal_value -1/0/+1 through single-feature table"
                attempts.append(attempt)
            if include_routed:
                tier_a_key = f"{materialized_id}__tier_a__{runtime_split}"
                tier_b_key = f"{materialized_id}__tier_b__{runtime_split}"
                tier_a_frame = split_frames[tier_a_key]
                from_date, to_date = base.split_dates(tier_a_frame)
                tier_a_feature = Path(str(feature_exports[tier_a_key]["path"])).name
                tier_b_feature = Path(str(feature_exports[tier_b_key]["path"])).name
                attempt = base.attempt_payload(
                    run_root=RUN_ROOT,
                    run_id=RUN_ID,
                    stage_number=293,
                    exploration_label=EXPLORATION_LABEL,
                    attempt_name=f"{token}_routed_{split_token}",
                    tier=mt5.TIER_AB,
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
                    extra_set_values=extra_set_values,
                )
                attach_identity(attempt, queue_row, max_hold, close_on_flat, same_reentry)
                attempt["signal_policy"] = "Tier A primary + Tier B fallback stage293 anti-direction/meta-simulator route_signal_value"
                attempts.append(attempt)
    return attempts


def prepare(args: argparse.Namespace) -> dict[str, Any]:
    queue_rows = base.load_queue_rows()
    feature_exports, split_frames, supply_rows = base.export_feature_matrices(queue_rows)
    base.write_csv(RUNTIME_SUPPLY, supply_rows)
    model_artifact = export_single_discrete_signal_score_table(
        MODEL_DIR / "stage293_run293B_route_signal_score_table.csv",
        feature_order=FEATURE_ORDER,
    )
    common_copies = base.copy_runtime_inputs(feature_exports, model_artifact, Path(args.common_files_root))
    full_attempts = build_all_attempts(queue_rows, feature_exports, split_frames, model_artifact, include_routed=not args.no_routed)
    start_index = max(0, int(args.start_index))
    end_index = start_index + int(args.limit) if args.limit is not None else None
    attempts = full_attempts[start_index:end_index]
    return {
        "stage_id": STAGE_ID,
        "stage_number": 293,
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "source_run_id": SOURCE_RUN_ID,
        "run_root": RUN_ROOT,
        "attempts": attempts,
        "planned_attempt_count": len(full_attempts),
        "common_copies": common_copies,
        "feature_exports": feature_exports,
        "model_artifact": model_artifact,
        "runtime_supply_matrix": supply_rows,
        "route_coverage": base.route_coverage_from_supply(supply_rows),
        "model_family": "single_discrete_signal_score_table",
        "feature_set_id": "stage293_profit_scale_density_calibration_route_signal_replay",
        "label_id": "not_applicable_precomputed_route_signal_from_stage293_models",
        "split_contract": "stage293 run293A payload split labels validation and oos",
        "claim_boundary": BOUNDARY,
    }


def classify_status(result: Mapping[str, Any], materialize_only: bool) -> tuple[str, str, str, str]:
    execution_results = list(result.get("execution_results", []))
    kpis = list(result.get("mt5_kpi_records", []))
    planned = int(result.get("planned_attempt_count", len(result.get("attempts", []))) or 0)
    limited = len(execution_results) < planned
    if materialize_only:
        return (
            STATUS_PREPARED,
            "anti_direction_meta_trade_sim_runtime_probe_prepared_no_external_execution",
            "out_of_scope_by_claim_materialize_only",
            "run293B_execute_profit_scale_density_calibration_mt5_probe_external_check",
        )
    completed_exec = sum(1 for item in execution_results if item.get("status") == "completed")
    if planned and completed_exec >= planned and len(kpis) >= planned:
        return (
            "completed_profit_scale_density_calibration_mt5_probe_no_selection",
            "runtime_probe_completed_requires_curve_quality_review_no_selection",
            "completed",
            "run293C_review_profit_scale_density_calibration_mt5_probe",
        )
    if kpis:
        return (
            "partial_profit_scale_density_calibration_mt5_probe_no_selection",
            "runtime_probe_partial_requires_continuation_or_review_no_selection",
            "partial_or_blocked",
            "run293B_continue_profit_scale_density_calibration_mt5_probe" if limited else "run293C_review_with_runtime_gaps",
        )
    return (
        "blocked_profit_scale_density_calibration_mt5_probe_no_kpi",
        "runtime_probe_blocked_no_kpi_no_selection",
        "blocked_or_invalid",
        "run293B_repair_or_block_profit_scale_density_calibration_mt5_probe",
    )


def report_markdown(result: Mapping[str, Any], status: str, judgment: str, external_status: str, next_action: str) -> str:
    attempts = list(result.get("attempts", []))
    execution_results = list(result.get("execution_results", []))
    kpis = list(result.get("mt5_kpi_records", []))
    completed = sum(1 for item in execution_results if item.get("status") == "completed")
    blocked = sum(1 for item in execution_results if item.get("status") == "blocked")
    return "\n".join(
        [
            "# run293B profit-scale density calibration MT5 Probe(293B ??갑??硫뷀??쇰꺼 嫄곕옒 ?쒕??덉씠??MT5 ?먯묠)",
            "",
            f"- run_id(?ㅽ뻾 ID): `{RUN_ID}`",
            f"- stage_id(?④퀎 ID): `{STAGE_ID}`",
            f"- source_run(?먯쿇 ?ㅽ뻾): `{SOURCE_RUN_ID}`",
            f"- status(?곹깭): `{status}`",
            f"- judgment(?먯젙): `{judgment}`",
            f"- external_verification_status(?몃? 寃利??곹깭): `{external_status}`",
            f"- attempts(?쒕룄): `{len(execution_results)}/{len(attempts)}`",
            f"- completed_attempts(?꾨즺 ?쒕룄): `{completed}`",
            f"- blocked_attempts(李⑤떒 ?쒕룄): `{blocked}`",
            f"- mt5_kpi_records(MT5 KPI 湲곕줉): `{len(kpis)}`",
            f"- feature_order(?쇱쿂 ?쒖꽌): `{'|'.join(FEATURE_ORDER)}`",
            "- selected_candidate(?좏깮 ?꾨낫): `none`",
            "- Adapter package(?대뙌???⑦궎吏): `none`",
            "- ONNX readiness(?⑥뿊??以鍮?: `not_claimed`",
            "- Goal Achieve(紐⑺몴 ?ъ꽦): `not_claimed`",
            f"- next_action(?ㅼ쓬 ?됰룞): `{next_action}`",
            "",
            "Effect(?④낵): run293A(293A ?ㅽ뻾)??route_signal_value(寃쎈줈 ?좏샇媛?瑜??ㅼ젣 MT5 tester(MT5 ?뚯뒪?????ｌ뿀?? ?꾨낫 ?먯젙? run293C(293C ?ㅽ뻾)?먯꽌 ?쒖닔?? ??嫄곕옒?? PF(?섏씡 ?⑺꽣), ?뚮났, 怨≪꽑 ?ъ폆??媛숈씠 蹂??ㅼ뿉留??쒕떎.",
            "",
            "## Boundary(寃쎄퀎)",
            "",
            f"`{BOUNDARY}`",
        ]
    )


def rewrite_outputs(result: Mapping[str, Any], status: str, judgment: str, external_status: str, next_action: str, created_at: str) -> list[Path]:
    attempts = list(result.get("attempts", []))
    execution_results = list(result.get("execution_results", []))
    kpis = list(result.get("mt5_kpi_records", []))
    base.write_json(EXECUTION_RESULT, {**dict(result), "status": status, "judgment": judgment, "external_verification_status": external_status, "next_action": next_action}, bom=True)
    base.write_csv(ATTEMPT_SUMMARY, base.attempt_summary_rows(result))
    base.write_csv(RUNTIME_SUPPLY, result.get("runtime_supply_matrix", []))
    base.write_csv(MT5_KPI_SUMMARY, kpis)
    base.write_json(
        RUNTIME_PARITY_RECEIPT,
        {
            "run_id": RUN_ID,
            "feature_order": list(FEATURE_ORDER),
            "feature_order_hash": ordered_hash(FEATURE_ORDER),
            "shared_contract": "route_signal_value -1 short, 0 flat, +1 long",
            "runtime_claim_boundary": "runtime_probe_only_no_candidate_selection",
        },
    )
    base.write_csv(
        RESULT_JUDGMENT,
        [
            {
                "result_subject": RUN_ID,
                "evidence_available": f"attempts={len(attempts)};execution_results={len(execution_results)};mt5_kpi_records={len(kpis)};report={base.rel(REPORT)}",
                "evidence_missing": "reviewed curve pockets;candidate package;Adapter package;ONNX parity;final candidate report",
                "judgment_label": judgment,
                "judgment_class": "runtime_probe(?고????먯묠)" if kpis else "blocked_or_prepared(李⑤떒 ?먮뒗 以鍮?",
                "claim_boundary": BOUNDARY,
                "next_condition": next_action,
                "user_explanation_hook": "MT5 ?먯묠 寃곌낵留뚯쑝濡쒕뒗 ?꾩쭅 ?좏깮 ?꾨낫媛 ?꾨땲??",
            }
        ],
        RESULT_COLUMNS,
    )
    base.write_csv(
        GATE_AUDIT,
        [
            {
                "gate_name": "feature_matrix_handoff(?쇱쿂 ?됰젹 ?멸퀎)",
                "status": "passed",
                "evidence_path": base.rel(RUNTIME_SUPPLY),
                "effect": "EA(Expert Advisor, ?꾨Ц媛 ?먮Ц)媛 ?⑥씪 route signal(寃쎈줈 ?좏샇)???쎌쓣 ???덇쾶 ?덈떎.",
            },
            {
                "gate_name": "external_runtime_attempt(?몃? ?고????쒕룄)",
                "status": external_status,
                "evidence_path": base.rel(EXECUTION_RESULT),
                "effect": "MT5 tester(MT5 ?뚯뒪?? ?ㅽ뻾 ?먮뒗 以鍮??곹깭瑜?湲곕줉?쒕떎.",
            },
            {
                "gate_name": "candidate_claim_boundary(?꾨낫 二쇱옣 寃쎄퀎)",
                "status": "passed",
                "evidence_path": base.rel(RESULT_JUDGMENT),
                "effect": "?좏깮 ?꾨낫, Adapter package(?대뙌???⑦궎吏), ONNX readiness(?⑥뿊??以鍮?瑜?二쇱옣?섏? ?딅뒗??",
            },
        ],
        GATE_COLUMNS,
    )
    base.write_md(REPORT, report_markdown(result, status, judgment, external_status, next_action))
    final_paths = [EXECUTION_RESULT, ATTEMPT_SUMMARY, RUNTIME_SUPPLY, MT5_KPI_SUMMARY, RUNTIME_PARITY_RECEIPT, RESULT_JUDGMENT, GATE_AUDIT, REPORT]
    base.write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "source_run_id": SOURCE_RUN_ID,
            "status": status,
            "judgment": judgment,
            "external_verification_status": external_status,
            "created_at_utc": created_at,
            "attempt_count": len(attempts),
            "execution_result_count": len(execution_results),
            "mt5_kpi_record_count": len(kpis),
            "selected_candidate": "none",
            "adapter_package": "none",
            "onnx_readiness": "not_claimed",
            "goal_achieve": "not_claimed",
            "next_action": next_action,
            "claim_boundary": BOUNDARY,
            "output_hashes": {base.rel(path): base.sha256_file_lf_normalized(path) for path in final_paths if base.path_exists(path)},
        },
    )
    final_paths.append(RUN_MANIFEST)
    base.write_json(
        LINEAGE,
        {
            "run_id": RUN_ID,
            "source_inputs": [base.rel(MT5_QUEUE), base.rel(SOURCE_MANIFEST), base.rel(SOURCE_RUN_MANIFEST), base.rel(ROOT / PRODUCER)],
            "producer": base.rel(ROOT / PRODUCER),
            "consumer": next_action,
            "artifact_paths": [base.rel(path) for path in final_paths if base.path_exists(path)],
            "artifact_hashes": {base.rel(path): base.sha256_file_lf_normalized(path) for path in final_paths if base.path_exists(path)},
            "claim_boundary": BOUNDARY,
        },
    )
    final_paths.append(LINEAGE)
    return final_paths


def upsert_ledgers(result: Mapping[str, Any], status: str, judgment: str, external_status: str, next_action: str) -> None:
    attempt_count = len(result.get("attempts", []))
    kpi_count = len(result.get("mt5_kpi_records", []))
    base.upsert_rows(
        RUN_REGISTRY,
        base.RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "profit_scale_density_calibration_mt5_probe",
                "status": status,
                "judgment": judgment,
                "path": base.rel(REPORT),
                "notes": f"attempts={attempt_count};mt5_kpi_records={kpi_count};selected_candidate=none;onnx_readiness=not_claimed;next_action={next_action}.",
            }
        ],
        key="run_id",
    )
    base.upsert_rows(
        ALPHA_LEDGER,
        base.ALPHA_LEDGER_COLUMNS,
        [
            {
                "ledger_row_id": f"{RUN_ID}__mt5_probe",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": RUN_NUMBER,
                "parent_run_id": SOURCE_RUN_ID,
                "record_view": "profit_scale_density_calibration_mt5_probe",
                "tier_scope": "Tier A used/Tier B fallback stress/actual routed total",
                "kpi_scope": "runtime_probe",
                "scoreboard_lane": "profit_scale_density_calibration",
                "status": status,
                "judgment": judgment,
                "path": base.rel(REPORT),
                "primary_kpi": f"attempts={attempt_count};mt5_kpi_records={kpi_count}",
                "guardrail_kpi": "selected_candidate=none;onnx_readiness=not_claimed",
                "external_verification_status": external_status,
                "notes": f"next_action={next_action}.",
            }
        ],
        key="ledger_row_id",
    )
    base.upsert_rows(
        STAGE_LEDGER,
        STAGE_LEDGER_COLUMNS,
        [
            {
                "row_id": f"{RUN_ID}__mt5_probe",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "view": "profit_scale_density_calibration_mt5_probe",
                "tier_scope": "Tier A used/Tier B fallback stress/actual routed total",
                "scoreboard": "runtime_probe",
                "status": status,
                "judgment": judgment,
                "evidence_boundary": "runtime_probe_no_candidate_no_onnx",
                "report_path": base.rel(REPORT),
                "notes": f"attempts={attempt_count};mt5_kpi_records={kpi_count}.",
            }
        ],
        key="row_id",
    )


def update_artifact_registry(paths: Sequence[Path], created_at: str) -> None:
    rows = [
        {
            "artifact_id": f"{RUN_ID}__{hashlib.sha1(base.rel(path).encode('utf-8')).hexdigest()[:12]}",
            "artifact_type": "stage293_profit_scale_density_calibration_mt5_artifact",
            "path": base.rel(path),
            "sha256": base.sha256_file_lf_normalized(path),
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": created_at,
            "notes": "run293B profit-scale density calibration MT5 probe",
        }
        for path in paths
        if base.path_exists(path)
    ]
    existing = base.read_csv_rows(ARTIFACT_REGISTRY) if base.path_exists(ARTIFACT_REGISTRY) else []
    new_keys = {str(row["artifact_id"]) for row in rows}
    merged = [row for row in existing if str(row.get("artifact_id", "")).strip() not in new_keys]
    merged.extend(rows)
    base.write_csv(ARTIFACT_REGISTRY, merged, ARTIFACT_COLUMNS)


def update_docs(status: str, judgment: str, next_action: str, kpi_count: int, attempt_count: int) -> None:
    selected = base.io_path(SELECTED).read_text(encoding="utf-8-sig") if base.path_exists(SELECTED) else ""
    selected = base.replace_line_prefix(selected, "- stage_status(?④퀎 ?곹깭):", f"- stage_status(?④퀎 ?곹깭): `{status}`")
    selected = base.replace_line_prefix(selected, "- current_run(?꾩옱 ?ㅽ뻾):", f"- current_run(?꾩옱 ?ㅽ뻾): `{RUN_ID}`")
    selected = base.replace_line_prefix(selected, "- next_action(?ㅼ쓬 ?됰룞):", f"- next_action(?ㅼ쓬 ?됰룞): `{next_action}`")
    selected = base.append_once(selected, "run293B_report", f"- run293B_report(293B 蹂닿퀬): `{base.rel(REPORT)}`")
    selected = base.append_once(selected, "run293B_execution_result", f"- run293B_execution_result(293B ?ㅽ뻾 寃곌낵): `{base.rel(EXECUTION_RESULT)}`")
    base.write_md(SELECTED, selected)

    review_index = base.io_path(REVIEW_INDEX).read_text(encoding="utf-8-sig") if base.path_exists(REVIEW_INDEX) else "# stage293 Review Index(293?④퀎 寃???됱씤)\n"
    review_index = base.append_once(
        review_index,
        "run293B_report",
        f"- run293B_report(293B 蹂닿퀬): `{base.rel(REPORT)}`\n- run293B_execution_result(293B ?ㅽ뻾 寃곌낵): `{base.rel(EXECUTION_RESULT)}`\n- run293B_mt5_kpi_summary(293B MT5 KPI ?붿빟): `{base.rel(MT5_KPI_SUMMARY)}`",
    )
    base.write_md(REVIEW_INDEX, review_index)

    current = base.io_path(CURRENT_STATE).read_text(encoding="utf-8-sig") if base.path_exists(CURRENT_STATE) else ""
    current = base.replace_line_prefix(current, "- current_run(?꾩옱 ?ㅽ뻾):", f"- current_run(?꾩옱 ?ㅽ뻾): `{RUN_ID}`")
    current = base.replace_line_prefix(current, "- status(?곹깭):", f"- status(?곹깭): `{status}`")
    current = base.replace_line_prefix(current, "- next_action(?ㅼ쓬 ?됰룞):", f"- next_action(?ㅼ쓬 ?됰룞): `{next_action}`")
    run293b_summary = (
        f"- run293B_summary(293B ?붿빟): profit-scale density calibration MT5 probe(??갑??硫뷀??쇰꺼/嫄곕옒 ?쒕??덉씠??MT5 ?먯묠)瑜??ㅽ뻾?덈떎. "
        f"Effect(?④낵): attempts(?쒕룄) `{attempt_count}`媛쒖? MT5 KPI records(MT5 KPI 湲곕줉) `{kpi_count}`媛쒕? ?④꼈怨??꾨낫/?대뙌???⑥뿊??二쇱옣? ?섏? ?딅뒗??"
    )
    if "run293B_summary" in current:
        current = base.replace_line_prefix(current, "- run293B_summary(293B ?붿빟):", run293b_summary)
    else:
        current = base.append_once(current, "run293B_summary", run293b_summary)
    base.write_md(CURRENT_STATE, current)

    workspace = base.io_path(WORKSPACE_STATE).read_text(encoding="utf-8-sig") if base.path_exists(WORKSPACE_STATE) else ""
    workspace = base.replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    workspace = base.replace_line_prefix(workspace, "updated_on:", f"updated_on: '{UPDATED_ON}'")
    focus = (
        f"- >-\n"
        f"  stage293(293?④퀎) run293B(293B ?ㅽ뻾) profit-scale density calibration MT5 probe(??갑??硫뷀??쇰꺼/嫄곕옒 ?쒕??덉씠??MT5 ?먯묠) `{RUN_ID}`. "
        f"Effect(?④낵): attempts(?쒕룄) `{attempt_count}`媛쒖? MT5 KPI records(MT5 KPI 湲곕줉) `{kpi_count}`媛쒕? 湲곕줉?덇퀬 selected candidate(?좏깮 ?꾨낫), Adapter package(?대뙌???⑦궎吏), ONNX readiness(?⑥뿊??以鍮???二쇱옣?섏? ?딅뒗??\n"
    )
    workspace = base.prepend_focus(workspace, focus, RUN_ID)
    base.write_md(WORKSPACE_STATE, workspace)

    changelog = base.io_path(CHANGELOG).read_text(encoding="utf-8-sig") if base.path_exists(CHANGELOG) else "# Changelog(蹂寃?湲곕줉)\n"
    changelog = base.append_once(
        changelog,
        RUN_ID,
        f"## {UPDATED_ON} run293B profit-scale density calibration MT5 probe(293B ??갑??硫뷀??쇰꺼 嫄곕옒 ?쒕??덉씠??MT5 ?먯묠)\n\n"
        f"- status(?곹깭): `{status}`\n"
        f"- judgment(?먯젙): `{judgment}`\n"
        f"- effect(?④낵): attempts(?쒕룄) `{attempt_count}`媛쒖? MT5 KPI records(MT5 KPI 湲곕줉) `{kpi_count}`媛쒕? 湲곕줉?덈떎.\n"
        f"- boundary(寃쎄퀎): selected candidate(?좏깮 ?꾨낫), Adapter package(?대뙌???⑦궎吏), ONNX readiness(?⑥뿊??以鍮?, Goal Achieve(紐⑺몴 ?ъ꽦)??`none/not_claimed`??\n",
    )
    base.write_md(CHANGELOG, changelog)


def run_probe(args: argparse.Namespace) -> dict[str, Any]:
    configure_base()
    created_at = utc_now()
    for path in (RUN_ROOT, FEATURE_DIR, MODEL_DIR, MT5_DIR, REVIEWS):
        base.io_path(path).mkdir(parents=True, exist_ok=True)
    prepared = prepare(args)
    if args.materialize_only:
        result = {
            **prepared,
            "compile": {"status": "not_attempted_materialize_only"},
            "execution_results": [],
            "strategy_tester_reports": [],
            "mt5_kpi_records": [],
        }
    else:
        result = base.execute_prepared(
            prepared,
            terminal_path=Path(args.terminal_path),
            metaeditor_path=Path(args.metaeditor_path),
            terminal_data_root=Path(args.terminal_data_root),
            common_files_root=Path(args.common_files_root),
            tester_profile_root=Path(args.tester_profile_root),
            timeout_seconds=int(args.timeout_seconds),
            runtime_timeout_seconds=int(args.runtime_timeout_seconds),
        )
    if args.merge_existing:
        result = base.merge_existing_result(result, start_index=max(0, int(args.start_index)), limit=args.limit)
    status, judgment, external_status, next_action = classify_status(result, bool(args.materialize_only))
    result = {
        **dict(result),
        "status": status,
        "judgment": judgment,
        "external_verification_status": external_status,
        "selected_candidate": "none",
        "selected_research_baseline": "none",
        "adapter_package": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": next_action,
        "created_at_utc": created_at,
    }
    final_paths = rewrite_outputs(result, status, judgment, external_status, next_action, created_at)
    upsert_ledgers(result, status, judgment, external_status, next_action)
    update_artifact_registry(final_paths, created_at)
    update_docs(status, judgment, next_action, len(result.get("mt5_kpi_records", [])), len(result.get("attempts", [])))
    return result


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Execute or prepare stage293 profit-scale density calibration MT5 probe.")
    parser.add_argument("--materialize-only", action="store_true")
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--start-index", type=int, default=0)
    parser.add_argument("--merge-existing", action="store_true")
    parser.add_argument("--no-routed", action="store_true")
    parser.add_argument("--terminal-path", default=str(TERMINAL_PATH_DEFAULT))
    parser.add_argument("--metaeditor-path", default=str(METAEDITOR_PATH_DEFAULT))
    parser.add_argument("--terminal-data-root", default=str(TERMINAL_DATA_ROOT_DEFAULT))
    parser.add_argument("--common-files-root", default=str(COMMON_FILES_ROOT_DEFAULT))
    parser.add_argument("--tester-profile-root", default=str(TESTER_PROFILE_ROOT_DEFAULT))
    parser.add_argument("--timeout-seconds", type=int, default=600)
    parser.add_argument("--runtime-timeout-seconds", type=int, default=900)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> None:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    result = run_probe(args)
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": result.get("status"),
                "judgment": result.get("judgment"),
                "attempts": len(result.get("attempts", [])),
                "execution_results": len(result.get("execution_results", [])),
                "external_verification_status": result.get("external_verification_status"),
                "mt5_kpi_records": len(result.get("mt5_kpi_records", [])),
                "selected_candidate": "none",
                "adapter_package": "none",
                "onnx_readiness": "not_claimed",
                "goal_achieve": "not_claimed",
                "next_action": result.get("next_action"),
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()

