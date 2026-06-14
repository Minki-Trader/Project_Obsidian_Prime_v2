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


STAGE_ID = "stage_frontier_24__density_bridge_payoff_pockets_onnx_scout"
RUN_ID = "frontier24A_stage_open_density_bridge_payoff_pockets_hypothesis_design_v1"
RUN_NUMBER = "frontier24A"
PARENT_RUN_ID = "frontier23D_stage_closeout_payoff_asymmetry_pf_source_v1"
NEXT_RUN_ID = "frontier24B_density_bridge_payoff_pockets_proxy_scout_v1"
STATUS = "opened_frontier24_density_bridge_payoff_pockets_no_authority"
JUDGMENT = "stage_opened_after_grok_adjusted_density_bridge_contract"

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REPORT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_report.md"
SCRIPT_PATH = Path("stage_pipelines/stage_frontier_24/materialize_frontier24a_stage_open.py")
GROK_PACKET = Path("docs/agent_control/grok_reviews/2026-06-14_frontier24_stage_open/small_review")

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
DECISION_PATH = Path("docs/decisions/2026-06-14_stage_frontier_24_density_bridge_payoff_pockets_onnx_scout_open.md")

F23_SELECTION = Path("stages/stage_frontier_23__payoff_asymmetry_pf_source_onnx_scout/04_selected/selection_status.md")
F23_PRESERVED = Path("stages/stage_frontier_23__payoff_asymmetry_pf_source_onnx_scout/04_selected/preserved_clue.md")
F23_NEGATIVE = Path("stages/stage_frontier_23__payoff_asymmetry_pf_source_onnx_scout/04_selected/negative_memory.md")
F23_CLOSEOUT = Path(
    "stages/stage_frontier_23__payoff_asymmetry_pf_source_onnx_scout/"
    "03_reviews/frontier23D_stage_closeout_payoff_asymmetry_pf_source_v1_report.md"
)
F23_STAGE_LEDGER = Path("stages/stage_frontier_23__payoff_asymmetry_pf_source_onnx_scout/03_reviews/stage_run_ledger.csv")

LOCKS = {
    "selection_split": "train_only",
    "forward_splits": "validation_oos_read_only",
    "structural_unit": "same_side_multi_pocket_entry_time_or_union",
    "duplicate_trade_rule": "one_trade_per_timestamp_when_multiple_pockets_fire",
    "opposite_side_rule": "do_not_mix_long_and_short_inside_one_bridge",
    "overlap_penalty": "train_overlap_ratio_penalized_and_capped_before_forward_read",
    "diversity_guard": "max_two_pockets_per_feature_family_and_min_two_families_for_bridge",
    "density_first": "F24B optimizes density bridge first; DD normalization is only diagnostic or later repair",
    "no_lifecycle_until_seed": "no lifecycle repair until density bridge seed surface exists",
    "no_onnx_until_handoff": "no model training or ONNX branch until handoff candidate exists",
}

CRITERIA = {
    "scout_clue": {"pf": 1.10, "density_low": 5.0, "density_high": 10.0, "dd_cap": 25.0},
    "seed_surface": {"pf": 1.20, "density_low": 5.0, "density_high": 10.0, "dd_cap": 18.0},
    "handoff_candidate": {"pf": 1.50, "density_low": 5.0, "density_high": 10.0, "dd_cap": 12.0, "equity_trend_r2": 0.35},
}


def main() -> int:
    ensure_dirs()
    normalize_grok_markdown()
    created_at = utc_now()
    feature_order = read_feature_order()
    grok = read_grok_packet()
    local = local_verification(feature_order, grok)
    if local["judgment"] != "pass_open_ready_with_density_bridge_locks":
        raise RuntimeError(f"Frontier24A local verification failed: {json.dumps(local, ensure_ascii=False)}")
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
        "output_excerpt": output[:2800],
    }


def classify_grok(text: str) -> str:
    lowered = text.lower()
    if "rejected" in lowered and "accepted" not in lowered:
        return "rejected(거절)"
    if "accepted_with_adjustments" in lowered or "조정 후 수용" in text or "조정 수용" in text:
        return "accepted_with_adjustments(조정 수용)"
    if "needs_local_verification" in lowered or "로컬 검증 필요" in text:
        return "needs_local_verification(로컬 검증 필요)"
    if "accepted" in lowered or "수용" in text:
        return "accepted(수용)"
    return "classification_missing(분류 누락)"


def local_verification(feature_order: list[str], grok: dict[str, Any]) -> dict[str, Any]:
    workspace = read_text(WORKSPACE_STATE)
    f23_selection = read_text(F23_SELECTION)
    f23_preserved = read_text(F23_PRESERVED)
    f23_negative = read_text(F23_NEGATIVE)
    f23_closeout = read_text(F23_CLOSEOUT)
    f23_ledger = read_text(F23_STAGE_LEDGER)
    grok_text = read_text(GROK_PACKET / "clean_output.md")
    feature_hash = ordered_hash(feature_order)
    checks = {
        "workspace_current_stage_frontier23_closed": f"current_stage_id: stage_frontier_23__payoff_asymmetry_pf_source_onnx_scout" in workspace
        and "closed_preserved_clue_negative_memory_payoff_asymmetry_pf_lift_pockets_no_handoff" in workspace,
        "workspace_next_run_frontier24a": f"next_run_id: {RUN_ID}" in workspace,
        "f23_selection_no_authority": "no selected baseline" in f23_selection.lower(),
        "f23_preserved_near_seed_pockets": "near_seed_pockets" in f23_preserved,
        "f23_negative_reopen_density_or_dd": "density bridge" in f23_negative and "DD normalization" in f23_negative,
        "f23_closeout_metrics_anchors": all(anchor in f23_closeout for anchor in ("f23c_0123", "f23c_0071", "f23c_0233")),
        "f23_stage_ledger_seed_handoff_zero": "f23c_scout=77;seed=0;handoff=0" in f23_ledger,
        "feature_hash_matches_contract": feature_hash == EXPECTED_FEATURE_HASH,
        "dataset_exists": path_exists(DATASET_PATH),
        "grok_transport_success": grok["success"] and grok["returncode"] == 0 and not grok["timed_out"],
        "grok_direction_accepted_with_adjustments": grok["classification"] in {
            "accepted_with_adjustments(조정 수용)",
            "needs_local_verification(로컬 검증 필요)",
        },
        "grok_requires_union_semantics": "OR-union" in grok_text or "OR 합집합" in grok_text,
        "grok_requires_two_step_scope": "density bridge first" in grok_text or "빈도 연결" in grok_text,
        "grok_no_unexpected_top_level_artifacts": not grok["unexpected_top_level_artifacts"],
    }
    return {
        "judgment": "pass_open_ready_with_density_bridge_locks" if all(checks.values()) else "needs_manual_review",
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
        "frontier_thesis": (
            "F23(전선23)의 고 PF 저빈도 구간을 단일 필터로 더 깎지 않고, "
            "여러 PF-positive micro-pocket(PF 양수 미세 구간)을 같은 방향 OR-union(OR 합집합)으로 연결해 "
            "빈도 5~10회/일을 먼저 회복할 수 있는지 시험한다."
        ),
        "hypothesis": (
            "train-only micro-pocket assembly(학습 전용 미세 구간 조립)가 개별 구간의 PF(수익 팩터)를 크게 희석하지 않고 "
            "validation/OOS(검증/표본외)에서 density(빈도)를 목표 범위로 끌어올릴 수 있다."
        ),
        "decision_use": "F24B proxy scout(전선24B 프록시 탐색)의 OR-union bridge(OR 합집합 연결) 선택 계약을 고정한다.",
        "comparison_baseline": "F23 preserved pockets(전선23 보존 구간) f23c_0123, f23c_0071, f23c_0233 and unconditional same-side train baseline(무조건 같은 방향 학습 기준).",
        "control_variables": [
            "feature_set_v2 58 features(58개 피처 고정)",
            "future_log_return_12 fwd12 proxy(fwd12 프록시 고정)",
            "train-only selection(학습 전용 선택)",
            "validation/OOS read-only(검증/표본외 읽기 전용)",
        ],
        "changed_variables": [
            "structural unit changes from single pocket to same-side OR-union bridge(구조 단위가 단일 구간에서 같은 방향 OR 합집합 연결로 변경)",
            "density bridge first; DD normalization deferred to repair if needed(빈도 연결 우선, 손실폭 정규화는 필요 시 수리로 지연)",
            "overlap and diversity guards are executable constraints(중복과 다양성 보호를 실행 제약으로 고정)",
        ],
        "sample_scope": "Tier A separate(티어 A 분리); Tier B missing_required(티어 B 필수 누락); Tier A+B out_of_scope_by_claim(티어 A+B 주장 범위 밖).",
        "success_criteria": CRITERIA,
        "failure_criteria": [
            "union bridge raises density but validation/OOS PF falls below 1.10(합집합 연결이 빈도는 올리지만 검증/표본외 PF가 1.10 미만)",
            "added density is mostly overlap with no unique contribution(추가 빈도가 대부분 중복이고 고유 기여가 없음)",
            "DD remains above 25% after density bridge read(빈도 연결 뒤 손실폭이 25% 초과)",
        ],
        "invalid_conditions": [
            "validation/OOS used for bridge selection(검증/표본외를 연결 선택에 사용)",
            "opposite long/short sides mixed inside one bridge(롱/숏을 한 연결 안에 혼합)",
            "ONNX/model training before handoff candidate(인계 후보 전 ONNX/모델 학습)",
        ],
        "stop_conditions": [
            "no train-only bridge can reach target density with positive PF(학습 전용 연결이 양수 PF와 목표 빈도에 도달하지 못함)",
            "seed or handoff appears and pre-expensive Grok is required(씨앗 또는 인계가 나타나 비싼 검증 전 Grok 필요)",
            "capped density bridge repair cannot create seed/handoff(상한 빈도 연결 수리가 씨앗/인계를 만들지 못함)",
        ],
        "locks": LOCKS,
        "criteria": CRITERIA,
        "feature_count": len(feature_order),
        "feature_order_hash": ordered_hash(feature_order),
        "grok": grok,
        "local_verification": local,
        "claim_boundary": {claim: "not_claimed(주장 없음)" for claim in f03b.FORBIDDEN_CLAIMS},
    }


def write_outputs(summary: dict[str, Any]) -> None:
    write_json(RUN_ROOT / "stage_open_summary.json", summary)
    write_json(RUN_ROOT / "run_manifest.json", run_manifest(summary))
    write_json(RUN_ROOT / "density_bridge_lock.json", {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "locks": LOCKS,
        "criteria": CRITERIA,
        "search_caps": {
            "micro_pocket_keep": 120,
            "pair_candidate_cap": 240,
            "triple_candidate_cap": 240,
            "max_bridge_pockets": 4,
        },
        "claim_boundary": summary["claim_boundary"],
    })
    write_json(RUN_ROOT / "grok_receipt.json", grok_receipt(summary))
    f03b.write_text_sig(STAGE_ROOT / "README.md", readme_text(summary))
    f03b.write_text_sig(STAGE_ROOT / "00_spec" / "stage_brief.md", stage_brief(summary))
    f03b.write_text_sig(STAGE_ROOT / "00_spec" / "density_bridge_lock_spec.md", lock_spec(summary))
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
        "rule_stack": {"entry_selection": LOCKS, "criteria": CRITERIA},
        "compatibility": {"schema_version": "frontier24a_stage_open_v1", "mismatch_policy": "fail_fast(빠른 실패)"},
        "claim_boundary": summary["claim_boundary"],
    }


def grok_receipt(summary: dict[str, Any]) -> dict[str, Any]:
    return {
        "trigger_reason": "stage_open_required_by_goal(목표가 단계 개방 Grok 검토를 요구)",
        "review_size": "small(소규모)",
        "direction_before_grok": "open F24 density bridge payoff pockets scout(전선24 빈도 연결 보상 구간 탐색 개방)",
        "bounded_evidence": [F23_SELECTION.as_posix(), F23_PRESERVED.as_posix(), F23_NEGATIVE.as_posix(), F23_CLOSEOUT.as_posix()],
        "prompt_identity": {"path": summary["grok"]["prompt"], "hash": summary["grok"]["prompt_hash"]},
        "grok_output_identity": {"path": summary["grok"]["output"], "classification": summary["grok"]["classification"]},
        "advice_classification": summary["grok"]["classification"],
        "local_verification": summary["local_verification"],
        "forbidden_claim_check": summary["claim_boundary"],
        "final_codex_direction": "apply executable OR-union semantics, overlap penalty, diversity guards, and density-first two-step scope(실행 가능한 OR 합집합 의미, 중복 페널티, 다양성 보호, 빈도 우선 2단계 범위 적용)",
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
        "notes": "frontier24_stage_open_grok_adjusted_density_bridge_contract_no_authority",
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
        "guardrail_kpi": "density_bridge_lock_no_model_training_no_wfo_no_mt5_no_authority(빈도 연결 잠금, 모델학습/WFO/MT5/권위 없음)",
        "external_verification_status": "grok_stage_open_review_completed_runtime_probe_requires_handoff_candidate(그록 단계 개방 검토 완료, 런타임 탐침은 인계 후보 필요)",
        "notes": f"next={NEXT_RUN_ID};or_union_semantics_locked=true;no_authority",
        "question": "Can same-side OR-union micro-pockets bridge PF-positive low-density payoff pockets?(같은 방향 OR 합집합 미세 구간이 PF 양수 저빈도 보상 구간을 연결할 수 있는가?)",
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

Action(행동): Frontier24(전선24)를 density bridge payoff pockets scout(빈도 연결 보상 구간 탐색)로 열었습니다.

Effect(효과): F23(전선23)의 PF-positive low-density pocket(PF 양수 저빈도 구간)을 단일 필터로 반복 수리하지 않고, 같은 방향 OR-union micro-pocket bridge(OR 합집합 미세 구간 연결)로 목표 빈도 5~10회/일을 먼저 시험합니다.

Claim boundary(주장 경계): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def readme_text(summary: dict[str, Any]) -> str:
    return f"""# {STAGE_ID}

Purpose(목적): PF-positive low-density payoff pockets(PF 양수 저빈도 보상 구간)을 same-side OR-union bridge(같은 방향 OR 합집합 연결)로 묶어 density(빈도)를 5~10회/일로 회복할 수 있는지 시험합니다.

Boundary(경계): scout-only(탐색 전용)입니다. completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 없습니다.

Current run(현재 실행): `{RUN_ID}`

Next run(다음 실행): `{NEXT_RUN_ID}`
"""


def stage_brief(summary: dict[str, Any]) -> str:
    return f"""# Frontier24 Stage Brief(전선24 단계 요약)

Opened(개방): {summary['created_at_utc']}

Frontier thesis(전선 가설): {summary['frontier_thesis']}

Hypothesis(가설): {summary['hypothesis']}

Novelty delta(신규성 차이): F24(전선24)는 F23(전선23)의 single pocket + entry filter repair(단일 구간 + 진입 필터 수리)를 반복하지 않습니다. 구조 단위(structural unit, 구조 단위)를 same-side multi-pocket OR-union bridge(같은 방향 다중 구간 OR 합집합 연결)로 바꿉니다.

OR-union semantics(OR 합집합 의미): 같은 timestamp(타임스탬프)에 여러 pocket(구간)이 켜져도 한 거래로 셉니다. long/short(롱/숏)은 한 bridge(연결) 안에서 섞지 않습니다.

Exit rule(종료 규칙): proxy(프록시), capped repair(상한 수리), closeout(마감)을 거쳐 completion candidate(완성 후보), preserved clue(보존 단서), negative memory(부정 기억), invalid setup(무효 설정), blocked(차단) 중 하나로 닫습니다.

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 not_claimed(주장 없음)입니다.
"""


def lock_spec(summary: dict[str, Any]) -> str:
    lines = ["# Frontier24 Density Bridge Lock Spec(전선24 빈도 연결 잠금 명세)", ""]
    lines.append("Locks(잠금):")
    lines.extend(f"- {key}: {value}" for key, value in LOCKS.items())
    lines.append("")
    lines.append("Criteria(기준):")
    lines.append(json.dumps(CRITERIA, ensure_ascii=False, indent=2))
    lines.append("")
    return "\n".join(lines)


def do_not_repeat_text() -> str:
    return """# Frontier24 Do Not Repeat(전선24 반복 금지)

- Do not repeat F23 single-pocket include/veto repair as the primary action(F23 단일 구간 포함/제외 수리를 주 행동으로 반복 금지).
- Do not optimize DD first before testing density bridge causality(빈도 연결 인과를 보기 전 손실폭 우선 최적화 금지).
- Do not mix long and short pockets inside one bridge(한 연결 안에 롱/숏 구간 혼합 금지).
- Do not count duplicate timestamp hits as multiple trades(중복 타임스탬프 신호를 여러 거래로 계산 금지).
- Do not export ONNX or train a model before handoff candidate(인계 후보 전 ONNX 내보내기 또는 모델 학습 금지).
"""


def experiment_design_text(summary: dict[str, Any]) -> str:
    return f"""# Frontier24 Experiment Design(전선24 실험 설계)

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
- evidence_plan(근거 계획): F24B run manifest(실행 목록), micro-pocket table(미세 구간 표), bridge candidate summary(연결 후보 요약), split metrics(분할 지표), run registry(실행 등록부), stage ledger(단계 장부).
"""


def prior_stage_scan_text() -> str:
    return """# Frontier24 Prior Stage Scan(전선24 이전 단계 점검)

F23 preserved clue(전선23 보존 단서): `f23_payoff_asymmetry_near_seed_pockets_reference_only(전선23 보상 비대칭 근접 씨앗 구간 참조 전용)`.

- `f23c_0123`: density aligned(빈도 맞음), OOS PF weak(표본외 PF 약함).
- `f23c_0071`: high PF(고 PF), low density(저 빈도).
- `f23c_0233`: PF-density possible(PF-빈도 가능), DD fail(손실폭 실패).

F23 negative memory(전선23 부정 기억): single-pocket payoff asymmetry + entry-known filters(단일 구간 보상 비대칭 + 진입시점 필터)는 seed/handoff(씨앗/인계)를 만들지 못했습니다.

Reference boundary(참조 경계): F23(전선23)은 reference only(참조 전용)입니다. winner/baseline/promotion/runtime authority(승자/기준선/승격/런타임 권위)는 상속하지 않습니다.
"""


def input_refs_text(summary: dict[str, Any]) -> str:
    return f"""# Frontier24 Input References(전선24 입력 참조)

- dataset(데이터셋): `{DATASET_PATH.as_posix()}`
- feature order(피처 순서): `{FEATURE_ORDER_PATH.as_posix()}`
- feature hash(피처 해시): `{summary['feature_order_hash']}`
- Grok packet(그록 묶음): `{GROK_PACKET.as_posix()}`
- F23 closeout(전선23 마감): `{F23_CLOSEOUT.as_posix()}`
"""


def review_index() -> str:
    return f"""# Frontier24 Review Index(전선24 검토 색인)

- stage open report(단계 개방 보고서): `{REPORT_PATH.as_posix()}`
- Grok receipt(그록 영수증): `03_reviews/grok_stage_open_receipt.md`
- local verification(로컬 검증): `03_reviews/local_verification.md`
- gate audit(게이트 감사): `03_reviews/required_gate_coverage_audit.md`
"""


def grok_receipt_text(summary: dict[str, Any]) -> str:
    return f"""# Frontier24 Grok Stage Open Receipt(전선24 그록 단계 개방 영수증)

Trigger reason(트리거 이유): stage open required by goal(목표가 단계 개방 검토를 요구).

Review size(검토 크기): small review(소규모 검토).

Direction before Grok(그록 전 방향): density bridge payoff pockets scout(빈도 연결 보상 구간 탐색).

Prompt(프롬프트): `{summary['grok']['prompt']}`

Output(출력): `{summary['grok']['output']}`

Advice classification(조언 분류): `{summary['grok']['classification']}`.

Accepted adjustments(수용 조정): OR-union semantics(OR 합집합 의미), overlap penalty(중복 페널티), diversity guard(다양성 보호), density-first two-step scope(빈도 우선 2단계 범위), smoothness proxy(매끄러움 프록시)를 명시했습니다.

Local verification(로컬 검증): `{summary['local_verification']['judgment']}`

Final Codex direction(최종 Codex 방향): F24B(전선24B)는 density bridge(빈도 연결)를 먼저 시험하고, DD normalization(손실폭 정규화)은 필요 시 수리로 분리합니다.
"""


def local_verification_text(summary: dict[str, Any]) -> str:
    lines = ["# Frontier24 Local Verification(전선24 로컬 검증)", ""]
    for key, value in summary["local_verification"]["checks"].items():
        lines.append(f"- {key}: `{value}`")
    lines.append("")
    lines.append(f"Judgment(판정): `{summary['local_verification']['judgment']}`")
    return "\n".join(lines) + "\n"


def gate_audit(summary: dict[str, Any]) -> str:
    return f"""# Frontier24 Required Gate Coverage Audit(전선24 필수 게이트 커버리지 감사)

- external_review_packet(외부 검토 묶음): covered by(충족) `{GROK_PACKET.as_posix()}`
- work_packet_schema_lint(작업 묶음 스키마 점검): experiment design fields(실험 설계 필드) materialized(물질화)
- local_verification_gate(로컬 검증 게이트): `{summary['local_verification']['judgment']}`
- OR_union_contract_gate(OR 합집합 계약 게이트): duplicate timestamp(중복 타임스탬프), overlap penalty(중복 페널티), side rule(방향 규칙) recorded(기록)
- final_claim_guard(최종 주장 방어): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성) all not_claimed(모두 주장 없음)
"""


def report_text(summary: dict[str, Any]) -> str:
    return f"""# Frontier24A Stage Open Report(전선24A 단계 개방 보고서)

Updated(갱신): {summary['created_at_utc']}

Status(상태): `{summary['status']}`

Judgment(판정): `{summary['judgment']}`

Action(행동): Frontier24(전선24)를 density bridge payoff pockets scout(빈도 연결 보상 구간 탐색)로 열었습니다.

Effect(효과): F23(전선23)의 high-PF low-density(고 PF 저빈도) 단서를 단일 구간 수리로 반복하지 않고, same-side OR-union bridge(같은 방향 OR 합집합 연결)로 빈도 5~10회/일을 먼저 시험합니다.

Grok classification(그록 분류): `{summary['grok']['classification']}`

Local verification(로컬 검증): `{summary['local_verification']['judgment']}`

Next action(다음 행동): `{NEXT_RUN_ID}`

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def selection_status(summary: dict[str, Any]) -> str:
    return f"""# Frontier24 Selection Status(전선24 선택 상태)

Updated(갱신): {summary['created_at_utc']}

Selection(선택): no selected baseline/completion candidate/promotion/runtime authority(선택 기준선/완성 후보/승격/런타임 권위 없음).

Status(상태): `{summary['status']}`

Next action(다음 행동): `{NEXT_RUN_ID}`
"""


def decision_text(summary: dict[str, Any]) -> str:
    return f"""# Decision: Open Frontier24 Density Bridge Payoff Pockets ONNX Scout(결정: 전선24 빈도 연결 보상 구간 ONNX 탐색 개방)

Date(날짜): {summary['created_at_utc']}

Decision(결정): `{summary['status']}`

Action(행동): F24(전선24)를 same-side OR-union density bridge(같은 방향 OR 합집합 빈도 연결) 가설로 열었습니다.

Effect(효과): F23(전선23) 단서는 reference only(참조 전용)로 쓰고, winner/baseline/promotion/runtime authority(승자/기준선/승격/런타임 권위)는 상속하지 않습니다.

Next action(다음 행동): `{NEXT_RUN_ID}`
"""


def changelog_entry(summary: dict[str, Any]) -> str:
    return (
        f"- {summary['created_at_utc']}: `{RUN_ID}` opened Frontier24(전선24) after Grok adjusted review(그록 조정 검토). "
        f"Effect(효과): next run(다음 실행) `{NEXT_RUN_ID}` must test executable same-side OR-union density bridge(실행 가능한 같은 방향 OR 합집합 빈도 연결)를 시험합니다.\n"
    )


def idea_registry_entry(summary: dict[str, Any]) -> str:
    return (
        f"- `IDEA-FR24-DENSITY-BRIDGE-PAYOFF-POCKETS-ONNX-SCOUT`: `{RUN_ID}` opens density bridge payoff pockets scout(빈도 연결 보상 구간 탐색). "
        "Effect(효과): F23 단일 구간 수리 반복 대신 다중 미세 구간 OR 합집합으로 빈도 회복을 시험합니다.\n"
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
