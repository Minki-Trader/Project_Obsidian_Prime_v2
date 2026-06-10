from __future__ import annotations

import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path  # noqa: E402
from stage_pipelines.stage364 import review_h17_density_floor_oos_pf_salvage_without_db as ek  # noqa: E402
from stage_pipelines.stage364 import train_h17_density_floor_oos_pf_salvage_without_db as ej  # noqa: E402


TODAY = "2026-06-06"
STAGE_ID = ej.STAGE_ID
RUN_NUMBER = "run364EL"
RUN_ID = "run364EL_train_h17_oos108_validation_floor_bridge_without_db_v1"
PARENT_RUN_ID = ek.RUN_ID
NEXT_RUN_ID = "run364EM_review_h17_oos108_validation_floor_bridge_without_db_v1"

STATUS_NO_BRIDGE = "completed_stage364EL_oos108_validation_floor_bridge_no_bridge_review_required_no_authority"
STATUS_SCOUT = "completed_stage364EL_oos108_validation_floor_bridge_scout_review_required_no_authority"
STATUS_STRICT = "completed_stage364EL_oos108_validation_floor_bridge_pf108_review_required_no_authority"
JUDGMENT_NO_BRIDGE = "inconclusive_oos108_validation_floor_bridge_no_bridge_candidate_no_package_no_authority"
JUDGMENT_SCOUT = "proxy_oos108_validation_floor_bridge_scout_review_required_no_authority"
JUDGMENT_STRICT = "proxy_oos108_validation_floor_bridge_pf108_candidate_review_required_no_authority"
DECISION = "stage364EL_open_run364EM_oos108_validation_floor_bridge_review"
CLAIM_BOUNDARY = (
    "research_development_oos108_validation_floor_bridge_proxy_and_onnx_smoke_only_"
    "no_new_mt5_execution_no_runtime_package_no_forward_pass_no_live_readiness_"
    "no_operating_promotion_no_runtime_authority_no_goal_claim"
)

STAGE_DIR = ej.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
MODEL_DIR = RUN_DIR / "models"
ONNX_DIR = RUN_DIR / "onnx"
REVIEW_DIR = STAGE_DIR / "03_reviews"
SPEC_DIR = STAGE_DIR / "00_spec"
SELECTED_DIR = STAGE_DIR / "04_selected"

INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
FEATURE_AUDIT = RUN_DIR / "el_feature_set_audit.csv"
LABEL_SUMMARY = RUN_DIR / "el_oos108_validation_floor_bridge_label_summary.csv"
MODEL_SCORECARD = RUN_DIR / "el_model_scorecard.csv"
TRADE_SURFACE = RUN_DIR / "el_oos108_validation_floor_bridge_trade_surface.csv"
SELECTED_CANDIDATE = RUN_DIR / "selected_el_candidate.json"
SELECTED_TRADE_TAPE = RUN_DIR / "selected_el_trade_tape.csv"
MONTH_STABILITY = RUN_DIR / "selected_el_month_stability.csv"
COST_STRESS = RUN_DIR / "selected_el_cost_stress.csv"
MODEL_ARTIFACT_MANIFEST = RUN_DIR / "model_artifact_manifest.csv"
ONNX_SMOKE_REPORT = RUN_DIR / "onnx_smoke_report.csv"
DATA_INTEGRITY_AUDIT = RUN_DIR / "data_integrity_audit.csv"
RUN364EM_QUEUE = RUN_DIR / "run364EM_oos108_validation_floor_bridge_review_queue.csv"
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

REPORT_PATH = REVIEW_DIR / "run364EL_h17_oos108_validation_floor_bridge.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364EL_h17_oos108_validation_floor_bridge.md"
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
    ek.FINAL_DECISION,
    ek.GATE_AUDIT,
    ek.REVIEW_SUMMARY,
    ek.FAILURE_MEMORY,
    ek.PACKAGE_DECISION,
    ek.RUN364EL_QUEUE,
    ek.REPORT_PATH,
    ej.FINAL_DECISION,
    ej.TRADE_SURFACE,
    ej.SELECTED_CANDIDATE,
    ej.SELECTED_TRADE_TAPE,
    ej.MONTH_STABILITY,
    ej.COST_STRESS,
    ej.MODEL_SCORECARD,
    ej.ONNX_SMOKE_REPORT,
    ej.DATA_INTEGRITY_AUDIT,
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
    MODEL_ARTIFACT_MANIFEST,
    ONNX_SMOKE_REPORT,
    DATA_INTEGRITY_AUDIT,
    RUN364EM_QUEUE,
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
    {"label_id": "oos108_valfloor_dir_h2_m1", "horizon_m5": 2, "threshold_points": 1.0, "max_hold_m5": 2},
    {"label_id": "oos108_valfloor_dir_h2_m1p25", "horizon_m5": 2, "threshold_points": 1.25, "max_hold_m5": 2},
    {"label_id": "oos108_valfloor_dir_h2_m1p5", "horizon_m5": 2, "threshold_points": 1.5, "max_hold_m5": 2},
]
DENSITY_TARGETS = [3, 4, 5, 6, 7, 8, 9]
MARGINS = [-0.07, -0.06, -0.05, -0.04, -0.03, -0.02, -0.01]
HOUR_SETS = {
    "all_hours": list(range(24)),
    "cash15_22": [15, 16, 17, 18, 19, 20, 21, 22],
    "no_h21_all_hours": [hour for hour in range(24) if hour != 21],
    "h17_22_density_keep": [17, 18, 19, 20, 21, 22],
}
STABILITY_FILTERS = [
    "none",
    "no_h21",
    "density_relief_months",
    "q4_h21_relief",
    "q1_q4_h21_gap",
    "valfloor_oos_blend",
    "oos108_side_quality",
]


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    return ej.rel(path)


def exists(path: Path | str) -> bool:
    return ej.exists(path)


def sha(path: Path | str) -> str:
    return ej.sha(path)


def read_json(path: Path) -> Any:
    return ej.read_json(path)


def write_json(path: Path, payload: Any) -> None:
    ej.write_json(path, payload)


def write_text(path: Path, text: str, *, bom: bool = True) -> None:
    ej.write_text(path, text, bom=bom)


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    ej.write_csv(path, rows, fieldnames)


def append_or_replace_csv(path: Path, key_fields: Sequence[str], rows: Sequence[Mapping[str, Any]], *, extend_header: bool = True) -> None:
    ej.append_or_replace_csv(path, key_fields, rows, extend_header=extend_header)


def append_text_once(path: Path, marker: str, text: str) -> None:
    ej.append_text_once(path, marker, text)


def replace_prefixed_lines(path: Path, replacements: Mapping[str, str], *, bom: bool = True) -> None:
    ej.replace_prefixed_lines(path, replacements, bom=bom)


def as_float(value: Any, default: float = 0.0) -> float:
    return ej.as_float(value, default)


def validate_inputs() -> dict[str, Any]:
    missing = [rel(path) for path in INPUT_FILES if path != Path(__file__) and not exists(path)]
    if missing:
        raise FileNotFoundError("missing EL inputs(EL 입력 누락): " + ", ".join(missing))
    parent = read_json(ek.FINAL_DECISION)
    if parent.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"EK next_run_id mismatch(EK 다음 실행 ID 불일치): {parent.get('next_run_id')} != {RUN_ID}")
    for key in ["runtime_authority", "operating_promotion", "live_readiness", "goal_achieve"]:
        if parent.get(key, "not_claimed") != "not_claimed":
            raise RuntimeError(f"EK forbidden claim(EK 금지 주장): {key}={parent.get(key)}")
    gates = pd.read_csv(io_path(ek.GATE_AUDIT), encoding="utf-8-sig").fillna("")
    if gates.empty or any(gates["status"].astype(str) != "passed"):
        raise RuntimeError("EK gate audit(EK 게이트 감사)가 모두 passed(통과)가 아닙니다.")
    return parent


def input_manifest_rows() -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "input_path": rel(path),
            "exists": exists(path),
            "sha256": sha(path) if exists(path) and io_path(path).is_file() else "",
            "input_role": "EL OOS108 validation floor bridge input(EL 표본외108 검증 바닥 연결 입력)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for path in INPUT_FILES
    ]


def el_feature_sets(feature_order: Sequence[str]) -> dict[str, list[str]]:
    dv = ej.eh.ef.ed.eb.dv
    base = list(feature_order)
    derived = dv.dt.derived_features()
    stability = dv.stability_features()
    session = [c for c in base if any(token in c for token in ["cash", "minutes", "open", "close"])]
    price = [c for c in base if any(token in c for token in ["return", "ratio", "ema", "sma", "rsi", "atr", "adx", "bb_", "bollinger", "vol", "gap"])]
    return {
        "source_all82": list(dict.fromkeys(base + derived + stability)),
        "source_all_price_session": list(dict.fromkeys(base + price + session + derived + stability)),
    }


def el_model_specs() -> list[tuple[str, str, Any]]:
    dp = ej.eh.ef.ed.eb.dv.dp
    return [
        (
            "et7_l70_n192",
            "ExtraTrees(엑스트라트리)",
            dp.ExtraTreesClassifier(n_estimators=192, max_depth=7, min_samples_leaf=70, class_weight="balanced", random_state=531, n_jobs=-1),
        ),
        (
            "et8_l90_n160",
            "ExtraTrees(엑스트라트리)",
            dp.ExtraTreesClassifier(n_estimators=160, max_depth=8, min_samples_leaf=90, class_weight="balanced", random_state=532, n_jobs=-1),
        ),
        (
            "et7_l55_n192",
            "ExtraTrees(엑스트라트리)",
            dp.ExtraTreesClassifier(n_estimators=192, max_depth=7, min_samples_leaf=55, class_weight="balanced", random_state=533, n_jobs=-1),
        ),
        (
            "rf8_l70_n160",
            "RandomForest(랜덤포레스트)",
            dp.RandomForestClassifier(n_estimators=160, max_depth=8, min_samples_leaf=70, class_weight="balanced_subsample", random_state=534, n_jobs=-1),
        ),
    ]


def el_stability_mask(frame: pd.DataFrame, score: np.ndarray, p_short: np.ndarray, p_long: np.ndarray, side: np.ndarray, filter_id: str) -> np.ndarray:
    hour = frame["timestamp"].dt.hour.to_numpy(dtype=int)
    month = frame["timestamp"].dt.month.to_numpy(dtype=int)
    direction_gap = np.abs(p_short - p_long)
    q4 = np.isin(month, [10, 11, 12])
    q1_q2 = np.isin(month, [1, 2, 3, 4])
    relief_month = q1_q2 | q4
    if filter_id == "none":
        return np.ones(len(frame), dtype=bool)
    if filter_id == "no_h21":
        return hour != 21
    if filter_id == "density_relief_months":
        return relief_month | ((direction_gap >= 0.006) & (hour != 21))
    if filter_id == "q4_h21_relief":
        return ((hour != 21) & (relief_month | (direction_gap >= 0.006))) | ((hour == 21) & q4 & (direction_gap >= 0.004))
    if filter_id == "q1_q4_h21_gap":
        return ((hour != 21) & (relief_month | (direction_gap >= 0.005))) | ((hour == 21) & relief_month & (direction_gap >= 0.014))
    if filter_id == "valfloor_oos_blend":
        return ((hour != 21) & (direction_gap >= 0.004)) | ((hour == 21) & q4 & (direction_gap >= 0.006))
    if filter_id == "oos108_side_quality":
        return ((side == "long") & (direction_gap >= 0.005) & ((hour != 21) | q4)) | ((side == "short") & (direction_gap >= 0.010) & ((hour != 21) | q4))
    raise ValueError(f"unknown EL filter(알 수 없는 EL 필터): {filter_id}")


def el_selection_score(row: Mapping[str, Any]) -> float:
    validation_net = as_float(row["validation_net"])
    oos_net = as_float(row["oos_net"])
    validation_pf = as_float(row["validation_profit_factor"])
    oos_pf = as_float(row["oos_profit_factor"])
    validation_density = as_float(row["validation_trade_density"])
    oos_density = as_float(row["oos_trade_density"])
    min_density = min(validation_density, oos_density)
    min_pf = min(validation_pf, oos_pf)
    density_gap = max(0.0, 3.0 - min_density)
    validation_floor_gap = max(0.0, 1.04 - validation_pf)
    oos108_gap = max(0.0, 1.08 - oos_pf)
    return (
        0.34 * validation_net
        + 0.42 * oos_net
        + 1050.0 * max(0.0, oos_pf - 1.0)
        + 920.0 * max(0.0, validation_pf - 1.0)
        + 460.0 * max(0.0, min_pf - 1.0)
        + 260.0 * min(min_density, 6.0)
        - 2300.0 * density_gap
        - 1900.0 * validation_floor_gap
        - 1800.0 * oos108_gap
        - 340.0 * abs(validation_pf - oos_pf)
        - (520.0 if validation_net <= 0 else 0.0)
        - (520.0 if oos_net <= 0 else 0.0)
    )


def el_selected_summary(surface_rows: Sequence[Mapping[str, Any]], smoke_rows: Sequence[Mapping[str, Any]], created_at: str) -> dict[str, Any]:
    smoke_pass = {str(row["model_id"]) for row in smoke_rows if str(row.get("status", "")).startswith("passed")}
    exportable_rows = [row for row in surface_rows if row["model_id"] in smoke_pass]
    density_rows = [
        row
        for row in exportable_rows
        if as_float(row["validation_trade_density"]) >= 3.0
        and as_float(row["oos_trade_density"]) >= 3.0
        and as_float(row["validation_net"]) > 0.0
        and as_float(row["oos_net"]) > 0.0
    ]
    bridge_rows = [row for row in density_rows if as_float(row["validation_profit_factor"]) >= 1.04 and as_float(row["oos_profit_factor"]) >= 1.08]
    pf108_rows = [row for row in density_rows if as_float(row["validation_profit_factor"]) >= 1.08 and as_float(row["oos_profit_factor"]) >= 1.08]
    oos108_rows = [row for row in density_rows if as_float(row["oos_profit_factor"]) >= 1.08]
    val104_rows = [row for row in density_rows if as_float(row["validation_profit_factor"]) >= 1.04]
    near_bridge_rows = [
        row
        for row in density_rows
        if as_float(row["validation_profit_factor"]) >= 1.03
        and as_float(row["oos_profit_factor"]) >= 1.07
    ]
    pool = pf108_rows or bridge_rows or near_bridge_rows or oos108_rows or val104_rows or density_rows or exportable_rows or list(surface_rows)
    best = max(pool, key=lambda row: as_float(row["selection_score"]))
    strict_count = len(pf108_rows)
    scout_count = len(bridge_rows)
    status = STATUS_STRICT if strict_count else (STATUS_SCOUT if scout_count else STATUS_NO_BRIDGE)
    judgment = JUDGMENT_STRICT if strict_count else (JUDGMENT_SCOUT if scout_count else JUDGMENT_NO_BRIDGE)
    return {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "status": status,
        "judgment": judgment,
        "decision": DECISION,
        "selected_model_id": best["model_id"],
        "selected_feature_set_id": best["feature_set_id"],
        "selected_label_id": best["label_id"],
        "selected_threshold": best["threshold"],
        "selected_hours_id": best["hours_id"],
        "selected_stability_filter": best["stability_filter"],
        "selected_margin_vs_flat": best["margin_vs_flat"],
        "selected_validation_net": best["validation_net"],
        "selected_validation_profit_factor": best["validation_profit_factor"],
        "selected_validation_trade_density": best["validation_trade_density"],
        "selected_validation_trade_count": best["validation_trade_count"],
        "selected_oos_net": best["oos_net"],
        "selected_oos_profit_factor": best["oos_profit_factor"],
        "selected_oos_trade_density": best["oos_trade_density"],
        "selected_oos_trade_count": best["oos_trade_count"],
        "selected_oos_long_trade_count": best["oos_long_trade_count"],
        "selected_oos_short_trade_count": best["oos_short_trade_count"],
        "selected_min_profit_factor": min(as_float(best["validation_profit_factor"]), as_float(best["oos_profit_factor"])),
        "density_net_count": len(density_rows),
        "oos108_count": len(oos108_rows),
        "val104_count": len(val104_rows),
        "bridge_count": len(bridge_rows),
        "near_bridge_count": len(near_bridge_rows),
        "pf108_count": len(pf108_rows),
        "scout115_count": 0,
        "strict_candidate_count": strict_count,
        "surface_rows": len(surface_rows),
        "onnx_smoke_pass_rows": len(smoke_pass),
        "runtime_package": "not_opened",
        "new_model_training": "run",
        "new_mt5_execution": "not_run",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "live_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "created_at_utc": created_at,
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "final_decision": rel(FINAL_DECISION),
        "selection_pool": "pf108" if pf108_rows else ("bridge" if bridge_rows else ("near_bridge" if near_bridge_rows else ("oos108" if oos108_rows else ("val104" if val104_rows else ("density_net" if density_rows else "exportable"))))),
    }


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
            "hypothesis": "EJ density OOS108 rows(EJ 밀도 OOS108 행)의 validation floor gap(검증 바닥 간극)을 month/hour/gap filters(월/시간/간극 필터)로 줄이면 validation PF>=1.04 and OOS PF>=1.08 bridge(검증 PF 1.04 이상 및 표본외 PF 1.08 이상 연결)가 생길 수 있습니다.",
            "comparison_baseline": parent["parent_run_id"],
            "success_criteria": "validation/OOS density>=3, validation PF>=1.04, OOS PF>=1.08 bridge; PF>=1.08 both splits strict",
            "failure_criteria": "no validation floor OOS108 bridge with density>=3",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def write_queue(summary: Mapping[str, Any]) -> None:
    write_csv(
        RUN364EM_QUEUE,
        [
            {
                "run_id": RUN_ID,
                "next_run_id": NEXT_RUN_ID,
                "queue_rank": 1,
                "queue_id": "em01_oos108_validation_floor_bridge_review",
                "review_subject": summary["selected_model_id"],
                "review_question": "Did EL bridge validation PF>=1.04 and OOS PF>=1.08 with density>=3?(EL이 밀도 3 이상에서 검증 PF 1.04와 표본외 PF 1.08을 연결했는가?)",
                "selection_pool": summary["selection_pool"],
                "bridge_count": summary["bridge_count"],
                "pf108_count": summary["pf108_count"],
                "oos108_count": summary["oos108_count"],
                "val104_count": summary["val104_count"],
                "selected_validation_profit_factor": summary["selected_validation_profit_factor"],
                "selected_oos_profit_factor": summary["selected_oos_profit_factor"],
                "selected_validation_trade_density": summary["selected_validation_trade_density"],
                "selected_oos_trade_density": summary["selected_oos_trade_density"],
                "effect": "EM review(EM 검토)가 package(패키지) 가능성과 다음 실패 기억을 분리합니다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )


def write_receipts(final: Mapping[str, Any]) -> None:
    base = {"run_id": RUN_ID, "stage_id": STAGE_ID, "created_at_utc": final["created_at_utc"], "claim_boundary": CLAIM_BOUNDARY}
    write_json(RUN_EVIDENCE_RECEIPT, {**base, "surface": rel(TRADE_SURFACE), "selected_candidate": rel(SELECTED_CANDIDATE), "selected_trade_tape": rel(SELECTED_TRADE_TAPE), "measurement_boundary": "Python proxy with ONNX smoke, no MT5(Python 프록시와 ONNX 스모크, MT5 없음)"})
    write_json(EXPERIMENT_RECEIPT, {**base, "hypothesis": "month/hour/gap filters can bridge OOS108 with validation floor(월/시간/간극 필터가 표본외108과 검증 바닥을 연결할 수 있음)", "comparison_baseline": PARENT_RUN_ID, "success_criteria": "density>=3 validation PF>=1.04 OOS PF>=1.08", "failure_criteria": "bridge_count=0 or OOS clue collapses", "decision_use": NEXT_RUN_ID})
    write_json(DATA_RECEIPT, {**base, "data_source": [rel(ej.eh.ef.ed.eb.dv.dp.MODEL_INPUT_DATASET), rel(ej.eh.ef.ed.eb.dv.dp.RAW_US100_M5)], "time_axis": "UTC model input timestamp and raw open join(UTC 모델 입력 timestamp와 원천 open 결합)", "feature_label_boundary": "future_open only in labels(미래 open은 라벨에만 사용)", "split_boundary": "chronological train validation OOS(시간순 학습/검증/표본외)", "integrity_judgment": "usable_with_proxy_boundary(프록시 경계 안에서 사용 가능)"})
    write_json(MODEL_RECEIPT, {**base, "model_family": "RandomForest/ExtraTrees(랜덤포레스트/엑스트라트리)", "selected_model_id": final["selected_model_id"], "onnx_smoke_pass_rows": final["onnx_smoke_pass_rows"], "validation_judgment": final["judgment"], "threshold_policy": "OOS108 validation floor bridge search(표본외108 검증 바닥 연결 탐색)"})
    write_json(ATTRIBUTION_RECEIPT, {**base, "observed_change": f"bridge_count {final['bridge_count']}; selected validation {final['selected_validation_profit_factor']}/{final['selected_validation_trade_density']}; OOS {final['selected_oos_profit_factor']}/{final['selected_oos_trade_density']}", "likely_drivers": ["month/hour/gap filters(월/시간/간극 필터)", "source_all h2 labels(전체 원천 h2 라벨)", "density floor selection(밀도 바닥 선택)"], "next_probe": NEXT_RUN_ID})
    write_json(JUDGMENT_RECEIPT, {**base, "result_subject": RUN_ID, "evidence_available": [rel(TRADE_SURFACE), rel(SELECTED_CANDIDATE), rel(ONNX_SMOKE_REPORT), rel(DATA_INTEGRITY_AUDIT)], "evidence_missing": ["MT5 runtime package(MT5 런타임 패키지)", "MT5 runtime probe(MT5 런타임 탐침)", "forward/replay evidence(전진/재생 근거)"], "judgment_label": final["judgment"], "next_condition": NEXT_RUN_ID})
    write_json(LINEAGE_RECEIPT, {**base, "source_inputs": [{"path": rel(path), "sha256": sha(path)} for path in INPUT_FILES if exists(path) and io_path(path).is_file()], "producer": rel(Path(__file__)), "consumer": NEXT_RUN_ID, "artifact_paths": [rel(path) for path in OUTPUT_FILES if exists(path)], "artifact_hashes": {rel(path): sha(path) for path in OUTPUT_FILES if exists(path) and io_path(path).is_file()}, "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)], "lineage_judgment": "connected_oos108_validation_floor_bridge(표본외108 검증 바닥 연결)"})
    write_json(CLAIM_RECEIPT, {**base, "runtime_package": "not_opened", "runtime_authority": "not_claimed", "operating_promotion": "not_claimed", "live_readiness": "not_claimed", "goal_achieve": "not_claimed", "effect": "EL 결과를 operating claim(운영 주장)으로 올리지 않습니다."})


def write_docs(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    gate_lines = "\n".join(f"- {row['gate']}: {row['status']} -> {row['evidence']}" for row in gates)
    report = f"""# run364EL H17 OOS108 Validation Floor Bridge(표본외108 검증 바닥 연결)

Created(생성): {final['created_at_utc']}

Action(행동): EK failure memory(EK 실패 기억)를 받아 density>=3 and OOS PF>=1.08(밀도 3 이상 및 표본외 PF 1.08 이상) 후보의 validation PF floor(검증 PF 바닥)를 수리하는 모델 탐색을 실행했습니다.

Effect(효과): EJ의 가까운 실패 경계를 bridge(연결) 후보로 바꿀 수 있는지 확인합니다.

Selected(선택): `{final['selected_model_id']}`

- selection_pool(선택 풀): `{final['selection_pool']}`
- validation net/PF/density(검증 순수익/PF/밀도): `{final['selected_validation_net']}` / `{final['selected_validation_profit_factor']}` / `{final['selected_validation_trade_density']}`
- OOS net/PF/density(표본외 순수익/PF/밀도): `{final['selected_oos_net']}` / `{final['selected_oos_profit_factor']}` / `{final['selected_oos_trade_density']}`
- min_pf(최소 PF): `{final['selected_min_profit_factor']}`
- bridge_count(연결 후보 수): `{final['bridge_count']}`
- pf108_count(PF 1.08 양쪽 통과 수): `{final['pf108_count']}`
- oos108_count(표본외 PF 1.08 후보 수): `{final['oos108_count']}`
- val104_count(검증 PF 1.04 후보 수): `{final['val104_count']}`

Judgment(판정): `{final['judgment']}`

Runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.

Next(다음): `{NEXT_RUN_ID}`

Gates(게이트):

{gate_lines}
"""
    write_text(REPORT_PATH, report, bom=True)
    write_text(DECISION_DOC, f"""# Decision(결정): stage364EL OOS108 validation floor bridge(표본외108 검증 바닥 연결)

- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{final['judgment']}`
- selected_model_id(선택 모델 ID): `{final['selected_model_id']}`
- selected_min_profit_factor(선택 최소 수익 팩터): `{final['selected_min_profit_factor']}`
- bridge_count(연결 후보 수): `{final['bridge_count']}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Action(행동): OOS108 validation floor bridge(표본외108 검증 바닥 연결)를 proxy and ONNX smoke(프록시 및 ONNX 스모크) 경계에서 실행했습니다.

Effect(효과): EM review(EM 검토)가 package(패키지), failure memory(실패 기억), next seed(다음 씨앗)를 분리합니다.
""", bom=True)
    append_text_once(REVIEW_INDEX, f"run364EL__{RUN_ID}", f"\n- run364EL__{RUN_ID}: [{REPORT_PATH.name}]({REPORT_PATH.name}) - OOS108 validation floor bridge(표본외108 검증 바닥 연결), next `{NEXT_RUN_ID}`.\n")
    append_text_once(STAGE_BRIEF, f"run364EL__{RUN_ID}", f"\n<!-- run364EL__{RUN_ID} -->\n\n## run364EL OOS108 Validation Floor Bridge(표본외108 검증 바닥 연결)\n\nAction(행동): density>=3과 OOS PF>=1.08(밀도 3 이상과 표본외 PF 1.08 이상)을 보존하며 validation PF floor(검증 PF 바닥)를 수리하는 모델을 학습했습니다.\n\nEffect(효과): `{NEXT_RUN_ID}`에서 package(패키지) 가능성과 다음 조건을 검토합니다.\n")
    append_text_once(STAGE_README, f"run364EL__{RUN_ID}", f"\n<!-- run364EL__{RUN_ID} -->\n## run364EL OOS108 validation floor bridge(표본외108 검증 바닥 연결)\n\nSelected(선택): `{final['selected_model_id']}`. min_pf(최소 PF): `{final['selected_min_profit_factor']}`. Next(다음): `{NEXT_RUN_ID}`.\n")
    replace_prefixed_lines(STAGE_BRIEF, {"- current_run_id": f"- current_run_id(현재 실행 ID): `{NEXT_RUN_ID}`", "- latest_completed_run_id": f"- latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`", "- selection_status": f"- selection_status(선택 상태): `{final['status']}`", "- claim_boundary": f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`"}, bom=True)
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

Current truth(현재 진실): `run364EL` trained(학습 완료) OOS108 validation floor bridge(표본외108 검증 바닥 연결). Selected validation/OOS net/PF/density(선택 검증/표본외 순수익/PF/밀도)는 `{final['selected_validation_net']}` / `{final['selected_validation_profit_factor']}` / `{final['selected_validation_trade_density']}` 및 `{final['selected_oos_net']}` / `{final['selected_oos_profit_factor']}` / `{final['selected_oos_trade_density']}`입니다. bridge_count(연결 후보 수)는 `{final['bridge_count']}`입니다.

Next action(다음 행동): `{NEXT_RUN_ID}`에서 EL 결과를 review(검토)합니다.

Operating boundary(운영 경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""", bom=True)
    write_text(SELECTION_STATUS, f"""# Stage364 selection status(선택 상태)

Updated(갱신): {final['created_at_utc']}

Current run(현재 실행): `{NEXT_RUN_ID}`
Latest completed run(최근 완료 실행): `{RUN_ID}`

Latest scout(최근 탐색): EL OOS108 validation floor bridge(EL 표본외108 검증 바닥 연결)는 selected model(선택 모델) `{final['selected_model_id']}`를 만들었습니다.

Validation net/PF/density(검증 순수익/PF/밀도): `{final['selected_validation_net']}` / `{final['selected_validation_profit_factor']}` / `{final['selected_validation_trade_density']}`
OOS net/PF/density(표본외 순수익/PF/밀도): `{final['selected_oos_net']}` / `{final['selected_oos_profit_factor']}` / `{final['selected_oos_trade_density']}`
Bridge count(연결 후보 수): `{final['bridge_count']}`
PF108 count(PF 1.08 양쪽 통과 수): `{final['pf108_count']}`

Authority(권위): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""", bom=True)
    append_text_once(WORKSPACE_CHANGELOG, f"run364EL__{RUN_ID}", f"\n<!-- run364EL__{RUN_ID} -->\n- {final['created_at_utc']} `{RUN_ID}` completed OOS108 validation floor bridge(표본외108 검증 바닥 연결); bridge_count `{final['bridge_count']}`; pf108_count `{final['pf108_count']}`; next `{NEXT_RUN_ID}`; no authority claim(권위 주장 없음).\n")
    append_text_once(IDEA_REGISTRY, f"run364EL__{RUN_ID}", f"\n<!-- run364EL__{RUN_ID} -->\n- `{RUN_ID}`: OOS108 validation floor bridge(표본외108 검증 바닥 연결)를 month/hour/gap filters(월/시간/간극 필터)로 탐색했습니다. Effect(효과): 밀도와 표본외 PF 단서가 검증 PF 바닥과 함께 살아남는지 확인합니다.\n")
    if int(final["bridge_count"]) == 0:
        append_text_once(NEGATIVE_REGISTER, f"run364EL__bridge_absent__{RUN_ID}", f"\n<!-- run364EL__bridge_absent__{RUN_ID} -->\n- `{RUN_ID}`: bridge_count(연결 후보 수)는 `{final['bridge_count']}`입니다. Effect(효과): EM review(EM 검토)에서 남은 실패 경계를 다음 씨앗으로 분리합니다.\n")


def write_ledgers(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    common = {"stage_id": STAGE_ID, "run_id": RUN_ID, "parent_run_id": PARENT_RUN_ID, "status": final["status"], "judgment": final["judgment"], "path": rel(FINAL_DECISION), "run_number": RUN_NUMBER, "date": TODAY, "decision": final["decision"], "next_run_id": NEXT_RUN_ID, "artifact_count": len([path for path in OUTPUT_FILES if exists(path)]), "gate_passes": sum(1 for row in gates if row["status"] == "passed"), "gate_total": len(gates), "claim_boundary": CLAIM_BOUNDARY, "report_path": rel(REPORT_PATH), "created_at_utc": final["created_at_utc"], "required_gate_audit": rel(GATE_AUDIT), "question": "Can OOS108 validation floor bridge hold density?(표본외108 검증 바닥 연결이 밀도를 유지하는가?)", "next_action": NEXT_RUN_ID, "notes": f"bridge_count={final['bridge_count']};pf108_count={final['pf108_count']};onnx_smoke_pass_rows={final['onnx_smoke_pass_rows']}", "runtime_authority": "not_claimed", "operating_promotion": "not_claimed"}
    rows = []
    for suffix, record_view, tier_scope, status in [
        ("tier_a_separate", "Tier A separate(Tier A 분리)", "Tier A", final["status"]),
        ("tier_b_missing_required", "Tier B separate(Tier B 분리)", "Tier B", "missing_required_no_tier_b_model_input(필수 누락, Tier B 모델 입력 없음)"),
        ("tier_a_b_combined_out_of_scope", "Tier A+B combined(Tier A+B 합산)", "Tier A+B", "out_of_scope_by_claim_proxy_tier_a_only(주장 범위 밖, 프록시 Tier A 전용)"),
    ]:
        rows.append({**common, "ledger_row_id": f"{RUN_ID}__{suffix}", "subrun_id": f"{RUN_ID}__{suffix}", "row_id": f"{RUN_ID}__{suffix}", "record_view": record_view, "tier_scope": tier_scope, "view": record_view, "tier": tier_scope, "kpi_scope": "EL OOS108 validation floor bridge(EL 표본외108 검증 바닥 연결)", "metric_scope": "python_proxy_onnx_smoke(Python 프록시 ONNX 스모크)", "status": status, "net_profit": final["selected_oos_net"] if suffix == "tier_a_separate" else "", "profit_factor": final["selected_oos_profit_factor"] if suffix == "tier_a_separate" else "", "trade_density_per_feature_day": final["selected_oos_trade_density"] if suffix == "tier_a_separate" else "", "trade_count": final["selected_oos_trade_count"] if suffix == "tier_a_separate" else "", "long_trade_count": final["selected_oos_long_trade_count"] if suffix == "tier_a_separate" else "", "short_trade_count": final["selected_oos_short_trade_count"] if suffix == "tier_a_separate" else "", "source_authority": "python_proxy_onnx_smoke_no_mt5(Python 프록시 ONNX 스모크, MT5 없음)"})
    append_or_replace_csv(STAGE_LEDGER, ["ledger_row_id"], rows, extend_header=True)
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], rows, extend_header=True)
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], [{**common, "lane": "offensive_exploration(공격 탐색)", "family": "alpha_exploration(알파 탐색)", "primary_report": rel(REPORT_PATH), "run_family": "experiment_execution(실험 실행)", "run_type": "oos108_validation_floor_bridge(표본외108 검증 바닥 연결)", "input_run_id": PARENT_RUN_ID, "output_path": rel(FINAL_DECISION), "result_path": rel(TRADE_SURFACE), "best_model_id": final["selected_model_id"], "net_profit": final["selected_oos_net"], "profit_factor": final["selected_oos_profit_factor"], "trade_density_per_feature_day": final["selected_oos_trade_density"], "trade_count": final["selected_oos_trade_count"], "long_trade_count": final["selected_oos_long_trade_count"], "short_trade_count": final["selected_oos_short_trade_count"], "result_status": final["status"], "primary_kpi": f"bridge_count={final['bridge_count']};oos_pf={final['selected_oos_profit_factor']}", "guardrail_kpi": f"validation_pf={final['selected_validation_profit_factor']};density={final['selected_oos_trade_density']};authority=not_claimed", "final_decision_path": rel(FINAL_DECISION), "gate_audit_path": rel(GATE_AUDIT), "external_verification_status": "not_run(미실행)", "evidence_boundary": "proxy_and_onnx_smoke_only_no_mt5_runtime_authority(프록시 및 ONNX 스모크만, MT5 런타임 권위 없음)"}], extend_header=True)
    ej.eh.ef.ed.eb.dz.repair_run_registry_line_endings(RUN_ID)


def write_artifact_registry(final: Mapping[str, Any]) -> None:
    rows = []
    for path in OUTPUT_FILES:
        if exists(path) and io_path(path).is_file():
            rows.append({
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "artifact_type": "script" if path == Path(__file__) else ("report" if path.suffix.lower() == ".md" else ("json" if path.suffix.lower() == ".json" else "csv")),
                "path": rel(path),
                "artifact_path": rel(path),
                "sha256": sha(path),
                "created_at": final["created_at_utc"],
                "created_at_utc": final["created_at_utc"],
                "claim_boundary": CLAIM_BOUNDARY,
                "artifact_id": f"{RUN_ID}__{path.stem}",
                "notes": "EL OOS108 validation floor bridge artifact(EL 표본외108 검증 바닥 연결 산출물)",
            })
    append_or_replace_csv(ARTIFACT_REGISTRY, ["artifact_id"], rows, extend_header=True)


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
            "input_files": [rel(path) for path in INPUT_FILES],
            "input_hashes": {rel(path): sha(path) for path in INPUT_FILES if exists(path) and io_path(path).is_file()},
            "output_files": [rel(path) for path in outputs],
            "output_hashes": {rel(path): sha(path) for path in outputs if io_path(path).is_file()},
        },
    )


def patch_ej_module() -> None:
    replacements = {
        "TODAY": TODAY,
        "RUN_NUMBER": RUN_NUMBER,
        "RUN_ID": RUN_ID,
        "PARENT_RUN_ID": PARENT_RUN_ID,
        "NEXT_RUN_ID": NEXT_RUN_ID,
        "STATUS_NO_BRIDGE": STATUS_NO_BRIDGE,
        "STATUS_SCOUT": STATUS_SCOUT,
        "STATUS_STRICT": STATUS_STRICT,
        "JUDGMENT_NO_BRIDGE": JUDGMENT_NO_BRIDGE,
        "JUDGMENT_SCOUT": JUDGMENT_SCOUT,
        "JUDGMENT_STRICT": JUDGMENT_STRICT,
        "DECISION": DECISION,
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
        "MODEL_ARTIFACT_MANIFEST": MODEL_ARTIFACT_MANIFEST,
        "ONNX_SMOKE_REPORT": ONNX_SMOKE_REPORT,
        "DATA_INTEGRITY_AUDIT": DATA_INTEGRITY_AUDIT,
        "RUN364EK_QUEUE": RUN364EM_QUEUE,
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
        "DENSITY_TARGETS": DENSITY_TARGETS,
        "MARGINS": MARGINS,
        "HOUR_SETS": HOUR_SETS,
        "STABILITY_FILTERS": STABILITY_FILTERS,
    }
    for name, value in replacements.items():
        setattr(ej, name, value)
    ej.validate_inputs = validate_inputs
    ej.input_manifest_rows = input_manifest_rows
    ej.write_work_packet = write_work_packet
    ej.ej_feature_sets = el_feature_sets
    ej.ej_model_specs = el_model_specs
    ej.ej_stability_mask = el_stability_mask
    ej.ej_selection_score = el_selection_score
    ej.ej_selected_summary = el_selected_summary
    ej.write_queue = write_queue
    ej.write_receipts = write_receipts
    ej.write_docs = write_docs
    ej.write_ledgers = write_ledgers


def main() -> None:
    patch_ej_module()
    ej.patch_eh_module()
    ej.eh.patch_ef_module()
    ej.eh.ef.write_artifact_registry = write_artifact_registry
    ej.eh.ef.write_manifest = write_manifest
    ej.eh.ef.main()


if __name__ == "__main__":
    main()
