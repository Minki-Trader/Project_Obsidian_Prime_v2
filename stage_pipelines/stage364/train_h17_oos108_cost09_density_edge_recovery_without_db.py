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
from stage_pipelines.stage364 import review_h17_oos108_density_cost_short_balance_reseed_without_db as eu  # noqa: E402
from stage_pipelines.stage364 import train_h17_oos108_density_cost_short_balance_reseed_without_db as et  # noqa: E402


TODAY = "2026-06-06"
STAGE_ID = et.STAGE_ID
RUN_NUMBER = "run364EV"
RUN_ID = "run364EV_train_h17_oos108_cost09_density_edge_recovery_without_db_v1"
PARENT_RUN_ID = eu.RUN_ID
NEXT_RUN_ID = "run364EW_review_h17_oos108_cost09_density_edge_recovery_without_db_v1"

STATUS_NO_STRICT = "completed_stage364EV_oos108_cost09_density_edge_recovery_no_strict_pass_review_required_no_authority"
STATUS_STRICT = "completed_stage364EV_oos108_cost09_density_edge_recovery_strict_proxy_review_required_no_authority"
JUDGMENT_NO_STRICT = "inconclusive_cost09_density_edge_recovery_no_strict_pass_review_required_no_authority"
JUDGMENT_STRICT = "inconclusive_cost09_density_edge_recovery_strict_proxy_review_required_no_authority"
DECISION_NO_STRICT = "stage364EV_open_run364EW_cost09_density_edge_review"
DECISION_STRICT = "stage364EV_open_run364EW_cost09_density_edge_review"
CLAIM_BOUNDARY = (
    "research_development_cost09_density_edge_recovery_proxy_and_onnx_smoke_only_no_new_mt5_execution_"
    "no_runtime_package_no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

STAGE_DIR = et.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
MODEL_DIR = RUN_DIR / "models"
ONNX_DIR = RUN_DIR / "onnx"
REVIEW_DIR = STAGE_DIR / "03_reviews"
SPEC_DIR = STAGE_DIR / "00_spec"
SELECTED_DIR = STAGE_DIR / "04_selected"

INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
FEATURE_AUDIT = RUN_DIR / "ev_feature_set_audit.csv"
LABEL_SUMMARY = RUN_DIR / "ev_cost09_density_label_summary.csv"
MODEL_SCORECARD = RUN_DIR / "ev_model_scorecard.csv"
TRADE_SURFACE = RUN_DIR / "ev_cost09_density_edge_surface.csv"
SELECTED_CANDIDATE = RUN_DIR / "selected_ev_candidate.json"
SELECTED_TRADE_TAPE = RUN_DIR / "selected_ev_trade_tape.csv"
MONTH_STABILITY = RUN_DIR / "selected_ev_month_stability.csv"
COST_STRESS = RUN_DIR / "selected_ev_cost_stress.csv"
SIDE_SESSION_REVIEW = RUN_DIR / "selected_ev_side_session_review.csv"
MODEL_ARTIFACT_MANIFEST = RUN_DIR / "model_artifact_manifest.csv"
ONNX_SMOKE_REPORT = RUN_DIR / "onnx_smoke_report.csv"
DATA_INTEGRITY_AUDIT = RUN_DIR / "data_integrity_audit.csv"
RUN364EW_QUEUE = RUN_DIR / "run364EW_cost09_density_edge_review_queue.csv"
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

REPORT_PATH = REVIEW_DIR / "run364EV_h17_oos108_cost09_density_edge_recovery.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364EV_h17_oos108_cost09_density_edge_recovery.md"
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

INPUT_FILES = [
    eu.FINAL_DECISION,
    eu.GATE_AUDIT,
    eu.REVIEW_SUMMARY,
    eu.FAILURE_ATTRIBUTION,
    eu.SALVAGE_CANDIDATES,
    eu.FAILURE_MEMORY,
    eu.RUN364EV_QUEUE,
    et.FINAL_DECISION,
    et.SELECTED_CANDIDATE,
    et.SELECTED_TRADE_TAPE,
    et.COST_STRESS,
    et.SIDE_SESSION_REVIEW,
    et.MONTH_STABILITY,
    et.TRADE_SURFACE,
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
    RUN364EW_QUEUE,
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
    {"label_id": "ev_sym_h2_m2", "horizon_m5": 2, "threshold_points": 2.0, "mode": "symmetric"},
    {"label_id": "ev_sym_h2_m2p5", "horizon_m5": 2, "threshold_points": 2.5, "mode": "symmetric"},
    {"label_id": "ev_asym_h2_l2_s3", "horizon_m5": 2, "threshold_points": 2.5, "long_threshold_points": 2.0, "short_threshold_points": 3.0, "mode": "asymmetric"},
]
TARGET_DENSITIES = [3, 4, 5, 6, 8]
MARGINS = [-0.06, -0.04, -0.02]
HOUR_SETS = {
    "ev_core_16_17_18_20_22": [16, 17, 18, 20, 22],
    "ev_no_h20": [16, 17, 18, 22],
    "ev_cash_15_22": [15, 16, 17, 18, 19, 20, 21, 22],
}
EXTRA_FILTERS = ["none", "ev_cost_edge_guard", "ev_density_repair_guard"]

DENSITY_FLOOR = 3.0
STRICT_SHORT_SHARE_FLOOR = 0.72
STRICT_MIN_PF_FLOOR = 1.12
OPERATIONAL_MIN_PF_FLOOR = 1.21
RUNTIME_NET_REFERENCE = 523.58
COST_PER_TRADE = et.COST_PER_TRADE


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
    return et.sha(path)


def as_float(value: Any, default: float = 0.0) -> float:
    return et.as_float(value, default)


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
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text, encoding="utf-8-sig" if bom else "utf-8")


def append_text_once(path: Path, marker: str, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    existing = io_path(path).read_text(encoding="utf-8-sig") if exists(path) else ""
    if marker in existing:
        return
    payload = existing.rstrip() + "\n" + text.lstrip() if existing.strip() else text
    io_path(path).write_text(payload, encoding="utf-8-sig")


def append_or_replace_csv(path: Path, key_fields: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> None:
    rows = list(rows)
    existing_rows: list[dict[str, Any]] = []
    fieldnames: list[str] = []
    materialized = io_path(path)
    if materialized.exists():
        with materialized.open("r", encoding="utf-8-sig", newline="") as handle:
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
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with materialized.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in merged:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def validate_inputs() -> dict[str, Any]:
    missing = [rel(path) for path in INPUT_FILES if path != THIS_FILE and not exists(path)]
    if missing:
        raise FileNotFoundError("missing EV inputs(EV 입력 누락): " + ", ".join(missing))
    parent = read_json(eu.FINAL_DECISION)
    if parent.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"EU next_run_id mismatch(EU 다음 실행 ID 불일치): {parent.get('next_run_id')} != {RUN_ID}")
    for key in ["runtime_authority", "operating_promotion", "live_readiness", "goal_achieve"]:
        if parent.get(key, "not_claimed") != "not_claimed":
            raise RuntimeError(f"forbidden EU claim(금지된 EU 주장): {key}={parent.get(key)}")
    gates = pd.read_csv(io_path(eu.GATE_AUDIT), encoding="utf-8-sig").fillna("")
    if gates.empty or any(gates["status"].astype(str) != "passed"):
        raise RuntimeError("EU gate audit(EU 게이트 감사)가 모두 passed(통과)가 아닙니다.")
    return parent


def input_manifest_rows() -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "input_path": rel(path),
            "exists": str(exists(path)).lower(),
            "sha256": sha(path) if exists(path) and io_path(path).is_file() else "",
            "input_role": "EV cost09/density edge input(EV 비용0.9/밀도 엣지 입력)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for path in INPUT_FILES
    ]


def ev_label_values(frame: pd.DataFrame, spec: Mapping[str, Any]) -> tuple[np.ndarray, np.ndarray]:
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


def ev_feature_sets(feature_order: Sequence[str]) -> dict[str, list[str]]:
    base = list(feature_order)
    derived = et.dt.derived_features()
    cost_behavior = [
        column
        for column in base
        if any(token in column for token in ["return", "ratio", "rsi", "atr", "adx", "vol", "gap", "vix", "breadth", "mega8"])
    ]
    session = [column for column in base if any(token in column for token in ["cash", "minutes", "open", "close"])]
    macro = [column for column in base if any(token in column for token in ["us10yr", "usdx", "vix", "breadth", "mega8"])]
    return {
        "ev_all72": list(dict.fromkeys(base + derived)),
        "ev_cost_session_macro": list(dict.fromkeys(cost_behavior + session + macro + derived)),
    }


def ev_model_specs() -> list[tuple[str, str, Any]]:
    return [
        (
            "et8_l34_n96",
            "ExtraTrees(엑스트라트리)",
            et.dt.dp.ExtraTreesClassifier(n_estimators=96, max_depth=8, min_samples_leaf=34, class_weight="balanced", random_state=761, n_jobs=1),
        ),
        (
            "rf8_l44_n96",
            "RandomForest(랜덤포레스트)",
            et.dt.dp.RandomForestClassifier(n_estimators=96, max_depth=8, min_samples_leaf=44, class_weight="balanced_subsample", random_state=762, n_jobs=1),
        ),
    ]


def col(frame: pd.DataFrame, name: str, default: float = 0.0) -> np.ndarray:
    if name in frame.columns:
        return frame[name].to_numpy(dtype=float)
    return np.full(len(frame), default, dtype=float)


def ev_extra_mask(frame: pd.DataFrame, side: np.ndarray, extra_filter: str) -> np.ndarray:
    mask = np.ones(len(frame), dtype=bool)
    hour = frame["timestamp"].dt.hour.to_numpy(dtype=int)
    breadth = col(frame, "mega8_pos_breadth_1", 0.5)
    vol_ratio = col(frame, "historical_vol_5_over_20", 1.0)
    log_return_3 = col(frame, "log_return_3", 0.0)
    vix_stress = col(frame, "vix_zscore_20", 0.0)
    if extra_filter == "none":
        return mask
    if extra_filter == "ev_cost_edge_guard":
        long_ok = (side == "long") & (((hour == 20) & (breadth >= 0.35)) | ((hour == 16) & (breadth >= 0.30)) | ((np.isin(hour, [17, 18])) & (breadth >= 0.55) & (log_return_3 >= -0.001)))
        short_ok = (side == "short") & (((np.isin(hour, [16, 18, 22])) & (vol_ratio >= 0.65)) | ((hour == 17) & (log_return_3 < -0.0002)) | ((hour == 20) & (breadth <= 0.35)))
        return mask & (long_ok | short_ok)
    if extra_filter == "ev_no_long18_short20":
        return mask & ~(((side == "long") & (hour == 18)) | ((side == "short") & (hour == 20)))
    if extra_filter == "ev_quality_breadth_guard":
        long_ok = (side == "long") & (breadth >= 0.42) & (vix_stress <= 1.25)
        short_ok = (side == "short") & ((breadth <= 0.58) | (log_return_3 < 0.0)) & (vol_ratio >= 0.70)
        return mask & (long_ok | short_ok)
    if extra_filter == "ev_density_repair_guard":
        long_ok = (side == "long") & np.isin(hour, [16, 17, 18, 20, 22]) & (breadth >= 0.28)
        short_ok = (side == "short") & np.isin(hour, [16, 17, 18, 20, 22]) & (vol_ratio >= 0.55)
        return mask & (long_ok | short_ok)
    raise ValueError(f"unknown EV filter(알 수 없는 EV 필터): {extra_filter}")


def ev_cost_values(row: Mapping[str, Any]) -> dict[str, float]:
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


def ev_strict_success(row: Mapping[str, Any]) -> bool:
    values = ev_cost_values(row)
    min_pf = min(as_float(row.get("validation_profit_factor")), as_float(row.get("oos_profit_factor")))
    return (
        values["combined_trade_density"] >= DENSITY_FLOOR
        and values["validation_trade_density"] >= DENSITY_FLOOR
        and values["validation_cost09_net"] >= 0.0
        and values["oos_cost09_net"] >= 0.0
        and values["combined_cost09_net"] >= 0.0
        and values["combined_short_share"] <= STRICT_SHORT_SHARE_FLOOR
        and min_pf >= STRICT_MIN_PF_FLOOR
        and values["combined_net"] > 0.0
    )


def ev_operational_stack(row: Mapping[str, Any]) -> bool:
    values = ev_cost_values(row)
    min_pf = min(as_float(row.get("validation_profit_factor")), as_float(row.get("oos_profit_factor")))
    return ev_strict_success(row) and values["combined_net"] >= RUNTIME_NET_REFERENCE and min_pf >= OPERATIONAL_MIN_PF_FLOOR


def ev_selection_score(row: Mapping[str, Any]) -> float:
    values = ev_cost_values(row)
    validation_pf = as_float(row.get("validation_profit_factor"))
    oos_pf = as_float(row.get("oos_profit_factor"))
    min_pf = min(validation_pf, oos_pf)
    density = values["combined_trade_density"]
    validation_density = values["validation_trade_density"]
    return (
        values["combined_net"]
        + 840.0 * max(0.0, min_pf - 1.0)
        + 230.0 * min(density, 6.0)
        + 150.0 * min(validation_density, 5.0)
        + 1.20 * values["combined_cost06_net"]
        + 1.85 * values["combined_cost09_net"]
        + 1.60 * values["validation_cost09_net"]
        + 0.80 * values["oos_cost09_net"]
        - 4.20 * max(0.0, -values["validation_cost09_net"])
        - 2.40 * max(0.0, -values["combined_cost09_net"])
        - 950.0 * max(0.0, DENSITY_FLOOR - density)
        - 720.0 * max(0.0, DENSITY_FLOOR - validation_density)
        - 650.0 * max(0.0, values["combined_short_share"] - STRICT_SHORT_SHARE_FLOOR)
        - 340.0 * max(0.0, STRICT_MIN_PF_FLOOR - min_pf)
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
            "hypothesis": "ET near miss(ET 근접 실패)는 cost0.9(비용0.9)와 full-tape density(전체 테이프 밀도)를 score(점수)에 더 세게 넣으면 회복될 수 있습니다.",
            "success_criteria": "validation density>=3, combined density>=3, validation cost0.9>=0, combined cost0.9>=0, OOS PF>=1.25, short_share<=0.72(검증/합산 밀도, 비용0.9, 표본외 PF, 숏 비중 조건)",
            "failure_criteria": "no strict candidate(엄격 후보 없음) or OOS-only winner(표본외 전용 승자)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def write_queue(summary: Mapping[str, Any]) -> None:
    et.write_csv(
        RUN364EW_QUEUE,
        [
            {
                "run_id": RUN_ID,
                "next_run_id": NEXT_RUN_ID,
                "queue_rank": 1,
                "queue_id": "ew01_cost09_density_edge_review",
                "review_subject": summary["selected_model_id"],
                "strict_candidate_count": summary["strict_candidate_count"],
                "operational_proxy_stack_pass_count": summary["operational_proxy_stack_pass_count"],
                "selected_combined_net": summary["selected_combined_net"],
                "selected_combined_trade_density": summary["selected_combined_trade_density"],
                "selected_combined_cost09_net": summary["selected_combined_cost09_net"],
                "selected_combined_short_share": summary["selected_combined_short_share"],
                "effect": "EW review(EW 검토)가 EV cost09/density edge(EV 비용0.9/밀도 엣지) 결과를 패키지와 실패 기억으로 분리합니다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )


def write_receipts(final: Mapping[str, Any]) -> None:
    base = {"run_id": RUN_ID, "stage_id": STAGE_ID, "created_at_utc": final["created_at_utc"], "claim_boundary": CLAIM_BOUNDARY}
    write_json(RUN_EVIDENCE_RECEIPT, {**base, "surface": rel(TRADE_SURFACE), "selected_candidate": rel(SELECTED_CANDIDATE), "selected_trade_tape": rel(SELECTED_TRADE_TAPE), "measurement_boundary": "Python proxy with ONNX smoke, no MT5(Python 프록시와 ONNX 스모크, MT5 없음)"})
    write_json(EXPERIMENT_RECEIPT, {**base, "hypothesis": "cost09/density edge(비용0.9/밀도 엣지)를 score(점수)에 직접 넣어 ET 실패를 회복합니다.", "comparison_baseline": PARENT_RUN_ID, "decision_use": NEXT_RUN_ID})
    write_json(DATA_RECEIPT, {**base, "data_source": [rel(et.dt.dp.MODEL_INPUT_DATASET), rel(et.dt.dp.RAW_US100_M5)], "time_axis": "UTC model input timestamp(UTC 모델 입력 타임스탬프)", "feature_label_boundary": "future_open only in labels(미래 open은 라벨에만 사용)", "split_boundary": "chronological train/validation/OOS(시간순 학습/검증/표본외)", "integrity_judgment": "usable_with_proxy_boundary(프록시 경계 안에서 사용 가능)"})
    write_json(MODEL_RECEIPT, {**base, "model_family": "RandomForest/ExtraTrees(랜덤포레스트/엑스트라트리)", "selected_model_id": final["selected_model_id"], "onnx_smoke_pass_rows": final["onnx_smoke_pass_rows"], "validation_judgment": final["judgment"]})
    write_json(ATTRIBUTION_RECEIPT, {**base, "observed_change": f"selected combined net/density/cost09/short {final['selected_combined_net']}/{final['selected_combined_trade_density']}/{final['selected_combined_cost09_net']}/{final['selected_combined_short_share']}", "likely_drivers": ["cost09 weighted score(비용0.9 가중 점수)", "validation density penalty(검증 밀도 벌점)", "segment quality guard(구간 품질 가드)"], "next_probe": NEXT_RUN_ID})
    write_json(JUDGMENT_RECEIPT, {**base, "result_subject": RUN_ID, "evidence_available": [rel(TRADE_SURFACE), rel(SELECTED_CANDIDATE), rel(ONNX_SMOKE_REPORT), rel(DATA_INTEGRITY_AUDIT)], "evidence_missing": ["MT5 runtime package(MT5 런타임 패키지)", "MT5 runtime probe(MT5 런타임 탐침)", "forward/replay evidence(전진/재생 근거)"], "judgment_label": final["judgment"], "next_condition": NEXT_RUN_ID})
    write_json(LINEAGE_RECEIPT, {**base, "source_inputs": [{"path": rel(path), "sha256": sha(path)} for path in INPUT_FILES if exists(path) and io_path(path).is_file()], "producer": rel(THIS_FILE), "consumer": NEXT_RUN_ID, "artifact_paths": [rel(path) for path in OUTPUT_FILES if exists(path)], "artifact_hashes": {rel(path): sha(path) for path in OUTPUT_FILES if exists(path) and io_path(path).is_file()}, "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)], "lineage_judgment": "connected_proxy_model_reseed(프록시 모델 재시드 연결)"})
    write_json(CLAIM_RECEIPT, {**base, "runtime_package": "not_opened", "runtime_authority": "not_claimed", "operating_promotion": "not_claimed", "live_readiness": "not_claimed", "goal_achieve": "not_claimed", "effect": "EV 모델 단서를 운영 주장으로 올리지 않습니다."})


def write_docs(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    gate_lines = "\n".join(f"- {row['gate']}: {row['status']} -> {row['evidence']}" for row in gates)
    report = f"""# run364EV H17 OOS108 Cost09/Density Edge Recovery(비용0.9/밀도 엣지 회복)

Created(생성): {final['created_at_utc']}

Action(행동): EU review(EU 검토)의 실패 기억을 받아 cost0.9(비용0.9), validation density(검증 밀도), full-tape density(전체 테이프 밀도)를 더 세게 반영한 model/label/score(모델/라벨/점수)를 학습했습니다.

Effect(효과): ET의 OOS PF(표본외 수익 팩터) 단서를 보존하면서 검증 비용 압박과 밀도 3/day(일 3회) 간극을 직접 시험했습니다.

- judgment(판정): `{final['judgment']}`
- selected_model_id(선택 모델 ID): `{final['selected_model_id']}`
- validation net/PF/density(검증 순수익/PF/밀도): `{final['selected_validation_net']}` / `{final['selected_validation_profit_factor']}` / `{final['selected_validation_trade_density']}`
- OOS net/PF/density(표본외 순수익/PF/밀도): `{final['selected_oos_net']}` / `{final['selected_oos_profit_factor']}` / `{final['selected_oos_trade_density']}`
- combined net/density/cost0.9/short share(합산 순수익/밀도/비용0.9/숏 비중): `{final['selected_combined_net']}` / `{final['selected_combined_trade_density']}` / `{final['selected_combined_cost09_net']}` / `{final['selected_combined_short_share']}`
- strict_candidate_count(엄격 후보 수): `{final['strict_candidate_count']}`
- operational_proxy_stack_pass_count(운영형 프록시 묶음 통과 수): `{final['operational_proxy_stack_pass_count']}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`

Gates(게이트):

{gate_lines}

Boundary(경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
"""
    decision_doc = f"""# Decision(결정): stage364EV cost09/density edge recovery(비용0.9/밀도 엣지 회복)

- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{final['decision']}`
- judgment(판정): `{final['judgment']}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Action(행동): EV 모델/라벨/점수 재시드를 실행하고 EW review(EW 검토)로 넘겼습니다.

Effect(효과): 비용0.9와 밀도 실패를 다음 판정에서 패키지 가능성 또는 실패 기억으로 닫을 수 있게 합니다.
"""
    write_text(REPORT_PATH, report, bom=True)
    write_text(DECISION_DOC, decision_doc, bom=True)
    append_text_once(REVIEW_INDEX, f"run364EV__{RUN_ID}", f"\n- run364EV__{RUN_ID}: [{REPORT_PATH.name}]({REPORT_PATH.name}) - cost09/density edge recovery(비용0.9/밀도 엣지 회복), next `{NEXT_RUN_ID}`.\n")
    append_text_once(STAGE_BRIEF, f"run364EV__{RUN_ID}", f"\n<!-- run364EV__{RUN_ID} -->\n\n## run364EV Cost09/Density Edge Recovery(비용0.9/밀도 엣지 회복)\n\nAction(행동): 비용0.9/밀도 엣지 회복 모델을 학습했습니다.\n\nEffect(효과): `{NEXT_RUN_ID}`에서 패키지 가능성과 실패 경계를 검토합니다.\n")
    append_text_once(STAGE_README, f"run364EV__{RUN_ID}", f"\n<!-- run364EV__{RUN_ID} -->\n## run364EV cost09/density edge recovery(비용0.9/밀도 엣지 회복)\n\nNext(다음): `{NEXT_RUN_ID}`.\n")
    write_text(
        WORKSPACE_STATE,
        f"""current_stage_id: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {final['status']}
current_judgment: {final['judgment']}
next_run_id: {NEXT_RUN_ID}
runtime_authority: not_claimed
operating_promotion: not_claimed
goal_achieve: not_claimed
updated_at_utc: {final['created_at_utc']}
""",
        bom=False,
    )
    write_text(
        CURRENT_WORKING_STATE,
        f"""# Current Working State(현재 작업 상태)

Updated(갱신): {final['created_at_utc']}

Active stage(활성 단계): `{STAGE_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Current run(현재 실행): `{NEXT_RUN_ID}`

Current truth(현재 진실): `run364EV` trained(학습 완료) cost09/density edge recovery(비용0.9/밀도 엣지 회복). Selected validation/OOS net/PF/density(선택 검증/표본외 순수익/PF/밀도)는 `{final['selected_validation_net']}` / `{final['selected_validation_profit_factor']}` / `{final['selected_validation_trade_density']}` 및 `{final['selected_oos_net']}` / `{final['selected_oos_profit_factor']}` / `{final['selected_oos_trade_density']}`입니다.

Package truth(패키지 진실): runtime package(런타임 패키지)는 아직 not opened(열지 않음)입니다. EW review(EW 검토)가 strict candidate(엄격 후보), cost0.9(비용0.9), density(밀도), short share(숏 비중)를 분리 판정해야 합니다.

Next action(다음 행동): `{NEXT_RUN_ID}`에서 EV 결과를 검토합니다.

Operating boundary(운영 경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""",
        bom=True,
    )
    write_text(
        SELECTION_STATUS,
        f"""# Stage364 selection status(선택 상태)

Updated(갱신): {final['created_at_utc']}

Current run(현재 실행): `{NEXT_RUN_ID}`
Latest completed run(최근 완료 실행): `{RUN_ID}`

Latest scout(최근 정찰): EV cost09/density edge recovery(EV 비용0.9/밀도 엣지 회복).

Selected model(선택 모델): `{final['selected_model_id']}`

Validation net/PF/density(검증 순수익/PF/밀도): `{final['selected_validation_net']}` / `{final['selected_validation_profit_factor']}` / `{final['selected_validation_trade_density']}`
OOS net/PF/density(표본외 순수익/PF/밀도): `{final['selected_oos_net']}` / `{final['selected_oos_profit_factor']}` / `{final['selected_oos_trade_density']}`
Combined net/density/cost0.9/short share(합산 순수익/밀도/비용0.9/숏 비중): `{final['selected_combined_net']}` / `{final['selected_combined_trade_density']}` / `{final['selected_combined_cost09_net']}` / `{final['selected_combined_short_share']}`

Judgment(판정): `{final['judgment']}`.

Authority(권위): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""",
        bom=True,
    )
    append_text_once(WORKSPACE_CHANGELOG, f"run364EV__{RUN_ID}", f"\n<!-- run364EV__{RUN_ID} -->\n- {final['created_at_utc']} `{RUN_ID}` completed cost09/density edge recovery(비용0.9/밀도 엣지 회복); strict candidates `{final['strict_candidate_count']}`; selected `{final['selected_model_id']}`; next `{NEXT_RUN_ID}`; no authority claim(권위 주장 없음).\n")
    append_text_once(IDEA_REGISTRY, f"run364EV__{RUN_ID}", f"\n<!-- run364EV__{RUN_ID} -->\n- `{RUN_ID}`: cost09/density edge recovery(비용0.9/밀도 엣지 회복)를 학습했습니다. Effect(효과): ET near miss(ET 근접 실패)를 더 강한 비용0.9/밀도 목적 함수로 재검사했습니다.\n")
    if int(final["strict_candidate_count"]) == 0:
        append_text_once(NEGATIVE_REGISTER, f"run364EV__strict_candidate_absent__{RUN_ID}", f"\n<!-- run364EV__strict_candidate_absent__{RUN_ID} -->\n- `{RUN_ID}`: cost09/density edge recovery(비용0.9/밀도 엣지 회복)는 strict candidate(엄격 후보)를 만들지 못했습니다. Effect(효과): EW에서 실패 경계와 회수 단서를 분리합니다.\n")


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
        "question": "Can cost09/density edge recovery repair ET near miss?(비용0.9/밀도 엣지 회복이 ET 근접 실패를 고칠 수 있는가?)",
        "next_action": NEXT_RUN_ID,
        "notes": f"strict_candidate_count={final['strict_candidate_count']};onnx_smoke_pass_rows={final['onnx_smoke_pass_rows']};combined_cost09={final['selected_combined_cost09_net']}",
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
                "kpi_scope": "EV cost09/density edge recovery(EV 비용0.9/밀도 엣지 회복)",
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
                "run_type": "cost09_density_edge_recovery(비용0.9/밀도 엣지 회복)",
                "input_run_id": PARENT_RUN_ID,
                "output_path": rel(FINAL_DECISION),
                "result_path": rel(TRADE_SURFACE),
                "selected_net_profit": final["selected_oos_net"],
                "selected_profit_factor": final["selected_oos_profit_factor"],
                "selected_trade_density": final["selected_oos_trade_density"],
            }
        ],
    )
    et.repair_run_registry_line_endings(RUN_ID)


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
                    "notes": "EV cost09/density edge recovery artifact(EV 비용0.9/밀도 엣지 회복 산출물)",
                }
            )
    append_or_replace_csv(ARTIFACT_REGISTRY, ["artifact_id"], rows)


def write_manifest(final: Mapping[str, Any]) -> None:
    outputs = [path for path in OUTPUT_FILES if exists(path)]
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "run_number": RUN_NUMBER,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "status": final["status"],
            "judgment": final["judgment"],
            "claim_boundary": CLAIM_BOUNDARY,
            "command": f"python {rel(THIS_FILE)}",
            "input_files": [rel(path) for path in INPUT_FILES],
            "input_hashes": {rel(path): sha(path) for path in INPUT_FILES if exists(path) and io_path(path).is_file()},
            "output_files": [rel(path) for path in outputs],
            "output_hashes": {rel(path): sha(path) for path in outputs if io_path(path).is_file()},
        },
    )


def apply_ev_patch() -> None:
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
        "RUN364EU_QUEUE": RUN364EW_QUEUE,
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
        "INPUT_FILES": INPUT_FILES,
        "OUTPUT_FILES": OUTPUT_FILES,
        "LABEL_SPECS": LABEL_SPECS,
        "TARGET_DENSITIES": TARGET_DENSITIES,
        "MARGINS": MARGINS,
        "HOUR_SETS": HOUR_SETS,
        "EXTRA_FILTERS": EXTRA_FILTERS,
    }
    for name, value in replacements.items():
        setattr(et, name, value)
    et.validate_inputs = validate_inputs
    et.input_manifest_rows = input_manifest_rows
    et.et_label_values = ev_label_values
    et.et_feature_sets = ev_feature_sets
    et.et_model_specs = ev_model_specs
    et.et_extra_mask = ev_extra_mask
    et.cost_values = ev_cost_values
    et.et_strict_success = ev_strict_success
    et.et_operational_stack = ev_operational_stack
    et.et_selection_score = ev_selection_score
    et.write_work_packet = write_work_packet
    et.write_queue = write_queue
    et.write_receipts = write_receipts
    et.write_docs = write_docs
    et.write_ledgers = write_ledgers
    et.write_artifact_registry = write_artifact_registry
    et.write_manifest = write_manifest


def main() -> None:
    apply_ev_patch()
    et.main()


if __name__ == "__main__":
    main()
