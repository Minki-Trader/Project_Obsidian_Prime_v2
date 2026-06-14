from __future__ import annotations

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
from stage_pipelines.stage_frontier_03 import frontier03b_regime_asymmetric_label_proxy_scout as f03b
from stage_pipelines.stage_frontier_30 import frontier30b_train_density_preserving_preselector_before_loss_veto_proxy_scout as f30b


STAGE_ID = f30b.STAGE_ID
RUN_ID = "frontier30C_density_preserving_preselector_repair_or_closeout_decision_v1"
RUN_NUMBER = "frontier30C"
PARENT_RUN_ID = f30b.RUN_ID
NEXT_RUN_ID = "frontier30D_stage_closeout_density_preserving_preselector_v1"
STATUS = "density_preserving_preselector_repair_rejected_scout_only_no_seed_no_handoff_no_authority"
JUDGMENT = "repair_rejected_frozen_contract_no_valid_train_only_pf_lift_opportunity"

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REPORT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_report.md"
GATE_AUDIT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_gate_audit.md"
SCRIPT_PATH = Path("stage_pipelines/stage_frontier_30/frontier30c_density_preserving_preselector_repair_or_closeout_decision.py")

F30B_SUMMARY = STAGE_ROOT / "02_runs" / f30b.RUN_ID / "final_summary.json"
F30B_CANDIDATE_SUMMARY = STAGE_ROOT / "02_runs" / f30b.RUN_ID / "density_preselector_candidate_summary.csv"
F30B_SOURCE_LEDGER = STAGE_ROOT / "02_runs" / f30b.RUN_ID / "train_density_preselector_source_ledger.csv"

RUN_REGISTRY = Path("docs/registers/run_registry.csv")
ALPHA_LEDGER = Path("docs/registers/alpha_run_ledger.csv")
IDEA_REGISTRY = Path("docs/registers/idea_registry.md")
CHANGELOG = Path("docs/workspace/changelog.md")
WORKSPACE_STATE = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE = Path("docs/context/current_working_state.md")

PRESERVED_CLUE = (
    "f30_density_preselector_recovered_five_train_selected_source_scouts_but_no_seed_handoff_reference_only"
    "(전선30 밀도 사전 선택기는 학습 선택 원천 탐색 5개를 회복했지만 씨앗/인계가 없어 참조 전용 보존)"
)
NEGATIVE_MEMORY = (
    "under_f30_locked_density_preselector_veto_branch_scout_zero_and_pf_lift_missing"
    "(전선30 잠금 밀도 사전 선택기 아래 차단 분기 탐색은 0개이고 수익 팩터 상승이 부족함)"
)
NEXT_HYPOTHESIS_CLUE = (
    "exit_shape_pivot_for_density_preserved_source_scout_pf_lift_reference_only"
    "(밀도 보존 원천 탐색의 수익 팩터 상승을 위한 청산 형태 전환을 참조 전용 다음 단서로 보존)"
)


def main() -> int:
    ensure_dirs()
    created_at = utc_now()
    f30b_summary = read_json(F30B_SUMMARY)
    candidates = pd.read_csv(io_path(F30B_CANDIDATE_SUMMARY))
    source_ledger = pd.read_csv(io_path(F30B_SOURCE_LEDGER))
    audit = build_repair_audit(candidates)
    final = build_final(created_at, f30b_summary, candidates, source_ledger, audit)
    write_outputs(final, audit)
    update_registries(final)
    update_current_truth(final)
    print(json.dumps(json_ready({
        "status": final["status"],
        "judgment": final["judgment"],
        "run_id": RUN_ID,
        "scout_clue_rows": final["diagnosis"]["scout_clue_rows"],
        "seed_surface_rows": final["diagnosis"]["seed_surface_rows"],
        "handoff_candidate_rows": final["diagnosis"]["handoff_candidate_rows"],
        "valid_train_density_repair_opportunity_rows": final["diagnosis"]["valid_train_density_repair_opportunity_rows"],
        "next_run_id": final["next_run_id"],
        "report": REPORT_PATH.as_posix(),
    }), ensure_ascii=False, indent=2))
    return 0


def ensure_dirs() -> None:
    for path in (RUN_ROOT, STAGE_ROOT / "03_reviews", STAGE_ROOT / "04_selected"):
        io_path(path).mkdir(parents=True, exist_ok=True)


def build_repair_audit(candidates: pd.DataFrame) -> pd.DataFrame:
    rows = candidates.copy()
    rows["density_bridge"] = rows["density_bridge_flag"].astype(bool)
    rows["dual_positive"] = (rows["validation_net_profit"] > 0) & (rows["oos_net_profit"] > 0)
    rows["scout"] = rows["scout_clue_flag"].astype(bool)
    rows["seed"] = rows["seed_surface_flag"].astype(bool)
    rows["handoff"] = rows["handoff_candidate_flag"].astype(bool)
    rows["near_seed_pf_band"] = rows["density_bridge"] & rows["dual_positive"] & (rows["forward_min_pf"] >= 1.15) & (rows["forward_max_dd"] <= 22.0)
    rows["scout_pf_blocked_seed"] = rows["scout"] & (rows["forward_min_pf"] < 1.20)
    rows["scout_dd_blocked_seed"] = rows["scout"] & (rows["forward_max_dd"] > 18.0)
    rows["source_branch_scout_only"] = rows["scout"] & rows["branch"].astype(str).eq("source_no_veto_density_preservation_branch")
    rows["veto_branch_scout"] = rows["scout"] & rows["branch"].astype(str).eq("top_density_preserving_loss_veto_variant_per_source")
    rows["would_require_exit_shape_pivot"] = rows["scout_pf_blocked_seed"] | rows["near_seed_pf_band"]
    rows["would_require_posthoc_contract_edit"] = rows["would_require_exit_shape_pivot"] | rows["source_branch_scout_only"]
    rows["valid_train_density_repair_opportunity"] = False
    rows["repair_rejection_reason"] = rows.apply(repair_rejection_reason, axis=1)
    keep = [
        "candidate_id",
        "branch",
        "source_stability_union_id",
        "preselector_rank",
        "train_only_preselector_score",
        "forward_min_pf",
        "forward_max_dd",
        "forward_min_density",
        "density_bridge",
        "dual_positive",
        "scout",
        "seed",
        "handoff",
        "near_seed_pf_band",
        "scout_pf_blocked_seed",
        "scout_dd_blocked_seed",
        "source_branch_scout_only",
        "veto_branch_scout",
        "would_require_exit_shape_pivot",
        "would_require_posthoc_contract_edit",
        "valid_train_density_repair_opportunity",
        "repair_rejection_reason",
    ]
    return rows[keep]


def repair_rejection_reason(row: pd.Series) -> str:
    if bool(row.get("seed", False)) or bool(row.get("handoff", False)):
        return "not_rejected_seed_or_handoff_present"
    if bool(row.get("scout_pf_blocked_seed", False)):
        return "scout_pf_below_seed_floor_requires_new_exit_shape_or_payoff_lift"
    if bool(row.get("source_branch_scout_only", False)):
        return "scout_exists_only_on_no_veto_source_branch_not_density_veto_branch"
    if bool(row.get("near_seed_pf_band", False)):
        return "near_seed_pf_band_requires_new_changed_variable_not_f30_threshold_edit"
    return "no_locked_train_density_repair_path"


def build_final(
    created_at: str,
    f30b_summary: dict[str, Any],
    candidates: pd.DataFrame,
    source_ledger: pd.DataFrame,
    audit: pd.DataFrame,
) -> dict[str, Any]:
    diagnosis = {
        "candidate_rows": int(len(candidates)),
        "source_rows": int(len(source_ledger)),
        "preselected_source_rows": int(source_ledger["preselector_selected_flag"].astype(bool).sum()),
        "density_bridge_rows": int(audit["density_bridge"].sum()),
        "dual_positive_rows": int(audit["dual_positive"].sum()),
        "scout_clue_rows": int(audit["scout"].sum()),
        "seed_surface_rows": int(audit["seed"].sum()),
        "handoff_candidate_rows": int(audit["handoff"].sum()),
        "near_seed_pf_band_rows": int(audit["near_seed_pf_band"].sum()),
        "scout_pf_blocked_seed_rows": int(audit["scout_pf_blocked_seed"].sum()),
        "scout_dd_blocked_seed_rows": int(audit["scout_dd_blocked_seed"].sum()),
        "source_branch_scout_only_rows": int(audit["source_branch_scout_only"].sum()),
        "veto_branch_scout_rows": int(audit["veto_branch_scout"].sum()),
        "would_require_exit_shape_pivot_rows": int(audit["would_require_exit_shape_pivot"].sum()),
        "would_require_posthoc_contract_edit_rows": int(audit["would_require_posthoc_contract_edit"].sum()),
        "valid_train_density_repair_opportunity_rows": int(audit["valid_train_density_repair_opportunity"].sum()),
    }
    if diagnosis["valid_train_density_repair_opportunity_rows"] != 0:
        raise RuntimeError(f"Unexpected F30 repair opportunity: {diagnosis}")
    return {
        "created_at_utc": created_at,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "repair_decision": "reject_repair_and_closeout",
        "preserved_clue": PRESERVED_CLUE,
        "negative_memory": NEGATIVE_MEMORY,
        "next_hypothesis_clue": NEXT_HYPOTHESIS_CLUE,
        "diagnosis": diagnosis,
        "f30b_summary": {
            "status": f30b_summary.get("status"),
            "judgment": f30b_summary.get("judgment"),
            "source_branch_scout_rows": f30b_summary.get("source_branch_scout_rows"),
            "veto_branch_scout_rows": f30b_summary.get("veto_branch_scout_rows"),
            "scout_clue_rows": f30b_summary.get("scout_clue_rows"),
            "seed_surface_rows": f30b_summary.get("seed_surface_rows"),
            "handoff_candidate_rows": f30b_summary.get("handoff_candidate_rows"),
            "runtime_probe_status": f30b_summary.get("runtime_probe_status"),
        },
        "runtime_probe_status": "runtime_probe_out_of_scope_by_claim_scout_only_no_handoff",
        "onnx_status": "onnx_branch_unattempted_no_handoff_candidate_after_f30c_repair_decision",
        "claim_boundary": {claim: "not_claimed" for claim in f03b.FORBIDDEN_CLAIMS},
        "result_boundary": "repair_decision_no_wfo_no_mt5_no_onnx_no_authority",
    }


def write_outputs(final: dict[str, Any], audit: pd.DataFrame) -> None:
    audit.to_csv(io_path(RUN_ROOT / "repair_rejection_audit.csv"), index=False, encoding="utf-8-sig")
    write_json(RUN_ROOT / "final_summary.json", final)
    write_json(RUN_ROOT / "run_manifest.json", run_manifest(final))
    f03b.write_text_sig(REPORT_PATH, report_text(final))
    f03b.write_text_sig(GATE_AUDIT_PATH, gate_audit(final))
    f03b.write_text_sig(STAGE_ROOT / "04_selected" / "selection_status.md", selection_status(final))


def run_manifest(final: dict[str, Any]) -> dict[str, Any]:
    artifacts = [
        SCRIPT_PATH,
        F30B_SUMMARY,
        F30B_CANDIDATE_SUMMARY,
        F30B_SOURCE_LEDGER,
        RUN_ROOT / "repair_rejection_audit.csv",
        RUN_ROOT / "final_summary.json",
        REPORT_PATH,
    ]
    return {
        "identity": {
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "parent_run_id": PARENT_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "created_at_utc": final["created_at_utc"],
        },
        "artifacts": [artifact_identity(path) for path in artifacts],
        "repair_decision": final["repair_decision"],
        "claim_boundary": final["claim_boundary"],
    }


def update_registries(final: dict[str, Any]) -> None:
    f03b.upsert_csv(RUN_REGISTRY, "run_id", run_registry_row(final))
    for row in ledger_rows(final):
        f03b.upsert_csv(ALPHA_LEDGER, "ledger_row_id", row)
        f30b.f30a.upsert_csv_io(STAGE_ROOT / "03_reviews" / "stage_run_ledger.csv", "ledger_row_id", row)
    f03b.append_once(CHANGELOG, RUN_ID, changelog_entry(final))
    f03b.append_once(IDEA_REGISTRY, RUN_ID, idea_registry_entry(final))


def run_registry_row(final: dict[str, Any]) -> dict[str, Any]:
    diagnosis = final["diagnosis"]
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "repair_or_closeout_decision(수리 또는 마감 결정)",
        "family": "experiment_execution(실험 실행)",
        "work_family": "experiment_execution(실험 실행)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": REPORT_PATH.as_posix(),
        "notes": f"scout={diagnosis['scout_clue_rows']};seed={diagnosis['seed_surface_rows']};handoff={diagnosis['handoff_candidate_rows']};valid_repair={diagnosis['valid_train_density_repair_opportunity_rows']};next={NEXT_RUN_ID}",
        "run_number": RUN_NUMBER,
        "date": "2026-06-14",
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "claim_boundary": final["result_boundary"],
        "report_path": REPORT_PATH.as_posix(),
        "created_at_utc": final["created_at_utc"],
        "primary_kpi": f"scout={diagnosis['scout_clue_rows']};seed={diagnosis['seed_surface_rows']};handoff={diagnosis['handoff_candidate_rows']};valid_repair={diagnosis['valid_train_density_repair_opportunity_rows']}",
        "guardrail_kpi": "repair_rejected_no_posthoc_threshold_edit_no_exit_shape_activation",
        "external_verification_status": final["runtime_probe_status"],
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "result_path": REPORT_PATH.as_posix(),
    }


def ledger_rows(final: dict[str, Any]) -> list[dict[str, Any]]:
    diagnosis = final["diagnosis"]
    primary = {
        "ledger_row_id": f"{RUN_ID}__repair_decision",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": f"{RUN_ID}__repair_decision",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "repair_or_closeout_decision(수리 또는 마감 결정)",
        "tier_scope": "Tier A(티어 A)",
        "kpi_scope": "repair_audit_no_runtime(수리 감사, 런타임 아님)",
        "scoreboard_lane": "repair_decision(수리 결정)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": REPORT_PATH.as_posix(),
        "primary_kpi": f"scout={diagnosis['scout_clue_rows']};seed={diagnosis['seed_surface_rows']};handoff={diagnosis['handoff_candidate_rows']};valid_repair={diagnosis['valid_train_density_repair_opportunity_rows']}",
        "guardrail_kpi": "no_posthoc_threshold_edit_no_exit_shape_activation_no_authority",
        "external_verification_status": final["runtime_probe_status"],
        "notes": f"preserved={PRESERVED_CLUE};negative={NEGATIVE_MEMORY};next={NEXT_RUN_ID}",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "run_family": "repair_decision(수리 결정)",
    }
    return [primary]


def update_current_truth(final: dict[str, Any]) -> None:
    io_path(WORKSPACE_STATE).write_text(workspace_state(final), encoding="utf-8-sig")
    f03b.write_text_sig(CURRENT_WORKING_STATE, current_working_state(final))


def workspace_state(final: dict[str, Any]) -> str:
    return "\n".join([
        f"current_stage_id: {STAGE_ID}",
        f"current_run_id: {RUN_ID}",
        f"latest_completed_run_id: {RUN_ID}",
        f"current_status: {final['status']}",
        f"current_judgment: {final['judgment']}",
        f"next_run_id: {NEXT_RUN_ID}",
        "runtime_authority: not_claimed",
        "operating_promotion: not_claimed",
        "goal_achieve: not_claimed",
        f"updated_at_utc: '{final['created_at_utc']}'",
        "",
    ])


def report_text(final: dict[str, Any]) -> str:
    d = final["diagnosis"]
    return f"""# Frontier30C Repair Or Closeout Decision Report(전선30C 수리 또는 마감 결정 보고서)

Updated(갱신): {final['created_at_utc']}

Status(상태): `{final['status']}`

Judgment(판정): `{final['judgment']}`

Action(행동): F30B density-preserving preselector(전선30B 밀도 보존 사전 선택기) 결과를 repair audit(수리 감사)로 분해했습니다.

Effect(효과): scout clue(탐색 단서)는 `5`개였지만 모두 source no-veto branch(원천 무차단 분기)에 있고, seed/handoff(씨앗/인계)는 `0/0`개라서 F30 잠금 안의 수리는 거절했습니다.

Diagnosis(진단):

- candidate_rows(후보 행): `{d['candidate_rows']}`
- density_bridge_rows(밀도 충족 행): `{d['density_bridge_rows']}`
- dual_positive_rows(양수 행): `{d['dual_positive_rows']}`
- scout_clue_rows(탐색 단서 행): `{d['scout_clue_rows']}`
- seed_surface_rows(씨앗 표면 행): `{d['seed_surface_rows']}`
- handoff_candidate_rows(인계 후보 행): `{d['handoff_candidate_rows']}`
- near_seed_pf_band_rows(씨앗 근접 PF 구간 행): `{d['near_seed_pf_band_rows']}`
- scout_pf_blocked_seed_rows(탐색 중 PF 부족 씨앗 차단 행): `{d['scout_pf_blocked_seed_rows']}`
- source_branch_scout_only_rows(원천 분기 전용 탐색 행): `{d['source_branch_scout_only_rows']}`
- veto_branch_scout_rows(차단 분기 탐색 행): `{d['veto_branch_scout_rows']}`
- valid_train_density_repair_opportunity_rows(유효 학습 밀도 수리 기회 행): `{d['valid_train_density_repair_opportunity_rows']}`

Preserved clue(보존 단서): `{PRESERVED_CLUE}`

Negative memory(부정 기억): `{NEGATIVE_MEMORY}`

Runtime probe status(런타임 탐침 상태): `{final['runtime_probe_status']}`

ONNX status(ONNX 상태): `{final['onnx_status']}`

Next action(다음 행동): `{NEXT_RUN_ID}`

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 not_claimed(주장 없음)입니다.
"""


def gate_audit(final: dict[str, Any]) -> str:
    return f"""# Frontier30C Gate Audit(전선30C 게이트 감사)

- proxy_source_gate(프록시 원천 게이트): `{F30B_CANDIDATE_SUMMARY.as_posix()}` read(읽음)
- repair_audit_gate(수리 감사 게이트): valid_train_density_repair_opportunity_rows(유효 학습 밀도 수리 기회 행) `{final['diagnosis']['valid_train_density_repair_opportunity_rows']}`
- posthoc_guard(사후 편집 방어): F29 threshold repair(F29 임계값 수리)와 exit-shape activation(청산 형태 활성화)을 F30C에서 금지
- runtime_probe_gate(런타임 탐침 게이트): `{final['runtime_probe_status']}`
- final_claim_guard(최종 주장 방어): runtime authority/operating promotion/Goal Achieve(런타임 권위/운영 승격/목표 달성) not_claimed(주장 없음)
"""


def selection_status(final: dict[str, Any]) -> str:
    return f"""# Frontier30 Selection Status(전선30 선택 상태)

Selection(선택): no selected baseline/completion/promotion/runtime authority(선택 기준선/완성/승격/런타임 권위 없음).

Latest decision(최근 결정): `{RUN_ID}`

Status(상태): `{final['status']}`

Judgment(판정): `{final['judgment']}`

Preserved clue(보존 단서): `{PRESERVED_CLUE}`

Negative memory(부정 기억): `{NEGATIVE_MEMORY}`

Runtime probe status(런타임 탐침 상태): `{final['runtime_probe_status']}`

Next action(다음 행동): `{NEXT_RUN_ID}`

Claim boundary(주장 경계): no completion, no baseline, no promotion, no runtime authority, no live readiness, no Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음).
"""


def current_working_state(final: dict[str, Any]) -> str:
    d = final["diagnosis"]
    return f"""# Current Working State(현재 작업 상태)

Updated(갱신): {final['created_at_utc']}

## Active Stage(현재 단계)

- stage(단계): `{STAGE_ID}`
- latest run(최근 실행): `{RUN_ID}`
- status(상태): `{final['status']}`
- judgment(판정): `{final['judgment']}`
- next run(다음 실행): `{NEXT_RUN_ID}`

## Current Truth(현재 진실)

Action(행동): F30C(전선30C)는 F30B(전선30B) scout-only(탐색 전용) 결과를 repair audit(수리 감사)로 닫았습니다.

Effect(효과): scout/seed/handoff(탐색/씨앗/인계)는 `{d['scout_clue_rows']}/{d['seed_surface_rows']}/{d['handoff_candidate_rows']}`이고, valid repair(유효 수리)는 `{d['valid_train_density_repair_opportunity_rows']}`개입니다. 따라서 다음은 closeout(마감)입니다.

Runtime probe boundary(런타임 탐침 경계): `{final['runtime_probe_status']}`

Claim boundary(주장 경계): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def changelog_entry(final: dict[str, Any]) -> str:
    d = final["diagnosis"]
    return (
        f"- {final['created_at_utc']}: `{RUN_ID}` rejected F30 repair(전선30 수리 거절). "
        f"Effect(효과): scout={d['scout_clue_rows']}, seed={d['seed_surface_rows']}, handoff={d['handoff_candidate_rows']}, valid_repair={d['valid_train_density_repair_opportunity_rows']}, next=`{NEXT_RUN_ID}`.\n"
    )


def idea_registry_entry(final: dict[str, Any]) -> str:
    return (
        f"- `IDEA-FR30-TRAIN-DENSITY-PRESERVING-PRESELECTOR-BEFORE-LOSS-VETO-ONNX-SCOUT`: `{RUN_ID}` preserved clue(보존 단서) `{PRESERVED_CLUE}` and negative memory(부정 기억) `{NEGATIVE_MEMORY}`. "
        "Effect(효과): next clue(다음 단서)는 exit-shape pivot(청산 형태 전환)입니다.\n"
    )


def artifact_identity(path: Path) -> dict[str, str]:
    return {"path": path.as_posix(), "sha256": sha256_io(path) if path_exists(path) else "missing"}


def sha256_io(path: Path) -> str:
    return hashlib.sha256(io_path(path).read_bytes()).hexdigest()


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


if __name__ == "__main__":
    raise SystemExit(main())
