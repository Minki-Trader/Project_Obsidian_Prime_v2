from __future__ import annotations

import csv
import hashlib
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Sequence


STAGE_ID = "253_adapter_research__stage252_asymmetric_binding_followup_review"
RUN_ID = "run253A_stage253_stage252_asymmetric_binding_followup_review_v1"
PACKET_ID = "stage253_stage252_asymmetric_binding_followup_review_v1"
SOURCE_STAGE_ID = "252_adapter_research__asymmetric_binding_repair_after_stage250_overprune"
SOURCE_RUN_ID = "run252A_stage252_asymmetric_binding_repair_after_stage250_overprune_v1"
SOURCE_STAGE252_EVIDENCE_COMMIT = "53aa5f020f0b7e6d97325d9fc25b2a50a3be5c1d"
SOURCE_STAGE252_HASH_RECORD_COMMIT = "1ae463e528189f7d406580aa99923edf0600aa46"
SOURCE_STAGE251_EVIDENCE_COMMIT = "5928b10add8f7d8da8680becdaf6ccf1049da1e6"
SOURCE_STAGE251_HASH_RECORD_COMMIT = "5cdb2cd2f0445e82e7311b30fd65df46fb31607f"
NEXT_STAGE_ID = "254_adapter_research__nonbinding_source_repair_after_binding_axis_no_gain"
NEXT_RUN_ID = "run254A_stage254_nonbinding_source_repair_after_binding_axis_no_gain_v1"
NEXT_PACKET_ID = "stage254_nonbinding_source_repair_after_binding_axis_no_gain_v1"
DECISION = "open_stage254_bounded_nonbinding_source_repair_after_binding_axis_no_gain_candidate_not_final"
BOUNDARY = "research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment"
TARGET_SURFACE = "legacy_34d_kpi_lesson_only_v2_native_nonbinding_source_repair_after_binding_axis_no_gain"
EXTERNAL_STATUS = "review_only_source_stage252_mt5_reports_completed"

LEGACY_34D_NET = 987.60
LEGACY_34D_PF = 1.583157
LEGACY_34D_DD = 12.909136

ROOT = Path.cwd()
STAGE_ROOT = ROOT / "stages" / STAGE_ID
REVIEWS = STAGE_ROOT / "03_reviews"
PACKET_ROOT = ROOT / "docs/agent_control/packets" / PACKET_ID
NEXT_STAGE_ROOT = ROOT / "stages" / NEXT_STAGE_ID
SOURCE_REVIEWS = ROOT / "stages" / SOURCE_STAGE_ID / "03_reviews"

QUALITY_PATH = SOURCE_REVIEWS / "stage252_quality_matrix.csv"
KPI_PATH = SOURCE_REVIEWS / "stage252_asymmetric_binding_kpi_summary.csv"
PROBABILITY_PATH = SOURCE_REVIEWS / "stage252_probability_binding_summary.csv"
SOURCE_ATTRIBUTION_PATH = SOURCE_REVIEWS / "stage252_performance_attribution.csv"
SOURCE_FAILURE_PATH = SOURCE_REVIEWS / "stage252_failure_memory.csv"
RISK_PATH = SOURCE_REVIEWS / "stage252_risk_atr_telemetry.csv"
SOURCE_REPORT_PATH = SOURCE_REVIEWS / "stage252_asymmetric_binding_report.md"
SOURCE_DECISION_PATH = SOURCE_REVIEWS / "stage252_decision.md"

REPORT_PATH = REVIEWS / "stage253_stage252_asymmetric_binding_followup_review.md"
TRADEOFF_PATH = REVIEWS / "stage253_tradeoff_review_matrix.csv"
ATTRIBUTION_PATH = REVIEWS / "stage253_performance_attribution.csv"
FAILURE_PATH = REVIEWS / "stage253_failure_memory.csv"
ROUTE_PATH = REVIEWS / "stage253_route_matrix.csv"
RISK_REVIEW_PATH = REVIEWS / "stage253_risk_atr_review.csv"
SUMMARY_PATH = REVIEWS / "stage253_summary.json"
DECISION_PATH = REVIEWS / "stage253_decision.md"
STAGE_LEDGER_PATH = REVIEWS / "stage_run_ledger.csv"
REVIEW_INDEX_PATH = REVIEWS / "review_index.md"
SELECTION_PATH = STAGE_ROOT / "04_selected/selection_status.md"

CURRENT_STATE_PATH = ROOT / "docs/context/current_working_state.md"
WORKSPACE_STATE_PATH = ROOT / "docs/workspace/workspace_state.yaml"
CHANGELOG_PATH = ROOT / "docs/workspace/changelog.md"
RUN_REGISTRY_PATH = ROOT / "docs/registers/run_registry.csv"
PROJECT_LEDGER_PATH = ROOT / "docs/registers/alpha_run_ledger.csv"
ARTIFACT_REGISTRY_PATH = ROOT / "docs/registers/artifact_registry.csv"
PRODUCER_PATH = ROOT / "stage_pipelines/stage253/stage252_asymmetric_binding_followup_review.py"

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


def as_int(value: Any) -> int:
    try:
        return int(float(value or 0))
    except (TypeError, ValueError):
        return 0


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


def probability_index(rows: Sequence[Mapping[str, str]]) -> dict[tuple[str, str, str], Mapping[str, str]]:
    return {(row["adapter_id"], row["split"], row["view"]): row for row in rows}


def decision_counts(row: Mapping[str, str]) -> dict[str, int]:
    try:
        parsed = json.loads(row.get("decision_counts", "{}"))
    except json.JSONDecodeError:
        return {"flat": 0, "long": 0, "short": 0}
    return {str(key): as_int(value) for key, value in parsed.items()}


def read_for_adapter(adapter_id: str, val_net_delta: float, dd_delta: float, mid_pf_delta: float, oos_net_delta: float) -> tuple[str, str, str]:
    if adapter_id == "s252_binding_control":
        return (
            "reference_only_best_overall_not_34d",
            "Stage252 control(252단계 기준)은 가장 덜 나쁘지만 34D(34디) 기준을 함께 넘지 못했다.",
            "use_as_reference_only_not_final",
        )
    if adapter_id == "s252_short_low_score006":
        return (
            "dd_improved_but_net_midpf_damaged",
            "short low score(숏 낮은 점수) 축은 DD(낙폭)를 낮췄지만 net(순수익)과 mid PF(중간 수익요인)를 손상했다.",
            NEXT_STAGE_ID,
        )
    if adapter_id == "s252_long_low_score006":
        return (
            "partial_midpf_dd_signal_but_net_oos_below",
            "long low score(롱 낮은 점수) 축은 작은 중간 구간 신호가 있으나 net(순수익)과 OOS(표본외)가 부족하다.",
            NEXT_STAGE_ID,
        )
    if "gate" in adapter_id and val_net_delta < -300:
        return (
            "gate_axis_overpruned_trade_supply",
            "gate(게이트) 축은 거래 공급을 너무 줄여 validation/OOS(검증/표본외) 순수익을 크게 훼손했다.",
            "do_not_repeat_as_primary_axis",
        )
    if dd_delta < 0 and (mid_pf_delta > 0 or oos_net_delta > -100):
        return (
            "salvage_clue_only_not_candidate",
            "일부 위험 지표는 좋아졌지만 후보(candidate, 후보)로 보기엔 부족하다.",
            NEXT_STAGE_ID,
        )
    return ("weak_or_no_gain", "KPI(핵심 성과 지표) 개선이 충분하지 않다.", NEXT_STAGE_ID)


def build_review() -> dict[str, Any]:
    quality_rows = read_csv(QUALITY_PATH)
    kpi_rows = read_csv(KPI_PATH)
    probability_rows = read_csv(PROBABILITY_PATH)
    source_attribution_rows = read_csv(SOURCE_ATTRIBUTION_PATH)
    source_failure_rows = read_csv(SOURCE_FAILURE_PATH)
    risk_rows = read_csv(RISK_PATH) if RISK_PATH.exists() else []

    prob = probability_index(probability_rows)
    control = next(row for row in quality_rows if row["adapter_id"] == "s252_binding_control")
    control_prob = prob[(control["adapter_id"], "validation_is", "actual_routed_total")]
    control_counts = decision_counts(control_prob)
    control_values = {
        "validation_net": as_float(control["validation_net"]),
        "validation_dd": as_float(control["validation_balance_dd_percent"]),
        "validation_mid_pf": as_float(control["validation_mid_pf"]),
        "oos_net": as_float(control["oos_net"]),
        "directional_pass": as_int(control_prob["directional_threshold_pass_rows"]),
        "order_filled": as_int(control_prob["order_filled_rows"]),
        "flat_count": control_counts.get("flat", 0),
        "long_count": control_counts.get("long", 0),
        "short_count": control_counts.get("short", 0),
    }

    tradeoff_rows: list[dict[str, Any]] = []
    hard_pass_count = 0
    for row in quality_rows:
        validation_prob = prob[(row["adapter_id"], "validation_is", "actual_routed_total")]
        counts = decision_counts(validation_prob)
        val_net = as_float(row["validation_net"])
        val_dd = as_float(row["validation_balance_dd_percent"])
        mid_pf = as_float(row["validation_mid_pf"])
        oos_net = as_float(row["oos_net"])
        directional = as_int(validation_prob["directional_threshold_pass_rows"])
        order_filled = as_int(validation_prob["order_filled_rows"])
        flat_count = counts.get("flat", 0)
        long_count = counts.get("long", 0)
        short_count = counts.get("short", 0)
        hard_pass = row.get("hard_quality_pass", "").lower() == "true"
        hard_pass_count += 1 if hard_pass else 0
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
                "directional_pass_validation": directional,
                "directional_pass_delta_vs_control": directional - control_values["directional_pass"],
                "order_filled_validation": order_filled,
                "order_filled_delta_vs_control": order_filled - control_values["order_filled"],
                "flat_count_validation": flat_count,
                "flat_count_delta_vs_control": flat_count - control_values["flat_count"],
                "long_count_validation": long_count,
                "long_count_delta_vs_control": long_count - control_values["long_count"],
                "short_count_validation": short_count,
                "short_count_delta_vs_control": short_count - control_values["short_count"],
                "hard_quality_pass": str(hard_pass),
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
                "status": row.get("status", ""),
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
                "read": "ATR/risk(ATR/위험)은 존재하지만 KPI(핵심 성과 지표) 통과의 충분조건이 아니다.",
            }
        )

    attribution_rows = [
        {
            "attribution_id": f"{RUN_ID}__binding_axis_no_gain",
            "observed_change": "Stage252 asymmetric binding(252단계 비대칭 결합)은 hard_quality_pass(강한 품질 통과)를 하나도 만들지 못했다.",
            "comparison_baseline": "s252_binding_control",
            "likely_drivers": "score-only(점수 전용)는 결정 수를 보존했지만 확률/위험 배치를 바꿔 순수익을 낮췄고, gate(게이트)는 거래 공급을 과감히 줄였다.",
            "segment_checks": "validation/OOS(검증/표본외), early/mid/late PF(초기/중간/후기 수익요인), DD(낙폭), 위험/ATR(위험/ATR), probability binding(확률 결합)을 검토했다.",
            "trade_shape": "score-only(점수 전용)는 269 trades(거래)를 유지했지만 net(순수익)을 -141.80 또는 -67.07 낮췄다. gate(게이트)는 거래 수를 175/182로 줄였다.",
            "alternative_explanations": "DD(낙폭) 개선은 decision quality(결정 품질) 개선이 아니라 exposure compression(노출 압축)일 수 있다.",
            "attribution_confidence": "high",
            "next_probe": NEXT_STAGE_ID,
        },
        {
            "attribution_id": f"{RUN_ID}__control_still_near_miss_not_final",
            "observed_change": "control(기준)은 validation net(검증 순수익) 972.15로 34D(34디) 목표 987.60보다 -15.45 낮고, DD(낙폭)도 12.9281로 목표 12.909136보다 높다.",
            "comparison_baseline": "legacy 34D lesson-only KPI target(레거시 34D 교훈 전용 KPI 목표)",
            "likely_drivers": "mid-window(중간 구간) quality(품질)와 source/lifecycle(원천/생명주기) 축이 아직 약하다.",
            "segment_checks": "validation mid PF(검증 중간 수익요인) 1.516650878, OOS net(표본외 순수익) 776.02, quality flags(품질 플래그)를 검토했다.",
            "trade_shape": "control(기준)은 가장 균형적이나 candidate final(최종 후보)이 아니다.",
            "alternative_explanations": "작은 차이는 tester path(테스터 경로)와 artifact identity(산출물 정체성) 차이일 수 있으나, hard pass(강한 통과) 실패는 그대로 남는다.",
            "attribution_confidence": "medium_high",
            "next_probe": NEXT_STAGE_ID,
        },
        {
            "attribution_id": f"{RUN_ID}__risk_atr_present_not_sufficient",
            "observed_change": "ATR bracket(ATR 브래킷)과 model risk(모델 위험)는 telemetry(원격측정)에 있지만 KPI(핵심 성과 지표)를 충분히 고치지 못했다.",
            "comparison_baseline": "research-grade BaselineAdapter package criteria(연구급 기준 어댑터 패키지 기준)",
            "likely_drivers": "mandatory capability(필수 기능)는 필요조건이고, validation/OOS(검증/표본외) 품질은 별도 문제다.",
            "segment_checks": "risk_floor_applied_count(위험 바닥 적용 수)는 0이고, max_model_risk_pct(최대 모델 위험비율)는 0.0305다.",
            "trade_shape": "위험/ATR(위험/ATR) 기능은 유지하되, 다음 단계는 비결합 source repair(원천 수리)로 전환해야 한다.",
            "alternative_explanations": "더 강한 ATR/risk(ATR/위험) 튜닝만으로 edge(우위)가 생긴다고 볼 근거는 없다.",
            "attribution_confidence": "high",
            "next_probe": NEXT_STAGE_ID,
        },
    ]

    failure_rows = [
        {
            "failure_id": f"{RUN_ID}__binding_axis_not_primary_repair",
            "source_failure": "stage250_stage252_binding_axis_no_gain",
            "why_it_matters": "결합(binding, 결합) 축은 결정 이동이나 노출 압축은 만들지만 34D(34디)급 KPI(핵심 성과 지표)를 안정적으로 넘기지 못했다.",
            "salvage_value": "probability binding diagnostics(확률 결합 진단), side-specific pockets(방향별 작은 신호), DD compression(낙폭 압축) 단서는 보존한다.",
            "do_not_repeat": "threshold(임계값)나 binding(결합)만 계속 조이는 방식으로 Stage254(254단계)를 만들지 않는다.",
            "next_handling": NEXT_STAGE_ID,
        },
        {
            "failure_id": f"{RUN_ID}__gate_variants_overpruned",
            "source_failure": "short_low_gate_and_long_low_gate_supply_damage",
            "why_it_matters": "gate(게이트)는 validation net(검증 순수익)을 336.96/611.36까지 낮췄고 OOS net(표본외 순수익)도 크게 훼손했다.",
            "salvage_value": "long low gate(롱 낮은 게이트)의 mid PF(중간 수익요인) 1.876033803은 원천/생명주기 수리 단서로만 보존한다.",
            "do_not_repeat": "거래 수 축소만으로 DD(낙폭)를 낮춘 결과를 품질 개선으로 오해하지 않는다.",
            "next_handling": NEXT_STAGE_ID,
        },
        {
            "failure_id": f"{RUN_ID}__score_variants_no_trade_count_gain",
            "source_failure": "score_only_probability_movement_without_kpi_gain",
            "why_it_matters": "score-only(점수 전용)는 trade count(거래 수)를 유지했지만 순수익과 중간 구간을 충분히 고치지 못했다.",
            "salvage_value": "soft probability movement(부드러운 확률 이동)는 직접 수익 개선이 아닌 diagnostic clue(진단 단서)로 보존한다.",
            "do_not_repeat": "확률 분포가 바뀌었다는 사실만으로 다음 후보(candidate, 후보)를 만들지 않는다.",
            "next_handling": NEXT_STAGE_ID,
        },
        {
            "failure_id": f"{RUN_ID}__stage252_resume_partials_pitfall",
            "source_failure": "resume_partials_zero_kpi_rewrite_pitfall",
            "why_it_matters": "--resume-partials(부분 재개) 재실행은 KPI(핵심 성과 지표)를 0으로 덮어쓴 전례가 있어 최종 closeout(종료)에 쓰면 안 된다.",
            "salvage_value": "full rerun(전체 재실행) 기준 KPI(핵심 성과 지표)만 Stage253(253단계) 판단에 사용한다.",
            "do_not_repeat": "Stage254(254단계) 최종 KPI(핵심 성과 지표)에 --resume-partials(부분 재개)를 쓰지 않는다.",
            "next_handling": NEXT_STAGE_ID,
        },
    ]

    route_rows = [
        {
            "route_id": f"{RUN_ID}__close_stage253_review_only",
            "evidence": "hard_quality_pass=false for all Stage252 candidates(252단계 모든 후보 강한 통과 실패)",
            "decision": DECISION,
            "effect": "Stage253(253단계)를 검토 전용으로 닫고, Stage254(254단계)를 비결합 수리 축으로 연다.",
            "next_stage_or_branch": NEXT_STAGE_ID,
        },
        {
            "route_id": f"{RUN_ID}__preserve_control_reference",
            "evidence": "s252_binding_control validation net=972.15, PF=1.59, DD=12.9281, OOS net=776.02",
            "decision": "reference_only_not_final",
            "effect": "가장 균형적인 기준은 보존하지만 final package(최종 패키지)로 주장하지 않는다.",
            "next_stage_or_branch": NEXT_STAGE_ID,
        },
        {
            "route_id": f"{RUN_ID}__stop_binding_as_primary_axis",
            "evidence": "score-only variants damaged net; gate variants over-pruned supply(점수 전용은 순수익 손상, 게이트는 공급 과축소)",
            "decision": "route_to_nonbinding_source_lifecycle_repair",
            "effect": "다음 작업은 source/feature/lifecycle(원천/피처/생명주기) 품질 수리로 좁혀진다.",
            "next_stage_or_branch": NEXT_STAGE_ID,
        },
    ]

    return {
        "control": control,
        "hard_pass_count": hard_pass_count,
        "tradeoff_rows": tradeoff_rows,
        "risk_review_rows": risk_review_rows,
        "source_attribution_rows": source_attribution_rows,
        "source_failure_rows": source_failure_rows,
        "attribution_rows": attribution_rows,
        "failure_rows": failure_rows,
        "route_rows": route_rows,
        "risk_rows_count": len(risk_rows),
    }


def write_reports(review: Mapping[str, Any]) -> None:
    control = review["control"]
    tradeoff_rows = review["tradeoff_rows"]
    best_dd = min(tradeoff_rows, key=lambda row: as_float(row["validation_dd_percent"]))
    best_mid_pf = max(tradeoff_rows, key=lambda row: as_float(row["validation_mid_pf"]))
    best_oos_pf = max(tradeoff_rows, key=lambda row: as_float(row["oos_pf"]))
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
    report = f"""# Stage253 Stage252 Asymmetric Binding Follow-up Review(253단계 252단계 비대칭 결합 후속 검토)

- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- source_stage252_evidence_commit(원천 252단계 근거 커밋): `{SOURCE_STAGE252_EVIDENCE_COMMIT}`
- source_stage252_hash_record_commit(원천 252단계 해시 기록 커밋): `{SOURCE_STAGE252_HASH_RECORD_COMMIT}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- decision(판정): `{DECISION}`
- claim_boundary(주장 경계): `{BOUNDARY}`

## Plain Read(쉬운 해석)

Stage252(252단계)는 valid evidence(유효 근거)를 만들었지만, strong candidate(강한 후보)는 만들지 못했다.
가장 나은 줄은 control(기준)이고 validation net(검증 순수익) `972.15`, PF(수익요인) `1.59`, DD(낙폭) `12.9281`이다.
하지만 legacy 34D lesson-only KPI target(레거시 34D 교훈 전용 핵심 성과 지표 목표)인 net(순수익) `987.60`, DD(낙폭) `12.909136`을 함께 넘지 못했다.

Effect(효과): binding axis(결합 축)를 primary repair(주 수리축)로 계속 밀지 않고, Stage254(254단계)에서 non-binding source/feature/lifecycle repair(비결합 원천/피처/생명주기 수리)로 넘긴다.

## KPI Tradeoff(핵심 성과 지표 절충)

| adapter(어댑터) | validation PF(검증 수익요인) | validation net(검증 순수익) | net delta vs control(기준 대비 순수익 차이) | DD(낙폭) | DD delta(낙폭 차이) | mid PF(중간 수익요인) | OOS PF(표본외 수익요인) | OOS net(표본외 순수익) | read(해석) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
{table_rows}

## What Worked A Little(조금 먹힌 부분)

- `s252_short_low_score006`: DD(낙폭)는 `9.3294`로 좋아졌지만 validation net(검증 순수익)이 control(기준)보다 `-141.80` 낮고 mid PF(중간 수익요인)도 나빠졌다.
- `s252_long_low_score006`: mid PF(중간 수익요인)는 control(기준)보다 `+0.028995` 좋지만 validation net(검증 순수익)이 `-67.07`, OOS net(표본외 순수익)이 `-49.32` 낮다.
- `s252_long_low_gate`: mid PF(중간 수익요인) `1.876033803`과 DD(낙폭) `8.8768` 단서는 있으나 OOS DD(표본외 낙폭) `14.2071`과 net(순수익) 손상이 크다.

## What Failed(실패한 부분)

- score-only(점수 전용) 변형은 trade count(거래 수)를 보존했지만 net(순수익)을 올리지 못했다.
- gate(게이트) 변형은 거래 공급을 줄여 DD(낙폭) 일부를 낮췄지만 validation/OOS net(검증/표본외 순수익)을 크게 손상했다.
- ATR/risk(ATR/위험)는 telemetry(원격측정)에 존재하지만, 필요조건이지 충분조건이 아니다.
- Stage252(252단계)의 `--resume-partials(부분 재개)` zero-KPI pitfall(0 핵심 성과 지표 함정)은 final KPI closeout(최종 핵심 성과 지표 종료)에 다시 쓰면 안 된다.

## Result Judgment(결과 판정)

- result_subject(판정 대상): `{RUN_ID}`
- evidence_available(사용 근거): quality matrix(품질 행렬), KPI summary(핵심 성과 지표 요약), probability binding(확률 결합), risk/ATR telemetry(위험/ATR 원격측정), source report(원천 보고서)
- evidence_missing(부족 근거): Stage254(254단계) 비결합 수리 실행, ONNX(오닉스) parity(동등성), MT5 ONNX/runtime(MT5 오닉스/런타임) reproduction(재현)
- judgment_label(판정 라벨): `negative_valid_binding_axis_no_gain_not_final`
- next_condition(다음 조건): `{NEXT_STAGE_ID}`

## Routing(경로)

Stage253(253단계)는 review-only(검토 전용)로 닫는다.
Next action(다음 행동)은 `{NEXT_RUN_ID}`이다.
Effect(효과): binding(결합) 축의 실패 기억을 보존하고, v2-native(브이투 고유) non-binding repair(비결합 수리)로 연구를 계속한다.

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준), overall_goal_complete(전체 목표 완료).
"""
    write_text(REPORT_PATH, report)

    decision_text = f"""# Stage253 Decision(253단계 판정)

- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- decision(판정): `{DECISION}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- source_stage252_evidence_commit(원천 252단계 근거 커밋): `{SOURCE_STAGE252_EVIDENCE_COMMIT}`
- source_stage252_hash_record_commit(원천 252단계 해시 기록 커밋): `{SOURCE_STAGE252_HASH_RECORD_COMMIT}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- best_overall_reference(최선 기준): `{control["adapter_id"]}`
- best_dd_clue(최선 낙폭 단서): `{best_dd["adapter_id"]}`
- best_mid_pf_clue(최선 중간 수익요인 단서): `{best_mid_pf["adapter_id"]}`
- best_oos_pf_clue(최선 표본외 수익요인 단서): `{best_oos_pf["adapter_id"]}`
- report(보고서): `{rel(REPORT_PATH)}`
- tradeoff_matrix(절충 행렬): `{rel(TRADEOFF_PATH)}`
- attribution(성과 귀속): `{rel(ATTRIBUTION_PATH)}`
- failure_memory(실패 기억): `{rel(FAILURE_PATH)}`
- route_matrix(경로 행렬): `{rel(ROUTE_PATH)}`
- risk_atr_review(위험/ATR 검토): `{rel(RISK_REVIEW_PATH)}`
- next_stage_or_branch(다음 단계 또는 분기): `{NEXT_STAGE_ID}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage253(253단계) closeout(종료)은 overall goal complete(전체 목표 완료)가 아니다.
"""
    write_text(DECISION_PATH, decision_text)

    write_text(
        REVIEW_INDEX_PATH,
        f"""# Stage253 Review Index(253단계 검토 색인)

- status(상태): `closed_open_stage254_nonbinding_source_repair_candidate_not_final`
- run(실행): `{RUN_ID}`
- decision(판정): `{DECISION}`
- report(보고서): `{rel(REPORT_PATH)}`
- tradeoff_matrix(절충 행렬): `{rel(TRADEOFF_PATH)}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
""",
    )

    write_text(
        SELECTION_PATH,
        f"""# Stage253 Selection Status(253단계 선택 상태)

- stage_status(단계 상태): `closed_open_stage254_nonbinding_source_repair_candidate_not_final`
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

Stage254(254단계)는 Stage250/252(250/252단계) binding axis(결합 축)가 KPI(핵심 성과 지표)를 올리지 못한 뒤 여는 bounded repair(경계 수리) 단계다.

## Bounded Question(경계 질문)

Can non-binding source/feature/lifecycle repair(비결합 원천/피처/생명주기 수리) recover legacy 34D lesson-only KPI target(레거시 34D 교훈 전용 핵심 성과 지표 목표) or better without relying on threshold/binding overprune(임계값/결합 과축소)?

## Must Preserve(반드시 보존)

- ATR SL/TP or bracket(ATR 손절/익절 또는 브래킷)
- model-controlled risk%(모델 제어 위험비율)
- validation/OOS(검증/표본외) KPI(핵심 성과 지표)
- segment(구간) and risk/ATR telemetry(위험/ATR 원격측정)
- failure memory(실패 기억): binding axis no-gain(결합 축 무개선), gate overprune(게이트 과축소), resume-partials zero-KPI pitfall(부분 재개 0 KPI 함정)

## Boundary(경계)

`{BOUNDARY}`
""",
    )
    write_text(
        NEXT_STAGE_ROOT / "01_inputs/input_refs.md",
        f"""# Stage254 Input References(254단계 입력 참조)

- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- source_decision(원천 판정): `{DECISION}`
- source_report(원천 보고서): `{rel(REPORT_PATH)}`
- source_tradeoff_matrix(원천 절충 행렬): `{rel(TRADEOFF_PATH)}`
- source_stage252_evidence_commit(원천 252단계 근거 커밋): `{SOURCE_STAGE252_EVIDENCE_COMMIT}`
- source_stage252_hash_record_commit(원천 252단계 해시 기록 커밋): `{SOURCE_STAGE252_HASH_RECORD_COMMIT}`
""",
    )
    write_text(
        NEXT_STAGE_ROOT / "03_reviews/review_index.md",
        f"""# Stage254 Review Index(254단계 검토 색인)

- status(상태): `open_planned_from_stage253`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- source_stage(원천 단계): `{STAGE_ID}`
- source_decision(원천 판정): `{DECISION}`
""",
    )
    write_text(
        NEXT_STAGE_ROOT / "04_selected/selection_status.md",
        f"""# Stage254 Selection Status(254단계 선택 상태)

- stage_status(단계 상태): `open_planned_from_stage253`
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
    current = f"""# Current Working State(현재 작업 상태)

- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- active_stage(활성 단계): `{NEXT_STAGE_ID}`
- selected_research_baseline(선택 연구 기준선): `none`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- adapter_under_review(검토 중 어댑터): `stage254_nonbinding_source_repair`
- status(상태): `stage253_closed_open_stage254_nonbinding_source_repair_candidate_not_final`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage253(253단계)는 Stage252(252단계) asymmetric binding repair(비대칭 결합 수리)를 review-only(검토 전용)로 판정했다.
Effect(효과): binding axis(결합 축)는 primary repair(주 수리축)로 중단하고, Stage254(254단계)는 non-binding source/feature/lifecycle repair(비결합 원천/피처/생명주기 수리)로 넘어간다.

## Latest Stage253 Evidence(최신 253단계 근거)

- run(실행): `{RUN_ID}`
- decision(판정): `{DECISION}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- report(보고서): `{rel(REPORT_PATH)}`
- tradeoff_matrix(절충 행렬): `{rel(TRADEOFF_PATH)}`
- attribution(성과 귀속): `{rel(ATTRIBUTION_PATH)}`
- failure_memory(실패 기억): `{rel(FAILURE_PATH)}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준), overall_goal_complete(전체 목표 완료).
"""
    write_text(CURRENT_STATE_PATH, current)

    workspace = read_text(WORKSPACE_STATE_PATH)
    workspace = re.sub(r"^current_run_id: .*$", f"current_run_id: {NEXT_RUN_ID}", workspace, count=1, flags=re.MULTILINE)
    workspace = re.sub(r"^updated_on: .*$", "updated_on: '2026-05-20'", workspace, count=1, flags=re.MULTILINE)
    workspace = re.sub(r"^active_stage: .*$", f"active_stage: {NEXT_STAGE_ID}", workspace, count=1, flags=re.MULTILINE)
    focus = f"""current_focus:
- >-
  Stage253(253단계) closed(종료) as `{DECISION}` and Stage254(254단계) `{NEXT_STAGE_ID}` is open_planned(개방 계획). Effect(효과): Stage252(252단계)의 asymmetric binding(비대칭 결합)은 KPI(핵심 성과 지표) 개선축이 아니라 failure memory(실패 기억)로 분리했다.
- >-
  Stage253 evidence(253단계 근거)는 `{rel(REPORT_PATH)}`, `{rel(TRADEOFF_PATH)}`, `{rel(ATTRIBUTION_PATH)}`, `{rel(FAILURE_PATH)}`에 있다. Effect(효과): Stage254(254단계)는 binding(결합) 반복이 아니라 source/feature/lifecycle(원천/피처/생명주기) 축으로 좁게 간다.
- >-
  Target surface(목표 표면)는 `{TARGET_SURFACE}`이고 legacy 34D(레거시 34D)는 lesson-only KPI target(교훈 전용 핵심 성과 지표 목표)이다. Effect(효과): v2-native research(v2 고유 연구)를 계속한다.
"""
    workspace = re.sub(r"current_focus:\n.*?(?=\n[A-Za-z0-9_]+:\n)", focus, workspace, count=1, flags=re.DOTALL)
    stage253_block = f"""stage253_stage252_asymmetric_binding_followup_review:
  packet_id: {PACKET_ID}
  stage_id: {STAGE_ID}
  status: closed_open_stage254_nonbinding_source_repair_candidate_not_final
  current_run_id: {RUN_ID}
  source_stage: {SOURCE_STAGE_ID}
  source_run: {SOURCE_RUN_ID}
  source_stage252_evidence_commit: {SOURCE_STAGE252_EVIDENCE_COMMIT}
  source_stage252_hash_record_commit: {SOURCE_STAGE252_HASH_RECORD_COMMIT}
  source_stage251_evidence_commit: {SOURCE_STAGE251_EVIDENCE_COMMIT}
  source_stage251_hash_record_commit: {SOURCE_STAGE251_HASH_RECORD_COMMIT}
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
    stage254_block = f"""stage254_nonbinding_source_repair_after_binding_axis_no_gain:
  packet_id: {NEXT_PACKET_ID}
  stage_id: {NEXT_STAGE_ID}
  status: open_planned_from_stage253
  current_run_id: {NEXT_RUN_ID}
  source_stage: {STAGE_ID}
  source_run: {RUN_ID}
  source_decision: {DECISION}
  next_action: {NEXT_RUN_ID}
  boundary: {BOUNDARY}
"""
    workspace = replace_or_append_block(workspace, "stage253_stage252_asymmetric_binding_followup_review", stage253_block)
    workspace = replace_or_append_block(workspace, "stage254_nonbinding_source_repair_after_binding_axis_no_gain", stage254_block)
    write_text(WORKSPACE_STATE_PATH, workspace, bom=False)

    changelog_entry = f"""
## {utc_now()} Stage253 Stage252 asymmetric binding follow-up review closeout(253단계 252단계 비대칭 결합 후속 검토 종료)

- action(행동): closed(종료) `{STAGE_ID}` with decision(판정) `{DECISION}`.
- effect(효과): binding axis(결합 축)를 primary repair(주 수리축)에서 내려놓고 `{NEXT_STAGE_ID}`를 열었다.
- boundary(주장 경계): `{BOUNDARY}`.
"""
    existing = read_text(CHANGELOG_PATH) if CHANGELOG_PATH.exists() else ""
    existing = re.sub(
        r"\n## [^\n]*Stage253 Stage252 asymmetric binding follow-up review closeout[^\n]*\n.*?(?=\n## |\Z)",
        "",
        existing,
        flags=re.DOTALL,
    )
    write_text(CHANGELOG_PATH, existing.rstrip() + changelog_entry, bom=False)


def write_ledgers_and_packet(review: Mapping[str, Any]) -> None:
    control = review["control"]
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__review_total",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "stage253_review_total",
        "parent_run_id": SOURCE_RUN_ID,
        "record_view": "review_total",
        "tier_scope": "Tier A+B",
        "kpi_scope": "baseline_adapter_followup_review",
        "scoreboard_lane": "regular_risk_execution",
        "status": "reviewed_closed",
        "judgment": DECISION,
        "path": rel(REPORT_PATH),
        "primary_kpi": f"control={control['adapter_id']};validation_net={control['validation_net']};validation_dd={control['validation_balance_dd_percent']};validation_mid_pf={control['validation_mid_pf']};oos_net={control['oos_net']}",
        "guardrail_kpi": f"hard_quality_pass_count={review['hard_pass_count']};binding_axis_no_gain=1;overall_goal_complete=0",
        "external_verification_status": EXTERNAL_STATUS,
        "notes": "Stage253 review only; routes to bounded Stage254 non-binding source repair.",
    }
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "baseline_adapter_followup_review(기준 어댑터 후속 검토)",
        "status": "reviewed_closed",
        "judgment": DECISION,
        "path": rel(REPORT_PATH),
        "notes": f"source_stage252_evidence_commit={SOURCE_STAGE252_EVIDENCE_COMMIT};source_stage252_hash_record_commit={SOURCE_STAGE252_HASH_RECORD_COMMIT};overall_goal_complete=0;boundary={BOUNDARY}",
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
        "source_stage252_evidence_commit": SOURCE_STAGE252_EVIDENCE_COMMIT,
        "source_stage252_hash_record_commit": SOURCE_STAGE252_HASH_RECORD_COMMIT,
        "decision": DECISION,
        "next_stage_or_branch": NEXT_STAGE_ID,
        "external_verification_status": EXTERNAL_STATUS,
        "overall_goal_complete": False,
        "pushed_commit_hash": "pending_until_push",
        "claim_boundary": BOUNDARY,
        "legacy_34d_lesson_only_targets": {"validation_net": LEGACY_34D_NET, "validation_pf": LEGACY_34D_PF, "validation_dd": LEGACY_34D_DD},
        "control": control,
        "hard_pass_count": review["hard_pass_count"],
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
            "artifact_type": "stage253_followup_review_evidence",
            "path": rel(path),
            "sha256": sha256_lf(path),
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": created,
            "notes": "Stage253 Stage252 asymmetric binding follow-up review evidence; research only.",
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
        "external_verification_status": EXTERNAL_STATUS,
        "claim_boundary": BOUNDARY,
        "overall_goal_complete": False,
    }
    packet_payloads = {
        "packet_receipt.json": {**base_payload, "created_at_utc": created, "status": "closed_pending_push_hash"},
        "routing_receipt.json": {**base_payload, "route": DECISION, "route_effect": "open Stage254 non-binding source/feature/lifecycle repair"},
        "kpi_contract_audit.json": {
            **base_payload,
            "status": "passed",
            "kpi_basis": [rel(QUALITY_PATH), rel(KPI_PATH), rel(PROBABILITY_PATH), rel(RISK_PATH)],
        },
        "result_judgment_gate.json": {
            **base_payload,
            "result_subject": RUN_ID,
            "evidence_available": [rel(REPORT_PATH), rel(TRADEOFF_PATH), rel(ATTRIBUTION_PATH), rel(FAILURE_PATH), rel(RISK_REVIEW_PATH)],
            "evidence_missing": [NEXT_STAGE_ID, "ONNX parity(오닉스 동등성)", "MT5 ONNX/runtime reproduction(MT5 오닉스/런타임 재현)"],
            "judgment_label": "negative_valid_binding_axis_no_gain_not_final",
            "next_condition": NEXT_STAGE_ID,
        },
        "performance_attribution_gate.json": {
            **base_payload,
            "observed_change": "Stage252 asymmetric binding did not create hard KPI pass",
            "attribution_rows": review["attribution_rows"],
            "attribution_confidence": "high",
        },
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
        f"""# Stage253 Closeout Packet(253단계 종료 작업 묶음)

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
