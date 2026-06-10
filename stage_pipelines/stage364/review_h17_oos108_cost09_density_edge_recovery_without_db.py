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
from stage_pipelines.stage364 import train_h17_oos108_cost09_density_edge_recovery_without_db as ev  # noqa: E402


TODAY = "2026-06-06"
STAGE_ID = ev.STAGE_ID
RUN_NUMBER = "run364EW"
RUN_ID = "run364EW_review_h17_oos108_cost09_density_edge_recovery_without_db_v1"
PARENT_RUN_ID = ev.RUN_ID
NEXT_RUN_ID = "run364EX_train_h17_oos108_oos_preserve_cost09_short_rebalance_without_db_v1"

STATUS = "completed_stage364EW_cost09_density_edge_review_package_rejected_open_ex_no_authority"
JUDGMENT = "negative_cost09_density_edge_review_validation_overfit_oos_collapse_no_package_no_authority"
DECISION = "stage364EW_reject_package_open_run364EX_oos_preserve_cost09_short_rebalance"
CLAIM_BOUNDARY = (
    "research_development_cost09_density_edge_review_only_no_runtime_package_no_new_mt5_execution_"
    "no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

STAGE_DIR = ev.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
SPEC_DIR = STAGE_DIR / "00_spec"
SELECTED_DIR = STAGE_DIR / "04_selected"

INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
REVIEW_SUMMARY = RUN_DIR / "ew_cost09_density_edge_review_summary.csv"
FAILURE_ATTRIBUTION = RUN_DIR / "ew_failure_attribution.csv"
PACKAGE_DECISION = RUN_DIR / "package_decision.csv"
FAILURE_MEMORY = RUN_DIR / "cost09_density_edge_failure_memory.csv"
RUN364EX_QUEUE = RUN_DIR / "run364EX_oos_preserve_cost09_short_rebalance_queue.csv"
RESULT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
ATTRIBUTION_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / "run364EW_oos108_cost09_density_edge_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364EW_h17_oos108_cost09_density_edge_review.md"
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
    ev.FINAL_DECISION,
    ev.GATE_AUDIT,
    ev.TRADE_SURFACE,
    ev.SELECTED_CANDIDATE,
    ev.SELECTED_TRADE_TAPE,
    ev.COST_STRESS,
    ev.SIDE_SESSION_REVIEW,
    ev.MONTH_STABILITY,
    ev.MODEL_SCORECARD,
    ev.MODEL_ARTIFACT_MANIFEST,
    ev.ONNX_SMOKE_REPORT,
    ev.DATA_INTEGRITY_AUDIT,
    ev.RUN364EW_QUEUE,
    ev.RUN_EVIDENCE_RECEIPT,
    ev.MODEL_RECEIPT,
    ev.ATTRIBUTION_RECEIPT,
    ev.JUDGMENT_RECEIPT,
    ev.LINEAGE_RECEIPT,
    ev.CLAIM_RECEIPT,
    ev.RUN_MANIFEST,
    ev.REPORT_PATH,
    Path(__file__),
]

OUTPUT_FILES = [
    INPUT_MANIFEST,
    WORK_PACKET,
    REVIEW_SUMMARY,
    FAILURE_ATTRIBUTION,
    PACKAGE_DECISION,
    FAILURE_MEMORY,
    RUN364EX_QUEUE,
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
    return ev.sha(path)


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
    materialized = io_path(path)
    if materialized.exists():
        with materialized.open("r", encoding="utf-8-sig", newline="") as handle:
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
    with materialized.open("w", encoding="utf-8-sig", newline="") as handle:
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
        raise FileNotFoundError("missing EV inputs(EV 입력 누락): " + ", ".join(missing))
    parent = read_json(ev.FINAL_DECISION)
    if parent.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"EV next_run_id mismatch(EV 다음 실행 ID 불일치): {parent.get('next_run_id')} != {RUN_ID}")
    for key in ["runtime_authority", "operating_promotion", "live_readiness", "goal_achieve"]:
        if parent.get(key, "not_claimed") != "not_claimed":
            raise RuntimeError(f"forbidden EV claim(금지된 EV 주장): {key}={parent.get(key)}")
    gates = read_csv(ev.GATE_AUDIT)
    if gates.empty or any(gates["status"].astype(str) != "passed"):
        raise RuntimeError("EV gate audit(EV 게이트 감사)가 모두 passed(통과)가 아닙니다.")
    return parent


def input_manifest_rows() -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "input_path": rel(path),
            "exists": str(exists(path)).lower(),
            "sha256": sha(path) if exists(path) and io_path(path).is_file() else "",
            "input_role": "EW cost09/density review input(EW 비용0.9/밀도 검토 입력)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for path in INPUT_FILES
    ]


def bool_count(mask: pd.Series) -> int:
    return int(mask.fillna(False).sum())


def build_review(parent: Mapping[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    surface = read_csv(ev.TRADE_SURFACE)
    for column in [
        "validation_net",
        "validation_profit_factor",
        "validation_trade_density",
        "oos_net",
        "oos_profit_factor",
        "oos_trade_density",
        "combined_net",
        "combined_trade_density",
        "combined_cost09_net",
        "combined_short_share",
        "min_split_profit_factor",
        "selection_score",
    ]:
        surface[column] = pd.to_numeric(surface[column], errors="coerce").fillna(0.0)
    cost = read_csv(ev.COST_STRESS)
    for column in ["cost_per_trade", "trade_count", "net_profit", "profit_factor", "expectancy"]:
        cost[column] = pd.to_numeric(cost[column], errors="coerce").fillna(0.0)
    side = read_csv(ev.SIDE_SESSION_REVIEW)
    for column in ["open_hour", "trade_count", "net_profit", "profit_factor", "expectancy"]:
        side[column] = pd.to_numeric(side[column], errors="coerce").fillna(0.0)

    strict_count = int(parent["strict_candidate_count"])
    oos_positive = (surface["validation_net"] > 0) & (surface["oos_net"] > 0)
    oos_pf125 = oos_positive & (surface["oos_profit_factor"] >= 1.25)
    dense_oos_pf = oos_pf125 & (surface["combined_trade_density"] >= 3.0)
    short_ok = surface["combined_short_share"] <= 0.72
    cost09_ok = surface["combined_cost09_net"] >= 0.0
    balanced_candidate = dense_oos_pf & short_ok & cost09_ok
    top_oos = surface[oos_positive].sort_values(["oos_profit_factor", "selection_score"], ascending=False).head(1)
    top_oos_row = top_oos.iloc[0].to_dict() if not top_oos.empty else {}
    selected_oos_cost09 = cost[(cost["split"] == "oos") & (cost["cost_per_trade"] == 0.9)]
    selected_validation_cost09 = cost[(cost["split"] == "validation") & (cost["cost_per_trade"] == 0.9)]
    worst_side = side.sort_values("net_profit").head(6).to_dict("records")

    summary = [
        {
            "run_id": RUN_ID,
            "parent_run_id": PARENT_RUN_ID,
            "selected_model_id": parent["selected_model_id"],
            "selected_validation_net": parent["selected_validation_net"],
            "selected_validation_profit_factor": parent["selected_validation_profit_factor"],
            "selected_validation_trade_density": parent["selected_validation_trade_density"],
            "selected_oos_net": parent["selected_oos_net"],
            "selected_oos_profit_factor": parent["selected_oos_profit_factor"],
            "selected_oos_trade_density": parent["selected_oos_trade_density"],
            "selected_combined_net": parent["selected_combined_net"],
            "selected_combined_trade_density": parent["selected_combined_trade_density"],
            "selected_combined_cost09_net": parent["selected_combined_cost09_net"],
            "selected_combined_short_share": parent["selected_combined_short_share"],
            "selected_min_split_profit_factor": parent["selected_min_split_profit_factor"],
            "selected_validation_cost09_net": finite(selected_validation_cost09["net_profit"].iloc[0]) if not selected_validation_cost09.empty else "",
            "selected_oos_cost09_net": finite(selected_oos_cost09["net_profit"].iloc[0]) if not selected_oos_cost09.empty else "",
            "strict_candidate_count": strict_count,
            "operational_proxy_stack_pass_count": parent["operational_proxy_stack_pass_count"],
            "surface_rows": len(surface),
            "oos_positive_count": bool_count(oos_positive),
            "oos_pf125_count": bool_count(oos_pf125),
            "dense_oos_pf_count": bool_count(dense_oos_pf),
            "short_share_ok_count": bool_count(short_ok),
            "cost09_ok_count": bool_count(cost09_ok),
            "balanced_candidate_count": bool_count(balanced_candidate),
            "top_oos_model_id": top_oos_row.get("model_id", ""),
            "top_oos_validation_pf": finite(top_oos_row.get("validation_profit_factor")),
            "top_oos_oos_pf": finite(top_oos_row.get("oos_profit_factor")),
            "top_oos_combined_density": finite(top_oos_row.get("combined_trade_density")),
            "top_oos_cost09": finite(top_oos_row.get("combined_cost09_net")),
            "package_eligible": "false",
            "review_judgment": JUDGMENT,
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]

    attribution = [
        {
            "run_id": RUN_ID,
            "attribution_id": "ew01_validation_overfit",
            "observed": f"validation_net={parent['selected_validation_net']}; oos_net={parent['selected_oos_net']}; min_pf={parent['selected_min_split_profit_factor']}",
            "driver": "EV score(EV 점수)가 validation cost09(검증 비용0.9)를 고쳤지만 OOS(표본외)를 무너뜨렸습니다.",
            "severity": "high(높음)",
            "effect": "EX는 validation-only(검증 전용) 비용 회복을 선택 점수에서 강하게 벌점 처리합니다.",
            "evidence": rel(ev.FINAL_DECISION),
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "attribution_id": "ew02_short_overweight_returns",
            "observed": f"combined_short_share={parent['selected_combined_short_share']}",
            "driver": "EV는 short share(숏 비중)를 0.82까지 다시 키웠습니다.",
            "severity": "high(높음)",
            "effect": "EX는 ET의 short_share<=0.72(숏 비중 0.72 이하) 단서를 되살립니다.",
            "evidence": rel(ev.SIDE_SESSION_REVIEW),
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "attribution_id": "ew03_density_not_recovered",
            "observed": f"combined_density={parent['selected_combined_trade_density']}; validation_density={parent['selected_validation_trade_density']}; oos_density={parent['selected_oos_trade_density']}",
            "driver": "cost09 pressure(비용0.9 압박)를 키웠지만 density(밀도)는 3/day(일 3회)에서 더 멀어졌습니다.",
            "severity": "high(높음)",
            "effect": "EX는 ET seed(ET 씨앗)에서 OOS 보존과 숏 균형을 먼저 잠그고 비용0.9를 보조 목표로 둡니다.",
            "evidence": rel(ev.SELECTED_TRADE_TAPE),
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    for rank, row in enumerate(worst_side, 1):
        attribution.append(
            {
                "run_id": RUN_ID,
                "attribution_id": f"ew_side_loss_{rank}",
                "observed": f"{row.get('split')} {row.get('direction')} hour {row.get('open_hour')} net={row.get('net_profit')} trades={row.get('trade_count')}",
                "driver": "side/session loss segment(방향/세션 손실 구간)",
                "severity": "context(문맥)",
                "effect": "EX의 penalty seed(벌점 씨앗)로만 쓰고 운영 필터로 고정하지 않습니다.",
                "evidence": rel(ev.SIDE_SESSION_REVIEW),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    package = [
        {
            "run_id": RUN_ID,
            "decision": "reject_runtime_package(런타임 패키지 거절)",
            "reason": "strict_candidate_count=0, OOS net negative, OOS cost0.9 negative, short share high, density<3(엄격 후보 0, 표본외 순수익 음수, 표본외 비용0.9 음수, 숏 비중 과다, 밀도 3 미만)",
            "runtime_package": "not_opened(열지 않음)",
            "new_mt5_execution": "not_run(미실행)",
            "runtime_authority": "not_claimed(주장 안 함)",
            "effect": "EV validation recovery(EV 검증 회복)를 운영 주장으로 올리지 않습니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    failure = [
        {
            "run_id": RUN_ID,
            "memory_id": "ew01_cost09_validation_overfit",
            "failed_boundary": "OOS preservation and short balance(표본외 보존과 숏 균형)",
            "why_failed": f"OOS net {parent['selected_oos_net']}, OOS PF {parent['selected_oos_profit_factor']}, short share {parent['selected_combined_short_share']}",
            "salvage_value": "validation cost0.9 became positive(검증 비용0.9 양수화) but cannot be used alone(단독 사용 불가).",
            "reopen_condition": "OOS PF>=1.25, OOS cost0.9>=0, short_share<=0.72 before validation cost09 reward(검증 비용 보상 전에 표본외/숏 조건 고정)",
            "do_not_repeat": "Do not overweight validation cost09(검증 비용0.9 과가중 금지).",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    queue = [
        {
            "run_id": RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "queue_rank": 1,
            "queue_id": "ex01_oos_preserve_cost09_short_rebalance",
            "hypothesis": "ET seed(ET 씨앗)의 OOS PF/cost clue(표본외 PF/비용 단서)와 short balance(숏 균형)를 먼저 잠그면 cost09(비용0.9)를 보조 보상으로 다시 넣어도 OOS collapse(표본외 붕괴)를 피할 수 있습니다.",
            "seed_from": "run364ET selected + EU failure memory(EU 실패 기억)",
            "required_preserve": "OOS PF>=1.25, OOS net>0, OOS cost0.6>0, short_share<=0.72(표본외 PF/순수익/비용0.6/숏 비중)",
            "required_repair": "validation density>=3, combined density>=3, validation cost0.9 improves without OOS net collapse(검증/합산 밀도와 검증 비용0.9 회복, 표본외 붕괴 금지)",
            "avoid": "validation-only cost09 reward(검증 전용 비용0.9 보상)",
            "effect": "EX는 EV 실패를 반대로 사용해 OOS 보존을 먼저 둡니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    return summary, attribution, package, failure, queue


def write_work_packet() -> None:
    write_json(
        WORK_PACKET,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "primary_family": "kpi_evidence(KPI 근거)",
            "primary_skill": "obsidian-run-evidence-system(실행 근거 시스템)",
            "support_skills": ["obsidian-artifact-lineage(산출물 계보)", "obsidian-result-judgment(결과 판정)", "obsidian-performance-attribution(성과 귀속)"],
            "review_question": "Should EV open package or seed EX OOS-preserving rebalance?(EV를 패키지로 열지, EX 표본외 보존 재균형 씨앗으로 보낼지)",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def write_receipts(final: Mapping[str, Any], summary: Mapping[str, Any], attribution: Sequence[Mapping[str, Any]]) -> None:
    base = {"run_id": RUN_ID, "stage_id": STAGE_ID, "created_at_utc": final["created_at_utc"], "claim_boundary": CLAIM_BOUNDARY}
    write_json(RESULT_RECEIPT, {**base, "result_subject": PARENT_RUN_ID, "evidence_available": [rel(REVIEW_SUMMARY), rel(FAILURE_ATTRIBUTION), rel(PACKAGE_DECISION), rel(ev.FINAL_DECISION)], "evidence_missing": ["MT5 runtime probe(MT5 런타임 탐침)", "runtime package(런타임 패키지)"], "judgment_label": JUDGMENT, "next_condition": NEXT_RUN_ID})
    write_json(MODEL_RECEIPT, {**base, "model_subject": PARENT_RUN_ID, "selected_model_id": summary["selected_model_id"], "validation_judgment": JUDGMENT})
    write_json(ATTRIBUTION_RECEIPT, {**base, "observed_change": f"validation/OOS net {summary['selected_validation_net']}/{summary['selected_oos_net']}; short_share {summary['selected_combined_short_share']}", "likely_drivers": [row["driver"] for row in attribution[:3]], "attribution_confidence": "medium_proxy_only(중간, 프록시 전용)", "next_probe": NEXT_RUN_ID})
    write_json(LINEAGE_RECEIPT, {**base, "source_inputs": [{"path": rel(path), "sha256": sha(path)} for path in INPUT_FILES if exists(path) and io_path(path).is_file()], "producer": rel(Path(__file__)), "consumer": NEXT_RUN_ID, "artifact_paths": [rel(path) for path in OUTPUT_FILES if exists(path)], "artifact_hashes": {rel(path): sha(path) for path in OUTPUT_FILES if exists(path) and io_path(path).is_file()}, "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)], "lineage_judgment": "connected_review_no_package(검토 연결, 패키지 없음)"})
    write_json(CLAIM_RECEIPT, {**base, "runtime_package": "not_opened", "runtime_authority": "not_claimed", "operating_promotion": "not_claimed", "live_readiness": "not_claimed", "goal_achieve": "not_claimed", "effect": "EV 결과를 운영 주장으로 올리지 않습니다."})


def gate_rows(final_written: bool) -> list[dict[str, Any]]:
    parent_gates = read_csv(ev.GATE_AUDIT)
    receipts = [RESULT_RECEIPT, MODEL_RECEIPT, ATTRIBUTION_RECEIPT, LINEAGE_RECEIPT, CLAIM_RECEIPT]
    checks = [
        ("input_lineage_gate", exists(INPUT_MANIFEST), INPUT_MANIFEST, "EV 입력 계보가 EW 검토에 연결됐습니다."),
        ("parent_gate_inheritance_gate", not parent_gates.empty and all(parent_gates["status"].astype(str) == "passed"), ev.GATE_AUDIT, "EV 게이트 통과 상태를 상속했습니다."),
        ("kpi_contract_audit", exists(REVIEW_SUMMARY) and exists(PACKAGE_DECISION), REVIEW_SUMMARY, "KPI, 패키지 결정, 실패 경계를 분리했습니다."),
        ("failure_attribution_gate", exists(FAILURE_ATTRIBUTION), FAILURE_ATTRIBUTION, "OOS 붕괴와 숏 과다를 귀속했습니다."),
        ("package_decision_gate", exists(PACKAGE_DECISION), PACKAGE_DECISION, "런타임 패키지 거절 근거를 기록했습니다."),
        ("failure_memory_gate", exists(FAILURE_MEMORY), FAILURE_MEMORY, "실패 기억과 재개 조건을 기록했습니다."),
        ("next_queue_gate", exists(RUN364EX_QUEUE), RUN364EX_QUEUE, "EX 표본외 보존 재균형 대기열을 만들었습니다."),
        ("receipt_coverage_gate", all(exists(path) for path in receipts), RESULT_RECEIPT, "필수 receipt(영수증)가 있습니다."),
        ("required_gate_coverage_audit", final_written and exists(GATE_AUDIT), GATE_AUDIT, "필수 gate(게이트)가 종료 기록에 연결됐습니다."),
        ("final_claim_guard", True, CLAIM_RECEIPT, "권위/승격/실거래/목표 달성 주장을 차단했습니다."),
    ]
    return [{"run_id": RUN_ID, "gate": gate, "status": "passed" if passed else "failed", "evidence": rel(evidence), "effect": effect, "claim_boundary": CLAIM_BOUNDARY} for gate, passed, evidence, effect in checks]


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
        "selected_combined_cost09_net": summary["selected_combined_cost09_net"],
        "selected_combined_short_share": summary["selected_combined_short_share"],
        "selected_oos_cost09_net": summary["selected_oos_cost09_net"],
        "selected_validation_cost09_net": summary["selected_validation_cost09_net"],
        "strict_candidate_count": summary["strict_candidate_count"],
        "balanced_candidate_count": summary["balanced_candidate_count"],
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


def write_docs(final: Mapping[str, Any], summary: Mapping[str, Any], attribution: Sequence[Mapping[str, Any]], package: Sequence[Mapping[str, Any]], failure: Sequence[Mapping[str, Any]], queue: Sequence[Mapping[str, Any]], gates: Sequence[Mapping[str, Any]]) -> None:
    report = f"""# run364EW OOS108 Cost09/Density Edge Review(표본외108 비용0.9/밀도 엣지 검토)

Created(생성): {final['created_at_utc']}

Action(행동): EV cost09/density edge recovery(EV 비용0.9/밀도 엣지 회복)를 package(패키지), failure memory(실패 기억), EX queue(EX 대기열)로 분리했습니다.

Effect(효과): validation cost09(검증 비용0.9)만 좋아진 결과를 운영 단서로 과장하지 않고, OOS collapse(표본외 붕괴)를 다음 제약으로 고정합니다.

- judgment(판정): `{final['judgment']}`
- selected model(선택 모델): `{final['selected_model_id']}`
- validation net/PF/density(검증 순수익/PF/밀도): `{final['selected_validation_net']}` / `{final['selected_validation_profit_factor']}` / `{final['selected_validation_trade_density']}`
- OOS net/PF/density(표본외 순수익/PF/밀도): `{final['selected_oos_net']}` / `{final['selected_oos_profit_factor']}` / `{final['selected_oos_trade_density']}`
- combined net/density/cost0.9/short share(합산 순수익/밀도/비용0.9/숏 비중): `{final['selected_combined_net']}` / `{final['selected_combined_trade_density']}` / `{final['selected_combined_cost09_net']}` / `{final['selected_combined_short_share']}`
- selected OOS cost0.9 net(선택 표본외 비용0.9 순수익): `{final['selected_oos_cost09_net']}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`

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
    decision_doc = f"""# Decision(결정): stage364EW cost09/density edge review(비용0.9/밀도 엣지 검토)

- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- package(패키지): `rejected(거절)`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Action(행동): EV 결과를 검토해 runtime package(런타임 패키지)를 열지 않고 EX OOS-preserving rebalance(EX 표본외 보존 재균형)로 넘겼습니다.

Effect(효과): validation-only recovery(검증 전용 회복)를 막고 OOS preservation(표본외 보존)을 다음 설계의 첫 조건으로 둡니다.
"""
    write_text(REPORT_PATH, report, bom=True)
    write_text(DECISION_DOC, decision_doc, bom=True)
    append_text_once(REVIEW_INDEX, f"run364EW__{RUN_ID}", f"\n- run364EW__{RUN_ID}: [{REPORT_PATH.name}]({REPORT_PATH.name}) - cost09/density edge review(비용0.9/밀도 엣지 검토), next `{NEXT_RUN_ID}`.\n")
    append_text_once(STAGE_BRIEF, f"run364EW__{RUN_ID}", f"\n<!-- run364EW__{RUN_ID} -->\n\n## run364EW Cost09/Density Edge Review(비용0.9/밀도 엣지 검토)\n\nAction(행동): EV 결과를 package rejected(패키지 거절)로 검토했습니다.\n\nEffect(효과): `{NEXT_RUN_ID}`에서 OOS-preserving cost09/short rebalance(표본외 보존 비용0.9/숏 재균형)를 다음 공격 탐색으로 엽니다.\n")
    append_text_once(STAGE_README, f"run364EW__{RUN_ID}", f"\n<!-- run364EW__{RUN_ID} -->\n## run364EW cost09/density edge review(비용0.9/밀도 엣지 검토)\n\nPackage(패키지): rejected(거절). Next(다음): `{NEXT_RUN_ID}`.\n")
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

Current truth(현재 진실): `run364EW` reviewed(검토 완료) EV cost09/density edge recovery(EV 비용0.9/밀도 엣지 회복). EV는 validation cost0.9(검증 비용0.9)는 회복했지만 selected OOS net/PF/cost0.9(선택 표본외 순수익/PF/비용0.9)가 `{final['selected_oos_net']}` / `{final['selected_oos_profit_factor']}` / `{final['selected_oos_cost09_net']}`로 무너졌습니다.

Package truth(패키지 진실): strict candidate(엄격 후보)는 `{final['strict_candidate_count']}`개이고 runtime package(런타임 패키지)는 not opened(열지 않음)입니다.

Next action(다음 행동): `{NEXT_RUN_ID}`에서 OOS-preserving cost09/short rebalance(표본외 보존 비용0.9/숏 재균형)를 실행합니다.

Operating boundary(운영 경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""", bom=True)
    write_text(SELECTION_STATUS, f"""# Stage364 selection status(선택 상태)

Updated(갱신): {final['created_at_utc']}

Current run(현재 실행): `{NEXT_RUN_ID}`
Latest completed run(최근 완료 실행): `{RUN_ID}`

Latest review(최근 검토): EW cost09/density edge review(EW 비용0.9/밀도 엣지 검토)는 EV package(EV 패키지)를 rejected(거절)했습니다.

Selected validation net/PF/density(선택 검증 순수익/PF/밀도): `{final['selected_validation_net']}` / `{final['selected_validation_profit_factor']}` / `{final['selected_validation_trade_density']}`
Selected OOS net/PF/density(선택 표본외 순수익/PF/밀도): `{final['selected_oos_net']}` / `{final['selected_oos_profit_factor']}` / `{final['selected_oos_trade_density']}`

Next seed(다음 씨앗): OOS-preserving cost09/short rebalance(표본외 보존 비용0.9/숏 재균형).

Authority(권위): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""", bom=True)
    append_text_once(WORKSPACE_CHANGELOG, f"run364EW__{RUN_ID}", f"\n<!-- run364EW__{RUN_ID} -->\n- {final['created_at_utc']} `{RUN_ID}` reviewed EV cost09/density edge recovery(비용0.9/밀도 엣지 회복); package rejected(패키지 거절); next `{NEXT_RUN_ID}`; no authority claim(권위 주장 없음).\n")
    append_text_once(IDEA_REGISTRY, f"run364EW__{RUN_ID}", f"\n<!-- run364EW__{RUN_ID} -->\n- `{RUN_ID}`: EV는 validation cost09(검증 비용0.9)를 일부 회복했지만 OOS collapse(표본외 붕괴)를 만들었습니다. Effect(효과): EX는 OOS preservation(표본외 보존)을 먼저 잠급니다.\n")
    append_text_once(NEGATIVE_REGISTER, f"run364EW__validation_overfit_oos_collapse__{RUN_ID}", f"\n<!-- run364EW__validation_overfit_oos_collapse__{RUN_ID} -->\n- `{RUN_ID}`: EV selected candidate(EV 선택 후보)는 OOS net/PF(표본외 순수익/PF) `{final['selected_oos_net']}` / `{final['selected_oos_profit_factor']}`로 package rejected(패키지 거절)입니다. Effect(효과): validation cost09(검증 비용0.9) 단독 보상 반복을 금지합니다.\n")


def write_ledgers(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    artifact_count = len({Path(path) for path in OUTPUT_FILES if exists(path) or Path(path) == RUN_MANIFEST})
    common = {"stage_id": STAGE_ID, "run_id": RUN_ID, "parent_run_id": PARENT_RUN_ID, "status": STATUS, "judgment": JUDGMENT, "path": rel(FINAL_DECISION), "run_number": RUN_NUMBER, "date": TODAY, "decision": DECISION, "next_run_id": NEXT_RUN_ID, "artifact_count": artifact_count, "gate_passes": final["gate_passes"], "gate_total": final["gate_total"], "claim_boundary": CLAIM_BOUNDARY, "report_path": rel(REPORT_PATH), "created_at_utc": final["created_at_utc"], "required_gate_audit": rel(GATE_AUDIT), "question": "Should EV open package or seed EX OOS-preserving rebalance?(EV를 패키지로 열지, EX 표본외 보존 재균형 씨앗으로 보낼지)", "next_action": NEXT_RUN_ID, "notes": f"oos_net={final['selected_oos_net']};short_share={final['selected_combined_short_share']};package=rejected", "runtime_authority": "not_claimed", "operating_promotion": "not_claimed", "goal_achieve": "not_claimed"}
    rows = []
    for suffix, record_view, tier_scope, status in [
        ("tier_a_separate", "Tier A separate(Tier A 분리)", "Tier A", STATUS),
        ("tier_b_missing_required", "Tier B separate(Tier B 분리)", "Tier B", "missing_required_no_tier_b_model_input(필수 누락, Tier B 모델 입력 없음)"),
        ("tier_a_b_combined_out_of_scope", "Tier A+B combined(Tier A+B 합산)", "Tier A+B", "out_of_scope_by_claim_proxy_tier_a_only(주장 범위 밖, 프록시 Tier A 전용)"),
    ]:
        rows.append({**common, "ledger_row_id": f"{RUN_ID}__{suffix}", "subrun_id": f"{RUN_ID}__{suffix}", "row_id": f"{RUN_ID}__{suffix}", "record_view": record_view, "tier_scope": tier_scope, "view": record_view, "tier": tier_scope, "kpi_scope": "EW cost09/density edge review(EW 비용0.9/밀도 엣지 검토)", "metric_scope": "python_proxy_review_no_mt5(Python 프록시 검토, MT5 없음)", "status": status, "net_profit": final["selected_oos_net"] if suffix == "tier_a_separate" else "", "profit_factor": final["selected_oos_profit_factor"] if suffix == "tier_a_separate" else "", "trade_density_per_feature_day": final["selected_oos_trade_density"] if suffix == "tier_a_separate" else "", "source_authority": "python_proxy_review_no_mt5(Python 프록시 검토, MT5 없음)"})
    append_or_replace_csv(STAGE_LEDGER, ["ledger_row_id"], rows)
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], rows)
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], [{**common, "lane": "review_control(검토 제어)", "family": "alpha_exploration_review(알파 탐색 검토)", "primary_report": rel(REPORT_PATH), "run_family": "kpi_evidence(KPI 근거)", "run_type": "cost09_density_edge_review(비용0.9/밀도 엣지 검토)", "input_run_id": PARENT_RUN_ID, "output_path": rel(FINAL_DECISION), "result_path": rel(PACKAGE_DECISION), "best_model_id": final["selected_model_id"], "net_profit": final["selected_oos_net"], "profit_factor": final["selected_oos_profit_factor"], "trade_density_per_feature_day": final["selected_oos_trade_density"], "result_status": STATUS, "primary_kpi": f"oos_net={final['selected_oos_net']};oos_pf={final['selected_oos_profit_factor']}", "guardrail_kpi": "package=rejected;authority=not_claimed", "final_decision_path": rel(FINAL_DECISION), "gate_audit_path": rel(GATE_AUDIT), "external_verification_status": "out_of_scope_by_claim(주장 범위 밖)", "evidence_boundary": "proxy_review_only_no_mt5_runtime_authority(프록시 검토만, MT5 런타임 권위 없음)"}])
    ev.et.repair_run_registry_line_endings(RUN_ID)


def write_artifact_registry(final: Mapping[str, Any]) -> None:
    rows = []
    for path in OUTPUT_FILES:
        if exists(path) and io_path(path).is_file():
            rows.append({"stage_id": STAGE_ID, "run_id": RUN_ID, "artifact_type": "script" if path == Path(__file__) else ("report" if path.suffix.lower() == ".md" else ("json" if path.suffix.lower() == ".json" else "csv")), "path": rel(path), "artifact_path": rel(path), "sha256": sha(path), "created_at": final["created_at_utc"], "created_at_utc": final["created_at_utc"], "claim_boundary": CLAIM_BOUNDARY, "artifact_id": f"{RUN_ID}__{path.stem}", "notes": "EW cost09/density edge review artifact(EW 비용0.9/밀도 엣지 검토 산출물)"})
    append_or_replace_csv(ARTIFACT_REGISTRY, ["artifact_id"], rows)


def write_manifest(final: Mapping[str, Any]) -> None:
    outputs = [path for path in OUTPUT_FILES if exists(path)]
    write_json(RUN_MANIFEST, {"run_id": RUN_ID, "run_number": RUN_NUMBER, "stage_id": STAGE_ID, "parent_run_id": PARENT_RUN_ID, "next_run_id": NEXT_RUN_ID, "status": STATUS, "judgment": JUDGMENT, "claim_boundary": CLAIM_BOUNDARY, "command": f"python {rel(Path(__file__))}", "input_files": [rel(path) for path in INPUT_FILES], "input_hashes": {rel(path): sha(path) for path in INPUT_FILES if exists(path) and io_path(path).is_file()}, "output_files": [rel(path) for path in outputs], "output_hashes": {rel(path): sha(path) for path in outputs if io_path(path).is_file()}})


def main() -> None:
    ensure_dirs()
    parent = validate_inputs()
    created_at = now_utc()
    write_csv(INPUT_MANIFEST, input_manifest_rows())
    write_work_packet()
    summary_rows, attribution, package, failure, queue = build_review(parent)
    summary = summary_rows[0]
    write_csv(REVIEW_SUMMARY, summary_rows)
    write_csv(FAILURE_ATTRIBUTION, attribution)
    write_csv(PACKAGE_DECISION, package)
    write_csv(FAILURE_MEMORY, failure)
    write_csv(RUN364EX_QUEUE, queue)
    gates = gate_rows(final_written=False)
    final = final_payload(summary, gates, created_at)
    write_json(FINAL_DECISION, final)
    write_receipts(final, summary, attribution)
    write_csv(GATE_AUDIT, gates)
    gates = gate_rows(final_written=True)
    final = final_payload(summary, gates, created_at)
    write_json(FINAL_DECISION, final)
    write_csv(GATE_AUDIT, gates)
    write_docs(final, summary, attribution, package, failure, queue, gates)
    write_manifest(final)
    write_ledgers(final, gates)
    write_artifact_registry(final)
    write_receipts(final, summary, attribution)
    print(json.dumps(json_ready({"run_id": RUN_ID, "status": STATUS, "judgment": JUDGMENT, "package_decision": "rejected", "next_run_id": NEXT_RUN_ID, "gate_passes": final["gate_passes"], "gate_total": final["gate_total"]}), ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
