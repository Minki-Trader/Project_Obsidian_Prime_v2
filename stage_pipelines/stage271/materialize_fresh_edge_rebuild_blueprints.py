from __future__ import annotations

import csv
import hashlib
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence


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


STAGE_ID = "271_onnx_candidate_campaign__fresh_edge_rebuild_after_nonfilter_failure"
SOURCE_STAGE_ID = "270_onnx_candidate_campaign__aggressive_nonfilter_upside_probe"
RUN_ID = "run271B_materialize_fresh_edge_rebuild_blueprints_v1"
SOURCE_RUN_ID = "run271A_design_fresh_edge_rebuild_queue_v1"
NEXT_ACTION = "run271C_materialize_fresh_edge_scoring_handoff_inputs"
STATUS = "completed_fresh_edge_rebuild_blueprint_materialization_no_candidate_selection"
JUDGMENT = "exploratory_blueprints_materialized_no_candidate_selection"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_"
    "no_deployment_no_onnx_until_candidate_package_gate"
)

FEATURE_ORDER_SOURCE = "docs/contracts/model_input_feature_set_contract_fpmarkets_v2.md"
FEATURE_ORDER_HASH = "fa06973c24462298ea38d84528b07ca0adf357e506f3bfeea02eb0d5691ab8e2"
FEATURE_COUNT = 58
BASE_ADAPTER_OUTPUTS = [
    "entry_signal",
    "route_code",
    "model_risk_pct",
    "atr_stop_multiplier",
    "atr_take_profit_multiplier",
    "max_hold_bars",
    "reentry_cooldown_bars",
]

STAGE_ROOT = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_ROOT / "02_runs" / "run271B"
REVIEWS = STAGE_ROOT / "03_reviews"
SELECTED = STAGE_ROOT / "04_selected"
RUN271A_DIR = STAGE_ROOT / "02_runs" / "run271A"
SOURCE_QUEUE = RUN271A_DIR / "fresh_edge_rebuild_package_queue.csv"
SOURCE_FAILURE_MAP = RUN271A_DIR / "failure_memory_map.csv"
SOURCE_EXPERIMENT_RECEIPT = RUN271A_DIR / "experiment_design_receipt.json"
SOURCE_DATA_RECEIPT = RUN271A_DIR / "data_integrity_receipt.json"
SOURCE_MODEL_RECEIPT = RUN271A_DIR / "model_validation_receipt.json"
SOURCE_LINEAGE_RECEIPT = RUN271A_DIR / "artifact_lineage_receipt.json"
SOURCE_REPORT = STAGE_ROOT / "03_reviews" / "run271A_report.md"

BLUEPRINTS_JSON = RUN_DIR / "fresh_edge_rebuild_blueprints.json"
BLUEPRINTS_CSV = RUN_DIR / "fresh_edge_rebuild_blueprints.csv"
FEATURE_ORDER_PLAN = RUN_DIR / "feature_order_plan.csv"
SCORING_SURFACE_SPECS = RUN_DIR / "scoring_surface_specs.json"
ADAPTER_HANDOFF_SCHEMA = RUN_DIR / "adapter_handoff_schema.csv"
RISK_LOGIC_RECEIPT = RUN_DIR / "risk_logic_receipt.csv"
PACKAGE_IDENTITY_RECEIPTS = RUN_DIR / "package_identity_receipts.csv"
DIFFERENCE_AUDIT_PLAN = RUN_DIR / "difference_audit_plan.csv"
DATA_INTEGRITY_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_VALIDATION_RECEIPT = RUN_DIR / "model_validation_receipt.json"
ARTIFACT_LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
RESULT_JUDGMENT = RUN_DIR / "result_judgment.csv"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"
RUN_REPORT = REVIEWS / "run271B_report.md"
SELECTION_STATUS = SELECTED / "selection_status.md"
REVIEW_INDEX = REVIEWS / "review_index.md"
STAGE_LEDGER = REVIEWS / "stage_run_ledger.csv"
CURRENT_STATE = ROOT / "docs/context/current_working_state.md"
WORKSPACE_STATE = ROOT / "docs/workspace/workspace_state.yaml"
CHANGELOG = ROOT / "docs/workspace/changelog.md"
RUN_REGISTRY = ROOT / "docs/registers/run_registry.csv"
ALPHA_LEDGER = ROOT / "docs/registers/alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs/registers/artifact_registry.csv"
PRODUCER_PATH = Path("stage_pipelines/stage271/materialize_fresh_edge_rebuild_blueprints.py")

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
BLUEPRINT_COLUMNS = (
    "package_id",
    "package_role",
    "materialization_status",
    "hypothesis",
    "decision_use",
    "comparison_baseline",
    "control_variables",
    "changed_variables",
    "sample_scope",
    "feature_order_source",
    "feature_order_hash",
    "feature_surface",
    "feature_owner",
    "model_or_scoring_surface",
    "decision_surface",
    "decision_rule_hash",
    "risk_logic",
    "risk_rule_hash",
    "adapter_output_schema",
    "adapter_schema_hash",
    "runtime_handoff_plan",
    "success_criteria",
    "failure_criteria",
    "invalid_conditions",
    "stop_conditions",
    "evidence_plan",
    "failure_memory",
    "lineage_judgment",
    "claim_boundary",
)
RESULT_COLUMNS = (
    "result_subject",
    "evidence_available",
    "evidence_missing",
    "judgment_label",
    "claim_boundary",
    "next_condition",
    "user_explanation_hook",
)


def rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT).as_posix()


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def write_json(path: Path, payload: Mapping[str, Any]) -> None:
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


def json_load(path: Path) -> dict[str, Any]:
    with io_path(path).open("r", encoding="utf-8-sig") as handle:
        return dict(json.load(handle))


def must_exist(paths: Sequence[Path]) -> None:
    missing = [rel(path) for path in paths if not path_exists(path)]
    if missing:
        raise FileNotFoundError("Missing required source artifacts: " + ", ".join(missing))


def text_hash(parts: Sequence[Any]) -> str:
    return sha256_text(json.dumps(json_ready(list(parts)), ensure_ascii=False, sort_keys=True))


def package_defs(queue_rows: Sequence[Mapping[str, str]]) -> dict[str, dict[str, Any]]:
    queue = {row["package_id"]: dict(row) for row in queue_rows}
    required = {
        "cp271A_damage_first_loss_asymmetry_surface",
        "cp271B_time_risk_phase_router_surface",
        "cp271C_recovery_tail_payoff_rebalance_surface",
        "cp271D_stage270_reference_control_boundary",
    }
    missing = sorted(required.difference(queue))
    if missing:
        raise ValueError("run271A queue is missing package rows: " + ", ".join(missing))
    return {
        "cp271A_damage_first_loss_asymmetry_surface": {
            "package_role": "selectable_blueprint",
            "hypothesis": "damage-first loss-asymmetry(손상 우선 손실 비대칭)가 q03/q01 weak-slice loss(약한 구간 손실)를 줄이면서 거래 공급을 유지할 수 있다",
            "decision_use": "run271C(271C 실행)에서 score table(점수표) 물질화 대상으로 넘길지 결정한다",
            "comparison_baseline": queue["cp271A_damage_first_loss_asymmetry_surface"]["comparison_baseline"],
            "control_variables": queue["cp271A_damage_first_loss_asymmetry_surface"]["control_variables"],
            "changed_variables": "damage_risk_score;opportunity_score;damage_state_skip;side_exposure_cap",
            "sample_scope": queue["cp271A_damage_first_loss_asymmetry_surface"]["sample_scope"],
            "feature_surface": [
                "loss_pressure_state",
                "recent_negative_expectancy",
                "side_specific_damage",
                "weak_slice_overlap",
                "damage_risk_score",
                "opportunity_score",
            ],
            "feature_owner": "stage_pipelines/stage271 until repeated use proves foundation/features owner need",
            "model_or_scoring_surface": "rank-only damage_risk_score(손상 위험 점수) plus opportunity_score(기회 점수)",
            "decision_surface": "enter when opportunity_score >= train_p60 and damage_risk_score <= train_p35 and weak_slice_overlap <= 1",
            "risk_logic": "damage_budget_skip(손상 예산 스킵);loss_streak_cooloff(손실 연속 냉각);side_exposure_cap(방향 노출 제한)",
            "adapter_extensions": [
                "damage_risk_score",
                "opportunity_score",
                "damage_state_code",
                "weak_slice_overlap",
                "risk_action_code",
                "reject_reason",
            ],
            "runtime_handoff_plan": "emit feature_order_hash, blueprint_hash, decision_rule_hash, risk_rule_hash, adapter_schema_hash, package_id, risk_action_code",
            "success_criteria": queue["cp271A_damage_first_loss_asymmetry_surface"]["upside_condition"],
            "failure_criteria": queue["cp271A_damage_first_loss_asymmetry_surface"]["failure_condition"],
            "invalid_conditions": queue["cp271A_damage_first_loss_asymmetry_surface"]["invalid_conditions"],
            "stop_conditions": queue["cp271A_damage_first_loss_asymmetry_surface"]["stop_conditions"],
            "evidence_plan": queue["cp271A_damage_first_loss_asymmetry_surface"]["evidence_plan"],
            "failure_memory": queue["cp271A_damage_first_loss_asymmetry_surface"]["source_failure_memory"],
        },
        "cp271B_time_risk_phase_router_surface": {
            "package_role": "selectable_blueprint",
            "hypothesis": "time-risk phase router(시간 위험 국면 라우터)가 목요일/2025-11/session damage(세션 손상)를 단순 금지가 아니라 상태별 route/abstain(라우트/보류)로 분리할 수 있다",
            "decision_use": "phase route count(국면 경로 수)와 weak-bucket damage(약한 버킷 손상)를 run271C(271C 실행) 점수 물질화로 넘길지 결정한다",
            "comparison_baseline": queue["cp271B_time_risk_phase_router_surface"]["comparison_baseline"],
            "control_variables": queue["cp271B_time_risk_phase_router_surface"]["control_variables"],
            "changed_variables": "weekday_phase;month_regime_pressure;session_clock_risk;chron_phase_age;phase_route_action",
            "sample_scope": queue["cp271B_time_risk_phase_router_surface"]["sample_scope"],
            "feature_surface": [
                "weekday_phase",
                "month_regime_pressure",
                "session_clock_risk",
                "chron_phase_age",
                "phase_risk_score",
                "phase_opportunity_score",
            ],
            "feature_owner": "stage_pipelines/stage271 router blueprint; no foundation owner until reused",
            "model_or_scoring_surface": "rank-only phase_risk_score(국면 위험 점수) plus phase_opportunity_score(국면 기회 점수)",
            "decision_surface": "route, reduce, or abstain by phase_id; damaged phases cannot widen supply",
            "risk_logic": "phase_lot_cap(국면 랏 제한);Thursday_2025_11_guardrail(목요일/2025-11 방어선);session_cooloff(세션 냉각)",
            "adapter_extensions": [
                "phase_id",
                "phase_risk_score",
                "phase_opportunity_score",
                "phase_action_code",
                "route_reason",
                "reject_reason",
            ],
            "runtime_handoff_plan": "emit phase_id, phase_action_code, route_reason, feature_order_hash, decision_rule_hash, risk_rule_hash",
            "success_criteria": queue["cp271B_time_risk_phase_router_surface"]["upside_condition"],
            "failure_criteria": queue["cp271B_time_risk_phase_router_surface"]["failure_condition"],
            "invalid_conditions": queue["cp271B_time_risk_phase_router_surface"]["invalid_conditions"],
            "stop_conditions": queue["cp271B_time_risk_phase_router_surface"]["stop_conditions"],
            "evidence_plan": queue["cp271B_time_risk_phase_router_surface"]["evidence_plan"],
            "failure_memory": queue["cp271B_time_risk_phase_router_surface"]["source_failure_memory"],
        },
        "cp271C_recovery_tail_payoff_rebalance_surface": {
            "package_role": "selectable_blueprint",
            "hypothesis": "recovery-tail payoff rebalance(회복-꼬리 보상 재균형)가 q04 tail reward failure(꼬리 보상 실패)를 극단 보상이 아니라 회복 품질로 다시 설계할 수 있다",
            "decision_use": "bounded payoff/recovery score(경계 보상/회복 점수)를 run271C(271C 실행) 점수 물질화로 넘길지 결정한다",
            "comparison_baseline": queue["cp271C_recovery_tail_payoff_rebalance_surface"]["comparison_baseline"],
            "control_variables": queue["cp271C_recovery_tail_payoff_rebalance_surface"]["control_variables"],
            "changed_variables": "payoff_balance_state;expected_recovery_pressure;drawdown_slope_state;thin_tail_warning;risk_action",
            "sample_scope": queue["cp271C_recovery_tail_payoff_rebalance_surface"]["sample_scope"],
            "feature_surface": [
                "payoff_balance_state",
                "expected_recovery_pressure",
                "drawdown_slope_state",
                "thin_tail_warning",
                "recovery_quality_score",
                "payoff_fragility_score",
            ],
            "feature_owner": "stage_pipelines/stage271 payoff blueprint; promote only after runtime package need",
            "model_or_scoring_surface": "rank-only recovery_quality_score(회복 품질 점수) minus payoff_fragility_score(보상 취약성 점수)",
            "decision_surface": "accept when recovery_quality_score covers payoff_fragility_score and thin_tail_warning is inactive",
            "risk_logic": "bounded_reward_target(경계 보상 목표);drawdown_slope_abort(손실폭 기울기 중단);expectancy_guard(기대값 방어)",
            "adapter_extensions": [
                "target_bucket",
                "recovery_quality_score",
                "payoff_fragility_score",
                "thin_tail_warning",
                "risk_action_code",
                "reject_reason",
            ],
            "runtime_handoff_plan": "emit target_bucket, recovery_quality_score, payoff_fragility_score, risk_action_code, risk_rule_hash",
            "success_criteria": queue["cp271C_recovery_tail_payoff_rebalance_surface"]["upside_condition"],
            "failure_criteria": queue["cp271C_recovery_tail_payoff_rebalance_surface"]["failure_condition"],
            "invalid_conditions": queue["cp271C_recovery_tail_payoff_rebalance_surface"]["invalid_conditions"],
            "stop_conditions": queue["cp271C_recovery_tail_payoff_rebalance_surface"]["stop_conditions"],
            "evidence_plan": queue["cp271C_recovery_tail_payoff_rebalance_surface"]["evidence_plan"],
            "failure_memory": queue["cp271C_recovery_tail_payoff_rebalance_surface"]["source_failure_memory"],
        },
        "cp271D_stage270_reference_control_boundary": {
            "package_role": "support_control",
            "hypothesis": "control boundary(대조 경계)가 새 후보가 q01/q03 이름 바꾸기인지 아닌지 구분한다",
            "decision_use": "difference audit(차이 감사)에서 selectable package(선택 가능 패키지)를 무효화할지 결정한다",
            "comparison_baseline": queue["cp271D_stage270_reference_control_boundary"]["comparison_baseline"],
            "control_variables": queue["cp271D_stage270_reference_control_boundary"]["control_variables"],
            "changed_variables": "none_reference_control_only",
            "sample_scope": queue["cp271D_stage270_reference_control_boundary"]["sample_scope"],
            "feature_surface": [
                "q01_reference_identity",
                "q03_preserved_clue_identity",
                "decision_rule_diff_hash",
                "risk_rule_diff_hash",
            ],
            "feature_owner": "stage_pipelines/stage271 difference audit control only",
            "model_or_scoring_surface": "reference-only identity comparison(참고 전용 정체성 비교)",
            "decision_surface": "not selectable; marks branches invalid if indistinguishable from q01/q03",
            "risk_logic": "no runtime risk logic; control receipt only",
            "adapter_extensions": [
                "reference_package_id",
                "blueprint_diff_hash",
                "decision_diff_flag",
                "risk_diff_flag",
            ],
            "runtime_handoff_plan": "out_of_scope_by_claim(주장 범위 밖); no runtime handoff",
            "success_criteria": "selectable branches prove non-duplicate feature/decision/risk identities",
            "failure_criteria": queue["cp271D_stage270_reference_control_boundary"]["failure_condition"],
            "invalid_conditions": queue["cp271D_stage270_reference_control_boundary"]["invalid_conditions"],
            "stop_conditions": queue["cp271D_stage270_reference_control_boundary"]["stop_conditions"],
            "evidence_plan": queue["cp271D_stage270_reference_control_boundary"]["evidence_plan"],
            "failure_memory": queue["cp271D_stage270_reference_control_boundary"]["source_failure_memory"],
        },
    }


def materialize_blueprints(defs: Mapping[str, Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for package_id, item in defs.items():
        adapter_schema = [*BASE_ADAPTER_OUTPUTS, *item["adapter_extensions"], "feature_order_hash", "package_id", "decision_rule_hash", "risk_rule_hash"]
        decision_rule_hash = text_hash([package_id, item["decision_surface"], item["changed_variables"]])
        risk_rule_hash = text_hash([package_id, item["risk_logic"], item["adapter_extensions"]])
        adapter_schema_hash = sha256_text("\n".join(adapter_schema))
        rows.append(
            {
                "package_id": package_id,
                "package_role": item["package_role"],
                "materialization_status": "blueprint_materialized_no_candidate_selection",
                "hypothesis": item["hypothesis"],
                "decision_use": item["decision_use"],
                "comparison_baseline": item["comparison_baseline"],
                "control_variables": item["control_variables"],
                "changed_variables": item["changed_variables"],
                "sample_scope": item["sample_scope"],
                "feature_order_source": FEATURE_ORDER_SOURCE,
                "feature_order_hash": FEATURE_ORDER_HASH,
                "feature_surface": item["feature_surface"],
                "feature_owner": item["feature_owner"],
                "model_or_scoring_surface": item["model_or_scoring_surface"],
                "decision_surface": item["decision_surface"],
                "decision_rule_hash": decision_rule_hash,
                "risk_logic": item["risk_logic"],
                "risk_rule_hash": risk_rule_hash,
                "adapter_output_schema": adapter_schema,
                "adapter_schema_hash": adapter_schema_hash,
                "runtime_handoff_plan": item["runtime_handoff_plan"],
                "success_criteria": item["success_criteria"],
                "failure_criteria": item["failure_criteria"],
                "invalid_conditions": item["invalid_conditions"],
                "stop_conditions": item["stop_conditions"],
                "evidence_plan": item["evidence_plan"],
                "failure_memory": item["failure_memory"],
                "lineage_judgment": "connected_with_boundary",
                "claim_boundary": BOUNDARY,
            }
        )
    return rows


def semicolon(value: Any) -> str:
    if isinstance(value, list):
        return ";".join(str(item) for item in value)
    return str(value)


def csv_blueprint_rows(blueprints: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return [{column: semicolon(row.get(column, "")) for column in BLUEPRINT_COLUMNS} for row in blueprints]


def feature_order_rows(blueprints: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for row in blueprints:
        derived = list(row["feature_surface"])
        rows.append(
            {
                "package_id": row["package_id"],
                "package_role": row["package_role"],
                "base_feature_count": FEATURE_COUNT,
                "base_feature_order_source": FEATURE_ORDER_SOURCE,
                "base_feature_order_hash": FEATURE_ORDER_HASH,
                "derived_feature_order": ";".join(derived),
                "derived_feature_order_hash": sha256_text("\n".join(derived)),
                "feature_owner": row["feature_owner"],
                "feature_label_boundary": "derived features must use closed bar and historical state only; no future label/future return columns allowed",
                "runtime_order_rule": "base 58 feature order stays unchanged; derived scores are adapter telemetry fields, not ONNX input order yet",
            }
        )
    return rows


def handoff_rows(blueprints: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    fields = [
        "package_id",
        "feature_order_hash",
        "blueprint_hash",
        "decision_rule_hash",
        "risk_rule_hash",
        "adapter_schema_hash",
        "score_columns_hash",
        "claim_boundary",
    ]
    output = []
    for row in blueprints:
        if row["package_role"] == "support_control":
            handoff_plan = "out_of_scope_by_claim(주장 범위 밖)"
            consumer = "run271C_difference_audit_control(271C 차이 감사 대조)"
        else:
            handoff_plan = f"stages/{STAGE_ID}/02_runs/run271C/handoff/{row['package_id']}.json"
            consumer = "run271C_materialize_fresh_edge_scoring_handoff_inputs(271C 점수/인계 입력 물질화)"
        output.append(
            {
                "package_id": row["package_id"],
                "package_role": row["package_role"],
                "adapter_output_schema": ";".join(row["adapter_output_schema"]),
                "adapter_schema_hash": row["adapter_schema_hash"],
                "runtime_handoff_plan": handoff_plan,
                "runtime_payload_fields": ";".join(fields),
                "required_hashes": "feature_order_hash;blueprint_hash;decision_rule_hash;risk_rule_hash;adapter_schema_hash;score_columns_hash",
                "next_consumer": consumer,
                "claim_boundary": BOUNDARY,
            }
        )
    return output


def risk_rows(blueprints: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "package_id": row["package_id"],
            "package_role": row["package_role"],
            "risk_logic": row["risk_logic"],
            "risk_rule_hash": row["risk_rule_hash"],
            "risk_owner": "stage_pipelines/stage271 until Adapter package gate",
            "runtime_meaning": "research risk action only; no live readiness(실거래 준비) or runtime authority(런타임 권위)",
            "failure_condition": row["failure_criteria"],
        }
        for row in blueprints
    ]


def identity_rows(blueprints: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    output = []
    for row in blueprints:
        blueprint_hash = text_hash([row[key] for key in BLUEPRINT_COLUMNS if key in row])
        score_columns = list(row["feature_surface"]) + ["candidate_decision_score", "risk_action_code"]
        output.append(
            {
                "package_id": row["package_id"],
                "package_role": row["package_role"],
                "feature_order_hash": FEATURE_ORDER_HASH,
                "blueprint_hash": blueprint_hash,
                "decision_rule_hash": row["decision_rule_hash"],
                "risk_rule_hash": row["risk_rule_hash"],
                "adapter_schema_hash": row["adapter_schema_hash"],
                "score_columns_hash": sha256_text("\n".join(score_columns)),
                "identity_judgment": "blueprint_identity_materialized_no_performance_claim",
            }
        )
    return output


def scoring_specs_payload(blueprints: Sequence[Mapping[str, Any]], identity: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    hashes = {row["package_id"]: row for row in identity}
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "source_run": SOURCE_RUN_ID,
        "feature_order_source": FEATURE_ORDER_SOURCE,
        "feature_order_hash": FEATURE_ORDER_HASH,
        "claim_boundary": BOUNDARY,
        "packages": [
            {
                "package_id": row["package_id"],
                "package_role": row["package_role"],
                "score_columns": [*row["feature_surface"], "candidate_decision_score", "risk_action_code"],
                "score_columns_hash": hashes[row["package_id"]]["score_columns_hash"],
                "model_or_scoring_surface": row["model_or_scoring_surface"],
                "decision_surface": row["decision_surface"],
                "decision_rule_hash": row["decision_rule_hash"],
                "risk_logic": row["risk_logic"],
                "risk_rule_hash": row["risk_rule_hash"],
                "adapter_schema_hash": row["adapter_schema_hash"],
                "runtime_handoff_plan": row["runtime_handoff_plan"],
                "claim_boundary": BOUNDARY,
            }
            for row in blueprints
        ],
    }


def difference_rows(blueprints: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "audit_id": "run271B_difference_audit_q01_q03_boundary",
            "source_control": "cp271D_stage270_reference_control_boundary",
            "checked_packages": ";".join(row["package_id"] for row in blueprints if row["package_role"] == "selectable_blueprint"),
            "reference_surfaces": "Stage270 q01 control reference(270단계 q01 대조 참고);Stage270 q03 preserved clue(270단계 q03 보존 단서)",
            "required_difference": "feature_surface_hash;decision_rule_hash;risk_rule_hash;adapter_schema_hash must not collapse to q01/q03 identity",
            "invalid_if": "selectable branch only renames Stage270 q01/q03 without a distinct feature/decision/risk surface",
            "next_consumer": NEXT_ACTION,
        }
    ]


def data_integrity_payload(source_hashes: Mapping[str, str]) -> dict[str, Any]:
    return {
        "data_source": {
            "package_queue": rel(SOURCE_QUEUE),
            "failure_memory_map": rel(SOURCE_FAILURE_MAP),
            "stage271_brief": rel(STAGE_ROOT / "00_spec" / "stage_brief.md"),
        },
        "time_axis": "run271B(271B 실행)는 새 bar(봉)를 만들지 않고 Stage270(270단계) failure memory(실패 기억)의 split/tier labels(분할/티어 라벨)만 소비한다",
        "sample_scope": "US100 M5(US100 5분봉), Stage270 validation_is/OOS(검증 표본내/표본외) memory, Tier A plus Tier B planned boundary",
        "missing_or_duplicate_check": "run271A queue has 4 package rows and failure map has 14 memory rows; run271B checks required package ids",
        "feature_label_boundary": "blueprints prohibit future_* and label columns in run271C materialization; derived features must use closed-bar historical state",
        "split_boundary": "no threshold or candidate selected; validation/OOS labels remain source evidence only",
        "leakage_risk": "known weak-slice overfit risk; run271C must test neutral buckets and Tier A/B separation",
        "data_hash_or_identity": dict(source_hashes),
        "integrity_judgment": "usable_with_boundary",
    }


def model_validation_payload(blueprints: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    return {
        "model_family": "planned rank/scoring surfaces only; no trained model in run271B",
        "target_and_label": "uses existing FPMarkets v2 fwd12 label contract later; no label materialized in run271B",
        "split_method": "planned Tier A separate, Tier B separate, Tier A+B combined with validation/OOS source labels",
        "selection_metric": "none_selected; future screen must combine net profit, PF, DD, recovery, expectancy, trade count, and weak-slice damage",
        "secondary_metrics": "phase route count, damage skip count, risk action count, month/weekday/session/chron_segment damage",
        "threshold_policy": "planned quantile thresholds only; run271B hashes rules but does not optimize thresholds",
        "overfit_risk": "high because blueprints are informed by Stage270 weak slices; difference audit and neutral-bucket checks are required",
        "calibration_risk": "rank-only scores, not calibrated probabilities",
        "comparison_baseline": [row["comparison_baseline"] for row in blueprints],
        "validation_judgment": "exploratory_blueprint_only_no_candidate_selection",
    }


def result_rows() -> list[dict[str, str]]:
    return [
        {
            "result_subject": RUN_ID,
            "evidence_available": "blueprints;feature_order_plan;adapter_handoff_schema;risk_logic_receipt;identity_receipts;difference_audit_plan;receipts;ledgers",
            "evidence_missing": "materialized score table;trading KPI;MT5 runtime output;Adapter package;ONNX export/parity;MT5 runtime reproduction",
            "judgment_label": "exploratory_blueprint",
            "claim_boundary": BOUNDARY,
            "next_condition": NEXT_ACTION,
            "user_explanation_hook": "청사진은 물질화됐지만 선택 후보(selected candidate, 선택 후보)는 아직 없다.",
        }
    ]


def report_markdown(blueprints: Sequence[Mapping[str, Any]]) -> str:
    selectable = [row for row in blueprints if row["package_role"] == "selectable_blueprint"]
    lines = "\n".join(
        f"- `{row['package_id']}`: decision_rule_hash(판단 규칙 해시) `{row['decision_rule_hash'][:12]}...`, risk_rule_hash(위험 규칙 해시) `{row['risk_rule_hash'][:12]}...`"
        for row in blueprints
    )
    return f"""# run271B Fresh Edge Rebuild Blueprints(271B 새 거래 우위 재구성 청사진)

- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- package_rows(패키지 행): `{len(blueprints)}`
- selectable_blueprints(선택 가능 청사진): `{len(selectable)}`
- support_controls(보조 대조): `{len(blueprints) - len(selectable)}`
- selected_candidate(선택 후보): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_ACTION}`

## Meaning(의미)

run271B(271B 실행)는 run271A(271A 실행)의 fresh edge rebuild queue(새 거래 우위 재구성 대기열)를 package blueprint(패키지 청사진)로 물질화했다.
효과(effect, 효과): 각 package(패키지)에 feature order hash(피처 순서 해시), decision rule hash(판단 규칙 해시), risk rule hash(위험 규칙 해시), Adapter schema hash(어댑터 스키마 해시), handoff plan(인계 계획)이 생겼다.

## Blueprint Identities(청사진 정체성)

{lines}

## Gate Coverage(게이트 커버리지)

- work_packet_schema_lint(작업 묶음 스키마 점검): `{rel(BLUEPRINTS_JSON)}`
- data_integrity_boundary(데이터 무결성 경계): `{rel(DATA_INTEGRITY_RECEIPT)}`
- model_validation_boundary(모델 검증 경계): `{rel(MODEL_VALIDATION_RECEIPT)}`
- artifact_lineage_audit(산출물 계보 감사): `{rel(ARTIFACT_LINEAGE_RECEIPT)}`
- final_claim_guard(최종 주장 방어): selected candidate(선택 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 주장하지 않는다.

## Boundary(경계)

`{BOUNDARY}`
"""


def manifest_payload(blueprints: Sequence[Mapping[str, Any]], source_hashes: Mapping[str, str]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "source_run": SOURCE_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "producer": rel(ROOT / PRODUCER_PATH),
        "entry_command": f"python {PRODUCER_PATH.as_posix()}",
        "created_at_utc": utc_now(),
        "source_inputs": list(source_hashes.keys()),
        "input_hashes": dict(source_hashes),
        "outputs": {
            "blueprints_json": rel(BLUEPRINTS_JSON),
            "blueprints_csv": rel(BLUEPRINTS_CSV),
            "feature_order_plan": rel(FEATURE_ORDER_PLAN),
            "scoring_surface_specs": rel(SCORING_SURFACE_SPECS),
            "adapter_handoff_schema": rel(ADAPTER_HANDOFF_SCHEMA),
            "risk_logic_receipt": rel(RISK_LOGIC_RECEIPT),
            "package_identity_receipts": rel(PACKAGE_IDENTITY_RECEIPTS),
            "difference_audit_plan": rel(DIFFERENCE_AUDIT_PLAN),
            "report": rel(RUN_REPORT),
        },
        "counts": {
            "package_rows": len(blueprints),
            "selectable_blueprints": sum(1 for row in blueprints if row["package_role"] == "selectable_blueprint"),
            "support_controls": sum(1 for row in blueprints if row["package_role"] == "support_control"),
        },
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": BOUNDARY,
        "next_action": NEXT_ACTION,
    }


def lineage_payload(paths: Sequence[Path], source_hashes: Mapping[str, str]) -> dict[str, Any]:
    return {
        "source_inputs": dict(source_hashes),
        "producer": rel(ROOT / PRODUCER_PATH),
        "consumer": NEXT_ACTION,
        "artifact_paths": [rel(path) for path in paths],
        "artifact_hashes": {rel(path): sha256_file_lf_normalized(path) for path in paths if path_exists(path)},
        "registry_links": {
            "run_registry": rel(RUN_REGISTRY),
            "alpha_ledger": rel(ALPHA_LEDGER),
            "stage_ledger": rel(STAGE_LEDGER),
            "artifact_registry": rel(ARTIFACT_REGISTRY),
        },
        "availability": "tracked_or_reproducible_from_command",
        "lineage_judgment": "connected_with_boundary",
        "claim_boundary": BOUNDARY,
    }


def write_selection_status() -> None:
    text = f"""# Stage271 Selection Status(271단계 선택 상태)

- stage_status(단계 상태): `{STATUS}`
- current_packet(현재 작업 묶음): `stage271_fresh_edge_rebuild_after_nonfilter_failure_v1`
- current_run(현재 실행): `{RUN_ID}`
- last_completed_run(마지막 완료 실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- selected_candidate(선택 후보): `none`
- selected_research_baseline(선택 연구 기준선): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- package_blueprints(패키지 청사진): `{rel(BLUEPRINTS_JSON)}`
- next_action(다음 행동): `{NEXT_ACTION}`

## Current Meaning(현재 의미)

run271B(271B 실행)는 selectable blueprint(선택 가능 청사진) `3`개와 support control(보조 대조) `1`개를 물질화했다.
효과(effect, 효과): 아직 선택 후보가 아니라 run271C(271C 실행)에서 score/handoff input(점수/인계 입력)으로 바꿀 수 있는 추적 가능한 패키지 정체성이 생긴 것이다.

## Boundary(경계)

`{BOUNDARY}`
"""
    write_md(SELECTION_STATUS, text)


def write_review_index() -> None:
    text = f"""# Stage271 Review Index(271단계 검토 색인)

## Current State(현재 상태)

Stage271(271단계)는 run271B(271B 실행) fresh edge rebuild blueprint materialization(새 거래 우위 재구성 청사진 물질화)을 완료했다.
효과(effect, 효과): selected candidate(선택 후보) 없이 run271C(271C 실행) score/handoff input materialization(점수/인계 입력 물질화)로 넘어간다.

## Reports(보고)

- stage brief(단계 개요): `stages/271_onnx_candidate_campaign__fresh_edge_rebuild_after_nonfilter_failure/00_spec/stage_brief.md`
- run271A report(271A 보고): `stages/271_onnx_candidate_campaign__fresh_edge_rebuild_after_nonfilter_failure/03_reviews/run271A_report.md`
- run271B report(271B 보고): `{rel(RUN_REPORT)}`
- run271B blueprints(271B 청사진): `{rel(BLUEPRINTS_JSON)}`
"""
    write_md(REVIEW_INDEX, text)


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


def update_state_docs() -> None:
    current = io_path(CURRENT_STATE).read_text(encoding="utf-8-sig")
    current = replace_line_prefix(current, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_line_prefix(current, "- target_surface(목표 표면):", "- target_surface(목표 표면): `fresh_edge_rebuild_blueprints`")
    current = replace_line_prefix(current, "- status(상태):", f"- status(상태): `{STATUS}`")
    current = replace_line_prefix(current, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    current = append_once(
        current,
        "run271B_summary(271B 요약)",
        f"- run271B_summary(271B 요약): run271B(271B 실행)는 selectable blueprint(선택 가능 청사진) `3`개와 support control(보조 대조) `1`개를 물질화했다. Effect(효과): feature order hash(피처 순서 해시), decision rule hash(판단 규칙 해시), risk rule hash(위험 규칙 해시), Adapter schema hash(어댑터 스키마 해시), handoff plan(인계 계획)을 만들었고, selected candidate(선택 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 주장하지 않는다.",
    )
    write_md(CURRENT_STATE, current)

    workspace = io_path(WORKSPACE_STATE).read_text(encoding="utf-8-sig")
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    workspace = replace_line_prefix(workspace, "active_stage:", f"active_stage: {STAGE_ID}")
    focus = (
        "- >-\n"
        f"  Stage271(271단계) run271B(271B 실행) fresh edge rebuild blueprint materialization(새 거래 우위 재구성 청사진 물질화) `{RUN_ID}`. "
        "Effect(효과): selectable blueprint(선택 가능 청사진) `3`개와 support control(보조 대조) `1`개에 feature/decision/risk/Adapter handoff identity(피처/판단/위험/어댑터 인계 정체성)를 붙였고, selected candidate(선택 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 주장하지 않는다.\n"
    )
    workspace = prepend_focus(workspace, focus, RUN_ID)
    write_md(WORKSPACE_STATE, workspace)

    change = io_path(CHANGELOG).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG) else "# Changelog(변경 기록)\n"
    change = append_once(
        change,
        RUN_ID,
        f"## 2026-05-23 run271B fresh edge rebuild blueprints(271B 새 거래 우위 재구성 청사진)\n\n- status(상태): `{STATUS}`\n- judgment(판정): `{JUDGMENT}`\n- effect(효과): selectable blueprint(선택 가능 청사진) `3`개와 support control(보조 대조) `1`개를 물질화했다.\n- boundary(경계): selected candidate(선택 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 `none/not_claimed`다.\n",
    )
    write_md(CHANGELOG, change)


def update_registers(created_at: str, artifacts: Sequence[Path], blueprints: Sequence[Mapping[str, Any]]) -> None:
    selectable = sum(1 for row in blueprints if row["package_role"] == "selectable_blueprint")
    support = sum(1 for row in blueprints if row["package_role"] == "support_control")
    upsert_csv_rows(
        RUN_REGISTRY,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "experiment_design",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(RUN_REPORT),
                "notes": f"package_rows={len(blueprints)};selectable={selectable};support_control={support};selected_candidate=none;onnx_readiness=not_claimed.",
            }
        ],
        key="run_id",
    )
    alpha_rows = [
        {
            "ledger_row_id": f"{RUN_ID}__tier_a_blueprint",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "tier_a_blueprint",
            "parent_run_id": "",
            "record_view": "Tier A blueprint(티어 A 청사진)",
            "tier_scope": "Tier A separate",
            "kpi_scope": "experiment_design",
            "scoreboard_lane": "fresh_edge_rebuild_blueprints",
            "status": STATUS,
            "judgment": JUDGMENT,
            "path": rel(BLUEPRINTS_JSON),
            "primary_kpi": f"selectable_blueprints={selectable};support_controls={support}",
            "guardrail_kpi": "selected_candidate=none;onnx_readiness=not_claimed;goal_achieve=not_claimed",
            "external_verification_status": "out_of_scope_by_claim_blueprint_only",
            "notes": "Tier A materialization planned in run271C.",
        },
        {
            "ledger_row_id": f"{RUN_ID}__tier_b_blueprint",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "tier_b_blueprint",
            "parent_run_id": "",
            "record_view": "Tier B blueprint(티어 B 청사진)",
            "tier_scope": "Tier B separate",
            "kpi_scope": "experiment_design",
            "scoreboard_lane": "fresh_edge_rebuild_blueprints",
            "status": STATUS,
            "judgment": "planned_with_mirror_boundary_receipt",
            "path": rel(DATA_INTEGRITY_RECEIPT),
            "primary_kpi": "tier_b_status=planned_boundary_not_authority",
            "guardrail_kpi": "no_fallback_authority_claimed",
            "external_verification_status": "out_of_scope_by_claim_blueprint_only",
            "notes": "Tier B must remain separated until actual routed record exists.",
        },
        {
            "ledger_row_id": f"{RUN_ID}__tier_ab_blueprint",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "tier_ab_blueprint",
            "parent_run_id": "",
            "record_view": "Tier A+B blueprint(티어 A+B 청사진)",
            "tier_scope": "Tier A+B combined",
            "kpi_scope": "experiment_design",
            "scoreboard_lane": "fresh_edge_rebuild_blueprints",
            "status": STATUS,
            "judgment": "planned_combined_record_no_performance_claim",
            "path": rel(BLUEPRINTS_JSON),
            "primary_kpi": "combined_record=planned",
            "guardrail_kpi": "performance_claim=none",
            "external_verification_status": "out_of_scope_by_claim_blueprint_only",
            "notes": "Combined record is not synthetic performance.",
        },
    ]
    upsert_csv_rows(ALPHA_LEDGER, ALPHA_LEDGER_COLUMNS, alpha_rows, key="ledger_row_id")
    upsert_csv_rows(
        STAGE_LEDGER,
        STAGE_LEDGER_COLUMNS,
        [
            {
                "row_id": f"{RUN_ID}__blueprint_materialization",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "view": "fresh_edge_rebuild_blueprint_materialization",
                "tier_scope": "Tier A+B paired blueprint",
                "scoreboard": "experiment_design",
                "status": STATUS,
                "judgment": JUDGMENT,
                "evidence_boundary": "blueprint_only_no_candidate_no_onnx",
                "report_path": rel(RUN_REPORT),
                "notes": f"selectable={selectable};support_control={support};next_action={NEXT_ACTION}.",
            }
        ],
        key="row_id",
    )
    if path_exists(ARTIFACT_REGISTRY):
        existing = [
            row
            for row in read_csv_rows(ARTIFACT_REGISTRY)
            if str(row.get("run_id", "")).strip() != RUN_ID
        ]
        write_csv_rows(ARTIFACT_REGISTRY, ARTIFACT_COLUMNS, existing)

    artifact_rows = [
        {
            "artifact_id": f"{RUN_ID}__{path.name.replace('.', '_')}",
            "artifact_type": "run271B_blueprint_artifact",
            "path": rel(path),
            "sha256": sha256_file_lf_normalized(path),
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": created_at,
            "notes": "run271B fresh edge rebuild blueprint artifact.",
        }
        for path in artifacts
        if path_exists(path)
    ]
    upsert_csv_rows(ARTIFACT_REGISTRY, ARTIFACT_COLUMNS, artifact_rows, key="artifact_id")


def run() -> dict[str, Any]:
    sources = [
        SOURCE_QUEUE,
        SOURCE_FAILURE_MAP,
        SOURCE_EXPERIMENT_RECEIPT,
        SOURCE_DATA_RECEIPT,
        SOURCE_MODEL_RECEIPT,
        SOURCE_LINEAGE_RECEIPT,
        SOURCE_REPORT,
        ROOT / FEATURE_ORDER_SOURCE,
    ]
    must_exist(sources)
    io_path(RUN_DIR).mkdir(parents=True, exist_ok=True)
    queue_rows = read_csv_rows(SOURCE_QUEUE)
    defs = package_defs(queue_rows)
    blueprints = materialize_blueprints(defs)
    identity = identity_rows(blueprints)
    source_hashes = {rel(path): sha256_file_lf_normalized(path) for path in sources}

    blueprint_payload = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "source_run": SOURCE_RUN_ID,
        "blueprint_status": STATUS,
        "shared_controls": {
            "symbol": "FPMarkets US100",
            "timeframe": "M5",
            "feature_order_source": FEATURE_ORDER_SOURCE,
            "feature_count": FEATURE_COUNT,
            "feature_order_hash": FEATURE_ORDER_HASH,
            "tier_records_required": ["Tier A separate", "Tier B separate", "Tier A+B combined"],
            "claim_boundary": BOUNDARY,
        },
        "packages": blueprints,
    }
    write_json(BLUEPRINTS_JSON, blueprint_payload)
    write_csv(BLUEPRINTS_CSV, BLUEPRINT_COLUMNS, csv_blueprint_rows(blueprints))
    write_csv(
        FEATURE_ORDER_PLAN,
        (
            "package_id",
            "package_role",
            "base_feature_count",
            "base_feature_order_source",
            "base_feature_order_hash",
            "derived_feature_order",
            "derived_feature_order_hash",
            "feature_owner",
            "feature_label_boundary",
            "runtime_order_rule",
        ),
        feature_order_rows(blueprints),
    )
    write_json(SCORING_SURFACE_SPECS, scoring_specs_payload(blueprints, identity))
    write_csv(
        ADAPTER_HANDOFF_SCHEMA,
        (
            "package_id",
            "package_role",
            "adapter_output_schema",
            "adapter_schema_hash",
            "runtime_handoff_plan",
            "runtime_payload_fields",
            "required_hashes",
            "next_consumer",
            "claim_boundary",
        ),
        handoff_rows(blueprints),
    )
    write_csv(
        RISK_LOGIC_RECEIPT,
        ("package_id", "package_role", "risk_logic", "risk_rule_hash", "risk_owner", "runtime_meaning", "failure_condition"),
        risk_rows(blueprints),
    )
    write_csv(
        PACKAGE_IDENTITY_RECEIPTS,
        (
            "package_id",
            "package_role",
            "feature_order_hash",
            "blueprint_hash",
            "decision_rule_hash",
            "risk_rule_hash",
            "adapter_schema_hash",
            "score_columns_hash",
            "identity_judgment",
        ),
        identity,
    )
    write_csv(
        DIFFERENCE_AUDIT_PLAN,
        ("audit_id", "source_control", "checked_packages", "reference_surfaces", "required_difference", "invalid_if", "next_consumer"),
        difference_rows(blueprints),
    )
    write_json(DATA_INTEGRITY_RECEIPT, data_integrity_payload(source_hashes))
    write_json(MODEL_VALIDATION_RECEIPT, model_validation_payload(blueprints))
    write_csv(RESULT_JUDGMENT, RESULT_COLUMNS, result_rows())
    write_json(RUN_MANIFEST, manifest_payload(blueprints, source_hashes))
    write_md(RUN_REPORT, report_markdown(blueprints))
    write_selection_status()
    write_review_index()

    artifacts = [
        RUN_MANIFEST,
        BLUEPRINTS_JSON,
        BLUEPRINTS_CSV,
        FEATURE_ORDER_PLAN,
        SCORING_SURFACE_SPECS,
        ADAPTER_HANDOFF_SCHEMA,
        RISK_LOGIC_RECEIPT,
        PACKAGE_IDENTITY_RECEIPTS,
        DIFFERENCE_AUDIT_PLAN,
        DATA_INTEGRITY_RECEIPT,
        MODEL_VALIDATION_RECEIPT,
        RESULT_JUDGMENT,
        RUN_REPORT,
        SELECTION_STATUS,
        REVIEW_INDEX,
    ]
    write_json(ARTIFACT_LINEAGE_RECEIPT, lineage_payload([*artifacts, ARTIFACT_LINEAGE_RECEIPT], source_hashes))
    artifacts.append(ARTIFACT_LINEAGE_RECEIPT)

    created_at = utc_now()
    update_registers(created_at, artifacts, blueprints)
    update_state_docs()
    selectable = sum(1 for row in blueprints if row["package_role"] == "selectable_blueprint")
    support = sum(1 for row in blueprints if row["package_role"] == "support_control")
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "package_rows": len(blueprints),
        "selectable_blueprints": selectable,
        "support_controls": support,
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
