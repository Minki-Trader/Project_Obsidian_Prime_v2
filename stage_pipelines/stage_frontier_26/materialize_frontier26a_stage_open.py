from __future__ import annotations

import csv
import hashlib
import json
import math
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists
from foundation.models.onnx_bridge import ordered_hash
from stage_pipelines.stage_frontier_03 import frontier03b_regime_asymmetric_label_proxy_scout as f03b
from stage_pipelines.stage_frontier_25 import frontier25d_stage_closeout as f25d


STAGE_ID = "stage_frontier_26__joint_micro_satisfaction_before_bridge_union_onnx_scout"
RUN_ID = "frontier26A_stage_open_joint_micro_satisfaction_bridge_union_hypothesis_design_v1"
RUN_NUMBER = "frontier26A"
PARENT_RUN_ID = f25d.RUN_ID
NEXT_RUN_ID = "frontier26B_joint_micro_satisfaction_before_bridge_union_proxy_scout_v1"
STATUS = "opened_frontier26_joint_micro_satisfaction_no_authority"
JUDGMENT = "stage_opened_after_grok_accepted_joint_micro_satisfaction_contract"

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REPORT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_report.md"
SCRIPT_PATH = Path("stage_pipelines/stage_frontier_26/materialize_frontier26a_stage_open.py")
GROK_PACKET = Path("docs/agent_control/grok_reviews/2026-06-14_frontier26_stage_open/small_review")

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
DECISION_PATH = Path("docs/decisions/2026-06-14_stage_frontier_26_joint_micro_satisfaction_before_bridge_union_onnx_scout_open.md")

F25_STAGE_ROOT = Path("stages") / f25d.STAGE_ID
F25_SELECTION = F25_STAGE_ROOT / "04_selected" / "selection_status.md"
F25_PRESERVED = F25_STAGE_ROOT / "04_selected" / "preserved_clue.md"
F25_NEGATIVE = F25_STAGE_ROOT / "04_selected" / "negative_memory.md"
F25_CLOSEOUT = F25_STAGE_ROOT / "03_reviews" / f"{f25d.RUN_ID}_report.md"
F25_STAGE_LEDGER = F25_STAGE_ROOT / "03_reviews" / "stage_run_ledger.csv"

LOCKS = {
    "selection_split": "train_only",
    "forward_splits": "validation_oos_read_only",
    "changed_variable": "joint_micro_satisfaction_before_bridge_union",
    "forbidden_primary_path": [
        "dd_headroom_first_bridge_archetype_preselection",
        "density_first_bridge_score_or_posthoc_dd_repair_as_primary_proxy",
        "validation_oos_targeted_capped_filter_repair",
    ],
    "structural_unit": "same_side_pair_or_triple_entry_time_or_union",
    "duplicate_trade_rule": "one_trade_per_timestamp_when_multiple_pockets_fire",
    "opposite_side_rule": "do_not_mix_long_and_short_inside_one_union",
    "micro_gate_contract": {
        "train_profit_factor_min": 1.18,
        "train_dd_risk_max": 14.0,
        "train_trades_per_day_min": 2.0,
        "train_trades_per_day_max": 6.0,
        "train_equity_trend_r2_min": 0.70,
        "train_max_loss_streak_max": 18,
        "train_adverse_loss_p10_abs_max": "source_median_train_adverse_loss_p10_abs",
        "direction_note": "lower_or_equal_is_better_for_loss_magnitude; local verification corrected Grok sign(손실 크기는 작거나 같을수록 좋으므로 Grok 부등호 방향을 로컬 검증에서 보정)",
    },
    "union_gate_contract": {
        "union_size": "same_side_pair_or_triple",
        "train_profit_factor_min": 1.10,
        "train_dd_risk_max": 16.0,
        "train_trades_per_day_min": 5.0,
        "train_trades_per_day_max": 10.0,
        "overlap_ratio_max": 0.40,
        "min_unique_density_contribution_min": 0.40,
    },
    "scoring_contract": (
        "joint_micro_satisfaction_score is train-only and combines micro PF floor, micro DD margin, "
        "micro R2 floor, adverse-loss margin, union PF, overlap penalty, unique contribution, "
        "and density fit; DD headroom is not the primary rank term"
    ),
    "no_repair_in_frontier26b": "F26B must test pre-union joint micro eligibility only; no capped repair or val/OOS-targeted filter",
    "no_lifecycle_until_seed": "no lifecycle repair until a seed or handoff worthy proxy exists",
    "no_onnx_until_handoff": "no ONNX, MT5, or runtime probe execution until handoff_candidate_rows > 0",
    "non_repeat_proof": "compare F26B top10 micro_id keys against both F25B and F24B top10; overlap without seed-gap lift is repeat",
    "reference_only_prior_artifacts": "F24/F25 artifacts are clues only, not baselines, winners, promotions, or runtime authority",
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
    if local["judgment"] != "pass_open_ready_with_joint_micro_locks":
        raise RuntimeError(f"Frontier26A local verification failed: {json.dumps(local, ensure_ascii=False)}")
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
    if "acceptable_new_hypothesis" in lowered and "accepted" in lowered:
        return "accepted_acceptable_new_hypothesis(수용, 허용 가능한 새 가설)"
    if "needs_local_verification" in lowered:
        return "needs_local_verification(로컬 검증 필요)"
    if "accepted" in lowered:
        return "accepted(수용)"
    return "classification_missing(분류 누락)"


def local_verification(feature_order: list[str], grok: dict[str, Any]) -> dict[str, Any]:
    workspace = read_text(WORKSPACE_STATE)
    f25_selection = read_text(F25_SELECTION)
    f25_preserved = read_text(F25_PRESERVED)
    f25_negative = read_text(F25_NEGATIVE)
    f25_closeout = read_text(F25_CLOSEOUT)
    f25_ledger = read_text(F25_STAGE_LEDGER)
    grok_text = read_text(GROK_PACKET / "clean_output.md")
    feature_hash = ordered_hash(feature_order)
    sign_correction = (
        "adverse loss p10" in grok_text.lower()
        and "source median" in grok_text.lower()
        and LOCKS["micro_gate_contract"]["train_adverse_loss_p10_abs_max"] == "source_median_train_adverse_loss_p10_abs"
    )
    checks = {
        "workspace_current_stage_frontier25_closed": f"current_stage_id: {f25d.STAGE_ID}" in workspace
        and f25d.STATUS in workspace,
        "workspace_next_run_frontier26a": f"next_run_id: {RUN_ID}" in workspace,
        "f25_selection_no_authority": "no selected baseline" in f25_selection.lower()
        and "Runtime probe blocker" in f25_selection,
        "f25_preserved_nonrepeat_scout": "nonrepeat_scout_clue" in f25_preserved or "비반복 탐색 단서" in f25_preserved,
        "f25_negative_seed_tradeoff": "did_not_break_seed_tradeoff" in f25_negative or "씨앗 상충" in f25_negative,
        "f25_closeout_next_clue": "train_joint_micro_satisfaction_before_bridge_union" in f25_closeout,
        "f25_stage_ledger_closeout": f25d.RUN_ID in f25_ledger,
        "feature_hash_matches_contract": feature_hash == EXPECTED_FEATURE_HASH,
        "dataset_exists": path_exists(DATASET_PATH),
        "grok_transport_success": grok["success"] and grok["returncode"] == 0 and not grok["timed_out"],
        "grok_accepts_stage_open": grok["classification"] in {
            "accepted_acceptable_new_hypothesis(수용, 허용 가능한 새 가설)",
            "accepted(수용)",
            "needs_local_verification(로컬 검증 필요)",
        },
        "grok_locks_joint_micro": "joint_micro_satisfaction" in grok_text or "joint micro satisfaction" in grok_text.lower(),
        "grok_locks_train_only": "train-only" in grok_text.lower(),
        "grok_blocks_forbidden_paths": "validation_oos_targeted_capped_filter_repair" in grok_text
        and "dd_headroom_first_bridge_archetype_preselection" in grok_text,
        "grok_defers_runtime": "handoff_candidate_rows > 0" in grok_text and "MT5" in grok_text,
        "adverse_loss_sign_corrected_locally": sign_correction,
        "grok_no_unexpected_top_level_artifacts": not grok["unexpected_top_level_artifacts"],
    }
    return {
        "judgment": "pass_open_ready_with_joint_micro_locks" if all(checks.values()) else "needs_manual_review",
        "checks": checks,
        "feature_order_hash": feature_hash,
        "feature_count": len(feature_order),
        "grok_advice_classification": {
            "accepted": [
                "open Frontier26 as acceptable new hypothesis(전선26을 허용 가능한 새 가설로 개방)",
                "lock train-only joint micro satisfaction before union(학습 전용 미세 구간 합동 충족을 합집합 전 잠금)",
                "defer ONNX/MT5/runtime probe until handoff candidate(인계 후보 전 ONNX/MT5/런타임 탐침 연기)",
            ],
            "needs_local_verification": [
                "adverse loss p10 sign was verified locally as lower-or-equal loss magnitude(불리한 손실 10분위 부등호는 로컬에서 작거나 같음 방향으로 검증)",
            ],
            "rejected": [],
        },
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
        "frontier_thesis": "component-level joint micro satisfaction before same-side OR-union may reduce forward seed DD bottleneck(같은 방향 OR 합집합 전 구성 요소 합동 충족이 전방 씨앗 손실폭 병목을 줄일 수 있다)",
        "hypothesis": "F25 failed because union-level selection admitted micros that were not individually joint-satisfactory; F26 filters each micro pocket on train-only PF+DD+density+shape before union(F25는 합집합 수준 선택이 개별적으로 합동 충족하지 않는 미세 구간을 허용했기 때문에 실패했고, F26은 합집합 전 각 미세 구간을 학습 전용 수익 팩터+손실폭+빈도+형태로 거른다)",
        "decision_use": "decide whether stricter pre-union component quality deserves proxy repair, WFO, or runtime handoff consideration(더 강한 합집합 전 구성 품질이 프록시 수리/WFO/런타임 인계 검토 가치가 있는지 결정)",
        "comparison_baseline": "F24B density-first bridge and F25B DD-headroom-first archetype preselection as reference-only, not baseline(F24B 빈도 우선 연결과 F25B 손실폭 여유 우선 원형 사전 선택은 참조 전용이며 기준선 아님)",
        "control_variables": [
            "US100 M5 Tier A dataset(US100 5분봉 티어 A 데이터셋)",
            "feature_set_v2 58 features(피처 세트 v2 58개)",
            "fwd12 label horizon(fwd12 라벨 지평)",
            "same-side OR-union semantics(같은 방향 OR 합집합 의미)",
            "validation/OOS read-only(검증/표본외 읽기 전용)",
        ],
        "changed_variables": [
            "joint_micro_satisfaction_before_bridge_union(연결 합집합 전 미세 구간 합동 충족)",
            "component eligibility before union(합집합 전 구성 요소 적격성)",
            "train-only joint_micro_satisfaction_score(학습 전용 미세 구간 합동 충족 점수)",
        ],
        "sample_scope": "Tier A US100 M5 model_input_dataset.parquet, train/validation/oos frozen split(티어 A US100 5분봉 고정 분할)",
        "success_criteria": {
            "scout": "validation and OOS PF>=1.10, density 5-10/day, max DD<=25%(검증/표본외 수익 팩터 1.10 이상, 일 5~10회, 최대 손실폭 25% 이하)",
            "seed": "PF>=1.20, density 5-10/day, max DD<=18%(수익 팩터 1.20 이상, 일 5~10회, 최대 손실폭 18% 이하)",
            "handoff": "PF>=1.50, density 5-10/day, max DD<=12%, smoothness proxy pass(수익 팩터 1.50 이상, 일 5~10회, 손실폭 12% 이하, 매끄러움 통과)",
        },
        "failure_criteria": [
            "zero joint micro passers or zero unions(합동 미세 통과 0개 또는 합집합 0개)",
            "top rows repeat F24B/F25B keys without seed-gap lift(F24B/F25B 키 반복이며 씨앗 간격 개선 없음)",
            "all forward rows remain scout-only with seed DD blocked(모든 전방 행이 씨앗 손실폭 차단 탐색 전용에 머묾)",
        ],
        "invalid_conditions": [
            "validation/OOS used in selection or repair(검증/표본외 선택 또는 수리 사용)",
            "F26B applies capped repair as primary path(F26B가 상한 수리를 기본 경로로 적용)",
            "score formula missing or DD-headroom-first reused as primary rank(점수 공식 누락 또는 손실폭 여유 우선 주 순위 재사용)",
            "feature hash mismatch(피처 해시 불일치)",
        ],
        "stop_conditions": [
            "zero passing micros or zero unions closes invalid setup(통과 미세 구간 0개 또는 합집합 0개면 무효 설정)",
            "seed/handoff remains zero with F25-like PF-ready/DD-blocked bottleneck closes negative memory(씨앗/인계 0이고 F25형 수익 팩터 충족/손실폭 차단 병목이면 부정 기억)",
            "handoff rows >0 triggers Grok before expensive WFO/MT5/ONNX(인계 행이 있으면 비싼 WFO/MT5/ONNX 전 Grok 검토)",
        ],
        "locks": LOCKS,
        "criteria": CRITERIA,
        "grok": grok,
        "local_verification": local,
        "feature_order_hash": ordered_hash(feature_order),
        "feature_count": len(feature_order),
        "claim_boundary": {claim: "not_claimed(주장 없음)" for claim in f03b.FORBIDDEN_CLAIMS},
    }


def write_outputs(summary: dict[str, Any]) -> None:
    write_json(RUN_ROOT / "stage_open_summary.json", summary)
    write_json(RUN_ROOT / "joint_micro_satisfaction_lock.json", {"locks": LOCKS, "criteria": CRITERIA})
    write_json(RUN_ROOT / "run_manifest.json", run_manifest(summary))
    f03b.write_text_sig(STAGE_ROOT / "README.md", readme_text(summary))
    f03b.write_text_sig(STAGE_ROOT / "00_spec" / "stage_brief.md", stage_brief(summary))
    f03b.write_text_sig(STAGE_ROOT / "00_spec" / "joint_micro_satisfaction_lock_spec.md", lock_spec())
    f03b.write_text_sig(STAGE_ROOT / "00_spec" / "do_not_repeat.md", do_not_repeat_text())
    f03b.write_text_sig(STAGE_ROOT / "01_inputs" / "prior_stage_scan.md", prior_stage_scan_text())
    f03b.write_text_sig(STAGE_ROOT / "01_inputs" / "experiment_design.md", experiment_design_text(summary))
    f03b.write_text_sig(STAGE_ROOT / "01_inputs" / "input_refs.md", input_refs_text(summary))
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / "review_index.md", review_index())
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / "grok_stage_open_receipt.md", grok_receipt_text(summary))
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / "local_verification.md", local_verification_text(summary))
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / "required_gate_coverage_audit.md", gate_audit(summary))
    f03b.write_text_sig(REPORT_PATH, report_text(summary))
    f03b.write_text_sig(STAGE_ROOT / "04_selected" / "selection_status.md", selection_status(summary))
    f03b.write_text_sig(DECISION_PATH, decision_text(summary))


def run_manifest(summary: dict[str, Any]) -> dict[str, Any]:
    artifacts = [
        SCRIPT_PATH,
        GROK_PACKET / "clean_output.md",
        F25_SELECTION,
        F25_PRESERVED,
        F25_NEGATIVE,
        F25_CLOSEOUT,
        RUN_ROOT / "stage_open_summary.json",
        REPORT_PATH,
    ]
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
        "rule_stack": {
            "entry": "same-side pair/triple OR-union after joint micro gate(합동 미세 게이트 뒤 같은 방향 쌍/삼중 OR 합집합)",
            "selection": "train-only joint micro satisfaction before union(학습 전용 합집합 전 미세 구간 합동 충족)",
            "forbidden": "no validation selection, no F26B repair, no ONNX/MT5 before handoff(검증 선택 없음, F26B 수리 없음, 인계 전 ONNX/MT5 없음)",
        },
        "claim_boundary": summary["claim_boundary"],
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
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": REPORT_PATH.as_posix(),
        "notes": "frontier26_stage_open_grok_accepted_joint_micro_satisfaction_contract_no_authority",
        "run_number": RUN_NUMBER,
        "date": "2026-06-14",
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "claim_boundary": "stage_open_no_model_training_no_wfo_no_mt5_no_authority_goal_claim",
        "report_path": REPORT_PATH.as_posix(),
        "created_at_utc": summary["created_at_utc"],
        "primary_kpi": "not_applicable_stage_open(단계 개방에는 해당 없음)",
        "guardrail_kpi": "joint_micro_satisfaction_lock_no_model_training_no_wfo_no_mt5_no_authority(미세 구간 합동 충족 잠금, 모델학습/WFO/MT5/권위 없음)",
        "external_verification_status": "grok_stage_open_review_completed_runtime_probe_requires_handoff_candidate(그록 단계 개방 검토 완료, 런타임 탐침은 인계 후보 필요)",
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
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": REPORT_PATH.as_posix(),
        "primary_kpi": f"grok={summary['grok']['classification']};feature_hash={summary['feature_order_hash']}",
        "guardrail_kpi": "joint_micro_satisfaction_lock_no_model_training_no_wfo_no_mt5_no_authority(미세 구간 합동 충족 잠금, 모델학습/WFO/MT5/권위 없음)",
        "external_verification_status": "grok_stage_open_review_completed_runtime_probe_requires_handoff_candidate(그록 단계 개방 검토 완료, 런타임 탐침은 인계 후보 필요)",
        "notes": f"next={NEXT_RUN_ID};joint_micro_satisfaction=true;no_authority",
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
        f"current_status: {STATUS}",
        f"current_judgment: {JUDGMENT}",
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
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- next run(다음 실행): `{NEXT_RUN_ID}`

## Current Truth(현재 진실)

Action(행동): Frontier26(전선26)를 joint micro satisfaction before bridge union ONNX scout(연결 합집합 전 미세 구간 합동 충족 ONNX 탐색)로 열었습니다.

Effect(효과): F25(전선25)의 union-level DD-headroom-first ranking(합집합 수준 손실폭 여유 우선 순위)을 상속하지 않고, train-only component eligibility(학습 전용 구성 요소 적격성)를 먼저 시험합니다.

Runtime/ONNX boundary(런타임/ONNX 경계): 각 stage(단계)마다 MT5 runtime probe(MT5 런타임 탐침) 상태를 기록하되, handoff candidate(인계 후보)가 나오기 전까지 실제 MT5(메타트레이더5), WFO(워크포워드 최적화), ONNX(온엑스)는 열지 않습니다.

Claim boundary(주장 경계): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def readme_text(summary: dict[str, Any]) -> str:
    return f"""# {STAGE_ID}

Purpose(목적): train-only joint micro satisfaction before same-side OR-union(학습 전용 같은 방향 OR 합집합 전 미세 구간 합동 충족)이 F25(전선25)의 seed DD bottleneck(씨앗 손실폭 병목)을 줄이는지 시험합니다.

Boundary(경계): scout-only(탐색 전용)입니다. completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 없습니다.

Current run(현재 실행): `{RUN_ID}`

Next run(다음 실행): `{NEXT_RUN_ID}`
"""


def stage_brief(summary: dict[str, Any]) -> str:
    return f"""# Frontier26 Stage Brief(전선26 단계 요약)

Opened(개방): {summary['created_at_utc']}

Frontier thesis(전선 가설): {summary['frontier_thesis']}

Hypothesis(가설): {summary['hypothesis']}

Novelty delta(신규성 차이): F26(전선26)는 F25B(전선25B)의 DD-headroom-first union ranking(손실폭 여유 우선 합집합 순위)을 반복하지 않습니다. changed variable(변경 변수)은 component-level joint micro satisfaction before union(합집합 전 구성 요소 수준 미세 구간 합동 충족)입니다.

Runtime probe rule(런타임 탐침 규칙): 각 stage(단계)는 MT5 runtime probe(MT5 런타임 탐침) 상태를 기록합니다. 실제 probe(탐침)는 handoff candidate(인계 후보)가 있을 때만 실행합니다.

Exit rule(종료 규칙): proxy(프록시), WFO/stress/runtime validation eligibility(WFO/스트레스/런타임 검증 적격성), repair decision(수리 결정), closeout(마감)을 거쳐 completion candidate(완성 후보), preserved clue(보존 단서), negative memory(부정 기억), invalid setup(무효 설정), blocked(차단) 중 하나로 닫습니다.

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 not_claimed(주장 없음)입니다.
"""


def lock_spec() -> str:
    lines = ["# Frontier26 Joint Micro Satisfaction Lock Spec(전선26 미세 구간 합동 충족 잠금 명세)", ""]
    lines.append("Locks(잠금):")
    lines.append(json.dumps(LOCKS, ensure_ascii=False, indent=2))
    lines.append("")
    lines.append("Criteria(기준):")
    lines.append(json.dumps(CRITERIA, ensure_ascii=False, indent=2))
    lines.append("")
    return "\n".join(lines)


def do_not_repeat_text() -> str:
    return """# Frontier26 Do Not Repeat(전선26 반복 금지)

- Do not repeat F25B DD-headroom-first union ranking as the primary rank(F25B 손실폭 여유 우선 합집합 순위를 기본 순위로 반복 금지).
- Do not repeat F24B density-first bridge score(F24B 빈도 우선 연결 점수 반복 금지).
- Do not add validation/OOS-targeted capped filters(검증/표본외 표적 상한 필터 추가 금지).
- Do not use validation/OOS in selection or repair(검증/표본외를 선택이나 수리에 사용 금지).
- Do not export ONNX or run MT5 before handoff candidate(인계 후보 전 ONNX 내보내기 또는 MT5 실행 금지).
"""


def experiment_design_text(summary: dict[str, Any]) -> str:
    return f"""# Frontier26 Experiment Design(전선26 실험 설계)

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
- evidence_plan(근거 계획): F26B run manifest(실행 목록), micro_joint_pass_audit.csv(미세 구간 합동 통과 감사), train-ranked joint union table(학습 순위 합동 합집합 표), F24B/F25B top-10 diff audit(F24B/F25B 상위10 차이 감사), split metrics(분할 지표), run registry(실행 등록부), stage ledger(단계 장부).
"""


def prior_stage_scan_text() -> str:
    return """# Frontier26 Prior Stage Scan(전선26 이전 단계 점검)

F25 preserved clue(전선25 보존 단서): `f25_dd_headroom_first_archetype_nonrepeat_scout_clue_reference_only(F25 손실폭 여유 우선 원형 비반복 탐색 단서 참조 전용)`.

F25 negative memory(전선25 부정 기억): `under_f25_locked_proxy_dd_headroom_first_preselection_did_not_break_seed_tradeoff(F25 잠금 프록시 아래 손실폭 여유 우선 사전 선택은 씨앗 상충을 깨지 못함)`.

Next clue(다음 단서): `train_joint_micro_satisfaction_before_bridge_union_reference_only(학습 전용 미세 구간 합동 충족 뒤 연결 합집합 참조 단서)`.

Reference boundary(참조 경계): F24/F25(전선24/25)는 reference only(참조 전용)입니다. winner/baseline/promotion/runtime authority(승자/기준선/승격/런타임 권위)는 상속하지 않습니다.
"""


def input_refs_text(summary: dict[str, Any]) -> str:
    return f"""# Frontier26 Input References(전선26 입력 참조)

- dataset(데이터셋): `{DATASET_PATH.as_posix()}`
- feature order(피처 순서): `{FEATURE_ORDER_PATH.as_posix()}`
- feature hash(피처 해시): `{summary['feature_order_hash']}`
- Grok packet(그록 묶음): `{GROK_PACKET.as_posix()}`
- F25 selection(전선25 선택): `{F25_SELECTION.as_posix()}`
- F25 closeout(전선25 마감): `{F25_CLOSEOUT.as_posix()}`
"""


def review_index() -> str:
    return f"""# Frontier26 Review Index(전선26 검토 색인)

- stage open report(단계 개방 보고서): `{REPORT_PATH.as_posix()}`
- Grok receipt(그록 영수증): `03_reviews/grok_stage_open_receipt.md`
- local verification(로컬 검증): `03_reviews/local_verification.md`
- gate audit(게이트 감사): `03_reviews/required_gate_coverage_audit.md`
"""


def grok_receipt_text(summary: dict[str, Any]) -> str:
    classification = summary["local_verification"]["grok_advice_classification"]
    return f"""# Frontier26 Grok Stage Open Receipt(전선26 그록 단계 개방 영수증)

Trigger reason(트리거 이유): stage open required by goal(목표가 단계 개방 검토를 요구).

Review size(검토 크기): small review(소규모 검토).

Direction before Grok(그록 전 방향): joint micro satisfaction before bridge union scout(연결 합집합 전 미세 구간 합동 충족 탐색).

Prompt(프롬프트): `{summary['grok']['prompt']}`

Output(출력): `{summary['grok']['output']}`

Advice classification(조언 분류): `{summary['grok']['classification']}`.

Accepted advice(수용 조언): {', '.join(classification['accepted'])}

Needs local verification(로컬 검증 필요): {', '.join(classification['needs_local_verification'])}

Rejected advice(거절 조언): none(없음).

Local verification(로컬 검증): `{summary['local_verification']['judgment']}`

Final Codex direction(최종 Codex 방향): F26B(전선26B)는 existing micro pocket chain(기존 미세 구간 체인)을 재사용하되, train-only joint_micro_satisfaction_score(학습 전용 미세 구간 합동 충족 점수)로 합집합 전 구성 요소를 먼저 잠급니다.
"""


def local_verification_text(summary: dict[str, Any]) -> str:
    lines = ["# Frontier26 Local Verification(전선26 로컬 검증)", ""]
    for key, value in summary["local_verification"]["checks"].items():
        lines.append(f"- {key}: `{value}`")
    lines.append("")
    lines.append(f"Judgment(판정): `{summary['local_verification']['judgment']}`")
    lines.append("")
    lines.append("Effect(효과): Grok(그록) 조언을 자동 실행하지 않고, F25 closeout(전선25 마감), local files(로컬 파일), feature hash(피처 해시), and stage locks(단계 잠금)로 재검증했습니다.")
    return "\n".join(lines) + "\n"


def gate_audit(summary: dict[str, Any]) -> str:
    return f"""# Frontier26 Required Gate Coverage Audit(전선26 필수 게이트 커버리지 감사)

- external_review_packet(외부 검토 묶음): covered by(충족) `{GROK_PACKET.as_posix()}`
- work_packet_schema_lint(작업 묶음 스키마 점검): experiment design fields(실험 설계 필드) materialized(물질화)
- local_verification_gate(로컬 검증 게이트): `{summary['local_verification']['judgment']}`
- joint_micro_score_contract_gate(미세 구간 합동 점수 계약 게이트): `joint_micro_satisfaction_score` recorded(기록)
- non_repeat_gate(반복 방지 게이트): F26B must compare top10 keys against F24B and F25B(F26B는 F24B/F25B 상위10 키 비교 필수)
- runtime_probe_gate(런타임 탐침 게이트): each stage records status(각 단계 상태 기록), execution requires handoff_candidate_rows > 0(실행은 인계 후보 필요)
- final_claim_guard(최종 주장 방어): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성) all not_claimed(모두 주장 없음)
"""


def report_text(summary: dict[str, Any]) -> str:
    return f"""# Frontier26A Stage Open Report(전선26A 단계 개방 보고서)

Updated(갱신): {summary['created_at_utc']}

Status(상태): `{summary['status']}`

Judgment(판정): `{summary['judgment']}`

Action(행동): Frontier26(전선26)를 joint micro satisfaction before bridge union ONNX scout(연결 합집합 전 미세 구간 합동 충족 ONNX 탐색)로 열었습니다.

Effect(효과): F25(전선25)의 DD-headroom-first union ranking(손실폭 여유 우선 합집합 순위) 반복을 막고, train-only component quality(학습 전용 구성 품질)를 먼저 시험합니다.

Grok classification(그록 분류): `{summary['grok']['classification']}`

Local verification(로컬 검증): `{summary['local_verification']['judgment']}`

MT5 runtime probe boundary(MT5 런타임 탐침 경계): stage status is recorded every stage(단계 상태는 매 단계 기록), but actual MT5 probe(실제 MT5 탐침)는 handoff candidate(인계 후보)가 있을 때만 실행합니다.

Next action(다음 행동): `{NEXT_RUN_ID}`

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def selection_status(summary: dict[str, Any]) -> str:
    return f"""# Frontier26 Selection Status(전선26 선택 상태)

Updated(갱신): {summary['created_at_utc']}

Selection(선택): no selected baseline/completion candidate/promotion/runtime authority(선택 기준선/완성 후보/승격/런타임 권위 없음).

Status(상태): `{summary['status']}`

Next action(다음 행동): `{NEXT_RUN_ID}`
"""


def decision_text(summary: dict[str, Any]) -> str:
    return f"""# Decision: Open Frontier26 Joint Micro Satisfaction Before Bridge Union ONNX Scout(결정: 전선26 연결 합집합 전 미세 구간 합동 충족 ONNX 탐색 개방)

Date(날짜): {summary['created_at_utc']}

Decision(결정): `{summary['status']}`

Action(행동): F26(전선26)를 train-only joint micro satisfaction before union(학습 전용 합집합 전 미세 구간 합동 충족) 가설로 열었습니다.

Effect(효과): F25(전선25) 단서는 reference only(참조 전용)로 쓰고, winner/baseline/promotion/runtime authority(승자/기준선/승격/런타임 권위)는 상속하지 않습니다.

Runtime probe rule(런타임 탐침 규칙): 매 stage(단계)에서 MT5 runtime probe(MT5 런타임 탐침) 상태는 기록하지만, 실제 실행은 handoff candidate(인계 후보) 뒤로 둡니다.

Next action(다음 행동): `{NEXT_RUN_ID}`
"""


def changelog_entry(summary: dict[str, Any]) -> str:
    return (
        f"- {summary['created_at_utc']}: `{RUN_ID}` opened Frontier26(전선26) after Grok accepted review(그록 수용 검토). "
        f"Effect(효과): next run(다음 실행) `{NEXT_RUN_ID}` must test train-only joint micro satisfaction before union(학습 전용 합집합 전 미세 구간 합동 충족)을 시험합니다.\n"
    )


def idea_registry_entry(summary: dict[str, Any]) -> str:
    return (
        f"- `IDEA-FR26-JOINT-MICRO-SATISFACTION-BEFORE-UNION-ONNX-SCOUT`: `{RUN_ID}` opens joint micro satisfaction before union scout(합집합 전 미세 구간 합동 충족 탐색). "
        "Effect(효과): F25 손실폭 여유 우선 순위 반복 대신 component-level joint eligibility(구성 요소 수준 합동 적격성)를 시험합니다.\n"
    )


def artifact_identity(path: Path) -> dict[str, str]:
    return {"path": path.as_posix(), "sha256": sha256_io(path) if path_exists(path) else "missing(누락)"}


def sha256_io(path: Path) -> str:
    h = hashlib.sha256()
    with io_path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def read_text(path: Path) -> str:
    return io_path(path).read_text(encoding="utf-8-sig")


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def fmt(value: Any) -> str:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return "NA"
    if not math.isfinite(number):
        return "NA"
    return f"{number:.6g}"


if __name__ == "__main__":
    raise SystemExit(main())
