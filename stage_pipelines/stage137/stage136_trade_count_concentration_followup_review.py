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


STAGE_ID = "137_adapter_research__stage136_trade_count_concentration_followup_review"
RUN_ID = "run137A_stage137_stage136_trade_count_concentration_followup_review_v1"
PACKET_ID = "stage137_stage136_trade_count_concentration_followup_review_v1"
PARENT_RUN_ID = "run136A_stage136_stage122_survivor_trade_count_concentration_repair_v1"
SOURCE_STAGE136_ID = "136_adapter_research__stage122_survivor_trade_count_concentration_repair"
SOURCE_STAGE136_CLOSEOUT_COMMIT = "fd3728e2aa224b1dede8ee6c36d3aabfab710124"
SOURCE_STAGE136_LATEST_COMMIT = "bd39fb842cc24ba70a25771541c4255ac71f4a85"
NEXT_STAGE_ID = "138_adapter_research__trade_supply_repair_after_stage136_no_gain"
NEXT_RUN_ID = "run138A_stage138_trade_supply_repair_after_stage136_no_gain_v1"
NEXT_PACKET_ID = "stage138_trade_supply_repair_after_stage136_no_gain_v1"
DECISION = "continue_stage138_bounded_trade_supply_repair_after_stage136_no_gain_candidate_not_final"
TARGET_SURFACE = "legacy_34d_kpi_lesson_only_no_legacy_inheritance"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment"
)
EXTERNAL_STATUS = "completed_existing_stage136_mt5_runtime_evidence_reviewed"

STAGE_ROOT = Path("stages") / STAGE_ID
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
SELECTED_ROOT = STAGE_ROOT / "04_selected"
SPEC_ROOT = STAGE_ROOT / "00_spec"
INPUT_ROOT = STAGE_ROOT / "01_inputs"
PACKET_ROOT = Path("docs/agent_control/packets") / PACKET_ID
NEXT_STAGE_ROOT = Path("stages") / NEXT_STAGE_ID

SOURCE_STAGE136_REVIEWS = Path("stages") / SOURCE_STAGE136_ID / "03_reviews"
SOURCE_SUMMARY = SOURCE_STAGE136_REVIEWS / "stage136_trade_count_concentration_repair_summary.csv"
SOURCE_SEGMENTS = SOURCE_STAGE136_REVIEWS / "stage136_segment_kpi_summary.csv"
SOURCE_RISK_ATR = SOURCE_STAGE136_REVIEWS / "stage136_risk_atr_telemetry.csv"
SOURCE_DECISION = SOURCE_STAGE136_REVIEWS / "stage136_decision.md"

REPORT_PATH = REVIEWS_ROOT / "stage137_stage136_followup_review.md"
COMPARISON_PATH = REVIEWS_ROOT / "stage137_stage136_repair_comparison.csv"
ROUTE_DECISION_PATH = REVIEWS_ROOT / "stage137_route_decision.csv"
DECISION_PATH = REVIEWS_ROOT / "stage137_decision.md"
SUMMARY_JSON_PATH = REVIEWS_ROOT / "stage137_followup_summary.json"
STAGE_LEDGER_PATH = REVIEWS_ROOT / "stage_run_ledger.csv"

RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
PROJECT_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
ARTIFACT_REGISTRY_PATH = Path("docs/registers/artifact_registry.csv")
WORKSPACE_STATE_PATH = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE_PATH = Path("docs/context/current_working_state.md")
CHANGELOG_PATH = Path("docs/workspace/changelog.md")

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


def read_label(val: Mapping[str, Any], oos: Mapping[str, Any], control: Mapping[str, Any]) -> str:
    val_net = as_float(val.get("net_profit"))
    oos_net = as_float(oos.get("net_profit"))
    val_pf = as_float(val.get("profit_factor"))
    oos_pf = as_float(oos.get("profit_factor"))
    val_trades = as_float(val.get("trade_count"))
    oos_trades = as_float(oos.get("trade_count"))
    trade_gain = oos_trades - as_float(control.get("trade_count"))
    if trade_gain > 0 and val_net >= LEGACY_34D["net_profit"] and oos_net >= LEGACY_34D["net_profit"]:
        return "trade_gain_candidate_needs_segment_audit"
    if val_pf >= 1.58 and oos_pf >= 1.58 and val_net >= LEGACY_34D["net_profit"] and oos_net >= LEGACY_34D["net_profit"]:
        return "quality_preserved_but_no_trade_count_gain"
    if oos_pf >= 1.58 and oos_net < LEGACY_34D["net_profit"]:
        return "dd_pf_improved_but_net_damaged"
    return "not_safe_repair"


def build_review() -> dict[str, Any]:
    rows = routed_summary_rows()
    segments = segment_rows()
    by_adapter_split: dict[tuple[str, str], dict[str, str]] = {
        (row["adapter_id"], row["split"]): row for row in rows
    }
    adapters = sorted({row["adapter_id"] for row in rows})
    control_oos = by_adapter_split.get(("s136_control_sht54_lng52_cd5_h3_risk035", "oos"), {})
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
            "oos_pf": as_float(oos.get("profit_factor")),
            "oos_net": as_float(oos.get("net_profit")),
            "oos_dd_percent": as_float(oos.get("max_drawdown_percent")),
            "oos_trades": as_float(oos.get("trade_count")),
            "oos_late_net_share": late_share(adapter_id, "oos", segments),
            "oos_net_gap_to_34d": as_float(oos.get("net_profit")) - LEGACY_34D["net_profit"],
            "oos_pf_gap_to_34d": as_float(oos.get("profit_factor")) - LEGACY_34D["profit_factor"],
            "oos_dd_gap_to_34d": as_float(oos.get("max_drawdown_percent")) - LEGACY_34D["max_drawdown_percent"],
            "oos_trade_gap_to_34d": as_float(oos.get("trade_count")) - LEGACY_34D["trade_count"],
            "oos_trade_gain_vs_control": as_float(oos.get("trade_count")) - as_float(control_oos.get("trade_count")),
            "oos_net_delta_vs_control": as_float(oos.get("net_profit")) - as_float(control_oos.get("net_profit")),
            "read": read_label(val, oos, control_oos),
        }
        comparison.append(row)
    best_preserved = max(
        comparison,
        key=lambda row: (
            row["read"] == "quality_preserved_but_no_trade_count_gain",
            row["oos_net"],
            row["validation_net"],
            -row["oos_dd_percent"],
        ),
        default={},
    )
    best_repair = max(
        comparison,
        key=lambda row: (
            row["oos_trade_gain_vs_control"],
            row["oos_net_delta_vs_control"],
            -row["oos_dd_percent"],
        ),
        default={},
    )
    route = [
        {
            "decision": DECISION,
            "reason": "stage136_preserved_control_quality_but_failed_trade_supply_gain",
            "best_preserved_adapter": best_preserved.get("adapter_id", ""),
            "best_repair_attempt": best_repair.get("adapter_id", ""),
            "next_stage": NEXT_STAGE_ID,
            "overall_goal_complete": False,
        }
    ]
    return {"comparison": comparison, "best_preserved": best_preserved, "best_repair": best_repair, "route": route}


def table_rows(rows: Sequence[Mapping[str, Any]]) -> str:
    header = (
        "| adapter(어댑터) | val PF(검증 수익 팩터) | val net(검증 순손익) | "
        "OOS PF(미래구간 수익 팩터) | OOS net(미래구간 순손익) | OOS DD%(미래구간 손실률) | "
        "OOS trades(미래구간 거래 수) | trade gain(거래 증가) | read(판독) |\n"
        "|---|---:|---:|---:|---:|---:|---:|---:|---|"
    )
    body = [
        (
            f"| {row['adapter_id']} | {row['validation_pf']:.2f} | {row['validation_net']:.2f} | "
            f"{row['oos_pf']:.2f} | {row['oos_net']:.2f} | {row['oos_dd_percent']:.2f} | "
            f"{row['oos_trades']:.0f} | {row['oos_trade_gain_vs_control']:.0f} | {row['read']} |"
        )
        for row in rows
    ]
    return "\n".join([header] + body)


def report_markdown(review: Mapping[str, Any]) -> str:
    best = review["best_preserved"]
    repair = review["best_repair"]
    return f"""# Stage137 Stage136 Follow-up Review(137단계 136단계 후속 검토)

- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE136_ID}`
- source_stage136_closeout_commit(원천 136단계 종료 커밋): `{SOURCE_STAGE136_CLOSEOUT_COMMIT}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- decision(판정): `{DECISION}`
- boundary(주장 경계): `{BOUNDARY}`

## Bounded Question(경계 질문)

Stage136(136단계)이 더 안전한 후보를 만들었는가, 아니면 trade supply(거래 공급) 수리를 새 bounded stage(경계 단계)로 계속해야 하는가?

Effect(효과): Stage136(136단계) 안에서 계속 고치지 않고, 결과를 판정해서 다음 질문만 연다.

## KPI Read(KPI 판독)

{table_rows(review["comparison"])}

## Judgment(판정)

- best_preserved_adapter(가장 잘 보존된 어댑터): `{best.get("adapter_id", "none")}`
- best_repair_attempt(가장 나은 수리 시도): `{repair.get("adapter_id", "none")}`
- observed_change(관찰 변화): Stage136(136단계)은 OOS trade count(미래구간 거래 수)를 179에서 늘리지 못했다.
- likely_driver(가능 원인): threshold/cooldown(임계값/대기시간) 조정이 signal supply(신호 공급) 자체를 늘리지 못했다.
- risk_tradeoff(위험 절충): risk030(위험 3.0%) 변형은 drawdown(손실률)을 낮췄지만 OOS net(미래구간 순손익)을 858.22로 낮췄다.
- claim_boundary(주장 경계): candidate_not_final(후보일 뿐 최종 아님), research_development_only(연구개발 전용).

## Next(다음)

next_stage_or_branch(다음 단계/분기): `{NEXT_STAGE_ID}`

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), overall goal complete(전체 목표 완료).
"""


def decision_markdown(review: Mapping[str, Any]) -> str:
    best = review["best_preserved"]
    return f"""# Stage137 Decision(137단계 판정)

decision(판정): `{DECISION}`

Stage137(137단계)는 Stage136(136단계) MT5(runtime, 런타임) 근거를 review-only(검토 전용)로 판정했다. Effect(효과): Stage136 수리가 거래 수를 늘리지 못했음을 보존하고 Stage138(138단계) trade supply repair(거래 공급 수리)로 넘긴다.

## Evidence(근거)

- review(검토): `{rel(REPORT_PATH)}`
- comparison(비교): `{rel(COMPARISON_PATH)}`
- route_decision(경로 판정): `{rel(ROUTE_DECISION_PATH)}`
- source_stage136_summary(원천 136단계 요약): `{rel(SOURCE_SUMMARY)}`
- source_stage136_segments(원천 136단계 구간): `{rel(SOURCE_SEGMENTS)}`
- source_stage136_risk_atr(원천 136단계 위험/ATR): `{rel(SOURCE_RISK_ATR)}`
- best_preserved_adapter(가장 잘 보존된 어댑터): `{best.get("adapter_id", "none")}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`

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
                    "artifact_type": "stage137_followup_review_evidence",
                    "path": rel(path),
                    "sha256": sha256_file_lf_normalized(path),
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "created_at_utc": created,
                    "notes": "Stage137 review-only follow-up artifact.",
                }
            )
    return rows


def write_ledgers(review: Mapping[str, Any], artifacts: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    best = review["best_preserved"]
    run_payload = upsert_csv_rows(
        RUN_REGISTRY_PATH,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "baseline_adapter_stage136_followup_review",
                "status": "completed",
                "judgment": DECISION,
                "path": rel(DECISION_PATH),
                "notes": ledger_pairs(
                    (
                        ("source_stage136_closeout_commit", SOURCE_STAGE136_CLOSEOUT_COMMIT),
                        ("source_stage136_latest_commit", SOURCE_STAGE136_LATEST_COMMIT),
                        ("best_preserved_adapter", best.get("adapter_id")),
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
            "ledger_row_id": f"{RUN_ID}__stage137_followup_review",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "stage137_followup_review",
            "parent_run_id": PARENT_RUN_ID,
            "record_view": "existing_stage136_evidence_review",
            "tier_scope": "Tier A+B routed review; Tier B disabled evidence preserved",
            "kpi_scope": "stage137_stage136_trade_count_concentration_followup_review",
            "scoreboard_lane": "followup_review",
            "status": "completed",
            "judgment": DECISION,
            "path": rel(DECISION_PATH),
            "primary_kpi": ledger_pairs(
                (
                    ("best_preserved_adapter", best.get("adapter_id")),
                    ("oos_net", best.get("oos_net")),
                    ("oos_pf", best.get("oos_pf")),
                    ("oos_trades", best.get("oos_trades")),
                    ("oos_trade_gap_to_34d", best.get("oos_trade_gap_to_34d")),
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
            "notes": "Stage137 review-only; no new MT5 execution; no operational claim.",
        }
    ]
    stage_payload = upsert_csv_rows(STAGE_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, ledger_rows, key="ledger_row_id")
    project_payload = upsert_csv_rows(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, ledger_rows, key="ledger_row_id")
    artifact_payload = upsert_csv_rows(ARTIFACT_REGISTRY_PATH, ARTIFACT_COLUMNS, list(artifacts), key="artifact_id")
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
            "evidence_missing": ["new_trade_supply_repair_not_attempted_in_stage137_by_design"],
            "judgment_label": "inconclusive",
            "decision": DECISION,
            "claim_boundary": BOUNDARY,
            "next_condition": "Stage138 must increase trade supply without damaging validation/OOS PF, net, DD, risk/ATR telemetry, or concentration.",
            "status": "passed_with_boundary",
        },
        "performance_attribution_gate.json": {
            "observed_change": "Stage136 variants did not increase OOS trade count above 179.",
            "comparison_baseline": "s136_control_sht54_lng52_cd5_h3_risk035",
            "likely_drivers": ["threshold_cooldown_changes_did_not_create_new_signal_supply", "risk030_lowered_net_while_reducing_dd"],
            "attribution_confidence": "medium",
            "next_probe": "bounded Stage138 trade supply repair",
            "status": "completed",
        },
        "artifact_lineage_audit.json": {
            "source_inputs": [rel(SOURCE_SUMMARY), rel(SOURCE_SEGMENTS), rel(SOURCE_RISK_ATR), rel(SOURCE_DECISION)],
            "producer": rel(Path("stage_pipelines/stage137/stage136_trade_count_concentration_followup_review.py")),
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
            "source_stage136_closeout_commit": SOURCE_STAGE136_CLOSEOUT_COMMIT,
            "source_stage136_latest_commit": SOURCE_STAGE136_LATEST_COMMIT,
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

Stage137(137단계)는 Stage136(136단계) trade count/concentration repair(거래 수/집중 수리)를 review-only(검토 전용)로 판정한다.

## Boundary(경계)

`{BOUNDARY}`
""",
    )
    write_md(
        INPUT_ROOT / "input_refs.md",
        f"""# Stage137 Input References(137단계 입력 참조)

- stage136_decision(136단계 판정): `{rel(SOURCE_DECISION)}`
- stage136_summary(136단계 요약): `{rel(SOURCE_SUMMARY)}`
- stage136_segments(136단계 구간): `{rel(SOURCE_SEGMENTS)}`
- stage136_risk_atr(136단계 위험/ATR): `{rel(SOURCE_RISK_ATR)}`
- source_stage136_closeout_commit(원천 136단계 종료 커밋): `{SOURCE_STAGE136_CLOSEOUT_COMMIT}`
""",
    )
    write_md(
        SELECTED_ROOT / "selection_status.md",
        f"""# Stage137 Selection Status(137단계 선택 상태)

- stage_status(단계 상태): `closed_review_only`
- current_packet(현재 작업 묶음): `{PACKET_ID}`
- current_run(현재 실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE136_ID}`
- source_decision(원천 판정): `continue_trade_count_concentration_repair_in_new_bounded_stage`
- stage137_decision(137단계 판정): `{DECISION}`
- next_stage_or_branch(다음 단계/분기): `{NEXT_STAGE_ID}`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- selected_research_baseline(선택 연구 기준): `none`
- claim_boundary(주장 경계): `{BOUNDARY}`
""",
    )
    write_md(
        REVIEWS_ROOT / "review_index.md",
        f"""# Stage137 Review Index(137단계 검토 색인)

- review(검토): `{rel(REPORT_PATH)}`
- comparison(비교): `{rel(COMPARISON_PATH)}`
- route_decision(경로 판정): `{rel(ROUTE_DECISION_PATH)}`
- decision(판정): `{rel(DECISION_PATH)}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "00_spec/stage_brief.md",
        f"""# {NEXT_STAGE_ID}

Stage138(138단계)는 Stage136/137(136/137단계)에서 확인된 trade count(거래 수) 정체를 bounded repair(경계 수리)로 다룬다.

## Bounded Question(경계 질문)

Can a bounded trade supply repair(거래 공급 수리) increase validation/OOS trade count(검증/미래구간 거래 수) without damaging PF(수익 팩터), net(순손익), DD(손실률), risk/ATR telemetry(위험/ATR 원격측정), and concentration(집중도)?

Effect(효과): Stage136(136단계)의 좋은 PF/net(수익 팩터/순손익)을 보호하면서 34D(34D) 대비 거래 수 격차를 줄일 수 있는지 좁게 시험한다.

## Boundary(경계)

`{BOUNDARY}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "01_inputs/input_refs.md",
        f"""# Stage138 Input References(138단계 입력 참조)

- stage137_decision(137단계 판정): `{rel(DECISION_PATH)}`
- stage137_review(137단계 검토): `{rel(REPORT_PATH)}`
- stage137_comparison(137단계 비교): `{rel(COMPARISON_PATH)}`
- stage136_summary(136단계 요약): `{rel(SOURCE_SUMMARY)}`
- stage136_segment_kpi(136단계 구간 KPI): `{rel(SOURCE_SEGMENTS)}`
- stage136_risk_atr_telemetry(136단계 위험/ATR 원격측정): `{rel(SOURCE_RISK_ATR)}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "03_reviews/review_index.md",
        """# Stage138 Review Index(138단계 검토 색인)

Stage138(138단계)는 active_planned(활성 계획) 상태다. Effect(효과): 거래 공급 수리를 새 경계 단계에서만 실행한다.
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "04_selected/selection_status.md",
        f"""# Stage138 Selection Status(138단계 선택 상태)

- stage_status(단계 상태): `active_planned_from_stage137`
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
- adapter_under_review(검토 중 어댑터): `stage136_trade_supply_repair_candidate`
- status(상태): `stage137_closed_{DECISION}_stage138_open_planned`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage137(137단계)는 Stage136(136단계) 수리가 trade count(거래 수)를 늘리지 못했다고 판정했다. Effect(효과): Stage138(138단계)에서 trade supply(거래 공급)를 새 경계 수리로만 다룬다.

## Latest Stage137 Evidence(최신 137단계 근거)

- run(실행): `{RUN_ID}`
- decision(판정): `{DECISION}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- report(보고서): `{rel(REPORT_PATH)}`
- comparison(비교): `{rel(COMPARISON_PATH)}`
- route_decision(경로 판정): `{rel(ROUTE_DECISION_PATH)}`

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준선), legacy_inheritance(레거시 상속), overall_goal_complete(전체 목표 완료).
""",
    )
    text = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig") if path_exists(WORKSPACE_STATE_PATH) else ""
    text = re.sub(r"^current_run_id:.*$", f"current_run_id: {NEXT_RUN_ID}", text, count=1, flags=re.MULTILINE)
    text = re.sub(r"^active_stage:.*$", f"active_stage: {NEXT_STAGE_ID}", text, count=1, flags=re.MULTILINE)
    focus = f"""current_focus:
- >-
  Stage137(137단계) closed(종료) as `{DECISION}` and Stage138(138단계) `{NEXT_STAGE_ID}` is active_planned(활성 계획). Effect(효과): Stage136 trade count(거래 수) 정체를 새 경계 수리로 넘긴다.
- >-
  Stage137 evidence(137단계 근거)는 `{rel(REPORT_PATH)}`, `{rel(COMPARISON_PATH)}`, `{rel(ROUTE_DECISION_PATH)}`에 있다. Effect(효과): trade supply(거래 공급) 수리 필요성을 숫자로 고정한다.
- >-
  Target surface(목표 표면)는 `{TARGET_SURFACE}`이고 legacy 34D(레거시 34D)는 lesson-only KPI target(교훈 전용 핵심 성과 지표 목표)이다. Effect(효과): v2-native research(브이투 고유 연구)만 계속한다.

"""
    text = re.sub(r"(?ms)^current_focus:\r?\n.*?(?=\r?\nstage\d+_)", focus, text, count=1) if re.search(r"(?ms)^current_focus:\r?\n.*?(?=\r?\nstage\d+_)", text) else text.rstrip() + "\n" + focus
    block = f"""
stage137_stage136_trade_count_concentration_followup_review:
  packet_id: {PACKET_ID}
  stage_id: {STAGE_ID}
  status: closed_review_only
  current_run_id: {RUN_ID}
  source_stage: {SOURCE_STAGE136_ID}
  source_stage136_closeout_commit: {SOURCE_STAGE136_CLOSEOUT_COMMIT}
  source_stage136_latest_commit: {SOURCE_STAGE136_LATEST_COMMIT}
  decision: {DECISION}
  report_path: {rel(REPORT_PATH)}
  decision_path: {rel(DECISION_PATH)}
  next_action: {NEXT_RUN_ID}
  boundary: {BOUNDARY}

stage138_trade_supply_repair_after_stage136_no_gain:
  packet_id: {NEXT_PACKET_ID}
  stage_id: {NEXT_STAGE_ID}
  status: active_planned_from_stage137
  current_run_id: {NEXT_RUN_ID}
  source_stage: {STAGE_ID}
  source_decision: {DECISION}
  next_action: run_stage138_trade_supply_repair
  boundary: {BOUNDARY}
"""
    text = re.sub(r"(?ms)\nstage137_stage136_trade_count_concentration_followup_review:.*?(?=\nstage\d+_|$)", "\n", text)
    text = re.sub(r"(?ms)\nstage138_trade_supply_repair_after_stage136_no_gain:.*?(?=\nstage\d+_|$)", "\n", text)
    io_path(WORKSPACE_STATE_PATH).write_text(text.rstrip() + "\n" + block, encoding="utf-8-sig")


def append_changelog() -> None:
    existing = io_path(CHANGELOG_PATH).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG_PATH) else ""
    if RUN_ID in existing:
        return
    entry = (
        f"\n## {utc_now()} Stage137 Stage136 follow-up review closeout(137단계 136단계 후속 검토 종료)\n\n"
        f"- action(행동): closed(종료) `{STAGE_ID}` with decision(판정) `{DECISION}`.\n"
        "- effect(효과): Stage136(136단계)이 거래 수를 늘리지 못했음을 기록하고 Stage138(138단계) trade supply repair(거래 공급 수리)로 넘겼다.\n"
        f"- boundary(주장 경계): `{BOUNDARY}`.\n"
    )
    io_path(CHANGELOG_PATH).write_text(existing.rstrip() + entry, encoding="utf-8-sig")


def main() -> int:
    review = build_review()
    write_csv(COMPARISON_PATH, review["comparison"])
    write_csv(ROUTE_DECISION_PATH, review["route"])
    write_md(REPORT_PATH, report_markdown(review))
    write_md(DECISION_PATH, decision_markdown(review))
    write_json(
        SUMMARY_JSON_PATH,
        {
            "created_at_utc": utc_now(),
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "packet_id": PACKET_ID,
            "decision": DECISION,
            "review": review,
            "claim_boundary": BOUNDARY,
            "overall_goal_complete": False,
        },
    )
    artifacts = artifact_rows()
    ledger_payload = write_ledgers(review, artifacts)
    write_json(
        SUMMARY_JSON_PATH,
        {
            "created_at_utc": utc_now(),
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "packet_id": PACKET_ID,
            "decision": DECISION,
            "review": review,
            "ledger_payload": ledger_payload,
            "claim_boundary": BOUNDARY,
            "overall_goal_complete": False,
        },
    )
    write_packet_files(review, ledger_payload)
    write_stage_docs()
    update_current_truth()
    append_changelog()
    ledger_payload["artifact_registry"] = upsert_csv_rows(
        ARTIFACT_REGISTRY_PATH,
        ARTIFACT_COLUMNS,
        artifact_rows(),
        key="artifact_id",
    )
    write_packet_files(review, ledger_payload)
    print(
        json.dumps(
            json_ready({"status": "ok", "run_id": RUN_ID, "decision": DECISION, "next_stage": NEXT_STAGE_ID}),
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
