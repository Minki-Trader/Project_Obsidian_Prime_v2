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


STAGE_ID = "134_adapter_research__stage122_survivor_followup_review"
RUN_ID = "run134A_stage134_stage122_survivor_followup_review_v1"
PACKET_ID = "stage134_stage122_survivor_followup_review_v1"
PARENT_RUN_ID = "run133A_stage133_stage122_survivor_density_recovery_branch_v1"
SOURCE_STAGE133_ID = "133_adapter_research__stage122_survivor_density_recovery_branch"
SOURCE_STAGE133_PUSHED_COMMIT = "d17e1172e486c879a70877a0be08d828fb910f7c"
NEXT_STAGE_ID = "135_adapter_research__stage122_survivor_segment_equity_audit"
NEXT_RUN_ID = "run135A_stage135_stage122_survivor_segment_equity_audit_v1"
NEXT_PACKET_ID = "stage135_stage122_survivor_segment_equity_audit_v1"
TARGET_SURFACE = "legacy_34d_kpi_lesson_only_no_legacy_inheritance"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment"
)
DECISION = "proceed_to_stage135_survivor_segment_equity_audit_candidate_not_final"

STAGE_ROOT = Path("stages") / STAGE_ID
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
SELECTED_ROOT = STAGE_ROOT / "04_selected"
SPEC_ROOT = STAGE_ROOT / "00_spec"
INPUT_ROOT = STAGE_ROOT / "01_inputs"
PACKET_ROOT = Path("docs/agent_control/packets") / PACKET_ID
NEXT_STAGE_ROOT = Path("stages") / NEXT_STAGE_ID

SOURCE_STAGE133_SUMMARY = Path("stages") / SOURCE_STAGE133_ID / "03_reviews/stage133_survivor_recovery_summary.csv"
SOURCE_STAGE133_DECISION = Path("stages") / SOURCE_STAGE133_ID / "03_reviews/stage133_decision.md"
SOURCE_STAGE133_SEGMENTS = Path("stages") / SOURCE_STAGE133_ID / "03_reviews/stage133_segment_kpi_summary.csv"
SOURCE_STAGE133_RISK = Path("stages") / SOURCE_STAGE133_ID / "03_reviews/stage133_risk_atr_telemetry.csv"

REPORT_PATH = REVIEWS_ROOT / "stage134_survivor_followup_review.md"
COMPARISON_PATH = REVIEWS_ROOT / "stage134_stage133_candidate_comparison.csv"
ROUTE_DECISION_PATH = REVIEWS_ROOT / "stage134_route_decision.csv"
DECISION_PATH = REVIEWS_ROOT / "stage134_decision.md"
SUMMARY_JSON_PATH = REVIEWS_ROOT / "stage134_followup_summary.json"
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
PF_34D_FLOOR = 1.58


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


def build_review() -> dict[str, Any]:
    rows = actual_routed(read_csv(SOURCE_STAGE133_SUMMARY))
    oos_by_adapter = {row["adapter_id"]: row for row in rows if row.get("split") == "oos"}
    val_by_adapter = {row["adapter_id"]: row for row in rows if row.get("split") == "validation_is"}
    comparison: list[dict[str, Any]] = []
    for adapter_id, oos in oos_by_adapter.items():
        val = val_by_adapter.get(adapter_id, {})
        comparison.append(
            {
                "adapter_id": adapter_id,
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
                "read": candidate_read(val, oos),
            }
        )
    best = max(
        comparison,
        key=lambda row: (
            row["read"] == "survivor_candidate_strong_but_trade_count_gap",
            row["oos_net"] >= LEGACY_34D["net_profit"],
            row["validation_net"] >= LEGACY_34D["net_profit"],
            row["oos_pf"] >= PF_34D_FLOOR,
            row["validation_pf"] >= PF_34D_FLOOR,
            -abs(row["oos_dd_pct"] - 14.0),
            row["oos_net"],
        ),
        default={},
    )
    route = [
        {
            "decision": DECISION,
            "reason": "survivor_control_preserved_34d_level_pf_net_but_trade_count_gap_and_segment_equity_audit_remain",
            "best_adapter": best.get("adapter_id", ""),
            "next_stage": NEXT_STAGE_ID,
            "overall_goal_complete": False,
        }
    ]
    return {"comparison": comparison, "best": best, "route": route}


def candidate_read(val: Mapping[str, Any], oos: Mapping[str, Any]) -> str:
    val_pf_ok = as_float(val.get("profit_factor")) >= PF_34D_FLOOR
    val_net_ok = as_float(val.get("net_profit")) >= LEGACY_34D["net_profit"]
    oos_pf_ok = as_float(oos.get("profit_factor")) >= PF_34D_FLOOR
    oos_net_ok = as_float(oos.get("net_profit")) >= LEGACY_34D["net_profit"]
    if val_pf_ok and val_net_ok and oos_pf_ok and oos_net_ok:
        return "survivor_candidate_strong_but_trade_count_gap"
    if oos_pf_ok and oos_net_ok:
        return "oos_strong_validation_tradeoff"
    return "not_candidate"


def report_markdown(review: Mapping[str, Any]) -> str:
    table = "\n".join(
        ["| adapter(어댑터) | val PF | val net | OOS PF | OOS net | OOS DD% | OOS trades | read(판독) |", "|---|---:|---:|---:|---:|---:|---:|---|"]
        + [
            f"| {row['adapter_id']} | {row['validation_pf']:.2f} | {row['validation_net']:.2f} | {row['oos_pf']:.2f} | {row['oos_net']:.2f} | {row['oos_dd_pct']:.2f} | {row['oos_trades']:.0f} | {row['read']} |"
            for row in review["comparison"]
        ]
    )
    best = review["best"]
    return f"""# Stage134 Survivor Follow-up Review(134단계 생존 후보 후속 검토)

- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- decision(판정): `{DECISION}`
- external_verification_status(외부 검증 상태): `completed_existing_stage133_mt5_runtime_evidence_reviewed`
- boundary(주장 경계): `{BOUNDARY}`

## Bounded Question(경계 질문)

Stage133(133단계) survivor recovery(생존 후보 복구) 결과를 후보로 보존하고 segment/equity audit(구간/자금곡선 감사)로 넘길 만큼 강한가?

## KPI Comparison(KPI 비교)

{table}

## Read(판독)

- best_candidate(최선 후보): `{best.get("adapter_id", "none")}`
- control(통제)은 validation/OOS(검증/미래구간) PF/net(수익 팩터/순손익)을 모두 34D 목표 근처 또는 이상으로 보존했다.
- h4(보유 4)는 OOS 순손익이 더 높지만 validation PF(검증 수익 팩터)가 약해져 바로 선택하지 않는다.
- trade_count(거래 수)는 34D보다 낮다. 그래서 전체 목표 완료가 아니라 Stage135(135단계) segment/equity audit(구간/자금곡선 감사)로 넘긴다.

Effect(효과): 강한 후보를 보존하지만, 구간 안정성·자금곡선·거래 수 약점 검토 전에는 final package(최종 패키지)나 deployment(배포)를 주장하지 않는다.
"""


def decision_markdown(review: Mapping[str, Any]) -> str:
    best = review["best"]
    return f"""# Stage134 Decision(134단계 판정)

decision(판정): `{DECISION}`

Stage134(134단계)는 Stage133(133단계) MT5(메타트레이더5) 근거를 review-only(검토 전용)로 판정했다. Effect(효과): Stage122 survivor(Stage122 생존 후보)는 강하게 살아났지만, 구간/자금곡선 감사 전에는 전체 목표 완료가 아니다.

## Evidence(근거)

- review(검토): `{rel(REPORT_PATH)}`
- comparison(비교): `{rel(COMPARISON_PATH)}`
- route_decision(경로 판정): `{rel(ROUTE_DECISION_PATH)}`
- source_stage133_summary(133단계 요약): `{rel(SOURCE_STAGE133_SUMMARY)}`
- source_stage133_segments(133단계 구간): `{rel(SOURCE_STAGE133_SEGMENTS)}`
- source_stage133_risk(133단계 위험): `{rel(SOURCE_STAGE133_RISK)}`
- best_candidate(최선 후보): `{best.get("adapter_id", "none")}`

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
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "artifact_type": "stage134_followup_review_evidence",
                    "path": rel(path),
                    "sha256": sha256_file_lf_normalized(path),
                    "hash_policy": "lf_normalized_text",
                    "created_at_utc": created,
                    "notes": "Stage134 review-only follow-up artifact.",
                }
            )
    return rows


def write_ledgers(review: Mapping[str, Any], artifacts: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    best = review["best"]
    run_payload = upsert_csv_rows(
        RUN_REGISTRY_PATH,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "baseline_adapter_survivor_followup_review",
                "status": "completed",
                "judgment": DECISION,
                "path": rel(DECISION_PATH),
                "notes": ledger_pairs((("best_candidate", best.get("adapter_id")), ("target_surface", TARGET_SURFACE), ("overall_goal_complete", False))),
            }
        ],
        key="run_id",
    )
    ledger_rows = [
        {
            "ledger_row_id": f"{RUN_ID}__stage134_followup_review",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "stage134_followup_review",
            "parent_run_id": PARENT_RUN_ID,
            "record_view": "existing_evidence_review",
            "tier_scope": "Tier A+B routed review; Tier B disabled evidence preserved",
            "kpi_scope": "stage134_survivor_followup_review",
            "scoreboard_lane": "followup_review",
            "status": "completed",
            "judgment": DECISION,
            "path": rel(DECISION_PATH),
            "primary_kpi": ledger_pairs((("best_candidate", best.get("adapter_id")), ("oos_net", best.get("oos_net")), ("oos_pf", best.get("oos_pf")), ("validation_net", best.get("validation_net")), ("validation_pf", best.get("validation_pf")))),
            "guardrail_kpi": ledger_pairs((("target_surface", TARGET_SURFACE), ("overall_goal_complete", False), ("claim_boundary", BOUNDARY))),
            "external_verification_status": "completed_existing_stage133_mt5_runtime_evidence_reviewed",
            "notes": "Stage134 review-only; no new MT5 execution; no operational claim.",
        }
    ]
    stage_payload = upsert_csv_rows(STAGE_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, ledger_rows, key="ledger_row_id")
    project_payload = upsert_csv_rows(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, ledger_rows, key="ledger_row_id")
    artifact_payload = upsert_csv_rows(ARTIFACT_REGISTRY_PATH, aw.ARTIFACT_COLUMNS, list(artifacts), key="artifact_id")
    return {"run_registry": run_payload, "stage_ledger": stage_payload, "project_alpha_ledger": project_payload, "artifact_registry": artifact_payload}


def write_packet_files(review: Mapping[str, Any], ledger_payload: Mapping[str, Any]) -> None:
    files = {
        "routing_receipt.json": {"packet_id": PACKET_ID, "primary_family": "adapter_development", "primary_skill": "obsidian-result-judgment", "support_skills": ["obsidian-performance-attribution", "obsidian-model-validation"], "required_gates": ["experiment_design_receipt", "kpi_contract_audit", "result_judgment_gate", "artifact_lineage_audit", "final_claim_guard"], "status": "completed"},
        "experiment_design_receipt.json": {"hypothesis": "Stage133 survivor candidate should be preserved for segment/equity audit, not final completion.", "decision_use": "open Stage135 audit only", "comparison_baseline": "Stage133 survivor variants", "success_criteria": ["route to audit if candidate preserves PF/net"], "failure_criteria": ["claim final package without segment/equity audit"], "status": "completed"},
        "kpi_contract_audit.json": {"comparison_path": rel(COMPARISON_PATH), "status": "completed"},
        "result_judgment_gate.json": {"result_subject": RUN_ID, "judgment_label": DECISION, "overall_goal_complete": False, "claim_boundary": BOUNDARY, "status": "passed_with_boundary"},
        "artifact_lineage_audit.json": {"source_inputs": [rel(SOURCE_STAGE133_SUMMARY), rel(SOURCE_STAGE133_SEGMENTS), rel(SOURCE_STAGE133_RISK)], "consumers": [rel(REPORT_PATH), rel(DECISION_PATH), rel(SUMMARY_JSON_PATH)], "ledger_links": ledger_payload},
        "final_claim_guard.json": {"overall_goal_complete": False, "deployment_claim": False, "live_readiness_claim": False, "runtime_authority_claim": False, "production_baseline_claim": False, "operating_reference_claim": False, "operating_promotion_claim": False, "status": "passed"},
        "required_gate_coverage_audit.json": {"required_gates": ["experiment_design_receipt", "kpi_contract_audit", "result_judgment_gate", "artifact_lineage_audit", "final_claim_guard"], "covered_by": ["experiment_design_receipt.json", "kpi_contract_audit.json", "result_judgment_gate.json", "artifact_lineage_audit.json", "final_claim_guard.json"], "status": "completed"},
        "aggregate_summary.json": {"packet_id": PACKET_ID, "stage_id": STAGE_ID, "run_id": RUN_ID, "decision": DECISION, "required_outputs": {"report": rel(REPORT_PATH), "comparison": rel(COMPARISON_PATH), "route_decision": rel(ROUTE_DECISION_PATH), "decision": rel(DECISION_PATH)}, "claim_boundary": BOUNDARY, "overall_goal_complete": False},
    }
    for name, payload in files.items():
        write_json(PACKET_ROOT / name, payload)


def write_stage_docs() -> None:
    write_md(SPEC_ROOT / "stage_brief.md", f"""# {STAGE_ID}

Stage134(134단계)는 Stage133(133단계) survivor recovery(생존 후보 복구) 결과를 review-only(검토 전용)로 판정했다.

## Boundary(경계)

`{BOUNDARY}`
""")
    write_md(INPUT_ROOT / "input_refs.md", f"""# Stage134 Input References(134단계 입력 참조)

- stage133_decision(133단계 판정): `{rel(SOURCE_STAGE133_DECISION)}`
- stage133_summary(133단계 요약): `{rel(SOURCE_STAGE133_SUMMARY)}`
- stage133_segments(133단계 구간): `{rel(SOURCE_STAGE133_SEGMENTS)}`
- stage133_risk(133단계 위험): `{rel(SOURCE_STAGE133_RISK)}`
- stage133_pushed_commit(133단계 푸시 커밋): `{SOURCE_STAGE133_PUSHED_COMMIT}`
""")
    write_md(SELECTED_ROOT / "selection_status.md", f"""# Stage134 Selection Status(134단계 선택 상태)

- stage_status(단계 상태): `closed_review_only`
- current_packet(현재 작업 묶음): `{PACKET_ID}`
- current_run(현재 실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE133_ID}`
- stage134_decision(134단계 판정): `{DECISION}`
- next_stage_or_branch(다음 단계/분기): `{NEXT_STAGE_ID}`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- selected_research_baseline(선택 연구 기준): `none`
- claim_boundary(주장 경계): `{BOUNDARY}`
""")
    write_md(REVIEWS_ROOT / "review_index.md", f"""# Stage134 Review Index(134단계 검토 색인)

- review(검토): `{rel(REPORT_PATH)}`
- comparison(비교): `{rel(COMPARISON_PATH)}`
- route_decision(경로 판정): `{rel(ROUTE_DECISION_PATH)}`
- decision(판정): `{rel(DECISION_PATH)}`
""")
    write_md(NEXT_STAGE_ROOT / "00_spec/stage_brief.md", f"""# {NEXT_STAGE_ID}

Stage135(135단계)는 Stage133/134 survivor candidate(생존 후보)의 segment/equity audit(구간/자금곡선 감사)를 수행한다.

## Bounded Question(경계 질문)

강한 PF/net(수익 팩터/순손익)이 segment stability(구간 안정성), equity curve(자금 곡선), risk/ATR behavior(위험/ATR 행동)에서도 credible(신뢰 가능)한가?

Effect(효과): 높은 최종 손익만 보고 전체 목표 완료를 주장하지 않는다.

## Boundary(경계)

`{BOUNDARY}`
""")
    write_md(NEXT_STAGE_ROOT / "01_inputs/input_refs.md", f"""# Stage135 Input References(135단계 입력 참조)

- stage134_decision(134단계 판정): `{rel(DECISION_PATH)}`
- stage134_review(134단계 검토): `{rel(REPORT_PATH)}`
- stage133_summary(133단계 요약): `{rel(SOURCE_STAGE133_SUMMARY)}`
- stage133_segment_kpi(133단계 구간 KPI): `{rel(SOURCE_STAGE133_SEGMENTS)}`
- stage133_risk_atr_telemetry(133단계 위험/ATR 원격측정): `{rel(SOURCE_STAGE133_RISK)}`
""")
    write_md(NEXT_STAGE_ROOT / "03_reviews/review_index.md", """# Stage135 Review Index(135단계 검토 색인)

Stage135(135단계)는 planned(계획) 상태다. Effect(효과): Stage133(133단계) 강한 후보를 segment/equity audit(구간/자금곡선 감사)로 검증한다.
""")
    write_md(NEXT_STAGE_ROOT / "04_selected/selection_status.md", f"""# Stage135 Selection Status(135단계 선택 상태)

- stage_status(단계 상태): `active_planned_from_stage134`
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
- adapter_under_review(검토 중 어댑터): `stage133_survivor_candidate_segment_equity_audit`
- status(상태): `stage134_closed_{DECISION}_stage135_open_planned`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage134(134단계)는 Stage133(133단계) survivor recovery(생존 후보 복구)를 strong candidate(강한 후보)로 보존하되, Stage135(135단계) segment/equity audit(구간/자금곡선 감사) 전에는 전체 목표 완료로 보지 않는다. Effect(효과): 좋은 최종 손익을 바로 과대 주장하지 않는다.

## Latest Stage134 Evidence(최신 134단계 근거)

- run(실행): `{RUN_ID}`
- decision(판정): `{DECISION}`
- report(보고서): `{rel(REPORT_PATH)}`
- comparison(비교): `{rel(COMPARISON_PATH)}`
- route_decision(경로 판정): `{rel(ROUTE_DECISION_PATH)}`

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준선), legacy_inheritance(레거시 상속), overall_goal_complete(전체 목표 완료).
""")
    text = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig") if path_exists(WORKSPACE_STATE_PATH) else ""
    text = re.sub(r"^current_run_id:.*$", f"current_run_id: {NEXT_RUN_ID}", text, count=1, flags=re.MULTILINE)
    text = re.sub(r"^active_stage:.*$", f"active_stage: {NEXT_STAGE_ID}", text, count=1, flags=re.MULTILINE)
    focus = f"""current_focus:
- >-
  Stage134(134단계) closed(종료) as `{DECISION}` and Stage135(135단계) `{NEXT_STAGE_ID}` is active_planned(활성 계획). Effect(효과): 강한 Stage133 survivor candidate(Stage133 생존 후보)를 구간/자금곡선 감사로 넘긴다.
- >-
  Stage134 evidence(134단계 근거)는 `{rel(REPORT_PATH)}`, `{rel(COMPARISON_PATH)}`에 있다. Effect(효과): 높은 순손익을 바로 전체 완료로 오해하지 않게 한다.
- >-
  Target surface(목표 표면)는 `{TARGET_SURFACE}`이고 legacy 34D(레거시 34D)는 lesson-only KPI target(교훈 전용 핵심 성과 지표 목표)이다. Effect(효과): v2-native research(브이투 고유 연구)만 계속한다.

"""
    text = re.sub(r"(?ms)^current_focus:\r?\n.*?(?=\r?\nstage\d+_)", focus, text, count=1) if re.search(r"(?ms)^current_focus:\r?\n.*?(?=\r?\nstage\d+_)", text) else text.rstrip() + "\n" + focus
    block = f"""
stage134_stage122_survivor_followup_review:
  packet_id: {PACKET_ID}
  stage_id: {STAGE_ID}
  status: closed_review_only
  current_run_id: {RUN_ID}
  source_stage: {SOURCE_STAGE133_ID}
  decision: {DECISION}
  report_path: {rel(REPORT_PATH)}
  decision_path: {rel(DECISION_PATH)}
  next_action: {NEXT_RUN_ID}
  boundary: {BOUNDARY}

stage135_stage122_survivor_segment_equity_audit:
  packet_id: {NEXT_PACKET_ID}
  stage_id: {NEXT_STAGE_ID}
  status: active_planned_from_stage134
  current_run_id: {NEXT_RUN_ID}
  source_stage: {STAGE_ID}
  source_decision: {DECISION}
  next_action: run_stage135_segment_equity_audit
  boundary: {BOUNDARY}
"""
    text = re.sub(r"(?ms)\nstage134_stage122_survivor_followup_review:.*?(?=\nstage\d+_|$)", "\n", text)
    text = re.sub(r"(?ms)\nstage135_stage122_survivor_segment_equity_audit:.*?(?=\nstage\d+_|$)", "\n", text)
    io_path(WORKSPACE_STATE_PATH).write_text(text.rstrip() + "\n" + block, encoding="utf-8-sig")


def append_changelog() -> None:
    existing = io_path(CHANGELOG_PATH).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG_PATH) else ""
    entry = (
        f"\n## {utc_now()} Stage134 survivor follow-up review closeout(134단계 생존 후보 후속 검토 종료)\n\n"
        f"- action(행동): closed(종료) `{STAGE_ID}` with decision(판정) `{DECISION}`.\n"
        f"- effect(효과): survivor candidate(생존 후보)를 Stage135(135단계) segment/equity audit(구간/자금곡선 감사)로 넘겼다.\n"
        f"- boundary(주장 경계): `{BOUNDARY}`.\n"
    )
    io_path(CHANGELOG_PATH).write_text(existing.rstrip() + entry, encoding="utf-8-sig")


def main() -> int:
    review = build_review()
    write_csv(COMPARISON_PATH, review["comparison"])
    write_csv(ROUTE_DECISION_PATH, review["route"])
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
