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
    ledger_value,
    path_exists,
    sha256_file_lf_normalized,
    upsert_csv_rows,
)
from stage_pipelines.stage56 import independent_event_source_route_branch as aw  # noqa: E402


STAGE59AH_ID = "59AH_adapter_repair__bounded_followup_from_stage59ag"
NEXT_STAGE_ID = "59AI_adapter_repair__backup_anchor_probe_from_stage59ah"
RUN_ID = "run59AC_stage59ah_bounded_followup_from_stage59ag_v1"
RUN_NUMBER = "run59AC"
PACKET_ID = "stage59ah_bounded_followup_from_stage59ag_v1"
PARENT_RUN_ID = "run59AB_stage59ag_bounded_followup_from_stage59af_v1"
SOURCE_STAGE59AG_PUSHED_COMMIT = "dfe1dd202724c51af965fb175edaa018bf75ef18"
DEVELOPMENT_ANCHOR = "v64_v47_ctxgap14_refill_etfw_h2_no_b"
BACKUP_ANCHOR = "v60_v47_et_stable_damage_firewall_h2c0_no_b"
DEMOTED_ADAPTER = "s59ad_v64_gap14_t60_h4_entrytrans_sd5"
DECISION = "demote_current_adapter_and_select_backup"
NEXT_PACKET_ID = "stage59ai_backup_anchor_probe_from_stage59ah_v1"
NEXT_RUN_ID = "run59AD_stage59ai_backup_anchor_probe_from_stage59ah_v1"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment"
)

STAGE_ROOT = Path("stages") / STAGE59AH_ID
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
SPEC_ROOT = STAGE_ROOT / "00_spec"
INPUT_ROOT = STAGE_ROOT / "01_inputs"
SELECTED_ROOT = STAGE_ROOT / "04_selected"
PACKET_ROOT = Path("docs/agent_control/packets") / PACKET_ID
NEXT_ROOT = Path("stages") / NEXT_STAGE_ID

REPORT_PATH = REVIEWS_ROOT / "adapter_demotion_review.md"
SUMMARY_CSV_PATH = REVIEWS_ROOT / "demotion_evidence_summary.csv"
DECISION_PATH = REVIEWS_ROOT / "stage59ah_decision.md"
STAGE_LEDGER_PATH = REVIEWS_ROOT / "stage_run_ledger.csv"
RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
PROJECT_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
ARTIFACT_REGISTRY_PATH = Path("docs/registers/artifact_registry.csv")
WORKSPACE_STATE_PATH = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE_PATH = Path("docs/context/current_working_state.md")
CHANGELOG_PATH = Path("docs/workspace/changelog.md")

SOURCE_STAGES = [
    {
        "stage_label": "59AB",
        "stage_id": "59AB_adapter_repair__bounded_followup_from_stage59aa",
        "decision": "stages/59AB_adapter_repair__bounded_followup_from_stage59aa/03_reviews/stage59ab_decision.md",
        "summary_json": "stages/59AB_adapter_repair__bounded_followup_from_stage59aa/03_reviews/bounded_followup_summary.json",
        "pushed_commit": "9ba71b24f7ec71c6e41371a1bad28761f385cbfe",
    },
    {
        "stage_label": "59AC",
        "stage_id": "59AC_adapter_repair__bounded_followup_from_stage59ab",
        "decision": "stages/59AC_adapter_repair__bounded_followup_from_stage59ab/03_reviews/stage59ac_decision.md",
        "summary_json": "stages/59AC_adapter_repair__bounded_followup_from_stage59ab/03_reviews/bounded_followup_summary.json",
        "pushed_commit": "7b9a1f2dcf27b2715f3f91ec75a302376ca49db2",
    },
    {
        "stage_label": "59AD",
        "stage_id": "59AD_adapter_repair__bounded_followup_from_stage59ac",
        "decision": "stages/59AD_adapter_repair__bounded_followup_from_stage59ac/03_reviews/stage59ad_decision.md",
        "summary_json": "stages/59AD_adapter_repair__bounded_followup_from_stage59ac/03_reviews/bounded_followup_summary.json",
        "pushed_commit": "0c535c12a572af2afd148dd973f6c556424e0347",
    },
    {
        "stage_label": "59AE",
        "stage_id": "59AE_adapter_repair__bounded_followup_from_stage59ad",
        "decision": "stages/59AE_adapter_repair__bounded_followup_from_stage59ad/03_reviews/stage59ae_decision.md",
        "summary_json": "stages/59AE_adapter_repair__bounded_followup_from_stage59ad/03_reviews/bounded_followup_summary.json",
        "pushed_commit": "086965f69ffbf467cfb3b432e2a7c913768a3525",
    },
    {
        "stage_label": "59AF",
        "stage_id": "59AF_adapter_repair__bounded_followup_from_stage59ae",
        "decision": "stages/59AF_adapter_repair__bounded_followup_from_stage59ae/03_reviews/stage59af_decision.md",
        "summary_json": "stages/59AF_adapter_repair__bounded_followup_from_stage59ae/03_reviews/bounded_followup_summary.json",
        "pushed_commit": "556e54ad52f47f3f23e8553c4ebb8b4b42ad7920",
    },
    {
        "stage_label": "59AG",
        "stage_id": "59AG_adapter_repair__bounded_followup_from_stage59af",
        "decision": "stages/59AG_adapter_repair__bounded_followup_from_stage59af/03_reviews/stage59ag_decision.md",
        "summary_json": "stages/59AG_adapter_repair__bounded_followup_from_stage59af/03_reviews/bounded_followup_summary.json",
        "pushed_commit": SOURCE_STAGE59AG_PUSHED_COMMIT,
    },
]


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    candidate = Path(str(path))
    try:
        return io_path(candidate).resolve().relative_to(io_path(REPO_ROOT).resolve()).as_posix()
    except ValueError:
        return candidate.as_posix()


def read_json(path: Path | str) -> dict[str, Any]:
    return json.loads(io_path(Path(path)).read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: Mapping[str, Any]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text, encoding="utf-8-sig")


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    columns = list(rows[0].keys()) if rows else []
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: ledger_value(row.get(column, "")) for column in columns})


def source_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCE_STAGES:
        payload = read_json(source["summary_json"])
        best = payload.get("best_repaired_variant", {})
        validation = best.get("validation") if isinstance(best.get("validation"), Mapping) else {}
        oos = best.get("oos") if isinstance(best.get("oos"), Mapping) else {}
        rows.append(
            {
                "stage_label": source["stage_label"],
                "stage_id": source["stage_id"],
                "best_adapter": best.get("adapter_id", "none"),
                "validation_pf": validation.get("profit_factor"),
                "validation_net": validation.get("net_profit"),
                "validation_drawdown": validation.get("max_drawdown_amount"),
                "validation_cost_stressed_expectancy": validation.get("cost_stressed_expectancy"),
                "oos_pf": oos.get("profit_factor"),
                "oos_net": oos.get("net_profit"),
                "oos_drawdown": oos.get("max_drawdown_amount"),
                "oos_cost_stressed_expectancy": oos.get("cost_stressed_expectancy"),
                "validation_pass": bool(
                    float(validation.get("profit_factor") or 0) >= 1.10
                    and float(validation.get("cost_stressed_expectancy") or 0) > 0
                    and float(validation.get("net_profit") or 0) > 0
                ),
                "oos_pass": bool(
                    float(oos.get("profit_factor") or 0) >= 1.10
                    and float(oos.get("cost_stressed_expectancy") or 0) > 0
                    and float(oos.get("net_profit") or 0) > 0
                ),
                "decision_path": source["decision"],
                "summary_json": source["summary_json"],
                "pushed_commit": source["pushed_commit"],
            }
        )
    return rows


def report_markdown(rows: Sequence[Mapping[str, Any]]) -> str:
    table = "\n".join(
        "| {stage} | {adapter} | {vpf} | {vnet} | {vcost} | {opf} | {onet} | {ocost} |".format(
            stage=row.get("stage_label"),
            adapter=row.get("best_adapter"),
            vpf=aw.fmt(row.get("validation_pf")),
            vnet=aw.fmt(row.get("validation_net")),
            vcost=aw.fmt(row.get("validation_cost_stressed_expectancy")),
            opf=aw.fmt(row.get("oos_pf")),
            onet=aw.fmt(row.get("oos_net")),
            ocost=aw.fmt(row.get("oos_cost_stressed_expectancy")),
        )
        for row in rows
    )
    failed_validation = [row.get("stage_label") for row in rows if not row.get("validation_pass")]
    return f"""# Stage59AH Adapter Demotion Review(59AH단계 어댑터 강등 검토)

- stage(단계): `{STAGE59AH_ID}`
- run(실행): `{RUN_ID}`
- decision(판정): `{DECISION}`
- boundary(경계): `{BOUNDARY}`

## Bounded Question(경계 질문)

Should the current v64 BaselineAdapter repair branch(현재 v64 기준선 어댑터 수리 분기) be demoted(강등) after Stage59AB-Stage59AG evidence, and should the next bounded stage(다음 경계 단계) probe the backup anchor(예비 기준점)?

## Evidence Table(근거 표)

| stage(단계) | best adapter(최선 어댑터) | validation PF(검증 수익 팩터) | validation net(검증 순손익) | validation cost exp(검증 비용 기대값) | OOS PF(표본외 수익 팩터) | OOS net(표본외 순손익) | OOS cost exp(표본외 비용 기대값) |
|---|---|---:|---:|---:|---:|---:|---:|
{table}

## Read(판독)

- failed_validation_stages(검증 실패 단계): `{";".join(str(item) for item in failed_validation)}`
- demoted_adapter(강등 어댑터): `{DEMOTED_ADAPTER}`
- backup_anchor(예비 기준점): `{BACKUP_ANCHOR}`
- next_stage_or_branch(다음 단계/분기): `{NEXT_STAGE_ID}`

Effect(효과): repeated repair failures(반복 수리 실패)를 숨기지 않고, 현재 v64 branch(v64 분기)를 Stage60 ONNX(60단계 ONNX)로 보내지 않는다. 다음 작업은 backup anchor probe(예비 기준점 탐침)로 좁힌다.

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), overall goal complete(전체 목표 완료).
"""


def decision_markdown(rows: Sequence[Mapping[str, Any]]) -> str:
    return f"""# Stage59AH Decision(59AH단계 판정)

decision(판정): `{DECISION}`

Stage59AH(59AH단계)는 Stage59AB-Stage59AG(Stage59AB-59AG단계)의 completed evidence(완료 근거)를 종합한 demotion review(강등 검토)다. Effect(효과): 반복된 validation PF/cost weakness(검증 수익 팩터/비용 약점)를 수리 성공으로 포장하지 않고 backup anchor(예비 기준점) 경로로 넘긴다.

## Evidence(근거)

- demotion_review(강등 검토): `{rel(REPORT_PATH)}`
- demotion_evidence_summary(강등 근거 요약): `{rel(SUMMARY_CSV_PATH)}`
- external_verification_status(외부 검증 상태): `completed_existing_mt5_evidence`
- source_stage_count(원천 단계 수): `{len(rows)}`

## Reason(이유)

- validation_success_count(검증 성공 수): `{sum(1 for row in rows if row.get("validation_pass"))}`
- validation_failure_count(검증 실패 수): `{sum(1 for row in rows if not row.get("validation_pass"))}`
- demoted_adapter(강등 어댑터): `{DEMOTED_ADAPTER}`

## Next(다음)

next_stage_or_branch(다음 단계/분기): `{NEXT_STAGE_ID}`

Stage59AH closeout(59AH단계 종료)는 overall goal completion(전체 목표 완료)이 아니다. Effect(효과): backup anchor probe(예비 기준점 탐침)를 다음 bounded stage(경계 단계)로 열고, operating claim(운영 주장)을 만들지 않는다.

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), overall goal complete(전체 목표 완료).
"""


def artifact_rows() -> list[dict[str, Any]]:
    created = utc_now()
    paths = [
        REPORT_PATH,
        SUMMARY_CSV_PATH,
        DECISION_PATH,
        STAGE_LEDGER_PATH,
        PACKET_ROOT / "aggregate_summary.json",
        PACKET_ROOT / "result_judgment_gate.json",
        PACKET_ROOT / "artifact_lineage_audit.json",
        PACKET_ROOT / "final_claim_guard.json",
        PACKET_ROOT / "required_gate_coverage_audit.json",
    ]
    rows = []
    for path in paths:
        if path_exists(path):
            rows.append(
                {
                    "artifact_id": f"{RUN_ID}__{re.sub(r'[^A-Za-z0-9]+', '_', rel(path)).strip('_')}",
                    "stage_id": STAGE59AH_ID,
                    "run_id": RUN_ID,
                    "artifact_type": "stage59ah_demotion_review_evidence",
                    "path": rel(path),
                    "sha256": sha256_file_lf_normalized(path),
                    "created_at_utc": created,
                    "notes": "Stage59AH demotion review artifact from Stage59AB-Stage59AG evidence.",
                }
            )
    return rows


def write_ledgers(rows: Sequence[Mapping[str, Any]], artifacts: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    run_payload = upsert_csv_rows(
        RUN_REGISTRY_PATH,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE59AH_ID,
                "lane": "baseline_adapter_demotion_review",
                "status": "completed",
                "judgment": DECISION,
                "path": rel(DECISION_PATH),
                "notes": ledger_pairs(
                    (
                        ("demoted_adapter", DEMOTED_ADAPTER),
                        ("backup_anchor", BACKUP_ANCHOR),
                        ("source_stage_count", len(rows)),
                        ("boundary", BOUNDARY),
                    )
                ),
            }
        ],
        key="run_id",
    )
    ledger_rows = [
        {
            "ledger_row_id": f"{RUN_ID}__aggregate_demotion_review",
            "stage_id": STAGE59AH_ID,
            "run_id": RUN_ID,
            "subrun_id": "aggregate_demotion_review",
            "parent_run_id": PARENT_RUN_ID,
            "record_view": "demotion_review",
            "tier_scope": "Tier A+B",
            "kpi_scope": "baseline_adapter_repair",
            "scoreboard_lane": "result_judgment",
            "status": "completed",
            "judgment": DECISION,
            "path": rel(DECISION_PATH),
            "primary_kpi": ledger_pairs(
                (
                    ("validation_success_count", sum(1 for row in rows if row.get("validation_pass"))),
                    ("validation_failure_count", sum(1 for row in rows if not row.get("validation_pass"))),
                    ("demoted_adapter", DEMOTED_ADAPTER),
                    ("backup_anchor", BACKUP_ANCHOR),
                )
            ),
            "guardrail_kpi": ledger_pairs(
                (
                    ("overall_goal_complete", False),
                    ("deployment_claim", False),
                    ("runtime_authority_claim", False),
                )
            ),
            "external_verification_status": "completed_existing_mt5_evidence",
            "notes": "Stage59AH demotion review only; not final package completion.",
        }
    ]
    stage_payload = upsert_csv_rows(STAGE_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, ledger_rows, key="ledger_row_id")
    project_payload = upsert_csv_rows(PROJECT_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, ledger_rows, key="ledger_row_id")
    artifact_payload = upsert_csv_rows(ARTIFACT_REGISTRY_PATH, aw.ARTIFACT_COLUMNS, list(artifacts), key="artifact_id")
    return {"run_registry": run_payload, "stage_ledger": stage_payload, "project_alpha_ledger": project_payload, "artifact_registry": artifact_payload}


def write_packet_files(rows: Sequence[Mapping[str, Any]], ledger_payload: Mapping[str, Any]) -> None:
    source_inputs = [item["decision"] for item in SOURCE_STAGES] + [item["summary_json"] for item in SOURCE_STAGES]
    files = {
        "routing_receipt.json": {
            "packet_id": PACKET_ID,
            "primary_family": "kpi_evidence",
            "primary_skill": "obsidian-result-judgment",
            "support_skills": ["obsidian-artifact-lineage", "obsidian-performance-attribution"],
            "required_gates": ["runtime_evidence_gate", "kpi_contract_audit", "result_judgment_gate", "artifact_lineage_audit", "final_claim_guard"],
            "status": "completed",
        },
        "runtime_evidence_gate.json": {
            "external_verification_status": "completed_existing_mt5_evidence",
            "source_stages": SOURCE_STAGES,
            "status": "completed",
        },
        "kpi_contract_audit.json": {
            "source_stage_count": len(rows),
            "summary_rows": len(rows),
            "status": "completed",
        },
        "result_judgment_gate.json": {
            "result_subject": RUN_ID,
            "evidence_available": [rel(REPORT_PATH), rel(SUMMARY_CSV_PATH), rel(DECISION_PATH)],
            "evidence_missing": [],
            "judgment_label": "exploratory",
            "stage_decision": DECISION,
            "claim_boundary": BOUNDARY,
            "next_condition": NEXT_STAGE_ID,
            "status": "passed_with_boundary",
        },
        "artifact_lineage_audit.json": {
            "source_inputs": source_inputs,
            "producer": rel(Path("stage_pipelines/stage59ah/demotion_review_from_stage59ag.py")),
            "consumers": [rel(REPORT_PATH), rel(SUMMARY_CSV_PATH), rel(DECISION_PATH)],
            "ledger_links": ledger_payload,
            "lineage_judgment": "connected_with_boundary",
            "status": "completed",
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
        "required_gate_coverage_audit.json": {
            "required_gates": ["runtime_evidence_gate", "kpi_contract_audit", "result_judgment_gate", "artifact_lineage_audit", "final_claim_guard"],
            "covered_by": ["runtime_evidence_gate.json", "kpi_contract_audit.json", "result_judgment_gate.json", "artifact_lineage_audit.json", "final_claim_guard.json"],
            "status": "completed",
        },
        "aggregate_summary.json": {
            "packet_id": PACKET_ID,
            "stage_id": STAGE59AH_ID,
            "run_id": RUN_ID,
            "decision": DECISION,
            "external_verification_status": "completed_existing_mt5_evidence",
            "demoted_adapter": DEMOTED_ADAPTER,
            "backup_anchor": BACKUP_ANCHOR,
            "next_stage_or_branch": NEXT_STAGE_ID,
            "overall_goal_complete": False,
            "claim_boundary": BOUNDARY,
        },
    }
    for name, payload in files.items():
        write_json(PACKET_ROOT / name, payload)


def write_stage_docs() -> None:
    write_md(
        SPEC_ROOT / "stage_brief.md",
        f"""# Stage59AH Brief(59AH단계 개요)

- stage_id(단계 ID): `{STAGE59AH_ID}`
- source_stage(원천 단계): `59AG_adapter_repair__bounded_followup_from_stage59af`
- source_decision(원천 판정): `continue_repair_in_new_bounded_stage`
- bounded_question(경계 질문): `Should repeated Stage59AB-Stage59AG repair failure demote the current v64 adapter and route to backup anchor probing?`
- boundary(경계): `{BOUNDARY}`

Stage59AH(59AH단계)는 existing evidence review(기존 근거 검토)다. Effect(효과): 새 파라미터를 더 얹지 않고 demotion/backup path(강등/예비 경로)를 명확히 정한다.
""",
    )
    write_md(
        INPUT_ROOT / "input_refs.md",
        "# Stage59AH Input References(59AH단계 입력 참조)\n\n"
        + "\n".join(f"- {item['stage_label']} decision(판정): `{item['decision']}`" for item in SOURCE_STAGES)
        + "\n",
    )
    write_md(
        SELECTED_ROOT / "selection_status.md",
        f"""# Stage59AH Selection Status(59AH단계 선택 상태)

- stage_status(단계 상태): `closed_demotion_review_from_stage59ag`
- source_stage(원천 단계): `59AG_adapter_repair__bounded_followup_from_stage59af`
- source_decision(원천 판정): `continue_repair_in_new_bounded_stage`
- stage59ah_decision(59AH단계 판정): `{DECISION}`
- next_stage_or_branch(다음 단계/분기): `{NEXT_STAGE_ID}`
- selected_research_baseline(선택 연구 기준선): `none`
- claim_boundary(주장 경계): `{BOUNDARY}`

Effect(효과): Stage59AH(59AH단계)는 current adapter(현재 어댑터)를 final package(최종 패키지)로 올리지 않고 backup anchor probe(예비 기준점 탐침)를 연다.
""",
    )
    write_md(
        REVIEWS_ROOT / "review_index.md",
        f"""# Stage59AH Review Index(59AH단계 검토 색인)

- adapter_demotion_review(어댑터 강등 검토): `{rel(REPORT_PATH)}`
- demotion_evidence_summary(강등 근거 요약): `{rel(SUMMARY_CSV_PATH)}`
- stage59ah_decision(59AH단계 판정): `{rel(DECISION_PATH)}`
""",
    )
    write_md(
        NEXT_ROOT / "00_spec/stage_brief.md",
        f"""# 59AI Brief(59AI단계 개요)

- stage_id(단계 ID): `{NEXT_STAGE_ID}`
- source_stage(원천 단계): `{STAGE59AH_ID}`
- source_decision(원천 판정): `{DECISION}`
- bounded_question(경계 질문): `Can the backup anchor be probed as a bounded replacement path after current v64 adapter demotion?`
- boundary(경계): `{BOUNDARY}`

59AI(59AI단계)는 backup anchor probe(예비 기준점 탐침) 계획 단계다. Effect(효과): current v64 adapter(현재 v64 어댑터)를 계속 수리하지 않고 replacement path(대체 경로)를 작게 연다.
""",
    )
    write_md(
        NEXT_ROOT / "01_inputs/input_refs.md",
        f"""# 59AI Input References(59AI단계 입력 참조)

- stage59ah_decision(59AH단계 판정): `{rel(DECISION_PATH)}`
- demotion_review(강등 검토): `{rel(REPORT_PATH)}`
- backup_anchor(예비 기준점): `{BACKUP_ANCHOR}`
""",
    )
    write_md(
        NEXT_ROOT / "03_reviews/review_index.md",
        "# 59AI Review Index(59AI단계 검토 색인)\n\n59AI(59AI단계)는 planned(계획) 상태다.\n",
    )
    write_md(
        NEXT_ROOT / "04_selected/selection_status.md",
        f"""# 59AI Selection Status(59AI단계 선택 상태)

- stage_status(단계 상태): `active_planned_from_stage59ah`
- source_stage(원천 단계): `{STAGE59AH_ID}`
- source_decision(원천 판정): `{DECISION}`
- selected_research_baseline(선택 연구 기준선): `none`
- claim_boundary(주장 경계): `{BOUNDARY}`

Effect(효과): 59AI(59AI단계)는 backup anchor(예비 기준점)를 다음 bounded question(경계 질문)으로 다룬다.
""",
    )


def update_current_truth(rows: Sequence[Mapping[str, Any]]) -> None:
    write_md(
        CURRENT_WORKING_STATE_PATH,
        f"""# Current Working State(현재 작업 상태)

- current_packet(현재 작업 묶음): `{NEXT_PACKET_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- active_stage(활성 단계): `{NEXT_STAGE_ID}`
- selected_research_baseline(선택 연구 기준선): `none`
- development_anchor(개발 기준점): `{DEVELOPMENT_ANCHOR}`
- backup_anchor(예비 기준점): `{BACKUP_ANCHOR}`
- adapter_under_review(검토 중 어댑터): `{BACKUP_ANCHOR}`
- status(상태): `stage59ah_closed_{DECISION}`
- claim_boundary(주장 경계): research/development only(연구/개발 전용)

Stage59AH(59AH단계) closed(종료) as existing-evidence demotion review(기존 근거 강등 검토). Effect(효과): Stage59AB-Stage59AG(Stage59AB-59AG단계)의 repeated validation weakness(반복 검증 약점)를 보존하고, current v64 adapter(현재 v64 어댑터)를 Stage60 ONNX(60단계 ONNX)로 넘기지 않는다.

## Latest Stage59AH Evidence(최신 59AH단계 근거)

- run(실행): `{RUN_ID}`
- decision(판정): `{DECISION}`
- demoted_adapter(강등 어댑터): `{DEMOTED_ADAPTER}`
- backup_anchor(예비 기준점): `{BACKUP_ANCHOR}`
- source_stage_count(원천 단계 수): `{len(rows)}`
- next_stage_or_branch(다음 단계/분기): `{NEXT_STAGE_ID}`
- report(보고서): `{rel(REPORT_PATH)}`
- stage59ah_decision(59AH단계 판정): `{rel(DECISION_PATH)}`

Forbidden claims(금지 주장): deployment(배포), live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(생산 기준선), overall_goal_complete(전체 목표 완료).
""",
    )
    text = io_path(WORKSPACE_STATE_PATH).read_text(encoding="utf-8-sig")
    text = re.sub(r"^current_run_id: .*$", f"current_run_id: {NEXT_RUN_ID}", text, count=1, flags=re.MULTILINE)
    text = re.sub(r"^updated_on: .*$", "updated_on: '2026-05-16'", text, count=1, flags=re.MULTILINE)
    text = re.sub(r"^active_stage: .*$", f"active_stage: {NEXT_STAGE_ID}", text, count=1, flags=re.MULTILINE)
    focus = (
        "current_focus:\n"
        f"- >-\n"
        f"  Stage59AH(59AH단계) `{STAGE59AH_ID}` closed(종료) as demotion review(강등 검토); decision(판정)=`{DECISION}`. "
        f"Effect(효과): current v64 adapter(현재 v64 어댑터)는 demoted(강등)되며 final(최종) 또는 operating(운영) 주장은 없다.\n"
        f"- >-\n"
        f"  Next stage_or_branch(다음 단계/분기) `{NEXT_STAGE_ID}` is active/planned(활성/계획). Effect(효과): backup anchor(예비 기준점)를 다음 bounded step(경계 다음 단계)으로 넘긴다.\n"
    )
    text = re.sub(r"current_focus:\n(?:- >-\n(?:  .*\n)+)+", focus, text, count=1)
    block = f"""

stage59ah_demotion_review_from_stage59ag:
  packet_id: {PACKET_ID}
  stage_id: {STAGE59AH_ID}
  status: closed_demotion_review_from_stage59ag
  current_run_id: {RUN_ID}
  demoted_adapter: {DEMOTED_ADAPTER}
  backup_anchor: {BACKUP_ANCHOR}
  source_stage59ag_pushed_commit: {SOURCE_STAGE59AG_PUSHED_COMMIT}
  decision: {DECISION}
  next_stage_or_branch: {NEXT_STAGE_ID}
  report_path: {rel(DECISION_PATH)}
  packet_summary_path: {rel(PACKET_ROOT / "aggregate_summary.json")}
  external_verification_status: completed_existing_mt5_evidence
  boundary: {BOUNDARY}
"""
    if "stage59ah_demotion_review_from_stage59ag:" in text:
        text = re.sub(r"\nstage59ah_demotion_review_from_stage59ag:\n(?:  .*\n)*", block, text, count=1)
    else:
        text += block
    io_path(WORKSPACE_STATE_PATH).write_text(text, encoding="utf-8-sig")


def append_changelog() -> None:
    entry = (
        "\n## 2026-05-16 - Stage59AH demotion review closeout(59AH단계 강등 검토 종료)\n\n"
        f"- run(실행): `{RUN_ID}`\n"
        f"- decision(판정): `{DECISION}`\n"
        f"- effect(효과): Stage59AB-Stage59AG(Stage59AB-59AG단계)의 repeated validation weakness(반복 검증 약점)를 근거로 `{DEMOTED_ADAPTER}`를 demoted(강등)하고 backup anchor probe(예비 기준점 탐침)로 넘겼다.\n"
    )
    existing = io_path(CHANGELOG_PATH).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG_PATH) else ""
    if f"- run(실행): `{RUN_ID}`" not in existing:
        io_path(CHANGELOG_PATH).write_text(existing.rstrip() + entry, encoding="utf-8-sig")


def main() -> int:
    rows = source_rows()
    write_csv(SUMMARY_CSV_PATH, rows)
    write_md(REPORT_PATH, report_markdown(rows))
    write_md(DECISION_PATH, decision_markdown(rows))
    write_packet_files(rows, {})
    artifacts = artifact_rows()
    ledger_payload = write_ledgers(rows, artifacts)
    write_packet_files(rows, ledger_payload)
    artifacts = artifact_rows()
    ledger_payload = write_ledgers(rows, artifacts)
    write_packet_files(rows, ledger_payload)
    write_stage_docs()
    update_current_truth(rows)
    append_changelog()
    print(json.dumps(json_ready({"status": "ok", "run_id": RUN_ID, "decision": DECISION, "next_stage": NEXT_STAGE_ID, "summary_csv": rel(SUMMARY_CSV_PATH)}), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
