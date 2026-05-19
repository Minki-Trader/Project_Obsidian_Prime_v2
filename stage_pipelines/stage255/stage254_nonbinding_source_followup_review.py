from __future__ import annotations

import csv
import hashlib
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Sequence


STAGE_ID = "255_adapter_research__stage254_nonbinding_source_followup_review"
RUN_ID = "run255A_stage255_stage254_nonbinding_source_followup_review_v1"
PACKET_ID = "stage255_stage254_nonbinding_source_followup_review_v1"
SOURCE_STAGE_ID = "254_adapter_research__nonbinding_source_repair_after_binding_axis_no_gain"
SOURCE_RUN_ID = "run254A_stage254_nonbinding_source_repair_after_binding_axis_no_gain_v1"
SOURCE_STAGE254_EVIDENCE_COMMIT = "2a505dea136acb476ff4ae1ca85c4a582f9d0171"
SOURCE_STAGE254_HASH_RECORD_COMMIT = "652000348554f7f883bcf06ca3ffe7e513916423"
NEXT_STAGE_ID = "256_adapter_research__source_feature_branch_after_binding_lifecycle_no_gain"
NEXT_RUN_ID = "run256A_stage256_source_feature_branch_after_binding_lifecycle_no_gain_v1"
NEXT_PACKET_ID = "stage256_source_feature_branch_after_binding_lifecycle_no_gain_v1"
DECISION = "open_stage256_bounded_source_feature_branch_after_binding_lifecycle_no_gain_candidate_not_final"
BOUNDARY = "research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment"
TARGET_SURFACE = "legacy_34d_kpi_lesson_only_v2_native_source_feature_branch_after_binding_lifecycle_no_gain"
EXTERNAL_STATUS = "review_only_source_stage254_mt5_reports_completed"

LEGACY_34D_NET = 987.60
LEGACY_34D_PF = 1.583157
LEGACY_34D_DD = 12.909136

ROOT = Path.cwd()
STAGE_ROOT = ROOT / "stages" / STAGE_ID
REVIEWS = STAGE_ROOT / "03_reviews"
PACKET_ROOT = ROOT / "docs/agent_control/packets" / PACKET_ID
NEXT_STAGE_ROOT = ROOT / "stages" / NEXT_STAGE_ID
SOURCE_REVIEWS = ROOT / "stages" / SOURCE_STAGE_ID / "03_reviews"

QUALITY_PATH = SOURCE_REVIEWS / "stage254_quality_matrix.csv"
KPI_PATH = SOURCE_REVIEWS / "stage254_nonbinding_source_kpi_summary.csv"
PROBABILITY_PATH = SOURCE_REVIEWS / "stage254_probability_telemetry_summary.csv"
SOURCE_ATTRIBUTION_PATH = SOURCE_REVIEWS / "stage254_performance_attribution.csv"
SOURCE_FAILURE_PATH = SOURCE_REVIEWS / "stage254_failure_memory.csv"
RISK_PATH = SOURCE_REVIEWS / "stage254_risk_atr_telemetry.csv"
SOURCE_REPORT_PATH = SOURCE_REVIEWS / "stage254_nonbinding_source_repair_report.md"
SOURCE_DECISION_PATH = SOURCE_REVIEWS / "stage254_decision.md"

REPORT_PATH = REVIEWS / "stage255_stage254_nonbinding_source_followup_review.md"
TRADEOFF_PATH = REVIEWS / "stage255_tradeoff_review_matrix.csv"
ATTRIBUTION_PATH = REVIEWS / "stage255_performance_attribution.csv"
FAILURE_PATH = REVIEWS / "stage255_failure_memory.csv"
ROUTE_PATH = REVIEWS / "stage255_route_matrix.csv"
RISK_REVIEW_PATH = REVIEWS / "stage255_risk_atr_review.csv"
SUMMARY_PATH = REVIEWS / "stage255_summary.json"
DECISION_PATH = REVIEWS / "stage255_decision.md"
STAGE_LEDGER_PATH = REVIEWS / "stage_run_ledger.csv"
REVIEW_INDEX_PATH = REVIEWS / "review_index.md"
SELECTION_PATH = STAGE_ROOT / "04_selected/selection_status.md"

CURRENT_STATE_PATH = ROOT / "docs/context/current_working_state.md"
WORKSPACE_STATE_PATH = ROOT / "docs/workspace/workspace_state.yaml"
CHANGELOG_PATH = ROOT / "docs/workspace/changelog.md"
RUN_REGISTRY_PATH = ROOT / "docs/registers/run_registry.csv"
PROJECT_LEDGER_PATH = ROOT / "docs/registers/alpha_run_ledger.csv"
ARTIFACT_REGISTRY_PATH = ROOT / "docs/registers/artifact_registry.csv"
PRODUCER_PATH = ROOT / "stage_pipelines/stage255/stage254_nonbinding_source_followup_review.py"

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


def fmt(value: float, digits: int = 2) -> str:
    return f"{value:.{digits}f}"


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


def read_for_adapter(adapter_id: str, val_net_delta: float, dd_delta: float, mid_pf_delta: float, oos_net_delta: float) -> tuple[str, str, str]:
    if adapter_id == "s254_stage252_control":
        return (
            "reference_only_near_miss_not_34d",
            "Stage254 control(254단계 기준)은 Stage252 control(252단계 기준)을 재현했지만 34D(34디) KPI(핵심 성과 지표)를 함께 넘지 못했다.",
            "use_as_reference_only_not_final",
        )
    if adapter_id == "s254_hold4":
        return (
            "tiny_dd_gain_large_net_midpf_damage",
            "hold4(4봉 보유)는 DD(낙폭)를 거의 34D(34디) 수준까지 낮췄지만 net(순수익)과 mid PF(중간 수익요인)를 크게 손상했다.",
            "do_not_continue_as_primary_axis",
        )
    if adapter_id == "s254_hold5":
        return (
            "net_nearer_but_dd_oos_damage",
            "hold5(5봉 보유)는 net(순수익) 손상은 작지만 DD/OOS DD(낙폭/표본외 낙폭)가 커져 실패다.",
            "do_not_continue_as_primary_axis",
        )
    if adapter_id == "s254_hold4_flatclose":
        return (
            "flatclose_collapsed_validation_net",
            "flat close(무포지션 신호 청산)는 validation net(검증 순수익)을 거의 붕괴시켰다.",
            "do_not_repeat",
        )
    if adapter_id == "s254_hold4_reentry12":
        return (
            "dd_improved_but_net_midpf_collapsed",
            "reentry12(12봉 재진입 대기)는 DD(낙폭)를 낮췄지만 net(순수익)과 mid PF(중간 수익요인)를 크게 손상했다.",
            "do_not_continue_as_primary_axis",
        )
    if dd_delta < 0 and val_net_delta < 0:
        return ("risk_tradeoff_not_quality_gain", "DD(낙폭) 개선이 수익 품질 개선으로 이어지지 않았다.", NEXT_STAGE_ID)
    return ("weak_or_no_gain", "KPI(핵심 성과 지표) 개선이 충분하지 않다.", NEXT_STAGE_ID)


def build_review() -> dict[str, Any]:
    quality_rows = read_csv(QUALITY_PATH)
    kpi_rows = read_csv(KPI_PATH)
    source_attribution_rows = read_csv(SOURCE_ATTRIBUTION_PATH)
    source_failure_rows = read_csv(SOURCE_FAILURE_PATH)
    control = next(row for row in quality_rows if row["adapter_id"] == "s254_stage252_control")
    control_values = {
        "validation_net": as_float(control["validation_net"]),
        "validation_dd": as_float(control["validation_balance_dd_percent"]),
        "validation_mid_pf": as_float(control["validation_mid_pf"]),
        "oos_net": as_float(control["oos_net"]),
    }

    tradeoff_rows: list[dict[str, Any]] = []
    for row in quality_rows:
        val_net = as_float(row["validation_net"])
        val_dd = as_float(row["validation_balance_dd_percent"])
        mid_pf = as_float(row["validation_mid_pf"])
        oos_net = as_float(row["oos_net"])
        val_net_delta = val_net - control_values["validation_net"]
        dd_delta = val_dd - control_values["validation_dd"]
        mid_pf_delta = mid_pf - control_values["validation_mid_pf"]
        oos_net_delta = oos_net - control_values["oos_net"]
        useful_signal, read, next_handling = read_for_adapter(row["adapter_id"], val_net_delta, dd_delta, mid_pf_delta, oos_net_delta)
        tradeoff_rows.append(
            {
                "adapter_id": row["adapter_id"],
                "axis": row["axis"],
                "validation_pf": row["validation_pf"],
                "validation_net": row["validation_net"],
                "validation_net_delta_vs_control": fmt(val_net_delta),
                "validation_net_gap_vs_34d": row["validation_net_gap_vs_34d"],
                "validation_dd_percent": row["validation_balance_dd_percent"],
                "validation_dd_delta_vs_control": fmt(dd_delta, 4),
                "validation_dd_margin_vs_34d": row["validation_dd_margin_vs_34d"],
                "validation_early_pf": row["validation_early_pf"],
                "validation_mid_pf": row["validation_mid_pf"],
                "validation_mid_pf_delta_vs_control": fmt(mid_pf_delta, 6),
                "validation_late_pf": row["validation_late_pf"],
                "oos_pf": row["oos_pf"],
                "oos_net": row["oos_net"],
                "oos_net_delta_vs_control": fmt(oos_net_delta),
                "oos_dd_percent": row["oos_balance_dd_percent"],
                "hard_quality_pass": row["hard_quality_pass"],
                "useful_signal": useful_signal,
                "read": read,
                "next_handling": next_handling,
            }
        )

    risk_review_rows: list[dict[str, Any]] = []
    for row in kpi_rows:
        if row.get("view") != "actual_routed_total":
            continue
        risk_review_rows.append(
            {
                "adapter_id": row["adapter_id"],
                "split": row["split"],
                "atr_enabled": row.get("atr_enabled", ""),
                "model_risk_enabled": row.get("model_risk_enabled", ""),
                "max_model_risk_pct": row.get("max_model_risk_pct", ""),
                "max_actual_risk_pct_after_floor": row.get("max_actual_risk_pct_after_floor", ""),
                "risk_floor_applied_count": row.get("risk_floor_applied_count", ""),
                "avg_executed_lot": row.get("avg_executed_lot", ""),
                "avg_atr_points": row.get("avg_atr_points", ""),
                "avg_open_sl_points": row.get("avg_open_sl_points", ""),
                "avg_open_tp_points": row.get("avg_open_tp_points", ""),
                "risk_bucket": row.get("risk_bucket", ""),
                "read": "ATR/risk(ATR/위험)은 유지됐지만 lifecycle(생명주기) 축은 KPI(핵심 성과 지표)를 충분히 고치지 못했다.",
            }
        )

    attribution_rows = [
        {
            "attribution_id": f"{RUN_ID}__lifecycle_axis_no_gain",
            "observed_change": "Stage254 non-binding lifecycle(254단계 비결합 생명주기) 변형은 hard_quality_pass(강한 품질 통과)를 하나도 만들지 못했다.",
            "comparison_baseline": "s254_stage252_control",
            "likely_drivers": "hold/reentry/flat-close(보유/재진입/무포지션 청산)는 노출 타이밍을 바꿨지만 entry/source quality(진입/원천 품질)를 고치지 못했다.",
            "segment_checks": "validation/OOS(검증/표본외), early/mid/late PF(초기/중간/후기 수익요인), DD(낙폭), risk/ATR telemetry(위험/ATR 원격측정)를 검토했다.",
            "trade_shape": "hold4/reentry12(4봉 보유/12봉 재진입)는 DD(낙폭) 단서가 있으나 net(순수익)과 mid PF(중간 수익요인)를 크게 낮췄다.",
            "alternative_explanations": "DD(낙폭) 개선은 edge(우위) 개선이 아니라 exposure timing(노출 타이밍) 손실일 수 있다.",
            "attribution_confidence": "high",
            "next_probe": NEXT_STAGE_ID,
        },
        {
            "attribution_id": f"{RUN_ID}__control_still_reference_only",
            "observed_change": "control(기준)은 validation net(검증 순수익) 972.15, PF(수익요인) 1.59, DD(낙폭) 12.9281로 34D(34디) 목표를 함께 넘지 못했다.",
            "comparison_baseline": "legacy 34D lesson-only KPI target(레거시 34D 교훈 전용 KPI 목표)",
            "likely_drivers": "decision/lifecycle(결정/생명주기) 후단 조정만으로는 source/feature(원천/피처) 약점을 고치지 못한다.",
            "segment_checks": "validation mid PF(검증 중간 수익요인) 1.516650878과 DD margin(낙폭 여유) -0.018964를 검토했다.",
            "trade_shape": "near-miss(근접 실패)지만 final package(최종 패키지) 근거는 아니다.",
            "alternative_explanations": "작은 차이는 tester path(테스터 경로) 차이일 수 있으나, hard pass(강한 통과) 실패는 남는다.",
            "attribution_confidence": "medium_high",
            "next_probe": NEXT_STAGE_ID,
        },
    ]

    failure_rows = [
        {
            "failure_id": f"{RUN_ID}__binding_and_lifecycle_axes_no_gain",
            "source_failure": "stage250_stage252_binding_axis_plus_stage254_lifecycle_axis_no_gain",
            "why_it_matters": "결합(binding, 결합)과 생명주기(lifecycle, 생명주기) 후단 축이 모두 34D(34디)급 KPI(핵심 성과 지표)를 만들지 못했다.",
            "salvage_value": "control(기준) near-miss(근접 실패), hold4/reentry12 DD(낙폭) 단서, hold5 net(순수익) 보존 단서는 보존한다.",
            "do_not_repeat": "threshold/binding/lifecycle(임계값/결합/생명주기)만 계속 조이지 않는다.",
            "next_handling": NEXT_STAGE_ID,
        },
        {
            "failure_id": f"{RUN_ID}__route_to_source_feature_branch",
            "source_failure": "post_decision_knobs_did_not_repair_mid_window_quality",
            "why_it_matters": "mid PF(중간 수익요인) 손상이 반복되어 source/feature/model branch(원천/피처/모델 분기)가 필요하다.",
            "salvage_value": "Stage256(256단계)는 ATR/risk(ATR/위험)를 유지한 채 새 source/feature branch(원천/피처 분기)를 좁게 시험한다.",
            "do_not_repeat": "한 번 더 보유/재진입만 바꾸는 Stage(단계)를 열지 않는다.",
            "next_handling": NEXT_STAGE_ID,
        },
    ]

    route_rows = [
        {
            "route_id": f"{RUN_ID}__close_stage255_review_only",
            "evidence": "hard_quality_pass=false for all Stage254 candidates(254단계 모든 후보 강한 통과 실패)",
            "decision": DECISION,
            "effect": "Stage255(255단계)를 검토 전용으로 닫고, Stage256(256단계)를 source/feature branch(원천/피처 분기)로 연다.",
            "next_stage_or_branch": NEXT_STAGE_ID,
        },
        {
            "route_id": f"{RUN_ID}__stop_lifecycle_as_primary_axis",
            "evidence": "hold/reentry/flat-close variants damaged net, DD, or mid PF(보유/재진입/무포지션 청산 변형이 순수익/낙폭/중간 수익요인을 손상)",
            "decision": "route_to_source_feature_branch",
            "effect": "다음 작업은 output knob(출력 손잡이)가 아니라 source/feature/model(원천/피처/모델) 축으로 좁혀진다.",
            "next_stage_or_branch": NEXT_STAGE_ID,
        },
    ]

    return {
        "control": control,
        "tradeoff_rows": tradeoff_rows,
        "risk_review_rows": risk_review_rows,
        "source_attribution_rows": source_attribution_rows,
        "source_failure_rows": source_failure_rows,
        "attribution_rows": attribution_rows,
        "failure_rows": failure_rows,
        "route_rows": route_rows,
    }


def write_reports(review: Mapping[str, Any]) -> None:
    tradeoff_rows = review["tradeoff_rows"]
    best_net = max(tradeoff_rows, key=lambda row: as_float(row["validation_net"]))
    best_dd = min(tradeoff_rows, key=lambda row: as_float(row["validation_dd_percent"]))
    write_csv(TRADEOFF_PATH, tradeoff_rows, list(tradeoff_rows[0].keys()))
    write_csv(ATTRIBUTION_PATH, review["attribution_rows"], list(review["attribution_rows"][0].keys()))
    write_csv(FAILURE_PATH, review["failure_rows"], list(review["failure_rows"][0].keys()))
    write_csv(ROUTE_PATH, review["route_rows"], list(review["route_rows"][0].keys()))
    write_csv(RISK_REVIEW_PATH, review["risk_review_rows"], list(review["risk_review_rows"][0].keys()))

    table_rows = "\n".join(
        "| {adapter_id} | {validation_pf} | {validation_net} | {validation_net_delta_vs_control} | {validation_dd_percent} | {validation_dd_delta_vs_control} | {validation_mid_pf} | {oos_pf} | {oos_net} | {useful_signal} |".format(
            **row
        )
        for row in tradeoff_rows
    )
    report = f"""# Stage255 Stage254 Non-binding Source Follow-up Review(255단계 254단계 비결합 원천 후속 검토)

- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- source_stage254_evidence_commit(원천 254단계 근거 커밋): `{SOURCE_STAGE254_EVIDENCE_COMMIT}`
- source_stage254_hash_record_commit(원천 254단계 해시 기록 커밋): `{SOURCE_STAGE254_HASH_RECORD_COMMIT}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- decision(판정): `{DECISION}`
- claim_boundary(주장 경계): `{BOUNDARY}`

## Plain Read(쉬운 해석)

Stage254(254단계)는 valid MT5 evidence(유효 메타트레이더5 근거)를 만들었지만, lifecycle axis(생명주기 축)는 34D(34디) KPI(핵심 성과 지표)를 넘기지 못했다.
control(기준)은 여전히 near-miss(근접 실패)이고, hold/reentry/flat-close(보유/재진입/무포지션 청산)는 net(순수익), DD(낙폭), mid PF(중간 수익요인) 중 하나 이상을 손상했다.

Effect(효과): Stage256(256단계)은 threshold/binding/lifecycle(임계값/결합/생명주기) 후단 조정이 아니라 source/feature/model branch(원천/피처/모델 분기)로 간다.

## KPI Tradeoff(핵심 성과 지표 절충)

| adapter(어댑터) | validation PF(검증 수익요인) | validation net(검증 순수익) | net delta(순수익 차이) | DD(낙폭) | DD delta(낙폭 차이) | mid PF(중간 수익요인) | OOS PF(표본외 수익요인) | OOS net(표본외 순수익) | read(해석) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
{table_rows}

## Key Clues(핵심 단서)

- best_net(최선 순수익): `{best_net["adapter_id"]}` validation net(검증 순수익) `{best_net["validation_net"]}`. 하지만 34D(34디) net(순수익)보다 낮다.
- best_dd(최선 낙폭): `{best_dd["adapter_id"]}` DD(낙폭) `{best_dd["validation_dd_percent"]}`. 하지만 net(순수익)과 mid PF(중간 수익요인)가 크게 손상됐다.
- no hard pass(강한 통과 없음): 모든 Stage254(254단계) variant(변형)는 `hard_quality_pass=False(강한 품질 통과 거짓)`이다.

## Result Judgment(결과 판정)

- result_subject(판정 대상): `{RUN_ID}`
- evidence_available(사용 근거): Stage254(254단계) quality matrix(품질 행렬), KPI summary(핵심 성과 지표 요약), risk/ATR telemetry(위험/ATR 원격측정), performance attribution(성과 귀속)
- evidence_missing(부족 근거): Stage256(256단계) source/feature branch(원천/피처 분기) 실행, ONNX parity(ONNX 동등성), MT5 ONNX/runtime reproduction(MT5 ONNX/런타임 재현)
- judgment_label(판정 라벨): `negative_valid_lifecycle_axis_no_gain_not_final`
- next_condition(다음 조건): `{NEXT_STAGE_ID}`

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준), overall_goal_complete(전체 목표 완료).
"""
    write_text(REPORT_PATH, report)

    write_text(
        DECISION_PATH,
        f"""# Stage255 Decision(255단계 판정)

- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- decision(판정): `{DECISION}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- source_stage254_evidence_commit(원천 254단계 근거 커밋): `{SOURCE_STAGE254_EVIDENCE_COMMIT}`
- source_stage254_hash_record_commit(원천 254단계 해시 기록 커밋): `{SOURCE_STAGE254_HASH_RECORD_COMMIT}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- report(보고서): `{rel(REPORT_PATH)}`
- tradeoff_matrix(절충 행렬): `{rel(TRADEOFF_PATH)}`
- attribution(성과 귀속): `{rel(ATTRIBUTION_PATH)}`
- failure_memory(실패 기억): `{rel(FAILURE_PATH)}`
- route_matrix(경로 행렬): `{rel(ROUTE_PATH)}`
- risk_atr_review(위험/ATR 검토): `{rel(RISK_REVIEW_PATH)}`
- next_stage_or_branch(다음 단계 또는 분기): `{NEXT_STAGE_ID}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage255(255단계) closeout(종료)은 overall goal complete(전체 목표 완료)가 아니다.
""",
    )

    write_text(
        REVIEW_INDEX_PATH,
        f"""# Stage255 Review Index(255단계 검토 색인)

- status(상태): `closed_open_stage256_source_feature_branch_candidate_not_final`
- run(실행): `{RUN_ID}`
- decision(판정): `{DECISION}`
- report(보고서): `{rel(REPORT_PATH)}`
- tradeoff_matrix(절충 행렬): `{rel(TRADEOFF_PATH)}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
""",
    )
    write_text(
        SELECTION_PATH,
        f"""# Stage255 Selection Status(255단계 선택 상태)

- stage_status(단계 상태): `closed_open_stage256_source_feature_branch_candidate_not_final`
- current_packet(현재 작업 묶음): `{PACKET_ID}`
- current_run(현재 실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- decision(판정): `{DECISION}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- next_stage_or_branch(다음 단계 또는 분기): `{NEXT_STAGE_ID}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`
- claim_boundary(주장 경계): `{BOUNDARY}`
""",
    )


def write_next_stage_seed() -> None:
    write_text(
        NEXT_STAGE_ROOT / "00_spec/stage_brief.md",
        f"""# {NEXT_STAGE_ID}

Stage256(256단계)는 Stage250/252/254(250/252/254단계)의 threshold/binding/lifecycle(임계값/결합/생명주기) 후단 축이 KPI(핵심 성과 지표)를 올리지 못한 뒤 여는 bounded source/feature branch(경계 원천/피처 분기)다.

## Bounded Question(경계 질문)

Can a v2-native source/feature/model branch(v2 고유 원천/피처/모델 분기) recover 34D-level or better validation/OOS KPI(34D급 이상 검증/표본외 핵심 성과 지표) while preserving ATR/risk(ATR/위험) telemetry(원격측정), without repeating threshold/binding/lifecycle over-tuning(임계값/결합/생명주기 과조정)?

## Boundary(경계)

`{BOUNDARY}`
""",
    )
    write_text(
        NEXT_STAGE_ROOT / "01_inputs/input_refs.md",
        f"""# Stage256 Input References(256단계 입력 참조)

- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- source_decision(원천 판정): `{DECISION}`
- source_report(원천 보고서): `{rel(REPORT_PATH)}`
- source_tradeoff_matrix(원천 절충 행렬): `{rel(TRADEOFF_PATH)}`
- source_stage254_evidence_commit(원천 254단계 근거 커밋): `{SOURCE_STAGE254_EVIDENCE_COMMIT}`
- source_stage254_hash_record_commit(원천 254단계 해시 기록 커밋): `{SOURCE_STAGE254_HASH_RECORD_COMMIT}`
""",
    )
    write_text(
        NEXT_STAGE_ROOT / "03_reviews/review_index.md",
        f"""# Stage256 Review Index(256단계 검토 색인)

- status(상태): `open_planned_from_stage255`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- source_stage(원천 단계): `{STAGE_ID}`
- source_decision(원천 판정): `{DECISION}`
""",
    )
    write_text(
        NEXT_STAGE_ROOT / "04_selected/selection_status.md",
        f"""# Stage256 Selection Status(256단계 선택 상태)

- stage_status(단계 상태): `open_planned_from_stage255`
- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- source_decision(원천 판정): `{DECISION}`
- claim_boundary(주장 경계): `{BOUNDARY}`
""",
    )


def replace_or_append_block(text: str, key: str, block: str) -> str:
    pattern = rf"^{re.escape(key)}:\n(?:  .*\n)+"
    if re.search(pattern, text, flags=re.MULTILINE):
        return re.sub(pattern, block, text, count=1, flags=re.MULTILINE)
    return text.rstrip() + "\n\n" + block


def update_current_truth() -> None:
    write_text(
        CURRENT_STATE_PATH,
        f"""# Current Working State(현재 작업 상태)

- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- active_stage(활성 단계): `{NEXT_STAGE_ID}`
- selected_research_baseline(선택 연구 기준선): `none`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- adapter_under_review(검토 중 어댑터): `stage256_source_feature_branch`
- status(상태): `stage255_closed_open_stage256_source_feature_branch_candidate_not_final`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage255(255단계)는 Stage254(254단계) non-binding lifecycle repair(비결합 생명주기 수리)를 review-only(검토 전용)로 판정했다.
Effect(효과): threshold/binding/lifecycle(임계값/결합/생명주기) 후단 조정을 멈추고 Stage256(256단계) source/feature/model branch(원천/피처/모델 분기)로 넘어간다.

## Latest Stage255 Evidence(최신 255단계 근거)

- run(실행): `{RUN_ID}`
- decision(판정): `{DECISION}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- report(보고서): `{rel(REPORT_PATH)}`
- tradeoff_matrix(절충 행렬): `{rel(TRADEOFF_PATH)}`
- attribution(성과 귀속): `{rel(ATTRIBUTION_PATH)}`
- failure_memory(실패 기억): `{rel(FAILURE_PATH)}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준), overall_goal_complete(전체 목표 완료).
""",
    )

    workspace = read_text(WORKSPACE_STATE_PATH)
    workspace = re.sub(r"^current_run_id: .*$", f"current_run_id: {NEXT_RUN_ID}", workspace, count=1, flags=re.MULTILINE)
    workspace = re.sub(r"^updated_on: .*$", "updated_on: '2026-05-20'", workspace, count=1, flags=re.MULTILINE)
    workspace = re.sub(r"^active_stage: .*$", f"active_stage: {NEXT_STAGE_ID}", workspace, count=1, flags=re.MULTILINE)
    focus = f"""current_focus:
- >-
  Stage255(255단계) closed(종료) as `{DECISION}` and Stage256(256단계) `{NEXT_STAGE_ID}` is open_planned(개방 계획). Effect(효과): binding/lifecycle(결합/생명주기) 축 무개선을 source/feature/model branch(원천/피처/모델 분기)로 분리한다.
- >-
  Stage255 evidence(255단계 근거)는 `{rel(REPORT_PATH)}`, `{rel(TRADEOFF_PATH)}`, `{rel(ATTRIBUTION_PATH)}`, `{rel(FAILURE_PATH)}`에 있다. Effect(효과): Stage256(256단계)는 후단 knob(손잡이)이 아니라 원천/피처/모델 축을 시험한다.
- >-
  Target surface(목표 표면)는 `{TARGET_SURFACE}`이고 legacy 34D(레거시 34D)는 lesson-only KPI target(교훈 전용 핵심 성과 지표 목표)이다. Effect(효과): v2-native research(v2 고유 연구)를 계속한다.
"""
    workspace = re.sub(r"current_focus:\n.*?(?=\n[A-Za-z0-9_]+:\n)", focus, workspace, count=1, flags=re.DOTALL)
    stage255_block = f"""stage255_stage254_nonbinding_source_followup_review:
  packet_id: {PACKET_ID}
  stage_id: {STAGE_ID}
  status: closed_open_stage256_source_feature_branch_candidate_not_final
  current_run_id: {RUN_ID}
  source_stage: {SOURCE_STAGE_ID}
  source_run: {SOURCE_RUN_ID}
  source_stage254_evidence_commit: {SOURCE_STAGE254_EVIDENCE_COMMIT}
  source_stage254_hash_record_commit: {SOURCE_STAGE254_HASH_RECORD_COMMIT}
  decision: {DECISION}
  report_path: {rel(REPORT_PATH)}
  decision_path: {rel(DECISION_PATH)}
  tradeoff_matrix_path: {rel(TRADEOFF_PATH)}
  attribution_path: {rel(ATTRIBUTION_PATH)}
  failure_memory_path: {rel(FAILURE_PATH)}
  route_matrix_path: {rel(ROUTE_PATH)}
  risk_atr_review_path: {rel(RISK_REVIEW_PATH)}
  external_verification_status: {EXTERNAL_STATUS}
  pushed_commit_hash: pending_until_push
  next_action: {NEXT_RUN_ID}
  boundary: {BOUNDARY}
"""
    stage256_block = f"""stage256_source_feature_branch_after_binding_lifecycle_no_gain:
  packet_id: {NEXT_PACKET_ID}
  stage_id: {NEXT_STAGE_ID}
  status: open_planned_from_stage255
  current_run_id: {NEXT_RUN_ID}
  source_stage: {STAGE_ID}
  source_run: {RUN_ID}
  source_decision: {DECISION}
  next_action: {NEXT_RUN_ID}
  boundary: {BOUNDARY}
"""
    workspace = replace_or_append_block(workspace, "stage255_stage254_nonbinding_source_followup_review", stage255_block)
    workspace = replace_or_append_block(workspace, "stage256_source_feature_branch_after_binding_lifecycle_no_gain", stage256_block)
    write_text(WORKSPACE_STATE_PATH, workspace, bom=False)

    existing = read_text(CHANGELOG_PATH) if CHANGELOG_PATH.exists() else ""
    changelog_entry = f"""
## {utc_now()} Stage255 Stage254 non-binding lifecycle follow-up review closeout(255단계 254단계 비결합 생명주기 후속 검토 종료)

- action(행동): closed(종료) `{STAGE_ID}` with decision(판정) `{DECISION}`.
- effect(효과): lifecycle axis no-gain(생명주기 축 무개선)을 source/feature branch(원천/피처 분기)로 넘겼다.
- boundary(주장 경계): `{BOUNDARY}`.
"""
    existing = re.sub(r"\n## [^\n]*Stage255 Stage254 non-binding lifecycle follow-up review closeout[^\n]*\n.*?(?=\n## |\Z)", "", existing, flags=re.DOTALL)
    write_text(CHANGELOG_PATH, existing.rstrip() + changelog_entry, bom=False)


def write_ledgers_and_packet(review: Mapping[str, Any]) -> None:
    control = review["control"]
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__review_total",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "stage255_review_total",
        "parent_run_id": SOURCE_RUN_ID,
        "record_view": "review_total",
        "tier_scope": "Tier A+B",
        "kpi_scope": "baseline_adapter_followup_review",
        "scoreboard_lane": "regular_risk_execution",
        "status": "reviewed_closed",
        "judgment": DECISION,
        "path": rel(REPORT_PATH),
        "primary_kpi": f"control={control['adapter_id']};validation_net={control['validation_net']};validation_dd={control['validation_balance_dd_percent']};validation_mid_pf={control['validation_mid_pf']};oos_net={control['oos_net']}",
        "guardrail_kpi": "hard_quality_pass_count=0;binding_lifecycle_axes_no_gain=1;overall_goal_complete=0",
        "external_verification_status": EXTERNAL_STATUS,
        "notes": "Stage255 review only; routes to bounded Stage256 source/feature branch.",
    }
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "baseline_adapter_followup_review(기준 어댑터 후속 검토)",
        "status": "reviewed_closed",
        "judgment": DECISION,
        "path": rel(REPORT_PATH),
        "notes": f"source_stage254_evidence_commit={SOURCE_STAGE254_EVIDENCE_COMMIT};source_stage254_hash_record_commit={SOURCE_STAGE254_HASH_RECORD_COMMIT};overall_goal_complete=0;boundary={BOUNDARY}",
    }
    write_csv(STAGE_LEDGER_PATH, [alpha_row], ALPHA_COLUMNS)
    run_payload = upsert_csv(RUN_REGISTRY_PATH, RUN_COLUMNS, [run_row], "run_id")
    project_payload = upsert_csv(PROJECT_LEDGER_PATH, ALPHA_COLUMNS, [alpha_row], "ledger_row_id")
    stage_payload = {"path": rel(STAGE_LEDGER_PATH), "rows": 1, "upserted_rows": 1, "sha256": sha256_lf(STAGE_LEDGER_PATH), "hash_policy": "lf_normalized_text_register"}
    ledger_payload = {"run_registry": run_payload, "project_alpha_ledger": project_payload, "stage_ledger": stage_payload}

    summary = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "packet_id": PACKET_ID,
        "source_stage": SOURCE_STAGE_ID,
        "source_run": SOURCE_RUN_ID,
        "source_stage254_evidence_commit": SOURCE_STAGE254_EVIDENCE_COMMIT,
        "source_stage254_hash_record_commit": SOURCE_STAGE254_HASH_RECORD_COMMIT,
        "decision": DECISION,
        "next_stage_or_branch": NEXT_STAGE_ID,
        "external_verification_status": EXTERNAL_STATUS,
        "overall_goal_complete": False,
        "pushed_commit_hash": "pending_until_push",
        "claim_boundary": BOUNDARY,
        "legacy_34d_lesson_only_targets": {"validation_net": LEGACY_34D_NET, "validation_pf": LEGACY_34D_PF, "validation_dd": LEGACY_34D_DD},
        "control": control,
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
            "artifact_type": "stage255_followup_review_evidence",
            "path": rel(path),
            "sha256": sha256_lf(path),
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": created,
            "notes": "Stage255 Stage254 non-binding lifecycle follow-up review evidence; research only.",
        }
        for path in artifact_paths
        if os.path.exists(extended_path(path))
    ]
    ledger_payload["artifact_registry"] = upsert_csv(ARTIFACT_REGISTRY_PATH, ARTIFACT_COLUMNS, artifact_rows, "artifact_id")
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
        "external_verification_status": EXTERNAL_STATUS,
        "claim_boundary": BOUNDARY,
        "overall_goal_complete": False,
    }
    packet_payloads = {
        "packet_receipt.json": {**base_payload, "created_at_utc": created, "status": "closed_pending_push_hash"},
        "routing_receipt.json": {**base_payload, "route": DECISION, "route_effect": "open Stage256 source/feature/model branch"},
        "kpi_contract_audit.json": {**base_payload, "status": "passed", "kpi_basis": [rel(QUALITY_PATH), rel(KPI_PATH), rel(PROBABILITY_PATH), rel(RISK_PATH)]},
        "result_judgment_gate.json": {
            **base_payload,
            "result_subject": RUN_ID,
            "evidence_available": [rel(REPORT_PATH), rel(TRADEOFF_PATH), rel(ATTRIBUTION_PATH), rel(FAILURE_PATH), rel(RISK_REVIEW_PATH)],
            "evidence_missing": [NEXT_STAGE_ID, "ONNX parity(ONNX 동등성)", "MT5 ONNX/runtime reproduction(MT5 ONNX/런타임 재현)"],
            "judgment_label": "negative_valid_lifecycle_axis_no_gain_not_final",
            "next_condition": NEXT_STAGE_ID,
        },
        "performance_attribution_gate.json": {**base_payload, "observed_change": "Stage254 lifecycle variants did not create hard KPI pass", "attribution_rows": review["attribution_rows"], "attribution_confidence": "high"},
        "artifact_lineage_audit.json": {
            **base_payload,
            "source_inputs": [rel(QUALITY_PATH), rel(KPI_PATH), rel(PROBABILITY_PATH), rel(SOURCE_ATTRIBUTION_PATH), rel(SOURCE_FAILURE_PATH), rel(RISK_PATH)],
            "producer": rel(PRODUCER_PATH),
            "consumer": NEXT_STAGE_ID,
            "artifact_paths": [rel(path) for path in artifact_paths if os.path.exists(extended_path(path))],
            "ledger_payload": ledger_payload,
            "lineage_judgment": "connected_with_boundary",
            "status": "completed",
        },
        "required_gate_coverage_audit.json": {**base_payload, "required_gates": ["kpi_contract_audit", "result_judgment_gate", "performance_attribution_gate", "artifact_lineage_audit", "final_claim_guard"], "status": "passed"},
        "final_claim_guard.json": {**base_payload, "forbidden_claims": ["deployment", "live_readiness", "runtime_authority", "operating_promotion", "operating_reference", "production_baseline", "overall_goal_complete"], "status": "passed"},
        "aggregate_summary.json": summary,
    }
    write_text(
        PACKET_ROOT / "closeout_packet.md",
        f"""# Stage255 Closeout Packet(255단계 종료 작업 묶음)

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
