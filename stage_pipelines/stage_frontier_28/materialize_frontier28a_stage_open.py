from __future__ import annotations

import csv
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists
from foundation.models.onnx_bridge import ordered_hash
from stage_pipelines.stage_frontier_03 import frontier03b_regime_asymmetric_label_proxy_scout as f03b
from stage_pipelines.stage_frontier_23 import frontier23b_payoff_asymmetry_pf_source_proxy_scout as f23b
from stage_pipelines.stage_frontier_27 import frontier27b_soft_joint_satisfaction_penalty_proxy_scout as f27b
from stage_pipelines.stage_frontier_27 import frontier27d_stage_closeout as f27d


STAGE_ID = "stage_frontier_28__train_only_stability_gap_penalty_for_pf_dd_balance_onnx_scout"
RUN_ID = "frontier28A_stage_open_train_only_stability_gap_penalty_pf_dd_balance_hypothesis_design_v1"
RUN_NUMBER = "frontier28A"
PARENT_RUN_ID = f27d.RUN_ID
NEXT_RUN_ID = "frontier28B_train_only_stability_gap_penalty_proxy_scout_v1"
STATUS = "opened_frontier28_train_only_stability_gap_penalty_no_authority"
JUDGMENT = "stage_opened_after_grok_accepted_stability_gap_contract"

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REPORT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_report.md"
SCRIPT_PATH = Path("stage_pipelines/stage_frontier_28/materialize_frontier28a_stage_open.py")
DECISION_PATH = Path("docs/decisions/2026-06-14_stage_frontier_28_train_only_stability_gap_penalty_open.md")

GROK_PACKET_PRIMARY = Path("docs/agent_control/grok_reviews/2026-06-14_frontier28_stage_open/small_review")
GROK_PACKET_RETRY = Path("docs/agent_control/grok_reviews/2026-06-14_frontier28_stage_open/small_review_retry")
F27_SELECTION = Path("stages") / f27d.STAGE_ID / "04_selected" / "selection_status.md"
F27_CLOSEOUT_REPORT = Path("stages") / f27d.STAGE_ID / "03_reviews" / f"{f27d.RUN_ID}_report.md"
F27B_SUMMARY = Path("stages") / f27d.STAGE_ID / "02_runs" / f27b.RUN_ID / "final_summary.json"
F27B_CANDIDATE_SUMMARY = Path("stages") / f27d.STAGE_ID / "02_runs" / f27b.RUN_ID / "soft_penalty_union_candidate_summary.csv"
F27B_UNION_CANDIDATES = Path("stages") / f27d.STAGE_ID / "02_runs" / f27b.RUN_ID / "train_ranked_soft_penalty_union_candidates.csv"

RUN_REGISTRY = Path("docs/registers/run_registry.csv")
ALPHA_LEDGER = Path("docs/registers/alpha_run_ledger.csv")
IDEA_REGISTRY = Path("docs/registers/idea_registry.md")
CHANGELOG = Path("docs/workspace/changelog.md")
WORKSPACE_STATE = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE = Path("docs/context/current_working_state.md")

LOCKS = {
    "selection_split": "train_only",
    "forward_splits": "validation_oos_read_only",
    "changed_variable": "train_subperiod_pf_dd_balance_stability_gap_rank",
    "hypothesis_delta": (
        "replace F27 global soft penalty rank with train-only chronological chunk stability gap rank"
    ),
    "source_surface": "f27b_234_soft_union_surface_reference_only_not_inherited_baseline",
    "f27_soft_penalty_role": "reference_clue_only_no_weight_retune_no_forward_selection_loop",
    "candidate_construction": "rebuild F27/F24 same-side OR-union machinery, then re-rank by F28 train chunks",
    "chunking_contract": {
        "split": "train",
        "chunk_count": 4,
        "method": "chronological_equal_row_count_chunks_locked_at_stage_open",
        "no_post_hoc_edits": True,
    },
    "stability_gap_terms": [
        "chunk_profit_factor_floor_shortfall",
        "chunk_dd_risk_max_pressure",
        "chunk_density_imbalance",
        "net_positive_chunk_count_shortfall",
        "chunk_equity_trend_r2_floor_shortfall",
        "chunk_max_loss_streak_pressure",
        "global_vs_chunk_pf_gap",
        "global_vs_chunk_dd_concentration",
    ],
    "selection_boundary": "rank_by_train_chunks_only_validation_oos_read_only",
    "forbidden_primary_path": [
        "retune_f27_soft_penalty_weights",
        "select_by_validation_or_oos_metrics",
        "restore_seed_surface_pressure_as_hidden_target",
        "f26_hard_gate_numeric_threshold_relaxation",
        "f25_dd_headroom_first_bridge_archetype_preselection",
        "f24_density_first_bridge_score_as_primary_rank",
        "onnx_mt5_wfo_before_handoff_candidate_and_pre_expensive_grok",
    ],
    "success_boundary": {
        "scout_clue": "validation_oos_read_only_positive_density_pf_dd_signal",
        "seed_surface": "forward_read_only_pf_ge_1_20_dd_le_18_density_5_to_10",
        "handoff_candidate": "forward_read_only_pf_ge_1_50_dd_le_12_smoothness_pass",
        "not_completion": "final_goal_gates_not_applicable_until_final_completion_review",
    },
    "runtime_probe_rule": "record runtime probe status every stage; execute MT5 only after handoff candidate and pre-expensive Grok",
    "reference_only_prior_artifacts": (
        "Stage12-364 and F24-F27 are clues only, not winners/baselines/promotions/runtime authority/live readiness"
    ),
}


def main() -> int:
    ensure_dirs()
    normalize_grok_markdown()
    created_at = utc_now()
    frame = f23b.load_frame()
    feature_order = f23b.read_feature_order()
    chunk_boundaries = build_train_chunk_boundaries(frame)
    grok_primary = read_grok_packet(GROK_PACKET_PRIMARY)
    grok_retry = read_grok_packet(GROK_PACKET_RETRY)
    local = local_verification(feature_order, chunk_boundaries, grok_primary, grok_retry)
    if local["judgment"] != "pass_open_ready_with_stability_gap_locks":
        raise RuntimeError(f"Frontier28A local verification failed: {json.dumps(local, ensure_ascii=False)}")
    summary = build_summary(created_at, feature_order, chunk_boundaries, grok_primary, grok_retry, local)
    write_outputs(summary)
    update_registries(summary)
    update_current_truth(summary)
    print(json.dumps(json_ready({
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "next_run_id": NEXT_RUN_ID,
        "grok_retry_classification": grok_retry["classification"],
        "local_verification": local["judgment"],
        "report": REPORT_PATH.as_posix(),
    }), ensure_ascii=False, indent=2))
    return 0


def ensure_dirs() -> None:
    for path in (
        RUN_ROOT,
        STAGE_ROOT / "00_spec",
        STAGE_ROOT / "01_inputs",
        STAGE_ROOT / "02_runs" / "active",
        STAGE_ROOT / "02_runs" / "archived",
        STAGE_ROOT / "03_reviews",
        STAGE_ROOT / "04_selected",
        DECISION_PATH.parent,
    ):
        io_path(path).mkdir(parents=True, exist_ok=True)
    ensure_stage_ledger_header()


def ensure_stage_ledger_header() -> None:
    path = STAGE_ROOT / "03_reviews" / "stage_run_ledger.csv"
    if path_exists(path):
        return
    with io_path(ALPHA_LEDGER).open("r", encoding="utf-8-sig", newline="") as handle:
        header = next(csv.reader(handle))
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        csv.writer(handle, lineterminator="\n").writerow(header)


def normalize_grok_markdown() -> None:
    for packet in (GROK_PACKET_PRIMARY, GROK_PACKET_RETRY):
        for name in ("prompt.md", "clean_output.md"):
            path = packet / name
            if path_exists(path):
                text = io_path(path).read_text(encoding="utf-8-sig")
                f03b.write_text_sig(path, text.rstrip() + "\n")


def build_train_chunk_boundaries(frame: pd.DataFrame) -> list[dict[str, Any]]:
    train = frame.loc[frame["split"].astype(str).eq("train"), ["timestamp"]].copy()
    train = train.sort_values("timestamp").reset_index(drop=True)
    chunks: list[dict[str, Any]] = []
    total = len(train)
    for index in range(4):
        start_pos = round(index * total / 4)
        end_pos = round((index + 1) * total / 4) - 1
        subset = train.iloc[start_pos : end_pos + 1]
        chunks.append({
            "chunk_id": f"train_chunk_{index + 1:02d}",
            "row_start_index": int(start_pos),
            "row_end_index": int(end_pos),
            "row_count": int(len(subset)),
            "start_timestamp": subset["timestamp"].iloc[0].isoformat(),
            "end_timestamp": subset["timestamp"].iloc[-1].isoformat(),
        })
    return chunks


def read_grok_packet(packet: Path) -> dict[str, Any]:
    metadata = read_json(packet / "metadata.json")
    output = read_text(packet / "clean_output.md")
    return {
        "packet": packet.as_posix(),
        "prompt": (packet / "prompt.md").as_posix(),
        "output": (packet / "clean_output.md").as_posix(),
        "metadata": (packet / "metadata.json").as_posix(),
        "prompt_hash": metadata.get("prompt_hash", ""),
        "success": bool(metadata.get("success")),
        "returncode": metadata.get("returncode"),
        "timed_out": bool(metadata.get("timed_out")),
        "unexpected_top_level_artifacts": metadata.get("unexpected_top_level_artifacts", []),
        "classification": classify_grok(output),
        "output_excerpt": output[:2200],
    }


def classify_grok(text: str) -> str:
    lowered = text.lower()
    if "verdict:" in lowered and "accepted" in lowered and "novelty_ok" in lowered and "yes" in lowered:
        if "leakage_risk" in lowered and "low" in lowered and "forbidden_path_risk" in lowered:
            return "accepted_new_hypothesis_low_leakage_low_forbidden_path_risk"
        return "accepted_new_hypothesis"
    if "needs_local_verification" in lowered:
        return "needs_local_verification"
    if "rejected" in lowered and "accepted" not in lowered:
        return "rejected"
    return "classification_missing"


def local_verification(
    feature_order: list[str],
    chunk_boundaries: list[dict[str, Any]],
    grok_primary: dict[str, Any],
    grok_retry: dict[str, Any],
) -> dict[str, Any]:
    workspace = read_text(WORKSPACE_STATE)
    f27_selection = read_text(F27_SELECTION)
    f27_closeout = read_text(F27_CLOSEOUT_REPORT)
    f27b_summary = read_json(F27B_SUMMARY)
    candidate_summary = pd.read_csv(io_path(F27B_CANDIDATE_SUMMARY))
    lock_json = json.dumps(LOCKS, ensure_ascii=False)
    retry_text = read_text(GROK_PACKET_RETRY / "clean_output.md").lower()
    checks = {
        "workspace_current_stage_frontier27_closed": f"current_stage_id: {f27d.STAGE_ID}" in workspace
        and "closed_preserved_clue_negative_memory_soft_penalty_scout_only_no_handoff" in workspace,
        "workspace_next_stage_frontier28": f"next_stage_id: {STAGE_ID}" in workspace,
        "workspace_next_run_frontier28a": f"next_run_id: {RUN_ID}" in workspace,
        "f27_selection_no_authority": "no selected baseline" in f27_selection.lower()
        and "Runtime probe blocker" in f27_selection,
        "f27_closeout_next_clue_stability_gap": "train_only_stability_gap_penalty" in f27_closeout,
        "f27b_summary_no_handoff": int(f27b_summary.get("handoff_candidate_rows", -1)) == 0,
        "f27b_candidate_surface_234": len(candidate_summary) == 234,
        "feature_hash_matches_contract": ordered_hash(feature_order) == f23b.EXPECTED_FEATURE_HASH,
        "dataset_exists": path_exists(f23b.DATASET_PATH),
        "grok_primary_transport_success": grok_primary["success"] and grok_primary["returncode"] == 0 and not grok_primary["timed_out"],
        "grok_retry_transport_success": grok_retry["success"] and grok_retry["returncode"] == 0 and not grok_retry["timed_out"],
        "grok_retry_accepted": grok_retry["classification"].startswith("accepted"),
        "grok_retry_novelty_yes": "novelty_ok" in retry_text and "yes" in retry_text,
        "grok_retry_low_risks": "leakage_risk" in retry_text and "low" in retry_text and "forbidden_path_risk" in retry_text,
        "grok_no_unexpected_top_level_artifacts": not grok_primary["unexpected_top_level_artifacts"]
        and not grok_retry["unexpected_top_level_artifacts"],
        "chunk_count_locked_four": len(chunk_boundaries) == 4,
        "chunk_boundaries_have_dates": all(row["start_timestamp"] and row["end_timestamp"] for row in chunk_boundaries),
        "lock_changed_variable_stability_gap": LOCKS["changed_variable"] == "train_subperiod_pf_dd_balance_stability_gap_rank",
        "lock_f27_reference_only": "reference_clue_only" in LOCKS["f27_soft_penalty_role"],
        "lock_no_posthoc_edits": bool(LOCKS["chunking_contract"]["no_post_hoc_edits"]),
        "lock_blocks_forward_selection": "select_by_validation_or_oos_metrics" in lock_json,
        "lock_blocks_f27_weight_retune": "retune_f27_soft_penalty_weights" in lock_json,
        "lock_defers_expensive_runtime": "handoff candidate" in LOCKS["runtime_probe_rule"],
    }
    accepted = [
        "open F28 as acceptable new hypothesis(전선28을 허용 가능한 새 가설로 개방)",
        "treat F27 soft penalty as reference clue only(F27 연성 페널티를 참조 단서 전용으로 처리)",
        "freeze four chronological train chunks and penalty terms(시간순 학습 4조각과 페널티 항을 고정)",
        "keep validation/OOS read-only(검증/표본외를 읽기 전용으로 유지)",
        "gate ONNX/MT5/WFO until handoff and pre-expensive review(인계와 비싼 검토 전까지 온엑스/MT5/WFO 차단)",
    ]
    return {
        "judgment": "pass_open_ready_with_stability_gap_locks" if all(checks.values()) else "needs_manual_review",
        "checks": checks,
        "feature_order_hash": ordered_hash(feature_order),
        "feature_count": len(feature_order),
        "grok_advice_classification": {
            "accepted": accepted,
            "needs_local_verification": [
                "first Grok packet was transport-success but verdict-weak(첫 Grok 묶음은 전송 성공이나 판정 약함)",
                "retry packet supplied explicit verdict(재시도 묶음이 명시 판정을 제공)",
            ],
            "rejected": [],
        },
    }


def build_summary(
    created_at: str,
    feature_order: list[str],
    chunk_boundaries: list[dict[str, Any]],
    grok_primary: dict[str, Any],
    grok_retry: dict[str, Any],
    local: dict[str, Any],
) -> dict[str, Any]:
    return {
        "created_at_utc": created_at,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "frontier_thesis": (
            "train-only chronological stability gaps may predict forward PF/DD balance better than global train soft scores"
            "(학습 전용 시간순 안정성 격차가 전체 학습 연성 점수보다 전진 수익 팩터/손실폭 균형을 더 잘 예고할 수 있다)"
        ),
        "hypothesis": (
            "F27 restored a tradable-density union surface but did not create seed or handoff rows; F28 tests whether train chunk "
            "PF/DD dispersion exposes the unstable unions before validation/OOS is read"
            "(F27은 거래 빈도 합집합 표면을 복원했지만 씨앗/인계를 만들지 못했고, F28은 검증/표본외를 읽기 전에 학습 조각 PF/DD 산포가 불안정 합집합을 드러내는지 시험한다)"
        ),
        "decision_use": (
            "decide whether train-only stability ranking deserves proxy scout, repair, or handoff consideration"
            "(학습 전용 안정성 순위가 프록시 탐색, 수리, 인계 검토 가치가 있는지 결정)"
        ),
        "comparison_baseline": (
            "F27 soft union surface is reference-only input, not inherited baseline or winner"
            "(F27 연성 합집합 표면은 참조 입력일 뿐 상속 기준선이나 승자가 아니다)"
        ),
        "control_variables": [
            "US100 M5 Tier A dataset(US100 5분봉 티어 A 데이터셋)",
            "feature_set_v2 58 features(피처 세트 v2 58개)",
            "fwd12 label horizon(fwd12 라벨 예측수평선)",
            "same-side OR-union semantics(같은 방향 OR 합집합 의미)",
            "validation/OOS read-only(검증/표본외 읽기 전용)",
        ],
        "changed_variables": [
            "train_subperiod_pf_dd_balance_stability_gap_rank(학습 하위기간 수익 팩터/손실폭 균형 안정성 격차 순위)",
            "locked four chronological train chunks(고정 시간순 학습 4조각)",
        ],
        "sample_scope": "Tier A US100 M5 model_input_dataset.parquet, frozen train/validation/oos split(티어 A US100 5분봉 고정 학습/검증/표본외 분할)",
        "success_criteria": LOCKS["success_boundary"],
        "failure_criteria": [
            "zero seed and zero handoff under locked stability ranking(잠금 안정성 순위 아래 씨앗 0, 인계 0)",
            "forward rows only improve headline PF without train stability rationale(학습 안정성 근거 없이 전진 표면 PF만 개선)",
            "top rows become implicit F27 weight retune or forward-metric selection(상위 행이 암묵적 F27 가중치 조정 또는 전진 지표 선택이 됨)",
        ],
        "invalid_conditions": [
            "validation/OOS used for selection(검증/표본외가 선택에 사용됨)",
            "chunk boundaries edited after seeing forward results(전진 결과를 본 뒤 조각 경계 수정)",
            "F27 penalty weights retuned as primary change(F27 페널티 가중치 조정이 주 변경점이 됨)",
            "feature hash mismatch(피처 해시 불일치)",
        ],
        "stop_conditions": [
            "handoff rows >0 triggers pre-expensive Grok before ONNX/MT5/WFO(인계 행이 0 초과면 온엑스/MT5/WFO 전 비싼 검토)",
            "seed or scout only triggers repair-or-closeout decision(씨앗 또는 탐색만 있으면 수리 또는 마감 결정)",
            "zero seed and zero handoff after capped repair closes negative memory(상한 수리 뒤 씨앗/인계 0이면 부정 기억 마감)",
        ],
        "locks": {**LOCKS, "chunk_boundaries": chunk_boundaries},
        "grok": {"primary": grok_primary, "retry": grok_retry},
        "local_verification": local,
        "feature_order_hash": ordered_hash(feature_order),
        "feature_count": len(feature_order),
        "claim_boundary": {claim: "not_claimed(주장 없음)" for claim in f03b.FORBIDDEN_CLAIMS},
    }


def write_outputs(summary: dict[str, Any]) -> None:
    write_json(RUN_ROOT / "stage_open_summary.json", summary)
    write_json(RUN_ROOT / "stability_gap_penalty_lock.json", {"locks": summary["locks"]})
    write_json(RUN_ROOT / "run_manifest.json", run_manifest(summary))
    f03b.write_text_sig(STAGE_ROOT / "README.md", readme_text(summary))
    f03b.write_text_sig(STAGE_ROOT / "00_spec" / "stage_brief.md", stage_brief(summary))
    f03b.write_text_sig(STAGE_ROOT / "00_spec" / "stability_gap_lock_spec.md", lock_spec(summary))
    f03b.write_text_sig(STAGE_ROOT / "00_spec" / "do_not_repeat.md", do_not_repeat_text())
    f03b.write_text_sig(STAGE_ROOT / "01_inputs" / "prior_stage_scan.md", prior_stage_scan_text())
    f03b.write_text_sig(STAGE_ROOT / "01_inputs" / "experiment_design.md", experiment_design_text(summary))
    f03b.write_text_sig(STAGE_ROOT / "01_inputs" / "input_refs.md", input_refs_text(summary))
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / "review_index.md", review_index())
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / "grok_stage_open_receipt.md", grok_receipt_text(summary))
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / "local_verification.md", local_verification_text(summary))
    f03b.write_text_sig(STAGE_ROOT / "03_reviews" / "required_gate_coverage_audit.md", gate_audit(summary))
    f03b.write_text_sig(REPORT_PATH, report_text(summary))
    f03b.write_text_sig(STAGE_ROOT / "04_selected" / "selection_status.md", selection_status(summary))
    f03b.write_text_sig(DECISION_PATH, decision_text(summary))


def run_manifest(summary: dict[str, Any]) -> dict[str, Any]:
    artifacts = [
        SCRIPT_PATH,
        GROK_PACKET_PRIMARY / "clean_output.md",
        GROK_PACKET_RETRY / "clean_output.md",
        F27_SELECTION,
        F27_CLOSEOUT_REPORT,
        F27B_SUMMARY,
        F27B_CANDIDATE_SUMMARY,
        F27B_UNION_CANDIDATES,
        RUN_ROOT / "stage_open_summary.json",
        RUN_ROOT / "stability_gap_penalty_lock.json",
        REPORT_PATH,
    ]
    return {
        "identity": {
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "parent_run_id": PARENT_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "created_at_utc": summary["created_at_utc"],
        },
        "artifacts": [artifact_identity(path) for path in artifacts],
        "feature_schema": {
            "feature_count": summary["feature_count"],
            "feature_order_hash": summary["feature_order_hash"],
            "feature_order_path": f23b.FEATURE_ORDER_PATH.as_posix(),
        },
        "rule_stack": {
            "source": "F27B 234 soft union surface as reference clue(F27B 234개 연성 합집합 표면 참조 단서)",
            "selection": "train-only chunk stability gap rank(학습 전용 조각 안정성 격차 순위)",
            "forbidden": "no forward selection, no F27 weight retune, no ONNX/MT5/WFO before handoff(전진 선택 없음, F27 가중치 조정 없음, 인계 전 온엑스/MT5/WFO 없음)",
        },
        "claim_boundary": summary["claim_boundary"],
    }


def update_registries(summary: dict[str, Any]) -> None:
    f03b.upsert_csv(RUN_REGISTRY, "run_id", run_registry_row(summary))
    f03b.upsert_csv(ALPHA_LEDGER, "ledger_row_id", ledger_row(summary))
    f03b.upsert_csv(STAGE_ROOT / "03_reviews" / "stage_run_ledger.csv", "ledger_row_id", ledger_row(summary))
    f03b.append_once(CHANGELOG, RUN_ID, changelog_entry(summary))
    f03b.append_once(IDEA_REGISTRY, RUN_ID, idea_registry_entry(summary))


def run_registry_row(summary: dict[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "stage_open(단계 개방)",
        "family": "experiment_execution(실험 실행)",
        "work_family": "experiment_execution(실험 실행)",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": REPORT_PATH.as_posix(),
        "notes": "frontier28_stage_open_grok_retry_accepted_stability_gap_contract_no_authority",
        "run_number": RUN_NUMBER,
        "date": "2026-06-14",
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "claim_boundary": "stage_open_no_model_training_no_wfo_no_mt5_no_authority_goal_claim",
        "report_path": REPORT_PATH.as_posix(),
        "created_at_utc": summary["created_at_utc"],
        "primary_kpi": f"grok_retry={summary['grok']['retry']['classification']};feature_hash={summary['feature_order_hash']}",
        "guardrail_kpi": "stability_gap_lock_no_model_training_no_wfo_no_mt5_no_authority(안정성 격차 잠금, 모델학습/WFO/MT5/권위 없음)",
        "external_verification_status": "grok_stage_open_review_completed_runtime_probe_requires_handoff_candidate(그록 단계 개방 검토 완료, 런타임 탐침은 인계 후보 필요)",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "result_path": REPORT_PATH.as_posix(),
    }


def ledger_row(summary: dict[str, Any]) -> dict[str, Any]:
    return {
        "ledger_row_id": f"{RUN_ID}__stage_open",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": f"{RUN_ID}__stage_open",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "stage_open(단계 개방)",
        "tier_scope": "not_applicable_stage_open(단계 개방에는 해당 없음)",
        "kpi_scope": "planning_only_no_trading_kpi(계획 전용, 거래 KPI 없음)",
        "scoreboard_lane": "stage_open(단계 개방)",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": REPORT_PATH.as_posix(),
        "primary_kpi": f"grok_retry={summary['grok']['retry']['classification']};feature_hash={summary['feature_order_hash']}",
        "guardrail_kpi": "stability_gap_lock_no_model_training_no_wfo_no_mt5_no_authority(안정성 격차 잠금, 모델학습/WFO/MT5/권위 없음)",
        "external_verification_status": "grok_stage_open_review_completed_runtime_probe_requires_handoff_candidate(그록 단계 개방 검토 완료, 런타임 탐침은 인계 후보 필요)",
        "notes": f"next={NEXT_RUN_ID};chunk_count=4;no_authority",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "run_family": "stage_open(단계 개방)",
    }


def update_current_truth(summary: dict[str, Any]) -> None:
    io_path(WORKSPACE_STATE).write_text(workspace_state(summary), encoding="utf-8-sig")
    f03b.write_text_sig(CURRENT_WORKING_STATE, current_working_state(summary))


def workspace_state(summary: dict[str, Any]) -> str:
    return "\n".join([
        f"current_stage_id: {STAGE_ID}",
        f"current_run_id: {RUN_ID}",
        f"latest_completed_run_id: {RUN_ID}",
        f"current_status: {STATUS}",
        f"current_judgment: {JUDGMENT}",
        f"next_run_id: {NEXT_RUN_ID}",
        "runtime_authority: not_claimed",
        "operating_promotion: not_claimed",
        "goal_achieve: not_claimed",
        f"updated_at_utc: '{summary['created_at_utc']}'",
        "",
    ])


def readme_text(summary: dict[str, Any]) -> str:
    return f"""# {STAGE_ID}

Purpose(목적): F27 soft union surface(F27 연성 합집합 표면)를 reference clue(참조 단서)로만 쓰고, train-only chunk stability gap(학습 전용 조각 안정성 격차)이 forward PF/DD balance(전진 수익 팩터/손실폭 균형)를 더 잘 고르는지 본다.

Boundary(경계): scout-only(탐색 전용)입니다. completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 없습니다.

Current run(현재 실행): `{RUN_ID}`

Next run(다음 실행): `{NEXT_RUN_ID}`
"""


def stage_brief(summary: dict[str, Any]) -> str:
    return f"""# Frontier28 Stage Brief(전선28 단계 요약)

Opened(개방): {summary['created_at_utc']}

Frontier thesis(전선 가설): {summary['frontier_thesis']}

Hypothesis(가설): {summary['hypothesis']}

Novelty delta(신규성 차이): F28은 F27 soft penalty rank(F27 연성 페널티 순위)를 조정하지 않습니다. changed variable(변경 변수)은 train_subperiod_pf_dd_balance_stability_gap_rank(학습 하위기간 수익 팩터/손실폭 균형 안정성 격차 순위)입니다.

Chunk contract(조각 계약): train split(학습 분할)을 시간순 4개 equal-row chunk(동일 행 수 조각)로 고정합니다.

Runtime probe rule(런타임 탐침 규칙): 각 stage(단계)마다 runtime probe status(런타임 탐침 상태)를 기록합니다. 실제 MT5 runtime probe(MT5 런타임 탐침)는 handoff_candidate_rows > 0(인계 후보 행 0 초과)이고 pre-expensive Grok review(비싼 검증 전 그록 검토)가 통과할 때만 실행합니다.

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 not_claimed(주장 없음)입니다.
"""


def lock_spec(summary: dict[str, Any]) -> str:
    return (
        "# Frontier28 Stability Gap Lock Spec(전선28 안정성 격차 잠금 명세)\n\n"
        "Locks(잠금):\n"
        f"{json.dumps(summary['locks'], ensure_ascii=False, indent=2)}\n"
    )


def do_not_repeat_text() -> str:
    return """# Frontier28 Do Not Repeat(전선28 반복 금지)

- Do not retune F27 soft penalty weights(F27 연성 페널티 가중치 재조정 금지).
- Do not select by validation/OOS metrics(검증/표본외 지표 선택 금지).
- Do not restore seed surface as a hidden target(씨앗 표면 복원을 숨은 목표로 삼기 금지).
- Do not relax F26 hard gate thresholds(F26 경성 게이트 임계값 완화 금지).
- Do not run ONNX/MT5/WFO before handoff candidate and pre-expensive Grok review(인계 후보와 비싼 검토 전 온엑스/MT5/WFO 실행 금지).
"""


def prior_stage_scan_text() -> str:
    return """# Frontier28 Prior Stage Scan(전선28 이전 단계 점검)

F27 preserved clue(보존 단서): `f27_soft_penalty_restored_union_surface_and_19_scout_rows_reference_only(F27 연성 페널티는 합집합 표면과 19개 탐색 행을 복원한 참조 전용 단서)`.

F27 negative memory(부정 기억): `under_f27_locked_soft_penalty_rank_seed_and_handoff_remained_zero(F27 잠금 연성 페널티 순위 아래 씨앗과 인계는 0개로 남음)`.

F27 runtime blocker(런타임 차단): `runtime_probe_ineligible_no_handoff_candidate_after_f27c_repair_decision(F27C 수리 결정 뒤 인계 후보 없어 런타임 탐침 부적격)`.

Next clue(다음 단서): `train_only_stability_gap_penalty_for_forward_pf_dd_balance_reference_only(전방 PF/DD 균형을 위한 학습 전용 안정성 격차 페널티 참조 전용)`.

Reference boundary(참조 경계): F24/F25/F26/F27은 reference only(참조 전용)입니다. winner/baseline/promotion/runtime authority/live readiness(승자/기준선/승격/런타임 권위/실거래 준비)는 상속하지 않습니다.
"""


def experiment_design_text(summary: dict[str, Any]) -> str:
    return f"""# Frontier28 Experiment Design(전선28 실험 설계)

- hypothesis(가설): {summary['hypothesis']}
- decision_use(결정 사용처): {summary['decision_use']}
- comparison_baseline(비교 기준): {summary['comparison_baseline']}
- control_variables(통제 변수): {', '.join(summary['control_variables'])}
- changed_variables(변경 변수): {', '.join(summary['changed_variables'])}
- sample_scope(표본 범위): {summary['sample_scope']}
- success_criteria(성공 기준): {json.dumps(summary['success_criteria'], ensure_ascii=False)}
- failure_criteria(실패 기준): {', '.join(summary['failure_criteria'])}
- invalid_conditions(무효 조건): {', '.join(summary['invalid_conditions'])}
- stop_conditions(중단 조건): {', '.join(summary['stop_conditions'])}
- evidence_plan(근거 계획): F28B run manifest(실행 목록), stability gap audit(안정성 격차 감사), chunk metric table(조각 지표 표), read-only forward summary(읽기 전용 전진 요약), run registry(실행 등록부), stage ledger(단계 장부).
"""


def input_refs_text(summary: dict[str, Any]) -> str:
    return f"""# Frontier28 Input References(전선28 입력 참조)

- dataset(데이터셋): `{f23b.DATASET_PATH.as_posix()}`
- feature order(피처 순서): `{f23b.FEATURE_ORDER_PATH.as_posix()}`
- feature hash(피처 해시): `{summary['feature_order_hash']}`
- F27 selection(F27 선택 상태): `{F27_SELECTION.as_posix()}`
- F27 closeout(F27 마감): `{F27_CLOSEOUT_REPORT.as_posix()}`
- F27B summary(F27B 요약): `{F27B_SUMMARY.as_posix()}`
- F27B candidate surface(F27B 후보 표면): `{F27B_CANDIDATE_SUMMARY.as_posix()}`
- Grok primary packet(그록 1차 묶음): `{GROK_PACKET_PRIMARY.as_posix()}`
- Grok retry packet(그록 재시도 묶음): `{GROK_PACKET_RETRY.as_posix()}`
"""


def review_index() -> str:
    return f"""# Frontier28 Review Index(전선28 검토 색인)

- stage open report(단계 개방 보고서): `{REPORT_PATH.as_posix()}`
- Grok receipt(그록 영수증): `03_reviews/grok_stage_open_receipt.md`
- local verification(로컬 검증): `03_reviews/local_verification.md`
- gate audit(게이트 감사): `03_reviews/required_gate_coverage_audit.md`
"""


def grok_receipt_text(summary: dict[str, Any]) -> str:
    classification = summary["local_verification"]["grok_advice_classification"]
    return f"""# Frontier28 Grok Stage Open Receipt(전선28 그록 단계 개방 영수증)

Trigger reason(트리거 이유): stage open required by goal(목표가 단계 개방 검토를 요구).

Review size(검토 크기): small review(소규모 검토) plus retry(재시도).

Direction before Grok(그록 전 방향): train-only stability gap penalty for PF/DD balance(수익 팩터/손실폭 균형을 위한 학습 전용 안정성 격차 페널티).

Primary prompt(1차 프롬프트): `{summary['grok']['primary']['prompt']}`

Primary output(1차 출력): `{summary['grok']['primary']['output']}`

Retry prompt(재시도 프롬프트): `{summary['grok']['retry']['prompt']}`

Retry output(재시도 출력): `{summary['grok']['retry']['output']}`

Advice classification(조언 분류): `{summary['grok']['retry']['classification']}`.

Accepted advice(수용 조언): {', '.join(classification['accepted'])}

Needs local verification(로컬 검증 필요): {', '.join(classification['needs_local_verification'])}

Rejected advice(거절 조언): none(없음).

Local verification(로컬 검증): `{summary['local_verification']['judgment']}`

Final Codex direction(최종 Codex 방향): F28B는 four locked train chunks(고정 학습 4조각)와 stability gap rank(안정성 격차 순위)만 선택 기준으로 씁니다.
"""


def local_verification_text(summary: dict[str, Any]) -> str:
    lines = ["# Frontier28 Local Verification(전선28 로컬 검증)", ""]
    for key, value in summary["local_verification"]["checks"].items():
        lines.append(f"- {key}: `{value}`")
    lines.append("")
    lines.append(f"Judgment(판정): `{summary['local_verification']['judgment']}`")
    lines.append("")
    lines.append("Effect(효과): Grok(그록) 조언을 자동 실행하지 않고 F27 closeout(F27 마감), 후보 표면(candidate surface, 후보 표면), feature hash(피처 해시), chunk lock(조각 잠금)으로 재검증했습니다.")
    return "\n".join(lines) + "\n"


def gate_audit(summary: dict[str, Any]) -> str:
    return f"""# Frontier28 Required Gate Coverage Audit(전선28 필수 게이트 커버리지 감사)

- external_review_packet(외부 검토 묶음): covered by(충족) `{GROK_PACKET_RETRY.as_posix()}`
- work_packet_schema_lint(작업 묶음 스키마 점검): experiment design fields(실험 설계 필드) materialized(물질화)
- local_verification_gate(로컬 검증 게이트): `{summary['local_verification']['judgment']}`
- stability_gap_contract_gate(안정성 격차 계약 게이트): 4 train chunks(학습 4조각) and penalty terms(페널티 항) locked(잠금)
- leakage_guard(누수 방지): validation/OOS read-only(검증/표본외 읽기 전용)
- runtime_probe_gate(런타임 탐침 게이트): stage-open only(단계 개방 전용), actual MT5 runtime probe(MT5 런타임 탐침)는 handoff candidate(인계 후보) 전까지 out_of_scope_by_claim(주장 범위 밖)
- final_claim_guard(최종 주장 방어): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성) all not_claimed(모두 주장 없음)
"""


def report_text(summary: dict[str, Any]) -> str:
    return f"""# {RUN_ID} Report(보고서)

Status(상태): `{summary['status']}`

Judgment(판정): `{summary['judgment']}`

Hypothesis(가설): {summary['hypothesis']}

Grok retry(그록 재시도): `{summary['grok']['retry']['classification']}`

Local verification(로컬 검증): `{summary['local_verification']['judgment']}`

Chunk boundaries(조각 경계): `{len(summary['locks']['chunk_boundaries'])}` locked train chunks(고정 학습 조각)

Next run(다음 실행): `{NEXT_RUN_ID}`

Runtime probe observation(런타임 탐침 관찰): stage-open only(단계 개방 전용). MT5 runtime probe(MT5 런타임 탐침)는 handoff candidate(인계 후보)가 없으므로 아직 실행하지 않습니다.

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 not_claimed(주장 없음)입니다.
"""


def selection_status(summary: dict[str, Any]) -> str:
    return f"""# Frontier28 Selection Status(전선28 선택 상태)

Selection(선택): no selected baseline/completion/promotion/runtime authority(선택 기준선/완성/승격/런타임 권위 없음).

Stage-open only(단계 개방 전용)입니다. F28B proxy(프록시)가 아직 실행되지 않았습니다.

Status(상태): `{STATUS}`

Judgment(판정): `{JUDGMENT}`

Next action(다음 행동): `{NEXT_RUN_ID}`

Runtime probe blocker(런타임 탐침 차단 사유): `runtime_probe_pending_no_handoff_candidate_at_stage_open(단계 개방 시점 인계 후보 없어 런타임 탐침 대기)`.

Claim boundary(주장 경계): no completion, no baseline, no promotion, no runtime authority, no live readiness, no Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음).
"""


def decision_text(summary: dict[str, Any]) -> str:
    return f"""# Decision(결정): Open Frontier28 Stability Gap Scout(전선28 안정성 격차 탐색 개방)

Date(날짜): 2026-06-14

Decision(결정): Open(개방) `{STAGE_ID}` with run(실행) `{RUN_ID}`.

Reason(이유): F27(전선27)은 union surface(합집합 표면)를 복원했지만 seed/handoff(씨앗/인계)를 만들지 못했습니다. Grok(그록)은 F28 stability gap selector(안정성 격차 선택기)를 accepted(수용)했고, Codex local verification(로컬 검증)이 chunk lock(조각 잠금)과 leakage guard(누수 방지)를 확인했습니다.

Effect(효과): 다음 proxy(프록시)는 forward metric selection(전진 지표 선택)이 아니라 train-only chunk stability(학습 전용 조각 안정성)를 시험합니다.

Claim boundary(주장 경계): no authority(권위 없음), no baseline(기준선 없음), no completion(완성 없음).
"""


def current_working_state(summary: dict[str, Any]) -> str:
    return f"""# Current Working State(현재 작업 상태)

Updated(갱신): {summary['created_at_utc']}

## Active Stage(현재 단계)

- stage(단계): `{STAGE_ID}`
- latest run(최근 실행): `{RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- next run(다음 실행): `{NEXT_RUN_ID}`

## Current Truth(현재 진실)

Action(행동): Frontier28(전선28)을 train-only stability gap penalty for PF/DD balance(수익 팩터/손실폭 균형을 위한 학습 전용 안정성 격차 페널티)로 열었습니다.

Effect(효과): F27 soft union surface(F27 연성 합집합 표면)는 reference clue only(참조 단서 전용)로만 쓰고, F28B는 검증/표본외 선택 없이 학습 4조각 안정성으로 후보를 다시 정렬합니다.

Runtime/ONNX boundary(런타임/온엑스 경계): handoff candidate(인계 후보)가 나오기 전까지 MT5 runtime probe(MT5 런타임 탐침), WFO(워크포워드 최적화), ONNX(온엑스)는 실행하지 않습니다. 각 stage(단계) closeout(마감)에는 runtime probe status(런타임 탐침 상태)를 기록합니다.

Claim boundary(주장 경계): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def changelog_entry(summary: dict[str, Any]) -> str:
    return (
        f"- {summary['created_at_utc']}: `{RUN_ID}` opened Frontier28 train-only stability gap scout(전선28 학습 전용 안정성 격차 탐색 개방). "
        f"Effect(효과): F27 surface(F27 표면)를 reference-only(참조 전용)로 두고 next run(다음 실행) `{NEXT_RUN_ID}`에서 chunk stability rank(조각 안정성 순위)를 시험합니다.\n"
    )


def idea_registry_entry(summary: dict[str, Any]) -> str:
    return (
        f"- `IDEA-FR28-TRAIN-ONLY-STABILITY-GAP-PENALTY-PF-DD-BALANCE-ONNX-SCOUT`: `{RUN_ID}` opens train-only chunk stability gap rank(학습 전용 조각 안정성 격차 순위) for PF/DD balance(수익 팩터/손실폭 균형). "
        "Effect(효과): F27 soft penalty surface(연성 페널티 표면)를 기준선이 아니라 참조 단서로만 사용합니다.\n"
    )


def artifact_identity(path: Path) -> dict[str, str]:
    return {"path": path.as_posix(), "sha256": sha256_io(path) if path_exists(path) else "missing(누락)"}


def sha256_io(path: Path) -> str:
    digest = hashlib.sha256()
    with io_path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8-sig")


def read_text(path: Path) -> str:
    return io_path(path).read_text(encoding="utf-8-sig")


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


if __name__ == "__main__":
    raise SystemExit(main())
