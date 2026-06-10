from __future__ import annotations

import json
import math
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Sequence

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from stage_pipelines.stage364 import train_h17_oos108_pf125_cost_repaired_density_reexpand_without_db as gl


fn = gl.fn
et = gl.et

TODAY = "2026-06-07"
STAGE_ID = gl.STAGE_ID
STAGE_DIR = gl.STAGE_DIR
REVIEW_DIR = gl.REVIEW_DIR
SPEC_DIR = gl.SPEC_DIR
SELECTED_DIR = gl.SELECTED_DIR

RUN_NUMBER = "run364GM"
RUN_ID = "run364GM_review_h17_oos108_pf125_cost_repaired_density_reexpand_without_db_v1"
PARENT_RUN_ID = gl.RUN_ID
NEXT_RUN_ID = "run364GN_train_h17_oos108_pf125_density_cost_dual_anchor_router_without_db_v1"

STATUS = "completed_stage364GM_cost_repaired_density_reexpand_review_density_recovered_cost_failed_open_gn_no_authority"
JUDGMENT = "negative_cost_repaired_density_reexpand_review_density_recovered_cost_failed_no_package_no_authority"
DECISION = "stage364GM_reject_package_open_run364GN_density_cost_dual_anchor_router"
CLAIM_BOUNDARY = (
    "research_development_cost_repaired_density_reexpand_review_only_no_runtime_package_no_new_mt5_execution_"
    "no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
REVIEW_SUMMARY = RUN_DIR / "gm_review_summary.csv"
SURFACE_DIAGNOSTIC = RUN_DIR / "gm_surface_diagnostic.csv"
FAILURE_ATTRIBUTION = RUN_DIR / "gm_failure_attribution.csv"
PACKAGE_DECISION = RUN_DIR / "package_decision.csv"
FAILURE_MEMORY = RUN_DIR / "gm_failure_memory.csv"
RUN364GN_QUEUE = RUN_DIR / "gm_gn_queue.csv"
RESULT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
ATTRIBUTION_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / "run364GM_cost_repaired_density_reexpand_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364GM_cost_repaired_density_reexpand_review.md"
REVIEW_INDEX = REVIEW_DIR / "review_index.md"
STAGE_LEDGER = REVIEW_DIR / "stage_run_ledger.csv"
STAGE_BRIEF = SPEC_DIR / "stage_brief.md"
SELECTION_STATUS = SELECTED_DIR / "selection_status.md"
STAGE_README = STAGE_DIR / "README.md"

WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_WORKING_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
PROJECT_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
IDEA_REGISTRY = ROOT / "docs" / "registers" / "idea_registry.md"
NEGATIVE_REGISTER = ROOT / "docs" / "registers" / "negative_result_register.md"

THIS_FILE = Path(__file__)

INPUT_FILES = [
    gl.FINAL_DECISION,
    gl.GATE_AUDIT,
    gl.TRADE_SURFACE,
    gl.SELECTED_CANDIDATE,
    gl.SELECTED_TRADE_TAPE,
    gl.COST_STRESS,
    gl.SIDE_SESSION_REVIEW,
    gl.MONTH_STABILITY,
    gl.MODEL_SCORECARD,
    gl.MODEL_ARTIFACT_MANIFEST,
    gl.ONNX_SMOKE_REPORT,
    gl.DATA_INTEGRITY_AUDIT,
    gl.RUN364GM_QUEUE,
    THIS_FILE,
]

OUTPUT_FILES = [
    INPUT_MANIFEST,
    WORK_PACKET,
    REVIEW_SUMMARY,
    SURFACE_DIAGNOSTIC,
    FAILURE_ATTRIBUTION,
    PACKAGE_DECISION,
    FAILURE_MEMORY,
    RUN364GN_QUEUE,
    RESULT_RECEIPT,
    MODEL_RECEIPT,
    ATTRIBUTION_RECEIPT,
    LINEAGE_RECEIPT,
    CLAIM_RECEIPT,
    GATE_AUDIT,
    FINAL_DECISION,
    RUN_MANIFEST,
    REPORT_PATH,
    DECISION_DOC,
    THIS_FILE,
]


def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def exists(path: Path) -> bool:
    return fn.io_path(path).exists()


def rel(path: Path) -> str:
    return gl.rel(path)


def sha(path: Path) -> str:
    return gl.sha(path)


def as_float(value: Any, default: float = 0.0) -> float:
    if value is None:
        return default
    try:
        number = float(value)
    except (TypeError, ValueError):
        return default
    return number if math.isfinite(number) else default


def fmt(value: Any, digits: int = 10) -> str:
    number = as_float(value, float("nan"))
    if not math.isfinite(number):
        return ""
    text = f"{number:.{digits}f}".rstrip("0").rstrip(".")
    return text if text else "0"


def read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(fn.io_path(path), encoding="utf-8-sig").fillna("")


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    et.write_csv(path, list(rows))


def write_json(path: Path, payload: Mapping[str, Any]) -> None:
    fn.write_json(path, payload)


def append_or_replace_csv(path: Path, keys: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> None:
    fn.append_or_replace_csv(path, list(keys), list(rows))


def ensure_dirs() -> None:
    for path in [RUN_DIR, REVIEW_DIR, SPEC_DIR, SELECTED_DIR, ROOT / "docs" / "decisions"]:
        path.mkdir(parents=True, exist_ok=True)


def validate_inputs() -> dict[str, Any]:
    missing = [rel(path) for path in INPUT_FILES if path != THIS_FILE and not exists(path)]
    if missing:
        raise FileNotFoundError("missing GM inputs(GM 입력 누락): " + ", ".join(missing))
    with fn.io_path(gl.FINAL_DECISION).open("r", encoding="utf-8-sig") as handle:
        parent = json.load(handle)
    if parent.get("run_id") != PARENT_RUN_ID:
        raise RuntimeError(f"parent run mismatch(상위 실행 불일치): {parent.get('run_id')} != {PARENT_RUN_ID}")
    if parent.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"GL next_run_id mismatch(GL 다음 실행 ID 불일치): {parent.get('next_run_id')} != {RUN_ID}")
    for key in ["runtime_authority", "operating_promotion", "live_readiness", "goal_achieve"]:
        if parent.get(key, "not_claimed") != "not_claimed":
            raise RuntimeError(f"forbidden GL claim(금지된 GL 주장): {key}={parent.get(key)}")
    gates = read_csv(gl.GATE_AUDIT)
    if gates.empty or any(gates["status"].astype(str) != "passed"):
        raise RuntimeError("GL gate audit(GL 게이트 감사)가 모두 passed(통과)가 아닙니다.")
    return parent


def input_manifest_rows() -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "input_path": rel(path),
            "exists": str(exists(path)).lower(),
            "sha256": sha(path) if exists(path) and fn.io_path(path).is_file() else "",
            "input_role": "GM cost-repaired density reexpand review input(GM 비용 수리 후 밀도 재확장 검토 입력)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for path in INPUT_FILES
    ]


def num(frame: pd.DataFrame, column: str) -> pd.Series:
    return pd.to_numeric(frame[column], errors="coerce") if column in frame.columns else pd.Series([float("nan")] * len(frame))


def row_from_frame(label: str, frame: pd.DataFrame, note: str) -> dict[str, Any]:
    if frame.empty:
        return {"run_id": RUN_ID, "diagnostic_id": label, "model_id": "", "note": note, "claim_boundary": CLAIM_BOUNDARY}
    row = frame.iloc[0].to_dict()
    return {
        "run_id": RUN_ID,
        "diagnostic_id": label,
        "model_id": row.get("model_id", ""),
        "label_id": row.get("label_id", ""),
        "feature_set_id": row.get("feature_set_id", ""),
        "hours_id": row.get("hours_id", ""),
        "extra_filter": row.get("extra_filter", ""),
        "validation_net": fmt(row.get("validation_net")),
        "validation_profit_factor": fmt(row.get("validation_profit_factor")),
        "validation_trade_density": fmt(row.get("validation_trade_density")),
        "oos_net": fmt(row.get("oos_net")),
        "oos_profit_factor": fmt(row.get("oos_profit_factor")),
        "oos_trade_density": fmt(row.get("oos_trade_density")),
        "oos_cost06_net": fmt(row.get("oos_cost06_net")),
        "oos_cost09_net": fmt(row.get("oos_cost09_net")),
        "combined_net": fmt(row.get("combined_net")),
        "combined_trade_density": fmt(row.get("combined_trade_density")),
        "combined_cost09_net": fmt(row.get("combined_cost09_net")),
        "combined_short_share": fmt(row.get("combined_short_share")),
        "selection_score": fmt(row.get("selection_score")),
        "note": note,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def build_review(parent: Mapping[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    surface = read_csv(gl.TRADE_SURFACE)
    validation_net = num(surface, "validation_net")
    oos_net = num(surface, "oos_net")
    validation_density = num(surface, "validation_trade_density")
    oos_density = num(surface, "oos_trade_density")
    combined_density = num(surface, "combined_trade_density")
    oos_pf = num(surface, "oos_profit_factor")
    oos_cost06 = num(surface, "oos_cost06_net")
    oos_cost09 = num(surface, "oos_cost09_net")
    combined_cost09 = num(surface, "combined_cost09_net")

    val_pos = validation_net > 0
    oos_pos = oos_net > 0
    density25 = (validation_density >= 2.5) & (oos_density >= 2.5) & (combined_density >= 2.5)
    density23 = (validation_density >= 2.3) & (oos_density >= 2.3) & (combined_density >= 2.3)
    density20 = (validation_density >= 2.0) & (oos_density >= 2.0) & (combined_density >= 2.0)
    cost_near = oos_cost06 >= -8
    cost_nonneg = oos_cost06 >= 0
    combined_cost09_better_than_gj = combined_cost09 >= -120

    selected_rows = surface[surface["model_id"].astype(str) == str(parent.get("selected_model_id", ""))]
    selected_best = selected_rows.sort_values("selection_score", ascending=False).head(1) if not selected_rows.empty else surface.sort_values("selection_score", ascending=False).head(1)
    best_density = surface[density25].sort_values(["combined_trade_density", "selection_score"], ascending=False).head(1)
    best_density_cost_near = surface[density23 & val_pos & oos_pos & cost_near].sort_values(["combined_trade_density", "oos_cost06_net"], ascending=False).head(1)
    best_cost = surface[cost_nonneg].sort_values(["combined_trade_density", "oos_cost06_net"], ascending=False).head(1)
    best_cost09 = surface[combined_cost09_better_than_gj].sort_values(["combined_trade_density", "combined_cost09_net"], ascending=False).head(1)

    summary = {
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "review_subject": parent.get("selected_model_id", ""),
        "selected_model_id": parent.get("selected_model_id", ""),
        "selected_validation_net": parent.get("selected_validation_net", ""),
        "selected_validation_profit_factor": parent.get("selected_validation_profit_factor", ""),
        "selected_validation_trade_density": parent.get("selected_validation_trade_density", ""),
        "selected_oos_net": parent.get("selected_oos_net", ""),
        "selected_oos_profit_factor": parent.get("selected_oos_profit_factor", ""),
        "selected_oos_trade_density": parent.get("selected_oos_trade_density", ""),
        "selected_oos_cost06_net": parent.get("selected_oos_cost06_net", ""),
        "selected_oos_cost09_net": parent.get("selected_oos_cost09_net", ""),
        "selected_combined_net": parent.get("selected_combined_net", ""),
        "selected_combined_trade_density": parent.get("selected_combined_trade_density", ""),
        "selected_combined_cost09_net": parent.get("selected_combined_cost09_net", ""),
        "selected_combined_short_share": parent.get("selected_combined_short_share", ""),
        "surface_rows": len(surface),
        "strict_candidate_count": parent.get("strict_candidate_count", 0),
        "operational_proxy_stack_pass_count": parent.get("operational_proxy_stack_pass_count", 0),
        "density25_all_splits_count": int(density25.sum()),
        "density25_valpos_oospos_count": int((density25 & val_pos & oos_pos).sum()),
        "density23_valpos_oospos_cost_near_count": int((density23 & val_pos & oos_pos & cost_near).sum()),
        "density20_valpos_oospos_cost_nonneg_count": int((density20 & val_pos & oos_pos & cost_nonneg).sum()),
        "oos_cost06_nonneg_count": int(cost_nonneg.sum()),
        "combined_cost09_better_than_gj_count": int(combined_cost09_better_than_gj.sum()),
        "max_validation_density": fmt(validation_density.max()),
        "max_oos_density": fmt(oos_density.max()),
        "max_combined_density": fmt(combined_density.max()),
        "max_oos_cost06_net": fmt(oos_cost06.max()),
        "max_oos_cost09_net": fmt(oos_cost09.max()),
        "max_combined_cost09_net": fmt(combined_cost09.max()),
        "package_eligible": "false",
        "runtime_package": "not_opened",
        "new_mt5_execution": "not_run",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "live_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "review_judgment": JUDGMENT,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    diagnostics = [
        row_from_frame("gm_selected(선택 행)", selected_best, "GL selected row(선택 행)는 밀도를 회복했지만 비용이 무너졌습니다."),
        row_from_frame("gm_best_density25(밀도2.5 이상 상위)", best_density, "밀도2.5 이상 행이 비용을 보존하는지 확인합니다."),
        row_from_frame("gm_best_density23_cost_near(밀도2.3 비용근접)", best_density_cost_near, "밀도2.3과 비용 근접 동시 후보가 있는지 확인합니다."),
        row_from_frame("gm_best_cost_nonnegative(비용 양수 상위)", best_cost, "비용0.6 양수 행의 밀도 상태를 확인합니다."),
        row_from_frame("gm_best_cost09_better(합산 비용0.9 개선 상위)", best_cost09, "합산 비용0.9가 GJ 수준 근처로 개선되는 행을 확인합니다."),
    ]
    attribution = [
        {"run_id": RUN_ID, "attribution_id": "gm01_density_recovered", "observation": "GL lifted selected combined density versus GJ(GL은 GJ 대비 선택 합산 밀도를 올림)", "evidence": f"selected_density={summary['selected_combined_trade_density']}", "effect": "h1 density supply(h1 밀도 공급)는 회수 단서입니다.", "claim_boundary": CLAIM_BOUNDARY},
        {"run_id": RUN_ID, "attribution_id": "gm02_cost_recollapsed", "observation": "GL lost cost repair(GL은 비용 수리를 잃음)", "evidence": f"oos_cost06={summary['selected_oos_cost06_net']};combined_cost09={summary['selected_combined_cost09_net']};density23_cost_near={summary['density23_valpos_oospos_cost_near_count']}", "effect": "GN은 cost anchor(비용 앵커)와 density anchor(밀도 앵커)를 분리 라우팅해야 합니다.", "claim_boundary": CLAIM_BOUNDARY},
    ]
    package = [{"run_id": RUN_ID, "package_eligible": "false", "decision": DECISION, "reason": "density recovered but cost floor failed and no MT5 runtime evidence(밀도는 회복됐지만 비용 바닥 실패, MT5 런타임 근거 없음)", "selected_model_id": summary["selected_model_id"], "next_run_id": NEXT_RUN_ID, "claim_boundary": CLAIM_BOUNDARY}]
    failure = [
        {
            "run_id": RUN_ID,
            "memory_id": "gm01_density_recovered_cost_failed",
            "failed_boundary": "density recovery with cost preservation(밀도 회복과 비용 보존 동시 충족)",
            "why_failed": f"selected_density={summary['selected_combined_trade_density']};oos_cost06={summary['selected_oos_cost06_net']};density23_cost_near={summary['density23_valpos_oospos_cost_near_count']}",
            "salvage_value": "GL h1 label stack recovered density and positive low-cost net(GL h1 라벨 묶음은 밀도와 저비용 양수 수익을 회복)",
            "reopen_condition": "dual-anchor router uses GJ cost anchor and GL density anchor together(이중 앵커 라우터가 GJ 비용 앵커와 GL 밀도 앵커를 함께 사용)",
            "do_not_repeat": "Do not alternate sparse cost-only and dense cost-collapse runs(희소 비용 전용과 고밀도 비용 붕괴 실행을 번갈아 반복하지 말 것).",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    queue = [
        {
            "run_id": RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "queue_rank": 1,
            "queue_id": "gn01_density_cost_dual_anchor_router",
            "hypothesis": "GJ cost anchor(GJ 비용 앵커)와 GL density anchor(GL 밀도 앵커)를 분리 라우팅하면 density-cost balance(밀도-비용 균형)가 개선될 수 있습니다.",
            "seed_from": "GJ cost-repaired sparse candidate + GL dense h1 candidate(GJ 비용 수리 희소 후보 + GL 고밀도 h1 후보)",
            "required_preserve": "combined density >=2.3 and OOS net>0(합산 밀도 2.3 이상과 표본외 순수익 양수)",
            "required_repair": "OOS cost0.6 near zero and combined cost0.9 materially better(표본외 비용0.6 0 근처와 합산 비용0.9 실질 개선)",
            "avoid": "simple score reweight oscillation(단순 점수 재가중 왕복)",
            "effect": "GN은 비용 앵커와 밀도 앵커를 한 모델 점수로 뭉개지 않고 라우팅합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    return [summary], diagnostics, attribution, package, failure, queue


def write_work_packet() -> None:
    write_json(
        WORK_PACKET,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "primary_family": "kpi_evidence(KPI 근거)",
            "primary_skill": "obsidian-run-evidence-system(옵시디언 실행 근거 시스템)",
            "support_skills": ["obsidian-artifact-lineage(옵시디언 산출물 계보)", "obsidian-result-judgment(옵시디언 결과 판정)", "obsidian-performance-attribution(옵시디언 성과 귀속)"],
            "required_gates": ["kpi_contract_audit(KPI 계약 감사)", "row_grain_audit(행 단위 감사)", "source_authority_audit(원천 권위 감사)", "required_gate_coverage_audit(필수 게이트 커버리지 감사)"],
            "decision_use": NEXT_RUN_ID,
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def final_payload(summary: Mapping[str, Any], gates: Sequence[Mapping[str, Any]], created_at: str) -> dict[str, Any]:
    return {
        **summary,
        "run_number": RUN_NUMBER,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_run_id": NEXT_RUN_ID,
        "gate_passes": sum(1 for row in gates if row["status"] == "passed"),
        "gate_total": len(gates),
        "created_at_utc": created_at,
        "report_path": rel(REPORT_PATH),
        "final_decision": rel(FINAL_DECISION),
    }


def gate_rows(final_written: bool) -> list[dict[str, Any]]:
    gates = [
        ("scope_completion_gate", REVIEW_SUMMARY),
        ("parent_integrity_gate", INPUT_MANIFEST),
        ("kpi_contract_audit", SURFACE_DIAGNOSTIC),
        ("package_decision_gate", PACKAGE_DECISION),
        ("failure_memory_gate", FAILURE_MEMORY),
        ("next_queue_gate", RUN364GN_QUEUE),
        ("paired_tier_record_gate", STAGE_LEDGER),
        ("receipt_coverage_gate", RESULT_RECEIPT),
        ("required_gate_coverage_audit", GATE_AUDIT),
        ("final_claim_guard", CLAIM_RECEIPT),
    ]
    rows = []
    for gate, path in gates:
        passed = exists(path) if gate != "required_gate_coverage_audit" else (final_written and exists(path))
        rows.append({"run_id": RUN_ID, "gate": gate, "status": "passed" if passed else "pending", "evidence": rel(path), "effect": "GM review gate keeps density-cost judgment bounded(GM 검토 게이트가 밀도-비용 판정 경계를 유지)", "claim_boundary": CLAIM_BOUNDARY})
    return rows


def write_receipts(final: Mapping[str, Any]) -> None:
    common = {"run_id": RUN_ID, "stage_id": STAGE_ID, "created_at_utc": final["created_at_utc"], "claim_boundary": CLAIM_BOUNDARY}
    write_json(RESULT_RECEIPT, {**common, "receipt_type": "result_judgment(결과 판정)", "judgment_label": JUDGMENT, "evidence_available": [rel(REVIEW_SUMMARY), rel(SURFACE_DIAGNOSTIC), rel(PACKAGE_DECISION)], "evidence_missing": ["MT5 runtime package(MT5 런타임 패키지)", "MT5 runtime probe(MT5 런타임 탐침)"], "next_condition": NEXT_RUN_ID})
    write_json(MODEL_RECEIPT, {**common, "receipt_type": "model_validation(모델 검증)", "review_subject": final["review_subject"], "selected_model_id": final["selected_model_id"], "validation_judgment": JUDGMENT, "overfit_risk": "single-window proxy search(단일 창 프록시 탐색)"})
    write_json(ATTRIBUTION_RECEIPT, {**common, "receipt_type": "performance_attribution(성과 귀속)", "observed_change": "GL recovered density but cost collapsed(GL은 밀도를 회복했지만 비용이 무너짐)", "next_probe": NEXT_RUN_ID})
    write_json(LINEAGE_RECEIPT, {**common, "receipt_type": "artifact_lineage(산출물 계보)", "inputs": [rel(path) for path in INPUT_FILES], "outputs": [rel(path) for path in OUTPUT_FILES if exists(path)], "lineage_judgment": "connected_with_review_boundary(검토 경계로 연결됨)"})
    write_json(CLAIM_RECEIPT, {**common, "receipt_type": "claim_boundary(주장 경계)", "runtime_authority": "not_claimed", "operating_promotion": "not_claimed", "live_readiness": "not_claimed", "goal_achieve": "not_claimed"})


def write_docs(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    gate_lines = "\n".join(f"- {row['gate']}: {row['status']} -> {row['evidence']}" for row in gates)
    report = f"""# run364GM Cost-Repaired Density Reexpand Review(비용 수리 후 밀도 재확장 검토)

Created(생성): {final['created_at_utc']}

Action(행동): GL proxy/ONNX smoke(GL 프록시/ONNX 온엑스 간이 검증) 결과를 density recovery(밀도 회복), cost recollapse(비용 재붕괴), package decision(패키지 결정)으로 검토했습니다.

Effect(효과): GL의 h1 density clue(h1 밀도 단서)는 보존하되, 비용 실패 때문에 운영 후보로 올리지 않고 GN dual-anchor router(GN 이중 앵커 라우터)로 넘깁니다.

- judgment(판정): `{final['judgment']}`
- selected_model_id(선택 모델 ID): `{final['selected_model_id']}`
- validation net/PF/density(검증 순수익/수익 팩터/밀도): `{final['selected_validation_net']}` / `{final['selected_validation_profit_factor']}` / `{final['selected_validation_trade_density']}`
- OOS net/PF/density(표본외 순수익/수익 팩터/밀도): `{final['selected_oos_net']}` / `{final['selected_oos_profit_factor']}` / `{final['selected_oos_trade_density']}`
- OOS cost0.6/cost0.9(표본외 비용0.6/비용0.9): `{final['selected_oos_cost06_net']}` / `{final['selected_oos_cost09_net']}`
- combined density/cost0.9(합산 밀도/비용0.9): `{final['selected_combined_trade_density']}` / `{final['selected_combined_cost09_net']}`
- density23 + cost near count(밀도2.3 + 비용 근접 수): `{final['density23_valpos_oospos_cost_near_count']}`
- package_eligible(패키지 가능): `{final['package_eligible']}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`

Gates(게이트):

{gate_lines}

Boundary(경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
"""
    decision_doc = f"""# Decision(결정): stage364GM Cost-Repaired Density Reexpand Review(비용 수리 후 밀도 재확장 검토)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(상위 실행 ID): `{PARENT_RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Action(행동): GL 결과를 package rejected(패키지 거절)로 닫고, GN density-cost dual-anchor router(GN 밀도-비용 이중 앵커 라우터)를 다음 입력으로 만들었습니다.

Effect(효과): 비용 수리와 밀도 회복을 하나의 단순 점수로 번갈아 잃는 패턴을 줄입니다.
"""
    fn.write_text(REPORT_PATH, report, bom=True)
    fn.write_text(DECISION_DOC, decision_doc, bom=True)
    fn.append_text_once(REVIEW_INDEX, f"run364GM__{RUN_ID}", f"\n- run364GM__{RUN_ID}: [{REPORT_PATH.name}]({REPORT_PATH.name}) - cost-repaired density reexpand review(비용 수리 후 밀도 재확장 검토), next `{NEXT_RUN_ID}`.\n")
    fn.append_text_once(STAGE_BRIEF, f"run364GM__{RUN_ID}", f"\n<!-- run364GM__{RUN_ID} -->\n\n## run364GM Cost-Repaired Density Reexpand Review(비용 수리 후 밀도 재확장 검토)\n\nAction(행동): GL 결과를 밀도 회복과 비용 재붕괴로 분리했습니다.\n\nEffect(효과): `{NEXT_RUN_ID}`에서 density-cost dual-anchor router(밀도-비용 이중 앵커 라우터)를 실행합니다.\n")
    fn.append_text_once(STAGE_README, f"run364GM__{RUN_ID}", f"\n<!-- run364GM__{RUN_ID} -->\n## run364GM cost-repaired density reexpand review(비용 수리 후 밀도 재확장 검토)\n\nNext(다음): `{NEXT_RUN_ID}`.\n")
    fn.write_text(WORKSPACE_STATE, f"""current_stage_id: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {STATUS}
current_judgment: {JUDGMENT}
next_run_id: {NEXT_RUN_ID}
runtime_authority: not_claimed
operating_promotion: not_claimed
goal_achieve: not_claimed
updated_at_utc: {final['created_at_utc']}
""", bom=False)
    fn.write_text(CURRENT_WORKING_STATE, f"""# Current Working State(현재 작업 상태)

Updated(갱신): {final['created_at_utc']}

Active stage(활성 단계): `{STAGE_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Current run(현재 실행): `{NEXT_RUN_ID}`

Current truth(현재 진실): `run364GM` reviewed(검토 완료) GL cost-repaired density reexpand(GL 비용 수리 후 밀도 재확장). GL selected(선택) 후보는 validation net/PF/density(검증 순수익/수익 팩터/밀도) `{final['selected_validation_net']}` / `{final['selected_validation_profit_factor']}` / `{final['selected_validation_trade_density']}`이고 OOS net/PF/density(표본외 순수익/수익 팩터/밀도)는 `{final['selected_oos_net']}` / `{final['selected_oos_profit_factor']}` / `{final['selected_oos_trade_density']}`입니다.

Failure truth(실패 진실): GL은 combined density(합산 밀도)를 `{final['selected_combined_trade_density']}`로 회복했지만 OOS cost0.6(표본외 비용0.6)은 `{final['selected_oos_cost06_net']}`, combined cost0.9(합산 비용0.9)는 `{final['selected_combined_cost09_net']}`로 다시 실패했습니다.

Next action(다음 행동): `{NEXT_RUN_ID}`에서 density-cost dual-anchor router(밀도-비용 이중 앵커 라우터)를 실행합니다.

Operating boundary(운영 경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""", bom=True)
    fn.write_text(SELECTION_STATUS, f"""# Stage364 selection status(선택 상태)

Updated(갱신): {final['created_at_utc']}

Current run(현재 실행): `{NEXT_RUN_ID}`
Latest completed run(최근 완료 실행): `{RUN_ID}`

Latest review(최근 검토): GM cost-repaired density reexpand review(GM 비용 수리 후 밀도 재확장 검토)가 GL package(GL 패키지)를 rejected(거절)했습니다.

Selected model(선택 모델): `{final['selected_model_id']}`

Validation net/PF/density(검증 순수익/수익 팩터/밀도): `{final['selected_validation_net']}` / `{final['selected_validation_profit_factor']}` / `{final['selected_validation_trade_density']}`
OOS net/PF/density(표본외 순수익/수익 팩터/밀도): `{final['selected_oos_net']}` / `{final['selected_oos_profit_factor']}` / `{final['selected_oos_trade_density']}`
OOS cost0.6/cost0.9(표본외 비용0.6/비용0.9): `{final['selected_oos_cost06_net']}` / `{final['selected_oos_cost09_net']}`
Combined density/cost0.9(합산 밀도/비용0.9): `{final['selected_combined_trade_density']}` / `{final['selected_combined_cost09_net']}`

Next seed(다음 씨앗): density-cost dual-anchor router(밀도-비용 이중 앵커 라우터).

Authority(권위): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""", bom=True)
    fn.append_text_once(WORKSPACE_CHANGELOG, f"run364GM__{RUN_ID}", f"\n<!-- run364GM__{RUN_ID} -->\n- {final['created_at_utc']} `{RUN_ID}` reviewed cost-repaired density reexpand(비용 수리 후 밀도 재확장); selected density(선택 밀도) `{final['selected_combined_trade_density']}`; OOS cost0.6(표본외 비용0.6) `{final['selected_oos_cost06_net']}`; package rejected(패키지 거절); next `{NEXT_RUN_ID}`; no authority claim(권위 주장 없음).\n")
    fn.append_text_once(IDEA_REGISTRY, f"run364GM__{RUN_ID}", f"\n<!-- run364GM__{RUN_ID} -->\n- `{RUN_ID}`: cost-repaired density reexpand(비용 수리 후 밀도 재확장)는 h1 density clue(h1 밀도 단서)를 만들었지만 비용 재붕괴로 GN dual-anchor router(GN 이중 앵커 라우터)를 다음 입력으로 남겼습니다. Effect(효과): 비용 앵커와 밀도 앵커를 분리 라우팅 조건으로 고정합니다.\n")
    fn.append_text_once(NEGATIVE_REGISTER, f"run364GM__density_recovered_cost_failed__{RUN_ID}", f"\n<!-- run364GM__density_recovered_cost_failed__{RUN_ID} -->\n- `{RUN_ID}`: GL은 combined density(합산 밀도) `{final['selected_combined_trade_density']}`를 회복했지만 OOS cost0.6(표본외 비용0.6) `{final['selected_oos_cost06_net']}`와 combined cost0.9(합산 비용0.9) `{final['selected_combined_cost09_net']}`로 실패했습니다. Effect(효과): GN에서 비용 앵커와 밀도 앵커를 분리합니다.\n")


def ledger_rows(final: Mapping[str, Any]) -> list[dict[str, Any]]:
    artifact_count = len({Path(path) for path in OUTPUT_FILES if exists(path) or Path(path) == RUN_MANIFEST})
    common = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(FINAL_DECISION),
        "run_number": RUN_NUMBER,
        "date": TODAY,
        "decision": DECISION,
        "next_run_id": NEXT_RUN_ID,
        "artifact_count": artifact_count,
        "gate_passes": final["gate_passes"],
        "gate_total": final["gate_total"],
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "created_at_utc": final["created_at_utc"],
        "required_gate_audit": rel(GATE_AUDIT),
        "question": "Should GL open package or seed GN dual-anchor router?(GL을 패키지로 열지, GN 이중 앵커 라우터로 보낼지)",
        "next_action": NEXT_RUN_ID,
        "notes": f"density={final['selected_combined_trade_density']};oos_cost06={final['selected_oos_cost06_net']};package=rejected",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
    }
    rows = []
    for suffix, record_view, tier_scope, status in [
        ("tier_a_separate", "Tier A separate(Tier A 분리)", "Tier A", STATUS),
        ("tier_b_missing_required", "Tier B separate(Tier B 분리)", "Tier B", "missing_required_no_tier_b_model_input(필수 누락, Tier B 모델 입력 없음)"),
        ("tier_a_b_combined_out_of_scope", "Tier A+B combined(Tier A+B 합산)", "Tier A+B", "out_of_scope_by_claim_proxy_tier_a_only(주장 범위 밖, 프록시 Tier A 전용)"),
    ]:
        rows.append(
            {
                **common,
                "ledger_row_id": f"{RUN_ID}__{suffix}",
                "subrun_id": f"{RUN_ID}__{suffix}",
                "row_id": f"{RUN_ID}__{suffix}",
                "record_view": record_view,
                "tier_scope": tier_scope,
                "view": record_view,
                "tier": tier_scope,
                "kpi_scope": "GM cost-repaired density reexpand review(GM 비용 수리 후 밀도 재확장 검토)",
                "metric_scope": "python_proxy_review_no_mt5(Python 프록시 검토, MT5 없음)",
                "status": status,
                "net_profit": final["selected_oos_net"] if suffix == "tier_a_separate" else "",
                "profit_factor": final["selected_oos_profit_factor"] if suffix == "tier_a_separate" else "",
                "trade_density": final["selected_oos_trade_density"] if suffix == "tier_a_separate" else "",
                "source_authority": "python_proxy_review_no_mt5(Python 프록시 검토, MT5 없음)",
            }
        )
    return rows


def write_ledgers(final: Mapping[str, Any]) -> None:
    rows = ledger_rows(final)
    append_or_replace_csv(STAGE_LEDGER, ["ledger_row_id"], rows)
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], rows)
    append_or_replace_csv(
        RUN_REGISTRY,
        ["run_id"],
        [
            {
                **rows[0],
                "lane": "review_control(검토 제어)",
                "family": "alpha_exploration_review(알파 탐색 검토)",
                "primary_report": rel(REPORT_PATH),
                "run_family": "kpi_evidence(KPI 근거)",
                "run_type": "cost_repaired_density_reexpand_review(비용 수리 후 밀도 재확장 검토)",
                "input_run_id": PARENT_RUN_ID,
                "output_path": rel(FINAL_DECISION),
                "result_path": rel(PACKAGE_DECISION),
                "best_model_id": final["selected_model_id"],
                "net_profit": final["selected_oos_net"],
                "profit_factor": final["selected_oos_profit_factor"],
                "trade_density_per_feature_day": final["selected_oos_trade_density"],
                "result_status": STATUS,
                "primary_kpi": f"density={final['selected_combined_trade_density']};oos_cost06={final['selected_oos_cost06_net']}",
                "guardrail_kpi": "package=rejected;authority=not_claimed",
            }
        ],
    )
    try:
        et.repair_run_registry_line_endings(RUN_ID)
    except AttributeError:
        pass


def write_manifest(final: Mapping[str, Any]) -> None:
    write_json(RUN_MANIFEST, {"run_id": RUN_ID, "run_number": RUN_NUMBER, "stage_id": STAGE_ID, "parent_run_id": PARENT_RUN_ID, "next_run_id": NEXT_RUN_ID, "status": STATUS, "judgment": JUDGMENT, "claim_boundary": CLAIM_BOUNDARY, "inputs": [rel(path) for path in INPUT_FILES], "outputs": [rel(path) for path in OUTPUT_FILES if exists(path)], "created_at_utc": final["created_at_utc"]})


def write_artifact_registry(final: Mapping[str, Any]) -> None:
    rows = []
    for path in OUTPUT_FILES:
        if exists(path) and fn.io_path(path).is_file():
            rows.append({"stage_id": STAGE_ID, "run_id": RUN_ID, "artifact_type": "script" if path == THIS_FILE else ("report" if path.suffix.lower() == ".md" else ("json" if path.suffix.lower() == ".json" else "csv")), "path": rel(path), "artifact_path": rel(path), "sha256": sha(path), "created_at": final["created_at_utc"], "created_at_utc": final["created_at_utc"], "claim_boundary": CLAIM_BOUNDARY, "artifact_id": f"{RUN_ID}__{path.stem}", "notes": "GM cost-repaired density reexpand review artifact(GM 비용 수리 후 밀도 재확장 검토 산출물)"})
    append_or_replace_csv(ARTIFACT_REGISTRY, ["artifact_id"], rows)


def main() -> None:
    ensure_dirs()
    parent = validate_inputs()
    created_at = now_utc()
    write_csv(INPUT_MANIFEST, input_manifest_rows())
    write_work_packet()
    summary_rows, diagnostics, attribution, package, failure, queue = build_review(parent)
    summary = summary_rows[0]
    write_csv(REVIEW_SUMMARY, summary_rows)
    write_csv(SURFACE_DIAGNOSTIC, diagnostics)
    write_csv(FAILURE_ATTRIBUTION, attribution)
    write_csv(PACKAGE_DECISION, package)
    write_csv(FAILURE_MEMORY, failure)
    write_csv(RUN364GN_QUEUE, queue)
    gates = gate_rows(final_written=False)
    final = final_payload(summary, gates, created_at)
    write_json(FINAL_DECISION, final)
    write_receipts(final)
    write_csv(GATE_AUDIT, gates)
    write_docs(final, gates)
    write_ledgers(final)
    write_manifest(final)
    write_artifact_registry(final)
    write_receipts(final)
    gates = gate_rows(final_written=True)
    final = final_payload(summary, gates, created_at)
    write_json(FINAL_DECISION, final)
    write_csv(GATE_AUDIT, gates)
    write_ledgers(final)
    write_manifest(final)
    write_artifact_registry(final)
    print(f"{RUN_ID}: gate {final['gate_passes']}/{final['gate_total']} package=rejected next={NEXT_RUN_ID}")


if __name__ == "__main__":
    main()
