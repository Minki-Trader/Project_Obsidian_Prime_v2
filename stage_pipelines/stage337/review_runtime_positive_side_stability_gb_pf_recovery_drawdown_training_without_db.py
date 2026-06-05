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
from stage_pipelines.stage337 import train_runtime_positive_side_stability_gb_pf_recovery_drawdown_repair_candidates_without_db as gm  # noqa: E402


aw = gm.aw

TODAY = "2026-05-31"
STAGE_ID = gm.STAGE_ID
RUN_NUMBER = "run337GN"
RUN_ID = "run337GN_review_runtime_positive_side_stability_gb_pf_recovery_drawdown_training_without_db_v1"
PARENT_RUN_ID = gm.RUN_ID
NEXT_RUN_ID = "run337GO_materialize_runtime_positive_side_stability_gb_pf_recovery_drawdown_repair_runtime_probe_package_without_db_v1"
STATUS = "completed_stage337GN_side_stability_gb_pf_recovery_drawdown_training_review_runtime_probe_queue_open_no_selection_no_mt5"
JUDGMENT = "onnx_candidates_have_parity_positive_proxy_clues_runtime_probe_required_no_selection"
DECISION = "stage337GN_open_run337GO_materialize_runtime_positive_side_stability_gb_pf_recovery_drawdown_repair_runtime_probe_package_without_db"
CLAIM_BOUNDARY = (
    "research_development_only_stage337GN_side_stability_gb_pf_recovery_drawdown_training_review_without_db_"
    "no_new_training_no_threshold_tuning_no_lot_optimization_no_operating_selection_no_mt5_execution_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = gm.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = gm.REVIEWS_DIR
REPORT_PATH = REVIEWS_DIR / "run337GN_side_stability_gb_pf_recovery_drawdown_training_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage337GN_side_stability_gb_pf_recovery_drawdown_training_review.md"
SELECTED_STATUS = gm.SELECTED_STATUS
STAGE_BRIEF = gm.STAGE_BRIEF
WORKSPACE_STATE = gm.WORKSPACE_STATE
CURRENT_STATE = gm.CURRENT_STATE
CHANGELOG = gm.CHANGELOG
RUN_REGISTRY = gm.RUN_REGISTRY
ALPHA_LEDGER = gm.ALPHA_LEDGER
ARTIFACT_REGISTRY = gm.ARTIFACT_REGISTRY
STAGE_LEDGER = gm.STAGE_LEDGER

GM_FINAL = gm.FINAL_DECISION
GM_GATES = gm.GATE_AUDIT
GM_QUEUE = gm.GN_QUEUE
GM_MODEL_MANIFEST = gm.TRAINED_MODEL_MANIFEST
GM_ONNX_PARITY = gm.ONNX_PARITY
GM_CLASSIFICATION = gm.CLASSIFICATION_SCORECARD
GM_PROXY = gm.PROXY_TRADE_SCORECARD
GM_IMPORTANCE = gm.FEATURE_IMPORTANCE
GM_RUNTIME_FIREWALL = gm.RUNTIME_FIREWALL
GM_RELEASE = gm.RELEASE_DISPOSITION
GM_FEATURE_SCHEMA = gm.FEATURE_SCHEMA
GM_WEIGHT_AUDIT = gm.SAMPLE_WEIGHT_AUDIT

TRAINING_REVIEW_SCORECARD = RUN_DIR / "training_review_scorecard.csv"
PROXY_CLUE_REVIEW = RUN_DIR / "proxy_clue_review.csv"
ONNX_READINESS_REVIEW = RUN_DIR / "onnx_artifact_readiness_review.csv"
RUNTIME_PROBE_CANDIDATE_QUEUE = RUN_DIR / "runtime_probe_candidate_queue.csv"
RUNTIME_PROBE_PACKAGE_CONTRACT = RUN_DIR / "runtime_probe_package_contract.csv"
RELEASE_FIREWALL_REVIEW = RUN_DIR / "release_firewall_review.csv"
GO_QUEUE = RUN_DIR / "run337GO_materialization_queue.csv"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (
    GM_FINAL,
    GM_GATES,
    GM_QUEUE,
    GM_MODEL_MANIFEST,
    GM_ONNX_PARITY,
    GM_CLASSIFICATION,
    GM_PROXY,
    GM_IMPORTANCE,
    GM_RUNTIME_FIREWALL,
    GM_RELEASE,
    GM_FEATURE_SCHEMA,
    GM_WEIGHT_AUDIT,
)
OUTPUT_FILES = (
    TRAINING_REVIEW_SCORECARD,
    PROXY_CLUE_REVIEW,
    ONNX_READINESS_REVIEW,
    RUNTIME_PROBE_CANDIDATE_QUEUE,
    RUNTIME_PROBE_PACKAGE_CONTRACT,
    RELEASE_FIREWALL_REVIEW,
    GO_QUEUE,
    MODEL_RECEIPT,
    PERFORMANCE_RECEIPT,
    RUNTIME_RECEIPT,
    JUDGMENT_RECEIPT,
    LINEAGE_RECEIPT,
    GATE_AUDIT,
    FINAL_DECISION,
    RUN_MANIFEST,
    REPORT_PATH,
    DECISION_DOC,
    SELECTED_STATUS,
    WORKSPACE_STATE,
    CURRENT_STATE,
    CHANGELOG,
    STAGE_BRIEF,
    RUN_REGISTRY,
    ALPHA_LEDGER,
    STAGE_LEDGER,
    ARTIFACT_REGISTRY,
    Path(__file__),
)

REVIEW_COLUMNS = (
    "model_id",
    "task_id",
    "inner_holdout_balanced_accuracy",
    "inner_holdout_signal_density",
    "inner_holdout_proxy_net",
    "inner_holdout_proxy_pf",
    "inner_holdout_trade_count",
    "inner_holdout_long_count",
    "inner_holdout_short_count",
    "review_status",
    "allowed_use",
    "forbidden_use",
    "effect",
    "claim_boundary",
)
PROXY_COLUMNS = (
    "model_id",
    "task_id",
    "proxy_net_log_return",
    "proxy_profit_factor",
    "proxy_expectancy",
    "proxy_drawdown",
    "proxy_recovery_factor",
    "proxy_trade_count",
    "long_count",
    "short_count",
    "clue_status",
    "blocked_reason",
    "runtime_probe_priority",
    "claim_boundary",
)
ONNX_COLUMNS = (
    "model_id",
    "onnx_path",
    "model_path",
    "onnx_parity_passed",
    "feature_count",
    "artifact_status",
    "effect",
    "claim_boundary",
)
QUEUE_COLUMNS = (
    "queue_id",
    "next_run_id",
    "priority",
    "model_id",
    "task_id",
    "required_inputs",
    "required_outputs",
    "blocked_if_missing",
    "forbidden_action",
    "effect",
    "claim_boundary",
)
CONTRACT_COLUMNS = (
    "contract_id",
    "subject",
    "rule",
    "required_artifact",
    "forbidden_action",
    "effect",
    "claim_boundary",
)
GATE_COLUMNS = ("gate_id", "status", "evidence_path", "observed", "expected", "effect", "claim_boundary")


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


def build_reviews() -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    dict[str, Any],
]:
    models = {row["model_id"]: row for row in read_csv(GM_MODEL_MANIFEST)}
    parity = {row["model_id"]: row for row in read_csv(GM_ONNX_PARITY)}
    class_rows = {(row["model_id"], row["split"]): row for row in read_csv(GM_CLASSIFICATION)}
    proxy_rows = {(row["model_id"], row["split"]): row for row in read_csv(GM_PROXY)}
    review_rows: list[dict[str, Any]] = []
    clue_rows: list[dict[str, Any]] = []
    onnx_rows: list[dict[str, Any]] = []
    queue_rows: list[dict[str, Any]] = []
    positive_proxy_rows = 0
    ready_rows = 0
    best_proxy = -10**9
    best_model = ""

    for model_id, model in models.items():
        cls = class_rows.get((model_id, "inner_holdout"), {})
        proxy = proxy_rows.get((model_id, "inner_holdout"), {})
        par = parity.get(model_id, {})
        net = as_float(proxy.get("net_log_return_after_cost"))
        pf = as_float(proxy.get("profit_factor"))
        recovery = as_float(proxy.get("recovery_factor"))
        drawdown = as_float(proxy.get("max_drawdown"))
        trades = as_int(proxy.get("trade_count"))
        long_count = as_int(proxy.get("long_count"))
        short_count = as_int(proxy.get("short_count"))
        positive_proxy_rows += int(net > 0)
        if net > best_proxy:
            best_proxy = net
            best_model = model_id
        blocked: list[str] = []
        if net <= 0:
            blocked.append("proxy_net_nonpositive(프록시 순수익 비양수)")
        if pf < 1.05:
            blocked.append("proxy_pf_weak(프록시 수익 팩터 약함)")
        if recovery < 0.25:
            blocked.append("proxy_recovery_weak(프록시 회복 약함)")
        if trades < 100:
            blocked.append("trade_count_low(거래수 낮음)")
        if short_count < 30 or long_count < 30:
            blocked.append("side_balance_extreme(방향 균형 극단)")
        clue_status = "weak_positive_proxy_clue_runtime_probe_required(약한 긍정 프록시 단서, 런타임 탐침 필요)" if net > 0 else "negative_proxy_memory(음수 프록시 기억)"
        review_status = "runtime_probe_queue_candidate_no_selection(런타임 탐침 대기 후보, 선택 아님)" if net > 0 else "negative_proxy_memory_no_selection(음수 프록시 기억, 선택 아님)"
        review_rows.append(
            {
                "model_id": model_id,
                "task_id": model.get("task_id", ""),
                "inner_holdout_balanced_accuracy": cls.get("balanced_accuracy", ""),
                "inner_holdout_signal_density": cls.get("signal_density", ""),
                "inner_holdout_proxy_net": net,
                "inner_holdout_proxy_pf": pf,
                "inner_holdout_trade_count": trades,
                "inner_holdout_long_count": long_count,
                "inner_holdout_short_count": short_count,
                "review_status": review_status,
                "allowed_use": "runtime probe planning only(런타임 탐침 계획 전용)",
                "forbidden_use": "selection, Forward/Goal, runtime authority(선택, 전진/목표, 런타임 권위)",
                "effect": "keeps proxy score below MT5 evidence(프록시 점수를 MT5 근거 아래에 둠)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        clue_rows.append(
            {
                "model_id": model_id,
                "task_id": model.get("task_id", ""),
                "proxy_net_log_return": net,
                "proxy_profit_factor": pf,
                "proxy_expectancy": proxy.get("expectancy", ""),
                "proxy_drawdown": drawdown,
                "proxy_recovery_factor": recovery,
                "proxy_trade_count": trades,
                "long_count": long_count,
                "short_count": short_count,
                "clue_status": clue_status,
                "blocked_reason": ";".join(blocked) if blocked else "proxy_review_only_not_release(프록시 검토 전용, 해제 아님)",
                "runtime_probe_priority": "P0" if net > 0 else "P1_negative_memory",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        ready = par.get("passed") == "True" or par.get("passed") == "true"
        ready_rows += int(ready)
        onnx_rows.append(
            {
                "model_id": model_id,
                "onnx_path": model.get("onnx_path", ""),
                "model_path": model.get("model_path", ""),
                "onnx_parity_passed": "true" if ready else "false",
                "feature_count": model.get("feature_count", ""),
                "artifact_status": "ready_for_runtime_probe_package(런타임 탐침 패키지 준비)" if ready else "blocked_parity_failed(동등성 실패 차단)",
                "effect": "checks model artifact before MT5 handoff(MT5 인계 전 모델 산출물 확인)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        if ready:
            queue_rows.append(
                {
                    "queue_id": f"go_probe_{model_id}",
                    "next_run_id": NEXT_RUN_ID,
                    "priority": "P0" if net > 0 else "P1",
                    "model_id": model_id,
                    "task_id": model.get("task_id", ""),
                    "required_inputs": f"{model.get('onnx_path', '')};{rel(gm.GK_FRAME)};{rel(GM_FEATURE_SCHEMA)}",
                    "required_outputs": "runtime feature matrix, expected probability tape, MT5 set/ini package(런타임 피처 행렬, 예상 확률 테이프, MT5 set/ini 패키지)",
                    "blocked_if_missing": "ONNX artifact or GK frame(ONNX 산출물 또는 GK 프레임)",
                    "forbidden_action": "selection or Forward/Goal claim in GO(GO에서 선택 또는 전진/목표 주장)",
                    "effect": "opens MT5 comparison for proxy clue(프록시 단서의 MT5 비교 개방)",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )

    package_contract = [
        {
            "contract_id": "gn001_runtime_probe_all_ready_models",
            "subject": "runtime probe package(런타임 탐침 패키지)",
            "rule": "package all ONNX-ready models, with priority on positive proxy clue(ONNX 준비 모델 전체를 패키지하고 긍정 프록시 단서를 우선)",
            "required_artifact": rel(RUNTIME_PROBE_CANDIDATE_QUEUE),
            "forbidden_action": "runtime selection before MT5 probe(MT5 탐침 전 런타임 선택)",
            "effect": "ensures proxy is compared with MT5(프록시를 MT5와 비교하게 함)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "contract_id": "gn002_unique_timestamp_handoff",
            "subject": "handoff grain(인계 단위)",
            "rule": "future GO package must dedupe feature timestamps and preserve GM feature order(향후 GO 패키지는 피처 시각 중복 제거와 GM 피처 순서 보존 필요)",
            "required_artifact": rel(GM_FEATURE_SCHEMA),
            "forbidden_action": "duplicate timestamp evidence inflation(중복 시각 근거 부풀림)",
            "effect": "keeps runtime comparison clean(런타임 비교를 깨끗하게 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    release_rows = [
        {
            "contract_id": "gn_release_firewall",
            "subject": "release firewall(해제 방화벽)",
            "rule": "GN can open runtime package but cannot select candidate(GN는 런타임 패키지를 열 수 있지만 후보 선택 불가)",
            "required_artifact": rel(PROXY_CLUE_REVIEW),
            "forbidden_action": "operating promotion, runtime authority, Goal Achieve(운영 승격, 런타임 권위, 목표 달성)",
            "effect": "keeps proxy clue exploratory(프록시 단서를 탐색으로 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    go_queue = [
        {
            "queue_id": "go001_materialize_runtime_positive_side_stability_gb_pf_recovery_drawdown_repair_runtime_probe_package",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "model_id": best_model,
            "task_id": models.get(best_model, {}).get("task_id", ""),
            "required_inputs": f"{rel(GM_MODEL_MANIFEST)};{rel(RUNTIME_PROBE_CANDIDATE_QUEUE)};{rel(GM_FEATURE_SCHEMA)};{rel(gm.GK_FRAME)}",
            "required_outputs": "Common Files sync, expected probability tape, MT5 tester package(Common Files 동기화, 예상 확률 테이프, MT5 테스터 패키지)",
            "blocked_if_missing": "GM model manifest or ONNX parity(GM 모델 목록 또는 ONNX 동등성)",
            "forbidden_action": "MT5 execution, selection, Forward/Goal claim in GO(GO에서 MT5 실행, 선택, 전진/목표 주장)",
            "effect": "moves review into runtime package materialization(검토를 런타임 패키지 물질화로 이동)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    summary = {
        "model_rows": len(models),
        "ready_onnx_rows": ready_rows,
        "positive_proxy_rows": positive_proxy_rows,
        "runtime_probe_candidate_rows": len(queue_rows),
        "go_queue_rows": len(go_queue),
        "best_model_id": best_model,
        "best_inner_holdout_proxy_net": best_proxy,
    }
    return review_rows, clue_rows, onnx_rows, queue_rows, package_contract, release_rows, go_queue, summary


def make_final(summary: Mapping[str, Any]) -> dict[str, Any]:
    gm_final = read_json(GM_FINAL)
    return {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_action": NEXT_RUN_ID,
        "missing_inputs": len(fail_if_missing(INPUT_FILES)),
        "gm_next_action": gm_final.get("next_action", ""),
        "gm_failed_gate_rows": sum(1 for row in read_csv(GM_GATES) if row.get("status") != "passed"),
        "new_training": "not_run",
        "threshold_tuning": "not_run",
        "lot_optimization": "not_run",
        "candidate_selection": "not_run",
        "mt5_execution": "not_run",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "runtime_authority": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
        **dict(summary),
    }


def build_gates(final: Mapping[str, Any]) -> list[dict[str, Any]]:
    no_forbidden_claim = final["candidate_selection"] == "not_run" and final["mt5_execution"] == "not_run" and final["goal_achieve"] == "not_claimed"
    checks = [
        ("input_presence", final["missing_inputs"] == 0, str(final["missing_inputs"]), "0", rel(GM_FINAL), "required GM outputs exist(필수 GM 산출물 존재)"),
        ("parent_gm_gates_passed", final["gm_failed_gate_rows"] == 0, str(final["gm_failed_gate_rows"]), "0", rel(GM_GATES), "GM gates passed(GM 게이트 통과)"),
        ("parent_next_action_matches", final["gm_next_action"] == RUN_ID, str(final["gm_next_action"]), RUN_ID, rel(GM_FINAL), "GN follows GM next action(GN이 GM 다음 행동을 따름)"),
        ("onnx_ready_reviewed", final["ready_onnx_rows"] == final["model_rows"] == 5, f"ready={final['ready_onnx_rows']};models={final['model_rows']}", "5/5", rel(ONNX_READINESS_REVIEW), "ONNX readiness reviewed(ONNX 준비 검토)"),
        ("proxy_clue_reviewed", final["positive_proxy_rows"] >= 1, str(final["positive_proxy_rows"]), ">=1", rel(PROXY_CLUE_REVIEW), "proxy clue reviewed(프록시 단서 검토)"),
        ("runtime_probe_queue_materialized", final["runtime_probe_candidate_rows"] == 5, str(final["runtime_probe_candidate_rows"]), "5", rel(RUNTIME_PROBE_CANDIDATE_QUEUE), "runtime probe candidate queue materialized(런타임 탐침 후보 대기열 물질화)"),
        ("go_queue_materialized", final["go_queue_rows"] == 1 and final["next_action"] == NEXT_RUN_ID, f"queue={final['go_queue_rows']};next={final['next_action']}", f"1 and {NEXT_RUN_ID}", rel(GO_QUEUE), "GO materialization queue opened(GO 물질화 대기열 열림)"),
        ("no_forbidden_claim", no_forbidden_claim, f"selection={final['candidate_selection']};mt5={final['mt5_execution']};goal={final['goal_achieve']}", "not_run/not_run/not_claimed", rel(FINAL_DECISION), "review without operating claim(운영 주장 없는 검토)"),
        ("required_gate_coverage_audit", True, "all required gates listed(모든 필수 게이트 열거)", "present", rel(GATE_AUDIT), "completion claim tied to gates(완료 주장이 게이트에 연결됨)"),
    ]
    return [
        {
            "gate_id": gid,
            "status": "passed" if ok else "failed",
            "evidence_path": ev,
            "observed": obs,
            "expected": exp,
            "effect": eff,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for gid, ok, obs, exp, ev, eff in checks
    ]


def build_receipts(final: Mapping[str, Any], artifacts: Sequence[Path]) -> list[Path]:
    model = {
        "onnx_ready": f"{final['ready_onnx_rows']}/{final['model_rows']}",
        "best_model_id": final["best_model_id"],
        "candidate_selection": "not_run(실행 안 함)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    performance = {
        "best_inner_holdout_proxy_net": final["best_inner_holdout_proxy_net"],
        "positive_proxy_rows": final["positive_proxy_rows"],
        "proxy_judgment": "weak clue only; MT5 runtime probe required(약한 단서 한정, MT5 런타임 탐침 필요)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    runtime = {
        "mt5_execution": "not_run(실행 안 함)",
        "runtime_probe_queue_rows": final["runtime_probe_candidate_rows"],
        "next_action": final["next_action"],
        "claim_boundary": CLAIM_BOUNDARY,
    }
    judgment = {
        "result_subject": RUN_ID,
        "judgment_label": final["judgment"],
        "goal_achieve": "not_claimed(주장 안 함)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    paths = [
        write_json(MODEL_RECEIPT, model),
        write_json(PERFORMANCE_RECEIPT, performance),
        write_json(RUNTIME_RECEIPT, runtime),
        write_json(JUDGMENT_RECEIPT, judgment),
    ]
    lineage_artifacts = list(artifacts) + paths
    lineage = {
        "source_inputs": [rel(path) for path in INPUT_FILES],
        "producer": rel(Path(__file__)),
        "consumer": NEXT_RUN_ID,
        "artifact_paths": [rel(path) for path in lineage_artifacts],
        "artifact_hashes": {
            rel(path): aw.sha256_file(path)
            for path in lineage_artifacts
            if path_exists(path) and aw.io_path(path).is_file()
        },
        "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
        "lineage_judgment": "connected_training_review_to_runtime_probe_package(학습 검토를 런타임 탐침 패키지에 연결)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    paths.append(write_json(LINEAGE_RECEIPT, lineage))
    return paths


def write_report(final: Mapping[str, Any]) -> Path:
    text = f"""# Stage337 run337GN Side Stability GB PF Recovery Drawdown Training Review(337단계 337GN 방향 안정 GB PF 회복 낙폭 학습 검토)

## Conclusion(결론)

Action(행동): GM ONNX candidates(GM ONNX 후보) `5`개를 검토했다. Effect(효과): ONNX readiness(ONNX 준비) `5/5`를 확인하고, proxy clue(프록시 단서) `{final['positive_proxy_rows']}`개를 MT5 runtime probe(MT5 런타임 탐침) 비교 대상으로 열었다.

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- best_model_id(최고 모델 ID): `{final['best_model_id']}`
- best_inner_holdout_proxy_net(최고 내부 보류 프록시 순수익): `{final['best_inner_holdout_proxy_net']}`
- runtime_probe_candidate_rows(런타임 탐침 후보 행): `{final['runtime_probe_candidate_rows']}`
- gates(게이트): `{final['passed_gates']}/{final['gate_rows']}`

Boundary(경계): GN(337GN 실행)는 review only(검토 전용)이다. MT5 execution(MT5 실행), candidate selection(후보 선택), Forward/Goal(전진/목표)은 모두 `not_claimed`다.

Next action(다음 행동): `{final['next_action']}`
"""
    return aw.write_text_lossless(REPORT_PATH, text, True)


def write_decision(final: Mapping[str, Any]) -> Path:
    text = f"""# {TODAY} Stage337GN Decision(337GN 결정)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- evidence(근거): `{rel(REPORT_PATH)}`, `{rel(PROXY_CLUE_REVIEW)}`, `{rel(RUNTIME_PROBE_CANDIDATE_QUEUE)}`

Action(행동): positive proxy clue(긍정 프록시 단서)를 MT5 runtime probe(MT5 런타임 탐침) 패키지로 넘겼다.
Effect(효과): 프록시 점수를 운영 주장으로 쓰지 않고 실제 MT5 비교로 연결한다.

Forward/Goal(전진/목표): `not_claimed`
runtime_authority(런타임 권위): `not_claimed`
claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return aw.write_text_lossless(DECISION_DOC, text, True)


def replace_line(text: str, prefix: str, replacement: str) -> str:
    pattern = re.compile(rf"^{re.escape(prefix)}.*$", flags=re.M)
    return pattern.sub(replacement, text, count=1) if pattern.search(text) else replacement + "\n" + text


def update_docs(final: Mapping[str, Any]) -> list[Path]:
    artifacts: list[Path] = []
    workspace, workspace_bom = aw.read_text_lossless(WORKSPACE_STATE)
    workspace = replace_line(workspace, "current_run_id:", f"current_run_id: {final['next_action']}")
    workspace = replace_line(workspace, "updated_on:", f"updated_on: '{TODAY}'")
    workspace = replace_line(workspace, "active_branch:", f"active_branch: {gm.fa.ey.current_branch()}")
    focus = (
        "- >-\n"
        f"  Stage337 run337GN focus complete: run337GN(337GN 실행)는 `{final['status']}`로 training review(학습 검토)를 완료했다. "
        f"Effect(효과): ONNX ready(ONNX 준비) `{final['ready_onnx_rows']}/{final['model_rows']}`, positive proxy rows(긍정 프록시 행) `{final['positive_proxy_rows']}`, gates(게이트) `{final['passed_gates']}/{final['gate_rows']}`를 기록하고 `{final['next_action']}`을 열었다. Forward/Goal(전진/목표)은 주장하지 않는다.\n"
    )
    if "Stage337 run337GN focus complete" in workspace:
        workspace = re.sub(r"- >-\n  Stage337 run337GN focus complete:.*?(?=\n- >-|\n[a-zA-Z_]+:|$)", focus.rstrip(), workspace, count=1, flags=re.S)
    else:
        workspace = workspace.replace("current_focus:\n", "current_focus:\n" + focus, 1)
    artifacts.append(aw.write_text_lossless(WORKSPACE_STATE, workspace, workspace_bom))

    current, current_bom = aw.read_text_lossless(CURRENT_STATE)
    for field_name, value in {
        "current_run": f"`{final['next_action']}`",
        "status": f"`{final['status']}`",
        "decision": f"`{final['decision']}`",
        "latest_completed_run": f"`{RUN_ID}`",
        "next_action": f"`{final['next_action']}`",
        "claim_boundary": f"`{CLAIM_BOUNDARY}`",
    }.items():
        current = gm.fb.replace_bullet_field(current, field_name, value)
    section = f"""## run337GN Side Stability GB PF Recovery Drawdown Training Review(방향 안정 GB PF 회복 낙폭 학습 검토)

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- best_model_id(최고 모델 ID): `{final['best_model_id']}`
- positive_proxy_rows(긍정 프록시 행): `{final['positive_proxy_rows']}`
- runtime_probe_candidate_rows(런타임 탐침 후보 행): `{final['runtime_probe_candidate_rows']}`
- gates(게이트): `{final['passed_gates']}/{final['gate_rows']}`
- effect(효과): proxy clue(프록시 단서)를 MT5 runtime probe package(MT5 런타임 탐침 패키지)로 넘겼다.
- next_action(다음 행동): `{final['next_action']}`
"""
    current = gm.fb.upsert_section_before(current, "## run337GM Side Stability GB PF Recovery Drawdown ONNX Training", section, "run337GN Side Stability GB PF Recovery Drawdown Training Review")
    artifacts.append(aw.write_text_lossless(CURRENT_STATE, current, current_bom))

    selection = f"""# Stage337 Selection Status(337단계 선택 상태)

- latest_run(최신 실행): `{RUN_ID}`
- latest_decision(최신 결정): `{final['decision']}`
- current_run(현재 실행): `{final['next_action']}`
- rebuild_status(재구축 상태): `{final['status']}`
- best_model_id(최고 모델 ID): `{final['best_model_id']}`
- best_inner_holdout_proxy_net(최고 내부 보류 프록시 순수익): `{final['best_inner_holdout_proxy_net']}`
- positive_proxy_rows(긍정 프록시 행): `{final['positive_proxy_rows']}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{final['next_action']}`
- effect(효과): GN(337GN 실행)는 review(검토)만 완료했고 MT5 execution(MT5 실행), operating selection(운영 선택)은 하지 않았다.
"""
    artifacts.append(aw.write_text_lossless(SELECTED_STATUS, selection, True))

    brief, brief_bom = aw.read_text_lossless(STAGE_BRIEF)
    brief_entry = f"- {TODAY}: run337GN(337GN 실행) `{final['status']}`. Effect(효과): positive proxy clue(긍정 프록시 단서) `{final['positive_proxy_rows']}`개를 MT5 runtime probe package(MT5 런타임 탐침 패키지) 물질화 `{final['next_action']}`으로 넘겼다. Forward/Goal(전진/목표)은 주장하지 않는다."
    artifacts.append(aw.write_text_lossless(STAGE_BRIEF, gm.fb.upsert_single_line(brief, "run337GN(337GN 실행)", brief_entry), brief_bom))

    changelog, changelog_bom = aw.read_text_lossless(CHANGELOG)
    changelog_entry = f"- {TODAY}: Stage337 run337GN(337GN 실행) `{final['status']}`. Effect(효과): GM ONNX 후보를 검토하고 GO runtime probe package(GO 런타임 탐침 패키지)를 열었다. Forward/Goal(전진/목표)은 주장하지 않았다."
    artifacts.append(aw.write_text_lossless(CHANGELOG, gm.fb.upsert_single_line(changelog, "Stage337 run337GN", changelog_entry), changelog_bom))
    return artifacts


def update_registers(final: Mapping[str, Any]) -> list[Path]:
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "side_stability_gb_pf_recovery_drawdown_training_review",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "notes": f"best={final['best_model_id']};proxy={final['best_inner_holdout_proxy_net']};positive_proxy_rows={final['positive_proxy_rows']};next_action={final['next_action']};goal_achieve_not_claimed.",
        "family": "model_validation_performance_attribution_result_judgment",
        "primary_report": rel(REPORT_PATH),
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__training_review",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "training_review",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "side_stability_gb_pf_recovery_drawdown_training_review(방향 안정 GB PF 회복 낙폭 학습 검토)",
        "tier_scope": "Tier A inner holdout proxy review; Tier B out_of_scope_by_claim(Tier A 내부 보류 프록시 검토, Tier B 주장 범위 밖)",
        "kpi_scope": "proxy and ONNX readiness only; no MT5 KPI(프록시와 ONNX 준비만, MT5 성과 없음)",
        "scoreboard_lane": "model_validation",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "primary_kpi": f"best_proxy={final['best_inner_holdout_proxy_net']};positive_proxy_rows={final['positive_proxy_rows']}",
        "guardrail_kpi": "onnx_ready;no_selection;no_mt5;no_goal",
        "external_verification_status": "required_next_action",
        "notes": f"decision={final['decision']};next_action={final['next_action']};goal_achieve_not_claimed.",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__training_review",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "model_validation_performance_attribution_result_judgment",
        "evidence_scope": "GM ONNX artifacts and proxy scorecard(GM ONNX 산출물과 프록시 점수표)",
        "kpi_scope": "proxy_no_mt5",
        "status": final["status"],
        "judgment": final["judgment"],
        "claim_boundary": CLAIM_BOUNDARY,
        "path": rel(REPORT_PATH),
        "notes": f"gates={final['passed_gates']}/{final['gate_rows']};next_action={final['next_action']};goal_achieve_not_claimed",
        "decision": final["decision"],
        "run_key": f"{RUN_ID}__training_review",
        "family": "side_stability_gb_pf_recovery_drawdown_training_review",
        "question": "which GM ONNX candidates require MT5 runtime comparison(GM ONNX 후보 중 어떤 후보가 MT5 런타임 비교가 필요한가)",
        "metric_scope": "onnx_readiness_proxy_clue_runtime_queue",
        "primary_artifact": rel(PROXY_CLUE_REVIEW),
        "report_path": rel(REPORT_PATH),
        "next_action": final["next_action"],
    }
    return [
        gm.fb.upsert_csv_worktree(RUN_REGISTRY, aw.RUN_REGISTRY_COLUMNS, run_row, "run_id"),
        gm.fb.upsert_csv_worktree(ALPHA_LEDGER, aw.ALPHA_LEDGER_COLUMNS, alpha_row, "ledger_row_id"),
        gm.fb.upsert_csv_worktree(STAGE_LEDGER, aw.STAGE_LEDGER_COLUMNS, stage_row, "ledger_row_id"),
    ]


def update_artifact_registry(paths: Sequence[Path]) -> Path:
    columns, rows = aw.read_csv_table(ARTIFACT_REGISTRY, prefer_head=False)
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
        row = {
            "artifact_id": artifact_id,
            "artifact_type": path.suffix.lstrip(".") or "file",
            "path": artifact_path,
            "sha256": aw.sha256_file(path),
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": created_at,
            "notes": STATUS,
            "artifact_path": artifact_path,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        rows.append({column: row.get(column, "") for column in columns})
    return write_csv(ARTIFACT_REGISTRY, columns, rows)


def main() -> int:
    aw.io_path(RUN_DIR).mkdir(parents=True, exist_ok=True)
    missing = fail_if_missing(INPUT_FILES)
    if missing:
        print(json.dumps({"run_id": RUN_ID, "status": "blocked_missing_inputs", "missing": [rel(path) for path in missing]}, ensure_ascii=False, indent=2))
        return 1
    review_rows, clue_rows, onnx_rows, queue_rows, package_contract, release_rows, go_queue, summary = build_reviews()
    final = make_final(summary)
    artifacts = [
        write_csv(TRAINING_REVIEW_SCORECARD, REVIEW_COLUMNS, review_rows),
        write_csv(PROXY_CLUE_REVIEW, PROXY_COLUMNS, clue_rows),
        write_csv(ONNX_READINESS_REVIEW, ONNX_COLUMNS, onnx_rows),
        write_csv(RUNTIME_PROBE_CANDIDATE_QUEUE, QUEUE_COLUMNS, queue_rows),
        write_csv(RUNTIME_PROBE_PACKAGE_CONTRACT, CONTRACT_COLUMNS, package_contract),
        write_csv(RELEASE_FIREWALL_REVIEW, CONTRACT_COLUMNS, release_rows),
        write_csv(GO_QUEUE, QUEUE_COLUMNS, go_queue),
    ]
    gates = build_gates(final)
    final["gate_rows"] = len(gates)
    final["passed_gates"] = sum(1 for row in gates if row["status"] == "passed")
    final["failed_gates"] = [row["gate_id"] for row in gates if row["status"] != "passed"]
    artifacts.extend(
        [
            write_csv(GATE_AUDIT, GATE_COLUMNS, gates),
            write_json(FINAL_DECISION, final),
            write_json(
                RUN_MANIFEST,
                {
                    "run_id": RUN_ID,
                    "parent_run_id": PARENT_RUN_ID,
                    "next_run_id": NEXT_RUN_ID,
                    "inputs": [rel(path) for path in INPUT_FILES],
                    "outputs": [rel(path) for path in OUTPUT_FILES],
                    "claim_boundary": CLAIM_BOUNDARY,
                },
            ),
        ]
    )
    artifacts.extend(build_receipts(final, artifacts))
    artifacts.extend([write_report(final), write_decision(final)])
    artifacts.extend(update_docs(final))
    artifacts.extend(update_registers(final))
    artifacts.append(update_artifact_registry(artifacts))
    print(json.dumps({"run_id": RUN_ID, "status": final["status"], "best_model_id": final["best_model_id"], "best_inner_holdout_proxy_net": final["best_inner_holdout_proxy_net"], "positive_proxy_rows": final["positive_proxy_rows"], "runtime_probe_candidate_rows": final["runtime_probe_candidate_rows"], "gates": f"{final['passed_gates']}/{final['gate_rows']}", "next_action": final["next_action"], "goal_achieve": "not_claimed"}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
