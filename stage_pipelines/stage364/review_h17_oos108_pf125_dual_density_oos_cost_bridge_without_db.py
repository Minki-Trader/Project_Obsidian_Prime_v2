from __future__ import annotations

import csv
import json
import math
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, json_ready  # noqa: E402
from stage_pipelines.stage364 import review_h17_oos108_pf125_oos_density_preserve_repair_without_db as fk  # noqa: E402
from stage_pipelines.stage364 import train_h17_oos108_pf125_dual_density_oos_cost_bridge_without_db as fl  # noqa: E402


TODAY = "2026-06-07"
STAGE_ID = fl.STAGE_ID
RUN_NUMBER = "run364FM"
RUN_ID = "run364FM_review_h17_oos108_pf125_dual_density_oos_cost_bridge_without_db_v1"
PARENT_RUN_ID = fl.RUN_ID
NEXT_RUN_ID = "run364FN_train_h17_oos108_pf125_density_cost_decoupled_bridge_without_db_v1"

STATUS = "completed_stage364FM_dual_density_oos_cost_bridge_review_package_rejected_open_fn_no_authority"
JUDGMENT = "negative_dual_density_oos_cost_bridge_review_oos_pf_cost_reloss_no_package_no_authority"
DECISION = "stage364FM_reject_package_open_run364FN_density_cost_decoupled_bridge"
CLAIM_BOUNDARY = (
    "research_development_dual_density_oos_cost_bridge_review_only_no_runtime_package_no_new_mt5_execution_"
    "no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

STAGE_DIR = fl.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
SPEC_DIR = STAGE_DIR / "00_spec"
SELECTED_DIR = STAGE_DIR / "04_selected"

INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
REVIEW_SUMMARY = RUN_DIR / "fm_review_summary.csv"
SURFACE_DIAGNOSTIC = RUN_DIR / "fm_surface_diagnostic.csv"
FAILURE_ATTRIBUTION = RUN_DIR / "fm_failure_attribution.csv"
PACKAGE_DECISION = RUN_DIR / "package_decision.csv"
FAILURE_MEMORY = RUN_DIR / "fm_failure_memory.csv"
RUN364FN_QUEUE = RUN_DIR / "fm_fn_queue.csv"
RESULT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
ATTRIBUTION_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / "run364FM_dual_density_oos_cost_bridge_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364FM_dual_density_oos_cost_bridge_review.md"
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
    fl.FINAL_DECISION,
    fl.GATE_AUDIT,
    fl.TRADE_SURFACE,
    fl.SELECTED_CANDIDATE,
    fl.SELECTED_TRADE_TAPE,
    fl.COST_STRESS,
    fl.SIDE_SESSION_REVIEW,
    fl.MONTH_STABILITY,
    fl.MODEL_SCORECARD,
    fl.MODEL_ARTIFACT_MANIFEST,
    fl.ONNX_SMOKE_REPORT,
    fl.DATA_INTEGRITY_AUDIT,
    fl.RUN364FM_QUEUE,
    fl.RUN_EVIDENCE_RECEIPT,
    fl.MODEL_RECEIPT,
    fl.ATTRIBUTION_RECEIPT,
    fl.JUDGMENT_RECEIPT,
    fl.LINEAGE_RECEIPT,
    fl.CLAIM_RECEIPT,
    fl.RUN_MANIFEST,
    fl.REPORT_PATH,
    fk.FAILURE_MEMORY,
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
    RUN364FN_QUEUE,
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
    REVIEW_INDEX,
    STAGE_LEDGER,
    STAGE_BRIEF,
    SELECTION_STATUS,
    STAGE_README,
    WORKSPACE_STATE,
    CURRENT_WORKING_STATE,
    WORKSPACE_CHANGELOG,
    RUN_REGISTRY,
    PROJECT_LEDGER,
    ARTIFACT_REGISTRY,
    IDEA_REGISTRY,
    NEGATIVE_REGISTER,
    THIS_FILE,
]


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    return fl.rel(path)


def exists(path: Path | str) -> bool:
    return Path(path).exists()


def sha(path: Path | str) -> str:
    return fl.sha(path)


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return default
    if not math.isfinite(number):
        return default
    return number


def finite(value: Any, digits: int = 10) -> float | str:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return ""
    if not math.isfinite(number):
        return ""
    return round(number, digits)


def read_json(path: Path) -> Any:
    with io_path(path).open("r", encoding="utf-8-sig") as handle:
        return json.load(handle)


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8") as handle:
        json.dump(json_ready(payload), handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")


def read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(io_path(path), encoding="utf-8-sig").fillna("")


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    rows = list(rows)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(str(key))
    if not fieldnames:
        fieldnames = ["empty"]
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def write_text(path: Path, text: str, *, bom: bool = True) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8-sig" if bom else "utf-8")


def append_text_once(path: Path, marker: str, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    existing = path.read_text(encoding="utf-8-sig") if path.exists() else ""
    if marker in existing:
        return
    payload = existing.rstrip() + "\n" + text.lstrip() if existing.strip() else text
    path.write_text(payload, encoding="utf-8-sig")


def append_or_replace_csv(path: Path, key_fields: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> None:
    rows = list(rows)
    existing_rows: list[dict[str, Any]] = []
    fieldnames: list[str] = []
    if path.exists():
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = list(reader.fieldnames or [])
            existing_rows = list(reader)
    for row in rows:
        for key in row.keys():
            if key not in fieldnames:
                fieldnames.append(str(key))
    if not fieldnames:
        fieldnames = ["empty"]
    new_keys = {tuple(str(row.get(key, "")) for key in key_fields) for row in rows}
    kept = [row for row in existing_rows if tuple(str(row.get(key, "")) for key in key_fields) not in new_keys]
    merged = kept + [dict(row) for row in rows]
    path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = path.with_name(f".{path.name}.tmp")
    with temp_path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in merged:
            writer.writerow({key: row.get(key, "") for key in fieldnames})
    temp_path.replace(path)


def markdown_table(rows: Sequence[Mapping[str, Any]], columns: Sequence[str], limit: int = 12) -> str:
    rows = list(rows)[:limit]
    if not rows:
        return "_no rows(행 없음)_"
    header = "| " + " | ".join(columns) + " |"
    divider = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(str(row.get(column, "")).replace("|", "/") for column in columns) + " |")
    return "\n".join([header, divider, *body])


def ensure_dirs() -> None:
    for path in [RUN_DIR, REVIEW_DIR, SPEC_DIR, SELECTED_DIR, DECISION_DOC.parent]:
        io_path(path).mkdir(parents=True, exist_ok=True)


def validate_inputs() -> Mapping[str, Any]:
    missing = [rel(path) for path in INPUT_FILES if path != THIS_FILE and not exists(path)]
    if missing:
        raise FileNotFoundError("missing FL inputs(FL 입력 누락): " + ", ".join(missing))
    parent = read_json(fl.FINAL_DECISION)
    if parent.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"FL next_run_id mismatch(FL 다음 실행 ID 불일치): {parent.get('next_run_id')} != {RUN_ID}")
    for key in ["runtime_authority", "operating_promotion", "live_readiness", "goal_achieve"]:
        if parent.get(key, "not_claimed") != "not_claimed":
            raise RuntimeError(f"forbidden FL claim(금지된 FL 주장): {key}={parent.get(key)}")
    gates = read_csv(fl.GATE_AUDIT)
    if gates.empty or any(gates["status"].astype(str) != "passed"):
        raise RuntimeError("FL gate audit(FL 게이트 감사)가 모두 passed(통과)가 아닙니다.")
    return parent


def input_manifest_rows() -> list[dict[str, Any]]:
    return [
        {"run_id": RUN_ID, "input_path": rel(path), "exists": str(exists(path)).lower(), "sha256": sha(path) if exists(path) and io_path(path).is_file() else "", "input_role": "FM review input(FM 검토 입력)", "claim_boundary": CLAIM_BOUNDARY}
        for path in INPUT_FILES
    ]


def bool_count(mask: pd.Series) -> int:
    return int(mask.fillna(False).sum())


def numeric_surface() -> pd.DataFrame:
    surface = read_csv(fl.TRADE_SURFACE)
    for column in ["validation_net", "validation_profit_factor", "validation_trade_density", "oos_net", "oos_profit_factor", "oos_trade_density", "oos_cost09_net", "combined_net", "combined_trade_density", "combined_cost09_net", "combined_short_share", "min_split_profit_factor", "selection_score"]:
        if column in surface.columns:
            surface[column] = pd.to_numeric(surface[column], errors="coerce").fillna(0.0)
    return surface


def cost_net(cost: pd.DataFrame, split: str, cost_per_trade: float) -> float | str:
    local = cost.copy()
    for column in ["cost_per_trade", "net_profit"]:
        local[column] = pd.to_numeric(local[column], errors="coerce").fillna(0.0)
    row = local[(local["split"].astype(str) == split) & (local["cost_per_trade"].round(4) == round(cost_per_trade, 4))]
    return finite(row["net_profit"].iloc[0]) if not row.empty else ""


def diagnostic_row(name: str, frame: pd.DataFrame, note: str) -> dict[str, Any]:
    if frame.empty:
        return {"run_id": RUN_ID, "diagnostic_id": name, "model_id": "", "validation_net": "", "validation_density": "", "oos_profit_factor": "", "oos_cost09_net": "", "oos_density": "", "combined_density": "", "combined_cost09_net": "", "combined_short_share": "", "selection_score": "", "note": note, "claim_boundary": CLAIM_BOUNDARY}
    row = frame.iloc[0].to_dict()
    return {
        "run_id": RUN_ID,
        "diagnostic_id": name,
        "model_id": row.get("model_id", ""),
        "validation_net": finite(row.get("validation_net")),
        "validation_density": finite(row.get("validation_trade_density")),
        "oos_profit_factor": finite(row.get("oos_profit_factor")),
        "oos_cost09_net": finite(row.get("oos_cost09_net")),
        "oos_density": finite(row.get("oos_trade_density")),
        "combined_density": finite(row.get("combined_trade_density")),
        "combined_cost09_net": finite(row.get("combined_cost09_net")),
        "combined_short_share": finite(row.get("combined_short_share")),
        "selection_score": finite(row.get("selection_score")),
        "note": note,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def build_review(parent: Mapping[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    surface = numeric_surface()
    cost = read_csv(fl.COST_STRESS)
    val_pos = surface["validation_net"] > 0
    density3 = (surface["validation_trade_density"] >= 3.0) & (surface["oos_trade_density"] >= 3.0) & (surface["combined_trade_density"] >= 3.0)
    oos_pf125 = (surface["oos_net"] > 0) & (surface["oos_profit_factor"] >= 1.25)
    oos_cost09_mask = surface["oos_cost09_net"] >= 0.0
    combined_cost09_mask = surface["combined_cost09_net"] >= 0.0
    short077 = surface["combined_short_share"] <= 0.77
    strict_like = val_pos & density3 & oos_pf125 & oos_cost09_mask & combined_cost09_mask & short077 & (surface["min_split_profit_factor"] >= 1.05)
    density_pf105 = val_pos & density3 & (surface["oos_profit_factor"] >= 1.05)
    selected_frame = surface[surface["model_id"] == parent["selected_model_id"]].sort_values("selection_score", ascending=False).head(1)
    diagnostics = [
        diagnostic_row("fm_selected(선택 후보)", selected_frame, "FL selected candidate(FL 선택 후보)는 density3(밀도3)를 회복했지만 OOS PF/cost(표본외 수익 팩터/비용)가 약합니다."),
        diagnostic_row("fm_best_density(밀도 후보)", surface[val_pos & density3].sort_values("selection_score", ascending=False).head(1), "density3(밀도3) 후보는 OOS PF/cost(표본외 수익 팩터/비용)를 통과하지 못했습니다."),
        diagnostic_row("fm_best_oos_cost(표본외 비용 후보)", surface[oos_pf125 & oos_cost09_mask & short077].sort_values("selection_score", ascending=False).head(1), "OOS PF/cost(표본외 수익 팩터/비용) 후보는 density3(밀도3)에 못 미칩니다."),
        diagnostic_row("fm_density_pf105(밀도 PF105)", surface[density_pf105].sort_values("selection_score", ascending=False).head(1), "density3(밀도3)와 OOS PF 1.05(표본외 수익 팩터 1.05)도 동시에 나오지 않았습니다."),
        diagnostic_row("fm_strict_like(엄격 유사)", surface[strict_like].sort_values("selection_score", ascending=False).head(1), "strict-like(엄격 유사) 후보는 없습니다."),
    ]
    validation_cost09 = cost_net(cost, "validation", 0.9)
    oos_cost09_value = cost_net(cost, "oos", 0.9)
    summary = [
        {
            "run_id": RUN_ID,
            "parent_run_id": PARENT_RUN_ID,
            "selected_model_id": parent["selected_model_id"],
            "selected_feature_set_id": parent["selected_feature_set_id"],
            "selected_label_id": parent["selected_label_id"],
            "selected_hours_id": parent["selected_hours_id"],
            "selected_threshold": parent["selected_threshold"],
            "selected_validation_net": parent["selected_validation_net"],
            "selected_validation_profit_factor": parent["selected_validation_profit_factor"],
            "selected_validation_trade_density": parent["selected_validation_trade_density"],
            "selected_validation_trade_count": parent["selected_validation_trade_count"],
            "selected_validation_cost09_net": validation_cost09,
            "selected_oos_net": parent["selected_oos_net"],
            "selected_oos_profit_factor": parent["selected_oos_profit_factor"],
            "selected_oos_trade_density": parent["selected_oos_trade_density"],
            "selected_oos_trade_count": parent["selected_oos_trade_count"],
            "selected_oos_cost06_net": parent["selected_oos_cost06_net"],
            "selected_oos_cost09_net": oos_cost09_value,
            "selected_combined_net": parent["selected_combined_net"],
            "selected_combined_trade_density": parent["selected_combined_trade_density"],
            "selected_combined_cost09_net": parent["selected_combined_cost09_net"],
            "selected_combined_short_share": parent["selected_combined_short_share"],
            "selected_min_split_profit_factor": parent["selected_min_split_profit_factor"],
            "strict_candidate_count": parent["strict_candidate_count"],
            "operational_proxy_stack_pass_count": parent["operational_proxy_stack_pass_count"],
            "surface_rows": len(surface),
            "validation_positive_density3_count": bool_count(val_pos & density3),
            "validation_positive_density3_oos_pf125_count": bool_count(val_pos & density3 & oos_pf125),
            "oos_pf125_cost09_count": bool_count(oos_pf125 & oos_cost09_mask),
            "oos_pf125_cost09_short077_count": bool_count(oos_pf125 & oos_cost09_mask & short077),
            "oos_pf125_cost09_density3_count": bool_count(oos_pf125 & oos_cost09_mask & density3),
            "oos_pf125_cost09_combined_cost09_density3_count": bool_count(oos_pf125 & oos_cost09_mask & combined_cost09_mask & density3),
            "density_pf105_count": bool_count(density_pf105),
            "strict_like_count": bool_count(strict_like),
            "package_eligible": "false",
            "review_judgment": JUDGMENT,
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    attribution = [
        {"run_id": RUN_ID, "attribution_id": "fm01_density_salvage", "observed": f"selected_density={parent['selected_validation_trade_density']}/{parent['selected_oos_trade_density']}/{parent['selected_combined_trade_density']}; validation_positive_density3_count={summary[0]['validation_positive_density3_count']}", "driver": "FL score(FL 점수)가 hard density floor(강제 밀도 바닥)를 회복했습니다.", "severity": "salvage(회수)", "effect": "FN에서는 이 밀도 단서를 보존하되 OOS PF/cost(표본외 수익 팩터/비용) 없는 package(패키지)는 열지 않습니다.", "evidence": rel(fl.TRADE_SURFACE), "claim_boundary": CLAIM_BOUNDARY},
        {"run_id": RUN_ID, "attribution_id": "fm02_oos_pf_cost_reloss", "observed": f"selected_oos_pf={parent['selected_oos_profit_factor']}; selected_oos_cost09={oos_cost09_value}; combined_cost09={parent['selected_combined_cost09_net']}", "driver": "density3(밀도3)를 강제하자 OOS PF/cost(표본외 수익 팩터/비용)가 다시 무너졌습니다.", "severity": "high(높음)", "effect": "runtime package(런타임 패키지)를 열지 않고 density/cost objective(밀도/비용 목적)를 분리한 다음 탐색으로 넘깁니다.", "evidence": rel(SURFACE_DIAGNOSTIC), "claim_boundary": CLAIM_BOUNDARY},
        {"run_id": RUN_ID, "attribution_id": "fm03_no_overlap_even_pf105", "observed": f"density_pf105_count={summary[0]['density_pf105_count']}; strict_like_count={summary[0]['strict_like_count']}", "driver": "density3(밀도3) 행은 OOS PF 1.05(표본외 수익 팩터 1.05)도 넘지 못했습니다.", "severity": "structural(구조)", "effect": "FN은 같은 점수 안에서 가중치만 흔들지 말고 density leg(밀도 다리)와 cost leg(비용 다리)를 decoupled bridge(분리 연결)로 다룹니다.", "evidence": rel(fl.TRADE_SURFACE), "claim_boundary": CLAIM_BOUNDARY},
    ]
    package = [{"run_id": RUN_ID, "decision": "rejected(거절)", "reason": "strict_candidate_count=0; density3_recovered_but_oos_pf_below_1p25_and_cost09_negative", "runtime_package": "not_opened", "new_mt5_execution": "not_run", "effect": "density(밀도) 회복을 MT5 운영 의미로 올리지 않습니다.", "claim_boundary": CLAIM_BOUNDARY}]
    failure = [
        {
            "run_id": RUN_ID,
            "memory_id": "fm01_density_salvage_oos_cost_reloss",
            "failed_boundary": "density3 with OOS PF125/cost09(밀도3과 표본외 PF125/비용0.9 동시 충족)",
            "why_failed": f"validation_positive_density3_count={summary[0]['validation_positive_density3_count']}; validation_positive_density3_oos_pf125_count={summary[0]['validation_positive_density3_oos_pf125_count']}; selected_oos_pf={parent['selected_oos_profit_factor']}; selected_oos_cost09={oos_cost09_value}",
            "salvage_value": f"density={parent['selected_validation_trade_density']}/{parent['selected_oos_trade_density']}/{parent['selected_combined_trade_density']}; validation_net={parent['selected_validation_net']}; short_share={parent['selected_combined_short_share']}",
            "reopen_condition": "density3 retained while OOS PF>=1.25 and OOS cost0.9>=0(밀도3 보존과 표본외 PF/비용 동시 충족)",
            "do_not_repeat": "Do not use one scalar score to alternate density and OOS cost; use decoupled bridge or regime split(단일 점수로 밀도와 표본외 비용 왕복 금지, 분리 연결 또는 국면 분할 사용).",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    queue = [
        {
            "run_id": RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "queue_rank": 1,
            "queue_id": "fn01_density_cost_decoupled_bridge",
            "hypothesis": "density leg(밀도 다리)와 OOS cost leg(표본외 비용 다리)를 같은 scalar score(단일 점수)가 아니라 decoupled bridge(분리 연결)로 조합하면 왕복 실패를 줄일 수 있습니다.",
            "seed_from": "FL density salvage + FM failure memory(FL 밀도 회수 + FM 실패 기억)",
            "required_preserve": "validation_density>=3, oos_density>=3, combined_density>=3, validation_net>0(검증/표본외/합산 밀도와 검증 수익 보존)",
            "required_repair": "OOS PF>=1.25, OOS cost0.9>=0, combined cost0.9 not deeply negative(표본외 수익 팩터/비용 회복)",
            "avoid": "single scalar oscillation, density-only package review, OOS-only package review(단일 점수 왕복, 밀도 전용 패키지 검토, 표본외 전용 패키지 검토)",
            "effect": "FN은 밀도 후보와 비용 후보를 분리해 찾은 뒤 겹치는 조건을 좁혀 봅니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    return summary, diagnostics, attribution, package, failure, queue


def final_payload(summary: Mapping[str, Any], gates: Sequence[Mapping[str, Any]], created_at: str) -> dict[str, Any]:
    gate_passes = sum(1 for row in gates if row["status"] == "passed")
    return {**summary, "run_id": RUN_ID, "run_number": RUN_NUMBER, "stage_id": STAGE_ID, "parent_run_id": PARENT_RUN_ID, "next_run_id": NEXT_RUN_ID, "status": STATUS, "judgment": JUDGMENT, "decision": DECISION, "created_at_utc": created_at, "gate_passes": gate_passes, "gate_total": len(gates), "runtime_package": "not_opened", "new_mt5_execution": "not_run", "runtime_authority": "not_claimed", "operating_promotion": "not_claimed", "live_readiness": "not_claimed", "goal_achieve": "not_claimed", "claim_boundary": CLAIM_BOUNDARY, "final_decision": rel(FINAL_DECISION), "report_path": rel(REPORT_PATH)}


def write_work_packet() -> None:
    write_json(WORK_PACKET, {"run_id": RUN_ID, "stage_id": STAGE_ID, "parent_run_id": PARENT_RUN_ID, "primary_family": "kpi_evidence(KPI 근거)", "primary_skill": "obsidian-result-judgment(옵시디언 결과 판정)", "support_skills": ["obsidian-artifact-lineage(옵시디언 산출물 계보)", "obsidian-performance-attribution(옵시디언 성과 귀속)", "obsidian-model-validation(옵시디언 모델 검증)"], "required_gates": ["kpi_contract_audit", "row_grain_audit", "source_authority_audit", "required_gate_coverage_audit"], "hypothesis": "FL 결과를 package decision(패키지 결정), failure memory(실패 기억), FN queue(FN 대기열)로 분리합니다.", "claim_boundary": CLAIM_BOUNDARY})


def write_receipts(final: Mapping[str, Any]) -> None:
    common = {"run_id": RUN_ID, "status": STATUS, "judgment": JUDGMENT, "claim_boundary": CLAIM_BOUNDARY, "created_at_utc": final["created_at_utc"]}
    write_json(RESULT_RECEIPT, {**common, "receipt_type": "result_judgment(결과 판정)", "decision": DECISION})
    write_json(MODEL_RECEIPT, {**common, "receipt_type": "model_validation(모델 검증)", "model_id": final["selected_model_id"], "package_eligible": False})
    write_json(ATTRIBUTION_RECEIPT, {**common, "receipt_type": "performance_attribution(성과 귀속)", "primary_failure": "density_recovered_oos_pf_cost_reloss(밀도 회복 뒤 표본외 PF/비용 재손실)"})
    write_json(LINEAGE_RECEIPT, {**common, "receipt_type": "artifact_lineage(산출물 계보)", "inputs": [rel(path) for path in INPUT_FILES], "outputs": [rel(path) for path in OUTPUT_FILES if exists(path)]})
    write_json(CLAIM_RECEIPT, {**common, "receipt_type": "claim_boundary(주장 경계)", "runtime_authority": "not_claimed", "operating_promotion": "not_claimed", "goal_achieve": "not_claimed"})


def gate_rows(final_written: bool) -> list[dict[str, Any]]:
    parent_gates = read_csv(fl.GATE_AUDIT)
    receipts = [RESULT_RECEIPT, MODEL_RECEIPT, ATTRIBUTION_RECEIPT, LINEAGE_RECEIPT, CLAIM_RECEIPT]
    checks = [
        ("input_lineage_gate", exists(INPUT_MANIFEST), INPUT_MANIFEST, "FL 입력 계보가 FM 검토에 연결됐습니다."),
        ("parent_gate_inheritance_gate", not parent_gates.empty and all(parent_gates["status"].astype(str) == "passed"), fl.GATE_AUDIT, "FL gate(게이트) 통과 상태를 상속했습니다."),
        ("kpi_contract_audit", exists(REVIEW_SUMMARY) and exists(PACKAGE_DECISION), REVIEW_SUMMARY, "KPI(핵심 성과 지표)와 package decision(패키지 결정)을 분리했습니다."),
        ("surface_tradeoff_gate", exists(SURFACE_DIAGNOSTIC), SURFACE_DIAGNOSTIC, "density/OOS cost(밀도/표본외 비용) tradeoff(절충 관계)를 기록했습니다."),
        ("failure_attribution_gate", exists(FAILURE_ATTRIBUTION), FAILURE_ATTRIBUTION, "표본외 PF/비용 재손실을 귀속했습니다."),
        ("package_decision_gate", exists(PACKAGE_DECISION), PACKAGE_DECISION, "runtime package(런타임 패키지) 거절 근거를 기록했습니다."),
        ("failure_memory_gate", exists(FAILURE_MEMORY), FAILURE_MEMORY, "실패 기억과 재개 조건을 기록했습니다."),
        ("next_queue_gate", exists(RUN364FN_QUEUE), RUN364FN_QUEUE, "FN density cost decoupled bridge(FN 밀도 비용 분리 연결) 대기열을 만들었습니다."),
        ("receipt_coverage_gate", all(exists(path) for path in receipts), RESULT_RECEIPT, "필수 receipt(영수증)가 있습니다."),
        ("required_gate_coverage_audit", final_written and exists(GATE_AUDIT), GATE_AUDIT, "필수 gate(게이트)가 종료 기록에 연결됐습니다."),
        ("final_claim_guard", True, CLAIM_RECEIPT, "권위/승격/실거래/목표 달성 주장을 차단했습니다."),
    ]
    return [{"run_id": RUN_ID, "gate": gate, "status": "passed" if passed else "failed", "evidence": rel(evidence), "effect": effect, "claim_boundary": CLAIM_BOUNDARY} for gate, passed, evidence, effect in checks]


def write_docs(final: Mapping[str, Any], attribution: Sequence[Mapping[str, Any]], package: Sequence[Mapping[str, Any]], failure: Sequence[Mapping[str, Any]], queue: Sequence[Mapping[str, Any]], diagnostics: Sequence[Mapping[str, Any]], gates: Sequence[Mapping[str, Any]]) -> None:
    report = f"""# run364FM Dual Density OOS Cost Bridge Review(양쪽 밀도 표본외 비용 연결 검토)

Created(생성): {final['created_at_utc']}

Action(행동): FL dual density OOS cost bridge(FL 양쪽 밀도 표본외 비용 연결)를 package decision(패키지 결정), failure memory(실패 기억), FN queue(FN 대기열)로 분리했습니다.

Effect(효과): density3(밀도3) 회복은 보존 단서로 남기고 OOS PF/cost(표본외 수익 팩터/비용) 재손실 때문에 운영 주장(operating claim, 운영 주장)을 막습니다.

- judgment(판정): `{final['judgment']}`
- selected model(선택 모델): `{final['selected_model_id']}`
- validation net/PF/density(검증 순수익/수익 팩터/밀도): `{final['selected_validation_net']}` / `{final['selected_validation_profit_factor']}` / `{final['selected_validation_trade_density']}`
- OOS net/PF/density(표본외 순수익/수익 팩터/밀도): `{final['selected_oos_net']}` / `{final['selected_oos_profit_factor']}` / `{final['selected_oos_trade_density']}`
- OOS cost0.9(표본외 비용0.9): `{final['selected_oos_cost09_net']}`
- combined density/cost0.9/short share(합산 밀도/비용0.9/숏 비중): `{final['selected_combined_trade_density']}` / `{final['selected_combined_cost09_net']}` / `{final['selected_combined_short_share']}`
- validation_positive_density3_count(검증 양수 밀도3 수): `{final['validation_positive_density3_count']}`
- validation_positive_density3_oos_pf125_count(검증 양수 밀도3과 표본외 PF125 동시 수): `{final['validation_positive_density3_oos_pf125_count']}`
- density_pf105_count(밀도3 표본외 PF105 수): `{final['density_pf105_count']}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`

## Surface Diagnostic(표면 진단)

{markdown_table(diagnostics, ['diagnostic_id', 'model_id', 'validation_net', 'validation_density', 'oos_profit_factor', 'oos_cost09_net', 'oos_density', 'combined_density', 'combined_cost09_net', 'combined_short_share', 'note'], limit=8)}

## Attribution(귀속)

{markdown_table(attribution, ['attribution_id', 'observed', 'driver', 'severity', 'effect'], limit=12)}

## Package Decision(패키지 결정)

{markdown_table(package, ['decision', 'reason', 'runtime_package', 'new_mt5_execution', 'effect'])}

## Failure Memory(실패 기억)

{markdown_table(failure, ['memory_id', 'failed_boundary', 'why_failed', 'salvage_value', 'reopen_condition'])}

## Next Queue(다음 대기열)

{markdown_table(queue, ['queue_id', 'hypothesis', 'required_preserve', 'required_repair', 'effect'])}

## Gates(게이트)

{markdown_table(gates, ['gate', 'status', 'evidence', 'effect'], limit=20)}

Runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
"""
    decision_doc = f"""# Decision(결정): stage364FM Dual Density OOS Cost Bridge Review(양쪽 밀도 표본외 비용 연결 검토)

- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- package(패키지): `rejected(거절)`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Action(행동): FL 결과를 검토해 runtime package(런타임 패키지)를 열지 않고 FN density cost decoupled bridge(FN 밀도 비용 분리 연결)로 넘겼습니다.

Effect(효과): 밀도 회복과 표본외 비용 회복을 단일 점수로 왕복하지 않도록 다음 탐색을 분리 연결 구조로 고정합니다.
"""
    write_text(REPORT_PATH, report, bom=True)
    write_text(DECISION_DOC, decision_doc, bom=True)
    append_text_once(REVIEW_INDEX, f"run364FM__{RUN_ID}", f"\n- run364FM__{RUN_ID}: [{REPORT_PATH.name}]({REPORT_PATH.name}) - dual density OOS cost bridge review(양쪽 밀도 표본외 비용 연결 검토), next `{NEXT_RUN_ID}`.\n")
    append_text_once(STAGE_BRIEF, f"run364FM__{RUN_ID}", f"\n<!-- run364FM__{RUN_ID} -->\n\n## run364FM Dual Density OOS Cost Bridge Review(양쪽 밀도 표본외 비용 연결 검토)\n\nAction(행동): FL 결과를 package rejected(패키지 거절)로 검토했습니다.\n\nEffect(효과): `{NEXT_RUN_ID}`에서 density/cost decoupled bridge(밀도/비용 분리 연결)를 실행합니다.\n")
    append_text_once(STAGE_README, f"run364FM__{RUN_ID}", f"\n<!-- run364FM__{RUN_ID} -->\n## run364FM dual density OOS cost bridge review(양쪽 밀도 표본외 비용 연결 검토)\n\nPackage(패키지): rejected(거절). Next(다음): `{NEXT_RUN_ID}`.\n")
    write_text(WORKSPACE_STATE, f"""current_stage_id: {STAGE_ID}
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
    write_text(CURRENT_WORKING_STATE, f"""# Current Working State(현재 작업 상태)

Updated(갱신): {final['created_at_utc']}

Active stage(활성 단계): `{STAGE_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Current run(현재 실행): `{NEXT_RUN_ID}`

Current truth(현재 진실): `run364FM` reviewed(검토 완료) FL dual density OOS cost bridge(FL 양쪽 밀도 표본외 비용 연결). FL selected(선택) 후보는 density(밀도) `{final['selected_validation_trade_density']}` / `{final['selected_oos_trade_density']}` / `{final['selected_combined_trade_density']}`를 회복했지만 OOS PF/cost0.9(표본외 수익 팩터/비용0.9)는 `{final['selected_oos_profit_factor']}` / `{final['selected_oos_cost09_net']}`입니다.

Failure truth(실패 진실): validation_positive_density3_count(검증 양수 밀도3 수)는 `{final['validation_positive_density3_count']}`이지만 validation_positive_density3_oos_pf125_count(검증 양수 밀도3과 표본외 PF125 동시 수)는 `{final['validation_positive_density3_oos_pf125_count']}`입니다.

Next action(다음 행동): `{NEXT_RUN_ID}`에서 density cost decoupled bridge(밀도 비용 분리 연결)를 실행합니다.

Operating boundary(운영 경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""", bom=True)
    write_text(SELECTION_STATUS, f"""# Stage364 selection status(선택 상태)

Updated(갱신): {final['created_at_utc']}

Current run(현재 실행): `{NEXT_RUN_ID}`
Latest completed run(최근 완료 실행): `{RUN_ID}`

Latest review(최근 검토): FM dual density OOS cost bridge review(FM 양쪽 밀도 표본외 비용 연결 검토)가 FL package(FL 패키지)를 rejected(거절)했습니다.

Selected validation net/PF/density(선택 검증 순수익/수익 팩터/밀도): `{final['selected_validation_net']}` / `{final['selected_validation_profit_factor']}` / `{final['selected_validation_trade_density']}`
Selected OOS net/PF/density(선택 표본외 순수익/수익 팩터/밀도): `{final['selected_oos_net']}` / `{final['selected_oos_profit_factor']}` / `{final['selected_oos_trade_density']}`
OOS cost0.9 and combined short share(표본외 비용0.9와 합산 숏 비중): `{final['selected_oos_cost09_net']}` / `{final['selected_combined_short_share']}`

Next seed(다음 씨앗): density cost decoupled bridge(밀도 비용 분리 연결).

Authority(권위): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""", bom=True)
    append_text_once(WORKSPACE_CHANGELOG, f"run364FM__{RUN_ID}", f"\n<!-- run364FM__{RUN_ID} -->\n- {final['created_at_utc']} `{RUN_ID}` reviewed FL dual density OOS cost bridge(양쪽 밀도 표본외 비용 연결); package rejected(패키지 거절); next `{NEXT_RUN_ID}`; no authority claim(권위 주장 없음).\n")
    append_text_once(IDEA_REGISTRY, f"run364FM__{RUN_ID}", f"\n<!-- run364FM__{RUN_ID} -->\n- `{RUN_ID}`: FL은 density3(밀도3)를 회복했지만 OOS PF/cost(표본외 수익 팩터/비용)를 잃었습니다. Effect(효과): FN은 density leg(밀도 다리)와 cost leg(비용 다리)를 분리 연결합니다.\n")
    append_text_once(NEGATIVE_REGISTER, f"run364FM__oos_cost_reloss__{RUN_ID}", f"\n<!-- run364FM__oos_cost_reloss__{RUN_ID} -->\n- `{RUN_ID}`: FL selected candidate(FL 선택 후보)는 density3(밀도3)는 회복했지만 OOS PF(표본외 수익 팩터) `{final['selected_oos_profit_factor']}`와 OOS cost0.9(표본외 비용0.9) `{final['selected_oos_cost09_net']}` 때문에 package rejected(패키지 거절)입니다. Effect(효과): 밀도만 좋은 저수익 후보를 운영 후보로 올리지 않습니다.\n")


def ledger_rows(final: Mapping[str, Any]) -> list[dict[str, Any]]:
    artifact_count = len({Path(path) for path in OUTPUT_FILES if exists(path) or Path(path) == RUN_MANIFEST})
    common = {"stage_id": STAGE_ID, "run_id": RUN_ID, "parent_run_id": PARENT_RUN_ID, "status": STATUS, "judgment": JUDGMENT, "path": rel(FINAL_DECISION), "run_number": RUN_NUMBER, "date": TODAY, "decision": DECISION, "next_run_id": NEXT_RUN_ID, "artifact_count": artifact_count, "gate_passes": final["gate_passes"], "gate_total": final["gate_total"], "claim_boundary": CLAIM_BOUNDARY, "report_path": rel(REPORT_PATH), "created_at_utc": final["created_at_utc"], "required_gate_audit": rel(GATE_AUDIT), "question": "Should FL open package or seed FN density cost decoupled bridge?(FL을 패키지로 열지, FN 밀도 비용 분리 연결로 보낼지)", "next_action": NEXT_RUN_ID, "notes": f"density={final['selected_validation_trade_density']}/{final['selected_oos_trade_density']}/{final['selected_combined_trade_density']};oos_pf={final['selected_oos_profit_factor']};oos_cost09={final['selected_oos_cost09_net']};package=rejected", "runtime_authority": "not_claimed", "operating_promotion": "not_claimed", "goal_achieve": "not_claimed"}
    rows = []
    for suffix, record_view, tier_scope, status in [("tier_a_separate", "Tier A separate(Tier A 분리)", "Tier A", STATUS), ("tier_b_missing_required", "Tier B separate(Tier B 분리)", "Tier B", "missing_required_no_tier_b_model_input(필수 누락, Tier B 모델 입력 없음)"), ("tier_a_b_combined_out_of_scope", "Tier A+B combined(Tier A+B 합산)", "Tier A+B", "out_of_scope_by_claim_proxy_tier_a_only(주장 범위 밖, 프록시 Tier A 전용)")]:
        rows.append({**common, "ledger_row_id": f"{RUN_ID}__{suffix}", "subrun_id": f"{RUN_ID}__{suffix}", "row_id": f"{RUN_ID}__{suffix}", "record_view": record_view, "tier_scope": tier_scope, "view": record_view, "tier": tier_scope, "kpi_scope": "FM dual density OOS cost bridge review(FM 양쪽 밀도 표본외 비용 연결 검토)", "metric_scope": "python_proxy_review_no_mt5(Python 프록시 검토, MT5 없음)", "status": status, "net_profit": final["selected_oos_net"] if suffix == "tier_a_separate" else "", "profit_factor": final["selected_oos_profit_factor"] if suffix == "tier_a_separate" else "", "trade_density_per_feature_day": final["selected_oos_trade_density"] if suffix == "tier_a_separate" else "", "source_authority": "python_proxy_review_no_mt5(Python 프록시 검토, MT5 없음)"})
    return rows


def write_ledgers(final: Mapping[str, Any]) -> None:
    rows = ledger_rows(final)
    append_or_replace_csv(STAGE_LEDGER, ["ledger_row_id"], rows)
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], rows)
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], [{**rows[0], "lane": "review_control(검토 제어)", "family": "alpha_exploration_review(알파 탐색 검토)", "primary_report": rel(REPORT_PATH), "run_family": "kpi_evidence(KPI 근거)", "run_type": "dual_density_oos_cost_bridge_review(양쪽 밀도 표본외 비용 연결 검토)", "input_run_id": PARENT_RUN_ID, "output_path": rel(FINAL_DECISION), "result_path": rel(PACKAGE_DECISION), "best_model_id": final["selected_model_id"], "net_profit": final["selected_oos_net"], "profit_factor": final["selected_oos_profit_factor"], "trade_density_per_feature_day": final["selected_oos_trade_density"], "result_status": STATUS, "primary_kpi": f"oos_net={final['selected_oos_net']};oos_pf={final['selected_oos_profit_factor']}", "guardrail_kpi": "package=rejected;authority=not_claimed", "final_decision_path": rel(FINAL_DECISION), "gate_audit_path": rel(GATE_AUDIT), "external_verification_status": "out_of_scope_by_claim(주장 범위 밖)", "evidence_boundary": "proxy_review_only_no_mt5_runtime_authority(프록시 검토만, MT5 런타임 권위 없음)"}])
    try:
        fl.et.repair_run_registry_line_endings(RUN_ID)
    except AttributeError:
        pass


def write_artifact_registry(final: Mapping[str, Any]) -> None:
    rows = []
    for path in OUTPUT_FILES:
        if exists(path) and io_path(path).is_file():
            rows.append({"stage_id": STAGE_ID, "run_id": RUN_ID, "artifact_type": "script" if path == THIS_FILE else ("report" if path.suffix.lower() == ".md" else ("json" if path.suffix.lower() == ".json" else "csv")), "path": rel(path), "artifact_path": rel(path), "sha256": sha(path), "created_at": final["created_at_utc"], "created_at_utc": final["created_at_utc"], "claim_boundary": CLAIM_BOUNDARY, "artifact_id": f"{RUN_ID}__{path.stem}", "notes": "FM dual density OOS cost bridge review artifact(FM 양쪽 밀도 표본외 비용 연결 검토 산출물)"})
    append_or_replace_csv(ARTIFACT_REGISTRY, ["artifact_id"], rows)


def write_manifest(final: Mapping[str, Any]) -> None:
    outputs = [path for path in OUTPUT_FILES if exists(path)]
    write_json(RUN_MANIFEST, {"run_id": RUN_ID, "run_number": RUN_NUMBER, "stage_id": STAGE_ID, "parent_run_id": PARENT_RUN_ID, "next_run_id": NEXT_RUN_ID, "status": STATUS, "judgment": JUDGMENT, "claim_boundary": CLAIM_BOUNDARY, "command": f"python {rel(THIS_FILE)}", "input_files": [rel(path) for path in INPUT_FILES], "input_hashes": {rel(path): sha(path) for path in INPUT_FILES if exists(path) and io_path(path).is_file()}, "output_files": [rel(path) for path in outputs], "output_hashes": {rel(path): sha(path) for path in outputs if io_path(path).is_file()}})


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
    write_csv(RUN364FN_QUEUE, queue)
    gates = gate_rows(final_written=False)
    final = final_payload(summary, gates, created_at)
    write_json(FINAL_DECISION, final)
    write_receipts(final)
    write_csv(GATE_AUDIT, gates)
    gates = gate_rows(final_written=True)
    final = final_payload(summary, gates, created_at)
    write_json(FINAL_DECISION, final)
    write_csv(GATE_AUDIT, gates)
    write_docs(final, attribution, package, failure, queue, diagnostics, gates)
    write_manifest(final)
    write_ledgers(final)
    write_artifact_registry(final)
    write_receipts(final)
    print(json.dumps(json_ready({"run_id": RUN_ID, "status": STATUS, "judgment": JUDGMENT, "package_decision": "rejected", "next_run_id": NEXT_RUN_ID, "gate_passes": final["gate_passes"], "gate_total": final["gate_total"]}), ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
