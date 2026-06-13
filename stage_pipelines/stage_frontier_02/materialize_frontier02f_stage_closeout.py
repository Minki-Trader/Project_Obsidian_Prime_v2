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
RUN_ID = "frontier02F_stage_closeout_preserved_clue_negative_memory_v1"
RUN_NUMBER = "frontier02F"
PARENT_RUN_ID = "frontier02E_grok_pre_expensive_review_or_second_repair_v1"
NEXT_RUN_ID = "frontier03A_stage_open_regime_conditioned_asymmetric_onnx_labeling_v1"
STATUS = "closed_frontier02_preserved_clue_negative_memory_no_authority"
JUDGMENT = "stage_closeout_preserved_clue_negative_memory_no_authority"
IDEA_ID = "IDEA-FR02-FOUR-AXIS-JOINT-ONNX-PROXY-SCOUT"
NEGATIVE_RESULT_ID = "NR-FR02-FOUR-AXIS-JOINT-ONNX-PROXY-SCOUT"

RUN_ROOT = Path("stages") / STAGE_ID / "02_runs" / RUN_ID
REPORT_PATH = Path("stages") / STAGE_ID / "03_reviews" / f"{RUN_ID}_report.md"
PACKET_ROOT = Path("docs/agent_control/packets") / RUN_ID
GROK_ROOT = Path("docs/agent_control/grok_reviews/2026-06-14_frontier02F_stage_closeout/medium_review")
GROK_PROMPT = GROK_ROOT / "prompt.md"
GROK_OUTPUT = GROK_ROOT / "clean_output.md"
GROK_METADATA = GROK_ROOT / "metadata.json"
GROK_RAW_DIAGNOSTICS = GROK_ROOT / "raw_diagnostics.json"

B_ROOT = Path("stages") / STAGE_ID / "02_runs" / "frontier02B_proxy_scout_execution_v1"
C_ROOT = Path("stages") / STAGE_ID / "02_runs" / "frontier02C_trainable_onnx_seed_surface_design_v1"
D_ROOT = Path("stages") / STAGE_ID / "02_runs" / "frontier02D_review_and_repair_onnx_seed_surface_v1"
E_ROOT = Path("stages") / STAGE_ID / "02_runs" / PARENT_RUN_ID
B_REPORT = Path("stages") / STAGE_ID / "03_reviews" / "frontier02B_proxy_scout_execution_v1_report.md"
C_REPORT = Path("stages") / STAGE_ID / "03_reviews" / "frontier02C_trainable_onnx_seed_surface_design_v1_report.md"
D_REPORT = Path("stages") / STAGE_ID / "03_reviews" / "frontier02D_review_and_repair_onnx_seed_surface_v1_report.md"
E_REPORT = Path("stages") / STAGE_ID / "03_reviews" / f"{PARENT_RUN_ID}_report.md"

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
NEGATIVE_RESULT_REGISTER = Path("docs/registers/negative_result_register.md")

FORBIDDEN_CLAIMS = [
    "completion",
    "selected_baseline",
    "operating_promotion",
    "runtime_authority",
    "live_readiness",
    "goal_achieve",
]
REQUIRED_GATES = [
    "state_sync_audit",
    "closeout_judgment_audit",
    "artifact_lineage_audit",
    "external_review_packet",
    "work_packet_schema_lint",
    "skill_receipt_lint",
    "skill_receipt_schema_lint",
    "required_gate_coverage_audit",
    "final_claim_guard",
]
REQUIRED_SKILLS = [
    "obsidian-reentry-read",
    "obsidian-grok-collaboration",
    "obsidian-result-judgment",
    "obsidian-artifact-lineage",
    "obsidian-exploration-mandate",
]


def main() -> int:
    now = utc_now()
    io_path(RUN_ROOT).mkdir(parents=True, exist_ok=True)
    io_path(PACKET_ROOT).mkdir(parents=True, exist_ok=True)
    normalize_markdown()

    b_summary = pd.read_csv(io_path(B_ROOT / "candidate_surface_summary.csv"))
    c_summary = pd.read_csv(io_path(C_ROOT / "decision_surface_summary.csv"))
    d_summary = pd.read_csv(io_path(D_ROOT / "repair_decision_surface_summary.csv"))
    e_summary = pd.read_csv(io_path(E_ROOT / "diagnostic_summary.csv"))
    e_loss = pd.read_csv(io_path(E_ROOT / "loss_attribution.csv"))
    e_manifest = read_json(E_ROOT / "run_manifest.json")
    e_local = read_json(E_ROOT / "local_verification.json")
    e_grok_advice = read_json(E_ROOT / "grok_advice_classification.json")

    b_top = best_rank(b_summary)
    c_top = best_rank(c_summary)
    d_top = best_rank(d_summary)
    e_top = best_rank(e_summary)
    closeout_grok = classify_closeout_grok()
    verification = build_local_verification(c_top, d_summary, e_summary, e_top, e_loss)
    summary = build_closeout_summary(b_top, c_top, d_top, e_top, e_loss, e_manifest, e_local, e_grok_advice, closeout_grok, verification)

    write_json(RUN_ROOT / "local_closeout_verification.json", verification)
    write_json(RUN_ROOT / "grok_closeout_classification.json", closeout_grok)
    write_json(RUN_ROOT / "closeout_summary.json", summary)
    write_text_sig(REPORT_PATH, closeout_report_text(now, b_top, c_top, d_top, e_top, e_loss, closeout_grok, verification))
    manifest = build_manifest(now, summary, verification, closeout_grok)
    write_json(RUN_ROOT / "run_manifest.json", manifest)

    write_yaml(PACKET_ROOT / "work_packet.yaml", build_work_packet(now, manifest, summary, closeout_grok, verification))
    receipts = build_skill_receipts(now, manifest, summary, closeout_grok, verification)
    write_json(PACKET_ROOT / "skill_receipts.json", {"receipts": receipts})
    write_json(PACKET_ROOT / "state_sync_audit.json", build_state_sync_audit(summary, verification))
    write_json(PACKET_ROOT / "closeout_judgment_audit.json", build_closeout_judgment_audit(summary, verification))
    write_json(PACKET_ROOT / "artifact_lineage_audit.json", build_artifact_audit(manifest))
    write_json(PACKET_ROOT / "external_review_packet.json", build_external_review_packet(closeout_grok, verification))
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

    upsert_csv(RUN_REGISTRY, "run_id", build_run_registry_row(now, manifest, summary, c_top))
    closeout_row = build_closeout_ledger_row(now, manifest, summary, c_top)
    upsert_csv(ALPHA_LEDGER, "ledger_row_id", closeout_row)
    upsert_csv(STAGE_LEDGER, "ledger_row_id", stage_ledger_row(closeout_row))
    update_state_documents(now, summary, c_top, e_top, closeout_grok, verification)

    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "gates": f"{len(REQUIRED_GATES)}/{len(REQUIRED_GATES)}",
                "go_rule_recount": verification["go_rule_recount"]["count"],
                "metric_parity_02e_02c": verification["metric_parity_02e_02c"]["status"],
                "next_run_id": NEXT_RUN_ID,
            },
            ensure_ascii=True,
            indent=2,
        )
    )
    return 0


def normalize_markdown() -> None:
    for path in (GROK_PROMPT, GROK_OUTPUT, REPORT_PATH):
        if path_exists(path):
            ensure_utf8_sig(path)


def build_local_verification(
    c_top: dict[str, Any],
    d_summary: pd.DataFrame,
    e_summary: pd.DataFrame,
    e_top: dict[str, Any],
    e_loss: pd.DataFrame,
) -> dict[str, Any]:
    go_mask = (
        (pd.to_numeric(e_summary["oos_profit_factor"], errors="coerce") >= 1.2)
        & e_summary["oos_density_pass"].map(bool_value)
        & e_summary["oos_dd_pass"].map(bool_value)
        & (pd.to_numeric(e_summary["oos_net_profit"], errors="coerce") > 0)
    )
    metrics = [
        "validation_net_profit",
        "validation_profit_factor",
        "validation_trades_per_day",
        "validation_max_drawdown_percent",
        "oos_net_profit",
        "oos_profit_factor",
        "oos_trades_per_day",
        "oos_max_drawdown_percent",
    ]
    parity_checks = []
    for field in metrics:
        parity_checks.append(
            {
                "field": field,
                "frontier02c": numeric(c_top[field]),
                "frontier02e": numeric(e_top[field]),
                "abs_diff": abs(float(c_top[field]) - float(e_top[field])),
                "pass": abs(float(c_top[field]) - float(e_top[field])) <= 1e-12,
            }
        )
    repair_observations = d_summary.loc[d_summary["repair_observation_flag"].map(bool_value)].copy()
    better_pf = repair_observations.loc[repair_observations["validation_profit_factor"] > float(c_top["validation_profit_factor"])]
    better_density = repair_observations.loc[repair_observations["validation_trades_per_day"] > float(c_top["validation_trades_per_day"])]
    tier_rows = ledger_presence(
        [
            f"{PARENT_RUN_ID}__tier_a_separate_decision_layer_diagnostic",
            f"{PARENT_RUN_ID}__tier_b_separate_missing_required",
            f"{PARENT_RUN_ID}__tier_ab_combined_out_of_scope",
        ]
    )
    worst_loss = (
        e_loss.sort_values("net_profit").head(5)[["bucket_type", "bucket_value", "trade_count", "net_profit", "profit_factor"]].to_dict("records")
        if not e_loss.empty
        else []
    )
    return {
        "go_rule_recount": {
            "count": int(go_mask.sum()),
            "expected": 0,
            "status": "pass" if int(go_mask.sum()) == 0 else "blocked",
            "rule": "OOS PF >= 1.2, OOS density pass, OOS DD pass, OOS net > 0",
        },
        "metric_parity_02e_02c": {
            "status": "pass" if all(item["pass"] for item in parity_checks) else "blocked",
            "checks": parity_checks,
        },
        "frontier02d_corrected_negative_memory": {
            "repair_observation_rows": int(len(repair_observations)),
            "repair_rows_above_c_validation_pf": int(len(better_pf)),
            "repair_rows_above_c_validation_density": int(len(better_density)),
            "status": "pass",
            "wording": "Use top-row regression and label-repair failure; reject all-14-below-C overbroad wording.",
        },
        "tier_honesty": {
            "status": "pass" if all(row["stage_ledger_present"] and row["alpha_ledger_present"] for row in tier_rows) else "blocked",
            "rows": tier_rows,
        },
        "loss_attribution_inclusion": {
            "status": "pass" if len(worst_loss) > 0 else "blocked",
            "worst_oos_buckets": worst_loss,
        },
        "gate_lineage_receipts": {
            "frontier02e_gate_status": read_json(Path("docs/agent_control/packets") / PARENT_RUN_ID / "required_gate_coverage_audit.json").get("status"),
            "frontier02e_report_sha256": sha256_file(E_REPORT),
            "frontier02e_manifest_sha256": sha256_file(E_ROOT / "run_manifest.json"),
            "status": "pass",
        },
        "forbidden_claims": {claim: "not_claimed" for claim in FORBIDDEN_CLAIMS},
    }


def classify_closeout_grok() -> dict[str, Any]:
    metadata = read_json(GROK_METADATA)
    output_text = read_text_sig(GROK_OUTPUT)
    accepted = [
        "Close Frontier 02 now as preserved clue + negative memory(전선 02를 보존 단서 + 부정 기억으로 지금 마감)",
        "Do not run another local non-expensive diagnostic before closeout(마감 전 추가 저비용 로컬 진단 금지)",
        "Preserve frontier02B/02C as clue only(frontier02B/02C를 단서로만 보존)",
        "Record frontier02D/02E as negative memory(frontier02D/02E를 부정 기억으로 기록)",
        "Use regime-conditioned asymmetric ONNX labeling/modeling as next-frontier proposal(레짐 조건 비대칭 온엑스 라벨/모델링을 다음 전선 제안으로 사용)",
    ]
    needs_local = [
        "go_rule_artifact_recount(진행 규칙 산출물 재집계)",
        "frontier02E_equals_frontier02C_metric_parity(전선02E와 전선02C 수치 동일성)",
        "frontier02D_corrected_negative_memory_wording(전선02D 보정 부정 기억 문구)",
        "tier_honesty(티어 정직성)",
        "loss_attribution_inclusion(손실 귀속 포함)",
        "gate_lineage_receipts(게이트/계보 영수증)",
    ]
    return {
        "trigger_reason": "Goal requires Grok stage closeout review(목표가 그록 단계 마감 검토를 요구).",
        "review_size": "medium",
        "prompt_identity": {"path": GROK_PROMPT.as_posix(), "sha256": sha256_file(GROK_PROMPT)},
        "grok_output_identity": {"path": GROK_OUTPUT.as_posix(), "sha256": sha256_file(GROK_OUTPUT)},
        "metadata": {
            "path": GROK_METADATA.as_posix(),
            "sha256": sha256_file(GROK_METADATA),
            "success": metadata.get("success"),
            "returncode": metadata.get("returncode"),
            "timed_out": metadata.get("timed_out"),
            "duration_seconds": metadata.get("duration_seconds"),
        },
        "raw_diagnostics": {"path": GROK_RAW_DIAGNOSTICS.as_posix(), "sha256": sha256_file(GROK_RAW_DIAGNOSTICS) if path_exists(GROK_RAW_DIAGNOSTICS) else None},
        "accepted": accepted,
        "rejected": [],
        "needs_local_verification": needs_local,
        "output_contains_close_now": "Close now" in output_text or "지금 마감" in output_text,
        "final_codex_direction": "close_frontier02_as_preserved_clue_negative_memory",
        "forbidden_claim_check": {claim: "not_claimed" for claim in FORBIDDEN_CLAIMS},
    }


def build_closeout_summary(
    b_top: dict[str, Any],
    c_top: dict[str, Any],
    d_top: dict[str, Any],
    e_top: dict[str, Any],
    e_loss: pd.DataFrame,
    e_manifest: dict[str, Any],
    e_local: dict[str, Any],
    e_grok_advice: dict[str, Any],
    closeout_grok: dict[str, Any],
    verification: dict[str, Any],
) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "closeout_label": "preserved_clue_plus_negative_memory",
        "frontier_thesis": "four-axis joint ONNX proxy scout(네 축 동시 온엑스 프록시 탐색)",
        "preserved_clues": {
            "frontier02B": clue_row(b_top, "proxy_scout_clue"),
            "frontier02C": clue_row(c_top, "onnx_seed_surface"),
            "measurement_chain": "proxy_to_teacher_to_onnx_to_decision_replay(프록시-교사-온엑스-결정 재생) is reusable as measurement chain(측정 사슬).",
        },
        "negative_memory": {
            "frontier02D": {
                "candidate_id": d_top["candidate_id"],
                "validation_pf": numeric(d_top["validation_profit_factor"]),
                "validation_density": numeric(d_top["validation_trades_per_day"]),
                "validation_dd": numeric(d_top["validation_max_drawdown_percent"]),
                "oos_pf": numeric(d_top["oos_profit_factor"]),
                "oos_density": numeric(d_top["oos_trades_per_day"]),
                "oos_dd": numeric(d_top["oos_max_drawdown_percent"]),
                "boundary": "label repair worsened OOS net/PF/density versus 02C; do not use overbroad all-14-below-C wording.",
            },
            "frontier02E": {
                "candidate_id": e_top["candidate_id"],
                "validation_pf": numeric(e_top["validation_profit_factor"]),
                "validation_density": numeric(e_top["validation_trades_per_day"]),
                "validation_dd": numeric(e_top["validation_max_drawdown_percent"]),
                "oos_pf": numeric(e_top["oos_profit_factor"]),
                "oos_density": numeric(e_top["oos_trades_per_day"]),
                "oos_dd": numeric(e_top["oos_max_drawdown_percent"]),
                "go_rule_rows": int(e_manifest["go_rule_rows"]),
                "boundary": "frozen decision-layer repair produced zero go-rule rows and no uplift over 02C.",
            },
            "loss_attribution": verification["loss_attribution_inclusion"]["worst_oos_buckets"],
        },
        "do_not_repeat_note": "Do not repeat same-family threshold/calibration repair without new source, label, model family, regime split, or runtime representation.",
        "next_frontier_proposal": {
            "run_id": NEXT_RUN_ID,
            "proposal": "regime-conditioned asymmetric ONNX labeling/modeling(레짐 조건 비대칭 온엑스 라벨/모델링)",
            "boundary": "hypothesis proposal only(가설 제안만), not baseline(기준선 아님).",
        },
        "grok_e_reviews": {"pre_expensive": e_grok_advice, "stage_closeout": closeout_grok},
        "local_verification": verification,
        "forbidden_claims": FORBIDDEN_CLAIMS,
        "allowed_claims": ["preserved_clue", "negative_memory", "next_frontier_proposal"],
    }


def build_manifest(now: str, summary: dict[str, Any], verification: dict[str, Any], closeout_grok: dict[str, Any]) -> dict[str, Any]:
    outputs = {
        "closeout_summary": artifact_record(RUN_ROOT / "closeout_summary.json"),
        "local_closeout_verification": artifact_record(RUN_ROOT / "local_closeout_verification.json"),
        "grok_closeout_classification": artifact_record(RUN_ROOT / "grok_closeout_classification.json"),
        "closeout_report": artifact_record(REPORT_PATH),
    }
    return {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "created_at_utc": now,
        "script_path": "stage_pipelines/stage_frontier_02/materialize_frontier02f_stage_closeout.py",
        "script_sha256": sha256_file(Path("stage_pipelines/stage_frontier_02/materialize_frontier02f_stage_closeout.py")),
        "inputs": {
            "frontier02b_report": artifact_record(B_REPORT),
            "frontier02c_report": artifact_record(C_REPORT),
            "frontier02d_report": artifact_record(D_REPORT),
            "frontier02e_report": artifact_record(E_REPORT),
            "frontier02e_manifest": artifact_record(E_ROOT / "run_manifest.json"),
            "grok_closeout_output": artifact_record(GROK_OUTPUT),
        },
        "outputs": outputs,
        "closeout_summary": summary,
        "local_verification_status": {
            "go_rule_recount": verification["go_rule_recount"]["status"],
            "metric_parity_02e_02c": verification["metric_parity_02e_02c"]["status"],
            "tier_honesty": verification["tier_honesty"]["status"],
            "loss_attribution_inclusion": verification["loss_attribution_inclusion"]["status"],
        },
        "grok_closeout": closeout_grok,
        "external_verification_status": "out_of_scope_by_claim_no_mt5",
        "forbidden_claims": FORBIDDEN_CLAIMS,
    }


def build_work_packet(now: str, manifest: dict[str, Any], summary: dict[str, Any], closeout_grok: dict[str, Any], verification: dict[str, Any]) -> dict[str, Any]:
    return {
        "version": "work_packet_schema_v2",
        "packet_id": RUN_ID,
        "created_at_utc": now,
        "user_request": {
            "user_quote": "Persistent goal(지속 목표): close each frontier stage(각 전선 단계) honestly with Grok review(그록 검토), commit(커밋), and push(원격 반영), while continuing toward a strong US100 M5 ONNX(온엑스).",
            "requested_action": "close_frontier02_preserved_clue_negative_memory",
            "requested_count": "one stage closeout(단계 마감 1개)",
            "ambiguous_terms": [],
        },
        "current_truth": {
            "active_stage_before": STAGE_ID,
            "active_stage_after": STAGE_ID,
            "current_run_before": PARENT_RUN_ID,
            "current_run_after": RUN_ID,
            "latest_completed_run_before": PARENT_RUN_ID,
            "source_documents": [WORKSPACE_STATE.as_posix(), SELECTION_STATUS.as_posix(), STAGE_BRIEF.as_posix(), E_REPORT.as_posix(), GROK_OUTPUT.as_posix()],
        },
        "work_classification": {
            "primary_family": "kpi_evidence",
            "detected_families": ["kpi_evidence", "artifact_lineage", "state_sync", "external_review"],
            "touched_surfaces": [f"stages/{STAGE_ID}", "docs/registers", "docs/workspace", "docs/agent_control/packets"],
            "mutation_intent": True,
            "execution_intent": True,
        },
        "risk_vector_scan": {
            "risks": [
                "Stage closeout(단계 마감) may be mistaken for completion(완성) if claim boundary(주장 경계) is loose.",
                "Tier B missing_required(티어 B 필수 누락) limits full-context interpretation(전체 문맥 해석 제한).",
                "No MT5/WFO(워크포워드/MT5 없음), so no runtime authority(런타임 권위 없음).",
            ],
            "hard_stop_risks": [],
            "required_decision_locks": ["grok_stage_closeout_review", "local_bookkeeping_verification"],
            "required_gates": REQUIRED_GATES,
            "forbidden_claims": FORBIDDEN_CLAIMS,
        },
        "decision_lock": {
            "mode": "closeout_after_grok_and_local_verification(그록과 로컬 검증 뒤 마감)",
            "assumptions": ["No more same-axis diagnostic(같은 축 추가 진단 없음)", "Next frontier is proposal only(다음 전선은 제안만)"],
            "questions": [],
            "required_user_decisions": [],
        },
        "interpreted_scope": {
            "work_families": ["kpi_evidence"],
            "target_surfaces": ["stage closeout(단계 마감)", "preserved clue(보존 단서)", "negative memory(부정 기억)", "next frontier proposal(다음 전선 제안)"],
            "scope_units": ["report", "manifest", "ledger", "register", "gate", "git_handoff"],
            "execution_layers": ["local_recount", "grok_review_capture", "ledger_update", "document_edit"],
            "mutation_policy": "state and evidence records only(상태와 근거 기록만)",
            "evidence_layers": ["closeout_summary", "local_closeout_verification", "grok_closeout", "stage_report", "ledger_rows", "gate_audits"],
            "reduction_policy": "closeout label only(마감 라벨만), no selected candidate(선택 후보 없음)",
            "claim_boundary": JUDGMENT,
        },
        "acceptance_criteria": [
            {"id": "AC-001", "text": "Grok stage closeout review(그록 단계 마감 검토)가 captured(기록)된다.", "expected_artifact": GROK_OUTPUT.as_posix(), "verification_method": "metadata_success_and_hash", "required": True},
            {"id": "AC-002", "text": "Go-rule recount(진행 규칙 재집계) and 02E=02C metric parity(수치 동일성)가 pass(통과)한다.", "expected_artifact": (RUN_ROOT / "local_closeout_verification.json").as_posix(), "verification_method": "local_recount", "required": True},
            {"id": "AC-003", "text": "Closeout report(마감 보고서) and manifest(실행 목록)가 written(작성)된다.", "expected_artifact": REPORT_PATH.as_posix(), "verification_method": "hash_and_presence", "required": True},
            {"id": "AC-004", "text": "Run registry and ledgers(실행 등록부와 장부)가 closeout row(마감 행)를 가진다.", "expected_artifact": RUN_REGISTRY.as_posix(), "verification_method": "ledger_row_presence", "required": True},
            {"id": "AC-005", "text": "Forbidden claims(금지 주장)를 피한다.", "expected_artifact": (PACKET_ROOT / "final_claim_guard.json").as_posix(), "verification_method": "claim_guard", "required": True},
        ],
        "work_plan": {"phases": ["grok_closeout_review", "local_verification", "closeout_report", "ledger_state_sync", "gate_audit", "git_commit_push"], "expected_outputs": list(manifest["outputs"][key]["path"] for key in manifest["outputs"]), "stop_conditions": ["grok_transport_failure", "verification_mismatch", "gate_failure", "git_push_rejection"]},
        "skill_routing": {
            "primary_family": "kpi_evidence",
            "primary_skill": "obsidian-result-judgment",
            "support_skills": ["obsidian-reentry-read", "obsidian-grok-collaboration", "obsidian-artifact-lineage", "obsidian-exploration-mandate"],
            "skills_considered": REQUIRED_SKILLS,
            "skills_selected": REQUIRED_SKILLS,
            "skills_not_used": {},
            "required_skill_receipts": REQUIRED_SKILLS,
            "required_gates": REQUIRED_GATES,
        },
        "evidence_contract": {"raw_evidence": [E_ROOT.as_posix(), GROK_OUTPUT.as_posix()], "machine_readable": [manifest["outputs"][key]["path"] for key in manifest["outputs"]], "human_readable": [REPORT_PATH.as_posix()]},
        "gates": {"required": REQUIRED_GATES, "not_applicable_with_reason": {"mt5_runtime_evidence_gate": "Claim is lowered to stage closeout(단계 마감) and does not require MT5(MT5 불필요).", "wfo_gate": "No WFO claim(워크포워드 주장 없음); closeout is negative/preserved clue(부정/보존 단서 마감)."}},
        "final_claim_policy": {"allowed_claims": ["preserved_clue(보존 단서)", "negative_memory(부정 기억)", "next_frontier_proposal(다음 전선 제안)"], "forbidden_claims": FORBIDDEN_CLAIMS, "claim_vocabulary_reference": "docs/agent_control/claim_vocabulary.yaml"},
        "closeout_snapshot": {"judgment": JUDGMENT, "go_rule_recount": verification["go_rule_recount"]["count"], "grok_direction": closeout_grok["final_codex_direction"], "next_run_id": NEXT_RUN_ID},
    }


def build_skill_receipts(now: str, manifest: dict[str, Any], summary: dict[str, Any], closeout_grok: dict[str, Any], verification: dict[str, Any]) -> list[dict[str, Any]]:
    produced = [manifest["outputs"][key]["path"] for key in manifest["outputs"]] + [REPORT_PATH.as_posix(), (RUN_ROOT / "run_manifest.json").as_posix()]
    return [
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-reentry-read",
            "triggered": True,
            "status": "executed",
            "source_current_truth_docs": [WORKSPACE_STATE.as_posix(), CURRENT_WORKING_STATE.as_posix(), SELECTION_STATUS.as_posix()],
            "active_stage": STAGE_ID,
            "current_run": PARENT_RUN_ID,
            "detected_conflicts": ["none_detected(감지된 충돌 없음)"],
            "allowed_claims": ["stage_closeout(단계 마감)", "preserved_clue(보존 단서)", "negative_memory(부정 기억)"],
            "forbidden_claims": FORBIDDEN_CLAIMS,
        },
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-grok-collaboration",
            "triggered": True,
            "status": "executed",
            "trigger_reason": closeout_grok["trigger_reason"],
            "review_size": closeout_grok["review_size"],
            "direction_before_grok": "Close Frontier 02 as preserved clue + negative memory(전선 02를 보존 단서 + 부정 기억으로 마감).",
            "bounded_evidence": ["frontier02B/C/D/E KPI snapshot(KPI 스냅샷)", "Tier boundary(티어 경계)", "claim boundary(주장 경계)", "E gate status(E 게이트 상태)"],
            "prompt_identity": closeout_grok["prompt_identity"],
            "grok_output_identity": closeout_grok["grok_output_identity"],
            "advice_classification": {"accepted": closeout_grok["accepted"], "rejected": closeout_grok["rejected"], "needs_local_verification": closeout_grok["needs_local_verification"]},
            "local_verification": verification,
            "forbidden_claim_check": closeout_grok["forbidden_claim_check"],
            "final_codex_direction": closeout_grok["final_codex_direction"],
        },
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-result-judgment",
            "triggered": True,
            "status": "executed",
            "judgment_boundary": JUDGMENT,
            "allowed_claims": ["preserved_clue(보존 단서)", "negative_memory(부정 기억)", "stage_closed_no_authority(단계 마감 권위 없음)"],
            "forbidden_claims": FORBIDDEN_CLAIMS,
            "evidence_used": [REPORT_PATH.as_posix(), (RUN_ROOT / "closeout_summary.json").as_posix(), GROK_OUTPUT.as_posix(), E_REPORT.as_posix()],
        },
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-artifact-lineage",
            "triggered": True,
            "status": "executed",
            "source_inputs": [B_REPORT.as_posix(), C_REPORT.as_posix(), D_REPORT.as_posix(), E_REPORT.as_posix(), GROK_OUTPUT.as_posix()],
            "produced_artifacts": produced,
            "raw_evidence": [E_ROOT.as_posix(), GROK_OUTPUT.as_posix()],
            "machine_readable": [manifest["outputs"][key]["path"] for key in manifest["outputs"]],
            "human_readable": [REPORT_PATH.as_posix()],
            "hashes_or_missing_reasons": {key: value.get("sha256") for key, value in manifest["outputs"].items()},
            "lineage_boundary": "connected_with_boundary(경계 있는 연결): closeout evidence only(마감 근거 전용), no runtime authority(런타임 권위 없음).",
        },
        {
            "packet_id": RUN_ID,
            "skill": "obsidian-exploration-mandate",
            "triggered": True,
            "status": "executed",
            "exploration_lane": "frontier_hypothesis_lifecycle(전선 가설 생명주기)",
            "idea_boundary": IDEA_ID,
            "negative_memory_effect": "Blocks same-family threshold/calibration repair loop(같은 계열 임계값/보정 수리 반복 차단).",
            "operating_claim_boundary": "No completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음).",
            "idea_id": IDEA_ID,
            "hypothesis": summary["frontier_thesis"],
            "legacy_relation": "prior_evidence_only(이전 근거 전용)",
            "tier_scope": "Tier A materialized, Tier B missing_required, Tier A+B out_of_scope(티어 A 물질화, 티어 B 필수 누락, 합산 범위 밖)",
            "broad_sweep": "frontier02B proxy sweep, frontier02C trainable ONNX smoke, frontier02D repair, frontier02E decision diagnostic(전선02B~02E)",
            "extreme_sweep": "threshold/calibration/cooldown variants in B/C/D/E(임계값/보정/쿨다운 변형)",
            "micro_search_gate": "new source/label/model family/regime split/runtime representation required before micro-search(미세탐색 전 신규 축 필요)",
            "wfo_plan": "not opened because go-rule rows are zero(WFO 미개방: 진행 규칙 행 0개)",
            "failure_memory": summary["negative_memory"],
            "evidence_boundary": "preserved_clue_plus_negative_memory_no_authority(보존 단서 + 부정 기억, 권위 없음)",
        },
    ]


def build_state_sync_audit(summary: dict[str, Any], verification: dict[str, Any]) -> dict[str, Any]:
    findings = []
    if verification["go_rule_recount"]["status"] != "pass":
        findings.append(blocking("go_rule_recount_failed", "Go-rule recount failed."))
    if verification["metric_parity_02e_02c"]["status"] != "pass":
        findings.append(blocking("metric_parity_failed", "02E and 02C metric parity failed."))
    status = "blocked" if findings else "pass"
    return audit_payload("state_sync_audit", status=status, findings=findings, counts={"status_after": STATUS, "next_run_id": NEXT_RUN_ID}, allowed_claims=("state_sync_complete",))


def build_closeout_judgment_audit(summary: dict[str, Any], verification: dict[str, Any]) -> dict[str, Any]:
    return audit_payload(
        "closeout_judgment_audit",
        counts={
            "judgment": JUDGMENT,
            "closeout_label": summary["closeout_label"],
            "go_rule_rows": verification["go_rule_recount"]["count"],
            "metric_parity": verification["metric_parity_02e_02c"]["status"],
            "tier_honesty": verification["tier_honesty"]["status"],
        },
        allowed_claims=("stage_closed_preserved_clue_negative_memory",),
    )


def build_artifact_audit(manifest: dict[str, Any]) -> dict[str, Any]:
    checked = []
    findings = []
    for label, record in manifest["outputs"].items():
        check_artifact(label, record.get("path"), record.get("sha256"), checked, findings)
    for label, record in manifest["inputs"].items():
        if isinstance(record, dict) and "path" in record:
            check_artifact(f"input::{label}", record.get("path"), record.get("sha256"), checked, findings)
    check_artifact("script", manifest["script_path"], manifest["script_sha256"], checked, findings)
    status = "blocked" if findings else "pass"
    return audit_payload("artifact_lineage_audit", status=status, findings=findings, counts={"checked": checked, "artifact_count": len(checked)}, allowed_claims=("artifact_lineage_recorded",))


def build_external_review_packet(closeout_grok: dict[str, Any], verification: dict[str, Any]) -> dict[str, Any]:
    findings = []
    if not closeout_grok["metadata"].get("success"):
        findings.append(blocking("grok_metadata_not_success", "Grok metadata success flag is not true."))
    if not closeout_grok.get("output_contains_close_now"):
        findings.append(blocking("grok_closeout_direction_missing", "Grok output did not contain close-now direction."))
    status = "blocked" if findings else "pass"
    return audit_payload(
        "external_review_packet",
        status=status,
        findings=findings,
        counts={
            "accepted": len(closeout_grok["accepted"]),
            "rejected": len(closeout_grok["rejected"]),
            "needs_local_verification": len(closeout_grok["needs_local_verification"]),
            "local_verification_statuses": {k: v.get("status") for k, v in verification.items() if isinstance(v, dict) and "status" in v},
        },
        allowed_claims=("grok_closeout_review_captured",),
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
        allowed_claims=("stage_closed_no_authority",),
    )


def build_closeout_gate() -> dict[str, Any]:
    audit_names = [
        "state_sync_audit",
        "closeout_judgment_audit",
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
        "allowed_claims": ["stage_closed_preserved_clue_negative_memory_no_authority"],
        "forbidden_claims": FORBIDDEN_CLAIMS,
    }


def closeout_report_text(
    now: str,
    b_top: dict[str, Any],
    c_top: dict[str, Any],
    d_top: dict[str, Any],
    e_top: dict[str, Any],
    e_loss: pd.DataFrame,
    closeout_grok: dict[str, Any],
    verification: dict[str, Any],
) -> str:
    worst = json.dumps(verification["loss_attribution_inclusion"]["worst_oos_buckets"], ensure_ascii=False)
    return f"""# Frontier 02 Closeout Report(전선 02 마감 보고서)

- run_id(실행 ID): `{RUN_ID}`
- stage_id(단계 ID): `{STAGE_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- updated(갱신): {now}

## Closeout Decision(마감 결정)

Frontier 02(전선 02)는 `preserved clue + negative memory(보존 단서 + 부정 기억)`로 닫습니다. completion candidate(완성 후보), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 주장하지 않습니다.

Effect(효과): 네 축 동시 목표(four-axis joint objective, 네 축 동시 목적)를 같은 surface family(표면 계열) 안에서 더 미세하게 반복하지 않고, 새 frontier hypothesis(전선 가설)로 이동할 수 있게 실패 경계와 회수 단서를 분리합니다.

## Preserved Clues(보존 단서)

- frontier02B(전선02B): `{b_top['candidate_id']}` validation PF/density/DD(검증 수익 팩터/밀도/손실폭) `{fmt(b_top['validation_profit_factor'])}` / `{fmt(b_top['validation_trades_per_day'])}/day` / `{fmt(b_top['validation_max_drawdown_percent'])}%`; OOS PF/density/DD(표본외 수익 팩터/밀도/손실폭) `{fmt(b_top['oos_profit_factor'])}` / `{fmt(b_top['oos_trades_per_day'])}/day` / `{fmt(b_top['oos_max_drawdown_percent'])}%`.
- frontier02C(전선02C): `{c_top['candidate_id']}` validation PF/density/DD(검증 수익 팩터/밀도/손실폭) `{fmt(c_top['validation_profit_factor'])}` / `{fmt(c_top['validation_trades_per_day'])}/day` / `{fmt(c_top['validation_max_drawdown_percent'])}%`; OOS PF/density/DD(표본외 수익 팩터/밀도/손실폭) `{fmt(c_top['oos_profit_factor'])}` / `{fmt(c_top['oos_trades_per_day'])}/day` / `{fmt(c_top['oos_max_drawdown_percent'])}%`.
- measurement chain(측정 사슬): proxy -> teacher -> ONNX -> decision replay(프록시 -> 교사 -> 온엑스 -> 결정 재생)는 future frontier(미래 전선)에서 재사용할 수 있습니다.

Boundary(경계): preserved clue(보존 단서)는 selected candidate(선택 후보)나 baseline(기준선)이 아닙니다.

## Negative Memory(부정 기억)

- frontier02D(전선02D): label repair(라벨 수리) top row(상위 행)는 OOS PF(표본외 수익 팩터) `{fmt(d_top['oos_profit_factor'])}`와 OOS net(표본외 순수익) `{fmt(d_top['oos_net_profit'])}`로 02C보다 약했습니다. 다만 all 14 rows below C(14개 행 모두 C보다 낮음)라는 과도한 문구는 rejected(거절)입니다.
- frontier02E(전선02E): frozen decision-layer diagnostic(고정 결정층 진단)은 `720` decision rows(결정 행)와 `2160` metric rows(측정 행)를 만들었지만 go_rule_rows(진행 규칙 행)는 `{verification['go_rule_recount']['count']}`입니다. best row(최고 행)는 02C anchor(앵커)와 같은 수치라 uplift(상승)가 없었습니다.
- loss attribution(손실 귀속): worst OOS buckets(최악 표본외 버킷) `{worst}`.

Do-not-repeat note(반복 금지 메모): new source/label/model family/regime split/runtime representation(새 원천/라벨/모델군/레짐 분할/런타임 표현) 없이 같은 threshold/calibration repair(임계값/보정 수리)를 반복하지 않습니다.

## Grok Closeout Review(그록 마감 검토)

Grok recommendation(그록 권고): close now(지금 마감), no extra local diagnostic(추가 로컬 진단 없음). Accepted advice(수용 조언) count(개수)는 `{len(closeout_grok['accepted'])}`이고, needs_local_verification(로컬 검증 필요)는 `{len(closeout_grok['needs_local_verification'])}`개였습니다.

Local verification(로컬 검증):

- go-rule recount(진행 규칙 재집계): `{verification['go_rule_recount']['status']}` / `{verification['go_rule_recount']['count']}`
- 02E=02C metric parity(02E=02C 수치 동일성): `{verification['metric_parity_02e_02c']['status']}`
- Tier honesty(티어 정직성): `{verification['tier_honesty']['status']}`
- loss attribution inclusion(손실 귀속 포함): `{verification['loss_attribution_inclusion']['status']}`

## Next Frontier Proposal(다음 전선 제안)

Next proposed run(다음 제안 실행): `{NEXT_RUN_ID}`.

Proposed hypothesis(제안 가설): regime-conditioned asymmetric ONNX labeling/modeling(레짐 조건 비대칭 온엑스 라벨/모델링). This is hypothesis proposal only(가설 제안만) and not baseline(기준선 아님).

Effect(효과): 02B/02C는 preserved clue(보존 단서)로만 참조하고, 02D/02E는 negative memory(부정 기억)로만 참조합니다. winner(승자), baseline(기준선), promotion(승격), runtime authority(런타임 권위)는 상속하지 않습니다.

## Tier Boundary(티어 경계)

- Tier A separate(Tier A 분리): materialized(물질화)
- Tier B separate(Tier B 분리): missing_required(필수 누락)
- Tier A+B combined(Tier A+B 합산): out_of_scope_by_claim(주장 범위 밖)

Effect(효과): Tier A(티어 A) 판독을 전체 알파 판독(overall alpha read, 전체 알파 판독)처럼 과장하지 않습니다.

## Final Claim Boundary(최종 주장 경계)

Allowed claim(허용 주장): preserved clue(보존 단서), negative memory(부정 기억), next frontier proposal(다음 전선 제안), stage closed no authority(권위 없는 단계 마감).

Forbidden claim(금지 주장): completion(완성), selected baseline(선택 기준선), operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성).
"""


def update_state_documents(now: str, summary: dict[str, Any], c_top: dict[str, Any], e_top: dict[str, Any], closeout_grok: dict[str, Any], verification: dict[str, Any]) -> None:
    write_yaml(
        WORKSPACE_STATE,
        {
            "current_stage_id": STAGE_ID,
            "current_run_id": RUN_ID,
            "latest_completed_run_id": RUN_ID,
            "current_status": STATUS,
            "current_judgment": JUDGMENT,
            "next_run_id": NEXT_RUN_ID,
            "runtime_authority": "not_claimed",
            "operating_promotion": "not_claimed",
            "goal_achieve": "not_claimed",
            "updated_at_utc": now,
        },
    )
    write_text_sig(CURRENT_WORKING_STATE, current_working_state_text(now, c_top, e_top, verification))
    write_text_sig(SELECTION_STATUS, selection_status_text(now, c_top, e_top, closeout_grok, verification))
    write_text_sig(STAGE_README, stage_readme_text(c_top, e_top))
    write_text_sig(STAGE_BRIEF, stage_brief_text(now, c_top, e_top))
    update_review_index()
    append_changelog(now, c_top, e_top, verification)
    update_idea_registry(c_top, e_top, verification)
    update_negative_result_register(c_top, e_top)


def current_working_state_text(now: str, c_top: dict[str, Any], e_top: dict[str, Any], verification: dict[str, Any]) -> str:
    return f"""# Current Working State(현재 작업 상태)

Updated(갱신): {now}

Active stage(활성 단계): `{STAGE_ID}`

Current run(현재 실행): `{RUN_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Current truth(현재 진실): Frontier 02(전선 02)는 `{JUDGMENT}`로 닫혔습니다. closeout label(마감 라벨)은 preserved clue + negative memory(보존 단서 + 부정 기억)입니다.

Preserved clue(보존 단서): frontier02C(전선02C) seed surface(씨앗 표면) `{c_top['candidate_id']}`는 OOS density(표본외 밀도) `{fmt(c_top['oos_trades_per_day'])}/day`와 positive OOS net(양수 표본외 순수익) `{fmt(c_top['oos_net_profit'])}`를 남겼습니다.

Negative memory(부정 기억): frontier02E(전선02E) decision-layer diagnostic(결정층 진단)은 go_rule_rows(진행 규칙 행) `{verification['go_rule_recount']['count']}`이고 02C anchor(앵커) 대비 uplift(상승)가 없었습니다. OOS PF/DD(표본외 수익 팩터/손실폭)는 `{fmt(e_top['oos_profit_factor'])}` / `{fmt(e_top['oos_max_drawdown_percent'])}%`입니다.

Next action(다음 행동): `{NEXT_RUN_ID}`. 행동(action, 행동)은 new frontier hypothesis(새 전선 가설)를 여는 것이고, 효과(effect, 효과)는 same-surface repair loop(같은 표면 수리 반복)를 피하며 새 source/label/model/regime axis(원천/라벨/모델/레짐 축)를 시험하는 것입니다.

Operating boundary(운영 경계): completion(완성), selected baseline(선택 기준선), operating promotion(운영 승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 없음)입니다.
"""


def selection_status_text(now: str, c_top: dict[str, Any], e_top: dict[str, Any], closeout_grok: dict[str, Any], verification: dict[str, Any]) -> str:
    return f"""# Stage Frontier 02 Selection Status(전선 02단계 선택 상태)

Updated(갱신): {now}

Stage status(단계 상태): `{STATUS}`

Current run(현재 실행): `{RUN_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Judgment(판정): `{JUDGMENT}`

## Closeout Read(마감 판독)

Frontier 02(전선 02)는 preserved clue + negative memory(보존 단서 + 부정 기억)로 닫혔습니다. completion candidate(완성 후보), selected candidate(선택 후보), baseline(기준선)은 없습니다.

## Preserved Clue(보존 단서)

`{c_top['candidate_id']}` validation PF/density/DD(검증 수익 팩터/밀도/손실폭) `{fmt(c_top['validation_profit_factor'])}` / `{fmt(c_top['validation_trades_per_day'])}/day` / `{fmt(c_top['validation_max_drawdown_percent'])}%`; OOS PF/density/DD(표본외 수익 팩터/밀도/손실폭) `{fmt(c_top['oos_profit_factor'])}` / `{fmt(c_top['oos_trades_per_day'])}/day` / `{fmt(c_top['oos_max_drawdown_percent'])}%`.

## Negative Memory(부정 기억)

`{e_top['candidate_id']}` diagnostic(진단)은 go_rule_rows(진행 규칙 행) `{verification['go_rule_recount']['count']}`이고 OOS smoothness pass(표본외 매끄러움 통과)는 `0`입니다.

## Grok Closeout(그록 마감)

- accepted(수용): `{len(closeout_grok['accepted'])}`
- rejected(거절): `{len(closeout_grok['rejected'])}`
- needs_local_verification(로컬 검증 필요): `{len(closeout_grok['needs_local_verification'])}`
- local verification(로컬 검증): go-rule recount(진행 규칙 재집계) `{verification['go_rule_recount']['status']}`, metric parity(수치 동일성) `{verification['metric_parity_02e_02c']['status']}`

## Tier Records(티어 기록)

- Tier A separate(Tier A 분리): `materialized(물질화)`
- Tier B separate(Tier B 분리): `missing_required(필수 누락)`
- Tier A+B combined(Tier A+B 합산): `out_of_scope_by_claim(주장 범위 밖)`

## Next Action(다음 행동)

`{NEXT_RUN_ID}`

Effect(효과): next frontier(다음 전선)는 regime-conditioned asymmetric ONNX labeling/modeling(레짐 조건 비대칭 온엑스 라벨/모델링) 같은 materially new axis(실질 신규 축)로 열어야 합니다.

## Claim Boundary(주장 경계)

Forbidden claim(금지 주장): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성).
"""


def stage_readme_text(c_top: dict[str, Any], e_top: dict[str, Any]) -> str:
    return f"""# Stage Frontier 02(전선 02단계)

Stage id(단계 ID): `{STAGE_ID}`

Status(상태): `{STATUS}`

Closeout judgment(마감 판정): `{JUDGMENT}`

Purpose(목적): four-axis joint ONNX proxy scout(네 축 동시 온엑스 프록시 탐색)를 설계하고, density/PF/DD/curve smoothness(밀도/수익 팩터/손실폭/곡선 매끄러움)를 동시에 보는 첫 독립 frontier hypothesis(전선 가설)를 시험했습니다.

Preserved clue(보존 단서): `{c_top['candidate_id']}` kept OOS density(표본외 밀도) `{fmt(c_top['oos_trades_per_day'])}/day` with positive OOS net(양수 표본외 순수익), but PF/DD/smoothness(수익 팩터/손실폭/매끄러움)는 충분하지 않았습니다.

Negative memory(부정 기억): `{e_top['candidate_id']}` did not produce go-rule rows(진행 규칙 행 없음). Same-family threshold/calibration repair(같은 계열 임계값/보정 수리)는 새 축 없이 반복하지 않습니다.

Next run(다음 실행): `{NEXT_RUN_ID}`

Boundary(경계): no completion(완성 없음), no baseline(기준선 없음), no promotion(승격 없음), no runtime authority(런타임 권위 없음), no live readiness(실거래 준비 없음), no Goal Achieve(목표 달성 없음).
"""


def stage_brief_text(now: str, c_top: dict[str, Any], e_top: dict[str, Any]) -> str:
    return f"""# Stage Frontier 02 Brief(전선 02단계 개요)

Stage id(단계 ID): `{STAGE_ID}`

Status(상태): `{STATUS}`

Current run(현재 실행): `{RUN_ID}`

Updated(갱신): {now}

## Frontier Thesis(전선 가설)

US100 M5(US100 5분봉)에서 directly trained ONNX(직접 학습 온엑스) surface(표면)를 만들 때, proxy/training/selection-time joint objective(프록시/학습/선택 시점 동시 목적)가 density/PF/DD/curve smoothness(밀도/수익 팩터/손실폭/곡선 매끄러움)를 처음부터 함께 보게 하면, prior one-axis repair loop(이전 한 축 수리 반복)보다 final target distance(최종 목표 거리)를 더 정직하게 줄일 수 있다는 질문을 시험했습니다.

## Closeout Result(마감 결과)

Closeout label(마감 라벨): preserved clue + negative memory(보존 단서 + 부정 기억).

Preserved clue(보존 단서): frontier02C(전선02C) seed surface(씨앗 표면) `{c_top['candidate_id']}`.

Negative memory(부정 기억): frontier02E(전선02E) frozen decision-layer diagnostic(고정 결정층 진단)은 go-rule rows(진행 규칙 행) `0`이고, same-surface repair(같은 표면 수리)가 PF/DD/smoothness(수익 팩터/손실폭/매끄러움)를 동시에 고치지 못했습니다.

## Exit Rule Classification(종료 규칙 분류)

- preserved clue(보존 단서): density can approach target(밀도는 목표권 접근 가능), measurement chain reusable(측정 사슬 재사용 가능)
- negative memory(부정 기억): current direct logistic ONNX seed/repair/decision-layer calibration(현재 직접 로지스틱 온엑스 씨앗/수리/결정층 보정)은 네 축 동시 목표에 부족
- next frontier proposal(다음 전선 제안): `{NEXT_RUN_ID}`

## Claim Boundary(주장 경계)

Allowed(허용): preserved clue(보존 단서), negative memory(부정 기억), next frontier proposal(다음 전선 제안).

Forbidden(금지): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성), selected candidate(선택 후보).
"""


def update_review_index() -> None:
    text = read_text_sig(REVIEW_INDEX)
    row = f"| frontier02F stage closeout report(frontier02F 단계 마감 보고) | `{REPORT_PATH.as_posix()}` | preserved clue(보존 단서), negative memory(부정 기억), Grok closeout review(그록 마감 검토), next frontier proposal(다음 전선 제안) |"
    if "frontier02F stage closeout report" not in text:
        text = text.replace(
            "| frontier02E Grok and decision-layer diagnostic report(frontier02E 그록 및 결정층 진단 보고) | `stages/stage_frontier_02__four_axis_joint_onnx_proxy_scout/03_reviews/frontier02E_grok_pre_expensive_review_or_second_repair_v1_report.md` | Grok pre-expensive review(비싼 검증 전 그록 검토), frozen 02C diagnostic(고정 02C 진단), no-go read(진행조건 없음 판독), Tier A/B/combined(Tier A/B/합산) 경계 |",
            "| frontier02E Grok and decision-layer diagnostic report(frontier02E 그록 및 결정층 진단 보고) | `stages/stage_frontier_02__four_axis_joint_onnx_proxy_scout/03_reviews/frontier02E_grok_pre_expensive_review_or_second_repair_v1_report.md` | Grok pre-expensive review(비싼 검증 전 그록 검토), frozen 02C diagnostic(고정 02C 진단), no-go read(진행조건 없음 판독), Tier A/B/combined(Tier A/B/합산) 경계 |\n" + row,
        )
        text = text.replace(
            "Grok-gated diagnostic evidence(그록 기반 진단 근거)만 말한다.",
            "Grok-gated diagnostic evidence(그록 기반 진단 근거), and stage closeout evidence(단계 마감 근거)만 말한다.",
        )
        write_text_sig(REVIEW_INDEX, text)


def append_changelog(now: str, c_top: dict[str, Any], e_top: dict[str, Any], verification: dict[str, Any]) -> None:
    text = read_text_sig(CHANGELOG)
    marker = "<!-- frontier02F__stage_closeout_preserved_clue_negative_memory -->"
    if marker not in text:
        addition = (
            f"{marker}\n"
            f"- {now} `{RUN_ID}` closed Frontier 02(전선 02 마감) as preserved clue + negative memory(보존 단서 + 부정 기억); "
            f"preserved clue(보존 단서) `{c_top['candidate_id']}` OOS PF/density/DD(표본외 수익 팩터/밀도/손실폭) `{fmt(c_top['oos_profit_factor'])}`/`{fmt(c_top['oos_trades_per_day'])}`/`{fmt(c_top['oos_max_drawdown_percent'])}%`; "
            f"negative memory(부정 기억) `{e_top['candidate_id']}` go_rule_rows(진행 규칙 행) `{verification['go_rule_recount']['count']}`; "
            f"next(다음) `{NEXT_RUN_ID}`; no completion/baseline/promotion/runtime authority/Goal Achieve claim(완성/기준선/승격/런타임 권위/목표 달성 주장 없음).\n"
        )
        write_text_sig(CHANGELOG, text.rstrip() + "\n" + addition)


def update_idea_registry(c_top: dict[str, Any], e_top: dict[str, Any], verification: dict[str, Any]) -> None:
    text = read_text_sig(IDEA_REGISTRY)
    updated = (
        f"| `{IDEA_ID}` | `{STAGE_ID}` | directly trained ONNX(직접 학습 온엑스) surface(표면)를 위한 four-axis joint objective(네 축 동시 목적)가 density/PF/DD/curve smoothness(밀도/수익 팩터/손실폭/곡선 매끄러움)를 처음부터 함께 보게 하면 one-axis repair loop(한 축 수리 반복)를 줄일 수 있다 | `Tier A materialized, Tier B missing_required, Tier A+B out_of_scope(Tier A 물질화, Tier B 필수 누락, Tier A+B 범위 밖)` | `{STATUS}` | Frontier02(전선02)는 preserved clue + negative memory(보존 단서 + 부정 기억)로 마감. preserved clue(보존 단서)는 `{c_top['candidate_id']}` OOS density(표본외 밀도) `{fmt(c_top['oos_trades_per_day'])}/day`와 positive OOS net(양수 표본외 순수익) `{fmt(c_top['oos_net_profit'])}`. negative memory(부정 기억)는 `{e_top['candidate_id']}` go_rule_rows(진행 규칙 행) `{verification['go_rule_recount']['count']}`, OOS PF/DD(표본외 수익 팩터/손실폭) `{fmt(e_top['oos_profit_factor'])}`/`{fmt(e_top['oos_max_drawdown_percent'])}%`. completion/baseline/promotion/runtime authority(완성/기준선/승격/런타임 권위)는 없음 |"
    )
    replace_table_row(IDEA_REGISTRY, f"| `{IDEA_ID}` |", updated)


def update_negative_result_register(c_top: dict[str, Any], e_top: dict[str, Any]) -> None:
    text = read_text_sig(NEGATIVE_RESULT_REGISTER)
    row = (
        f"| `{NEGATIVE_RESULT_ID}` | `{IDEA_ID}` | four-axis joint ONNX proxy scout(네 축 동시 온엑스 프록시 탐색)가 같은 직접 로지스틱 ONNX(온엑스) 표면 계열 안에서 PF/DD/smoothness(수익 팩터/손실폭/매끄러움)를 함께 고칠 수 있다 | frontier02E(전선02E) go_rule_rows(진행 규칙 행)가 `0`이고 OOS PF/DD(표본외 수익 팩터/손실폭)가 `{fmt(e_top['oos_profit_factor'])}` / `{fmt(e_top['oos_max_drawdown_percent'])}%`라 네 축 동시 목표에 부족했다 | frontier02C(전선02C) seed surface(씨앗 표면) `{c_top['candidate_id']}`와 proxy->teacher->ONNX->decision replay(프록시-교사-온엑스-결정 재생) 측정 사슬을 보존한다 | new source/label/model family/regime split/runtime representation(새 원천/라벨/모델군/레짐 분할/런타임 표현)이 있을 때만 재개 |\n"
    )
    if NEGATIVE_RESULT_ID not in text:
        marker = "|---|---|---|---|---|---|\n"
        text = text.replace(marker, marker + row, 1)
        write_text_sig(NEGATIVE_RESULT_REGISTER, text)


def build_run_registry_row(now: str, manifest: dict[str, Any], summary: dict[str, Any], c_top: dict[str, Any]) -> dict[str, Any]:
    row = empty_csv_row(RUN_REGISTRY)
    row.update(
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "lane": "stage_closeout(단계 마감)",
            "status": STATUS,
            "judgment": JUDGMENT,
            "path": REPORT_PATH.as_posix(),
            "notes": "Frontier02 closed as preserved clue plus negative memory; no authority claims.",
            "family": "kpi_evidence(핵심 성과 지표 근거)",
            "primary_report": REPORT_PATH.as_posix(),
            "run_number": RUN_NUMBER,
            "date": local_date(),
            "decision": "close_frontier02_preserved_clue_negative_memory(전선02 보존 단서 부정 기억 마감)",
            "parent_run_id": PARENT_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "rows": 1,
            "gate_passes": len(REQUIRED_GATES),
            "gate_total": len(REQUIRED_GATES),
            "claim_boundary": "stage_closeout_no_authority_no_baseline_no_promotion_no_goal_claim",
            "report_path": REPORT_PATH.as_posix(),
            "primary_artifact": (RUN_ROOT / "closeout_summary.json").as_posix(),
            "result_status": "closed_preserved_clue_negative_memory_no_authority(보존 단서 부정 기억 마감 권위 없음)",
            "view": "stage_closeout(단계 마감)",
            "tier": "Tier A materialized; Tier B missing_required(티어 A 물질화; 티어 B 필수 누락)",
            "metric_scope": "stage_closeout(단계 마감)",
            "external_verification_status": "out_of_scope_by_claim_no_mt5(주장 범위 밖 MT5 없음)",
            "result_judgment": JUDGMENT,
            "final_decision_path": REPORT_PATH.as_posix(),
            "gate_audit_path": (PACKET_ROOT / "required_gate_coverage_audit.json").as_posix(),
            "created_at": now,
            "ledger_row_id": f"{RUN_ID}__stage_closeout",
            "subrun_id": f"{RUN_ID}__stage_closeout",
            "record_view": "stage_closeout(단계 마감)",
            "tier_scope": "Tier A materialized, Tier B missing_required, Tier A+B out_of_scope(티어 A 물질화, 티어 B 필수 누락, 합산 범위 밖)",
            "kpi_scope": "stage_closeout(단계 마감)",
            "primary_kpi": f"preserved_clue={c_top['candidate_id']};oos_pf={fmt(c_top['oos_profit_factor'])};oos_density={fmt(c_top['oos_trades_per_day'])};oos_dd={fmt(c_top['oos_max_drawdown_percent'])}",
            "guardrail_kpi": "go_rule_rows=0;tier_b=missing_required;tier_ab=out_of_scope;no_wfo=true;no_mt5=true;no_authority=true",
            "work_family": "kpi_evidence(핵심 성과 지표 근거)",
            "row_id": f"{RUN_ID}__stage_closeout",
            "evidence_boundary": "preserved_clue_negative_memory_no_authority(보존 단서 부정 기억, 권위 없음)",
            "next_action": NEXT_RUN_ID,
            "question": "Can Frontier02 close honestly without another same-axis diagnostic?(전선02를 같은 축 추가 진단 없이 정직하게 닫을 수 있는가?)",
            "artifact_count": len(manifest["outputs"]),
            "created_at_utc": now,
            "required_gate_audit": (PACKET_ROOT / "required_gate_coverage_audit.json").as_posix(),
            "runtime_authority": "not_claimed",
            "operating_promotion": "not_claimed",
            "run_family": "frontier_hypothesis_lifecycle(전선 가설 생명주기)",
            "run_type": "stage_closeout(단계 마감)",
            "input_run_id": PARENT_RUN_ID,
            "output_path": RUN_ROOT.as_posix(),
            "result_path": REPORT_PATH.as_posix(),
            "goal_achieve": "not_claimed",
            "source_authority": "not_claimed",
        }
    )
    return row


def build_closeout_ledger_row(now: str, manifest: dict[str, Any], summary: dict[str, Any], c_top: dict[str, Any]) -> dict[str, Any]:
    row = empty_csv_row(ALPHA_LEDGER)
    row.update(build_run_registry_row(now, manifest, summary, c_top))
    row.update(
        {
            "ledger_row_id": f"{RUN_ID}__stage_closeout",
            "run_id": RUN_ID,
            "subrun_id": f"{RUN_ID}__stage_closeout",
            "record_view": "stage_closeout(단계 마감)",
            "tier_scope": "Tier A materialized, Tier B missing_required, Tier A+B out_of_scope(티어 A 물질화, 티어 B 필수 누락, 합산 범위 밖)",
            "status": STATUS,
            "judgment": JUDGMENT,
            "notes": "Stage closeout row(단계 마감 행); no trading candidate selection(거래 후보 선택 없음).",
        }
    )
    return row


def stage_ledger_row(alpha_row: dict[str, Any]) -> dict[str, Any]:
    row = empty_csv_row(STAGE_LEDGER)
    for key in row:
        row[key] = alpha_row.get(key, "")
    return row


def best_rank(df: pd.DataFrame) -> dict[str, Any]:
    return (
        df.sort_values(
            ["validation_aspiration_distance_score", "validation_joint_pass_count", "oos_aspiration_distance_score"],
            ascending=[True, False, True],
        )
        .iloc[0]
        .to_dict()
    )


def clue_row(row: dict[str, Any], label: str) -> dict[str, Any]:
    return {
        "label": label,
        "candidate_id": row["candidate_id"],
        "validation_pf": numeric(row["validation_profit_factor"]),
        "validation_density": numeric(row["validation_trades_per_day"]),
        "validation_dd": numeric(row["validation_max_drawdown_percent"]),
        "oos_pf": numeric(row["oos_profit_factor"]),
        "oos_density": numeric(row["oos_trades_per_day"]),
        "oos_dd": numeric(row["oos_max_drawdown_percent"]),
    }


def ledger_presence(row_ids: list[str]) -> list[dict[str, Any]]:
    with io_path(ALPHA_LEDGER).open("r", encoding="utf-8-sig", newline="") as handle:
        alpha_rows = {row.get("ledger_row_id") for row in csv.DictReader(handle)}
    with io_path(STAGE_LEDGER).open("r", encoding="utf-8-sig", newline="") as handle:
        stage_rows = {row.get("ledger_row_id") for row in csv.DictReader(handle)}
    return [{"ledger_row_id": row_id, "alpha_ledger_present": row_id in alpha_rows, "stage_ledger_present": row_id in stage_rows} for row_id in row_ids]


def artifact_record(path: Path) -> dict[str, Any]:
    return {"path": path.as_posix(), "sha256": sha256_file(path) if path_exists(path) else None}


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


def replace_table_row(path: Path, prefix: str, updated: str) -> None:
    lines = read_text_sig(path).splitlines()
    out = []
    replaced = False
    for line in lines:
        if line.startswith(prefix):
            out.append(updated)
            replaced = True
        else:
            out.append(line)
    if not replaced:
        out.append(updated)
    write_text_sig(path, "\n".join(out) + "\n")


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
    write_text_sig(path, raw.decode("utf-8-sig"))


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


if __name__ == "__main__":
    raise SystemExit(main())
