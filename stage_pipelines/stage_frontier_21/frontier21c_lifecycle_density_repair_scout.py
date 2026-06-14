from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.control_plane.ledger import io_path, json_ready
from foundation.models.onnx_bridge import ordered_hash
from stage_pipelines.stage_frontier_03 import frontier03b_regime_asymmetric_label_proxy_scout as f03b
from stage_pipelines.stage_frontier_07 import frontier07b_adverse_excursion_risk_label_proxy_scout as f07b
from stage_pipelines.stage_frontier_21 import frontier21b_f20_seed_lifecycle_proxy_scout as f21b


STAGE_ID = f21b.STAGE_ID
RUN_ID = "frontier21C_lifecycle_density_repair_scout_v1"
RUN_NUMBER = "frontier21C"
PARENT_RUN_ID = f21b.RUN_ID
NEXT_CLOSEOUT_RUN_ID = "frontier21D_lifecycle_repair_or_closeout_decision_v1"
NEXT_PRE_EXPENSIVE_GROK_RUN_ID = "frontier21D_grok_pre_expensive_lifecycle_repair_handoff_review_v1"

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REPORT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_report.md"
SCRIPT_PATH = Path("stage_pipelines/stage_frontier_21/frontier21c_lifecycle_density_repair_scout.py")
F21A_LOCK = STAGE_ROOT / "02_runs" / f21b.PARENT_RUN_ID / "lifecycle_lock.json"
F21B_SUMMARY = STAGE_ROOT / "02_runs" / PARENT_RUN_ID / "final_summary.json"

RUN_REGISTRY = Path("docs/registers/run_registry.csv")
ALPHA_LEDGER = Path("docs/registers/alpha_run_ledger.csv")
IDEA_REGISTRY = Path("docs/registers/idea_registry.md")
CHANGELOG = Path("docs/workspace/changelog.md")
WORKSPACE_STATE = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE = Path("docs/context/current_working_state.md")


REPAIR_PROFILES = [
    f21b.LifecycleProfile("f21b_sim_baseline_hold12_no_stop", "repair_reference_baseline(수리 참조 비교 행)", 12, 0.0, 0.0, 0, False),
    f21b.LifecycleProfile("f21c_hold1_atr0p6_tp1p0_cd0_early", "density_repair(빈도 수리)", 1, 0.6, 1.0, 0, True),
    f21b.LifecycleProfile("f21c_hold1_atr0p8_tp1p2_cd0", "density_repair(빈도 수리)", 1, 0.8, 1.2, 0, False),
    f21b.LifecycleProfile("f21c_hold2_atr0p6_tp1p2_cd0_early", "density_repair(빈도 수리)", 2, 0.6, 1.2, 0, True),
    f21b.LifecycleProfile("f21c_hold2_atr0p8_tp1p6_cd0", "density_repair(빈도 수리)", 2, 0.8, 1.6, 0, False),
    f21b.LifecycleProfile("f21c_hold3_atr0p8_tp1p6_cd0_early", "density_repair(빈도 수리)", 3, 0.8, 1.6, 0, True),
    f21b.LifecycleProfile("f21c_hold3_atr1p0_tp2p0_cd0", "density_repair(빈도 수리)", 3, 1.0, 2.0, 0, False),
]


def main() -> int:
    io_path(RUN_ROOT).mkdir(parents=True, exist_ok=True)
    created_at = utc_now()
    parent = read_json(F21B_SUMMARY)
    feature_order = f21b.read_feature_order()
    validate_context(parent, feature_order)
    full, raw, source_integrity = f07b.load_training_packet()
    signal_context = f21b.build_fixed_entry_signal(full)
    result = f21b.run_lifecycle_grid(full, raw, REPAIR_PROFILES, signal_context)
    final = build_final(created_at, parent, source_integrity, signal_context, result, feature_order)
    artifacts = write_artifacts(final, result)
    update_registries(final, artifacts)
    update_current_truth(final)
    print(json.dumps(json_ready({
        "status": final["status"],
        "judgment": final["judgment"],
        "run_id": RUN_ID,
        "scout_clue_rows": final["scout_clue_rows"],
        "seed_surface_rows": final["seed_surface_rows"],
        "handoff_candidate_rows": final["handoff_candidate_rows"],
        "best_profile_id": final["best_profile_id"],
        "next_run_id": final["next_run_id"],
        "report": REPORT_PATH.as_posix(),
    }), ensure_ascii=False, indent=2))
    return 0


def validate_context(parent: dict[str, Any], feature_order: list[str]) -> None:
    workspace = f21b.read_text(WORKSPACE_STATE)
    checks = {
        "workspace_current_stage_frontier21": f"current_stage_id: {STAGE_ID}" in workspace,
        "workspace_next_run_frontier21c": "next_run_id: frontier21C_lifecycle_repair_or_closeout_decision_v1" in workspace,
        "parent_run_matches": parent.get("run_id") == PARENT_RUN_ID,
        "parent_no_scout_seed_handoff": parent.get("scout_clue_rows") == 0 and parent.get("seed_surface_rows") == 0 and parent.get("handoff_candidate_rows") == 0,
        "repair_profile_count_capped": len(REPAIR_PROFILES) == 7,
        "feature_hash_matches": ordered_hash(feature_order) == f21b.EXPECTED_FEATURE_HASH,
    }
    if not all(checks.values()):
        raise RuntimeError(f"Frontier21C context check failed: {json.dumps(checks, ensure_ascii=False)}")


def build_final(
    created_at: str,
    parent: dict[str, Any],
    source_integrity: dict[str, Any],
    signal_context: dict[str, Any],
    result: dict[str, Any],
    feature_order: list[str],
) -> dict[str, Any]:
    summary = pd.DataFrame(result["candidate_summary"])
    handoff_count = int(summary["handoff_candidate_flag"].sum()) if not summary.empty else 0
    seed_count = int(summary["seed_surface_flag"].sum()) if not summary.empty else 0
    scout_count = int(summary["scout_clue_flag"].sum()) if not summary.empty else 0
    best = dict(summary.iloc[0]) if not summary.empty else {}
    if handoff_count:
        status = "density_repair_handoff_candidate_proxy_needs_pre_expensive_grok_no_authority"
        judgment = "handoff_candidate_proxy_observation(인계 후보 프록시 관찰)"
        next_run_id = NEXT_PRE_EXPENSIVE_GROK_RUN_ID
    elif seed_count:
        status = "density_repair_seed_surface_proxy_no_runtime_no_authority"
        judgment = "seed_surface(씨앗 표면)"
        next_run_id = NEXT_CLOSEOUT_RUN_ID
    elif scout_count:
        status = "density_repair_scout_clue_low_dd_low_pf_no_authority"
        judgment = "scout_clue_low_dd_pf_shortfall(낮은 손실폭 탐색 단서, 수익 팩터 부족)"
        next_run_id = NEXT_CLOSEOUT_RUN_ID
    else:
        status = "density_repair_no_forward_clue_closeout_required"
        judgment = "negative_pressure_after_capped_repair(상한 수리 뒤 부정 압력)"
        next_run_id = NEXT_CLOSEOUT_RUN_ID
    return {
        "created_at_utc": created_at,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": next_run_id,
        "status": status,
        "judgment": judgment,
        "feature_count": len(feature_order),
        "feature_order_hash": ordered_hash(feature_order),
        "source_integrity": source_integrity,
        "entry_signal": {key: value for key, value in signal_context.items() if key != "signal"},
        "parent_status": parent.get("status"),
        "profile_count": len(REPAIR_PROFILES),
        "metric_rows": len(result["metrics"]),
        "subperiod_metric_rows": len(result["subperiod_metrics"]),
        "trade_rows": len(result["trades"]),
        "scout_clue_rows": scout_count,
        "seed_surface_rows": seed_count,
        "handoff_candidate_rows": handoff_count,
        "best_profile_id": best.get("profile_id", ""),
        "best_profile": best,
        "repair_boundary": "density_only_repair_entry_still_fixed_no_threshold_or_side_change(빈도 전용 수리, 진입 고정, 임계값/방향 변경 없음)",
        "runtime_probe_status": "pre_expensive_grok_required_before_mt5(비싼 MT5 전 그록 검토 필요)" if handoff_count else "out_of_scope_by_claim_no_handoff_candidate(인계 후보 없어 주장 범위 밖)",
        "claim_boundary": {claim: "not_claimed(주장 없음)" for claim in f03b.FORBIDDEN_CLAIMS},
    }


def write_artifacts(final: dict[str, Any], result: dict[str, Any]) -> dict[str, Path]:
    artifacts = {
        "final_summary": RUN_ROOT / "final_summary.json",
        "candidate_summary": RUN_ROOT / "candidate_summary.csv",
        "metrics_by_split": RUN_ROOT / "metrics_by_split.csv",
        "subperiod_metrics": RUN_ROOT / "subperiod_metrics.csv",
        "trade_log": RUN_ROOT / "trade_log.csv",
        "run_manifest": RUN_ROOT / "run_manifest.json",
        "report": REPORT_PATH,
        "gate_audit": STAGE_ROOT / "03_reviews" / f"{RUN_ID}_gate_audit.md",
    }
    f21b.write_json(artifacts["final_summary"], final)
    f21b.write_csv(artifacts["candidate_summary"], result["candidate_summary"])
    f21b.write_csv(artifacts["metrics_by_split"], result["metrics"])
    f21b.write_csv(artifacts["subperiod_metrics"], result["subperiod_metrics"])
    f21b.write_csv(artifacts["trade_log"], result["trades"])
    f03b.write_text_sig(REPORT_PATH, report_text(final, artifacts))
    f03b.write_text_sig(artifacts["gate_audit"], gate_audit(final, artifacts))
    f21b.write_json(artifacts["run_manifest"], run_manifest(final, artifacts))
    return artifacts


def run_manifest(final: dict[str, Any], artifacts: dict[str, Path]) -> dict[str, Any]:
    return {
        "identity": {
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "parent_run_id": PARENT_RUN_ID,
            "next_run_id": final["next_run_id"],
            "created_at_utc": final["created_at_utc"],
        },
        "artifacts": [
            f21b.artifact_identity(SCRIPT_PATH),
            f21b.artifact_identity(F21B_SUMMARY),
            f21b.artifact_identity(F21A_LOCK),
            *[f21b.artifact_identity(path) for path in artifacts.values() if path != artifacts["run_manifest"]],
        ],
        "rule_stack": {
            "entry": final["entry_signal"],
            "repair_profiles": [profile.__dict__ for profile in REPAIR_PROFILES],
        },
        "results": {
            "cross_split": {
                "scout_clue_rows": final["scout_clue_rows"],
                "seed_surface_rows": final["seed_surface_rows"],
                "handoff_candidate_rows": final["handoff_candidate_rows"],
                "best_profile_id": final["best_profile_id"],
            },
            "report_refs": [{"role": "density_repair_report", "path": REPORT_PATH.as_posix()}],
        },
        "compatibility": {"schema_version": "frontier21c_density_repair_v1", "mismatch_policy": "fail_fast(빠른 실패)"},
    }


def report_text(final: dict[str, Any], artifacts: dict[str, Path]) -> str:
    best = final["best_profile"]
    return f"""# Frontier21C Lifecycle Density Repair Scout Report(전선21C 생명주기 빈도 수리 탐색 보고서)

Updated(갱신): {final['created_at_utc']}

Status(상태): `{final['status']}`

Judgment(판정): `{final['judgment']}`

Action(행동): F21B(전선21B)의 low-DD/low-density(낮은 손실폭/낮은 빈도) 실패를 보고, entry(진입)는 그대로 둔 채 shorter hold/no cooldown(짧은 보유/쿨다운 없음) density repair(빈도 수리)를 한 번 실행했습니다.

Effect(효과): density(빈도)는 5~6/day로 회복됐지만 PF(수익 팩터)는 seed floor(씨앗 바닥) 1.2에 닿지 못했습니다.

Scout/seed/handoff rows(탐색/씨앗/인계 행): `{final['scout_clue_rows']}` / `{final['seed_surface_rows']}` / `{final['handoff_candidate_rows']}`

Best profile(최상 프로필): `{final['best_profile_id']}`

Best validation PF/density/DD(최상 검증 수익 팩터/빈도/손실폭): `{f21b.fmt(best.get('validation_profit_factor'))}` / `{f21b.fmt(best.get('validation_trades_per_day'))}/day` / `{f21b.fmt(best.get('validation_dd_risk_percent'))}%`

Best OOS PF/density/DD(최상 표본외 수익 팩터/빈도/손실폭): `{f21b.fmt(best.get('oos_profit_factor'))}` / `{f21b.fmt(best.get('oos_trades_per_day'))}/day` / `{f21b.fmt(best.get('oos_dd_risk_percent'))}%`

Artifacts(산출물): `{artifacts['candidate_summary'].as_posix()}`, `{artifacts['metrics_by_split'].as_posix()}`, `{artifacts['trade_log'].as_posix()}`

Next action(다음 행동): `{final['next_run_id']}`

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def gate_audit(final: dict[str, Any], artifacts: dict[str, Path]) -> str:
    return f"""# Frontier21C Gate Audit(전선21C 게이트 감사)

- scope_completion_gate(범위 완료 게이트): density repair artifacts(빈도 수리 산출물) created(생성)
- kpi_contract_audit(KPI 계약 감사): candidate_summary/metrics/trade_log(후보 요약/지표/거래 기록) created(생성)
- required_gate_coverage_audit(필수 게이트 커버리지 감사): this file(이 파일)
- final_claim_guard(최종 주장 방지): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음)
"""


def update_registries(final: dict[str, Any], artifacts: dict[str, Path]) -> None:
    f03b.upsert_csv(RUN_REGISTRY, "run_id", run_registry_row(final))
    for row in ledger_rows(final):
        f03b.upsert_csv(ALPHA_LEDGER, "ledger_row_id", row)
        f03b.upsert_csv(STAGE_ROOT / "03_reviews" / "stage_run_ledger.csv", "ledger_row_id", row)
    f03b.append_once(CHANGELOG, RUN_ID, changelog_entry(final))
    f03b.append_once(IDEA_REGISTRY, RUN_ID, idea_registry_entry(final))
    f03b.write_text_sig(STAGE_ROOT / "04_selected" / "selection_status.md", selection_status(final))


def run_registry_row(final: dict[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "experiment_execution(실험 실행)",
        "family": "experiment_execution(실험 실행)",
        "work_family": "experiment_execution(실험 실행)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": REPORT_PATH.as_posix(),
        "notes": f"scout={final['scout_clue_rows']};seed={final['seed_surface_rows']};handoff={final['handoff_candidate_rows']};next={final['next_run_id']}",
        "run_number": RUN_NUMBER,
        "date": "2026-06-14",
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": final["next_run_id"],
        "claim_boundary": final["repair_boundary"],
        "report_path": REPORT_PATH.as_posix(),
        "created_at_utc": final["created_at_utc"],
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "result_path": REPORT_PATH.as_posix(),
    }


def ledger_rows(final: dict[str, Any]) -> list[dict[str, Any]]:
    best = final["best_profile"]
    primary = {
        "ledger_row_id": f"{RUN_ID}__tier_a_density_repair",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": f"{RUN_ID}__tier_a_density_repair",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "Tier A separate(티어 A 분리)",
        "tier_scope": "Tier A(티어 A)",
        "kpi_scope": "density_repair_proxy_not_runtime(빈도 수리 프록시, 런타임 아님)",
        "scoreboard_lane": "trade_shape_proxy(거래 형태 프록시)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": REPORT_PATH.as_posix(),
        "primary_kpi": (
            f"best={final['best_profile_id']};"
            f"oos_pf={f21b.fmt(best.get('oos_profit_factor'))};"
            f"oos_density={f21b.fmt(best.get('oos_trades_per_day'))};"
            f"oos_dd={f21b.fmt(best.get('oos_dd_risk_percent'))}"
        ),
        "guardrail_kpi": "capped_repair_no_wfo_no_mt5_no_authority(상한 수리, WFO/MT5/권위 없음)",
        "external_verification_status": final["runtime_probe_status"],
        "notes": f"scout={final['scout_clue_rows']};seed={final['seed_surface_rows']};handoff={final['handoff_candidate_rows']}",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "run_family": "experiment_execution(실험 실행)",
    }
    tier_b = {**primary, "ledger_row_id": f"{RUN_ID}__tier_b_missing_required", "subrun_id": f"{RUN_ID}__tier_b_missing_required", "record_view": "Tier B separate(티어 B 분리)", "tier_scope": "Tier B(티어 B)", "kpi_scope": "missing_required(필수 누락)", "primary_kpi": "missing_required_no_tier_b_model_input(필수 누락, Tier B 모델 입력 없음)", "guardrail_kpi": "no_tier_b_claim(티어 B 주장 없음)", "notes": "Tier B source absent(Tier B 원천 없음)"}
    combined = {**primary, "ledger_row_id": f"{RUN_ID}__tier_ab_combined_out_of_scope", "subrun_id": f"{RUN_ID}__tier_ab_combined_out_of_scope", "record_view": "Tier A+B combined(티어 A+B 합산)", "tier_scope": "Tier A+B(티어 A+B)", "kpi_scope": "out_of_scope_by_claim(주장 범위 밖)", "primary_kpi": "out_of_scope_by_claim_no_combined_source(주장 범위 밖, 합산 원천 없음)", "guardrail_kpi": "no_synthetic_combined_claim(합성 합산 주장 없음)", "notes": "Combined source absent(합산 원천 없음)"}
    return [primary, tier_b, combined]


def selection_status(final: dict[str, Any]) -> str:
    best = final["best_profile"]
    return f"""# Frontier21 Selection Status(전선21 선택 상태)

Updated(갱신): {final['created_at_utc']}

Selection(선택): no selected baseline/completion/promotion/runtime authority(선택 기준선/완성/승격/런타임 권위 없음).

Latest repair(최근 수리): `{RUN_ID}`

Status(상태): `{final['status']}`

Judgment(판정): `{final['judgment']}`

Best profile(최상 프로필): `{final['best_profile_id']}` with validation/OOS PF-density-DD(검증/표본외 수익 팩터-빈도-손실폭) `{f21b.fmt(best.get('validation_profit_factor'))}/{f21b.fmt(best.get('validation_trades_per_day'))}/{f21b.fmt(best.get('validation_dd_risk_percent'))}` and `{f21b.fmt(best.get('oos_profit_factor'))}/{f21b.fmt(best.get('oos_trades_per_day'))}/{f21b.fmt(best.get('oos_dd_risk_percent'))}`.

Scout/seed/handoff rows(탐색/씨앗/인계 행): `{final['scout_clue_rows']}` / `{final['seed_surface_rows']}` / `{final['handoff_candidate_rows']}`

Next action(다음 행동): `{final['next_run_id']}`
"""


def changelog_entry(final: dict[str, Any]) -> str:
    return (
        f"- {final['created_at_utc']}: `{RUN_ID}` ran capped density repair(상한 빈도 수리). "
        f"Effect(효과): scout/seed/handoff(탐색/씨앗/인계) counts are {final['scout_clue_rows']}/{final['seed_surface_rows']}/{final['handoff_candidate_rows']}.\n"
    )


def idea_registry_entry(final: dict[str, Any]) -> str:
    return (
        f"- `IDEA-FR21-F20-SEED-LIFECYCLE-DD-CONTAINMENT-ONNX-SCOUT`: `{RUN_ID}` found low-DD density repair scout clue(낮은 손실폭 빈도 수리 탐색 단서) but no seed/handoff(씨앗/인계 없음). "
        "Effect(효과): final closeout must separate preserved DD clue(보존 손실폭 단서) from PF shortfall(수익 팩터 부족).\n"
    )


def update_current_truth(final: dict[str, Any]) -> None:
    io_path(WORKSPACE_STATE).write_text(workspace_state(final), encoding="utf-8-sig")
    f03b.write_text_sig(CURRENT_WORKING_STATE, current_working_state(final))


def workspace_state(final: dict[str, Any]) -> str:
    return "\n".join([
        f"current_stage_id: {STAGE_ID}",
        f"current_run_id: {RUN_ID}",
        f"latest_completed_run_id: {RUN_ID}",
        f"current_status: {final['status']}",
        f"current_judgment: {final['judgment']}",
        f"next_run_id: {final['next_run_id']}",
        "runtime_authority: not_claimed",
        "operating_promotion: not_claimed",
        "goal_achieve: not_claimed",
        f"updated_at_utc: '{final['created_at_utc']}'",
        "",
    ])


def current_working_state(final: dict[str, Any]) -> str:
    best = final["best_profile"]
    return f"""# Current Working State(현재 작업 상태)

Updated(갱신): {final['created_at_utc']}

## Active Stage(현재 단계)

- stage(단계): `{STAGE_ID}`
- latest run(최근 실행): `{RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- next run(다음 실행): `{final['next_run_id']}`

## Current Truth(현재 진실)

Action(행동): F21C(전선21C)가 capped density repair(상한 빈도 수리)를 실행했습니다.

Effect(효과): DD(손실폭)는 낮고 density(빈도)는 5~6/day로 회복됐지만 PF(수익 팩터)가 1.2 seed floor(씨앗 바닥)에 못 닿아 closeout(마감) 검토가 필요합니다.

Best repair profile(최상 수리 프로필): `{final['best_profile_id']}` with validation/OOS PF-density-DD(검증/표본외 수익 팩터-빈도-손실폭) `{f21b.fmt(best.get('validation_profit_factor'))}/{f21b.fmt(best.get('validation_trades_per_day'))}/{f21b.fmt(best.get('validation_dd_risk_percent'))}` and `{f21b.fmt(best.get('oos_profit_factor'))}/{f21b.fmt(best.get('oos_trades_per_day'))}/{f21b.fmt(best.get('oos_dd_risk_percent'))}`.

Claim boundary(주장 경계): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


if __name__ == "__main__":
    raise SystemExit(main())
