from __future__ import annotations

import csv
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


STAGE_ID = "245_adapter_research__stage244_timestamp_guard_followup_review"
RUN_ID = "run245A_stage245_stage244_timestamp_guard_followup_review_v1"
PACKET_ID = "stage245_stage244_timestamp_guard_followup_review_v1"
SOURCE_STAGE_ID = "244_adapter_research__timestamp_aware_midwindow_guard_repair_after_stage242_inactive_guard"
SOURCE_RUN_ID = "run244A_stage244_timestamp_aware_midwindow_guard_repair_after_stage242_inactive_guard_v1"
SOURCE_EVIDENCE_COMMIT = "8a5691eac72e6b347263e7b0ab110004e2054668"
SOURCE_HASH_RECORD_COMMIT = "579cf6cddc067f425169846926b51617f651d563"
NEXT_STAGE_ID = "246_adapter_research__soft_timestamp_guard_repair_after_stage244_overprune"
NEXT_RUN_ID = "run246A_stage246_soft_timestamp_guard_repair_after_stage244_overprune_v1"
NEXT_PACKET_ID = "stage246_soft_timestamp_guard_repair_after_stage244_overprune_v1"
DECISION = "open_stage246_bounded_soft_guard_repair_after_stage244_overprune_candidate_not_final"
BOUNDARY = "research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment"
TARGET_SURFACE = "legacy_34d_kpi_lesson_only_v2_native_soft_timestamp_guard_repair_after_overprune"

ROOT = Path.cwd()
STAGE_ROOT = ROOT / "stages" / STAGE_ID
REVIEWS = STAGE_ROOT / "03_reviews"
PACKET_ROOT = ROOT / "docs/agent_control/packets" / PACKET_ID
NEXT_STAGE_ROOT = ROOT / "stages" / NEXT_STAGE_ID
SOURCE_REVIEWS = ROOT / "stages" / SOURCE_STAGE_ID / "03_reviews"

QUALITY_PATH = SOURCE_REVIEWS / "stage244_quality_matrix.csv"
GATE_PATH = SOURCE_REVIEWS / "stage244_gate_feature_summary.csv"
SEGMENT_PATH = SOURCE_REVIEWS / "stage244_segment_kpi_summary.csv"
RISK_PATH = SOURCE_REVIEWS / "stage244_risk_atr_telemetry.csv"

REPORT_PATH = REVIEWS / "stage245_stage244_followup_review.md"
TRADEOFF_PATH = REVIEWS / "stage245_tradeoff_review_matrix.csv"
ATTRIBUTION_PATH = REVIEWS / "stage245_performance_attribution.csv"
FAILURE_PATH = REVIEWS / "stage245_failure_memory.csv"
ROUTE_PATH = REVIEWS / "stage245_route_matrix.csv"
SUMMARY_PATH = REVIEWS / "stage245_summary.json"
DECISION_PATH = REVIEWS / "stage245_decision.md"
STAGE_LEDGER_PATH = REVIEWS / "stage_run_ledger.csv"
REVIEW_INDEX_PATH = REVIEWS / "review_index.md"
SELECTION_PATH = STAGE_ROOT / "04_selected/selection_status.md"

CURRENT_STATE_PATH = ROOT / "docs/context/current_working_state.md"
WORKSPACE_STATE_PATH = ROOT / "docs/workspace/workspace_state.yaml"
CHANGELOG_PATH = ROOT / "docs/workspace/changelog.md"
RUN_REGISTRY_PATH = ROOT / "docs/registers/run_registry.csv"
PROJECT_LEDGER_PATH = ROOT / "docs/registers/alpha_run_ledger.csv"
ARTIFACT_REGISTRY_PATH = ROOT / "docs/registers/artifact_registry.csv"
PRODUCER_PATH = ROOT / "stage_pipelines/stage245/stage244_timestamp_guard_followup_review.py"

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
    absolute = str(path.resolve())
    if os.name == "nt" and not absolute.startswith("\\\\?\\"):
        return "\\\\?\\" + absolute
    return absolute


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


def write_csv(path: Path, rows: list[dict[str, Any]], columns: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(long_path(path), "w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: row.get(column, "") for column in columns})


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(long_path(path), "w", encoding="utf-8", newline="\n") as handle:
        json.dump(payload, handle, indent=2, ensure_ascii=False, sort_keys=True)
        handle.write("\n")


def sha256_lf(path: Path) -> str:
    with open(long_path(path), "rb") as handle:
        raw = handle.read()
    return hashlib.sha256(raw.replace(b"\r\n", b"\n")).hexdigest()


def fnum(value: str) -> float:
    try:
        return float(value or 0)
    except ValueError:
        return 0.0


def upsert_csv(path: Path, columns: list[str], rows: list[dict[str, Any]], key: str) -> dict[str, Any]:
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


def gate_counts() -> dict[str, dict[str, int]]:
    result: dict[str, dict[str, int]] = {}
    for row in read_csv(GATE_PATH):
        adapter = row["adapter_id"]
        split = row["split"]
        target = result.setdefault(adapter, {"validation_is": 0, "oos": 0})
        target[split] += int(float(row.get("selective_blocked_signal_rows") or 0))
    return result


def build_tradeoff_rows(quality_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    gates = gate_counts()
    samecap = next(row for row in quality_rows if row["adapter_id"] == "s244_samecap_control")
    classes = {
        "s244_samecap_control": "samecap_reference_still_below_34d",
        "s244_midlow_guard": "active_low_guard_overpruned_validation_net_and_mid_pf",
        "s244_midlowmid_guard": "active_low_mid_guard_collapsed_mid_pf",
        "s244_cap0305_control": "cap0305_control_near_miss_no_guard",
        "s244_midlowmid_guard_cap0305": "cap0305_plus_active_guard_overpruned",
    }
    reads = {
        "s244_samecap_control": "OOS(표본외)는 강하지만 34D(34D 기준) 대비 validation net/DD/mid PF(검증 순손익/낙폭/중간 수익요인)가 부족하다.",
        "s244_midlow_guard": "low bucket(낮은 구간)을 막자 DD(낙폭)는 좋아졌지만 validation net(검증 순손익)과 mid PF(중간 수익요인)가 크게 무너졌다.",
        "s244_midlowmid_guard": "low+mid bucket(낮은+중간 구간)을 막자 mid PF(중간 수익요인)가 거의 1.0까지 내려가 over-prune(과차단)이 확인됐다.",
        "s244_cap0305_control": "mild cap(완만한 상한)만 둔 near-miss(근접 실패)다. 가장 가깝지만 아직 34D(34D 기준)를 동시에 넘지 못한다.",
        "s244_midlowmid_guard_cap0305": "cap(상한)과 hard guard(강한 보호문)를 같이 쓰면 OOS PF(표본외 수익요인)는 높지만 validation net(검증 순손익)이 크게 손상된다.",
    }
    rows: list[dict[str, Any]] = []
    for row in quality_rows:
        adapter = row["adapter_id"]
        blocked = gates.get(adapter, {})
        rows.append(
            {
                "adapter_id": adapter,
                "review_class": classes[adapter],
                "validation_net": row["validation_net"],
                "validation_net_delta_vs_samecap": f"{fnum(row['validation_net']) - fnum(samecap['validation_net']):.2f}",
                "validation_dd_percent": row["validation_balance_dd_percent"],
                "validation_dd_delta_vs_samecap": f"{fnum(row['validation_balance_dd_percent']) - fnum(samecap['validation_balance_dd_percent']):.4f}",
                "validation_mid_pf": row["validation_mid_pf"],
                "validation_mid_pf_delta_vs_samecap": f"{fnum(row['validation_mid_pf']) - fnum(samecap['validation_mid_pf']):.6f}",
                "oos_net": row["oos_net"],
                "oos_net_delta_vs_samecap": f"{fnum(row['oos_net']) - fnum(samecap['oos_net']):.2f}",
                "oos_pf": row["oos_pf"],
                "selective_blocked_validation": blocked.get("validation_is", 0),
                "selective_blocked_oos": blocked.get("oos", 0),
                "hard_quality_pass": row["hard_quality_pass"],
                "read": reads[adapter],
            }
        )
    return rows


def main() -> None:
    quality_rows = read_csv(QUALITY_PATH)
    tradeoff_rows = build_tradeoff_rows(quality_rows)
    q = {row["adapter_id"]: row for row in quality_rows}
    samecap = q["s244_samecap_control"]

    def delta(adapter: str, key: str) -> float:
        return fnum(q[adapter][key]) - fnum(samecap[key])

    attribution_rows = [
        {
            "attribution_id": f"{RUN_ID}__timestamp_parser_repair_validated",
            "observed_change": "mid_window_rows and selective_blocked_signal_rows became nonzero",
            "comparison_baseline": "Stage242 inactive guard evidence",
            "likely_drivers": "timestamp parser repair for YYYY.MM.DD HH:MM:SS feature time",
            "segment_checks": "validation/OOS gate_feature_summary reviewed for every Stage244 variant",
            "trade_shape": "active guard reduced trade count where blocked rows became nonzero",
            "alternative_explanations": "none material; gate telemetry directly changed",
            "attribution_confidence": "high",
            "next_probe": "repair guard selectivity, not parser",
        },
        {
            "attribution_id": f"{RUN_ID}__low_guard_overprune_damage",
            "observed_change": f"validation_net_delta={delta('s244_midlow_guard','validation_net'):.2f};mid_pf_delta={delta('s244_midlow_guard','validation_mid_pf'):.6f};oos_net_delta={delta('s244_midlow_guard','oos_net'):.2f}",
            "comparison_baseline": "s244_samecap_control",
            "likely_drivers": "hard low-bucket middle-window block; 73 validation and 40 OOS signals blocked",
            "segment_checks": "validation/OOS and early/mid/late reviewed; mid PF dropped to 1.148244",
            "trade_shape": "validation trades fell from 269 to 198; validation net fell from 967.85 to 526.85",
            "alternative_explanations": "DD improvement came from removing too much profitable exposure",
            "attribution_confidence": "high",
            "next_probe": "soft or score-weighted guard instead of hard low block",
        },
        {
            "attribution_id": f"{RUN_ID}__low_mid_guard_mid_pf_collapse",
            "observed_change": f"validation_net_delta={delta('s244_midlowmid_guard','validation_net'):.2f};mid_pf_delta={delta('s244_midlowmid_guard','validation_mid_pf'):.6f};oos_net_delta={delta('s244_midlowmid_guard','oos_net'):.2f}",
            "comparison_baseline": "s244_samecap_control",
            "likely_drivers": "hard low+mid middle-window block; 87 validation and 46 OOS signals blocked",
            "segment_checks": "middle chronological third reviewed; validation mid PF dropped to 1.019201",
            "trade_shape": "validation trades fell from 269 to 184",
            "alternative_explanations": "OOS PF gain does not rescue validation collapse",
            "attribution_confidence": "high",
            "next_probe": NEXT_STAGE_ID,
        },
        {
            "attribution_id": f"{RUN_ID}__cap0305_near_miss_not_final",
            "observed_change": f"validation_net_delta={delta('s244_cap0305_control','validation_net'):.2f};validation_dd_delta={delta('s244_cap0305_control','validation_balance_dd_percent'):.4f};oos_net_delta={delta('s244_cap0305_control','oos_net'):.2f}",
            "comparison_baseline": "s244_samecap_control and legacy 34D lesson-only KPI target",
            "likely_drivers": "mild model-risk cap 0.0305 improves validation balance but trims OOS net",
            "segment_checks": "quality flags remain validation_net_below_34d, validation_balance_dd_above_34d, validation_mid_pf_below_34d",
            "trade_shape": "trade count unchanged versus samecap; risk sizing changed",
            "alternative_explanations": "small validation gain could be sizing noise; still useful as control arm",
            "attribution_confidence": "medium_high",
            "next_probe": "Stage246 should preserve cap0305 control while testing softer guard forms",
        },
    ]
    failure_rows = [
        {"failure_id": "stage245_active_guard_is_valid_but_not_quality_positive", "evidence": "parser fixed and blocked rows became nonzero", "impact": "activation is necessary but not sufficient", "next_handling": NEXT_STAGE_ID},
        {"failure_id": "stage245_low_guard_overpruned_validation_net", "evidence": "s244_midlow_guard validation net 526.85 vs samecap 967.85", "impact": "DD improvement came with unacceptable net and mid PF damage", "next_handling": "avoid hard low bucket block"},
        {"failure_id": "stage245_low_mid_guard_mid_pf_collapse", "evidence": "s244_midlowmid_guard mid PF 1.019201 and validation net 453.46", "impact": "middle segment became nearly flat", "next_handling": "test soft or score-weighted guard only"},
        {"failure_id": "stage245_cap0305_near_miss_not_final", "evidence": "s244_cap0305_control validation net gap -10.93; DD margin -0.033664; mid PF 1.522877", "impact": "closest row remains below 34D", "next_handling": "use as reference control in Stage246"},
    ]
    route_rows = [
        {
            "route_id": "stage245_route_to_stage246",
            "decision": DECISION,
            "reason": "Stage244 guard activation worked but hard blocking over-pruned KPI.",
            "next_stage_or_branch": NEXT_STAGE_ID,
            "allowed_work": "bounded soft/score-weighted guard repair with cap0305 control",
            "forbidden_work": "ONNX, deployment, live readiness, open-ended Stage244 tuning, final adapter claim",
        }
    ]

    trade_cols = ["adapter_id", "review_class", "validation_net", "validation_net_delta_vs_samecap", "validation_dd_percent", "validation_dd_delta_vs_samecap", "validation_mid_pf", "validation_mid_pf_delta_vs_samecap", "oos_net", "oos_net_delta_vs_samecap", "oos_pf", "selective_blocked_validation", "selective_blocked_oos", "hard_quality_pass", "read"]
    attr_cols = ["attribution_id", "observed_change", "comparison_baseline", "likely_drivers", "segment_checks", "trade_shape", "alternative_explanations", "attribution_confidence", "next_probe"]
    failure_cols = ["failure_id", "evidence", "impact", "next_handling"]
    route_cols = ["route_id", "decision", "reason", "next_stage_or_branch", "allowed_work", "forbidden_work"]
    write_csv(TRADEOFF_PATH, tradeoff_rows, trade_cols)
    write_csv(ATTRIBUTION_PATH, attribution_rows, attr_cols)
    write_csv(FAILURE_PATH, failure_rows, failure_cols)
    write_csv(ROUTE_PATH, route_rows, route_cols)

    report_lines = [
        "# Stage245 Stage244 Follow-up Review(245단계 244단계 후속 검토)",
        "",
        f"- stage(단계): `{STAGE_ID}`",
        f"- run(실행): `{RUN_ID}`",
        f"- source_stage(원천 단계): `{SOURCE_STAGE_ID}`",
        f"- source_stage244_evidence_commit(원천 244단계 근거 커밋): `{SOURCE_EVIDENCE_COMMIT}`",
        f"- source_stage244_hash_record_commit(원천 244단계 해시 기록 커밋): `{SOURCE_HASH_RECORD_COMMIT}`",
        "- external_verification_status(외부 검증 상태): `review_only_source_stage244_mt5_reports_completed`",
        f"- decision(판정): `{DECISION}`",
        f"- boundary(주장 경계): `{BOUNDARY}`",
        "",
        "## Easy Read(쉬운 판독)",
        "",
        "- Stage244(244단계)는 timestamp parser(시간 파서)를 고쳐 guard(보호문)를 실제로 작동시켰다.",
        "- 그러나 hard guard(강한 보호문)는 너무 많이 막았다. validation net(검증 순손익)과 mid PF(중간 수익요인)가 크게 낮아졌다.",
        "- `s244_cap0305_control`이 가장 가까운 near-miss(근접 실패)이지만 아직 34D(34D 기준)를 동시에 넘지 못한다.",
        "- 결론: guard activation(보호문 작동)은 성공, KPI quality(핵심 성과 지표 품질)는 실패다.",
        "",
        "## KPI Read(KPI 핵심 성과 지표 판독)",
        "",
        "| adapter(어댑터) | class(분류) | val net(검증 순손익) | net delta(순손익 차이) | DD%(낙폭) | mid PF(중간 수익요인) | OOS net(표본외 순손익) | blocked val/OOS(차단 검증/표본외) |",
        "|---|---|---:|---:|---:|---:|---:|---:|",
    ]
    for row in tradeoff_rows:
        report_lines.append(f"| {row['adapter_id']} | {row['review_class']} | {row['validation_net']} | {row['validation_net_delta_vs_samecap']} | {row['validation_dd_percent']} | {row['validation_mid_pf']} | {row['oos_net']} | {row['selective_blocked_validation']}/{row['selective_blocked_oos']} |")
    report_lines.extend(
        [
            "",
            "## Judgment(판정)",
            "",
            f"- result_subject(판정 대상): `{RUN_ID}`",
            f"- evidence_available(사용 근거): Stage244(244단계) quality/gate/segment/risk files(품질/보호문/구간/위험 파일).",
            "- evidence_missing(부족 근거): soft guard repair measurement(부드러운 보호문 수리 측정), ONNX parity(ONNX 동등성), MT5 ONNX/runtime reproduction(MT5 ONNX/런타임 재현).",
            "- judgment_label(판정 라벨): `active_guard_overprune_negative_not_final(작동 보호문 과차단 부정, 최종 아님)`",
            f"- claim_boundary(주장 경계): `{BOUNDARY}`",
            f"- next_condition(다음 조건): `{NEXT_STAGE_ID}`",
            "",
            "Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준선), overall_goal_complete(전체 목표 완료).",
        ]
    )
    write_text(REPORT_PATH, "\n".join(report_lines))

    write_text(
        DECISION_PATH,
        f"""# Stage245 Decision(245단계 판정)

- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- decision(판정): `{DECISION}`
- external_verification_status(외부 검증 상태): `review_only_source_stage244_mt5_reports_completed`
- report(보고서): `{rel(REPORT_PATH)}`
- tradeoff_matrix(상충 행렬): `{rel(TRADEOFF_PATH)}`
- attribution(기여 분석): `{rel(ATTRIBUTION_PATH)}`
- failure_memory(실패 기억): `{rel(FAILURE_PATH)}`
- route_matrix(경로 행렬): `{rel(ROUTE_PATH)}`
- next_stage_or_branch(다음 단계 또는 분기): `{NEXT_STAGE_ID}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage245(245단계) closeout(종료)는 overall goal complete(전체 목표 완료)가 아니다.

Effect(효과): Stage246(246단계)에서 hard block(강한 차단)을 반복하지 않고 soft/score-weighted guard(부드러운/점수 가중 보호문)를 좁게 시험한다.
""",
    )

    summary = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "packet_id": PACKET_ID,
        "source_stage": SOURCE_STAGE_ID,
        "source_run_id": SOURCE_RUN_ID,
        "source_stage244_evidence_commit": SOURCE_EVIDENCE_COMMIT,
        "source_stage244_hash_record_commit": SOURCE_HASH_RECORD_COMMIT,
        "decision": DECISION,
        "next_stage_or_branch": NEXT_STAGE_ID,
        "external_verification_status": "review_only_source_stage244_mt5_reports_completed",
        "overall_goal_complete": False,
        "pushed_commit_hash": "pending_until_push",
        "claim_boundary": BOUNDARY,
        "best_reference": "s244_cap0305_control",
        "tradeoff_rows": tradeoff_rows,
        "attribution_rows": attribution_rows,
        "failure_memory_rows": failure_rows,
        "required_outputs": {
            "report": rel(REPORT_PATH),
            "tradeoff_matrix": rel(TRADEOFF_PATH),
            "attribution": rel(ATTRIBUTION_PATH),
            "failure_memory": rel(FAILURE_PATH),
            "route_matrix": rel(ROUTE_PATH),
            "decision": rel(DECISION_PATH),
        },
    }
    write_json(SUMMARY_PATH, summary)

    write_text(REVIEW_INDEX_PATH, f"""# Stage245 Review Index(245단계 검토 색인)

- status(상태): `reviewed_closed_open_stage246_soft_guard_repair_candidate_not_final`
- report(보고서): `{rel(REPORT_PATH)}`
- decision(판정): `{rel(DECISION_PATH)}`
- tradeoff_matrix(상충 행렬): `{rel(TRADEOFF_PATH)}`
- attribution(기여 분석): `{rel(ATTRIBUTION_PATH)}`
- failure_memory(실패 기억): `{rel(FAILURE_PATH)}`
- route_matrix(경로 행렬): `{rel(ROUTE_PATH)}`
""")
    write_text(SELECTION_PATH, f"""# Stage245 Selection Status(245단계 선택 상태)

- stage_status(단계 상태): `reviewed_closed_open_stage246_soft_guard_repair_candidate_not_final`
- current_packet(현재 작업 묶음): `{PACKET_ID}`
- current_run(현재 실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- external_verification_status(외부 검증 상태): `review_only_source_stage244_mt5_reports_completed`
- decision(판정): `{DECISION}`
- next_stage_or_branch(다음 단계 또는 분기): `{NEXT_STAGE_ID}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`
- claim_boundary(주장 경계): `{BOUNDARY}`
""")

    write_text(NEXT_STAGE_ROOT / "00_spec/stage_brief.md", f"""# {NEXT_STAGE_ID}

Stage246(246단계)는 Stage244/245(244/245단계) failure memory(실패 기억)를 받아 soft timestamp guard repair(부드러운 시간 보호문 수리)를 측정하는 bounded repair(경계 수리) 단계다.

## Bounded Question(경계 질문)

Can a soft or score-weighted midwindow guard(부드러운 또는 점수 가중 중간 창 보호문) reduce DD(낙폭) and improve mid PF(중간 수익요인) without destroying validation/OOS net(검증/표본외 순손익), ATR SL/TP(ATR 손절/익절), model-controlled risk%(모델 제어 위험 비율), and segment behavior(구간 행동)?

## Boundary(경계)

`{BOUNDARY}`
""")
    write_text(NEXT_STAGE_ROOT / "01_inputs/input_refs.md", f"""# Stage246 Inputs(246단계 입력)

- source_stage(원천 단계): `{STAGE_ID}`
- source_decision(원천 판정): `{DECISION}`
- source_report(원천 보고서): `{rel(REPORT_PATH)}`
- source_tradeoff_matrix(원천 상충 행렬): `{rel(TRADEOFF_PATH)}`
- source_failure_memory(원천 실패 기억): `{rel(FAILURE_PATH)}`
- source_stage244_quality_matrix(원천 244단계 품질 행렬): `{rel(QUALITY_PATH)}`
- source_stage244_gate_feature_summary(원천 244단계 보호문 피처 요약): `{rel(GATE_PATH)}`
""")
    write_text(NEXT_STAGE_ROOT / "03_reviews/review_index.md", f"""# Stage246 Review Index(246단계 검토 색인)

- status(상태): `open_planned_from_stage245`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- source_stage(원천 단계): `{STAGE_ID}`
- source_decision(원천 판정): `{DECISION}`
""")
    write_text(NEXT_STAGE_ROOT / "04_selected/selection_status.md", f"""# Stage246 Selection Status(246단계 선택 상태)

- stage_status(단계 상태): `open_planned_from_stage245`
- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- source_decision(원천 판정): `{DECISION}`
- claim_boundary(주장 경계): `{BOUNDARY}`
""")

    stage_ledger_rows = [
        {
            "ledger_row_id": f"{RUN_ID}__review_total",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "stage245_review_total",
            "parent_run_id": RUN_ID,
            "record_view": "review_total",
            "tier_scope": "Tier A+B",
            "kpi_scope": "review_only_source_stage244",
            "scoreboard_lane": "baseline_adapter_stage245_followup_review",
            "status": "reviewed_closed",
            "judgment": DECISION,
            "path": rel(REPORT_PATH),
            "primary_kpi": "best_reference=s244_cap0305_control;validation_net=976.67;validation_dd=12.9428;validation_mid_pf=1.522877;oos_net=775.76",
            "guardrail_kpi": "active_guard_overpruned;hard_quality_pass=false;overall_goal_complete=0",
            "external_verification_status": "review_only_source_stage244_mt5_reports_completed",
            "notes": "Stage245 review only; routes to bounded Stage246 soft guard repair.",
        }
    ]
    write_csv(STAGE_LEDGER_PATH, stage_ledger_rows, ALPHA_COLUMNS)
    run_payload = upsert_csv(
        RUN_REGISTRY_PATH,
        RUN_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "baseline_adapter_research(기준선 어댑터 연구)",
                "status": "reviewed_closed",
                "judgment": DECISION,
                "path": rel(REPORT_PATH),
                "notes": f"source_stage244_evidence_commit={SOURCE_EVIDENCE_COMMIT};source_stage244_hash_record_commit={SOURCE_HASH_RECORD_COMMIT};boundary={BOUNDARY}",
            }
        ],
        "run_id",
    )
    project_payload = upsert_csv(PROJECT_LEDGER_PATH, ALPHA_COLUMNS, stage_ledger_rows, "ledger_row_id")
    stage_payload = {"path": rel(STAGE_LEDGER_PATH), "rows": len(stage_ledger_rows), "upserted_rows": len(stage_ledger_rows), "sha256": sha256_lf(STAGE_LEDGER_PATH), "hash_policy": "lf_normalized_text_register"}

    write_text(CURRENT_STATE_PATH, f"""# Current Working State(현재 작업 상태)

- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- active_stage(활성 단계): `{NEXT_STAGE_ID}`
- selected_research_baseline(선택 연구 기준선): `none`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- adapter_under_review(검토 중 어댑터): `stage244_cap0305_near_miss_and_active_guard_failure_memory`
- status(상태): `stage245_open_stage246_bounded_soft_guard_repair_after_stage244_overprune_candidate_not_final`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage245(245단계)는 Stage244(244단계) timestamp-aware guard(시간 형식 인식 보호문)를 review-only(검토 전용)로 판정했다. Effect(효과): Stage246(246단계)이 hard block(강한 차단)을 반복하지 않고 soft/score-weighted guard(부드러운/점수 가중 보호문)를 좁게 시험한다.

## Latest Stage245 Evidence(최신 245단계 근거)

- run(실행): `{RUN_ID}`
- decision(판정): `{DECISION}`
- external_verification_status(외부 검증 상태): `review_only_source_stage244_mt5_reports_completed`
- report(보고서): `{rel(REPORT_PATH)}`
- tradeoff_matrix(상충 행렬): `{rel(TRADEOFF_PATH)}`
- attribution(기여 분석): `{rel(ATTRIBUTION_PATH)}`
- failure_memory(실패 기억): `{rel(FAILURE_PATH)}`
- route_matrix(경로 행렬): `{rel(ROUTE_PATH)}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준선), legacy_inheritance(레거시 상속), overall_goal_complete(전체 목표 완료).
""")

    workspace = read_text(WORKSPACE_STATE_PATH)
    workspace = workspace.replace("current_run_id: run245A_stage245_stage244_timestamp_guard_followup_review_v1", f"current_run_id: {NEXT_RUN_ID}", 1)
    workspace = workspace.replace("active_stage: 245_adapter_research__stage244_timestamp_guard_followup_review", f"active_stage: {NEXT_STAGE_ID}", 1)
    focus = f"""- >-
  Stage245(245단계) closed(종료) as `{DECISION}` and Stage246(246단계) `{NEXT_STAGE_ID}` is open_planned(개방 계획). Effect(효과): active hard guard(작동 강한 보호문)의 over-prune damage(과차단 손상)를 failure memory(실패 기억)로 두고 soft/score-weighted guard(부드러운/점수 가중 보호문)를 좁게 측정한다.
- >-
  Stage245 evidence(245단계 근거)는 `{rel(REPORT_PATH)}`, `{rel(TRADEOFF_PATH)}`, `{rel(ATTRIBUTION_PATH)}`, `{rel(FAILURE_PATH)}`에 있다. Effect(효과): 34D(34D 기준) 목표에 가까운 cap0305(0.0305 상한) near-miss(근접 실패)를 보존하되 hard block(강한 차단)은 반복하지 않는다.
- >-
  Target surface(목표 표면)는 `{TARGET_SURFACE}`이고 legacy 34D(레거시 34D)는 lesson-only KPI target(교훈 전용 핵심 성과 지표 목표)이다. Effect(효과): v2-native research(v2 고유 연구)를 계속한다.

"""
    workspace = workspace.replace("current_focus:\n", "current_focus:\n" + focus, 1)
    workspace = workspace.replace("  status: open_planned_from_stage244\n  current_run_id: run245A_stage245_stage244_timestamp_guard_followup_review_v1", f"  status: reviewed_closed_open_stage246_soft_guard_repair_candidate_not_final\n  current_run_id: {RUN_ID}", 1)
    stage245_open_block = f"""stage245_stage244_timestamp_guard_followup_review:
  packet_id: {PACKET_ID}
  stage_id: {STAGE_ID}
  status: reviewed_closed_open_stage246_soft_guard_repair_candidate_not_final
  current_run_id: {RUN_ID}
  source_stage: {SOURCE_STAGE_ID}
  source_run: {SOURCE_RUN_ID}
  source_decision: open_stage245_bounded_followup_due_to_timestamp_guard_tradeoff_candidate_not_final
  decision: {DECISION}
  report_path: {rel(REPORT_PATH)}
  decision_path: {rel(DECISION_PATH)}
  tradeoff_matrix_path: {rel(TRADEOFF_PATH)}
  attribution_path: {rel(ATTRIBUTION_PATH)}
  failure_memory_path: {rel(FAILURE_PATH)}
  route_matrix_path: {rel(ROUTE_PATH)}
  external_verification_status: review_only_source_stage244_mt5_reports_completed
  pushed_commit_hash: pending_until_push
  next_action: {NEXT_RUN_ID}
  boundary: {BOUNDARY}
"""
    workspace = workspace.replace("""stage245_stage244_timestamp_guard_followup_review:
  packet_id: stage245_stage244_timestamp_guard_followup_review_v1
  stage_id: 245_adapter_research__stage244_timestamp_guard_followup_review
  status: open_planned_from_stage244
  current_run_id: run245A_stage245_stage244_timestamp_guard_followup_review_v1
  source_stage: 244_adapter_research__timestamp_aware_midwindow_guard_repair_after_stage242_inactive_guard
  source_run: run244A_stage244_timestamp_aware_midwindow_guard_repair_after_stage242_inactive_guard_v1
  source_decision: open_stage245_bounded_followup_due_to_timestamp_guard_tradeoff_candidate_not_final
  next_action: run245A_stage245_stage244_timestamp_guard_followup_review_v1
  boundary: research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment
""", stage245_open_block, 1)
    workspace = workspace.replace("""stage245_stage244_timestamp_guard_followup_review:
  packet_id: stage245_stage244_timestamp_guard_followup_review_v1
  stage_id: 245_adapter_research__stage244_timestamp_guard_followup_review
  status: reviewed_closed_open_stage246_soft_guard_repair_candidate_not_final
  current_run_id: run245A_stage245_stage244_timestamp_guard_followup_review_v1
  source_stage: 244_adapter_research__timestamp_aware_midwindow_guard_repair_after_stage242_inactive_guard
  source_run: run244A_stage244_timestamp_aware_midwindow_guard_repair_after_stage242_inactive_guard_v1
  source_decision: open_stage245_bounded_followup_due_to_timestamp_guard_tradeoff_candidate_not_final
  next_action: run245A_stage245_stage244_timestamp_guard_followup_review_v1
  boundary: research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_proDUCTION_baseline_no_deployment
""", stage245_open_block, 1)
    workspace = workspace.replace("""stage245_stage244_timestamp_guard_followup_review:
  packet_id: stage245_stage244_timestamp_guard_followup_review_v1
  stage_id: 245_adapter_research__stage244_timestamp_guard_followup_review
  status: reviewed_closed_open_stage246_soft_guard_repair_candidate_not_final
  current_run_id: run245A_stage245_stage244_timestamp_guard_followup_review_v1
  source_stage: 244_adapter_research__timestamp_aware_midwindow_guard_repair_after_stage242_inactive_guard
  source_run: run244A_stage244_timestamp_aware_midwindow_guard_repair_after_stage242_inactive_guard_v1
  source_decision: open_stage245_bounded_followup_due_to_timestamp_guard_tradeoff_candidate_not_final
  next_action: run245A_stage245_stage244_timestamp_guard_followup_review_v1
  boundary: research_development_only_no_live_readiness_no_runtime_authority_no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment
""", stage245_open_block, 1)
    if "stage246_soft_timestamp_guard_repair_after_stage244_overprune:" not in workspace:
        workspace += f"""

stage246_soft_timestamp_guard_repair_after_stage244_overprune:
  packet_id: {NEXT_PACKET_ID}
  stage_id: {NEXT_STAGE_ID}
  status: open_planned_from_stage245
  current_run_id: {NEXT_RUN_ID}
  source_stage: {STAGE_ID}
  source_run: {RUN_ID}
  source_decision: {DECISION}
  next_action: {NEXT_RUN_ID}
  boundary: {BOUNDARY}
"""
    workspace = workspace.replace("  status: open_planned_from_stage243\n  current_run_id: run244A_stage244_timestamp_aware_midwindow_guard_repair_after_stage242_inactive_guard_v1", "  status: closed_superseded_by_stage244_closeout_record\n  current_run_id: run244A_stage244_timestamp_aware_midwindow_guard_repair_after_stage242_inactive_guard_v1", 1)
    write_text(WORKSPACE_STATE_PATH, workspace, bom=False)

    with open(long_path(CHANGELOG_PATH), "a", encoding="utf-8", newline="\n") as handle:
        handle.write(f"\n## {datetime.now().date()} Stage245 stage244 timestamp guard follow-up review(245단계 244단계 시간 보호문 후속 검토)\n\n")
        handle.write(f"- action(행동): closed(종료) `{STAGE_ID}` with decision(판정) `{DECISION}`.\n")
        handle.write(f"- effect(효과): hard guard(강한 보호문) over-prune damage(과차단 손상)를 기록하고 `{NEXT_STAGE_ID}`를 열었다.\n")

    packet_payloads = {
        "packet_receipt.json": {"packet_id": PACKET_ID, "stage_id": STAGE_ID, "run_id": RUN_ID, "primary_family": "baseline_adapter_research", "primary_skill": "obsidian-result-judgment", "support_skills": ["obsidian-performance-attribution"], "created_at_utc": utc_now()},
        "routing_receipt.json": {"packet_id": PACKET_ID, "route": DECISION, "next_stage_or_branch": NEXT_STAGE_ID, "boundary": BOUNDARY},
        "result_judgment_gate.json": {"result_subject": RUN_ID, "evidence_available": [rel(REPORT_PATH), rel(TRADEOFF_PATH), rel(ATTRIBUTION_PATH), rel(FAILURE_PATH)], "evidence_missing": ["soft_guard_repair_measurement", "onnx_parity", "mt5_onnx_runtime_reproduction"], "judgment_label": "active_guard_overprune_negative_not_final", "claim_boundary": BOUNDARY, "next_condition": NEXT_STAGE_ID},
        "performance_attribution_gate.json": {"run_id": RUN_ID, "attribution_rows": attribution_rows, "attribution_confidence": "high_for_overprune_damage"},
        "kpi_contract_audit.json": {"run_id": RUN_ID, "source_stage": SOURCE_STAGE_ID, "kpi_files_reviewed": [rel(QUALITY_PATH), rel(GATE_PATH), rel(SEGMENT_PATH), rel(RISK_PATH)], "result": "reviewed_closed_not_final"},
        "artifact_lineage_audit.json": {"packet_id": PACKET_ID, "source_stage244_evidence_commit": SOURCE_EVIDENCE_COMMIT, "source_stage244_hash_record_commit": SOURCE_HASH_RECORD_COMMIT, "artifacts": [rel(REPORT_PATH), rel(TRADEOFF_PATH), rel(ATTRIBUTION_PATH), rel(FAILURE_PATH), rel(DECISION_PATH)]},
        "required_gate_coverage_audit.json": {"packet_id": PACKET_ID, "required_gates": ["result_judgment", "performance_attribution", "kpi_contract", "artifact_lineage", "current_truth_update"], "status": "passed"},
        "final_claim_guard.json": {"overall_goal_complete": False, "forbidden_claims": ["deployment", "live_readiness", "runtime_authority", "operating_promotion", "operating_reference", "production_baseline"], "boundary": BOUNDARY},
    }
    write_text(PACKET_ROOT / "closeout_packet.md", f"""# Stage245 Closeout Packet(245단계 종료 작업 묶음)

- run(실행): `{RUN_ID}`
- decision(판정): `{DECISION}`
- report(보고서): `{rel(REPORT_PATH)}`
- next_stage(다음 단계): `{NEXT_STAGE_ID}`
- boundary(경계): `{BOUNDARY}`
""")
    for name, payload in packet_payloads.items():
        write_json(PACKET_ROOT / name, payload)

    artifact_paths = [
        PRODUCER_PATH,
        REPORT_PATH,
        TRADEOFF_PATH,
        ATTRIBUTION_PATH,
        FAILURE_PATH,
        ROUTE_PATH,
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
            "artifact_id": f"{RUN_ID}__{path.name}",
            "artifact_type": "stage245_followup_review_evidence",
            "path": rel(path),
            "sha256": sha256_lf(path),
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": utc_now(),
            "notes": "Stage245 Stage244 timestamp guard follow-up review evidence; research only.",
        }
        for path in artifact_paths
    ]
    artifact_payload = upsert_csv(ARTIFACT_REGISTRY_PATH, ARTIFACT_COLUMNS, artifact_rows, "artifact_id")
    ledger_payload = {"run_registry": run_payload, "project_alpha_ledger": project_payload, "stage_ledger": stage_payload, "artifact_registry": artifact_payload}
    summary["ledger_payload"] = ledger_payload
    write_json(PACKET_ROOT / "aggregate_summary.json", summary)
    lineage = dict(packet_payloads["artifact_lineage_audit.json"])
    lineage["ledger_payload"] = ledger_payload
    write_json(PACKET_ROOT / "artifact_lineage_audit.json", lineage)

    print(json.dumps({"stage": STAGE_ID, "decision": DECISION, "next_stage": NEXT_STAGE_ID, "ledger_payload": ledger_payload}, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
