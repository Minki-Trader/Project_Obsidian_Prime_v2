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
from stage_pipelines.stage364 import review_h17_oos108_pf125_density_bridge_repair_without_db as fc  # noqa: E402
from stage_pipelines.stage364 import train_h17_oos108_pf125_short_cost09_balance_repair_without_db as fd  # noqa: E402


TODAY = "2026-06-06"
STAGE_ID = fd.STAGE_ID
RUN_NUMBER = "run364FE"
RUN_ID = "run364FE_review_h17_oos108_pf125_short_cost09_balance_repair_without_db_v1"
PARENT_RUN_ID = fd.RUN_ID
NEXT_RUN_ID = "run364FF_train_h17_oos108_pf125_density_rejoin_cost09_short_guard_without_db_v1"

STATUS = "completed_stage364FE_pf125_short_cost09_balance_review_package_rejected_open_ff_no_authority"
JUDGMENT = "negative_pf125_short_cost09_balance_review_density_reloss_no_package_no_authority"
DECISION = "stage364FE_reject_package_open_run364FF_pf125_density_rejoin_cost09_short_guard"
CLAIM_BOUNDARY = (
    "research_development_pf125_short_cost09_balance_review_only_no_runtime_package_no_new_mt5_execution_"
    "no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

STAGE_DIR = fd.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
SPEC_DIR = STAGE_DIR / "00_spec"
SELECTED_DIR = STAGE_DIR / "04_selected"

INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
REVIEW_SUMMARY = RUN_DIR / "fe_pf125_short_cost09_balance_review_summary.csv"
SURFACE_DIAGNOSTIC = RUN_DIR / "fe_surface_tradeoff_diagnostic.csv"
FAILURE_ATTRIBUTION = RUN_DIR / "fe_failure_attribution.csv"
PACKAGE_DECISION = RUN_DIR / "package_decision.csv"
FAILURE_MEMORY = RUN_DIR / "pf125_density_rejoin_failure_memory.csv"
RUN364FF_QUEUE = RUN_DIR / "run364FF_pf125_density_rejoin_cost09_short_guard_queue.csv"
RESULT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
ATTRIBUTION_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / "run364FE_pf125_short_cost09_balance_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364FE_h17_oos108_pf125_short_cost09_balance_review.md"
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
    fd.FINAL_DECISION,
    fd.GATE_AUDIT,
    fd.TRADE_SURFACE,
    fd.SELECTED_CANDIDATE,
    fd.SELECTED_TRADE_TAPE,
    fd.COST_STRESS,
    fd.SIDE_SESSION_REVIEW,
    fd.MONTH_STABILITY,
    fd.MODEL_SCORECARD,
    fd.MODEL_ARTIFACT_MANIFEST,
    fd.ONNX_SMOKE_REPORT,
    fd.DATA_INTEGRITY_AUDIT,
    fd.RUN364FE_QUEUE,
    fd.RUN_EVIDENCE_RECEIPT,
    fd.MODEL_RECEIPT,
    fd.ATTRIBUTION_RECEIPT,
    fd.JUDGMENT_RECEIPT,
    fd.LINEAGE_RECEIPT,
    fd.CLAIM_RECEIPT,
    fd.RUN_MANIFEST,
    fd.REPORT_PATH,
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
    RUN364FF_QUEUE,
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
    return fd.rel(path)


def exists(path: Path | str) -> bool:
    return Path(path).exists()


def sha(path: Path | str) -> str:
    return fd.sha(path)


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
    fc.write_csv(path, rows)


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
    return fc.markdown_table(rows, columns, limit)


def ensure_dirs() -> None:
    for path in [RUN_DIR, REVIEW_DIR, SPEC_DIR, SELECTED_DIR, DECISION_DOC.parent]:
        io_path(path).mkdir(parents=True, exist_ok=True)


def validate_inputs() -> Mapping[str, Any]:
    missing = [rel(path) for path in INPUT_FILES if path != THIS_FILE and not exists(path)]
    if missing:
        raise FileNotFoundError("missing FD inputs(FD 입력 누락): " + ", ".join(missing))
    parent = read_json(fd.FINAL_DECISION)
    if parent.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"FD next_run_id mismatch(FD 다음 실행 ID 불일치): {parent.get('next_run_id')} != {RUN_ID}")
    for key in ["runtime_authority", "operating_promotion", "live_readiness", "goal_achieve"]:
        if parent.get(key, "not_claimed") != "not_claimed":
            raise RuntimeError(f"forbidden FD claim(금지된 FD 주장): {key}={parent.get(key)}")
    gates = read_csv(fd.GATE_AUDIT)
    if gates.empty or any(gates["status"].astype(str) != "passed"):
        raise RuntimeError("FD gate audit(FD 게이트 감사)가 모두 passed(통과)가 아닙니다.")
    return parent


def input_manifest_rows() -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "input_path": rel(path),
            "exists": str(exists(path)).lower(),
            "sha256": sha(path) if exists(path) and io_path(path).is_file() else "",
            "input_role": "FE review input(FE 검토 입력)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for path in INPUT_FILES
    ]


def bool_count(mask: pd.Series) -> int:
    return int(mask.fillna(False).sum())


def load_surface() -> pd.DataFrame:
    surface = read_csv(fd.TRADE_SURFACE)
    for column in [
        "validation_net",
        "validation_profit_factor",
        "validation_trade_density",
        "oos_net",
        "oos_profit_factor",
        "oos_trade_density",
        "oos_cost09_net",
        "combined_net",
        "combined_trade_density",
        "combined_cost09_net",
        "combined_short_share",
        "min_split_profit_factor",
        "selection_score",
    ]:
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
        return {"run_id": RUN_ID, "diagnostic_id": name, "model_id": "", "validation_density": "", "oos_profit_factor": "", "oos_cost09_net": "", "combined_density": "", "combined_short_share": "", "selection_score": "", "note": note, "claim_boundary": CLAIM_BOUNDARY}
    row = frame.iloc[0].to_dict()
    return {
        "run_id": RUN_ID,
        "diagnostic_id": name,
        "model_id": row.get("model_id", ""),
        "validation_density": finite(row.get("validation_trade_density")),
        "oos_profit_factor": finite(row.get("oos_profit_factor")),
        "oos_cost09_net": finite(row.get("oos_cost09_net")),
        "combined_density": finite(row.get("combined_trade_density")),
        "combined_short_share": finite(row.get("combined_short_share")),
        "selection_score": finite(row.get("selection_score")),
        "note": note,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def build_review(parent: Mapping[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    surface = load_surface()
    cost = read_csv(fd.COST_STRESS)
    side = read_csv(fd.SIDE_SESSION_REVIEW)
    for column in ["open_hour", "trade_count", "net_profit", "profit_factor", "expectancy"]:
        if column in side.columns:
            side[column] = pd.to_numeric(side[column], errors="coerce").fillna(0.0)

    val_pos = surface["validation_net"] > 0
    oos_pos = surface["oos_net"] > 0
    density3 = (surface["validation_trade_density"] >= 3.0) & (surface["oos_trade_density"] >= 3.0) & (surface["combined_trade_density"] >= 3.0)
    oos_pf125 = oos_pos & (surface["oos_profit_factor"] >= 1.25)
    oos_cost09 = surface["oos_cost09_net"] >= 0.0
    short_ok = surface["combined_short_share"] <= 0.72
    strict_like = val_pos & density3 & oos_pf125 & oos_cost09 & short_ok & (surface["min_split_profit_factor"] >= 1.05)
    near_rejoin = val_pos & oos_pf125 & oos_cost09 & (surface["validation_trade_density"] >= 2.6) & (surface["combined_trade_density"] >= 2.8)

    selected_frame = surface[surface["model_id"] == parent["selected_model_id"]].head(1)
    diagnostics = [
        diagnostic_row("fe_selected(선택 후보)", selected_frame, "FD 선택 후보는 OOS PF/cost0.9(표본외 PF/비용0.9)를 고쳤지만 밀도가 다시 낮아졌습니다."),
        diagnostic_row("fe_best_pf_cost_short(표본외 PF/비용/숏 최고)", surface[oos_pf125 & oos_cost09 & short_ok].sort_values(["selection_score"], ascending=False).head(1), "숏 비중과 비용을 맞추면 밀도가 크게 부족합니다."),
        diagnostic_row("fe_best_density_rejoin(밀도 재결합 근접)", surface[near_rejoin].sort_values(["validation_trade_density", "selection_score"], ascending=False).head(1), "밀도 3/day(일 3회) 근처 후보는 있지만 validation density(검증 밀도)가 아직 낮습니다."),
        diagnostic_row("fe_best_strict_like(엄격 유사)", surface[strict_like].sort_values(["selection_score"], ascending=False).head(1), "모든 핵심 조건을 동시에 만족한 후보는 없습니다."),
    ]

    selected_validation_cost09 = cost_net(cost, "validation", 0.9)
    selected_oos_cost09 = cost_net(cost, "oos", 0.9)
    worst_side = side.sort_values("net_profit").head(6).to_dict("records") if not side.empty else []

    summary = [
        {
            "run_id": RUN_ID,
            "parent_run_id": PARENT_RUN_ID,
            "selected_model_id": parent["selected_model_id"],
            "selected_validation_net": parent["selected_validation_net"],
            "selected_validation_profit_factor": parent["selected_validation_profit_factor"],
            "selected_validation_trade_density": parent["selected_validation_trade_density"],
            "selected_validation_cost06_net": parent["selected_validation_cost06_net"],
            "selected_validation_cost09_net": selected_validation_cost09,
            "selected_oos_net": parent["selected_oos_net"],
            "selected_oos_profit_factor": parent["selected_oos_profit_factor"],
            "selected_oos_trade_density": parent["selected_oos_trade_density"],
            "selected_oos_cost06_net": parent["selected_oos_cost06_net"],
            "selected_oos_cost09_net": selected_oos_cost09,
            "selected_combined_net": parent["selected_combined_net"],
            "selected_combined_trade_density": parent["selected_combined_trade_density"],
            "selected_combined_cost09_net": parent["selected_combined_cost09_net"],
            "selected_combined_short_share": parent["selected_combined_short_share"],
            "selected_min_split_profit_factor": parent["selected_min_split_profit_factor"],
            "strict_candidate_count": parent["strict_candidate_count"],
            "operational_proxy_stack_pass_count": parent["operational_proxy_stack_pass_count"],
            "surface_rows": len(surface),
            "validation_positive_density3_count": bool_count(val_pos & density3),
            "oos_pf125_cost09_count": bool_count(oos_pf125 & oos_cost09),
            "oos_pf125_cost09_short_ok_count": bool_count(oos_pf125 & oos_cost09 & short_ok),
            "oos_pf125_cost09_density3_count": bool_count(oos_pf125 & oos_cost09 & density3),
            "near_density_rejoin_count": bool_count(near_rejoin),
            "strict_like_count": bool_count(strict_like),
            "package_eligible": "false",
            "review_judgment": JUDGMENT,
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]

    attribution = [
        {
            "run_id": RUN_ID,
            "attribution_id": "fe01_oos_pf_cost09_repaired",
            "observed": f"oos_pf={parent['selected_oos_profit_factor']}; oos_cost09={selected_oos_cost09}; combined_short_share={parent['selected_combined_short_share']}",
            "driver": "FD score(FD 점수)는 OOS PF/cost0.9(표본외 PF/비용0.9)와 숏 비중을 의미 있게 회복했습니다.",
            "severity": "salvage(회수)",
            "effect": "FF는 이 OOS 비용/수익 단서를 보존 조건으로 잠급니다.",
            "evidence": rel(fd.FINAL_DECISION),
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "attribution_id": "fe02_density_reloss",
            "observed": f"validation_density={parent['selected_validation_trade_density']}; combined_density={parent['selected_combined_trade_density']}",
            "driver": "숏/비용 균형을 강화하면서 validation/combined density(검증/합산 밀도)가 3/day(일 3회) 아래로 떨어졌습니다.",
            "severity": "high(높음)",
            "effect": "FF는 density rejoin(밀도 재결합)을 직접 수리합니다.",
            "evidence": rel(fd.TRADE_SURFACE),
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "attribution_id": "fe03_validation_cost_weak",
            "observed": f"validation_cost09={selected_validation_cost09}; validation_cost06={parent['selected_validation_cost06_net']}",
            "driver": "검증은 원시 net(순수익)은 양수지만 cost stress(비용 압박)에 약합니다.",
            "severity": "high(높음)",
            "effect": "FF는 validation cost(검증 비용)를 패키지 조건이 아니라 보조 벌점으로 둡니다.",
            "evidence": rel(fd.COST_STRESS),
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "attribution_id": "fe04_surface_tradeoff",
            "observed": f"oos_pf125_cost09={bool_count(oos_pf125 & oos_cost09)}; oos_pf125_cost09_short_ok={bool_count(oos_pf125 & oos_cost09 & short_ok)}; strict_like={bool_count(strict_like)}",
            "driver": "PF/cost/short(PF/비용/숏) 후보는 많지만 밀도까지 동시에 맞춘 후보는 없습니다.",
            "severity": "structural(구조)",
            "effect": "FF는 threshold relaxation(임계값 완화)보다 density rejoin with cost guard(비용 가드가 있는 밀도 재결합)를 시험합니다.",
            "evidence": rel(SURFACE_DIAGNOSTIC),
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    for rank, row in enumerate(worst_side, 1):
        attribution.append(
            {
                "run_id": RUN_ID,
                "attribution_id": f"fe_side_loss_{rank}",
                "observed": f"{row.get('split')} {row.get('direction')} hour {row.get('open_hour')} net={row.get('net_profit')} trades={row.get('trade_count')}",
                "driver": "side/session loss segment(방향/세션 손실 구간)",
                "severity": "context(문맥)",
                "effect": "FF에서 세션 재결합 후보의 벌점으로 쓰되 운영 필터로 고정하지 않습니다.",
                "evidence": rel(fd.SIDE_SESSION_REVIEW),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    package = [
        {
            "run_id": RUN_ID,
            "decision": "reject_runtime_package(런타임 패키지 거절)",
            "reason": "strict_candidate_count=0; validation_density<3; combined_density<3; validation cost stress weak(엄격 후보 없음, 검증/합산 밀도 부족, 검증 비용 압박 약함)",
            "runtime_package": "not_opened(열지 않음)",
            "new_mt5_execution": "not_run(미실행)",
            "runtime_authority": "not_claimed(주장 안 함)",
            "effect": "FD의 OOS 개선을 운영 주장으로 올리지 않습니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    failure = [
        {
            "run_id": RUN_ID,
            "memory_id": "fe01_density_rejoin_gap",
            "failed_boundary": "PF/cost/short with 3/day density(PF/비용/숏과 일 3회 밀도 동시 충족)",
            "why_failed": f"validation_density={parent['selected_validation_trade_density']}; combined_density={parent['selected_combined_trade_density']}; strict_count={parent['strict_candidate_count']}",
            "salvage_value": f"OOS PF/cost0.9/short share(표본외 PF/비용0.9/숏 비중)는 {parent['selected_oos_profit_factor']} / {selected_oos_cost09} / {parent['selected_combined_short_share']}로 개선됐습니다.",
            "reopen_condition": "preserve OOS PF>=1.25 and OOS cost0.9>=0 while validation_density>=3 and combined_density>=3(표본외 PF/비용0.9 보존과 검증/합산 밀도 3 이상)",
            "do_not_repeat": "Do not restore density by adding low-expectancy trades(저기대값 거래 추가로 밀도 회복 금지).",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    queue = [
        {
            "run_id": RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "queue_rank": 1,
            "queue_id": "ff01_pf125_density_rejoin_cost09_short_guard",
            "hypothesis": "Cost09/short guard(비용0.9/숏 가드)를 유지한 채 density rejoin score(밀도 재결합 점수)를 추가하면 FD의 OOS edge(FD 표본외 엣지)를 보존하면서 3/day(일 3회)를 회복할 수 있습니다.",
            "seed_from": "run364FD selected + FE failure memory(FE 실패 기억)",
            "required_preserve": "OOS PF>=1.25, OOS cost0.9>=0, short_share improves or <=0.77(표본외 PF/비용0.9 보존, 숏 비중 개선)",
            "required_repair": "validation_density>=3, combined_density>=3, validation_net>0(검증/합산 밀도와 검증 순수익 회복)",
            "avoid": "profit-splitting density, OOS-only selection, validation-only density(수익 쪼개기 밀도, 표본외 전용 선택, 검증 전용 밀도 금지)",
            "effect": "FF는 FD가 고친 OOS 비용/수익 단서를 유지하면서 밀도만 다시 붙입니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    return summary, diagnostics, attribution, package, failure, queue


def write_work_packet() -> None:
    write_json(
        WORK_PACKET,
        {
            "run_id": RUN_ID,
            "run_number": RUN_NUMBER,
            "stage_id": STAGE_ID,
            "work_family": "alpha_exploration_review(알파 탐색 검토)",
            "primary_skill": "obsidian-result-judgment(결과 판정)",
            "support_skills": ["obsidian-performance-attribution(성과 귀속)", "obsidian-artifact-lineage(산출물 계보)", "obsidian-model-validation(모델 검증)"],
            "required_gates": ["input_lineage_gate", "parent_gate_inheritance_gate", "kpi_contract_audit", "surface_tradeoff_gate", "failure_attribution_gate", "package_decision_gate", "failure_memory_gate", "next_queue_gate", "receipt_coverage_gate", "required_gate_coverage_audit", "final_claim_guard"],
            "claim_boundary": CLAIM_BOUNDARY,
            "effect": "FE review(FE 검토)는 FD의 OOS 회복과 밀도 재손실을 분리합니다.",
        },
    )


def final_payload(summary: Mapping[str, Any], gates: Sequence[Mapping[str, Any]], created_at: str) -> dict[str, Any]:
    gate_passes = sum(1 for row in gates if row["status"] == "passed")
    return {
        **summary,
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "created_at_utc": created_at,
        "gate_passes": gate_passes,
        "gate_total": len(gates),
        "runtime_package": "not_opened",
        "new_mt5_execution": "not_run",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "live_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "claim_boundary": CLAIM_BOUNDARY,
        "final_decision": rel(FINAL_DECISION),
        "report_path": rel(REPORT_PATH),
    }


def write_receipts(final: Mapping[str, Any]) -> None:
    common = {"run_id": RUN_ID, "status": STATUS, "judgment": JUDGMENT, "claim_boundary": CLAIM_BOUNDARY, "created_at_utc": final["created_at_utc"]}
    write_json(RESULT_RECEIPT, {**common, "receipt_type": "result_judgment(결과 판정)", "decision": DECISION})
    write_json(MODEL_RECEIPT, {**common, "receipt_type": "model_validation(모델 검증)", "model_id": final["selected_model_id"], "package_eligible": False})
    write_json(ATTRIBUTION_RECEIPT, {**common, "receipt_type": "performance_attribution(성과 귀속)", "primary_failure": "density_reloss_after_oos_cost_repair(표본외 비용 수리 후 밀도 재손실)"})
    write_json(LINEAGE_RECEIPT, {**common, "receipt_type": "artifact_lineage(산출물 계보)", "inputs": [rel(path) for path in INPUT_FILES], "outputs": [rel(path) for path in OUTPUT_FILES if exists(path)]})
    write_json(CLAIM_RECEIPT, {**common, "receipt_type": "claim_boundary(주장 경계)", "runtime_authority": "not_claimed", "operating_promotion": "not_claimed", "goal_achieve": "not_claimed"})


def gate_rows(final_written: bool) -> list[dict[str, Any]]:
    parent_gates = read_csv(fd.GATE_AUDIT)
    receipts = [RESULT_RECEIPT, MODEL_RECEIPT, ATTRIBUTION_RECEIPT, LINEAGE_RECEIPT, CLAIM_RECEIPT]
    checks = [
        ("input_lineage_gate", exists(INPUT_MANIFEST), INPUT_MANIFEST, "FD 입력 계보가 FE 검토에 연결됐습니다."),
        ("parent_gate_inheritance_gate", not parent_gates.empty and all(parent_gates["status"].astype(str) == "passed"), fd.GATE_AUDIT, "FD 게이트 통과 상태를 상속했습니다."),
        ("kpi_contract_audit", exists(REVIEW_SUMMARY) and exists(PACKAGE_DECISION), REVIEW_SUMMARY, "KPI(핵심 성과 지표)와 패키지 결정을 분리했습니다."),
        ("surface_tradeoff_gate", exists(SURFACE_DIAGNOSTIC), SURFACE_DIAGNOSTIC, "PF/비용/숏/밀도 tradeoff(상충관계)를 기록했습니다."),
        ("failure_attribution_gate", exists(FAILURE_ATTRIBUTION), FAILURE_ATTRIBUTION, "밀도 재손실을 귀속했습니다."),
        ("package_decision_gate", exists(PACKAGE_DECISION), PACKAGE_DECISION, "런타임 패키지 거절 근거를 기록했습니다."),
        ("failure_memory_gate", exists(FAILURE_MEMORY), FAILURE_MEMORY, "실패 기억과 재개 조건을 기록했습니다."),
        ("next_queue_gate", exists(RUN364FF_QUEUE), RUN364FF_QUEUE, "FF 밀도 재결합 대기열을 만들었습니다."),
        ("receipt_coverage_gate", all(exists(path) for path in receipts), RESULT_RECEIPT, "필수 receipt(영수증)가 있습니다."),
        ("required_gate_coverage_audit", final_written and exists(GATE_AUDIT), GATE_AUDIT, "필수 gate(게이트)가 종료 기록에 연결됐습니다."),
        ("final_claim_guard", True, CLAIM_RECEIPT, "권위/승격/실거래/목표 달성 주장을 차단했습니다."),
    ]
    return [{"run_id": RUN_ID, "gate": gate, "status": "passed" if passed else "failed", "evidence": rel(evidence), "effect": effect, "claim_boundary": CLAIM_BOUNDARY} for gate, passed, evidence, effect in checks]


def write_docs(final: Mapping[str, Any], attribution: Sequence[Mapping[str, Any]], package: Sequence[Mapping[str, Any]], failure: Sequence[Mapping[str, Any]], queue: Sequence[Mapping[str, Any]], diagnostics: Sequence[Mapping[str, Any]], gates: Sequence[Mapping[str, Any]]) -> None:
    report = f"""# run364FE PF125 Short/Cost09 Balance Review(PF125 숏/비용0.9 균형 검토)

Created(생성): {final['created_at_utc']}

Action(행동): FD PF125 short/cost09 balance repair(FD PF125 숏/비용0.9 균형 수리)를 package decision(패키지 결정), failure memory(실패 기억), FF queue(FF 대기열)로 분리했습니다.

Effect(효과): OOS PF/cost0.9/short(표본외 PF/비용0.9/숏) 개선은 보존하고, validation/combined density(검증/합산 밀도) 재손실은 다음 탐색의 제약으로 고정합니다.

- judgment(판정): `{final['judgment']}`
- selected model(선택 모델): `{final['selected_model_id']}`
- validation net/PF/density(검증 순수익/수익 팩터/밀도): `{final['selected_validation_net']}` / `{final['selected_validation_profit_factor']}` / `{final['selected_validation_trade_density']}`
- OOS net/PF/density(표본외 순수익/수익 팩터/밀도): `{final['selected_oos_net']}` / `{final['selected_oos_profit_factor']}` / `{final['selected_oos_trade_density']}`
- OOS cost0.6/cost0.9(표본외 비용0.6/0.9): `{final['selected_oos_cost06_net']}` / `{final['selected_oos_cost09_net']}`
- combined net/density/cost0.9/short share(합산 순수익/밀도/비용0.9/숏 비중): `{final['selected_combined_net']}` / `{final['selected_combined_trade_density']}` / `{final['selected_combined_cost09_net']}` / `{final['selected_combined_short_share']}`
- strict_candidate_count(엄격 후보 수): `{final['strict_candidate_count']}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`

## Surface Diagnostic(표면 진단)

{markdown_table(diagnostics, ['diagnostic_id', 'model_id', 'validation_density', 'oos_profit_factor', 'oos_cost09_net', 'combined_density', 'combined_short_share', 'note'], limit=8)}

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
    decision_doc = f"""# Decision(결정): stage364FE PF125 Short/Cost09 Balance Review(PF125 숏/비용0.9 균형 검토)

- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- package(패키지): `rejected(거절)`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Action(행동): FD 결과를 검토해 runtime package(런타임 패키지)를 열지 않고 FF density rejoin(FF 밀도 재결합)으로 넘겼습니다.

Effect(효과): OOS 비용/수익 회복은 보존하고 밀도 재손실만 다음 공격 대상으로 좁힙니다.
"""
    write_text(REPORT_PATH, report, bom=True)
    write_text(DECISION_DOC, decision_doc, bom=True)
    append_text_once(REVIEW_INDEX, f"run364FE__{RUN_ID}", f"\n- run364FE__{RUN_ID}: [{REPORT_PATH.name}]({REPORT_PATH.name}) - PF125 short/cost09 balance review(PF125 숏/비용0.9 균형 검토), next `{NEXT_RUN_ID}`.\n")
    append_text_once(STAGE_BRIEF, f"run364FE__{RUN_ID}", f"\n<!-- run364FE__{RUN_ID} -->\n\n## run364FE PF125 Short/Cost09 Balance Review(PF125 숏/비용0.9 균형 검토)\n\nAction(행동): FD 결과를 package rejected(패키지 거절)로 검토했습니다.\n\nEffect(효과): `{NEXT_RUN_ID}`에서 비용/숏 가드를 보존한 밀도 재결합을 다음 공격 탐색으로 엽니다.\n")
    append_text_once(STAGE_README, f"run364FE__{RUN_ID}", f"\n<!-- run364FE__{RUN_ID} -->\n## run364FE PF125 short/cost09 balance review(PF125 숏/비용0.9 균형 검토)\n\nPackage(패키지): rejected(거절). Next(다음): `{NEXT_RUN_ID}`.\n")
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

Current truth(현재 진실): `run364FE` reviewed(검토 완료) FD PF125 short/cost09 balance repair(FD PF125 숏/비용0.9 균형 수리). FD는 OOS net/PF/cost0.9(표본외 순수익/수익 팩터/비용0.9)를 `{final['selected_oos_net']}` / `{final['selected_oos_profit_factor']}` / `{final['selected_oos_cost09_net']}`로 회복했고, combined short share(합산 숏 비중)는 `{final['selected_combined_short_share']}`입니다.

Failure truth(실패 진실): validation density/combined density(검증 밀도/합산 밀도)는 `{final['selected_validation_trade_density']}` / `{final['selected_combined_trade_density']}`이고 strict candidate(엄격 후보)는 `{final['strict_candidate_count']}`개입니다.

Next action(다음 행동): `{NEXT_RUN_ID}`에서 PF125 density rejoin cost09 short guard(PF125 밀도 재결합 비용0.9 숏 가드)를 실행합니다.

Operating boundary(운영 경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""", bom=True)
    write_text(SELECTION_STATUS, f"""# Stage364 selection status(선택 상태)

Updated(갱신): {final['created_at_utc']}

Current run(현재 실행): `{NEXT_RUN_ID}`
Latest completed run(최근 완료 실행): `{RUN_ID}`

Latest review(최근 검토): FE PF125 short/cost09 balance review(FE PF125 숏/비용0.9 균형 검토)는 FD package(FD 패키지)를 rejected(거절)했습니다.

Selected validation net/PF/density(선택 검증 순수익/수익 팩터/밀도): `{final['selected_validation_net']}` / `{final['selected_validation_profit_factor']}` / `{final['selected_validation_trade_density']}`
Selected OOS net/PF/density(선택 표본외 순수익/수익 팩터/밀도): `{final['selected_oos_net']}` / `{final['selected_oos_profit_factor']}` / `{final['selected_oos_trade_density']}`
OOS cost0.9 and combined short share(표본외 비용0.9와 합산 숏 비중): `{final['selected_oos_cost09_net']}` / `{final['selected_combined_short_share']}`

Next seed(다음 씨앗): PF125 density rejoin cost09 short guard(PF125 밀도 재결합 비용0.9 숏 가드).

Authority(권위): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""", bom=True)
    append_text_once(WORKSPACE_CHANGELOG, f"run364FE__{RUN_ID}", f"\n<!-- run364FE__{RUN_ID} -->\n- {final['created_at_utc']} `{RUN_ID}` reviewed FD PF125 short/cost09 balance repair(PF125 숏/비용0.9 균형 수리); package rejected(패키지 거절); next `{NEXT_RUN_ID}`; no authority claim(권위 주장 없음).\n")
    append_text_once(IDEA_REGISTRY, f"run364FE__{RUN_ID}", f"\n<!-- run364FE__{RUN_ID} -->\n- `{RUN_ID}`: FD는 OOS PF/cost0.9/short(표본외 PF/비용0.9/숏)을 회복했지만 density(밀도)가 재손실됐습니다. Effect(효과): FF는 비용/숏 가드를 유지하면서 밀도를 다시 붙입니다.\n")
    append_text_once(NEGATIVE_REGISTER, f"run364FE__density_reloss__{RUN_ID}", f"\n<!-- run364FE__density_reloss__{RUN_ID} -->\n- `{RUN_ID}`: FD selected candidate(FD 선택 후보)는 validation/combined density(검증/합산 밀도) 재손실로 package rejected(패키지 거절)입니다. Effect(효과): 표본외 PF/비용0.9 보존과 밀도 재결합을 다음 조건으로 고정합니다.\n")


def ledger_rows(final: Mapping[str, Any]) -> list[dict[str, Any]]:
    artifact_count = len({Path(path) for path in OUTPUT_FILES if exists(path) or Path(path) == RUN_MANIFEST})
    common = {"stage_id": STAGE_ID, "run_id": RUN_ID, "parent_run_id": PARENT_RUN_ID, "status": STATUS, "judgment": JUDGMENT, "path": rel(FINAL_DECISION), "run_number": RUN_NUMBER, "date": TODAY, "decision": DECISION, "next_run_id": NEXT_RUN_ID, "artifact_count": artifact_count, "gate_passes": final["gate_passes"], "gate_total": final["gate_total"], "claim_boundary": CLAIM_BOUNDARY, "report_path": rel(REPORT_PATH), "created_at_utc": final["created_at_utc"], "required_gate_audit": rel(GATE_AUDIT), "question": "Should FD open package or seed FF density rejoin?(FD를 패키지로 열지, FF 밀도 재결합으로 보낼지)", "next_action": NEXT_RUN_ID, "notes": f"oos_pf={final['selected_oos_profit_factor']};oos_cost09={final['selected_oos_cost09_net']};validation_density={final['selected_validation_trade_density']};package=rejected", "runtime_authority": "not_claimed", "operating_promotion": "not_claimed", "goal_achieve": "not_claimed"}
    rows = []
    for suffix, record_view, tier_scope, status in [
        ("tier_a_separate", "Tier A separate(Tier A 분리)", "Tier A", STATUS),
        ("tier_b_missing_required", "Tier B separate(Tier B 분리)", "Tier B", "missing_required_no_tier_b_model_input(필수 누락, Tier B 모델 입력 없음)"),
        ("tier_a_b_combined_out_of_scope", "Tier A+B combined(Tier A+B 합산)", "Tier A+B", "out_of_scope_by_claim_proxy_tier_a_only(주장 범위 밖, 프록시 Tier A 전용)"),
    ]:
        rows.append({**common, "ledger_row_id": f"{RUN_ID}__{suffix}", "subrun_id": f"{RUN_ID}__{suffix}", "row_id": f"{RUN_ID}__{suffix}", "record_view": record_view, "tier_scope": tier_scope, "view": record_view, "tier": tier_scope, "kpi_scope": "FE PF125 short/cost09 balance review(FE PF125 숏/비용0.9 균형 검토)", "metric_scope": "python_proxy_review_no_mt5(Python 프록시 검토, MT5 없음)", "status": status, "net_profit": final["selected_oos_net"] if suffix == "tier_a_separate" else "", "profit_factor": final["selected_oos_profit_factor"] if suffix == "tier_a_separate" else "", "trade_density_per_feature_day": final["selected_oos_trade_density"] if suffix == "tier_a_separate" else "", "source_authority": "python_proxy_review_no_mt5(Python 프록시 검토, MT5 없음)"})
    return rows


def write_ledgers(final: Mapping[str, Any]) -> None:
    rows = ledger_rows(final)
    append_or_replace_csv(STAGE_LEDGER, ["ledger_row_id"], rows)
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], rows)
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], [{**rows[0], "lane": "review_control(검토 제어)", "family": "alpha_exploration_review(알파 탐색 검토)", "primary_report": rel(REPORT_PATH), "run_family": "kpi_evidence(KPI 근거)", "run_type": "pf125_short_cost09_balance_review(PF125 숏/비용0.9 균형 검토)", "input_run_id": PARENT_RUN_ID, "output_path": rel(FINAL_DECISION), "result_path": rel(PACKAGE_DECISION), "best_model_id": final["selected_model_id"], "net_profit": final["selected_oos_net"], "profit_factor": final["selected_oos_profit_factor"], "trade_density_per_feature_day": final["selected_oos_trade_density"], "result_status": STATUS, "primary_kpi": f"oos_net={final['selected_oos_net']};oos_pf={final['selected_oos_profit_factor']}", "guardrail_kpi": "package=rejected;authority=not_claimed", "final_decision_path": rel(FINAL_DECISION), "gate_audit_path": rel(GATE_AUDIT), "external_verification_status": "out_of_scope_by_claim(주장 범위 밖)", "evidence_boundary": "proxy_review_only_no_mt5_runtime_authority(프록시 검토만, MT5 런타임 권위 없음)"}])
    try:
        fd.et.repair_run_registry_line_endings(RUN_ID)
    except AttributeError:
        pass


def write_artifact_registry(final: Mapping[str, Any]) -> None:
    rows = []
    for path in OUTPUT_FILES:
        if exists(path) and io_path(path).is_file():
            rows.append({"stage_id": STAGE_ID, "run_id": RUN_ID, "artifact_type": "script" if path == THIS_FILE else ("report" if path.suffix.lower() == ".md" else ("json" if path.suffix.lower() == ".json" else "csv")), "path": rel(path), "artifact_path": rel(path), "sha256": sha(path), "created_at": final["created_at_utc"], "created_at_utc": final["created_at_utc"], "claim_boundary": CLAIM_BOUNDARY, "artifact_id": f"{RUN_ID}__{path.stem}", "notes": "FE PF125 short/cost09 balance review artifact(FE PF125 숏/비용0.9 균형 검토 산출물)"})
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
    write_csv(RUN364FF_QUEUE, queue)
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
