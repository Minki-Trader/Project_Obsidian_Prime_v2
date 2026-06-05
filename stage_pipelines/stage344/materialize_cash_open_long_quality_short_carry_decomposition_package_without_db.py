from __future__ import annotations

import csv
import json
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
    design_cash_open_long_quality_short_carry_decomposition_probe_without_db as design,
)
from stage_pipelines.stage344 import (  # noqa: E402
    materialize_directional_long_supply_quality_surface_package_without_db as surface_pkg,
)
from stage_pipelines.stage344 import (  # noqa: E402
    materialize_s07_forward_cost_stability_validation_package_without_db as source_pkg,
)


TODAY = "2026-06-01"
STAGE_ID = design.STAGE_ID
STAGE_DIR = design.STAGE_DIR
RUN_NUMBER = "run344N"
RUN_ID = "run344N_materialize_cash_open_long_quality_short_carry_decomposition_package_without_db_v1"
PARENT_RUN_ID = design.RUN_ID
SOURCE_PACKAGE_RUN_ID = source_pkg.RUN_ID
SOURCE_RUNTIME_RUN_ID = design.SOURCE_RUNTIME_RUN_ID
NEXT_RUN_ID = "run344O_execute_cash_open_long_quality_short_carry_decomposition_mt5_probe_without_db_v1"

STATUS = "completed_stage344N_cash_open_long_quality_short_carry_package_materialized_no_mt5_execution"
JUDGMENT = (
    "cash_open_long_quality_short_carry_package_ready_with_single_side_filter_limit_"
    "no_operating_claim"
)
DECISION = "stage344N_open_run344O_execute_cash_open_long_quality_short_carry_mt5_probe"
CLAIM_BOUNDARY = (
    "research_development_runtime_package_only_cash_open_long_quality_short_carry_decomposition_"
    "single_side_filter_limit_no_mt5_execution_no_candidate_selection_no_forward_pass_"
    "no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

S07_ATTEMPT = "s07_trend_confirmed_long_only"
EXPLORATION_LABEL = "stage344_CashOpenLongShort__DecompositionPackage"
MAGIC_BASE = 3445000

RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
FEATURE_DIR = RUN_DIR / "features"
EXPECTED_DIR = RUN_DIR / "expected"
MODEL_DIR = RUN_DIR / "models"
MT5_DIR = RUN_DIR / "mt5"
SET_DIR = MT5_DIR / "sets"
INI_DIR = MT5_DIR / "inis"

COMMON_ROOT = f"Project_Obsidian_Prime_v2/stage344/{RUN_NUMBER}_cash_open_decomp"
COMMON_FEATURE_DIR = f"{COMMON_ROOT}/features"
COMMON_MODEL_DIR = f"{COMMON_ROOT}/models"
COMMON_TELEMETRY_DIR = f"{COMMON_ROOT}/telemetry"

REPORT_PATH = REVIEW_DIR / "run344N_cash_open_long_quality_short_carry_decomposition_package.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage344N_cash_open_long_quality_short_carry_decomposition_package.md"
SELECTION_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
STAGE_README = STAGE_DIR / "README.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"

SOURCE_ATTEMPT_PACKAGE = STAGE_DIR / "02_runs" / "run344G" / "runtime_probe_attempt_package.csv"
SOURCE_FEATURE_MATRIX = STAGE_DIR / "02_runs" / "run344G" / "features" / "runtime_features.csv"
SOURCE_EXPECTED_TAPE = STAGE_DIR / "02_runs" / "run344G" / "expected" / "expected_tape.csv"
SOURCE_MODEL_HANDOFF = STAGE_DIR / "02_runs" / "run344G" / "model_handoff_manifest.csv"

FEATURE_MATRIX = FEATURE_DIR / "runtime_features.csv"
EXPECTED_TAPE = EXPECTED_DIR / "expected_tape.csv"
EXPECTED_TAPE_INDEX = RUN_DIR / "expected_tape_index.csv"
PACKAGEABILITY_MATRIX = RUN_DIR / "packageability_matrix.csv"
VARIANT_RUNTIME_MAPPING = RUN_DIR / "variant_runtime_mapping.csv"
RUNTIME_PROBE_ATTEMPT_PACKAGE = RUN_DIR / "runtime_probe_attempt_package.csv"
MODEL_HANDOFF_MANIFEST = RUN_DIR / "model_handoff_manifest.csv"
COMMON_FILES_SYNC = RUN_DIR / "common_files_sync.csv"
TESTER_SET_MANIFEST = RUN_DIR / "tester_set_manifest.csv"
TESTER_INI_MANIFEST = RUN_DIR / "tester_ini_manifest.csv"
TESTER_IDENTITY_CONTRACT = RUN_DIR / "tester_identity_contract.csv"
RUNTIME_PARITY_CONTRACT = RUN_DIR / "runtime_parity_contract.csv"
RUN344O_QUEUE = RUN_DIR / "run344O_queue.csv"
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

INPUT_FILES = (
    design.FINAL_DECISION,
    design.GATE_AUDIT,
    design.VARIANT_GRID_CONTRACT,
    design.RUNTIME_HANDOFF_PLAN,
    design.RUN344N_QUEUE,
    SOURCE_ATTEMPT_PACKAGE,
    SOURCE_FEATURE_MATRIX,
    SOURCE_EXPECTED_TAPE,
    SOURCE_MODEL_HANDOFF,
)

OUTPUT_FILES = (
    FEATURE_MATRIX,
    EXPECTED_TAPE,
    EXPECTED_TAPE_INDEX,
    PACKAGEABILITY_MATRIX,
    VARIANT_RUNTIME_MAPPING,
    RUNTIME_PROBE_ATTEMPT_PACKAGE,
    MODEL_HANDOFF_MANIFEST,
    COMMON_FILES_SYNC,
    TESTER_SET_MANIFEST,
    TESTER_INI_MANIFEST,
    TESTER_IDENTITY_CONTRACT,
    RUNTIME_PARITY_CONTRACT,
    RUN344O_QUEUE,
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


def exists(path: Path) -> bool:
    return source_pkg.path_is_file(path)


def ensure_parent(path: Path) -> None:
    source_pkg.ensure_parent(path)


def required(path: Path) -> Path:
    return source_pkg.required(path)


def sha256_file(path: Path) -> str:
    return source_pkg.sha256_file(path)


def read_json(path: Path) -> Any:
    return source_pkg.read_json(path)


def read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, low_memory=False)


def write_json(path: Path, payload: Any) -> None:
    source_pkg.write_json(path, payload)


def write_text(path: Path, text: str) -> None:
    source_pkg.write_text(path, text)


def append_text_once(path: Path, marker: str, text: str) -> None:
    source_pkg.append_text_once(path, marker, text)


def append_or_replace_csv(path: Path, keys: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> None:
    source_pkg.append_or_replace_csv(path, keys, rows)


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
    with open(path, "w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fieldnames), extrasaction="ignore")
        writer.writeheader()
        for row in rows_list:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def write_frame(path: Path, frame: pd.DataFrame) -> None:
    ensure_parent(path)
    frame.to_csv(path, index=False, encoding="utf-8-sig")


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        if pd.isna(value) or value == "":
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def as_int(value: Any, default: int = 0) -> int:
    try:
        if pd.isna(value) or value == "":
            return default
        return int(round(float(value)))
    except (TypeError, ValueError):
        return default


def as_bool(value: Any) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def parse_range(text: Any) -> tuple[bool, float, float]:
    return surface_pkg.parse_range(text)


def decide_label(p_short: float, p_flat: float, p_long: float, short_threshold: float, long_threshold: float, min_margin: float) -> str:
    return surface_pkg.decide_label(p_short, p_flat, p_long, short_threshold, long_threshold, min_margin)


def label_class(label: str) -> int:
    return surface_pkg.label_class(label)


def parent_gates_passed() -> bool:
    gates = read_csv(design.GATE_AUDIT)
    return bool(len(gates) > 0 and gates["status"].astype(str).str.lower().eq("passed").all())


def copy_file(source: Path, target: Path, sync_id: str, effect: str) -> dict[str, Any]:
    ensure_parent(target)
    shutil.copy2(source, target)
    ok = exists(target)
    return {
        "sync_id": sync_id,
        "source_path": rel(source) if str(source.resolve()).lower().startswith(str(ROOT.resolve()).lower()) else source.as_posix(),
        "target_path": rel(target) if str(target.resolve()).lower().startswith(str(ROOT.resolve()).lower()) else target.as_posix(),
        "exists": ok,
        "sha256": sha256_file(target) if ok else "",
        "status": "synced(동기화됨)" if ok else "missing(누락)",
        "effect": effect,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def source_s07_config(source_attempts: pd.DataFrame) -> Mapping[str, Any]:
    row = source_attempts.loc[source_attempts["attempt_name"].astype(str).eq(S07_ATTEMPT)]
    if row.empty:
        raise RuntimeError("missing s07 source attempt package")
    return row.iloc[0].to_dict()


def source_s07_model(source_models: pd.DataFrame) -> Path:
    row = source_models.loc[source_models["attempt_name"].astype(str).eq(S07_ATTEMPT)]
    if row.empty:
        raise RuntimeError("missing s07 model handoff row")
    return ROOT / str(row.iloc[0]["local_model_path"])


def feature_index_map(features: pd.DataFrame) -> dict[str, int]:
    return {column: index for index, column in enumerate([col for col in features.columns if col != "timestamp"])}


def variant_specs(source_config: Mapping[str, Any], features: pd.DataFrame) -> list[dict[str, Any]]:
    feature_index = feature_index_map(features)
    adx_index = feature_index["adx_14"]
    minutes_index = feature_index["minutes_from_cash_open"]
    base_short = as_float(source_config["short_threshold"])
    base_long = as_float(source_config["long_threshold"])
    min_margin = as_float(source_config["min_margin"])
    max_hold = as_int(source_config["max_hold_bars"])
    fixed_lot = as_float(source_config["fixed_lot"])
    base_block_long = str(source_config.get("block_long_range", ""))
    common = {
        "source_attempt": S07_ATTEMPT,
        "base_model_id": "logreg_balanced_c025",
        "feature_set_id": source_config.get("feature_set_id", ""),
        "feature_count": as_int(source_config.get("feature_count")),
        "feature_order_hash": source_config.get("feature_order_hash", ""),
        "from_date": source_config.get("from_date", "2024.07.30"),
        "to_date": source_config.get("to_date", "2025.01.01"),
        "decision_mode": "threshold_margin",
        "min_margin": min_margin,
        "fixed_lot": fixed_lot,
        "max_hold_bars": max_hold,
        "close_on_flat": False,
    }
    return [
        {
            **common,
            "attempt_name": "n01_s07_base_control",
            "package_short_name": "n01_base",
            "model_id": "logreg_balanced_c025_n01_s07_base_control",
            "variant_role": "base_control(기본 대조)",
            "short_threshold": base_short,
            "long_threshold": base_long,
            "side_filter_enabled": True,
            "side_filter_feature_index": adx_index,
            "side_filter_feature_name": "adx_14",
            "block_long_range": base_block_long,
            "block_short_range": "",
            "known_difference": "none_exact_s07_parameter_copy(s07 파라미터 정확 복사)",
            "source_design_variant": "control_not_from_posthoc_grid(대조용)",
        },
        {
            **common,
            "attempt_name": "n02_s07_long_only_disable_short",
            "package_short_name": "n02_long",
            "model_id": "logreg_balanced_c025_n02_s07_long_only_disable_short",
            "variant_role": "long_only_control(롱 전용 대조)",
            "short_threshold": 2.0,
            "long_threshold": base_long,
            "side_filter_enabled": True,
            "side_filter_feature_index": adx_index,
            "side_filter_feature_name": "adx_14",
            "block_long_range": base_block_long,
            "block_short_range": "",
            "known_difference": "short side disabled by unreachable threshold(숏을 도달 불가 임계값으로 비활성화)",
            "source_design_variant": "m05_s07_long_only_all_sessions",
        },
        {
            **common,
            "attempt_name": "n03_s07_short_only_disable_long",
            "package_short_name": "n03_short",
            "model_id": "logreg_balanced_c025_n03_s07_short_only_disable_long",
            "variant_role": "short_only_control(숏 전용 대조)",
            "short_threshold": base_short,
            "long_threshold": 2.0,
            "side_filter_enabled": True,
            "side_filter_feature_index": adx_index,
            "side_filter_feature_name": "adx_14",
            "block_long_range": base_block_long,
            "block_short_range": "",
            "known_difference": "long side disabled by unreachable threshold(롱을 도달 불가 임계값으로 비활성화)",
            "source_design_variant": "m06_s07_sell_only_all_sessions",
        },
        {
            **common,
            "attempt_name": "n04_s07_no_cash_open_short_single_filter",
            "package_short_name": "n04_nocos",
            "model_id": "logreg_balanced_c025_n04_s07_no_cash_open_short_single_filter",
            "variant_role": "cash_open_short_block(현금장 초반 숏 차단)",
            "short_threshold": base_short,
            "long_threshold": base_long,
            "side_filter_enabled": True,
            "side_filter_feature_index": minutes_index,
            "side_filter_feature_name": "minutes_from_cash_open",
            "block_long_range": "",
            "block_short_range": "0,60",
            "known_difference": "single side filter replaces s07 ADX long block(단일 사이드 필터가 s07 ADX 롱 차단을 대체)",
            "source_design_variant": "m08_no_cash_open_short",
        },
        {
            **common,
            "attempt_name": "n05_s07_late_long_firewall_single_filter",
            "package_short_name": "n05_latefw",
            "model_id": "logreg_balanced_c025_n05_s07_late_long_firewall_single_filter",
            "variant_role": "late_long_firewall(후반 롱 방화벽)",
            "short_threshold": base_short,
            "long_threshold": base_long,
            "side_filter_enabled": True,
            "side_filter_feature_index": minutes_index,
            "side_filter_feature_name": "minutes_from_cash_open",
            "block_long_range": "210,10000",
            "block_short_range": "",
            "known_difference": "single side filter replaces s07 ADX long block(단일 사이드 필터가 s07 ADX 롱 차단을 대체)",
            "source_design_variant": "m04_s07_without_late_long",
        },
        {
            **common,
            "attempt_name": "n06_s07_long_only_late_firewall",
            "package_short_name": "n06_longfw",
            "model_id": "logreg_balanced_c025_n06_s07_long_only_late_firewall",
            "variant_role": "long_only_late_firewall(롱 전용 후반 방화벽)",
            "short_threshold": 2.0,
            "long_threshold": base_long,
            "side_filter_enabled": True,
            "side_filter_feature_index": minutes_index,
            "side_filter_feature_name": "minutes_from_cash_open",
            "block_long_range": "210,10000",
            "block_short_range": "",
            "known_difference": "exploratory combination; replaces s07 ADX long block(탐색 조합, s07 ADX 롱 차단 대체)",
            "source_design_variant": "derived_from_m04_and_m05(m04/m05 파생)",
        },
    ]


def build_packageability_matrix(variant_grid: pd.DataFrame, packaged: Sequence[Mapping[str, Any]]) -> pd.DataFrame:
    packaged_by_source = {str(row["source_design_variant"]): row for row in packaged}
    rows: list[dict[str, Any]] = [
        {
            "design_variant_id": "control_not_from_posthoc_grid(대조용)",
            "package_status": "packageable(포장 가능)",
            "runtime_attempt": "n01_s07_base_control",
            "reason": "exact s07 package control(정확 s07 패키지 대조)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    for _, row in variant_grid.iterrows():
        variant_id = str(row["variant_id"])
        if variant_id in packaged_by_source:
            spec = packaged_by_source[variant_id]
            status = "packageable_with_boundary(경계 포함 포장 가능)"
            runtime_attempt = spec["attempt_name"]
            reason = spec["known_difference"]
        elif variant_id in {"m01_cash_open_long_only", "m02_cash_open_short_carry_only", "m03_cash_open_directional_mix", "m07_long_all_plus_cash_open_short"}:
            status = "not_packageable_current_ea(현재 EA 포장 불가)"
            runtime_attempt = ""
            reason = "current EA has one contiguous side-filter range, so exact cash-open-only routing needs module change(현재 EA는 단일 연속 사이드 필터만 있어 정확한 현금장 전용 라우팅은 모듈 변경 필요)"
        else:
            status = "not_selected_for_package(이번 포장 제외)"
            runtime_attempt = ""
            reason = "covered by a derived package attempt or lower priority(파생 패키지 시도나 낮은 우선순위로 처리)"
        rows.append(
            {
                "design_variant_id": variant_id,
                "package_status": status,
                "runtime_attempt": runtime_attempt,
                "reason": reason,
                "posthoc_proxy_net": row.get("trade_filter_proxy_net_profit", ""),
                "posthoc_heavy_recovery": row.get("heavy_adjusted_recovery_factor_vs_parent_dd", ""),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    rows.append(
        {
            "design_variant_id": "derived_from_m04_and_m05(m04/m05 파생)",
            "package_status": "packageable_with_boundary(경계 포함 포장 가능)",
            "runtime_attempt": "n06_s07_long_only_late_firewall",
            "reason": "extra exploratory combination for long-only plus late firewall(롱 전용과 후반 방화벽 추가 탐색 조합)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    )
    return pd.DataFrame(rows)


def build_expected_tape(variants: Sequence[Mapping[str, Any]], source_expected: pd.DataFrame, features: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    feature_lookup = features.set_index("timestamp", drop=False)
    source = source_expected.loc[source_expected["attempt_name"].astype(str).eq(S07_ATTEMPT)].copy()
    if source.empty:
        raise RuntimeError("source s07 expected tape is empty")
    expected_rows: list[dict[str, Any]] = []
    index_rows: list[dict[str, Any]] = []
    for variant in variants:
        labels: list[str] = []
        blocked_long = 0
        blocked_short = 0
        missing_feature_rows = 0
        block_long_enabled, block_long_min, block_long_max = parse_range(variant.get("block_long_range", ""))
        block_short_enabled, block_short_min, block_short_max = parse_range(variant.get("block_short_range", ""))
        for _, row in source.iterrows():
            p_short = as_float(row.get("p_short"))
            p_flat = as_float(row.get("p_flat"))
            p_long = as_float(row.get("p_long"))
            pre_label = decide_label(
                p_short,
                p_flat,
                p_long,
                as_float(variant["short_threshold"]),
                as_float(variant["long_threshold"]),
                as_float(variant["min_margin"]),
            )
            label = pre_label
            side_applied = False
            side_reason = ""
            feature_value: float | str = ""
            bar_time = str(row.get("bar_time", ""))
            if as_bool(variant["side_filter_enabled"]) and pre_label != "flat":
                feature_name = str(variant["side_filter_feature_name"])
                if bar_time in feature_lookup.index:
                    feature_value = as_float(feature_lookup.loc[bar_time, feature_name])
                    if pre_label == "long" and block_long_enabled and block_long_min <= float(feature_value) <= block_long_max:
                        label = "flat"
                        side_applied = True
                        blocked_long += 1
                        side_reason = "side_filter_block_long_feature_range(사이드 필터 롱 범위 차단)"
                    elif pre_label == "short" and block_short_enabled and block_short_min <= float(feature_value) <= block_short_max:
                        label = "flat"
                        side_applied = True
                        blocked_short += 1
                        side_reason = "side_filter_block_short_feature_range(사이드 필터 숏 범위 차단)"
                else:
                    missing_feature_rows += 1
            labels.append(label)
            expected_rows.append(
                {
                    "attempt_name": variant["attempt_name"],
                    "model_id": variant["model_id"],
                    "base_model_id": variant["base_model_id"],
                    "source_attempt_name": S07_ATTEMPT,
                    "bar_time": bar_time,
                    "source_time": row.get("source_time", bar_time),
                    "source_row_id": row.get("source_row_id", ""),
                    "feature_input_hash": row.get("feature_input_hash", ""),
                    "p_short": p_short,
                    "p_flat": p_flat,
                    "p_long": p_long,
                    "pre_filter_decision_label": pre_label,
                    "decision_class": label_class(label),
                    "decision_label": label,
                    "short_threshold": variant["short_threshold"],
                    "long_threshold": variant["long_threshold"],
                    "min_margin": variant["min_margin"],
                    "max_hold_bars": variant["max_hold_bars"],
                    "close_on_flat": variant["close_on_flat"],
                    "side_filter_enabled": variant["side_filter_enabled"],
                    "side_filter_feature_index": variant["side_filter_feature_index"],
                    "side_filter_feature_name": variant["side_filter_feature_name"],
                    "side_filter_feature_value": feature_value,
                    "side_filter_applied": side_applied,
                    "side_filter_reason": side_reason,
                    "block_long_range_enabled": block_long_enabled,
                    "block_long_min": block_long_min,
                    "block_long_max": block_long_max,
                    "block_short_range_enabled": block_short_enabled,
                    "block_short_min": block_short_min,
                    "block_short_max": block_short_max,
                    "variant_role": variant["variant_role"],
                    "known_difference": variant["known_difference"],
                    "allowed_use": "proxy-vs-MT5 runtime parity comparison(프록시-MT5 런타임 동등성 비교)",
                    "forbidden_use": "MT5 KPI substitute or operating selection(MT5 KPI 대체 또는 운영 선정)",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
        counts = pd.Series(labels).value_counts()
        index_rows.append(
            {
                "attempt_name": variant["attempt_name"],
                "model_id": variant["model_id"],
                "row_count": int(len(labels)),
                "signal_long_count": int(counts.get("long", 0)),
                "signal_short_count": int(counts.get("short", 0)),
                "signal_flat_count": int(counts.get("flat", 0)),
                "blocked_long_count": blocked_long,
                "blocked_short_count": blocked_short,
                "missing_feature_rows": missing_feature_rows,
                "path": rel(EXPECTED_TAPE),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return pd.DataFrame(expected_rows), pd.DataFrame(index_rows)


def materialize_runtime_package(variants: Sequence[Mapping[str, Any]], source_model: Path, features: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    sync_rows: list[dict[str, Any]] = []
    model_rows: list[dict[str, Any]] = []
    attempt_rows: list[dict[str, Any]] = []
    set_rows: list[dict[str, Any]] = []
    ini_rows: list[dict[str, Any]] = []
    tester_rows: list[dict[str, Any]] = []
    feature_common = f"{COMMON_FEATURE_DIR}/runtime_features.csv"
    sync_rows.append(copy_file(SOURCE_FEATURE_MATRIX, FEATURE_MATRIX, "local_feature_matrix", "피처 행렬을 run344N 패키지에 복사"))
    common_feature_path = source_pkg.source_pkg.DEFAULT_COMMON_FILES / Path(feature_common)
    sync_rows.append(copy_file(FEATURE_MATRIX, common_feature_path, "common_feature_matrix", "피처 행렬을 MT5 Common Files(MT5 공용 파일)에 복사"))
    feature_hash = sha256_file(FEATURE_MATRIX)
    feature_count = len([column for column in features.columns if column != "timestamp"])

    for index, variant in enumerate(variants, start=1):
        short = str(variant["package_short_name"])
        local_model = MODEL_DIR / f"{short}.onnx"
        common_model = f"{COMMON_MODEL_DIR}/{short}.onnx"
        common_model_path = source_pkg.source_pkg.DEFAULT_COMMON_FILES / Path(common_model)
        sync_rows.append(copy_file(source_model, local_model, f"local_model::{variant['attempt_name']}", "s07 ONNX(온엑스)를 변형 이름으로 복사"))
        sync_rows.append(copy_file(local_model, common_model_path, f"common_model::{variant['attempt_name']}", "s07 ONNX(온엑스)를 MT5 Common Files(MT5 공용 파일)에 복사"))
        set_name = f"OPV2_{RUN_NUMBER}_{short}.set"
        ini_name = f"OPV2_{RUN_NUMBER}_{short}.ini"
        report_name = f"POPv2_{RUN_NUMBER}_{short}"
        set_path = SET_DIR / set_name
        ini_path = INI_DIR / ini_name
        block_long_enabled, block_long_min, block_long_max = parse_range(variant.get("block_long_range", ""))
        block_short_enabled, block_short_min, block_short_max = parse_range(variant.get("block_short_range", ""))
        set_values = {
            "InpRunId": f"{RUN_ID}_{variant['attempt_name']}",
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
            "InpModelId": variant["model_id"],
            "InpModelBackend": "onnx",
            "InpModelUseCommonFiles": True,
            "InpModelUseCpuOnly": True,
            "InpModelNoConversion": False,
            "InpSetOutputShape": True,
            "InpFeatureOrderHash": variant["feature_order_hash"],
            "InpFallbackEnabled": False,
            "InpShortThreshold": variant["short_threshold"],
            "InpLongThreshold": variant["long_threshold"],
            "InpMinMargin": variant["min_margin"],
            "InpDecisionMode": variant["decision_mode"],
            "InpInvertSignal": False,
            "InpSideFilterEnabled": variant["side_filter_enabled"],
            "InpSideFilterFeatureIndex": variant["side_filter_feature_index"],
            "InpFallbackSideFilterFeatureIndex": variant["side_filter_feature_index"],
            "InpBlockShortFeatureRange": block_short_enabled,
            "InpBlockShortFeatureMin": block_short_min,
            "InpBlockShortFeatureMax": block_short_max,
            "InpBlockLongFeatureRange": block_long_enabled,
            "InpBlockLongFeatureMin": block_long_min,
            "InpBlockLongFeatureMax": block_long_max,
            "InpAllowTrading": True,
            "InpFixedLot": variant["fixed_lot"],
            "InpMagic": MAGIC_BASE + index,
            "InpDeviationPoints": 20,
            "InpCloseOnFlatSignal": variant["close_on_flat"],
            "InpReverseOnOppositeSignal": True,
            "InpCloseOnlyOnOppositeSignal": False,
            "InpMaxHoldBars": variant["max_hold_bars"],
            "InpMaxConcurrentPositions": 1,
            "InpReentryCooldownBars": 0,
            "InpSameDirectionReentryCooldownBars": 0,
            "InpEntryTransitionOnly": False,
            "InpExitRiskOverlayEnabled": False,
            "InpAtrSltpEnabled": False,
            "InpModelRiskSizingEnabled": False,
            "InpTelemetryEnabled": True,
            "InpTelemetryUseCommonFiles": True,
            "InpTelemetryCsvPath": f"{COMMON_TELEMETRY_DIR}/{short}_telemetry.csv",
            "InpSummaryCsvPath": f"{COMMON_TELEMETRY_DIR}/{short}_summary.csv",
        }
        set_payload = mt5.materialize_tester_set_file(set_values, set_path, generated_by=rel(Path(__file__)))
        ini_payload = mt5.materialize_tester_ini_file(
            mt5.TesterMaterializationConfig(
                shutdown_terminal=1,
                from_date=str(variant["from_date"]),
                to_date=str(variant["to_date"]),
                report=report_name,
            ),
            ini_path,
            set_file_path=Path(set_name),
        )
        tester = ini_payload["tester"]
        model_rows.append(
            {
                "attempt_name": variant["attempt_name"],
                "package_short_name": short,
                "model_id": variant["model_id"],
                "source_model_path": rel(source_model),
                "local_model_path": rel(local_model),
                "local_model_sha256": sha256_file(local_model),
                "common_model_path": common_model,
                "common_model_sha256": sha256_file(common_model_path),
                "feature_order_hash": variant["feature_order_hash"],
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        set_rows.append(
            {
                "attempt_name": variant["attempt_name"],
                "package_short_name": short,
                "variant_role": variant["variant_role"],
                "set_path": rel(set_path),
                "set_sha256": set_payload["sha256"],
                "short_threshold": variant["short_threshold"],
                "long_threshold": variant["long_threshold"],
                "side_filter_feature_index": variant["side_filter_feature_index"],
                "side_filter_feature_name": variant["side_filter_feature_name"],
                "block_long_range": variant["block_long_range"],
                "block_short_range": variant["block_short_range"],
                "magic": MAGIC_BASE + index,
                "known_difference": variant["known_difference"],
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        ini_rows.append(
            {
                "attempt_name": variant["attempt_name"],
                "package_short_name": short,
                "ini_path": rel(ini_path),
                "ini_sha256": ini_payload["sha256"],
                "set_name": set_name,
                "report_name": report_name,
                "from_date": variant["from_date"],
                "to_date": variant["to_date"],
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        tester_rows.append(
            {
                "attempt_name": variant["attempt_name"],
                "package_short_name": short,
                "tester_symbol": tester.get("symbol"),
                "tester_period": tester.get("period"),
                "tester_model": tester.get("model"),
                "tester_deposit": tester.get("deposit"),
                "tester_leverage": tester.get("leverage"),
                "tester_report": report_name,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        attempt_rows.append(
            {
                "attempt_name": variant["attempt_name"],
                "package_short_name": short,
                "queue_id": f"{RUN_NUMBER}_{short}",
                "next_run_id": NEXT_RUN_ID,
                "probe_priority": index,
                "tier": "Tier A",
                "split": "inner_holdout_runtime_collapsed_probe",
                "model_id": variant["model_id"],
                "base_model_id": variant["base_model_id"],
                "source_attempt": S07_ATTEMPT,
                "source_design_variant": variant["source_design_variant"],
                "feature_set_id": variant["feature_set_id"],
                "feature_count": feature_count,
                "feature_order_hash": variant["feature_order_hash"],
                "feature_local_path": rel(FEATURE_MATRIX),
                "feature_common_path": feature_common,
                "feature_matrix_sha256": feature_hash,
                "model_local_path": rel(local_model),
                "model_common_path": common_model,
                "expected_tape_path": rel(EXPECTED_TAPE),
                "common_telemetry_path": f"{COMMON_TELEMETRY_DIR}/{short}_telemetry.csv",
                "common_summary_path": f"{COMMON_TELEMETRY_DIR}/{short}_summary.csv",
                "set_path": rel(set_path),
                "set_name": set_name,
                "ini_path": rel(ini_path),
                "ini_name": ini_name,
                "report_name": report_name,
                "from_date": variant["from_date"],
                "to_date": variant["to_date"],
                "decision_mode": variant["decision_mode"],
                "short_threshold": variant["short_threshold"],
                "long_threshold": variant["long_threshold"],
                "min_margin": variant["min_margin"],
                "fixed_lot": variant["fixed_lot"],
                "max_hold_bars": variant["max_hold_bars"],
                "close_on_flat": variant["close_on_flat"],
                "side_filter_enabled": variant["side_filter_enabled"],
                "side_filter_feature_index": variant["side_filter_feature_index"],
                "side_filter_feature_name": variant["side_filter_feature_name"],
                "block_long_range": variant["block_long_range"],
                "block_short_range": variant["block_short_range"],
                "variant_role": variant["variant_role"],
                "known_difference": variant["known_difference"],
                "runtime_mapping": "single_side_filter_package(단일 사이드 필터 패키지)",
                "effect": "ready for narrow MT5 probe(좁은 MT5 탐침 준비)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return (
        pd.DataFrame(sync_rows),
        pd.DataFrame(model_rows),
        pd.DataFrame(attempt_rows),
        pd.DataFrame(set_rows),
        pd.DataFrame(ini_rows),
        pd.DataFrame(tester_rows),
    )


def make_gates(final: Mapping[str, Any]) -> pd.DataFrame:
    no_forbidden = (
        final["candidate_selection"] == "not_run"
        and final["mt5_execution"] == "not_run"
        and final["forward_passed"] == "not_claimed"
        and final["goal_achieve"] == "not_claimed"
        and final["runtime_authority"] == "not_claimed"
        and final["operating_promotion"] == "not_claimed"
    )
    rows = [
        ("parent_run344M_gates_passed", final["parent_gate_passed"], rel(design.GATE_AUDIT), "run344M gate(게이트)를 이어받음"),
        ("packageability_matrix_written", final["packageability_rows"] >= 10, rel(PACKAGEABILITY_MATRIX), "포장 가능성 한계 기록"),
        ("package_variants_materialized", final["attempt_rows"] >= 6, rel(RUNTIME_PROBE_ATTEMPT_PACKAGE), "런타임 시도 패키지 작성"),
        ("feature_model_common_sync_ready", final["common_sync_missing"] == 0, rel(COMMON_FILES_SYNC), "피처와 모델 공용 파일 동기화"),
        ("expected_tape_materialized", final["expected_rows"] == final["feature_rows"] * final["attempt_rows"], rel(EXPECTED_TAPE), "예상 테이프 작성"),
        ("set_ini_materialized", final["set_rows"] == final["attempt_rows"] and final["ini_rows"] == final["attempt_rows"], rel(TESTER_SET_MANIFEST), "set/ini 파일 작성"),
        ("runtime_parity_contract_written", final["runtime_parity_contract_rows"] == 1, rel(RUNTIME_PARITY_CONTRACT), "런타임 동등성 계약 작성"),
        ("next_mt5_probe_queue_written", final["queue_rows"] == final["attempt_rows"], rel(RUN344O_QUEUE), "다음 MT5 탐침 큐 작성"),
        ("no_forbidden_operating_claim", no_forbidden, rel(FINAL_DECISION), "패키지를 운영 주장으로 올리지 않음"),
        ("required_gate_coverage_audit_written", True, rel(GATE_AUDIT), "필수 gate coverage audit(게이트 커버리지 감사) 기록"),
    ]
    return pd.DataFrame(
        [
            {"gate_id": gate, "status": "passed" if passed else "failed", "evidence_path": evidence, "effect": effect, "claim_boundary": CLAIM_BOUNDARY}
            for gate, passed, evidence, effect in rows
        ]
    )


def write_receipts(final: Mapping[str, Any]) -> None:
    write_json(
        DATA_RECEIPT,
        {
            "run_id": RUN_ID,
            "data_source": [rel(SOURCE_FEATURE_MATRIX), rel(SOURCE_EXPECTED_TAPE)],
            "time_axis": "same M5 bar-close timestamps as run344G(344G와 같은 M5 봉 종료 시각)",
            "sample_scope": f"Tier A feature_rows={final['feature_rows']};attempts={final['attempt_rows']}",
            "feature_label_boundary": "expected tape recomputes runtime decisions from current-bar features only(예상 테이프는 현재 봉 피처만으로 런타임 결정을 재계산)",
            "split_boundary": "existing inner holdout runtime slice(기존 내부 홀드아웃 런타임 구간)",
            "leakage_risk": "posthoc package variants need MT5 probe before KPI meaning(사후 변형은 MT5 탐침 전 KPI 의미 없음)",
            "data_hash_or_identity": sha256_file(FEATURE_MATRIX),
            "integrity_judgment": "usable_with_boundary(경계 포함 사용 가능)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(
        RUNTIME_RECEIPT,
        {
            "run_id": RUN_ID,
            "research_path": rel(design.VARIANT_GRID_CONTRACT),
            "runtime_path": rel(RUNTIME_PROBE_ATTEMPT_PACKAGE),
            "shared_contract": "feature order, ONNX model, thresholds, side-filter values, M5 timestamp(피처 순서, ONNX 모델, 임계값, 사이드 필터 값, M5 시각)",
            "known_differences": "single side-filter limit prevents exact cash-open-only variants(단일 사이드 필터 한계로 정확한 현금장 전용 변형 불가)",
            "parity_check": "package-level expected tape only; MT5 tester pending run344O(패키지 수준 예상 테이프만, MT5 테스터는 run344O 대기)",
            "parity_identity": {
                "feature_hash": sha256_file(FEATURE_MATRIX),
                "attempt_package_hash": sha256_file(RUNTIME_PROBE_ATTEMPT_PACKAGE),
                "set_manifest_hash": sha256_file(TESTER_SET_MANIFEST),
            },
            "runtime_claim_boundary": "runtime_probe_package_only(런타임 탐침 패키지 전용)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            "run_id": RUN_ID,
            "allowed_claims": ["runtime package materialized(런타임 패키지 물질화)", "MT5 probe queued(MT5 탐침 큐 등록)"],
            "forbidden_claims": ["candidate selection(후보 선정)", "forward pass(전진 통과)", "operating promotion(운영 승격)", "runtime authority(런타임 권위)", "Goal Achieve(목표 달성)"],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def write_docs(final: Mapping[str, Any]) -> None:
    report = f"""# run344N Cash-Open Long/Short Runtime Package(344N 현금장 롱/숏 런타임 패키지)

## Summary(요약)

- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- packaged_attempts(포장 시도): `{final['attempt_rows']}`
- expected_rows(예상 행): `{final['expected_rows']}`
- common_sync_missing(공용 동기화 누락): `{final['common_sync_missing']}`
- next_run(다음 실행): `{NEXT_RUN_ID}`

## Action(행동)

run344M design(설계)을 받아 s07 base(기본), long-only(롱 전용), short-only(숏 전용), cash-open short block(현금장 초반 숏 차단), late-long firewall(후반 롱 방화벽)을 MT5 set/ini(설정 파일)와 expected tape(예상 테이프)로 물질화했다.

## Effect(효과)

run344O는 바로 MT5 Strategy Tester(MT5 전략 테스터)를 실행할 수 있다. 포장 가능성 표(packageability matrix, 포장 가능성 표)에 현재 EA(전문가 자문)의 single side-filter limit(단일 사이드 필터 한계)도 같이 남겼다.

## Boundary(경계)

이 run(실행)은 package only(패키지 전용)다. MT5 execution(MT5 실행), forward pass(전진 통과), operating promotion(운영 승격), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 주장하지 않는다.
"""
    decision = f"""# {TODAY} Stage344N Package Decision(344N 패키지 결정)

- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- evidence(근거): `{rel(RUNTIME_PROBE_ATTEMPT_PACKAGE)}`, `{rel(TESTER_SET_MANIFEST)}`, `{rel(TESTER_INI_MANIFEST)}`, `{rel(RUNTIME_PARITY_CONTRACT)}`

Action(행동): 현금장 롱/숏 분해 변형을 MT5 실행 패키지로 만들었다.
Effect(효과): 다음 작업은 run344O MT5 runtime probe(MT5 런타임 탐침) 실행이다.

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

run344N package(패키지)가 완료되어 run344O MT5 runtime probe(MT5 런타임 탐침)를 열었다.

## Boundary(경계)

`{CLAIM_BOUNDARY}`
"""
    selection = f"""# Stage 344 Selection Status(344단계 선정 상태)

- selected_model(선정 모델): `none(없음)`
- latest_package(최근 패키지): `{RUN_ID}`
- package_status(패키지 상태): `ready_for_run344O_mt5_probe(run344O MT5 탐침 준비)`
- runtime_authority(런타임 권위): `not_claimed(주장 없음)`
- operating_promotion(운영 승격): `not_claimed(주장 없음)`
- Goal Achieve(목표 달성): `not_claimed(주장 없음)`

Effect(효과): 실행 패키지는 준비됐지만 운영 선정은 열지 않는다.
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
    marker = f"run344N {RUN_ID}"
    append_text_once(
        STAGE_BRIEF,
        marker,
        f"""## run344N Cash-Open Runtime Package(344N 현금장 런타임 패키지)

- run_id(실행 ID): `{RUN_ID}`
- attempts(시도): `{final['attempt_rows']}`
- expected_rows(예상 행): `{final['expected_rows']}`
- effect(효과): run344O MT5 탐침을 열었다.
""",
    )
    append_text_once(
        STAGE_README,
        marker,
        f"""## run344N Cash-Open Runtime Package(344N 현금장 런타임 패키지)

- report(보고서): `{rel(REPORT_PATH)}`
- attempt_package(시도 패키지): `{rel(RUNTIME_PROBE_ATTEMPT_PACKAGE)}`
- packageability(포장 가능성): `{rel(PACKAGEABILITY_MATRIX)}`
- effect(효과): 단일 사이드 필터 한계를 기록하고 실행 가능한 변형을 포장했다.
""",
    )
    changelog = f"""## {TODAY} run344N Cash-Open Runtime Package(현금장 런타임 패키지)

- action(행동): 현금장 롱/숏 분해 변형을 MT5 set/ini(설정 파일)와 예상 테이프로 물질화했다.
- effect(효과): 다음 run344O는 MT5 runtime probe(런타임 탐침)를 실행할 수 있다.
- boundary(경계): 패키지 전용이며 운영 주장은 없음.
"""
    append_text_once(ROOT_CHANGELOG, marker, changelog)
    append_text_once(WORKSPACE_CHANGELOG, marker, changelog)


def write_registers(final: Mapping[str, Any], gates: pd.DataFrame) -> None:
    base_row = {
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
        "gate_passes": int(gates["status"].astype(str).eq("passed").sum()),
        "gate_total": int(len(gates)),
        "claim_boundary": CLAIM_BOUNDARY,
        "source_package_run_id": SOURCE_PACKAGE_RUN_ID,
    }
    run_row = {
        **base_row,
        "lane": "runtime_probe_package(런타임 탐침 패키지)",
        "family": "runtime_backtest(MT5/런타임 백테스트)",
        "primary_report": rel(REPORT_PATH),
        "run_number": RUN_NUMBER,
        "notes": "cash-open decomposition runtime package(현금장 분해 런타임 패키지); no MT5 execution(MT5 실행 없음).",
        "candidate_model_id": "logreg_balanced_c025_s07_runtime_variants",
        "attempt_count": final["attempt_rows"],
        "sample_rows": final["feature_rows"],
        "matched_rows": final["expected_rows"],
        "result_status": JUDGMENT,
    }
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], [run_row])
    rows = [
        {
            **base_row,
            "ledger_row_id": f"{RUN_ID}__Tier A",
            "subrun_id": "Tier A",
            "view": "Tier A separate(Tier A 분리)",
            "record_view": "Tier A separate(Tier A 분리)",
            "tier": "Tier A",
            "tier_scope": "Tier A",
            "metric_scope": "runtime_package_no_mt5_kpi",
            "kpi_scope": "runtime_package_no_mt5_kpi",
            "scoreboard_lane": "runtime_probe_package(런타임 탐침 패키지)",
            "candidate_model_id": "logreg_balanced_c025_s07_runtime_variants",
            "sample_rows": final["feature_rows"],
            "matched_rows": final["expected_rows"],
            "attempt_count": final["attempt_rows"],
            "result_status": JUDGMENT,
            "primary_kpi": f"attempts={final['attempt_rows']};expected_rows={final['expected_rows']}",
            "guardrail_kpi": f"common_sync_missing={final['common_sync_missing']};packageability_rows={final['packageability_rows']}",
            "external_verification_status": "pending_mt5_runtime_probe(MT5 런타임 탐침 대기)",
            "notes": "Tier A runtime package(Tier A 런타임 패키지); no selection(선정 없음).",
        },
        {
            **base_row,
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
            "notes": "Tier B was outside this package(Tier B는 이번 패키지 밖).",
        },
        {
            **base_row,
            "ledger_row_id": f"{RUN_ID}__Tier A+B",
            "subrun_id": "Tier A+B",
            "view": "Tier A+B combined(Tier A+B 합산)",
            "record_view": "Tier A+B combined(Tier A+B 합산)",
            "tier": "Tier A+B",
            "tier_scope": "Tier A+B",
            "metric_scope": "same_as_tier_a_until_tier_b_available",
            "kpi_scope": "same_as_tier_a_until_tier_b_available",
            "scoreboard_lane": "runtime_probe_package(런타임 탐침 패키지)",
            "candidate_model_id": "logreg_balanced_c025_s07_runtime_variants",
            "sample_rows": final["feature_rows"],
            "matched_rows": final["expected_rows"],
            "attempt_count": final["attempt_rows"],
            "result_status": "same_as_tier_a_until_tier_b_available",
            "primary_kpi": f"attempts={final['attempt_rows']};expected_rows={final['expected_rows']}",
            "guardrail_kpi": "Tier B missing_required(Tier B 필수 누락)",
            "external_verification_status": "pending_mt5_runtime_probe(MT5 런타임 탐침 대기)",
            "notes": "Combined view is same as Tier A until Tier B exists(Tier B 전에는 합산이 Tier A와 같음).",
        },
    ]
    append_or_replace_csv(PROJECT_LEDGER, ["run_id", "view"], rows)
    append_or_replace_csv(STAGE_LEDGER, ["run_id", "view"], rows)


def write_lineage_receipt() -> None:
    hashed = {
        rel(path): sha256_file(path)
        for path in OUTPUT_FILES
        if exists(path) and path not in {ARTIFACT_REGISTRY, LINEAGE_RECEIPT}
    }
    write_json(
        LINEAGE_RECEIPT,
        {
            "source_inputs": [rel(path) for path in INPUT_FILES],
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [rel(path) for path in OUTPUT_FILES if path != ARTIFACT_REGISTRY],
            "artifact_hashes": hashed,
            "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "availability": "tracked_or_reproducible_from_command(추적됨 또는 명령으로 재현 가능)",
            "lineage_judgment": "connected_with_runtime_package_boundary(런타임 패키지 경계 포함 연결)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def update_artifact_registry(paths: Sequence[Path]) -> None:
    ensure_parent(ARTIFACT_REGISTRY)
    existing_rows: list[dict[str, Any]] = []
    fieldnames: list[str] = []
    if exists(ARTIFACT_REGISTRY):
        with open(ARTIFACT_REGISTRY, "r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = list(reader.fieldnames or [])
            existing_rows = [dict(row) for row in reader]
    required_fields = ["stage_id", "run_id", "artifact_type", "path", "sha256", "created_at", "claim_boundary", "artifact_id", "created_at_utc", "notes", "artifact_path"]
    for field in required_fields:
        if field not in fieldnames:
            fieldnames.append(field)
    new_rows: list[dict[str, Any]] = []
    for path in paths:
        if not exists(path):
            continue
        artifact_id = f"{RUN_NUMBER}::{rel(path)}"
        new_rows.append(
            {
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "artifact_type": path.suffix.lower().lstrip(".") or "artifact",
                "path": rel(path),
                "artifact_path": rel(path),
                "sha256": sha256_file(path),
                "created_at": TODAY,
                "created_at_utc": now_utc(),
                "artifact_id": artifact_id,
                "notes": "run344N runtime package artifact(run344N 런타임 패키지 산출물)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    new_ids = {row["artifact_id"] for row in new_rows}
    kept = [row for row in existing_rows if row.get("artifact_id") not in new_ids]
    with open(ARTIFACT_REGISTRY, "w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in kept + new_rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def build_package() -> Mapping[str, Any]:
    for path in INPUT_FILES:
        required(path)
    parent_final = read_json(design.FINAL_DECISION)
    if parent_final.get("next_run_id") != RUN_ID:
        raise RuntimeError("run344M next_run_id does not point to run344N")
    if not parent_gates_passed():
        raise RuntimeError("run344M gate audit has failed rows")

    source_attempts = read_csv(SOURCE_ATTEMPT_PACKAGE)
    source_expected = read_csv(SOURCE_EXPECTED_TAPE)
    source_models = read_csv(SOURCE_MODEL_HANDOFF)
    features = read_csv(SOURCE_FEATURE_MATRIX)
    variant_grid = read_csv(design.VARIANT_GRID_CONTRACT)
    s07_config = source_s07_config(source_attempts)
    source_model = source_s07_model(source_models)
    variants = variant_specs(s07_config, features)

    expected, expected_index = build_expected_tape(variants, source_expected, features)
    sync, models, attempts, sets, inis, tester = materialize_runtime_package(variants, source_model, features)
    packageability = build_packageability_matrix(variant_grid, variants)
    mapping = pd.DataFrame(
        [
            {
                "attempt_name": variant["attempt_name"],
                "source_design_variant": variant["source_design_variant"],
                "known_difference": variant["known_difference"],
                "package_short_name": variant["package_short_name"],
                "claim_boundary": CLAIM_BOUNDARY,
            }
            for variant in variants
        ]
    )
    parity = pd.DataFrame(
        [
            {
                "research_path": rel(design.VARIANT_GRID_CONTRACT),
                "runtime_path": rel(RUNTIME_PROBE_ATTEMPT_PACKAGE),
                "shared_contract": "same feature matrix, same s07 ONNX, explicit thresholds and side-filter params(같은 피처 행렬, 같은 s07 ONNX, 명시적 임계값/사이드 필터)",
                "known_differences": "single side-filter limit recorded in packageability matrix(단일 사이드 필터 한계는 포장 가능성 표에 기록)",
                "parity_check": "expected tape generated; MT5 tester pending run344O(예상 테이프 생성, MT5 테스터는 run344O 대기)",
                "runtime_claim_boundary": "runtime_probe_package_only(런타임 탐침 패키지 전용)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )
    queue = pd.DataFrame(
        [
            {
                "queue_id": f"{RUN_NUMBER}_{row['package_short_name']}",
                "attempt_name": row["attempt_name"],
                "next_run_id": NEXT_RUN_ID,
                "ini_path": row["ini_path"],
                "set_path": attempts.loc[attempts["attempt_name"].eq(row["attempt_name"]), "set_path"].iloc[0],
                "action": "execute MT5 Strategy Tester(MT5 전략 테스터 실행)",
                "effect": "collect runtime KPI and parity evidence(런타임 KPI와 동등성 근거 수집)",
                "must_not_claim": "runtime_authority(런타임 권위)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
            for _, row in inis.iterrows()
        ]
    )

    write_frame(EXPECTED_TAPE, expected)
    expected_index["path"] = rel(EXPECTED_TAPE)
    expected_index["sha256"] = sha256_file(EXPECTED_TAPE)
    write_frame(EXPECTED_TAPE_INDEX, expected_index)
    write_frame(PACKAGEABILITY_MATRIX, packageability)
    write_frame(VARIANT_RUNTIME_MAPPING, mapping)
    write_frame(RUNTIME_PROBE_ATTEMPT_PACKAGE, attempts)
    write_frame(MODEL_HANDOFF_MANIFEST, models)
    write_frame(COMMON_FILES_SYNC, sync)
    write_frame(TESTER_SET_MANIFEST, sets)
    write_frame(TESTER_INI_MANIFEST, inis)
    write_frame(TESTER_IDENTITY_CONTRACT, tester)
    write_frame(RUNTIME_PARITY_CONTRACT, parity)
    write_frame(RUN344O_QUEUE, queue)

    final: dict[str, Any] = {
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
        "parent_gate_passed": True,
        "packageability_rows": int(len(packageability)),
        "packageable_attempts": int(len(variants)),
        "attempt_rows": int(len(attempts)),
        "feature_rows": int(len(features)),
        "expected_rows": int(len(expected)),
        "model_rows": int(len(models)),
        "common_sync_rows": int(len(sync)),
        "common_sync_missing": int((~sync["exists"].astype(bool)).sum()),
        "set_rows": int(len(sets)),
        "ini_rows": int(len(inis)),
        "runtime_parity_contract_rows": int(len(parity)),
        "queue_rows": int(len(queue)),
        "candidate_selection": "not_run",
        "selected_model": "none(없음)",
        "mt5_execution": "not_run",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "goal_achieve": "not_claimed",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "external_verification_status": "pending_run344O_mt5_probe(run344O MT5 탐침 대기)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    gates = make_gates(final)
    final["gate_passes"] = int(gates["status"].astype(str).eq("passed").sum())
    final["gate_total"] = int(len(gates))
    write_frame(GATE_AUDIT, gates)
    write_json(FINAL_DECISION, final)
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "source_package_run_id": SOURCE_PACKAGE_RUN_ID,
            "created_at_utc": now_utc(),
            "execution_command": f"python -B {rel(Path(__file__))}",
            "inputs": [rel(path) for path in INPUT_FILES],
            "outputs": [rel(path) for path in OUTPUT_FILES],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_receipts(final)
    write_docs(final)
    write_registers(final, gates)
    write_lineage_receipt()
    update_artifact_registry([path for path in OUTPUT_FILES if path != ARTIFACT_REGISTRY])
    return final


def main() -> None:
    final = build_package()
    print(json.dumps(final, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
