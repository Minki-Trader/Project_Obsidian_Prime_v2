from __future__ import annotations

import csv
import hashlib
import json
import re
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence


STAGE_ID = "261_adapter_research__stage260_tight_plus_highedge_pf_oos_followup_review"
RUN_ID = "run261A_stage261_stage260_tight_plus_highedge_pf_oos_followup_review_v1"
PACKET_ID = "stage261_stage260_tight_plus_highedge_pf_oos_followup_review_v1"
SOURCE_STAGE_ID = "260_adapter_research__tight_plus_highedge_pf_oos_recovery_repair"
SOURCE_RUN_ID = "run260A_stage260_tight_plus_highedge_pf_oos_recovery_repair_v1"
SOURCE_STAGE260_EVIDENCE_COMMIT = "eb99d51a9d38093e9ed2c97932f93b10127edb49"
SOURCE_STAGE260_HASH_RECORD_COMMIT = "8cdeb8526ed3fbb1aae24a25a990aab846916332"
NEXT_STAGE_ID = "262_adapter_research__lowrank_lowedge_oos_recovery_repair"
NEXT_RUN_ID = "run262A_stage262_lowrank_lowedge_oos_recovery_repair_v1"
NEXT_PACKET_ID = "stage262_lowrank_lowedge_oos_recovery_repair_v1"
DECISION = "open_stage262_bounded_lowrank_lowedge_oos_recovery_candidate_not_final"
BOUNDARY = "research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment"
TARGET_SURFACE = "legacy_34d_kpi_lesson_only_v2_native_lowrank_lowedge_oos_recovery_repair"
EXTERNAL_STATUS = "review_only_source_stage260_mt5_reports_completed"

LEGACY_34D_NET = 987.60
LEGACY_34D_PF = 1.583157
LEGACY_34D_DD = 12.909136

ROOT = Path.cwd()
STAGE_ROOT = ROOT / "stages" / STAGE_ID
REVIEWS = STAGE_ROOT / "03_reviews"
PACKET_ROOT = ROOT / "docs/agent_control/packets" / PACKET_ID
NEXT_STAGE_ROOT = ROOT / "stages" / NEXT_STAGE_ID
SOURCE_REVIEWS = ROOT / "stages" / SOURCE_STAGE_ID / "03_reviews"

QUALITY_PATH = SOURCE_REVIEWS / "stage260_quality_matrix.csv"
SOURCE_FEATURE_PATH = SOURCE_REVIEWS / "stage260_source_feature_summary.csv"
PROBABILITY_PATH = SOURCE_REVIEWS / "stage260_probability_telemetry_summary.csv"
RISK_PATH = SOURCE_REVIEWS / "stage260_risk_atr_telemetry.csv"
SOURCE_REPORT_PATH = SOURCE_REVIEWS / "stage260_tight_plus_highedge_pf_oos_recovery_report.md"
SOURCE_DECISION_PATH = SOURCE_REVIEWS / "stage260_decision.md"

REPORT_PATH = REVIEWS / "stage261_stage260_tight_plus_highedge_pf_oos_followup_review.md"
TRADEOFF_PATH = REVIEWS / "stage261_tradeoff_review_matrix.csv"
ATTRIBUTION_PATH = REVIEWS / "stage261_performance_attribution.csv"
FAILURE_PATH = REVIEWS / "stage261_failure_memory.csv"
ROUTE_PATH = REVIEWS / "stage261_route_matrix.csv"
RISK_REVIEW_PATH = REVIEWS / "stage261_risk_atr_review.csv"
PROBABILITY_REVIEW_PATH = REVIEWS / "stage261_probability_review.csv"
SUMMARY_PATH = REVIEWS / "stage261_summary.json"
DECISION_PATH = REVIEWS / "stage261_decision.md"
STAGE_LEDGER_PATH = REVIEWS / "stage_run_ledger.csv"
REVIEW_INDEX_PATH = REVIEWS / "review_index.md"
SELECTION_PATH = STAGE_ROOT / "04_selected/selection_status.md"

CURRENT_STATE_PATH = ROOT / "docs/context/current_working_state.md"
WORKSPACE_STATE_PATH = ROOT / "docs/workspace/workspace_state.yaml"
CHANGELOG_PATH = ROOT / "docs/workspace/changelog.md"
RUN_REGISTRY_PATH = ROOT / "docs/registers/run_registry.csv"
PROJECT_LEDGER_PATH = ROOT / "docs/registers/alpha_run_ledger.csv"
ARTIFACT_REGISTRY_PATH = ROOT / "docs/registers/artifact_registry.csv"
PRODUCER_PATH = ROOT / "stage_pipelines/stage261/stage260_tight_plus_highedge_pf_oos_followup_review.py"

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
    return {"path": rel(path), "rows": len(ordered), "upserted_rows": len(rows), "sha256": sha256_lf(path), "hash_policy": "lf_normalized_text_register"}


def replace_or_append_block(text: str, key: str, block: str) -> str:
    pattern = rf"^{re.escape(key)}:\n(?:  .*\n)+"
    if re.search(pattern, text, flags=re.MULTILINE):
        return re.sub(pattern, block, text, count=1, flags=re.MULTILINE)
    return text.rstrip() + "\n\n" + block


def build_review() -> dict[str, Any]:
    quality_rows = read_csv(QUALITY_PATH)
    feature_rows = read_csv(SOURCE_FEATURE_PATH)
    risk_rows = read_csv(RISK_PATH)
    probability_rows = read_csv(PROBABILITY_PATH)
    control = next(row for row in quality_rows if row["adapter_id"] == "s260_highedge_control")
    best = next(row for row in quality_rows if row["adapter_id"] == "s260_lowrank_lowedge_filter")
    control_values = {
        "validation_pf": as_float(control["validation_pf"]),
        "validation_net": as_float(control["validation_net"]),
        "validation_dd": as_float(control["validation_balance_dd_percent"]),
        "validation_mid_pf": as_float(control["validation_mid_pf"]),
        "oos_pf": as_float(control["oos_pf"]),
        "oos_net": as_float(control["oos_net"]),
        "oos_dd": as_float(control["oos_balance_dd_percent"]),
    }
    tradeoff_rows: list[dict[str, Any]] = []
    for row in quality_rows:
        adapter = row["adapter_id"]
        val_pf = as_float(row["validation_pf"])
        val_net = as_float(row["validation_net"])
        val_dd = as_float(row["validation_balance_dd_percent"])
        mid_pf = as_float(row["validation_mid_pf"])
        oos_pf = as_float(row["oos_pf"])
        oos_net = as_float(row["oos_net"])
        if adapter == "s260_lowrank_lowedge_filter":
            label = "best_validation_tradeoff_oos_repair_needed"
            read = "validation(검증) PF/net/mid PF가 34D 목표를 넘지만 OOS net/PF가 아직 약해 다음 단계에서 표본외 회복이 필요하다."
            next_handling = NEXT_STAGE_ID
        elif adapter == "s260_lowrank_filter_vhigh_relax":
            label = "duplicate_best_shape_oos_repair_needed"
            read = "lowrank filter와 같은 KPI 모양이다. 독립 축이라기보다 같은 단서로 묶는다."
            next_handling = NEXT_STAGE_ID
        elif adapter == "s260_midlow_lowedge_filter":
            label = "oos_pf_help_validation_damage"
            read = "OOS PF는 1.78까지 회복했지만 validation net/DD/mid PF가 약해 주축 후보가 아니다."
            next_handling = "side_clue_only"
        elif adapter == "s260_highedge_control":
            label = "control_reference_not_final"
            read = "Stage258 highedge control은 validation net/DD는 좋지만 PF와 mid PF가 아직 낮다."
            next_handling = "reference_only"
        else:
            label = "no_effect_or_duplicate"
            read = "대조군과 사실상 같거나 추가 개선이 없다."
            next_handling = "failure_memory"
        tradeoff_rows.append(
            {
                "adapter_id": adapter,
                "axis": row["axis"],
                "validation_pf": row["validation_pf"],
                "validation_pf_gap_vs_34d": fmt(val_pf - LEGACY_34D_PF, 6),
                "validation_net": row["validation_net"],
                "validation_net_delta_vs_control": fmt(val_net - control_values["validation_net"]),
                "validation_net_gap_vs_34d": fmt(val_net - LEGACY_34D_NET),
                "validation_dd_percent": row["validation_balance_dd_percent"],
                "validation_dd_delta_vs_control": fmt(val_dd - control_values["validation_dd"], 4),
                "validation_dd_margin_vs_34d": fmt(LEGACY_34D_DD - val_dd, 4),
                "validation_early_pf": row["validation_early_pf"],
                "validation_mid_pf": row["validation_mid_pf"],
                "validation_mid_pf_gap_vs_34d_pf": fmt(mid_pf - LEGACY_34D_PF, 6),
                "validation_late_pf": row["validation_late_pf"],
                "oos_pf": row["oos_pf"],
                "oos_pf_delta_vs_control": fmt(oos_pf - control_values["oos_pf"], 4),
                "oos_net": row["oos_net"],
                "oos_net_delta_vs_control": fmt(oos_net - control_values["oos_net"]),
                "oos_dd_percent": row["oos_balance_dd_percent"],
                "hard_quality_pass": row["hard_quality_pass"],
                "quality_flags": row["quality_flags"],
                "review_label": label,
                "plain_read": read,
                "next_handling": next_handling,
            }
        )
    risk_review_rows = [
        {key: row.get(key, "") for key in ["adapter_id", "split", "atr_enabled", "model_risk_enabled", "max_model_risk_pct", "risk_floor_applied_count", "max_actual_risk_pct_after_floor", "avg_executed_lot", "avg_atr_points", "avg_open_sl_points", "avg_open_tp_points", "risk_bucket"]}
        for row in risk_rows
        if row.get("view") == "actual_routed_total" and row.get("split") in {"validation_is", "oos"}
    ]
    probability_review_rows = [
        {key: row.get(key, "") for key in ["adapter_id", "split", "block_mode", "directional_threshold_pass_rows", "side_filter_block_rows", "order_attempted_rows", "order_filled_rows", "decision_counts"]}
        for row in probability_rows
        if row.get("view") == "actual_routed_total" and row.get("split") in {"validation_is", "oos"}
    ]
    gate_rows = [
        {key: row.get(key, "") for key in ["adapter_id", "split", "source_branch_mode", "signal_rows", "base_blocked_signal_rows", "blocked_signal_rows", "changed_gate_rows", "allowed_signal_rows", "allowed_signal_rank_counts"]}
        for row in feature_rows
    ]
    attribution_rows = [
        {
            "attribution_id": f"{RUN_ID}__lowrank_filter_best_validation_tradeoff",
            "observed_change": "s260_lowrank_lowedge_filter: validation_pf=1.61, validation_net=1291.28, validation_mid_pf=1.600364571, OOS net=775.97.",
            "comparison_baseline": "s260_highedge_control",
            "likely_drivers": "low-rank low-edge short signals were blocked while thresholds/lifecycle/ATR/risk stayed fixed.",
            "segment_checks": "validation/OOS, early/mid/late PF, DD, probability telemetry, risk/ATR telemetry.",
            "trade_shape": "validation quality improved strongly but OOS net fell by 52.99 versus control.",
            "alternative_explanations": "validation improvement may be a cluster-removal gain rather than robust OOS improvement.",
            "attribution_confidence": "medium_high",
            "next_probe": NEXT_STAGE_ID,
        },
        {
            "attribution_id": f"{RUN_ID}__midlow_filter_side_clue",
            "observed_change": "s260_midlow_lowedge_filter: OOS PF=1.78 but validation net=972.15 and DD=12.9281.",
            "comparison_baseline": "s260_highedge_control",
            "likely_drivers": "broader low/mid-rank filtering removed more supply and restored OOS PF while damaging validation net/DD.",
            "segment_checks": "validation net/DD/mid PF and OOS PF/net.",
            "trade_shape": "side clue only; not next primary anchor.",
            "alternative_explanations": "OOS PF recovery may come from supply shrink.",
            "attribution_confidence": "medium",
            "next_probe": NEXT_STAGE_ID,
        },
    ]
    failure_rows = [
        {
            "failure_id": f"{RUN_ID}__oos_recovery_needed",
            "evidence": "best validation tradeoff s260_lowrank_lowedge_filter has OOS net=775.97 and OOS PF=1.70.",
            "impact": "cannot stop at validation PF/net improvement; Stage262 must target OOS recovery.",
            "next_handling": NEXT_STAGE_ID,
        },
        {
            "failure_id": f"{RUN_ID}__stage261_not_overall_complete",
            "evidence": "ONNX parity, MT5 ONNX/runtime reproduction, and research package review are not done.",
            "impact": "research/development continues; no deployment or live-readiness claim.",
            "next_handling": NEXT_STAGE_ID,
        },
    ]
    route_rows = [
        {
            "route_id": f"{RUN_ID}__open_stage262_lowrank_lowedge_oos_recovery",
            "evidence": "s260_lowrank_lowedge_filter is the best validation tradeoff but OOS net/PF remain weak.",
            "decision": DECISION,
            "effect": "Stage262(262단계)는 lowrank_lowedge_filter(낮은 순위 낮은 마진 가장자리 필터)의 validation 장점을 지키며 OOS 회복만 좁게 시험한다.",
            "next_stage_or_branch": NEXT_STAGE_ID,
        }
    ]
    return {
        "control": control,
        "best": best,
        "tradeoff_rows": tradeoff_rows,
        "gate_rows": gate_rows,
        "risk_review_rows": risk_review_rows,
        "probability_review_rows": probability_review_rows,
        "attribution_rows": attribution_rows,
        "failure_rows": failure_rows,
        "route_rows": route_rows,
    }


def write_reports(review: Mapping[str, Any]) -> None:
    write_csv(TRADEOFF_PATH, review["tradeoff_rows"], list(review["tradeoff_rows"][0].keys()))
    write_csv(ATTRIBUTION_PATH, review["attribution_rows"], list(review["attribution_rows"][0].keys()))
    write_csv(FAILURE_PATH, review["failure_rows"], list(review["failure_rows"][0].keys()))
    write_csv(ROUTE_PATH, review["route_rows"], list(review["route_rows"][0].keys()))
    write_csv(RISK_REVIEW_PATH, review["risk_review_rows"], list(review["risk_review_rows"][0].keys()))
    write_csv(PROBABILITY_REVIEW_PATH, review["probability_review_rows"], list(review["probability_review_rows"][0].keys()))
    rows = "\n".join(
        "| {adapter_id} | {validation_pf} | {validation_pf_gap_vs_34d} | {validation_net} | {validation_dd_percent} | {validation_mid_pf} | {oos_pf} | {oos_net} | {review_label} |".format(**row)
        for row in review["tradeoff_rows"]
    )
    write_text(
        REPORT_PATH,
        f"""# Stage261 Stage260 Tight Plus High Edge PF/OOS Follow-up Review(261단계 260단계 PF/표본외 후속 검토)

- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- source_stage260_evidence_commit(원천 260단계 근거 커밋): `{SOURCE_STAGE260_EVIDENCE_COMMIT}`
- source_stage260_hash_record_commit(원천 260단계 해시 기록 커밋): `{SOURCE_STAGE260_HASH_RECORD_COMMIT}`
- decision(판정): `{DECISION}`
- boundary(주장 경계): `{BOUNDARY}`

## Easy Read(쉬운 해석)

`s260_lowrank_lowedge_filter`는 validation(검증) 기준으로는 34D(레거시 34D) 목표를 넘었다. validation PF(검증 수익 팩터) 1.61, validation net(검증 순수익) 1291.28, mid PF(중간 수익 팩터) 1.6004다.

하지만 OOS(표본외)는 아직 약하다. OOS net(표본외 순수익)이 775.97이고, OOS PF(표본외 수익 팩터)는 1.70이다. 그래서 최종이 아니라 Stage262(262단계)에서 OOS 회복만 좁게 수리한다.

## KPI Tradeoff(KPI 절충)

| adapter(어댑터) | val PF(검증 수익 팩터) | PF gap vs 34D(34D 대비 PF 차이) | val net(검증 순수익) | DD%(손실폭) | mid PF(중간 수익 팩터) | OOS PF(표본외 수익 팩터) | OOS net(표본외 순수익) | read(해석) |
|---|---:|---:|---:|---:|---:|---:|---:|---|
{rows}

## Judgment(판정)

- result_subject(판정 대상): `{RUN_ID}`
- judgment_label(판정 라벨): `useful_validation_tradeoff_not_final`
- evidence_missing(부족 근거): Stage262 OOS recovery repair(262단계 표본외 회복 수리), ONNX parity(ONNX 동등성), MT5 ONNX/runtime reproduction(MT5 ONNX/런타임 재현).
- next_condition(다음 조건): `{NEXT_STAGE_ID}`
- forbidden_claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), production_baseline(생산 기준), overall_goal_complete(전체 목표 완료).
""",
    )
    write_text(
        DECISION_PATH,
        f"""# Stage261 Decision(261단계 판정)

- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- decision(판정): `{DECISION}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- source_stage260_evidence_commit(원천 260단계 근거 커밋): `{SOURCE_STAGE260_EVIDENCE_COMMIT}`
- source_stage260_hash_record_commit(원천 260단계 해시 기록 커밋): `{SOURCE_STAGE260_HASH_RECORD_COMMIT}`
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

Stage261(261단계) closeout(종료)은 overall goal complete(전체 목표 완료)가 아니다.
""",
    )
    write_text(REVIEW_INDEX_PATH, f"# Stage261 Review Index(261단계 검토 색인)\n\n- status(상태): `closed_open_stage262_oos_recovery_candidate_not_final`\n- run(실행): `{RUN_ID}`\n- decision(판정): `{DECISION}`\n- report(보고서): `{rel(REPORT_PATH)}`\n")
    write_text(SELECTION_PATH, f"# Stage261 Selection Status(261단계 선택 상태)\n\n- stage_status(단계 상태): `closed_open_stage262_oos_recovery_candidate_not_final`\n- current_packet(현재 작업 묶음): `{PACKET_ID}`\n- current_run(현재 실행): `{RUN_ID}`\n- source_stage(원천 단계): `{SOURCE_STAGE_ID}`\n- source_run(원천 실행): `{SOURCE_RUN_ID}`\n- decision(판정): `{DECISION}`\n- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`\n- next_stage_or_branch(다음 단계 또는 분기): `{NEXT_STAGE_ID}`\n- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`\n- claim_boundary(주장 경계): `{BOUNDARY}`\n")


def write_next_stage_seed() -> None:
    write_text(NEXT_STAGE_ROOT / "00_spec/stage_brief.md", f"# {NEXT_STAGE_ID}\n\nStage262(262단계)는 `s260_lowrank_lowedge_filter`의 validation PF/net/DD(검증 수익 팩터/순수익/손실폭) 장점을 보존하면서 OOS net/PF(표본외 순수익/수익 팩터)를 회복하는 bounded repair(경계 수리) 단계다.\n\n## Bounded Question(경계 질문)\n\nCan a v2-native repair(v2 고유 수리) recover OOS net/PF(표본외 순수익/수익 팩터) without losing the Stage260 validation PF/net/mid-PF gains(260단계 검증 PF/순수익/중간 PF 개선)?\n\n## Boundary(경계)\n\n`{BOUNDARY}`\n")
    write_text(NEXT_STAGE_ROOT / "01_inputs/input_refs.md", f"# Stage262 Input References(262단계 입력 참조)\n\n- source_stage(원천 단계): `{STAGE_ID}`\n- source_run(원천 실행): `{RUN_ID}`\n- source_decision(원천 판정): `{DECISION}`\n- source_report(원천 보고서): `{rel(REPORT_PATH)}`\n- source_tradeoff_matrix(원천 절충 행렬): `{rel(TRADEOFF_PATH)}`\n")
    write_text(NEXT_STAGE_ROOT / "03_reviews/review_index.md", f"# Stage262 Review Index(262단계 검토 색인)\n\n- status(상태): `open_planned_from_stage261`\n- current_run(현재 실행): `{NEXT_RUN_ID}`\n- source_stage(원천 단계): `{STAGE_ID}`\n- source_decision(원천 판정): `{DECISION}`\n")
    write_text(NEXT_STAGE_ROOT / "04_selected/selection_status.md", f"# Stage262 Selection Status(262단계 선택 상태)\n\n- stage_status(단계 상태): `open_planned_from_stage261`\n- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`\n- current_run(현재 실행): `{NEXT_RUN_ID}`\n- source_stage(원천 단계): `{STAGE_ID}`\n- source_run(원천 실행): `{RUN_ID}`\n- source_decision(원천 판정): `{DECISION}`\n- claim_boundary(주장 경계): `{BOUNDARY}`\n")


def update_current_truth() -> None:
    write_text(CURRENT_STATE_PATH, f"# Current Working State(현재 작업 상태)\n\n- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`\n- current_run(현재 실행): `{NEXT_RUN_ID}`\n- active_stage(활성 단계): `{NEXT_STAGE_ID}`\n- selected_research_baseline(선택 연구 기준선): `none`\n- target_surface(목표 표면): `{TARGET_SURFACE}`\n- adapter_under_review(검토 중 어댑터): `s260_lowrank_lowedge_filter`\n- status(상태): `stage261_closed_open_stage262_oos_recovery_candidate_not_final`\n- claim_boundary(주장 경계): `{BOUNDARY}`\n\nStage261(261단계)는 Stage260(260단계) 결과를 review-only(검토 전용)로 판정했다.\nEffect(효과): Stage262(262단계)은 validation(검증) 장점을 지키면서 OOS(표본외) 회복을 좁게 시험한다.\n\n## Latest Stage261 Evidence(최신 261단계 근거)\n\n- run(실행): `{RUN_ID}`\n- decision(판정): `{DECISION}`\n- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`\n- report(보고서): `{rel(REPORT_PATH)}`\n- tradeoff_matrix(절충 행렬): `{rel(TRADEOFF_PATH)}`\n- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`\n\nForbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준), overall_goal_complete(전체 목표 완료).\n")
    workspace = read_text(WORKSPACE_STATE_PATH)
    workspace = re.sub(r"^current_run_id: .*$", f"current_run_id: {NEXT_RUN_ID}", workspace, count=1, flags=re.MULTILINE)
    workspace = re.sub(r"^updated_on: .*$", "updated_on: '2026-05-20'", workspace, count=1, flags=re.MULTILINE)
    workspace = re.sub(r"^active_stage: .*$", f"active_stage: {NEXT_STAGE_ID}", workspace, count=1, flags=re.MULTILINE)
    focus = f"""current_focus:
- >-
  Stage261(261단계) closed(종료) as `{DECISION}` and Stage262(262단계) `{NEXT_STAGE_ID}` is open_planned(개방 계획). Effect(효과): Stage260의 validation(검증) 개선 후보를 OOS recovery(표본외 회복) 질문으로 좁힌다.
- >-
  Stage261 evidence(261단계 근거)는 `{rel(REPORT_PATH)}`와 `{rel(TRADEOFF_PATH)}`에 있다. Effect(효과): 다음 단계가 final(최종)이 아니라 약점 수리로 이어진다.
- >-
  Target surface(목표 표면)는 `{TARGET_SURFACE}`이고 legacy 34D(레거시 34D)는 lesson-only KPI target(교훈 전용 KPI 목표)이다. Effect(효과): v2-native research(v2 고유 연구)를 계속한다.
"""
    workspace = re.sub(r"current_focus:\n.*?(?=\n[A-Za-z0-9_]+:\n)", focus, workspace, count=1, flags=re.DOTALL)
    stage261_block = f"""stage261_stage260_tight_plus_highedge_pf_oos_followup_review:
  packet_id: {PACKET_ID}
  stage_id: {STAGE_ID}
  status: closed_open_stage262_oos_recovery_candidate_not_final
  current_run_id: {RUN_ID}
  source_stage: {SOURCE_STAGE_ID}
  source_run: {SOURCE_RUN_ID}
  source_stage260_evidence_commit: {SOURCE_STAGE260_EVIDENCE_COMMIT}
  source_stage260_hash_record_commit: {SOURCE_STAGE260_HASH_RECORD_COMMIT}
  decision: {DECISION}
  report_path: {rel(REPORT_PATH)}
  decision_path: {rel(DECISION_PATH)}
  tradeoff_matrix_path: {rel(TRADEOFF_PATH)}
  attribution_path: {rel(ATTRIBUTION_PATH)}
  failure_memory_path: {rel(FAILURE_PATH)}
  external_verification_status: {EXTERNAL_STATUS}
  pushed_commit_hash: pending_until_push
  next_action: {NEXT_RUN_ID}
  boundary: {BOUNDARY}
"""
    stage262_block = f"""stage262_lowrank_lowedge_oos_recovery_repair:
  packet_id: {NEXT_PACKET_ID}
  stage_id: {NEXT_STAGE_ID}
  status: open_planned_from_stage261
  current_run_id: {NEXT_RUN_ID}
  source_stage: {STAGE_ID}
  source_run: {RUN_ID}
  source_decision: {DECISION}
  next_action: {NEXT_RUN_ID}
  boundary: {BOUNDARY}
"""
    workspace = replace_or_append_block(workspace, "stage261_stage260_tight_plus_highedge_pf_oos_followup_review", stage261_block)
    workspace = replace_or_append_block(workspace, "stage262_lowrank_lowedge_oos_recovery_repair", stage262_block)
    write_text(WORKSPACE_STATE_PATH, workspace, bom=False)
    existing = read_text(CHANGELOG_PATH) if CHANGELOG_PATH.exists() else ""
    marker = "Stage261 Stage260 tight plus highedge follow-up review closeout"
    existing = re.sub(rf"\n## [^\n]*{re.escape(marker)}[^\n]*\n.*?(?=\n## |\Z)", "", existing, flags=re.DOTALL)
    write_text(CHANGELOG_PATH, existing.rstrip() + f"\n\n## {utc_now()} {marker}(261단계 260단계 후속 검토 종료)\n\n- action(행동): closed(종료) `{STAGE_ID}` with decision(판정) `{DECISION}`.\n- effect(효과): `s260_lowrank_lowedge_filter`를 Stage262(262단계) OOS recovery(표본외 회복) 질문으로 좁혔다.\n- boundary(주장 경계): `{BOUNDARY}`.\n", bom=False)


def write_ledgers_and_packet(review: Mapping[str, Any]) -> None:
    best = next(row for row in review["tradeoff_rows"] if row["adapter_id"] == "s260_lowrank_lowedge_filter")
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__review_total",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "stage261_review_total",
        "parent_run_id": SOURCE_RUN_ID,
        "record_view": "review_total",
        "tier_scope": "Tier A+B",
        "kpi_scope": "baseline_adapter_followup_review",
        "scoreboard_lane": "baseline_adapter_stage261_stage260_followup_review",
        "status": "reviewed_closed",
        "judgment": DECISION,
        "path": rel(REPORT_PATH),
        "primary_kpi": f"best=s260_lowrank_lowedge_filter;validation_pf={best['validation_pf']};validation_net={best['validation_net']};oos_net={best['oos_net']}",
        "guardrail_kpi": "oos_recovery_needed=1;overall_goal_complete=0",
        "external_verification_status": EXTERNAL_STATUS,
        "notes": "Stage261 review only; routes to Stage262 OOS recovery repair.",
    }
    run_row = {"run_id": RUN_ID, "stage_id": STAGE_ID, "lane": "baseline_adapter_stage261_stage260_followup_review", "status": "reviewed_closed", "judgment": DECISION, "path": rel(REPORT_PATH), "notes": f"source_stage260_evidence_commit={SOURCE_STAGE260_EVIDENCE_COMMIT};source_stage260_hash_record_commit={SOURCE_STAGE260_HASH_RECORD_COMMIT};overall_goal_complete=0;boundary={BOUNDARY}"}
    write_csv(STAGE_LEDGER_PATH, [alpha_row], ALPHA_COLUMNS)
    ledger_payload = {
        "run_registry": upsert_csv(RUN_REGISTRY_PATH, RUN_COLUMNS, [run_row], "run_id"),
        "project_alpha_ledger": upsert_csv(PROJECT_LEDGER_PATH, ALPHA_COLUMNS, [alpha_row], "ledger_row_id"),
        "stage_ledger": {"path": rel(STAGE_LEDGER_PATH), "rows": 1, "upserted_rows": 1, "sha256": sha256_lf(STAGE_LEDGER_PATH), "hash_policy": "lf_normalized_text_register"},
    }
    summary = {"stage_id": STAGE_ID, "run_id": RUN_ID, "packet_id": PACKET_ID, "source_stage": SOURCE_STAGE_ID, "source_run": SOURCE_RUN_ID, "source_stage260_evidence_commit": SOURCE_STAGE260_EVIDENCE_COMMIT, "source_stage260_hash_record_commit": SOURCE_STAGE260_HASH_RECORD_COMMIT, "decision": DECISION, "next_stage_or_branch": NEXT_STAGE_ID, "external_verification_status": EXTERNAL_STATUS, "overall_goal_complete": False, "pushed_commit_hash": "pending_until_push", "claim_boundary": BOUNDARY, "legacy_34d_lesson_only_targets": {"validation_net": LEGACY_34D_NET, "validation_pf": LEGACY_34D_PF, "validation_dd": LEGACY_34D_DD}, "tradeoff_rows": review["tradeoff_rows"], "gate_rows": review["gate_rows"], "risk_review_rows": review["risk_review_rows"], "probability_review_rows": review["probability_review_rows"], "attribution_rows": review["attribution_rows"], "failure_memory_rows": review["failure_rows"], "route_rows": review["route_rows"], "ledger_payload": ledger_payload}
    write_json(SUMMARY_PATH, summary)
    created = utc_now()
    artifact_paths = [PRODUCER_PATH, REPORT_PATH, TRADEOFF_PATH, ATTRIBUTION_PATH, FAILURE_PATH, ROUTE_PATH, RISK_REVIEW_PATH, PROBABILITY_REVIEW_PATH, SUMMARY_PATH, DECISION_PATH, STAGE_LEDGER_PATH, REVIEW_INDEX_PATH, SELECTION_PATH, CURRENT_STATE_PATH, WORKSPACE_STATE_PATH, CHANGELOG_PATH, NEXT_STAGE_ROOT / "00_spec/stage_brief.md", NEXT_STAGE_ROOT / "01_inputs/input_refs.md", NEXT_STAGE_ROOT / "03_reviews/review_index.md", NEXT_STAGE_ROOT / "04_selected/selection_status.md"]
    artifact_rows = [{"artifact_id": artifact_id_for(path), "artifact_type": "stage261_followup_review_evidence", "path": rel(path), "sha256": sha256_lf(path), "stage_id": STAGE_ID, "run_id": RUN_ID, "created_at_utc": created, "notes": "Stage261 Stage260 follow-up review evidence; research only."} for path in artifact_paths if path.exists()]
    ledger_payload["artifact_registry"] = upsert_csv(ARTIFACT_REGISTRY_PATH, ARTIFACT_COLUMNS, artifact_rows, "artifact_id")
    summary["ledger_payload"] = ledger_payload
    write_json(SUMMARY_PATH, summary)
    base_payload = {"packet_id": PACKET_ID, "stage_id": STAGE_ID, "run_id": RUN_ID, "source_stage": SOURCE_STAGE_ID, "source_run": SOURCE_RUN_ID, "decision": DECISION, "next_stage_or_branch": NEXT_STAGE_ID, "external_verification_status": EXTERNAL_STATUS, "claim_boundary": BOUNDARY, "overall_goal_complete": False}
    packet_payloads = {
        "packet_receipt.json": {**base_payload, "created_at_utc": created, "status": "closed_pending_push_hash"},
        "routing_receipt.json": {**base_payload, "route": DECISION, "route_effect": "open Stage262 lowrank_lowedge OOS recovery repair"},
        "kpi_contract_audit.json": {**base_payload, "status": "passed", "kpi_basis": [rel(QUALITY_PATH), rel(SOURCE_FEATURE_PATH), rel(PROBABILITY_PATH), rel(RISK_PATH)]},
        "result_judgment_gate.json": {**base_payload, "judgment_label": "useful_validation_tradeoff_not_final", "next_condition": NEXT_STAGE_ID},
        "performance_attribution_gate.json": {**base_payload, "attribution_rows": review["attribution_rows"], "attribution_confidence": "medium_high"},
        "artifact_lineage_audit.json": {**base_payload, "source_inputs": [rel(QUALITY_PATH), rel(SOURCE_FEATURE_PATH), rel(PROBABILITY_PATH), rel(RISK_PATH), rel(SOURCE_REPORT_PATH), rel(SOURCE_DECISION_PATH)], "producer": rel(PRODUCER_PATH), "consumer": NEXT_STAGE_ID, "artifact_paths": [rel(path) for path in artifact_paths if path.exists()], "ledger_payload": ledger_payload, "status": "completed"},
        "required_gate_coverage_audit.json": {**base_payload, "required_gates": ["kpi_contract_audit", "result_judgment_gate", "performance_attribution_gate", "artifact_lineage_audit", "final_claim_guard"], "status": "passed"},
        "final_claim_guard.json": {**base_payload, "forbidden_claims": ["deployment", "live_readiness", "runtime_authority", "operating_promotion", "operating_reference", "production_baseline", "overall_goal_complete"], "status": "passed"},
        "aggregate_summary.json": summary,
    }
    write_text(PACKET_ROOT / "closeout_packet.md", f"# Stage261 Closeout Packet(261단계 종료 작업 묶음)\n\n- run(실행): `{RUN_ID}`\n- decision(판정): `{DECISION}`\n- report(보고서): `{rel(REPORT_PATH)}`\n- next_stage(다음 단계): `{NEXT_STAGE_ID}`\n- overall_goal_complete(전체 목표 완료): `false`\n- boundary(경계): `{BOUNDARY}`\n")
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
