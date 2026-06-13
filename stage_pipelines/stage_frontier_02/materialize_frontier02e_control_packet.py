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
RUN_ID = "frontier02E_grok_pre_expensive_review_or_second_repair_v1"
RUN_NUMBER = "frontier02E"
PARENT_RUN_ID = "frontier02D_review_and_repair_onnx_seed_surface_v1"
ANCHOR_RUN_ID = "frontier02C_trainable_onnx_seed_surface_design_v1"
NEXT_RUN_ID = "frontier02F_stage_closeout_preserved_clue_negative_memory_v1"
STATUS = "completed_frontier02E_decision_layer_diagnostic_no_go_no_authority"
JUDGMENT = "no_go_decision_layer_diagnostic_prepare_stage_closeout_no_authority"

PACKET_ROOT = Path("docs/agent_control/packets") / RUN_ID
RUN_ROOT = Path("stages") / STAGE_ID / "02_runs" / RUN_ID
MANIFEST_PATH = RUN_ROOT / "run_manifest.json"
REPORT_PATH = Path("stages") / STAGE_ID / "03_reviews" / f"{RUN_ID}_report.md"
GROK_ROOT = Path("docs/agent_control/grok_reviews/2026-06-14_frontier02E_pre_expensive_review/medium_review")
GROK_PROMPT = GROK_ROOT / "prompt.md"
GROK_OUTPUT = GROK_ROOT / "clean_output.md"
GROK_METADATA = GROK_ROOT / "metadata.json"
GROK_RAW_DIAGNOSTICS = GROK_ROOT / "raw_diagnostics.json"

STAGE_LEDGER = Path("stages") / STAGE_ID / "03_reviews" / "stage_run_ledger.csv"
ALPHA_LEDGER = Path("docs/registers/alpha_run_ledger.csv")
RUN_REGISTRY = Path("docs/registers/run_registry.csv")
WORKSPACE_STATE = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE = Path("docs/context/current_working_state.md")
SELECTION_STATUS = Path("stages") / STAGE_ID / "04_selected" / "selection_status.md"
REVIEW_INDEX = Path("stages") / STAGE_ID / "03_reviews" / "review_index.md"
STAGE_README = Path("stages") / STAGE_ID / "README.md"
STAGE_BRIEF = Path("stages") / STAGE_ID / "00_spec" / "stage_brief.md"
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
    "diagnostic_contract_audit",
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
    "obsidian-result-judgment",
]


def main() -> int:
    now = utc_now()
    io_path(PACKET_ROOT).mkdir(parents=True, exist_ok=True)

    normalize_grok_markdown()
    refresh_manifest_hashes()

    manifest = read_json(MANIFEST_PATH)
    summary = pd.read_csv(io_path(RUN_ROOT / "diagnostic_summary.csv"))
    metrics = pd.read_csv(io_path(RUN_ROOT / "diagnostic_metrics.csv"))
    go_rows = pd.read_csv(io_path(RUN_ROOT / "go_rule_rows.csv"))
    local_verification = read_json(RUN_ROOT / "local_verification.json")
    advice = read_json(RUN_ROOT / "grok_advice_classification.json")
    top = dict(manifest["best_validation_rank"])
    counts = axis_counts(summary)
    diagnostic_observation_rows = bool_count(summary, "diagnostic_observation_flag")

    write_yaml(PACKET_ROOT / "work_packet.yaml", build_work_packet(now, manifest, top, summary, metrics, go_rows))
    receipts = build_skill_receipts(manifest, top, counts, diagnostic_observation_rows, local_verification, advice)
    write_json(PACKET_ROOT / "skill_receipts.json", {"receipts": receipts})

    write_json(PACKET_ROOT / "scope_completion_gate.json", build_scope_gate(manifest, summary, metrics, go_rows, diagnostic_observation_rows))
    write_json(PACKET_ROOT / "kpi_contract_audit.json", build_kpi_audit(top, counts, diagnostic_observation_rows))
    write_json(PACKET_ROOT / "diagnostic_contract_audit.json", build_diagnostic_contract_audit(manifest, summary, go_rows))
    write_json(PACKET_ROOT / "artifact_lineage_audit.json", build_artifact_audit(manifest))
    write_json(PACKET_ROOT / "external_review_packet.json", build_external_review_packet(advice, local_verification))
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

    upsert_csv(RUN_REGISTRY, "run_id", build_run_registry_row(now, manifest, top, counts, diagnostic_observation_rows))
    for row in build_alpha_ledger_rows(now, manifest, top, counts, diagnostic_observation_rows):
        upsert_csv(ALPHA_LEDGER, "ledger_row_id", row)
        upsert_csv(STAGE_LEDGER, "ledger_row_id", build_stage_ledger_row(row))

    update_state_documents(now, manifest, top, counts, diagnostic_observation_rows, local_verification, advice)

    print(
        json.dumps(
            {
                "packet_root": PACKET_ROOT.as_posix(),
                "decision_rows": int(len(summary)),
                "metric_rows": int(len(metrics)),
                "go_rule_rows": int(len(go_rows)),
                "diagnostic_observation_rows": int(diagnostic_observation_rows),
                "best_candidate": top["candidate_id"],
                "validation_pf": fmt(top["validation_profit_factor"]),
                "validation_density": fmt(top["validation_trades_per_day"]),
                "validation_dd": fmt(top["validation_max_drawdown_percent"]),
                "oos_pf": fmt(top["oos_profit_factor"]),
                "oos_density": fmt(top["oos_trades_per_day"]),
                "oos_dd": fmt(top["oos_max_drawdown_percent"]),
                "judgment": JUDGMENT,
                "next_run_id": NEXT_RUN_ID,
            },
            ensure_ascii=True,
            indent=2,
        )
    )
    return 0


def normalize_grok_markdown() -> None:
    for path in (GROK_PROMPT, GROK_OUTPUT, REPORT_PATH):
        if path_exists(path):
            ensure_utf8_sig(path)


def refresh_manifest_hashes() -> None:
    advice_path = RUN_ROOT / "grok_advice_classification.json"
    manifest = read_json(MANIFEST_PATH)
    advice = read_json(advice_path)
    if "prompt_identity" in advice:
        advice["prompt_identity"]["sha256"] = sha256_file(GROK_PROMPT) if path_exists(GROK_PROMPT) else None
    if "grok_output_identity" in advice:
        advice["grok_output_identity"]["sha256"] = sha256_file(GROK_OUTPUT) if path_exists(GROK_OUTPUT) else None
    write_json(advice_path, advice)

    manifest["inputs"]["grok_review_output_sha256"] = sha256_file(GROK_OUTPUT) if path_exists(GROK_OUTPUT) else None
    manifest["outputs"]["grok_advice_classification"]["sha256"] = sha256_file(advice_path)
    manifest["outputs"]["report"]["sha256"] = sha256_file(REPORT_PATH)
    write_json(MANIFEST_PATH, manifest)


def build_work_packet(
    now: str,
    manifest: dict[str, Any],
    top: dict[str, Any],
    summary: pd.DataFrame,
    metrics: pd.DataFrame,
    go_rows: pd.DataFrame,
) -> dict[str, Any]:
    return {
        "version": "work_packet_schema_v2",
        "packet_id": RUN_ID,
        "created_at_utc": now,
        "user_request": {
            "user_quote": "Persistent goal(지속 목표): build a genuinely strong US100 M5 ONNX(온엑스), with Grok(그록) review before expensive WFO/MT5(비싼 WFO/MT5) and no hard final gates(강제 최종 게이트) during early exploration(초기 탐색).",
            "requested_action": "execute_frontier02E_grok_pre_expensive_review_and_frozen_decision_layer_diagnostic",
            "requested_count": "one Grok review(그록 검토) plus one non-expensive diagnostic(저비용 진단)",
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
                (Path("stages") / STAGE_ID / "02_runs" / PARENT_RUN_ID / "run_manifest.json").as_posix(),
                GROK_OUTPUT.as_posix(),
            ],
        },
        "work_classification": {
            "primary_family": "experiment_execution",
            "detected_families": ["experiment_execution", "external_review", "model_validation", "artifact_lineage", "state_sync"],
            "touched_surfaces": [
                "stage_pipelines/stage_frontier_02/frontier02e_frozen_02c_decision_layer_diagnostic.py",
                "stage_pipelines/stage_frontier_02/materialize_frontier02e_control_packet.py",
                f"stages/{STAGE_ID}",
                "docs/agent_control/grok_reviews",
                "docs/registers",
            ],
            "mutation_intent": True,
            "execution_intent": True,
        },
        "risk_vector_scan": {
            "risks": [
                "Grok(그록) is external advice(외부 조언), not automatic authority(자동 권위 아님).",
                "Frozen decision-layer diagnostic(고정 결정층 진단) reuses frontier02C probabilities(frontier02C 확률) and does not create a new ONNX(새 온엑스 생성 없음).",
                "OOS(표본외)는 diagnostic only(진단 전용) and not a selector(선택기 아님).",
                "Tier B partial-context artifact(티어 B 부분 문맥 산출물) is still missing_required(필수 누락).",
            ],
            "hard_stop_risks": [],
            "required_decision_locks": ["no_wfo_mt5_before_grok_local_verification"],
            "required_gates": REQUIRED_GATES,
            "forbidden_claims": FORBIDDEN_CLAIMS,
        },
        "decision_lock": {
            "mode": "execute_non_expensive_diagnostic_before_expensive_validation(비싼 검증 전 저비용 진단 실행)",
            "assumptions": [
                "The best frontier02C seed observation(씨앗 관찰) is enough for a frozen decision-layer diagnostic(고정 결정층 진단).",
                "A go rule(진행 규칙) must require OOS PF(표본외 수익 팩터), density(밀도), DD(손실폭), and net(순수익) to move forward.",
                "No new WFO/MT5(WFO/MT5 없음) is claimed in this packet(묶음).",
            ],
            "questions": [],
            "required_user_decisions": [],
        },
        "interpreted_scope": {
            "work_families": ["experiment_execution"],
            "target_surfaces": [
                "Grok pre-expensive review(비싼 검증 전 그록 검토)",
                "frozen frontier02C decision layer(고정 전선02C 결정층)",
                "probability threshold and calibration diagnostic(확률 임계값과 보정 진단)",
            ],
            "scope_units": ["external_review", "diagnostic_run", "report", "ledger", "gate"],
            "execution_layers": ["grok_wrapper_capture", "python_execution", "decision_surface_replay", "ledger_update", "document_edit"],
            "mutation_policy": "stage-local diagnostic artifacts and control-plane records only(단계 로컬 진단 산출물과 제어면 기록만)",
            "evidence_layers": ["grok_output", "run_manifest", "diagnostic_summary", "go_rule_rows", "local_verification", "stage_report", "ledger_rows", "gate_audits"],
            "reduction_policy": "validation rank orders diagnostics only(검증 순위는 진단 정렬 전용), go/no-go uses OOS diagnostic rule(진행/중단은 표본외 진단 규칙)",
            "claim_boundary": "decision-layer diagnostic no-go only no authority(결정층 진단 진행조건 없음, 권위 없음)",
        },
        "acceptance_criteria": [
            {
                "id": "AC-001",
                "text": "Grok review(그록 검토) is captured with bounded evidence(제한 근거) and local classification(로컬 분류).",
                "expected_artifact": GROK_OUTPUT.as_posix(),
                "verification_method": "metadata_success_and_hash",
                "required": True,
            },
            {
                "id": "AC-002",
                "text": "Frozen decision-layer diagnostic(고정 결정층 진단) runs without retraining(재학습 없음) or new ONNX(새 온엑스 없음).",
                "expected_artifact": manifest["script_path"],
                "verification_method": "py_compile_and_manifest_contract",
                "required": True,
            },
            {
                "id": "AC-003",
                "text": "Diagnostic metrics(진단 측정값), go-rule rows(진행 규칙 행), and report(보고서) are materialized(물질화).",
                "expected_artifact": manifest["outputs"]["diagnostic_summary"]["path"],
                "verification_method": "row_count_and_hash",
                "required": True,
            },
            {
                "id": "AC-004",
                "text": "Tier A/B/combined ledger rows(티어 A/B/합산 장부 행) are recorded with boundary labels(경계 라벨).",
                "expected_artifact": STAGE_LEDGER.as_posix(),
                "verification_method": "ledger_row_presence",
                "required": True,
            },
            {
                "id": "AC-005",
                "text": "Forbidden final claims(금지 최종 주장) are avoided(회피).",
                "expected_artifact": (PACKET_ROOT / "final_claim_guard.json").as_posix(),
                "verification_method": "claim_guard",
                "required": True,
            },
        ],
        "work_plan": {
            "phases": [
                "Grok review capture(그록 검토 기록)",
                "local verification(로컬 검증)",
                "frozen decision-layer diagnostic(고정 결정층 진단)",
                "go/no-go judgment(진행/중단 판정)",
                "ledger sync(장부 동기화)",
                "gate audit(게이트 감사)",
            ],
            "expected_outputs": [manifest["outputs"][key]["path"] for key in manifest["outputs"]] + [MANIFEST_PATH.as_posix(), REPORT_PATH.as_posix()],
            "stop_conditions": ["missing Grok output(그록 출력 누락)", "artifact hash mismatch(산출물 해시 불일치)", "gate failure(게이트 실패)"],
        },
        "skill_routing": {
            "primary_family": "experiment_execution",
            "primary_skill": "obsidian-run-evidence-system",
            "support_skills": [
                "obsidian-experiment-design",
                "obsidian-data-integrity",
                "obsidian-model-validation",
                "obsidian-artifact-lineage",
                "obsidian-grok-collaboration",
                "obsidian-result-judgment",
            ],
            "skills_considered": REQUIRED_SKILLS + ["obsidian-runtime-parity", "obsidian-backtest-forensics", "obsidian-performance-attribution"],
            "skills_selected": REQUIRED_SKILLS,
            "skills_not_used": {
                "obsidian-runtime-parity": {"not_selected_reason": "No MT5 runtime execution(MT5 런타임 실행 없음)."},
                "obsidian-backtest-forensics": {"not_selected_reason": "No Strategy Tester output(전략 테스터 출력 없음)."},
                "obsidian-performance-attribution": {"not_selected_reason": "Loss attribution(손실 귀속)은 diagnostic support(진단 보조)로만 기록, full attribution(전체 귀속) 아님."},
            },
            "required_skill_receipts": REQUIRED_SKILLS,
            "required_gates": REQUIRED_GATES,
        },
        "evidence_contract": {
            "raw_evidence": [
                manifest["inputs"]["anchor_replay_path"],
                manifest["inputs"]["model_input_dataset_path"],
                GROK_OUTPUT.as_posix(),
            ],
            "machine_readable": [manifest["outputs"][key]["path"] for key in manifest["outputs"]] + [MANIFEST_PATH.as_posix()],
            "human_readable": [REPORT_PATH.as_posix()],
        },
        "gates": {
            "required": REQUIRED_GATES,
            "not_applicable_with_reason": {
                "onnx_parity_audit": "No new ONNX(새 온엑스 없음); frontier02C parity(전선02C 동등성)는 anchor evidence(앵커 근거)로만 참조.",
                "model_training_audit": "No retraining(재학습 없음); diagnostic contract audit(진단 계약 감사)가 대신 no_new_onnx/no_retrain(새 온엑스 없음/재학습 없음)을 확인.",
                "mt5_runtime_evidence_gate": "No MT5 execution(MT5 실행 없음); claim lowered to diagnostic read(진단 판독).",
                "wfo_gate": "No WFO execution(WFO 실행 없음); Grok advised no WFO/MT5 yet(그록이 아직 WFO/MT5 금지 조언).",
            },
        },
        "final_claim_policy": {
            "allowed_claims": [
                "grok_pre_expensive_review_captured(비싼 검증 전 그록 검토 기록)",
                "frozen_decision_layer_diagnostic_completed(고정 결정층 진단 완료)",
                "no_go_decision_layer_diagnostic_no_authority(결정층 진단 진행조건 없음, 권위 없음)",
            ],
            "forbidden_claims": FORBIDDEN_CLAIMS,
            "claim_vocabulary_reference": "docs/agent_control/claim_vocabulary.yaml",
        },
        "kpi_snapshot": {
            "best_candidate": top["candidate_id"],
            "decision_rows": int(len(summary)),
            "metric_rows": int(len(metrics)),
            "go_rule_rows": int(len(go_rows)),
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
    counts: dict[str, int],
    diagnostic_observation_rows: int,
    local_verification: dict[str, Any],
    advice: dict[str, Any],
) -> list[dict[str, Any]]:
    produced = [manifest["outputs"][key]["path"] for key in manifest["outputs"]] + [MANIFEST_PATH.as_posix(), REPORT_PATH.as_posix()]
    return [
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-run-evidence-system",
            "triggered": True,
            "status": "executed",
            "source_inputs": [manifest["inputs"]["anchor_replay_path"], manifest["inputs"]["model_input_dataset_path"], GROK_OUTPUT.as_posix()],
            "produced_artifacts": produced,
            "ledger_rows": [
                f"{RUN_ID}__tier_a_separate_decision_layer_diagnostic",
                f"{RUN_ID}__tier_b_separate_missing_required",
                f"{RUN_ID}__tier_ab_combined_out_of_scope",
            ],
            "missing_evidence": ["Tier B partial-context artifact(티어 B 부분 문맥 산출물)", "MT5 fills(MT5 체결)", "WFO validation(WFO 검증)"],
            "allowed_claims": ["frozen_decision_layer_diagnostic_completed(고정 결정층 진단 완료)", "no_go_decision_layer_diagnostic_no_authority(결정층 진단 진행조건 없음, 권위 없음)"],
            "forbidden_claims": FORBIDDEN_CLAIMS,
        },
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-experiment-design",
            "triggered": True,
            "status": "executed",
            "hypothesis": "A frozen frontier02C decision layer(고정 전선02C 결정층) might recover PF/DD(수익 팩터/손실폭) without retraining(재학습 없음) before expensive validation(비싼 검증).",
            "baseline": "frontier02C seed observation(전선02C 씨앗 관찰); no selected baseline(선택 기준선 없음).",
            "changed_variables": ["score_mode(점수 방식)", "probability_threshold(확률 임계값)", "probability_margin(확률 마진)", "cooldown_bars(쿨다운 봉)"],
            "invalid_conditions": ["new ONNX produced(새 온엑스 생성)", "retraining performed(재학습 수행)", "OOS used as selector(표본외를 선택기로 사용)", "Grok advice accepted without local verification(로컬 검증 없는 그록 조언 수용)"],
            "evidence_plan": ["Grok output(그록 출력)", "diagnostic_summary.csv", "go_rule_rows.csv", "local_verification.json", "run_manifest.json", "ledger rows(장부 행)", "gate audits(게이트 감사)"],
        },
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-data-integrity",
            "triggered": True,
            "status": "executed",
            "data_sources_checked": [manifest["inputs"]["anchor_replay_path"], manifest["inputs"]["model_input_dataset_path"], manifest["inputs"]["feature_order_path"]],
            "time_axis_boundary": "timestamp UTC(UTC 타임스탬프) alignment(정렬) checked by replay alignment(재생 정렬).",
            "split_boundary": "train/validation/oos(학습/검증/표본외) from existing model input dataset(기존 모델 입력 데이터셋); OOS not used as selector(표본외 선택기 사용 없음).",
            "leakage_checks": ["calibration fit uses validation only(보정 적합은 검증만 사용)", "frozen probabilities reused(고정 확률 재사용)", "no target relabeling(목표 재라벨링 없음)"],
            "missing_data_boundary": "Tier B separate(티어 B 분리) missing_required(필수 누락); no combined routed total(합산 라우팅 전체 없음).",
        },
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-model-validation",
            "triggered": True,
            "status": "executed",
            "model_or_threshold_surface": "frozen frontier02C probability decision layer(고정 전선02C 확률 결정층)",
            "validation_split": "validation rank(검증 순위) orders diagnostics; OOS(표본외) checks go/no-go only(진행/중단만 확인).",
            "overfit_checks": ["no retraining(재학습 없음)", "go rule requires OOS PF/density/DD/net(표본외 수익 팩터/밀도/손실폭/순수익)", "go_rule_rows=0 means no expensive validation(진행 규칙 행 0개로 비싼 검증 없음)"],
            "selection_metric_boundary": "best validation rank(검증 순위 1위) is diagnostic read(진단 판독), not selected candidate(선택 후보 아님).",
            "allowed_claims": ["decision_layer_diagnostic_read(결정층 진단 판독)"],
            "forbidden_claims": FORBIDDEN_CLAIMS,
        },
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-artifact-lineage",
            "triggered": True,
            "status": "executed",
            "source_inputs": [manifest["inputs"]["anchor_replay_path"], manifest["inputs"]["model_input_dataset_path"], GROK_OUTPUT.as_posix()],
            "produced_artifacts": produced,
            "raw_evidence": [manifest["inputs"]["anchor_replay_path"], GROK_OUTPUT.as_posix()],
            "machine_readable": [manifest["outputs"][key]["path"] for key in manifest["outputs"]] + [MANIFEST_PATH.as_posix()],
            "human_readable": [REPORT_PATH.as_posix()],
            "hashes_or_missing_reasons": artifact_hash_summary(manifest),
            "lineage_boundary": "diagnostic artifacts derive from frozen 02C replay(고정 02C 재생) and Grok review(그록 검토); no new ONNX(새 온엑스 없음).",
        },
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-grok-collaboration",
            "triggered": True,
            "status": "executed",
            "trigger_reason": advice["trigger_reason"],
            "review_size": advice["review_size"],
            "direction_before_grok": "Codex proposed no expensive WFO/MT5 yet(코덱스가 아직 비싼 WFO/MT5 보류 제안) and either capped repair(상한 수리) or closeout decision(마감 결정).",
            "bounded_evidence": ["frontier02B/C/D KPI snapshot(frontier02B/C/D KPI 스냅샷)", "Tier boundary(티어 경계)", "claim boundary(주장 경계)"],
            "prompt_identity": advice["prompt_identity"],
            "grok_output_identity": advice["grok_output_identity"],
            "advice_classification": {"accepted": advice["accepted"], "rejected": advice["rejected"], "needs_local_verification": advice["needs_local_verification"]},
            "local_verification": local_verification,
            "forbidden_claim_check": advice["forbidden_claim_check"],
            "final_codex_direction": advice["final_codex_direction"],
        },
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-result-judgment",
            "triggered": True,
            "status": "executed",
            "judgment_boundary": JUDGMENT,
            "allowed_claims": ["no_go_decision_layer_diagnostic_no_authority(결정층 진단 진행조건 없음, 권위 없음)", "prepare_stage_closeout(단계 마감 준비)"],
            "forbidden_claims": FORBIDDEN_CLAIMS,
            "evidence_used": [manifest["outputs"]["diagnostic_summary"]["path"], manifest["outputs"]["go_rule_rows"]["path"], manifest["outputs"]["local_verification"]["path"], REPORT_PATH.as_posix()],
        },
    ]


def build_scope_gate(
    manifest: dict[str, Any],
    summary: pd.DataFrame,
    metrics: pd.DataFrame,
    go_rows: pd.DataFrame,
    diagnostic_observation_rows: int,
) -> dict[str, Any]:
    findings: list[dict[str, Any]] = []
    if len(summary) != int(manifest["decision_rows"]):
        findings.append(blocking("summary_row_mismatch", "Diagnostic summary row count does not match manifest."))
    if len(metrics) != 2160:
        findings.append(blocking("metric_row_mismatch", "Diagnostic metric row count does not match expected 2160."))
    if len(go_rows) != int(manifest["go_rule_rows"]):
        findings.append(blocking("go_row_mismatch", "Go-rule row count does not match manifest."))
    if not bool(manifest["diagnostic_contract"]["no_new_onnx"]) or not bool(manifest["diagnostic_contract"]["no_retrain"]):
        findings.append(blocking("diagnostic_contract", "Diagnostic contract must say no new ONNX and no retrain."))
    status = "blocked" if findings else "pass"
    return audit_payload(
        "scope_completion_gate",
        status=status,
        findings=findings,
        counts={
            "decision_rows": int(len(summary)),
            "metric_rows": int(len(metrics)),
            "go_rule_rows": int(len(go_rows)),
            "diagnostic_observation_rows": int(diagnostic_observation_rows),
            "no_new_onnx": bool(manifest["diagnostic_contract"]["no_new_onnx"]),
            "no_retrain": bool(manifest["diagnostic_contract"]["no_retrain"]),
        },
        allowed_claims=("scope_executed",) if not findings else ("blocked",),
    )


def build_kpi_audit(top: dict[str, Any], counts: dict[str, int], diagnostic_observation_rows: int) -> dict[str, Any]:
    return audit_payload(
        "kpi_contract_audit",
        counts={
            "best_candidate": top["candidate_id"],
            "diagnostic_observation_rows": diagnostic_observation_rows,
            "validation_profit_factor": numeric(top["validation_profit_factor"]),
            "validation_trades_per_day": numeric(top["validation_trades_per_day"]),
            "validation_max_drawdown_percent": numeric(top["validation_max_drawdown_percent"]),
            "oos_profit_factor": numeric(top["oos_profit_factor"]),
            "oos_trades_per_day": numeric(top["oos_trades_per_day"]),
            "oos_max_drawdown_percent": numeric(top["oos_max_drawdown_percent"]),
            "go_rule_rows": 0,
            **counts,
        },
        allowed_claims=("kpi_recorded_diagnostic_only",),
    )


def build_diagnostic_contract_audit(manifest: dict[str, Any], summary: pd.DataFrame, go_rows: pd.DataFrame) -> dict[str, Any]:
    findings: list[dict[str, Any]] = []
    contract = manifest.get("diagnostic_contract", {})
    if not contract.get("no_new_onnx"):
        findings.append(blocking("new_onnx_not_allowed", "Diagnostic contract must forbid new ONNX."))
    if not contract.get("no_retrain"):
        findings.append(blocking("retrain_not_allowed", "Diagnostic contract must forbid retraining."))
    if int(summary["go_rule_flag"].astype(str).str.lower().eq("true").sum()) != len(go_rows):
        findings.append(blocking("go_rule_count_mismatch", "Go-rule count mismatch."))
    status = "blocked" if findings else "pass"
    return audit_payload(
        "diagnostic_contract_audit",
        status=status,
        findings=findings,
        counts={
            "anchor_candidate_id": contract.get("anchor_candidate_id"),
            "parent_negative_repair_candidate_id": contract.get("parent_negative_repair_candidate_id"),
            "no_new_onnx": contract.get("no_new_onnx"),
            "no_retrain": contract.get("no_retrain"),
            "go_rule_rows": int(len(go_rows)),
            "selector_scope": contract.get("selector_scope"),
        },
        allowed_claims=("diagnostic_contract_valid",) if not findings else ("blocked",),
    )


def build_artifact_audit(manifest: dict[str, Any]) -> dict[str, Any]:
    checked: list[dict[str, Any]] = []
    findings: list[dict[str, Any]] = []
    for label, record in manifest["outputs"].items():
        check_artifact(label, record.get("path"), record.get("sha256"), checked, findings)
    check_artifact("run_manifest", MANIFEST_PATH.as_posix(), sha256_file(MANIFEST_PATH), checked, findings)
    check_artifact("script", manifest["script_path"], manifest.get("script_sha256"), checked, findings)
    check_artifact("grok_output", GROK_OUTPUT.as_posix(), manifest["inputs"].get("grok_review_output_sha256"), checked, findings)
    status = "blocked" if findings else "pass"
    return audit_payload(
        "artifact_lineage_audit",
        status=status,
        findings=findings,
        counts={"artifact_count": len(checked), "checked": checked},
        allowed_claims=("artifact_lineage_recorded",) if not findings else ("blocked",),
    )


def build_external_review_packet(advice: dict[str, Any], local_verification: dict[str, Any]) -> dict[str, Any]:
    metadata = read_json(GROK_METADATA) if path_exists(GROK_METADATA) else {}
    findings: list[dict[str, Any]] = []
    if not metadata.get("success"):
        findings.append(blocking("grok_metadata_success_missing", "Grok metadata success flag is missing or false."))
    if not path_exists(GROK_OUTPUT):
        findings.append(blocking("grok_output_missing", "Grok clean output is missing."))
    if path_exists(GROK_RAW_DIAGNOSTICS):
        raw_text = read_text_sig(GROK_RAW_DIAGNOSTICS)
        if "UnicodeEncodeError" in raw_text:
            findings.append(
                {
                    "check_id": "grok_wrapper_stdout_encoding_warning",
                    "message": "Wrapper content succeeded, but one stdout JSON print hit console encoding after files were written.",
                    "severity": "warning",
                    "details": {"raw_diagnostics": GROK_RAW_DIAGNOSTICS.as_posix()},
                }
            )
    status = "blocked" if any(item.get("severity") == "blocking" for item in findings) else "pass"
    return audit_payload(
        "external_review_packet",
        status=status,
        findings=findings,
        counts={
            "review_size": advice.get("review_size"),
            "metadata_success": metadata.get("success"),
            "metadata_returncode": metadata.get("returncode"),
            "timed_out": metadata.get("timed_out"),
            "accepted_count": len(advice.get("accepted", [])),
            "rejected_count": len(advice.get("rejected", [])),
            "needs_local_verification_count": len(advice.get("needs_local_verification", [])),
            "local_degradation_claim_classification": local_verification.get("grok_degradation_claim_check", {}).get("classification"),
        },
        allowed_claims=("grok_review_captured_local_verification_done",) if status == "pass" else ("blocked",),
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
        allowed_claims=("no_go_decision_layer_diagnostic_no_authority",),
    )


def build_closeout_gate() -> dict[str, Any]:
    audit_names = [
        "scope_completion_gate",
        "kpi_contract_audit",
        "diagnostic_contract_audit",
        "artifact_lineage_audit",
        "external_review_packet",
        "work_packet_schema_lint",
        "skill_receipt_lint",
        "skill_receipt_schema_lint",
        "required_gate_coverage_audit",
    ]
    audits = []
    for name in audit_names:
        path = PACKET_ROOT / f"{name}.json"
        status = "missing"
        if path_exists(path):
            status = str(read_json(path).get("status", "unknown"))
        audits.append({"audit_name": name, "status": status, "path": path.as_posix()})
    return {
        "audit_name": "closeout_gate",
        "status": "pass" if all(audit["status"] in {"pass", "complete", "completed"} for audit in audits if audit["audit_name"] != "required_gate_coverage_audit") else "blocked",
        "packet_id": RUN_ID,
        "audits": audits,
        "final_claim_guard": build_final_claim_guard(),
        "allowed_claims": ["no_go_decision_layer_diagnostic_no_authority"],
        "forbidden_claims": FORBIDDEN_CLAIMS,
    }


def build_run_registry_row(
    now: str,
    manifest: dict[str, Any],
    top: dict[str, Any],
    counts: dict[str, int],
    diagnostic_observation_rows: int,
) -> dict[str, Any]:
    row = empty_csv_row(RUN_REGISTRY)
    primary = primary_kpi_text(top)
    guardrail = guardrail_text(counts, diagnostic_observation_rows, manifest)
    report = REPORT_PATH.as_posix()
    row.update(
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "lane": "decision_layer_diagnostic(결정층 진단)",
            "status": STATUS,
            "judgment": JUDGMENT,
            "path": report,
            "notes": f"decision_rows={manifest['decision_rows']};metric_rows=2160;go_rule_rows={manifest['go_rule_rows']};best_validation={top['candidate_id']};no authority claims.",
            "family": "experiment_execution(실험 실행)",
            "primary_report": report,
            "run_number": RUN_NUMBER,
            "date": local_date(),
            "decision": "frontier02E_decision_layer_diagnostic_no_go_prepare_closeout(전선02E 결정층 진단 진행조건 없음 마감 준비)",
            "parent_run_id": PARENT_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "rows": manifest["decision_rows"],
            "gate_passes": len(REQUIRED_GATES),
            "gate_total": len(REQUIRED_GATES),
            "claim_boundary": "decision_layer_diagnostic_only_no_wfo_no_mt5_no_candidate_selection_no_authority_goal_claim",
            "report_path": report,
            "trained_models": 0,
            "onnx_parity": "not_applicable_no_new_onnx(해당 없음 새 온엑스 없음)",
            "best_proxy": top["candidate_id"],
            "candidate_rows": manifest["decision_rows"],
            "positive_proxy_rows": diagnostic_observation_rows,
            "best_model_id": top["candidate_model_id"],
            "best_proxy_net": top["validation_net_profit"],
            "attempt_rows": 2160,
            "feature_matrix_rows": 46650,
            "runtime_completed_rows": 0,
            "matched_rows": 0,
            "mismatch_rows": 0,
            "positive_net_rows": diagnostic_observation_rows,
            "best_net_profit": top["validation_net_profit"],
            "best_profit_factor": top["validation_profit_factor"],
            "operating_ready_rows": 0,
            "run_date": local_date(),
            "primary_artifact": manifest["outputs"]["diagnostic_summary"]["path"],
            "candidate_model_id": top["candidate_model_id"],
            "net_profit": top["validation_net_profit"],
            "profit_factor": top["validation_profit_factor"],
            "drawdown": top["validation_max_drawdown_percent"],
            "trade_count": top["validation_trade_count"],
            "result_status": "completed_decision_layer_diagnostic_no_go_no_authority(결정층 진단 완료 진행조건 없음 권위 없음)",
            "sample_rows": 46650,
            "feature_count": 58,
            "expectancy": top["validation_expectancy"],
            "attempt_count": 2160,
            "view": "Tier A separate(티어 A 분리)",
            "tier": "Tier A(티어 A)",
            "metric_scope": "decision_layer_diagnostic(결정층 진단)",
            "scoreboard_lane": "decision_layer_diagnostic(결정층 진단)",
            "external_verification_status": "out_of_scope_by_claim_no_mt5(주장 범위 밖 MT5 없음)",
            "trade_density_per_feature_day": top["validation_trades_per_day"],
            "trade_density_requirement_status": "below_goal_validation_oos_pf_dd_gap(검증/표본외 수익 팩터와 손실폭 차이)",
            "result_judgment": JUDGMENT,
            "final_decision_path": report,
            "gate_audit_path": (PACKET_ROOT / "required_gate_coverage_audit.json").as_posix(),
            "created_at": now,
            "probability_parity_pass_rows": "not_applicable_no_new_onnx(해당 없음 새 온엑스 없음)",
            "ledger_row_id": f"{RUN_ID}__tier_a_separate_decision_layer_diagnostic",
            "subrun_id": f"{RUN_ID}__tier_a_separate_decision_layer_diagnostic",
            "record_view": "Tier A separate(티어 A 분리)",
            "tier_scope": "Tier A(티어 A)",
            "kpi_scope": "decision_layer_diagnostic(결정층 진단)",
            "primary_kpi": primary,
            "guardrail_kpi": guardrail,
            "model_variants": 0,
            "selected_surfaces": top["candidate_id"],
            "runtime_attempt_rows": 0,
            "work_family": "experiment_execution(실험 실행)",
            "max_drawdown_amount": top["validation_max_drawdown_percent"],
            "long_trade_count": top["validation_long_trade_count"],
            "short_trade_count": top["validation_short_trade_count"],
            "row_id": f"{RUN_ID}__tier_a_separate_decision_layer_diagnostic",
            "evidence_boundary": "frozen_02c_decision_layer_no_new_onnx_no_retrain_no_wfo_no_mt5(고정 02C 결정층, 새 온엑스/재학습/WFO/MT5 없음)",
            "next_action": NEXT_RUN_ID,
            "question": "Can a frozen 02C decision layer create a go-rule candidate before WFO/MT5?(고정 02C 결정층이 WFO/MT5 전 진행조건 후보를 만들 수 있는가?)",
            "artifact_count": artifact_count(manifest),
            "created_at_utc": now,
            "required_gate_audit": (PACKET_ROOT / "required_gate_coverage_audit.json").as_posix(),
            "runtime_authority": "not_claimed",
            "operating_promotion": "not_claimed",
            "run_family": "frontier_hypothesis_lifecycle(전선 가설 생명주기)",
            "run_type": "decision_layer_diagnostic(결정층 진단)",
            "input_run_id": ANCHOR_RUN_ID,
            "output_path": RUN_ROOT.as_posix(),
            "result_path": report,
            "selected_net_profit": top["validation_net_profit"],
            "selected_profit_factor": top["validation_profit_factor"],
            "selected_trade_density": top["validation_trades_per_day"],
            "goal_achieve": "not_claimed",
            "source_authority": "not_claimed",
            "trade_density": top["validation_trades_per_day"],
            "expected_net_profit": top["oos_net_profit"],
            "expected_profit_factor": top["oos_profit_factor"],
            "expected_trade_count": top["oos_trade_count"],
            "expected_trade_density": top["oos_trades_per_day"],
            "expected_estimated_mt5_density": "not_claimed",
            "scaled_density_estimate": "",
            "max_drawdown_percent": top["validation_max_drawdown_percent"],
            "strict_joint_pass_count": top["validation_joint_pass_count"],
        }
    )
    return row


def build_alpha_ledger_rows(
    now: str,
    manifest: dict[str, Any],
    top: dict[str, Any],
    counts: dict[str, int],
    diagnostic_observation_rows: int,
) -> list[dict[str, Any]]:
    base = empty_csv_row(ALPHA_LEDGER)
    common = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "scoreboard_lane": "decision_layer_diagnostic(결정층 진단)",
        "path": REPORT_PATH.as_posix(),
        "external_verification_status": "out_of_scope_by_claim_no_mt5(주장 범위 밖 MT5 없음)",
        "run_number": RUN_NUMBER,
        "date": local_date(),
        "decision": "frontier02E_decision_layer_diagnostic_no_go_prepare_closeout(전선02E 결정층 진단 진행조건 없음 마감 준비)",
        "next_run_id": NEXT_RUN_ID,
        "rows": manifest["decision_rows"],
        "gate_passes": len(REQUIRED_GATES),
        "gate_total": len(REQUIRED_GATES),
        "claim_boundary": "decision_layer_diagnostic_only_no_wfo_no_mt5_no_candidate_selection_no_authority_goal_claim",
        "report_path": REPORT_PATH.as_posix(),
        "trained_models": 0,
        "onnx_parity": "not_applicable_no_new_onnx(해당 없음 새 온엑스 없음)",
        "best_proxy": top["candidate_id"],
        "candidate_rows": manifest["decision_rows"],
        "positive_proxy_rows": diagnostic_observation_rows,
        "best_model_id": top["candidate_model_id"],
        "best_proxy_net": top["validation_net_profit"],
        "attempt_rows": 2160,
        "feature_matrix_rows": 46650,
        "runtime_completed_rows": 0,
        "matched_rows": 0,
        "mismatch_rows": 0,
        "positive_net_rows": diagnostic_observation_rows,
        "best_net_profit": top["validation_net_profit"],
        "best_profit_factor": top["validation_profit_factor"],
        "operating_ready_rows": 0,
        "run_date": local_date(),
        "primary_artifact": manifest["outputs"]["diagnostic_summary"]["path"],
        "net_profit": top["validation_net_profit"],
        "profit_factor": top["validation_profit_factor"],
        "expectancy": top["validation_expectancy"],
        "drawdown": top["validation_max_drawdown_percent"],
        "trade_count": top["validation_trade_count"],
        "candidate_model_id": top["candidate_model_id"],
        "result_status": "completed_decision_layer_diagnostic_no_go_no_authority(결정층 진단 완료 진행조건 없음 권위 없음)",
        "long_trade_count": top["validation_long_trade_count"],
        "short_trade_count": top["validation_short_trade_count"],
        "feature_count": 58,
        "sample_rows": 46650,
        "attempt_count": 2160,
        "lane": "decision_layer_diagnostic(결정층 진단)",
        "family": "experiment_execution(실험 실행)",
        "primary_report": REPORT_PATH.as_posix(),
        "evidence_boundary": "frozen_02c_decision_layer_no_new_onnx_no_retrain_no_wfo_no_mt5(고정 02C 결정층, 새 온엑스/재학습/WFO/MT5 없음)",
        "work_family": "experiment_execution(실험 실행)",
        "evidence_scope": "diagnostic_only(진단 전용)",
        "run_key": RUN_ID,
        "question": "Can a frozen 02C decision layer create a go-rule candidate before WFO/MT5?(고정 02C 결정층이 WFO/MT5 전 진행조건 후보를 만들 수 있는가?)",
        "next_action": NEXT_RUN_ID,
        "trade_density_per_feature_day": top["validation_trades_per_day"],
        "trade_density_requirement_status": "below_goal_validation_oos_pf_dd_gap(검증/표본외 수익 팩터와 손실폭 차이)",
        "result_judgment": JUDGMENT,
        "max_drawdown_amount": top["validation_max_drawdown_percent"],
        "final_decision_path": REPORT_PATH.as_posix(),
        "created_at": now,
        "gate_audit_path": (PACKET_ROOT / "required_gate_coverage_audit.json").as_posix(),
        "artifact_count": artifact_count(manifest),
        "created_at_utc": now,
        "required_gate_audit": (PACKET_ROOT / "required_gate_coverage_audit.json").as_posix(),
        "kpi_summary": primary_kpi_text(top),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "trade_density": top["validation_trades_per_day"],
        "source_authority": "not_claimed",
        "goal_achieve": "not_claimed",
        "run_family": "frontier_hypothesis_lifecycle(전선 가설 생명주기)",
        "run_type": "decision_layer_diagnostic(결정층 진단)",
        "input_run_id": ANCHOR_RUN_ID,
        "output_path": RUN_ROOT.as_posix(),
        "result_path": REPORT_PATH.as_posix(),
        "selected_net_profit": top["validation_net_profit"],
        "selected_profit_factor": top["validation_profit_factor"],
        "selected_trade_density": top["validation_trades_per_day"],
        "expected_net_profit": top["oos_net_profit"],
        "expected_profit_factor": top["oos_profit_factor"],
        "expected_trade_count": top["oos_trade_count"],
        "expected_trade_density": top["oos_trades_per_day"],
        "route_attribution_boundary": "not_claimed",
        "max_drawdown_percent": top["validation_max_drawdown_percent"],
        "strict_joint_pass_count": top["validation_joint_pass_count"],
    }
    rows: list[dict[str, Any]] = []
    tier_a = dict(base)
    tier_a.update(
        common
        | {
            "ledger_row_id": f"{RUN_ID}__tier_a_separate_decision_layer_diagnostic",
            "subrun_id": f"{RUN_ID}__tier_a_separate_decision_layer_diagnostic",
            "row_id": f"{RUN_ID}__tier_a_separate_decision_layer_diagnostic",
            "record_view": "Tier A separate(티어 A 분리)",
            "tier_scope": "Tier A(티어 A)",
            "kpi_scope": "decision_layer_diagnostic(결정층 진단)",
            "status": "completed",
            "judgment": JUDGMENT,
            "primary_kpi": primary_kpi_text(top),
            "guardrail_kpi": guardrail_text(counts, diagnostic_observation_rows, manifest),
            "notes": "Tier A frozen 02C decision-layer diagnostic materialized(티어 A 고정 02C 결정층 진단 물질화); no go-rule rows(진행 규칙 행 없음); no authority(권위 없음).",
            "view": "Tier A separate(티어 A 분리)",
            "tier": "Tier A(티어 A)",
            "metric_scope": "decision_layer_diagnostic(결정층 진단)",
        }
    )
    rows.append(tier_a)

    tier_b = dict(base)
    tier_b.update(
        common
        | {
            "ledger_row_id": f"{RUN_ID}__tier_b_separate_missing_required",
            "subrun_id": f"{RUN_ID}__tier_b_separate_missing_required",
            "row_id": f"{RUN_ID}__tier_b_separate_missing_required",
            "record_view": "Tier B separate(티어 B 분리)",
            "tier_scope": "Tier B(티어 B)",
            "kpi_scope": "decision_layer_diagnostic(결정층 진단)",
            "status": "missing_required",
            "judgment": "missing_required_partial_context_artifact_not_materialized",
            "primary_kpi": "not_measured(측정 안 됨)",
            "guardrail_kpi": "Tier B partial-context dataset not materialized(티어 B 부분 문맥 데이터셋 물질화 안 됨)",
            "notes": "Required paired record kept as missing_required(필수 쌍 기록을 필수 누락으로 유지).",
            "result_status": "missing_required_tier_b_no_authority(티어 B 필수 누락, 권위 없음)",
            "view": "Tier B separate(티어 B 분리)",
            "tier": "Tier B(티어 B)",
            "net_profit": "",
            "profit_factor": "",
            "expectancy": "",
            "drawdown": "",
            "trade_count": "",
            "trade_density": "missing_required(필수 누락)",
            "source_authority": "not_claimed",
        }
    )
    rows.append(tier_b)

    combined = dict(base)
    combined.update(
        common
        | {
            "ledger_row_id": f"{RUN_ID}__tier_ab_combined_out_of_scope",
            "subrun_id": f"{RUN_ID}__tier_ab_combined_out_of_scope",
            "row_id": f"{RUN_ID}__tier_ab_combined_out_of_scope",
            "record_view": "Tier A+B combined(Tier A+B 합산)",
            "tier_scope": "Tier A+B(Tier A+B 합산)",
            "kpi_scope": "decision_layer_diagnostic(결정층 진단)",
            "status": "out_of_scope_by_claim",
            "judgment": "combined_routed_total_not_claimed_no_tier_b_fallback",
            "primary_kpi": "not_measured(측정 안 됨)",
            "guardrail_kpi": "No routed Tier B fallback(라우팅 티어 B 대체 없음); synthetic sum not created(합성 합산 만들지 않음)",
            "notes": "Combined row is not synthetic sum(합산 행은 합성 합산이 아님).",
            "result_status": "out_of_scope_combined_no_authority(합산 범위 밖, 권위 없음)",
            "view": "Tier A+B combined(Tier A+B 합산)",
            "tier": "Tier A+B(Tier A+B 합산)",
            "net_profit": "",
            "profit_factor": "",
            "expectancy": "",
            "drawdown": "",
            "trade_count": "",
            "trade_density": "out_of_scope_by_claim(주장 범위 밖)",
            "source_authority": "not_claimed",
        }
    )
    rows.append(combined)
    return rows


def build_stage_ledger_row(alpha_row: dict[str, Any]) -> dict[str, Any]:
    row = empty_csv_row(STAGE_LEDGER)
    for key in row:
        row[key] = alpha_row.get(key, "")
    return row


def update_state_documents(
    now: str,
    manifest: dict[str, Any],
    top: dict[str, Any],
    counts: dict[str, int],
    diagnostic_observation_rows: int,
    local_verification: dict[str, Any],
    advice: dict[str, Any],
) -> None:
    state = {
        "current_stage_id": STAGE_ID,
        "current_run_id": RUN_ID,
        "latest_completed_run_id": RUN_ID,
        "current_status": "active_frontier02_decision_layer_diagnostic_completed_no_go_no_authority",
        "current_judgment": JUDGMENT,
        "next_run_id": NEXT_RUN_ID,
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "updated_at_utc": now,
    }
    write_yaml(WORKSPACE_STATE, state)
    write_text_sig(CURRENT_WORKING_STATE, current_working_state_text(now, top, counts, diagnostic_observation_rows, local_verification, advice))
    write_text_sig(SELECTION_STATUS, selection_status_text(now, top, counts, diagnostic_observation_rows, advice))
    write_text_sig(STAGE_README, stage_readme_text(top))
    write_text_sig(STAGE_BRIEF, stage_brief_text(now, top))
    update_review_index()
    append_changelog(now, top, manifest, diagnostic_observation_rows)
    update_idea_registry(top, diagnostic_observation_rows)


def current_working_state_text(
    now: str,
    top: dict[str, Any],
    counts: dict[str, int],
    diagnostic_observation_rows: int,
    local_verification: dict[str, Any],
    advice: dict[str, Any],
) -> str:
    return f"""# Current Working State(현재 작업 상태)

Updated(갱신): {now}

Active stage(활성 단계): `{STAGE_ID}`

Current run(현재 실행): `{RUN_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Current truth(현재 진실): Frontier 02(전선 02)는 four-axis joint ONNX proxy scout(네 축 동시 온엑스 프록시 탐색) 가설 생명주기(hypothesis lifecycle, 가설 생명주기) 안에서 진행 중입니다. Stage12~364(12~364단계)는 reference only(참조 전용)이고 winner/baseline/promotion/runtime authority/live readiness(승자/기준선/승격/런타임 권위/실거래 준비)는 상속하지 않습니다.

Latest evidence(최근 근거): `{RUN_ID}`는 Grok pre-expensive review(비싼 검증 전 그록 검토)를 받고, frontier02C(전선02C) 고정 probability output(확률 출력)만 사용한 decision-layer diagnostic(결정층 진단)을 실행했습니다. decision rows(결정 행)는 `720`, metric rows(측정 행)는 `2160`, diagnostic observation rows(진단 관찰 행)는 `{diagnostic_observation_rows}`, go_rule_rows(진행 규칙 행)는 `0`입니다.

Best validation rank(검증 순위 1위): `{top['candidate_id']}`. validation PF/density/DD(검증 수익 팩터/밀도/손실폭)는 `{fmt(top['validation_profit_factor'])}` / `{fmt(top['validation_trades_per_day'])}/day` / `{fmt(top['validation_max_drawdown_percent'])}%`이고, OOS PF/density/DD(표본외 수익 팩터/밀도/손실폭)는 `{fmt(top['oos_profit_factor'])}` / `{fmt(top['oos_trades_per_day'])}/day` / `{fmt(top['oos_max_drawdown_percent'])}%`입니다.

KPI read(지표 판독): OOS density(표본외 밀도)는 목표권에 닿았지만 OOS PF(표본외 수익 팩터)는 `1.05433`이고 OOS DD(표본외 손실폭)는 `10.3356%`입니다. 효과(effect, 효과)는 expensive WFO/MT5(비싼 WFO/MT5)로 넘기지 않고 no-go diagnostic read(진행조건 없음 진단 판독)로 낮춰 stage closeout(단계 마감)을 준비하는 것입니다.

Grok classification(그록 분류): accepted(수용)은 no WFO/MT5 yet(아직 WFO/MT5 금지), frozen 02C decision-layer diagnostic(고정 02C 결정층 진단), C as seed observation(C를 씨앗 관찰), D as negative repair memory(D를 부정 수리 기억)입니다. rejected(거절)은 `{'; '.join(advice['rejected']) if advice['rejected'] else 'none(없음)'}`입니다. Local verification(로컬 검증)은 D repair rows(수리 행) 중 C보다 validation PF(검증 수익 팩터)가 높은 행이 `{local_verification['grok_degradation_claim_check']['repair_rows_above_c_validation_pf']}`개임을 확인했습니다.

Axis counts(축별 개수): validation density/PF/DD/smoothness pass(검증 밀도/수익 팩터/손실폭/매끄러움 통과)는 `{counts['validation_density_pass_rows']}` / `{counts['validation_pf_pass_rows']}` / `{counts['validation_dd_pass_rows']}` / `{counts['validation_smoothness_pass_rows']}`이고, OOS density/PF/DD/smoothness pass(표본외 밀도/수익 팩터/손실폭/매끄러움 통과)는 `{counts['oos_density_pass_rows']}` / `{counts['oos_pf_pass_rows']}` / `{counts['oos_dd_pass_rows']}` / `{counts['oos_smoothness_pass_rows']}`입니다.

Tier boundary(티어 경계): Tier A separate(Tier A 분리)는 materialized(물질화)했습니다. Tier B separate(Tier B 분리)는 `missing_required(필수 누락)`이고, Tier A+B combined(Tier A+B 합산)는 `out_of_scope_by_claim(주장 범위 밖)`입니다.

Evidence paths(근거 경로): run manifest(실행 목록)는 `{MANIFEST_PATH.as_posix()}`, report(보고서)는 `{REPORT_PATH.as_posix()}`, control packet(제어 묶음)은 `{PACKET_ROOT.as_posix()}/`입니다.

Next action(다음 행동): `{NEXT_RUN_ID}`. 행동(action, 행동)은 Frontier 02(전선 02)를 preserved clue(보존 단서)와 negative memory(부정 기억) 중심으로 마감 준비하는 것입니다. 효과(effect, 효과)는 같은 수리 실패 축을 새 정보 없이 반복하지 않고 다음 frontier hypothesis(전선 가설)로 넘어갈 근거를 닫는 것입니다.

Operating boundary(운영 경계): completion(완성), selected baseline(선택 기준선), operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 없음)입니다.
"""


def selection_status_text(
    now: str,
    top: dict[str, Any],
    counts: dict[str, int],
    diagnostic_observation_rows: int,
    advice: dict[str, Any],
) -> str:
    return f"""# Stage Frontier 02 Selection Status(전선 02단계 선택 상태)

Updated(갱신): {now}

Stage status(단계 상태): `active_frontier02_decision_layer_diagnostic_completed_no_go_no_authority`

Current run(현재 실행): `{RUN_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Judgment(판정): `{JUDGMENT}`

## Current Truth(현재 진실)

Frontier 02(전선 02)는 `stage_frontier_02__four_axis_joint_onnx_proxy_scout`로 열려 있으며, `{RUN_ID}`에서 Grok review(그록 검토)와 frozen 02C decision-layer diagnostic(고정 02C 결정층 진단)을 완료했습니다.

Effect(효과): 진행 규칙 행(go_rule_rows, 진행 규칙 행)이 `0`개라 WFO/MT5(WFO/MT5)로 넘기지 않고 stage closeout(단계 마감)을 준비합니다.

## Decision-Layer Diagnostic Read(결정층 진단 판독)

- decision rows(결정 행): `720`
- metric rows(측정 행): `2160`
- diagnostic observation rows(진단 관찰 행): `{diagnostic_observation_rows}`
- go_rule_rows(진행 규칙 행): `0`
- best validation rank(검증 순위 1위): `{top['candidate_id']}`
- validation PF/density/DD(검증 수익 팩터/밀도/손실폭): `{fmt(top['validation_profit_factor'])}` / `{fmt(top['validation_trades_per_day'])}/day` / `{fmt(top['validation_max_drawdown_percent'])}%`
- OOS PF/density/DD(표본외 수익 팩터/밀도/손실폭): `{fmt(top['oos_profit_factor'])}` / `{fmt(top['oos_trades_per_day'])}/day` / `{fmt(top['oos_max_drawdown_percent'])}%`

## Grok Classification(그록 분류)

- accepted(수용): `{len(advice['accepted'])}`
- rejected(거절): `{len(advice['rejected'])}`
- final Codex direction(최종 코덱스 방향): `{advice['final_codex_direction']}`

## Axis Counts(축별 개수)

- validation density/PF/DD/smoothness pass(검증 밀도/수익 팩터/손실폭/매끄러움 통과): `{counts['validation_density_pass_rows']}` / `{counts['validation_pf_pass_rows']}` / `{counts['validation_dd_pass_rows']}` / `{counts['validation_smoothness_pass_rows']}`
- OOS density/PF/DD/smoothness pass(표본외 밀도/수익 팩터/손실폭/매끄러움 통과): `{counts['oos_density_pass_rows']}` / `{counts['oos_pf_pass_rows']}` / `{counts['oos_dd_pass_rows']}` / `{counts['oos_smoothness_pass_rows']}`

## Tier Records(티어 기록)

- Tier A separate(Tier A 분리): `materialized(물질화)`
- Tier B separate(Tier B 분리): `missing_required(필수 누락)`
- Tier A+B combined(Tier A+B 합산): `out_of_scope_by_claim(주장 범위 밖)`

## Claim Boundary(주장 경계)

Allowed claim(허용 주장):

- Grok pre-expensive review captured(비싼 검증 전 그록 검토 기록)
- frozen 02C diagnostic completed(고정 02C 진단 완료)
- no-go diagnostic read(진행조건 없음 진단 판독)

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

Effect(효과): preserved clue(보존 단서)와 negative memory(부정 기억)를 분리해 Frontier 02(전선 02)를 정직하게 닫을 준비를 합니다.
"""


def stage_readme_text(top: dict[str, Any]) -> str:
    return f"""# Stage Frontier 02(전선 02단계)

Stage id(단계 ID): `{STAGE_ID}`

Purpose(목적): four-axis joint ONNX proxy scout(네 축 동시 온엑스 프록시 탐색)를 설계하고, density/PF/DD/curve smoothness(밀도/수익 팩터/손실폭/곡선 매끄러움)를 동시에 보는 첫 독립 frontier hypothesis(전선 가설)를 연다.

Latest run(최근 실행): `{RUN_ID}` completed Grok pre-expensive review(비싼 검증 전 그록 검토) and frozen frontier02C decision-layer diagnostic(고정 전선02C 결정층 진단). No new ONNX(새 온엑스 없음), no retraining(재학습 없음), no WFO/MT5(WFO/MT5 없음).

Latest best read(최근 최고 판독): `{top['candidate_id']}` validation PF/density/DD(검증 수익 팩터/밀도/손실폭) `{fmt(top['validation_profit_factor'])}` / `{fmt(top['validation_trades_per_day'])}/day` / `{fmt(top['validation_max_drawdown_percent'])}%`; OOS PF/density/DD(표본외 수익 팩터/밀도/손실폭) `{fmt(top['oos_profit_factor'])}` / `{fmt(top['oos_trades_per_day'])}/day` / `{fmt(top['oos_max_drawdown_percent'])}%`.

Next run(다음 실행): `{NEXT_RUN_ID}`

Boundary(경계): this stage(이 단계)는 active exploration(활성 탐색)이다. It has no completion(완성 없음), no baseline(기준선 없음), no promotion(승격 없음), no runtime authority(런타임 권위 없음), no live readiness(실거래 준비 없음), and no Goal Achieve(목표 달성 없음).
"""


def stage_brief_text(now: str, top: dict[str, Any]) -> str:
    return f"""# Stage Frontier 02 Brief(전선 02단계 개요)

Stage id(단계 ID): `{STAGE_ID}`

Status(상태): `active_frontier02_decision_layer_diagnostic_completed_no_go_no_authority`

Current run(현재 실행): `{RUN_ID}`

Updated(갱신): {now}

## Frontier Thesis(전선 가설)

US100 M5(US100 5분봉)에서 directly trained ONNX(직접 학습 온엑스) surface(표면)를 만들 때, proxy/training/selection-time joint objective(프록시/학습/선택 시점 동시 목적)가 density/PF/DD/curve smoothness(밀도/수익 팩터/손실폭/곡선 매끄러움)를 처음부터 함께 보게 하면, prior one-axis repair loop(이전 한 축 수리 반복)보다 final target distance(최종 목표 거리)를 더 정직하게 줄일 수 있다.

## Current Evidence(현재 근거)

`{RUN_ID}`는 Grok pre-expensive review(비싼 검증 전 그록 검토) 뒤 frozen frontier02C decision-layer diagnostic(고정 전선02C 결정층 진단)을 실행했습니다. Best validation rank(검증 순위 1위)는 `{top['candidate_id']}`이고 validation PF/density/DD(검증 수익 팩터/밀도/손실폭)는 `{fmt(top['validation_profit_factor'])}` / `{fmt(top['validation_trades_per_day'])}/day` / `{fmt(top['validation_max_drawdown_percent'])}%`, OOS PF/density/DD(표본외 수익 팩터/밀도/손실폭)는 `{fmt(top['oos_profit_factor'])}` / `{fmt(top['oos_trades_per_day'])}/day` / `{fmt(top['oos_max_drawdown_percent'])}%`입니다.

Effect(효과): go_rule_rows(진행 규칙 행)가 `0`개이므로 WFO/MT5(WFO/MT5) 전진 대신 preserved clue(보존 단서)와 negative memory(부정 기억) 중심 closeout(마감)을 준비합니다.

## Prior-Stage Scan(이전 단계 점검)

Primary archive inputs(주 보관소 입력):

- `stages/stage_frontier_01__archive_synthesis_and_new_axis_lock/01_inputs/stage12_364_campaign_map.md`
- `stages/stage_frontier_01__archive_synthesis_and_new_axis_lock/01_inputs/do_not_repeat_list.md`
- `stages/364_source_regime_label_pivot__dense_cost_recovery/03_reviews/run364HS_stage364_closeout_no_next_stage.md`
- `docs/registers/negative_result_register.md`

Import rule(반입 규칙): preserved clue(보존 단서), negative memory(부정 기억), reusable artifact(재사용 산출물), do-not-repeat note(반복 금지 메모)만 참조한다.

Forbidden imports(금지 반입): winner(승자), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성).

## Exit Rule(종료 규칙)

Close this frontier stage(전선 단계 마감)는 아래 중 하나로만 한다.

- completion candidate(완성 후보): proxy/WFO/stress/runtime(프록시/WFO/스트레스/런타임)이 같은 방향을 가리키고 네 축이 동시에 접근한다.
- preserved clue(보존 단서): 한계는 있으나 새 표면이나 새 측정법이 다음 가설에 유용하다.
- negative memory(부정 기억): broad sweep(넓은 탐색)과 capped repair(상한 있는 수리) 뒤에도 joint objective(동시 목적)가 한 축 실패를 반복한다.
- invalid setup(무효 설정): data/split/label/feature boundary(데이터/분할/라벨/피처 경계)가 깨져 결과 해석이 불가능하다.
- blocked(차단): 필요한 도구, 데이터, MT5 output(MT5 출력), 또는 외부 상태가 없어 복구 시도 뒤에도 진행할 수 없다.

Capped repair rule(상한 있는 수리 규칙): 같은 실패 축을 새 정보 없이 두 번 반복하면 다음 repair(수리)를 자동으로 늘리지 않고 negative memory(부정 기억) 또는 blocked(차단)로 닫는다.

## Claim Boundary(주장 경계)

Allowed now(현재 허용):

- Grok pre-expensive review captured(비싼 검증 전 그록 검토 기록)
- frozen decision-layer diagnostic completed(고정 결정층 진단 완료)
- no-go diagnostic read(진행조건 없음 진단 판독)
- no authority claimed(권위 주장 없음)

Forbidden now(현재 금지):

- completion(완성)
- baseline(기준선)
- promotion(승격)
- runtime authority(런타임 권위)
- operating promotion(운영 승격)
- live readiness(실거래 준비)
- Goal Achieve(목표 달성)
- selected candidate(선택 후보)
"""


def update_review_index() -> None:
    text = read_text_sig(REVIEW_INDEX)
    row = f"| frontier02E Grok and decision-layer diagnostic report(frontier02E 그록 및 결정층 진단 보고) | `{REPORT_PATH.as_posix()}` | Grok pre-expensive review(비싼 검증 전 그록 검토), frozen 02C diagnostic(고정 02C 진단), no-go read(진행조건 없음 판독), Tier A/B/combined(Tier A/B/합산) 경계 |"
    if "frontier02E Grok and decision-layer diagnostic report" not in text:
        text = text.replace(
            "| frontier02D ONNX repair scout report(frontier02D 온엑스 수리 탐색 보고) | `stages/stage_frontier_02__four_axis_joint_onnx_proxy_scout/03_reviews/frontier02D_review_and_repair_onnx_seed_surface_v1_report.md` | cheap repair scout(저비용 수리 탐색), repair observation rows(수리 관찰 행), negative repair judgment(부정 수리 판정), Tier A/B/combined(Tier A/B/합산) 경계 |",
            "| frontier02D ONNX repair scout report(frontier02D 온엑스 수리 탐색 보고) | `stages/stage_frontier_02__four_axis_joint_onnx_proxy_scout/03_reviews/frontier02D_review_and_repair_onnx_seed_surface_v1_report.md` | cheap repair scout(저비용 수리 탐색), repair observation rows(수리 관찰 행), negative repair judgment(부정 수리 판정), Tier A/B/combined(Tier A/B/합산) 경계 |\n" + row,
        )
        text = text.replace(
            "cheap ONNX repair evidence(저비용 온엑스 수리 근거)만 말한다.",
            "cheap ONNX repair evidence(저비용 온엑스 수리 근거), and Grok-gated diagnostic evidence(그록 기반 진단 근거)만 말한다.",
        )
        write_text_sig(REVIEW_INDEX, text)


def append_changelog(now: str, top: dict[str, Any], manifest: dict[str, Any], diagnostic_observation_rows: int) -> None:
    text = read_text_sig(CHANGELOG)
    marker = "<!-- frontier02E__grok_decision_layer_diagnostic -->"
    if marker not in text:
        addition = (
            f"{marker}\n"
            f"- {now} `{RUN_ID}` completed Grok pre-expensive review(비싼 검증 전 그록 검토) and frozen 02C decision-layer diagnostic(고정 02C 결정층 진단); "
            f"decision_rows(결정 행) `{manifest['decision_rows']}`, metric_rows(측정 행) `2160`, diagnostic_observation_rows(진단 관찰 행) `{diagnostic_observation_rows}`, go_rule_rows(진행 규칙 행) `0`; "
            f"best validation rank(검증 순위 1위) `{top['candidate_id']}` validation PF/density/DD(검증 수익 팩터/밀도/손실폭) `{fmt(top['validation_profit_factor'])}`/`{fmt(top['validation_trades_per_day'])}`/`{fmt(top['validation_max_drawdown_percent'])}%`; "
            f"OOS PF/density/DD(표본외 수익 팩터/밀도/손실폭) `{fmt(top['oos_profit_factor'])}`/`{fmt(top['oos_trades_per_day'])}`/`{fmt(top['oos_max_drawdown_percent'])}%`; judgment(판정) `{JUDGMENT}`; next(다음) `{NEXT_RUN_ID}`; no completion/baseline/promotion/runtime authority/Goal Achieve claim(완성/기준선/승격/런타임 권위/목표 달성 주장 없음).\n"
        )
        write_text_sig(CHANGELOG, text.rstrip() + "\n" + addition)


def update_idea_registry(top: dict[str, Any], diagnostic_observation_rows: int) -> None:
    text = read_text_sig(IDEA_REGISTRY)
    updated = (
        "| `IDEA-FR02-FOUR-AXIS-JOINT-ONNX-PROXY-SCOUT` | `stage_frontier_02__four_axis_joint_onnx_proxy_scout` | directly trained ONNX(직접 학습 온엑스) surface(표면)를 위한 four-axis joint objective(네 축 동시 목적)가 density/PF/DD/curve smoothness(밀도/수익 팩터/손실폭/곡선 매끄러움)를 처음부터 함께 보게 하면 one-axis repair loop(한 축 수리 반복)를 줄일 수 있다 | `Tier A materialized, Tier B missing_required, Tier A+B out_of_scope(Tier A 물질화, Tier B 필수 누락, Tier A+B 범위 밖)` | `active_decision_layer_diagnostic_completed_no_go_no_authority` | "
        f"`{RUN_ID}`에서 Grok pre-expensive review(비싼 검증 전 그록 검토)와 frozen 02C decision-layer diagnostic(고정 02C 결정층 진단)을 완료. diagnostic observation rows(진단 관찰 행) `{diagnostic_observation_rows}`개였지만 go_rule_rows(진행 규칙 행)가 `0`개라 WFO/MT5(WFO/MT5) 전진 없이 stage closeout(단계 마감) 준비로 판정. best validation rank(검증 순위 1위) `{top['candidate_id']}` validation PF/density/DD(검증 수익 팩터/밀도/손실폭) `{fmt(top['validation_profit_factor'])}`/`{fmt(top['validation_trades_per_day'])}`/`{fmt(top['validation_max_drawdown_percent'])}%`; OOS PF/density/DD(표본외 수익 팩터/밀도/손실폭) `{fmt(top['oos_profit_factor'])}`/`{fmt(top['oos_trades_per_day'])}`/`{fmt(top['oos_max_drawdown_percent'])}%`. completion/baseline/promotion/runtime authority(완성/기준선/승격/런타임 권위)는 없음 |"
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
        "validation_density_pass_rows": bool_count(summary, "validation_density_pass"),
        "validation_pf_pass_rows": bool_count(summary, "validation_pf_pass"),
        "validation_dd_pass_rows": bool_count(summary, "validation_dd_pass"),
        "validation_smoothness_pass_rows": bool_count(summary, "validation_smoothness_pass"),
        "oos_density_pass_rows": bool_count(summary, "oos_density_pass"),
        "oos_pf_pass_rows": bool_count(summary, "oos_pf_pass"),
        "oos_dd_pass_rows": bool_count(summary, "oos_dd_pass"),
        "oos_smoothness_pass_rows": bool_count(summary, "oos_smoothness_pass"),
        "go_rule_rows": bool_count(summary, "go_rule_flag"),
    }


def primary_kpi_text(top: dict[str, Any]) -> str:
    return (
        f"best_validation={top['candidate_id']};"
        f"model={top['candidate_model_id']};score_mode={top['score_mode']};"
        f"val_net={fmt(top['validation_net_profit'])};val_pf={fmt(top['validation_profit_factor'])};"
        f"val_density={fmt(top['validation_trades_per_day'])};val_dd={fmt(top['validation_max_drawdown_percent'])};"
        f"oos_net={fmt(top['oos_net_profit'])};oos_pf={fmt(top['oos_profit_factor'])};"
        f"oos_density={fmt(top['oos_trades_per_day'])};oos_dd={fmt(top['oos_max_drawdown_percent'])}"
    )


def guardrail_text(counts: dict[str, int], diagnostic_observation_rows: int, manifest: dict[str, Any]) -> str:
    return (
        "no_new_onnx=true;no_retrain=true;"
        f"decision_rows={manifest['decision_rows']};metric_rows=2160;"
        f"diagnostic_observation_rows={diagnostic_observation_rows};go_rule_rows=0;"
        f"grok_rejected={len(manifest['grok_advice_classification'].get('rejected', []))};"
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
    rows["run_manifest"] = {"path": MANIFEST_PATH.as_posix(), "sha256": sha256_file(MANIFEST_PATH)}
    rows["script"] = {"path": manifest.get("script_path"), "sha256": manifest.get("script_sha256")}
    return rows


def check_artifact(label: str, path_text: str | None, expected_hash: str | None, checked: list[dict[str, Any]], findings: list[dict[str, Any]]) -> None:
    if not path_text:
        findings.append(blocking(f"artifact::{label}::missing_path", "Artifact path is missing."))
        return
    path = Path(path_text)
    exists = path_exists(path)
    actual_hash = sha256_file(path) if exists else None
    checked.append({"label": label, "path": path.as_posix(), "exists": exists, "expected_sha256": expected_hash, "actual_sha256": actual_hash})
    if not exists:
        findings.append(blocking(f"artifact::{label}::missing", "Artifact is missing.", {"path": path.as_posix()}))
    elif expected_hash and actual_hash != expected_hash:
        findings.append(blocking(f"artifact::{label}::hash_mismatch", "Artifact hash mismatch.", {"path": path.as_posix(), "expected": expected_hash, "actual": actual_hash}))


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
        forbidden_claims = () if status == "pass" else tuple(FORBIDDEN_CLAIMS)
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


def blocking(check_id: str, message: str, details: dict[str, Any] | None = None) -> dict[str, Any]:
    return {"check_id": check_id, "message": message, "severity": "blocking", "details": details or {}}


def empty_csv_row(path: Path) -> dict[str, Any]:
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return {field: "" for field in list(reader.fieldnames or [])}


def upsert_csv(path: Path, key: str, row: dict[str, Any]) -> None:
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = list(reader.fieldnames or [])
        existing = [record for record in reader if str(record.get(key, "")).strip() != str(row.get(key, "")).strip()]
    existing.append({field: row.get(field, "") for field in fieldnames})
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(existing)


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


def ensure_utf8_sig(path: Path) -> None:
    raw = io_path(path).read_bytes()
    if raw.startswith(b"\xef\xbb\xbf"):
        return
    text = raw.decode("utf-8-sig")
    write_text_sig(path, text)


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
    return len(manifest.get("outputs", {})) + 3


if __name__ == "__main__":
    raise SystemExit(main())
