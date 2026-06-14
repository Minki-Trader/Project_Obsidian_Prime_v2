from __future__ import annotations

import csv
import hashlib
import json
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
from stage_pipelines.stage_frontier_26 import frontier26d_stage_closeout as f26d


STAGE_ID = "stage_frontier_27__soft_joint_satisfaction_penalty_bridge_union_onnx_scout"
RUN_ID = "frontier27A_stage_open_soft_joint_satisfaction_penalty_bridge_union_hypothesis_design_v1"
RUN_NUMBER = "frontier27A"
PARENT_RUN_ID = f26d.RUN_ID
NEXT_RUN_ID = "frontier27B_soft_joint_satisfaction_penalty_bridge_union_proxy_scout_v1"
STATUS = "opened_frontier27_soft_joint_satisfaction_penalty_no_authority"
JUDGMENT = "stage_opened_after_grok_accepted_soft_penalty_contract"

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REPORT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_report.md"
SCRIPT_PATH = Path("stage_pipelines/stage_frontier_27/materialize_frontier27a_stage_open.py")
GROK_PACKET = Path("docs/agent_control/grok_reviews/2026-06-14_frontier27_stage_open/small_review")

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
DECISION_PATH = Path("docs/decisions/2026-06-14_stage_frontier_27_soft_joint_satisfaction_penalty_bridge_union_onnx_scout_open.md")

F26_STAGE_ROOT = Path("stages") / f26d.STAGE_ID
F26_SELECTION = F26_STAGE_ROOT / "04_selected" / "selection_status.md"
F26_INVALID = F26_STAGE_ROOT / "04_selected" / "invalid_setup.md"
F26_NEGATIVE = F26_STAGE_ROOT / "04_selected" / "negative_memory.md"
F26_CLOSEOUT = F26_STAGE_ROOT / "03_reviews" / f"{f26d.RUN_ID}_report.md"
F26_STAGE_LEDGER = F26_STAGE_ROOT / "03_reviews" / "stage_run_ledger.csv"

LOCKS = {
    "selection_split": "train_only",
    "forward_splits": "validation_oos_read_only",
    "changed_variable": "soft_joint_satisfaction_penalty_rank",
    "hypothesis_delta": (
        "replace F26 hard joint micro eligibility gate with train-only soft penalty rank before same-side OR-union"
    ),
    "source_micro_pool": "full_f24_80_micro_pocket_surface_reference_only_not_f26_three_passer_surface",
    "structural_unit": "same_side_pair_or_triple_entry_time_or_union",
    "duplicate_trade_rule": "one_trade_per_timestamp_when_multiple_pockets_fire",
    "opposite_side_rule": "do_not_mix_long_and_short_inside_one_union",
    "soft_penalty_contract": {
        "score_direction": "higher_is_better_after_penalty",
        "terms": [
            "train_profit_factor_shortfall_to_1_18",
            "train_dd_pressure_above_14",
            "train_density_distance_from_4_0_to_6_0_micro_band",
            "train_equity_trend_r2_shortfall_to_0_70",
            "train_max_loss_streak_pressure_above_18",
            "train_adverse_loss_p10_abs_pressure_above_source_median",
            "train_union_density_distance_from_7_5",
            "train_union_dd_pressure_above_16",
            "train_overlap_ratio_penalty",
            "min_unique_density_contribution_reward",
        ],
        "not_allowed": "using F26 micro_gate_contract or union_gate_contract pass/fail as the primary selector",
    },
    "broad_scout_envelope": {
        "purpose": "diagnostic_admission_after_penalty_rank_not_final_gate",
        "train_net_profit": "> 0",
        "train_profit_factor_min": 1.06,
        "train_trades_per_day_min": 4.0,
        "train_trades_per_day_max": 11.5,
        "train_dd_risk_max": 22.0,
        "overlap_ratio_max": 0.55,
        "min_unique_density_contribution_min": 0.35,
    },
    "forbidden_primary_path": [
        "f26_hard_gate_numeric_threshold_relaxation",
        "f25_dd_headroom_first_bridge_archetype_preselection",
        "f24_density_first_bridge_score_as_primary_rank",
        "validation_oos_targeted_repair_or_selection",
        "onnx_mt5_runtime_probe_before_handoff_candidate",
    ],
    "invalid_setup_tripwire": (
        "if F27B creates rows only by widening F26 caps without the written soft penalty mechanism, close invalid_setup"
    ),
    "no_repair_in_frontier27b": "F27B tests the locked penalty mechanism only; no capped repair or validation/OOS-targeted filter",
    "no_lifecycle_until_seed": "no lifecycle repair until a seed or handoff worthy proxy exists",
    "no_onnx_until_handoff": "no ONNX, MT5, or runtime probe execution until handoff_candidate_rows > 0",
    "non_repeat_proof": "compare F27B top10 keys against F24B, F25B, and F26B; overlap without seed-gap lift is repeat",
    "reference_only_prior_artifacts": "F24/F25/F26 artifacts are clues only, not baselines, winners, promotions, or runtime authority",
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
    if local["judgment"] != "pass_open_ready_with_soft_penalty_locks":
        raise RuntimeError(f"Frontier27A local verification failed: {json.dumps(local, ensure_ascii=False)}")
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
    if "verdict" in lowered and "accepted" in lowered and "novelty_ok" in lowered and "yes" in lowered:
        return "accepted_new_hypothesis_medium_forbidden_path_risk(수용, 새 가설, 중간 금지 경로 위험)"
    if "needs_local_verification" in lowered:
        return "needs_local_verification(로컬 검증 필요)"
    if "rejected" in lowered and "accepted" not in lowered:
        return "rejected(거절)"
    if "accepted" in lowered:
        return "accepted(수용)"
    return "classification_missing(분류 누락)"


def local_verification(feature_order: list[str], grok: dict[str, Any]) -> dict[str, Any]:
    workspace = read_text(WORKSPACE_STATE)
    f26_selection = read_text(F26_SELECTION)
    f26_invalid = read_text(F26_INVALID)
    f26_negative = read_text(F26_NEGATIVE)
    f26_closeout = read_text(F26_CLOSEOUT)
    f26_ledger = read_text(F26_STAGE_LEDGER)
    grok_text = read_text(GROK_PACKET / "clean_output.md")
    feature_hash = ordered_hash(feature_order)
    lock_json = json.dumps(LOCKS, ensure_ascii=False)
    checks = {
        "workspace_current_stage_frontier26_closed": f"current_stage_id: {f26d.STAGE_ID}" in workspace
        and f26d.STATUS in workspace,
        "workspace_next_run_frontier27a": f"next_run_id: {RUN_ID}" in workspace,
        "f26_selection_no_authority": "no selected baseline" in f26_selection.lower()
        and "Runtime probe blocker" in f26_selection,
        "f26_invalid_union_collapse": "zero valid unions" in f26_invalid.lower()
        or "zero_valid_unions" in f26_invalid,
        "f26_negative_hard_gate_collapse": "collapsed_union_surface" in f26_negative
        or "hard component gate" in f26_closeout.lower(),
        "f26_closeout_next_clue_soft_penalty": "soft_joint_satisfaction_penalty" in f26_closeout,
        "f26_stage_ledger_closeout": f26d.RUN_ID in f26_ledger,
        "feature_hash_matches_contract": feature_hash == EXPECTED_FEATURE_HASH,
        "dataset_exists": path_exists(DATASET_PATH),
        "grok_transport_success": grok["success"] and grok["returncode"] == 0 and not grok["timed_out"],
        "grok_accepts_stage_open": grok["classification"] in {
            "accepted_new_hypothesis_medium_forbidden_path_risk(수용, 새 가설, 중간 금지 경로 위험)",
            "accepted(수용)",
            "needs_local_verification(로컬 검증 필요)",
        },
        "grok_novelty_yes": "novelty_ok" in grok_text.lower() and "yes" in grok_text.lower(),
        "grok_flags_medium_risk": "forbidden_path_risk" in grok_text.lower() and "medium" in grok_text.lower(),
        "grok_requires_penalty_formula": "penalty formula" in grok_text.lower()
        and "soft penalty rank" in grok_text.lower(),
        "grok_requires_full_80_pool": "80 micro" in grok_text.lower()
        and "not restricted to f26 3" in grok_text.lower(),
        "grok_defers_runtime": "handoff_candidate_rows > 0" in grok_text and "MT5" in grok_text,
        "lock_changed_variable_soft_penalty": LOCKS["changed_variable"] == "soft_joint_satisfaction_penalty_rank",
        "lock_blocks_f26_threshold_relaxation": "f26_hard_gate_numeric_threshold_relaxation" in lock_json,
        "lock_penalty_terms_written": len(LOCKS["soft_penalty_contract"]["terms"]) >= 8,
        "lock_scout_envelope_not_final_gate": LOCKS["broad_scout_envelope"]["purpose"].startswith("diagnostic"),
        "grok_no_unexpected_top_level_artifacts": not grok["unexpected_top_level_artifacts"],
    }
    return {
        "judgment": "pass_open_ready_with_soft_penalty_locks" if all(checks.values()) else "needs_manual_review",
        "checks": checks,
        "feature_order_hash": feature_hash,
        "feature_count": len(feature_order),
        "grok_advice_classification": {
            "accepted": [
                "open Frontier27 as acceptable new hypothesis(전선27을 허용 가능한 새 가설로 개방)",
                "lock train-only soft joint satisfaction penalty rank(학습 전용 연성 합동 충족 페널티 순위 잠금)",
                "use full F24 80 micro source surface, not F26 3 passers(F24 전체 80 미세 원천 표면 사용, F26 3 통과자 제한 금지)",
                "defer ONNX/MT5/runtime probe until handoff candidate(인계 후보 전 ONNX/MT5/런타임 탐침 지연)",
            ],
            "needs_local_verification": [
                "verify F27A lock JSON and penalty formula before F27B(F27B 전 F27A 잠금 JSON과 페널티 공식 검증)",
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
        "frontier_thesis": (
            "soft joint satisfaction penalty before same-side OR-union may restore union surface without repeating F26 hard-gate relaxation"
            "(같은 방향 OR 합집합 전 연성 합동 충족 페널티가 F26 경성 게이트 완화 반복 없이 합집합 표면을 복원할 수 있음)"
        ),
        "hypothesis": (
            "F26 failed because hard component pass/fail reduced 80 micro pockets to 3 passers; F27 keeps train-only selection "
            "but ranks the full micro source by soft penalties before union construction"
            "(F26은 경성 구성 통과/탈락이 80개 미세 구간을 3개로 줄여 실패했고, F27은 학습 전용 선택을 유지하되 전체 미세 원천을 연성 페널티로 순위화한 뒤 합집합을 구성)"
        ),
        "decision_use": (
            "decide whether soft penalty ranking deserves proxy repair, WFO, or runtime handoff consideration"
            "(연성 페널티 순위가 프록시 수리, WFO, 런타임 인계 검토 가치가 있는지 결정)"
        ),
        "comparison_baseline": (
            "F24 density-first, F25 DD-headroom-first, and F26 hard joint gate are reference-only, not baselines"
            "(F24 빈도 우선, F25 손실폭 여유 우선, F26 경성 합동 게이트는 참조 전용이며 기준선 아님)"
        ),
        "control_variables": [
            "US100 M5 Tier A dataset(US100 5분봉 티어 A 데이터셋)",
            "feature_set_v2 58 features(피처 세트 v2 58개)",
            "fwd12 label horizon(fwd12 라벨 지평)",
            "same-side OR-union semantics(같은 방향 OR 합집합 의미)",
            "validation/OOS read-only(검증/OOS 읽기 전용)",
        ],
        "changed_variables": [
            "soft_joint_satisfaction_penalty_rank(연성 합동 충족 페널티 순위)",
            "full 80 micro source pool before union(합집합 전 전체 80 미세 원천 풀)",
            "diagnostic scout envelope, not final gate(진단용 탐색 외피, 최종 게이트 아님)",
        ],
        "sample_scope": "Tier A US100 M5 model_input_dataset.parquet, frozen train/validation/oos split(티어 A US100 5분봉 고정 분할)",
        "success_criteria": CRITERIA,
        "failure_criteria": [
            "zero valid soft-penalty unions(유효 연성 페널티 합집합 0개)",
            "top rows repeat F24/F25/F26 keys without seed-gap lift(F24/F25/F26 키 반복인데 씨앗 격차 개선 없음)",
            "all forward rows remain scout-only with seed DD blocked(모든 전방 행이 씨앗 손실폭에서 막힌 탐색 전용)",
        ],
        "invalid_conditions": [
            "F26 hard gate numeric relaxation is primary path(F26 경성 게이트 숫자 완화가 주 경로)",
            "validation/OOS used in selection or repair(검증/OOS를 선택 또는 수리에 사용)",
            "penalty formula missing before proxy(프록시 전 페널티 공식 누락)",
            "feature hash mismatch(피처 해시 불일치)",
        ],
        "stop_conditions": [
            "handoff rows >0 triggers Grok before WFO/MT5/ONNX(인계 행이 있으면 WFO/MT5/ONNX 전 Grok 검토)",
            "seed or scout only triggers repair-or-closeout decision(씨앗 또는 탐색만 있으면 수리 또는 마감 결정)",
            "zero union or repeat-only closes invalid_setup or negative_memory(합집합 0개 또는 반복만 있으면 무효 설정 또는 부정 기억)",
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
    write_json(RUN_ROOT / "soft_joint_satisfaction_penalty_lock.json", {"locks": LOCKS, "criteria": CRITERIA})
    write_json(RUN_ROOT / "run_manifest.json", run_manifest(summary))
    f03b.write_text_sig(STAGE_ROOT / "README.md", readme_text(summary))
    f03b.write_text_sig(STAGE_ROOT / "00_spec" / "stage_brief.md", stage_brief(summary))
    f03b.write_text_sig(STAGE_ROOT / "00_spec" / "soft_penalty_lock_spec.md", lock_spec())
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
        F26_SELECTION,
        F26_INVALID,
        F26_NEGATIVE,
        F26_CLOSEOUT,
        RUN_ROOT / "stage_open_summary.json",
        RUN_ROOT / "soft_joint_satisfaction_penalty_lock.json",
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
            "entry": "same-side pair/triple OR-union after soft penalty rank(연성 페널티 순위 뒤 같은 방향 2/3중 OR 합집합)",
            "selection": "train-only soft joint satisfaction penalty(학습 전용 연성 합동 충족 페널티)",
            "forbidden": "no F26 numeric gate relaxation, no validation selection, no ONNX/MT5 before handoff(F26 숫자 게이트 완화 없음, 검증 선택 없음, 인계 전 ONNX/MT5 없음)",
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
        "notes": "frontier27_stage_open_grok_accepted_soft_penalty_contract_no_authority",
        "run_number": RUN_NUMBER,
        "date": "2026-06-14",
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "claim_boundary": "stage_open_no_model_training_no_wfo_no_mt5_no_authority_goal_claim",
        "report_path": REPORT_PATH.as_posix(),
        "created_at_utc": summary["created_at_utc"],
        "primary_kpi": "not_applicable_stage_open(단계 개방에는 해당 없음)",
        "guardrail_kpi": "soft_penalty_lock_no_model_training_no_wfo_no_mt5_no_authority(연성 페널티 잠금, 모델학습/WFO/MT5/권위 없음)",
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
        "guardrail_kpi": "soft_penalty_lock_no_model_training_no_wfo_no_mt5_no_authority(연성 페널티 잠금, 모델학습/WFO/MT5/권위 없음)",
        "external_verification_status": "grok_stage_open_review_completed_runtime_probe_requires_handoff_candidate(그록 단계 개방 검토 완료, 런타임 탐침은 인계 후보 필요)",
        "notes": f"next={NEXT_RUN_ID};soft_penalty=true;no_authority",
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

Action(행동): Frontier27(전선27)을 soft joint satisfaction penalty before bridge union ONNX scout(합집합 전 연성 합동 충족 페널티 ONNX 탐색)로 열었습니다.

Effect(효과): F26(전선26)의 hard component gate(경성 구성 게이트) 붕괴를 단순 threshold relaxation(임계값 완화)으로 고치지 않고, full 80 micro source pool(전체 80 미세 원천 풀)을 train-only soft penalty rank(학습 전용 연성 페널티 순위)로 시험합니다.

Runtime/ONNX boundary(런타임/ONNX 경계): 각 stage(단계)마다 MT5 runtime probe(MT5 런타임 탐침) 상태를 기록하되, handoff candidate(인계 후보)가 나오기 전까지 실제 MT5(메타트레이더5), WFO(워크포워드 최적화), ONNX(온엑스)는 실행하지 않습니다.

Claim boundary(주장 경계): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def readme_text(summary: dict[str, Any]) -> str:
    return f"""# {STAGE_ID}

Purpose(목적): train-only soft joint satisfaction penalty before same-side OR-union(학습 전용 같은 방향 OR 합집합 전 연성 합동 충족 페널티)가 F26(전선26)의 hard gate collapse(경성 게이트 붕괴)를 반복 없이 넘을 수 있는지 봅니다.

Boundary(경계): scout-only(탐색 전용)입니다. completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 없습니다.

Current run(현재 실행): `{RUN_ID}`

Next run(다음 실행): `{NEXT_RUN_ID}`
"""


def stage_brief(summary: dict[str, Any]) -> str:
    return f"""# Frontier27 Stage Brief(전선27 단계 요약)

Opened(개방): {summary['created_at_utc']}

Frontier thesis(전선 가설): {summary['frontier_thesis']}

Hypothesis(가설): {summary['hypothesis']}

Novelty delta(신규성 차이): F27(전선27)은 F26(전선26)의 hard pass/fail gate(경성 통과/탈락 게이트)를 낮추지 않습니다. changed variable(변경 변수)은 soft penalty rank(연성 페널티 순위)입니다.

Runtime probe rule(런타임 탐침 규칙): 각 stage(단계)는 MT5 runtime probe(MT5 런타임 탐침) 상태를 기록합니다. 실제 probe(탐침)는 handoff_candidate_rows > 0(인계 후보 행 0 초과)일 때만 실행합니다.

Exit rule(종료 규칙): proxy(프록시), repair decision(수리 결정), closeout(마감)을 거쳐 completion candidate(완성 후보), preserved clue(보존 단서), negative memory(부정 기억), invalid setup(무효 설정), blocked(차단) 중 하나로 닫습니다.

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 not_claimed(주장 없음)입니다.
"""


def lock_spec() -> str:
    return (
        "# Frontier27 Soft Penalty Lock Spec(전선27 연성 페널티 잠금 명세)\n\n"
        "Locks(잠금):\n"
        f"{json.dumps(LOCKS, ensure_ascii=False, indent=2)}\n\n"
        "Criteria(기준):\n"
        f"{json.dumps(CRITERIA, ensure_ascii=False, indent=2)}\n"
    )


def do_not_repeat_text() -> str:
    return """# Frontier27 Do Not Repeat(전선27 반복 금지)

- Do not relax F26 hard gates as the primary path(F26 경성 게이트를 주 경로로 완화하지 않음).
- Do not reuse F25 DD-headroom-first rank(F25 손실폭 여유 우선 순위 재사용 금지).
- Do not reuse F24 density-first rank as primary(F24 빈도 우선 순위 주 경로 재사용 금지).
- Do not use validation/OOS in selection or repair(검증/OOS를 선택 또는 수리에 사용 금지).
- Do not export ONNX or run MT5 before handoff candidate(인계 후보 전 ONNX 내보내기 또는 MT5 실행 금지).
"""


def prior_stage_scan_text() -> str:
    return """# Frontier27 Prior Stage Scan(전선27 이전 단계 점검)

F26 invalid setup(전선26 무효 설정): `invalid_setup_joint_gate_left_three_passers_zero_valid_unions(무효 설정: 합동 게이트 통과 3개, 유효 합집합 0개)`.

F26 negative memory(전선26 부정 기억): `under_f26_locked_joint_micro_satisfaction_gate_collapsed_union_surface(F26 잠금 합동 미세 충족 게이트는 합집합 표면을 붕괴시킴)`.

Next clue(다음 단서): `soft_joint_satisfaction_penalty_instead_of_hard_component_gate_reference_only(경성 구성 게이트 대신 연성 합동 충족 페널티 참조 단서)`.

Reference boundary(참조 경계): F24/F25/F26(전선24/25/26)은 reference only(참조 전용)입니다. winner/baseline/promotion/runtime authority(승자/기준선/승격/런타임 권위)는 상속하지 않습니다.
"""


def experiment_design_text(summary: dict[str, Any]) -> str:
    return f"""# Frontier27 Experiment Design(전선27 실험 설계)

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
- evidence_plan(근거 계획): F27B run manifest(실행 목록), soft penalty audit(연성 페널티 감사), train-ranked union table(학습 순위 합집합 표), F24/F25/F26 top-10 non-repeat audit(상위 10 비반복 감사), split metrics(분할 지표), run registry(실행 등록부), stage ledger(단계 장부).
"""


def input_refs_text(summary: dict[str, Any]) -> str:
    return f"""# Frontier27 Input References(전선27 입력 참조)

- dataset(데이터셋): `{DATASET_PATH.as_posix()}`
- feature order(피처 순서): `{FEATURE_ORDER_PATH.as_posix()}`
- feature hash(피처 해시): `{summary['feature_order_hash']}`
- Grok packet(그록 묶음): `{GROK_PACKET.as_posix()}`
- F26 selection(전선26 선택): `{F26_SELECTION.as_posix()}`
- F26 invalid setup(전선26 무효 설정): `{F26_INVALID.as_posix()}`
- F26 closeout(전선26 마감): `{F26_CLOSEOUT.as_posix()}`
"""


def review_index() -> str:
    return f"""# Frontier27 Review Index(전선27 검토 색인)

- stage open report(단계 개방 보고서): `{REPORT_PATH.as_posix()}`
- Grok receipt(그록 영수증): `03_reviews/grok_stage_open_receipt.md`
- local verification(로컬 검증): `03_reviews/local_verification.md`
- gate audit(게이트 감사): `03_reviews/required_gate_coverage_audit.md`
"""


def grok_receipt_text(summary: dict[str, Any]) -> str:
    classification = summary["local_verification"]["grok_advice_classification"]
    return f"""# Frontier27 Grok Stage Open Receipt(전선27 그록 단계 개방 영수증)

Trigger reason(트리거 이유): stage open required by goal(목표가 단계 개방 검토를 요구).

Review size(검토 크기): small review(소규모 검토).

Direction before Grok(그록 전 방향): soft joint satisfaction penalty before bridge union scout(합집합 전 연성 합동 충족 페널티 탐색).

Prompt(프롬프트): `{summary['grok']['prompt']}`

Output(출력): `{summary['grok']['output']}`

Advice classification(조언 분류): `{summary['grok']['classification']}`.

Accepted advice(수용 조언): {', '.join(classification['accepted'])}

Needs local verification(로컬 검증 필요): {', '.join(classification['needs_local_verification'])}

Rejected advice(거절 조언): none(없음).

Local verification(로컬 검증): `{summary['local_verification']['judgment']}`

Final Codex direction(최종 Codex 방향): F27B(전선27B)는 full 80 micro pool(전체 80 미세 풀)과 written soft penalty contract(작성된 연성 페널티 계약)만 사용합니다.
"""


def local_verification_text(summary: dict[str, Any]) -> str:
    lines = ["# Frontier27 Local Verification(전선27 로컬 검증)", ""]
    for key, value in summary["local_verification"]["checks"].items():
        lines.append(f"- {key}: `{value}`")
    lines.append("")
    lines.append(f"Judgment(판정): `{summary['local_verification']['judgment']}`")
    lines.append("")
    lines.append("Effect(효과): Grok(그록) 조언을 자동 실행하지 않고 F26 closeout(전선26 마감), local files(로컬 파일), feature hash(피처 해시), and lock JSON(잠금 JSON)으로 재검증했습니다.")
    return "\n".join(lines) + "\n"


def gate_audit(summary: dict[str, Any]) -> str:
    return f"""# Frontier27 Required Gate Coverage Audit(전선27 필수 게이트 커버리지 감사)

- external_review_packet(외부 검토 묶음): covered by(충족) `{GROK_PACKET.as_posix()}`
- work_packet_schema_lint(작업 묶음 스키마 검사): experiment design fields(실험 설계 필드) materialized(물질화)
- local_verification_gate(로컬 검증 게이트): `{summary['local_verification']['judgment']}`
- soft_penalty_contract_gate(연성 페널티 계약 게이트): `soft_joint_satisfaction_penalty_rank` recorded(기록)
- non_repeat_gate(반복 방지 게이트): F27B must compare top10 keys against F24B, F25B, and F26B(F27B는 F24B/F25B/F26B 상위10 키 비교 필수)
- runtime_probe_gate(런타임 탐침 게이트): each stage records status(각 단계 상태 기록), execution requires handoff_candidate_rows > 0(실행은 인계 후보 필요)
- final_claim_guard(최종 주장 방어): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성) all not_claimed(모두 주장 없음)
"""


def report_text(summary: dict[str, Any]) -> str:
    return f"""# {RUN_ID} Report(보고서)

Status(상태): `{summary['status']}`

Judgment(판정): `{summary['judgment']}`

Hypothesis(가설): {summary['hypothesis']}

Grok(그록): `{summary['grok']['classification']}`

Local verification(로컬 검증): `{summary['local_verification']['judgment']}`

Next run(다음 실행): `{NEXT_RUN_ID}`

Runtime probe observation(런타임 탐침 관찰): stage-open only(단계 개방 전용). MT5 runtime probe(MT5 런타임 탐침)는 handoff candidate(인계 후보)가 없으므로 아직 실행하지 않습니다.

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 not_claimed(주장 없음)입니다.
"""


def selection_status(summary: dict[str, Any]) -> str:
    return f"""# Frontier27 Selection Status(전선27 선택 상태)

No selected baseline(선택 기준선 없음).

Stage-open only(단계 개방 전용)입니다. F27B(전선27B) proxy(프록시)가 아직 실행되지 않았습니다.

Next run(다음 실행): `{NEXT_RUN_ID}`

Runtime probe blocker(런타임 탐침 차단 사유): `runtime_probe_pending_no_handoff_candidate_at_stage_open(단계 개방 시점 인계 후보 없어 런타임 탐침 대기)`.

Claim boundary(주장 경계): no completion, no baseline, no promotion, no runtime authority, no live readiness, no Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음).
"""


def decision_text(summary: dict[str, Any]) -> str:
    return f"""# Decision(결정): Open Frontier27 Soft Penalty Scout(전선27 연성 페널티 탐색 개방)

Date(날짜): 2026-06-14

Decision(결정): Open(개방) `{STAGE_ID}` with run(실행) `{RUN_ID}`.

Reason(이유): F26(전선26) hard joint gate(경성 합동 게이트)가 union surface(합집합 표면)를 0개로 붕괴시켰고, Grok(그록)이 F27 soft penalty rank(연성 페널티 순위)를 acceptable new hypothesis(허용 가능한 새 가설)로 분류했습니다.

Effect(효과): 다음 proxy(프록시)는 F26 gate relaxation(F26 게이트 완화)이 아니라 train-only soft penalty mechanism(학습 전용 연성 페널티 메커니즘)을 검증합니다.

Claim boundary(주장 경계): no authority(권위 없음), no baseline(기준선 없음), no completion(완성 없음).
"""


def changelog_entry(summary: dict[str, Any]) -> str:
    return (
        f"- `{RUN_ID}`: opened Frontier27 soft joint satisfaction penalty scout(전선27 연성 합동 충족 페널티 탐색 개방). "
        "Effect(효과): F26 hard-gate collapse(F26 경성 게이트 붕괴)를 reference-only clue(참조 전용 단서)로 전환하고 F27B proxy(프록시)를 준비합니다.\n"
    )


def idea_registry_entry(summary: dict[str, Any]) -> str:
    return (
        f"- `IDEA-FR27-SOFT-JOINT-SATISFACTION-PENALTY-BRIDGE-UNION-ONNX-SCOUT`: `{RUN_ID}` opens soft joint satisfaction penalty before union scout(합집합 전 연성 합동 충족 페널티 탐색). "
        "Effect(효과): F26 threshold relaxation(F26 임계값 완화) 반복 대신 full 80 micro penalty rank(전체 80 미세 페널티 순위)를 시험합니다.\n"
    )


def artifact_identity(path: Path) -> dict[str, str]:
    actual = io_path(path)
    if not actual.exists():
        return {"path": path.as_posix(), "exists": "false", "sha256": ""}
    digest = hashlib.sha256(actual.read_bytes()).hexdigest()
    return {"path": path.as_posix(), "exists": "true", "sha256": digest}


def write_json(path: Path, payload: Any) -> None:
    io_path(path).parent.mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def read_text(path: Path) -> str:
    return io_path(path).read_text(encoding="utf-8-sig")


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


if __name__ == "__main__":
    raise SystemExit(main())
