from __future__ import annotations

import csv
import json
import re
import sys
from collections import Counter
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
RUN_NUMBER = "run337DC"
RUN_ID = "run337DC_design_cost_shape_two_stage_handoff_repair_without_db_v1"
PARENT_RUN_ID = "run337DB_review_objective_feature_contract_pivot_training_without_db_v1"
NEXT_RUN_ID = "run337DD_materialize_cost_shape_two_stage_handoff_repair_inputs_without_db_v1"
STATUS = "completed_stage337DC_cost_shape_two_stage_handoff_repair_design_no_training_no_selection"
JUDGMENT = "cost_shape_repair_design_ready_no_runtime_release"
DECISION = "stage337DC_open_run337DD_materialize_cost_shape_two_stage_handoff_repair_inputs"
CLAIM_BOUNDARY = (
    "research_development_only_stage337DC_cost_shape_two_stage_handoff_repair_design_without_db_"
    "no_new_training_no_threshold_tuning_no_lot_optimization_no_candidate_selection_no_mt5_probe_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = STAGE_DIR / "03_reviews"
REPORT_PATH = REVIEWS_DIR / "run337DC_cost_shape_two_stage_handoff_repair_design.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-28_stage337DC_cost_shape_two_stage_handoff_repair_design.md"
SELECTED_STATUS = STAGE_DIR / "04_selected" / "selection_status.md"
STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
STAGE_LEDGER = REVIEWS_DIR / "stage_run_ledger.csv"

DB_DIR = STAGE_DIR / "02_runs" / "run337DB"
DB_FINAL = DB_DIR / "final_decision.json"
DB_GATES = DB_DIR / "required_gate_coverage_audit.csv"
DB_TARGET_FAMILY = DB_DIR / "target_family_summary.csv"
DB_TOP_POCKETS = DB_DIR / "top_validation_diagnostic_pockets.csv"
DB_BLOCKERS = DB_DIR / "release_blocker_summary.csv"
DB_CONTROL_COST_RANK = DB_DIR / "control_cost_rank_summary.csv"
DB_RANK_REVIEW = DB_DIR / "rank_signal_handoff_review.csv"
DB_REPAIR_QUEUE = DB_DIR / "run337DC_repair_design_queue.csv"
DA_COST = STAGE_DIR / "02_runs" / "run337DA" / "cost_curve_scorecard.csv"
DA_SCORE = STAGE_DIR / "02_runs" / "run337DA" / "objective_training_scorecard.csv"

COST_ATTRIBUTION = RUN_DIR / "cost_shape_failure_attribution_matrix.csv"
TWO_STAGE_CONTRACT = RUN_DIR / "two_stage_handoff_repair_contract.csv"
POINT_COST_CONTRACT = RUN_DIR / "point_cost_identity_repair_contract.csv"
NO_RELEASE_FIREWALL = RUN_DIR / "no_release_firewall_contract.csv"
DD_QUEUE = RUN_DIR / "run337DD_materialization_queue.csv"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment_design_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
PERFORMANCE_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
REQUIRED_GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (
    DB_FINAL,
    DB_GATES,
    DB_TARGET_FAMILY,
    DB_TOP_POCKETS,
    DB_BLOCKERS,
    DB_CONTROL_COST_RANK,
    DB_RANK_REVIEW,
    DB_REPAIR_QUEUE,
    DA_COST,
    DA_SCORE,
)
OUTPUT_FILES = (
    COST_ATTRIBUTION,
    TWO_STAGE_CONTRACT,
    POINT_COST_CONTRACT,
    NO_RELEASE_FIREWALL,
    DD_QUEUE,
    EXPERIMENT_RECEIPT,
    MODEL_RECEIPT,
    DATA_RECEIPT,
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

COST_ATTRIBUTION_COLUMNS = (
    "attribution_id",
    "evidence_source",
    "observed_failure",
    "likely_cause",
    "repair_design",
    "success_condition",
    "failure_condition",
    "invalid_condition",
    "forbidden_action",
    "effect",
    "claim_boundary",
)
TWO_STAGE_COLUMNS = (
    "contract_id",
    "stage",
    "input_contract",
    "output_contract",
    "threshold_policy",
    "onnx_packaging_rule",
    "adapter_rule",
    "proxy_mt5_compare_requirement",
    "blocked_if",
    "effect",
    "claim_boundary",
)
POINT_COST_COLUMNS = (
    "contract_id",
    "identity_field",
    "source_rule",
    "validation_rule",
    "blocked_if",
    "forbidden_action",
    "effect",
    "claim_boundary",
)
FIREWALL_COLUMNS = (
    "firewall_id",
    "blocked_claim_or_action",
    "reason",
    "allowed_next_action",
    "evidence_required_to_release",
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
GATE_COLUMNS = ("gate_id", "status", "observed", "expected", "effect", "claim_boundary")


def bool_text(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value).strip().lower()


def as_int(value: Any) -> int:
    text = str(value).strip()
    if not text:
        return 0
    return int(float(text))


def fail_if_missing(paths: Sequence[Path]) -> list[Path]:
    return [path for path in paths if not path_exists(path)]


def summarize_inputs() -> dict[str, Any]:
    final = read_json(DB_FINAL)
    gates = read_csv(DB_GATES)
    target_rows = read_csv(DB_TARGET_FAMILY)
    blockers = read_csv(DB_BLOCKERS)
    rank_rows = read_csv(DB_RANK_REVIEW)
    queue_rows = read_csv(DB_REPAIR_QUEUE)
    family_cost_blocks = {
        row.get("target_family", ""): as_int(row.get("cost_block_rows", 0))
        for row in target_rows
    }
    blocker_counts = {
        row.get("release_blockers", ""): as_int(row.get("rows", 0))
        for row in blockers
    }
    db_failed_gates = [row for row in gates if row.get("status") != "passed"]
    return {
        "final": final,
        "gates": gates,
        "target_rows": target_rows,
        "blockers": blockers,
        "rank_rows": rank_rows,
        "queue_rows": queue_rows,
        "family_cost_blocks": family_cost_blocks,
        "blocker_counts": blocker_counts,
        "db_failed_gates": db_failed_gates,
        "total_cost_blocks": as_int(final.get("cost_block_rows", 0)),
        "rank_pass_rows": as_int(final.get("rank_pass_rows", 0)),
        "rank_rows_total": as_int(final.get("rank_rows", 0)),
        "review_eligible_rows": as_int(final.get("review_eligible_rows", 0)),
        "best_validation_balanced": float(final.get("best_validation_balanced") or 0.0),
    }


def build_cost_attribution(summary: Mapping[str, Any]) -> list[dict[str, str]]:
    family_blocks: Mapping[str, int] = summary["family_cost_blocks"]
    blocker_counts: Mapping[str, int] = summary["blocker_counts"]
    return [
        {
            "attribution_id": "cost_direction_curve_break",
            "evidence_source": f"{rel(DB_TARGET_FAMILY)};{rel(DB_BLOCKERS)}",
            "observed_failure": f"cost_direction cost_block_rows={family_blocks.get('cost_direction(비용 방향)', 0)}; release cost_shape_block={blocker_counts.get('cost_shape_block', 0)}",
            "likely_cause": "single direction surface keeps low-edge trades after cost(단일 방향 표면이 비용 후 낮은 기대값 거래를 남김)",
            "repair_design": "split tradeability gate from direction ranking(거래가능성 게이트와 방향 순위를 분리)",
            "success_condition": "DD creates train-only cost tradeability labels with point-cost identity(DD가 학습 전용 비용 거래가능성 라벨과 포인트 비용 정체성을 생성)",
            "failure_condition": "validation cost curve remains negative at declared cost levels(검증 비용 곡선이 선언 비용 구간에서 계속 음수)",
            "invalid_condition": "threshold chosen from validation or OOS(검증 또는 OOS에서 임계값 선택)",
            "forbidden_action": "no threshold lowering, no lot optimization(임계값 낮추기 금지, 로트 최적화 금지)",
            "effect": "turns cost failure into a predeclared label/action repair(비용 실패를 사전 선언 라벨/행동 수리로 전환)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "attribution_id": "control_residual_curve_break",
            "evidence_source": rel(DB_TARGET_FAMILY),
            "observed_failure": f"control_residual cost_block_rows={family_blocks.get('control_residual_direction(대조 잔차 방향)', 0)}",
            "likely_cause": "residual target clears controls but not execution cost(잔차 목표는 대조를 통과하지만 실행 비용을 이기지 못함)",
            "repair_design": "keep controls mandatory and add cost gate before residual direction(대조를 필수로 유지하고 잔차 방향 앞에 비용 게이트 추가)",
            "success_condition": "control blocks stay zero while cost blocks fall(대조 차단은 0 유지, 비용 차단 감소)",
            "failure_condition": "cost gate only removes trades without improving curve shape(비용 게이트가 곡선 개선 없이 거래만 제거)",
            "invalid_condition": "failed controls are dropped after seeing outcome(결과 확인 뒤 실패 대조 제거)",
            "forbidden_action": "no control weakening(대조 약화 금지)",
            "effect": "prevents a cost repair from becoming another control overfit(비용 수리가 또 다른 대조 과적합이 되는 것을 막음)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "attribution_id": "rank_signal_handoff_needed",
            "evidence_source": f"{rel(DB_TARGET_FAMILY)};{rel(DB_RANK_REVIEW)}",
            "observed_failure": f"rank_pass_rows={summary['rank_pass_rows']}/{summary['rank_rows_total']} but review_eligible_rows={summary['review_eligible_rows']}",
            "likely_cause": "rank signal is useful as ordering, not as a standalone trade surface(순위 신호는 독립 거래 표면이 아니라 정렬 정보로 유용)",
            "repair_design": "use payoff rank as stage2 only after stage1 cost gate(1단계 비용 게이트 통과 뒤 2단계 보상 순위로만 사용)",
            "success_condition": "DD materializes explicit stage1/stage2 handoff fields(DD가 명시적 1단계/2단계 인계 필드 생성)",
            "failure_condition": "rank score is treated as calibrated probability(순위 점수를 보정 확률처럼 취급)",
            "invalid_condition": "fake single ONNX hides the handoff(가짜 단일 ONNX가 인계를 숨김)",
            "forbidden_action": "no fake single-surface packaging(가짜 단일 표면 패키징 금지)",
            "effect": "keeps the rank signal while blocking runtime ambiguity(순위 신호는 살리고 런타임 모호성은 막음)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "attribution_id": "point_cost_identity_gap",
            "evidence_source": f"{rel(DB_REPAIR_QUEUE)};{rel(DA_COST)}",
            "observed_failure": "prior cost proxy used derived cost pressure, not a fully audited close/point identity(이전 비용 프록시는 완전 감사된 종가/포인트 정체성이 아님)",
            "likely_cause": "point value, close, spread, and slippage identity are not yet one contract(포인트값, 종가, 스프레드, 슬리피지가 아직 하나의 계약이 아님)",
            "repair_design": "DD must create close/point/spread/slippage sidecar before labels(DD는 라벨 전 종가/포인트/스프레드/슬리피지 보조표를 생성)",
            "success_condition": "row-count and timestamp identity match the label frame(행 수와 타임스탬프 정체성이 라벨 프레임과 일치)",
            "failure_condition": "any cost component is missing or forward-filled without age(비용 구성요소 누락 또는 나이 없는 전진 채움)",
            "invalid_condition": "cost points are tuned after validation result(검증 결과 뒤 비용 포인트 조정)",
            "forbidden_action": "no validation cost retuning(검증 비용 재조정 금지)",
            "effect": "makes cost stress measurable before any new model(새 모델 전 비용 압박을 측정 가능하게 함)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_two_stage_contract() -> list[dict[str, str]]:
    return [
        {
            "contract_id": "stage1_cost_tradeability_gate",
            "stage": "stage1(1단계)",
            "input_contract": "lag-safe features plus point-cost identity sidecar(지연 안전 피처와 포인트 비용 정체성 보조표)",
            "output_contract": "stage1_pass;stage1_score;stage1_threshold_source=train_only(1단계 통과/점수/학습 전용 임계값 원천)",
            "threshold_policy": "train_only_predeclared_quantile_or_margin(학습 전용 사전 선언 분위/여백)",
            "onnx_packaging_rule": "stage1 separate ONNX only after later training review(이후 학습 검토 뒤 1단계 별도 ONNX)",
            "adapter_rule": "adapter may skip trade if stage1_pass=false(1단계 미통과면 어댑터가 거래 생략 가능)",
            "proxy_mt5_compare_requirement": "compare stage1 fields row by row before KPI(성과 지표 전 1단계 필드 행 단위 비교)",
            "blocked_if": "cost identity sidecar missing or threshold not train-only(비용 정체성 보조표 누락 또는 임계값 학습 전용 아님)",
            "effect": "removes low-edge trades before direction logic(방향 로직 전 낮은 기대값 거래 제거)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "contract_id": "stage2_payoff_rank_direction",
            "stage": "stage2(2단계)",
            "input_contract": "only rows where stage1_pass=true(1단계 통과 행만)",
            "output_contract": "stage2_rank_score;stage2_side;stage2_rank_bucket(2단계 순위 점수/방향/순위 버킷)",
            "threshold_policy": "rank bins from train only, not calibrated probability(순위 구간은 학습 전용이며 보정 확률 아님)",
            "onnx_packaging_rule": "stage2 separate ONNX; no fake single ONNX(2단계 별도 ONNX, 가짜 단일 ONNX 금지)",
            "adapter_rule": "adapter combines stage1 pass and stage2 rank deterministically(어댑터가 1단계 통과와 2단계 순위를 결정적으로 결합)",
            "proxy_mt5_compare_requirement": "compare final_action source fields and not only net profit(순손익만이 아니라 최종 행동 원천 필드 비교)",
            "blocked_if": "rank is used without stage1 pass or treated as probability(순위가 1단계 통과 없이 쓰이거나 확률로 취급됨)",
            "effect": "keeps rank signal without pretending it is a full action policy(순위 신호를 유지하되 완전 행동 정책처럼 꾸미지 않음)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "contract_id": "final_action_handoff_manifest",
            "stage": "adapter_handoff(어댑터 인계)",
            "input_contract": "stage1_pass, stage1_score, stage2_side, stage2_rank_score, cost_points(1단계/2단계/비용 필드)",
            "output_contract": "final_action;skip_reason;handoff_version;source_hash(최종 행동/생략 사유/인계 버전/원천 해시)",
            "threshold_policy": "read thresholds from train-only manifest(학습 전용 목록에서 임계값 읽기)",
            "onnx_packaging_rule": "two ONNX plus deterministic adapter, unless later review proves safe merge(2개 ONNX와 결정적 어댑터, 안전 병합 근거 전 병합 금지)",
            "adapter_rule": "runtime contract versioned before MT5 package(MT5 패키지 전 런타임 계약 버전화)",
            "proxy_mt5_compare_requirement": "proxy/MT5 parity must include handoff_version and skip_reason(프록시/MT5 동등성은 인계 버전과 생략 사유 포함)",
            "blocked_if": "handoff schema ambiguous or missing source hash(인계 스키마 모호 또는 원천 해시 누락)",
            "effect": "prevents runtime ambiguity from being mistaken for model edge(런타임 모호성을 모델 우위로 오해하지 않게 함)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_point_cost_contract() -> list[dict[str, str]]:
    return [
        {
            "contract_id": "broker_close_identity",
            "identity_field": "m5_close(5분 종가)",
            "source_rule": "use broker US100 M5 close with UTC timestamp(UTC 타임스탬프의 브로커 US100 M5 종가 사용)",
            "validation_rule": "same row count and timestamp order as feature frame(피처 프레임과 같은 행 수 및 시간 순서)",
            "blocked_if": "close is absent, duplicated, or shifted(종가 누락/중복/이동)",
            "forbidden_action": "no synthetic close for release claim(해제 주장용 합성 종가 금지)",
            "effect": "anchors cost labels to executable price identity(비용 라벨을 실행 가능 가격 정체성에 고정)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "contract_id": "point_value_identity",
            "identity_field": "point_value and point_size(포인트 가치와 포인트 크기)",
            "source_rule": "read from broker symbol contract or pinned contract file(브로커 심볼 계약 또는 고정 계약 파일에서 읽기)",
            "validation_rule": "hash contract and store in sidecar(계약을 해시하고 보조표에 저장)",
            "blocked_if": "point source differs across Python/MT5(파이썬/MT5 포인트 원천 불일치)",
            "forbidden_action": "no hidden point override(숨은 포인트 덮어쓰기 금지)",
            "effect": "keeps cost points comparable between proxy and MT5(프록시와 MT5 비용 포인트 비교 가능성 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "contract_id": "spread_slippage_stress_identity",
            "identity_field": "spread_points;slippage_points(스프레드 포인트/슬리피지 포인트)",
            "source_rule": "predeclare base and stress costs before validation read(검증 읽기 전 기본/압박 비용 사전 선언)",
            "validation_rule": "cost levels are listed in manifest and never selected from OOS(비용 구간을 목록에 기록하고 OOS에서 선택하지 않음)",
            "blocked_if": "stress level chosen because it looks best(좋아 보이는 압박 구간 선택)",
            "forbidden_action": "no cost-level optimization(비용 구간 최적화 금지)",
            "effect": "turns cost stress into a robustness test, not a tuner(비용 압박을 튜너가 아니라 강건성 시험으로 만듦)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_firewalls() -> list[dict[str, str]]:
    return [
        {
            "firewall_id": "no_runtime_release_from_db_or_dc",
            "blocked_claim_or_action": "runtime release, MT5 package, live readiness(런타임 해제, MT5 패키지, 실거래 준비)",
            "reason": "DB review_eligible_rows=0 and DC is design-only(DB 해제 가능 행 0이며 DC는 설계 전용)",
            "allowed_next_action": NEXT_RUN_ID,
            "evidence_required_to_release": "future training review plus proxy/MT5 handoff parity(향후 학습 검토와 프록시/MT5 인계 동등성)",
            "effect": "prevents design work from masquerading as deployment evidence(설계 작업이 배포 근거처럼 보이는 것을 막음)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "firewall_id": "no_threshold_or_lot_repair",
            "blocked_claim_or_action": "threshold lowering, lot optimization(임계값 낮추기, 로트 최적화)",
            "reason": "would turn repair into overfit(수리를 과적합으로 바꿈)",
            "allowed_next_action": "train-only threshold contract only(학습 전용 임계값 계약만 허용)",
            "evidence_required_to_release": "predeclared train split manifest(사전 선언 학습 분할 목록)",
            "effect": "keeps repair causal and auditable(수리를 원인 기반과 감사 가능 상태로 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "firewall_id": "no_fake_single_onnx",
            "blocked_claim_or_action": "single ONNX claim hiding two-stage handoff(2단계 인계를 숨기는 단일 ONNX 주장)",
            "reason": "rank signal is not a complete action surface(순위 신호는 완전 행동 표면이 아님)",
            "allowed_next_action": "two-stage manifest and deterministic adapter(2단계 목록과 결정적 어댑터)",
            "evidence_required_to_release": "row-level handoff parity(행 단위 인계 동등성)",
            "effect": "keeps runtime semantics visible(런타임 의미를 보이게 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_dd_queue() -> list[dict[str, str]]:
    return [
        {
            "queue_id": "run337DD_materialize_point_cost_identity",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "task": "materialize close/point/spread/slippage identity sidecar(종가/포인트/스프레드/슬리피지 정체성 보조표 물질화)",
            "required_inputs": "broker US100 M5 frame; symbol contract; DB cost review(브로커 US100 M5 프레임, 심볼 계약, DB 비용 검토)",
            "required_outputs": "point_cost_identity_sidecar.csv; cost_identity_receipt.json(포인트 비용 정체성 보조표와 영수증)",
            "blocked_if_missing": "close, point value, timestamp, or contract hash(종가/포인트 가치/타임스탬프/계약 해시)",
            "forbidden_action": "no synthetic cost identity for release(해제용 합성 비용 정체성 금지)",
            "effect": "makes cost labels executable and auditable(비용 라벨을 실행 가능하고 감사 가능하게 함)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run337DD_materialize_stage1_cost_gate_labels",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "task": "materialize train-only cost tradeability gate labels(학습 전용 비용 거래가능성 게이트 라벨 물질화)",
            "required_inputs": "point_cost_identity_sidecar; feature frame; split manifest(비용 정체성 보조표, 피처 프레임, 분할 목록)",
            "required_outputs": "stage1_cost_tradeability_label_frame.parquet; threshold_manifest.json(1단계 비용 거래가능성 라벨 프레임과 임계값 목록)",
            "blocked_if_missing": "train-only split or base/stress cost list(학습 전용 분할 또는 기본/압박 비용 목록)",
            "forbidden_action": "no validation/OOS threshold selection(검증/OOS 임계값 선택 금지)",
            "effect": "separates skip logic from direction logic(생략 로직과 방향 로직 분리)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run337DD_materialize_stage2_rank_handoff",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P0",
            "task": "materialize explicit stage2 payoff-rank handoff fields(명시적 2단계 보상 순위 인계 필드 물질화)",
            "required_inputs": "stage1 labels; payoff rank evidence; feature frame(1단계 라벨, 보상 순위 근거, 피처 프레임)",
            "required_outputs": "two_stage_handoff_manifest.json; stage2_rank_label_frame.parquet(2단계 인계 목록과 순위 라벨 프레임)",
            "blocked_if_missing": "stage1 pass field or rank bucket contract(1단계 통과 필드 또는 순위 버킷 계약)",
            "forbidden_action": "no rank-as-probability claim(순위를 확률로 주장 금지)",
            "effect": "keeps rank as ordering evidence(순위를 정렬 근거로 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "queue_id": "run337DD_materialize_control_and_firewall_audit",
            "next_run_id": NEXT_RUN_ID,
            "priority": "P1",
            "task": "materialize control, leakage, no-release gates(대조/누수/해제 금지 게이트 물질화)",
            "required_inputs": "DB gates; DC contracts; split manifest(DB 게이트, DC 계약, 분할 목록)",
            "required_outputs": "control_firewall_audit.csv; required_gate_coverage_audit.csv(대조 방화벽 감사와 필수 게이트 감사)",
            "blocked_if_missing": "negative controls or no-release evidence(부정 대조 또는 해제 금지 근거)",
            "forbidden_action": "no MT5 probe queue from DD materialization alone(DD 물질화만으로 MT5 탐침 대기열 금지)",
            "effect": "keeps DD as input materialization only(DD를 입력 물질화로만 유지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def gate_row(gate_id: str, ok: bool, observed: Any, expected: Any, effect: str) -> dict[str, str]:
    return {
        "gate_id": gate_id,
        "status": "passed" if ok else "failed",
        "observed": str(observed),
        "expected": str(expected),
        "effect": effect,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def build_gates(final: Mapping[str, Any]) -> list[dict[str, str]]:
    return [
        gate_row("dc_gate_parent_db_passed", final["db_failed_gate_rows"] == 0, final["db_failed_gate_rows"], 0, "DB 근거가 실패 상태에서 설계로 전파되지 않게 한다."),
        gate_row("dc_gate_parent_next_action_matches", final["db_next_action"] == RUN_ID, final["db_next_action"], RUN_ID, "작업 전환이 장부와 일치하게 한다."),
        gate_row("dc_gate_cost_blocks_present", final["db_cost_block_rows"] > 0, final["db_cost_block_rows"], ">0", "수리 대상이 실제 비용 곡선 실패임을 확인한다."),
        gate_row("dc_gate_rank_signal_recorded", final["db_rank_pass_rows"] > 0, final["db_rank_pass_rows"], ">0", "순위 신호를 폐기하지 않고 2단계 근거로 보존한다."),
        gate_row("dc_gate_no_release_rows", final["db_review_eligible_rows"] == 0, final["db_review_eligible_rows"], 0, "해제 가능 행이 없음을 유지한다."),
        gate_row("dc_gate_two_stage_contract", final["two_stage_rows"] >= 3, final["two_stage_rows"], ">=3", "1단계/2단계/인계 표면을 분리한다."),
        gate_row("dc_gate_point_cost_identity_contract", final["point_cost_rows"] >= 3, final["point_cost_rows"], ">=3", "비용 포인트 정체성 수리를 명시한다."),
        gate_row("dc_gate_no_release_firewall", final["firewall_rows"] >= 3, final["firewall_rows"], ">=3", "해제/임계값/가짜 ONNX 방화벽을 기록한다."),
        gate_row("dc_gate_next_queue_materialized", final["queue_rows"] >= 4, final["queue_rows"], ">=4", "DD 물질화 입력을 충분히 지정한다."),
        gate_row("dc_gate_no_forbidden_actions", final["model_training"] == "not_run_design_only" and final["threshold_tuning"] == "not_run" and final["mt5_runtime_probe"] == "not_run", "no_training_no_tuning_no_mt5", "no_training_no_tuning_no_mt5", "설계 실행이 학습/튜닝/MT5로 새지 않게 한다."),
    ]


def build_receipts(final: Mapping[str, Any], artifact_paths: Sequence[Path]) -> list[Path]:
    experiment_receipt = {
        "hypothesis": "DA/DB failure is not solved by threshold tuning; it needs cost identity plus two-stage handoff(DA/DB 실패는 임계값 튜닝이 아니라 비용 정체성과 2단계 인계가 필요함)",
        "decision_use": "decide DD materialization contract only(DD 물질화 계약 결정만)",
        "comparison_baseline": PARENT_RUN_ID,
        "control_variables": "no new training, no threshold tuning, no lot optimization, no MT5 probe(새 학습/임계값 튜닝/로트 최적화/MT5 탐침 없음)",
        "changed_variables": "label/action contract design and handoff semantics(라벨/행동 계약 설계와 인계 의미)",
        "sample_scope": "design from existing DB/DA artifacts only(기존 DB/DA 산출물 기반 설계 전용)",
        "success_criteria": "DD can materialize point-cost and two-stage inputs without leakage(DD가 누수 없이 포인트 비용과 2단계 입력을 물질화 가능)",
        "failure_criteria": "no executable cost identity or ambiguous handoff(실행 가능 비용 정체성 없음 또는 인계 모호)",
        "invalid_conditions": "any validation/OOS selection or runtime release claim(검증/OOS 선택 또는 런타임 해제 주장)",
        "stop_conditions": "gate failure or missing DB evidence(게이트 실패 또는 DB 근거 누락)",
        "evidence_plan": [rel(path) for path in artifact_paths],
        "claim_boundary": CLAIM_BOUNDARY,
    }
    model_receipt = {
        "model_family": "design only, no model training(설계 전용, 모델 학습 없음)",
        "target_and_label": "future stage1 cost tradeability and stage2 payoff rank labels(향후 1단계 비용 거래가능성 및 2단계 보상 순위 라벨)",
        "split_method": "train-only thresholds; validation/OOS read-only(학습 전용 임계값, 검증/OOS 읽기 전용)",
        "selection_metric": "not_applicable_no_selection(선택 없음)",
        "secondary_metrics": "cost curve, control blocks, rank monotonicity, proxy-MT5 handoff parity(비용 곡선, 대조 차단, 순위 단조성, 프록시-MT5 인계 동등성)",
        "threshold_policy": "predeclared train-only(사전 선언 학습 전용)",
        "overfit_risk": "cost level tuning or fake handoff merge(비용 구간 튜닝 또는 가짜 인계 병합)",
        "calibration_risk": "rank score is ordering, not probability(순위 점수는 정렬이지 확률이 아님)",
        "comparison_baseline": PARENT_RUN_ID,
        "validation_judgment": "design_ready_for_materialization",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    data_receipt = {
        "data_source": [rel(path) for path in INPUT_FILES],
        "time_axis": "inherited from DB/DA; DD must audit broker M5 UTC close identity(DB/DA 상속, DD는 브로커 M5 UTC 종가 정체성 감사 필요)",
        "sample_scope": "design only; no new bars joined(설계 전용, 새 봉 결합 없음)",
        "missing_or_duplicate_check": "input presence gate and future DD sidecar audit(입력 존재 게이트와 향후 DD 보조표 감사)",
        "feature_label_boundary": "labels are specified but not created in DC(DC에서는 라벨을 명세만 하고 생성하지 않음)",
        "split_boundary": "train-only thresholds predeclared(학습 전용 임계값 사전 선언)",
        "leakage_risk": "using validation/OOS to pick cost or rank bucket(검증/OOS로 비용 또는 순위 버킷 선택)",
        "data_hash_or_identity": {"db_final_sha256": sha256_file(DB_FINAL)},
        "integrity_judgment": "usable_with_boundary",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    performance_receipt = {
        "attribution_subject": RUN_ID,
        "from_failure": f"DB cost_block_rows={final['db_cost_block_rows']}; rank_pass={final['db_rank_pass_rows']}/{final['db_rank_rows']}",
        "performance_intent": "curve shape repair before any KPI claim(성과 주장 전 곡선 형태 수리)",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    judgment_receipt = {
        "result_subject": RUN_ID,
        "evidence_available": "DB final, design contracts, DD queue(DB 최종판정, 설계 계약, DD 대기열)",
        "evidence_missing": "materialized DD inputs, new models, ONNX, proxy/MT5 parity(DD 물질화 입력, 새 모델, ONNX, 프록시/MT5 동등성)",
        "judgment_label": "exploratory_design_ready",
        "claim_boundary": CLAIM_BOUNDARY,
        "next_condition": NEXT_RUN_ID,
        "user_explanation_hook": "지금은 수익 개선 주장이 아니라, 비용 실패를 다시 과적합하지 않도록 설계로 묶는 단계입니다.",
    }
    receipt_paths = [
        write_json(EXPERIMENT_RECEIPT, experiment_receipt),
        write_json(MODEL_RECEIPT, model_receipt),
        write_json(DATA_RECEIPT, data_receipt),
        write_json(PERFORMANCE_RECEIPT, performance_receipt),
        write_json(JUDGMENT_RECEIPT, judgment_receipt),
    ]
    lineage_receipt = {
        "source_inputs": [rel(path) for path in INPUT_FILES],
        "producer": rel(Path(__file__)),
        "consumer": NEXT_RUN_ID,
        "artifact_paths": [rel(path) for path in artifact_paths] + [rel(path) for path in receipt_paths],
        "artifact_hashes": {
            rel(path): sha256_file(path)
            for path in list(artifact_paths) + receipt_paths
            if path_exists(path) and io_path(path).is_file()
        },
        "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
        "availability": "tracked_script_and_docs_with_ignored_run_outputs(추적 스크립트/문서와 무시된 실행 산출물)",
        "lineage_judgment": "connected_with_boundary",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    receipt_paths.append(write_json(LINEAGE_RECEIPT, lineage_receipt))
    return receipt_paths


def write_report(final: Mapping[str, Any]) -> Path:
    text = f"""# Stage337 run337DC Cost Shape Two-Stage Handoff Repair Design(비용 곡선 2단계 인계 수리 설계)

## Conclusion(결론)

run337DC(337DC 실행)는 run337DB(337DB 실행)의 review(검토)를 새 학습 없이 design contract(설계 계약)로 바꿨다. ONNX parity(ONNX 동등성)는 이미 DB에서 분리됐고, 남은 핵심은 cost shape block(비용 곡선 차단) `{final["db_cost_block_rows"]}`행이다.

Effect(효과): 다음 run337DD(337DD 실행)는 point-cost identity(포인트 비용 정체성), stage1 cost gate(1단계 비용 게이트), stage2 payoff rank handoff(2단계 보상 순위 인계)를 물질화한다. 이번 실행은 training(학습), selection(선택), MT5 probe(MT5 탐침), Forward/Goal(전진/목표)을 주장하지 않는다.

## Result(결과)

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- cost_attribution_rows(비용 귀속 행): `{final["cost_attribution_rows"]}`
- two_stage_rows(2단계 계약 행): `{final["two_stage_rows"]}`
- point_cost_rows(포인트 비용 계약 행): `{final["point_cost_rows"]}`
- firewall_rows(방화벽 행): `{final["firewall_rows"]}`
- queue_rows(대기열 행): `{final["queue_rows"]}`
- gates_passed(게이트 통과): `{final["passed_gates"]}/{final["gate_rows"]}`

## Boundary(경계)

- model_training(모델 학습): `not_run_design_only`
- threshold_tuning(임계값 튜닝): `not_run`
- lot_optimization(로트 최적화): `not_run`
- candidate_selection(후보 선택): `not_run`
- MT5 runtime probe(MT5 런타임 탐침): `not_run`
- Forward Passed/Failed(전진 통과/실패): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return write_md(REPORT_PATH, text)


def write_decision_doc(final: Mapping[str, Any]) -> Path:
    text = f"""# Decision(결정): Stage337 run337DC

- date(날짜): `{TODAY}`
- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- effect(효과): cost shape failure(비용 곡선 실패)를 point-cost identity(포인트 비용 정체성)와 explicit two-stage handoff(명시적 2단계 인계) 물질화로 넘긴다.
- evidence(근거): `{rel(REPORT_PATH)}`, `{rel(REQUIRED_GATE_AUDIT)}`, `{rel(COST_ATTRIBUTION)}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- Forward/Goal(전진/목표): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    return write_md(DECISION_DOC, text)


def prepend_once_after_heading(text: str, heading: str, entry: str, unique: str) -> str:
    if unique in text:
        return text
    return text.replace(heading, f"{heading}\n{entry}", 1)


def append_once(text: str, entry: str, unique: str) -> str:
    if unique in text:
        return text
    return text.rstrip() + "\n" + entry + "\n"


def update_docs() -> list[Path]:
    artifacts: list[Path] = []
    workspace_text, workspace_bom = read_text_lossless(WORKSPACE_STATE)
    workspace_text = re.sub(r"^current_run_id: .*$", f"current_run_id: {NEXT_RUN_ID}", workspace_text, count=1, flags=re.MULTILINE)
    focus_entry = (
        "- >-\n"
        f"  Stage337 run337DC focus complete: cost shape two-stage handoff repair design(비용 곡선 2단계 인계 수리 설계)을 `{STATUS}`로 닫았다. "
        f"Effect(효과): run337DD(337DD 실행)에서 point-cost identity/stage1 cost gate/stage2 rank handoff(포인트 비용 정체성/1단계 비용 게이트/2단계 순위 인계) 입력을 물질화한다."
    )
    workspace_text = prepend_once_after_heading(workspace_text, "current_focus:", focus_entry, "Stage337 run337DC focus complete")
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
## Stage337 run337DC(337DC 실행) - {TODAY}

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): cost shape/two-stage/point-cost identity(비용 곡선/2단계/포인트 비용 정체성) 수리 설계를 만들었다. Forward/Goal(전진/목표)은 주장하지 않는다.
"""
    marker = "## Stage337 run337DB(337DB"
    if "## Stage337 run337DC(337DC 실행)" not in current_text:
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
- actual_mt5_execution(실제 MT5 실행): `not_run_dc_design_only`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): 다음은 cost shape two-stage handoff repair inputs(비용 곡선 2단계 인계 수리 입력) 물질화이다.
"""
    artifacts.append(write_text_preserving(SELECTED_STATUS, selection, True))

    stage_text, stage_bom = read_text_lossless(STAGE_BRIEF)
    stage_entry = (
        f"- {TODAY}: run337DC(337DC 실행) designed cost shape two-stage handoff repair(비용 곡선 2단계 인계 수리 설계). "
        f"Status(상태) `{STATUS}`. Forward/Goal(전진/목표)은 주장하지 않음."
    )
    artifacts.append(write_text_preserving(STAGE_BRIEF, append_once(stage_text, stage_entry, "run337DC(337DC 실행) designed cost shape"), stage_bom))

    changelog_text, changelog_bom = read_text_lossless(CHANGELOG)
    changelog_entry = (
        f"- {TODAY}: Stage337 run337DC designed cost shape two-stage handoff repair(비용 곡선 2단계 인계 수리 설계) "
        f"and opened `{NEXT_RUN_ID}`."
    )
    artifacts.append(write_text_preserving(CHANGELOG, append_once(changelog_text, changelog_entry, "Stage337 run337DC designed cost shape"), changelog_bom))
    return artifacts


def update_registers(artifact_paths: Sequence[Path], final: Mapping[str, Any]) -> list[Path]:
    generated = now_utc()
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "cost_shape_two_stage_handoff_repair_design_without_db",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "notes": f"cost_blocks={final['db_cost_block_rows']};two_stage_rows={final['two_stage_rows']};next={NEXT_RUN_ID};goal_achieve_not_claimed.",
        "family": "experiment_design_data_integrity_model_validation_artifact_lineage",
        "primary_report": rel(REPORT_PATH),
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__cost_shape_two_stage_design",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "cost_shape_two_stage_design",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "design_no_training",
        "tier_scope": "out_of_scope_by_claim_no_mt5",
        "kpi_scope": "design_contract_no_kpi",
        "scoreboard_lane": "experiment_design",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(REPORT_PATH),
        "primary_kpi": f"cost_blocks={final['db_cost_block_rows']};queue_rows={final['queue_rows']}",
        "guardrail_kpi": "no_threshold_tuning;no_lot_optimization;no_fake_single_onnx;no_mt5_probe",
        "external_verification_status": "out_of_scope_by_claim",
        "notes": f"decision={DECISION};next={NEXT_RUN_ID}",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__cost_shape_two_stage_design",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "experiment_design_data_integrity_model_validation_artifact_lineage",
        "evidence_scope": "DB cost shape failure converted into DD materialization design",
        "kpi_scope": "design_contract_no_training",
        "status": STATUS,
        "judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
        "path": rel(REPORT_PATH),
        "notes": f"next_action={NEXT_RUN_ID};goal_achieve_not_claimed",
        "decision": DECISION,
        "run_key": f"{RUN_ID}__cost_shape_two_stage_design",
        "family": "experiment_design_data_integrity_model_validation_artifact_lineage",
        "question": "how should cost-shape failure be repaired without overfit tuning",
        "metric_scope": "design_contract_firewall_queue",
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
    if missing:
        print(json.dumps({"run_id": RUN_ID, "status": "blocked_missing_inputs", "missing": [rel(path) for path in missing]}, ensure_ascii=False, indent=2))
        return 1

    summary = summarize_inputs()
    cost_rows = build_cost_attribution(summary)
    two_stage_rows = build_two_stage_contract()
    point_cost_rows = build_point_cost_contract()
    firewall_rows = build_firewalls()
    queue_rows = build_dd_queue()
    artifacts: list[Path] = [
        write_csv(COST_ATTRIBUTION, COST_ATTRIBUTION_COLUMNS, cost_rows),
        write_csv(TWO_STAGE_CONTRACT, TWO_STAGE_COLUMNS, two_stage_rows),
        write_csv(POINT_COST_CONTRACT, POINT_COST_COLUMNS, point_cost_rows),
        write_csv(NO_RELEASE_FIREWALL, FIREWALL_COLUMNS, firewall_rows),
        write_csv(DD_QUEUE, QUEUE_COLUMNS, queue_rows),
    ]
    final: dict[str, Any] = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_action": NEXT_RUN_ID,
        "db_next_action": summary["final"].get("next_action", ""),
        "db_failed_gate_rows": len(summary["db_failed_gates"]),
        "db_cost_block_rows": summary["total_cost_blocks"],
        "db_rank_pass_rows": summary["rank_pass_rows"],
        "db_rank_rows": summary["rank_rows_total"],
        "db_review_eligible_rows": summary["review_eligible_rows"],
        "db_best_validation_balanced": summary["best_validation_balanced"],
        "cost_attribution_rows": len(cost_rows),
        "two_stage_rows": len(two_stage_rows),
        "point_cost_rows": len(point_cost_rows),
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
    artifacts.extend(update_docs())
    artifacts.extend(update_registers(artifacts, final))
    print(json.dumps(json_ready(final), ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if not final["failed_gates"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
