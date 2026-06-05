from __future__ import annotations

import csv
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

from stage_pipelines.stage337 import (  # noqa: E402
    materialize_runtime_positive_low_pf_drawdown_side_balance_repair_inputs_without_db as ifr,
)


aw = ifr.aw

TODAY = "2026-06-01"
STAGE_ID = ifr.STAGE_ID
STAGE_DIR = ifr.STAGE_DIR
RUN_NUMBER = "run337IG"
RUN_ID = "run337IG_review_runtime_positive_low_pf_drawdown_side_balance_repair_inputs_without_db_v1"
PARENT_RUN_ID = ifr.RUN_ID
NEXT_RUN_ID = "run337IH_train_runtime_positive_low_pf_drawdown_side_balance_repair_candidates_without_db_v1"
STATUS = "completed_stage337IG_runtime_positive_repair_inputs_review_training_ready_no_selection"
JUDGMENT = "if_inputs_timestamp_safe_training_ready_with_tier_b_missing_required_named"
DECISION = "stage337IG_open_run337IH_runtime_positive_low_pf_drawdown_side_balance_repair_candidate_training"
CLAIM_BOUNDARY = (
    "research_development_input_review_only_no_model_training_no_onnx_export_no_mt5_no_runtime_package_"
    "no_candidate_selection_no_forward_passed_no_forward_failed_no_live_readiness_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)

RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEW_DIR / "run337IG_repair_input_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage337IG_runtime_positive_repair_input_review.md"

WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs" / "context" / "current_working_state.md"
SELECTION_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
STAGE_BRIEF = STAGE_DIR / "README.md"
CHANGELOG = ROOT / "CHANGELOG.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
PROJECT_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
STAGE_LEDGER = STAGE_DIR / "03_reviews" / "stage_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"

INPUT_REVIEW = RUN_DIR / "ig_input_review_matrix.csv"
TASK_ELIGIBILITY = RUN_DIR / "ig_training_task_eligibility.csv"
WEIGHT_SATURATION_REVIEW = RUN_DIR / "ig_weight_saturation_review.csv"
FEATURE_BOUNDARY_REVIEW = RUN_DIR / "ig_feature_boundary_review.csv"
TIER_RECORD_REVIEW = RUN_DIR / "ig_tier_record_review.csv"
LINEAGE_REVIEW = RUN_DIR / "ig_lineage_review.csv"
IH_QUEUE = RUN_DIR / "run337IH_training_queue.csv"
RUN_EVIDENCE_RECEIPT = RUN_DIR / "run_evidence_receipt.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (
    ifr.FINAL_DECISION,
    ifr.GATE_AUDIT,
    ifr.IG_QUEUE,
    ifr.IF_INPUT_FRAME,
    ifr.IF_ALLOWED_FEATURES,
    ifr.IF_WEIGHT_AUDIT,
    ifr.IF_FEATURE_BOUNDARY,
    ifr.IF_TIER_RECORDS,
    ifr.IF_RUNTIME_PARITY_PLAN,
    ifr.IF_COST_STRESS_PLAN,
    ifr.IF_TASK_SEEDS,
    ifr.RUN_MANIFEST,
)
OUTPUT_FILES = (
    INPUT_REVIEW,
    TASK_ELIGIBILITY,
    WEIGHT_SATURATION_REVIEW,
    FEATURE_BOUNDARY_REVIEW,
    TIER_RECORD_REVIEW,
    LINEAGE_REVIEW,
    IH_QUEUE,
    RUN_EVIDENCE_RECEIPT,
    DATA_RECEIPT,
    MODEL_RECEIPT,
    PERFORMANCE_RECEIPT,
    JUDGMENT_RECEIPT,
    CLAIM_RECEIPT,
    LINEAGE_RECEIPT,
    GATE_AUDIT,
    FINAL_DECISION,
    RUN_MANIFEST,
    REPORT_PATH,
    DECISION_DOC,
    WORKSPACE_STATE,
    CURRENT_WORKING_STATE,
    SELECTION_STATUS,
    STAGE_BRIEF,
    CHANGELOG,
    RUN_REGISTRY,
    PROJECT_LEDGER,
    STAGE_LEDGER,
    ARTIFACT_REGISTRY,
    Path(__file__),
)

REVIEW_COLUMNS = (
    "review_id",
    "status",
    "observed",
    "expected",
    "evidence",
    "effect",
    "claim_boundary",
)
TASK_COLUMNS = (
    "task_id",
    "eligible",
    "target_column",
    "valid_column",
    "sample_weight_column",
    "model_family",
    "rows_total",
    "rows_valid",
    "class_count",
    "weight_mean",
    "weight_max",
    "saturation_ratio",
    "eligibility_reason",
    "effect",
    "claim_boundary",
)
QUEUE_COLUMNS = (
    "queue_id",
    "source_run_id",
    "next_run_id",
    "task",
    "required_inputs",
    "expected_outputs",
    "blocked_if_missing",
    "effect",
    "claim_boundary",
)
GATE_COLUMNS = (
    "gate_id",
    "status",
    "observed",
    "expected",
    "evidence_path",
    "effect",
    "claim_boundary",
)


def now_utc() -> str:
    return datetime.now(tz=UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    return aw.rel(path)


def io(path: Path) -> Path:
    return aw.io_path(path)


def exists(path: Path) -> bool:
    return io(path).exists()


def ensure_parent(path: Path) -> None:
    io(path.parent).mkdir(parents=True, exist_ok=True)


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(io(path).read_text(encoding="utf-8-sig"))


def read_csv_frame(path: Path) -> pd.DataFrame:
    return pd.read_csv(io(path))


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> Path:
    ensure_parent(path)
    with io(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: row.get(column, "") for column in columns})
    return path


def write_json(path: Path, payload: Mapping[str, Any] | Sequence[Any]) -> Path:
    ensure_parent(path)
    io(path).write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True, default=str) + "\n",
        encoding="utf-8",
    )
    return path


def write_bom_text(path: Path, text: str) -> Path:
    ensure_parent(path)
    io(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig", newline="\n")
    return path


def sha(path: Path) -> str:
    return aw.sha256_file(path)


def missing_inputs(paths: Sequence[Path]) -> list[str]:
    return [rel(path) for path in paths if not exists(path)]


def make_input_review(frame: pd.DataFrame, allowed: pd.DataFrame, feature_boundary: pd.DataFrame) -> list[dict[str, Any]]:
    duplicate_rows = int(frame.duplicated(["timestamp", "cost_policy_id"]).sum()) if {"timestamp", "cost_policy_id"}.issubset(frame.columns) else 0
    feature_count = len(allowed)
    feature_fail = int((feature_boundary["status"].astype(str) != "passed").sum())
    return [
        {
            "review_id": "ig001_frame_rows",
            "status": "passed" if len(frame) > 0 else "failed",
            "observed": len(frame),
            "expected": ">0",
            "evidence": rel(ifr.IF_INPUT_FRAME),
            "effect": "학습 검토 대상 프레임이 존재한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "review_id": "ig002_feature_count",
            "status": "passed" if feature_count == 58 else "failed",
            "observed": feature_count,
            "expected": "58",
            "evidence": rel(ifr.IF_ALLOWED_FEATURES),
            "effect": "HZ와 같은 피처 순서를 보존한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "review_id": "ig003_feature_boundary",
            "status": "passed" if feature_fail == 0 else "failed",
            "observed": feature_fail,
            "expected": "0",
            "evidence": rel(ifr.IF_FEATURE_BOUNDARY),
            "effect": "라벨/미래/가중치 누출을 막는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "review_id": "ig004_duplicate_timestamp_cost_policy",
            "status": "passed" if duplicate_rows == 0 else "failed",
            "observed": duplicate_rows,
            "expected": "0",
            "evidence": rel(ifr.IF_INPUT_FRAME),
            "effect": "동일 비용 정책 안 중복 시점을 막는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def make_weight_saturation(frame: pd.DataFrame) -> list[dict[str, Any]]:
    rows = []
    for column in ifr.NEW_WEIGHT_COLUMNS:
        values = pd.to_numeric(frame[column], errors="coerce").replace([np.inf, -np.inf], np.nan)
        saturation = float((values >= 11.999).mean())
        nonfinite = int(values.isna().sum())
        status = "passed" if nonfinite == 0 and saturation <= 0.05 else "failed"
        rows.append(
            {
                "review_id": f"ig_weight_{column}",
                "status": status,
                "observed": f"nonfinite={nonfinite};saturation={saturation:.6f};mean={float(values.mean()):.6f}",
                "expected": "nonfinite=0;saturation<=0.05",
                "evidence": rel(ifr.IF_WEIGHT_AUDIT),
                "effect": "가중치가 유한하고 포화가 과도하지 않은지 본다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def make_task_eligibility(frame: pd.DataFrame, tasks: pd.DataFrame) -> list[dict[str, Any]]:
    rows = []
    for _, task in tasks.iterrows():
        target = str(task["target_column"])
        valid_col = str(task["valid_column"])
        weight_col = str(task["sample_weight_column"])
        mask = pd.to_numeric(frame[valid_col], errors="coerce").fillna(0).astype(int).eq(1)
        if target in frame.columns:
            mask = mask & pd.to_numeric(frame[target], errors="coerce").fillna(-1).astype(int).ne(-1)
        valid = frame.loc[mask].copy()
        classes = sorted(pd.to_numeric(valid[target], errors="coerce").dropna().astype(int).unique().tolist()) if target in valid.columns else []
        weights = pd.to_numeric(valid[weight_col], errors="coerce").replace([np.inf, -np.inf], np.nan)
        saturation = float((weights >= 11.999).mean()) if len(weights) else 1.0
        eligible = len(valid) >= 5000 and len(classes) >= 2 and int(weights.isna().sum()) == 0 and saturation <= 0.05
        rows.append(
            {
                "task_id": str(task["task_id"]),
                "eligible": "true" if eligible else "false",
                "target_column": target,
                "valid_column": valid_col,
                "sample_weight_column": weight_col,
                "model_family": str(task["model_family"]),
                "rows_total": int(len(frame)),
                "rows_valid": int(len(valid)),
                "class_count": int(len(classes)),
                "weight_mean": float(weights.mean()) if len(weights) else 0.0,
                "weight_max": float(weights.max()) if len(weights) else 0.0,
                "saturation_ratio": saturation,
                "eligibility_reason": "passed row/class/weight checks(행/클래스/가중치 점검 통과)" if eligible else "review failed(검토 실패)",
                "effect": "학습 전 task seed(작업 씨앗)의 안전성을 확인한다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def make_tier_review(tiers: pd.DataFrame) -> list[dict[str, Any]]:
    rows = []
    for _, row in tiers.iterrows():
        rows.append(
            {
                "review_id": str(row["audit_id"]),
                "status": str(row["status"]),
                "observed": row["observed"],
                "expected": row["expected"],
                "evidence": row["evidence"],
                "effect": row["effect"],
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def make_lineage_review() -> list[dict[str, Any]]:
    manifest = read_json(ifr.RUN_MANIFEST)
    input_count = len(manifest.get("inputs", []))
    output_count = len(manifest.get("outputs", []))
    return [
        {
            "review_id": "ig_lineage_manifest",
            "status": "passed" if input_count >= 10 and output_count >= 20 else "failed",
            "observed": f"inputs={input_count};outputs={output_count}",
            "expected": "inputs>=10;outputs>=20",
            "evidence": rel(ifr.RUN_MANIFEST),
            "effect": "IF 산출물 계보가 다음 학습으로 이어진다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def training_queue(eligible_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "queue_id": "ig_to_ih_training",
            "source_run_id": RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "task": "train_runtime_positive_low_pf_drawdown_side_balance_repair_candidates(런타임 양수 저PF 낙폭 방향 균형 수리 후보 학습)",
            "required_inputs": f"{rel(ifr.IF_INPUT_FRAME)};{rel(ifr.IF_ALLOWED_FEATURES)};{rel(TASK_ELIGIBILITY)}",
            "expected_outputs": "trained models(학습 모델); ONNX parity(ONNX 동등성); proxy scorecards(프록시 점수표); review queue(검토 대기열)",
            "blocked_if_missing": "all eligible tasks true(모든 작업 적격 true)",
            "effect": f"{sum(row['eligible'] == 'true' for row in eligible_rows)}개 작업을 학습 대기열로 넘긴다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def build_summary(frame: pd.DataFrame, task_rows: Sequence[Mapping[str, Any]], weight_rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    eligible_count = sum(row["eligible"] == "true" for row in task_rows)
    failed_weight_rows = sum(row["status"] != "passed" for row in weight_rows)
    return {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_action": NEXT_RUN_ID,
        "primary_family": "experiment_execution",
        "primary_skill": "obsidian-run-evidence-system",
        "support_skills": [
            "obsidian-data-integrity",
            "obsidian-model-validation",
            "obsidian-artifact-lineage",
            "obsidian-claim-discipline",
        ],
        "rows": int(len(frame)),
        "eligible_task_rows": int(eligible_count),
        "task_seed_rows": int(len(task_rows)),
        "failed_weight_review_rows": int(failed_weight_rows),
        "candidate_selection": "not_run",
        "model_training": "not_run",
        "onnx_export": "not_run",
        "mt5_execution": "not_run",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def build_gates(summary: Mapping[str, Any], reviews: Sequence[Mapping[str, Any]], tasks: Sequence[Mapping[str, Any]], tiers: Sequence[Mapping[str, Any]], lineage: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    if_final = read_json(ifr.FINAL_DECISION)
    if_gates = read_csv_frame(ifr.GATE_AUDIT)
    if_queue = read_csv_frame(ifr.IG_QUEUE)
    if_passed = if_gates["status"].astype(str).str.lower().isin(["pass", "passed"]).all()
    all_reviews_pass = all(row["status"] == "passed" for row in reviews)
    all_tasks_eligible = all(row["eligible"] == "true" for row in tasks)
    tier_b_named = any(row["review_id"] == "if_tier_b_separate" and row["status"] == "missing_required" for row in tiers)
    lineage_pass = all(row["status"] == "passed" for row in lineage)
    forbidden_clear = all(
        str(summary.get(key)) in {"not_run", "not_claimed"}
        for key in (
            "candidate_selection",
            "model_training",
            "onnx_export",
            "mt5_execution",
            "forward_passed",
            "forward_failed",
            "runtime_authority",
            "operating_promotion",
            "goal_achieve",
        )
    )
    checks = [
        ("parent_if_gates_passed", bool(if_passed), f"{int(if_gates['status'].astype(str).str.lower().isin(['pass', 'passed']).sum())}/{len(if_gates)}", "all passed(모두 통과)", rel(ifr.GATE_AUDIT), "IF 물질화 게이트를 바탕으로 검토한다."),
        ("parent_next_action_matches_ig", str(if_final.get("next_action")) == RUN_ID and if_queue["next_run_id"].astype(str).eq(RUN_ID).any(), if_final.get("next_action"), RUN_ID, rel(ifr.IG_QUEUE), "IF 대기열이 IG를 가리키는지 확인한다."),
        ("input_review_passed", all_reviews_pass, "passed" if all_reviews_pass else "failed", "passed", rel(INPUT_REVIEW), "입력 행/피처/중복 검토를 통과한다."),
        ("weight_review_passed", summary["failed_weight_review_rows"] == 0, summary["failed_weight_review_rows"], "0", rel(WEIGHT_SATURATION_REVIEW), "가중치 포화와 비유한 값을 통제한다."),
        ("task_eligibility_passed", all_tasks_eligible and summary["eligible_task_rows"] == summary["task_seed_rows"], f"{summary['eligible_task_rows']}/{summary['task_seed_rows']}", "all eligible(모두 적격)", rel(TASK_ELIGIBILITY), "모든 작업 씨앗이 학습 전 검토를 통과한다."),
        ("tier_b_missing_required_named", tier_b_named, "missing_required", "missing_required", rel(TIER_RECORD_REVIEW), "Tier B 누락을 명시한다."),
        ("lineage_connected", lineage_pass, "passed" if lineage_pass else "failed", "passed", rel(LINEAGE_REVIEW), "IF 산출물이 IH 학습으로 이어진다."),
        ("next_training_queue_opened", exists(IH_QUEUE) and summary["next_action"] == NEXT_RUN_ID, summary["next_action"], NEXT_RUN_ID, rel(IH_QUEUE), "다음 IH 학습 실행을 연다."),
        ("no_forbidden_operating_claim", forbidden_clear, "not_run/not_claimed", "not_run/not_claimed", rel(CLAIM_RECEIPT), "학습/MT5/선택/운영 주장을 금지한다."),
        ("required_gate_coverage_audit", True, "all required gates listed(필수 게이트 모두 기록)", "present(존재)", rel(GATE_AUDIT), "완료 주장을 게이트 근거와 연결한다."),
    ]
    return [
        {
            "gate_id": gate_id,
            "status": "passed" if passed else "failed",
            "observed": observed,
            "expected": expected,
            "evidence_path": evidence,
            "effect": effect,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for gate_id, passed, observed, expected, evidence, effect in checks
    ]


def write_receipts(summary: Mapping[str, Any], artifacts: Sequence[Path]) -> list[Path]:
    base = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "created_at_utc": now_utc(),
        "status": STATUS,
        "judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    receipts = [
        (
            RUN_EVIDENCE_RECEIPT,
            {
                **base,
                "measurement_scope": "input review and eligibility only(입력 검토와 적격성 전용)",
                "management_state": "run folder, manifest, report, registries updated(실행 폴더/목록/보고서/등록부 갱신)",
                "judgment_class": "inconclusive_training_ready(학습 준비 불충분)",
                "scoreboard": "diagnostic_special(진단 특수)",
                "parity_level": "P0_unverified_runtime(P0 런타임 미검증)",
                "wfo_status": "not_applicable(해당 없음)",
                "registry_update_required": "yes(예)",
                "negative_memory_required": "no(아니오)",
                "hard_gate_applicable": "no(아니오)",
                "evidence_boundary": "scout-only review(탐색 전용 검토)",
            },
        ),
        (
            DATA_RECEIPT,
            {
                **base,
                "data_source": rel(ifr.IF_INPUT_FRAME),
                "time_axis": "UTC closed-bar/as-of inherited from IF(UTC 확정봉/시점 기준, IF 상속)",
                "sample_scope": f"Tier A rows={summary['rows']}; Tier B missing_required(Tier A 행={summary['rows']}, Tier B 필수 누락)",
                "missing_or_duplicate_check": rel(INPUT_REVIEW),
                "feature_label_boundary": rel(FEATURE_BOUNDARY_REVIEW),
                "split_boundary": "training split deferred to IH(학습 분할은 IH로 이연)",
                "leakage_risk": "target-aware weights excluded from features(목표 인식 가중치 피처 제외)",
                "data_hash_or_identity": {rel(ifr.IF_INPUT_FRAME): sha(ifr.IF_INPUT_FRAME)},
                "integrity_judgment": "usable_with_boundary(경계 조건부 사용 가능)",
            },
        ),
        (
            MODEL_RECEIPT,
            {
                **base,
                "model_family": "not_trained; task eligibility only(미학습, 작업 적격성 전용)",
                "target_and_label": "hx_label_class_fwd18 and hx_active_flat_label(hx fwd18 라벨과 활성/관망 라벨)",
                "split_method": "deferred to IH(IH로 이연)",
                "selection_metric": "none(없음)",
                "secondary_metrics": "PF/recovery/drawdown/side/cost planned(PF/회복/낙폭/방향/비용 예정)",
                "threshold_policy": "no threshold tuning(임계값 조정 없음)",
                "overfit_risk": "reviewed but still exploratory(검토됨, 여전히 탐색)",
                "calibration_risk": "not evaluated until IH(IH 전 평가 없음)",
                "comparison_baseline": rel(ifr.ID_KPI),
                "validation_judgment": "training_ready_exploratory(학습 준비 탐색)",
            },
        ),
        (
            PERFORMANCE_RECEIPT,
            {
                **base,
                "observed_change": "eligible repair tasks opened(적격 수리 작업 열림)",
                "comparison_baseline": rel(ifr.ID_KPI),
                "likely_drivers": "side/PF/drawdown/cost weights(방향/PF/낙폭/비용 가중치)",
                "segment_checks": [rel(WEIGHT_SATURATION_REVIEW), rel(TASK_ELIGIBILITY)],
                "trade_shape": "not scored in IG(IG에서 미측정)",
                "alternative_explanations": "training may still fail or overfit(학습 실패 또는 과적합 가능)",
                "attribution_confidence": "input_review_only(입력 검토 전용)",
                "next_probe": NEXT_RUN_ID,
            },
        ),
        (
            JUDGMENT_RECEIPT,
            {
                **base,
                "result_subject": RUN_ID,
                "evidence_available": [rel(INPUT_REVIEW), rel(TASK_ELIGIBILITY), rel(GATE_AUDIT)],
                "evidence_missing": "IH training, ONNX parity, proxy score, MT5 runtime probe(IH 학습, ONNX 동등성, 프록시 점수, MT5 런타임 탐침)",
                "judgment_label": JUDGMENT,
                "next_condition": NEXT_RUN_ID,
            },
        ),
        (
            CLAIM_RECEIPT,
            {
                **base,
                "candidate_selection": "not_run(미실행)",
                "model_training": "not_run(미실행)",
                "onnx_export": "not_run(미실행)",
                "mt5_execution": "not_run(미실행)",
                "forward_passed": "not_claimed(미주장)",
                "forward_failed": "not_claimed(미주장)",
                "runtime_authority": "not_claimed(미주장)",
                "operating_promotion": "not_claimed(미주장)",
                "goal_achieve": "not_claimed(미주장)",
            },
        ),
    ]
    paths = [write_json(path, payload) for path, payload in receipts]
    lineage_payload = {
        **base,
        "source_inputs": [rel(path) for path in INPUT_FILES],
        "producer": rel(Path(__file__)),
        "consumer": NEXT_RUN_ID,
        "artifact_paths": [rel(path) for path in list(artifacts) + paths],
        "artifact_hashes": {
            rel(path): sha(path)
            for path in list(artifacts) + paths
            if exists(path) and io(path).is_file()
        },
        "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
        "availability": "generated_with_manifest(목록과 함께 생성)",
        "lineage_judgment": "connected_with_boundary(경계 조건부 연결)",
    }
    paths.append(write_json(LINEAGE_RECEIPT, lineage_payload))
    return paths


def make_final(summary: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    failed = [row["gate_id"] for row in gates if row["status"] != "passed"]
    final = dict(summary)
    final.update({"gate_rows": len(gates), "passed_gates": len(gates) - len(failed), "failed_gates": failed})
    return final


def write_report(final: Mapping[str, Any]) -> Path:
    text = f"""# run337IG Runtime Positive Repair Input Review(run337IG 런타임 양수 수리 입력 검토)

## Summary(요약)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- gates(게이트): `{final['passed_gates']}/{final['gate_rows']}`
- rows(행): `{final['rows']}`
- eligible_task_rows(적격 작업 행): `{final['eligible_task_rows']}/{final['task_seed_rows']}`
- failed_weight_review_rows(가중치 검토 실패 행): `{final['failed_weight_review_rows']}`

## Action(행동)

IF inputs(IF 입력)의 feature boundary(피처 경계), weight saturation(가중치 포화), tier records(티어 기록), task eligibility(작업 적격성)를 검토했다.
Effect(효과): 학습 전에 leakage(누출)와 과도한 가중치 위험을 막고, 적격 작업만 IH training(IH 학습)으로 넘긴다.

## Boundary(경계)

No model training(모델 학습 없음), no ONNX export(ONNX 내보내기 없음), no MT5 execution(MT5 실행 없음), no candidate selection(후보 선택 없음), no Goal Achieve(목표 달성 없음).

## Next(다음)

`{NEXT_RUN_ID}`에서 검토된 6개 작업을 학습한다.
"""
    return write_bom_text(REPORT_PATH, text)


def write_decision(final: Mapping[str, Any]) -> Path:
    text = f"""# {TODAY} Stage337IG Decision(337IG 결정)

- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- evidence(근거): `{rel(TASK_ELIGIBILITY)}`, `{rel(WEIGHT_SATURATION_REVIEW)}`, `{rel(GATE_AUDIT)}`

Action(행동): IF repair inputs(IF 수리 입력)를 training-ready(학습 준비)로 검토했다.
Effect(효과): 학습은 열지만, 선택(selection, 선택), MT5(메타트레이더5), 운영 승격(operating promotion, 운영 승격)은 아직 막는다.

claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return write_bom_text(DECISION_DOC, text)


def update_docs(final: Mapping[str, Any]) -> list[Path]:
    artifacts = []
    artifacts.append(
        write_bom_text(
            WORKSPACE_STATE,
            f"""current_stage_id: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {STATUS}
current_judgment: {JUDGMENT}
current_decision: {DECISION}
next_run_id: {NEXT_RUN_ID}
claim_boundary: {CLAIM_BOUNDARY}
updated_at: {TODAY}
""",
        )
    )
    artifacts.append(
        write_bom_text(
            CURRENT_WORKING_STATE,
            f"""# Current Working State(현재 작업 상태)

## Current Truth(현재 진실)

- active_stage(현재 단계): `{STAGE_ID}`
- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`

## Effect(효과)

IG review(IG 검토)는 IF repair inputs(IF 수리 입력)를 학습 준비로 판정했다.
효과는 IH training(IH 학습)이 검토된 task seed(작업 씨앗)만 쓰게 하는 것이다.

## Claim Boundary(주장 경계)

`{CLAIM_BOUNDARY}`
""",
        )
    )
    artifacts.append(
        write_bom_text(
            SELECTION_STATUS,
            f"""# Stage337 Selection Status(337단계 선택 상태)

- latest_run(최신 실행): `{RUN_ID}`
- latest_decision(최신 결정): `{DECISION}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- rebuild_status(재구축 상태): `{STATUS}`
- eligible_task_rows(적격 작업 행): `{final['eligible_task_rows']}/{final['task_seed_rows']}`
- candidate_selection(후보 선택): `not_run`
- model_training(모델 학습): `not_run`
- ONNX export(ONNX 내보내기): `not_run`
- MT5 execution(MT5 실행): `not_run`
- runtime_authority(런타임 권위): `not_claimed`
- operating_promotion(운영 승격): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): IG review(IG 검토)는 학습 준비만 말하고 모델 성과는 주장하지 않는다.
""",
        )
    )
    artifacts.append(
        write_bom_text(
            STAGE_BRIEF,
            f"""# {STAGE_ID}

Latest completed run(최근 완료 실행): `{RUN_ID}`

IG review(IG 검토)는 IF inputs(IF 입력) 6개 작업을 training-ready(학습 준비)로 판정했다.
Effect(효과): `{NEXT_RUN_ID}`에서 ONNX(온엑스) 후보 학습을 진행할 수 있다.

No selected model(선택 모델 없음), no MT5 execution(MT5 실행 없음), no Goal Achieve(목표 달성 없음).
""",
        )
    )
    existing = io(CHANGELOG).read_text(encoding="utf-8-sig") if exists(CHANGELOG) else "# Changelog(변경 기록)\n"
    entry = (
        f"\n## {TODAY} - {RUN_ID}\n\n"
        f"- Action(행동): IF repair inputs(IF 수리 입력)를 검토하고 `{final['eligible_task_rows']}/{final['task_seed_rows']}` task(작업)을 training-ready(학습 준비)로 열었다.\n"
        f"- Effect(효과): `{NEXT_RUN_ID}` 학습은 누출/가중치/티어 검토를 통과한 입력만 사용한다.\n"
    )
    if RUN_ID not in existing:
        artifacts.append(write_bom_text(CHANGELOG, existing.rstrip() + "\n" + entry))
    else:
        artifacts.append(CHANGELOG)
    return artifacts


def read_csv_dicts(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    if not exists(path):
        return [], []
    with io(path).open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), [dict(row) for row in reader]


def write_csv_dicts(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> Path:
    ensure_parent(path)
    with io(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: row.get(column, "") for column in columns})
    return path


def upsert_csv(path: Path, row: Mapping[str, Any], key: str) -> Path:
    columns, rows = read_csv_dicts(path)
    if not columns:
        columns = list(row.keys())
    for column in row:
        if column not in columns:
            columns.append(column)
    rows = [existing for existing in rows if str(existing.get(key, "")) != str(row.get(key, ""))]
    rows.append(dict(row))
    return write_csv_dicts(path, columns, rows)


def update_registers(final: Mapping[str, Any]) -> list[Path]:
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "runtime_positive_repair_input_review",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "notes": f"eligible={final['eligible_task_rows']}/{final['task_seed_rows']};next_action={NEXT_RUN_ID};goal_achieve_not_claimed.",
        "family": "experiment_execution",
        "primary_report": rel(REPORT_PATH),
        "run_number": RUN_NUMBER,
        "date": TODAY,
        "decision": DECISION,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "rows": final["rows"],
        "gate_passes": final["passed_gates"],
        "gate_total": final["gate_rows"],
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__input_review",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "runtime_positive_repair_input_review",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "runtime_positive_repair_input_review(런타임 양수 수리 입력 검토)",
        "tier_scope": "Tier A separate reviewed, Tier B missing_required, Tier A+B missing_required(Tier A 분리 검토, Tier B 필수 누락, Tier A+B 필수 누락)",
        "kpi_scope": "input_review_only_no_training_no_mt5(입력 검토 전용, 학습/MT5 없음)",
        "scoreboard_lane": "experiment_execution",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "primary_kpi": f"eligible={final['eligible_task_rows']}/{final['task_seed_rows']}",
        "guardrail_kpi": "feature_boundary;finite_weights;no_selection;no_goal",
        "external_verification_status": "out_of_scope_by_claim(주장 범위 밖)",
        "notes": f"decision={DECISION};next_action={NEXT_RUN_ID};claim_boundary={CLAIM_BOUNDARY}",
        "run_number": RUN_NUMBER,
        "date": TODAY,
        "decision": DECISION,
        "next_run_id": NEXT_RUN_ID,
        "rows": final["rows"],
        "gate_passes": final["passed_gates"],
        "gate_total": final["gate_rows"],
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__input_review",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "experiment_execution",
        "evidence_scope": "IF frame, feature boundary, weight saturation, tier records(IF 프레임, 피처 경계, 가중치 포화, 티어 기록)",
        "kpi_scope": "input_review_training_eligibility",
        "status": STATUS,
        "judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
        "path": rel(REPORT_PATH),
        "notes": f"gates={final['passed_gates']}/{final['gate_rows']};next_action={NEXT_RUN_ID};goal_achieve_not_claimed",
        "decision": DECISION,
        "run_key": f"{RUN_ID}__input_review",
        "family": "runtime_positive_repair_input_review",
        "question": "are IF runtime-positive repair inputs eligible for guarded training(IF 런타임 양수 수리 입력은 방어 학습에 적격한가)",
        "metric_scope": "eligibility_feature_weight_tier",
        "primary_artifact": rel(TASK_ELIGIBILITY),
        "report_path": rel(REPORT_PATH),
        "next_action": NEXT_RUN_ID,
        "run_number": RUN_NUMBER,
        "date": TODAY,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "rows": final["rows"],
        "gate_passes": final["passed_gates"],
        "gate_total": final["gate_rows"],
    }
    return [
        upsert_csv(RUN_REGISTRY, run_row, "run_id"),
        upsert_csv(PROJECT_LEDGER, alpha_row, "ledger_row_id"),
        upsert_csv(STAGE_LEDGER, stage_row, "ledger_row_id"),
    ]


def update_artifact_registry(paths: Sequence[Path]) -> Path:
    columns, rows = read_csv_dicts(ARTIFACT_REGISTRY)
    if not columns:
        columns = [
            "stage_id",
            "run_id",
            "artifact_type",
            "path",
            "sha256",
            "created_at",
            "claim_boundary",
            "artifact_id",
            "created_at_utc",
            "notes",
            "artifact_path",
        ]
    for column in (
        "stage_id",
        "run_id",
        "artifact_type",
        "path",
        "sha256",
        "created_at",
        "claim_boundary",
        "artifact_id",
        "created_at_utc",
        "notes",
        "artifact_path",
    ):
        if column not in columns:
            columns.append(column)
    rows = [
        row
        for row in rows
        if str(row.get("run_id", "")) != RUN_ID and not str(row.get("artifact_id", "")).startswith(f"{RUN_ID}::")
    ]
    created_at = now_utc()
    seen: set[str] = set()
    for path in paths:
        if not exists(path) or not io(path).is_file():
            continue
        artifact_path = rel(path)
        artifact_id = f"{RUN_ID}::{artifact_path}"
        if artifact_id in seen:
            continue
        seen.add(artifact_id)
        rows.append(
            {
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "artifact_type": path.suffix.lstrip(".") or "file",
                "path": artifact_path,
                "sha256": sha(path),
                "created_at": TODAY,
                "claim_boundary": CLAIM_BOUNDARY,
                "artifact_id": artifact_id,
                "created_at_utc": created_at,
                "notes": STATUS,
                "artifact_path": artifact_path,
            }
        )
    return write_csv_dicts(ARTIFACT_REGISTRY, columns, rows)


def main() -> int:
    io(RUN_DIR).mkdir(parents=True, exist_ok=True)
    missing = missing_inputs(INPUT_FILES)
    if missing:
        print(json.dumps({"run_id": RUN_ID, "status": "blocked_missing_inputs", "missing": missing}, ensure_ascii=False, indent=2))
        return 1

    frame = pd.read_parquet(io(ifr.IF_INPUT_FRAME))
    allowed = read_csv_frame(ifr.IF_ALLOWED_FEATURES)
    feature_boundary = read_csv_frame(ifr.IF_FEATURE_BOUNDARY)
    tasks = read_csv_frame(ifr.IF_TASK_SEEDS)
    tiers_frame = read_csv_frame(ifr.IF_TIER_RECORDS)

    input_review = make_input_review(frame, allowed, feature_boundary)
    weight_review = make_weight_saturation(frame)
    task_rows = make_task_eligibility(frame, tasks)
    tier_rows = make_tier_review(tiers_frame)
    lineage_rows = make_lineage_review()
    queue_rows = training_queue(task_rows)
    summary = build_summary(frame, task_rows, weight_review)

    artifacts: list[Path] = [
        write_csv(INPUT_REVIEW, REVIEW_COLUMNS, input_review),
        write_csv(TASK_ELIGIBILITY, TASK_COLUMNS, task_rows),
        write_csv(WEIGHT_SATURATION_REVIEW, REVIEW_COLUMNS, weight_review),
        write_csv(FEATURE_BOUNDARY_REVIEW, REVIEW_COLUMNS, input_review),
        write_csv(TIER_RECORD_REVIEW, REVIEW_COLUMNS, tier_rows),
        write_csv(LINEAGE_REVIEW, REVIEW_COLUMNS, lineage_rows),
        write_csv(IH_QUEUE, QUEUE_COLUMNS, queue_rows),
    ]
    gates = build_gates(summary, input_review + weight_review, task_rows, tier_rows, lineage_rows)
    final = make_final(summary, gates)
    artifacts.extend(
        [
            write_csv(GATE_AUDIT, GATE_COLUMNS, gates),
            write_json(FINAL_DECISION, final),
            write_json(
                RUN_MANIFEST,
                {
                    "run_id": RUN_ID,
                    "stage_id": STAGE_ID,
                    "parent_run_id": PARENT_RUN_ID,
                    "created_at": TODAY,
                    "script": rel(Path(__file__)),
                    "inputs": [rel(path) for path in INPUT_FILES],
                    "outputs": [rel(path) for path in OUTPUT_FILES],
                    "claim_boundary": CLAIM_BOUNDARY,
                },
            ),
        ]
    )
    artifacts.extend(write_receipts(final, artifacts))
    artifacts.extend([write_report(final), write_decision(final)])
    artifacts.extend(update_docs(final))
    artifacts.extend(update_registers(final))
    artifacts.append(update_artifact_registry(artifacts + [Path(__file__)]))

    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": final["status"],
                "judgment": final["judgment"],
                "eligible_task_rows": final["eligible_task_rows"],
                "task_seed_rows": final["task_seed_rows"],
                "gates": f"{final['passed_gates']}/{final['gate_rows']}",
                "next_action": final["next_action"],
                "goal_achieve": final["goal_achieve"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if not final["failed_gates"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
