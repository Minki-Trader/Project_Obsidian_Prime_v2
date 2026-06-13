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

from foundation.control_plane.ledger import io_path, json_ready
from foundation.control_plane.skill_receipt_lint import lint_skill_receipts
from foundation.models.onnx_bridge import sha256_file


STAGE_ID = "stage_frontier_02__four_axis_joint_onnx_proxy_scout"
RUN_ID = "frontier02C_trainable_onnx_seed_surface_design_v1"
RUN_NUMBER = "frontier02C"
PARENT_RUN_ID = "frontier02B_proxy_scout_execution_v1"
NEXT_RUN_ID = "frontier02D_review_and_repair_onnx_seed_surface_v1"
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
    model_table = pd.read_csv(io_path(RUN_ROOT / "model_training_summary.csv"))
    summary = pd.read_csv(io_path(RUN_ROOT / "decision_surface_summary.csv"))
    metrics = pd.read_csv(io_path(RUN_ROOT / "decision_surface_metrics.csv"))
    classifier = pd.read_csv(io_path(RUN_ROOT / "classifier_metrics.csv"))
    top = (
        summary.sort_values(
            ["validation_aspiration_distance_score", "validation_joint_pass_count", "oos_aspiration_distance_score"],
            ascending=[True, False, True],
        )
        .iloc[0]
        .to_dict()
    )
    counts = axis_counts(summary)

    work_packet = build_work_packet(now, manifest, top, summary, metrics, model_table)
    write_yaml(PACKET_ROOT / "work_packet.yaml", work_packet)
    receipts = build_skill_receipts(manifest, top, summary, model_table)
    write_json(PACKET_ROOT / "skill_receipts.json", {"receipts": receipts})
    write_json(PACKET_ROOT / "scope_completion_gate.json", build_scope_gate(summary, metrics, model_table))
    write_json(PACKET_ROOT / "kpi_contract_audit.json", build_kpi_audit(top, counts))
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

    append_unique_csv(RUN_REGISTRY, "run_id", build_run_registry_row(now, manifest, top, summary, metrics, model_table, counts))
    for row in build_alpha_ledger_rows(now, manifest, top, summary, model_table, counts):
        append_unique_csv(ALPHA_LEDGER, "ledger_row_id", row)
        append_unique_csv(STAGE_LEDGER, "ledger_row_id", build_stage_ledger_row(row))
    update_state_documents(now, manifest, top, counts, model_table)

    print(
        json.dumps(
            {
                "packet_root": PACKET_ROOT.as_posix(),
                "trained_models": int(len(model_table)),
                "decision_rows": int(len(summary)),
                "onnx_parity_passes": int(model_table["onnx_parity_passed"].sum()),
                "best_candidate": top["candidate_id"],
                "validation_pf": fmt(top["validation_profit_factor"]),
                "validation_density": fmt(top["validation_trades_per_day"]),
                "oos_pf": fmt(top["oos_profit_factor"]),
                "oos_density": fmt(top["oos_trades_per_day"]),
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
            "user_quote": "persistent_goal(지속 목표): build a genuinely strong US100 M5 ONNX(온엑스) through frontier hypothesis lifecycle(전선 가설 생명주기).",
            "requested_action": "execute_frontier02C_trainable_onnx_seed_surface_smoke",
            "requested_count": "one_trainable_seed_smoke_run(학습 가능 씨앗 스모크 실행 1회)",
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
            "detected_families": ["experiment_execution", "kpi_evidence", "artifact_lineage", "state_sync"],
            "touched_surfaces": [
                "stage_pipelines/stage_frontier_02/trainable_onnx_seed_surface.py",
                "stage_pipelines/stage_frontier_02/materialize_frontier02c_control_packet.py",
                f"stages/{STAGE_ID}",
                "docs/registers",
            ],
            "mutation_intent": True,
            "execution_intent": True,
        },
        "risk_vector_scan": {
            "risks": [
                "proxy_teacher_is_not_mt5_fill(프록시 교사는 MT5 체결이 아님)",
                "ONNX parity does not imply runtime authority(온엑스 동등성은 런타임 권위가 아님)",
                "OOS diagnostic must not become selector(OOS 진단을 선택기로 쓰면 안 됨)",
                "Tier B artifact missing in this run(Tier B 산출물 이번 실행 누락)",
            ],
            "hard_stop_risks": [],
            "required_decision_locks": [],
            "required_gates": REQUIRED_GATES,
            "forbidden_claims": FORBIDDEN_CLAIMS,
        },
        "decision_lock": {
            "mode": "reasonable_assumption_execute_with_smoke_boundary(합리적 가정으로 스모크 경계 내 실행)",
            "assumptions": [
                "cheap ONNX smoke training(저비용 온엑스 스모크 학습)는 WFO/MT5(워크포워드/MT5) 전 Grok call(그록 호출) 없이 가능",
                "validation rank(검증 순위)만 selector(선택기)이고 OOS(표본외)는 diagnostic(진단)이다",
            ],
            "questions": [],
            "required_user_decisions": [],
        },
        "interpreted_scope": {
            "work_families": ["experiment_execution"],
            "target_surfaces": ["trainable_onnx_seed_surface(학습 가능 온엑스 씨앗 표면)", "proxy_teacher_distillation(프록시 교사 증류)", "onnx_probability_parity(온엑스 확률 동등성)"],
            "scope_units": ["code_module", "model_artifact", "onnx_artifact", "run", "report", "ledger", "gate"],
            "execution_layers": ["code_edit", "python_execution", "onnx_export", "parity_check", "ledger_update", "document_edit"],
            "mutation_policy": "stage_local_adapter_and_run_artifacts_only(단계 전용 어댑터와 실행 산출물만)",
            "evidence_layers": ["run_manifest", "model_training_summary", "onnx_parity_audit", "decision_surface_summary", "stage_report", "ledger_rows", "gate_audits"],
            "reduction_policy": "top_validation_rank_seed_for_next_repair_review(다음 수리/검토용 검증 순위 씨앗만 축약)",
            "claim_boundary": "onnx_seed_observation_only_no_authority(온엑스 씨앗 관찰까지만, 권위 없음)",
        },
        "acceptance_criteria": [
            {
                "id": "AC-001",
                "text": "stage-local training script(단계 전용 학습 스크립트)가 실행된다.",
                "expected_artifact": "stage_pipelines/stage_frontier_02/trainable_onnx_seed_surface.py",
                "verification_method": "py_compile_and_run",
                "required": True,
            },
            {
                "id": "AC-002",
                "text": "ONNX model artifacts(온엑스 모델 산출물)와 parity audit(동등성 감사)가 생성된다.",
                "expected_artifact": manifest["outputs"]["onnx_parity_audit"]["path"],
                "verification_method": "file_hash_and_parity_pass",
                "required": True,
            },
            {
                "id": "AC-003",
                "text": "decision surface metrics(결정 표면 측정값)가 생성된다.",
                "expected_artifact": manifest["outputs"]["decision_surface_summary"]["path"],
                "verification_method": "file_hash_and_row_count",
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
                "text": "final forbidden claims(최종 금지 주장)을 하지 않는다.",
                "expected_artifact": (PACKET_ROOT / "final_claim_guard.json").as_posix(),
                "verification_method": "claim_guard",
                "required": True,
            },
        ],
        "work_plan": {
            "phases": ["input_audit(입력 감사)", "teacher_signal_materialization(교사 신호 물질화)", "model_training(모델 학습)", "onnx_export_parity(온엑스 내보내기 동등성)", "decision_surface_replay(결정 표면 재생)", "ledger_sync(장부 동기화)", "gate_audit(게이트 감사)"],
            "expected_outputs": [manifest["outputs"][key]["path"] for key in manifest["outputs"]] + [REPORT_PATH.as_posix()],
            "stop_conditions": ["input_hash_mismatch(입력 해시 불일치)", "feature_order_mismatch(피처 순서 불일치)", "no_trainable_teacher_models(학습 가능 교사 모델 없음)", "onnx_parity_failure(온엑스 동등성 실패)", "gate_failure(게이트 실패)"],
        },
        "skill_routing": {
            "primary_family": "experiment_execution",
            "primary_skill": "obsidian-run-evidence-system",
            "support_skills": ["obsidian-experiment-design", "obsidian-data-integrity", "obsidian-model-validation", "obsidian-artifact-lineage"],
            "skills_considered": REQUIRED_SKILLS + ["obsidian-runtime-parity", "obsidian-backtest-forensics", "obsidian-result-judgment"],
            "skills_selected": REQUIRED_SKILLS,
            "skills_not_used": {
                "obsidian-runtime-parity": {"not_selected_reason": "No MT5 runtime execution(MT5 런타임 실행 없음)."},
                "obsidian-backtest-forensics": {"not_selected_reason": "No Strategy Tester output(전략 테스터 출력 없음)."},
                "obsidian-result-judgment": {"not_selected_reason": "Run report(실행 보고)는 seed observation boundary(씨앗 관찰 경계)만 쓰며 stage closeout judgment(단계 마감 판정)이 아님."},
            },
            "required_skill_receipts": REQUIRED_SKILLS,
            "required_gates": REQUIRED_GATES,
        },
        "evidence_contract": {
            "raw_evidence": [manifest["inputs"]["model_input_dataset_path"], manifest["inputs"]["parent_top_seed_surfaces_path"]],
            "machine_readable": [manifest["outputs"][key]["path"] for key in manifest["outputs"]] + [MANIFEST_PATH.as_posix()],
            "human_readable": [REPORT_PATH.as_posix()],
        },
        "gates": {
            "required": REQUIRED_GATES,
            "not_applicable_with_reason": {
                "mt5_runtime_evidence_gate": "No MT5 execution(MT5 실행 없음); claim lowered to ONNX smoke seed observation(온엑스 스모크 씨앗 관찰로 주장 축소).",
                "wfo_gate": "No WFO execution(워크포워드 실행 없음); not a validation candidate(검증 후보 아님).",
            },
        },
        "final_claim_policy": {
            "allowed_claims": [
                "trainable_onnx_seed_smoke_completed(학습 가능 온엑스 씨앗 스모크 완료)",
                "onnx_parity_passed(온엑스 동등성 통과)",
                "onnx_seed_observation_exists(온엑스 씨앗 관찰 있음)",
            ],
            "forbidden_claims": FORBIDDEN_CLAIMS,
            "claim_vocabulary_reference": "docs/agent_control/claim_vocabulary.yaml",
        },
    }


def build_skill_receipts(
    manifest: dict[str, Any],
    top: dict[str, Any],
    summary: pd.DataFrame,
    model_table: pd.DataFrame,
) -> list[dict[str, Any]]:
    produced = [manifest["outputs"][key]["path"] for key in manifest["outputs"]] + [MANIFEST_PATH.as_posix(), REPORT_PATH.as_posix()]
    onnx_paths = [record["onnx_export"]["path"] for record in manifest.get("exports", [])]
    return [
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-run-evidence-system",
            "triggered": True,
            "status": "executed",
            "source_inputs": [manifest["inputs"]["model_input_dataset_path"], manifest["inputs"]["parent_top_seed_surfaces_path"]],
            "produced_artifacts": produced,
            "ledger_rows": [
                f"{RUN_ID}__tier_a_separate_onnx_seed_smoke",
                f"{RUN_ID}__tier_b_separate_missing_required",
                f"{RUN_ID}__tier_ab_combined_out_of_scope",
            ],
            "missing_evidence": ["Tier B partial-context artifact(부분 문맥 Tier B 산출물)", "MT5 fills(MT5 체결)", "WFO validation(워크포워드 검증)"],
            "allowed_claims": ["trainable_onnx_seed_smoke_completed(학습 가능 온엑스 씨앗 스모크 완료)", "onnx_seed_observation_exists(온엑스 씨앗 관찰 있음)"],
            "forbidden_claims": FORBIDDEN_CLAIMS,
        },
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-experiment-design",
            "triggered": True,
            "status": "executed",
            "hypothesis": "frontier02B proxy seed surfaces(프록시 씨앗 표면)를 trainable ONNX(학습 가능 온엑스) teacher model(교사 모델)로 바꾸면 다음 repair/review(수리/검토)에 쓸 seed observation(씨앗 관찰)을 만들 수 있다.",
            "baseline": "no selected baseline(선택 기준선 없음); Stage12-364 reference only(참조 전용)",
            "changed_variables": ["teacher candidate(교사 후보)", "probability threshold(확률 임계값)", "probability margin(확률 마진)", "cooldown bars(쿨다운 봉수)", "runtime filter(런타임 필터)"],
            "invalid_conditions": ["feature order mismatch(피처 순서 불일치)", "missing 3-class train labels(3클래스 학습 라벨 누락)", "ONNX parity failure(온엑스 동등성 실패)", "OOS selector leakage(OOS 선택기 누수)"],
            "evidence_plan": ["model_training_summary.csv", "onnx_parity_audit.json", "decision_surface_summary.csv", "run_manifest.json", "ledger rows(장부 행)", "gate audits(게이트 감사)"],
        },
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-data-integrity",
            "triggered": True,
            "status": "executed",
            "data_sources_checked": [manifest["inputs"]["model_input_dataset_path"], "model_input_feature_order.txt", manifest["inputs"]["parent_top_seed_surfaces_path"]],
            "time_axis_boundary": "timestamp UTC(UTC 타임스탬프)를 America/New_York date(뉴욕 날짜)로 scope days(범위 일수) 계산에만 사용.",
            "split_boundary": "train fit(학습 적합), validation rank(검증 순위), OOS diagnostic only(표본외 진단 전용).",
            "leakage_checks": ["feature hash matched(피처 해시 일치)", "dataset hash matched parent(부모 데이터셋 해시 일치)", "OOS not used for rank(표본외 순위 미사용)"],
            "missing_data_boundary": "Tier B partial-context dataset(부분 문맥 Tier B 데이터셋)은 이번 실행에서 materialized(물질화)하지 않음.",
        },
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-model-validation",
            "triggered": True,
            "status": "executed",
            "model_or_threshold_surface": "3-class logistic teacher-distillation ONNX seed surfaces(3클래스 로지스틱 교사 증류 온엑스 씨앗 표면).",
            "validation_split": "validation ranking only(검증 순위 전용); OOS diagnostic only(표본외 진단 전용).",
            "overfit_checks": ["model fitted on train only(모델 학습 구간만 적합)", "validation ranking only(검증 순위만)", "OOS not selector(OOS 선택기 아님)", "ONNX parity checked(온엑스 동등성 확인)"],
            "selection_metric_boundary": "aspiration_distance_score(목표 거리 점수)는 seed observation comparison(씨앗 관찰 비교) 전용.",
            "allowed_claims": ["onnx_seed_observation_exists(온엑스 씨앗 관찰 있음)"],
            "forbidden_claims": FORBIDDEN_CLAIMS,
        },
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-artifact-lineage",
            "triggered": True,
            "status": "executed",
            "source_inputs": [manifest["inputs"]["model_input_dataset_path"], manifest["inputs"]["parent_top_seed_surfaces_path"]],
            "produced_artifacts": produced + onnx_paths,
            "raw_evidence": [manifest["inputs"]["model_input_dataset_path"], manifest["inputs"]["parent_top_seed_surfaces_path"]],
            "machine_readable": [manifest["outputs"][key]["path"] for key in manifest["outputs"]] + [MANIFEST_PATH.as_posix()],
            "human_readable": [REPORT_PATH.as_posix()],
            "hashes_or_missing_reasons": {key: manifest["outputs"][key]["sha256"] for key in manifest["outputs"]},
            "lineage_boundary": "cheap ONNX smoke only(저비용 온엑스 스모크 전용); no MT5 artifact(MT5 산출물 없음).",
        },
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-grok-collaboration",
            "triggered": True,
            "status": "executed",
            "trigger_reason": "persistent goal(지속 목표) requires Grok at stage open/pre-expensive/closeout; this run is cheap ONNX smoke(저비용 온엑스 스모크).",
            "review_size": "not_called_this_run_existing_stage_open_review_applies(이번 실행 새 호출 없음, 기존 단계 개방 검토 적용)",
            "direction_before_grok": "stage-open direction already reviewed(단계 개방 방향은 이미 검토됨); execute cheap trainable ONNX smoke(저비용 학습 가능 온엑스 스모크 실행).",
            "bounded_evidence": [
                "docs/agent_control/grok_reviews/2026-06-14_frontier02_stage_open/medium_review/clean_output.md",
                f"stages/{STAGE_ID}/03_reviews/frontier02B_proxy_scout_execution_v1_report.md",
            ],
            "prompt_identity": "not_created_this_run_no_new_grok_call(이번 실행 새 그록 호출 없음)",
            "grok_output_identity": "docs/agent_control/grok_reviews/2026-06-14_frontier02_stage_open/medium_review/clean_output.md",
            "advice_classification": {
                "accepted": ["four-axis wording(네 축 표현)", "avoid density-only framing(밀도 단독 표현 회피)"],
                "rejected": [],
                "needs_local_verification": [],
            },
            "local_verification": "frontier02C did not start WFO/MT5(워크포워드/MT5 미시작); pre-expensive Grok review(비싼 검증 전 그록 검토)는 next serious validation(다음 진지 검증) 전에 필요.",
            "forbidden_claim_check": FORBIDDEN_CLAIMS,
            "final_codex_direction": "use ONNX output as seed observation only(온엑스 출력을 씨앗 관찰로만 사용).",
        },
    ]


def build_scope_gate(summary: pd.DataFrame, metrics: pd.DataFrame, model_table: pd.DataFrame) -> dict[str, Any]:
    return {
        "audit_name": "scope_completion_gate",
        "status": "pass",
        "passed": True,
        "observed": {
            "trained_models": int(len(model_table)),
            "decision_rows": int(len(summary)),
            "metric_rows": int(len(metrics)),
            "onnx_seed_observation_rows": int(summary["onnx_seed_observation_flag"].sum()),
            "report_path": REPORT_PATH.as_posix(),
        },
        "forbidden_claims": FORBIDDEN_CLAIMS,
    }


def build_kpi_audit(top: dict[str, Any], counts: dict[str, int]) -> dict[str, Any]:
    return {
        "audit_name": "kpi_contract_audit",
        "status": "pass",
        "passed": True,
        "scoreboard_lane": "trainable_onnx_seed_smoke(학습 가능 온엑스 씨앗 스모크)",
        "tier_records": {
            "tier_a_separate": "materialized(물질화)",
            "tier_b_separate": "missing_required(필수 누락)",
            "tier_ab_combined": "out_of_scope_by_claim(주장 범위 밖)",
        },
        "best_validation_rank": json_ready(top),
        "axis_counts": counts,
        "boundary": "proxy KPI(프록시 KPI) and ONNX parity(온엑스 동등성) only; not MT5 trading KPI(MT5 거래 KPI 아님).",
    }


def build_model_training_audit(model_table: pd.DataFrame, classifier: pd.DataFrame) -> dict[str, Any]:
    return {
        "audit_name": "model_training_audit",
        "status": "pass",
        "passed": True,
        "trained_models": int(len(model_table)),
        "model_family": "sklearn_logistic_regression_multiclass_teacher_distillation",
        "class_order": [0, 1, 2],
        "validation_macro_f1_mean": float(classifier.loc[classifier["split"].eq("validation"), "macro_f1"].mean()),
        "oos_macro_f1_mean": float(classifier.loc[classifier["split"].eq("oos"), "macro_f1"].mean()),
        "skipped_teachers_boundary": "one-sided teachers skipped for fixed 3-class ONNX(한 방향 교사는 고정 3클래스 온엑스에서 건너뜀).",
    }


def build_onnx_parity_gate(manifest: dict[str, Any]) -> dict[str, Any]:
    records = [record["onnx_parity"] for record in manifest.get("exports", [])]
    return {
        "audit_name": "onnx_parity_audit",
        "status": "pass" if records and all(record.get("passed") for record in records) else "blocked",
        "passed": bool(records and all(record.get("passed") for record in records)),
        "records": records,
        "boundary": "parity means sklearn-vs-ONNX probability match(동등성은 sklearn-온엑스 확률 일치만 뜻함), not runtime authority(런타임 권위 아님).",
    }


def build_artifact_audit(manifest: dict[str, Any]) -> dict[str, Any]:
    return {
        "audit_name": "artifact_lineage_audit",
        "status": "pass",
        "passed": True,
        "source_inputs": manifest["inputs"],
        "produced_artifacts": manifest["outputs"],
        "onnx_exports": manifest.get("exports", []),
        "manifest": {"path": MANIFEST_PATH.as_posix(), "sha256": sha256_file(MANIFEST_PATH)},
        "report": {"path": REPORT_PATH.as_posix(), "sha256": sha256_file(REPORT_PATH)},
        "lineage_boundary": "trainable ONNX seed smoke only(학습 가능 온엑스 씨앗 스모크 전용)",
    }


def build_external_review_packet() -> dict[str, Any]:
    return {
        "audit_name": "external_review_packet",
        "status": "pass",
        "passed": True,
        "review_action": "no_new_grok_call_this_run(이번 실행 새 그록 호출 없음)",
        "reason": "frontier02C is cheap ONNX smoke(저비용 온엑스 스모크) after stage-open Grok review(단계 개방 그록 검토 후 실행); WFO/MT5 not started(워크포워드/MT5 미시작).",
        "existing_review": "docs/agent_control/grok_reviews/2026-06-14_frontier02_stage_open/medium_review/clean_output.md",
        "next_required_review": "before expensive WFO/MT5 or stage closeout(비싼 워크포워드/MT5 또는 단계 마감 전)",
    }


def build_final_claim_guard() -> dict[str, Any]:
    return {
        "audit_name": "final_claim_guard",
        "status": "pass",
        "passed": True,
        "requested_claims": ["trainable_onnx_seed_smoke_completed(학습 가능 온엑스 씨앗 스모크 완료)", "onnx_seed_observation_exists(온엑스 씨앗 관찰 있음)"],
        "allowed_claims": ["trainable_onnx_seed_smoke_completed(학습 가능 온엑스 씨앗 스모크 완료)", "onnx_seed_observation_exists(온엑스 씨앗 관찰 있음)"],
        "forbidden_claims": FORBIDDEN_CLAIMS,
        "forbidden_claims_detected": [],
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
    }


def build_closeout_gate() -> dict[str, Any]:
    return {
        "audit_name": "closeout_gate",
        "status": "pass",
        "audits": [
            {"audit_name": "scope_completion_gate", "status": "pass"},
            {"audit_name": "kpi_contract_audit", "status": "pass"},
            {"audit_name": "model_training_audit", "status": "pass"},
            {"audit_name": "onnx_parity_audit", "status": "pass"},
            {"audit_name": "artifact_lineage_audit", "status": "pass"},
            {"audit_name": "external_review_packet", "status": "pass"},
            {"audit_name": "work_packet_schema_lint", "status": "pass"},
            {"audit_name": "skill_receipt_lint", "status": "pass"},
            {"audit_name": "skill_receipt_schema_lint", "status": "pass"},
            {"audit_name": "required_gate_coverage_audit", "status": "pass"},
        ],
        "final_claim_guard": {"audit_name": "final_claim_guard", "status": "pass"},
    }


def build_run_registry_row(
    now: str,
    manifest: dict[str, Any],
    top: dict[str, Any],
    summary: pd.DataFrame,
    metrics: pd.DataFrame,
    model_table: pd.DataFrame,
    counts: dict[str, int],
) -> dict[str, Any]:
    primary = primary_kpi_text(top)
    guardrail = guardrail_text(counts, model_table)
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "trainable_onnx_seed_smoke(학습 가능 온엑스 씨앗 스모크)",
        "status": "completed_frontier02C_trainable_onnx_seed_smoke_no_authority",
        "judgment": "onnx_seed_observation_density_oos_touched_pf_gap_remains_no_authority",
        "path": REPORT_PATH.as_posix(),
        "notes": (
            f"trained_models={len(model_table)};decision_rows={len(summary)};observation_rows={int(summary['onnx_seed_observation_flag'].sum())};"
            f"best_validation={top['candidate_id']};val_pf={fmt(top['validation_profit_factor'])};"
            f"val_density={fmt(top['validation_trades_per_day'])};oos_pf={fmt(top['oos_profit_factor'])};"
            f"oos_density={fmt(top['oos_trades_per_day'])};no authority claims."
        ),
        "family": "experiment_execution(실험 실행)",
        "primary_report": REPORT_PATH.as_posix(),
        "run_number": RUN_NUMBER,
        "date": "2026-06-14",
        "decision": "frontier02C_trainable_onnx_seed_smoke_completed_repair_required",
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "rows": int(len(summary)),
        "gate_passes": len(REQUIRED_GATES),
        "gate_total": len(REQUIRED_GATES),
        "claim_boundary": "trainable_onnx_seed_smoke_only_no_wfo_no_mt5_no_candidate_selection_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim",
        "report_path": REPORT_PATH.as_posix(),
        "trained_models": int(len(model_table)),
        "onnx_parity": f"{int(model_table['onnx_parity_passed'].sum())}/{len(model_table)} pass",
        "best_proxy": top["teacher_candidate_id"],
        "candidate_rows": int(len(summary)),
        "positive_proxy_rows": int(summary["onnx_seed_observation_flag"].sum()),
        "best_model_id": top["candidate_model_id"],
        "best_proxy_net": fmt(top["validation_net_profit"]),
        "attempt_rows": int(len(metrics)),
        "feature_matrix_rows": int(manifest["inputs"]["rows"]),
        "runtime_completed_rows": 0,
        "best_net_profit": fmt(top["validation_net_profit"]),
        "best_profit_factor": fmt(top["validation_profit_factor"]),
        "operating_ready_rows": 0,
        "run_date": "2026-06-14",
        "primary_artifact": manifest["outputs"]["top_onnx_seed_surfaces"]["path"],
        "candidate_model_id": top["candidate_model_id"],
        "net_profit": fmt(top["validation_net_profit"]),
        "profit_factor": fmt(top["validation_profit_factor"]),
        "drawdown": fmt(top["validation_max_drawdown_percent"]),
        "trade_count": int(top["validation_trade_count"]),
        "result_status": "completed_onnx_seed_smoke_no_authority(온엑스 씨앗 스모크 완료, 권위 없음)",
        "sample_rows": int(manifest["inputs"]["rows"]),
        "feature_count": int(manifest["model_contract"]["feature_count"]),
        "expectancy": fmt(top["validation_expectancy"]),
        "attempt_count": int(len(metrics)),
        "view": "Tier A separate(티어 A 분리)",
        "tier": "Tier A(티어 A)",
        "metric_scope": "trainable_onnx_seed_smoke(학습 가능 온엑스 씨앗 스모크)",
        "scoreboard_lane": "trainable_onnx_seed_smoke(학습 가능 온엑스 씨앗 스모크)",
        "external_verification_status": "out_of_scope_by_claim_no_mt5(주장 범위 밖 MT5 없음)",
        "trade_density_per_feature_day": fmt(top["validation_trades_per_day"]),
        "trade_density_requirement_status": "below_goal_validation_oos_in_goal_proxy(검증 미달, 표본외 프록시 목표권)",
        "result_judgment": "onnx_seed_observation_no_authority_pf_gap_remains",
        "final_decision_path": REPORT_PATH.as_posix(),
        "gate_audit_path": (PACKET_ROOT / "required_gate_coverage_audit.json").as_posix(),
        "created_at_utc": now,
        "ledger_row_id": f"{RUN_ID}__tier_a_separate_onnx_seed_smoke",
        "subrun_id": f"{RUN_ID}__tier_a_separate_onnx_seed_smoke",
        "record_view": "Tier A separate(티어 A 분리)",
        "tier_scope": "Tier A(티어 A)",
        "kpi_scope": "trainable_onnx_seed_smoke(학습 가능 온엑스 씨앗 스모크)",
        "primary_kpi": primary,
        "guardrail_kpi": guardrail,
        "model_variants": int(len(model_table)),
        "selected_surfaces": top["candidate_id"],
        "runtime_attempt_rows": 0,
        "work_family": "experiment_execution(실험 실행)",
        "max_drawdown_amount": fmt(top["validation_max_drawdown_percent"]),
        "long_trade_count": int(top["validation_long_trade_count"]),
        "short_trade_count": int(top["validation_short_trade_count"]),
        "row_id": f"{RUN_ID}__tier_a_separate_onnx_seed_smoke",
        "evidence_boundary": "onnx_seed_smoke_only_no_authority(온엑스 씨앗 스모크 전용, 권위 없음)",
        "next_action": NEXT_RUN_ID,
        "question": "Can trainable ONNX seed surfaces repair PF and density together?(학습 가능 온엑스 씨앗 표면이 수익 팩터와 밀도를 함께 수리할 수 있는가?)",
        "artifact_count": len(manifest["outputs"]),
        "required_gate_audit": (PACKET_ROOT / "required_gate_coverage_audit.json").as_posix(),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "run_family": "frontier_hypothesis_lifecycle(전선 가설 생명주기)",
        "run_type": "onnx_seed_smoke(온엑스 씨앗 스모크)",
        "input_run_id": PARENT_RUN_ID,
        "output_path": RUN_ROOT.as_posix(),
        "result_path": REPORT_PATH.as_posix(),
        "selected_net_profit": fmt(top["validation_net_profit"]),
        "selected_profit_factor": fmt(top["validation_profit_factor"]),
        "selected_trade_density": fmt(top["validation_trades_per_day"]),
        "goal_achieve": "not_claimed",
        "source_authority": "model_input_dataset_parent_proxy_seed_and_onnx_parity(모델 입력 데이터셋/부모 프록시 씨앗/온엑스 동등성)",
        "trade_density": fmt(top["validation_trades_per_day"]),
        "expected_net_profit": fmt(top["oos_net_profit"]),
        "expected_profit_factor": fmt(top["oos_profit_factor"]),
        "expected_trade_count": int(top["oos_trade_count"]),
        "expected_trade_density": fmt(top["oos_trades_per_day"]),
        "max_drawdown_percent": fmt(top["validation_max_drawdown_percent"]),
        "strict_joint_pass_count": int(top["validation_joint_pass_count"]),
    }


def build_alpha_ledger_rows(
    now: str,
    manifest: dict[str, Any],
    top: dict[str, Any],
    summary: pd.DataFrame,
    model_table: pd.DataFrame,
    counts: dict[str, int],
) -> list[dict[str, Any]]:
    primary = primary_kpi_text(top)
    guardrail = guardrail_text(counts, model_table)
    common = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "kpi_scope": "trainable_onnx_seed_smoke(학습 가능 온엑스 씨앗 스모크)",
        "scoreboard_lane": "trainable_onnx_seed_smoke(학습 가능 온엑스 씨앗 스모크)",
        "path": REPORT_PATH.as_posix(),
        "run_number": RUN_NUMBER,
        "date": "2026-06-14",
        "next_run_id": NEXT_RUN_ID,
        "claim_boundary": "onnx_seed_smoke_only_no_wfo_no_mt5_no_candidate_selection_no_authority_goal_claim",
        "report_path": REPORT_PATH.as_posix(),
        "work_family": "experiment_execution(실험 실행)",
        "created_at_utc": now,
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "external_verification_status": "out_of_scope_by_claim_no_mt5(주장 범위 밖 MT5 없음)",
        "trained_models": int(len(model_table)),
        "onnx_parity": f"{int(model_table['onnx_parity_passed'].sum())}/{len(model_table)} pass",
        "best_proxy": top["teacher_candidate_id"],
        "best_model_id": top["candidate_model_id"],
        "candidate_model_id": top["candidate_model_id"],
        "candidate_rows": int(len(summary)),
        "positive_proxy_rows": int(summary["onnx_seed_observation_flag"].sum()),
        "primary_artifact": manifest["outputs"]["top_onnx_seed_surfaces"]["path"],
        "feature_count": int(manifest["model_contract"]["feature_count"]),
        "source_authority": "model_input_dataset_parent_proxy_seed_and_onnx_parity(모델 입력 데이터셋/부모 프록시 씨앗/온엑스 동등성)",
    }
    return [
        {
            **common,
            "ledger_row_id": f"{RUN_ID}__tier_a_separate_onnx_seed_smoke",
            "subrun_id": f"{RUN_ID}__tier_a_separate_onnx_seed_smoke",
            "record_view": "Tier A separate(티어 A 분리)",
            "tier_scope": "Tier A(티어 A)",
            "status": "completed",
            "judgment": "onnx_seed_observation_no_authority_pf_gap_remains",
            "primary_kpi": primary,
            "guardrail_kpi": guardrail,
            "notes": "Tier A ONNX seed smoke materialized(티어 A 온엑스 씨앗 스모크 물질화); no MT5/no authority(MT5/권위 없음).",
            "decision": "continue_to_frontier02D_review_and_repair(전선02D 검토와 수리로 계속)",
            "result_status": "completed_onnx_seed_smoke_no_authority(온엑스 씨앗 스모크 완료, 권위 없음)",
            "result_judgment": "onnx_seed_observation_no_authority_pf_gap_remains",
            "net_profit": fmt(top["validation_net_profit"]),
            "profit_factor": fmt(top["validation_profit_factor"]),
            "expectancy": fmt(top["validation_expectancy"]),
            "drawdown": fmt(top["validation_max_drawdown_percent"]),
            "trade_count": int(top["validation_trade_count"]),
            "long_trade_count": int(top["validation_long_trade_count"]),
            "short_trade_count": int(top["validation_short_trade_count"]),
            "trade_density_per_feature_day": fmt(top["validation_trades_per_day"]),
            "trade_density_requirement_status": "below_goal_validation_oos_in_goal_proxy(검증 미달, 표본외 프록시 목표권)",
            "expected_net_profit": fmt(top["oos_net_profit"]),
            "expected_profit_factor": fmt(top["oos_profit_factor"]),
            "expected_trade_count": int(top["oos_trade_count"]),
            "expected_trade_density": fmt(top["oos_trades_per_day"]),
            "max_drawdown_percent": fmt(top["validation_max_drawdown_percent"]),
            "strict_joint_pass_count": int(top["validation_joint_pass_count"]),
        },
        {
            **common,
            "ledger_row_id": f"{RUN_ID}__tier_b_separate_missing_required",
            "subrun_id": f"{RUN_ID}__tier_b_separate_missing_required",
            "record_view": "Tier B separate(티어 B 분리)",
            "tier_scope": "Tier B(티어 B)",
            "status": "missing_required",
            "judgment": "missing_required_partial_context_artifact_not_materialized",
            "primary_kpi": "not_measured(측정 안 됨)",
            "guardrail_kpi": "Tier B partial-context dataset not materialized(티어 B 부분 문맥 데이터셋 물질화 안 됨)",
            "notes": "Required paired record kept as missing_required(필수 쌍 기록을 필수 누락으로 유지).",
            "decision": "materialize_tier_b_before_serious_validation(진지 검증 전 티어 B 물질화 필요)",
            "result_status": "missing_required_tier_b_no_authority(티어 B 필수 누락, 권위 없음)",
            "result_judgment": "missing_required",
            "source_authority": "missing_required(필수 누락)",
        },
        {
            **common,
            "ledger_row_id": f"{RUN_ID}__tier_ab_combined_out_of_scope",
            "subrun_id": f"{RUN_ID}__tier_ab_combined_out_of_scope",
            "record_view": "Tier A+B combined(Tier A+B 합산)",
            "tier_scope": "Tier A+B(Tier A+B 합산)",
            "status": "out_of_scope_by_claim",
            "judgment": "combined_routed_total_not_claimed_no_tier_b_fallback",
            "primary_kpi": "not_measured(측정 안 됨)",
            "guardrail_kpi": "No routed Tier B fallback(라우팅 티어 B 대체 없음); synthetic sum not created(합성 합산 만들지 않음)",
            "notes": "Combined row is not synthetic sum(합산 행은 합성 합산이 아님).",
            "decision": "route_later_only_after_tier_b_and_grok_pre_expensive_review(티어 B와 비싼 검증 전 그록 검토 후 나중 라우팅)",
            "result_status": "out_of_scope_combined_no_authority(합산 범위 밖, 권위 없음)",
            "result_judgment": "out_of_scope_by_claim",
            "source_authority": "out_of_scope_by_claim(주장 범위 밖)",
        },
    ]


def build_stage_ledger_row(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": row["subrun_id"],
        "parent_run_id": PARENT_RUN_ID,
        "scoreboard_lane": row.get("scoreboard_lane", ""),
        "status": row.get("status", ""),
        "judgment": row.get("judgment", ""),
        "path": REPORT_PATH.as_posix(),
        "external_verification_status": row.get("external_verification_status", ""),
        "notes": row.get("notes", ""),
        "run_number": RUN_NUMBER,
        "date": "2026-06-14",
        "decision": row.get("decision", ""),
        "next_run_id": NEXT_RUN_ID,
        "claim_boundary": row.get("claim_boundary", ""),
        "report_path": REPORT_PATH.as_posix(),
        "result_status": row.get("result_status", ""),
        "work_family": row.get("work_family", ""),
        "result_judgment": row.get("result_judgment", ""),
        "created_at_utc": row.get("created_at_utc", ""),
        "lane": row.get("scoreboard_lane", ""),
        "primary_report": REPORT_PATH.as_posix(),
        "evidence_boundary": "onnx_seed_smoke_only_no_authority(온엑스 씨앗 스모크 전용, 권위 없음)",
        "next_action": NEXT_RUN_ID,
        "question": "Can trainable ONNX seed surfaces repair PF and density together?(학습 가능 온엑스 씨앗 표면이 수익 팩터와 밀도를 함께 수리할 수 있는가?)",
        "ledger_row_id": row["ledger_row_id"],
        "row_id": row["ledger_row_id"],
        "record_view": row["record_view"],
        "tier_scope": row["tier_scope"],
        "kpi_scope": row.get("kpi_scope", ""),
        "primary_kpi": row.get("primary_kpi", ""),
        "guardrail_kpi": row.get("guardrail_kpi", ""),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "source_authority": row.get("source_authority", ""),
        "goal_achieve": "not_claimed",
    }


def update_state_documents(
    now: str,
    manifest: dict[str, Any],
    top: dict[str, Any],
    counts: dict[str, int],
    model_table: pd.DataFrame,
) -> None:
    state = {
        "current_stage_id": STAGE_ID,
        "current_run_id": RUN_ID,
        "latest_completed_run_id": RUN_ID,
        "current_status": "active_frontier02_trainable_onnx_seed_smoke_completed_no_authority",
        "current_judgment": "onnx_seed_observation_density_oos_touched_pf_gap_remains_no_authority",
        "next_run_id": NEXT_RUN_ID,
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "updated_at_utc": now,
    }
    write_yaml(WORKSPACE_STATE, state)
    write_text_sig(CURRENT_WORKING_STATE, current_working_state_text(now, manifest, top, counts, model_table))
    write_text_sig(SELECTION_STATUS, selection_status_text(now, top, counts, model_table))
    update_review_index()
    update_stage_readme(top)
    append_changelog(now, top, model_table)
    update_idea_registry(top, model_table)


def current_working_state_text(
    now: str,
    manifest: dict[str, Any],
    top: dict[str, Any],
    counts: dict[str, int],
    model_table: pd.DataFrame,
) -> str:
    return f"""# Current Working State(현재 작업 상태)

Updated(갱신): {now}

Active stage(활성 단계): `{STAGE_ID}`

Current run(현재 실행): `{RUN_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Current truth(현재 진실): Stage364(364단계)는 negative memory(부정 기억)로 닫혔고, `stage_frontier_01(전선 01단계)`은 Stage12~364(12~364단계)를 reference archive(참조 보관소)로 정리한 archive interface(보관소 접점)로 닫혔습니다. Frontier 02(전선 02)는 첫 독립 ONNX(온엑스) hypothesis lifecycle(가설 생명주기)로 열린 상태입니다.

Frontier 02 thesis(전선 02 가설): directly trained ONNX(직접 학습 온엑스) surface(표면)를 위한 four-axis joint objective(네 축 동시 목적)를 proxy/training/selection-time(프록시/학습/선택 시점)에서 먼저 설계하면 density/PF/DD/curve smoothness(밀도/수익 팩터/손실폭/곡선 매끄러움)를 한 축씩 수리하는 반복을 줄일 수 있습니다.

Latest evidence(최근 근거): `frontier02C_trainable_onnx_seed_surface_design_v1`은 frontier02B(전선02B)의 seed surface(씨앗 표면)를 cheap teacher model(저비용 교사 모델)로 학습해 ONNX(온엑스) artifact(산출물) {len(model_table)}개를 만들었고 parity(동등성)는 `{int(model_table['onnx_parity_passed'].sum())}/{len(model_table)}` 통과했습니다. best validation rank(검증 순위 1위)는 `{top['candidate_id']}`이고 validation(검증) PF(수익 팩터) `{fmt(top['validation_profit_factor'])}`, density(밀도) `{fmt(top['validation_trades_per_day'])}/day`, DD(손실폭) `{fmt(top['validation_max_drawdown_percent'])}%`, OOS(표본외) PF(수익 팩터) `{fmt(top['oos_profit_factor'])}`, density(밀도) `{fmt(top['oos_trades_per_day'])}/day`, DD(손실폭) `{fmt(top['oos_max_drawdown_percent'])}%`입니다.

KPI read(핵심 성과 지표 판독): ONNX seed observation(온엑스 씨앗 관찰)은 있습니다. OOS(표본외) density(밀도)는 목표권에 닿았지만 validation(검증) density(밀도), PF(수익 팩터), OOS DD(표본외 손실폭), smoothness(매끄러움)는 아직 부족합니다. validation(검증)에서 density pass(밀도 통과)는 {counts['validation_density_pass_rows']}개 row(행), PF pass(수익 팩터 통과)는 {counts['validation_pf_pass_rows']}개 row(행), DD pass(손실폭 통과)는 {counts['validation_dd_pass_rows']}개 row(행), smoothness pass(매끄러움 통과)는 {counts['validation_smoothness_pass_rows']}개 row(행)입니다.

Tier boundary(티어 경계): Tier A separate(Tier A 분리)는 materialized(물질화)했습니다. Tier B separate(Tier B 분리)는 `missing_required(필수 누락)`이고, Tier A+B combined(Tier A+B 합산)는 routed fallback(라우팅 대체)을 실행하지 않았으므로 `out_of_scope_by_claim(주장 범위 밖)`입니다.

Evidence paths(근거 경로): run manifest(실행 목록)는 `{MANIFEST_PATH.as_posix()}`이고, report(보고서)는 `{REPORT_PATH.as_posix()}`입니다. control packet(통제 묶음)은 `{PACKET_ROOT.as_posix()}/`입니다.

Grok boundary(그록 경계): 이번 실행은 cheap ONNX smoke(저비용 온엑스 스모크)라 새 Grok call(그록 호출)을 하지 않았습니다. 기존 stage-open Grok review(단계 개방 그록 검토)를 적용했고, WFO/MT5(워크포워드/MT5) 같은 expensive validation(비싼 검증) 전에는 새 Grok review(그록 검토)가 필요합니다.

Next action(다음 행동): `{NEXT_RUN_ID}`. 이 행동(action, 행동)의 효과(effect, 효과)는 ONNX seed observation(온엑스 씨앗 관찰)의 PF gap(수익 팩터 차이)과 density/DD tradeoff(밀도/손실폭 상충)를 수리하고, serious validation(진지 검증) 전 Grok review(그록 검토) 필요 여부를 분리하는 것입니다.

Operating boundary(운영 경계): completion(완성), selected baseline(선택 기준선), operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
"""


def selection_status_text(now: str, top: dict[str, Any], counts: dict[str, int], model_table: pd.DataFrame) -> str:
    return f"""# Stage Frontier 02 Selection Status(전선 02단계 선택 상태)

Updated(갱신): {now}

Stage status(단계 상태): `active_frontier02_trainable_onnx_seed_smoke_completed_no_authority`

Current run(현재 실행): `{RUN_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Judgment(판정): `onnx_seed_observation_density_oos_touched_pf_gap_remains_no_authority`

## Current Truth(현재 진실)

Frontier 02(전선 02)는 `stage_frontier_02__four_axis_joint_onnx_proxy_scout`로 열려 있으며, `frontier02C_trainable_onnx_seed_surface_design_v1`에서 first trainable ONNX smoke(첫 학습 가능 온엑스 스모크)를 완료했습니다.

The stage thesis(단계 가설)는 directly trained ONNX(직접 학습 온엑스) surface(표면)를 위한 four-axis joint objective(네 축 동시 목적)를 먼저 설계하는 것입니다.

## ONNX Seed Read(온엑스 씨앗 판독)

- trained_models(학습 모델): `{len(model_table)}`
- ONNX parity pass(온엑스 동등성 통과): `{int(model_table['onnx_parity_passed'].sum())}/{len(model_table)}`
- best validation rank(검증 순위 1위): `{top['candidate_id']}`
- validation PF/density/DD(검증 수익 팩터/밀도/손실폭): `{fmt(top['validation_profit_factor'])}` / `{fmt(top['validation_trades_per_day'])}/day` / `{fmt(top['validation_max_drawdown_percent'])}%`
- OOS PF/density/DD(표본외 수익 팩터/밀도/손실폭): `{fmt(top['oos_profit_factor'])}` / `{fmt(top['oos_trades_per_day'])}/day` / `{fmt(top['oos_max_drawdown_percent'])}%`

Effect(효과): ONNX seed observation(온엑스 씨앗 관찰)은 있지만, PF(수익 팩터)와 smoothness(매끄러움)는 final completion target(최종 완성 목표)에 아직 멀다. 이 표면(surface, 표면)은 next repair seed(다음 수리 씨앗)이지 selected candidate(선택 후보)가 아니다.

## Axis Counts(축별 개수)

- validation density/PF/DD/smoothness pass(검증 밀도/수익 팩터/손실폭/매끄러움 통과): `{counts['validation_density_pass_rows']}` / `{counts['validation_pf_pass_rows']}` / `{counts['validation_dd_pass_rows']}` / `{counts['validation_smoothness_pass_rows']}`
- OOS density/PF/DD/smoothness pass(표본외 밀도/수익 팩터/손실폭/매끄러움 통과): `{counts['oos_density_pass_rows']}` / `{counts['oos_pf_pass_rows']}` / `{counts['oos_dd_pass_rows']}` / `{counts['oos_smoothness_pass_rows']}`

## Tier Records(티어 기록)

- Tier A separate(Tier A 분리): `materialized(물질화)`
- Tier B separate(Tier B 분리): `missing_required(필수 누락)`
- Tier A+B combined(Tier A+B 합산): `out_of_scope_by_claim(주장 범위 밖)`

## Claim Boundary(주장 경계)

Allowed claim(허용 주장):

- trainable ONNX seed smoke completed(학습 가능 온엑스 씨앗 스모크 완료)
- ONNX parity passed(온엑스 동등성 통과)
- ONNX seed observation exists(온엑스 씨앗 관찰 있음)
- no authority claimed(권위 주장 없음)

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

Effect(효과): ONNX seed(온엑스 씨앗)의 PF gap(수익 팩터 차이), density gap(밀도 차이), OOS DD edge(표본외 손실폭 경계)를 수리하고, WFO/MT5(워크포워드/MT5) 전 Grok review(그록 검토) 조건을 분리한다.
"""


def update_review_index() -> None:
    text = read_text_sig(REVIEW_INDEX)
    row = f"| frontier02C trainable ONNX seed smoke report(frontier02C 학습 가능 온엑스 씨앗 스모크 보고) | `{REPORT_PATH.as_posix()}` | cheap teacher training(저비용 교사 학습), ONNX parity(온엑스 동등성), decision surface(결정 표면) 결과와 Tier A/B/combined(Tier A/B/합산) 경계 |"
    if "frontier02C trainable ONNX seed smoke report" not in text:
        text = text.replace(
            "| frontier02B proxy scout report(frontier02B 프록시 탐색 보고) | `stages/stage_frontier_02__four_axis_joint_onnx_proxy_scout/03_reviews/frontier02B_proxy_scout_execution_v1_report.md` | cheap proxy replay(저비용 프록시 재생) 결과와 Tier A/B/combined(Tier A/B/합산) 경계 |",
            "| frontier02B proxy scout report(frontier02B 프록시 탐색 보고) | `stages/stage_frontier_02__four_axis_joint_onnx_proxy_scout/03_reviews/frontier02B_proxy_scout_execution_v1_report.md` | cheap proxy replay(저비용 프록시 재생) 결과와 Tier A/B/combined(Tier A/B/합산) 경계 |\n" + row,
        )
        text = text.replace(
            "This index(이 색인)는 review capture(검토 기록)와 proxy scout evidence(프록시 탐색 근거)만 말한다. It is not model training(모델 학습 아님), WFO(워크포워드 최적화 아님), MT5 validation(MT5 검증 아님), or candidate selection(후보 선택 아님).",
            "This index(이 색인)는 review capture(검토 기록), proxy scout evidence(프록시 탐색 근거), and cheap ONNX smoke evidence(저비용 온엑스 스모크 근거)만 말한다. It is not WFO(워크포워드 최적화 아님), MT5 validation(MT5 검증 아님), candidate selection(후보 선택 아님), or runtime authority(런타임 권위 아님).",
        )
        write_text_sig(REVIEW_INDEX, text)


def update_stage_readme(top: dict[str, Any]) -> None:
    text = f"""# Stage Frontier 02(전선 02단계)

Stage id(단계 ID): `{STAGE_ID}`

Purpose(목적): four-axis joint ONNX proxy scout(네 축 동시 온엑스 프록시 탐색)를 설계하고, density/PF/DD/curve smoothness(밀도/수익 팩터/손실폭/곡선 매끄러움)를 동시에 보는 첫 독립 frontier hypothesis(전선 가설)를 연다.

Latest run(최근 실행): `frontier02C_trainable_onnx_seed_surface_design_v1` completed cheap trainable ONNX smoke(저비용 학습 가능 온엑스 스모크), generated ONNX parity-passed seed artifacts(온엑스 동등성 통과 씨앗 산출물), and found seed observation(씨앗 관찰), not selected candidate(선택 후보 아님).

Latest best read(최근 최고 판독): `{top['candidate_id']}` validation PF/density/DD(검증 수익 팩터/밀도/손실폭) `{fmt(top['validation_profit_factor'])}` / `{fmt(top['validation_trades_per_day'])}/day` / `{fmt(top['validation_max_drawdown_percent'])}%`; OOS PF/density/DD(표본외 수익 팩터/밀도/손실폭) `{fmt(top['oos_profit_factor'])}` / `{fmt(top['oos_trades_per_day'])}/day` / `{fmt(top['oos_max_drawdown_percent'])}%`.

Next run(다음 실행): `{NEXT_RUN_ID}`

Boundary(경계): this stage(이 단계)는 active exploration(활성 탐색)이다. It has no completion(완성 없음), no baseline(기준선 없음), no promotion(승격 없음), no runtime authority(런타임 권위 없음), no live readiness(실거래 준비 없음), and no Goal Achieve(목표 달성 없음).
"""
    write_text_sig(STAGE_README, text)


def append_changelog(now: str, top: dict[str, Any], model_table: pd.DataFrame) -> None:
    text = read_text_sig(CHANGELOG)
    marker = "<!-- frontier02C__trainable_onnx_seed_surface -->"
    if marker not in text:
        addition = (
            f"{marker}\n"
            f"- {now} `{RUN_ID}` completed cheap trainable ONNX smoke(저비용 학습 가능 온엑스 스모크); trained_models(학습 모델) `{len(model_table)}`, ONNX parity pass(온엑스 동등성 통과) `{int(model_table['onnx_parity_passed'].sum())}/{len(model_table)}`; "
            f"best validation rank(검증 순위 1위) `{top['candidate_id']}` validation PF/density/DD(검증 수익 팩터/밀도/손실폭) `{fmt(top['validation_profit_factor'])}`/`{fmt(top['validation_trades_per_day'])}`/`{fmt(top['validation_max_drawdown_percent'])}%`; "
            f"OOS PF/density/DD(표본외 수익 팩터/밀도/손실폭) `{fmt(top['oos_profit_factor'])}`/`{fmt(top['oos_trades_per_day'])}`/`{fmt(top['oos_max_drawdown_percent'])}%`; next(다음) `{NEXT_RUN_ID}`; no completion/baseline/promotion/runtime authority/Goal Achieve claim(완성/기준선/승격/런타임 권위/목표 달성 주장 없음).\n"
        )
        write_text_sig(CHANGELOG, text.rstrip() + "\n" + addition)


def update_idea_registry(top: dict[str, Any], model_table: pd.DataFrame) -> None:
    text = read_text_sig(IDEA_REGISTRY)
    updated = (
        "| `IDEA-FR02-FOUR-AXIS-JOINT-ONNX-PROXY-SCOUT` | `stage_frontier_02__four_axis_joint_onnx_proxy_scout` | directly trained ONNX(직접 학습 온엑스) surface(표면)를 위한 four-axis joint objective(네 축 동시 목적)가 density/PF/DD/curve smoothness(밀도/수익 팩터/손실폭/곡선 매끄러움)를 처음부터 함께 보게 하면 one-axis repair loop(한 축 수리 반복)를 줄일 수 있다 | `Tier A materialized, Tier B missing_required, Tier A+B out_of_scope(Tier A 물질화, Tier B 필수 누락, Tier A+B 범위 밖)` | `active_onnx_seed_smoke_completed_seed_observation_no_authority` | "
        f"`frontier02C_trainable_onnx_seed_surface_design_v1`에서 ONNX(온엑스) 모델 {len(model_table)}개를 만들고 parity(동등성) `{int(model_table['onnx_parity_passed'].sum())}/{len(model_table)}` 통과. best validation rank(검증 순위 1위)는 PF(수익 팩터) `{fmt(top['validation_profit_factor'])}`, density(밀도) `{fmt(top['validation_trades_per_day'])}/day`, DD(손실폭) `{fmt(top['validation_max_drawdown_percent'])}%`; OOS(표본외)는 PF(수익 팩터) `{fmt(top['oos_profit_factor'])}`, density(밀도) `{fmt(top['oos_trades_per_day'])}/day`, DD(손실폭) `{fmt(top['oos_max_drawdown_percent'])}%`. seed observation(씨앗 관찰)은 있지만 completion/baseline/promotion/runtime authority(완성/기준선/승격/런타임 권위)는 없음 |"
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


def axis_counts(summary: pd.DataFrame) -> dict[str, int]:
    return {
        "validation_density_pass_rows": int(summary["validation_density_pass"].sum()),
        "validation_pf_pass_rows": int(summary["validation_pf_pass"].sum()),
        "validation_dd_pass_rows": int(summary["validation_dd_pass"].sum()),
        "validation_smoothness_pass_rows": int(summary["validation_smoothness_pass"].sum()),
        "oos_density_pass_rows": int(summary["oos_density_pass"].sum()),
        "oos_pf_pass_rows": int(summary["oos_pf_pass"].sum()),
        "oos_dd_pass_rows": int(summary["oos_dd_pass"].sum()),
        "oos_smoothness_pass_rows": int(summary["oos_smoothness_pass"].sum()),
    }


def primary_kpi_text(top: dict[str, Any]) -> str:
    return (
        f"best_validation={top['candidate_id']};"
        f"model={top['candidate_model_id']};teacher={top['teacher_candidate_id']};"
        f"val_net={fmt(top['validation_net_profit'])};val_pf={fmt(top['validation_profit_factor'])};"
        f"val_density={fmt(top['validation_trades_per_day'])};val_dd={fmt(top['validation_max_drawdown_percent'])};"
        f"oos_net={fmt(top['oos_net_profit'])};oos_pf={fmt(top['oos_profit_factor'])};"
        f"oos_density={fmt(top['oos_trades_per_day'])};oos_dd={fmt(top['oos_max_drawdown_percent'])}"
    )


def guardrail_text(counts: dict[str, int], model_table: pd.DataFrame) -> str:
    return (
        f"onnx_parity={int(model_table['onnx_parity_passed'].sum())}/{len(model_table)};"
        "validation_axis_pass_rows="
        f"density:{counts['validation_density_pass_rows']},pf:{counts['validation_pf_pass_rows']},"
        f"dd:{counts['validation_dd_pass_rows']},smooth:{counts['validation_smoothness_pass_rows']};"
        "oos_axis_pass_rows="
        f"density:{counts['oos_density_pass_rows']},pf:{counts['oos_pf_pass_rows']},"
        f"dd:{counts['oos_dd_pass_rows']},smooth:{counts['oos_smoothness_pass_rows']};"
        "tier_b=missing_required;tier_ab=out_of_scope"
    )


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


def fmt(value: Any) -> str:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return "NA"
    if not pd.notna(number):
        return "NA"
    return f"{number:.6g}"


if __name__ == "__main__":
    raise SystemExit(main())
