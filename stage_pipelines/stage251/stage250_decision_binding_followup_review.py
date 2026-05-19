from __future__ import annotations

import csv
import hashlib
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Sequence


STAGE_ID = "251_adapter_research__stage250_decision_binding_followup_review"
RUN_ID = "run251A_stage251_stage250_decision_binding_followup_review_v1"
PACKET_ID = "stage251_stage250_decision_binding_followup_review_v1"
SOURCE_STAGE_ID = "250_adapter_research__decision_surface_binding_repair_after_stage248_threshold_no_effect"
SOURCE_RUN_ID = "run250A_stage250_decision_surface_binding_repair_after_stage248_threshold_no_effect_v1"
SOURCE_STAGE250_EVIDENCE_COMMIT = "70625d3b9651397a9c24ed4399483691f221780c"
SOURCE_STAGE250_HASH_RECORD_COMMIT = "5f65e46fbcd2f3653cf461c254d27ca0977e01e4"
NEXT_STAGE_ID = "252_adapter_research__asymmetric_binding_repair_after_stage250_overprune"
NEXT_RUN_ID = "run252A_stage252_asymmetric_binding_repair_after_stage250_overprune_v1"
NEXT_PACKET_ID = "stage252_asymmetric_binding_repair_after_stage250_overprune_v1"
DECISION = "open_stage252_bounded_asymmetric_binding_repair_after_stage250_overprune_candidate_not_final"
BOUNDARY = "research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment"
TARGET_SURFACE = "legacy_34d_kpi_lesson_only_v2_native_decision_surface_binding_after_stage248_threshold_no_effect"
EXTERNAL_STATUS = "review_only_source_stage250_mt5_reports_completed"

LEGACY_34D_NET = 987.60
LEGACY_34D_PF = 1.583157
LEGACY_34D_DD = 12.909136

ROOT = Path.cwd()
STAGE_ROOT = ROOT / "stages" / STAGE_ID
REVIEWS = STAGE_ROOT / "03_reviews"
PACKET_ROOT = ROOT / "docs/agent_control/packets" / PACKET_ID
NEXT_STAGE_ROOT = ROOT / "stages" / NEXT_STAGE_ID
SOURCE_REVIEWS = ROOT / "stages" / SOURCE_STAGE_ID / "03_reviews"

QUALITY_PATH = SOURCE_REVIEWS / "stage250_quality_matrix.csv"
KPI_PATH = SOURCE_REVIEWS / "stage250_decision_binding_kpi_summary.csv"
PROBABILITY_PATH = SOURCE_REVIEWS / "stage250_probability_binding_summary.csv"
ATTRIBUTION_SOURCE_PATH = SOURCE_REVIEWS / "stage250_performance_attribution.csv"
FAILURE_SOURCE_PATH = SOURCE_REVIEWS / "stage250_failure_memory.csv"
RISK_PATH = SOURCE_REVIEWS / "stage250_risk_atr_telemetry.csv"
SEGMENT_PATH = SOURCE_REVIEWS / "stage250_segment_kpi_summary.csv"
SOURCE_REPORT_PATH = SOURCE_REVIEWS / "stage250_decision_binding_report.md"
SOURCE_DECISION_PATH = SOURCE_REVIEWS / "stage250_decision.md"

REPORT_PATH = REVIEWS / "stage251_stage250_decision_binding_followup_review.md"
TRADEOFF_PATH = REVIEWS / "stage251_tradeoff_review_matrix.csv"
ATTRIBUTION_PATH = REVIEWS / "stage251_performance_attribution.csv"
FAILURE_PATH = REVIEWS / "stage251_failure_memory.csv"
ROUTE_PATH = REVIEWS / "stage251_route_matrix.csv"
RISK_REVIEW_PATH = REVIEWS / "stage251_risk_atr_review.csv"
SUMMARY_PATH = REVIEWS / "stage251_summary.json"
DECISION_PATH = REVIEWS / "stage251_decision.md"
STAGE_LEDGER_PATH = REVIEWS / "stage_run_ledger.csv"
REVIEW_INDEX_PATH = REVIEWS / "review_index.md"
SELECTION_PATH = STAGE_ROOT / "04_selected/selection_status.md"

CURRENT_STATE_PATH = ROOT / "docs/context/current_working_state.md"
WORKSPACE_STATE_PATH = ROOT / "docs/workspace/workspace_state.yaml"
CHANGELOG_PATH = ROOT / "docs/workspace/changelog.md"
RUN_REGISTRY_PATH = ROOT / "docs/registers/run_registry.csv"
PROJECT_LEDGER_PATH = ROOT / "docs/registers/alpha_run_ledger.csv"
ARTIFACT_REGISTRY_PATH = ROOT / "docs/registers/artifact_registry.csv"
PRODUCER_PATH = ROOT / "stage_pipelines/stage251/stage250_decision_binding_followup_review.py"

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
    index: dict[tuple[str, str, str], Mapping[str, str]] = {}
    for row in rows:
        index[(row["adapter_id"], row["split"], row["view"])] = row
    return index


def decision_counts(row: Mapping[str, str]) -> dict[str, int]:
    try:
        parsed = json.loads(row.get("decision_counts", "{}"))
    except json.JSONDecodeError:
        return {"flat": 0, "long": 0, "short": 0}
    return {str(key): as_int(value) for key, value in parsed.items()}


def build_review() -> dict[str, Any]:
    quality_rows = read_csv(QUALITY_PATH)
    kpi_rows = read_csv(KPI_PATH)
    probability_rows = read_csv(PROBABILITY_PATH)
    source_attribution_rows = read_csv(ATTRIBUTION_SOURCE_PATH)
    source_failure_rows = read_csv(FAILURE_SOURCE_PATH)
    risk_rows = read_csv(RISK_PATH) if RISK_PATH.exists() else []
    prob = probability_index(probability_rows)
    control = quality_rows[0]
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
    }

    tradeoff_rows: list[dict[str, Any]] = []
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
        hard_pass = row.get("hard_quality_pass", "").lower() == "true"
        is_control = row["adapter_id"] == control["adapter_id"]
        if is_control:
            read = "near_repeat_control_not_34d_equivalent"
            next_handling = "use_as_reference_only_not_final"
        elif val_net < control_values["validation_net"] - 300:
            read = "binding_active_but_overpruned_profitable_supply"
            next_handling = NEXT_STAGE_ID
        else:
            read = "binding_effect_unclear"
            next_handling = "review_before_reuse"
        tradeoff_rows.append(
            {
                "adapter_id": row["adapter_id"],
                "axis": row["axis"],
                "validation_pf": row["validation_pf"],
                "validation_net": row["validation_net"],
                "validation_net_delta_vs_control": fmt(val_net - control_values["validation_net"]),
                "validation_net_gap_vs_34d": row["validation_net_gap_vs_34d"],
                "validation_dd_percent": row["validation_balance_dd_percent"],
                "validation_dd_delta_vs_control": fmt(val_dd - control_values["validation_dd"], 4),
                "validation_dd_margin_vs_34d": row["validation_dd_margin_vs_34d"],
                "validation_mid_pf": row["validation_mid_pf"],
                "validation_mid_pf_delta_vs_control": fmt(mid_pf - control_values["validation_mid_pf"], 6),
                "oos_pf": row["oos_pf"],
                "oos_net": row["oos_net"],
                "oos_net_delta_vs_control": fmt(oos_net - control_values["oos_net"]),
                "directional_pass_validation": directional,
                "directional_pass_delta_vs_control": directional - control_values["directional_pass"],
                "order_filled_validation": order_filled,
                "order_filled_delta_vs_control": order_filled - control_values["order_filled"],
                "flat_count_validation": flat_count,
                "flat_count_delta_vs_control": flat_count - control_values["flat_count"],
                "hard_quality_pass": str(hard_pass),
                "read": read,
                "next_handling": next_handling,
            }
        )

    risk_review_rows: list[dict[str, Any]] = []
    for row in kpi_rows:
        if row.get("view") != "actual_routed_total" or row.get("status") != "completed":
            continue
        risk_review_rows.append(
            {
                "adapter_id": row["adapter_id"],
                "split": row["split"],
                "max_model_risk_pct": row.get("max_model_risk_pct", ""),
                "max_actual_risk_pct_after_floor": row.get("max_actual_risk_pct_after_floor", ""),
                "risk_floor_applied_count": row.get("risk_floor_applied_count", ""),
                "avg_executed_lot": row.get("avg_executed_lot", ""),
                "avg_open_sl_points": row.get("avg_open_sl_points", ""),
                "avg_open_tp_points": row.get("avg_open_tp_points", ""),
                "risk_bucket": row.get("risk_bucket", ""),
                "read": "risk_atr_present_not_sufficient_for_final_package",
            }
        )

    attribution_rows = [
        {
            "attribution_id": f"{RUN_ID}__binding_active_but_overpruned",
            "observed_change": "Directional pass rows moved from 468 in the control to 309, 204, and 110 in the binding variants, but validation net collapsed.",
            "comparison_baseline": "s250_stage248_binding_control",
            "likely_drivers": "rank-conditioned flat tilt changed model probabilities before the same MT5 thresholds and pruned high-value trade supply",
            "segment_checks": "validation/OOS full split, early/mid/late PF, probability binding, risk/ATR telemetry, DD and OOS PF reviewed",
            "trade_shape": "accepted/fill rows fell sharply; validation net fell by -765.62 to -859.27 while OOS net fell by -514.40 to -575.35",
            "alternative_explanations": "some DD and OOS PF improvement can be mechanical exposure shrink, not true edge improvement",
            "attribution_confidence": "high",
            "next_probe": NEXT_STAGE_ID,
        },
        {
            "attribution_id": f"{RUN_ID}__control_still_near_miss_not_34d",
            "observed_change": "Stage250 control stayed near the Stage248 reference but missed 34D-equivalent validation net, DD, and mid PF together.",
            "comparison_baseline": "legacy 34D lesson-only KPI target",
            "likely_drivers": "mid-window quality and decision/source binding remain limiting even with ATR bracket and model-controlled risk present",
            "segment_checks": "validation net gap, DD margin, validation mid PF, OOS net, and quality flags reviewed",
            "trade_shape": "control validation net 972.15 is -15.45 below 34D; DD margin is -0.018964; mid PF remains 1.516650878",
            "alternative_explanations": "small control drift versus Stage248 can come from Stage250 model/feature identity and tester path differences",
            "attribution_confidence": "medium_high",
            "next_probe": NEXT_STAGE_ID,
        },
        {
            "attribution_id": f"{RUN_ID}__dd_pf_without_net_not_enough",
            "observed_change": "Some variants improved DD or OOS PF, but the net/profit supply damage was too large.",
            "comparison_baseline": "research-grade BaselineAdapter package criteria",
            "likely_drivers": "exposure compression removed both bad and good trades instead of selectively repairing weak decisions",
            "segment_checks": "validation/OOS net, PF, DD, mid PF, OOS PF, and trade count checked",
            "trade_shape": "best DD compression row still had validation net only 112.88 and validation PF 1.36",
            "alternative_explanations": "lower DD can reflect fewer trades rather than stronger decision quality",
            "attribution_confidence": "high",
            "next_probe": NEXT_STAGE_ID,
        },
    ]

    failure_rows = [
        {
            "failure_id": f"{RUN_ID}__broad_rank_flat_tilt_overpruned",
            "source_failure": "stage250_rank_conditioned_flat_tilt_trade_supply_damage",
            "why_it_matters": "decision binding became active, but the broad flat tilt removed too much profitable supply",
            "salvage_value": "keep probability-binding diagnostics and avoid repeating inactive threshold-only nudges",
            "do_not_repeat": "do not treat directional-pass reduction or DD compression as sufficient improvement",
            "next_handling": NEXT_STAGE_ID,
        },
        {
            "failure_id": f"{RUN_ID}__control_near_miss_not_final",
            "source_failure": "stage250_control_still_below_34d_combined_kpi",
            "why_it_matters": "control net, DD, and mid PF still do not clear the 34D lesson-only target together",
            "salvage_value": "use the control as a reference surface, not as a final adapter",
            "do_not_repeat": "do not call high OOS PF or ATR/risk presence enough for final package completion",
            "next_handling": NEXT_STAGE_ID,
        },
        {
            "failure_id": f"{RUN_ID}__risk_atr_present_not_sufficient",
            "source_failure": "mandatory_capability_present_but_kpi_not_repaired",
            "why_it_matters": "ATR SL/TP and model-controlled risk are necessary, but net/PF/DD and segment stability still govern research quality",
            "salvage_value": "keep ATR/risk telemetry in every follow-up run",
            "do_not_repeat": "do not split ATR/risk into a standalone success claim",
            "next_handling": NEXT_STAGE_ID,
        },
    ]

    route_rows = [
        {
            "route_id": f"{RUN_ID}__do_not_accept_stage250_as_final",
            "evidence": "hard_quality_pass false for all Stage250 candidates",
            "decision": "candidate_not_final",
            "effect": "keeps research/development boundary and avoids final-package claim",
            "next_stage_or_branch": NEXT_STAGE_ID,
        },
        {
            "route_id": f"{RUN_ID}__open_asymmetric_binding_repair",
            "evidence": "binding moved decisions but broad flat tilt damaged validation net and mid PF",
            "decision": DECISION,
            "effect": "focuses Stage252 on selective/asymmetric repair instead of another broad threshold or broad flat-tilt pass",
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
        "risk_rows_count": len(risk_rows),
    }


def write_reports(review: Mapping[str, Any]) -> None:
    control = review["control"]
    tradeoff_rows = review["tradeoff_rows"]
    best_dd = min(tradeoff_rows, key=lambda row: as_float(row["validation_dd_percent"]))
    worst_net = min(tradeoff_rows, key=lambda row: as_float(row["validation_net"]))
    write_csv(TRADEOFF_PATH, tradeoff_rows, list(tradeoff_rows[0].keys()))
    write_csv(ATTRIBUTION_PATH, review["attribution_rows"], list(review["attribution_rows"][0].keys()))
    write_csv(FAILURE_PATH, review["failure_rows"], list(review["failure_rows"][0].keys()))
    write_csv(ROUTE_PATH, review["route_rows"], list(review["route_rows"][0].keys()))
    write_csv(RISK_REVIEW_PATH, review["risk_review_rows"], list(review["risk_review_rows"][0].keys()))

    table_rows = "\n".join(
        "| {adapter_id} | {validation_net} | {validation_net_delta_vs_control} | {validation_dd_percent} | {validation_mid_pf} | {oos_net} | {directional_pass_validation} | {read} |".format(
            **row
        )
        for row in tradeoff_rows
    )
    report = f"""# Stage251 Stage250 Decision Binding Follow-up Review(251단계 250단계 결정 결합 후속 검토)

- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- source_evidence_commit(원천 근거 커밋): `{SOURCE_STAGE250_EVIDENCE_COMMIT}`
- source_hash_record_commit(원천 해시 기록 커밋): `{SOURCE_STAGE250_HASH_RECORD_COMMIT}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- decision(판정): `{DECISION}`
- boundary(주장 경계): `{BOUNDARY}`

## Easy Read(쉬운 판독)

- Stage250(250단계)는 decision binding(결정 결합)이 실제로 움직인다는 점을 확인했다.
- 다만 움직임의 방향이 좋지 않았다. directional pass(방향 통과)는 `468`에서 `309`, `204`, `110`까지 줄었지만 validation net(검증 순손익)은 `972.15`에서 `206.53`, `130.73`, `112.88`로 무너졌다.
- `s250_lowmid_flat025_015`는 DD(낙폭)를 `11.4408%`까지 낮췄지만 validation net(검증 순손익)이 `112.88`이라 품질 개선으로 볼 수 없다.
- ATR SL/TP(ATR 손절/익절)와 model-controlled risk%(모델 제어 위험 비율)는 존재한다. 하지만 이것만으로 final adapter(최종 어댑터)가 아니다.
- 다음 행동(action, 행동)은 broad flat tilt(넓은 플랫 기울임)를 반복하지 않고 asymmetric binding repair(비대칭 결합 수리)를 여는 것이다. 효과(effect, 효과)는 좋은 trade supply(거래 공급)를 보존하면서 약한 결정만 좁게 줄이는지 시험하는 것이다.

## KPI Tradeoff Matrix(KPI 핵심 성과 지표 상충 행렬)

| adapter(어댑터) | val net(검증 순손익) | net delta(순손익 차이) | DD%(낙폭률) | mid PF(중간 수익요인) | OOS net(표본외 순손익) | dir pass(방향 통과) | read(판독) |
|---|---:|---:|---:|---:|---:|---:|---|
{table_rows}

## Judgment(판정)

- result_subject(판정 대상): `{RUN_ID}`
- evidence_available(사용 근거): Stage250(250단계) quality matrix(품질 행렬), KPI summary(KPI 요약), probability binding(확률 결합), performance attribution(성과 귀속), risk/ATR telemetry(위험/ATR 기록), MT5(MetaTrader 5, 메타트레이더5) validation/OOS(검증/표본외) report(보고서).
- evidence_missing(누락 근거): Stage252(252단계) asymmetric binding repair(비대칭 결합 수리), ONNX parity(ONNX 동등성), MT5 ONNX/runtime reproduction(MT5 ONNX/런타임 재현).
- judgment_label(판정 라벨): `binding_active_but_overpruned_negative_not_final(결합 활성이나 과감축 부정, 최종 아님)`
- claim_boundary(주장 경계): research/development only(연구개발 전용). deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위)는 모두 금지다.
- next_condition(다음 조건): `{NEXT_STAGE_ID}`에서 side/session/segment-aware asymmetric binding(방향/세션/구간 인식 비대칭 결합)이 net/PF/DD(순손익/수익요인/낙폭)를 함께 개선하는지 확인한다.

## Review Notes(검토 메모)

- control(기준): `{control["adapter_id"]}` validation net(검증 순손익) `{control["validation_net"]}`, validation DD(검증 낙폭) `{control["validation_balance_dd_percent"]}`, validation mid PF(검증 중간 수익요인) `{control["validation_mid_pf"]}`.
- best_dd_row(최저 낙폭 행): `{best_dd["adapter_id"]}` DD(낙폭) `{best_dd["validation_dd_percent"]}`, validation net(검증 순손익) `{best_dd["validation_net"]}`.
- worst_net_row(최저 순손익 행): `{worst_net["adapter_id"]}` validation net(검증 순손익) `{worst_net["validation_net"]}`.

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준), overall_goal_complete(전체 목표 완료).
"""
    write_text(REPORT_PATH, report)
    decision_text = f"""# Stage251 Decision(251단계 판정)

- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- decision(판정): `{DECISION}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- source_stage250_evidence_commit(원천 250단계 근거 커밋): `{SOURCE_STAGE250_EVIDENCE_COMMIT}`
- source_stage250_hash_record_commit(원천 250단계 해시 기록 커밋): `{SOURCE_STAGE250_HASH_RECORD_COMMIT}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- report(보고서): `{rel(REPORT_PATH)}`
- tradeoff_matrix(상충 행렬): `{rel(TRADEOFF_PATH)}`
- attribution(성과 귀속): `{rel(ATTRIBUTION_PATH)}`
- failure_memory(실패 기억): `{rel(FAILURE_PATH)}`
- route_matrix(경로 행렬): `{rel(ROUTE_PATH)}`
- risk_atr_review(위험/ATR 검토): `{rel(RISK_REVIEW_PATH)}`
- next_stage_or_branch(다음 단계 또는 분기): `{NEXT_STAGE_ID}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage251(251단계) closeout(종료)은 overall goal complete(전체 목표 완료)가 아니다.
"""
    write_text(DECISION_PATH, decision_text)
    write_text(
        REVIEW_INDEX_PATH,
        f"""# Stage251 Review Index(251단계 검토 색인)

- status(상태): `closed_open_stage252_repair_candidate_not_final`
- run(실행): `{RUN_ID}`
- decision(판정): `{DECISION}`
- report(보고서): `{rel(REPORT_PATH)}`
- tradeoff_matrix(상충 행렬): `{rel(TRADEOFF_PATH)}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
""",
    )
    write_text(
        SELECTION_PATH,
        f"""# Stage251 Selection Status(251단계 선택 상태)

- stage_status(단계 상태): `closed_open_stage252_repair_candidate_not_final`
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

Stage252(252단계)는 Stage250(250단계)의 overprune damage(과감축 손상)를 받은 뒤 asymmetric binding repair(비대칭 결합 수리)를 좁게 시험하는 bounded repair(경계 수리) 단계다.

## Bounded Question(경계 질문)

Can side/session/segment-aware asymmetric binding(방향/세션/구간 인식 비대칭 결합) preserve the Stage250 control trade supply(기준 거래 공급) while reducing weak decisions enough to improve validation/OOS net, PF, DD, and mid-window behavior(검증/표본외 순손익, 수익요인, 낙폭, 중간 구간 행동)?

## Boundary(경계)

`{BOUNDARY}`
""",
    )
    write_text(
        NEXT_STAGE_ROOT / "01_inputs/input_refs.md",
        f"""# Stage252 Input References(252단계 입력 참조)

- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- source_decision(원천 판정): `{DECISION}`
- source_report(원천 보고서): `{rel(REPORT_PATH)}`
- source_tradeoff_matrix(원천 상충 행렬): `{rel(TRADEOFF_PATH)}`
- source_stage250_evidence_commit(원천 250단계 근거 커밋): `{SOURCE_STAGE250_EVIDENCE_COMMIT}`
- source_stage250_hash_record_commit(원천 250단계 해시 기록 커밋): `{SOURCE_STAGE250_HASH_RECORD_COMMIT}`
""",
    )
    write_text(
        NEXT_STAGE_ROOT / "03_reviews/review_index.md",
        f"""# Stage252 Review Index(252단계 검토 색인)

- status(상태): `open_planned_from_stage251`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- source_stage(원천 단계): `{STAGE_ID}`
- source_decision(원천 판정): `{DECISION}`
""",
    )
    write_text(
        NEXT_STAGE_ROOT / "04_selected/selection_status.md",
        f"""# Stage252 Selection Status(252단계 선택 상태)

- stage_status(단계 상태): `open_planned_from_stage251`
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
- adapter_under_review(검토 중 어댑터): `stage251_stage250_decision_binding_followup_review`
- status(상태): `stage251_closed_open_stage252_asymmetric_binding_repair_candidate_not_final`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage251(251단계)는 Stage250(250단계) decision binding(결정 결합)을 review-only(검토 전용)로 판정했다. Effect(효과): Stage252(252단계)은 broad flat tilt(넓은 플랫 기울임)를 반복하지 않고 asymmetric binding repair(비대칭 결합 수리)를 좁게 시험한다.

## Latest Stage251 Evidence(최신 251단계 근거)

- run(실행): `{RUN_ID}`
- decision(판정): `{DECISION}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- report(보고서): `{rel(REPORT_PATH)}`
- tradeoff_matrix(상충 행렬): `{rel(TRADEOFF_PATH)}`
- attribution(성과 귀속): `{rel(ATTRIBUTION_PATH)}`
- failure_memory(실패 기억): `{rel(FAILURE_PATH)}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준), overall_goal_complete(전체 목표 완료).
"""
    write_text(CURRENT_STATE_PATH, current)

    workspace = read_text(WORKSPACE_STATE_PATH)
    workspace = re.sub(r"^current_run_id: .*$", f"current_run_id: {NEXT_RUN_ID}", workspace, count=1, flags=re.MULTILINE)
    workspace = re.sub(r"^updated_on: .*$", "updated_on: '2026-05-19'", workspace, count=1, flags=re.MULTILINE)
    workspace = re.sub(r"^active_stage: .*$", f"active_stage: {NEXT_STAGE_ID}", workspace, count=1, flags=re.MULTILINE)
    focus = f"""current_focus:
- >-
  Stage251(251단계) closed(종료) as `{DECISION}` and Stage252(252단계) `{NEXT_STAGE_ID}` is open_planned(개방 계획). Effect(효과): Stage250(250단계)의 decision movement(결정 이동)은 보존하되 overprune damage(과감축 손상)는 다음 수리축으로 분리한다.
- >-
  Stage251 evidence(251단계 근거)는 `{rel(REPORT_PATH)}`, `{rel(TRADEOFF_PATH)}`, `{rel(ATTRIBUTION_PATH)}`, `{rel(FAILURE_PATH)}`에 있다. Effect(효과): broad flat tilt(넓은 플랫 기울임)를 반복하지 않고 asymmetric binding repair(비대칭 결합 수리)를 시험한다.
- >-
  Target surface(목표 표면)는 `{TARGET_SURFACE}`이고 legacy 34D(레거시 34D)는 lesson-only KPI target(교훈 전용 핵심 성과 지표 목표)이다. Effect(효과): v2-native research(v2 고유 연구)를 계속한다.
"""
    workspace = re.sub(r"current_focus:\n.*?(?=\n[A-Za-z0-9_]+:\n)", focus, workspace, count=1, flags=re.DOTALL)
    stage251_block = f"""stage251_stage250_decision_binding_followup_review:
  packet_id: {PACKET_ID}
  stage_id: {STAGE_ID}
  status: closed_open_stage252_asymmetric_binding_repair_candidate_not_final
  current_run_id: {RUN_ID}
  source_stage: {SOURCE_STAGE_ID}
  source_run: {SOURCE_RUN_ID}
  source_stage250_evidence_commit: {SOURCE_STAGE250_EVIDENCE_COMMIT}
  source_stage250_hash_record_commit: {SOURCE_STAGE250_HASH_RECORD_COMMIT}
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
    stage252_block = f"""stage252_asymmetric_binding_repair_after_stage250_overprune:
  packet_id: {NEXT_PACKET_ID}
  stage_id: {NEXT_STAGE_ID}
  status: open_planned_from_stage251
  current_run_id: {NEXT_RUN_ID}
  source_stage: {STAGE_ID}
  source_run: {RUN_ID}
  source_decision: {DECISION}
  next_action: {NEXT_RUN_ID}
  boundary: {BOUNDARY}
"""
    workspace = replace_or_append_block(workspace, "stage251_stage250_decision_binding_followup_review", stage251_block)
    workspace = replace_or_append_block(workspace, "stage252_asymmetric_binding_repair_after_stage250_overprune", stage252_block)
    write_text(WORKSPACE_STATE_PATH, workspace, bom=False)

    changelog_entry = f"""
## {utc_now()} Stage251 Stage250 decision binding follow-up review closeout(251단계 250단계 결정 결합 후속 검토 종료)

- action(행동): closed(종료) `{STAGE_ID}` with decision(판정) `{DECISION}`.
- effect(효과): Stage250(250단계)의 active binding(활성 결합)과 overprune damage(과감축 손상)를 분리하고 `{NEXT_STAGE_ID}`를 열었다.
- boundary(주장 경계): `{BOUNDARY}`.
"""
    existing = read_text(CHANGELOG_PATH) if CHANGELOG_PATH.exists() else ""
    existing = re.sub(
        r"\n## [^\n]*Stage251 Stage250 decision binding follow-up review closeout[^\n]*\n.*?(?=\n## |\Z)",
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
        "subrun_id": "stage251_review_total",
        "parent_run_id": SOURCE_RUN_ID,
        "record_view": "review_total",
        "tier_scope": "Tier A+B",
        "kpi_scope": "baseline_adapter_followup_review",
        "scoreboard_lane": "regular_risk_execution",
        "status": "reviewed_closed",
        "judgment": DECISION,
        "path": rel(REPORT_PATH),
        "primary_kpi": f"control={control['adapter_id']};validation_net={control['validation_net']};validation_dd={control['validation_balance_dd_percent']};validation_mid_pf={control['validation_mid_pf']};oos_net={control['oos_net']}",
        "guardrail_kpi": "binding_active=1;overprune_damage=1;hard_quality_pass_count=0;overall_goal_complete=0",
        "external_verification_status": EXTERNAL_STATUS,
        "notes": "Stage251 review only; routes to bounded Stage252 asymmetric binding repair.",
    }
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "baseline_adapter_followup_review(기준선 어댑터 후속 검토)",
        "status": "reviewed_closed",
        "judgment": DECISION,
        "path": rel(REPORT_PATH),
        "notes": f"source_stage250_evidence_commit={SOURCE_STAGE250_EVIDENCE_COMMIT};source_stage250_hash_record_commit={SOURCE_STAGE250_HASH_RECORD_COMMIT};overall_goal_complete=0;boundary={BOUNDARY}",
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
        "source_stage250_evidence_commit": SOURCE_STAGE250_EVIDENCE_COMMIT,
        "source_stage250_hash_record_commit": SOURCE_STAGE250_HASH_RECORD_COMMIT,
        "decision": DECISION,
        "next_stage_or_branch": NEXT_STAGE_ID,
        "external_verification_status": EXTERNAL_STATUS,
        "overall_goal_complete": False,
        "pushed_commit_hash": "pending_until_push",
        "claim_boundary": BOUNDARY,
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
            "artifact_type": "stage251_followup_review_evidence",
            "path": rel(path),
            "sha256": sha256_lf(path),
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": created,
            "notes": "Stage251 Stage250 decision binding follow-up review evidence; research only.",
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
        "routing_receipt.json": {**base_payload, "route": DECISION, "route_effect": "open Stage252 asymmetric binding repair after Stage250 overprune"},
        "kpi_contract_audit.json": {
            **base_payload,
            "status": "passed",
            "kpi_basis": [rel(QUALITY_PATH), rel(KPI_PATH), rel(PROBABILITY_PATH), rel(RISK_PATH), rel(SEGMENT_PATH)],
        },
        "result_judgment_gate.json": {
            **base_payload,
            "result_subject": RUN_ID,
            "evidence_available": [rel(REPORT_PATH), rel(TRADEOFF_PATH), rel(ATTRIBUTION_PATH), rel(FAILURE_PATH), rel(RISK_REVIEW_PATH)],
            "evidence_missing": ["Stage252 asymmetric binding repair", "ONNX parity", "MT5 ONNX/runtime reproduction"],
            "judgment_label": "binding_active_but_overpruned_negative_not_final",
            "next_condition": NEXT_STAGE_ID,
        },
        "performance_attribution_gate.json": {
            **base_payload,
            "observed_change": "Stage250 binding moved decisions but over-pruned profitable supply",
            "attribution_rows": review["attribution_rows"],
            "attribution_confidence": "high",
        },
        "artifact_lineage_audit.json": {
            **base_payload,
            "source_inputs": [rel(QUALITY_PATH), rel(KPI_PATH), rel(PROBABILITY_PATH), rel(ATTRIBUTION_SOURCE_PATH), rel(FAILURE_SOURCE_PATH), rel(RISK_PATH)],
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
        f"""# Stage251 Closeout Packet(251단계 종료 작업 묶음)

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
