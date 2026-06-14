from __future__ import annotations

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
from stage_pipelines.stage_frontier_03 import frontier03b_regime_asymmetric_label_proxy_scout as f03b
from stage_pipelines.stage_frontier_29 import frontier29b_train_only_loss_concentration_veto_proxy_scout as f29b
from stage_pipelines.stage_frontier_29 import materialize_frontier29a_stage_open as f29a


STAGE_ID = f29a.STAGE_ID
RUN_ID = "frontier29C_loss_concentration_veto_repair_or_closeout_decision_v1"
RUN_NUMBER = "frontier29C"
PARENT_RUN_ID = f29b.RUN_ID
NEXT_RUN_ID = "frontier29D_stage_closeout_loss_concentration_veto_v1"
STATUS = "loss_concentration_veto_repair_rejected_no_scout_no_handoff_no_authority"
JUDGMENT = "repair_rejected_frozen_contract_no_valid_train_only_density_preserving_opportunity"

STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REPORT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_report.md"
GATE_AUDIT_PATH = STAGE_ROOT / "03_reviews" / f"{RUN_ID}_gate_audit.md"
SCRIPT_PATH = Path("stage_pipelines/stage_frontier_29/frontier29c_loss_concentration_veto_repair_or_closeout_decision.py")

F29A_SUMMARY = STAGE_ROOT / "02_runs" / f29a.RUN_ID / "stage_open_summary.json"
F29B_SUMMARY = STAGE_ROOT / "02_runs" / f29b.RUN_ID / "final_summary.json"
F29B_CANDIDATE_SUMMARY = STAGE_ROOT / "02_runs" / f29b.RUN_ID / "loss_veto_candidate_summary.csv"
F29B_SCREENED_RULES = STAGE_ROOT / "02_runs" / f29b.RUN_ID / "loss_concentration_screened_rule_ledger.csv"

RUN_REGISTRY = Path("docs/registers/run_registry.csv")
ALPHA_LEDGER = Path("docs/registers/alpha_run_ledger.csv")
IDEA_REGISTRY = Path("docs/registers/idea_registry.md")
CHANGELOG = Path("docs/workspace/changelog.md")
WORKSPACE_STATE = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE = Path("docs/context/current_working_state.md")

PRESERVED_CLUE = (
    "f29_loss_concentration_veto_created_density_bridge_and_dual_positive_fragments_but_no_scout_rows_reference_only"
    "(전선29 손실 집중 차단은 밀도 충족과 양수 조각을 만들었지만 탐색 행은 0개라 참조 전용 보존)"
)
NEGATIVE_MEMORY = (
    "under_f29_locked_train_loss_veto_contract_scout_seed_and_handoff_remained_zero"
    "(전선29 잠금 학습 손실 차단 계약 아래 탐색/씨앗/인계가 모두 0개로 남음)"
)
NEXT_HYPOTHESIS_CLUE = (
    "train_density_preserving_selector_before_loss_veto_or_exit_shape_pivot_reference_only"
    "(손실 차단 전 학습 밀도 보존 선택기 또는 청산 형태 전환을 참조 전용 다음 단서로 보존)"
)


def main() -> int:
    ensure_dirs()
    created_at = utc_now()
    stage_open = read_json(F29A_SUMMARY)
    f29b_summary = read_json(F29B_SUMMARY)
    candidates = pd.read_csv(io_path(F29B_CANDIDATE_SUMMARY))
    screened = pd.read_csv(io_path(F29B_SCREENED_RULES))
    audit = build_repair_audit(candidates)
    final = build_final(created_at, stage_open, f29b_summary, candidates, screened, audit)
    write_outputs(final, audit)
    update_registries(final)
    update_current_truth(final)
    print(json.dumps(json_ready({
        "status": final["status"],
        "judgment": final["judgment"],
        "run_id": RUN_ID,
        "near_scout_rows": final["diagnosis"]["near_scout_rows"],
        "valid_train_loss_repair_opportunity_rows": final["diagnosis"]["valid_train_loss_repair_opportunity_rows"],
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
    rows["density_dual_positive"] = rows["density_bridge"] & rows["dual_positive"]
    rows["near_scout"] = (
        rows["density_bridge"]
        & rows["dual_positive"]
        & (rows["forward_min_pf"] >= 1.05)
        & (rows["forward_max_dd"] <= 30.0)
    )
    rows["pf_ready_density"] = rows["density_bridge"] & rows["dual_positive"] & (rows["forward_min_pf"] >= 1.10)
    rows["dd_ready_density"] = rows["density_bridge"] & rows["dual_positive"] & (rows["forward_max_dd"] <= 25.0)
    rows["pf_ready_dd_blocked"] = rows["pf_ready_density"] & (rows["forward_max_dd"] > 25.0)
    rows["dd_ready_pf_blocked"] = rows["dd_ready_density"] & (rows["forward_min_pf"] < 1.10)
    rows["density_thin_near_forward"] = rows["near_scout"] & (rows["forward_min_density"] < 5.0)
    rows["would_require_posthoc_contract_edit"] = (
        rows["near_scout"]
        | rows["density_thin_near_forward"]
        | rows["dd_ready_pf_blocked"]
        | rows["pf_ready_dd_blocked"]
    )
    rows["valid_train_loss_repair_opportunity"] = False
    rows["repair_rejection_reason"] = rows.apply(repair_rejection_reason, axis=1)
    keep = [
        "veto_candidate_id",
        "source_stability_union_id",
        "train_veto_score",
        "removed_train_trade_fraction",
        "loss_capture_ratio",
        "validation_profit_factor",
        "validation_trades_per_day",
        "validation_dd_risk",
        "oos_profit_factor",
        "oos_trades_per_day",
        "oos_dd_risk",
        "forward_min_pf",
        "forward_max_dd",
        "forward_min_density",
        "forward_max_density",
        "density_bridge",
        "dual_positive",
        "density_dual_positive",
        "near_scout",
        "pf_ready_density",
        "dd_ready_density",
        "pf_ready_dd_blocked",
        "dd_ready_pf_blocked",
        "density_thin_near_forward",
        "would_require_posthoc_contract_edit",
        "valid_train_loss_repair_opportunity",
        "repair_rejection_reason",
    ]
    return rows[keep].copy()


def repair_rejection_reason(row: pd.Series) -> str:
    if bool(row.get("scout_clue_flag", False)):
        return "not_rejected_existing_scout_row"
    if bool(row.get("would_require_posthoc_contract_edit", False)):
        return "rejected_requires_posthoc_density_or_threshold_edit_after_forward_read"
    return "rejected_no_scout_signal_under_frozen_train_loss_veto_contract"


def build_final(
    created_at: str,
    stage_open: dict[str, Any],
    f29b_summary: dict[str, Any],
    candidates: pd.DataFrame,
    screened: pd.DataFrame,
    audit: pd.DataFrame,
) -> dict[str, Any]:
    workspace = read_text(WORKSPACE_STATE)
    checks = {
        "workspace_current_frontier29b": f"current_run_id: {PARENT_RUN_ID}" in workspace,
        "stage_open_lock_no_posthoc": bool(stage_open.get("locks", {}).get("veto_contract", {}).get("no_post_hoc_edits")),
        "f29b_no_scout": int(f29b_summary.get("scout_clue_rows", -1)) == 0,
        "f29b_no_seed": int(f29b_summary.get("seed_surface_rows", -1)) == 0,
        "f29b_no_handoff": int(f29b_summary.get("handoff_candidate_rows", -1)) == 0,
        "candidate_rows_match": len(candidates) == int(f29b_summary.get("selected_veto_rows", -1)),
        "screened_rows_match": len(screened) == int(f29b_summary.get("screened_rule_rows", -1)),
        "audit_rows_match": len(audit) == len(candidates),
        "valid_repair_zero": int(audit["valid_train_loss_repair_opportunity"].sum()) == 0,
    }
    if not all(checks.values()):
        raise RuntimeError(f"Frontier29C repair decision checks failed: {json.dumps(checks, ensure_ascii=False)}")
    diagnosis = {
        "selected_veto_rows": int(len(candidates)),
        "screened_rule_rows": int(len(screened)),
        "density_bridge_rows": int(audit["density_bridge"].sum()),
        "dual_positive_rows": int(audit["dual_positive"].sum()),
        "density_dual_positive_rows": int(audit["density_dual_positive"].sum()),
        "near_scout_rows": int(audit["near_scout"].sum()),
        "pf_ready_density_rows": int(audit["pf_ready_density"].sum()),
        "dd_ready_density_rows": int(audit["dd_ready_density"].sum()),
        "pf_ready_dd_blocked_rows": int(audit["pf_ready_dd_blocked"].sum()),
        "dd_ready_pf_blocked_rows": int(audit["dd_ready_pf_blocked"].sum()),
        "density_thin_near_forward_rows": int(audit["density_thin_near_forward"].sum()),
        "would_require_posthoc_contract_edit_rows": int(audit["would_require_posthoc_contract_edit"].sum()),
        "valid_train_loss_repair_opportunity_rows": int(audit["valid_train_loss_repair_opportunity"].sum()),
    }
    return {
        "created_at_utc": created_at,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "preserved_clue": PRESERVED_CLUE,
        "negative_memory": NEGATIVE_MEMORY,
        "next_hypothesis_clue": NEXT_HYPOTHESIS_CLUE,
        "repair_decision": "reject_repair_and_closeout",
        "diagnosis": diagnosis,
        "checks": checks,
        "runtime_probe_status": "runtime_probe_ineligible_no_handoff_candidate_after_f29c_repair_decision",
        "onnx_status": "onnx_branch_unattempted_no_handoff_candidate_after_f29c_repair_decision",
        "claim_boundary": {claim: "not_claimed" for claim in f03b.FORBIDDEN_CLAIMS},
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
        F29A_SUMMARY,
        F29B_SUMMARY,
        F29B_CANDIDATE_SUMMARY,
        F29B_SCREENED_RULES,
        RUN_ROOT / "repair_rejection_audit.csv",
        RUN_ROOT / "final_summary.json",
        REPORT_PATH,
        GATE_AUDIT_PATH,
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
        "diagnosis": final["diagnosis"],
        "claim_boundary": final["claim_boundary"],
    }


def update_registries(final: dict[str, Any]) -> None:
    f03b.upsert_csv(RUN_REGISTRY, "run_id", run_registry_row(final))
    for row in ledger_rows(final):
        f03b.upsert_csv(ALPHA_LEDGER, "ledger_row_id", row)
        f03b.upsert_csv(STAGE_ROOT / "03_reviews" / "stage_run_ledger.csv", "ledger_row_id", row)
    f03b.append_once(CHANGELOG, RUN_ID, changelog_entry(final))
    f03b.append_once(IDEA_REGISTRY, RUN_ID, idea_registry_entry(final))


def run_registry_row(final: dict[str, Any]) -> dict[str, Any]:
    d = final["diagnosis"]
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "repair_or_closeout_decision(수리 또는 마감 결정)",
        "family": "result_judgment(결과 판정)",
        "work_family": "result_judgment(결과 판정)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": REPORT_PATH.as_posix(),
        "notes": f"near={d['near_scout_rows']};pf_ready_density={d['pf_ready_density_rows']};dd_ready_pf_blocked={d['dd_ready_pf_blocked_rows']};valid_repair={d['valid_train_loss_repair_opportunity_rows']};next={NEXT_RUN_ID}",
        "run_number": RUN_NUMBER,
        "date": "2026-06-14",
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "claim_boundary": "repair_rejected_no_wfo_no_mt5_no_onnx_no_authority_goal_claim",
        "report_path": REPORT_PATH.as_posix(),
        "created_at_utc": final["created_at_utc"],
        "primary_kpi": f"near={d['near_scout_rows']};valid_repair={d['valid_train_loss_repair_opportunity_rows']};scout=0;seed=0;handoff=0",
        "guardrail_kpi": "frozen_contract_no_posthoc_threshold_edit_no_authority",
        "external_verification_status": final["runtime_probe_status"],
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "result_path": REPORT_PATH.as_posix(),
    }


def ledger_rows(final: dict[str, Any]) -> list[dict[str, Any]]:
    d = final["diagnosis"]
    primary = {
        "ledger_row_id": f"{RUN_ID}__tier_a_repair_decision",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": f"{RUN_ID}__tier_a_repair_decision",
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "Tier A separate(티어 A 분리)",
        "tier_scope": "Tier A(티어 A)",
        "kpi_scope": "repair_decision_not_runtime(수리 결정, 런타임 아님)",
        "scoreboard_lane": "repair_or_closeout_decision(수리 또는 마감 결정)",
        "status": final["status"],
        "judgment": final["judgment"],
        "path": REPORT_PATH.as_posix(),
        "primary_kpi": f"near={d['near_scout_rows']};valid_repair={d['valid_train_loss_repair_opportunity_rows']};scout=0;seed=0;handoff=0",
        "guardrail_kpi": "no_posthoc_contract_edit_no_wfo_no_mt5_no_onnx_no_authority",
        "external_verification_status": final["runtime_probe_status"],
        "notes": f"{final['preserved_clue']};{final['negative_memory']}",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "run_family": "result_judgment(결과 판정)",
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
        f"next_run_id: {final['next_run_id']}",
        "runtime_authority: not_claimed",
        "operating_promotion: not_claimed",
        "goal_achieve: not_claimed",
        f"updated_at_utc: '{final['created_at_utc']}'",
        "",
    ])


def report_text(final: dict[str, Any]) -> str:
    d = final["diagnosis"]
    return f"""# Frontier29C Repair Or Closeout Decision Report(전선29C 수리 또는 마감 결정 보고서)

Updated(갱신): {final['created_at_utc']}

Status(상태): `{final['status']}`

Judgment(판정): `{final['judgment']}`

Action(행동): F29B loss concentration veto(전선29B 손실 집중 차단) 결과를 repair audit(수리 감사)로 분해했습니다.

Effect(효과): near scout(탐색 근접) 행은 있었지만 scout/seed/handoff(탐색/씨앗/인계)가 0개였고, 추가 수리는 F29A frozen contract(고정 계약)을 사후 변경해야 하므로 거절했습니다.

Diagnosis(진단):

- selected_veto_rows(선택 차단 행): `{d['selected_veto_rows']}`
- density_bridge_rows(밀도 충족 행): `{d['density_bridge_rows']}`
- density_dual_positive_rows(밀도+양수 행): `{d['density_dual_positive_rows']}`
- near_scout_rows(탐색 근접 행): `{d['near_scout_rows']}`
- pf_ready_density_rows(PF 준비+밀도 행): `{d['pf_ready_density_rows']}`
- dd_ready_pf_blocked_rows(DD 준비+PF 차단 행): `{d['dd_ready_pf_blocked_rows']}`
- would_require_posthoc_contract_edit_rows(사후 계약 변경 필요 행): `{d['would_require_posthoc_contract_edit_rows']}`
- valid_train_loss_repair_opportunity_rows(유효 학습 손실 수리 기회 행): `{d['valid_train_loss_repair_opportunity_rows']}`

Preserved clue(보존 단서): `{final['preserved_clue']}`

Negative memory(부정 기억): `{final['negative_memory']}`

Runtime probe status(런타임 탐침 상태): `{final['runtime_probe_status']}`

ONNX status(ONNX 상태): `{final['onnx_status']}`

Next action(다음 행동): `{final['next_run_id']}`

Claim boundary(주장 경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 not_claimed(주장 없음)입니다.
"""


def gate_audit(final: dict[str, Any]) -> str:
    d = final["diagnosis"]
    return f"""# Frontier29C Gate Audit(전선29C 게이트 감사)

- repair_audit_gate(수리 감사 게이트): `repair_rejection_audit.csv` created(생성)
- frozen_contract_gate(고정 계약 게이트): no post-hoc threshold/density edit(사후 임계값/밀도 편집 없음)
- repair_decision_gate(수리 결정 게이트): valid_train_loss_repair_opportunity_rows(유효 학습 손실 수리 기회 행) `{d['valid_train_loss_repair_opportunity_rows']}`
- runtime_probe_gate(런타임 탐침 게이트): `{final['runtime_probe_status']}`
- onnx_gate(ONNX 게이트): `{final['onnx_status']}`
- final_claim_guard(최종 주장 방어): runtime authority/operating promotion/Goal Achieve(런타임 권위/운영 승격/목표 달성) not_claimed(주장 없음)
"""


def selection_status(final: dict[str, Any]) -> str:
    return f"""# Frontier29 Selection Status(전선29 선택 상태)

Selection(선택): no selected baseline/completion/promotion/runtime authority(선택 기준선/완성/승격/런타임 권위 없음).

Latest decision(최근 결정): `{RUN_ID}`

Status(상태): `{final['status']}`

Judgment(판정): `{final['judgment']}`

Preserved clue(보존 단서): `{final['preserved_clue']}`

Negative memory(부정 기억): `{final['negative_memory']}`

Runtime probe status(런타임 탐침 상태): `{final['runtime_probe_status']}`

ONNX status(ONNX 상태): `{final['onnx_status']}`

Next action(다음 행동): `{final['next_run_id']}`
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
- next run(다음 실행): `{final['next_run_id']}`

## Current Truth(현재 진실)

Action(행동): F29C(전선29C)가 F29B loss veto(손실 차단) 수리 가능성을 감사하고 repair rejected(수리 거절)로 닫을 준비를 했습니다.

Effect(효과): near_scout(탐색 근접) `{d['near_scout_rows']}`개는 있었지만 valid_train_loss_repair_opportunity(유효 학습 손실 수리 기회)는 `{d['valid_train_loss_repair_opportunity_rows']}`개라, 사후 threshold/density edit(임계값/밀도 편집)을 하지 않습니다.

Runtime probe status(런타임 탐침 상태): `{final['runtime_probe_status']}`

Claim boundary(주장 경계): completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not_claimed(주장 없음)입니다.
"""


def changelog_entry(final: dict[str, Any]) -> str:
    d = final["diagnosis"]
    return (
        f"- {final['created_at_utc']}: `{RUN_ID}` rejected F29 loss-veto repair(전선29 손실 차단 수리 거절). "
        f"Effect(효과): near/valid_repair(근접/유효 수리) counts are {d['near_scout_rows']}/{d['valid_train_loss_repair_opportunity_rows']} and next run(다음 실행) is `{NEXT_RUN_ID}`.\n"
    )


def idea_registry_entry(final: dict[str, Any]) -> str:
    return (
        f"- `IDEA-FR29-TRAIN-ONLY-LOSS-CONCENTRATION-VETO-PF-DD-BALANCE-ONNX-SCOUT`: `{RUN_ID}` found no valid frozen-contract repair(고정 계약 수리 없음). "
        f"Effect(효과): `{final['negative_memory']}`.\n"
    )


def artifact_identity(path: Path) -> dict[str, str]:
    return {"path": path.as_posix(), "sha256": sha256_io(path) if path_exists(path) else "missing"}


def sha256_io(path: Path) -> str:
    digest = hashlib.sha256()
    with io_path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_json(path: Path) -> Any:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def read_text(path: Path) -> str:
    return io_path(path).read_text(encoding="utf-8-sig")


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
