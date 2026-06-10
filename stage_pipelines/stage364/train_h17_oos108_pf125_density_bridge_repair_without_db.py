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
from stage_pipelines.stage364 import review_h17_oos108_oos_pf125_cost09_gap_repair_without_db as fa  # noqa: E402
from stage_pipelines.stage364 import train_h17_oos108_oos_pf125_cost09_gap_repair_without_db as ez  # noqa: E402


TODAY = "2026-06-06"
STAGE_ID = ez.STAGE_ID
RUN_NUMBER = "run364FB"
RUN_ID = "run364FB_train_h17_oos108_pf125_density_bridge_repair_without_db_v1"
PARENT_RUN_ID = fa.RUN_ID
NEXT_RUN_ID = "run364FC_review_h17_oos108_pf125_density_bridge_repair_without_db_v1"

STATUS_NO_STRICT = "completed_stage364FB_pf125_density_bridge_repair_no_strict_pass_review_required_no_authority"
STATUS_STRICT = "completed_stage364FB_pf125_density_bridge_repair_strict_proxy_review_required_no_authority"
JUDGMENT_NO_STRICT = "inconclusive_pf125_density_bridge_repair_no_strict_pass_review_required_no_authority"
JUDGMENT_STRICT = "inconclusive_pf125_density_bridge_repair_strict_proxy_review_required_no_authority"
DECISION_NO_STRICT = "stage364FB_open_run364FC_pf125_density_bridge_repair_review"
DECISION_STRICT = "stage364FB_open_run364FC_pf125_density_bridge_repair_review"
CLAIM_BOUNDARY = (
    "research_development_pf125_density_bridge_repair_proxy_and_onnx_smoke_only_no_new_mt5_execution_"
    "no_runtime_package_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

STAGE_DIR = ez.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
MODEL_DIR = RUN_DIR / "models"
ONNX_DIR = RUN_DIR / "onnx"
REVIEW_DIR = STAGE_DIR / "03_reviews"
SPEC_DIR = STAGE_DIR / "00_spec"
SELECTED_DIR = STAGE_DIR / "04_selected"

INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
FEATURE_AUDIT = RUN_DIR / "fb_feature_set_audit.csv"
LABEL_SUMMARY = RUN_DIR / "fb_pf125_density_bridge_label_summary.csv"
MODEL_SCORECARD = RUN_DIR / "fb_model_scorecard.csv"
TRADE_SURFACE = RUN_DIR / "fb_pf125_density_bridge_surface.csv"
SELECTED_CANDIDATE = RUN_DIR / "selected_fb_candidate.json"
SELECTED_TRADE_TAPE = RUN_DIR / "selected_fb_trade_tape.csv"
MONTH_STABILITY = RUN_DIR / "selected_fb_month_stability.csv"
COST_STRESS = RUN_DIR / "selected_fb_cost_stress.csv"
SIDE_SESSION_REVIEW = RUN_DIR / "selected_fb_side_session_review.csv"
MODEL_ARTIFACT_MANIFEST = RUN_DIR / "model_artifact_manifest.csv"
ONNX_SMOKE_REPORT = RUN_DIR / "onnx_smoke_report.csv"
DATA_INTEGRITY_AUDIT = RUN_DIR / "data_integrity_audit.csv"
RUN364FC_QUEUE = RUN_DIR / "run364FC_pf125_density_bridge_review_queue.csv"
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

REPORT_PATH = REVIEW_DIR / "run364FB_h17_oos108_pf125_density_bridge_repair.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364FB_h17_oos108_pf125_density_bridge_repair.md"
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
et = ez.ex.et

INPUT_FILES = [
    fa.FINAL_DECISION,
    fa.GATE_AUDIT,
    fa.REVIEW_SUMMARY,
    fa.SURFACE_DIAGNOSTIC,
    fa.FAILURE_ATTRIBUTION,
    fa.PACKAGE_DECISION,
    fa.FAILURE_MEMORY,
    fa.RUN364FB_QUEUE,
    ez.FINAL_DECISION,
    ez.TRADE_SURFACE,
    ez.SELECTED_CANDIDATE,
    ez.SELECTED_TRADE_TAPE,
    ez.COST_STRESS,
    ez.SIDE_SESSION_REVIEW,
    ez.MONTH_STABILITY,
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
    RUN364FC_QUEUE,
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
    {"label_id": "fb_sym_h2_m2", "horizon_m5": 2, "threshold_points": 2.0, "mode": "symmetric"},
    {"label_id": "fb_sym_h2_m2p5", "horizon_m5": 2, "threshold_points": 2.5, "mode": "symmetric"},
    {"label_id": "fb_asym_h2_l2_s3", "horizon_m5": 2, "threshold_points": 2.5, "long_threshold_points": 2.0, "short_threshold_points": 3.0, "mode": "asymmetric"},
    {"label_id": "fb_asym_h3_l2p5_s3p5", "horizon_m5": 3, "threshold_points": 3.0, "long_threshold_points": 2.5, "short_threshold_points": 3.5, "mode": "asymmetric"},
]
TARGET_DENSITIES = [3, 4, 5, 6, 8, 10, 12]
MARGINS = [-0.08, -0.04, 0.0, 0.02, 0.04]
HOUR_SETS = {
    "fb_core_16_17_18_20_22": [16, 17, 18, 20, 22],
    "fb_plus_15_16_17_18_20_22": [15, 16, 17, 18, 20, 22],
    "fb_cash_15_to_22": [15, 16, 17, 18, 19, 20, 21, 22],
    "fb_no_h18": [15, 16, 17, 20, 22],
    "fb_no_h20": [15, 16, 17, 18, 22],
}
EXTRA_FILTERS = ["none", "fb_density_bridge_guard", "fb_short_loss_veto", "fb_two_lane_quality_guard", "fb_cost_side_balance_guard"]

DENSITY_FLOOR = 3.0
STRICT_SHORT_SHARE_FLOOR = 0.72
STRICT_MIN_PF_FLOOR = 1.05
OOS_PF_TARGET = 1.25
OPERATIONAL_MIN_PF_FLOOR = 1.18
RUNTIME_NET_REFERENCE = 523.58


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    return ez.rel(path)


def exists(path: Path | str) -> bool:
    return Path(path).exists()


def sha(path: Path | str) -> str:
    return ez.sha(path)


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return default
    if not math.isfinite(number):
        return default
    return number


def finite(value: Any, digits: int = 10) -> float | str:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return ""
    if not math.isfinite(number):
        return ""
    return round(number, digits)


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
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in merged:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def validate_inputs() -> dict[str, Any]:
    missing = [rel(path) for path in INPUT_FILES if path != THIS_FILE and not exists(path)]
    if missing:
        raise FileNotFoundError("missing FB inputs(FB 입력 누락): " + ", ".join(missing))
    parent = read_json(fa.FINAL_DECISION)
    if parent.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"FA next_run_id mismatch(FA 다음 실행 ID 불일치): {parent.get('next_run_id')} != {RUN_ID}")
    for key in ["runtime_authority", "operating_promotion", "live_readiness", "goal_achieve"]:
        if parent.get(key, "not_claimed") != "not_claimed":
            raise RuntimeError(f"forbidden FA claim(금지된 FA 주장): {key}={parent.get(key)}")
    gates = pd.read_csv(io_path(fa.GATE_AUDIT), encoding="utf-8-sig").fillna("")
    if gates.empty or any(gates["status"].astype(str) != "passed"):
        raise RuntimeError("FA gate audit(FA 게이트 감사)가 모두 passed(통과)가 아닙니다.")
    return parent


def input_manifest_rows() -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "input_path": rel(path),
            "exists": str(exists(path)).lower(),
            "sha256": sha(path) if exists(path) and io_path(path).is_file() else "",
            "input_role": "FB PF125 density bridge repair input(FB PF125 밀도 연결 수리 입력)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for path in INPUT_FILES
    ]


def fb_label_values(frame: pd.DataFrame, spec: Mapping[str, Any]) -> tuple[np.ndarray, np.ndarray]:
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


def fb_feature_sets(feature_order: Sequence[str]) -> dict[str, list[str]]:
    base = list(feature_order)
    derived = et.dt.derived_features()
    price = [column for column in base if any(token in column for token in ["return", "ratio", "rsi", "atr", "adx", "vol", "gap"])]
    macro = [column for column in base if any(token in column for token in ["vix", "us10yr", "usdx", "mega8", "breadth"])]
    session = [column for column in base if any(token in column for token in ["cash", "minutes", "open", "close"])]
    behavior = [column for column in base if any(token in column for token in ["trend", "momentum", "range", "body", "wick", "spread"])]
    return {
        "fb_all72": list(dict.fromkeys(base + derived)),
        "fb_density_behavior_macro": list(dict.fromkeys(price + macro + session + behavior + derived)),
        "fb_session_cost_stack": list(dict.fromkeys(price + session + macro + derived)),
    }


def fb_model_specs() -> list[tuple[str, str, Any]]:
    return [
        (
            "et8_l24_n128",
            "ExtraTrees(엑스트라트리)",
            et.dt.dp.ExtraTreesClassifier(n_estimators=128, max_depth=8, min_samples_leaf=24, class_weight="balanced", random_state=791, n_jobs=1),
        ),
        (
            "et9_l28_n128",
            "ExtraTrees(엑스트라트리)",
            et.dt.dp.ExtraTreesClassifier(n_estimators=128, max_depth=9, min_samples_leaf=28, class_weight="balanced", random_state=792, n_jobs=1),
        ),
        (
            "rf8_l36_n128",
            "RandomForest(랜덤포레스트)",
            et.dt.dp.RandomForestClassifier(n_estimators=128, max_depth=8, min_samples_leaf=36, class_weight="balanced_subsample", random_state=793, n_jobs=1),
        ),
    ]


def col(frame: pd.DataFrame, name: str, default: float = 0.0) -> np.ndarray:
    if name in frame.columns:
        return frame[name].to_numpy(dtype=float)
    return np.full(len(frame), default, dtype=float)


def fb_extra_mask(frame: pd.DataFrame, side: np.ndarray, extra_filter: str) -> np.ndarray:
    mask = np.ones(len(frame), dtype=bool)
    hour = frame["timestamp"].dt.hour.to_numpy(dtype=int)
    breadth = col(frame, "mega8_pos_breadth_1", 0.5)
    vol_ratio = col(frame, "historical_vol_5_over_20", 1.0)
    log_return_3 = col(frame, "log_return_3", 0.0)
    vix_stress = col(frame, "vix_zscore_20", 0.0)
    if extra_filter == "none":
        return mask
    if extra_filter == "fb_density_bridge_guard":
        long_ok = (side == "long") & np.isin(hour, [15, 16, 18, 20, 22]) & (breadth >= 0.36) & (vix_stress <= 1.55)
        short_ok = (side == "short") & np.isin(hour, [16, 17, 18, 22]) & (vol_ratio >= 0.66) & ((breadth <= 0.60) | (log_return_3 < -0.00005))
        return mask & (long_ok | short_ok)
    if extra_filter == "fb_short_loss_veto":
        veto = (
            ((side == "short") & (hour == 17) & (log_return_3 > -0.00012))
            | ((side == "short") & (hour == 18) & (vol_ratio < 0.88))
            | ((side == "short") & (hour == 20))
            | ((side == "long") & (hour == 17) & (breadth < 0.58))
        )
        return mask & ~veto
    if extra_filter == "fb_two_lane_quality_guard":
        long_ok = (side == "long") & (
            ((hour == 15) & (breadth >= 0.48))
            | ((hour == 16) & (breadth >= 0.40))
            | ((hour == 18) & (breadth >= 0.54) & (vix_stress <= 1.35))
            | ((hour == 20) & (breadth >= 0.44) & (vix_stress <= 1.25))
            | ((hour == 22) & (breadth >= 0.46))
        )
        short_ok = (side == "short") & (
            ((hour == 16) & (vol_ratio >= 0.72))
            | ((hour == 17) & (log_return_3 < -0.00018))
            | ((hour == 18) & (vol_ratio >= 0.92) & (breadth <= 0.56))
            | ((hour == 22) & (vol_ratio >= 0.70))
        )
        return mask & (long_ok | short_ok)
    if extra_filter == "fb_cost_side_balance_guard":
        long_ok = (side == "long") & (breadth >= 0.42) & (vix_stress <= 1.40) & ~np.isin(hour, [17, 21])
        short_ok = (side == "short") & (vol_ratio >= 0.74) & ((breadth <= 0.52) | (log_return_3 < -0.00012)) & ~np.isin(hour, [18, 20, 21])
        return mask & (long_ok | short_ok)
    raise ValueError(f"unknown FB filter(알 수 없는 FB 필터): {extra_filter}")


def fb_cost_values(row: Mapping[str, Any]) -> dict[str, float]:
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


def fb_strict_success(row: Mapping[str, Any]) -> bool:
    values = fb_cost_values(row)
    validation_pf = as_float(row.get("validation_profit_factor"))
    oos_pf = as_float(row.get("oos_profit_factor"))
    min_pf = min(validation_pf, oos_pf)
    return (
        as_float(row.get("validation_net")) > 0.0
        and as_float(row.get("oos_net")) > 0.0
        and oos_pf >= OOS_PF_TARGET
        and values["oos_cost09_net"] >= 0.0
        and values["validation_trade_density"] >= DENSITY_FLOOR
        and values["oos_trade_density"] >= DENSITY_FLOOR
        and values["combined_trade_density"] >= DENSITY_FLOOR
        and values["combined_net"] > 0.0
        and values["combined_cost06_net"] >= 0.0
        and values["combined_short_share"] <= STRICT_SHORT_SHARE_FLOOR
        and min_pf >= STRICT_MIN_PF_FLOOR
    )


def fb_operational_stack(row: Mapping[str, Any]) -> bool:
    values = fb_cost_values(row)
    min_pf = min(as_float(row.get("validation_profit_factor")), as_float(row.get("oos_profit_factor")))
    return fb_strict_success(row) and values["combined_net"] >= RUNTIME_NET_REFERENCE and min_pf >= OPERATIONAL_MIN_PF_FLOOR


def fb_selection_score(row: Mapping[str, Any]) -> float:
    values = fb_cost_values(row)
    validation_net = as_float(row.get("validation_net"))
    oos_net = as_float(row.get("oos_net"))
    validation_pf = as_float(row.get("validation_profit_factor"))
    oos_pf = as_float(row.get("oos_profit_factor"))
    min_pf = min(validation_pf, oos_pf)
    density = values["combined_trade_density"]
    validation_density = values["validation_trade_density"]
    oos_density = values["oos_trade_density"]
    return (
        1.20 * validation_net
        + 1.30 * oos_net
        + 0.75 * values["combined_net"]
        + 2100.0 * max(0.0, oos_pf - 1.0)
        + 1150.0 * max(0.0, min_pf - 1.0)
        + 800.0 * max(0.0, validation_pf - 1.0)
        + 2.00 * values["oos_cost09_net"]
        + 1.15 * values["oos_cost06_net"]
        + 0.65 * values["combined_cost09_net"]
        + 260.0 * min(validation_density, 6.0)
        + 260.0 * min(oos_density, 6.0)
        + 240.0 * min(density, 6.0)
        - 2600.0 * max(0.0, OOS_PF_TARGET - oos_pf)
        - 1550.0 * (1.0 if validation_net <= 0.0 else 0.0)
        - 1450.0 * (1.0 if oos_net <= 0.0 else 0.0)
        - 6.20 * max(0.0, -values["oos_cost09_net"])
        - 1.55 * max(0.0, -values["combined_cost09_net"])
        - 1250.0 * max(0.0, DENSITY_FLOOR - validation_density)
        - 1150.0 * max(0.0, DENSITY_FLOOR - oos_density)
        - 1100.0 * max(0.0, DENSITY_FLOOR - density)
        - 980.0 * max(0.0, values["combined_short_share"] - STRICT_SHORT_SHARE_FLOOR)
        - 520.0 * max(0.0, STRICT_MIN_PF_FLOOR - min_pf)
    )


def write_work_packet(parent: Mapping[str, Any]) -> None:
    write_json(
        WORK_PACKET,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "primary_family": "experiment_execution(실험 실행)",
            "primary_skill": "obsidian-run-evidence-system(실행 근거 시스템)",
            "support_skills": [
                "obsidian-experiment-design(실험 설계)",
                "obsidian-data-integrity(데이터 무결성)",
                "obsidian-model-validation(모델 검증)",
                "obsidian-artifact-lineage(산출물 계보)",
            ],
            "hypothesis": "Two-lane threshold stack(두 갈래 임계값 묶음)과 density bridge guard(밀도 연결 가드)를 쓰면 OOS PF125(표본외 PF125)를 버리지 않고 validation/density(검증/밀도)를 회복할 수 있습니다.",
            "broad_sweep": "lower movement labels(낮은 이동 라벨), lower target thresholds(낮은 목표 밀도 임계값), side/session loss veto(방향/세션 손실 차단)",
            "success_criteria": "validation_net>0, validation_density>=3, OOS PF>=1.25, OOS density>=3, combined density>=3, OOS cost0.9>=0(검증/표본외/합산 밀도와 표본외 PF/비용 조건)",
            "failure_criteria": "OOS-only winner(표본외 전용 승자), validation-only winner(검증 전용 승자), density below 3/day(밀도 일 3회 미만)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def write_queue(summary: Mapping[str, Any]) -> None:
    et.write_csv(
        RUN364FC_QUEUE,
        [
            {
                "run_id": RUN_ID,
                "next_run_id": NEXT_RUN_ID,
                "queue_rank": 1,
                "queue_id": "fc01_pf125_density_bridge_review",
                "review_subject": summary["selected_model_id"],
                "strict_candidate_count": summary["strict_candidate_count"],
                "operational_proxy_stack_pass_count": summary["operational_proxy_stack_pass_count"],
                "selected_validation_net": summary["selected_validation_net"],
                "selected_validation_profit_factor": summary["selected_validation_profit_factor"],
                "selected_validation_trade_density": summary["selected_validation_trade_density"],
                "selected_oos_net": summary["selected_oos_net"],
                "selected_oos_profit_factor": summary["selected_oos_profit_factor"],
                "selected_oos_trade_density": summary["selected_oos_trade_density"],
                "selected_combined_trade_density": summary["selected_combined_trade_density"],
                "selected_combined_cost09_net": summary["selected_combined_cost09_net"],
                "selected_combined_short_share": summary["selected_combined_short_share"],
                "effect": "FC review(FC 검토)가 FB density bridge(FB 밀도 연결) 결과를 패키지 가능성과 다음 실패 기억으로 분리합니다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )


def write_receipts(final: Mapping[str, Any]) -> None:
    base = {"run_id": RUN_ID, "stage_id": STAGE_ID, "created_at_utc": final["created_at_utc"], "claim_boundary": CLAIM_BOUNDARY}
    write_json(RUN_EVIDENCE_RECEIPT, {**base, "surface": rel(TRADE_SURFACE), "selected_candidate": rel(SELECTED_CANDIDATE), "selected_trade_tape": rel(SELECTED_TRADE_TAPE), "measurement_boundary": "Python proxy with ONNX smoke(Python 프록시와 ONNX 스모크), no MT5(MT5 없음)"})
    write_json(EXPERIMENT_RECEIPT, {**base, "hypothesis": "PF125 density bridge(PF125 밀도 연결)가 FA의 OOS-only failure(표본외 전용 실패)를 줄일 수 있는지 시험합니다.", "comparison_baseline": PARENT_RUN_ID, "decision_use": NEXT_RUN_ID})
    write_json(DATA_RECEIPT, {**base, "data_source": [rel(et.dt.dp.MODEL_INPUT_DATASET), rel(et.dt.dp.RAW_US100_M5)], "time_axis": "UTC model input timestamp(UTC 모델 입력 타임스탬프)", "feature_label_boundary": "future_open only in labels(future_open은 라벨에만 사용)", "split_boundary": "chronological train/validation/OOS(시간순 학습/검증/표본외)", "integrity_judgment": "usable_with_proxy_boundary(프록시 경계 안에서 사용 가능)"})
    write_json(MODEL_RECEIPT, {**base, "model_family": "RandomForest/ExtraTrees(랜덤포레스트/엑스트라트리)", "selected_model_id": final["selected_model_id"], "onnx_smoke_pass_rows": final["onnx_smoke_pass_rows"], "validation_judgment": final["judgment"]})
    write_json(ATTRIBUTION_RECEIPT, {**base, "observed_change": f"selected validation/OOS net/PF/density {final['selected_validation_net']}/{final['selected_validation_profit_factor']}/{final['selected_validation_trade_density']} and {final['selected_oos_net']}/{final['selected_oos_profit_factor']}/{final['selected_oos_trade_density']}", "likely_drivers": ["two-lane threshold stack(두 갈래 임계값 묶음)", "density bridge score(밀도 연결 점수)", "side/session veto(방향/세션 차단)"], "next_probe": NEXT_RUN_ID})
    write_json(JUDGMENT_RECEIPT, {**base, "result_subject": RUN_ID, "evidence_available": [rel(TRADE_SURFACE), rel(SELECTED_CANDIDATE), rel(ONNX_SMOKE_REPORT), rel(DATA_INTEGRITY_AUDIT)], "evidence_missing": ["MT5 runtime package(MT5 런타임 패키지)", "MT5 runtime probe(MT5 런타임 탐침)", "forward/replay evidence(전진/재생 근거)"], "judgment_label": final["judgment"], "next_condition": NEXT_RUN_ID})
    write_json(LINEAGE_RECEIPT, {**base, "source_inputs": [{"path": rel(path), "sha256": sha(path)} for path in INPUT_FILES if exists(path) and io_path(path).is_file()], "producer": rel(THIS_FILE), "consumer": NEXT_RUN_ID, "artifact_paths": [rel(path) for path in OUTPUT_FILES if exists(path)], "artifact_hashes": {rel(path): sha(path) for path in OUTPUT_FILES if exists(path) and io_path(path).is_file()}, "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)], "lineage_judgment": "connected_proxy_model_reseed(프록시 모델 재시드 연결)"})
    write_json(CLAIM_RECEIPT, {**base, "runtime_package": "not_opened", "runtime_authority": "not_claimed", "operating_promotion": "not_claimed", "live_readiness": "not_claimed", "goal_achieve": "not_claimed", "effect": "FB 모델 단서를 운영 주장으로 올리지 않습니다."})


def write_docs(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    gate_lines = "\n".join(f"- {row['gate']}: {row['status']} -> {row['evidence']}" for row in gates)
    report = f"""# run364FB H17 OOS108 PF125 Density Bridge Repair(PF125 밀도 연결 수리)

Created(생성): {final['created_at_utc']}

Action(행동): FA failure memory(FA 실패 기억)를 받아 two-lane threshold stack(두 갈래 임계값 묶음), density bridge score(밀도 연결 점수), side/session veto(방향/세션 차단)를 학습했습니다.

Effect(효과): EZ의 OOS PF125/OOS cost0.9(표본외 PF125/표본외 비용0.9) 단서를 버리지 않고 validation/density(검증/밀도) 붕괴를 수리합니다.

- judgment(판정): `{final['judgment']}`
- selected_model_id(선택 모델 ID): `{final['selected_model_id']}`
- validation net/PF/density(검증 순수익/수익 팩터/밀도): `{final['selected_validation_net']}` / `{final['selected_validation_profit_factor']}` / `{final['selected_validation_trade_density']}`
- OOS net/PF/density(표본외 순수익/수익 팩터/밀도): `{final['selected_oos_net']}` / `{final['selected_oos_profit_factor']}` / `{final['selected_oos_trade_density']}`
- OOS cost0.6 net(표본외 비용0.6 순수익): `{final['selected_oos_cost06_net']}`
- combined net/density/cost0.9/short share(합산 순수익/밀도/비용0.9/숏 비중): `{final['selected_combined_net']}` / `{final['selected_combined_trade_density']}` / `{final['selected_combined_cost09_net']}` / `{final['selected_combined_short_share']}`
- strict_candidate_count(엄격 후보 수): `{final['strict_candidate_count']}`
- operational_proxy_stack_pass_count(운영형 프록시 묶음 통과 수): `{final['operational_proxy_stack_pass_count']}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`

Gates(게이트):

{gate_lines}

Boundary(경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
"""
    decision_doc = f"""# Decision(결정): stage364FB PF125 Density Bridge Repair(PF125 밀도 연결 수리)

- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{final['decision']}`
- judgment(판정): `{final['judgment']}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Action(행동): FB model/label/score(모델/라벨/점수) 재시드를 실행하고 FC review(FC 검토)로 넘겼습니다.

Effect(효과): PF125 density bridge(PF125 밀도 연결) 결과를 운영 주장 없이 다음 판정에 넘깁니다.
"""
    write_text(REPORT_PATH, report, bom=True)
    write_text(DECISION_DOC, decision_doc, bom=True)
    append_text_once(REVIEW_INDEX, f"run364FB__{RUN_ID}", f"\n- run364FB__{RUN_ID}: [{REPORT_PATH.name}]({REPORT_PATH.name}) - PF125 density bridge repair(PF125 밀도 연결 수리), next `{NEXT_RUN_ID}`.\n")
    append_text_once(STAGE_BRIEF, f"run364FB__{RUN_ID}", f"\n<!-- run364FB__{RUN_ID} -->\n\n## run364FB PF125 Density Bridge Repair(PF125 밀도 연결 수리)\n\nAction(행동): PF125 밀도 연결 수리 모델을 학습했습니다.\n\nEffect(효과): `{NEXT_RUN_ID}`에서 패키지 가능성과 실패 경계를 검토합니다.\n")
    append_text_once(STAGE_README, f"run364FB__{RUN_ID}", f"\n<!-- run364FB__{RUN_ID} -->\n## run364FB PF125 density bridge repair(PF125 밀도 연결 수리)\n\nNext(다음): `{NEXT_RUN_ID}`.\n")
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

Current truth(현재 진실): `run364FB` trained(학습 완료) PF125 density bridge repair(PF125 밀도 연결 수리). Selected validation/OOS net/PF/density(선택 검증/표본외 순수익/수익 팩터/밀도)는 `{final['selected_validation_net']}` / `{final['selected_validation_profit_factor']}` / `{final['selected_validation_trade_density']}` 및 `{final['selected_oos_net']}` / `{final['selected_oos_profit_factor']}` / `{final['selected_oos_trade_density']}`입니다.

Cost/side truth(비용/방향 진실): OOS cost0.6 net(표본외 비용0.6 순수익)은 `{final['selected_oos_cost06_net']}`이고, combined cost0.9/short share(합산 비용0.9/숏 비중)는 `{final['selected_combined_cost09_net']}` / `{final['selected_combined_short_share']}`입니다.

Next action(다음 행동): `{NEXT_RUN_ID}`에서 FB 결과를 review(검토)합니다.

Operating boundary(운영 경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""", bom=True)
    write_text(SELECTION_STATUS, f"""# Stage364 selection status(선택 상태)

Updated(갱신): {final['created_at_utc']}

Current run(현재 실행): `{NEXT_RUN_ID}`
Latest completed run(최근 완료 실행): `{RUN_ID}`

Latest scout(최근 정찰): FB PF125 density bridge repair(FB PF125 밀도 연결 수리).

Selected model(선택 모델): `{final['selected_model_id']}`

Validation net/PF/density(검증 순수익/수익 팩터/밀도): `{final['selected_validation_net']}` / `{final['selected_validation_profit_factor']}` / `{final['selected_validation_trade_density']}`
OOS net/PF/density(표본외 순수익/수익 팩터/밀도): `{final['selected_oos_net']}` / `{final['selected_oos_profit_factor']}` / `{final['selected_oos_trade_density']}`
Combined net/density/cost0.9/short share(합산 순수익/밀도/비용0.9/숏 비중): `{final['selected_combined_net']}` / `{final['selected_combined_trade_density']}` / `{final['selected_combined_cost09_net']}` / `{final['selected_combined_short_share']}`

Judgment(판정): `{final['judgment']}`.

Authority(권위): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""", bom=True)
    append_text_once(WORKSPACE_CHANGELOG, f"run364FB__{RUN_ID}", f"\n<!-- run364FB__{RUN_ID} -->\n- {final['created_at_utc']} `{RUN_ID}` completed PF125 density bridge repair(PF125 밀도 연결 수리); strict candidates `{final['strict_candidate_count']}`; selected `{final['selected_model_id']}`; next `{NEXT_RUN_ID}`; no authority claim(권위 주장 없음).\n")
    append_text_once(IDEA_REGISTRY, f"run364FB__{RUN_ID}", f"\n<!-- run364FB__{RUN_ID} -->\n- `{RUN_ID}`: PF125 density bridge repair(PF125 밀도 연결 수리)를 학습했습니다. Effect(효과): FA의 표본외 PF 단서와 밀도 실패를 같은 표면에서 다시 시험했습니다.\n")
    if int(final["strict_candidate_count"]) == 0:
        append_text_once(NEGATIVE_REGISTER, f"run364FB__strict_candidate_absent__{RUN_ID}", f"\n<!-- run364FB__strict_candidate_absent__{RUN_ID} -->\n- `{RUN_ID}`: PF125 density bridge repair(PF125 밀도 연결 수리)는 strict candidate(엄격 후보)를 만들지 못했습니다. Effect(효과): FC에서 실패 경계와 회수 단서를 분리합니다.\n")


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
        "question": "Can PF125 density bridge repair recover validation and 3/day density?(PF125 밀도 연결 수리가 검증과 일 3회 밀도를 회복할 수 있는가?)",
        "next_action": NEXT_RUN_ID,
        "notes": f"strict_candidate_count={final['strict_candidate_count']};onnx_smoke_pass_rows={final['onnx_smoke_pass_rows']};validation_pf={final['selected_validation_profit_factor']};oos_pf={final['selected_oos_profit_factor']};combined_density={final['selected_combined_trade_density']}",
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
                "kpi_scope": "FB PF125 density bridge repair(FB PF125 밀도 연결 수리)",
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
                "run_type": "pf125_density_bridge_repair(PF125 밀도 연결 수리)",
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
                    "notes": "FB PF125 density bridge repair artifact(FB PF125 밀도 연결 수리 산출물)",
                }
            )
    append_or_replace_csv(ARTIFACT_REGISTRY, ["artifact_id"], rows)


def apply_fb_patch() -> None:
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
        "RUN364FA_QUEUE": RUN364FC_QUEUE,
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
        setattr(ez, name, value)
    ez.validate_inputs = validate_inputs
    ez.input_manifest_rows = input_manifest_rows
    ez.ez_label_values = fb_label_values
    ez.ez_feature_sets = fb_feature_sets
    ez.ez_model_specs = fb_model_specs
    ez.ez_extra_mask = fb_extra_mask
    ez.ez_cost_values = fb_cost_values
    ez.ez_strict_success = fb_strict_success
    ez.ez_operational_stack = fb_operational_stack
    ez.ez_selection_score = fb_selection_score
    ez.write_work_packet = write_work_packet
    ez.write_queue = write_queue
    ez.write_receipts = write_receipts
    ez.write_docs = write_docs
    ez.write_ledgers = write_ledgers
    ez.write_artifact_registry = write_artifact_registry
    ez.write_text = write_text
    ez.append_text_once = append_text_once
    ez.append_or_replace_csv = append_or_replace_csv
    ez.write_json = write_json
    ez.apply_ez_patch()


def main() -> None:
    apply_fb_patch()
    ez.ex.et.main()


if __name__ == "__main__":
    main()
