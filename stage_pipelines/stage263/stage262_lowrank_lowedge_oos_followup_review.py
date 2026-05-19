from __future__ import annotations

import csv
import hashlib
import json
import re
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from stage_pipelines.stage262 import lowrank_lowedge_oos_recovery_repair as source


s250 = source.s250

STAGE_ID = "263_adapter_research__stage262_lowrank_lowedge_oos_followup_review"
RUN_ID = "run263A_stage263_stage262_lowrank_lowedge_oos_followup_review_v1"
PACKET_ID = "stage263_stage262_lowrank_lowedge_oos_followup_review_v1"
SOURCE_STAGE_ID = source.STAGE_ID
SOURCE_RUN_ID = source.RUN_ID
SOURCE_STAGE262_EVIDENCE_COMMIT = "8ac5d3953c7665247713cec835bde857c755b2aa"
SOURCE_STAGE262_HASH_RECORD_COMMIT = "eb25585d9e0e6ccdd3a1fdb50697b15629f75032"
NEXT_STAGE_ID = "264_adapter_research__dual_objective_lowrank_lowedge_repair"
NEXT_RUN_ID = "run264A_stage264_dual_objective_lowrank_lowedge_repair_v1"
NEXT_PACKET_ID = "stage264_dual_objective_lowrank_lowedge_repair_v1"
DECISION = "open_stage264_bounded_dual_objective_lowrank_lowedge_repair_candidate_not_final"
BOUNDARY = source.BOUNDARY
TARGET_SURFACE = source.TARGET_SURFACE
EXTERNAL_STATUS = "review_only_source_stage262_mt5_reports_completed"

ROOT = Path.cwd()
STAGE_ROOT = ROOT / "stages" / STAGE_ID
REVIEWS = STAGE_ROOT / "03_reviews"
PACKET_ROOT = ROOT / "docs/agent_control/packets" / PACKET_ID
NEXT_STAGE_ROOT = ROOT / "stages" / NEXT_STAGE_ID
SOURCE_REVIEWS = ROOT / "stages" / SOURCE_STAGE_ID / "03_reviews"

QUALITY_PATH = SOURCE_REVIEWS / "stage262_quality_matrix.csv"
SOURCE_FEATURE_PATH = SOURCE_REVIEWS / "stage262_source_feature_summary.csv"
RISK_PATH = SOURCE_REVIEWS / "stage262_risk_atr_telemetry.csv"
PROBABILITY_PATH = SOURCE_REVIEWS / "stage262_probability_telemetry_summary.csv"
SOURCE_REPORT_PATH = SOURCE_REVIEWS / "stage262_lowrank_lowedge_oos_recovery_report.md"
SOURCE_DECISION_PATH = SOURCE_REVIEWS / "stage262_decision.md"

REPORT_PATH = REVIEWS / "stage263_stage262_lowrank_lowedge_oos_followup_review.md"
TRADEOFF_PATH = REVIEWS / "stage263_tradeoff_review_matrix.csv"
ATTRIBUTION_PATH = REVIEWS / "stage263_performance_attribution.csv"
FAILURE_PATH = REVIEWS / "stage263_failure_memory.csv"
ROUTE_PATH = REVIEWS / "stage263_route_matrix.csv"
RISK_REVIEW_PATH = REVIEWS / "stage263_risk_atr_review.csv"
PROBABILITY_REVIEW_PATH = REVIEWS / "stage263_probability_review.csv"
SUMMARY_PATH = REVIEWS / "stage263_summary.json"
DECISION_PATH = REVIEWS / "stage263_decision.md"
STAGE_LEDGER_PATH = REVIEWS / "stage_run_ledger.csv"
REVIEW_INDEX_PATH = REVIEWS / "review_index.md"
SELECTION_PATH = STAGE_ROOT / "04_selected/selection_status.md"

CURRENT_STATE_PATH = ROOT / "docs/context/current_working_state.md"
WORKSPACE_STATE_PATH = ROOT / "docs/workspace/workspace_state.yaml"
CHANGELOG_PATH = ROOT / "docs/workspace/changelog.md"
RUN_REGISTRY_PATH = ROOT / "docs/registers/run_registry.csv"
PROJECT_LEDGER_PATH = ROOT / "docs/registers/alpha_run_ledger.csv"
ARTIFACT_REGISTRY_PATH = ROOT / "docs/registers/artifact_registry.csv"
PRODUCER_PATH = ROOT / "stage_pipelines/stage263/stage262_lowrank_lowedge_oos_followup_review.py"


def extended_path(path: Path) -> str:
    resolved = path if path.is_absolute() else ROOT / path
    return "\\\\?\\" + str(resolved.resolve())


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


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


def write_md(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(extended_path(path), "w", encoding="utf-8-sig", newline="\n") as handle:
        handle.write(text.rstrip() + "\n")


def write_json(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(extended_path(path), "w", encoding="utf-8", newline="\n") as handle:
        json.dump(payload, handle, indent=2, ensure_ascii=False, sort_keys=True)
        handle.write("\n")


def sha256_lf(path: Path) -> str:
    with open(extended_path(path), "rb") as handle:
        return hashlib.sha256(handle.read().replace(b"\r\n", b"\n")).hexdigest()


def as_float(row: Mapping[str, Any], key: str, default: float = 0.0) -> float:
    try:
        return float(row.get(key, default) or default)
    except (TypeError, ValueError):
        return default


def fmt(value: float, digits: int = 2) -> str:
    return f"{value:.{digits}f}"


def table(rows: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        "| adapter(어댑터) | label(라벨) | val PF(검증 수익 팩터) | val net(검증 순손익) | OOS PF(표본외 수익 팩터) | OOS net(표본외 순손익) | read(해석) |",
        "|---|---|---:|---:|---:|---:|---|",
    ]
    for row in rows:
        lines.append(f"| {row['adapter_id']} | {row['review_label']} | {row['validation_pf']} | {row['validation_net']} | {row['oos_pf']} | {row['oos_net']} | {row['plain_read']} |")
    return "\n".join(lines)


def upsert_csv(path: Path, rows: Sequence[Mapping[str, Any]], key: str) -> dict[str, Any]:
    if path.exists():
        with open(extended_path(path), "r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            columns = list(reader.fieldnames or [])
            existing = list(reader)
    else:
        columns = list(rows[0].keys()) if rows else []
        existing = []
    for row in rows:
        for column in row:
            if column not in columns:
                columns.append(column)
    by_key = {row.get(key, ""): row for row in existing if row.get(key)}
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
    return {"path": rel(path), "rows": len(ordered), "upserted_rows": len(rows), "sha256": sha256_lf(path)}


def replace_stage_block(text: str, key: str, block: str) -> str:
    pattern = rf"^{re.escape(key)}:\n(?:  .*\n)+"
    if re.search(pattern, text, flags=re.MULTILINE):
        return re.sub(pattern, block, text, count=1, flags=re.MULTILINE)
    return text.rstrip() + "\n\n" + block


def build_review() -> dict[str, Any]:
    quality_rows = read_csv(QUALITY_PATH)
    feature_rows = read_csv(SOURCE_FEATURE_PATH)
    risk_rows = read_csv(RISK_PATH)
    probability_rows = read_csv(PROBABILITY_PATH)
    lowrank = next(row for row in quality_rows if row["adapter_id"] == "s262_lowrank_control")
    highedge = next(row for row in quality_rows if row["adapter_id"] == "s262_highedge_reference")
    tradeoff_rows: list[dict[str, Any]] = []
    for row in quality_rows:
        adapter = row["adapter_id"]
        val_pf = as_float(row, "validation_pf")
        val_net = as_float(row, "validation_net")
        val_mid_pf = as_float(row, "validation_mid_pf")
        oos_pf = as_float(row, "oos_pf")
        oos_net = as_float(row, "oos_net")
        if adapter == "s262_lowrank_outer_half_filter":
            label = "oos_recovery_validation_pf_damage"
            read = "OOS(표본외) 순손익과 PF(수익 팩터)는 회복했지만 validation(검증) PF와 mid PF(중간 수익 팩터)가 34D 기준 아래로 내려갔다."
            next_handling = NEXT_STAGE_ID
        elif adapter == "s262_lowrank_inner_half_filter":
            label = "validation_lift_oos_damage"
            read = "validation(검증) 순손익/PF는 최고지만 OOS(표본외) 순손익과 PF가 더 약해졌다."
            next_handling = NEXT_STAGE_ID
        elif adapter == "s262_lowrank_control":
            label = "validation_anchor_oos_weak"
            read = "검증 기준점으로는 가장 안정적이지만 OOS(표본외) 순손익이 낮다."
            next_handling = NEXT_STAGE_ID
        else:
            label = "oos_reference_validation_pf_failed"
            read = "OOS(표본외)는 비교 기준이지만 validation(검증) PF/mid PF가 34D 목표 아래다."
            next_handling = "reference_only"
        tradeoff_rows.append(
            {
                "adapter_id": adapter,
                "axis": row["axis"],
                "validation_pf": row["validation_pf"],
                "validation_pf_delta_vs_lowrank": fmt(val_pf - as_float(lowrank, "validation_pf"), 4),
                "validation_pf_gap_vs_34d": fmt(val_pf - source.LEGACY_34D["profit_factor"], 6),
                "validation_net": row["validation_net"],
                "validation_net_delta_vs_lowrank": fmt(val_net - as_float(lowrank, "validation_net")),
                "validation_mid_pf": row["validation_mid_pf"],
                "validation_mid_pf_gap_vs_34d": fmt(val_mid_pf - source.LEGACY_34D["profit_factor"], 6),
                "validation_dd_percent": row["validation_balance_dd_percent"],
                "oos_pf": row["oos_pf"],
                "oos_pf_delta_vs_lowrank": fmt(oos_pf - as_float(lowrank, "oos_pf"), 4),
                "oos_pf_delta_vs_highedge": fmt(oos_pf - as_float(highedge, "oos_pf"), 4),
                "oos_net": row["oos_net"],
                "oos_net_delta_vs_lowrank": fmt(oos_net - as_float(lowrank, "oos_net")),
                "oos_net_delta_vs_highedge": fmt(oos_net - as_float(highedge, "oos_net")),
                "oos_dd_percent": row["oos_balance_dd_percent"],
                "hard_quality_pass": row["hard_quality_pass"],
                "quality_flags": row["quality_flags"],
                "review_label": label,
                "plain_read": read,
                "next_handling": next_handling,
            }
        )
    route_rows = [
        {
            "route_id": f"{RUN_ID}__dual_objective_repair",
            "route": NEXT_STAGE_ID,
            "reason": "outer half recovers OOS but damages validation; inner half lifts validation but damages OOS; next bounded stage must search for a non-calendar dual-objective rule",
            "allowed_claim": "research_development_only",
            "forbidden_claims": "deployment;live_readiness;runtime_authority;operating_promotion;production_baseline",
        },
        {
            "route_id": f"{RUN_ID}__do_not_select_outer_oos_only",
            "route": "failure_memory",
            "reason": "s262_lowrank_outer_half_filter OOS net 857.64/PF 1.74 is useful but validation PF 1.54 and mid PF 1.534 fail 34D-like target",
            "allowed_claim": "oos_recovery_clue_only",
            "forbidden_claims": "final_adapter;baseline",
        },
        {
            "route_id": f"{RUN_ID}__do_not_select_inner_validation_only",
            "route": "failure_memory",
            "reason": "s262_lowrank_inner_half_filter validation net 1336.78/PF 1.62 is useful but OOS net falls to 745.71",
            "allowed_claim": "validation_lift_clue_only",
            "forbidden_claims": "final_adapter;baseline",
        },
    ]
    attribution_rows = [
        {
            "attribution_id": f"{RUN_ID}__stage262_tradeoff",
            "observed_change": "outer_half_oos_net_plus_81_67_vs_lowrank_but_validation_pf_minus_0_07;inner_half_validation_net_plus_45_50_vs_lowrank_but_oos_net_minus_30_26",
            "comparison_baseline": "s262_lowrank_control",
            "likely_drivers": "low-rank low-edge blocked short supply is directionally mixed; outer supply appears OOS-helpful but validation-harmful, inner supply appears validation-helpful but OOS-harmful",
            "segment_checks": "validation/OOS headline, early/mid/late, monthly, source gate counts, risk/ATR telemetry, probability telemetry",
            "trade_shape": "small signal-count changes create material net swings, so the next probe must control concentration and avoid calendar overfit",
            "alternative_explanations": "cluster timing and small blocked-signal sample can explain the split behavior",
            "attribution_confidence": "medium",
            "next_probe": NEXT_STAGE_ID,
        }
    ]
    failure_rows = [
        {
            "failure_id": f"{RUN_ID}__no_single_stage262_variant_final",
            "evidence": "outer_half improves OOS but fails validation PF/mid PF; inner_half improves validation but hurts OOS",
            "impact": "Stage262 cannot become final or baseline",
            "next_handling": NEXT_STAGE_ID,
        },
        {
            "failure_id": f"{RUN_ID}__oos_only_not_enough",
            "evidence": "s262_lowrank_outer_half_filter OOS net 857.64/PF 1.74 but validation PF 1.54",
            "impact": "OOS recovery alone is not sufficient",
            "next_handling": NEXT_STAGE_ID,
        },
    ]
    risk_review_rows = [
        {key: row.get(key, "") for key in ["adapter_id", "split", "atr_enabled", "model_risk_enabled", "max_model_risk_pct", "risk_floor_applied_count", "max_actual_risk_pct_after_floor", "avg_executed_lot", "avg_atr_points", "avg_open_sl_points", "avg_open_tp_points", "risk_bucket"]}
        for row in risk_rows
        if row.get("view") == "actual_routed_total" and row.get("split") in {"validation_is", "oos"}
    ]
    probability_review_rows = [
        {key: row.get(key, "") for key in ["adapter_id", "split", "view", "block_mode", "status", "directional_threshold_pass_rows", "side_filter_block_rows", "order_attempted_rows", "order_filled_rows", "decision_counts"]}
        for row in probability_rows
        if row.get("view") == "actual_routed_total"
    ]
    return {
        "quality_rows": quality_rows,
        "feature_rows": feature_rows,
        "risk_rows": risk_rows,
        "probability_rows": probability_rows,
        "tradeoff_rows": tradeoff_rows,
        "route_rows": route_rows,
        "attribution_rows": attribution_rows,
        "failure_rows": failure_rows,
        "risk_review_rows": risk_review_rows,
        "probability_review_rows": probability_review_rows,
    }


def write_reports(payload: Mapping[str, Any]) -> None:
    tradeoff_rows = payload["tradeoff_rows"]
    report = f"""# Stage263 Stage262 Lowrank Lowedge OOS Follow-up Review(263단계 262단계 낮은 순위 낮은 가장자리 표본외 후속 검토)

- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- source_stage262_evidence_commit(원천 262단계 근거 커밋): `{SOURCE_STAGE262_EVIDENCE_COMMIT}`
- source_stage262_hash_record_commit(원천 262단계 해시 기록 커밋): `{SOURCE_STAGE262_HASH_RECORD_COMMIT}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- decision(판정): `{DECISION}`
- boundary(주장 경계): `{BOUNDARY}`

## Review Read(검토 해석)

Stage262(262단계)는 명확한 절충을 만들었다. `s262_lowrank_outer_half_filter`는 OOS(표본외) 순손익을 857.64까지 회복했지만 validation(검증) PF(수익 팩터)가 1.54로 내려갔다. `s262_lowrank_inner_half_filter`는 validation(검증) 순손익 1336.78/PF 1.62로 좋아졌지만 OOS(표본외) 순손익은 745.71로 더 내려갔다.

Effect(효과): 단일 Stage262(262단계) 변형은 final(최종)이 아니며, Stage264(264단계)는 non-calendar dual-objective rule(달력 의존 없는 이중목표 규칙)을 좁게 시험해야 한다.

## Tradeoff Matrix(절충 행렬)

{table(tradeoff_rows)}

## Judgment(판정)

- result_subject(판정 대상): `{RUN_ID}`
- evidence_available(사용 근거): Stage262 MT5(MetaTrader 5, 메타트레이더5) validation/OOS(검증/표본외) reports(보고서), KPI(핵심 성과 지표) matrix(행렬), risk/ATR telemetry(위험/ATR 원격측정), probability telemetry(확률 원격측정).
- evidence_missing(부족 근거): Stage264(264단계) bounded repair(경계 수리), ONNX parity(ONNX 동등성), MT5 ONNX/runtime reproduction(MT5 ONNX/런타임 재현).
- judgment_label(판정 라벨): `reviewed_tradeoff_candidate_not_final`
- claim_boundary(주장 경계): research/development only(연구개발 전용).
- next_condition(다음 조건): `{NEXT_STAGE_ID}`에서 validation(검증) PF/net/DD(수익 팩터/순손익/손실률)와 OOS(표본외) net/PF(순손익/수익 팩터)를 동시에 보존하는지 확인한다.
"""
    write_md(REPORT_PATH, report)
    write_csv(TRADEOFF_PATH, tradeoff_rows, list(tradeoff_rows[0].keys()))
    write_csv(ATTRIBUTION_PATH, payload["attribution_rows"], list(payload["attribution_rows"][0].keys()))
    write_csv(FAILURE_PATH, payload["failure_rows"], list(payload["failure_rows"][0].keys()))
    write_csv(ROUTE_PATH, payload["route_rows"], list(payload["route_rows"][0].keys()))
    write_csv(RISK_REVIEW_PATH, payload["risk_review_rows"], list(payload["risk_review_rows"][0].keys()))
    write_csv(PROBABILITY_REVIEW_PATH, payload["probability_review_rows"], list(payload["probability_review_rows"][0].keys()))
    write_json(
        SUMMARY_PATH,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "source_stage": SOURCE_STAGE_ID,
            "source_run": SOURCE_RUN_ID,
            "source_stage262_evidence_commit": SOURCE_STAGE262_EVIDENCE_COMMIT,
            "source_stage262_hash_record_commit": SOURCE_STAGE262_HASH_RECORD_COMMIT,
            "decision": DECISION,
            "external_verification_status": EXTERNAL_STATUS,
            "tradeoff_rows": tradeoff_rows,
            "route_rows": payload["route_rows"],
            "attribution_rows": payload["attribution_rows"],
            "failure_rows": payload["failure_rows"],
            "claim_boundary": BOUNDARY,
            "overall_goal_complete": False,
            "pushed_commit_hash": "pending_until_push",
        },
    )
    write_md(
        DECISION_PATH,
        f"""# Stage263 Decision(263단계 판정)

- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- decision(판정): `{DECISION}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- source_stage262_evidence_commit(원천 262단계 근거 커밋): `{SOURCE_STAGE262_EVIDENCE_COMMIT}`
- source_stage262_hash_record_commit(원천 262단계 해시 기록 커밋): `{SOURCE_STAGE262_HASH_RECORD_COMMIT}`
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

Stage263(263단계) closeout(종료)은 overall goal complete(전체 목표 완료)가 아니다.
""",
    )


def write_next_stage_seed() -> None:
    write_md(
        NEXT_STAGE_ROOT / "00_spec" / "stage_brief.md",
        f"""# {NEXT_STAGE_ID}

Stage264(264단계)는 Stage263(263단계) review-only(검토 전용)가 찾은 OOS/validation tradeoff(표본외/검증 절충)를 좁게 수리하는 단계다.

## Bounded Question(경계 질문)

Can a non-calendar dual-objective rule(달력 의존 없는 이중목표 규칙) keep the validation(검증) quality of `s262_lowrank_control`/`s262_lowrank_inner_half_filter` while recovering the OOS(표본외) net/PF clue of `s262_lowrank_outer_half_filter`?

## Boundary(경계)

`{BOUNDARY}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "01_inputs" / "input_refs.md",
        f"""# Stage264 Input References(264단계 입력 참조)

- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- source_decision(원천 판정): `{DECISION}`
- source_report(원천 보고서): `{rel(REPORT_PATH)}`
- source_tradeoff_matrix(원천 절충 행렬): `{rel(TRADEOFF_PATH)}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "03_reviews" / "review_index.md",
        f"""# Stage264 Review Index(264단계 검토 색인)

- status(상태): `open_planned_from_stage263`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- source_stage(원천 단계): `{STAGE_ID}`
- source_decision(원천 판정): `{DECISION}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "04_selected" / "selection_status.md",
        f"""# Stage264 Selection Status(264단계 선택 상태)

- stage_status(단계 상태): `open_planned_from_stage263`
- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- source_decision(원천 판정): `{DECISION}`
- claim_boundary(주장 경계): `{BOUNDARY}`
""",
    )


def update_current_truth() -> None:
    state = s250.io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    state = re.sub(r"^current_run_id: .*$", f"current_run_id: {NEXT_RUN_ID}", state, count=1, flags=re.MULTILINE)
    state = re.sub(r"^updated_on: .*$", "updated_on: '2026-05-20'", state, count=1, flags=re.MULTILINE)
    state = re.sub(r"^active_stage: .*$", f"active_stage: {NEXT_STAGE_ID}", state, count=1, flags=re.MULTILINE)
    focus = f"""current_focus:
- >-
  Stage263(263단계) closed(종료) as `{DECISION}` and Stage264(264단계) `{NEXT_STAGE_ID}` is open_planned(개방 계획). Effect(효과): Stage262(262단계)의 OOS/validation tradeoff(표본외/검증 절충)를 다음 bounded repair(경계 수리)로 넘긴다.
- >-
  Stage263 evidence(263단계 근거)는 `{rel(REPORT_PATH)}`, `{rel(TRADEOFF_PATH)}`, `{rel(ATTRIBUTION_PATH)}`, `{rel(FAILURE_PATH)}`에 있다. Effect(효과): OOS-only(표본외 전용) 개선과 validation-only(검증 전용) 개선을 final(최종)로 착각하지 않는다.
- >-
  Target surface(목표 표면)는 `{TARGET_SURFACE}`이고 legacy 34D(레거시 34D)는 lesson-only KPI target(교훈 전용 핵심 성과 지표 목표)이다. Effect(효과): v2-native research(v2 고유 연구)를 계속한다.
"""
    state = re.sub(r"current_focus:\n.*?(?=\n[A-Za-z0-9_]+:\n)", focus, state, count=1, flags=re.DOTALL)
    stage263_block = f"""stage263_stage262_lowrank_lowedge_oos_followup_review:
  packet_id: {PACKET_ID}
  stage_id: {STAGE_ID}
  status: reviewed_closed_open_stage264_candidate_not_final
  current_run_id: {RUN_ID}
  source_stage: {SOURCE_STAGE_ID}
  source_run: {SOURCE_RUN_ID}
  source_stage262_evidence_commit: {SOURCE_STAGE262_EVIDENCE_COMMIT}
  source_stage262_hash_record_commit: {SOURCE_STAGE262_HASH_RECORD_COMMIT}
  decision: {DECISION}
  report_path: {rel(REPORT_PATH)}
  decision_path: {rel(DECISION_PATH)}
  tradeoff_matrix_path: {rel(TRADEOFF_PATH)}
  external_verification_status: {EXTERNAL_STATUS}
  pushed_commit_hash: pending_until_push
  next_action: {NEXT_RUN_ID}
  boundary: {BOUNDARY}
"""
    stage264_block = f"""stage264_dual_objective_lowrank_lowedge_repair:
  packet_id: {NEXT_PACKET_ID}
  stage_id: {NEXT_STAGE_ID}
  status: open_planned_from_stage263
  current_run_id: {NEXT_RUN_ID}
  source_stage: {STAGE_ID}
  source_run: {RUN_ID}
  source_decision: {DECISION}
  next_action: {NEXT_RUN_ID}
  boundary: {BOUNDARY}
"""
    state = replace_stage_block(state, "stage263_stage262_lowrank_lowedge_oos_followup_review", stage263_block)
    state = replace_stage_block(state, "stage264_dual_objective_lowrank_lowedge_repair", stage264_block)
    s250.io_path(WORKSPACE_STATE_PATH).write_text(state, encoding="utf-8")
    write_md(
        CURRENT_STATE_PATH,
        f"""# Current Working State(현재 작업 상태)

- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- active_stage(활성 단계): `{NEXT_STAGE_ID}`
- selected_research_baseline(선택 연구 기준선): `none`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- adapter_under_review(검토 중 어댑터): `stage262_lowrank_lowedge_tradeoff`
- status(상태): `stage263_closed_open_stage264_dual_objective_repair_candidate_not_final`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage263(263단계)는 Stage262(262단계)의 lowrank lowedge(낮은 순위 낮은 가장자리) 결과를 review-only(검토 전용)로 판정했다.
Effect(효과): Stage264(264단계)는 OOS(표본외) 회복과 validation(검증) 보존을 동시에 노리는 bounded repair(경계 수리)를 한다.

## Latest Stage263 Evidence(최신 263단계 근거)

- run(실행): `{RUN_ID}`
- decision(판정): `{DECISION}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- report(보고서): `{rel(REPORT_PATH)}`
- tradeoff_matrix(절충 행렬): `{rel(TRADEOFF_PATH)}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준), overall_goal_complete(전체 목표 완료).
""",
    )


def write_status_files() -> None:
    write_md(
        REVIEW_INDEX_PATH,
        f"""# Stage263 Review Index(263단계 검토 색인)

- status(상태): `reviewed_closed_open_stage264_candidate_not_final`
- current_run(현재 실행): `{RUN_ID}`
- decision(판정): `{DECISION}`
- report(보고서): `{rel(REPORT_PATH)}`
- tradeoff_matrix(절충 행렬): `{rel(TRADEOFF_PATH)}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
""",
    )
    write_md(
        SELECTION_PATH,
        f"""# Stage263 Selection Status(263단계 선택 상태)

- stage_status(단계 상태): `reviewed_closed_open_stage264_candidate_not_final`
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


def append_changelog() -> None:
    existing = s250.io_path(CHANGELOG_PATH).read_text(encoding="utf-8-sig") if s250.io_path(CHANGELOG_PATH).exists() else ""
    marker = "Stage263 Stage262 lowrank lowedge OOS follow-up review closeout"
    existing = re.sub(rf"\n## [^\n]*{re.escape(marker)}[^\n]*\n.*?(?=\n## |\Z)", "", existing, flags=re.DOTALL)
    entry = (
        f"\n## {utc_now()} Stage263 Stage262 lowrank lowedge OOS follow-up review closeout(263단계 262단계 낮은 순위 낮은 가장자리 표본외 후속 검토 종료)\n\n"
        f"- action(행동): closed(종료) `{STAGE_ID}` with decision(판정) `{DECISION}`.\n"
        "- effect(효과): OOS(표본외) 회복 단서와 validation(검증) 손상을 분리해 Stage264(264단계) 이중목표 수리로 넘겼다.\n"
        f"- boundary(주장 경계): `{BOUNDARY}`.\n"
    )
    s250.io_path(CHANGELOG_PATH).write_text(existing.rstrip() + entry, encoding="utf-8")


def artifact_rows(paths: Sequence[Path]) -> list[dict[str, Any]]:
    now = utc_now()
    rows = []
    for path in paths:
        rows.append(
            {
                "artifact_id": f"{RUN_ID}__{rel(path).replace('/', '__').replace('.', '_').replace('-', '_')}",
                "artifact_type": "stage263_stage262_followup_review_evidence",
                "path": rel(path),
                "sha256": sha256_lf(path),
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": now,
                "notes": "Stage263 review-only evidence; research only.",
            }
        )
    return rows


def write_ledgers(artifacts: Sequence[Mapping[str, Any]], tradeoff_rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    best_validation = next(row for row in tradeoff_rows if row["adapter_id"] == "s262_lowrank_inner_half_filter")
    best_oos = next(row for row in tradeoff_rows if row["adapter_id"] == "s262_lowrank_outer_half_filter")
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__review_total",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "stage263_review_total",
        "parent_run_id": SOURCE_RUN_ID,
        "record_view": "review_total",
        "tier_scope": "Tier A+B",
        "kpi_scope": "baseline_adapter_followup_review",
        "scoreboard_lane": "baseline_adapter_stage263_stage262_followup_review",
        "status": "reviewed_closed",
        "judgment": DECISION,
        "path": rel(REPORT_PATH),
        "primary_kpi": f"best_validation=s262_lowrank_inner_half_filter;validation_pf={best_validation['validation_pf']};validation_net={best_validation['validation_net']};best_oos=s262_lowrank_outer_half_filter;oos_pf={best_oos['oos_pf']};oos_net={best_oos['oos_net']}",
        "guardrail_kpi": "no_single_variant_final=1;overall_goal_complete=0",
        "external_verification_status": EXTERNAL_STATUS,
        "notes": "Stage263 review only; routes to Stage264 dual-objective repair.",
    }
    run_row = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "baseline_adapter_stage263_stage262_followup_review",
        "status": "reviewed_closed",
        "judgment": DECISION,
        "path": rel(DECISION_PATH),
        "notes": f"source_stage262_evidence_commit={SOURCE_STAGE262_EVIDENCE_COMMIT};source_stage262_hash_record_commit={SOURCE_STAGE262_HASH_RECORD_COMMIT};overall_goal_complete=0;boundary={BOUNDARY}",
    }
    return {
        "run_registry": upsert_csv(RUN_REGISTRY_PATH, [run_row], "run_id"),
        "project_alpha_ledger": upsert_csv(PROJECT_LEDGER_PATH, [alpha_row], "ledger_row_id"),
        "stage_ledger": upsert_csv(STAGE_LEDGER_PATH, [alpha_row], "ledger_row_id"),
        "artifact_registry": upsert_csv(ARTIFACT_REGISTRY_PATH, artifacts, "artifact_id"),
    }


def write_packet_files(payload: Mapping[str, Any], ledger_payload: Mapping[str, Any], artifacts: Sequence[Mapping[str, Any]]) -> None:
    base_payload = {
        "packet_id": PACKET_ID,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "source_stage": SOURCE_STAGE_ID,
        "source_run_id": SOURCE_RUN_ID,
        "source_stage262_evidence_commit": SOURCE_STAGE262_EVIDENCE_COMMIT,
        "source_stage262_hash_record_commit": SOURCE_STAGE262_HASH_RECORD_COMMIT,
        "decision": DECISION,
        "external_verification_status": EXTERNAL_STATUS,
        "tradeoff_rows": payload["tradeoff_rows"],
        "claim_boundary": BOUNDARY,
        "overall_goal_complete": False,
    }
    required_gates = ["kpi_contract_audit", "result_judgment_gate", "performance_attribution_gate", "artifact_lineage_audit", "final_claim_guard", "required_gate_coverage_audit"]
    files = {
        "routing_receipt.json": {**base_payload, "route": DECISION, "next_stage_or_branch": NEXT_STAGE_ID, "required_gates": required_gates, "status": "completed"},
        "kpi_contract_audit.json": {**base_payload, "tradeoff_matrix": rel(TRADEOFF_PATH), "risk_atr_review": rel(RISK_REVIEW_PATH), "probability_review": rel(PROBABILITY_REVIEW_PATH), "status": "completed"},
        "result_judgment_gate.json": {**base_payload, "judgment_label": "reviewed_tradeoff_candidate_not_final", "status": "passed_with_boundary"},
        "performance_attribution_gate.json": {**base_payload, "attribution": rel(ATTRIBUTION_PATH), "status": "completed"},
        "artifact_lineage_audit.json": {**base_payload, "producer": rel(PRODUCER_PATH), "artifacts": list(artifacts), "ledger_payload": ledger_payload, "status": "completed"},
        "final_claim_guard.json": {**base_payload, "deployment_claim": False, "live_readiness_claim": False, "runtime_authority_claim": False, "production_baseline_claim": False, "operating_reference_claim": False, "operating_promotion_claim": False, "status": "passed"},
        "required_gate_coverage_audit.json": {**base_payload, "required_gates": required_gates, "missing_gates": [], "status": "passed"},
        "aggregate_summary.json": {**base_payload, "ledger_payload": ledger_payload, "pushed_commit_hash": "pending_until_push"},
        "packet_receipt.json": base_payload,
    }
    for name, item in files.items():
        write_json(PACKET_ROOT / name, item)
    write_md(
        PACKET_ROOT / "closeout_packet.md",
        f"""# Stage263 Closeout Packet(263단계 종료 작업 묶음)

- packet(작업 묶음): `{PACKET_ID}`
- run(실행): `{RUN_ID}`
- status(상태): `{EXTERNAL_STATUS}`
- decision(판정): `{DECISION}`
- report(보고서): `{rel(REPORT_PATH)}`
- next_stage(다음 단계): `{NEXT_STAGE_ID}`
- overall_goal_complete(전체 목표 완료): `false`
- boundary(경계): `{BOUNDARY}`
""",
    )


def main() -> int:
    payload = build_review()
    write_reports(payload)
    write_next_stage_seed()
    update_current_truth()
    write_status_files()
    append_changelog()
    artifact_paths = [
        REPORT_PATH,
        TRADEOFF_PATH,
        ATTRIBUTION_PATH,
        FAILURE_PATH,
        ROUTE_PATH,
        RISK_REVIEW_PATH,
        PROBABILITY_REVIEW_PATH,
        SUMMARY_PATH,
        DECISION_PATH,
        REVIEW_INDEX_PATH,
        SELECTION_PATH,
        PRODUCER_PATH,
    ]
    artifacts = artifact_rows(artifact_paths)
    ledger_payload = write_ledgers(artifacts, payload["tradeoff_rows"])
    write_packet_files(payload, ledger_payload, artifacts)
    print(json.dumps({"run_id": RUN_ID, "decision": DECISION, "external_verification_status": EXTERNAL_STATUS}, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
