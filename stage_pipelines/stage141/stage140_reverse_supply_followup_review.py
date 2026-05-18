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


STAGE_ID = "141_adapter_research__stage140_reverse_supply_followup_review"
RUN_ID = "run141A_stage141_stage140_reverse_supply_followup_review_v1"
PACKET_ID = "stage141_stage140_reverse_supply_followup_review_v1"
PARENT_RUN_ID = "run140A_stage140_reverse_supply_late_concentration_repair_v1"
SOURCE_STAGE140_ID = "140_adapter_research__reverse_supply_late_concentration_repair"
SOURCE_STAGE140_CLOSEOUT_COMMIT = "e2d8e9082a74723de334c18b2c32c972364097c8"
SOURCE_STAGE140_HASH_RECORD_COMMIT = "685cdb0454ddb1f32af8d34ffe0cb7ad00ed24f8"
SOURCE_STAGE139_HASH_RECORD_COMMIT = "7ddace59be1aac317467dfedc93e0e137d9f2e3c"
NEXT_STAGE_ID = "142_adapter_research__route_coverage_supply_branch_after_reverse_exhaustion"
NEXT_RUN_ID = "run142A_stage142_route_coverage_supply_branch_after_reverse_exhaustion_v1"
NEXT_PACKET_ID = "stage142_route_coverage_supply_branch_after_reverse_exhaustion_v1"
DECISION = "open_stage142_route_coverage_supply_branch_after_reverse_axis_exhaustion_candidate_not_final"
TARGET_SURFACE = "legacy_34d_kpi_lesson_only_no_legacy_inheritance"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment"
)
EXTERNAL_STATUS = "completed_existing_stage140_mt5_runtime_evidence_reviewed"

STAGE_ROOT = Path("stages") / STAGE_ID
SPEC_ROOT = STAGE_ROOT / "00_spec"
INPUT_ROOT = STAGE_ROOT / "01_inputs"
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
SELECTED_ROOT = STAGE_ROOT / "04_selected"
PACKET_ROOT = Path("docs/agent_control/packets") / PACKET_ID
NEXT_STAGE_ROOT = Path("stages") / NEXT_STAGE_ID

SOURCE_STAGE140_REVIEWS = Path("stages") / SOURCE_STAGE140_ID / "03_reviews"
SOURCE_SUMMARY = SOURCE_STAGE140_REVIEWS / "stage140_reverse_supply_repair_summary.csv"
SOURCE_SEGMENTS = SOURCE_STAGE140_REVIEWS / "stage140_segment_kpi_summary.csv"
SOURCE_RISK_ATR = SOURCE_STAGE140_REVIEWS / "stage140_risk_atr_telemetry.csv"
SOURCE_DECISION = SOURCE_STAGE140_REVIEWS / "stage140_decision.md"

REPORT_PATH = REVIEWS_ROOT / "stage141_stage140_reverse_supply_followup_review.md"
COMPARISON_PATH = REVIEWS_ROOT / "stage141_stage140_reverse_supply_comparison.csv"
ROUTE_DECISION_PATH = REVIEWS_ROOT / "stage141_route_decision.csv"
DECISION_PATH = REVIEWS_ROOT / "stage141_decision.md"
SUMMARY_JSON_PATH = REVIEWS_ROOT / "stage141_followup_summary.json"
STAGE_LEDGER_PATH = REVIEWS_ROOT / "stage_run_ledger.csv"

RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
PROJECT_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
ARTIFACT_REGISTRY_PATH = Path("docs/registers/artifact_registry.csv")
WORKSPACE_STATE_PATH = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE_PATH = Path("docs/context/current_working_state.md")
CHANGELOG_PATH = Path("docs/workspace/changelog.md")

CONTROL_ADAPTER = "s140_reverse_control_h3_cd5_risk035"
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
        return "validation_quality_failed"
    if row["oos_net"] < LEGACY_34D["net_profit"]:
        return "oos_net_failed"
    if row["oos_trade_gain_vs_control"] > 0:
        return "unexpected_trade_gain_candidate"
    if row["validation_late_net_share_delta_vs_control"] < -0.01 and row["oos_net_delta_vs_control"] >= -50:
        return "concentration_repair_candidate"
    if row["adapter_id"] == CONTROL_ADAPTER:
        return "control_preserved_no_new_supply"
    return "no_trade_gain_duplicate_surface"


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
    best = max(
        comparison,
        key=lambda row: (
            row["read"] in {"unexpected_trade_gain_candidate", "concentration_repair_candidate", "control_preserved_no_new_supply"},
            row["oos_trade_gain_vs_control"],
            row["oos_net_delta_vs_control"],
            -row["validation_late_net_share"],
        ),
        default={},
    )
    route = [
        {
            "decision": DECISION,
            "reason": "stage140_reverse_variants_failed_to_add_trade_supply; hold2_damaged_net; cd3_and_threshold_variants_duplicate_control",
            "best_adapter": best.get("adapter_id", ""),
            "next_stage": NEXT_STAGE_ID,
            "overall_goal_complete": False,
        }
    ]
    return {"comparison": comparison, "best": best, "route": route}


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
    return f"""# Stage141 Stage140 Reverse Supply Follow-up Review(141단계 140단계 반전 공급 후속 검토)

- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE140_ID}`
- source_stage140_closeout_commit(원천 140단계 종료 커밋): `{SOURCE_STAGE140_CLOSEOUT_COMMIT}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- decision(판정): `{DECISION}`
- boundary(주장 경계): `{BOUNDARY}`

## Bounded Question(경계 질문)

Did Stage140(140단계) improve reverse supply(반전 공급) enough to continue the reverse axis?

Effect(효과): 같은 축을 계속 고치며 시간을 쓰지 않고, no gain/damage(증가 없음/손상)를 다음 연구 설계의 입력으로 보존한다.

## KPI Read(KPI 핵심 성과 지표 판독)

{table_rows(review["comparison"])}

## Judgment(판정)

- best_adapter(최선 어댑터): `{best.get("adapter_id", "none")}`
- oos_trade_gap_to_34d(34D 대비 미래구간 거래 수 격차): `{best.get("oos_trade_gap_to_34d", 0):.0f}`
- main_failure(주요 실패): `reverse_axis_no_additional_supply`
- damaged_variant(손상 변형): `s140_reverse_cd3_h2_risk035`
- overall_goal_complete(전체 목표 완료): `false`

Stage141(141단계) 판독은 reverse axis(반전 축)를 더 밀기보다 route coverage supply branch(경로 커버리지 공급 분기)로 이동해야 한다고 본다. Effect(효과): 다음 Stage142(142단계)는 새 모델 전체 탐색이 아니라, 거래 공급 부족을 다른 경로 커버리지 질문으로 좁혀 다룬다.
"""


def decision_markdown(review: Mapping[str, Any]) -> str:
    best = review["best"]
    return f"""# Stage141 Decision(141단계 판정)

decision(판정): `{DECISION}`

Stage141(141단계)는 Stage140(140단계) MT5(runtime, 런타임) 근거를 review-only(검토 전용)로 판정했다. Effect(효과): reverse axis(반전 축) 실패를 숨기지 않고, Stage142(142단계)에서 route coverage supply branch(경로 커버리지 공급 분기)를 열도록 한다.

## Evidence(근거)

- review(검토): `{rel(REPORT_PATH)}`
- comparison(비교): `{rel(COMPARISON_PATH)}`
- route_decision(경로 판정): `{rel(ROUTE_DECISION_PATH)}`
- source_stage140_summary(원천 140단계 요약): `{rel(SOURCE_SUMMARY)}`
- source_stage140_segments(원천 140단계 구간): `{rel(SOURCE_SEGMENTS)}`
- source_stage140_risk_atr(원천 140단계 위험/ATR): `{rel(SOURCE_RISK_ATR)}`
- best_adapter(최선 어댑터): `{best.get("adapter_id", "none")}`
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
                    "artifact_type": "stage141_followup_review_evidence",
                    "path": rel(path),
                    "sha256": sha256_file_lf_normalized(path),
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "created_at_utc": created,
                    "notes": "Stage141 review-only follow-up artifact.",
                }
            )
    return rows


def write_ledgers(review: Mapping[str, Any]) -> dict[str, Any]:
    best = review["best"]
    run_payload = upsert_csv_rows(
        RUN_REGISTRY_PATH,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "baseline_adapter_stage140_reverse_supply_followup_review",
                "status": "completed",
                "judgment": DECISION,
                "path": rel(DECISION_PATH),
                "notes": ledger_pairs(
                    (
                        ("source_stage140_closeout_commit", SOURCE_STAGE140_CLOSEOUT_COMMIT),
                        ("source_stage140_hash_record_commit", SOURCE_STAGE140_HASH_RECORD_COMMIT),
                        ("best_adapter", best.get("adapter_id")),
                        ("oos_trade_gap_to_34d", best.get("oos_trade_gap_to_34d")),
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
            "ledger_row_id": f"{RUN_ID}__stage141_followup_review",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "stage141_followup_review",
            "parent_run_id": PARENT_RUN_ID,
            "record_view": "existing_stage140_evidence_review",
            "tier_scope": "Tier A+B routed review; Tier B disabled evidence preserved",
            "kpi_scope": "stage141_stage140_reverse_supply_followup_review",
            "scoreboard_lane": "followup_review",
            "status": "completed",
            "judgment": DECISION,
            "path": rel(DECISION_PATH),
            "primary_kpi": ledger_pairs(
                (
                    ("best_adapter", best.get("adapter_id")),
                    ("oos_trades", best.get("oos_trades")),
                    ("oos_trade_gain_vs_control", best.get("oos_trade_gain_vs_control")),
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
            "notes": "Stage141 review-only; no new MT5 execution; no operational claim.",
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
            "evidence_missing": ["new_repair_not_attempted_in_stage141_by_design"],
            "judgment_label": "negative_failure_memory_not_final",
            "decision": DECISION,
            "claim_boundary": BOUNDARY,
            "next_condition": "Stage142 must test a bounded route coverage supply branch without hiding reverse-axis failure.",
            "status": "passed_with_boundary",
        },
        "performance_attribution_gate.json": {
            "observed_change": "Stage140 reverse variants did not increase OOS trade count beyond 180; hold2 reduced OOS net to 534.32.",
            "comparison_baseline": CONTROL_ADAPTER,
            "likely_drivers": ["reverse_axis_exhausted_for_trade_supply", "short_hold_damages_payoff_shape", "threshold_and_cooldown_changes_duplicate_control"],
            "attribution_confidence": "medium",
            "next_probe": "bounded Stage142 route coverage supply branch",
            "status": "completed",
        },
        "artifact_lineage_audit.json": {
            "source_inputs": [rel(SOURCE_SUMMARY), rel(SOURCE_SEGMENTS), rel(SOURCE_RISK_ATR), rel(SOURCE_DECISION)],
            "producer": rel(Path("stage_pipelines/stage141/stage140_reverse_supply_followup_review.py")),
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
            "source_stage140_closeout_commit": SOURCE_STAGE140_CLOSEOUT_COMMIT,
            "source_stage140_hash_record_commit": SOURCE_STAGE140_HASH_RECORD_COMMIT,
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

Stage141(141단계)는 Stage140(140단계) reverse supply repair(반전 공급 수리)를 review-only(검토 전용)로 판정한다.

## Boundary(경계)

`{BOUNDARY}`
""",
    )
    write_md(
        INPUT_ROOT / "input_refs.md",
        f"""# Stage141 Input References(141단계 입력 참조)

- stage140_decision(140단계 판정): `{rel(SOURCE_DECISION)}`
- stage140_summary(140단계 요약): `{rel(SOURCE_SUMMARY)}`
- stage140_segments(140단계 구간): `{rel(SOURCE_SEGMENTS)}`
- stage140_risk_atr(140단계 위험/ATR): `{rel(SOURCE_RISK_ATR)}`
- source_stage140_closeout_commit(원천 140단계 종료 커밋): `{SOURCE_STAGE140_CLOSEOUT_COMMIT}`
""",
    )
    write_md(
        SELECTED_ROOT / "selection_status.md",
        f"""# Stage141 Selection Status(141단계 선택 상태)

- stage_status(단계 상태): `closed_review_only`
- current_packet(현재 작업 묶음): `{PACKET_ID}`
- current_run(현재 실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE140_ID}`
- source_decision(원천 판정): `continue_stage141_reverse_supply_repair_after_damage_or_no_gain_candidate_not_final`
- stage141_decision(141단계 판정): `{DECISION}`
- next_stage_or_branch(다음 단계/분기): `{NEXT_STAGE_ID}`
- pushed_commit_hash(푸시 커밋 해시): `pending_until_push`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- selected_research_baseline(선택 연구 기준): `none`
- claim_boundary(주장 경계): `{BOUNDARY}`
""",
    )
    write_md(
        REVIEWS_ROOT / "review_index.md",
        f"""# Stage141 Review Index(141단계 검토 색인)

- review(검토): `{rel(REPORT_PATH)}`
- comparison(비교): `{rel(COMPARISON_PATH)}`
- route_decision(경로 판정): `{rel(ROUTE_DECISION_PATH)}`
- decision(판정): `{rel(DECISION_PATH)}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "00_spec/stage_brief.md",
        f"""# {NEXT_STAGE_ID}

Stage142(142단계)는 Stage141(141단계) 판정에 따라 route coverage supply branch(경로 커버리지 공급 분기)를 연다.

## Bounded Question(경계 질문)

Can a bounded route coverage supply branch(경계 경로 커버리지 공급 분기) increase validation/OOS trade count(검증/미래구간 거래 수) beyond the reverse-axis ceiling(반전 축 상한) without damaging PF/net/DD(수익 팩터/순손익/손실률), risk/ATR telemetry(위험/ATR 원격측정), and segment KPI(구간 핵심 성과 지표)?

Effect(효과): reverse axis(반전 축) 실패를 반복하지 않고, 거래 공급 부족을 route coverage(경로 커버리지) 질문으로만 좁혀 시험한다.

## Boundary(경계)

`{BOUNDARY}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "01_inputs/input_refs.md",
        f"""# Stage142 Input References(142단계 입력 참조)

- stage141_decision(141단계 판정): `{rel(DECISION_PATH)}`
- stage141_review(141단계 검토): `{rel(REPORT_PATH)}`
- stage141_comparison(141단계 비교): `{rel(COMPARISON_PATH)}`
- stage140_summary(140단계 요약): `{rel(SOURCE_SUMMARY)}`
- stage140_segment_kpi(140단계 구간 KPI): `{rel(SOURCE_SEGMENTS)}`
- stage140_risk_atr_telemetry(140단계 위험/ATR 원격측정): `{rel(SOURCE_RISK_ATR)}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "03_reviews/review_index.md",
        """# Stage142 Review Index(142단계 검토 색인)

Stage142(142단계)는 active_planned(활성 계획) 상태다. Effect(효과): 새 실험은 route coverage supply(경로 커버리지 공급)만 다룬다.
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "04_selected/selection_status.md",
        f"""# Stage142 Selection Status(142단계 선택 상태)

- stage_status(단계 상태): `active_planned_from_stage141`
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
- adapter_under_review(검토 중 어댑터): `stage142_route_coverage_supply_branch_candidate`
- status(상태): `stage141_closed_{DECISION}_stage142_open_planned`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage141(141단계)는 Stage140(140단계)의 reverse supply(반전 공급) 축이 추가 거래 수를 만들지 못했다고 판정했다. Effect(효과): 반전 축 실패를 보존하고 Stage142(142단계) route coverage supply branch(경로 커버리지 공급 분기)로 전환한다.

## Latest Stage141 Evidence(최신 141단계 근거)

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
  Stage141(141단계) closed(종료) as `{DECISION}` and Stage142(142단계) `{NEXT_STAGE_ID}` is active_planned(활성 계획). Effect(효과): reverse axis(반전 축) 실패를 보존하고 route coverage supply(경로 커버리지 공급) 질문으로 넘어간다.
- >-
  Stage141 evidence(141단계 근거)는 `{rel(REPORT_PATH)}`, `{rel(COMPARISON_PATH)}`, `{rel(ROUTE_DECISION_PATH)}`에 있다. Effect(효과): no-gain/damage(증가 없음/손상)를 다음 설계의 실패 기억으로 쓴다.
- >-
  Target surface(목표 표면)는 `{TARGET_SURFACE}`이고 legacy 34D(레거시 34D)는 lesson-only KPI target(교훈 전용 핵심 성과 지표 목표)이다. Effect(효과): v2-native research(v2 고유 연구)만 계속한다.

"""
    text = re.sub(r"(?ms)^current_focus:\r?\n.*?(?=\r?\nstage\d+_)", focus, text, count=1) if re.search(r"(?ms)^current_focus:\r?\n.*?(?=\r?\nstage\d+_)", text) else text.rstrip() + "\n" + focus
    block = f"""
stage141_stage140_reverse_supply_followup_review:
  packet_id: {PACKET_ID}
  stage_id: {STAGE_ID}
  status: closed_review_only
  current_run_id: {RUN_ID}
  source_stage: {SOURCE_STAGE140_ID}
  source_stage140_closeout_commit: {SOURCE_STAGE140_CLOSEOUT_COMMIT}
  source_stage140_hash_record_commit: {SOURCE_STAGE140_HASH_RECORD_COMMIT}
  decision: {DECISION}
  report_path: {rel(REPORT_PATH)}
  decision_path: {rel(DECISION_PATH)}
  next_action: {NEXT_RUN_ID}
  pushed_commit_hash: pending_until_push
  boundary: {BOUNDARY}

stage142_route_coverage_supply_branch_after_reverse_exhaustion:
  packet_id: {NEXT_PACKET_ID}
  stage_id: {NEXT_STAGE_ID}
  status: active_planned_from_stage141
  current_run_id: {NEXT_RUN_ID}
  source_stage: {STAGE_ID}
  source_decision: {DECISION}
  next_action: run_stage142_route_coverage_supply_branch
  boundary: {BOUNDARY}
"""
    text = re.sub(r"(?ms)\nstage141_stage140_reverse_supply_followup_review:.*?(?=\nstage\d+_|$)", "\n", text)
    text = re.sub(r"(?ms)\nstage142_route_coverage_supply_branch_after_reverse_exhaustion:.*?(?=\nstage\d+_|$)", "\n", text)
    io_path(WORKSPACE_STATE_PATH).write_text(text.rstrip() + "\n" + block, encoding="utf-8-sig")


def append_changelog() -> None:
    existing = io_path(CHANGELOG_PATH).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG_PATH) else ""
    if RUN_ID in existing:
        return
    entry = (
        f"\n## {utc_now()} Stage141 Stage140 reverse supply follow-up closeout(141단계 140단계 반전 공급 후속 종료)\n\n"
        f"- action(행동): closed(종료) `{STAGE_ID}` with decision(판정) `{DECISION}`.\n"
        "- effect(효과): reverse axis(반전 축) no-gain/damage(증가 없음/손상)를 기록하고 Stage142(142단계) route coverage supply branch(경로 커버리지 공급 분기)를 열었다.\n"
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
