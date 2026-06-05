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
from stage_pipelines.stage337 import train_mt5_negative_repair_probability_mismatch_net_recovery_post_runtime_probe_candidates_without_db as hk  # noqa: E402


aw = hk.aw
fb = hk.fb
he = hk.he

TODAY = "2026-05-31"
STAGE_ID = hk.STAGE_ID
RUN_NUMBER = "run337HL"
RUN_ID = "run337HL_review_mt5_negative_repair_probability_mismatch_net_recovery_post_runtime_probe_training_without_db_v1"
PARENT_RUN_ID = hk.RUN_ID
NEXT_RUN_ID = "run337HM_design_post_runtime_probe_proxy_negative_trade_shape_repair_without_db_v1"
STATUS = "completed_stage337HL_post_runtime_probe_training_review_all_proxy_negative_no_runtime_package_no_selection"
JUDGMENT = "onnx_parity_passed_but_all_inner_holdout_proxy_negative_repair_design_required"
DECISION = "stage337HL_open_run337HM_proxy_negative_trade_shape_repair_design"
CLAIM_BOUNDARY = (
    "research_development_only_stage337HL_post_runtime_probe_training_review_without_db_"
    "onnx_parity_reviewed_proxy_negative_no_runtime_package_no_candidate_selection_no_mt5_execution_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = hk.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = hk.REVIEWS_DIR
REPORT_PATH = REVIEWS_DIR / "run337HL_post_runtime_probe_training_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage337HL_post_runtime_probe_training_review.md"

HK_FINAL = hk.FINAL_DECISION
HK_GATES = hk.GATE_AUDIT
HK_QUEUE = hk.HL_QUEUE
HK_MODEL_MANIFEST = hk.TRAINED_MODEL_MANIFEST
HK_ONNX_PARITY = hk.ONNX_PARITY
HK_CLASSIFICATION = hk.CLASSIFICATION_SCORECARD
HK_PROXY = hk.PROXY_TRADE_SCORECARD
HK_FIREWALL = hk.RUNTIME_FIREWALL
HK_RELEASE = hk.RELEASE_DISPOSITION
HK_FEATURE_SCHEMA = hk.FEATURE_SCHEMA

TRAINING_CANDIDATE_REVIEW = RUN_DIR / "training_candidate_review.csv"
ONNX_PARITY_REVIEW = RUN_DIR / "onnx_parity_review.csv"
PROXY_CLUE_REVIEW = RUN_DIR / "proxy_clue_review.csv"
RELEASE_DISPOSITION_REVIEW = RUN_DIR / "release_disposition_review.csv"
NEGATIVE_TRAINING_MEMORY = RUN_DIR / "negative_training_memory.csv"
HM_QUEUE = RUN_DIR / "run337HM_design_queue.csv"
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
    HK_FINAL,
    HK_GATES,
    HK_QUEUE,
    HK_MODEL_MANIFEST,
    HK_ONNX_PARITY,
    HK_CLASSIFICATION,
    HK_PROXY,
    HK_FIREWALL,
    HK_RELEASE,
    HK_FEATURE_SCHEMA,
)
OUTPUT_FILES = (
    TRAINING_CANDIDATE_REVIEW,
    ONNX_PARITY_REVIEW,
    PROXY_CLUE_REVIEW,
    RELEASE_DISPOSITION_REVIEW,
    NEGATIVE_TRAINING_MEMORY,
    HM_QUEUE,
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
    "holdout_long_count",
    "holdout_short_count",
    "review_status",
    "blocked_reason",
    "effect",
    "claim_boundary",
)
PARITY_COLUMNS = ("model_id", "task_id", "passed", "max_abs_diff", "mean_abs_diff", "review_status", "effect", "claim_boundary")
PROXY_COLUMNS = ("review_id", "model_id", "net", "profit_factor", "expectancy", "trade_count", "long_short", "review_status", "allowed_use", "forbidden_use", "effect", "claim_boundary")
RELEASE_COLUMNS = ("review_id", "subject", "review_status", "allowed_use", "forbidden_use", "effect", "claim_boundary")
MEMORY_COLUMNS = ("memory_id", "source_run_id", "source_model", "evidence", "next_constraint_or_seed", "effect", "claim_boundary")
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
GATE_COLUMNS = hk.GATE_COLUMNS


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


def as_int(value: Any) -> int:
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return 0


def by_key(rows: Sequence[Mapping[str, str]], key: str) -> dict[str, Mapping[str, str]]:
    return {str(row.get(key, "")): row for row in rows}


def build_reviews() -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    dict[str, Any],
]:
    hk_final = read_json(HK_FINAL)
    model_rows = read_csv(HK_MODEL_MANIFEST)
    parity_rows = read_csv(HK_ONNX_PARITY)
    class_rows = [row for row in read_csv(HK_CLASSIFICATION) if row.get("split") == "inner_holdout"]
    proxy_rows = [row for row in read_csv(HK_PROXY) if row.get("split") == "inner_holdout"]
    release_rows = read_csv(HK_RELEASE)
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
        passed = str(parity.get("passed", "")).lower() == "true"
        review_status = "runtime_probe_blocked_proxy_negative(프록시 음수로 런타임 탐침 보류)" if net <= 0 else "runtime_probe_candidate(런타임 탐침 후보)"
        candidate_rows.append(
            {
                "model_id": model_id,
                "task_id": model.get("task_id", ""),
                "onnx_parity_passed": str(passed).lower(),
                "holdout_balanced_accuracy": cls.get("balanced_accuracy", ""),
                "holdout_proxy_net": net,
                "holdout_profit_factor": proxy.get("profit_factor", ""),
                "holdout_expectancy": proxy.get("expectancy", ""),
                "holdout_max_drawdown": proxy.get("max_drawdown", ""),
                "holdout_recovery_factor": proxy.get("recovery_factor", ""),
                "holdout_trade_count": proxy.get("trade_count", ""),
                "holdout_long_count": proxy.get("long_count", ""),
                "holdout_short_count": proxy.get("short_count", ""),
                "review_status": review_status,
                "blocked_reason": "inner_holdout_proxy_net_nonpositive(내부 보류 프록시 순수익 비양수)" if net <= 0 else "",
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
    proxy_review = [
        {
            "review_id": "hl_proxy_best",
            "model_id": best_candidate.get("model_id", ""),
            "net": best_candidate.get("holdout_proxy_net", 0),
            "profit_factor": best_candidate.get("holdout_profit_factor", ""),
            "expectancy": best_candidate.get("holdout_expectancy", ""),
            "trade_count": best_candidate.get("holdout_trade_count", ""),
            "long_short": f"{best_candidate.get('holdout_long_count', '')}/{best_candidate.get('holdout_short_count', '')}",
            "review_status": "negative(부정)" if not positive_proxy_rows else "positive_proxy_exists(긍정 프록시 존재)",
            "allowed_use": "repair design seed only(수리 설계 씨앗 전용)",
            "forbidden_use": "MT5 KPI or runtime authority(MT5 지표 또는 런타임 권위)",
            "effect": "blocks runtime package until proxy or design improves(프록시 또는 설계가 개선될 때까지 런타임 패키지 보류)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    release_review = [
        {
            "review_id": row.get("review_id", ""),
            "subject": row.get("subject", ""),
            "review_status": "carried_but_not_released(인계됐지만 해제 없음)",
            "allowed_use": "repair design only(수리 설계 전용)",
            "forbidden_use": "runtime package or selection(런타임 패키지 또는 선택)",
            "effect": "keeps release gates inactive because proxy is negative(프록시가 음수라 해제 게이트를 비활성 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for row in release_rows
    ]
    memory_rows = [
        {
            "memory_id": "hk_proxy_negative_all_candidates",
            "source_run_id": PARENT_RUN_ID,
            "source_model": best_candidate.get("model_id", ""),
            "evidence": f"best_proxy_net={best_candidate.get('holdout_proxy_net', '')};positive_proxy_rows={len(positive_proxy_rows)};onnx_parity={hk_final.get('onnx_parity_passed_rows')}/{hk_final.get('onnx_parity_rows')}",
            "next_constraint_or_seed": "repair trade-shape and proxy-negative surface before MT5 packaging(MT5 패키징 전 거래 형태와 프록시 음수 표면 수리)",
            "effect": "turns failed training into next design constraint(실패 학습을 다음 설계 제약으로 바꿈)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    queue_rows = [
        {
            "queue_id": "hm_proxy_negative_trade_shape_repair_design",
            "source_run_id": RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "task": "design repair for all-negative proxy ONNX training after post-runtime repair(사후 런타임 수리 뒤 전부 음수 프록시 ONNX 학습 수리 설계)",
            "required_inputs": f"{rel(TRAINING_CANDIDATE_REVIEW)};{rel(PROXY_CLUE_REVIEW)};{rel(NEGATIVE_TRAINING_MEMORY)}",
            "expected_outputs": "repair design queue, new weight or model-family proposal(수리 설계 대기열, 새 가중치 또는 모델 계열 제안)",
            "blocked_if_missing": "HL training review or negative memory(HL 학습 검토 또는 음수 기억)",
            "effect": "opens repair without runtime overclaim(런타임 과장 없이 수리 열기)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    summary = {
        "model_rows": len(model_rows),
        "candidate_review_rows": len(candidate_rows),
        "onnx_parity_rows": len(parity_review),
        "onnx_parity_passed_rows": sum(1 for row in parity_review if row["review_status"].startswith("passed")),
        "positive_proxy_rows": len(positive_proxy_rows),
        "best_model_id": best_candidate.get("model_id", ""),
        "best_inner_holdout_proxy_net": as_float(best_candidate.get("holdout_proxy_net")),
        "best_inner_holdout_profit_factor": as_float(best_candidate.get("holdout_profit_factor")),
        "best_inner_holdout_expectancy": as_float(best_candidate.get("holdout_expectancy")),
        "best_inner_holdout_trade_count": as_int(best_candidate.get("holdout_trade_count")),
        "best_inner_holdout_long_count": as_int(best_candidate.get("holdout_long_count")),
        "best_inner_holdout_short_count": as_int(best_candidate.get("holdout_short_count")),
        "release_review_rows": len(release_review),
        "negative_memory_rows": len(memory_rows),
        "hm_queue_rows": len(queue_rows),
        "hk_next_action": hk_final.get("next_action", ""),
        "hk_failed_gate_rows": sum(1 for row in read_csv(HK_GATES) if row.get("status") != "passed"),
    }
    return candidate_rows, parity_review, proxy_review, release_review, memory_rows, queue_rows, summary


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
        "threshold_tuning": "not_run",
        "lot_optimization": "not_run",
        "candidate_selection": "not_run",
        "mt5_runtime_probe": "not_run",
        "runtime_package": "not_run",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "live_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
        "primary_family": "kpi_evidence",
        "primary_skill": "obsidian-run-evidence-system",
        "support_skills": "obsidian-model-validation;obsidian-result-judgment;obsidian-performance-attribution;obsidian-claim-discipline",
        **dict(summary),
    }


def build_gates(final: Mapping[str, Any]) -> list[dict[str, Any]]:
    no_forbidden_claim = final["candidate_selection"] == "not_run" and final["mt5_runtime_probe"] == "not_run" and final["runtime_package"] == "not_run" and final["goal_achieve"] == "not_claimed"
    checks = [
        ("input_presence", final["missing_inputs"] == 0, str(final["missing_inputs"]), "0", rel(HK_MODEL_MANIFEST), "required HK outputs exist(필수 HK 산출물 존재)"),
        ("parent_hk_gates_passed", final["hk_failed_gate_rows"] == 0, str(final["hk_failed_gate_rows"]), "0", rel(HK_GATES), "HK gates passed(HK 게이트 통과)"),
        ("parent_next_action_matches", final["hk_next_action"] == RUN_ID, str(final["hk_next_action"]), RUN_ID, rel(HK_FINAL), "HL follows HK next action(HL이 HK 다음 행동을 따름)"),
        ("model_manifest_reviewed", final["model_rows"] == 5 and final["candidate_review_rows"] == 5, f"models={final['model_rows']};review={final['candidate_review_rows']}", "5/5", rel(TRAINING_CANDIDATE_REVIEW), "all trained candidates reviewed(모든 학습 후보 검토)"),
        ("onnx_parity_reviewed", final["onnx_parity_passed_rows"] == final["onnx_parity_rows"] == 5, f"passed={final['onnx_parity_passed_rows']};rows={final['onnx_parity_rows']}", "5/5", rel(ONNX_PARITY_REVIEW), "ONNX parity reviewed(ONNX 동등성 검토)"),
        ("proxy_negative_named", final["positive_proxy_rows"] == 0 and final["best_inner_holdout_proxy_net"] <= 0, f"positive={final['positive_proxy_rows']};best_net={final['best_inner_holdout_proxy_net']}", "0 positive and best<=0", rel(PROXY_CLUE_REVIEW), "all-negative proxy named(전부 음수 프록시 명명)"),
        ("runtime_package_blocked", final["runtime_package"] == "not_run", final["runtime_package"], "not_run", rel(RELEASE_DISPOSITION_REVIEW), "runtime package blocked before MT5 overclaim(MT5 과장 전 런타임 패키지 보류)"),
        ("negative_memory_written", final["negative_memory_rows"] >= 1, str(final["negative_memory_rows"]), ">=1", rel(NEGATIVE_TRAINING_MEMORY), "negative memory written(음수 기억 기록)"),
        ("repair_queue_opened", final["hm_queue_rows"] == 1 and final["next_action"] == NEXT_RUN_ID, f"queue={final['hm_queue_rows']};next={final['next_action']}", f"1 and {NEXT_RUN_ID}", rel(HM_QUEUE), "HM repair design queue opened(HM 수리 설계 대기열 열림)"),
        ("no_forbidden_claim", no_forbidden_claim, f"selection={final['candidate_selection']};mt5={final['mt5_runtime_probe']};runtime_package={final['runtime_package']};goal={final['goal_achieve']}", "not_run/not_run/not_run/not_claimed", rel(FINAL_DECISION), "review without operating claim(운영 주장 없는 검토)"),
        ("required_gate_coverage_audit", True, "all required gates listed(모든 필수 게이트 열거)", "present", rel(GATE_AUDIT), "completion claim tied to gates(완료 주장을 게이트에 연결)"),
    ]
    return [{"gate_id": gate_id, "status": "passed" if passed else "failed", "evidence_path": evidence, "observed": observed, "expected": expected, "effect": effect, "claim_boundary": CLAIM_BOUNDARY} for gate_id, passed, observed, expected, evidence, effect in checks]


def build_receipts(final: Mapping[str, Any], artifacts: Sequence[Path]) -> list[Path]:
    base = {"run_id": RUN_ID, "parent_run_id": PARENT_RUN_ID, "stage_id": STAGE_ID, "created_at_utc": now_utc(), "status": final["status"], "judgment": final["judgment"], "claim_boundary": CLAIM_BOUNDARY}
    receipts = [
        (DATA_RECEIPT, {**base, "data_source": rel(HK_FEATURE_SCHEMA), "integrity_judgment": "reviewable_artifacts_present(검토 가능 산출물 존재)"}),
        (MODEL_RECEIPT, {**base, "model_family": "LightGBM -> ONNX(라이트GBM -> 온엑스)", "onnx_parity": f"{final['onnx_parity_passed_rows']}/{final['onnx_parity_rows']}", "validation_judgment": "negative_proxy_no_runtime_package(프록시 음수, 런타임 패키지 없음)", "selection_metric": "none(없음)"}),
        (PERFORMANCE_RECEIPT, {**base, "best_inner_holdout_proxy_net": final["best_inner_holdout_proxy_net"], "positive_proxy_rows": final["positive_proxy_rows"], "attribution": "trade-shape/proxy surface still negative(거래 형태/프록시 표면 여전히 음수)"}),
        (RUNTIME_RECEIPT, {**base, "runtime_package": final["runtime_package"], "mt5_runtime_probe": final["mt5_runtime_probe"], "runtime_claim_boundary": "not_applicable_until_positive_training_review(긍정 학습 검토 전 해당 없음)"}),
        (JUDGMENT_RECEIPT, {**base, "result_subject": RUN_ID, "evidence_available": [rel(TRAINING_CANDIDATE_REVIEW), rel(ONNX_PARITY_REVIEW), rel(PROXY_CLUE_REVIEW)], "evidence_missing": "MT5 runtime probe and positive proxy candidate(MT5 런타임 탐침과 긍정 프록시 후보)", "judgment_label": "negative(부정)", "next_condition": NEXT_RUN_ID}),
        (CLAIM_RECEIPT, {**base, "forbidden_claims": "selected, runtime package, operating promotion, runtime authority, Goal Achieve(선택, 런타임 패키지, 운영 승격, 런타임 권위, 목표 달성)", "claim_guard": "all forbidden claims remain not_claimed/not_run(모든 금지 주장은 not_claimed/not_run)"}),
    ]
    paths = [write_json(path, payload) for path, payload in receipts]
    all_artifacts = list(artifacts) + paths
    lineage = {**base, "source_inputs": [rel(path) for path in INPUT_FILES], "producer": rel(Path(__file__)), "consumer": NEXT_RUN_ID, "artifact_paths": [rel(path) for path in all_artifacts], "artifact_hashes": {rel(path): aw.sha256_file(path) for path in all_artifacts if path_exists(path) and aw.io_path(path).is_file()}, "registry_links": [rel(he.RUN_REGISTRY), rel(he.ALPHA_LEDGER), rel(he.STAGE_LEDGER), rel(he.ARTIFACT_REGISTRY)], "availability": "generated_with_manifest(목록과 함께 생성)", "lineage_judgment": "connected_negative_training_review_to_HM_design_queue(음수 학습 검토를 HM 설계 대기열에 연결)"}
    paths.append(write_json(LINEAGE_RECEIPT, lineage))
    return paths


def write_report(final: Mapping[str, Any]) -> Path:
    text = f"""# Stage337 run337HL Post Runtime Probe Training Review(337단계 337HL 사후 런타임 학습 검토)

Action(행동): HK ONNX training(HK ONNX 학습) 결과를 검토했다. Effect(효과): ONNX parity(ONNX 동등성)는 `{final['onnx_parity_passed_rows']}/{final['onnx_parity_rows']}`로 통과했지만 inner holdout proxy(내부 보류 프록시)가 전부 음수라 runtime package(런타임 패키지)를 열지 않았다.

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- best_model(최고 모델): `{final['best_model_id']}`
- best_inner_holdout_proxy_net(최고 내부 보류 프록시 순수익): `{final['best_inner_holdout_proxy_net']}`
- positive_proxy_rows(긍정 프록시 행): `{final['positive_proxy_rows']}`
- best_trade_count(최고 거래수): `{final['best_inner_holdout_trade_count']}`
- long_short(롱/숏): `{final['best_inner_holdout_long_count']}/{final['best_inner_holdout_short_count']}`
- gates(게이트): `{final['passed_gates']}/{final['gate_rows']}`
- next_action(다음 행동): `{final['next_action']}`

Boundary(경계): MT5 execution(MT5 실행), runtime package(런타임 패키지), candidate selection(후보 선택), Forward/Goal(전진/목표)은 모두 `not_claimed/not_run`이다.
"""
    return aw.write_text_lossless(REPORT_PATH, text, True)


def write_decision(final: Mapping[str, Any]) -> Path:
    text = f"""# {TODAY} Stage337HL Decision(337HL 결정)

- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{final['decision']}`
- judgment(판정): `{final['judgment']}`
- next_action(다음 행동): `{final['next_action']}`
- evidence(근거): `{rel(REPORT_PATH)}`, `{rel(TRAINING_CANDIDATE_REVIEW)}`, `{rel(PROXY_CLUE_REVIEW)}`

Action(행동): proxy-negative training(프록시 음수 학습)을 runtime package(런타임 패키지)로 보내지 않았다.
Effect(효과): 다음 HM에서 trade-shape/proxy-negative repair(거래 형태/프록시 음수 수리)를 설계하게 한다.

Forward/Goal(전진/목표): `not_claimed`
runtime_authority(런타임 권위): `not_claimed`
claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return aw.write_text_lossless(DECISION_DOC, text, True)


def update_docs(final: Mapping[str, Any]) -> list[Path]:
    artifacts: list[Path] = []
    workspace, workspace_bom = aw.read_text_lossless(he.WORKSPACE_STATE)
    workspace = re.sub(r"^current_run_id:.*$", f"current_run_id: {final['next_action']}", workspace, count=1, flags=re.M)
    workspace = re.sub(r"^updated_on:.*$", f"updated_on: '{TODAY}'", workspace, count=1, flags=re.M)
    focus = (
        "- >-\n"
        f"  Stage337 run337HL focus complete(337단계 337HL 초점 완료): HK training review(HK 학습 검토)를 `{final['status']}`로 완료했다. "
        f"Effect(효과): ONNX parity(ONNX 동등성) `{final['onnx_parity_passed_rows']}/{final['onnx_parity_rows']}`는 통과했지만 best proxy net(최고 프록시 순수익) `{final['best_inner_holdout_proxy_net']}`라서 runtime package(런타임 패키지)를 열지 않고 `{final['next_action']}`을 열었다. Forward/Goal(전진/목표)은 주장하지 않는다.\n"
    )
    if "Stage337 run337HL focus complete" in workspace:
        workspace = re.sub(r"- >-\n  Stage337 run337HL focus complete.*?(?=\n- >-|\n[a-zA-Z_]+:|$)", focus.rstrip(), workspace, count=1, flags=re.S)
    else:
        workspace = workspace.replace("current_focus:\n", "current_focus:\n" + focus, 1)
    artifacts.append(aw.write_text_lossless(he.WORKSPACE_STATE, workspace, workspace_bom))

    current, current_bom = aw.read_text_lossless(he.CURRENT_STATE)
    for field_name, value in {
        "current_run": f"`{final['next_action']}`",
        "status": f"`{final['status']}`",
        "decision": f"`{final['decision']}`",
        "latest_completed_run": f"`{RUN_ID}`",
        "next_action": f"`{final['next_action']}`",
        "claim_boundary": f"`{CLAIM_BOUNDARY}`",
    }.items():
        current = fb.replace_bullet_field(current, field_name, value)
    section = f"""## run337HL Post Runtime Probe Training Review

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- onnx_parity(ONNX 동등성): `{final['onnx_parity_passed_rows']}/{final['onnx_parity_rows']}`
- positive_proxy_rows(긍정 프록시 행): `{final['positive_proxy_rows']}`
- best_inner_holdout_proxy_net(최고 내부 보류 프록시 순수익): `{final['best_inner_holdout_proxy_net']}`
- effect(효과): proxy(프록시)가 전부 음수라 런타임 패키지를 열지 않고 HM repair design(HM 수리 설계)을 열었다.
- next_action(다음 행동): `{final['next_action']}`
"""
    current = fb.upsert_section_before(current, "## run337HK Post Runtime Probe Repair LightGBM ONNX Training", section, "run337HL Post Runtime Probe Training Review")
    artifacts.append(aw.write_text_lossless(he.CURRENT_STATE, current, current_bom))

    selection = f"""# Stage337 Selection Status(337단계 선택 상태)

- latest_run(최신 실행): `{RUN_ID}`
- latest_decision(최신 결정): `{final['decision']}`
- current_run(현재 실행): `{final['next_action']}`
- rebuild_status(재구축 상태): `{final['status']}`
- onnx_parity(ONNX 동등성): `{final['onnx_parity_passed_rows']}/{final['onnx_parity_rows']}`
- positive_proxy_rows(긍정 프록시 행): `{final['positive_proxy_rows']}`
- best_inner_holdout_proxy_net(최고 내부 보류 프록시 순수익): `{final['best_inner_holdout_proxy_net']}`
- runtime_package(런타임 패키지): `not_run`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{final['next_action']}`
- effect(효과): HL review(검토)는 proxy negative(프록시 음수)를 수리 설계로 넘기고 operating selection(운영 선택)은 하지 않는다.
"""
    artifacts.append(aw.write_text_lossless(he.SELECTED_STATUS, selection, True))

    brief, brief_bom = aw.read_text_lossless(he.STAGE_BRIEF)
    brief_entry = f"- {TODAY}: run337HL(337HL 실행) `{final['status']}`. Effect(효과): ONNX parity `{final['onnx_parity_passed_rows']}/{final['onnx_parity_rows']}`는 통과했지만 best proxy net `{final['best_inner_holdout_proxy_net']}`라서 runtime package(런타임 패키지)를 열지 않고 `{final['next_action']}`을 열었다. Forward/Goal(전진/목표)은 주장하지 않는다."
    artifacts.append(aw.write_text_lossless(he.STAGE_BRIEF, fb.upsert_single_line(brief, "run337HL(337HL 실행)", brief_entry), brief_bom))

    changelog, changelog_bom = aw.read_text_lossless(he.CHANGELOG)
    changelog_entry = f"- {TODAY}: Stage337 run337HL(337HL 실행) `{final['status']}`. Effect(효과): HK training review(HK 학습 검토)를 음수 프록시로 닫고 HM repair design(HM 수리 설계)을 열었다."
    artifacts.append(aw.write_text_lossless(he.CHANGELOG, fb.upsert_single_line(changelog, "Stage337 run337HL", changelog_entry), changelog_bom))
    return artifacts


def update_registers(final: Mapping[str, Any]) -> list[Path]:
    run_row = {"run_id": RUN_ID, "stage_id": STAGE_ID, "lane": "post_runtime_probe_training_review", "status": final["status"], "judgment": final["judgment"], "path": rel(REPORT_PATH), "notes": f"onnx={final['onnx_parity_passed_rows']}/{final['onnx_parity_rows']};positive_proxy={final['positive_proxy_rows']};best_proxy={final['best_inner_holdout_proxy_net']};next_action={final['next_action']};goal_achieve_not_claimed."}
    alpha_row = {"ledger_row_id": f"{RUN_ID}__training_review", "stage_id": STAGE_ID, "run_id": RUN_ID, "subrun_id": "training_review", "parent_run_id": PARENT_RUN_ID, "record_view": "post_runtime_probe_training_review(사후 런타임 학습 검토)", "tier_scope": "Tier A inner holdout training review(Tier A 내부 보류 학습 검토)", "kpi_scope": "inner_holdout_proxy_no_mt5(내부 보류 프록시, MT5 없음)", "scoreboard_lane": "model_validation", "status": final["status"], "judgment": final["judgment"], "path": rel(REPORT_PATH), "primary_kpi": f"best_proxy={final['best_inner_holdout_proxy_net']};positive_proxy={final['positive_proxy_rows']}", "guardrail_kpi": "no_runtime_package;no_selection;no_goal", "external_verification_status": "out_of_scope_by_claim", "notes": f"decision={final['decision']};next_action={final['next_action']};goal_achieve_not_claimed."}
    stage_row = {"ledger_row_id": f"{RUN_ID}__training_review", "stage_id": STAGE_ID, "run_id": RUN_ID, "work_family": "kpi_evidence_model_validation_result_judgment", "evidence_scope": "HK model manifest, ONNX parity, proxy scorecard", "kpi_scope": "training_review_no_operating_claim", "status": final["status"], "judgment": final["judgment"], "claim_boundary": CLAIM_BOUNDARY, "path": rel(REPORT_PATH), "notes": f"gates={final['passed_gates']}/{final['gate_rows']};next_action={final['next_action']};goal_achieve_not_claimed", "decision": final["decision"], "run_key": f"{RUN_ID}__training_review", "family": "post_runtime_probe_training_review", "question": "do HK ONNX candidates merit MT5 runtime packaging(HK ONNX 후보가 MT5 런타임 패키징 가치가 있는가)", "metric_scope": "onnx_parity_inner_holdout_proxy_release_disposition", "primary_artifact": rel(TRAINING_CANDIDATE_REVIEW), "report_path": rel(REPORT_PATH), "next_action": final["next_action"]}
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
    candidate_rows, parity_rows, proxy_rows, release_rows, memory_rows, queue_rows, summary = build_reviews()
    final = make_final(summary)
    artifacts = [
        write_csv(TRAINING_CANDIDATE_REVIEW, CANDIDATE_COLUMNS, candidate_rows),
        write_csv(ONNX_PARITY_REVIEW, PARITY_COLUMNS, parity_rows),
        write_csv(PROXY_CLUE_REVIEW, PROXY_COLUMNS, proxy_rows),
        write_csv(RELEASE_DISPOSITION_REVIEW, RELEASE_COLUMNS, release_rows),
        write_csv(NEGATIVE_TRAINING_MEMORY, MEMORY_COLUMNS, memory_rows),
        write_csv(HM_QUEUE, QUEUE_COLUMNS, queue_rows),
    ]
    gates = build_gates(final)
    final["gate_rows"] = len(gates)
    final["passed_gates"] = sum(1 for row in gates if row["status"] == "passed")
    final["failed_gates"] = [row["gate_id"] for row in gates if row["status"] != "passed"]
    artifacts.extend([write_csv(GATE_AUDIT, GATE_COLUMNS, gates), write_json(FINAL_DECISION, final), write_json(RUN_MANIFEST, {"run_id": RUN_ID, "parent_run_id": PARENT_RUN_ID, "inputs": [rel(path) for path in INPUT_FILES], "outputs": [rel(path) for path in OUTPUT_FILES], "claim_boundary": CLAIM_BOUNDARY})])
    artifacts.extend(build_receipts(final, artifacts))
    artifacts.extend([write_report(final), write_decision(final)])
    artifacts.extend(update_docs(final))
    artifacts.extend(update_registers(final))
    artifacts.append(update_artifact_registry(artifacts))
    print(json.dumps({"run_id": RUN_ID, "status": final["status"], "positive_proxy_rows": final["positive_proxy_rows"], "best_inner_holdout_proxy_net": final["best_inner_holdout_proxy_net"], "onnx_parity": f"{final['onnx_parity_passed_rows']}/{final['onnx_parity_rows']}", "runtime_package": final["runtime_package"], "gates": f"{final['passed_gates']}/{final['gate_rows']}", "next_action": final["next_action"], "goal_achieve": "not_claimed"}, ensure_ascii=False, indent=2))
    return 0 if not final["failed_gates"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
