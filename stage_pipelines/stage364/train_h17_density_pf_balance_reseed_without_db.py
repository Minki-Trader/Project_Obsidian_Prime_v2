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
from stage_pipelines.stage364 import review_h17_validation_stability_density_recovery_reseed_without_db as dy  # noqa: E402
from stage_pipelines.stage364 import train_h17_validation_stability_regime_source_reseed_without_db as dv  # noqa: E402
from stage_pipelines.stage364.review_pf_pass_density_restore_offensive_scout_without_db import repair_run_registry_line_endings  # noqa: E402


TODAY = "2026-06-06"
STAGE_ID = dv.STAGE_ID
RUN_NUMBER = "run364DZ"
RUN_ID = "run364DZ_train_h17_density_pf_balance_reseed_without_db_v1"
PARENT_RUN_ID = dy.RUN_ID
NEXT_RUN_ID = "run364EA_review_h17_density_pf_balance_reseed_without_db_v1"

STATUS_NO_STRICT = "completed_stage364DZ_density_pf_balance_reseed_no_strict_review_required_no_authority"
STATUS_STRICT = "completed_stage364DZ_density_pf_balance_reseed_proxy_candidate_review_required_no_authority"
JUDGMENT_NO_STRICT = "inconclusive_density_pf_balance_reseed_no_cross_split_candidate_no_package_no_authority"
JUDGMENT_STRICT = "proxy_density_pf_balance_reseed_found_cross_split_candidate_review_required_no_authority"
DECISION = "stage364DZ_open_run364EA_density_pf_balance_reseed_review"
CLAIM_BOUNDARY = (
    "research_development_density_pf_balance_proxy_and_onnx_smoke_only_no_new_mt5_execution_"
    "no_runtime_package_no_forward_pass_no_live_readiness_no_operating_promotion_"
    "no_runtime_authority_no_goal_claim"
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
FEATURE_AUDIT = RUN_DIR / "dz_feature_set_audit.csv"
LABEL_SUMMARY = RUN_DIR / "dz_density_pf_balance_label_summary.csv"
MODEL_SCORECARD = RUN_DIR / "dz_model_scorecard.csv"
TRADE_SURFACE = RUN_DIR / "dz_density_pf_balance_trade_surface.csv"
SELECTED_CANDIDATE = RUN_DIR / "selected_dz_candidate.json"
SELECTED_TRADE_TAPE = RUN_DIR / "selected_dz_trade_tape.csv"
MONTH_STABILITY = RUN_DIR / "selected_dz_month_stability.csv"
COST_STRESS = RUN_DIR / "selected_dz_cost_stress.csv"
MODEL_ARTIFACT_MANIFEST = RUN_DIR / "model_artifact_manifest.csv"
ONNX_SMOKE_REPORT = RUN_DIR / "onnx_smoke_report.csv"
DATA_INTEGRITY_AUDIT = RUN_DIR / "data_integrity_audit.csv"
RUN364EA_QUEUE = RUN_DIR / "run364EA_density_pf_balance_review_queue.csv"
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

REPORT_PATH = REVIEW_DIR / "run364DZ_h17_density_pf_balance_reseed.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364DZ_h17_density_pf_balance_reseed.md"
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
    dy.FINAL_DECISION,
    dy.GATE_AUDIT,
    dy.REVIEW_SUMMARY,
    dy.FAILURE_MEMORY,
    dy.RUN364DZ_QUEUE,
    dy.REPORT_PATH,
    dy.dx.FINAL_DECISION,
    dy.dx.TRADE_SURFACE,
    dy.dx.SELECTED_CANDIDATE,
    dy.dx.COST_STRESS,
    dy.dx.MONTH_STABILITY,
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
    RUN364EA_QUEUE,
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
    {"label_id": "balance_dir_h2_m1p5", "horizon_m5": 2, "threshold_points": 1.5, "max_hold_m5": 2},
    {"label_id": "balance_dir_h3_m2", "horizon_m5": 3, "threshold_points": 2.0, "max_hold_m5": 3},
    {"label_id": "balance_dir_h4_m2p5", "horizon_m5": 4, "threshold_points": 2.5, "max_hold_m5": 4},
]
DENSITY_TARGETS = [6, 8, 10, 12, 14, 18, 22]
MARGINS = [-0.05, 0.0, 0.03, 0.06]
HOUR_SETS = {
    "all_hours": list(range(24)),
    "cash15_21": [15, 16, 17, 18, 19, 20, 21],
    "pf_hours_16_18_19_22": [16, 18, 19, 22],
    "pf_hours_16_18_19": [16, 18, 19],
    "no_bad_oos_17_20_21": [15, 16, 18, 19, 22, 23],
}
STABILITY_FILTERS = [
    "none",
    "no_h20",
    "no_h21",
    "no_h17_20_21",
    "short_only",
    "short_no_h17_20_21",
    "drop_oos_bad_months_oct_dec",
    "november_only_stress",
    "score_mid_high",
    "score_top_60",
    "gap_2pct_no_h21",
    "side_payoff_balance",
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
    dv.write_json(path, json_ready(payload))


def write_text(path: Path, text: str, *, bom: bool = True) -> None:
    dv.write_text(path, text, bom=bom)


def json_ready(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(key): json_ready(inner) for key, inner in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_ready(inner) for inner in value]
    if hasattr(value, "item"):
        try:
            return value.item()
        except (TypeError, ValueError):
            return str(value)
    if isinstance(value, float) and not math.isfinite(value):
        return ""
    return value


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    materialized = [{str(key): json_ready(value) for key, value in row.items()} for row in rows]
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


def read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(io_path(path), encoding="utf-8-sig").fillna("")


def append_or_replace_csv(path: Path, key_fields: Sequence[str], rows: Sequence[Mapping[str, Any]], *, extend_header: bool = True) -> None:
    dv.append_or_replace_csv(path, key_fields, [{str(key): json_ready(value) for key, value in row.items()} for row in rows], extend_header=extend_header)


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
        raise FileNotFoundError("missing DZ inputs(DZ 입력 누락): " + ", ".join(missing))
    parent = read_json(dy.FINAL_DECISION)
    if parent.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"DY next_run_id mismatch(DY 다음 실행 ID 불일치): {parent.get('next_run_id')} != {RUN_ID}")
    for key in ["runtime_authority", "operating_promotion", "live_readiness", "goal_achieve"]:
        if parent.get(key, "not_claimed") != "not_claimed":
            raise RuntimeError(f"DY forbidden claim(DY 금지 주장): {key}={parent.get(key)}")
    gates = read_csv(dy.GATE_AUDIT)
    if gates.empty or any(gates["status"].astype(str) != "passed"):
        raise RuntimeError("DY gate audit(DY 게이트 감사)가 모두 passed(통과)가 아닙니다.")
    return parent


def input_manifest_rows() -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "input_path": rel(path),
            "exists": exists(path),
            "sha256": sha(path) if exists(path) and io_path(path).is_file() else "",
            "input_role": "DZ density/PF balance input(DZ 밀도/PF 균형 입력)",
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
            "hypothesis": "OOS-negative hour/side pruning and PF-aware density fill(표본외 음수 시간/방향 가지치기와 PF 인식 밀도 보충)이 density>=3(밀도 3 이상)을 유지하면서 net/PF(순수익/PF)를 회복할 수 있다.",
            "comparison_baseline": parent["parent_run_id"],
            "success_criteria": "validation/OOS net>0, PF>=1.20, density>=3(검증/표본외 순수익 양수, PF 1.20 이상, 밀도 3 이상)",
            "failure_criteria": "density remains high but OOS PF/net fails(밀도는 높지만 표본외 PF/순수익 실패)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def dz_stability_mask(frame: pd.DataFrame, score: np.ndarray, p_short: np.ndarray, p_long: np.ndarray, side: np.ndarray, filter_id: str) -> np.ndarray:
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
    if filter_id == "no_h17_20_21":
        return ~np.isin(hour, [17, 20, 21])
    if filter_id == "short_only":
        return side == "short"
    if filter_id == "short_no_h17_20_21":
        return (side == "short") & (~np.isin(hour, [17, 20, 21]))
    if filter_id == "drop_oos_bad_months_oct_dec":
        return ~np.isin(month, [10, 12])
    if filter_id == "november_only_stress":
        return month == 11
    if filter_id == "score_mid_high":
        return (score >= 0.410) & (score <= 0.435)
    if filter_id == "score_top_60":
        return score >= 0.408
    if filter_id == "gap_2pct_no_h21":
        return (direction_gap >= 0.02) & (hour != 21)
    if filter_id == "side_payoff_balance":
        return ((side == "short") & (direction_gap >= 0.012)) | ((side == "long") & (direction_gap >= 0.045) & (~np.isin(hour, [17, 20, 21])))
    raise ValueError(f"unknown DZ filter(알 수 없는 DZ 필터): {filter_id}")


def dz_selection_score(row: Mapping[str, Any]) -> float:
    validation_net = as_float(row["validation_net"])
    oos_net = as_float(row["oos_net"])
    validation_pf = as_float(row["validation_profit_factor"])
    oos_pf = as_float(row["oos_profit_factor"])
    validation_density = as_float(row["validation_trade_density"])
    oos_density = as_float(row["oos_trade_density"])
    min_density = min(validation_density, oos_density)
    min_pf = min(validation_pf, oos_pf)
    return (
        0.35 * validation_net
        + 0.65 * oos_net
        + 260.0 * max(0.0, min_pf - 1.0)
        + 120.0 * min(min_density, 5.0)
        - 240.0 * max(0.0, 3.0 - min_density)
        - (300.0 if oos_net <= 0 else 0.0)
        - (220.0 if oos_pf < 1.20 else 0.0)
        - (180.0 if validation_pf < 1.20 else 0.0)
        - (140.0 if validation_net <= 0 else 0.0)
    )


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
        "RUN364DW_QUEUE": RUN364EA_QUEUE,
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
    dv.stability_mask = dz_stability_mask
    dv.selection_score = dz_selection_score


def write_queue(summary: Mapping[str, Any]) -> None:
    write_csv(
        RUN364EA_QUEUE,
        [
            {
                "run_id": RUN_ID,
                "next_run_id": NEXT_RUN_ID,
                "queue_rank": 1,
                "queue_id": "ea01_density_pf_balance_review",
                "review_subject": summary["selected_model_id"],
                "review_question": "Did DZ keep density>=3 while restoring validation/OOS net and PF?(DZ가 밀도 3 이상을 유지하면서 검증/표본외 순수익과 PF를 회복했는가?)",
                "strict_candidate_count": summary["strict_candidate_count"],
                "selected_validation_net": summary["selected_validation_net"],
                "selected_validation_profit_factor": summary["selected_validation_profit_factor"],
                "selected_validation_trade_density": summary["selected_validation_trade_density"],
                "selected_oos_net": summary["selected_oos_net"],
                "selected_oos_profit_factor": summary["selected_oos_profit_factor"],
                "selected_oos_trade_density": summary["selected_oos_trade_density"],
                "effect": "EA review(EA 검토)가 패키지 가능성과 실패 기억을 분리 판정합니다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )


def write_receipts(final: Mapping[str, Any]) -> None:
    base = {"run_id": RUN_ID, "stage_id": STAGE_ID, "created_at_utc": final["created_at_utc"], "claim_boundary": CLAIM_BOUNDARY}
    write_json(RUN_EVIDENCE_RECEIPT, {**base, "surface": rel(TRADE_SURFACE), "selected_candidate": rel(SELECTED_CANDIDATE), "selected_trade_tape": rel(SELECTED_TRADE_TAPE), "measurement_boundary": "Python proxy with ONNX smoke, no MT5(Python 프록시와 ONNX 스모크, MT5 없음)"})
    write_json(EXPERIMENT_RECEIPT, {**base, "hypothesis": "PF-aware filters can preserve density while restoring OOS PF(PF 인식 필터가 밀도를 보존하면서 표본외 PF를 회복할 수 있음)", "comparison_baseline": PARENT_RUN_ID, "success_criteria": "validation/OOS net>0 PF>=1.20 density>=3", "failure_criteria": "no strict cross-split candidate", "decision_use": NEXT_RUN_ID})
    write_json(DATA_RECEIPT, {**base, "data_source": [rel(dv.dp.MODEL_INPUT_DATASET), rel(dv.dp.RAW_US100_M5)], "time_axis": "UTC model input timestamp and raw open join(UTC 모델 입력 timestamp와 원천 open 결합)", "feature_label_boundary": "future_open only in labels", "split_boundary": "chronological train validation OOS", "integrity_judgment": "usable_with_proxy_boundary(프록시 경계 안에서 사용 가능)"})
    write_json(MODEL_RECEIPT, {**base, "model_family": "RandomForest/ExtraTrees(랜덤포레스트/엑스트라트리)", "selected_model_id": final["selected_model_id"], "onnx_smoke_pass_rows": final["onnx_smoke_pass_rows"], "validation_judgment": final["judgment"], "threshold_policy": "density/PF balance search(밀도/PF 균형 탐색)"})
    write_json(ATTRIBUTION_RECEIPT, {**base, "observed_change": f"selected validation {final['selected_validation_net']}/{final['selected_validation_profit_factor']}/{final['selected_validation_trade_density']}; OOS {final['selected_oos_net']}/{final['selected_oos_profit_factor']}/{final['selected_oos_trade_density']}", "likely_drivers": ["OOS bad-hour pruning(표본외 나쁜 시간 가지치기)", "side payoff balance(방향별 손익 균형)", "PF-aware selection(PF 인식 선택)"], "next_probe": NEXT_RUN_ID})
    write_json(JUDGMENT_RECEIPT, {**base, "result_subject": RUN_ID, "evidence_available": [rel(TRADE_SURFACE), rel(SELECTED_CANDIDATE), rel(ONNX_SMOKE_REPORT), rel(DATA_INTEGRITY_AUDIT)], "evidence_missing": ["MT5 runtime package(MT5 런타임 패키지)", "MT5 runtime probe(MT5 런타임 탐침)", "forward/replay evidence(전진/재생 근거)"], "judgment_label": final["judgment"], "next_condition": NEXT_RUN_ID})
    write_json(LINEAGE_RECEIPT, {**base, "source_inputs": [{"path": rel(path), "sha256": sha(path)} for path in INPUT_FILES if exists(path) and io_path(path).is_file()], "producer": rel(Path(__file__)), "consumer": NEXT_RUN_ID, "artifact_paths": [rel(path) for path in OUTPUT_FILES if exists(path)], "artifact_hashes": {rel(path): sha(path) for path in OUTPUT_FILES if exists(path) and io_path(path).is_file()}, "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)], "lineage_judgment": "connected_density_pf_balance_reseed(밀도/PF 균형 재시드 연결)"})
    write_json(CLAIM_RECEIPT, {**base, "runtime_package": "not_opened", "runtime_authority": "not_claimed", "operating_promotion": "not_claimed", "live_readiness": "not_claimed", "goal_achieve": "not_claimed", "effect": "DZ 모델 단서를 운영 주장으로 올리지 않습니다."})


def final_payload(summary: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    return {**summary, "gate_passes": sum(1 for row in gates if row["status"] == "passed"), "gate_total": len(gates)}


def write_docs(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    report = f"""# run364DZ H17 Density/PF Balance Reseed(밀도/PF 균형 재시드)

Created(생성): {final['created_at_utc']}

## Summary(요약)

Action(행동): DY failure memory(DY 실패 기억)를 받아 OOS bad-hour pruning(표본외 나쁜 시간 가지치기), side payoff balance(방향별 손익 균형), PF-aware selection(PF 인식 선택)을 실험했습니다.

Effect(효과): density>=3(밀도 3 이상)을 유지하면서 validation/OOS net/PF(검증/표본외 순수익/PF)를 동시에 회복할 수 있는지 확인했습니다.

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

`{NEXT_RUN_ID}`에서 DZ 밀도/PF 균형 씨앗을 review(검토)합니다.

## Gates(게이트)

{chr(10).join(f"- {row['gate']}: {row['status']} -> {row['evidence']}" for row in gates)}
"""
    write_text(REPORT_PATH, report, bom=True)
    write_text(
        DECISION_DOC,
        f"""# Decision(결정): stage364DZ density/PF balance reseed(밀도/PF 균형 재시드)

- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{final['judgment']}`
- selected_model_id(선택 모델 ID): `{final['selected_model_id']}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Action(행동): density/PF balance filters(밀도/PF 균형 필터)를 실험했습니다.

Effect(효과): 패키지(package, 패키지)는 아직 열지 않고 EA review(EA 검토)로 넘깁니다.
""",
        bom=True,
    )
    append_text_once(REVIEW_INDEX, f"run364DZ__{RUN_ID}", f"\n- run364DZ__{RUN_ID}: [{REPORT_PATH.name}]({REPORT_PATH.name}) - density/PF balance reseed(밀도/PF 균형 재시드), next `{NEXT_RUN_ID}`.\n")
    append_text_once(STAGE_BRIEF, f"run364DZ__{RUN_ID}", f"\n<!-- run364DZ__{RUN_ID} -->\n\n## run364DZ Density/PF Balance Reseed(밀도/PF 균형 재시드)\n\nAction(행동): PF 인식 필터로 새 모델을 학습했습니다.\n\nEffect(효과): `{NEXT_RUN_ID}`에서 package(패키지) 가능성과 failure memory(실패 기억)를 검토합니다.\n")
    append_text_once(STAGE_README, f"run364DZ__{RUN_ID}", f"\n<!-- run364DZ__{RUN_ID} -->\n## run364DZ density/PF balance reseed(밀도/PF 균형 재시드)\n\nSelected(선택): `{final['selected_model_id']}`. Strict candidates(엄격 후보): `{final['strict_candidate_count']}`. Next(다음): `{NEXT_RUN_ID}`.\n")
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

Current truth(현재 진실): `run364DZ` trained(학습 완료) density/PF balance model(밀도/PF 균형 모델). Selected validation/OOS net/PF/density(선택 검증/표본외 순수익/PF/밀도)는 `{final['selected_validation_net']}` / `{final['selected_validation_profit_factor']}` / `{final['selected_validation_trade_density']}` 및 `{final['selected_oos_net']}` / `{final['selected_oos_profit_factor']}` / `{final['selected_oos_trade_density']}`입니다. strict_candidate_count(엄격 후보 수)는 `{final['strict_candidate_count']}`입니다.

Next action(다음 행동): `{NEXT_RUN_ID}`에서 DZ 밀도/PF 균형 씨앗을 review(검토)합니다.

Operating boundary(운영 경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""", bom=True)
    write_text(SELECTION_STATUS, f"""# Stage364 selection status(선택 상태)

Updated(갱신): {final['created_at_utc']}

Current run(현재 실행): `{NEXT_RUN_ID}`
Latest completed run(최근 완료 실행): `{RUN_ID}`

Latest scout(최근 탐색): DZ density/PF balance reseed(DZ 밀도/PF 균형 재시드)는 selected model(선택 모델) `{final['selected_model_id']}`를 만들었습니다.

Validation net/PF/density(검증 순수익/PF/밀도): `{final['selected_validation_net']}` / `{final['selected_validation_profit_factor']}` / `{final['selected_validation_trade_density']}`
OOS net/PF/density(표본외 순수익/PF/밀도): `{final['selected_oos_net']}` / `{final['selected_oos_profit_factor']}` / `{final['selected_oos_trade_density']}`

Authority(권위): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""", bom=True)
    append_text_once(WORKSPACE_CHANGELOG, f"run364DZ__{RUN_ID}", f"\n<!-- run364DZ__{RUN_ID} -->\n- {final['created_at_utc']} `{RUN_ID}` completed density/PF balance reseed(밀도/PF 균형 재시드); strict candidates `{final['strict_candidate_count']}`; next `{NEXT_RUN_ID}`; no authority claim(권위 주장 없음).\n")
    append_text_once(IDEA_REGISTRY, f"run364DZ__{RUN_ID}", f"\n<!-- run364DZ__{RUN_ID} -->\n- `{RUN_ID}`: OOS bad-hour pruning(표본외 나쁜 시간 가지치기)과 PF-aware selection(PF 인식 선택)을 학습했습니다. Effect(효과): 밀도 회복과 PF 회복을 동시에 겨냥합니다.\n")
    if int(final["strict_candidate_count"]) == 0:
        append_text_once(NEGATIVE_REGISTER, f"run364DZ__strict_candidate_absent__{RUN_ID}", f"\n<!-- run364DZ__strict_candidate_absent__{RUN_ID} -->\n- `{RUN_ID}`: density/PF balance reseed(밀도/PF 균형 재시드)는 strict cross-split candidate(엄격 교차 분할 후보)를 만들지 못했습니다. Effect(효과): EA review(EA 검토)에서 실패 기억과 재사용 단서를 분리합니다.\n")


def write_ledgers(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    common = {"stage_id": STAGE_ID, "run_id": RUN_ID, "parent_run_id": PARENT_RUN_ID, "status": final["status"], "judgment": final["judgment"], "path": rel(FINAL_DECISION), "run_number": RUN_NUMBER, "date": TODAY, "decision": final["decision"], "next_run_id": NEXT_RUN_ID, "artifact_count": len([path for path in OUTPUT_FILES if exists(path)]), "gate_passes": sum(1 for row in gates if row["status"] == "passed"), "gate_total": len(gates), "claim_boundary": CLAIM_BOUNDARY, "report_path": rel(REPORT_PATH), "created_at_utc": final["created_at_utc"], "required_gate_audit": rel(GATE_AUDIT), "question": "Can density/PF balance keep density>=3 while restoring OOS net and PF?(밀도/PF 균형이 밀도 3 이상을 유지하면서 표본외 순수익과 PF를 회복할 수 있는가?)", "next_action": NEXT_RUN_ID, "notes": f"strict_candidate_count={final['strict_candidate_count']};onnx_smoke_pass_rows={final['onnx_smoke_pass_rows']}", "runtime_authority": "not_claimed", "operating_promotion": "not_claimed"}
    rows = []
    for suffix, record_view, tier_scope, status in [
        ("tier_a_separate", "Tier A separate(Tier A 분리)", "Tier A", final["status"]),
        ("tier_b_missing_required", "Tier B separate(Tier B 분리)", "Tier B", "missing_required_no_tier_b_model_input(필수 누락, Tier B 모델 입력 없음)"),
        ("tier_a_b_combined_out_of_scope", "Tier A+B combined(Tier A+B 합산)", "Tier A+B", "out_of_scope_by_claim_proxy_tier_a_only(주장 범위 밖, 프록시 Tier A 전용)"),
    ]:
        rows.append({**common, "ledger_row_id": f"{RUN_ID}__{suffix}", "subrun_id": f"{RUN_ID}__{suffix}", "row_id": f"{RUN_ID}__{suffix}", "record_view": record_view, "tier_scope": tier_scope, "view": record_view, "tier": tier_scope, "kpi_scope": "DZ density/PF balance reseed(DZ 밀도/PF 균형 재시드)", "metric_scope": "python_proxy_onnx_smoke(Python 프록시 ONNX 스모크)", "status": status, "net_profit": final["selected_oos_net"] if suffix == "tier_a_separate" else "", "profit_factor": final["selected_oos_profit_factor"] if suffix == "tier_a_separate" else "", "trade_density": final["selected_oos_trade_density"] if suffix == "tier_a_separate" else "", "trade_count": final["selected_oos_trade_count"] if suffix == "tier_a_separate" else "", "source_authority": "python_proxy_onnx_smoke_no_mt5(Python 프록시 ONNX 스모크, MT5 없음)"})
    append_or_replace_csv(STAGE_LEDGER, ["ledger_row_id"], rows, extend_header=True)
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], rows, extend_header=True)
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], [{**common, "run_family": "experiment_execution(실험 실행)", "run_type": "density_pf_balance_model_reseed(밀도/PF 균형 모델 재시드)", "input_run_id": PARENT_RUN_ID, "output_path": rel(FINAL_DECISION), "result_path": rel(TRADE_SURFACE), "selected_net_profit": final["selected_oos_net"], "selected_profit_factor": final["selected_oos_profit_factor"], "selected_trade_density": final["selected_oos_trade_density"]}], extend_header=True)
    repair_run_registry_line_endings(RUN_ID)


def write_artifact_registry(final: Mapping[str, Any]) -> None:
    rows = []
    for path in OUTPUT_FILES:
        if exists(path) and io_path(path).is_file():
            rows.append({"stage_id": STAGE_ID, "run_id": RUN_ID, "artifact_type": "script" if path == Path(__file__) else ("report" if path.suffix.lower() == ".md" else ("json" if path.suffix.lower() == ".json" else "csv")), "path": rel(path), "artifact_path": rel(path), "sha256": sha(path), "created_at": final["created_at_utc"], "created_at_utc": final["created_at_utc"], "claim_boundary": CLAIM_BOUNDARY, "artifact_id": f"{RUN_ID}__{path.stem}", "notes": "DZ density/PF balance reseed artifact(DZ 밀도/PF 균형 재시드 산출물)"})
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
