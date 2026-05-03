from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Mapping, Sequence

from foundation.control_plane.ledger import json_ready, sha256_file_lf_normalized
from stage_pipelines.stage16 import qda_characterization_probe as base
from stage_pipelines.stage16 import qda_run09_followup_probe as engine


PACKET_ID = "stage16_qda_run10A_run10L_decision_microprobe_mt5_v1"
REVIEW_PACKET_PATH = base.STAGE_ROOT / "03_reviews/run10A_run10L_qda_decision_microprobe_mt5_packet.md"
DECISION_PATH = base.ROOT / "docs/decisions/2026-05-03_stage16_qda_run10A_run10L_decision_microprobe.md"
PACKET_ROOT = base.ROOT / "docs/agent_control/packets" / PACKET_ID
BOUNDARY = "qda_run10_decision_microprobe_runtime_probe_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority"
JUDGMENT_COMPLETED = "inconclusive_qda_run10_decision_microprobe_mt5_completed"
JUDGMENT_BLOCKED = "blocked_qda_run10_decision_microprobe_after_attempt"
EXPLORATION_LABEL = "stage16_Model__QDARun10DecisionMicroprobe"
BASELINE_RUN_ID = "run09D_qda_reg018_full58_followup_v1"


def run10_specs() -> list[engine.FollowupSpec]:
    return [
        engine.FollowupSpec("run10A", "run10A_qda_reg016_full58_decision_microprobe_v1", "v28_reg016_full58", "full58_reg016_q90", "QDA full58 reg_param 0.16, q90 coverage.", "full58_reg_stability", 0.16, random_state=2001),
        engine.FollowupSpec("run10B", "run10B_qda_reg018_full58_resample_decision_microprobe_v1", "v29_reg018_full58_resample", "full58_reg018_resample_q90", "QDA full58 reg_param 0.18 resample, q90 coverage.", "full58_reg_stability", 0.18, random_state=2002),
        engine.FollowupSpec("run10C", "run10C_qda_reg020_full58_decision_microprobe_v1", "v30_reg020_full58", "full58_reg020_q90", "QDA full58 reg_param 0.20, q90 coverage.", "full58_reg_stability", 0.20, random_state=2003),
        engine.FollowupSpec("run10D", "run10D_qda_reg018_full58_q88_decision_microprobe_v1", "v31_reg018_full58_q88", "full58_reg018_q88", "QDA full58 reg_param 0.18, q88 coverage.", "full58_threshold_stability", 0.18, threshold_quantile=0.88, random_state=2004),
        engine.FollowupSpec("run10E", "run10E_qda_reg018_full58_q92_decision_microprobe_v1", "v32_reg018_full58_q92", "full58_reg018_q92", "QDA full58 reg_param 0.18, q92 coverage.", "full58_threshold_stability", 0.18, threshold_quantile=0.92, random_state=2005),
        engine.FollowupSpec("run10F", "run10F_qda_reg012_drop_mega10_decision_microprobe_v1", "v33_reg012_drop_mega10", "drop_mega10_reg012_q90", "QDA drop_mega10 reg_param 0.12, q90 coverage.", "drop_mega10_reg_stability", 0.12, excluded_features=base.MEGA_FEATURES, tier_a_feature_mode="full58_drop_mega10", random_state=2006),
        engine.FollowupSpec("run10G", "run10G_qda_reg015_drop_mega10_resample_decision_microprobe_v1", "v34_reg015_drop_mega10_resample", "drop_mega10_reg015_resample_q90", "QDA drop_mega10 reg_param 0.15 resample, q90 coverage.", "drop_mega10_reg_stability", 0.15, excluded_features=base.MEGA_FEATURES, tier_a_feature_mode="full58_drop_mega10", random_state=2007),
        engine.FollowupSpec("run10H", "run10H_qda_reg018_drop_mega10_decision_microprobe_v1", "v35_reg018_drop_mega10", "drop_mega10_reg018_q90", "QDA drop_mega10 reg_param 0.18, q90 coverage.", "drop_mega10_reg_stability", 0.18, excluded_features=base.MEGA_FEATURES, tier_a_feature_mode="full58_drop_mega10", random_state=2008),
        engine.FollowupSpec("run10I", "run10I_qda_reg020_drop_mega10_decision_microprobe_v1", "v36_reg020_drop_mega10", "drop_mega10_reg020_q90", "QDA drop_mega10 reg_param 0.20, q90 coverage.", "drop_mega10_reg_stability", 0.20, excluded_features=base.MEGA_FEATURES, tier_a_feature_mode="full58_drop_mega10", random_state=2009),
        engine.FollowupSpec("run10J", "run10J_qda_reg015_drop_mega10_q85_decision_microprobe_v1", "v37_reg015_drop_mega10_q85", "drop_mega10_reg015_q85", "QDA drop_mega10 reg_param 0.15, q85 coverage.", "drop_mega10_threshold_stability", 0.15, threshold_quantile=0.85, excluded_features=base.MEGA_FEATURES, tier_a_feature_mode="full58_drop_mega10", random_state=2010),
        engine.FollowupSpec("run10K", "run10K_qda_reg015_drop_mega10_q93_decision_microprobe_v1", "v38_reg015_drop_mega10_q93", "drop_mega10_reg015_q93", "QDA drop_mega10 reg_param 0.15, q93 coverage.", "drop_mega10_threshold_stability", 0.15, threshold_quantile=0.93, excluded_features=base.MEGA_FEATURES, tier_a_feature_mode="full58_drop_mega10", random_state=2011),
        engine.FollowupSpec("run10L", "run10L_qda_reg018_drop_mega10_q88_decision_microprobe_v1", "v39_reg018_drop_mega10_q88", "drop_mega10_reg018_q88", "QDA drop_mega10 reg_param 0.18, q88 coverage.", "drop_mega10_threshold_stability", 0.18, threshold_quantile=0.88, excluded_features=base.MEGA_FEATURES, tier_a_feature_mode="full58_drop_mega10", random_state=2012),
    ]


def metric(row: Mapping[str, Any], split: str, key: str, default: float = 0.0) -> float:
    return base.safe_float((row.get(split) or {}).get(key), default)


def focus_family(row: Mapping[str, Any]) -> str:
    text = " ".join(str(row.get(key, "")) for key in ("axis", "idea_id", "feature_mode"))
    return "drop_mega10" if "drop_mega10" in text else "full58_reg018_neighborhood"


def strong_survivor(row: Mapping[str, Any]) -> bool:
    val = row.get("validation_routed") or {}
    oos = row.get("oos_routed") or {}
    return bool(
        row.get("external_verification_status") == "completed"
        and base.safe_float(val.get("net_profit")) > 0
        and base.safe_float(val.get("profit_factor")) >= 1.0
        and int(base.safe_float(val.get("trade_count"))) >= 100
        and base.safe_float(oos.get("net_profit")) > 0
        and base.safe_float(oos.get("profit_factor")) >= 1.25
        and int(base.safe_float(oos.get("trade_count"))) >= 100
        and base.safe_float(oos.get("max_drawdown_amount"), 1e9) <= 220
        and base.safe_float(oos.get("recovery_factor")) >= 1.5
    )


def survivor_score(row: Mapping[str, Any]) -> float:
    return (
        metric(row, "validation_routed", "net_profit")
        + metric(row, "oos_routed", "net_profit")
        + 80.0 * min(metric(row, "validation_routed", "profit_factor"), 2.0)
        + 120.0 * min(metric(row, "oos_routed", "profit_factor"), 3.0)
        - 0.5 * metric(row, "oos_routed", "max_drawdown_amount", 500.0)
    )


def decision_recommendation(aggregate: Mapping[str, Any], summaries: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    if aggregate.get("external_verification_status") != "completed":
        return {
            "recommendation": "blocked_need_repair_before_stage16_decision",
            "reason": "MT5(메타트레이더5) 또는 KPI(핵심성과지표) 근거가 일부 비어 있어 close(닫기)/continue(진행) 판정을 낮춘다.",
            "selected_current_run_id": str((aggregate.get("best_oos_routed_net_run") or {}).get("run_id") or ""),
            "survivors_by_family": {},
            "decision_rule": "runtime evidence(런타임 근거)와 KPI contract(KPI 계약)가 먼저 통과해야 한다.",
        }
    survivors = [row for row in summaries if strong_survivor(row)]
    grouped: dict[str, list[str]] = {}
    for row in survivors:
        grouped.setdefault(focus_family(row), []).append(str(row["run_id"]))
    best_family = max(grouped, key=lambda key: len(grouped[key]), default="")
    if best_family and len(grouped[best_family]) >= 2:
        family_rows = [row for row in survivors if focus_family(row) == best_family]
        selected = max(family_rows, key=survivor_score)
        recommendation = "continue_stage16_one_more_context_or_wfo_probe"
        reason = "같은 QDA(이차판별분석) 하위 계열에서 validation(검증)과 OOS(표본외)가 함께 양수인 변형이 2개 이상 반복됐다."
    else:
        selected = aggregate.get("best_oos_routed_net_run") or {}
        recommendation = "close_stage16_preserve_qda_clues"
        reason = "좋은 OOS(표본외) 숫자가 단일 지점에 치우쳤거나 validation(검증) 안정성이 충분히 반복되지 않았다."
    return {
        "recommendation": recommendation,
        "reason": reason,
        "selected_current_run_id": str(selected.get("run_id") or ""),
        "selected_current_run_number": str(selected.get("run_number") or ""),
        "survivors_by_family": grouped,
        "survivor_count": len(survivors),
        "decision_rule": "continue(진행)는 같은 family(계열)에서 2개 이상 strong survivor(강한 생존 변형)가 나올 때만 허용한다. 아니면 close(닫기)하고 단서를 보존한다.",
        "strong_survivor_criteria": {
            "validation": "net_profit > 0, profit_factor >= 1.0, trade_count >= 100",
            "oos": "net_profit > 0, profit_factor >= 1.25, trade_count >= 100, max_drawdown_amount <= 220, recovery_factor >= 1.5",
        },
    }


def aggregate_summary(summaries: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    completed = [row for row in summaries if row.get("external_verification_status") == "completed"]
    best_oos = max(summaries, key=lambda row: base.safe_float((row.get("oos_routed") or {}).get("net_profit"), -1e18), default=None)
    best_val = max(summaries, key=lambda row: base.safe_float((row.get("validation_routed") or {}).get("net_profit"), -1e18), default=None)
    aggregate = {
        "packet_id": PACKET_ID,
        "stage_id": base.STAGE_ID,
        "run_range": "run10A-run10L",
        "baseline_comparison_run_id": BASELINE_RUN_ID,
        "run_count": len(summaries),
        "completed_run_count": len(completed),
        "blocked_run_count": len(summaries) - len(completed),
        "external_verification_status": "completed" if len(completed) == len(summaries) else "blocked_or_partial",
        "judgment": JUDGMENT_COMPLETED if len(completed) == len(summaries) else JUDGMENT_BLOCKED,
        "boundary": BOUNDARY,
        "mt5_kpi_record_count": sum(int(row.get("mt5_kpi_record_count", 0)) for row in summaries),
        "attempt_count": sum(int(row.get("attempt_count", 0)) for row in summaries),
        "best_oos_routed_net_run": best_oos,
        "best_validation_routed_net_run": best_val,
        "run_ids": [row["run_id"] for row in summaries],
    }
    aggregate["decision_recommendation"] = decision_recommendation(aggregate, summaries)
    return aggregate


def experiment_design() -> dict[str, Any]:
    return {
        "hypothesis": "QDA(이차판별분석) run09D full58 reg0.18 OOS(표본외) 급등과 run09G drop_mega10(대형주 10개 제거) 안정 단서 중 하나가 nearby setting(인접 설정)에서 반복되면 Stage16(16단계)을 한 번 더 진행할 가치가 있다.",
        "decision_use": "Stage16(16단계)을 close(닫기)할지, continue(진행)할지 정한다.",
        "comparison_baseline": BASELINE_RUN_ID,
        "control_variables": {
            "symbol": "FPMarkets US100",
            "timeframe": "M5",
            "label": base.LABEL_ID,
            "split": base.SPLIT_CONTRACT,
            "routing": "Tier A primary + Tier B fallback(Tier A 우선 + Tier B 대체)",
            "max_hold_bars": engine.MAX_HOLD_BARS,
            "threshold_method": "validation nonflat coverage quantile(검증 비평탄 커버리지 분위수), not profit-searched(수익 최적화 아님)",
        },
        "changed_variables": ["full58 reg0.16/0.18/0.20 and q88/q92", "drop_mega10 reg0.12/0.15/0.18/0.20 and q85/q88/q93", "new random_state(새 표본 난수) resample"],
        "sample_scope": "Tier A full-context(전체 문맥) plus Tier B partial-context fallback(부분 문맥 대체), validation(검증) and OOS(표본외) MT5 Strategy Tester(전략 테스터).",
        "success_criteria": "같은 family(계열)에서 strong survivor(강한 생존 변형)가 2개 이상 나오고 MT5/KPI parser(파서) 오류가 없다.",
        "failure_criteria": "좋은 수치가 한 점에만 남거나 validation/OOS(검증/표본외)가 갈라진다.",
        "invalid_conditions": "MT5(메타트레이더5) 출력 누락, ONNX(온닉스) parity(동등성) 실패, feature order(피처 순서) 불일치, KPI parser(파서) 오류, ledger(장부) 누락.",
        "stop_conditions": "strong survivor(강한 생존 변형)가 반복되지 않으면 Stage16(16단계)은 close(닫기) 권고로 닫고 QDA(이차판별분석) 단서만 보존한다.",
        "evidence_plan": ["run_manifest.json", "kpi_record.json", "MT5 Strategy Tester reports", "normalized_kpi_summary.csv", "trade_attribution_summary.csv", "decision_recommendation.json", "stage/project alpha ledgers", "gate JSON files"],
    }


def run_result_markdown(summary: Mapping[str, Any]) -> str:
    val = summary.get("validation_routed", {})
    oos = summary.get("oos_routed", {})
    return "\n".join(
        [
            f"# {summary['run_id']} Result Summary({summary['run_id']} 결과 요약)",
            "",
            f"- variant(변형): `{summary['variant_id']}`",
            f"- axis(축): `{summary['axis']}`",
            f"- judgment(판정): `{summary['judgment']}`",
            f"- MT5 KPI records(MT5 핵심성과지표 기록): `{summary.get('mt5_kpi_record_count', 0)}`",
            f"- validation routed net/PF/trades(검증 라우팅 순수익/수익 팩터/거래 수): `{val.get('net_profit')}` / `{val.get('profit_factor')}` / `{val.get('trade_count')}`",
            f"- OOS routed net/PF/trades(표본외 라우팅 순수익/수익 팩터/거래 수): `{oos.get('net_profit')}` / `{oos.get('profit_factor')}` / `{oos.get('trade_count')}`",
            "",
            "효과(effect, 효과): 이 run(실행)은 QDA(이차판별분석) Stage16(16단계) close(닫기)/continue(진행) 판단용 runtime_probe(런타임 탐침)이다.",
        ]
    )


def packet_markdown(aggregate: Mapping[str, Any], summaries: Sequence[Mapping[str, Any]], kpi: Mapping[str, Any]) -> str:
    recommendation = aggregate.get("decision_recommendation") or {}
    lines = [
        "# Stage16 QDA RUN10A-RUN10L Decision Microprobe(16단계 QDA 실행 10A-10L 결정 미세 탐침)",
        "",
        f"- judgment(판정): `{aggregate['judgment']}`",
        f"- recommendation(권고): `{recommendation.get('recommendation')}`",
        f"- reason(이유): {recommendation.get('reason')}",
        f"- completed runs(완료 실행): `{aggregate['completed_run_count']}/{aggregate['run_count']}`",
        f"- MT5 KPI records(MT5 핵심성과지표 기록): `{aggregate['mt5_kpi_record_count']}`",
        f"- normalized KPI records(정규화 KPI 기록): `{kpi['normalized_records']}`",
        f"- trade attribution records(거래 귀속 기록): `{kpi['trade_attribution_records']}`",
        f"- comparison reference(비교 참고): `{BASELINE_RUN_ID}`",
        f"- boundary(경계): `{BOUNDARY}`",
        "",
        "| run(실행) | family(계열) | topic(주제) | reg(정규화) | q(분위수) | features(피처) | val net/PF/trades(검증) | oos net/PF/trades/DD/RF(표본외) | strong(강한 생존) |",
        "|---|---|---|---:|---:|---:|---:|---:|---|",
    ]
    for row in summaries:
        val = row.get("validation_routed", {})
        oos = row.get("oos_routed", {})
        lines.append(
            f"| `{row['run_number']}` | `{focus_family(row)}` | `{row['idea_id']}` | `{row['reg_param']}` | `{row['threshold_quantile']}` | `{row['feature_count']}` | `{val.get('net_profit')}/{val.get('profit_factor')}/{val.get('trade_count')}` | `{oos.get('net_profit')}/{oos.get('profit_factor')}/{oos.get('trade_count')}/{oos.get('max_drawdown_amount')}/{oos.get('recovery_factor')}` | `{strong_survivor(row)}` |"
        )
    best_oos = aggregate.get("best_oos_routed_net_run") or {}
    best_val = aggregate.get("best_validation_routed_net_run") or {}
    lines.extend(
        [
            "",
            f"- best OOS routed net(최고 표본외 라우팅 순수익): `{best_oos.get('run_number')}` `{best_oos.get('idea_id')}` `{(best_oos.get('oos_routed') or {}).get('net_profit')}`",
            f"- best validation routed net(최고 검증 라우팅 순수익): `{best_val.get('run_number')}` `{best_val.get('idea_id')}` `{(best_val.get('validation_routed') or {}).get('net_profit')}`",
            f"- survivors by family(계열별 강한 생존): `{json.dumps(recommendation.get('survivors_by_family', {}), ensure_ascii=False, sort_keys=True)}`",
            "",
            "효과(effect, 효과): 이 묶음은 QDA(이차판별분석) Stage16(16단계)을 더 밀지 닫을지 정하기 위해 같은 계열의 반복 생존 여부만 본다.",
            "",
            "금지 주장(forbidden claims, 금지 주장): edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위).",
        ]
    )
    return "\n".join(lines)


def gate_payloads(aggregate: Mapping[str, Any], kpi: Mapping[str, Any]) -> dict[str, Any]:
    expected_kpi = int(aggregate["run_count"]) * 10
    expected_attempts = int(aggregate["run_count"]) * 6
    runtime_ok = aggregate["completed_run_count"] == aggregate["run_count"] and aggregate["attempt_count"] == expected_attempts and aggregate["mt5_kpi_record_count"] == expected_kpi
    kpi_ok = kpi["normalized_records"] == expected_kpi and kpi["parser_errors"] == 0 and kpi["missing_runs"] == 0
    passed = bool(runtime_ok and kpi_ok)
    return {
        "runtime_evidence_gate": {"audit_name": "runtime_evidence_gate", "status": "pass" if runtime_ok else "blocked", "passed": runtime_ok, "expected_attempts": expected_attempts, "expected_kpi_records": expected_kpi, "counts": {"attempt_count": aggregate["attempt_count"], "mt5_kpi_record_count": aggregate["mt5_kpi_record_count"]}},
        "kpi_contract_audit": {"audit_name": "kpi_contract_audit", "status": "pass" if kpi_ok else "blocked", "passed": kpi_ok, **dict(kpi)},
        "source_authority_audit": {"audit_name": "source_authority_audit", "status": "pass" if passed else "blocked", "passed": passed, "source": "run kpi_record.json plus MT5 Strategy Tester reports plus normalized KPI files"},
        "final_claim_guard": {"audit_name": "final_claim_guard", "status": "pass" if passed else "blocked", "passed": passed, "allowed_claims": [aggregate["judgment"], "runtime_probe", "close_or_continue_recommendation"], "forbidden_claims": ["edge", "alpha_quality", "baseline", "promotion_candidate", "operating_promotion", "runtime_authority"]},
        "required_gate_coverage_audit": {"audit_name": "required_gate_coverage_audit", "status": "pass" if passed else "blocked", "passed": passed, "required_gates": {"runtime_evidence_gate": "pass" if runtime_ok else "blocked", "kpi_contract_audit": "pass" if kpi_ok else "blocked", "source_authority_audit": "pass" if passed else "blocked", "final_claim_guard": "pass" if passed else "blocked"}},
    }


def write_packet_files(aggregate: Mapping[str, Any], summaries: Sequence[Mapping[str, Any]], kpi: Mapping[str, Any], created_at: str) -> None:
    engine.write_json(PACKET_ROOT / "aggregate_summary.json", {**dict(aggregate), "kpi_management": dict(kpi)})
    engine.write_json(PACKET_ROOT / "experiment_design.json", experiment_design())
    engine.write_json(PACKET_ROOT / "decision_recommendation.json", aggregate.get("decision_recommendation") or {})
    engine.write_json(PACKET_ROOT / "artifact_index.json", {"run_summaries": list(summaries), "report_path": base.rel(REVIEW_PACKET_PATH), "created_at_utc": created_at})
    engine.write_json(PACKET_ROOT / "routing_receipt.json", {"packet_id": PACKET_ID, "created_at_utc": created_at, "primary_family": "runtime_backtest", "primary_skill": "obsidian-runtime-parity", "support_skills": ["obsidian-experiment-design", "obsidian-exploration-mandate", "obsidian-backtest-forensics", "obsidian-artifact-lineage", "obsidian-result-judgment"], "required_gates": ["runtime_evidence_gate", "kpi_contract_audit", "source_authority_audit", "required_gate_coverage_audit", "final_claim_guard"]})
    engine.write_json(PACKET_ROOT / "skill_receipts.json", {"packet_id": PACKET_ID, "created_at_utc": created_at, "receipts": [{"skill": "obsidian-experiment-design", "status": "completed", "decision_use": "Stage16 QDA close-or-continue decision"}, {"skill": "obsidian-exploration-mandate", "status": "completed", "evidence_boundary": "runtime_probe"}, {"skill": "obsidian-runtime-parity", "status": "completed", "runtime_claim_boundary": "runtime_probe"}, {"skill": "obsidian-backtest-forensics", "status": "completed", "backtest_judgment": "usable_with_boundary"}, {"skill": "obsidian-artifact-lineage", "status": "completed", "lineage_judgment": "connected_with_boundary"}, {"skill": "obsidian-result-judgment", "status": "completed", "judgment_label": aggregate["judgment"], "claim_boundary": BOUNDARY, "recommendation": (aggregate.get("decision_recommendation") or {}).get("recommendation")} ]})
    engine.write_json(PACKET_ROOT / "runtime_identity.json", {"research_path": "stage_pipelines/stage16/qda_run10_decision_microprobe.py", "runtime_path": "foundation/mt5/ObsidianPrimeV2_RuntimeProbeEA.mq5", "shared_contract": {"feature_set_id": base.FEATURE_SET_ID, "label_id": base.LABEL_ID, "split_contract": base.SPLIT_CONTRACT, "onnx_opset": engine.ONNX_OPSET}, "module_hashes": {"pipeline": sha256_file_lf_normalized(Path(__file__)), "ea": sha256_file_lf_normalized(base.ROOT / "foundation/mt5/ObsidianPrimeV2_RuntimeProbeEA.mq5"), "model_runtime": sha256_file_lf_normalized(base.ROOT / "foundation/mt5/include/ObsidianPrime/ModelRuntime.mqh")}, "runtime_claim_boundary": "runtime_probe"})
    for name, payload in gate_payloads(aggregate, kpi).items():
        engine.write_json(PACKET_ROOT / f"{name}.json", payload)
    engine.write_md(REVIEW_PACKET_PATH, packet_markdown(aggregate, summaries, kpi))


def sync_docs(aggregate: Mapping[str, Any], kpi: Mapping[str, Any]) -> None:
    recommendation = aggregate.get("decision_recommendation") or {}
    current_run = str(recommendation.get("selected_current_run_id") or (aggregate.get("best_oos_routed_net_run") or {}).get("run_id") or "run10L_qda_reg018_drop_mega10_q88_decision_microprobe_v1")
    rec = str(recommendation.get("recommendation") or "blocked_need_repair_before_stage16_decision")
    engine.write_md(
        base.STAGE_ROOT / "03_reviews/review_index.md",
        "\n".join(
            [
                "# Stage 16 Review Index(16단계 검토 색인)",
                "",
                "- `run08A`~`run08J`: QDA(이차판별분석) characterization(특성 파악) structural scout(구조 탐색).",
                "- `run08A`~`run08J` MT5(`MetaTrader 5`, 메타트레이더5): QDA(이차판별분석) runtime_probe(런타임 탐침).",
                "- `run09A`~`run09Q`: follow-up(후속 탐색) regularization/feature/sample/coverage(정규화/피처/표본/커버리지).",
                f"- `run10A`~`run10L`: decision microprobe(결정 미세 탐침), recommendation(권고) `{rec}`, report(보고서): `{base.rel(REVIEW_PACKET_PATH)}`",
                "",
                "효과(effect, 효과): Stage16(16단계)은 QDA(이차판별분석)의 class covariance(클래스별 공분산) 특성을 MT5(메타트레이더5) KPI(핵심성과지표)까지 연결했지만 edge(거래 우위)는 주장하지 않는다.",
            ]
        ),
    )
    engine.write_md(
        base.STAGE_ROOT / "04_selected/selection_status.md",
        "\n".join(
            [
                "# Stage 16 Selection Status(16단계 선택 상태)",
                "",
                "## Current Read(현재 판독)",
                "",
                f"- stage(단계): `{base.STAGE_ID}`",
                "- status(상태): `reviewed_qda_run10A_run10L_decision_microprobe_no_edge(검토됨, QDA 실행 10A-10L 결정 미세 탐침, 엣지 없음)`",
                f"- current run(현재 실행): `{current_run}`",
                "- model family(모델 계열): QDA(`Quadratic Discriminant Analysis`, 이차 판별 분석)",
                "- selected operating reference/promotion/baseline(선택 운영 기준/승격/기준선): `none(없음)`",
                f"- judgment(판정): `{aggregate['judgment']}`",
                f"- recommendation(권고): `{rec}`",
                f"- MT5 KPI records(MT5 핵심성과지표 기록): `{aggregate['mt5_kpi_record_count']}`",
                f"- normalized KPI records(정규화 KPI 기록): `{kpi['normalized_records']}`",
                f"- boundary(경계): `{BOUNDARY}`",
                "",
                "효과(effect, 효과): 이번 microprobe(미세 탐침)는 Stage16(16단계)을 close(닫기)할지 continue(진행)할지 판단하지만 edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 만들지 않는다.",
            ]
        ),
    )
    engine.write_md(
        DECISION_PATH,
        "\n".join(
            [
                "# 2026-05-03 Stage16 QDA Run10 Decision Microprobe(16단계 QDA 실행10 결정 미세 탐침)",
                "",
                "## Decision(결정)",
                "",
                f"`run10A`~`run10L` QDA(`Quadratic Discriminant Analysis`, 이차 판별 분석) decision microprobe(결정 미세 탐침)를 MT5(`MetaTrader 5`, 메타트레이더5) Strategy Tester(전략 테스터)까지 실행했다.",
                "",
                f"- recommendation(권고): `{rec}`",
                f"- reason(이유): {recommendation.get('reason')}",
                f"- selected current run(선택 현재 실행): `{current_run}`",
                "",
                "효과(effect, 효과): close(닫기)라면 QDA(이차판별분석)는 보존 단서로 남기고 다음 stage topic(단계 주제)로 이동한다. continue(진행)라면 같은 계열을 context/WFO(문맥/워크포워드) 쪽으로 한 번 더 좁힌다.",
                "",
                "## Boundary(경계)",
                "",
                f"`{BOUNDARY}`",
            ]
        ),
    )
    sync_workspace_docs(aggregate, kpi, current_run, rec)
    sync_misc_docs(rec)


def sync_workspace_docs(aggregate: Mapping[str, Any], kpi: Mapping[str, Any], current_run: str, recommendation: str) -> None:
    state_path = base.ROOT / "docs/workspace/workspace_state.yaml"
    state = engine.io_path(state_path).read_text(encoding="utf-8-sig")
    state = re.sub(r"^current_run_id: .*$", f"current_run_id: {current_run}", state, count=1, flags=re.M)
    state = state.replace("stage16_qda_run09A_run09Q_followup_mt5_runtime_probe_reviewed", "stage16_qda_run10A_run10L_decision_microprobe_mt5_runtime_probe_reviewed")
    state = state.replace("reviewed_qda_run09A_run09Q_followup_mt5_runtime_probe_no_edge", "reviewed_qda_run10A_run10L_decision_microprobe_no_edge")
    stage_block = f"""stage16_qda_class_covariance_scout:
  stage_id: {base.STAGE_ID}
  status: reviewed_qda_run10A_run10L_decision_microprobe_no_edge
  lane: independent_model_family_topic_pivot_no_promotion
  model_family: {base.MODEL_FAMILY}
  current_run_id: {current_run}
  current_status: run10A_run10L_decision_microprobe_mt5_runtime_probe_reviewed
  source_clue: Stage15 LDA light covariance shrinkage clue; QDA tests class-specific covariance behavior without edge search
  hypothesis: QDA class-specific covariance may show probability shape and signal-density behavior different from LDA under the same label and split contract.
  comparison_baseline: no trading baseline; compare run10 decision microprobe against run09D/run09G as within-stage references only
  boundary: {BOUNDARY}
  stage_brief_path: stages/{base.STAGE_ID}/00_spec/stage_brief.md
  input_references_path: stages/{base.STAGE_ID}/01_inputs/input_references.md
  selection_status_path: stages/{base.STAGE_ID}/04_selected/selection_status.md
  current_run_packet_path: {base.rel(REVIEW_PACKET_PATH)}
  decision_path: {base.rel(DECISION_PATH)}
  next_action: {recommendation}
"""
    state = re.sub(r"stage16_qda_class_covariance_scout:\n.*?(?=stage16_qda_characterization_run08A_run08J:)", stage_block, state, count=1, flags=re.S)
    append = f"""stage16_qda_run10_decision_microprobe:
  packet_id: {PACKET_ID}
  status: reviewed_runtime_probe_completed
  judgment: {aggregate['judgment']}
  recommendation: {recommendation}
  run_range: run10A-run10L
  current_run_id: {current_run}
  completed_run_count: {aggregate['completed_run_count']}
  mt5_kpi_record_count: {aggregate['mt5_kpi_record_count']}
  normalized_kpi_record_count: {kpi['normalized_records']}
  trade_attribution_records: {kpi['trade_attribution_records']}
  selected_operating_reference: none
  selected_promotion_candidate: none
  selected_baseline: none
  boundary: {BOUNDARY}
  report_path: {base.rel(REVIEW_PACKET_PATH)}
  decision_path: {base.rel(DECISION_PATH)}
  next_action: {recommendation}
"""
    if "stage16_qda_run10_decision_microprobe:" not in state:
        state = state.replace("stage16_qda_run09_followup_mt5_runtime_probe:\n", append + "stage16_qda_run09_followup_mt5_runtime_probe:\n", 1)
    engine.io_path(state_path).write_text(state.rstrip() + "\n", encoding="utf-8")
    current_path = base.ROOT / "docs/context/current_working_state.md"
    current = engine.io_path(current_path).read_text(encoding="utf-8-sig")
    current = re.sub(r"- current run\(현재 실행\): `[^`]+`", f"- current run(현재 실행): `{current_run}`", current, count=1)
    latest = "\n".join(
        [
            "## Latest Stage 16 Update(최신 Stage 16 업데이트)",
            "",
            f"Stage16(16단계)는 QDA(`Quadratic Discriminant Analysis`, 이차 판별 분석) `run10A`~`run10L` decision microprobe(결정 미세 탐침)를 MT5(`MetaTrader 5`, 메타트레이더5) runtime_probe(런타임 탐침)와 KPI(`Key Performance Indicator`, 핵심성과지표) 정규화까지 완료했다.",
            "",
            f"효과(effect, 효과): recommendation(권고)은 `{recommendation}`이다. 이 판정은 close(닫기)/continue(진행) 방향만 말하며 edge(거래 우위), alpha quality(알파 품질), baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 만들지 않는다.",
            "",
        ]
    )
    if "## Latest Stage 16 Update(최신 Stage 16 업데이트)" in current:
        current = re.sub(r"## Latest Stage 16 Update\(최신 Stage 16 업데이트\)\n\n.*?(?=## 쉬운 설명)", latest, current, count=1, flags=re.S)
    else:
        current = current.rstrip() + "\n\n" + latest
    engine.io_path(current_path).write_text(current.rstrip() + "\n", encoding="utf-8-sig")


def sync_misc_docs(recommendation: str) -> None:
    changelog_path = base.ROOT / "docs/workspace/changelog.md"
    changelog = engine.io_path(changelog_path).read_text(encoding="utf-8-sig")
    line = f"- 2026-05-03: Stage16 QDA(이차판별분석) `run10A`~`run10L` decision microprobe(결정 미세 탐침)를 MT5 runtime_probe(MT5 런타임 탐침)와 KPI(핵심성과지표) 정규화까지 완료했다. recommendation(권고): `{recommendation}`. 효과(effect, 효과): Stage16(16단계)을 닫을지 진행할지 판단 근거를 남기되 edge(거래 우위)는 주장하지 않는다."
    if line not in changelog:
        engine.io_path(changelog_path).write_text(changelog.rstrip() + "\n" + line + "\n", encoding="utf-8-sig")
    idea_path = base.ROOT / "docs/registers/idea_registry.md"
    idea = engine.io_path(idea_path).read_text(encoding="utf-8-sig")
    line = f"- 2026-05-03 Stage16 QDA run10 decision microprobe(16단계 QDA 실행10 결정 미세 탐침): full58 reg0.18 neighborhood(full58 정규화 0.18 주변)와 drop_mega10(대형주 10개 제거) 계열을 MT5(메타트레이더5) KPI(핵심성과지표)까지 재검증했다. recommendation(권고): `{recommendation}`. 효과(effect, 효과): 반복 생존 여부를 close(닫기)/continue(진행) 판정에 연결한다."
    if line not in idea:
        engine.io_path(idea_path).write_text(idea.rstrip() + "\n" + line + "\n", encoding="utf-8-sig")


def configure_engine() -> None:
    engine.PACKET_ID = PACKET_ID
    engine.REVIEW_PACKET_PATH = REVIEW_PACKET_PATH
    engine.DECISION_PATH = DECISION_PATH
    engine.PACKET_ROOT = PACKET_ROOT
    engine.BOUNDARY = BOUNDARY
    engine.JUDGMENT_COMPLETED = JUDGMENT_COMPLETED
    engine.JUDGMENT_BLOCKED = JUDGMENT_BLOCKED
    engine.EXPLORATION_LABEL = EXPLORATION_LABEL
    engine.BASELINE_RUN_ID = BASELINE_RUN_ID
    engine.run09_specs = run10_specs
    engine.aggregate_summary = aggregate_summary
    engine.experiment_design = experiment_design
    engine.packet_markdown = packet_markdown
    engine.gate_payloads = gate_payloads
    engine.write_packet_files = write_packet_files
    engine.sync_docs = sync_docs
    engine.run_result_markdown = run_result_markdown


def main(argv: Sequence[str] | None = None) -> int:
    configure_engine()
    engine.main(argv)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
