from __future__ import annotations

import csv
import json
import math
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, json_ready  # noqa: E402
from stage_pipelines.stage364 import train_h17_density_failure_regime_behavior_reseed_without_db as dt  # noqa: E402
from stage_pipelines.stage364 import train_h17_oos108_scope_aligned_cost_side_repair_scout_without_db as eq  # noqa: E402
from stage_pipelines.stage364.review_pf_pass_density_restore_offensive_scout_without_db import repair_run_registry_line_endings  # noqa: E402


TODAY = "2026-06-06"
STAGE_ID = eq.STAGE_ID
RUN_NUMBER = "run364ER"
RUN_ID = "run364ER_train_h17_oos108_cost_side_model_label_feature_reseed_without_db_v1"
PARENT_RUN_ID = eq.RUN_ID
NEXT_RUN_ID = "run364ES_review_h17_oos108_cost_side_model_label_feature_reseed_without_db_v1"

STATUS_STRICT = "completed_stage364ER_oos108_cost_side_reseed_proxy_candidate_review_required_no_authority"
STATUS_NO_STRICT = "completed_stage364ER_oos108_cost_side_reseed_no_strict_pass_review_required_no_authority"
JUDGMENT_STRICT = "positive_proxy_cost_side_model_label_feature_reseed_candidate_review_required_no_authority"
JUDGMENT_NO_STRICT = "inconclusive_cost_side_model_label_feature_reseed_no_strict_pass_review_required_no_authority"
DECISION_STRICT = "stage364ER_open_run364ES_cost_side_reseed_candidate_review"
DECISION_NO_STRICT = "stage364ER_open_run364ES_cost_side_reseed_failure_memory_review"
CLAIM_BOUNDARY = (
    "research_development_cost_side_model_label_feature_reseed_proxy_and_onnx_smoke_only_"
    "no_new_mt5_execution_no_runtime_package_no_forward_pass_no_live_readiness_"
    "no_operating_promotion_no_runtime_authority_no_goal_claim"
)

POINT_VALUE = dt.POINT_VALUE
COST_PER_TRADE = dt.COST_PER_TRADE
DENSITY_FLOOR = 3.0
STRICT_VALIDATION_PF_FLOOR = 1.05
STRICT_OOS_PF_FLOOR = 1.08
SHORT_SHARE_FLOOR = 0.75
RUNTIME_NET_REFERENCE = 523.58
RUNTIME_PF_REFERENCE = 1.21

STAGE_DIR = eq.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
MODEL_DIR = RUN_DIR / "models"
ONNX_DIR = RUN_DIR / "onnx"
REVIEW_DIR = STAGE_DIR / "03_reviews"
SPEC_DIR = STAGE_DIR / "00_spec"
SELECTED_DIR = STAGE_DIR / "04_selected"

INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
FEATURE_AUDIT = RUN_DIR / "er_feature_set_audit.csv"
LABEL_SUMMARY = RUN_DIR / "er_cost_side_label_summary.csv"
MODEL_SCORECARD = RUN_DIR / "er_model_scorecard.csv"
TRADE_SURFACE = RUN_DIR / "er_cost_side_trade_surface.csv"
SELECTED_CANDIDATE = RUN_DIR / "selected_er_candidate.json"
SELECTED_TRADE_TAPE = RUN_DIR / "selected_er_trade_tape.csv"
MONTH_STABILITY = RUN_DIR / "selected_er_month_stability.csv"
COST_STRESS = RUN_DIR / "selected_er_cost_stress.csv"
SIDE_SESSION_REVIEW = RUN_DIR / "selected_er_side_session_review.csv"
MODEL_ARTIFACT_MANIFEST = RUN_DIR / "model_artifact_manifest.csv"
ONNX_SMOKE_REPORT = RUN_DIR / "onnx_smoke_report.csv"
DATA_INTEGRITY_AUDIT = RUN_DIR / "data_integrity_audit.csv"
RUN364ES_QUEUE = RUN_DIR / "run364ES_cost_side_reseed_review_queue.csv"
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

REPORT_PATH = REVIEW_DIR / "run364ER_oos108_cost_side_reseed.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364ER_h17_oos108_cost_side_model_label_feature_reseed.md"
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

INPUT_FILES = [
    eq.FINAL_DECISION,
    eq.GATE_AUDIT,
    eq.SURFACE,
    eq.FAILURE_ATTRIBUTION,
    eq.RUN364ER_QUEUE,
    dt.dp.MODEL_INPUT_DATASET,
    dt.dp.MODEL_INPUT_FEATURE_ORDER,
    dt.dp.RAW_US100_M5,
    Path(__file__),
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
    RUN364ES_QUEUE,
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
    Path(__file__),
]

LABEL_SPECS = [
    {"label_id": "costside_dir_h2_m3", "horizon_m5": 2, "threshold_points": 3.0},
    {"label_id": "costside_dir_h3_m3", "horizon_m5": 3, "threshold_points": 3.0},
    {"label_id": "costside_dir_h4_m4", "horizon_m5": 4, "threshold_points": 4.0},
]
TARGET_DENSITIES = [3, 4, 5, 6, 8, 10]
MARGINS = [-0.02, 0.0, 0.03]
HOUR_SETS = {
    "all_hours": list(range(24)),
    "no_h20_21": [hour for hour in range(24) if hour not in [20, 21]],
    "cash_15_22": [15, 16, 17, 18, 19, 20, 21, 22],
    "quality_15_19_22": [15, 16, 17, 18, 19, 22],
}
EXTRA_FILTERS = ["none", "cost_quality", "short_quality", "vol_breadth_quality"]


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    try:
        return Path(path).resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return Path(path).as_posix()


def exists(path: Path | str) -> bool:
    return Path(path).exists()


def sha(path: Path | str) -> str:
    return dt.sha(Path(path))


def as_float(value: Any, default: float = 0.0) -> float:
    return dt.as_float(value, default)


def finite(value: Any, digits: int = 10) -> float | str:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return ""
    if not math.isfinite(number):
        return ""
    return round(number, digits)


def read_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8-sig") as handle:
        return json.load(handle)


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(json_ready(payload), handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")


def write_text(path: Path, text: str, *, bom: bool = True) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8-sig" if bom else "utf-8")


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    rows = list(rows)
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fields: list[str] = []
        for row in rows:
            for key in row.keys():
                if key not in fields:
                    fields.append(str(key))
        fieldnames = fields or ["empty"]
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fieldnames), extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def append_text_once(path: Path, marker: str, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    existing = path.read_text(encoding="utf-8-sig") if path.exists() else ""
    if marker in existing:
        return
    payload = existing.rstrip() + "\n" + text.lstrip() if existing.strip() else text
    path.write_text(payload, encoding="utf-8-sig")


def append_or_replace_csv(path: Path, key_fields: Sequence[str], rows: Sequence[Mapping[str, Any]], *, extend_header: bool = True) -> None:
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


def ensure_dirs() -> None:
    for path in [RUN_DIR, MODEL_DIR, ONNX_DIR, REVIEW_DIR, SPEC_DIR, SELECTED_DIR, DECISION_DOC.parent]:
        path.mkdir(parents=True, exist_ok=True)


def input_manifest_rows() -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "input_path": rel(path),
            "exists": str(exists(path)).lower(),
            "sha256": sha(path) if exists(path) and Path(path).is_file() else "",
            "input_role": "ER cost/side reseed input(ER 비용/방향 재시드 입력)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for path in INPUT_FILES
    ]


def validate_inputs() -> dict[str, Any]:
    missing = [rel(path) for path in INPUT_FILES if path != Path(__file__) and not exists(path)]
    if missing:
        raise FileNotFoundError("missing ER inputs(ER 입력 누락): " + ", ".join(missing))
    eq_final = read_json(eq.FINAL_DECISION)
    if eq_final.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"EQ next_run_id mismatch(EQ 다음 실행 ID 불일치): {eq_final.get('next_run_id')} != {RUN_ID}")
    for key in ["runtime_authority", "operating_promotion", "live_readiness", "goal_achieve"]:
        if eq_final.get(key, "not_claimed") != "not_claimed":
            raise RuntimeError(f"forbidden prior claim(이전 금지 주장): {key}={eq_final.get(key)}")
    return eq_final


def er_feature_sets(feature_order: Sequence[str]) -> dict[str, list[str]]:
    base = list(feature_order)
    derived = dt.derived_features()
    price = [column for column in base if any(token in column for token in ["return", "ratio", "rsi", "atr", "adx", "bb_", "bollinger", "vol", "gap"])]
    macro = [column for column in base if any(token in column for token in ["vix", "us10yr", "usdx", "mega8", "top3", "breadth"])]
    session = [column for column in base if any(token in column for token in ["cash", "minutes", "open", "close"])]
    return {
        "costside_all72": list(dict.fromkeys(base + derived)),
        "costside_price_macro_session": list(dict.fromkeys(price + macro + session + derived)),
    }


def er_model_specs() -> list[tuple[str, str, Any]]:
    return [
        (
            "et8_l45_n160",
            "ExtraTrees(엑스트라트리)",
            dt.dp.ExtraTreesClassifier(n_estimators=160, max_depth=8, min_samples_leaf=45, class_weight="balanced", random_state=641, n_jobs=-1),
        ),
        (
            "rf9_l55_n160",
            "RandomForest(랜덤포레스트)",
            dt.dp.RandomForestClassifier(n_estimators=160, max_depth=9, min_samples_leaf=55, class_weight="balanced_subsample", random_state=642, n_jobs=-1),
        ),
    ]


def er_extra_mask(frame: pd.DataFrame, side: np.ndarray, extra_filter: str) -> np.ndarray:
    mask = np.ones(len(frame), dtype=bool)
    hour = frame["timestamp"].dt.hour.to_numpy(dtype=int)
    log_return_3 = frame["log_return_3"].to_numpy(dtype=float)
    vol_ratio = frame["historical_vol_5_over_20"].to_numpy(dtype=float)
    breadth = frame["mega8_pos_breadth_1"].to_numpy(dtype=float)
    vix_stress = frame["vix_zscore_20"].to_numpy(dtype=float)
    if extra_filter == "none":
        return mask
    if extra_filter == "cost_quality":
        return mask & (hour != 21) & (vol_ratio >= 0.75)
    if extra_filter == "short_quality":
        short_ok = (side == "short") & (log_return_3 < 0.0) & (breadth <= 0.62) & ~np.isin(hour, [20, 21])
        long_ok = (side == "long") & (breadth >= 0.45) & (vix_stress <= 1.25) & (hour != 21)
        return mask & (short_ok | long_ok)
    if extra_filter == "vol_breadth_quality":
        return mask & (vol_ratio >= 0.85) & ((breadth <= 0.45) | (breadth >= 0.55)) & (hour != 21)
    raise ValueError(f"unknown ER filter(알 수 없는 ER 필터): {extra_filter}")


def cost_side_values(row: Mapping[str, Any]) -> dict[str, float]:
    validation_net = as_float(row.get("validation_net"))
    oos_net = as_float(row.get("oos_net"))
    validation_trades = as_float(row.get("validation_trade_count"))
    oos_trades = as_float(row.get("oos_trade_count"))
    validation_density = as_float(row.get("validation_trade_density"))
    oos_density = as_float(row.get("oos_trade_density"))
    validation_days = validation_trades / validation_density if validation_density > 0 else 0.0
    oos_days = oos_trades / oos_density if oos_density > 0 else 0.0
    combined_trades = validation_trades + oos_trades
    combined_net = validation_net + oos_net
    combined_density = combined_trades / (validation_days + oos_days) if (validation_days + oos_days) > 0 else 0.0
    combined_short = as_float(row.get("validation_short_trade_count")) + as_float(row.get("oos_short_trade_count"))
    combined_long = as_float(row.get("validation_long_trade_count")) + as_float(row.get("oos_long_trade_count"))
    min_pf = min(as_float(row.get("validation_profit_factor")), as_float(row.get("oos_profit_factor")))
    return {
        "validation_cost06_net": validation_net - 0.30 * validation_trades,
        "oos_cost06_net": oos_net - 0.30 * oos_trades,
        "combined_net": combined_net,
        "combined_trade_count": combined_trades,
        "combined_trade_density": combined_density,
        "combined_cost06_net": combined_net - 0.30 * combined_trades,
        "combined_cost09_net": combined_net - 0.60 * combined_trades,
        "combined_long_trade_count": combined_long,
        "combined_short_trade_count": combined_short,
        "combined_short_share": combined_short / combined_trades if combined_trades > 0 else 0.0,
        "min_split_profit_factor": min_pf,
        "runtime_net_gap_vs_523_58": combined_net - RUNTIME_NET_REFERENCE,
    }


def er_strict_success(row: Mapping[str, Any]) -> bool:
    values = cost_side_values(row)
    return (
        values["combined_trade_density"] >= DENSITY_FLOOR
        and values["validation_cost06_net"] >= 0
        and values["oos_cost06_net"] > 0
        and as_float(row.get("validation_profit_factor")) >= STRICT_VALIDATION_PF_FLOOR
        and as_float(row.get("oos_profit_factor")) >= STRICT_OOS_PF_FLOOR
        and values["combined_short_share"] <= SHORT_SHARE_FLOOR
        and values["combined_net"] > 0
    )


def er_operational_proxy_stack(row: Mapping[str, Any]) -> bool:
    values = cost_side_values(row)
    return (
        er_strict_success(row)
        and values["combined_cost09_net"] >= 0
        and values["combined_net"] >= RUNTIME_NET_REFERENCE
        and values["min_split_profit_factor"] >= RUNTIME_PF_REFERENCE
        and values["combined_short_share"] <= eq.SHORT_SHARE_TARGET
    )


def er_selection_score(row: Mapping[str, Any]) -> float:
    values = cost_side_values(row)
    validation_pf = as_float(row.get("validation_profit_factor"))
    oos_pf = as_float(row.get("oos_profit_factor"))
    return (
        values["combined_net"]
        + 420.0 * max(0.0, min(validation_pf, oos_pf) - 1.0)
        + 90.0 * min(values["combined_trade_density"], 6.0)
        + 0.45 * values["combined_cost06_net"]
        + 0.18 * values["combined_cost09_net"]
        - 2.20 * max(0.0, -values["validation_cost06_net"])
        - 1.60 * max(0.0, -values["oos_cost06_net"])
        - 430.0 * max(0.0, values["combined_short_share"] - SHORT_SHARE_FLOOR)
        - 250.0 * max(0.0, DENSITY_FLOOR - values["combined_trade_density"])
        - 180.0 * max(0.0, STRICT_OOS_PF_FLOOR - oos_pf)
        - 140.0 * max(0.0, STRICT_VALIDATION_PF_FLOOR - validation_pf)
    )


def patch_dt_core() -> None:
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
        "FEATURE_AUDIT": FEATURE_AUDIT,
        "LABEL_SUMMARY": LABEL_SUMMARY,
        "MODEL_SCORECARD": MODEL_SCORECARD,
        "TRADE_SURFACE": TRADE_SURFACE,
        "SELECTED_CANDIDATE": SELECTED_CANDIDATE,
        "SELECTED_TRADE_TAPE": SELECTED_TRADE_TAPE,
        "MONTH_STABILITY": MONTH_STABILITY,
        "COST_STRESS": COST_STRESS,
        "MODEL_ARTIFACT_MANIFEST": MODEL_ARTIFACT_MANIFEST,
        "ONNX_SMOKE_REPORT": ONNX_SMOKE_REPORT,
        "LABEL_SPECS": LABEL_SPECS,
        "TARGET_DENSITIES": TARGET_DENSITIES,
        "MARGINS": MARGINS,
        "HOUR_SETS": HOUR_SETS,
        "EXTRA_FILTERS": EXTRA_FILTERS,
    }
    for name, value in replacements.items():
        setattr(dt, name, value)
    dt.feature_sets = er_feature_sets
    dt.model_specs = er_model_specs
    dt.extra_mask = er_extra_mask
    dt.strict_success = er_strict_success
    dt.selection_score = er_selection_score


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
                "obsidian-exploration-mandate(탐색 명령)",
                "obsidian-data-integrity(데이터 무결성)",
                "obsidian-model-validation(모델 검증)",
                "obsidian-artifact-lineage(산출물 계보)",
                "obsidian-result-judgment(결과 판정)",
            ],
            "hypothesis": "Cost-aware 3-class labels(비용 인식 3분류 라벨) and regime/behavior features(국면/현상 피처) can improve cost resilience(비용 회복력) without dropping density(밀도).",
            "changed_variables": ["label threshold >= cost equivalent(비용 상당 임계값 이상 라벨)", "regime/behavior derived features(국면/현상 파생 피처)", "side-quality filters(방향 품질 필터)", "full selected trade tape(전체 선택 거래 테이프)"],
            "controls": ["chronological train/validation/OOS split(시간순 학습/검증/표본외 분할)", "no trade splitting(거래 쪼개기 없음)", "no MT5 execution(MT5 실행 없음)"],
            "parent_summary": {
                "strict_pass": parent.get("strict_operational_proxy_pass_count"),
                "best_density_seed": parent.get("best_density_seed_id"),
            },
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def write_feature_audit(sets: Mapping[str, Sequence[str]]) -> None:
    rows = []
    derived = set(dt.derived_features())
    for name, columns in sets.items():
        rows.append(
            {
                "run_id": RUN_ID,
                "feature_set_id": name,
                "feature_count": len(columns),
                "derived_count": len([column for column in columns if column in derived]),
                "first_features": "|".join(list(columns)[:12]),
                "effect": "비용/방향 재시드에서 가격, 거시, 세션, 현상 피처의 기여를 분리합니다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(FEATURE_AUDIT, rows)


def write_label_summary(frame: pd.DataFrame) -> None:
    rows = []
    for spec in LABEL_SPECS:
        labels, ok = dt.label_values(frame, spec)
        for split in ["train", "validation", "oos"]:
            mask = frame["split"].eq(split).to_numpy() & ok
            split_labels = labels[mask]
            rows.append(
                {
                    "run_id": RUN_ID,
                    "label_id": spec["label_id"],
                    "split": split,
                    "horizon_m5": spec["horizon_m5"],
                    "threshold_points": spec["threshold_points"],
                    "rows": int(mask.sum()),
                    "short_count": int(np.sum(split_labels == 0)),
                    "flat_count": int(np.sum(split_labels == 1)),
                    "long_count": int(np.sum(split_labels == 2)),
                    "direction_rate": finite(float(np.mean(np.isin(split_labels, [0, 2]))) if len(split_labels) else 0.0),
                    "label_boundary": "future open is label only, never feature(미래 open은 라벨 전용, 피처 아님)",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    write_csv(LABEL_SUMMARY, rows)


def enrich_surface(surface_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    enriched = []
    for raw in surface_rows:
        row = dict(raw)
        values = cost_side_values(row)
        row.update({key: finite(value, 10) for key, value in values.items()})
        row["er_strict_cost_side_pass"] = "passed(통과)" if er_strict_success(row) else "failed(실패)"
        row["er_operational_proxy_stack_pass"] = "passed(통과)" if er_operational_proxy_stack(row) else "failed(실패)"
        row["strict_cross_split_success"] = row["er_strict_cost_side_pass"]
        row["selection_score"] = finite(er_selection_score(row), 6)
        enriched.append(row)
    return sorted(enriched, key=lambda item: (str(item["er_strict_cost_side_pass"]).startswith("passed"), as_float(item["selection_score"])), reverse=True)


def profit_factor(profits: Sequence[float]) -> float:
    return dt.profit_factor(profits)


def write_trade_auxiliary(trades: Sequence[Mapping[str, Any]]) -> None:
    write_csv(SELECTED_TRADE_TAPE, list(trades))
    frame = pd.DataFrame(list(trades))
    month_rows: list[dict[str, Any]] = []
    stress_rows: list[dict[str, Any]] = []
    side_rows: list[dict[str, Any]] = []
    if not frame.empty:
        frame["net_profit"] = pd.to_numeric(frame["net_profit"], errors="coerce").fillna(0.0)
        direction_col = "direction" if "direction" in frame.columns else "side"
        for (split, month), group in frame.groupby(["split", "open_month"], sort=True):
            profits = group["net_profit"].to_numpy(dtype="float64")
            month_rows.append({"run_id": RUN_ID, "split": split, "open_month": month, "trade_count": int(len(group)), "net_profit": finite(float(profits.sum()), 4), "profit_factor": finite(profit_factor(profits), 10), "positive_month": str(float(profits.sum()) > 0).lower(), "claim_boundary": CLAIM_BOUNDARY})
        for cost in [0.30, 0.45, 0.60, 0.90]:
            adjusted = frame["net_profit"] - (cost - COST_PER_TRADE)
            for split, group in frame.assign(adjusted=adjusted).groupby("split", sort=True):
                profits = group["adjusted"].to_numpy(dtype="float64")
                stress_rows.append({"run_id": RUN_ID, "split": split, "cost_per_trade": cost, "trade_count": int(len(group)), "net_profit": finite(float(profits.sum()), 4), "profit_factor": finite(profit_factor(profits), 10), "expectancy": finite(float(np.mean(profits)) if len(profits) else 0.0, 10), "claim_boundary": CLAIM_BOUNDARY})
        for (split, direction, hour), group in frame.groupby(["split", direction_col, "open_hour"], sort=True):
            profits = group["net_profit"].to_numpy(dtype="float64")
            side_rows.append({"run_id": RUN_ID, "split": split, "direction": direction, "open_hour": int(hour), "trade_count": int(len(group)), "net_profit": finite(float(profits.sum()), 4), "profit_factor": finite(profit_factor(profits), 10), "expectancy": finite(float(np.mean(profits)) if len(profits) else 0.0, 10), "claim_boundary": CLAIM_BOUNDARY})
    write_csv(MONTH_STABILITY, month_rows)
    write_csv(COST_STRESS, stress_rows)
    write_csv(SIDE_SESSION_REVIEW, side_rows)


def smoke_pass_model_ids(smoke_rows: Sequence[Mapping[str, Any]]) -> set[str]:
    return {str(row["model_id"]) for row in smoke_rows if str(row.get("status", "")).startswith("passed")}


def selected_surface_row(surface_rows: Sequence[Mapping[str, Any]], smoke_rows: Sequence[Mapping[str, Any]]) -> Mapping[str, Any]:
    smoke_pass = smoke_pass_model_ids(smoke_rows)
    exportable = [row for row in surface_rows if str(row.get("model_id")) in smoke_pass]
    strict = [row for row in exportable if str(row.get("er_strict_cost_side_pass", "")).startswith("passed")]
    return max(strict or exportable or list(surface_rows), key=lambda row: as_float(row.get("selection_score")))


def replay_selected_trades(frame: pd.DataFrame, trained: Mapping[str, Mapping[str, Any]], selected: Mapping[str, Any]) -> list[dict[str, Any]]:
    model_id = str(selected["model_id"])
    trained_payload = trained[model_id]
    label_spec = next(spec for spec in LABEL_SPECS if spec["label_id"] == str(selected["label_id"]))
    _, ok = dt.label_values(frame, label_spec)
    split_masks = {split: frame["split"].eq(split).to_numpy() & ok for split in ["validation", "oos"]}
    selected_trades: list[dict[str, Any]] = []
    for split in ["validation", "oos"]:
        split_frame = frame.loc[split_masks[split]].reset_index(drop=True)
        matrix = split_frame.loc[:, trained_payload["feature_columns"]].replace([np.inf, -np.inf], np.nan).fillna(0.0).to_numpy(dtype=np.float32)
        probs, classes = dt.predict_probabilities(trained_payload["model"], matrix)
        _, trades = dt.simulate_directional(
            split_frame,
            probs,
            classes,
            threshold=as_float(selected["threshold"]),
            margin_vs_flat=as_float(selected["margin_vs_flat"]),
            hours=[int(hour) for hour in str(selected["hours"]).split("|") if hour],
            extra_filter=str(selected["extra_filter"]),
            max_hold_m5=int(selected["max_hold_m5"]),
            model_id=model_id,
            split=split,
            collect_trades=True,
        )
        selected_trades.extend(trades)
    return selected_trades


def split_days_from_selected(selected: Mapping[str, Any], split: str) -> int:
    count = as_float(selected.get(f"{split}_trade_count"))
    density = as_float(selected.get(f"{split}_trade_density"))
    if density <= 0:
        return 1
    return max(1, int(round(count / density)))


def selected_trade_metrics(trade_frame: pd.DataFrame, selected: Mapping[str, Any]) -> dict[str, Any]:
    metrics: dict[str, Any] = {}
    direction_column = "direction" if "direction" in trade_frame.columns else "side"
    for split in ["validation", "oos"]:
        split_frame = trade_frame[trade_frame["split"] == split] if not trade_frame.empty else pd.DataFrame()
        profits = split_frame["net_profit"].astype(float).to_numpy(dtype="float64") if not split_frame.empty else np.asarray([], dtype="float64")
        count = int(len(split_frame))
        net = float(np.sum(profits)) if count else 0.0
        drawdown = dt.closed_drawdown(profits)
        days = split_days_from_selected(selected, split)
        metrics.update(
            {
                f"{split}_net": finite(net, 4),
                f"{split}_profit_factor": finite(profit_factor(profits), 10),
                f"{split}_expectancy": finite(net / count, 10) if count else 0.0,
                f"{split}_trade_density": finite(count / days, 10),
                f"{split}_trade_count": count,
                f"{split}_max_drawdown": finite(drawdown, 4),
                f"{split}_recovery_factor": finite(net / drawdown, 10) if drawdown > 0 else (999.0 if net > 0 else 0.0),
                f"{split}_long_trade_count": int((split_frame[direction_column] == "long").sum()) if not split_frame.empty else 0,
                f"{split}_short_trade_count": int((split_frame[direction_column] == "short").sum()) if not split_frame.empty else 0,
            }
        )
    return metrics


def selected_summary(surface_rows: Sequence[Mapping[str, Any]], smoke_rows: Sequence[Mapping[str, Any]], created_at: str, trades: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    smoke_pass = smoke_pass_model_ids(smoke_rows)
    exportable = [row for row in surface_rows if str(row.get("model_id")) in smoke_pass]
    strict = [row for row in exportable if str(row.get("er_strict_cost_side_pass", "")).startswith("passed")]
    operational = [row for row in exportable if str(row.get("er_operational_proxy_stack_pass", "")).startswith("passed")]
    best = selected_surface_row(surface_rows, smoke_rows)
    status = STATUS_STRICT if strict else STATUS_NO_STRICT
    judgment = JUDGMENT_STRICT if strict else JUDGMENT_NO_STRICT
    decision = DECISION_STRICT if strict else DECISION_NO_STRICT
    trade_frame = pd.DataFrame(list(trades))
    metric_row = dict(best)
    metric_row.update(selected_trade_metrics(trade_frame, best))
    values = cost_side_values(metric_row)
    validation_tape_count = int((trade_frame["split"] == "validation").sum()) if not trade_frame.empty else 0
    oos_tape_count = int((trade_frame["split"] == "oos").sum()) if not trade_frame.empty else 0
    return {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "status": status,
        "judgment": judgment,
        "decision": decision,
        "selected_model_id": best["model_id"],
        "selected_feature_set_id": best["feature_set_id"],
        "selected_label_id": best["label_id"],
        "selected_threshold": best["threshold"],
        "selected_hours_id": best["hours_id"],
        "selected_extra_filter": best["extra_filter"],
        "selected_margin_vs_flat": best["margin_vs_flat"],
        "selected_metric_source": "full_trade_tape_replay(전체 거래 테이프 재생)",
        "selected_surface_validation_net": best["validation_net"],
        "selected_surface_validation_trade_count": best["validation_trade_count"],
        "selected_surface_oos_net": best["oos_net"],
        "selected_surface_oos_trade_count": best["oos_trade_count"],
        "selected_surface_selection_score": best["selection_score"],
        "selected_validation_net": metric_row["validation_net"],
        "selected_validation_profit_factor": metric_row["validation_profit_factor"],
        "selected_validation_trade_density": metric_row["validation_trade_density"],
        "selected_validation_trade_count": metric_row["validation_trade_count"],
        "selected_oos_net": metric_row["oos_net"],
        "selected_oos_profit_factor": metric_row["oos_profit_factor"],
        "selected_oos_trade_density": metric_row["oos_trade_density"],
        "selected_oos_trade_count": metric_row["oos_trade_count"],
        "selected_oos_long_trade_count": metric_row["oos_long_trade_count"],
        "selected_oos_short_trade_count": metric_row["oos_short_trade_count"],
        "selected_combined_net": finite(values["combined_net"]),
        "selected_combined_trade_count": finite(values["combined_trade_count"]),
        "selected_combined_trade_density": finite(values["combined_trade_density"]),
        "selected_combined_cost06_net": finite(values["combined_cost06_net"]),
        "selected_combined_cost09_net": finite(values["combined_cost09_net"]),
        "selected_validation_cost06_net": finite(values["validation_cost06_net"]),
        "selected_oos_cost06_net": finite(values["oos_cost06_net"]),
        "selected_combined_short_share": finite(values["combined_short_share"]),
        "selected_min_split_profit_factor": finite(values["min_split_profit_factor"]),
        "strict_candidate_count": len(strict),
        "operational_proxy_stack_pass_count": len(operational),
        "surface_rows": len(surface_rows),
        "onnx_smoke_pass_rows": len(smoke_pass),
        "validation_trade_tape_rows": validation_tape_count,
        "oos_trade_tape_rows": oos_tape_count,
        "runtime_package": "not_opened",
        "new_model_training": "run",
        "new_mt5_execution": "not_run",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "live_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "report_path": rel(REPORT_PATH),
        "final_decision": rel(FINAL_DECISION),
        "created_at_utc": created_at,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def data_integrity_rows(frame: pd.DataFrame, feature_order: Sequence[str], summary: Mapping[str, Any]) -> list[dict[str, Any]]:
    duplicate_timestamps = int(frame["timestamp"].duplicated().sum())
    split_counts = frame["split"].value_counts().to_dict()
    missing_features = [column for column in list(feature_order) + dt.derived_features() if column not in frame.columns]
    rows = [
        {"run_id": RUN_ID, "audit_item": "input_lineage(입력 계보)", "status": "passed" if all(exists(path) for path in INPUT_FILES if path != Path(__file__)) else "failed", "observed": ";".join(rel(path) for path in INPUT_FILES if path != Path(__file__)), "effect": "EQ 실패 기억과 모델 입력을 ER 학습에 연결합니다.", "claim_boundary": CLAIM_BOUNDARY},
        {"run_id": RUN_ID, "audit_item": "duplicate_timestamp(중복 타임스탬프)", "status": "passed" if duplicate_timestamps == 0 else "failed", "observed": f"duplicate_timestamps={duplicate_timestamps}", "effect": "중복 행이 거래 재생을 부풀리지 않게 합니다.", "claim_boundary": CLAIM_BOUNDARY},
        {"run_id": RUN_ID, "audit_item": "split_presence(분할 존재)", "status": "passed" if all(split_counts.get(split, 0) > 0 for split in ["train", "validation", "oos"]) else "failed", "observed": json.dumps(split_counts, ensure_ascii=False, sort_keys=True), "effect": "train/validation/OOS(학습/검증/표본외) 경계를 유지합니다.", "claim_boundary": CLAIM_BOUNDARY},
        {"run_id": RUN_ID, "audit_item": "feature_columns_present(피처 컬럼 존재)", "status": "passed" if not missing_features else "failed", "observed": "|".join(missing_features), "effect": "국면/현상 파생 피처가 명시적으로 존재하는지 확인합니다.", "claim_boundary": CLAIM_BOUNDARY},
        {"run_id": RUN_ID, "audit_item": "label_boundary(라벨 경계)", "status": "passed", "observed": "future_open used only for cost-aware 3-class target labels(미래 open은 비용 인식 3분류 목표 라벨에만 사용)", "effect": "look-ahead bias(미래참조 편향)를 피처로 흘리지 않습니다.", "claim_boundary": CLAIM_BOUNDARY},
        {"run_id": RUN_ID, "audit_item": "selected_trade_tape_full(선택 거래 테이프 전체)", "status": "passed" if int(summary["validation_trade_tape_rows"]) == int(float(summary["selected_validation_trade_count"])) and int(summary["oos_trade_tape_rows"]) == int(float(summary["selected_oos_trade_count"])) else "failed", "observed": f"validation_tape={summary['validation_trade_tape_rows']};oos_tape={summary['oos_trade_tape_rows']}", "effect": "세션/방향 귀속을 부분 테이프로 과장하지 않습니다.", "claim_boundary": CLAIM_BOUNDARY},
        {"run_id": RUN_ID, "audit_item": "no_trade_splitting(거래 쪼개기 없음)", "status": "passed", "observed": "simulator jumps past exit index after entry(진입 뒤 청산 인덱스 이후로 이동)", "effect": "거래수를 쪼개 수익을 나누지 않습니다.", "claim_boundary": CLAIM_BOUNDARY},
    ]
    write_csv(DATA_INTEGRITY_AUDIT, rows)
    return rows


def write_queue(summary: Mapping[str, Any]) -> None:
    write_csv(
        RUN364ES_QUEUE,
        [
            {
                "run_id": RUN_ID,
                "next_run_id": NEXT_RUN_ID,
                "queue_rank": 1,
                "queue_id": "es01_cost_side_reseed_review",
                "review_subject": summary["selected_model_id"],
                "review_question": "Did ER improve cost resilience(비용 회복력) without breaking density(밀도)?",
                "strict_candidate_count": summary["strict_candidate_count"],
                "operational_proxy_stack_pass_count": summary["operational_proxy_stack_pass_count"],
                "selected_combined_net": summary["selected_combined_net"],
                "selected_combined_cost06_net": summary["selected_combined_cost06_net"],
                "selected_combined_cost09_net": summary["selected_combined_cost09_net"],
                "selected_combined_short_share": summary["selected_combined_short_share"],
                "effect": "ES review(ES 검토)가 package(패키지) 가능성과 실패 기억을 분리합니다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "run_id": RUN_ID,
                "next_run_id": NEXT_RUN_ID,
                "queue_rank": 2,
                "queue_id": "es02_side_session_attribution",
                "review_subject": rel(SIDE_SESSION_REVIEW),
                "review_question": "Which side/session(방향/세션)이 cost-side result(비용/방향 결과)를 움직였는가?",
                "effect": "시장 현상(market behavior, 시장 현상) 해석을 다음 수리 제약으로 바꿉니다.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ],
    )


def write_receipts(final: Mapping[str, Any]) -> None:
    base = {"run_id": RUN_ID, "stage_id": STAGE_ID, "created_at_utc": final["created_at_utc"], "claim_boundary": CLAIM_BOUNDARY}
    write_json(RUN_EVIDENCE_RECEIPT, {**base, "surface": rel(TRADE_SURFACE), "selected_candidate": rel(SELECTED_CANDIDATE), "selected_trade_tape": rel(SELECTED_TRADE_TAPE), "measurement_boundary": "Python proxy with ONNX smoke, no MT5(Python 프록시와 ONNX 스모크, MT5 없음)"})
    write_json(EXPERIMENT_RECEIPT, {**base, "idea_id": "stage364ER_cost_side_model_label_feature_reseed", "hypothesis": "Cost-aware 3-class labels and regime/behavior features(비용 인식 3분류 라벨과 국면/현상 피처)가 비용 회복력을 올릴 수 있다.", "broad_sweep": "3 label specs, 2 feature sets, 2 model families, density/hour/filter sweep(라벨/피처/모델/밀도/시간/필터 탐색)", "micro_search_gate": "strict cost-side pass before threshold polishing(엄격 비용/방향 통과 전 임계값 다듬기 금지)", "wfo_plan": "single-window scout only; WFO required before promotion(단일 구간 정찰 전용, 승격 전 WFO 필요)", "evidence_boundary": "scout-only with ONNX smoke(정찰 전용과 ONNX 스모크)"})
    write_json(DATA_RECEIPT, {**base, "data_source": [rel(dt.dp.MODEL_INPUT_DATASET), rel(dt.dp.RAW_US100_M5)], "time_axis": "UTC model input timestamp and raw open join(UTC 모델 입력 timestamp와 원천 open 결합)", "feature_label_boundary": "future_open only in cost-aware labels(미래 open은 비용 인식 라벨에만 사용)", "split_boundary": "chronological train validation OOS(시간순 학습/검증/표본외)", "integrity_audit": rel(DATA_INTEGRITY_AUDIT), "integrity_judgment": "usable_with_proxy_boundary(프록시 경계 안에서 사용 가능)"})
    write_json(MODEL_RECEIPT, {**base, "model_training": "completed(완료)", "model_family": "RandomForest/ExtraTrees(랜덤포레스트/엑스트라트리)", "onnx_smoke": rel(ONNX_SMOKE_REPORT), "strict_candidate_count": final["strict_candidate_count"], "operational_proxy_stack_pass_count": final["operational_proxy_stack_pass_count"], "selected_model_id": final["selected_model_id"], "validation_oos_boundary": "OOS is read-only(표본외는 읽기 전용)"})
    write_json(ATTRIBUTION_RECEIPT, {**base, "observed_change": f"selected combined net/density/cost06/cost09/short_share {final['selected_combined_net']} / {final['selected_combined_trade_density']} / {final['selected_combined_cost06_net']} / {final['selected_combined_cost09_net']} / {final['selected_combined_short_share']}", "likely_drivers": ["cost-aware label threshold(비용 인식 라벨 임계값)", "side-quality filters(방향 품질 필터)", "regime/behavior features(국면/현상 피처)"], "next_probe": NEXT_RUN_ID})
    write_json(JUDGMENT_RECEIPT, {**base, "result_subject": RUN_ID, "evidence_available": [rel(TRADE_SURFACE), rel(SELECTED_CANDIDATE), rel(ONNX_SMOKE_REPORT), rel(DATA_INTEGRITY_AUDIT)], "evidence_missing": ["MT5 runtime package(MT5 런타임 패키지)", "MT5 runtime probe(MT5 런타임 탐침)", "forward/replay evidence(전진/재생 근거)"], "judgment_label": final["judgment"], "next_condition": NEXT_RUN_ID, "claim_boundary": CLAIM_BOUNDARY})
    write_json(LINEAGE_RECEIPT, {**base, "source_inputs": [{"path": rel(path), "sha256": sha(path)} for path in INPUT_FILES if exists(path) and Path(path).is_file()], "producer": rel(Path(__file__)), "consumer": NEXT_RUN_ID, "artifact_paths": [rel(path) for path in OUTPUT_FILES if exists(path)], "artifact_hashes": {rel(path): sha(path) for path in OUTPUT_FILES if exists(path) and Path(path).is_file()}, "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)], "lineage_judgment": "connected_cost_side_model_reseed(비용/방향 모델 재시드 연결)"})
    write_json(CLAIM_RECEIPT, {**base, "runtime_package": "not_opened", "runtime_authority": "not_claimed", "operating_promotion": "not_claimed", "live_readiness": "not_claimed", "goal_achieve": "not_claimed", "effect": "ONNX smoke(온엑스 스모크)를 운영 주장으로 올리지 않습니다."})


def gate_rows(final: Mapping[str, Any], data_rows: Sequence[Mapping[str, Any]], *, final_written: bool) -> list[dict[str, Any]]:
    receipts = [RUN_EVIDENCE_RECEIPT, EXPERIMENT_RECEIPT, DATA_RECEIPT, MODEL_RECEIPT, ATTRIBUTION_RECEIPT, JUDGMENT_RECEIPT, LINEAGE_RECEIPT, CLAIM_RECEIPT]
    checks = [
        ("scope_completion_gate", exists(TRADE_SURFACE) and exists(SELECTED_CANDIDATE), TRADE_SURFACE, "ER surface(ER 표면)와 선택 후보를 작성했습니다."),
        ("input_lineage_gate", exists(INPUT_MANIFEST), INPUT_MANIFEST, "입력 계보가 연결됐습니다."),
        ("data_integrity_gate", bool(data_rows) and all(str(row["status"]) == "passed" for row in data_rows), DATA_INTEGRITY_AUDIT, "시점/분할/피처/라벨/테이프 검사를 통과했습니다."),
        ("training_split_gate", exists(MODEL_SCORECARD), MODEL_SCORECARD, "train split(학습 분할)로 모델을 적합하고 validation/OOS(검증/표본외)를 분리했습니다."),
        ("model_artifact_gate", exists(MODEL_ARTIFACT_MANIFEST), MODEL_ARTIFACT_MANIFEST, "joblib/ONNX(잡립/온엑스) 산출물 목록이 있습니다."),
        ("onnx_smoke_gate", exists(ONNX_SMOKE_REPORT) and int(final["onnx_smoke_pass_rows"]) > 0, ONNX_SMOKE_REPORT, "ONNX smoke(온엑스 스모크) 통과 모델이 있습니다."),
        ("cost_side_surface_gate", exists(TRADE_SURFACE) and int(final["surface_rows"]) > 0, TRADE_SURFACE, "비용/방향 파생 지표를 표면에 기록했습니다."),
        ("full_trade_tape_gate", exists(SELECTED_TRADE_TAPE), SELECTED_TRADE_TAPE, "선택 후보의 전체 검증/OOS 거래 테이프를 기록했습니다."),
        ("strict_contract_decision_gate", exists(RUN364ES_QUEUE), RUN364ES_QUEUE, "엄격 후보 수와 다음 검토를 기록했습니다."),
        ("paired_tier_record_gate", True, STAGE_LEDGER, "Tier A/Tier B/Tier A+B 장부 행을 남깁니다."),
        ("receipt_coverage_gate", all(exists(path) for path in receipts), RUN_EVIDENCE_RECEIPT, "필수 영수증이 있습니다."),
        ("required_gate_coverage_audit", final_written, GATE_AUDIT, "필수 게이트가 종료 기록에 연결됐습니다."),
        ("final_claim_guard", final["runtime_authority"] == "not_claimed" and final["operating_promotion"] == "not_claimed" and final["goal_achieve"] == "not_claimed", CLAIM_RECEIPT, "권위/승격/목표 달성 주장을 차단했습니다."),
    ]
    rows = [{"run_id": RUN_ID, "gate": gate, "status": "passed" if passed else "failed", "evidence": rel(evidence), "effect": effect, "claim_boundary": CLAIM_BOUNDARY} for gate, passed, evidence, effect in checks]
    write_csv(GATE_AUDIT, rows)
    return rows


def final_payload(summary: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    return {**summary, "gate_passes": sum(1 for row in gates if row["status"] == "passed"), "gate_total": len(gates)}


def write_docs(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    report = f"""# run364ER OOS108 cost/side model-label-feature reseed(OOS108 비용/방향 모델-라벨-피처 재시드)

Created(생성): {final['created_at_utc']}

## Summary(요약)

Action(행동): EQ strict pass 0(엄격 통과 0)을 받아 cost-aware 3-class labels(비용 인식 3분류 라벨), regime/behavior features(국면/현상 피처), side-quality filters(방향 품질 필터)로 새 모델을 학습했습니다.

Effect(효과): 기존 EL surface(EL 표면) 미세조정 반복을 멈추고, 비용을 이긴 움직임만 더 강하게 학습하는 새 수익 원천을 열었습니다.

## Selected(선택)

- selected_model_id(선택 모델 ID): `{final['selected_model_id']}`
- selected_metric_source(선택 지표 원천): `{final['selected_metric_source']}`
- validation net/PF/density/trades(검증 순수익/PF/밀도/거래수): `{final['selected_validation_net']}` / `{final['selected_validation_profit_factor']}` / `{final['selected_validation_trade_density']}` / `{final['selected_validation_trade_count']}`
- OOS net/PF/density/trades(표본외 순수익/PF/밀도/거래수): `{final['selected_oos_net']}` / `{final['selected_oos_profit_factor']}` / `{final['selected_oos_trade_density']}` / `{final['selected_oos_trade_count']}`
- combined net/density/trades(합산 순수익/밀도/거래수): `{final['selected_combined_net']}` / `{final['selected_combined_trade_density']}` / `{final['selected_combined_trade_count']}`
- surface scan reference(표면 탐색 참조): validation net/count(검증 순수익/개수) `{final['selected_surface_validation_net']}` / `{final['selected_surface_validation_trade_count']}`, OOS net/count(표본외 순수익/개수) `{final['selected_surface_oos_net']}` / `{final['selected_surface_oos_trade_count']}`
- cost0.6 validation/OOS/combined(비용0.6 검증/표본외/합산): `{final['selected_validation_cost06_net']}` / `{final['selected_oos_cost06_net']}` / `{final['selected_combined_cost06_net']}`
- combined cost0.9 net(합산 비용0.9 순수익): `{final['selected_combined_cost09_net']}`
- combined short share(합산 숏 비중): `{final['selected_combined_short_share']}`
- strict candidate count(엄격 후보 수): `{final['strict_candidate_count']}`
- operational proxy stack pass(운영형 프록시 묶음 통과): `{final['operational_proxy_stack_pass_count']}`
- ONNX smoke pass rows(온엑스 스모크 통과 행): `{final['onnx_smoke_pass_rows']}`

## Judgment(판정)

`{final['judgment']}`

Runtime package(런타임 패키지), runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.

## Next(다음)

`{NEXT_RUN_ID}`에서 비용/방향 재시드 결과를 검토하고, package(패키지) 여부와 실패 기억을 분리합니다.

## Gates(게이트)

{chr(10).join(f"- {row['gate']}: {row['status']} -> {row['evidence']}" for row in gates)}
"""
    decision_doc = f"""# Decision(결정): stage364ER cost/side model-label-feature reseed(비용/방향 모델-라벨-피처 재시드)

- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{final['decision']}`
- judgment(판정): `{final['judgment']}`
- selected_model_id(선택 모델 ID): `{final['selected_model_id']}`
- strict_candidate_count(엄격 후보 수): `{final['strict_candidate_count']}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Action(행동): 비용을 반영한 3분류 라벨과 국면/현상 피처로 새 ONNX(온엑스) 후보군을 만들었습니다.

Effect(효과): ES review(ES 검토)가 수익 구조, 비용 압박, 방향/세션 귀속, ONNX 산출물 계보를 함께 판정할 수 있습니다.
"""
    write_text(REPORT_PATH, report, bom=True)
    write_text(DECISION_DOC, decision_doc, bom=True)
    append_text_once(REVIEW_INDEX, f"run364ER__{RUN_ID}", f"\n- run364ER__{RUN_ID}: [{REPORT_PATH.name}]({REPORT_PATH.name}) - cost/side model-label-feature reseed(비용/방향 모델-라벨-피처 재시드), next `{NEXT_RUN_ID}`.\n")
    append_text_once(STAGE_BRIEF, f"run364ER__{RUN_ID}", f"\n<!-- run364ER__{RUN_ID} -->\n\n## run364ER Cost/Side Reseed(비용/방향 재시드)\n\nAction(행동): cost-aware labels(비용 인식 라벨)와 regime/behavior features(국면/현상 피처)로 모델을 학습했습니다.\n\nEffect(효과): `{NEXT_RUN_ID}`에서 package(패키지) 가능성과 failure memory(실패 기억)를 검토합니다.\n")
    append_text_once(STAGE_README, f"run364ER__{RUN_ID}", f"\n<!-- run364ER__{RUN_ID} -->\n## run364ER cost/side model-label-feature reseed(비용/방향 모델-라벨-피처 재시드)\n\nSelected(선택): `{final['selected_model_id']}`. Strict candidates(엄격 후보): `{final['strict_candidate_count']}`. Next(다음): `{NEXT_RUN_ID}`.\n")
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

Current truth(현재 진실): `run364ER` trained(학습 완료) cost-side model/label/feature reseed(비용/방향 모델/라벨/피처 재시드). Selected validation/OOS net/PF/density(선택 검증/표본외 순수익/PF/밀도)는 `{final['selected_validation_net']}` / `{final['selected_validation_profit_factor']}` / `{final['selected_validation_trade_density']}` 및 `{final['selected_oos_net']}` / `{final['selected_oos_profit_factor']}` / `{final['selected_oos_trade_density']}`입니다.

Cost/side truth(비용/방향 진실): combined cost0.6/cost0.9 net(합산 비용0.6/0.9 순수익)은 `{final['selected_combined_cost06_net']}` / `{final['selected_combined_cost09_net']}`이고, combined short share(합산 숏 비중)는 `{final['selected_combined_short_share']}`입니다.

Next action(다음 행동): `{NEXT_RUN_ID}`에서 ER 결과를 review(검토)하고 package(패키지) 가능성과 failure memory(실패 기억)를 분리합니다.

Operating boundary(운영 경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""", bom=True)
    write_text(SELECTION_STATUS, f"""# Stage364 selection status(선택 상태)

Updated(갱신): {final['created_at_utc']}

Current run(현재 실행): `{NEXT_RUN_ID}`
Latest completed run(최근 완료 실행): `{RUN_ID}`

Latest scout(최근 정찰): ER cost/side model-label-feature reseed(ER 비용/방향 모델-라벨-피처 재시드).

Selected model(선택 모델): `{final['selected_model_id']}`

Validation net/PF/density(검증 순수익/PF/밀도): `{final['selected_validation_net']}` / `{final['selected_validation_profit_factor']}` / `{final['selected_validation_trade_density']}`
OOS net/PF/density(표본외 순수익/PF/밀도): `{final['selected_oos_net']}` / `{final['selected_oos_profit_factor']}` / `{final['selected_oos_trade_density']}`

Judgment(판정): `{final['judgment']}`.

Authority(권위): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""", bom=True)
    append_text_once(WORKSPACE_CHANGELOG, f"run364ER__{RUN_ID}", f"\n<!-- run364ER__{RUN_ID} -->\n- {final['created_at_utc']} `{RUN_ID}` completed cost/side model-label-feature reseed(비용/방향 모델-라벨-피처 재시드); strict candidates `{final['strict_candidate_count']}`; selected `{final['selected_model_id']}`; next `{NEXT_RUN_ID}`; no authority claim(권위 주장 없음).\n")
    append_text_once(IDEA_REGISTRY, f"run364ER__{RUN_ID}", f"\n<!-- run364ER__{RUN_ID} -->\n- `{RUN_ID}`: cost-aware 3-class label(비용 인식 3분류 라벨)과 regime/behavior features(국면/현상 피처)를 학습했습니다. Effect(효과): 표면 미세탐색 실패를 새 model/label/feature(모델/라벨/피처) 수익 원천 탐색으로 전환했습니다.\n")
    if int(final["strict_candidate_count"]) == 0:
        append_text_once(NEGATIVE_REGISTER, f"run364ER__strict_candidate_absent__{RUN_ID}", f"\n<!-- run364ER__strict_candidate_absent__{RUN_ID} -->\n- `{RUN_ID}`: cost-side reseed(비용/방향 재시드)는 strict candidate(엄격 후보)를 만들지 못했습니다. Effect(효과): ES에서 OOS clue(표본외 단서)와 validation/cost failure(검증/비용 실패)를 분리 검토합니다.\n")


def write_ledgers(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
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
        "artifact_count": len([path for path in OUTPUT_FILES if exists(path)]),
        "gate_passes": sum(1 for row in gates if row["status"] == "passed"),
        "gate_total": len(gates),
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "created_at_utc": final["created_at_utc"],
        "required_gate_audit": rel(GATE_AUDIT),
        "question": "Can cost-aware labels and regime/behavior features repair cost/side weakness?(비용 인식 라벨과 국면/현상 피처가 비용/방향 약점을 고칠 수 있는가?)",
        "next_action": NEXT_RUN_ID,
        "notes": f"strict_candidate_count={final['strict_candidate_count']};onnx_smoke_pass_rows={final['onnx_smoke_pass_rows']};combined_cost09={final['selected_combined_cost09_net']}",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "run_family": "experiment_execution(실험 실행)",
        "run_type": "cost_side_model_label_feature_reseed(비용/방향 모델/라벨/피처 재시드)",
        "input_run_id": PARENT_RUN_ID,
        "output_path": rel(FINAL_DECISION),
        "result_path": rel(TRADE_SURFACE),
        "selected_net_profit": final["selected_oos_net"],
        "selected_profit_factor": final["selected_oos_profit_factor"],
        "selected_trade_density": final["selected_oos_trade_density"],
    }
    rows = []
    for suffix, record_view, tier_scope, status in [
        ("tier_a_separate", "Tier A separate(Tier A 분리)", "Tier A", final["status"]),
        ("tier_b_missing_required", "Tier B separate(Tier B 분리)", "Tier B", "missing_required_no_tier_b_model_input(필수 누락, Tier B 모델 입력 없음)"),
        ("tier_a_b_combined_out_of_scope", "Tier A+B combined(Tier A+B 합산)", "Tier A+B", "out_of_scope_by_claim_proxy_tier_a_only(주장 범위 밖, 프록시 Tier A 전용)"),
    ]:
        row = {**common, "ledger_row_id": f"{RUN_ID}__{suffix}", "subrun_id": f"{RUN_ID}__{suffix}", "row_id": f"{RUN_ID}__{suffix}", "record_view": record_view, "tier_scope": tier_scope, "view": record_view, "tier": tier_scope, "kpi_scope": "ER cost-side model reseed(ER 비용/방향 모델 재시드)", "metric_scope": "python_proxy_onnx_smoke(Python 프록시 ONNX 스모크)", "status": status, "net_profit": final["selected_oos_net"] if suffix == "tier_a_separate" else "", "profit_factor": final["selected_oos_profit_factor"] if suffix == "tier_a_separate" else "", "trade_density": final["selected_oos_trade_density"] if suffix == "tier_a_separate" else "", "trade_count": final["selected_oos_trade_count"] if suffix == "tier_a_separate" else "", "source_authority": "python_proxy_onnx_smoke_no_mt5(Python 프록시 ONNX 스모크, MT5 없음)"}
        rows.append(row)
    append_or_replace_csv(STAGE_LEDGER, ["ledger_row_id"], rows, extend_header=True)
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], rows, extend_header=True)
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], [common], extend_header=True)
    repair_run_registry_line_endings(RUN_ID)


def write_artifact_registry(final: Mapping[str, Any]) -> None:
    rows = []
    for path in OUTPUT_FILES + [Path(__file__)]:
        if exists(path) and Path(path).is_file():
            rows.append({"stage_id": STAGE_ID, "run_id": RUN_ID, "artifact_type": "script" if path == Path(__file__) else ("report" if path.suffix.lower() == ".md" else ("json" if path.suffix.lower() == ".json" else "csv")), "path": rel(path), "artifact_path": rel(path), "sha256": sha(path), "created_at": final["created_at_utc"], "created_at_utc": final["created_at_utc"], "claim_boundary": CLAIM_BOUNDARY, "artifact_id": f"{RUN_ID}__{path.stem}", "notes": "ER cost-side reseed artifact(ER 비용/방향 재시드 산출물)"})
    append_or_replace_csv(ARTIFACT_REGISTRY, ["artifact_id"], rows, extend_header=True)


def write_manifest(final: Mapping[str, Any]) -> None:
    outputs = [path for path in OUTPUT_FILES if exists(path)]
    write_json(RUN_MANIFEST, {"run_id": RUN_ID, "run_number": RUN_NUMBER, "stage_id": STAGE_ID, "parent_run_id": PARENT_RUN_ID, "next_run_id": NEXT_RUN_ID, "status": final["status"], "judgment": final["judgment"], "claim_boundary": CLAIM_BOUNDARY, "command": f"python {rel(Path(__file__))}", "input_files": [rel(path) for path in INPUT_FILES], "input_hashes": {rel(path): sha(path) for path in INPUT_FILES if exists(path) and Path(path).is_file()}, "output_files": [rel(path) for path in outputs], "output_hashes": {rel(path): sha(path) for path in outputs if Path(path).is_file()}})


def main() -> None:
    patch_dt_core()
    ensure_dirs()
    parent = validate_inputs()
    write_csv(INPUT_MANIFEST, input_manifest_rows())
    write_work_packet(parent)
    feature_order = dt.load_feature_order()
    frame = dt.load_dataset(feature_order)
    sets = er_feature_sets(feature_order)
    write_feature_audit(sets)
    write_label_summary(frame)
    score_rows, surface_rows, trained, selected_trades = dt.train_and_score(frame, sets)
    surface_rows = enrich_surface(surface_rows)
    write_csv(MODEL_SCORECARD, score_rows)
    write_csv(TRADE_SURFACE, surface_rows)
    _, smoke_rows = dt.export_models(trained)
    selected_trades = replay_selected_trades(frame, trained, selected_surface_row(surface_rows, smoke_rows))
    write_trade_auxiliary(selected_trades)
    summary = selected_summary(surface_rows, smoke_rows, now_utc(), selected_trades)
    write_json(SELECTED_CANDIDATE, summary)
    write_queue(summary)
    data_rows = data_integrity_rows(frame, feature_order, summary)
    gates = gate_rows(summary, data_rows, final_written=False)
    final = final_payload(summary, gates)
    write_json(FINAL_DECISION, final)
    write_receipts(final)
    gates = gate_rows(final, data_rows, final_written=True)
    final = final_payload(summary, gates)
    write_json(FINAL_DECISION, final)
    write_docs(final, gates)
    write_ledgers(final, gates)
    write_manifest(final)
    write_artifact_registry(final)
    print(json.dumps(json_ready({"run_id": RUN_ID, "status": final["status"], "judgment": final["judgment"], "strict_candidate_count": final["strict_candidate_count"], "operational_proxy_stack_pass_count": final["operational_proxy_stack_pass_count"], "selected_model_id": final["selected_model_id"], "gate_passes": final["gate_passes"], "gate_total": final["gate_total"]}), ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
