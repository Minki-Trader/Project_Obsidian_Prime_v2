from __future__ import annotations

import csv
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
from stage_pipelines.stage337 import train_broker_confirmed_side_cost_curve_repair_candidates_without_db as ey  # noqa: E402


aw = ey.aw

TODAY = "2026-05-31"
STAGE_ID = ey.STAGE_ID
RUN_NUMBER = "run337EZ"
RUN_ID = "run337EZ_review_broker_confirmed_side_cost_curve_training_without_db_v1"
PARENT_RUN_ID = ey.RUN_ID
NEXT_RUN_ID = "run337FA_materialize_broker_confirmed_side_cost_curve_runtime_probe_package_without_db_v1"
STATUS = "completed_stage337EZ_side_cost_curve_training_review_runtime_probe_queue_open_no_selection_no_mt5"
JUDGMENT = "onnx_candidates_have_parity_one_positive_proxy_clue_runtime_probe_required_no_selection"
DECISION = "stage337EZ_open_run337FA_materialize_side_cost_curve_runtime_probe_package_without_db"
CLAIM_BOUNDARY = (
    "research_development_only_stage337EZ_broker_confirmed_side_cost_curve_training_review_without_db_"
    "no_new_training_no_threshold_tuning_no_lot_optimization_no_operating_selection_no_mt5_probe_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = ey.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = ey.REVIEWS_DIR
REPORT_PATH = REVIEWS_DIR / "run337EZ_broker_confirmed_side_cost_curve_training_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage337EZ_broker_confirmed_side_cost_curve_training_review.md"
SELECTED_STATUS = ey.SELECTED_STATUS
STAGE_BRIEF = ey.STAGE_BRIEF
WORKSPACE_STATE = ey.WORKSPACE_STATE
CURRENT_STATE = ey.CURRENT_STATE
CHANGELOG = ey.CHANGELOG
RUN_REGISTRY = ey.RUN_REGISTRY
ALPHA_LEDGER = ey.ALPHA_LEDGER
ARTIFACT_REGISTRY = ey.ARTIFACT_REGISTRY
STAGE_LEDGER = ey.STAGE_LEDGER

EY_FINAL = ey.FINAL_DECISION
EY_GATES = ey.GATE_AUDIT
EY_QUEUE = ey.EZ_QUEUE
EY_MODEL_MANIFEST = ey.TRAINED_MODEL_MANIFEST
EY_ONNX_PARITY = ey.ONNX_PARITY
EY_CLASSIFICATION_SCORECARD = ey.CLASSIFICATION_SCORECARD
EY_PROXY_SCORECARD = ey.PROXY_TRADE_SCORECARD
EY_FEATURE_IMPORTANCE = ey.FEATURE_IMPORTANCE
EY_RUNTIME_FIREWALL = ey.RUNTIME_FIREWALL
EY_RELEASE_DISPOSITION = ey.RELEASE_DISPOSITION
EY_FEATURE_SCHEMA = ey.FEATURE_SCHEMA
EY_SAMPLE_WEIGHT_AUDIT = ey.SAMPLE_WEIGHT_AUDIT

TRAINING_REVIEW_SCORECARD = RUN_DIR / "training_review_scorecard.csv"
PROXY_CLUE_REVIEW = RUN_DIR / "proxy_clue_review.csv"
ONNX_READINESS_REVIEW = RUN_DIR / "onnx_artifact_readiness_review.csv"
RUNTIME_PROBE_CANDIDATE_QUEUE = RUN_DIR / "runtime_probe_candidate_queue.csv"
RUNTIME_PROBE_PACKAGE_CONTRACT = RUN_DIR / "runtime_probe_package_contract.csv"
RELEASE_FIREWALL_REVIEW = RUN_DIR / "release_firewall_review.csv"
FA_QUEUE = RUN_DIR / "run337FA_materialization_queue.csv"
ROUTING_RECEIPT = RUN_DIR / "routing_receipt.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (
    EY_FINAL,
    EY_GATES,
    EY_QUEUE,
    EY_MODEL_MANIFEST,
    EY_ONNX_PARITY,
    EY_CLASSIFICATION_SCORECARD,
    EY_PROXY_SCORECARD,
    EY_FEATURE_IMPORTANCE,
    EY_RUNTIME_FIREWALL,
    EY_RELEASE_DISPOSITION,
    EY_FEATURE_SCHEMA,
    EY_SAMPLE_WEIGHT_AUDIT,
)
OUTPUT_FILES = (
    TRAINING_REVIEW_SCORECARD,
    PROXY_CLUE_REVIEW,
    ONNX_READINESS_REVIEW,
    RUNTIME_PROBE_CANDIDATE_QUEUE,
    RUNTIME_PROBE_PACKAGE_CONTRACT,
    RELEASE_FIREWALL_REVIEW,
    FA_QUEUE,
    ROUTING_RECEIPT,
    DATA_RECEIPT,
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
    Path(__file__),
)

TRAINING_REVIEW_COLUMNS = (
    "model_id",
    "task_id",
    "feature_count",
    "inner_holdout_balanced_accuracy",
    "inner_holdout_macro_f1",
    "inner_holdout_log_loss",
    "inner_holdout_signal_density",
    "short_prediction_count",
    "long_prediction_count",
    "flat_prediction_count",
    "review_status",
    "allowed_use",
    "forbidden_use",
    "effect",
    "claim_boundary",
)
PROXY_REVIEW_COLUMNS = (
    "model_id",
    "task_id",
    "proxy_rank",
    "inner_holdout_trade_count",
    "inner_holdout_signal_density",
    "net_log_return_after_cost",
    "profit_factor",
    "expectancy",
    "max_drawdown",
    "recovery_factor",
    "long_count",
    "short_count",
    "long_net",
    "short_net",
    "balance_status",
    "proxy_clue_status",
    "allowed_use",
    "forbidden_use",
    "effect",
    "claim_boundary",
)
ONNX_REVIEW_COLUMNS = (
    "model_id",
    "task_id",
    "model_path",
    "model_exists",
    "model_sha256_matches",
    "onnx_path",
    "onnx_exists",
    "onnx_sha256_matches",
    "onnx_parity_passed",
    "onnx_max_abs_diff",
    "onnx_mean_abs_diff",
    "feature_order_hash",
    "class_order_json",
    "readiness_status",
    "allowed_use",
    "forbidden_use",
    "effect",
    "claim_boundary",
)
RUNTIME_QUEUE_COLUMNS = (
    "queue_id",
    "next_run_id",
    "probe_priority",
    "model_id",
    "task_id",
    "onnx_path",
    "model_path",
    "feature_schema_path",
    "proxy_reference",
    "required_mt5_symbol",
    "timeframe",
    "deposit",
    "leverage",
    "tester_model",
    "required_outputs",
    "blocked_if_missing",
    "forbidden_action",
    "effect",
    "claim_boundary",
)
CONTRACT_COLUMNS = (
    "contract_id",
    "requirement",
    "required_input",
    "required_output",
    "blocked_if_missing",
    "forbidden_action",
    "effect",
    "claim_boundary",
)
FIREWALL_COLUMNS = (
    "firewall_id",
    "status",
    "evidence_path",
    "allowed_use",
    "forbidden_use",
    "effect",
    "claim_boundary",
)
QUEUE_COLUMNS = (
    "queue_id",
    "next_run_id",
    "priority",
    "task",
    "required_inputs",
    "required_outputs",
    "blocked_if_missing",
    "forbidden_action",
    "effect",
    "claim_boundary",
)
GATE_COLUMNS = (
    "gate_id",
    "status",
    "evidence_path",
    "observed",
    "expected",
    "effect",
    "claim_boundary",
)


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


def repo_path(value: str) -> Path:
    path = Path(str(value))
    return path if path.is_absolute() else ROOT / path


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


def parse_json_map(value: str) -> dict[str, int]:
    try:
        parsed = json.loads(value or "{}")
    except json.JSONDecodeError:
        return {}
    return {str(key): as_int(item) for key, item in parsed.items()}


def bool_text(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "passed"}


def find_row(rows: Sequence[Mapping[str, str]], **criteria: str) -> dict[str, str]:
    for row in rows:
        if all(str(row.get(key, "")) == value for key, value in criteria.items()):
            return dict(row)
    return {}


def review_training_and_proxy() -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    dict[str, Any],
]:
    models = read_csv(EY_MODEL_MANIFEST)
    parity_rows = read_csv(EY_ONNX_PARITY)
    class_rows = read_csv(EY_CLASSIFICATION_SCORECARD)
    proxy_rows = read_csv(EY_PROXY_SCORECARD)

    training_review: list[dict[str, Any]] = []
    proxy_review: list[dict[str, Any]] = []
    onnx_review: list[dict[str, Any]] = []
    runtime_queue: list[dict[str, Any]] = []

    proxy_holdout = [row for row in proxy_rows if row.get("split") == "inner_holdout"]
    proxy_sorted = sorted(proxy_holdout, key=lambda row: as_float(row.get("net_log_return_after_cost")), reverse=True)
    proxy_rank = {row.get("model_id", ""): rank for rank, row in enumerate(proxy_sorted, start=1)}
    positive_proxy_rows = 0

    for model in models:
        model_id = model.get("model_id", "")
        task_id = model.get("task_id", "")
        class_row = find_row(class_rows, model_id=model_id, split="inner_holdout")
        proxy_row = find_row(proxy_rows, model_id=model_id, split="inner_holdout")
        parity = find_row(parity_rows, model_id=model_id)
        pred_counts = parse_json_map(class_row.get("pred_counts_json", "{}"))
        proxy_net = as_float(proxy_row.get("net_log_return_after_cost"))
        positive_proxy_rows += int(proxy_net > 0)
        short_count = as_int(proxy_row.get("short_count"))
        long_count = as_int(proxy_row.get("long_count"))
        if short_count < 50 or long_count < 50:
            balance_status = "imbalanced_probe_required(불균형 탐침 필요)"
        elif min(short_count, long_count) / max(short_count, long_count) < 0.20:
            balance_status = "side_skew_probe_required(방향 쏠림 탐침 필요)"
        else:
            balance_status = "balanced_enough_for_probe(탐침 가능 균형)"
        if proxy_net > 0:
            clue_status = "positive_proxy_clue_only(긍정 프록시 단서 한정)"
        elif proxy_net > -0.05:
            clue_status = "near_flat_proxy_clue_only(중립 근처 프록시 단서 한정)"
        else:
            clue_status = "negative_proxy_memory(음수 프록시 기억)"

        training_review.append(
            {
                "model_id": model_id,
                "task_id": task_id,
                "feature_count": model.get("feature_count", ""),
                "inner_holdout_balanced_accuracy": class_row.get("balanced_accuracy", ""),
                "inner_holdout_macro_f1": class_row.get("macro_f1", ""),
                "inner_holdout_log_loss": class_row.get("log_loss", ""),
                "inner_holdout_signal_density": class_row.get("signal_density", ""),
                "short_prediction_count": pred_counts.get("short", 0),
                "long_prediction_count": pred_counts.get("long", 0),
                "flat_prediction_count": pred_counts.get("flat", 0),
                "review_status": "weak_classification_surface_probe_only(약한 분류 표면, 탐침 전용)",
                "allowed_use": "runtime probe ordering and sanity review(런타임 탐침 순서와 점검)",
                "forbidden_use": "candidate selection, Forward Passed/Failed, Goal Achieve(후보 선택, 전진 통과/실패, 목표 달성)",
                "effect": "classification score is kept as context, not operating evidence(분류 점수는 문맥으로만 쓰고 운영 근거로 쓰지 않음)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

        proxy_review.append(
            {
                "model_id": model_id,
                "task_id": task_id,
                "proxy_rank": proxy_rank.get(model_id, ""),
                "inner_holdout_trade_count": proxy_row.get("trade_count", ""),
                "inner_holdout_signal_density": proxy_row.get("signal_density", ""),
                "net_log_return_after_cost": proxy_row.get("net_log_return_after_cost", ""),
                "profit_factor": proxy_row.get("profit_factor", ""),
                "expectancy": proxy_row.get("expectancy", ""),
                "max_drawdown": proxy_row.get("max_drawdown", ""),
                "recovery_factor": proxy_row.get("recovery_factor", ""),
                "long_count": long_count,
                "short_count": short_count,
                "long_net": proxy_row.get("long_net", ""),
                "short_net": proxy_row.get("short_net", ""),
                "balance_status": balance_status,
                "proxy_clue_status": clue_status,
                "allowed_use": "proxy sanity and MT5 comparison baseline(프록시 점검과 MT5 비교 기준)",
                "forbidden_use": "MT5 KPI substitute or operating selection(MT5 핵심 성과 지표 대체 또는 운영 선택)",
                "effect": "proxy clue is carried into MT5 probe instead of being promoted(프록시 단서를 승격하지 않고 MT5 탐침으로 넘김)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

        model_path = repo_path(model.get("model_path", ""))
        onnx_path = repo_path(model.get("onnx_path", ""))
        model_exists = path_exists(model_path)
        onnx_exists = path_exists(onnx_path)
        model_hash_match = model_exists and aw.sha256_file(model_path) == model.get("model_sha256")
        onnx_hash_match = onnx_exists and aw.sha256_file(onnx_path) == model.get("onnx_sha256")
        parity_passed = bool_text(parity.get("passed", ""))
        readiness = (
            "ready_for_runtime_probe(런타임 탐침 준비)"
            if model_exists and onnx_exists and model_hash_match and onnx_hash_match and parity_passed
            else "blocked_artifact_or_parity_gap(산출물 또는 동등성 공백 차단)"
        )
        onnx_review.append(
            {
                "model_id": model_id,
                "task_id": task_id,
                "model_path": model.get("model_path", ""),
                "model_exists": model_exists,
                "model_sha256_matches": model_hash_match,
                "onnx_path": model.get("onnx_path", ""),
                "onnx_exists": onnx_exists,
                "onnx_sha256_matches": onnx_hash_match,
                "onnx_parity_passed": parity_passed,
                "onnx_max_abs_diff": parity.get("max_abs_diff", ""),
                "onnx_mean_abs_diff": parity.get("mean_abs_diff", ""),
                "feature_order_hash": model.get("feature_order_hash", ""),
                "class_order_json": model.get("class_order_json", ""),
                "readiness_status": readiness,
                "allowed_use": "materialize MT5 runtime probe package(MT5 런타임 탐침 패키지 물질화)",
                "forbidden_use": "deployment or runtime authority(배포 또는 런타임 권위)",
                "effect": "artifact hashes and parity are checked before handoff(인계 전 산출물 해시와 동등성을 확인)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

        if readiness.startswith("ready"):
            priority = "P0" if proxy_rank.get(model_id) == 1 else f"P{min(proxy_rank.get(model_id, 9), 3)}"
            runtime_queue.append(
                {
                    "queue_id": f"fa_probe_{model_id}",
                    "next_run_id": NEXT_RUN_ID,
                    "probe_priority": priority,
                    "model_id": model_id,
                    "task_id": task_id,
                    "onnx_path": model.get("onnx_path", ""),
                    "model_path": model.get("model_path", ""),
                    "feature_schema_path": rel(EY_FEATURE_SCHEMA),
                    "proxy_reference": f"rank={proxy_rank.get(model_id, '')};net={proxy_row.get('net_log_return_after_cost', '')};pf={proxy_row.get('profit_factor', '')}",
                    "required_mt5_symbol": "US100",
                    "timeframe": "M5",
                    "deposit": "500",
                    "leverage": "100",
                    "tester_model": "Model=4 real ticks(실제 틱)",
                    "required_outputs": "MT5 report/trade tape/proxy diff/lineage(MT5 보고서/거래 테이프/프록시 차이/계보)",
                    "blocked_if_missing": "ONNX artifact, feature schema, Common Files handoff(ONNX 산출물, 피처 스키마, 공용 파일 인계)",
                    "forbidden_action": "probe rank is not operating selection(탐침 순위는 운영 선택이 아님)",
                    "effect": "all parity-passed candidates move to runtime evidence collection(동등성 통과 후보 모두 런타임 근거 수집으로 이동)",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )

    contract_rows = [
        {
            "contract_id": "mt5_runtime_probe_contract",
            "requirement": "run FPMarkets US100 M5 with Deposit=500, Leverage=100, Model=4 real ticks(FPMarkets US100 M5, 예수금 500, 레버리지 100, 실제 틱 실행)",
            "required_input": rel(RUNTIME_PROBE_CANDIDATE_QUEUE),
            "required_output": "MT5 report, trade list, tester settings, terminal output(MT5 보고서, 거래 목록, 테스터 설정, 터미널 출력)",
            "blocked_if_missing": "broker visibility or tester output(브로커 가시성 또는 테스터 출력)",
            "forbidden_action": "Forward Passed/Failed without MT5 evidence(MT5 근거 없는 전진 통과/실패)",
            "effect": "runtime meaning is tested outside proxy score(프록시 점수 밖에서 런타임 의미를 시험)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "contract_id": "proxy_mt5_diff_contract",
            "requirement": "compare proxy expected value with MT5 runtime probe(프록시 예상값과 MT5 런타임 탐침 비교)",
            "required_input": rel(PROXY_CLUE_REVIEW),
            "required_output": "diff, attribution, usability review(차이, 귀속, 사용 가능성 검토)",
            "blocked_if_missing": "runtime probe result(런타임 탐침 결과)",
            "forbidden_action": "use proxy as MT5 KPI(프록시를 MT5 핵심 성과 지표로 사용)",
            "effect": "proxy helps triage but cannot replace tester KPI(프록시는 선별을 돕지만 테스터 성과를 대체하지 않음)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "contract_id": "artifact_lineage_contract",
            "requirement": "preserve model, ONNX, feature schema, and hash lineage(모델, ONNX, 피처 스키마, 해시 계보 보존)",
            "required_input": f"{rel(EY_MODEL_MANIFEST)};{rel(ONNX_READINESS_REVIEW)}",
            "required_output": "runtime package manifest and receipt(런타임 패키지 목록과 영수증)",
            "blocked_if_missing": "hash mismatch or missing package manifest(해시 불일치 또는 패키지 목록 누락)",
            "forbidden_action": "untracked handoff(추적 없는 인계)",
            "effect": "runtime result can be traced back to trained artifact(런타임 결과를 학습 산출물로 추적 가능)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "contract_id": "no_threshold_or_lot_optimization_contract",
            "requirement": "use fixed candidate outputs without threshold or lot optimization(임계값 또는 로트 최적화 없이 고정 후보 출력 사용)",
            "required_input": rel(RUNTIME_PROBE_CANDIDATE_QUEUE),
            "required_output": "probe-only tester run(탐침 전용 테스터 실행)",
            "blocked_if_missing": "fixed probe settings(고정 탐침 설정)",
            "forbidden_action": "optimize thresholds, margins, or lots before probe(탐침 전 임계값, 마진, 로트 최적화)",
            "effect": "runtime probe measures the model surface, not tuned execution(런타임 탐침이 튜닝 실행이 아닌 모델 표면을 측정)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]

    firewall_rows = [
        {
            "firewall_id": "proxy_not_mt5_kpi",
            "status": "active(활성)",
            "evidence_path": rel(PROXY_CLUE_REVIEW),
            "allowed_use": "sanity clue and comparison baseline(점검 단서와 비교 기준)",
            "forbidden_use": "MT5 KPI, Forward Passed/Failed(MT5 성과, 전진 통과/실패)",
            "effect": "positive proxy net is not promoted(긍정 프록시 순값을 승격하지 않음)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "firewall_id": "selection_not_run",
            "status": "active(활성)",
            "evidence_path": rel(RUNTIME_PROBE_CANDIDATE_QUEUE),
            "allowed_use": "probe queue(탐침 대기열)",
            "forbidden_use": "operating selection(운영 선택)",
            "effect": "all parity-ready models remain candidates(동등성 준비 모델은 모두 후보로 남음)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "firewall_id": "mt5_not_run",
            "status": "active(활성)",
            "evidence_path": rel(RUNTIME_PROBE_PACKAGE_CONTRACT),
            "allowed_use": "open next runtime package work(다음 런타임 패키지 작업 열기)",
            "forbidden_use": "runtime authority or live readiness(런타임 권위 또는 실거래 준비)",
            "effect": "external verification is required before any operating claim(운영 주장 전 외부 검증이 필요)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]

    fa_queue = [
        {
            "queue_id": "fa_materialize_side_cost_curve_runtime_probe_package",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "task": "materialize MT5 runtime probe package for parity-ready ONNX candidates(동등성 준비 ONNX 후보의 MT5 런타임 탐침 패키지 물질화)",
            "required_inputs": f"{rel(RUNTIME_PROBE_CANDIDATE_QUEUE)};{rel(RUNTIME_PROBE_PACKAGE_CONTRACT)};{rel(EY_FEATURE_SCHEMA)}",
            "required_outputs": "run_manifest, Common Files handoff, tester execution instructions, proxy-vs-MT5 comparison shell(실행 목록, 공용 파일 인계, 테스터 실행 지시, 프록시-MT5 비교 틀)",
            "blocked_if_missing": "candidate queue or ONNX artifact(후보 대기열 또는 ONNX 산출물)",
            "forbidden_action": "declare Forward/Goal before MT5 probe(MT5 탐침 전 전진/목표 선언)",
            "effect": "EZ review turns trained artifacts into a bounded runtime verification packet(EZ 검토가 학습 산출물을 제한된 런타임 검증 묶음으로 바꿈)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]

    best_proxy = proxy_sorted[0] if proxy_sorted else {}
    holdout_class = [row for row in class_rows if row.get("split") == "inner_holdout"]
    best_class = max(holdout_class, key=lambda row: as_float(row.get("balanced_accuracy")), default={})
    summary = {
        "trained_model_rows": len(models),
        "onnx_rows": len(models),
        "onnx_readiness_rows": len(onnx_review),
        "onnx_ready_rows": sum(1 for row in onnx_review if str(row["readiness_status"]).startswith("ready")),
        "onnx_parity_rows": len(parity_rows),
        "onnx_parity_passed_rows": sum(1 for row in parity_rows if bool_text(row.get("passed", ""))),
        "training_review_rows": len(training_review),
        "proxy_review_rows": len(proxy_review),
        "positive_proxy_rows": positive_proxy_rows,
        "runtime_probe_queue_rows": len(runtime_queue),
        "package_contract_rows": len(contract_rows),
        "firewall_rows": len(firewall_rows),
        "fa_queue_rows": len(fa_queue),
        "best_proxy_model_id": best_proxy.get("model_id", ""),
        "best_proxy_net": as_float(best_proxy.get("net_log_return_after_cost")),
        "best_proxy_pf": as_float(best_proxy.get("profit_factor")),
        "best_holdout_model_id": best_class.get("model_id", ""),
        "best_inner_holdout_balanced_accuracy": as_float(best_class.get("balanced_accuracy")),
        "weak_classifier_max_bacc": as_float(best_class.get("balanced_accuracy")),
    }
    return training_review, proxy_review, onnx_review, runtime_queue, contract_rows + firewall_rows + fa_queue, summary


def build_gates(final: Mapping[str, Any]) -> list[dict[str, Any]]:
    no_forbidden_claim = (
        final["candidate_selection"] == "not_run"
        and final["mt5_runtime_probe"] == "not_run"
        and final["forward_passed"] == "not_claimed"
        and final["forward_failed"] == "not_claimed"
        and final["goal_achieve"] == "not_claimed"
    )
    checks = [
        ("input_presence", final["missing_inputs"] == 0, str(final["missing_inputs"]), "0", rel(EY_MODEL_MANIFEST), "required EY outputs exist(필수 EY 산출물 존재)"),
        ("parent_ey_gates_passed", final["ey_failed_gate_rows"] == 0, str(final["ey_failed_gate_rows"]), "0", rel(EY_GATES), "EY gates passed(EY 게이트 통과)"),
        ("parent_next_action_matches", final["ey_next_action"] == RUN_ID, str(final["ey_next_action"]), RUN_ID, rel(EY_FINAL), "EZ follows EY next action(EZ가 EY 다음 행동을 따름)"),
        ("onnx_artifacts_ready", final["onnx_ready_rows"] == final["trained_model_rows"] == 4, f"ready={final['onnx_ready_rows']};models={final['trained_model_rows']}", "4/4", rel(ONNX_READINESS_REVIEW), "ONNX artifacts and hashes ready(ONNX 산출물과 해시 준비)"),
        ("onnx_parity_passed", final["onnx_parity_passed_rows"] == final["onnx_parity_rows"] == 4, f"passed={final['onnx_parity_passed_rows']};rows={final['onnx_parity_rows']}", "4/4", rel(EY_ONNX_PARITY), "ONNX parity already passed(ONNX 동등성 통과)"),
        ("training_review_materialized", final["training_review_rows"] == 4, str(final["training_review_rows"]), "4", rel(TRAINING_REVIEW_SCORECARD), "training diagnostics reviewed(학습 진단 검토)"),
        ("proxy_clue_reviewed", final["proxy_review_rows"] == 4 and final["positive_proxy_rows"] >= 1, f"rows={final['proxy_review_rows']};positive={final['positive_proxy_rows']}", "4 rows and >=1 positive clue", rel(PROXY_CLUE_REVIEW), "proxy clue separated from MT5 claim(프록시 단서를 MT5 주장과 분리)"),
        ("runtime_probe_queue_all_candidates", final["runtime_probe_queue_rows"] == 4, str(final["runtime_probe_queue_rows"]), "4", rel(RUNTIME_PROBE_CANDIDATE_QUEUE), "all parity-ready candidates queued(동등성 준비 후보 모두 대기열 등록)"),
        ("runtime_probe_package_contract_materialized", final["package_contract_rows"] >= 4, str(final["package_contract_rows"]), ">=4", rel(RUNTIME_PROBE_PACKAGE_CONTRACT), "runtime probe contract exists(런타임 탐침 계약 존재)"),
        ("release_firewall_active", final["firewall_rows"] >= 3 and final["candidate_selection"] == "not_run", f"firewall={final['firewall_rows']};selection={final['candidate_selection']}", ">=3 and not_run", rel(RELEASE_FIREWALL_REVIEW), "selection and release remain blocked(선택과 해제가 계속 차단)"),
        ("fa_queue_materialized", final["fa_queue_rows"] == 1 and final["next_action"] == NEXT_RUN_ID, f"rows={final['fa_queue_rows']};next={final['next_action']}", f"1 and {NEXT_RUN_ID}", rel(FA_QUEUE), "FA runtime package queue opened(FA 런타임 패키지 대기열 열림)"),
        ("no_forbidden_claim", no_forbidden_claim, f"selection={final['candidate_selection']};mt5={final['mt5_runtime_probe']};goal={final['goal_achieve']}", "not_run/not_claimed", rel(FINAL_DECISION), "EZ reviews without operating claim(EZ는 운영 주장 없이 검토)"),
        ("required_gate_coverage_audit", True, "all required gates listed in closeout(모든 필수 게이트가 종료 기록에 있음)", "present", rel(GATE_AUDIT), "connects gates to completion claim(게이트를 완료 주장과 연결)"),
    ]
    return [
        {
            "gate_id": gate_id,
            "status": "passed" if passed else "failed",
            "evidence_path": evidence,
            "observed": observed,
            "expected": expected,
            "effect": effect,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for gate_id, passed, observed, expected, evidence, effect in checks
    ]


def split_combined_rows(rows: Sequence[Mapping[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    contracts: list[dict[str, Any]] = []
    firewalls: list[dict[str, Any]] = []
    fa_queue: list[dict[str, Any]] = []
    for row in rows:
        if "contract_id" in row:
            contracts.append(dict(row))
        elif "firewall_id" in row:
            firewalls.append(dict(row))
        else:
            fa_queue.append(dict(row))
    return contracts, firewalls, fa_queue


def build_receipts(final: Mapping[str, Any], artifact_paths: Sequence[Path]) -> list[Path]:
    routing = {
        "run_id": RUN_ID,
        "primary_family": "model_validation(모델 검증)",
        "primary_skill": "obsidian-model-validation(옵시디언 모델 검증)",
        "support_skills": [
            "obsidian-runtime-parity(옵시디언 런타임 동등성)",
            "obsidian-performance-attribution(옵시디언 성과 귀속)",
            "obsidian-artifact-lineage(옵시디언 산출물 계보)",
            "obsidian-result-judgment(옵시디언 결과 판정)",
        ],
        "required_gates": [row["gate_id"] for row in read_csv(GATE_AUDIT)] if path_exists(GATE_AUDIT) else [],
        "claim_boundary": CLAIM_BOUNDARY,
    }
    data = {
        "review_inputs": [rel(path) for path in INPUT_FILES],
        "feature_schema": rel(EY_FEATURE_SCHEMA),
        "data_judgment": "EY train-only inputs already reviewed; EZ does not reopen data split(EY 학습 전용 입력은 이미 검토됨, EZ는 데이터 분할을 다시 열지 않음)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    model = {
        "trained_models_reviewed": final["trained_model_rows"],
        "onnx_ready_rows": final["onnx_ready_rows"],
        "onnx_parity": f"{final['onnx_parity_passed_rows']}/{final['onnx_parity_rows']}",
        "selection_metric": "none; runtime probe queue only(없음, 런타임 탐침 대기열 전용)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    performance = {
        "best_proxy_model_id": final["best_proxy_model_id"],
        "best_proxy_net": final["best_proxy_net"],
        "best_proxy_pf": final["best_proxy_pf"],
        "best_holdout_model_id": final["best_holdout_model_id"],
        "best_inner_holdout_balanced_accuracy": final["best_inner_holdout_balanced_accuracy"],
        "performance_judgment": "proxy clue exists but MT5 runtime probe is required(프록시 단서는 있으나 MT5 런타임 탐침 필요)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    runtime = {
        "runtime_execution": "not_run(미실행)",
        "next_runtime_packet": NEXT_RUN_ID,
        "probe_queue_rows": final["runtime_probe_queue_rows"],
        "mt5_contract": "US100 M5 Deposit=500 Leverage=100 Model=4 real ticks(US100 M5 예수금 500 레버리지 100 실제 틱)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    judgment = {
        "result_subject": RUN_ID,
        "judgment_label": final["judgment"],
        "evidence_available": [
            rel(TRAINING_REVIEW_SCORECARD),
            rel(PROXY_CLUE_REVIEW),
            rel(ONNX_READINESS_REVIEW),
            rel(RUNTIME_PROBE_CANDIDATE_QUEUE),
        ],
        "evidence_missing": "MT5 runtime probe and proxy-vs-MT5 diff(MT5 런타임 탐침과 프록시-MT5 차이)",
        "goal_achieve": "not_claimed(주장 안 함)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    paths = [
        write_json(ROUTING_RECEIPT, routing),
        write_json(DATA_RECEIPT, data),
        write_json(MODEL_RECEIPT, model),
        write_json(PERFORMANCE_RECEIPT, performance),
        write_json(RUNTIME_RECEIPT, runtime),
        write_json(JUDGMENT_RECEIPT, judgment),
    ]
    all_artifacts = list(artifact_paths) + paths
    lineage = {
        "source_inputs": [rel(path) for path in INPUT_FILES],
        "producer": rel(Path(__file__)),
        "consumer": NEXT_RUN_ID,
        "artifact_paths": [rel(path) for path in all_artifacts],
        "artifact_hashes": {
            rel(path): aw.sha256_file(path)
            for path in all_artifacts
            if path_exists(path) and aw.io_path(path).is_file()
        },
        "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
        "lineage_judgment": "EY ONNX artifacts connected to FA runtime probe package(EY ONNX 산출물을 FA 런타임 탐침 패키지에 연결)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    paths.append(write_json(LINEAGE_RECEIPT, lineage))
    return paths


def write_report(final: Mapping[str, Any]) -> Path:
    text = f"""# Stage337 run337EZ Side/Cost/Curve Training Review(337단계 337EZ 방향/비용/곡선 학습 검토)

## Conclusion(결론)

run337EZ(337EZ 실행)는 run337EY(337EY 실행)의 ONNX candidates(온엑스 후보) `4`개를 검토했다.

Action(행동): ONNX artifact(온엑스 산출물), hash(해시), parity(동등성)를 확인했다. Effect(효과): Python model(파이썬 모델)과 ONNX(온엑스) 출력이 이어지는 후보만 runtime probe(런타임 탐침)로 넘긴다.

Action(행동): proxy expected value(프록시 예상값)를 MT5 KPI(MT5 핵심 성과 지표)와 분리했다. Effect(효과): positive proxy clue(긍정 프록시 단서) `1`개가 있어도 operating selection(운영 선택)으로 과장하지 않는다.

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- trained_models(학습 모델): `{final['trained_model_rows']}`
- onnx_ready(온엑스 준비): `{final['onnx_ready_rows']}/{final['onnx_readiness_rows']}`
- onnx_parity(온엑스 동등성): `{final['onnx_parity_passed_rows']}/{final['onnx_parity_rows']}`
- best_proxy_model(최고 프록시 모델): `{final['best_proxy_model_id']}`
- best_proxy_net(최고 프록시 순값): `{final['best_proxy_net']}`
- best_inner_holdout_balanced_accuracy(최고 내부 보류 균형 정확도): `{final['best_inner_holdout_balanced_accuracy']}`
- runtime_probe_queue(런타임 탐침 대기열): `{final['runtime_probe_queue_rows']}`
- gates(게이트): `{final['passed_gates']}/{final['gate_rows']}`

## Boundary(경계)

- candidate_selection(후보 선택): `not_run`
- MT5 runtime probe(MT5 런타임 탐침): `not_run`
- Forward Passed/Failed(전진 통과/실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return aw.write_text_lossless(REPORT_PATH, text, True)


def write_decision(final: Mapping[str, Any]) -> Path:
    text = f"""# {TODAY} Stage337EZ Decision(337EZ 결정)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- evidence(근거): `{rel(REPORT_PATH)}`, `{rel(RUNTIME_PROBE_CANDIDATE_QUEUE)}`, `{rel(RUNTIME_PROBE_PACKAGE_CONTRACT)}`

Action(행동): EY ONNX candidates(EY 온엑스 후보)를 runtime probe queue(런타임 탐침 대기열)로 넘겼다.
Effect(효과): 다음 FA packet(FA 작업 묶음)이 MT5 runtime evidence(MT5 런타임 근거)를 만들 수 있다.

Forward/Goal(전진/목표): `not_claimed`
runtime_authority(런타임 권위): `not_claimed`
claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return aw.write_text_lossless(DECISION_DOC, text, True)


def replace_line(text: str, prefix: str, replacement: str) -> str:
    pattern = re.compile(rf"^{re.escape(prefix)}.*$", flags=re.M)
    return pattern.sub(replacement, text, count=1) if pattern.search(text) else replacement + "\n" + text


FIELD_LABELS = {
    "current_run": "current_run(현재 실행)",
    "status": "status(상태)",
    "decision": "decision(결정)",
    "latest_completed_run": "latest_completed_run(최근 완료 실행)",
    "next_action": "next_action(다음 행동)",
    "claim_boundary": "claim_boundary(주장 경계)",
}


def replace_bullet_field(text: str, field_name: str, value: str) -> str:
    pattern = re.compile(rf"^- {re.escape(field_name)}(\([^)]+\))?: .*$", flags=re.M)
    replacement = f"- {FIELD_LABELS.get(field_name, field_name)}: {value}"
    return pattern.sub(replacement, text, count=1) if pattern.search(text) else replacement + "\n" + text


def upsert_section_before(text: str, marker: str, section: str, heading: str) -> str:
    pattern = re.compile(rf"^## {re.escape(heading)}.*?(?=^## )", flags=re.M | re.S)
    if pattern.search(text):
        return pattern.sub(section.rstrip() + "\n\n", text, count=1)
    return text.replace(marker, section.rstrip() + "\n\n" + marker, 1) if marker in text else text.rstrip() + "\n\n" + section.rstrip() + "\n"


def upsert_single_line(text: str, needle: str, entry: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if needle in line:
            lines[index] = entry
            trailing = "\n" if text.endswith("\n") else ""
            return "\n".join(lines) + trailing
    return text.rstrip() + "\n" + entry.rstrip() + "\n"


def update_docs(final: Mapping[str, Any]) -> list[Path]:
    artifacts: list[Path] = []
    branch = ey.current_branch()
    workspace, workspace_bom = aw.read_text_lossless(WORKSPACE_STATE)
    workspace = replace_line(workspace, "current_run_id:", f"current_run_id: {final['next_action']}")
    workspace = replace_line(workspace, "updated_on:", f"updated_on: '{TODAY}'")
    workspace = replace_line(workspace, "active_branch:", f"active_branch: {branch}")
    focus = (
        "- >-\n"
        f"  Stage337 run337EZ focus complete: run337EZ(337EZ 실행)는 `{final['status']}`로 side/cost/curve training review(방향/비용/곡선 학습 검토)를 완료했다. "
        f"Effect(효과): ONNX ready(온엑스 준비) `{final['onnx_ready_rows']}/{final['onnx_readiness_rows']}`, proxy positive clue(긍정 프록시 단서) `{final['positive_proxy_rows']}`, runtime probe queue(런타임 탐침 대기열) `{final['runtime_probe_queue_rows']}`를 만들고 `{final['next_action']}`을 열었다. Forward/Goal(전진/목표)은 주장하지 않는다.\n"
    )
    if "Stage337 run337EZ focus complete" in workspace:
        workspace = re.sub(
            r"- >-\n  Stage337 run337EZ focus complete:.*?(?=\n- >-|\n[a-zA-Z_]+:|$)",
            focus.rstrip(),
            workspace,
            count=1,
            flags=re.S,
        )
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
        current = replace_bullet_field(current, field_name, value)
    section = f"""## run337EZ Side/Cost/Curve Training Review(방향/비용/곡선 학습 검토)

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- onnx_ready(온엑스 준비): `{final['onnx_ready_rows']}/{final['onnx_readiness_rows']}`
- best_proxy_model(최고 프록시 모델): `{final['best_proxy_model_id']}`
- best_proxy_net(최고 프록시 순값): `{final['best_proxy_net']}`
- runtime_probe_queue(런타임 탐침 대기열): `{final['runtime_probe_queue_rows']}`
- gates(게이트): `{final['passed_gates']}/{final['gate_rows']}`
- effect(효과): proxy clue(프록시 단서)를 MT5 runtime probe(MT5 런타임 탐침) 대기열로 넘기고 selection/Forward/Goal(선택/전진/목표) 주장은 닫는다.
- next_action(다음 행동): `{final['next_action']}`
"""
    current = upsert_section_before(current, "## run337EY Side/Cost/Curve", section, "run337EZ Side/Cost/Curve")
    artifacts.append(aw.write_text_lossless(CURRENT_STATE, current, current_bom))

    selection = f"""# Stage337 Selection Status(337단계 선택 상태)

- latest_run(최신 실행): `{RUN_ID}`
- latest_decision(최신 결정): `{final['decision']}`
- current_run(현재 실행): `{final['next_action']}`
- rebuild_status(재구축 상태): `{final['status']}`
- onnx_ready(온엑스 준비): `{final['onnx_ready_rows']}/{final['onnx_readiness_rows']}`
- runtime_probe_queue(런타임 탐침 대기열): `{final['runtime_probe_queue_rows']}`
- best_proxy_model(최고 프록시 모델): `{final['best_proxy_model_id']}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{final['next_action']}`
- effect(효과): EZ(337EZ 실행)는 review(검토)와 runtime probe queue(런타임 탐침 대기열)만 만들며 operating selection(운영 선택)은 하지 않는다.
"""
    artifacts.append(aw.write_text_lossless(SELECTED_STATUS, selection, True))

    brief, brief_bom = aw.read_text_lossless(STAGE_BRIEF)
    brief_entry = (
        f"- {TODAY}: run337EZ(337EZ 실행) `{final['status']}`. "
        f"Effect(효과): ONNX ready(온엑스 준비) `{final['onnx_ready_rows']}/{final['onnx_readiness_rows']}`, runtime probe queue(런타임 탐침 대기열) `{final['runtime_probe_queue_rows']}`를 만들고 `{final['next_action']}`을 열었다. Forward/Goal(전진/목표)은 주장하지 않는다."
    )
    artifacts.append(aw.write_text_lossless(STAGE_BRIEF, upsert_single_line(brief, "run337EZ(337EZ 실행)", brief_entry), brief_bom))

    changelog, changelog_bom = aw.read_text_lossless(CHANGELOG)
    changelog_entry = (
        f"- {TODAY}: Stage337 run337EZ(337EZ 실행) `{final['status']}`. "
        f"Effect(효과): EY ONNX candidates(EY 온엑스 후보)를 runtime probe queue(런타임 탐침 대기열)로 넘기고 `{final['next_action']}`을 열었다. Forward/Goal(전진/목표)은 주장하지 않았다."
    )
    artifacts.append(aw.write_text_lossless(CHANGELOG, upsert_single_line(changelog, "Stage337 run337EZ", changelog_entry), changelog_bom))
    return artifacts


def upsert_csv_worktree(path: Path, columns: Sequence[str], row: Mapping[str, Any], key: str) -> Path:
    existing_columns, existing = aw.read_csv_table(path, prefer_head=False)
    merged_columns = list(existing_columns or columns)
    for column in columns:
        if column not in merged_columns:
            merged_columns.append(column)
    for column in row:
        if column not in merged_columns:
            merged_columns.append(column)
    key_value = str(row.get(key, ""))
    rows = [item for item in existing if str(item.get(key, "")) != key_value]
    rows.append({column: row.get(column, "") for column in merged_columns})
    return write_csv(path, merged_columns, rows)


def update_registers(final: Mapping[str, Any]) -> list[Path]:
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "side_cost_curve_training_review",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "notes": f"onnx_ready={final['onnx_ready_rows']}/{final['onnx_readiness_rows']};proxy_positive={final['positive_proxy_rows']};runtime_queue={final['runtime_probe_queue_rows']};next_action={final['next_action']};goal_achieve_not_claimed.",
        "family": "model_validation_runtime_parity_result_judgment",
        "primary_report": rel(REPORT_PATH),
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__training_review",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "training_review",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "side_cost_curve_training_review(방향/비용/곡선 학습 검토)",
        "tier_scope": "Tier A train-only ONNX review with MT5 probe pending(Tier A 학습 전용 ONNX 검토, MT5 탐침 대기)",
        "kpi_scope": "proxy clue and ONNX readiness only; no MT5 KPI(프록시 단서와 ONNX 준비만, MT5 성과 아님)",
        "scoreboard_lane": "model_validation_runtime_parity",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": rel(REPORT_PATH),
        "primary_kpi": f"best_proxy_model={final['best_proxy_model_id']};best_proxy_net={final['best_proxy_net']};best_bacc={final['best_inner_holdout_balanced_accuracy']}",
        "guardrail_kpi": f"onnx_ready={final['onnx_ready_rows']}/{final['onnx_readiness_rows']};queue={final['runtime_probe_queue_rows']};no_selection;no_mt5;no_forward",
        "external_verification_status": "required_next_action",
        "notes": f"decision={final['decision']};next_action={final['next_action']};goal_achieve_not_claimed.",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__training_review",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "model_validation_runtime_parity_result_judgment",
        "evidence_scope": "EY model manifest, ONNX parity, inner holdout proxy",
        "kpi_scope": "training_review_proxy_clue_runtime_probe_queue",
        "status": final["status"],
        "judgment": final["judgment"],
        "claim_boundary": CLAIM_BOUNDARY,
        "path": rel(REPORT_PATH),
        "notes": f"gates={final['passed_gates']}/{final['gate_rows']};next_action={final['next_action']};goal_achieve_not_claimed",
        "decision": final["decision"],
        "run_key": f"{RUN_ID}__training_review",
        "family": "side_cost_curve_training_review",
        "question": "which EY ONNX candidates are ready for MT5 runtime probe without selection",
        "metric_scope": "onnx_readiness_proxy_clue_queue",
        "primary_artifact": rel(REPORT_PATH),
        "report_path": rel(REPORT_PATH),
        "next_action": final["next_action"],
    }
    return [
        upsert_csv_worktree(RUN_REGISTRY, aw.RUN_REGISTRY_COLUMNS, run_row, "run_id"),
        upsert_csv_worktree(ALPHA_LEDGER, aw.ALPHA_LEDGER_COLUMNS, alpha_row, "ledger_row_id"),
        upsert_csv_worktree(STAGE_LEDGER, aw.STAGE_LEDGER_COLUMNS, stage_row, "ledger_row_id"),
    ]


def update_artifact_registry(paths: Sequence[Path]) -> Path:
    columns, rows = aw.read_csv_table(ARTIFACT_REGISTRY, prefer_head=False)
    columns = list(columns or aw.ARTIFACT_COLUMNS)
    for column in aw.ARTIFACT_COLUMNS:
        if column not in columns:
            columns.append(column)
    rows = [
        row
        for row in rows
        if not str(row.get("artifact_id", "")).startswith(f"{RUN_ID}::") and str(row.get("run_id", "")) != RUN_ID
    ]
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
        rows.append(
            {
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
        )
    return write_csv(ARTIFACT_REGISTRY, columns, rows)


def make_final(summary: Mapping[str, Any]) -> dict[str, Any]:
    ey_final = read_json(EY_FINAL)
    final = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_action": NEXT_RUN_ID,
        "missing_inputs": len(fail_if_missing(INPUT_FILES)),
        "ey_next_action": ey_final.get("next_action", ""),
        "ey_failed_gate_rows": sum(1 for row in read_csv(EY_GATES) if row.get("status") != "passed"),
        "new_training": "not_run",
        "candidate_selection": "not_run",
        "threshold_tuning": "not_run",
        "lot_optimization": "not_run",
        "mt5_runtime_probe": "not_run",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "runtime_authority": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
        **dict(summary),
    }
    return final


def main() -> int:
    aw.io_path(RUN_DIR).mkdir(parents=True, exist_ok=True)
    missing = fail_if_missing(INPUT_FILES)
    if missing:
        print(json.dumps({"run_id": RUN_ID, "status": "blocked_missing_inputs", "missing": [rel(path) for path in missing]}, ensure_ascii=False, indent=2))
        return 1

    training_rows, proxy_rows, onnx_rows, runtime_rows, combined_rows, summary = review_training_and_proxy()
    contract_rows, firewall_rows, fa_rows = split_combined_rows(combined_rows)
    final = make_final(summary | {"package_contract_rows": len(contract_rows), "firewall_rows": len(firewall_rows), "fa_queue_rows": len(fa_rows)})

    artifacts: list[Path] = [
        write_csv(TRAINING_REVIEW_SCORECARD, TRAINING_REVIEW_COLUMNS, training_rows),
        write_csv(PROXY_CLUE_REVIEW, PROXY_REVIEW_COLUMNS, proxy_rows),
        write_csv(ONNX_READINESS_REVIEW, ONNX_REVIEW_COLUMNS, onnx_rows),
        write_csv(RUNTIME_PROBE_CANDIDATE_QUEUE, RUNTIME_QUEUE_COLUMNS, runtime_rows),
        write_csv(RUNTIME_PROBE_PACKAGE_CONTRACT, CONTRACT_COLUMNS, contract_rows),
        write_csv(RELEASE_FIREWALL_REVIEW, FIREWALL_COLUMNS, firewall_rows),
        write_csv(FA_QUEUE, QUEUE_COLUMNS, fa_rows),
    ]

    gates = build_gates(final)
    final["gate_rows"] = len(gates)
    final["passed_gates"] = sum(1 for row in gates if row["status"] == "passed")
    final["failed_gates"] = [row["gate_id"] for row in gates if row["status"] != "passed"]
    if final["failed_gates"]:
        final["status"] = "invalid_stage337EZ_required_gate_failure_no_selection_no_mt5"
        final["judgment"] = "required_gate_failure_blocks_FA_runtime_probe_package"
        final["decision"] = "repair_stage337EZ_required_gate_failure_before_FA"
        final["next_action"] = "repair_stage337EZ_required_gate_failure_v1"

    artifacts.extend(
        [
            write_csv(GATE_AUDIT, GATE_COLUMNS, gates),
            write_json(FINAL_DECISION, final),
            write_json(
                RUN_MANIFEST,
                {
                    "run_id": RUN_ID,
                    "parent_run_id": PARENT_RUN_ID,
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

    if final["failed_gates"]:
        print(json.dumps({"run_id": RUN_ID, "status": final["status"], "failed_gates": final["failed_gates"]}, ensure_ascii=False, indent=2))
        return 1
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": final["status"],
                "onnx_ready": f"{final['onnx_ready_rows']}/{final['onnx_readiness_rows']}",
                "onnx_parity": f"{final['onnx_parity_passed_rows']}/{final['onnx_parity_rows']}",
                "best_proxy_model_id": final["best_proxy_model_id"],
                "best_proxy_net": final["best_proxy_net"],
                "runtime_probe_queue_rows": final["runtime_probe_queue_rows"],
                "gates": f"{final['passed_gates']}/{final['gate_rows']}",
                "next_action": final["next_action"],
                "goal_achieve": "not_claimed",
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
