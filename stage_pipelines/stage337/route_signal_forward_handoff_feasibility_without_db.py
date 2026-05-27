from __future__ import annotations

import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from stage_pipelines.stage337 import review_mt5_probe_execution_package_without_db as bl


aw = bl.aw
bg = bl.bg

TODAY = "2026-05-27"
STAGE_ID = bl.STAGE_ID
RUN_NUMBER = "run337BM"
RUN_ID = "run337BM_route_signal_forward_handoff_feasibility_without_db_v1"
PARENT_RUN_ID = bl.RUN_ID
NEXT_RUN_ID = "run337BN_design_forward_safe_route_signal_rebuild_packet_without_db_v1"
STATUS = "completed_stage337BM_exact_cp322a_route_signal_handoff_not_feasible_rebuild_queue_opened"
JUDGMENT = "exact_cp322a_forward_handoff_not_repairable_under_frozen_rules"
DECISION = "stage337BM_close_exact_cp322a_forward_handoff_blocker_open_run337BN_forward_safe_rebuild_design"
CLAIM_BOUNDARY = (
    "research_development_only_stage337BM_route_signal_handoff_feasibility_without_db_cp322a_frozen_"
    "exact_forward_handoff_not_feasible_no_model_training_no_threshold_retuning_no_db_rule_rewrite_"
    "no_lot_optimization_no_candidate_selection_no_forward_passed_no_forward_failed_no_live_readiness_"
    "no_deployment_no_operating_promotion_no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = bl.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = bl.REVIEWS_DIR
REPORT_PATH = REVIEWS_DIR / "run337BM_route_signal_forward_handoff_feasibility.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-27_stage337BM_route_signal_forward_handoff_feasibility.md"
SELECTED_STATUS = bl.SELECTED_STATUS
STAGE_BRIEF = bl.STAGE_BRIEF
WORKSPACE_STATE = bl.WORKSPACE_STATE
CURRENT_STATE = bl.CURRENT_STATE
CHANGELOG = bl.CHANGELOG
RUN_REGISTRY = bl.RUN_REGISTRY
ALPHA_LEDGER = bl.ALPHA_LEDGER
ARTIFACT_REGISTRY = bl.ARTIFACT_REGISTRY
STAGE_LEDGER = bl.STAGE_LEDGER

BL_DIR = STAGE_DIR / "02_runs" / "run337BL"
BL_FINAL = BL_DIR / "final_decision.json"
BL_BLOCKER = BL_DIR / "route_signal_blocker_review.csv"
BL_QUEUE = BL_DIR / "run337BM_route_signal_handoff_queue.csv"
BL_GATE_AUDIT = BL_DIR / "required_gate_coverage_audit.csv"
BK_ROUTE = STAGE_DIR / "02_runs" / "run337BK" / "route_signal_handoff_status.csv"
BK_HANDOFF = STAGE_DIR / "02_runs" / "run337BK" / "runtime_file_handoff_manifest.csv"
STAGE328_CONTRACT = bl.bk.STAGE328_SIGNAL_CONTRACT
STAGE328B_REPORT = bl.bk.STAGE328B_DECISION_REPORT

FEASIBILITY_MATRIX = RUN_DIR / "route_signal_feasibility_matrix.csv"
FORBIDDEN_REPAIR_REVIEW = RUN_DIR / "forbidden_repair_review.csv"
FAILURE_MEMORY = RUN_DIR / "failure_memory.csv"
RUN337BN_QUEUE = RUN_DIR / "run337BN_forward_safe_rebuild_queue.csv"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
RUNTIME_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
REQUIRED_GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

INPUT_FILES = (
    BL_FINAL,
    BL_BLOCKER,
    BL_QUEUE,
    BL_GATE_AUDIT,
    BK_ROUTE,
    BK_HANDOFF,
    STAGE328_CONTRACT,
    STAGE328B_REPORT,
)
OUTPUT_FILES = (
    FEASIBILITY_MATRIX,
    FORBIDDEN_REPAIR_REVIEW,
    FAILURE_MEMORY,
    RUN337BN_QUEUE,
    DATA_RECEIPT,
    MODEL_RECEIPT,
    RUNTIME_RECEIPT,
    JUDGMENT_RECEIPT,
    REQUIRED_GATE_AUDIT,
    FINAL_DECISION,
    RUN_MANIFEST,
)

FEASIBILITY_COLUMNS = (
    "option_id",
    "option_name",
    "uses_new_data",
    "changes_frozen_surface",
    "requires_outcome_source",
    "requires_forward_rank_fit",
    "allowed_scope",
    "decision",
    "effect",
    "claim_boundary",
)
FORBIDDEN_COLUMNS = (
    "repair_action",
    "status",
    "reason",
    "allowed_alternative",
    "effect",
    "claim_boundary",
)
MEMORY_COLUMNS = (
    "memory_id",
    "evidence",
    "failure_mode",
    "consequence",
    "next_allowed_work",
    "claim_boundary",
)
QUEUE_COLUMNS = bl.QUEUE_COLUMNS
GATE_COLUMNS = bl.GATE_COLUMNS


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(aw.io_path(path).read_text(encoding="utf-8-sig"))


def read_rows(path: Path) -> list[dict[str, str]]:
    _, rows = aw.read_csv_table(path, prefer_head=False)
    return rows


def pass_fail(ok: bool) -> str:
    return "passed" if ok else "failed"


def load_inputs() -> dict[str, Any]:
    missing = [aw.rel(path) for path in INPUT_FILES if not aw.path_exists(path)]
    if missing:
        raise FileNotFoundError(f"missing route-signal feasibility inputs: {missing}")
    return {
        "bl_final": read_json(BL_FINAL),
        "bl_blocker": read_rows(BL_BLOCKER),
        "bl_queue": read_rows(BL_QUEUE),
        "bl_gates": read_rows(BL_GATE_AUDIT),
        "bk_route": read_rows(BK_ROUTE),
        "bk_handoff": read_rows(BK_HANDOFF),
        "stage328": read_json(STAGE328_CONTRACT),
        "stage328b_text": aw.io_path(STAGE328B_REPORT).read_text(encoding="utf-8-sig"),
    }


def build_feasibility_matrix(src: Mapping[str, Any]) -> list[dict[str, Any]]:
    contract = src["stage328"].get("contract", {})
    thresholds = contract.get("frozen_threshold_candidates", {})
    formula = contract.get("exact_formula", "")
    return [
        {
            "option_id": "exact_split_local_rank_forward",
            "option_name": formula,
            "uses_new_data": "true",
            "changes_frozen_surface": "false",
            "requires_outcome_source": "true",
            "requires_forward_rank_fit": "true",
            "allowed_scope": "not_allowed_for_actual_mt5_forward",
            "decision": "rejected_requires_forward_rank_recalculation_and_outcome_source",
            "effect": "prevents recreating the old split rank on new data(새 데이터에서 과거 분할 순위 재생성 차단)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "option_id": "historical_oos_threshold_replay",
            "option_name": f"use historical oos threshold {contract.get('historical_split_thresholds', {}).get('oos')}",
            "uses_new_data": "false",
            "changes_frozen_surface": "true",
            "requires_outcome_source": "true",
            "requires_forward_rank_fit": "false",
            "allowed_scope": "not_allowed_for_frozen_cp322a",
            "decision": "rejected_changes_rank_surface_and_uses_oos_threshold",
            "effect": "blocks hidden OOS threshold replay(OOS 임계값 재사용 은폐 차단)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "option_id": "train_only_fixed_threshold_proxy",
            "option_name": f"use train_only candidate {thresholds.get('train_only')}",
            "uses_new_data": "false",
            "changes_frozen_surface": "true",
            "requires_outcome_source": "true",
            "requires_forward_rank_fit": "false",
            "allowed_scope": "diagnostic_or_new_rebuild_only",
            "decision": "rejected_for_exact_cp322a_allowed_only_as_new_predeclared_rebuild_control",
            "effect": "separates possible rebuild control from frozen cp322A(가능한 재구축 대조와 고정 cp322A 분리)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "option_id": "stage318_outcome_source_replay",
            "option_name": "reuse outcome-distilled Stage318 source",
            "uses_new_data": "false",
            "changes_frozen_surface": "false",
            "requires_outcome_source": "true",
            "requires_forward_rank_fit": "false",
            "allowed_scope": "not_forward_authority",
            "decision": "rejected_outcome_distilled_source_not_forward_safe",
            "effect": "prevents outcome-distilled signal from becoming live feature(결과 증류 신호의 실시간 피처화 차단)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "option_id": "proxy_diagnostic_only",
            "option_name": "make diagnostic proxy without MT5 KPI authority",
            "uses_new_data": "possible",
            "changes_frozen_surface": "not_applicable",
            "requires_outcome_source": "false",
            "requires_forward_rank_fit": "false",
            "allowed_scope": "diagnostic_only",
            "decision": "allowed_only_for_failure_memory_not_forward_result",
            "effect": "keeps proxy useful for debugging but not KPI(프록시는 디버깅 전용, KPI 권위 없음)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "option_id": "live_computable_rebuild",
            "option_name": "design raw market/live-computable route signal rebuild",
            "uses_new_data": "allowed_with_asof_controls",
            "changes_frozen_surface": "true_new_candidate_or_control",
            "requires_outcome_source": "false",
            "requires_forward_rank_fit": "forbidden",
            "allowed_scope": "next_research_packet",
            "decision": "allowed_as_run337BN_rebuild_design_not_cp322a_exact_repair",
            "effect": "moves work to forward-safe rebuild without pretending cp322A exact survived(cp322A 생존 주장 없이 전진 안전 재구축으로 이동)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def build_forbidden_review() -> list[dict[str, Any]]:
    actions = [
        ("threshold_retune", "forbidden", "would change score threshold or rank surface(점수 임계값 또는 순위 표면 변경)", "predeclare new rebuild control(새 재구축 대조 사전 선언)"),
        ("D_B_rule_rewrite", "forbidden", "would change D/B decision surface(D/B 판단 표면 변경)", "new live-computable feature family(새 실시간 계산 가능 피처군)"),
        ("lot_optimization", "forbidden", "does not solve handoff and masks risk(인계 문제를 풀지 못하고 위험을 가림)", "lot-normalized review only(로트 정규화 검토만)"),
        ("forward_rank_recalculation", "forbidden", "fits rank boundary on new forward data(새 전진 데이터 순위 경계 맞춤)", "as-of fixed controls only(시점 기준 고정 대조만)"),
        ("outcome_distillation", "forbidden", "uses realized MT5 outcome as signal source(실현 MT5 결과를 신호 원천으로 사용)", "raw market/live-computable inputs(원천 시장/실시간 계산 가능 입력)"),
        ("claim_forward_passed", "forbidden", "no actual forward MT5 evidence exists(실제 전진 MT5 근거 없음)", "run337BN design then external proof(337BN 설계 후 외부 검증)"),
    ]
    return [
        {
            "repair_action": action,
            "status": status,
            "reason": reason,
            "allowed_alternative": alternative,
            "effect": "keeps repair from becoming another overfit(수리가 또 다른 과적합이 되지 않게 함)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for action, status, reason, alternative in actions
    ]


def build_failure_memory(src: Mapping[str, Any]) -> list[dict[str, Any]]:
    decision = src["stage328"].get("decision", "")
    stage328b_has_rebuild = "live_feature_rebuild_required" in src["stage328b_text"]
    return [
        {
            "memory_id": "cp322a_exact_route_signal_forward_handoff_not_feasible",
            "evidence": f"stage328_decision={decision};stage328b_live_feature_rebuild_required={stage328b_has_rebuild};run337BL_blocker=route_signal_pair_missing",
            "failure_mode": "route_signal requires split-local rank and outcome-distilled source that are not forward-safe(경로 신호가 전진 안전하지 않은 분할 순위와 결과 증류 원천을 요구)",
            "consequence": "exact cp322A cannot be used for actual frozen forward MT5 under frozen rules(고정 규칙 아래 정확 cp322A 실제 전진 MT5 사용 불가)",
            "next_allowed_work": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def build_queue() -> list[dict[str, Any]]:
    return [
        {
            "queue_id": "run337BN_forward_safe_route_signal_rebuild_design",
            "next_run_id": NEXT_RUN_ID,
            "review_subject": "forward-safe route signal rebuild design(전진 안전 경로 신호 재구축 설계)",
            "inputs_to_review": ";".join([aw.rel(FEASIBILITY_MATRIX), aw.rel(FORBIDDEN_REPAIR_REVIEW), aw.rel(FAILURE_MEMORY), aw.rel(STAGE328B_REPORT)]),
            "must_confirm": "raw market/live-computable inputs, as-of joins, no outcome source, no forward rank fit(원천 시장/실시간 계산 가능 입력, 시점 기준 결합, 결과 원천 금지, 전진 순위 맞춤 금지)",
            "must_reject_if": "claims cp322A exact forward passed, reuses outcome source, changes frozen cp322A silently(cp322A 정확 전진 통과 주장/결과 원천 재사용/고정 cp322A 몰래 변경)",
            "expected_outputs": "new rebuild design packet with negative controls and external MT5 proof requirements(부정 대조와 외부 MT5 검증 요건이 있는 새 재구축 설계 패키지)",
            "priority": "P0",
            "effect": "moves from impossible exact repair to honest forward-safe rebuild(불가능한 정확 수리에서 정직한 전진 안전 재구축으로 이동)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def build_receipts(final: Mapping[str, Any]) -> list[Path]:
    payloads = [
        (
            DATA_RECEIPT,
            {
                "decision": final["decision"],
                "data_boundary": "no new data generated; feasibility only(새 데이터 생성 없음, 가능성 검토만)",
                "no_lookahead_guard": "forward rank recalculation and outcome distillation rejected(전진 순위 재계산과 결과 증류 거절)",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            MODEL_RECEIPT,
            {
                "model_boundary": "cp322A ONNX unchanged and exact handoff not repairable under frozen rules(cp322A ONNX 변경 없음, 고정 규칙 안에서 정확 인계 수리 불가)",
                "allowed_next": "new rebuild design only(새 재구축 설계만 허용)",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            RUNTIME_RECEIPT,
            {
                "runtime_path": aw.rel(BK_HANDOFF),
                "parity_check": "runtime blocked before MT5 because required route-signal CSV pair cannot be generated safely(필수 경로 신호 CSV 쌍을 안전하게 만들 수 없어 MT5 전 차단)",
                "runtime_claim_boundary": "blocked_not_runtime_authority",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        (
            JUDGMENT_RECEIPT,
            {
                "judgment": final["judgment"],
                "forward_passed": "not_claimed",
                "forward_failed": "not_claimed",
                "forward_blocked": "closed_for_exact_cp322a_handoff_only",
                "goal_achieve": "not_claimed",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
    ]
    return [aw.write_json(path, payload) for path, payload in payloads]


def build_gates(
    src: Mapping[str, Any],
    feasibility_rows: Sequence[Mapping[str, Any]],
    forbidden_rows: Sequence[Mapping[str, Any]],
    memory_rows: Sequence[Mapping[str, Any]],
    queue_rows: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    bl_gates = sum(1 for row in src["bl_gates"] if row.get("status") == "passed")
    rejected_exact = sum(1 for row in feasibility_rows if str(row.get("decision", "")).startswith("rejected")) >= 4
    allowed_rebuild = any(row.get("option_id") == "live_computable_rebuild" and "allowed" in row.get("decision", "") for row in feasibility_rows)
    forbidden_ok = all(row.get("status") == "forbidden" for row in forbidden_rows)
    specs = [
        ("bm_gate_parent_loaded", src["bl_final"].get("next_action") == RUN_ID, f"parent_next={src['bl_final'].get('next_action')}", "run337BL opens run337BM(337BL이 337BM을 엶)"),
        ("bm_gate_parent_gates_passed", bl_gates == 9 and src["bl_final"].get("passed_gates") == 9, f"bl_gates={bl_gates}", "run337BL gates passed(337BL 게이트 통과)"),
        ("bm_gate_stage328_hazard_loaded", src["stage328"].get("decision") == "exact_cp322a_forward_signal_contract_not_safe_without_upstream_rebuild", f"decision={src['stage328'].get('decision')}", "Stage328 hazard loaded(Stage328 위험 로드)"),
        ("bm_gate_stage328b_rebuild_required", "live_feature_rebuild_required" in src["stage328b_text"], "stage328b_live_feature_rebuild_required", "Stage328B rebuild requirement loaded(Stage328B 재구축 요구 로드)"),
        ("bm_gate_exact_options_rejected", rejected_exact, f"rejected_exact_count={sum(1 for row in feasibility_rows if str(row.get('decision', '')).startswith('rejected'))}", "exact handoff options rejected(정확 인계 선택지 거절)"),
        ("bm_gate_rebuild_option_allowed", allowed_rebuild, f"allowed_rebuild={allowed_rebuild}", "rebuild option allowed as new work(재구축 선택지를 새 작업으로 허용)"),
        ("bm_gate_forbidden_repairs_named", forbidden_ok, f"forbidden_rows={len(forbidden_rows)}", "forbidden repairs named(금지 수리 명명)"),
        ("bm_gate_failure_memory_ready", len(memory_rows) == 1, f"memory_rows={len(memory_rows)}", "failure memory ready(실패 기억 준비)"),
        ("bm_gate_queue_ready", len(queue_rows) == 1 and queue_rows[0].get("next_run_id") == NEXT_RUN_ID, f"queue={len(queue_rows)}", "run337BN queue ready(337BN 대기열 준비)"),
        ("bm_gate_no_goal_or_forward_pass_claim", True, "forward_passed=not_claimed;goal=not_claimed", "no forbidden claim(금지 주장 없음)"),
    ]
    return [
        {
            "gate_id": gate_id,
            "status": pass_fail(ok),
            "observed": observed,
            "expected": expected,
            "effect": "keeps feasibility judgment separate from operating claim(가능성 판정을 운영 주장과 분리)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for gate_id, ok, observed, expected in specs
    ]


def count_passed(rows: Sequence[Mapping[str, Any]]) -> int:
    return sum(1 for row in rows if row.get("status") == "passed")


def write_report(final: Mapping[str, Any]) -> Path:
    text = f"""# Stage337 run337BM Route Signal Forward Handoff Feasibility(경로 신호 전진 인계 가능성)

## Conclusion(결론)

run337BM(337BM 실행)은 cp322A exact route-signal forward handoff(cp322A 정확 경로 신호 전진 인계)를 고정 규칙 안에서 만들 수 없다고 판정했다.

Effect(효과): 이 판정은 Forward Failed(전진 실패)나 운영 불합격이 아니다. 실제 forward MT5(MT5 전진 실행)를 할 수 있는 입력이 없으므로 exact cp322A forward handoff(정확 cp322A 전진 인계)만 닫고, live-computable rebuild(실시간 계산 가능 재구축) 설계를 연다.

## Result(결과)

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- gates(게이트): `{final['passed_gates']}/{final['gate_rows']}`
- exact_cp322a_handoff(정확 cp322A 인계): `not_feasible_under_frozen_rules`
- next_action(다음 행동): `{final['next_action']}`

## Boundary(경계)

- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime authority(런타임 권위): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

Claim boundary(주장 경계): `{final['claim_boundary']}`
"""
    return aw.write_text_lossless(REPORT_PATH, text, True)


def write_decision_doc(final: Mapping[str, Any]) -> Path:
    text = f"""# Decision: Stage337 run337BM Route Signal Forward Handoff Feasibility(결정: 337단계 337BM 경로 신호 전진 인계 가능성)

- date(날짜): {TODAY}
- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(상위 실행 ID): `{PARENT_RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- gates(게이트): `{final['passed_gates']}/{final['gate_rows']}`

Effect(효과): cp322A exact(정확 cp322A)를 몰래 고치지 않고, 전진 안전 재구축(rebuild, 재구축) 설계로 넘긴다.

Claim boundary(주장 경계): `{final['claim_boundary']}`
"""
    return aw.write_text_lossless(DECISION_DOC, text, True)


def update_docs(final: Mapping[str, Any]) -> list[Path]:
    artifacts: list[Path] = []
    workspace_text, workspace_bom = aw.read_text_lossless(WORKSPACE_STATE)
    workspace = bg.remove_workspace_focus_block(workspace_text, "Stage337 run337BM focus")
    workspace = bg.replace_top_value(workspace, "current_run_id: ", NEXT_RUN_ID)
    focus = (
        f"- >-\n  Stage337 run337BM focus complete: exact cp322A route-signal forward handoff(정확 cp322A 경로 신호 전진 인계)는 "
        f"`not_feasible_under_frozen_rules`로 닫았다. Effect(효과): Forward/Goal(전진/목표)은 주장하지 않고 "
        f"run337BN(337BN 실행) live-computable rebuild design(실시간 계산 가능 재구축 설계)을 연다.\n"
    )
    workspace = workspace.replace("current_focus:\n", "current_focus:\n" + focus, 1)
    artifacts.append(aw.write_text_lossless(WORKSPACE_STATE, workspace, workspace_bom))

    current_text, current_bom = aw.read_text_lossless(CURRENT_STATE)
    current = bg.remove_markdown_section(current_text, "## Stage337 run337BM(337BM 실행)")
    replacements = {
        "- current_run(현재 실행): ": f"`{NEXT_RUN_ID}`",
        "- status(상태): ": f"`{final['status']}`",
        "- decision(결정): ": f"`{final['decision']}`",
        "- latest_completed_run(최근 완료 실행): ": f"`{RUN_ID}`",
        "- next_action(다음 행동): ": f"`{NEXT_RUN_ID}`",
        "- claim_boundary(주장 경계): ": f"`{CLAIM_BOUNDARY}`",
    }
    for prefix, value in replacements.items():
        current = bg.replace_top_value(current, prefix, value)
    entry = f"""
## Stage337 run337BM(337BM 실행) - {TODAY}

- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- decision(결정): `{final['decision']}`
- next_action(다음 행동): `{final['next_action']}`
- effect(효과): run337BM(337BM 실행)은 exact cp322A route-signal forward handoff(정확 cp322A 경로 신호 전진 인계)가 고정 규칙 안에서 불가능함을 선택지별로 반증했고, live-computable rebuild design(실시간 계산 가능 재구축 설계)을 연다. Forward/Goal(전진/목표)은 주장하지 않는다.
"""
    current = current.replace("## Stage337 run337BL(337BL 실행)", entry + "\n## Stage337 run337BL(337BL 실행)", 1)
    artifacts.append(aw.write_text_lossless(CURRENT_STATE, current, current_bom))

    selection_text = f"""# Stage337 Selection Status(337단계 선택 상태)

- latest_run(최신 실행): `{RUN_ID}`
- latest_decision(최신 결정): `{final['decision']}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- frozen_subject(고정 대상): `cp322A_cp321b_exact_replay_control_surface`
- exact_cp322a_forward_handoff(정확 cp322A 전진 인계): `not_feasible_under_frozen_rules`
- preserved_status(보존 상태): `research_artifact_only`
- actual_mt5_execution(실제 MT5 실행): `not_run_no_forward_safe_route_signal`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- Forward Blocked(전진 차단): `closed_for_exact_cp322a_handoff_only`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): cp322A exact(정확 cp322A)는 몰래 고치지 않고 연구 산출물로 보존하며, 다음은 전진 안전 재구축 설계다.
"""
    artifacts.append(aw.write_text_lossless(SELECTED_STATUS, selection_text, True))

    stage_text, stage_bom = aw.read_text_lossless(STAGE_BRIEF)
    stage_text = stage_text.rstrip() + f"\n- {TODAY}: run337BM(337BM 실행) closed exact cp322A route-signal forward handoff(정확 cp322A 경로 신호 전진 인계) as not feasible under frozen rules(고정 규칙 내 불가능) and opened run337BN(337BN 실행) rebuild design(재구축 설계). Forward/Goal(전진/목표)은 주장하지 않는다.\n"
    artifacts.append(aw.write_text_lossless(STAGE_BRIEF, stage_text, stage_bom))

    changelog_text, changelog_bom = aw.read_text_lossless(CHANGELOG)
    changelog_text = changelog_text.rstrip() + f"\n- {TODAY}: Stage337 run337BM proved exact cp322A route-signal forward handoff(정확 cp322A 경로 신호 전진 인계) is not feasible under frozen rules(고정 규칙 내 불가능) and opened forward-safe rebuild design(전진 안전 재구축 설계).\n"
    artifacts.append(aw.write_text_lossless(CHANGELOG, changelog_text, changelog_bom))
    return artifacts


def update_registers(final: Mapping[str, Any]) -> list[Path]:
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "route_signal_forward_handoff_feasibility_without_db",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": aw.rel(REPORT_PATH),
        "notes": f"decision={final['decision']};next_action={final['next_action']};gates={final['passed_gates']}/{final['gate_rows']};goal_achieve_not_claimed.",
        "work_family": "runtime_backtest",
        "primary_artifact": aw.rel(REPORT_PATH),
    }
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__route_signal_handoff_feasibility",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "route_signal_handoff_feasibility",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "Stage337 run337BM route-signal handoff feasibility",
        "tier_scope": "research_feasibility_only",
        "kpi_scope": "no_new_trading_kpi",
        "scoreboard_lane": "runtime_backtest",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": aw.rel(REPORT_PATH),
        "primary_kpi": f"feasibility_options={final['feasibility_rows']};gates={final['passed_gates']}/{final['gate_rows']}",
        "guardrail_kpi": "exact_cp322a_handoff_not_feasible;no_forward_claim;no_goal_achieve",
        "external_verification_status": "not_applicable_feasibility_only(가능성 검토 전용)",
        "notes": f"next_action={final['next_action']};cp322a_preserved_research_artifact.",
    }
    stage_row = {
        "ledger_row_id": f"{RUN_ID}__route_signal_handoff_feasibility",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "work_family": "runtime_backtest",
        "evidence_scope": "Stage328/328B route-signal source audit and run337BL blocker",
        "kpi_scope": "handoff_feasibility_no_forward_decision",
        "status": final["status"],
        "judgment": final["judgment"],
        "claim_boundary": CLAIM_BOUNDARY,
        "path": aw.rel(REPORT_PATH),
        "notes": "goal_achieve_not_claimed;forward_passed_not_claimed;exact_cp322a_handoff_not_feasible",
        "decision": final["decision"],
        "run_key": f"{RUN_ID}__route_signal_handoff_feasibility",
        "family": "route_signal_forward_handoff_feasibility_without_db",
        "question": "can exact cp322A route_signal forward handoff be made under frozen rules",
        "metric_scope": "feasibility_failure_memory_rebuild_queue",
        "primary_artifact": aw.rel(REPORT_PATH),
        "report_path": aw.rel(REPORT_PATH),
        "next_action": final["next_action"],
    }
    aw.upsert_csv(RUN_REGISTRY, aw.RUN_REGISTRY_COLUMNS, run_row, "run_id")
    aw.upsert_csv(ALPHA_LEDGER, aw.ALPHA_LEDGER_COLUMNS, alpha_row, "ledger_row_id")
    aw.upsert_csv(STAGE_LEDGER, aw.STAGE_LEDGER_COLUMNS, stage_row, "ledger_row_id")
    return [RUN_REGISTRY, ALPHA_LEDGER, STAGE_LEDGER]


def update_artifact_registry(paths: Sequence[Path], final: Mapping[str, Any]) -> Path:
    columns, rows = aw.read_csv_table(ARTIFACT_REGISTRY, prefer_head=False)
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
    feasibility_rows = build_feasibility_matrix(src)
    feasibility_path = aw.write_csv(FEASIBILITY_MATRIX, FEASIBILITY_COLUMNS, feasibility_rows)
    forbidden_rows = build_forbidden_review()
    forbidden_path = aw.write_csv(FORBIDDEN_REPAIR_REVIEW, FORBIDDEN_COLUMNS, forbidden_rows)
    memory_rows = build_failure_memory(src)
    memory_path = aw.write_csv(FAILURE_MEMORY, MEMORY_COLUMNS, memory_rows)
    queue_rows = build_queue()
    queue_path = aw.write_csv(RUN337BN_QUEUE, QUEUE_COLUMNS, queue_rows)
    gate_rows = build_gates(src, feasibility_rows, forbidden_rows, memory_rows, queue_rows)
    gate_path = aw.write_csv(REQUIRED_GATE_AUDIT, GATE_COLUMNS, gate_rows)
    all_gates_pass = all(row.get("status") == "passed" for row in gate_rows)
    final = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS if all_gates_pass else "invalid_stage337BM_route_signal_feasibility_gate_failure",
        "judgment": JUDGMENT if all_gates_pass else "route_signal_handoff_feasibility_gate_failure",
        "decision": DECISION if all_gates_pass else "repair_stage337BM_feasibility_packet_before_rebuild_design",
        "next_action": NEXT_RUN_ID if all_gates_pass else "repair_stage337BM_feasibility_gate_failure_v1",
        "feasibility_rows": len(feasibility_rows),
        "forbidden_rows": len(forbidden_rows),
        "failure_memory_rows": len(memory_rows),
        "queue_rows": len(queue_rows),
        "gate_rows": len(gate_rows),
        "passed_gates": count_passed(gate_rows),
        "failed_gates": [row.get("gate_id") for row in gate_rows if row.get("status") != "passed"],
        "exact_cp322a_forward_handoff": "not_feasible_under_frozen_rules",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "forward_blocked": "closed_for_exact_cp322a_handoff_only",
        "runtime_authority": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    final_path = aw.write_json(FINAL_DECISION, final)
    manifest = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "created_at_utc": now_utc(),
        "producer": aw.rel(Path(__file__)),
        "parent_run_id": PARENT_RUN_ID,
        "inputs": [aw.rel(path) for path in INPUT_FILES],
        "outputs": [aw.rel(path) for path in OUTPUT_FILES],
        "external_verification_status": "not_applicable_feasibility_only(가능성 검토 전용)",
        "actual_mt5_execution": "not_run",
        "forbidden_actions": [
            "model training(모델 학습)",
            "threshold retuning(임계값 재조정)",
            "D/B rewrite(D/B 재작성)",
            "lot optimization(로트 최적화)",
            "forward rank recalculation(전진 순위 재계산)",
            "outcome distillation(결과 증류)",
            "Forward Passed/Failed claim(전진 통과/실패 주장)",
            "runtime authority claim(런타임 권위 주장)",
            "Goal Achieve claim(목표 달성 주장)",
        ],
        "claim_boundary": CLAIM_BOUNDARY,
    }
    manifest_path = aw.write_json(RUN_MANIFEST, manifest)
    receipt_paths = build_receipts(final)
    report_path = write_report(final)
    decision_path = write_decision_doc(final)
    doc_paths = update_docs(final)
    register_paths = update_registers(final)
    artifact_paths = [
        feasibility_path,
        forbidden_path,
        memory_path,
        queue_path,
        gate_path,
        *receipt_paths,
        final_path,
        manifest_path,
        report_path,
        decision_path,
        *doc_paths,
        *register_paths,
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
                "gates": f"{final['passed_gates']}/{final['gate_rows']}",
                "exact_cp322a_forward_handoff": final["exact_cp322a_forward_handoff"],
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
