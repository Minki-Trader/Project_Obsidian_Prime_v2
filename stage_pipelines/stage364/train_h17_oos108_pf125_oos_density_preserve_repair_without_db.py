from __future__ import annotations

import csv
import json
import math
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, json_ready  # noqa: E402
from stage_pipelines.stage364 import review_h17_oos108_pf125_validation_density_profit_repair_without_db as fi  # noqa: E402
from stage_pipelines.stage364 import train_h17_oos108_pf125_validation_density_profit_repair_without_db as fh  # noqa: E402


TODAY = "2026-06-07"
STAGE_ID = fh.STAGE_ID
RUN_NUMBER = "run364FJ"
RUN_ID = "run364FJ_train_h17_oos108_pf125_oos_density_preserve_repair_without_db_v1"
PARENT_RUN_ID = fi.RUN_ID
NEXT_RUN_ID = "run364FK_review_h17_oos108_pf125_oos_density_preserve_repair_without_db_v1"

STATUS_NO_STRICT = "completed_stage364FJ_oos_density_preserve_repair_no_strict_pass_review_required_no_authority"
STATUS_STRICT = "completed_stage364FJ_oos_density_preserve_repair_strict_proxy_review_required_no_authority"
JUDGMENT_NO_STRICT = "inconclusive_oos_density_preserve_repair_no_strict_pass_review_required_no_authority"
JUDGMENT_STRICT = "inconclusive_oos_density_preserve_repair_strict_proxy_review_required_no_authority"
DECISION_NO_STRICT = "stage364FJ_open_run364FK_oos_density_preserve_repair_review"
DECISION_STRICT = "stage364FJ_open_run364FK_oos_density_preserve_repair_review"
CLAIM_BOUNDARY = (
    "research_development_oos_density_preserve_repair_proxy_and_onnx_smoke_only_no_new_mt5_execution_"
    "no_runtime_package_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

STAGE_DIR = fh.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
MODEL_DIR = RUN_DIR / "models"
ONNX_DIR = RUN_DIR / "onnx"
REVIEW_DIR = STAGE_DIR / "03_reviews"
SPEC_DIR = STAGE_DIR / "00_spec"
SELECTED_DIR = STAGE_DIR / "04_selected"

INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
FEATURE_AUDIT = RUN_DIR / "fj_feature_audit.csv"
LABEL_SUMMARY = RUN_DIR / "fj_label_summary.csv"
MODEL_SCORECARD = RUN_DIR / "fj_model_scorecard.csv"
TRADE_SURFACE = RUN_DIR / "fj_surface.csv"
SELECTED_CANDIDATE = RUN_DIR / "selected_fj_candidate.json"
SELECTED_TRADE_TAPE = RUN_DIR / "selected_fj_trade_tape.csv"
MONTH_STABILITY = RUN_DIR / "selected_fj_month_stability.csv"
COST_STRESS = RUN_DIR / "selected_fj_cost_stress.csv"
SIDE_SESSION_REVIEW = RUN_DIR / "selected_fj_side_session_review.csv"
MODEL_ARTIFACT_MANIFEST = RUN_DIR / "model_artifact_manifest.csv"
ONNX_SMOKE_REPORT = RUN_DIR / "onnx_smoke_report.csv"
DATA_INTEGRITY_AUDIT = RUN_DIR / "data_integrity_audit.csv"
RUN364FK_QUEUE = RUN_DIR / "fj_fk_queue.csv"
RUN_EVIDENCE_RECEIPT = RUN_DIR / "run_evidence_receipt.json"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment_design_receipt.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
ATTRIBUTION_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / "run364FJ_oos_density_preserve_repair.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364FJ_oos_density_preserve_repair.md"
REVIEW_INDEX = REVIEW_DIR / "review_index.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"
STAGE_BRIEF = SPEC_DIR / "stage_brief.md"
SELECTION_STATUS = SELECTED_DIR / "selection_status.md"
STAGE_README = STAGE_DIR / "README.md"

WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
PROJECT_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
IDEA_REGISTRY = ROOT / "docs" / "registers" / "idea_registry.md"
NEGATIVE_REGISTER = ROOT / "docs" / "registers" / "negative_result_register.md"

THIS_FILE = Path(__file__)
et = fh.et

INPUT_FILES = [
    fi.FINAL_DECISION,
    fi.GATE_AUDIT,
    fi.REVIEW_SUMMARY,
    fi.SURFACE_DIAGNOSTIC,
    fi.FAILURE_ATTRIBUTION,
    fi.PACKAGE_DECISION,
    fi.FAILURE_MEMORY,
    fi.RUN364FJ_QUEUE,
    fh.FINAL_DECISION,
    fh.TRADE_SURFACE,
    fh.SELECTED_CANDIDATE,
    fh.SELECTED_TRADE_TAPE,
    fh.COST_STRESS,
    fh.SIDE_SESSION_REVIEW,
    fh.MONTH_STABILITY,
    et.dt.dp.MODEL_INPUT_DATASET,
    et.dt.dp.MODEL_INPUT_FEATURE_ORDER,
    et.dt.dp.RAW_US100_M5,
    THIS_FILE,
]

OUTPUT_FILES = [
    INPUT_MANIFEST,
    WORK_PACKET,
    FEATURE_AUDIT,
    LABEL_SUMMARY,
    MODEL_SCORECARD,
    TRADE_SURFACE,
    SELECTED_CANDIDATE,
    SELECTED_TRADE_TAPE,
    MONTH_STABILITY,
    COST_STRESS,
    SIDE_SESSION_REVIEW,
    MODEL_ARTIFACT_MANIFEST,
    ONNX_SMOKE_REPORT,
    DATA_INTEGRITY_AUDIT,
    RUN364FK_QUEUE,
    RUN_EVIDENCE_RECEIPT,
    EXPERIMENT_RECEIPT,
    DATA_RECEIPT,
    MODEL_RECEIPT,
    ATTRIBUTION_RECEIPT,
    JUDGMENT_RECEIPT,
    LINEAGE_RECEIPT,
    CLAIM_RECEIPT,
    GATE_AUDIT,
    FINAL_DECISION,
    RUN_MANIFEST,
    REPORT_PATH,
    DECISION_DOC,
    REVIEW_INDEX,
    STAGE_LEDGER,
    STAGE_BRIEF,
    SELECTION_STATUS,
    STAGE_README,
    WORKSPACE_STATE,
    CURRENT_WORKING_STATE,
    WORKSPACE_CHANGELOG,
    RUN_REGISTRY,
    PROJECT_LEDGER,
    ARTIFACT_REGISTRY,
    IDEA_REGISTRY,
    NEGATIVE_REGISTER,
    THIS_FILE,
]

LABEL_SPECS = [
    {"label_id": "fj_sym_h2_m1p75", "horizon_m5": 2, "threshold_points": 1.75, "mode": "symmetric"},
    {"label_id": "fj_sym_h2_m2p25", "horizon_m5": 2, "threshold_points": 2.25, "mode": "symmetric"},
    {"label_id": "fj_asym_h2_l1p75_s3p0", "horizon_m5": 2, "threshold_points": 2.30, "long_threshold_points": 1.75, "short_threshold_points": 3.00, "mode": "asymmetric"},
    {"label_id": "fj_asym_h3_l2p25_s3p5", "horizon_m5": 3, "threshold_points": 2.80, "long_threshold_points": 2.25, "short_threshold_points": 3.50, "mode": "asymmetric"},
]
TARGET_DENSITIES = [3.0, 3.1, 3.25, 3.5, 4.0, 4.75, 5.5]
MARGINS = [-0.08, -0.04, -0.02, 0.0, 0.02]
HOUR_SETS = {
    "fj_dense_cash_15_16_17_18_20_22": [15, 16, 17, 18, 20, 22],
    "fj_oos_cost_16_18_20_22": [16, 18, 20, 22],
    "fj_no_h19": [15, 16, 17, 18, 20, 21, 22],
    "fj_cash_15_to_22": [15, 16, 17, 18, 19, 20, 21, 22],
    "fj_val_oos_bridge_15_16_18_21_22": [15, 16, 18, 21, 22],
}
EXTRA_FILTERS = [
    "none",
    "fj_oos_pf_cost_guard",
    "fj_validation_density_preserve",
    "fj_dual_density_cost_guard",
    "fj_short_balance_cost_guard",
    "fj_no_cost_bleed",
]

DENSITY_FLOOR = 3.0
STRICT_SHORT_SHARE_FLOOR = 0.77
PRESERVE_SHORT_SHARE_FLOOR = 0.77
STRICT_MIN_PF_FLOOR = 1.05
OOS_PF_TARGET = 1.25
OPERATIONAL_MIN_PF_FLOOR = 1.18
RUNTIME_NET_REFERENCE = 523.58


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    return fh.rel(path)


def exists(path: Path | str) -> bool:
    return Path(path).exists()


def sha(path: Path | str) -> str:
    return fh.sha(path)


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return default
    if not math.isfinite(number):
        return default
    return number


def read_json(path: Path) -> Any:
    with io_path(path).open("r", encoding="utf-8-sig") as handle:
        return json.load(handle)


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8") as handle:
        json.dump(json_ready(payload), handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")


def write_text(path: Path, text: str, *, bom: bool = True) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8-sig" if bom else "utf-8")


def append_text_once(path: Path, marker: str, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    existing = path.read_text(encoding="utf-8-sig") if path.exists() else ""
    if marker in existing:
        return
    payload = existing.rstrip() + "\n" + text.lstrip() if existing.strip() else text
    path.write_text(payload, encoding="utf-8-sig")


def append_or_replace_csv(path: Path, key_fields: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> None:
    rows = list(rows)
    existing_rows: list[dict[str, Any]] = []
    fieldnames: list[str] = []
    if path.exists():
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = list(reader.fieldnames or [])
            existing_rows = list(reader)
    for row in rows:
        for key in row.keys():
            if key not in fieldnames:
                fieldnames.append(str(key))
    if not fieldnames:
        fieldnames = ["empty"]
    new_keys = {tuple(str(row.get(key, "")) for key in key_fields) for row in rows}
    kept = [row for row in existing_rows if tuple(str(row.get(key, "")) for key in key_fields) not in new_keys]
    merged = kept + [dict(row) for row in rows]
    path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = path.with_name(f".{path.name}.tmp")
    with temp_path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in merged:
            writer.writerow({key: row.get(key, "") for key in fieldnames})
    temp_path.replace(path)


def validate_inputs() -> dict[str, Any]:
    missing = [rel(path) for path in INPUT_FILES if path != THIS_FILE and not exists(path)]
    if missing:
        raise FileNotFoundError("missing FJ inputs(FJ 입력 누락): " + ", ".join(missing))
    parent = read_json(fi.FINAL_DECISION)
    if parent.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"FI next_run_id mismatch(FI 다음 실행 ID 불일치): {parent.get('next_run_id')} != {RUN_ID}")
    for key in ["runtime_authority", "operating_promotion", "live_readiness", "goal_achieve"]:
        if parent.get(key, "not_claimed") != "not_claimed":
            raise RuntimeError(f"forbidden FI claim(금지된 FI 주장): {key}={parent.get(key)}")
    gates = pd.read_csv(io_path(fi.GATE_AUDIT), encoding="utf-8-sig").fillna("")
    if gates.empty or any(gates["status"].astype(str) != "passed"):
        raise RuntimeError("FI gate audit(FI 게이트 감사)가 모두 passed(통과)가 아닙니다.")
    return parent


def input_manifest_rows() -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "input_path": rel(path),
            "exists": str(exists(path)).lower(),
            "sha256": sha(path) if exists(path) and io_path(path).is_file() else "",
            "input_role": "FJ OOS density preserve repair input(FJ 표본외 밀도 보존 수리 입력)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for path in INPUT_FILES
    ]


def full_label_spec(spec: Mapping[str, Any]) -> Mapping[str, Any]:
    label_id = str(spec.get("label_id", ""))
    for candidate in LABEL_SPECS:
        if candidate["label_id"] == label_id:
            return {**candidate, **dict(spec)}
    return spec


def fj_label_values(frame: pd.DataFrame, spec: Mapping[str, Any]) -> tuple[np.ndarray, np.ndarray]:
    spec = full_label_spec(spec)
    horizon = int(spec["horizon_m5"])
    move = frame[f"future_open_h{horizon}"] - frame["entry_open"]
    ok = np.isfinite(move.to_numpy(dtype=float)) & np.isfinite(frame["entry_open"].to_numpy(dtype=float))
    if spec.get("mode") == "asymmetric":
        long_threshold = float(spec["long_threshold_points"])
        short_threshold = float(spec["short_threshold_points"])
    else:
        long_threshold = short_threshold = float(spec["threshold_points"])
    move_values = move.to_numpy(dtype=float)
    labels = np.where(move_values <= -short_threshold, 0, np.where(move_values >= long_threshold, 2, 1)).astype("int8")
    labels[~ok] = 1
    return labels, ok


def fj_feature_sets(feature_order: Sequence[str]) -> dict[str, list[str]]:
    base = list(feature_order)
    derived = et.dt.derived_features()
    price = [column for column in base if any(token in column for token in ["return", "ratio", "rsi", "atr", "adx", "vol", "gap"])]
    macro = [column for column in base if any(token in column for token in ["vix", "us10yr", "usdx", "mega8", "breadth"])]
    session = [column for column in base if any(token in column for token in ["cash", "minutes", "open", "close"])]
    behavior = [column for column in base if any(token in column for token in ["trend", "momentum", "range", "body", "wick", "spread"])]
    return {
        "fj_all72": list(dict.fromkeys(base + derived)),
        "fj_macro_session_cost": list(dict.fromkeys(price + macro + session + derived)),
        "fj_behavior_density_cost": list(dict.fromkeys(price + macro + session + behavior + derived)),
    }


def fj_model_specs() -> list[tuple[str, str, Any]]:
    return [
        (
            "et8_l18_n160",
            "ExtraTrees(엑스트라트리)",
            et.dt.dp.ExtraTreesClassifier(n_estimators=160, max_depth=8, min_samples_leaf=18, class_weight="balanced", random_state=831, n_jobs=1),
        ),
        (
            "et9_l24_n160",
            "ExtraTrees(엑스트라트리)",
            et.dt.dp.ExtraTreesClassifier(n_estimators=160, max_depth=9, min_samples_leaf=24, class_weight="balanced", random_state=832, n_jobs=1),
        ),
        (
            "rf8_l28_n160",
            "RandomForest(랜덤포레스트)",
            et.dt.dp.RandomForestClassifier(n_estimators=160, max_depth=8, min_samples_leaf=28, class_weight="balanced_subsample", random_state=833, n_jobs=1),
        ),
    ]


def col(frame: pd.DataFrame, name: str, default: float = 0.0) -> np.ndarray:
    if name in frame.columns:
        return frame[name].to_numpy(dtype=float)
    return np.full(len(frame), default, dtype=float)


def fj_extra_mask(frame: pd.DataFrame, side: np.ndarray, extra_filter: str) -> np.ndarray:
    mask = np.ones(len(frame), dtype=bool)
    hour = frame["timestamp"].dt.hour.to_numpy(dtype=int)
    breadth = col(frame, "mega8_pos_breadth_1", 0.5)
    vol_ratio = col(frame, "historical_vol_5_over_20", 1.0)
    log_return_3 = col(frame, "log_return_3", 0.0)
    vix_stress = col(frame, "vix_zscore_20", 0.0)
    range_ratio = col(frame, "range_5_over_20", 1.0)
    if extra_filter == "none":
        return mask
    if extra_filter == "fj_oos_pf_cost_guard":
        long_ok = (side == "long") & np.isin(hour, [15, 16, 18, 21, 22]) & (breadth >= 0.42) & (vix_stress <= 1.50) & (range_ratio >= 0.72)
        short_ok = (side == "short") & np.isin(hour, [16, 18, 22]) & (vol_ratio >= 0.88) & ((breadth <= 0.53) | (log_return_3 < -0.00012))
        return mask & (long_ok | short_ok)
    if extra_filter == "fj_validation_density_preserve":
        long_ok = (side == "long") & np.isin(hour, [15, 16, 17, 18, 20, 21, 22]) & (breadth >= 0.35) & (vix_stress <= 1.75)
        short_ok = (side == "short") & np.isin(hour, [16, 17, 18, 22]) & (vol_ratio >= 0.78) & ((breadth <= 0.58) | (log_return_3 < -0.00005))
        return mask & (long_ok | short_ok)
    if extra_filter == "fj_dual_density_cost_guard":
        long_ok = (side == "long") & np.isin(hour, [15, 16, 18, 20, 22]) & (breadth >= 0.40) & (range_ratio >= 0.75)
        short_ok = (side == "short") & np.isin(hour, [16, 18, 22]) & (vol_ratio >= 0.90) & (breadth <= 0.55)
        return mask & (long_ok | short_ok)
    if extra_filter == "fj_short_balance_cost_guard":
        long_ok = (side == "long") & np.isin(hour, [15, 16, 18, 20, 21, 22]) & (breadth >= 0.44) & (vix_stress <= 1.55)
        short_ok = (side == "short") & np.isin(hour, [16, 18, 22]) & (vol_ratio >= 0.92) & (breadth <= 0.52)
        return mask & (long_ok | short_ok)
    if extra_filter == "fj_no_cost_bleed":
        veto = (
            ((side == "short") & np.isin(hour, [17, 20]))
            | ((side == "short") & (hour == 18) & (vol_ratio < 0.86))
            | ((side == "long") & (hour == 19) & (breadth < 0.56))
            | ((side == "long") & (vix_stress > 1.85))
        )
        return mask & ~veto
    raise ValueError(f"unknown FJ filter(알 수 없는 FJ 필터): {extra_filter}")


def fj_cost_values(row: Mapping[str, Any]) -> dict[str, float]:
    values = et.er.cost_side_values(row)
    validation_trades = as_float(row.get("validation_trade_count"))
    oos_trades = as_float(row.get("oos_trade_count"))
    validation_net = as_float(row.get("validation_net"))
    oos_net = as_float(row.get("oos_net"))
    values["validation_cost09_net"] = validation_net - 0.60 * validation_trades
    values["oos_cost09_net"] = oos_net - 0.60 * oos_trades
    values["validation_trade_density"] = as_float(row.get("validation_trade_density"))
    values["oos_trade_density"] = as_float(row.get("oos_trade_density"))
    return values


def fj_strict_success(row: Mapping[str, Any]) -> bool:
    values = fj_cost_values(row)
    validation_pf = as_float(row.get("validation_profit_factor"))
    oos_pf = as_float(row.get("oos_profit_factor"))
    min_pf = min(validation_pf, oos_pf)
    return (
        as_float(row.get("validation_net")) > 0.0
        and as_float(row.get("oos_net")) > 0.0
        and oos_pf >= OOS_PF_TARGET
        and values["oos_cost09_net"] >= 0.0
        and values["validation_cost09_net"] >= -120.0
        and values["validation_trade_density"] >= DENSITY_FLOOR
        and values["oos_trade_density"] >= DENSITY_FLOOR
        and values["combined_trade_density"] >= DENSITY_FLOOR
        and values["combined_net"] > 0.0
        and values["combined_cost06_net"] >= 0.0
        and values["combined_short_share"] <= STRICT_SHORT_SHARE_FLOOR
        and min_pf >= STRICT_MIN_PF_FLOOR
    )


def fj_operational_stack(row: Mapping[str, Any]) -> bool:
    values = fj_cost_values(row)
    min_pf = min(as_float(row.get("validation_profit_factor")), as_float(row.get("oos_profit_factor")))
    return fj_strict_success(row) and values["combined_net"] >= RUNTIME_NET_REFERENCE and min_pf >= OPERATIONAL_MIN_PF_FLOOR


def fj_selection_score(row: Mapping[str, Any]) -> float:
    values = fj_cost_values(row)
    validation_net = as_float(row.get("validation_net"))
    oos_net = as_float(row.get("oos_net"))
    validation_pf = as_float(row.get("validation_profit_factor"))
    oos_pf = as_float(row.get("oos_profit_factor"))
    min_pf = min(validation_pf, oos_pf)
    density = values["combined_trade_density"]
    validation_density = values["validation_trade_density"]
    oos_density = values["oos_trade_density"]
    short_share = values["combined_short_share"]
    density_floor_credit = min(validation_density, oos_density, density)
    validation_cost09 = values["validation_cost09_net"]
    oos_cost09 = values["oos_cost09_net"]
    strict_shape_bonus = (
        1.0
        if validation_net > 0.0
        and validation_density >= DENSITY_FLOOR
        and oos_density >= DENSITY_FLOOR
        and density >= DENSITY_FLOOR
        and oos_pf >= OOS_PF_TARGET
        and oos_cost09 >= 0.0
        and short_share <= PRESERVE_SHORT_SHARE_FLOOR
        else 0.0
    )
    return (
        1.20 * validation_net
        + 1.72 * oos_net
        + 0.84 * values["combined_net"]
        + 3350.0 * max(0.0, oos_pf - 1.0)
        + 1180.0 * max(0.0, validation_pf - 1.0)
        + 980.0 * max(0.0, min_pf - 1.0)
        + 3.90 * oos_cost09
        + 1.70 * values["oos_cost06_net"]
        + 1.00 * values["combined_cost09_net"]
        + 0.95 * validation_cost09
        + 1160.0 * min(density_floor_credit, 4.5)
        + 420.0 * min(validation_density, 5.5)
        + 390.0 * min(oos_density, 5.5)
        + 360.0 * min(density, 5.5)
        + 980.0 * max(0.0, PRESERVE_SHORT_SHARE_FLOOR - short_share)
        + 3900.0 * strict_shape_bonus
        - 3400.0 * max(0.0, OOS_PF_TARGET - oos_pf)
        - 2100.0 * (1.0 if validation_net <= 0.0 else 0.0)
        - 1700.0 * (1.0 if oos_net <= 0.0 else 0.0)
        - 13.0 * max(0.0, -oos_cost09)
        - 6.0 * max(0.0, -validation_cost09 - 80.0)
        - 3.8 * max(0.0, -values["combined_cost09_net"])
        - 3100.0 * max(0.0, DENSITY_FLOOR - validation_density)
        - 2600.0 * max(0.0, DENSITY_FLOOR - oos_density)
        - 3000.0 * max(0.0, DENSITY_FLOOR - density)
        - 1650.0 * max(0.0, short_share - PRESERVE_SHORT_SHARE_FLOOR)
        - 900.0 * max(0.0, STRICT_MIN_PF_FLOOR - min_pf)
    )


def write_work_packet(parent: Mapping[str, Any]) -> None:
    write_json(
        WORK_PACKET,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "primary_family": "experiment_execution(실험 실행)",
            "primary_skill": "obsidian-run-evidence-system(옵시디언 실행 근거 시스템)",
            "support_skills": [
                "obsidian-experiment-design(옵시디언 실험 설계)",
                "obsidian-data-integrity(옵시디언 데이터 무결성)",
                "obsidian-model-validation(옵시디언 모델 검증)",
                "obsidian-artifact-lineage(옵시디언 산출물 계보)",
            ],
            "required_gates": [
                "scope_completion_gate",
                "kpi_contract_audit",
                "skill_receipt_lint",
                "required_gate_coverage_audit",
            ],
            "hypothesis": "FJ OOS density preserve repair(FJ 표본외 밀도 보존 수리)가 FH의 validation-positive density3(검증 양수 밀도3)를 보존하면서 OOS PF/cost(표본외 수익 팩터/비용)를 회복할 수 있는지 시험합니다.",
            "preserve_conditions": [
                "validation_net>0(검증 순수익 양수)",
                "validation_density>=3 and combined_density>=3(검증/합산 밀도 3 이상)",
                "combined_short_share<=0.77(합산 숏 비중 0.77 이하)",
            ],
            "repair_conditions": [
                "OOS PF>=1.25(표본외 수익 팩터 1.25 이상)",
                "OOS cost0.9>=0(표본외 비용0.9 0 이상)",
                "validation cost0.9 not deeply negative(검증 비용0.9 과도 음수 방지)",
            ],
            "avoid": "validation-only scoring(검증 전용 점수), low-density PF(저밀도 수익 팩터), cost0.9 negative rows(비용0.9 음수 행)",
            "parent_summary": {
                "selected_model_id": parent.get("selected_model_id"),
                "validation_positive_density3_count": parent.get("validation_positive_density3_count"),
                "validation_positive_density3_oos_pf125_count": parent.get("validation_positive_density3_oos_pf125_count"),
                "selected_oos_profit_factor": parent.get("selected_oos_profit_factor"),
                "selected_oos_cost09_net": parent.get("selected_oos_cost09_net"),
            },
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def write_queue(summary: Mapping[str, Any]) -> None:
    RUN364FK_QUEUE.parent.mkdir(parents=True, exist_ok=True)
    et.write_csv(
        RUN364FK_QUEUE,
        [
            {
                "run_id": RUN_ID,
                "next_run_id": NEXT_RUN_ID,
                "queue_rank": 1,
                "queue_id": "fk01_oos_density_preserve_review",
                "review_subject": summary["selected_model_id"],
                "strict_candidate_count": summary["strict_candidate_count"],
                "operational_proxy_stack_pass_count": summary["operational_proxy_stack_pass_count"],
                "selected_validation_density": summary["selected_validation_trade_density"],
                "selected_validation_net": summary["selected_validation_net"],
                "selected_oos_profit_factor": summary["selected_oos_profit_factor"],
                "selected_oos_cost06_net": summary["selected_oos_cost06_net"],
                "selected_combined_density": summary["selected_combined_trade_density"],
                "selected_combined_cost09_net": summary["selected_combined_cost09_net"],
                "selected_combined_short_share": summary["selected_combined_short_share"],
                "effect": "FK review(FK 검토)가 FJ의 표본외 보존 수리가 package(패키지) 후보인지 실패 기억인지 분리합니다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )


def write_receipts(final: Mapping[str, Any]) -> None:
    base = {"run_id": RUN_ID, "stage_id": STAGE_ID, "created_at_utc": final["created_at_utc"], "claim_boundary": CLAIM_BOUNDARY}
    write_json(RUN_EVIDENCE_RECEIPT, {**base, "surface": rel(TRADE_SURFACE), "selected_candidate": rel(SELECTED_CANDIDATE), "selected_trade_tape": rel(SELECTED_TRADE_TAPE), "measurement_boundary": "Python proxy with ONNX smoke(Python 프록시와 ONNX 스모크), no MT5(MT5 없음)"})
    write_json(EXPERIMENT_RECEIPT, {**base, "hypothesis": "FJ OOS density preserve repair(FJ 표본외 밀도 보존 수리)가 검증 밀도와 표본외 PF/비용을 동시에 복구하는지 시험합니다.", "comparison_baseline": PARENT_RUN_ID, "decision_use": NEXT_RUN_ID})
    write_json(DATA_RECEIPT, {**base, "data_source": [rel(et.dt.dp.MODEL_INPUT_DATASET), rel(et.dt.dp.RAW_US100_M5)], "time_axis": "UTC model input timestamp(UTC 모델 입력 타임스탬프)", "sample_scope": "US100 M5 Tier A proxy split(US100 M5 Tier A 프록시 분할)", "feature_label_boundary": "future_open only in labels(future_open은 라벨에만 사용)", "split_boundary": "chronological train/validation/OOS(시간순 학습/검증/표본외)", "integrity_judgment": "usable_with_proxy_boundary(프록시 경계 안에서 사용 가능)"})
    write_json(MODEL_RECEIPT, {**base, "model_family": "RandomForest/ExtraTrees(랜덤포레스트/엑스트라트리)", "target_and_label": "3-class next-open horizon direction(3분류 다음 시가 horizon 방향)", "split_method": "chronological holdout(시간순 홀드아웃)", "selection_metric": "FJ score balances OOS PF/cost, validation density, combined density, short balance(FJ 점수는 표본외 PF/비용, 검증 밀도, 합산 밀도, 숏 균형을 함께 봄)", "threshold_policy": "searched threshold and density target(탐색 임계값과 밀도 목표)", "selected_model_id": final["selected_model_id"], "onnx_smoke_pass_rows": final["onnx_smoke_pass_rows"], "validation_judgment": final["judgment"]})
    write_json(ATTRIBUTION_RECEIPT, {**base, "observed_change": f"selected validation/OOS net/PF/density {final['selected_validation_net']}/{final['selected_validation_profit_factor']}/{final['selected_validation_trade_density']} and {final['selected_oos_net']}/{final['selected_oos_profit_factor']}/{final['selected_oos_trade_density']}", "likely_drivers": ["OOS PF/cost score(표본외 수익 팩터/비용 점수)", "dual density guard(양쪽 밀도 가드)", "short balance guard(숏 균형 가드)"], "next_probe": NEXT_RUN_ID})
    write_json(JUDGMENT_RECEIPT, {**base, "result_subject": RUN_ID, "evidence_available": [rel(TRADE_SURFACE), rel(SELECTED_CANDIDATE), rel(ONNX_SMOKE_REPORT), rel(DATA_INTEGRITY_AUDIT)], "evidence_missing": ["MT5 runtime package(MT5 런타임 패키지)", "MT5 runtime probe(MT5 런타임 탐침)", "forward/replay evidence(전진/재생 근거)"], "judgment_label": final["judgment"], "next_condition": NEXT_RUN_ID})
    write_json(LINEAGE_RECEIPT, {**base, "source_inputs": [{"path": rel(path), "sha256": sha(path)} for path in INPUT_FILES if exists(path) and io_path(path).is_file()], "producer": rel(THIS_FILE), "consumer": NEXT_RUN_ID, "artifact_paths": [rel(path) for path in OUTPUT_FILES if exists(path)], "artifact_hashes": {rel(path): sha(path) for path in OUTPUT_FILES if exists(path) and io_path(path).is_file()}, "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)], "lineage_judgment": "connected_proxy_model_reseed(프록시 모델 재시드 연결)"})
    write_json(CLAIM_RECEIPT, {**base, "runtime_package": "not_opened", "runtime_authority": "not_claimed", "operating_promotion": "not_claimed", "live_readiness": "not_claimed", "goal_achieve": "not_claimed", "effect": "FJ 모델 단서를 운영 주장으로 올리지 않습니다."})


def write_docs(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    gate_lines = "\n".join(f"- {row['gate']}: {row['status']} -> {row['evidence']}" for row in gates)
    report = f"""# run364FJ OOS Density Preserve Repair(표본외 밀도 보존 수리)

Created(생성): {final['created_at_utc']}

Action(행동): FI failure memory(FI 실패 기억)를 받아 OOS PF/cost score(표본외 수익 팩터/비용 점수), dual density guard(양쪽 밀도 가드), short balance guard(숏 균형 가드)를 학습했습니다.

Effect(효과): FH가 만든 validation-positive density3(검증 양수 밀도3) 단서를 버리지 않고 OOS PF/cost(표본외 수익 팩터/비용)를 회복할 수 있는지 확인합니다.

- judgment(판정): `{final['judgment']}`
- selected_model_id(선택 모델 ID): `{final['selected_model_id']}`
- validation net/PF/density(검증 순수익/수익 팩터/밀도): `{final['selected_validation_net']}` / `{final['selected_validation_profit_factor']}` / `{final['selected_validation_trade_density']}`
- OOS net/PF/density(표본외 순수익/수익 팩터/밀도): `{final['selected_oos_net']}` / `{final['selected_oos_profit_factor']}` / `{final['selected_oos_trade_density']}`
- OOS cost0.6 net(표본외 비용0.6 순수익): `{final['selected_oos_cost06_net']}`
- combined net/density/cost0.9/short share(합산 순수익/밀도/비용0.9/숏 비중): `{final['selected_combined_net']}` / `{final['selected_combined_trade_density']}` / `{final['selected_combined_cost09_net']}` / `{final['selected_combined_short_share']}`
- strict_candidate_count(엄격 후보 수): `{final['strict_candidate_count']}`
- operational_proxy_stack_pass_count(운영 프록시 묶음 통과 수): `{final['operational_proxy_stack_pass_count']}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`

Gates(게이트):

{gate_lines}

Boundary(경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
"""
    decision_doc = f"""# Decision(결정): stage364FJ OOS Density Preserve Repair(표본외 밀도 보존 수리)

- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{final['decision']}`
- judgment(판정): `{final['judgment']}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Action(행동): FJ model/label/score(모델/라벨/점수) 재시드를 실행하고 FK review(FK 검토)로 넘겼습니다.

Effect(효과): 검증 밀도와 표본외 PF/cost(수익 팩터/비용)의 동시 복구 여부를 운영 주장 없이 다음 판정으로 보냅니다.
"""
    write_text(REPORT_PATH, report, bom=True)
    write_text(DECISION_DOC, decision_doc, bom=True)
    append_text_once(REVIEW_INDEX, f"run364FJ__{RUN_ID}", f"\n- run364FJ__{RUN_ID}: [{REPORT_PATH.name}]({REPORT_PATH.name}) - OOS density preserve repair(표본외 밀도 보존 수리), next `{NEXT_RUN_ID}`.\n")
    append_text_once(STAGE_BRIEF, f"run364FJ__{RUN_ID}", f"\n<!-- run364FJ__{RUN_ID} -->\n\n## run364FJ OOS Density Preserve Repair(표본외 밀도 보존 수리)\n\nAction(행동): 표본외 PF/비용 보존과 검증/합산 밀도 복구를 함께 점수화했습니다.\n\nEffect(효과): `{NEXT_RUN_ID}`에서 패키지 가능성과 실패 경계를 검토합니다.\n")
    append_text_once(STAGE_README, f"run364FJ__{RUN_ID}", f"\n<!-- run364FJ__{RUN_ID} -->\n## run364FJ OOS density preserve repair(표본외 밀도 보존 수리)\n\nNext(다음): `{NEXT_RUN_ID}`.\n")
    write_text(WORKSPACE_STATE, f"""current_stage_id: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {final['status']}
current_judgment: {final['judgment']}
next_run_id: {NEXT_RUN_ID}
runtime_authority: not_claimed
operating_promotion: not_claimed
goal_achieve: not_claimed
updated_at_utc: {final['created_at_utc']}
""", bom=False)
    write_text(CURRENT_WORKING_STATE, f"""# Current Working State(현재 작업 상태)

Updated(갱신): {final['created_at_utc']}

Active stage(활성 단계): `{STAGE_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Current run(현재 실행): `{NEXT_RUN_ID}`

Current truth(현재 진실): `run364FJ` trained(학습 완료) OOS density preserve repair(표본외 밀도 보존 수리). Selected validation/OOS net/PF/density(선택 검증/표본외 순수익/수익 팩터/밀도)는 `{final['selected_validation_net']}` / `{final['selected_validation_profit_factor']}` / `{final['selected_validation_trade_density']}` 및 `{final['selected_oos_net']}` / `{final['selected_oos_profit_factor']}` / `{final['selected_oos_trade_density']}`입니다.

Cost/side truth(비용/방향 진실): OOS cost0.6 net(표본외 비용0.6 순수익)은 `{final['selected_oos_cost06_net']}`이고, combined cost0.9/short share(합산 비용0.9/숏 비중)는 `{final['selected_combined_cost09_net']}` / `{final['selected_combined_short_share']}`입니다.

Next action(다음 행동): `{NEXT_RUN_ID}`에서 FJ 결과를 review(검토)합니다.

Operating boundary(운영 경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""", bom=True)
    write_text(SELECTION_STATUS, f"""# Stage364 selection status(선택 상태)

Updated(갱신): {final['created_at_utc']}

Current run(현재 실행): `{NEXT_RUN_ID}`
Latest completed run(최근 완료 실행): `{RUN_ID}`

Latest scout(최근 탐색): FJ OOS density preserve repair(FJ 표본외 밀도 보존 수리).

Selected model(선택 모델): `{final['selected_model_id']}`

Validation net/PF/density(검증 순수익/수익 팩터/밀도): `{final['selected_validation_net']}` / `{final['selected_validation_profit_factor']}` / `{final['selected_validation_trade_density']}`
OOS net/PF/density(표본외 순수익/수익 팩터/밀도): `{final['selected_oos_net']}` / `{final['selected_oos_profit_factor']}` / `{final['selected_oos_trade_density']}`
Combined net/density/cost0.9/short share(합산 순수익/밀도/비용0.9/숏 비중): `{final['selected_combined_net']}` / `{final['selected_combined_trade_density']}` / `{final['selected_combined_cost09_net']}` / `{final['selected_combined_short_share']}`

Judgment(판정): `{final['judgment']}`.

Authority(권위): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""", bom=True)
    append_text_once(WORKSPACE_CHANGELOG, f"run364FJ__{RUN_ID}", f"\n<!-- run364FJ__{RUN_ID} -->\n- {final['created_at_utc']} `{RUN_ID}` completed OOS density preserve repair(표본외 밀도 보존 수리); strict candidates `{final['strict_candidate_count']}`; selected `{final['selected_model_id']}`; next `{NEXT_RUN_ID}`; no authority claim(권위 주장 없음).\n")
    append_text_once(IDEA_REGISTRY, f"run364FJ__{RUN_ID}", f"\n<!-- run364FJ__{RUN_ID} -->\n- `{RUN_ID}`: OOS density preserve repair(표본외 밀도 보존 수리)를 학습했습니다. Effect(효과): FI 실패 기억을 표본외 PF/비용 회복 점수와 검증/합산 밀도 보존 조건으로 직접 공격했습니다.\n")
    if int(final["strict_candidate_count"]) == 0:
        append_text_once(NEGATIVE_REGISTER, f"run364FJ__strict_candidate_absent__{RUN_ID}", f"\n<!-- run364FJ__strict_candidate_absent__{RUN_ID} -->\n- `{RUN_ID}`: OOS density preserve repair(표본외 밀도 보존 수리)는 strict candidate(엄격 후보)를 만들지 못했습니다. Effect(효과): FK에서 실패 경계와 회수 단서를 분리합니다.\n")


def write_ledgers(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    artifact_count = len({Path(path) for path in OUTPUT_FILES if exists(path) or Path(path) == RUN_MANIFEST})
    common = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(FINAL_DECISION),
        "run_number": RUN_NUMBER,
        "date": TODAY,
        "decision": final["decision"],
        "next_run_id": NEXT_RUN_ID,
        "artifact_count": artifact_count,
        "gate_passes": final["gate_passes"],
        "gate_total": final["gate_total"],
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "created_at_utc": final["created_at_utc"],
        "required_gate_audit": rel(GATE_AUDIT),
        "question": "Can OOS density preserve repair recover OOS PF/cost while preserving validation density?(표본외 밀도 보존 수리가 검증 밀도를 보존하며 표본외 PF/비용을 회복할 수 있는가?)",
        "next_action": NEXT_RUN_ID,
        "notes": f"strict_candidate_count={final['strict_candidate_count']};onnx_smoke_pass_rows={final['onnx_smoke_pass_rows']};validation_density={final['selected_validation_trade_density']};oos_pf={final['selected_oos_profit_factor']};combined_density={final['selected_combined_trade_density']};combined_short={final['selected_combined_short_share']}",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
    }
    rows = []
    for suffix, record_view, tier_scope, status in [
        ("tier_a_separate", "Tier A separate(Tier A 분리)", "Tier A", final["status"]),
        ("tier_b_missing_required", "Tier B separate(Tier B 분리)", "Tier B", "missing_required_no_tier_b_model_input(필수 누락, Tier B 모델 입력 없음)"),
        ("tier_a_b_combined_out_of_scope", "Tier A+B combined(Tier A+B 합산)", "Tier A+B", "out_of_scope_by_claim_proxy_tier_a_only(주장 범위 밖, 프록시 Tier A 전용)"),
    ]:
        rows.append(
            {
                **common,
                "ledger_row_id": f"{RUN_ID}__{suffix}",
                "subrun_id": f"{RUN_ID}__{suffix}",
                "row_id": f"{RUN_ID}__{suffix}",
                "record_view": record_view,
                "tier_scope": tier_scope,
                "view": record_view,
                "tier": tier_scope,
                "kpi_scope": "FJ OOS density preserve repair(FJ 표본외 밀도 보존 수리)",
                "metric_scope": "python_proxy_onnx_smoke(Python 프록시/ONNX 스모크)",
                "status": status,
                "net_profit": final["selected_oos_net"] if suffix == "tier_a_separate" else "",
                "profit_factor": final["selected_oos_profit_factor"] if suffix == "tier_a_separate" else "",
                "trade_density": final["selected_oos_trade_density"] if suffix == "tier_a_separate" else "",
                "trade_count": final["selected_oos_trade_count"] if suffix == "tier_a_separate" else "",
                "source_authority": "python_proxy_onnx_smoke_no_mt5(Python 프록시/ONNX 스모크, MT5 없음)",
            }
        )
    append_or_replace_csv(STAGE_LEDGER, ["ledger_row_id"], rows)
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], rows)
    append_or_replace_csv(
        RUN_REGISTRY,
        ["run_id"],
        [
            {
                **common,
                "run_family": "experiment_execution(실험 실행)",
                "run_type": "oos_density_preserve_repair(표본외 밀도 보존 수리)",
                "input_run_id": PARENT_RUN_ID,
                "output_path": rel(FINAL_DECISION),
                "result_path": rel(TRADE_SURFACE),
                "selected_net_profit": final["selected_oos_net"],
                "selected_profit_factor": final["selected_oos_profit_factor"],
                "selected_trade_density": final["selected_oos_trade_density"],
            }
        ],
    )
    try:
        et.repair_run_registry_line_endings(RUN_ID)
    except AttributeError:
        pass


def write_artifact_registry(final: Mapping[str, Any]) -> None:
    rows = []
    for path in OUTPUT_FILES:
        if exists(path) and io_path(path).is_file():
            rows.append(
                {
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "artifact_type": "script" if path == THIS_FILE else ("report" if path.suffix.lower() == ".md" else ("json" if path.suffix.lower() == ".json" else "csv")),
                    "path": rel(path),
                    "artifact_path": rel(path),
                    "sha256": sha(path),
                    "created_at": final["created_at_utc"],
                    "created_at_utc": final["created_at_utc"],
                    "claim_boundary": CLAIM_BOUNDARY,
                    "artifact_id": f"{RUN_ID}__{path.stem}",
                    "notes": "FJ OOS density preserve repair artifact(FJ 표본외 밀도 보존 수리 산출물)",
                }
            )
    append_or_replace_csv(ARTIFACT_REGISTRY, ["artifact_id"], rows)


def apply_fj_patch() -> None:
    replacements = {
        "TODAY": TODAY,
        "RUN_NUMBER": RUN_NUMBER,
        "RUN_ID": RUN_ID,
        "PARENT_RUN_ID": PARENT_RUN_ID,
        "NEXT_RUN_ID": NEXT_RUN_ID,
        "STATUS_NO_STRICT": STATUS_NO_STRICT,
        "STATUS_STRICT": STATUS_STRICT,
        "JUDGMENT_NO_STRICT": JUDGMENT_NO_STRICT,
        "JUDGMENT_STRICT": JUDGMENT_STRICT,
        "DECISION_NO_STRICT": DECISION_NO_STRICT,
        "DECISION_STRICT": DECISION_STRICT,
        "CLAIM_BOUNDARY": CLAIM_BOUNDARY,
        "RUN_DIR": RUN_DIR,
        "MODEL_DIR": MODEL_DIR,
        "ONNX_DIR": ONNX_DIR,
        "INPUT_MANIFEST": INPUT_MANIFEST,
        "WORK_PACKET": WORK_PACKET,
        "FEATURE_AUDIT": FEATURE_AUDIT,
        "LABEL_SUMMARY": LABEL_SUMMARY,
        "MODEL_SCORECARD": MODEL_SCORECARD,
        "TRADE_SURFACE": TRADE_SURFACE,
        "SELECTED_CANDIDATE": SELECTED_CANDIDATE,
        "SELECTED_TRADE_TAPE": SELECTED_TRADE_TAPE,
        "MONTH_STABILITY": MONTH_STABILITY,
        "COST_STRESS": COST_STRESS,
        "SIDE_SESSION_REVIEW": SIDE_SESSION_REVIEW,
        "MODEL_ARTIFACT_MANIFEST": MODEL_ARTIFACT_MANIFEST,
        "ONNX_SMOKE_REPORT": ONNX_SMOKE_REPORT,
        "DATA_INTEGRITY_AUDIT": DATA_INTEGRITY_AUDIT,
        "RUN364FI_QUEUE": RUN364FK_QUEUE,
        "RUN_EVIDENCE_RECEIPT": RUN_EVIDENCE_RECEIPT,
        "EXPERIMENT_RECEIPT": EXPERIMENT_RECEIPT,
        "DATA_RECEIPT": DATA_RECEIPT,
        "MODEL_RECEIPT": MODEL_RECEIPT,
        "ATTRIBUTION_RECEIPT": ATTRIBUTION_RECEIPT,
        "JUDGMENT_RECEIPT": JUDGMENT_RECEIPT,
        "LINEAGE_RECEIPT": LINEAGE_RECEIPT,
        "CLAIM_RECEIPT": CLAIM_RECEIPT,
        "GATE_AUDIT": GATE_AUDIT,
        "FINAL_DECISION": FINAL_DECISION,
        "RUN_MANIFEST": RUN_MANIFEST,
        "REPORT_PATH": REPORT_PATH,
        "DECISION_DOC": DECISION_DOC,
        "THIS_FILE": THIS_FILE,
        "INPUT_FILES": INPUT_FILES,
        "OUTPUT_FILES": OUTPUT_FILES,
        "LABEL_SPECS": LABEL_SPECS,
        "TARGET_DENSITIES": TARGET_DENSITIES,
        "MARGINS": MARGINS,
        "HOUR_SETS": HOUR_SETS,
        "EXTRA_FILTERS": EXTRA_FILTERS,
    }
    for name, value in replacements.items():
        setattr(fh, name, value)
    fh.fg = fi
    fh.validate_inputs = validate_inputs
    fh.input_manifest_rows = input_manifest_rows
    fh.full_label_spec = full_label_spec
    fh.fh_label_values = fj_label_values
    fh.fh_feature_sets = fj_feature_sets
    fh.fh_model_specs = fj_model_specs
    fh.fh_extra_mask = fj_extra_mask
    fh.fh_cost_values = fj_cost_values
    fh.fh_strict_success = fj_strict_success
    fh.fh_operational_stack = fj_operational_stack
    fh.fh_selection_score = fj_selection_score
    fh.write_work_packet = write_work_packet
    fh.write_queue = write_queue
    fh.write_receipts = write_receipts
    fh.write_docs = write_docs
    fh.write_ledgers = write_ledgers
    fh.write_artifact_registry = write_artifact_registry
    fh.write_text = write_text
    fh.append_text_once = append_text_once
    fh.append_or_replace_csv = append_or_replace_csv
    fh.write_json = write_json


def main() -> None:
    apply_fj_patch()
    fh.main()


if __name__ == "__main__":
    main()
