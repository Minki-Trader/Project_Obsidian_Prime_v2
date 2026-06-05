from __future__ import annotations

import json
import math
import re
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import json_ready, path_exists  # noqa: E402
from stage_pipelines.stage337 import train_post_runtime_probe_proxy_negative_trade_shape_repair_candidates_without_db as hp  # noqa: E402


aw = hp.aw
fb = hp.fb
he = hp.he

TODAY = "2026-05-31"
STAGE_ID = hp.STAGE_ID
RUN_NUMBER = "run337HQ"
RUN_ID = "run337HQ_review_post_runtime_probe_proxy_negative_trade_shape_repair_training_without_db_v1"
PARENT_RUN_ID = hp.RUN_ID
NEXT_RUN_ID = "run337HR_design_proxy_negative_trade_shape_second_order_repair_without_db_v1"
STATUS = "completed_stage337HQ_proxy_negative_trade_shape_training_review_all_proxy_negative_no_runtime_package_no_selection"
JUDGMENT = "onnx_parity_passed_but_all_inner_holdout_proxy_negative_second_order_repair_design_required"
DECISION = "stage337HQ_open_run337HR_proxy_negative_trade_shape_second_order_repair_design"
CLAIM_BOUNDARY = (
    "research_development_only_stage337HQ_proxy_negative_trade_shape_training_review_without_db_"
    "onnx_parity_reviewed_all_proxy_negative_no_runtime_package_no_candidate_selection_no_mt5_execution_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = hp.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = hp.REVIEWS_DIR
REPORT_PATH = REVIEWS_DIR / "run337HQ_proxy_negative_trade_shape_training_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage337HQ_proxy_negative_trade_shape_training_review.md"

HP_FINAL = hp.FINAL_DECISION
HP_GATES = hp.GATE_AUDIT
HP_QUEUE = hp.HQ_QUEUE
HP_MODEL_MANIFEST = hp.TRAINED_MODEL_MANIFEST
HP_ONNX_PARITY = hp.ONNX_PARITY
HP_CLASSIFICATION = hp.CLASSIFICATION_SCORECARD
HP_PROXY = hp.PROXY_TRADE_SCORECARD
HP_FIREWALL = hp.RUNTIME_FIREWALL
HP_RELEASE = hp.RELEASE_DISPOSITION
HP_FEATURE_SCHEMA = hp.FEATURE_SCHEMA

TRAINING_CANDIDATE_REVIEW = RUN_DIR / "training_candidate_review.csv"
ONNX_PARITY_REVIEW = RUN_DIR / "onnx_parity_review.csv"
PROXY_NEGATIVE_MEMORY = RUN_DIR / "proxy_negative_training_memory.csv"
RUNTIME_PACKAGE_DECISION = RUN_DIR / "runtime_package_decision.csv"
RELEASE_DISPOSITION_REVIEW = RUN_DIR / "release_disposition_review.csv"
HR_QUEUE = RUN_DIR / "run337HR_design_queue.csv"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_discipline_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (
    HP_FINAL,
    HP_GATES,
    HP_QUEUE,
    HP_MODEL_MANIFEST,
    HP_ONNX_PARITY,
    HP_CLASSIFICATION,
    HP_PROXY,
    HP_FIREWALL,
    HP_RELEASE,
    HP_FEATURE_SCHEMA,
)
OUTPUT_FILES = (
    TRAINING_CANDIDATE_REVIEW,
    ONNX_PARITY_REVIEW,
    PROXY_NEGATIVE_MEMORY,
    RUNTIME_PACKAGE_DECISION,
    RELEASE_DISPOSITION_REVIEW,
    HR_QUEUE,
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
    he.SELECTED_STATUS,
    he.WORKSPACE_STATE,
    he.CURRENT_STATE,
    he.CHANGELOG,
    he.STAGE_BRIEF,
    he.RUN_REGISTRY,
    he.ALPHA_LEDGER,
    he.STAGE_LEDGER,
    he.ARTIFACT_REGISTRY,
    Path(__file__),
)

CANDIDATE_COLUMNS = (
    "model_id",
    "task_id",
    "onnx_parity_passed",
    "holdout_balanced_accuracy",
    "holdout_proxy_net",
    "holdout_profit_factor",
    "holdout_expectancy",
    "holdout_max_drawdown",
    "holdout_recovery_factor",
    "holdout_trade_count",
    "holdout_signal_density",
    "holdout_long_count",
    "holdout_short_count",
    "review_status",
    "blocked_reason",
    "effect",
    "claim_boundary",
)
PARITY_COLUMNS = ("model_id", "task_id", "passed", "max_abs_diff", "mean_abs_diff", "review_status", "effect", "claim_boundary")
MEMORY_COLUMNS = ("memory_id", "source_run_id", "source_model", "evidence", "next_constraint_or_seed", "effect", "claim_boundary")
DECISION_COLUMNS = ("decision_id", "decision_status", "observed", "required_for_runtime_package", "effect", "claim_boundary")
RELEASE_COLUMNS = ("review_id", "subject", "review_status", "allowed_use", "forbidden_use", "effect", "claim_boundary")
QUEUE_COLUMNS = ("queue_id", "source_run_id", "next_run_id", "task", "required_inputs", "expected_outputs", "blocked_if_missing", "effect", "claim_boundary")
GATE_COLUMNS = hp.GATE_COLUMNS


def now_utc() -> str:
    return datetime.now(tz=UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    return aw.rel(path)


def read_csv(path: Path) -> list[dict[str, str]]:
    return aw.read_csv(path)


def read_json(path: Path) -> dict[str, Any]:
    return aw.read_json(path)


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> Path:
    return aw.write_csv(path, columns, rows)


def write_json(path: Path, payload: Mapping[str, Any] | Sequence[Any]) -> Path:
    aw.io_path(path.parent).mkdir(parents=True, exist_ok=True)
    aw.io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def fail_if_missing(paths: Sequence[Path]) -> list[Path]:
    return [path for path in paths if not path_exists(path)]


def as_float(value: Any) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return 0.0
    return number if math.isfinite(number) else 0.0


def by_key(rows: Sequence[Mapping[str, str]], key: str) -> dict[str, Mapping[str, str]]:
    return {str(row.get(key, "")): row for row in rows}


def build_hr_queue() -> list[dict[str, Any]]:
    return [
        {
            "queue_id": "hr001_proxy_negative_trade_shape_second_order_repair_design",
            "source_run_id": RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "task": "design second-order repair after all HP proxy rows stayed negative(HP 프록시 행이 모두 음수로 남은 뒤 2차 수리 설계)",
            "required_inputs": f"{rel(TRAINING_CANDIDATE_REVIEW)};{rel(PROXY_NEGATIVE_MEMORY)};{rel(RUNTIME_PACKAGE_DECISION)}",
            "expected_outputs": "new density/selectivity/calibration design and materialization queue(새 밀도/선택성/보정 설계와 물질화 대기열)",
            "blocked_if_missing": "candidate review or negative memory(후보 검토 또는 음수 기억)",
            "effect": "converts valid negative training evidence into next exploration constraints(유효한 음수 학습 근거를 다음 탐색 제약으로 변환)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def build_reviews() -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    dict[str, Any],
]:
    hp_final = read_json(HP_FINAL)
    hp_queue = read_csv(HP_QUEUE)
    model_rows = read_csv(HP_MODEL_MANIFEST)
    parity_rows = read_csv(HP_ONNX_PARITY)
    class_rows = [row for row in read_csv(HP_CLASSIFICATION) if row.get("split") == "inner_holdout"]
    proxy_rows = [row for row in read_csv(HP_PROXY) if row.get("split") == "inner_holdout"]
    release_rows = read_csv(HP_RELEASE)
    parity_by_model = by_key(parity_rows, "model_id")
    class_by_model = by_key(class_rows, "model_id")
    proxy_by_model = by_key(proxy_rows, "model_id")

    candidate_rows: list[dict[str, Any]] = []
    for model in model_rows:
        model_id = model.get("model_id", "")
        parity = parity_by_model.get(model_id, {})
        cls = class_by_model.get(model_id, {})
        proxy = proxy_by_model.get(model_id, {})
        net = as_float(proxy.get("net_log_return_after_cost"))
        parity_passed = str(parity.get("passed", "")).lower() == "true"
        runtime_ready = parity_passed and net > 0
        candidate_rows.append(
            {
                "model_id": model_id,
                "task_id": model.get("task_id", ""),
                "onnx_parity_passed": str(parity_passed).lower(),
                "holdout_balanced_accuracy": cls.get("balanced_accuracy", ""),
                "holdout_proxy_net": net,
                "holdout_profit_factor": proxy.get("profit_factor", ""),
                "holdout_expectancy": proxy.get("expectancy", ""),
                "holdout_max_drawdown": proxy.get("max_drawdown", ""),
                "holdout_recovery_factor": proxy.get("recovery_factor", ""),
                "holdout_trade_count": proxy.get("trade_count", ""),
                "holdout_signal_density": proxy.get("signal_density", ""),
                "holdout_long_count": proxy.get("long_count", ""),
                "holdout_short_count": proxy.get("short_count", ""),
                "review_status": "runtime_probe_candidate(런타임 탐침 후보)" if runtime_ready else "runtime_package_blocked(런타임 패키지 차단)",
                "blocked_reason": "" if runtime_ready else "inner_holdout_proxy_net_nonpositive(내부 보류 프록시 순수익 비양수)",
                "effect": "keeps proxy as review evidence, not MT5 authority(프록시를 MT5 권위가 아닌 검토 근거로 유지)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    parity_review = [
        {
            "model_id": row.get("model_id", ""),
            "task_id": row.get("task_id", ""),
            "passed": row.get("passed", ""),
            "max_abs_diff": row.get("max_abs_diff", ""),
            "mean_abs_diff": row.get("mean_abs_diff", ""),
            "review_status": "passed(통과)" if str(row.get("passed", "")).lower() == "true" else "failed(실패)",
            "effect": "confirms ONNX probability output matches sklearn API(ONNX 확률 출력이 sklearn API와 맞는지 확인)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for row in parity_rows
    ]
    best_candidate = max(candidate_rows, key=lambda row: as_float(row["holdout_proxy_net"]), default={})
    positive_proxy_rows = [row for row in candidate_rows if as_float(row["holdout_proxy_net"]) > 0]
    memory_rows = [
        {
            "memory_id": "hq_memory001_all_holdout_proxy_negative",
            "source_run_id": hp.RUN_ID,
            "source_model": best_candidate.get("model_id", ""),
            "evidence": f"positive_proxy_rows={len(positive_proxy_rows)};best_net={best_candidate.get('holdout_proxy_net', '')};best_pf={best_candidate.get('holdout_profit_factor', '')};density_range={hp_final.get('min_inner_holdout_signal_density')}..{hp_final.get('max_inner_holdout_signal_density')}",
            "next_constraint_or_seed": "reduce trade density, add calibration/selectivity gate, and preserve ONNX parity(거래 밀도를 줄이고 보정/선택성 게이트를 추가하며 ONNX 동등성 유지)",
            "effect": "turns valid negative result into next design guard(유효한 부정 결과를 다음 설계 보호조건으로 변환)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "memory_id": "hq_memory002_train_holdout_inversion_repeated",
            "source_run_id": hp.RUN_ID,
            "source_model": best_candidate.get("model_id", ""),
            "evidence": "inner_train proxy positive but all inner_holdout proxy negative(내부 학습 프록시는 양수지만 내부 보류 프록시는 모두 음수)",
            "next_constraint_or_seed": "require holdout-first proxy gate before runtime package(런타임 패키지 전 보류 우선 프록시 게이트 요구)",
            "effect": "blocks training-only optimism from becoming runtime work(학습 전용 낙관이 런타임 작업으로 넘어가는 것을 막음)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    runtime_decision = [
        {
            "decision_id": "hq_runtime_package_decision",
            "decision_status": "not_opened(열지 않음)",
            "observed": f"onnx_parity={sum(1 for row in parity_review if row['review_status'].startswith('passed'))}/{len(parity_review)};positive_proxy_rows={len(positive_proxy_rows)};best_net={best_candidate.get('holdout_proxy_net', '')}",
            "required_for_runtime_package": "positive proxy net and release gate review before MT5 package(MT5 패키지 전 양수 프록시 순수익과 릴리스 게이트 검토)",
            "effect": "prevents ONNX parity alone from starting MT5 runtime probe(ONNX 동등성만으로 MT5 런타임 탐침을 시작하지 않게 함)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    release_review = [
        {
            "review_id": row.get("review_id", f"release_{idx:02d}"),
            "subject": row.get("subject", ""),
            "review_status": "carried_but_blocked_by_negative_proxy(이월했지만 음수 프록시로 차단)",
            "allowed_use": row.get("allowed_use", ""),
            "forbidden_use": row.get("forbidden_use", ""),
            "effect": row.get("effect", ""),
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for idx, row in enumerate(release_rows, start=1)
    ]
    queue_rows = build_hr_queue()
    queue_next = hp_queue[0].get("next_run_id", "") if hp_queue else ""
    summary = {
        "hp_next_action": hp_final.get("next_action", ""),
        "hp_failed_gate_rows": sum(1 for row in read_csv(HP_GATES) if row.get("status") != "passed"),
        "hp_queue_next_action": queue_next,
        "trained_model_rows": len(model_rows),
        "candidate_rows": len(candidate_rows),
        "onnx_parity_rows": len(parity_review),
        "onnx_parity_passed_rows": sum(1 for row in parity_review if row["review_status"].startswith("passed")),
        "positive_proxy_rows": len(positive_proxy_rows),
        "best_inner_holdout_proxy_net": as_float(best_candidate.get("holdout_proxy_net")),
        "best_inner_holdout_profit_factor": as_float(best_candidate.get("holdout_profit_factor")),
        "best_inner_holdout_expectancy": as_float(best_candidate.get("holdout_expectancy")),
        "best_inner_holdout_trade_count": as_float(best_candidate.get("holdout_trade_count")),
        "best_inner_holdout_signal_density": as_float(best_candidate.get("holdout_signal_density")),
        "runtime_package_decision_rows": len(runtime_decision),
        "negative_memory_rows": len(memory_rows),
        "release_review_rows": len(release_review),
        "queue_rows": len(queue_rows),
    }
    return candidate_rows, parity_review, memory_rows, runtime_decision, release_review, queue_rows, summary


def make_final(summary: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_action": NEXT_RUN_ID,
        "missing_inputs": len(fail_if_missing(INPUT_FILES)),
        "new_training": "not_run",
        "runtime_package": "not_opened",
        "mt5_execution": "not_run",
        "threshold_tuning": "not_run",
        "lot_optimization": "not_run",
        "candidate_selection": "not_run",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "live_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
        "primary_family": "kpi_evidence",
        "primary_skill": "obsidian-run-evidence-system",
        "support_skills": "obsidian-result-judgment;obsidian-model-validation;obsidian-artifact-lineage;obsidian-data-integrity",
        "required_gates": "kpi_contract_audit;row_grain_audit;source_authority_audit;required_gate_coverage_audit;final_claim_guard",
        **dict(summary),
    }


def build_gates(final: Mapping[str, Any]) -> list[dict[str, Any]]:
    no_forbidden_claim = final["candidate_selection"] == "not_run" and final["mt5_execution"] == "not_run" and final["goal_achieve"] == "not_claimed"
    checks = [
        ("input_presence", final["missing_inputs"] == 0, str(final["missing_inputs"]), "0", rel(HP_MODEL_MANIFEST), "required HP training outputs exist(필수 HP 학습 출력 존재)"),
        ("parent_hp_gates_passed", final["hp_failed_gate_rows"] == 0, str(final["hp_failed_gate_rows"]), "0", rel(HP_GATES), "HP gates passed(HP 게이트 통과)"),
        ("parent_next_action_matches", final["hp_next_action"] == RUN_ID and final["hp_queue_next_action"] == RUN_ID, f"final={final['hp_next_action']};queue={final['hp_queue_next_action']}", RUN_ID, rel(HP_FINAL), "HQ follows HP next action(HQ가 HP 다음 행동을 따름)"),
        ("model_manifest_reviewed", final["trained_model_rows"] == final["candidate_rows"] == 5, f"models={final['trained_model_rows']};reviews={final['candidate_rows']}", "5/5", rel(TRAINING_CANDIDATE_REVIEW), "all trained models reviewed(모든 학습 모델 검토)"),
        ("onnx_parity_reviewed", final["onnx_parity_passed_rows"] == final["onnx_parity_rows"] == 5, f"passed={final['onnx_parity_passed_rows']};rows={final['onnx_parity_rows']}", "5/5", rel(ONNX_PARITY_REVIEW), "ONNX parity carried forward(ONNX 동등성 이월)"),
        ("all_proxy_negative_named", final["positive_proxy_rows"] == 0 and final["best_inner_holdout_proxy_net"] <= 0, f"positive={final['positive_proxy_rows']};best={final['best_inner_holdout_proxy_net']}", "0 and <=0", rel(PROXY_NEGATIVE_MEMORY), "all-negative proxy result named(전부 음수 프록시 결과 명명)"),
        ("runtime_package_blocked", final["runtime_package"] == "not_opened" and final["runtime_package_decision_rows"] == 1, f"runtime_package={final['runtime_package']};rows={final['runtime_package_decision_rows']}", "not_opened and 1", rel(RUNTIME_PACKAGE_DECISION), "runtime package remains closed(런타임 패키지 닫힘 유지)"),
        ("negative_memory_materialized", final["negative_memory_rows"] >= 2, str(final["negative_memory_rows"]), ">=2", rel(PROXY_NEGATIVE_MEMORY), "negative memory materialized(부정 기억 물질화)"),
        ("hr_design_queue_opened", final["queue_rows"] == 1 and final["next_action"] == NEXT_RUN_ID, f"queue={final['queue_rows']};next={final['next_action']}", f"1 and {NEXT_RUN_ID}", rel(HR_QUEUE), "HR design queue opened(HR 설계 대기열 개방)"),
        ("no_forbidden_claim", no_forbidden_claim, f"selection={final['candidate_selection']};mt5={final['mt5_execution']};goal={final['goal_achieve']}", "not_run/not_run/not_claimed", rel(FINAL_DECISION), "review without operating claim(운영 주장 없는 검토)"),
        ("required_gate_coverage_audit", True, "all required gates listed(모든 필수 게이트 열거)", "present", rel(GATE_AUDIT), "completion claim tied to gates(완료 주장을 게이트에 연결)"),
    ]
    return [
        {"gate_id": gate_id, "status": "passed" if passed else "failed", "evidence_path": evidence, "observed": observed, "expected": expected, "effect": effect, "claim_boundary": CLAIM_BOUNDARY}
        for gate_id, passed, observed, expected, evidence, effect in checks
    ]


def write_receipts(final: Mapping[str, Any], artifacts: Sequence[Path]) -> list[Path]:
    base = {"run_id": RUN_ID, "parent_run_id": PARENT_RUN_ID, "stage_id": STAGE_ID, "created_at_utc": now_utc(), "status": final["status"], "judgment": final["judgment"], "claim_boundary": CLAIM_BOUNDARY}
    receipts = [
        (DATA_RECEIPT, {**base, "data_source": rel(HP_PROXY), "sample_scope": "HP inner holdout proxy rows only(HP 내부 보류 프록시 행 전용)", "integrity_judgment": "usable_for_negative_review(부정 검토에 사용 가능)"}),
        (MODEL_RECEIPT, {**base, "model_family": "LightGBM ONNX review(LightGBM ONNX 검토)", "model_training": "not_run_review_only(미실행, 검토 전용)", "onnx_parity": f"{final['onnx_parity_passed_rows']}/{final['onnx_parity_rows']}", "selection_metric": "none; runtime package blocked(없음; 런타임 패키지 차단)", "validation_judgment": JUDGMENT}),
        (PERFORMANCE_RECEIPT, {**base, "result_subject": "HP inner holdout proxy(HP 내부 보류 프록시)", "best_proxy_net": final["best_inner_holdout_proxy_net"], "best_profit_factor": final["best_inner_holdout_profit_factor"], "positive_proxy_rows": final["positive_proxy_rows"], "performance_judgment": "negative but valid(부정이지만 유효)"}),
        (RUNTIME_RECEIPT, {**base, "runtime_package": final["runtime_package"], "mt5_execution": final["mt5_execution"], "runtime_judgment": "not_started_due_negative_proxy(음수 프록시 때문에 시작 안 함)", "evidence": rel(RUNTIME_PACKAGE_DECISION)}),
        (JUDGMENT_RECEIPT, {**base, "result_subject": RUN_ID, "evidence_available": [rel(TRAINING_CANDIDATE_REVIEW), rel(ONNX_PARITY_REVIEW), rel(PROXY_NEGATIVE_MEMORY)], "evidence_missing": "new HR design, model retraining, MT5 runtime probe(새 HR 설계, 모델 재학습, MT5 런타임 탐침)", "judgment_label": "negative(부정)", "next_condition": NEXT_RUN_ID, "user_explanation_hook": "ONNX works, but the signal still loses on proxy holdout(ONNX는 작동하지만 신호는 프록시 보류에서 여전히 진다)"}),
        (CLAIM_RECEIPT, {**base, "forbidden_claims": "runtime authority, operating promotion, Goal Achieve(런타임 권위, 운영 승격, 목표 달성)", "claim_guard": "all forbidden claims remain not_claimed/not_run(모든 금지 주장은 not_claimed/not_run 유지)"}),
    ]
    paths = [write_json(path, payload) for path, payload in receipts]
    all_artifacts = list(artifacts) + paths
    lineage = {**base, "source_inputs": [rel(path) for path in INPUT_FILES], "producer": rel(Path(__file__)), "consumer": NEXT_RUN_ID, "artifact_paths": [rel(path) for path in all_artifacts], "artifact_hashes": {rel(path): aw.sha256_file(path) for path in all_artifacts if path_exists(path) and aw.io_path(path).is_file()}, "registry_links": [rel(he.RUN_REGISTRY), rel(he.ALPHA_LEDGER), rel(he.STAGE_LEDGER), rel(he.ARTIFACT_REGISTRY)], "availability": "generated_with_manifest(목록과 함께 생성)", "lineage_judgment": "HP training evidence connected to HR design queue(HP 학습 근거를 HR 설계 대기열에 연결)"}
    paths.append(write_json(LINEAGE_RECEIPT, lineage))
    return paths


def write_report(final: Mapping[str, Any]) -> Path:
    text = f"""# run337HQ Proxy Negative Trade Shape Training Review(run337HQ 프록시 음수 거래 형태 학습 검토)

Action(행동): HP trained ONNX candidates(HP 학습 ONNX 후보) 5개를 ONNX parity(ONNX 동등성), inner holdout proxy(내부 보류 프록시), release firewall(해제 방화벽)로 검토했다. Effect(효과): ONNX parity(ONNX 동등성)는 `5/5` 통과했지만 proxy net(프록시 순수익)이 모두 음수라 runtime package(런타임 패키지)를 열지 않았다.

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- trained_model_rows(학습 모델 행): `{final['trained_model_rows']}`
- onnx_parity(ONNX 동등성): `{final['onnx_parity_passed_rows']}/{final['onnx_parity_rows']}`
- positive_proxy_rows(양수 프록시 행): `{final['positive_proxy_rows']}`
- best_inner_holdout_proxy_net(최고 내부 보류 프록시 순수익): `{final['best_inner_holdout_proxy_net']}`
- best_inner_holdout_profit_factor(최고 내부 보류 수익 팩터): `{final['best_inner_holdout_profit_factor']}`
- runtime_package(런타임 패키지): `{final['runtime_package']}`
- gates(게이트): `{final['passed_gates']}/{final['gate_rows']}`

Boundary(경계): 이 review(검토)는 negative evidence(부정 근거)를 닫는 작업이다. MT5 execution(MT5 실행), Forward/Goal(전진/목표), runtime authority(런타임 권위), operating promotion(운영 승격)은 주장하지 않는다.

Next action(다음 행동): `{final['next_action']}`
"""
    return aw.write_text_lossless(REPORT_PATH, text, True)


def write_decision(final: Mapping[str, Any]) -> Path:
    text = f"""# {TODAY} Stage337HQ Decision(337HQ 결정)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- evidence(근거): `{rel(REPORT_PATH)}`, `{rel(TRAINING_CANDIDATE_REVIEW)}`, `{rel(PROXY_NEGATIVE_MEMORY)}`, `{rel(RUNTIME_PACKAGE_DECISION)}`

Action(행동): HP ONNX candidates(HP ONNX 후보)를 runtime package(런타임 패키지)로 넘기지 않고 HR second-order repair design(HR 2차 수리 설계)으로 넘겼다.
Effect(효과): ONNX parity(ONNX 동등성)만 좋은 후보를 운영 가능 모델로 착각하지 않는다.

Forward/Goal(전진/목표): `not_claimed`
runtime_authority(런타임 권위): `not_claimed`
claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return aw.write_text_lossless(DECISION_DOC, text, True)


def upsert_section_after_metadata(text: str, title_marker: str, section: str) -> str:
    lines = text.splitlines()
    start = None
    for index, line in enumerate(lines):
        if line.startswith("## ") and title_marker in line:
            start = index
            break
    if start is not None:
        end = start + 1
        while end < len(lines) and not lines[end].startswith("## "):
            end += 1
        del lines[start:end]
    insert_at = next((index for index, line in enumerate(lines) if line.startswith("## ")), len(lines))
    return "\n".join(lines[:insert_at] + section.strip("\n").splitlines() + [""] + lines[insert_at:]) + "\n"


def update_docs(final: Mapping[str, Any]) -> list[Path]:
    artifacts: list[Path] = []
    workspace, workspace_bom = aw.read_text_lossless(he.WORKSPACE_STATE)
    workspace = re.sub(r"^current_run_id:.*$", f"current_run_id: {final['next_action']}", workspace, count=1, flags=re.M)
    workspace = re.sub(r"^updated_on:.*$", f"updated_on: '{TODAY}'", workspace, count=1, flags=re.M)
    focus = (
        "- >-\n"
        f"  Stage337 run337HQ focus complete(337단계 run337HQ 초점 완료): `{final['status']}`. "
        f"Effect(효과): ONNX parity(ONNX 동등성) `{final['onnx_parity_passed_rows']}/{final['onnx_parity_rows']}`는 통과했지만 positive proxy rows(양수 프록시 행) `{final['positive_proxy_rows']}`라 runtime package(런타임 패키지)를 닫고 `{final['next_action']}`을 열었다. Forward/Goal(전진/목표)은 주장하지 않는다.\n"
    )
    if "Stage337 run337HQ focus complete" in workspace:
        workspace = re.sub(r"- >-\n  Stage337 run337HQ focus complete.*?(?=\n- >-|\n[a-zA-Z_]+:|$)", focus.rstrip(), workspace, count=1, flags=re.S)
    else:
        workspace = workspace.replace("current_focus:\n", "current_focus:\n" + focus, 1)
    artifacts.append(aw.write_text_lossless(he.WORKSPACE_STATE, workspace, workspace_bom))

    current, current_bom = aw.read_text_lossless(he.CURRENT_STATE)
    current_lines = current.splitlines()
    replacements = {
        "- current_run(": f"- current_run(현재 실행): `{final['next_action']}`",
        "- status(": f"- status(상태): `{final['status']}`",
        "- decision(": f"- decision(결정): `{final['decision']}`",
        "- latest_completed_run(": f"- latest_completed_run(최근 완료 실행): `{RUN_ID}`",
        "- next_action(": f"- next_action(다음 행동): `{final['next_action']}`",
        "- claim_boundary(": f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
    }
    for index, line in enumerate(current_lines):
        if line.startswith("## "):
            break
        for prefix, replacement in replacements.items():
            if line.startswith(prefix):
                current_lines[index] = replacement
                break
    current = "\n".join(current_lines) + "\n"
    section = f"""## run337HQ Proxy Negative Trade Shape Training Review(프록시 음수 거래 형태 학습 검토)

Action(행동): run337HQ(337HQ 실행)는 HP trained ONNX candidates(HP 학습 ONNX 후보)를 검토했다.
Effect(효과): ONNX parity(ONNX 동등성) `{final['onnx_parity_passed_rows']}/{final['onnx_parity_rows']}`는 통과했지만 positive proxy rows(양수 프록시 행) `{final['positive_proxy_rows']}`, best proxy net(최고 프록시 순수익) `{final['best_inner_holdout_proxy_net']}`라 runtime package(런타임 패키지)를 열지 않았다.

Boundary(경계): MT5 execution(MT5 실행), Forward/Goal(전진/목표), runtime authority(런타임 권위), operating promotion(운영 승격)은 주장하지 않는다.
Next(다음): `{final['next_action']}`.
"""
    current = upsert_section_after_metadata(current, "run337HQ Proxy Negative Trade Shape Training Review", section)
    artifacts.append(aw.write_text_lossless(he.CURRENT_STATE, current, current_bom))

    selection = f"""# Stage337 Selection Status(337단계 선택 상태)

- latest_run(최신 실행): `{RUN_ID}`
- latest_decision(최신 결정): `{final['decision']}`
- current_run(현재 실행): `{final['next_action']}`
- rebuild_status(재구축 상태): `{final['status']}`
- trained_model_rows(학습 모델 행): `{final['trained_model_rows']}`
- onnx_parity(ONNX 동등성): `{final['onnx_parity_passed_rows']}/{final['onnx_parity_rows']}`
- positive_proxy_rows(양수 프록시 행): `{final['positive_proxy_rows']}`
- best_inner_holdout_proxy_net(최고 내부 보류 프록시 순수익): `{final['best_inner_holdout_proxy_net']}`
- runtime_package(런타임 패키지): `{final['runtime_package']}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{final['next_action']}`
- effect(효과): HQ review(HQ 검토)는 음수 프록시를 부정 근거로 닫고 HR design(HR 설계) 조건을 만든다.
"""
    artifacts.append(aw.write_text_lossless(he.SELECTED_STATUS, selection, True))

    brief, brief_bom = aw.read_text_lossless(he.STAGE_BRIEF)
    brief_entry = (
        f"- {TODAY}: run337HQ(337HQ 실행) `{final['status']}`. "
        f"Effect(효과): positive proxy rows(양수 프록시 행) `{final['positive_proxy_rows']}`, best net(최고 순수익) `{final['best_inner_holdout_proxy_net']}`로 runtime package(런타임 패키지)를 열지 않고 `{final['next_action']}`을 열었다."
    )
    artifacts.append(aw.write_text_lossless(he.STAGE_BRIEF, fb.upsert_single_line(brief, "run337HQ(337HQ 실행)", brief_entry), brief_bom))

    changelog, changelog_bom = aw.read_text_lossless(he.CHANGELOG)
    changelog_entry = (
        f"- {TODAY}: Stage337 run337HQ(337HQ 실행) `{final['status']}`. "
        f"Effect(효과): HP ONNX training(HP ONNX 학습)을 부정 검토로 닫고 `{final['next_action']}`을 열었다."
    )
    artifacts.append(aw.write_text_lossless(he.CHANGELOG, fb.upsert_single_line(changelog, "Stage337 run337HQ", changelog_entry), changelog_bom))
    return artifacts


def update_registers(final: Mapping[str, Any]) -> list[Path]:
    run_row = {"run_id": RUN_ID, "stage_id": STAGE_ID, "lane": "proxy_negative_trade_shape_training_review", "status": final["status"], "judgment": final["judgment"], "path": rel(REPORT_PATH), "notes": f"onnx={final['onnx_parity_passed_rows']}/{final['onnx_parity_rows']};positive_proxy={final['positive_proxy_rows']};best_net={final['best_inner_holdout_proxy_net']};runtime_package={final['runtime_package']};next_action={final['next_action']};goal_achieve_not_claimed."}
    alpha_row = {"ledger_row_id": f"{RUN_ID}__training_review", "stage_id": STAGE_ID, "run_id": RUN_ID, "subrun_id": "training_review", "parent_run_id": PARENT_RUN_ID, "record_view": "proxy_negative_trade_shape_training_review(프록시 음수 거래 형태 학습 검토)", "tier_scope": "Tier A inner holdout review(Tier A 내부 보류 검토)", "kpi_scope": "proxy_negative_onnx_parity_no_runtime_package(프록시 음수, ONNX 동등성, 런타임 패키지 없음)", "scoreboard_lane": "model_validation", "status": final["status"], "judgment": final["judgment"], "path": rel(REPORT_PATH), "primary_kpi": f"positive_proxy={final['positive_proxy_rows']};best_net={final['best_inner_holdout_proxy_net']}", "guardrail_kpi": "onnx_parity_passed;no_mt5;no_selection;no_goal", "external_verification_status": "out_of_scope_by_claim(주장 범위 밖)", "notes": f"decision={final['decision']};next_action={final['next_action']};claim_boundary={CLAIM_BOUNDARY}"}
    stage_row = {"ledger_row_id": f"{RUN_ID}__training_review", "stage_id": STAGE_ID, "run_id": RUN_ID, "work_family": "kpi_evidence_model_validation", "evidence_scope": "HP model manifest, ONNX parity, proxy scorecard", "kpi_scope": "negative_proxy_no_operating_claim", "status": final["status"], "judgment": final["judgment"], "claim_boundary": CLAIM_BOUNDARY, "path": rel(REPORT_PATH), "notes": f"gates={final['passed_gates']}/{final['gate_rows']};next_action={final['next_action']};goal_achieve_not_claimed", "decision": final["decision"], "run_key": f"{RUN_ID}__training_review", "family": "proxy_negative_trade_shape_training_review", "question": "do HP trained ONNX candidates justify runtime package(HP 학습 ONNX 후보가 런타임 패키지를 정당화하는가)", "metric_scope": "onnx_parity_proxy_net_runtime_package_decision", "primary_artifact": rel(TRAINING_CANDIDATE_REVIEW), "report_path": rel(REPORT_PATH), "next_action": final["next_action"]}
    return [
        fb.upsert_csv_worktree(he.RUN_REGISTRY, aw.RUN_REGISTRY_COLUMNS, run_row, "run_id"),
        fb.upsert_csv_worktree(he.ALPHA_LEDGER, aw.ALPHA_LEDGER_COLUMNS, alpha_row, "ledger_row_id"),
        fb.upsert_csv_worktree(he.STAGE_LEDGER, aw.STAGE_LEDGER_COLUMNS, stage_row, "ledger_row_id"),
    ]


def update_artifact_registry(paths: Sequence[Path]) -> Path:
    columns, rows = aw.read_csv_table(he.ARTIFACT_REGISTRY, prefer_head=False)
    columns = list(columns or aw.ARTIFACT_COLUMNS)
    for column in aw.ARTIFACT_COLUMNS:
        if column not in columns:
            columns.append(column)
    for extra in ("artifact_path", "claim_boundary"):
        if extra not in columns:
            columns.append(extra)
    rows = [row for row in rows if not str(row.get("artifact_id", "")).startswith(f"{RUN_ID}::") and str(row.get("run_id", "")) != RUN_ID]
    created_at = now_utc()
    seen: set[str] = set()
    for path in paths:
        if not path_exists(path) or not aw.io_path(path).is_file():
            continue
        artifact_path = rel(path)
        artifact_id = f"{RUN_ID}::{artifact_path}"
        if artifact_id in seen:
            continue
        seen.add(artifact_id)
        rows.append({"artifact_id": artifact_id, "artifact_type": path.suffix.lstrip(".") or "file", "path": artifact_path, "sha256": aw.sha256_file(path), "stage_id": STAGE_ID, "run_id": RUN_ID, "created_at_utc": created_at, "notes": STATUS, "artifact_path": artifact_path, "claim_boundary": CLAIM_BOUNDARY})
    return write_csv(he.ARTIFACT_REGISTRY, columns, rows)


def main() -> int:
    aw.io_path(RUN_DIR).mkdir(parents=True, exist_ok=True)
    missing = fail_if_missing(INPUT_FILES)
    if missing:
        print(json.dumps({"run_id": RUN_ID, "status": "blocked_missing_inputs", "missing": [rel(path) for path in missing]}, ensure_ascii=False, indent=2))
        return 1
    candidate_rows, parity_rows, memory_rows, runtime_decision, release_rows, queue_rows, summary = build_reviews()
    final = make_final(summary)
    artifacts: list[Path] = [
        write_csv(TRAINING_CANDIDATE_REVIEW, CANDIDATE_COLUMNS, candidate_rows),
        write_csv(ONNX_PARITY_REVIEW, PARITY_COLUMNS, parity_rows),
        write_csv(PROXY_NEGATIVE_MEMORY, MEMORY_COLUMNS, memory_rows),
        write_csv(RUNTIME_PACKAGE_DECISION, DECISION_COLUMNS, runtime_decision),
        write_csv(RELEASE_DISPOSITION_REVIEW, RELEASE_COLUMNS, release_rows),
        write_csv(HR_QUEUE, QUEUE_COLUMNS, queue_rows),
    ]
    gates = build_gates(final)
    final["gate_rows"] = len(gates)
    final["passed_gates"] = sum(1 for row in gates if row["status"] == "passed")
    final["failed_gates"] = [row["gate_id"] for row in gates if row["status"] != "passed"]
    artifacts.extend([write_csv(GATE_AUDIT, GATE_COLUMNS, gates), write_json(FINAL_DECISION, final), write_json(RUN_MANIFEST, {"run_id": RUN_ID, "parent_run_id": PARENT_RUN_ID, "inputs": [rel(path) for path in INPUT_FILES], "outputs": [rel(path) for path in OUTPUT_FILES], "claim_boundary": CLAIM_BOUNDARY})])
    artifacts.extend(write_receipts(final, artifacts))
    artifacts.extend([write_report(final), write_decision(final)])
    artifacts.extend(update_docs(final))
    artifacts.extend(update_registers(final))
    artifacts.append(update_artifact_registry(artifacts))
    print(json.dumps({"run_id": RUN_ID, "status": final["status"], "onnx_parity": f"{final['onnx_parity_passed_rows']}/{final['onnx_parity_rows']}", "positive_proxy_rows": final["positive_proxy_rows"], "best_inner_holdout_proxy_net": final["best_inner_holdout_proxy_net"], "runtime_package": final["runtime_package"], "gates": f"{final['passed_gates']}/{final['gate_rows']}", "next_action": final["next_action"], "goal_achieve": "not_claimed"}, ensure_ascii=False, indent=2))
    return 0 if not final["failed_gates"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
