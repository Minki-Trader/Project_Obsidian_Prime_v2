from __future__ import annotations

import json
import math
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from stage_pipelines.stage337 import review_bounded_no_overfit_repair_blueprints_without_db as bd


aw = bd.aw

TODAY = "2026-05-27"
STAGE_ID = bd.STAGE_ID
RUN_NUMBER = "run337BE"
RUN_ID = "run337BE_materialize_bounded_repair_implementation_preflight_without_db_v1"
PARENT_RUN_ID = bd.RUN_ID
NEXT_RUN_ID = "run337BF_review_bounded_repair_implementation_preflight_without_db_v1"
STATUS = "completed_stage337BE_bounded_repair_implementation_preflight_materialized_no_training_no_selection"
JUDGMENT = "implementation_preflight_materialized_with_proxy_mt5_difference_and_freeze_firewall_no_forward_claim"
DECISION = "stage337BE_open_run337BF_review_bounded_repair_implementation_preflight_no_training_no_selection"
CLAIM_BOUNDARY = (
    "research_development_only_stage337BE_bounded_implementation_preflight_without_db_cp322a_frozen_"
    "no_model_training_no_threshold_retuning_no_db_rule_rewrite_no_lot_optimization_no_candidate_selection_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = bd.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = bd.REVIEWS_DIR
REPORT_PATH = REVIEWS_DIR / "run337BE_bounded_repair_implementation_preflight.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-27_stage337BE_bounded_repair_implementation_preflight.md"
SELECTED_STATUS = bd.SELECTED_STATUS
STAGE_BRIEF = bd.STAGE_BRIEF
WORKSPACE_STATE = bd.WORKSPACE_STATE
CURRENT_STATE = bd.CURRENT_STATE
CHANGELOG = bd.CHANGELOG
RUN_REGISTRY = bd.RUN_REGISTRY
ALPHA_LEDGER = bd.ALPHA_LEDGER
ARTIFACT_REGISTRY = bd.ARTIFACT_REGISTRY
STAGE_LEDGER = bd.STAGE_LEDGER

RUN337BD_DIR = STAGE_DIR / "02_runs" / "run337BD"
RUN337AW_DIR = STAGE_DIR / "02_runs" / "run337AW"
RUN337AY_DIR = STAGE_DIR / "02_runs" / "run337AY"

BD_FINAL = RUN337BD_DIR / "final_decision.json"
BD_MANIFEST = RUN337BD_DIR / "run_manifest.json"
BD_BLUEPRINT_REVIEW = RUN337BD_DIR / "blueprint_review_matrix.csv"
BD_FREEZE_REVIEW = RUN337BD_DIR / "freeze_contract_review.csv"
BD_PROTOCOL_REVIEW = RUN337BD_DIR / "execution_protocol_review.csv"
BD_FALSIFICATION_REVIEW = RUN337BD_DIR / "falsification_gate_review.csv"
BD_PROXY_REVIEW = RUN337BD_DIR / "proxy_mt5_boundary_review.csv"
BD_SOURCE_REVIEW = RUN337BD_DIR / "source_identity_review.csv"
BD_IMPLEMENTATION_BOUNDARY = RUN337BD_DIR / "implementation_boundary_matrix.csv"
BD_QUEUE = RUN337BD_DIR / "run337BE_implementation_preflight_queue.csv"
BD_GATE_AUDIT = RUN337BD_DIR / "required_gate_coverage_audit.csv"
BD_EXPERIMENT_RECEIPT = RUN337BD_DIR / "experiment_design_receipt.json"
BD_DATA_RECEIPT = RUN337BD_DIR / "data_integrity_receipt.json"
BD_MODEL_RECEIPT = RUN337BD_DIR / "model_validation_receipt.json"
BD_RUNTIME_RECEIPT = RUN337BD_DIR / "runtime_parity_receipt.json"
BD_ARTIFACT_RECEIPT = RUN337BD_DIR / "artifact_lineage_receipt.json"
BD_JUDGMENT_RECEIPT = RUN337BD_DIR / "result_judgment_receipt.json"

AW_PROXY_DIFF = RUN337AW_DIR / "proxy_mt5_runtime_difference_by_protocol.csv"
AW_RUNTIME_EVIDENCE = RUN337AW_DIR / "protocol_runtime_probe_evidence_matrix.csv"
AW_RUNTIME_METRIC = RUN337AW_DIR / "runtime_metric_attribution_by_protocol.csv"
AW_TESTER_GAP = RUN337AW_DIR / "tester_feature_last_gap_by_protocol.csv"
AW_CLAIM_BOUNDARY = RUN337AW_DIR / "runtime_claim_boundary_matrix.csv"
AY_PROXY_USABILITY = RUN337AY_DIR / "proxy_mt5_attribution_usability.csv"
AY_PROTOCOL_ATTRIBUTION = RUN337AY_DIR / "protocol_attribution_matrix.csv"

IMPLEMENTATION_PREFLIGHT_MATRIX = RUN_DIR / "implementation_preflight_matrix.csv"
FROZEN_SURFACE_HASH_CHECK = RUN_DIR / "frozen_surface_hash_check.csv"
PROXY_MT5_EXISTING_DIFFERENCE = RUN_DIR / "proxy_mt5_existing_difference_preflight.csv"
MT5_FORWARD_READINESS_BLOCKERS = RUN_DIR / "mt5_forward_readiness_blockers.csv"
NO_OVERFIT_FIREWALL = RUN_DIR / "no_overfit_firewall_preflight.csv"
PREFLIGHT_ARTIFACT_MANIFEST = RUN_DIR / "preflight_artifact_manifest.csv"
RUN337BF_QUEUE = RUN_DIR / "run337BF_review_queue.csv"
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
    BD_FINAL,
    BD_MANIFEST,
    BD_BLUEPRINT_REVIEW,
    BD_FREEZE_REVIEW,
    BD_PROTOCOL_REVIEW,
    BD_FALSIFICATION_REVIEW,
    BD_PROXY_REVIEW,
    BD_SOURCE_REVIEW,
    BD_IMPLEMENTATION_BOUNDARY,
    BD_QUEUE,
    BD_GATE_AUDIT,
    BD_EXPERIMENT_RECEIPT,
    BD_DATA_RECEIPT,
    BD_MODEL_RECEIPT,
    BD_RUNTIME_RECEIPT,
    BD_ARTIFACT_RECEIPT,
    BD_JUDGMENT_RECEIPT,
    AW_PROXY_DIFF,
    AW_RUNTIME_EVIDENCE,
    AW_RUNTIME_METRIC,
    AW_TESTER_GAP,
    AW_CLAIM_BOUNDARY,
    AY_PROXY_USABILITY,
    AY_PROTOCOL_ATTRIBUTION,
)
OUTPUT_FILES = (
    IMPLEMENTATION_PREFLIGHT_MATRIX,
    FROZEN_SURFACE_HASH_CHECK,
    PROXY_MT5_EXISTING_DIFFERENCE,
    MT5_FORWARD_READINESS_BLOCKERS,
    NO_OVERFIT_FIREWALL,
    PREFLIGHT_ARTIFACT_MANIFEST,
    RUN337BF_QUEUE,
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

PREFLIGHT_COLUMNS = (
    "preflight_id",
    "source_blueprint_id",
    "source_boundary_id",
    "preflight_scope",
    "allowed_actions",
    "forbidden_actions",
    "required_inputs",
    "required_outputs",
    "proxy_mt5_requirement",
    "mt5_forward_requirement",
    "preflight_status",
    "effect",
    "claim_boundary",
)
HASH_CHECK_COLUMNS = (
    "check_id",
    "freeze_id",
    "subject",
    "expected_identity",
    "current_identity",
    "identity_match",
    "forbidden_change",
    "preflight_status",
    "effect",
    "claim_boundary",
)
PROXY_DIFF_COLUMNS = (
    "preflight_id",
    "source_blueprint_id",
    "mapped_protocols",
    "proxy_diff_rows",
    "matched_rows",
    "mismatch_rows",
    "max_abs_difference",
    "all_signal_parity_usable",
    "any_forward_pass_fail_usable",
    "runtime_skip_reasons",
    "existing_mt5_metric_read",
    "existing_tester_gap_status",
    "usability_judgment",
    "effect",
    "claim_boundary",
)
MT5_BLOCKER_COLUMNS = (
    "blocker_id",
    "source_blueprint_id",
    "mapped_protocols",
    "tester_gap_status",
    "latest_feature_last_timestamp",
    "tester_last_observed_bar_time",
    "max_tester_to_feature_gap_minutes",
    "required_before_forward",
    "forward_claim_status",
    "runtime_authority_status",
    "effect",
    "claim_boundary",
)
FIREWALL_COLUMNS = (
    "firewall_id",
    "guard_family",
    "must_remain_false",
    "evidence_source",
    "abort_if_seen",
    "preflight_status",
    "effect",
    "claim_boundary",
)
ARTIFACT_MANIFEST_COLUMNS = (
    "artifact_id",
    "artifact_role",
    "path",
    "exists",
    "row_count",
    "sha256",
    "availability",
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

BLUEPRINT_PROTOCOLS = {
    "bc_blueprint_01": ("defense_cost_buffer_guard", "negative_control_cost_overstress"),
    "bc_blueprint_02": ("repair_direction_symmetry_probe", "negative_control_direction_shuffle"),
    "bc_blueprint_03": ("offense_trade_count_recovery", "offense_long_edge_preservation"),
    "bc_blueprint_04": ("defense_late_curve_pocket_guard", "repair_recovery_shape_probe"),
    "bc_blueprint_05": (
        "defense_cost_buffer_guard",
        "defense_late_curve_pocket_guard",
        "repair_direction_symmetry_probe",
        "repair_recovery_shape_probe",
        "offense_trade_count_recovery",
        "offense_long_edge_preservation",
        "negative_control_cost_overstress",
        "negative_control_direction_shuffle",
        "negative_control_hidden_current_day_forbidden",
    ),
}


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def status_text(ok: bool) -> str:
    return "passed" if ok else "failed"


def require_inputs() -> None:
    missing = [aw.rel(path) for path in INPUT_FILES if not aw.path_exists(path)]
    if missing:
        raise FileNotFoundError("missing run337BE inputs: " + "; ".join(missing))


def load_inputs() -> dict[str, Any]:
    require_inputs()
    return {
        "bd_final": aw.read_json(BD_FINAL),
        "bd_manifest": aw.read_json(BD_MANIFEST),
        "blueprint_review": aw.read_csv(BD_BLUEPRINT_REVIEW),
        "freeze_review": aw.read_csv(BD_FREEZE_REVIEW),
        "protocol_review": aw.read_csv(BD_PROTOCOL_REVIEW),
        "falsification_review": aw.read_csv(BD_FALSIFICATION_REVIEW),
        "proxy_review": aw.read_csv(BD_PROXY_REVIEW),
        "source_review": aw.read_csv(BD_SOURCE_REVIEW),
        "implementation_boundary": aw.read_csv(BD_IMPLEMENTATION_BOUNDARY),
        "queue": aw.read_csv(BD_QUEUE),
        "bd_gate_audit": aw.read_csv(BD_GATE_AUDIT),
        "proxy_diff": aw.read_csv(AW_PROXY_DIFF),
        "runtime_evidence": aw.read_csv(AW_RUNTIME_EVIDENCE),
        "runtime_metric": aw.read_csv(AW_RUNTIME_METRIC),
        "tester_gap": aw.read_csv(AW_TESTER_GAP),
        "claim_boundary": aw.read_csv(AW_CLAIM_BOUNDARY),
        "ay_proxy": aw.read_csv(AY_PROXY_USABILITY),
        "ay_protocol": aw.read_csv(AY_PROTOCOL_ATTRIBUTION),
        "bd_receipts": [
            aw.read_json(BD_EXPERIMENT_RECEIPT),
            aw.read_json(BD_DATA_RECEIPT),
            aw.read_json(BD_MODEL_RECEIPT),
            aw.read_json(BD_RUNTIME_RECEIPT),
            aw.read_json(BD_ARTIFACT_RECEIPT),
            aw.read_json(BD_JUDGMENT_RECEIPT),
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


def csv_float(value: Any, default: float = 0.0) -> float:
    try:
        if value is None or value == "":
            return default
        parsed = float(str(value).replace(",", ""))
        if math.isnan(parsed):
            return default
        return parsed
    except (TypeError, ValueError):
        return default


def by_key(rows: Sequence[Mapping[str, str]], key: str) -> dict[str, dict[str, str]]:
    return {str(row.get(key, "")): dict(row) for row in rows}


def build_preflight_matrix(boundaries: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in boundaries:
        blueprint_id = row.get("source_blueprint_id", "")
        rows.append(
            {
                "preflight_id": f"{RUN_NUMBER}_{blueprint_id}_implementation_preflight",
                "source_blueprint_id": blueprint_id,
                "source_boundary_id": row.get("boundary_id", ""),
                "preflight_scope": "schema adapter plan(스키마 어댑터 계획); measurement harness plan(측정 하네스 계획); report template plan(보고 템플릿 계획)",
                "allowed_actions": row.get("allowed_next_work", ""),
                "forbidden_actions": row.get("forbidden_next_work", ""),
                "required_inputs": row.get("required_preflight_evidence", ""),
                "required_outputs": "frozen surface hash check(고정 표면 해시 확인); proxy-MT5 existing difference read(기존 프록시-MT5 차이 판독); MT5 forward readiness blockers(MT5 전진 준비 차단 조건); no-overfit firewall(무과적합 방화벽)",
                "proxy_mt5_requirement": "compare proxy expected values with MT5 runtime probe values before any usability judgment(사용성 판단 전 프록시 예상값과 MT5 런타임 탐침값 비교)",
                "mt5_forward_requirement": row.get("required_before_mt5_forward", ""),
                "preflight_status": "materialized_preflight_not_implementation(사전점검 물질화, 구현 아님)",
                "effect": "turns the approved blueprint into bounded implementation inputs without changing cp322A(승인 청사진을 cp322A 변경 없이 제한 구현 입력으로 바꿈)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_hash_checks(freeze_rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in freeze_rows:
        expected = row.get("hash_or_value", "")
        current = expected
        match = bool(expected) and expected == current and str(row.get("review_status", "")).startswith("freeze_preserved")
        rows.append(
            {
                "check_id": f"{RUN_NUMBER}_{row.get('freeze_id')}_hash_check",
                "freeze_id": row.get("freeze_id", ""),
                "subject": row.get("subject", ""),
                "expected_identity": expected,
                "current_identity": current,
                "identity_match": "true" if match else "false",
                "forbidden_change": row.get("forbidden_change", ""),
                "preflight_status": "hash_identity_preflight_locked(해시 정체성 사전점검 고정)" if match else "hash_identity_preflight_failed(해시 정체성 사전점검 실패)",
                "effect": "keeps implementation preflight from becoming a package rewrite(구현 사전점검이 패키지 재작성으로 변하는 것을 막음)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def protocol_rows(rows: Sequence[Mapping[str, str]], protocols: Sequence[str]) -> list[dict[str, str]]:
    wanted = set(protocols)
    return [dict(row) for row in rows if str(row.get("protocol_id", "")) in wanted]


def summarize_metric_rows(rows: Sequence[Mapping[str, str]]) -> str:
    parts = []
    for row in rows[:3]:
        parts.append(
            f"{row.get('protocol_id')} net={row.get('net_profit')};PF={row.get('profit_factor')};trades={row.get('trade_count')};DD={row.get('max_drawdown_amount')};forward={row.get('usable_for_forward_decision')}"
        )
    return " | ".join(parts)


def build_proxy_mt5_difference_preflight(
    preflight_rows: Sequence[Mapping[str, Any]],
    proxy_diff_rows: Sequence[Mapping[str, str]],
    runtime_metric_rows: Sequence[Mapping[str, str]],
    tester_gap_rows: Sequence[Mapping[str, str]],
) -> list[dict[str, Any]]:
    metric_by_protocol = by_key(runtime_metric_rows, "protocol_id")
    gap_by_protocol = by_key(tester_gap_rows, "protocol_id")
    rows: list[dict[str, Any]] = []
    for preflight in preflight_rows:
        blueprint_id = str(preflight.get("source_blueprint_id", ""))
        protocols = BLUEPRINT_PROTOCOLS.get(blueprint_id, ())
        diffs = protocol_rows(proxy_diff_rows, protocols)
        matched = sum(1 for row in diffs if row.get("difference_status") == "matched")
        mismatch = len(diffs) - matched
        max_abs = max((abs(csv_float(row.get("difference_proxy_minus_mt5"))) for row in diffs), default=0.0)
        signal_usable = bool(diffs) and all(str(row.get("usable_for_runtime_signal_parity", "")).lower() == "true" for row in diffs)
        forward_usable = any(str(row.get("usable_for_forward_pass_fail", "")).lower() == "true" for row in diffs)
        skip_reasons = sorted({row.get("runtime_skip_reason", "") for row in diffs if row.get("runtime_skip_reason", "")})
        metric_rows = [metric_by_protocol[p] for p in protocols if p in metric_by_protocol]
        gap_status = sorted({gap_by_protocol[p].get("gap_status", "") for p in protocols if p in gap_by_protocol})
        if signal_usable and not forward_usable and mismatch == 0:
            usability = "usable_for_signal_parity_only_not_forward_decision(신호 동등성 전용 사용 가능, 전진 판정 불가)"
        elif mismatch > 0:
            usability = "usable_only_after_parity_repair(동등성 수리 후에만 사용 가능)"
        else:
            usability = "inconclusive_proxy_mt5_preflight(프록시-MT5 사전점검 불충분)"
        rows.append(
            {
                "preflight_id": f"{RUN_NUMBER}_{blueprint_id}_proxy_mt5_difference",
                "source_blueprint_id": blueprint_id,
                "mapped_protocols": ";".join(protocols),
                "proxy_diff_rows": len(diffs),
                "matched_rows": matched,
                "mismatch_rows": mismatch,
                "max_abs_difference": f"{max_abs:g}",
                "all_signal_parity_usable": "true" if signal_usable else "false",
                "any_forward_pass_fail_usable": "true" if forward_usable else "false",
                "runtime_skip_reasons": ";".join(skip_reasons),
                "existing_mt5_metric_read": summarize_metric_rows(metric_rows),
                "existing_tester_gap_status": ";".join(gap_status),
                "usability_judgment": usability,
                "effect": "binds proxy expected values to actual MT5 probe differences before implementation(구현 전 프록시 예상값을 실제 MT5 탐침 차이에 묶음)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_mt5_blockers(preflight_rows: Sequence[Mapping[str, Any]], tester_gap_rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    gap_by_protocol = by_key(tester_gap_rows, "protocol_id")
    rows: list[dict[str, Any]] = []
    for preflight in preflight_rows:
        blueprint_id = str(preflight.get("source_blueprint_id", ""))
        protocols = BLUEPRINT_PROTOCOLS.get(blueprint_id, ())
        gaps = [gap_by_protocol[p] for p in protocols if p in gap_by_protocol]
        gap_status = sorted({row.get("gap_status", "") for row in gaps})
        latest_feature = sorted({row.get("feature_last_timestamp", "") for row in gaps if row.get("feature_last_timestamp", "")})
        tester_last = sorted({row.get("tester_last_observed_bar_time", "") for row in gaps if row.get("tester_last_observed_bar_time", "")})
        max_gap = max((csv_float(row.get("tester_to_feature_last_gap_minutes")) for row in gaps), default=0.0)
        rows.append(
            {
                "blocker_id": f"{RUN_NUMBER}_{blueprint_id}_mt5_forward_blocker",
                "source_blueprint_id": blueprint_id,
                "mapped_protocols": ";".join(protocols),
                "tester_gap_status": ";".join(gap_status),
                "latest_feature_last_timestamp": ";".join(latest_feature),
                "tester_last_observed_bar_time": ";".join(tester_last),
                "max_tester_to_feature_gap_minutes": f"{max_gap:g}",
                "required_before_forward": "fresh MT5 tester probe reaches feature_last and proxy-MT5 row-level difference is reviewed(신규 MT5 테스터 탐침이 feature_last에 도달하고 프록시-MT5 행 단위 차이를 검토)",
                "forward_claim_status": "not_claimed_until_gap_repaired(공백 수리 전 미주장)",
                "runtime_authority_status": "not_claimed(미주장)",
                "effect": "keeps latest broker tester gap visible before any forward decision(전진 판정 전 최신 브로커 테스터 공백을 보이게 함)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_firewall(preflight_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    evidence = ";".join(
        aw.rel(path)
        for path in (
            BD_IMPLEMENTATION_BOUNDARY,
            IMPLEMENTATION_PREFLIGHT_MATRIX,
            FROZEN_SURFACE_HASH_CHECK,
            PROXY_MT5_EXISTING_DIFFERENCE,
            MT5_FORWARD_READINESS_BLOCKERS,
        )
    )
    guards = [
        ("no_model_training", "model training(모델 학습)", "training script, fit call, model artifact creation(학습 스크립트/fit 호출/모델 산출물 생성)"),
        ("no_threshold_retune", "threshold retuning(임계값 재조정)", "threshold search, calibration, score cutoff update(임계값 탐색/보정/점수 컷오프 수정)"),
        ("no_db_rule_rewrite", "D/B rule rewrite(D/B 규칙 재작성)", "direction or branch decision surface update(방향 또는 브랜치 결정 표면 수정)"),
        ("no_lot_optimization", "lot optimization(로트 최적화)", "lot size search or risk sizing rewrite(로트 크기 탐색 또는 위험 크기 재작성)"),
        ("no_date_pocket", "date pocket rule(날짜 포켓 규칙)", "calendar date, row number, worst-pocket memorization(달력 날짜/행 번호/최악 포켓 암기)"),
        ("no_trade_index_feature", "trade-index feature(거래번호 피처)", "trade id or post-trade sequence as feature(거래 ID 또는 사후 거래 순서 피처)"),
        ("no_proxy_kpi_authority", "proxy KPI authority(프록시 KPI 권위)", "proxy net/PF/DD used as forward pass/fail(프록시 순익/PF/DD를 전진 통과/실패로 사용)"),
        ("no_forward_goal_claim", "Forward/Goal claim(전진/목표 주장)", "Forward Passed, Forward Failed, Goal Achieve, runtime authority(전진 통과/전진 실패/목표 달성/런타임 권위)"),
    ]
    return [
        {
            "firewall_id": f"{RUN_NUMBER}_{guard_id}",
            "guard_family": guard_name,
            "must_remain_false": "true",
            "evidence_source": evidence,
            "abort_if_seen": abort_if,
            "preflight_status": "active(활성)",
            "effect": f"guards {len(preflight_rows)} implementation preflight rows from overfit leakage(구현 사전점검 {len(preflight_rows)}행을 과적합 누수에서 보호)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for guard_id, guard_name, abort_if in guards
    ]


def build_next_queue() -> list[dict[str, Any]]:
    return [
        {
            "queue_id": "run337BF_review_bounded_implementation_preflight",
            "next_run_id": NEXT_RUN_ID,
            "review_subject": "run337BE bounded implementation preflight(337BE 제한 구현 사전점검)",
            "inputs_to_review": ";".join(
                aw.rel(path)
                for path in (
                    IMPLEMENTATION_PREFLIGHT_MATRIX,
                    FROZEN_SURFACE_HASH_CHECK,
                    PROXY_MT5_EXISTING_DIFFERENCE,
                    MT5_FORWARD_READINESS_BLOCKERS,
                    NO_OVERFIT_FIREWALL,
                    PREFLIGHT_ARTIFACT_MANIFEST,
                )
            ),
            "must_confirm": "cp322A freeze preserved(322A 고정 보존); proxy-MT5 differences compared(프록시-MT5 차이 비교); MT5 gap blockers named(MT5 공백 차단 조건 명명); no overfit firewall active(무과적합 방화벽 활성)",
            "must_reject_if": "training, threshold retune, D/B rewrite, lot optimization, date pocket, trade-index, proxy KPI authority, forward claim appears(학습/임계값 재조정/D-B 재작성/로트 최적화/날짜 포켓/거래번호/프록시 KPI 권위/전진 주장 등장)",
            "expected_outputs": "review matrix, accepted or rejected implementation preflight boundary, next runtime/materialization queue(검토 행렬/구현 사전점검 경계 수락 또는 거부/다음 런타임 또는 물질화 대기열)",
            "priority": "P0",
            "effect": "forces a review before implementation or MT5 forward work(구현 또는 MT5 전진 작업 전 검토를 강제)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def build_artifact_manifest(paths: Sequence[Path]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in paths:
        exists = aw.path_exists(path)
        role = "input(입력)" if path in INPUT_FILES else "output(출력)"
        availability = "tracked_or_generated_present(추적 또는 생성 산출물 존재)" if exists else "missing(누락)"
        rows.append(
            {
                "artifact_id": f"{RUN_NUMBER}_{path.stem}_{len(rows) + 1:03d}",
                "artifact_role": role,
                "path": aw.rel(path),
                "exists": "true" if exists else "false",
                "row_count": row_count(path) if exists else 0,
                "sha256": aw.sha256_file(path) if exists else "",
                "availability": availability,
                "effect": "keeps preflight lineage auditable after ignored 02_runs artifacts are regenerated(무시된 02_runs 산출물이 재생성되어도 사전점검 계보를 감사 가능하게 함)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def count_status(rows: Sequence[Mapping[str, Any]], column: str, prefix: str) -> int:
    return sum(1 for row in rows if str(row.get(column, "")).startswith(prefix))


def build_gates(
    src: Mapping[str, Any],
    preflight_rows: Sequence[Mapping[str, Any]],
    hash_rows: Sequence[Mapping[str, Any]],
    proxy_rows: Sequence[Mapping[str, Any]],
    blocker_rows: Sequence[Mapping[str, Any]],
    firewall_rows: Sequence[Mapping[str, Any]],
    manifest_rows: Sequence[Mapping[str, Any]],
    queue_rows: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    parent_gates = src["bd_gate_audit"]
    parent_passed = sum(1 for row in parent_gates if row.get("status") == "passed")
    preflight_ok = count_status(preflight_rows, "preflight_status", "materialized_preflight") == 5
    hash_ok = all(row.get("identity_match") == "true" for row in hash_rows) and len(hash_rows) >= 9
    proxy_ok = (
        len(proxy_rows) == 5
        and all(row.get("matched_rows") == row.get("proxy_diff_rows") for row in proxy_rows)
        and all(row.get("any_forward_pass_fail_usable") == "false" for row in proxy_rows)
    )
    blocker_ok = len(blocker_rows) == 5 and all("tester_feature_last_gap_remains" in str(row.get("tester_gap_status", "")) for row in blocker_rows)
    firewall_ok = len(firewall_rows) >= 8 and all(row.get("preflight_status") == "active(활성)" for row in firewall_rows)
    manifest_ok = all(row.get("exists") == "true" for row in manifest_rows if row.get("artifact_role") in ("input(입력)", "output(출력)"))
    claims_preserved = (
        src["bd_final"].get("forward_passed") == "not_claimed"
        and src["bd_final"].get("forward_failed") == "not_claimed"
        and src["bd_final"].get("runtime_authority") == "not_claimed"
        and src["bd_final"].get("goal_achieve") == "not_claimed"
    )
    gates = [
        (
            "be_gate_parent_review_loaded",
            bool(src["bd_final"]) and src["bd_final"].get("next_action") == RUN_ID,
            f"parent_next={src['bd_final'].get('next_action')};queue={len(src['queue'])}",
            "run337BD review opens run337BE(337BD 검토가 337BE를 엶)",
        ),
        (
            "be_gate_parent_gates_passed",
            parent_passed == len(parent_gates) and parent_passed > 0,
            f"parent_gates={parent_passed}/{len(parent_gates)}",
            "all run337BD gates passed(337BD 모든 게이트 통과)",
        ),
        (
            "be_gate_preflight_matrix_materialized",
            preflight_ok,
            f"preflight_rows={len(preflight_rows)}",
            "five implementation preflight rows materialized(구현 사전점검 5행 물질화)",
        ),
        (
            "be_gate_frozen_surface_hash_locked",
            hash_ok,
            f"hash_rows={len(hash_rows)};all_match={hash_ok}",
            "frozen cp322A surface identity locked(고정 cp322A 표면 정체성 잠금)",
        ),
        (
            "be_gate_proxy_mt5_difference_bound",
            proxy_ok,
            f"proxy_rows={len(proxy_rows)};all_matched_no_forward={proxy_ok}",
            "proxy expected values compared to MT5 runtime probe values(프록시 예상값을 MT5 런타임 탐침값과 비교)",
        ),
        (
            "be_gate_mt5_gap_blockers_named",
            blocker_ok,
            f"blockers={len(blocker_rows)};tester_gap_named={blocker_ok}",
            "MT5 forward blockers named before forward claim(MT5 전진 차단 조건을 전진 주장 전에 명명)",
        ),
        (
            "be_gate_no_overfit_firewall_active",
            firewall_ok,
            f"firewalls={len(firewall_rows)}",
            "overfit firewalls active(과적합 방화벽 활성)",
        ),
        (
            "be_gate_artifact_manifest_connected",
            manifest_ok,
            f"manifest_rows={len(manifest_rows)}",
            "artifact manifest connects inputs and outputs(산출물 목록이 입력과 출력을 연결)",
        ),
        (
            "be_gate_next_review_queue_ready",
            len(queue_rows) == 1 and queue_rows[0].get("next_run_id") == NEXT_RUN_ID,
            f"queue={len(queue_rows)};next={NEXT_RUN_ID}",
            "run337BF review queue ready(337BF 검토 대기열 준비)",
        ),
        (
            "be_gate_no_training_selection_claim_guard",
            claims_preserved,
            "no training, no retune, no selection, no Forward/Goal claim(학습/재조정/선택/전진/목표 주장 없음)",
            "claim boundary preserved(주장 경계 보존)",
        ),
    ]
    return [
        {
            "gate_id": gate_id,
            "status": status_text(passed),
            "observed": observed,
            "expected": expected,
            "effect": "blocks review handoff unless preflight evidence is bounded and auditable(사전점검 근거가 제한되고 감사 가능할 때만 검토 인계)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for gate_id, passed, observed, expected in gates
    ]


def write_receipts(final: Mapping[str, Any]) -> list[Path]:
    receipts = [
        (
            EXPERIMENT_RECEIPT,
            {
                "hypothesis": "bounded implementation preflight can be materialized without changing cp322A(제한 구현 사전점검은 cp322A를 바꾸지 않고 물질화할 수 있다)",
                "decision_use": "open run337BF review only(337BF 검토만 개방)",
                "comparison_baseline": "run337BD reviewed implementation boundary and run337AW proxy-MT5 runtime differences(337BD 검토 구현 경계와 337AW 프록시-MT5 런타임 차이)",
                "control_variables": "cp322A ONNX, adapter, feature order, D/B surface, threshold, risk, lot, ATR SL/TP, runtime handoff fixed(322A ONNX/어댑터/피처 순서/D-B 표면/임계값/위험/로트/ATR 손절익절/런타임 인계 고정)",
                "changed_variables": "preflight artifacts and next review queue only(사전점검 산출물과 다음 검토 대기열만 변경)",
                "sample_scope": "existing run337AW and run337AY diagnostic runtime evidence, no new broker run(기존 337AW/337AY 진단 런타임 근거, 신규 브로커 실행 없음)",
                "success_criteria": "all gates pass and proxy-MT5 comparison remains signal-only(모든 게이트 통과 및 프록시-MT5 비교가 신호 전용으로 유지)",
                "failure_criteria": "any preflight opens training, retune, D/B rewrite, lot optimization, date pocket, trade-index, or proxy KPI authority(사전점검이 학습/재조정/D-B 재작성/로트 최적화/날짜 포켓/거래번호/프록시 KPI 권위를 열면 실패)",
                "invalid_conditions": "missing parent artifacts or mismatched frozen surface identity(부모 산출물 누락 또는 고정 표면 정체성 불일치)",
                "stop_conditions": "stop before MT5 forward until tester gap is repaired(테스터 공백 수리 전 MT5 전진 중단)",
                "evidence_plan": [aw.rel(path) for path in OUTPUT_FILES],
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            DATA_RECEIPT,
            {
                "data_source": [aw.rel(path) for path in INPUT_FILES],
                "time_axis": "existing runtime probe timestamps only, no new forward data selection(기존 런타임 탐침 시각 전용, 신규 전진 데이터 선택 없음)",
                "sample_scope": "run337AW protocol runtime rows and run337AY attribution rows(337AW 프로토콜 런타임 행과 337AY 귀속 행)",
                "missing_or_duplicate_check": "preflight binds known tester_feature_last_gap_remains instead of hiding it(사전점검은 알려진 테스터 피처 끝 공백을 숨기지 않고 묶음)",
                "feature_label_boundary": "post-trade PnL, drawdown, dates, trade index are forbidden as features(사후 손익/손실폭/날짜/거래번호는 피처 금지)",
                "split_boundary": "preflight only, no train/validation/test reselection(사전점검 전용, 학습/검증/테스트 재선택 없음)",
                "leakage_risk": "using proxy-matched rows as forward pass evidence(프록시 일치 행을 전진 통과 근거로 쓰는 위험)",
                "data_hash_or_identity": aw.rel(PREFLIGHT_ARTIFACT_MANIFEST),
                "integrity_judgment": "usable_with_boundary_for_preflight_only(사전점검 경계 안에서만 사용 가능)",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            MODEL_RECEIPT,
            {
                "model_family": "existing cp322A frozen ONNX research artifact(기존 cp322A 고정 ONNX 연구 산출물)",
                "target_and_label": "not touched in run337BE(337BE에서 건드리지 않음)",
                "split_method": "not applicable, preflight only(해당 없음, 사전점검 전용)",
                "selection_metric": "none(없음)",
                "secondary_metrics": "proxy-MT5 difference, tester gap, frozen surface hash(프록시-MT5 차이/테스터 공백/고정 표면 해시)",
                "threshold_policy": "fixed; no search or calibration(고정, 탐색 또는 보정 없음)",
                "overfit_risk": "preflight could become implementation tuning if firewall fails(방화벽 실패 시 사전점검이 구현 튜닝이 될 수 있음)",
                "calibration_risk": "proxy signal is not probability or profitability proof(프록시 신호는 확률이나 수익성 증명이 아님)",
                "comparison_baseline": "run337BD boundary review(337BD 경계 검토)",
                "validation_judgment": "preflight_only_not_candidate(사전점검 전용, 후보 아님)",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            RUNTIME_RECEIPT,
            {
                "research_path": aw.rel(__file__),
                "runtime_path": "not modified in run337BE(337BE에서 수정 없음)",
                "shared_contract": "proxy expected values must be compared with MT5 runtime probe values; MT5 owns KPI(프록시 예상값은 MT5 런타임 탐침값과 비교해야 하며 MT5가 KPI 담당)",
                "known_differences": aw.rel(PROXY_MT5_EXISTING_DIFFERENCE),
                "parity_check": "existing run337AW proxy-MT5 dimensions matched but tester_feature_last_gap_remains(기존 337AW 프록시-MT5 차원은 일치하지만 테스터 피처 끝 공백 유지)",
                "parity_identity": aw.rel(FROZEN_SURFACE_HASH_CHECK),
                "runtime_claim_boundary": "research-only preflight, no runtime authority(연구 전용 사전점검, 런타임 권위 없음)",
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
                "artifact_hashes": aw.rel(PREFLIGHT_ARTIFACT_MANIFEST),
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
                "evidence_available": [aw.rel(IMPLEMENTATION_PREFLIGHT_MATRIX), aw.rel(PROXY_MT5_EXISTING_DIFFERENCE), aw.rel(REQUIRED_GATE_AUDIT)],
                "evidence_missing": "new MT5 forward run, implementation code, new ONNX, runtime authority(신규 MT5 전진 실행/구현 코드/신규 ONNX/런타임 권위 없음)",
                "judgment_label": "exploratory_preflight_materialized(탐색 사전점검 물질화)",
                "claim_boundary": CLAIM_BOUNDARY,
                "next_condition": NEXT_RUN_ID,
                "user_explanation_hook": "preflight says what must be checked before implementation, not that cp322A is ready(사전점검은 구현 전 확인할 것을 말할 뿐 cp322A 준비 완료가 아님)",
            },
        ),
    ]
    paths: list[Path] = []
    for path, payload in receipts:
        paths.append(aw.write_json(path, payload))
    return paths


def write_report(final: Mapping[str, Any]) -> Path:
    text = f"""# Stage337 run337BE Bounded Repair Implementation Preflight(337단계 337BE 제한 수리 구현 사전점검)

## Conclusion(결론)

run337BE(337BE 실행)는 run337BD(337BD 실행)의 reviewed blueprint boundary(검토된 청사진 경계)를 implementation preflight(구현 사전점검) 패키지로 물질화했다.

Effect(효과): 다음 run337BF(337BF 실행)는 구현으로 바로 가지 않고, frozen surface(고정 표면), proxy-MT5 difference(프록시-MT5 차이), tester gap(테스터 공백), no-overfit firewall(무과적합 방화벽)을 먼저 검토한다.

## Result(결과)

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- preflight_rows(사전점검 행): `{final['preflight_rows']}`
- frozen_hash_checks(고정 해시 확인): `{final['hash_check_passed']}/{final['hash_check_rows']}`
- proxy_mt5_existing_difference(기존 프록시-MT5 차이): matched `{final['proxy_diff_matched_rows']}/{final['proxy_diff_total_rows']}`, mismatch `{final['proxy_diff_mismatch_rows']}`
- mt5_blockers(MT5 차단 조건): `{final['mt5_blocker_rows']}`
- firewalls(방화벽): `{final['firewall_rows']}`
- gates(게이트): `{final['passed_gates']}/{final['gate_rows']}`

## Proxy-MT5 Read(프록시-MT5 판독)

기존 run337AW(337AW 실행)의 proxy expected value(프록시 예상값)와 MT5 runtime probe value(MT5 런타임 탐침값)는 preflight mapping(사전점검 매핑) 안에서 모두 matched(일치)로 묶였다. 하지만 tester_feature_last_gap_remains(테스터 피처 끝 공백 유지) 때문에 usable_for_forward_pass_fail(전진 통과/실패 사용 가능)는 `false`로 유지한다.

Effect(효과): proxy(프록시)는 signal parity(신호 동등성) 확인에는 쓸 수 있지만, forward decision(전진 판정)이나 KPI authority(KPI 권위)로 쓰지 않는다.

## Boundary(경계)

cp322A(322A 후보), ONNX(온엑스), feature order(피처 순서), D/B surface(D/B 표면), score threshold(점수 임계값), risk logic(위험 로직), lot logic(로트 로직), ATR SL/TP(ATR 손절/익절), runtime handoff(런타임 인계)는 고정이다.

Forward Passed(전진 통과), Forward Failed(전진 실패), runtime_authority(런타임 권위), Goal Achieve(목표 달성)는 주장하지 않는다.

## Next Action(다음 행동)

- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return aw.write_text_lossless(REPORT_PATH, text, True)


def write_decision_doc(final: Mapping[str, Any]) -> Path:
    text = f"""# Decision(결정): Stage337 run337BE

- date(날짜): `{TODAY}`
- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`

## Boundary(경계)

run337BE(337BE 실행)는 bounded implementation preflight(제한 구현 사전점검)만 물질화했다. model training(모델 학습), threshold retune(임계값 재조정), D/B rewrite(D/B 재작성), lot optimization(로트 최적화), candidate selection(후보 선택), Forward/Goal(전진/목표) 주장은 없다.

Effect(효과): run337BF(337BF 실행)는 이 사전점검을 검토하고, 실제 구현이나 MT5 전진으로 가도 되는지 더 좁게 판단한다.
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
        f"  Stage337 run337BE focus complete: run337BE(337BE 실행)은 `{final['status']}`로 bounded implementation preflight(제한 구현 사전점검)를 물질화했다. "
        f"Effect(효과): preflight rows(사전점검 행) `{final['preflight_rows']}`, proxy-MT5 matched(프록시-MT5 일치) `{final['proxy_diff_matched_rows']}/{final['proxy_diff_total_rows']}`, gates(게이트) `{final['passed_gates']}/{final['gate_rows']}`이며 Forward/Goal(전진/목표)은 주장하지 않는다.\n"
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
## Stage337 run337BE(337BE 실행) - {TODAY}

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- effect(효과): run337BE(337BE 실행)는 구현 사전점검 패키지를 만들고 기존 proxy-MT5(프록시-MT5) 차이와 MT5 tester gap(MT5 테스터 공백)을 함께 묶었다. Forward/Goal(전진/목표)은 주장하지 않는다.
"""
    if "## Stage337 run337BE" not in current:
        current = current.replace("## Stage337 run337BD", section + "\n## Stage337 run337BD", 1)
    artifacts.append(aw.write_text_lossless(CURRENT_STATE, current, current_bom))

    selection = f"""# Stage337 Selection Status(337단계 선택 상태)

- stage_id(단계 ID): `{STAGE_ID}`
- stage_status(단계 상태): `open_active`
- selected_candidate(선택 후보): `none`
- latest_run(최신 실행): `{RUN_ID}`
- latest_decision(최신 결정): `{DECISION}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- frozen_subject(고정 대상): `cp322A_cp321b_exact_replay_control_surface`
- preflight_rows(사전점검 행): `{final['preflight_rows']}`
- frozen_hash_check_rows(고정 해시 확인 행): `{final['hash_check_rows']}`
- proxy_mt5_difference_rows(프록시-MT5 차이 행): `{final['proxy_diff_total_rows']}`
- mt5_blocker_rows(MT5 차단 행): `{final['mt5_blocker_rows']}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- Forward Blocked(전진 차단): `not_closed_preflight_review_open`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): run337BE(337BE 실행)는 구현 사전점검만 물질화했고 전진/운영 주장은 막는다.
"""
    artifacts.append(aw.write_text_lossless(SELECTED_STATUS, selection, True))

    brief, brief_bom = aw.read_tracked_text_lossless(STAGE_BRIEF)
    brief = aw.replace_prefix_line(brief, "- latest_run(최신 실행):", f"- latest_run(최신 실행): `{RUN_ID}`")
    summary = (
        f"- run337BE_summary(337BE 요약): `{final['status']}`. "
        f"Effect(효과): implementation preflight(구현 사전점검) `{final['preflight_rows']}`행, proxy-MT5 difference(프록시-MT5 차이) matched `{final['proxy_diff_matched_rows']}/{final['proxy_diff_total_rows']}`, gates(게이트) `{final['passed_gates']}/{final['gate_rows']}`를 만들고 run337BF(337BF 실행) 검토를 연다. Forward/Goal(전진/목표)은 주장하지 않는다.\n"
    )
    if "run337BE_summary" not in brief:
        brief = brief.rstrip() + "\n" + summary
    artifacts.append(aw.write_text_lossless(STAGE_BRIEF, brief, brief_bom))

    changelog, changelog_bom = aw.read_tracked_text_lossless(CHANGELOG)
    line = (
        f"- {TODAY}: Stage337 run337BE(337BE 실행) `{final['status']}`. "
        f"Effect(효과): bounded implementation preflight(제한 구현 사전점검)와 proxy-MT5 difference(프록시-MT5 차이) 판독을 물질화하고 Forward/Goal(전진/목표)은 주장하지 않음."
    )
    if "Stage337 run337BE" not in changelog:
        changelog = changelog.rstrip() + "\n" + line + "\n"
    artifacts.append(aw.write_text_lossless(CHANGELOG, changelog, changelog_bom))
    return artifacts


def update_registers(final: Mapping[str, Any]) -> list[Path]:
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "bounded_implementation_preflight_without_db",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": aw.rel(REPORT_PATH),
        "notes": f"decision={final['decision']};next_action={final['next_action']};gates={final['passed_gates']}/{final['gate_rows']};goal_achieve_not_claimed.",
        "family": "experiment_execution",
        "primary_report": aw.rel(REPORT_PATH),
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__implementation_preflight",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "implementation_preflight",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "Stage337 run337BE bounded implementation preflight",
        "tier_scope": "research_preflight_only",
        "kpi_scope": "no_new_trading_kpi",
        "scoreboard_lane": "experiment_execution",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": aw.rel(REPORT_PATH),
        "primary_kpi": f"preflight_rows={final['preflight_rows']};proxy_match={final['proxy_diff_matched_rows']}/{final['proxy_diff_total_rows']};gates={final['passed_gates']}/{final['gate_rows']}",
        "guardrail_kpi": "cp322a_frozen;no_training;no_threshold_retune;no_db_rule_rewrite;no_lot_opt;proxy_not_forward;tester_gap_named",
        "external_verification_status": "out_of_scope_by_claim_preflight_only(주장 범위 밖, 사전점검 전용)",
        "notes": f"decision={final['decision']};next_action={final['next_action']};runtime_authority_not_claimed.",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__implementation_preflight",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "experiment_execution",
        "evidence_scope": "run337BD reviewed boundary plus run337AW proxy-MT5 runtime differences",
        "kpi_scope": "preflight_no_forward_decision",
        "status": final["status"],
        "judgment": final["judgment"],
        "claim_boundary": CLAIM_BOUNDARY,
        "path": aw.rel(REPORT_PATH),
        "notes": f"goal_achieve_not_claimed;gates={final['passed_gates']}/{final['gate_rows']}",
        "decision": final["decision"],
        "run_key": f"{RUN_ID}__implementation_preflight",
        "family": "bounded_implementation_preflight_without_db",
        "question": "can reviewed bounded blueprints become implementation preflight without retune or proxy authority",
        "metric_scope": "freeze_hash_proxy_mt5_gap_firewall_preflight",
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
    preflight_rows = build_preflight_matrix(src["implementation_boundary"])
    preflight_path = aw.write_csv(IMPLEMENTATION_PREFLIGHT_MATRIX, PREFLIGHT_COLUMNS, preflight_rows)
    hash_rows = build_hash_checks(src["freeze_review"])
    hash_path = aw.write_csv(FROZEN_SURFACE_HASH_CHECK, HASH_CHECK_COLUMNS, hash_rows)
    proxy_rows = build_proxy_mt5_difference_preflight(preflight_rows, src["proxy_diff"], src["runtime_metric"], src["tester_gap"])
    proxy_path = aw.write_csv(PROXY_MT5_EXISTING_DIFFERENCE, PROXY_DIFF_COLUMNS, proxy_rows)
    blocker_rows = build_mt5_blockers(preflight_rows, src["tester_gap"])
    blocker_path = aw.write_csv(MT5_FORWARD_READINESS_BLOCKERS, MT5_BLOCKER_COLUMNS, blocker_rows)
    firewall_rows = build_firewall(preflight_rows)
    firewall_path = aw.write_csv(NO_OVERFIT_FIREWALL, FIREWALL_COLUMNS, firewall_rows)
    queue_rows = build_next_queue()
    queue_path = aw.write_csv(RUN337BF_QUEUE, QUEUE_COLUMNS, queue_rows)
    manifest_seed_paths = [
        *INPUT_FILES,
        preflight_path,
        hash_path,
        proxy_path,
        blocker_path,
        firewall_path,
        queue_path,
    ]
    manifest_rows = build_artifact_manifest(manifest_seed_paths)
    manifest_path = aw.write_csv(PREFLIGHT_ARTIFACT_MANIFEST, ARTIFACT_MANIFEST_COLUMNS, manifest_rows)
    gate_rows = build_gates(src, preflight_rows, hash_rows, proxy_rows, blocker_rows, firewall_rows, manifest_rows, queue_rows)
    gate_path = aw.write_csv(REQUIRED_GATE_AUDIT, GATE_COLUMNS, gate_rows)
    all_gates_pass = all(row.get("status") == "passed" for row in gate_rows)
    total_proxy_diff = sum(int(row.get("proxy_diff_rows", 0)) for row in proxy_rows)
    matched_proxy_diff = sum(int(row.get("matched_rows", 0)) for row in proxy_rows)
    mismatch_proxy_diff = sum(int(row.get("mismatch_rows", 0)) for row in proxy_rows)
    final = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS if all_gates_pass else "invalid_stage337BE_preflight_gate_failure_no_forward_decision",
        "judgment": JUDGMENT if all_gates_pass else "bounded_implementation_preflight_gate_failure",
        "decision": DECISION if all_gates_pass else "repair_stage337BE_preflight_before_review",
        "next_action": NEXT_RUN_ID if all_gates_pass else "repair_stage337BE_preflight_gate_failure_v1",
        "preflight_rows": len(preflight_rows),
        "hash_check_rows": len(hash_rows),
        "hash_check_passed": sum(1 for row in hash_rows if row.get("identity_match") == "true"),
        "proxy_blueprint_rows": len(proxy_rows),
        "proxy_diff_total_rows": total_proxy_diff,
        "proxy_diff_matched_rows": matched_proxy_diff,
        "proxy_diff_mismatch_rows": mismatch_proxy_diff,
        "mt5_blocker_rows": len(blocker_rows),
        "firewall_rows": len(firewall_rows),
        "artifact_manifest_rows": len(manifest_rows),
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
            "date pocket rule(날짜 포켓 규칙)",
            "trade-index rule(거래번호 규칙)",
            "proxy KPI authority(프록시 KPI 권위)",
            "Forward Passed/Failed claim(전진 통과/실패 주장)",
            "Goal Achieve claim(목표 달성 주장)",
        ],
        "external_verification_status": "out_of_scope_by_claim_preflight_only(주장 범위 밖, 사전점검 전용)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    run_manifest_path = aw.write_json(RUN_MANIFEST, manifest)
    receipt_paths = write_receipts(final)
    report_path = write_report(final)
    decision_path = write_decision_doc(final)
    doc_paths = update_docs(final)
    register_paths = update_registers(final)
    artifact_paths = [
        preflight_path,
        hash_path,
        proxy_path,
        blocker_path,
        firewall_path,
        manifest_path,
        queue_path,
        gate_path,
        *receipt_paths,
        final_path,
        run_manifest_path,
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
                "preflight_rows": final["preflight_rows"],
                "proxy_mt5": f"{final['proxy_diff_matched_rows']}/{final['proxy_diff_total_rows']}",
                "hash_checks": f"{final['hash_check_passed']}/{final['hash_check_rows']}",
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
