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
    ledger_pairs,
    path_exists,
    sha256_file_lf_normalized,
    upsert_csv_rows,
)
from stage_pipelines.stage56.independent_event_source_route_branch import ARTIFACT_COLUMNS  # noqa: E402


STAGE59F_ID = "59F_adapter_repair__new_model_branch_from_failure_memory"
STAGE59G_ID = "59G_adapter_repair__bounded_followup_from_stage59f"
STAGE59H_ID = "59H_adapter_repair__bounded_followup_from_stage59g"
STAGE59I_ID = "59I_adapter_repair__bounded_followup_from_stage59h"
NEXT_STAGE_ID = "59J_adapter_repair__new_model_branch_from_stage59i"
RUN_ID = "run59D_stage59i_bounded_followup_from_stage59h_v1"
NEXT_RUN_ID = "run59E_stage59j_new_model_branch_from_stage59i_v1"
PACKET_ID = "stage59i_bounded_followup_from_stage59h_v1"
NEXT_PACKET_ID = "stage59j_new_model_branch_from_stage59i_v1"
PARENT_RUN_ID = "run59C_stage59h_bounded_followup_from_stage59g_v1"
SOURCE_ADAPTER_ID = "s59h_v54_th60_sd10"
SOURCE_STAGE59H_PUSHED_COMMIT = "6a3f23223a431e9a234f5fc2557ece5c517761f1"
DEVELOPMENT_ANCHOR = "v64_v47_ctxgap14_refill_etfw_h2_no_b"
BACKUP_ANCHOR = "v60_v47_et_stable_damage_firewall_h2c0_no_b"
DECISION = "open_new_model_branch"
EXTERNAL_STATUS = "not_applicable"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment"
)

STAGE_ROOT = Path("stages") / STAGE59I_ID
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
SPEC_ROOT = STAGE_ROOT / "00_spec"
INPUT_ROOT = STAGE_ROOT / "01_inputs"
SELECTED_ROOT = STAGE_ROOT / "04_selected"
PACKET_ROOT = Path("docs/agent_control/packets") / PACKET_ID
NEXT_STAGE_ROOT = Path("stages") / NEXT_STAGE_ID

SOURCE59G_ROOT = Path("stages") / STAGE59G_ID
SOURCE59H_ROOT = Path("stages") / STAGE59H_ID
SOURCE59G_SUMMARY = SOURCE59G_ROOT / "03_reviews/bounded_followup_summary.csv"
SOURCE59G_DECISION = SOURCE59G_ROOT / "03_reviews/stage59g_decision.md"
SOURCE59H_SUMMARY = SOURCE59H_ROOT / "03_reviews/bounded_followup_summary.csv"
SOURCE59H_DECISION = SOURCE59H_ROOT / "03_reviews/stage59h_decision.md"
SOURCE59H_SEGMENT = SOURCE59H_ROOT / "03_reviews/bounded_followup_segment_kpi_summary.csv"
SOURCE59H_RISK = SOURCE59H_ROOT / "03_reviews/bounded_followup_risk_atr_telemetry.csv"

REPORT_PATH = REVIEWS_ROOT / "demotion_or_branch_from_stage59h_report.md"
SUMMARY_JSON_PATH = REVIEWS_ROOT / "demotion_or_branch_summary.json"
SUMMARY_CSV_PATH = REVIEWS_ROOT / "demotion_or_branch_summary.csv"
DECISION_PATH = REVIEWS_ROOT / "stage59i_decision.md"
STAGE_LEDGER_PATH = REVIEWS_ROOT / "stage_run_ledger.csv"
RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
PROJECT_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
ARTIFACT_REGISTRY_PATH = Path("docs/registers/artifact_registry.csv")
WORKSPACE_STATE_PATH = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE_PATH = Path("docs/context/current_working_state.md")
CHANGELOG_PATH = Path("docs/workspace/changelog.md")


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    candidate = Path(str(path))
    try:
        return io_path(candidate).resolve().relative_to(io_path(REPO_ROOT).resolve()).as_posix()
    except ValueError:
        return candidate.as_posix()


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text, encoding="utf-8-sig")


def write_json(path: Path, payload: Mapping[str, Any]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    columns = [
        "source_stage",
        "adapter_id",
        "split",
        "profit_factor",
        "net_profit",
        "max_drawdown_amount",
        "cost_stressed_expectancy",
        "trade_count",
        "same_move_reentry_ratio",
        "risk_floor_applied_count",
        "status",
    ]
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: row.get(column, "") for column in columns})


def read_actual_rows(path: Path, source_stage: str) -> list[dict[str, str]]:
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        rows = []
        for row in csv.DictReader(handle):
            if row.get("view") != "actual_routed_total":
                continue
            rows.append(
                {
                    "source_stage": source_stage,
                    "adapter_id": row.get("adapter_id", ""),
                    "split": row.get("split", ""),
                    "profit_factor": row.get("profit_factor", ""),
                    "net_profit": row.get("net_profit", ""),
                    "max_drawdown_amount": row.get("max_drawdown_amount", ""),
                    "cost_stressed_expectancy": row.get("cost_stressed_expectancy", ""),
                    "trade_count": row.get("trade_count", ""),
                    "same_move_reentry_ratio": row.get("same_move_reentry_ratio", ""),
                    "risk_floor_applied_count": row.get("risk_floor_applied_count", ""),
                    "status": row.get("status", ""),
                }
            )
        return rows


def num(row: Mapping[str, str], key: str) -> float | None:
    try:
        return float(str(row.get(key, "")).strip())
    except ValueError:
        return None


def rows_by_adapter(rows: Sequence[Mapping[str, str]]) -> dict[str, dict[str, Mapping[str, str]]]:
    grouped: dict[str, dict[str, Mapping[str, str]]] = {}
    for row in rows:
        grouped.setdefault(str(row.get("adapter_id")), {})[str(row.get("split"))] = row
    return grouped


def best_validation_net(rows: Sequence[Mapping[str, str]]) -> Mapping[str, str]:
    candidates = [row for row in rows if row.get("split") == "validation_is"]
    return max(candidates, key=lambda row: num(row, "net_profit") if num(row, "net_profit") is not None else -999999999)


def report_markdown(rows: Sequence[Mapping[str, str]], decision: str) -> str:
    table = "\n".join(
        "| {stage} | {adapter} | {split} | {pf} | {net} | {cost} | {same} | {trades} |".format(
            stage=row.get("source_stage"),
            adapter=row.get("adapter_id"),
            split=row.get("split"),
            pf=row.get("profit_factor"),
            net=row.get("net_profit"),
            cost=row.get("cost_stressed_expectancy"),
            same=row.get("same_move_reentry_ratio"),
            trades=row.get("trade_count"),
        )
        for row in rows
    )
    best_val = best_validation_net(rows)
    return f"""# Stage59I Demotion Or Branch From Stage59H Report(59I단계 59H단계 이후 강등 또는 분기 보고서)

- stage(단계): `{STAGE59I_ID}`
- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{STAGE59H_ID}`
- source_adapter(원천 어댑터): `{SOURCE_ADAPTER_ID}`
- source_external_verification(원천 외부 검증): `completed`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- decision(판정): `{decision}`
- boundary(경계): `{BOUNDARY}`

## Bounded Question(경계 질문)

Should the Stage59F-to-Stage59H v54 repair line(59F단계부터 59H단계까지의 v54 수리 계열) continue, be demoted(강등), or open a new model branch(새 모델 분기 개방) without starting ONNX hardening(ONNX 경화)?

## Evidence Table(근거 표)

| source(원천) | adapter(어댑터) | split(구간) | PF(수익 팩터) | net(순손익) | cost exp(비용 기대값) | same move(같은 움직임) | trades(거래 수) |
|---|---|---|---:|---:|---:|---:|---:|
{table}

## Read(판독)

- best_validation_net(최선 검증 순손익): `{best_val.get('adapter_id')}` / `{best_val.get('net_profit')}`
- repeated_failure_boundary(반복 실패 경계): `validation_net_negative;validation_pf_lt_1_10;validation_cost_stressed_expectancy_negative`
- repair_line_disposition(수리 계열 처리): `demote_current_v54_repair_line_and_open_new_model_branch`
- next_stage_or_branch(다음 단계/분기): `{NEXT_STAGE_ID}`

Effect(효과): Stage59I(59I단계)는 새 성능을 주장하지 않고, completed source evidence(완료된 원천 근거)로 Stage59F-H repair line(59F-H 수리 계열)의 반복 약점을 정리해 다음 bounded new branch(경계 새 분기)로 넘긴다.

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), overall goal complete(전체 목표 완료).
"""


def decision_markdown(decision: str) -> str:
    return f"""# Stage59I Decision(59I단계 판정)

decision(판정): `{decision}`

Stage59I(59I단계)는 Stage59G/Stage59H(59G/59H단계)의 completed MT5 evidence(완료된 MT5 근거)를 종합해 현재 v54 repair line(v54 수리 계열)을 계속 미세 조정하지 않기로 판정한다. Effect(효과): 반복된 validation weakness(검증 약점)를 숨기지 않고 다음 bounded new model branch(경계 새 모델 분기)로 넘긴다.

## Evidence(근거)

- stage59g_summary(59G단계 요약): `{rel(SOURCE59G_SUMMARY)}`
- stage59g_decision(59G단계 판정): `{rel(SOURCE59G_DECISION)}`
- stage59h_summary(59H단계 요약): `{rel(SOURCE59H_SUMMARY)}`
- stage59h_decision(59H단계 판정): `{rel(SOURCE59H_DECISION)}`
- synthesis_report(종합 보고서): `{rel(REPORT_PATH)}`
- synthesis_summary(종합 요약): `{rel(SUMMARY_CSV_PATH)}`
- source_external_verification_status(원천 외부 검증 상태): `completed`
- stage59i_external_verification_status(59I단계 외부 검증 상태): `{EXTERNAL_STATUS}`

## Reason(이유)

- Stage59G(59G단계) and Stage59H(59H단계) both kept validation net(검증 순손익) negative(음수), validation PF(검증 수익 팩터) below 1.10, and cost-stressed expectancy(비용 가중 기대값) negative(음수).
- Same-move reduction(같은 움직임 감소)은 확인됐지만 validation quality(검증 품질)를 회복하지 못했다.
- More threshold/cooldown tuning(추가 문턱값/쿨다운 조정)은 bounded stage anti-bloat(경계 단계 비대화 방지) 규칙상 Stage59I(59I단계) 안에서 계속하지 않는다.

## Next(다음)

next_stage_or_branch(다음 단계/분기): `{NEXT_STAGE_ID}`

Stage59I closeout(59I단계 종료)는 overall goal completion(전체 목표 완료)이 아니다. Effect(효과): Stage60 ONNX hardening(60단계 ONNX 경화)은 아직 열리지 않는다.

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), overall goal complete(전체 목표 완료).
"""


def artifact_rows(paths: Sequence[Path]) -> list[dict[str, Any]]:
    created = utc_now()
    rows = []
    for path in paths:
        if not path_exists(path):
            continue
        rows.append(
            {
                "artifact_id": f"{RUN_ID}__{re.sub(r'[^A-Za-z0-9]+', '_', rel(path)).strip('_')}",
                "artifact_type": "stage59i_decision_evidence",
                "path": rel(path),
                "sha256": sha256_file_lf_normalized(path),
                "stage_id": STAGE59I_ID,
                "run_id": RUN_ID,
                "created_at_utc": created,
                "notes": "Stage59I evidence synthesis and branch decision artifact.",
            }
        )
    return rows


def write_ledgers(summary_rows: Sequence[Mapping[str, str]], artifacts: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    best_val = best_validation_net(summary_rows)
    run_payload = upsert_csv_rows(
        RUN_REGISTRY_PATH,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE59I_ID,
                "lane": "baseline_adapter_demotion_or_branch_from_stage59h",
                "status": "completed",
                "judgment": DECISION,
                "path": rel(DECISION_PATH),
                "notes": ledger_pairs(
                    (
                        ("source_adapter", SOURCE_ADAPTER_ID),
                        ("best_validation_adapter", best_val.get("adapter_id")),
                        ("best_validation_net", best_val.get("net_profit")),
                        ("next_stage", NEXT_STAGE_ID),
                        ("boundary", BOUNDARY),
                    )
                ),
            }
        ],
        key="run_id",
    )
    ledger_rows = [
        {
            "ledger_row_id": f"{RUN_ID}__stage59i_branch_decision",
            "stage_id": STAGE59I_ID,
            "run_id": RUN_ID,
            "subrun_id": "stage59i_branch_decision",
            "parent_run_id": PARENT_RUN_ID,
            "record_view": "demotion_or_branch_from_stage59h",
            "tier_scope": "Tier A+B",
            "kpi_scope": "baseline_adapter_repair_decision",
            "scoreboard_lane": "kpi_evidence",
            "status": "completed",
            "judgment": DECISION,
            "path": rel(DECISION_PATH),
            "primary_kpi": ledger_pairs(
                (
                    ("best_validation_adapter", best_val.get("adapter_id")),
                    ("best_validation_net", best_val.get("net_profit")),
                    ("best_validation_pf", best_val.get("profit_factor")),
                    ("next_stage", NEXT_STAGE_ID),
                )
            ),
            "guardrail_kpi": ledger_pairs(
                (
                    ("overall_goal_complete", False),
                    ("onnx_hardening_opened", False),
                    ("deployment_claim", False),
                    ("source_external_verification", "completed"),
                )
            ),
            "external_verification_status": EXTERNAL_STATUS,
            "notes": "Decision-only stage using completed Stage59G/H evidence; opens next bounded model branch.",
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


def write_packet_files(summary_rows: Sequence[Mapping[str, str]], ledger_payload: Mapping[str, Any]) -> None:
    best_val = best_validation_net(summary_rows)
    files = {
        "routing_receipt.json": {
            "packet_id": PACKET_ID,
            "primary_family": "kpi_evidence",
            "primary_skill": "obsidian-run-evidence-system",
            "support_skills": ["obsidian-artifact-lineage", "obsidian-result-judgment", "obsidian-performance-attribution"],
            "required_gates": ["kpi_contract_audit", "source_authority_audit", "result_judgment_gate", "artifact_lineage_audit", "final_claim_guard"],
            "status": "completed",
        },
        "kpi_contract_audit.json": {
            "status": "completed",
            "source_rows": len(summary_rows),
            "source_files": [rel(SOURCE59G_SUMMARY), rel(SOURCE59H_SUMMARY)],
            "covered_requirements": ["validation/OOS PF", "validation/OOS net", "cost-stressed expectancy", "same-move concentration", "risk floor count"],
        },
        "source_authority_audit.json": {
            "status": "completed",
            "source_external_verification_status": "completed",
            "source_decisions": [rel(SOURCE59G_DECISION), rel(SOURCE59H_DECISION)],
            "stage59i_external_verification_status": EXTERNAL_STATUS,
        },
        "result_judgment_gate.json": {
            "result_subject": RUN_ID,
            "evidence_available": [rel(REPORT_PATH), rel(SUMMARY_CSV_PATH), rel(SOURCE59G_SUMMARY), rel(SOURCE59H_SUMMARY)],
            "evidence_missing": ["robust_post_atr_risk_adapter", "stage60_onnx_evidence", "research_package_review"],
            "judgment_label": DECISION,
            "best_validation_adapter": best_val.get("adapter_id"),
            "best_validation_net": best_val.get("net_profit"),
            "claim_boundary": BOUNDARY,
            "next_condition": NEXT_STAGE_ID,
            "status": "passed_with_boundary",
        },
        "artifact_lineage_audit.json": {
            "source_inputs": [rel(SOURCE59G_SUMMARY), rel(SOURCE59G_DECISION), rel(SOURCE59H_SUMMARY), rel(SOURCE59H_DECISION), rel(SOURCE59H_SEGMENT), rel(SOURCE59H_RISK)],
            "consumers": [rel(REPORT_PATH), rel(SUMMARY_JSON_PATH), rel(DECISION_PATH)],
            "ledger_links": ledger_payload,
        },
        "final_claim_guard.json": {
            "overall_goal_complete": False,
            "deployment_claim": False,
            "live_readiness_claim": False,
            "runtime_authority_claim": False,
            "production_baseline_claim": False,
            "operating_reference_claim": False,
            "operating_promotion_claim": False,
            "onnx_hardening_opened": False,
            "status": "passed",
        },
        "required_gate_coverage_audit.json": {
            "required_gates": ["kpi_contract_audit", "source_authority_audit", "result_judgment_gate", "artifact_lineage_audit", "final_claim_guard"],
            "covered_by": ["kpi_contract_audit.json", "source_authority_audit.json", "result_judgment_gate.json", "artifact_lineage_audit.json", "final_claim_guard.json"],
            "status": "completed",
        },
        "aggregate_summary.json": {
            "packet_id": PACKET_ID,
            "stage_id": STAGE59I_ID,
            "run_id": RUN_ID,
            "decision": DECISION,
            "external_verification_status": EXTERNAL_STATUS,
            "source_external_verification_status": "completed",
            "required_outputs": {
                "demotion_or_branch_report": rel(REPORT_PATH),
                "demotion_or_branch_summary_json": rel(SUMMARY_JSON_PATH),
                "demotion_or_branch_summary_csv": rel(SUMMARY_CSV_PATH),
                "stage59i_decision": rel(DECISION_PATH),
            },
            "claim_boundary": BOUNDARY,
            "overall_goal_complete": False,
        },
    }
    for name, payload in files.items():
        write_json(PACKET_ROOT / name, payload)


def write_stage_docs() -> None:
    write_md(
        SPEC_ROOT / "stage_brief.md",
        f"""# Stage59I Brief(59I단계 개요)

- stage_id(단계 ID): `{STAGE59I_ID}`
- source_stage(원천 단계): `{STAGE59H_ID}`
- source_decision(원천 판정): `continue_repair_in_new_bounded_stage`
- bounded_question(경계 질문): `Should the Stage59F-H v54 repair line continue, be demoted, or open a new model branch without starting ONNX?`
- boundary(경계): `{BOUNDARY}`

Stage59I(59I단계)는 새 MT5 run(새 MT5 실행)을 만들지 않는 evidence synthesis(근거 종합) 단계다. Effect(효과): 반복 실패한 local repair(로컬 수리)를 멈추고 다음 bounded branch(경계 분기)를 명확히 고른다.
""",
    )
    write_md(
        INPUT_ROOT / "input_refs.md",
        f"""# Stage59I Input References(59I단계 입력 참조)

- stage59g_summary(59G단계 요약): `{rel(SOURCE59G_SUMMARY)}`
- stage59g_decision(59G단계 판정): `{rel(SOURCE59G_DECISION)}`
- stage59h_summary(59H단계 요약): `{rel(SOURCE59H_SUMMARY)}`
- stage59h_decision(59H단계 판정): `{rel(SOURCE59H_DECISION)}`
- stage59h_segment_kpi(59H단계 구간 KPI): `{rel(SOURCE59H_SEGMENT)}`
- stage59h_risk_atr_telemetry(59H단계 위험/ATR 텔레메트리): `{rel(SOURCE59H_RISK)}`
- stage59h_pushed_commit(59H단계 푸시 커밋): `{SOURCE_STAGE59H_PUSHED_COMMIT}`

Effect(효과): Stage59I(59I단계)는 completed source evidence(완료된 원천 근거)만 사용해 분기 판정을 만든다.
""",
    )
    write_md(
        SELECTED_ROOT / "selection_status.md",
        f"""# Stage59I Selection Status(59I단계 선택 상태)

- stage_status(단계 상태): `closed_open_new_model_branch`
- source_stage(원천 단계): `{STAGE59H_ID}`
- source_decision(원천 판정): `continue_repair_in_new_bounded_stage`
- stage59i_decision(59I단계 판정): `{DECISION}`
- next_stage_or_branch(다음 단계/분기): `{NEXT_STAGE_ID}`
- selected_research_baseline(선택 연구 기준선): `none`
- claim_boundary(주장 경계): `{BOUNDARY}`

Effect(효과): Stage59I(59I단계)는 현재 v54 repair line(v54 수리 계열)을 final package(최종 패키지)로 만들지 않고 새 bounded branch(경계 분기)로 넘긴다.
""",
    )
    write_md(
        REVIEWS_ROOT / "review_index.md",
        f"""# Stage59I Review Index(59I단계 검토 색인)

- demotion_or_branch_report(강등 또는 분기 보고서): `{rel(REPORT_PATH)}`
- demotion_or_branch_summary(강등 또는 분기 요약): `{rel(SUMMARY_CSV_PATH)}`
- demotion_or_branch_summary_json(강등 또는 분기 JSON 요약): `{rel(SUMMARY_JSON_PATH)}`
- stage59i_decision(59I단계 판정): `{rel(DECISION_PATH)}`
- stage_run_ledger(단계 실행 장부): `{rel(STAGE_LEDGER_PATH)}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "00_spec/stage_brief.md",
        f"""# Stage59J Brief(59J단계 개요)

- stage_id(단계 ID): `{NEXT_STAGE_ID}`
- source_stage(원천 단계): `{STAGE59I_ID}`
- source_decision(원천 판정): `{DECISION}`
- bounded_question(경계 질문): `Can a new bounded model branch produce a post-ATR/risk adapter candidate after the Stage59F-H v54 repair line was demoted?`
- boundary(경계): `{BOUNDARY}`

Stage59J(59J단계)는 demoted v54 repair line(강등된 v54 수리 계열) 대신 새 model branch(모델 분기)를 작게 연다. Effect(효과): 같은 local threshold/cooldown repair(로컬 문턱값/쿨다운 수리)를 반복하지 않는다.
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "01_inputs/input_refs.md",
        f"""# Stage59J Input References(59J단계 입력 참조)

- stage59i_decision(59I단계 판정): `{rel(DECISION_PATH)}`
- stage59i_report(59I단계 보고서): `{rel(REPORT_PATH)}`
- stage59i_summary(59I단계 요약): `{rel(SUMMARY_CSV_PATH)}`
- stage59h_summary(59H단계 요약): `{rel(SOURCE59H_SUMMARY)}`
- stage59h_decision(59H단계 판정): `{rel(SOURCE59H_DECISION)}`

Effect(효과): Stage59J(59J단계)는 실패 기억(failure memory, 실패 기억)을 새 분기 입력으로 받는다.
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "03_reviews/review_index.md",
        """# Stage59J Review Index(59J단계 검토 색인)

Stage59J(59J단계)는 planned(계획) 상태다. Effect(효과): Stage59I(59I단계)의 branch decision(분기 판정)을 다음 실행 근거로 넘긴다.
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "04_selected/selection_status.md",
        f"""# Stage59J Selection Status(59J단계 선택 상태)

- stage_status(단계 상태): `active_planned_from_stage59i`
- source_stage(원천 단계): `{STAGE59I_ID}`
- source_decision(원천 판정): `{DECISION}`
- selected_research_baseline(선택 연구 기준선): `none`
- claim_boundary(주장 경계): `{BOUNDARY}`

Effect(효과): Stage59J(59J단계)는 Stage60 ONNX(60단계 ONNX)가 아니라 새 bounded model branch(경계 모델 분기)를 연다.
""",
    )


def update_current_truth() -> None:
    write_md(
        CURRENT_WORKING_STATE_PATH,
        f"""# Current Working State(현재 작업 상태)

- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- active_stage(활성 단계): `{NEXT_STAGE_ID}`
- selected_research_baseline(선택 연구 기준선): `none`
- development_anchor(개발 기준점): `{DEVELOPMENT_ANCHOR}`
- backup_anchor(예비 기준점): `{BACKUP_ANCHOR}`
- adapter_under_review(검토 중 어댑터): `none_new_branch_pending`
- status(상태): `stage59i_closed_open_new_model_branch`
- claim_boundary(주장 경계): research/development only(연구/개발 전용)

Stage59I(59I단계) closed(종료) as demotion/branch decision(강등/분기 판정). Effect(효과): Stage59F-H(59F-H단계) v54 repair line(v54 수리 계열)은 final package(최종 패키지)나 Stage60 ONNX(60단계 ONNX) 후보가 아니며, Stage59J(59J단계) 새 bounded branch(경계 새 분기)로 넘어간다.

## Latest Stage59I Evidence(최신 59I단계 근거)

- run(실행): `{RUN_ID}`
- decision(판정): `{DECISION}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- source_external_verification_status(원천 외부 검증 상태): `completed`
- next_stage_or_branch(다음 단계/분기): `{NEXT_STAGE_ID}`
- report(보고서): `{rel(REPORT_PATH)}`
- stage59i_decision(59I단계 판정): `{rel(DECISION_PATH)}`

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준선), overall_goal_complete(전체 목표 완료).
""",
    )
    text = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    text = re.sub(r"^current_run_id: .*$", f"current_run_id: {NEXT_RUN_ID}", text, count=1, flags=re.MULTILINE)
    text = re.sub(r"^updated_on: .*$", "updated_on: '2026-05-15'", text, count=1, flags=re.MULTILINE)
    text = re.sub(r"^active_stage: .*$", f"active_stage: {NEXT_STAGE_ID}", text, count=1, flags=re.MULTILINE)
    focus = (
        "current_focus:\n"
        f"- >-\n"
        f"  Stage59I(59I단계) `{STAGE59I_ID}` closed(종료) as demotion/branch decision(강등/분기 판정); decision(판정)=`{DECISION}`. Effect(효과): repeated v54 repair weakness(반복된 v54 수리 약점)을 보존하고 새 branch(분기)로 넘긴다.\n"
        f"- >-\n"
        f"  Next stage_or_branch(다음 단계/분기) `{NEXT_STAGE_ID}` is active/planned(활성/계획). Effect(효과): Stage60 ONNX(60단계 ONNX) 대신 새 bounded model branch(경계 모델 분기)를 연다.\n"
    )
    text = re.sub(r"current_focus:\n(?:- >-\n  Stage59I[^\n]*\n- >-\n  Next stage_or_branch[^\n]*\n)+", "current_focus:\n", text, count=1)
    text = re.sub(r"current_focus:\n", focus, text, count=1)
    block = f"""

stage59i_demotion_or_branch_from_stage59h:
  packet_id: {PACKET_ID}
  stage_id: {STAGE59I_ID}
  status: closed_open_new_model_branch
  current_run_id: {RUN_ID}
  source_adapter: {SOURCE_ADAPTER_ID}
  source_stage59h_pushed_commit: {SOURCE_STAGE59H_PUSHED_COMMIT}
  decision: {DECISION}
  next_stage_or_branch: {NEXT_STAGE_ID}
  report_path: {rel(DECISION_PATH)}
  packet_summary_path: {rel(PACKET_ROOT / "aggregate_summary.json")}
  external_verification_status: {EXTERNAL_STATUS}
  source_external_verification_status: completed
  boundary: {BOUNDARY}
"""
    if "stage59i_demotion_or_branch_from_stage59h:" in text:
        text = re.sub(r"\nstage59i_demotion_or_branch_from_stage59h:\n(?:  .*\n)*", block, text, count=1)
    else:
        text += block
    io_path(WORKSPACE_STATE_PATH).write_text(text, encoding="utf-8-sig")


def append_changelog() -> None:
    entry = (
        "\n## 2026-05-15 - Stage59I demotion or branch decision closeout(59I단계 강등 또는 분기 판정 종료)\n\n"
        f"- run(실행): `{RUN_ID}`\n"
        f"- decision(판정): `{DECISION}`\n"
        "- effect(효과): Stage59F-H(59F-H단계)의 v54 repair line(v54 수리 계열)을 final(최종)로 보지 않고 Stage59J(59J단계) 새 bounded model branch(경계 모델 분기)로 넘겼다.\n"
    )
    existing = io_path(CHANGELOG_PATH).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG_PATH) else ""
    if f"- run(실행): `{RUN_ID}`" not in existing:
        io_path(CHANGELOG_PATH).write_text(existing.rstrip() + entry, encoding="utf-8-sig")


def main() -> int:
    source_rows = read_actual_rows(SOURCE59G_SUMMARY, STAGE59G_ID) + read_actual_rows(SOURCE59H_SUMMARY, STAGE59H_ID)
    write_csv(SUMMARY_CSV_PATH, source_rows)
    payload = {
        "created_at_utc": utc_now(),
        "stage_id": STAGE59I_ID,
        "run_id": RUN_ID,
        "packet_id": PACKET_ID,
        "parent_run_id": PARENT_RUN_ID,
        "source_adapter": SOURCE_ADAPTER_ID,
        "decision": DECISION,
        "next_stage_or_branch": NEXT_STAGE_ID,
        "external_verification_status": EXTERNAL_STATUS,
        "source_external_verification_status": "completed",
        "summary_rows": source_rows,
        "claim_boundary": BOUNDARY,
        "overall_goal_complete": False,
    }
    write_json(SUMMARY_JSON_PATH, payload)
    write_md(REPORT_PATH, report_markdown(source_rows, DECISION))
    write_md(DECISION_PATH, decision_markdown(DECISION))
    artifacts = artifact_rows([REPORT_PATH, SUMMARY_JSON_PATH, SUMMARY_CSV_PATH, DECISION_PATH, STAGE_LEDGER_PATH, Path(__file__)])
    ledger_payload = write_ledgers(source_rows, artifacts)
    artifacts = artifact_rows([REPORT_PATH, SUMMARY_JSON_PATH, SUMMARY_CSV_PATH, DECISION_PATH, STAGE_LEDGER_PATH, Path(__file__)])
    ledger_payload = write_ledgers(source_rows, artifacts)
    payload["ledger_payload"] = ledger_payload
    write_json(SUMMARY_JSON_PATH, payload)
    write_packet_files(source_rows, ledger_payload)
    write_stage_docs()
    update_current_truth()
    append_changelog()
    print(json.dumps({"status": "ok", "run_id": RUN_ID, "decision": DECISION, "next_stage": NEXT_STAGE_ID}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
