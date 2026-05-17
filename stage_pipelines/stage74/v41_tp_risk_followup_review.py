from __future__ import annotations

import csv
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Mapping

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


STAGE_ID = "74_adapter_research__v41_tp_risk_followup_review"
RUN_ID = "run74A_stage74_v41_tp_risk_followup_review_v1"
PACKET_ID = "stage74_v41_tp_risk_followup_review_v1"
SOURCE_STAGE_ID = "73_adapter_research__v41_gate_repair_followup"
SOURCE_RUN_ID = "run73A_stage73_v41_gate_repair_followup_v1"
SOURCE_STAGE73_CLOSEOUT_COMMIT = "30bc138764da2c04c1552f0f9e12830f95eef250"
SOURCE_STAGE73_LATEST_COMMIT = "76db6f199ff917da2f8311544f68dc6f24612e0e"
NEXT_STAGE_ID = "75_adapter_research__v41_dd_balance_repair"
NEXT_RUN_ID = "run75A_stage75_v41_dd_balance_repair_v1"
NEXT_PACKET_ID = "stage75_v41_dd_balance_repair_v1"
TARGET_SURFACE = "legacy_34d_kpi_lesson_only_no_legacy_inheritance"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment"
)

STAGE_ROOT = Path("stages") / STAGE_ID
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
SELECTED_ROOT = STAGE_ROOT / "04_selected"
PACKET_ROOT = Path("docs/agent_control/packets") / PACKET_ID
NEXT_STAGE_ROOT = Path("stages") / NEXT_STAGE_ID

SOURCE_SUMMARY = Path("stages/73_adapter_research__v41_gate_repair_followup/03_reviews/stage73_v41_tp_risk_summary.csv")
SOURCE_REPORT = Path("stages/73_adapter_research__v41_gate_repair_followup/03_reviews/stage73_v41_tp_risk_report.md")
SOURCE_DECISION = Path("stages/73_adapter_research__v41_gate_repair_followup/03_reviews/stage73_decision.md")
SOURCE_RISK_ATR = Path("stages/73_adapter_research__v41_gate_repair_followup/03_reviews/stage73_risk_atr_telemetry.csv")

REVIEW_REPORT = REVIEWS_ROOT / "stage74_tp_risk_followup_review.md"
COMPARISON_CSV = REVIEWS_ROOT / "stage74_candidate_comparison.csv"
DECISION_PATH = REVIEWS_ROOT / "stage74_decision.md"
STAGE_LEDGER_PATH = REVIEWS_ROOT / "stage_run_ledger.csv"
RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
PROJECT_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
ARTIFACT_REGISTRY_PATH = Path("docs/registers/artifact_registry.csv")
WORKSPACE_STATE_PATH = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE_PATH = Path("docs/context/current_working_state.md")
CHANGELOG_PATH = Path("docs/workspace/changelog.md")


def rel(path: Path) -> str:
    return path.as_posix()


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        if value in (None, ""):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def write_md(path: Path, text: str) -> None:
    io_path(path).parent.mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def write_json(path: Path, payload: Mapping[str, Any]) -> None:
    io_path(path).parent.mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]]) -> None:
    rows = list(rows)
    io_path(path).parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        io_path(path).write_text("", encoding="utf-8")
        return
    columns = list(rows[0].keys())
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)


def source_rows() -> list[dict[str, str]]:
    with io_path(SOURCE_SUMMARY).open(encoding="utf-8-sig", newline="") as handle:
        return [row for row in csv.DictReader(handle) if row.get("view") == "actual_routed_total"]


def paired_metrics(rows: list[Mapping[str, str]]) -> list[dict[str, Any]]:
    by_adapter: dict[str, dict[str, Mapping[str, str]]] = {}
    for row in rows:
        by_adapter.setdefault(str(row.get("adapter_id")), {})[str(row.get("split"))] = row
    out: list[dict[str, Any]] = []
    for adapter_id, splits in sorted(by_adapter.items()):
        val = splits.get("validation_is", {})
        oos = splits.get("oos", {})
        val_net = as_float(val.get("net_profit"))
        oos_net = as_float(oos.get("net_profit"))
        val_pf = as_float(val.get("profit_factor"))
        oos_pf = as_float(oos.get("profit_factor"))
        val_dd = as_float(val.get("max_drawdown_percent"))
        oos_dd = as_float(oos.get("max_drawdown_percent"))
        out.append(
            {
                "adapter_id": adapter_id,
                "validation_pf": val_pf,
                "validation_net": val_net,
                "validation_dd_pct": val_dd,
                "validation_expectancy": as_float(val.get("expectancy")),
                "oos_pf": oos_pf,
                "oos_net": oos_net,
                "oos_dd_pct": oos_dd,
                "oos_expectancy": as_float(oos.get("expectancy")),
                "balanced_score": round((val_pf + oos_pf) * 100.0 + (val_net + oos_net) / 20.0 - (val_dd + oos_dd), 4),
                "stage74_read": "needs_dd_net_balance_repair",
            }
        )
    return out


def decision_for(rows: list[Mapping[str, Any]]) -> str:
    for row in rows:
        if (
            row["validation_net"] >= 900
            and row["oos_net"] >= 520
            and row["validation_dd_pct"] <= 20.0
            and row["oos_dd_pct"] <= 20.0
            and row["validation_pf"] >= 1.50
            and row["oos_pf"] >= 1.35
        ):
            return "proceed_to_stage75_candidate_package_review"
    return "continue_v41_dd_balance_repair_in_stage75"


def report_markdown(rows: list[Mapping[str, Any]], decision: str) -> str:
    table = "\n".join(
        "| {adapter_id} | {validation_pf:.2f} | {validation_net:.2f} | {validation_dd_pct:.2f} | {oos_pf:.2f} | {oos_net:.2f} | {oos_dd_pct:.2f} | {balanced_score:.2f} |".format(**row)
        for row in rows
    )
    best_score = max(rows, key=lambda row: row["balanced_score"])
    best_oos = max(rows, key=lambda row: row["oos_net"])
    best_val = max(rows, key=lambda row: row["validation_net"])
    lowest_val_dd = min(rows, key=lambda row: row["validation_dd_pct"])
    return f"""# Stage74 TP/Risk Follow-up Review(74단계 TP/위험 후속 검토)

- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- source_stage73_closeout_commit(원천 73단계 종료 커밋): `{SOURCE_STAGE73_CLOSEOUT_COMMIT}`
- source_stage73_latest_commit(원천 73단계 최신 커밋): `{SOURCE_STAGE73_LATEST_COMMIT}`
- source_summary(원천 요약): `{rel(SOURCE_SUMMARY)}`
- external_verification_status(외부 검증 상태): `completed_existing_stage73_evidence_reviewed`
- decision(판정): `{decision}`
- boundary(경계): `{BOUNDARY}`

## KPI Table(KPI 핵심 성과 지표 표)

| adapter(어댑터) | val PF(검증 수익 팩터) | val net(검증 순손익) | val DD%(검증 손실률) | OOS PF(표본외 수익 팩터) | OOS net(표본외 순손익) | OOS DD%(표본외 손실률) | balance score(균형 점수) |
|---|---:|---:|---:|---:|---:|---:|---:|
{table}

## Read(판독)

- best_balanced_score(최고 균형 점수): `{best_score["adapter_id"]}`
- best_validation_net(최고 검증 순손익): `{best_val["adapter_id"]}`
- best_oos_net(최고 표본외 순손익): `{best_oos["adapter_id"]}`
- lowest_validation_dd(최저 검증 손실률): `{lowest_val_dd["adapter_id"]}`

Stage73(73단계)는 Stage72(72단계)보다 회복됐지만, validation DD(검증 손실률)가 아직 높고 net/DD balance(순손익/손실률 균형)가 34D target surface(34D 목표 표면)에 닿지 않았다. Effect(효과): Stage75(75단계)는 새 모델 탐색이 아니라 v41(브이41)의 DD/net balance(손실률/순손익 균형)만 좁게 수리한다.

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), legacy inheritance(레거시 상속).
"""


def decision_markdown(decision: str) -> str:
    return f"""# Stage74 Decision(74단계 판정)

decision(판정): `{decision}`

Stage74(74단계)는 Stage73(73단계)의 TP/risk(익절 폭/위험) 결과를 review gate(검토 게이트)로 판독했다.

Effect(효과): Stage75(75단계)는 `risk4.5~5.0`, `TP3.5~4.0`, 그리고 validation DD(검증 손실률) 완화를 좁게 재측정한다.

## Evidence(근거)

- review_report(검토 보고서): `{rel(REVIEW_REPORT)}`
- comparison_csv(비교 CSV): `{rel(COMPARISON_CSV)}`
- source_summary(원천 요약): `{rel(SOURCE_SUMMARY)}`
- source_report(원천 보고서): `{rel(SOURCE_REPORT)}`
- source_risk_atr(원천 위험/ATR): `{rel(SOURCE_RISK_ATR)}`
- external_verification_status(외부 검증 상태): `completed_existing_stage73_evidence_reviewed`

## Next(다음)

next_stage_or_branch(다음 단계/분기): `{NEXT_STAGE_ID}`

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), legacy inheritance(레거시 상속).
"""


def artifact_rows() -> list[dict[str, Any]]:
    created = utc_now()
    paths = [REVIEW_REPORT, COMPARISON_CSV, DECISION_PATH, STAGE_LEDGER_PATH]
    rows = []
    for path in paths:
        if path_exists(path):
            rows.append(
                {
                    "artifact_id": f"{RUN_ID}__{path.name}",
                    "artifact_type": "stage74_tp_risk_followup_review_evidence",
                    "path": rel(path),
                    "sha256": sha256_file_lf_normalized(path),
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "created_at_utc": created,
                    "notes": "Stage74 review gate artifact from existing Stage73 MT5 evidence.",
                }
            )
    return rows


def write_ledgers(decision: str, artifacts: list[Mapping[str, Any]]) -> Mapping[str, Any]:
    run_payload = upsert_csv_rows(
        RUN_REGISTRY_PATH,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "baseline_adapter_v2_native_v41_tp_risk_review_gate",
                "status": "completed",
                "judgment": decision,
                "path": rel(DECISION_PATH),
                "notes": ledger_pairs(
                    (
                        ("source_run", SOURCE_RUN_ID),
                        ("source_stage73_latest_commit", SOURCE_STAGE73_LATEST_COMMIT),
                        ("target_surface", TARGET_SURFACE),
                        ("legacy_relation", "lesson_only"),
                    )
                ),
            }
        ],
        key="run_id",
    )
    alpha_row = {
        "ledger_row_id": f"{RUN_ID}__stage74_review_gate",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": "stage74_review_gate",
        "parent_run_id": SOURCE_RUN_ID,
        "record_view": "review_gate",
        "tier_scope": "Tier A+B",
        "kpi_scope": "stage73_tp_risk_followup_review",
        "scoreboard_lane": "research_review",
        "status": "completed",
        "judgment": decision,
        "path": rel(DECISION_PATH),
        "primary_kpi": "stage73_best_validation_pf=1.50;stage73_best_oos_pf=1.47",
        "guardrail_kpi": "stage73_validation_dd_still_high;target_surface=legacy_34d_lesson_only",
        "external_verification_status": "completed_existing_stage73_evidence_reviewed",
        "notes": "Review gate only; no new MT5 tester run in Stage74.",
    }
    alpha_payload = upsert_csv_rows(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, [alpha_row], key="ledger_row_id")
    stage_payload = upsert_csv_rows(STAGE_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, [alpha_row], key="ledger_row_id")
    artifact_payload = upsert_csv_rows(
        ARTIFACT_REGISTRY_PATH,
        ("artifact_id", "artifact_type", "path", "sha256", "stage_id", "run_id", "created_at_utc", "notes"),
        list(artifacts),
        key="artifact_id",
    )
    return {"run_registry": run_payload, "alpha_ledger": alpha_payload, "stage_ledger": stage_payload, "artifact_registry": artifact_payload}


def write_packet(decision: str, ledger_payload: Mapping[str, Any]) -> None:
    write_json(PACKET_ROOT / "routing_receipt.json", {"packet_id": PACKET_ID, "stage_id": STAGE_ID, "primary_family": "performance_attribution", "primary_skill": "obsidian-performance-attribution", "support_skills": ["obsidian-result-judgment", "obsidian-experiment-design"], "required_gates": ["kpi_contract_audit", "result_judgment_gate"], "status": "completed"})
    write_json(PACKET_ROOT / "result_judgment_gate.json", {"packet_id": PACKET_ID, "run_id": RUN_ID, "decision": decision, "claim_boundary": BOUNDARY, "overall_goal_complete": False})
    write_json(PACKET_ROOT / "aggregate_summary.json", {"packet_id": PACKET_ID, "stage_id": STAGE_ID, "run_id": RUN_ID, "decision": decision, "source_stage73_latest_commit": SOURCE_STAGE73_LATEST_COMMIT, "ledger_payload": ledger_payload, "overall_goal_complete": False})


def update_current_truth(decision: str) -> None:
    text = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    text = re.sub(r"^current_run_id: .*$", f"current_run_id: {NEXT_RUN_ID}", text, count=1, flags=re.MULTILINE)
    text = re.sub(r"^updated_on: .*$", "updated_on: '2026-05-17'", text, count=1, flags=re.MULTILINE)
    text = re.sub(r"^active_stage: .*$", f"active_stage: {NEXT_STAGE_ID}", text, count=1, flags=re.MULTILINE)
    current_focus = f"""current_focus:
- >-
  Stage74(74단계) closed(종료) as `{decision}` and Stage75(75단계) `{NEXT_STAGE_ID}` is open_planned(열림 계획). Effect(효과): Stage73(73단계) KPI(핵심 성과 지표)를 검토해 DD/net balance(손실률/순손익 균형) 수리 질문으로 넘긴다.
- >-
  Stage74 result(74단계 결과): Stage73(73단계)는 Stage72(72단계)보다 회복됐지만 validation DD(검증 손실률)와 34D gap(34D 격차)이 남았다. Effect(효과): Stage75(75단계)는 새 모델 탐색이 아니라 v41(브이41) TP/risk(익절 폭/위험) 주변만 좁게 재측정한다.
- >-
  Target surface(목표 표면)는 `{TARGET_SURFACE}`이고 legacy 34D(레거시 34D)는 lesson-only KPI target(교훈 전용 핵심 성과 지표 목표)이다. Effect(효과): 목표는 높게 유지하지만 v2-native research(v2 고유 연구)만 계속한다.
"""
    text = re.sub(r"current_focus:\n(?:- >-\n(?:  .*\n)+)+", current_focus, text, count=1, flags=re.MULTILINE)
    block = f"""

stage74_tp_risk_followup_review:
  packet_id: {PACKET_ID}
  stage_id: {STAGE_ID}
  status: closed_{decision}
  current_run_id: {RUN_ID}
  source_run_id: {SOURCE_RUN_ID}
  source_stage73_latest_commit: {SOURCE_STAGE73_LATEST_COMMIT}
  target_surface: {TARGET_SURFACE}
  decision: {decision}
  next_stage_or_branch: {NEXT_STAGE_ID}
  report_path: {rel(DECISION_PATH)}
  packet_summary_path: {rel(PACKET_ROOT / "aggregate_summary.json")}
  external_verification_status: completed_existing_stage73_evidence_reviewed
  boundary: {BOUNDARY}
"""
    text = text.rstrip() + block
    io_path(WORKSPACE_STATE_PATH).write_text(text + "\n", encoding="utf-8-sig")
    write_md(CURRENT_WORKING_STATE_PATH, f"""# Current Working State(현재 작업 상태)

- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- active_stage(활성 단계): `{NEXT_STAGE_ID}`
- selected_research_baseline(선택 연구 기준): `research_package_only_reference_surface`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- adapter_under_review(검토 중 어댑터): `stage73_v41_tp_risk_followup_surface`
- status(상태): `stage74_closed_{decision}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Stage74(74단계) closed(종료) as v2-native TP/risk review gate(v2 고유 익절 폭/위험 검토 게이트). Effect(효과): Stage75(75단계)는 34D KPI(34D 핵심 성과 지표) 격차 중 DD/net balance(손실률/순손익 균형)만 좁게 수리한다.

## Latest Stage74 Evidence(최신 74단계 근거)

- run(실행): `{RUN_ID}`
- decision(판정): `{decision}`
- source_stage73_latest_commit(원천 73단계 최신 커밋): `{SOURCE_STAGE73_LATEST_COMMIT}`
- external_verification_status(외부 검증 상태): `completed_existing_stage73_evidence_reviewed`
- report(보고서): `{rel(REVIEW_REPORT)}`
- stage74_decision(74단계 판정): `{rel(DECISION_PATH)}`

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준선), legacy_inheritance(레거시 상속).
""")


def write_stage_status(decision: str) -> None:
    write_md(SELECTED_ROOT / "selection_status.md", f"""# Stage74 Selection Status(74단계 선택 상태)

- stage_status(단계 상태): `closed_{decision}`
- current_packet(현재 작업 묶음): `{PACKET_ID}`
- current_run(현재 실행): `{RUN_ID}`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- source_stage73_latest_commit(원천 73단계 최신 커밋): `{SOURCE_STAGE73_LATEST_COMMIT}`
- stage74_decision(74단계 판정): `{decision}`
- next_stage_or_branch(다음 단계/분기): `{NEXT_STAGE_ID}`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Effect(효과): Stage74(74단계)는 새 MT5 실행 없이 Stage73 근거를 판독하고, Stage75(75단계)의 좁은 DD/net balance(손실률/순손익 균형) 수리로 넘긴다.
""")
    write_md(NEXT_STAGE_ROOT / "00_spec" / "stage_brief.md", f"""# {NEXT_STAGE_ID}

Stage75(75단계)는 Stage74(74단계)의 review gate(검토 게이트)를 받아 v41 TP/risk(V41 익절 폭/위험)의 DD/net balance(손실률/순손익 균형)를 좁게 수리하는 단계다.

## Bounded Question(경계 질문)

Stage73(73단계)에서 보인 `risk5_tp35`, `risk45_tp40`, `risk5_tp40` 사이에서 validation DD(검증 손실률)를 낮추면서 validation/OOS net(검증/표본외 순손익)을 유지할 수 있는가?

Effect(효과): Stage75(75단계)는 새 모델 원천을 찾지 않고, v41(브이41) risk cap(위험 상한), TP(익절 폭), DD guard(손실률 보호) 주변만 측정한다.

## Boundary(경계)

`{BOUNDARY}`
""")
    write_md(NEXT_STAGE_ROOT / "01_inputs" / "input_refs.md", f"""# Stage75 Input References(75단계 입력 참조)

- source_stage(원천 단계): `{STAGE_ID}`
- source_run(원천 실행): `{RUN_ID}`
- source_decision(원천 판정): `{decision}`
- source_stage73_latest_commit(원천 73단계 최신 커밋): `{SOURCE_STAGE73_LATEST_COMMIT}`
- stage74_report(74단계 보고서): `{rel(REVIEW_REPORT)}`
- stage74_decision(74단계 판정): `{rel(DECISION_PATH)}`
- stage73_summary(73단계 요약): `{rel(SOURCE_SUMMARY)}`
- target_surface(목표 표면): `{TARGET_SURFACE}`

Effect(효과): Stage75(75단계)는 Stage73/74 근거만 이어받아 34D KPI(34D 핵심 성과 지표) 격차 축소를 계속한다.
""")
    write_md(NEXT_STAGE_ROOT / "03_reviews" / "review_index.md", f"""# Stage75 Review Index(75단계 검토 색인)

- status(상태): `open_planned`
- source_decision(원천 판정): `{decision}`
- planned_packet(계획 작업 묶음): `{NEXT_PACKET_ID}`
- planned_run(계획 실행): `{NEXT_RUN_ID}`

Effect(효과): Stage75(75단계)는 DD/net balance(손실률/순손익 균형) 수리 실행만 검토한다.
""")
    write_md(NEXT_STAGE_ROOT / "04_selected" / "selection_status.md", f"""# Stage75 Selection Status(75단계 선택 상태)

- stage_status(단계 상태): `open_planned`
- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- source_stage(원천 단계): `{STAGE_ID}`
- source_decision(원천 판정): `{decision}`
- target_surface(목표 표면): `{TARGET_SURFACE}`
- claim_boundary(주장 경계): `{BOUNDARY}`

Effect(효과): Stage75(75단계)는 34D KPI(34D 핵심 성과 지표) 격차 축소를 계속하지만, 운영 의미 없이 연구개발로만 이어진다.
""")


def append_changelog(decision: str) -> None:
    entry = (
        "\n## 2026-05-17 - Stage74 TP/risk follow-up review closeout(74단계 TP/위험 후속 검토 종료)\n\n"
        f"- run(실행): `{RUN_ID}`\n"
        f"- decision(판정): `{decision}`\n"
        f"- source_stage73_latest_commit(원천 73단계 최신 커밋): `{SOURCE_STAGE73_LATEST_COMMIT}`\n"
        f"- target_surface(목표 표면): `{TARGET_SURFACE}`\n"
        "- effect(효과): Stage73(73단계)의 TP/risk(익절 폭/위험) KPI(핵심 성과 지표)를 검토해 Stage75(75단계) DD/net balance(손실률/순손익 균형) 수리로 넘겼다.\n"
    )
    existing = io_path(CHANGELOG_PATH).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG_PATH) else ""
    if RUN_ID not in existing:
        io_path(CHANGELOG_PATH).write_text(existing.rstrip() + entry, encoding="utf-8-sig")


def main() -> int:
    rows = paired_metrics(source_rows())
    decision = decision_for(rows)
    write_csv(COMPARISON_CSV, rows)
    write_md(REVIEW_REPORT, report_markdown(rows, decision))
    write_md(DECISION_PATH, decision_markdown(decision))
    artifacts = artifact_rows()
    ledger_payload = write_ledgers(decision, artifacts)
    write_packet(decision, ledger_payload)
    write_stage_status(decision)
    update_current_truth(decision)
    append_changelog(decision)
    print(json.dumps(json_ready({"status": "ok", "run_id": RUN_ID, "decision": decision, "review_report": rel(REVIEW_REPORT)}), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
