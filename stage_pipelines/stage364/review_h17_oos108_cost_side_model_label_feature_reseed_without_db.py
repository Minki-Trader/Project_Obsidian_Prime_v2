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
from stage_pipelines.stage364 import train_h17_oos108_cost_side_model_label_feature_reseed_without_db as er  # noqa: E402
from stage_pipelines.stage364.review_pf_pass_density_restore_offensive_scout_without_db import repair_run_registry_line_endings  # noqa: E402


TODAY = "2026-06-06"
STAGE_ID = er.STAGE_ID
RUN_NUMBER = "run364ES"
RUN_ID = "run364ES_review_h17_oos108_cost_side_model_label_feature_reseed_without_db_v1"
PARENT_RUN_ID = er.RUN_ID
NEXT_RUN_ID = "run364ET_train_h17_oos108_density_cost_short_balance_reseed_without_db_v1"

STATUS = "completed_stage364ES_oos108_cost_side_reseed_review_package_rejected_open_et_no_authority"
JUDGMENT = "negative_cost_side_reseed_review_density_cost_short_failure_no_package_no_authority"
DECISION = "stage364ES_reject_package_open_run364ET_density_cost_short_balance_reseed"
CLAIM_BOUNDARY = (
    "research_development_cost_side_reseed_review_only_no_runtime_package_no_new_mt5_execution_"
    "no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

STAGE_DIR = er.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
SPEC_DIR = STAGE_DIR / "00_spec"
SELECTED_DIR = STAGE_DIR / "04_selected"

INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
REVIEW_SUMMARY = RUN_DIR / "es_cost_side_reseed_review_summary.csv"
FAILURE_ATTRIBUTION = RUN_DIR / "es_failure_attribution.csv"
PACKAGE_DECISION = RUN_DIR / "package_decision.csv"
SIDE_SESSION_GUARDRAIL = RUN_DIR / "es_side_session_guardrail.csv"
MONTH_COST_REVIEW = RUN_DIR / "es_month_cost_review.csv"
FAILURE_MEMORY = RUN_DIR / "cost_side_reseed_failure_memory.csv"
RUN364ET_QUEUE = RUN_DIR / "run364ET_density_cost_short_balance_reseed_queue.csv"
RESULT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
ATTRIBUTION_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / "run364ES_oos108_cost_side_reseed_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364ES_h17_oos108_cost_side_model_label_feature_reseed_review.md"
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
    er.FINAL_DECISION,
    er.GATE_AUDIT,
    er.TRADE_SURFACE,
    er.SELECTED_CANDIDATE,
    er.SELECTED_TRADE_TAPE,
    er.MONTH_STABILITY,
    er.COST_STRESS,
    er.SIDE_SESSION_REVIEW,
    er.MODEL_SCORECARD,
    er.ONNX_SMOKE_REPORT,
    er.DATA_INTEGRITY_AUDIT,
    er.RUN364ES_QUEUE,
    er.REPORT_PATH,
    er.RUN_MANIFEST,
    er.RUN_EVIDENCE_RECEIPT,
    er.MODEL_RECEIPT,
    er.ATTRIBUTION_RECEIPT,
    er.JUDGMENT_RECEIPT,
    er.LINEAGE_RECEIPT,
    er.CLAIM_RECEIPT,
    Path(__file__),
]

OUTPUT_FILES = [
    INPUT_MANIFEST,
    WORK_PACKET,
    REVIEW_SUMMARY,
    FAILURE_ATTRIBUTION,
    PACKAGE_DECISION,
    SIDE_SESSION_GUARDRAIL,
    MONTH_COST_REVIEW,
    FAILURE_MEMORY,
    RUN364ET_QUEUE,
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
    return er.sha(path)


def as_float(value: Any, default: float = 0.0) -> float:
    return er.as_float(value, default)


def finite(value: Any, digits: int = 10) -> float | str:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return ""
    if not math.isfinite(number):
        return ""
    return round(number, digits)


def read_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8-sig") as handle:
        return json.load(handle)


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(json_ready(payload), handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")


def read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, encoding="utf-8-sig").fillna("")


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    materialized = [dict(row) for row in rows]
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fields: list[str] = []
        for row in materialized:
            for key in row.keys():
                if key not in fields:
                    fields.append(str(key))
        fieldnames = fields or ["empty"]
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fieldnames), extrasaction="ignore")
        writer.writeheader()
        for row in materialized:
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
        path.mkdir(parents=True, exist_ok=True)


def validate_inputs() -> dict[str, Any]:
    missing = [rel(path) for path in INPUT_FILES if path != Path(__file__) and not exists(path)]
    if missing:
        raise FileNotFoundError("missing ES inputs(ES 입력 누락): " + ", ".join(missing))
    parent = read_json(er.FINAL_DECISION)
    if parent.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"ER next_run_id mismatch(ER 다음 실행 ID 불일치): {parent.get('next_run_id')} != {RUN_ID}")
    for key in ["runtime_authority", "operating_promotion", "live_readiness", "goal_achieve"]:
        if parent.get(key, "not_claimed") != "not_claimed":
            raise RuntimeError(f"forbidden prior claim(이전 금지 주장): {key}={parent.get(key)}")
    gates = read_csv(er.GATE_AUDIT)
    if gates.empty or any(gates["status"].astype(str) != "passed"):
        raise RuntimeError("ER gate audit(ER 게이트 감사)가 모두 passed(통과)가 아닙니다.")
    return parent


def input_manifest_rows() -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "input_path": rel(path),
            "exists": str(exists(path)).lower(),
            "sha256": sha(path) if exists(path) and Path(path).is_file() else "",
            "input_role": "ES cost-side review input(ES 비용/방향 검토 입력)",
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


def build_tables(parent: Mapping[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    numeric_columns = [
        "validation_net",
        "validation_profit_factor",
        "validation_trade_density",
        "validation_trade_count",
        "oos_net",
        "oos_profit_factor",
        "oos_trade_density",
        "oos_trade_count",
        "combined_net",
        "combined_trade_density",
        "combined_cost06_net",
        "combined_cost09_net",
        "combined_short_share",
        "selection_score",
    ]
    surface = numeric_frame(er.TRADE_SURFACE, numeric_columns)
    side = numeric_frame(er.SIDE_SESSION_REVIEW, ["trade_count", "net_profit", "profit_factor", "expectancy"])
    month = numeric_frame(er.MONTH_STABILITY, ["trade_count", "net_profit", "profit_factor"])
    cost = numeric_frame(er.COST_STRESS, ["cost_per_trade", "trade_count", "net_profit", "profit_factor", "expectancy"])
    smoke = read_csv(er.ONNX_SMOKE_REPORT)

    density_ge_3 = surface["combined_trade_density"] >= 3.0
    validation_cost06_ge0 = (surface["validation_net"] - 0.30 * surface["validation_trade_count"]) >= 0.0
    oos_cost06_gt0 = (surface["oos_net"] - 0.30 * surface["oos_trade_count"]) > 0.0
    combined_cost09_ge0 = surface["combined_cost09_net"] >= 0.0
    min_pf_ge_121 = surface[["validation_profit_factor", "oos_profit_factor"]].min(axis=1) >= 1.21
    short_share_le_072 = surface["combined_short_share"] <= 0.72
    net_ge_runtime = surface["combined_net"] >= er.eq.RUNTIME_NET_REFERENCE
    strict_mask = density_ge_3 & validation_cost06_ge0 & oos_cost06_gt0 & combined_cost09_ge0 & min_pf_ge_121 & short_share_le_072 & net_ge_runtime
    density_cost_oos = density_ge_3 & validation_cost06_ge0 & oos_cost06_gt0

    best_selection = surface.sort_values("selection_score", ascending=False).iloc[0].to_dict()
    best_density = surface[density_ge_3].sort_values("selection_score", ascending=False).head(1)
    best_density_row = best_density.iloc[0].to_dict() if not best_density.empty else {}
    high_pf_sparse = surface[combined_cost09_ge0 & min_pf_ge_121].sort_values("selection_score", ascending=False).head(1)
    high_pf_sparse_row = high_pf_sparse.iloc[0].to_dict() if not high_pf_sparse.empty else {}

    val_cost06 = as_float(parent["selected_validation_cost06_net"])
    oos_cost06 = as_float(parent["selected_oos_cost06_net"])
    combined_cost09 = as_float(parent["selected_combined_cost09_net"])
    density = as_float(parent["selected_combined_trade_density"])
    short_share = as_float(parent["selected_combined_short_share"])

    summary = [
        {
            "run_id": RUN_ID,
            "parent_run_id": PARENT_RUN_ID,
            "selected_model_id": parent["selected_model_id"],
            "selected_metric_source": parent.get("selected_metric_source", ""),
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
            "strict_candidate_count": parent["strict_candidate_count"],
            "operational_proxy_stack_pass_count": parent["operational_proxy_stack_pass_count"],
            "onnx_smoke_pass_rows": int(smoke["status"].astype(str).str.startswith("passed").sum()) if not smoke.empty else 0,
            "surface_rows": len(surface),
            "density_ge_3_count": bool_count(density_ge_3),
            "validation_cost06_ge0_count": bool_count(validation_cost06_ge0),
            "oos_cost06_gt0_count": bool_count(oos_cost06_gt0),
            "combined_cost09_ge0_count": bool_count(combined_cost09_ge0),
            "min_pf_ge_1p21_count": bool_count(min_pf_ge_121),
            "short_share_le_0p72_count": bool_count(short_share_le_072),
            "combined_net_ge_523p58_count": bool_count(net_ge_runtime),
            "density_cost_oos_count": bool_count(density_cost_oos),
            "strict_recomputed_count": bool_count(strict_mask),
            "package_eligible": "false",
            "review_judgment": JUDGMENT,
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]

    attribution = [
        {
            "run_id": RUN_ID,
            "attribution_id": "es01_density_cost_conflict",
            "observed": f"combined density {density}; density_ge_3_count={bool_count(density_ge_3)}; density_cost_oos_count={bool_count(density_cost_oos)}",
            "driver": "density floor(밀도 바닥)을 맞추면 cost recovery(비용 회복)가 같이 깨집니다.",
            "evidence": rel(er.TRADE_SURFACE),
            "severity": "high(높음)",
            "effect": "ET는 threshold(임계값) 미세 조정보다 density/cost 동시 목표를 새 score(점수)에 넣어야 합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "attribution_id": "es02_oos_cost06_failure",
            "observed": f"validation cost0.6 net {val_cost06}; OOS cost0.6 net {oos_cost06}",
            "driver": "OOS cost resilience(표본외 비용 회복력)가 부족합니다.",
            "evidence": rel(er.COST_STRESS),
            "severity": "high(높음)",
            "effect": "OOS cost0.6(표본외 비용0.6)을 다음 strict scout(엄격 정찰)의 최소 조건으로 유지합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "attribution_id": "es03_cost09_break",
            "observed": f"combined cost0.9 net {combined_cost09}",
            "driver": "stress cost(압박 비용)에서 expectancy(기대값)가 너무 얇습니다.",
            "evidence": rel(er.COST_STRESS),
            "severity": "high(높음)",
            "effect": "ET는 trade count(거래수)를 늘리되 per-trade edge(거래당 우위)를 깎는 조합을 피해야 합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "attribution_id": "es04_short_share_overweight",
            "observed": f"combined short share {short_share}",
            "driver": "short exposure(숏 노출)가 여전히 큽니다.",
            "evidence": rel(er.SIDE_SESSION_REVIEW),
            "severity": "medium(중간)",
            "effect": "ET는 short veto(숏 차단)보다 long recovery(롱 회복)와 short hour guard(숏 시간 가드)를 함께 시험합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "attribution_id": "es05_runtime_net_gap",
            "observed": f"combined net {parent['selected_combined_net']} versus reference {er.eq.RUNTIME_NET_REFERENCE}",
            "driver": "runtime reference net(런타임 기준 순수익)까지 절대 순수익이 부족합니다.",
            "evidence": rel(er.FINAL_DECISION),
            "severity": "medium(중간)",
            "effect": "현재 ER 후보는 package(패키지)가 아니라 다음 offensive exploration(공격 탐색) 입력입니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]

    package = [
        {
            "run_id": RUN_ID,
            "decision": "reject_runtime_package(런타임 패키지 거절)",
            "reason": "strict_candidate_count=0, density<3, OOS cost0.6<0, combined cost0.9<0, short share>0.72(엄격 후보 0, 밀도 미달, 표본외 비용0.6 음수, 합산 비용0.9 음수, 숏 비중 초과)",
            "selected_model_id": parent["selected_model_id"],
            "runtime_package": "not_opened(열지 않음)",
            "new_mt5_execution": "not_run(미실행)",
            "runtime_authority": "not_claimed(주장 안 함)",
            "effect": "Python proxy(Python 프록시) 단서를 운영 주장(operating claim, 운영 주장)으로 올리지 않습니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]

    worst_side = side.sort_values("net_profit").head(8)
    best_side = side.sort_values("net_profit", ascending=False).head(8)
    side_rows: list[dict[str, Any]] = []
    for row in worst_side.to_dict("records"):
        side_rows.append(
            {
                "run_id": RUN_ID,
                "guardrail_id": f"bad_{row.get('split')}_{row.get('direction')}_{row.get('open_hour')}",
                "split": row.get("split"),
                "direction": row.get("direction"),
                "open_hour": row.get("open_hour"),
                "trade_count": row.get("trade_count"),
                "net_profit": finite(row.get("net_profit"), 6),
                "profit_factor": finite(row.get("profit_factor"), 10),
                "role": "risk_segment(위험 구간)",
                "effect": "ET에서 이 방향/시간 조합을 guard(가드) 또는 score penalty(점수 벌점) 후보로 씁니다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    for row in best_side.to_dict("records"):
        side_rows.append(
            {
                "run_id": RUN_ID,
                "guardrail_id": f"good_{row.get('split')}_{row.get('direction')}_{row.get('open_hour')}",
                "split": row.get("split"),
                "direction": row.get("direction"),
                "open_hour": row.get("open_hour"),
                "trade_count": row.get("trade_count"),
                "net_profit": finite(row.get("net_profit"), 6),
                "profit_factor": finite(row.get("profit_factor"), 10),
                "role": "salvage_segment(회수 구간)",
                "effect": "ET에서 유지할 세션/방향 단서로 씁니다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    month_rows: list[dict[str, Any]] = []
    for row in month.sort_values("net_profit").head(10).to_dict("records"):
        month_rows.append(
            {
                "run_id": RUN_ID,
                "review_id": f"month_{row.get('split')}_{row.get('open_month')}",
                "split": row.get("split"),
                "open_month": row.get("open_month"),
                "trade_count": row.get("trade_count"),
                "net_profit": finite(row.get("net_profit"), 6),
                "profit_factor": finite(row.get("profit_factor"), 10),
                "positive_month": row.get("positive_month"),
                "role": "bad_month_memory(나쁜 월 기억)",
                "effect": "ET에서 월별 안정성(month stability, 월 안정성)을 보고하되 월 필터만으로 과적합하지 않습니다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    for row in cost.to_dict("records"):
        month_rows.append(
            {
                "run_id": RUN_ID,
                "review_id": f"cost_{row.get('split')}_{row.get('cost_per_trade')}",
                "split": row.get("split"),
                "open_month": "",
                "trade_count": row.get("trade_count"),
                "net_profit": finite(row.get("net_profit"), 6),
                "profit_factor": finite(row.get("profit_factor"), 10),
                "positive_month": "",
                "role": "cost_stress_line(비용 압박 행)",
                "effect": "ET strict condition(ET 엄격 조건)에 cost0.6/cost0.9(비용0.6/0.9)를 유지합니다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    failure = [
        {
            "run_id": RUN_ID,
            "memory_id": "es_failure_density_cost_cross_split",
            "why_failed": "density>=3 and validation/OOS cost0.6 pass(밀도 3 이상과 검증/표본외 비용0.6 통과)를 동시에 만족한 row(행)가 0개입니다.",
            "salvage_value": f"best sparse edge(희소 우위) {high_pf_sparse_row.get('model_id', '')} has combined_cost09={finite(high_pf_sparse_row.get('combined_cost09_net', ''))}, min_pf={finite(min(as_float(high_pf_sparse_row.get('validation_profit_factor')), as_float(high_pf_sparse_row.get('oos_profit_factor'))))}",
            "reopen_condition": "density>=3, validation_cost06>=0, oos_cost06>0, combined_cost09>=0(밀도/검증 비용/표본외 비용/합산 비용 조건) 동시 통과",
            "do_not_repeat": "ER surface(ER 표면)에서 threshold(임계값)만 반복 조정하지 않습니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "memory_id": "es_failure_short_heavy_cost_thin",
            "why_failed": "selected combined short share(선택 합산 숏 비중)가 0.72보다 높고 cost0.9(비용0.9)가 음수입니다.",
            "salvage_value": "short 16/18 hour(숏 16/18시)와 long 16/20 hour(롱 16/20시)는 부분 salvage segment(회수 구간)입니다.",
            "reopen_condition": "short share<=0.72 with long recovery(숏 비중 0.72 이하와 롱 회복) 또는 cost0.9>=0",
            "do_not_repeat": "short_quality filter(숏 품질 필터)만 강하게 걸어 density(밀도)를 더 줄이지 않습니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "memory_id": "es_failure_dense_low_pf_surface",
            "why_failed": f"best density>=3 row(최고 밀도 3 이상 행)는 {best_density_row.get('model_id', '')}이고 combined_cost09={finite(best_density_row.get('combined_cost09_net', ''))}, short_share={finite(best_density_row.get('combined_short_share', ''))}입니다.",
            "salvage_value": "costside_dir_h3_m3 label(비용방향 h3 m3 라벨)은 density(밀도)를 회복하지만 PF/cost(수익 팩터/비용)가 약합니다.",
            "reopen_condition": "dense label(고밀도 라벨)에 cost-aware sample weight(비용 인식 표본 가중치)나 asymmetric payoff label(비대칭 보상 라벨)을 붙여야 합니다.",
            "do_not_repeat": "dense row(고밀도 행)를 trade-count(거래수)만 보고 후보로 올리지 않습니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]

    queue = [
        {
            "run_id": RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "queue_rank": 1,
            "queue_id": "et01_density_cost_short_balance_reseed",
            "hypothesis": "cost-weighted dense label(비용 가중 고밀도 라벨)과 side/session penalty(방향/세션 벌점)를 같이 쓰면 density>=3(밀도 3 이상)을 유지하면서 OOS cost0.6(표본외 비용0.6)과 short share(숏 비중)를 복구할 수 있습니다.",
            "seed_from": parent["selected_model_id"],
            "broad_sweep": "h2/h3/h4 label(라벨), target density 3-10(목표 밀도 3-10), cost0.6/cost0.9 score(비용 점수), side-hour guard(방향-시간 가드)",
            "extreme_sweep": "dense threshold 10/day(고밀도 10/일), short_share caps 0.60/0.70/0.75(숏 비중 상한), cost stress 0.9(비용 압박 0.9)",
            "success_gate": "validation_cost06>=0, oos_cost06>0, combined_cost09>=0, density>=3, short_share<=0.72, min_pf>=1.12(검증/표본외 비용, 합산 비용, 밀도, 숏 비중, 최소 PF 조건)",
            "effect": "ET는 ER 실패 조건을 score(점수)와 label(라벨)에 직접 넣는 공격 탐색입니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "queue_rank": 2,
            "queue_id": "et02_long_recovery_without_trade_splitting",
            "hypothesis": "long recovery segments(롱 회복 구간)을 살리면 short overweight(숏 과다)를 낮추면서 trade count(거래수)를 쪼개지 않고 유지할 수 있습니다.",
            "seed_from": rel(er.SIDE_SESSION_REVIEW),
            "broad_sweep": "long 16/20 salvage(롱 16/20 회수), short 20/21 veto(숏 20/21 차단), OOS long 17 penalty(OOS 롱 17시 벌점)",
            "extreme_sweep": "no side cap(방향 상한 없음) vs short cap 0.60(숏 상한 0.60)",
            "success_gate": "long/short balance(롱/숏 균형) improves without density<3(밀도 3 미만 없이 개선)",
            "effect": "side/session attribution(방향/세션 귀속)을 다음 모델 탐색 제약으로 바꿉니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    return summary, attribution, package, side_rows, month_rows, failure, queue


def write_work_packet() -> None:
    write_json(
        WORK_PACKET,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "primary_family": "kpi_evidence(KPI 근거)",
            "primary_skill": "obsidian-result-judgment(결과 판정)",
            "support_skills": [
                "obsidian-model-validation(모델 검증)",
                "obsidian-performance-attribution(성과 귀속)",
                "obsidian-artifact-lineage(산출물 계보)",
            ],
            "review_subject": PARENT_RUN_ID,
            "review_question": "Can ER open a runtime package(런타임 패키지), or must it become ET failure-memory seed(ET 실패 기억 씨앗)?",
            "decision_use": "Reject package(패키지 거절) unless strict candidate(엄격 후보) exists with density/cost/short/net stack(밀도/비용/숏/순수익 묶음).",
            "claim_boundary": CLAIM_BOUNDARY,
            "required_gates": [
                "input_lineage_gate",
                "parent_gate_inheritance_gate",
                "review_summary_gate",
                "failure_attribution_gate",
                "package_decision_gate",
                "next_queue_gate",
                "receipt_coverage_gate",
                "required_gate_coverage_audit",
                "final_claim_guard",
            ],
        },
    )


def build_final(parent: Mapping[str, Any], summary: Mapping[str, Any], created_at: str, gates: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "created_at_utc": created_at,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "claim_boundary": CLAIM_BOUNDARY,
        "selected_model_id": parent["selected_model_id"],
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
        "strict_candidate_count": parent["strict_candidate_count"],
        "operational_proxy_stack_pass_count": parent["operational_proxy_stack_pass_count"],
        "density_ge_3_count": summary["density_ge_3_count"],
        "density_cost_oos_count": summary["density_cost_oos_count"],
        "combined_cost09_ge0_count": summary["combined_cost09_ge0_count"],
        "min_pf_ge_1p21_count": summary["min_pf_ge_1p21_count"],
        "short_share_le_0p72_count": summary["short_share_le_0p72_count"],
        "strict_recomputed_count": summary["strict_recomputed_count"],
        "package_decision": "rejected(거절)",
        "runtime_package": "not_opened",
        "new_mt5_execution": "not_run",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "live_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "report_path": rel(REPORT_PATH),
        "final_decision": rel(FINAL_DECISION),
        "gate_passes": sum(1 for row in gates if row["status"] == "passed"),
        "gate_total": len(gates),
    }


def write_receipts(final: Mapping[str, Any], attribution: Sequence[Mapping[str, Any]]) -> None:
    base = {"run_id": RUN_ID, "stage_id": STAGE_ID, "created_at_utc": final["created_at_utc"], "claim_boundary": CLAIM_BOUNDARY}
    write_json(
        RESULT_RECEIPT,
        {
            **base,
            "result_subject": PARENT_RUN_ID,
            "evidence_available": [rel(REVIEW_SUMMARY), rel(FAILURE_ATTRIBUTION), rel(PACKAGE_DECISION), rel(FAILURE_MEMORY), rel(RUN364ET_QUEUE)],
            "evidence_missing": ["MT5 runtime package(MT5 런타임 패키지)", "MT5 runtime probe(MT5 런타임 탐침)", "forward/replay evidence(전진/재생 근거)"],
            "judgment_label": JUDGMENT,
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": NEXT_RUN_ID,
            "user_explanation_hook": "ER은 수익 단서가 있지만 밀도/비용/숏 비중이 동시에 깨져 패키지로 올리지 않습니다.",
        },
    )
    write_json(
        MODEL_RECEIPT,
        {
            **base,
            "model_family": "ExtraTrees/RandomForest(엑스트라트리/랜덤포레스트)",
            "selected_model_id": final["selected_model_id"],
            "target_and_label": "cost-aware 3-class direction label(비용 인식 3분류 방향 라벨)",
            "split_method": "chronological train/validation/OOS(시간순 학습/검증/표본외)",
            "selection_metric": "full trade tape replay KPI(전체 거래 테이프 재생 KPI)",
            "secondary_metrics": ["cost stress(비용 압박)", "side/session attribution(방향/세션 귀속)", "density floor(밀도 바닥)", "short share(숏 비중)"],
            "overfit_risk": "surface over-selection and threshold boundary(표면 과선택과 임계값 경계)",
            "validation_judgment": JUDGMENT,
        },
    )
    write_json(
        ATTRIBUTION_RECEIPT,
        {
            **base,
            "observed_change": f"combined net/density/cost09/short_share {final['selected_combined_net']}/{final['selected_combined_trade_density']}/{final['selected_combined_cost09_net']}/{final['selected_combined_short_share']}",
            "likely_drivers": [row["driver"] for row in attribution],
            "segment_checks": [rel(SIDE_SESSION_GUARDRAIL), rel(MONTH_COST_REVIEW)],
            "attribution_confidence": "medium_proxy_only(중간, 프록시 전용)",
            "next_probe": NEXT_RUN_ID,
        },
    )
    write_json(
        LINEAGE_RECEIPT,
        {
            **base,
            "source_inputs": [{"path": rel(path), "sha256": sha(path)} for path in INPUT_FILES if exists(path) and Path(path).is_file()],
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [rel(path) for path in OUTPUT_FILES if exists(path)],
            "artifact_hashes": {rel(path): sha(path) for path in OUTPUT_FILES if exists(path) and Path(path).is_file()},
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
            "effect": "ER proxy(ER 프록시) 결과를 운영 주장(operating claim, 운영 주장)으로 바꾸지 않습니다.",
        },
    )


def gate_rows(final_written: bool) -> list[dict[str, Any]]:
    parent_gates = read_csv(er.GATE_AUDIT)
    receipts = [RESULT_RECEIPT, MODEL_RECEIPT, ATTRIBUTION_RECEIPT, LINEAGE_RECEIPT, CLAIM_RECEIPT]
    checks = [
        ("input_lineage_gate", exists(INPUT_MANIFEST), INPUT_MANIFEST, "ER 입력 계보를 ES 검토에 연결했습니다."),
        ("parent_gate_inheritance_gate", not parent_gates.empty and all(parent_gates["status"].astype(str) == "passed"), er.GATE_AUDIT, "ER 게이트 통과 상태를 상속했습니다."),
        ("review_summary_gate", exists(REVIEW_SUMMARY), REVIEW_SUMMARY, "ER KPI(핵심 성과 지표)를 검토 요약으로 남겼습니다."),
        ("failure_attribution_gate", exists(FAILURE_ATTRIBUTION), FAILURE_ATTRIBUTION, "밀도/비용/숏 실패 원인을 분해했습니다."),
        ("side_session_guardrail_gate", exists(SIDE_SESSION_GUARDRAIL), SIDE_SESSION_GUARDRAIL, "방향/세션 귀속을 다음 제약으로 남겼습니다."),
        ("package_decision_gate", exists(PACKAGE_DECISION), PACKAGE_DECISION, "런타임 패키지 거절 근거를 기록했습니다."),
        ("failure_memory_gate", exists(FAILURE_MEMORY), FAILURE_MEMORY, "실패 기억과 재개 조건을 기록했습니다."),
        ("next_queue_gate", exists(RUN364ET_QUEUE), RUN364ET_QUEUE, "ET 탐색 대기열을 만들었습니다."),
        ("receipt_coverage_gate", all(exists(path) for path in receipts), RESULT_RECEIPT, "필수 receipt(영수증)가 있습니다."),
        ("required_gate_coverage_audit", final_written and exists(GATE_AUDIT), GATE_AUDIT, "필수 gate(게이트)가 종료 기록에 연결됐습니다."),
        ("final_claim_guard", True, CLAIM_RECEIPT, "권위/승격/실거래/목표 달성 주장을 차단했습니다."),
    ]
    rows = []
    for gate, passed, evidence, effect in checks:
        rows.append({"run_id": RUN_ID, "gate": gate, "status": "passed" if passed else "failed", "evidence": rel(evidence), "effect": effect, "claim_boundary": CLAIM_BOUNDARY})
    return rows


def write_docs(final: Mapping[str, Any], summary: Sequence[Mapping[str, Any]], attribution: Sequence[Mapping[str, Any]], package: Sequence[Mapping[str, Any]], failure: Sequence[Mapping[str, Any]], queue: Sequence[Mapping[str, Any]], gates: Sequence[Mapping[str, Any]]) -> None:
    report = f"""# run364ES OOS108 cost/side reseed review(OOS108 비용/방향 재시드 검토)

Created(생성): {final['created_at_utc']}

## Judgment(판정)

Action(행동): ER cost-side model/label/feature reseed(ER 비용/방향 모델/라벨/피처 재시드)를 package(패키지) 후보인지 검토했습니다.

Effect(효과): 수익 단서는 남기지만 density/cost/short/net(밀도/비용/숏/순수익) 묶음이 깨진 후보를 MT5 package(MT5 패키지)로 올리지 않습니다.

- judgment(판정): `{final['judgment']}`
- selected_model_id(선택 모델 ID): `{final['selected_model_id']}`
- validation net/PF/density(검증 순수익/PF/밀도): `{final['selected_validation_net']}` / `{final['selected_validation_profit_factor']}` / `{final['selected_validation_trade_density']}`
- OOS net/PF/density(표본외 순수익/PF/밀도): `{final['selected_oos_net']}` / `{final['selected_oos_profit_factor']}` / `{final['selected_oos_trade_density']}`
- combined net/density/cost0.9/short share(합산 순수익/밀도/비용0.9/숏 비중): `{final['selected_combined_net']}` / `{final['selected_combined_trade_density']}` / `{final['selected_combined_cost09_net']}` / `{final['selected_combined_short_share']}`
- package_decision(패키지 결정): `{final['package_decision']}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`

## Summary(요약)

{markdown_table(summary, ['selected_model_id', 'density_ge_3_count', 'density_cost_oos_count', 'combined_cost09_ge0_count', 'min_pf_ge_1p21_count', 'short_share_le_0p72_count', 'strict_recomputed_count'])}

## Attribution(귀속)

{markdown_table(attribution, ['attribution_id', 'observed', 'driver', 'severity', 'effect'])}

## Package Decision(패키지 결정)

{markdown_table(package, ['decision', 'reason', 'runtime_package', 'new_mt5_execution', 'effect'])}

## Failure Memory(실패 기억)

{markdown_table(failure, ['memory_id', 'why_failed', 'salvage_value', 'reopen_condition', 'do_not_repeat'])}

## Next Queue(다음 대기열)

{markdown_table(queue, ['queue_id', 'hypothesis', 'success_gate', 'effect'])}

## Gates(게이트)

{markdown_table(gates, ['gate', 'status', 'evidence', 'effect'])}

## Boundary(경계)

Runtime package(런타임 패키지), runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
"""
    decision_doc = f"""# Decision(결정): stage364ES cost/side reseed review(비용/방향 재시드 검토)

- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- package(패키지): `rejected(거절)`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Action(행동): ER 결과를 package decision(패키지 결정), failure memory(실패 기억), ET queue(ET 대기열)로 분리했습니다.

Effect(효과): 운영 주장(operating claim, 운영 주장)은 닫아두고, 다음 공격 탐색(offensive exploration, 공격 탐색)이 실패 조건을 직접 겨냥하게 합니다.
"""
    write_text(REPORT_PATH, report, bom=True)
    write_text(DECISION_DOC, decision_doc, bom=True)
    append_text_once(REVIEW_INDEX, f"run364ES__{RUN_ID}", f"\n- run364ES__{RUN_ID}: [{REPORT_PATH.name}]({REPORT_PATH.name}) - cost/side reseed review(비용/방향 재시드 검토), next `{NEXT_RUN_ID}`.\n")
    append_text_once(STAGE_BRIEF, f"run364ES__{RUN_ID}", f"\n<!-- run364ES__{RUN_ID} -->\n\n## run364ES Cost/Side Reseed Review(비용/방향 재시드 검토)\n\nAction(행동): ER 결과를 package(패키지)와 failure memory(실패 기억)로 분리했습니다.\n\nEffect(효과): `{NEXT_RUN_ID}`에서 density/cost/short balance(밀도/비용/숏 균형)를 직접 재탐색합니다.\n")
    append_text_once(STAGE_README, f"run364ES__{RUN_ID}", f"\n<!-- run364ES__{RUN_ID} -->\n## run364ES cost/side reseed review(비용/방향 재시드 검토)\n\nPackage(패키지): rejected(거절). Next(다음): `{NEXT_RUN_ID}`.\n")
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

Current truth(현재 진실): `run364ES` reviewed(검토 완료) ER cost/side reseed(ER 비용/방향 재시드). Selected validation/OOS net/PF/density(선택 검증/표본외 순수익/PF/밀도)는 `{final['selected_validation_net']}` / `{final['selected_validation_profit_factor']}` / `{final['selected_validation_trade_density']}` 및 `{final['selected_oos_net']}` / `{final['selected_oos_profit_factor']}` / `{final['selected_oos_trade_density']}`입니다.

Package truth(패키지 진실): strict candidate(엄격 후보)는 `{final['strict_candidate_count']}`개이고, density/cost/short/net(밀도/비용/숏/순수익) 묶음이 깨져 runtime package(런타임 패키지)는 not opened(열지 않음)입니다.

Next action(다음 행동): `{NEXT_RUN_ID}`에서 density/cost/short balance reseed(밀도/비용/숏 균형 재시드)를 실행합니다.

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

Latest review(최근 검토): ES cost/side reseed review(ES 비용/방향 재시드 검토)는 ER package(ER 패키지)를 rejected(거절)했습니다.

Selected validation net/PF/density(선택 검증 순수익/PF/밀도): `{final['selected_validation_net']}` / `{final['selected_validation_profit_factor']}` / `{final['selected_validation_trade_density']}`
Selected OOS net/PF/density(선택 표본외 순수익/PF/밀도): `{final['selected_oos_net']}` / `{final['selected_oos_profit_factor']}` / `{final['selected_oos_trade_density']}`

Next seed(다음 씨앗): density/cost/short balance reseed(밀도/비용/숏 균형 재시드).

Authority(권위): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""",
        bom=True,
    )
    append_text_once(WORKSPACE_CHANGELOG, f"run364ES__{RUN_ID}", f"\n<!-- run364ES__{RUN_ID} -->\n- {final['created_at_utc']} `{RUN_ID}` reviewed ER cost/side reseed(ER 비용/방향 재시드); package rejected(패키지 거절); next `{NEXT_RUN_ID}`; no authority claim(권위 주장 없음).\n")
    append_text_once(IDEA_REGISTRY, f"run364ES__{RUN_ID}", f"\n<!-- run364ES__{RUN_ID} -->\n- `{RUN_ID}`: ER 비용/방향 재시드는 density/cost/short(밀도/비용/숏) 묶음 실패로 package(패키지)에서 제외됐습니다. Effect(효과): ET는 cost-weighted dense label(비용 가중 고밀도 라벨)과 side/session penalty(방향/세션 벌점)를 직접 시험합니다.\n")
    append_text_once(NEGATIVE_REGISTER, f"run364ES__density_cost_short_failure__{RUN_ID}", f"\n<!-- run364ES__density_cost_short_failure__{RUN_ID} -->\n- `{RUN_ID}`: density>=3 and validation/OOS cost0.6 pass(밀도 3 이상과 검증/표본외 비용0.6 통과)를 동시에 만족한 row(행)가 0개라 package rejected(패키지 거절)입니다. Effect(효과): threshold micro-search(임계값 미세탐색) 반복 대신 ET에서 label/score(라벨/점수)를 다시 엽니다.\n")


def write_ledgers(final: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
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
        "gate_passes": final["gate_passes"],
        "gate_total": final["gate_total"],
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "created_at_utc": final["created_at_utc"],
        "required_gate_audit": rel(GATE_AUDIT),
        "question": "Should ER open package or become ET density/cost/short seed?(ER을 패키지로 열지, ET 밀도/비용/숏 씨앗으로 보낼지)",
        "next_action": NEXT_RUN_ID,
        "notes": f"density_cost_oos_count={final['density_cost_oos_count']};strict={final['strict_candidate_count']};package=rejected",
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
        row = {
            **common,
            "ledger_row_id": f"{RUN_ID}__{suffix}",
            "subrun_id": f"{RUN_ID}__{suffix}",
            "row_id": f"{RUN_ID}__{suffix}",
            "record_view": record_view,
            "tier_scope": tier_scope,
            "view": record_view,
            "tier": tier_scope,
            "kpi_scope": "ES cost/side reseed review(ES 비용/방향 재시드 검토)",
            "metric_scope": "proxy_review_no_mt5(프록시 검토, MT5 없음)",
            "status": status,
            "net_profit": final["selected_oos_net"] if suffix == "tier_a_separate" else "",
            "profit_factor": final["selected_oos_profit_factor"] if suffix == "tier_a_separate" else "",
            "trade_density": final["selected_oos_trade_density"] if suffix == "tier_a_separate" else "",
            "source_authority": "python_proxy_review_no_mt5(Python 프록시 검토, MT5 없음)",
        }
        rows.append(row)
    append_or_replace_csv(STAGE_LEDGER, ["ledger_row_id"], rows)
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], rows)
    append_or_replace_csv(
        RUN_REGISTRY,
        ["run_id"],
        [
            {
                **common,
                "run_family": "kpi_evidence(KPI 근거)",
                "run_type": "cost_side_reseed_review(비용/방향 재시드 검토)",
                "input_run_id": PARENT_RUN_ID,
                "output_path": rel(FINAL_DECISION),
                "result_path": rel(PACKAGE_DECISION),
                "selected_net_profit": final["selected_oos_net"],
                "selected_profit_factor": final["selected_oos_profit_factor"],
                "selected_trade_density": final["selected_oos_trade_density"],
            }
        ],
    )
    repair_run_registry_line_endings(RUN_ID)


def write_artifact_registry(final: Mapping[str, Any]) -> None:
    rows = []
    for path in OUTPUT_FILES:
        if exists(path) and Path(path).is_file():
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
                    "notes": "ES cost/side reseed review artifact(ES 비용/방향 재시드 검토 산출물)",
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
            "input_hashes": {rel(path): sha(path) for path in INPUT_FILES if exists(path) and Path(path).is_file()},
            "output_files": [rel(path) for path in outputs],
            "output_hashes": {rel(path): sha(path) for path in outputs if Path(path).is_file()},
        },
    )


def main() -> None:
    ensure_dirs()
    parent = validate_inputs()
    created_at = now_utc()
    write_csv(INPUT_MANIFEST, input_manifest_rows())
    write_work_packet()
    summary, attribution, package, side_rows, month_rows, failure, queue = build_tables(parent)
    write_csv(REVIEW_SUMMARY, summary)
    write_csv(FAILURE_ATTRIBUTION, attribution)
    write_csv(PACKAGE_DECISION, package)
    write_csv(SIDE_SESSION_GUARDRAIL, side_rows)
    write_csv(MONTH_COST_REVIEW, month_rows)
    write_csv(FAILURE_MEMORY, failure)
    write_csv(RUN364ET_QUEUE, queue)
    provisional = build_final(parent, summary[0], created_at, [])
    write_json(FINAL_DECISION, provisional)
    write_receipts(provisional, attribution)
    gates = gate_rows(final_written=False)
    write_csv(GATE_AUDIT, gates)
    gates = gate_rows(final_written=True)
    final = build_final(parent, summary[0], created_at, gates)
    write_json(FINAL_DECISION, final)
    write_csv(GATE_AUDIT, gates)
    write_docs(final, summary, attribution, package, failure, queue, gates)
    write_ledgers(final, gates)
    write_artifact_registry(final)
    write_manifest(final)
    write_receipts(final, attribution)
    print(json.dumps(json_ready({"run_id": RUN_ID, "status": STATUS, "judgment": JUDGMENT, "package_decision": "rejected", "next_run_id": NEXT_RUN_ID, "gate_passes": final["gate_passes"], "gate_total": final["gate_total"]}), ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
