from __future__ import annotations

import csv
import json
import math
import re
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists  # noqa: E402
from foundation.models.onnx_bridge import sha256_file  # noqa: E402
from stage_pipelines.stage337.design_directional_label_action_repair import (  # noqa: E402
    now_utc,
    read_csv,
    read_json,
    read_text_lossless,
    rel,
    replace_bullet_value,
    upsert_csv,
    write_csv,
    write_json,
    write_md,
    write_text_preserving,
)


TODAY = "2026-05-28"
STAGE_ID = "337_onnx_research_packet__cost_buffer_direction_curve_rebuild"
RUN_NUMBER = "run337DG"
RUN_ID = "run337DG_design_validation_pocket_cost_shape_repair_without_db_v1"
PARENT_RUN_ID = "run337DF_review_cost_shape_two_stage_handoff_training_without_db_v1"
NEXT_RUN_ID = "run337DH_materialize_validation_pocket_cost_shape_repair_inputs_without_db_v1"
STATUS = "completed_stage337DG_validation_pocket_cost_shape_repair_design_no_training_no_selection"
JUDGMENT = "validation_oos_divergence_converted_to_no_overfit_repair_design"
DECISION = "stage337DG_open_run337DH_materialize_validation_pocket_cost_shape_repair_inputs"
CLAIM_BOUNDARY = (
    "research_development_only_stage337DG_validation_pocket_cost_shape_repair_design_without_db_"
    "no_new_training_no_threshold_tuning_no_lot_optimization_no_candidate_selection_no_mt5_probe_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEWS_DIR / "run337DG_validation_pocket_cost_shape_repair_design.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-28_stage337DG_validation_pocket_cost_shape_repair_design.md"
SELECTED_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
STAGE_LEDGER = REVIEWS_DIR / "stage_run_ledger.csv"

DF_DIR = STAGE_DIR / "02_runs" / "run337DF"
DF_FINAL = DF_DIR / "final_decision.json"
DF_GATES = DF_DIR / "required_gate_coverage_audit.csv"
DF_PAIR_SUMMARY = DF_DIR / "pair_validation_oos_summary.csv"
DF_DIVERGENCE = DF_DIR / "validation_oos_divergence_review.csv"
DF_BLOCKERS = DF_DIR / "release_blocker_summary.csv"
DF_MODEL_SUMMARY = DF_DIR / "model_family_summary.csv"
DF_RANK_SUMMARY = DF_DIR / "rank_stage_review_summary.csv"
DF_QUEUE = DF_DIR / "run337DG_repair_design_queue.csv"

DE_PAIR = STAGE_DIR / "02_runs" / "run337DE" / "two_stage_pair_scorecard.csv"
DD_STAGE1 = STAGE_DIR / "02_runs" / "run337DD" / "stage1_cost_tradeability_label_frame.parquet"
DD_STAGE2 = STAGE_DIR / "02_runs" / "run337DD" / "stage2_payoff_rank_handoff_frame.parquet"
DD_POINT = STAGE_DIR / "02_runs" / "run337DD" / "point_cost_identity_sidecar.csv"
DD_MANIFEST = STAGE_DIR / "02_runs" / "run337DD" / "two_stage_handoff_manifest.json"

FAILURE_MEMORY = RUN_DIR / "validation_pocket_failure_memory.csv"
REPAIR_CONTRACT = RUN_DIR / "validation_pf_floor_repair_contract.csv"
SLICE_CONTRACT = RUN_DIR / "slice_stability_design_contract.csv"
PAIR_SMOOTHNESS = RUN_DIR / "pair_cost_surface_smoothness_contract.csv"
FIREWALL = RUN_DIR / "anti_overfit_firewall_contract.csv"
DH_QUEUE = RUN_DIR / "run337DH_materialization_queue.csv"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment_design_receipt.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
REQUIRED_GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (
    DF_FINAL,
    DF_GATES,
    DF_PAIR_SUMMARY,
    DF_DIVERGENCE,
    DF_BLOCKERS,
    DF_MODEL_SUMMARY,
    DF_RANK_SUMMARY,
    DF_QUEUE,
    DE_PAIR,
    DD_STAGE1,
    DD_STAGE2,
    DD_POINT,
    DD_MANIFEST,
)
OUTPUT_FILES = (
    FAILURE_MEMORY,
    REPAIR_CONTRACT,
    SLICE_CONTRACT,
    PAIR_SMOOTHNESS,
    FIREWALL,
    DH_QUEUE,
    EXPERIMENT_RECEIPT,
    DATA_RECEIPT,
    MODEL_RECEIPT,
    PERFORMANCE_RECEIPT,
    JUDGMENT_RECEIPT,
    LINEAGE_RECEIPT,
    REQUIRED_GATE_AUDIT,
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

FAILURE_COLUMNS = (
    "memory_id",
    "evidence_source",
    "observed_pattern",
    "interpretation",
    "repair_use",
    "forbidden_use",
    "effect",
    "claim_boundary",
)
REPAIR_COLUMNS = (
    "contract_id",
    "hypothesis",
    "decision_use",
    "comparison_baseline",
    "control_variables",
    "changed_variables",
    "sample_scope",
    "success_criteria",
    "failure_criteria",
    "invalid_conditions",
    "stop_conditions",
    "evidence_plan",
    "effect",
    "claim_boundary",
)
SLICE_COLUMNS = (
    "slice_contract_id",
    "slice_axis",
    "required_source",
    "minimum_output",
    "success_signal",
    "failure_signal",
    "invalid_condition",
    "forbidden_action",
    "effect",
    "claim_boundary",
)
SMOOTHNESS_COLUMNS = (
    "surface_contract_id",
    "surface_axis",
    "baseline",
    "smoothness_check",
    "pocket_check",
    "blocked_if",
    "effect",
    "claim_boundary",
)
FIREWALL_COLUMNS = (
    "firewall_id",
    "blocked_action",
    "reason",
    "allowed_next_action",
    "release_condition",
    "effect",
    "claim_boundary",
)
QUEUE_COLUMNS = (
    "queue_id",
    "next_run_id",
    "priority",
    "materialization_task",
    "required_inputs",
    "required_outputs",
    "blocked_if_missing",
    "forbidden_action",
    "effect",
    "claim_boundary",
)
GATE_COLUMNS = ("gate_id", "status", "observed", "expected", "effect", "claim_boundary")


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


def append_once(text: str, entry: str, unique: str) -> str:
    if unique in text:
        return text
    return text.rstrip() + "\n" + entry + "\n"


def prepend_once(text: str, heading: str, entry: str, unique: str) -> str:
    if unique in text:
        return text
    return text.replace(heading, f"{heading}\n{entry}", 1)


def summarize_inputs() -> dict[str, Any]:
    final = read_json(DF_FINAL)
    gates = read_csv(DF_GATES)
    pairs = read_csv(DF_PAIR_SUMMARY)
    divergence = read_csv(DF_DIVERGENCE)
    blockers = read_csv(DF_BLOCKERS)
    model_summary = read_csv(DF_MODEL_SUMMARY)
    rank_summary = read_csv(DF_RANK_SUMMARY)
    queue_rows = read_csv(DF_QUEUE)
    blocker_counts = {row.get("release_blocker", ""): as_int(row.get("rows")) for row in blockers}
    best_validation = max((as_float(row.get("validation_pf")) for row in pairs), default=0.0)
    best_oos = max((as_float(row.get("oos_pf")) for row in pairs), default=0.0)
    validation_thin = sum(1 for row in pairs if as_float(row.get("validation_pf")) < 1.05)
    oos_positive_thin = sum(
        1
        for row in pairs
        if as_float(row.get("oos_pf")) >= 1.10 and as_float(row.get("validation_pf")) < 1.05
    )
    divergence_watch = [
        row
        for row in divergence
        if as_float(row.get("pf_gap_oos_minus_validation")) > 0.20
        and as_float(row.get("validation_pf")) < 1.05
    ]
    stage1_rows = [row for row in model_summary if str(row.get("target_family", "")).startswith("stage1_cost_gate")]
    stage2_rows = [row for row in model_summary if str(row.get("target_family", "")).startswith("stage2_")]
    return {
        "final": final,
        "gates": gates,
        "pairs": pairs,
        "divergence": divergence,
        "blockers": blockers,
        "model_summary": model_summary,
        "rank_summary": rank_summary,
        "queue_rows": queue_rows,
        "blocker_counts": blocker_counts,
        "best_validation_pf": best_validation,
        "best_oos_pf": best_oos,
        "validation_thin_rows": validation_thin,
        "oos_positive_thin_rows": oos_positive_thin,
        "divergence_watch_rows": len(divergence_watch),
        "df_failed_gates": [row for row in gates if row.get("status") != "passed"],
        "stage1_best_balanced": max((as_float(row.get("validation_balanced_max")) for row in stage1_rows), default=0.0),
        "stage2_best_balanced": max((as_float(row.get("validation_balanced_max")) for row in stage2_rows), default=0.0),
    }


def build_failure_memory(summary: Mapping[str, Any]) -> list[dict[str, str]]:
    blocker_counts: Mapping[str, int] = summary["blocker_counts"]
    return [
        {
            "memory_id": "validation_pf_floor_block",
            "evidence_source": f"{rel(DF_PAIR_SUMMARY)};{rel(DF_BLOCKERS)}",
            "observed_pattern": f"validation_pf_below_1p05_rows={summary['validation_thin_rows']}; best_validation_pf={summary['best_validation_pf']}",
            "interpretation": "validation edge is too thin for runtime probe(검증 우위가 런타임 탐침에는 얇음)",
            "repair_use": "design train-only cost-shape stability inputs(학습 전용 비용 곡선 안정성 입력 설계)",
            "forbidden_use": "do not lower PF floor or tune threshold on validation/OOS(검증/OOS로 PF 하한이나 임계값을 낮추지 않음)",
            "effect": "turns weak validation into a repair target(약한 검증을 수리 대상으로 전환)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "memory_id": "oos_positive_validation_thin_quarantine",
            "evidence_source": rel(DF_DIVERGENCE),
            "observed_pattern": f"oos_positive_validation_thin_rows={summary['oos_positive_thin_rows']}; divergence_watch_rows={summary['divergence_watch_rows']}; best_oos_pf={summary['best_oos_pf']}",
            "interpretation": "OOS pocket may be regime luck or multiple-testing residue(OOS 포켓은 국면 운 또는 다중시험 잔여일 수 있음)",
            "repair_use": "quarantine OOS as read-only falsification evidence(OOS를 읽기 전용 반증 근거로 격리)",
            "forbidden_use": "do not choose OOS-positive pair as winner(OOS 양호 쌍을 승자로 고르지 않음)",
            "effect": "blocks another overfit path(또 다른 과적합 경로를 차단)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "memory_id": "stage1_signal_stage2_weakness_split",
            "evidence_source": rel(DF_MODEL_SUMMARY),
            "observed_pattern": f"stage1_best_balanced={summary['stage1_best_balanced']}; stage2_best_balanced={summary['stage2_best_balanced']}",
            "interpretation": "cost gate signal exists but stage2 action/rank remains weak(비용 게이트 신호는 있으나 2단계 행동/순위가 약함)",
            "repair_use": "preserve stage1 identity while redesigning stability checks(1단계 정체성을 보존하고 안정성 점검을 재설계)",
            "forbidden_use": "do not present rank score as calibrated probability(순위 점수를 보정된 확률처럼 말하지 않음)",
            "effect": "separates useful signal from unreleased stack(쓸모 있는 신호와 미해제 스택을 분리)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "memory_id": "release_firewall_stays_closed",
            "evidence_source": rel(DF_BLOCKERS),
            "observed_pattern": f"runtime_release_rows=0; blockers={json.dumps(blocker_counts, sort_keys=True)}",
            "interpretation": "release blocker is intentional, not an execution omission(해제 차단은 의도된 판단이지 실행 누락이 아님)",
            "repair_use": "carry no-MT5/no-selection firewall into DH(DH로 MT5 금지/선택 금지 방화벽 이월)",
            "forbidden_use": "do not build MT5 package from DF review(DF 검토만으로 MT5 패키지를 만들지 않음)",
            "effect": "keeps evidence boundary intact(근거 경계를 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_repair_contract(summary: Mapping[str, Any]) -> list[dict[str, str]]:
    return [
        {
            "contract_id": "validation_pf_floor_repair",
            "hypothesis": "Cost-shape stack may need a validation-stable tradeability floor, not a looser threshold(비용 곡선 스택에는 느슨한 임계값이 아니라 검증 안정 거래가능성 하한이 필요할 수 있음)",
            "decision_use": "open DH materialization only(DH 물질화만 개방)",
            "comparison_baseline": rel(DF_PAIR_SUMMARY),
            "control_variables": "same DE models, same feature order, same cost policies, same split(DE 모델/피처 순서/비용 정책/분할 고정)",
            "changed_variables": "diagnostic labels and slice contracts only(진단 라벨과 슬라이스 계약만 변경)",
            "sample_scope": "US100 M5 train/validation/OOS inherited from DD/DE(DD/DE의 US100 M5 학습/검증/OOS)",
            "success_criteria": "DH writes train-only floor inputs and validation read-only audit(DH가 학습 전용 하한 입력과 검증 읽기 전용 감사를 작성)",
            "failure_criteria": "cannot name a non-OOS-selected floor repair(OOS 선택 없는 하한 수리를 이름 붙이지 못함)",
            "invalid_conditions": "threshold or pair is chosen from validation/OOS(검증/OOS에서 임계값이나 쌍을 선택)",
            "stop_conditions": "any release, MT5, or candidate-selection request appears(해제/MT5/후보 선택 요청이 나타남)",
            "evidence_plan": f"{rel(FAILURE_MEMORY)};{rel(SLICE_CONTRACT)};{rel(DH_QUEUE)}",
            "effect": "turns PF weakness into predeclared input work(PF 약점을 사전 선언 입력 작업으로 전환)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "contract_id": "oos_quarantine_falsification",
            "hypothesis": "OOS-positive validation-thin rows should be used as falsification, not selection(OOS 양호/검증 얇음 행은 선택이 아니라 반증에 써야 함)",
            "decision_use": "design quarantine fields for DH(DH 격리 필드 설계)",
            "comparison_baseline": rel(DF_DIVERGENCE),
            "control_variables": "OOS read-only, no thresholds, no lot changes(OOS 읽기 전용/임계값 없음/로트 변경 없음)",
            "changed_variables": "quarantine labels, divergence buckets(격리 라벨/괴리 버킷)",
            "sample_scope": "pair-level DF review rows(DF 쌍 단위 검토 행)",
            "success_criteria": "DH can flag all OOS-positive validation-thin pairs(DH가 모든 OOS 양호/검증 얇음 쌍을 표시)",
            "failure_criteria": "OOS pocket is used to rank-release a pair(OOS 포켓으로 쌍 해제 순위를 만듦)",
            "invalid_conditions": "OOS-derived filtering changes training inputs(OOS 파생 필터가 학습 입력을 바꿈)",
            "stop_conditions": "quarantine cannot be reproduced from DF files(격리를 DF 파일에서 재현할 수 없음)",
            "evidence_plan": rel(DH_QUEUE),
            "effect": "keeps positive-looking OOS honest(좋아 보이는 OOS를 정직한 반증 근거로 둠)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "contract_id": "slice_stability_before_release",
            "hypothesis": "A pair must survive time/regime/cost slices before any runtime handoff(쌍은 런타임 인계 전에 시간/국면/비용 슬라이스를 견뎌야 함)",
            "decision_use": "design required slice outputs(필수 슬라이스 산출물 설계)",
            "comparison_baseline": rel(DE_PAIR),
            "control_variables": "same pair scorecard and DD point-cost identity(같은 쌍 점수표와 DD 포인트 비용 정체성)",
            "changed_variables": "slice attribution artifacts only(슬라이스 귀속 산출물만 변경)",
            "sample_scope": "session, month, volatility, ADX, cost policy, feature set(세션/월/변동성/ADX/비용 정책/피처 묶음)",
            "success_criteria": "DH defines enough slice rows to expose pocket concentration(DH가 포켓 집중을 드러낼 만큼 슬라이스 행을 정의)",
            "failure_criteria": "best OOS pocket comes from one thin slice only(최고 OOS 포켓이 얇은 한 슬라이스에서만 나옴)",
            "invalid_conditions": "slice labels use future outcome beyond declared split(슬라이스 라벨이 선언 분할 밖 미래 결과를 사용)",
            "stop_conditions": "required DD/DE sources are missing(필수 DD/DE 원천 누락)",
            "evidence_plan": f"{rel(SLICE_CONTRACT)};{rel(DD_STAGE2)}",
            "effect": "moves from headline PF to pocket anatomy(헤드라인 PF에서 포켓 해부로 이동)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "contract_id": "pair_surface_smoothness",
            "hypothesis": "Cost-policy neighbors should not flip from weak validation to strong OOS by chance(비용 정책 이웃이 우연히 약한 검증에서 강한 OOS로 뒤집히면 안 됨)",
            "decision_use": "design pair-neighborhood checks(쌍 이웃 점검 설계)",
            "comparison_baseline": rel(DF_PAIR_SUMMARY),
            "control_variables": "cost policies extra0/extra2/extra5 and model configs fixed(extra0/extra2/extra5 비용 정책과 모델 설정 고정)",
            "changed_variables": "surface smoothness diagnostics(표면 매끄러움 진단)",
            "sample_scope": "pair rows grouped by feature set and model config(피처 묶음/모델 설정별 쌍 행)",
            "success_criteria": "DH can mark isolated OOS pockets(DH가 고립 OOS 포켓을 표시)",
            "failure_criteria": "all apparent edge is isolated to one cost policy(겉보기 우위가 한 비용 정책에만 고립)",
            "invalid_conditions": "neighbor check changes the model or threshold(이웃 점검이 모델/임계값을 바꿈)",
            "stop_conditions": "pair scorecard lacks comparable cost policies(쌍 점수표에 비교 가능한 비용 정책이 없음)",
            "evidence_plan": rel(PAIR_SMOOTHNESS),
            "effect": "reduces surface-mining risk(표면 채굴 위험을 낮춤)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_slice_contract() -> list[dict[str, str]]:
    axes = [
        ("session", "session bucket from timestamp(시각 기반 세션 버킷)"),
        ("hour", "UTC hour from bar close(봉 마감 UTC 시각)"),
        ("month", "calendar month from bar close(봉 마감 월)"),
        ("volatility", "ATR/realized range bucket(ATR/실현 범위 버킷)"),
        ("adx", "ADX state bucket(ADX 상태 버킷)"),
        ("cost_policy", "spread_plus_extra policy(스프레드+추가 비용 정책)"),
        ("feature_set", "feature-set identity(피처 묶음 정체성)"),
        ("model_config", "model family/config(모델 계열/설정)"),
    ]
    rows: list[dict[str, str]] = []
    for axis, source in axes:
        rows.append(
            {
                "slice_contract_id": f"slice_{axis}",
                "slice_axis": axis,
                "required_source": f"{source}; {rel(DD_STAGE2)}; {rel(DF_PAIR_SUMMARY)}",
                "minimum_output": "split, trades, net_after_cost, pf, concentration_share(분할/거래/비용 후 순익/PF/집중 비율)",
                "success_signal": "validation is not negative in broad slices and OOS is not isolated(넓은 슬라이스에서 검증이 음수가 아니고 OOS가 고립되지 않음)",
                "failure_signal": "edge appears only in OOS or one thin slice(우위가 OOS나 얇은 한 슬라이스에만 나타남)",
                "invalid_condition": "slice assignment uses future outcome(슬라이스 배정이 미래 결과를 사용)",
                "forbidden_action": "no model selection from slice winners(슬라이스 승자로 모델 선택 금지)",
                "effect": "defines stability evidence before training or MT5(학습/MT5 전 안정성 근거 정의)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_pair_smoothness() -> list[dict[str, str]]:
    return [
        {
            "surface_contract_id": "cost_policy_neighbor_smoothness",
            "surface_axis": "spread_plus_extra0_points -> extra2 -> extra5",
            "baseline": rel(DF_PAIR_SUMMARY),
            "smoothness_check": "PF/net/trade_count should degrade or improve gradually across cost policies(PF/순익/거래수가 비용 정책 사이에서 급격히 튀지 않아야 함)",
            "pocket_check": "flag one-policy OOS spike with weak validation(검증 약함 + 한 정책 OOS 급등 표시)",
            "blocked_if": "best pair exists only at one cost and validation PF remains below 1.05(최고 쌍이 한 비용에만 있고 검증 PF가 1.05 미만)",
            "effect": "prevents cost-level cherry-pick(비용 수준 골라잡기를 막음)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "surface_contract_id": "feature_set_neighbor_smoothness",
            "surface_axis": "technical_session_vol_lag_safe, macro_equity_lag_safe_rescue, state_carry_ge70_pruned_cost_context",
            "baseline": rel(DF_PAIR_SUMMARY),
            "smoothness_check": "same model config should not depend on a single rescued feature pocket(같은 모델 설정이 구조된 한 피처 포켓에만 의존하지 않아야 함)",
            "pocket_check": "flag feature-set-only OOS pocket(피처 묶음 단독 OOS 포켓 표시)",
            "blocked_if": "OOS PF is strong but validation net is negative( OOS PF는 강하지만 검증 순익이 음수)",
            "effect": "separates feature context from pocket luck(피처 문맥과 포켓 운을 분리)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "surface_contract_id": "model_family_surface_check",
            "surface_axis": "logreg_balanced_c075 vs extratrees_depth6_leaf160",
            "baseline": rel(DF_MODEL_SUMMARY),
            "smoothness_check": "tree-only OOS improvement must be checked against weak stage2 labels(tree 단독 OOS 개선은 약한 2단계 라벨과 대조)",
            "pocket_check": "flag model-family-only OOS pocket(모델 계열 단독 OOS 포켓 표시)",
            "blocked_if": "stage2 balanced score remains weak and pair PF relies on one model family(2단계 균형 점수가 약하고 쌍 PF가 한 모델 계열에 의존)",
            "effect": "keeps model complexity from masking label weakness(모델 복잡도가 라벨 약점을 숨기지 못하게 함)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_firewall() -> list[dict[str, str]]:
    return [
        {
            "firewall_id": "no_oos_winner_selection",
            "blocked_action": "candidate selection from OOS-positive rows(OOS 양호 행으로 후보 선택)",
            "reason": "DF found OOS-positive/validation-thin watch(DF가 OOS 양호/검증 얇음 감시를 찾음)",
            "allowed_next_action": NEXT_RUN_ID,
            "release_condition": "predeclared validation/slice repair survives review(사전 선언 검증/슬라이스 수리가 검토를 통과)",
            "effect": "prevents overfit handoff(과적합 인계를 방지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "firewall_id": "no_threshold_tuning",
            "blocked_action": "score threshold change(점수 임계값 변경)",
            "reason": "threshold tuning would convert review evidence into selection(임계값 튜닝은 검토 근거를 선택으로 바꿈)",
            "allowed_next_action": "materialize diagnostics only(진단만 물질화)",
            "release_condition": "separate predeclared training stage exists(별도 사전 선언 학습 단계가 존재)",
            "effect": "keeps validation read-only(검증을 읽기 전용으로 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "firewall_id": "no_lot_optimization",
            "blocked_action": "lot or sizing optimization(로트 또는 사이징 최적화)",
            "reason": "cost-shape weakness must not be hidden by sizing(비용 곡선 약점을 사이징으로 숨기면 안 됨)",
            "allowed_next_action": "lot-normalized diagnostics only(로트 정규화 진단만 허용)",
            "release_condition": "after model and cost surface pass without sizing help(사이징 도움 없이 모델/비용 표면 통과 후)",
            "effect": "keeps signal quality visible(신호 품질을 보이게 함)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "firewall_id": "no_mt5_probe",
            "blocked_action": "MT5 runtime probe or package(MT5 런타임 탐침 또는 패키지)",
            "reason": "runtime release rows are zero(런타임 해제 행이 0)",
            "allowed_next_action": NEXT_RUN_ID,
            "release_condition": "review explicitly opens runtime probe after repair(수리 후 검토가 명시적으로 런타임 탐침을 개방)",
            "effect": "keeps runtime claim closed(런타임 주장을 닫아 둠)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "firewall_id": "no_forward_claim",
            "blocked_action": "Forward Passed/Failed or Goal Achieve(전진 통과/실패 또는 목표 달성)",
            "reason": "DG is design only(DG는 설계 전용)",
            "allowed_next_action": "record research decision only(연구 결정만 기록)",
            "release_condition": "future forward protocol with required evidence(향후 필수 근거가 있는 전진 프로토콜)",
            "effect": "prevents premature closure(성급한 종료를 방지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_queue() -> list[dict[str, str]]:
    return [
        {
            "queue_id": "run337DH_materialize_validation_pf_floor_inputs",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "materialization_task": "build validation PF floor repair input frame without threshold tuning(임계값 튜닝 없이 검증 PF 하한 수리 입력 프레임 생성)",
            "required_inputs": f"{rel(DF_PAIR_SUMMARY)};{rel(DF_DIVERGENCE)};{rel(DD_STAGE1)};{rel(DD_STAGE2)}",
            "required_outputs": "validation_pf_floor_input_frame;floor_audit(검증 PF 하한 입력 프레임/하한 감사)",
            "blocked_if_missing": "DF pair rows or DD two-stage frames(DF 쌍 행 또는 DD 2단계 프레임)",
            "forbidden_action": "no validation/OOS threshold fitting(검증/OOS 임계값 맞춤 금지)",
            "effect": "makes thin validation a measurable repair target(얇은 검증을 측정 가능한 수리 대상으로 만듦)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run337DH_materialize_slice_stability_frame",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "materialization_task": "materialize session/month/volatility/ADX/cost-policy slices(세션/월/변동성/ADX/비용 정책 슬라이스 물질화)",
            "required_inputs": f"{rel(SLICE_CONTRACT)};{rel(DD_STAGE2)};{rel(DD_POINT)}",
            "required_outputs": "slice_stability_frame;slice_pocket_audit(슬라이스 안정성 프레임/포켓 감사)",
            "blocked_if_missing": "timestamp or cost identity fields(시각 또는 비용 정체성 필드)",
            "forbidden_action": "no pair selection from slice winners(슬라이스 승자로 쌍 선택 금지)",
            "effect": "checks pocket anatomy before any runtime route(런타임 경로 전 포켓 해부를 점검)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run337DH_materialize_oos_quarantine_audit",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "materialization_task": "mark OOS-positive validation-thin rows as quarantine/falsification(OOS 양호/검증 얇음 행을 격리/반증으로 표시)",
            "required_inputs": f"{rel(DF_DIVERGENCE)};{rel(FIREWALL)}",
            "required_outputs": "oos_quarantine_audit;forbidden_selection_audit(OOS 격리 감사/금지 선택 감사)",
            "blocked_if_missing": "divergence rows(괴리 행)",
            "forbidden_action": "no OOS winner promotion(OOS 승자 승격 금지)",
            "effect": "turns attractive OOS into a test, not a choice(매력적인 OOS를 선택이 아닌 시험으로 전환)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run337DH_materialize_pair_surface_controls",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P1",
            "materialization_task": "build cost-policy/feature/model smoothness control matrix(비용 정책/피처/모델 표면 매끄러움 대조 행렬 생성)",
            "required_inputs": f"{rel(PAIR_SMOOTHNESS)};{rel(DE_PAIR)};{rel(DF_MODEL_SUMMARY)}",
            "required_outputs": "pair_surface_smoothness_matrix;isolated_pocket_flags(쌍 표면 매끄러움 행렬/고립 포켓 표시)",
            "blocked_if_missing": "comparable pair rows(비교 가능한 쌍 행)",
            "forbidden_action": "no model-family cherry-pick(모델 계열 골라잡기 금지)",
            "effect": "checks whether the pocket is smooth or mined(포켓이 매끄러운지 채굴된 것인지 점검)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_gates(final: Mapping[str, Any]) -> list[dict[str, str]]:
    checks = [
        (
            "input_presence",
            final["missing_inputs"] == 0,
            str(final["missing_inputs"]),
            "0",
            "required DF/DD/DE inputs exist(필수 DF/DD/DE 입력 존재)",
        ),
        (
            "parent_df_gates_passed",
            final["df_failed_gate_rows"] == 0,
            str(final["df_failed_gate_rows"]),
            "0",
            "parent review is usable(부모 검토 사용 가능)",
        ),
        (
            "parent_next_action_matches",
            final["df_next_action"] == RUN_ID,
            str(final["df_next_action"]),
            RUN_ID,
            "continues declared queue(선언 대기열을 이어감)",
        ),
        (
            "validation_thin_named",
            final["validation_thin_rows"] > 0,
            str(final["validation_thin_rows"]),
            ">0",
            "names validation weakness(검증 약점을 이름 붙임)",
        ),
        (
            "oos_quarantine_named",
            final["oos_positive_thin_rows"] > 0,
            str(final["oos_positive_thin_rows"]),
            ">0",
            "quarantines OOS pocket(OOS 포켓 격리)",
        ),
        (
            "repair_contract_materialized",
            final["repair_contract_rows"] >= 4,
            str(final["repair_contract_rows"]),
            ">=4",
            "design contracts exist(설계 계약 존재)",
        ),
        (
            "slice_contract_materialized",
            final["slice_contract_rows"] >= 8,
            str(final["slice_contract_rows"]),
            ">=8",
            "slice stability axes declared(슬라이스 안정성 축 선언)",
        ),
        (
            "firewall_materialized",
            final["firewall_rows"] >= 5,
            str(final["firewall_rows"]),
            ">=5",
            "forbidden paths are blocked(금지 경로 차단)",
        ),
        (
            "dh_queue_materialized",
            final["queue_rows"] >= 4,
            str(final["queue_rows"]),
            ">=4",
            "next materialization queue exists(다음 물질화 대기열 존재)",
        ),
        (
            "no_release_claim",
            final["candidate_selection"] == "not_run"
            and final["mt5_runtime_probe"] == "not_run"
            and final["forward_passed"] == "not_claimed"
            and final["goal_achieve"] == "not_claimed",
            f"selection={final['candidate_selection']};mt5={final['mt5_runtime_probe']};goal={final['goal_achieve']}",
            "not_run/not_claimed",
            "claim boundary is preserved(주장 경계 보존)",
        ),
    ]
    rows = []
    for gate_id, passed, observed, expected, effect in checks:
        rows.append(
            {
                "gate_id": gate_id,
                "status": "passed" if passed else "failed",
                "observed": observed,
                "expected": expected,
                "effect": effect,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def build_receipts(final: Mapping[str, Any], artifact_paths: Sequence[Path]) -> list[Path]:
    experiment_receipt = {
        "hypothesis": "validation/OOS divergence can be repaired by predeclared cost-shape stability inputs(검증/OOS 괴리는 사전 선언 비용 곡선 안정성 입력으로 수리할 수 있음)",
        "decision_use": NEXT_RUN_ID,
        "comparison_baseline": rel(DF_PAIR_SUMMARY),
        "control_variables": "DE models, DD point-cost identity, split, feature order(DE 모델/DD 포인트 비용 정체성/분할/피처 순서)",
        "changed_variables": "design artifacts only(설계 산출물만)",
        "sample_scope": "US100 M5 inherited DD/DE/DF(DD/DE/DF에서 상속한 US100 M5)",
        "success_criteria": "contracts, firewalls, DH queue materialized(계약/방화벽/DH 대기열 물질화)",
        "failure_criteria": "cannot define repair without OOS selection(OOS 선택 없이 수리를 정의하지 못함)",
        "invalid_conditions": "threshold tuning, model training, pair selection(임계값 튜닝/모델 학습/쌍 선택)",
        "stop_conditions": "missing DF/DD/DE inputs or failed gate(DF/DD/DE 입력 누락 또는 게이트 실패)",
        "evidence_plan": [rel(path) for path in artifact_paths],
        "claim_boundary": CLAIM_BOUNDARY,
    }
    data_receipt = {
        "data_source": [rel(path) for path in INPUT_FILES],
        "time_axis": "inherits DD closed M5 UTC bar-close identity(DD 닫힌 M5 UTC 봉마감 정체성 상속)",
        "sample_scope": "design only, no new rows selected(설계 전용, 새 행 선택 없음)",
        "missing_or_duplicate_check": f"missing_inputs={final['missing_inputs']}",
        "feature_label_boundary": "no new feature/label values computed in DG(DG에서 새 피처/라벨 값 계산 없음)",
        "split_boundary": "train/validation/OOS remain inherited and read-only(학습/검증/OOS는 상속되고 읽기 전용)",
        "leakage_risk": "OOS-positive pocket selection(OOS 양호 포켓 선택)",
        "data_hash_or_identity": {
            "df_final": sha256_file(DF_FINAL),
            "df_pair_summary": sha256_file(DF_PAIR_SUMMARY),
            "dd_manifest": sha256_file(DD_MANIFEST),
        },
        "integrity_judgment": "usable_with_boundary",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    model_receipt = {
        "model_family": "DE two-stage candidates reviewed only(DE 2단계 후보 검토 전용)",
        "target_and_label": "stage1 cost gate and stage2 rank/action inherited from DD/DE(DD/DE의 1단계 비용 게이트와 2단계 순위/행동)",
        "split_method": "inherited chronological train/validation/OOS(상속된 시간순 학습/검증/OOS)",
        "selection_metric": "none in DG(DG에서는 없음)",
        "secondary_metrics": "validation PF floor, OOS divergence, slice stability(검증 PF 하한/OOS 괴리/슬라이스 안정성)",
        "threshold_policy": "fixed/read-only; no tuning(고정/읽기 전용, 튜닝 없음)",
        "overfit_risk": "choosing OOS-positive validation-thin pocket(OOS 양호/검증 얇음 포켓 선택)",
        "calibration_risk": "rank scores are ordering only(순위 점수는 순서 전용)",
        "comparison_baseline": rel(DF_MODEL_SUMMARY),
        "validation_judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    performance_receipt = {
        "observed_change": f"best_validation_pf={final['best_validation_pf']};best_oos_pf={final['best_oos_pf']}",
        "comparison_baseline": rel(DF_DIVERGENCE),
        "likely_drivers": "cost policy, model family, feature context, regime pocket(비용 정책/모델 계열/피처 문맥/국면 포켓)",
        "segment_checks": "designed, not executed in DG(DG에서는 설계만 하고 실행하지 않음)",
        "trade_shape": "DF pair trade counts read-only(DF 쌍 거래수 읽기 전용)",
        "alternative_explanations": "regime luck, multiple testing, stage2 weakness(국면 운/다중시험/2단계 약점)",
        "attribution_confidence": "medium_for_blocker_low_for_cause(차단 근거는 중간, 원인 확정은 낮음)",
        "next_probe": NEXT_RUN_ID,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    judgment_receipt = {
        "result_subject": RUN_ID,
        "evidence_available": "DF final, pair divergence, blockers, DD/DE inputs(DF 최종/쌍 괴리/차단 요소/DD/DE 입력)",
        "evidence_missing": "DH materialized slices and any later rerun(DH 물질화 슬라이스와 이후 재실행)",
        "judgment_label": "exploratory_design",
        "claim_boundary": CLAIM_BOUNDARY,
        "next_condition": NEXT_RUN_ID,
        "user_explanation_hook": "좋아 보이는 OOS를 고르지 않고, 왜 검증에서 얇은지 먼저 해부하도록 설계를 고정했습니다.",
    }
    paths = [
        write_json(EXPERIMENT_RECEIPT, experiment_receipt),
        write_json(DATA_RECEIPT, data_receipt),
        write_json(MODEL_RECEIPT, model_receipt),
        write_json(PERFORMANCE_RECEIPT, performance_receipt),
        write_json(JUDGMENT_RECEIPT, judgment_receipt),
    ]
    lineage = {
        "source_inputs": [rel(path) for path in INPUT_FILES],
        "producer": rel(Path(__file__)),
        "consumer": NEXT_RUN_ID,
        "artifact_paths": [rel(path) for path in list(artifact_paths) + paths],
        "artifact_hashes": {
            rel(path): sha256_file(path)
            for path in list(artifact_paths) + paths
            if path_exists(path) and io_path(path).is_file()
        },
        "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
        "availability": "ignored_design_outputs_with_tracked_report(무시된 설계 산출물과 추적 보고서)",
        "lineage_judgment": "connected_with_boundary",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    paths.append(write_json(LINEAGE_RECEIPT, lineage))
    return paths


def write_report(final: Mapping[str, Any]) -> Path:
    text = f"""# Stage337 run337DG Validation Pocket Cost-Shape Repair Design(검증 포켓 비용 곡선 수리 설계)

## Conclusion(결론)

run337DG(337DG 실행)는 run337DF(337DF 실행)의 validation-thin/OOS-positive(검증 얇음/표본외 양호) 패턴을 수리 설계로 바꿨다.

best validation PF(최고 검증 수익 팩터)는 `{final["best_validation_pf"]}`이고 best OOS PF(최고 표본외 수익 팩터)는 `{final["best_oos_pf"]}`이다. 이 차이는 후보 선택(candidate selection, 후보 선택) 근거가 아니라 overfit watch(과적합 감시) 근거다.

Effect(효과): run337DH(337DH 실행)에서 validation PF floor(검증 PF 하한), slice stability(슬라이스 안정성), OOS quarantine(OOS 격리), pair surface smoothness(쌍 표면 매끄러움) 입력을 물질화한다. MT5 probe(MT5 탐침), threshold tuning(임계값 튜닝), lot optimization(로트 최적화), Forward/Goal(전진/목표)은 모두 닫혀 있다.

## Result(결과)

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- validation_thin_rows(검증 얇음 행): `{final["validation_thin_rows"]}`
- oos_positive_thin_rows(OOS 양호/검증 얇음 행): `{final["oos_positive_thin_rows"]}`
- repair_contract_rows(수리 계약 행): `{final["repair_contract_rows"]}`
- slice_contract_rows(슬라이스 계약 행): `{final["slice_contract_rows"]}`
- firewall_rows(방화벽 행): `{final["firewall_rows"]}`
- gates_passed(게이트 통과): `{final["passed_gates"]}/{final["gate_rows"]}`

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return write_md(REPORT_PATH, text)


def write_decision_doc(final: Mapping[str, Any]) -> Path:
    text = f"""# Decision(결정): Stage337 run337DG

- date(날짜): `{TODAY}`
- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- effect(효과): OOS-positive/validation-thin(표본외 양호/검증 얇음) 포켓을 선택하지 않고, 수리 입력 물질화로 넘긴다.
- evidence(근거): `{rel(REPORT_PATH)}`, `{rel(REQUIRED_GATE_AUDIT)}`, `{rel(REPAIR_CONTRACT)}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- Forward/Goal(전진/목표): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return write_md(DECISION_DOC, text)


def update_docs(final: Mapping[str, Any]) -> list[Path]:
    artifacts: list[Path] = []
    workspace_text, workspace_bom = read_text_lossless(WORKSPACE_STATE)
    workspace_text = re.sub(r"^current_run_id: .*$", f"current_run_id: {NEXT_RUN_ID}", workspace_text, count=1, flags=re.MULTILINE)
    focus_entry = (
        "- >-\n"
        f"  Stage337 run337DG focus complete: validation pocket cost-shape repair design(검증 포켓 비용 곡선 수리 설계)을 `{STATUS}`로 닫았다. "
        f"Effect(효과): run337DH(337DH 실행)에서 validation PF floor/slice stability/OOS quarantine(검증 PF 하한/슬라이스 안정성/OOS 격리) 입력을 물질화한다."
    )
    workspace_text = prepend_once(workspace_text, "current_focus:", focus_entry, "Stage337 run337DG focus complete")
    artifacts.append(write_text_preserving(WORKSPACE_STATE, workspace_text, workspace_bom))

    current_text, current_bom = read_text_lossless(CURRENT_STATE)
    for field_name, value in {
        "current_run": f"`{NEXT_RUN_ID}`",
        "status": f"`{STATUS}`",
        "decision": f"`{DECISION}`",
        "latest_completed_run": f"`{RUN_ID}`",
        "next_action": f"`{NEXT_RUN_ID}`",
        "claim_boundary": f"`{CLAIM_BOUNDARY}`",
    }.items():
        current_text = replace_bullet_value(current_text, field_name, value)
    section = f"""
## Stage337 run337DG(337DG 실행) - {TODAY}

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): OOS-positive/validation-thin(표본외 양호/검증 얇음) 포켓을 선택하지 않고 수리 입력 설계로 격리했다. Forward/Goal(전진/목표)은 주장하지 않는다.
"""
    marker = "## Stage337 run337DF(337DF"
    if "## Stage337 run337DG(337DG 실행)" not in current_text:
        current_text = current_text.replace(marker, section + "\n" + marker, 1) if marker in current_text else current_text.rstrip() + "\n\n" + section
    artifacts.append(write_text_preserving(CURRENT_STATE, current_text, current_bom))

    selection = f"""# Stage337 Selection Status(337단계 선택 상태)

- latest_run(최신 실행): `{RUN_ID}`
- latest_decision(최신 결정): `{DECISION}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- frozen_subject(고정 대상): `cp322A_cp321b_exact_replay_control_surface`
- exact_cp322a_forward_handoff(정확 cp322A 전진 인계): `not_feasible_under_frozen_rules`
- preserved_status(보존 상태): `research_artifact_only`
- rebuild_status(재구축 상태): `{STATUS}`
- actual_mt5_execution(실제 MT5 실행): `not_run_dg_design_only`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): 다음은 validation pocket cost-shape repair input materialization(검증 포켓 비용 곡선 수리 입력 물질화)이다.
"""
    artifacts.append(write_text_preserving(SELECTED_STATUS, selection, True))

    stage_text, stage_bom = read_text_lossless(STAGE_BRIEF)
    stage_entry = (
        f"- {TODAY}: run337DG(337DG 실행) designed validation pocket cost-shape repair(검증 포켓 비용 곡선 수리 설계). "
        f"Status(상태) `{STATUS}`. Forward/Goal(전진/목표)은 주장하지 않음."
    )
    artifacts.append(write_text_preserving(STAGE_BRIEF, append_once(stage_text, stage_entry, "run337DG(337DG 실행) designed validation pocket"), stage_bom))

    changelog_text, changelog_bom = read_text_lossless(CHANGELOG)
    changelog_entry = (
        f"- {TODAY}: Stage337 run337DG designed validation pocket cost-shape repair(검증 포켓 비용 곡선 수리 설계) "
        f"and opened `{NEXT_RUN_ID}`."
    )
    artifacts.append(write_text_preserving(CHANGELOG, append_once(changelog_text, changelog_entry, "Stage337 run337DG designed validation pocket"), changelog_bom))
    return artifacts


def update_registers(artifact_paths: Sequence[Path], final: Mapping[str, Any]) -> list[Path]:
    generated = now_utc()
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "validation_pocket_cost_shape_repair_design_without_db",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "notes": f"validation_thin={final['validation_thin_rows']};oos_positive_thin={final['oos_positive_thin_rows']};next={NEXT_RUN_ID};goal_achieve_not_claimed.",
        "family": "experiment_design_data_integrity_model_validation_artifact_lineage",
        "primary_report": rel(REPORT_PATH),
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__repair_design",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "repair_design",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "design_no_training_no_selection",
        "tier_scope": "out_of_scope_by_claim_no_mt5",
        "kpi_scope": "validation_oos_divergence_design",
        "scoreboard_lane": "experiment_design_model_validation",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "primary_kpi": f"validation_thin={final['validation_thin_rows']};oos_positive_thin={final['oos_positive_thin_rows']}",
        "guardrail_kpi": "no_selection;no_threshold_tuning;no_mt5",
        "external_verification_status": "out_of_scope_by_claim",
        "notes": f"decision={DECISION};next={NEXT_RUN_ID}",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__repair_design",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "experiment_design_data_integrity_model_validation_artifact_lineage",
        "evidence_scope": "DF validation/OOS divergence converted to repair design",
        "kpi_scope": "validation_pf_floor_oos_quarantine_slice_design",
        "status": STATUS,
        "judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
        "path": rel(REPORT_PATH),
        "notes": f"next_action={NEXT_RUN_ID};goal_achieve_not_claimed",
        "decision": DECISION,
        "run_key": f"{RUN_ID}__repair_design",
        "family": "experiment_design_data_integrity_model_validation_artifact_lineage",
        "question": "how to repair validation-thin OOS-positive cost-shape pocket without overfitting",
        "metric_scope": "validation_pf_floor_oos_quarantine_slice_contracts",
        "primary_artifact": rel(REPORT_PATH),
        "report_path": rel(REPORT_PATH),
        "next_action": NEXT_RUN_ID,
    }
    artifacts = [
        upsert_csv(RUN_REGISTRY, "run_id", run_row),
        upsert_csv(ALPHA_LEDGER, "ledger_row_id", alpha_row),
        upsert_csv(STAGE_LEDGER, "ledger_row_id", stage_row),
    ]
    artifact_columns: list[str] = []
    artifact_rows: list[dict[str, str]] = []
    if path_exists(ARTIFACT_REGISTRY):
        with io_path(ARTIFACT_REGISTRY).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            artifact_columns = list(reader.fieldnames or [])
            artifact_rows = [dict(row) for row in reader]
    if not artifact_columns:
        artifact_columns = ["artifact_id", "artifact_type", "path", "sha256", "stage_id", "run_id", "created_at_utc", "notes", "artifact_path", "claim_boundary"]
    new_rows = []
    for path in artifact_paths:
        if not path_exists(path) or not io_path(path).is_file():
            continue
        artifact_path = rel(path)
        new_rows.append(
            {
                "artifact_id": f"{RUN_ID}::{artifact_path}",
                "artifact_type": path.suffix.lstrip(".") or "file",
                "path": artifact_path,
                "sha256": sha256_file(path),
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": generated,
                "notes": STATUS,
                "artifact_path": artifact_path,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    keys = {row["artifact_id"] for row in new_rows}
    artifact_rows = [row for row in artifact_rows if row.get("artifact_id") not in keys and row.get("run_id") != RUN_ID]
    artifact_rows.extend(new_rows)
    artifacts.append(write_csv(ARTIFACT_REGISTRY, artifact_columns, artifact_rows))
    return artifacts


def main() -> int:
    io_path(RUN_DIR).mkdir(parents=True, exist_ok=True)
    missing = fail_if_missing(INPUT_FILES)
    summary = summarize_inputs() if not missing else {}
    if missing:
        print(json.dumps({"run_id": RUN_ID, "status": "blocked_missing_inputs", "missing": [rel(path) for path in missing]}, ensure_ascii=False, indent=2))
        return 1

    failure_rows = build_failure_memory(summary)
    repair_rows = build_repair_contract(summary)
    slice_rows = build_slice_contract()
    smoothness_rows = build_pair_smoothness()
    firewall_rows = build_firewall()
    queue_rows = build_queue()
    artifacts: list[Path] = [
        write_csv(FAILURE_MEMORY, FAILURE_COLUMNS, failure_rows),
        write_csv(REPAIR_CONTRACT, REPAIR_COLUMNS, repair_rows),
        write_csv(SLICE_CONTRACT, SLICE_COLUMNS, slice_rows),
        write_csv(PAIR_SMOOTHNESS, SMOOTHNESS_COLUMNS, smoothness_rows),
        write_csv(FIREWALL, FIREWALL_COLUMNS, firewall_rows),
        write_csv(DH_QUEUE, QUEUE_COLUMNS, queue_rows),
    ]
    df_final: Mapping[str, Any] = summary["final"]
    final: dict[str, Any] = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_action": NEXT_RUN_ID,
        "df_next_action": df_final.get("next_action", ""),
        "df_failed_gate_rows": len(summary["df_failed_gates"]),
        "missing_inputs": len(missing),
        "best_validation_pf": summary["best_validation_pf"],
        "best_oos_pf": summary["best_oos_pf"],
        "validation_thin_rows": summary["validation_thin_rows"],
        "oos_positive_thin_rows": summary["oos_positive_thin_rows"],
        "divergence_watch_rows": summary["divergence_watch_rows"],
        "stage1_best_balanced": summary["stage1_best_balanced"],
        "stage2_best_balanced": summary["stage2_best_balanced"],
        "failure_memory_rows": len(failure_rows),
        "repair_contract_rows": len(repair_rows),
        "slice_contract_rows": len(slice_rows),
        "pair_smoothness_rows": len(smoothness_rows),
        "firewall_rows": len(firewall_rows),
        "queue_rows": len(queue_rows),
        "model_training": "not_run_design_only",
        "threshold_tuning": "not_run",
        "lot_optimization": "not_run",
        "candidate_selection": "not_run",
        "mt5_runtime_probe": "not_run",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "runtime_authority": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    gates = build_gates(final)
    final["gate_rows"] = len(gates)
    final["passed_gates"] = sum(1 for row in gates if row["status"] == "passed")
    final["failed_gates"] = [row["gate_id"] for row in gates if row["status"] != "passed"]
    artifacts.extend(
        [
            write_csv(REQUIRED_GATE_AUDIT, GATE_COLUMNS, gates),
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
    artifacts.append(write_report(final))
    artifacts.append(write_decision_doc(final))
    artifacts.extend(update_docs(final))
    artifacts.extend(update_registers(artifacts, final))
    print(json.dumps(json_ready(final), ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if not final["failed_gates"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
