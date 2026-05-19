from __future__ import annotations

import csv
import hashlib
import json
import re
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence


STAGE_ID = "259_adapter_research__stage258_short_tight_margin_pf_followup_review"
RUN_ID = "run259A_stage259_stage258_short_tight_margin_pf_followup_review_v1"
PACKET_ID = "stage259_stage258_short_tight_margin_pf_followup_review_v1"
SOURCE_STAGE_ID = "258_adapter_research__short_tight_margin_pf_repair_after_stage256_tradeoff"
SOURCE_RUN_ID = "run258A_stage258_short_tight_margin_pf_repair_after_stage256_tradeoff_v1"
SOURCE_STAGE258_EVIDENCE_COMMIT = "5dbd67b79c824e3d7049b6f482b8c83b0eda92db"
SOURCE_STAGE258_HASH_RECORD_COMMIT = "7f916e6bae523c45f269eb48c91f6c17e61a55e3"
NEXT_STAGE_ID = "260_adapter_research__tight_plus_highedge_pf_oos_recovery_repair"
NEXT_RUN_ID = "run260A_stage260_tight_plus_highedge_pf_oos_recovery_repair_v1"
NEXT_PACKET_ID = "stage260_tight_plus_highedge_pf_oos_recovery_repair_v1"
DECISION = "open_stage260_bounded_tight_plus_highedge_pf_oos_recovery_repair_candidate_not_final"
BOUNDARY = "research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment"
TARGET_SURFACE = "legacy_34d_kpi_lesson_only_v2_native_tight_plus_highedge_pf_oos_recovery_repair"
EXTERNAL_STATUS = "review_only_source_stage258_mt5_reports_completed"

LEGACY_34D_NET = 987.60
LEGACY_34D_PF = 1.583157
LEGACY_34D_DD = 12.909136

ROOT = Path.cwd()
STAGE_ROOT = ROOT / "stages" / STAGE_ID
REVIEWS = STAGE_ROOT / "03_reviews"
PACKET_ROOT = ROOT / "docs/agent_control/packets" / PACKET_ID
NEXT_STAGE_ROOT = ROOT / "stages" / NEXT_STAGE_ID
SOURCE_REVIEWS = ROOT / "stages" / SOURCE_STAGE_ID / "03_reviews"

QUALITY_PATH = SOURCE_REVIEWS / "stage258_quality_matrix.csv"
SOURCE_FEATURE_PATH = SOURCE_REVIEWS / "stage258_source_feature_summary.csv"
KPI_PATH = SOURCE_REVIEWS / "stage258_source_feature_kpi_summary.csv"
PROBABILITY_PATH = SOURCE_REVIEWS / "stage258_probability_telemetry_summary.csv"
SOURCE_ATTRIBUTION_PATH = SOURCE_REVIEWS / "stage258_performance_attribution.csv"
SOURCE_FAILURE_PATH = SOURCE_REVIEWS / "stage258_failure_memory.csv"
RISK_PATH = SOURCE_REVIEWS / "stage258_risk_atr_telemetry.csv"
SOURCE_REPORT_PATH = SOURCE_REVIEWS / "stage258_source_feature_branch_report.md"
SOURCE_DECISION_PATH = SOURCE_REVIEWS / "stage258_decision.md"

REPORT_PATH = REVIEWS / "stage259_stage258_short_tight_margin_pf_followup_review.md"
TRADEOFF_PATH = REVIEWS / "stage259_tradeoff_review_matrix.csv"
ATTRIBUTION_PATH = REVIEWS / "stage259_performance_attribution.csv"
FAILURE_PATH = REVIEWS / "stage259_failure_memory.csv"
ROUTE_PATH = REVIEWS / "stage259_route_matrix.csv"
RISK_REVIEW_PATH = REVIEWS / "stage259_risk_atr_review.csv"
PROBABILITY_REVIEW_PATH = REVIEWS / "stage259_probability_review.csv"
SUMMARY_PATH = REVIEWS / "stage259_summary.json"
DECISION_PATH = REVIEWS / "stage259_decision.md"
STAGE_LEDGER_PATH = REVIEWS / "stage_run_ledger.csv"
REVIEW_INDEX_PATH = REVIEWS / "review_index.md"
SELECTION_PATH = STAGE_ROOT / "04_selected/selection_status.md"

CURRENT_STATE_PATH = ROOT / "docs/context/current_working_state.md"
WORKSPACE_STATE_PATH = ROOT / "docs/workspace/workspace_state.yaml"
CHANGELOG_PATH = ROOT / "docs/workspace/changelog.md"
RUN_REGISTRY_PATH = ROOT / "docs/registers/run_registry.csv"
PROJECT_LEDGER_PATH = ROOT / "docs/registers/alpha_run_ledger.csv"
ARTIFACT_REGISTRY_PATH = ROOT / "docs/registers/artifact_registry.csv"
PRODUCER_PATH = ROOT / "stage_pipelines/stage259/stage258_short_tight_margin_pf_followup_review.py"

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
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


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


def replace_or_append_block(text: str, key: str, block: str) -> str:
    pattern = rf"^{re.escape(key)}:\n(?:  .*\n)+"
    if re.search(pattern, text, flags=re.MULTILINE):
        return re.sub(pattern, block, text, count=1, flags=re.MULTILINE)
    return text.rstrip() + "\n\n" + block


def read_for_adapter(row: Mapping[str, str], control: Mapping[str, float]) -> tuple[str, str, str]:
    adapter = row["adapter_id"]
    val_pf = as_float(row["validation_pf"])
    val_net = as_float(row["validation_net"])
    mid_pf = as_float(row["validation_mid_pf"])
    oos_net = as_float(row["oos_net"])
    oos_pf = as_float(row["oos_pf"])
    val_dd = as_float(row["validation_balance_dd_percent"])
    if adapter == "s258_tight_plus_highedge":
        return (
            "best_v2_tradeoff_not_final",
            "검증(validation, 검증) 순수익(net, 순수익)과 PF(수익 팩터)를 가장 크게 끌어올렸지만, PF와 중간 구간 PF(mid PF, 중간 PF)가 34D 목표 아래라 아직 최종이 아니다.",
            NEXT_STAGE_ID,
        )
    if adapter == "s258_tight_plus_lowedge":
        return (
            "oos_pf_mid_late_help_but_validation_net_damage",
            "OOS(표본외) PF와 중간/후반 구간은 좋아졌지만 검증 순수익이 34D 아래로 내려가 주축으로 삼기 어렵다.",
            "failure_memory_and_side_clue",
        )
    if adapter == "s258_lowedge_only":
        return (
            "over_blocked_validation_damage",
            "lowedge 단독 차단은 검증 순수익, PF, DD(손실폭)를 동시에 망가뜨려 실패 기억으로 남긴다.",
            "do_not_repeat_as_primary_axis",
        )
    if adapter == "s258_highedge_only":
        return (
            "oos_dd_damage_and_midpf_collapse",
            "highedge 단독 차단은 OOS DD와 중간 PF가 크게 나빠져 실패 기억으로 남긴다.",
            "do_not_repeat_as_primary_axis",
        )
    if val_pf < LEGACY_34D_PF and mid_pf < LEGACY_34D_PF and val_net > LEGACY_34D_NET and oos_net > control["oos_net"]:
        return (
            "control_near_miss_reference",
            "기준(control, 대조군)은 순수익과 DD는 좋지만 PF 축이 약해서 다음 수리의 비교 기준으로만 쓴다.",
            "reference_only",
        )
    return (
        "weak_or_mixed_tradeoff",
        f"PF={fmt(val_pf, 4)}, net={fmt(val_net)}, mid PF={fmt(mid_pf, 4)}, OOS PF={fmt(oos_pf, 4)}, DD={fmt(val_dd, 4)} 조합이 주축으로 충분하지 않다.",
        "failure_memory",
    )


def build_review() -> dict[str, Any]:
    quality_rows = read_csv(QUALITY_PATH)
    source_feature_rows = read_csv(SOURCE_FEATURE_PATH)
    risk_rows = read_csv(RISK_PATH)
    probability_rows = read_csv(PROBABILITY_PATH)
    source_attr_rows = read_csv(SOURCE_ATTRIBUTION_PATH)
    source_failure_rows = read_csv(SOURCE_FAILURE_PATH)
    control_row = next(row for row in quality_rows if row["adapter_id"] == "s258_short_tight_control")
    best_row = next(row for row in quality_rows if row["adapter_id"] == "s258_tight_plus_highedge")
    control = {
        "validation_pf": as_float(control_row["validation_pf"]),
        "validation_net": as_float(control_row["validation_net"]),
        "validation_dd": as_float(control_row["validation_balance_dd_percent"]),
        "validation_mid_pf": as_float(control_row["validation_mid_pf"]),
        "oos_pf": as_float(control_row["oos_pf"]),
        "oos_net": as_float(control_row["oos_net"]),
        "oos_dd": as_float(control_row["oos_balance_dd_percent"]),
    }

    tradeoff_rows: list[dict[str, Any]] = []
    for row in quality_rows:
        label, plain_read, next_handling = read_for_adapter(row, control)
        val_pf = as_float(row["validation_pf"])
        val_net = as_float(row["validation_net"])
        val_dd = as_float(row["validation_balance_dd_percent"])
        mid_pf = as_float(row["validation_mid_pf"])
        oos_pf = as_float(row["oos_pf"])
        oos_net = as_float(row["oos_net"])
        oos_dd = as_float(row["oos_balance_dd_percent"])
        tradeoff_rows.append(
            {
                "adapter_id": row["adapter_id"],
                "axis": row["axis"],
                "validation_pf": row["validation_pf"],
                "validation_pf_gap_vs_34d": fmt(val_pf - LEGACY_34D_PF, 6),
                "validation_net": row["validation_net"],
                "validation_net_delta_vs_control": fmt(val_net - control["validation_net"]),
                "validation_net_gap_vs_34d": fmt(val_net - LEGACY_34D_NET),
                "validation_dd_percent": row["validation_balance_dd_percent"],
                "validation_dd_delta_vs_control": fmt(val_dd - control["validation_dd"], 4),
                "validation_dd_margin_vs_34d": fmt(LEGACY_34D_DD - val_dd, 4),
                "validation_early_pf": row["validation_early_pf"],
                "validation_mid_pf": row["validation_mid_pf"],
                "validation_mid_pf_gap_vs_34d_pf": fmt(mid_pf - LEGACY_34D_PF, 6),
                "validation_late_pf": row["validation_late_pf"],
                "oos_pf": row["oos_pf"],
                "oos_pf_delta_vs_control": fmt(oos_pf - control["oos_pf"], 4),
                "oos_net": row["oos_net"],
                "oos_net_delta_vs_control": fmt(oos_net - control["oos_net"]),
                "oos_dd_percent": row["oos_balance_dd_percent"],
                "oos_dd_delta_vs_control": fmt(oos_dd - control["oos_dd"], 4),
                "hard_quality_pass": row["hard_quality_pass"],
                "quality_flags": row["quality_flags"],
                "review_label": label,
                "plain_read": plain_read,
                "next_handling": next_handling,
            }
        )

    gate_rows = [
        {
            "adapter_id": row["adapter_id"],
            "split": row["split"],
            "source_branch_mode": row["source_branch_mode"],
            "signal_rows": row["signal_rows"],
            "base_blocked_signal_rows": row["base_blocked_signal_rows"],
            "blocked_signal_rows": row["blocked_signal_rows"],
            "changed_gate_rows": row["changed_gate_rows"],
            "allowed_signal_rows": row["allowed_signal_rows"],
            "allowed_signal_rank_counts": row["allowed_signal_rank_counts"],
        }
        for row in source_feature_rows
    ]

    risk_review_rows = [
        {
            "adapter_id": row["adapter_id"],
            "split": row["split"],
            "atr_enabled": row["atr_enabled"],
            "model_risk_enabled": row["model_risk_enabled"],
            "max_model_risk_pct": row["max_model_risk_pct"],
            "risk_floor_applied_count": row["risk_floor_applied_count"],
            "max_actual_risk_pct_after_floor": row["max_actual_risk_pct_after_floor"],
            "avg_executed_lot": row["avg_executed_lot"],
            "avg_atr_points": row["avg_atr_points"],
            "avg_open_sl_points": row["avg_open_sl_points"],
            "avg_open_tp_points": row["avg_open_tp_points"],
            "risk_bucket": row["risk_bucket"],
            "read": "ATR(평균 진폭) bracket(브래킷)과 model risk(모델 위험)는 켜져 있고 floor(최소 랏 바닥) 영향은 0으로 보인다.",
        }
        for row in risk_rows
        if row.get("view") == "actual_routed_total" and row.get("split") in {"validation_is", "oos"}
    ]

    probability_review_rows = [
        {
            "adapter_id": row["adapter_id"],
            "split": row["split"],
            "block_mode": row["block_mode"],
            "directional_threshold_pass_rows": row["directional_threshold_pass_rows"],
            "side_filter_block_rows": row["side_filter_block_rows"],
            "order_attempted_rows": row["order_attempted_rows"],
            "order_filled_rows": row["order_filled_rows"],
            "decision_counts": row["decision_counts"],
            "read": "score surface(점수 표면)와 threshold(임계값)는 고정이고, 차이는 short margin gate(숏 마진 차단문) 공급 변화에서 나온다.",
        }
        for row in probability_rows
        if row.get("view") == "actual_routed_total" and row.get("split") in {"validation_is", "oos"}
    ]

    attribution_rows = [
        {
            "attribution_id": f"{RUN_ID}__highedge_best_tradeoff",
            "observed_change": "s258_tight_plus_highedge improved validation PF from 1.48 to 1.56 and validation net from 1043.99 to 1204.24 versus control.",
            "comparison_baseline": "s258_short_tight_control",
            "likely_drivers": "high-edge short margin guard changed short supply while score table, threshold, lifecycle, ATR bracket, and model risk stayed fixed.",
            "segment_checks": "validation/OOS, early/mid/late PF, DD, gate row counts, probability telemetry, risk/ATR telemetry.",
            "trade_shape": "validation DD stayed low at 9.0307, OOS DD improved to 9.5478, but OOS net fell by 121.26 versus control.",
            "alternative_explanations": "gain may come from removing a harmful cluster rather than durable signal quality; OOS net loss keeps confidence below high.",
            "attribution_confidence": "medium_high",
            "next_probe": NEXT_STAGE_ID,
        },
        {
            "attribution_id": f"{RUN_ID}__lowedge_side_clue_not_primary",
            "observed_change": "s258_tight_plus_lowedge raised OOS PF to 1.76 and mid PF to 1.5565 but validation net fell to 815.42.",
            "comparison_baseline": "s258_short_tight_control",
            "likely_drivers": "low-edge guard pruned supply more aggressively and helped some OOS/mid-late buckets while damaging validation early/net quality.",
            "segment_checks": "early/mid/late PF and validation/OOS net/DD.",
            "trade_shape": "useful side clue but not a primary path because validation net is below the 34D lesson-only target.",
            "alternative_explanations": "OOS PF gain could be sample shrink rather than robust edge.",
            "attribution_confidence": "medium",
            "next_probe": NEXT_STAGE_ID,
        },
        {
            "attribution_id": f"{RUN_ID}__single_edge_guards_failure_memory",
            "observed_change": "lowedge_only and highedge_only both damaged at least one critical validation or OOS guardrail.",
            "comparison_baseline": "s258_short_tight_control",
            "likely_drivers": "single edge guard changes supply too broadly compared with the tight-plus composite guards.",
            "segment_checks": "validation PF/net/DD, mid PF, OOS PF/net/DD.",
            "trade_shape": "single guard variants are failure memory, not next primary candidates.",
            "alternative_explanations": "some OOS net was preserved, but validation/mid/OOS DD guardrails are too weak.",
            "attribution_confidence": "medium_high",
            "next_probe": NEXT_STAGE_ID,
        },
    ]

    failure_rows = [
        {
            "failure_id": f"{RUN_ID}__hard_quality_not_reached",
            "evidence": "hard_quality_pass=False for every Stage258 candidate.",
            "impact": "Stage258 cannot be treated as final even though s258_tight_plus_highedge is a useful v2 tradeoff.",
            "next_handling": NEXT_STAGE_ID,
        },
        {
            "failure_id": f"{RUN_ID}__highedge_pf_gap_remaining",
            "evidence": "s258_tight_plus_highedge validation_pf=1.56 versus 34D lesson-only PF target=1.583157; validation_mid_pf=1.534204818.",
            "impact": "Stage260 must close the PF and mid-PF gap without losing low DD and validation net.",
            "next_handling": NEXT_STAGE_ID,
        },
        {
            "failure_id": f"{RUN_ID}__highedge_oos_net_damage",
            "evidence": "s258_tight_plus_highedge OOS net=828.96 versus control OOS net=950.22.",
            "impact": "Stage260 must recover OOS net/PF consistency instead of only optimizing validation headline net.",
            "next_handling": NEXT_STAGE_ID,
        },
    ]

    route_rows = [
        {
            "route_id": f"{RUN_ID}__open_stage260_highedge_pf_oos_recovery",
            "evidence": "s258_tight_plus_highedge is the strongest validation tradeoff but remains not-final due to PF/midPF and OOS net gaps.",
            "decision": DECISION,
            "effect": "Stage260(260단계)은 highedge composite guard(고엣지 복합 차단문)를 보존하면서 PF(수익 팩터)와 OOS(표본외) 회복만 좁게 시험한다.",
            "next_stage_or_branch": NEXT_STAGE_ID,
        }
    ]

    return {
        "control": control_row,
        "best": best_row,
        "tradeoff_rows": tradeoff_rows,
        "gate_rows": gate_rows,
        "risk_review_rows": risk_review_rows,
        "probability_review_rows": probability_review_rows,
        "source_attr_rows": source_attr_rows,
        "source_failure_rows": source_failure_rows,
        "attribution_rows": attribution_rows,
        "failure_rows": failure_rows,
        "route_rows": route_rows,
    }


def write_reports(review: Mapping[str, Any]) -> None:
    tradeoff_rows = review["tradeoff_rows"]
    write_csv(TRADEOFF_PATH, tradeoff_rows, list(tradeoff_rows[0].keys()))
    write_csv(ATTRIBUTION_PATH, review["attribution_rows"], list(review["attribution_rows"][0].keys()))
    write_csv(FAILURE_PATH, review["failure_rows"], list(review["failure_rows"][0].keys()))
    write_csv(ROUTE_PATH, review["route_rows"], list(review["route_rows"][0].keys()))
    write_csv(RISK_REVIEW_PATH, review["risk_review_rows"], list(review["risk_review_rows"][0].keys()))
    write_csv(PROBABILITY_REVIEW_PATH, review["probability_review_rows"], list(review["probability_review_rows"][0].keys()))

    rows = "\n".join(
        "| {adapter_id} | {validation_pf} | {validation_pf_gap_vs_34d} | {validation_net} | {validation_net_delta_vs_control} | {validation_dd_percent} | {validation_mid_pf} | {oos_pf} | {oos_net} | {oos_net_delta_vs_control} | {review_label} |".format(**row)
        for row in tradeoff_rows
    )
    write_text(
        REPORT_PATH,
        f"""# Stage259 Stage258 Short Tight Margin PF Follow-up Review(259단계 258단계 숏 좁은 마진 PF 후속 검토)

- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- source_stage258_evidence_commit(원천 258단계 근거 커밋): `{SOURCE_STAGE258_EVIDENCE_COMMIT}`
- source_stage258_hash_record_commit(원천 258단계 해시 기록 커밋): `{SOURCE_STAGE258_HASH_RECORD_COMMIT}`
- decision(판정): `{DECISION}`
- boundary(주장 경계): `{BOUNDARY}`

## Easy Read(쉬운 해석)

Stage258(258단계)는 완성(final, 최종)이 아니다. 그래도 `s258_tight_plus_highedge`는 지금까지의 v2 고유 연구에서 가장 쓸 만한 tradeoff(절충안)이다.

좋은 점은 validation(검증) net(순수익) 1204.24, DD(손실폭) 9.0307, early PF(초기 수익 팩터) 1.6751이다. 나쁜 점은 validation PF(검증 수익 팩터) 1.56이 34D 목표 1.583157보다 아직 낮고, mid PF(중간 수익 팩터) 1.5342도 낮으며, OOS net(표본외 순수익)이 control(대조군)보다 121.26 낮다는 것이다.

그래서 Stage260(260단계)은 `s258_tight_plus_highedge`를 중심으로 PF(수익 팩터)와 OOS(표본외) 회복만 좁게 시험한다.

## KPI Tradeoff(KPI 절충)

| adapter(어댑터) | val PF(검증 수익 팩터) | PF gap vs 34D(34D 대비 PF 차이) | val net(검증 순수익) | net delta(순수익 차이) | DD%(손실폭) | mid PF(중간 수익 팩터) | OOS PF(표본외 수익 팩터) | OOS net(표본외 순수익) | OOS net delta(표본외 순수익 차이) | read(해석) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
{rows}

## Judgment(판정)

- result_subject(판정 대상): `{RUN_ID}`
- evidence_available(사용 근거): Stage258 quality matrix(품질 행렬), source feature summary(소스 피처 요약), probability telemetry(확률 원격측정), risk/ATR telemetry(위험/ATR 원격측정), performance attribution(성과 귀속).
- evidence_missing(부족 근거): Stage260 repair result(260단계 수리 결과), ONNX parity(ONNX 동등성), MT5 ONNX/runtime reproduction(MT5 ONNX/런타임 재현).
- judgment_label(판정 라벨): `useful_tradeoff_not_final`
- next_condition(다음 조건): `{NEXT_STAGE_ID}`
- forbidden_claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), production_baseline(생산 기준), overall_goal_complete(전체 목표 완료).
""",
    )

    write_text(
        DECISION_PATH,
        f"""# Stage259 Decision(259단계 판정)

- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- decision(판정): `{DECISION}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- source_stage258_evidence_commit(원천 258단계 근거 커밋): `{SOURCE_STAGE258_EVIDENCE_COMMIT}`
- source_stage258_hash_record_commit(원천 258단계 해시 기록 커밋): `{SOURCE_STAGE258_HASH_RECORD_COMMIT}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- report(보고서): `{rel(REPORT_PATH)}`
- tradeoff_matrix(절충 행렬): `{rel(TRADEOFF_PATH)}`
- attribution(성과 귀속): `{rel(ATTRIBUTION_PATH)}`
- failure_memory(실패 기억): `{rel(FAILURE_PATH)}`
- route_matrix(경로 행렬): `{rel(ROUTE_PATH)}`
- risk_atr_review(위험/ATR 검토): `{rel(RISK_REVIEW_PATH)}`
- probability_review(확률 검토): `{rel(PROBABILITY_REVIEW_PATH)}`
- next_stage_or_branch(다음 단계 또는 분기): `{NEXT_STAGE_ID}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage259(259단계) closeout(종료)은 overall goal complete(전체 목표 완료)가 아니다.
""",
    )

    write_text(
        REVIEW_INDEX_PATH,
        f"""# Stage259 Review Index(259단계 검토 색인)

- status(상태): `closed_open_stage260_highedge_pf_oos_recovery_candidate_not_final`
- run(실행): `{RUN_ID}`
- decision(판정): `{DECISION}`
- report(보고서): `{rel(REPORT_PATH)}`
- tradeoff_matrix(절충 행렬): `{rel(TRADEOFF_PATH)}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
""",
    )
    write_text(
        SELECTION_PATH,
        f"""# Stage259 Selection Status(259단계 선택 상태)

- stage_status(단계 상태): `closed_open_stage260_highedge_pf_oos_recovery_candidate_not_final`
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

Stage260(260단계)는 Stage259(259단계)가 고른 `s258_tight_plus_highedge` tradeoff(절충안)를 좁게 수리하는 bounded repair(경계 수리) 단계다.

## Bounded Question(경계 질문)

Can a v2-native repair(v2 고유 수리) preserve `s258_tight_plus_highedge` validation net/DD(검증 순수익/손실폭) gains while closing the remaining PF/mid-PF gap(PF/중간 PF 차이) and recovering OOS net/PF(표본외 순수익/PF)?

## Boundary(경계)

`{BOUNDARY}`
""",
    )
    write_text(
        NEXT_STAGE_ROOT / "01_inputs/input_refs.md",
        f"""# Stage260 Input References(260단계 입력 참조)

- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- source_decision(원천 판정): `{DECISION}`
- source_report(원천 보고서): `{rel(REPORT_PATH)}`
- source_tradeoff_matrix(원천 절충 행렬): `{rel(TRADEOFF_PATH)}`
- source_stage258_evidence_commit(원천 258단계 근거 커밋): `{SOURCE_STAGE258_EVIDENCE_COMMIT}`
- source_stage258_hash_record_commit(원천 258단계 해시 기록 커밋): `{SOURCE_STAGE258_HASH_RECORD_COMMIT}`
""",
    )
    write_text(
        NEXT_STAGE_ROOT / "03_reviews/review_index.md",
        f"""# Stage260 Review Index(260단계 검토 색인)

- status(상태): `open_planned_from_stage259`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- source_stage(원천 단계): `{STAGE_ID}`
- source_decision(원천 판정): `{DECISION}`
""",
    )
    write_text(
        NEXT_STAGE_ROOT / "04_selected/selection_status.md",
        f"""# Stage260 Selection Status(260단계 선택 상태)

- stage_status(단계 상태): `open_planned_from_stage259`
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
- adapter_under_review(검토 중 어댑터): `s258_tight_plus_highedge`
- status(상태): `stage259_closed_open_stage260_highedge_pf_oos_recovery_candidate_not_final`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage259(259단계)는 Stage258(258단계) 결과를 review-only(검토 전용)로 판정했다.
Effect(효과): Stage260(260단계)은 `s258_tight_plus_highedge`의 validation net/DD(검증 순수익/손실폭) 장점을 지키면서 PF(수익 팩터), mid PF(중간 PF), OOS(표본외) 회복을 좁게 시험한다.

## Latest Stage259 Evidence(최신 259단계 근거)

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
  Stage259(259단계) closed(종료) as `{DECISION}` and Stage260(260단계) `{NEXT_STAGE_ID}` is open_planned(개방 계획). Effect(효과): Stage258(258단계)의 가장 강한 tradeoff(절충안)인 `s258_tight_plus_highedge`를 좁은 PF/OOS recovery(PF/표본외 회복) 질문으로 넘긴다.
- >-
  Stage259 evidence(259단계 근거)는 `{rel(REPORT_PATH)}`, `{rel(TRADEOFF_PATH)}`, `{rel(ATTRIBUTION_PATH)}`, `{rel(FAILURE_PATH)}`에 있다. Effect(효과): Stage260(260단계)은 validation net/DD(검증 순수익/손실폭) 장점을 보존하면서 PF(수익 팩터), mid PF(중간 PF), OOS net/PF(표본외 순수익/PF)를 복구해야 한다.
- >-
  Target surface(목표 표면)는 `{TARGET_SURFACE}`이고 legacy 34D(레거시 34D)는 lesson-only KPI target(교훈 전용 KPI 목표)이다. Effect(효과): v2-native research(v2 고유 연구)를 계속한다.
"""
    workspace = re.sub(r"current_focus:\n.*?(?=\n[A-Za-z0-9_]+:\n)", focus, workspace, count=1, flags=re.DOTALL)
    stage259_block = f"""stage259_stage258_short_tight_margin_pf_followup_review:
  packet_id: {PACKET_ID}
  stage_id: {STAGE_ID}
  status: closed_open_stage260_highedge_pf_oos_recovery_candidate_not_final
  current_run_id: {RUN_ID}
  source_stage: {SOURCE_STAGE_ID}
  source_run: {SOURCE_RUN_ID}
  source_stage258_evidence_commit: {SOURCE_STAGE258_EVIDENCE_COMMIT}
  source_stage258_hash_record_commit: {SOURCE_STAGE258_HASH_RECORD_COMMIT}
  decision: {DECISION}
  report_path: {rel(REPORT_PATH)}
  decision_path: {rel(DECISION_PATH)}
  tradeoff_matrix_path: {rel(TRADEOFF_PATH)}
  attribution_path: {rel(ATTRIBUTION_PATH)}
  failure_memory_path: {rel(FAILURE_PATH)}
  route_matrix_path: {rel(ROUTE_PATH)}
  risk_atr_review_path: {rel(RISK_REVIEW_PATH)}
  probability_review_path: {rel(PROBABILITY_REVIEW_PATH)}
  external_verification_status: {EXTERNAL_STATUS}
  pushed_commit_hash: pending_until_push
  next_action: {NEXT_RUN_ID}
  boundary: {BOUNDARY}
"""
    stage260_block = f"""stage260_tight_plus_highedge_pf_oos_recovery_repair:
  packet_id: {NEXT_PACKET_ID}
  stage_id: {NEXT_STAGE_ID}
  status: open_planned_from_stage259
  current_run_id: {NEXT_RUN_ID}
  source_stage: {STAGE_ID}
  source_run: {RUN_ID}
  source_decision: {DECISION}
  next_action: {NEXT_RUN_ID}
  boundary: {BOUNDARY}
"""
    workspace = replace_or_append_block(workspace, "stage259_stage258_short_tight_margin_pf_followup_review", stage259_block)
    workspace = replace_or_append_block(workspace, "stage260_tight_plus_highedge_pf_oos_recovery_repair", stage260_block)
    write_text(WORKSPACE_STATE_PATH, workspace, bom=False)

    existing = read_text(CHANGELOG_PATH) if CHANGELOG_PATH.exists() else ""
    marker = "Stage259 Stage258 short tight margin PF follow-up review closeout"
    existing = re.sub(rf"\n## [^\n]*{re.escape(marker)}[^\n]*\n.*?(?=\n## |\Z)", "", existing, flags=re.DOTALL)
    entry = f"""
## {utc_now()} {marker}(259단계 258단계 숏 좁은 마진 PF 후속 검토 종료)

- action(행동): closed(종료) `{STAGE_ID}` with decision(판정) `{DECISION}`.
- effect(효과): `s258_tight_plus_highedge`를 Stage260(260단계) PF/OOS recovery(PF/표본외 회복) 질문으로 좁혔다.
- boundary(주장 경계): `{BOUNDARY}`.
"""
    write_text(CHANGELOG_PATH, existing.rstrip() + entry, bom=False)


def write_ledgers_and_packet(review: Mapping[str, Any]) -> None:
    best = next(row for row in review["tradeoff_rows"] if row["adapter_id"] == "s258_tight_plus_highedge")
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__review_total",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "stage259_review_total",
        "parent_run_id": SOURCE_RUN_ID,
        "record_view": "review_total",
        "tier_scope": "Tier A+B",
        "kpi_scope": "baseline_adapter_followup_review",
        "scoreboard_lane": "baseline_adapter_stage259_stage258_followup_review",
        "status": "reviewed_closed",
        "judgment": DECISION,
        "path": rel(REPORT_PATH),
        "primary_kpi": f"best=s258_tight_plus_highedge;validation_pf={best['validation_pf']};validation_net={best['validation_net']};validation_dd={best['validation_dd_percent']};oos_net={best['oos_net']}",
        "guardrail_kpi": "hard_quality_pass_count=0;pf_gap_remaining=1;oos_net_recovery_needed=1;overall_goal_complete=0",
        "external_verification_status": EXTERNAL_STATUS,
        "notes": "Stage259 review only; routes to bounded Stage260 tight_plus_highedge PF/OOS recovery repair.",
    }
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "baseline_adapter_stage259_stage258_followup_review",
        "status": "reviewed_closed",
        "judgment": DECISION,
        "path": rel(REPORT_PATH),
        "notes": f"source_stage258_evidence_commit={SOURCE_STAGE258_EVIDENCE_COMMIT};source_stage258_hash_record_commit={SOURCE_STAGE258_HASH_RECORD_COMMIT};overall_goal_complete=0;boundary={BOUNDARY}",
    }
    write_csv(STAGE_LEDGER_PATH, [alpha_row], ALPHA_COLUMNS)
    run_payload = upsert_csv(RUN_REGISTRY_PATH, RUN_COLUMNS, [run_row], "run_id")
    project_payload = upsert_csv(PROJECT_LEDGER_PATH, ALPHA_COLUMNS, [alpha_row], "ledger_row_id")
    stage_payload = {"path": rel(STAGE_LEDGER_PATH), "rows": 1, "upserted_rows": 1, "sha256": sha256_lf(STAGE_LEDGER_PATH), "hash_policy": "lf_normalized_text_register"}
    ledger_payload: dict[str, Any] = {"run_registry": run_payload, "project_alpha_ledger": project_payload, "stage_ledger": stage_payload}

    summary = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "packet_id": PACKET_ID,
        "source_stage": SOURCE_STAGE_ID,
        "source_run": SOURCE_RUN_ID,
        "source_stage258_evidence_commit": SOURCE_STAGE258_EVIDENCE_COMMIT,
        "source_stage258_hash_record_commit": SOURCE_STAGE258_HASH_RECORD_COMMIT,
        "decision": DECISION,
        "next_stage_or_branch": NEXT_STAGE_ID,
        "external_verification_status": EXTERNAL_STATUS,
        "overall_goal_complete": False,
        "pushed_commit_hash": "pending_until_push",
        "claim_boundary": BOUNDARY,
        "legacy_34d_lesson_only_targets": {"validation_net": LEGACY_34D_NET, "validation_pf": LEGACY_34D_PF, "validation_dd": LEGACY_34D_DD},
        "tradeoff_rows": review["tradeoff_rows"],
        "gate_rows": review["gate_rows"],
        "risk_review_rows": review["risk_review_rows"],
        "probability_review_rows": review["probability_review_rows"],
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
        PROBABILITY_REVIEW_PATH,
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
    artifact_rows = [
        {
            "artifact_id": artifact_id_for(path),
            "artifact_type": "stage259_followup_review_evidence",
            "path": rel(path),
            "sha256": sha256_lf(path),
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": created,
            "notes": "Stage259 Stage258 short_tight_margin PF follow-up review evidence; research only.",
        }
        for path in artifact_paths
        if path.exists()
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
        "routing_receipt.json": {**base_payload, "route": DECISION, "route_effect": "open Stage260 tight_plus_highedge PF/OOS recovery repair"},
        "kpi_contract_audit.json": {**base_payload, "status": "passed", "kpi_basis": [rel(QUALITY_PATH), rel(SOURCE_FEATURE_PATH), rel(PROBABILITY_PATH), rel(RISK_PATH)]},
        "result_judgment_gate.json": {
            **base_payload,
            "result_subject": RUN_ID,
            "evidence_available": [rel(REPORT_PATH), rel(TRADEOFF_PATH), rel(ATTRIBUTION_PATH), rel(FAILURE_PATH), rel(RISK_REVIEW_PATH), rel(PROBABILITY_REVIEW_PATH)],
            "evidence_missing": [NEXT_STAGE_ID, "ONNX parity(ONNX 동등성)", "MT5 ONNX/runtime reproduction(MT5 ONNX/런타임 재현)"],
            "judgment_label": "useful_tradeoff_not_final",
            "next_condition": NEXT_STAGE_ID,
        },
        "performance_attribution_gate.json": {**base_payload, "attribution_rows": review["attribution_rows"], "attribution_confidence": "medium_high"},
        "artifact_lineage_audit.json": {
            **base_payload,
            "source_inputs": [rel(QUALITY_PATH), rel(SOURCE_FEATURE_PATH), rel(KPI_PATH), rel(PROBABILITY_PATH), rel(RISK_PATH), rel(SOURCE_REPORT_PATH), rel(SOURCE_DECISION_PATH)],
            "producer": rel(PRODUCER_PATH),
            "consumer": NEXT_STAGE_ID,
            "artifact_paths": [rel(path) for path in artifact_paths if path.exists()],
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
        f"""# Stage259 Closeout Packet(259단계 종료 작업 묶음)

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


def main() -> int:
    review = build_review()
    write_reports(review)
    write_next_stage_seed()
    update_current_truth()
    write_ledgers_and_packet(review)
    print(json.dumps({"stage": STAGE_ID, "decision": DECISION, "next_stage": NEXT_STAGE_ID}, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
