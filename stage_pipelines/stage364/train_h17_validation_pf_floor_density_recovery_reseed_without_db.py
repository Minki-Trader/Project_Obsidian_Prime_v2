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

from foundation.control_plane.ledger import io_path  # noqa: E402
from stage_pipelines.stage364 import review_h17_density_pf_balance_reseed_without_db as ea  # noqa: E402
from stage_pipelines.stage364 import train_h17_density_pf_balance_reseed_without_db as dz  # noqa: E402
from stage_pipelines.stage364 import train_h17_validation_stability_regime_source_reseed_without_db as dv  # noqa: E402


TODAY = "2026-06-06"
STAGE_ID = dv.STAGE_ID
RUN_NUMBER = "run364EB"
RUN_ID = "run364EB_train_h17_validation_pf_floor_density_recovery_reseed_without_db_v1"
PARENT_RUN_ID = ea.RUN_ID
NEXT_RUN_ID = "run364EC_review_h17_validation_pf_floor_density_recovery_reseed_without_db_v1"

STATUS_NO_STRICT = "completed_stage364EB_validation_pf_floor_reseed_no_strict_review_required_no_authority"
STATUS_STRICT = "completed_stage364EB_validation_pf_floor_reseed_proxy_candidate_review_required_no_authority"
JUDGMENT_NO_STRICT = "inconclusive_validation_pf_floor_reseed_no_cross_split_candidate_no_package_no_authority"
JUDGMENT_STRICT = "proxy_validation_pf_floor_reseed_found_cross_split_candidate_review_required_no_authority"
DECISION = "stage364EB_open_run364EC_validation_pf_floor_reseed_review"
CLAIM_BOUNDARY = (
    "research_development_validation_pf_floor_density_recovery_proxy_and_onnx_smoke_only_"
    "no_new_mt5_execution_no_runtime_package_no_forward_pass_no_live_readiness_"
    "no_operating_promotion_no_runtime_authority_no_goal_claim"
)

STAGE_DIR = dv.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
MODEL_DIR = RUN_DIR / "models"
ONNX_DIR = RUN_DIR / "onnx"
REVIEW_DIR = STAGE_DIR / "03_reviews"
SPEC_DIR = STAGE_DIR / "00_spec"
SELECTED_DIR = STAGE_DIR / "04_selected"

INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
FEATURE_AUDIT = RUN_DIR / "eb_feature_set_audit.csv"
LABEL_SUMMARY = RUN_DIR / "eb_validation_pf_floor_label_summary.csv"
MODEL_SCORECARD = RUN_DIR / "eb_model_scorecard.csv"
TRADE_SURFACE = RUN_DIR / "eb_validation_pf_floor_trade_surface.csv"
SELECTED_CANDIDATE = RUN_DIR / "selected_eb_candidate.json"
SELECTED_TRADE_TAPE = RUN_DIR / "selected_eb_trade_tape.csv"
MONTH_STABILITY = RUN_DIR / "selected_eb_month_stability.csv"
COST_STRESS = RUN_DIR / "selected_eb_cost_stress.csv"
MODEL_ARTIFACT_MANIFEST = RUN_DIR / "model_artifact_manifest.csv"
ONNX_SMOKE_REPORT = RUN_DIR / "onnx_smoke_report.csv"
DATA_INTEGRITY_AUDIT = RUN_DIR / "data_integrity_audit.csv"
RUN364EC_QUEUE = RUN_DIR / "run364EC_validation_pf_floor_review_queue.csv"
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

REPORT_PATH = REVIEW_DIR / "run364EB_h17_validation_pf_floor_density_recovery_reseed.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364EB_h17_validation_pf_floor_density_recovery_reseed.md"
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
    ea.FINAL_DECISION,
    ea.GATE_AUDIT,
    ea.REVIEW_SUMMARY,
    ea.FAILURE_MEMORY,
    ea.PACKAGE_DECISION,
    ea.RUN364EB_QUEUE,
    ea.REPORT_PATH,
    dz.FINAL_DECISION,
    dz.TRADE_SURFACE,
    dz.SELECTED_CANDIDATE,
    dz.SELECTED_TRADE_TAPE,
    dz.MONTH_STABILITY,
    dz.COST_STRESS,
    dz.MODEL_SCORECARD,
    dz.ONNX_SMOKE_REPORT,
    dz.DATA_INTEGRITY_AUDIT,
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
    RUN364EC_QUEUE,
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
    {"label_id": "pf_floor_dir_h1_m1", "horizon_m5": 1, "threshold_points": 1.0, "max_hold_m5": 1},
    {"label_id": "pf_floor_dir_h2_m1p5", "horizon_m5": 2, "threshold_points": 1.5, "max_hold_m5": 2},
    {"label_id": "pf_floor_dir_h2_m2", "horizon_m5": 2, "threshold_points": 2.0, "max_hold_m5": 2},
    {"label_id": "pf_floor_dir_h3_m2", "horizon_m5": 3, "threshold_points": 2.0, "max_hold_m5": 3},
]
DENSITY_TARGETS = [4, 5, 6, 7, 8, 9, 10, 12]
MARGINS = [-0.02, 0.0, 0.03, 0.06]
HOUR_SETS = {
    "all_hours": list(range(24)),
    "cash15_22": [15, 16, 17, 18, 19, 20, 21, 22],
    "pf_bridge_16_17_18_22": [16, 17, 18, 22],
    "validation_profit_16_22_plus_oos18": [16, 18, 22],
}
STABILITY_FILTERS = [
    "none",
    "no_h20",
    "no_h21",
    "no_h20_21",
    "no_h17_20",
    "no_h18_20",
    "no_validation_bad_hours_17_18_20",
    "gap_2pct_no20_21",
    "long_payoff_balance",
    "short_quality_long_keep",
    "drop_validation_bad_months_mar_may_jun_jul_sep",
]


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    return dv.rel(path)


def exists(path: Path | str) -> bool:
    return dv.exists(path)


def sha(path: Path | str) -> str:
    return dv.sha(path)


def read_json(path: Path) -> Any:
    return dv.read_json(path)


def write_json(path: Path, payload: Any) -> None:
    dv.write_json(path, dz.json_ready(payload))


def write_text(path: Path, text: str, *, bom: bool = True) -> None:
    dv.write_text(path, text, bom=bom)


def read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(io_path(path), encoding="utf-8-sig").fillna("")


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    materialized = [{str(key): dz.json_ready(value) for key, value in row.items()} for row in rows]
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fields: list[str] = []
        for row in materialized:
            for key in row:
                if key not in fields:
                    fields.append(key)
        fieldnames = fields or ["empty"]
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fieldnames), extrasaction="ignore")
        writer.writeheader()
        for row in materialized:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def append_or_replace_csv(path: Path, key_fields: Sequence[str], rows: Sequence[Mapping[str, Any]], *, extend_header: bool = True) -> None:
    dv.append_or_replace_csv(path, key_fields, [{str(key): dz.json_ready(value) for key, value in row.items()} for row in rows], extend_header=extend_header)


def append_text_once(path: Path, marker: str, text: str) -> None:
    dv.append_text_once(path, marker, text)


def replace_prefixed_lines(path: Path, replacements: Mapping[str, str], *, bom: bool = True) -> None:
    dv.replace_prefixed_lines(path, replacements, bom=bom)


def as_float(value: Any, default: float = 0.0) -> float:
    return dv.as_float(value, default)


def ensure_dirs() -> None:
    for path in [RUN_DIR, MODEL_DIR, ONNX_DIR, REVIEW_DIR, SPEC_DIR, SELECTED_DIR, DECISION_DOC.parent]:
        io_path(path).mkdir(parents=True, exist_ok=True)


def validate_inputs() -> dict[str, Any]:
    missing = [rel(path) for path in INPUT_FILES if path != Path(__file__) and not exists(path)]
    if missing:
        raise FileNotFoundError("missing EB inputs(EB 입력 누락): " + ", ".join(missing))
    parent = read_json(ea.FINAL_DECISION)
    if parent.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"EA next_run_id mismatch(EA 다음 실행 ID 불일치): {parent.get('next_run_id')} != {RUN_ID}")
    for key in ["runtime_authority", "operating_promotion", "live_readiness", "goal_achieve"]:
        if parent.get(key, "not_claimed") != "not_claimed":
            raise RuntimeError(f"EA forbidden claim(EA 금지 주장): {key}={parent.get(key)}")
    gates = read_csv(ea.GATE_AUDIT)
    if gates.empty or any(gates["status"].astype(str) != "passed"):
        raise RuntimeError("EA gate audit(EA 게이트 감사)가 모두 passed(통과)가 아닙니다.")
    return parent


def input_manifest_rows() -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "input_path": rel(path),
            "exists": exists(path),
            "sha256": sha(path) if exists(path) and io_path(path).is_file() else "",
            "input_role": "EB validation PF floor input(EB 검증 PF 바닥 입력)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for path in INPUT_FILES
    ]


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
            "hypothesis": "validation PF floor reward(검증 PF 바닥 보상)와 high-quality direction filters(고품질 방향 필터)가 no_h21/no_h20 OOS clue(21시/20시 제거 표본외 단서)를 잃지 않고 PF 1.20 양쪽 통과에 가까워질 수 있습니다.",
            "comparison_baseline": parent["parent_run_id"],
            "success_criteria": "validation/OOS net>0, PF>=1.20, density>=3(검증/표본외 순수익 양수, PF 1.20 이상, 밀도 3 이상)",
            "failure_criteria": "validation PF remains below floor or OOS clue collapses(검증 PF가 바닥 미만이거나 표본외 단서 붕괴)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def eb_model_specs() -> list[tuple[str, str, Any]]:
    return [
        (
            "et8_l50_n160(엑스트라트리8_잎50_160)",
            "ExtraTrees(엑스트라트리)",
            dv.dp.ExtraTreesClassifier(n_estimators=160, max_depth=8, min_samples_leaf=50, class_weight="balanced", random_state=401, n_jobs=-1),
        ),
        (
            "rf8_l60_n128(랜덤포레스트8_잎60_128)",
            "RandomForest(랜덤포레스트)",
            dv.dp.RandomForestClassifier(n_estimators=128, max_depth=8, min_samples_leaf=60, class_weight="balanced_subsample", random_state=402, n_jobs=-1),
        ),
    ]


def eb_stability_mask(frame: pd.DataFrame, score: np.ndarray, p_short: np.ndarray, p_long: np.ndarray, side: np.ndarray, filter_id: str) -> np.ndarray:
    timestamp = frame["timestamp"]
    hour = timestamp.dt.hour.to_numpy(dtype=int)
    month = timestamp.dt.month.to_numpy(dtype=int)
    direction_gap = np.abs(p_short - p_long)
    if filter_id == "none":
        return np.ones(len(frame), dtype=bool)
    if filter_id == "no_h20":
        return hour != 20
    if filter_id == "no_h21":
        return hour != 21
    if filter_id == "no_h20_21":
        return ~np.isin(hour, [20, 21])
    if filter_id == "no_h17_20":
        return ~np.isin(hour, [17, 20])
    if filter_id == "no_h18_20":
        return ~np.isin(hour, [18, 20])
    if filter_id == "no_validation_bad_hours_17_18_20":
        return ~np.isin(hour, [17, 18, 20])
    if filter_id == "gap_2pct_no20_21":
        return (direction_gap >= 0.02) & (~np.isin(hour, [20, 21]))
    if filter_id == "long_payoff_balance":
        return ((side == "long") & (direction_gap >= 0.010)) | ((side == "short") & (direction_gap >= 0.035) & (~np.isin(hour, [17, 18, 20])))
    if filter_id == "short_quality_long_keep":
        return ((side == "short") & (direction_gap >= 0.025) & (~np.isin(hour, [17, 20]))) | ((side == "long") & (direction_gap >= 0.015))
    if filter_id == "drop_validation_bad_months_mar_may_jun_jul_sep":
        return ~np.isin(month, [3, 5, 6, 7, 9])
    raise ValueError(f"unknown EB filter(알 수 없는 EB 필터): {filter_id}")


def eb_selection_score(row: Mapping[str, Any]) -> float:
    validation_net = as_float(row["validation_net"])
    oos_net = as_float(row["oos_net"])
    validation_pf = as_float(row["validation_profit_factor"])
    oos_pf = as_float(row["oos_profit_factor"])
    validation_density = as_float(row["validation_trade_density"])
    oos_density = as_float(row["oos_trade_density"])
    min_density = min(validation_density, oos_density)
    min_pf = min(validation_pf, oos_pf)
    pf_gap = max(0.0, 1.20 - min_pf)
    validation_pf_gap = max(0.0, 1.20 - validation_pf)
    oos_pf_gap = max(0.0, 1.20 - oos_pf)
    density_gap = max(0.0, 3.0 - min_density)
    return (
        0.58 * validation_net
        + 0.42 * oos_net
        + 620.0 * max(0.0, min_pf - 1.0)
        + 220.0 * max(0.0, validation_pf - 1.0)
        + 150.0 * max(0.0, oos_pf - 1.0)
        + 90.0 * min(min_density, 5.0)
        - 760.0 * pf_gap
        - 520.0 * validation_pf_gap
        - 380.0 * oos_pf_gap
        - 900.0 * density_gap
        - (380.0 if validation_net <= 0 else 0.0)
        - (300.0 if oos_net <= 0 else 0.0)
    )


def eb_selected_summary(surface_rows: Sequence[Mapping[str, Any]], smoke_rows: Sequence[Mapping[str, Any]], created_at: str) -> dict[str, Any]:
    smoke_pass = {str(row["model_id"]) for row in smoke_rows if str(row.get("status", "")).startswith("passed")}
    exportable_rows = [row for row in surface_rows if row["model_id"] in smoke_pass]
    strict_rows = [row for row in exportable_rows if str(row["strict_cross_split_success"]).startswith("passed")]
    density_rows = [
        row
        for row in exportable_rows
        if as_float(row["validation_trade_density"]) >= 3.0
        and as_float(row["oos_trade_density"]) >= 3.0
        and as_float(row["validation_net"]) > 0.0
        and as_float(row["oos_net"]) > 0.0
    ]
    pf_bridge_rows = [
        row
        for row in density_rows
        if as_float(row["validation_profit_factor"]) >= 1.10 and as_float(row["oos_profit_factor"]) >= 1.10
    ]
    pool = strict_rows or pf_bridge_rows or density_rows or exportable_rows or list(surface_rows)
    best = max(pool, key=lambda row: as_float(row["selection_score"]))
    strict_count = len(strict_rows)
    status = STATUS_STRICT if strict_count else STATUS_NO_STRICT
    judgment = JUDGMENT_STRICT if strict_count else JUDGMENT_NO_STRICT
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
        "selection_pool": "strict" if strict_rows else ("pf_bridge_density" if pf_bridge_rows else ("density_net" if density_rows else "exportable")),
    }


def patch_dv_module() -> None:
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
        "RUN364DW_QUEUE": RUN364EC_QUEUE,
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
        setattr(dv, name, value)
    dv.model_specs = eb_model_specs
    dv.stability_mask = eb_stability_mask
    dv.selection_score = eb_selection_score
    dv.selected_summary = eb_selected_summary


def write_queue(summary: Mapping[str, Any]) -> None:
    write_csv(
        RUN364EC_QUEUE,
        [
            {
                "run_id": RUN_ID,
                "next_run_id": NEXT_RUN_ID,
                "queue_rank": 1,
                "queue_id": "ec01_validation_pf_floor_review",
                "review_subject": summary["selected_model_id"],
                "review_question": "Did EB lift validation PF floor without losing OOS net/PF/density?(EB가 표본외 순수익/PF/밀도를 잃지 않고 검증 PF 바닥을 올렸는가?)",
                "strict_candidate_count": summary["strict_candidate_count"],
                "selected_validation_net": summary["selected_validation_net"],
                "selected_validation_profit_factor": summary["selected_validation_profit_factor"],
                "selected_validation_trade_density": summary["selected_validation_trade_density"],
                "selected_oos_net": summary["selected_oos_net"],
                "selected_oos_profit_factor": summary["selected_oos_profit_factor"],
                "selected_oos_trade_density": summary["selected_oos_trade_density"],
                "effect": "EC review(EC 검토)가 package(패키지) 가능성과 failure memory(실패 기억)를 분리 판정합니다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )


def write_receipts(final: Mapping[str, Any]) -> None:
    base = {"run_id": RUN_ID, "stage_id": STAGE_ID, "created_at_utc": final["created_at_utc"], "claim_boundary": CLAIM_BOUNDARY}
    write_json(RUN_EVIDENCE_RECEIPT, {**base, "surface": rel(TRADE_SURFACE), "selected_candidate": rel(SELECTED_CANDIDATE), "selected_trade_tape": rel(SELECTED_TRADE_TAPE), "measurement_boundary": "Python proxy with ONNX smoke, no MT5(Python 프록시와 ONNX 스모크, MT5 없음)"})
    write_json(EXPERIMENT_RECEIPT, {**base, "hypothesis": "validation PF floor reward can lift cross-split PF(검증 PF 바닥 보상이 교차 분할 PF를 올릴 수 있음)", "comparison_baseline": PARENT_RUN_ID, "success_criteria": "validation/OOS net>0 PF>=1.20 density>=3", "failure_criteria": "no strict cross-split candidate", "decision_use": NEXT_RUN_ID})
    write_json(DATA_RECEIPT, {**base, "data_source": [rel(dv.dp.MODEL_INPUT_DATASET), rel(dv.dp.RAW_US100_M5)], "time_axis": "UTC model input timestamp and raw open join(UTC 모델 입력 timestamp와 원천 open 결합)", "feature_label_boundary": "future_open only in labels", "split_boundary": "chronological train validation OOS", "integrity_judgment": "usable_with_proxy_boundary(프록시 경계 안에서 사용 가능)"})
    write_json(MODEL_RECEIPT, {**base, "model_family": "RandomForest/ExtraTrees(랜덤포레스트/엑스트라트리)", "selected_model_id": final["selected_model_id"], "onnx_smoke_pass_rows": final["onnx_smoke_pass_rows"], "validation_judgment": final["judgment"], "threshold_policy": "validation PF floor search(검증 PF 바닥 탐색)"})
    write_json(ATTRIBUTION_RECEIPT, {**base, "observed_change": f"selected validation {final['selected_validation_net']}/{final['selected_validation_profit_factor']}/{final['selected_validation_trade_density']}; OOS {final['selected_oos_net']}/{final['selected_oos_profit_factor']}/{final['selected_oos_trade_density']}", "likely_drivers": ["validation PF weighted score(검증 PF 가중 점수)", "density target extension(밀도 목표 확장)", "direction quality filters(방향 품질 필터)"], "next_probe": NEXT_RUN_ID})
    write_json(JUDGMENT_RECEIPT, {**base, "result_subject": RUN_ID, "evidence_available": [rel(TRADE_SURFACE), rel(SELECTED_CANDIDATE), rel(ONNX_SMOKE_REPORT), rel(DATA_INTEGRITY_AUDIT)], "evidence_missing": ["MT5 runtime package(MT5 런타임 패키지)", "MT5 runtime probe(MT5 런타임 탐침)", "forward/replay evidence(전진/재생 근거)"], "judgment_label": final["judgment"], "next_condition": NEXT_RUN_ID})
    write_json(LINEAGE_RECEIPT, {**base, "source_inputs": [{"path": rel(path), "sha256": sha(path)} for path in INPUT_FILES if exists(path) and io_path(path).is_file()], "producer": rel(Path(__file__)), "consumer": NEXT_RUN_ID, "artifact_paths": [rel(path) for path in OUTPUT_FILES if exists(path)], "artifact_hashes": {rel(path): sha(path) for path in OUTPUT_FILES if exists(path) and io_path(path).is_file()}, "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)], "lineage_judgment": "connected_validation_pf_floor_reseed(검증 PF 바닥 재시드 연결)"})
    write_json(CLAIM_RECEIPT, {**base, "runtime_package": "not_opened", "runtime_authority": "not_claimed", "operating_promotion": "not_claimed", "live_readiness": "not_claimed", "goal_achieve": "not_claimed", "effect": "EB 모델 단서를 운영 주장(operating claim, 운영 주장)으로 올리지 않습니다."})


def final_payload(summary: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    return {**summary, "gate_passes": sum(1 for row in gates if row["status"] == "passed"), "gate_total": len(gates)}


def write_docs(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    report = f"""# run364EB H17 Validation PF Floor Density Recovery Reseed(검증 PF 바닥 밀도 회복 재시드)

Created(생성): {final['created_at_utc']}

## Summary(요약)

Action(행동): EA failure memory(EA 실패 기억)를 받아 validation PF floor(검증 PF 바닥)를 직접 보상하는 label/filter/model sweep(라벨/필터/모델 탐색)을 실행했습니다.

Effect(효과): DZ의 OOS recovery clue(표본외 회복 단서)를 보존하면서 validation PF(검증 PF)를 끌어올릴 수 있는지 확인했습니다.

## Selected(선택)

- selected_model_id(선택 모델 ID): `{final['selected_model_id']}`
- selected_filter(선택 필터): `{final['selected_stability_filter']}`
- validation net/PF/density(검증 순수익/PF/밀도): `{final['selected_validation_net']}` / `{final['selected_validation_profit_factor']}` / `{final['selected_validation_trade_density']}`
- OOS net/PF/density(표본외 순수익/PF/밀도): `{final['selected_oos_net']}` / `{final['selected_oos_profit_factor']}` / `{final['selected_oos_trade_density']}`
- strict_candidate_count(엄격 후보 수): `{final['strict_candidate_count']}`

## Judgment(판정)

`{final['judgment']}`

Runtime package(런타임 패키지), runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.

## Next(다음)

`{NEXT_RUN_ID}`에서 EB validation PF floor seed(EB 검증 PF 바닥 씨앗)를 review(검토)합니다.

## Gates(게이트)

{chr(10).join(f"- {row['gate']}: {row['status']} -> {row['evidence']}" for row in gates)}
"""
    write_text(REPORT_PATH, report, bom=True)
    write_text(
        DECISION_DOC,
        f"""# Decision(결정): stage364EB validation PF floor density recovery reseed(검증 PF 바닥 밀도 회복 재시드)

- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{final['judgment']}`
- selected_model_id(선택 모델 ID): `{final['selected_model_id']}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Action(행동): validation PF floor search(검증 PF 바닥 탐색)를 실행했습니다.

Effect(효과): EC review(EC 검토)가 package(패키지) 가능성과 다음 실패 기억을 분리 판정하게 합니다.
""",
        bom=True,
    )
    append_text_once(REVIEW_INDEX, f"run364EB__{RUN_ID}", f"\n- run364EB__{RUN_ID}: [{REPORT_PATH.name}]({REPORT_PATH.name}) - validation PF floor density recovery reseed(검증 PF 바닥 밀도 회복 재시드), next `{NEXT_RUN_ID}`.\n")
    append_text_once(STAGE_BRIEF, f"run364EB__{RUN_ID}", f"\n<!-- run364EB__{RUN_ID} -->\n\n## run364EB Validation PF Floor Density Recovery(검증 PF 바닥 밀도 회복)\n\nAction(행동): validation PF floor(검증 PF 바닥)를 직접 보상하는 모델을 학습했습니다.\n\nEffect(효과): `{NEXT_RUN_ID}`에서 package(패키지) 가능성과 failure memory(실패 기억)를 검토합니다.\n")
    append_text_once(STAGE_README, f"run364EB__{RUN_ID}", f"\n<!-- run364EB__{RUN_ID} -->\n## run364EB validation PF floor density recovery(검증 PF 바닥 밀도 회복)\n\nSelected(선택): `{final['selected_model_id']}`. Strict candidates(엄격 후보): `{final['strict_candidate_count']}`. Next(다음): `{NEXT_RUN_ID}`.\n")
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

Current truth(현재 진실): `run364EB` trained(학습 완료) validation PF floor density recovery model(검증 PF 바닥 밀도 회복 모델). Selected validation/OOS net/PF/density(선택 검증/표본외 순수익/PF/밀도)는 `{final['selected_validation_net']}` / `{final['selected_validation_profit_factor']}` / `{final['selected_validation_trade_density']}` 및 `{final['selected_oos_net']}` / `{final['selected_oos_profit_factor']}` / `{final['selected_oos_trade_density']}`입니다. strict_candidate_count(엄격 후보 수)는 `{final['strict_candidate_count']}`입니다.

Next action(다음 행동): `{NEXT_RUN_ID}`에서 EB 검증 PF 바닥 씨앗을 review(검토)합니다.

Operating boundary(운영 경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""", bom=True)
    write_text(SELECTION_STATUS, f"""# Stage364 selection status(선택 상태)

Updated(갱신): {final['created_at_utc']}

Current run(현재 실행): `{NEXT_RUN_ID}`
Latest completed run(최근 완료 실행): `{RUN_ID}`

Latest scout(최근 탐색): EB validation PF floor density recovery(EB 검증 PF 바닥 밀도 회복)는 selected model(선택 모델) `{final['selected_model_id']}`를 만들었습니다.

Validation net/PF/density(검증 순수익/PF/밀도): `{final['selected_validation_net']}` / `{final['selected_validation_profit_factor']}` / `{final['selected_validation_trade_density']}`
OOS net/PF/density(표본외 순수익/PF/밀도): `{final['selected_oos_net']}` / `{final['selected_oos_profit_factor']}` / `{final['selected_oos_trade_density']}`

Authority(권위): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""", bom=True)
    append_text_once(WORKSPACE_CHANGELOG, f"run364EB__{RUN_ID}", f"\n<!-- run364EB__{RUN_ID} -->\n- {final['created_at_utc']} `{RUN_ID}` completed validation PF floor density recovery reseed(검증 PF 바닥 밀도 회복 재시드); strict candidates `{final['strict_candidate_count']}`; next `{NEXT_RUN_ID}`; no authority claim(권위 주장 없음).\n")
    append_text_once(IDEA_REGISTRY, f"run364EB__{RUN_ID}", f"\n<!-- run364EB__{RUN_ID} -->\n- `{RUN_ID}`: validation PF floor reward(검증 PF 바닥 보상)와 direction quality filters(방향 품질 필터)를 실험했습니다. Effect(효과): DZ의 OOS clue(표본외 단서)를 검증 PF 제약과 함께 다시 판독합니다.\n")
    if int(final["strict_candidate_count"]) == 0:
        append_text_once(NEGATIVE_REGISTER, f"run364EB__strict_candidate_absent__{RUN_ID}", f"\n<!-- run364EB__strict_candidate_absent__{RUN_ID} -->\n- `{RUN_ID}`: validation PF floor density recovery(검증 PF 바닥 밀도 회복)가 strict cross-split candidate(엄격 교차 분할 후보)를 만들지 못했습니다. Effect(효과): EC review(EC 검토)에서 salvage value(회수 가치)와 reopen condition(재개 조건)을 분리합니다.\n")


def write_ledgers(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    common = {"stage_id": STAGE_ID, "run_id": RUN_ID, "parent_run_id": PARENT_RUN_ID, "status": final["status"], "judgment": final["judgment"], "path": rel(FINAL_DECISION), "run_number": RUN_NUMBER, "date": TODAY, "decision": final["decision"], "next_run_id": NEXT_RUN_ID, "artifact_count": len([path for path in OUTPUT_FILES if exists(path)]), "gate_passes": sum(1 for row in gates if row["status"] == "passed"), "gate_total": len(gates), "claim_boundary": CLAIM_BOUNDARY, "report_path": rel(REPORT_PATH), "created_at_utc": final["created_at_utc"], "required_gate_audit": rel(GATE_AUDIT), "question": "Can validation PF floor recover without losing OOS density?(검증 PF 바닥이 표본외 밀도 손실 없이 회복되는가?)", "next_action": NEXT_RUN_ID, "notes": f"strict_candidate_count={final['strict_candidate_count']};onnx_smoke_pass_rows={final['onnx_smoke_pass_rows']}", "runtime_authority": "not_claimed", "operating_promotion": "not_claimed"}
    rows = []
    for suffix, record_view, tier_scope, status in [
        ("tier_a_separate", "Tier A separate(Tier A 분리)", "Tier A", final["status"]),
        ("tier_b_missing_required", "Tier B separate(Tier B 분리)", "Tier B", "missing_required_no_tier_b_model_input(필수 누락, Tier B 모델 입력 없음)"),
        ("tier_a_b_combined_out_of_scope", "Tier A+B combined(Tier A+B 합산)", "Tier A+B", "out_of_scope_by_claim_proxy_tier_a_only(주장 범위 밖, 프록시 Tier A 전용)"),
    ]:
        rows.append({**common, "ledger_row_id": f"{RUN_ID}__{suffix}", "subrun_id": f"{RUN_ID}__{suffix}", "row_id": f"{RUN_ID}__{suffix}", "record_view": record_view, "tier_scope": tier_scope, "view": record_view, "tier": tier_scope, "kpi_scope": "EB validation PF floor density recovery(EB 검증 PF 바닥 밀도 회복)", "metric_scope": "python_proxy_onnx_smoke(Python 프록시 ONNX 스모크)", "status": status, "net_profit": final["selected_oos_net"] if suffix == "tier_a_separate" else "", "profit_factor": final["selected_oos_profit_factor"] if suffix == "tier_a_separate" else "", "trade_density": final["selected_oos_trade_density"] if suffix == "tier_a_separate" else "", "trade_count": final["selected_oos_trade_count"] if suffix == "tier_a_separate" else "", "source_authority": "python_proxy_onnx_smoke_no_mt5(Python 프록시 ONNX 스모크, MT5 없음)"})
    append_or_replace_csv(STAGE_LEDGER, ["ledger_row_id"], rows, extend_header=True)
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], rows, extend_header=True)
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], [{**common, "run_family": "experiment_execution(실험 실행)", "run_type": "validation_pf_floor_density_recovery_model_reseed(검증 PF 바닥 밀도 회복 모델 재시드)", "input_run_id": PARENT_RUN_ID, "output_path": rel(FINAL_DECISION), "result_path": rel(TRADE_SURFACE), "selected_net_profit": final["selected_oos_net"], "selected_profit_factor": final["selected_oos_profit_factor"], "selected_trade_density": final["selected_oos_trade_density"]}], extend_header=True)
    dz.repair_run_registry_line_endings(RUN_ID)


def write_artifact_registry(final: Mapping[str, Any]) -> None:
    rows = []
    for path in OUTPUT_FILES:
        if exists(path) and io_path(path).is_file():
            rows.append({"stage_id": STAGE_ID, "run_id": RUN_ID, "artifact_type": "script" if path == Path(__file__) else ("report" if path.suffix.lower() == ".md" else ("json" if path.suffix.lower() == ".json" else "csv")), "path": rel(path), "artifact_path": rel(path), "sha256": sha(path), "created_at": final["created_at_utc"], "created_at_utc": final["created_at_utc"], "claim_boundary": CLAIM_BOUNDARY, "artifact_id": f"{RUN_ID}__{path.stem}", "notes": "EB validation PF floor density recovery artifact(EB 검증 PF 바닥 밀도 회복 산출물)"})
    append_or_replace_csv(ARTIFACT_REGISTRY, ["artifact_id"], rows, extend_header=True)


def write_manifest(final: Mapping[str, Any]) -> None:
    outputs = [path for path in OUTPUT_FILES if exists(path)]
    write_json(RUN_MANIFEST, {"run_id": RUN_ID, "run_number": RUN_NUMBER, "stage_id": STAGE_ID, "parent_run_id": PARENT_RUN_ID, "next_run_id": NEXT_RUN_ID, "status": final["status"], "judgment": final["judgment"], "claim_boundary": CLAIM_BOUNDARY, "input_files": [rel(path) for path in INPUT_FILES], "input_hashes": {rel(path): sha(path) for path in INPUT_FILES if exists(path) and io_path(path).is_file()}, "output_files": [rel(path) for path in outputs], "output_hashes": {rel(path): sha(path) for path in outputs if io_path(path).is_file()}})


def main() -> None:
    ensure_dirs()
    parent = validate_inputs()
    patch_dv_module()
    feature_order = dv.dt.load_feature_order()
    frame, _ = dv.load_frame()
    sets = dv.feature_sets(feature_order)
    write_csv(INPUT_MANIFEST, input_manifest_rows())
    write_work_packet(parent)
    dv.write_feature_audit(sets)
    dv.write_label_summary(frame)
    score_rows, surface_rows, trained, selected_trades = dv.train_and_score(frame, sets)
    write_csv(MODEL_SCORECARD, score_rows)
    write_csv(TRADE_SURFACE, surface_rows)
    dv.write_trade_auxiliary(selected_trades)
    _, smoke_rows = dv.export_models(trained)
    summary = dv.selected_summary(surface_rows, smoke_rows, now_utc())
    write_json(SELECTED_CANDIDATE, summary)
    write_queue(summary)
    data_rows = dv.data_integrity_rows(frame, feature_order, summary)
    gates = dv.gate_rows(summary, data_rows, final_written=False)
    final = final_payload(summary, gates)
    write_json(FINAL_DECISION, final)
    write_receipts(final)
    gates = dv.gate_rows(final, data_rows, final_written=True)
    final = final_payload(summary, gates)
    write_json(FINAL_DECISION, final)
    write_docs(final, gates)
    write_ledgers(final, gates)
    write_artifact_registry(final)
    write_manifest(final)
    print(json.dumps({"run_id": RUN_ID, "status": final["status"], "judgment": final["judgment"], "strict_candidate_count": final["strict_candidate_count"], "selected_model_id": final["selected_model_id"], "gate_passes": final["gate_passes"], "gate_total": final["gate_total"]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
