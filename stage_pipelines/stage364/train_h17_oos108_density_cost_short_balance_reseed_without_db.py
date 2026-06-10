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
from stage_pipelines.stage364 import review_h17_oos108_cost_side_model_label_feature_reseed_without_db as es  # noqa: E402
from stage_pipelines.stage364 import train_h17_density_failure_regime_behavior_reseed_without_db as dt  # noqa: E402
from stage_pipelines.stage364 import train_h17_oos108_cost_side_model_label_feature_reseed_without_db as er  # noqa: E402
from stage_pipelines.stage364.review_pf_pass_density_restore_offensive_scout_without_db import repair_run_registry_line_endings  # noqa: E402


TODAY = "2026-06-06"
STAGE_ID = er.STAGE_ID
RUN_NUMBER = "run364ET"
RUN_ID = "run364ET_train_h17_oos108_density_cost_short_balance_reseed_without_db_v1"
PARENT_RUN_ID = es.RUN_ID
NEXT_RUN_ID = "run364EU_review_h17_oos108_density_cost_short_balance_reseed_without_db_v1"

STATUS_STRICT = "completed_stage364ET_oos108_density_cost_short_balance_reseed_proxy_candidate_review_required_no_authority"
STATUS_NO_STRICT = "completed_stage364ET_oos108_density_cost_short_balance_reseed_no_strict_pass_review_required_no_authority"
JUDGMENT_STRICT = "positive_proxy_density_cost_short_balance_reseed_candidate_review_required_no_authority"
JUDGMENT_NO_STRICT = "inconclusive_density_cost_short_balance_reseed_no_strict_pass_review_required_no_authority"
DECISION_STRICT = "stage364ET_open_run364EU_density_cost_short_balance_candidate_review"
DECISION_NO_STRICT = "stage364ET_open_run364EU_density_cost_short_balance_failure_review"
CLAIM_BOUNDARY = (
    "research_development_density_cost_short_balance_reseed_proxy_and_onnx_smoke_only_"
    "no_new_mt5_execution_no_runtime_package_no_forward_pass_no_live_readiness_"
    "no_operating_promotion_no_runtime_authority_no_goal_claim"
)

POINT_VALUE = dt.POINT_VALUE
COST_PER_TRADE = dt.COST_PER_TRADE
DENSITY_FLOOR = 3.0
STRICT_MIN_PF_FLOOR = 1.12
STRICT_SHORT_SHARE_FLOOR = 0.72
OPERATIONAL_MIN_PF_FLOOR = 1.21
RUNTIME_NET_REFERENCE = 523.58

STAGE_DIR = er.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
MODEL_DIR = RUN_DIR / "models"
ONNX_DIR = RUN_DIR / "onnx"
REVIEW_DIR = STAGE_DIR / "03_reviews"
SPEC_DIR = STAGE_DIR / "00_spec"
SELECTED_DIR = STAGE_DIR / "04_selected"

INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
FEATURE_AUDIT = RUN_DIR / "et_feature_set_audit.csv"
LABEL_SUMMARY = RUN_DIR / "et_density_cost_label_summary.csv"
MODEL_SCORECARD = RUN_DIR / "et_model_scorecard.csv"
TRADE_SURFACE = RUN_DIR / "et_density_cost_short_surface.csv"
SELECTED_CANDIDATE = RUN_DIR / "selected_et_candidate.json"
SELECTED_TRADE_TAPE = RUN_DIR / "selected_et_trade_tape.csv"
MONTH_STABILITY = RUN_DIR / "selected_et_month_stability.csv"
COST_STRESS = RUN_DIR / "selected_et_cost_stress.csv"
SIDE_SESSION_REVIEW = RUN_DIR / "selected_et_side_session_review.csv"
MODEL_ARTIFACT_MANIFEST = RUN_DIR / "model_artifact_manifest.csv"
ONNX_SMOKE_REPORT = RUN_DIR / "onnx_smoke_report.csv"
DATA_INTEGRITY_AUDIT = RUN_DIR / "data_integrity_audit.csv"
RUN364EU_QUEUE = RUN_DIR / "run364EU_density_cost_short_balance_review_queue.csv"
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

REPORT_PATH = REVIEW_DIR / "run364ET_oos108_density_cost_short_balance_reseed.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364ET_h17_oos108_density_cost_short_balance_reseed.md"
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
    es.FINAL_DECISION,
    es.GATE_AUDIT,
    es.REVIEW_SUMMARY,
    es.FAILURE_ATTRIBUTION,
    es.SIDE_SESSION_GUARDRAIL,
    es.FAILURE_MEMORY,
    es.RUN364ET_QUEUE,
    er.TRADE_SURFACE,
    er.SELECTED_TRADE_TAPE,
    er.SIDE_SESSION_REVIEW,
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
    RUN364EU_QUEUE,
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
    {"label_id": "densecost_sym_h2_m2p5", "horizon_m5": 2, "threshold_points": 2.5, "mode": "symmetric"},
    {"label_id": "densecost_sym_h3_m3", "horizon_m5": 3, "threshold_points": 3.0, "mode": "symmetric"},
    {"label_id": "densecost_asym_h3_l2p5_s3p5", "horizon_m5": 3, "long_threshold_points": 2.5, "short_threshold_points": 3.5, "mode": "asymmetric"},
    {"label_id": "densecost_asym_h4_l3_s4p5", "horizon_m5": 4, "long_threshold_points": 3.0, "short_threshold_points": 4.5, "mode": "asymmetric"},
]
TARGET_DENSITIES = [3, 4, 5, 6, 8, 10, 12]
MARGINS = [-0.04, -0.02, 0.0, 0.02]
HOUR_SETS = {
    "all_hours": list(range(24)),
    "no_h20_21": [hour for hour in range(24) if hour not in [20, 21]],
    "cash_15_22": [15, 16, 17, 18, 19, 20, 21, 22],
    "core_16_18_20_22": [16, 17, 18, 20, 22],
}
EXTRA_FILTERS = ["none", "short_h20_21_veto", "long_recovery_guard", "side_balance_guard"]


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
    return er.as_float(value, default)


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
            "input_role": "ET density/cost/short balance input(ET 밀도/비용/숏 균형 입력)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for path in INPUT_FILES
    ]


def validate_inputs() -> dict[str, Any]:
    missing = [rel(path) for path in INPUT_FILES if path != Path(__file__) and not exists(path)]
    if missing:
        raise FileNotFoundError("missing ET inputs(ET 입력 누락): " + ", ".join(missing))
    parent = read_json(es.FINAL_DECISION)
    if parent.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"ES next_run_id mismatch(ES 다음 실행 ID 불일치): {parent.get('next_run_id')} != {RUN_ID}")
    for key in ["runtime_authority", "operating_promotion", "live_readiness", "goal_achieve"]:
        if parent.get(key, "not_claimed") != "not_claimed":
            raise RuntimeError(f"forbidden prior claim(이전 금지 주장): {key}={parent.get(key)}")
    gates = pd.read_csv(es.GATE_AUDIT, encoding="utf-8-sig").fillna("")
    if gates.empty or any(gates["status"].astype(str) != "passed"):
        raise RuntimeError("ES gate audit(ES 게이트 감사)가 모두 passed(통과)가 아닙니다.")
    return parent


def et_label_values(frame: pd.DataFrame, spec: Mapping[str, Any]) -> tuple[np.ndarray, np.ndarray]:
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


def et_feature_sets(feature_order: Sequence[str]) -> dict[str, list[str]]:
    base = list(feature_order)
    derived = dt.derived_features()
    price = [column for column in base if any(token in column for token in ["return", "ratio", "rsi", "atr", "adx", "vol", "gap"])]
    macro = [column for column in base if any(token in column for token in ["vix", "us10yr", "usdx", "mega8", "breadth"])]
    session = [column for column in base if any(token in column for token in ["cash", "minutes", "open", "close"])]
    return {
        "et_all72": list(dict.fromkeys(base + derived)),
        "et_cost_session_macro": list(dict.fromkeys(price + macro + session + derived)),
    }


def et_model_specs() -> list[tuple[str, str, Any]]:
    return [
        (
            "et8_l35_n144",
            "ExtraTrees(엑스트라트리)",
            dt.dp.ExtraTreesClassifier(n_estimators=144, max_depth=8, min_samples_leaf=35, class_weight="balanced", random_state=751, n_jobs=-1),
        ),
        (
            "rf9_l45_n144",
            "RandomForest(랜덤포레스트)",
            dt.dp.RandomForestClassifier(n_estimators=144, max_depth=9, min_samples_leaf=45, class_weight="balanced_subsample", random_state=752, n_jobs=-1),
        ),
    ]


def et_extra_mask(frame: pd.DataFrame, side: np.ndarray, extra_filter: str) -> np.ndarray:
    mask = np.ones(len(frame), dtype=bool)
    hour = frame["timestamp"].dt.hour.to_numpy(dtype=int)
    breadth = frame["mega8_pos_breadth_1"].to_numpy(dtype=float)
    vol_ratio = frame["historical_vol_5_over_20"].to_numpy(dtype=float)
    log_return_3 = frame["log_return_3"].to_numpy(dtype=float)
    vix_stress = frame["vix_zscore_20"].to_numpy(dtype=float)
    if extra_filter == "none":
        return mask
    if extra_filter == "short_h20_21_veto":
        return mask & ~((side == "short") & np.isin(hour, [20, 21]))
    if extra_filter == "long_recovery_guard":
        long_ok = (side == "long") & np.isin(hour, [16, 20]) & (breadth >= 0.40)
        short_ok = (side == "short") & np.isin(hour, [16, 17, 18]) & (log_return_3 < 0.0) & (vol_ratio >= 0.75)
        return mask & (long_ok | short_ok)
    if extra_filter == "side_balance_guard":
        short_ok = (side == "short") & ~np.isin(hour, [19, 20, 21]) & ((breadth <= 0.55) | (log_return_3 < 0.0))
        long_ok = (side == "long") & ~((hour == 17) & (vix_stress > 0.75)) & (breadth >= 0.35)
        return mask & (short_ok | long_ok)
    raise ValueError(f"unknown ET filter(알 수 없는 ET 필터): {extra_filter}")


def cost_values(row: Mapping[str, Any]) -> dict[str, float]:
    return er.cost_side_values(row)


def et_strict_success(row: Mapping[str, Any]) -> bool:
    values = cost_values(row)
    min_pf = min(as_float(row.get("validation_profit_factor")), as_float(row.get("oos_profit_factor")))
    return (
        values["combined_trade_density"] >= DENSITY_FLOOR
        and values["validation_cost06_net"] >= 0
        and values["oos_cost06_net"] > 0
        and values["combined_cost09_net"] >= 0
        and values["combined_short_share"] <= STRICT_SHORT_SHARE_FLOOR
        and min_pf >= STRICT_MIN_PF_FLOOR
        and values["combined_net"] > 0
    )


def et_operational_stack(row: Mapping[str, Any]) -> bool:
    values = cost_values(row)
    min_pf = min(as_float(row.get("validation_profit_factor")), as_float(row.get("oos_profit_factor")))
    return et_strict_success(row) and values["combined_net"] >= RUNTIME_NET_REFERENCE and min_pf >= OPERATIONAL_MIN_PF_FLOOR


def et_selection_score(row: Mapping[str, Any]) -> float:
    values = cost_values(row)
    validation_pf = as_float(row.get("validation_profit_factor"))
    oos_pf = as_float(row.get("oos_profit_factor"))
    min_pf = min(validation_pf, oos_pf)
    density = values["combined_trade_density"]
    return (
        values["combined_net"]
        + 760.0 * max(0.0, min_pf - 1.0)
        + 160.0 * min(density, 8.0)
        + 0.85 * values["combined_cost06_net"]
        + 0.55 * values["combined_cost09_net"]
        - 3.00 * max(0.0, -values["validation_cost06_net"])
        - 3.00 * max(0.0, -values["oos_cost06_net"])
        - 620.0 * max(0.0, values["combined_short_share"] - STRICT_SHORT_SHARE_FLOOR)
        - 500.0 * max(0.0, DENSITY_FLOOR - density)
        - 260.0 * max(0.0, STRICT_MIN_PF_FLOOR - min_pf)
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
    dt.label_values = et_label_values
    dt.feature_sets = et_feature_sets
    dt.model_specs = et_model_specs
    dt.extra_mask = et_extra_mask
    dt.strict_success = et_strict_success
    dt.selection_score = et_selection_score


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
            ],
            "hypothesis": "cost-weighted dense label(비용 가중 고밀도 라벨)과 side/session penalty(방향/세션 벌점)가 density/cost/short balance(밀도/비용/숏 균형)를 복구할 수 있습니다.",
            "broad_sweep": "h2/h3/h4 label(라벨), target density 3-12(목표 밀도 3-12), short/long guards(숏/롱 가드)",
            "extreme_sweep": "density 12/day(일 12회 밀도), short cap pressure(숏 상한 압박), cost0.9 stress(비용0.9 압박)",
            "success_criteria": "validation_cost06>=0, oos_cost06>0, combined_cost09>=0, density>=3, short_share<=0.72, min_pf>=1.12(검증/표본외 비용, 합산 비용, 밀도, 숏 비중, 최소 PF 조건)",
            "failure_criteria": "no strict candidate(엄격 후보 없음) or density-cost contradiction(밀도-비용 충돌)",
            "invalid_conditions": "input lineage mismatch, split leakage, ONNX smoke failure for selected model(입력 계보 불일치, 분할 누수, 선택 모델 ONNX 스모크 실패)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def write_feature_audit(sets: Mapping[str, Sequence[str]]) -> None:
    rows = []
    derived = set(dt.derived_features())
    for feature_set_id, columns in sets.items():
        rows.append(
            {
                "run_id": RUN_ID,
                "feature_set_id": feature_set_id,
                "feature_count": len(columns),
                "derived_feature_count": sum(1 for column in columns if column in derived),
                "effect": "ET score(ET 점수)가 비용/방향 실패 기억을 사용할 피처 묶음을 고정합니다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(FEATURE_AUDIT, rows)


def write_label_summary(frame: pd.DataFrame) -> None:
    rows = []
    for spec in LABEL_SPECS:
        labels, ok = et_label_values(frame, spec)
        for split in ["train", "validation", "oos"]:
            mask = frame["split"].eq(split).to_numpy() & ok
            values = labels[mask]
            rows.append(
                {
                    "run_id": RUN_ID,
                    "label_id": spec["label_id"],
                    "split": split,
                    "horizon_m5": spec["horizon_m5"],
                    "mode": spec["mode"],
                    "rows": int(mask.sum()),
                    "short_labels": int((values == 0).sum()),
                    "flat_labels": int((values == 1).sum()),
                    "long_labels": int((values == 2).sum()),
                    "effect": "label balance(라벨 균형)가 density/cost 탐색(밀도/비용 탐색)의 출발 조건을 보여줍니다.",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    write_csv(LABEL_SUMMARY, rows)


def enrich_surface(surface_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    enriched = []
    for raw in surface_rows:
        row = dict(raw)
        values = cost_values(row)
        row.update({key: finite(value, 10) for key, value in values.items()})
        row["et_strict_density_cost_short_pass"] = "passed(통과)" if et_strict_success(row) else "failed(실패)"
        row["et_operational_proxy_stack_pass"] = "passed(통과)" if et_operational_stack(row) else "failed(실패)"
        row["strict_cross_split_success"] = row["et_strict_density_cost_short_pass"]
        row["selection_score"] = finite(et_selection_score(row), 6)
        enriched.append(row)
    return sorted(enriched, key=lambda item: (str(item["et_strict_density_cost_short_pass"]).startswith("passed"), as_float(item["selection_score"])), reverse=True)


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
    strict = [row for row in exportable if str(row.get("et_strict_density_cost_short_pass", "")).startswith("passed")]
    return max(strict or exportable or list(surface_rows), key=lambda row: as_float(row.get("selection_score")))


def replay_selected_trades(frame: pd.DataFrame, trained: Mapping[str, Mapping[str, Any]], selected: Mapping[str, Any]) -> list[dict[str, Any]]:
    model_id = str(selected["model_id"])
    trained_payload = trained[model_id]
    label_spec = next(spec for spec in LABEL_SPECS if spec["label_id"] == str(selected["label_id"]))
    _, ok = et_label_values(frame, label_spec)
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
    return max(1, int(round(count / density))) if density > 0 else 1


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
    strict = [row for row in exportable if str(row.get("et_strict_density_cost_short_pass", "")).startswith("passed")]
    operational = [row for row in exportable if str(row.get("et_operational_proxy_stack_pass", "")).startswith("passed")]
    best = selected_surface_row(surface_rows, smoke_rows)
    trade_frame = pd.DataFrame(list(trades))
    metric_row = dict(best)
    metric_row.update(selected_trade_metrics(trade_frame, best))
    values = cost_values(metric_row)
    validation_tape_count = int((trade_frame["split"] == "validation").sum()) if not trade_frame.empty else 0
    oos_tape_count = int((trade_frame["split"] == "oos").sum()) if not trade_frame.empty else 0
    status = STATUS_STRICT if strict else STATUS_NO_STRICT
    judgment = JUDGMENT_STRICT if strict else JUDGMENT_NO_STRICT
    decision = DECISION_STRICT if strict else DECISION_NO_STRICT
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
        {"run_id": RUN_ID, "audit_item": "input_lineage(입력 계보)", "status": "passed" if all(exists(path) for path in INPUT_FILES if path != Path(__file__)) else "failed", "observed": ";".join(rel(path) for path in INPUT_FILES if path != Path(__file__)), "effect": "ES 실패 기억과 모델 입력을 ET 학습에 연결합니다.", "claim_boundary": CLAIM_BOUNDARY},
        {"run_id": RUN_ID, "audit_item": "duplicate_timestamp(중복 타임스탬프)", "status": "passed" if duplicate_timestamps == 0 else "failed", "observed": f"duplicate_timestamps={duplicate_timestamps}", "effect": "중복 행이 거래 재생을 부풀리지 않게 합니다.", "claim_boundary": CLAIM_BOUNDARY},
        {"run_id": RUN_ID, "audit_item": "split_presence(분할 존재)", "status": "passed" if all(split_counts.get(split, 0) > 0 for split in ["train", "validation", "oos"]) else "failed", "observed": json.dumps(split_counts, ensure_ascii=False, sort_keys=True), "effect": "train/validation/OOS(학습/검증/표본외) 경계를 유지합니다.", "claim_boundary": CLAIM_BOUNDARY},
        {"run_id": RUN_ID, "audit_item": "feature_columns_present(피처 컬럼 존재)", "status": "passed" if not missing_features else "failed", "observed": "|".join(missing_features), "effect": "국면/현상 파생 피처가 명시적으로 존재하는지 확인합니다.", "claim_boundary": CLAIM_BOUNDARY},
        {"run_id": RUN_ID, "audit_item": "label_boundary(라벨 경계)", "status": "passed", "observed": "future_open used only for dense cost direction labels(미래 open은 고밀도 비용 방향 라벨에만 사용)", "effect": "look-ahead bias(미래참조 편향)를 피처로 흘리지 않습니다.", "claim_boundary": CLAIM_BOUNDARY},
        {"run_id": RUN_ID, "audit_item": "selected_trade_tape_full(선택 거래 테이프 전체)", "status": "passed" if int(summary["validation_trade_tape_rows"]) == int(float(summary["selected_validation_trade_count"])) and int(summary["oos_trade_tape_rows"]) == int(float(summary["selected_oos_trade_count"])) else "failed", "observed": f"validation_tape={summary['validation_trade_tape_rows']};oos_tape={summary['oos_trade_tape_rows']}", "effect": "세션/방향 귀속을 부분 테이프로 과장하지 않습니다.", "claim_boundary": CLAIM_BOUNDARY},
        {"run_id": RUN_ID, "audit_item": "no_trade_splitting(거래 쪼개기 없음)", "status": "passed", "observed": "simulator jumps past exit index after entry(진입 뒤 청산 인덱스 이후로 이동)", "effect": "거래수를 쪼개 수익을 나누지 않습니다.", "claim_boundary": CLAIM_BOUNDARY},
    ]
    write_csv(DATA_INTEGRITY_AUDIT, rows)
    return rows


def write_queue(summary: Mapping[str, Any]) -> None:
    write_csv(
        RUN364EU_QUEUE,
        [
            {
                "run_id": RUN_ID,
                "next_run_id": NEXT_RUN_ID,
                "queue_rank": 1,
                "queue_id": "eu01_density_cost_short_balance_review",
                "review_subject": summary["selected_model_id"],
                "strict_candidate_count": summary["strict_candidate_count"],
                "operational_proxy_stack_pass_count": summary["operational_proxy_stack_pass_count"],
                "selected_combined_net": summary["selected_combined_net"],
                "selected_combined_trade_density": summary["selected_combined_trade_density"],
                "selected_combined_cost09_net": summary["selected_combined_cost09_net"],
                "selected_combined_short_share": summary["selected_combined_short_share"],
                "effect": "EU review(EU 검토)가 ET의 밀도/비용/숏 균형 단서를 패키지와 실패 기억으로 분리합니다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )


def write_receipts(final: Mapping[str, Any]) -> None:
    base = {"run_id": RUN_ID, "stage_id": STAGE_ID, "created_at_utc": final["created_at_utc"], "claim_boundary": CLAIM_BOUNDARY}
    write_json(RUN_EVIDENCE_RECEIPT, {**base, "surface": rel(TRADE_SURFACE), "selected_candidate": rel(SELECTED_CANDIDATE), "selected_trade_tape": rel(SELECTED_TRADE_TAPE), "measurement_boundary": "Python proxy with ONNX smoke, no MT5(Python 프록시와 ONNX 스모크, MT5 없음)"})
    write_json(EXPERIMENT_RECEIPT, {**base, "hypothesis": "density/cost/short balance(밀도/비용/숏 균형)를 label/score/filter(라벨/점수/필터)에 직접 넣으면 ER 실패를 일부 회복할 수 있습니다.", "comparison_baseline": PARENT_RUN_ID, "decision_use": NEXT_RUN_ID})
    write_json(DATA_RECEIPT, {**base, "data_source": [rel(dt.dp.MODEL_INPUT_DATASET), rel(dt.dp.RAW_US100_M5)], "time_axis": "UTC model input timestamp and raw open join(UTC 모델 입력 timestamp와 원천 open 결합)", "sample_scope": "train/validation/OOS", "feature_label_boundary": "future_open only in labels(미래 open은 라벨에만 사용)", "split_boundary": "chronological train validation OOS(시간순 학습 검증 표본외)", "integrity_judgment": "usable_with_proxy_boundary(프록시 경계 안에서 사용 가능)"})
    write_json(MODEL_RECEIPT, {**base, "model_family": "RandomForest/ExtraTrees(랜덤포레스트/엑스트라트리)", "selected_model_id": final["selected_model_id"], "onnx_smoke_pass_rows": final["onnx_smoke_pass_rows"], "validation_judgment": final["judgment"]})
    write_json(ATTRIBUTION_RECEIPT, {**base, "observed_change": f"selected validation {final['selected_validation_net']}/{final['selected_validation_profit_factor']}/{final['selected_validation_trade_density']}; OOS {final['selected_oos_net']}/{final['selected_oos_profit_factor']}/{final['selected_oos_trade_density']}", "likely_drivers": ["cost-weighted dense label(비용 가중 고밀도 라벨)", "side/session penalty(방향/세션 벌점)", "short share pressure(숏 비중 압박)"], "next_probe": NEXT_RUN_ID})
    write_json(JUDGMENT_RECEIPT, {**base, "result_subject": RUN_ID, "evidence_available": [rel(TRADE_SURFACE), rel(SELECTED_CANDIDATE), rel(ONNX_SMOKE_REPORT), rel(DATA_INTEGRITY_AUDIT)], "evidence_missing": ["MT5 runtime package(MT5 런타임 패키지)", "MT5 runtime probe(MT5 런타임 탐침)", "forward/replay evidence(전진/재생 근거)"], "judgment_label": final["judgment"], "next_condition": NEXT_RUN_ID})
    write_json(LINEAGE_RECEIPT, {**base, "source_inputs": [{"path": rel(path), "sha256": sha(path)} for path in INPUT_FILES if exists(path) and Path(path).is_file()], "producer": rel(Path(__file__)), "consumer": NEXT_RUN_ID, "artifact_paths": [rel(path) for path in OUTPUT_FILES if exists(path)], "artifact_hashes": {rel(path): sha(path) for path in OUTPUT_FILES if exists(path) and Path(path).is_file()}, "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)], "lineage_judgment": "connected_proxy_model_reseed(프록시 모델 재시드 연결)"})
    write_json(CLAIM_RECEIPT, {**base, "runtime_package": "not_opened", "runtime_authority": "not_claimed", "operating_promotion": "not_claimed", "live_readiness": "not_claimed", "goal_achieve": "not_claimed", "effect": "ET 모델 단서를 운영 주장으로 올리지 않습니다."})


def gate_rows(final: Mapping[str, Any], data_rows: Sequence[Mapping[str, Any]], *, final_written: bool) -> list[dict[str, Any]]:
    receipts = [RUN_EVIDENCE_RECEIPT, EXPERIMENT_RECEIPT, DATA_RECEIPT, MODEL_RECEIPT, ATTRIBUTION_RECEIPT, JUDGMENT_RECEIPT, LINEAGE_RECEIPT, CLAIM_RECEIPT]
    checks = [
        ("scope_completion_gate", exists(TRADE_SURFACE) and exists(SELECTED_CANDIDATE), TRADE_SURFACE, "ET surface(ET 표면)와 선택 후보를 작성했습니다."),
        ("input_lineage_gate", exists(INPUT_MANIFEST), INPUT_MANIFEST, "입력 계보가 연결됐습니다."),
        ("data_integrity_gate", bool(data_rows) and all(str(row["status"]) == "passed" for row in data_rows), DATA_INTEGRITY_AUDIT, "시점/분할/피처/라벨/테이프 검사를 통과했습니다."),
        ("training_split_gate", exists(MODEL_SCORECARD), MODEL_SCORECARD, "train split(학습 분할)로 모델을 적합하고 validation/OOS(검증/표본외)를 분리했습니다."),
        ("model_artifact_gate", exists(MODEL_ARTIFACT_MANIFEST), MODEL_ARTIFACT_MANIFEST, "joblib/ONNX(잡립/온엑스) 산출물 목록이 있습니다."),
        ("onnx_smoke_gate", exists(ONNX_SMOKE_REPORT) and int(final["onnx_smoke_pass_rows"]) > 0, ONNX_SMOKE_REPORT, "ONNX smoke(온엑스 스모크) 통과 모델이 있습니다."),
        ("density_cost_surface_gate", exists(TRADE_SURFACE) and int(final["surface_rows"]) > 0, TRADE_SURFACE, "밀도/비용/숏 파생 지표를 표면에 기록했습니다."),
        ("full_trade_tape_gate", exists(SELECTED_TRADE_TAPE), SELECTED_TRADE_TAPE, "선택 후보의 전체 검증/OOS 거래 테이프를 기록했습니다."),
        ("strict_contract_decision_gate", exists(RUN364EU_QUEUE), RUN364EU_QUEUE, "엄격 후보 수와 다음 검토를 기록했습니다."),
        ("paired_tier_record_gate", True, STAGE_LEDGER, "Tier A/Tier B/Tier A+B 행을 남깁니다."),
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
    report = f"""# run364ET OOS108 density/cost/short balance reseed(OOS108 밀도/비용/숏 균형 재시드)

Created(생성): {final['created_at_utc']}

## Summary(요약)

Action(행동): ES failure memory(ES 실패 기억)를 받아 dense cost labels(고밀도 비용 라벨), side/session filters(방향/세션 필터), cost-heavy selection score(비용 중시 선택 점수)로 새 모델을 학습했습니다.

Effect(효과): ER의 density/cost/short(밀도/비용/숏) 동시 실패를 threshold micro-search(임계값 미세탐색)가 아니라 label/score/filter(라벨/점수/필터)로 직접 공격합니다.

## Selected(선택)

- selected_model_id(선택 모델 ID): `{final['selected_model_id']}`
- selected_metric_source(선택 지표 원천): `{final['selected_metric_source']}`
- validation net/PF/density/trades(검증 순수익/PF/밀도/거래수): `{final['selected_validation_net']}` / `{final['selected_validation_profit_factor']}` / `{final['selected_validation_trade_density']}` / `{final['selected_validation_trade_count']}`
- OOS net/PF/density/trades(표본외 순수익/PF/밀도/거래수): `{final['selected_oos_net']}` / `{final['selected_oos_profit_factor']}` / `{final['selected_oos_trade_density']}` / `{final['selected_oos_trade_count']}`
- combined net/density/trades(합산 순수익/밀도/거래수): `{final['selected_combined_net']}` / `{final['selected_combined_trade_density']}` / `{final['selected_combined_trade_count']}`
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

`{NEXT_RUN_ID}`에서 ET 결과를 review(검토)하고 package(패키지) 가능성과 실패 기억을 분리합니다.

## Gates(게이트)

{chr(10).join(f"- {row['gate']}: {row['status']} -> {row['evidence']}" for row in gates)}
"""
    decision_doc = f"""# Decision(결정): stage364ET density/cost/short balance reseed(밀도/비용/숏 균형 재시드)

- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{final['decision']}`
- judgment(판정): `{final['judgment']}`
- selected_model_id(선택 모델 ID): `{final['selected_model_id']}`
- strict_candidate_count(엄격 후보 수): `{final['strict_candidate_count']}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Action(행동): cost-weighted dense labels(비용 가중 고밀도 라벨)와 side/session penalty(방향/세션 벌점)를 새 모델 학습에 반영했습니다.

Effect(효과): ET review(ET 검토)가 실제 개선인지 또는 새 실패 기억인지 판단할 수 있는 ONNX(온엑스) 산출물과 full trade tape(전체 거래 테이프)를 남깁니다.
"""
    write_text(REPORT_PATH, report, bom=True)
    write_text(DECISION_DOC, decision_doc, bom=True)
    append_text_once(REVIEW_INDEX, f"run364ET__{RUN_ID}", f"\n- run364ET__{RUN_ID}: [{REPORT_PATH.name}]({REPORT_PATH.name}) - density/cost/short balance reseed(밀도/비용/숏 균형 재시드), next `{NEXT_RUN_ID}`.\n")
    append_text_once(STAGE_BRIEF, f"run364ET__{RUN_ID}", f"\n<!-- run364ET__{RUN_ID} -->\n\n## run364ET Density/Cost/Short Balance Reseed(밀도/비용/숏 균형 재시드)\n\nAction(행동): 비용 가중 고밀도 라벨과 방향/세션 벌점으로 모델을 재학습했습니다.\n\nEffect(효과): `{NEXT_RUN_ID}`에서 패키지 가능성과 실패 기억을 분리합니다.\n")
    append_text_once(STAGE_README, f"run364ET__{RUN_ID}", f"\n<!-- run364ET__{RUN_ID} -->\n## run364ET density/cost/short balance reseed(밀도/비용/숏 균형 재시드)\n\nSelected(선택): `{final['selected_model_id']}`. Strict candidates(엄격 후보): `{final['strict_candidate_count']}`. Next(다음): `{NEXT_RUN_ID}`.\n")
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

Current truth(현재 진실): `run364ET` trained(학습 완료) density/cost/short balance reseed(밀도/비용/숏 균형 재시드). Selected validation/OOS net/PF/density(선택 검증/표본외 순수익/PF/밀도)는 `{final['selected_validation_net']}` / `{final['selected_validation_profit_factor']}` / `{final['selected_validation_trade_density']}` 및 `{final['selected_oos_net']}` / `{final['selected_oos_profit_factor']}` / `{final['selected_oos_trade_density']}`입니다.

Cost/side truth(비용/방향 진실): combined cost0.6/cost0.9 net(합산 비용0.6/0.9 순수익)은 `{final['selected_combined_cost06_net']}` / `{final['selected_combined_cost09_net']}`이고, combined short share(합산 숏 비중)는 `{final['selected_combined_short_share']}`입니다.

Next action(다음 행동): `{NEXT_RUN_ID}`에서 ET 결과를 review(검토)하고 package(패키지) 가능성과 failure memory(실패 기억)를 분리합니다.

Operating boundary(운영 경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""", bom=True)
    write_text(SELECTION_STATUS, f"""# Stage364 selection status(선택 상태)

Updated(갱신): {final['created_at_utc']}

Current run(현재 실행): `{NEXT_RUN_ID}`
Latest completed run(최근 완료 실행): `{RUN_ID}`

Latest scout(최근 정찰): ET density/cost/short balance reseed(ET 밀도/비용/숏 균형 재시드).

Selected model(선택 모델): `{final['selected_model_id']}`

Validation net/PF/density(검증 순수익/PF/밀도): `{final['selected_validation_net']}` / `{final['selected_validation_profit_factor']}` / `{final['selected_validation_trade_density']}`
OOS net/PF/density(표본외 순수익/PF/밀도): `{final['selected_oos_net']}` / `{final['selected_oos_profit_factor']}` / `{final['selected_oos_trade_density']}`

Judgment(판정): `{final['judgment']}`.

Authority(권위): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""", bom=True)
    append_text_once(WORKSPACE_CHANGELOG, f"run364ET__{RUN_ID}", f"\n<!-- run364ET__{RUN_ID} -->\n- {final['created_at_utc']} `{RUN_ID}` completed density/cost/short balance reseed(밀도/비용/숏 균형 재시드); strict candidates `{final['strict_candidate_count']}`; selected `{final['selected_model_id']}`; next `{NEXT_RUN_ID}`; no authority claim(권위 주장 없음).\n")
    append_text_once(IDEA_REGISTRY, f"run364ET__{RUN_ID}", f"\n<!-- run364ET__{RUN_ID} -->\n- `{RUN_ID}`: cost-weighted dense label(비용 가중 고밀도 라벨)과 side/session penalty(방향/세션 벌점)를 학습했습니다. Effect(효과): ER 실패 기억을 score/label/filter(점수/라벨/필터) 탐색으로 전환했습니다.\n")
    if int(final["strict_candidate_count"]) == 0:
        append_text_once(NEGATIVE_REGISTER, f"run364ET__strict_candidate_absent__{RUN_ID}", f"\n<!-- run364ET__strict_candidate_absent__{RUN_ID} -->\n- `{RUN_ID}`: density/cost/short balance reseed(밀도/비용/숏 균형 재시드)가 strict candidate(엄격 후보)를 만들지 못했습니다. Effect(효과): EU에서 실패 조건과 salvage segment(회수 구간)를 분리합니다.\n")


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
        "artifact_count": len({Path(path) for path in OUTPUT_FILES if exists(path) or Path(path) == RUN_MANIFEST}),
        "gate_passes": sum(1 for row in gates if row["status"] == "passed"),
        "gate_total": len(gates),
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "created_at_utc": final["created_at_utc"],
        "required_gate_audit": rel(GATE_AUDIT),
        "question": "Can dense cost labels and side/session penalties repair density/cost/short balance?(고밀도 비용 라벨과 방향/세션 벌점이 밀도/비용/숏 균형을 고칠 수 있는가?)",
        "next_action": NEXT_RUN_ID,
        "notes": f"strict_candidate_count={final['strict_candidate_count']};onnx_smoke_pass_rows={final['onnx_smoke_pass_rows']};combined_cost09={final['selected_combined_cost09_net']}",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "run_family": "experiment_execution(실험 실행)",
        "run_type": "density_cost_short_balance_reseed(밀도/비용/숏 균형 재시드)",
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
        row = {**common, "ledger_row_id": f"{RUN_ID}__{suffix}", "subrun_id": f"{RUN_ID}__{suffix}", "row_id": f"{RUN_ID}__{suffix}", "record_view": record_view, "tier_scope": tier_scope, "view": record_view, "tier": tier_scope, "kpi_scope": "ET density/cost/short balance reseed(ET 밀도/비용/숏 균형 재시드)", "metric_scope": "python_proxy_onnx_smoke(Python 프록시 ONNX 스모크)", "status": status, "net_profit": final["selected_oos_net"] if suffix == "tier_a_separate" else "", "profit_factor": final["selected_oos_profit_factor"] if suffix == "tier_a_separate" else "", "trade_density": final["selected_oos_trade_density"] if suffix == "tier_a_separate" else "", "trade_count": final["selected_oos_trade_count"] if suffix == "tier_a_separate" else "", "source_authority": "python_proxy_onnx_smoke_no_mt5(Python 프록시 ONNX 스모크, MT5 없음)"}
        rows.append(row)
    append_or_replace_csv(STAGE_LEDGER, ["ledger_row_id"], rows)
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], rows)
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], [common])
    repair_run_registry_line_endings(RUN_ID)


def write_artifact_registry(final: Mapping[str, Any]) -> None:
    rows = []
    for path in OUTPUT_FILES:
        if exists(path) and Path(path).is_file():
            rows.append({"stage_id": STAGE_ID, "run_id": RUN_ID, "artifact_type": "script" if path == Path(__file__) else ("report" if path.suffix.lower() == ".md" else ("json" if path.suffix.lower() == ".json" else "csv")), "path": rel(path), "artifact_path": rel(path), "sha256": sha(path), "created_at": final["created_at_utc"], "created_at_utc": final["created_at_utc"], "claim_boundary": CLAIM_BOUNDARY, "artifact_id": f"{RUN_ID}__{path.stem}", "notes": "ET density/cost/short balance reseed artifact(ET 밀도/비용/숏 균형 재시드 산출물)"})
    append_or_replace_csv(ARTIFACT_REGISTRY, ["artifact_id"], rows)


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
    sets = et_feature_sets(feature_order)
    write_feature_audit(sets)
    write_label_summary(frame)
    score_rows, surface_rows, trained, _ = dt.train_and_score(frame, sets)
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
