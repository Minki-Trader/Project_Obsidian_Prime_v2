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


STAGE_ID = "stage_frontier_22__session_return_shock_pf_source_onnx_scout"
RUN_ID = "frontier22A_stage_open_new_pf_edge_source_hypothesis_design_v1"
RUN_NUMBER = "frontier22A"
PARENT_RUN_ID = "frontier21D_lifecycle_repair_or_closeout_decision_v1"
NEXT_RUN_ID = "frontier22B_session_return_shock_pf_source_proxy_scout_v1"
STATUS = "opened_frontier22_session_return_shock_pf_source_no_authority"
JUDGMENT = "stage_opened_after_grok_adjusted_shock_cross_family_contract"

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REPORT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_report.md"
SCRIPT_PATH = Path("stage_pipelines/stage_frontier_22/materialize_frontier22a_stage_open.py")
GROK_PACKET = Path("docs/agent_control/grok_reviews/2026-06-14_frontier22_stage_open/small_review")

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
DECISION_PATH = Path("docs/decisions/2026-06-14_stage_frontier_22_session_return_shock_pf_source_onnx_scout_open.md")

F20_SELECTION = Path("stages/stage_frontier_20__train_only_feature_state_rule_atlas_onnx_scout/04_selected/selection_status.md")
F20_NEGATIVE = Path("stages/stage_frontier_20__train_only_feature_state_rule_atlas_onnx_scout/04_selected/negative_memory.md")
F21_SELECTION = Path("stages/stage_frontier_21__f20_seed_lifecycle_dd_containment_onnx_scout/04_selected/selection_status.md")
F21_CLOSEOUT = Path(
    "stages/stage_frontier_21__f20_seed_lifecycle_dd_containment_onnx_scout/"
    "03_reviews/frontier21D_lifecycle_repair_or_closeout_decision_v1_report.md"
)

BUCKETS = {
    "shock": [
        "return_zscore_20",
        "log_return_1",
        "return_1_over_atr_14",
        "gap_percent",
        "close_prev_close_ratio",
    ],
    "volatility": [
        "atr_14_over_atr_50",
        "historical_vol_5_over_20",
        "vix_zscore_20",
        "hl_zscore_50",
    ],
    "trend_chop": [
        "adx_14",
        "ema20_ema50_diff",
        "ema20_ema50_spread_zscore_50",
        "bb_squeeze",
    ],
    "session_age": [
        "minutes_from_cash_open",
        "is_first_30m_after_open",
        "is_last_30m_before_cash_close",
        "is_us_cash_open",
    ],
    "breadth": [
        "mega8_pos_breadth_1",
        "mega8_dispersion_5",
        "us100_minus_mega8_equal_return_1",
        "us100_minus_top3_weighted_return_1",
    ],
}

LOCKS = {
    "novelty_delta": "shock-anchored cross-family entry states(충격 고정 교차군 진입 상태)",
    "mandatory_rule_shape": "one shock condition plus one non-shock context condition(충격 조건 1개와 비충격 문맥 조건 1개)",
    "search_cap": "family_condition_cap<=8, pair_depth=2, max_candidates<=200(군별 조건 8개 이하, 깊이 2, 후보 200개 이하)",
    "side_hypothesis": "two locked lanes: shock_continuation and shock_fade(고정 2개 방향: 충격 지속과 충격 되돌림)",
    "exit_proxy": "future_log_return_12 minus rough proxy cost only(12봉 미래 수익률에서 거친 비용만 차감)",
    "f20_duplicate_guard": "F20 vix_zscore_20+close_ema50_ratio duplicate cannot be scout clue(F20 중복은 탐색 단서 금지)",
    "f21_guard": "no lifecycle repair in first proxy(F22B 첫 프록시에는 생명주기 수리 금지)",
}


def main() -> int:
    ensure_dirs()
    normalize_grok_markdown()
    now = utc_now()
    feature_order = read_feature_order()
    grok = read_grok_packet()
    local = local_verification(feature_order, grok)
    summary = build_summary(now, feature_order, grok, local)
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
    return [line.strip() for line in io_path(FEATURE_ORDER_PATH).read_text(encoding="utf-8-sig").splitlines() if line.strip()]


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
        "output_excerpt": output[:2200],
    }


def classify_grok(text: str) -> str:
    lowered = text.lower()
    if "decision" in lowered and "adjust" in lowered:
        return "accepted_with_adjustments(조정 수용)"
    if "decision" in lowered and "accept" in lowered:
        return "accepted(수용)"
    if "decision" in lowered and "reject" in lowered:
        return "rejected(거절)"
    return "classification_missing(분류 누락)"


def local_verification(feature_order: list[str], grok: dict[str, Any]) -> dict[str, Any]:
    workspace = read_text(WORKSPACE_STATE)
    f20_selection = read_text(F20_SELECTION)
    f20_negative = read_text(F20_NEGATIVE)
    f21_selection = read_text(F21_SELECTION)
    f21_closeout = read_text(F21_CLOSEOUT)
    feature_hash = ordered_hash(feature_order)
    feature_set = set(feature_order)
    bucket_features = {feature for features in BUCKETS.values() for feature in features}
    checks = {
        "workspace_current_stage_frontier21_closed": "current_stage_id: stage_frontier_21__f20_seed_lifecycle_dd_containment_onnx_scout" in workspace
        and "current_status: closed_preserved_clue_negative_memory_lifecycle_low_dd_density_no_pf_edge_no_handoff" in workspace,
        "workspace_next_run_frontier22a": f"next_run_id: {RUN_ID}" in workspace,
        "f20_negative_memory_present": "train_only_depth2_rule_atlas" in f20_negative,
        "f20_no_authority_present": "no selected baseline" in f20_selection.lower(),
        "f21_negative_memory_present": "lifecycle_dd_density_repair_alone" in f21_selection or "lifecycle_dd_density_repair_alone" in f21_closeout,
        "feature_hash_matches_contract": feature_hash == EXPECTED_FEATURE_HASH,
        "feature_count_is_58": len(feature_order) == 58,
        "bucket_features_exist": bucket_features.issubset(feature_set),
        "dataset_exists": path_exists(DATASET_PATH),
        "grok_transport_success": grok["success"] and grok["returncode"] == 0 and not grok["timed_out"],
        "grok_adjustment_accepted": grok["classification"] == "accepted_with_adjustments(조정 수용)",
        "no_unexpected_top_level_artifacts": not grok["unexpected_top_level_artifacts"],
    }
    return {
        "judgment": "pass_open_ready_with_adjusted_locks(조정 잠금 반영 후 개방 가능)" if all(checks.values()) else "needs_manual_review(수동 검토 필요)",
        "checks": checks,
        "feature_order_hash": feature_hash,
        "feature_count": len(feature_order),
    }


def build_summary(now: str, feature_order: list[str], grok: dict[str, Any], local: dict[str, Any]) -> dict[str, Any]:
    return {
        "created_at_utc": now,
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
            "obsidian-claim-discipline(주장 규율)",
        ],
        "frontier_thesis": (
            "A new PF edge source(새 수익 팩터 우위 원천) may exist in shock-anchored cross-family "
            "entry states(충격 고정 교차군 진입 상태), not in more lifecycle repair(추가 생명주기 수리)."
        ),
        "hypothesis": (
            "US100 M5 return shock(수익률 충격) combined with exactly one context family(문맥군) "
            "can isolate favorable payoff asymmetry(유리한 보상 비대칭) before any lifecycle repair(생명주기 수리 전)."
        ),
        "decision_use": "Open F22B proxy scout(F22B 프록시 탐색)를 shock+context locked rule shape(충격+문맥 잠금 규칙 형태)로 실행합니다.",
        "comparison_baseline": "F20/F21 are reference-only(참조 전용) and no selected baseline(선택 기준선 없음).",
        "control_variables": [
            "feature_set_v2 fixed 58 features(고정 58개 피처)",
            "future_log_return_12 fixed proxy(고정 12봉 미래 수익률 프록시)",
            "train-only thresholds(학습 전용 임계값)",
            "validation/OOS read-only diagnostics(검증/표본외 읽기 전용 진단)",
        ],
        "changed_variables": [
            "shock feature family(충격 피처군)",
            "one context condition(문맥 조건 1개)",
            "locked shock continuation/fade lane(고정 충격 지속/되돌림 방향)",
        ],
        "sample_scope": "Tier A separate only(티어 A 분리 전용); Tier B missing_required(티어 B 필수 누락); Tier A+B out_of_scope_by_claim(티어 A+B 주장 범위 밖).",
        "success_criteria": {
            "scout_clue": "shock present, not F20 duplicate, validation/OOS net positive, PF>=1.05, density 3-12/day(충격 포함, F20 중복 아님, 검증/표본외 양수)",
            "seed_surface": "PF>=1.2 both, density 5-10/day, DD<=25%(양쪽 수익 팩터 1.2 이상, 빈도 5-10, 손실폭 25% 이하)",
            "handoff_candidate": "PF>=1.5 both, density 5-10/day, DD<=15%, smoothness pass, then Grok before MT5/ONNX(양쪽 수익 팩터 1.5 이상 뒤 비싼 검증 전 그록)",
        },
        "failure_criteria": [
            "best rule is F20 duplicate pressure(F20 중복 압력)",
            "no validation/OOS positive PF clue(검증/표본외 양수 수익 팩터 단서 없음)",
            "density/PF/DD cannot coexist(빈도/수익 팩터/손실폭 공존 실패)",
        ],
        "invalid_conditions": [
            "candidate without shock feature(충격 피처 없는 후보)",
            "candidate with more than one context condition(문맥 조건 1개 초과 후보)",
            "validation/OOS threshold selection(검증/표본외 임계값 선택)",
            "lifecycle repair inside F22B(F22B 안 생명주기 수리)",
        ],
        "stop_conditions": [
            "max candidate cap reached(후보 상한 도달)",
            "handoff-like candidate appears and pre-expensive Grok is required(인계형 후보 발생 후 비싼 검증 전 그록 필요)",
            "no scout/seed clue after capped proxy(상한 프록시 뒤 단서 없음)",
        ],
        "evidence_plan": [
            "stage_open_summary.json(단계 개방 요약)",
            "shock_pf_source_lock.json(충격 수익 팩터 원천 잠금)",
            "condition_pool.csv(조건 풀)",
            "candidate_summary.csv(후보 요약)",
            "proxy_metrics_by_split.csv(분할별 프록시 지표)",
            "stage_run_ledger.csv(단계 실행 장부)",
        ],
        "buckets": BUCKETS,
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
    write_json(RUN_ROOT / "shock_pf_source_lock.json", {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "buckets": BUCKETS,
        "locks": LOCKS,
        "search_caps": {"family_condition_cap": 8, "pair_depth": 2, "max_candidates": 200},
        "side_lanes": ["shock_continuation(충격 지속)", "shock_fade(충격 되돌림)"],
        "claim_boundary": summary["claim_boundary"],
    })
    write_json(RUN_ROOT / "grok_receipt.json", grok_receipt(summary))
    f03b.write_text_sig(STAGE_ROOT / "README.md", readme_text(summary))
    f03b.write_text_sig(STAGE_ROOT / "00_spec" / "stage_brief.md", stage_brief(summary))
    f03b.write_text_sig(STAGE_ROOT / "00_spec" / "shock_pf_source_lock_spec.md", lock_spec(summary))
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
        "data_snapshot": {
            "dataset_path": DATASET_PATH.as_posix(),
            "split_names": ["train", "validation", "oos"],
        },
        "rule_stack": {"entry": LOCKS, "buckets": BUCKETS},
        "compatibility": {"schema_version": "frontier22a_stage_open_v1", "mismatch_policy": "fail_fast(빠른 실패)"},
        "claim_boundary": summary["claim_boundary"],
    }


def grok_receipt(summary: dict[str, Any]) -> dict[str, Any]:
    return {
        "trigger_reason": "stage_open_required_by_goal(목표상 단계 개방 그록 검토 필요)",
        "review_size": "small(소규모)",
        "direction_before_grok": "open F22 PF source scout(전선22 수익 팩터 원천 탐색 개방)",
        "bounded_evidence": [F20_SELECTION.as_posix(), F20_NEGATIVE.as_posix(), F21_SELECTION.as_posix(), F21_CLOSEOUT.as_posix()],
        "prompt_identity": {"path": summary["grok"]["prompt"], "hash": summary["grok"]["prompt_hash"]},
        "grok_output_identity": {"path": summary["grok"]["output"], "classification": summary["grok"]["classification"]},
        "advice_classification": "accepted_with_adjustments(조정 수용)",
        "local_verification": summary["local_verification"],
        "forbidden_claim_check": summary["claim_boundary"],
        "final_codex_direction": "apply shock-anchored cross-family contract and F20 duplicate guard(충격 고정 교차군 계약과 F20 중복 가드 반영)",
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
        "notes": "frontier22_stage_open_grok_adjusted_shock_cross_family_contract_no_authority",
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
        "guardrail_kpi": "shock_cross_family_lock_no_model_training_no_wfo_no_mt5_no_authority(충격 교차군 잠금, 모델학습/WFO/MT5/권위 없음)",
        "external_verification_status": "grok_stage_open_review_completed_runtime_probe_requires_handoff_candidate(그록 단계 개방 검토 완료, 런타임 탐침은 인계 후보 필요)",
        "notes": f"next={NEXT_RUN_ID};shock_required=true;max_candidates=200;no_authority",
        "question": "Can shock-anchored cross-family entry states create PF edge?(충격 고정 교차군 진입 상태가 수익 팩터 우위를 만들 수 있는가?)",
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

Action(행동): Frontier22(전선22)를 session return shock PF source scout(세션 수익률 충격 수익 팩터 원천 탐색)로 열었습니다.

Effect(효과): F21 lifecycle repair(전선21 생명주기 수리)를 반복하지 않고, shock feature(충격 피처)와 one context family(문맥군 1개)가 PF edge(수익 팩터 우위)를 만드는지 먼저 봅니다.

Claim boundary(주장 경계): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def readme_text(summary: dict[str, Any]) -> str:
    return f"""# {STAGE_ID}

Purpose(목적): shock-anchored cross-family entry states(충격 고정 교차군 진입 상태)가 PF edge(수익 팩터 우위)를 만들 수 있는지 봅니다.

Boundary(경계): scout-only(탐색 전용)입니다. completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 없습니다.

Current run(현재 실행): `{RUN_ID}`

Next run(다음 실행): `{NEXT_RUN_ID}`
"""


def stage_brief(summary: dict[str, Any]) -> str:
    return f"""# Frontier22 Stage Brief(전선22 단계 요약)

Opened(개방): {summary['created_at_utc']}

Frontier thesis(전선 가설): {summary['frontier_thesis']}

Hypothesis(가설): {summary['hypothesis']}

Novelty delta(신규성 차이): F20(전선20)의 global 58-feature rule atlas(전체 58피처 규칙 지도)를 반복하지 않습니다. 모든 후보는 shock feature(충격 피처) 1개와 context family(문맥군) 1개를 함께 가져야 합니다. F21(전선21)의 lifecycle/density repair(생명주기/빈도 수리)는 첫 프록시에 쓰지 않습니다.

Exit rule(종료 규칙): proxy/repaired evidence(프록시/수리 근거)를 보고 completion candidate(완성 후보), preserved clue(보존 단서), negative memory(부정 기억), invalid setup(무효 설정), blocked(차단) 중 하나로 닫습니다.

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 not_claimed(주장 없음)입니다.
"""


def lock_spec(summary: dict[str, Any]) -> str:
    lines = ["# Frontier22 Shock PF Source Lock Spec(전선22 충격 수익 팩터 원천 잠금 명세)", ""]
    lines.append("Locks(잠금):")
    lines.extend(f"- {key}: {value}" for key, value in LOCKS.items())
    lines.append("")
    lines.append("Buckets(버킷):")
    for bucket, features in BUCKETS.items():
        lines.append(f"- {bucket}: `{', '.join(features)}`")
    lines.append("")
    return "\n".join(lines)


def do_not_repeat_text() -> str:
    return """# Frontier22 Do Not Repeat(전선22 반복 금지)

- Do not rerun F20 global depth-2 rule atlas(F20 전체 깊이2 규칙 지도 재실행 금지).
- Do not claim a rule without shock feature as scout clue(충격 피처 없는 규칙을 탐색 단서로 주장 금지).
- Do not use F21 lifecycle/density repair in F22B(F22B에서 F21 생명주기/빈도 수리 금지).
- Do not use validation/OOS to pick thresholds(검증/표본외로 임계값 선택 금지).
- Do not treat ONNX/MT5 as eligible before a handoff candidate exists(인계 후보 전 ONNX/MT5 적격 주장 금지).
"""


def experiment_design_text(summary: dict[str, Any]) -> str:
    return f"""# Frontier22 Experiment Design(전선22 실험 설계)

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
- evidence_plan(근거 계획): {', '.join(summary['evidence_plan'])}
"""


def prior_stage_scan_text() -> str:
    return """# Frontier22 Prior Stage Scan(전선22 이전 단계 점검)

F20 preserved clue(전선20 보존 단서): low-VIX momentum/price-position long surface(낮은 VIX 모멘텀/가격 위치 롱 표면)는 reference-only(참조 전용)입니다.

F20 negative memory(전선20 부정 기억): train-only depth-2 rule atlas(학습 전용 깊이2 규칙 지도) 단독은 DD(손실폭)나 handoff(인계)를 만들지 못했습니다.

F21 negative memory(전선21 부정 기억): lifecycle DD/density repair(생명주기 손실폭/빈도 수리) 단독은 PF edge(수익 팩터 우위)를 만들지 못했습니다.

Reference boundary(참조 경계): Stage12~364(12~364단계), F20(전선20), F21(전선21)은 reference only(참조 전용)이며 winner/baseline/promotion/runtime authority(승자/기준선/승격/런타임 권위)는 상속하지 않습니다.
"""


def input_refs_text(summary: dict[str, Any]) -> str:
    return f"""# Frontier22 Input References(전선22 입력 참조)

- dataset(데이터셋): `{DATASET_PATH.as_posix()}`
- feature order(피처 순서): `{FEATURE_ORDER_PATH.as_posix()}`
- feature hash(피처 해시): `{summary['feature_order_hash']}`
- Grok packet(그록 묶음): `{GROK_PACKET.as_posix()}`
"""


def review_index() -> str:
    return f"""# Frontier22 Review Index(전선22 검토 색인)

- stage open report(단계 개방 보고서): `{REPORT_PATH.as_posix()}`
- Grok receipt(그록 영수증): `03_reviews/grok_stage_open_receipt.md`
- local verification(로컬 검증): `03_reviews/local_verification.md`
- gate audit(게이트 감사): `03_reviews/required_gate_coverage_audit.md`
"""


def grok_receipt_text(summary: dict[str, Any]) -> str:
    return f"""# Frontier22 Grok Stage Open Receipt(전선22 그록 단계 개방 영수증)

Trigger reason(트리거 이유): stage open required by goal(목표가 요구한 단계 개방 검토).

Review size(검토 크기): small review(소규모 검토).

Direction before Grok(그록 전 방향): shock/context PF source scout(충격/문맥 수익 팩터 원천 탐색).

Prompt(프롬프트): `{summary['grok']['prompt']}`

Output(출력): `{summary['grok']['output']}`

Advice classification(조언 분류): `{summary['grok']['classification']}`; Codex accepted adjustments locally(코덱스가 조정을 로컬 검증 후 수용).

Local verification(로컬 검증): `{summary['local_verification']['judgment']}`

Final Codex direction(최종 코덱스 방향): shock-anchored cross-family contract(충격 고정 교차군 계약), F20 duplicate guard(F20 중복 가드), search cap(탐색 상한)을 적용합니다.
"""


def local_verification_text(summary: dict[str, Any]) -> str:
    lines = ["# Frontier22 Local Verification(전선22 로컬 검증)", ""]
    for key, value in summary["local_verification"]["checks"].items():
        lines.append(f"- {key}: `{value}`")
    lines.append("")
    lines.append(f"Judgment(판정): `{summary['local_verification']['judgment']}`")
    return "\n".join(lines) + "\n"


def gate_audit(summary: dict[str, Any]) -> str:
    return f"""# Frontier22 Required Gate Coverage Audit(전선22 필수 게이트 커버리지 감사)

- external_review_packet(외부 검토 묶음): covered by(충족) `{GROK_PACKET.as_posix()}`
- kpi_contract_audit(KPI 계약 감사): planned for(계획됨) `{NEXT_RUN_ID}`
- required_gate_coverage_audit(필수 게이트 커버리지 감사): this file(이 파일)
- final_claim_guard(최종 주장 방지): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성) all not_claimed(모두 주장 없음)
"""


def report_text(summary: dict[str, Any]) -> str:
    return f"""# Frontier22A Stage Open Report(전선22A 단계 개방 보고서)

Updated(갱신): {summary['created_at_utc']}

Status(상태): `{summary['status']}`

Judgment(판정): `{summary['judgment']}`

Action(행동): Frontier22(전선22)를 session return shock PF source scout(세션 수익률 충격 수익 팩터 원천 탐색)로 열었습니다.

Effect(효과): F20 전체 규칙 지도와 F21 생명주기 수리를 반복하지 않고, shock feature(충격 피처)가 포함된 교차군 진입 상태만 시험합니다.

Grok classification(그록 분류): `{summary['grok']['classification']}`

Local verification(로컬 검증): `{summary['local_verification']['judgment']}`

Next action(다음 행동): `{NEXT_RUN_ID}`

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def selection_status(summary: dict[str, Any]) -> str:
    return f"""# Frontier22 Selection Status(전선22 선택 상태)

Updated(갱신): {summary['created_at_utc']}

Selection(선택): no selected baseline/completion candidate/promotion/runtime authority(선택 기준선/완성 후보/승격/런타임 권위 없음).

Status(상태): `{summary['status']}`

Next action(다음 행동): `{NEXT_RUN_ID}`
"""


def decision_text(summary: dict[str, Any]) -> str:
    return f"""# Decision: Open Frontier22 Session Return Shock PF Source ONNX Scout(결정: 전선22 세션 수익률 충격 수익 팩터 원천 ONNX 탐색 개방)

Date(날짜): {summary['created_at_utc']}

Decision(결정): `{summary['status']}`

Action(행동): F22(전선22)를 shock-anchored cross-family PF source scout(충격 고정 교차군 수익 팩터 원천 탐색)로 열었습니다.

Effect(효과): 다음 proxy(프록시)는 shock feature(충격 피처) 1개와 context family(문맥군) 1개를 반드시 포함하므로 F20 재탐색 압력을 줄입니다.

Next action(다음 행동): `{NEXT_RUN_ID}`
"""


def changelog_entry(summary: dict[str, Any]) -> str:
    return (
        f"- {summary['created_at_utc']}: `{RUN_ID}` opened Frontier22(전선22) after Grok adjusted review(그록 조정 검토). "
        f"Effect(효과): next run(다음 실행) `{NEXT_RUN_ID}` is locked to shock+context PF source scout(충격+문맥 수익 팩터 원천 탐색).\n"
    )


def idea_registry_entry(summary: dict[str, Any]) -> str:
    return (
        f"- `IDEA-FR22-SESSION-RETURN-SHOCK-PF-SOURCE-ONNX-SCOUT`: `{RUN_ID}` opens shock-anchored cross-family PF source scout(충격 고정 교차군 수익 팩터 원천 탐색). "
        "Effect(효과): F21의 생명주기 수리 반복을 멈추고 PF edge(수익 팩터 우위) 원천을 진입 상태에서 찾습니다.\n"
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
