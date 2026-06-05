from __future__ import annotations

import csv
import json
import os
import shutil
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.mt5 import runtime_support as mt5  # noqa: E402
from stage_pipelines.stage344 import (  # noqa: E402
    design_s07_trend_confirmed_forward_cost_stability_validation_without_db as design,
)
from stage_pipelines.stage344 import (  # noqa: E402
    materialize_directional_long_supply_quality_surface_package_without_db as source_pkg,
)


TODAY = "2026-06-01"
STAGE_ID = source_pkg.STAGE_ID
STAGE_DIR = source_pkg.STAGE_DIR
RUN_NUMBER = "run344G"
RUN_ID = "run344G_materialize_s07_forward_cost_stability_validation_package_without_db_v1"
PARENT_RUN_ID = design.RUN_ID
SOURCE_PACKAGE_RUN_ID = source_pkg.RUN_ID
SOURCE_RUNTIME_RUN_ID = design.SOURCE_RUNTIME_RUN_ID
NEXT_RUN_ID = "run344H_execute_s07_forward_cost_stability_validation_mt5_probe_without_db_v1"

STATUS = "completed_stage344G_s07_forward_cost_stability_validation_package_materialized_no_selection"
JUDGMENT = "s07_validation_package_ready_for_mt5_probe_and_attribution_no_operating_claim"
DECISION = "stage344G_open_run344H_execute_s07_forward_cost_stability_validation_mt5_probe"
CLAIM_BOUNDARY = (
    "research_development_s07_forward_cost_stability_validation_package_only_"
    "no_mt5_execution_no_candidate_selection_no_forward_pass_no_live_readiness_"
    "no_operating_promotion_no_runtime_authority_no_goal_claim"
)

RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
FEATURE_DIR = RUN_DIR / "features"
EXPECTED_DIR = RUN_DIR / "expected"
MODEL_DIR = RUN_DIR / "models"
MT5_DIR = RUN_DIR / "mt5"
SET_DIR = MT5_DIR / "sets"
INI_DIR = MT5_DIR / "inis"
CONTRACT_DIR = RUN_DIR / "contracts"

COMMON_ROOT = f"Project_Obsidian_Prime_v2/stage344/{RUN_NUMBER}_s07_validation"
COMMON_FEATURE_DIR = f"{COMMON_ROOT}/features"
COMMON_MODEL_DIR = f"{COMMON_ROOT}/models"
COMMON_TELEMETRY_DIR = f"{COMMON_ROOT}/telemetry"
EXPLORATION_LABEL = "stage344_S07ForwardCostStability__ValidationPackage"
MAGIC_BASE = 3443000

REPORT_PATH = REVIEW_DIR / "run344G_s07_forward_cost_stability_validation_package.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage344G_s07_forward_cost_stability_validation_package.md"
SELECTION_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
STAGE_README = STAGE_DIR / "README.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"

PARENT_FINAL = design.FINAL_DECISION
PARENT_GATES = design.GATE_AUDIT
PARENT_QUEUE = design.NEXT_QUEUE
PARENT_COST_STRESS = design.COST_STRESS_CONTRACT
PARENT_SESSION_PLAN = design.SESSION_REGIME_PLAN
PARENT_COMPARATOR_PLAN = design.COMPARATOR_PLAN
PARENT_HANDOFF_PLAN = design.FORWARD_REPLAY_HANDOFF_PLAN
PARENT_VALIDATION_PLAN = design.VALIDATION_SURFACE_PLAN

SOURCE_ATTEMPT_PACKAGE = source_pkg.RUNTIME_PROBE_ATTEMPT_PACKAGE
SOURCE_FEATURE_MATRIX = source_pkg.FEATURE_MATRIX
SOURCE_EXPECTED_TAPE = source_pkg.EXPECTED_TAPE
SOURCE_RUNTIME_SUMMARY = STAGE_DIR / "02_runs" / "run344D" / "directional_long_quality_surface_mt5_probe_summary.csv"
SOURCE_RUNTIME_IDENTITY = STAGE_DIR / "02_runs" / "run344D" / "runtime_identity.csv"

FEATURE_MATRIX = FEATURE_DIR / "runtime_features.csv"
EXPECTED_TAPE = EXPECTED_DIR / "expected_tape.csv"
EXPECTED_TAPE_INDEX = RUN_DIR / "expected_tape_index.csv"
RUNTIME_PROBE_ATTEMPT_PACKAGE = RUN_DIR / "runtime_probe_attempt_package.csv"
MODEL_HANDOFF_MANIFEST = RUN_DIR / "model_handoff_manifest.csv"
COMMON_FILES_SYNC = RUN_DIR / "common_files_sync.csv"
TESTER_SET_MANIFEST = RUN_DIR / "tester_set_manifest.csv"
TESTER_INI_MANIFEST = RUN_DIR / "tester_ini_manifest.csv"
TESTER_IDENTITY_CONTRACT = RUN_DIR / "tester_identity_contract.csv"
RUNTIME_PARITY_CONTRACT = RUN_DIR / "runtime_parity_contract.csv"
VALIDATION_CONTRACT_MANIFEST = RUN_DIR / "validation_contract_manifest.csv"
COST_STRESS_CONTRACT = CONTRACT_DIR / "cost_stress_contract.csv"
SESSION_REGIME_PLAN = CONTRACT_DIR / "session_regime_attribution_plan.csv"
COMPARATOR_PLAN = CONTRACT_DIR / "anchor_s05_s07_comparator_plan.csv"
FORWARD_REPLAY_HANDOFF_PLAN = CONTRACT_DIR / "forward_replay_handoff_plan.csv"
RUN344H_QUEUE = RUN_DIR / "run344H_queue.csv"
RUN_EVIDENCE_RECEIPT = RUN_DIR / "run_evidence_receipt.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs" / "context" / "current_working_state.md"
ROOT_CHANGELOG = ROOT / "CHANGELOG.md"
WORKSPACE_CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
PROJECT_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
ROOT_SELECTION_STATUS = ROOT / "docs" / "registers" / "selection_status.md"

SELECTED_ATTEMPTS = (
    ("s07_trend_confirmed_long_only", "primary_candidate(주 후보)", "v01_s07"),
    ("s05_long_quality_extreme_top20", "quality_threshold_comparator(품질 임계값 대조)", "v02_s05"),
    ("s01_anchor_short_supply_control", "anchor_comparator(앵커 대조)", "v03_s01"),
)

INPUT_FILES = (
    PARENT_FINAL,
    PARENT_GATES,
    PARENT_QUEUE,
    PARENT_COST_STRESS,
    PARENT_SESSION_PLAN,
    PARENT_COMPARATOR_PLAN,
    PARENT_HANDOFF_PLAN,
    PARENT_VALIDATION_PLAN,
    SOURCE_ATTEMPT_PACKAGE,
    SOURCE_FEATURE_MATRIX,
    SOURCE_EXPECTED_TAPE,
    SOURCE_RUNTIME_SUMMARY,
    SOURCE_RUNTIME_IDENTITY,
)

OUTPUT_FILES = (
    FEATURE_MATRIX,
    EXPECTED_TAPE,
    EXPECTED_TAPE_INDEX,
    RUNTIME_PROBE_ATTEMPT_PACKAGE,
    MODEL_HANDOFF_MANIFEST,
    COMMON_FILES_SYNC,
    TESTER_SET_MANIFEST,
    TESTER_INI_MANIFEST,
    TESTER_IDENTITY_CONTRACT,
    RUNTIME_PARITY_CONTRACT,
    VALIDATION_CONTRACT_MANIFEST,
    COST_STRESS_CONTRACT,
    SESSION_REGIME_PLAN,
    COMPARATOR_PLAN,
    FORWARD_REPLAY_HANDOFF_PLAN,
    RUN344H_QUEUE,
    RUN_EVIDENCE_RECEIPT,
    DATA_RECEIPT,
    RUNTIME_RECEIPT,
    LINEAGE_RECEIPT,
    CLAIM_RECEIPT,
    GATE_AUDIT,
    FINAL_DECISION,
    RUN_MANIFEST,
    REPORT_PATH,
    DECISION_DOC,
    WORKSPACE_STATE,
    CURRENT_WORKING_STATE,
    SELECTION_STATUS,
    ROOT_SELECTION_STATUS,
    STAGE_BRIEF,
    STAGE_README,
    ROOT_CHANGELOG,
    WORKSPACE_CHANGELOG,
    RUN_REGISTRY,
    PROJECT_LEDGER,
    STAGE_LEDGER,
    ARTIFACT_REGISTRY,
    Path(__file__),
)


def now_utc() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def rel(path: Path | str) -> str:
    return source_pkg.rel(path)


def path_is_file(path: Path) -> bool:
    return source_pkg.path_is_file(path)


def ensure_parent(path: Path) -> None:
    source_pkg.ensure_parent(path)


def required(path: Path) -> Path:
    return source_pkg.required(path)


def read_json(path: Path) -> Any:
    return source_pkg.read_json(path)


def read_csv(path: Path) -> pd.DataFrame:
    return source_pkg.read_csv(path)


def write_json(path: Path, payload: Any) -> None:
    source_pkg.write_json(path, payload)


def write_text(path: Path, text: str) -> None:
    source_pkg.write_text(path, text)


def append_text_once(path: Path, marker: str, text: str) -> None:
    source_pkg.append_text_once(path, marker, text)


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    rows_list = [dict(row) for row in rows]
    if fieldnames is None:
        fields: list[str] = []
        for row in rows_list:
            for key in row:
                if key not in fields:
                    fields.append(key)
        fieldnames = fields
    ensure_parent(path)
    with open(source_pkg.fs_path(path), "w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fieldnames), extrasaction="ignore")
        writer.writeheader()
        for row in rows_list:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def write_frame(path: Path, frame: pd.DataFrame) -> None:
    source_pkg.write_csv(path, frame)


def append_or_replace_csv(path: Path, keys: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> None:
    source_pkg.append_or_replace_csv(path, keys, rows)


def sha256_file(path: Path) -> str:
    return source_pkg.sha256_file(path)


def as_bool(value: Any) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def as_int(value: Any, default: int = 0) -> int:
    try:
        if pd.isna(value) or value == "":
            return default
        return int(round(float(value)))
    except (TypeError, ValueError):
        return default


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        if pd.isna(value) or value == "":
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def parse_range(text: Any) -> tuple[bool, float, float]:
    return source_pkg.parse_range(text)


def copy_file(source: Path, target: Path, sync_id: str, effect: str) -> dict[str, Any]:
    ensure_parent(target)
    shutil.copy2(source_pkg.fs_path(source), source_pkg.fs_path(target))
    exists = path_is_file(target)
    return {
        "sync_id": sync_id,
        "source_path": rel(source) if source.is_absolute() and str(source.resolve()).lower().startswith(str(ROOT.resolve()).lower()) else source.as_posix(),
        "target_path": rel(target) if str(target.resolve()).lower().startswith(str(ROOT.resolve()).lower()) else target.as_posix(),
        "exists": bool(exists),
        "sha256": sha256_file(target) if exists else "",
        "status": "synced(동기화됨)" if exists else "missing(누락)",
        "effect": effect,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def parent_gates_passed() -> bool:
    gates = read_csv(PARENT_GATES)
    return bool(len(gates) > 0 and gates["status"].astype(str).str.lower().eq("passed").all())


def selected_source_rows(attempts: pd.DataFrame) -> pd.DataFrame:
    selected = [attempt for attempt, _, _ in SELECTED_ATTEMPTS]
    frame = attempts.loc[attempts["attempt_name"].astype(str).isin(selected)].copy()
    if len(frame) != len(selected):
        missing = sorted(set(selected) - set(frame["attempt_name"].astype(str)))
        raise RuntimeError(f"missing selected attempts: {missing}")
    order = {attempt: index for index, (attempt, _, _) in enumerate(SELECTED_ATTEMPTS)}
    frame["_order"] = frame["attempt_name"].map(order)
    return frame.sort_values("_order").drop(columns=["_order"])


def build_package() -> dict[str, Any]:
    for source in INPUT_FILES:
        required(source)
    parent_final = read_json(PARENT_FINAL)
    if parent_final.get("next_run_id", parent_final.get("next_action")) != RUN_ID:
        raise RuntimeError("run344F next run does not point to run344G")
    if not parent_gates_passed():
        raise RuntimeError("run344F gate audit has failed rows")

    attempts = read_csv(SOURCE_ATTEMPT_PACKAGE)
    selected_attempts = selected_source_rows(attempts)
    expected = read_csv(SOURCE_EXPECTED_TAPE)
    selected_names = set(selected_attempts["attempt_name"].astype(str))
    expected_filtered = expected.loc[expected["attempt_name"].astype(str).isin(selected_names)].copy()
    if expected_filtered.empty:
        raise RuntimeError("filtered expected tape is empty")

    sync_rows: list[dict[str, Any]] = []
    model_rows: list[dict[str, Any]] = []
    set_rows: list[dict[str, Any]] = []
    ini_rows: list[dict[str, Any]] = []
    attempt_rows: list[dict[str, Any]] = []
    tester_identity_rows: list[dict[str, Any]] = []

    sync_rows.append(copy_file(SOURCE_FEATURE_MATRIX, FEATURE_MATRIX, "local_feature_matrix", "runtime feature matrix(런타임 피처 행렬)를 검증 패키지에 복사"))
    feature_common = f"{COMMON_FEATURE_DIR}/runtime_features.csv"
    sync_rows.append(copy_file(FEATURE_MATRIX, source_pkg.DEFAULT_COMMON_FILES / Path(feature_common), "common_feature_matrix", "MT5 Common Files(MT5 공용 파일)에 피처 행렬 복사"))
    write_frame(EXPECTED_TAPE, expected_filtered)

    source_contracts = [
        (PARENT_COST_STRESS, COST_STRESS_CONTRACT, "cost_stress_contract(비용 압박 계약)"),
        (PARENT_SESSION_PLAN, SESSION_REGIME_PLAN, "session_regime_plan(세션/국면 계획)"),
        (PARENT_COMPARATOR_PLAN, COMPARATOR_PLAN, "comparator_plan(대조 계획)"),
        (PARENT_HANDOFF_PLAN, FORWARD_REPLAY_HANDOFF_PLAN, "forward_replay_handoff_plan(전진/재생 인계 계획)"),
    ]
    contract_rows = []
    for source, target, name in source_contracts:
        sync_rows.append(copy_file(source, target, f"contract::{target.name}", f"{name}을 run344G package(패키지)에 고정"))
        contract_rows.append(
            {
                "contract_name": name,
                "source_path": rel(source),
                "package_path": rel(target),
                "package_sha256": sha256_file(target),
                "effect": "keeps validation meaning beside runtime package(검증 의미를 런타임 패키지 옆에 고정)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(VALIDATION_CONTRACT_MANIFEST, contract_rows)

    feature_count = as_int(selected_attempts.iloc[0].get("feature_count"))
    feature_hash = str(selected_attempts.iloc[0].get("feature_order_hash", ""))

    role_lookup = {attempt: role for attempt, role, _ in SELECTED_ATTEMPTS}
    short_lookup = {attempt: short for attempt, _, short in SELECTED_ATTEMPTS}
    for index, (_, row) in enumerate(selected_attempts.iterrows(), start=1):
        attempt = str(row["attempt_name"])
        short_name = short_lookup[attempt]
        role = role_lookup[attempt]
        source_model = ROOT / str(row["model_local_path"])
        local_model = MODEL_DIR / f"{short_name}.onnx"
        common_model = f"{COMMON_MODEL_DIR}/{short_name}.onnx"
        sync_rows.append(copy_file(source_model, local_model, f"local_model::{attempt}", f"{attempt} ONNX(온엑스)를 짧은 패키지 이름으로 복사"))
        sync_rows.append(copy_file(local_model, source_pkg.DEFAULT_COMMON_FILES / Path(common_model), f"common_model::{attempt}", f"{attempt} ONNX(온엑스)를 MT5 Common Files(MT5 공용 파일)로 복사"))

        block_long_enabled, block_long_min, block_long_max = parse_range(row.get("block_long_range", ""))
        block_short_enabled, block_short_min, block_short_max = parse_range(row.get("block_short_range", ""))
        side_enabled = as_bool(row.get("side_filter_enabled"))
        feature_index = as_int(row.get("side_filter_feature_index"), -1)
        set_name = f"OPV2_{RUN_NUMBER}_{short_name}.set"
        ini_name = f"OPV2_{RUN_NUMBER}_{short_name}.ini"
        report_name = f"POPv2_{RUN_NUMBER}_{short_name}"
        set_path = SET_DIR / set_name
        ini_path = INI_DIR / ini_name
        set_values = {
            "InpRunId": f"{RUN_ID}_{attempt}",
            "InpExplorationLabel": EXPLORATION_LABEL,
            "InpTierLabel": "Tier A",
            "InpPrimaryActiveTier": "tier_a",
            "InpSplitLabel": "inner_holdout_runtime_collapsed_probe",
            "InpMainSymbol": "US100",
            "InpTimeframe": 5,
            "InpEnforceM5": True,
            "InpFeatureCsvPath": feature_common,
            "InpFeatureCount": feature_count,
            "InpFeatureCsvUseCommonFiles": True,
            "InpFeatureRequireTimestampMatch": True,
            "InpFeatureAllowLatestFallback": False,
            "InpFeatureStrictHeader": True,
            "InpCsvTimestampIsBarClose": True,
            "InpModelPath": common_model,
            "InpModelId": row["model_id"],
            "InpModelBackend": "onnx",
            "InpModelUseCommonFiles": True,
            "InpModelUseCpuOnly": True,
            "InpModelNoConversion": False,
            "InpSetOutputShape": True,
            "InpFeatureOrderHash": feature_hash,
            "InpFallbackEnabled": False,
            "InpShortThreshold": as_float(row["short_threshold"]),
            "InpLongThreshold": as_float(row["long_threshold"]),
            "InpMinMargin": as_float(row["min_margin"]),
            "InpDecisionMode": "threshold_margin",
            "InpInvertSignal": False,
            "InpSideFilterEnabled": side_enabled,
            "InpSideFilterFeatureIndex": feature_index,
            "InpFallbackSideFilterFeatureIndex": feature_index,
            "InpBlockShortFeatureRange": side_enabled and block_short_enabled,
            "InpBlockShortFeatureMin": block_short_min,
            "InpBlockShortFeatureMax": block_short_max,
            "InpBlockLongFeatureRange": side_enabled and block_long_enabled,
            "InpBlockLongFeatureMin": block_long_min,
            "InpBlockLongFeatureMax": block_long_max,
            "InpAllowTrading": True,
            "InpFixedLot": as_float(row["fixed_lot"]),
            "InpMagic": MAGIC_BASE + index,
            "InpDeviationPoints": 20,
            "InpCloseOnFlatSignal": as_bool(row["close_on_flat"]),
            "InpReverseOnOppositeSignal": True,
            "InpCloseOnlyOnOppositeSignal": False,
            "InpMaxHoldBars": as_int(row["max_hold_bars"]),
            "InpMaxConcurrentPositions": 1,
            "InpReentryCooldownBars": 0,
            "InpSameDirectionReentryCooldownBars": 0,
            "InpEntryTransitionOnly": False,
            "InpExitRiskOverlayEnabled": False,
            "InpAtrSltpEnabled": False,
            "InpModelRiskSizingEnabled": False,
            "InpTelemetryEnabled": True,
            "InpTelemetryUseCommonFiles": True,
            "InpTelemetryCsvPath": f"{COMMON_TELEMETRY_DIR}/{short_name}_telemetry.csv",
            "InpSummaryCsvPath": f"{COMMON_TELEMETRY_DIR}/{short_name}_summary.csv",
        }
        set_payload = mt5.materialize_tester_set_file(set_values, set_path, generated_by=rel(Path(__file__)))
        ini_payload = mt5.materialize_tester_ini_file(
            mt5.TesterMaterializationConfig(
                shutdown_terminal=1,
                from_date=str(row["from_date"]),
                to_date=str(row["to_date"]),
                report=report_name,
            ),
            ini_path,
            set_file_path=Path(set_name),
        )
        tester = ini_payload["tester"]
        model_rows.append(
            {
                "attempt_name": attempt,
                "package_short_name": short_name,
                "model_id": row["model_id"],
                "variant_role": role,
                "source_model_path": rel(source_model),
                "source_model_sha256": sha256_file(source_model),
                "local_model_path": rel(local_model),
                "local_model_sha256": sha256_file(local_model),
                "common_model_path": common_model,
                "common_model_sha256": sha256_file(source_pkg.DEFAULT_COMMON_FILES / Path(common_model)),
                "feature_order_hash": feature_hash,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        set_rows.append(
            {
                "attempt_name": attempt,
                "package_short_name": short_name,
                "model_id": row["model_id"],
                "variant_role": role,
                "set_path": rel(set_path),
                "set_sha256": set_payload["sha256"],
                "short_threshold": row["short_threshold"],
                "long_threshold": row["long_threshold"],
                "min_margin": row["min_margin"],
                "max_hold_bars": row["max_hold_bars"],
                "close_on_flat": row["close_on_flat"],
                "side_filter_enabled": side_enabled,
                "side_filter_feature_index": feature_index,
                "block_long_range": row.get("block_long_range", ""),
                "block_short_range": row.get("block_short_range", ""),
                "magic": MAGIC_BASE + index,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        ini_rows.append(
            {
                "attempt_name": attempt,
                "package_short_name": short_name,
                "model_id": row["model_id"],
                "ini_path": rel(ini_path),
                "ini_sha256": ini_payload["sha256"],
                "expert": tester.get("Expert", ""),
                "symbol": tester.get("Symbol", ""),
                "period": tester.get("Period", ""),
                "from_date": tester.get("FromDate", ""),
                "to_date": tester.get("ToDate", ""),
                "report": tester.get("Report", ""),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        attempt_rows.append(
            {
                "attempt_name": attempt,
                "package_short_name": short_name,
                "queue_id": f"{RUN_NUMBER}_{short_name}",
                "next_run_id": NEXT_RUN_ID,
                "probe_priority": index,
                "tier": "Tier A",
                "split": "inner_holdout_runtime_collapsed_probe",
                "model_id": row["model_id"],
                "base_model_id": row["base_model_id"],
                "source_attempt": row["source_attempt"],
                "feature_set_id": row["feature_set_id"],
                "feature_count": feature_count,
                "feature_order_hash": feature_hash,
                "feature_local_path": rel(FEATURE_MATRIX),
                "feature_common_path": feature_common,
                "model_local_path": rel(local_model),
                "model_common_path": common_model,
                "expected_tape_path": rel(EXPECTED_TAPE),
                "common_telemetry_path": f"{COMMON_TELEMETRY_DIR}/{short_name}_telemetry.csv",
                "common_summary_path": f"{COMMON_TELEMETRY_DIR}/{short_name}_summary.csv",
                "set_path": rel(set_path),
                "set_name": set_name,
                "ini_path": rel(ini_path),
                "ini_name": ini_name,
                "report_name": report_name,
                "from_date": row["from_date"],
                "to_date": row["to_date"],
                "decision_mode": "threshold_margin",
                "short_threshold": row["short_threshold"],
                "long_threshold": row["long_threshold"],
                "min_margin": row["min_margin"],
                "fixed_lot": row["fixed_lot"],
                "max_hold_bars": row["max_hold_bars"],
                "close_on_flat": row["close_on_flat"],
                "side_filter_enabled": side_enabled,
                "side_filter_feature_index": feature_index,
                "block_long_range": row.get("block_long_range", ""),
                "block_short_range": row.get("block_short_range", ""),
                "variant_role": role,
                "runtime_mapping": "copied_from_run344C_with_short_validation_paths(344C에서 짧은 검증 경로로 복사)",
                "effect": "keeps runtime meaning while narrowing validation scope(런타임 의미를 유지하면서 검증 범위를 좁힘)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        tester_identity_rows.append(
            {
                "contract_id": f"tester_identity::{attempt}",
                "attempt_name": attempt,
                "package_short_name": short_name,
                "terminal_path": source_pkg.DEFAULT_TERMINAL.as_posix(),
                "tester_profile_root": source_pkg.DEFAULT_TESTER_PROFILE_ROOT.as_posix(),
                "portable_root": source_pkg.DEFAULT_PORTABLE_ROOT.as_posix(),
                "expert": tester.get("Expert", ""),
                "symbol": tester.get("Symbol", ""),
                "period": tester.get("Period", ""),
                "from_date": tester.get("FromDate", ""),
                "to_date": tester.get("ToDate", ""),
                "report": tester.get("Report", ""),
                "ea_binary": source_pkg.EA_BINARY.as_posix(),
                "portable_ea_ex5": source_pkg.PORTABLE_EA_EX5.as_posix(),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    write_csv(RUNTIME_PROBE_ATTEMPT_PACKAGE, attempt_rows)
    write_csv(MODEL_HANDOFF_MANIFEST, model_rows)
    write_csv(COMMON_FILES_SYNC, sync_rows)
    write_csv(TESTER_SET_MANIFEST, set_rows)
    write_csv(TESTER_INI_MANIFEST, ini_rows)
    write_csv(TESTER_IDENTITY_CONTRACT, tester_identity_rows)

    index_rows = []
    for attempt in selected_names:
        rows = expected_filtered.loc[expected_filtered["attempt_name"].astype(str).eq(attempt)]
        index_rows.append(
            {
                "attempt_name": attempt,
                "model_id": rows["model_id"].iloc[0] if not rows.empty else "",
                "row_count": int(len(rows)),
                "path": rel(EXPECTED_TAPE),
                "sha256": sha256_file(EXPECTED_TAPE),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(EXPECTED_TAPE_INDEX, sorted(index_rows, key=lambda item: item["attempt_name"]))

    runtime_parity_rows = [
        {
            "contract_id": "run344G_runtime_parity_contract(런타임 동등성 계약)",
            "attempt_rows": len(attempt_rows),
            "expected_rows": int(len(expected_filtered)),
            "feature_rows": int(len(read_csv(FEATURE_MATRIX))),
            "feature_order_hash": feature_hash,
            "research_path": rel(Path(__file__)),
            "runtime_path": rel(RUNTIME_PROBE_ATTEMPT_PACKAGE),
            "shared_contract": "same source attempts and same model probabilities, only package paths/report names changed(같은 원천 시도와 모델 확률, 패키지 경로/보고서 이름만 변경)",
            "known_differences": "cost/session contracts are carried for later attribution and do not change EA decisions(비용/세션 계약은 이후 귀속용이며 EA 결정을 바꾸지 않음)",
            "parity_check": "run344H must compare filtered expected tape against MT5 telemetry(344H에서 필터된 예상 테이프와 MT5 텔레메트리 비교 필요)",
            "runtime_claim_boundary": "package_only_no_runtime_authority(패키지 전용, 런타임 권위 없음)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    write_csv(RUNTIME_PARITY_CONTRACT, runtime_parity_rows)

    queue_rows = [
        {
            "queue_id": "run344H_01_execute_s07_anchor_s05_mt5_probe(344H s07/앵커/s05 MT5 탐침)",
            "next_run_id": NEXT_RUN_ID,
            "attempt_count": len(attempt_rows),
            "expected_rows": int(len(expected_filtered)),
            "action": "execute the three-attempt validation package in MT5 Strategy Tester(3개 시도 검증 패키지를 MT5 전략 테스터에서 실행)",
            "effect": "refreshes runtime evidence under short validation paths(짧은 검증 경로에서 런타임 근거를 새로 확인)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run344H_02_collect_reports_and_telemetry(보고서와 텔레메트리 수집)",
            "next_run_id": NEXT_RUN_ID,
            "attempt_count": len(attempt_rows),
            "expected_rows": int(len(expected_filtered)),
            "action": "copy report and telemetry outputs for later cost/session attribution(이후 비용/세션 귀속을 위해 보고서와 텔레메트리 복사)",
            "effect": "prepares run344I review(344I 검토 준비)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    write_csv(RUN344H_QUEUE, queue_rows)

    final = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "source_package_run_id": SOURCE_PACKAGE_RUN_ID,
        "source_runtime_run_id": SOURCE_RUNTIME_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_run_id": NEXT_RUN_ID,
        "next_action": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
        "attempt_rows": len(attempt_rows),
        "expected_rows": int(len(expected_filtered)),
        "feature_rows": int(len(read_csv(FEATURE_MATRIX))),
        "model_rows": len(model_rows),
        "set_rows": len(set_rows),
        "ini_rows": len(ini_rows),
        "common_sync_rows": len(sync_rows),
        "common_sync_missing": sum(1 for row in sync_rows if not row["exists"]),
        "contract_rows": len(contract_rows),
        "runtime_parity_contract_rows": len(runtime_parity_rows),
        "tester_identity_rows": len(tester_identity_rows),
        "selected_attempts": ";".join(attempt for attempt, _, _ in SELECTED_ATTEMPTS),
        "candidate_selection": "not_run",
        "selected_model": "none(없음)",
        "mt5_execution": "not_run",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "live_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
    }
    return final


def gate(gate_id: str, passed: bool, evidence: Path, effect: str) -> dict[str, Any]:
    return {
        "gate_id": gate_id,
        "status": "passed" if passed else "failed",
        "evidence_path": rel(evidence),
        "effect": effect,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def make_gates(final: Mapping[str, Any]) -> list[dict[str, Any]]:
    no_forbidden = (
        final["candidate_selection"] == "not_run"
        and final["selected_model"] == "none(없음)"
        and final["mt5_execution"] == "not_run"
        and final["forward_passed"] == "not_claimed"
        and final["runtime_authority"] == "not_claimed"
        and final["operating_promotion"] == "not_claimed"
        and final["goal_achieve"] == "not_claimed"
    )
    return [
        gate("parent_run344F_gates_passed", parent_gates_passed(), PARENT_GATES, "run344F design(설계) gate(게이트)가 통과됨"),
        gate("selected_attempts_found", final["attempt_rows"] == len(SELECTED_ATTEMPTS), RUNTIME_PROBE_ATTEMPT_PACKAGE, "s07/s05/s01 검증 시도가 모두 패키지에 포함됨"),
        gate("feature_and_expected_tape_materialized", path_is_file(FEATURE_MATRIX) and path_is_file(EXPECTED_TAPE) and final["expected_rows"] > 0, EXPECTED_TAPE, "피처와 예상 테이프를 물질화"),
        gate("model_and_common_sync_ready", final["model_rows"] == len(SELECTED_ATTEMPTS) and final["common_sync_missing"] == 0, COMMON_FILES_SYNC, "모델과 공용 파일 동기화가 완료"),
        gate("set_ini_materialized", final["set_rows"] == len(SELECTED_ATTEMPTS) and final["ini_rows"] == len(SELECTED_ATTEMPTS), TESTER_SET_MANIFEST, "set/ini 파일을 생성"),
        gate("validation_contracts_carried", final["contract_rows"] == 4, VALIDATION_CONTRACT_MANIFEST, "비용/세션/대조/인계 계약을 패키지에 고정"),
        gate("runtime_parity_contract_written", final["runtime_parity_contract_rows"] == 1, RUNTIME_PARITY_CONTRACT, "런타임 동등성 계약을 작성"),
        gate("no_forbidden_operating_claim", no_forbidden, FINAL_DECISION, "패키지 물질화를 운영 주장으로 올리지 않음"),
        gate("required_gate_coverage_audit_written", True, GATE_AUDIT, "필수 게이트 커버리지 감사를 기록"),
    ]


def parent_gates_passed() -> bool:
    return parent_gates_passed_impl()


def parent_gates_passed_impl() -> bool:
    gates = read_csv(PARENT_GATES)
    return bool(len(gates) > 0 and gates["status"].astype(str).str.lower().eq("passed").all())


def write_receipts(final: Mapping[str, Any]) -> None:
    write_json(
        RUN_EVIDENCE_RECEIPT,
        {
            "receipt_id": "run344G_run_evidence_package(실행 근거 패키지)",
            "run_id": RUN_ID,
            "attempt_rows": final["attempt_rows"],
            "expected_rows": final["expected_rows"],
            "set_rows": final["set_rows"],
            "ini_rows": final["ini_rows"],
            "effect": "creates executable MT5 validation package(실행 가능한 MT5 검증 패키지 생성)",
            "claim_boundary": CLAIM_BOUNDARY,
            "created_at_utc": now_utc(),
        },
    )
    write_json(
        DATA_RECEIPT,
        {
            "receipt_id": "run344G_data_integrity(데이터 무결성)",
            "run_id": RUN_ID,
            "data_source": [rel(SOURCE_FEATURE_MATRIX), rel(SOURCE_EXPECTED_TAPE)],
            "time_axis": "same US100 M5 runtime feature matrix and expected tape(동일 US100 M5 런타임 피처 행렬과 예상 테이프)",
            "feature_label_boundary": "package copies existing runtime decisions only(기존 런타임 결정만 복사)",
            "integrity_judgment": "usable_with_boundary(경계부 사용 가능)",
            "claim_boundary": CLAIM_BOUNDARY,
            "created_at_utc": now_utc(),
        },
    )
    write_json(
        RUNTIME_RECEIPT,
        {
            "receipt_id": "run344G_runtime_parity(런타임 동등성)",
            "run_id": RUN_ID,
            "runtime_path": rel(RUNTIME_PROBE_ATTEMPT_PACKAGE),
            "known_differences": "short package paths and report names only(짧은 패키지 경로와 보고서 이름만 변경)",
            "parity_check": "pending run344H MT5 execution(344H MT5 실행 대기)",
            "runtime_claim_boundary": "package_only_no_runtime_authority(패키지 전용, 런타임 권위 없음)",
            "claim_boundary": CLAIM_BOUNDARY,
            "created_at_utc": now_utc(),
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            "receipt_id": "run344G_claim_boundary(주장 경계)",
            "run_id": RUN_ID,
            "candidate_selection": final["candidate_selection"],
            "selected_model": final["selected_model"],
            "mt5_execution": final["mt5_execution"],
            "forward_passed": final["forward_passed"],
            "runtime_authority": final["runtime_authority"],
            "operating_promotion": final["operating_promotion"],
            "goal_achieve": final["goal_achieve"],
            "effect": "prevents package readiness from becoming operating readiness(패키지 준비를 운영 준비로 오해하지 않게 함)",
            "claim_boundary": CLAIM_BOUNDARY,
            "created_at_utc": now_utc(),
        },
    )


def write_lineage() -> None:
    inputs = [
        {
            "path": rel(path),
            "exists": path_is_file(path),
            "sha256": sha256_file(path) if path_is_file(path) else "",
        }
        for path in INPUT_FILES
    ]
    outputs = [
        {
            "path": rel(path),
            "exists": path_is_file(path),
            "sha256": sha256_file(path) if path_is_file(path) else "",
        }
        for path in OUTPUT_FILES
        if path != ARTIFACT_REGISTRY
    ]
    write_json(
        LINEAGE_RECEIPT,
        {
            "receipt_id": "run344G_artifact_lineage(산출물 계보)",
            "run_id": RUN_ID,
            "parent_run_id": PARENT_RUN_ID,
            "source_package_run_id": SOURCE_PACKAGE_RUN_ID,
            "source_runtime_run_id": SOURCE_RUNTIME_RUN_ID,
            "source_inputs": inputs,
            "artifact_paths": outputs,
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "lineage_judgment": "connected_with_package_boundary(패키지 경계로 연결됨)",
            "claim_boundary": CLAIM_BOUNDARY,
            "created_at_utc": now_utc(),
        },
    )


def write_docs(final: Mapping[str, Any]) -> None:
    report = f"""# run344G s07 Forward/Cost/Stability Validation Package(344G s07 전진/비용/안정성 검증 패키지)

## Current Truth(현재 진실)

- run_id(실행 ID): `{RUN_ID}`
- parent_run(부모 실행): `{PARENT_RUN_ID}`
- attempts(시도): `{final['attempt_rows']}`
- expected_rows(예상 행): `{final['expected_rows']}`
- set_rows(set 행): `{final['set_rows']}`
- ini_rows(ini 행): `{final['ini_rows']}`
- common_sync_missing(공용 동기화 누락): `{final['common_sync_missing']}`
- next_run(다음 실행): `{NEXT_RUN_ID}`
- Goal Achieve(목표 달성): `{final['goal_achieve']}`

## Action(행동)

run344F design(설계)에서 정한 s07/s05/s01 검증 범위를 실제 ONNX(온엑스), feature(피처), expected tape(예상 테이프), set/ini(설정 파일), cost/session contract(비용/세션 계약) 패키지로 물질화했다.

## Effect(효과)

다음 run344H는 설계 해석 없이 바로 MT5 Strategy Tester(MT5 전략 테스터) 실행과 telemetry(텔레메트리) 수집을 할 수 있다.

## Boundary(경계)

이 run(실행)은 package only(패키지 전용)이다. MT5 execution(MT5 실행), forward pass(전진 통과), selection(선정), operating promotion(운영 승격), runtime authority(런타임 권위)는 없다.
"""
    decision = f"""# {TODAY} Stage344G Package Decision(344G 패키지 결정)

- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- attempts(시도): `{final['selected_attempts']}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- evidence(근거): `{rel(RUNTIME_PROBE_ATTEMPT_PACKAGE)}`, `{rel(TESTER_SET_MANIFEST)}`, `{rel(TESTER_INI_MANIFEST)}`, `{rel(RUNTIME_PARITY_CONTRACT)}`

Action(행동): s07 검증 패키지를 물질화했다.
Effect(효과): 다음 작업은 MT5 runtime probe(런타임 탐침) 실행으로 좁혀진다.

claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    current = f"""# Current Working State(현재 작업 상태)

## Current Truth(현재 진실)

- active_stage(현재 단계): `{STAGE_ID}`
- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`

## Effect(효과)

run344G materialization(물질화)이 완료되어 다음은 run344H MT5 runtime probe(MT5 런타임 탐침) 실행이다.

## Boundary(경계)

`{CLAIM_BOUNDARY}`
"""
    selection = f"""# Stage 344 Selection Status(344단계 선정 상태)

- selected_model(선정 모델): `none(없음)`
- promotion_candidate(승격 후보): `s07_trend_confirmed_long_only`
- package_status(패키지 상태): `run344G_materialized_ready_for_mt5_probe(344G 물질화 완료, MT5 탐침 준비)`
- attempts(시도): `{final['selected_attempts']}`
- runtime_authority(런타임 권위): `not_claimed(주장 없음)`
- operating_promotion(운영 승격): `not_claimed(주장 없음)`
- Goal Achieve(목표 달성): `not_claimed(주장 없음)`

Effect(효과): s07은 검증 패키지 준비 상태일 뿐 운영 선정은 아니다.
"""
    workspace = f"""current_stage_id: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {STATUS}
current_judgment: {JUDGMENT}
current_decision: {DECISION}
next_run_id: {NEXT_RUN_ID}
claim_boundary: {CLAIM_BOUNDARY}
updated_at: {TODAY}
"""
    write_text(REPORT_PATH, report)
    write_text(DECISION_DOC, decision)
    write_text(CURRENT_WORKING_STATE, current)
    write_text(SELECTION_STATUS, selection)
    write_text(ROOT_SELECTION_STATUS, selection)
    write_text(WORKSPACE_STATE, workspace)
    marker = f"run344G {RUN_ID}"
    append_text_once(
        STAGE_BRIEF,
        marker,
        f"""## run344G s07 Validation Package(344G s07 검증 패키지)

- run_id(실행 ID): `{RUN_ID}`
- attempts(시도): `{final['attempt_rows']}`
- expected_rows(예상 행): `{final['expected_rows']}`
- next_run(다음 실행): `{NEXT_RUN_ID}`
- effect(효과): run344H MT5 탐침 실행 패키지를 준비.
""",
    )
    append_text_once(
        STAGE_README,
        marker,
        f"""## run344G s07 Validation Package(344G s07 검증 패키지)

- report(보고서): `{rel(REPORT_PATH)}`
- attempt_package(시도 패키지): `{rel(RUNTIME_PROBE_ATTEMPT_PACKAGE)}`
- next_queue(다음 대기열): `{rel(RUN344H_QUEUE)}`
- effect(효과): MT5 실행으로 바로 이어질 수 있게 파일을 고정.
""",
    )
    changelog = f"""## {TODAY} run344G s07 Validation Package(s07 검증 패키지)

- action(행동): s07/s05/s01 검증 패키지를 ONNX(온엑스), set/ini(설정), expected tape(예상 테이프), contract(계약)로 물질화했다.
- effect(효과): 다음 run344H는 MT5 runtime probe(런타임 탐침)를 바로 실행할 수 있다.
- boundary(경계): 패키지 전용이며 운영 주장은 없음.
"""
    append_text_once(ROOT_CHANGELOG, marker, changelog)
    append_text_once(WORKSPACE_CHANGELOG, marker, changelog)


def write_registers(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    gate_passes = sum(1 for row in gates if row["status"] == "passed")
    gate_total = len(gates)
    base = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "run_date": TODAY,
        "date": TODAY,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_run_id": NEXT_RUN_ID,
        "primary_artifact": rel(FINAL_DECISION),
        "report_path": rel(REPORT_PATH),
        "path": rel(REPORT_PATH),
        "gate_passes": gate_passes,
        "gate_total": gate_total,
        "claim_boundary": CLAIM_BOUNDARY,
        "source_package_run_id": SOURCE_PACKAGE_RUN_ID,
    }
    run_row = {
        **base,
        "lane": "runtime_probe_package(런타임 탐침 패키지)",
        "family": "runtime_backtest(MT5/런타임 백테스트)",
        "primary_report": rel(REPORT_PATH),
        "run_number": RUN_NUMBER,
        "notes": "s07 validation package materialized(s07 검증 패키지 물질화); no MT5 execution(MT5 실행 없음).",
        "candidate_model_id": "logreg_balanced_c025_s07_trend_confirmed_long_only",
        "attempt_count": final["attempt_rows"],
        "sample_rows": final["feature_rows"],
        "matched_rows": final["expected_rows"],
        "result_status": JUDGMENT,
    }
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], [run_row])
    ledger_rows = [
        {
            **base,
            "ledger_row_id": f"{RUN_ID}__Tier A",
            "subrun_id": "Tier A",
            "view": "Tier A separate(Tier A 분리)",
            "record_view": "Tier A separate(Tier A 분리)",
            "tier": "Tier A",
            "tier_scope": "Tier A",
            "metric_scope": "runtime_package_no_mt5_kpi",
            "kpi_scope": "runtime_package_no_mt5_kpi",
            "scoreboard_lane": "runtime_probe_package(런타임 탐침 패키지)",
            "candidate_model_id": "logreg_balanced_c025_s07_trend_confirmed_long_only",
            "sample_rows": final["feature_rows"],
            "matched_rows": final["expected_rows"],
            "attempt_count": final["attempt_rows"],
            "result_status": JUDGMENT,
            "primary_kpi": f"attempts={final['attempt_rows']};expected_rows={final['expected_rows']}",
            "guardrail_kpi": f"common_sync_missing={final['common_sync_missing']};set_rows={final['set_rows']};ini_rows={final['ini_rows']}",
            "external_verification_status": "pending_mt5_runtime_probe(MT5 런타임 탐침 대기)",
            "notes": "Package only(패키지 전용); opens run344H MT5 runtime probe(344H MT5 런타임 탐침 개방).",
        },
        {
            **base,
            "ledger_row_id": f"{RUN_ID}__Tier B",
            "subrun_id": "Tier B",
            "view": "Tier B separate(Tier B 분리)",
            "record_view": "Tier B separate(Tier B 분리)",
            "tier": "Tier B",
            "tier_scope": "Tier B",
            "metric_scope": "missing_required",
            "kpi_scope": "missing_required",
            "scoreboard_lane": "runtime_probe_package(런타임 탐침 패키지)",
            "candidate_model_id": "missing_required",
            "primary_kpi": "missing_required",
            "guardrail_kpi": "missing_required",
            "external_verification_status": "missing_required(필수 누락)",
            "result_status": "missing_required(필수 누락)",
            "notes": "Tier B(티어 B)는 이번 package(패키지) 범위 밖이므로 필수 누락으로 기록.",
        },
        {
            **base,
            "ledger_row_id": f"{RUN_ID}__Tier A+B",
            "subrun_id": "Tier A+B",
            "view": "Tier A+B combined(Tier A+B 합산)",
            "record_view": "Tier A+B combined(Tier A+B 합산)",
            "tier": "Tier A+B",
            "tier_scope": "Tier A+B",
            "metric_scope": "same_as_tier_a_until_tier_b_available",
            "kpi_scope": "same_as_tier_a_until_tier_b_available",
            "scoreboard_lane": "runtime_probe_package(런타임 탐침 패키지)",
            "candidate_model_id": "logreg_balanced_c025_s07_trend_confirmed_long_only",
            "sample_rows": final["feature_rows"],
            "matched_rows": final["expected_rows"],
            "attempt_count": final["attempt_rows"],
            "result_status": "same_as_tier_a_until_tier_b_available",
            "primary_kpi": f"attempts={final['attempt_rows']};expected_rows={final['expected_rows']}",
            "guardrail_kpi": f"common_sync_missing={final['common_sync_missing']};set_rows={final['set_rows']};ini_rows={final['ini_rows']}",
            "external_verification_status": "pending_mt5_runtime_probe(MT5 런타임 탐침 대기)",
            "notes": "Combined(합산)는 Tier B(티어 B) 부재로 Tier A와 같은 패키지 경계.",
        },
    ]
    append_or_replace_csv(PROJECT_LEDGER, ["run_id", "view"], ledger_rows)
    append_or_replace_csv(STAGE_LEDGER, ["run_id", "view"], ledger_rows)


def write_artifact_registry() -> None:
    rows = []
    for index, path in enumerate(OUTPUT_FILES, start=1):
        if path == ARTIFACT_REGISTRY or not path_is_file(path):
            continue
        artifact_type = "script" if path == Path(__file__) else path.suffix.lstrip(".") or "artifact"
        rows.append(
            {
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "artifact_type": artifact_type,
                "path": rel(path),
                "artifact_path": rel(path),
                "sha256": sha256_file(path),
                "created_at": TODAY,
                "created_at_utc": now_utc(),
                "artifact_id": f"{RUN_NUMBER}_{index:02d}_{artifact_type}",
                "notes": "run344G validation package output(344G 검증 패키지 산출물)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    if path_is_file(ARTIFACT_REGISTRY):
        fieldnames, existing = source_pkg.read_csv_rows(ARTIFACT_REGISTRY)
    else:
        fieldnames, existing = [], []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    kept = [row for row in existing if row.get("run_id") != RUN_ID]
    ensure_parent(ARTIFACT_REGISTRY)
    with open(ARTIFACT_REGISTRY, "w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in kept + rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def cleanup_stale_outputs() -> None:
    run_root = RUN_DIR.resolve()
    if not os.path.isdir(source_pkg.fs_path(run_root)):
        return
    for child in RUN_DIR.iterdir():
        resolved = child.resolve()
        if not str(resolved).lower().startswith(str(run_root).lower()):
            raise RuntimeError(f"refusing stale output outside run dir: {child}")


def main() -> None:
    cleanup_stale_outputs()
    final = build_package()
    gates = make_gates(final)
    final = {
        **final,
        "gate_passes": sum(1 for row in gates if row["status"] == "passed"),
        "gate_total": len(gates),
    }
    write_csv(GATE_AUDIT, gates)
    write_json(FINAL_DECISION, final)
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "source_package_run_id": SOURCE_PACKAGE_RUN_ID,
            "source_runtime_run_id": SOURCE_RUNTIME_RUN_ID,
            "status": STATUS,
            "judgment": JUDGMENT,
            "decision": DECISION,
            "inputs": [rel(path) for path in INPUT_FILES],
            "outputs": [rel(path) for path in OUTPUT_FILES],
            "gates": gates,
            "claim_boundary": CLAIM_BOUNDARY,
            "created_at_utc": now_utc(),
        },
    )
    write_receipts(final)
    write_docs(final)
    write_registers(final, gates)
    write_lineage()
    write_artifact_registry()

    if any(row["status"] != "passed" for row in gates):
        raise RuntimeError("run344G gate audit failed")

    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "attempt_rows": final["attempt_rows"],
                "expected_rows": final["expected_rows"],
                "gate_passes": final["gate_passes"],
                "gate_total": final["gate_total"],
                "next_run_id": NEXT_RUN_ID,
                "goal_achieve": final["goal_achieve"],
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
