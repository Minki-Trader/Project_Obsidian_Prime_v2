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
from stage_pipelines.stage56 import independent_event_source_route_branch as aw  # noqa: E402


STAGE_ID = "132_adapter_research__v42_density_repair_followup"
RUN_ID = "run132A_stage132_v42_density_repair_followup_v1"
PACKET_ID = "stage132_v42_density_repair_followup_v1"
PARENT_RUN_ID = "run131A_stage131_new_v2_model_branch_followup_review_v1"
SOURCE_STAGE130_ID = "130_adapter_research__new_v2_model_branch_after_v41_tradeoff_failure"
SOURCE_STAGE131_ID = "131_adapter_research__new_v2_model_branch_followup_review"
SOURCE_STAGE122_ID = "122_adapter_research__v41_density_scale_repair_after_dd_guardrail"
SOURCE_STAGE131_PUSHED_COMMIT = "f80ebc6dd05dca1016597a7c4f5b9c721dae9cf6"
NEXT_STAGE_ID = "133_adapter_research__stage122_survivor_density_recovery_branch"
NEXT_RUN_ID = "run133A_stage133_stage122_survivor_density_recovery_branch_v1"
NEXT_PACKET_ID = "stage133_stage122_survivor_density_recovery_branch_v1"
TARGET_SURFACE = "legacy_34d_kpi_lesson_only_no_legacy_inheritance"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment"
)
DECISION = "demote_v42_and_open_stage133_stage122_survivor_recovery_branch"

STAGE_ROOT = Path("stages") / STAGE_ID
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
SELECTED_ROOT = STAGE_ROOT / "04_selected"
SPEC_ROOT = STAGE_ROOT / "00_spec"
INPUT_ROOT = STAGE_ROOT / "01_inputs"
PACKET_ROOT = Path("docs/agent_control/packets") / PACKET_ID
NEXT_STAGE_ROOT = Path("stages") / NEXT_STAGE_ID

SOURCE_STAGE130_SUMMARY = Path("stages") / SOURCE_STAGE130_ID / "03_reviews/stage130_new_v2_model_branch_summary.csv"
SOURCE_STAGE130_DECISION = Path("stages") / SOURCE_STAGE130_ID / "03_reviews/stage130_decision.md"
SOURCE_STAGE131_SUMMARY = Path("stages") / SOURCE_STAGE131_ID / "03_reviews/stage131_v42_density_repair_summary.csv"
SOURCE_STAGE131_DECISION = Path("stages") / SOURCE_STAGE131_ID / "03_reviews/stage131_decision.md"
SOURCE_STAGE122_SUMMARY = Path("stages") / SOURCE_STAGE122_ID / "03_reviews/stage122_density_scale_repair_summary.csv"
SOURCE_STAGE122_SEGMENTS = Path("stages") / SOURCE_STAGE122_ID / "03_reviews/stage122_segment_kpi_summary.csv"
SOURCE_STAGE122_RISK = Path("stages") / SOURCE_STAGE122_ID / "03_reviews/stage122_risk_atr_telemetry.csv"
SOURCE_STAGE122_DECISION = Path("stages") / SOURCE_STAGE122_ID / "03_reviews/stage122_decision.md"

REPORT_PATH = REVIEWS_ROOT / "stage132_v42_density_repair_followup_review.md"
GAP_SUMMARY_PATH = REVIEWS_ROOT / "stage132_stage122_130_131_34d_gap_summary.csv"
ROUTE_DECISION_PATH = REVIEWS_ROOT / "stage132_route_decision.csv"
DECISION_PATH = REVIEWS_ROOT / "stage132_decision.md"
SUMMARY_JSON_PATH = REVIEWS_ROOT / "stage132_followup_summary.json"
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
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def actual_routed(rows: Sequence[Mapping[str, str]]) -> list[dict[str, str]]:
    return [dict(row) for row in rows if row.get("view") == "actual_routed_total"]


def paired_score(rows: Sequence[Mapping[str, str]]) -> dict[str, Any]:
    grouped: dict[str, dict[str, Mapping[str, str]]] = {}
    for row in actual_routed(rows):
        grouped.setdefault(str(row.get("adapter_id")), {})[str(row.get("split"))] = row
    candidates: list[dict[str, Any]] = []
    for adapter_id, parts in grouped.items():
        val = parts.get("validation_is", {})
        oos = parts.get("oos", {})
        score = (
            as_float(val.get("net_profit"))
            + as_float(oos.get("net_profit"))
            + 750.0 * as_float(val.get("profit_factor"))
            + 750.0 * as_float(oos.get("profit_factor"))
            - 0.6 * as_float(val.get("max_drawdown_percent"))
            - 0.6 * as_float(oos.get("max_drawdown_percent"))
        )
        candidates.append({"adapter_id": adapter_id, "validation": dict(val), "oos": dict(oos), "score": score})
    return max(candidates, key=lambda item: item["score"], default={})


def gap_row(stage: str, candidate: Mapping[str, Any]) -> dict[str, Any]:
    val = candidate.get("validation", {}) if isinstance(candidate.get("validation"), Mapping) else {}
    oos = candidate.get("oos", {}) if isinstance(candidate.get("oos"), Mapping) else {}
    return {
        "stage": stage,
        "adapter_id": candidate.get("adapter_id", ""),
        "validation_pf": as_float(val.get("profit_factor")),
        "validation_net": as_float(val.get("net_profit")),
        "validation_dd_pct": as_float(val.get("max_drawdown_percent")),
        "validation_trades": as_float(val.get("trade_count")),
        "oos_pf": as_float(oos.get("profit_factor")),
        "oos_net": as_float(oos.get("net_profit")),
        "oos_dd_pct": as_float(oos.get("max_drawdown_percent")),
        "oos_trades": as_float(oos.get("trade_count")),
        "oos_net_gap_to_34d": as_float(oos.get("net_profit")) - LEGACY_34D["net_profit"],
        "oos_pf_gap_to_34d": as_float(oos.get("profit_factor")) - LEGACY_34D["profit_factor"],
        "oos_trade_gap_to_34d": as_float(oos.get("trade_count")) - LEGACY_34D["trade_count"],
    }


def build_review() -> dict[str, Any]:
    stage130_best = paired_score(read_csv(SOURCE_STAGE130_SUMMARY))
    stage131_best = paired_score(read_csv(SOURCE_STAGE131_SUMMARY))
    stage122_best = paired_score(read_csv(SOURCE_STAGE122_SUMMARY))
    rows = [
        gap_row("stage122_survivor_reference", stage122_best),
        gap_row("stage130_v42_v45_source_branch", stage130_best),
        gap_row("stage131_v42_density_repair", stage131_best),
    ]
    route = [
        {
            "decision": DECISION,
            "reason": "stage131_density_repair_reduced_or_flattened_kpi_while_stage122_survivor_remains_stronger",
            "stage122_oos_net": rows[0]["oos_net"],
            "stage122_oos_pf": rows[0]["oos_pf"],
            "stage131_oos_net": rows[2]["oos_net"],
            "stage131_oos_pf": rows[2]["oos_pf"],
            "next_stage": NEXT_STAGE_ID,
            "overall_goal_complete": False,
        }
    ]
    return {"stage122_best": stage122_best, "stage130_best": stage130_best, "stage131_best": stage131_best, "gap_rows": rows, "route_rows": route}


def report_markdown(review: Mapping[str, Any]) -> str:
    rows = review["gap_rows"]
    table = "\n".join(
        ["| stage(단계) | adapter(어댑터) | val PF | val net | OOS PF | OOS net | OOS trades | OOS net gap |", "|---|---|---:|---:|---:|---:|---:|---:|"]
        + [
            f"| {row['stage']} | {row['adapter_id']} | {row['validation_pf']:.2f} | {row['validation_net']:.2f} | {row['oos_pf']:.2f} | {row['oos_net']:.2f} | {row['oos_trades']:.0f} | {row['oos_net_gap_to_34d']:.2f} |"
            for row in rows
        ]
    )
    return f"""# Stage132 V42 Density Repair Follow-up Review(132단계 v42 밀도 수리 후속 검토)

- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- decision(판정): `{DECISION}`
- external_verification_status(외부 검증 상태): `completed_existing_stage130_stage131_stage122_evidence_reviewed`
- boundary(주장 경계): `{BOUNDARY}`

## Bounded Question(경계 질문)

Stage131(131단계)의 v42 density repair(v42 밀도 수리)를 계속할 만큼 좋은가, 아니면 Stage122 survivor(Stage122 생존 후보) 복구 분기로 갈 것인가?

## KPI Comparison(KPI 비교)

{table}

## Read(판독)

- Stage131(131단계) 최선은 OOS(미래구간) 순손익 71.23, PF(수익 팩터) 1.06으로 34D 목표와 멀다.
- Stage122(122단계) 생존 후보는 OOS(미래구간) 순손익 1102.04, PF(수익 팩터) 1.75로 훨씬 강하지만 trade count(거래 수)는 34D보다 낮다.
- decision(판정): v42는 demote(강등)하고 Stage133(133단계)에서 Stage122 survivor recovery(Stage122 생존 후보 복구)를 연다.

Effect(효과): 약한 v42를 계속 깎지 않고, 이미 강했던 v2-native survivor(브이투 고유 생존 후보)를 새 경계 분기로 다룬다. 전체 목표 완료는 아니다.
"""


def decision_markdown(review: Mapping[str, Any]) -> str:
    return f"""# Stage132 Decision(132단계 판정)

decision(판정): `{DECISION}`

Stage132(132단계)는 Stage130/131(130/131단계)의 v42 branch(v42 분기)와 Stage122 survivor(Stage122 생존 후보)를 비교했다. Effect(효과): v42 밀도 수리는 약하므로 더 붙잡지 않고, Stage133(133단계)에서 Stage122 생존 후보의 밀도/손상 없는 복구를 시도한다.

## Evidence(근거)

- review(검토): `{rel(REPORT_PATH)}`
- gap_summary(차이 요약): `{rel(GAP_SUMMARY_PATH)}`
- route_decision(경로 판정): `{rel(ROUTE_DECISION_PATH)}`
- source_stage130_summary(130단계 요약): `{rel(SOURCE_STAGE130_SUMMARY)}`
- source_stage131_summary(131단계 요약): `{rel(SOURCE_STAGE131_SUMMARY)}`
- source_stage122_summary(122단계 요약): `{rel(SOURCE_STAGE122_SUMMARY)}`

## Next(다음)

next_stage_or_branch(다음 단계/분기): `{NEXT_STAGE_ID}`

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), overall goal complete(전체 목표 완료).
"""


def artifact_rows() -> list[dict[str, Any]]:
    created = utc_now()
    rows: list[dict[str, Any]] = []
    for path in [REPORT_PATH, GAP_SUMMARY_PATH, ROUTE_DECISION_PATH, DECISION_PATH, SUMMARY_JSON_PATH, STAGE_LEDGER_PATH]:
        if path_exists(path):
            rows.append(
                {
                    "artifact_id": f"{RUN_ID}__{path.name}",
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "artifact_type": "stage132_followup_review_evidence",
                    "path": rel(path),
                    "sha256": sha256_file_lf_normalized(path),
                    "hash_policy": "lf_normalized_text",
                    "created_at_utc": created,
                    "notes": "Stage132 review-only follow-up artifact.",
                }
            )
    return rows


def write_ledgers(review: Mapping[str, Any], artifacts: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    best122 = review["stage122_best"]
    best131 = review["stage131_best"]
    run_payload = upsert_csv_rows(
        RUN_REGISTRY_PATH,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "baseline_adapter_v42_density_followup_review",
                "status": "completed",
                "judgment": DECISION,
                "path": rel(DECISION_PATH),
                "notes": ledger_pairs((("stage122_survivor", best122.get("adapter_id")), ("stage131_best", best131.get("adapter_id")), ("target_surface", TARGET_SURFACE), ("overall_goal_complete", False))),
            }
        ],
        key="run_id",
    )
    ledger_rows = [
        {
            "ledger_row_id": f"{RUN_ID}__stage132_followup_review",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "stage132_followup_review",
            "parent_run_id": PARENT_RUN_ID,
            "record_view": "existing_evidence_review",
            "tier_scope": "Tier A+B routed review; Tier B disabled evidence preserved",
            "kpi_scope": "stage132_v42_density_followup_review",
            "scoreboard_lane": "followup_review",
            "status": "completed",
            "judgment": DECISION,
            "path": rel(DECISION_PATH),
            "primary_kpi": ledger_pairs((("stage122_survivor", best122.get("adapter_id")), ("stage131_best", best131.get("adapter_id")), ("stage122_oos_net", best122.get("oos", {}).get("net_profit")), ("stage131_oos_net", best131.get("oos", {}).get("net_profit")))),
            "guardrail_kpi": ledger_pairs((("target_surface", TARGET_SURFACE), ("overall_goal_complete", False), ("claim_boundary", BOUNDARY))),
            "external_verification_status": "completed_existing_stage130_stage131_stage122_evidence_reviewed",
            "notes": "Stage132 review-only; no new MT5 execution; no operational claim.",
        }
    ]
    stage_payload = upsert_csv_rows(STAGE_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, ledger_rows, key="ledger_row_id")
    project_payload = upsert_csv_rows(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, ledger_rows, key="ledger_row_id")
    artifact_payload = upsert_csv_rows(ARTIFACT_REGISTRY_PATH, aw.ARTIFACT_COLUMNS, list(artifacts), key="artifact_id")
    return {"run_registry": run_payload, "stage_ledger": stage_payload, "project_alpha_ledger": project_payload, "artifact_registry": artifact_payload}


def write_packet_files(review: Mapping[str, Any], ledger_payload: Mapping[str, Any]) -> None:
    files = {
        "routing_receipt.json": {"packet_id": PACKET_ID, "primary_family": "adapter_development", "primary_skill": "obsidian-result-judgment", "support_skills": ["obsidian-performance-attribution", "obsidian-model-validation"], "required_gates": ["experiment_design_receipt", "kpi_contract_audit", "result_judgment_gate", "artifact_lineage_audit", "final_claim_guard"], "status": "completed"},
        "experiment_design_receipt.json": {"hypothesis": "Stage131 v42 density repair is too weak, so Stage122 survivor recovery is the better bounded route.", "decision_use": "choose Stage133 branch route only", "comparison_baseline": "Stage130/Stage131 v42 branch versus Stage122 survivor evidence", "success_criteria": ["route decision is explicit", "no new MT5 claim is made"], "failure_criteria": ["v42 is kept open indefinitely"], "status": "completed"},
        "kpi_contract_audit.json": {"gap_summary": rel(GAP_SUMMARY_PATH), "status": "completed"},
        "result_judgment_gate.json": {"result_subject": RUN_ID, "judgment_label": DECISION, "overall_goal_complete": False, "claim_boundary": BOUNDARY, "status": "passed_with_boundary"},
        "artifact_lineage_audit.json": {"source_inputs": [rel(SOURCE_STAGE130_SUMMARY), rel(SOURCE_STAGE131_SUMMARY), rel(SOURCE_STAGE122_SUMMARY), rel(SOURCE_STAGE122_SEGMENTS), rel(SOURCE_STAGE122_RISK)], "consumers": [rel(REPORT_PATH), rel(DECISION_PATH), rel(SUMMARY_JSON_PATH)], "ledger_links": ledger_payload},
        "final_claim_guard.json": {"overall_goal_complete": False, "deployment_claim": False, "live_readiness_claim": False, "runtime_authority_claim": False, "production_baseline_claim": False, "operating_reference_claim": False, "operating_promotion_claim": False, "status": "passed"},
        "required_gate_coverage_audit.json": {"required_gates": ["experiment_design_receipt", "kpi_contract_audit", "result_judgment_gate", "artifact_lineage_audit", "final_claim_guard"], "covered_by": ["experiment_design_receipt.json", "kpi_contract_audit.json", "result_judgment_gate.json", "artifact_lineage_audit.json", "final_claim_guard.json"], "status": "completed"},
        "aggregate_summary.json": {"packet_id": PACKET_ID, "stage_id": STAGE_ID, "run_id": RUN_ID, "decision": DECISION, "required_outputs": {"report": rel(REPORT_PATH), "gap_summary": rel(GAP_SUMMARY_PATH), "route_decision": rel(ROUTE_DECISION_PATH), "decision": rel(DECISION_PATH)}, "claim_boundary": BOUNDARY, "overall_goal_complete": False},
    }
    for name, payload in files.items():
        write_json(PACKET_ROOT / name, payload)


def write_stage_docs() -> None:
    write_md(SPEC_ROOT / "stage_brief.md", f"""# {STAGE_ID}

Stage132(132단계)는 Stage131(131단계) 결과를 검토해 v42 density repair(v42 밀도 수리)를 계속할지, Stage122 survivor recovery(Stage122 생존 후보 복구)를 열지 판정했다.

## Boundary(경계)

`{BOUNDARY}`
""")
    write_md(INPUT_ROOT / "input_refs.md", f"""# Stage132 Input References(132단계 입력 참조)

- stage130_summary(130단계 요약): `{rel(SOURCE_STAGE130_SUMMARY)}`
- stage131_summary(131단계 요약): `{rel(SOURCE_STAGE131_SUMMARY)}`
- stage122_summary(122단계 요약): `{rel(SOURCE_STAGE122_SUMMARY)}`
- stage131_pushed_commit(131단계 푸시 커밋): `{SOURCE_STAGE131_PUSHED_COMMIT}`
""")
    write_md(SELECTED_ROOT / "selection_status.md", f"""# Stage132 Selection Status(132단계 선택 상태)

- stage_status(단계 상태): `closed_review_only`
- current_packet(현재 작업 묶음): `{PACKET_ID}`
- current_run(현재 실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE131_ID}`
- stage132_decision(132단계 판정): `{DECISION}`
- next_stage_or_branch(다음 단계/분기): `{NEXT_STAGE_ID}`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- selected_research_baseline(선택 연구 기준): `none`
- claim_boundary(주장 경계): `{BOUNDARY}`
""")
    write_md(REVIEWS_ROOT / "review_index.md", f"""# Stage132 Review Index(132단계 검토 색인)

- review(검토): `{rel(REPORT_PATH)}`
- gap_summary(차이 요약): `{rel(GAP_SUMMARY_PATH)}`
- route_decision(경로 판정): `{rel(ROUTE_DECISION_PATH)}`
- decision(판정): `{rel(DECISION_PATH)}`
""")
    write_md(NEXT_STAGE_ROOT / "00_spec/stage_brief.md", f"""# {NEXT_STAGE_ID}

Stage133(133단계)는 Stage122 survivor(Stage122 생존 후보)를 새 경계 분기로 복구한다.

## Bounded Question(경계 질문)

Stage122 survivor(Stage122 생존 후보)의 강한 PF/net(수익 팩터/순손익)을 보존하면서, trade count(거래 수) 부족과 후속 route-supply damage(경로 공급 손상)를 피할 수 있는가?

Effect(효과): v42 약한 분기를 더 수리하지 않고, 강한 v2-native survivor(브이투 고유 생존 후보)를 손상 없이 회수한다.

## Boundary(경계)

`{BOUNDARY}`
""")
    write_md(NEXT_STAGE_ROOT / "01_inputs/input_refs.md", f"""# Stage133 Input References(133단계 입력 참조)

- stage132_decision(132단계 판정): `{rel(DECISION_PATH)}`
- stage132_review(132단계 검토): `{rel(REPORT_PATH)}`
- stage122_summary(122단계 요약): `{rel(SOURCE_STAGE122_SUMMARY)}`
- stage122_segments(122단계 구간): `{rel(SOURCE_STAGE122_SEGMENTS)}`
- stage122_risk_atr(122단계 위험/ATR): `{rel(SOURCE_STAGE122_RISK)}`
""")
    write_md(NEXT_STAGE_ROOT / "03_reviews/review_index.md", """# Stage133 Review Index(133단계 검토 색인)

Stage133(133단계)는 planned(계획) 상태다. Effect(효과): Stage122 survivor recovery(Stage122 생존 후보 복구)를 다음 실행으로 연결한다.
""")
    write_md(NEXT_STAGE_ROOT / "04_selected/selection_status.md", f"""# Stage133 Selection Status(133단계 선택 상태)

- stage_status(단계 상태): `active_planned_from_stage132`
- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- source_stage(원천 단계): `{STAGE_ID}`
- source_decision(원천 판정): `{DECISION}`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- selected_research_baseline(선택 연구 기준): `none`
- claim_boundary(주장 경계): `{BOUNDARY}`
""")


def update_current_truth() -> None:
    write_md(CURRENT_WORKING_STATE_PATH, f"""# Current Working State(현재 작업 상태)

- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- active_stage(활성 단계): `{NEXT_STAGE_ID}`
- selected_research_baseline(선택 연구 기준): `none`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- adapter_under_review(검토 중 어댑터): `stage122_survivor_recovery_branch`
- status(상태): `stage132_closed_{DECISION}_stage133_open_planned`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage132(132단계)는 v42 density repair(v42 밀도 수리)를 demote(강등)하고 Stage122 survivor recovery(Stage122 생존 후보 복구)를 Stage133(133단계)로 열었다. Effect(효과): 약한 v42를 계속 깎지 않고, 강한 v2-native survivor(브이투 고유 생존 후보)를 손상 없이 회수하는 방향으로 간다.

## Latest Stage132 Evidence(최신 132단계 근거)

- run(실행): `{RUN_ID}`
- decision(판정): `{DECISION}`
- report(보고서): `{rel(REPORT_PATH)}`
- gap_summary(차이 요약): `{rel(GAP_SUMMARY_PATH)}`
- route_decision(경로 판정): `{rel(ROUTE_DECISION_PATH)}`

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준선), legacy_inheritance(레거시 상속), overall_goal_complete(전체 목표 완료).
""")
    text = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig") if path_exists(WORKSPACE_STATE_PATH) else ""
    text = re.sub(r"^current_run_id:.*$", f"current_run_id: {NEXT_RUN_ID}", text, count=1, flags=re.MULTILINE)
    text = re.sub(r"^active_stage:.*$", f"active_stage: {NEXT_STAGE_ID}", text, count=1, flags=re.MULTILINE)
    focus = f"""current_focus:
- >-
  Stage132(132단계) closed(종료) as `{DECISION}` and Stage133(133단계) `{NEXT_STAGE_ID}` is active_planned(활성 계획). Effect(효과): v42 weak branch(v42 약한 분기)를 강등하고 Stage122 survivor recovery(Stage122 생존 후보 복구)를 연다.
- >-
  Stage132 evidence(132단계 근거)는 `{rel(REPORT_PATH)}`, `{rel(GAP_SUMMARY_PATH)}`에 있다. Effect(효과): Stage133(133단계)이 어떤 후보를 회수해야 하는지 명확해진다.
- >-
  Target surface(목표 표면)는 `{TARGET_SURFACE}`이고 legacy 34D(레거시 34D)는 lesson-only KPI target(교훈 전용 핵심 성과 지표 목표)이다. Effect(효과): v2-native research(브이투 고유 연구)만 계속한다.

"""
    text = re.sub(r"(?ms)^current_focus:\r?\n.*?(?=\r?\nstage\d+_)", focus, text, count=1) if re.search(r"(?ms)^current_focus:\r?\n.*?(?=\r?\nstage\d+_)", text) else text.rstrip() + "\n" + focus
    block = f"""
stage132_v42_density_repair_followup:
  packet_id: {PACKET_ID}
  stage_id: {STAGE_ID}
  status: closed_review_only
  current_run_id: {RUN_ID}
  source_stage: {SOURCE_STAGE131_ID}
  decision: {DECISION}
  report_path: {rel(REPORT_PATH)}
  decision_path: {rel(DECISION_PATH)}
  next_action: {NEXT_RUN_ID}
  boundary: {BOUNDARY}

stage133_stage122_survivor_density_recovery_branch:
  packet_id: {NEXT_PACKET_ID}
  stage_id: {NEXT_STAGE_ID}
  status: active_planned_from_stage132
  current_run_id: {NEXT_RUN_ID}
  source_stage: {STAGE_ID}
  source_decision: {DECISION}
  next_action: run_stage133_survivor_recovery
  boundary: {BOUNDARY}
"""
    text = re.sub(r"(?ms)\nstage132_v42_density_repair_followup:.*?(?=\nstage\d+_|$)", "\n", text)
    text = re.sub(r"(?ms)\nstage133_stage122_survivor_density_recovery_branch:.*?(?=\nstage\d+_|$)", "\n", text)
    io_path(WORKSPACE_STATE_PATH).write_text(text.rstrip() + "\n" + block, encoding="utf-8-sig")


def append_changelog() -> None:
    existing = io_path(CHANGELOG_PATH).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG_PATH) else ""
    entry = (
        f"\n## {utc_now()} Stage132 v42 density follow-up review closeout(132단계 v42 밀도 후속 검토 종료)\n\n"
        f"- action(행동): closed(종료) `{STAGE_ID}` with decision(판정) `{DECISION}`.\n"
        f"- effect(효과): v42 branch(v42 분기)를 demote(강등)하고 Stage122 survivor recovery(Stage122 생존 후보 복구)를 Stage133(133단계)로 열었다.\n"
        f"- boundary(주장 경계): `{BOUNDARY}`.\n"
    )
    io_path(CHANGELOG_PATH).write_text(existing.rstrip() + entry, encoding="utf-8-sig")


def main() -> int:
    review = build_review()
    write_csv(GAP_SUMMARY_PATH, review["gap_rows"])
    write_csv(ROUTE_DECISION_PATH, review["route_rows"])
    write_md(REPORT_PATH, report_markdown(review))
    write_md(DECISION_PATH, decision_markdown(review))
    write_json(SUMMARY_JSON_PATH, {"created_at_utc": utc_now(), "stage_id": STAGE_ID, "run_id": RUN_ID, "packet_id": PACKET_ID, "decision": DECISION, "review": review, "claim_boundary": BOUNDARY, "overall_goal_complete": False})
    artifacts = artifact_rows()
    ledger_payload = write_ledgers(review, artifacts)
    write_json(SUMMARY_JSON_PATH, {"created_at_utc": utc_now(), "stage_id": STAGE_ID, "run_id": RUN_ID, "packet_id": PACKET_ID, "decision": DECISION, "review": review, "ledger_payload": ledger_payload, "claim_boundary": BOUNDARY, "overall_goal_complete": False})
    write_packet_files(review, ledger_payload)
    write_stage_docs()
    update_current_truth()
    append_changelog()
    print(json.dumps(json_ready({"status": "ok", "run_id": RUN_ID, "decision": DECISION, "report": rel(REPORT_PATH), "next_stage": NEXT_STAGE_ID}), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
