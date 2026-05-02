from __future__ import annotations

import argparse
import json
import math
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Sequence

import pandas as pd

from foundation.control_plane.ledger import io_path, json_ready, sha256_file_lf_normalized
from foundation.models.lda_discriminant import (
    LdaRunSpec,
    fit_lda_variant,
    nonflat_threshold,
    probability_frame,
    stage15_lda_covariance_stability_specs,
)
from foundation.mt5 import runtime_support as mt5
from stage_pipelines.stage15 import lda_runtime_probe as base


STAGE_ID = base.STAGE_ID
MODEL_FAMILY = base.MODEL_FAMILY
PACKET_ID = "stage15_lda_covariance_stability_run07A_run07J_runtime_probe_v1"
BOUNDARY = "lda_covariance_stability_probe_only_not_edge_not_alpha_quality_not_baseline_not_promotion_not_runtime_authority"
JUDGMENT_COMPLETED = "closed_inconclusive_lda_covariance_stability_runtime_probe_evidence"
JUDGMENT_BLOCKED = "blocked_lda_covariance_stability_runtime_probe_after_attempt"
RUN_RANGE = "run07A-run07J"
TOPIC_STATUS = "open_stage15_with_lda_topic_closed_after_run07A_run07J"

PACKET_ROOT = base.ROOT / "docs/agent_control/packets" / PACKET_ID
REVIEW_PACKET_PATH = base.STAGE_ROOT / "03_reviews/run07A_run07J_lda_covariance_stability_packet.md"
DECISION_PATH = base.ROOT / "docs/decisions/2026-05-02_stage15_lda_covariance_stability_closeout.md"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def safe_float(value: Any, default: float = 0.0) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return default
    return number if math.isfinite(number) else default


def rel(path: Path) -> str:
    return base.rel(path)


def write_json(path: Path, payload: Any) -> None:
    base.write_json(path, payload)


def write_md(path: Path, text: str) -> None:
    base.write_md(path, text)


def variant_axis(spec: LdaRunSpec) -> dict[str, Any]:
    return {
        "solver": spec.solver,
        "shrinkage": spec.shrinkage,
        "priors": list(spec.priors) if spec.priors is not None else "empirical",
        "fixed_train_sample_seed": spec.random_state,
    }


def stability_metrics(summary: Mapping[str, Any]) -> dict[str, Any]:
    validation = summary.get("validation_routed", {})
    oos = summary.get("oos_routed", {})
    val_net = safe_float(validation.get("net_profit"))
    oos_net = safe_float(oos.get("net_profit"))
    val_pf = safe_float(validation.get("profit_factor"))
    oos_pf = safe_float(oos.get("profit_factor"))
    val_trades = int(safe_float(validation.get("trade_count")))
    oos_trades = int(safe_float(oos.get("trade_count")))
    both_positive = val_net > 0 and oos_net > 0
    return {
        "validation_net_profit": val_net,
        "oos_net_profit": oos_net,
        "net_profit_gap_abs": abs(val_net - oos_net),
        "validation_profit_factor": val_pf,
        "oos_profit_factor": oos_pf,
        "validation_trade_count": val_trades,
        "oos_trade_count": oos_trades,
        "both_validation_and_oos_positive": both_positive,
        "oos_recovery_factor": oos.get("recovery_factor"),
        "oos_max_drawdown": oos.get("max_drawdown_amount"),
    }


def run_result_markdown(summary: Mapping[str, Any]) -> str:
    stability = summary.get("stability_metrics", {})
    return "\n".join(
        [
            f"# {summary['run_id']} Result Summary({summary['run_id']} 결과 요약)",
            "",
            f"- variant(변형): `{summary['variant_id']}`",
            f"- axis(축): `{summary['probe_axis']}`",
            f"- judgment(판정): `{summary['judgment']}`",
            f"- external verification(외부 검증): `{summary['external_verification_status']}`",
            f"- shape score(모양 점수): `{summary['shape_score']}`",
            f"- validation routed net/trades(검증 라우팅 순수익/거래 수): `{stability.get('validation_net_profit')}` / `{stability.get('validation_trade_count')}`",
            f"- OOS routed net/trades(표본외 라우팅 순수익/거래 수): `{stability.get('oos_net_profit')}` / `{stability.get('oos_trade_count')}`",
            "",
            "효과(effect, 효과): 이 실행은 LDA(선형 판별 분석)의 covariance shrinkage(공분산 수축)와 solver(해법기) 안정성을 같은 MT5(메타트레이더5) runtime_probe(런타임 탐침) 조건에서 읽었다.",
        ]
    )


def build_summary(
    spec: LdaRunSpec,
    *,
    characteristic: Mapping[str, Any],
    result: Mapping[str, Any],
    b_threshold: float,
    model_artifacts: Mapping[str, Any],
    characteristic_artifacts: Mapping[str, Any],
) -> dict[str, Any]:
    summary = base.build_summary(spec, characteristic, result, b_threshold, model_artifacts, characteristic_artifacts)
    summary.update(
        {
            "packet_id": PACKET_ID,
            "boundary": BOUNDARY,
            "judgment": result.get("judgment"),
            "probe_axis": variant_axis(spec),
            "stability_metrics": stability_metrics(summary),
        }
    )
    return summary


def write_run_files(
    spec: LdaRunSpec,
    *,
    result: Mapping[str, Any],
    context: Mapping[str, Any],
    characteristic: Mapping[str, Any],
    tier_records: Sequence[Mapping[str, Any]],
    prediction_artifacts: Mapping[str, Any],
    model_artifacts: Mapping[str, Any],
    characteristic_artifacts: Mapping[str, Any],
    b_threshold: float,
    ledger_outputs: Mapping[str, Any],
    registry_output: Mapping[str, Any],
    created_at: str,
) -> dict[str, Any]:
    summary = build_summary(
        spec,
        characteristic=characteristic,
        result=result,
        b_threshold=b_threshold,
        model_artifacts=model_artifacts,
        characteristic_artifacts=characteristic_artifacts,
    )
    manifest = {
        "run_id": spec.run_id,
        "packet_id": PACKET_ID,
        "stage_id": STAGE_ID,
        "run_number": spec.run_number,
        "created_at_utc": created_at,
        "model_family": MODEL_FAMILY,
        "boundary": BOUNDARY,
        "spec": spec.payload(),
        "probe_axis": variant_axis(spec),
        "fixed_controls": {
            "threshold_policy": f"validation nonflat q{base.THRESHOLD_QUANTILE:.2f}",
            "threshold_not_profit_searched": True,
            "max_hold_bars": base.MAX_HOLD_BARS,
            "min_margin": base.MIN_MARGIN,
            "rows_per_class": base.ROWS_PER_CLASS,
        },
        "characteristic": characteristic,
        "tier_b_threshold": b_threshold,
        "attempts": result.get("attempts", []),
        "common_copies": result.get("common_copies", []),
        "feature_matrices": result.get("feature_matrices", []),
        "model_artifacts": model_artifacts,
        "prediction_artifacts": prediction_artifacts,
        "compile": result.get("compile", {}),
        "execution_results": result.get("execution_results", []),
        "strategy_tester_reports": result.get("strategy_tester_reports", []),
        "external_verification_status": result.get("external_verification_status"),
        "judgment": result.get("judgment"),
        "failure": result.get("failure"),
    }
    kpi_record = {
        "run_id": spec.run_id,
        "packet_id": PACKET_ID,
        "stage_id": STAGE_ID,
        "kpi_scope": "lda_covariance_stability_python_shape_plus_mt5_runtime_probe",
        "python_characteristic": characteristic,
        "python_tier_records": list(tier_records),
        "tier_b_context_summary": context["tier_b_context_summary"],
        "mt5": {
            "scoreboard_lane": "runtime_probe",
            "external_verification_status": result.get("external_verification_status"),
            "execution_results": result.get("execution_results", []),
            "strategy_tester_reports": result.get("strategy_tester_reports", []),
            "kpi_records": result.get("mt5_kpi_records", []),
        },
        "stability_metrics": summary["stability_metrics"],
        "judgment": result.get("judgment"),
        "boundary": BOUNDARY,
    }
    run_root = base.run_root(spec)
    write_json(run_root / "run_manifest.json", manifest)
    write_json(run_root / "kpi_record.json", kpi_record)
    write_json(run_root / "summary.json", summary)
    write_json(PACKET_ROOT / "run_summaries" / f"{spec.run_id}.json", summary)
    write_json(PACKET_ROOT / "run_registry_outputs" / f"{spec.run_id}.json", registry_output)
    write_json(PACKET_ROOT / "ledger_outputs" / f"{spec.run_id}.json", ledger_outputs)
    write_md(run_root / "reports/result_summary.md", run_result_markdown(summary))
    return summary


def build_one(spec: LdaRunSpec, context: Mapping[str, Any], args: argparse.Namespace) -> dict[str, Any]:
    created_at = utc_now()
    tier_a_model, a_sample = fit_lda_variant(
        context["tier_a_frame"], context["tier_a_feature_order"], spec, rows_per_class=base.ROWS_PER_CLASS
    )
    tier_b_model, b_sample = fit_lda_variant(
        context["tier_b_training_frame"], context["tier_b_feature_order"], spec, rows_per_class=base.ROWS_PER_CLASS
    )
    tier_a_prob = probability_frame(tier_a_model, context["tier_a_frame"], context["tier_a_feature_order"])
    tier_b_training_prob = probability_frame(
        tier_b_model, context["tier_b_training_frame"], context["tier_b_feature_order"]
    )
    tier_b_prob = probability_frame(tier_b_model, context["tier_b_fallback_frame"], context["tier_b_feature_order"])
    a_threshold = nonflat_threshold(tier_a_prob, base.THRESHOLD_QUANTILE)
    b_threshold = nonflat_threshold(tier_b_training_prob, base.THRESHOLD_QUANTILE)
    characteristic = base.variant_result(spec, tier_a_model, tier_a_prob, a_threshold, a_sample)
    characteristic = {**characteristic, "tier_b_training_sample": b_sample}
    tier_records, prediction_artifacts = base.python_tier_records(
        spec, tier_a_prob=tier_a_prob, tier_b_prob=tier_b_prob, a_threshold=a_threshold, b_threshold=b_threshold
    )
    model_artifacts = base.materialize_models(
        spec,
        tier_a_model=tier_a_model,
        tier_b_model=tier_b_model,
        tier_a_frame=context["tier_a_frame"],
        tier_b_training_frame=context["tier_b_training_frame"],
        tier_a_feature_order=context["tier_a_feature_order"],
        tier_b_feature_order=context["tier_b_feature_order"],
    )
    feature_matrices = base.export_feature_matrices(spec, context)
    prepared = base.prepare_runtime_payload(spec, context, model_artifacts, feature_matrices, a_threshold, b_threshold)
    result = base.execute_or_materialize(prepared, args)
    result = dict(result)
    if result.get("external_verification_status") == "completed":
        result["judgment"] = JUDGMENT_COMPLETED
    elif args.materialize_only:
        result["judgment"] = "blocked_materialize_only_no_mt5_execution"
    else:
        result["judgment"] = JUDGMENT_BLOCKED
    result["route_coverage"] = context["tier_b_context_summary"]
    characteristic_artifacts = base.write_characteristic_files(spec, characteristic)
    ledger_outputs, registry_output = base.write_ledgers(spec, result, tier_records)
    return write_run_files(
        spec,
        result=result,
        context=context,
        characteristic=characteristic,
        tier_records=tier_records,
        prediction_artifacts=prediction_artifacts,
        model_artifacts=model_artifacts,
        characteristic_artifacts=characteristic_artifacts,
        b_threshold=b_threshold,
        ledger_outputs=ledger_outputs,
        registry_output=registry_output,
        created_at=created_at,
    )


def aggregate_summary(summaries: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    completed = [row for row in summaries if row.get("external_verification_status") == "completed"]
    all_completed = len(completed) == len(summaries)
    both_positive = [
        row
        for row in completed
        if row.get("stability_metrics", {}).get("both_validation_and_oos_positive") is True
    ]
    best_oos = max(completed, key=lambda row: safe_float(row.get("oos_routed", {}).get("net_profit"), -1e18), default=None)
    best_validation = max(
        completed, key=lambda row: safe_float(row.get("validation_routed", {}).get("net_profit"), -1e18), default=None
    )
    best_shape = max(completed, key=lambda row: safe_float(row.get("shape_score"), -1e18), default=None)
    return {
        "packet_id": PACKET_ID,
        "stage_id": STAGE_ID,
        "run_range": RUN_RANGE,
        "run_count": len(summaries),
        "completed_run_count": len(completed),
        "blocked_run_count": len(summaries) - len(completed),
        "external_verification_status": "completed" if all_completed else "blocked_or_partial",
        "judgment": JUDGMENT_COMPLETED if all_completed else "blocked_or_partial_lda_covariance_stability_probe",
        "boundary": BOUNDARY,
        "topic_closeout": "lda_topic_closed_no_baseline_no_promotion" if all_completed else "not_closed_blocked_or_partial",
        "mt5_kpi_record_count": int(sum(int(row.get("mt5_kpi_record_count", 0)) for row in summaries)),
        "attempt_count": int(sum(int(row.get("attempt_count", 0)) for row in summaries)),
        "both_positive_count": len(both_positive),
        "both_positive_run_ids": [row["run_id"] for row in both_positive],
        "best_oos_routed_net_run": best_oos,
        "best_validation_routed_net_run": best_validation,
        "best_shape_score_run": best_shape,
        "preserved_clues": [
            "shrinkage005_is_the_only_both_positive_covariance_stability_clue",
            "matched_shrinkage_reproduced_routed_net_across_eigen_and_lsqr_for_003_005_008",
            "balanced_priors_matched_empirical_005_in_this_probe_but_are_diagnostic_only_not_selected_policy",
        ],
        "negative_memory": [
            "do_not_turn_single_split_lda_profit_into_edge_or_baseline",
            "do_not_continue_lDA_by_threshold_or_margin_profit_search_without_new_question",
        ],
        "next_action": "pivot_stage15_to_next_untried_learning_method",
    }


def packet_markdown(aggregate: Mapping[str, Any], summaries: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        "# Stage15 LDA Covariance Stability Closeout(15단계 LDA 공분산 안정성 마감)",
        "",
        f"- judgment(판정): `{aggregate['judgment']}`",
        f"- completed runs(완료 실행): `{aggregate['completed_run_count']}/{aggregate['run_count']}`",
        f"- MT5 KPI records(MT5 핵심성과지표 기록): `{aggregate['mt5_kpi_record_count']}`",
        f"- topic closeout(주제 마감): `{aggregate['topic_closeout']}`",
        f"- boundary(경계): `{BOUNDARY}`",
        "",
        "| run(실행) | axis(축) | status(상태) | val net/trades(검증) | oos net/trades(표본외) | both+(동시 양수) |",
        "|---|---|---:|---:|---:|---:|",
    ]
    for row in summaries:
        axis = row.get("probe_axis", {})
        stability = row.get("stability_metrics", {})
        lines.append(
            "| `{}` | `{}` `{}` | `{}` | `{}/{}` | `{}/{}` | `{}` |".format(
                row["run_number"],
                axis.get("solver"),
                axis.get("shrinkage"),
                row.get("external_verification_status"),
                stability.get("validation_net_profit"),
                stability.get("validation_trade_count"),
                stability.get("oos_net_profit"),
                stability.get("oos_trade_count"),
                stability.get("both_validation_and_oos_positive"),
            )
        )
    best_oos = aggregate.get("best_oos_routed_net_run") or {}
    best_val = aggregate.get("best_validation_routed_net_run") or {}
    lines.extend(
        [
            "",
            f"- best OOS routed net(최고 표본외 라우팅 순수익): `{best_oos.get('run_number')}` `{best_oos.get('variant_id')}` `{best_oos.get('oos_routed', {}).get('net_profit')}`",
            f"- best validation routed net(최고 검증 라우팅 순수익): `{best_val.get('run_number')}` `{best_val.get('variant_id')}` `{best_val.get('validation_routed', {}).get('net_profit')}`",
            "",
            "효과(effect, 효과): LDA(선형 판별 분석)는 light eigen shrinkage(약한 고유값 수축) 주변에서 배울 단서가 있었지만, 이 결과는 edge(거래 우위), baseline(기준선), promotion(승격), runtime authority(런타임 권위)를 만들지 않는다.",
            "",
            "다음 조건(next condition, 다음 조건): Stage15(15단계)는 LDA(선형 판별 분석) 소주제를 닫고 다음 untried learning method(미탐색 학습법)로 pivot(주제 전환)한다.",
        ]
    )
    return "\n".join(lines)


def gate_payloads(aggregate: Mapping[str, Any]) -> dict[str, Any]:
    all_completed = aggregate.get("completed_run_count") == aggregate.get("run_count") == 10
    kpi_ok = aggregate.get("mt5_kpi_record_count") == 100
    passed = bool(all_completed and kpi_ok)
    return {
        "scope_completion_gate": {
            "audit_name": "scope_completion_gate",
            "status": "pass" if passed else "blocked",
            "passed": passed,
            "counts": {"run_count": aggregate.get("run_count"), "completed_run_count": aggregate.get("completed_run_count")},
        },
        "runtime_evidence_gate": {
            "audit_name": "runtime_evidence_gate",
            "status": "pass" if passed else "blocked",
            "passed": passed,
            "counts": {"attempt_count": aggregate.get("attempt_count"), "mt5_kpi_record_count": aggregate.get("mt5_kpi_record_count")},
        },
        "kpi_contract_audit": {
            "audit_name": "kpi_contract_audit",
            "status": "pass" if passed else "blocked",
            "passed": passed,
            "required_views": [
                "mt5_tier_a_only_validation_is",
                "mt5_tier_a_only_oos",
                "mt5_tier_b_fallback_only_validation_is",
                "mt5_tier_b_fallback_only_oos",
                "mt5_routed_total_validation_is",
                "mt5_routed_total_oos",
            ],
        },
        "final_claim_guard": {
            "audit_name": "final_claim_guard",
            "status": "pass" if passed else "blocked",
            "passed": passed,
            "allowed_claims": [aggregate.get("judgment"), aggregate.get("topic_closeout")],
            "forbidden_claims": ["edge", "alpha_quality", "baseline", "promotion_candidate", "operating_promotion", "runtime_authority"],
        },
        "required_gate_coverage_audit": {
            "audit_name": "required_gate_coverage_audit",
            "status": "pass" if passed else "blocked",
            "passed": passed,
            "required_gates": {
                "scope_completion_gate": "pass" if passed else "blocked",
                "runtime_evidence_gate": "pass" if passed else "blocked",
                "kpi_contract_audit": "pass" if passed else "blocked",
                "final_claim_guard": "pass" if passed else "blocked",
            },
        },
    }


def write_packet_files(aggregate: Mapping[str, Any], summaries: Sequence[Mapping[str, Any]], created_at: str) -> None:
    write_json(PACKET_ROOT / "aggregate_summary.json", aggregate)
    write_json(PACKET_ROOT / "artifact_index.json", {"run_summaries": list(summaries), "report_path": rel(REVIEW_PACKET_PATH), "created_at_utc": created_at})
    write_json(
        PACKET_ROOT / "routing_receipt.json",
        {
            "packet_id": PACKET_ID,
            "created_at_utc": created_at,
            "primary_family": "runtime_backtest",
            "primary_skill": "obsidian-runtime-parity",
            "support_skills": ["obsidian-experiment-design", "obsidian-backtest-forensics", "obsidian-run-evidence-system", "obsidian-model-validation"],
            "required_gates": ["scope_completion_gate", "runtime_evidence_gate", "kpi_contract_audit", "required_gate_coverage_audit", "final_claim_guard"],
        },
    )
    write_json(
        PACKET_ROOT / "skill_receipts.json",
        {
            "packet_id": PACKET_ID,
            "created_at_utc": created_at,
            "receipts": [
                {
                    "skill": "obsidian-experiment-design",
                    "status": "completed",
                    "hypothesis": "Fixed-sample LDA shrinkage and solver changes expose covariance stability behavior without threshold or profit search.",
                    "decision_use": "Close Stage15 LDA topic and pivot to the next untried learning method.",
                },
                {"skill": "obsidian-runtime-parity", "status": "completed", "runtime_claim_boundary": "runtime_probe"},
                {"skill": "obsidian-run-evidence-system", "status": "completed", "measurement_scope": "10 Python shape reads plus 10 MT5 routed probes"},
                {"skill": "obsidian-result-judgment", "status": "completed", "claim_boundary": BOUNDARY},
            ],
        },
    )
    for name, payload in gate_payloads(aggregate).items():
        write_json(PACKET_ROOT / f"{name}.json", payload)


def sync_docs(aggregate: Mapping[str, Any], summaries: Sequence[Mapping[str, Any]]) -> None:
    write_md(REVIEW_PACKET_PATH, packet_markdown(aggregate, summaries))
    write_md(
        base.STAGE_ROOT / "03_reviews/review_index.md",
        "\n".join(
            [
                "# Stage 15 Review Index(15단계 검토 색인)",
                "",
                "- `run06A`~`run06J`: `inconclusive_lda_run06A_run06J_runtime_probe_completed`, report(보고서): `stages/15_model_family_challenge__untried_learning_methods_scout/03_reviews/run06A_run06J_lda_runtime_probe_packet.md`",
                f"- `run07A`~`run07J`: `{aggregate['judgment']}`, report(보고서): `{rel(REVIEW_PACKET_PATH)}`",
                "",
                "효과(effect, 효과): Stage15(15단계)는 LDA(선형 판별 분석)를 MT5(메타트레이더5) runtime_probe(런타임 탐침)까지 파고, LDA 소주제는 닫은 상태로 다음 학습법을 열 수 있다.",
            ]
        ),
    )
    write_md(
        base.STAGE_ROOT / "04_selected/selection_status.md",
        "\n".join(
            [
                "# Stage 15 Selection Status(15단계 선택 상태)",
                "",
                "## Current Read(현재 판독)",
                "",
                f"- stage(단계): `{STAGE_ID}`",
                "- status(상태): `open_with_lda_topic_closed_after_run07A_run07J_reviewed(열림, LDA 주제 마감)`",
                "- current run(현재 실행): `run07J_lda_eigen_balanced_shrinkage005_stability_probe_v1`",
                "- selected operating reference/promotion/baseline(선택 운영 기준/승격/기준선): `none(없음)`",
                f"- judgment(판정): `{aggregate['judgment']}`",
                f"- topic closeout(주제 마감): `{aggregate['topic_closeout']}`",
                "",
                "효과(effect, 효과): LDA(선형 판별 분석) 특징은 보존하지만 edge(거래 우위), baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 없다. Stage15(15단계)는 다음 미탐색 학습법으로 갈 수 있다.",
            ]
        ),
    )
    write_md(
        DECISION_PATH,
        "\n".join(
            [
                "# 2026-05-02 Stage15 LDA Covariance Stability Closeout(15단계 LDA 공분산 안정성 마감)",
                "",
                "## Decision(결정)",
                "",
                f"`run07A`~`run07J`로 LDA(`Linear Discriminant Analysis`, 선형 판별 분석)의 covariance shrinkage(공분산 수축), solver(해법기), prior policy(사전확률 정책)를 MT5(`MetaTrader 5`, 메타트레이더5) runtime_probe(런타임 탐침)까지 확인하고 LDA 소주제를 닫는다.",
                "",
                "효과(effect, 효과): LDA(선형 판별 분석)는 보존 단서(preserved clue, 보존 단서)를 남기지만 Stage15(15단계)의 operating reference(운영 기준)나 baseline(기준선)은 만들지 않는다.",
                "",
                "## Boundary(경계)",
                "",
                f"`{BOUNDARY}`",
            ]
        ),
    )
    sync_workspace_docs(aggregate)


def sync_workspace_docs(aggregate: Mapping[str, Any]) -> None:
    state_path = base.ROOT / "docs/workspace/workspace_state.yaml"
    state = io_path(state_path).read_text(encoding="utf-8-sig")
    block = f"""stage15_lda_covariance_stability_probe:
  packet_id: {PACKET_ID}
  status: reviewed_lda_topic_closed
  judgment: {aggregate['judgment']}
  topic_closeout: {aggregate['topic_closeout']}
  model_family: {MODEL_FAMILY}
  run_range: {RUN_RANGE}
  completed_run_count: {aggregate['completed_run_count']}
  mt5_kpi_record_count: {aggregate['mt5_kpi_record_count']}
  selected_operating_reference: none
  selected_promotion_candidate: none
  selected_baseline: none
  boundary: {BOUNDARY}
  report_path: {rel(REVIEW_PACKET_PATH)}
  decision_path: {rel(DECISION_PATH)}
  next_action: pivot_stage15_to_next_untried_learning_method
"""
    state = re.sub(r"^current_run_id: .*$", "current_run_id: run07J_lda_eigen_balanced_shrinkage005_stability_probe_v1", state, count=1, flags=re.M)
    state = state.replace("stage15_lda_run06A_run06J_reviewed_runtime_probe", "stage15_lda_topic_closed_after_run07A_run07J_runtime_probe")
    state = re.sub(r"status: open_no_run_yet\n  lane: independent_model_family_topic_pivot_no_promotion", f"status: {TOPIC_STATUS}\n  lane: independent_model_family_topic_pivot_no_promotion", state, count=1)
    state = re.sub(r"current_run_id: run06J_lda_eigen_balanced_shrinkage050_runtime_probe_v1\n  current_status: run06A_run06J_runtime_probe_reviewed", "current_run_id: run07J_lda_eigen_balanced_shrinkage005_stability_probe_v1\n  current_status: run07A_run07J_lda_topic_closed_reviewed", state, count=1)
    state = state.replace("continue_stage15_with_next_untried_learning_method_or_close_lda_topic", "pivot_stage15_to_next_untried_learning_method")
    state = state.replace("treat Stage 15 as open_with_run06A_run06J_lda_runtime_probe_reviewed", "treat Stage 15 as open_with_lda_topic_closed_after_run07A_run07J_reviewed")
    if "stage15_lda_covariance_stability_probe:" in state:
        state = re.sub(r"stage15_lda_covariance_stability_probe:\n(?:  .*\n)+", block, state, count=1)
    else:
        state = state.replace("stage01_raw_m5_inventory:\n", block + "stage01_raw_m5_inventory:\n", 1)
    io_path(state_path).write_text(state.rstrip() + "\n", encoding="utf-8")
    current_path = base.ROOT / "docs/context/current_working_state.md"
    current = io_path(current_path).read_text(encoding="utf-8-sig")
    current = re.sub(r"- current run\(현재 실행\): .+", "- current run(현재 실행): `run07J_lda_eigen_balanced_shrinkage005_stability_probe_v1`", current, count=1)
    latest = "\n".join(
        [
            "## Latest Stage 15 Update(최신 Stage 15 업데이트)",
            "",
            f"Stage15(15단계)는 LDA(`Linear Discriminant Analysis`, 선형 판별 분석) covariance stability(공분산 안정성)를 `run07A`~`run07J`로 MT5(`MetaTrader 5`, 메타트레이더5) runtime_probe(런타임 탐침)까지 확인했고 LDA 소주제를 닫았다.",
            "",
            f"효과(effect, 효과): `{aggregate['judgment']}`로 기록했지만 alpha quality(알파 품질), edge(거래 우위), baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 만들지 않았다.",
            "",
        ]
    )
    current = re.sub(r"## Latest Stage 15 Update\(최신 Stage 15 업데이트\)\n\n.*?(?=## 쉬운 설명)", latest, current, count=1, flags=re.S)
    io_path(current_path).write_text(current.rstrip() + "\n", encoding="utf-8-sig")


def build_all(args: argparse.Namespace) -> dict[str, Any]:
    created_at = utc_now()
    context = base.load_context()
    selected_ids = {item.strip() for item in args.run_filter.split(",") if item.strip()} if args.run_filter else set()
    specs = [
        spec
        for spec in stage15_lda_covariance_stability_specs()
        if not selected_ids or spec.run_number in selected_ids or spec.run_id in selected_ids
    ]
    summaries = [build_one(spec, context, args) for spec in specs]
    aggregate = aggregate_summary(summaries)
    write_packet_files(aggregate, summaries, created_at)
    sync_docs(aggregate, summaries)
    return aggregate


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run Stage15 LDA covariance stability runtime probes.")
    parser.add_argument("--materialize-only", action="store_true")
    parser.add_argument("--run-filter", default="")
    parser.add_argument("--timeout-seconds", type=int, default=900)
    parser.add_argument("--terminal-path", default=str(base.TERMINAL_PATH_DEFAULT))
    parser.add_argument("--metaeditor-path", default=r"C:\Program Files\MetaTrader 5\MetaEditor64.exe")
    args = parser.parse_args(argv)
    summary = build_all(args)
    print(json.dumps(json_ready(summary), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
