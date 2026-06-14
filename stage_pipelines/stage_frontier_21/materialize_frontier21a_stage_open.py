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


STAGE_ID = "stage_frontier_21__f20_seed_lifecycle_dd_containment_onnx_scout"
RUN_ID = "frontier21A_stage_open_f20_seed_lifecycle_dd_containment_onnx_scout_v1"
RUN_NUMBER = "frontier21A"
PARENT_RUN_ID = "frontier20C_rule_atlas_repair_or_closeout_decision_v1"
NEXT_RUN_ID = "frontier21B_f20_seed_lifecycle_proxy_scout_v1"
STATUS = "opened_frontier21_f20_seed_lifecycle_dd_containment_no_authority"
JUDGMENT = "stage_opened_after_grok_adjusted_review_with_entry_lock_and_lifecycle_dd_contract"

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REPORT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_report.md"
DECISION_PATH = Path("docs/decisions/2026-06-14_stage_frontier_21_f20_seed_lifecycle_dd_containment_onnx_scout_open.md")
SCRIPT_PATH = Path("stage_pipelines/stage_frontier_21/materialize_frontier21a_stage_open.py")

GROK_PACKET = Path("docs/agent_control/grok_reviews/2026-06-14_frontier21_stage_open/small_review")
F20_STAGE = Path("stages/stage_frontier_20__train_only_feature_state_rule_atlas_onnx_scout")
F20_SELECTION = F20_STAGE / "04_selected" / "selection_status.md"
F20_PRESERVED = F20_STAGE / "04_selected" / "preserved_clue.md"
F20_NEGATIVE = F20_STAGE / "04_selected" / "negative_memory.md"
F20_SUMMARY = F20_STAGE / "02_runs/frontier20B_feature_state_rule_atlas_proxy_scout_v1/final_summary.json"
F18_SELECTION = Path("stages/stage_frontier_18__asymmetric_exit_lifecycle_profit_lock_onnx_scout/04_selected/selection_status.md")
F18_NEGATIVE_REPORT = Path(
    "stages/stage_frontier_18__asymmetric_exit_lifecycle_profit_lock_onnx_scout/"
    "03_reviews/frontier18C_asymmetric_exit_lifecycle_repair_or_closeout_decision_v1_report.md"
)

DATASET_PATH = Path(
    "data/processed/model_inputs/"
    "label_v1_fwd12_split_v1_feature_set_v2_mt5_price_proxy_58/"
    "model_input_dataset.parquet"
)
FEATURE_ORDER_PATH = DATASET_PATH.with_name("model_input_feature_order.txt")
EXPECTED_FEATURE_HASH = "fa06973c24462298ea38d84528b07ca0adf357e506f3bfeea02eb0d5691ab8e2"

RUN_REGISTRY = Path("docs/registers/run_registry.csv")
ALPHA_LEDGER = Path("docs/registers/alpha_run_ledger.csv")
IDEA_REGISTRY = Path("docs/registers/idea_registry.md")
CHANGELOG = Path("docs/workspace/changelog.md")
WORKSPACE_STATE = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE = Path("docs/context/current_working_state.md")

ENTRY_LOCK = {
    "rule_id": "f20_fixed_low_vix_price_position_long",
    "side": "long(롱)",
    "definition": "vix_zscore_20 <= q30 & close_ema50_ratio >= q70",
    "source_boundary": "F20 preserved clue only(F20 보존 단서 전용)",
    "selection_boundary": "fixed_before_f21_no_validation_oos_reselection(F21 전 고정, 검증/표본외 재선택 없음)",
}

LIFECYCLE_GRID = (
    {
        "profile_id": "f21b_sim_baseline_hold12_no_stop",
        "role": "parity_baseline_row(동등성 비교 행)",
        "max_hold_bars": 12,
        "atr_stop_multiplier": 0.0,
        "atr_take_profit_multiplier": 0.0,
        "cooldown_bars": 0,
        "early_adverse_exit_enabled": False,
    },
    {
        "profile_id": "f21b_hold4_atr0p8_tp1p6_cd2_early",
        "role": "dd_containment_profile(손실폭 억제 프로필)",
        "max_hold_bars": 4,
        "atr_stop_multiplier": 0.8,
        "atr_take_profit_multiplier": 1.6,
        "cooldown_bars": 2,
        "early_adverse_exit_enabled": True,
    },
    {
        "profile_id": "f21b_hold6_atr1p0_tp2p0_cd3",
        "role": "balanced_profile(균형 프로필)",
        "max_hold_bars": 6,
        "atr_stop_multiplier": 1.0,
        "atr_take_profit_multiplier": 2.0,
        "cooldown_bars": 3,
        "early_adverse_exit_enabled": False,
    },
    {
        "profile_id": "f21b_hold8_atr1p2_tp2p4_cd4_early",
        "role": "wide_profile_with_early_exit(넓은 프로필+초기 청산)",
        "max_hold_bars": 8,
        "atr_stop_multiplier": 1.2,
        "atr_take_profit_multiplier": 2.4,
        "cooldown_bars": 4,
        "early_adverse_exit_enabled": True,
    },
    {
        "profile_id": "f21b_hold10_atr1p5_tp3p0_cd6",
        "role": "loose_profile(느슨한 프로필)",
        "max_hold_bars": 10,
        "atr_stop_multiplier": 1.5,
        "atr_take_profit_multiplier": 3.0,
        "cooldown_bars": 6,
        "early_adverse_exit_enabled": False,
    },
)

LOCKS = (
    "F20 entry surface is fixed(F20 진입 표면 고정)",
    "No new rule-atlas rerank(새 규칙 지도 재순위 없음)",
    "No side flip(방향 전환 없음)",
    "No boosted backbone(부스팅 백본 없음)",
    "No probability threshold search(확률 임계값 탐색 없음)",
    "No new feature engineering(새 피처 설계 없음)",
    "Lifecycle grid is capped and pre-registered(생명주기 격자는 상한 있고 사전 등록됨)",
    "Validation/OOS are read-only diagnostics(검증/표본외는 읽기 전용 진단)",
    "Pre-expensive Grok review before any MT5/runtime work(비싼 MT5/런타임 전 그록 검토)",
)


def main() -> int:
    ensure_dirs()
    normalize_grok_markdown()
    now = utc_now()
    feature_order = read_feature_order()
    grok = read_grok_packet(GROK_PACKET)
    f20 = read_f20_context()
    local = local_verification(feature_order, grok, f20)
    summary = build_summary(now, feature_order, grok, f20, local)
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
        "entry_lock": ENTRY_LOCK["definition"],
        "profile_count": len(LIFECYCLE_GRID),
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


def normalize_grok_markdown() -> None:
    for name in ("prompt.md", "clean_output.md"):
        path = GROK_PACKET / name
        if path_exists(path):
            text = io_path(path).read_text(encoding="utf-8-sig")
            f03b.write_text_sig(path, text.rstrip() + "\n")


def read_grok_packet(packet: Path) -> dict[str, Any]:
    metadata = read_json(packet / "metadata.json")
    output = read_text(packet / "clean_output.md")
    return {
        "packet": packet.as_posix(),
        "prompt": (packet / "prompt.md").as_posix(),
        "output": (packet / "clean_output.md").as_posix(),
        "metadata": (packet / "metadata.json").as_posix(),
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
    if "decision" in lowered and "adjust" in lowered:
        return "accepted_with_adjustments(조정 수용)"
    if "decision" in lowered and "accept" in lowered:
        return "accepted(수용)"
    if "decision" in lowered and "reject" in lowered:
        return "rejected(거절)"
    return "classification_missing(분류 누락)"


def read_f20_context() -> dict[str, Any]:
    summary = read_json(F20_SUMMARY)
    best = summary.get("best_candidate", {})
    return {
        "selection_text": read_text(F20_SELECTION),
        "preserved_text": read_text(F20_PRESERVED),
        "negative_text": read_text(F20_NEGATIVE),
        "summary_path": F20_SUMMARY.as_posix(),
        "best_candidate_id": best.get("candidate_id", ""),
        "best_rule": best.get("rule_definition", ""),
        "best_side": best.get("side", ""),
        "validation_profit_factor": best.get("validation_profit_factor"),
        "validation_trades_per_day": best.get("validation_trades_per_day"),
        "validation_dd_risk": best.get("validation_dd_risk"),
        "oos_profit_factor": best.get("oos_profit_factor"),
        "oos_trades_per_day": best.get("oos_trades_per_day"),
        "oos_dd_risk": best.get("oos_dd_risk"),
    }


def local_verification(feature_order: list[str], grok: dict[str, Any], f20: dict[str, Any]) -> dict[str, Any]:
    workspace = read_text(WORKSPACE_STATE)
    f18_selection = read_text(F18_SELECTION)
    f18_negative = read_text(F18_NEGATIVE_REPORT)
    feature_hash = ordered_hash(feature_order)
    checks = {
        "workspace_current_stage_frontier20_closed": "current_stage_id: stage_frontier_20__train_only_feature_state_rule_atlas_onnx_scout" in workspace
        and "current_status: closed_preserved_clue_negative_memory_rule_atlas_seed_surface_no_handoff_no_authority" in workspace,
        "workspace_next_run_frontier21a": "next_run_id: frontier21A_stage_open_new_hypothesis_design_v1" in workspace,
        "f20_best_rule_matches_entry_lock": str(f20["best_rule"]) == ENTRY_LOCK["definition"],
        "f20_best_side_long": "long" in str(f20["best_side"]).lower() or "롱" in str(f20["best_side"]),
        "f20_preserved_clue_present": "low_vix_momentum" in f20["preserved_text"],
        "f20_negative_memory_present": "train_only_depth2_rule_atlas" in f20["negative_text"],
        "f18_negative_memory_present": "negative_memory" in f18_selection.lower() and "asymmetric_exit_lifecycle" in f18_negative,
        "feature_order_hash_matches_contract": feature_hash == EXPECTED_FEATURE_HASH,
        "feature_count_is_58": len(feature_order) == 58,
        "dataset_exists": path_exists(DATASET_PATH),
        "grok_transport_success": grok["success"] and not grok["timed_out"] and grok["returncode"] == 0,
        "grok_adjustment_accepted_locally": grok["classification"] == "accepted_with_adjustments(조정 수용)",
        "grok_no_unexpected_top_level_artifacts": not grok["unexpected_top_level_artifacts"],
        "lifecycle_profile_cap_is_five": len(LIFECYCLE_GRID) == 5,
        "parity_baseline_row_registered": LIFECYCLE_GRID[0]["role"].startswith("parity_baseline_row"),
    }
    return {
        "judgment": "pass_open_ready_with_adjustments(조정 반영 후 개방 준비 통과)" if all(checks.values()) else "needs_manual_review(수동 검토 필요)",
        "checks": checks,
        "feature_order_hash": feature_hash,
        "feature_count": len(feature_order),
    }


def build_summary(now: str, feature_order: list[str], grok: dict[str, Any], f20: dict[str, Any], local: dict[str, Any]) -> dict[str, Any]:
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
            "obsidian-result-judgment(결과 판정)",
            "obsidian-claim-discipline(주장 규율)",
        ],
        "required_gates": [
            "external_review_packet(외부 검토 묶음)",
            "kpi_contract_audit(KPI 계약 감사)",
            "required_gate_coverage_audit(필수 게이트 커버리지 감사)",
            "final_claim_guard(최종 주장 방지)",
        ],
        "frontier_thesis": (
            "A fixed F20 low-VIX price-position long seed(F20 낮은 VIX 가격 위치 롱 씨앗) may become a better ONNX scout surface(ONNX 탐색 표면) "
            "only if a runtime-representable lifecycle/risk stack(런타임 표현 가능한 생명주기/위험 묶음) materially reduces DD(손실폭)."
        ),
        "hypothesis": (
            "With F20 entry fixed(F20 진입 고정), next-bar-open entry(다음 봉 시가 진입), ATR stop/take-profit(ATR 손절/익절), "
            "max-hold(최대 보유), cooldown(쿨다운), and optional early-adverse-exit(선택적 초기 불리 이동 청산) can reduce DD(손실폭) "
            "toward the final goal without validation/OOS reselecting the entry(검증/표본외 진입 재선택 없이 최종 목표 쪽으로 이동)."
        ),
        "decision_use": "Open F21A(전선21A)를 tracked stage open(추적 단계 개방)으로 만들고 F21B proxy(전선21B 프록시)의 fixed entry/lifecycle grid(고정 진입/생명주기 격자)를 잠급니다.",
        "comparison_baseline": (
            "F20 seed as reported(F20 보고 씨앗) plus F21 same-simulator parity baseline row(F21 동일 시뮬레이터 비교 행). "
            "This is not a selected baseline(선택 기준선 아님)."
        ),
        "control_variables": [
            "US100 M5 FPMarkets v2 model input dataset(US100 5분 FPMarkets v2 모델 입력 데이터셋)",
            "feature_set_v2 58 features(피처 세트 v2 58개 피처)",
            "label_v1 fwd12 split(라벨 v1 12봉 전방 분할)",
            "F20 entry rule and side fixed(F20 진입 규칙과 방향 고정)",
            "validation/OOS read-only diagnostics(검증/표본외 읽기 전용 진단)",
        ],
        "changed_variables": [
            "lifecycle profile(생명주기 프로필)",
            "ATR stop/take-profit multipliers(ATR 손절/익절 배수)",
            "max-hold bars(최대 보유 봉)",
            "cooldown bars(쿨다운 봉)",
            "early adverse exit flag(초기 불리 이동 청산 플래그)",
        ],
        "sample_scope": (
            "Tier A separate(티어 A 분리)는 58-feature model input(58개 피처 모델 입력)과 raw OHLC alignment(원천 OHLC 정렬)로 실행합니다. "
            "Tier B separate(티어 B 분리)와 Tier A+B combined(티어 A+B 합산)는 원천이 없으면 missing_required/out_of_scope_by_claim(필수 누락/주장 범위 밖)으로 기록합니다."
        ),
        "success_criteria": {
            "scout_clue": "validation/OOS positive(검증/표본외 양수), density near 5~10/day(일 5~10회 근처), DD clearly below F20 seed(F20 씨앗보다 명확히 낮은 손실폭)",
            "seed_surface": "PF around 1.2+(수익 팩터 약 1.2 이상), density 5~10/day(일 5~10회), validation DD <25% and OOS DD <18%(검증 손실폭 25% 미만 및 표본외 손실폭 18% 미만)",
            "handoff_candidate": "PF >=1.5, density 5~10/day, DD <=15%, smoothness improved, then pre-expensive Grok review before MT5(PF 1.5 이상/빈도 일 5~10회/DD 15% 이하/매끄러움 개선 뒤 MT5 전 그록 검토)",
        },
        "failure_criteria": [
            "No profile materially lowers DD versus F20 seed(F20 씨앗 대비 손실폭을 유의미하게 낮춘 프로필 없음)",
            "OOS PF below 1.0(표본외 수익 팩터 1.0 미만)",
            "Density leaves target band while only DD improves(손실폭만 개선되고 빈도가 목표 대역 이탈)",
            "Entry rule, quantile, or side changes(진입 규칙/분위수/방향 변경)",
        ],
        "invalid_conditions": [
            "new feature engineering(새 피처 설계)",
            "new entry rule search(새 진입 규칙 탐색)",
            "validation/OOS retuning(검증/표본외 재조정)",
            "MT5 claim without pre-expensive Grok review(MT5 전 그록 검토 없는 MT5 주장)",
        ],
        "stop_conditions": [
            "capped lifecycle sweep complete with no DD reduction(상한 생명주기 훑기 완료, 손실폭 감소 없음)",
            "profile count cap exceeded(프로필 수 상한 초과)",
            "handoff-like row appears and pre-expensive review is needed(인계 비슷한 행이 나타나 비싼 실행 전 검토 필요)",
        ],
        "evidence_plan": [
            "stage_open_summary.json(단계 개방 요약)",
            "lifecycle_lock.json(생명주기 잠금)",
            "F21B proxy metrics by split(F21B 분할별 프록시 지표)",
            "trade_log.csv(거래 기록)",
            "Tier A/Tier B/Tier A+B ledger rows(티어 A/B/합산 장부 행)",
            "runtime probe report or blocker(런타임 탐침 보고서 또는 차단 사유)",
        ],
        "entry_lock": ENTRY_LOCK,
        "lifecycle_grid": list(LIFECYCLE_GRID),
        "locks": list(LOCKS),
        "feature_count": len(feature_order),
        "feature_order_hash": ordered_hash(feature_order),
        "grok": grok,
        "f20_context": f20,
        "local_verification": local,
        "claim_boundary": {claim: "not_claimed(주장 없음)" for claim in f03b.FORBIDDEN_CLAIMS},
    }


def write_outputs(summary: dict[str, Any]) -> None:
    write_json(RUN_ROOT / "stage_open_summary.json", summary)
    write_json(RUN_ROOT / "run_manifest.json", run_manifest(summary))
    write_json(RUN_ROOT / "lifecycle_lock.json", lifecycle_lock(summary))
    write_json(RUN_ROOT / "guard_manifest.json", {"locks": summary["locks"], "entry_lock": ENTRY_LOCK, "lifecycle_grid": list(LIFECYCLE_GRID)})
    write_json(RUN_ROOT / "grok_receipt.json", grok_receipt(summary))
    f03b.write_text_sig(STAGE_ROOT / "README.md", readme_text(summary))
    f03b.write_text_sig(STAGE_ROOT / "00_spec" / "stage_brief.md", stage_brief(summary))
    f03b.write_text_sig(STAGE_ROOT / "00_spec" / "lifecycle_lock_spec.md", lifecycle_lock_spec(summary))
    f03b.write_text_sig(STAGE_ROOT / "00_spec" / "do_not_repeat.md", do_not_repeat_text(summary))
    f03b.write_text_sig(STAGE_ROOT / "01_inputs" / "experiment_design.md", experiment_design_text(summary))
    f03b.write_text_sig(STAGE_ROOT / "01_inputs" / "prior_stage_scan.md", prior_stage_scan_text(summary))
    f03b.write_text_sig(STAGE_ROOT / "01_inputs" / "input_refs.md", input_refs_text(summary))
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / "review_index.md", review_index(summary))
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / "grok_stage_open_receipt.md", grok_receipt_text(summary))
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / "local_verification.md", local_checks_text(summary))
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / "required_gate_coverage_audit.md", gate_audit(summary))
    f03b.write_text_sig(REPORT_PATH, report_text(summary))
    f03b.write_text_sig(STAGE_ROOT / "04_selected" / "selection_status.md", selection_status(summary))
    f03b.write_text_sig(DECISION_PATH, decision_text(summary))


def run_manifest(summary: dict[str, Any]) -> dict[str, Any]:
    return {
        "identity": {
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "parent_run_id": PARENT_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "created_at_utc": summary["created_at_utc"],
        },
        "artifacts": [
            artifact_identity(SCRIPT_PATH),
            artifact_identity(DATASET_PATH),
            artifact_identity(FEATURE_ORDER_PATH),
            artifact_identity(GROK_PACKET / "clean_output.md"),
            artifact_identity(F20_SUMMARY),
        ],
        "feature_schema": {
            "feature_count": summary["feature_count"],
            "feature_order_hash": summary["feature_order_hash"],
            "feature_order_path": FEATURE_ORDER_PATH.as_posix(),
        },
        "runtime_snapshot": {
            "symbol": "US100",
            "timeframe": "M5",
            "entry_timing": "next_bar_open_proxy(다음 봉 시가 프록시)",
            "position_management": "pre_registered_lifecycle_grid(사전 등록 생명주기 격자)",
            "cost_behavior": "rough_log_return_cost_proxy_only(거친 로그수익률 비용 프록시 전용)",
        },
        "rule_stack": {
            "entry": [ENTRY_LOCK],
            "position": list(LIFECYCLE_GRID),
            "filters": list(LOCKS),
            "exit": "ATR stop/take + max-hold + optional early-adverse-exit(ATR 손절/익절 + 최대 보유 + 선택적 초기 불리 청산)",
        },
        "results": {
            "by_split": {},
            "cross_split": {"stage_open": "planning_only_no_trading_kpi(계획 전용, 거래 KPI 없음)"},
            "report_refs": [{"role": "stage_open_report", "path": REPORT_PATH.as_posix()}],
        },
        "compatibility": {
            "schema_version": "frontier21_stage_open_v1",
            "mismatch_policy": "fail_fast(빠른 실패)",
            "required_output_schema": "not_applicable_stage_open(단계 개방에는 해당 없음)",
        },
    }


def lifecycle_lock(summary: dict[str, Any]) -> dict[str, Any]:
    return {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "entry_lock": ENTRY_LOCK,
        "lifecycle_grid": list(LIFECYCLE_GRID),
        "locks": list(LOCKS),
        "selection_boundary": "entry_fixed_lifecycle_only_train_selection_then_validation_oos_readonly(진입 고정, 생명주기만 학습 선택 뒤 검증/표본외 읽기 전용)",
        "claim_boundary": summary["claim_boundary"],
    }


def grok_receipt(summary: dict[str, Any]) -> dict[str, Any]:
    grok = summary["grok"]
    return {
        "trigger_reason": "stage_open_required_by_goal(목표가 요구한 단계 개방 검토)",
        "review_size": "small review(소규모 검토)",
        "direction_before_grok": "open F21 as fixed F20 seed plus lifecycle DD containment scout(F21을 고정 F20 씨앗 + 생명주기 손실폭 억제 탐색으로 개방)",
        "bounded_evidence": [
            F20_SELECTION.as_posix(),
            F20_PRESERVED.as_posix(),
            F20_NEGATIVE.as_posix(),
            F18_NEGATIVE_REPORT.as_posix(),
        ],
        "prompt_identity": {"path": grok["prompt"], "hash": grok["prompt_hash"]},
        "grok_output_identity": {"path": grok["output"], "classification": grok["classification"]},
        "advice_classification": "accepted_with_adjustments(조정 수용)",
        "local_verification": summary["local_verification"],
        "forbidden_claim_check": summary["claim_boundary"],
        "final_codex_direction": "Apply F20 entry lock, F18 differentiation lock, tiered DD criteria, and same-simulator baseline row(F20 진입 잠금/F18 차별화/계층 DD 기준/동일 시뮬레이터 비교 행 반영)",
    }


def readme_text(summary: dict[str, Any]) -> str:
    return f"""# {STAGE_ID}

Purpose(목적): fixed F20 seed entry(고정 F20 씨앗 진입)에 capped lifecycle DD containment(상한 생명주기 손실폭 억제)을 씌워 scout clue(탐색 단서)가 생기는지 봅니다.

Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음).

Current run(현재 실행): `{RUN_ID}`

Next run(다음 실행): `{NEXT_RUN_ID}`
"""


def stage_brief(summary: dict[str, Any]) -> str:
    return f"""# Frontier21 Stage Brief(전선21 단계 요약)

Opened(개방): {summary['created_at_utc']}

Frontier thesis(전선 가설): {summary['frontier_thesis']}

Hypothesis(가설): {summary['hypothesis']}

Novelty delta(신규성 차이): F20(전선20)의 rule atlas rerank(규칙 지도 재순위)를 반복하지 않고, F18(전선18)의 model/backbone lifecycle sweep(모델/백본 생명주기 훑기)도 반복하지 않습니다. Entry(진입)는 F20 fixed clue(고정 단서)이고 changed variable(변경 변수)은 lifecycle/risk stack(생명주기/위험 묶음)뿐입니다.

Entry lock(진입 잠금): `{ENTRY_LOCK['definition']}`, `{ENTRY_LOCK['side']}`

Exit rule(종료 규칙): capped lifecycle scout(상한 생명주기 탐색) 뒤 scout clue(탐색 단서), seed surface(씨앗 표면), completion candidate(완성 후보), preserved clue(보존 단서), negative memory(부정 기억), invalid setup(무효 설정), blocked(차단) 중 하나로 닫습니다.

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 not_claimed(주장 없음)입니다.
"""


def lifecycle_lock_spec(summary: dict[str, Any]) -> str:
    rows = [
        "| profile_id(프로필 ID) | role(역할) | max_hold(최대 보유) | stop ATR(손절 ATR) | take ATR(익절 ATR) | cooldown(쿨다운) | early exit(초기 청산) |",
        "|---|---:|---:|---:|---:|---:|---|",
    ]
    for profile in LIFECYCLE_GRID:
        rows.append(
            f"| `{profile['profile_id']}` | {profile['role']} | {profile['max_hold_bars']} | "
            f"{profile['atr_stop_multiplier']} | {profile['atr_take_profit_multiplier']} | {profile['cooldown_bars']} | {profile['early_adverse_exit_enabled']} |"
        )
    return "\n".join([
        "# Frontier21 Lifecycle Lock Spec(전선21 생명주기 잠금 명세)",
        "",
        f"Entry lock(진입 잠금): `{ENTRY_LOCK['definition']}`, `{ENTRY_LOCK['side']}`",
        "",
        "Rules(규칙):",
        "",
        *[f"- {item}" for item in LOCKS],
        "",
        *rows,
        "",
    ])


def do_not_repeat_text(summary: dict[str, Any]) -> str:
    return """# Frontier21 Do Not Repeat(전선21 반복 금지)

- Do not rerank F20 train-only rule atlas(F20 학습 전용 규칙 지도 재순위 금지).
- Do not change F20 entry quantile, conjunction, or side(F20 진입 분위수/결합/방향 변경 금지).
- Do not repeat F18 pre-registered model/backbone lifecycle sweep(F18 사전 등록 모델/백본 생명주기 훑기 반복 금지).
- Do not use F17 loss-cluster firewall as the main alpha(F17 손실 군집 방화벽을 주 알파로 쓰지 않음).
- Do not claim ONNX success before a surviving surface is encoded and checked(생존 표면 인코딩/검사 전 ONNX 성공 주장 금지).
"""


def experiment_design_text(summary: dict[str, Any]) -> str:
    return f"""# Frontier21 Experiment Design(전선21 실험 설계)

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


def prior_stage_scan_text(summary: dict[str, Any]) -> str:
    f20 = summary["f20_context"]
    return f"""# Frontier21 Prior Stage Scan(전선21 이전 단계 점검)

F20 preserved clue(전선20 보존 단서): `{ENTRY_LOCK['definition']}` long(롱), validation/OOS PF-density-DD(검증/표본외 수익 팩터-빈도-손실폭) `{fmt(f20['validation_profit_factor'])}/{fmt(f20['validation_trades_per_day'])}/{fmt(f20['validation_dd_risk'])}` and `{fmt(f20['oos_profit_factor'])}/{fmt(f20['oos_trades_per_day'])}/{fmt(f20['oos_dd_risk'])}`.

F20 negative memory(전선20 부정 기억): train-only depth-2 rule atlas(학습 전용 깊이2 규칙 지도) alone(단독)은 DD(손실폭)나 handoff(인계)를 해결하지 못했습니다.

F18 negative memory(전선18 부정 기억): lifecycle profile sweep(생명주기 프로필 훑기)은 단독 승격 근거가 아니며 low-DD shapes(낮은 손실폭 모양)만 참고 단서로 남겼습니다.

Reference boundary(참조 경계): Stage12~364(12~364단계)와 F18/F20(전선18/20)은 reference only(참조 전용)입니다. winner/baseline/promotion/runtime authority(승자/기준선/승격/런타임 권위)는 상속하지 않습니다.
"""


def input_refs_text(summary: dict[str, Any]) -> str:
    return f"""# Frontier21 Input References(전선21 입력 참조)

- dataset(데이터셋): `{DATASET_PATH.as_posix()}`
- feature order(피처 순서): `{FEATURE_ORDER_PATH.as_posix()}`
- feature hash(피처 해시): `{summary['feature_order_hash']}`
- F20 summary(F20 요약): `{F20_SUMMARY.as_posix()}`
- Grok packet(그록 묶음): `{GROK_PACKET.as_posix()}`
"""


def review_index(summary: dict[str, Any]) -> str:
    return f"""# Frontier21 Review Index(전선21 검토 색인)

- stage open report(단계 개방 보고서): `{REPORT_PATH.as_posix()}`
- Grok receipt(그록 영수증): `03_reviews/grok_stage_open_receipt.md`
- local verification(로컬 검증): `03_reviews/local_verification.md`
- gate audit(게이트 감사): `03_reviews/required_gate_coverage_audit.md`
"""


def grok_receipt_text(summary: dict[str, Any]) -> str:
    return f"""# Frontier21 Grok Stage Open Receipt(전선21 그록 단계 개방 영수증)

Trigger reason(트리거 이유): stage open required by goal(목표가 요구한 단계 개방 검토).

Review size(검토 크기): small review(소규모 검토).

Direction before Grok(그록 전 방향): fixed F20 entry plus lifecycle DD containment scout(고정 F20 진입 + 생명주기 손실폭 억제 탐색).

Prompt(프롬프트): `{summary['grok']['prompt']}`

Output(출력): `{summary['grok']['output']}`

Advice classification(조언 분류): `{summary['grok']['classification']}` accepted locally as adjusted direction(조정 방향으로 로컬 수용).

Local verification(로컬 검증): `{summary['local_verification']['judgment']}`

Final Codex direction(최종 코덱스 방향): F20 entry lock(F20 진입 잠금), F18 differentiation(F18 차별화), tiered DD criteria(계층 손실폭 기준), parity baseline row(동등성 비교 행)를 반영합니다.
"""


def local_checks_text(summary: dict[str, Any]) -> str:
    lines = ["# Frontier21 Local Verification(전선21 로컬 검증)", ""]
    for key, value in summary["local_verification"]["checks"].items():
        lines.append(f"- {key}: `{value}`")
    lines.append("")
    lines.append(f"Judgment(판정): `{summary['local_verification']['judgment']}`")
    return "\n".join(lines) + "\n"


def gate_audit(summary: dict[str, Any]) -> str:
    return f"""# Frontier21 Required Gate Coverage Audit(전선21 필수 게이트 커버리지 감사)

- external_review_packet(외부 검토 묶음): covered by(충족) `{GROK_PACKET.as_posix()}`
- kpi_contract_audit(KPI 계약 감사): planned for(계획됨) `{NEXT_RUN_ID}` split metrics(분할 지표)
- required_gate_coverage_audit(필수 게이트 커버리지 감사): this file(이 파일)
- final_claim_guard(최종 주장 방지): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성) all not_claimed(모두 주장 없음)
"""


def report_text(summary: dict[str, Any]) -> str:
    return f"""# Frontier21A Stage Open Report(전선21A 단계 개방 보고서)

Updated(갱신): {summary['created_at_utc']}

Status(상태): `{summary['status']}`

Judgment(판정): `{summary['judgment']}`

Action(행동): Frontier21(전선21)을 fixed F20 seed lifecycle DD containment scout(고정 F20 씨앗 생명주기 손실폭 억제 탐색)로 열었습니다.

Effect(효과): F20 entry(전선20 진입)는 고정하고, F21B(전선21B)는 lifecycle/risk stack(생명주기/위험 묶음)만 시험합니다. 이렇게 하면 DD(손실폭) 개선이 entry retuning(진입 재조정) 때문인지 lifecycle(생명주기) 때문인지 분리됩니다.

Grok classification(그록 분류): `{summary['grok']['classification']}`

Local verification(로컬 검증): `{summary['local_verification']['judgment']}`

Entry lock(진입 잠금): `{ENTRY_LOCK['definition']}`, `{ENTRY_LOCK['side']}`

Lifecycle profiles(생명주기 프로필 수): `{len(LIFECYCLE_GRID)}`

Next action(다음 행동): `{NEXT_RUN_ID}`

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def selection_status(summary: dict[str, Any]) -> str:
    return f"""# Frontier21 Selection Status(전선21 선택 상태)

Updated(갱신): {summary['created_at_utc']}

Selection(선택): no selected baseline/completion candidate/promotion/runtime authority(선택 기준선/완성 후보/승격/런타임 권위 없음).

Status(상태): `{summary['status']}`

Next action(다음 행동): `{NEXT_RUN_ID}`
"""


def decision_text(summary: dict[str, Any]) -> str:
    return f"""# Decision: Open Frontier21 F20 Seed Lifecycle DD Containment ONNX Scout(결정: 전선21 F20 씨앗 생명주기 손실폭 억제 ONNX 탐색 개방)

Date(날짜): {summary['created_at_utc']}

Decision(결정): `{summary['status']}`

Action(행동): F21(전선21)을 fixed entry lifecycle scout(고정 진입 생명주기 탐색)로 열었습니다.

Effect(효과): F20(전선20)의 보존 단서를 진입 표면으로만 쓰고, 손실폭 억제 메커니즘이 실제로 네 축 목표에 가까워지는지 봅니다.

Next action(다음 행동): `{NEXT_RUN_ID}`
"""


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
        "notes": "frontier21_stage_open_grok_adjusted_fixed_f20_entry_lifecycle_dd_contract_no_authority",
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
        "primary_kpi": f"grok={summary['grok']['classification']};profiles={len(LIFECYCLE_GRID)};feature_hash={summary['feature_order_hash']}",
        "guardrail_kpi": "fixed_f20_entry_no_model_training_no_wfo_no_mt5_no_authority(고정 F20 진입, 모델 학습/WFO/MT5/권위 없음)",
        "external_verification_status": "grok_stage_open_review_completed_runtime_probe_requires_handoff_candidate(그록 단계 개방 검토 완료, 런타임 탐침은 인계 후보 필요)",
        "notes": f"next={NEXT_RUN_ID};entry_lock=f20_seed;lifecycle_grid_cap={len(LIFECYCLE_GRID)};no_authority",
        "question": "Can a runtime-representable lifecycle stack contain DD on the fixed F20 seed?(런타임 표현 가능한 생명주기 묶음이 고정 F20 씨앗 손실폭을 억제할 수 있는가?)",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "run_family": "stage_open(단계 개방)",
    }


def idea_registry_entry(summary: dict[str, Any]) -> str:
    return (
        f"- `IDEA-FR21-F20-SEED-LIFECYCLE-DD-CONTAINMENT-ONNX-SCOUT`: `{RUN_ID}` opens fixed F20 seed lifecycle DD containment scout(고정 F20 씨앗 생명주기 손실폭 억제 탐색). "
        "Effect(효과): F20의 low-VIX long seed(낮은 VIX 롱 씨앗)를 진입으로만 고정하고, F18/F17 반복 없이 lifecycle/risk stack(생명주기/위험 묶음)의 DD 억제력을 봅니다.\n"
    )


def changelog_entry(summary: dict[str, Any]) -> str:
    return (
        f"- {summary['created_at_utc']}: `{RUN_ID}` opened Frontier21(전선21) after Grok adjusted review(그록 조정 검토). "
        f"Effect(효과): next run(다음 실행) `{NEXT_RUN_ID}` is locked to fixed F20 entry(고정 F20 진입) plus capped lifecycle grid(상한 생명주기 격자).\n"
    )


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

Action(행동): Frontier21(전선21)을 fixed F20 seed lifecycle DD containment scout(고정 F20 씨앗 생명주기 손실폭 억제 탐색)로 열었습니다.

Effect(효과): F20 entry(전선20 진입)는 바꾸지 않고, F21B(전선21B)에서 손절/익절/보유/쿨다운 생명주기만 시험해 DD(손실폭)가 줄어드는지 봅니다.

Claim boundary(주장 경계): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def ensure_stage_ledger_header() -> None:
    path = STAGE_ROOT / "03_reviews" / "stage_run_ledger.csv"
    if path_exists(path):
        return
    with io_path(ALPHA_LEDGER).open("r", encoding="utf-8-sig", newline="") as handle:
        header = next(csv.reader(handle))
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        csv.writer(handle, lineterminator="\n").writerow(header)


def artifact_identity(path: Path) -> dict[str, str]:
    return {"path": path.as_posix(), "sha256": sha256_file(path) if path_exists(path) else "missing(누락)"}


def read_feature_order() -> list[str]:
    return [line.strip() for line in io_path(FEATURE_ORDER_PATH).read_text(encoding="utf-8-sig").splitlines() if line.strip()]


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
    return f"{number:.6g}"


if __name__ == "__main__":
    raise SystemExit(main())
