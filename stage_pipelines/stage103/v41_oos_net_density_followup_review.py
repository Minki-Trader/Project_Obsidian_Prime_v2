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


STAGE_ID = "103_adapter_research__v41_oos_net_density_followup_review"
RUN_ID = "run103A_stage103_v41_oos_net_density_followup_review_v1"
PACKET_ID = "stage103_v41_oos_net_density_followup_review_v1"
PARENT_RUN_ID = "run102A_stage102_v41_oos_net_density_dd_repair_v1"
SOURCE_STAGE102_ID = "102_adapter_research__v41_oos_net_density_dd_repair"
SOURCE_STAGE102_CLOSEOUT_COMMIT = "c2b1bfbfef06ab887adcd20554fbf9b99f8475f2"
SOURCE_STAGE102_LATEST_COMMIT = "5ca329c468db459a8f68b9c28dd0897dfbf79623"
SOURCE_STAGE101_LATEST_COMMIT = "172104e12a1f8dda9352d5f84c668d2467a7adb3"
TARGET_SURFACE = "legacy_34d_kpi_lesson_only_no_legacy_inheritance"
DECISION = "continue_oos_early_segment_repair_in_stage104"
NEXT_STAGE_ID = "104_adapter_research__v41_oos_early_segment_repair"
NEXT_RUN_ID = "run104A_stage104_v41_oos_early_segment_repair_v1"
NEXT_PACKET_ID = "stage104_v41_oos_early_segment_repair_v1"
EXTERNAL_STATUS = "completed_existing_stage102_mt5_runtime_evidence_reviewed"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment"
)

LEGACY_34D = {
    "profit_factor": 1.583157,
    "net_profit": 987.60,
    "max_drawdown_percent": 12.909136,
    "trade_count": 404,
}

STAGE100_BEST = {
    "adapter_id": "s100_v41_h3_cd8_lng_early_adx20",
    "split": "oos",
    "profit_factor": 1.584029112,
    "net_profit": 605.06,
    "max_drawdown_percent": 18.69,
    "trade_count": 149,
    "expectancy": 4.060805369,
}

STAGE100_EARLY = {
    "adapter_id": "s100_v41_h3_cd8_lng_early_adx20",
    "segment": "early",
    "profit_factor": 1.128143477,
    "net_profit": 32.51,
    "trade_count": 50,
    "mfe_capture_ratio": 0.06074909558,
}

STAGE_ROOT = Path("stages") / STAGE_ID
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
SELECTED_ROOT = STAGE_ROOT / "04_selected"
PACKET_ROOT = Path("docs/agent_control/packets") / PACKET_ID
NEXT_STAGE_ROOT = Path("stages") / NEXT_STAGE_ID

SOURCE_REVIEWS = Path("stages") / SOURCE_STAGE102_ID / "03_reviews"
SOURCE_SUMMARY = SOURCE_REVIEWS / "stage102_oos_net_density_dd_repair_summary.csv"
SOURCE_SEGMENTS = SOURCE_REVIEWS / "stage102_segment_kpi_summary.csv"
SOURCE_DECISION = SOURCE_REVIEWS / "stage102_decision.md"
SOURCE_REPORT = SOURCE_REVIEWS / "stage102_oos_net_density_dd_repair_report.md"

REPORT_PATH = REVIEWS_ROOT / "stage103_oos_net_density_followup_review.md"
KPI_COMPARISON_PATH = REVIEWS_ROOT / "stage103_stage100_stage102_34d_comparison.csv"
SEGMENT_WARNING_PATH = REVIEWS_ROOT / "stage103_segment_warning_summary.csv"
DECISION_PATH = REVIEWS_ROOT / "stage103_decision.md"
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


def full_segment_lookup() -> dict[tuple[str, str], dict[str, str]]:
    lookup: dict[tuple[str, str], dict[str, str]] = {}
    for row in read_csv(SOURCE_SEGMENTS):
        if row.get("view") == "actual_routed_total" and row.get("segment_type") == "full_split":
            lookup[(row.get("adapter_id", ""), row.get("split", ""))] = row
    return lookup


def routed_rows() -> list[dict[str, Any]]:
    precise = full_segment_lookup()
    rows: list[dict[str, Any]] = [
        {
            "source": "stage100_best",
            **STAGE100_BEST,
        }
    ]
    for row in read_csv(SOURCE_SUMMARY):
        if row.get("view") != "actual_routed_total" or row.get("split") != "oos":
            continue
        segment = precise.get((row.get("adapter_id", ""), "oos"), {})
        rows.append(
            {
                "source": "stage102",
                "adapter_id": row.get("adapter_id", ""),
                "split": "oos",
                "profit_factor": num(segment, "profit_factor") if segment else num(row, "profit_factor"),
                "net_profit": num(segment, "net_profit") if segment else num(row, "net_profit"),
                "max_drawdown_percent": num(row, "max_drawdown_percent"),
                "trade_count": num(segment, "trade_count") if segment else num(row, "trade_count"),
                "expectancy": num(segment, "expectancy") if segment else num(row, "expectancy"),
            }
        )
    return rows


def best_stage102(rows: Sequence[Mapping[str, Any]]) -> Mapping[str, Any]:
    candidates = [row for row in rows if row.get("source") == "stage102"]
    return max(
        candidates,
        key=lambda row: (
            float(row.get("profit_factor") or 0.0),
            float(row.get("net_profit") or 0.0),
            -float(row.get("max_drawdown_percent") or 999.0),
        ),
    )


def kpi_comparison_rows(rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for row in rows:
        pf = float(row.get("profit_factor") or 0.0)
        net = float(row.get("net_profit") or 0.0)
        dd = float(row.get("max_drawdown_percent") or 0.0)
        trades = float(row.get("trade_count") or 0.0)
        if row.get("source") == "stage100_best":
            read = "stage100_reference_surface"
        elif net > STAGE100_BEST["net_profit"] and pf >= STAGE100_BEST["profit_factor"]:
            read = "full_oos_improved_over_stage100_but_34d_net_dd_gap_remains"
        else:
            read = "not_preferred_stage102_variant"
        output.append(
            {
                "run_id": RUN_ID,
                "source": row.get("source", ""),
                "adapter_id": row.get("adapter_id", ""),
                "split": "oos",
                "profit_factor": fmt(pf),
                "net_profit": fmt(net, 2),
                "max_drawdown_percent": fmt(dd),
                "trade_count": fmt(trades, 0),
                "expectancy": fmt(float(row.get("expectancy") or 0.0), 6),
                "pf_delta_vs_stage100_best": fmt(pf - STAGE100_BEST["profit_factor"]),
                "net_delta_vs_stage100_best": fmt(net - STAGE100_BEST["net_profit"], 2),
                "dd_delta_vs_stage100_best": fmt(dd - STAGE100_BEST["max_drawdown_percent"], 6),
                "trade_delta_vs_stage100_best": fmt(trades - STAGE100_BEST["trade_count"], 0),
                "pf_gap_to_34d_latest": fmt(pf - LEGACY_34D["profit_factor"]),
                "net_gap_to_34d_latest": fmt(net - LEGACY_34D["net_profit"], 2),
                "dd_gap_to_34d_latest": fmt(dd - LEGACY_34D["max_drawdown_percent"], 6),
                "stage103_read": read,
            }
        )
    return output


def segment_warning_rows(best: Mapping[str, Any]) -> list[dict[str, Any]]:
    best_id = str(best.get("adapter_id", ""))
    output = [
        {
            "run_id": RUN_ID,
            "source": "stage100_best",
            "adapter_id": STAGE100_EARLY["adapter_id"],
            "segment": "early",
            "trade_count": STAGE100_EARLY["trade_count"],
            "net_profit": fmt(STAGE100_EARLY["net_profit"], 2),
            "profit_factor": fmt(STAGE100_EARLY["profit_factor"]),
            "mfe_capture_ratio": fmt(STAGE100_EARLY["mfe_capture_ratio"]),
            "stage103_read": "stage100_early_reference_already_weak",
        }
    ]
    for row in read_csv(SOURCE_SEGMENTS):
        if row.get("adapter_id") != best_id:
            continue
        if row.get("split") != "oos" or row.get("segment_type") != "chronological_third":
            continue
        segment = row.get("segment", "")
        if segment == "early":
            read = "stage102_best_full_oos_improved_but_early_segment_degraded"
        elif segment == "mid":
            read = "stage102_best_profit_concentrated_in_mid_segment"
        else:
            read = "stage102_best_late_segment_supportive"
        output.append(
            {
                "run_id": RUN_ID,
                "source": "stage102_best",
                "adapter_id": best_id,
                "segment": segment,
                "trade_count": row.get("trade_count", ""),
                "net_profit": row.get("net_profit", ""),
                "profit_factor": row.get("profit_factor", ""),
                "mfe_capture_ratio": row.get("mfe_capture_ratio", ""),
                "stage103_read": read,
            }
        )
    return output


def report_markdown(comparison: Sequence[Mapping[str, Any]], warnings: Sequence[Mapping[str, Any]], best: Mapping[str, Any]) -> str:
    lines = [
        "# Stage103 OOS Net Density Follow-up Review(103단계 표본외 순손익 밀도 후속 검토)",
        "",
        f"- run(실행): `{RUN_ID}`",
        f"- source_run(원천 실행): `{PARENT_RUN_ID}`",
        f"- source_stage102_closeout_commit(원천 102단계 종료 커밋): `{SOURCE_STAGE102_CLOSEOUT_COMMIT}`",
        f"- source_stage102_latest_commit(원천 102단계 최신 커밋): `{SOURCE_STAGE102_LATEST_COMMIT}`",
        f"- target_surface(목표 표면): `{TARGET_SURFACE}`",
        f"- decision(판정): `{DECISION}`",
        f"- boundary(경계): `{BOUNDARY}`",
        "",
        "## Bounded Question(경계 질문)",
        "",
        "Stage102(102단계)의 OOS net density/DD repair(표본외 순손익 밀도/손실률 수리)가 Stage100 best(100단계 최선)보다 좋아졌는가, 그리고 34D KPI(34D 핵심 성과 지표) 목표에 충분한가?",
        "",
        "Effect(효과): Stage103(103단계)은 새 실행 없이 결과 판독과 다음 수리축 선택만 한다.",
        "",
        "## KPI Comparison(KPI 비교)",
        "",
        "| source(원천) | adapter(어댑터) | PF(수익 팩터) | net(순손익) | DD%(손실률) | trades(거래 수) | net delta(순손익 변화) | read(판독) |",
        "|---|---|---:|---:|---:|---:|---:|---|",
    ]
    for row in comparison:
        lines.append(
            f"| {row['source']} | {row['adapter_id']} | {row['profit_factor']} | {row['net_profit']} | {row['max_drawdown_percent']} | {row['trade_count']} | {row['net_delta_vs_stage100_best']} | {row['stage103_read']} |"
        )
    lines.extend(
        [
            "",
            "## Segment Warning(구간 경고)",
            "",
            "| source(원천) | segment(구간) | net(순손익) | PF(수익 팩터) | MFE capture(MFE 포착률) | read(판독) |",
            "|---|---|---:|---:|---:|---|",
        ]
    )
    for row in warnings:
        lines.append(
            f"| {row['source']} | {row['segment']} | {row['net_profit']} | {row['profit_factor']} | {row['mfe_capture_ratio']} | {row['stage103_read']} |"
        )
    lines.extend(
        [
            "",
            "## Decision(판정)",
            "",
            f"decision(판정): `{DECISION}`",
            "",
            f"Stage102 best(102단계 최선) `{best['adapter_id']}`는 full OOS(전체 표본외) 기준으로 Stage100 best(100단계 최선)보다 좋아졌다.",
            "",
            "하지만 OOS early(표본외 초반)는 더 약해졌다. 즉 전체 개선이 mid/late(중반/후반)에 더 기대고 있어서, 34D급 연구 패키지로 보기에는 아직 불안정하다.",
            "",
            "Effect(효과): Stage104(104단계)는 full OOS(전체 표본외) 개선을 보존하면서 OOS early segment(표본외 초반 구간)를 좁게 수리한다.",
            "",
            "Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), legacy inheritance(레거시 상속).",
        ]
    )
    return "\n".join(lines) + "\n"


def decision_markdown() -> str:
    return f"""# Stage103 Decision(103단계 판정)

decision(판정): `{DECISION}`

Stage103(103단계)은 Stage102(102단계)의 실제 MT5 runtime(실행환경) 근거만 후속 검토했다.

Effect(효과): Stage102(102단계)의 full OOS(전체 표본외) 개선은 보존하되, 약해진 OOS early(표본외 초반)를 다음 수리축으로 넘긴다.

## Evidence(근거)

- report(보고서): `{rel(REPORT_PATH)}`
- comparison(비교): `{rel(KPI_COMPARISON_PATH)}`
- segment_warning_summary(구간 경고 요약): `{rel(SEGMENT_WARNING_PATH)}`
- source_stage102_summary(원천 102단계 요약): `{rel(SOURCE_SUMMARY)}`
- source_stage102_segment_kpi(원천 102단계 구간 KPI): `{rel(SOURCE_SEGMENTS)}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- pushed_commit_hash(푸시된 커밋 해시): `pending_until_push`

## Next(다음)

next_stage_or_branch(다음 단계/분기): `{NEXT_STAGE_ID}`

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), legacy inheritance(레거시 상속).
"""


def ledger_rows(best: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "ledger_row_id": f"{RUN_ID}__review_gate",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "review_gate",
            "parent_run_id": PARENT_RUN_ID,
            "record_view": "stage103_review_gate",
            "tier_scope": "Tier A+B",
            "kpi_scope": "stage103_v41_oos_net_density_followup_review",
            "scoreboard_lane": "regular_risk_execution_review",
            "status": "reviewed",
            "judgment": DECISION,
            "path": rel(DECISION_PATH),
            "primary_kpi": ledger_pairs(
                [
                    ("best_adapter", best.get("adapter_id")),
                    ("oos_pf", best.get("profit_factor")),
                    ("oos_net", best.get("net_profit")),
                    ("oos_dd_pct", best.get("max_drawdown_percent")),
                ]
            ),
            "guardrail_kpi": "oos_early_segment_degraded_after_stage102_full_oos_improvement",
            "external_verification_status": EXTERNAL_STATUS,
            "notes": "Review-only gate using Stage102 MT5 runtime evidence; no new runtime claim.",
        }
    ]


def write_ledgers(best: Mapping[str, Any]) -> Mapping[str, Any]:
    rows = ledger_rows(best)
    write_csv(STAGE_LEDGER_PATH, rows, ALPHA_LEDGER_COLUMNS)
    project = upsert_csv_rows(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, rows, key="ledger_row_id")
    registry = upsert_csv_rows(
        RUN_REGISTRY_PATH,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "baseline_adapter_v2_native_v41_oos_net_density_followup_review",
                "status": "reviewed",
                "judgment": DECISION,
                "path": rel(DECISION_PATH),
                "notes": (
                    f"source_run={PARENT_RUN_ID};source_stage102_latest_commit={SOURCE_STAGE102_LATEST_COMMIT};"
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
            "source_stage102_closeout_commit": SOURCE_STAGE102_CLOSEOUT_COMMIT,
            "source_stage102_latest_commit": SOURCE_STAGE102_LATEST_COMMIT,
            "comparison_path": rel(KPI_COMPARISON_PATH),
            "segment_warning_path": rel(SEGMENT_WARNING_PATH),
            "ledger_payload": ledger_payload,
            "pushed_commit_hash": "pending_until_push",
            "overall_goal_complete": False,
        },
    )


def artifact_rows() -> list[dict[str, Any]]:
    created = datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    paths = [
        (REPORT_PATH, "stage103_v41_oos_net_density_followup_review_evidence", "Stage103 bounded review report."),
        (KPI_COMPARISON_PATH, "stage103_v41_oos_net_density_followup_review_evidence", "Stage103 Stage100/Stage102/34D comparison."),
        (SEGMENT_WARNING_PATH, "stage103_v41_oos_net_density_followup_review_evidence", "Stage103 segment warning summary."),
        (DECISION_PATH, "stage103_v41_oos_net_density_followup_review_evidence", "Stage103 decision."),
        (STAGE_LEDGER_PATH, "stage103_v41_oos_net_density_followup_review_evidence", "Stage103 local ledger."),
        (PACKET_ROOT / "aggregate_summary.json", "packet_summary", "Stage103 packet aggregate summary."),
        (PACKET_ROOT / "routing_receipt.json", "packet_control", "Stage103 routing receipt."),
        (PACKET_ROOT / "runtime_evidence_gate.json", "packet_control", "Stage103 runtime evidence gate."),
        (PACKET_ROOT / "result_judgment_gate.json", "packet_control", "Stage103 result judgment gate."),
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

Stage104(104단계)는 Stage103(103단계) 판정에 따라 OOS early segment(표본외 초반 구간)를 좁게 수리한다.

## Bounded Question(경계 질문)

Stage102 best(102단계 최선)의 full OOS(전체 표본외) PF/net/DD(수익 팩터/순손익/손실률) 개선을 보존하면서 OOS early(표본외 초반)의 PF(수익 팩터), net(순손익), MFE capture(MFE 포착률)를 회복할 수 있는가?

Effect(효과): Stage104(104단계)는 전체 후보를 새로 찾지 않고, Stage102(102단계)에서 생긴 초반 구간 약화만 좁게 다룬다.

## Boundary(경계)

`{BOUNDARY}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "01_inputs" / "input_refs.md",
        f"""# Stage104 Input References(104단계 입력 참조)

- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- source_decision(원천 판정): `{DECISION}`
- source_report(원천 보고서): `{rel(REPORT_PATH)}`
- source_comparison(원천 비교): `{rel(KPI_COMPARISON_PATH)}`
- source_segment_warning(원천 구간 경고): `{rel(SEGMENT_WARNING_PATH)}`
- target_surface(목표 표면): `{TARGET_SURFACE}`

Effect(효과): Stage104(104단계)는 Stage103(103단계)의 판독 근거를 그대로 이어받아, 수리 범위를 초반 구간으로 제한한다.
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "03_reviews" / "review_index.md",
        f"""# Stage104 Review Index(104단계 검토 색인)

- status(상태): `open_planned`
- source_decision(원천 판정): `{DECISION}`
- planned_packet(계획 작업 묶음): `{NEXT_PACKET_ID}`
- planned_run(계획 실행): `{NEXT_RUN_ID}`

Effect(효과): Stage104(104단계)는 Stage103(103단계) closeout(종료 기록)을 받아 좁은 수리만 수행한다.
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "04_selected" / "selection_status.md",
        f"""# Stage104 Selection Status(104단계 선택 상태)

- stage_status(단계 상태): `open_planned`
- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- source_stage(원천 단계): `{STAGE_ID}`
- source_decision(원천 판정): `{DECISION}`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Effect(효과): Stage104(104단계)는 34D KPI(34D 핵심 성과 지표) 격차 축소를 계속하지만, 운영 의미 없이 연구개발로만 이어진다.
""",
    )


def update_current_truth() -> None:
    text = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    text = re.sub(r"^current_run_id: .*$", f"current_run_id: {NEXT_RUN_ID}", text, count=1, flags=re.MULTILINE)
    text = re.sub(r"^updated_on: .*$", "updated_on: '2026-05-18'", text, count=1, flags=re.MULTILINE)
    text = re.sub(r"^active_stage: .*$", f"active_stage: {NEXT_STAGE_ID}", text, count=1, flags=re.MULTILINE)
    current_focus = f"""current_focus:
- >-
  Stage103(103단계) closed(종료) as `{DECISION}` and Stage104(104단계) `{NEXT_STAGE_ID}` is open_planned(열림 계획). Effect(효과): Stage102(102단계)의 full OOS(전체 표본외) 개선은 보존하고 OOS early segment(표본외 초반 구간) 수리로 넘긴다.
- >-
  Stage103 result(103단계 결과)는 `{rel(KPI_COMPARISON_PATH)}`와 `{rel(SEGMENT_WARNING_PATH)}`에 기록된다. Effect(효과): Stage102 best(102단계 최선)의 장점과 약점을 다음 단계 입력으로 보존한다.
- >-
  Target surface(목표 표면)는 `{TARGET_SURFACE}`이고 legacy 34D(레거시 34D)는 lesson-only KPI target(교훈 전용 핵심 성과 지표 목표)이다. Effect(효과): 목표는 높게 유지하지만 v2-native research(브이투 고유 연구)만 계속한다.
"""
    text = re.sub(r"current_focus:\n.*?\n\nstage", current_focus.rstrip() + "\n\nstage", text, count=1, flags=re.DOTALL)
    block = f"""

stage103_v41_oos_net_density_followup_review:
  packet_id: {PACKET_ID}
  stage_id: {STAGE_ID}
  status: closed_{DECISION}
  current_run_id: {RUN_ID}
  source_stage102_closeout_commit: {SOURCE_STAGE102_CLOSEOUT_COMMIT}
  source_stage102_latest_commit: {SOURCE_STAGE102_LATEST_COMMIT}
  source_stage101_latest_commit: {SOURCE_STAGE101_LATEST_COMMIT}
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
    marker = "stage103_v41_oos_net_density_followup_review:"
    if marker in text:
        text = re.sub(r"\nstage103_v41_oos_net_density_followup_review:\n(?:  .*\n)+", block + "\n", text, count=1)
    else:
        text = text.rstrip() + block + "\n"
    io_path(WORKSPACE_STATE_PATH).write_text(text.rstrip() + "\n", encoding="utf-8-sig")
    write_md(
        SELECTED_ROOT / "selection_status.md",
        f"""# Stage103 Selection Status(103단계 선택 상태)

- stage_status(단계 상태): `closed_{DECISION}`
- current_packet(현재 작업 묶음): `{PACKET_ID}`
- current_run(현재 실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE102_ID}`
- source_decision(원천 판정): `continue_oos_net_density_followup_review_in_stage103`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- stage103_decision(103단계 판정): `{DECISION}`
- next_stage_or_branch(다음 단계/분기): `{NEXT_STAGE_ID}`
- pushed_commit_hash(푸시된 커밋 해시): `pending_until_push`
- claim_boundary(주장 경계): `{BOUNDARY}`

Effect(효과): Stage103(103단계)은 Stage102(102단계) 실제 실행 결과를 판독하고, 운영 의미 없이 Stage104(104단계)로 넘긴다.
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
- adapter_under_review(검토 중 어댑터): `s102_v41_h3_cd8_lng_early_adx18`
- status(상태): `stage103_closed_{DECISION}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage103(103단계) closed(종료) as v2-native v41 OOS net density follow-up review(브이투 고유 브이41 표본외 순손익 밀도 후속 검토). Effect(효과): legacy 34D(레거시 34D)는 target surface(목표 표면)로만 쓰였고, 다음 연구는 Stage104(104단계)로 이어진다.

## Latest Stage103 Evidence(최신 103단계 근거)

- run(실행): `{RUN_ID}`
- decision(판정): `{DECISION}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- report(보고서): `{rel(REPORT_PATH)}`
- comparison(비교): `{rel(KPI_COMPARISON_PATH)}`
- segment_warning_summary(구간 경고 요약): `{rel(SEGMENT_WARNING_PATH)}`

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준선), legacy_inheritance(레거시 상속).
""",
    )
    create_next_stage()


def append_changelog() -> None:
    entry = (
        "\n## 2026-05-18 - Stage103 v41 OOS net density follow-up review closeout(103단계 v41 표본외 순손익 밀도 후속 검토 종료)\n\n"
        f"- run(실행): `{RUN_ID}`\n"
        f"- decision(판정): `{DECISION}`\n"
        "- pushed_commit_hash(푸시된 커밋 해시): `pending_until_push`\n"
        f"- target_surface(목표 표면): `{TARGET_SURFACE}`\n"
        "- effect(효과): Stage102(102단계)는 full OOS(전체 표본외)를 개선했지만 OOS early(표본외 초반)가 약해져 Stage104(104단계) 초반 구간 수리로 넘겼다.\n"
    )
    existing = io_path(CHANGELOG_PATH).read_text(encoding="utf-8-sig")
    if RUN_ID not in existing:
        io_path(CHANGELOG_PATH).write_text(existing.rstrip() + entry, encoding="utf-8-sig")


def main() -> int:
    rows = routed_rows()
    best = best_stage102(rows)
    comparison = kpi_comparison_rows(rows)
    warnings = segment_warning_rows(best)
    write_csv(
        KPI_COMPARISON_PATH,
        comparison,
        (
            "run_id",
            "source",
            "adapter_id",
            "split",
            "profit_factor",
            "net_profit",
            "max_drawdown_percent",
            "trade_count",
            "expectancy",
            "pf_delta_vs_stage100_best",
            "net_delta_vs_stage100_best",
            "dd_delta_vs_stage100_best",
            "trade_delta_vs_stage100_best",
            "pf_gap_to_34d_latest",
            "net_gap_to_34d_latest",
            "dd_gap_to_34d_latest",
            "stage103_read",
        ),
    )
    write_csv(
        SEGMENT_WARNING_PATH,
        warnings,
        (
            "run_id",
            "source",
            "adapter_id",
            "segment",
            "trade_count",
            "net_profit",
            "profit_factor",
            "mfe_capture_ratio",
            "stage103_read",
        ),
    )
    write_md(REPORT_PATH, report_markdown(comparison, warnings, best))
    write_md(DECISION_PATH, decision_markdown())
    ledger_payload = write_ledgers(best)
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
