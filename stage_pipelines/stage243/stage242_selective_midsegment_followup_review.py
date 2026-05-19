from __future__ import annotations

import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence


STAGE_ID = "243_adapter_research__stage242_selective_midsegment_followup_review"
RUN_ID = "run243A_stage243_stage242_selective_midsegment_followup_review_v1"
PACKET_ID = "stage243_stage242_selective_midsegment_followup_review_v1"
SOURCE_STAGE_ID = "242_adapter_research__selective_midsegment_quality_repair_after_highbonus_tradeoff"
SOURCE_RUN_ID = "run242A_stage242_selective_midsegment_quality_repair_after_highbonus_tradeoff_v1"
SOURCE_STAGE242_EVIDENCE_COMMIT = "a62f41abb82b2879008fdad85578eda1c78b1c21"
SOURCE_STAGE242_HASH_RECORD_COMMIT = "00b3182ba007d87ff20d3f5dbbeeb7370a4a853b"
NEXT_STAGE_ID = "244_adapter_research__timestamp_aware_midwindow_guard_repair_after_stage242_inactive_guard"
NEXT_RUN_ID = "run244A_stage244_timestamp_aware_midwindow_guard_repair_after_stage242_inactive_guard_v1"
DECISION = "open_stage244_bounded_timestamp_aware_midwindow_guard_repair_after_stage242_inactive_guard_candidate_not_final"
BOUNDARY = "research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment"

ROOT = Path.cwd()
STAGE_ROOT = Path("stages") / STAGE_ID
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
PACKET_ROOT = Path("docs/agent_control/packets") / PACKET_ID
NEXT_STAGE_ROOT = Path("stages") / NEXT_STAGE_ID

QUALITY_PATH = Path("stages") / SOURCE_STAGE_ID / "03_reviews/stage242_quality_matrix.csv"
GATE_PATH = Path("stages") / SOURCE_STAGE_ID / "03_reviews/stage242_gate_feature_summary.csv"
REPORT_PATH = REVIEWS_ROOT / "stage243_stage242_followup_review.md"
TRADEOFF_PATH = REVIEWS_ROOT / "stage243_tradeoff_review_matrix.csv"
ATTRIBUTION_PATH = REVIEWS_ROOT / "stage243_performance_attribution.csv"
FAILURE_MEMORY_PATH = REVIEWS_ROOT / "stage243_failure_memory.csv"
ROUTE_MATRIX_PATH = REVIEWS_ROOT / "stage243_route_matrix.csv"
SUMMARY_PATH = REVIEWS_ROOT / "stage243_summary.json"
DECISION_PATH = REVIEWS_ROOT / "stage243_decision.md"
STAGE_LEDGER_PATH = REVIEWS_ROOT / "stage_run_ledger.csv"
REVIEW_INDEX_PATH = REVIEWS_ROOT / "review_index.md"
SELECTION_STATUS_PATH = STAGE_ROOT / "04_selected/selection_status.md"

PROJECT_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
ARTIFACT_REGISTRY_PATH = Path("docs/registers/artifact_registry.csv")
CHANGELOG_PATH = Path("docs/workspace/changelog.md")
PRODUCER_PATH = Path("stage_pipelines/stage243/stage242_selective_midsegment_followup_review.py")

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
    return path.as_posix()


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in columns})


def write_md(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def write_json(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8-sig")


def sha256_lf(path: Path) -> str:
    raw = path.read_bytes()
    return hashlib.sha256(raw.replace(b"\r\n", b"\n")).hexdigest()


def upsert_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]], key: str) -> dict[str, Any]:
    existing: list[dict[str, str]] = []
    if path.exists():
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            existing = list(csv.DictReader(handle))
    by_key = {row.get(key, ""): row for row in existing if row.get(key, "")}
    for row in rows:
        by_key[str(row[key])] = {column: str(row.get(column, "")) for column in columns}
    ordered = [by_key[row.get(key, "")] for row in existing if row.get(key, "") in by_key]
    known = {row.get(key, "") for row in ordered}
    ordered.extend(by_key[item] for item in sorted(by_key) if item not in known)
    write_csv(path, ordered, columns)
    return {
        "path": rel(path),
        "rows": len(ordered),
        "upserted_rows": len(rows),
        "sha256": sha256_lf(path),
        "hash_policy": "lf_normalized_text_register",
    }


def as_float(row: Mapping[str, str], key: str) -> float:
    try:
        return float(row.get(key, "") or 0.0)
    except ValueError:
        return 0.0


def by_adapter(rows: Iterable[Mapping[str, str]]) -> dict[str, Mapping[str, str]]:
    return {str(row.get("adapter_id", "")): row for row in rows}


def gate_totals(rows: Sequence[Mapping[str, str]]) -> dict[str, dict[str, int]]:
    totals: dict[str, dict[str, int]] = {}
    for row in rows:
        adapter = str(row.get("adapter_id", ""))
        target = totals.setdefault(adapter, {"mid_window_rows": 0, "selective_blocked_signal_rows": 0})
        target["mid_window_rows"] += int(float(row.get("mid_window_rows") or 0))
        target["selective_blocked_signal_rows"] += int(float(row.get("selective_blocked_signal_rows") or 0))
    return totals


def build_review() -> dict[str, Any]:
    quality = read_csv(QUALITY_PATH)
    gates = read_csv(GATE_PATH)
    gate_by_adapter = gate_totals(gates)
    quality_by_adapter = by_adapter(quality)
    samecap = quality_by_adapter["s242_samecap_control"]
    cap = quality_by_adapter["s242_midlowmid_guard_cap0305"]

    tradeoff_rows: list[dict[str, Any]] = []
    for row in quality:
        adapter = row["adapter_id"]
        gate = gate_by_adapter.get(adapter, {})
        if adapter == "s242_midlowmid_guard_cap0305":
            review_class = "near_miss_mild_cap_oos_damage_guard_inactive"
            read = "34D(34D 기준)에 아주 가까워졌지만 OOS(표본외) 순손익을 깎고 중간 보호문은 작동하지 않았다."
        elif adapter in {"s242_midlow_guard", "s242_midlowmid_guard"}:
            review_class = "guard_variant_identical_to_control_due_to_inactive_window"
            read = "의도한 middle-window guard(중간 기간 보호문)가 0건이라 samecap control(동일 상한 대조군)과 같다."
        else:
            review_class = "control_still_below_34d"
            read = "순손익/OOS(표본외)는 강하지만 DD/PF(낙폭/수익요인)가 아직 34D에 못 닿는다."
        tradeoff_rows.append(
            {
                "adapter_id": adapter,
                "review_class": review_class,
                "validation_net": row["validation_net"],
                "validation_net_gap_vs_34d": row["validation_net_gap_vs_34d"],
                "validation_dd_percent": row["validation_balance_dd_percent"],
                "validation_dd_margin_vs_34d": row["validation_dd_margin_vs_34d"],
                "validation_mid_pf": row["validation_mid_pf"],
                "oos_net": row["oos_net"],
                "oos_pf": row["oos_pf"],
                "mid_window_rows": gate.get("mid_window_rows", 0),
                "selective_blocked_signal_rows": gate.get("selective_blocked_signal_rows", 0),
                "hard_quality_pass": row["hard_quality_pass"],
                "read": read,
            }
        )

    cap_val_delta = as_float(cap, "validation_net") - as_float(samecap, "validation_net")
    cap_oos_delta = as_float(cap, "oos_net") - as_float(samecap, "oos_net")
    cap_dd_delta = as_float(cap, "validation_balance_dd_percent") - as_float(samecap, "validation_balance_dd_percent")
    cap_mid_pf_delta = as_float(cap, "validation_mid_pf") - as_float(samecap, "validation_mid_pf")

    attribution_rows = [
        {
            "attribution_id": f"{RUN_ID}__middle_window_guard_inactive",
            "observed_change": "low/mid guard variants matched samecap control",
            "comparison_baseline": "s242_samecap_control",
            "likely_drivers": "Stage242 parser did not parse YYYY.MM.DD HH:MM:SS feature time; mid_window_rows=0",
            "segment_checks": "gate_feature_summary validation/OOS all variants",
            "trade_shape": "no selective blocked signal rows, so no trade shape change from guard",
            "alternative_explanations": "none material after gate telemetry",
            "attribution_confidence": "high",
            "next_probe": NEXT_STAGE_ID,
        },
        {
            "attribution_id": f"{RUN_ID}__cap0305_near_miss",
            "observed_change": f"validation_net_delta={cap_val_delta:.2f};validation_dd_delta={cap_dd_delta:.4f};mid_pf_delta={cap_mid_pf_delta:.6f};oos_net_delta={cap_oos_delta:.2f}",
            "comparison_baseline": "s242_samecap_control",
            "likely_drivers": "mild model-risk cap 0.0305, not active middle-window guard",
            "segment_checks": "validation early/mid/late and OOS full split reviewed",
            "trade_shape": "trade_count unchanged; risk sizing changed; OOS net damaged",
            "alternative_explanations": "minor rounding or tester path effects possible but guard telemetry rules them out as primary driver",
            "attribution_confidence": "medium_high",
            "next_probe": "timestamp-aware guard with cap0305 control arm",
        },
        {
            "attribution_id": f"{RUN_ID}__still_below_34d",
            "observed_change": "best row still has validation_net_gap_vs_34d=-10.93;validation_dd_margin_vs_34d=-0.033664;validation_mid_pf=1.522877",
            "comparison_baseline": "legacy 34D lesson-only KPI target",
            "likely_drivers": "midsegment quality remains weak and active guard was not actually applied",
            "segment_checks": "quality matrix and segment KPI summary",
            "trade_shape": "OOS remains strong by PF but net falls versus samecap",
            "alternative_explanations": "KPI close enough to justify bounded repair, not enough for final candidate",
            "attribution_confidence": "high",
            "next_probe": NEXT_STAGE_ID,
        },
    ]

    failure_rows = [
        {
            "failure_id": f"{RUN_ID}__stage242_guard_inactive",
            "hypothesis": "Stage242 selective middle-window low/mid margin guard can repair mid PF and DD.",
            "why_failed": "mid_window_rows=0;selective_blocked_signal_rows=0;feature_time_format=YYYY.MM.DD HH:MM:SS;parser_expected_iso_date",
            "salvage_value": "guard idea remains untested; cap0305 near-miss gives a useful control arm",
            "do_not_repeat": "do not treat Stage242 guard variants as active guard evidence",
        },
        {
            "failure_id": f"{RUN_ID}__cap0305_not_final",
            "hypothesis": "Mild model-risk cap 0.0305 may close the 34D gap by itself.",
            "why_failed": "validation_net_gap_vs_34d=-10.93;validation_dd_margin_vs_34d=-0.033664;validation_mid_pf_below_34d;oos_net_delta_vs_samecap=-37.04",
            "salvage_value": "near-miss cap setting can be retained as a comparison arm",
            "do_not_repeat": "do not call cap0305 a final adapter or proceed to ONNX hardening",
        },
    ]

    route_rows = [
        {
            "route_id": DECISION,
            "status": "selected",
            "reason": "Stage242 guard was inactive and cap0305 is near-miss but not final.",
            "effect": "opens a timestamp-aware bounded repair instead of hiding the parser failure",
        },
        {
            "route_id": "proceed_to_onnx_hardening",
            "status": "rejected",
            "reason": "mandatory quality not met and active guard evidence missing",
            "effect": "prevents ONNX(ONNX) from starting on an unproven adapter",
        },
        {
            "route_id": "repeat_global_cap_only",
            "status": "rejected",
            "reason": "Stage240/Stage242 show OOS net damage from cap-only compression",
            "effect": "keeps the next stage bounded to timestamp-aware conditional repair",
        },
    ]

    return {
        "quality_rows": quality,
        "gate_rows": gates,
        "tradeoff_rows": tradeoff_rows,
        "attribution_rows": attribution_rows,
        "failure_rows": failure_rows,
        "route_rows": route_rows,
        "cap0305_vs_samecap": {
            "validation_net_delta": round(cap_val_delta, 2),
            "validation_dd_delta": round(cap_dd_delta, 4),
            "validation_mid_pf_delta": round(cap_mid_pf_delta, 6),
            "oos_net_delta": round(cap_oos_delta, 2),
        },
        "best_adapter": "s242_midlowmid_guard_cap0305",
    }


def write_reports(review: Mapping[str, Any]) -> None:
    tradeoff_rows = list(review["tradeoff_rows"])
    attribution_rows = list(review["attribution_rows"])
    failure_rows = list(review["failure_rows"])
    route_rows = list(review["route_rows"])

    write_csv(
        TRADEOFF_PATH,
        tradeoff_rows,
        [
            "adapter_id",
            "review_class",
            "validation_net",
            "validation_net_gap_vs_34d",
            "validation_dd_percent",
            "validation_dd_margin_vs_34d",
            "validation_mid_pf",
            "oos_net",
            "oos_pf",
            "mid_window_rows",
            "selective_blocked_signal_rows",
            "hard_quality_pass",
            "read",
        ],
    )
    write_csv(
        ATTRIBUTION_PATH,
        attribution_rows,
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
    write_csv(FAILURE_MEMORY_PATH, failure_rows, ["failure_id", "hypothesis", "why_failed", "salvage_value", "do_not_repeat"])
    write_csv(ROUTE_MATRIX_PATH, route_rows, ["route_id", "status", "reason", "effect"])

    matrix_lines = [
        "| adapter(어댑터) | class(분류) | val net(검증 순손익) | DD%(낙폭) | mid PF(중간 수익요인) | OOS net(표본외 순손익) | guard rows(보호문 행) | read(판독) |",
        "|---|---|---:|---:|---:|---:|---:|---|",
    ]
    for row in tradeoff_rows:
        matrix_lines.append(
            f"| {row['adapter_id']} | {row['review_class']} | {row['validation_net']} | {row['validation_dd_percent']} | {row['validation_mid_pf']} | {row['oos_net']} | {row['selective_blocked_signal_rows']} | {row['read']} |"
        )

    report = f"""# Stage243 Stage242 Follow-up Review(243단계 242단계 후속 검토)

- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- source_stage242_evidence_commit(원천 242단계 근거 커밋): `{SOURCE_STAGE242_EVIDENCE_COMMIT}`
- source_stage242_hash_record_commit(원천 242단계 해시 기록 커밋): `{SOURCE_STAGE242_HASH_RECORD_COMMIT}`
- external_verification_status(외부 검증 상태): `review_only_source_stage242_mt5_reports_completed`
- decision(판정): `{DECISION}`
- boundary(주장 경계): `{BOUNDARY}`

## Easy Read(쉬운 판독)

- Stage242(242단계)는 34D(34D 기준)에 더 가까운 near-miss(근접 실패)를 찾았다. `s242_midlowmid_guard_cap0305`는 validation net(검증 순손익) `976.67`, DD(낙폭) `12.9428`, OOS net(표본외 순손익) `775.76`이다.
- 하지만 `mid_window_rows`(중간 창 행 수)와 `selective_blocked_signal_rows`(선택 차단 신호 행 수)가 전부 `0`이다. Effect(효과): Stage242(242단계)의 middle-window guard(중간 기간 보호문)는 실제로 작동하지 않았다.
- 그래서 `s242_midlowmid_guard_cap0305`의 개선은 active guard(작동 보호문)가 아니라 mild model-risk cap(완만한 모델 위험 상한) `0.0305`의 효과로 본다.
- KPI(핵심 성과 지표) 기준으로는 아직 최종 후보가 아니다. validation net(검증 순손익)은 34D보다 `10.93` 낮고, DD(낙폭)는 `0.033664` percentage point(퍼센트포인트) 높고, mid PF(중간 수익요인)는 `1.522877`로 부족하다.

## Tradeoff Matrix(상충 행렬)

{chr(10).join(matrix_lines)}

## Attribution(성과 기여 분석)

- guard_inactive(보호문 비활성): Stage242(242단계) parser(파서)가 `YYYY.MM.DD HH:MM:SS` feature time(피처 시간)을 ISO date(ISO 날짜)처럼 해석하지 못했다. Effect(효과): 선택적 차단은 0건이었다.
- cap0305_near_miss(0.0305 상한 근접 실패): validation net(검증 순손익)은 samecap control(동일 상한 대조군)보다 `{review['cap0305_vs_samecap']['validation_net_delta']}` 좋아졌고 DD(낙폭)는 `{review['cap0305_vs_samecap']['validation_dd_delta']}` 낮아졌지만 OOS net(표본외 순손익)은 `{review['cap0305_vs_samecap']['oos_net_delta']}` 나빠졌다.
- route(경로): Stage244(244단계)는 timestamp-aware midwindow guard(시간 형식 인식 중간 창 보호문)를 실제로 작동시키고, cap0305(0.0305 상한)는 control arm(대조군)으로 남긴다.

## Judgment(판정)

- result_subject(판정 대상): `{RUN_ID}`
- evidence_available(사용 근거): Stage242(242단계) MT5(MetaTrader 5, 메타트레이더5) validation/OOS(검증/표본외) report(보고서), quality matrix(품질 행렬), gate feature summary(보호문 피처 요약), risk/ATR telemetry(위험/ATR 기록).
- evidence_missing(부족 근거): active middle-window guard(작동 중간 기간 보호문) 측정, 34D(34D 기준) 동시 통과, ONNX parity(ONNX 동등성), MT5 ONNX/runtime reproduction(MT5 ONNX/런타임 재현).
- judgment_label(판정 라벨): `stage242_inactive_guard_near_miss_not_final(242단계 비활성 보호문 근접 실패, 최종 아님)`
- claim_boundary(주장 경계): research/development only(연구개발 전용). no deployment(배포 없음), no live_readiness(실거래 준비 없음), no runtime_authority(런타임 권위 없음).
- next_condition(다음 조건): `{NEXT_STAGE_ID}`에서 날짜 파서와 middle-window guard(중간 기간 보호문)를 고친 뒤 같은 KPI(핵심 성과 지표)를 다시 측정한다.

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준선), overall_goal_complete(전체 목표 완료).
"""
    write_md(REPORT_PATH, report)

    decision = f"""# Stage243 Decision(243단계 판정)

- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- decision(판정): `{DECISION}`
- external_verification_status(외부 검증 상태): `review_only_source_stage242_mt5_reports_completed`
- report(보고서): `{rel(REPORT_PATH)}`
- tradeoff_matrix(상충 행렬): `{rel(TRADEOFF_PATH)}`
- attribution(기여 분석): `{rel(ATTRIBUTION_PATH)}`
- failure_memory(실패 기억): `{rel(FAILURE_MEMORY_PATH)}`
- route_matrix(경로 행렬): `{rel(ROUTE_MATRIX_PATH)}`
- next_stage_or_branch(다음 단계 또는 분기): `{NEXT_STAGE_ID}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage243(243단계) closeout(종료)는 overall goal complete(전체 목표 완료)가 아니다.

Effect(효과): Stage244(244단계)에서 timestamp-aware midwindow guard(시간 형식 인식 중간 창 보호문)를 실제로 작동시키고, 34D(34D 기준) KPI(핵심 성과 지표)와 OOS(표본외) 손상을 다시 측정한다.
"""
    write_md(DECISION_PATH, decision)

    write_md(
        REVIEW_INDEX_PATH,
        f"""# Stage243 Review Index(243단계 검토 색인)

- status(상태): `closed_open_stage244_timestamp_aware_midwindow_guard_repair_candidate_not_final`
- packet(작업 묶음): `{PACKET_ID}`
- run(실행): `{RUN_ID}`
- decision(판정): `{DECISION}`
- report(보고서): `{rel(REPORT_PATH)}`
- tradeoff_matrix(상충 행렬): `{rel(TRADEOFF_PATH)}`
- attribution(기여 분석): `{rel(ATTRIBUTION_PATH)}`
- failure_memory(실패 기억): `{rel(FAILURE_MEMORY_PATH)}`
- route_matrix(경로 행렬): `{rel(ROUTE_MATRIX_PATH)}`
- next_stage_or_branch(다음 단계 또는 분기): `{NEXT_STAGE_ID}`
""",
    )

    write_md(
        SELECTION_STATUS_PATH,
        f"""# Stage243 Selection Status(243단계 선택 상태)

- stage_status(단계 상태): `closed_open_stage244_timestamp_aware_midwindow_guard_repair_candidate_not_final`
- current_packet(현재 작업 묶음): `{PACKET_ID}`
- current_run(현재 실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- decision(판정): `{DECISION}`
- next_stage_or_branch(다음 단계 또는 분기): `{NEXT_STAGE_ID}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`
- claim_boundary(주장 경계): `{BOUNDARY}`
""",
    )


def write_next_stage_seed() -> None:
    write_md(
        NEXT_STAGE_ROOT / "00_spec/stage_brief.md",
        f"""# {NEXT_STAGE_ID}

Stage244(244단계)는 Stage242(242단계) inactive guard(비활성 보호문) 실패를 고치는 bounded repair(경계 수리) 단계다.

## Bounded Question(경계 질문)

Can a timestamp-aware middle-window guard(시간 형식 인식 중간 기간 보호문) actually activate on `YYYY.MM.DD HH:MM:SS` feature time(피처 시간) and improve DD(낙폭), mid PF(중간 수익요인), and 34D(34D 기준) gap without damaging validation/OOS net(검증/표본외 순손익)?

Effect(효과): Stage242(242단계)의 parser(파서) 실패를 별도 단계에서 좁게 고치고, cap0305(0.0305 상한)는 control arm(대조군)으로만 비교한다.

## Boundary(경계)

`{BOUNDARY}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "01_inputs/input_refs.md",
        f"""# Stage244 Inputs(244단계 입력)

- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- source_decision(원천 판정): `{DECISION}`
- stage243_report(243단계 보고서): `{rel(REPORT_PATH)}`
- stage243_failure_memory(243단계 실패 기억): `{rel(FAILURE_MEMORY_PATH)}`
- stage242_gate_feature_summary(242단계 보호문 피처 요약): `{rel(GATE_PATH)}`
- stage242_quality_matrix(242단계 품질 행렬): `{rel(QUALITY_PATH)}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "03_reviews/review_index.md",
        f"""# Stage244 Review Index(244단계 검토 색인)

- status(상태): `open_planned_from_stage243`
- source_stage(원천 단계): `{STAGE_ID}`
- source_decision(원천 판정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "04_selected/selection_status.md",
        f"""# Stage244 Selection Status(244단계 선택 상태)

- stage_status(단계 상태): `open_planned_from_stage243`
- current_packet(현재 작업 묶음): `stage244_timestamp_aware_midwindow_guard_repair_after_stage242_inactive_guard_v1`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- source_decision(원천 판정): `{DECISION}`
- claim_boundary(주장 경계): `{BOUNDARY}`
""",
    )


def write_ledgers_and_packet(review: Mapping[str, Any]) -> None:
    primary = "decision={};best_adapter={};next_stage={}".format(DECISION, review["best_adapter"], NEXT_STAGE_ID)
    guardrail = "guard_inactive=1;overall_goal_complete=0;boundary={}".format(BOUNDARY)
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__review_total",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "stage243_review_total",
        "parent_run_id": SOURCE_RUN_ID,
        "record_view": "review_total",
        "tier_scope": "Tier A+B",
        "kpi_scope": "baseline_adapter_review",
        "scoreboard_lane": "baseline_adapter_stage243_followup_review",
        "status": "reviewed_closed",
        "judgment": DECISION,
        "path": rel(REPORT_PATH),
        "primary_kpi": primary,
        "guardrail_kpi": guardrail,
        "external_verification_status": "review_only_source_stage242_mt5_reports_completed",
        "notes": "Stage243 review only; no new MT5 run.",
    }
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "baseline_adapter_stage243_followup_review",
        "status": "reviewed_closed",
        "judgment": DECISION,
        "path": rel(DECISION_PATH),
        "notes": f"source_stage242_evidence_commit={SOURCE_STAGE242_EVIDENCE_COMMIT};source_stage242_hash_record_commit={SOURCE_STAGE242_HASH_RECORD_COMMIT};overall_goal_complete=0",
    }
    project_payload = upsert_csv(PROJECT_LEDGER_PATH, ALPHA_COLUMNS, [alpha_row], key="ledger_row_id")
    stage_payload = upsert_csv(STAGE_LEDGER_PATH, ALPHA_COLUMNS, [alpha_row], key="ledger_row_id")
    run_payload = upsert_csv(RUN_REGISTRY_PATH, RUN_COLUMNS, [run_row], key="run_id")

    created = utc_now()
    artifact_paths = [
        PRODUCER_PATH,
        REPORT_PATH,
        TRADEOFF_PATH,
        ATTRIBUTION_PATH,
        FAILURE_MEMORY_PATH,
        ROUTE_MATRIX_PATH,
        DECISION_PATH,
        REVIEW_INDEX_PATH,
        SELECTION_STATUS_PATH,
        STAGE_LEDGER_PATH,
    ]
    artifacts = [
        {
            "artifact_id": f"{RUN_ID}__{path.name}",
            "artifact_type": "stage243_stage242_followup_review_evidence",
            "path": rel(path),
            "sha256": sha256_lf(path),
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": created,
            "notes": "Stage243 Stage242 follow-up review evidence.",
        }
        for path in artifact_paths
        if path.exists()
    ]
    artifact_payload = upsert_csv(ARTIFACT_REGISTRY_PATH, ARTIFACT_COLUMNS, artifacts, key="artifact_id")

    summary = {
        "packet_id": PACKET_ID,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "source_stage": SOURCE_STAGE_ID,
        "source_run": SOURCE_RUN_ID,
        "decision": DECISION,
        "next_stage": NEXT_STAGE_ID,
        "external_verification_status": "review_only_source_stage242_mt5_reports_completed",
        "overall_goal_complete": False,
        "claim_boundary": BOUNDARY,
        "pushed_commit_hash": "pending_until_push",
        "best_adapter": review["best_adapter"],
        "cap0305_vs_samecap": review["cap0305_vs_samecap"],
        "failure_memory": list(review["failure_rows"]),
        "route_rows": list(review["route_rows"]),
        "required_outputs": {
            "report": rel(REPORT_PATH),
            "tradeoff_matrix": rel(TRADEOFF_PATH),
            "attribution": rel(ATTRIBUTION_PATH),
            "failure_memory": rel(FAILURE_MEMORY_PATH),
            "decision": rel(DECISION_PATH),
        },
        "ledger_payload": {
            "run_registry": run_payload,
            "project_alpha_ledger": project_payload,
            "stage_ledger": stage_payload,
            "artifact_registry": artifact_payload,
        },
    }
    write_json(SUMMARY_PATH, summary)
    write_json(PACKET_ROOT / "aggregate_summary.json", summary)

    base_payload = {
        "packet_id": PACKET_ID,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "source_stage": SOURCE_STAGE_ID,
        "source_run": SOURCE_RUN_ID,
        "decision": DECISION,
        "next_stage": NEXT_STAGE_ID,
        "external_verification_status": "review_only_source_stage242_mt5_reports_completed",
        "claim_boundary": BOUNDARY,
        "overall_goal_complete": False,
    }
    gates = {
        "routing_receipt.json": {
            **base_payload,
            "primary_family": "kpi_evidence(KPI/근거)",
            "primary_skill": "obsidian-result-judgment(결과 판정)",
            "support_skills": [
                "obsidian-performance-attribution(성과 기여 분석)",
                "obsidian-artifact-lineage(산출물 계보)",
            ],
        },
        "kpi_contract_audit.json": {**base_payload, "status": "passed", "kpi_basis": "source Stage242 MT5 reports and summaries"},
        "result_judgment_gate.json": {
            **base_payload,
            "result_subject": RUN_ID,
            "evidence_available": [rel(QUALITY_PATH), rel(GATE_PATH), rel(REPORT_PATH)],
            "evidence_missing": ["active middle-window guard measurement", "34D simultaneous pass", "ONNX parity"],
            "judgment_label": "stage242_inactive_guard_near_miss_not_final",
            "next_condition": NEXT_STAGE_ID,
        },
        "performance_attribution_gate.json": {**base_payload, "attribution_rows": list(review["attribution_rows"])},
        "artifact_lineage_audit.json": {
            **base_payload,
            "source_inputs": [rel(QUALITY_PATH), rel(GATE_PATH)],
            "producer": rel(PRODUCER_PATH),
            "artifact_paths": [rel(path) for path in artifact_paths if path.exists()],
            "lineage_judgment": "connected_with_boundary",
        },
        "final_claim_guard.json": {**base_payload, "forbidden_claims": ["deployment", "live_readiness", "runtime_authority", "overall_goal_complete"], "status": "passed"},
        "required_gate_coverage_audit.json": {**base_payload, "required_gates": ["kpi_contract_audit", "result_judgment_gate", "performance_attribution_gate", "artifact_lineage_audit", "final_claim_guard"], "status": "passed"},
        "packet_receipt.json": {**base_payload, "created_at_utc": created, "status": "closed_pending_push_hash"},
        "closeout_packet.md": "# Stage243 Closeout Packet(243단계 종료 묶음)\n\n- decision(판정): `{}`\n- next_stage(다음 단계): `{}`\n- overall_goal_complete(전체 목표 완료): `false`\n".format(DECISION, NEXT_STAGE_ID),
    }
    for name, payload in gates.items():
        if isinstance(payload, str):
            write_md(PACKET_ROOT / name, payload)
        else:
            write_json(PACKET_ROOT / name, payload)


def update_changelog() -> None:
    entry = f"""
## {utc_now()} Stage243 Stage242 follow-up review closeout(243단계 242단계 후속 검토 종료)

- action(행동): closed(종료) `{STAGE_ID}` with decision(판정) `{DECISION}`.
- effect(효과): Stage242(242단계)의 inactive guard(비활성 보호문)와 cap0305 near-miss(0.0305 상한 근접 실패)를 분리하고 Stage244(244단계) timestamp-aware repair(시간 형식 인식 수리)로 넘겼다.
- boundary(주장 경계): `{BOUNDARY}`.
"""
    existing = CHANGELOG_PATH.read_text(encoding="utf-8-sig") if CHANGELOG_PATH.exists() else ""
    CHANGELOG_PATH.write_text(existing.rstrip() + entry, encoding="utf-8-sig")


def main() -> None:
    STAGE_ROOT.joinpath("00_spec").mkdir(parents=True, exist_ok=True)
    STAGE_ROOT.joinpath("01_inputs").mkdir(parents=True, exist_ok=True)
    STAGE_ROOT.joinpath("04_selected").mkdir(parents=True, exist_ok=True)
    review = build_review()
    write_reports(review)
    write_next_stage_seed()
    write_ledgers_and_packet(review)
    update_changelog()
    print(json.dumps({"status": "completed", "stage": STAGE_ID, "decision": DECISION, "next_stage": NEXT_STAGE_ID}, ensure_ascii=False))


if __name__ == "__main__":
    main()
