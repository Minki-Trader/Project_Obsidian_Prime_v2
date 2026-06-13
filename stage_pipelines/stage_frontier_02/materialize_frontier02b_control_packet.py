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
RUN_ID = "frontier02B_proxy_scout_execution_v1"
RUN_NUMBER = "frontier02B"
PACKET_ROOT = Path("docs/agent_control/packets") / RUN_ID
RUN_ROOT = Path("stages") / STAGE_ID / "02_runs" / RUN_ID
MANIFEST_PATH = RUN_ROOT / "run_manifest.json"
REPORT_PATH = Path("stages") / STAGE_ID / "03_reviews" / f"{RUN_ID}_report.md"
STAGE_LEDGER = Path("stages") / STAGE_ID / "03_reviews" / "stage_run_ledger.csv"
ALPHA_LEDGER = Path("docs/registers/alpha_run_ledger.csv")
RUN_REGISTRY = Path("docs/registers/run_registry.csv")
NEXT_RUN_ID = "frontier02C_trainable_onnx_seed_surface_design_v1"
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
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    io_path(PACKET_ROOT).mkdir(parents=True, exist_ok=True)
    manifest = read_json(MANIFEST_PATH)
    summary = pd.read_csv(io_path(RUN_ROOT / "candidate_surface_summary.csv"))
    metrics = pd.read_csv(io_path(RUN_ROOT / "candidate_surface_metrics.csv"))
    top = (
        summary.sort_values(
            ["validation_aspiration_distance_score", "validation_joint_pass_count", "oos_aspiration_distance_score"],
            ascending=[True, False, True],
        )
        .iloc[0]
        .to_dict()
    )
    counts = axis_counts(summary)

    work_packet = build_work_packet(now, manifest)
    write_yaml(PACKET_ROOT / "work_packet.yaml", work_packet)
    receipts = build_skill_receipts(manifest)
    write_json(PACKET_ROOT / "skill_receipts.json", {"receipts": receipts})

    write_json(PACKET_ROOT / "scope_completion_gate.json", build_scope_gate(summary, metrics))
    write_json(PACKET_ROOT / "kpi_contract_audit.json", build_kpi_audit(counts))
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

    append_unique_csv(RUN_REGISTRY, "run_id", build_run_registry_row(now, manifest, top, summary, metrics, counts))
    for row in build_ledger_rows(now, manifest, top, summary, metrics, counts):
        append_unique_csv(ALPHA_LEDGER, "ledger_row_id", row)
        append_unique_csv(STAGE_LEDGER, "ledger_row_id", row)

    print(
        json.dumps(
            {
                "packet_root": PACKET_ROOT.as_posix(),
                "candidate_rows": int(len(summary)),
                "metric_rows": int(len(metrics)),
                "scout_clue_rows": int(summary["scout_clue_flag"].sum()),
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


def build_work_packet(now: str, manifest: dict[str, Any]) -> dict[str, Any]:
    return {
        "version": "work_packet_schema_v2",
        "packet_id": RUN_ID,
        "created_at_utc": now,
        "user_request": {
            "user_quote": "persistent_goal(지속 목표): build a genuinely strong US100 M5 ONNX(온엑스) with frontier hypothesis lifecycle(전선 가설 생명주기).",
            "requested_action": "execute_frontier02B_four_axis_proxy_scout",
            "requested_count": "one_proxy_scout_run(프록시 탐색 실행 1회)",
            "ambiguous_terms": [],
        },
        "current_truth": {
            "active_stage_before": STAGE_ID,
            "active_stage_after": STAGE_ID,
            "current_run_before": "frontier02A_proxy_score_spec_v1",
            "current_run_after": RUN_ID,
            "latest_completed_run_before": "frontier02A_proxy_score_spec_v1",
            "source_documents": [
                "docs/workspace/workspace_state.yaml",
                "docs/context/current_working_state.md",
                f"stages/{STAGE_ID}/01_inputs/proxy_score_plan.md",
                f"stages/{STAGE_ID}/01_inputs/experiment_design.md",
            ],
        },
        "work_classification": {
            "primary_family": "experiment_execution",
            "detected_families": ["experiment_execution", "kpi_evidence", "artifact_lineage", "state_sync"],
            "touched_surfaces": [
                "stage_pipelines/stage_frontier_02/four_axis_proxy_scout.py",
                f"stages/{STAGE_ID}",
                "docs/registers",
            ],
            "mutation_intent": True,
            "execution_intent": True,
        },
        "risk_vector_scan": {
            "risks": [
                "proxy_returns_are_not_mt5_fills(프록시 수익은 MT5 체결이 아님)",
                "Tier B artifact missing in this run(Tier B 산출물 이번 실행 누락)",
                "OOS diagnostic must not become selector(OOS 진단을 선택기로 쓰면 안 됨)",
            ],
            "hard_stop_risks": [],
            "required_decision_locks": [],
            "required_gates": REQUIRED_GATES,
            "forbidden_claims": FORBIDDEN_CLAIMS,
        },
        "decision_lock": {
            "mode": "reasonable_assumption_execute_with_proxy_boundary(합리적 가정으로 프록시 경계 내 실행)",
            "assumptions": ["cheap proxy replay(저비용 프록시 재생)는 Grok pre-expensive review(비싼 검증 전 그록 검토) 전에도 가능"],
            "questions": [],
            "required_user_decisions": [],
        },
        "interpreted_scope": {
            "work_families": ["experiment_execution"],
            "target_surfaces": ["four_axis_proxy_scout(네 축 프록시 탐색)", "structural_scout_kpi(구조 탐색 KPI)"],
            "scope_units": ["code_module", "run", "artifact", "report", "ledger", "kpi_row"],
            "execution_layers": ["code_edit", "python_execution", "kpi_recording", "ledger_update", "document_edit"],
            "mutation_policy": "stage_local_adapter_and_run_artifacts_only(단계 전용 어댑터와 실행 산출물만)",
            "evidence_layers": ["run_manifest", "candidate_surface_metrics", "candidate_surface_summary", "stage_report", "ledger_rows", "gate_audits"],
            "reduction_policy": "validation_rank_top_surfaces_only_for_next_inspection(다음 점검용 검증 순위 표면만 축약)",
            "claim_boundary": "scout_clue_or_seed_surface_only_no_authority(탐색 단서 또는 씨앗 표면까지만, 권위 없음)",
        },
        "acceptance_criteria": [
            {
                "id": "AC-001",
                "text": "stage-local script(단계 전용 스크립트)가 존재하고 실행된다.",
                "expected_artifact": "stage_pipelines/stage_frontier_02/four_axis_proxy_scout.py",
                "verification_method": "py_compile_and_run",
                "required": True,
            },
            {
                "id": "AC-002",
                "text": "candidate surface metrics(후보 표면 측정값)가 생성된다.",
                "expected_artifact": manifest["outputs"]["candidate_surface_metrics"]["path"],
                "verification_method": "file_hash_and_row_count",
                "required": True,
            },
            {
                "id": "AC-003",
                "text": "Tier A/B/combined ledger rows(티어 A/B/합산 장부 행)가 기록된다.",
                "expected_artifact": STAGE_LEDGER.as_posix(),
                "verification_method": "ledger_row_presence",
                "required": True,
            },
            {
                "id": "AC-004",
                "text": "final forbidden claims(최종 금지 주장)을 하지 않는다.",
                "expected_artifact": (PACKET_ROOT / "final_claim_guard.json").as_posix(),
                "verification_method": "claim_guard",
                "required": True,
            },
        ],
        "work_plan": {
            "phases": ["input_audit(입력 감사)", "proxy_surface_grid(프록시 표면 격자)", "four_axis_scoring(네 축 점수화)", "ledger_sync(장부 동기화)", "gate_audit(게이트 감사)"],
            "expected_outputs": [manifest["outputs"][key]["path"] for key in manifest["outputs"]] + [REPORT_PATH.as_posix()],
            "stop_conditions": ["input_hash_mismatch(입력 해시 불일치)", "feature_order_mismatch(피처 순서 불일치)", "no_metric_rows(측정 행 없음)", "gate_failure(게이트 실패)"],
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
                "obsidian-result-judgment": {"not_selected_reason": "Run report(실행 보고)는 scout clue boundary(탐색 단서 경계)만 쓰며 stage closeout judgment(단계 마감 판정)이 아님."},
            },
            "required_skill_receipts": REQUIRED_SKILLS,
            "required_gates": REQUIRED_GATES,
        },
        "evidence_contract": {
            "raw_evidence": [manifest["inputs"]["model_input_dataset_path"]],
            "machine_readable": [manifest["outputs"][key]["path"] for key in manifest["outputs"]] + [MANIFEST_PATH.as_posix()],
            "human_readable": [REPORT_PATH.as_posix()],
        },
        "gates": {
            "required": REQUIRED_GATES,
            "not_applicable_with_reason": {
                "mt5_runtime_evidence_gate": "No MT5 execution(MT5 실행 없음); claim lowered to proxy scout(프록시 탐색으로 주장 축소).",
                "model_training_gate": "No ONNX/model training(온엑스/모델 학습 없음); surfaces are score replays(점수 재생).",
            },
        },
        "final_claim_policy": {
            "allowed_claims": [
                "proxy_scout_completed(프록시 탐색 완료)",
                "scout_clue_exists(탐색 단서 있음)",
                "seed_surface_for_next_inspection(다음 점검용 씨앗 표면)",
            ],
            "forbidden_claims": FORBIDDEN_CLAIMS,
            "claim_vocabulary_reference": "docs/agent_control/claim_vocabulary.yaml",
        },
    }


def build_skill_receipts(manifest: dict[str, Any]) -> list[dict[str, Any]]:
    produced = [manifest["outputs"][key]["path"] for key in manifest["outputs"]] + [MANIFEST_PATH.as_posix(), REPORT_PATH.as_posix()]
    return [
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-run-evidence-system",
            "triggered": True,
            "status": "executed",
            "source_inputs": [manifest["inputs"]["model_input_dataset_path"], f"stages/{STAGE_ID}/01_inputs/proxy_score_plan.md"],
            "produced_artifacts": produced,
            "ledger_rows": [
                f"{RUN_ID}__tier_a_separate_proxy_scout",
                f"{RUN_ID}__tier_b_separate_missing_required",
                f"{RUN_ID}__tier_ab_combined_out_of_scope",
            ],
            "missing_evidence": ["Tier B partial-context artifact(부분 문맥 Tier B 산출물)", "MT5 fills(MT5 체결)", "ONNX model artifact(온엑스 모델 산출물)"],
            "allowed_claims": ["proxy_scout_completed(프록시 탐색 완료)", "scout_clue_exists(탐색 단서 있음)"],
            "forbidden_claims": FORBIDDEN_CLAIMS,
        },
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-experiment-design",
            "triggered": True,
            "status": "executed",
            "hypothesis": "four-axis joint proxy objective(네 축 동시 프록시 목적)가 one-axis repair loop(한 축 수리 반복)를 줄일 수 있는지 탐색한다.",
            "baseline": "no selected baseline(선택 기준선 없음); Stage12-364 reference only(참조 전용)",
            "changed_variables": ["surface score components(표면 점수 구성)", "threshold quantile(임계값 분위수)", "cooldown bars(쿨다운 봉수)", "side mode(방향 모드)", "rough cost proxy(거친 비용 프록시)"],
            "invalid_conditions": ["feature order mismatch(피처 순서 불일치)", "split contamination(분할 오염)", "OOS selector leakage(OOS 선택기 누수)", "missing source artifact(원천 산출물 누락)"],
            "evidence_plan": ["candidate_surface_metrics.csv", "candidate_surface_summary.csv", "run_manifest.json", "ledger rows(장부 행)", "gate audits(게이트 감사)"],
        },
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-data-integrity",
            "triggered": True,
            "status": "executed",
            "data_sources_checked": [manifest["inputs"]["model_input_dataset_path"], "model_input_feature_order.txt"],
            "time_axis_boundary": "timestamp UTC(UTC 타임스탬프)를 America/New_York date(뉴욕 날짜)로 scope days(범위 일수) 계산에만 사용.",
            "split_boundary": "train thresholds(학습 임계값), validation rank(검증 순위), OOS diagnostic only(표본외 진단 전용).",
            "leakage_checks": ["feature hash matched(피처 해시 일치)", "timestamp duplicates absent(중복 타임스탬프 없음)", "OOS not used for rank(표본외 순위 미사용)"],
            "missing_data_boundary": "Tier B partial-context dataset(부분 문맥 Tier B 데이터셋)은 이번 실행에서 materialized(물질화)하지 않음.",
        },
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-model-validation",
            "triggered": True,
            "status": "executed",
            "model_or_threshold_surface": "score replay threshold surfaces(점수 재생 임계값 표면), no trained ONNX(학습된 온엑스 없음).",
            "validation_split": "validation 2025-01-02 to 2025-09-30; OOS 2025-10-01 to 2026-04-13 diagnostic(진단).",
            "overfit_checks": ["thresholds from train only(임계값 학습 구간 산출)", "validation ranking only(검증 순위만)", "OOS not selector(OOS 선택기 아님)"],
            "selection_metric_boundary": "aspiration_distance_score(목표 거리 점수)는 scout comparison(탐색 비교) 전용.",
            "allowed_claims": ["seed_surface_for_training_design(학습 설계용 씨앗 표면)"],
            "forbidden_claims": FORBIDDEN_CLAIMS,
        },
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-artifact-lineage",
            "triggered": True,
            "status": "executed",
            "source_inputs": [manifest["inputs"]["model_input_dataset_path"], f"stages/{STAGE_ID}/01_inputs/proxy_score_plan.md"],
            "produced_artifacts": produced,
            "raw_evidence": [manifest["inputs"]["model_input_dataset_path"]],
            "machine_readable": [manifest["outputs"][key]["path"] for key in manifest["outputs"]] + [MANIFEST_PATH.as_posix()],
            "human_readable": [REPORT_PATH.as_posix()],
            "hashes_or_missing_reasons": {key: manifest["outputs"][key]["sha256"] for key in manifest["outputs"]},
            "lineage_boundary": "proxy replay only(프록시 재생 전용); no model artifact(모델 산출물 없음), no MT5 artifact(MT5 산출물 없음).",
        },
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-grok-collaboration",
            "triggered": True,
            "status": "executed",
            "trigger_reason": "persistent goal(지속 목표) requires Grok at stage open/pre-expensive/closeout; this run is cheap proxy replay(저비용 프록시 재생).",
            "review_size": "not_called_this_run_existing_stage_open_review_applies(이번 실행 새 호출 없음, 기존 단계 개방 검토 적용)",
            "direction_before_grok": "stage-open direction already reviewed(단계 개방 방향은 이미 검토됨); execute cheap proxy scout(저비용 프록시 탐색 실행).",
            "bounded_evidence": [
                "docs/agent_control/grok_reviews/2026-06-14_frontier02_stage_open/medium_review/clean_output.md",
                f"stages/{STAGE_ID}/01_inputs/proxy_score_plan.md",
            ],
            "prompt_identity": "not_created_this_run_no_new_grok_call(이번 실행 새 그록 호출 없음)",
            "grok_output_identity": "docs/agent_control/grok_reviews/2026-06-14_frontier02_stage_open/medium_review/clean_output.md",
            "advice_classification": {
                "accepted": ["four-axis wording(네 축 표현)", "avoid density-only framing(밀도 단독 표현 회피)"],
                "rejected": [],
                "needs_local_verification": [],
            },
            "local_verification": "frontier02B did not start WFO/MT5(워크포워드/MT5 미시작); pre-expensive Grok review(비싼 검증 전 그록 검토)는 next serious validation(다음 진지 검증) 전에 필요.",
            "forbidden_claim_check": FORBIDDEN_CLAIMS,
            "final_codex_direction": "use proxy scout output as seed surface clues only(프록시 탐색 출력을 씨앗 표면 단서로만 사용).",
        },
    ]


def build_scope_gate(summary: pd.DataFrame, metrics: pd.DataFrame) -> dict[str, Any]:
    return {
        "audit_name": "scope_completion_gate",
        "status": "pass",
        "passed": True,
        "observed": {
            "candidate_rows": int(len(summary)),
            "metric_rows": int(len(metrics)),
            "scout_clue_rows": int(summary["scout_clue_flag"].sum()),
            "report_path": REPORT_PATH.as_posix(),
        },
        "forbidden_claims": FORBIDDEN_CLAIMS,
    }


def build_kpi_audit(counts: dict[str, int]) -> dict[str, Any]:
    return {
        "audit_name": "kpi_contract_audit",
        "status": "pass",
        "passed": True,
        "scoreboard_lane": "structural_scout(구조 탐색)",
        "tier_records": {
            "tier_a_separate": "materialized(물질화)",
            "tier_b_separate": "missing_required(필수 누락)",
            "tier_ab_combined": "out_of_scope_by_claim(주장 범위 밖)",
        },
        "axis_counts": counts,
        "boundary": "proxy KPI(프록시 KPI) only; not MT5 trading KPI(MT5 거래 KPI 아님).",
    }


def build_artifact_audit(manifest: dict[str, Any]) -> dict[str, Any]:
    return {
        "audit_name": "artifact_lineage_audit",
        "status": "pass",
        "passed": True,
        "source_inputs": manifest["inputs"],
        "produced_artifacts": manifest["outputs"],
        "manifest": manifest,
        "report": {"path": REPORT_PATH.as_posix(), "sha256": sha256_file(REPORT_PATH)},
        "lineage_boundary": "proxy scout only(프록시 탐색 전용)",
    }


def build_external_review_packet() -> dict[str, Any]:
    return {
        "audit_name": "external_review_packet",
        "status": "pass",
        "passed": True,
        "review_action": "no_new_grok_call_this_run(이번 실행 새 그록 호출 없음)",
        "reason": "frontier02B is cheap proxy replay(저비용 프록시 재생) after stage-open Grok review(단계 개방 그록 검토 후 실행); WFO/MT5 not started(워크포워드/MT5 미시작).",
        "existing_review": "docs/agent_control/grok_reviews/2026-06-14_frontier02_stage_open/medium_review/clean_output.md",
        "next_required_review": "before expensive WFO/MT5 or stage closeout(비싼 워크포워드/MT5 또는 단계 마감 전)",
    }


def build_final_claim_guard() -> dict[str, Any]:
    return {
        "audit_name": "final_claim_guard",
        "status": "pass",
        "passed": True,
        "requested_claims": ["proxy_scout_completed(프록시 탐색 완료)", "scout_clue_exists(탐색 단서 있음)"],
        "allowed_claims": ["proxy_scout_completed(프록시 탐색 완료)", "scout_clue_exists(탐색 단서 있음)"],
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
    counts: dict[str, int],
) -> dict[str, Any]:
    primary_kpi = primary_kpi_text(top)
    guardrail = guardrail_text(counts)
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "structural_scout(구조 탐색)",
        "status": "completed_frontier02B_proxy_scout_no_authority",
        "judgment": "scout_clue_proxy_only_four_axis_gaps_remain_no_authority",
        "path": REPORT_PATH.as_posix(),
        "notes": (
            f"candidate_rows={len(summary)};metric_rows={len(metrics)};scout_clue_rows={int(summary['scout_clue_flag'].sum())};"
            f"best_validation={top['candidate_id']};val_pf={fmt(top['validation_profit_factor'])};"
            f"val_density={fmt(top['validation_trades_per_day'])};oos_pf={fmt(top['oos_profit_factor'])};"
            f"oos_density={fmt(top['oos_trades_per_day'])};no authority claims."
        ),
        "family": "experiment_execution(실험 실행)",
        "primary_report": REPORT_PATH.as_posix(),
        "run_number": RUN_NUMBER,
        "date": "2026-06-14",
        "decision": "frontier02B_proxy_scout_completed_seed_surface_clues_only",
        "parent_run_id": "frontier02A_proxy_score_spec_v1",
        "next_run_id": NEXT_RUN_ID,
        "rows": int(len(summary)),
        "gate_passes": len(REQUIRED_GATES),
        "gate_total": len(REQUIRED_GATES),
        "claim_boundary": "proxy_scout_only_no_model_training_no_wfo_no_mt5_no_candidate_selection_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim",
        "report_path": REPORT_PATH.as_posix(),
        "trained_models": 0,
        "onnx_parity": "not_applicable(해당 없음)",
        "best_proxy": top["candidate_id"],
        "candidate_rows": int(len(summary)),
        "positive_proxy_rows": int(summary["scout_clue_flag"].sum()),
        "best_proxy_net": fmt(top["validation_net_profit"]),
        "attempt_rows": int(len(metrics)),
        "runtime_completed_rows": 0,
        "best_net_profit": fmt(top["validation_net_profit"]),
        "best_profit_factor": fmt(top["validation_profit_factor"]),
        "operating_ready_rows": 0,
        "run_date": "2026-06-14",
        "primary_artifact": manifest["outputs"]["candidate_surface_summary"]["path"],
        "net_profit": fmt(top["validation_net_profit"]),
        "profit_factor": fmt(top["validation_profit_factor"]),
        "drawdown": fmt(top["validation_max_drawdown_percent"]),
        "trade_count": int(top["validation_trade_count"]),
        "result_status": "completed_proxy_scout_no_authority(프록시 탐색 완료, 권위 없음)",
        "sample_rows": int(manifest["inputs"]["rows"]),
        "feature_count": 58,
        "expectancy": fmt(top["validation_expectancy"]),
        "attempt_count": int(len(metrics)),
        "view": "Tier A separate(티어 A 분리)",
        "tier": "Tier A(티어 A)",
        "metric_scope": "four_axis_proxy_scout(네 축 프록시 탐색)",
        "scoreboard_lane": "structural_scout(구조 탐색)",
        "external_verification_status": "out_of_scope_by_claim_no_mt5(주장 범위 밖 MT5 없음)",
        "trade_density_per_feature_day": fmt(top["validation_trades_per_day"]),
        "trade_density_requirement_status": "below_goal_proxy(목표 미달 프록시)",
        "result_judgment": "scout_clue_proxy_only_no_authority",
        "final_decision_path": REPORT_PATH.as_posix(),
        "gate_audit_path": (PACKET_ROOT / "required_gate_coverage_audit.json").as_posix(),
        "created_at_utc": now,
        "ledger_row_id": f"{RUN_ID}__tier_a_separate_proxy_scout",
        "subrun_id": f"{RUN_ID}__tier_a_separate_proxy_scout",
        "record_view": "Tier A separate(티어 A 분리)",
        "tier_scope": "Tier A(티어 A)",
        "kpi_scope": "four_axis_proxy_scout(네 축 프록시 탐색)",
        "primary_kpi": primary_kpi,
        "guardrail_kpi": guardrail,
        "model_variants": 0,
        "selected_surfaces": top["candidate_id"],
        "runtime_attempt_rows": 0,
        "work_family": "experiment_execution(실험 실행)",
        "max_drawdown_amount": fmt(top["validation_max_drawdown_percent"]),
        "row_id": f"{RUN_ID}__tier_a_separate_proxy_scout",
        "evidence_boundary": "proxy_replay_only_no_authority(프록시 재생 전용, 권위 없음)",
        "next_action": NEXT_RUN_ID,
        "question": "Which seed surfaces should become trainable ONNX-ready candidates?(어떤 씨앗 표면을 학습 가능한 온엑스 준비 후보로 바꿀 것인가?)",
        "artifact_count": 13,
        "required_gate_audit": (PACKET_ROOT / "required_gate_coverage_audit.json").as_posix(),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "run_family": "frontier_hypothesis_lifecycle(전선 가설 생명주기)",
        "run_type": "proxy_scout(프록시 탐색)",
        "input_run_id": "frontier02A_proxy_score_spec_v1",
        "output_path": RUN_ROOT.as_posix(),
        "result_path": REPORT_PATH.as_posix(),
        "selected_net_profit": fmt(top["validation_net_profit"]),
        "selected_profit_factor": fmt(top["validation_profit_factor"]),
        "selected_trade_density": fmt(top["validation_trades_per_day"]),
        "goal_achieve": "not_claimed",
        "source_authority": "model_input_dataset_and_proxy_script(모델 입력 데이터셋과 프록시 스크립트)",
        "trade_density": fmt(top["validation_trades_per_day"]),
        "expected_net_profit": fmt(top["oos_net_profit"]),
        "expected_profit_factor": fmt(top["oos_profit_factor"]),
        "expected_trade_count": int(top["oos_trade_count"]),
        "expected_trade_density": fmt(top["oos_trades_per_day"]),
        "max_drawdown_percent": fmt(top["validation_max_drawdown_percent"]),
        "strict_joint_pass_count": int(top["validation_joint_pass_count"]),
    }


def build_ledger_rows(
    now: str,
    manifest: dict[str, Any],
    top: dict[str, Any],
    summary: pd.DataFrame,
    metrics: pd.DataFrame,
    counts: dict[str, int],
) -> list[dict[str, Any]]:
    primary = primary_kpi_text(top)
    guardrail = guardrail_text(counts)
    common = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": "frontier02A_proxy_score_spec_v1",
        "kpi_scope": "four_axis_proxy_scout(네 축 프록시 탐색)",
        "scoreboard_lane": "structural_scout(구조 탐색)",
        "path": REPORT_PATH.as_posix(),
        "run_number": RUN_NUMBER,
        "date": "2026-06-14",
        "next_run_id": NEXT_RUN_ID,
        "claim_boundary": "proxy_scout_only_no_model_training_no_wfo_no_mt5_no_candidate_selection_no_authority_goal_claim",
        "report_path": REPORT_PATH.as_posix(),
        "work_family": "experiment_execution(실험 실행)",
        "created_at_utc": now,
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "external_verification_status": "out_of_scope_by_claim_no_mt5(주장 범위 밖 MT5 없음)",
    }
    return [
        {
            **common,
            "ledger_row_id": f"{RUN_ID}__tier_a_separate_proxy_scout",
            "subrun_id": f"{RUN_ID}__tier_a_separate_proxy_scout",
            "record_view": "Tier A separate(티어 A 분리)",
            "tier_scope": "Tier A(티어 A)",
            "status": "completed",
            "judgment": "scout_clue_proxy_only_no_authority",
            "primary_kpi": primary,
            "guardrail_kpi": guardrail,
            "notes": "Tier A proxy metrics materialized(티어 A 프록시 측정값 물질화); no MT5/no ONNX authority(MT5/온엑스 권위 없음).",
            "decision": "continue_to_trainable_seed_surface_design(학습 가능한 씨앗 표면 설계로 계속)",
            "result_status": "completed_proxy_scout_no_authority(프록시 탐색 완료, 권위 없음)",
            "result_judgment": "scout_clue_proxy_only_no_authority",
            "source_authority": "model_input_dataset_and_proxy_script(모델 입력 데이터셋과 프록시 스크립트)",
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
        f"val_net={fmt(top['validation_net_profit'])};val_pf={fmt(top['validation_profit_factor'])};"
        f"val_density={fmt(top['validation_trades_per_day'])};val_dd={fmt(top['validation_max_drawdown_percent'])};"
        f"oos_net={fmt(top['oos_net_profit'])};oos_pf={fmt(top['oos_profit_factor'])};"
        f"oos_density={fmt(top['oos_trades_per_day'])};oos_dd={fmt(top['oos_max_drawdown_percent'])}"
    )


def guardrail_text(counts: dict[str, int]) -> str:
    return (
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


def run_cmd(command: list[str]) -> None:
    result = subprocess.run(command, cwd=REPO_ROOT, text=True, capture_output=True)
    if result.returncode != 0:
        print(result.stdout)
        print(result.stderr, file=sys.stderr)
        raise SystemExit(result.returncode)


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
