from __future__ import annotations

import csv
import hashlib
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
from stage_pipelines.stage342 import (  # noqa: E402
    materialize_f01_session_long_firewall_mt5_probe_package_without_db as mt5_base,
)


TODAY = "2026-06-01"
STAGE_ID = "344_directional_long_quality__supply_surface_probe"
SOURCE_STAGE_ID = "343_quality_margin_runtime__early_long_mix_mt5_probe"

RUN_NUMBER = "run344C"
RUN_ID = "run344C_materialize_directional_long_supply_quality_surface_package_without_db_v1"
PARENT_RUN_ID = "run344B_design_directional_long_supply_quality_surface_without_db_v1"
NEXT_RUN_ID = "run344D_execute_directional_long_supply_quality_surface_mt5_probe_without_db_v1"
STATUS = "completed_stage344C_directional_long_quality_surface_package_materialized_no_selection"
JUDGMENT = "directional_long_quality_surface_package_ready_runtime_execution_required_no_selection"
DECISION = "stage344C_open_run344D_execute_directional_long_quality_surface_mt5_probe"
CLAIM_BOUNDARY = (
    "research_development_directional_long_quality_surface_runtime_probe_package_only_"
    "no_mt5_execution_no_candidate_selection_no_forward_no_live_readiness_no_operating_promotion_"
    "no_runtime_authority_no_goal_claim"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
SOURCE_STAGE_DIR = ROOT / "stages" / SOURCE_STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
MT5_DIR = RUN_DIR / "mt5"
SET_DIR = MT5_DIR / "sets"
INI_DIR = MT5_DIR / "inis"
MODEL_DIR = RUN_DIR / "models"
FEATURE_DIR = RUN_DIR / "features"
EXPECTED_DIR = RUN_DIR / "expected"

REPORT_PATH = REVIEW_DIR / "run344C_directional_long_quality_surface_package.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage344C_directional_long_quality_surface_package.md"
SELECTION_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
STAGE_README = STAGE_DIR / "README.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"
REVIEW_INDEX = REVIEW_DIR / "review_index.md"

PARENT_RUN_DIR = STAGE_DIR / "02_runs" / "run344B"
PARENT_FINAL_DECISION = PARENT_RUN_DIR / "final_decision.json"
PARENT_GATE_AUDIT = PARENT_RUN_DIR / "required_gate_coverage_audit.csv"
PARENT_QUEUE = PARENT_RUN_DIR / "run344C_materialization_queue.csv"
PARENT_PLAN = PARENT_RUN_DIR / "directional_long_quality_surface_plan.csv"
PARENT_LINEAGE = PARENT_RUN_DIR / "artifact_lineage_receipt.json"

SOURCE_PACKAGE_DIR = SOURCE_STAGE_DIR / "02_runs" / "run343D"
SOURCE_REVIEW_DIR = SOURCE_STAGE_DIR / "02_runs" / "run343F"
SOURCE_FEATURE_MATRIX = SOURCE_PACKAGE_DIR / "features" / "runtime_features.csv"
SOURCE_EXPECTED_TAPE = SOURCE_PACKAGE_DIR / "expected" / "expected_tape.csv"
SOURCE_ATTEMPT_PACKAGE = SOURCE_PACKAGE_DIR / "runtime_probe_attempt_package.csv"
SOURCE_MODEL_MANIFEST = SOURCE_PACKAGE_DIR / "model_handoff_manifest.csv"
SOURCE_PACKAGE_FINAL = SOURCE_PACKAGE_DIR / "final_decision.json"
SOURCE_REVIEW_FINAL = SOURCE_REVIEW_DIR / "final_decision.json"
SOURCE_REVIEW_SCORECARD = SOURCE_REVIEW_DIR / "trade_shape_rescue_review_scorecard.csv"
SOURCE_FAILURE_MEMORY = SOURCE_REVIEW_DIR / "failure_memory.csv"

DEFAULT_COMMON_FILES = mt5_base.DEFAULT_COMMON_FILES
DEFAULT_TERMINAL = mt5_base.DEFAULT_TERMINAL
DEFAULT_TESTER_PROFILE_ROOT = mt5_base.DEFAULT_TESTER_PROFILE_ROOT
DEFAULT_PORTABLE_ROOT = mt5_base.DEFAULT_PORTABLE_ROOT
EA_BINARY = mt5_base.EA_BINARY
PORTABLE_EA_EX5 = mt5_base.PORTABLE_EA_EX5

COMMON_ROOT = f"Project_Obsidian_Prime_v2/stage344/{RUN_NUMBER}_directional_long_quality_surface_probe"
COMMON_FEATURE_DIR = f"{COMMON_ROOT}/features"
COMMON_MODEL_DIR = f"{COMMON_ROOT}/models"
COMMON_TELEMETRY_DIR = f"{COMMON_ROOT}/telemetry"
EXPLORATION_LABEL = "stage344_DirectionalLongQualitySurface__RuntimeMappedONNX"
MAGIC_BASE = 3442000

FEATURE_MATRIX = FEATURE_DIR / "runtime_features.csv"
FEATURE_MATRIX_MANIFEST = RUN_DIR / "feature_matrix_manifest.csv"
EXPECTED_TAPE = EXPECTED_DIR / "expected_tape.csv"
EXPECTED_TAPE_INDEX = RUN_DIR / "expected_tape_index.csv"
VARIANT_PREVIEW = RUN_DIR / "variant_preview.csv"
RUNTIME_MAPPING_AUDIT = RUN_DIR / "runtime_mapping_audit.csv"
SIDE_FILTER_EXPECTED_AUDIT = RUN_DIR / "side_filter_expected_decision_audit.csv"
MODEL_HANDOFF_MANIFEST = RUN_DIR / "model_handoff_manifest.csv"
COMMON_FILES_SYNC = RUN_DIR / "common_files_sync.csv"
TESTER_SET_MANIFEST = RUN_DIR / "tester_set_manifest.csv"
TESTER_INI_MANIFEST = RUN_DIR / "tester_ini_manifest.csv"
RUNTIME_PROBE_ATTEMPT_PACKAGE = RUN_DIR / "runtime_probe_attempt_package.csv"
TESTER_IDENTITY_CONTRACT = RUN_DIR / "tester_identity_contract.csv"
PROXY_MT5_COMPARISON_CONTRACT = RUN_DIR / "proxy_mt5_comparison_contract.csv"
RUNTIME_PARITY_CONTRACT = RUN_DIR / "runtime_parity_contract.csv"
RUN344D_QUEUE = RUN_DIR / "run344D_queue.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
RUN_EVIDENCE_RECEIPT = RUN_DIR / "run_evidence_system_receipt.json"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment_design_receipt.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs" / "context" / "current_working_state.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
PROJECT_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
IDEA_REGISTRY = ROOT / "docs" / "registers" / "idea_registry.md"
ROOT_SELECTION_STATUS = ROOT / "docs" / "registers" / "selection_status.md"
ROOT_CHANGELOG = ROOT / "CHANGELOG.md"
WORKSPACE_CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"

STAGE_LEDGER_COLUMNS = [
    "stage_id",
    "run_id",
    "parent_run_id",
    "run_date",
    "status",
    "judgment",
    "decision",
    "next_run_id",
    "primary_artifact",
    "report_path",
    "gate_passes",
    "gate_total",
    "claim_boundary",
    "view",
    "tier",
    "metric_scope",
    "candidate_model_id",
    "net_profit",
    "profit_factor",
    "drawdown",
    "recovery_factor",
    "trade_count",
    "result_status",
    "sample_rows",
    "feature_count",
    "matched_rows",
    "expectancy",
    "attempt_count",
    "source_package_run_id",
    "ledger_row_id",
    "subrun_id",
    "record_view",
    "tier_scope",
    "kpi_scope",
    "scoreboard_lane",
    "path",
    "primary_kpi",
    "guardrail_kpi",
    "external_verification_status",
    "notes",
]


def now_utc() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def fs_path(path: Path) -> str:
    resolved = path.resolve()
    text = str(resolved)
    if os.name != "nt" or text.startswith("\\\\?\\") or len(text) < 240:
        return text
    if text.startswith("\\\\"):
        return "\\\\?\\UNC\\" + text[2:]
    return "\\\\?\\" + text


def rel(path: Path | str) -> str:
    candidate = Path(path)
    if not candidate.is_absolute():
        candidate = ROOT / candidate
    try:
        return candidate.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return candidate.as_posix()


def ensure_parent(path: Path) -> None:
    os.makedirs(fs_path(path.parent), exist_ok=True)


def path_exists(path: Path) -> bool:
    return os.path.exists(fs_path(path))


def path_is_file(path: Path) -> bool:
    return os.path.isfile(fs_path(path))


def required(path: Path) -> Path:
    if not path_is_file(path):
        raise FileNotFoundError(rel(path))
    return path


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with open(fs_path(path), "rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(fs_path(path), low_memory=False, encoding="utf-8-sig").fillna("")


def read_json(path: Path) -> dict[str, Any]:
    with open(fs_path(path), encoding="utf-8-sig") as handle:
        return json.load(handle)


def write_csv(path: Path, frame: pd.DataFrame) -> None:
    ensure_parent(path)
    with open(fs_path(path), "w", encoding="utf-8-sig", newline="") as handle:
        frame.to_csv(handle, index=False, lineterminator="\n", quoting=csv.QUOTE_MINIMAL)


def write_json(path: Path, payload: Mapping[str, Any]) -> None:
    ensure_parent(path)
    with open(fs_path(path), "w", encoding="utf-8", newline="\n") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")


def write_text(path: Path, text: str) -> None:
    ensure_parent(path)
    with open(fs_path(path), "w", encoding="utf-8-sig", newline="\n") as handle:
        handle.write(text.rstrip() + "\n")


def read_text(path: Path) -> str:
    with open(fs_path(path), encoding="utf-8-sig") as handle:
        return handle.read()


def append_text_once(path: Path, marker: str, text: str) -> None:
    current = read_text(path) if path_is_file(path) else ""
    if marker in current:
        return
    next_text = f"{current.rstrip()}\n\n{text.strip()}\n" if current.strip() else text.strip() + "\n"
    write_text(path, next_text)


def read_csv_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with open(fs_path(path), encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), [dict(row) for row in reader]


def write_csv_rows(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    rows_list = [dict(row) for row in rows]
    if fieldnames is None:
        keys: list[str] = []
        for row in rows_list:
            for key in row:
                if key not in keys:
                    keys.append(key)
        fieldnames = keys
    ensure_parent(path)
    with open(fs_path(path), "w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fieldnames), extrasaction="ignore")
        writer.writeheader()
        for row in rows_list:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def append_or_replace_csv(path: Path, key_columns: Sequence[str], rows: Iterable[Mapping[str, Any]]) -> None:
    rows_list = [dict(row) for row in rows]
    if path_is_file(path):
        fieldnames, existing = read_csv_rows(path)
    else:
        fieldnames, existing = [], []
    for row in rows_list:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    replacement_keys = {tuple(str(row.get(key, "")) for key in key_columns) for row in rows_list}
    kept = [
        row
        for row in existing
        if tuple(str(row.get(key, "")) for key in key_columns) not in replacement_keys
    ]
    write_csv_rows(path, kept + rows_list, fieldnames)


def numeric(value: Any, default: float = 0.0) -> float:
    try:
        if pd.isna(value) or value == "":
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def boolish(value: Any) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def copy_file(source: Path, target: Path, sync_id: str, effect: str) -> dict[str, Any]:
    ensure_parent(target)
    shutil.copy2(fs_path(source), fs_path(target))
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


def decide_label(
    p_short: float,
    p_flat: float,
    p_long: float,
    short_threshold: float,
    long_threshold: float,
    min_margin: float,
) -> str:
    short_margin = p_short - max(p_flat, p_long)
    long_margin = p_long - max(p_flat, p_short)
    short_ok = p_short >= short_threshold and short_margin >= min_margin
    long_ok = p_long >= long_threshold and long_margin >= min_margin
    if long_ok and (not short_ok or p_long >= p_short):
        return "long"
    if short_ok:
        return "short"
    return "flat"


def label_class(label: str) -> int:
    return {"short": 0, "flat": 1, "long": 2}[label]


def parse_range(text: Any) -> tuple[bool, float, float]:
    cleaned = str(text or "").strip()
    if not cleaned:
        return False, 0.0, 0.0
    low_text, high_text = [part.strip() for part in cleaned.split(",", 1)]
    low = float(low_text)
    high = float(high_text)
    if low > high:
        raise ValueError(f"invalid reversed range: {text}")
    return True, low, high


def load_context() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, dict[str, Any]]:
    parent = read_json(required(PARENT_FINAL_DECISION))
    parent_next = parent.get("next_run_id", parent.get("next_action"))
    if parent_next != RUN_ID:
        raise RuntimeError(f"parent next_run_id mismatch: {parent_next} != {RUN_ID}")
    parent_gates = read_csv(required(PARENT_GATE_AUDIT))
    if not parent_gates["status"].astype(str).str.lower().eq("passed").all():
        raise RuntimeError("run344B parent gate audit has failed rows")
    queue = read_csv(required(PARENT_QUEUE))
    plan = read_csv(required(PARENT_PLAN))
    source_package = read_csv(required(SOURCE_ATTEMPT_PACKAGE))
    source_expected = read_csv(required(SOURCE_EXPECTED_TAPE))
    return queue, plan, source_package, source_expected, parent


def source_config(attempt_name: str, source_package: pd.DataFrame) -> dict[str, Any]:
    matched = source_package.loc[source_package["attempt_name"].astype(str).eq(attempt_name)]
    if matched.empty:
        raise RuntimeError(f"missing source attempt config: {attempt_name}")
    row = matched.iloc[0]
    return {
        "attempt_name": attempt_name,
        "model_id": row.get("model_id", ""),
        "base_model_id": row.get("base_model_id", "logreg_balanced_c025"),
        "feature_set_id": row.get("feature_set_id", "run338D_training_feature_schema"),
        "feature_count": int(numeric(row.get("feature_count"), 0)),
        "feature_order_hash": str(row.get("feature_order_hash", "")),
        "model_local_path": str(row.get("model_local_path", "")),
        "short_threshold": numeric(row.get("short_threshold"), 0.0),
        "long_threshold": numeric(row.get("long_threshold"), 0.0),
        "min_margin": numeric(row.get("min_margin"), 0.0),
        "max_hold_bars": int(numeric(row.get("max_hold_bars"), 0)),
        "close_on_flat": boolish(row.get("close_on_flat")),
        "from_date": str(row.get("from_date", "2024.07.30")),
        "to_date": str(row.get("to_date", "2025.01.01")),
    }


def base_variant_defs() -> list[dict[str, Any]]:
    return [
        {
            "variant_id": "s01_anchor_short_supply_control",
            "priority": "P0",
            "source_attempt": "d01_h04_anchor45",
            "side_filter_feature_name": "minutes_from_cash_open",
            "block_long_range": "0,45",
            "role": "anchor_control(앵커 대조)",
            "runtime_mapping": "source anchor parameters unchanged(원천 앵커 파라미터 무변경)",
            "effect": "profit anchor(수익 앵커)의 short supply(숏 공급)를 대조군으로 보존한다.",
        },
        {
            "variant_id": "s02_shape_control_payoff_audit",
            "priority": "P0",
            "source_attempt": "d02_h02_shape_ctl",
            "role": "shape_control_payoff_audit(거래 형태 대조 손익 귀속)",
            "runtime_mapping": "source shape control parameters unchanged(원천 거래 형태 대조 파라미터 무변경)",
            "effect": "롱 공급을 가장 넓게 두고 payoff tax(손익 세금)를 귀속한다.",
        },
        {
            "variant_id": "s03_near_anchor_long_rescue_seed",
            "priority": "P0",
            "source_attempt": "d06_q04_m015_blk15",
            "side_filter_feature_name": "minutes_from_cash_open",
            "block_long_range": "0,15",
            "role": "near_anchor_long_rescue(앵커 근처 롱 복구)",
            "runtime_mapping": "source soft 0-15 minute long block retained(원천 0-15분 롱 차단 유지)",
            "effect": "수익 앵커와 롱 복구 사이의 작은 회복점을 확인한다.",
        },
        {
            "variant_id": "s04_long_quality_high_conf",
            "priority": "P0",
            "source_attempt": "d02_h02_shape_ctl",
            "long_keep_top_fraction": 0.35,
            "role": "long_quality_high_conf(고신뢰 롱 품질)",
            "runtime_mapping": "rank intent mapped to raised long_threshold(순위 의도를 상향 롱 임계값으로 매핑)",
            "effect": "강한 롱만 남겨 trade shape(거래 형태)가 살아나는지 본다.",
        },
        {
            "variant_id": "s05_long_quality_extreme_top20",
            "priority": "P1",
            "source_attempt": "d02_h02_shape_ctl",
            "long_keep_top_fraction": 0.20,
            "role": "long_quality_extreme_top20(롱 품질 극단 상위 20%)",
            "runtime_mapping": "extreme rank intent mapped to raised long_threshold(극단 순위 의도를 상향 롱 임계값으로 매핑)",
            "effect": "롱 품질 cliff(절벽)를 확인한다.",
        },
        {
            "variant_id": "s06_volatility_mid_long_only",
            "priority": "P1",
            "source_attempt": "d02_h02_shape_ctl",
            "side_filter_feature_name": "historical_vol_20",
            "block_long_quantile_range": (0.80, 1.00),
            "role": "volatility_mid_long_only(중간 변동성 롱 전용)",
            "runtime_mapping": "highest volatility long veto mapped to feature range side filter(최고 변동성 롱 거부를 피처 범위 사이드 필터로 매핑)",
            "effect": "shock long(충격 롱)을 줄인다.",
        },
        {
            "variant_id": "s07_trend_confirmed_long_only",
            "priority": "P1",
            "source_attempt": "d02_h02_shape_ctl",
            "side_filter_feature_name": "adx_14",
            "block_long_quantile_range": (0.00, 0.50),
            "role": "trend_confirmed_long_only(추세 확인 롱 전용)",
            "runtime_mapping": "trend confirmation mapped to low-ADX long veto(추세 확인을 낮은 ADX 롱 거부로 매핑)",
            "effect": "시장 구조 없는 롱을 줄인다.",
        },
        {
            "variant_id": "s08_cash_open_late_reentry",
            "priority": "P1",
            "source_attempt": "d01_h04_anchor45",
            "side_filter_feature_name": "minutes_from_cash_open",
            "block_long_range": "0,110",
            "role": "cash_open_late_reentry(현금장 후반 재진입)",
            "runtime_mapping": "late-only long intent mapped to 0-110 minute long block(후반 롱 의도를 0-110분 롱 차단으로 매핑)",
            "effect": "개장 충격 구간 롱을 더 강하게 제외한다.",
        },
        {
            "variant_id": "s09_exit_lifecycle_short_hold_longs",
            "priority": "P2",
            "source_attempt": "d02_h02_shape_ctl",
            "max_hold_bars_override": 6,
            "role": "exit_lifecycle_short_hold(청산 생명주기 짧은 보유)",
            "runtime_mapping": "long-only hold intent mapped to global max_hold_bars=6(롱 전용 보유 단축 의도를 전역 최대 보유 6봉으로 매핑)",
            "effect": "약한 롱 손실 꼬리를 줄이는지 본다.",
        },
        {
            "variant_id": "s10_exit_lifecycle_flat_recheck",
            "priority": "P2",
            "source_attempt": "d02_h02_shape_ctl",
            "close_on_flat_override": True,
            "role": "exit_lifecycle_flat_recheck(관망 청산 재확인)",
            "runtime_mapping": "long-only flat close intent mapped to global close_on_flat=true(롱 전용 관망 청산 의도를 전역 관망 청산 켜기로 매핑)",
            "effect": "flat signal(관망 신호) 청산 cliff(절벽)를 본다.",
        },
        {
            "variant_id": "s11_short_supply_protect_vol_filter",
            "priority": "P2",
            "source_attempt": "d01_h04_anchor45",
            "side_filter_feature_name": "historical_vol_20",
            "block_long_quantile_range": (0.80, 1.00),
            "role": "short_supply_protect_vol_filter(숏 공급 보호 변동성 필터)",
            "runtime_mapping": "short threshold unchanged; high-volatility long veto only(숏 임계값 무변경, 고변동성 롱 거부만 적용)",
            "effect": "q10 short-threshold tax(q10 숏 임계값 세금) 없이 변동성 롱만 줄인다.",
        },
        {
            "variant_id": "s12_no_entry_change_exit_only",
            "priority": "P2",
            "source_attempt": "d06_q04_m015_blk15",
            "side_filter_feature_name": "minutes_from_cash_open",
            "block_long_range": "0,15",
            "max_hold_bars_override": 6,
            "role": "no_entry_change_exit_only(진입 무변경 청산 전용)",
            "runtime_mapping": "entry gate unchanged from s03; exit hold shortened(진입 게이트는 s03과 같고 청산 보유만 단축)",
            "effect": "진입 효과와 청산 효과를 분리한다.",
        },
    ]


def resolve_variants(
    source_expected: pd.DataFrame,
    source_package: pd.DataFrame,
    features: pd.DataFrame,
    feature_columns: Sequence[str],
) -> list[dict[str, Any]]:
    resolved: list[dict[str, Any]] = []
    for row in base_variant_defs():
        config = source_config(str(row["source_attempt"]), source_package)
        variant = {**row}
        variant["short_threshold"] = config["short_threshold"]
        variant["long_threshold"] = config["long_threshold"]
        variant["min_margin"] = config["min_margin"]
        variant["max_hold_bars"] = int(row.get("max_hold_bars_override", config["max_hold_bars"]))
        variant["close_on_flat"] = bool(row.get("close_on_flat_override", config["close_on_flat"]))
        if "long_keep_top_fraction" in row:
            source = source_expected.loc[source_expected["attempt_name"].astype(str).eq(str(row["source_attempt"]))]
            long_scores = []
            for _, expected_row in source.iterrows():
                p_short = numeric(expected_row.get("p_short"))
                p_flat = numeric(expected_row.get("p_flat"))
                p_long = numeric(expected_row.get("p_long"))
                label = decide_label(
                    p_short,
                    p_flat,
                    p_long,
                    config["short_threshold"],
                    config["long_threshold"],
                    config["min_margin"],
                )
                if label == "long":
                    long_scores.append(p_long)
            keep_fraction = float(row["long_keep_top_fraction"])
            quantile = 1.0 - keep_fraction
            threshold = max(config["long_threshold"], float(pd.Series(long_scores).quantile(quantile))) if long_scores else config["long_threshold"]
            variant["long_threshold"] = round(threshold, 8)
            variant["runtime_mapping_value"] = f"keep_top_fraction={keep_fraction};derived_long_threshold={variant['long_threshold']}"
        feature_name = str(row.get("side_filter_feature_name", "")).strip()
        if feature_name:
            if feature_name not in feature_columns:
                raise RuntimeError(f"missing feature for variant {row['variant_id']}: {feature_name}")
            variant["side_filter_enabled"] = True
            variant["side_filter_feature_index"] = int(feature_columns.index(feature_name))
            if "block_long_quantile_range" in row:
                q_low, q_high = row["block_long_quantile_range"]
                series = pd.to_numeric(features[feature_name], errors="coerce").dropna()
                low = float(series.quantile(q_low))
                high = float(series.max() if q_high >= 1.0 else series.quantile(q_high))
                variant["block_long_range"] = f"{round(low, 8)},{round(high, 8)}"
                variant["runtime_mapping_value"] = f"{variant.get('runtime_mapping_value', '')};feature={feature_name};block_long_range={variant['block_long_range']}".strip(";")
        else:
            variant["side_filter_enabled"] = False
            variant["side_filter_feature_index"] = -1
            variant["block_long_range"] = ""
        variant["block_short_range"] = str(row.get("block_short_range", ""))
        variant["claim_boundary"] = CLAIM_BOUNDARY
        resolved.append(variant)
    return resolved


def source_model_path(attempt_name: str, source_package: pd.DataFrame) -> Path:
    config = source_config(attempt_name, source_package)
    local = str(config["model_local_path"]).strip()
    if not local:
        raise RuntimeError(f"missing source model path: {attempt_name}")
    return required(ROOT / local)


def materialize_feature_matrix(source_package: pd.DataFrame) -> tuple[str, int, int, str, list[str], int]:
    feature_common = f"{COMMON_FEATURE_DIR}/runtime_features.csv"
    copy_file(
        required(SOURCE_FEATURE_MATRIX),
        FEATURE_MATRIX,
        "local_feature_matrix",
        "feature matrix(피처 행렬)를 run344C 실행 폴더로 복사한다.",
    )
    common_target = DEFAULT_COMMON_FILES / Path(feature_common)
    copy_file(
        FEATURE_MATRIX,
        common_target,
        "common_feature_matrix",
        "feature matrix(피처 행렬)를 MT5 Common Files(MT5 공용 파일)로 복사한다.",
    )
    features = read_csv(FEATURE_MATRIX)
    feature_columns = [column for column in features.columns if column != "timestamp"]
    first = source_package.iloc[0]
    feature_count = int(numeric(first.get("feature_count"), len(feature_columns)))
    feature_hash = str(first.get("feature_order_hash", ""))
    duplicate_timestamps = int(features["timestamp"].duplicated().sum()) if "timestamp" in features.columns else -1
    write_csv(
        FEATURE_MATRIX_MANIFEST,
        pd.DataFrame(
            [
                {
                    "matrix_id": "run344C_runtime_features_reused_from_run343D",
                    "path": rel(FEATURE_MATRIX),
                    "common_path": feature_common,
                    "rows": int(len(features)),
                    "feature_count": feature_count,
                    "actual_feature_columns": len(feature_columns),
                    "feature_order_hash": feature_hash,
                    "duplicate_timestamps": duplicate_timestamps,
                    "sha256": sha256_file(FEATURE_MATRIX),
                    "source_path": rel(SOURCE_FEATURE_MATRIX),
                    "time_axis": "bar_time is M5 bar close timestamp(5분봉 종료 시각)",
                    "feature_label_boundary": "feature-only runtime replay; no label join(피처 전용 런타임 재생, 라벨 결합 없음)",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            ]
        ),
    )
    return feature_common, int(len(features)), feature_count, feature_hash, feature_columns, duplicate_timestamps


def build_expected_tape(
    variants: Sequence[Mapping[str, Any]],
    source_expected: pd.DataFrame,
    features: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    feature_lookup = features.set_index("timestamp", drop=False)
    expected_rows: list[dict[str, Any]] = []
    preview_rows: list[dict[str, Any]] = []
    audit_rows: list[dict[str, Any]] = []

    for variant in variants:
        attempt = str(variant["variant_id"])
        source_attempt = str(variant["source_attempt"])
        source = source_expected.loc[source_expected["attempt_name"].astype(str).eq(source_attempt)].copy()
        if source.empty:
            raise RuntimeError(f"source expected tape empty: {source_attempt}")
        labels: list[str] = []
        pre_labels: list[str] = []
        blocked_long = 0
        blocked_short = 0
        missing_feature_rows = 0
        feature_name = str(variant.get("side_filter_feature_name", ""))
        side_enabled = bool(variant.get("side_filter_enabled"))
        block_long_enabled, block_long_min, block_long_max = parse_range(variant.get("block_long_range", ""))
        block_short_enabled, block_short_min, block_short_max = parse_range(variant.get("block_short_range", ""))
        for _, row in source.iterrows():
            p_short = numeric(row.get("p_short"))
            p_flat = numeric(row.get("p_flat"))
            p_long = numeric(row.get("p_long"))
            pre_label = decide_label(
                p_short,
                p_flat,
                p_long,
                float(variant["short_threshold"]),
                float(variant["long_threshold"]),
                float(variant["min_margin"]),
            )
            label = pre_label
            side_applied = False
            side_reason = ""
            feature_value: float | str = ""
            bar_time = str(row.get("bar_time", ""))
            if side_enabled and pre_label != "flat" and feature_name:
                if bar_time in feature_lookup.index:
                    feature_value = numeric(feature_lookup.loc[bar_time, feature_name])
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
            pre_labels.append(pre_label)
            expected_rows.append(
                {
                    "attempt_name": attempt,
                    "model_id": f"logreg_balanced_c025_{attempt}",
                    "base_model_id": "logreg_balanced_c025",
                    "source_attempt_name": source_attempt,
                    "source_queue_id": row.get("source_queue_id", ""),
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
                    "side_filter_enabled": side_enabled,
                    "side_filter_feature_index": variant["side_filter_feature_index"],
                    "side_filter_feature_name": feature_name,
                    "side_filter_feature_value": feature_value,
                    "side_filter_applied": side_applied,
                    "side_filter_reason": side_reason,
                    "block_long_range_enabled": block_long_enabled,
                    "block_long_min": block_long_min,
                    "block_long_max": block_long_max,
                    "block_short_range_enabled": block_short_enabled,
                    "block_short_min": block_short_min,
                    "block_short_max": block_short_max,
                    "variant_role": variant["role"],
                    "runtime_mapping": variant["runtime_mapping"],
                    "runtime_mapping_value": variant.get("runtime_mapping_value", ""),
                    "allowed_use": "proxy-vs-MT5 runtime parity comparison(프록시-MT5 런타임 동등성 비교)",
                    "forbidden_use": "MT5 KPI substitute or operating selection(MT5 KPI 대체 또는 운영 선정)",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
        counts = pd.Series(labels).value_counts()
        pre_counts = pd.Series(pre_labels).value_counts()
        long_count = int(counts.get("long", 0))
        short_count = int(counts.get("short", 0))
        trade_count = long_count + short_count
        side_balance = min(long_count, short_count) / max(long_count, short_count) if max(long_count, short_count) else 0.0
        preview_rows.append(
            {
                "attempt_name": attempt,
                "source_attempt": source_attempt,
                "priority": variant["priority"],
                "variant_role": variant["role"],
                "signal_trade_count": trade_count,
                "signal_long_count": long_count,
                "signal_short_count": short_count,
                "signal_flat_count": int(counts.get("flat", 0)),
                "pre_filter_long_count": int(pre_counts.get("long", 0)),
                "pre_filter_short_count": int(pre_counts.get("short", 0)),
                "side_filter_blocked_long_count": blocked_long,
                "side_filter_blocked_short_count": blocked_short,
                "missing_feature_rows": missing_feature_rows,
                "signal_side_balance": round(side_balance, 8),
                "short_threshold": variant["short_threshold"],
                "long_threshold": variant["long_threshold"],
                "min_margin": variant["min_margin"],
                "max_hold_bars": variant["max_hold_bars"],
                "close_on_flat": variant["close_on_flat"],
                "side_filter_enabled": side_enabled,
                "side_filter_feature_index": variant["side_filter_feature_index"],
                "side_filter_feature_name": feature_name,
                "block_long_range": variant.get("block_long_range", ""),
                "block_short_range": variant.get("block_short_range", ""),
                "runtime_mapping": variant["runtime_mapping"],
                "runtime_mapping_value": variant.get("runtime_mapping_value", ""),
                "effect": variant["effect"],
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        audit_rows.append(
            {
                "attempt_name": attempt,
                "source_attempt": source_attempt,
                "side_filter_enabled": side_enabled,
                "feature_index": variant["side_filter_feature_index"],
                "feature_name": feature_name,
                "source_expected_rows": int(len(source)),
                "post_filter_rows": int(len(labels)),
                "blocked_long_count": blocked_long,
                "blocked_short_count": blocked_short,
                "missing_feature_rows": missing_feature_rows,
                "timestamp_safe": missing_feature_rows == 0,
                "effect": "feature row(피처 행)의 현재 시각 값만 사용해 side filter(사이드 필터)를 적용한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    expected = pd.DataFrame(expected_rows)
    preview = pd.DataFrame(preview_rows)
    audit = pd.DataFrame(audit_rows)
    write_csv(EXPECTED_TAPE, expected)
    write_csv(VARIANT_PREVIEW, preview)
    write_csv(SIDE_FILTER_EXPECTED_AUDIT, audit)
    write_csv(
        EXPECTED_TAPE_INDEX,
        pd.DataFrame(
            [
                {
                    "attempt_name": row["attempt_name"],
                    "model_id": f"logreg_balanced_c025_{row['attempt_name']}",
                    "row_count": int(len(expected.loc[expected["attempt_name"].eq(row["attempt_name"])])),
                    "path": rel(EXPECTED_TAPE),
                    "sha256": sha256_file(EXPECTED_TAPE),
                    "claim_boundary": CLAIM_BOUNDARY,
                }
                for _, row in preview.iterrows()
            ]
        ),
    )
    return expected, preview, audit


def materialize_attempts(
    variants: Sequence[Mapping[str, Any]],
    source_package: pd.DataFrame,
    feature_common: str,
    feature_count: int,
    feature_hash: str,
) -> dict[str, pd.DataFrame]:
    sync_rows: list[dict[str, Any]] = [
        {
            "sync_id": "common_feature_matrix",
            "source_path": rel(FEATURE_MATRIX),
            "target_path": (DEFAULT_COMMON_FILES / Path(feature_common)).as_posix(),
            "exists": path_is_file(DEFAULT_COMMON_FILES / Path(feature_common)),
            "sha256": sha256_file(DEFAULT_COMMON_FILES / Path(feature_common))
            if path_is_file(DEFAULT_COMMON_FILES / Path(feature_common))
            else "",
            "status": "synced(동기화됨)",
            "effect": "feature matrix(피처 행렬)를 MT5 Common Files(MT5 공용 파일)에 고정한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    model_rows: list[dict[str, Any]] = []
    set_rows: list[dict[str, Any]] = []
    ini_rows: list[dict[str, Any]] = []
    attempt_rows: list[dict[str, Any]] = []
    tester_rows: list[dict[str, Any]] = []
    proxy_rows: list[dict[str, Any]] = []
    runtime_rows: list[dict[str, Any]] = []
    mapping_rows: list[dict[str, Any]] = []

    for index, variant in enumerate(variants):
        attempt = str(variant["variant_id"])
        source_attempt = str(variant["source_attempt"])
        config = source_config(source_attempt, source_package)
        source_model = source_model_path(source_attempt, source_package)
        model_id = f"logreg_balanced_c025_{attempt}"
        magic = MAGIC_BASE + index + 1
        local_onnx = MODEL_DIR / f"{attempt}.onnx"
        common_onnx = f"{COMMON_MODEL_DIR}/{attempt}.onnx"
        sync_rows.append(copy_file(source_model, local_onnx, f"local_onnx::{attempt}", "ONNX(온엑스)를 변형 이름으로 복사한다."))
        sync_rows.append(copy_file(local_onnx, DEFAULT_COMMON_FILES / Path(common_onnx), f"common_onnx::{attempt}", "ONNX(온엑스)를 MT5 Common Files(MT5 공용 파일)로 복사한다."))

        side_enabled = bool(variant["side_filter_enabled"])
        feature_index = int(variant["side_filter_feature_index"])
        block_long_enabled, block_long_min, block_long_max = parse_range(variant.get("block_long_range", ""))
        block_short_enabled, block_short_min, block_short_max = parse_range(variant.get("block_short_range", ""))
        set_name = f"OPV2_{RUN_NUMBER}_{attempt}.set"
        ini_name = f"OPV2_{RUN_NUMBER}_{attempt}.ini"
        report_name = f"POPv2_{RUN_NUMBER}_{attempt}"
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
            "InpModelPath": common_onnx,
            "InpModelId": model_id,
            "InpModelBackend": "onnx",
            "InpModelUseCommonFiles": True,
            "InpModelUseCpuOnly": True,
            "InpModelNoConversion": False,
            "InpSetOutputShape": True,
            "InpFeatureOrderHash": feature_hash,
            "InpFallbackEnabled": False,
            "InpShortThreshold": variant["short_threshold"],
            "InpLongThreshold": variant["long_threshold"],
            "InpMinMargin": variant["min_margin"],
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
            "InpFixedLot": 0.10,
            "InpMagic": magic,
            "InpDeviationPoints": 20,
            "InpCloseOnFlatSignal": bool(variant["close_on_flat"]),
            "InpReverseOnOppositeSignal": True,
            "InpCloseOnlyOnOppositeSignal": False,
            "InpMaxHoldBars": int(variant["max_hold_bars"]),
            "InpMaxConcurrentPositions": 1,
            "InpReentryCooldownBars": 0,
            "InpSameDirectionReentryCooldownBars": 0,
            "InpEntryTransitionOnly": False,
            "InpExitRiskOverlayEnabled": False,
            "InpAtrSltpEnabled": False,
            "InpModelRiskSizingEnabled": False,
            "InpTelemetryEnabled": True,
            "InpTelemetryUseCommonFiles": True,
            "InpTelemetryCsvPath": f"{COMMON_TELEMETRY_DIR}/{attempt}_telemetry.csv",
            "InpSummaryCsvPath": f"{COMMON_TELEMETRY_DIR}/{attempt}_summary.csv",
        }
        set_payload = mt5.materialize_tester_set_file(set_values, set_path, generated_by=rel(Path(__file__)))
        ini_payload = mt5.materialize_tester_ini_file(
            mt5.TesterMaterializationConfig(
                shutdown_terminal=1,
                from_date=config["from_date"],
                to_date=config["to_date"],
                report=report_name,
            ),
            ini_path,
            set_file_path=Path(set_name),
        )
        tester = ini_payload["tester"]
        model_rows.append(
            {
                "attempt_name": attempt,
                "model_id": model_id,
                "source_attempt": source_attempt,
                "source_model_id": config["model_id"],
                "source_onnx_path": rel(source_model),
                "source_onnx_sha256": sha256_file(source_model),
                "local_onnx_path": rel(local_onnx),
                "local_onnx_sha256": sha256_file(local_onnx),
                "common_onnx_path": common_onnx,
                "common_onnx_sha256": sha256_file(DEFAULT_COMMON_FILES / Path(common_onnx)),
                "feature_order_hash": feature_hash,
                "handoff_status": "ready_for_mt5_probe(MT5 탐침 준비)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        set_rows.append(
            {
                "attempt_name": attempt,
                "source_attempt": source_attempt,
                "model_id": model_id,
                "variant_role": variant["role"],
                "set_path": rel(set_path),
                "set_sha256": set_payload["sha256"],
                "short_threshold": variant["short_threshold"],
                "long_threshold": variant["long_threshold"],
                "min_margin": variant["min_margin"],
                "max_hold_bars": variant["max_hold_bars"],
                "close_on_flat": variant["close_on_flat"],
                "side_filter_enabled": side_enabled,
                "side_filter_feature_index": feature_index,
                "side_filter_feature_name": variant.get("side_filter_feature_name", ""),
                "block_long_range_enabled": side_enabled and block_long_enabled,
                "block_long_min": block_long_min,
                "block_long_max": block_long_max,
                "block_short_range_enabled": side_enabled and block_short_enabled,
                "block_short_min": block_short_min,
                "block_short_max": block_short_max,
                "magic": magic,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        ini_rows.append(
            {
                "attempt_name": attempt,
                "model_id": model_id,
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
                "queue_id": f"run344C_{attempt}",
                "next_run_id": NEXT_RUN_ID,
                "probe_priority": index + 1,
                "tier": "Tier A",
                "split": "inner_holdout_runtime_collapsed_probe",
                "model_id": model_id,
                "base_model_id": config["base_model_id"],
                "source_attempt": source_attempt,
                "feature_set_id": config["feature_set_id"],
                "feature_count": feature_count,
                "feature_order_hash": feature_hash,
                "feature_local_path": rel(FEATURE_MATRIX),
                "feature_common_path": feature_common,
                "model_local_path": rel(local_onnx),
                "model_common_path": common_onnx,
                "expected_tape_path": rel(EXPECTED_TAPE),
                "common_telemetry_path": f"{COMMON_TELEMETRY_DIR}/{attempt}_telemetry.csv",
                "common_summary_path": f"{COMMON_TELEMETRY_DIR}/{attempt}_summary.csv",
                "set_path": rel(set_path),
                "set_name": set_name,
                "ini_path": rel(ini_path),
                "ini_name": ini_name,
                "report_name": report_name,
                "from_date": config["from_date"],
                "to_date": config["to_date"],
                "decision_mode": "threshold_margin",
                "short_threshold": variant["short_threshold"],
                "long_threshold": variant["long_threshold"],
                "min_margin": variant["min_margin"],
                "fixed_lot": 0.10,
                "max_hold_bars": variant["max_hold_bars"],
                "close_on_flat": variant["close_on_flat"],
                "side_filter_enabled": side_enabled,
                "side_filter_feature_index": feature_index,
                "block_long_range": variant.get("block_long_range", ""),
                "block_short_range": variant.get("block_short_range", ""),
                "variant_role": variant["role"],
                "runtime_mapping": variant["runtime_mapping"],
                "effect": variant["effect"],
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        tester_rows.append(
            {
                "contract_id": f"tester_identity::{attempt}",
                "attempt_name": attempt,
                "terminal_path": DEFAULT_TERMINAL.as_posix(),
                "tester_profile_root": DEFAULT_TESTER_PROFILE_ROOT.as_posix(),
                "portable_root": DEFAULT_PORTABLE_ROOT.as_posix(),
                "expert": tester.get("Expert", ""),
                "symbol": tester.get("Symbol", ""),
                "period": tester.get("Period", ""),
                "from_date": tester.get("FromDate", ""),
                "to_date": tester.get("ToDate", ""),
                "report": tester.get("Report", ""),
                "ea_binary": EA_BINARY.as_posix(),
                "portable_ea_ex5": PORTABLE_EA_EX5.as_posix(),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        proxy_rows.append(
            {
                "contract_id": f"proxy_mt5_comparison::{attempt}",
                "attempt_name": attempt,
                "expected_tape": rel(EXPECTED_TAPE),
                "runtime_telemetry_expected": f"{COMMON_TELEMETRY_DIR}/{attempt}_telemetry.csv",
                "must_compare": "feature_input_hash, probabilities, mapped decision, trade KPI(피처 해시, 확률, 매핑 결정, 거래 KPI)",
                "known_difference": variant["runtime_mapping"],
                "forbidden_use": "replace MT5 KPI(MT5 KPI 대체)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        runtime_rows.append(
            {
                "contract_id": f"runtime_parity::{attempt}",
                "attempt_name": attempt,
                "runtime_path": rel(set_path),
                "shared_contract": (
                    f"features={feature_count};feature_hash={feature_hash};short={variant['short_threshold']};"
                    f"long={variant['long_threshold']};min_margin={variant['min_margin']};hold={variant['max_hold_bars']};"
                    f"close_flat={variant['close_on_flat']};side_filter={side_enabled};feature_index={feature_index};"
                    f"block_long={side_enabled and block_long_enabled}:{block_long_min}:{block_long_max};"
                    f"block_short={side_enabled and block_short_enabled}:{block_short_min}:{block_short_max}"
                ),
                "parity_check": f"{NEXT_RUN_ID} telemetry-vs-expected tape(다음 실행 기록 대 예상 테이프)",
                "runtime_claim_boundary": "runtime_probe_package_only(런타임 탐침 패키지 전용)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        mapping_rows.append(
            {
                "attempt_name": attempt,
                "source_attempt": source_attempt,
                "design_intent": variant["role"],
                "runtime_mapping": variant["runtime_mapping"],
                "runtime_mapping_value": variant.get("runtime_mapping_value", ""),
                "known_difference": "package uses EA-supported thresholds, feature-range side filters, global hold/flat controls(EA 지원 임계값, 피처 범위 필터, 전역 보유/관망 청산 사용)",
                "usability": "usable_for_runtime_probe(런타임 탐침 사용 가능)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    queue_out = pd.DataFrame(
        [
            {
                "queue_id": f"{NEXT_RUN_ID}_queue",
                "next_run_id": NEXT_RUN_ID,
                "priority": "P0",
                "attempt_count": len(variants),
                "attempt_package": rel(RUNTIME_PROBE_ATTEMPT_PACKAGE),
                "required_outputs": "runtime telemetry, tester reports, proxy-MT5 diff(런타임 기록, 테스터 보고서, 프록시-MT5 차이)",
                "effect": "run344C package(344C 패키지)를 MT5 runtime probe(MT5 런타임 탐침)로 넘긴다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )
    tables = {
        "sync": pd.DataFrame(sync_rows),
        "model": pd.DataFrame(model_rows),
        "set": pd.DataFrame(set_rows),
        "ini": pd.DataFrame(ini_rows),
        "attempts": pd.DataFrame(attempt_rows),
        "tester": pd.DataFrame(tester_rows),
        "proxy": pd.DataFrame(proxy_rows),
        "runtime": pd.DataFrame(runtime_rows),
        "mapping": pd.DataFrame(mapping_rows),
        "queue": queue_out,
    }
    for path, frame in [
        (COMMON_FILES_SYNC, tables["sync"]),
        (MODEL_HANDOFF_MANIFEST, tables["model"]),
        (TESTER_SET_MANIFEST, tables["set"]),
        (TESTER_INI_MANIFEST, tables["ini"]),
        (RUNTIME_PROBE_ATTEMPT_PACKAGE, tables["attempts"]),
        (TESTER_IDENTITY_CONTRACT, tables["tester"]),
        (PROXY_MT5_COMPARISON_CONTRACT, tables["proxy"]),
        (RUNTIME_PARITY_CONTRACT, tables["runtime"]),
        (RUNTIME_MAPPING_AUDIT, tables["mapping"]),
        (RUN344D_QUEUE, tables["queue"]),
    ]:
        write_csv(path, frame)
    return tables


def output_paths() -> list[Path]:
    return [
        FEATURE_MATRIX,
        FEATURE_MATRIX_MANIFEST,
        EXPECTED_TAPE,
        EXPECTED_TAPE_INDEX,
        VARIANT_PREVIEW,
        RUNTIME_MAPPING_AUDIT,
        SIDE_FILTER_EXPECTED_AUDIT,
        MODEL_HANDOFF_MANIFEST,
        COMMON_FILES_SYNC,
        TESTER_SET_MANIFEST,
        TESTER_INI_MANIFEST,
        RUNTIME_PROBE_ATTEMPT_PACKAGE,
        TESTER_IDENTITY_CONTRACT,
        PROXY_MT5_COMPARISON_CONTRACT,
        RUNTIME_PARITY_CONTRACT,
        RUN344D_QUEUE,
        WORK_PACKET,
        RUN_EVIDENCE_RECEIPT,
        EXPERIMENT_RECEIPT,
        DATA_RECEIPT,
        MODEL_RECEIPT,
        RUNTIME_RECEIPT,
        LINEAGE_RECEIPT,
        CLAIM_RECEIPT,
        GATE_AUDIT,
        FINAL_DECISION,
        RUN_MANIFEST,
        REPORT_PATH,
        DECISION_DOC,
        SELECTION_STATUS,
        ROOT_SELECTION_STATUS,
        STAGE_LEDGER,
        REVIEW_INDEX,
        WORKSPACE_STATE,
        CURRENT_WORKING_STATE,
        RUN_REGISTRY,
        PROJECT_LEDGER,
        ARTIFACT_REGISTRY,
        Path(__file__),
    ]


def build_summary(
    variants: Sequence[Mapping[str, Any]],
    feature_rows: int,
    feature_count: int,
    feature_hash: str,
    duplicate_timestamps: int,
    expected: pd.DataFrame,
    preview: pd.DataFrame,
    audit: pd.DataFrame,
    tables: Mapping[str, pd.DataFrame],
) -> dict[str, Any]:
    return {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_run_id": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
        "attempt_count": int(len(variants)),
        "feature_rows": int(feature_rows),
        "feature_count": int(feature_count),
        "feature_order_hash": feature_hash,
        "duplicate_timestamps": int(duplicate_timestamps),
        "expected_rows": int(len(expected)),
        "side_filter_attempt_count": int(preview["side_filter_enabled"].astype(bool).sum()),
        "side_filter_blocked_long_rows": int(audit["blocked_long_count"].sum()),
        "side_filter_blocked_short_rows": int(audit["blocked_short_count"].sum()),
        "side_filter_missing_feature_rows": int(audit["missing_feature_rows"].sum()),
        "preview_max_signal_trade_count": int(preview["signal_trade_count"].max()) if not preview.empty else 0,
        "preview_min_signal_trade_count": int(preview["signal_trade_count"].min()) if not preview.empty else 0,
        "preview_best_signal_side_balance": float(preview["signal_side_balance"].max()) if not preview.empty else 0.0,
        "common_sync_missing": int((~tables["sync"]["exists"].astype(bool)).sum()),
        "set_rows": int(len(tables["set"])),
        "ini_rows": int(len(tables["ini"])),
        "terminal_exists": path_is_file(DEFAULT_TERMINAL),
        "common_files_exists": path_exists(DEFAULT_COMMON_FILES),
        "ea_binary_exists": path_is_file(EA_BINARY),
        "portable_ea_exists": path_is_file(PORTABLE_EA_EX5),
        "candidate_selection": "not_run",
        "model_training": "not_run",
        "mt5_execution": "not_run",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
    }


def write_contracts_and_receipts(summary: Mapping[str, Any]) -> None:
    write_json(
        WORK_PACKET,
        {
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "primary_family": "experiment_execution(실험 실행)",
            "primary_skill": "obsidian-run-evidence-system(실행 근거 시스템)",
            "support_skills": [
                "obsidian-experiment-design(실험 설계)",
                "obsidian-data-integrity(데이터 무결성)",
                "obsidian-model-validation(모델 검증)",
                "obsidian-runtime-parity(런타임 동등성)",
                "obsidian-artifact-lineage(산출물 계보)",
            ],
            "required_gates": [
                "scope_completion_gate",
                "kpi_contract_audit",
                "skill_receipt_lint",
                "required_gate_coverage_audit",
            ],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    base = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "created_at_utc": now_utc(),
        "status": STATUS,
        "judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(RUN_EVIDENCE_RECEIPT, {**base, "evidence_type": "runtime_probe_package_materialization(런타임 탐침 패키지 물질화)", "kpi_boundary": "MT5 KPI not measured in this run(이번 실행에서 MT5 KPI 미측정)"})
    write_json(EXPERIMENT_RECEIPT, {**base, "hypothesis": "directional long quality surface can recover long supply without losing the short profit anchor(방향성 롱 품질 표면이 숏 수익 앵커를 잃지 않고 롱 공급을 회복할 수 있다)", "broad_sweep": "12 runtime-mapped variants(런타임 매핑 변형 12개)"})
    write_json(DATA_RECEIPT, {**base, "data_source": [rel(SOURCE_FEATURE_MATRIX), rel(SOURCE_EXPECTED_TAPE)], "time_axis": "M5 bar close timestamp(5분봉 종료 시각)", "feature_label_boundary": "no new labels and no future joins(새 라벨 없음, 미래 결합 없음)", "integrity_judgment": "usable_with_boundary(경계 있는 사용 가능)"})
    write_json(MODEL_RECEIPT, {**base, "model_family": "existing logreg ONNX reused(기존 로지스틱 온엑스 재사용)", "model_training": "not_run(미실행)", "validation_judgment": "runtime_package_only(런타임 패키지 전용)"})
    write_json(RUNTIME_RECEIPT, {**base, "research_path": rel(Path(__file__)), "runtime_path": rel(RUNTIME_PROBE_ATTEMPT_PACKAGE), "shared_contract": rel(RUNTIME_PARITY_CONTRACT), "parity_check": f"{NEXT_RUN_ID} telemetry-vs-expected required(다음 실행에서 기록 대 예상 비교 필요)", "runtime_claim_boundary": "runtime_probe_package_only(런타임 탐침 패키지 전용)"})
    write_json(CLAIM_RECEIPT, {**base, "allowed_claim": "package ready for MT5 runtime probe(MT5 런타임 탐침 패키지 준비)", "forbidden_claims": ["MT5 KPI", "candidate_selection(후보 선정)", "operating_promotion(운영 승격)", "runtime_authority(런타임 권위)", "Goal_Achieve(목표 달성)"]})


def write_lineage_receipt() -> None:
    source_inputs = [
        PARENT_FINAL_DECISION,
        PARENT_GATE_AUDIT,
        PARENT_QUEUE,
        PARENT_PLAN,
        PARENT_LINEAGE,
        SOURCE_FEATURE_MATRIX,
        SOURCE_EXPECTED_TAPE,
        SOURCE_ATTEMPT_PACKAGE,
        SOURCE_MODEL_MANIFEST,
        SOURCE_PACKAGE_FINAL,
        SOURCE_REVIEW_FINAL,
        SOURCE_REVIEW_SCORECARD,
        SOURCE_FAILURE_MEMORY,
    ]
    artifacts = [path for path in output_paths() if path_is_file(path) and path != LINEAGE_RECEIPT]
    write_json(
        LINEAGE_RECEIPT,
        {
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "parent_run_id": PARENT_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "created_at_utc": now_utc(),
            "source_inputs": [
                {"path": rel(path), "sha256": sha256_file(path), "availability": "tracked"}
                for path in source_inputs
                if path_is_file(path)
            ],
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [rel(path) for path in artifacts],
            "artifact_hashes": {rel(path): sha256_file(path) for path in artifacts},
            "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "availability": "tracked_and_common_files_synced(추적 및 공용 파일 동기화)",
            "lineage_judgment": "connected_with_boundary(경계 있는 연결)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def gate_row(gate_id: str, status: bool, evidence_path: str, effect: str) -> dict[str, Any]:
    return {
        "gate_id": gate_id,
        "status": "passed" if status else "failed",
        "evidence_path": evidence_path,
        "effect": effect,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def build_gates(summary: Mapping[str, Any]) -> list[dict[str, Any]]:
    parent_gates = read_csv(required(PARENT_GATE_AUDIT))
    no_forbidden = (
        summary["candidate_selection"] == "not_run"
        and summary["runtime_authority"] == "not_claimed"
        and summary["operating_promotion"] == "not_claimed"
        and summary["goal_achieve"] == "not_claimed"
        and summary["mt5_execution"] == "not_run"
    )
    receipts = [
        RUN_EVIDENCE_RECEIPT,
        EXPERIMENT_RECEIPT,
        DATA_RECEIPT,
        MODEL_RECEIPT,
        RUNTIME_RECEIPT,
        LINEAGE_RECEIPT,
        CLAIM_RECEIPT,
    ]
    return [
        gate_row("parent_run344B_gates_passed", bool(parent_gates["status"].astype(str).str.lower().eq("passed").all()), rel(PARENT_GATE_AUDIT), "run344B(344B 실행)의 설계 gate(게이트)를 이어받는다."),
        gate_row("source_runtime_package_available", all(path_is_file(path) for path in [SOURCE_FEATURE_MATRIX, SOURCE_EXPECTED_TAPE, SOURCE_ATTEMPT_PACKAGE]), f"{rel(SOURCE_FEATURE_MATRIX)};{rel(SOURCE_EXPECTED_TAPE)};{rel(SOURCE_ATTEMPT_PACKAGE)}", "run343D(343D 실행)의 런타임 패키지를 재사용한다."),
        gate_row("scope_completion_gate", summary["attempt_count"] == 12 and summary["set_rows"] == 12 and summary["ini_rows"] == 12 and path_is_file(RUNTIME_PROBE_ATTEMPT_PACKAGE), rel(RUNTIME_PROBE_ATTEMPT_PACKAGE), "12개 변형을 모두 package(패키지)로 물질화한다."),
        gate_row("feature_matrix_reused_timestamp_safe", path_is_file(FEATURE_MATRIX) and summary["feature_rows"] > 0 and summary["duplicate_timestamps"] == 0, rel(FEATURE_MATRIX_MANIFEST), "피처를 새로 만들지 않고 timestamp-safe(시점 안전) 재사용으로 고정한다."),
        gate_row("expected_tape_materialized", summary["expected_rows"] == summary["feature_rows"] * summary["attempt_count"] and path_is_file(EXPECTED_TAPE), rel(EXPECTED_TAPE), "expected tape(예상 테이프)에 runtime mapping(런타임 매핑)을 반영한다."),
        gate_row("runtime_mapping_audit_written", path_is_file(RUNTIME_MAPPING_AUDIT), rel(RUNTIME_MAPPING_AUDIT), "설계 의도와 EA 지원 매핑 차이를 기록한다."),
        gate_row("common_files_synced", summary["common_sync_missing"] == 0, rel(COMMON_FILES_SYNC), "MT5 Common Files(MT5 공용 파일) 인계를 확인한다."),
        gate_row("tester_set_ini_materialized", summary["set_rows"] == summary["attempt_count"] and summary["ini_rows"] == summary["attempt_count"], rel(TESTER_SET_MANIFEST), "tester set/ini(테스터 설정 파일)를 만든다."),
        gate_row("runtime_parity_contract_written", path_is_file(RUNTIME_PARITY_CONTRACT) and path_is_file(PROXY_MT5_COMPARISON_CONTRACT), rel(RUNTIME_PARITY_CONTRACT), "runtime parity(런타임 동등성) 비교 계약을 남긴다."),
        gate_row("tester_identity_visible", summary["terminal_exists"] and summary["common_files_exists"] and summary["ea_binary_exists"] and summary["portable_ea_exists"], rel(TESTER_IDENTITY_CONTRACT), "MT5 실행 가시성을 기록한다."),
        gate_row("run344D_queue_opened", path_is_file(RUN344D_QUEUE), rel(RUN344D_QUEUE), "다음 MT5 runtime probe(런타임 탐침) queue(대기열)를 연다."),
        gate_row("kpi_contract_audit", path_is_file(PROXY_MT5_COMPARISON_CONTRACT), rel(PROXY_MT5_COMPARISON_CONTRACT), "proxy(프록시)가 MT5 KPI를 대체하지 못하도록 경계를 적는다."),
        gate_row("skill_receipt_lint", all(path_is_file(path) for path in receipts), ";".join(rel(path) for path in receipts), "필수 skill receipt(스킬 영수증)를 모두 남긴다."),
        gate_row("artifact_lineage_audit", path_is_file(LINEAGE_RECEIPT), rel(LINEAGE_RECEIPT), "source inputs(원천 입력)와 package artifacts(패키지 산출물)를 연결한다."),
        gate_row("no_forbidden_selection_or_goal_claim", no_forbidden, rel(CLAIM_RECEIPT), "패키지를 selection(선정)이나 Goal Achieve(목표 달성)로 주장하지 않는다."),
        gate_row("required_gate_coverage_audit", True, rel(GATE_AUDIT), "required gate coverage audit(필수 게이트 커버리지 감사)를 기록한다."),
    ]


def write_docs(summary: Mapping[str, Any]) -> None:
    report = f"""# run344C Directional Long Quality Surface Package(344C 방향성 롱 품질 표면 패키지)

## Summary(요약)

- run_id(실행 ID): `{RUN_ID}`
- parent_run(부모 실행): `{PARENT_RUN_ID}`
- next_run(다음 실행): `{NEXT_RUN_ID}`
- attempts(시도): `{summary['attempt_count']}`
- feature_rows(피처 행): `{summary['feature_rows']}`
- expected_rows(예상 행): `{summary['expected_rows']}`
- side_filter_attempts(사이드 필터 시도): `{summary['side_filter_attempt_count']}`
- preview_max_signal_trade_count(미리보기 최대 신호 거래수): `{summary['preview_max_signal_trade_count']}`
- preview_best_signal_side_balance(미리보기 최고 방향 균형): `{summary['preview_best_signal_side_balance']}`

## Action(행동)

run344B(344B 실행)의 12개 directional long quality surface(방향성 롱 품질 표면) 설계를 MT5 Strategy Tester(MT5 전략 테스터)가 읽을 수 있는 `.set/.ini`, ONNX(온엑스), feature matrix(피처 행렬), expected tape(예상 테이프), run344D queue(344D 대기열)로 물질화했다.

## Effect(효과)

rank intent(순위 의도), regime veto(국면 거부), exit lifecycle(청산 생명주기)을 EA-supported runtime mapping(EA 지원 런타임 매핑)으로 바꿔서 실제 MT5 runtime probe(MT5 런타임 탐침)로 넘길 수 있다.

## Boundary(경계)

Package only(패키지 전용). No MT5 execution(MT5 실행 없음), no selected model(선정 모델 없음), no operating promotion(운영 승격 없음), no runtime authority(런타임 권위 없음), no Goal Achieve(목표 달성 없음).
"""
    decision = f"""# {TODAY} Stage344C Directional Long Quality Surface Package Decision(344C 방향성 롱 품질 표면 패키지 결정)

- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- package(패키지): `{rel(RUNTIME_PROBE_ATTEMPT_PACKAGE)}`
- queue(대기열): `{rel(RUN344D_QUEUE)}`
- next_run(다음 실행): `{NEXT_RUN_ID}`

Action(행동): 12개 runtime-mapped variant(런타임 매핑 변형)를 MT5 probe package(MT5 탐침 패키지)로 만들었다.
Effect(효과): 다음 작업에서 Strategy Tester(전략 테스터) 실행과 proxy-MT5 diff(프록시-MT5 차이) 검증으로 바로 이어갈 수 있다.

claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    selection = f"""# Stage 344 Selection Status(344단계 선정 상태)

- active_stage(현재 단계): `{STAGE_ID}`
- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- selected_model(선정 모델): `none(없음)`
- packaged_attempts(패키지 시도): `{summary['attempt_count']}`
- next_probe(다음 탐침): `directional_long_quality_surface_mt5_runtime_probe(방향성 롱 품질 표면 MT5 런타임 탐침)`
- runtime_authority(런타임 권위): `not_claimed(주장 없음)`
- operating_promotion(운영 승격): `not_claimed(주장 없음)`
- Goal Achieve(목표 달성): `not_claimed(주장 없음)`

Effect(효과): Stage344(344단계)는 설계에서 MT5 실행 대기 상태로 이동했다.
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

run344C(344C 실행)는 directional long quality surface(방향성 롱 품질 표면)를 runtime package(런타임 패키지)로 물질화했다. run344D(344D 실행)는 이 패키지를 MT5 runtime probe(MT5 런타임 탐침)로 실행해야 한다.

## Claim Boundary(주장 경계)

`{CLAIM_BOUNDARY}`
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
    write_text(SELECTION_STATUS, selection)
    write_text(ROOT_SELECTION_STATUS, selection)
    write_text(CURRENT_WORKING_STATE, current)
    write_text(WORKSPACE_STATE, workspace)
    append_text_once(STAGE_BRIEF, RUN_ID, f"""## run344C Directional Long Quality Surface Package(344C 방향성 롱 품질 표면 패키지)

- run_id(실행 ID): `{RUN_ID}`
- attempts(시도): `{summary['attempt_count']}`
- next(다음): `{NEXT_RUN_ID}`
- effect(효과): 설계된 long quality surface(롱 품질 표면)를 MT5 runtime probe(MT5 런타임 탐침) 실행 대기열로 바꿨다.
""")
    append_text_once(STAGE_README, RUN_ID, f"""## run344C Directional Long Quality Surface Package(344C 방향성 롱 품질 표면 패키지)

- package(패키지): `{rel(RUNTIME_PROBE_ATTEMPT_PACKAGE)}`
- queue(대기열): `{rel(RUN344D_QUEUE)}`
- effect(효과): Stage344(344단계)가 MT5 실행 단계로 넘어갈 준비를 마쳤다.
""")
    append_text_once(REVIEW_INDEX, RUN_ID, f"- run344C package(344C 패키지): `{rel(REPORT_PATH)}`")
    changelog = f"""## {TODAY} run344C Directional Long Quality Surface Package(방향성 롱 품질 표면 패키지)

- action(행동): 12개 runtime-mapped variant(런타임 매핑 변형)를 MT5 package(MT5 패키지)로 만들었다.
- effect(효과): run344D(344D 실행)가 Strategy Tester(전략 테스터)에서 실제 KPI(핵심 성과 지표)를 검증할 수 있다.
- boundary(경계): package only(패키지 전용), no MT5 execution(MT5 실행 없음), no selection(선정 없음), no runtime authority(런타임 권위 없음).
"""
    append_text_once(ROOT_CHANGELOG, RUN_ID, changelog)
    append_text_once(WORKSPACE_CHANGELOG, RUN_ID, changelog)
    append_text_once(IDEA_REGISTRY, RUN_ID, f"""## {TODAY} {RUN_ID} Directional Long Quality Runtime Mapping(방향성 롱 품질 런타임 매핑)

- idea_id(아이디어 ID): `stage344_directional_long_quality_surface`
- action(행동): rank/regime/exit ideas(순위/국면/청산 아이디어)를 EA-supported runtime mapping(EA 지원 런타임 매핑)으로 만들었다.
- effect(효과): MT5 runtime probe(MT5 런타임 탐침)에서 실행 가능한 candidate surface(후보 표면)가 생겼다.
- next_run(다음 실행): `{NEXT_RUN_ID}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
""")


def write_final_and_manifest(summary: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    final = {
        **dict(summary),
        "gate_passes": sum(1 for gate in gates if gate["status"] == "passed"),
        "gate_total": len(gates),
        "created_at_utc": now_utc(),
    }
    write_json(FINAL_DECISION, final)
    write_json(
        RUN_MANIFEST,
        {
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "parent_run_id": PARENT_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "command": f"python -B {rel(Path(__file__))}",
            "inputs": [
                rel(PARENT_FINAL_DECISION),
                rel(PARENT_QUEUE),
                rel(PARENT_PLAN),
                rel(SOURCE_FEATURE_MATRIX),
                rel(SOURCE_EXPECTED_TAPE),
                rel(SOURCE_ATTEMPT_PACKAGE),
            ],
            "outputs": [rel(path) for path in output_paths() if path_is_file(path)],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def ledger_rows(summary: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    gate_passes = sum(1 for gate in gates if gate["status"] == "passed")
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
        "path": rel(REPORT_PATH),
        "report_path": rel(REPORT_PATH),
        "primary_report": rel(REPORT_PATH),
        "gate_passes": gate_passes,
        "gate_total": gate_total,
        "claim_boundary": CLAIM_BOUNDARY,
        "scoreboard_lane": "runtime_probe_package(런타임 탐침 패키지)",
        "lane": "experiment_execution(실험 실행)",
        "family": "experiment_execution(실험 실행)",
        "run_number": RUN_NUMBER,
        "source_package_run_id": "run343D_materialize_trade_shape_rescue_quality_margin_blend_package_without_db_v1",
        "attempt_count": summary["attempt_count"],
        "sample_rows": summary["feature_rows"],
        "feature_count": summary["feature_count"],
        "matched_rows": summary["expected_rows"],
        "notes": "Package only(패키지 전용); opens run344D MT5 runtime probe(344D MT5 런타임 탐침 개방).",
    }
    tier_a = {
        **base,
        "ledger_row_id": f"{RUN_ID}__Tier A",
        "subrun_id": "Tier A",
        "view": "Tier A separate(Tier A 분리)",
        "record_view": "Tier A separate(Tier A 분리)",
        "tier": "Tier A",
        "tier_scope": "Tier A",
        "metric_scope": "runtime_package_no_mt5_kpi",
        "kpi_scope": "runtime_package_no_mt5_kpi",
        "candidate_model_id": "12_runtime_mapped_variants",
        "result_status": "package_ready_runtime_execution_required_no_selection(패키지 준비, 런타임 실행 필요, 선정 없음)",
        "primary_kpi": f"attempt_count={summary['attempt_count']};expected_rows={summary['expected_rows']};preview_max_signal_trade_count={summary['preview_max_signal_trade_count']}",
        "guardrail_kpi": f"no_mt5_kpi;side_filter_missing_feature_rows={summary['side_filter_missing_feature_rows']};common_sync_missing={summary['common_sync_missing']}",
        "external_verification_status": "pending_mt5_runtime_probe(MT5 런타임 탐침 대기)",
    }
    tier_b = {
        **base,
        "ledger_row_id": f"{RUN_ID}__Tier B",
        "subrun_id": "Tier B",
        "view": "Tier B separate(Tier B 분리)",
        "record_view": "Tier B separate(Tier B 분리)",
        "tier": "Tier B",
        "tier_scope": "Tier B",
        "metric_scope": "missing_required",
        "kpi_scope": "missing_required",
        "candidate_model_id": "missing_required",
        "result_status": "missing_required(필수 누락)",
        "primary_kpi": "missing_required",
        "guardrail_kpi": "missing_required",
        "external_verification_status": "missing_required(필수 누락)",
        "attempt_count": "",
    }
    combined = {
        **tier_a,
        "ledger_row_id": f"{RUN_ID}__Tier A+B",
        "subrun_id": "Tier A+B",
        "view": "Tier A+B combined(Tier A+B 합산)",
        "record_view": "Tier A+B combined(Tier A+B 합산)",
        "tier": "Tier A+B",
        "tier_scope": "Tier A+B",
        "metric_scope": "same_as_tier_a_until_tier_b_available",
        "kpi_scope": "same_as_tier_a_until_tier_b_available",
        "result_status": "same_as_tier_a_until_tier_b_available",
    }
    return [tier_a, tier_b, combined]


def write_registries(summary: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    rows = ledger_rows(summary, gates)
    append_or_replace_csv(STAGE_LEDGER, ["run_id", "view"], [{key: row.get(key, "") for key in STAGE_LEDGER_COLUMNS} for row in rows])
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], rows)
    append_or_replace_csv(
        RUN_REGISTRY,
        ["run_id"],
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "experiment_execution(실험 실행)",
                "family": "experiment_execution(실험 실행)",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(FINAL_DECISION),
                "notes": "Directional long quality surface package only(방향성 롱 품질 표면 패키지 전용).",
                "primary_report": rel(REPORT_PATH),
                "run_number": RUN_NUMBER,
                "date": TODAY,
                "decision": DECISION,
                "parent_run_id": PARENT_RUN_ID,
                "next_run_id": NEXT_RUN_ID,
                "gate_passes": sum(1 for gate in gates if gate["status"] == "passed"),
                "gate_total": len(gates),
                "claim_boundary": CLAIM_BOUNDARY,
                "report_path": rel(REPORT_PATH),
                "primary_artifact": rel(FINAL_DECISION),
                "candidate_model_id": "12_runtime_mapped_variants",
                "result_status": "package_ready_runtime_execution_required_no_selection(패키지 준비, 런타임 실행 필요, 선정 없음)",
                "matched_rows": summary["expected_rows"],
                "sample_rows": summary["feature_rows"],
                "feature_count": summary["feature_count"],
                "attempt_count": summary["attempt_count"],
                "view": "Tier A separate(Tier A 분리)",
                "tier": "Tier A",
                "metric_scope": "runtime_package_no_mt5_kpi",
                "source_package_run_id": "run343D_materialize_trade_shape_rescue_quality_margin_blend_package_without_db_v1",
            }
        ],
    )
    artifact_rows = []
    for path in output_paths():
        if path_is_file(path):
            artifact_rows.append(
                {
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "artifact_type": path.suffix.lstrip(".") or "file",
                    "path": rel(path),
                    "artifact_path": rel(path),
                    "sha256": sha256_file(path),
                    "created_at": TODAY,
                    "created_at_utc": now_utc(),
                    "notes": "run344C directional long quality runtime package artifact(344C 방향성 롱 품질 런타임 패키지 산출물)",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    append_or_replace_csv(ARTIFACT_REGISTRY, ["stage_id", "run_id", "path"], artifact_rows)


def main() -> None:
    _queue, _plan, source_package, source_expected, _parent = load_context()
    feature_common, feature_rows, feature_count, feature_hash, feature_columns, duplicate_timestamps = materialize_feature_matrix(source_package)
    features = read_csv(FEATURE_MATRIX)
    variants = resolve_variants(source_expected, source_package, features, feature_columns)
    expected, preview, audit = build_expected_tape(variants, source_expected, features)
    tables = materialize_attempts(variants, source_package, feature_common, feature_count, feature_hash)
    summary = build_summary(variants, feature_rows, feature_count, feature_hash, duplicate_timestamps, expected, preview, audit, tables)
    write_contracts_and_receipts(summary)
    write_docs(summary)
    write_lineage_receipt()
    gates = build_gates(summary)
    write_csv_rows(GATE_AUDIT, gates)
    write_final_and_manifest(summary, gates)
    write_registries(summary, gates)
    write_lineage_receipt()
    gates = build_gates(summary)
    write_csv_rows(GATE_AUDIT, gates)
    write_final_and_manifest(summary, gates)
    print(json.dumps({
        "run_id": RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "next_run_id": NEXT_RUN_ID,
        "attempt_count": summary["attempt_count"],
        "gate_passes": sum(1 for gate in gates if gate["status"] == "passed"),
        "gate_total": len(gates),
        "mt5_execution": "not_run",
        "goal_achieve": "not_claimed",
    }, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
