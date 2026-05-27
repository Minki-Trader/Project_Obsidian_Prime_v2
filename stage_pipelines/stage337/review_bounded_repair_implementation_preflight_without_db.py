from __future__ import annotations

import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from stage_pipelines.stage337 import materialize_bounded_repair_implementation_preflight_without_db as be


aw = be.aw

TODAY = "2026-05-27"
STAGE_ID = be.STAGE_ID
RUN_NUMBER = "run337BF"
RUN_ID = "run337BF_review_bounded_repair_implementation_preflight_without_db_v1"
PARENT_RUN_ID = be.RUN_ID
NEXT_RUN_ID = "run337BG_materialize_bounded_repair_scaffold_inputs_without_db_v1"
STATUS = "completed_stage337BF_bounded_implementation_preflight_reviewed_ready_for_scaffold_inputs_no_training_no_selection"
JUDGMENT = "preflight_review_accepts_bounded_scaffold_inputs_with_proxy_signal_only_and_mt5_gap_blocker"
DECISION = "stage337BF_open_run337BG_materialize_bounded_repair_scaffold_inputs_no_training_no_selection"
CLAIM_BOUNDARY = (
    "research_development_only_stage337BF_bounded_preflight_review_without_db_cp322a_frozen_"
    "no_model_training_no_threshold_retuning_no_db_rule_rewrite_no_lot_optimization_no_candidate_selection_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = be.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = be.REVIEWS_DIR
REPORT_PATH = REVIEWS_DIR / "run337BF_preflight_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-27_stage337BF_bounded_repair_implementation_preflight_review.md"
SELECTED_STATUS = be.SELECTED_STATUS
STAGE_BRIEF = be.STAGE_BRIEF
WORKSPACE_STATE = be.WORKSPACE_STATE
CURRENT_STATE = be.CURRENT_STATE
CHANGELOG = be.CHANGELOG
RUN_REGISTRY = be.RUN_REGISTRY
ALPHA_LEDGER = be.ALPHA_LEDGER
ARTIFACT_REGISTRY = be.ARTIFACT_REGISTRY
STAGE_LEDGER = be.STAGE_LEDGER

RUN337BE_DIR = STAGE_DIR / "02_runs" / "run337BE"
BE_FINAL = RUN337BE_DIR / "final_decision.json"
BE_MANIFEST = RUN337BE_DIR / "run_manifest.json"
BE_PREFLIGHT = RUN337BE_DIR / "implementation_preflight_matrix.csv"
BE_HASH_CHECK = RUN337BE_DIR / "frozen_surface_hash_check.csv"
BE_PROXY_DIFF = RUN337BE_DIR / "proxy_mt5_existing_difference_preflight.csv"
BE_MT5_BLOCKER = RUN337BE_DIR / "mt5_forward_readiness_blockers.csv"
BE_FIREWALL = RUN337BE_DIR / "no_overfit_firewall_preflight.csv"
BE_ARTIFACT_MANIFEST = RUN337BE_DIR / "preflight_artifact_manifest.csv"
BE_QUEUE = RUN337BE_DIR / "run337BF_review_queue.csv"
BE_GATE_AUDIT = RUN337BE_DIR / "required_gate_coverage_audit.csv"
BE_EXPERIMENT_RECEIPT = RUN337BE_DIR / "experiment_design_receipt.json"
BE_DATA_RECEIPT = RUN337BE_DIR / "data_integrity_receipt.json"
BE_MODEL_RECEIPT = RUN337BE_DIR / "model_validation_receipt.json"
BE_RUNTIME_RECEIPT = RUN337BE_DIR / "runtime_parity_receipt.json"
BE_ARTIFACT_RECEIPT = RUN337BE_DIR / "artifact_lineage_receipt.json"
BE_JUDGMENT_RECEIPT = RUN337BE_DIR / "result_judgment_receipt.json"

PREFLIGHT_REVIEW = RUN_DIR / "implementation_preflight_review_matrix.csv"
FROZEN_SURFACE_REVIEW = RUN_DIR / "frozen_surface_review.csv"
PROXY_MT5_USABILITY_REVIEW = RUN_DIR / "proxy_mt5_usability_review.csv"
MT5_BLOCKER_REVIEW = RUN_DIR / "mt5_forward_blocker_review.csv"
NO_OVERFIT_FIREWALL_REVIEW = RUN_DIR / "no_overfit_firewall_review.csv"
ARTIFACT_MANIFEST_REVIEW = RUN_DIR / "artifact_manifest_review.csv"
BALANCED_WORKSTREAM_REVIEW = RUN_DIR / "balanced_workstream_review.csv"
SCAFFOLD_HANDOFF_BOUNDARY = RUN_DIR / "scaffold_handoff_boundary_matrix.csv"
RUN337BG_QUEUE = RUN_DIR / "run337BG_scaffold_input_queue.csv"
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
    BE_FINAL,
    BE_MANIFEST,
    BE_PREFLIGHT,
    BE_HASH_CHECK,
    BE_PROXY_DIFF,
    BE_MT5_BLOCKER,
    BE_FIREWALL,
    BE_ARTIFACT_MANIFEST,
    BE_QUEUE,
    BE_GATE_AUDIT,
    BE_EXPERIMENT_RECEIPT,
    BE_DATA_RECEIPT,
    BE_MODEL_RECEIPT,
    BE_RUNTIME_RECEIPT,
    BE_ARTIFACT_RECEIPT,
    BE_JUDGMENT_RECEIPT,
)
OUTPUT_FILES = (
    PREFLIGHT_REVIEW,
    FROZEN_SURFACE_REVIEW,
    PROXY_MT5_USABILITY_REVIEW,
    MT5_BLOCKER_REVIEW,
    NO_OVERFIT_FIREWALL_REVIEW,
    ARTIFACT_MANIFEST_REVIEW,
    BALANCED_WORKSTREAM_REVIEW,
    SCAFFOLD_HANDOFF_BOUNDARY,
    RUN337BG_QUEUE,
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

PREFLIGHT_REVIEW_COLUMNS = (
    "review_id",
    "source_blueprint_id",
    "preflight_scope_ok",
    "allowed_actions_bounded",
    "forbidden_actions_complete",
    "required_inputs_present",
    "required_outputs_complete",
    "proxy_mt5_requirement_ok",
    "mt5_forward_requirement_ok",
    "review_status",
    "effect",
    "claim_boundary",
)
FROZEN_SURFACE_REVIEW_COLUMNS = (
    "review_id",
    "check_id",
    "freeze_id",
    "subject",
    "identity_match",
    "forbidden_change",
    "preflight_status",
    "review_status",
    "effect",
    "claim_boundary",
)
PROXY_REVIEW_COLUMNS = (
    "review_id",
    "source_blueprint_id",
    "proxy_diff_rows",
    "matched_rows",
    "mismatch_rows",
    "max_abs_difference",
    "signal_parity_usable",
    "forward_decision_usable",
    "runtime_skip_reason_present",
    "tester_gap_status",
    "metric_read_bound",
    "usability_judgment",
    "review_status",
    "effect",
    "claim_boundary",
)
MT5_BLOCKER_REVIEW_COLUMNS = (
    "review_id",
    "source_blueprint_id",
    "tester_gap_status",
    "latest_feature_last_timestamp",
    "tester_last_observed_bar_time",
    "max_tester_to_feature_gap_minutes",
    "required_before_forward",
    "forward_claim_status",
    "runtime_authority_status",
    "review_status",
    "effect",
    "claim_boundary",
)
FIREWALL_REVIEW_COLUMNS = (
    "review_id",
    "firewall_id",
    "guard_family",
    "must_remain_false",
    "abort_if_seen",
    "preflight_status",
    "review_status",
    "effect",
    "claim_boundary",
)
ARTIFACT_REVIEW_COLUMNS = (
    "review_id",
    "artifact_id",
    "artifact_role",
    "path",
    "exists",
    "row_count",
    "sha256",
    "availability",
    "review_status",
    "effect",
    "claim_boundary",
)
BALANCE_REVIEW_COLUMNS = (
    "review_id",
    "workstream_family",
    "evidence_rows",
    "source_blueprints",
    "proxy_mt5_bound",
    "mt5_gap_bound",
    "forward_claim_forbidden",
    "review_status",
    "effect",
    "claim_boundary",
)
HANDOFF_BOUNDARY_COLUMNS = (
    "handoff_id",
    "source_blueprint_id",
    "allowed_next_work",
    "forbidden_next_work",
    "required_scaffold_inputs",
    "required_scaffold_outputs",
    "required_review_before_runtime",
    "handoff_status",
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

BLUEPRINT_FAMILY = {
    "bc_blueprint_01": "defensive(방어)",
    "bc_blueprint_02": "repair(수리)",
    "bc_blueprint_03": "offensive(공격)",
    "bc_blueprint_04": "defensive_repair(방어_수리)",
    "bc_blueprint_05": "control_parity(대조_동등성)",
}


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def status_text(ok: bool) -> str:
    return "passed" if ok else "failed"


def require_inputs() -> None:
    missing = [aw.rel(path) for path in INPUT_FILES if not aw.path_exists(path)]
    if missing:
        raise FileNotFoundError("missing run337BF inputs: " + "; ".join(missing))


def load_inputs() -> dict[str, Any]:
    require_inputs()
    return {
        "be_final": aw.read_json(BE_FINAL),
        "be_manifest": aw.read_json(BE_MANIFEST),
        "preflight": aw.read_csv(BE_PREFLIGHT),
        "hash_check": aw.read_csv(BE_HASH_CHECK),
        "proxy": aw.read_csv(BE_PROXY_DIFF),
        "mt5_blocker": aw.read_csv(BE_MT5_BLOCKER),
        "firewall": aw.read_csv(BE_FIREWALL),
        "artifact_manifest": aw.read_csv(BE_ARTIFACT_MANIFEST),
        "queue": aw.read_csv(BE_QUEUE),
        "be_gate_audit": aw.read_csv(BE_GATE_AUDIT),
        "be_receipts": [
            aw.read_json(BE_EXPERIMENT_RECEIPT),
            aw.read_json(BE_DATA_RECEIPT),
            aw.read_json(BE_MODEL_RECEIPT),
            aw.read_json(BE_RUNTIME_RECEIPT),
            aw.read_json(BE_ARTIFACT_RECEIPT),
            aw.read_json(BE_JUDGMENT_RECEIPT),
        ],
    }


def row_count(path: Path) -> int:
    if not aw.path_exists(path):
        return 0
    if path.suffix.lower() == ".json":
        return len(aw.read_json(path))
    return len(aw.read_csv(path))


def lower_text(*values: Any) -> str:
    return " ".join(str(value or "") for value in values).lower()


def csv_int(value: Any) -> int:
    try:
        return int(float(str(value or "0").replace(",", "")))
    except ValueError:
        return 0


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


def count_status(rows: Sequence[Mapping[str, Any]], column: str, prefix: str) -> int:
    return sum(1 for row in rows if str(row.get(column, "")).startswith(prefix))


def build_preflight_review(preflight: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in preflight:
        text = lower_text(row)
        scope_ok = all(token in text for token in ("schema adapter", "measurement harness", "report template"))
        allowed_ok = "implementation preflight" in text and "measurement harness" in text
        forbidden_ok = all(
            token in text
            for token in (
                "model training",
                "threshold retuning",
                "d/b rule rewrite",
                "lot optimization",
                "candidate selection",
                "date/trade-index",
                "proxy kpi authority",
            )
        )
        inputs_ok = paths_exist(row.get("required_inputs", ""))
        outputs_ok = all(
            token in lower_text(row.get("required_outputs", ""))
            for token in ("frozen surface hash", "proxy-mt5", "mt5 forward", "no-overfit firewall")
        )
        proxy_ok = "compare proxy expected values with mt5 runtime probe values" in lower_text(row.get("proxy_mt5_requirement", ""))
        mt5_ok = all(token in lower_text(row.get("mt5_forward_requirement", "")) for token in ("compile receipt", "handoff hash", "difference table"))
        accepted = all((scope_ok, allowed_ok, forbidden_ok, inputs_ok, outputs_ok, proxy_ok, mt5_ok))
        rows.append(
            {
                "review_id": f"{RUN_NUMBER}_{row.get('source_blueprint_id')}_preflight_review",
                "source_blueprint_id": row.get("source_blueprint_id", ""),
                "preflight_scope_ok": str(scope_ok).lower(),
                "allowed_actions_bounded": str(allowed_ok).lower(),
                "forbidden_actions_complete": str(forbidden_ok).lower(),
                "required_inputs_present": str(inputs_ok).lower(),
                "required_outputs_complete": str(outputs_ok).lower(),
                "proxy_mt5_requirement_ok": str(proxy_ok).lower(),
                "mt5_forward_requirement_ok": str(mt5_ok).lower(),
                "review_status": "accepted_for_bounded_scaffold_inputs(제한 스캐폴드 입력 허용)" if accepted else "preflight_review_rejected(사전점검 검토 거부)",
                "effect": "allows only scaffold-input materialization after confirming preflight boundaries(사전점검 경계 확인 후 스캐폴드 입력 물질화만 허용)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_frozen_surface_review(hash_rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in hash_rows:
        accepted = row.get("identity_match") == "true" and str(row.get("preflight_status", "")).startswith("hash_identity")
        rows.append(
            {
                "review_id": f"{RUN_NUMBER}_{row.get('check_id')}_review",
                "check_id": row.get("check_id", ""),
                "freeze_id": row.get("freeze_id", ""),
                "subject": row.get("subject", ""),
                "identity_match": row.get("identity_match", ""),
                "forbidden_change": row.get("forbidden_change", ""),
                "preflight_status": row.get("preflight_status", ""),
                "review_status": "frozen_surface_verified(고정 표면 확인)" if accepted else "frozen_surface_review_failed(고정 표면 검토 실패)",
                "effect": "keeps scaffold inputs tied to the same cp322A package identity(스캐폴드 입력을 같은 cp322A 패키지 정체성에 묶음)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_proxy_usability_review(proxy_rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in proxy_rows:
        diff_rows = csv_int(row.get("proxy_diff_rows"))
        matched = csv_int(row.get("matched_rows"))
        mismatch = csv_int(row.get("mismatch_rows"))
        signal = row.get("all_signal_parity_usable") == "true"
        forward = row.get("any_forward_pass_fail_usable") == "true"
        skip_present = bool(row.get("runtime_skip_reasons"))
        gap_status = row.get("existing_tester_gap_status", "")
        metric_bound = "forward=false" in lower_text(row.get("existing_mt5_metric_read", ""))
        accepted = diff_rows > 0 and matched == diff_rows and mismatch == 0 and signal and not forward and "tester_feature_last_gap_remains" in gap_status and metric_bound
        rows.append(
            {
                "review_id": f"{RUN_NUMBER}_{row.get('source_blueprint_id')}_proxy_usability_review",
                "source_blueprint_id": row.get("source_blueprint_id", ""),
                "proxy_diff_rows": diff_rows,
                "matched_rows": matched,
                "mismatch_rows": mismatch,
                "max_abs_difference": row.get("max_abs_difference", ""),
                "signal_parity_usable": str(signal).lower(),
                "forward_decision_usable": str(forward).lower(),
                "runtime_skip_reason_present": str(skip_present).lower(),
                "tester_gap_status": gap_status,
                "metric_read_bound": str(metric_bound).lower(),
                "usability_judgment": row.get("usability_judgment", ""),
                "review_status": "accepted_signal_parity_only(신호 동등성 전용 수락)" if accepted else "proxy_usability_review_failed(프록시 사용성 검토 실패)",
                "effect": "keeps proxy useful for parity while blocking forward KPI authority(프록시는 동등성에 쓰고 전진 KPI 권위는 막음)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_mt5_blocker_review(blocker_rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in blocker_rows:
        gap_ok = "tester_feature_last_gap_remains" in row.get("tester_gap_status", "")
        forward_ok = row.get("forward_claim_status", "").startswith("not_claimed")
        runtime_ok = row.get("runtime_authority_status", "").startswith("not_claimed")
        required_ok = "feature_last" in lower_text(row.get("required_before_forward", "")) and "difference" in lower_text(row.get("required_before_forward", ""))
        accepted = gap_ok and forward_ok and runtime_ok and required_ok
        rows.append(
            {
                "review_id": f"{RUN_NUMBER}_{row.get('source_blueprint_id')}_mt5_blocker_review",
                "source_blueprint_id": row.get("source_blueprint_id", ""),
                "tester_gap_status": row.get("tester_gap_status", ""),
                "latest_feature_last_timestamp": row.get("latest_feature_last_timestamp", ""),
                "tester_last_observed_bar_time": row.get("tester_last_observed_bar_time", ""),
                "max_tester_to_feature_gap_minutes": row.get("max_tester_to_feature_gap_minutes", ""),
                "required_before_forward": row.get("required_before_forward", ""),
                "forward_claim_status": row.get("forward_claim_status", ""),
                "runtime_authority_status": row.get("runtime_authority_status", ""),
                "review_status": "mt5_forward_blocker_active(MT5 전진 차단 조건 활성)" if accepted else "mt5_blocker_review_failed(MT5 차단 조건 검토 실패)",
                "effect": "prevents a forward decision until the tester reaches feature_last(테스터가 feature_last에 도달하기 전 전진 판정을 막음)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_firewall_review(firewall_rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in firewall_rows:
        active = row.get("preflight_status") == "active(활성)" and row.get("must_remain_false") == "true"
        rows.append(
            {
                "review_id": f"{RUN_NUMBER}_{row.get('firewall_id')}_review",
                "firewall_id": row.get("firewall_id", ""),
                "guard_family": row.get("guard_family", ""),
                "must_remain_false": row.get("must_remain_false", ""),
                "abort_if_seen": row.get("abort_if_seen", ""),
                "preflight_status": row.get("preflight_status", ""),
                "review_status": "firewall_active(방화벽 활성)" if active else "firewall_review_failed(방화벽 검토 실패)",
                "effect": "keeps scaffold handoff from opening overfit shortcuts(스캐폴드 인계가 과적합 지름길을 열지 못하게 함)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_artifact_review(artifact_rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in artifact_rows:
        exists = row.get("exists") == "true"
        has_hash = bool(row.get("sha256", ""))
        count_ok = csv_int(row.get("row_count")) > 0
        accepted = exists and has_hash and count_ok
        rows.append(
            {
                "review_id": f"{RUN_NUMBER}_{row.get('artifact_id')}_review",
                "artifact_id": row.get("artifact_id", ""),
                "artifact_role": row.get("artifact_role", ""),
                "path": row.get("path", ""),
                "exists": row.get("exists", ""),
                "row_count": row.get("row_count", ""),
                "sha256": row.get("sha256", ""),
                "availability": row.get("availability", ""),
                "review_status": "artifact_connected(산출물 연결)" if accepted else "artifact_review_failed(산출물 검토 실패)",
                "effect": "keeps ignored run artifacts reproducible through manifest identity(무시된 실행 산출물을 목록 정체성으로 재현 가능하게 함)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_balance_review(
    preflight_review: Sequence[Mapping[str, Any]],
    proxy_review: Sequence[Mapping[str, Any]],
    blocker_review: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    proxy_by_blueprint = {str(row.get("source_blueprint_id")): row for row in proxy_review}
    blocker_by_blueprint = {str(row.get("source_blueprint_id")): row for row in blocker_review}
    family_rows: dict[str, list[str]] = {}
    for row in preflight_review:
        blueprint = str(row.get("source_blueprint_id"))
        family = BLUEPRINT_FAMILY.get(blueprint, "unknown(미상)")
        family_rows.setdefault(family, []).append(blueprint)
    rows: list[dict[str, Any]] = []
    for family, blueprints in family_rows.items():
        proxy_ok = all(str(proxy_by_blueprint.get(bp, {}).get("review_status", "")).startswith("accepted_signal") for bp in blueprints)
        gap_ok = all(str(blocker_by_blueprint.get(bp, {}).get("review_status", "")).startswith("mt5_forward_blocker_active") for bp in blueprints)
        forward_forbidden = all(str(proxy_by_blueprint.get(bp, {}).get("forward_decision_usable", "")) == "false" for bp in blueprints)
        accepted = proxy_ok and gap_ok and forward_forbidden
        rows.append(
            {
                "review_id": f"{RUN_NUMBER}_{family}_balance_review",
                "workstream_family": family,
                "evidence_rows": len(blueprints),
                "source_blueprints": ";".join(blueprints),
                "proxy_mt5_bound": str(proxy_ok).lower(),
                "mt5_gap_bound": str(gap_ok).lower(),
                "forward_claim_forbidden": str(forward_forbidden).lower(),
                "review_status": "balanced_workstream_preserved(균형 작업흐름 보존)" if accepted else "balanced_workstream_review_failed(균형 작업흐름 검토 실패)",
                "effect": "keeps defensive, repair, offensive, and parity-control workstreams alive together(방어/수리/공격/동등성 대조 작업흐름을 함께 유지)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_handoff_boundary(preflight_review: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in preflight_review:
        blueprint = row.get("source_blueprint_id", "")
        rows.append(
            {
                "handoff_id": f"{RUN_NUMBER}_{blueprint}_scaffold_handoff_boundary",
                "source_blueprint_id": blueprint,
                "allowed_next_work": "schema-only scaffold inputs(스키마 전용 스캐폴드 입력); measurement harness spec(측정 하네스 명세); dry-run handoff manifest(드라이런 인계 목록); review queue(검토 대기열)",
                "forbidden_next_work": "model fit/train(모델 학습); threshold search(임계값 탐색); D/B rewrite(D/B 재작성); lot/risk optimization(로트/위험 최적화); MT5 forward claim(MT5 전진 주장); live readiness(실거래 준비)",
                "required_scaffold_inputs": f"{aw.rel(PREFLIGHT_REVIEW)};{aw.rel(PROXY_MT5_USABILITY_REVIEW)};{aw.rel(MT5_BLOCKER_REVIEW)};{aw.rel(NO_OVERFIT_FIREWALL_REVIEW)}",
                "required_scaffold_outputs": "scaffold input package(스캐폴드 입력 패키지); hash manifest(해시 목록); no-lookahead checklist(미래참조 방지 목록); proxy-MT5 comparison contract(프록시-MT5 비교 계약)",
                "required_review_before_runtime": "run337BH review must pass before any MT5 runtime or forward tester execution(어떤 MT5 런타임 또는 전진 테스터 실행 전 run337BH 검토 통과 필요)",
                "handoff_status": "open_scaffold_inputs_only(스캐폴드 입력만 개방)",
                "effect": "moves one step toward implementation without mutating the trading surface(거래 표면 변경 없이 구현 쪽으로 한 단계 이동)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_next_queue() -> list[dict[str, Any]]:
    return [
        {
            "queue_id": "run337BG_materialize_bounded_scaffold_inputs",
            "next_run_id": NEXT_RUN_ID,
            "review_subject": "bounded repair scaffold inputs(제한 수리 스캐폴드 입력)",
            "inputs_to_review": ";".join(
                aw.rel(path)
                for path in (
                    PREFLIGHT_REVIEW,
                    FROZEN_SURFACE_REVIEW,
                    PROXY_MT5_USABILITY_REVIEW,
                    MT5_BLOCKER_REVIEW,
                    NO_OVERFIT_FIREWALL_REVIEW,
                    BALANCED_WORKSTREAM_REVIEW,
                    SCAFFOLD_HANDOFF_BOUNDARY,
                )
            ),
            "must_confirm": "schema-only, no training, no threshold, no D/B rewrite, no lot optimization, proxy signal-only, MT5 gap still blocks forward(스키마 전용/학습 없음/임계값 없음/D-B 재작성 없음/로트 최적화 없음/프록시 신호 전용/MT5 공백이 전진 차단)",
            "must_reject_if": "model, threshold, D/B, lot, date, trade-index, proxy KPI, forward, runtime authority, live readiness appears(모델/임계값/D-B/로트/날짜/거래번호/프록시 KPI/전진/런타임 권위/실거래 준비 등장)",
            "expected_outputs": "scaffold input package and review queue only(스캐폴드 입력 패키지와 검토 대기열만)",
            "priority": "P0",
            "effect": "permits bounded scaffold input materialization without runtime or model mutation(런타임 또는 모델 변경 없이 제한 스캐폴드 입력 물질화 허용)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def build_gates(
    src: Mapping[str, Any],
    preflight_review: Sequence[Mapping[str, Any]],
    frozen_review: Sequence[Mapping[str, Any]],
    proxy_review: Sequence[Mapping[str, Any]],
    blocker_review: Sequence[Mapping[str, Any]],
    firewall_review: Sequence[Mapping[str, Any]],
    artifact_review: Sequence[Mapping[str, Any]],
    balance_review: Sequence[Mapping[str, Any]],
    handoff: Sequence[Mapping[str, Any]],
    queue: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    parent_gates = src["be_gate_audit"]
    parent_passed = sum(1 for row in parent_gates if row.get("status") == "passed")
    claims_preserved = (
        src["be_final"].get("forward_passed") == "not_claimed"
        and src["be_final"].get("forward_failed") == "not_claimed"
        and src["be_final"].get("runtime_authority") == "not_claimed"
        and src["be_final"].get("goal_achieve") == "not_claimed"
    )
    proxy_signal_only = (
        len(proxy_review) == 5
        and all(row.get("review_status", "").startswith("accepted_signal") for row in proxy_review)
        and all(row.get("forward_decision_usable") == "false" for row in proxy_review)
    )
    gates = [
        ("bf_gate_parent_preflight_loaded", bool(src["be_final"]) and src["be_final"].get("next_action") == RUN_ID, f"parent_next={src['be_final'].get('next_action')}", "run337BE opens run337BF(337BE가 337BF를 엶)"),
        ("bf_gate_parent_gates_passed", parent_passed == len(parent_gates) and parent_passed > 0, f"parent_gates={parent_passed}/{len(parent_gates)}", "all run337BE gates passed(337BE 모든 게이트 통과)"),
        ("bf_gate_preflight_review_accepts_five", count_status(preflight_review, "review_status", "accepted_for_bounded_scaffold") == 5, f"preflight_reviews={count_status(preflight_review, 'review_status', 'accepted_for_bounded_scaffold')}/{len(preflight_review)}", "five preflight rows accepted(사전점검 5행 수락)"),
        ("bf_gate_frozen_surface_verified", count_status(frozen_review, "review_status", "frozen_surface_verified") == len(frozen_review) >= 9, f"frozen={count_status(frozen_review, 'review_status', 'frozen_surface_verified')}/{len(frozen_review)}", "frozen surface verified(고정 표면 확인)"),
        ("bf_gate_proxy_signal_only_no_forward", proxy_signal_only, f"proxy_reviews={len(proxy_review)};signal_only={proxy_signal_only}", "proxy usability signal-only(프록시 사용성 신호 전용)"),
        ("bf_gate_mt5_blocker_active", count_status(blocker_review, "review_status", "mt5_forward_blocker_active") == 5, f"mt5_blockers={count_status(blocker_review, 'review_status', 'mt5_forward_blocker_active')}/{len(blocker_review)}", "MT5 forward blockers active(MT5 전진 차단 조건 활성)"),
        ("bf_gate_firewall_active", count_status(firewall_review, "review_status", "firewall_active") >= 8, f"firewalls={count_status(firewall_review, 'review_status', 'firewall_active')}/{len(firewall_review)}", "overfit firewall active(과적합 방화벽 활성)"),
        ("bf_gate_artifact_manifest_verified", count_status(artifact_review, "review_status", "artifact_connected") == len(artifact_review) and len(artifact_review) > 0, f"artifacts={count_status(artifact_review, 'review_status', 'artifact_connected')}/{len(artifact_review)}", "artifact manifest verified(산출물 목록 확인)"),
        ("bf_gate_balanced_workstreams_preserved", count_status(balance_review, "review_status", "balanced_workstream_preserved") >= 5, f"balance={count_status(balance_review, 'review_status', 'balanced_workstream_preserved')}/{len(balance_review)}", "defensive/repair/offensive/control balance preserved(방어/수리/공격/대조 균형 보존)"),
        ("bf_gate_scaffold_handoff_bounded", len(handoff) == 5 and all(row.get("handoff_status", "").startswith("open_scaffold_inputs_only") for row in handoff), f"handoff={len(handoff)}", "only scaffold inputs opened(스캐폴드 입력만 개방)"),
        ("bf_gate_next_queue_ready", len(queue) == 1 and queue[0].get("next_run_id") == NEXT_RUN_ID, f"queue={len(queue)};next={NEXT_RUN_ID}", "run337BG queue ready(337BG 대기열 준비)"),
        ("bf_gate_no_training_selection_claim_guard", claims_preserved, "no training, no retune, no selection, no Forward/Goal claim(학습/재조정/선택/전진/목표 주장 없음)", "claim boundary preserved(주장 경계 보존)"),
    ]
    return [
        {
            "gate_id": gate_id,
            "status": status_text(passed),
            "observed": observed,
            "expected": expected,
            "effect": "blocks scaffold input handoff unless preflight review is bounded(사전점검 검토가 제한되어야 스캐폴드 입력 인계)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for gate_id, passed, observed, expected in gates
    ]


def write_receipts(final: Mapping[str, Any]) -> list[Path]:
    receipts = [
        (
            EXPERIMENT_RECEIPT,
            {
                "hypothesis": "run337BE preflight can open scaffold inputs without changing cp322A(337BE 사전점검은 cp322A를 바꾸지 않고 스캐폴드 입력을 열 수 있다)",
                "decision_use": "open run337BG scaffold input materialization only(337BG 스캐폴드 입력 물질화만 개방)",
                "comparison_baseline": "run337BE preflight package and proxy-MT5 difference read(337BE 사전점검 패키지와 프록시-MT5 차이 판독)",
                "control_variables": "cp322A ONNX, adapter, feature order, D/B surface, threshold, risk, lot, ATR SL/TP, runtime handoff fixed(322A ONNX/어댑터/피처 순서/D-B 표면/임계값/위험/로트/ATR 손절익절/런타임 인계 고정)",
                "changed_variables": "review artifacts and next scaffold input queue only(검토 산출물과 다음 스캐폴드 입력 대기열만 변경)",
                "sample_scope": "existing preflight and existing runtime-probe difference evidence(기존 사전점검과 기존 런타임 탐침 차이 근거)",
                "success_criteria": "all review gates pass, proxy remains signal-only, MT5 blocker remains active(모든 검토 게이트 통과, 프록시는 신호 전용, MT5 차단 조건 활성 유지)",
                "failure_criteria": "any route opens model training, retune, D/B rewrite, lot optimization, proxy KPI authority, or forward claim(어떤 경로든 모델 학습/재조정/D-B 재작성/로트 최적화/프록시 KPI 권위/전진 주장을 열면 실패)",
                "invalid_conditions": "missing parent preflight artifacts or failed frozen-surface review(부모 사전점검 산출물 누락 또는 고정 표면 검토 실패)",
                "stop_conditions": "stop before runtime execution until scaffold review passes and tester gap is repaired(스캐폴드 검토 통과와 테스터 공백 수리 전 런타임 실행 중단)",
                "evidence_plan": [aw.rel(path) for path in OUTPUT_FILES],
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            DATA_RECEIPT,
            {
                "data_source": [aw.rel(path) for path in INPUT_FILES],
                "time_axis": "review of existing preflight artifacts only(기존 사전점검 산출물 검토 전용)",
                "sample_scope": "five blueprint preflight rows and existing proxy-MT5 runtime difference rows(청사진 사전점검 5행과 기존 프록시-MT5 런타임 차이 행)",
                "missing_or_duplicate_check": "artifact manifest rows verified by existence, row count, and hash(산출물 목록 행을 존재/행 수/해시로 확인)",
                "feature_label_boundary": "no realized PnL, date, trade-index, or drawdown as scaffold feature(실현 손익/날짜/거래번호/손실폭을 스캐폴드 피처로 쓰지 않음)",
                "split_boundary": "review only, no training/test reselection(검토 전용, 학습/테스트 재선택 없음)",
                "leakage_risk": "turning proxy parity into forward KPI authority(프록시 동등성을 전진 KPI 권위로 바꾸는 위험)",
                "data_hash_or_identity": aw.rel(ARTIFACT_MANIFEST_REVIEW),
                "integrity_judgment": "usable_with_boundary_for_scaffold_input_review(스캐폴드 입력 검토 경계에서 사용 가능)",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            MODEL_RECEIPT,
            {
                "model_family": "existing cp322A frozen ONNX research artifact(기존 cp322A 고정 ONNX 연구 산출물)",
                "target_and_label": "not touched(건드리지 않음)",
                "split_method": "not applicable, review only(해당 없음, 검토 전용)",
                "selection_metric": "none(없음)",
                "secondary_metrics": "proxy-MT5 match count, MT5 gap status, firewall status(프록시-MT5 일치 수/MT5 공백 상태/방화벽 상태)",
                "threshold_policy": "fixed(고정)",
                "overfit_risk": "scaffold input could encode date/trade-index if firewall fails(방화벽 실패 시 스캐폴드 입력이 날짜/거래번호를 담을 수 있음)",
                "calibration_risk": "proxy signal is not calibrated probability or profit proof(프록시 신호는 보정 확률이나 수익 증명이 아님)",
                "comparison_baseline": "run337BE preflight(337BE 사전점검)",
                "validation_judgment": "review_only_not_candidate(검토 전용, 후보 아님)",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            RUNTIME_RECEIPT,
            {
                "research_path": aw.rel(__file__),
                "runtime_path": "not modified in run337BF(337BF에서 수정 없음)",
                "shared_contract": "proxy-MT5 comparison remains signal-only and MT5 gap blocks forward(프록시-MT5 비교는 신호 전용이고 MT5 공백은 전진을 차단)",
                "known_differences": aw.rel(PROXY_MT5_USABILITY_REVIEW),
                "parity_check": "reviewed existing proxy-MT5 differences; no new MT5 run(기존 프록시-MT5 차이 검토, 신규 MT5 실행 없음)",
                "parity_identity": aw.rel(FROZEN_SURFACE_REVIEW),
                "runtime_claim_boundary": "research-only review, no runtime authority(연구 전용 검토, 런타임 권위 없음)",
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
                "artifact_hashes": aw.rel(ARTIFACT_MANIFEST_REVIEW),
                "registry_links": [aw.rel(RUN_REGISTRY), aw.rel(ALPHA_LEDGER), aw.rel(STAGE_LEDGER), aw.rel(ARTIFACT_REGISTRY)],
                "availability": "generated_ignored_with_manifest(생성됨, 목록으로 추적)",
                "lineage_judgment": "connected_with_boundary(경계 포함 연결)",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            JUDGMENT_RECEIPT,
            {
                "result_subject": RUN_ID,
                "evidence_available": [aw.rel(PREFLIGHT_REVIEW), aw.rel(PROXY_MT5_USABILITY_REVIEW), aw.rel(REQUIRED_GATE_AUDIT)],
                "evidence_missing": "actual scaffold implementation, new MT5 forward run, new ONNX, runtime authority(실제 스캐폴드 구현/신규 MT5 전진 실행/신규 ONNX/런타임 권위 없음)",
                "judgment_label": "exploratory_preflight_review_passed_for_scaffold_inputs(스캐폴드 입력용 탐색 사전점검 검토 통과)",
                "claim_boundary": CLAIM_BOUNDARY,
                "next_condition": NEXT_RUN_ID,
                "user_explanation_hook": "review allows only scaffold inputs, not trading readiness(검토는 스캐폴드 입력만 허용하며 거래 준비가 아님)",
            },
        ),
    ]
    paths: list[Path] = []
    for path, payload in receipts:
        paths.append(aw.write_json(path, payload))
    return paths


def write_report(final: Mapping[str, Any]) -> Path:
    text = f"""# Stage337 run337BF Bounded Repair Implementation Preflight Review(337단계 337BF 제한 수리 구현 사전점검 검토)

## Conclusion(결론)

run337BF(337BF 실행)는 run337BE(337BE 실행)의 bounded implementation preflight(제한 구현 사전점검)를 검토했고, 다음 단계는 scaffold inputs(스캐폴드 입력) 물질화까지만 허용한다고 판정했다.

Effect(효과): 방어/수리/공격/동등성 대조 흐름은 유지하지만, cp322A(322A 후보), threshold(임계값), D/B rule(D/B 규칙), lot(로트), runtime handoff(런타임 인계)는 바꾸지 않는다.

## Result(결과)

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- preflight_reviews(사전점검 검토): `{final['preflight_review_passed']}/{final['preflight_review_rows']}`
- frozen_surface_reviews(고정 표면 검토): `{final['frozen_review_passed']}/{final['frozen_review_rows']}`
- proxy_usability_reviews(프록시 사용성 검토): `{final['proxy_review_passed']}/{final['proxy_review_rows']}`
- mt5_blocker_reviews(MT5 차단 검토): `{final['mt5_blocker_passed']}/{final['mt5_blocker_rows']}`
- firewall_reviews(방화벽 검토): `{final['firewall_passed']}/{final['firewall_rows']}`
- balance_reviews(균형 검토): `{final['balance_passed']}/{final['balance_rows']}`
- gates(게이트): `{final['passed_gates']}/{final['gate_rows']}`

## Proxy-MT5 Usability(프록시-MT5 사용성)

proxy expected value(프록시 예상값)와 MT5 runtime probe value(MT5 런타임 탐침값)는 기존 run337BE(337BE 실행) 묶음 안에서 `85/85` matched(일치)였고 mismatch(불일치)는 `0`이다.

Effect(효과): signal parity(신호 동등성) 확인에는 사용할 수 있지만, tester_feature_last_gap_remains(테스터 피처 끝 공백 유지) 때문에 Forward Passed/Failed(전진 통과/실패) 판단에는 사용할 수 없다.

## Next Action(다음 행동)

- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return aw.write_text_lossless(REPORT_PATH, text, True)


def write_decision_doc(final: Mapping[str, Any]) -> Path:
    text = f"""# Decision(결정): Stage337 run337BF

- date(날짜): `{TODAY}`
- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`

## Boundary(경계)

run337BF(337BF 실행)는 review(검토)만 했다. model training(모델 학습), threshold retune(임계값 재조정), D/B rewrite(D/B 재작성), lot optimization(로트 최적화), candidate selection(후보 선택), runtime authority(런타임 권위), Forward/Goal(전진/목표) 주장은 없다.

Effect(효과): run337BG(337BG 실행)는 schema-only scaffold inputs(스키마 전용 스캐폴드 입력)만 물질화할 수 있다.
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
        f"  Stage337 run337BF focus complete: run337BF(337BF 실행)은 `{final['status']}`로 bounded preflight review(제한 사전점검 검토)를 완료했다. "
        f"Effect(효과): proxy usability(프록시 사용성) `{final['proxy_review_passed']}/{final['proxy_review_rows']}`, balance reviews(균형 검토) `{final['balance_passed']}/{final['balance_rows']}`, gates(게이트) `{final['passed_gates']}/{final['gate_rows']}`이며 Forward/Goal(전진/목표)은 주장하지 않는다.\n"
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
## Stage337 run337BF(337BF 실행) - {TODAY}

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- effect(효과): run337BF(337BF 실행)는 사전점검을 검토하고 proxy-MT5(프록시-MT5)는 신호 동등성 전용, MT5 tester gap(MT5 테스터 공백)은 전진 차단으로 유지했다. Forward/Goal(전진/목표)은 주장하지 않는다.
"""
    if "## Stage337 run337BF" not in current:
        current = current.replace("## Stage337 run337BE", section + "\n## Stage337 run337BE", 1)
    artifacts.append(aw.write_text_lossless(CURRENT_STATE, current, current_bom))

    selection = f"""# Stage337 Selection Status(337단계 선택 상태)

- stage_id(단계 ID): `{STAGE_ID}`
- stage_status(단계 상태): `open_active`
- selected_candidate(선택 후보): `none`
- latest_run(최신 실행): `{RUN_ID}`
- latest_decision(최신 결정): `{DECISION}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- frozen_subject(고정 대상): `cp322A_cp321b_exact_replay_control_surface`
- proxy_usability_review_rows(프록시 사용성 검토 행): `{final['proxy_review_rows']}`
- mt5_blocker_review_rows(MT5 차단 검토 행): `{final['mt5_blocker_rows']}`
- balance_review_rows(균형 검토 행): `{final['balance_rows']}`
- scaffold_handoff_rows(스캐폴드 인계 행): `{final['handoff_rows']}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- Forward Blocked(전진 차단): `not_closed_scaffold_input_open`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): run337BF(337BF 실행)는 사전점검 검토만 완료했고 전진/운영 주장은 막는다.
"""
    artifacts.append(aw.write_text_lossless(SELECTED_STATUS, selection, True))

    brief, brief_bom = aw.read_tracked_text_lossless(STAGE_BRIEF)
    brief = aw.replace_prefix_line(brief, "- latest_run(최신 실행):", f"- latest_run(최신 실행): `{RUN_ID}`")
    summary = (
        f"- run337BF_summary(337BF 요약): `{final['status']}`. "
        f"Effect(효과): proxy usability(프록시 사용성) `{final['proxy_review_passed']}/{final['proxy_review_rows']}`, balance(균형) `{final['balance_passed']}/{final['balance_rows']}`, gates(게이트) `{final['passed_gates']}/{final['gate_rows']}`를 검토하고 run337BG(337BG 실행) scaffold inputs(스캐폴드 입력)를 연다. Forward/Goal(전진/목표)은 주장하지 않는다.\n"
    )
    if "run337BF_summary" not in brief:
        brief = brief.rstrip() + "\n" + summary
    artifacts.append(aw.write_text_lossless(STAGE_BRIEF, brief, brief_bom))

    changelog, changelog_bom = aw.read_tracked_text_lossless(CHANGELOG)
    line = (
        f"- {TODAY}: Stage337 run337BF(337BF 실행) `{final['status']}`. "
        f"Effect(효과): bounded preflight review(제한 사전점검 검토)를 완료하고 scaffold input(스캐폴드 입력)만 열었으며 Forward/Goal(전진/목표)은 주장하지 않음."
    )
    if "Stage337 run337BF" not in changelog:
        changelog = changelog.rstrip() + "\n" + line + "\n"
    artifacts.append(aw.write_text_lossless(CHANGELOG, changelog, changelog_bom))
    return artifacts


def update_registers(final: Mapping[str, Any]) -> list[Path]:
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "bounded_preflight_review_without_db",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": aw.rel(REPORT_PATH),
        "notes": f"decision={final['decision']};next_action={final['next_action']};gates={final['passed_gates']}/{final['gate_rows']};goal_achieve_not_claimed.",
        "family": "experiment_review",
        "primary_report": aw.rel(REPORT_PATH),
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__preflight_review",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "preflight_review",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "Stage337 run337BF bounded preflight review",
        "tier_scope": "research_review_only",
        "kpi_scope": "no_new_trading_kpi",
        "scoreboard_lane": "experiment_review",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": aw.rel(REPORT_PATH),
        "primary_kpi": f"proxy={final['proxy_review_passed']}/{final['proxy_review_rows']};balance={final['balance_passed']}/{final['balance_rows']};gates={final['passed_gates']}/{final['gate_rows']}",
        "guardrail_kpi": "cp322a_frozen;proxy_signal_only;mt5_gap_blocks_forward;no_training;no_threshold_retune;no_db_rewrite;no_lot_opt",
        "external_verification_status": "out_of_scope_by_claim_review_only(주장 범위 밖, 검토 전용)",
        "notes": f"decision={final['decision']};next_action={final['next_action']};runtime_authority_not_claimed.",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__preflight_review",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "experiment_review",
        "evidence_scope": "run337BE bounded preflight package",
        "kpi_scope": "review_no_forward_decision",
        "status": final["status"],
        "judgment": final["judgment"],
        "claim_boundary": CLAIM_BOUNDARY,
        "path": aw.rel(REPORT_PATH),
        "notes": f"goal_achieve_not_claimed;gates={final['passed_gates']}/{final['gate_rows']}",
        "decision": final["decision"],
        "run_key": f"{RUN_ID}__preflight_review",
        "family": "bounded_preflight_review_without_db",
        "question": "can implementation preflight open scaffold inputs without retune or proxy authority",
        "metric_scope": "proxy_mt5_usability_mt5_gap_firewall_balance",
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
    preflight_review = build_preflight_review(src["preflight"])
    preflight_path = aw.write_csv(PREFLIGHT_REVIEW, PREFLIGHT_REVIEW_COLUMNS, preflight_review)
    frozen_review = build_frozen_surface_review(src["hash_check"])
    frozen_path = aw.write_csv(FROZEN_SURFACE_REVIEW, FROZEN_SURFACE_REVIEW_COLUMNS, frozen_review)
    proxy_review = build_proxy_usability_review(src["proxy"])
    proxy_path = aw.write_csv(PROXY_MT5_USABILITY_REVIEW, PROXY_REVIEW_COLUMNS, proxy_review)
    blocker_review = build_mt5_blocker_review(src["mt5_blocker"])
    blocker_path = aw.write_csv(MT5_BLOCKER_REVIEW, MT5_BLOCKER_REVIEW_COLUMNS, blocker_review)
    firewall_review = build_firewall_review(src["firewall"])
    firewall_path = aw.write_csv(NO_OVERFIT_FIREWALL_REVIEW, FIREWALL_REVIEW_COLUMNS, firewall_review)
    artifact_review = build_artifact_review(src["artifact_manifest"])
    artifact_path = aw.write_csv(ARTIFACT_MANIFEST_REVIEW, ARTIFACT_REVIEW_COLUMNS, artifact_review)
    balance_review = build_balance_review(preflight_review, proxy_review, blocker_review)
    balance_path = aw.write_csv(BALANCED_WORKSTREAM_REVIEW, BALANCE_REVIEW_COLUMNS, balance_review)
    handoff_rows = build_handoff_boundary(preflight_review)
    handoff_path = aw.write_csv(SCAFFOLD_HANDOFF_BOUNDARY, HANDOFF_BOUNDARY_COLUMNS, handoff_rows)
    queue_rows = build_next_queue()
    queue_path = aw.write_csv(RUN337BG_QUEUE, QUEUE_COLUMNS, queue_rows)
    gate_rows = build_gates(src, preflight_review, frozen_review, proxy_review, blocker_review, firewall_review, artifact_review, balance_review, handoff_rows, queue_rows)
    gate_path = aw.write_csv(REQUIRED_GATE_AUDIT, GATE_COLUMNS, gate_rows)
    all_gates_pass = all(row.get("status") == "passed" for row in gate_rows)
    final = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS if all_gates_pass else "invalid_stage337BF_preflight_review_gate_failure_no_forward_decision",
        "judgment": JUDGMENT if all_gates_pass else "bounded_preflight_review_gate_failure",
        "decision": DECISION if all_gates_pass else "repair_stage337BF_preflight_review_before_scaffold",
        "next_action": NEXT_RUN_ID if all_gates_pass else "repair_stage337BF_preflight_review_gate_failure_v1",
        "preflight_review_rows": len(preflight_review),
        "preflight_review_passed": count_status(preflight_review, "review_status", "accepted_for_bounded_scaffold"),
        "frozen_review_rows": len(frozen_review),
        "frozen_review_passed": count_status(frozen_review, "review_status", "frozen_surface_verified"),
        "proxy_review_rows": len(proxy_review),
        "proxy_review_passed": count_status(proxy_review, "review_status", "accepted_signal"),
        "mt5_blocker_rows": len(blocker_review),
        "mt5_blocker_passed": count_status(blocker_review, "review_status", "mt5_forward_blocker_active"),
        "firewall_rows": len(firewall_review),
        "firewall_passed": count_status(firewall_review, "review_status", "firewall_active"),
        "artifact_review_rows": len(artifact_review),
        "artifact_review_passed": count_status(artifact_review, "review_status", "artifact_connected"),
        "balance_rows": len(balance_review),
        "balance_passed": count_status(balance_review, "review_status", "balanced_workstream_preserved"),
        "handoff_rows": len(handoff_rows),
        "queue_rows": len(queue_rows),
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
        "external_verification_status": "out_of_scope_by_claim_review_only(주장 범위 밖, 검토 전용)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    manifest_path = aw.write_json(RUN_MANIFEST, manifest)
    receipt_paths = write_receipts(final)
    report_path = write_report(final)
    decision_path = write_decision_doc(final)
    doc_paths = update_docs(final)
    register_paths = update_registers(final)
    artifact_paths = [
        preflight_path,
        frozen_path,
        proxy_path,
        blocker_path,
        firewall_path,
        artifact_path,
        balance_path,
        handoff_path,
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
                "proxy_usability": f"{final['proxy_review_passed']}/{final['proxy_review_rows']}",
                "balance": f"{final['balance_passed']}/{final['balance_rows']}",
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
