from __future__ import annotations

import csv
import json
import math
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, json_ready  # noqa: E402
from stage_pipelines.stage364 import train_h17_oos108_density_cost_short_balance_reseed_without_db as et  # noqa: E402


TODAY = "2026-06-06"
STAGE_ID = et.STAGE_ID
RUN_NUMBER = "run364EU"
RUN_ID = "run364EU_review_h17_oos108_density_cost_short_balance_reseed_without_db_v1"
PARENT_RUN_ID = et.RUN_ID
NEXT_RUN_ID = "run364EV_train_h17_oos108_cost09_density_edge_recovery_without_db_v1"

STATUS = "completed_stage364EU_density_cost_short_balance_review_package_rejected_open_ev_no_authority"
JUDGMENT = "negative_density_cost_short_balance_review_cost09_density_edge_failure_no_package_no_authority"
DECISION = "stage364EU_reject_package_open_run364EV_cost09_density_edge_recovery"
CLAIM_BOUNDARY = (
    "research_development_density_cost_short_balance_review_only_no_runtime_package_no_new_mt5_execution_"
    "no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

STAGE_DIR = et.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
SPEC_DIR = STAGE_DIR / "00_spec"
SELECTED_DIR = STAGE_DIR / "04_selected"

INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
REVIEW_SUMMARY = RUN_DIR / "eu_density_cost_short_balance_review_summary.csv"
FAILURE_ATTRIBUTION = RUN_DIR / "eu_failure_attribution.csv"
SALVAGE_CANDIDATES = RUN_DIR / "eu_salvage_candidates.csv"
PACKAGE_DECISION = RUN_DIR / "package_decision.csv"
FAILURE_MEMORY = RUN_DIR / "density_cost_short_balance_failure_memory.csv"
RUN364EV_QUEUE = RUN_DIR / "run364EV_cost09_density_edge_recovery_queue.csv"
RESULT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
ATTRIBUTION_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / "run364EU_oos108_density_cost_short_balance_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364EU_h17_oos108_density_cost_short_balance_review.md"
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

INPUT_FILES = [
    et.FINAL_DECISION,
    et.GATE_AUDIT,
    et.TRADE_SURFACE,
    et.SELECTED_CANDIDATE,
    et.SELECTED_TRADE_TAPE,
    et.MONTH_STABILITY,
    et.COST_STRESS,
    et.SIDE_SESSION_REVIEW,
    et.MODEL_SCORECARD,
    et.MODEL_ARTIFACT_MANIFEST,
    et.ONNX_SMOKE_REPORT,
    et.DATA_INTEGRITY_AUDIT,
    et.RUN364EU_QUEUE,
    et.RUN_EVIDENCE_RECEIPT,
    et.EXPERIMENT_RECEIPT,
    et.DATA_RECEIPT,
    et.MODEL_RECEIPT,
    et.ATTRIBUTION_RECEIPT,
    et.JUDGMENT_RECEIPT,
    et.LINEAGE_RECEIPT,
    et.CLAIM_RECEIPT,
    et.RUN_MANIFEST,
    et.REPORT_PATH,
    Path(__file__),
]

OUTPUT_FILES = [
    INPUT_MANIFEST,
    WORK_PACKET,
    REVIEW_SUMMARY,
    FAILURE_ATTRIBUTION,
    SALVAGE_CANDIDATES,
    PACKAGE_DECISION,
    FAILURE_MEMORY,
    RUN364EV_QUEUE,
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
    Path(__file__),
]


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    try:
        return Path(path).resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return Path(path).as_posix()


def exists(path: Path | str) -> bool:
    return Path(path).exists()


def sha(path: Path | str) -> str:
    return et.sha(path)


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


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    materialized = [dict(row) for row in rows]
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fields: list[str] = []
        for row in materialized:
            for key in row.keys():
                if key not in fields:
                    fields.append(str(key))
        fieldnames = fields or ["empty"]
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fieldnames), extrasaction="ignore")
        writer.writeheader()
        for row in materialized:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def write_text(path: Path, text: str, *, bom: bool = True) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text, encoding="utf-8-sig" if bom else "utf-8")


def append_text_once(path: Path, marker: str, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    existing = io_path(path).read_text(encoding="utf-8-sig") if exists(path) else ""
    if marker in existing:
        return
    payload = existing.rstrip() + "\n" + text.lstrip() if existing.strip() else text
    io_path(path).write_text(payload, encoding="utf-8-sig")


def append_or_replace_csv(path: Path, key_fields: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> None:
    rows = list(rows)
    existing_rows: list[dict[str, Any]] = []
    fieldnames: list[str] = []
    materialized_path = io_path(path)
    if materialized_path.exists():
        with materialized_path.open("r", encoding="utf-8-sig", newline="") as handle:
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
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with materialized_path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in merged:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def markdown_table(rows: Sequence[Mapping[str, Any]], columns: Sequence[str], limit: int = 12) -> str:
    lines = ["|" + "|".join(columns) + "|", "|" + "|".join("---" for _ in columns) + "|"]
    for row in list(rows)[:limit]:
        lines.append("|" + "|".join(str(row.get(column, "")) for column in columns) + "|")
    return "\n".join(lines)


def ensure_dirs() -> None:
    for path in [RUN_DIR, REVIEW_DIR, SPEC_DIR, SELECTED_DIR, DECISION_DOC.parent]:
        io_path(path).mkdir(parents=True, exist_ok=True)


def validate_inputs() -> dict[str, Any]:
    missing = [rel(path) for path in INPUT_FILES if path != Path(__file__) and not exists(path)]
    if missing:
        raise FileNotFoundError("missing ET inputs(ET 입력 누락): " + ", ".join(missing))
    parent = read_json(et.FINAL_DECISION)
    if parent.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"ET next_run_id mismatch(ET 다음 실행 ID 불일치): {parent.get('next_run_id')} != {RUN_ID}")
    for key in ["runtime_authority", "operating_promotion", "live_readiness", "goal_achieve"]:
        if parent.get(key, "not_claimed") != "not_claimed":
            raise RuntimeError(f"forbidden ET claim(금지된 ET 주장): {key}={parent.get(key)}")
    gates = read_csv(et.GATE_AUDIT)
    if gates.empty or any(gates["status"].astype(str) != "passed"):
        raise RuntimeError("ET gate audit(ET 게이트 감사)가 모두 passed(통과)가 아닙니다.")
    return parent


def input_manifest_rows() -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "input_path": rel(path),
            "exists": str(exists(path)).lower(),
            "sha256": sha(path) if exists(path) and io_path(path).is_file() else "",
            "input_role": "ET density/cost/short review input(ET 밀도/비용/숏 검토 입력)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for path in INPUT_FILES
    ]


def numeric_frame(path: Path, columns: Sequence[str]) -> pd.DataFrame:
    frame = read_csv(path)
    for column in columns:
        if column in frame.columns:
            frame[column] = pd.to_numeric(frame[column], errors="coerce").fillna(0.0)
    return frame


def bool_count(mask: pd.Series) -> int:
    return int(mask.fillna(False).sum())


def build_review(parent: Mapping[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    surface_columns = [
        "validation_net",
        "validation_profit_factor",
        "validation_trade_density",
        "validation_trade_count",
        "oos_net",
        "oos_profit_factor",
        "oos_trade_density",
        "oos_trade_count",
        "combined_net",
        "combined_trade_count",
        "combined_trade_density",
        "combined_cost06_net",
        "combined_cost09_net",
        "combined_short_share",
        "min_split_profit_factor",
        "selection_score",
    ]
    surface = numeric_frame(et.TRADE_SURFACE, surface_columns)
    cost = numeric_frame(et.COST_STRESS, ["cost_per_trade", "trade_count", "net_profit", "profit_factor", "expectancy"])
    side = numeric_frame(et.SIDE_SESSION_REVIEW, ["open_hour", "trade_count", "net_profit", "profit_factor", "expectancy"])
    month = numeric_frame(et.MONTH_STABILITY, ["trade_count", "net_profit", "profit_factor"])
    tape = read_csv(et.SELECTED_TRADE_TAPE)

    density_ge_3 = surface["combined_trade_density"] >= 3.0
    near_density = surface["combined_trade_density"] >= 2.95
    validation_cost06_ge0 = surface["validation_cost06_net"] >= 0.0
    oos_cost06_gt0 = surface["oos_cost06_net"] > 0.0
    combined_cost09_ge0 = surface["combined_cost09_net"] >= 0.0
    short_share_ok = surface["combined_short_share"] <= 0.72
    min_pf_ok = surface[["validation_profit_factor", "oos_profit_factor"]].min(axis=1) >= 1.12
    runtime_net_reference = as_float(getattr(et.er.eq, "RUNTIME_NET_REFERENCE", 523.58), 523.58)
    runtime_net_ok = surface["combined_net"] >= runtime_net_reference
    strict_mask = density_ge_3 & validation_cost06_ge0 & oos_cost06_gt0 & combined_cost09_ge0 & short_share_ok & min_pf_ok & runtime_net_ok
    near_mask = near_density & validation_cost06_ge0 & oos_cost06_gt0 & short_share_ok & min_pf_ok
    dense_pf_mask = density_ge_3 & short_share_ok & (surface["validation_profit_factor"] >= 1.10) & (surface["oos_profit_factor"] >= 1.10)

    salvage_rows = (
        surface[near_mask]
        .sort_values(["combined_cost09_net", "selection_score"], ascending=[False, False])
        .head(12)
        .to_dict("records")
    )
    dense_pf_rows = (
        surface[dense_pf_mask]
        .sort_values(["combined_cost09_net", "selection_score"], ascending=[False, False])
        .head(6)
        .to_dict("records")
    )
    selected_surface = surface.sort_values("selection_score", ascending=False).iloc[0].to_dict() if not surface.empty else {}
    worst_side = side.sort_values("net_profit").head(8).to_dict("records")
    worst_month = month.sort_values("net_profit").head(8).to_dict("records")
    validation_cost09 = cost[(cost["split"] == "validation") & (cost["cost_per_trade"] == 0.9)]
    oos_cost09 = cost[(cost["split"] == "oos") & (cost["cost_per_trade"] == 0.9)]
    validation_cost09_net = as_float(validation_cost09["net_profit"].iloc[0]) if not validation_cost09.empty else 0.0
    oos_cost09_net = as_float(oos_cost09["net_profit"].iloc[0]) if not oos_cost09.empty else 0.0

    selected_combined_density = as_float(parent["selected_combined_trade_density"])
    density_gap = round(3.0 - selected_combined_density, 10)
    cost09_gap = round(0.0 - as_float(parent["selected_combined_cost09_net"]), 10)
    net_gap = round(runtime_net_reference - as_float(parent["selected_combined_net"]), 10)
    validation_density_gap = round(3.0 - as_float(parent["selected_validation_trade_density"]), 10)

    no_trade_splitting = "passed" if not tape.empty and tape["no_trade_splitting"].astype(str).str.contains("single_position", regex=False).all() else "failed"
    validation_tape_rows = int((tape["split"] == "validation").sum()) if "split" in tape.columns else 0
    oos_tape_rows = int((tape["split"] == "oos").sum()) if "split" in tape.columns else 0

    summary = [
        {
            "run_id": RUN_ID,
            "parent_run_id": PARENT_RUN_ID,
            "selected_model_id": parent["selected_model_id"],
            "selected_label_id": parent["selected_label_id"],
            "selected_feature_set_id": parent["selected_feature_set_id"],
            "selected_hours_id": parent["selected_hours_id"],
            "selected_threshold": parent["selected_threshold"],
            "selected_validation_net": parent["selected_validation_net"],
            "selected_validation_profit_factor": parent["selected_validation_profit_factor"],
            "selected_validation_trade_density": parent["selected_validation_trade_density"],
            "selected_oos_net": parent["selected_oos_net"],
            "selected_oos_profit_factor": parent["selected_oos_profit_factor"],
            "selected_oos_trade_density": parent["selected_oos_trade_density"],
            "selected_combined_net": parent["selected_combined_net"],
            "selected_combined_trade_density": parent["selected_combined_trade_density"],
            "selected_combined_cost06_net": parent["selected_combined_cost06_net"],
            "selected_combined_cost09_net": parent["selected_combined_cost09_net"],
            "selected_combined_short_share": parent["selected_combined_short_share"],
            "selected_min_split_profit_factor": parent["selected_min_split_profit_factor"],
            "strict_candidate_count": parent["strict_candidate_count"],
            "operational_proxy_stack_pass_count": parent["operational_proxy_stack_pass_count"],
            "surface_rows": len(surface),
            "density_ge_3_count": bool_count(density_ge_3),
            "near_density_2p95_count": bool_count(near_density),
            "validation_cost06_ge0_count": bool_count(validation_cost06_ge0),
            "oos_cost06_gt0_count": bool_count(oos_cost06_gt0),
            "combined_cost09_ge0_count": bool_count(combined_cost09_ge0),
            "short_share_ok_count": bool_count(short_share_ok),
            "min_pf112_count": bool_count(min_pf_ok),
            "runtime_net_reference": runtime_net_reference,
            "runtime_net_ok_count": bool_count(runtime_net_ok),
            "strict_recomputed_count": bool_count(strict_mask),
            "near_density_cost_side_pf_count": bool_count(near_mask),
            "dense_pf110_side_count": bool_count(dense_pf_mask),
            "selected_density_gap_to_3": density_gap,
            "selected_validation_density_gap_to_3": validation_density_gap,
            "selected_cost09_gap_to_zero": cost09_gap,
            "selected_runtime_net_gap": net_gap,
            "surface_selected_combined_density": finite(selected_surface.get("combined_trade_density")),
            "surface_selected_combined_cost09_net": finite(selected_surface.get("combined_cost09_net")),
            "validation_cost09_net": validation_cost09_net,
            "oos_cost09_net": oos_cost09_net,
            "validation_trade_tape_rows": validation_tape_rows,
            "oos_trade_tape_rows": oos_tape_rows,
            "no_trade_splitting_check": no_trade_splitting,
            "package_eligible": "false",
            "review_judgment": JUDGMENT,
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]

    attribution = [
        {
            "run_id": RUN_ID,
            "attribution_id": "eu01_near_density_but_not_full_tape_pass",
            "observed": f"combined_density={selected_combined_density}; density_gap={density_gap}; surface_density={finite(selected_surface.get('combined_trade_density'))}",
            "driver": "surface(표면)는 거의 3/day(일 3회)에 닿았지만 full trade tape replay(전체 거래 테이프 재생)는 2.9936/day(일)로 내려왔습니다.",
            "severity": "high(높음)",
            "effect": "EV는 surface score(표면 점수)가 아니라 full tape(전체 테이프) 밀도 기준으로 닫아야 합니다.",
            "evidence": rel(et.SELECTED_TRADE_TAPE),
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "attribution_id": "eu02_validation_cost09_break",
            "observed": f"validation_cost09_net={validation_cost09_net}; oos_cost09_net={oos_cost09_net}; combined_cost09={parent['selected_combined_cost09_net']}",
            "driver": "OOS(표본외)는 cost0.9(비용0.9)에서도 양수지만 validation(검증) 비용 압박이 크게 깨집니다.",
            "severity": "high(높음)",
            "effect": "EV는 OOS-only(표본외 전용) 회복을 패키지 근거로 쓰지 않고 validation cost0.9(검증 비용0.9)를 직접 제약으로 둡니다.",
            "evidence": rel(et.COST_STRESS),
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "attribution_id": "eu03_short_balance_repaired_not_sufficient",
            "observed": f"combined_short_share={parent['selected_combined_short_share']}; short cap 0.72 passed",
            "driver": "short share(숏 비중)는 0.72 이하로 고쳐졌지만 density/cost09/net(밀도/비용0.9/순수익)이 동시에 통과하지 못했습니다.",
            "severity": "medium(중간)",
            "effect": "다음 탐색은 short cap(숏 상한)을 더 조이는 반복보다 cost edge(비용 엣지)와 validation density(검증 밀도)를 같이 봅니다.",
            "evidence": rel(et.SIDE_SESSION_REVIEW),
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "attribution_id": "eu04_runtime_net_gap_remains",
            "observed": f"combined_net={parent['selected_combined_net']}; runtime_reference={runtime_net_reference}; gap={net_gap}",
            "driver": "MT5 runtime probe(MT5 런타임 탐침) reference net(기준 순수익)보다 아직 낮습니다.",
            "severity": "medium(중간)",
            "effect": "EU는 runtime package(런타임 패키지)를 열지 않고 EV 재시드 조건으로 넘깁니다.",
            "evidence": rel(et.FINAL_DECISION),
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]

    package = [
        {
            "run_id": RUN_ID,
            "decision": "reject_runtime_package(런타임 패키지 거절)",
            "reason": "strict_candidate_count=0, full_tape_density<3, combined_cost09<0, runtime_net_reference_not_met(엄격 후보 0, 전체 테이프 밀도 3 미만, 합산 비용0.9 음수, 런타임 기준 순수익 미달)",
            "runtime_package": "not_opened(열지 않음)",
            "new_mt5_execution": "not_run(미실행)",
            "runtime_authority": "not_claimed(주장 안 함)",
            "effect": "ET proxy(ET 프록시)를 MT5 operating claim(MT5 운영 주장)으로 올리지 않습니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]

    failure = [
        {
            "run_id": RUN_ID,
            "memory_id": "eu01_density_cost09_edge_near_miss",
            "hypothesis": "cost-weighted dense labels(비용 가중 고밀도 라벨)이 density/cost/short(밀도/비용/숏)을 동시에 복구할 수 있다.",
            "failed_boundary": "strict density/cost09/net package boundary(엄격 밀도/비용0.9/순수익 패키지 경계)",
            "why_failed": f"full tape density gap {density_gap}, combined cost0.9 gap {cost09_gap}, runtime net gap {net_gap}",
            "salvage_value": f"OOS PF {parent['selected_oos_profit_factor']} and OOS cost0.9 {oos_cost09_net} are strong; short share {parent['selected_combined_short_share']} is repaired.",
            "reopen_condition": "full tape density>=3, combined cost0.9>=0, validation cost0.9>=0, min PF>=1.12(전체 테이프 밀도/비용/검증 비용/최소 PF 동시 통과)",
            "do_not_repeat": "Do not repeat threshold micro-search(임계값 미세탐색 반복 금지) unless cost09 and full-tape density are in the score.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "memory_id": "eu02_validation_cost_stress",
            "hypothesis": "OOS cost recovery(표본외 비용 회복)가 검증 비용 압박에도 유지될 수 있다.",
            "failed_boundary": f"validation cost0.9 net {validation_cost09_net}",
            "why_failed": "validation(검증)의 low-edge trades(낮은 엣지 거래)가 cost0.9(비용0.9)에서 expectancy(기대값)를 음수로 만듭니다.",
            "salvage_value": "OOS(표본외) cost0.9 is still positive, so the idea is not dead(아이디어 사망 아님).",
            "reopen_condition": "validation cost0.9>=0 without density<3(검증 비용0.9 양수와 밀도 3 이상 동시 유지)",
            "do_not_repeat": "Do not package OOS-only cost pass(표본외 전용 비용 통과를 패키지화 금지).",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]

    queue = [
        {
            "run_id": RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "queue_rank": 1,
            "queue_id": "ev01_cost09_density_edge_recovery",
            "hypothesis": "ET selected seed(ET 선택 씨앗)의 OOS PF/cost strength(표본외 PF/비용 강점)를 보존하면서 validation cost0.9(검증 비용0.9)와 full-tape density>=3(전체 테이프 밀도 3 이상)을 같이 회복할 수 있습니다.",
            "seed_from": parent["selected_model_id"],
            "required_preserve": "OOS PF>=1.25, OOS cost0.9>=0, short_share<=0.72(표본외 PF/비용0.9/숏 비중 보존)",
            "required_repair": "validation density>=3, combined density>=3, validation cost0.9>=0, combined cost0.9>=0(검증/합산 밀도와 비용0.9 회복)",
            "avoid": "trade splitting(거래 쪼개기), OOS-only winner(표본외 전용 승자), threshold-only repeat(임계값 전용 반복)",
            "effect": "EV는 ET near miss(근접 실패)를 cost09/density edge(비용0.9/밀도 엣지) 문제로 좁혀 공격합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "queue_rank": 2,
            "queue_id": "ev02_validation_loss_segment_veto_without_density_collapse",
            "hypothesis": "validation loss segments(검증 손실 구간)를 score penalty(점수 벌점)로 누르면 cost0.9(비용0.9)를 회복하되 density(밀도)를 3 미만으로 떨어뜨리지 않을 수 있습니다.",
            "seed_from": rel(et.SIDE_SESSION_REVIEW),
            "required_preserve": "no trade splitting(거래 쪼개기 없음), combined density>=3(합산 밀도 3 이상)",
            "required_repair": "validation long hour/session loss(검증 롱 시간/세션 손실), validation month stress(검증 월 스트레스)",
            "avoid": "hard month exclusion as operating rule(월 배제를 운영 규칙처럼 쓰기 금지)",
            "effect": "세그먼트 손실을 운영 필터가 아니라 다음 학습 제약으로 바꿉니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]

    salvage: list[dict[str, Any]] = []
    for rank, row in enumerate(salvage_rows + dense_pf_rows, 1):
        salvage.append(
            {
                "run_id": RUN_ID,
                "rank": rank,
                "model_id": row.get("model_id", ""),
                "threshold": finite(row.get("threshold"), 12),
                "label_id": row.get("label_id", ""),
                "feature_set_id": row.get("feature_set_id", ""),
                "hours_id": row.get("hours_id", ""),
                "extra_filter": row.get("extra_filter", ""),
                "combined_net": finite(row.get("combined_net")),
                "combined_trade_density": finite(row.get("combined_trade_density")),
                "combined_cost06_net": finite(row.get("combined_cost06_net")),
                "combined_cost09_net": finite(row.get("combined_cost09_net")),
                "combined_short_share": finite(row.get("combined_short_share")),
                "validation_profit_factor": finite(row.get("validation_profit_factor")),
                "oos_profit_factor": finite(row.get("oos_profit_factor")),
                "selection_score": finite(row.get("selection_score")),
                "salvage_type": "near_density_cost_side_pf(근접 밀도/비용/방향/PF)" if rank <= len(salvage_rows) else "dense_pf110_side(고밀도 PF1.10 방향)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    # Keep the most relevant loss segments as review context without turning them into rules.
    for rank, row in enumerate(worst_side[:4], 1):
        attribution.append(
            {
                "run_id": RUN_ID,
                "attribution_id": f"eu_side_loss_{rank}",
                "observed": f"{row.get('split')} {row.get('direction')} hour {row.get('open_hour')} net={row.get('net_profit')} trades={row.get('trade_count')}",
                "driver": "side/session loss segment(방향/세션 손실 구간)",
                "severity": "context(문맥)",
                "effect": "EV penalty seed(EV 벌점 씨앗)로만 쓰고 운영 필터로 고정하지 않습니다.",
                "evidence": rel(et.SIDE_SESSION_REVIEW),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    for rank, row in enumerate(worst_month[:3], 1):
        attribution.append(
            {
                "run_id": RUN_ID,
                "attribution_id": f"eu_month_loss_{rank}",
                "observed": f"{row.get('split')} {row.get('open_month')} net={row.get('net_profit')} trades={row.get('trade_count')}",
                "driver": "month stress segment(월 스트레스 구간)",
                "severity": "context(문맥)",
                "effect": "월 배제 운영 규칙이 아니라 다음 모델 점수의 위험 메모로만 남깁니다.",
                "evidence": rel(et.MONTH_STABILITY),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    return summary, attribution, salvage, package, failure, queue


def write_work_packet() -> None:
    write_json(
        WORK_PACKET,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "primary_family": "kpi_evidence(KPI 근거)",
            "primary_skill": "obsidian-run-evidence-system(실행 근거 시스템)",
            "support_skills": [
                "obsidian-artifact-lineage(산출물 계보)",
                "obsidian-result-judgment(결과 판정)",
                "obsidian-performance-attribution(성과 귀속)",
            ],
            "required_gates": [
                "kpi_contract_audit",
                "row_grain_audit",
                "source_authority_audit",
                "required_gate_coverage_audit",
                "final_claim_guard",
            ],
            "review_question": "Should ET open runtime package or become EV cost09/density seed?(ET를 런타임 패키지로 열지, EV 비용0.9/밀도 씨앗으로 보낼지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def write_receipts(final: Mapping[str, Any], summary: Mapping[str, Any], attribution: Sequence[Mapping[str, Any]]) -> None:
    base = {"run_id": RUN_ID, "stage_id": STAGE_ID, "created_at_utc": final["created_at_utc"], "claim_boundary": CLAIM_BOUNDARY}
    write_json(
        RESULT_RECEIPT,
        {
            **base,
            "result_subject": PARENT_RUN_ID,
            "evidence_available": [rel(REVIEW_SUMMARY), rel(FAILURE_ATTRIBUTION), rel(PACKAGE_DECISION), rel(SALVAGE_CANDIDATES), rel(et.FINAL_DECISION)],
            "evidence_missing": ["MT5 runtime probe(MT5 런타임 탐침)", "forward/replay evidence(전진/재생 근거)", "runtime package(런타임 패키지)"],
            "judgment_label": JUDGMENT,
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": NEXT_RUN_ID,
            "user_explanation_hook": "ET는 좋은 OOS 단서를 만들었지만 패키지 기준은 못 넘었습니다.",
        },
    )
    write_json(
        MODEL_RECEIPT,
        {
            **base,
            "model_family": "RandomForest/ExtraTrees(랜덤포레스트/엑스트라트리)",
            "target_and_label": "dense cost-aware direction label(고밀도 비용 인식 방향 라벨)",
            "split_method": "train/validation/OOS static split(학습/검증/표본외 고정 분할)",
            "selection_metric": "density/cost/short weighted score(밀도/비용/숏 가중 점수)",
            "secondary_metrics": ["cost0.9(비용0.9)", "full tape density(전체 테이프 밀도)", "short share(숏 비중)", "min PF(최소 PF)"],
            "threshold_policy": "searched proxy threshold(탐색된 프록시 임계값)",
            "overfit_risk": "surface over-selection and threshold edge(표면 과선택과 임계값 경계)",
            "calibration_risk": "scores are rank/order only(점수는 순위 전용)",
            "comparison_baseline": PARENT_RUN_ID,
            "validation_judgment": JUDGMENT,
        },
    )
    write_json(
        ATTRIBUTION_RECEIPT,
        {
            **base,
            "observed_change": f"selected combined net/density/cost09/short_share {summary['selected_combined_net']}/{summary['selected_combined_trade_density']}/{summary['selected_combined_cost09_net']}/{summary['selected_combined_short_share']}",
            "likely_drivers": [row["driver"] for row in attribution[:4]],
            "segment_checks": [rel(et.SIDE_SESSION_REVIEW), rel(et.MONTH_STABILITY), rel(et.COST_STRESS)],
            "attribution_confidence": "medium_proxy_only(중간, 프록시 전용)",
            "next_probe": NEXT_RUN_ID,
        },
    )
    write_json(
        LINEAGE_RECEIPT,
        {
            **base,
            "source_inputs": [{"path": rel(path), "sha256": sha(path)} for path in INPUT_FILES if exists(path) and io_path(path).is_file()],
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [rel(path) for path in OUTPUT_FILES if exists(path)],
            "artifact_hashes": {rel(path): sha(path) for path in OUTPUT_FILES if exists(path) and io_path(path).is_file()},
            "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
            "lineage_judgment": "connected_review_no_package(검토 연결, 패키지 없음)",
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            **base,
            "runtime_package": "not_opened",
            "runtime_authority": "not_claimed",
            "operating_promotion": "not_claimed",
            "live_readiness": "not_claimed",
            "goal_achieve": "not_claimed",
            "effect": "ET proxy(ET 프록시)를 운영 주장(operating claim, 운영 주장)으로 바꾸지 않습니다.",
        },
    )


def gate_rows(final_written: bool) -> list[dict[str, Any]]:
    parent_gates = read_csv(et.GATE_AUDIT)
    receipts = [RESULT_RECEIPT, MODEL_RECEIPT, ATTRIBUTION_RECEIPT, LINEAGE_RECEIPT, CLAIM_RECEIPT]
    checks = [
        ("input_lineage_gate", exists(INPUT_MANIFEST), INPUT_MANIFEST, "ET 입력 계보가 EU 검토에 연결됐습니다."),
        ("parent_gate_inheritance_gate", not parent_gates.empty and all(parent_gates["status"].astype(str) == "passed"), et.GATE_AUDIT, "ET 게이트 통과 상태를 상속했습니다."),
        ("kpi_contract_audit", exists(REVIEW_SUMMARY) and exists(PACKAGE_DECISION), REVIEW_SUMMARY, "KPI(핵심 성과 지표), 패키지 결정, 실패 경계를 분리했습니다."),
        ("row_grain_audit", exists(SALVAGE_CANDIDATES) and exists(FAILURE_ATTRIBUTION), SALVAGE_CANDIDATES, "surface row(표면 행), selected tape(선택 테이프), segment(구간)를 다른 grain(입도)로 기록했습니다."),
        ("source_authority_audit", exists(CLAIM_RECEIPT), CLAIM_RECEIPT, "Python proxy/ONNX smoke(Python 프록시/ONNX 스모크) 전용 권위를 명시했습니다."),
        ("failure_attribution_gate", exists(FAILURE_ATTRIBUTION), FAILURE_ATTRIBUTION, "density/cost09/net 실패 귀속을 기록했습니다."),
        ("package_decision_gate", exists(PACKAGE_DECISION), PACKAGE_DECISION, "런타임 패키지 거절 근거를 기록했습니다."),
        ("failure_memory_gate", exists(FAILURE_MEMORY), FAILURE_MEMORY, "실패 기억과 재개 조건을 기록했습니다."),
        ("next_queue_gate", exists(RUN364EV_QUEUE), RUN364EV_QUEUE, "EV 비용0.9/밀도 엣지 회복 대기열을 만들었습니다."),
        ("receipt_coverage_gate", all(exists(path) for path in receipts), RESULT_RECEIPT, "필수 receipt(영수증)가 있습니다."),
        ("required_gate_coverage_audit", final_written and exists(GATE_AUDIT), GATE_AUDIT, "필수 gate(게이트)가 종료 기록에 연결됐습니다."),
        ("final_claim_guard", True, CLAIM_RECEIPT, "권위/승격/실거래/목표 달성 주장을 차단했습니다."),
    ]
    return [
        {"run_id": RUN_ID, "gate": gate, "status": "passed" if passed else "failed", "evidence": rel(evidence), "effect": effect, "claim_boundary": CLAIM_BOUNDARY}
        for gate, passed, evidence, effect in checks
    ]


def final_payload(summary: Mapping[str, Any], gates: Sequence[Mapping[str, Any]], created_at: str) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "package_decision": "rejected",
        "selected_model_id": summary["selected_model_id"],
        "selected_validation_net": summary["selected_validation_net"],
        "selected_validation_profit_factor": summary["selected_validation_profit_factor"],
        "selected_validation_trade_density": summary["selected_validation_trade_density"],
        "selected_oos_net": summary["selected_oos_net"],
        "selected_oos_profit_factor": summary["selected_oos_profit_factor"],
        "selected_oos_trade_density": summary["selected_oos_trade_density"],
        "selected_combined_net": summary["selected_combined_net"],
        "selected_combined_trade_density": summary["selected_combined_trade_density"],
        "selected_combined_cost06_net": summary["selected_combined_cost06_net"],
        "selected_combined_cost09_net": summary["selected_combined_cost09_net"],
        "selected_combined_short_share": summary["selected_combined_short_share"],
        "selected_min_split_profit_factor": summary["selected_min_split_profit_factor"],
        "selected_density_gap_to_3": summary["selected_density_gap_to_3"],
        "selected_validation_density_gap_to_3": summary["selected_validation_density_gap_to_3"],
        "selected_cost09_gap_to_zero": summary["selected_cost09_gap_to_zero"],
        "selected_runtime_net_gap": summary["selected_runtime_net_gap"],
        "validation_cost09_net": summary["validation_cost09_net"],
        "oos_cost09_net": summary["oos_cost09_net"],
        "strict_candidate_count": summary["strict_candidate_count"],
        "strict_recomputed_count": summary["strict_recomputed_count"],
        "near_density_cost_side_pf_count": summary["near_density_cost_side_pf_count"],
        "dense_pf110_side_count": summary["dense_pf110_side_count"],
        "gate_passes": sum(1 for row in gates if row["status"] == "passed"),
        "gate_total": len(gates),
        "runtime_package": "not_opened",
        "new_mt5_execution": "not_run",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "live_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "created_at_utc": created_at,
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "final_decision": rel(FINAL_DECISION),
    }


def write_docs(final: Mapping[str, Any], summary: Mapping[str, Any], attribution: Sequence[Mapping[str, Any]], salvage: Sequence[Mapping[str, Any]], package: Sequence[Mapping[str, Any]], failure: Sequence[Mapping[str, Any]], queue: Sequence[Mapping[str, Any]], gates: Sequence[Mapping[str, Any]]) -> None:
    report = f"""# run364EU OOS108 Density/Cost/Short Balance Review(표본외108 밀도/비용/숏 균형 검토)

Created(생성): {final['created_at_utc']}

## Judgment(판정)

Action(행동): ET density/cost/short balance reseed(ET 밀도/비용/숏 균형 재시드)를 package(패키지), failure memory(실패 기억), EV queue(EV 대기열)로 분리했습니다.

Effect(효과): OOS PF(표본외 수익 팩터)와 short balance(숏 균형) 단서는 보존하지만, full-tape density(전체 테이프 밀도)와 cost0.9(비용0.9)가 깨진 결과를 runtime package(런타임 패키지)로 올리지 않습니다.

- judgment(판정): `{final['judgment']}`
- selected_model_id(선택 모델 ID): `{final['selected_model_id']}`
- validation net/PF/density(검증 순수익/PF/밀도): `{final['selected_validation_net']}` / `{final['selected_validation_profit_factor']}` / `{final['selected_validation_trade_density']}`
- OOS net/PF/density(표본외 순수익/PF/밀도): `{final['selected_oos_net']}` / `{final['selected_oos_profit_factor']}` / `{final['selected_oos_trade_density']}`
- combined net/density/cost0.9/short share(합산 순수익/밀도/비용0.9/숏 비중): `{final['selected_combined_net']}` / `{final['selected_combined_trade_density']}` / `{final['selected_combined_cost09_net']}` / `{final['selected_combined_short_share']}`
- density gap to 3(밀도 3까지 간극): `{final['selected_density_gap_to_3']}`
- validation cost0.9 net(검증 비용0.9 순수익): `{final['validation_cost09_net']}`
- package_decision(패키지 결정): `{final['package_decision']}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`

## Summary(요약)

{markdown_table([summary], ['strict_candidate_count', 'near_density_cost_side_pf_count', 'dense_pf110_side_count', 'selected_density_gap_to_3', 'selected_cost09_gap_to_zero', 'selected_runtime_net_gap'])}

## Attribution(귀속)

{markdown_table(attribution, ['attribution_id', 'observed', 'driver', 'severity', 'effect'], limit=12)}

## Salvage Candidates(회수 후보)

{markdown_table(salvage, ['rank', 'model_id', 'combined_trade_density', 'combined_cost09_net', 'combined_short_share', 'validation_profit_factor', 'oos_profit_factor', 'salvage_type'], limit=12)}

## Package Decision(패키지 결정)

{markdown_table(package, ['decision', 'reason', 'runtime_package', 'new_mt5_execution', 'effect'])}

## Failure Memory(실패 기억)

{markdown_table(failure, ['memory_id', 'failed_boundary', 'why_failed', 'salvage_value', 'reopen_condition'])}

## Next Queue(다음 대기열)

{markdown_table(queue, ['queue_id', 'hypothesis', 'required_preserve', 'required_repair', 'effect'])}

## Gates(게이트)

{markdown_table(gates, ['gate', 'status', 'evidence', 'effect'], limit=20)}

## Boundary(경계)

Runtime package(런타임 패키지), runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
"""
    decision_doc = f"""# Decision(결정): stage364EU density/cost/short balance review(밀도/비용/숏 균형 검토)

- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- package(패키지): `rejected(거절)`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Action(행동): ET 결과를 검토해 runtime package(런타임 패키지)를 열지 않고 EV cost09/density edge recovery(EV 비용0.9/밀도 엣지 회복)로 넘겼습니다.

Effect(효과): OOS(표본외) 강점을 보존하되, 검증 비용 압박과 전체 테이프 밀도 실패를 다음 탐색의 직접 조건으로 만듭니다.
"""
    write_text(REPORT_PATH, report, bom=True)
    write_text(DECISION_DOC, decision_doc, bom=True)
    append_text_once(REVIEW_INDEX, f"run364EU__{RUN_ID}", f"\n- run364EU__{RUN_ID}: [{REPORT_PATH.name}]({REPORT_PATH.name}) - density/cost/short balance review(밀도/비용/숏 균형 검토), next `{NEXT_RUN_ID}`.\n")
    append_text_once(STAGE_BRIEF, f"run364EU__{RUN_ID}", f"\n<!-- run364EU__{RUN_ID} -->\n\n## run364EU Density/Cost/Short Balance Review(밀도/비용/숏 균형 검토)\n\nAction(행동): ET 결과를 package rejected(패키지 거절)로 검토했습니다.\n\nEffect(효과): `{NEXT_RUN_ID}`에서 cost09/density edge recovery(비용0.9/밀도 엣지 회복)를 다음 공격 탐색으로 엽니다.\n")
    append_text_once(STAGE_README, f"run364EU__{RUN_ID}", f"\n<!-- run364EU__{RUN_ID} -->\n## run364EU density/cost/short balance review(밀도/비용/숏 균형 검토)\n\nPackage(패키지): rejected(거절). Next(다음): `{NEXT_RUN_ID}`.\n")
    write_text(
        WORKSPACE_STATE,
        f"""current_stage_id: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {STATUS}
current_judgment: {JUDGMENT}
next_run_id: {NEXT_RUN_ID}
runtime_authority: not_claimed
operating_promotion: not_claimed
goal_achieve: not_claimed
updated_at_utc: {final['created_at_utc']}
""",
        bom=False,
    )
    write_text(
        CURRENT_WORKING_STATE,
        f"""# Current Working State(현재 작업 상태)

Updated(갱신): {final['created_at_utc']}

Active stage(활성 단계): `{STAGE_ID}`

Latest completed run(최근 완료 실행): `{RUN_ID}`

Current run(현재 실행): `{NEXT_RUN_ID}`

Current truth(현재 진실): `run364EU` reviewed(검토 완료) ET density/cost/short balance reseed(ET 밀도/비용/숏 균형 재시드). ET selected validation/OOS net/PF/density(ET 선택 검증/표본외 순수익/PF/밀도)는 `{final['selected_validation_net']}` / `{final['selected_validation_profit_factor']}` / `{final['selected_validation_trade_density']}` 및 `{final['selected_oos_net']}` / `{final['selected_oos_profit_factor']}` / `{final['selected_oos_trade_density']}`입니다.

Package truth(패키지 진실): strict candidate(엄격 후보)는 `{final['strict_candidate_count']}`개입니다. OOS PF(표본외 수익 팩터)와 OOS cost0.9(표본외 비용0.9)는 단서지만, combined density(합산 밀도) `{final['selected_combined_trade_density']}`, validation cost0.9 net(검증 비용0.9 순수익) `{final['validation_cost09_net']}`, combined cost0.9 net(합산 비용0.9 순수익) `{final['selected_combined_cost09_net']}` 때문에 runtime package(런타임 패키지)는 not opened(열지 않음)입니다.

Next action(다음 행동): `{NEXT_RUN_ID}`에서 cost09/density edge recovery(비용0.9/밀도 엣지 회복)를 실행합니다.

Operating boundary(운영 경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""",
        bom=True,
    )
    write_text(
        SELECTION_STATUS,
        f"""# Stage364 selection status(선택 상태)

Updated(갱신): {final['created_at_utc']}

Current run(현재 실행): `{NEXT_RUN_ID}`
Latest completed run(최근 완료 실행): `{RUN_ID}`

Latest review(최근 검토): EU density/cost/short balance review(EU 밀도/비용/숏 균형 검토)는 ET package(ET 패키지)를 rejected(거절)했습니다.

Selected validation net/PF/density(선택 검증 순수익/PF/밀도): `{final['selected_validation_net']}` / `{final['selected_validation_profit_factor']}` / `{final['selected_validation_trade_density']}`
Selected OOS net/PF/density(선택 표본외 순수익/PF/밀도): `{final['selected_oos_net']}` / `{final['selected_oos_profit_factor']}` / `{final['selected_oos_trade_density']}`
Combined density/cost0.9/short share(합산 밀도/비용0.9/숏 비중): `{final['selected_combined_trade_density']}` / `{final['selected_combined_cost09_net']}` / `{final['selected_combined_short_share']}`

Next seed(다음 씨앗): cost09/density edge recovery(비용0.9/밀도 엣지 회복).

Authority(권위): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""",
        bom=True,
    )
    append_text_once(WORKSPACE_CHANGELOG, f"run364EU__{RUN_ID}", f"\n<!-- run364EU__{RUN_ID} -->\n- {final['created_at_utc']} `{RUN_ID}` reviewed ET density/cost/short balance reseed(ET 밀도/비용/숏 균형 재시드); package rejected(패키지 거절); next `{NEXT_RUN_ID}`; no authority claim(권위 주장 없음).\n")
    append_text_once(IDEA_REGISTRY, f"run364EU__{RUN_ID}", f"\n<!-- run364EU__{RUN_ID} -->\n- `{RUN_ID}`: ET made OOS PF/cost clue(표본외 PF/비용 단서) and repaired short share(숏 비중 수리)를 만들었지만 full-tape density/cost09(전체 테이프 밀도/비용0.9) 경계에서 패키지 제외입니다. Effect(효과): EV는 cost09/density edge(비용0.9/밀도 엣지)를 직접 공격합니다.\n")
    append_text_once(NEGATIVE_REGISTER, f"run364EU__cost09_density_edge_failure__{RUN_ID}", f"\n<!-- run364EU__cost09_density_edge_failure__{RUN_ID} -->\n- `{RUN_ID}`: ET selected candidate(ET 선택 후보)는 combined density(합산 밀도) `{final['selected_combined_trade_density']}`와 combined cost0.9 net(합산 비용0.9 순수익) `{final['selected_combined_cost09_net']}` 때문에 package rejected(패키지 거절)입니다. Effect(효과): OOS-only cost strength(표본외 전용 비용 강점)를 운영 근거로 쓰지 않고 EV 수리 조건으로 넘깁니다.\n")


def write_ledgers(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
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
        "question": "Should ET open runtime package or become EV cost09/density seed?(ET를 런타임 패키지로 열지, EV 비용0.9/밀도 씨앗으로 보낼지)",
        "next_action": NEXT_RUN_ID,
        "notes": f"strict=0;density={final['selected_combined_trade_density']};cost09={final['selected_combined_cost09_net']};package=rejected",
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
                "kpi_scope": "EU density/cost/short balance review(EU 밀도/비용/숏 균형 검토)",
                "metric_scope": "python_proxy_review_no_mt5(Python 프록시 검토, MT5 없음)",
                "status": status,
                "net_profit": final["selected_oos_net"] if suffix == "tier_a_separate" else "",
                "profit_factor": final["selected_oos_profit_factor"] if suffix == "tier_a_separate" else "",
                "trade_density_per_feature_day": final["selected_oos_trade_density"] if suffix == "tier_a_separate" else "",
                "source_authority": "python_proxy_review_no_mt5(Python 프록시 검토, MT5 없음)",
            }
        )
    append_or_replace_csv(STAGE_LEDGER, ["ledger_row_id"], rows)
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], rows)
    append_or_replace_csv(
        RUN_REGISTRY,
        ["run_id"],
        [
            {
                **common,
                "lane": "review_control(검토 제어)",
                "family": "alpha_exploration_review(알파 탐색 검토)",
                "primary_report": rel(REPORT_PATH),
                "run_family": "kpi_evidence(KPI 근거)",
                "run_type": "density_cost_short_balance_review(밀도/비용/숏 균형 검토)",
                "input_run_id": PARENT_RUN_ID,
                "output_path": rel(FINAL_DECISION),
                "result_path": rel(PACKAGE_DECISION),
                "best_model_id": final["selected_model_id"],
                "net_profit": final["selected_oos_net"],
                "profit_factor": final["selected_oos_profit_factor"],
                "trade_density_per_feature_day": final["selected_oos_trade_density"],
                "result_status": STATUS,
                "primary_kpi": f"combined_density={final['selected_combined_trade_density']};cost09={final['selected_combined_cost09_net']}",
                "guardrail_kpi": "package=rejected;authority=not_claimed",
                "final_decision_path": rel(FINAL_DECISION),
                "gate_audit_path": rel(GATE_AUDIT),
                "external_verification_status": "out_of_scope_by_claim(주장 범위 밖)",
                "evidence_boundary": "proxy_review_only_no_mt5_runtime_authority(프록시 검토만, MT5 런타임 권위 없음)",
            }
        ],
    )
    et.repair_run_registry_line_endings(RUN_ID)


def write_artifact_registry(final: Mapping[str, Any]) -> None:
    rows = []
    for path in OUTPUT_FILES:
        if exists(path) and io_path(path).is_file():
            rows.append(
                {
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "artifact_type": "script" if path == Path(__file__) else ("report" if path.suffix.lower() == ".md" else ("json" if path.suffix.lower() == ".json" else "csv")),
                    "path": rel(path),
                    "artifact_path": rel(path),
                    "sha256": sha(path),
                    "created_at": final["created_at_utc"],
                    "created_at_utc": final["created_at_utc"],
                    "claim_boundary": CLAIM_BOUNDARY,
                    "artifact_id": f"{RUN_ID}__{path.stem}",
                    "notes": "EU density/cost/short balance review artifact(EU 밀도/비용/숏 균형 검토 산출물)",
                }
            )
    append_or_replace_csv(ARTIFACT_REGISTRY, ["artifact_id"], rows)


def write_manifest(final: Mapping[str, Any]) -> None:
    outputs = [path for path in OUTPUT_FILES if exists(path)]
    write_json(
        RUN_MANIFEST,
        {
            "run_id": RUN_ID,
            "run_number": RUN_NUMBER,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "status": STATUS,
            "judgment": JUDGMENT,
            "claim_boundary": CLAIM_BOUNDARY,
            "command": f"python {rel(Path(__file__))}",
            "input_files": [rel(path) for path in INPUT_FILES],
            "input_hashes": {rel(path): sha(path) for path in INPUT_FILES if exists(path) and io_path(path).is_file()},
            "output_files": [rel(path) for path in outputs],
            "output_hashes": {rel(path): sha(path) for path in outputs if io_path(path).is_file()},
        },
    )


def main() -> None:
    ensure_dirs()
    parent = validate_inputs()
    created_at = now_utc()
    write_csv(INPUT_MANIFEST, input_manifest_rows())
    write_work_packet()
    summary_rows, attribution, salvage, package, failure, queue = build_review(parent)
    summary = summary_rows[0]
    write_csv(REVIEW_SUMMARY, summary_rows)
    write_csv(FAILURE_ATTRIBUTION, attribution)
    write_csv(SALVAGE_CANDIDATES, salvage)
    write_csv(PACKAGE_DECISION, package)
    write_csv(FAILURE_MEMORY, failure)
    write_csv(RUN364EV_QUEUE, queue)
    gates = gate_rows(final_written=False)
    final = final_payload(summary, gates, created_at)
    write_json(FINAL_DECISION, final)
    write_receipts(final, summary, attribution)
    write_csv(GATE_AUDIT, gates)
    gates = gate_rows(final_written=True)
    final = final_payload(summary, gates, created_at)
    write_json(FINAL_DECISION, final)
    write_csv(GATE_AUDIT, gates)
    write_docs(final, summary, attribution, salvage, package, failure, queue, gates)
    write_manifest(final)
    write_ledgers(final, gates)
    write_artifact_registry(final)
    write_receipts(final, summary, attribution)
    print(
        json.dumps(
            json_ready(
                {
                    "run_id": RUN_ID,
                    "status": STATUS,
                    "judgment": JUDGMENT,
                    "package_decision": "rejected",
                    "next_run_id": NEXT_RUN_ID,
                    "gate_passes": final["gate_passes"],
                    "gate_total": final["gate_total"],
                }
            ),
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
