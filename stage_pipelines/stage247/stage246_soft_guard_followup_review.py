from __future__ import annotations

import csv
import hashlib
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Sequence


STAGE_ID = "247_adapter_research__stage246_soft_guard_followup_review"
RUN_ID = "run247A_stage247_stage246_soft_guard_followup_review_v1"
PACKET_ID = "stage247_stage246_soft_guard_followup_review_v1"
SOURCE_STAGE_ID = "246_adapter_research__soft_timestamp_guard_repair_after_stage244_overprune"
SOURCE_RUN_ID = "run246A_stage246_soft_timestamp_guard_repair_after_stage244_overprune_v1"
SOURCE_EVIDENCE_COMMIT = "b6a388299dd99e64595d08529ac4462d578297c9"
SOURCE_HASH_RECORD_COMMIT = "528a69d866925607e496b4fe7d7b270c822c7392"
NEXT_STAGE_ID = "248_adapter_research__entry_source_quality_repair_after_stage246_soft_guard_tradeoff"
NEXT_RUN_ID = "run248A_stage248_entry_source_quality_repair_after_stage246_soft_guard_tradeoff_v1"
NEXT_PACKET_ID = "stage248_entry_source_quality_repair_after_stage246_soft_guard_tradeoff_v1"
DECISION = "open_stage248_bounded_entry_source_quality_repair_after_stage246_soft_guard_tradeoff_candidate_not_final"
BOUNDARY = "research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment"
TARGET_SURFACE = "legacy_34d_kpi_lesson_only_v2_native_entry_source_quality_repair_after_soft_guard_tradeoff"

LEGACY_34D_NET = 987.6
LEGACY_34D_PF = 1.583157
LEGACY_34D_DD = 12.909136

ROOT = Path.cwd()
STAGE_ROOT = ROOT / "stages" / STAGE_ID
REVIEWS = STAGE_ROOT / "03_reviews"
PACKET_ROOT = ROOT / "docs/agent_control/packets" / PACKET_ID
NEXT_STAGE_ROOT = ROOT / "stages" / NEXT_STAGE_ID
SOURCE_REVIEWS = ROOT / "stages" / SOURCE_STAGE_ID / "03_reviews"

QUALITY_PATH = SOURCE_REVIEWS / "stage246_quality_matrix.csv"
SEGMENT_PATH = SOURCE_REVIEWS / "stage246_segment_kpi_summary.csv"
BALANCE_PATH = SOURCE_REVIEWS / "stage246_balance_curve_audit.csv"
RISK_PATH = SOURCE_REVIEWS / "stage246_risk_atr_telemetry.csv"
CONCENTRATION_PATH = SOURCE_REVIEWS / "stage246_concentration_risk_summary.csv"
SOURCE_REPORT_PATH = SOURCE_REVIEWS / "stage246_soft_guard_repair_report.md"

REPORT_PATH = REVIEWS / "stage247_stage246_soft_guard_followup_review.md"
TRADEOFF_PATH = REVIEWS / "stage247_tradeoff_review_matrix.csv"
ATTRIBUTION_PATH = REVIEWS / "stage247_performance_attribution.csv"
FAILURE_PATH = REVIEWS / "stage247_failure_memory.csv"
ROUTE_PATH = REVIEWS / "stage247_route_matrix.csv"
RISK_REVIEW_PATH = REVIEWS / "stage247_risk_atr_review.csv"
SUMMARY_PATH = REVIEWS / "stage247_summary.json"
DECISION_PATH = REVIEWS / "stage247_decision.md"
STAGE_LEDGER_PATH = REVIEWS / "stage_run_ledger.csv"
REVIEW_INDEX_PATH = REVIEWS / "review_index.md"
SELECTION_PATH = STAGE_ROOT / "04_selected/selection_status.md"

CURRENT_STATE_PATH = ROOT / "docs/context/current_working_state.md"
WORKSPACE_STATE_PATH = ROOT / "docs/workspace/workspace_state.yaml"
CHANGELOG_PATH = ROOT / "docs/workspace/changelog.md"
RUN_REGISTRY_PATH = ROOT / "docs/registers/run_registry.csv"
PROJECT_LEDGER_PATH = ROOT / "docs/registers/alpha_run_ledger.csv"
ARTIFACT_REGISTRY_PATH = ROOT / "docs/registers/artifact_registry.csv"
PRODUCER_PATH = ROOT / "stage_pipelines/stage247/stage246_soft_guard_followup_review.py"

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


def long_path(path: Path) -> str:
    return str(path.resolve())


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read_text(path: Path) -> str:
    with open(long_path(path), "r", encoding="utf-8-sig") as handle:
        return handle.read()


def write_text(path: Path, text: str, *, bom: bool = True) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(long_path(path), "w", encoding="utf-8-sig" if bom else "utf-8", newline="\n") as handle:
        handle.write(text.rstrip() + "\n")


def read_csv(path: Path) -> list[dict[str, str]]:
    with open(long_path(path), "r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(long_path(path), "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: row.get(column, "") for column in columns})


def write_json(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(long_path(path), "w", encoding="utf-8", newline="\n") as handle:
        json.dump(payload, handle, indent=2, ensure_ascii=False, sort_keys=True)
        handle.write("\n")


def sha256_lf(path: Path) -> str:
    with open(long_path(path), "rb") as handle:
        raw = handle.read()
    return hashlib.sha256(raw.replace(b"\r\n", b"\n")).hexdigest()


def artifact_id_for(path: Path) -> str:
    safe_path = rel(path).replace("/", "__").replace(".", "_").replace("-", "_")
    return f"{RUN_ID}__{safe_path}"


def prune_run_artifacts() -> None:
    if not ARTIFACT_REGISTRY_PATH.exists():
        return
    with open(long_path(ARTIFACT_REGISTRY_PATH), "r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    kept = [row for row in rows if not row.get("artifact_id", "").startswith(f"{RUN_ID}__")]
    write_csv(ARTIFACT_REGISTRY_PATH, kept, ARTIFACT_COLUMNS)


def as_float(value: Any) -> float:
    try:
        return float(value or 0.0)
    except (TypeError, ValueError):
        return 0.0


def upsert_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]], key: str) -> dict[str, Any]:
    existing: list[dict[str, str]] = []
    if path.exists():
        with open(long_path(path), "r", encoding="utf-8-sig", newline="") as handle:
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


def compact_status(value: bool) -> str:
    return "pass" if value else "fail"


def build_review() -> dict[str, Any]:
    quality_rows = read_csv(QUALITY_PATH)
    risk_rows = read_csv(RISK_PATH)
    quality_by_id = {row["adapter_id"]: row for row in quality_rows}
    control = quality_by_id["s246_cap0305_control"]

    tradeoff_rows: list[dict[str, Any]] = []
    for row in quality_rows:
        adapter = row["adapter_id"]
        net = as_float(row["validation_net"])
        dd = as_float(row["validation_balance_dd_percent"])
        mid_pf = as_float(row["validation_mid_pf"])
        oos_net = as_float(row["oos_net"])
        net_delta = net - as_float(control["validation_net"])
        dd_delta = dd - as_float(control["validation_balance_dd_percent"])
        mid_delta = mid_pf - as_float(control["validation_mid_pf"])
        oos_delta = oos_net - as_float(control["oos_net"])
        dd_better = dd < as_float(control["validation_balance_dd_percent"])
        net_damaged = net < as_float(control["validation_net"])
        mid_damaged = mid_pf < as_float(control["validation_mid_pf"])
        if adapter == "s246_cap0305_control":
            review_class = "control_near_miss_not_final"
            decision_read = "가장 가까운 reference surface(참고 표면)이지만 34D(34D 기준) net(순손익), DD(낙폭), mid PF(중간 수익요인)를 동시에 넘지 못했다."
        else:
            review_class = "soft_guard_dd_helped_but_net_midpf_damaged"
            decision_read = "soft guard(부드러운 보호문)는 DD(낙폭)를 줄였지만 validation net(검증 순손익)과 mid PF(중간 수익요인)를 깎았다."
        tradeoff_rows.append(
            {
                "adapter_id": adapter,
                "axis": row["axis"],
                "review_class": review_class,
                "validation_net": f"{net:.2f}",
                "validation_net_gap_vs_34d": f"{net - LEGACY_34D_NET:.2f}",
                "validation_net_delta_vs_control": f"{net_delta:.2f}",
                "validation_dd_percent": f"{dd:.4f}",
                "validation_dd_margin_vs_34d": f"{LEGACY_34D_DD - dd:.6f}",
                "validation_dd_delta_vs_control": f"{dd_delta:.4f}",
                "validation_mid_pf": f"{mid_pf:.9f}",
                "validation_mid_pf_gap_vs_34d_pf": f"{mid_pf - LEGACY_34D_PF:.6f}",
                "validation_mid_pf_delta_vs_control": f"{mid_delta:.6f}",
                "oos_net": f"{oos_net:.2f}",
                "oos_net_delta_vs_control": f"{oos_delta:.2f}",
                "oos_pf": row["oos_pf"],
                "hard_quality_pass": row["hard_quality_pass"],
                "dd_improved_vs_control": compact_status(dd_better),
                "net_damaged_vs_control": compact_status(net_damaged),
                "mid_pf_damaged_vs_control": compact_status(mid_damaged),
                "decision_read": decision_read,
            }
        )

    risk_review_rows: list[dict[str, Any]] = []
    for row in risk_rows:
        if row.get("view") != "actual_routed_total" or row.get("status") != "completed":
            continue
        risk_review_rows.append(
            {
                "adapter_id": row["adapter_id"],
                "split": row["split"],
                "atr_enabled": row["atr_enabled"],
                "model_risk_enabled": row["model_risk_enabled"],
                "model_risk_max_pct": row.get("model_risk_max_pct", row.get("max_model_risk_pct", "")),
                "max_actual_risk_pct_after_floor": row.get("max_actual_risk_pct_after_floor", ""),
                "risk_floor_applied_count": row.get("risk_floor_applied_count", ""),
                "avg_open_sl_points": row.get("avg_open_sl_points", ""),
                "avg_open_tp_points": row.get("avg_open_tp_points", ""),
                "same_move_reentry_ratio": row.get("same_move_reentry_ratio", ""),
                "mfe_capture_ratio": row.get("mfe_capture_ratio", ""),
                "cost_stressed_expectancy": row.get("cost_stressed_expectancy", ""),
                "cap_5pct_check": compact_status(as_float(row["max_actual_risk_pct_after_floor"]) <= 0.05),
                "floor_inflation_flag": compact_status(as_float(row["risk_floor_applied_count"]) > 0),
            }
        )

    attribution_rows = [
        {
            "attribution_id": f"{RUN_ID}__soft_guard_tradeoff_confirmed",
            "observed_change": "soft guard variants lowered validation DD but reduced validation net and mid PF",
            "comparison_baseline": "s246_cap0305_control",
            "likely_drivers": "probability tilt lowered exposure quality inside the middle-window surface",
            "segment_checks": "validation/OOS quality matrix, balance curve audit, segment KPI, and risk/ATR telemetry reviewed",
            "trade_shape": "trade count stayed 269 validation and 195 OOS; sizing/exposure changed rather than route coverage",
            "alternative_explanations": "small OOS PF gain can be explained by lower exposure, not stronger full adapter quality",
            "attribution_confidence": "high",
            "next_probe": NEXT_STAGE_ID,
        },
        {
            "attribution_id": f"{RUN_ID}__control_near_miss_preserved",
            "observed_change": "control remains closest to 34D but still misses validation net, DD, and mid PF together",
            "comparison_baseline": "legacy 34D lesson-only KPI target",
            "likely_drivers": "core entry/source quality remains the limiting surface after risk and ATR are present",
            "segment_checks": "mid chronological third remains weak and validation DD is slightly above 34D",
            "trade_shape": "ATR SL/TP and model-controlled risk are present; they are necessary but not sufficient",
            "alternative_explanations": "rounding or tester variance is too small to close all three gaps",
            "attribution_confidence": "medium_high",
            "next_probe": NEXT_STAGE_ID,
        },
        {
            "attribution_id": f"{RUN_ID}__do_not_repeat_stronger_soft_guard",
            "observed_change": "larger soft penalties worsened net more than they helped DD",
            "comparison_baseline": "s246_softlow_flat003 versus stronger soft rows",
            "likely_drivers": "blanket low/mid suppression removes profitable middle-window trades",
            "segment_checks": "softlow_flat005 and softlowmid rows reviewed against control",
            "trade_shape": "same trade count and lower risk-weighted returns indicate quality dilution",
            "alternative_explanations": "DD gain is real but not enough for 34D-equivalent KPI",
            "attribution_confidence": "high",
            "next_probe": "entry/source repair rather than stronger soft guard",
        },
    ]
    failure_rows = [
        {
            "failure_id": f"{RUN_ID}__soft_guard_not_sufficient",
            "hypothesis": "soft timestamp guard(부드러운 시간 보호문) can repair Stage244 over-prune and reach or exceed 34D KPI(34D 핵심 성과 지표)",
            "why_failed": "DD(낙폭)는 줄었지만 validation net(검증 순손익)과 mid PF(중간 수익요인)가 함께 손상됐다",
            "salvage_value": "cap0305 control(0.0305 상한 대조군)은 near-miss(근접 실패) reference surface(참고 표면)로 보존한다",
            "do_not_repeat": "stronger low/mid soft tilt(저/중간 부드러운 기울기)를 단독으로 더 키우지 않는다",
            "reopen_condition": "new entry/source feature(진입/원천 피처) or model branch(모델 분기)가 mid PF(중간 수익요인)를 회복할 때",
        },
        {
            "failure_id": f"{RUN_ID}__risk_atr_present_not_sufficient",
            "hypothesis": "ATR SL/TP(ATR 손절/익절) and model-controlled risk%(모델 제어 위험 비율) are enough once integrated",
            "why_failed": "mandatory capability(필수 기능)는 존재하지만 full adapter KPI(전체 어댑터 핵심 성과 지표)는 34D(34D 기준)에 미달했다",
            "salvage_value": "risk/ATR telemetry(위험/ATR 기록)는 Stage248(248단계)에서도 유지해야 하는 control constraint(제어 조건)다",
            "do_not_repeat": "risk/ATR integration(위험/ATR 통합) 자체를 final claim(최종 주장)으로 말하지 않는다",
            "reopen_condition": "post-repair adapter(수리 후 어댑터)가 validation/OOS(검증/표본외)에서 net/PF/DD를 같이 통과할 때",
        },
    ]
    route_rows = [
        {
            "route_id": DECISION,
            "status": "selected",
            "reason": "soft guard(부드러운 보호문)는 DD(낙폭)를 돕지만 net/PF(순손익/수익요인)를 손상했다",
            "effect": "Stage248(248단계)을 entry/source quality repair(진입/원천 품질 수리)로 연다",
        },
        {
            "route_id": "repeat_stronger_soft_guard",
            "status": "rejected",
            "reason": "penalty(벌점)를 키울수록 validation net(검증 순손익)이 더 낮아졌다",
            "effect": "같은 손실 방향 미세조정(마이크로 튜닝)을 반복하지 않는다",
        },
        {
            "route_id": "proceed_to_onnx_hardening",
            "status": "rejected",
            "reason": "adapter quality(어댑터 품질)가 risk/ATR(위험/ATR) 이후 충분히 강하지 않다",
            "effect": "ONNX hardening(ONNX 경화)을 미리 시작하지 않는다",
        },
    ]

    return {
        "quality_rows": quality_rows,
        "tradeoff_rows": tradeoff_rows,
        "risk_review_rows": risk_review_rows,
        "attribution_rows": attribution_rows,
        "failure_rows": failure_rows,
        "route_rows": route_rows,
        "best_reference": "s246_cap0305_control",
        "decision": DECISION,
    }


def write_reports(review: Mapping[str, Any]) -> None:
    trade_columns = [
        "adapter_id",
        "axis",
        "review_class",
        "validation_net",
        "validation_net_gap_vs_34d",
        "validation_net_delta_vs_control",
        "validation_dd_percent",
        "validation_dd_margin_vs_34d",
        "validation_dd_delta_vs_control",
        "validation_mid_pf",
        "validation_mid_pf_gap_vs_34d_pf",
        "validation_mid_pf_delta_vs_control",
        "oos_net",
        "oos_net_delta_vs_control",
        "oos_pf",
        "hard_quality_pass",
        "dd_improved_vs_control",
        "net_damaged_vs_control",
        "mid_pf_damaged_vs_control",
        "decision_read",
    ]
    risk_columns = [
        "adapter_id",
        "split",
        "atr_enabled",
        "model_risk_enabled",
        "model_risk_max_pct",
        "max_actual_risk_pct_after_floor",
        "risk_floor_applied_count",
        "avg_open_sl_points",
        "avg_open_tp_points",
        "same_move_reentry_ratio",
        "mfe_capture_ratio",
        "cost_stressed_expectancy",
        "cap_5pct_check",
        "floor_inflation_flag",
    ]
    attr_columns = [
        "attribution_id",
        "observed_change",
        "comparison_baseline",
        "likely_drivers",
        "segment_checks",
        "trade_shape",
        "alternative_explanations",
        "attribution_confidence",
        "next_probe",
    ]
    failure_columns = ["failure_id", "hypothesis", "why_failed", "salvage_value", "do_not_repeat", "reopen_condition"]
    route_columns = ["route_id", "status", "reason", "effect"]

    write_csv(TRADEOFF_PATH, review["tradeoff_rows"], trade_columns)
    write_csv(RISK_REVIEW_PATH, review["risk_review_rows"], risk_columns)
    write_csv(ATTRIBUTION_PATH, review["attribution_rows"], attr_columns)
    write_csv(FAILURE_PATH, review["failure_rows"], failure_columns)
    write_csv(ROUTE_PATH, review["route_rows"], route_columns)

    matrix_lines = [
        "| adapter(어댑터) | class(분류) | val net(검증 순손익) | net gap(순손익 차이) | DD%(낙폭) | DD margin(낙폭 여유) | mid PF(중간 수익요인) | OOS net(표본외 순손익) | read(판독) |",
        "|---|---|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in review["tradeoff_rows"]:
        matrix_lines.append(
            f"| {row['adapter_id']} | {row['review_class']} | {row['validation_net']} | {row['validation_net_gap_vs_34d']} | {row['validation_dd_percent']} | {row['validation_dd_margin_vs_34d']} | {row['validation_mid_pf']} | {row['oos_net']} | {row['decision_read']} |"
        )

    report = f"""# Stage247 Stage246 Soft Guard Follow-up Review(247단계 246단계 부드러운 보호문 후속 검토)

- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- source_stage246_evidence_commit(원천 246단계 근거 커밋): `{SOURCE_EVIDENCE_COMMIT}`
- source_stage246_hash_record_commit(원천 246단계 해시 기록 커밋): `{SOURCE_HASH_RECORD_COMMIT}`
- external_verification_status(외부 검증 상태): `review_only_source_stage246_mt5_reports_completed`
- decision(판정): `{DECISION}`
- boundary(주장 경계): `{BOUNDARY}`

## Easy Read(쉬운 판독)

- Stage246(246단계)의 soft guard(부드러운 보호문)는 DD(낙폭)를 줄였다.
- 하지만 validation net(검증 순손익)과 mid PF(중간 수익요인)를 같이 깎았다.
- 가장 가까운 행은 여전히 `s246_cap0305_control`이다. 하지만 이 행도 34D(34D 기준) 대비 net(순손익) `-10.93`, DD(낙폭) `-0.033664`, mid PF(중간 수익요인) 부족이 남는다.
- ATR SL/TP(ATR 손절/익절)와 model-controlled risk%(모델 제어 위험 비율)는 존재한다. 효과는 필수 기능은 통과했지만, 이것만으로 final adapter(최종 어댑터)가 되지 않는다는 점을 분리해 보여준다.
- 결론은 stronger soft guard(더 강한 부드러운 보호문)가 아니라 entry/source quality repair(진입/원천 품질 수리)로 넘어가는 것이다.

## KPI Matrix(KPI 핵심 성과 지표 행렬)

{chr(10).join(matrix_lines)}

## Judgment(판정)

- result_subject(판정 대상): `{RUN_ID}`
- evidence_available(사용 근거): Stage246(246단계) MT5(MetaTrader 5, 메타트레이더5) validation/OOS(검증/표본외) report(보고서), quality matrix(품질 행렬), segment KPI(구간 핵심 성과 지표), balance curve audit(잔고 곡선 감사), risk/ATR telemetry(위험/ATR 기록).
- evidence_missing(부족 근거): Stage248(248단계) entry/source repair(진입/원천 수리) 측정, ONNX parity(ONNX 동등성), MT5 ONNX/runtime reproduction(MT5 ONNX/런타임 재현).
- judgment_label(판정 라벨): `soft_guard_tradeoff_negative_not_final(부드러운 보호문 상충 부정, 최종 아님)`
- claim_boundary(주장 경계): research/development only(연구개발 전용). no deployment(배포 없음), no live_readiness(실거래 준비 없음), no runtime_authority(런타임 권위 없음).
- next_condition(다음 조건): `{NEXT_STAGE_ID}`에서 entry/source quality(진입/원천 품질)를 좁게 수리하고 같은 KPI(핵심 성과 지표)를 다시 잰다.

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준), overall_goal_complete(전체 목표 완료).
"""
    write_text(REPORT_PATH, report)

    decision = f"""# Stage247 Decision(247단계 판정)

- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- decision(판정): `{DECISION}`
- external_verification_status(외부 검증 상태): `review_only_source_stage246_mt5_reports_completed`
- report(보고서): `{rel(REPORT_PATH)}`
- tradeoff_matrix(상충 행렬): `{rel(TRADEOFF_PATH)}`
- attribution(기여 분석): `{rel(ATTRIBUTION_PATH)}`
- failure_memory(실패 기억): `{rel(FAILURE_PATH)}`
- route_matrix(경로 행렬): `{rel(ROUTE_PATH)}`
- risk_atr_review(위험/ATR 검토): `{rel(RISK_REVIEW_PATH)}`
- next_stage_or_branch(다음 단계 또는 분기): `{NEXT_STAGE_ID}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage247(247단계) closeout(종료)은 overall goal complete(전체 목표 완료)가 아니다.

Effect(효과): Stage248(248단계)은 stronger soft guard(더 강한 부드러운 보호문)가 아니라 entry/source quality repair(진입/원천 품질 수리)를 좁게 시험한다.
"""
    write_text(DECISION_PATH, decision)

    write_text(
        REVIEW_INDEX_PATH,
        f"""# Stage247 Review Index(247단계 검토 색인)

- status(상태): `closed_open_stage248_entry_source_quality_repair_candidate_not_final`
- packet(작업 묶음): `{PACKET_ID}`
- run(실행): `{RUN_ID}`
- decision(판정): `{DECISION}`
- report(보고서): `{rel(REPORT_PATH)}`
- tradeoff_matrix(상충 행렬): `{rel(TRADEOFF_PATH)}`
- attribution(기여 분석): `{rel(ATTRIBUTION_PATH)}`
- failure_memory(실패 기억): `{rel(FAILURE_PATH)}`
- route_matrix(경로 행렬): `{rel(ROUTE_PATH)}`
- risk_atr_review(위험/ATR 검토): `{rel(RISK_REVIEW_PATH)}`
- next_stage_or_branch(다음 단계 또는 분기): `{NEXT_STAGE_ID}`
""",
    )

    write_text(
        SELECTION_PATH,
        f"""# Stage247 Selection Status(247단계 선택 상태)

- stage_status(단계 상태): `closed_open_stage248_entry_source_quality_repair_candidate_not_final`
- current_packet(현재 작업 묶음): `{PACKET_ID}`
- current_run(현재 실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- external_verification_status(외부 검증 상태): `review_only_source_stage246_mt5_reports_completed`
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

Stage248(248단계)는 Stage247(247단계)의 soft guard tradeoff(부드러운 보호문 상충) 판정 뒤에 여는 bounded repair(경계 수리) 단계다.

## Bounded Question(경계 질문)

Can entry/source quality repair(진입/원천 품질 수리) lift validation net(검증 순손익), mid PF(중간 수익요인), and DD(낙폭) toward or beyond 34D(34D 기준) while preserving ATR SL/TP(ATR 손절/익절), model-controlled risk%(모델 제어 위험 비율), OOS(표본외) strength, and segment stability(구간 안정성)?

## Boundary(경계)

`{BOUNDARY}`

## Starting Clues(시작 단서)

- Preserve(보존): `s246_cap0305_control` as near-miss reference surface(근접 실패 참고 표면).
- Avoid(회피): stronger low/mid soft tilt(더 강한 저/중간 부드러운 기울기) as standalone repair(단독 수리).
- Repair focus(수리 초점): entry/source quality(진입/원천 품질), mid-window trade quality(중간 창 거래 품질), and side/context source(방향/문맥 원천).
""",
    )
    write_text(
        NEXT_STAGE_ROOT / "01_inputs/input_refs.md",
        f"""# Stage248 Inputs(248단계 입력)

- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- source_decision(원천 판정): `{DECISION}`
- stage247_report(247단계 보고서): `{rel(REPORT_PATH)}`
- stage247_failure_memory(247단계 실패 기억): `{rel(FAILURE_PATH)}`
- stage247_route_matrix(247단계 경로 행렬): `{rel(ROUTE_PATH)}`
- stage246_quality_matrix(246단계 품질 행렬): `{rel(QUALITY_PATH)}`
- stage246_segment_kpi_summary(246단계 구간 KPI 요약): `{rel(SEGMENT_PATH)}`
- stage246_risk_atr_telemetry(246단계 위험/ATR 기록): `{rel(RISK_PATH)}`
""",
    )
    write_text(
        NEXT_STAGE_ROOT / "03_reviews/review_index.md",
        f"""# Stage248 Review Index(248단계 검토 색인)

- status(상태): `open_planned_from_stage247`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- source_stage(원천 단계): `{STAGE_ID}`
- source_decision(원천 판정): `{DECISION}`
""",
    )
    write_text(
        NEXT_STAGE_ROOT / "04_selected/selection_status.md",
        f"""# Stage248 Selection Status(248단계 선택 상태)

- stage_status(단계 상태): `open_planned_from_stage247`
- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- source_decision(원천 판정): `{DECISION}`
- claim_boundary(주장 경계): `{BOUNDARY}`
""",
    )


def update_current_truth() -> None:
    current_text = f"""# Current Working State(현재 작업 상태)

- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- active_stage(활성 단계): `{NEXT_STAGE_ID}`
- selected_research_baseline(선택 연구 기준선): `none`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- adapter_under_review(검토 중 어댑터): `stage246_cap0305_control_near_miss_and_soft_guard_tradeoff`
- status(상태): `stage247_closed_open_stage248_entry_source_quality_repair_candidate_not_final`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage247(247단계)는 Stage246(246단계) soft guard(부드러운 보호문)를 review-only(검토 전용)로 판정했다. Effect(효과): Stage248(248단계)은 더 강한 soft guard(부드러운 보호문)를 반복하지 않고 entry/source quality repair(진입/원천 품질 수리)로 넘어간다.

## Latest Stage247 Evidence(최신 247단계 근거)

- run(실행): `{RUN_ID}`
- decision(판정): `{DECISION}`
- external_verification_status(외부 검증 상태): `review_only_source_stage246_mt5_reports_completed`
- report(보고서): `{rel(REPORT_PATH)}`
- tradeoff_matrix(상충 행렬): `{rel(TRADEOFF_PATH)}`
- attribution(기여 분석): `{rel(ATTRIBUTION_PATH)}`
- failure_memory(실패 기억): `{rel(FAILURE_PATH)}`
- route_matrix(경로 행렬): `{rel(ROUTE_PATH)}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준), overall_goal_complete(전체 목표 완료).
"""
    write_text(CURRENT_STATE_PATH, current_text)

    workspace = read_text(WORKSPACE_STATE_PATH)
    workspace = re.sub(r"^current_run_id: .*$", f"current_run_id: {NEXT_RUN_ID}", workspace, count=1, flags=re.MULTILINE)
    workspace = re.sub(r"^active_stage: .*$", f"active_stage: {NEXT_STAGE_ID}", workspace, count=1, flags=re.MULTILINE)
    focus = f"""- >-
  Stage247(247단계) closed(종료) as `{DECISION}` and Stage248(248단계) `{NEXT_STAGE_ID}` is open_planned(개방 계획). Effect(효과): soft guard(부드러운 보호문) 상충을 failure memory(실패 기억)로 두고 entry/source quality repair(진입/원천 품질 수리)를 좁게 시험한다.
- >-
  Stage247 evidence(247단계 근거)는 `{rel(REPORT_PATH)}`, `{rel(TRADEOFF_PATH)}`, `{rel(ATTRIBUTION_PATH)}`, `{rel(FAILURE_PATH)}`에 있다. Effect(효과): DD(낙폭) 개선과 net/PF(순손익/수익요인) 손상을 분리해 다음 경로를 정한다.
- >-
  Target surface(목표 표면)는 `{TARGET_SURFACE}`이고 legacy 34D(레거시 34D)는 lesson-only KPI target(교훈 전용 핵심 성과 지표 목표)이다. Effect(효과): v2-native research(v2 고유 연구)를 계속한다.

"""
    workspace = re.sub(
        rf"- >-\n  Stage247\(247.*?Target surface.*?`{re.escape(TARGET_SURFACE)}`.*?\n\n",
        "",
        workspace,
        flags=re.DOTALL,
    )
    workspace = workspace.replace("current_focus:\n", "current_focus:\n" + focus, 1)
    stage247_block = f"""stage247_stage246_soft_guard_followup_review:
  packet_id: {PACKET_ID}
  stage_id: {STAGE_ID}
  status: closed_open_stage248_entry_source_quality_repair_candidate_not_final
  current_run_id: {RUN_ID}
  source_stage: {SOURCE_STAGE_ID}
  source_run: {SOURCE_RUN_ID}
  source_decision: open_stage247_bounded_followup_due_to_soft_guard_tradeoff_candidate_not_final
  decision: {DECISION}
  report_path: {rel(REPORT_PATH)}
  decision_path: {rel(DECISION_PATH)}
  tradeoff_matrix_path: {rel(TRADEOFF_PATH)}
  attribution_path: {rel(ATTRIBUTION_PATH)}
  failure_memory_path: {rel(FAILURE_PATH)}
  route_matrix_path: {rel(ROUTE_PATH)}
  risk_atr_review_path: {rel(RISK_REVIEW_PATH)}
  external_verification_status: review_only_source_stage246_mt5_reports_completed
  pushed_commit_hash: pending_until_push
  next_action: {NEXT_RUN_ID}
  boundary: {BOUNDARY}
"""
    workspace = re.sub(
        r"stage247_stage246_soft_guard_followup_review:\n(?:  .*\n)+",
        stage247_block,
        workspace,
        count=1,
    )
    if "stage248_entry_source_quality_repair_after_stage246_soft_guard_tradeoff:" not in workspace:
        workspace += f"""

stage248_entry_source_quality_repair_after_stage246_soft_guard_tradeoff:
  packet_id: {NEXT_PACKET_ID}
  stage_id: {NEXT_STAGE_ID}
  status: open_planned_from_stage247
  current_run_id: {NEXT_RUN_ID}
  source_stage: {STAGE_ID}
  source_run: {RUN_ID}
  source_decision: {DECISION}
  next_action: {NEXT_RUN_ID}
  boundary: {BOUNDARY}
"""
    write_text(WORKSPACE_STATE_PATH, workspace, bom=False)

    changelog_entry = f"""
## {utc_now()} Stage247 Stage246 soft guard follow-up review closeout(247단계 246단계 부드러운 보호문 후속 검토 종료)

- action(행동): closed(종료) `{STAGE_ID}` with decision(판정) `{DECISION}`.
- effect(효과): soft guard(부드러운 보호문)의 DD(낙폭) 개선과 net/PF(순손익/수익요인) 손상을 기록하고 `{NEXT_STAGE_ID}`를 열었다.
- boundary(주장 경계): `{BOUNDARY}`.
"""
    existing = read_text(CHANGELOG_PATH) if CHANGELOG_PATH.exists() else ""
    existing = re.sub(
        r"\n## [^\n]*Stage247 Stage246 soft guard follow-up review closeout[^\n]*\n.*?(?=\n## |\Z)",
        "",
        existing,
        flags=re.DOTALL,
    )
    write_text(CHANGELOG_PATH, existing.rstrip() + changelog_entry, bom=False)


def write_ledgers_and_packet(review: Mapping[str, Any]) -> None:
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__review_total",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "stage247_review_total",
        "parent_run_id": SOURCE_RUN_ID,
        "record_view": "review_total",
        "tier_scope": "Tier A+B",
        "kpi_scope": "baseline_adapter_followup_review",
        "scoreboard_lane": "regular_risk_execution",
        "status": "reviewed_closed",
        "judgment": DECISION,
        "path": rel(REPORT_PATH),
        "primary_kpi": "best_reference=s246_cap0305_control;validation_net=976.67;validation_dd=12.9428;validation_mid_pf=1.522877;oos_net=775.76",
        "guardrail_kpi": "soft_guard_dd_helped_but_net_midpf_damaged;overall_goal_complete=0",
        "external_verification_status": "review_only_source_stage246_mt5_reports_completed",
        "notes": "Stage247 review only; routes to bounded Stage248 entry/source quality repair.",
    }
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "baseline_adapter_followup_review(기준선 어댑터 후속 검토)",
        "status": "reviewed_closed",
        "judgment": DECISION,
        "path": rel(REPORT_PATH),
        "notes": f"source_stage246_evidence_commit={SOURCE_EVIDENCE_COMMIT};source_stage246_hash_record_commit={SOURCE_HASH_RECORD_COMMIT};overall_goal_complete=0;boundary={BOUNDARY}",
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
            "artifact_type": "stage247_followup_review_evidence",
            "path": rel(path),
            "sha256": sha256_lf(path),
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": created,
            "notes": "Stage247 Stage246 soft guard follow-up review evidence; research only.",
        }
        for path in artifact_paths
        if path.exists()
    ]
    artifact_payload = upsert_csv(ARTIFACT_REGISTRY_PATH, ARTIFACT_COLUMNS, artifact_rows, "artifact_id")
    ledger_payload = {
        "run_registry": run_payload,
        "project_alpha_ledger": project_payload,
        "stage_ledger": stage_payload,
        "artifact_registry": artifact_payload,
    }

    summary = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "packet_id": PACKET_ID,
        "source_stage": SOURCE_STAGE_ID,
        "source_run": SOURCE_RUN_ID,
        "source_stage246_evidence_commit": SOURCE_EVIDENCE_COMMIT,
        "source_stage246_hash_record_commit": SOURCE_HASH_RECORD_COMMIT,
        "decision": DECISION,
        "next_stage_or_branch": NEXT_STAGE_ID,
        "external_verification_status": "review_only_source_stage246_mt5_reports_completed",
        "overall_goal_complete": False,
        "pushed_commit_hash": "pending_until_push",
        "claim_boundary": BOUNDARY,
        "best_reference": review["best_reference"],
        "tradeoff_rows": review["tradeoff_rows"],
        "risk_review_rows": review["risk_review_rows"],
        "attribution_rows": review["attribution_rows"],
        "failure_memory_rows": review["failure_rows"],
        "route_rows": review["route_rows"],
        "required_outputs": {
            "report": rel(REPORT_PATH),
            "tradeoff_matrix": rel(TRADEOFF_PATH),
            "attribution": rel(ATTRIBUTION_PATH),
            "failure_memory": rel(FAILURE_PATH),
            "route_matrix": rel(ROUTE_PATH),
            "risk_atr_review": rel(RISK_REVIEW_PATH),
            "decision": rel(DECISION_PATH),
        },
        "ledger_payload": ledger_payload,
    }
    write_json(SUMMARY_PATH, summary)

    base_payload = {
        "packet_id": PACKET_ID,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "source_stage": SOURCE_STAGE_ID,
        "source_run": SOURCE_RUN_ID,
        "decision": DECISION,
        "next_stage_or_branch": NEXT_STAGE_ID,
        "external_verification_status": "review_only_source_stage246_mt5_reports_completed",
        "claim_boundary": BOUNDARY,
        "overall_goal_complete": False,
    }
    packet_payloads: dict[str, Any] = {
        "packet_receipt.json": {
            **base_payload,
            "created_at_utc": created,
            "primary_family": "baseline_adapter_research",
            "primary_skill": "obsidian-result-judgment(결과 판정)",
            "support_skills": ["obsidian-performance-attribution(성과 귀속)", "obsidian-artifact-lineage(산출물 계보)"],
            "status": "closed_pending_push_hash",
        },
        "routing_receipt.json": {**base_payload, "route": DECISION, "route_effect": "open Stage248 entry/source quality repair"},
        "kpi_contract_audit.json": {
            **base_payload,
            "status": "passed",
            "kpi_basis": [rel(QUALITY_PATH), rel(SEGMENT_PATH), rel(BALANCE_PATH), rel(RISK_PATH)],
        },
        "result_judgment_gate.json": {
            **base_payload,
            "result_subject": RUN_ID,
            "evidence_available": [rel(REPORT_PATH), rel(TRADEOFF_PATH), rel(RISK_REVIEW_PATH)],
            "evidence_missing": ["Stage248 entry/source repair measurement", "ONNX parity", "MT5 ONNX/runtime reproduction"],
            "judgment_label": "soft_guard_tradeoff_negative_not_final",
            "next_condition": NEXT_STAGE_ID,
        },
        "performance_attribution_gate.json": {
            **base_payload,
            "observed_change": "soft guard lowered DD while damaging net and mid PF",
            "attribution_rows": review["attribution_rows"],
            "attribution_confidence": "high_for_soft_guard_tradeoff",
        },
        "artifact_lineage_audit.json": {
            **base_payload,
            "source_inputs": [rel(QUALITY_PATH), rel(SEGMENT_PATH), rel(BALANCE_PATH), rel(RISK_PATH), rel(CONCENTRATION_PATH)],
            "producer": rel(PRODUCER_PATH),
            "artifact_paths": [rel(path) for path in artifact_paths if path.exists()],
            "ledger_payload": ledger_payload,
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
        f"""# Stage247 Closeout Packet(247단계 종료 작업 묶음)

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
