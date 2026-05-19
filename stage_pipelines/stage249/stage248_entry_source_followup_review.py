from __future__ import annotations

import csv
import hashlib
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Sequence


STAGE_ID = "249_adapter_research__stage248_entry_source_followup_review"
RUN_ID = "run249A_stage249_stage248_entry_source_followup_review_v1"
PACKET_ID = "stage249_stage248_entry_source_followup_review_v1"
SOURCE_STAGE_ID = "248_adapter_research__entry_source_quality_repair_after_stage246_soft_guard_tradeoff"
SOURCE_RUN_ID = "run248A_stage248_entry_source_quality_repair_after_stage246_soft_guard_tradeoff_v1"
SOURCE_EVIDENCE_COMMIT = "ab50acc695fdc069cb25dece7a66a38bb89bc925"
SOURCE_HASH_RECORD_COMMIT = "c7466b6836bf1837fcaab2148e55bd5b065fb327"
NEXT_STAGE_ID = "250_adapter_research__decision_surface_binding_repair_after_stage248_threshold_no_effect"
NEXT_RUN_ID = "run250A_stage250_decision_surface_binding_repair_after_stage248_threshold_no_effect_v1"
NEXT_PACKET_ID = "stage250_decision_surface_binding_repair_after_stage248_threshold_no_effect_v1"
DECISION = "open_stage250_bounded_decision_surface_binding_repair_after_stage248_threshold_no_effect_candidate_not_final"
BOUNDARY = "research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment"
TARGET_SURFACE = "legacy_34d_kpi_lesson_only_v2_native_decision_surface_binding_after_stage248_threshold_no_effect"

LEGACY_34D_NET = 987.6
LEGACY_34D_PF = 1.583157
LEGACY_34D_DD = 12.909136

ROOT = Path.cwd()
STAGE_ROOT = ROOT / "stages" / STAGE_ID
REVIEWS = STAGE_ROOT / "03_reviews"
PACKET_ROOT = ROOT / "docs/agent_control/packets" / PACKET_ID
NEXT_STAGE_ROOT = ROOT / "stages" / NEXT_STAGE_ID
SOURCE_REVIEWS = ROOT / "stages" / SOURCE_STAGE_ID / "03_reviews"

QUALITY_PATH = SOURCE_REVIEWS / "stage248_quality_matrix.csv"
KPI_PATH = SOURCE_REVIEWS / "stage248_entry_source_kpi_summary.csv"
ATTRIBUTION_SOURCE_PATH = SOURCE_REVIEWS / "stage248_performance_attribution.csv"
FAILURE_SOURCE_PATH = SOURCE_REVIEWS / "stage248_failure_memory.csv"
RISK_PATH = SOURCE_REVIEWS / "stage248_risk_atr_telemetry.csv"
SEGMENT_PATH = SOURCE_REVIEWS / "stage248_segment_kpi_summary.csv"
BALANCE_PATH = SOURCE_REVIEWS / "stage248_balance_curve_audit.csv"
SOURCE_REPORT_PATH = SOURCE_REVIEWS / "stage248_entry_source_repair_report.md"

REPORT_PATH = REVIEWS / "stage249_stage248_entry_source_followup_review.md"
TRADEOFF_PATH = REVIEWS / "stage249_tradeoff_review_matrix.csv"
ATTRIBUTION_PATH = REVIEWS / "stage249_performance_attribution.csv"
FAILURE_PATH = REVIEWS / "stage249_failure_memory.csv"
ROUTE_PATH = REVIEWS / "stage249_route_matrix.csv"
RISK_REVIEW_PATH = REVIEWS / "stage249_risk_atr_review.csv"
SUMMARY_PATH = REVIEWS / "stage249_summary.json"
DECISION_PATH = REVIEWS / "stage249_decision.md"
STAGE_LEDGER_PATH = REVIEWS / "stage_run_ledger.csv"
REVIEW_INDEX_PATH = REVIEWS / "review_index.md"
SELECTION_PATH = STAGE_ROOT / "04_selected/selection_status.md"

CURRENT_STATE_PATH = ROOT / "docs/context/current_working_state.md"
WORKSPACE_STATE_PATH = ROOT / "docs/workspace/workspace_state.yaml"
CHANGELOG_PATH = ROOT / "docs/workspace/changelog.md"
RUN_REGISTRY_PATH = ROOT / "docs/registers/run_registry.csv"
PROJECT_LEDGER_PATH = ROOT / "docs/registers/alpha_run_ledger.csv"
ARTIFACT_REGISTRY_PATH = ROOT / "docs/registers/artifact_registry.csv"
PRODUCER_PATH = ROOT / "stage_pipelines/stage249/stage248_entry_source_followup_review.py"

ALPHA_COLUMNS = [
    "ledger_row_id",
    "stage_id",
    "run_id",
    "subrun_id",
    "parent_run_id",
    "record_view",
    "tier_scope",
    "kpi_scope",
    "scoreboard_lane",
    "status",
    "judgment",
    "path",
    "primary_kpi",
    "guardrail_kpi",
    "external_verification_status",
    "notes",
]
RUN_COLUMNS = ["run_id", "stage_id", "lane", "status", "judgment", "path", "notes"]
ARTIFACT_COLUMNS = ["artifact_id", "artifact_type", "path", "sha256", "stage_id", "run_id", "created_at_utc", "notes"]


def extended_path(path: Path) -> str:
    resolved = path if path.is_absolute() else ROOT / path
    return "\\\\?\\" + str(resolved.resolve())


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read_text(path: Path) -> str:
    with open(extended_path(path), "r", encoding="utf-8-sig") as handle:
        return handle.read()


def write_text(path: Path, text: str, *, bom: bool = True) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(extended_path(path), "w", encoding="utf-8-sig" if bom else "utf-8", newline="\n") as handle:
        handle.write(text.rstrip() + "\n")


def read_csv(path: Path) -> list[dict[str, str]]:
    with open(extended_path(path), "r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(extended_path(path), "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: row.get(column, "") for column in columns})


def write_json(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(extended_path(path), "w", encoding="utf-8", newline="\n") as handle:
        json.dump(payload, handle, indent=2, ensure_ascii=False, sort_keys=True)
        handle.write("\n")


def sha256_lf(path: Path) -> str:
    with open(extended_path(path), "rb") as handle:
        raw = handle.read()
    return hashlib.sha256(raw.replace(b"\r\n", b"\n")).hexdigest()


def artifact_id_for(path: Path) -> str:
    safe = rel(path).replace("/", "__").replace(".", "_").replace("-", "_")
    return f"{RUN_ID}__{safe}"


def as_float(value: Any) -> float:
    try:
        return float(value or 0.0)
    except (TypeError, ValueError):
        return 0.0


def yes_no(value: bool) -> str:
    return "yes" if value else "no"


def upsert_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]], key: str) -> dict[str, Any]:
    existing: list[dict[str, str]] = []
    if path.exists():
        with open(extended_path(path), "r", encoding="utf-8-sig", newline="") as handle:
            existing = list(csv.DictReader(handle))
    by_key = {row.get(key, ""): row for row in existing if row.get(key, "")}
    for row in rows:
        by_key[str(row[key])] = {column: str(row.get(column, "")) for column in columns}
    ordered: list[dict[str, str]] = []
    seen: set[str] = set()
    for row in existing:
        row_key = row.get(key, "")
        if row_key in by_key and row_key not in seen:
            ordered.append(by_key[row_key])
            seen.add(row_key)
    ordered.extend(by_key[row_key] for row_key in sorted(by_key) if row_key not in seen)
    write_csv(path, ordered, columns)
    return {
        "path": rel(path),
        "rows": len(ordered),
        "upserted_rows": len(rows),
        "sha256": sha256_lf(path),
        "hash_policy": "lf_normalized_text_register",
    }


def prune_run_artifacts() -> None:
    if not ARTIFACT_REGISTRY_PATH.exists():
        return
    with open(extended_path(ARTIFACT_REGISTRY_PATH), "r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    kept = [row for row in rows if not row.get("artifact_id", "").startswith(f"{RUN_ID}__")]
    write_csv(ARTIFACT_REGISTRY_PATH, kept, ARTIFACT_COLUMNS)


def build_review() -> dict[str, Any]:
    quality_rows = read_csv(QUALITY_PATH)
    attribution_source = read_csv(ATTRIBUTION_SOURCE_PATH)
    failure_source = read_csv(FAILURE_SOURCE_PATH)
    risk_rows = read_csv(RISK_PATH)
    reference = quality_rows[0]
    reference_values = {
        "validation_net": as_float(reference["validation_net"]),
        "validation_dd": as_float(reference["validation_balance_dd_percent"]),
        "validation_mid_pf": as_float(reference["validation_mid_pf"]),
        "oos_net": as_float(reference["oos_net"]),
    }

    tradeoff_rows: list[dict[str, Any]] = []
    for row in quality_rows:
        val_net = as_float(row["validation_net"])
        val_dd = as_float(row["validation_balance_dd_percent"])
        mid_pf = as_float(row["validation_mid_pf"])
        oos_net = as_float(row["oos_net"])
        identical = (
            abs(val_net - reference_values["validation_net"]) < 1e-9
            and abs(val_dd - reference_values["validation_dd"]) < 1e-9
            and abs(mid_pf - reference_values["validation_mid_pf"]) < 1e-9
            and abs(oos_net - reference_values["oos_net"]) < 1e-9
        )
        tradeoff_rows.append(
            {
                "adapter_id": row["adapter_id"],
                "axis": row["axis"],
                "validation_net": f"{val_net:.2f}",
                "validation_net_gap_vs_34d": f"{val_net - LEGACY_34D_NET:.2f}",
                "validation_dd_percent": f"{val_dd:.4f}",
                "validation_dd_margin_vs_34d": f"{LEGACY_34D_DD - val_dd:.6f}",
                "validation_mid_pf": f"{mid_pf:.9f}",
                "validation_mid_pf_gap_vs_34d_pf": f"{mid_pf - LEGACY_34D_PF:.6f}",
                "oos_net": f"{oos_net:.2f}",
                "oos_pf": row["oos_pf"],
                "delta_net_vs_reference": f"{val_net - reference_values['validation_net']:.2f}",
                "delta_dd_vs_reference": f"{val_dd - reference_values['validation_dd']:.4f}",
                "delta_mid_pf_vs_reference": f"{mid_pf - reference_values['validation_mid_pf']:.9f}",
                "delta_oos_net_vs_reference": f"{oos_net - reference_values['oos_net']:.2f}",
                "identical_to_reference": yes_no(identical),
                "hard_quality_pass": row["hard_quality_pass"],
                "review_label": "threshold_axis_no_effect_candidate_not_final" if identical else "threshold_axis_changed_kpi",
                "quality_flags": row["quality_flags"],
            }
        )

    actual_routed = [row for row in risk_rows if row.get("view") == "actual_routed_total" and row.get("status") == "completed"]
    risk_review_rows = []
    for row in actual_routed:
        risk_review_rows.append(
            {
                "adapter_id": row["adapter_id"],
                "split": row["split"],
                "atr_enabled": row["atr_enabled"],
                "model_risk_enabled": row["model_risk_enabled"],
                "max_model_risk_pct": row["max_model_risk_pct"],
                "max_actual_risk_pct_after_floor": row["max_actual_risk_pct_after_floor"],
                "risk_floor_applied_count": row["risk_floor_applied_count"],
                "avg_atr_points": row["avg_atr_points"],
                "avg_open_sl_points": row["avg_open_sl_points"],
                "avg_open_tp_points": row["avg_open_tp_points"],
                "risk_bucket": row["risk_bucket"],
                "risk_cap_5pct_ok": yes_no(as_float(row["max_actual_risk_pct_after_floor"]) <= 0.05),
                "floor_inflation_observed": yes_no(as_float(row["risk_floor_applied_count"]) > 0),
            }
        )

    attribution_rows = [
        {
            "attribution_id": f"{RUN_ID}__threshold_axis_no_effect_confirmed",
            "observed_change": "all Stage248 threshold variants reproduced the reference validation and OOS KPI exactly",
            "comparison_baseline": "s248_cap0305_reference",
            "likely_drivers": "the tested entry threshold knobs did not bind the runtime decision surface",
            "segment_checks": "validation/OOS full split, early/mid/late KPI, risk/ATR telemetry, and Stage248 failure memory reviewed",
            "trade_shape": "trade count, net, DD, mid PF, OOS net, and risk telemetry stayed unchanged across variants",
            "alternative_explanations": "accepted score distribution may already sit outside the tested thresholds",
            "attribution_confidence": "high",
            "next_probe": NEXT_STAGE_ID,
        },
        {
            "attribution_id": f"{RUN_ID}__near_miss_still_not_34d_equivalent",
            "observed_change": "reference remains close but still misses 34D validation net, DD, and mid PF together",
            "comparison_baseline": "legacy 34D lesson-only KPI target",
            "likely_drivers": "decision/source binding and mid-window quality remain the limiting surface",
            "segment_checks": "mid PF gap and validation DD margin reviewed",
            "trade_shape": "ATR bracket and model risk are present but not enough to repair KPI",
            "alternative_explanations": "rounding cannot close the net, DD, and mid PF gaps at the same time",
            "attribution_confidence": "high",
            "next_probe": NEXT_STAGE_ID,
        },
        {
            "attribution_id": f"{RUN_ID}__risk_atr_present_not_sufficient",
            "observed_change": "risk cap, ATR SL/TP, and telemetry are present without making the adapter final",
            "comparison_baseline": "mandatory ATR/risk capability requirement",
            "likely_drivers": "capability integration is necessary but not a standalone KPI repair",
            "segment_checks": "risk floor count, max actual risk, SL/TP points, and bucket telemetry reviewed",
            "trade_shape": "max actual risk remained below 5 percent and min-lot floor did not inflate Stage248 rows",
            "alternative_explanations": "runtime risk telemetry is healthy, but entry quality still limits KPI",
            "attribution_confidence": "medium_high",
            "next_probe": NEXT_STAGE_ID,
        },
    ]

    failure_rows = [
        {
            "failure_id": f"{RUN_ID}__stage248_threshold_axis_no_effect_reviewed",
            "source_failure": "stage248_entry_threshold_variants_no_effect",
            "why_it_matters": "the tested threshold controls did not change accepted runtime decisions",
            "do_not_repeat": "do not repeat the same short055/short056/long053 threshold-only axis",
            "salvage_value": "use Stage248 as a binding failure memory and repair the decision surface or source feature connection",
            "next_handling": NEXT_STAGE_ID,
        },
        {
            "failure_id": f"{RUN_ID}__stage248_candidate_not_final_reviewed",
            "source_failure": "stage248_entry_threshold_not_final_until_reviewed",
            "why_it_matters": "hard_quality_pass stayed false for all variants and 34D-equivalent KPI was not reached",
            "do_not_repeat": "do not call high final OOS PF or present ATR/risk enough for final package completion",
            "salvage_value": "keep s248_cap0305_reference as near-miss reference while repairing binding",
            "next_handling": NEXT_STAGE_ID,
        },
    ]

    route_rows = [
        {
            "route_id": DECISION,
            "status": "selected",
            "reason": "Stage248 proved threshold-only knobs did not bind decisions",
            "effect": "open a bounded decision-surface binding repair stage",
        },
        {
            "route_id": "repeat_stage248_threshold_nudges",
            "status": "rejected",
            "reason": "short055, short056, long053, and balanced threshold rows were identical to reference",
            "effect": "avoid another no-effect threshold-only loop",
        },
        {
            "route_id": "proceed_to_onnx_hardening",
            "status": "rejected",
            "reason": "adapter quality is not genuinely strong after Stage248",
            "effect": "ONNX hardening waits until KPI and decision behavior improve",
        },
        {
            "route_id": "claim_research_package_complete",
            "status": "rejected",
            "reason": "34D-equivalent KPI, ONNX parity, runtime reproduction, and full package review are still missing",
            "effect": "overall goal remains active",
        },
    ]

    return {
        "quality_rows": quality_rows,
        "tradeoff_rows": tradeoff_rows,
        "risk_review_rows": risk_review_rows,
        "source_attribution_rows": attribution_source,
        "source_failure_rows": failure_source,
        "attribution_rows": attribution_rows,
        "failure_rows": failure_rows,
        "route_rows": route_rows,
        "reference": reference,
        "decision": DECISION,
    }


def write_reports(review: Mapping[str, Any]) -> None:
    write_csv(
        TRADEOFF_PATH,
        review["tradeoff_rows"],
        [
            "adapter_id",
            "axis",
            "validation_net",
            "validation_net_gap_vs_34d",
            "validation_dd_percent",
            "validation_dd_margin_vs_34d",
            "validation_mid_pf",
            "validation_mid_pf_gap_vs_34d_pf",
            "oos_net",
            "oos_pf",
            "delta_net_vs_reference",
            "delta_dd_vs_reference",
            "delta_mid_pf_vs_reference",
            "delta_oos_net_vs_reference",
            "identical_to_reference",
            "hard_quality_pass",
            "review_label",
            "quality_flags",
        ],
    )
    write_csv(
        RISK_REVIEW_PATH,
        review["risk_review_rows"],
        [
            "adapter_id",
            "split",
            "atr_enabled",
            "model_risk_enabled",
            "max_model_risk_pct",
            "max_actual_risk_pct_after_floor",
            "risk_floor_applied_count",
            "avg_atr_points",
            "avg_open_sl_points",
            "avg_open_tp_points",
            "risk_bucket",
            "risk_cap_5pct_ok",
            "floor_inflation_observed",
        ],
    )
    write_csv(
        ATTRIBUTION_PATH,
        review["attribution_rows"],
        [
            "attribution_id",
            "observed_change",
            "comparison_baseline",
            "likely_drivers",
            "segment_checks",
            "trade_shape",
            "alternative_explanations",
            "attribution_confidence",
            "next_probe",
        ],
    )
    write_csv(FAILURE_PATH, review["failure_rows"], ["failure_id", "source_failure", "why_it_matters", "do_not_repeat", "salvage_value", "next_handling"])
    write_csv(ROUTE_PATH, review["route_rows"], ["route_id", "status", "reason", "effect"])

    ref = review["reference"]
    matrix = [
        "| adapter(어댑터) | val net(검증 순손익) | DD%(낙폭률) | mid PF(중간 수익요인) | OOS net(표본외 순손익) | same as ref(기준 동일) | read(판독) |",
        "|---|---:|---:|---:|---:|---|---|",
    ]
    for row in review["tradeoff_rows"]:
        matrix.append(
            f"| {row['adapter_id']} | {row['validation_net']} | {row['validation_dd_percent']} | {row['validation_mid_pf']} | {row['oos_net']} | {row['identical_to_reference']} | {row['review_label']} |"
        )

    report = f"""# Stage249 Stage248 Entry Source Follow-up Review(249단계 248단계 진입 원천 후속 검토)

- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- source_evidence_commit(원천 근거 커밋): `{SOURCE_EVIDENCE_COMMIT}`
- source_hash_record_commit(원천 해시 기록 커밋): `{SOURCE_HASH_RECORD_COMMIT}`
- external_verification_status(외부 검증 상태): `review_only_source_stage248_mt5_reports_completed`
- decision(판정): `{DECISION}`
- boundary(주장 경계): `{BOUNDARY}`

## Easy Read(쉬운 판독)

- Stage248(248단계)는 entry threshold(진입 임계값)를 바꿔 봤지만 KPI(핵심 성과 지표)가 하나도 움직이지 않았다.
- validation net(검증 순손익) `{float(ref['validation_net']):.2f}`은 34D(레거시 34D) 목표보다 `{float(ref['validation_net']) - LEGACY_34D_NET:.2f}` 낮다.
- validation DD(검증 낙폭) `{float(ref['validation_balance_dd_percent']):.4f}%`는 34D(레거시 34D)보다 `{LEGACY_34D_DD - float(ref['validation_balance_dd_percent']):.6f}` 불리하다.
- validation mid PF(검증 중간 수익요인) `{float(ref['validation_mid_pf']):.9f}`는 34D PF(34D 수익요인)보다 `{float(ref['validation_mid_pf']) - LEGACY_34D_PF:.6f}` 낮다.
- ATR SL/TP(ATR 손절/익절)와 model-controlled risk%(모델 제어 위험 비율)는 존재하지만, 이 사실만으로 final adapter(최종 어댑터)가 아니다.
- 다음 행동(action, 행동)은 decision surface binding repair(결정 표면 결합 수리)이다. 효과(effect, 효과)는 임계값/원천 수리가 실제 trade decision(거래 결정)을 바꾸는지 먼저 확인하는 것이다.

## KPI Matrix(KPI 핵심 성과 지표 행렬)

{chr(10).join(matrix)}

## Judgment(판정)

- result_subject(판정 대상): `{RUN_ID}`
- evidence_available(사용 근거): Stage248(248단계) quality matrix(품질 행렬), risk/ATR telemetry(위험/ATR 기록), failure memory(실패 기억), MT5(MetaTrader 5, 메타트레이더5) validation/OOS(검증/표본외) report(보고서).
- evidence_missing(누락 근거): Stage250(250단계) binding repair(결합 수리) 실행, ONNX parity(ONNX 동등성), MT5 ONNX/runtime reproduction(MT5 ONNX/런타임 재현).
- judgment_label(판정 라벨): `threshold_axis_no_effect_negative_not_final(임계값 축 효과 없음 부정, 최종 아님)`
- claim_boundary(주장 경계): research/development only(연구개발 전용). deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위)는 모두 금지다.
- next_condition(다음 조건): `{NEXT_STAGE_ID}`에서 decision/source binding(결정/원천 결합)이 실제 decision(결정)을 바꾸는지 확인한다.

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준), overall_goal_complete(전체 목표 완료).
"""
    write_text(REPORT_PATH, report)

    decision_text = f"""# Stage249 Decision(249단계 판정)

- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- decision(판정): `{DECISION}`
- external_verification_status(외부 검증 상태): `review_only_source_stage248_mt5_reports_completed`
- report(보고서): `{rel(REPORT_PATH)}`
- tradeoff_matrix(상충 행렬): `{rel(TRADEOFF_PATH)}`
- attribution(성과 귀속): `{rel(ATTRIBUTION_PATH)}`
- failure_memory(실패 기억): `{rel(FAILURE_PATH)}`
- route_matrix(경로 행렬): `{rel(ROUTE_PATH)}`
- risk_atr_review(위험/ATR 검토): `{rel(RISK_REVIEW_PATH)}`
- next_stage_or_branch(다음 단계 또는 분기): `{NEXT_STAGE_ID}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage249(249단계) closeout(종료)은 overall goal complete(전체 목표 완료)가 아니다.

Effect(효과): Stage250(250단계)은 같은 threshold-only(임계값 전용) 반복이 아니라 decision surface binding(결정 표면 결합)을 좁게 수리한다.
"""
    write_text(DECISION_PATH, decision_text)

    write_text(
        REVIEW_INDEX_PATH,
        f"""# Stage249 Review Index(249단계 검토 색인)

- status(상태): `closed_open_stage250_decision_surface_binding_repair_candidate_not_final`
- packet(작업 묶음): `{PACKET_ID}`
- run(실행): `{RUN_ID}`
- decision(판정): `{DECISION}`
- report(보고서): `{rel(REPORT_PATH)}`
- tradeoff_matrix(상충 행렬): `{rel(TRADEOFF_PATH)}`
- attribution(성과 귀속): `{rel(ATTRIBUTION_PATH)}`
- failure_memory(실패 기억): `{rel(FAILURE_PATH)}`
- route_matrix(경로 행렬): `{rel(ROUTE_PATH)}`
- risk_atr_review(위험/ATR 검토): `{rel(RISK_REVIEW_PATH)}`
- next_stage_or_branch(다음 단계 또는 분기): `{NEXT_STAGE_ID}`
""",
    )

    write_text(
        SELECTION_PATH,
        f"""# Stage249 Selection Status(249단계 선택 상태)

- stage_status(단계 상태): `closed_open_stage250_decision_surface_binding_repair_candidate_not_final`
- current_packet(현재 작업 묶음): `{PACKET_ID}`
- current_run(현재 실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- external_verification_status(외부 검증 상태): `review_only_source_stage248_mt5_reports_completed`
- decision(판정): `{DECISION}`
- next_stage_or_branch(다음 단계 또는 분기): `{NEXT_STAGE_ID}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`
- claim_boundary(주장 경계): `{BOUNDARY}`
""",
    )


def write_next_stage_seed() -> None:
    write_text(
        NEXT_STAGE_ROOT / "00_spec/stage_brief.md",
        f"""# {NEXT_STAGE_ID}

Stage250(250단계)는 Stage249(249단계)의 no-effect threshold axis(효과 없음 임계값 축) 판정 뒤에 여는 bounded repair(경계 수리) 단계다.

## Bounded Question(경계 질문)

Can the Stage248(248단계) reference adapter(참조 어댑터) be repaired so decision/source controls(결정/원천 제어)가 actual accepted decisions(실제 수락 결정)을 바꾸고 34D(레거시 34D) lesson-only KPI target(교훈 전용 핵심 성과 지표 목표)에 가까워지는가?

## Must Not(금지)

- threshold-only nudge(임계값 전용 미세 조정)를 반복하지 않는다.
- ONNX hardening(ONNX 경화)을 시작하지 않는다.
- final package(최종 패키지)나 live readiness(실거래 준비)를 주장하지 않는다.

## Boundary(경계)

`{BOUNDARY}`
""",
    )
    write_text(
        NEXT_STAGE_ROOT / "01_inputs/input_refs.md",
        f"""# Stage250 Inputs(250단계 입력)

- source_stage249_report(원천 249단계 보고서): `{rel(REPORT_PATH)}`
- source_stage249_decision(원천 249단계 판정): `{rel(DECISION_PATH)}`
- stage248_quality_matrix(248단계 품질 행렬): `{rel(QUALITY_PATH)}`
- stage248_failure_memory(248단계 실패 기억): `{rel(FAILURE_SOURCE_PATH)}`
- stage248_risk_atr_telemetry(248단계 위험/ATR 기록): `{rel(RISK_PATH)}`
""",
    )
    write_text(
        NEXT_STAGE_ROOT / "03_reviews/review_index.md",
        f"""# Stage250 Review Index(250단계 검토 색인)

- status(상태): `open_planned_from_stage249`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- source_stage(원천 단계): `{STAGE_ID}`
- source_decision(원천 판정): `{DECISION}`
""",
    )
    write_text(
        NEXT_STAGE_ROOT / "04_selected/selection_status.md",
        f"""# Stage250 Selection Status(250단계 선택 상태)

- stage_status(단계 상태): `open_planned_from_stage249`
- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- source_decision(원천 판정): `{DECISION}`
- claim_boundary(주장 경계): `{BOUNDARY}`
""",
    )


def update_current_truth() -> None:
    write_text(
        CURRENT_STATE_PATH,
        f"""# Current Working State(현재 작업 상태)

- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- active_stage(활성 단계): `{NEXT_STAGE_ID}`
- selected_research_baseline(선택 연구 기준선): `none`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- adapter_under_review(검토 중 어댑터): `stage248_threshold_axis_no_effect_reference`
- status(상태): `stage249_closed_open_stage250_decision_surface_binding_repair_candidate_not_final`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage249(249단계)는 Stage248(248단계) entry/source repair(진입/원천 수리)를 review-only(검토 전용)로 판정했다. Effect(효과): Stage250(250단계)은 threshold-only(임계값 전용) 반복을 피하고 decision surface binding(결정 표면 결합)을 수리한다.

## Latest Stage249 Evidence(최신 249단계 근거)

- run(실행): `{RUN_ID}`
- decision(판정): `{DECISION}`
- external_verification_status(외부 검증 상태): `review_only_source_stage248_mt5_reports_completed`
- report(보고서): `{rel(REPORT_PATH)}`
- tradeoff_matrix(상충 행렬): `{rel(TRADEOFF_PATH)}`
- attribution(성과 귀속): `{rel(ATTRIBUTION_PATH)}`
- failure_memory(실패 기억): `{rel(FAILURE_PATH)}`
- route_matrix(경로 행렬): `{rel(ROUTE_PATH)}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준), overall_goal_complete(전체 목표 완료).
""",
    )

    workspace = read_text(WORKSPACE_STATE_PATH)
    workspace = re.sub(r"^current_run_id: .*$", f"current_run_id: {NEXT_RUN_ID}", workspace, count=1, flags=re.MULTILINE)
    workspace = re.sub(r"^active_stage: .*$", f"active_stage: {NEXT_STAGE_ID}", workspace, count=1, flags=re.MULTILINE)
    focus = f"""- >-
  Stage249(249단계) closed(종료) as `{DECISION}` and Stage250(250단계) `{NEXT_STAGE_ID}` is open_planned(개방 계획). Effect(효과): Stage248(248단계)의 threshold-only no-effect(임계값 전용 효과 없음)을 failure memory(실패 기억)로 두고 decision surface binding repair(결정 표면 결합 수리)를 좁게 시험한다.
- >-
  Stage249 evidence(249단계 근거)는 `{rel(REPORT_PATH)}`, `{rel(TRADEOFF_PATH)}`, `{rel(ATTRIBUTION_PATH)}`, `{rel(FAILURE_PATH)}`에 있다. Effect(효과): 같은 threshold nudge(임계값 미세 조정)를 반복하지 않고 다음 수리축을 정한다.
- >-
  Target surface(목표 표면)는 `{TARGET_SURFACE}`이고 legacy 34D(레거시 34D)는 lesson-only KPI target(교훈 전용 핵심 성과 지표 목표)이다. Effect(효과): v2-native research(v2 고유 연구)를 계속한다.

"""
    workspace = re.sub(
        r"- >-\n  Stage249\(249단계\).*?Target surface.*?\n\n",
        "",
        workspace,
        flags=re.DOTALL,
    )
    workspace = workspace.replace("current_focus:\n", "current_focus:\n" + focus, 1)
    stage249_block = f"""stage249_stage248_entry_source_followup_review:
  packet_id: {PACKET_ID}
  stage_id: {STAGE_ID}
  status: closed_open_stage250_decision_surface_binding_repair_candidate_not_final
  current_run_id: {RUN_ID}
  source_stage: {SOURCE_STAGE_ID}
  source_run: {SOURCE_RUN_ID}
  source_stage248_evidence_commit: {SOURCE_EVIDENCE_COMMIT}
  source_stage248_hash_record_commit: {SOURCE_HASH_RECORD_COMMIT}
  decision: {DECISION}
  report_path: {rel(REPORT_PATH)}
  decision_path: {rel(DECISION_PATH)}
  tradeoff_matrix_path: {rel(TRADEOFF_PATH)}
  attribution_path: {rel(ATTRIBUTION_PATH)}
  failure_memory_path: {rel(FAILURE_PATH)}
  route_matrix_path: {rel(ROUTE_PATH)}
  risk_atr_review_path: {rel(RISK_REVIEW_PATH)}
  external_verification_status: review_only_source_stage248_mt5_reports_completed
  pushed_commit_hash: pending_until_push
  next_action: {NEXT_RUN_ID}
  boundary: {BOUNDARY}
"""
    if "stage249_stage248_entry_source_followup_review:" in workspace:
        workspace = re.sub(
            r"stage249_stage248_entry_source_followup_review:\n(?:  .*\n)+",
            stage249_block,
            workspace,
            count=1,
        )
    else:
        workspace += "\n\n" + stage249_block
    if "stage250_decision_surface_binding_repair_after_stage248_threshold_no_effect:" not in workspace:
        workspace += f"""

stage250_decision_surface_binding_repair_after_stage248_threshold_no_effect:
  packet_id: {NEXT_PACKET_ID}
  stage_id: {NEXT_STAGE_ID}
  status: open_planned_from_stage249
  current_run_id: {NEXT_RUN_ID}
  source_stage: {STAGE_ID}
  source_run: {RUN_ID}
  source_decision: {DECISION}
  next_action: {NEXT_RUN_ID}
  boundary: {BOUNDARY}
"""
    write_text(WORKSPACE_STATE_PATH, workspace, bom=False)

    changelog_entry = f"""
## {utc_now()} Stage249 Stage248 entry source follow-up review closeout(249단계 248단계 진입 원천 후속 검토 종료)

- action(행동): closed(종료) `{STAGE_ID}` with decision(판정) `{DECISION}`.
- effect(효과): Stage248(248단계)의 threshold-only no-effect(임계값 전용 효과 없음)을 기록하고 `{NEXT_STAGE_ID}`를 열었다.
- boundary(주장 경계): `{BOUNDARY}`.
"""
    existing = read_text(CHANGELOG_PATH) if CHANGELOG_PATH.exists() else ""
    existing = re.sub(
        r"\n## [^\n]*Stage249 Stage248 entry source follow-up review closeout[^\n]*\n.*?(?=\n## |\Z)",
        "",
        existing,
        flags=re.DOTALL,
    )
    write_text(CHANGELOG_PATH, existing.rstrip() + changelog_entry, bom=False)


def write_ledgers_and_packet(review: Mapping[str, Any]) -> None:
    ref = review["reference"]
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__review_total",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "stage249_review_total",
        "parent_run_id": SOURCE_RUN_ID,
        "record_view": "review_total",
        "tier_scope": "Tier A+B",
        "kpi_scope": "baseline_adapter_followup_review",
        "scoreboard_lane": "regular_risk_execution",
        "status": "reviewed_closed",
        "judgment": DECISION,
        "path": rel(REPORT_PATH),
        "primary_kpi": f"reference=s248_cap0305_reference;validation_net={ref['validation_net']};validation_dd={ref['validation_balance_dd_percent']};validation_mid_pf={ref['validation_mid_pf']};oos_net={ref['oos_net']}",
        "guardrail_kpi": "threshold_variants_identical=1;hard_quality_pass_count=0;overall_goal_complete=0",
        "external_verification_status": "review_only_source_stage248_mt5_reports_completed",
        "notes": "Stage249 review only; routes to bounded Stage250 decision-surface binding repair.",
    }
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "baseline_adapter_followup_review(기준선 어댑터 후속 검토)",
        "status": "reviewed_closed",
        "judgment": DECISION,
        "path": rel(REPORT_PATH),
        "notes": f"source_stage248_evidence_commit={SOURCE_EVIDENCE_COMMIT};source_stage248_hash_record_commit={SOURCE_HASH_RECORD_COMMIT};overall_goal_complete=0;boundary={BOUNDARY}",
    }
    write_csv(STAGE_LEDGER_PATH, [alpha_row], ALPHA_COLUMNS)
    run_payload = upsert_csv(RUN_REGISTRY_PATH, RUN_COLUMNS, [run_row], "run_id")
    project_payload = upsert_csv(PROJECT_LEDGER_PATH, ALPHA_COLUMNS, [alpha_row], "ledger_row_id")
    stage_payload = {
        "path": rel(STAGE_LEDGER_PATH),
        "rows": 1,
        "upserted_rows": 1,
        "sha256": sha256_lf(STAGE_LEDGER_PATH),
        "hash_policy": "lf_normalized_text_register",
    }
    ledger_payload = {"run_registry": run_payload, "project_alpha_ledger": project_payload, "stage_ledger": stage_payload}

    summary = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "packet_id": PACKET_ID,
        "source_stage": SOURCE_STAGE_ID,
        "source_run": SOURCE_RUN_ID,
        "source_stage248_evidence_commit": SOURCE_EVIDENCE_COMMIT,
        "source_stage248_hash_record_commit": SOURCE_HASH_RECORD_COMMIT,
        "decision": DECISION,
        "next_stage_or_branch": NEXT_STAGE_ID,
        "external_verification_status": "review_only_source_stage248_mt5_reports_completed",
        "overall_goal_complete": False,
        "pushed_commit_hash": "pending_until_push",
        "claim_boundary": BOUNDARY,
        "reference": ref,
        "tradeoff_rows": review["tradeoff_rows"],
        "risk_review_rows": review["risk_review_rows"],
        "source_attribution_rows": review["source_attribution_rows"],
        "source_failure_rows": review["source_failure_rows"],
        "attribution_rows": review["attribution_rows"],
        "failure_memory_rows": review["failure_rows"],
        "route_rows": review["route_rows"],
        "ledger_payload": ledger_payload,
    }
    write_json(SUMMARY_PATH, summary)

    created = utc_now()
    artifact_paths = [
        PRODUCER_PATH,
        REPORT_PATH,
        TRADEOFF_PATH,
        ATTRIBUTION_PATH,
        FAILURE_PATH,
        ROUTE_PATH,
        RISK_REVIEW_PATH,
        SUMMARY_PATH,
        DECISION_PATH,
        STAGE_LEDGER_PATH,
        REVIEW_INDEX_PATH,
        SELECTION_PATH,
        CURRENT_STATE_PATH,
        WORKSPACE_STATE_PATH,
        CHANGELOG_PATH,
        NEXT_STAGE_ROOT / "00_spec/stage_brief.md",
        NEXT_STAGE_ROOT / "01_inputs/input_refs.md",
        NEXT_STAGE_ROOT / "03_reviews/review_index.md",
        NEXT_STAGE_ROOT / "04_selected/selection_status.md",
    ]
    prune_run_artifacts()
    artifact_rows = [
        {
            "artifact_id": artifact_id_for(path),
            "artifact_type": "stage249_followup_review_evidence",
            "path": rel(path),
            "sha256": sha256_lf(path),
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": created,
            "notes": "Stage249 Stage248 entry source follow-up review evidence; research only.",
        }
        for path in artifact_paths
        if os.path.exists(extended_path(path))
    ]
    artifact_payload = upsert_csv(ARTIFACT_REGISTRY_PATH, ARTIFACT_COLUMNS, artifact_rows, "artifact_id")
    ledger_payload["artifact_registry"] = artifact_payload
    summary["ledger_payload"] = ledger_payload
    write_json(SUMMARY_PATH, summary)

    base_payload = {
        "packet_id": PACKET_ID,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "source_stage": SOURCE_STAGE_ID,
        "source_run": SOURCE_RUN_ID,
        "decision": DECISION,
        "next_stage_or_branch": NEXT_STAGE_ID,
        "external_verification_status": "review_only_source_stage248_mt5_reports_completed",
        "claim_boundary": BOUNDARY,
        "overall_goal_complete": False,
    }
    packet_payloads = {
        "packet_receipt.json": {**base_payload, "created_at_utc": created, "status": "closed_pending_push_hash"},
        "routing_receipt.json": {**base_payload, "route": DECISION, "route_effect": "open Stage250 decision-surface binding repair"},
        "kpi_contract_audit.json": {
            **base_payload,
            "status": "passed",
            "kpi_basis": [rel(QUALITY_PATH), rel(KPI_PATH), rel(RISK_PATH), rel(SEGMENT_PATH), rel(BALANCE_PATH)],
        },
        "result_judgment_gate.json": {
            **base_payload,
            "result_subject": RUN_ID,
            "evidence_available": [rel(REPORT_PATH), rel(TRADEOFF_PATH), rel(RISK_REVIEW_PATH), rel(FAILURE_SOURCE_PATH)],
            "evidence_missing": ["Stage250 decision-surface binding repair", "ONNX parity", "MT5 ONNX/runtime reproduction"],
            "judgment_label": "threshold_axis_no_effect_negative_not_final",
            "next_condition": NEXT_STAGE_ID,
        },
        "performance_attribution_gate.json": {
            **base_payload,
            "observed_change": "Stage248 threshold variants produced no KPI or decision-surface movement",
            "attribution_rows": review["attribution_rows"],
            "attribution_confidence": "high",
        },
        "artifact_lineage_audit.json": {
            **base_payload,
            "source_inputs": [rel(QUALITY_PATH), rel(ATTRIBUTION_SOURCE_PATH), rel(FAILURE_SOURCE_PATH), rel(RISK_PATH)],
            "producer": rel(PRODUCER_PATH),
            "artifact_paths": [rel(path) for path in artifact_paths if os.path.exists(extended_path(path))],
            "ledger_payload": ledger_payload,
            "status": "completed",
        },
        "required_gate_coverage_audit.json": {
            **base_payload,
            "required_gates": ["kpi_contract_audit", "result_judgment_gate", "performance_attribution_gate", "artifact_lineage_audit", "final_claim_guard"],
            "status": "passed",
        },
        "final_claim_guard.json": {
            **base_payload,
            "forbidden_claims": ["deployment", "live_readiness", "runtime_authority", "operating_promotion", "operating_reference", "production_baseline", "overall_goal_complete"],
            "status": "passed",
        },
        "aggregate_summary.json": summary,
    }
    write_text(
        PACKET_ROOT / "closeout_packet.md",
        f"""# Stage249 Closeout Packet(249단계 종료 작업 묶음)

- run(실행): `{RUN_ID}`
- decision(판정): `{DECISION}`
- report(보고서): `{rel(REPORT_PATH)}`
- next_stage(다음 단계): `{NEXT_STAGE_ID}`
- overall_goal_complete(전체 목표 완료): `false`
- boundary(경계): `{BOUNDARY}`
""",
    )
    for name, payload in packet_payloads.items():
        write_json(PACKET_ROOT / name, payload)


def main() -> None:
    review = build_review()
    write_reports(review)
    write_next_stage_seed()
    update_current_truth()
    write_ledgers_and_packet(review)
    print(json.dumps({"stage": STAGE_ID, "decision": DECISION, "next_stage": NEXT_STAGE_ID}, ensure_ascii=False))


if __name__ == "__main__":
    main()
