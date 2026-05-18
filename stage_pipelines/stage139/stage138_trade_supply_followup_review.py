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
    path_exists,
    sha256_file_lf_normalized,
    upsert_csv_rows,
)
from stage_pipelines.stage56.independent_event_source_route_branch import ARTIFACT_COLUMNS  # noqa: E402


STAGE_ID = "139_adapter_research__stage138_trade_supply_followup_review"
RUN_ID = "run139A_stage139_stage138_trade_supply_followup_review_v1"
PACKET_ID = "stage139_stage138_trade_supply_followup_review_v1"
PARENT_RUN_ID = "run138A_stage138_trade_supply_repair_after_stage136_no_gain_v1"
SOURCE_STAGE138_ID = "138_adapter_research__trade_supply_repair_after_stage136_no_gain"
SOURCE_STAGE138_CLOSEOUT_COMMIT = "9a5bedb1b1e8e20d13ef1072edeca7039dba1080"
SOURCE_STAGE138_HASH_RECORD_COMMIT = "4a2ed5eb197334f8995fa37dc8f4345db7a0d341"
SOURCE_STAGE137_LATEST_COMMIT = "685ae86bd49fb58eb70668efc7d8b69706753396"
NEXT_STAGE_ID = "140_adapter_research__reverse_supply_late_concentration_repair"
NEXT_RUN_ID = "run140A_stage140_reverse_supply_late_concentration_repair_v1"
NEXT_PACKET_ID = "stage140_reverse_supply_late_concentration_repair_v1"
DECISION = "continue_stage140_reverse_supply_late_concentration_repair_candidate_not_final"
TARGET_SURFACE = "legacy_34d_kpi_lesson_only_no_legacy_inheritance"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment"
)
EXTERNAL_STATUS = "completed_existing_stage138_mt5_runtime_evidence_reviewed"

STAGE_ROOT = Path("stages") / STAGE_ID
SPEC_ROOT = STAGE_ROOT / "00_spec"
INPUT_ROOT = STAGE_ROOT / "01_inputs"
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
SELECTED_ROOT = STAGE_ROOT / "04_selected"
PACKET_ROOT = Path("docs/agent_control/packets") / PACKET_ID
NEXT_STAGE_ROOT = Path("stages") / NEXT_STAGE_ID

SOURCE_STAGE138_REVIEWS = Path("stages") / SOURCE_STAGE138_ID / "03_reviews"
SOURCE_SUMMARY = SOURCE_STAGE138_REVIEWS / "stage138_trade_supply_repair_summary.csv"
SOURCE_SEGMENTS = SOURCE_STAGE138_REVIEWS / "stage138_segment_kpi_summary.csv"
SOURCE_RISK_ATR = SOURCE_STAGE138_REVIEWS / "stage138_risk_atr_telemetry.csv"
SOURCE_DECISION = SOURCE_STAGE138_REVIEWS / "stage138_decision.md"

REPORT_PATH = REVIEWS_ROOT / "stage139_stage138_trade_supply_followup_review.md"
COMPARISON_PATH = REVIEWS_ROOT / "stage139_stage138_trade_supply_comparison.csv"
ROUTE_DECISION_PATH = REVIEWS_ROOT / "stage139_route_decision.csv"
DECISION_PATH = REVIEWS_ROOT / "stage139_decision.md"
SUMMARY_JSON_PATH = REVIEWS_ROOT / "stage139_followup_summary.json"
STAGE_LEDGER_PATH = REVIEWS_ROOT / "stage_run_ledger.csv"

RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
PROJECT_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
ARTIFACT_REGISTRY_PATH = Path("docs/registers/artifact_registry.csv")
WORKSPACE_STATE_PATH = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE_PATH = Path("docs/context/current_working_state.md")
CHANGELOG_PATH = Path("docs/workspace/changelog.md")

CONTROL_ADAPTER = "s138_control_sht54_lng52_cd5_h3_risk035"
REVERSE_ADAPTER = "s138_reverse_opposite_h3_cd5_risk035"
LEGACY_34D = {
    "profit_factor": 1.583157,
    "net_profit": 987.60,
    "max_drawdown_percent": 12.909136,
    "trade_count": 404,
}


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    candidate = Path(str(path))
    try:
        return io_path(candidate).resolve().relative_to(io_path(REPO_ROOT).resolve()).as_posix()
    except ValueError:
        return candidate.as_posix()


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        if value in (None, ""):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def csv_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, float):
        return f"{value:.10f}"
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(json_ready(value), ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return str(value)


def read_csv(path: Path) -> list[dict[str, str]]:
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str] | None = None) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    if columns is None:
        ordered: list[str] = []
        for row in rows:
            for key in row:
                if key not in ordered:
                    ordered.append(key)
        columns = tuple(ordered)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: csv_value(row.get(column)) for column in columns})


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(
        json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def routed_summary_rows() -> list[dict[str, str]]:
    return [
        row
        for row in read_csv(SOURCE_SUMMARY)
        if row.get("view") == "actual_routed_total" and row.get("route_role") == "routed_total"
    ]


def segment_rows() -> list[dict[str, str]]:
    return [row for row in read_csv(SOURCE_SEGMENTS) if row.get("view") == "actual_routed_total"]


def late_share(adapter_id: str, split: str, segments: Sequence[Mapping[str, str]]) -> float:
    full = 0.0
    late = 0.0
    for row in segments:
        if row.get("adapter_id") != adapter_id or row.get("split") != split:
            continue
        if row.get("segment_type") == "full_split":
            full = as_float(row.get("net_profit"))
        if row.get("segment_type") == "chronological_third" and row.get("segment") == "late":
            late = as_float(row.get("net_profit"))
    return late / full if full else 0.0


def read_label(row: Mapping[str, Any]) -> str:
    if row["validation_pf"] < 1.55 or row["validation_net"] < LEGACY_34D["net_profit"]:
        return "validation_quality_failed_trade_supply_damage"
    if row["oos_trade_gain_vs_control"] > 0 and row["oos_net_delta_vs_control"] > 0:
        if row["validation_late_net_share_delta_vs_control"] > 0.01:
            return "small_trade_gain_quality_preserved_but_late_concentration_worse"
        return "small_trade_gain_quality_preserved"
    if row["oos_pf"] >= LEGACY_34D["profit_factor"] and row["oos_net"] >= LEGACY_34D["net_profit"]:
        return "quality_preserved_but_no_trade_count_gain"
    return "not_safe_repair"


def build_review() -> dict[str, Any]:
    rows = routed_summary_rows()
    segments = segment_rows()
    by_adapter_split = {(row["adapter_id"], row["split"]): row for row in rows}
    adapters = sorted({row["adapter_id"] for row in rows})
    control_val = by_adapter_split.get((CONTROL_ADAPTER, "validation_is"), {})
    control_oos = by_adapter_split.get((CONTROL_ADAPTER, "oos"), {})
    control_late = late_share(CONTROL_ADAPTER, "validation_is", segments)
    comparison: list[dict[str, Any]] = []
    for adapter_id in adapters:
        val = by_adapter_split.get((adapter_id, "validation_is"), {})
        oos = by_adapter_split.get((adapter_id, "oos"), {})
        row = {
            "adapter_id": adapter_id,
            "validation_pf": as_float(val.get("profit_factor")),
            "validation_net": as_float(val.get("net_profit")),
            "validation_dd_percent": as_float(val.get("max_drawdown_percent")),
            "validation_trades": as_float(val.get("trade_count")),
            "validation_late_net_share": late_share(adapter_id, "validation_is", segments),
            "validation_late_net_share_delta_vs_control": late_share(adapter_id, "validation_is", segments) - control_late,
            "oos_pf": as_float(oos.get("profit_factor")),
            "oos_net": as_float(oos.get("net_profit")),
            "oos_dd_percent": as_float(oos.get("max_drawdown_percent")),
            "oos_trades": as_float(oos.get("trade_count")),
            "oos_late_net_share": late_share(adapter_id, "oos", segments),
            "oos_trade_gain_vs_control": as_float(oos.get("trade_count")) - as_float(control_oos.get("trade_count")),
            "validation_trade_gain_vs_control": as_float(val.get("trade_count")) - as_float(control_val.get("trade_count")),
            "oos_net_delta_vs_control": as_float(oos.get("net_profit")) - as_float(control_oos.get("net_profit")),
            "oos_pf_delta_vs_control": as_float(oos.get("profit_factor")) - as_float(control_oos.get("profit_factor")),
            "oos_dd_delta_vs_control": as_float(oos.get("max_drawdown_percent")) - as_float(control_oos.get("max_drawdown_percent")),
            "oos_trade_gap_to_34d": as_float(oos.get("trade_count")) - LEGACY_34D["trade_count"],
            "oos_net_gap_to_34d": as_float(oos.get("net_profit")) - LEGACY_34D["net_profit"],
            "oos_pf_gap_to_34d": as_float(oos.get("profit_factor")) - LEGACY_34D["profit_factor"],
            "oos_dd_gap_to_34d": as_float(oos.get("max_drawdown_percent")) - LEGACY_34D["max_drawdown_percent"],
        }
        row["read"] = read_label(row)
        comparison.append(row)
    reverse = next((row for row in comparison if row["adapter_id"] == REVERSE_ADAPTER), {})
    best = max(
        comparison,
        key=lambda row: (
            row["read"].startswith("small_trade_gain_quality_preserved"),
            row["oos_trade_gain_vs_control"],
            row["oos_net_delta_vs_control"],
            row["oos_pf"],
            -row["validation_late_net_share_delta_vs_control"],
        ),
        default={},
    )
    route = [
        {
            "decision": DECISION,
            "reason": "reverse_opposite_added_only_one_oos_trade_and_improved_oos_net_but_trade_gap_remains_large_and_validation_late_concentration_worsened",
            "best_adapter": best.get("adapter_id", ""),
            "reverse_adapter_read": reverse.get("read", ""),
            "next_stage": NEXT_STAGE_ID,
            "overall_goal_complete": False,
        }
    ]
    return {"comparison": comparison, "best": best, "reverse": reverse, "route": route}


def table_rows(rows: Sequence[Mapping[str, Any]]) -> str:
    header = (
        "| adapter(어댑터) | val PF(검증 수익 팩터) | val net(검증 순손익) | val late share(검증 후반 비중) | "
        "OOS PF(미래구간 수익 팩터) | OOS net(미래구간 순손익) | OOS trades(미래구간 거래 수) | "
        "trade gain(거래 증가) | read(판독) |\n"
        "|---|---:|---:|---:|---:|---:|---:|---:|---|"
    )
    body = [
        (
            f"| {row['adapter_id']} | {row['validation_pf']:.2f} | {row['validation_net']:.2f} | "
            f"{row['validation_late_net_share']:.3f} | {row['oos_pf']:.2f} | {row['oos_net']:.2f} | "
            f"{row['oos_trades']:.0f} | {row['oos_trade_gain_vs_control']:.0f} | {row['read']} |"
        )
        for row in rows
    ]
    return "\n".join([header] + body)


def report_markdown(review: Mapping[str, Any]) -> str:
    best = review["best"]
    reverse = review["reverse"]
    return f"""# Stage139 Stage138 Trade Supply Follow-up Review(139단계 138단계 거래 공급 후속 검토)

- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE138_ID}`
- source_stage138_closeout_commit(원천 138단계 종료 커밋): `{SOURCE_STAGE138_CLOSEOUT_COMMIT}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- decision(판정): `{DECISION}`
- boundary(주장 경계): `{BOUNDARY}`

## Bounded Question(경계 질문)

Did Stage138(138단계) improve trade supply(거래 공급) enough to continue the same axis, or did it reveal damage/no-gain that requires a different bounded repair?

Effect(효과): +1 trade(거래 1건 증가)를 과장하지 않고, 품질 보존과 집중도 악화를 같이 보고 다음 질문을 좁힌다.

## KPI Read(KPI 핵심 성과 지표 판독)

{table_rows(review["comparison"])}

## Judgment(판정)

- best_adapter(최선 어댑터): `{best.get("adapter_id", "none")}`
- reverse_adapter(반전 어댑터): `{reverse.get("adapter_id", "none")}`
- reverse_oos_trade_gain(반전 미래구간 거래 증가): `{reverse.get("oos_trade_gain_vs_control", 0):.0f}`
- reverse_oos_net_delta(반전 미래구간 순손익 변화): `{reverse.get("oos_net_delta_vs_control", 0):.2f}`
- reverse_trade_gap_to_34d(반전 34D 거래 수 격차): `{reverse.get("oos_trade_gap_to_34d", 0):.0f}`
- reverse_validation_late_share_delta(반전 검증 후반 집중 변화): `{reverse.get("validation_late_net_share_delta_vs_control", 0):.3f}`
- overall_goal_complete(전체 목표 완료): `false`

Stage139(139단계) 판독은 reverse-on-opposite(반대 신호 반전)이 유일한 유효 축이라고 본다. Effect(효과): flat exit(평탄 청산) 계열은 검증 품질을 망가뜨렸으므로 다음 단계에서 제외하고, 반전 공급을 더 좁게 고친다.
"""


def decision_markdown(review: Mapping[str, Any]) -> str:
    reverse = review["reverse"]
    return f"""# Stage139 Decision(139단계 판정)

decision(판정): `{DECISION}`

Stage139(139단계)는 Stage138(138단계) MT5(runtime, 런타임) 근거를 review-only(검토 전용)로 판정했다. Effect(효과): 작은 OOS(미래구간) 개선은 보존하되, 전체 목표나 최종 후보로 과장하지 않는다.

## Evidence(근거)

- review(검토): `{rel(REPORT_PATH)}`
- comparison(비교): `{rel(COMPARISON_PATH)}`
- route_decision(경로 판정): `{rel(ROUTE_DECISION_PATH)}`
- source_stage138_summary(원천 138단계 요약): `{rel(SOURCE_SUMMARY)}`
- source_stage138_segments(원천 138단계 구간): `{rel(SOURCE_SEGMENTS)}`
- source_stage138_risk_atr(원천 138단계 위험/ATR): `{rel(SOURCE_RISK_ATR)}`
- reverse_adapter(반전 어댑터): `{reverse.get("adapter_id", "none")}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`

## Next(다음)

next_stage_or_branch(다음 단계/분기): `{NEXT_STAGE_ID}`

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), overall goal complete(전체 목표 완료).
"""


def artifact_rows() -> list[dict[str, Any]]:
    created = utc_now()
    rows: list[dict[str, Any]] = []
    for path in [REPORT_PATH, COMPARISON_PATH, ROUTE_DECISION_PATH, DECISION_PATH, SUMMARY_JSON_PATH, STAGE_LEDGER_PATH]:
        if path_exists(path):
            rows.append(
                {
                    "artifact_id": f"{RUN_ID}__{path.name}",
                    "artifact_type": "stage139_followup_review_evidence",
                    "path": rel(path),
                    "sha256": sha256_file_lf_normalized(path),
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "created_at_utc": created,
                    "notes": "Stage139 review-only follow-up artifact.",
                }
            )
    return rows


def write_ledgers(review: Mapping[str, Any]) -> dict[str, Any]:
    best = review["best"]
    reverse = review["reverse"]
    run_payload = upsert_csv_rows(
        RUN_REGISTRY_PATH,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "baseline_adapter_stage138_trade_supply_followup_review",
                "status": "completed",
                "judgment": DECISION,
                "path": rel(DECISION_PATH),
                "notes": ledger_pairs(
                    (
                        ("source_stage138_closeout_commit", SOURCE_STAGE138_CLOSEOUT_COMMIT),
                        ("source_stage138_hash_record_commit", SOURCE_STAGE138_HASH_RECORD_COMMIT),
                        ("best_adapter", best.get("adapter_id")),
                        ("reverse_oos_trade_gain", reverse.get("oos_trade_gain_vs_control")),
                        ("reverse_oos_net_delta", reverse.get("oos_net_delta_vs_control")),
                        ("target_surface", TARGET_SURFACE),
                        ("overall_goal_complete", False),
                    )
                ),
            }
        ],
        key="run_id",
    )
    ledger_rows = [
        {
            "ledger_row_id": f"{RUN_ID}__stage139_followup_review",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "stage139_followup_review",
            "parent_run_id": PARENT_RUN_ID,
            "record_view": "existing_stage138_evidence_review",
            "tier_scope": "Tier A+B routed review; Tier B disabled evidence preserved",
            "kpi_scope": "stage139_stage138_trade_supply_followup_review",
            "scoreboard_lane": "followup_review",
            "status": "completed",
            "judgment": DECISION,
            "path": rel(DECISION_PATH),
            "primary_kpi": ledger_pairs(
                (
                    ("best_adapter", best.get("adapter_id")),
                    ("reverse_oos_trade_gain", reverse.get("oos_trade_gain_vs_control")),
                    ("reverse_oos_net_delta", reverse.get("oos_net_delta_vs_control")),
                    ("reverse_oos_trades", reverse.get("oos_trades")),
                    ("reverse_oos_trade_gap_to_34d", reverse.get("oos_trade_gap_to_34d")),
                )
            ),
            "guardrail_kpi": ledger_pairs(
                (
                    ("decision", DECISION),
                    ("claim_boundary", BOUNDARY),
                    ("overall_goal_complete", False),
                )
            ),
            "external_verification_status": EXTERNAL_STATUS,
            "notes": "Stage139 review-only; no new MT5 execution; no operational claim.",
        }
    ]
    stage_payload = upsert_csv_rows(STAGE_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, ledger_rows, key="ledger_row_id")
    project_payload = upsert_csv_rows(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, ledger_rows, key="ledger_row_id")
    artifact_payload = upsert_csv_rows(ARTIFACT_REGISTRY_PATH, ARTIFACT_COLUMNS, artifact_rows(), key="artifact_id")
    return {
        "run_registry": run_payload,
        "stage_ledger": stage_payload,
        "project_alpha_ledger": project_payload,
        "artifact_registry": artifact_payload,
    }


def write_packet_files(review: Mapping[str, Any], ledger_payload: Mapping[str, Any]) -> None:
    files = {
        "routing_receipt.json": {
            "packet_id": PACKET_ID,
            "primary_family": "adapter_development",
            "primary_skill": "obsidian-result-judgment",
            "support_skills": ["obsidian-performance-attribution", "obsidian-artifact-lineage"],
            "required_gates": [
                "kpi_contract_audit",
                "result_judgment_gate",
                "performance_attribution_gate",
                "artifact_lineage_audit",
                "final_claim_guard",
            ],
            "status": "completed",
        },
        "kpi_contract_audit.json": {
            "source_summary": rel(SOURCE_SUMMARY),
            "source_segments": rel(SOURCE_SEGMENTS),
            "comparison_path": rel(COMPARISON_PATH),
            "status": "completed",
        },
        "result_judgment_gate.json": {
            "result_subject": RUN_ID,
            "evidence_available": [rel(REPORT_PATH), rel(COMPARISON_PATH), rel(DECISION_PATH)],
            "evidence_missing": ["new_repair_not_attempted_in_stage139_by_design"],
            "judgment_label": "candidate_not_final",
            "decision": DECISION,
            "claim_boundary": BOUNDARY,
            "next_condition": "Stage140 must test selective reverse supply without worsening late concentration or validation/OOS KPI.",
            "status": "passed_with_boundary",
        },
        "performance_attribution_gate.json": {
            "observed_change": "Reverse-on-opposite increased OOS trades by 1 and OOS net by 84.26, but validation late share worsened and trade gap to 34D remains -224.",
            "comparison_baseline": CONTROL_ADAPTER,
            "likely_drivers": ["opposite_signal_reversal_can_unlock_some_supply", "flat_exit_damages_validation_quality"],
            "attribution_confidence": "medium",
            "next_probe": "bounded Stage140 selective reverse supply and late concentration repair",
            "status": "completed",
        },
        "artifact_lineage_audit.json": {
            "source_inputs": [rel(SOURCE_SUMMARY), rel(SOURCE_SEGMENTS), rel(SOURCE_RISK_ATR), rel(SOURCE_DECISION)],
            "producer": rel(Path("stage_pipelines/stage139/stage138_trade_supply_followup_review.py")),
            "consumers": [rel(REPORT_PATH), rel(DECISION_PATH), rel(SUMMARY_JSON_PATH), NEXT_STAGE_ID],
            "artifact_paths": [rel(path) for path in [REPORT_PATH, COMPARISON_PATH, ROUTE_DECISION_PATH, DECISION_PATH, SUMMARY_JSON_PATH]],
            "registry_links": [rel(RUN_REGISTRY_PATH), rel(PROJECT_LEDGER_PATH), rel(STAGE_LEDGER_PATH), rel(ARTIFACT_REGISTRY_PATH)],
            "availability": "tracked",
            "lineage_judgment": "connected_with_boundary",
            "ledger_payload": ledger_payload,
        },
        "final_claim_guard.json": {
            "overall_goal_complete": False,
            "deployment_claim": False,
            "live_readiness_claim": False,
            "runtime_authority_claim": False,
            "production_baseline_claim": False,
            "operating_reference_claim": False,
            "operating_promotion_claim": False,
            "status": "passed",
        },
        "aggregate_summary.json": {
            "packet_id": PACKET_ID,
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "decision": DECISION,
            "source_stage138_closeout_commit": SOURCE_STAGE138_CLOSEOUT_COMMIT,
            "source_stage138_hash_record_commit": SOURCE_STAGE138_HASH_RECORD_COMMIT,
            "required_outputs": {
                "report": rel(REPORT_PATH),
                "comparison": rel(COMPARISON_PATH),
                "route_decision": rel(ROUTE_DECISION_PATH),
                "decision": rel(DECISION_PATH),
            },
            "ledger_payload": ledger_payload,
            "pushed_commit_hash": "pending_until_push",
            "claim_boundary": BOUNDARY,
            "overall_goal_complete": False,
        },
    }
    for name, payload in files.items():
        write_json(PACKET_ROOT / name, payload)


def write_stage_docs() -> None:
    write_md(
        SPEC_ROOT / "stage_brief.md",
        f"""# {STAGE_ID}

Stage139(139단계)는 Stage138(138단계) trade supply repair(거래 공급 수리) 결과를 review-only(검토 전용)로 판정한다.

## Boundary(경계)

`{BOUNDARY}`
""",
    )
    write_md(
        INPUT_ROOT / "input_refs.md",
        f"""# Stage139 Input References(139단계 입력 참조)

- stage138_decision(138단계 판정): `{rel(SOURCE_DECISION)}`
- stage138_summary(138단계 요약): `{rel(SOURCE_SUMMARY)}`
- stage138_segments(138단계 구간): `{rel(SOURCE_SEGMENTS)}`
- stage138_risk_atr(138단계 위험/ATR): `{rel(SOURCE_RISK_ATR)}`
- source_stage138_closeout_commit(원천 138단계 종료 커밋): `{SOURCE_STAGE138_CLOSEOUT_COMMIT}`
""",
    )
    write_md(
        SELECTED_ROOT / "selection_status.md",
        f"""# Stage139 Selection Status(139단계 선택 상태)

- stage_status(단계 상태): `closed_review_only`
- current_packet(현재 작업 묶음): `{PACKET_ID}`
- current_run(현재 실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE138_ID}`
- source_decision(원천 판정): `proceed_to_stage139_trade_supply_followup_review_with_small_gain_candidate_not_final`
- stage139_decision(139단계 판정): `{DECISION}`
- next_stage_or_branch(다음 단계/분기): `{NEXT_STAGE_ID}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- selected_research_baseline(선택 연구 기준): `none`
- claim_boundary(주장 경계): `{BOUNDARY}`
""",
    )
    write_md(
        REVIEWS_ROOT / "review_index.md",
        f"""# Stage139 Review Index(139단계 검토 색인)

- review(검토): `{rel(REPORT_PATH)}`
- comparison(비교): `{rel(COMPARISON_PATH)}`
- route_decision(경로 판정): `{rel(ROUTE_DECISION_PATH)}`
- decision(판정): `{rel(DECISION_PATH)}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "00_spec/stage_brief.md",
        f"""# {NEXT_STAGE_ID}

Stage140(140단계)는 Stage139(139단계) 판정에 따라 reverse-on-opposite(반대 신호 반전) 거래 공급 축을 더 좁게 수리한다.

## Bounded Question(경계 질문)

Can selective reverse supply(선택적 반전 공급) improve validation/OOS trade count(검증/미래구간 거래 수) beyond the +1 trade(거래 1건 증가) seen in Stage138(138단계), without damaging PF/net/DD(수익 팩터/순손익/손실률), late concentration(후반 집중), risk/ATR telemetry(위험/ATR 원격측정), or segment KPI(구간 핵심 성과 지표)?

Effect(효과): flat exit(평탄 청산) 손상 축은 제외하고, 유일하게 품질을 보존한 reverse(반전) 축만 좁게 고친다.

## Boundary(경계)

`{BOUNDARY}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "01_inputs/input_refs.md",
        f"""# Stage140 Input References(140단계 입력 참조)

- stage139_decision(139단계 판정): `{rel(DECISION_PATH)}`
- stage139_review(139단계 검토): `{rel(REPORT_PATH)}`
- stage139_comparison(139단계 비교): `{rel(COMPARISON_PATH)}`
- stage138_summary(138단계 요약): `{rel(SOURCE_SUMMARY)}`
- stage138_segment_kpi(138단계 구간 KPI): `{rel(SOURCE_SEGMENTS)}`
- stage138_risk_atr_telemetry(138단계 위험/ATR 원격측정): `{rel(SOURCE_RISK_ATR)}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "03_reviews/review_index.md",
        """# Stage140 Review Index(140단계 검토 색인)

Stage140(140단계)는 active_planned(활성 계획) 상태다. Effect(효과): 새 수리는 reverse supply(반전 공급)와 late concentration(후반 집중)만 다룬다.
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "04_selected/selection_status.md",
        f"""# Stage140 Selection Status(140단계 선택 상태)

- stage_status(단계 상태): `active_planned_from_stage139`
- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- source_stage(원천 단계): `{STAGE_ID}`
- source_decision(원천 판정): `{DECISION}`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- selected_research_baseline(선택 연구 기준): `none`
- claim_boundary(주장 경계): `{BOUNDARY}`
""",
    )


def update_current_truth() -> None:
    write_md(
        CURRENT_WORKING_STATE_PATH,
        f"""# Current Working State(현재 작업 상태)

- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- active_stage(활성 단계): `{NEXT_STAGE_ID}`
- selected_research_baseline(선택 연구 기준): `none`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- adapter_under_review(검토 중 어댑터): `stage138_reverse_supply_small_gain_candidate`
- status(상태): `stage139_closed_{DECISION}_stage140_open_planned`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage139(139단계)는 Stage138(138단계)의 +1 OOS trade(미래구간 거래 1건 증가)를 small gain candidate(작은 증가 후보)로만 판정했다. Effect(효과): reverse-on-opposite(반대 신호 반전)은 보존하지만, 전체 목표 완료나 최종 후보로 과장하지 않는다.

## Latest Stage139 Evidence(최신 139단계 근거)

- run(실행): `{RUN_ID}`
- decision(판정): `{DECISION}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- report(보고서): `{rel(REPORT_PATH)}`
- comparison(비교): `{rel(COMPARISON_PATH)}`
- route_decision(경로 판정): `{rel(ROUTE_DECISION_PATH)}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준선), legacy_inheritance(레거시 상속), overall_goal_complete(전체 목표 완료).
""",
    )
    text = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig") if path_exists(WORKSPACE_STATE_PATH) else ""
    text = re.sub(r"^current_run_id:.*$", f"current_run_id: {NEXT_RUN_ID}", text, count=1, flags=re.MULTILINE)
    text = re.sub(r"^active_stage:.*$", f"active_stage: {NEXT_STAGE_ID}", text, count=1, flags=re.MULTILINE)
    focus = f"""current_focus:
- >-
  Stage139(139단계) closed(종료) as `{DECISION}` and Stage140(140단계) `{NEXT_STAGE_ID}` is active_planned(활성 계획). Effect(효과): reverse-on-opposite(반대 신호 반전)만 다음 bounded repair(경계 수리) 축으로 남긴다.
- >-
  Stage139 evidence(139단계 근거)는 `{rel(REPORT_PATH)}`, `{rel(COMPARISON_PATH)}`, `{rel(ROUTE_DECISION_PATH)}`에 있다. Effect(효과): +1 trade(거래 1건 증가)는 보존하되 충분하지 않음을 기록한다.
- >-
  Target surface(목표 표면)는 `{TARGET_SURFACE}`이고 legacy 34D(레거시 34D)는 lesson-only KPI target(교훈 전용 핵심 성과 지표 목표)이다. Effect(효과): v2-native research(v2 고유 연구)만 계속한다.

"""
    text = re.sub(r"(?ms)^current_focus:\r?\n.*?(?=\r?\nstage\d+_)", focus, text, count=1) if re.search(r"(?ms)^current_focus:\r?\n.*?(?=\r?\nstage\d+_)", text) else text.rstrip() + "\n" + focus
    block = f"""
stage139_stage138_trade_supply_followup_review:
  packet_id: {PACKET_ID}
  stage_id: {STAGE_ID}
  status: closed_review_only
  current_run_id: {RUN_ID}
  source_stage: {SOURCE_STAGE138_ID}
  source_stage138_closeout_commit: {SOURCE_STAGE138_CLOSEOUT_COMMIT}
  source_stage138_hash_record_commit: {SOURCE_STAGE138_HASH_RECORD_COMMIT}
  decision: {DECISION}
  report_path: {rel(REPORT_PATH)}
  decision_path: {rel(DECISION_PATH)}
  next_action: {NEXT_RUN_ID}
  pushed_commit_hash: pending_until_push
  boundary: {BOUNDARY}

stage140_reverse_supply_late_concentration_repair:
  packet_id: {NEXT_PACKET_ID}
  stage_id: {NEXT_STAGE_ID}
  status: active_planned_from_stage139
  current_run_id: {NEXT_RUN_ID}
  source_stage: {STAGE_ID}
  source_decision: {DECISION}
  next_action: run_stage140_reverse_supply_late_concentration_repair
  boundary: {BOUNDARY}
"""
    text = re.sub(r"(?ms)\nstage139_stage138_trade_supply_followup_review:.*?(?=\nstage\d+_|$)", "\n", text)
    text = re.sub(r"(?ms)\nstage140_reverse_supply_late_concentration_repair:.*?(?=\nstage\d+_|$)", "\n", text)
    io_path(WORKSPACE_STATE_PATH).write_text(text.rstrip() + "\n" + block, encoding="utf-8-sig")


def append_changelog() -> None:
    existing = io_path(CHANGELOG_PATH).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG_PATH) else ""
    if RUN_ID in existing:
        return
    entry = (
        f"\n## {utc_now()} Stage139 Stage138 trade supply follow-up closeout(139단계 138단계 거래 공급 후속 종료)\n\n"
        f"- action(행동): closed(종료) `{STAGE_ID}` with decision(판정) `{DECISION}`.\n"
        "- effect(효과): reverse-on-opposite(반대 신호 반전)만 다음 Stage140(140단계) 수리 축으로 보존하고 flat exit(평탄 청산) 손상 축은 제외했다.\n"
        f"- boundary(주장 경계): `{BOUNDARY}`.\n"
    )
    io_path(CHANGELOG_PATH).write_text(existing.rstrip() + entry, encoding="utf-8-sig")


def refresh_artifact_registry(ledger_payload: Mapping[str, Any]) -> dict[str, Any]:
    artifact_payload = upsert_csv_rows(ARTIFACT_REGISTRY_PATH, ARTIFACT_COLUMNS, artifact_rows(), key="artifact_id")
    refreshed = dict(ledger_payload)
    refreshed["artifact_registry"] = artifact_payload
    return refreshed


def main() -> int:
    review = build_review()
    write_stage_docs()
    write_csv(COMPARISON_PATH, review["comparison"])
    write_csv(ROUTE_DECISION_PATH, review["route"])
    write_json(SUMMARY_JSON_PATH, review)
    write_md(REPORT_PATH, report_markdown(review))
    write_md(DECISION_PATH, decision_markdown(review))
    ledger_payload = write_ledgers(review)
    ledger_payload = refresh_artifact_registry(ledger_payload)
    write_packet_files(review, ledger_payload)
    update_current_truth()
    append_changelog()
    ledger_payload = refresh_artifact_registry(ledger_payload)
    write_packet_files(review, ledger_payload)
    print(
        json.dumps(
            {
                "status": "ok",
                "run_id": RUN_ID,
                "decision": DECISION,
                "summary_json": rel(SUMMARY_JSON_PATH),
                "comparison_csv": rel(COMPARISON_PATH),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
