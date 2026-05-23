from __future__ import annotations

import hashlib
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import (
    ALPHA_LEDGER_COLUMNS,
    RUN_REGISTRY_COLUMNS,
    io_path,
    json_ready,
    path_exists,
    read_csv_rows,
    sha256_file_lf_normalized,
    upsert_csv_rows,
    write_csv_rows,
)


STAGE275_ID = "275_onnx_candidate_campaign__fresh_candidate_construction_after_filter_like_rebuild_failure"
STAGE276_ID = "276_onnx_candidate_campaign__aggressive_fresh_surface_probe"
RUN_ID = "run276A_design_aggressive_fresh_surface_probe_packet_v1"
SOURCE_RUN_ID = "run275F_close_stage275_open_stage276_aggressive_fresh_surface_probe_v1"
SOURCE_SCREEN_RUN_ID = "run275E_screen_fresh_candidate_score_surfaces_v1"
STATUS = "completed_aggressive_fresh_surface_probe_packet_design_no_candidate_selection"
JUDGMENT = "aggressive_probe_packet_ready_no_candidate_selection"
NEXT_ACTION = "run276B_materialize_aggressive_fresh_surface_probe_payloads"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_"
    "no_deployment_no_onnx_until_candidate_package_gate"
)

STAGE275 = ROOT / "stages" / STAGE275_ID
STAGE276 = ROOT / "stages" / STAGE276_ID
RUN_DIR = STAGE276 / "02_runs" / "run276A"
REVIEWS = STAGE276 / "03_reviews"
SELECTED = STAGE276 / "04_selected"
RUN275F = STAGE275 / "02_runs" / "run275F"

SOURCE_QUEUE = STAGE276 / "01_inputs" / "stage276_probe_queue.csv"
SOURCE_SUPPORT = STAGE276 / "01_inputs" / "support_control.csv"
SOURCE_FAILURE = STAGE276 / "01_inputs" / "stage275_failure_memory.csv"
SOURCE_INPUT_REFS = STAGE276 / "01_inputs" / "input_refs.md"
SOURCE_STAGE_BRIEF = STAGE276 / "00_spec" / "stage_brief.md"
SOURCE_CLOSEOUT = STAGE275 / "03_reviews" / "stage275_closeout_stage276_handoff.md"
SOURCE_RUN275F_MANIFEST = RUN275F / "run_manifest.json"
SOURCE_RUN275F_LINEAGE = RUN275F / "lineage.json"

BRANCH_PLAN = RUN_DIR / "branch_plan.csv"
BRANCH_SUPPLY = RUN_DIR / "branch_supply_metrics.csv"
MT5_QUEUE = RUN_DIR / "mt5_probe_design_queue.csv"
THRESHOLD_RECEIPT = RUN_DIR / "thresholds.json"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment.json"
DATA_INTEGRITY_RECEIPT = RUN_DIR / "data.json"
MODEL_VALIDATION_RECEIPT = RUN_DIR / "model.json"
RESULT_JUDGMENT = RUN_DIR / "judgment.csv"
GATE_AUDIT = RUN_DIR / "gates.csv"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"
LINEAGE_RECEIPT = RUN_DIR / "lineage.json"
RUN_REPORT = REVIEWS / "run276A_report.md"

SELECTION_STATUS = SELECTED / "selection_status.md"
REVIEW_INDEX = REVIEWS / "review_index.md"
STAGE_LEDGER = REVIEWS / "stage_run_ledger.csv"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
PRODUCER_PATH = Path("stage_pipelines/stage276/design_aggressive_fresh_surface_probe_packet.py")

STAGE_LEDGER_COLUMNS = (
    "row_id",
    "stage_id",
    "run_id",
    "view",
    "tier_scope",
    "scoreboard",
    "status",
    "judgment",
    "evidence_boundary",
    "report_path",
    "notes",
)
ARTIFACT_COLUMNS = (
    "artifact_id",
    "artifact_type",
    "path",
    "sha256",
    "stage_id",
    "run_id",
    "created_at_utc",
    "notes",
)
BRANCH_COLUMNS = (
    "variant_id",
    "package_id",
    "variant_role",
    "fresh_thesis",
    "comparison_baseline",
    "decision_rule",
    "thresholds_json",
    "pressure_axis",
    "upside_condition",
    "failure_mode",
    "discard_condition",
    "invalid_conditions",
    "stop_conditions",
    "evidence_plan",
    "duplicate_of",
    "queue_recommendation",
    "claim_boundary",
)
SUPPLY_COLUMNS = (
    "variant_id",
    "package_id",
    "tier_view",
    "split",
    "rows",
    "decision_count",
    "decision_rate",
    "long_share",
    "short_share",
    "new_active_rate",
    "direction_changed_rate",
    "mean_score",
    "mean_risk_pct",
    "claim_boundary",
)
MT5_QUEUE_COLUMNS = (
    "queue_id",
    "queue_priority",
    "variant_id",
    "package_id",
    "source_score_table",
    "source_handoff_json",
    "required_support_control",
    "materialization_status",
    "mt5_probe_question",
    "success_condition",
    "discard_condition",
    "required_evidence",
    "claim_boundary",
)
RESULT_COLUMNS = (
    "result_subject",
    "evidence_available",
    "evidence_missing",
    "judgment_label",
    "judgment_class",
    "claim_boundary",
    "next_condition",
    "user_explanation_hook",
)
GATE_COLUMNS = ("gate_name", "status", "evidence_path", "effect")


def rel(path: Path | str) -> str:
    item = Path(str(path))
    try:
        return item.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return item.as_posix()


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def digest_mask(mask: pd.Series) -> str:
    raw = mask.astype("int8").to_numpy().tobytes()
    return hashlib.sha256(raw).hexdigest()


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(
        json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> None:
    write_csv_rows(path, columns, rows)


def must_exist(paths: Sequence[Path]) -> None:
    missing = [rel(path) for path in paths if not path_exists(path)]
    if missing:
        raise FileNotFoundError("Missing required source artifacts: " + ", ".join(missing))


def repo_path(text: str) -> Path:
    return ROOT / text


def load_table(path_text: str) -> pd.DataFrame:
    columns = ["timestamp", "split", "tier_view", "entry_signal", "candidate_decision_score", "model_risk_pct"]
    return pd.read_parquet(io_path(repo_path(path_text)), columns=columns)


def round_float(value: float, digits: int = 8) -> float:
    return round(float(value), digits) if np.isfinite(value) else 0.0


def train_thresholds(frame: pd.DataFrame) -> dict[str, float]:
    train = frame[(frame["tier_view"].astype(str).eq("Tier A separate")) & (frame["split"].astype(str).eq("train"))]
    if train.empty:
        raise ValueError("Tier A train rows(티어 A 학습 행)가 필요하다.")
    score = pd.to_numeric(train["candidate_decision_score"], errors="coerce")
    risk = pd.to_numeric(train["model_risk_pct"], errors="coerce")
    return {
        "score_q60": float(score.quantile(0.60)),
        "score_q70": float(score.quantile(0.70)),
        "score_q80": float(score.quantile(0.80)),
        "risk_q60": float(risk.quantile(0.60)),
        "risk_q70": float(risk.quantile(0.70)),
    }


def variant_templates(package_id: str, fresh_thesis: str, thresholds: Mapping[str, float]) -> list[dict[str, Any]]:
    short = package_id.split("_")[0]
    return [
        {
            "variant_id": f"run276A_{short}_q01_base_surface",
            "variant_role": "reference_aggressive_seed(기준 공격형 씨앗)",
            "fresh_thesis": fresh_thesis,
            "decision_rule": "entry_signal != flat",
            "thresholds_json": json.dumps({}, sort_keys=True),
            "pressure_axis": "base_supply(기준 공급)",
            "upside_condition": "base surface(기준 표면)가 MT5 probe(MT5 탐침)에서 곡선 손상 없이 양의 거래 품질을 만든다.",
            "failure_mode": "base supply(기준 공급)가 curve damage(곡선 손상)나 trade quality collapse(거래 품질 붕괴)를 만든다.",
            "discard_condition": "PF/DD/recovery/expectancy(수익 팩터/손실폭/회복/기대값)가 함께 무너지면 폐기한다.",
        },
        {
            "variant_id": f"run276A_{short}_q02_score_q70_focus",
            "variant_role": "focused_score_pressure(점수 집중 압박)",
            "fresh_thesis": fresh_thesis,
            "decision_rule": "entry_signal != flat and candidate_decision_score >= train_tier_a_score_q70",
            "thresholds_json": json.dumps({"score_min": thresholds["score_q70"]}, sort_keys=True),
            "pressure_axis": "score_focus(점수 집중)",
            "upside_condition": "high-score subset(고점수 부분집합)이 더 깨끗한 trade quality(거래 품질)를 만든다.",
            "failure_mode": "subset(부분집합)이 너무 좁거나 같은 손실 모양을 반복한다.",
            "discard_condition": "validation/oos(검증/표본외) decision count(판단 수)가 부족하거나 curve(곡선)가 악화되면 폐기한다.",
        },
        {
            "variant_id": f"run276A_{short}_q03_q04_distance_focus",
            "variant_role": "q04_distance_pressure(q04 거리 압박)",
            "fresh_thesis": fresh_thesis,
            "decision_rule": "entry_signal != flat and entry_signal != q04_guard_entry_signal",
            "thresholds_json": json.dumps({}, sort_keys=True),
            "pressure_axis": "q04_distance(q04 거리)",
            "upside_condition": "q04 guard(q04 방어 기준)와 다른 신호가 보상 비대칭을 만든다.",
            "failure_mode": "fresh signal(새 신호)이 실제 거래에서는 q04 실패를 다른 모양으로 반복한다.",
            "discard_condition": "new/direction signal(새/방향 신호)이 MT5(메타트레이더5)에서 음의 거래 품질이면 폐기한다.",
        },
        {
            "variant_id": f"run276A_{short}_q04_risk_q70_focus",
            "variant_role": "risk_budget_pressure(위험 예산 압박)",
            "fresh_thesis": fresh_thesis,
            "decision_rule": "entry_signal != flat and model_risk_pct >= train_tier_a_risk_q70",
            "thresholds_json": json.dumps({"risk_min": thresholds["risk_q70"]}, sort_keys=True),
            "pressure_axis": "risk_budget_focus(위험 예산 집중)",
            "upside_condition": "higher risk budget(높은 위험 예산) 구간이 더 나은 upside(상방)를 만든다.",
            "failure_mode": "risk budget(위험 예산)이 손실폭만 키운다.",
            "discard_condition": "DD/drawdown(손실폭)이 커지고 recovery(회복)가 약하면 폐기한다.",
        },
    ]


def decision_mask(frame: pd.DataFrame, control: pd.DataFrame, template: Mapping[str, Any]) -> pd.Series:
    active = frame["entry_signal"].astype(str).ne("flat")
    variant_id = str(template["variant_id"])
    thresholds = json.loads(str(template["thresholds_json"]))
    if variant_id.endswith("_q01_base_surface"):
        return active
    if variant_id.endswith("_q02_score_q70_focus"):
        return active & pd.to_numeric(frame["candidate_decision_score"], errors="coerce").ge(float(thresholds["score_min"]))
    if variant_id.endswith("_q03_q04_distance_focus"):
        return active & frame["entry_signal"].astype(str).ne(control["entry_signal"].astype(str))
    if variant_id.endswith("_q04_risk_q70_focus"):
        return active & pd.to_numeric(frame["model_risk_pct"], errors="coerce").ge(float(thresholds["risk_min"]))
    raise ValueError(f"Unknown variant_id: {variant_id}")


def summarize_variant(package_id: str, variant_id: str, frame: pd.DataFrame, control: pd.DataFrame, mask: pd.Series) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for tier_view in ["Tier A separate", "Tier B separate", "Tier A+B combined"]:
        tier_frame = frame if tier_view == "Tier A+B combined" else frame[frame["tier_view"].astype(str).eq(tier_view)]
        tier_mask = mask.loc[tier_frame.index]
        control_active = control.loc[tier_frame.index, "entry_signal"].astype(str).ne("flat")
        direction_changed = tier_mask & control_active & tier_frame["entry_signal"].astype(str).ne(control.loc[tier_frame.index, "entry_signal"].astype(str))
        new_active = tier_mask & ~control_active
        for split in ["train", "validation", "oos"]:
            part = tier_frame[tier_frame["split"].astype(str).eq(split)]
            part_mask = tier_mask.loc[part.index]
            rows.append(
                {
                    "variant_id": variant_id,
                    "package_id": package_id,
                    "tier_view": tier_view,
                    "split": split,
                    "rows": int(len(part)),
                    "decision_count": int(part_mask.sum()),
                    "decision_rate": round_float(float(part_mask.mean()) if len(part_mask) else 0.0),
                    "long_share": round_float(float(part.loc[part_mask, "entry_signal"].astype(str).eq("long").mean()) if int(part_mask.sum()) else 0.0),
                    "short_share": round_float(float(part.loc[part_mask, "entry_signal"].astype(str).eq("short").mean()) if int(part_mask.sum()) else 0.0),
                    "new_active_rate": round_float(float(new_active.loc[part.index].mean()) if len(part) else 0.0),
                    "direction_changed_rate": round_float(float(direction_changed.loc[part.index].mean()) if len(part) else 0.0),
                    "mean_score": round_float(float(pd.to_numeric(part.loc[part_mask, "candidate_decision_score"], errors="coerce").mean()) if int(part_mask.sum()) else 0.0),
                    "mean_risk_pct": round_float(float(pd.to_numeric(part.loc[part_mask, "model_risk_pct"], errors="coerce").mean()) if int(part_mask.sum()) else 0.0),
                    "claim_boundary": BOUNDARY,
                }
            )
    return rows


def combined_metric(rows: Sequence[Mapping[str, Any]], variant_id: str, split: str, field: str) -> float:
    for row in rows:
        if row["variant_id"] == variant_id and row["tier_view"] == "Tier A+B combined" and row["split"] == split:
            return float(row[field])
    return 0.0


def queue_recommendation(variant_id: str, supply_rows: Sequence[Mapping[str, Any]], duplicate_of: str) -> str:
    if duplicate_of:
        return "hold_duplicate(중복 보류)"
    validation_count = combined_metric(supply_rows, variant_id, "validation", "decision_count")
    oos_count = combined_metric(supply_rows, variant_id, "oos", "decision_count")
    validation_rate = combined_metric(supply_rows, variant_id, "validation", "decision_rate")
    oos_rate = combined_metric(supply_rows, variant_id, "oos", "decision_rate")
    if validation_count >= 75 and oos_count >= 75 and validation_rate <= 0.50 and oos_rate <= 0.50:
        return "queue_for_run276B_payload_materialization(run276B 페이로드 물질화 대기열)"
    return "hold_insufficient_supply_or_too_broad(공급 부족 또는 과도 공급 보류)"


def build_design() -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    queue = read_csv_rows(SOURCE_QUEUE)
    support = read_csv_rows(SOURCE_SUPPORT)
    if not queue:
        raise ValueError("Stage276 probe queue(276단계 탐침 대기열)가 비어 있다.")
    control_path = support[0]["source_score_table"]
    control = load_table(control_path).reset_index(drop=True)
    branch_rows: list[dict[str, Any]] = []
    supply_rows: list[dict[str, Any]] = []
    threshold_rows: dict[str, Any] = {}
    masks_by_package: dict[str, dict[str, str]] = {}
    for queue_row in queue:
        package_id = str(queue_row["package_id"])
        frame = load_table(str(queue_row["source_score_table"])).reset_index(drop=True)
        thresholds = train_thresholds(frame)
        threshold_rows[package_id] = thresholds
        package_masks: dict[str, str] = {}
        base_hash = ""
        for template in variant_templates(package_id, str(queue_row["fresh_thesis"]), thresholds):
            mask = decision_mask(frame, control, template)
            mask_hash = digest_mask(mask)
            duplicate_of = ""
            if template["variant_id"].endswith("_q01_base_surface"):
                base_hash = mask_hash
            elif mask_hash == base_hash:
                duplicate_of = "base_surface(기준 표면)"
            package_masks[str(template["variant_id"])] = mask_hash
            variant_supply = summarize_variant(package_id, str(template["variant_id"]), frame, control, mask)
            supply_rows.extend(variant_supply)
            recommendation = queue_recommendation(str(template["variant_id"]), variant_supply, duplicate_of)
            branch_rows.append(
                {
                    "variant_id": template["variant_id"],
                    "package_id": package_id,
                    "variant_role": template["variant_role"],
                    "fresh_thesis": template["fresh_thesis"],
                    "comparison_baseline": queue_row["support_control"],
                    "decision_rule": template["decision_rule"],
                    "thresholds_json": template["thresholds_json"],
                    "pressure_axis": template["pressure_axis"],
                    "upside_condition": template["upside_condition"],
                    "failure_mode": template["failure_mode"],
                    "discard_condition": template["discard_condition"],
                    "invalid_conditions": "claiming selected candidate(선택 후보 주장) or ONNX readiness(ONNX 준비 주장) before MT5 evidence(MT5 근거)",
                    "stop_conditions": "missing payload(페이로드 누락), missing MT5 output(MT5 출력 누락), or weak curve/trade quality(약한 곡선/거래 품질)",
                    "evidence_plan": "run276B payload;MT5 probe;balance/equity curve;trade quality;runtime handoff receipt",
                    "duplicate_of": duplicate_of,
                    "queue_recommendation": recommendation,
                    "claim_boundary": BOUNDARY,
                }
            )
        masks_by_package[package_id] = package_masks
    mt5_rows = build_mt5_queue(branch_rows, queue)
    threshold_payload = {
        "run_id": RUN_ID,
        "stage_id": STAGE276_ID,
        "threshold_source": "Tier A train split(티어 A 학습 분할)",
        "thresholds_by_package": threshold_rows,
        "decision_mask_hashes": masks_by_package,
        "claim_boundary": BOUNDARY,
    }
    return branch_rows, supply_rows, mt5_rows, threshold_payload


def build_mt5_queue(branch_rows: Sequence[Mapping[str, Any]], source_queue: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    source_by_package = {row["package_id"]: row for row in source_queue}
    queued = [row for row in branch_rows if str(row["queue_recommendation"]).startswith("queue_for_run276B")]
    queued = sorted(queued, key=lambda row: (str(row["package_id"]), str(row["variant_id"])))
    rows: list[dict[str, Any]] = []
    for index, row in enumerate(queued, start=1):
        package_id = str(row["package_id"])
        source = source_by_package[package_id]
        rows.append(
            {
                "queue_id": f"run276B_{index:02d}_{row['variant_id']}",
                "queue_priority": index,
                "variant_id": row["variant_id"],
                "package_id": package_id,
                "source_score_table": source["source_score_table"],
                "source_handoff_json": source["source_handoff_json"],
                "required_support_control": source["support_control"],
                "materialization_status": "ready_for_run276B_payload_materialization",
                "mt5_probe_question": "Does this branch(분기)가 MT5 runtime probe(MT5 런타임 탐침)에서 curve/trade quality(곡선/거래 품질)를 버티는가?",
                "success_condition": "net/PF/DD/recovery/expectancy(순수익/수익 팩터/손실폭/회복/기대값)가 함께 납득되고 weak slice(약한 구간)가 치명적으로 깨지지 않는다.",
                "discard_condition": row["discard_condition"],
                "required_evidence": "payload parquet;MT5 signal CSV;attempt manifest;tester output;KPI receipt;curve trade-quality review",
                "claim_boundary": BOUNDARY,
            }
        )
    return rows


def write_receipts(branch_rows: Sequence[Mapping[str, Any]], supply_rows: Sequence[Mapping[str, Any]], mt5_rows: Sequence[Mapping[str, Any]], threshold_payload: Mapping[str, Any]) -> None:
    write_csv(BRANCH_PLAN, BRANCH_COLUMNS, branch_rows)
    write_csv(BRANCH_SUPPLY, SUPPLY_COLUMNS, supply_rows)
    write_csv(MT5_QUEUE, MT5_QUEUE_COLUMNS, mt5_rows)
    write_json(THRESHOLD_RECEIPT, threshold_payload)
    write_json(
        EXPERIMENT_RECEIPT,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE276_ID,
            "source_run_id": SOURCE_RUN_ID,
            "hypothesis": "Stage275 probe seeds(275단계 탐침 씨앗)는 MT5 pressure probe(MT5 압박 탐침)로 보상 비대칭을 확인할 가치가 있다.",
            "decision_use": "run276B payload materialization(run276B 페이로드 물질화) 대기열을 만든다. 후보 선택은 하지 않는다.",
            "comparison_baseline": "cp275E q04 failure signature guard(q04 실패 서명 방어)",
            "control_variables": "source score table(원천 점수표), handoff JSON(인계 JSON), Tier A/B paired scope(티어 A/B 쌍 범위)",
            "changed_variables": "base/focused/q04-distance/risk-focus branch(기준/집중/q04 거리/위험 집중 분기)",
            "success_criteria": "MT5 probe design queue(MT5 탐침 설계 대기열)가 생성되고 각 분기 discard condition(폐기 조건)이 명시된다.",
            "failure_criteria": "no queue rows(대기열 없음), duplicate-only branches(중복 분기만 있음), missing source handoff(원천 인계 누락)",
            "invalid_conditions": "selected candidate(선택 후보) 또는 ONNX readiness(ONNX 준비)를 이 설계에서 주장하는 경우",
            "branch_rows": len(branch_rows),
            "mt5_queue_rows": len(mt5_rows),
            "selected_candidate": "none",
            "onnx_readiness": "not_claimed",
            "goal_achieve": "not_claimed",
            "claim_boundary": BOUNDARY,
        },
    )
    write_json(
        DATA_INTEGRITY_RECEIPT,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE276_ID,
            "source_inputs": [rel(path) for path in source_inputs()],
            "source_hashes": {rel(path): sha256_file_lf_normalized(path) for path in source_inputs() if path_exists(path)},
            "time_axis": "timestamp/split/tier_view(시각/분할/티어 보기)를 유지하고 새 bar(봉)를 만들지 않는다.",
            "feature_label_boundary": "label/profit columns(라벨/수익 열)을 쓰지 않고 score/signal/risk(점수/신호/위험)만 쓴다.",
            "split_boundary": "thresholds(임계값)는 Tier A train split(티어 A 학습 분할)에서만 얻는다.",
            "performance_claim": "none",
            "integrity_judgment": "usable_with_boundary(경계 포함 사용 가능)",
            "claim_boundary": BOUNDARY,
        },
    )
    write_json(
        MODEL_VALIDATION_RECEIPT,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE276_ID,
            "model_family": "deterministic branch design(결정론 분기 설계), no trained model(학습 모델 없음)",
            "selection_metric": "materialization readiness(물질화 준비성), not candidate selection(후보 선택 아님)",
            "overfit_risk": "branch rules(분기 규칙)가 Stage275 screen(275단계 선별)에 맞춰져 있으므로 MT5 pressure(MT5 압박)가 필수다.",
            "calibration_risk": "candidate_decision_score(후보 판단 점수)는 probability(확률)가 아니다.",
            "allowed_claims": ["mt5_probe_design_queue_ready(MT5 탐침 설계 대기열 준비)"],
            "forbidden_claims": ["selected_candidate(선택 후보)", "ONNX readiness(ONNX 준비)", "Goal Achieve(목표 달성)"],
            "claim_boundary": BOUNDARY,
        },
    )
    write_csv(RESULT_JUDGMENT, RESULT_COLUMNS, result_rows(mt5_rows))
    write_csv(GATE_AUDIT, GATE_COLUMNS, gate_rows(mt5_rows))


def result_rows(mt5_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, str]]:
    return [
        {
            "result_subject": RUN_ID,
            "evidence_available": "branch_plan(분기 계획), supply_metrics(공급 지표), mt5_probe_design_queue(MT5 탐침 설계 대기열), threshold_receipt(임계값 영수증)",
            "evidence_missing": "payload materialization(페이로드 물질화), MT5 tester output(MT5 테스터 출력), KPI receipt(KPI 영수증), curve/trade-quality review(곡선/거래 품질 검토)",
            "judgment_label": JUDGMENT,
            "judgment_class": "design_ready_no_candidate_selection",
            "claim_boundary": BOUNDARY,
            "next_condition": NEXT_ACTION,
            "user_explanation_hook": f"MT5 probe design queue(MT5 탐침 설계 대기열) {len(mt5_rows)}개가 준비됐지만 선택 후보는 아니다.",
        }
    ]


def gate_rows(mt5_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, str]]:
    return [
        {
            "gate_name": "scope_completion_gate(범위 완료 게이트)",
            "status": "passed(통과)" if mt5_rows else "failed_no_mt5_queue(MT5 대기열 없음)",
            "evidence_path": rel(MT5_QUEUE),
            "effect": "run276B(276B 실행)가 소비할 MT5 probe design queue(MT5 탐침 설계 대기열)를 만든다.",
        },
        {
            "gate_name": "kpi_contract_audit(KPI 계약 감사)",
            "status": "passed_with_boundary(경계 포함 통과)",
            "evidence_path": rel(RESULT_JUDGMENT),
            "effect": "이 실행은 trading KPI(거래 핵심 성과 지표)를 주장하지 않고 설계만 주장한다.",
        },
        {
            "gate_name": "data_integrity_gate(데이터 무결성 게이트)",
            "status": "passed(통과)",
            "evidence_path": rel(DATA_INTEGRITY_RECEIPT),
            "effect": "threshold(임계값), source hash(원천 해시), label boundary(라벨 경계)를 기록한다.",
        },
        {
            "gate_name": "final_claim_guard(최종 주장 방어)",
            "status": "passed(통과)",
            "evidence_path": rel(RESULT_JUDGMENT),
            "effect": "selected candidate(선택 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)를 주장하지 않는다.",
        },
    ]


def source_inputs() -> list[Path]:
    paths = [SOURCE_QUEUE, SOURCE_SUPPORT, SOURCE_FAILURE, SOURCE_INPUT_REFS, SOURCE_STAGE_BRIEF, SOURCE_CLOSEOUT, SOURCE_RUN275F_MANIFEST, SOURCE_RUN275F_LINEAGE]
    for row in read_csv_rows(SOURCE_QUEUE):
        paths.append(repo_path(row["source_score_table"]))
        paths.append(repo_path(row["source_handoff_json"]))
    for row in read_csv_rows(SOURCE_SUPPORT):
        paths.append(repo_path(row["source_score_table"]))
        paths.append(repo_path(row["source_handoff_json"]))
    return paths


def write_report(branch_rows: Sequence[Mapping[str, Any]], mt5_rows: Sequence[Mapping[str, Any]]) -> None:
    queue_lines = "\n".join(
        f"- `{row['variant_id']}` package(패키지) `{row['package_id']}` status(상태) `{row['materialization_status']}`"
        for row in mt5_rows
    )
    write_md(
        RUN_REPORT,
        f"""# run276A Aggressive Fresh Surface Probe Design(276A 공격형 새 표면 탐침 설계)

- run_id(실행 ID): `{RUN_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- branch_rows(분기 행): `{len(branch_rows)}`
- mt5_probe_design_queue_rows(MT5 탐침 설계 대기열 행): `{len(mt5_rows)}`
- selected_candidate(선택 후보): `none`
- ONNX readiness(ONNX 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_ACTION}`

## Plain Result(쉬운 결과)

run276A(276A 실행)는 Stage275(275단계)의 3개 probe seed(탐침 씨앗)를 branch plan(분기 계획)으로 확장했다.
효과(effect, 효과): run276B(276B 실행)는 MT5 signal payload(MT5 신호 페이로드)를 만들 수 있고, 아직 성과나 후보 선택은 주장하지 않는다.

## MT5 Queue(MT5 대기열)

{queue_lines}

## Evidence Paths(근거 경로)

- branch_plan(분기 계획): `{rel(BRANCH_PLAN)}`
- supply_metrics(공급 지표): `{rel(BRANCH_SUPPLY)}`
- mt5_probe_design_queue(MT5 탐침 설계 대기열): `{rel(MT5_QUEUE)}`
- thresholds(임계값): `{rel(THRESHOLD_RECEIPT)}`
- lineage(계보): `{rel(LINEAGE_RECEIPT)}`

## Boundary(경계)

`{BOUNDARY}`
""",
    )


def replace_line_prefix(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + replacement + "\n"


def append_once(text: str, marker: str, addition: str) -> str:
    if marker in text:
        return text
    return text.rstrip() + "\n\n" + addition.rstrip() + "\n"


def prepend_focus(text: str, focus: str, marker: str) -> str:
    if marker in text:
        return text
    anchor = "current_focus:\n"
    if anchor in text:
        return text.replace(anchor, anchor + focus, 1)
    return text.rstrip() + "\ncurrent_focus:\n" + focus


def update_stage_docs(branch_rows: Sequence[Mapping[str, Any]], mt5_rows: Sequence[Mapping[str, Any]]) -> None:
    selection = io_path(SELECTION_STATUS).read_text(encoding="utf-8-sig")
    selection = replace_line_prefix(selection, "- stage_status(", f"- stage_status(단계 상태): `{STATUS}`")
    selection = replace_line_prefix(selection, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    selection = replace_line_prefix(selection, "- last_completed_run(", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
    selection = replace_line_prefix(selection, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    selection = append_once(selection, "run276A_report", f"- run276A_report(276A 보고서): `{rel(RUN_REPORT)}`")
    selection = append_once(selection, "run276A_mt5_queue", f"- run276A_mt5_queue(276A MT5 대기열): `{rel(MT5_QUEUE)}`")
    write_md(SELECTION_STATUS, selection)

    review = io_path(REVIEW_INDEX).read_text(encoding="utf-8-sig")
    review = append_once(
        review,
        "run276A_report",
        "\n".join(
            [
                f"- run276A_report(276A 보고서): `{rel(RUN_REPORT)}`",
                f"- run276A_branch_plan(276A 분기 계획): `{rel(BRANCH_PLAN)}`",
                f"- run276A_mt5_queue(276A MT5 대기열): `{rel(MT5_QUEUE)}`",
            ]
        ),
    )
    write_md(REVIEW_INDEX, review)

    current = io_path(CURRENT_STATE).read_text(encoding="utf-8-sig")
    current = replace_line_prefix(current, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_line_prefix(current, "- status(", f"- status(상태): `{STATUS}`")
    current = replace_line_prefix(current, "- target_surface(", "- target_surface(목표 표면): `aggressive_fresh_surface_probe_design`")
    current = replace_line_prefix(current, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    current = append_once(
        current,
        "run276A_summary",
        (
            f"- run276A_summary(276A 요약): branch plan(분기 계획) `{len(branch_rows)}`행과 MT5 probe design queue(MT5 탐침 설계 대기열) "
            f"`{len(mt5_rows)}`행을 만들었다. Effect(효과): run276B(276B 실행)가 payload(페이로드)를 만들 수 있고, selected candidate(선택 후보), "
            "ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 주장하지 않는다."
        ),
    )
    write_md(CURRENT_STATE, current)

    workspace = io_path(WORKSPACE_STATE).read_text(encoding="utf-8-sig")
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    workspace = replace_line_prefix(workspace, "active_stage:", f"active_stage: {STAGE276_ID}")
    focus = (
        "- >-\n"
        f"  Stage276(276단계) run276A(276A 실행) aggressive fresh surface probe design(공격형 새 표면 탐침 설계) `{RUN_ID}`. "
        f"Effect(효과): branch plan(분기 계획) `{len(branch_rows)}`행과 MT5 probe design queue(MT5 탐침 설계 대기열) `{len(mt5_rows)}`행을 만들고, "
        "selected candidate(선택 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 주장하지 않는다.\n"
    )
    workspace = prepend_focus(workspace, focus, RUN_ID)
    write_md(WORKSPACE_STATE, workspace)

    changelog = io_path(CHANGELOG).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG) else "# Changelog(변경 기록)\n"
    changelog = append_once(
        changelog,
        RUN_ID,
        (
            "## 2026-05-23 run276A aggressive fresh surface probe design(276A 공격형 새 표면 탐침 설계)\n\n"
            f"- status(상태): `{STATUS}`\n"
            f"- judgment(판정): `{JUDGMENT}`\n"
            f"- effect(효과): MT5 probe design queue(MT5 탐침 설계 대기열) `{len(mt5_rows)}`행을 만들었다.\n"
            "- boundary(경계): selected candidate(선택 후보), ONNX readiness(ONNX 준비), Goal Achieve(목표 달성)는 `none/not_claimed`다.\n"
        ),
    )
    write_md(CHANGELOG, changelog)


def manifest_payload(created_at: str, artifacts: Sequence[Path], inputs: Sequence[Path], branch_rows: Sequence[Mapping[str, Any]], mt5_rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE276_ID,
        "source_run_id": SOURCE_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "created_at_utc": created_at,
        "producer": rel(PRODUCER_PATH),
        "entry_command": f"python {rel(PRODUCER_PATH)}",
        "source_inputs": [rel(path) for path in inputs],
        "input_hashes": {rel(path): sha256_file_lf_normalized(path) for path in inputs if path_exists(path)},
        "output_artifacts": [rel(path) for path in artifacts if path_exists(path)],
        "output_hashes": {rel(path): sha256_file_lf_normalized(path) for path in artifacts if path_exists(path)},
        "branch_rows": len(branch_rows),
        "mt5_probe_design_queue_rows": len(mt5_rows),
        "selected_candidate": "none",
        "selected_research_baseline": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "external_verification_status": "out_of_scope_by_claim_design_only",
        "next_action": NEXT_ACTION,
        "claim_boundary": BOUNDARY,
    }


def lineage_payload(manifest: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE276_ID,
        "source_run_id": SOURCE_RUN_ID,
        "source_inputs": manifest["source_inputs"],
        "producer": manifest["producer"],
        "consumer": [NEXT_ACTION, rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
        "artifact_paths": manifest["output_artifacts"],
        "artifact_hashes": manifest["output_hashes"],
        "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
        "availability": "tracked_generated_stage_local",
        "lineage_judgment": "connected_with_boundary(경계 포함 연결)",
        "claim_boundary": BOUNDARY,
    }


def update_registers(created_at: str, branch_rows: Sequence[Mapping[str, Any]], mt5_rows: Sequence[Mapping[str, Any]], artifacts: Sequence[Path]) -> None:
    upsert_csv_rows(
        RUN_REGISTRY,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE276_ID,
                "lane": "experiment_design",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(RUN_REPORT),
                "notes": f"branch_rows={len(branch_rows)};mt5_queue={len(mt5_rows)};selected_candidate=none;onnx_readiness=not_claimed;next_action={NEXT_ACTION}.",
            }
        ],
        key="run_id",
    )
    alpha_rows = [
        {
            "ledger_row_id": f"{RUN_ID}__{row['variant_id']}",
            "stage_id": STAGE276_ID,
            "run_id": RUN_ID,
            "subrun_id": row["variant_id"],
            "parent_run_id": SOURCE_RUN_ID,
            "record_view": "aggressive fresh surface probe design(공격형 새 표면 탐침 설계)",
            "tier_scope": "Tier A separate/Tier B separate/Tier A+B combined",
            "kpi_scope": "design_only_no_trading_kpi",
            "scoreboard_lane": "mt5_probe_design_queue",
            "status": STATUS,
            "judgment": row["queue_recommendation"],
            "path": rel(BRANCH_PLAN),
            "primary_kpi": f"package={row['package_id']};duplicate_of={row['duplicate_of']}",
            "guardrail_kpi": "selected_candidate=none;onnx_readiness=not_claimed;goal_achieve=not_claimed",
            "external_verification_status": "out_of_scope_by_claim_design_only",
            "notes": row["discard_condition"],
        }
        for row in branch_rows
    ]
    upsert_csv_rows(ALPHA_LEDGER, ALPHA_LEDGER_COLUMNS, alpha_rows, key="ledger_row_id")
    upsert_csv_rows(
        STAGE_LEDGER,
        STAGE_LEDGER_COLUMNS,
        [
            {
                "row_id": f"{RUN_ID}__design",
                "stage_id": STAGE276_ID,
                "run_id": RUN_ID,
                "view": "aggressive_fresh_surface_probe_design",
                "tier_scope": "Tier A separate/Tier B separate/Tier A+B combined",
                "scoreboard": "experiment_design",
                "status": STATUS,
                "judgment": JUDGMENT,
                "evidence_boundary": "design_only_no_candidate_no_onnx",
                "report_path": rel(RUN_REPORT),
                "notes": f"branch_rows={len(branch_rows)};mt5_queue={len(mt5_rows)};next_action={NEXT_ACTION}.",
            }
        ],
        key="row_id",
    )
    artifact_rows = [
        {
            "artifact_id": f"{RUN_ID}__{path.name.replace('.', '_')}",
            "artifact_type": "run276A_aggressive_probe_design_artifact",
            "path": rel(path),
            "sha256": sha256_file_lf_normalized(path),
            "stage_id": STAGE276_ID,
            "run_id": RUN_ID,
            "created_at_utc": created_at,
            "notes": "run276A aggressive fresh surface probe design artifact.",
        }
        for path in artifacts
        if path_exists(path)
    ]
    upsert_csv_rows(ARTIFACT_REGISTRY, ARTIFACT_COLUMNS, artifact_rows, key="artifact_id")


def run() -> dict[str, Any]:
    inputs = source_inputs()
    must_exist(inputs)
    io_path(RUN_DIR).mkdir(parents=True, exist_ok=True)
    created_at = utc_now()
    branch_rows, supply_rows, mt5_rows, threshold_payload = build_design()
    write_receipts(branch_rows, supply_rows, mt5_rows, threshold_payload)
    write_report(branch_rows, mt5_rows)
    artifacts = [
        BRANCH_PLAN,
        BRANCH_SUPPLY,
        MT5_QUEUE,
        THRESHOLD_RECEIPT,
        EXPERIMENT_RECEIPT,
        DATA_INTEGRITY_RECEIPT,
        MODEL_VALIDATION_RECEIPT,
        RESULT_JUDGMENT,
        GATE_AUDIT,
        RUN_REPORT,
    ]
    manifest = manifest_payload(created_at, artifacts, inputs, branch_rows, mt5_rows)
    write_json(RUN_MANIFEST, manifest)
    artifacts.append(RUN_MANIFEST)
    manifest = manifest_payload(created_at, artifacts, inputs, branch_rows, mt5_rows)
    write_json(LINEAGE_RECEIPT, lineage_payload(manifest))
    artifacts.append(LINEAGE_RECEIPT)
    manifest = manifest_payload(created_at, artifacts, inputs, branch_rows, mt5_rows)
    write_json(RUN_MANIFEST, manifest)

    update_stage_docs(branch_rows, mt5_rows)
    update_registers(created_at, branch_rows, mt5_rows, artifacts)

    return {
        "run_id": RUN_ID,
        "stage_id": STAGE276_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "branch_rows": len(branch_rows),
        "supply_rows": len(supply_rows),
        "mt5_probe_design_queue_rows": len(mt5_rows),
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": NEXT_ACTION,
        "report": rel(RUN_REPORT),
    }


def main() -> int:
    print(json.dumps(run(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
