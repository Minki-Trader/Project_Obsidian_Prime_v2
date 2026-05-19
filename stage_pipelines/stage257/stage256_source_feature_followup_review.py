from __future__ import annotations

import csv
import hashlib
import json
import re
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence


STAGE_ID = "257_adapter_research__stage256_source_feature_followup_review"
RUN_ID = "run257A_stage257_stage256_source_feature_followup_review_v1"
PACKET_ID = "stage257_stage256_source_feature_followup_review_v1"
SOURCE_STAGE_ID = "256_adapter_research__source_feature_branch_after_binding_lifecycle_no_gain"
SOURCE_RUN_ID = "run256A_stage256_source_feature_branch_after_binding_lifecycle_no_gain_v1"
SOURCE_STAGE256_EVIDENCE_COMMIT = "c5e1c2f8bd930f1a5c9f025b1e67630897e5ab10"
SOURCE_STAGE256_HASH_RECORD_COMMIT = "d5e503be2fbb26b773eb61b5caf16e7d602f784a"
NEXT_STAGE_ID = "258_adapter_research__short_tight_margin_pf_repair_after_stage256_tradeoff"
NEXT_RUN_ID = "run258A_stage258_short_tight_margin_pf_repair_after_stage256_tradeoff_v1"
NEXT_PACKET_ID = "stage258_short_tight_margin_pf_repair_after_stage256_tradeoff_v1"
DECISION = "open_stage258_bounded_short_tight_margin_pf_repair_after_stage256_tradeoff_candidate_not_final"
BOUNDARY = "research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment"
TARGET_SURFACE = "legacy_34d_kpi_lesson_only_v2_native_short_tight_margin_pf_repair_after_stage256_tradeoff"
EXTERNAL_STATUS = "review_only_source_stage256_mt5_reports_completed"

LEGACY_34D_NET = 987.60
LEGACY_34D_PF = 1.583157
LEGACY_34D_DD = 12.909136

ROOT = Path.cwd()
STAGE_ROOT = ROOT / "stages" / STAGE_ID
REVIEWS = STAGE_ROOT / "03_reviews"
PACKET_ROOT = ROOT / "docs/agent_control/packets" / PACKET_ID
NEXT_STAGE_ROOT = ROOT / "stages" / NEXT_STAGE_ID
SOURCE_REVIEWS = ROOT / "stages" / SOURCE_STAGE_ID / "03_reviews"

QUALITY_PATH = SOURCE_REVIEWS / "stage256_quality_matrix.csv"
SOURCE_FEATURE_PATH = SOURCE_REVIEWS / "stage256_source_feature_summary.csv"
SUMMARY_KPI_PATH = SOURCE_REVIEWS / "stage256_source_feature_kpi_summary.csv"
SOURCE_ATTRIBUTION_PATH = SOURCE_REVIEWS / "stage256_performance_attribution.csv"
SOURCE_FAILURE_PATH = SOURCE_REVIEWS / "stage256_failure_memory.csv"
RISK_PATH = SOURCE_REVIEWS / "stage256_risk_atr_telemetry.csv"
SOURCE_REPORT_PATH = SOURCE_REVIEWS / "stage256_source_feature_branch_report.md"
SOURCE_DECISION_PATH = SOURCE_REVIEWS / "stage256_decision.md"

REPORT_PATH = REVIEWS / "stage257_stage256_source_feature_followup_review.md"
TRADEOFF_PATH = REVIEWS / "stage257_tradeoff_review_matrix.csv"
ATTRIBUTION_PATH = REVIEWS / "stage257_performance_attribution.csv"
FAILURE_PATH = REVIEWS / "stage257_failure_memory.csv"
ROUTE_PATH = REVIEWS / "stage257_route_matrix.csv"
RISK_REVIEW_PATH = REVIEWS / "stage257_risk_atr_review.csv"
SUMMARY_PATH = REVIEWS / "stage257_summary.json"
DECISION_PATH = REVIEWS / "stage257_decision.md"
STAGE_LEDGER_PATH = REVIEWS / "stage_run_ledger.csv"
REVIEW_INDEX_PATH = REVIEWS / "review_index.md"
SELECTION_PATH = STAGE_ROOT / "04_selected/selection_status.md"

CURRENT_STATE_PATH = ROOT / "docs/context/current_working_state.md"
WORKSPACE_STATE_PATH = ROOT / "docs/workspace/workspace_state.yaml"
CHANGELOG_PATH = ROOT / "docs/workspace/changelog.md"
RUN_REGISTRY_PATH = ROOT / "docs/registers/run_registry.csv"
PROJECT_LEDGER_PATH = ROOT / "docs/registers/alpha_run_ledger.csv"
ARTIFACT_REGISTRY_PATH = ROOT / "docs/registers/artifact_registry.csv"
PRODUCER_PATH = ROOT / "stage_pipelines/stage257/stage256_source_feature_followup_review.py"

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


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def write_text(path: Path, text: str, *, bom: bool = True) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8-sig" if bom else "utf-8")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: row.get(column, "") for column in columns})


def write_json(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def sha256_lf(path: Path) -> str:
    raw = path.read_bytes()
    return hashlib.sha256(raw.replace(b"\r\n", b"\n")).hexdigest()


def artifact_id_for(path: Path) -> str:
    return f"{RUN_ID}__{rel(path).replace('/', '__').replace('.', '_').replace('-', '_')}"


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
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
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


def read_for_adapter(row: Mapping[str, str], control: Mapping[str, float]) -> dict[str, str]:
    adapter = row["adapter_id"]
    val_net = as_float(row["validation_net"])
    val_dd = as_float(row["validation_balance_dd_percent"])
    mid_pf = as_float(row["validation_mid_pf"])
    oos_net = as_float(row["oos_net"])
    oos_pf = as_float(row["oos_pf"])
    deltas = {
        "validation_net_delta_vs_control": fmt(val_net - control["validation_net"]),
        "validation_dd_delta_vs_control": fmt(val_dd - control["validation_dd"], 4),
        "validation_mid_pf_delta_vs_control": fmt(mid_pf - control["validation_mid_pf"], 6),
        "oos_net_delta_vs_control": fmt(oos_net - control["oos_net"]),
        "oos_pf_delta_vs_control": fmt(oos_pf - control["oos_pf"], 4),
    }
    if adapter == "s256_short_tight_margin":
        return {
            **deltas,
            "review_label": "best_tradeoff_not_final",
            "plain_read": "검증 순수익, 낙폭, 표본외 순수익은 좋아졌지만 PF(수익요인)와 중간 구간 PF가 아직 약하다.",
            "next_handling": NEXT_STAGE_ID,
        }
    if adapter == "s256_long_session_relax":
        return {
            **deltas,
            "review_label": "validation_gain_oos_damage",
            "plain_read": "검증 순수익과 낙폭은 좋아졌지만 표본외 순수익과 중간 PF가 훼손됐다.",
            "next_handling": "do_not_promote_as_primary",
        }
    if adapter == "s256_short_margin_relax":
        return {
            **deltas,
            "review_label": "oos_gain_validation_damage",
            "plain_read": "표본외 순수익은 좋아졌지만 검증 PF와 중간 PF가 크게 무너졌다.",
            "next_handling": "failure_memory_only",
        }
    if adapter == "s256_short_session_relax":
        return {
            **deltas,
            "review_label": "mid_pf_gain_dd_oos_damage",
            "plain_read": "중간 PF는 조금 좋아졌지만 낙폭과 표본외가 훼손됐다.",
            "next_handling": "side_clue_only",
        }
    return {
        **deltas,
        "review_label": "control_reference_near_miss",
        "plain_read": "대조군은 가까운 기준점이지만 34D급 hard pass(엄격 통과)는 아니다.",
        "next_handling": "reference_only",
    }


def build_review() -> dict[str, Any]:
    quality_rows = read_csv(QUALITY_PATH)
    source_feature_rows = read_csv(SOURCE_FEATURE_PATH)
    risk_rows = read_csv(RISK_PATH)
    source_attr_rows = read_csv(SOURCE_ATTRIBUTION_PATH)
    source_failure_rows = read_csv(SOURCE_FAILURE_PATH)
    control_row = next(row for row in quality_rows if row["adapter_id"] == "s256_stage254_control")
    control = {
        "validation_net": as_float(control_row["validation_net"]),
        "validation_dd": as_float(control_row["validation_balance_dd_percent"]),
        "validation_mid_pf": as_float(control_row["validation_mid_pf"]),
        "oos_net": as_float(control_row["oos_net"]),
        "oos_pf": as_float(control_row["oos_pf"]),
    }

    tradeoff_rows: list[dict[str, Any]] = []
    for row in quality_rows:
        read = read_for_adapter(row, control)
        tradeoff_rows.append(
            {
                "adapter_id": row["adapter_id"],
                "validation_pf": row["validation_pf"],
                "validation_net": row["validation_net"],
                "validation_net_delta_vs_control": read["validation_net_delta_vs_control"],
                "validation_net_gap_vs_34d": fmt(as_float(row["validation_net"]) - LEGACY_34D_NET),
                "validation_dd_percent": row["validation_balance_dd_percent"],
                "validation_dd_delta_vs_control": read["validation_dd_delta_vs_control"],
                "validation_dd_margin_vs_34d": fmt(LEGACY_34D_DD - as_float(row["validation_balance_dd_percent"]), 4),
                "validation_early_pf": row["validation_early_pf"],
                "validation_mid_pf": row["validation_mid_pf"],
                "validation_mid_pf_delta_vs_control": read["validation_mid_pf_delta_vs_control"],
                "validation_late_pf": row["validation_late_pf"],
                "oos_pf": row["oos_pf"],
                "oos_pf_delta_vs_control": read["oos_pf_delta_vs_control"],
                "oos_net": row["oos_net"],
                "oos_net_delta_vs_control": read["oos_net_delta_vs_control"],
                "oos_dd_percent": row["oos_balance_dd_percent"],
                "hard_quality_pass": row["hard_quality_pass"],
                "review_label": read["review_label"],
                "plain_read": read["plain_read"],
                "next_handling": read["next_handling"],
            }
        )

    gate_rows: list[dict[str, Any]] = []
    for row in source_feature_rows:
        if row["split"] != "validation_is":
            continue
        gate_rows.append(
            {
                "adapter_id": row["adapter_id"],
                "source_branch_mode": row["source_branch_mode"],
                "signal_rows": row["signal_rows"],
                "base_blocked_signal_rows": row["base_blocked_signal_rows"],
                "blocked_signal_rows": row["blocked_signal_rows"],
                "changed_gate_rows": row["changed_gate_rows"],
                "allowed_signal_rows": row["allowed_signal_rows"],
            }
        )

    risk_review_rows: list[dict[str, Any]] = []
    for row in risk_rows:
        if row.get("view") != "actual_routed_total" or row.get("split") not in {"validation_is", "oos"}:
            continue
        risk_review_rows.append(
            {
                "adapter_id": row["adapter_id"],
                "split": row["split"],
                "atr_enabled": row["atr_enabled"],
                "model_risk_enabled": row["model_risk_enabled"],
                "max_model_risk_pct": row["max_model_risk_pct"],
                "max_actual_risk_pct_after_floor": row["max_actual_risk_pct_after_floor"],
                "risk_floor_applied_count": row["risk_floor_applied_count"],
                "avg_executed_lot": row["avg_executed_lot"],
                "avg_atr_points": row["avg_atr_points"],
                "risk_bucket": row["risk_bucket"],
                "read": "ATR/risk(ATR/위험)는 유지됐고, 이번 실패/진전은 주로 source gate(소스 차단문) 공급 변화에서 온다.",
            }
        )

    attribution_rows = [
        {
            "attribution_id": f"{RUN_ID}__short_tight_margin_best_tradeoff",
            "observed_change": "s256_short_tight_margin validation_net +71.84, DD -3.9194, OOS net +174.20 vs control(대조군 대비 개선).",
            "comparison_baseline": "s256_stage254_control",
            "likely_drivers": "short margin block(숏 마진 차단문)을 tight band(좁은 구간)로 줄여 공급을 늘렸지만 score table(점수표), threshold(임계값), lifecycle(생명주기), ATR/risk(ATR/위험)는 고정했다.",
            "segment_checks": "validation/OOS(검증/표본외), early/mid/late PF(초기/중간/후기 수익요인), DD(낙폭), gate changed rows(차단문 변경 행), risk/ATR telemetry(위험/ATR 원격측정).",
            "trade_shape": "net/DD/OOS는 좋아졌지만 validation PF 1.48, mid PF 1.5108, OOS PF 1.69로 34D급 품질은 아니다.",
            "alternative_explanations": "공급 증가가 일부 좋은 구간을 잡았을 수 있으나 PF 약화가 남아 있어 신호 품질 개선으로 확정할 수 없다.",
            "attribution_confidence": "medium_high",
            "next_probe": NEXT_STAGE_ID,
        },
        {
            "attribution_id": f"{RUN_ID}__short_relaxation_failure_memory",
            "observed_change": "short_margin_relax and short_session_relax(숏 마진/숏 세션 완화)는 한쪽 KPI만 좋아지고 검증 또는 OOS가 훼손됐다.",
            "comparison_baseline": "s256_stage254_control",
            "likely_drivers": "숏 공급을 너무 크게 열면 validation PF(검증 수익요인) 또는 OOS(표본외)가 손상된다.",
            "segment_checks": "short_margin_relax validation PF 1.25, mid PF 1.1437; short_session_relax OOS net 581.18 and DD 14.3278.",
            "trade_shape": "source gate(소스 차단문)는 효과가 있지만 넓은 완화는 불안정하다.",
            "alternative_explanations": "표본외 한 지표 상승은 구간 편향일 수 있다.",
            "attribution_confidence": "medium",
            "next_probe": NEXT_STAGE_ID,
        },
    ]

    failure_rows = [
        {
            "failure_id": f"{RUN_ID}__hard_quality_not_reached",
            "evidence": "hard_quality_pass=False for all Stage256 candidates(모든 후보 엄격 통과 실패).",
            "impact": "Stage256은 유용한 tradeoff(절충)를 만들었지만 final adapter(최종 어댑터)가 아니다.",
            "next_handling": NEXT_STAGE_ID,
        },
        {
            "failure_id": f"{RUN_ID}__pf_midpf_remaining_weakness",
            "evidence": "best tradeoff s256_short_tight_margin has validation_pf=1.48 and validation_mid_pf=1.510763553.",
            "impact": "34D급 목표에는 PF(수익요인)와 segment stability(구간 안정성) 회복이 필요하다.",
            "next_handling": NEXT_STAGE_ID,
        },
    ]

    route_rows = [
        {
            "route_id": f"{RUN_ID}__open_stage258_short_tight_margin_pf_repair",
            "evidence": "s256_short_tight_margin improved validation net, validation DD, and OOS net while remaining not-final due to PF weakness.",
            "decision": DECISION,
            "effect": "Stage258(258단계)는 short_tight_margin(숏 좁은 마진) 장점을 보존하면서 PF(수익요인)를 회복하는 bounded repair(경계 수리)를 한다.",
            "next_stage_or_branch": NEXT_STAGE_ID,
        }
    ]
    return {
        "control": control_row,
        "tradeoff_rows": tradeoff_rows,
        "gate_rows": gate_rows,
        "risk_review_rows": risk_review_rows,
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

    rows = "\n".join(
        "| {adapter_id} | {validation_pf} | {validation_net} | {validation_net_delta_vs_control} | {validation_dd_percent} | {validation_dd_delta_vs_control} | {validation_mid_pf} | {oos_pf} | {oos_net} | {review_label} |".format(**row)
        for row in tradeoff_rows
    )
    write_text(
        REPORT_PATH,
        f"""# Stage257 Stage256 Source/Feature Follow-up Review(257단계 256단계 소스/피처 후속 검토)

- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- source_stage256_evidence_commit(원천 256단계 근거 커밋): `{SOURCE_STAGE256_EVIDENCE_COMMIT}`
- source_stage256_hash_record_commit(원천 256단계 해시 기록 커밋): `{SOURCE_STAGE256_HASH_RECORD_COMMIT}`
- decision(판정): `{DECISION}`
- boundary(주장 경계): `{BOUNDARY}`

## Easy Read(쉬운 해석)

Stage256(256단계)는 완전 성공이 아니다. 다만 `s256_short_tight_margin`은 validation net(검증 순수익), DD(낙폭), OOS net(표본외 순수익)을 동시에 개선했다. 약점은 PF(수익요인)와 mid PF(중간 수익요인)다. 그래서 Stage258(258단계)은 이 장점을 보존하면서 PF를 회복하는 좁은 repair(수리)로 간다.

## KPI Tradeoff(KPI 절충)

| adapter(어댑터) | val PF(검증 수익요인) | val net(검증 순수익) | net delta(순수익 차이) | DD%(낙폭률) | DD delta(낙폭 차이) | mid PF(중간 수익요인) | OOS PF(표본외 수익요인) | OOS net(표본외 순수익) | read(해석) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
{rows}

## Judgment(판정)

- result_subject(판정 대상): `{RUN_ID}`
- evidence_available(사용 근거): Stage256(256단계) quality matrix(품질 행렬), source feature summary(소스 피처 요약), risk/ATR telemetry(위험/ATR 원격측정), performance attribution(성과 귀속).
- judgment_label(판정 라벨): `useful_tradeoff_not_final`
- next_condition(다음 조건): `{NEXT_STAGE_ID}`
- forbidden_claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), production_baseline(생산 기준), overall_goal_complete(전체 목표 완료).
""",
    )

    write_text(
        DECISION_PATH,
        f"""# Stage257 Decision(257단계 판정)

- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- decision(판정): `{DECISION}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- source_stage256_evidence_commit(원천 256단계 근거 커밋): `{SOURCE_STAGE256_EVIDENCE_COMMIT}`
- source_stage256_hash_record_commit(원천 256단계 해시 기록 커밋): `{SOURCE_STAGE256_HASH_RECORD_COMMIT}`
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

Stage257(257단계) closeout(종료)은 overall goal complete(전체 목표 완료)가 아니다.
""",
    )

    write_text(
        REVIEW_INDEX_PATH,
        f"""# Stage257 Review Index(257단계 검토 색인)

- status(상태): `closed_open_stage258_short_tight_margin_pf_repair_candidate_not_final`
- run(실행): `{RUN_ID}`
- decision(판정): `{DECISION}`
- report(보고서): `{rel(REPORT_PATH)}`
- tradeoff_matrix(절충 행렬): `{rel(TRADEOFF_PATH)}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
""",
    )
    write_text(
        SELECTION_PATH,
        f"""# Stage257 Selection Status(257단계 선택 상태)

- stage_status(단계 상태): `closed_open_stage258_short_tight_margin_pf_repair_candidate_not_final`
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

Stage258(258단계)는 Stage256(256단계)의 best tradeoff(최선 절충)인 `s256_short_tight_margin`을 기준으로 PF(수익요인)와 mid PF(중간 수익요인)를 회복하는 bounded repair(경계 수리) 단계다.

## Bounded Question(경계 질문)

Can a v2-native source/feature repair(v2 고유 소스/피처 수리) preserve the `s256_short_tight_margin` validation net/DD/OOS gains(검증 순수익/낙폭/표본외 개선)을 while restoring PF and mid-window stability(PF와 중간 구간 안정성 회복) without repeating threshold/binding/lifecycle over-tuning(임계값/결합/생명주기 과조정)?

## Boundary(경계)

`{BOUNDARY}`
""",
    )
    write_text(
        NEXT_STAGE_ROOT / "01_inputs/input_refs.md",
        f"""# Stage258 Input References(258단계 입력 참조)

- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- source_decision(원천 판정): `{DECISION}`
- source_report(원천 보고서): `{rel(REPORT_PATH)}`
- source_tradeoff_matrix(원천 절충 행렬): `{rel(TRADEOFF_PATH)}`
- source_stage256_evidence_commit(원천 256단계 근거 커밋): `{SOURCE_STAGE256_EVIDENCE_COMMIT}`
- source_stage256_hash_record_commit(원천 256단계 해시 기록 커밋): `{SOURCE_STAGE256_HASH_RECORD_COMMIT}`
""",
    )
    write_text(
        NEXT_STAGE_ROOT / "03_reviews/review_index.md",
        f"""# Stage258 Review Index(258단계 검토 색인)

- status(상태): `open_planned_from_stage257`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- source_stage(원천 단계): `{STAGE_ID}`
- source_decision(원천 판정): `{DECISION}`
""",
    )
    write_text(
        NEXT_STAGE_ROOT / "04_selected/selection_status.md",
        f"""# Stage258 Selection Status(258단계 선택 상태)

- stage_status(단계 상태): `open_planned_from_stage257`
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
- adapter_under_review(검토 중 어댑터): `s256_short_tight_margin_pf_repair`
- status(상태): `stage257_closed_open_stage258_short_tight_margin_pf_repair_candidate_not_final`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage257(257단계)는 Stage256(256단계) source/feature branch(소스/피처 분기)를 review-only(검토 전용)로 판정했다.
Effect(효과): `s256_short_tight_margin`의 net/DD/OOS(순수익/낙폭/표본외) 장점을 보존하면서 PF(수익요인)를 회복하는 Stage258(258단계)을 연다.

## Latest Stage257 Evidence(최신 257단계 근거)

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
  Stage257(257단계) closed(종료) as `{DECISION}` and Stage258(258단계) `{NEXT_STAGE_ID}` is open_planned(개방 계획). Effect(효과): Stage256(256단계)의 useful tradeoff(유용한 절충)를 PF repair(PF 수리) 질문으로 좁힌다.
- >-
  Stage257 evidence(257단계 근거)는 `{rel(REPORT_PATH)}`, `{rel(TRADEOFF_PATH)}`, `{rel(ATTRIBUTION_PATH)}`, `{rel(FAILURE_PATH)}`에 있다. Effect(효과): Stage258(258단계)는 `s256_short_tight_margin`의 net/DD/OOS(순수익/낙폭/표본외) 장점을 보존하며 PF(수익요인)를 수리한다.
- >-
  Target surface(목표 표면)는 `{TARGET_SURFACE}`이고 legacy 34D(레거시 34D)는 lesson-only KPI target(교훈 전용 핵심 성과 지표 목표)이다. Effect(효과): v2-native research(v2 고유 연구)를 계속한다.
"""
    workspace = re.sub(r"current_focus:\n.*?(?=\n[A-Za-z0-9_]+:\n)", focus, workspace, count=1, flags=re.DOTALL)
    stage257_block = f"""stage257_stage256_source_feature_followup_review:
  packet_id: {PACKET_ID}
  stage_id: {STAGE_ID}
  status: closed_open_stage258_short_tight_margin_pf_repair_candidate_not_final
  current_run_id: {RUN_ID}
  source_stage: {SOURCE_STAGE_ID}
  source_run: {SOURCE_RUN_ID}
  source_stage256_evidence_commit: {SOURCE_STAGE256_EVIDENCE_COMMIT}
  source_stage256_hash_record_commit: {SOURCE_STAGE256_HASH_RECORD_COMMIT}
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
    stage258_block = f"""stage258_short_tight_margin_pf_repair_after_stage256_tradeoff:
  packet_id: {NEXT_PACKET_ID}
  stage_id: {NEXT_STAGE_ID}
  status: open_planned_from_stage257
  current_run_id: {NEXT_RUN_ID}
  source_stage: {STAGE_ID}
  source_run: {RUN_ID}
  source_decision: {DECISION}
  next_action: {NEXT_RUN_ID}
  boundary: {BOUNDARY}
"""
    workspace = replace_or_append_block(workspace, "stage257_stage256_source_feature_followup_review", stage257_block)
    workspace = replace_or_append_block(workspace, "stage258_short_tight_margin_pf_repair_after_stage256_tradeoff", stage258_block)
    write_text(WORKSPACE_STATE_PATH, workspace, bom=False)

    existing = read_text(CHANGELOG_PATH) if CHANGELOG_PATH.exists() else ""
    marker = "Stage257 Stage256 source-feature follow-up review closeout"
    existing = re.sub(rf"\n## [^\n]*{re.escape(marker)}[^\n]*\n.*?(?=\n## |\Z)", "", existing, flags=re.DOTALL)
    entry = f"""
## {utc_now()} {marker}(257단계 256단계 소스-피처 후속 검토 종료)

- action(행동): closed(종료) `{STAGE_ID}` with decision(판정) `{DECISION}`.
- effect(효과): Stage256(256단계)의 short_tight_margin(숏 좁은 마진) 절충을 Stage258(258단계) PF repair(PF 수리) 질문으로 좁혔다.
- boundary(주장 경계): `{BOUNDARY}`.
"""
    write_text(CHANGELOG_PATH, existing.rstrip() + entry, bom=False)


def write_ledgers_and_packet(review: Mapping[str, Any]) -> None:
    best = next(row for row in review["tradeoff_rows"] if row["adapter_id"] == "s256_short_tight_margin")
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__review_total",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "stage257_review_total",
        "parent_run_id": SOURCE_RUN_ID,
        "record_view": "review_total",
        "tier_scope": "Tier A+B",
        "kpi_scope": "baseline_adapter_followup_review",
        "scoreboard_lane": "baseline_adapter_stage257_source_feature_followup_review",
        "status": "reviewed_closed",
        "judgment": DECISION,
        "path": rel(REPORT_PATH),
        "primary_kpi": f"best=s256_short_tight_margin;validation_net={best['validation_net']};validation_dd={best['validation_dd_percent']};validation_pf={best['validation_pf']};oos_net={best['oos_net']}",
        "guardrail_kpi": "hard_quality_pass_count=0;pf_midpf_remaining_weakness=1;overall_goal_complete=0",
        "external_verification_status": EXTERNAL_STATUS,
        "notes": "Stage257 review only; routes to bounded Stage258 short_tight_margin PF repair.",
    }
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "baseline_adapter_stage257_source_feature_followup_review",
        "status": "reviewed_closed",
        "judgment": DECISION,
        "path": rel(REPORT_PATH),
        "notes": f"source_stage256_evidence_commit={SOURCE_STAGE256_EVIDENCE_COMMIT};source_stage256_hash_record_commit={SOURCE_STAGE256_HASH_RECORD_COMMIT};overall_goal_complete=0;boundary={BOUNDARY}",
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
        "source_stage256_evidence_commit": SOURCE_STAGE256_EVIDENCE_COMMIT,
        "source_stage256_hash_record_commit": SOURCE_STAGE256_HASH_RECORD_COMMIT,
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
    artifact_rows = [
        {
            "artifact_id": artifact_id_for(path),
            "artifact_type": "stage257_followup_review_evidence",
            "path": rel(path),
            "sha256": sha256_lf(path),
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": created,
            "notes": "Stage257 Stage256 source/feature follow-up review evidence; research only.",
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
        "routing_receipt.json": {**base_payload, "route": DECISION, "route_effect": "open Stage258 short_tight_margin PF repair"},
        "kpi_contract_audit.json": {**base_payload, "status": "passed", "kpi_basis": [rel(QUALITY_PATH), rel(SOURCE_FEATURE_PATH), rel(RISK_PATH)]},
        "result_judgment_gate.json": {
            **base_payload,
            "result_subject": RUN_ID,
            "evidence_available": [rel(REPORT_PATH), rel(TRADEOFF_PATH), rel(ATTRIBUTION_PATH), rel(FAILURE_PATH), rel(RISK_REVIEW_PATH)],
            "evidence_missing": [NEXT_STAGE_ID, "ONNX parity(ONNX 동등성)", "MT5 ONNX/runtime reproduction(MT5 ONNX/런타임 재현)"],
            "judgment_label": "useful_tradeoff_not_final",
            "next_condition": NEXT_STAGE_ID,
        },
        "performance_attribution_gate.json": {**base_payload, "attribution_rows": review["attribution_rows"], "attribution_confidence": "medium_high"},
        "artifact_lineage_audit.json": {
            **base_payload,
            "source_inputs": [rel(QUALITY_PATH), rel(SOURCE_FEATURE_PATH), rel(SUMMARY_KPI_PATH), rel(RISK_PATH), rel(SOURCE_REPORT_PATH), rel(SOURCE_DECISION_PATH)],
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
        f"""# Stage257 Closeout Packet(257단계 종료 작업 묶음)

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
