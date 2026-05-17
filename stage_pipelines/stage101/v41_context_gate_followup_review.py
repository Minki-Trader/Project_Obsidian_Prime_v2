from __future__ import annotations

import csv
import json
import re
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.control_plane.ledger import (  # noqa: E402
    ALPHA_LEDGER_COLUMNS,
    RUN_REGISTRY_COLUMNS,
    io_path,
    json_ready,
    ledger_pairs,
    sha256_file_lf_normalized,
    upsert_csv_rows,
)


STAGE_ID = "101_adapter_research__v41_context_gate_followup_review"
RUN_ID = "run101A_stage101_v41_context_gate_followup_review_v1"
PACKET_ID = "stage101_v41_context_gate_followup_review_v1"
PARENT_RUN_ID = "run100A_stage100_v41_oos_early_context_gate_runtime_repair_v1"
SOURCE_STAGE100_ID = "100_adapter_research__v41_oos_early_context_gate_runtime_repair"
SOURCE_STAGE100_CLOSEOUT_COMMIT = "85d881d1b0df85768f8fb38dfe0afe6a7877a7fd"
SOURCE_STAGE100_LATEST_COMMIT = "ef4b4ab1fbcb63a985512af5a6c49d199533e1fd"
SOURCE_STAGE99_LATEST_COMMIT = "31354b3fad25e66e10159bd9870ee1da87defeeb"
TARGET_SURFACE = "legacy_34d_kpi_lesson_only_no_legacy_inheritance"
DECISION = "continue_oos_net_density_dd_repair_in_stage102"
NEXT_STAGE_ID = "102_adapter_research__v41_oos_net_density_dd_repair"
NEXT_RUN_ID = "run102A_stage102_v41_oos_net_density_dd_repair_v1"
NEXT_PACKET_ID = "stage102_v41_oos_net_density_dd_repair_v1"
EXTERNAL_STATUS = "completed_existing_stage100_mt5_runtime_evidence_reviewed"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment"
)

LEGACY_34D_LATEST = {
    "profit_factor": 1.583157,
    "net_profit": 987.60,
    "max_drawdown_percent": 12.909136,
    "trade_count": 404,
}

STAGE_ROOT = Path("stages") / STAGE_ID
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
SELECTED_ROOT = STAGE_ROOT / "04_selected"
PACKET_ROOT = Path("docs/agent_control/packets") / PACKET_ID
NEXT_STAGE_ROOT = Path("stages") / NEXT_STAGE_ID

SOURCE_REVIEWS = Path("stages") / SOURCE_STAGE100_ID / "03_reviews"
SOURCE_SUMMARY = SOURCE_REVIEWS / "stage100_context_gate_runtime_repair_summary.csv"
SOURCE_SEGMENTS = SOURCE_REVIEWS / "stage100_segment_kpi_summary.csv"
SOURCE_GATES = SOURCE_REVIEWS / "stage100_gate_feature_summary.csv"
SOURCE_RISK_ATR = SOURCE_REVIEWS / "stage100_risk_atr_telemetry.csv"
SOURCE_DECISION = SOURCE_REVIEWS / "stage100_decision.md"
SOURCE_REPORT = SOURCE_REVIEWS / "stage100_context_gate_runtime_repair_report.md"
SOURCE_STAGE99_PROJECTION = (
    Path("stages")
    / "99_adapter_research__v41_oos_early_side_session_context_repair"
    / "03_reviews"
    / "stage99_context_gate_projection.csv"
)

REPORT_PATH = REVIEWS_ROOT / "stage101_context_gate_followup_review.md"
KPI_GAP_PATH = REVIEWS_ROOT / "stage101_34d_kpi_gap_summary.csv"
SEGMENT_GAP_PATH = REVIEWS_ROOT / "stage101_segment_gap_summary.csv"
PROJECTION_RUNTIME_PATH = REVIEWS_ROOT / "stage101_projection_runtime_delta.csv"
DECISION_PATH = REVIEWS_ROOT / "stage101_decision.md"
STAGE_LEDGER_PATH = REVIEWS_ROOT / "stage_run_ledger.csv"

RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
PROJECT_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
ARTIFACT_REGISTRY_PATH = Path("docs/registers/artifact_registry.csv")
WORKSPACE_STATE_PATH = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE_PATH = Path("docs/context/current_working_state.md")
CHANGELOG_PATH = Path("docs/workspace/changelog.md")


def rel(path: Path | str) -> str:
    return Path(path).as_posix()


def read_csv(path: Path) -> list[dict[str, str]]:
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: row.get(column, "") for column in columns})


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text, encoding="utf-8-sig")


def write_json(path: Path, payload: Mapping[str, Any]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(
        json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def num(row: Mapping[str, Any], key: str) -> float | None:
    value = row.get(key)
    if value is None or str(value).strip() == "":
        return None
    try:
        return float(str(value))
    except ValueError:
        return None


def fmt(value: float | None, digits: int = 6) -> str:
    return "" if value is None else f"{value:.{digits}f}"


def routed_rows() -> list[dict[str, str]]:
    return [
        row
        for row in read_csv(SOURCE_SUMMARY)
        if row.get("view") == "actual_routed_total"
        and row.get("split") in {"validation_is", "oos"}
        and row.get("status") == "completed"
    ]


def full_segment_lookup() -> dict[tuple[str, str], dict[str, str]]:
    lookup: dict[tuple[str, str], dict[str, str]] = {}
    for row in read_csv(SOURCE_SEGMENTS):
        if row.get("view") != "actual_routed_total":
            continue
        if row.get("segment_type") != "full_split":
            continue
        lookup[(row.get("adapter_id", ""), row.get("split", ""))] = row
    return lookup


def kpi_gap_rows(rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    precise = full_segment_lookup()
    for row in rows:
        segment_row = precise.get((row.get("adapter_id", ""), row.get("split", "")), {})
        pf = num(segment_row, "profit_factor") if segment_row else num(row, "profit_factor")
        net = num(segment_row, "net_profit") if segment_row else num(row, "net_profit")
        dd = num(row, "max_drawdown_percent")
        trades = num(segment_row, "trade_count") if segment_row else num(row, "trade_count")
        expectancy = segment_row.get("expectancy", row.get("expectancy", "")) if segment_row else row.get("expectancy", "")
        pf_gap = None if pf is None else pf - LEGACY_34D_LATEST["profit_factor"]
        net_gap = None if net is None else net - LEGACY_34D_LATEST["net_profit"]
        dd_gap = None if dd is None else dd - LEGACY_34D_LATEST["max_drawdown_percent"]
        trade_gap = None if trades is None else trades - LEGACY_34D_LATEST["trade_count"]
        if row.get("split") == "oos" and row.get("adapter_id") == "s100_v41_h3_cd8_lng_early_adx20":
            read = "best_stage100_runtime_surface_pf_met_net_dd_not_met"
        elif row.get("split") == "oos":
            read = "oos_pf_near_target_but_net_dd_gap_remains"
        else:
            read = "validation_strong_but_dd_above_34d_surface"
        output.append(
            {
                "run_id": RUN_ID,
                "source_run_id": PARENT_RUN_ID,
                "adapter_id": row.get("adapter_id", ""),
                "repair_label": row.get("repair_label", ""),
                "split": row.get("split", ""),
                "profit_factor": fmt(pf),
                "net_profit": fmt(net, 2),
                "max_drawdown_percent": fmt(dd, 6),
                "trade_count": fmt(trades, 0),
                "expectancy": expectancy,
                "cost_stressed_expectancy": row.get("cost_stressed_expectancy", ""),
                "pf_gap_to_34d_latest": fmt(pf_gap),
                "net_gap_to_34d_latest": fmt(net_gap, 2),
                "dd_percent_gap_to_34d_latest": fmt(dd_gap, 6),
                "trade_count_gap_to_34d_latest": fmt(trade_gap, 0),
                "stage101_read": read,
            }
        )
    return output


def segment_gap_rows() -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for row in read_csv(SOURCE_SEGMENTS):
        if row.get("view") != "actual_routed_total":
            continue
        if row.get("split") != "oos":
            continue
        if row.get("segment_type") not in {"full_split", "chronological_third"}:
            continue
        segment = row.get("segment", "")
        pf = num(row, "profit_factor")
        net = num(row, "net_profit")
        mfe_capture = num(row, "mfe_capture_ratio")
        if row.get("segment_type") == "full_split":
            read = "full_oos_positive_but_net_scale_and_dd_gap_remain"
        elif segment == "early":
            read = "oos_early_repaired_from_negative_but_still_low_net_and_mfe_capture"
        elif segment == "mid":
            read = "oos_mid_carries_most_profit"
        else:
            read = "oos_late_positive_but_not_enough_to_close_net_gap"
        output.append(
            {
                "run_id": RUN_ID,
                "adapter_id": row.get("adapter_id", ""),
                "split": row.get("split", ""),
                "segment_type": row.get("segment_type", ""),
                "segment": segment,
                "trade_count": row.get("trade_count", ""),
                "net_profit": fmt(net, 2),
                "profit_factor": fmt(pf),
                "expectancy": row.get("expectancy", ""),
                "mfe_capture_ratio": fmt(mfe_capture),
                "max_closed_trade_drawdown": row.get("max_closed_trade_drawdown", ""),
                "stage101_read": read,
            }
        )
    return output


def projection_runtime_delta_rows(rows: Sequence[Mapping[str, str]]) -> list[dict[str, Any]]:
    projection_rows = read_csv(SOURCE_STAGE99_PROJECTION)
    projection_key = {
        (row["candidate_gate"], row["split"]): row
        for row in projection_rows
        if row.get("adapter_id") == "s97_v41_h3_risk475_gate08_sl2075_tp40_cd8"
    }
    gate_map = {
        "s100_v41_h3_cd8_lng_earlymid_adx20": "long_early_mid_range_adxlt20",
        "s100_v41_h3_cd8_lng_early_adx20": "long_early_range_adxlt20",
    }
    output: list[dict[str, Any]] = []
    for row in rows:
        split = row["split"]
        gate = gate_map.get(row["adapter_id"])
        projected = projection_key.get((gate or "", split), {})
        runtime_net = num(row, "net_profit")
        runtime_pf = num(row, "profit_factor")
        projected_net = num(projected, "projected_net")
        projected_pf = num(projected, "projected_profit_factor")
        output.append(
            {
                "run_id": RUN_ID,
                "adapter_id": row.get("adapter_id", ""),
                "candidate_gate": gate or "",
                "split": split,
                "projected_net": fmt(projected_net, 2),
                "runtime_net": fmt(runtime_net, 2),
                "runtime_minus_projected_net": fmt(
                    None if projected_net is None or runtime_net is None else runtime_net - projected_net,
                    2,
                ),
                "projected_profit_factor": fmt(projected_pf),
                "runtime_profit_factor": fmt(runtime_pf),
                "runtime_minus_projected_pf": fmt(
                    None if projected_pf is None or runtime_pf is None else runtime_pf - projected_pf,
                    6,
                ),
                "stage101_read": "runtime_confirmed_projection_direction_with_remaining_gap",
            }
        )
    return output


def best_oos_row(rows: Sequence[Mapping[str, Any]]) -> Mapping[str, Any]:
    candidates = [row for row in rows if row.get("split") == "oos"]
    return max(
        candidates,
        key=lambda row: (
            float(str(row.get("profit_factor") or "0")),
            float(str(row.get("net_profit") or "0")),
            -float(str(row.get("max_drawdown_percent") or "999")),
        ),
    )


def report_markdown(gaps: Sequence[Mapping[str, Any]], segments: Sequence[Mapping[str, Any]], deltas: Sequence[Mapping[str, Any]]) -> str:
    best = best_oos_row(gaps)
    early = [
        row
        for row in segments
        if row.get("adapter_id") == best["adapter_id"]
        and row.get("segment_type") == "chronological_third"
        and row.get("segment") == "early"
    ][0]
    mid = [
        row
        for row in segments
        if row.get("adapter_id") == best["adapter_id"]
        and row.get("segment_type") == "chronological_third"
        and row.get("segment") == "mid"
    ][0]
    late = [
        row
        for row in segments
        if row.get("adapter_id") == best["adapter_id"]
        and row.get("segment_type") == "chronological_third"
        and row.get("segment") == "late"
    ][0]
    lines = [
        "# Stage101 Context Gate Follow-up Review(101단계 문맥 제한문 후속 검토)",
        "",
        f"- run(실행): `{RUN_ID}`",
        f"- source_run(원천 실행): `{PARENT_RUN_ID}`",
        f"- source_stage100_closeout_commit(원천 100단계 종료 커밋): `{SOURCE_STAGE100_CLOSEOUT_COMMIT}`",
        f"- source_stage100_latest_commit(원천 100단계 최신 커밋): `{SOURCE_STAGE100_LATEST_COMMIT}`",
        f"- target_surface(목표 표면): `{TARGET_SURFACE}`",
        f"- decision(판정): `{DECISION}`",
        f"- boundary(경계): `{BOUNDARY}`",
        "",
        "## Bounded Question(경계 질문)",
        "",
        "Stage100(100단계)의 실제 MT5 runtime(실행환경) 문맥 제한문 수리가 34D KPI(34D 핵심 성과 지표) 목표 표면에 충분히 가까워졌는가, 아니면 다음 좁은 수리가 필요한가?",
        "",
        "Effect(효과): Stage101(101단계)은 새 최적화가 아니라 판독과 다음 수리축 선택만 한다.",
        "",
        "## 34D Gap Read(34D 차이 판독)",
        "",
        "| adapter(어댑터) | split(분할) | PF gap(PF 차이) | net gap(순손익 차이) | DD gap(손실률 차이) | trade gap(거래 수 차이) | read(판독) |",
        "|---|---|---:|---:|---:|---:|---|",
    ]
    for row in gaps:
        lines.append(
            f"| {row['adapter_id']} | {row['split']} | {row['pf_gap_to_34d_latest']} | {row['net_gap_to_34d_latest']} | {row['dd_percent_gap_to_34d_latest']} | {row['trade_count_gap_to_34d_latest']} | {row['stage101_read']} |"
        )
    lines.extend(
        [
            "",
            "## Best Runtime Surface(최선 실행환경 표면)",
            "",
            f"- best_adapter(최선 어댑터): `{best['adapter_id']}`",
            f"- OOS PF(표본외 수익 팩터): `{best['profit_factor']}` versus 34D latest(34D 최신) `{LEGACY_34D_LATEST['profit_factor']}`",
            f"- OOS net(표본외 순손익): `{best['net_profit']}` versus 34D latest(34D 최신) `{LEGACY_34D_LATEST['net_profit']}`",
            f"- OOS DD%(표본외 손실률): `{best['max_drawdown_percent']}` versus 34D latest(34D 최신) `{LEGACY_34D_LATEST['max_drawdown_percent']}`",
            f"- OOS early(표본외 초반): net(순손익) `{early['net_profit']}`, PF(수익 팩터) `{early['profit_factor']}`, MFE capture(MFE 포착률) `{early['mfe_capture_ratio']}`",
            f"- OOS mid(표본외 중반): net(순손익) `{mid['net_profit']}`, PF(수익 팩터) `{mid['profit_factor']}`",
            f"- OOS late(표본외 후반): net(순손익) `{late['net_profit']}`, PF(수익 팩터) `{late['profit_factor']}`",
            "",
            "## Projection vs Runtime(투영 대비 실행환경)",
            "",
            "| adapter(어댑터) | split(분할) | runtime net - projected net(실행 순손익 - 투영 순손익) | runtime PF - projected PF(실행 PF - 투영 PF) |",
            "|---|---|---:|---:|",
        ]
    )
    for row in deltas:
        lines.append(
            f"| {row['adapter_id']} | {row['split']} | {row['runtime_minus_projected_net']} | {row['runtime_minus_projected_pf']} |"
        )
    lines.extend(
        [
            "",
            "## Decision(판정)",
            "",
            f"decision(판정): `{DECISION}`",
            "",
            "Stage100(100단계)는 좋은 방향이다. 특히 early-only gate(초반 전용 제한문)는 OOS PF(표본외 수익 팩터)를 34D 최신 목표보다 아주 조금 넘겼다.",
            "",
            "하지만 OOS net(표본외 순손익), DD%(손실률), trade density(거래 밀도)는 아직 34D 목표 표면에 부족하다. OOS early(표본외 초반)는 음수에서 벗어났지만 이익 규모와 MFE capture(MFE 포착률)가 낮다.",
            "",
            "Effect(효과): Stage102(102단계)는 OOS PF를 보존하면서 net density(순손익 밀도)와 DD(손실률)를 좁게 수리한다.",
            "",
            "Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), legacy inheritance(레거시 상속).",
        ]
    )
    return "\n".join(lines) + "\n"


def decision_markdown() -> str:
    return f"""# Stage101 Decision(101단계 판정)

decision(판정): `{DECISION}`

Stage101(101단계)은 Stage100(100단계)의 실제 MT5 runtime(실행환경) 근거만 후속 검토했다.

Effect(효과): Stage100(100단계)의 개선은 보존하되, 전체 목표 완료로 오해하지 않고 Stage102(102단계) 수리축으로 넘긴다.

## Evidence(근거)

- report(보고서): `{rel(REPORT_PATH)}`
- 34d_kpi_gap_summary(34D 핵심 성과 지표 차이 요약): `{rel(KPI_GAP_PATH)}`
- segment_gap_summary(구간 차이 요약): `{rel(SEGMENT_GAP_PATH)}`
- projection_runtime_delta(투영 대비 실행환경 차이): `{rel(PROJECTION_RUNTIME_PATH)}`
- source_stage100_summary(원천 100단계 요약): `{rel(SOURCE_SUMMARY)}`
- source_stage100_segment_kpi(원천 100단계 구간 KPI): `{rel(SOURCE_SEGMENTS)}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- pushed_commit_hash(푸시된 커밋 해시): `pending_until_push`

## Read(판독)

- Stage100 best(100단계 최선): `s100_v41_h3_cd8_lng_early_adx20`
- OOS PF(표본외 수익 팩터)는 34D 최신 목표를 아주 작게 초과했다.
- OOS net(표본외 순손익)은 34D 최신 목표보다 낮다.
- OOS DD%(표본외 손실률)는 34D 최신 목표보다 높다.
- OOS early(표본외 초반)는 회복됐지만 아직 약하다.

## Next(다음)

next_stage_or_branch(다음 단계/분기): `{NEXT_STAGE_ID}`

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), legacy inheritance(레거시 상속).
"""


def ledger_rows(gaps: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    best = best_oos_row(gaps)
    primary = ledger_pairs(
        [
            ("best_oos_adapter", best["adapter_id"]),
            ("oos_pf", best["profit_factor"]),
            ("oos_net", best["net_profit"]),
            ("oos_dd_pct", best["max_drawdown_percent"]),
        ]
    )
    guardrail = ledger_pairs(
        [
            ("pf_gap_to_34d", best["pf_gap_to_34d_latest"]),
            ("net_gap_to_34d", best["net_gap_to_34d_latest"]),
            ("dd_gap_to_34d", best["dd_percent_gap_to_34d_latest"]),
            ("trade_gap_to_34d", best["trade_count_gap_to_34d_latest"]),
        ]
    )
    return [
        {
            "ledger_row_id": f"{RUN_ID}__review_gate",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "review_gate",
            "parent_run_id": PARENT_RUN_ID,
            "record_view": "stage101_review_gate",
            "tier_scope": "Tier A+B",
            "kpi_scope": "stage101_v41_context_gate_followup_review",
            "scoreboard_lane": "regular_risk_execution_review",
            "status": "reviewed",
            "judgment": DECISION,
            "path": rel(DECISION_PATH),
            "primary_kpi": primary,
            "guardrail_kpi": guardrail,
            "external_verification_status": EXTERNAL_STATUS,
            "notes": "Review-only gate using Stage100 MT5 runtime evidence; no new runtime claim.",
        }
    ]


def write_ledgers(gaps: Sequence[Mapping[str, Any]]) -> Mapping[str, Any]:
    rows = ledger_rows(gaps)
    write_csv(STAGE_LEDGER_PATH, rows, ALPHA_LEDGER_COLUMNS)
    project = upsert_csv_rows(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, rows, key="ledger_row_id")
    registry = upsert_csv_rows(
        RUN_REGISTRY_PATH,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "baseline_adapter_v2_native_v41_context_gate_followup_review",
                "status": "reviewed",
                "judgment": DECISION,
                "path": rel(DECISION_PATH),
                "notes": (
                    "source_run=run100A_stage100_v41_oos_early_context_gate_runtime_repair_v1;"
                    f"source_stage100_latest_commit={SOURCE_STAGE100_LATEST_COMMIT};"
                    f"target_surface={TARGET_SURFACE};legacy_relation=lesson_only;new_runtime=no_review_gate_only"
                ),
            }
        ],
        key="run_id",
    )
    return {"stage_ledger_path": rel(STAGE_LEDGER_PATH), "project_ledger": project, "run_registry": registry}


def packet_files(ledger_payload: Mapping[str, Any]) -> None:
    write_json(
        PACKET_ROOT / "routing_receipt.json",
        {
            "packet_id": PACKET_ID,
            "stage_id": STAGE_ID,
            "primary_family": "result_judgment",
            "primary_skill": "obsidian-result-judgment",
            "support_skills": ["obsidian-performance-attribution", "obsidian-model-validation"],
            "required_gates": ["runtime_evidence_gate", "kpi_contract_audit", "result_judgment_gate"],
            "status": "completed",
        },
    )
    write_json(
        PACKET_ROOT / "runtime_evidence_gate.json",
        {
            "packet_id": PACKET_ID,
            "run_id": RUN_ID,
            "external_verification_status": EXTERNAL_STATUS,
            "source_runtime_summary": rel(SOURCE_SUMMARY),
            "source_segment_summary": rel(SOURCE_SEGMENTS),
            "claim_boundary": BOUNDARY,
            "new_runtime": False,
        },
    )
    write_json(
        PACKET_ROOT / "result_judgment_gate.json",
        {
            "packet_id": PACKET_ID,
            "run_id": RUN_ID,
            "decision": DECISION,
            "legacy_relation": "lesson_only_target_surface_no_code_copy",
            "overall_goal_complete": False,
            "forbidden_claims": [
                "deployment",
                "live_readiness",
                "production_baseline",
                "operating_promotion",
                "operating_reference",
                "runtime_authority",
                "legacy_inheritance",
            ],
        },
    )
    write_json(
        PACKET_ROOT / "aggregate_summary.json",
        {
            "packet_id": PACKET_ID,
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "decision": DECISION,
            "source_stage100_closeout_commit": SOURCE_STAGE100_CLOSEOUT_COMMIT,
            "source_stage100_latest_commit": SOURCE_STAGE100_LATEST_COMMIT,
            "kpi_gap_path": rel(KPI_GAP_PATH),
            "segment_gap_path": rel(SEGMENT_GAP_PATH),
            "projection_runtime_delta_path": rel(PROJECTION_RUNTIME_PATH),
            "ledger_payload": ledger_payload,
            "pushed_commit_hash": "pending_until_push",
            "overall_goal_complete": False,
        },
    )


def artifact_rows() -> list[dict[str, Any]]:
    created = datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    paths = [
        (REPORT_PATH, "stage101_v41_context_gate_followup_review_evidence", "Stage101 bounded review report."),
        (KPI_GAP_PATH, "stage101_v41_context_gate_followup_review_evidence", "Stage101 34D KPI gap summary."),
        (SEGMENT_GAP_PATH, "stage101_v41_context_gate_followup_review_evidence", "Stage101 segment gap summary."),
        (PROJECTION_RUNTIME_PATH, "stage101_v41_context_gate_followup_review_evidence", "Stage101 projection/runtime delta summary."),
        (DECISION_PATH, "stage101_v41_context_gate_followup_review_evidence", "Stage101 decision."),
        (STAGE_LEDGER_PATH, "stage101_v41_context_gate_followup_review_evidence", "Stage101 local ledger."),
        (PACKET_ROOT / "aggregate_summary.json", "packet_summary", "Stage101 packet aggregate summary."),
        (PACKET_ROOT / "routing_receipt.json", "packet_control", "Stage101 routing receipt."),
        (PACKET_ROOT / "runtime_evidence_gate.json", "packet_control", "Stage101 runtime evidence gate."),
        (PACKET_ROOT / "result_judgment_gate.json", "packet_control", "Stage101 result judgment gate."),
    ]
    return [
        {
            "artifact_id": f"{RUN_ID}__{path.name}",
            "artifact_type": artifact_type,
            "path": rel(path),
            "sha256": sha256_file_lf_normalized(path),
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": created,
            "notes": notes,
        }
        for path, artifact_type, notes in paths
    ]


def update_artifact_registry() -> Mapping[str, Any]:
    return upsert_csv_rows(
        ARTIFACT_REGISTRY_PATH,
        ("artifact_id", "artifact_type", "path", "sha256", "stage_id", "run_id", "created_at_utc", "notes"),
        artifact_rows(),
        key="artifact_id",
    )


def create_next_stage() -> None:
    write_md(
        NEXT_STAGE_ROOT / "00_spec" / "stage_brief.md",
        f"""# {NEXT_STAGE_ID}

Stage102(102단계)는 Stage101(101단계) 판정에 따라 OOS net density(표본외 순손익 밀도)와 DD(손실률)를 좁게 수리한다.

## Bounded Question(경계 질문)

Stage100 best(100단계 최선)인 `s100_v41_h3_cd8_lng_early_adx20`의 OOS PF(표본외 수익 팩터) 개선을 보존하면서 OOS net(표본외 순손익), trade density(거래 밀도), DD%(손실률)를 34D target surface(34D 목표 표면)에 더 가깝게 만들 수 있는가?

Effect(효과): Stage102(102단계)는 새 광범위 탐색이 아니라 Stage100(100단계)의 좋은 방향을 유지하며 부족한 KPI(핵심 성과 지표)만 좁게 수리한다.

## Boundary(경계)

`{BOUNDARY}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "01_inputs" / "input_refs.md",
        f"""# Stage102 Input References(102단계 입력 참조)

- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- source_decision(원천 판정): `{DECISION}`
- source_report(원천 보고서): `{rel(REPORT_PATH)}`
- source_kpi_gap_summary(원천 KPI 차이 요약): `{rel(KPI_GAP_PATH)}`
- source_segment_gap_summary(원천 구간 차이 요약): `{rel(SEGMENT_GAP_PATH)}`
- source_stage100_summary(원천 100단계 요약): `{rel(SOURCE_SUMMARY)}`
- target_surface(목표 표면): `{TARGET_SURFACE}`

Effect(효과): Stage102(102단계)는 Stage101(101단계)의 판독 근거를 그대로 이어받아, 수리 범위를 넓히지 않는다.
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "03_reviews" / "review_index.md",
        f"""# Stage102 Review Index(102단계 검토 색인)

- status(상태): `open_planned`
- source_decision(원천 판정): `{DECISION}`
- planned_packet(계획 작업 묶음): `{NEXT_PACKET_ID}`
- planned_run(계획 실행): `{NEXT_RUN_ID}`

Effect(효과): Stage102(102단계)는 Stage101(101단계) closeout(종료 기록)을 받아 좁은 수리만 수행한다.
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "04_selected" / "selection_status.md",
        f"""# Stage102 Selection Status(102단계 선택 상태)

- stage_status(단계 상태): `open_planned`
- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- source_stage(원천 단계): `{STAGE_ID}`
- source_decision(원천 판정): `{DECISION}`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Effect(효과): Stage102(102단계)는 34D KPI(34D 핵심 성과 지표) 격차 축소를 계속하지만, 운영 의미 없이 연구개발로만 이어진다.
""",
    )


def update_current_truth() -> None:
    text = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    text = re.sub(r"^current_run_id: .*$", f"current_run_id: {NEXT_RUN_ID}", text, count=1, flags=re.MULTILINE)
    text = re.sub(r"^updated_on: .*$", "updated_on: '2026-05-18'", text, count=1, flags=re.MULTILINE)
    text = re.sub(r"^active_stage: .*$", f"active_stage: {NEXT_STAGE_ID}", text, count=1, flags=re.MULTILINE)
    current_focus = f"""current_focus:
- >-
  Stage101(101단계) closed(종료) as `{DECISION}` and Stage102(102단계) `{NEXT_STAGE_ID}` is open_planned(열림 계획). Effect(효과): Stage100(100단계)의 PF(수익 팩터) 개선은 보존하고 OOS net/DD/trade density(표본외 순손익/손실률/거래 밀도) 수리로 넘긴다.
- >-
  Stage101 result(101단계 결과)는 `{rel(KPI_GAP_PATH)}`와 `{rel(SEGMENT_GAP_PATH)}`에 기록된다. Effect(효과): 34D target surface(34D 목표 표면) 대비 남은 KPI(핵심 성과 지표) 차이를 다음 단계 입력으로 보존한다.
- >-
  Target surface(목표 표면)는 `{TARGET_SURFACE}`이고 legacy 34D(레거시 34D)는 lesson-only KPI target(교훈 전용 핵심 성과 지표 목표)이다. Effect(효과): 목표는 높게 유지하지만 v2-native research(브이투 고유 연구)만 계속한다.
"""
    text = re.sub(r"current_focus:\n.*?\n\nstage", current_focus.rstrip() + "\n\nstage", text, count=1, flags=re.DOTALL)
    block = f"""

stage101_v41_context_gate_followup_review:
  packet_id: {PACKET_ID}
  stage_id: {STAGE_ID}
  status: closed_{DECISION}
  current_run_id: {RUN_ID}
  source_stage100_closeout_commit: {SOURCE_STAGE100_CLOSEOUT_COMMIT}
  source_stage100_latest_commit: {SOURCE_STAGE100_LATEST_COMMIT}
  source_stage99_latest_commit: {SOURCE_STAGE99_LATEST_COMMIT}
  target_surface: {TARGET_SURFACE}
  decision: {DECISION}
  next_stage_or_branch: {NEXT_STAGE_ID}
  report_path: {rel(REPORT_PATH)}
  decision_path: {rel(DECISION_PATH)}
  packet_summary_path: {rel(PACKET_ROOT / "aggregate_summary.json")}
  external_verification_status: {EXTERNAL_STATUS}
  pushed_commit_hash: pending_until_push
  boundary: {BOUNDARY}
"""
    marker = "stage101_v41_context_gate_followup_review:"
    if marker in text:
        text = re.sub(r"\nstage101_v41_context_gate_followup_review:\n(?:  .*\n)+", block + "\n", text, count=1)
    else:
        text = text.rstrip() + block + "\n"
    io_path(WORKSPACE_STATE_PATH).write_text(text.rstrip() + "\n", encoding="utf-8-sig")

    write_md(
        SELECTED_ROOT / "selection_status.md",
        f"""# Stage101 Selection Status(101단계 선택 상태)

- stage_status(단계 상태): `closed_{DECISION}`
- current_packet(현재 작업 묶음): `{PACKET_ID}`
- current_run(현재 실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE100_ID}`
- source_decision(원천 판정): `continue_context_gate_followup_review_in_stage101`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- stage101_decision(101단계 판정): `{DECISION}`
- next_stage_or_branch(다음 단계/분기): `{NEXT_STAGE_ID}`
- pushed_commit_hash(푸시된 커밋 해시): `pending_until_push`
- claim_boundary(주장 경계): `{BOUNDARY}`

Effect(효과): Stage101(101단계)은 Stage100(100단계) 실제 실행 결과를 판독하고, 운영 의미 없이 Stage102(102단계)로 넘긴다.
""",
    )
    write_md(
        CURRENT_WORKING_STATE_PATH,
        f"""# Current Working State(현재 작업 상태)

- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- active_stage(활성 단계): `{NEXT_STAGE_ID}`
- selected_research_baseline(선택 연구 기준): `research_package_only_reference_surface`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- adapter_under_review(검토 중 어댑터): `s100_v41_h3_cd8_lng_early_adx20`
- status(상태): `stage101_closed_{DECISION}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage101(101단계) closed(종료) as v2-native v41 context gate follow-up review(브이투 고유 브이41 문맥 제한문 후속 검토). Effect(효과): legacy 34D(레거시 34D)는 target surface(목표 표면)로만 쓰였고, 다음 연구는 Stage102(102단계)로 이어진다.

## Latest Stage101 Evidence(최신 101단계 근거)

- run(실행): `{RUN_ID}`
- decision(판정): `{DECISION}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- report(보고서): `{rel(REPORT_PATH)}`
- kpi_gap_summary(KPI 차이 요약): `{rel(KPI_GAP_PATH)}`
- segment_gap_summary(구간 차이 요약): `{rel(SEGMENT_GAP_PATH)}`
- projection_runtime_delta(투영 대비 실행환경 차이): `{rel(PROJECTION_RUNTIME_PATH)}`

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준선), legacy_inheritance(레거시 상속).
""",
    )
    create_next_stage()


def append_changelog() -> None:
    existing = io_path(CHANGELOG_PATH).read_text(encoding="utf-8-sig")
    existing = existing.replace(
        "continue_context_gate_repair_or_branch_review_in_stage101",
        "continue_context_gate_followup_review_in_stage101",
    )
    entry = (
        "\n## 2026-05-18 - Stage101 v41 context gate follow-up review closeout(101단계 v41 문맥 제한문 후속 검토 종료)\n\n"
        f"- run(실행): `{RUN_ID}`\n"
        f"- decision(판정): `{DECISION}`\n"
        "- pushed_commit_hash(푸시된 커밋 해시): `pending_until_push`\n"
        f"- target_surface(목표 표면): `{TARGET_SURFACE}`\n"
        "- effect(효과): Stage100(100단계)의 PF(수익 팩터) 개선은 확인했지만 OOS net/DD/trade density(표본외 순손익/손실률/거래 밀도)가 34D KPI(34D 핵심 성과 지표) 목표에 부족해 Stage102(102단계) 수리로 넘겼다.\n"
    )
    if RUN_ID not in existing:
        existing = existing.rstrip() + entry
    io_path(CHANGELOG_PATH).write_text(existing, encoding="utf-8-sig")


def main() -> int:
    rows = routed_rows()
    gaps = kpi_gap_rows(rows)
    segments = segment_gap_rows()
    deltas = projection_runtime_delta_rows(rows)
    write_csv(
        KPI_GAP_PATH,
        gaps,
        (
            "run_id",
            "source_run_id",
            "adapter_id",
            "repair_label",
            "split",
            "profit_factor",
            "net_profit",
            "max_drawdown_percent",
            "trade_count",
            "expectancy",
            "cost_stressed_expectancy",
            "pf_gap_to_34d_latest",
            "net_gap_to_34d_latest",
            "dd_percent_gap_to_34d_latest",
            "trade_count_gap_to_34d_latest",
            "stage101_read",
        ),
    )
    write_csv(
        SEGMENT_GAP_PATH,
        segments,
        (
            "run_id",
            "adapter_id",
            "split",
            "segment_type",
            "segment",
            "trade_count",
            "net_profit",
            "profit_factor",
            "expectancy",
            "mfe_capture_ratio",
            "max_closed_trade_drawdown",
            "stage101_read",
        ),
    )
    write_csv(
        PROJECTION_RUNTIME_PATH,
        deltas,
        (
            "run_id",
            "adapter_id",
            "candidate_gate",
            "split",
            "projected_net",
            "runtime_net",
            "runtime_minus_projected_net",
            "projected_profit_factor",
            "runtime_profit_factor",
            "runtime_minus_projected_pf",
            "stage101_read",
        ),
    )
    write_md(REPORT_PATH, report_markdown(gaps, segments, deltas))
    write_md(DECISION_PATH, decision_markdown())
    ledger_payload = write_ledgers(gaps)
    packet_files(ledger_payload)
    update_artifact_registry()
    update_current_truth()
    append_changelog()
    print(
        json.dumps(
            json_ready(
                {
                    "status": "ok",
                    "run_id": RUN_ID,
                    "decision": DECISION,
                    "external_verification_status": EXTERNAL_STATUS,
                    "report": rel(REPORT_PATH),
                    "decision_path": rel(DECISION_PATH),
                    "next_stage": NEXT_STAGE_ID,
                }
            ),
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
