from __future__ import annotations

import csv
import json
import math
import shutil
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.control_plane.ledger import (
    ALPHA_LEDGER_COLUMNS,
    RUN_REGISTRY_COLUMNS,
    io_path,
    json_ready,
    path_exists,
    sha256_file_lf_normalized,
    upsert_csv_rows,
)
from foundation.control_plane.mt5_tier_balance_completion import (
    COMMON_FILES_ROOT_DEFAULT,
    copy_to_common,
)
from foundation.models.onnx_bridge import ordered_hash
from stage_pipelines.stage267 import (
    run267CV_shared_weakness_breakout_followup_or_prune_materialization as source_aih_materializer,
)
from stage_pipelines.stage267 import (
    run267DQ_runtime_gap_aware_fourth_followup_or_prune_materialization as source_runtime_materializer,
)
from stage_pipelines.stage267 import (
    run267DT_runtime_gap_aware_fifth_followup_or_prune_design as source_design,
)


STAGE_ID = source_design.STAGE_ID
RUN_NUMBER = "run267DU"
RUN_ID = "run267DU_stage267_runtime_gap_aware_fifth_followup_or_prune_materialization_v1"
PARENT_RUN_ID = source_design.RUN_ID
SOURCE_RUNTIME_RUN_ID = source_runtime_materializer.RUN_ID
SOURCE_AIH_RUN_ID = source_aih_materializer.RUN_ID
STATUS = "run267DU_runtime_gap_aware_fifth_followup_or_prune_materialized_execution_pending"
JUDGMENT = "runtime_gap_aware_fifth_followup_or_prune_materialized_no_candidate_selection"
NEXT_ACTION = "run267DV_execute_runtime_gap_aware_fifth_followup_or_prune_mt5_batch"
CLAIM_BOUNDARY = source_design.CLAIM_BOUNDARY

STAGE_ROOT = source_design.STAGE_ROOT
REVIEWS_ROOT = source_design.REVIEWS_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER / "runtime_gap_aware_fifth_followup_or_prune_materialization"
FEATURE_ROOT = RUN_ROOT / "features"
VARIANT_ROOT = RUN_ROOT / "variants"
MT5_ROOT = RUN_ROOT / "mt5"

SOURCE_QUEUE_PATH = source_design.MATERIALIZATION_QUEUE_PATH
SOURCE_FEATURE_BLUEPRINT_PATH = source_design.FEATURE_BLUEPRINT_PATH
SOURCE_BRANCH_DECISION_PATH = source_design.BRANCH_DECISION_PATH
SOURCE_PRUNE_MATRIX_PATH = source_design.PRUNE_MATRIX_PATH
SOURCE_FAILURE_MEMORY_PATH = source_design.FAILURE_MEMORY_PATH
SOURCE_REVIEW_RESULT_PATH = source_design.REVIEW_RESULT_PATH
SOURCE_DESIGN_REPORT_PATH = source_design.REPORT_PATH
SOURCE_INITIAL_SCOREBOARD_PATH = source_design.INITIAL_SCOREBOARD_PATH
SOURCE_MONTHLY_WEAKNESS_PATH = source_design.MONTHLY_WEAKNESS_PATH

SOURCE_DQ_VARIANT_MANIFEST_PATH = source_runtime_materializer.VARIANT_MANIFEST_PATH
SOURCE_DQ_ATTEMPT_MANIFEST_PATH = source_runtime_materializer.ATTEMPT_MANIFEST_PATH
SOURCE_DQ_RUNTIME_CONTRACT_PATH = source_runtime_materializer.RUNTIME_CONTRACT_PATH
SOURCE_DQ_HANDOFF_RECEIPT_PATH = source_runtime_materializer.HANDOFF_RECEIPT_PATH
SOURCE_DQ_REPORT_PATH = source_runtime_materializer.REPORT_PATH

SOURCE_CV_VARIANT_MANIFEST_PATH = source_aih_materializer.VARIANT_MANIFEST_PATH
SOURCE_CV_ATTEMPT_MANIFEST_PATH = source_aih_materializer.ATTEMPT_MANIFEST_PATH
SOURCE_CV_RUNTIME_CONTRACT_PATH = source_aih_materializer.RUNTIME_CONTRACT_PATH
SOURCE_CV_REPORT_PATH = source_aih_materializer.REPORT_PATH

SOURCE_FEATURE_MANIFEST_PATH = STAGE_ROOT / "02_runs" / "run267B" / "source_feature_manifest.csv"

MATERIALIZATION_PLAN_PATH = RUN_ROOT / "materialization_plan.csv"
QUEUE_DECISION_PATH = RUN_ROOT / "queue_decision.csv"
FEATURE_FRAME_MANIFEST_PATH = RUN_ROOT / "feature_frame_manifest.csv"
MODEL_MANIFEST_PATH = RUN_ROOT / "model_manifest.csv"
VARIANT_MANIFEST_PATH = RUN_ROOT / "variant_manifest.csv"
ATTEMPT_MANIFEST_PATH = RUN_ROOT / "attempt_manifest.csv"
RUNTIME_CONTRACT_PATH = RUN_ROOT / "runtime_contract.csv"
HELD_QUEUE_PATH = RUN_ROOT / "held_queue.csv"
PREFLIGHT_RECEIPT_PATH = RUN_ROOT / "preflight_handoff_receipt.csv"
SUPPLY_DIAGNOSTIC_PATH = RUN_ROOT / "pre_runtime_supply_diagnostic.csv"
REPLACEMENT_PREPLAN_PATH = RUN_ROOT / "similar_replacement_preplan.csv"
EXPERIMENT_DESIGN_RECEIPT_PATH = RUN_ROOT / "experiment_design_receipt.csv"
ENVIRONMENT_REPRODUCIBILITY_RECEIPT_PATH = RUN_ROOT / "environment_reproducibility_receipt.csv"
DATA_INTEGRITY_RECEIPT_PATH = RUN_ROOT / "data_integrity_receipt.csv"
RUNTIME_PARITY_RECEIPT_PATH = RUN_ROOT / "runtime_parity_receipt.csv"
RESULT_JUDGMENT_PATH = RUN_ROOT / "result_judgment.csv"
GATE_AUDIT_PATH = RUN_ROOT / "gate_audit.csv"
RUN_MANIFEST_PATH = RUN_ROOT / "run_manifest.json"
LINEAGE_PATH = RUN_ROOT / "lineage.json"
REVIEW_RESULT_PATH = RUN_ROOT / "review_result.json"
REPORT_PATH = REVIEWS_ROOT / "stage267_run267DU_runtime_gap_aware_fifth_followup_or_prune_materialization.md"
PRODUCER_PATH = Path("stage_pipelines/stage267/run267DU_runtime_gap_aware_fifth_followup_or_prune_materialization.py")

STAGE_LEDGER_PATH = source_design.STAGE_LEDGER_PATH
PROJECT_LEDGER_PATH = source_design.PROJECT_LEDGER_PATH
RUN_REGISTRY_PATH = source_design.RUN_REGISTRY_PATH
ARTIFACT_REGISTRY_PATH = source_design.ARTIFACT_REGISTRY_PATH
CURRENT_WORKING_STATE_PATH = source_design.CURRENT_WORKING_STATE_PATH
WORKSPACE_STATE_PATH = source_design.WORKSPACE_STATE_PATH
SELECTION_STATUS_PATH = source_design.SELECTION_STATUS_PATH
REVIEW_INDEX_PATH = source_design.REVIEW_INDEX_PATH

STAGE_LEDGER_COLUMNS = source_design.STAGE_LEDGER_COLUMNS
ARTIFACT_COLUMNS = source_design.ARTIFACT_COLUMNS

COMMON_ROOT = "OPV2/s267du/run267DU_runtime_gap_aware_fifth_followup_or_prune"
EXPLORATION_LABEL = "stage267_BaselineRacing__RuntimeGapAwareFifthFollowupOrPrune"
MATERIALIZATION_BOUNDARY = "materialization_only_execution_pending_no_candidate_selection_no_selected_research_baseline_no_onnx"
TIER_PAIR_BOUNDARY = (
    "Tier A and duplicate-boundary Tier A+B rows are materialized only where inputs exist; "
    "true Tier B fallback and actual routed total remain unclaimed"
)

PLAN_CONFIGS: tuple[dict[str, Any], ...] = (
    {
        "queue_id": "q01_s258_supply_continuity_table_handoff_repair",
        "source_kind": "dq",
        "source_variant_id": "run267dq_01_s258_stc_2023h2_supply_continuity_sidefilter_open",
        "variant_id": "run267du_01_s258_stc_2023h2_handoff_repair",
        "candidate_id": "s258_short_tight_control",
        "candidate_alias": "s258_stc",
        "candidate_role": "stress_challenger",
        "profile_label": "s258_stc_table_handoff_repair_2023h2",
        "profile_token": "s258_handoff_repair",
        "materialization_type": "copy_source_with_common_files_table_handoff_repair",
        "split": "adjacent_2023_h2_train_pre_2024",
        "period_label": "2023H2",
        "from_date": "2023.07.05",
        "to_date": "2024.01.01",
        "attempt_role": "handoff_repair_retry",
        "priority": "P0_repair",
        "set_updates": {},
        "known_difference": "Repairs Common Files table handoff for the completed source profile without changing the signal surface.",
    },
    {
        "queue_id": "q01_s258_supply_continuity_table_handoff_repair",
        "source_kind": "dq",
        "source_variant_id": "run267dq_02_s258_stc_2025h1_supply_continuity_sidefilter_open",
        "variant_id": "run267du_02_s258_stc_2025h1_handoff_repair",
        "candidate_id": "s258_short_tight_control",
        "candidate_alias": "s258_stc",
        "candidate_role": "stress_challenger",
        "profile_label": "s258_stc_table_handoff_repair_2025h1",
        "profile_token": "s258_handoff_repair",
        "materialization_type": "copy_source_with_common_files_table_handoff_repair",
        "split": "adjacent_2025_h1_validation_post_2024",
        "period_label": "2025H1",
        "from_date": "2025.01.02",
        "to_date": "2025.07.01",
        "attempt_role": "handoff_repair_retry",
        "priority": "P0_repair",
        "set_updates": {},
        "known_difference": "Repairs table handoff for 2025H1 and keeps the weak-period evidence separate from performance judgment.",
    },
    {
        "queue_id": "q01_s258_supply_continuity_table_handoff_repair",
        "source_kind": "dq",
        "source_variant_id": "run267dq_03_s258_stc_2025h2_supply_continuity_sidefilter_open",
        "variant_id": "run267du_03_s258_stc_2025h2_handoff_repair",
        "candidate_id": "s258_short_tight_control",
        "candidate_alias": "s258_stc",
        "candidate_role": "stress_challenger",
        "profile_label": "s258_stc_table_handoff_repair_2025h2",
        "profile_token": "s258_handoff_repair",
        "materialization_type": "copy_source_with_common_files_table_handoff_repair",
        "split": "adjacent_2025_h2_oos_followthrough",
        "period_label": "2025H2",
        "from_date": "2025.07.01",
        "to_date": "2026.01.01",
        "attempt_role": "handoff_repair_retry",
        "priority": "P0_repair",
        "set_updates": {},
        "known_difference": "Repairs table handoff for 2025H2 and keeps late-OOS quality evidence inspectable.",
    },
    {
        "queue_id": "q02_s258_noncalendar_impulse_reentry_cross_period",
        "source_kind": "dq",
        "source_variant_id": "run267dq_01_s258_stc_2023h2_supply_continuity_sidefilter_open",
        "variant_id": "run267du_04_s258_stc_2023h2_noncalendar_impulse",
        "candidate_id": "s258_short_tight_control",
        "candidate_alias": "s258_stc",
        "candidate_role": "stress_challenger",
        "profile_label": "s258_stc_noncalendar_impulse_2023h2",
        "profile_token": "s258_noncalendar_impulse",
        "materialization_type": "aggressive_set_shape_from_repaired_supply_surface",
        "split": "adjacent_2023_h2_train_pre_2024",
        "period_label": "2023H2",
        "from_date": "2023.07.05",
        "to_date": "2024.01.01",
        "attempt_role": "aggressive_noncalendar_impulse",
        "priority": "P0_aggressive",
        "set_updates": {
            "InpShortThreshold": "0.50",
            "InpLongThreshold": "0.48",
            "InpAtrStopMultiplier": "2.25",
            "InpAtrTakeProfitMultiplier": "5.10",
            "InpModelRiskMaxPct": "0.035",
            "InpMaxHoldBars": "4",
            "InpSideFilterEnabled": "false",
            "InpSameDirectionReentryCooldownBars": "0",
        },
        "known_difference": "Aggressively reopens impulse strength and ATR-z-like risk shape without adding calendar filters.",
    },
    {
        "queue_id": "q02_s258_noncalendar_impulse_reentry_cross_period",
        "source_kind": "dq",
        "source_variant_id": "run267dq_02_s258_stc_2025h1_supply_continuity_sidefilter_open",
        "variant_id": "run267du_05_s258_stc_2025h1_noncalendar_impulse",
        "candidate_id": "s258_short_tight_control",
        "candidate_alias": "s258_stc",
        "candidate_role": "stress_challenger",
        "profile_label": "s258_stc_noncalendar_impulse_2025h1",
        "profile_token": "s258_noncalendar_impulse",
        "materialization_type": "aggressive_set_shape_from_repaired_supply_surface",
        "split": "adjacent_2025_h1_validation_post_2024",
        "period_label": "2025H1",
        "from_date": "2025.01.02",
        "to_date": "2025.07.01",
        "attempt_role": "aggressive_noncalendar_impulse",
        "priority": "P0_aggressive",
        "set_updates": {
            "InpShortThreshold": "0.50",
            "InpLongThreshold": "0.48",
            "InpAtrStopMultiplier": "2.25",
            "InpAtrTakeProfitMultiplier": "5.10",
            "InpModelRiskMaxPct": "0.035",
            "InpMaxHoldBars": "4",
            "InpSideFilterEnabled": "false",
            "InpSameDirectionReentryCooldownBars": "0",
        },
        "known_difference": "Pressures the weak 2025H1 period with a noncalendar impulse shape instead of a new filter stack.",
    },
    {
        "queue_id": "q02_s258_noncalendar_impulse_reentry_cross_period",
        "source_kind": "dq",
        "source_variant_id": "run267dq_03_s258_stc_2025h2_supply_continuity_sidefilter_open",
        "variant_id": "run267du_06_s258_stc_2025h2_noncalendar_impulse",
        "candidate_id": "s258_short_tight_control",
        "candidate_alias": "s258_stc",
        "candidate_role": "stress_challenger",
        "profile_label": "s258_stc_noncalendar_impulse_2025h2",
        "profile_token": "s258_noncalendar_impulse",
        "materialization_type": "aggressive_set_shape_from_repaired_supply_surface",
        "split": "adjacent_2025_h2_oos_followthrough",
        "period_label": "2025H2",
        "from_date": "2025.07.01",
        "to_date": "2026.01.01",
        "attempt_role": "aggressive_noncalendar_impulse",
        "priority": "P0_aggressive",
        "set_updates": {
            "InpShortThreshold": "0.50",
            "InpLongThreshold": "0.48",
            "InpAtrStopMultiplier": "2.25",
            "InpAtrTakeProfitMultiplier": "5.10",
            "InpModelRiskMaxPct": "0.035",
            "InpMaxHoldBars": "4",
            "InpSideFilterEnabled": "false",
            "InpSameDirectionReentryCooldownBars": "0",
        },
        "known_difference": "Pressures 2025H2 follow-through with the same noncalendar impulse shape.",
    },
    {
        "queue_id": "q03_s264_aih_explosive_shock_state_oos_final_month",
        "source_kind": "canonical",
        "source_candidate_id": "s264_allow_inner_high_quarter",
        "source_split": "validation_is",
        "variant_id": "run267du_07_s264_aih_validation_explosive_shock_anchor",
        "candidate_id": "s264_allow_inner_high_quarter",
        "candidate_alias": "s264_aih",
        "candidate_role": "challenger_core",
        "profile_label": "s264_aih_validation_explosive_shock_anchor",
        "profile_token": "s264_aih_explosive_shock",
        "materialization_type": "canonical_score_table_explosive_set_shape_validation_anchor",
        "split": "validation_is",
        "period_label": "validation_is",
        "from_date": "2025.01.02",
        "to_date": "2025.10.01",
        "attempt_role": "validation_anchor_for_explosive_oos_probe",
        "priority": "P0_explosive",
        "set_updates": {
            "InpShortThreshold": "0.50",
            "InpLongThreshold": "0.48",
            "InpAtrStopMultiplier": "2.20",
            "InpAtrTakeProfitMultiplier": "5.05",
            "InpModelRiskMaxPct": "0.034",
            "InpMaxHoldBars": "4",
            "InpSideFilterEnabled": "false",
            "InpSameDirectionReentryCooldownBars": "0",
        },
        "known_difference": "Uses the canonical s264_aih validation surface as the damage anchor for the explosive OOS-final-month probe.",
    },
    {
        "queue_id": "q03_s264_aih_explosive_shock_state_oos_final_month",
        "source_kind": "canonical",
        "source_candidate_id": "s264_allow_inner_high_quarter",
        "source_split": "oos",
        "variant_id": "run267du_08_s264_aih_202604_explosive_shock_probe",
        "candidate_id": "s264_allow_inner_high_quarter",
        "candidate_alias": "s264_aih",
        "candidate_role": "challenger_core",
        "profile_label": "s264_aih_202604_explosive_shock_probe",
        "profile_token": "s264_aih_explosive_shock",
        "materialization_type": "canonical_score_table_explosive_set_shape_oos_final_month",
        "split": "oos_final_month_2026_04",
        "period_label": "2026.04",
        "from_date": "2026.04.01",
        "to_date": "2026.04.14",
        "attempt_role": "oos_final_month_explosive_probe",
        "priority": "P0_explosive",
        "set_updates": {
            "InpShortThreshold": "0.50",
            "InpLongThreshold": "0.48",
            "InpAtrStopMultiplier": "2.20",
            "InpAtrTakeProfitMultiplier": "5.05",
            "InpModelRiskMaxPct": "0.034",
            "InpMaxHoldBars": "4",
            "InpSideFilterEnabled": "false",
            "InpSameDirectionReentryCooldownBars": "0",
        },
        "known_difference": "Zooms directly into the 2026.04 OOS final-month weakness while preserving canonical s264_aih feature order.",
    },
    {
        "queue_id": "q04_s264_lc_defensive_dd_cluster_control",
        "source_kind": "canonical",
        "source_candidate_id": "s264_lowrank_control",
        "source_split": "oos",
        "variant_id": "run267du_09_s264_lc_202604_defensive_control",
        "candidate_id": "s264_lowrank_control",
        "candidate_alias": "s264_lc",
        "candidate_role": "defensive_control",
        "profile_label": "s264_lc_202604_defensive_control",
        "profile_token": "s264_lc_control",
        "materialization_type": "canonical_control_replay_for_same_oos_final_month",
        "split": "oos_final_month_2026_04",
        "period_label": "2026.04",
        "from_date": "2026.04.01",
        "to_date": "2026.04.14",
        "attempt_role": "defensive_control_same_month",
        "priority": "P0_control",
        "set_updates": {
            "InpShortThreshold": "0.54",
            "InpLongThreshold": "0.52",
            "InpAtrStopMultiplier": "2.0325",
            "InpAtrTakeProfitMultiplier": "4.615",
            "InpModelRiskMaxPct": "0.0305",
            "InpMaxHoldBars": "3",
            "InpSideFilterEnabled": "true",
            "InpSameDirectionReentryCooldownBars": "8",
        },
        "known_difference": "Keeps s264_lc as a same-month control receipt only; no safe-control or selected-candidate claim.",
    },
)

HELD_QUEUE_CONFIGS: tuple[dict[str, str], ...] = (
    {
        "queue_id": "q05_s264_aia_s262_lih_supply_manifest_diagnostic",
        "priority": "P1_diagnostic",
        "candidate_aliases": "s264_aia;s262_lih",
        "decision": "diagnostic_only_no_mt5_scheduled",
        "why": "run267DT(267DT 실행)는 nonzero activation proof(비영 활성 증명) 전 blind retry(무작정 재시도)를 금지했다.",
        "reopen_condition": "supply diagnostic(공급 진단)이 nonzero feature/model surface(비영 피처/모델 표면)를 확인한 뒤 별도 queue(대기열)를 연다.",
    },
    {
        "queue_id": "q06_s264_aih_s258_similar_feature_replacement",
        "priority": "P1_replacement",
        "candidate_aliases": "s264_aih;s258_stc",
        "decision": "held_until_q02_q03_shape_available",
        "why": "similar replacement(유사 피처 대체)는 q02/q03의 곡선/공급 형태가 나온 뒤 같은 의미 축이 버티는지 확인해야 한다.",
        "reopen_condition": "run267DV(267DV 실행) MT5 result(결과)가 q02/q03에서 붕괴하지 않는 shape(형태)를 보일 때.",
    },
)


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    item = Path(path)
    try:
        return item.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return item.as_posix()


def repo_path(path_text: str) -> Path:
    path = Path(path_text)
    return path if path.is_absolute() else REPO_ROOT / path


def cell(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, float):
        return f"{value:.12g}" if math.isfinite(value) else ""
    if isinstance(value, (list, tuple, set)):
        return ";".join(str(item) for item in value)
    return str(value)


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path_exists(path):
        return []
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str] | None = None) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    ordered: list[str] = []
    if columns:
        ordered.extend(columns)
    for row in rows:
        for key in row:
            if key not in ordered:
                ordered.append(str(key))
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=ordered)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: cell(row.get(key, "")) for key in ordered})


def write_json(path: Path, payload: Mapping[str, Any]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(
        json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8-sig",
    )


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text, encoding="utf-8-sig")


def write_key_values(path: Path, values: Mapping[str, Any], header: str | None = None) -> dict[str, str]:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    lines: list[str] = []
    if header:
        lines.append(header)
    for key, value in values.items():
        if isinstance(value, bool):
            rendered = "true" if value else "false"
        else:
            rendered = str(value)
        lines.append(f"{key}={rendered}")
    io_path(path).write_text("\n".join(lines) + "\n", encoding="utf-8-sig")
    return {"path": rel(path), "sha256": sha256_file_lf_normalized(path)}


def parse_key_values(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not path_exists(path):
        return values
    for line in io_path(path).read_text(encoding="utf-8-sig").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith(";") or stripped.startswith("[") or "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        values[key.strip()] = value.strip()
    return values


def source_by_id(rows: Sequence[Mapping[str, str]], key: str) -> dict[str, Mapping[str, str]]:
    return {str(row[key]): row for row in rows if row.get(key)}


def attempts_by_variant(rows: Sequence[Mapping[str, str]]) -> dict[str, list[Mapping[str, str]]]:
    out: dict[str, list[Mapping[str, str]]] = {}
    for row in rows:
        out.setdefault(str(row.get("variant_id", "")), []).append(row)
    return out


def feature_order_from_csv(path: Path) -> list[str]:
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.reader(handle)
        header = next(reader)
    return [column for column in header if column not in {"bar_time_server", "timestamp", "time", "datetime"}]


def feature_stats(path: Path) -> dict[str, Any]:
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        row_count = 0
        first_time = ""
        last_time = ""
        for row in reader:
            row_count += 1
            timestamp = row.get("bar_time_server") or row.get("timestamp") or row.get("time") or ""
            if row_count == 1:
                first_time = timestamp
            last_time = timestamp
    order = feature_order_from_csv(path)
    return {
        "feature_rows": row_count,
        "feature_count": len(order),
        "first_time": first_time,
        "last_time": last_time,
        "feature_order": ";".join(order),
        "feature_order_hash": ordered_hash(order),
    }


def copy_file(source: Path, destination: Path) -> dict[str, str]:
    if not path_exists(source):
        raise FileNotFoundError(source)
    io_path(destination.parent).mkdir(parents=True, exist_ok=True)
    shutil.copy2(io_path(source), io_path(destination))
    return {"source": rel(source), "path": rel(destination), "sha256": sha256_file_lf_normalized(destination)}


def canonical_source_rows() -> dict[tuple[str, str], Mapping[str, str]]:
    rows = read_csv(SOURCE_FEATURE_MANIFEST_PATH)
    return {(row["candidate_id"], row["split"]): row for row in rows}


def source_variant_rows() -> dict[str, Mapping[str, str]]:
    rows = read_csv(SOURCE_DQ_VARIANT_MANIFEST_PATH) + read_csv(SOURCE_CV_VARIANT_MANIFEST_PATH)
    return source_by_id(rows, "variant_id")


def source_attempt_rows() -> dict[str, list[Mapping[str, str]]]:
    rows = read_csv(SOURCE_DQ_ATTEMPT_MANIFEST_PATH) + read_csv(SOURCE_CV_ATTEMPT_MANIFEST_PATH)
    return attempts_by_variant(rows)


def source_inputs_for_plan(
    plan: Mapping[str, Any],
    variant_by_id: Mapping[str, Mapping[str, str]],
    canonical_by_key: Mapping[tuple[str, str], Mapping[str, str]],
) -> dict[str, Any]:
    if plan["source_kind"] == "dq":
        source_variant = variant_by_id[str(plan["source_variant_id"])]
        return {
            "source_run_id": source_variant.get("source_run_id") or SOURCE_RUNTIME_RUN_ID,
            "source_variant_id": source_variant["variant_id"],
            "source_feature_path": source_variant["runtime_feature_file"],
            "source_model_path": source_variant["runtime_model_file"],
            "source_feature_sha256": source_variant.get("runtime_feature_sha256", ""),
            "source_model_sha256": source_variant.get("runtime_model_sha256", ""),
            "source_profile_label": source_variant.get("profile_label", ""),
        }
    source_row = canonical_by_key[(str(plan["source_candidate_id"]), str(plan["source_split"]))]
    return {
        "source_run_id": "stage267_run267B_source_feature_manifest",
        "source_variant_id": f"{source_row['candidate_id']}_{source_row['split']}",
        "source_feature_path": source_row["feature_file"],
        "source_model_path": source_row["model_file"],
        "source_feature_sha256": sha256_file_lf_normalized(repo_path(source_row["feature_file"])),
        "source_model_sha256": sha256_file_lf_normalized(repo_path(source_row["model_file"])),
        "source_profile_label": f"canonical_{source_row['candidate_id']}_{source_row['split']}",
    }


def source_attempt_for_plan(
    plan: Mapping[str, Any],
    source_attempts: Mapping[str, Sequence[Mapping[str, str]]],
) -> Mapping[str, str] | None:
    if plan["source_kind"] != "dq":
        return None
    attempts = source_attempts.get(str(plan["source_variant_id"]), [])
    if not attempts:
        return None
    period = str(plan["period_label"]).lower()
    for attempt in attempts:
        attempt_name = str(attempt.get("attempt_name", "")).lower()
        if period.replace(".", "") in attempt_name or period in attempt_name:
            return attempt
    return attempts[0]


def base_set_values(plan: Mapping[str, Any], source_attempt: Mapping[str, str] | None) -> dict[str, str]:
    if source_attempt and source_attempt.get("set_path"):
        values = parse_key_values(repo_path(str(source_attempt["set_path"])))
    else:
        values = {
            "InpMainSymbol": "US100",
            "InpTimeframe": "5",
            "InpModelBackend": "ebm_table",
            "InpModelUseCommonFiles": "true",
            "InpFeatureCsvUseCommonFiles": "true",
            "InpFeatureRequireTimestampMatch": "true",
            "InpFeatureAllowLatestFallback": "false",
            "InpFeatureStrictHeader": "true",
            "InpCsvTimestampIsBarClose": "true",
            "InpFallbackEnabled": "false",
            "InpFallbackTierLabel": "Tier B partial-context fallback",
            "InpTelemetryUseCommonFiles": "true",
            "InpShortThreshold": "0.54",
            "InpLongThreshold": "0.52",
            "InpMinMargin": "0",
            "InpInvertSignal": "false",
            "InpAllowTrading": "true",
            "InpFixedLot": "0.25",
            "InpCloseOnFlatSignal": "false",
            "InpReverseOnOppositeSignal": "true",
            "InpCloseOnlyOnOppositeSignal": "false",
            "InpMaxHoldBars": "3",
            "InpMaxConcurrentPositions": "1",
            "InpAtrSltpEnabled": "true",
            "InpAtrPeriod": "14",
            "InpAtrStopMultiplier": "2.0325",
            "InpAtrTakeProfitMultiplier": "4.615",
            "InpAtrMinStopPoints": "0",
            "InpAtrMaxStopPoints": "0",
            "InpAtrMinTakeProfitPoints": "0",
            "InpAtrMaxTakeProfitPoints": "0",
            "InpModelRiskSizingEnabled": "true",
            "InpModelRiskMinPct": "0.005",
            "InpModelRiskMaxPct": "0.0305",
            "InpModelRiskConfidenceFloor": "0.5",
            "InpModelRiskConfidenceCeiling": "0.6",
            "InpModelRiskFallbackLot": "0.25",
            "InpFallbackUseOnPrimaryFlat": "false",
            "InpFallbackUseOnPrimaryLowConfidence": "false",
            "InpReentryCooldownBars": "0",
            "InpSameDirectionReentryCooldownBars": "8",
            "InpEntryTransitionOnly": "false",
            "InpEntryTransitionRearmMinConfidenceDelta": "0",
            "InpSideFilterEnabled": "true",
            "InpSideFilterFeatureIndex": "2",
            "InpFallbackSideFilterFeatureIndex": "2",
            "InpBlockShortFeatureRange": "false",
            "InpBlockLongFeatureRange": "false",
        }
    values.update({key: str(value) for key, value in plan.get("set_updates", {}).items()})
    return values


def materialize_plan(
    plan: Mapping[str, Any],
    variant_by_id: Mapping[str, Mapping[str, str]],
    source_attempts: Mapping[str, Sequence[Mapping[str, str]]],
    canonical_by_key: Mapping[tuple[str, str], Mapping[str, str]],
    magic_index: int,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    source_info = source_inputs_for_plan(plan, variant_by_id, canonical_by_key)
    source_feature = repo_path(str(source_info["source_feature_path"]))
    source_model = repo_path(str(source_info["source_model_path"]))
    variant_id = str(plan["variant_id"])
    candidate_alias = str(plan["candidate_alias"])
    feature_path = FEATURE_ROOT / candidate_alias / variant_id / f"{variant_id}_features.csv"
    model_path = VARIANT_ROOT / candidate_alias / variant_id / "models" / f"{variant_id}_model.csv"
    feature_copy = copy_file(source_feature, feature_path)
    model_copy = copy_file(source_model, model_path)
    stats = feature_stats(feature_path)
    common_base = f"{COMMON_ROOT}/{candidate_alias}/{variant_id}"
    common_feature_path = f"{common_base}/features/{feature_path.name}"
    common_model_path = f"{common_base}/models/{model_path.name}"
    common_feature = copy_to_common(feature_path, common_feature_path, COMMON_FILES_ROOT_DEFAULT)
    common_model = copy_to_common(model_path, common_model_path, COMMON_FILES_ROOT_DEFAULT)
    feature_order = stats["feature_order"]
    feature_order_hash = stats["feature_order_hash"]
    source_attempt = source_attempt_for_plan(plan, source_attempts)
    attempt_name = f"{variant_id}_{str(plan['period_label']).lower().replace('.', '')}"
    telemetry = f"{common_base}/telemetry/{attempt_name}_telemetry.csv"
    summary = f"{common_base}/telemetry/{attempt_name}_summary.csv"
    set_values = base_set_values(plan, source_attempt)
    set_values.update(
        {
            "InpRunId": RUN_ID,
            "InpExplorationLabel": EXPLORATION_LABEL,
            "InpTierLabel": "Tier A",
            "InpPrimaryActiveTier": "tier_a",
            "InpSplitLabel": plan["split"],
            "InpMainSymbol": "US100",
            "InpTimeframe": "5",
            "InpModelPath": common_model_path,
            "InpModelId": f"{RUN_ID}_{variant_id}",
            "InpModelBackend": "ebm_table",
            "InpModelUseCommonFiles": "true",
            "InpFeatureCsvPath": common_feature_path,
            "InpFeatureCount": str(stats["feature_count"]),
            "InpFeatureCsvUseCommonFiles": "true",
            "InpFeatureRequireTimestampMatch": "true",
            "InpFeatureAllowLatestFallback": "false",
            "InpFeatureStrictHeader": "true",
            "InpCsvTimestampIsBarClose": "true",
            "InpFeatureOrderHash": feature_order_hash,
            "InpFallbackEnabled": "false",
            "InpFallbackFeatureCsvPath": common_feature_path,
            "InpFallbackFeatureCount": str(stats["feature_count"]),
            "InpFallbackModelPath": common_model_path,
            "InpFallbackModelId": f"{RUN_ID}_{variant_id}_fallback_boundary_disabled",
            "InpFallbackModelBackend": "ebm_table",
            "InpFallbackFeatureOrderHash": feature_order_hash,
            "InpTelemetryCsvPath": telemetry,
            "InpSummaryCsvPath": summary,
            "InpTelemetryUseCommonFiles": "true",
            "InpMagic": str(26741000 + magic_index),
        }
    )
    set_payload = write_key_values(
        MT5_ROOT / f"{attempt_name}.set",
        set_values,
        header="; generated_by=run267DU_runtime_gap_aware_fifth_followup_or_prune_materialization",
    )
    ini_payload = write_key_values(
        MT5_ROOT / f"{attempt_name}.ini",
        {
            "Expert": r"Project_Obsidian_Prime_v2\foundation\mt5\ObsidianPrimeV2_RuntimeProbeEA.ex5",
            "Symbol": "US100",
            "Period": "M5",
            "Model": "4",
            "Deposit": "500",
            "Leverage": "1:100",
            "Optimization": "0",
            "ExecutionMode": "0",
            "ForwardMode": "0",
            "UseLocal": "1",
            "UseRemote": "0",
            "UseCloud": "0",
            "ReplaceReport": "1",
            "ShutdownTerminal": "1",
            "FromDate": plan["from_date"],
            "ToDate": plan["to_date"],
            "Report": f"Project_Obsidian_Prime_v2_{RUN_NUMBER}_{attempt_name}",
            "ExpertParameters": f"{attempt_name}.set",
        },
        header="[Tester]",
    )
    variant = {
        "variant_id": variant_id,
        "queue_id": plan["queue_id"],
        "priority": plan["priority"],
        "source_run_id": source_info["source_run_id"],
        "source_variant_id": source_info["source_variant_id"],
        "candidate_id": plan["candidate_id"],
        "candidate_alias": candidate_alias,
        "candidate_role": plan["candidate_role"],
        "profile_label": plan["profile_label"],
        "profile_token": plan["profile_token"],
        "materialization_type": plan["materialization_type"],
        "split": plan["split"],
        "period_label": plan["period_label"],
        "runtime_model_file": model_copy["path"],
        "runtime_model_sha256": model_copy["sha256"],
        "common_model_path": common_model["common_path"],
        "common_model_sha256": common_model["sha256"],
        "runtime_feature_file": feature_copy["path"],
        "runtime_feature_sha256": feature_copy["sha256"],
        "common_feature_path": common_feature["common_path"],
        "common_feature_sha256": common_feature["sha256"],
        "feature_count": stats["feature_count"],
        "feature_order": feature_order,
        "feature_order_hash": feature_order_hash,
        "known_difference": plan["known_difference"],
        "materialization_boundary": MATERIALIZATION_BOUNDARY,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    feature_row = {
        "variant_id": variant_id,
        "candidate_alias": candidate_alias,
        "source_feature_path": source_info["source_feature_path"],
        "runtime_feature_file": feature_copy["path"],
        "runtime_feature_sha256": feature_copy["sha256"],
        "common_feature_path": common_feature["common_path"],
        "feature_rows": stats["feature_rows"],
        "feature_count": stats["feature_count"],
        "first_time": stats["first_time"],
        "last_time": stats["last_time"],
        "feature_order_hash": feature_order_hash,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    model_row = {
        "variant_id": variant_id,
        "candidate_alias": candidate_alias,
        "source_model_path": source_info["source_model_path"],
        "runtime_model_file": model_copy["path"],
        "runtime_model_sha256": model_copy["sha256"],
        "common_model_path": common_model["common_path"],
        "common_model_sha256": common_model["sha256"],
        "model_backend": "ebm_table",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    attempt = {
        "attempt_name": attempt_name,
        "variant_id": variant_id,
        "queue_id": plan["queue_id"],
        "priority": plan["priority"],
        "candidate_id": plan["candidate_id"],
        "candidate_alias": candidate_alias,
        "candidate_role": plan["candidate_role"],
        "profile_label": plan["profile_label"],
        "tier": "Tier A",
        "split": plan["split"],
        "period_label": plan["period_label"],
        "from_date": plan["from_date"],
        "to_date": plan["to_date"],
        "attempt_role": plan["attempt_role"],
        "set_path": set_payload["path"],
        "set_sha256": set_payload["sha256"],
        "ini_path": ini_payload["path"],
        "ini_sha256": ini_payload["sha256"],
        "telemetry_path": telemetry,
        "summary_path": summary,
        "execution_status": "materialized_execution_pending",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    preflight = {
        "attempt_name": attempt_name,
        "variant_id": variant_id,
        "queue_id": plan["queue_id"],
        "candidate_alias": candidate_alias,
        "feature_exists": path_exists(feature_path),
        "model_exists": path_exists(model_path),
        "common_feature_path": common_feature["common_path"],
        "common_feature_sha256": common_feature["sha256"],
        "common_model_path": common_model["common_path"],
        "common_model_sha256": common_model["sha256"],
        "set_path": set_payload["path"],
        "ini_path": ini_payload["path"],
        "preflight_status": "ready_for_mt5_execution",
        "effect": "Common Files handoff(공통 파일 인계)을 먼저 증명해 ebm_table_open_failed(EBM 테이블 열기 실패)를 성능 결과와 분리한다.",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    return variant, feature_row, model_row, attempt, preflight


def materialization_plan_rows(queue_rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    queue_by_id = {row["queue_id"]: row for row in queue_rows}
    rows: list[dict[str, Any]] = []
    for plan in PLAN_CONFIGS:
        queue = queue_by_id[str(plan["queue_id"])]
        rows.append(
            {
                "plan_id": plan["variant_id"],
                "queue_id": plan["queue_id"],
                "priority": plan["priority"],
                "candidate_alias": plan["candidate_alias"],
                "candidate_id": plan["candidate_id"],
                "workstream": queue.get("workstream"),
                "materialization_type": plan["materialization_type"],
                "split": plan["split"],
                "period_label": plan["period_label"],
                "source_kind": plan["source_kind"],
                "source_variant_id": plan.get("source_variant_id") or f"{plan.get('source_candidate_id')}_{plan.get('source_split')}",
                "changed_variables": queue.get("changed_variables"),
                "control_variables": queue.get("control_variables"),
                "known_difference": plan["known_difference"],
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def diagnostic_rows(canonical_by_key: Mapping[tuple[str, str], Mapping[str, str]]) -> list[dict[str, Any]]:
    alias_map = {
        "s264_allow_inner_all_oos_anchor": "s264_aia",
        "s262_lowrank_inner_half_filter": "s262_lih",
    }
    rows: list[dict[str, Any]] = []
    for candidate_id, alias in alias_map.items():
        for split in ("validation_is", "oos"):
            source = canonical_by_key[(candidate_id, split)]
            feature_path = repo_path(source["feature_file"])
            model_path = repo_path(source["model_file"])
            stats = feature_stats(feature_path)
            rows.append(
                {
                    "diagnostic_id": f"run267du_diag_{alias}_{split}",
                    "queue_id": "q05_s264_aia_s262_lih_supply_manifest_diagnostic",
                    "candidate_id": candidate_id,
                    "candidate_alias": alias,
                    "split": split,
                    "feature_file": source["feature_file"],
                    "feature_sha256": sha256_file_lf_normalized(feature_path),
                    "model_file": source["model_file"],
                    "model_sha256": sha256_file_lf_normalized(model_path),
                    "feature_rows": stats["feature_rows"],
                    "feature_count": stats["feature_count"],
                    "first_time": stats["first_time"],
                    "last_time": stats["last_time"],
                    "pre_runtime_supply_status": "source_surface_present_mt5_activation_unproven",
                    "mt5_schedule_status": "held_no_mt5_until_nonzero_activation_proof",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    return rows


def held_queue_rows() -> list[dict[str, Any]]:
    return [
        {
            **row,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for row in HELD_QUEUE_CONFIGS
    ]


def replacement_preplan_rows() -> list[dict[str, Any]]:
    return [
        {
            "preplan_id": "run267du_q06_trend_strength_replacement",
            "queue_id": "q06_s264_aih_s258_similar_feature_replacement",
            "candidate_aliases": "s264_aih;s258_stc",
            "replacement_axis": "ADX-like trend strength(ADX류 추세 강도) -> vortex/supertrend/range-pressure proxy(대체 축)",
            "status": "held_until_runtime_shape_available",
            "reason": "q02/q03 MT5 shape(형태) 없이 replacement(대체)를 먼저 돌리면 단일 지표 미세조정 루프가 된다.",
            "next_condition": "open after run267DV balance/equity(잔액/평가금) and trade quality(거래 품질) review.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def queue_decision_rows(
    queue_rows: Sequence[Mapping[str, str]],
    variant_rows: Sequence[Mapping[str, Any]],
    attempt_rows: Sequence[Mapping[str, Any]],
    held_rows: Sequence[Mapping[str, Any]],
    diagnostic_count: int,
) -> list[dict[str, Any]]:
    variants_by_queue: dict[str, int] = {}
    attempts_by_queue: dict[str, int] = {}
    for row in variant_rows:
        queue_id = str(row["queue_id"])
        variants_by_queue[queue_id] = variants_by_queue.get(queue_id, 0) + 1
    for row in attempt_rows:
        queue_id = str(row["queue_id"])
        attempts_by_queue[queue_id] = attempts_by_queue.get(queue_id, 0) + 1
    held_by_id = {str(row["queue_id"]): row for row in held_rows}
    rows: list[dict[str, Any]] = []
    for queue in queue_rows:
        queue_id = str(queue["queue_id"])
        held = held_by_id.get(queue_id)
        if held:
            decision = str(held["decision"])
            effect = "보류 이유와 재개 조건을 남겨 blind retry(무작정 재시도)를 막는다."
        else:
            decision = "materialized_for_mt5_execution"
            effect = "다음 MT5(MetaTrader 5, 메타트레이더5) 실행에서 곡선/약점 구간/거래 품질을 볼 수 있다."
        rows.append(
            {
                "queue_id": queue_id,
                "priority": queue.get("priority"),
                "candidate_aliases": queue.get("candidate_aliases"),
                "workstream": queue.get("workstream"),
                "decision": decision,
                "variant_count": variants_by_queue.get(queue_id, 0),
                "attempt_count": attempts_by_queue.get(queue_id, 0),
                "diagnostic_rows": diagnostic_count if queue_id == "q05_s264_aia_s262_lih_supply_manifest_diagnostic" else 0,
                "effect": effect,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def runtime_contract_rows(variant_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "variant_id": row["variant_id"],
            "candidate_alias": row["candidate_alias"],
            "queue_id": row["queue_id"],
            "shared_contract": "US100 M5;RuntimeProbeEA;ebm_table_csv;feature_order_hash_tracked;Common Files handoff",
            "tier_pair_boundary": TIER_PAIR_BOUNDARY,
            "runtime_status": "materialized_execution_pending",
            "runtime_claim": "runtime reproduction pending(런타임 재현 대기)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for row in variant_rows
    ]


def experiment_design_rows() -> list[dict[str, Any]]:
    return [
        {
            "design_id": "run267du_runtime_gap_aware_materialization",
            "hypothesis": "s258 table failures can be separated from performance, while s264_aih can be re-pressured aggressively on validation and 2026.04 without selecting a candidate.",
            "decision_use": "prepare run267DV MT5 batch and keep q05/q06 held with explicit reopen conditions.",
            "comparison_baseline": "run267DT materialization queue and Stage267 initial scoreboard final-month weakness.",
            "control_variables": "US100 M5, candidate pool, source feature order, RuntimeProbeEA, no selected baseline.",
            "changed_variables": "Common Files handoff repair, s258 noncalendar impulse set shape, s264_aih final-month explosive set shape, s264_lc same-month control.",
            "sample_scope": "s258 2023H2/2025H1/2025H2, s264_aih validation_is and 2026.04, s264_lc 2026.04 control, q05 diagnostics, q06 held.",
            "success_criteria": "all materialized attempts have feature/model/set/ini hashes and held rows remain explicit.",
            "failure_criteria": "missing source artifact, missing Common Files handoff, hidden candidate selection, or filter-stack drift.",
            "invalid_conditions": "feature order mismatch, data leakage, missing report, or false runtime claim.",
            "stop_conditions": "q01 has one repair retry only; q06 opens only after q02/q03 runtime shape exists.",
            "evidence_plan": "variant_manifest;attempt_manifest;preflight_handoff_receipt;runtime_contract;gate_audit;ledgers.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def environment_rows(counts: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "check_id": "run267du_environment_reproducibility",
            "status": "pass" if counts["variants"] == counts["preflight_receipts"] else "fail",
            "evidence": "feature/model copies, Common Files handoff hashes, set/ini manifests",
            "effect": "다음 실행이 같은 입력을 다시 찾을 수 있다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def data_integrity_rows(feature_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "check_id": "run267du_feature_order_integrity",
            "status": "pass" if feature_rows and all(row.get("feature_order_hash") for row in feature_rows) else "fail",
            "feature_frames": len(feature_rows),
            "evidence": "feature_frame_manifest includes feature_order_hash for every materialized variant",
            "effect": "feature order drift(피처 순서 드리프트)를 다음 실행 전에 잡는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def runtime_parity_rows(variant_rows: Sequence[Mapping[str, Any]], attempt_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "check_id": "run267du_runtime_handoff_ready",
            "status": "pass" if variant_rows and attempt_rows else "fail",
            "variants": len(variant_rows),
            "attempts": len(attempt_rows),
            "evidence": "variant_manifest;attempt_manifest;runtime_contract;preflight_handoff_receipt",
            "runtime_claim": "materialized_execution_pending_only",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def result_judgment_rows(counts: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "result_subject": RUN_ID,
            "evidence_available": "materialization manifests, handoff receipts, diagnostics, gate audit, ledgers",
            "evidence_missing": "MT5 execution output, KPI, balance/equity curve, trade list, Adapter finalization, ONNX parity",
            "judgment_label": "materialization_completed_execution_pending",
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": NEXT_ACTION,
            "user_explanation_hook": f"variants={counts['variants']};attempts={counts['attempts']};held={counts['held_rows']};diagnostics={counts['diagnostics']}",
        }
    ]


def gate_audit_rows(counts: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "queue_accounting_gate",
            "gate_name": "run267DT queue rows accounted",
            "status": "pass" if counts["queue_rows"] == 6 and counts["materialized_queue_rows"] == 4 and counts["held_rows"] == 2 else "fail",
            "evidence": f"queue_rows={counts['queue_rows']};materialized_queue_rows={counts['materialized_queue_rows']};held_rows={counts['held_rows']}",
            "effect": "물질화 축과 보류 축을 숨기지 않는다.",
        },
        {
            "gate_id": "aggressive_branch_gate",
            "gate_name": "aggressive and explosive rows materialized",
            "status": "pass" if counts["aggressive_variants"] >= 5 and counts["s264_aih_variants"] >= 2 else "fail",
            "evidence": f"aggressive_variants={counts['aggressive_variants']};s264_aih_variants={counts['s264_aih_variants']}",
            "effect": "방어적인 control(대조)만 반복하지 않고 공격형 실험을 실제 실행 입력으로 만든다.",
        },
        {
            "gate_id": "handoff_repair_gate",
            "gate_name": "preflight handoff receipts exist",
            "status": "pass" if counts["preflight_receipts"] == counts["variants"] else "fail",
            "evidence": f"preflight_receipts={counts['preflight_receipts']};variants={counts['variants']}",
            "effect": "EBM table handoff(EBM 테이블 인계) 실패를 다음 실행 전에 좁게 확인한다.",
        },
        {
            "gate_id": "final_claim_guard",
            "gate_name": "forbidden claims withheld",
            "status": "pass",
            "evidence": "selected_candidate=none;selected_research_baseline=none;onnx_readiness=not_claimed;goal_achieve=not_claimed",
            "effect": "물질화 완료를 후보 선정이나 ONNX 준비로 과장하지 않는다.",
        },
    ]


def output_paths() -> dict[str, str]:
    return {
        "materialization_plan": rel(MATERIALIZATION_PLAN_PATH),
        "queue_decision": rel(QUEUE_DECISION_PATH),
        "feature_frame_manifest": rel(FEATURE_FRAME_MANIFEST_PATH),
        "model_manifest": rel(MODEL_MANIFEST_PATH),
        "variant_manifest": rel(VARIANT_MANIFEST_PATH),
        "attempt_manifest": rel(ATTEMPT_MANIFEST_PATH),
        "runtime_contract": rel(RUNTIME_CONTRACT_PATH),
        "held_queue": rel(HELD_QUEUE_PATH),
        "preflight_handoff_receipt": rel(PREFLIGHT_RECEIPT_PATH),
        "pre_runtime_supply_diagnostic": rel(SUPPLY_DIAGNOSTIC_PATH),
        "similar_replacement_preplan": rel(REPLACEMENT_PREPLAN_PATH),
        "experiment_design_receipt": rel(EXPERIMENT_DESIGN_RECEIPT_PATH),
        "environment_reproducibility_receipt": rel(ENVIRONMENT_REPRODUCIBILITY_RECEIPT_PATH),
        "data_integrity_receipt": rel(DATA_INTEGRITY_RECEIPT_PATH),
        "runtime_parity_receipt": rel(RUNTIME_PARITY_RECEIPT_PATH),
        "result_judgment": rel(RESULT_JUDGMENT_PATH),
        "gate_audit": rel(GATE_AUDIT_PATH),
        "run_manifest": rel(RUN_MANIFEST_PATH),
        "lineage": rel(LINEAGE_PATH),
        "review_result": rel(REVIEW_RESULT_PATH),
        "report": rel(REPORT_PATH),
    }


def source_paths() -> dict[str, str]:
    return {
        "source_queue": rel(SOURCE_QUEUE_PATH),
        "source_feature_blueprint": rel(SOURCE_FEATURE_BLUEPRINT_PATH),
        "source_branch_decision": rel(SOURCE_BRANCH_DECISION_PATH),
        "source_prune_matrix": rel(SOURCE_PRUNE_MATRIX_PATH),
        "source_failure_memory": rel(SOURCE_FAILURE_MEMORY_PATH),
        "source_review_result": rel(SOURCE_REVIEW_RESULT_PATH),
        "source_design_report": rel(SOURCE_DESIGN_REPORT_PATH),
        "source_initial_scoreboard": rel(SOURCE_INITIAL_SCOREBOARD_PATH),
        "source_monthly_weakness": rel(SOURCE_MONTHLY_WEAKNESS_PATH),
        "source_dq_variant_manifest": rel(SOURCE_DQ_VARIANT_MANIFEST_PATH),
        "source_dq_attempt_manifest": rel(SOURCE_DQ_ATTEMPT_MANIFEST_PATH),
        "source_dq_runtime_contract": rel(SOURCE_DQ_RUNTIME_CONTRACT_PATH),
        "source_dq_handoff_receipt": rel(SOURCE_DQ_HANDOFF_RECEIPT_PATH),
        "source_dq_report": rel(SOURCE_DQ_REPORT_PATH),
        "source_cv_variant_manifest": rel(SOURCE_CV_VARIANT_MANIFEST_PATH),
        "source_cv_attempt_manifest": rel(SOURCE_CV_ATTEMPT_MANIFEST_PATH),
        "source_cv_runtime_contract": rel(SOURCE_CV_RUNTIME_CONTRACT_PATH),
        "source_cv_report": rel(SOURCE_CV_REPORT_PATH),
        "source_feature_manifest": rel(SOURCE_FEATURE_MANIFEST_PATH),
    }


def run_manifest(result: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "source_runtime_run_id": SOURCE_RUNTIME_RUN_ID,
        "source_aih_run_id": SOURCE_AIH_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "created_at_utc": result["created_at_utc"],
        "claim_boundary": CLAIM_BOUNDARY,
        "materialization_boundary": MATERIALIZATION_BOUNDARY,
        "tier_pair_boundary": TIER_PAIR_BOUNDARY,
        "sources": result["sources"],
        "outputs": result["outputs"],
        "counts": result["counts"],
        "next_action": NEXT_ACTION,
    }


def lineage(result: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "source_inputs": result["sources"],
        "producer": rel(PRODUCER_PATH),
        "consumer": NEXT_ACTION,
        "artifact_paths": result["outputs"],
        "artifact_hashes": "registered_in_artifact_registry(산출물 등록부에 기록)",
        "registry_links": {
            "stage_ledger": rel(STAGE_LEDGER_PATH),
            "project_ledger": rel(PROJECT_LEDGER_PATH),
            "run_registry": rel(RUN_REGISTRY_PATH),
            "artifact_registry": rel(ARTIFACT_REGISTRY_PATH),
        },
        "availability": "tracked_and_common_files_handoff",
        "lineage_judgment": "connected_with_boundary_no_selection",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def report_markdown(result: Mapping[str, Any]) -> str:
    counts = result["counts"]
    queue_lines = [
        "| queue_id(대기열 ID) | decision(판단) | variants(변형) | attempts(시도) |",
        "|---|---|---:|---:|",
    ]
    for row in result["queue_decision"]:
        queue_lines.append(
            f"| `{row['queue_id']}` | {row['decision']} | {row['variant_count']} | {row['attempt_count']} |"
        )
    return "\n".join(
        [
            "# Stage267 Run267DU Runtime Gap Aware Fifth Follow-Up/Prune Materialization(267단계 267DU 런타임 공백 반영 5차 후속/가지치기 물질화)",
            "",
            f"- status(상태): `{STATUS}`",
            f"- parent_run(부모 실행): `{PARENT_RUN_ID}`",
            f"- variants(변형): `{counts['variants']}`",
            f"- attempts(시도): `{counts['attempts']}`",
            f"- aggressive_variants(공격형 변형): `{counts['aggressive_variants']}`",
            f"- held_queue_rows(보류 대기열 행): `{counts['held_rows']}`",
            f"- diagnostics(진단): `{counts['diagnostics']}`",
            f"- next_action(다음 행동): `{NEXT_ACTION}`",
            "- selected_candidate(선택 후보): `none`",
            "- selected_research_baseline(선택 연구 기준 후보): `none`",
            "- ONNX readiness(ONNX 준비): `not_claimed`",
            "- Goal Achieve(목표 달성): `not_claimed`",
            "",
            "## Easy Read(쉬운 설명)",
            "",
            "run267DU(267DU 실행)는 run267DT(267DT 실행)의 설계 queue(대기열)를 MT5(MetaTrader 5, 메타트레이더5) 실행 가능한 입력으로 바꿨다.",
            "효과: s258_stc(258 STC)는 table handoff repair(테이블 인계 수리)와 aggressive noncalendar impulse(공격형 비달력 충격)를 분리했고, s264_aih(264 AIH)는 validation anchor(검증 앵커)와 2026.04 final month(2026년 4월 마지막 표본외 월)를 직접 압박하게 했다.",
            "s264_lc(264 LC)는 same-month control(같은 월 대조)로만 남겼고, s264_aia/s262_lih(264 AIA/262 LIH)는 blind retry(무작정 재시도) 없이 supply diagnostic(공급 진단)으로 보류했다.",
            "",
            "## Queue Decisions(대기열 판단)",
            "",
            *queue_lines,
            "",
            "## Boundary(경계)",
            "",
            "이 실행은 materialization(물질화)이다. 아직 MT5 KPI(MT5 핵심 성과 지표), balance/equity curve(잔액/평가금 곡선), trade quality(거래 품질), Adapter finalization(어댑터 최종화), ONNX parity(ONNX 동등성)는 없다.",
            "따라서 selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 모두 주장하지 않는다.",
            "",
            "## Artifacts(산출물)",
            "",
            f"- materialization_plan(물질화 계획): `{rel(MATERIALIZATION_PLAN_PATH)}`",
            f"- variant_manifest(변형 목록): `{rel(VARIANT_MANIFEST_PATH)}`",
            f"- attempt_manifest(시도 목록): `{rel(ATTEMPT_MANIFEST_PATH)}`",
            f"- runtime_contract(런타임 계약): `{rel(RUNTIME_CONTRACT_PATH)}`",
            f"- preflight_handoff_receipt(사전 인계 영수증): `{rel(PREFLIGHT_RECEIPT_PATH)}`",
            f"- supply_diagnostic(공급 진단): `{rel(SUPPLY_DIAGNOSTIC_PATH)}`",
            f"- gate_audit(게이트 감사): `{rel(GATE_AUDIT_PATH)}`",
        ]
    ) + "\n"


def artifact_rows(created_at: str, result: Mapping[str, Any]) -> list[dict[str, Any]]:
    specs: list[tuple[str, str, Path, str]] = [
        ("stage267_run267DU_producer", "producer_script", PRODUCER_PATH, "Builds run267DU materialization package."),
        ("stage267_run267DU_materialization_plan", "materialization_plan", MATERIALIZATION_PLAN_PATH, "Materialization plan."),
        ("stage267_run267DU_queue_decision", "queue_decision", QUEUE_DECISION_PATH, "Queue decisions."),
        ("stage267_run267DU_feature_frame_manifest", "feature_frame_manifest", FEATURE_FRAME_MANIFEST_PATH, "Feature frame manifest."),
        ("stage267_run267DU_model_manifest", "model_manifest", MODEL_MANIFEST_PATH, "Model manifest."),
        ("stage267_run267DU_variant_manifest", "variant_manifest", VARIANT_MANIFEST_PATH, "Variant manifest."),
        ("stage267_run267DU_attempt_manifest", "attempt_manifest", ATTEMPT_MANIFEST_PATH, "Attempt manifest."),
        ("stage267_run267DU_runtime_contract", "runtime_contract", RUNTIME_CONTRACT_PATH, "Runtime contract."),
        ("stage267_run267DU_held_queue", "held_queue", HELD_QUEUE_PATH, "Held queue."),
        ("stage267_run267DU_preflight_handoff", "preflight_handoff_receipt", PREFLIGHT_RECEIPT_PATH, "Preflight handoff receipt."),
        ("stage267_run267DU_supply_diagnostic", "pre_runtime_supply_diagnostic", SUPPLY_DIAGNOSTIC_PATH, "Supply diagnostic."),
        ("stage267_run267DU_replacement_preplan", "similar_replacement_preplan", REPLACEMENT_PREPLAN_PATH, "Similar replacement preplan."),
        ("stage267_run267DU_experiment_design", "experiment_design_receipt", EXPERIMENT_DESIGN_RECEIPT_PATH, "Experiment design receipt."),
        ("stage267_run267DU_environment", "environment_reproducibility_receipt", ENVIRONMENT_REPRODUCIBILITY_RECEIPT_PATH, "Environment receipt."),
        ("stage267_run267DU_data_integrity", "data_integrity_receipt", DATA_INTEGRITY_RECEIPT_PATH, "Data integrity receipt."),
        ("stage267_run267DU_runtime_parity", "runtime_parity_receipt", RUNTIME_PARITY_RECEIPT_PATH, "Runtime parity receipt."),
        ("stage267_run267DU_result_judgment", "result_judgment", RESULT_JUDGMENT_PATH, "Result judgment."),
        ("stage267_run267DU_gate_audit", "gate_audit", GATE_AUDIT_PATH, "Gate audit."),
        ("stage267_run267DU_run_manifest", "run_manifest", RUN_MANIFEST_PATH, "Run manifest."),
        ("stage267_run267DU_lineage", "lineage", LINEAGE_PATH, "Lineage."),
        ("stage267_run267DU_review_result", "review_result", REVIEW_RESULT_PATH, "Review result."),
        ("stage267_run267DU_report", "review_report", REPORT_PATH, "User-facing report."),
    ]
    for row in result["variant_manifest"]:
        specs.append((f"stage267_run267DU_feature_{row['variant_id']}", "runtime_feature_frame", repo_path(row["runtime_feature_file"]), "Runtime feature copy."))
        specs.append((f"stage267_run267DU_model_{row['variant_id']}", "runtime_model_table", repo_path(row["runtime_model_file"]), "Runtime model copy."))
    for row in result["attempt_manifest"]:
        specs.append((f"stage267_run267DU_set_{row['attempt_name']}", "mt5_set", repo_path(row["set_path"]), "MT5 set file."))
        specs.append((f"stage267_run267DU_ini_{row['attempt_name']}", "mt5_ini", repo_path(row["ini_path"]), "MT5 tester ini file."))
    rows: list[dict[str, Any]] = []
    for artifact_id, artifact_type, path, notes in specs:
        rows.append(
            {
                "artifact_id": artifact_id,
                "artifact_type": artifact_type,
                "path": rel(path),
                "sha256": sha256_file_lf_normalized(path) if path_exists(path) else "",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": created_at,
                "notes": notes,
            }
        )
    return rows


def update_ledgers(created_at: str, result: Mapping[str, Any]) -> None:
    counts = result["counts"]
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "runtime_gap_aware_fifth_followup_or_prune_materialization",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "notes": f"variants={counts['variants']};attempts={counts['attempts']};held={counts['held_rows']};next_action={NEXT_ACTION}.",
    }
    upsert_csv_rows(RUN_REGISTRY_PATH, RUN_REGISTRY_COLUMNS, [run_row], key="run_id")
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__runtime_gap_aware_fifth_followup_or_prune_materialization",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "runtime_gap_aware_fifth_followup_or_prune_materialization",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "materialization",
        "tier_scope": "Tier A and duplicate-boundary Tier A+B where input exists; held rows explicit",
        "kpi_scope": "execution_pending_no_kpi",
        "scoreboard_lane": "runtime_gap_aware_materialization",
        "status": "out_of_scope_by_claim",
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "primary_kpi": f"variants={counts['variants']};attempts={counts['attempts']}",
        "guardrail_kpi": "selected_candidate=none;onnx_readiness=not_claimed;goal_achieve=not_claimed",
        "external_verification_status": "out_of_scope_by_claim",
        "notes": f"Next action: {NEXT_ACTION}. Materialization only; MT5 output missing.",
    }
    upsert_csv_rows(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, [alpha_row], key="ledger_row_id")
    stage_row = {
        "row_id": "stage267_run267DU_runtime_gap_aware_fifth_followup_or_prune_materialization",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "view": "runtime_gap_aware_fifth_followup_or_prune_materialization",
        "tier_scope": "Tier A materialized and held rows explicit",
        "scoreboard": "execution_pending_no_candidate_selection_no_onnx",
        "status": STATUS,
        "judgment": JUDGMENT,
        "evidence_boundary": "feature_model_set_ini_handoff_materialized_no_mt5_kpi",
        "report_path": rel(REPORT_PATH),
        "notes": f"variants={counts['variants']};attempts={counts['attempts']};held={counts['held_rows']};diagnostics={counts['diagnostics']}.",
    }
    upsert_csv_rows(STAGE_LEDGER_PATH, STAGE_LEDGER_COLUMNS, [stage_row], key="row_id")
    upsert_csv_rows(ARTIFACT_REGISTRY_PATH, ARTIFACT_COLUMNS, artifact_rows(created_at, result), key="artifact_id")


def read_text(path: Path) -> str:
    return io_path(path).read_text(encoding="utf-8-sig")


def replace_line_containing(text: str, needle: str, replacement: str) -> str:
    return "\n".join(replacement if needle in line else line for line in text.splitlines()) + "\n"


def replace_line_prefix(text: str, prefix: str, replacement: str) -> str:
    return "\n".join(replacement if line.startswith(prefix) else line for line in text.splitlines()) + "\n"


def append_after_contains(text: str, needle: str, new_line: str) -> str:
    if new_line in text:
        return text
    lines = text.splitlines()
    out: list[str] = []
    inserted = False
    for line in lines:
        out.append(line)
        if not inserted and needle in line:
            out.append(new_line)
            inserted = True
    if not inserted:
        out.append(new_line)
    return "\n".join(out) + "\n"


def append_block_once(text: str, marker: str, block: str) -> str:
    if marker in text:
        return text
    return text.rstrip() + "\n\n" + block.rstrip() + "\n"


def update_workspace_block(text: str) -> str:
    lines = text.splitlines()
    output: list[str] = []
    in_stage267 = False
    report_line = f"  run267DU_runtime_gap_aware_fifth_followup_or_prune_materialization_report_path: {rel(REPORT_PATH)}"
    report_seen = any(report_line.strip() == line.strip() for line in lines)
    for line in lines:
        if line.startswith("stage267_baseline_candidate_racing_protocol:"):
            in_stage267 = True
            output.append(line)
            continue
        if in_stage267 and line and not line.startswith(" ") and not line.startswith("-"):
            if not report_seen:
                output.append(report_line)
                report_seen = True
            in_stage267 = False
        if in_stage267:
            stripped = line.strip()
            if stripped.startswith("status:"):
                output.append(f"  status: {STATUS}")
                continue
            if stripped.startswith("current_run_id:"):
                output.append(f"  current_run_id: {RUN_ID}")
                continue
            if stripped.startswith("last_completed_run_id:"):
                output.append(f"  last_completed_run_id: {RUN_ID}")
                continue
            if stripped.startswith("next_action:"):
                if not report_seen:
                    output.append(report_line)
                    report_seen = True
                output.append(f"  next_action: {NEXT_ACTION}")
                continue
        output.append(line)
    if in_stage267 and not report_seen:
        output.append(report_line)
    return "\n".join(output) + "\n"


def update_current_docs(result: Mapping[str, Any]) -> None:
    counts = result["counts"]
    report_line = (
        "- run267DU_runtime_gap_aware_fifth_followup_or_prune_materialization"
        f"(267DU 런타임 공백 반영 5차 후속/가지치기 물질화): `{rel(REPORT_PATH)}`"
    )
    block = "\n".join(
        [
            "Run267DU(267DU 실행)는 run267DT(267DT 실행)의 materialization queue(물질화 대기열)를 feature/model/set/ini(피처/모델/설정/초기화 파일) 입력으로 바꿨다.",
            f"Effect(효과): variants(변형) `{counts['variants']}`개, attempts(시도) `{counts['attempts']}`개, held rows(보류 행) `{counts['held_rows']}`개, diagnostics(진단) `{counts['diagnostics']}`개를 만들었다.",
            "Boundary(경계): selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 계속 `none/not_claimed`다.",
        ]
    )
    for path in (CURRENT_WORKING_STATE_PATH, SELECTION_STATUS_PATH, REVIEW_INDEX_PATH):
        text = read_text(path)
        if path == CURRENT_WORKING_STATE_PATH:
            text = replace_line_containing(text, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
            text = replace_line_containing(
                text,
                "- adapter_under_review(",
                "- adapter_under_review(검토 중 어댑터): `runtime_gap_aware_fifth_followup_or_prune_materialization`",
            )
            text = replace_line_containing(text, "- status(", f"- status(상태): `{STATUS}`")
            text = replace_line_containing(text, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
            text = append_after_contains(text, "stage267_run267DT_runtime_gap_aware_fifth_followup_or_prune_design.md", report_line)
        elif path == SELECTION_STATUS_PATH:
            text = replace_line_containing(text, "- stage_status(", f"- stage_status(단계 상태): `{STATUS}`")
            text = replace_line_containing(text, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
            text = replace_line_containing(text, "- last_completed_run(", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
            text = replace_line_containing(text, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
            text = append_after_contains(text, "run267DT_runtime_gap_aware_fifth_followup_or_prune_design", report_line)
        else:
            text = replace_line_containing(text, "- status(", f"- status(상태): `{STATUS}`")
            text = replace_line_containing(text, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
            text = replace_line_containing(text, "- last_completed_run(", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
            text = append_after_contains(text, "run267DT_runtime_gap_aware_fifth_followup_or_prune_design", report_line)
        text = append_block_once(text, "Run267DU(267DU 실행)는 run267DT", block)
        write_md(path, text)

    workspace = read_text(WORKSPACE_STATE_PATH)
    focus = (
        "- >-\n"
        f"  Stage267(267단계) run267DU(267DU 실행) runtime gap aware fifth follow-up/prune materialization"
        f"(런타임 공백 반영 5차 후속/가지치기 물질화) `{STATUS}`. "
        f"Effect(효과): run267DT(267DT 실행)의 queue(대기열)를 variants(변형) `{counts['variants']}`개, "
        f"attempts(시도) `{counts['attempts']}`개, held rows(보류 행) `{counts['held_rows']}`개로 바꿨고, "
        "selected candidate(선택 후보), selected research baseline(선택 연구 기준 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 주장하지 않는다.\n"
    )
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    if f"`{STATUS}`" not in workspace:
        workspace = workspace.replace("current_focus:\n", "current_focus:\n" + focus, 1)
    workspace = update_workspace_block(workspace)
    write_md(WORKSPACE_STATE_PATH, workspace)


def write_outputs(result: Mapping[str, Any]) -> None:
    write_csv(MATERIALIZATION_PLAN_PATH, result["materialization_plan"])
    write_csv(QUEUE_DECISION_PATH, result["queue_decision"])
    write_csv(FEATURE_FRAME_MANIFEST_PATH, result["feature_frame_manifest"])
    write_csv(MODEL_MANIFEST_PATH, result["model_manifest"])
    write_csv(VARIANT_MANIFEST_PATH, result["variant_manifest"])
    write_csv(ATTEMPT_MANIFEST_PATH, result["attempt_manifest"])
    write_csv(RUNTIME_CONTRACT_PATH, result["runtime_contract"])
    write_csv(HELD_QUEUE_PATH, result["held_queue"])
    write_csv(PREFLIGHT_RECEIPT_PATH, result["preflight_handoff_receipt"])
    write_csv(SUPPLY_DIAGNOSTIC_PATH, result["pre_runtime_supply_diagnostic"])
    write_csv(REPLACEMENT_PREPLAN_PATH, result["similar_replacement_preplan"])
    write_csv(EXPERIMENT_DESIGN_RECEIPT_PATH, result["experiment_design_receipt"])
    write_csv(ENVIRONMENT_REPRODUCIBILITY_RECEIPT_PATH, result["environment_reproducibility_receipt"])
    write_csv(DATA_INTEGRITY_RECEIPT_PATH, result["data_integrity_receipt"])
    write_csv(RUNTIME_PARITY_RECEIPT_PATH, result["runtime_parity_receipt"])
    write_csv(RESULT_JUDGMENT_PATH, result["result_judgment"])
    write_csv(GATE_AUDIT_PATH, result["gate_audit"])
    write_json(RUN_MANIFEST_PATH, run_manifest(result))
    write_json(LINEAGE_PATH, lineage(result))
    write_json(REVIEW_RESULT_PATH, result)
    write_md(REPORT_PATH, report_markdown(result))


def build_result() -> dict[str, Any]:
    required = [
        SOURCE_QUEUE_PATH,
        SOURCE_FEATURE_BLUEPRINT_PATH,
        SOURCE_BRANCH_DECISION_PATH,
        SOURCE_PRUNE_MATRIX_PATH,
        SOURCE_FAILURE_MEMORY_PATH,
        SOURCE_REVIEW_RESULT_PATH,
        SOURCE_DQ_VARIANT_MANIFEST_PATH,
        SOURCE_DQ_ATTEMPT_MANIFEST_PATH,
        SOURCE_DQ_RUNTIME_CONTRACT_PATH,
        SOURCE_DQ_HANDOFF_RECEIPT_PATH,
        SOURCE_CV_VARIANT_MANIFEST_PATH,
        SOURCE_CV_ATTEMPT_MANIFEST_PATH,
        SOURCE_CV_RUNTIME_CONTRACT_PATH,
        SOURCE_FEATURE_MANIFEST_PATH,
    ]
    missing = [rel(path) for path in required if not path_exists(path)]
    if missing:
        raise FileNotFoundError("missing required inputs: " + "; ".join(missing))

    created_at = utc_now()
    queue_rows = read_csv(SOURCE_QUEUE_PATH)
    variant_by_id = source_variant_rows()
    attempts = source_attempt_rows()
    canonical = canonical_source_rows()
    materialization_plan = materialization_plan_rows(queue_rows)
    variant_rows: list[dict[str, Any]] = []
    feature_rows: list[dict[str, Any]] = []
    model_rows: list[dict[str, Any]] = []
    attempt_rows: list[dict[str, Any]] = []
    preflight_rows: list[dict[str, Any]] = []
    for index, plan in enumerate(PLAN_CONFIGS, start=1):
        variant, feature, model, attempt, preflight = materialize_plan(plan, variant_by_id, attempts, canonical, index)
        variant_rows.append(variant)
        feature_rows.append(feature)
        model_rows.append(model)
        attempt_rows.append(attempt)
        preflight_rows.append(preflight)
    diagnostics = diagnostic_rows(canonical)
    held = held_queue_rows()
    replacement = replacement_preplan_rows()
    queue_decisions = queue_decision_rows(queue_rows, variant_rows, attempt_rows, held, len(diagnostics))
    materialized_queue_ids = {row["queue_id"] for row in variant_rows}
    counts = {
        "missing_required": len(missing),
        "queue_rows": len(queue_rows),
        "materialized_queue_rows": len(materialized_queue_ids),
        "held_rows": len(held),
        "variants": len(variant_rows),
        "attempts": len(attempt_rows),
        "feature_frames": len(feature_rows),
        "models": len(model_rows),
        "preflight_receipts": len(preflight_rows),
        "diagnostics": len(diagnostics),
        "replacement_preplans": len(replacement),
        "aggressive_variants": sum(1 for row in variant_rows if row["priority"] in {"P0_aggressive", "P0_explosive"}),
        "repair_variants": sum(1 for row in variant_rows if row["priority"] == "P0_repair"),
        "control_variants": sum(1 for row in variant_rows if row["priority"] == "P0_control"),
        "s258_variants": sum(1 for row in variant_rows if row["candidate_alias"] == "s258_stc"),
        "s264_aih_variants": sum(1 for row in variant_rows if row["candidate_alias"] == "s264_aih"),
        "s264_lc_variants": sum(1 for row in variant_rows if row["candidate_alias"] == "s264_lc"),
        "selected_candidate": "none",
        "selected_research_baseline": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
    }
    result: dict[str, Any] = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "source_runtime_run_id": SOURCE_RUNTIME_RUN_ID,
        "source_aih_run_id": SOURCE_AIH_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "created_at_utc": created_at,
        "next_action": NEXT_ACTION,
        "claim_boundary": CLAIM_BOUNDARY,
        "tier_pair_boundary": TIER_PAIR_BOUNDARY,
        "materialization_boundary": MATERIALIZATION_BOUNDARY,
        "counts": counts,
        "sources": source_paths(),
        "outputs": output_paths(),
        "materialization_plan": materialization_plan,
        "queue_decision": queue_decisions,
        "feature_frame_manifest": feature_rows,
        "model_manifest": model_rows,
        "variant_manifest": variant_rows,
        "attempt_manifest": attempt_rows,
        "runtime_contract": runtime_contract_rows(variant_rows),
        "held_queue": held,
        "preflight_handoff_receipt": preflight_rows,
        "pre_runtime_supply_diagnostic": diagnostics,
        "similar_replacement_preplan": replacement,
        "experiment_design_receipt": experiment_design_rows(),
        "environment_reproducibility_receipt": environment_rows(counts),
        "data_integrity_receipt": data_integrity_rows(feature_rows),
        "runtime_parity_receipt": runtime_parity_rows(variant_rows, attempt_rows),
        "result_judgment": result_judgment_rows(counts),
        "gate_audit": gate_audit_rows(counts),
        "selected_candidate": "none",
        "selected_research_baseline": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
    }
    return result


def execute() -> dict[str, Any]:
    result = build_result()
    write_outputs(result)
    update_ledgers(str(result["created_at_utc"]), result)
    update_current_docs(result)
    return result


def main() -> int:
    result = execute()
    counts = result["counts"]
    print(
        json.dumps(
            {
                "status": result["status"],
                "variants": counts["variants"],
                "attempts": counts["attempts"],
                "aggressive_variants": counts["aggressive_variants"],
                "held_rows": counts["held_rows"],
                "diagnostics": counts["diagnostics"],
                "selected_candidate": result["selected_candidate"],
                "selected_research_baseline": result["selected_research_baseline"],
                "onnx_readiness": result["onnx_readiness"],
                "goal_achieve": result["goal_achieve"],
                "next_action": result["next_action"],
                "report": rel(REPORT_PATH),
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
