from __future__ import annotations

import csv
import hashlib
import json
import math
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
from stage_pipelines.stage_frontier_30 import frontier30d_stage_closeout as f30d


STAGE_ID = "stage_frontier_31__exit_shape_pivot_for_density_preserved_source_scout_pf_lift_onnx_scout"
RUN_ID = "frontier31A_stage_open_exit_shape_pivot_for_density_preserved_source_scout_pf_lift_hypothesis_design_v1"
RUN_NUMBER = "frontier31A"
PARENT_RUN_ID = f30d.RUN_ID
NEXT_RUN_ID = "frontier31B_return_space_exit_shape_proxy_scout_v1"
STATUS = "opened_frontier31_return_space_exit_shape_pivot_no_authority"
JUDGMENT = "stage_opened_after_grok_accepted_return_space_exit_shape_boundary"

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REPORT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_report.md"
GROK_RECEIPT_PATH = STAGE_ROOT / "03_reviews" / "grok_stage_open_receipt.md"
LOCAL_VERIFICATION_PATH = STAGE_ROOT / "03_reviews" / "local_verification.md"
SCRIPT_PATH = Path("stage_pipelines/stage_frontier_31/materialize_frontier31a_stage_open.py")
DECISION_PATH = Path("docs/decisions/2026-06-14_stage_frontier_31_return_space_exit_shape_open.md")

GROK_PACKET = Path("docs/agent_control/grok_reviews/2026-06-14_frontier31_stage_open/small_review")
F30_SELECTION = Path("stages") / f30d.STAGE_ID / "04_selected" / "selection_status.md"
F30D_SUMMARY = Path("stages") / f30d.STAGE_ID / "02_runs" / f30d.RUN_ID / "final_closeout_summary.json"
F30D_REPORT = Path("stages") / f30d.STAGE_ID / "03_reviews" / f"{f30d.RUN_ID}_report.md"
F30B_CANDIDATE_SUMMARY = Path("stages") / f30d.STAGE_ID / "02_runs" / f30d.f30b.RUN_ID / "density_preselector_candidate_summary.csv"

RUN_REGISTRY = Path("docs/registers/run_registry.csv")
ALPHA_LEDGER = Path("docs/registers/alpha_run_ledger.csv")
IDEA_REGISTRY = Path("docs/registers/idea_registry.md")
CHANGELOG = Path("docs/workspace/changelog.md")
WORKSPACE_STATE = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE = Path("docs/context/current_working_state.md")

FIXED_SCOUT_SOURCE_IDS = ("f28b_0002", "f28b_0086", "f28b_0054", "f28b_0080", "f28b_0079")
FIXED_SCOUT_CANDIDATE_IDS = ("f30b_0003", "f30b_0151", "f30b_0185", "f30b_0213", "f30b_0214")

LOCKS = {
    "selection_split": "train_only",
    "forward_splits": "validation_oos_read_only",
    "active_changed_variable": "train_only_return_space_exit_shape_transform_for_density_preserved_source_scouts",
    "fixed_entry_surface": "f30b_source_no_veto_scout_rows_only",
    "fixed_candidate_ids": list(FIXED_SCOUT_CANDIDATE_IDS),
    "fixed_source_ids": list(FIXED_SCOUT_SOURCE_IDS),
    "entry_mask_contract": {
        "source": F30B_CANDIDATE_SUMMARY.as_posix(),
        "required_branch": "source_no_veto_density_preservation_branch",
        "required_scout_clue_flag": True,
        "entry_masks_mutable": False,
        "source_scout_rerank_allowed": False,
    },
    "return_space_exit_shape_contract": {
        "data_basis": "future_log_return_12_proxy_only_no_intrabar_path",
        "parameter_source": "train_split_pnl_distribution_only",
        "validation_oos_role": "read_only_diagnostics",
        "transform_families": [
            "control_no_exit_transform",
            "loss_cap_train_loss_quantile",
            "asymmetric_clip_train_loss_and_win_quantiles",
        ],
        "loss_cap_quantiles": [0.45, 0.60, 0.75, 0.90],
        "take_cap_quantiles": [0.75, 0.90, 0.98],
        "minimum_stop_cap_log_return": 0.00025,
        "unrealistic_tight_clip_rule": "flag_if_stop_cap_le_train_loss_abs_q25_or_caps_more_than_55pct_of_train_losses",
        "no_post_hoc_edits": True,
        "all_variants_recorded": True,
    },
    "forbidden_primary_path": [
        "select_exit_params_by_validation_or_oos_pf_dd_density",
        "change_f30b_entry_masks_or_source_scout_identity",
        "rerank_fixed_scouts_by_forward_metrics",
        "claim_mt5_executable_behavior_from_return_space_clip_only",
        "inherit_f30_best_forward_candidate_as_baseline_or_handoff",
        "mt5_onnx_wfo_before_executable_exit_representation_and_pre_expensive_grok",
    ],
    "success_boundary": {
        "scout_clue": "return_space_proxy_validation_oos_positive_density_pf_dd_signal",
        "seed_surface": "return_space_proxy_forward_pf_ge_1_20_dd_le_18_density_5_to_10",
        "handoff_candidate": "return_space_proxy_pf_ge_1_50_dd_le_12_smoothness_pass_but_executable_representation_still_required",
        "not_completion": "final_goal_gates_not_applicable_until_final_completion_review",
    },
    "runtime_probe_rule": "record runtime probe status every stage; execute MT5 only after executable exit representation, handoff candidate, and pre-expensive Grok",
    "tier_pair_boundary": "Tier B and Tier A+B are missing_required until explicitly materialized in this frontier",
}


def main() -> int:
    ensure_dirs()
    normalize_grok_markdown()
    created_at = utc_now()
    frame = f23b.load_frame()
    feature_order = f23b.read_feature_order()
    f30d_summary = read_json(F30D_SUMMARY)
    f30_candidates = pd.read_csv(io_path(F30B_CANDIDATE_SUMMARY))
    grok = read_grok_packet(GROK_PACKET)
    local = local_verification(frame, feature_order, f30d_summary, f30_candidates, grok)
    if local["judgment"] != "pass_open_ready_with_return_space_exit_shape_locks":
        raise RuntimeError(f"Frontier31A local verification failed: {json.dumps(local, ensure_ascii=False)}")
    summary = build_summary(created_at, frame, feature_order, f30d_summary, f30_candidates, grok, local)
    write_outputs(summary)
    update_registries(summary)
    update_current_truth(summary)
    print(json.dumps(json_ready({
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "grok_classification": grok["classification"],
        "fixed_scout_rows": summary["fixed_scout_rows"],
        "runtime_probe_status": summary["runtime_probe_status"],
        "next_run_id": NEXT_RUN_ID,
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
    for name in ("input_prompt.md", "prompt.md", "clean_output.md"):
        path = GROK_PACKET / name
        if path_exists(path):
            text = io_path(path).read_text(encoding="utf-8-sig")
            f03b.write_text_sig(path, text.rstrip() + "\n")


def read_grok_packet(packet: Path) -> dict[str, Any]:
    metadata = read_json(packet / "metadata.json")
    output = read_text(packet / "clean_output.md")
    lowered = output.lower()
    accepted = (
        "verdict:** accepted" in lowered or "verdict: accepted" in lowered
    ) and (
        "novelty_ok:** yes" in lowered or "novelty_ok: yes" in lowered
    ) and (
        "leakage_risk:** low" in lowered or "leakage_risk: low" in lowered
    ) and (
        "frontier_boundary_ok:** yes" in lowered or "frontier_boundary_ok: yes" in lowered
    ) and (
        "hypothesis_scope_ok:** yes" in lowered or "hypothesis_scope_ok: yes" in lowered
    ) and (
        "runtime_claim_boundary_ok:** yes" in lowered or "runtime_claim_boundary_ok: yes" in lowered
    )
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
        "preflight_warnings": metadata.get("preflight_warnings", []),
        "classification": "accepted_return_space_exit_shape_boundary_low_leakage" if accepted else "needs_local_verification",
        "accepted": accepted,
        "output_excerpt": output[:3600],
    }


def local_verification(
    frame: pd.DataFrame,
    feature_order: list[str],
    f30d_summary: dict[str, Any],
    f30_candidates: pd.DataFrame,
    grok: dict[str, Any],
) -> dict[str, Any]:
    workspace = read_text(WORKSPACE_STATE)
    f30_selection = read_text(F30_SELECTION)
    f30_report = read_text(F30D_REPORT)
    scout_rows = fixed_scout_rows(f30_candidates)
    intrabar_like = {"open", "high", "low", "close", "mfe", "mae"}
    lower_columns = {column.lower() for column in frame.columns}
    split_counts = frame["split"].astype(str).value_counts().to_dict()
    checks = {
        "workspace_current_f30d_or_f31a": (
            f"current_stage_id: {f30d.STAGE_ID}" in workspace
            and f"current_run_id: {f30d.RUN_ID}" in workspace
        ) or (
            f"current_stage_id: {STAGE_ID}" in workspace
            and f"current_run_id: {RUN_ID}" in workspace
        ),
        "workspace_next_frontier31a_or_frontier31b": f"next_run_id: {RUN_ID}" in workspace
        or f"next_run_id: {NEXT_RUN_ID}" in workspace,
        "f30d_next_stage_matches": f30d_summary.get("next_stage_id") == STAGE_ID
        and f30d_summary.get("next_run_id") == RUN_ID,
        "f30_selection_next_action_matches": RUN_ID in f30_selection,
        "f30_closeout_report_mentions_exit_shape_next_clue": "exit_shape_pivot_for_density_preserved_source_scout_pf_lift" in f30_report,
        "f30_scout_seed_handoff_counts": int(f30d_summary["f30b_summary"]["scout_clue_rows"]) == 5
        and int(f30d_summary["f30b_summary"]["seed_surface_rows"]) == 0
        and int(f30d_summary["f30b_summary"]["handoff_candidate_rows"]) == 0,
        "fixed_scout_rows_five": len(scout_rows) == 5,
        "fixed_scout_ids_match": tuple(scout_rows["candidate_id"].astype(str).tolist()) == FIXED_SCOUT_CANDIDATE_IDS,
        "fixed_scout_branch_source_no_veto": scout_rows["branch"].astype(str).eq("source_no_veto_density_preservation_branch").all(),
        "fixed_scout_forward_readonly_not_seed": not scout_rows["seed_surface_flag"].astype(bool).any()
        and not scout_rows["handoff_candidate_flag"].astype(bool).any(),
        "dataset_has_future_log_return_12": "future_log_return_12" in frame.columns,
        "dataset_no_intrabar_path_columns": not bool(intrabar_like & lower_columns),
        "feature_hash_matches_contract": ordered_hash(feature_order) == f23b.EXPECTED_FEATURE_HASH,
        "dataset_has_required_splits": all(split in split_counts for split in ("train", "validation", "oos")),
        "grok_transport_success": grok["success"] and grok["returncode"] == 0 and not grok["timed_out"],
        "grok_accepted_low_leakage": grok["accepted"] and grok["classification"].startswith("accepted"),
        "grok_no_unexpected_top_level_artifacts": not grok["unexpected_top_level_artifacts"],
        "lock_active_changed_variable_exit_shape": LOCKS["active_changed_variable"]
        == "train_only_return_space_exit_shape_transform_for_density_preserved_source_scouts",
        "lock_blocks_forward_selection": "select_exit_params_by_validation_or_oos_pf_dd_density" in json.dumps(LOCKS),
        "lock_blocks_runtime_claim_from_clip": "claim_mt5_executable_behavior_from_return_space_clip_only" in json.dumps(LOCKS),
    }
    return {
        "checks": checks,
        "judgment": "pass_open_ready_with_return_space_exit_shape_locks" if all(checks.values()) else "needs_manual_review",
        "fixed_scout_candidate_ids": scout_rows["candidate_id"].astype(str).tolist(),
        "fixed_scout_source_ids": scout_rows["source_stability_union_id"].astype(str).tolist(),
        "data_limitation": "future_log_return_12_only_no_intrabar_high_low_mfe_mae",
    }


def fixed_scout_rows(f30_candidates: pd.DataFrame) -> pd.DataFrame:
    rows = f30_candidates.loc[
        f30_candidates["scout_clue_flag"].astype(bool)
        & f30_candidates["branch"].astype(str).eq("source_no_veto_density_preservation_branch")
    ].copy()
    return rows.sort_values("candidate_id").reset_index(drop=True)


def build_summary(
    created_at: str,
    frame: pd.DataFrame,
    feature_order: list[str],
    f30d_summary: dict[str, Any],
    f30_candidates: pd.DataFrame,
    grok: dict[str, Any],
    local: dict[str, Any],
) -> dict[str, Any]:
    scout_rows = fixed_scout_rows(f30_candidates)
    return {
        "created_at_utc": created_at,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "frontier_thesis": "return_space_exit_shape_can_lift_pf_for_density_preserved_source_scouts_without_entry_change",
        "novelty_delta": "F31 activates exit_shape_pivot after F30 kept it reference-only; entry masks remain fixed.",
        "fixed_scout_rows": int(len(scout_rows)),
        "fixed_scout_candidate_ids": scout_rows["candidate_id"].astype(str).tolist(),
        "fixed_scout_source_ids": scout_rows["source_stability_union_id"].astype(str).tolist(),
        "fixed_scout_micro_ids": scout_rows["micro_ids"].astype(str).tolist(),
        "dataset_rows": int(len(frame)),
        "split_counts": {key: int(value) for key, value in frame["split"].astype(str).value_counts().to_dict().items()},
        "feature_count": int(len(feature_order)),
        "feature_order_hash": ordered_hash(feature_order),
        "locks": LOCKS,
        "grok": grok,
        "local_verification": local,
        "prior_stage_scan": {
            "f30_status": f30d_summary.get("status"),
            "f30_judgment": f30d_summary.get("judgment"),
            "preserved_clue": f30d_summary.get("preserved_clue"),
            "negative_memory": f30d_summary.get("negative_memory"),
            "next_hypothesis_clue": f30d_summary.get("next_hypothesis_clue"),
        },
        "runtime_probe_status": "runtime_probe_out_of_scope_by_claim_stage_open_no_handoff_candidate",
        "result_boundary": "stage_open_no_model_training_no_wfo_no_mt5_no_onnx_no_authority",
        "claim_boundary": {claim: "not_claimed" for claim in f03b.FORBIDDEN_CLAIMS},
    }


def write_outputs(summary: dict[str, Any]) -> None:
    write_json(RUN_ROOT / "stage_open_summary.json", summary)
    write_json(RUN_ROOT / "run_manifest.json", run_manifest(summary))
    write_json(RUN_ROOT / "return_space_exit_shape_lock.json", LOCKS)
    f03b.write_text_sig(STAGE_ROOT / "00_spec" / "stage_brief.md", stage_brief(summary))
    f03b.write_text_sig(STAGE_ROOT / "01_inputs" / "fixed_f30_source_scout_surface.md", fixed_surface_text(summary))
    f03b.write_text_sig(REPORT_PATH, report_text(summary))
    f03b.write_text_sig(GROK_RECEIPT_PATH, grok_receipt(summary))
    f03b.write_text_sig(LOCAL_VERIFICATION_PATH, local_verification_text(summary))
    f03b.write_text_sig(STAGE_ROOT / "04_selected" / "selection_status.md", selection_status(summary))
    f03b.write_text_sig(DECISION_PATH, decision_text(summary))


def run_manifest(summary: dict[str, Any]) -> dict[str, Any]:
    artifacts = [
        SCRIPT_PATH,
        GROK_PACKET / "prompt.md",
        GROK_PACKET / "clean_output.md",
        GROK_PACKET / "metadata.json",
        F30D_SUMMARY,
        F30B_CANDIDATE_SUMMARY,
        f23b.DATASET_PATH,
        f23b.FEATURE_ORDER_PATH,
        RUN_ROOT / "stage_open_summary.json",
        RUN_ROOT / "return_space_exit_shape_lock.json",
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
        "selection_boundary": "train_only_exit_shape_parameterization_validation_oos_read_only",
        "claim_boundary": summary["claim_boundary"],
    }


def update_registries(summary: dict[str, Any]) -> None:
    f03b.upsert_csv(RUN_REGISTRY, "run_id", run_registry_row(summary))
    for row in ledger_rows(summary):
        f03b.upsert_csv(ALPHA_LEDGER, "ledger_row_id", row)
        upsert_csv_io(STAGE_ROOT / "03_reviews" / "stage_run_ledger.csv", "ledger_row_id", row)
    f03b.append_once(CHANGELOG, RUN_ID, changelog_entry(summary))
    f03b.append_once(IDEA_REGISTRY, RUN_ID, idea_registry_entry(summary))


def run_registry_row(summary: dict[str, Any]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "stage_open(단계 개방)",
        "family": "experiment_design(실험 설계)",
        "work_family": "experiment_design(실험 설계)",
        "status": summary["status"],
        "judgment": summary["judgment"],
        "path": REPORT_PATH.as_posix(),
        "notes": f"fixed_scout_rows={summary['fixed_scout_rows']};next={NEXT_RUN_ID};no_authority",
        "run_number": RUN_NUMBER,
        "date": "2026-06-14",
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "claim_boundary": summary["result_boundary"],
        "report_path": REPORT_PATH.as_posix(),
        "created_at_utc": summary["created_at_utc"],
        "primary_kpi": f"fixed_scout_rows={summary['fixed_scout_rows']};dataset_rows={summary['dataset_rows']}",
        "guardrail_kpi": "return_space_proxy_only_no_mt5_no_onnx_no_authority",
        "external_verification_status": summary["runtime_probe_status"],
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "result_path": REPORT_PATH.as_posix(),
    }


def ledger_rows(summary: dict[str, Any]) -> list[dict[str, Any]]:
    return [{
        "ledger_row_id": f"{RUN_ID}__stage_open",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": f"{RUN_ID}__stage_open",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "stage_open(단계 개방)",
        "tier_scope": "not_applicable_stage_open(단계 개방에는 해당 없음)",
        "kpi_scope": "planning_only_no_trading_kpi(계획 전용, 거래 KPI 없음)",
        "scoreboard_lane": "stage_open(단계 개방)",
        "status": summary["status"],
        "judgment": summary["judgment"],
        "path": REPORT_PATH.as_posix(),
        "primary_kpi": f"grok={summary['grok']['classification']};fixed_scout_rows={summary['fixed_scout_rows']}",
        "guardrail_kpi": "return_space_exit_shape_lock_no_model_training_no_wfo_no_mt5_no_authority",
        "external_verification_status": summary["runtime_probe_status"],
        "notes": f"next={NEXT_RUN_ID};changed_variable={LOCKS['active_changed_variable']};no_authority",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "run_family": "stage_open(단계 개방)",
    }]


def update_current_truth(summary: dict[str, Any]) -> None:
    io_path(WORKSPACE_STATE).write_text(workspace_state(summary), encoding="utf-8-sig")
    f03b.write_text_sig(CURRENT_WORKING_STATE, current_working_state(summary))


def workspace_state(summary: dict[str, Any]) -> str:
    return "\n".join([
        f"current_stage_id: {STAGE_ID}",
        f"current_run_id: {RUN_ID}",
        f"latest_completed_run_id: {RUN_ID}",
        f"current_status: {summary['status']}",
        f"current_judgment: {summary['judgment']}",
        f"next_run_id: {NEXT_RUN_ID}",
        "runtime_authority: not_claimed",
        "operating_promotion: not_claimed",
        "goal_achieve: not_claimed",
        f"updated_at_utc: '{summary['created_at_utc']}'",
        "",
    ])


def stage_brief(summary: dict[str, Any]) -> str:
    return f"""# Frontier31 Stage Brief(전선31 단계 요약)

Opened(개방): {summary['created_at_utc']}

Frontier thesis(전선 가설): F30(전선30)이 회복한 density-preserved source scouts(밀도 보존 원천 탐색) 5개는 진입 표면(entry surface, 진입 표면)은 유지하고, return-space exit-shape transform(수익률 공간 청산 형태 변환)만 바꾸면 PF lift(PF 상승)와 DD reduction(손실폭 감소)이 가능한지 시험합니다.

Hypothesis(가설): train-only(학습 전용)으로 고른 loss cap/asymmetric clip(손실 상한/비대칭 클립) 변환이 validation/OOS(검증/표본외)에서 read-only(읽기 전용)으로 seed surface(씨앗 표면)나 handoff candidate(인계 후보) 단서를 만들 수 있습니다.

Novelty delta(신규성 차이): F31(전선31)은 F30(전선30)에서 reference fallback only(참조 대체 전용)였던 exit-shape pivot(청산 형태 전환)을 단일 active changed variable(활성 변경 변수)로 격상합니다.

Fixed surface(고정 표면): `{', '.join(summary['fixed_scout_candidate_ids'])}`.

Data limitation(데이터 한계): `future_log_return_12` only(12봉 미래 로그수익률만 있음), no intrabar high/low/MFE/MAE(봉내 고가/저가/최대유리/최대불리 없음).

Runtime probe rule(런타임 탐침 규칙): 각 stage(단계)마다 runtime probe status(런타임 탐침 상태)를 기록합니다. 실제 MT5 runtime probe(MT5 런타임 탐침)는 executable exit representation(실행 가능한 청산 표현), handoff candidate(인계 후보), pre-expensive Grok review(비싼 실행 전 그록 검토)가 모두 있을 때만 실행합니다.
"""


def fixed_surface_text(summary: dict[str, Any]) -> str:
    lines = [
        "# Frontier31 Fixed F30 Source Scout Surface(전선31 고정 F30 원천 탐색 표면)",
        "",
        "Action(행동): F30B(전선30B)의 source no-veto scout rows(원천 무차단 탐색 행) 5개만 고정 입력으로 사용합니다.",
        "",
        "Effect(효과): F31B(전선31B)는 entry mask(진입 마스크)를 바꾸지 않고 exit-shape transform(청산 형태 변환)만 시험합니다.",
        "",
    ]
    for candidate_id, source_id, micro_ids in zip(
        summary["fixed_scout_candidate_ids"], summary["fixed_scout_source_ids"], summary["fixed_scout_micro_ids"]
    ):
        lines.append(f"- `{candidate_id}` from `{source_id}` micro_ids(마이크로 ID): `{micro_ids}`")
    return "\n".join(lines) + "\n"


def report_text(summary: dict[str, Any]) -> str:
    return f"""# Frontier31A Stage Open Report(전선31A 단계 개방 보고서)

Updated(갱신): {summary['created_at_utc']}

Status(상태): `{summary['status']}`

Judgment(판정): `{summary['judgment']}`

Action(행동): F31(전선31)을 return-space exit-shape pivot(수익률 공간 청산 형태 전환) stage(단계)로 열었습니다.

Effect(효과): F30B(전선30B)의 source no-veto scout(원천 무차단 탐색) 5개를 고정하고, F31B(전선31B)는 train-only(학습 전용) exit parameter(청산 파라미터)만 시험합니다.

Grok classification(그록 분류): `{summary['grok']['classification']}`

Fixed scout rows(고정 탐색 행): `{summary['fixed_scout_rows']}`

Data limitation(데이터 한계): `{summary['local_verification']['data_limitation']}`

Runtime probe status(런타임 탐침 상태): `{summary['runtime_probe_status']}`

Next action(다음 행동): `{NEXT_RUN_ID}`

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def grok_receipt(summary: dict[str, Any]) -> str:
    grok = summary["grok"]
    return f"""# Frontier31A Grok Stage-Open Receipt(전선31A 그록 단계 개방 영수증)

Trigger reason(트리거 이유): goal(목표)이 Grok second opinion(그록 2차 의견)을 stage open(단계 개방)에 요구합니다.

Review size(검토 크기): small review(소규모 검토)

Direction before Grok(그록 전 방향): F30(전선30) exit-shape reference fallback(청산 형태 참조 대체)을 F31(전선31)의 단일 active changed variable(활성 변경 변수)로 격상합니다.

Prompt(프롬프트): `{grok['prompt']}`

Output(출력): `{grok['output']}`

Metadata(메타데이터): `{grok['metadata']}`

Classification(분류): `{grok['classification']}`

Accepted advice(수용 조언): return-space proxy(수익률 공간 프록시)는 탐색으로 유효하지만 MT5 executability(MT5 실행 가능성)는 주장하지 않습니다.

Rejected advice(거절 조언): validation/OOS(검증/표본외)로 stop/take(손절/익절)를 고르거나 clipping(클리핑)만으로 runtime authority(런타임 권위)를 주장하는 경로입니다.

Needs local verification(로컬 검증 필요): fixed scout identity(고정 탐색 정체성), transform family(변환군), train-only audit trail(학습 전용 감사 추적).

Local verification(로컬 검증): `{summary['local_verification']['judgment']}`
"""


def local_verification_text(summary: dict[str, Any]) -> str:
    rows = [f"- {key}: `{value}`" for key, value in summary["local_verification"]["checks"].items()]
    return f"""# Frontier31A Local Verification(전선31A 로컬 검증)

Judgment(판정): `{summary['local_verification']['judgment']}`

{chr(10).join(rows)}

Effect(효과): Grok(그록) 조언을 자동 실행하지 않고, F30(전선30) closeout(마감), candidate summary(후보 요약), dataset contract(데이터셋 계약)과 대조한 뒤 stage-open(단계 개방)을 물질화했습니다.
"""


def selection_status(summary: dict[str, Any]) -> str:
    return f"""# Frontier31 Selection Status(전선31 선택 상태)

Updated(갱신): {summary['created_at_utc']}

Selection(선택): no selected baseline/completion/promotion/runtime authority(선택 기준선/완성/승격/런타임 권위 없음).

Latest run(최근 실행): `{RUN_ID}`

Status(상태): `{summary['status']}`

Judgment(판정): `{summary['judgment']}`

Fixed scout rows(고정 탐색 행): `{summary['fixed_scout_rows']}`

Runtime probe status(런타임 탐침 상태): `{summary['runtime_probe_status']}`

Next action(다음 행동): `{NEXT_RUN_ID}`

Claim boundary(주장 경계): no completion, no baseline, no promotion, no runtime authority, no live readiness, no Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음).
"""


def decision_text(summary: dict[str, Any]) -> str:
    return f"""# Decision: Open Frontier31 Return-Space Exit Shape(결정: 전선31 수익률 공간 청산 형태 개방)

Date(날짜): 2026-06-14

Decision(결정): Open(개방) `{STAGE_ID}` with run(실행) `{RUN_ID}`.

Rationale(근거): F30(전선30)은 source scout(원천 탐색) 5개를 회복했지만 seed/handoff(씨앗/인계)가 없었습니다. F31(전선31)은 entry(진입)를 고정하고 exit shape(청산 형태)만 시험합니다.

Effect(효과): 다음 run(실행) `{NEXT_RUN_ID}`는 train-only return-space proxy(학습 전용 수익률 공간 프록시)만 수행하며, MT5/ONNX/WFO(MT5/온엑스/워크포워드 최적화)는 아직 실행하지 않습니다.
"""


def current_working_state(summary: dict[str, Any]) -> str:
    return f"""# Current Working State(현재 작업 상태)

Updated(갱신): {summary['created_at_utc']}

## Active Stage(현재 단계)

- stage(단계): `{STAGE_ID}`
- latest run(최근 실행): `{RUN_ID}`
- status(상태): `{summary['status']}`
- judgment(판정): `{summary['judgment']}`
- next run(다음 실행): `{NEXT_RUN_ID}`

## Current Truth(현재 진실)

Action(행동): F31(전선31)을 return-space exit-shape pivot(수익률 공간 청산 형태 전환) stage(단계)로 열었습니다.

Effect(효과): F30B(전선30B)의 고정 scout rows(탐색 행) `{summary['fixed_scout_rows']}`개를 대상으로, entry mask(진입 마스크)는 고정하고 exit transform(청산 변환)만 학습 구간에서 고릅니다.

Runtime probe boundary(런타임 탐침 경계): `{summary['runtime_probe_status']}`

Claim boundary(주장 경계): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def changelog_entry(summary: dict[str, Any]) -> str:
    return (
        f"- {summary['created_at_utc']}: `{RUN_ID}` opened Frontier31 return-space exit-shape pivot(전선31 수익률 공간 청산 형태 전환). "
        f"Effect(효과): fixed_scout_rows={summary['fixed_scout_rows']}, next=`{NEXT_RUN_ID}`, no authority(권위 없음).\n"
    )


def idea_registry_entry(summary: dict[str, Any]) -> str:
    return (
        f"- `IDEA-FR31-RETURN-SPACE-EXIT-SHAPE-PF-LIFT-ONNX-SCOUT`: `{RUN_ID}` opened a train-only return-space exit-shape transform(학습 전용 수익률 공간 청산 형태 변환) against F30 fixed scouts(전선30 고정 탐색). "
        "Effect(효과): proxy-only(프록시 전용) exploration begins without MT5/ONNX authority(MT5/온엑스 권위 없음).\n"
    )


def artifact_identity(path: Path) -> dict[str, str]:
    return {"path": path.as_posix(), "sha256": sha256_io(path) if path_exists(path) else "missing"}


def sha256_io(path: Path) -> str:
    digest = hashlib.sha256()
    with io_path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def read_text(path: Path) -> str:
    return io_path(path).read_text(encoding="utf-8-sig")


def upsert_csv_io(path: Path, key: str, row: dict[str, Any]) -> None:
    header: list[str]
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        header = next(csv.reader(handle))
        rows = list(csv.DictReader(handle, fieldnames=header))
    normalized = {column: f03b.stringify(row.get(column, "")) for column in header}
    replaced = False
    for index, existing in enumerate(rows):
        if existing.get(key) == normalized.get(key):
            rows[index] = normalized
            replaced = True
            break
    if not replaced:
        rows.append(normalized)
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=header, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for item in rows:
            writer.writerow({column: f03b.stringify(item.get(column, "")) for column in header})


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def fmt(value: Any) -> str:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return "NA"
    if not math.isfinite(number):
        return "NA"
    return f"{number:.3f}"


if __name__ == "__main__":
    raise SystemExit(main())
