from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
STAGE_ID = "269_onnx_candidate_campaign__fresh_thesis_candidate_construction"
RUN_ID = "run269E_materialized_score_surface_screen_v1"
RUN_ROOT = ROOT / "stages" / STAGE_ID / "02_runs" / "run269E"
REVIEW_ROOT = ROOT / "stages" / STAGE_ID / "03_reviews"
RUN269D_ROOT = ROOT / "stages" / STAGE_ID / "02_runs" / "run269D"
RUN269D_REPORT = ROOT / "stages" / STAGE_ID / "03_reviews" / "run269D_report.md"
RUN269D_MANIFEST = RUN269D_ROOT / "run_manifest.json"
RUN269D_SUMMARY = RUN269D_ROOT / "score_materialization_summary.csv"
RUN269D_TIER_RECEIPTS = RUN269D_ROOT / "tier_scope_receipts.csv"
RUN269D_DATA_INTEGRITY = RUN269D_ROOT / "data_integrity_receipt.json"
RUN269D_HANDOFF_RESOLUTION = RUN269D_ROOT / "handoff_path_resolution.csv"

CLAIM_BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_"
    "no_deployment_no_onnx_until_candidate_package_gate"
)

PACKAGE_META = {
    "cp269A_asymmetric_nonfilter_reentry_surface": {
        "short_id": "cp269A",
        "fresh_thesis": "asymmetric_nonfilter_upside",
        "role": "selectable_blueprint",
        "primary_score": "candidate_decision_score",
    },
    "cp269B_identity_collapse_disambiguator": {
        "short_id": "cp269B",
        "fresh_thesis": "identity_collapse_reconstruction",
        "role": "selectable_blueprint",
        "primary_score": "divergence_metric",
    },
    "cp269C_session_skew_reward_surface": {
        "short_id": "cp269C",
        "fresh_thesis": "session_skew_reward_surface",
        "role": "selectable_blueprint",
        "primary_score": "session_reward_score",
    },
    "cp269D_runtime_handoff_isolation_control": {
        "short_id": "cp269D",
        "fresh_thesis": "runtime_handoff_isolation",
        "role": "support_control",
        "primary_score": "identity_match_flag",
    },
}


def repo_path(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_json(path: Path, payload: Any, *, bom: bool = False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    encoding = "utf-8-sig" if bom else "utf-8"
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding=encoding)


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_md(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8-sig")


def package_rows(table: pd.DataFrame, package_id: str) -> dict[str, Any]:
    meta = PACKAGE_META[package_id]
    primary_score = meta["primary_score"]
    rows = int(len(table))
    decision_count = int(table["materialized_decision_flag"].sum())
    decision_rate = float(decision_count / rows) if rows else 0.0
    tier_rates = {
        str(tier): float(group["materialized_decision_flag"].mean())
        for tier, group in table.groupby("tier_view", dropna=False)
    }
    split_rates = {
        str(split): float(group["materialized_decision_flag"].mean())
        for split, group in table.groupby("split", dropna=False)
    }
    score = pd.to_numeric(table[primary_score], errors="coerce") if primary_score in table.columns else pd.Series(dtype="float64")
    quantiles = score.quantile([0.1, 0.5, 0.9]).to_dict() if not score.empty else {}
    return {
        "package_id": package_id,
        "package_role": meta["role"],
        "fresh_thesis": meta["fresh_thesis"],
        "rows": rows,
        "decision_count": decision_count,
        "decision_rate": decision_rate,
        "tier_a_decision_rate": tier_rates.get("Tier A separate", 0.0),
        "tier_b_decision_rate": tier_rates.get("Tier B separate", 0.0),
        "train_decision_rate": split_rates.get("train", 0.0),
        "validation_decision_rate": split_rates.get("validation", 0.0),
        "oos_decision_rate": split_rates.get("oos", 0.0),
        "primary_score_p10": float(quantiles.get(0.1, np.nan)),
        "primary_score_median": float(quantiles.get(0.5, np.nan)),
        "primary_score_p90": float(quantiles.get(0.9, np.nan)),
    }


def judge_package(summary: dict[str, Any], table: pd.DataFrame) -> dict[str, str]:
    package_id = summary["package_id"]
    decision_rate = summary["decision_rate"]
    validation_rate = summary["validation_decision_rate"]
    oos_rate = summary["oos_decision_rate"]
    if package_id.startswith("cp269A"):
        if 0.05 <= validation_rate <= 0.35 and 0.05 <= oos_rate <= 0.35:
            return {
                "screening_judgment": "stage270_aggressive_probe_seed",
                "next_action": "queue_for_stage270_aggressive_upside_probe",
                "reason": "nonfilter_reward_skew_surface_has_bounded_supply_without_performance_claim",
            }
        return {
            "screening_judgment": "needs_threshold_reconstruction_before_aggressive_probe",
            "next_action": "reconstruct_score_threshold_before_stage270",
            "reason": "nonfilter_reward_skew_supply_not_in_bounded_screening_band",
        }
    if package_id.startswith("cp269B"):
        duplicate_rate = float(pd.to_numeric(table["duplicate_signature_flag"], errors="coerce").mean())
        if duplicate_rate <= 0.20 and decision_rate <= 0.65:
            return {
                "screening_judgment": "identity_branch_followup_seed",
                "next_action": "hold_for_identity_disambiguation_followup",
                "reason": "identity_divergence_exists_but_not_an_aggressive_upside_surface_yet",
            }
        return {
            "screening_judgment": "identity_surface_too_broad_or_duplicate",
            "next_action": "tighten_identity_threshold_or_downgrade_to_failure_memory",
            "reason": "identity_surface_needs_tighter_nonduplicate_decision_rule",
        }
    if package_id.startswith("cp269C"):
        if decision_rate >= 0.95:
            return {
                "screening_judgment": "reconstruct_before_stage270",
                "next_action": "rebuild_session_skew_decision_surface",
                "reason": "session_surface_all_pass_risk_hides_decision_surface",
            }
        return {
            "screening_judgment": "session_surface_watch",
            "next_action": "hold_for_session_threshold_review",
            "reason": "session_surface_materialized_but_not_stage270_primary_seed",
        }
    if package_id.startswith("cp269D"):
        tier_a_match = float(table.loc[table["tier_view"].eq("Tier A separate"), "identity_match_flag"].mean())
        tier_b_match = float(table.loc[table["tier_view"].eq("Tier B separate"), "identity_match_flag"].mean())
        return {
            "screening_judgment": "support_control_keep",
            "next_action": "carry_as_handoff_identity_control",
            "reason": f"tier_a_identity_match={tier_a_match:.4f};tier_b_partial_context_match={tier_b_match:.4f}",
        }
    raise RuntimeError(f"Unknown package_id: {package_id}")


def materialize() -> dict[str, Any]:
    RUN_ROOT.mkdir(parents=True, exist_ok=True)
    REVIEW_ROOT.mkdir(parents=True, exist_ok=True)

    source_paths = [
        RUN269D_MANIFEST,
        RUN269D_SUMMARY,
        RUN269D_TIER_RECEIPTS,
        RUN269D_DATA_INTEGRITY,
        RUN269D_HANDOFF_RESOLUTION,
        RUN269D_REPORT,
    ]
    source_paths.extend(sorted((RUN269D_ROOT / "scores").glob("*.parquet")))
    source_paths.extend(sorted((RUN269D_ROOT / "handoff").glob("*.json")))
    source_hashes = {repo_path(path): sha256_file(path) for path in source_paths}

    screening_rows: list[dict[str, Any]] = []
    queue_rows: list[dict[str, Any]] = []
    failure_rows: list[dict[str, Any]] = []
    support_rows: list[dict[str, Any]] = []

    for package_id, meta in PACKAGE_META.items():
        table_path = RUN269D_ROOT / "scores" / f"{meta['short_id']}_scores.parquet"
        table = pd.read_parquet(table_path)
        summary = package_rows(table, package_id)
        judgment = judge_package(summary, table)
        row = {
            **summary,
            "decision_rate": round(summary["decision_rate"], 8),
            "tier_a_decision_rate": round(summary["tier_a_decision_rate"], 8),
            "tier_b_decision_rate": round(summary["tier_b_decision_rate"], 8),
            "train_decision_rate": round(summary["train_decision_rate"], 8),
            "validation_decision_rate": round(summary["validation_decision_rate"], 8),
            "oos_decision_rate": round(summary["oos_decision_rate"], 8),
            "primary_score_p10": round(summary["primary_score_p10"], 8) if np.isfinite(summary["primary_score_p10"]) else "",
            "primary_score_median": round(summary["primary_score_median"], 8) if np.isfinite(summary["primary_score_median"]) else "",
            "primary_score_p90": round(summary["primary_score_p90"], 8) if np.isfinite(summary["primary_score_p90"]) else "",
            **judgment,
            "selected_candidate": "none",
            "onnx_readiness": "not_claimed",
            "performance_claim": "none",
        }
        screening_rows.append(row)
        if judgment["screening_judgment"] == "stage270_aggressive_probe_seed":
            queue_rows.append(
                {
                    "queue_id": "stage270_q01_cp269A_aggressive_nonfilter_reward_skew",
                    "package_id": package_id,
                    "source_run": RUN_ID,
                    "queue_role": "aggressive_upside_probe_seed",
                    "required_support_control": "cp269D_runtime_handoff_isolation_control",
                    "required_inputs": "score_table;handoff_json;tier_scope_receipts;data_integrity_receipt",
                    "success_probe_question": "Can bounded non-filter reward skew produce upside before stability review?",
                    "failure_mode_to_watch": "trade_supply_inflation_or_weak_context_damage",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
        elif judgment["screening_judgment"] in {"reconstruct_before_stage270", "identity_surface_too_broad_or_duplicate"}:
            failure_rows.append(
                {
                    "package_id": package_id,
                    "failed_boundary": judgment["screening_judgment"],
                    "why_failed_or_not_ready": judgment["reason"],
                    "salvage_value": "reconstruct_decision_surface" if package_id.startswith("cp269C") else "tighten_identity_threshold",
                    "reopen_condition": "new_decision_surface_with_bounded_supply_and_hash_receipt",
                    "do_not_repeat_note": "do_not_treat_all_pass_or_duplicate_surface_as_candidate",
                }
            )
        elif meta["role"] == "support_control":
            support_rows.append(
                {
                    "package_id": package_id,
                    "support_role": "handoff_identity_control",
                    "screening_judgment": judgment["screening_judgment"],
                    "carry_condition": "required_for_stage270_handoff_identity_checks",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )

    screening_path = RUN_ROOT / "package_screening_summary.csv"
    write_csv(
        screening_path,
        screening_rows,
        [
            "package_id",
            "package_role",
            "fresh_thesis",
            "rows",
            "decision_count",
            "decision_rate",
            "tier_a_decision_rate",
            "tier_b_decision_rate",
            "train_decision_rate",
            "validation_decision_rate",
            "oos_decision_rate",
            "primary_score_p10",
            "primary_score_median",
            "primary_score_p90",
            "screening_judgment",
            "next_action",
            "reason",
            "selected_candidate",
            "onnx_readiness",
            "performance_claim",
        ],
    )
    queue_path = RUN_ROOT / "stage270_aggressive_probe_queue.csv"
    write_csv(
        queue_path,
        queue_rows,
        [
            "queue_id",
            "package_id",
            "source_run",
            "queue_role",
            "required_support_control",
            "required_inputs",
            "success_probe_question",
            "failure_mode_to_watch",
            "claim_boundary",
        ],
    )
    failure_path = RUN_ROOT / "screening_failure_memory.csv"
    write_csv(
        failure_path,
        failure_rows,
        [
            "package_id",
            "failed_boundary",
            "why_failed_or_not_ready",
            "salvage_value",
            "reopen_condition",
            "do_not_repeat_note",
        ],
    )
    support_path = RUN_ROOT / "support_control_carry.csv"
    write_csv(
        support_path,
        support_rows,
        [
            "package_id",
            "support_role",
            "screening_judgment",
            "carry_condition",
            "claim_boundary",
        ],
    )

    output_paths = [screening_path, queue_path, failure_path, support_path]
    output_hashes = {repo_path(path): sha256_file(path) for path in output_paths}

    manifest_path = RUN_ROOT / "run_manifest.json"
    manifest_payload = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "status": "completed_score_surface_screen_no_candidate_selection",
        "producer": "stage_pipelines/stage269/screen_materialized_scores.py",
        "entry_command": "python stage_pipelines/stage269/screen_materialized_scores.py",
        "source_inputs": list(source_hashes.keys()),
        "input_hashes": source_hashes,
        "output_artifacts": list(output_hashes.keys()),
        "output_hashes": output_hashes,
        "screened_packages": len(screening_rows),
        "stage270_queue_rows": len(queue_rows),
        "failure_memory_rows": len(failure_rows),
        "support_control_rows": len(support_rows),
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "external_verification_status": "out_of_scope_by_claim_score_screening_only",
        "claim_boundary": CLAIM_BOUNDARY,
        "next_action": "open_stage270_aggressive_upside_probe_from_run269E_queue",
    }
    write_json(manifest_path, manifest_payload)

    report_path = REVIEW_ROOT / "run269E_report.md"
    queued = "; ".join(row["package_id"] for row in queue_rows) if queue_rows else "none"
    report = f"""# Stage269 Run269E Materialized Score Surface Screen(269단계 269E 물질화 점수 표면 선별)

- status(상태): `completed_score_surface_screen_no_candidate_selection`
- run(실행): `{RUN_ID}`
- source_run(원천 실행): `run269D_scoring_materialization_probe_v1`
- screened_packages(선별 패키지): `{len(screening_rows)}`
- stage270_queue_rows(270단계 대기열 행): `{len(queue_rows)}`
- queued_package(대기 패키지): `{queued}`
- failure_memory_rows(실패 기억 행): `{len(failure_rows)}`
- selected_candidate(선택 후보): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `open_stage270_aggressive_upside_probe_from_run269E_queue`

## Plain Result(쉬운 결과)

run269E(269E 실행)는 run269D(269D 실행)의 score table(점수표)을 성과가 아니라 구조로 선별했다.
효과(effect, 효과): `cp269A_asymmetric_nonfilter_reentry_surface`는 Stage270(270단계) aggressive upside probe(공격형 상방 탐침) seed(씨앗)로 넘기고, `cp269C_session_skew_reward_surface`는 all-pass risk(전체 통과 위험) 때문에 재구성 기억으로 낮췄다. `cp269B_identity_collapse_disambiguator`는 identity follow-up(정체성 후속)으로 보류하고, `cp269D_runtime_handoff_isolation_control`은 support control(보조 대조)로 유지한다.

## Result Judgment(결과 판정)

- result_subject(판정 대상): materialized score surfaces(물질화된 점수 표면)
- evidence_available(있는 근거): score tables(점수표), handoff JSON(인계 JSON), tier receipts(티어 영수증), data integrity receipt(데이터 무결성 영수증)
- evidence_missing(빠진 근거): trading KPI(거래 핵심 성과 지표), balance/equity curve(잔액/평가금 곡선), MT5 runtime output(MT5 런타임 출력), ONNX export/parity(온엑스 내보내기/동등성)
- judgment_label(판정 라벨): `screened_for_next_probe_no_candidate_selection`
- claim_boundary(주장 경계): research/development only(연구/개발 전용)
- next_condition(다음 조건): Stage270(270단계)에서 cp269A(269A 패키지)를 aggressive upside probe(공격형 상방 탐침)로 실행해 upside/failure mode/discard condition(상방/실패 방식/폐기 조건)을 기록해야 한다.

## Boundary(경계)

This report(이 보고서)는 selected candidate(선택 후보), ONNX readiness(온엑스 준비), deployment(배포), live readiness(실거래 준비), runtime authority(런타임 권위), operating promotion(운영 승격), operating reference(운영 기준), production baseline(운영 기준선), Goal Achieve(목표 달성)를 주장하지 않는다.
"""
    write_md(report_path, report)

    lineage_path = RUN_ROOT / "lineage.json"
    lineage_payload = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "source_inputs": list(source_hashes.keys()),
        "producer": "stage_pipelines/stage269/screen_materialized_scores.py",
        "consumer": "open_stage270_aggressive_upside_probe_from_run269E_queue",
        "artifact_paths": [repo_path(path) for path in [manifest_path, *output_paths, lineage_path, report_path]],
        "artifact_hashes": {
            **source_hashes,
            **output_hashes,
            repo_path(manifest_path): sha256_file(manifest_path),
            repo_path(report_path): sha256_file(report_path),
        },
        "self_hash_note": "lineage file hash is recorded in docs/registers/artifact_registry.csv after generation",
        "registry_links": [
            "docs/registers/run_registry.csv",
            "docs/registers/alpha_run_ledger.csv",
            f"stages/{STAGE_ID}/03_reviews/stage_run_ledger.csv",
            "docs/registers/artifact_registry.csv",
        ],
        "availability": "tracked",
        "lineage_judgment": "connected_with_boundary",
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_json(lineage_path, lineage_payload)

    final_hashes = {repo_path(path): sha256_file(path) for path in [manifest_path, *output_paths, lineage_path, report_path]}
    return {
        "run_id": RUN_ID,
        "status": manifest_payload["status"],
        "screened_packages": len(screening_rows),
        "stage270_queue_rows": len(queue_rows),
        "failure_memory_rows": len(failure_rows),
        "outputs": final_hashes,
    }


if __name__ == "__main__":
    print(json.dumps(materialize(), ensure_ascii=False, indent=2))
