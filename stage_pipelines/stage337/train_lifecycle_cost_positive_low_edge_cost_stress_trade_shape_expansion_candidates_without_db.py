from __future__ import annotations

import json
import re
import sys
from datetime import UTC, datetime
from pathlib import Path
from types import SimpleNamespace
from typing import Any, Iterable, Mapping, Sequence

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from stage_pipelines.stage337 import (  # noqa: E402
    review_lifecycle_cost_positive_low_edge_cost_stress_trade_shape_expansion_inputs_without_db as iw,
)
from stage_pipelines.stage337 import (  # noqa: E402
    train_proxy_mt5_negative_lifecycle_cost_trade_shape_repair_candidates_without_db as train_base,
)


aw = iw.aw

TODAY = "2026-06-01"
STAGE_ID = iw.STAGE_ID
STAGE_DIR = iw.STAGE_DIR
RUN_NUMBER = "run337IX"
RUN_ID = "run337IX_train_lifecycle_cost_positive_low_edge_cost_stress_trade_shape_expansion_candidates_without_db_v1"
PARENT_RUN_ID = iw.RUN_ID
NEXT_RUN_ID = "run337IY_review_lifecycle_cost_positive_low_edge_cost_stress_trade_shape_expansion_training_without_db_v1"
STATUS = "completed_stage337IX_positive_low_edge_expansion_candidates_trained_onnx_materialized_review_required_no_selection_no_mt5"
JUDGMENT = "positive_low_edge_expansion_candidates_trained_with_onnx_parity_and_proxy_score_review_required"
DECISION = "stage337IX_open_run337IY_positive_low_edge_expansion_training_review"
CLAIM_BOUNDARY = (
    "research_development_candidate_training_only_no_threshold_tuning_no_lot_optimization_no_candidate_selection_"
    "no_mt5_execution_no_forward_passed_no_forward_failed_no_runtime_package_authority_no_live_readiness_"
    "no_operating_promotion_no_runtime_authority_no_goal_achieve"
)

RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
MODEL_DIR = RUN_DIR / "models"
ONNX_DIR = RUN_DIR / "onnx"
REVIEW_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEW_DIR / "run337IX_positive_low_edge_expansion_candidate_training.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage337IX_positive_low_edge_expansion_candidate_training.md"

WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs" / "context" / "current_working_state.md"
SELECTION_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
STAGE_BRIEF = STAGE_DIR / "README.md"
ROOT_CHANGELOG = ROOT / "CHANGELOG.md"
WORKSPACE_CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
PROJECT_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
STAGE_LEDGER = STAGE_DIR / "03_reviews" / "stage_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"

FEATURE_SCHEMA = RUN_DIR / "ix_allowed_feature_schema.json"
TRAINING_TASK_REVIEW = RUN_DIR / "ix_training_task_review.csv"
SAMPLE_WEIGHT_AUDIT = RUN_DIR / "ix_sample_weight_audit.csv"
TRAINED_MODEL_MANIFEST = RUN_DIR / "ix_trained_model_manifest.csv"
ONNX_PARITY = RUN_DIR / "ix_onnx_parity_matrix.csv"
CLASSIFICATION_SCORECARD = RUN_DIR / "ix_inner_holdout_classification_scorecard.csv"
PROXY_TRADE_SCORECARD = RUN_DIR / "ix_inner_holdout_proxy_trade_scorecard.csv"
FEATURE_IMPORTANCE = RUN_DIR / "ix_feature_importance_top20.csv"
RUNTIME_FIREWALL = RUN_DIR / "ix_runtime_firewall_review.csv"
RELEASE_DISPOSITION = RUN_DIR / "ix_training_release_disposition.csv"
IY_QUEUE = RUN_DIR / "run337IY_review_queue.csv"
RUN_EVIDENCE_RECEIPT = RUN_DIR / "run_evidence_receipt.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

FEATURE_SET_ID = "iv_positive_low_edge_allowed_pretrade_features_v1"

INPUT_FILES = (
    iw.FINAL_DECISION,
    iw.GATE_AUDIT,
    iw.IX_QUEUE,
    iw.iv.IV_INPUT_FRAME,
    iw.iv.IV_ALLOWED_FEATURES,
    iw.iv.IV_TASK_SEEDS,
    iw.IW_TASK_ELIGIBILITY,
)
OUTPUT_FILES = (
    FEATURE_SCHEMA,
    TRAINING_TASK_REVIEW,
    SAMPLE_WEIGHT_AUDIT,
    TRAINED_MODEL_MANIFEST,
    ONNX_PARITY,
    CLASSIFICATION_SCORECARD,
    PROXY_TRADE_SCORECARD,
    FEATURE_IMPORTANCE,
    RUNTIME_FIREWALL,
    RELEASE_DISPOSITION,
    IY_QUEUE,
    RUN_EVIDENCE_RECEIPT,
    DATA_RECEIPT,
    MODEL_RECEIPT,
    PERFORMANCE_RECEIPT,
    RUNTIME_RECEIPT,
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
    ROOT_CHANGELOG,
    WORKSPACE_CHANGELOG,
    RUN_REGISTRY,
    PROJECT_LEDGER,
    STAGE_LEDGER,
    ARTIFACT_REGISTRY,
    Path(__file__),
)


def now_utc() -> str:
    return datetime.now(tz=UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def io(path: Path) -> Path:
    return aw.io_path(path)


def rel(path: Path | str) -> str:
    return aw.rel(path)


def exists(path: Path) -> bool:
    return io(path).exists()


def ensure_parent(path: Path) -> None:
    io(path.parent).mkdir(parents=True, exist_ok=True)


def read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(io(path), low_memory=False)


def read_json(path: Path) -> Any:
    return json.loads(io(path).read_text(encoding="utf-8-sig"))


def write_csv(path: Path, frame: pd.DataFrame) -> Path:
    ensure_parent(path)
    target = path if len(str(path)) < 240 else io(path)
    frame.to_csv(target, index=False, encoding="utf-8-sig", lineterminator="\n")
    return path


def write_json(path: Path, payload: Any) -> Path:
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


def passed(series: pd.Series) -> bool:
    return series.astype(str).str.lower().isin(["pass", "passed", "true", "1", "yes"]).all()


def safe_model_id(task_id: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9_]+", "_", task_id).strip("_")
    return f"ix_{cleaned}"


def configure_training_engine() -> None:
    source = SimpleNamespace(
        aw=iw.aw,
        STAGE_ID=STAGE_ID,
        STAGE_DIR=STAGE_DIR,
        RUN_ID=iw.RUN_ID,
        FINAL_DECISION=iw.FINAL_DECISION,
        GATE_AUDIT=iw.GATE_AUDIT,
        IP_QUEUE=iw.IX_QUEUE,
        IO_TASK_ELIGIBILITY=iw.IW_TASK_ELIGIBILITY,
        IO_FEATURE_BOUNDARY_REVIEW=iw.IW_FEATURE_BOUNDARY_REVIEW,
        inr=SimpleNamespace(
            IN_INPUT_FRAME=iw.iv.IV_INPUT_FRAME,
            IN_ALLOWED_FEATURES=iw.iv.IV_ALLOWED_FEATURES,
            IN_TASK_SEEDS=iw.iv.IV_TASK_SEEDS,
        ),
    )
    train_base.__file__ = __file__
    train_base.io_review = source
    train_base.aw = aw
    train_base.TODAY = TODAY
    train_base.STAGE_ID = STAGE_ID
    train_base.STAGE_DIR = STAGE_DIR
    train_base.RUN_NUMBER = RUN_NUMBER
    train_base.RUN_ID = RUN_ID
    train_base.PARENT_RUN_ID = PARENT_RUN_ID
    train_base.NEXT_RUN_ID = NEXT_RUN_ID
    train_base.STATUS = STATUS
    train_base.JUDGMENT = JUDGMENT
    train_base.DECISION = DECISION
    train_base.CLAIM_BOUNDARY = CLAIM_BOUNDARY
    train_base.RUN_DIR = RUN_DIR
    train_base.MODEL_DIR = MODEL_DIR
    train_base.ONNX_DIR = ONNX_DIR
    train_base.REVIEW_DIR = REVIEW_DIR
    train_base.REPORT_PATH = REPORT_PATH
    train_base.DECISION_DOC = DECISION_DOC
    train_base.WORKSPACE_STATE = WORKSPACE_STATE
    train_base.CURRENT_WORKING_STATE = CURRENT_WORKING_STATE
    train_base.SELECTION_STATUS = SELECTION_STATUS
    train_base.STAGE_BRIEF = STAGE_BRIEF
    train_base.ROOT_CHANGELOG = ROOT_CHANGELOG
    train_base.WORKSPACE_CHANGELOG = WORKSPACE_CHANGELOG
    train_base.RUN_REGISTRY = RUN_REGISTRY
    train_base.PROJECT_LEDGER = PROJECT_LEDGER
    train_base.STAGE_LEDGER = STAGE_LEDGER
    train_base.ARTIFACT_REGISTRY = ARTIFACT_REGISTRY
    train_base.FEATURE_SCHEMA = FEATURE_SCHEMA
    train_base.TRAINING_TASK_REVIEW = TRAINING_TASK_REVIEW
    train_base.SAMPLE_WEIGHT_AUDIT = SAMPLE_WEIGHT_AUDIT
    train_base.TRAINED_MODEL_MANIFEST = TRAINED_MODEL_MANIFEST
    train_base.ONNX_PARITY = ONNX_PARITY
    train_base.CLASSIFICATION_SCORECARD = CLASSIFICATION_SCORECARD
    train_base.PROXY_TRADE_SCORECARD = PROXY_TRADE_SCORECARD
    train_base.FEATURE_IMPORTANCE = FEATURE_IMPORTANCE
    train_base.RUNTIME_FIREWALL = RUNTIME_FIREWALL
    train_base.RELEASE_DISPOSITION = RELEASE_DISPOSITION
    train_base.IQ_QUEUE = IY_QUEUE
    train_base.RUN_EVIDENCE_RECEIPT = RUN_EVIDENCE_RECEIPT
    train_base.DATA_RECEIPT = DATA_RECEIPT
    train_base.MODEL_RECEIPT = MODEL_RECEIPT
    train_base.PERFORMANCE_RECEIPT = PERFORMANCE_RECEIPT
    train_base.RUNTIME_RECEIPT = RUNTIME_RECEIPT
    train_base.JUDGMENT_RECEIPT = JUDGMENT_RECEIPT
    train_base.CLAIM_RECEIPT = CLAIM_RECEIPT
    train_base.LINEAGE_RECEIPT = LINEAGE_RECEIPT
    train_base.GATE_AUDIT = GATE_AUDIT
    train_base.FINAL_DECISION = FINAL_DECISION
    train_base.RUN_MANIFEST = RUN_MANIFEST
    train_base.FEATURE_SET_ID = FEATURE_SET_ID
    train_base.INPUT_FILES = INPUT_FILES
    train_base.OUTPUT_FILES = OUTPUT_FILES
    train_base.safe_model_id = safe_model_id


def gate_row(gate: str, status: str, evidence: str, effect: str) -> dict[str, Any]:
    return {
        "gate_id": gate,
        "status": status,
        "evidence_path": evidence,
        "effect": effect,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def make_gates(summary: Mapping[str, Any]) -> pd.DataFrame:
    iw_gates = read_csv(iw.GATE_AUDIT)
    return pd.DataFrame(
        [
            gate_row(
                "parent_iw_gates_passed",
                "passed" if passed(iw_gates["status"]) else "failed",
                rel(iw.GATE_AUDIT),
                "IW review(IW 검토) 통과 뒤 학습한다.",
            ),
            gate_row(
                "feature_schema_materialized",
                "passed" if summary["feature_count"] == 58 and exists(FEATURE_SCHEMA) else "failed",
                rel(FEATURE_SCHEMA),
                "ONNX(온엑스) 인계용 feature order(피처 순서)를 고정한다.",
            ),
            gate_row(
                "all_eligible_tasks_trained",
                "passed" if summary["trained_model_rows"] == summary["task_seed_rows"] == 7 else "failed",
                rel(TRAINING_TASK_REVIEW),
                "IW 적격 작업 7개가 모두 학습됐다.",
            ),
            gate_row(
                "onnx_exports_materialized",
                "passed" if summary["onnx_rows"] == summary["trained_model_rows"] else "failed",
                rel(TRAINED_MODEL_MANIFEST),
                "각 모델의 ONNX(온엑스) 산출물이 있다.",
            ),
            gate_row(
                "onnx_parity_passed",
                "passed"
                if summary["onnx_parity_passed_rows"] == summary["onnx_parity_rows"] == summary["trained_model_rows"]
                else "failed",
                rel(ONNX_PARITY),
                "Python/ONNX(파이썬/온엑스) probability parity(확률 동등성)가 통과했다.",
            ),
            gate_row(
                "classification_scored",
                "passed" if summary["classification_rows"] == summary["trained_model_rows"] * 2 else "failed",
                rel(CLASSIFICATION_SCORECARD),
                "inner train/holdout(내부 학습/보류) 분류 진단이 있다.",
            ),
            gate_row(
                "proxy_trade_scored",
                "passed" if summary["proxy_trade_rows"] == summary["trained_model_rows"] * 2 else "failed",
                rel(PROXY_TRADE_SCORECARD),
                "proxy trade(프록시 거래) 점수가 있다.",
            ),
            gate_row(
                "runtime_firewall_active",
                "passed" if exists(RUNTIME_FIREWALL) and exists(RELEASE_DISPOSITION) else "failed",
                f"{rel(RUNTIME_FIREWALL)};{rel(RELEASE_DISPOSITION)}",
                "학습 산출물과 runtime package(런타임 패키지)를 분리한다.",
            ),
            gate_row(
                "next_review_queue_opened",
                "passed" if exists(IY_QUEUE) else "failed",
                rel(IY_QUEUE),
                "IY review(IY 검토)를 학습 뒤 필수 단계로 연다.",
            ),
            gate_row(
                "no_forbidden_operating_claim",
                "passed",
                rel(CLAIM_RECEIPT),
                "선택, MT5 성공, runtime authority(런타임 권위), Goal Achieve(목표 달성)를 주장하지 않는다.",
            ),
            gate_row(
                "required_gate_coverage_audit",
                "passed",
                rel(GATE_AUDIT),
                "gate evidence(게이트 근거)를 closeout(종료 기록)에 연결한다.",
            ),
        ]
    )


def write_review_queue() -> None:
    write_csv(
        IY_QUEUE,
        pd.DataFrame(
            [
                {
                    "next_run_id": NEXT_RUN_ID,
                    "parent_run_id": RUN_ID,
                    "queued_task": "review_positive_low_edge_expansion_training_before_runtime_package(런타임 패키지 전 양수 낮은 엣지 확장 학습 검토)",
                    "trained_model_manifest": rel(TRAINED_MODEL_MANIFEST),
                    "onnx_parity": rel(ONNX_PARITY),
                    "proxy_trade_scorecard": rel(PROXY_TRADE_SCORECARD),
                    "required_review": "proxy usability, ONNX parity, cost/side/PF/drawdown/equity attribution(프록시 활용성, ONNX 동등성, 비용/방향/PF/낙폭/수익곡선 귀속)",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            ]
        ),
    )


def write_receipts(summary: Mapping[str, Any], gates: pd.DataFrame) -> None:
    base = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "created_at_utc": now_utc(),
        "status": STATUS,
        "judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(
        RUN_EVIDENCE_RECEIPT,
        {
            **base,
            "measurement_scope": "inner holdout proxy and ONNX parity only(내부 보류 프록시와 ONNX 동등성 전용)",
            "scoreboard": "structural_scout(구조 스카우트)",
            "parity_level": "P2_model_input_parity_closed(P2 모델 입력 동등성 닫힘)",
            "external_verification_status": "out_of_scope_by_claim(주장 범위 밖)",
            "effect": "후보는 만들지만 MT5 KPI(MT5 핵심 성과 지표)로 해석하지 않는다.",
        },
    )
    write_json(
        DATA_RECEIPT,
        {
            **base,
            "data_source": rel(iw.iv.IV_INPUT_FRAME),
            "time_axis": "UTC closed-bar/as-of inherited from IV(UTC 닫힌 봉/시점 기준, IV 상속)",
            "sample_scope": f"Tier A rows={summary['frame_rows']}; Tier B missing_required(Tier A 행={summary['frame_rows']}, Tier B 필수 누락)",
            "feature_label_boundary": rel(iw.IW_FEATURE_BOUNDARY_REVIEW),
            "split_boundary": "source_row_id ordered 80/20 inner split(source_row_id 순서 80/20 내부 분할)",
            "leakage_risk": "train-only labels and weights are excluded from model features(학습 전용 라벨/가중치는 모델 피처에서 제외)",
            "data_hash_or_identity": {rel(iw.iv.IV_INPUT_FRAME): sha(iw.iv.IV_INPUT_FRAME)},
            "integrity_judgment": "usable_with_boundary(경계 조건부 사용 가능)",
        },
    )
    write_json(
        MODEL_RECEIPT,
        {
            **base,
            "model_family": "LightGBM/XGBoost/ExtraTrees(라이트GBM/엑스지부스트/엑스트라트리스)",
            "trained_model_rows": summary["trained_model_rows"],
            "onnx_rows": summary["onnx_rows"],
            "onnx_parity": f"{summary['onnx_parity_passed_rows']}/{summary['onnx_parity_rows']}",
            "target_and_label": "iv_label_class_cost_stress_fwd18, hx_label_class_fwd6, hx_label_class_fwd18, hx_label_class_fwd24",
            "split_method": "source_row_id ordered inner holdout(source_row_id 순서 내부 보류)",
            "selection_metric": "none; review only(없음, 검토 전용)",
            "secondary_metrics": "balanced_accuracy, macro_f1, proxy net/PF/drawdown(균형 정확도, 매크로 F1, 프록시 순수익/PF/낙폭)",
            "threshold_policy": "argmax only, no threshold tuning(argmax 전용, 임계값 조정 없음)",
            "overfit_risk": "multiple task exploration without WFO(여러 작업 탐색, WFO 없음)",
            "calibration_risk": "probabilities are uncalibrated rank signals(확률은 미보정 순위 신호)",
            "comparison_baseline": rel(iw.FINAL_DECISION),
            "validation_judgment": JUDGMENT,
        },
    )
    write_json(
        PERFORMANCE_RECEIPT,
        {
            **base,
            "observed_change": "positive low-edge cost-stress expansion candidates trained(양수 낮은 엣지 비용 압박 확장 후보 학습)",
            "comparison_baseline": rel(iw.FINAL_DECISION),
            "best_inner_holdout_proxy_net": summary["best_inner_holdout_proxy_net"],
            "best_inner_holdout_profit_factor": summary["best_inner_holdout_profit_factor"],
            "positive_inner_holdout_proxy_rows": summary["positive_inner_holdout_proxy_rows"],
            "segment_checks": "direction, density, drawdown proxy only(방향, 밀도, 낙폭 프록시 전용)",
            "trade_shape": rel(PROXY_TRADE_SCORECARD),
            "alternative_explanations": "proxy may not survive MT5 lifecycle/cost(프록시는 MT5 생명주기/비용에서 사라질 수 있음)",
            "attribution_confidence": "low_until_IY_review_and_MT5_probe(IY 검토와 MT5 탐침 전까지 낮음)",
            "next_probe": NEXT_RUN_ID,
        },
    )
    write_json(
        RUNTIME_RECEIPT,
        {
            **base,
            "research_path": rel(Path(__file__)),
            "runtime_path": "not_created(미생성)",
            "shared_contract": rel(FEATURE_SCHEMA),
            "known_differences": "no MT5 package or tester run(MT5 패키지 또는 테스터 실행 없음)",
            "parity_check": rel(ONNX_PARITY),
            "parity_identity": f"{summary['onnx_parity_passed_rows']}/{summary['onnx_parity_rows']}",
            "runtime_claim_boundary": "research-only(연구 전용)",
        },
    )
    write_json(
        JUDGMENT_RECEIPT,
        {
            **base,
            "result_subject": RUN_ID,
            "evidence_available": [rel(TRAINED_MODEL_MANIFEST), rel(ONNX_PARITY), rel(PROXY_TRADE_SCORECARD), rel(GATE_AUDIT)],
            "evidence_missing": "IY review, runtime package, MT5 runtime probe(IY 검토, 런타임 패키지, MT5 런타임 탐침)",
            "judgment_label": JUDGMENT,
            "next_condition": NEXT_RUN_ID,
            "user_explanation_hook": "후보는 학습됐지만 운영 모델은 아니다.",
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            **base,
            "candidate_selection": "not_run",
            "mt5_execution": "not_run",
            "forward_passed": "not_claimed",
            "forward_failed": "not_claimed",
            "runtime_authority": "not_claimed",
            "operating_promotion": "not_claimed",
            "goal_achieve": "not_claimed",
        },
    )
    write_json(
        LINEAGE_RECEIPT,
        {
            **base,
            "source_inputs": [rel(path) for path in INPUT_FILES],
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [rel(path) for path in artifact_paths() if exists(path)],
            "artifact_hashes": {rel(path): sha(path) for path in artifact_paths() if exists(path) and io(path).is_file()},
            "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "availability": "generated_with_manifest(목록과 함께 생성)",
            "lineage_judgment": "connected_with_boundary(경계 조건부 연결)",
        },
    )


def write_final(summary: Mapping[str, Any], gates: pd.DataFrame) -> dict[str, Any]:
    final = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_action": NEXT_RUN_ID,
        "candidate_selection": "not_run",
        "mt5_runtime_probe": "not_run",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "gate_passes": int(gates["status"].astype(str).eq("passed").sum()),
        "gate_total": int(len(gates)),
        "claim_boundary": CLAIM_BOUNDARY,
        **dict(summary),
    }
    write_json(FINAL_DECISION, final)
    return final


def write_manifest() -> None:
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "created_at": TODAY,
            "created_at_utc": now_utc(),
            "script": rel(Path(__file__)),
            "inputs": [rel(path) for path in INPUT_FILES],
            "outputs": [rel(path) for path in OUTPUT_FILES if exists(path)],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def write_docs(final: Mapping[str, Any]) -> None:
    report = f"""# run337IX Positive Low-Edge Expansion Candidate Training(run337IX 양수 낮은 엣지 확장 후보 학습)

## Summary(요약)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- judgment(판정): `{JUDGMENT}`
- gates(게이트): `{final['gate_passes']}/{final['gate_total']}`
- trained_model_rows(학습 모델 수): `{final['trained_model_rows']}`
- onnx_parity(ONNX 동등성): `{final['onnx_parity_passed_rows']}/{final['onnx_parity_rows']}`
- best_inner_holdout_proxy_net(최고 내부 보류 프록시 순수익): `{final['best_inner_holdout_proxy_net']}`
- best_inner_holdout_profit_factor(최고 내부 보류 수익 팩터): `{final['best_inner_holdout_profit_factor']}`
- positive_inner_holdout_proxy_rows(내부 보류 프록시 양성 행): `{final['positive_inner_holdout_proxy_rows']}`

## Action(행동)

IW review(IW 검토)에서 적격 판정된 7개 task seed(작업 씨앗)를 학습하고 ONNX(온엑스) 산출물과 proxy scorecard(프록시 점수표)를 만들었다.
Effect(효과): IY review(IY 검토)가 proxy usability(프록시 활용성), ONNX parity(ONNX 동등성), cost/side/PF/drawdown/equity(비용/방향/PF/낙폭/수익곡선)를 함께 볼 수 있다.

## Boundary(경계)

No candidate selection(후보 선택 없음), no MT5 execution(MT5 실행 없음), no Forward Passed/Failed(전진 통과/실패 없음), no runtime authority(런타임 권위 없음), no Goal Achieve(목표 달성 없음).

## Next(다음)

`{NEXT_RUN_ID}`에서 학습 산출물을 검토한다.
"""
    decision = f"""# {TODAY} Stage337IX Decision(337IX 결정)

- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- evidence(근거): `{rel(TRAINED_MODEL_MANIFEST)}`, `{rel(ONNX_PARITY)}`, `{rel(PROXY_TRADE_SCORECARD)}`

Action(행동): positive low-edge cost-stress expansion candidate(양수 낮은 엣지 비용 압박 확장 후보)를 학습했다.
Effect(효과): 다음 IY review(IY 검토)가 proxy KPI(프록시 핵심 성과 지표)를 MT5 KPI(MT5 핵심 성과 지표)로 착각하지 않게 분리한다.

claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    current = f"""# Current Working State(현재 작업 상태)

## Current Truth(현재 진실)

- active_stage(현재 단계): `{STAGE_ID}`
- latest_completed_run(최근 완료 실행): `{RUN_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`

## Effect(효과)

IX training(IX 학습)은 ONNX(온엑스) 후보와 proxy score(프록시 점수)를 만들었다.
효과는 IY review(IY 검토)가 학습 산출물을 runtime package(런타임 패키지)로 넘길지 좁게 판단하게 하는 것이다.

## Claim Boundary(주장 경계)

`{CLAIM_BOUNDARY}`
"""
    selection = f"""# Stage337 Selection Status(337단계 선택 상태)

- latest_run(최신 실행): `{RUN_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- selected_model(선정 모델): `none(없음)`
- trained_model_rows(학습 모델 수): `{final['trained_model_rows']}`
- ONNX parity(ONNX 동등성): `{final['onnx_parity_passed_rows']}/{final['onnx_parity_rows']}`
- best_inner_holdout_proxy_net(최고 내부 보류 프록시 순수익): `{final['best_inner_holdout_proxy_net']}`
- candidate_selection(후보 선택): `not_run(미실행)`
- MT5 execution(MT5 실행): `not_run(미실행)`
- runtime_authority(런타임 권위): `not_claimed(주장 안 함)`
- operating_promotion(운영 승격): `not_claimed(주장 안 함)`
- goal_achieve(목표 달성): `not_claimed(주장 안 함)`

Effect(효과): 학습 산출물을 운영 모델로 오해하지 않게 한다.
"""
    workspace = f"""current_stage_id: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {STATUS}
current_judgment: {JUDGMENT}
current_decision: {DECISION}
next_run_id: {NEXT_RUN_ID}
claim_boundary: {CLAIM_BOUNDARY}
updated_at: {TODAY}
"""
    write_bom_text(REPORT_PATH, report)
    write_bom_text(DECISION_DOC, decision)
    write_bom_text(CURRENT_WORKING_STATE, current)
    write_bom_text(SELECTION_STATUS, selection)
    write_bom_text(WORKSPACE_STATE, workspace)
    marker = f"run337IX {RUN_ID}"
    append_text_once(
        STAGE_BRIEF,
        marker,
        f"""## run337IX Positive Low-Edge Expansion Candidate Training(양수 낮은 엣지 확장 후보 학습)

- run_id(실행 ID): `{RUN_ID}`
- judgment(판정): `{JUDGMENT}`
- next(다음): `{NEXT_RUN_ID}`
- effect(효과): 7개 ONNX(온엑스) 후보를 만들고 parity(동등성) `{final['onnx_parity_passed_rows']}/{final['onnx_parity_rows']}`를 기록했다.
""",
    )
    changelog_entry = f"""## {TODAY} run337IX Positive Low-Edge Expansion Candidate Training(양수 낮은 엣지 확장 후보 학습)

- action(행동): IW 적격 task seed(작업 씨앗) 7개를 학습하고 ONNX(온엑스) 후보를 만들었다.
- effect(효과): IY review(IY 검토)가 proxy(프록시), parity(동등성), trade shape(거래 형태)를 함께 검토할 수 있게 했다.
- boundary(경계): candidate selection(후보 선택), MT5 execution(MT5 실행), Goal Achieve(목표 달성)는 없다.
"""
    append_text_once(ROOT_CHANGELOG, marker, changelog_entry)
    append_text_once(WORKSPACE_CHANGELOG, marker, changelog_entry)


def append_text_once(path: Path, marker: str, text: str) -> None:
    current = io(path).read_text(encoding="utf-8-sig") if exists(path) else ""
    if marker in current:
        return
    next_text = (current.rstrip() + "\n\n" + text.strip() + "\n") if current.strip() else text.strip() + "\n"
    write_bom_text(path, next_text)


def append_or_replace_csv(path: Path, key_columns: Iterable[str], row: Mapping[str, Any]) -> None:
    frame = read_csv(path) if exists(path) else pd.DataFrame()
    if frame.empty:
        frame = pd.DataFrame(columns=list(row.keys()))
    for column in row:
        if column not in frame.columns:
            frame[column] = ""
    mask = pd.Series(True, index=frame.index)
    for key in key_columns:
        if key in frame.columns:
            mask = mask & frame[key].astype(str).eq(str(row[key]))
        else:
            mask = mask & False
    frame = frame.loc[~mask].copy()
    frame = pd.concat([frame, pd.DataFrame([row])], ignore_index=True)
    ordered = list(dict.fromkeys(list(frame.columns) + list(row.keys())))
    write_csv(path, frame[ordered])


def update_registers(final: Mapping[str, Any]) -> None:
    base = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "run_date": TODAY,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_run_id": NEXT_RUN_ID,
        "primary_artifact": rel(FINAL_DECISION),
        "report_path": rel(REPORT_PATH),
        "claim_boundary": CLAIM_BOUNDARY,
    }
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], base)
    rows = [
        {
            **base,
            "view": "Tier A separate(Tier A 분리)",
            "tier": "Tier A",
            "metric_scope": "candidate_training_inner_holdout_proxy",
            "trained_model_rows": final["trained_model_rows"],
            "onnx_parity": f"{final['onnx_parity_passed_rows']}/{final['onnx_parity_rows']}",
            "best_inner_holdout_proxy_net": final["best_inner_holdout_proxy_net"],
            "best_inner_holdout_profit_factor": final["best_inner_holdout_profit_factor"],
            "result_status": "trained_review_required_no_selection",
        },
        {
            **base,
            "view": "Tier B separate(Tier B 분리)",
            "tier": "Tier B",
            "metric_scope": "missing_required",
            "result_status": "missing_required",
        },
        {
            **base,
            "view": "Tier A+B combined(Tier A+B 합산)",
            "tier": "Tier A+B",
            "metric_scope": "missing_required",
            "result_status": "missing_required",
        },
    ]
    for row in rows:
        append_or_replace_csv(PROJECT_LEDGER, ["run_id", "view"], row)
        append_or_replace_csv(STAGE_LEDGER, ["run_id", "view"], row)


def artifact_paths() -> list[Path]:
    return list(OUTPUT_FILES)


def update_artifact_registry(paths: Sequence[Path]) -> None:
    registry = read_csv(ARTIFACT_REGISTRY) if exists(ARTIFACT_REGISTRY) else pd.DataFrame()
    required = ["stage_id", "run_id", "artifact_type", "path", "sha256", "created_at", "claim_boundary"]
    for column in required:
        if column not in registry.columns:
            registry[column] = ""
    rows = []
    for path in paths:
        if exists(path) and io(path).is_file():
            rows.append(
                {
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "artifact_type": "report" if path.suffix.lower() == ".md" else path.suffix.lower().lstrip("."),
                    "path": rel(path),
                    "sha256": sha(path),
                    "created_at": TODAY,
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    if rows:
        new_paths = {row["path"] for row in rows}
        registry = registry.loc[~registry["path"].astype(str).isin(new_paths)].copy()
        registry = pd.concat([registry, pd.DataFrame(rows)], ignore_index=True)
        columns = list(dict.fromkeys(required + list(registry.columns)))
        write_csv(ARTIFACT_REGISTRY, registry[columns])


def main() -> None:
    configure_training_engine()
    for path in (RUN_DIR, MODEL_DIR, ONNX_DIR, REVIEW_DIR, DECISION_DOC.parent):
        io(path).mkdir(parents=True, exist_ok=True)
    missing = [rel(path) for path in INPUT_FILES if not exists(path)]
    if missing:
        raise FileNotFoundError(f"missing required input files: {missing}")
    summary = train_base.train_all()
    write_review_queue()
    gates = make_gates(summary)
    write_csv(GATE_AUDIT, gates)
    write_receipts(summary, gates)
    final = write_final(summary, gates)
    write_docs(final)
    write_manifest()
    update_registers(final)
    update_artifact_registry(artifact_paths())
    failed = gates.loc[~gates["status"].astype(str).eq("passed")]
    if not failed.empty:
        raise RuntimeError(f"IX gates failed: {failed[['gate_id', 'status']].to_dict(orient='records')}")
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "trained_model_rows": final["trained_model_rows"],
                "onnx_parity": f"{final['onnx_parity_passed_rows']}/{final['onnx_parity_rows']}",
                "best_inner_holdout_proxy_net": final["best_inner_holdout_proxy_net"],
                "best_inner_holdout_profit_factor": final["best_inner_holdout_profit_factor"],
                "positive_inner_holdout_proxy_rows": final["positive_inner_holdout_proxy_rows"],
                "gates": f"{final['gate_passes']}/{final['gate_total']}",
                "next_action": NEXT_RUN_ID,
                "goal_achieve": "not_claimed",
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
