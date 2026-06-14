from __future__ import annotations

import csv
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists
from foundation.models.onnx_bridge import ordered_hash, sha256_file
from stage_pipelines.stage_frontier_03 import frontier03b_regime_asymmetric_label_proxy_scout as f03b


STAGE_ID = "stage_frontier_23__payoff_asymmetry_pf_source_onnx_scout"
RUN_ID = "frontier23A_stage_open_payoff_asymmetry_pf_source_hypothesis_design_v1"
RUN_NUMBER = "frontier23A"
PARENT_RUN_ID = "frontier22D_stage_closeout_shock_pf_source_v1"
NEXT_RUN_ID = "frontier23B_payoff_asymmetry_pf_source_proxy_scout_v1"
STATUS = "opened_frontier23_payoff_asymmetry_pf_source_no_authority"
JUDGMENT = "stage_opened_after_grok_adjusted_payoff_asymmetry_contract"

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REPORT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_report.md"
SCRIPT_PATH = Path("stage_pipelines/stage_frontier_23/materialize_frontier23a_stage_open.py")
GROK_PACKET = Path("docs/agent_control/grok_reviews/2026-06-14_frontier23_stage_open/small_review")

DATASET_PATH = Path(
    "data/processed/model_inputs/"
    "label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/"
    "model_input_dataset.parquet"
)
FEATURE_ORDER_PATH = DATASET_PATH.with_name("model_input_feature_order.txt")
EXPECTED_FEATURE_HASH = "fa06973c24462298ea38d84528b07ca0adf357e506f3bfeea02eb0d5691ab8e2"

WORKSPACE_STATE = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE = Path("docs/context/current_working_state.md")
RUN_REGISTRY = Path("docs/registers/run_registry.csv")
ALPHA_LEDGER = Path("docs/registers/alpha_run_ledger.csv")
IDEA_REGISTRY = Path("docs/registers/idea_registry.md")
CHANGELOG = Path("docs/workspace/changelog.md")
DECISION_PATH = Path("docs/decisions/2026-06-14_stage_frontier_23_payoff_asymmetry_pf_source_onnx_scout_open.md")

F22_SELECTION = Path("stages/stage_frontier_22__session_return_shock_pf_source_onnx_scout/04_selected/selection_status.md")
F22_PRESERVED = Path("stages/stage_frontier_22__session_return_shock_pf_source_onnx_scout/04_selected/preserved_clue.md")
F22_NEGATIVE = Path("stages/stage_frontier_22__session_return_shock_pf_source_onnx_scout/04_selected/negative_memory.md")
F22_CLOSEOUT = Path(
    "stages/stage_frontier_22__session_return_shock_pf_source_onnx_scout/"
    "03_reviews/frontier22D_stage_closeout_shock_pf_source_v1_report.md"
)

PAYOFF_METRICS = {
    "avg_win_loss_ratio": "mean(winning proxy pnl) / abs(mean(losing proxy pnl))",
    "right_tail_loss_tail_ratio": "positive p90 proxy pnl / abs(negative p10 proxy pnl)",
    "adverse_loss_containment": "conditional negative-tail loss vs unconditional same-side train baseline",
    "profit_factor": "gross positive proxy pnl / abs(gross negative proxy pnl)",
}

LOCKS = {
    "selection_axis": "outcome_conditioned_train_payoff_distribution_first",
    "label_horizon": "fwd12 fixed future_log_return_12",
    "selection_split": "train_only",
    "forward_splits": "validation_oos_read_only",
    "pre_scout_sanity_gate": "single_condition_payoff_asymmetry_must_beat_unconditional_train_baseline",
    "no_lifecycle_until_seed": "no lifecycle repair until proxy seed surface exists",
    "no_onnx_until_handoff": "no model training or ONNX branch until handoff candidate exists",
    "f22_reference_boundary": "F22 low-DD lifecycle is risk containment reference only",
}


def main() -> int:
    ensure_dirs()
    normalize_grok_markdown()
    created_at = utc_now()
    feature_order = read_feature_order()
    grok = read_grok_packet()
    local = local_verification(feature_order, grok)
    if local["judgment"] != "pass_open_ready_with_adjusted_payoff_locks":
        raise RuntimeError(f"Frontier23A local verification failed: {json.dumps(local, ensure_ascii=False)}")
    summary = build_summary(created_at, feature_order, grok, local)
    write_outputs(summary)
    update_registries(summary)
    update_current_truth(summary)
    print(json.dumps(json_ready({
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "next_run_id": NEXT_RUN_ID,
        "grok_classification": grok["classification"],
        "local_verification": local["judgment"],
        "report": REPORT_PATH.as_posix(),
    }), ensure_ascii=False, indent=2))
    return 0


def ensure_dirs() -> None:
    for path in (
        RUN_ROOT,
        STAGE_ROOT / "00_spec",
        STAGE_ROOT / "01_inputs",
        STAGE_ROOT / "02_runs" / "active",
        STAGE_ROOT / "02_runs" / "archived",
        STAGE_ROOT / "03_reviews",
        STAGE_ROOT / "04_selected",
        DECISION_PATH.parent,
    ):
        io_path(path).mkdir(parents=True, exist_ok=True)
    ensure_stage_ledger_header()


def ensure_stage_ledger_header() -> None:
    path = STAGE_ROOT / "03_reviews" / "stage_run_ledger.csv"
    if path_exists(path):
        return
    with io_path(ALPHA_LEDGER).open("r", encoding="utf-8-sig", newline="") as handle:
        header = next(csv.reader(handle))
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        csv.writer(handle, lineterminator="\n").writerow(header)


def normalize_grok_markdown() -> None:
    for name in ("prompt.md", "clean_output.md"):
        path = GROK_PACKET / name
        if path_exists(path):
            text = io_path(path).read_text(encoding="utf-8-sig")
            f03b.write_text_sig(path, text.rstrip() + "\n")


def read_feature_order() -> list[str]:
    features = [line.strip() for line in io_path(FEATURE_ORDER_PATH).read_text(encoding="utf-8-sig").splitlines() if line.strip()]
    if len(features) != 58:
        raise ValueError(f"feature count mismatch: {len(features)}")
    return features


def read_grok_packet() -> dict[str, Any]:
    metadata = read_json(GROK_PACKET / "metadata.json")
    output = read_text(GROK_PACKET / "clean_output.md")
    return {
        "packet": GROK_PACKET.as_posix(),
        "prompt": (GROK_PACKET / "prompt.md").as_posix(),
        "output": (GROK_PACKET / "clean_output.md").as_posix(),
        "metadata": (GROK_PACKET / "metadata.json").as_posix(),
        "prompt_hash": metadata.get("prompt_hash", ""),
        "success": bool(metadata.get("success")),
        "returncode": metadata.get("returncode"),
        "timed_out": bool(metadata.get("timed_out")),
        "unexpected_top_level_artifacts": metadata.get("unexpected_top_level_artifacts", []),
        "classification": classify_grok(output),
        "output_excerpt": output[:2400],
    }


def classify_grok(text: str) -> str:
    lowered = text.lower()
    if "decision: accept with adjustments" in lowered:
        return "accepted_with_adjustments(조정 수용)"
    if "decision: accept" in lowered:
        return "accepted(수용)"
    if "decision: reject" in lowered:
        return "rejected(거절)"
    return "classification_missing(분류 누락)"


def local_verification(feature_order: list[str], grok: dict[str, Any]) -> dict[str, Any]:
    workspace = read_text(WORKSPACE_STATE)
    f22_selection = read_text(F22_SELECTION)
    f22_preserved = read_text(F22_PRESERVED)
    f22_negative = read_text(F22_NEGATIVE)
    f22_closeout = read_text(F22_CLOSEOUT)
    grok_text = read_text(GROK_PACKET / "clean_output.md")
    feature_hash = ordered_hash(feature_order)
    forbidden_claims = ("Goal Achieve", "runtime authority", "live readiness", "operating promotion", "selected baseline")
    checks = {
        "workspace_current_stage_frontier22_closed": f"current_stage_id: stage_frontier_22__session_return_shock_pf_source_onnx_scout" in workspace
        and "closed_preserved_clue_negative_memory_shock_lifecycle_low_dd_density_weak_pf_no_handoff" in workspace,
        "workspace_next_run_frontier23a": f"next_run_id: {RUN_ID}" in workspace,
        "f22_selection_no_authority": "no selected baseline" in f22_selection.lower(),
        "f22_preserved_clue_present": "low_dd_density_reference" in f22_preserved or "낮은 손실폭" in f22_preserved,
        "f22_negative_memory_present": "did_not_create_seed_or_handoff" in f22_negative or "씨앗/인계" in f22_negative,
        "f22_closeout_runtime_ineligible": "runtime_probe_ineligible" in f22_closeout,
        "feature_hash_matches_contract": feature_hash == EXPECTED_FEATURE_HASH,
        "dataset_exists": path_exists(DATASET_PATH),
        "grok_transport_success": grok["success"] and grok["returncode"] == 0 and not grok["timed_out"],
        "grok_accepts_with_adjustments": grok["classification"] == "accepted_with_adjustments(조정 수용)",
        "grok_metric_lock_present": "Metric definition lock" in grok_text or "지표 정의 잠금" in grok_text,
        "grok_pre_scout_gate_present": "Pre-scout sanity gate" in grok_text or "탐색 전 건전성 게이트" in grok_text,
        "grok_no_unexpected_top_level_artifacts": not grok["unexpected_top_level_artifacts"],
        "forbidden_claims_not_created_by_codex": all(f"{claim}: claimed" not in grok_text for claim in forbidden_claims),
    }
    return {
        "judgment": "pass_open_ready_with_adjusted_payoff_locks" if all(checks.values()) else "needs_manual_review",
        "checks": checks,
        "feature_order_hash": feature_hash,
        "feature_count": len(feature_order),
    }


def build_summary(created_at: str, feature_order: list[str], grok: dict[str, Any], local: dict[str, Any]) -> dict[str, Any]:
    return {
        "created_at_utc": created_at,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "primary_family": "experiment_execution(실험 실행)",
        "primary_skill": "obsidian-run-evidence-system(실행 근거 시스템)",
        "support_skills": [
            "obsidian-experiment-design(실험 설계)",
            "obsidian-data-integrity(데이터 무결성)",
            "obsidian-model-validation(모델 검증)",
            "obsidian-artifact-lineage(산출물 계보)",
            "obsidian-grok-collaboration(그록 협업)",
        ],
        "frontier_thesis": (
            "PF source(수익 팩터 원천)는 shock+trend(충격+추세) 상속이 아니라 "
            "train-only payoff distribution asymmetry(학습 전용 보상 분포 비대칭)에서 먼저 찾아야 한다."
        ),
        "hypothesis": (
            "평균 이익/손실 비, 우측 꼬리 대 최악 손실 억제, 불리 손실 필터가 좋은 진입 상태는 "
            "validation/OOS(검증/표본외)에서도 PF(수익 팩터) 원천에 가까운 단서를 줄 수 있다."
        ),
        "decision_use": "F23B proxy scout(F23B 프록시 탐색)의 선택 지표와 중단 조건을 고정한다.",
        "comparison_baseline": "unconditional same-side train baseline(무조건 동일 방향 학습 기준선)과 F22 negative memory(F22 부정 기억).",
        "control_variables": [
            "feature_set_v2 58 features(58개 피처 고정)",
            "future_log_return_12 fwd12 proxy(fwd12 프록시 고정)",
            "train-only selection(학습 전용 선택)",
            "validation/OOS read-only(검증/표본외 읽기 전용)",
        ],
        "changed_variables": [
            "selection metric becomes payoff asymmetry(선택 지표를 보상 비대칭으로 변경)",
            "no shock-required entry lock(충격 필수 진입 잠금 제거)",
            "pre-scout sanity gate(탐색 전 건전성 게이트) 추가",
        ],
        "sample_scope": "Tier A separate(티어 A 분리); Tier B missing_required(티어 B 필수 누락); Tier A+B out_of_scope_by_claim(티어 A+B 주장 범위 밖).",
        "success_criteria": {
            "pre_scout_sanity": "at least one train-only asymmetry condition beats unconditional train baseline(학습 전용 비대칭 조건 하나 이상이 무조건 학습 기준선을 초과)",
            "scout_clue": "validation/OOS net positive, PF>=1.05, density 3-12/day, DD<=35(검증/표본외 순수익 양수, 수익 팩터 1.05 이상, 빈도 3-12/일, 손실폭 35 이하)",
            "seed_surface": "validation/OOS PF>=1.20 both, density 5-10/day, DD controlled(검증/표본외 둘 다 수익 팩터 1.20 이상, 빈도 5-10/일, 손실폭 억제)",
            "handoff_candidate": "PF>=1.50 both, density 5-10/day, DD<=12, smoothness pass, then Grok before WFO/MT5/ONNX(둘 다 수익 팩터 1.50 이상이면 비싼 검증 전 그록 검토)",
        },
        "failure_criteria": [
            "pre-scout sanity gate fails(탐색 전 건전성 게이트 실패)",
            "no validation/OOS positive PF clue(검증/표본외 양수 수익 팩터 단서 없음)",
            "best rows are shock+trend or F20 atlas restatement(최상위 행이 충격+추세 또는 F20 규칙 지도 재진술)",
        ],
        "invalid_conditions": [
            "validation/OOS used for selection stats(검증/표본외를 선택 통계에 사용)",
            "lifecycle repair before proxy seed(프록시 씨앗 전 생명주기 수리)",
            "ONNX/model training before handoff candidate(인계 후보 전 ONNX/모델 학습)",
        ],
        "stop_conditions": [
            "pre-scout sanity gate fails(탐색 전 건전성 게이트 실패)",
            "handoff-like row appears and pre-expensive Grok is required(인계성 행 발생 시 비싼 검증 전 그록 필요)",
            "capped proxy and repair cannot create seed/handoff(상한 프록시/수리가 씨앗/인계를 못 만듦)",
        ],
        "payoff_metrics": PAYOFF_METRICS,
        "locks": LOCKS,
        "feature_count": len(feature_order),
        "feature_order_hash": ordered_hash(feature_order),
        "grok": grok,
        "local_verification": local,
        "claim_boundary": {claim: "not_claimed(주장 없음)" for claim in f03b.FORBIDDEN_CLAIMS},
    }


def write_outputs(summary: dict[str, Any]) -> None:
    write_json(RUN_ROOT / "stage_open_summary.json", summary)
    write_json(RUN_ROOT / "run_manifest.json", run_manifest(summary))
    write_json(RUN_ROOT / "payoff_asymmetry_lock.json", {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "payoff_metrics": PAYOFF_METRICS,
        "locks": LOCKS,
        "search_caps": {"single_condition_keep": 140, "pair_candidate_cap": 360, "pair_depth": 2},
        "claim_boundary": summary["claim_boundary"],
    })
    write_json(RUN_ROOT / "grok_receipt.json", grok_receipt(summary))
    f03b.write_text_sig(STAGE_ROOT / "README.md", readme_text(summary))
    f03b.write_text_sig(STAGE_ROOT / "00_spec" / "stage_brief.md", stage_brief(summary))
    f03b.write_text_sig(STAGE_ROOT / "00_spec" / "payoff_asymmetry_lock_spec.md", lock_spec(summary))
    f03b.write_text_sig(STAGE_ROOT / "00_spec" / "do_not_repeat.md", do_not_repeat_text())
    f03b.write_text_sig(STAGE_ROOT / "01_inputs" / "experiment_design.md", experiment_design_text(summary))
    f03b.write_text_sig(STAGE_ROOT / "01_inputs" / "prior_stage_scan.md", prior_stage_scan_text())
    f03b.write_text_sig(STAGE_ROOT / "01_inputs" / "input_refs.md", input_refs_text(summary))
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / "review_index.md", review_index())
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / "grok_stage_open_receipt.md", grok_receipt_text(summary))
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / "local_verification.md", local_verification_text(summary))
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / "required_gate_coverage_audit.md", gate_audit(summary))
    f03b.write_text_sig(REPORT_PATH, report_text(summary))
    f03b.write_text_sig(STAGE_ROOT / "04_selected" / "selection_status.md", selection_status(summary))
    f03b.write_text_sig(DECISION_PATH, decision_text(summary))


def run_manifest(summary: dict[str, Any]) -> dict[str, Any]:
    artifacts = [SCRIPT_PATH, DATASET_PATH, FEATURE_ORDER_PATH, GROK_PACKET / "prompt.md", GROK_PACKET / "clean_output.md"]
    return {
        "identity": {
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "parent_run_id": PARENT_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "created_at_utc": summary["created_at_utc"],
        },
        "artifacts": [artifact_identity(path) for path in artifacts],
        "feature_schema": {
            "feature_count": summary["feature_count"],
            "feature_order_hash": summary["feature_order_hash"],
            "feature_order_path": FEATURE_ORDER_PATH.as_posix(),
        },
        "data_snapshot": {"dataset_path": DATASET_PATH.as_posix(), "split_names": ["train", "validation", "oos"]},
        "rule_stack": {"entry_selection": LOCKS, "payoff_metrics": PAYOFF_METRICS},
        "compatibility": {"schema_version": "frontier23a_stage_open_v1", "mismatch_policy": "fail_fast(빠른 실패)"},
        "claim_boundary": summary["claim_boundary"],
    }


def grok_receipt(summary: dict[str, Any]) -> dict[str, Any]:
    return {
        "trigger_reason": "stage_open_required_by_goal(목표가 단계 개방 그록 검토를 요구)",
        "review_size": "small(소규모)",
        "direction_before_grok": "open F23 payoff asymmetry PF source scout(F23 보상 비대칭 수익 팩터 원천 탐색 개방)",
        "bounded_evidence": [F22_SELECTION.as_posix(), F22_PRESERVED.as_posix(), F22_NEGATIVE.as_posix(), F22_CLOSEOUT.as_posix()],
        "prompt_identity": {"path": summary["grok"]["prompt"], "hash": summary["grok"]["prompt_hash"]},
        "grok_output_identity": {"path": summary["grok"]["output"], "classification": summary["grok"]["classification"]},
        "advice_classification": "accepted_with_adjustments(조정 수용)",
        "local_verification": summary["local_verification"],
        "forbidden_claim_check": summary["claim_boundary"],
        "final_codex_direction": "apply payoff metric lock, pre-scout sanity gate, novelty guard, no lifecycle before seed(보상 지표 잠금, 탐색 전 건전성 게이트, 신규성 가드, 씨앗 전 생명주기 금지 적용)",
    }


def update_registries(summary: dict[str, Any]) -> None:
    f03b.upsert_csv(RUN_REGISTRY, "run_id", run_registry_row(summary))
    f03b.upsert_csv(ALPHA_LEDGER, "ledger_row_id", ledger_row(summary))
    f03b.upsert_csv(STAGE_ROOT / "03_reviews" / "stage_run_ledger.csv", "ledger_row_id", ledger_row(summary))
    f03b.append_once(CHANGELOG, RUN_ID, changelog_entry(summary))
    f03b.append_once(IDEA_REGISTRY, RUN_ID, idea_registry_entry(summary))


def run_registry_row(summary: dict[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "stage_open(단계 개방)",
        "family": "experiment_execution(실험 실행)",
        "work_family": "experiment_execution(실험 실행)",
        "status": summary["status"],
        "judgment": summary["judgment"],
        "path": REPORT_PATH.as_posix(),
        "notes": "frontier23_stage_open_grok_adjusted_payoff_asymmetry_contract_no_authority",
        "run_number": RUN_NUMBER,
        "date": "2026-06-14",
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "claim_boundary": "stage_open_no_model_training_no_wfo_no_mt5_no_authority_goal_claim",
        "report_path": REPORT_PATH.as_posix(),
        "created_at_utc": summary["created_at_utc"],
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "result_path": REPORT_PATH.as_posix(),
    }


def ledger_row(summary: dict[str, Any]) -> dict[str, Any]:
    return {
        "ledger_row_id": f"{RUN_ID}__stage_open",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": f"{RUN_ID}__stage_open",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "stage_open(단계 개방)",
        "tier_scope": "not_applicable_stage_open(단계 개방에는 해당 없음)",
        "kpi_scope": "planning_only_no_trading_kpi(계획 전용, 거래 KPI 없음)",
        "scoreboard_lane": "stage_open(단계 개방)",
        "status": summary["status"],
        "judgment": summary["judgment"],
        "path": REPORT_PATH.as_posix(),
        "primary_kpi": f"grok={summary['grok']['classification']};feature_hash={summary['feature_order_hash']}",
        "guardrail_kpi": "payoff_metric_lock_no_model_training_no_wfo_no_mt5_no_authority(보상 지표 잠금, 모델학습/WFO/MT5/권위 없음)",
        "external_verification_status": "grok_stage_open_review_completed_runtime_probe_requires_handoff_candidate(그록 단계 개방 검토 완료, 런타임 탐침은 인계 후보 필요)",
        "notes": f"next={NEXT_RUN_ID};pre_scout_sanity_required=true;no_authority",
        "question": "Can train-only payoff asymmetry identify a stronger PF source?(학습 전용 보상 비대칭이 더 강한 수익 팩터 원천을 찾을 수 있는가?)",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "run_family": "stage_open(단계 개방)",
    }


def update_current_truth(summary: dict[str, Any]) -> None:
    io_path(WORKSPACE_STATE).write_text(workspace_state(summary), encoding="utf-8-sig")
    f03b.write_text_sig(CURRENT_WORKING_STATE, current_working_state(summary))


def workspace_state(summary: dict[str, Any]) -> str:
    return "\n".join([
        f"current_stage_id: {STAGE_ID}",
        f"current_run_id: {RUN_ID}",
        f"latest_completed_run_id: {RUN_ID}",
        f"current_status: {summary['status']}",
        f"current_judgment: {summary['judgment']}",
        f"next_run_id: {NEXT_RUN_ID}",
        "runtime_authority: not_claimed",
        "operating_promotion: not_claimed",
        "goal_achieve: not_claimed",
        f"updated_at_utc: '{summary['created_at_utc']}'",
        "",
    ])


def current_working_state(summary: dict[str, Any]) -> str:
    return f"""# Current Working State(현재 작업 상태)

Updated(갱신): {summary['created_at_utc']}

## Active Stage(현재 단계)

- stage(단계): `{STAGE_ID}`
- latest run(최근 실행): `{RUN_ID}`
- status(상태): `{summary['status']}`
- judgment(판정): `{summary['judgment']}`
- next run(다음 실행): `{NEXT_RUN_ID}`

## Current Truth(현재 진실)

Action(행동): Frontier23(전선23)을 payoff asymmetry PF source scout(보상 비대칭 수익 팩터 원천 탐색)로 열었습니다.

Effect(효과): F22(전선22)의 shock+trend lifecycle(충격+추세 생명주기)을 상속하지 않고, train-only payoff distribution(학습 전용 보상 분포)이 PF source(수익 팩터 원천)를 먼저 만드는지 확인합니다.

Claim boundary(주장 경계): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def readme_text(summary: dict[str, Any]) -> str:
    return f"""# {STAGE_ID}

Purpose(목적): train-only payoff asymmetry(학습 전용 보상 비대칭)가 US100 M5 PF source(수익 팩터 원천)를 만들 수 있는지 탐색합니다.

Boundary(경계): scout-only(탐색 전용)입니다. completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 없습니다.

Current run(현재 실행): `{RUN_ID}`

Next run(다음 실행): `{NEXT_RUN_ID}`
"""


def stage_brief(summary: dict[str, Any]) -> str:
    return f"""# Frontier23 Stage Brief(전선23 단계 요약)

Opened(개방): {summary['created_at_utc']}

Frontier thesis(전선 가설): {summary['frontier_thesis']}

Hypothesis(가설): {summary['hypothesis']}

Novelty delta(신규성 차이): F23(전선23)은 shock-required(충격 필수)나 lifecycle-first(생명주기 우선)가 아닙니다. train-only outcome-conditioned payoff asymmetry(학습 결과 분포 기반 보상 비대칭)를 먼저 고르고, validation/OOS(검증/표본외)는 읽기 전용으로만 확인합니다.

Exit rule(종료 규칙): proxy(프록시), repair(수리), closeout(마감)을 거쳐 completion candidate(완성 후보), preserved clue(보존 단서), negative memory(부정 기억), invalid setup(무효 설정), blocked(차단) 중 하나로 닫습니다.

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 not_claimed(주장 없음)입니다.
"""


def lock_spec(summary: dict[str, Any]) -> str:
    lines = ["# Frontier23 Payoff Asymmetry Lock Spec(전선23 보상 비대칭 잠금 명세)", ""]
    lines.append("Payoff metrics(보상 지표):")
    lines.extend(f"- {key}: {value}" for key, value in PAYOFF_METRICS.items())
    lines.append("")
    lines.append("Locks(잠금):")
    lines.extend(f"- {key}: {value}" for key, value in LOCKS.items())
    lines.append("")
    return "\n".join(lines)


def do_not_repeat_text() -> str:
    return """# Frontier23 Do Not Repeat(전선23 반복 금지)

- Do not require shock+trend primary entry(충격+추세 주 진입 필수화 금지).
- Do not run hold2/ATR lifecycle-first repair before proxy seed(프록시 씨앗 전 hold2/ATR 생명주기 우선 수리 금지).
- Do not restate F20 rule atlas(F20 규칙 지도 재진술 금지).
- Do not use validation/OOS for threshold or condition selection(검증/표본외를 임계값 또는 조건 선택에 사용 금지).
- Do not export ONNX or train a model before handoff candidate(인계 후보 전 ONNX 내보내기 또는 모델 학습 금지).
"""


def experiment_design_text(summary: dict[str, Any]) -> str:
    return f"""# Frontier23 Experiment Design(전선23 실험 설계)

- hypothesis(가설): {summary['hypothesis']}
- decision_use(결정 사용처): {summary['decision_use']}
- comparison_baseline(비교 기준): {summary['comparison_baseline']}
- control_variables(통제 변수): {', '.join(summary['control_variables'])}
- changed_variables(변경 변수): {', '.join(summary['changed_variables'])}
- sample_scope(표본 범위): {summary['sample_scope']}
- success_criteria(성공 기준): {json.dumps(summary['success_criteria'], ensure_ascii=False)}
- failure_criteria(실패 기준): {', '.join(summary['failure_criteria'])}
- invalid_conditions(무효 조건): {', '.join(summary['invalid_conditions'])}
- stop_conditions(중단 조건): {', '.join(summary['stop_conditions'])}
"""


def prior_stage_scan_text() -> str:
    return """# Frontier23 Prior Stage Scan(전선23 이전 단계 점검)

F22 preserved clue(F22 보존 단서): shock+trend hold2 lifecycle(충격+추세 hold2 생명주기)은 낮은 DD(손실폭)와 목표 density(빈도)를 보였지만 reference-only(참조 전용)입니다.

F22 negative memory(F22 부정 기억): shock-anchored cross-family PF source(충격 고정 교차군 수익 팩터 원천)는 seed/handoff(씨앗/인계)를 만들지 못했습니다.

F20/F21 boundary(F20/F21 경계): rule atlas(규칙 지도)와 lifecycle repair(생명주기 수리)는 reference only(참조 전용)입니다. winner/baseline/promotion/runtime authority(승자/기준선/승격/런타임 권위)는 상속하지 않습니다.
"""


def input_refs_text(summary: dict[str, Any]) -> str:
    return f"""# Frontier23 Input References(전선23 입력 참조)

- dataset(데이터셋): `{DATASET_PATH.as_posix()}`
- feature order(피처 순서): `{FEATURE_ORDER_PATH.as_posix()}`
- feature hash(피처 해시): `{summary['feature_order_hash']}`
- Grok packet(그록 묶음): `{GROK_PACKET.as_posix()}`
"""


def review_index() -> str:
    return f"""# Frontier23 Review Index(전선23 검토 색인)

- stage open report(단계 개방 보고서): `{REPORT_PATH.as_posix()}`
- Grok receipt(그록 영수증): `03_reviews/grok_stage_open_receipt.md`
- local verification(로컬 검증): `03_reviews/local_verification.md`
- gate audit(게이트 감사): `03_reviews/required_gate_coverage_audit.md`
"""


def grok_receipt_text(summary: dict[str, Any]) -> str:
    return f"""# Frontier23 Grok Stage Open Receipt(전선23 그록 단계 개방 영수증)

Trigger reason(트리거 이유): stage open required by goal(목표가 단계 개방 검토를 요구).

Review size(검토 크기): small review(소규모 검토).

Direction before Grok(그록 전 방향): payoff asymmetry PF source scout(보상 비대칭 수익 팩터 원천 탐색).

Prompt(프롬프트): `{summary['grok']['prompt']}`

Output(출력): `{summary['grok']['output']}`

Advice classification(조언 분류): `{summary['grok']['classification']}`.

Accepted adjustments(수용 조정): metric definition lock(지표 정의 잠금), pre-scout sanity gate(탐색 전 건전성 게이트), novelty guard(신규성 가드), no lifecycle before seed(씨앗 전 생명주기 금지), ONNX scope honesty(ONNX 범위 정직성).

Local verification(로컬 검증): `{summary['local_verification']['judgment']}`

Final Codex direction(최종 Codex 방향): F23B(전선23B)는 train-only payoff asymmetry sanity gate(학습 전용 보상 비대칭 건전성 게이트)를 먼저 통과해야 합니다.
"""


def local_verification_text(summary: dict[str, Any]) -> str:
    lines = ["# Frontier23 Local Verification(전선23 로컬 검증)", ""]
    for key, value in summary["local_verification"]["checks"].items():
        lines.append(f"- {key}: `{value}`")
    lines.append("")
    lines.append(f"Judgment(판정): `{summary['local_verification']['judgment']}`")
    return "\n".join(lines) + "\n"


def gate_audit(summary: dict[str, Any]) -> str:
    return f"""# Frontier23 Required Gate Coverage Audit(전선23 필수 게이트 커버리지 감사)

- external_review_packet(외부 검토 묶음): covered by(충족) `{GROK_PACKET.as_posix()}`
- work_packet_schema_lint(작업 묶음 스키마 점검): experiment design fields(실험 설계 필드) materialized(물질화)
- pre_scout_sanity_gate(탐색 전 건전성 게이트): required for(필수 대상) `{NEXT_RUN_ID}`
- final_claim_guard(최종 주장 방지): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성) all not_claimed(모두 주장 없음)
"""


def report_text(summary: dict[str, Any]) -> str:
    return f"""# Frontier23A Stage Open Report(전선23A 단계 개방 보고서)

Updated(갱신): {summary['created_at_utc']}

Status(상태): `{summary['status']}`

Judgment(판정): `{summary['judgment']}`

Action(행동): Frontier23(전선23)을 payoff asymmetry PF source scout(보상 비대칭 수익 팩터 원천 탐색)로 열었습니다.

Effect(효과): shock+trend(충격+추세) 반복 대신, train-only payoff distribution(학습 전용 보상 분포)이 PF source(수익 팩터 원천)를 만드는지 먼저 확인합니다.

Grok classification(그록 분류): `{summary['grok']['classification']}`

Local verification(로컬 검증): `{summary['local_verification']['judgment']}`

Next action(다음 행동): `{NEXT_RUN_ID}`

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def selection_status(summary: dict[str, Any]) -> str:
    return f"""# Frontier23 Selection Status(전선23 선택 상태)

Updated(갱신): {summary['created_at_utc']}

Selection(선택): no selected baseline/completion candidate/promotion/runtime authority(선택 기준선/완성 후보/승격/런타임 권위 없음).

Status(상태): `{summary['status']}`

Next action(다음 행동): `{NEXT_RUN_ID}`
"""


def decision_text(summary: dict[str, Any]) -> str:
    return f"""# Decision: Open Frontier23 Payoff Asymmetry PF Source ONNX Scout(결정: 전선23 보상 비대칭 수익 팩터 원천 ONNX 탐색 개방)

Date(날짜): {summary['created_at_utc']}

Decision(결정): `{summary['status']}`

Action(행동): F23(전선23)을 train-only payoff asymmetry(학습 전용 보상 비대칭) 가설로 열었습니다.

Effect(효과): F22(전선22)의 낮은 DD(손실폭) 단서는 risk containment reference(위험 억제 참조)로만 남기고, PF source(수익 팩터 원천)는 새 선택 지표에서 찾습니다.

Next action(다음 행동): `{NEXT_RUN_ID}`
"""


def changelog_entry(summary: dict[str, Any]) -> str:
    return (
        f"- {summary['created_at_utc']}: `{RUN_ID}` opened Frontier23(전선23) after Grok adjusted review(그록 조정 검토). "
        f"Effect(효과): next run(다음 실행) `{NEXT_RUN_ID}` must pass train-only payoff sanity gate(학습 전용 보상 건전성 게이트).\n"
    )


def idea_registry_entry(summary: dict[str, Any]) -> str:
    return (
        f"- `IDEA-FR23-PAYOFF-ASYMMETRY-PF-SOURCE-ONNX-SCOUT`: `{RUN_ID}` opens payoff asymmetry PF source scout(보상 비대칭 수익 팩터 원천 탐색). "
        "Effect(효과): F22 충격/생명주기 반복 대신 학습 전용 손익 분포 비대칭을 먼저 시험합니다.\n"
    )


def artifact_identity(path: Path) -> dict[str, str]:
    return {"path": path.as_posix(), "sha256": sha256_file(path) if path_exists(path) else "missing(누락)"}


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def read_text(path: Path) -> str:
    return io_path(path).read_text(encoding="utf-8-sig")


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


if __name__ == "__main__":
    raise SystemExit(main())
