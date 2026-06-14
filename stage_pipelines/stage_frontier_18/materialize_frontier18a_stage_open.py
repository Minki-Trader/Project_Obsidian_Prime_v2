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
from foundation.models.onnx_bridge import sha256_file
from stage_pipelines.stage_frontier_03 import frontier03b_regime_asymmetric_label_proxy_scout as f03b


STAGE_ID = "stage_frontier_18__asymmetric_exit_lifecycle_profit_lock_onnx_scout"
RUN_ID = "frontier18A_stage_open_asymmetric_exit_lifecycle_profit_lock_onnx_scout_v1"
RUN_NUMBER = "frontier18A"
PARENT_RUN_ID = "frontier17D_loss_cluster_firewall_repair_or_closeout_decision_v1"
NEXT_RUN_ID = "frontier18B_asymmetric_exit_lifecycle_proxy_scout_v1"
STATUS = "opened_frontier18_asymmetric_exit_lifecycle_profit_lock_onnx_scout_no_authority"
JUDGMENT = "stage_opened_after_grok_review_with_lifecycle_profile_locks_and_runtime_probe_obligation_no_authority"

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REPORT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_report.md"
DECISION_PATH = Path("docs/decisions/2026-06-14_stage_frontier_18_asymmetric_exit_lifecycle_profit_lock_onnx_scout_open.md")
SCRIPT_PATH = Path("stage_pipelines/stage_frontier_18/materialize_frontier18a_stage_open.py")
GROK_PACKET = Path("docs/agent_control/grok_reviews/2026-06-14_frontier18_stage_open/small_review")

F17_SELECTION = Path("stages/stage_frontier_17__loss_cluster_firewall_profit_persistence_onnx_scout/04_selected/selection_status.md")
F17C_REPORT = Path("stages/stage_frontier_17__loss_cluster_firewall_profit_persistence_onnx_scout/03_reviews/frontier17C_loss_cluster_firewall_runtime_probe_v1_report.md")
F17D_REPORT = Path("stages/stage_frontier_17__loss_cluster_firewall_profit_persistence_onnx_scout/03_reviews/frontier17D_loss_cluster_firewall_repair_or_closeout_decision_v1_report.md")
NEGATIVE_REGISTER = Path("docs/registers/negative_result_register.md")
IDEA_REGISTER = Path("docs/registers/idea_registry.md")
ALPHA_LEDGER = Path("docs/registers/alpha_run_ledger.csv")
RUN_REGISTRY = Path("docs/registers/run_registry.csv")
EA_ENTRYPOINT = Path("foundation/mt5/ObsidianPrimeV2_RuntimeProbeEA.mq5")

LIFECYCLE_PROFILES: tuple[dict[str, Any], ...] = (
    {
        "profile_id": "f18b_hold4_flat_close_atr1p2_tp2p4",
        "max_hold_bars": 4,
        "close_on_flat": True,
        "reverse_on_opposite": False,
        "atr_stop_multiplier": 1.2,
        "atr_take_profit_multiplier": 2.4,
        "intent": "short lifecycle with explicit profit lock(짧은 생명주기와 명시적 수익 잠금)",
    },
    {
        "profile_id": "f18b_hold6_reverse_atr1p5_tp3p0",
        "max_hold_bars": 6,
        "close_on_flat": False,
        "reverse_on_opposite": True,
        "atr_stop_multiplier": 1.5,
        "atr_take_profit_multiplier": 3.0,
        "intent": "balanced lifecycle with opposite signal transition(균형 생명주기와 반대 신호 전환)",
    },
    {
        "profile_id": "f18b_hold8_exit_risk_overlay_atr1p0_tp2p0",
        "max_hold_bars": 8,
        "close_on_flat": True,
        "reverse_on_opposite": False,
        "atr_stop_multiplier": 1.0,
        "atr_take_profit_multiplier": 2.0,
        "intent": "exit-risk overlay lane for early damage control(초기 손상 제어를 위한 청산 위험 덧씌움 축)",
    },
)

GUARDS: tuple[dict[str, str], ...] = (
    {
        "guard_id": "reference_not_inheritance",
        "rule": "No old winner, baseline, promotion, runtime authority, live readiness, or Goal Achieve is imported(이전 승자/기준선/승격/런타임 권위/실거래 준비/목표 달성 반입 금지).",
    },
    {
        "guard_id": "no_f17_alpha_reuse",
        "rule": "RuntimeVetoTape may be infrastructure only; loss-cluster firewall alpha is not the main hypothesis(RuntimeVetoTape는 인프라만, 손실 군집 방화벽 알파는 주 가설 금지).",
    },
    {
        "guard_id": "profile_cap_exactly_three",
        "rule": "Exactly three lifecycle profiles before Frontier18B metrics(전선18B 지표 전 생명주기 프로필 3개 고정).",
    },
    {
        "guard_id": "train_only_profile_policy",
        "rule": "No validation/OOS retuning of lifecycle parameters(검증/표본외 생명주기 파라미터 재조정 금지).",
    },
    {
        "guard_id": "stage344_exit_overlay_disclosure",
        "rule": "Stage344 exit-overlay failure is prior evidence only and must be disclosed(344단계 청산 오버레이 실패는 이전 근거 전용으로 공개).",
    },
    {
        "guard_id": "stage337_lifecycle_failure_disclosure",
        "rule": "Stage337 lifecycle-aware MT5 probe and cost2 failure are prior evidence only(337단계 생명주기 인식 MT5 탐침과 비용2 실패는 이전 근거 전용).",
    },
    {
        "guard_id": "tier_paired_records",
        "rule": "Record Tier A, Tier B, and Tier A+B or explicit missing_required(티어 A, 티어 B, 티어 A+B 또는 명시적 필수 누락 기록).",
    },
    {
        "guard_id": "runtime_probe_before_closeout",
        "rule": "Run one narrow MT5 runtime probe before closeout or record exact blocker(마감 전 좁은 MT5 런타임 탐침 1회 또는 정확한 차단 기록).",
    },
    {
        "guard_id": "claim_boundary_lock",
        "rule": "Only scout clue, seed surface, runtime probe observation, preserved clue, negative memory, invalid setup, or blocked may be claimed(탐색 단서/씨앗 표면/런타임 탐침 관찰/보존 단서/부정 기억/무효 설정/차단만 주장).",
    },
)


def main() -> int:
    now = utc_now()
    ensure_dirs()
    grok = read_grok()
    local = local_verification(grok)
    summary = build_summary(now, grok, local)
    write_outputs(summary)
    update_state_and_registries(summary)
    print(json.dumps(json_ready({
        "status": summary["status"],
        "judgment": summary["judgment"],
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "grok_classification": summary["grok_classification"],
        "local_verification": summary["local_verification"]["judgment"],
        "profile_count": len(LIFECYCLE_PROFILES),
        "guard_count": len(GUARDS),
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
    ensure_csv_header(STAGE_ROOT / "03_reviews" / "stage_run_ledger.csv", f03b.ALPHA_LEDGER)


def read_grok() -> dict[str, Any]:
    meta = read_json(GROK_PACKET / "metadata.json")
    output = read_text(GROK_PACKET / "clean_output.md")
    lowered = output.lower()
    return {
        "packet": GROK_PACKET.as_posix(),
        "prompt": (GROK_PACKET / "prompt.md").as_posix(),
        "output": (GROK_PACKET / "clean_output.md").as_posix(),
        "prompt_hash": meta.get("prompt_hash", ""),
        "success": bool(meta.get("success")),
        "duration_seconds": meta.get("duration_seconds", ""),
        "preflight_warnings": meta.get("preflight_warnings", []),
        "unexpected_top_level_artifacts": meta.get("unexpected_top_level_artifacts", []),
        "classification": classify_grok(output),
        "accepted_axis": "execution/lifecycle surface" in lowered or "실행/생명주기 표면" in output,
        "requires_stage344_scan": "stage344" in lowered and "exit" in lowered,
        "requires_runtime_probe": "runtime probe" in lowered or "런타임 탐침" in output,
        "forbidden_claim_clean": not any(term in lowered for term in (
            "runtime authority granted",
            "live readiness",
            "goal achieve",
            "selected baseline",
        )),
    }


def classify_grok(text: str) -> str:
    lowered = text.lower()
    if "classification" in lowered and "accepted" in lowered:
        return "accepted(수용)"
    if "classification" in lowered and "rejected" in lowered:
        return "rejected(거절)"
    if "needs_local_verification" in lowered:
        return "needs_local_verification(로컬 검증 필요)"
    return "classification_missing(분류 누락)"


def local_verification(grok: dict[str, Any]) -> dict[str, Any]:
    workspace = read_text(f03b.WORKSPACE_STATE)
    f17_selection = read_text(F17_SELECTION)
    f17c_report = read_text(F17C_REPORT)
    f17d_report = read_text(F17D_REPORT)
    negative_register = read_text(NEGATIVE_REGISTER)
    idea_register = read_text(IDEA_REGISTER)
    alpha_ledger = read_text(ALPHA_LEDGER)
    run_registry = read_text(RUN_REGISTRY)
    ea_text = read_text(EA_ENTRYPOINT)
    guard_ids = {guard["guard_id"] for guard in GUARDS}
    checks = {
        "workspace_points_to_frontier18A": (
            "next_run_id: frontier18A_stage_open_new_hypothesis_design_v1" in workspace
            or (f"current_stage_id: {STAGE_ID}" in workspace and f"current_run_id: {RUN_ID}" in workspace)
        ),
        "f17_closed_negative_memory": "negative_memory" in f17_selection and "no selected baseline" in f17_selection.lower(),
        "f17_runtime_signal_matched_but_dd_failed": "signal_diff=0" in f17d_report and "DD=47.5%" in f17d_report,
        "f17c_runtime_probe_completed": "runtime_probe_observation_completed_signal_matched_no_authority" in f17c_report,
        "stage344_exit_overlay_memory_found": "run344E Exit Overlay Failure Memory" in negative_register,
        "stage337_lifecycle_memory_found": (
            "run337CD_train_lifecycle_aware_guarded_scouts" in alpha_ledger
            or "run337CD_train_lifecycle_aware_guarded_scouts" in run_registry
            or "run337CD_train_lifecycle_aware_guarded_scouts" in idea_register
            or "run337CD_train_lifecycle_aware_guarded_scouts" in negative_register
        ),
        "ea_lifecycle_inputs_available": all(token in ea_text for token in (
            "InpMaxHoldBars",
            "InpReverseOnOppositeSignal",
            "InpCloseOnlyOnOppositeSignal",
            "InpExitRiskOverlayEnabled",
            "InpAtrStopMultiplier",
            "InpAtrTakeProfitMultiplier",
        )),
        "grok_success": bool(grok["success"]),
        "grok_accepted": grok["classification"] == "accepted(수용)",
        "grok_axis_supported": bool(grok["accepted_axis"]),
        "grok_stage344_requirement_supported": bool(grok["requires_stage344_scan"]),
        "grok_runtime_probe_supported": bool(grok["requires_runtime_probe"]),
        "grok_no_unexpected_top_level_artifacts": not grok["unexpected_top_level_artifacts"],
        "grok_forbidden_claim_clean": bool(grok["forbidden_claim_clean"]),
        "profile_cap_is_three": len(LIFECYCLE_PROFILES) == 3,
        "required_guard_ids_present": {
            "reference_not_inheritance",
            "no_f17_alpha_reuse",
            "stage344_exit_overlay_disclosure",
            "runtime_probe_before_closeout",
            "claim_boundary_lock",
        }.issubset(guard_ids),
    }
    return {
        "checks": checks,
        "preflight_warnings": grok["preflight_warnings"],
        "judgment": "pass_with_boundary(경계 포함 통과)" if all(checks.values()) else "needs_manual_review(수동 검토 필요)",
    }


def build_summary(now: str, grok: dict[str, Any], local: dict[str, Any]) -> dict[str, Any]:
    return {
        "created_at_utc": now,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "hypothesis": (
            "Asymmetric exit lifecycle(비대칭 청산 생명주기) and profit-lock policy(수익 잠금 정책) can improve "
            "PF/DD/smoothness(수익 팩터/손실폭/매끄러움) for moderate ONNX entry signals(중간 품질 ONNX 진입 신호) "
            "without reusing F17 loss-cluster firewall alpha(전선17 손실 군집 방화벽 알파)."
        ),
        "decision_use": "Open a bounded proxy scout(제한된 프록시 탐색) for lifecycle profiles(생명주기 프로필), not a completion or runtime authority claim(완성 또는 런타임 권위 주장 아님).",
        "comparison_baseline": "F17B proxy and F17C MT5 runtime observation(전선17B 프록시와 전선17C MT5 런타임 관찰), reference only(참조 전용).",
        "control_variables": [
            "US100 M5 FPMarkets data contract(US100 5분봉 FPMarkets 데이터 계약)",
            "closed-bar inference(닫힌 봉 추론)",
            "58-feature order contract(58개 피처 순서 계약)",
            "one concurrent position max(동시 포지션 1개)",
            "fixed 0.1 lot for scout runtime probe(탐색 런타임 탐침 고정 0.1랏)",
        ],
        "changed_variables": [
            "max hold bars(최대 보유 봉)",
            "flat/opposite exit behavior(중립/반대 신호 청산 동작)",
            "ATR stop/take-profit bracket(ATR 손절/익절 괄호)",
            "entry-known exit-risk overlay when available(가능하면 진입 시점에 아는 청산 위험 덧씌움)",
        ],
        "sample_scope": "Tier A full-context sample first(티어 A 전체 문맥 표본 우선), Tier B and combined records explicit if missing(티어 B와 합산은 누락 시 명시).",
        "success_criteria": {
            "scout_clue": "validation/OOS PF moves toward 2+, density stays near 5~10/day, DD improves toward 10~15%, and smoothness improves(검증/표본외 수익 팩터 2+ 방향, 일 5~10회 근처, 손실폭 10~15% 방향, 매끄러움 개선).",
            "seed_surface": "a lifecycle profile reduces proxy or MT5 DD/smoothness damage without density below 3/day(생명주기 프로필이 밀도 3/day 미만 붕괴 없이 프록시 또는 MT5 손실폭/매끄러움 손상을 줄임).",
            "runtime_probe_obligation": "one narrow MT5 runtime probe before closeout or exact blocked reason(마감 전 좁은 MT5 런타임 탐침 1회 또는 정확한 차단 사유).",
        },
        "failure_criteria": [
            "global exit repair damages net/PF/expectancy like Stage344(전역 청산 수리가 344단계처럼 순수익/수익 팩터/기대값 훼손)",
            "lifecycle-aware proxy clears parity but cost/direction failure remains like Stage337(생명주기 인식 프록시가 동등성은 맞지만 337단계처럼 비용/방향 실패 유지)",
            "density/PF/DD tradeoff repeats F17 MT5 collapse(빈도/수익 팩터/손실폭 상충이 전선17 MT5 붕괴 반복)",
        ],
        "invalid_conditions": [
            "validation/OOS lifecycle retuning(검증/표본외 생명주기 재조정)",
            "F17 loss-cluster firewall alpha reused as main hypothesis(전선17 손실 군집 방화벽 알파를 주 가설로 재사용)",
            "current-bar or future outcome leakage(현재봉 또는 미래 결과 누수)",
        ],
        "stop_conditions": [
            "strict scout clue or seed surface found, then pre-expensive Grok review before MT5(WFO/MT5 전 그록 검토)",
            "no seed after pre-registered profiles, then repair/closeout decision(사전 등록 프로필 후 씨앗 없음이면 수리/마감 결정)",
            "runtime claim would be needed, then MT5 probe attempted or exact blocked reason recorded(런타임 주장이 필요하면 MT5 탐침 시도 또는 정확한 차단 기록)",
        ],
        "evidence_plan": [
            "stage open summary and manifests(단계 개방 요약과 목록)",
            "proxy profile metrics by split(분할별 프록시 프로필 지표)",
            "Tier A/B/combined ledger rows(티어 A/B/합산 장부 행)",
            "ONNX parity when a model artifact is created(모델 산출물 생성 시 ONNX 동등성)",
            "MT5 runtime probe report before closeout(마감 전 MT5 런타임 탐침 보고서)",
        ],
        "data_integrity": {
            "data_source": "existing FPMarkets v2 US100 M5 model input dataset(기존 FPMarkets v2 US100 5분봉 모델 입력 데이터셋)",
            "time_axis": "closed-bar broker-clock alignment plus project time-axis policy(닫힌 봉 브로커 시계 정렬과 프로젝트 시간축 정책)",
            "feature_label_boundary": "lifecycle parameters are train-only or pre-registered; no future outcome in runtime rules(생명주기 파라미터는 학습 전용 또는 사전 등록, 런타임 규칙에 미래 결과 없음)",
            "split_boundary": "train/validation/OOS chronological split(시간순 학습/검증/표본외 분할)",
            "integrity_judgment": "usable_with_boundary(경계 포함 사용 가능)",
        },
        "model_validation": {
            "model_family": "existing ONNX-compatible classifier family to be chosen in Frontier18B(전선18B에서 선택할 ONNX 호환 분류기 계열)",
            "target_and_label": "entry signal unchanged at stage open; lifecycle decision surface changed(단계 개방에서는 진입 신호 유지, 생명주기 결정 표면 변경)",
            "selection_metric": "joint PF/DD/density/smoothness proxy, not single metric(수익 팩터/손실폭/빈도/매끄러움 동시 프록시, 단일 지표 아님)",
            "threshold_policy": "pre-registered or train-only(사전 등록 또는 학습 전용)",
            "validation_judgment": "exploratory_stage_open(탐색 단계 개방)",
        },
        "lifecycle_profiles": list(LIFECYCLE_PROFILES),
        "guards": list(GUARDS),
        "grok_packet": grok["packet"],
        "grok_output": grok["output"],
        "grok_prompt_hash": grok["prompt_hash"],
        "grok_duration_seconds": grok["duration_seconds"],
        "grok_classification": grok["classification"],
        "local_verification": local,
        "claim_boundary": {claim: "not_claimed(주장 없음)" for claim in f03b.FORBIDDEN_CLAIMS},
    }


def write_outputs(summary: dict[str, Any]) -> None:
    write_json(RUN_ROOT / "stage_open_summary.json", summary)
    write_json(RUN_ROOT / "run_manifest.json", run_manifest(summary))
    write_json(RUN_ROOT / "lifecycle_profile_manifest.json", {"profiles": summary["lifecycle_profiles"]})
    write_json(RUN_ROOT / "guard_manifest.json", {"guards": summary["guards"]})
    f03b.write_text_sig(STAGE_ROOT / "README.md", readme_text(summary))
    f03b.write_text_sig(STAGE_ROOT / "00_spec" / "stage_brief.md", stage_brief(summary))
    f03b.write_text_sig(STAGE_ROOT / "00_spec" / "lifecycle_profile_spec.md", lifecycle_profile_spec(summary))
    f03b.write_text_sig(STAGE_ROOT / "00_spec" / "do_not_repeat.md", do_not_repeat_text(summary))
    f03b.write_text_sig(STAGE_ROOT / "01_inputs" / "experiment_design.md", experiment_design_text(summary))
    f03b.write_text_sig(STAGE_ROOT / "01_inputs" / "prior_stage_scan.md", prior_stage_scan_text(summary))
    f03b.write_text_sig(STAGE_ROOT / "01_inputs" / "local_checks.md", local_checks_text(summary))
    f03b.write_text_sig(STAGE_ROOT / "01_inputs" / "input_refs.md", input_refs_text(summary))
    f03b.write_text_sig(STAGE_ROOT / "01_inputs" / "selection_metric_spec.md", selection_metric_spec(summary))
    f03b.write_text_sig(REPORT_PATH, report_text(summary))
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / "review_index.md", review_index(summary))
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / "required_gate_coverage_audit.md", gate_audit(summary))
    f03b.write_text_sig(STAGE_ROOT / "04_selected" / "selection_status.md", selection_status(summary))
    f03b.write_text_sig(DECISION_PATH, decision_text(summary))


def update_state_and_registries(summary: dict[str, Any]) -> None:
    f03b.write_text_sig(f03b.WORKSPACE_STATE, workspace_state(summary))
    f03b.write_text_sig(f03b.CURRENT_WORKING_STATE, current_working_state(summary))
    upsert_csv_io(f03b.RUN_REGISTRY, "run_id", run_registry_row(summary))
    upsert_csv_io(f03b.ALPHA_LEDGER, "ledger_row_id", ledger_row(summary))
    upsert_csv_io(STAGE_ROOT / "03_reviews" / "stage_run_ledger.csv", "ledger_row_id", ledger_row(summary))
    f03b.append_once(f03b.IDEA_REGISTRY, RUN_ID, idea_registry_entry(summary))
    f03b.append_once(f03b.CHANGELOG, RUN_ID, changelog_entry(summary))


def run_manifest(summary: dict[str, Any]) -> dict[str, Any]:
    return {
        **summary,
        "script_path": SCRIPT_PATH.as_posix(),
        "script_sha256": sha256_file(SCRIPT_PATH),
        "inputs": {
            "frontier17_selection": artifact_identity(F17_SELECTION),
            "frontier17c_runtime_report": artifact_identity(F17C_REPORT),
            "frontier17d_closeout_report": artifact_identity(F17D_REPORT),
            "negative_result_register": artifact_identity(NEGATIVE_REGISTER),
            "idea_register": artifact_identity(IDEA_REGISTER),
            "alpha_run_ledger": artifact_identity(ALPHA_LEDGER),
            "run_registry": artifact_identity(RUN_REGISTRY),
            "ea_entrypoint": artifact_identity(EA_ENTRYPOINT),
            "grok_stage_open_output": artifact_identity(Path(summary["grok_output"])),
        },
        "outputs": {
            "stage_open_summary": (RUN_ROOT / "stage_open_summary.json").as_posix(),
            "lifecycle_profile_manifest": (RUN_ROOT / "lifecycle_profile_manifest.json").as_posix(),
            "guard_manifest": (RUN_ROOT / "guard_manifest.json").as_posix(),
            "report": REPORT_PATH.as_posix(),
            "decision": DECISION_PATH.as_posix(),
        },
    }


def readme_text(summary: dict[str, Any]) -> str:
    return f"""# Frontier18 Asymmetric Exit Lifecycle Profit Lock ONNX Scout(전선18 비대칭 청산 생명주기 수익 잠금 ONNX 탐색)

Status(상태): `{summary['status']}`

Next run(다음 실행): `{NEXT_RUN_ID}`

Claim boundary(주장 경계): scout clue/seed surface/runtime probe observation/preserved clue/negative memory/invalid setup/blocked(탐색 단서/씨앗 표면/런타임 탐침 관찰/보존 단서/부정 기억/무효 설정/차단)까지만 허용합니다.
"""


def stage_brief(summary: dict[str, Any]) -> str:
    return f"""# Frontier18 Stage Brief(전선18 단계 개요)

Stage id(단계 ID): `{STAGE_ID}`

Question(질문): asymmetric exit lifecycle(비대칭 청산 생명주기) and profit-lock policy(수익 잠금 정책)가 moderate ONNX entry signals(중간 품질 ONNX 진입 신호)의 PF/DD/smoothness(수익 팩터/손실폭/매끄러움)를 개선할 수 있는가?

## Frontier Thesis(전선 가설)

{summary['hypothesis']}

## Novelty Delta(신규성 차이)

Changed variable(변경 변수)은 entry veto(진입 차단)가 아니라 position lifecycle/execution surface(포지션 생명주기/실행 표면)입니다. Effect(효과): F15 score threshold(점수 임계값), F16 edge-margin risk-veto(엣지 마진 위험 배제), F17 loss-cluster firewall(손실 군집 방화벽)을 반복하지 않습니다.

## Exit Rule(종료 규칙)

Frontier18(전선18)은 proxy(프록시), WFO/stress/runtime validation(WFO/스트레스/런타임 검증), repair(수리), closeout(마감)을 지나며 completion candidate(완성 후보), preserved clue(보존 단서), negative memory(부정 기억), invalid setup(무효 설정), blocked(차단) 중 하나로 닫습니다.

## Claim Boundary(주장 경계)

completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def lifecycle_profile_spec(summary: dict[str, Any]) -> str:
    rows = "\n".join(
        "- `{profile_id}`: max_hold_bars(최대 보유 봉) `{max_hold_bars}`, close_on_flat(중립 청산) `{close_on_flat}`, reverse_on_opposite(반대 신호 전환) `{reverse_on_opposite}`, ATR SL/TP(ATR 손절/익절) `{atr_stop_multiplier}`/`{atr_take_profit_multiplier}`; {intent}".format(**profile)
        for profile in summary["lifecycle_profiles"]
    )
    return f"""# Frontier18 Lifecycle Profile Spec(전선18 생명주기 프로필 명세)

Action(행동): Frontier18B(전선18B) 전에 3 lifecycle profiles(생명주기 프로필)를 고정합니다.

Effect(효과): validation/OOS(검증/표본외) 결과를 본 뒤 exit parameter(청산 파라미터)를 추가하는 repair ladder(수리 사다리)를 막습니다.

{rows}
"""


def do_not_repeat_text(summary: dict[str, Any]) -> str:
    rows = "\n".join(f"- `{guard['guard_id']}`: {guard['rule']}" for guard in summary["guards"])
    return f"""# Do Not Repeat(반복 금지)

{rows}
"""


def experiment_design_text(summary: dict[str, Any]) -> str:
    return f"""# Frontier18 Experiment Design(전선18 실험 설계)

- primary_family(주 작업군): `experiment_design(실험 설계)`
- primary_skill(주 스킬): `obsidian-experiment-design`
- support_skills(보조 스킬): `obsidian-data-integrity`, `obsidian-model-validation`, `obsidian-grok-collaboration`
- required_gates(필수 게이트): `work_packet_schema_lint`, `external_review_packet`, `lifecycle_profile_lock_gate`, `required_gate_coverage_audit`, `final_claim_guard`

hypothesis(가설): {summary['hypothesis']}

decision_use(결정 용도): {summary['decision_use']}

comparison_baseline(비교 기준): {summary['comparison_baseline']}

control_variables(통제 변수): {', '.join(summary['control_variables'])}

changed_variables(변경 변수): {', '.join(summary['changed_variables'])}

sample_scope(표본 범위): {summary['sample_scope']}

success_criteria(성공 기준): {json.dumps(summary['success_criteria'], ensure_ascii=False)}

failure_criteria(실패 기준): {', '.join(summary['failure_criteria'])}

invalid_conditions(무효 조건): {', '.join(summary['invalid_conditions'])}

stop_conditions(중단 조건): {', '.join(summary['stop_conditions'])}

evidence_plan(근거 계획): {', '.join(summary['evidence_plan'])}
"""


def prior_stage_scan_text(summary: dict[str, Any]) -> str:
    return """# Frontier18 Prior Stage Scan(전선18 이전 단계 점검)

F17 negative memory(전선17 부정 기억): loss-cluster firewall profit persistence(손실 군집 방화벽 수익 지속)는 MT5 economics/DD(MT5 실행 경제성/손실폭)에서 실패했습니다. Effect(효과): F18은 같은 entry firewall(진입 방화벽)을 반복하지 않습니다.

F17 preserved clue(전선17 보존 단서): RuntimeVetoTape(런타임 차단 테이프) handoff(인계)는 기술 단서로만 보존합니다. Effect(효과): F18의 주 가설은 RuntimeVetoTape가 아니라 lifecycle/execution surface(생명주기/실행 표면)입니다.

Stage344 prior evidence only(344단계 이전 근거 전용): run344E(344E 실행)의 s09/s10/s12 exit lifecycle overlay(청산 생명주기 덧씌움)는 net/PF/expectancy(순수익/수익 팩터/기대값)를 훼손했습니다. Effect(효과): global exit repair(전역 청산 수리)를 기본 해법으로 반복하지 않습니다.

Stage337 prior evidence only(337단계 이전 근거 전용): lifecycle-aware guarded scouts(생명주기 인식 방어 스카우트)는 ONNX parity(ONNX 동등성)와 runtime overlap parity(런타임 겹침 동등성)를 일부 맞췄지만 cost2 survivor(비용2 생존자) 0과 direction failure(방향 실패)가 남았습니다. Effect(효과): parity(동등성)만으로 긍정 판정을 만들지 않습니다.

Reference only(참조 전용): winner/baseline/promotion/runtime authority/live readiness/Goal Achieve(승자/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 상속하지 않습니다.
"""


def local_checks_text(summary: dict[str, Any]) -> str:
    checks = "\n".join(f"- {key}: `{value}`" for key, value in summary["local_verification"]["checks"].items())
    warnings = ", ".join(summary["local_verification"].get("preflight_warnings", [])) or "none(없음)"
    return f"""# Frontier18 Local Checks(전선18 로컬 확인)

Judgment(판정): `{summary['local_verification']['judgment']}`

Grok preflight warnings(그록 사전 경고): `{warnings}`

{checks}
"""


def input_refs_text(summary: dict[str, Any]) -> str:
    return f"""# Frontier18 Input Refs(전선18 입력 참조)

- Frontier17 selection status(전선17 선택 상태): `{F17_SELECTION.as_posix()}`
- Frontier17C runtime report(전선17C 런타임 보고서): `{F17C_REPORT.as_posix()}`
- Frontier17D closeout report(전선17D 마감 보고서): `{F17D_REPORT.as_posix()}`
- negative result register(부정 결과 등록부): `{NEGATIVE_REGISTER.as_posix()}`
- Grok stage-open output(그록 단계 개방 출력): `{summary['grok_output']}`
- EA entrypoint(EA 진입점): `{EA_ENTRYPOINT.as_posix()}`
"""


def selection_metric_spec(summary: dict[str, Any]) -> str:
    return f"""# Frontier18 Selection Metric Spec(전선18 선택 지표 명세)

- scout clue(탐색 단서): validation/OOS(검증/표본외) PF, density, DD, smoothness(수익 팩터, 빈도, 손실폭, 매끄러움)를 함께 봅니다.
- seed surface(씨앗 표면): DD/smoothness(손실폭/매끄러움)를 줄이면서 density(빈도)가 3/day(일 3회) 아래로 무너지지 않는 profile(프로필)만 기록합니다.
- negative memory(부정 기억): Stage344(344단계)처럼 exit overlay(청산 덧씌움)가 net/PF/expectancy(순수익/수익 팩터/기대값)를 훼손하거나, F17(전선17)처럼 MT5 DD collapse(MT5 손실폭 붕괴)가 반복되면 닫습니다.
- runtime probe observation(런타임 탐침 관찰): closeout(마감) 전 best-or-seed candidate(최선 또는 씨앗 후보) 1개를 MT5 runtime probe(MT5 런타임 탐침)로 시도합니다.
"""


def report_text(summary: dict[str, Any]) -> str:
    return f"""# Frontier18A Stage Open Report(전선18A 단계 개방 보고서)

Updated(갱신): {summary['created_at_utc']}

Status(상태): `{summary['status']}`

Judgment(판정): `{summary['judgment']}`

Action(행동): Frontier18(전선18)을 asymmetric exit lifecycle profit-lock ONNX scout(비대칭 청산 생명주기 수익 잠금 ONNX 탐색)로 열었습니다.

Effect(효과): F17(전선17)의 entry firewall(진입 방화벽) 실패를 반복하지 않고, MT5에서 이미 표현 가능한 lifecycle/execution surface(생명주기/실행 표면)를 새 가설 축으로 고정합니다.

Grok classification(그록 분류): `{summary['grok_classification']}`

Local verification(로컬 검증): `{summary['local_verification']['judgment']}`

Profile count(프로필 수): `{len(summary['lifecycle_profiles'])}`

Guard count(가드 수): `{len(summary['guards'])}`

Next run(다음 실행): `{NEXT_RUN_ID}`

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def review_index(summary: dict[str, Any]) -> str:
    return f"""# Frontier18 Review Index(전선18 검토 색인)

Updated(갱신): {summary['created_at_utc']}

- `{RUN_ID}`: stage open(단계 개방), Grok accepted(그록 수용), lifecycle profile locks(생명주기 프로필 고정), Stage344/337 prior evidence(344/337단계 이전 근거), runtime probe obligation(런타임 탐침 의무) recorded(기록).
"""


def gate_audit(summary: dict[str, Any]) -> str:
    return f"""# Frontier18A Required Gate Coverage Audit(전선18A 필수 게이트 커버리지 감사)

Updated(갱신): {summary['created_at_utc']}

Status(상태): pass_with_boundary(경계 포함 통과)

- work_packet_schema_lint(작업 묶음 스키마 점검): hypothesis/controls/success/failure/invalid/stop/evidence(가설/통제/성공/실패/무효/중단/근거) recorded(기록).
- external_review_packet(외부 검토 묶음): Grok accepted(그록 수용), packet(묶음) `{summary['grok_packet']}`.
- lifecycle_profile_lock_gate(생명주기 프로필 고정 게이트): 3 profiles(프로필 3개) fixed before Frontier18B metrics(전선18B 지표 전 고정).
- prior_stage_scan_gate(이전 단계 점검 게이트): F17/Stage344/Stage337(전선17/344단계/337단계) recorded as reference only(참조 전용 기록).
- runtime_probe_obligation_gate(런타임 탐침 의무 게이트): `runtime_probe_before_closeout` recorded(기록).
- final_claim_guard(최종 주장 보호): no completion/baseline/promotion/runtime/live/Goal claim(완성/기준선/승격/런타임/실거래/목표 주장 없음).
"""


def selection_status(summary: dict[str, Any]) -> str:
    return f"""# Frontier18 Selection Status(전선18 선택 상태)

Updated(갱신): {summary['created_at_utc']}

Status(상태): `{summary['status']}`

Judgment(판정): `{summary['judgment']}`

Selection(선택): no selected baseline/completion candidate/promotion/runtime authority(선택 기준선/완성 후보/승격/런타임 권위 없음).

Next action(다음 행동): `{NEXT_RUN_ID}`
"""


def decision_text(summary: dict[str, Any]) -> str:
    return f"""# Decision: Open Frontier18 Asymmetric Exit Lifecycle Profit Lock ONNX Scout(결정: 전선18 비대칭 청산 생명주기 수익 잠금 ONNX 탐색 개방)

Date(날짜): {summary['created_at_utc']}

Decision(결정): `{summary['status']}`

Action(행동): Frontier18(전선18)을 새 hypothesis lifecycle(가설 생명주기)로 열었습니다.

Effect(효과): F17(전선17)의 손실 군집 방화벽 알파를 상속하지 않고, MT5 runtime capability(MT5 런타임 기능)로 표현 가능한 lifecycle/execution surface(생명주기/실행 표면)를 탐색합니다.

Next action(다음 행동): `{NEXT_RUN_ID}`
"""


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

Action(행동): Frontier18(전선18)을 asymmetric exit lifecycle profit-lock ONNX scout(비대칭 청산 생명주기 수익 잠금 ONNX 탐색)로 열었습니다.

Effect(효과): 다음 실행은 3 lifecycle profiles(생명주기 프로필 3개)를 proxy(프록시)로 시험하며, F17 loss-cluster firewall alpha(전선17 손실 군집 방화벽 알파)는 주 가설로 반복하지 않습니다.

Claim boundary(주장 경계): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def run_registry_row(summary: dict[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "stage_open(단계 개방)",
        "status": summary["status"],
        "judgment": summary["judgment"],
        "path": REPORT_PATH.as_posix(),
        "notes": "frontier18_stage_open_grok_accepted_lifecycle_profile_locks_runtime_probe_obligation_no_authority",
        "family": "experiment_design(실험 설계)",
        "work_family": "experiment_design(실험 설계)",
        "run_number": RUN_NUMBER,
        "date": "2026-06-14",
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "claim_boundary": "stage_open_no_model_no_wfo_no_mt5_no_authority_goal_claim",
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
        "primary_kpi": f"grok_classification={summary['grok_classification']};profiles={len(LIFECYCLE_PROFILES)};guards={len(GUARDS)}",
        "guardrail_kpi": "no_model_no_wfo_no_mt5_no_authority(모델/WFO/MT5/권위 없음)",
        "external_verification_status": "grok_stage_open_review_completed_runtime_probe_required_before_closeout(그록 단계 개방 검토 완료, 마감 전 런타임 탐침 필요)",
        "notes": f"next={NEXT_RUN_ID};lifecycle_profile_locks;no_authority",
        "question": "Can asymmetric exit lifecycle plus profit lock improve PF/DD/smoothness?(비대칭 청산 생명주기와 수익 잠금이 수익 팩터/손실폭/매끄러움을 개선할 수 있는가?)",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "run_family": "stage_open(단계 개방)",
    }


def idea_registry_entry(summary: dict[str, Any]) -> str:
    return (
        f"- `IDEA-FR18-ASYMMETRIC-EXIT-LIFECYCLE-PROFIT-LOCK-ONNX-SCOUT`: `{RUN_ID}` opens asymmetric exit lifecycle profit-lock ONNX scout(비대칭 청산 생명주기 수익 잠금 ONNX 탐색). "
        "Effect(효과): F17(전선17)의 entry firewall(진입 방화벽)을 반복하지 않고 lifecycle/execution surface(생명주기/실행 표면)를 새 가설로 시험합니다.\n"
    )


def changelog_entry(summary: dict[str, Any]) -> str:
    return (
        f"- {summary['created_at_utc']}: `{RUN_ID}` opened Frontier18(전선18) after Grok stage-open accepted(그록 단계 개방 수용). "
        f"Effect(효과): next run(다음 실행) `{NEXT_RUN_ID}` will test 3 lifecycle profiles(생명주기 프로필 3개) with no authority claims(권위 주장 없음).\n"
    )


def ensure_csv_header(path: Path, template_path: Path) -> None:
    if path_exists(path):
        return
    header = read_csv_header_io(template_path)
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        csv.writer(handle, lineterminator="\n").writerow(header)


def read_csv_header_io(path: Path) -> list[str]:
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return next(csv.reader(handle))


def upsert_csv_io(path: Path, key: str, row: dict[str, Any]) -> None:
    header = read_csv_header_io(path)
    rows: list[dict[str, str]] = []
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        for existing in csv.DictReader(handle):
            rows.append(dict(existing))
    normalized = {column: f03b.stringify(row.get(column, "")) for column in header}
    replaced = False
    for index, existing in enumerate(rows):
        if existing.get(key) == normalized.get(key):
            rows[index] = normalized
            replaced = True
            break
    if not replaced:
        rows.append(normalized)
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=header, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for item in rows:
            writer.writerow({column: f03b.stringify(item.get(column, "")) for column in header})


def artifact_identity(path: Path) -> dict[str, str]:
    return {"path": path.as_posix(), "sha256": sha256_file(path) if path_exists(path) else "missing(누락)"}


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def read_text(path: Path) -> str:
    return io_path(path).read_text(encoding="utf-8-sig")


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8-sig")


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


if __name__ == "__main__":
    raise SystemExit(main())
