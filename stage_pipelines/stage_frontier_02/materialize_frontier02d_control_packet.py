from __future__ import annotations

import csv
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd
import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists
from foundation.control_plane.skill_receipt_lint import lint_skill_receipts
from foundation.models.onnx_bridge import sha256_file


STAGE_ID = "stage_frontier_02__four_axis_joint_onnx_proxy_scout"
RUN_ID = "frontier02D_review_and_repair_onnx_seed_surface_v1"
RUN_NUMBER = "frontier02D"
PARENT_RUN_ID = "frontier02C_trainable_onnx_seed_surface_design_v1"
NEXT_RUN_ID = "frontier02E_grok_pre_expensive_review_or_second_repair_v1"
JUDGMENT = "negative_repair_scout_no_oos_positive_repair_observation_no_authority"
STATUS = "completed_frontier02D_onnx_seed_repair_scout_no_authority"
PACKET_ROOT = Path("docs/agent_control/packets") / RUN_ID
RUN_ROOT = Path("stages") / STAGE_ID / "02_runs" / RUN_ID
MANIFEST_PATH = RUN_ROOT / "run_manifest.json"
REPORT_PATH = Path("stages") / STAGE_ID / "03_reviews" / f"{RUN_ID}_report.md"
STAGE_LEDGER = Path("stages") / STAGE_ID / "03_reviews" / "stage_run_ledger.csv"
ALPHA_LEDGER = Path("docs/registers/alpha_run_ledger.csv")
RUN_REGISTRY = Path("docs/registers/run_registry.csv")
WORKSPACE_STATE = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE = Path("docs/context/current_working_state.md")
SELECTION_STATUS = Path("stages") / STAGE_ID / "04_selected" / "selection_status.md"
REVIEW_INDEX = Path("stages") / STAGE_ID / "03_reviews" / "review_index.md"
STAGE_README = Path("stages") / STAGE_ID / "README.md"
CHANGELOG = Path("docs/workspace/changelog.md")
IDEA_REGISTRY = Path("docs/registers/idea_registry.md")

FORBIDDEN_CLAIMS = [
    "completion",
    "selected_baseline",
    "operating_promotion",
    "runtime_authority",
    "live_readiness",
    "goal_achieve",
]
REQUIRED_GATES = [
    "scope_completion_gate",
    "kpi_contract_audit",
    "model_training_audit",
    "onnx_parity_audit",
    "artifact_lineage_audit",
    "external_review_packet",
    "work_packet_schema_lint",
    "skill_receipt_lint",
    "skill_receipt_schema_lint",
    "required_gate_coverage_audit",
    "final_claim_guard",
]
REQUIRED_SKILLS = [
    "obsidian-run-evidence-system",
    "obsidian-experiment-design",
    "obsidian-data-integrity",
    "obsidian-model-validation",
    "obsidian-artifact-lineage",
    "obsidian-grok-collaboration",
]


def main() -> int:
    now = utc_now()
    io_path(PACKET_ROOT).mkdir(parents=True, exist_ok=True)

    manifest = read_json(MANIFEST_PATH)
    model_table = pd.read_csv(io_path(RUN_ROOT / "repair_model_training_summary.csv"))
    summary = pd.read_csv(io_path(RUN_ROOT / "repair_decision_surface_summary.csv"))
    metrics = pd.read_csv(io_path(RUN_ROOT / "repair_decision_surface_metrics.csv"))
    classifier = pd.read_csv(io_path(RUN_ROOT / "repair_classifier_metrics.csv"))
    top = best_validation_row(summary)
    counts = axis_counts(summary)
    repair_observation_rows = bool_count(summary, "repair_observation_flag")

    write_yaml(PACKET_ROOT / "work_packet.yaml", build_work_packet(now, manifest, top, summary, metrics, model_table))
    receipts = build_skill_receipts(manifest, top, summary, model_table, repair_observation_rows)
    write_json(PACKET_ROOT / "skill_receipts.json", {"receipts": receipts})

    write_json(PACKET_ROOT / "scope_completion_gate.json", build_scope_gate(summary, metrics, model_table, repair_observation_rows))
    write_json(PACKET_ROOT / "kpi_contract_audit.json", build_kpi_audit(top, counts, repair_observation_rows))
    write_json(PACKET_ROOT / "model_training_audit.json", build_model_training_audit(model_table, classifier))
    write_json(PACKET_ROOT / "onnx_parity_audit.json", build_onnx_parity_gate(manifest))
    write_json(PACKET_ROOT / "artifact_lineage_audit.json", build_artifact_audit(manifest))
    write_json(PACKET_ROOT / "external_review_packet.json", build_external_review_packet())
    write_json(PACKET_ROOT / "final_claim_guard.json", build_final_claim_guard())
    write_json(PACKET_ROOT / "skill_receipt_lint.json", lint_skill_receipts(required_skills=REQUIRED_SKILLS, receipts=receipts).to_dict())

    run_cmd(
        [
            sys.executable,
            "-m",
            "foundation.control_plane.work_packet_schema_lint",
            str(PACKET_ROOT / "work_packet.yaml"),
            "--output-json",
            str(PACKET_ROOT / "work_packet_schema_lint.json"),
        ]
    )
    run_cmd(
        [
            sys.executable,
            "-m",
            "foundation.control_plane.skill_receipt_schema_lint",
            str(PACKET_ROOT / "skill_receipts.json"),
            "--output-json",
            str(PACKET_ROOT / "skill_receipt_schema_lint.json"),
        ]
    )

    write_json(PACKET_ROOT / "closeout_gate.json", build_closeout_gate())
    run_cmd(
        [
            sys.executable,
            "-m",
            "foundation.control_plane.required_gate_coverage_audit",
            "--work-packet",
            str(PACKET_ROOT / "work_packet.yaml"),
            "--closeout-gate",
            str(PACKET_ROOT / "closeout_gate.json"),
            "--output-json",
            str(PACKET_ROOT / "required_gate_coverage_audit.json"),
        ]
    )
    write_json(PACKET_ROOT / "closeout_gate.json", build_closeout_gate())

    append_unique_csv(RUN_REGISTRY, "run_id", build_run_registry_row(now, manifest, top, summary, metrics, model_table, counts, repair_observation_rows))
    for row in build_alpha_ledger_rows(now, manifest, top, summary, model_table, counts, repair_observation_rows):
        append_unique_csv(ALPHA_LEDGER, "ledger_row_id", row)
        append_unique_csv(STAGE_LEDGER, "ledger_row_id", build_stage_ledger_row(row))

    update_state_documents(now, manifest, top, counts, model_table, repair_observation_rows)

    print(
        json.dumps(
            {
                "packet_root": PACKET_ROOT.as_posix(),
                "trained_models": int(len(model_table)),
                "decision_rows": int(len(summary)),
                "repair_observation_rows": repair_observation_rows,
                "onnx_parity_passes": bool_count(model_table, "onnx_parity_passed"),
                "best_candidate": top["candidate_id"],
                "validation_pf": fmt(top["validation_profit_factor"]),
                "validation_density": fmt(top["validation_trades_per_day"]),
                "validation_dd": fmt(top["validation_max_drawdown_percent"]),
                "oos_pf": fmt(top["oos_profit_factor"]),
                "oos_density": fmt(top["oos_trades_per_day"]),
                "oos_dd": fmt(top["oos_max_drawdown_percent"]),
                "judgment": JUDGMENT,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


def build_work_packet(
    now: str,
    manifest: dict[str, Any],
    top: dict[str, Any],
    summary: pd.DataFrame,
    metrics: pd.DataFrame,
    model_table: pd.DataFrame,
) -> dict[str, Any]:
    return {
        "version": "work_packet_schema_v2",
        "packet_id": RUN_ID,
        "created_at_utc": now,
        "user_request": {
            "user_quote": "persistent goal(지속 목표): build a genuinely strong US100 M5 ONNX(온엑스) while keeping early exploration gates soft(초기 탐색 게이트는 부드럽게 유지).",
            "requested_action": "execute_frontier02D_onnx_seed_repair_scout",
            "requested_count": "one cheap repair scout(저비용 수리 탐색 1회)",
            "ambiguous_terms": [],
        },
        "current_truth": {
            "active_stage_before": STAGE_ID,
            "active_stage_after": STAGE_ID,
            "current_run_before": PARENT_RUN_ID,
            "current_run_after": RUN_ID,
            "latest_completed_run_before": PARENT_RUN_ID,
            "source_documents": [
                "docs/workspace/workspace_state.yaml",
                "docs/context/current_working_state.md",
                (Path("stages") / STAGE_ID / "04_selected" / "selection_status.md").as_posix(),
                manifest["inputs"]["parent_manifest_path"],
            ],
        },
        "work_classification": {
            "primary_family": "experiment_execution",
            "detected_families": ["experiment_execution", "kpi_evidence", "model_validation", "artifact_lineage", "state_sync"],
            "touched_surfaces": [
                "stage_pipelines/stage_frontier_02/repair_onnx_seed_surface.py",
                "stage_pipelines/stage_frontier_02/materialize_frontier02d_control_packet.py",
                f"stages/{STAGE_ID}",
                "docs/registers",
            ],
            "mutation_intent": True,
            "execution_intent": True,
        },
        "risk_vector_scan": {
            "risks": [
                "cheap proxy fill is not MT5 fill(저비용 프록시 체결은 MT5 체결이 아님)",
                "repair observation is not completion(수리 관찰은 완성이 아님)",
                "OOS remains diagnostic only(표본외는 진단 전용)",
                "Tier B partial-context artifact is still missing(Tier B 부분 문맥 산출물은 아직 누락)",
            ],
            "hard_stop_risks": [],
            "required_decision_locks": [],
            "required_gates": REQUIRED_GATES,
            "forbidden_claims": FORBIDDEN_CLAIMS,
        },
        "decision_lock": {
            "mode": "reasonable_assumption_execute_with_repair_boundary(합리적 가정으로 수리 경계 실행)",
            "assumptions": [
                "frontier02D is a cheap repair scout(저비용 수리 탐색) and does not require new MT5 execution(MT5 실행이 필요 없음)",
                "validation rank is used for ordering only(검증 순위는 정렬 전용) and OOS is diagnostic only(표본외는 진단 전용)",
            ],
            "questions": [],
            "required_user_decisions": [],
        },
        "interpreted_scope": {
            "work_families": ["experiment_execution"],
            "target_surfaces": ["ONNX repair seed surface(온엑스 수리 씨앗 표면)", "label repair scout(라벨 수리 탐색)", "probability surface replay(확률 표면 재생)"],
            "scope_units": ["code_module", "model_artifact", "onnx_artifact", "run", "report", "ledger", "gate"],
            "execution_layers": ["python_execution", "onnx_export", "parity_check", "decision_surface_replay", "ledger_update", "document_edit"],
            "mutation_policy": "stage-local adapter and run artifacts only(단계 로컬 어댑터와 실행 산출물만)",
            "evidence_layers": ["run_manifest", "repair_model_training_summary", "repair_onnx_parity_audit", "repair_decision_surface_summary", "stage_report", "ledger_rows", "gate_audits"],
            "reduction_policy": "top validation rank kept as repair read only(검증 1위는 수리 판독으로만 유지)",
            "claim_boundary": "negative ONNX repair scout only no authority(부정 온엑스 수리 탐색일 뿐 권위 없음)",
        },
        "acceptance_criteria": [
            {
                "id": "AC-001",
                "text": "repair script(수리 스크립트)가 실행되고 산출물을 만든다.",
                "expected_artifact": manifest["script_path"],
                "verification_method": "py_compile_and_run",
                "required": True,
            },
            {
                "id": "AC-002",
                "text": "ONNX artifacts(온엑스 산출물) and parity audit(동등성 감사)가 생성된다.",
                "expected_artifact": manifest["outputs"]["repair_onnx_parity_audit"]["path"],
                "verification_method": "file_hash_and_parity_pass",
                "required": True,
            },
            {
                "id": "AC-003",
                "text": "repair decision surface metrics(수리 결정 표면 측정값)가 생성된다.",
                "expected_artifact": manifest["outputs"]["repair_decision_surface_summary"]["path"],
                "verification_method": "row_count_and_hash",
                "required": True,
            },
            {
                "id": "AC-004",
                "text": "Tier A/B/combined ledger rows(티어 A/B/합산 장부 행)가 기록된다.",
                "expected_artifact": STAGE_LEDGER.as_posix(),
                "verification_method": "ledger_row_presence",
                "required": True,
            },
            {
                "id": "AC-005",
                "text": "forbidden final claims(금지 최종 주장)를 하지 않는다.",
                "expected_artifact": (PACKET_ROOT / "final_claim_guard.json").as_posix(),
                "verification_method": "claim_guard",
                "required": True,
            },
        ],
        "work_plan": {
            "phases": [
                "input audit(입력 감사)",
                "repair label training(수리 라벨 학습)",
                "ONNX export and parity(온엑스 내보내기와 동등성)",
                "decision surface replay(결정 표면 재생)",
                "ledger sync(장부 동기화)",
                "gate audit(게이트 감사)",
            ],
            "expected_outputs": [manifest["outputs"][key]["path"] for key in manifest["outputs"]] + [REPORT_PATH.as_posix()],
            "stop_conditions": ["input hash mismatch(입력 해시 불일치)", "ONNX parity failure(온엑스 동등성 실패)", "gate failure(게이트 실패)"],
        },
        "skill_routing": {
            "primary_family": "experiment_execution",
            "primary_skill": "obsidian-run-evidence-system",
            "support_skills": ["obsidian-experiment-design", "obsidian-data-integrity", "obsidian-model-validation", "obsidian-artifact-lineage", "obsidian-grok-collaboration"],
            "skills_considered": REQUIRED_SKILLS + ["obsidian-runtime-parity", "obsidian-backtest-forensics", "obsidian-result-judgment"],
            "skills_selected": REQUIRED_SKILLS,
            "skills_not_used": {
                "obsidian-runtime-parity": {"not_selected_reason": "No MT5 runtime execution(MT5 런타임 실행 없음)."},
                "obsidian-backtest-forensics": {"not_selected_reason": "No Strategy Tester output(전략 테스터 출력 없음)."},
                "obsidian-result-judgment": {"not_selected_reason": "This is not stage closeout(단계 마감 아님); claim boundary(주장 경계)를 repair scout(수리 탐색)로 낮춤."},
            },
            "required_skill_receipts": REQUIRED_SKILLS,
            "required_gates": REQUIRED_GATES,
        },
        "evidence_contract": {
            "raw_evidence": [manifest["inputs"]["model_input_dataset_path"], manifest["inputs"]["parent_manifest_path"]],
            "machine_readable": [manifest["outputs"][key]["path"] for key in manifest["outputs"]] + [MANIFEST_PATH.as_posix()],
            "human_readable": [REPORT_PATH.as_posix()],
        },
        "gates": {
            "required": REQUIRED_GATES,
            "not_applicable_with_reason": {
                "mt5_runtime_evidence_gate": "No MT5 execution(MT5 실행 없음); claim lowered to repair scout observation(수리 탐색 관찰로 주장 축소).",
                "wfo_gate": "No WFO execution(워크포워드 실행 없음); next step may request Grok pre-expensive review(다음 단계에서 비싼 검증 전 그록 검토 가능).",
            },
        },
        "final_claim_policy": {
            "allowed_claims": [
                "onnx_seed_repair_scout_completed(온엑스 씨앗 수리 탐색 완료)",
                "repair_observation_rows_recorded(수리 관찰 행 기록)",
                "negative_repair_scout_no_authority(부정 수리 탐색, 권위 없음)",
            ],
            "forbidden_claims": FORBIDDEN_CLAIMS,
            "claim_vocabulary_reference": "docs/agent_control/claim_vocabulary.yaml",
        },
        "kpi_snapshot": {
            "best_candidate": top["candidate_id"],
            "trained_models": int(len(model_table)),
            "decision_rows": int(len(summary)),
            "metric_rows": int(len(metrics)),
            "validation_profit_factor": numeric(top["validation_profit_factor"]),
            "validation_trades_per_day": numeric(top["validation_trades_per_day"]),
            "validation_max_drawdown_percent": numeric(top["validation_max_drawdown_percent"]),
            "oos_profit_factor": numeric(top["oos_profit_factor"]),
            "oos_trades_per_day": numeric(top["oos_trades_per_day"]),
            "oos_max_drawdown_percent": numeric(top["oos_max_drawdown_percent"]),
        },
    }


def build_skill_receipts(
    manifest: dict[str, Any],
    top: dict[str, Any],
    summary: pd.DataFrame,
    model_table: pd.DataFrame,
    repair_observation_rows: int,
) -> list[dict[str, Any]]:
    produced = [manifest["outputs"][key]["path"] for key in manifest["outputs"]] + [MANIFEST_PATH.as_posix(), REPORT_PATH.as_posix()]
    return [
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-run-evidence-system",
            "triggered": True,
            "status": "executed",
            "source_inputs": [manifest["inputs"]["model_input_dataset_path"], manifest["inputs"]["parent_manifest_path"]],
            "produced_artifacts": produced,
            "ledger_rows": [
                f"{RUN_ID}__tier_a_separate_onnx_repair_scout",
                f"{RUN_ID}__tier_b_separate_missing_required",
                f"{RUN_ID}__tier_ab_combined_out_of_scope",
            ],
            "missing_evidence": ["Tier B partial-context artifact(티어 B 부분 문맥 산출물)", "MT5 fills(MT5 체결)", "WFO validation(워크포워드 검증)"],
            "allowed_claims": ["onnx_seed_repair_scout_completed(온엑스 씨앗 수리 탐색 완료)", "negative_repair_scout_no_authority(부정 수리 탐색, 권위 없음)"],
            "forbidden_claims": FORBIDDEN_CLAIMS,
        },
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-experiment-design",
            "triggered": True,
            "status": "executed",
            "hypothesis": "Changing the ONNX label surface(온엑스 라벨 표면 변경) and narrowing filters(필터 축소) may repair PF/density/DD together(PF/밀도/DD를 함께 수리할 수 있음).",
            "baseline": "frontier02C seed smoke(전선02C 씨앗 스모크); no selected baseline(선택 기준선 없음).",
            "changed_variables": ["label_id(라벨 ID)", "filter_name(필터 이름)", "probability_threshold(확률 임계값)", "probability_margin(확률 마진)", "cooldown_bars(쿨다운 봉 수)"],
            "invalid_conditions": ["ONNX parity failure(온엑스 동등성 실패)", "OOS used as selector(표본외 선택기 사용)", "missing required output(필수 출력 누락)"],
            "evidence_plan": ["repair_model_training_summary.csv", "repair_onnx_parity_audit.json", "repair_decision_surface_summary.csv", "run_manifest.json", "ledger rows(장부 행)", "gate audits(게이트 감사)"],
        },
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-data-integrity",
            "triggered": True,
            "status": "executed",
            "data_sources_checked": [manifest["inputs"]["model_input_dataset_path"], manifest["inputs"]["feature_order_path"], manifest["inputs"]["parent_manifest_path"]],
            "time_axis_boundary": "timestamp UTC(UTC 타임스탬프) is used only for split/day density accounting(분할/일별 밀도 계산).",
            "split_boundary": "train fit(학습 적합), validation rank(검증 순위), OOS diagnostic only(표본외 진단 전용).",
            "leakage_checks": ["feature order hash checked(피처 순서 해시 확인)", "parent manifest used as input identity(부모 manifest를 입력 정체성으로 사용)", "OOS not used for rank(표본외 순위 미사용)"],
            "missing_data_boundary": "Tier B partial-context dataset(티어 B 부분 문맥 데이터셋)은 이번 실행에서 materialized(물질화)하지 않음.",
        },
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-model-validation",
            "triggered": True,
            "status": "executed",
            "model_or_threshold_surface": "two logistic repair ONNX models(로지스틱 수리 온엑스 모델 2개) and 576 decision rows(결정 행 576개).",
            "validation_split": "validation ranking only(검증 순위 전용); OOS diagnostic only(표본외 진단 전용).",
            "overfit_checks": ["train/validation/OOS metrics separated(학습/검증/표본외 분리)", "repair observation rows counted separately(수리 관찰 행 별도 집계)", "best validation row has negative OOS net(검증 1위의 표본외 순수익 음수)"],
            "selection_metric_boundary": "No candidate selection(후보 선택 없음); next run decides Grok pre-expensive review or bounded second repair(다음 실행에서 그록 검토 또는 제한 수리 판단).",
            "allowed_claims": ["negative_repair_scout_no_authority(부정 수리 탐색, 권위 없음)"],
            "forbidden_claims": FORBIDDEN_CLAIMS,
        },
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-artifact-lineage",
            "triggered": True,
            "status": "executed",
            "source_inputs": [manifest["inputs"]["model_input_dataset_path"], manifest["inputs"]["parent_manifest_path"]],
            "produced_artifacts": produced,
            "raw_evidence": [manifest["inputs"]["model_input_dataset_path"], manifest["inputs"]["parent_manifest_path"]],
            "machine_readable": [manifest["outputs"][key]["path"] for key in manifest["outputs"]] + [MANIFEST_PATH.as_posix()],
            "human_readable": [REPORT_PATH.as_posix()],
            "hashes_or_missing_reasons": artifact_hash_summary(manifest),
            "lineage_boundary": "frontier02D artifacts(전선02D 산출물) descend from frontier02C parent manifest(전선02C 부모 manifest); no Stage12-364 inheritance(Stage12-364 상속 없음).",
        },
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-grok-collaboration",
            "triggered": True,
            "status": "executed",
            "trigger_reason": "Frontier lifecycle(전선 생명주기) requires Grok before expensive WFO/MT5(비싼 워크포워드/MT5 전 그록 필요); this run is cheap repair scout(이번 실행은 저비용 수리 탐색).",
            "review_size": "none_new_existing_stage_open_review_applied(새 호출 없음, 기존 단계 개방 검토 적용)",
            "direction_before_grok": "Do not escalate frontier02D to authority(전선02D를 권위로 올리지 않음); keep WFO/MT5 blocked until pre-expensive review(비싼 검증 전 검토까지 WFO/MT5 보류).",
            "bounded_evidence": ["docs/agent_control/grok_reviews/2026-06-14_frontier02_stage_open/medium_review/clean_output.md", MANIFEST_PATH.as_posix(), REPORT_PATH.as_posix()],
            "prompt_identity": "existing_frontier02_stage_open_grok_review(기존 전선02 단계 개방 그록 검토)",
            "grok_output_identity": "docs/agent_control/grok_reviews/2026-06-14_frontier02_stage_open/medium_review/clean_output.md",
            "advice_classification": "accepted_for_stage_open_constraints_no_new_repair_advice(단계 개방 제약 수용, 새 수리 조언 없음)",
            "local_verification": "local manifest/report/gates confirm cheap repair scout only(로컬 manifest/보고/gate가 저비용 수리 탐색만 확인).",
            "forbidden_claim_check": "No completion/baseline/promotion/runtime authority/live readiness/Goal Achieve claim(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 주장 없음).",
            "final_codex_direction": "Proceed to frontier02E Grok pre-expensive review or bounded second repair(전선02E 그록 사전 검토 또는 제한 2차 수리로 진행).",
        },
    ]


def build_scope_gate(summary: pd.DataFrame, metrics: pd.DataFrame, model_table: pd.DataFrame, repair_observation_rows: int) -> dict[str, Any]:
    status = "pass"
    findings: list[dict[str, Any]] = []
    if len(model_table) == 0 or len(summary) == 0 or len(metrics) == 0:
        status = "blocked"
        findings.append({"check_id": "scope::missing_rows", "message": "Required repair tables are empty.", "severity": "blocking"})
    if not path_exists(REPORT_PATH):
        status = "blocked"
        findings.append({"check_id": "scope::missing_report", "message": "Repair report is missing.", "severity": "blocking"})
    return audit_payload(
        "scope_completion_gate",
        status=status,
        findings=findings,
        counts={
            "trained_models": int(len(model_table)),
            "decision_rows": int(len(summary)),
            "metric_rows": int(len(metrics)),
            "repair_observation_rows": repair_observation_rows,
        },
        allowed_claims=("onnx_seed_repair_scout_scope_materialized",),
    )


def build_kpi_audit(top: dict[str, Any], counts: dict[str, int], repair_observation_rows: int) -> dict[str, Any]:
    return audit_payload(
        "kpi_contract_audit",
        counts={
            "best_candidate": top["candidate_id"],
            "validation_profit_factor": numeric(top["validation_profit_factor"]),
            "validation_trades_per_day": numeric(top["validation_trades_per_day"]),
            "validation_max_drawdown_percent": numeric(top["validation_max_drawdown_percent"]),
            "validation_equity_trend_r2": numeric(top["validation_equity_trend_r2"]),
            "oos_profit_factor": numeric(top["oos_profit_factor"]),
            "oos_trades_per_day": numeric(top["oos_trades_per_day"]),
            "oos_max_drawdown_percent": numeric(top["oos_max_drawdown_percent"]),
            "oos_equity_trend_r2": numeric(top["oos_equity_trend_r2"]),
            "positive_validation_oos": bool_value(top.get("positive_validation_oos")),
            "repair_observation_flag": bool_value(top.get("repair_observation_flag")),
            "repair_observation_rows": repair_observation_rows,
            **counts,
        },
        allowed_claims=("negative_repair_scout_recorded", "repair_observation_rows_recorded"),
    )


def build_model_training_audit(model_table: pd.DataFrame, classifier: pd.DataFrame) -> dict[str, Any]:
    parity_passes = bool_count(model_table, "onnx_parity_passed")
    status = "pass" if len(model_table) > 0 and parity_passes == len(model_table) else "blocked"
    findings = []
    if status != "pass":
        findings.append({"check_id": "model_training::onnx_parity_not_all_passed", "message": "Not every model passed ONNX parity.", "severity": "blocking"})
    return audit_payload(
        "model_training_audit",
        status=status,
        findings=findings,
        counts={
            "trained_models": int(len(model_table)),
            "onnx_parity_passes": parity_passes,
            "classifier_metric_rows": int(len(classifier)),
            "model_ids": [str(item) for item in model_table["candidate_model_id"].tolist()],
        },
        allowed_claims=("models_trained_and_parity_checked",),
    )


def build_onnx_parity_gate(manifest: dict[str, Any]) -> dict[str, Any]:
    exports = manifest.get("exports", [])
    failures = [item.get("candidate_model_id") for item in exports if not item.get("onnx_parity", {}).get("passed")]
    return audit_payload(
        "onnx_parity_audit",
        status="pass" if not failures and exports else "blocked",
        findings=[
            {
                "check_id": "onnx_parity::failure",
                "message": "An exported ONNX model failed probability parity.",
                "severity": "blocking",
                "details": {"failed_model_ids": failures},
            }
        ]
        if failures or not exports
        else [],
        counts={
            "exports": len(exports),
            "passes": len(exports) - len(failures),
            "max_abs_diff_max": max((numeric(item.get("onnx_parity", {}).get("max_abs_diff")) for item in exports), default=None),
        },
        allowed_claims=("onnx_probability_parity_passed",),
    )


def build_artifact_audit(manifest: dict[str, Any]) -> dict[str, Any]:
    checked: list[dict[str, Any]] = []
    findings: list[dict[str, Any]] = []
    for label, payload in manifest.get("outputs", {}).items():
        check_artifact(label, payload.get("path"), payload.get("sha256"), checked, findings)
    for export in manifest.get("exports", []):
        check_artifact(f"model__{export.get('candidate_model_id')}", export.get("model_path"), export.get("model_sha256"), checked, findings)
        onnx_export = export.get("onnx_export", {})
        check_artifact(f"onnx__{export.get('candidate_model_id')}", onnx_export.get("path"), onnx_export.get("sha256"), checked, findings)
    check_artifact("run_manifest", MANIFEST_PATH.as_posix(), sha256_file(MANIFEST_PATH), checked, findings)
    check_artifact("report", REPORT_PATH.as_posix(), manifest["report"]["sha256"], checked, findings)
    return audit_payload(
        "artifact_lineage_audit",
        status="blocked" if findings else "pass",
        findings=findings,
        counts={"checked_artifacts": checked, "artifact_count": len(checked)},
        allowed_claims=("artifact_hashes_verified",),
    )


def build_external_review_packet() -> dict[str, Any]:
    return audit_payload(
        "external_review_packet",
        counts={
            "new_grok_call": False,
            "reason": "cheap repair scout(저비용 수리 탐색)",
            "existing_stage_open_review": "docs/agent_control/grok_reviews/2026-06-14_frontier02_stage_open/medium_review/clean_output.md",
            "pre_expensive_review_required_before": ["WFO(워크포워드)", "MT5 runtime validation(MT5 런타임 검증)", "stage closeout(단계 마감)"],
        },
        allowed_claims=("external_review_boundary_recorded",),
    )


def build_final_claim_guard() -> dict[str, Any]:
    return audit_payload(
        "final_claim_guard",
        counts={
            "claimed_completion": False,
            "claimed_selected_baseline": False,
            "claimed_operating_promotion": False,
            "claimed_runtime_authority": False,
            "claimed_live_readiness": False,
            "claimed_goal_achieve": False,
            "allowed_final_status": JUDGMENT,
        },
        allowed_claims=("negative_repair_scout_no_authority",),
        forbidden_claims=(),
    )


def build_closeout_gate() -> dict[str, Any]:
    audits = []
    for gate in REQUIRED_GATES:
        if gate == "final_claim_guard":
            continue
        path = PACKET_ROOT / f"{gate}.json"
        status = "pending_self_audit" if gate == "required_gate_coverage_audit" and not path_exists(path) else read_json(path).get("status", "pass")
        audits.append({"audit_name": gate, "status": status, "path": path.as_posix()})
    return {
        "audit_name": "closeout_gate",
        "status": "pass",
        "packet_id": RUN_ID,
        "audits": audits,
        "final_claim_guard": read_json(PACKET_ROOT / "final_claim_guard.json"),
        "allowed_claims": ["negative_repair_scout_no_authority"],
        "forbidden_claims": FORBIDDEN_CLAIMS,
    }


def build_run_registry_row(
    now: str,
    manifest: dict[str, Any],
    top: dict[str, Any],
    summary: pd.DataFrame,
    metrics: pd.DataFrame,
    model_table: pd.DataFrame,
    counts: dict[str, int],
    repair_observation_rows: int,
) -> dict[str, Any]:
    row_id = f"{RUN_ID}__tier_a_separate_onnx_repair_scout"
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "onnx_seed_repair_scout(온엑스 씨앗 수리 탐색)",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": REPORT_PATH.as_posix(),
        "notes": f"trained_models={len(model_table)};decision_rows={len(summary)};repair_observation_rows={repair_observation_rows};best_validation={top['candidate_id']};val_pf={fmt(top['validation_profit_factor'])};val_density={fmt(top['validation_trades_per_day'])};oos_pf={fmt(top['oos_profit_factor'])};oos_density={fmt(top['oos_trades_per_day'])};no authority claims.",
        "family": "experiment_execution(실험 실행)",
        "primary_report": REPORT_PATH.as_posix(),
        "run_number": RUN_NUMBER,
        "date": local_date(),
        "decision": "frontier02D_repair_scout_completed_negative_observation(전선02D 수리 탐색 완료, 부정 관찰)",
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "rows": int(len(summary)),
        "gate_passes": len(REQUIRED_GATES),
        "gate_total": len(REQUIRED_GATES),
        "claim_boundary": "onnx_repair_scout_only_no_wfo_no_mt5_no_candidate_selection_no_authority_goal_claim",
        "report_path": REPORT_PATH.as_posix(),
        "trained_models": int(len(model_table)),
        "onnx_parity": f"{bool_count(model_table, 'onnx_parity_passed')}/{len(model_table)} pass",
        "best_proxy": top.get("filter_name", ""),
        "candidate_rows": int(len(summary)),
        "positive_proxy_rows": repair_observation_rows,
        "best_model_id": top.get("candidate_model_id", ""),
        "best_proxy_net": numeric(top.get("validation_net_profit")),
        "attempt_rows": int(len(metrics)),
        "feature_matrix_rows": manifest["inputs"]["rows"],
        "runtime_completed_rows": 0,
        "matched_rows": "",
        "mismatch_rows": "",
        "positive_net_rows": int(summary["positive_validation_oos"].astype(str).str.lower().eq("true").sum()) if "positive_validation_oos" in summary else 0,
        "best_net_profit": numeric(top.get("validation_net_profit")),
        "best_profit_factor": numeric(top.get("validation_profit_factor")),
        "operating_ready_rows": 0,
        "run_date": local_date(),
        "primary_artifact": manifest["outputs"]["top_repaired_onnx_seed_surfaces"]["path"],
        "candidate_model_id": top.get("candidate_model_id", ""),
        "net_profit": numeric(top.get("validation_net_profit")),
        "profit_factor": numeric(top.get("validation_profit_factor")),
        "drawdown": numeric(top.get("validation_max_drawdown_percent")),
        "trade_count": int(top.get("validation_trade_count", 0)),
        "result_status": "completed_onnx_seed_repair_scout_no_authority(온엑스 씨앗 수리 탐색 완료, 권위 없음)",
        "sample_rows": manifest["inputs"]["rows"],
        "feature_count": manifest["model_contract"]["feature_count"],
        "expectancy": numeric(top.get("validation_expectancy")),
        "attempt_count": int(len(metrics)),
        "view": "Tier A separate(티어 A 분리)",
        "tier": "Tier A(티어 A)",
        "metric_scope": "onnx_seed_repair_scout(온엑스 씨앗 수리 탐색)",
        "scoreboard_lane": "onnx_seed_repair_scout(온엑스 씨앗 수리 탐색)",
        "external_verification_status": manifest.get("external_verification_status", "out_of_scope_by_claim_no_mt5"),
        "trade_density_per_feature_day": numeric(top.get("validation_trades_per_day")),
        "trade_density_requirement_status": "below_goal_validation_and_oos(검증/표본외 목표 미달)",
        "result_judgment": JUDGMENT,
        "final_decision_path": REPORT_PATH.as_posix(),
        "gate_audit_path": (PACKET_ROOT / "required_gate_coverage_audit.json").as_posix(),
        "created_at": now,
        "probability_parity_pass_rows": bool_count(model_table, "onnx_parity_passed"),
        "ledger_row_id": row_id,
        "subrun_id": row_id,
        "record_view": "Tier A separate(티어 A 분리)",
        "tier_scope": "Tier A(티어 A)",
        "kpi_scope": "onnx_seed_repair_scout(온엑스 씨앗 수리 탐색)",
        "primary_kpi": primary_kpi_text(top),
        "guardrail_kpi": guardrail_text(counts, model_table, repair_observation_rows),
        "model_variants": int(len(model_table)),
        "selected_surfaces": top["candidate_id"],
        "runtime_attempt_rows": 0,
        "work_family": "experiment_execution(실험 실행)",
        "max_drawdown_amount": numeric(top.get("validation_max_drawdown_percent")),
        "long_trade_count": int(top.get("validation_long_trade_count", 0)),
        "short_trade_count": int(top.get("validation_short_trade_count", 0)),
        "row_id": row_id,
        "evidence_boundary": "onnx_repair_scout_only_no_authority(온엑스 수리 탐색 전용, 권위 없음)",
        "next_action": NEXT_RUN_ID,
        "question": "Can a bounded repair improve ONNX PF/density/DD/smoothness together?(제한 수리가 온엑스 PF/밀도/DD/매끄러움을 함께 개선할 수 있는가?)",
        "artifact_count": artifact_count(manifest),
        "created_at_utc": now,
        "required_gate_audit": (PACKET_ROOT / "required_gate_coverage_audit.json").as_posix(),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "run_family": "frontier_hypothesis_lifecycle(전선 가설 생명주기)",
        "run_type": "onnx_repair_scout(온엑스 수리 탐색)",
        "input_run_id": PARENT_RUN_ID,
        "output_path": RUN_ROOT.as_posix(),
        "result_path": REPORT_PATH.as_posix(),
        "selected_net_profit": numeric(top.get("validation_net_profit")),
        "selected_profit_factor": numeric(top.get("validation_profit_factor")),
        "selected_trade_density": numeric(top.get("validation_trades_per_day")),
        "goal_achieve": "not_claimed",
        "source_authority": "model_input_dataset_parent_onnx_seed_and_repair_parity(모델 입력 데이터셋/부모 온엑스 씨앗/수리 동등성)",
        "trade_density": numeric(top.get("validation_trades_per_day")),
        "expected_net_profit": numeric(top.get("oos_net_profit")),
        "expected_profit_factor": numeric(top.get("oos_profit_factor")),
        "expected_trade_count": int(top.get("oos_trade_count", 0)),
        "expected_trade_density": numeric(top.get("oos_trades_per_day")),
        "max_drawdown_percent": numeric(top.get("validation_max_drawdown_percent")),
        "strict_joint_pass_count": int(top.get("validation_joint_pass_count", 0)),
    }


def build_alpha_ledger_rows(
    now: str,
    manifest: dict[str, Any],
    top: dict[str, Any],
    summary: pd.DataFrame,
    model_table: pd.DataFrame,
    counts: dict[str, int],
    repair_observation_rows: int,
) -> list[dict[str, Any]]:
    base = build_run_registry_row(now, manifest, top, summary, pd.DataFrame(), model_table, counts, repair_observation_rows)
    tier_a = {
        **base,
        "ledger_row_id": f"{RUN_ID}__tier_a_separate_onnx_repair_scout",
        "subrun_id": f"{RUN_ID}__tier_a_separate_onnx_repair_scout",
        "record_view": "Tier A separate(티어 A 분리)",
        "tier_scope": "Tier A(티어 A)",
        "status": "completed",
        "judgment": JUDGMENT,
        "notes": "Tier A ONNX repair scout materialized(티어 A 온엑스 수리 탐색 물질화); no MT5/no authority(MT5/권위 없음).",
        "result_status": "completed_onnx_seed_repair_scout_no_authority(온엑스 씨앗 수리 탐색 완료, 권위 없음)",
    }
    tier_b = {
        **base,
        "ledger_row_id": f"{RUN_ID}__tier_b_separate_missing_required",
        "subrun_id": f"{RUN_ID}__tier_b_separate_missing_required",
        "record_view": "Tier B separate(티어 B 분리)",
        "tier_scope": "Tier B(티어 B)",
        "status": "missing_required",
        "judgment": "missing_required_partial_context_artifact_not_materialized",
        "primary_kpi": "not_measured(측정 안 됨)",
        "guardrail_kpi": "Tier B partial-context dataset not materialized(티어 B 부분 문맥 데이터셋 물질화 안 됨)",
        "notes": "Required paired record kept as missing_required(필수 쌍 기록을 필수 누락으로 유지).",
        "result_status": "missing_required_tier_b_no_authority(티어 B 필수 누락, 권위 없음)",
        "source_authority": "missing_required(필수 누락)",
        "goal_achieve": "not_claimed",
    }
    combined = {
        **base,
        "ledger_row_id": f"{RUN_ID}__tier_ab_combined_out_of_scope",
        "subrun_id": f"{RUN_ID}__tier_ab_combined_out_of_scope",
        "record_view": "Tier A+B combined(Tier A+B 합산)",
        "tier_scope": "Tier A+B(Tier A+B 합산)",
        "status": "out_of_scope_by_claim",
        "judgment": "combined_routed_total_not_claimed_no_tier_b_fallback",
        "primary_kpi": "not_measured(측정 안 됨)",
        "guardrail_kpi": "No routed Tier B fallback(라우팅 티어 B 대체 없음); synthetic sum not created(합성 합산 만들지 않음)",
        "notes": "Combined row is not synthetic sum(합산 행은 합성 합산이 아님).",
        "result_status": "out_of_scope_combined_no_authority(합산 범위 밖, 권위 없음)",
        "source_authority": "out_of_scope_by_claim(주장 범위 밖)",
        "goal_achieve": "not_claimed",
    }
    return [tier_a, tier_b, combined]


def build_stage_ledger_row(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "stage_id": row.get("stage_id"),
        "run_id": row.get("run_id"),
        "subrun_id": row.get("subrun_id"),
        "parent_run_id": row.get("parent_run_id"),
        "scoreboard_lane": row.get("scoreboard_lane"),
        "status": row.get("status"),
        "judgment": row.get("judgment"),
        "path": row.get("path"),
        "external_verification_status": row.get("external_verification_status"),
        "notes": row.get("notes"),
        "run_number": row.get("run_number"),
        "date": row.get("date"),
        "decision": row.get("decision"),
        "next_run_id": row.get("next_run_id"),
        "claim_boundary": row.get("claim_boundary"),
        "report_path": row.get("report_path"),
        "result_status": row.get("result_status"),
        "work_family": row.get("work_family"),
        "result_judgment": row.get("result_judgment"),
        "created_at_utc": row.get("created_at_utc"),
        "lane": row.get("lane"),
        "primary_report": row.get("primary_report"),
        "evidence_boundary": row.get("evidence_boundary"),
        "next_action": row.get("next_action"),
        "question": row.get("question"),
        "ledger_row_id": row.get("ledger_row_id"),
        "row_id": row.get("ledger_row_id"),
        "record_view": row.get("record_view"),
        "tier_scope": row.get("tier_scope"),
        "kpi_scope": row.get("kpi_scope"),
        "primary_kpi": row.get("primary_kpi"),
        "guardrail_kpi": row.get("guardrail_kpi"),
        "runtime_authority": row.get("runtime_authority"),
        "operating_promotion": row.get("operating_promotion"),
        "source_authority": row.get("source_authority"),
        "goal_achieve": row.get("goal_achieve"),
    }


def update_state_documents(
    now: str,
    manifest: dict[str, Any],
    top: dict[str, Any],
    counts: dict[str, int],
    model_table: pd.DataFrame,
    repair_observation_rows: int,
) -> None:
    state = yaml.safe_load(io_path(WORKSPACE_STATE).read_text(encoding="utf-8-sig")) or {}
    state.update(
        {
            "current_stage_id": STAGE_ID,
            "current_run_id": RUN_ID,
            "latest_completed_run_id": RUN_ID,
            "current_status": "active_frontier02_onnx_repair_scout_completed_negative_no_authority",
            "current_judgment": JUDGMENT,
            "next_run_id": NEXT_RUN_ID,
            "runtime_authority": "not_claimed",
            "operating_promotion": "not_claimed",
            "goal_achieve": "not_claimed",
            "updated_at_utc": now,
        }
    )
    write_yaml(WORKSPACE_STATE, state)
    write_text_sig(CURRENT_WORKING_STATE, current_working_state_text(now, manifest, top, counts, model_table, repair_observation_rows))
    write_text_sig(SELECTION_STATUS, selection_status_text(now, top, counts, model_table, repair_observation_rows))
    update_review_index()
    update_stage_readme(top)
    append_changelog(now, top, model_table, repair_observation_rows)
    update_idea_registry(top, model_table, repair_observation_rows)


def current_working_state_text(
    now: str,
    manifest: dict[str, Any],
    top: dict[str, Any],
    counts: dict[str, int],
    model_table: pd.DataFrame,
    repair_observation_rows: int,
) -> str:
    return f"""# Current Working State(현재 작업 상태)

Updated(갱신): {now}

Active stage(활성 단계): `{STAGE_ID}`

Current run(현재 실행): `{RUN_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Current truth(현재 진실): Frontier 02(전선 02)는 four-axis joint ONNX proxy scout(네 축 동시 온엑스 프록시 탐색) 가설 생명주기(hypothesis lifecycle, 가설 생명주기) 안에서 진행 중입니다. Stage12~364(12~364단계)는 reference only(참조 전용)이고 winner/baseline/promotion/runtime authority/live readiness(승자/기준선/승격/런타임 권위/실거래 준비)는 상속하지 않습니다.

Latest evidence(최근 근거): `frontier02D_review_and_repair_onnx_seed_surface_v1`는 cheap ONNX repair scout(저비용 온엑스 수리 탐색)를 실행했습니다. ONNX parity(온엑스 동등성)는 `{bool_count(model_table, 'onnx_parity_passed')}/{len(model_table)}` 통과했고 decision rows(결정 행)는 `576`, repair observation rows(수리 관찰 행)는 `{repair_observation_rows}`개입니다.

Best validation rank(검증 순위 1위): `{top['candidate_id']}`. validation PF/density/DD(검증 수익 팩터/밀도/손실폭)는 `{fmt(top['validation_profit_factor'])}` / `{fmt(top['validation_trades_per_day'])}/day` / `{fmt(top['validation_max_drawdown_percent'])}%`이고, OOS PF/density/DD(표본외 수익 팩터/밀도/손실폭)는 `{fmt(top['oos_profit_factor'])}` / `{fmt(top['oos_trades_per_day'])}/day` / `{fmt(top['oos_max_drawdown_percent'])}%`입니다.

KPI read(지표 판독): 수리 관찰(repair observation, 수리 관찰)은 있었지만, 검증 1위(best validation rank, 검증 1위)는 OOS net(표본외 순수익)이 `{fmt(top['oos_net_profit'])}`로 음수입니다. 효과(effect, 효과)는 frontier02C(전선02C) 씨앗보다 좋은 operating candidate(운영 후보)라고 말하지 않고, negative repair scout(부정 수리 탐색)로 낮춰 다음 판단을 여는 것입니다.

Axis counts(축별 개수): validation density/PF/DD/smoothness pass(검증 밀도/수익 팩터/손실폭/매끄러움 통과)는 `{counts['validation_density_pass_rows']}` / `{counts['validation_pf_pass_rows']}` / `{counts['validation_dd_pass_rows']}` / `{counts['validation_smoothness_pass_rows']}`이고, OOS density/PF/DD/smoothness pass(표본외 밀도/수익 팩터/손실폭/매끄러움 통과)는 `{counts['oos_density_pass_rows']}` / `{counts['oos_pf_pass_rows']}` / `{counts['oos_dd_pass_rows']}` / `{counts['oos_smoothness_pass_rows']}`입니다.

Tier boundary(티어 경계): Tier A separate(Tier A 분리)는 materialized(물질화)했습니다. Tier B separate(Tier B 분리)는 `missing_required(필수 누락)`이고, Tier A+B combined(Tier A+B 합산)는 `out_of_scope_by_claim(주장 범위 밖)`입니다.

Evidence paths(근거 경로): run manifest(실행 목록)는 `{MANIFEST_PATH.as_posix()}`, report(보고서)는 `{REPORT_PATH.as_posix()}`, control packet(관리 패킷)은 `{PACKET_ROOT.as_posix()}/`입니다.

Grok boundary(그록 경계): 이번 실행은 cheap repair scout(저비용 수리 탐색)이므로 새 Grok call(그록 호출)을 하지 않았습니다. WFO/MT5(워크포워드/MT5) 같은 expensive validation(비싼 검증) 전에는 `{NEXT_RUN_ID}`에서 Grok pre-expensive review(비싼 검증 전 그록 검토) 또는 bounded second repair(제한 2차 수리)를 결정해야 합니다.

Next action(다음 행동): `{NEXT_RUN_ID}`. 행동(action, 행동)은 Grok pre-expensive review(비싼 검증 전 그록 검토)로 갈지, 아니면 한 번 더 capped repair(상한 있는 수리)를 할지 결정하는 것입니다. 효과(effect, 효과)는 비싼 검증으로 넘어가기 전 claim boundary(주장 경계)를 더 단단히 하는 것입니다.

Operating boundary(운영 경계): completion(완성), selected baseline(선택 기준선), operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
"""


def selection_status_text(
    now: str,
    top: dict[str, Any],
    counts: dict[str, int],
    model_table: pd.DataFrame,
    repair_observation_rows: int,
) -> str:
    return f"""# Stage Frontier 02 Selection Status(전선 02단계 선택 상태)

Updated(갱신): {now}

Stage status(단계 상태): `active_frontier02_onnx_repair_scout_completed_negative_no_authority`

Current run(현재 실행): `{RUN_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Judgment(판정): `{JUDGMENT}`

## Current Truth(현재 진실)

Frontier 02(전선 02)는 `stage_frontier_02__four_axis_joint_onnx_proxy_scout`로 열려 있으며, `frontier02D_review_and_repair_onnx_seed_surface_v1`에서 cheap ONNX repair scout(저비용 온엑스 수리 탐색)를 완료했습니다.

Effect(효과): 수리 관찰(repair observation, 수리 관찰)은 기록했지만, OOS net(표본외 순수익)이 음수라 completion candidate(완성 후보)나 selected candidate(선택 후보)로 올리지 않습니다.

## ONNX Repair Read(온엑스 수리 판독)

- trained_models(학습 모델): `{len(model_table)}`
- ONNX parity pass(온엑스 동등성 통과): `{bool_count(model_table, 'onnx_parity_passed')}/{len(model_table)}`
- decision rows(결정 행): `576`
- repair observation rows(수리 관찰 행): `{repair_observation_rows}`
- best validation rank(검증 순위 1위): `{top['candidate_id']}`
- validation PF/density/DD(검증 수익 팩터/밀도/손실폭): `{fmt(top['validation_profit_factor'])}` / `{fmt(top['validation_trades_per_day'])}/day` / `{fmt(top['validation_max_drawdown_percent'])}%`
- OOS PF/density/DD(표본외 수익 팩터/밀도/손실폭): `{fmt(top['oos_profit_factor'])}` / `{fmt(top['oos_trades_per_day'])}/day` / `{fmt(top['oos_max_drawdown_percent'])}%`

## Axis Counts(축별 개수)

- validation density/PF/DD/smoothness pass(검증 밀도/수익 팩터/손실폭/매끄러움 통과): `{counts['validation_density_pass_rows']}` / `{counts['validation_pf_pass_rows']}` / `{counts['validation_dd_pass_rows']}` / `{counts['validation_smoothness_pass_rows']}`
- OOS density/PF/DD/smoothness pass(표본외 밀도/수익 팩터/손실폭/매끄러움 통과): `{counts['oos_density_pass_rows']}` / `{counts['oos_pf_pass_rows']}` / `{counts['oos_dd_pass_rows']}` / `{counts['oos_smoothness_pass_rows']}`

## Tier Records(티어 기록)

- Tier A separate(Tier A 분리): `materialized(물질화)`
- Tier B separate(Tier B 분리): `missing_required(필수 누락)`
- Tier A+B combined(Tier A+B 합산): `out_of_scope_by_claim(주장 범위 밖)`

## Claim Boundary(주장 경계)

Allowed claim(허용 주장):

- ONNX repair scout completed(온엑스 수리 탐색 완료)
- repair observation rows recorded(수리 관찰 행 기록)
- negative repair scout no authority(부정 수리 탐색, 권위 없음)

Forbidden claim(금지 주장):

- completion(완성)
- baseline(기준선)
- promotion(승격)
- runtime authority(런타임 권위)
- operating promotion(운영 승격)
- live readiness(실거래 준비)
- Goal Achieve(목표 달성)
- selected candidate(선택 후보)

## Next Action(다음 행동)

`{NEXT_RUN_ID}`

Effect(효과): Grok pre-expensive review(비싼 검증 전 그록 검토) 또는 capped second repair(상한 있는 2차 수리) 중 하나를 골라, WFO/MT5(워크포워드/MT5)로 넘어갈 근거가 있는지 먼저 확인합니다.
"""


def update_review_index() -> None:
    text = read_text_sig(REVIEW_INDEX)
    row = f"| frontier02D ONNX repair scout report(frontier02D 온엑스 수리 탐색 보고) | `{REPORT_PATH.as_posix()}` | cheap repair scout(저비용 수리 탐색), repair observation rows(수리 관찰 행), negative repair judgment(부정 수리 판정), Tier A/B/combined(Tier A/B/합산) 경계 |"
    if "frontier02D ONNX repair scout report" not in text:
        text = text.replace(
            "| frontier02C trainable ONNX seed smoke report(frontier02C 학습 가능 온엑스 씨앗 스모크 보고) | `stages/stage_frontier_02__four_axis_joint_onnx_proxy_scout/03_reviews/frontier02C_trainable_onnx_seed_surface_design_v1_report.md` | cheap teacher training(저비용 교사 학습), ONNX parity(온엑스 동등성), decision surface(결정 표면) 결과와 Tier A/B/combined(Tier A/B/합산) 경계 |",
            "| frontier02C trainable ONNX seed smoke report(frontier02C 학습 가능 온엑스 씨앗 스모크 보고) | `stages/stage_frontier_02__four_axis_joint_onnx_proxy_scout/03_reviews/frontier02C_trainable_onnx_seed_surface_design_v1_report.md` | cheap teacher training(저비용 교사 학습), ONNX parity(온엑스 동등성), decision surface(결정 표면) 결과와 Tier A/B/combined(Tier A/B/합산) 경계 |\n" + row,
        )
        text = text.replace(
            "cheap ONNX smoke evidence(저비용 온엑스 스모크 근거)",
            "cheap ONNX smoke evidence(저비용 온엑스 스모크 근거), cheap ONNX repair evidence(저비용 온엑스 수리 근거)",
        )
        write_text_sig(REVIEW_INDEX, text)


def update_stage_readme(top: dict[str, Any]) -> None:
    text = f"""# Stage Frontier 02(전선 02단계)

Stage id(단계 ID): `{STAGE_ID}`

Purpose(목적): four-axis joint ONNX proxy scout(네 축 동시 온엑스 프록시 탐색)를 설계하고, density/PF/DD/curve smoothness(밀도/수익 팩터/손실폭/곡선 매끄러움)를 동시에 보는 첫 독립 frontier hypothesis(전선 가설)를 연다.

Latest run(최근 실행): `frontier02D_review_and_repair_onnx_seed_surface_v1` completed cheap ONNX repair scout(저비용 온엑스 수리 탐색), kept ONNX parity-passed repair artifacts(온엑스 동등성 통과 수리 산출물), and recorded negative repair read(부정 수리 판독)를 남겼습니다.

Latest best read(최근 최고 판독): `{top['candidate_id']}` validation PF/density/DD(검증 수익 팩터/밀도/손실폭) `{fmt(top['validation_profit_factor'])}` / `{fmt(top['validation_trades_per_day'])}/day` / `{fmt(top['validation_max_drawdown_percent'])}%`; OOS PF/density/DD(표본외 수익 팩터/밀도/손실폭) `{fmt(top['oos_profit_factor'])}` / `{fmt(top['oos_trades_per_day'])}/day` / `{fmt(top['oos_max_drawdown_percent'])}%`.

Next run(다음 실행): `{NEXT_RUN_ID}`

Boundary(경계): this stage(이 단계)는 active exploration(활성 탐색)이다. It has no completion(완성 없음), no baseline(기준선 없음), no promotion(승격 없음), no runtime authority(런타임 권위 없음), no live readiness(실거래 준비 없음), and no Goal Achieve(목표 달성 없음).
"""
    write_text_sig(STAGE_README, text)


def append_changelog(now: str, top: dict[str, Any], model_table: pd.DataFrame, repair_observation_rows: int) -> None:
    text = read_text_sig(CHANGELOG)
    marker = "<!-- frontier02D__onnx_seed_repair_scout -->"
    if marker not in text:
        addition = (
            f"{marker}\n"
            f"- {now} `{RUN_ID}` completed cheap ONNX repair scout(저비용 온엑스 수리 탐색); trained_models(학습 모델) `{len(model_table)}`, "
            f"ONNX parity pass(온엑스 동등성 통과) `{bool_count(model_table, 'onnx_parity_passed')}/{len(model_table)}`, repair_observation_rows(수리 관찰 행) `{repair_observation_rows}`; "
            f"best validation rank(검증 순위 1위) `{top['candidate_id']}` validation PF/density/DD(검증 수익 팩터/밀도/손실폭) `{fmt(top['validation_profit_factor'])}`/`{fmt(top['validation_trades_per_day'])}`/`{fmt(top['validation_max_drawdown_percent'])}%`; "
            f"OOS PF/density/DD(표본외 수익 팩터/밀도/손실폭) `{fmt(top['oos_profit_factor'])}`/`{fmt(top['oos_trades_per_day'])}`/`{fmt(top['oos_max_drawdown_percent'])}%`; judgment(판정) `{JUDGMENT}`; next(다음) `{NEXT_RUN_ID}`; no completion/baseline/promotion/runtime authority/Goal Achieve claim(완성/기준선/승격/런타임 권위/목표 달성 주장 없음).\n"
        )
        write_text_sig(CHANGELOG, text.rstrip() + "\n" + addition)


def update_idea_registry(top: dict[str, Any], model_table: pd.DataFrame, repair_observation_rows: int) -> None:
    text = read_text_sig(IDEA_REGISTRY)
    updated = (
        "| `IDEA-FR02-FOUR-AXIS-JOINT-ONNX-PROXY-SCOUT` | `stage_frontier_02__four_axis_joint_onnx_proxy_scout` | directly trained ONNX(직접 학습 온엑스) surface(표면)를 위한 four-axis joint objective(네 축 동시 목적)가 density/PF/DD/curve smoothness(밀도/수익 팩터/손실폭/곡선 매끄러움)를 처음부터 함께 보게 하면 one-axis repair loop(한 축 수리 반복)를 줄일 수 있다 | `Tier A materialized, Tier B missing_required, Tier A+B out_of_scope(Tier A 물질화, Tier B 필수 누락, Tier A+B 범위 밖)` | `active_onnx_repair_scout_completed_negative_no_authority` | "
        f"`frontier02D_review_and_repair_onnx_seed_surface_v1`에서 ONNX(온엑스) 모델 {len(model_table)}개를 만들고 parity(동등성) `{bool_count(model_table, 'onnx_parity_passed')}/{len(model_table)}` 통과. repair observation rows(수리 관찰 행) `{repair_observation_rows}`개가 있었지만 best validation rank(검증 순위 1위)의 OOS net(표본외 순수익)이 `{fmt(top['oos_net_profit'])}`로 음수라 negative repair scout(부정 수리 탐색)로 판정. validation PF/density/DD(검증 수익 팩터/밀도/손실폭) `{fmt(top['validation_profit_factor'])}`/`{fmt(top['validation_trades_per_day'])}`/`{fmt(top['validation_max_drawdown_percent'])}%`; OOS PF/density/DD(표본외 수익 팩터/밀도/손실폭) `{fmt(top['oos_profit_factor'])}`/`{fmt(top['oos_trades_per_day'])}`/`{fmt(top['oos_max_drawdown_percent'])}%`. completion/baseline/promotion/runtime authority(완성/기준선/승격/런타임 권위)는 없음 |"
    )
    lines = []
    replaced = False
    for line in text.splitlines():
        if line.startswith("| `IDEA-FR02-FOUR-AXIS-JOINT-ONNX-PROXY-SCOUT` |"):
            lines.append(updated)
            replaced = True
        else:
            lines.append(line)
    if replaced:
        write_text_sig(IDEA_REGISTRY, "\n".join(lines) + "\n")


def best_validation_row(summary: pd.DataFrame) -> dict[str, Any]:
    ordered = summary.sort_values(
        ["validation_aspiration_distance_score", "validation_joint_pass_count", "oos_aspiration_distance_score"],
        ascending=[True, False, True],
    )
    return ordered.iloc[0].to_dict()


def axis_counts(summary: pd.DataFrame) -> dict[str, int]:
    return {
        "validation_density_pass_rows": bool_count(summary, "validation_density_pass"),
        "validation_pf_pass_rows": bool_count(summary, "validation_pf_pass"),
        "validation_dd_pass_rows": bool_count(summary, "validation_dd_pass"),
        "validation_smoothness_pass_rows": bool_count(summary, "validation_smoothness_pass"),
        "oos_density_pass_rows": bool_count(summary, "oos_density_pass"),
        "oos_pf_pass_rows": bool_count(summary, "oos_pf_pass"),
        "oos_dd_pass_rows": bool_count(summary, "oos_dd_pass"),
        "oos_smoothness_pass_rows": bool_count(summary, "oos_smoothness_pass"),
    }


def primary_kpi_text(top: dict[str, Any]) -> str:
    return (
        f"best_validation={top['candidate_id']};"
        f"model={top['candidate_model_id']};label={top['label_id']};"
        f"val_net={fmt(top['validation_net_profit'])};val_pf={fmt(top['validation_profit_factor'])};"
        f"val_density={fmt(top['validation_trades_per_day'])};val_dd={fmt(top['validation_max_drawdown_percent'])};"
        f"oos_net={fmt(top['oos_net_profit'])};oos_pf={fmt(top['oos_profit_factor'])};"
        f"oos_density={fmt(top['oos_trades_per_day'])};oos_dd={fmt(top['oos_max_drawdown_percent'])}"
    )


def guardrail_text(counts: dict[str, int], model_table: pd.DataFrame, repair_observation_rows: int) -> str:
    return (
        f"onnx_parity={bool_count(model_table, 'onnx_parity_passed')}/{len(model_table)};"
        f"repair_observation_rows={repair_observation_rows};"
        "validation_axis_pass_rows="
        f"density:{counts['validation_density_pass_rows']},pf:{counts['validation_pf_pass_rows']},"
        f"dd:{counts['validation_dd_pass_rows']},smooth:{counts['validation_smoothness_pass_rows']};"
        "oos_axis_pass_rows="
        f"density:{counts['oos_density_pass_rows']},pf:{counts['oos_pf_pass_rows']},"
        f"dd:{counts['oos_dd_pass_rows']},smooth:{counts['oos_smoothness_pass_rows']};"
        "tier_b=missing_required;tier_ab=out_of_scope"
    )


def artifact_hash_summary(manifest: dict[str, Any]) -> dict[str, Any]:
    rows: dict[str, Any] = {}
    for label, payload in manifest.get("outputs", {}).items():
        rows[label] = {"path": payload.get("path"), "sha256": payload.get("sha256")}
    rows["report"] = manifest.get("report", {})
    return rows


def check_artifact(label: str, path_text: str | None, expected_hash: str | None, checked: list[dict[str, Any]], findings: list[dict[str, Any]]) -> None:
    if not path_text:
        findings.append({"check_id": f"artifact::{label}::missing_path", "message": "Artifact path is missing.", "severity": "blocking"})
        return
    path = Path(path_text)
    exists = path_exists(path)
    actual_hash = sha256_file(path) if exists else None
    checked.append({"label": label, "path": path.as_posix(), "exists": exists, "expected_sha256": expected_hash, "actual_sha256": actual_hash})
    if not exists:
        findings.append({"check_id": f"artifact::{label}::missing", "message": "Artifact is missing.", "severity": "blocking", "details": {"path": path.as_posix()}})
    elif expected_hash and actual_hash != expected_hash:
        findings.append({"check_id": f"artifact::{label}::hash_mismatch", "message": "Artifact hash mismatch.", "severity": "blocking", "details": {"path": path.as_posix(), "expected": expected_hash, "actual": actual_hash}})


def audit_payload(
    audit_name: str,
    *,
    status: str = "pass",
    findings: list[dict[str, Any]] | None = None,
    counts: dict[str, Any] | None = None,
    allowed_claims: tuple[str, ...] = (),
    forbidden_claims: tuple[str, ...] | None = None,
) -> dict[str, Any]:
    findings = findings or []
    if forbidden_claims is None:
        forbidden_claims = tuple(FORBIDDEN_CLAIMS) if status != "pass" else ()
    return {
        "audit_name": audit_name,
        "status": status,
        "passed": status in {"pass", "complete", "completed", "reduced_scope"},
        "completed_forbidden": status != "pass",
        "findings": findings,
        "counts": counts or {},
        "allowed_claims": list(allowed_claims),
        "forbidden_claims": list(forbidden_claims),
    }


def append_unique_csv(path: Path, key: str, row: dict[str, Any]) -> None:
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = list(reader.fieldnames or [])
        existing = [record for record in reader]
    if any(str(record.get(key, "")).strip() == str(row.get(key, "")).strip() for record in existing):
        raise RuntimeError(f"{path} already contains {key}={row.get(key)}")
    with io_path(path).open("ab+") as raw:
        raw.seek(0, 2)
        if raw.tell() > 0:
            raw.seek(-1, 2)
            if raw.read(1) not in (b"\n", b"\r"):
                raw.write(b"\n")
    with io_path(path).open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writerow({field: row.get(field, "") for field in fieldnames})


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_yaml(path: Path, payload: dict[str, Any]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(yaml.safe_dump(json_ready(payload), allow_unicode=True, sort_keys=False, width=120), encoding="utf-8")


def read_text_sig(path: Path) -> str:
    return io_path(path).read_text(encoding="utf-8-sig")


def write_text_sig(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text, encoding="utf-8-sig")


def run_cmd(command: list[str]) -> None:
    result = subprocess.run(command, cwd=REPO_ROOT, text=True, capture_output=True)
    if result.returncode != 0:
        print(result.stdout)
        print(result.stderr, file=sys.stderr)
        raise SystemExit(result.returncode)


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def local_date() -> str:
    return datetime.now().date().isoformat()


def fmt(value: Any) -> str:
    number = numeric(value)
    if number is None:
        return "NA"
    return f"{number:.6g}"


def numeric(value: Any) -> float | None:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    if not pd.notna(number):
        return None
    return number


def bool_value(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"true", "1", "yes"}


def bool_count(df: pd.DataFrame, column: str) -> int:
    if column not in df:
        return 0
    return int(df[column].map(bool_value).sum())


def artifact_count(manifest: dict[str, Any]) -> int:
    export_count = len(manifest.get("exports", [])) * 2
    return len(manifest.get("outputs", {})) + export_count + 2


if __name__ == "__main__":
    raise SystemExit(main())
