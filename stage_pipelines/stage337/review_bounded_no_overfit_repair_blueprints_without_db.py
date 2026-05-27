from __future__ import annotations

import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from stage_pipelines.stage337 import materialize_bounded_no_overfit_repair_blueprints_from_reviewed_inputs_without_db as bc


aw = bc.aw

TODAY = "2026-05-27"
STAGE_ID = bc.STAGE_ID
RUN_NUMBER = "run337BD"
RUN_ID = "run337BD_review_bounded_no_overfit_repair_blueprints_without_db_v1"
PARENT_RUN_ID = bc.RUN_ID
NEXT_RUN_ID = "run337BE_materialize_bounded_repair_implementation_preflight_without_db_v1"
STATUS = "completed_stage337BD_bounded_no_overfit_blueprints_reviewed_ready_for_implementation_preflight_no_training_no_selection"
JUDGMENT = "bounded_blueprints_review_pass_open_implementation_preflight_without_forward_or_runtime_claim"
DECISION = "stage337BD_open_run337BE_materialize_bounded_repair_implementation_preflight_no_training_no_selection"
CLAIM_BOUNDARY = (
    "research_development_only_stage337BD_bounded_blueprint_review_without_db_cp322a_frozen_"
    "no_model_training_no_threshold_retuning_no_db_rule_rewrite_no_lot_optimization_no_candidate_selection_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = bc.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = bc.REVIEWS_DIR
REPORT_PATH = REVIEWS_DIR / "run337BD_bounded_no_overfit_blueprint_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-27_stage337BD_bounded_no_overfit_blueprint_review.md"
SELECTED_STATUS = bc.SELECTED_STATUS
STAGE_BRIEF = bc.STAGE_BRIEF
WORKSPACE_STATE = bc.WORKSPACE_STATE
CURRENT_STATE = bc.CURRENT_STATE
CHANGELOG = bc.CHANGELOG
RUN_REGISTRY = bc.RUN_REGISTRY
ALPHA_LEDGER = bc.ALPHA_LEDGER
ARTIFACT_REGISTRY = bc.ARTIFACT_REGISTRY
STAGE_LEDGER = bc.STAGE_LEDGER

RUN337BC_DIR = STAGE_DIR / "02_runs" / "run337BC"
BC_FINAL = RUN337BC_DIR / "final_decision.json"
BC_MANIFEST = RUN337BC_DIR / "run_manifest.json"
BC_BLUEPRINT = RUN337BC_DIR / "bounded_repair_blueprint_matrix.csv"
BC_FREEZE = RUN337BC_DIR / "cp322a_freeze_contract.csv"
BC_PROTOCOL = RUN337BC_DIR / "bounded_execution_protocol_matrix.csv"
BC_FALSIFICATION = RUN337BC_DIR / "blueprint_falsification_gate_matrix.csv"
BC_PROXY = RUN337BC_DIR / "proxy_mt5_blueprint_measurement_plan.csv"
BC_SOURCE = RUN337BC_DIR / "blueprint_source_identity.csv"
BC_QUEUE = RUN337BC_DIR / "run337BD_review_queue.csv"
BC_GATE_AUDIT = RUN337BC_DIR / "required_gate_coverage_audit.csv"
BC_EXPERIMENT_RECEIPT = RUN337BC_DIR / "experiment_design_receipt.json"
BC_DATA_RECEIPT = RUN337BC_DIR / "data_integrity_receipt.json"
BC_MODEL_RECEIPT = RUN337BC_DIR / "model_validation_receipt.json"
BC_RUNTIME_RECEIPT = RUN337BC_DIR / "runtime_parity_receipt.json"
BC_ARTIFACT_RECEIPT = RUN337BC_DIR / "artifact_lineage_receipt.json"
BC_JUDGMENT_RECEIPT = RUN337BC_DIR / "result_judgment_receipt.json"

BLUEPRINT_REVIEW = RUN_DIR / "blueprint_review_matrix.csv"
FREEZE_REVIEW = RUN_DIR / "freeze_contract_review.csv"
PROTOCOL_REVIEW = RUN_DIR / "execution_protocol_review.csv"
FALSIFICATION_REVIEW = RUN_DIR / "falsification_gate_review.csv"
PROXY_BOUNDARY_REVIEW = RUN_DIR / "proxy_mt5_boundary_review.csv"
SOURCE_REVIEW = RUN_DIR / "source_identity_review.csv"
IMPLEMENTATION_BOUNDARY = RUN_DIR / "implementation_boundary_matrix.csv"
RUN337BE_QUEUE = RUN_DIR / "run337BE_implementation_preflight_queue.csv"
REQUIRED_GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment_design_receipt.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
ARTIFACT_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (
    BC_FINAL,
    BC_MANIFEST,
    BC_BLUEPRINT,
    BC_FREEZE,
    BC_PROTOCOL,
    BC_FALSIFICATION,
    BC_PROXY,
    BC_SOURCE,
    BC_QUEUE,
    BC_GATE_AUDIT,
    BC_EXPERIMENT_RECEIPT,
    BC_DATA_RECEIPT,
    BC_MODEL_RECEIPT,
    BC_RUNTIME_RECEIPT,
    BC_ARTIFACT_RECEIPT,
    BC_JUDGMENT_RECEIPT,
)
OUTPUT_FILES = (
    BLUEPRINT_REVIEW,
    FREEZE_REVIEW,
    PROTOCOL_REVIEW,
    FALSIFICATION_REVIEW,
    PROXY_BOUNDARY_REVIEW,
    SOURCE_REVIEW,
    IMPLEMENTATION_BOUNDARY,
    RUN337BE_QUEUE,
    REQUIRED_GATE_AUDIT,
    EXPERIMENT_RECEIPT,
    DATA_RECEIPT,
    MODEL_RECEIPT,
    RUNTIME_RECEIPT,
    ARTIFACT_RECEIPT,
    JUDGMENT_RECEIPT,
    FINAL_DECISION,
    RUN_MANIFEST,
)

BLUEPRINT_REVIEW_COLUMNS = (
    "review_id",
    "blueprint_id",
    "source_design_id",
    "repair_axis",
    "allowed_input_paths_checked",
    "freeze_boundary_ok",
    "mutable_scope_ok",
    "evidence_plan_ok",
    "negative_control_ok",
    "proxy_mt5_boundary_ok",
    "overfit_rejection_ok",
    "review_status",
    "effect",
    "claim_boundary",
)
FREEZE_REVIEW_COLUMNS = (
    "review_id",
    "freeze_id",
    "subject",
    "source_identity",
    "hash_or_value",
    "freeze_status",
    "forbidden_change",
    "identity_present",
    "freeze_preserved",
    "forbidden_change_declared",
    "review_status",
    "effect",
    "claim_boundary",
)
PROTOCOL_REVIEW_COLUMNS = (
    "review_id",
    "protocol_id",
    "source_blueprint_id",
    "required_artifacts_ok",
    "preflight_checks_ok",
    "measurement_scope_ok",
    "allowed_decision_use_ok",
    "invalid_if_ok",
    "next_run_owner_ok",
    "review_status",
    "effect",
    "claim_boundary",
)
FALSIFICATION_REVIEW_COLUMNS = (
    "review_id",
    "gate_id",
    "source_blueprint_id",
    "gate_family",
    "blocks_threshold_lot_db_date_trade_proxy",
    "abort_condition_declared",
    "evidence_artifact_exists",
    "materialized_status_ok",
    "review_status",
    "effect",
    "claim_boundary",
)
PROXY_BOUNDARY_REVIEW_COLUMNS = (
    "review_id",
    "plan_id",
    "source_blueprint_id",
    "proxy_artifact_exists",
    "mt5_artifact_exists",
    "proxy_allowed_signal_only",
    "mt5_kpi_authority_required",
    "mismatch_aborts_forward_claim",
    "proxy_kpi_authority_forbidden",
    "review_status",
    "effect",
    "claim_boundary",
)
SOURCE_REVIEW_COLUMNS = (
    "review_id",
    "source_id",
    "path",
    "exists",
    "row_count",
    "recorded_sha256",
    "current_sha256",
    "hash_matches",
    "review_status",
    "effect",
    "claim_boundary",
)
IMPLEMENTATION_BOUNDARY_COLUMNS = (
    "boundary_id",
    "source_blueprint_id",
    "allowed_next_work",
    "forbidden_next_work",
    "required_preflight_evidence",
    "required_before_mt5_forward",
    "proxy_role",
    "mt5_role",
    "implementation_status",
    "effect",
    "claim_boundary",
)
QUEUE_COLUMNS = (
    "queue_id",
    "next_run_id",
    "review_subject",
    "inputs_to_review",
    "must_confirm",
    "must_reject_if",
    "expected_outputs",
    "priority",
    "effect",
    "claim_boundary",
)
GATE_COLUMNS = aw.GATE_COLUMNS


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def status_text(ok: bool) -> str:
    return "passed" if ok else "failed"


def repo_path(raw: str) -> Path:
    value = str(raw or "").strip()
    path = Path(value)
    if path.is_absolute():
        return path
    return ROOT / value.replace("/", "\\")


def split_repo_paths(value: str) -> list[str]:
    paths: list[str] = []
    for chunk in str(value or "").replace("\n", ";").split(";"):
        item = chunk.strip()
        if item.startswith(("stages/", "docs/", "data/", "foundation/", "stage_pipelines/")):
            paths.append(item)
    return paths


def paths_exist(value: str) -> bool:
    paths = split_repo_paths(value)
    return bool(paths) and all(aw.path_exists(repo_path(path)) for path in paths)


def row_count(path: Path) -> int:
    if not aw.path_exists(path):
        return 0
    if path.suffix.lower() == ".json":
        return len(aw.read_json(path))
    return len(aw.read_csv(path))


def require_inputs() -> None:
    missing = [aw.rel(path) for path in INPUT_FILES if not aw.path_exists(path)]
    if missing:
        raise FileNotFoundError("missing run337BD inputs: " + "; ".join(missing))


def load_inputs() -> dict[str, Any]:
    require_inputs()
    return {
        "bc_final": aw.read_json(BC_FINAL),
        "bc_manifest": aw.read_json(BC_MANIFEST),
        "blueprints": aw.read_csv(BC_BLUEPRINT),
        "freeze": aw.read_csv(BC_FREEZE),
        "protocols": aw.read_csv(BC_PROTOCOL),
        "falsification": aw.read_csv(BC_FALSIFICATION),
        "proxy": aw.read_csv(BC_PROXY),
        "sources": aw.read_csv(BC_SOURCE),
        "queue": aw.read_csv(BC_QUEUE),
        "bc_gate_audit": aw.read_csv(BC_GATE_AUDIT),
        "bc_receipts": [
            aw.read_json(BC_EXPERIMENT_RECEIPT),
            aw.read_json(BC_DATA_RECEIPT),
            aw.read_json(BC_MODEL_RECEIPT),
            aw.read_json(BC_RUNTIME_RECEIPT),
            aw.read_json(BC_ARTIFACT_RECEIPT),
            aw.read_json(BC_JUDGMENT_RECEIPT),
        ],
    }


def ok(value: bool) -> str:
    return "true" if value else "false"


def lower_text(*values: Any) -> str:
    return " ".join(str(value or "") for value in values).lower()


def count_status(rows: Sequence[Mapping[str, Any]], value: str) -> int:
    return sum(1 for row in rows if str(row.get("review_status", "")).startswith(value))


def build_blueprint_review(blueprints: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in blueprints:
        text = lower_text(row)
        allowed_input_ok = paths_exist(row.get("allowed_inputs", ""))
        freeze_ok = all(
            token in text
            for token in ("onnx", "feature order", "d/b", "score threshold", "risk logic", "lot", "atr", "runtime handoff")
        )
        mutable_ok = "blueprint text" in text and "future review queue only" in text
        evidence_ok = "mt5 kpi" in text and "proxy mismatch" in text and "no-lookahead" in text
        negative_ok = paths_exist(row.get("negative_controls", ""))
        proxy_ok = "proxy checks signal" in text and "mt5 owns kpi" in text
        rejection_ok = bool(row.get("overfit_rejection_rule")) and lower_text(row.get("overfit_rejection_rule")) == lower_text(row.get("failure_evidence"))
        status_ok = str(row.get("status", "")).startswith("materialized_blueprint_for_review")
        accepted = all((allowed_input_ok, freeze_ok, mutable_ok, evidence_ok, negative_ok, proxy_ok, rejection_ok, status_ok))
        rows.append(
            {
                "review_id": f"{RUN_NUMBER}_{row.get('blueprint_id')}_review",
                "blueprint_id": row.get("blueprint_id", ""),
                "source_design_id": row.get("source_design_id", ""),
                "repair_axis": row.get("repair_axis", ""),
                "allowed_input_paths_checked": ok(allowed_input_ok),
                "freeze_boundary_ok": ok(freeze_ok),
                "mutable_scope_ok": ok(mutable_ok),
                "evidence_plan_ok": ok(evidence_ok),
                "negative_control_ok": ok(negative_ok),
                "proxy_mt5_boundary_ok": ok(proxy_ok),
                "overfit_rejection_ok": ok(rejection_ok),
                "review_status": "accepted_for_implementation_preflight(구현 사전점검 허용)" if accepted else "rejected_repair_blueprint_review(수리 청사진 검토 거부)",
                "effect": "keeps each blueprint bounded before implementation(각 청사진을 구현 전에 제한 상태로 유지)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_freeze_review(freeze_rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in freeze_rows:
        identity_present = bool(str(row.get("hash_or_value", "")).strip())
        freeze_preserved = str(row.get("freeze_status", "")).startswith("frozen_not_modified")
        forbidden_declared = bool(str(row.get("forbidden_change", "")).strip())
        accepted = identity_present and freeze_preserved and forbidden_declared
        rows.append(
            {
                "review_id": f"{RUN_NUMBER}_{row.get('freeze_id')}_freeze_review",
                "freeze_id": row.get("freeze_id", ""),
                "subject": row.get("subject", ""),
                "source_identity": row.get("source_identity", ""),
                "hash_or_value": row.get("hash_or_value", ""),
                "freeze_status": row.get("freeze_status", ""),
                "forbidden_change": row.get("forbidden_change", ""),
                "identity_present": ok(identity_present),
                "freeze_preserved": ok(freeze_preserved),
                "forbidden_change_declared": ok(forbidden_declared),
                "review_status": "freeze_preserved(고정 보존)" if accepted else "freeze_review_failed(고정 검토 실패)",
                "effect": "prevents cp322A identity or trading surface drift(322A 정체성과 거래 표면 이탈을 막음)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_protocol_review(protocols: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in protocols:
        invalid_text = lower_text(row.get("invalid_if"))
        measurement_text = lower_text(row.get("measurement_scope"))
        allowed_text = lower_text(row.get("allowed_decision_use"))
        preflight_text = lower_text(row.get("preflight_checks"))
        required_ok = paths_exist(row.get("required_artifacts", ""))
        preflight_ok = all(token in preflight_text for token in ("freeze contract", "no-lookahead", "proxy-mt5", "negative controls"))
        measurement_ok = all(token in measurement_text for token in ("mt5 kpi", "proxy mismatch", "cost stress", "curve pocket", "trade density"))
        decision_ok = "review" in allowed_text and "implementation design only" in allowed_text
        invalid_ok = all(token in invalid_text for token in ("training", "threshold", "lot", "d-b", "date", "trade-index"))
        owner_ok = row.get("next_run_owner") == RUN_ID
        status_ok = str(row.get("status", "")).startswith("protocol_materialized_for_review")
        accepted = all((required_ok, preflight_ok, measurement_ok, decision_ok, invalid_ok, owner_ok, status_ok))
        rows.append(
            {
                "review_id": f"{RUN_NUMBER}_{row.get('protocol_id')}_review",
                "protocol_id": row.get("protocol_id", ""),
                "source_blueprint_id": row.get("source_blueprint_id", ""),
                "required_artifacts_ok": ok(required_ok),
                "preflight_checks_ok": ok(preflight_ok),
                "measurement_scope_ok": ok(measurement_ok),
                "allowed_decision_use_ok": ok(decision_ok),
                "invalid_if_ok": ok(invalid_ok),
                "next_run_owner_ok": ok(owner_ok),
                "review_status": "protocol_review_accepted(절차 검토 수락)" if accepted else "protocol_review_failed(절차 검토 실패)",
                "effect": "keeps implementation entry tied to predeclared measurement and abort rules(구현 진입을 사전 선언 측정과 중단 규칙에 묶음)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_falsification_review(gates: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in gates:
        block_text = lower_text(row.get("blocks_overfit_path"))
        abort_text = lower_text(row.get("must_fail_or_abort_if"))
        evidence_path = repo_path(row.get("evidence_artifact", ""))
        blocks_all = all(token in block_text for token in ("threshold", "lot", "d-b", "date", "trade-index", "proxy-kpi"))
        abort_ok = "true" in abort_text and "forbidden change" in abort_text
        evidence_ok = aw.path_exists(evidence_path)
        status_ok = str(row.get("status", "")).startswith("materialized_falsification_gate")
        accepted = blocks_all and abort_ok and evidence_ok and status_ok
        rows.append(
            {
                "review_id": f"{RUN_NUMBER}_{row.get('gate_id')}_review",
                "gate_id": row.get("gate_id", ""),
                "source_blueprint_id": row.get("source_blueprint_id", ""),
                "gate_family": row.get("gate_family", ""),
                "blocks_threshold_lot_db_date_trade_proxy": ok(blocks_all),
                "abort_condition_declared": ok(abort_ok),
                "evidence_artifact_exists": ok(evidence_ok),
                "materialized_status_ok": ok(status_ok),
                "review_status": "falsification_gate_active(반증 게이트 활성)" if accepted else "falsification_gate_review_failed(반증 게이트 검토 실패)",
                "effect": "turns hidden overfit shortcuts into explicit abort conditions(숨은 과적합 지름길을 명시 중단 조건으로 바꿈)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_proxy_boundary_review(plans: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in plans:
        proxy_allowed = lower_text(row.get("proxy_allowed_use"))
        mt5_required = lower_text(row.get("mt5_required_use"))
        mismatch_action = lower_text(row.get("mismatch_action"))
        not_allowed = lower_text(row.get("not_allowed_use"))
        proxy_exists = aw.path_exists(repo_path(row.get("proxy_artifact", "")))
        mt5_exists = aw.path_exists(repo_path(row.get("mt5_artifact", "")))
        signal_only = all(token in proxy_allowed for token in ("schema", "signal", "mismatch detection")) and not any(
            token in proxy_allowed for token in ("profit", "pf", "drawdown", "dd")
        )
        mt5_kpi = all(token in mt5_required for token in ("profit", "pf", "drawdown", "expectancy", "trade count"))
        mismatch_ok = "abort forward claim" in mismatch_action and "parity repair" in mismatch_action
        proxy_kpi_forbidden = all(token in not_allowed for token in ("proxy net", "pf", "dd", "forward passed", "forward failed"))
        accepted = all((proxy_exists, mt5_exists, signal_only, mt5_kpi, mismatch_ok, proxy_kpi_forbidden))
        rows.append(
            {
                "review_id": f"{RUN_NUMBER}_{row.get('plan_id')}_review",
                "plan_id": row.get("plan_id", ""),
                "source_blueprint_id": row.get("source_blueprint_id", ""),
                "proxy_artifact_exists": ok(proxy_exists),
                "mt5_artifact_exists": ok(mt5_exists),
                "proxy_allowed_signal_only": ok(signal_only),
                "mt5_kpi_authority_required": ok(mt5_kpi),
                "mismatch_aborts_forward_claim": ok(mismatch_ok),
                "proxy_kpi_authority_forbidden": ok(proxy_kpi_forbidden),
                "review_status": "proxy_mt5_boundary_preserved(프록시-MT5 경계 보존)" if accepted else "proxy_mt5_boundary_failed(프록시-MT5 경계 실패)",
                "effect": "keeps proxy useful for mismatch checks without turning it into KPI authority(프록시는 불일치 확인에 쓰되 KPI 권위가 되지 않게 함)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_source_review(source_rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in source_rows:
        path = repo_path(row.get("path", ""))
        exists = aw.path_exists(path)
        current_sha = aw.sha256_file(path) if exists else ""
        recorded_sha = row.get("sha256", "")
        hash_matches = exists and current_sha == recorded_sha
        count_ok = int(str(row.get("row_count", "0") or "0")) > 0
        connected = str(row.get("status", "")).startswith("connected")
        accepted = exists and hash_matches and count_ok and connected
        rows.append(
            {
                "review_id": f"{RUN_NUMBER}_{row.get('source_id')}_source_review",
                "source_id": row.get("source_id", ""),
                "path": row.get("path", ""),
                "exists": ok(exists),
                "row_count": row.get("row_count", ""),
                "recorded_sha256": recorded_sha,
                "current_sha256": current_sha,
                "hash_matches": ok(hash_matches),
                "review_status": "source_identity_verified(원천 정체성 확인)" if accepted else "source_identity_review_failed(원천 정체성 검토 실패)",
                "effect": "keeps reviewed blueprints tied to the same source files(검토 청사진을 같은 원천 파일에 묶음)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_implementation_boundary(blueprints: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in blueprints:
        rows.append(
            {
                "boundary_id": f"{RUN_NUMBER}_{row.get('blueprint_id')}_implementation_boundary",
                "source_blueprint_id": row.get("blueprint_id", ""),
                "allowed_next_work": "stage-local implementation preflight(단계 로컬 구현 사전점검); schema adapters(스키마 어댑터); measurement harness(측정 하네스); report templates(보고 템플릿)",
                "forbidden_next_work": "model training(모델 학습); threshold retuning(임계값 재조정); D/B rule rewrite(D/B 규칙 재작성); lot optimization(로트 최적화); candidate selection(후보 선택); date/trade-index rule(날짜/거래번호 규칙); proxy KPI authority(프록시 KPI 권위)",
                "required_preflight_evidence": f"{aw.rel(BLUEPRINT_REVIEW)};{aw.rel(FREEZE_REVIEW)};{aw.rel(PROXY_BOUNDARY_REVIEW)};{aw.rel(REQUIRED_GATE_AUDIT)}",
                "required_before_mt5_forward": "compile receipt(컴파일 영수증); runtime handoff hash check(런타임 인계 해시 확인); proxy expected vs MT5 probe difference table(프록시 예상값 대 MT5 탐침 차이표)",
                "proxy_role": "schema/signal/mismatch only(스키마/신호/불일치 전용)",
                "mt5_role": "future KPI authority only after fresh tester evidence(신규 테스터 근거 이후 KPI 권위 전용)",
                "implementation_status": "preflight_open_not_implemented(사전점검 개방, 미구현)",
                "effect": "allows the next run to build only a bounded preflight package(다음 실행이 제한된 사전점검 패키지만 만들게 함)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_next_queue() -> list[dict[str, Any]]:
    return [
        {
            "queue_id": "run337BE_implementation_preflight",
            "next_run_id": NEXT_RUN_ID,
            "review_subject": "bounded repair implementation preflight(제한 수리 구현 사전점검)",
            "inputs_to_review": ";".join(aw.rel(path) for path in (BLUEPRINT_REVIEW, FREEZE_REVIEW, PROTOCOL_REVIEW, FALSIFICATION_REVIEW, PROXY_BOUNDARY_REVIEW, IMPLEMENTATION_BOUNDARY)),
            "must_confirm": "cp322A freeze(322A 고정); no training(학습 없음); no threshold retune(임계값 재조정 없음); proxy-MT5 boundary(프록시-MT5 경계); implementation preflight only(구현 사전점검 전용)",
            "must_reject_if": "model training, threshold, lot, D/B, date, trade-index, candidate selection, proxy KPI authority appears(모델 학습/임계값/로트/D-B/날짜/거래번호/후보 선택/프록시 KPI 권위 등장)",
            "expected_outputs": "implementation preflight package, hash checks, proxy-MT5 comparison plan, no forward decision(구현 사전점검 패키지/해시 확인/프록시-MT5 비교 계획/전진 판정 없음)",
            "priority": "P0",
            "effect": "moves from review to bounded preflight without changing the trading surface(거래 표면을 바꾸지 않고 검토에서 제한 사전점검으로 이동)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def build_gates(
    src: Mapping[str, Any],
    blueprint_review: Sequence[Mapping[str, Any]],
    freeze_review: Sequence[Mapping[str, Any]],
    protocol_review: Sequence[Mapping[str, Any]],
    falsification_review: Sequence[Mapping[str, Any]],
    proxy_review: Sequence[Mapping[str, Any]],
    source_review: Sequence[Mapping[str, Any]],
    implementation_boundary: Sequence[Mapping[str, Any]],
    queue: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    parent_gates = src["bc_gate_audit"]
    parent_gates_passed = sum(1 for row in parent_gates if row.get("status") == "passed")
    blueprint_passed = count_status(blueprint_review, "accepted_for_implementation_preflight")
    freeze_passed = count_status(freeze_review, "freeze_preserved")
    protocol_passed = count_status(protocol_review, "protocol_review_accepted")
    falsification_passed = count_status(falsification_review, "falsification_gate_active")
    proxy_passed = count_status(proxy_review, "proxy_mt5_boundary_preserved")
    source_passed = count_status(source_review, "source_identity_verified")
    boundary_text = lower_text(implementation_boundary)
    forbidden_terms_declared = all(
        token in boundary_text
        for token in ("model training", "threshold retuning", "d/b rule rewrite", "lot optimization", "candidate selection", "proxy kpi authority")
    )
    claims_preserved = (
        src["bc_final"].get("forward_passed") == "not_claimed"
        and src["bc_final"].get("forward_failed") == "not_claimed"
        and src["bc_final"].get("runtime_authority") == "not_claimed"
        and src["bc_final"].get("goal_achieve") == "not_claimed"
    )
    gates = [
        (
            "bd_gate_parent_blueprint_package_loaded",
            bool(src["bc_final"]) and src["bc_final"].get("next_action") == RUN_ID,
            f"parent_next={src['bc_final'].get('next_action')};blueprints={len(src['blueprints'])}",
            "run337BC package points to run337BD(337BC 패키지가 337BD를 가리킴)",
        ),
        (
            "bd_gate_parent_gates_passed",
            parent_gates_passed == len(parent_gates) and parent_gates_passed > 0,
            f"parent_gates={parent_gates_passed}/{len(parent_gates)}",
            "all run337BC gates passed(337BC 모든 게이트 통과)",
        ),
        (
            "bd_gate_blueprint_review_accepts_five",
            blueprint_passed == 5 == len(blueprint_review),
            f"blueprint_reviews={blueprint_passed}/{len(blueprint_review)}",
            "five blueprints accepted for preflight(청사진 5개 사전점검 허용)",
        ),
        (
            "bd_gate_freeze_contract_preserved",
            freeze_passed == len(freeze_review) >= 9,
            f"freeze_reviews={freeze_passed}/{len(freeze_review)}",
            "cp322A freeze contract preserved(322A 고정 계약 보존)",
        ),
        (
            "bd_gate_execution_protocol_review_accepts_five",
            protocol_passed == 5 == len(protocol_review),
            f"protocol_reviews={protocol_passed}/{len(protocol_review)}",
            "five execution protocols accepted(실행 절차 5개 수락)",
        ),
        (
            "bd_gate_falsification_review_active",
            falsification_passed == len(falsification_review) >= 30,
            f"falsification_reviews={falsification_passed}/{len(falsification_review)}",
            "all falsification gates active(모든 반증 게이트 활성)",
        ),
        (
            "bd_gate_proxy_mt5_boundary_preserved",
            proxy_passed == 5 == len(proxy_review),
            f"proxy_boundary={proxy_passed}/{len(proxy_review)}",
            "proxy signal only and MT5 KPI authority preserved(프록시는 신호 전용, MT5 KPI 권위 보존)",
        ),
        (
            "bd_gate_source_identity_hash_verified",
            source_passed == len(source_review) and source_passed > 0,
            f"sources={source_passed}/{len(source_review)}",
            "source hashes still match(원천 해시 일치 유지)",
        ),
        (
            "bd_gate_implementation_boundary_conservative",
            len(implementation_boundary) == 5 and forbidden_terms_declared,
            f"boundaries={len(implementation_boundary)};forbidden_terms_declared={forbidden_terms_declared}",
            "next implementation preflight remains bounded(다음 구현 사전점검이 제한 상태 유지)",
        ),
        (
            "bd_gate_next_queue_ready",
            len(queue) == 1 and queue[0].get("next_run_id") == NEXT_RUN_ID,
            f"queue={len(queue)};next={NEXT_RUN_ID}",
            "run337BE queue ready(337BE 대기열 준비)",
        ),
        (
            "bd_gate_no_forward_runtime_goal_claim",
            claims_preserved,
            "Forward/Runtime/Goal not claimed(전진/런타임/목표 미주장)",
            "claim boundary preserved(주장 경계 보존)",
        ),
    ]
    return [
        {
            "gate_id": gate_id,
            "status": status_text(passed),
            "observed": observed,
            "expected": expected,
            "effect": "blocks implementation preflight unless review evidence is complete and bounded(검토 근거가 완전하고 제한되어야 구현 사전점검을 엶)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for gate_id, passed, observed, expected in gates
    ]


def write_receipts(final: Mapping[str, Any]) -> list[Path]:
    receipts = [
        (
            EXPERIMENT_RECEIPT,
            {
                "hypothesis": "run337BC bounded blueprints can be reviewed without changing cp322A(337BC 제한 청사진은 cp322A를 바꾸지 않고 검토할 수 있다)",
                "decision_use": "open implementation preflight only(구현 사전점검만 개방)",
                "control_variables": "cp322A ONNX, adapter package, feature order, D/B surface, score threshold, risk, lot, ATR SL/TP, runtime handoff fixed(322A ONNX/어댑터 패키지/피처 순서/D-B 표면/점수 임계값/위험/로트/ATR 손절익절/런타임 인계 고정)",
                "changed_variables": "review artifacts and next queue only(검토 산출물과 다음 대기열만 변경)",
                "success_criteria": "all review gates pass with no Forward or runtime claim(모든 검토 게이트 통과 및 전진/런타임 주장 없음)",
                "failure_criteria": "any path opens training, retune, D/B rewrite, lot optimization, date pocket, trade-index, or proxy KPI authority(학습/재조정/D-B 재작성/로트 최적화/날짜 포켓/거래번호/프록시 KPI 권위가 열리면 실패)",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            DATA_RECEIPT,
            {
                "data_source": [aw.rel(path) for path in INPUT_FILES],
                "time_axis": "as-of and predeclared review evidence only(시점 기준 및 사전 선언 검토 근거 전용)",
                "sample_scope": "run337BC blueprint package, no new broker data used(337BC 청사진 패키지, 신규 브로커 데이터 미사용)",
                "feature_label_boundary": "date pocket, trade index, realized PnL, realized drawdown cannot become features(날짜 포켓/거래번호/실현 손익/실현 손실폭은 피처가 될 수 없음)",
                "integrity_judgment": "source hashes verified for review-only use(검토 전용 사용을 위해 원천 해시 확인)",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            MODEL_RECEIPT,
            {
                "model_family": "existing cp322A frozen ONNX research artifact(기존 cp322A 고정 ONNX 연구 산출물)",
                "threshold_policy": "fixed; no search, calibration, or retune in run337BD(고정, 337BD에서 탐색/보정/재조정 없음)",
                "overfit_risk": "implementation preflight could become retune unless bounded(제한하지 않으면 구현 사전점검이 재조정으로 바뀔 수 있음)",
                "validation_judgment": "blueprint review only, not candidate selection(청사진 검토 전용, 후보 선택 아님)",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            RUNTIME_RECEIPT,
            {
                "research_path": aw.rel(__file__),
                "runtime_path": "not modified in run337BD(337BD에서 수정 없음)",
                "shared_contract": "proxy checks schema/signal/mismatch; MT5 owns KPI(프록시는 스키마/신호/불일치 확인, MT5가 KPI 담당)",
                "known_difference_policy": "proxy expected values must be compared with MT5 probe values before usability judgment(프록시 예상값은 사용성 판단 전 MT5 탐침값과 비교해야 함)",
                "runtime_claim_boundary": "no runtime authority(런타임 권위 없음)",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            ARTIFACT_RECEIPT,
            {
                "source_inputs": [aw.rel(path) for path in INPUT_FILES],
                "producer": aw.rel(__file__),
                "consumer": NEXT_RUN_ID,
                "artifact_paths": [aw.rel(path) for path in OUTPUT_FILES],
                "registry_links": [aw.rel(RUN_REGISTRY), aw.rel(ALPHA_LEDGER), aw.rel(STAGE_LEDGER), aw.rel(ARTIFACT_REGISTRY)],
                "lineage_judgment": "connected_with_hash_review(해시 검토로 연결)",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            JUDGMENT_RECEIPT,
            {
                "result_subject": RUN_ID,
                "evidence_available": [aw.rel(BLUEPRINT_REVIEW), aw.rel(FREEZE_REVIEW), aw.rel(PROXY_BOUNDARY_REVIEW), aw.rel(REQUIRED_GATE_AUDIT)],
                "evidence_missing": "no implementation, no fresh MT5 forward, no new ONNX, no runtime authority(구현 없음/신규 MT5 전진 없음/신규 ONNX 없음/런타임 권위 없음)",
                "judgment_label": "bounded_blueprint_review_passed_for_preflight_only(사전점검 전용 제한 청사진 검토 통과)",
                "next_condition": NEXT_RUN_ID,
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
    ]
    paths: list[Path] = []
    for path, payload in receipts:
        paths.append(aw.write_json(path, payload))
    return paths


def write_report(final: Mapping[str, Any]) -> Path:
    text = f"""# Stage337 run337BD Bounded No-Overfit Blueprint Review(337단계 337BD 제한 무과적합 청사진 검토)

## Conclusion(결론)

run337BD(337BD 실행)는 run337BC(337BC 실행)의 bounded blueprints(제한 청사진)를 검토했고, implementation preflight(구현 사전점검)로만 넘길 수 있다고 판정했다.

Effect(효과): 다음 실행은 구현 사전점검을 만들 수 있지만 cp322A(322A 후보), threshold(임계값), lot(로트), D/B rule(D/B 규칙), runtime handoff(런타임 인계)는 바꿀 수 없다.

## Result(결과)

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- blueprint_reviews(청사진 검토): `{final['blueprint_review_passed']}/{final['blueprint_review_rows']}`
- freeze_reviews(고정 검토): `{final['freeze_review_passed']}/{final['freeze_review_rows']}`
- protocol_reviews(절차 검토): `{final['protocol_review_passed']}/{final['protocol_review_rows']}`
- falsification_reviews(반증 검토): `{final['falsification_review_passed']}/{final['falsification_review_rows']}`
- proxy_boundary_reviews(프록시 경계 검토): `{final['proxy_boundary_passed']}/{final['proxy_boundary_rows']}`
- source_reviews(원천 검토): `{final['source_review_passed']}/{final['source_review_rows']}`
- gates(게이트): `{final['passed_gates']}/{final['gate_rows']}`

## Boundary(경계)

proxy expected value(프록시 예상값)는 schema/signal/mismatch(스키마/신호/불일치) 확인에만 쓴다. KPI(핵심 지표)는 fresh MT5 evidence(신규 MT5 근거)가 담당한다.

Forward Passed(전진 통과), Forward Failed(전진 실패), runtime_authority(런타임 권위), Goal Achieve(목표 달성)는 주장하지 않는다.

## Next Action(다음 행동)

- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return aw.write_text_lossless(REPORT_PATH, text, True)


def write_decision_doc(final: Mapping[str, Any]) -> Path:
    text = f"""# Decision(결정): Stage337 run337BD

- date(날짜): `{TODAY}`
- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`

## Boundary(경계)

run337BD(337BD 실행)는 review(검토)만 했다. model training(모델 학습), threshold retune(임계값 재조정), D/B rewrite(D/B 재작성), lot optimization(로트 최적화), candidate selection(후보 선택)은 없다.

Effect(효과): run337BE(337BE 실행)는 bounded implementation preflight(제한 구현 사전점검)만 열고, Forward/Goal(전진/목표)은 계속 주장하지 않는다.
"""
    return aw.write_text_lossless(DECISION_DOC, text, True)


def insert_current_focus(text: str, block: str) -> str:
    marker = "current_focus:\n"
    if block.strip() in text:
        return text
    if marker not in text:
        return text.rstrip() + "\n" + block
    return text.replace(marker, marker + block, 1)


def update_docs(final: Mapping[str, Any]) -> list[Path]:
    artifacts: list[Path] = []
    workspace, workspace_bom = aw.read_tracked_text_lossless(WORKSPACE_STATE)
    workspace = aw.replace_prefix_line(workspace, "current_run_id:", f"current_run_id: {NEXT_RUN_ID}")
    focus = (
        "- >-\n"
        f"  Stage337 run337BD focus complete: run337BD(337BD 실행)은 `{final['status']}`로 bounded blueprint review(제한 청사진 검토)를 완료했다. "
        f"Effect(효과): blueprint reviews(청사진 검토) `{final['blueprint_review_passed']}/{final['blueprint_review_rows']}`, "
        f"freeze reviews(고정 검토) `{final['freeze_review_passed']}/{final['freeze_review_rows']}`, gates(게이트) `{final['passed_gates']}/{final['gate_rows']}`이며 Forward/Goal(전진/목표)은 주장하지 않는다.\n"
    )
    workspace = insert_current_focus(workspace, focus)
    artifacts.append(aw.write_text_lossless(WORKSPACE_STATE, workspace, workspace_bom))

    current, current_bom = aw.read_tracked_text_lossless(CURRENT_STATE)
    replacements = {
        "- current_run(현재 실행):": f"- current_run(현재 실행): `{NEXT_RUN_ID}`",
        "- status(상태):": f"- status(상태): `{final['status']}`",
        "- decision(결정):": f"- decision(결정): `{final['decision']}`",
        "- latest_completed_run(최근 완료 실행):": f"- latest_completed_run(최근 완료 실행): `{RUN_ID}`",
        "- next_action(다음 행동):": f"- next_action(다음 행동): `{NEXT_RUN_ID}`",
        "- claim_boundary(주장 경계):": f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
    }
    for prefix, replacement in replacements.items():
        current = aw.replace_prefix_line(current, prefix, replacement)
    section = f"""
## Stage337 run337BD(337BD 실행) - {TODAY}

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- effect(효과): run337BD(337BD 실행)는 run337BC(337BC 실행)의 청사진/고정/절차/반증/proxy-MT5(프록시-MT5) 경계를 검토했고, 구현 사전점검만 열었다. Forward/Goal(전진/목표)은 주장하지 않는다.
"""
    if "## Stage337 run337BD" not in current:
        current = current.replace("## Stage337 run337BC", section + "\n## Stage337 run337BC", 1)
    artifacts.append(aw.write_text_lossless(CURRENT_STATE, current, current_bom))

    selection = f"""# Stage337 Selection Status(337단계 선택 상태)

- stage_id(단계 ID): `{STAGE_ID}`
- stage_status(단계 상태): `open_active`
- selected_candidate(선택 후보): `none`
- latest_run(최신 실행): `{RUN_ID}`
- latest_decision(최신 결정): `{DECISION}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- frozen_subject(고정 대상): `cp322A_cp321b_exact_replay_control_surface`
- blueprint_review_rows(청사진 검토 행): `{final['blueprint_review_rows']}`
- freeze_review_rows(고정 검토 행): `{final['freeze_review_rows']}`
- falsification_review_rows(반증 검토 행): `{final['falsification_review_rows']}`
- implementation_boundary_rows(구현 경계 행): `{final['implementation_boundary_rows']}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- Forward Blocked(전진 차단): `not_closed_preflight_open`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): run337BD(337BD 실행)는 청사진 검토만 완료했고 전진/운영 주장은 막는다.
"""
    artifacts.append(aw.write_text_lossless(SELECTED_STATUS, selection, True))

    brief, brief_bom = aw.read_tracked_text_lossless(STAGE_BRIEF)
    brief = aw.replace_prefix_line(brief, "- latest_run(최신 실행):", f"- latest_run(최신 실행): `{RUN_ID}`")
    summary = (
        f"- run337BD_summary(337BD 요약): `{final['status']}`. "
        f"Effect(효과): bounded blueprint review(제한 청사진 검토) `{final['blueprint_review_passed']}/{final['blueprint_review_rows']}`, "
        f"freeze review(고정 검토) `{final['freeze_review_passed']}/{final['freeze_review_rows']}`, gates(게이트) `{final['passed_gates']}/{final['gate_rows']}`를 완료하고 "
        f"run337BE(337BE 실행) implementation preflight(구현 사전점검)를 연다. Forward/Goal(전진/목표)은 주장하지 않는다.\n"
    )
    if "run337BD_summary" not in brief:
        brief = brief.rstrip() + "\n" + summary
    artifacts.append(aw.write_text_lossless(STAGE_BRIEF, brief, brief_bom))

    changelog, changelog_bom = aw.read_tracked_text_lossless(CHANGELOG)
    line = (
        f"- {TODAY}: Stage337 run337BD(337BD 실행) `{final['status']}`. "
        f"Effect(효과): bounded no-overfit blueprint review(제한 무과적합 청사진 검토)를 완료하고 implementation preflight(구현 사전점검)만 열었으며 Forward/Goal(전진/목표)은 주장하지 않음."
    )
    if "Stage337 run337BD" not in changelog:
        changelog = changelog.rstrip() + "\n" + line + "\n"
    artifacts.append(aw.write_text_lossless(CHANGELOG, changelog, changelog_bom))
    return artifacts


def update_registers(final: Mapping[str, Any]) -> list[Path]:
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "bounded_no_overfit_blueprint_review_without_db",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": aw.rel(REPORT_PATH),
        "notes": f"decision={final['decision']};next_action={final['next_action']};goal_achieve_not_claimed.",
        "family": "experiment_review",
        "primary_report": aw.rel(REPORT_PATH),
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__blueprint_review",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "blueprint_review",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "Stage337 run337BD bounded blueprint review",
        "tier_scope": "research_review_only",
        "kpi_scope": "no_new_trading_kpi",
        "scoreboard_lane": "experiment_review",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": aw.rel(REPORT_PATH),
        "primary_kpi": f"blueprints={final['blueprint_review_passed']}/{final['blueprint_review_rows']};gates={final['passed_gates']}/{final['gate_rows']}",
        "guardrail_kpi": "cp322a_frozen;no_training;no_threshold_retune;no_db_rule_rewrite;no_lot_opt;no_forward_claim",
        "external_verification_status": "out_of_scope_by_claim_review_only(주장 범위 밖, 검토 전용)",
        "notes": f"decision={final['decision']};next_action={final['next_action']};runtime_authority_not_claimed.",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__blueprint_review",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "experiment_review",
        "evidence_scope": "run337BC bounded blueprint package",
        "kpi_scope": "review_no_forward_decision",
        "status": final["status"],
        "judgment": final["judgment"],
        "claim_boundary": CLAIM_BOUNDARY,
        "path": aw.rel(REPORT_PATH),
        "notes": f"goal_achieve_not_claimed;gates={final['passed_gates']}/{final['gate_rows']}",
        "decision": final["decision"],
        "run_key": f"{RUN_ID}__blueprint_review",
        "family": "bounded_no_overfit_blueprint_review_without_db",
        "question": "can bounded cp322A repair blueprints open implementation preflight without retune",
        "metric_scope": "blueprint_freeze_protocol_falsification_proxy_boundary",
        "primary_artifact": aw.rel(REPORT_PATH),
        "report_path": aw.rel(REPORT_PATH),
        "next_action": final["next_action"],
    }
    aw.upsert_csv(RUN_REGISTRY, aw.RUN_REGISTRY_COLUMNS, run_row, "run_id")
    aw.upsert_csv(ALPHA_LEDGER, aw.ALPHA_LEDGER_COLUMNS, alpha_row, "ledger_row_id")
    aw.upsert_csv(STAGE_LEDGER, aw.STAGE_LEDGER_COLUMNS, stage_row, "ledger_row_id")
    return [RUN_REGISTRY, ALPHA_LEDGER, STAGE_LEDGER]


def update_artifact_registry(paths: Sequence[Path], final: Mapping[str, Any]) -> Path:
    columns, rows = aw.read_csv_table(ARTIFACT_REGISTRY, prefer_head=True)
    columns = columns or list(aw.ARTIFACT_COLUMNS)
    rows = [row for row in rows if not str(row.get("artifact_id", "")).startswith(f"{RUN_ID}::")]
    created_at = now_utc()
    seen: set[str] = set()
    for path in paths:
        if not aw.path_exists(path):
            continue
        artifact_path = aw.rel(path)
        if artifact_path in seen:
            continue
        seen.add(artifact_path)
        rows.append(
            {
                "artifact_id": f"{RUN_ID}::{artifact_path}",
                "artifact_type": path.suffix.lower().lstrip(".") or "file",
                "path": artifact_path,
                "sha256": aw.sha256_file(path),
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": created_at,
                "notes": final["status"],
                "artifact_path": artifact_path,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return aw.write_csv(ARTIFACT_REGISTRY, columns, rows)


def main() -> int:
    aw.io_path(RUN_DIR).mkdir(parents=True, exist_ok=True)
    src = load_inputs()

    blueprint_review = build_blueprint_review(src["blueprints"])
    blueprint_path = aw.write_csv(BLUEPRINT_REVIEW, BLUEPRINT_REVIEW_COLUMNS, blueprint_review)
    freeze_review = build_freeze_review(src["freeze"])
    freeze_path = aw.write_csv(FREEZE_REVIEW, FREEZE_REVIEW_COLUMNS, freeze_review)
    protocol_review = build_protocol_review(src["protocols"])
    protocol_path = aw.write_csv(PROTOCOL_REVIEW, PROTOCOL_REVIEW_COLUMNS, protocol_review)
    falsification_review = build_falsification_review(src["falsification"])
    falsification_path = aw.write_csv(FALSIFICATION_REVIEW, FALSIFICATION_REVIEW_COLUMNS, falsification_review)
    proxy_review = build_proxy_boundary_review(src["proxy"])
    proxy_path = aw.write_csv(PROXY_BOUNDARY_REVIEW, PROXY_BOUNDARY_REVIEW_COLUMNS, proxy_review)
    source_review = build_source_review(src["sources"])
    source_path = aw.write_csv(SOURCE_REVIEW, SOURCE_REVIEW_COLUMNS, source_review)
    implementation_boundary = build_implementation_boundary(src["blueprints"])
    boundary_path = aw.write_csv(IMPLEMENTATION_BOUNDARY, IMPLEMENTATION_BOUNDARY_COLUMNS, implementation_boundary)
    next_queue = build_next_queue()
    queue_path = aw.write_csv(RUN337BE_QUEUE, QUEUE_COLUMNS, next_queue)

    gate_rows = build_gates(
        src,
        blueprint_review,
        freeze_review,
        protocol_review,
        falsification_review,
        proxy_review,
        source_review,
        implementation_boundary,
        next_queue,
    )
    gate_path = aw.write_csv(REQUIRED_GATE_AUDIT, GATE_COLUMNS, gate_rows)
    all_gates_pass = all(row.get("status") == "passed" for row in gate_rows)
    final = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS if all_gates_pass else "invalid_stage337BD_bounded_blueprint_review_gate_failure_no_forward_decision",
        "judgment": JUDGMENT if all_gates_pass else "bounded_blueprint_review_gate_failure",
        "decision": DECISION if all_gates_pass else "repair_stage337BD_blueprint_review_before_preflight",
        "next_action": NEXT_RUN_ID if all_gates_pass else "repair_stage337BD_blueprint_review_gate_failure_v1",
        "blueprint_review_rows": len(blueprint_review),
        "blueprint_review_passed": count_status(blueprint_review, "accepted_for_implementation_preflight"),
        "freeze_review_rows": len(freeze_review),
        "freeze_review_passed": count_status(freeze_review, "freeze_preserved"),
        "protocol_review_rows": len(protocol_review),
        "protocol_review_passed": count_status(protocol_review, "protocol_review_accepted"),
        "falsification_review_rows": len(falsification_review),
        "falsification_review_passed": count_status(falsification_review, "falsification_gate_active"),
        "proxy_boundary_rows": len(proxy_review),
        "proxy_boundary_passed": count_status(proxy_review, "proxy_mt5_boundary_preserved"),
        "source_review_rows": len(source_review),
        "source_review_passed": count_status(source_review, "source_identity_verified"),
        "implementation_boundary_rows": len(implementation_boundary),
        "queue_rows": len(next_queue),
        "gate_rows": len(gate_rows),
        "passed_gates": sum(1 for row in gate_rows if row.get("status") == "passed"),
        "failed_gates": [row.get("gate_id") for row in gate_rows if row.get("status") != "passed"],
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "runtime_authority": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    final_path = aw.write_json(FINAL_DECISION, final)
    manifest = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "created_at_utc": now_utc(),
        "producer": aw.rel(__file__),
        "parent_run_id": PARENT_RUN_ID,
        "inputs": [aw.rel(path) for path in INPUT_FILES],
        "outputs": [aw.rel(path) for path in OUTPUT_FILES],
        "forbidden_actions": [
            "model training(모델 학습)",
            "threshold retuning(임계값 재조정)",
            "D/B rewrite(D/B 재작성)",
            "lot optimization(로트 최적화)",
            "candidate selection(후보 선택)",
            "proxy KPI authority(프록시 KPI 권위)",
            "Forward Passed/Failed claim(전진 통과/실패 주장)",
            "Goal Achieve claim(목표 달성 주장)",
        ],
        "claim_boundary": CLAIM_BOUNDARY,
    }
    manifest_path = aw.write_json(RUN_MANIFEST, manifest)
    receipt_paths = write_receipts(final)
    report_path = write_report(final)
    decision_path = write_decision_doc(final)
    doc_paths = update_docs(final)
    register_paths = update_registers(final)
    artifact_paths = [
        blueprint_path,
        freeze_path,
        protocol_path,
        falsification_path,
        proxy_path,
        source_path,
        boundary_path,
        queue_path,
        gate_path,
        *receipt_paths,
        final_path,
        manifest_path,
        report_path,
        decision_path,
        *doc_paths,
        *register_paths,
        Path(__file__),
    ]
    artifact_registry_path = update_artifact_registry(artifact_paths, final)
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": final["status"],
                "judgment": final["judgment"],
                "decision": final["decision"],
                "next_action": final["next_action"],
                "blueprint_reviews": f"{final['blueprint_review_passed']}/{final['blueprint_review_rows']}",
                "freeze_reviews": f"{final['freeze_review_passed']}/{final['freeze_review_rows']}",
                "proxy_boundary": f"{final['proxy_boundary_passed']}/{final['proxy_boundary_rows']}",
                "gates": f"{final['passed_gates']}/{final['gate_rows']}",
                "report": aw.rel(report_path),
                "artifact_registry": aw.rel(artifact_registry_path),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if all_gates_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
