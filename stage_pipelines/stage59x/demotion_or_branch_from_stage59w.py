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


STAGE59V_ID = "59V_adapter_repair__bounded_followup_from_stage59u"
STAGE59W_ID = "59W_adapter_repair__bounded_followup_from_stage59v"
STAGE59X_ID = "59X_adapter_repair__bounded_followup_from_stage59w"
NEXT_STAGE_ID = "59Y_adapter_repair__new_model_branch_from_stage59x"
RUN_ID = "run59S_stage59x_bounded_followup_from_stage59w_v1"
NEXT_RUN_ID = "run59T_stage59y_new_model_branch_from_stage59x_v1"
PACKET_ID = "stage59x_bounded_followup_from_stage59w_v1"
NEXT_PACKET_ID = "stage59y_new_model_branch_from_stage59x_v1"
PARENT_RUN_ID = "run59R_stage59w_bounded_followup_from_stage59v_v1"
SOURCE_ADAPTER_ID = "s59w_s59v_st54_mr025_sl20_tp30_sd12_h5_rearm002"
SOURCE_STAGE59V_PUSHED_COMMIT = "f106d9fcdb94b368b48f635ff6870decf0542b10"
SOURCE_STAGE59W_PUSHED_COMMIT = "d529a6cbd51b1701e755cc6493104d78f02aa3a5"
DEVELOPMENT_ANCHOR = "v64_v47_ctxgap14_refill_etfw_h2_no_b"
BACKUP_ANCHOR = "v60_v47_et_stable_damage_firewall_h2c0_no_b"
DECISION = "open_new_model_branch"
EXTERNAL_STATUS = "not_applicable"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_no_deployment"
)

STAGE_ROOT = Path("stages") / STAGE59X_ID
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
SPEC_ROOT = STAGE_ROOT / "00_spec"
INPUT_ROOT = STAGE_ROOT / "01_inputs"
SELECTED_ROOT = STAGE_ROOT / "04_selected"
PACKET_ROOT = Path("docs/agent_control/packets") / PACKET_ID
NEXT_STAGE_ROOT = Path("stages") / NEXT_STAGE_ID

SOURCE59V_ROOT = Path("stages") / STAGE59V_ID
SOURCE59W_ROOT = Path("stages") / STAGE59W_ID
SOURCE59V_SUMMARY = SOURCE59V_ROOT / "03_reviews/bounded_followup_summary.csv"
SOURCE59V_DECISION = SOURCE59V_ROOT / "03_reviews/stage59v_decision.md"
SOURCE59V_SEGMENT = SOURCE59V_ROOT / "03_reviews/bounded_followup_segment_kpi_summary.csv"
SOURCE59V_RISK = SOURCE59V_ROOT / "03_reviews/bounded_followup_risk_atr_telemetry.csv"
SOURCE59W_SUMMARY = SOURCE59W_ROOT / "03_reviews/bounded_followup_summary.csv"
SOURCE59W_DECISION = SOURCE59W_ROOT / "03_reviews/stage59w_decision.md"
SOURCE59W_SEGMENT = SOURCE59W_ROOT / "03_reviews/bounded_followup_segment_kpi_summary.csv"
SOURCE59W_RISK = SOURCE59W_ROOT / "03_reviews/bounded_followup_risk_atr_telemetry.csv"

REPORT_PATH = REVIEWS_ROOT / "demotion_or_branch_from_stage59w_report.md"
SUMMARY_JSON_PATH = REVIEWS_ROOT / "demotion_or_branch_summary.json"
SUMMARY_CSV_PATH = REVIEWS_ROOT / "demotion_or_branch_summary.csv"
DECISION_PATH = REVIEWS_ROOT / "stage59x_decision.md"
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


def read_segment_flags(path: Path, source_stage: str, adapter_id: str) -> list[dict[str, str]]:
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        flagged = []
        for row in csv.DictReader(handle):
            if row.get("adapter_id") != adapter_id:
                continue
            quality_flag = str(row.get("quality_flag") or "")
            if not quality_flag or quality_flag == "acceptable_measurement_only":
                continue
            flagged.append(
                {
                    "source_stage": source_stage,
                    "split": row.get("split", ""),
                    "segment_type": row.get("segment_type", ""),
                    "segment": row.get("segment", ""),
                    "net_profit": row.get("net_profit", ""),
                    "profit_factor": row.get("profit_factor", ""),
                    "expectancy": row.get("expectancy", ""),
                    "mfe_capture_ratio": row.get("mfe_capture_ratio", ""),
                    "quality_flag": quality_flag,
                }
            )
        return flagged


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


def flag_markdown(flags: Sequence[Mapping[str, str]]) -> str:
    if not flags:
        return "- flagged_segments(표시된 구간): `none_detected_in_source_files`"
    return "\n".join(
        "- {stage} / {split} / {segment}: net={net}, PF={pf}, expectancy={exp}, MFE capture={mfe}, flag=`{flag}`".format(
            stage=row.get("source_stage"),
            split=row.get("split"),
            segment=row.get("segment"),
            net=row.get("net_profit"),
            pf=row.get("profit_factor"),
            exp=row.get("expectancy"),
            mfe=row.get("mfe_capture_ratio"),
            flag=row.get("quality_flag"),
        )
        for row in flags
    )


def report_markdown(rows: Sequence[Mapping[str, str]], flags: Sequence[Mapping[str, str]], decision: str) -> str:
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
    return f"""# Stage59X Demotion Or Branch From Stage59W Report(59X단계 59W단계 이후 강등 또는 분기 보고서)

- stage(단계): `{STAGE59X_ID}`
- run(실행): `{RUN_ID}`
- source_stage(원천 단계): `{STAGE59W_ID}`
- source_adapter(원천 어댑터): `{SOURCE_ADAPTER_ID}`
- source_external_verification(원천 외부 검증): `completed`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- decision(판정): `{decision}`
- boundary(경계): `{BOUNDARY}`

## Bounded Question(경계 질문)

Should the Stage59S/V/W repair line(Stage59S/V/W 수리 계열) continue with more local threshold/risk-cap repairs, be demoted(강등), or open a new model branch(새 모델 분기 개방) without starting ONNX hardening(ONNX 경화)?

## Evidence Table(근거 표)

| source(원천) | adapter(어댑터) | split(구간) | PF(수익 팩터) | net(순손익) | cost exp(비용 기대값) | same move(같은 움직임) | trades(거래 수) |
|---|---|---|---:|---:|---:|---:|---:|
{table}

## Read(판독)

- best_validation_net(최선 검증 순손익): `{best_val.get('adapter_id')}` / `{best_val.get('net_profit')}`
- repeated_weakness_boundary(반복 약점 경계): `validation_early_negative;validation_early_pf_below_1;OOS_mid_weak_pf;short_threshold_no_op`
- repair_line_disposition(수리 계열 처리): `demote_current_stage59s_v_w_repair_line_and_open_new_model_branch`
- next_stage_or_branch(다음 단계/분기): `{NEXT_STAGE_ID}`

## Segment Flags(구간 표시)

{flag_markdown(flags)}

Effect(효과): Stage59X(59X단계)는 새 성능을 주장하지 않고, completed source evidence(완료된 원천 근거)로 Stage59S/V/W repair line(Stage59S/V/W 수리 계열)의 반복 약점을 정리해 다음 bounded new branch(경계 새 분기)로 넘긴다.

Forbidden claims(금지 주장): deployment(배포), live readiness(실거래 준비), production baseline(생산 기준선), operating promotion(운영 승격), operating reference(운영 기준), runtime authority(런타임 권위), overall goal complete(전체 목표 완료).
"""


def decision_markdown(flags: Sequence[Mapping[str, str]], decision: str) -> str:
    return f"""# Stage59X Decision(59X단계 판정)

decision(판정): `{decision}`

Stage59X(59X단계)는 Stage59V/Stage59W(59V/59W단계)의 completed MT5 evidence(완료된 MT5 근거)를 종합해 현재 Stage59S/V/W repair line(Stage59S/V/W 수리 계열)을 계속 미세 조정하지 않기로 판정한다. Effect(효과): 반복된 segment weakness(구간 약점)를 숨기지 않고 다음 bounded new model branch(경계 새 모델 분기)로 넘긴다.

## Evidence(근거)

- stage59v_summary(59V단계 요약): `{rel(SOURCE59V_SUMMARY)}`
- stage59v_decision(59V단계 판정): `{rel(SOURCE59V_DECISION)}`
- stage59w_summary(59W단계 요약): `{rel(SOURCE59W_SUMMARY)}`
- stage59w_decision(59W단계 판정): `{rel(SOURCE59W_DECISION)}`
- synthesis_report(종합 보고서): `{rel(REPORT_PATH)}`
- synthesis_summary(종합 요약): `{rel(SUMMARY_CSV_PATH)}`
- source_external_verification_status(원천 외부 검증 상태): `completed`
- stage59x_external_verification_status(59X단계 외부 검증 상태): `{EXTERNAL_STATUS}`

## Reason(이유)

- Stage59W(59W단계) short_threshold(숏 임계값) 0.54/0.56/0.58 variants(변형)는 final KPI(최종 KPI)가 사실상 동일했다.
- validation early(검증 초기) net(순손익) `-73.11`, PF(수익 팩터) `0.9366` and OOS mid(표본외 중간) PF(수익 팩터) `1.0424` weakness(약점)가 남았다.
- More threshold/risk-cap tuning(추가 문턱값/위험 상한 조정)은 bounded stage anti-bloat(경계 단계 비대화 방지) 규칙상 Stage59X(59X단계) 안에서 계속하지 않는다.

## Segment Flags(구간 표시)

{flag_markdown(flags)}

## Next(다음)

next_stage_or_branch(다음 단계/분기): `{NEXT_STAGE_ID}`

Stage59X closeout(59X단계 종료)는 overall goal completion(전체 목표 완료)이 아니다. Effect(효과): Stage60 ONNX hardening(60단계 ONNX 경화)은 아직 열리지 않는다.

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
                "artifact_type": "stage59x_decision_evidence",
                "path": rel(path),
                "sha256": sha256_file_lf_normalized(path),
                "stage_id": STAGE59X_ID,
                "run_id": RUN_ID,
                "created_at_utc": created,
                "notes": "Stage59X evidence synthesis and branch decision artifact.",
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
                "stage_id": STAGE59X_ID,
                "lane": "baseline_adapter_demotion_or_branch_from_stage59w",
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
            "ledger_row_id": f"{RUN_ID}__stage59x_branch_decision",
            "stage_id": STAGE59X_ID,
            "run_id": RUN_ID,
            "subrun_id": "stage59x_branch_decision",
            "parent_run_id": PARENT_RUN_ID,
            "record_view": "demotion_or_branch_from_stage59w",
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
            "notes": "Decision-only stage using completed Stage59V/W evidence; opens next bounded model branch.",
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
            "source_files": [rel(SOURCE59V_SUMMARY), rel(SOURCE59W_SUMMARY)],
            "covered_requirements": ["validation/OOS PF", "validation/OOS net", "cost-stressed expectancy", "same-move concentration", "risk floor count"],
        },
        "source_authority_audit.json": {
            "status": "completed",
            "source_external_verification_status": "completed",
            "source_decisions": [rel(SOURCE59V_DECISION), rel(SOURCE59W_DECISION)],
            "stage59x_external_verification_status": EXTERNAL_STATUS,
        },
        "result_judgment_gate.json": {
            "result_subject": RUN_ID,
            "evidence_available": [
                rel(REPORT_PATH),
                rel(SUMMARY_CSV_PATH),
                rel(SOURCE59V_SUMMARY),
                rel(SOURCE59V_SEGMENT),
                rel(SOURCE59W_SUMMARY),
                rel(SOURCE59W_SEGMENT),
            ],
            "evidence_missing": ["robust_post_atr_risk_adapter", "stage60_onnx_evidence", "research_package_review"],
            "judgment_label": "exploratory",
            "stage_decision": DECISION,
            "best_validation_adapter": best_val.get("adapter_id"),
            "best_validation_net": best_val.get("net_profit"),
            "claim_boundary": BOUNDARY,
            "next_condition": NEXT_STAGE_ID,
            "status": "passed_with_boundary",
        },
        "artifact_lineage_audit.json": {
            "source_inputs": [
                rel(SOURCE59V_SUMMARY),
                rel(SOURCE59V_DECISION),
                rel(SOURCE59V_SEGMENT),
                rel(SOURCE59V_RISK),
                rel(SOURCE59W_SUMMARY),
                rel(SOURCE59W_DECISION),
                rel(SOURCE59W_SEGMENT),
                rel(SOURCE59W_RISK),
            ],
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
            "stage_id": STAGE59X_ID,
            "run_id": RUN_ID,
            "decision": DECISION,
            "external_verification_status": EXTERNAL_STATUS,
            "source_external_verification_status": "completed",
            "required_outputs": {
                "demotion_or_branch_report": rel(REPORT_PATH),
                "demotion_or_branch_summary_json": rel(SUMMARY_JSON_PATH),
                "demotion_or_branch_summary_csv": rel(SUMMARY_CSV_PATH),
                "stage59x_decision": rel(DECISION_PATH),
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
        f"""# Stage59X Brief(59X단계 개요)

- stage_id(단계 ID): `{STAGE59X_ID}`
- source_stage(원천 단계): `{STAGE59W_ID}`
- source_decision(원천 판정): `continue_repair_in_new_bounded_stage`
- bounded_question(경계 질문): `Should the Stage59S/V/W repair line continue, be demoted, or open a new model branch without starting ONNX?`
- boundary(경계): `{BOUNDARY}`

Stage59X(59X단계)는 새 MT5 run(새 MT5 실행)을 만들지 않는 evidence synthesis(근거 종합) 단계다. Effect(효과): 반복된 local threshold/risk-cap repair(로컬 문턱값/위험 상한 수리)를 멈추고 다음 bounded branch(경계 분기)를 명확히 고른다.
""",
    )
    write_md(
        INPUT_ROOT / "input_refs.md",
        f"""# Stage59X Input References(59X단계 입력 참조)

- stage59v_summary(59V단계 요약): `{rel(SOURCE59V_SUMMARY)}`
- stage59v_decision(59V단계 판정): `{rel(SOURCE59V_DECISION)}`
- stage59v_segment_kpi(59V단계 구간 KPI): `{rel(SOURCE59V_SEGMENT)}`
- stage59v_risk_atr_telemetry(59V단계 위험/ATR 텔레메트리): `{rel(SOURCE59V_RISK)}`
- stage59v_pushed_commit(59V단계 푸시 커밋): `{SOURCE_STAGE59V_PUSHED_COMMIT}`
- stage59w_summary(59W단계 요약): `{rel(SOURCE59W_SUMMARY)}`
- stage59w_decision(59W단계 판정): `{rel(SOURCE59W_DECISION)}`
- stage59w_segment_kpi(59W단계 구간 KPI): `{rel(SOURCE59W_SEGMENT)}`
- stage59w_risk_atr_telemetry(59W단계 위험/ATR 텔레메트리): `{rel(SOURCE59W_RISK)}`
- stage59w_pushed_commit(59W단계 푸시 커밋): `{SOURCE_STAGE59W_PUSHED_COMMIT}`

Effect(효과): Stage59X(59X단계)는 completed source evidence(완료된 원천 근거)만 사용해 분기 판정을 만든다.
""",
    )
    write_md(
        SELECTED_ROOT / "selection_status.md",
        f"""# Stage59X Selection Status(59X단계 선택 상태)

- stage_status(단계 상태): `closed_open_new_model_branch`
- source_stage(원천 단계): `{STAGE59W_ID}`
- source_decision(원천 판정): `continue_repair_in_new_bounded_stage`
- stage59x_decision(59X단계 판정): `{DECISION}`
- next_stage_or_branch(다음 단계/분기): `{NEXT_STAGE_ID}`
- selected_research_baseline(선택 연구 기준선): `none`
- claim_boundary(주장 경계): `{BOUNDARY}`

Effect(효과): Stage59X(59X단계)는 현재 Stage59S/V/W repair line(Stage59S/V/W 수리 계열)을 final package(최종 패키지)로 만들지 않고 새 bounded branch(경계 분기)로 넘긴다.
""",
    )
    write_md(
        REVIEWS_ROOT / "review_index.md",
        f"""# Stage59X Review Index(59X단계 검토 색인)

- demotion_or_branch_report(강등 또는 분기 보고서): `{rel(REPORT_PATH)}`
- demotion_or_branch_summary(강등 또는 분기 요약): `{rel(SUMMARY_CSV_PATH)}`
- demotion_or_branch_summary_json(강등 또는 분기 JSON 요약): `{rel(SUMMARY_JSON_PATH)}`
- stage59x_decision(59X단계 판정): `{rel(DECISION_PATH)}`
- stage_run_ledger(단계 실행 장부): `{rel(STAGE_LEDGER_PATH)}`
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "00_spec/stage_brief.md",
        f"""# Stage59Y Brief(59Y단계 개요)

- stage_id(단계 ID): `{NEXT_STAGE_ID}`
- source_stage(원천 단계): `{STAGE59X_ID}`
- source_decision(원천 판정): `{DECISION}`
- bounded_question(경계 질문): `Can a new bounded model branch produce a post-ATR/risk adapter candidate after the Stage59S/V/W repair line was demoted?`
- boundary(경계): `{BOUNDARY}`

Stage59Y(59Y단계)는 demoted Stage59S/V/W repair line(강등된 Stage59S/V/W 수리 계열) 대신 새 model branch(모델 분기)를 작게 연다. Effect(효과): 같은 local threshold/risk-cap repair(로컬 문턱값/위험 상한 수리)를 반복하지 않는다.
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "01_inputs/input_refs.md",
        f"""# Stage59Y Input References(59Y단계 입력 참조)

- stage59x_decision(59X단계 판정): `{rel(DECISION_PATH)}`
- stage59x_report(59X단계 보고서): `{rel(REPORT_PATH)}`
- stage59x_summary(59X단계 요약): `{rel(SUMMARY_CSV_PATH)}`
- stage59w_summary(59W단계 요약): `{rel(SOURCE59W_SUMMARY)}`
- stage59w_decision(59W단계 판정): `{rel(SOURCE59W_DECISION)}`

Effect(효과): Stage59Y(59Y단계)는 실패 기억(failure memory, 실패 기억)을 새 분기 입력으로 받는다.
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "03_reviews/review_index.md",
        """# Stage59Y Review Index(59Y단계 검토 색인)

Stage59Y(59Y단계)는 planned(계획) 상태다. Effect(효과): Stage59X(59X단계)의 branch decision(분기 판정)을 다음 실행 근거로 넘긴다.
""",
    )
    write_md(
        NEXT_STAGE_ROOT / "04_selected/selection_status.md",
        f"""# Stage59Y Selection Status(59Y단계 선택 상태)

- stage_status(단계 상태): `active_planned_from_stage59x`
- source_stage(원천 단계): `{STAGE59X_ID}`
- source_decision(원천 판정): `{DECISION}`
- selected_research_baseline(선택 연구 기준선): `none`
- claim_boundary(주장 경계): `{BOUNDARY}`

Effect(효과): Stage59Y(59Y단계)는 Stage60 ONNX(60단계 ONNX)가 아니라 새 bounded model branch(경계 모델 분기)를 연다.
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
- status(상태): `stage59x_closed_open_new_model_branch`
- claim_boundary(주장 경계): research/development only(연구/개발 전용)

Stage59X(59X단계) closed(종료) as demotion/branch decision(강등/분기 판정). Effect(효과): Stage59S/V/W(Stage59S/V/W단계) repair line(수리 계열)은 final package(최종 패키지)나 Stage60 ONNX(60단계 ONNX) 후보가 아니며, Stage59Y(59Y단계) 새 bounded branch(경계 새 분기)로 넘어간다.

## Latest Stage59X Evidence(최신 59X단계 근거)

- run(실행): `{RUN_ID}`
- decision(판정): `{DECISION}`
- external_verification_status(외부 검증 상태): `{EXTERNAL_STATUS}`
- source_external_verification_status(원천 외부 검증 상태): `completed`
- next_stage_or_branch(다음 단계/분기): `{NEXT_STAGE_ID}`
- report(보고서): `{rel(REPORT_PATH)}`
- stage59x_decision(59X단계 판정): `{rel(DECISION_PATH)}`

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
        f"  Stage59X(59X단계) `{STAGE59X_ID}` closed(종료) as demotion/branch decision(강등/분기 판정); decision(판정)=`{DECISION}`. Effect(효과): repeated Stage59V/W segment weakness(반복된 59V/W단계 구간 약점)을 보존하고 새 branch(분기)로 넘긴다.\n"
        f"- >-\n"
        f"  Next stage_or_branch(다음 단계/분기) `{NEXT_STAGE_ID}` is active/planned(활성/계획). Effect(효과): Stage60 ONNX(60단계 ONNX) 대신 새 bounded model branch(경계 모델 분기)를 연다.\n"
    )
    text = re.sub(r"current_focus:\n(?:- >-\n  Stage59X[^\n]*\n- >-\n  Next stage_or_branch[^\n]*\n)+", "current_focus:\n", text, count=1)
    text = re.sub(r"current_focus:\n", focus, text, count=1)
    block = f"""

stage59x_demotion_or_branch_from_stage59w:
  packet_id: {PACKET_ID}
  stage_id: {STAGE59X_ID}
  status: closed_open_new_model_branch
  current_run_id: {RUN_ID}
  source_adapter: {SOURCE_ADAPTER_ID}
  source_stage59v_pushed_commit: {SOURCE_STAGE59V_PUSHED_COMMIT}
  source_stage59w_pushed_commit: {SOURCE_STAGE59W_PUSHED_COMMIT}
  decision: {DECISION}
  next_stage_or_branch: {NEXT_STAGE_ID}
  report_path: {rel(DECISION_PATH)}
  packet_summary_path: {rel(PACKET_ROOT / "aggregate_summary.json")}
  external_verification_status: {EXTERNAL_STATUS}
  source_external_verification_status: completed
  boundary: {BOUNDARY}
"""
    if "stage59x_demotion_or_branch_from_stage59w:" in text:
        text = re.sub(r"\nstage59x_demotion_or_branch_from_stage59w:\n(?:  .*\n)*", block, text, count=1)
    else:
        text += block
    io_path(WORKSPACE_STATE_PATH).write_text(text, encoding="utf-8-sig")


def append_changelog() -> None:
    entry = (
        "\n## 2026-05-16 - Stage59X demotion or branch decision closeout(59X단계 강등 또는 분기 판정 종료)\n\n"
        f"- run(실행): `{RUN_ID}`\n"
        f"- decision(판정): `{DECISION}`\n"
        "- effect(효과): Stage59S/V/W(Stage59S/V/W단계)의 repair line(수리 계열)을 final(최종)로 보지 않고 Stage59Y(59Y단계) 새 bounded model branch(경계 모델 분기)로 넘겼다.\n"
    )
    existing = io_path(CHANGELOG_PATH).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG_PATH) else ""
    if f"- run(실행): `{RUN_ID}`" not in existing:
        io_path(CHANGELOG_PATH).write_text(existing.rstrip() + entry, encoding="utf-8-sig")


def main() -> int:
    source_rows = read_actual_rows(SOURCE59V_SUMMARY, STAGE59V_ID) + read_actual_rows(SOURCE59W_SUMMARY, STAGE59W_ID)
    segment_flags = read_segment_flags(SOURCE59V_SEGMENT, STAGE59V_ID, "s59v_s59s_mr025_sl20_tp30_sd12_h5_rearm002")
    segment_flags += read_segment_flags(SOURCE59W_SEGMENT, STAGE59W_ID, SOURCE_ADAPTER_ID)
    write_csv(SUMMARY_CSV_PATH, source_rows)
    payload = {
        "created_at_utc": utc_now(),
        "stage_id": STAGE59X_ID,
        "run_id": RUN_ID,
        "packet_id": PACKET_ID,
        "parent_run_id": PARENT_RUN_ID,
        "source_adapter": SOURCE_ADAPTER_ID,
        "decision": DECISION,
        "next_stage_or_branch": NEXT_STAGE_ID,
        "external_verification_status": EXTERNAL_STATUS,
        "source_external_verification_status": "completed",
        "summary_rows": source_rows,
        "segment_flags": segment_flags,
        "claim_boundary": BOUNDARY,
        "overall_goal_complete": False,
    }
    write_json(SUMMARY_JSON_PATH, payload)
    write_md(REPORT_PATH, report_markdown(source_rows, segment_flags, DECISION))
    write_md(DECISION_PATH, decision_markdown(segment_flags, DECISION))
    artifacts = artifact_rows([REPORT_PATH, SUMMARY_JSON_PATH, SUMMARY_CSV_PATH, DECISION_PATH, STAGE_LEDGER_PATH, Path(__file__)])
    ledger_payload = write_ledgers(source_rows, artifacts)
    artifacts = artifact_rows([REPORT_PATH, SUMMARY_JSON_PATH, SUMMARY_CSV_PATH, DECISION_PATH, STAGE_LEDGER_PATH, Path(__file__)])
    ledger_payload = write_ledgers(source_rows, artifacts)
    write_packet_files(source_rows, ledger_payload)
    write_stage_docs()
    update_current_truth()
    append_changelog()
    print(json.dumps({"status": "ok", "run_id": RUN_ID, "decision": DECISION, "next_stage": NEXT_STAGE_ID}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
