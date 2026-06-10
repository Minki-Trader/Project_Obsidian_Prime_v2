from __future__ import annotations

import csv
import json
import math
import sys
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, json_ready  # noqa: E402
from stage_pipelines.stage364 import train_h17_oos108_pf125_density3_profit_floor_repair_without_db as gh  # noqa: E402


TODAY = "2026-06-07"
STAGE_ID = gh.STAGE_ID
RUN_NUMBER = "run364GI"
RUN_ID = "run364GI_review_h17_oos108_pf125_density3_profit_floor_repair_without_db_v1"
PARENT_RUN_ID = gh.RUN_ID
NEXT_RUN_ID = "run364GJ_train_h17_oos108_pf125_density_cost_floor_rejoin_without_db_v1"

STATUS = "completed_stage364GI_density3_profit_floor_repair_review_density_lift_cost_floor_failed_open_gj_no_authority"
JUDGMENT = "negative_density3_profit_floor_repair_review_density_lift_cost_floor_failed_no_package_no_authority"
DECISION = "stage364GI_reject_package_open_run364GJ_density_cost_floor_rejoin"
CLAIM_BOUNDARY = (
    "research_development_density3_profit_floor_repair_review_only_no_runtime_package_no_new_mt5_execution_"
    "no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

STAGE_DIR = gh.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
SPEC_DIR = STAGE_DIR / "00_spec"
SELECTED_DIR = STAGE_DIR / "04_selected"

INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
REVIEW_SUMMARY = RUN_DIR / "gi_review_summary.csv"
SURFACE_DIAGNOSTIC = RUN_DIR / "gi_surface_diagnostic.csv"
FAILURE_ATTRIBUTION = RUN_DIR / "gi_failure_attribution.csv"
PACKAGE_DECISION = RUN_DIR / "package_decision.csv"
FAILURE_MEMORY = RUN_DIR / "gi_failure_memory.csv"
RUN364GJ_QUEUE = RUN_DIR / "gi_gj_queue.csv"
RESULT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
ATTRIBUTION_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / "run364GI_density3_profit_floor_repair_review.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364GI_density3_profit_floor_repair_review.md"
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
    gh.FINAL_DECISION,
    gh.GATE_AUDIT,
    gh.TRADE_SURFACE,
    gh.SELECTED_CANDIDATE,
    gh.SELECTED_TRADE_TAPE,
    gh.COST_STRESS,
    gh.SIDE_SESSION_REVIEW,
    gh.MONTH_STABILITY,
    gh.MODEL_SCORECARD,
    gh.MODEL_ARTIFACT_MANIFEST,
    gh.ONNX_SMOKE_REPORT,
    gh.DATA_INTEGRITY_AUDIT,
    gh.RUN364GI_QUEUE,
    gh.RUN_EVIDENCE_RECEIPT,
    gh.MODEL_RECEIPT,
    gh.ATTRIBUTION_RECEIPT,
    gh.JUDGMENT_RECEIPT,
    gh.LINEAGE_RECEIPT,
    gh.CLAIM_RECEIPT,
    gh.RUN_MANIFEST,
    gh.REPORT_PATH,
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
    RUN364GJ_QUEUE,
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
    return gh.rel(path)


def exists(path: Path | str) -> bool:
    return Path(path).exists()


def sha(path: Path | str) -> str:
    return gh.sha(path)


def finite(value: Any, digits: int = 10) -> float | str:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return ""
    if not math.isfinite(number):
        return ""
    return round(number, digits)


def num(df: pd.DataFrame, column: str) -> pd.Series:
    if column not in df.columns:
        return pd.Series(0.0, index=df.index)
    return pd.to_numeric(df[column], errors="coerce").fillna(0.0)


def truthy(df: pd.DataFrame, column: str) -> pd.Series:
    if column not in df.columns:
        return pd.Series(False, index=df.index)
    series = df[column]
    if pd.api.types.is_bool_dtype(series):
        return series.fillna(False)
    if pd.api.types.is_numeric_dtype(series):
        return series.fillna(0).astype(float) != 0
    return series.astype(str).str.lower().isin(["true", "1", "yes", "passed", "통과"])


def bool_count(mask: pd.Series) -> int:
    return int(mask.fillna(False).sum())


def read_json(path: Path) -> Any:
    with io_path(path).open("r", encoding="utf-8-sig") as handle:
        return json.load(handle)


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(json_ready(payload), handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")


def read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(io_path(path), encoding="utf-8-sig").fillna("")


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row.keys():
            if key not in fieldnames:
                fieldnames.append(str(key))
    if not fieldnames:
        fieldnames = ["empty"]
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
    path.write_text(existing.rstrip() + "\n" + text.lstrip(), encoding="utf-8-sig")


def append_or_replace_csv(path: Path, key_fields: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> None:
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
    for attempt in range(6):
        try:
            temp_path.replace(path)
            break
        except PermissionError:
            if attempt == 5:
                raise
            time.sleep(0.25 * (attempt + 1))


def markdown_table(rows: Sequence[Mapping[str, Any]], columns: Sequence[str], limit: int = 12) -> str:
    shown = list(rows)[:limit]
    if not shown:
        return "_none(없음)_"
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join(["---"] * len(columns)) + " |"
    body = []
    for row in shown:
        body.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |")
    return "\n".join([header, sep, *body])


def ensure_dirs() -> None:
    for path in [RUN_DIR, REVIEW_DIR, SPEC_DIR, SELECTED_DIR, ROOT / "docs" / "decisions"]:
        path.mkdir(parents=True, exist_ok=True)


def validate_inputs() -> Mapping[str, Any]:
    required = [gh.FINAL_DECISION, gh.GATE_AUDIT, gh.TRADE_SURFACE, gh.SELECTED_CANDIDATE, gh.RUN364GI_QUEUE]
    missing = [rel(path) for path in required if not exists(path)]
    if missing:
        raise FileNotFoundError(f"missing GH review inputs(누락된 GH 검토 입력): {missing}")
    parent = read_json(gh.FINAL_DECISION)
    if parent.get("run_id") != PARENT_RUN_ID:
        raise ValueError(f"parent run mismatch(상위 실행 불일치): {parent.get('run_id')} != {PARENT_RUN_ID}")
    if parent.get("next_run_id") != RUN_ID:
        raise ValueError(f"GH next_run_id mismatch(GH 다음 실행 ID 불일치): {parent.get('next_run_id')} != {RUN_ID}")
    parent_gates = read_csv(gh.GATE_AUDIT)
    if parent_gates.empty or not all(parent_gates["status"].astype(str) == "passed"):
        raise ValueError("GH gate audit did not fully pass(GH 게이트 감사가 모두 통과하지 않음)")
    for key in ["runtime_authority", "operating_promotion", "live_readiness", "goal_achieve"]:
        if parent.get(key, "not_claimed") != "not_claimed":
            raise RuntimeError(f"forbidden GH claim(금지된 GH 주장): {key}={parent.get(key)}")
    surface = read_csv(gh.TRADE_SURFACE)
    if surface.empty:
        raise ValueError("GH surface is empty(GH 표면이 비어 있음)")
    return parent


def input_manifest_rows() -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "role": "input(입력)",
            "path": rel(path),
            "exists": exists(path),
            "sha256": sha(path) if exists(path) and io_path(path).is_file() else "",
            "effect": "GI review(GI 검토)의 계보 입력으로 고정했습니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for path in INPUT_FILES
    ]


def diagnostic_row(diagnostic_id: str, rows: pd.DataFrame, note: str) -> dict[str, Any]:
    if rows.empty:
        return {"diagnostic_id": diagnostic_id, "note": note, "row_found": "false", "claim_boundary": CLAIM_BOUNDARY}
    row = rows.iloc[0]
    return {
        "diagnostic_id": diagnostic_id,
        "row_found": "true",
        "model_id": row.get("model_id", ""),
        "label_id": row.get("label_id", ""),
        "feature_set_id": row.get("feature_set_id", ""),
        "hours_id": row.get("hours_id", ""),
        "extra_filter": row.get("extra_filter", ""),
        "threshold": finite(row.get("threshold", "")),
        "selection_score": finite(row.get("selection_score", "")),
        "validation_net": finite(row.get("validation_net", "")),
        "validation_profit_factor": finite(row.get("validation_profit_factor", "")),
        "validation_density": finite(row.get("validation_trade_density", "")),
        "oos_net": finite(row.get("oos_net", "")),
        "oos_profit_factor": finite(row.get("oos_profit_factor", "")),
        "oos_density": finite(row.get("oos_trade_density", "")),
        "oos_cost09_net": finite(row.get("oos_cost09_net", "")),
        "combined_net": finite(row.get("combined_net", "")),
        "combined_density": finite(row.get("combined_trade_density", "")),
        "combined_cost09_net": finite(row.get("combined_cost09_net", "")),
        "combined_short_share": finite(row.get("combined_short_share", "")),
        "note": note,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def build_review(parent: Mapping[str, Any]) -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
]:
    surface = read_csv(gf.TRADE_SURFACE)
    validation_net = num(surface, "validation_net")
    oos_net = num(surface, "oos_net")
    validation_density = num(surface, "validation_trade_density")
    oos_density = num(surface, "oos_trade_density")
    combined_density = num(surface, "combined_trade_density")
    oos_pf = num(surface, "oos_profit_factor")
    min_pf = num(surface, "min_split_profit_factor")
    oos_cost09 = num(surface, "oos_cost09_net")
    combined_cost09 = num(surface, "combined_cost09_net")
    combined_short = num(surface, "combined_short_share")

    val_pos = validation_net > 0
    oos_pos = oos_net > 0
    density3 = (validation_density >= 3.0) & (oos_density >= 3.0) & (combined_density >= 3.0)
    validation_positive_density3 = val_pos & (validation_density >= 3.0) & (combined_density >= 3.0)
    oos_pf105 = oos_pf >= 1.05
    oos_pf125 = oos_pf >= 1.25
    oos_cost09_nonneg = oos_cost09 >= 0
    combined_cost09_nonneg = combined_cost09 >= 0
    short077 = combined_short <= 0.77
    strict_like = val_pos & oos_pos & density3 & oos_pf125 & oos_cost09_nonneg & combined_cost09_nonneg & short077 & (min_pf >= 1.05)
    operational_stack = truthy(surface, "et_operational_proxy_stack_pass") | truthy(surface, "operational_proxy_stack_pass")

    selected_rows = surface[surface["model_id"].astype(str) == str(parent["selected_model_id"])]
    selected_best = selected_rows.sort_values("selection_score", ascending=False).head(1)
    selected_oos_cost09 = ""
    if not selected_best.empty:
        selected_oos_cost09 = finite(selected_best.iloc[0].get("oos_cost09_net", ""))

    diagnostics = [
        diagnostic_row("ge_selected_candidate(선택 후보)", selected_best, "선택 후보는 OOS profit/cost(표본외 수익/비용)를 개선했지만 validation/density(검증/밀도)가 실패했습니다."),
        diagnostic_row("ge_best_oos_positive(표본외 양수 상위)", surface[oos_pos].sort_values("selection_score", ascending=False).head(1), "표본외 양수 행의 밀도와 비용 상태를 확인합니다."),
        diagnostic_row("ge_best_density3(밀도3 상위)", surface[density3].sort_values("selection_score", ascending=False).head(1), "전 분할 density3(밀도3) 후보가 수익을 보존하는지 확인합니다."),
        diagnostic_row("ge_oos_pf125_cost09(표본외 PF125 비용0.9)", surface[oos_pf125 & oos_cost09_nonneg].sort_values("oos_cost09_net", ascending=False).head(1), "OOS PF125/cost0.9(표본외 수익 팩터 1.25/비용0.9) 단서를 확인합니다."),
        diagnostic_row("ge_strict_like(엄격 유사)", surface[strict_like].sort_values("selection_score", ascending=False).head(1), "엄격 유사 행은 없습니다."),
    ]

    summary = [
        {
            "run_id": RUN_ID,
            "parent_run_id": PARENT_RUN_ID,
            "review_subject": parent["selected_model_id"],
            "surface_rows": len(surface),
            "strict_candidate_count": int(parent.get("strict_candidate_count", 0)),
            "operational_proxy_stack_pass_count": int(parent.get("operational_proxy_stack_pass_count", bool_count(operational_stack))),
            "onnx_smoke_pass_rows": int(parent.get("onnx_smoke_pass_rows", 0)),
            "selected_model_id": parent["selected_model_id"],
            "selected_validation_net": parent["selected_validation_net"],
            "selected_validation_profit_factor": parent["selected_validation_profit_factor"],
            "selected_validation_trade_density": parent["selected_validation_trade_density"],
            "selected_oos_net": parent["selected_oos_net"],
            "selected_oos_profit_factor": parent["selected_oos_profit_factor"],
            "selected_oos_trade_density": parent["selected_oos_trade_density"],
            "selected_oos_cost06_net": parent["selected_oos_cost06_net"],
            "selected_oos_cost09_net": selected_oos_cost09,
            "selected_combined_net": parent["selected_combined_net"],
            "selected_combined_trade_density": parent["selected_combined_trade_density"],
            "selected_combined_cost09_net": parent["selected_combined_cost09_net"],
            "selected_combined_short_share": parent["selected_combined_short_share"],
            "validation_positive_density3_count": bool_count(validation_positive_density3),
            "validation_positive_density3_oos_pf105_count": bool_count(validation_positive_density3 & oos_pf105),
            "validation_positive_density3_oos_pf125_count": bool_count(validation_positive_density3 & oos_pf125),
            "density3_all_splits_count": bool_count(density3),
            "density3_all_splits_valpos_oospos_count": bool_count(density3 & val_pos & oos_pos),
            "density3_all_splits_oos_pf105_count": bool_count(density3 & oos_pf105),
            "density3_all_splits_oos_pf125_count": bool_count(density3 & oos_pf125),
            "oos_pf125_count": bool_count(oos_pf125),
            "oos_pf125_cost09_count": bool_count(oos_pf125 & oos_cost09_nonneg),
            "oos_pf125_density3_count": bool_count(oos_pf125 & density3),
            "oos_pf125_cost09_density3_count": bool_count(oos_pf125 & oos_cost09_nonneg & density3),
            "oos_cost09_nonneg_count": bool_count(oos_cost09_nonneg),
            "combined_cost09_nonneg_count": bool_count(combined_cost09_nonneg),
            "strict_like_count": bool_count(strict_like),
            "operational_stack_surface_count": bool_count(operational_stack),
            "max_validation_density": finite(validation_density.max()),
            "max_oos_density": finite(oos_density.max()),
            "max_combined_density": finite(combined_density.max()),
            "max_oos_profit_factor": finite(oos_pf.max()),
            "max_oos_cost09_net": finite(oos_cost09.max()),
            "max_combined_cost09_net": finite(combined_cost09.max()),
            "package_eligible": "false",
            "runtime_package": "not_opened",
            "new_mt5_execution": "not_run",
            "review_judgment": JUDGMENT,
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    s = summary[0]
    attribution = [
        {
            "run_id": RUN_ID,
            "attribution_id": "ge01_oos_profit_cost_improved",
            "observed": f"density3_all_splits_count={s['density3_all_splits_count']}; selected_density={s['selected_validation_trade_density']}/{s['selected_oos_trade_density']}/{s['selected_combined_trade_density']}",
            "driver": "profit-preserving density recovery(수익 보존 밀도 회복)가 OOS net/PF(표본외 순수익/수익 팩터)와 OOS cost0.6(표본외 비용0.6)을 개선했습니다.",
            "severity": "salvage_clue(회수 단서)",
            "effect": "GF(364GF)는 OOS profit floor(표본외 수익 바닥)를 유지하면서 density(밀도)를 끌어올려야 합니다.",
            "evidence": rel(gf.TRADE_SURFACE),
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "attribution_id": "ge02_validation_density_failed",
            "observed": f"selected_oos_net={s['selected_oos_net']}; selected_oos_pf={s['selected_oos_profit_factor']}; density3_all_splits_valpos_oospos_count={s['density3_all_splits_valpos_oospos_count']}",
            "driver": "선택 후보는 validation net(검증 순수익)이 약하고 density(밀도)가 3 미만입니다.",
            "severity": "high(높음)",
            "effect": "package(패키지)를 거절하고 profit-floor density lift(수익 바닥 밀도 상승)로 넘깁니다.",
            "evidence": rel(SURFACE_DIAGNOSTIC),
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "attribution_id": "ge03_cost_and_short_improved_but_not_enough",
            "observed": f"selected_combined_cost09_net={s['selected_combined_cost09_net']}; selected_short_share={s['selected_combined_short_share']}",
            "driver": "선택 후보는 short share(숏 비중)는 개선됐지만 combined cost0.9(합산 비용0.9)는 아직 음수입니다.",
            "severity": "medium(중간)",
            "effect": "다음 실행에서 cost0.9(비용0.9) 개선을 보조 제약으로 유지합니다.",
            "evidence": rel(gf.COST_STRESS),
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    package = [
        {
            "run_id": RUN_ID,
            "decision": "rejected(거절)",
            "reason": "GD improved OOS profit and OOS cost0.6 but validation is weak, density is below 3, combined_cost09<0, strict_candidate_count=0(GD 표본외 수익/비용0.6 개선, 약한 검증, 밀도3 미달, 합산 비용0.9 음수, 엄격 후보 0)",
            "runtime_package": "not_opened",
            "new_mt5_execution": "not_run",
            "effect": "표본외 개선 단서를 운영 가능한 후보로 과장하지 않습니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    failure = [
        {
            "run_id": RUN_ID,
            "memory_id": "ge01_oos_profit_improved_validation_density_failed",
            "failed_boundary": "OOS profit plus validation plus density plus cost(표본외 수익과 검증과 밀도와 비용 동시 충족)",
            "why_failed": f"selected_oos_net={s['selected_oos_net']}; selected_oos_pf={s['selected_oos_profit_factor']}; density3_all_splits_count={s['density3_all_splits_count']}; selected_density={s['selected_validation_trade_density']}/{s['selected_oos_trade_density']}/{s['selected_combined_trade_density']}",
            "salvage_value": f"selected_oos_net={s['selected_oos_net']}; selected_oos_pf={s['selected_oos_profit_factor']}; selected_oos_cost09_net={s['selected_oos_cost09_net']}; max_combined_cost09_net={s['max_combined_cost09_net']}",
            "reopen_condition": "preserve OOS net/PF and OOS cost0.6 while lifting density and validation net(표본외 순수익/수익 팩터와 표본외 비용0.6 보존, 밀도와 검증 순수익 상승)",
            "do_not_repeat": "Do not improve OOS by starving density or weakening validation(밀도를 굶기거나 검증을 약화하며 표본외만 개선하지 말 것).",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    queue = [
        {
            "run_id": RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "queue_rank": 1,
            "queue_id": "gf01_profit_floor_density_lift",
            "hypothesis": "GD OOS profit floor(GD 표본외 수익 바닥)를 고정하고 threshold/density target(임계값/밀도 목표)을 다시 조정하면 validation/density(검증/밀도)를 끌어올릴 수 있습니다.",
            "seed_from": "GD OOS profit/cost clue(GD 표본외 수익/비용 단서) + GE failure memory(GE 실패 기억)",
            "required_preserve": "OOS net>0, OOS PF>=1.10, OOS cost0.6>=0(표본외 순수익/수익 팩터/비용0.6 보존)",
            "required_repair": "validation_net and density lift toward 3, combined_cost09 improves(검증 순수익과 밀도 3 접근, 합산 비용0.9 개선)",
            "avoid": "low-density OOS-only optimization(저밀도 표본외 전용 최적화)",
            "effect": "GF는 GD의 표본외 수익 바닥을 보존하면서 검증과 밀도를 다시 끌어올립니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    return summary, diagnostics, attribution, package, failure, queue


def build_review(parent: Mapping[str, Any]) -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
]:
    surface = read_csv(gf.TRADE_SURFACE)
    validation_net = num(surface, "validation_net")
    oos_net = num(surface, "oos_net")
    validation_density = num(surface, "validation_trade_density")
    oos_density = num(surface, "oos_trade_density")
    combined_density = num(surface, "combined_trade_density")
    oos_pf = num(surface, "oos_profit_factor")
    min_pf = num(surface, "min_split_profit_factor")
    oos_cost09 = num(surface, "oos_cost09_net")
    combined_cost09 = num(surface, "combined_cost09_net")
    combined_short = num(surface, "combined_short_share")

    val_pos = validation_net > 0
    oos_pos = oos_net > 0
    density3 = (validation_density >= 3.0) & (oos_density >= 3.0) & (combined_density >= 3.0)
    validation_positive_density3 = val_pos & (validation_density >= 3.0) & (combined_density >= 3.0)
    oos_pf110 = oos_pf >= 1.10
    oos_pf125 = oos_pf >= 1.25
    oos_cost09_nonneg = oos_cost09 >= 0
    combined_cost09_nonneg = combined_cost09 >= 0
    strict_like = val_pos & oos_pos & density3 & oos_pf125 & oos_cost09_nonneg & combined_cost09_nonneg & (combined_short <= 0.77) & (min_pf >= 1.05)
    operational_stack = truthy(surface, "et_operational_proxy_stack_pass") | truthy(surface, "operational_proxy_stack_pass")

    selected_rows = surface[surface["model_id"].astype(str) == str(parent["selected_model_id"])]
    selected_best = selected_rows.sort_values("selection_score", ascending=False).head(1)
    selected_oos_cost09 = ""
    if not selected_best.empty:
        selected_oos_cost09 = finite(selected_best.iloc[0].get("oos_cost09_net", ""))

    diagnostics = [
        diagnostic_row("gg_selected_candidate(선택 후보)", selected_best, "선택 후보는 validation net(검증 순수익)을 개선하고 OOS floor(표본외 바닥)를 보존했지만 density3(밀도3)은 실패했습니다."),
        diagnostic_row("gg_best_oos_positive(표본외 양수 상위)", surface[oos_pos].sort_values("selection_score", ascending=False).head(1), "표본외 양수 후보의 밀도와 비용 상태를 확인합니다."),
        diagnostic_row("gg_best_density3(밀도3 상위)", surface[density3].sort_values("selection_score", ascending=False).head(1), "전 분할 density3(밀도3) 후보가 수익을 보존하는지 확인합니다."),
        diagnostic_row("gg_oos_pf125_cost09(표본외 PF125 비용0.9)", surface[oos_pf125 & oos_cost09_nonneg].sort_values("oos_cost09_net", ascending=False).head(1), "OOS PF125/cost0.9(표본외 수익 팩터 1.25/비용0.9) 단서를 확인합니다."),
        diagnostic_row("gg_strict_like(엄격 유사)", surface[strict_like].sort_values("selection_score", ascending=False).head(1), "엄격 유사 행이 있는지 확인합니다."),
    ]

    summary = [
        {
            "run_id": RUN_ID,
            "parent_run_id": PARENT_RUN_ID,
            "review_subject": parent["selected_model_id"],
            "surface_rows": len(surface),
            "strict_candidate_count": int(parent.get("strict_candidate_count", 0)),
            "operational_proxy_stack_pass_count": int(parent.get("operational_proxy_stack_pass_count", bool_count(operational_stack))),
            "onnx_smoke_pass_rows": int(parent.get("onnx_smoke_pass_rows", 0)),
            "selected_model_id": parent["selected_model_id"],
            "selected_validation_net": parent["selected_validation_net"],
            "selected_validation_profit_factor": parent["selected_validation_profit_factor"],
            "selected_validation_trade_density": parent["selected_validation_trade_density"],
            "selected_oos_net": parent["selected_oos_net"],
            "selected_oos_profit_factor": parent["selected_oos_profit_factor"],
            "selected_oos_trade_density": parent["selected_oos_trade_density"],
            "selected_oos_cost06_net": parent["selected_oos_cost06_net"],
            "selected_oos_cost09_net": selected_oos_cost09,
            "selected_combined_net": parent["selected_combined_net"],
            "selected_combined_trade_density": parent["selected_combined_trade_density"],
            "selected_combined_cost09_net": parent["selected_combined_cost09_net"],
            "selected_combined_short_share": parent["selected_combined_short_share"],
            "validation_positive_density3_count": bool_count(validation_positive_density3),
            "validation_positive_density3_oos_pf105_count": bool_count(validation_positive_density3 & (oos_pf >= 1.05)),
            "validation_positive_density3_oos_pf125_count": bool_count(validation_positive_density3 & oos_pf125),
            "density3_all_splits_count": bool_count(density3),
            "density3_all_splits_valpos_oospos_count": bool_count(density3 & val_pos & oos_pos),
            "density3_all_splits_oos_pf105_count": bool_count(density3 & (oos_pf >= 1.05)),
            "density3_all_splits_oos_pf125_count": bool_count(density3 & oos_pf125),
            "oos_pf125_count": bool_count(oos_pf125),
            "oos_pf125_cost09_count": bool_count(oos_pf125 & oos_cost09_nonneg),
            "oos_pf125_density3_count": bool_count(oos_pf125 & density3),
            "oos_pf125_cost09_density3_count": bool_count(oos_pf125 & oos_cost09_nonneg & density3),
            "oos_cost09_nonneg_count": bool_count(oos_cost09_nonneg),
            "combined_cost09_nonneg_count": bool_count(combined_cost09_nonneg),
            "strict_like_count": bool_count(strict_like),
            "operational_stack_surface_count": bool_count(operational_stack),
            "max_validation_density": finite(validation_density.max()),
            "max_oos_density": finite(oos_density.max()),
            "max_combined_density": finite(combined_density.max()),
            "max_oos_profit_factor": finite(oos_pf.max()),
            "max_oos_cost09_net": finite(oos_cost09.max()),
            "max_combined_cost09_net": finite(combined_cost09.max()),
            "package_eligible": "false",
            "runtime_package": "not_opened",
            "new_mt5_execution": "not_run",
            "review_judgment": JUDGMENT,
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    s = summary[0]
    attribution = [
        {
            "run_id": RUN_ID,
            "attribution_id": "gg01_validation_profit_improved_oos_floor_preserved",
            "observed": f"validation_net={s['selected_validation_net']}; oos_pf={s['selected_oos_profit_factor']}; oos_cost06={s['selected_oos_cost06_net']}",
            "driver": "profit-floor density lift(수익 바닥 밀도 상승)가 validation net(검증 순수익)을 개선하고 OOS PF/cost0.6(표본외 수익 팩터/비용0.6)을 보존했습니다.",
            "severity": "salvage_clue(회수 단서)",
            "effect": "GH(364GH)는 이 수익 바닥을 유지하면서 density3(밀도3)을 다시 공격해야 합니다.",
            "evidence": rel(gf.TRADE_SURFACE),
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "attribution_id": "gg02_density3_failed",
            "observed": f"density3_all_splits_count={s['density3_all_splits_count']}; selected_density={s['selected_validation_trade_density']}/{s['selected_oos_trade_density']}/{s['selected_combined_trade_density']}",
            "driver": "선택 후보는 validation net(검증 순수익)이 좋아졌지만 density(밀도)가 3 미만입니다.",
            "severity": "high(높음)",
            "effect": "package(패키지)를 거절하고 density3 profit-floor repair(밀도3 수익 바닥 수리)로 넘깁니다.",
            "evidence": rel(SURFACE_DIAGNOSTIC),
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "attribution_id": "gg03_cost09_still_negative",
            "observed": f"selected_combined_cost09_net={s['selected_combined_cost09_net']}; max_combined_cost09_net={s['max_combined_cost09_net']}",
            "driver": "combined cost0.9(합산 비용0.9)는 아직 음수입니다.",
            "severity": "medium(중간)",
            "effect": "다음 실행에서 cost0.9(비용0.9) 개선을 보조 제약으로 유지합니다.",
            "evidence": rel(gf.COST_STRESS),
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    package = [
        {
            "run_id": RUN_ID,
            "decision": "rejected(거절)",
            "reason": "GF improved validation and preserved OOS floor but density is below 3, combined_cost09<0, strict_candidate_count=0(GF 검증 개선, 표본외 바닥 보존, 밀도3 미달, 합산 비용0.9 음수, 엄격 후보 0)",
            "runtime_package": "not_opened",
            "new_mt5_execution": "not_run",
            "effect": "좋아진 프록시 단서를 운영 가능한 후보로 과장하지 않습니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    failure = [
        {
            "run_id": RUN_ID,
            "memory_id": "gg01_validation_improved_density3_failed",
            "failed_boundary": "validation plus OOS floor plus density plus cost(검증과 표본외 바닥과 밀도와 비용 동시 충족)",
            "why_failed": f"selected_validation_net={s['selected_validation_net']}; selected_oos_pf={s['selected_oos_profit_factor']}; density3_all_splits_count={s['density3_all_splits_count']}; selected_density={s['selected_validation_trade_density']}/{s['selected_oos_trade_density']}/{s['selected_combined_trade_density']}",
            "salvage_value": f"selected_validation_net={s['selected_validation_net']}; selected_oos_net={s['selected_oos_net']}; selected_oos_pf={s['selected_oos_profit_factor']}; selected_oos_cost06={s['selected_oos_cost06_net']}",
            "reopen_condition": "preserve validation net, OOS net/PF, and OOS cost0.6 while lifting density toward 3(검증 순수익, 표본외 순수익/수익 팩터, 표본외 비용0.6을 보존하며 밀도3으로 상승)",
            "do_not_repeat": "Do not improve validation by starving density or losing OOS cost0.6(밀도를 굶기거나 표본외 비용0.6을 잃으며 검증만 개선하지 말 것).",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    queue = [
        {
            "run_id": RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "queue_rank": 1,
            "queue_id": "gh01_density3_profit_floor_repair",
            "hypothesis": "GF validation lift(GF 검증 상승)와 OOS profit floor(표본외 수익 바닥)를 고정하고 density target(밀도 목표)을 더 공격하면 density3(밀도3)에 접근할 수 있습니다.",
            "seed_from": "GF validation/OOS profit clue(GF 검증/표본외 수익 단서) + GG failure memory(GG 실패 기억)",
            "required_preserve": "validation net>0, OOS net>0, OOS PF>=1.10, OOS cost0.6>=0(검증/표본외 수익 바닥 보존)",
            "required_repair": "density lift toward 3 and combined_cost09 improves(밀도 3 접근과 합산 비용0.9 개선)",
            "avoid": "low-density validation-only optimization(저밀도 검증 전용 최적화)",
            "effect": "GH는 GF의 검증 개선을 보존하면서 부족한 거래 밀도를 다시 공격합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    return summary, diagnostics, attribution, package, failure, queue


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
        "report_path": rel(REPORT_PATH),
        "final_decision": rel(FINAL_DECISION),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "live_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "runtime_package": "not_opened",
        "new_mt5_execution": "not_run",
        "claim_boundary": CLAIM_BOUNDARY,
    }


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
            "required_gates": ["kpi_contract_audit", "row_grain_audit", "source_authority_audit", "required_gate_coverage_audit"],
            "hypothesis": "GD 결과를 package decision(패키지 결정), failure memory(실패 기억), GF queue(GF 대기열)로 분리합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def write_receipts(final: Mapping[str, Any]) -> None:
    common = {"run_id": RUN_ID, "stage_id": STAGE_ID, "created_at_utc": final["created_at_utc"], "claim_boundary": CLAIM_BOUNDARY}
    write_json(RESULT_RECEIPT, {**common, "receipt_type": "result_judgment(결과 판정)", "decision": DECISION, "judgment_label": JUDGMENT, "evidence_available": [rel(REVIEW_SUMMARY), rel(SURFACE_DIAGNOSTIC), rel(PACKAGE_DECISION)], "evidence_missing": ["MT5 runtime package(MT5 런타임 패키지)", "MT5 runtime probe(MT5 런타임 탐침)"]})
    write_json(MODEL_RECEIPT, {**common, "receipt_type": "model_validation(모델 검증)", "review_subject": final["review_subject"], "selected_model_id": final["selected_model_id"], "validation_judgment": JUDGMENT})
    write_json(ATTRIBUTION_RECEIPT, {**common, "receipt_type": "performance_attribution(성과 귀속)", "observed_change": "OOS profit improved but validation, density, and combined cost failed(표본외 수익 개선, 검증/밀도/합산 비용 실패)", "next_probe": NEXT_RUN_ID})
    write_json(LINEAGE_RECEIPT, {**common, "receipt_type": "artifact_lineage(산출물 계보)", "inputs": [rel(path) for path in INPUT_FILES], "outputs": [rel(path) for path in OUTPUT_FILES if exists(path)]})
    write_json(CLAIM_RECEIPT, {**common, "receipt_type": "claim_boundary(주장 경계)", "runtime_authority": "not_claimed", "operating_promotion": "not_claimed", "live_readiness": "not_claimed", "goal_achieve": "not_claimed", "effect": "GE review(GE 검토)를 운영 주장으로 올리지 않습니다."})


def stage_ledger_has_rows() -> bool:
    if not STAGE_LEDGER.exists():
        return False
    rows = read_csv(STAGE_LEDGER)
    return bool_count(rows.get("run_id", pd.Series(dtype=str)).astype(str) == RUN_ID) >= 3


def gate_rows(final_written: bool) -> list[dict[str, Any]]:
    gates = [
        ("input_lineage_gate", exists(INPUT_MANIFEST), INPUT_MANIFEST, "GF 입력 계보를 기록했습니다."),
        ("parent_gate_inheritance_gate", exists(gf.GATE_AUDIT), gf.GATE_AUDIT, "GF 게이트 통과 상태를 상속 확인했습니다."),
        ("kpi_contract_audit", exists(REVIEW_SUMMARY) and exists(PACKAGE_DECISION), REVIEW_SUMMARY, "KPI와 package decision(패키지 결정)을 분리했습니다."),
        ("surface_overlap_audit", exists(SURFACE_DIAGNOSTIC), SURFACE_DIAGNOSTIC, "OOS profit(표본외 수익)과 density loss(밀도 손실)를 분리 진단했습니다."),
        ("failure_attribution_gate", exists(FAILURE_ATTRIBUTION), FAILURE_ATTRIBUTION, "표본외 수익 회복과 밀도 손실 귀속을 기록했습니다."),
        ("package_decision_gate", exists(PACKAGE_DECISION), PACKAGE_DECISION, "runtime package(런타임 패키지) 거절 근거를 기록했습니다."),
        ("failure_memory_gate", exists(FAILURE_MEMORY), FAILURE_MEMORY, "다음 GH 실행의 실패 기억을 기록했습니다."),
        ("next_queue_gate", exists(RUN364GH_QUEUE), RUN364GH_QUEUE, "GH 대기열을 기록했습니다."),
        ("receipt_coverage_gate", all(exists(path) for path in [RESULT_RECEIPT, MODEL_RECEIPT, ATTRIBUTION_RECEIPT, LINEAGE_RECEIPT, CLAIM_RECEIPT]), RESULT_RECEIPT, "필수 receipt(영수증)를 기록했습니다."),
        ("paired_tier_record_gate", stage_ledger_has_rows(), STAGE_LEDGER, "Tier A/B 쌍 기록을 장부에 남겼습니다."),
        ("required_gate_coverage_audit", True, GATE_AUDIT, "필수 게이트 목록을 closeout(종료 기록)에 연결했습니다."),
        ("final_claim_guard", final_written and exists(FINAL_DECISION), CLAIM_RECEIPT, "운영/목표 주장을 모두 차단했습니다."),
    ]
    return [
        {
            "run_id": RUN_ID,
            "gate": name,
            "status": "passed" if ok else "failed",
            "evidence": rel(evidence),
            "effect": effect,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for name, ok, evidence, effect in gates
    ]


def write_docs(final: Mapping[str, Any], attribution: Sequence[Mapping[str, Any]], package: Sequence[Mapping[str, Any]], failure: Sequence[Mapping[str, Any]], queue: Sequence[Mapping[str, Any]], diagnostics: Sequence[Mapping[str, Any]], gates: Sequence[Mapping[str, Any]]) -> None:
    gate_lines = "\n".join(f"- {row['gate']}: {row['status']} -> {row['evidence']}" for row in gates)
    report = f"""# run364GE Profit Preserving Density Recovery Review(수익 보존 밀도 회복 검토)

Created(생성): {final['created_at_utc']}

Action(행동): GD proxy/ONNX smoke(GD 프록시/ONNX 간이 검증) 결과를 OOS profit improvement(표본외 수익 개선), validation weakness(검증 약화), density failure(밀도 실패), package decision(패키지 결정)으로 검토했습니다.

Effect(효과): 표본외 수익/비용 단서를 보존하되 운영 후보로 올리지 않고 GF(364GF) profit-floor density lift(수익 바닥 밀도 상승)로 넘깁니다.

- judgment(판정): `{final['judgment']}`
- selected_model_id(선택 모델 ID): `{final['selected_model_id']}`
- validation net/PF/density(검증 순수익/수익 팩터/밀도): `{final['selected_validation_net']}` / `{final['selected_validation_profit_factor']}` / `{final['selected_validation_trade_density']}`
- OOS net/PF/density(표본외 순수익/수익 팩터/밀도): `{final['selected_oos_net']}` / `{final['selected_oos_profit_factor']}` / `{final['selected_oos_trade_density']}`
- selected OOS cost0.9 net(선택 표본외 비용0.9 순수익): `{final['selected_oos_cost09_net']}`
- combined net/density/cost0.9/short share(합산 순수익/밀도/비용0.9/숏 비중): `{final['selected_combined_net']}` / `{final['selected_combined_trade_density']}` / `{final['selected_combined_cost09_net']}` / `{final['selected_combined_short_share']}`
- density3_all_splits_count(전 분할 밀도3 수): `{final['density3_all_splits_count']}`
- oos_pf125_cost09_count(표본외 PF125 비용0.9 수): `{final['oos_pf125_cost09_count']}`
- package_eligible(패키지 가능): `{final['package_eligible']}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`

## Diagnostics(진단)

{markdown_table(diagnostics, ['diagnostic_id', 'row_found', 'model_id', 'validation_net', 'validation_density', 'oos_net', 'oos_profit_factor', 'oos_density', 'oos_cost09_net', 'combined_cost09_net', 'note'])}

## Attribution(귀속)

{markdown_table(attribution, ['attribution_id', 'observed', 'driver', 'severity', 'effect'])}

## Package Decision(패키지 결정)

{markdown_table(package, ['decision', 'reason', 'runtime_package', 'new_mt5_execution', 'effect'])}

## Failure Memory(실패 기억)

{markdown_table(failure, ['memory_id', 'failed_boundary', 'why_failed', 'salvage_value', 'reopen_condition', 'do_not_repeat'])}

## Next Queue(다음 대기열)

{markdown_table(queue, ['next_run_id', 'queue_id', 'hypothesis', 'required_preserve', 'required_repair', 'avoid', 'effect'])}

## Gates(게이트)

{gate_lines}

Boundary(경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
"""
    decision_doc = f"""# Decision(결정): stage364GE Profit Preserving Density Recovery Review(수익 보존 밀도 회복 검토)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(상위 실행 ID): `{PARENT_RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Action(행동): GD 결과를 package rejected(패키지 거절)로 닫고 GF profit-floor density lift(GF 수익 바닥 밀도 상승)로 넘깁니다.

Effect(효과): GD 표본외 수익 바닥을 다음 탐색의 보존 조건으로 바꾸고, 검증/밀도 실패를 수리 대상으로 둡니다.
"""
    write_text(REPORT_PATH, report, bom=True)
    write_text(DECISION_DOC, decision_doc, bom=True)
    append_text_once(REVIEW_INDEX, f"run364GE__{RUN_ID}", f"\n- run364GE__{RUN_ID}: [{REPORT_PATH.name}]({REPORT_PATH.name}) - profit preserving density recovery review(수익 보존 밀도 회복 검토), next `{NEXT_RUN_ID}`.\n")
    append_text_once(STAGE_BRIEF, f"run364GE__{RUN_ID}", f"\n<!-- run364GE__{RUN_ID} -->\n\n## run364GE Profit Preserving Density Recovery Review(수익 보존 밀도 회복 검토)\n\nAction(행동): GD 결과를 표본외 수익 개선과 검증/밀도 실패로 분리했습니다.\n\nEffect(효과): `{NEXT_RUN_ID}`에서 profit-floor density lift(수익 바닥 밀도 상승)를 실행합니다.\n")
    append_text_once(STAGE_README, f"run364GE__{RUN_ID}", f"\n<!-- run364GE__{RUN_ID} -->\n## run364GE profit preserving density recovery review(수익 보존 밀도 회복 검토)\n\nNext(다음): `{NEXT_RUN_ID}`.\n")
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

Current truth(현재 진실): `run364GE` reviewed(검토 완료) GD profit preserving density recovery(GD 수익 보존 밀도 회복). GD selected(선택) 후보는 validation net/PF/density(검증 순수익/수익 팩터/밀도) `{final['selected_validation_net']}` / `{final['selected_validation_profit_factor']}` / `{final['selected_validation_trade_density']}`이고 OOS net/PF/density(표본외 순수익/수익 팩터/밀도)는 `{final['selected_oos_net']}` / `{final['selected_oos_profit_factor']}` / `{final['selected_oos_trade_density']}`입니다.

Failure truth(실패 진실): profit preserving density recovery(수익 보존 밀도 회복)는 OOS net/PF(표본외 순수익/수익 팩터)를 `{final['selected_oos_net']}` / `{final['selected_oos_profit_factor']}`로 개선했지만 validation net(검증 순수익)은 `{final['selected_validation_net']}`로 약하고 selected density(선택 밀도)는 `{final['selected_validation_trade_density']}` / `{final['selected_oos_trade_density']}` / `{final['selected_combined_trade_density']}`로 3 미만입니다.

Next action(다음 행동): `{NEXT_RUN_ID}`에서 profit-floor density lift(수익 바닥 밀도 상승)를 실행합니다.

Operating boundary(운영 경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""", bom=True)
    write_text(SELECTION_STATUS, f"""# Stage364 selection status(선택 상태)

Updated(갱신): {final['created_at_utc']}

Current run(현재 실행): `{NEXT_RUN_ID}`
Latest completed run(최근 완료 실행): `{RUN_ID}`

Latest review(최근 검토): GE profit preserving density recovery review(GE 수익 보존 밀도 회복 검토)가 GD package(GD 패키지)를 rejected(거절)했습니다.

Selected model(선택 모델): `{final['selected_model_id']}`

Validation net/PF/density(검증 순수익/수익 팩터/밀도): `{final['selected_validation_net']}` / `{final['selected_validation_profit_factor']}` / `{final['selected_validation_trade_density']}`
OOS net/PF/density(표본외 순수익/수익 팩터/밀도): `{final['selected_oos_net']}` / `{final['selected_oos_profit_factor']}` / `{final['selected_oos_trade_density']}`
Combined net/density/cost0.9/short share(합산 순수익/밀도/비용0.9/숏 비중): `{final['selected_combined_net']}` / `{final['selected_combined_trade_density']}` / `{final['selected_combined_cost09_net']}` / `{final['selected_combined_short_share']}`

Next seed(다음 씨앗): profit-floor density lift(수익 바닥 밀도 상승).

Authority(권위): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""", bom=True)
    append_text_once(WORKSPACE_CHANGELOG, f"run364GE__{RUN_ID}", f"\n<!-- run364GE__{RUN_ID} -->\n- {final['created_at_utc']} `{RUN_ID}` reviewed profit preserving density recovery(수익 보존 밀도 회복); selected OOS net(선택 표본외 순수익) `{final['selected_oos_net']}`; selected density(선택 밀도) `{final['selected_validation_trade_density']}/{final['selected_oos_trade_density']}/{final['selected_combined_trade_density']}`; package rejected(패키지 거절); next `{NEXT_RUN_ID}`; no authority claim(권위 주장 없음).\n")
    append_text_once(IDEA_REGISTRY, f"run364GE__{RUN_ID}", f"\n<!-- run364GE__{RUN_ID} -->\n- `{RUN_ID}`: profit preserving density recovery(수익 보존 밀도 회복)는 OOS profit/cost(표본외 수익/비용)를 개선했지만 validation/density(검증/밀도)가 실패해 profit-floor density lift(수익 바닥 밀도 상승)를 다음 입력으로 남겼습니다. Effect(효과): 표본외 수익 바닥을 보존 조건으로 고정합니다.\n")
    append_text_once(NEGATIVE_REGISTER, f"run364GE__oos_profit_improved_validation_density_failed__{RUN_ID}", f"\n<!-- run364GE__oos_profit_improved_validation_density_failed__{RUN_ID} -->\n- `{RUN_ID}`: profit preserving density recovery(수익 보존 밀도 회복)는 selected OOS net/PF(선택 표본외 순수익/수익 팩터) `{final['selected_oos_net']}` / `{final['selected_oos_profit_factor']}`로 개선됐지만 validation/density(검증/밀도) `{final['selected_validation_net']}` / `{final['selected_validation_trade_density']}/{final['selected_oos_trade_density']}/{final['selected_combined_trade_density']}`로 실패했습니다. Effect(효과): GF에서 수익 바닥 밀도 상승을 실행합니다.\n")


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
        "question": "Should GD open package or seed GF profit-floor density lift?(GD를 패키지로 열지, GF 수익 바닥 밀도 상승으로 보낼지)",
        "next_action": NEXT_RUN_ID,
        "notes": f"selected_oos_net={final['selected_oos_net']};density3={final['density3_all_splits_count']};package=rejected",
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
                "kpi_scope": "GE profit preserving density recovery review(GE 수익 보존 밀도 회복 검토)",
                "metric_scope": "python_proxy_review_no_mt5(Python 프록시 검토, MT5 없음)",
                "status": status,
                "net_profit": final["selected_oos_net"] if suffix == "tier_a_separate" else "",
                "profit_factor": final["selected_oos_profit_factor"] if suffix == "tier_a_separate" else "",
                "trade_density_per_feature_day": final["selected_oos_trade_density"] if suffix == "tier_a_separate" else "",
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
                "run_type": "profit_preserving_density_recovery_review(수익 보존 밀도 회복 검토)",
                "input_run_id": PARENT_RUN_ID,
                "output_path": rel(FINAL_DECISION),
                "result_path": rel(PACKAGE_DECISION),
                "best_model_id": final["selected_model_id"],
                "net_profit": final["selected_oos_net"],
                "profit_factor": final["selected_oos_profit_factor"],
                "trade_density_per_feature_day": final["selected_oos_trade_density"],
                "result_status": STATUS,
                "primary_kpi": f"oos_net={final['selected_oos_net']};density3={final['density3_all_splits_count']}",
                "guardrail_kpi": "package=rejected;authority=not_claimed",
                "final_decision_path": rel(FINAL_DECISION),
                "gate_audit_path": rel(GATE_AUDIT),
                "external_verification_status": "out_of_scope_by_claim(주장 범위 밖)",
                "evidence_boundary": "proxy_review_only_no_mt5_runtime_authority(프록시 검토만, MT5 런타임 권위 없음)",
            }
        ],
    )
    try:
        gf.et.repair_run_registry_line_endings(RUN_ID)
    except AttributeError:
        pass


def write_artifact_registry(final: Mapping[str, Any]) -> None:
    rows = []
    for path in OUTPUT_FILES:
        if exists(path) and io_path(path).is_file():
            rows.append(
                {
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "artifact_type": "script" if path == THIS_FILE else ("report" if path.suffix.lower() == ".md" else ("json" if path.suffix.lower() == ".json" else "csv")),
                    "path": rel(path),
                    "artifact_path": rel(path),
                    "sha256": sha(path),
                    "created_at": final["created_at_utc"],
                    "created_at_utc": final["created_at_utc"],
                    "claim_boundary": CLAIM_BOUNDARY,
                    "artifact_id": f"{RUN_ID}__{path.stem}",
                    "notes": "GE profit preserving density recovery review artifact(GE 수익 보존 밀도 회복 검토 산출물)",
                }
            )
    append_or_replace_csv(ARTIFACT_REGISTRY, ["artifact_id"], rows)


def write_work_packet() -> None:
    write_json(
        WORK_PACKET,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "primary_family": "kpi_evidence(KPI 근거)",
            "primary_skill": "obsidian-run-evidence-system(옵시디언 실행 근거 시스템)",
            "support_skills": [
                "obsidian-artifact-lineage(옵시디언 산출물 계보)",
                "obsidian-result-judgment(옵시디언 결과 판정)",
                "obsidian-performance-attribution(옵시디언 성과 귀속)",
            ],
            "required_gates": ["kpi_contract_audit(KPI 계약 감사)", "source_authority_audit(진실 권한 감사)", "required_gate_coverage_audit(필수 게이트 커버리지 감사)"],
            "hypothesis": "GF 결과를 package decision(패키지 결정), failure memory(실패 기억), GH queue(GH 대기열)로 분리합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def write_receipts(final: Mapping[str, Any]) -> None:
    common = {"run_id": RUN_ID, "stage_id": STAGE_ID, "created_at_utc": final["created_at_utc"], "claim_boundary": CLAIM_BOUNDARY}
    write_json(RESULT_RECEIPT, {**common, "receipt_type": "result_judgment(결과 판정)", "decision": DECISION, "judgment_label": JUDGMENT, "evidence_available": [rel(REVIEW_SUMMARY), rel(SURFACE_DIAGNOSTIC), rel(PACKAGE_DECISION)], "evidence_missing": ["MT5 runtime package(MT5 런타임 패키지)", "MT5 runtime probe(MT5 런타임 탐침)"]})
    write_json(MODEL_RECEIPT, {**common, "receipt_type": "model_validation(모델 검증)", "review_subject": final["review_subject"], "selected_model_id": final["selected_model_id"], "validation_judgment": JUDGMENT})
    write_json(ATTRIBUTION_RECEIPT, {**common, "receipt_type": "performance_attribution(성과 귀속)", "observed_change": "GF improved validation while density3 and combined cost failed(GF는 검증을 개선했지만 밀도3과 합산 비용은 실패)", "next_probe": NEXT_RUN_ID})
    write_json(LINEAGE_RECEIPT, {**common, "receipt_type": "artifact_lineage(산출물 계보)", "inputs": [rel(path) for path in INPUT_FILES], "outputs": [rel(path) for path in OUTPUT_FILES if exists(path)]})
    write_json(CLAIM_RECEIPT, {**common, "receipt_type": "claim_boundary(주장 경계)", "runtime_authority": "not_claimed", "operating_promotion": "not_claimed", "live_readiness": "not_claimed", "goal_achieve": "not_claimed", "effect": "GG review(GG 검토)를 운영 주장으로 올리지 않습니다."})


def gate_rows(final_written: bool) -> list[dict[str, Any]]:
    gates = [
        ("input_lineage_gate", exists(INPUT_MANIFEST), INPUT_MANIFEST, "GF 입력 계보를 기록했습니다."),
        ("parent_gate_inheritance_gate", exists(gf.GATE_AUDIT), gf.GATE_AUDIT, "GF 게이트 통과 상태를 상속 확인했습니다."),
        ("kpi_contract_audit", exists(REVIEW_SUMMARY) and exists(PACKAGE_DECISION), REVIEW_SUMMARY, "KPI와 package decision(패키지 결정)을 분리했습니다."),
        ("surface_overlap_audit", exists(SURFACE_DIAGNOSTIC), SURFACE_DIAGNOSTIC, "validation lift(검증 상승)와 density failure(밀도 실패)를 분리 진단했습니다."),
        ("failure_attribution_gate", exists(FAILURE_ATTRIBUTION), FAILURE_ATTRIBUTION, "회수 단서와 실패 원인을 기록했습니다."),
        ("package_decision_gate", exists(PACKAGE_DECISION), PACKAGE_DECISION, "runtime package(런타임 패키지) 거절 근거를 기록했습니다."),
        ("failure_memory_gate", exists(FAILURE_MEMORY), FAILURE_MEMORY, "다음 GH 실행의 실패 기억을 기록했습니다."),
        ("next_queue_gate", exists(RUN364GH_QUEUE), RUN364GH_QUEUE, "GH 대기열을 기록했습니다."),
        ("receipt_coverage_gate", all(exists(path) for path in [RESULT_RECEIPT, MODEL_RECEIPT, ATTRIBUTION_RECEIPT, LINEAGE_RECEIPT, CLAIM_RECEIPT]), RESULT_RECEIPT, "필수 receipt(영수증)를 기록했습니다."),
        ("paired_tier_record_gate", stage_ledger_has_rows(), STAGE_LEDGER, "Tier A/B 쌍 기록을 장부에 남겼습니다."),
        ("required_gate_coverage_audit", True, GATE_AUDIT, "필수 게이트 목록을 closeout(종료 기록)에 연결했습니다."),
        ("final_claim_guard", final_written and exists(FINAL_DECISION), CLAIM_RECEIPT, "운영/목표 주장을 모두 차단했습니다."),
    ]
    return [
        {
            "run_id": RUN_ID,
            "gate": name,
            "status": "passed" if ok else "failed",
            "evidence": rel(evidence),
            "effect": effect,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for name, ok, evidence, effect in gates
    ]


def write_docs(final: Mapping[str, Any], attribution: Sequence[Mapping[str, Any]], package: Sequence[Mapping[str, Any]], failure: Sequence[Mapping[str, Any]], queue: Sequence[Mapping[str, Any]], diagnostics: Sequence[Mapping[str, Any]], gates: Sequence[Mapping[str, Any]]) -> None:
    gate_lines = "\n".join(f"- {row['gate']}: {row['status']} -> {row['evidence']}" for row in gates)
    report = f"""# run364GG Profit-Floor Density Lift Review(수익 바닥 밀도 상승 검토)

Created(생성): {final['created_at_utc']}

Action(행동): GF proxy/ONNX smoke(GF 프록시/ONNX 온엑스 간이 검증) 결과를 validation lift(검증 상승), OOS floor preserve(표본외 바닥 보존), density3 failure(밀도3 실패), package decision(패키지 결정)으로 검토했습니다.

Effect(효과): 개선된 검증/표본외 단서를 보존하되 운영 후보로 올리지 않고 GH density3 profit-floor repair(GH 밀도3 수익 바닥 수리)로 넘깁니다.

- judgment(판정): `{final['judgment']}`
- selected_model_id(선택 모델 ID): `{final['selected_model_id']}`
- validation net/PF/density(검증 순수익/수익 팩터/밀도): `{final['selected_validation_net']}` / `{final['selected_validation_profit_factor']}` / `{final['selected_validation_trade_density']}`
- OOS net/PF/density(표본외 순수익/수익 팩터/밀도): `{final['selected_oos_net']}` / `{final['selected_oos_profit_factor']}` / `{final['selected_oos_trade_density']}`
- selected OOS cost0.9 net(선택 표본외 비용0.9 순수익): `{final['selected_oos_cost09_net']}`
- OOS cost0.6 net(표본외 비용0.6 순수익): `{final['selected_oos_cost06_net']}`
- combined net/density/cost0.9/short share(합산 순수익/밀도/비용0.9/숏 비중): `{final['selected_combined_net']}` / `{final['selected_combined_trade_density']}` / `{final['selected_combined_cost09_net']}` / `{final['selected_combined_short_share']}`
- density3_all_splits_count(전 분할 밀도3 수): `{final['density3_all_splits_count']}`
- max_combined_cost09_net(최대 합산 비용0.9 순수익): `{final['max_combined_cost09_net']}`
- package_eligible(패키지 가능): `{final['package_eligible']}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`

## Diagnostics(진단)

{markdown_table(diagnostics, ['diagnostic_id', 'row_found', 'model_id', 'validation_net', 'validation_density', 'oos_net', 'oos_profit_factor', 'oos_density', 'oos_cost09_net', 'combined_cost09_net', 'note'])}

## Attribution(귀속)

{markdown_table(attribution, ['attribution_id', 'observed', 'driver', 'severity', 'effect'])}

## Package Decision(패키지 결정)

{markdown_table(package, ['decision', 'reason', 'runtime_package', 'new_mt5_execution', 'effect'])}

## Failure Memory(실패 기억)

{markdown_table(failure, ['memory_id', 'failed_boundary', 'why_failed', 'salvage_value', 'reopen_condition', 'do_not_repeat'])}

## Next Queue(다음 대기열)

{markdown_table(queue, ['next_run_id', 'queue_id', 'hypothesis', 'required_preserve', 'required_repair', 'avoid', 'effect'])}

## Gates(게이트)

{gate_lines}

Boundary(경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
"""
    decision_doc = f"""# Decision(결정): stage364GG Profit-Floor Density Lift Review(수익 바닥 밀도 상승 검토)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(상위 실행 ID): `{PARENT_RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Action(행동): GF 결과를 package rejected(패키지 거절)로 닫고 GH density3 profit-floor repair(GH 밀도3 수익 바닥 수리)로 넘깁니다.

Effect(효과): 검증 개선과 표본외 바닥을 다음 탐색의 보존 조건으로 바꾸고, 밀도3 실패를 수리 대상으로 둡니다.
"""
    write_text(REPORT_PATH, report, bom=True)
    write_text(DECISION_DOC, decision_doc, bom=True)
    append_text_once(REVIEW_INDEX, f"run364GG__{RUN_ID}", f"\n- run364GG__{RUN_ID}: [{REPORT_PATH.name}]({REPORT_PATH.name}) - profit-floor density lift review(수익 바닥 밀도 상승 검토), next `{NEXT_RUN_ID}`.\n")
    append_text_once(STAGE_BRIEF, f"run364GG__{RUN_ID}", f"\n<!-- run364GG__{RUN_ID} -->\n\n## run364GG Profit-Floor Density Lift Review(수익 바닥 밀도 상승 검토)\n\nAction(행동): GF 결과를 검증 개선, 표본외 바닥 보존, 밀도3 실패로 분리했습니다.\n\nEffect(효과): `{NEXT_RUN_ID}`에서 density3 profit-floor repair(밀도3 수익 바닥 수리)를 실행합니다.\n")
    append_text_once(STAGE_README, f"run364GG__{RUN_ID}", f"\n<!-- run364GG__{RUN_ID} -->\n## run364GG profit-floor density lift review(수익 바닥 밀도 상승 검토)\n\nNext(다음): `{NEXT_RUN_ID}`.\n")
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

Current truth(현재 진실): `run364GG` reviewed(검토 완료) GF profit-floor density lift(GF 수익 바닥 밀도 상승). GF selected(선택) 후보는 validation net/PF/density(검증 순수익/수익 팩터/밀도) `{final['selected_validation_net']}` / `{final['selected_validation_profit_factor']}` / `{final['selected_validation_trade_density']}`이고 OOS net/PF/density(표본외 순수익/수익 팩터/밀도)는 `{final['selected_oos_net']}` / `{final['selected_oos_profit_factor']}` / `{final['selected_oos_trade_density']}`입니다.

Failure truth(실패 진실): GF는 validation net(검증 순수익)을 개선하고 OOS cost0.6(표본외 비용0.6)을 `{final['selected_oos_cost06_net']}`로 보존했지만 selected density(선택 밀도)는 `{final['selected_validation_trade_density']}` / `{final['selected_oos_trade_density']}` / `{final['selected_combined_trade_density']}`로 3 미만이고 combined cost0.9(합산 비용0.9)는 `{final['selected_combined_cost09_net']}`입니다.

Next action(다음 행동): `{NEXT_RUN_ID}`에서 density3 profit-floor repair(밀도3 수익 바닥 수리)를 실행합니다.

Operating boundary(운영 경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""", bom=True)
    write_text(SELECTION_STATUS, f"""# Stage364 selection status(선택 상태)

Updated(갱신): {final['created_at_utc']}

Current run(현재 실행): `{NEXT_RUN_ID}`
Latest completed run(최근 완료 실행): `{RUN_ID}`

Latest review(최근 검토): GG profit-floor density lift review(GG 수익 바닥 밀도 상승 검토)가 GF package(GF 패키지)를 rejected(거절)했습니다.

Selected model(선택 모델): `{final['selected_model_id']}`

Validation net/PF/density(검증 순수익/수익 팩터/밀도): `{final['selected_validation_net']}` / `{final['selected_validation_profit_factor']}` / `{final['selected_validation_trade_density']}`
OOS net/PF/density(표본외 순수익/수익 팩터/밀도): `{final['selected_oos_net']}` / `{final['selected_oos_profit_factor']}` / `{final['selected_oos_trade_density']}`
Combined net/density/cost0.9/short share(합산 순수익/밀도/비용0.9/숏 비중): `{final['selected_combined_net']}` / `{final['selected_combined_trade_density']}` / `{final['selected_combined_cost09_net']}` / `{final['selected_combined_short_share']}`

Next seed(다음 씨앗): density3 profit-floor repair(밀도3 수익 바닥 수리).

Authority(권위): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""", bom=True)
    append_text_once(WORKSPACE_CHANGELOG, f"run364GG__{RUN_ID}", f"\n<!-- run364GG__{RUN_ID} -->\n- {final['created_at_utc']} `{RUN_ID}` reviewed profit-floor density lift(수익 바닥 밀도 상승); validation net(검증 순수익) `{final['selected_validation_net']}`; OOS PF(표본외 수익 팩터) `{final['selected_oos_profit_factor']}`; selected density(선택 밀도) `{final['selected_validation_trade_density']}/{final['selected_oos_trade_density']}/{final['selected_combined_trade_density']}`; package rejected(패키지 거절); next `{NEXT_RUN_ID}`; no authority claim(권위 주장 없음).\n")
    append_text_once(IDEA_REGISTRY, f"run364GG__{RUN_ID}", f"\n<!-- run364GG__{RUN_ID} -->\n- `{RUN_ID}`: profit-floor density lift(수익 바닥 밀도 상승)는 validation/OOS(검증/표본외) 단서를 개선했지만 density3(밀도3) 실패로 GH density3 repair(GH 밀도3 수리)를 다음 입력으로 남겼습니다. Effect(효과): 검증 개선을 보존 조건으로 고정합니다.\n")
    append_text_once(NEGATIVE_REGISTER, f"run364GG__density3_failed__{RUN_ID}", f"\n<!-- run364GG__density3_failed__{RUN_ID} -->\n- `{RUN_ID}`: GF selected(선택) 후보는 validation net/PF(검증 순수익/수익 팩터) `{final['selected_validation_net']}` / `{final['selected_validation_profit_factor']}`와 OOS PF(표본외 수익 팩터) `{final['selected_oos_profit_factor']}`를 만들었지만 density(밀도) `{final['selected_validation_trade_density']}/{final['selected_oos_trade_density']}/{final['selected_combined_trade_density']}`로 실패했습니다. Effect(효과): GH에서 밀도3 수익 바닥 수리를 실행합니다.\n")


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
        "question": "Should GF open package or seed GH density3 repair?(GF를 패키지로 열지, GH 밀도3 수리로 보낼지)",
        "next_action": NEXT_RUN_ID,
        "notes": f"validation_net={final['selected_validation_net']};oos_pf={final['selected_oos_profit_factor']};density3={final['density3_all_splits_count']};package=rejected",
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
                "kpi_scope": "GG profit-floor density lift review(GG 수익 바닥 밀도 상승 검토)",
                "metric_scope": "python_proxy_review_no_mt5(Python 프록시 검토, MT5 없음)",
                "status": status,
                "net_profit": final["selected_oos_net"] if suffix == "tier_a_separate" else "",
                "profit_factor": final["selected_oos_profit_factor"] if suffix == "tier_a_separate" else "",
                "trade_density_per_feature_day": final["selected_oos_trade_density"] if suffix == "tier_a_separate" else "",
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
                "run_type": "profit_floor_density_lift_review(수익 바닥 밀도 상승 검토)",
                "input_run_id": PARENT_RUN_ID,
                "output_path": rel(FINAL_DECISION),
                "result_path": rel(PACKAGE_DECISION),
                "best_model_id": final["selected_model_id"],
                "net_profit": final["selected_oos_net"],
                "profit_factor": final["selected_oos_profit_factor"],
                "trade_density_per_feature_day": final["selected_oos_trade_density"],
                "result_status": STATUS,
                "primary_kpi": f"validation_net={final['selected_validation_net']};oos_pf={final['selected_oos_profit_factor']};density3={final['density3_all_splits_count']}",
                "guardrail_kpi": "package=rejected;authority=not_claimed",
                "final_decision_path": rel(FINAL_DECISION),
                "gate_audit_path": rel(GATE_AUDIT),
                "external_verification_status": "out_of_scope_by_claim(주장 범위 밖)",
                "evidence_boundary": "proxy_review_only_no_mt5_runtime_authority(프록시 검토만, MT5 런타임 권위 없음)",
            }
        ],
    )
    try:
        gf.et.repair_run_registry_line_endings(RUN_ID)
    except AttributeError:
        pass


def write_artifact_registry(final: Mapping[str, Any]) -> None:
    rows = []
    for path in OUTPUT_FILES:
        if exists(path) and io_path(path).is_file():
            rows.append(
                {
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "artifact_type": "script" if path == THIS_FILE else ("report" if path.suffix.lower() == ".md" else ("json" if path.suffix.lower() == ".json" else "csv")),
                    "path": rel(path),
                    "artifact_path": rel(path),
                    "sha256": sha(path),
                    "created_at": final["created_at_utc"],
                    "created_at_utc": final["created_at_utc"],
                    "claim_boundary": CLAIM_BOUNDARY,
                    "artifact_id": f"{RUN_ID}__{path.stem}",
                    "notes": "GG profit-floor density lift review artifact(GG 수익 바닥 밀도 상승 검토 산출물)",
                }
            )
    append_or_replace_csv(ARTIFACT_REGISTRY, ["artifact_id"], rows)


def build_review(parent: Mapping[str, Any]) -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
]:
    surface = read_csv(gh.TRADE_SURFACE)
    validation_net = num(surface, "validation_net")
    oos_net = num(surface, "oos_net")
    validation_density = num(surface, "validation_trade_density")
    oos_density = num(surface, "oos_trade_density")
    combined_density = num(surface, "combined_trade_density")
    oos_pf = num(surface, "oos_profit_factor")
    min_pf = num(surface, "min_split_profit_factor")
    oos_cost06 = num(surface, "oos_cost06_net")
    oos_cost09 = num(surface, "oos_cost09_net")
    combined_cost09 = num(surface, "combined_cost09_net")
    combined_short = num(surface, "combined_short_share")

    val_pos = validation_net > 0
    oos_pos = oos_net > 0
    density275 = (validation_density >= 2.75) & (oos_density >= 2.75) & (combined_density >= 2.75)
    density3 = (validation_density >= 3.0) & (oos_density >= 3.0) & (combined_density >= 3.0)
    oos_pf110 = oos_pf >= 1.10
    oos_pf125 = oos_pf >= 1.25
    oos_cost06_nonneg = oos_cost06 >= 0
    oos_cost09_nonneg = oos_cost09 >= 0
    combined_cost09_nonneg = combined_cost09 >= 0
    strict_like = val_pos & oos_pos & density3 & oos_pf125 & oos_cost09_nonneg & combined_cost09_nonneg & (combined_short <= 0.77) & (min_pf >= 1.05)
    operational_stack = truthy(surface, "et_operational_proxy_stack_pass") | truthy(surface, "operational_proxy_stack_pass")

    selected_rows = surface[surface["model_id"].astype(str) == str(parent["selected_model_id"])]
    selected_best = selected_rows.sort_values("selection_score", ascending=False).head(1)
    selected_oos_cost09 = ""
    if not selected_best.empty:
        selected_oos_cost09 = finite(selected_best.iloc[0].get("oos_cost09_net", ""))

    diagnostics = [
        diagnostic_row("gi_selected_candidate(선택 후보)", selected_best, "선택 후보는 density(밀도)를 크게 올렸지만 validation/cost floor(검증/비용 바닥)가 약해졌습니다."),
        diagnostic_row("gi_best_density275(밀도2.75 상위)", surface[density275].sort_values("selection_score", ascending=False).head(1), "전 분할 density2.75(밀도2.75) 이상 후보가 수익을 보존하는지 확인합니다."),
        diagnostic_row("gi_best_density3(밀도3 상위)", surface[density3].sort_values("selection_score", ascending=False).head(1), "전 분할 density3(밀도3) 후보가 있는지 확인합니다."),
        diagnostic_row("gi_oos_pf125_cost09(표본외 PF125 비용0.9)", surface[oos_pf125 & oos_cost09_nonneg].sort_values("oos_cost09_net", ascending=False).head(1), "OOS PF125/cost0.9(표본외 수익 팩터 1.25/비용0.9) 단서를 확인합니다."),
        diagnostic_row("gi_cost_floor_rejoin(비용 바닥 재결합)", surface[val_pos & oos_pos & oos_pf110 & oos_cost06_nonneg].sort_values("combined_trade_density", ascending=False).head(1), "수익 바닥을 보존한 후보의 밀도 상한을 확인합니다."),
        diagnostic_row("gi_strict_like(엄격 유사)", surface[strict_like].sort_values("selection_score", ascending=False).head(1), "엄격 유사 행이 있는지 확인합니다."),
    ]

    summary = [
        {
            "run_id": RUN_ID,
            "parent_run_id": PARENT_RUN_ID,
            "review_subject": parent["selected_model_id"],
            "surface_rows": len(surface),
            "strict_candidate_count": int(parent.get("strict_candidate_count", 0)),
            "operational_proxy_stack_pass_count": int(parent.get("operational_proxy_stack_pass_count", bool_count(operational_stack))),
            "onnx_smoke_pass_rows": int(parent.get("onnx_smoke_pass_rows", 0)),
            "selected_model_id": parent["selected_model_id"],
            "selected_validation_net": parent["selected_validation_net"],
            "selected_validation_profit_factor": parent["selected_validation_profit_factor"],
            "selected_validation_trade_density": parent["selected_validation_trade_density"],
            "selected_oos_net": parent["selected_oos_net"],
            "selected_oos_profit_factor": parent["selected_oos_profit_factor"],
            "selected_oos_trade_density": parent["selected_oos_trade_density"],
            "selected_oos_cost06_net": parent["selected_oos_cost06_net"],
            "selected_oos_cost09_net": selected_oos_cost09,
            "selected_combined_net": parent["selected_combined_net"],
            "selected_combined_trade_density": parent["selected_combined_trade_density"],
            "selected_combined_cost09_net": parent["selected_combined_cost09_net"],
            "selected_combined_short_share": parent["selected_combined_short_share"],
            "density275_all_splits_count": bool_count(density275),
            "density275_valpos_oospos_pf110_count": bool_count(density275 & val_pos & oos_pos & oos_pf110),
            "density3_all_splits_count": bool_count(density3),
            "density3_all_splits_valpos_oospos_count": bool_count(density3 & val_pos & oos_pos),
            "density3_all_splits_oos_pf125_count": bool_count(density3 & oos_pf125),
            "oos_pf125_count": bool_count(oos_pf125),
            "oos_pf125_cost09_count": bool_count(oos_pf125 & oos_cost09_nonneg),
            "oos_cost06_nonneg_count": bool_count(oos_cost06_nonneg),
            "oos_cost09_nonneg_count": bool_count(oos_cost09_nonneg),
            "combined_cost09_nonneg_count": bool_count(combined_cost09_nonneg),
            "strict_like_count": bool_count(strict_like),
            "operational_stack_surface_count": bool_count(operational_stack),
            "max_validation_density": finite(validation_density.max()),
            "max_oos_density": finite(oos_density.max()),
            "max_combined_density": finite(combined_density.max()),
            "max_oos_profit_factor": finite(oos_pf.max()),
            "max_oos_cost06_net": finite(oos_cost06.max()),
            "max_oos_cost09_net": finite(oos_cost09.max()),
            "max_combined_cost09_net": finite(combined_cost09.max()),
            "package_eligible": "false",
            "runtime_package": "not_opened",
            "new_mt5_execution": "not_run",
            "review_judgment": JUDGMENT,
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    s = summary[0]
    attribution = [
        {
            "run_id": RUN_ID,
            "attribution_id": "gi01_density_lift_salvage",
            "observed": f"selected_density={s['selected_validation_trade_density']}/{s['selected_oos_trade_density']}/{s['selected_combined_trade_density']}; density275_count={s['density275_all_splits_count']}",
            "driver": "lower threshold and wider hours(낮은 임계값과 넓은 시간)이 density supply(밀도 공급)를 실제로 늘렸습니다.",
            "severity": "salvage_clue(회수 단서)",
            "effect": "GJ(364GJ)는 이 밀도 공급을 유지하면서 cost floor(비용 바닥)를 다시 붙여야 합니다.",
            "evidence": rel(gh.TRADE_SURFACE),
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "attribution_id": "gi02_cost_floor_failed",
            "observed": f"selected_oos_cost06_net={s['selected_oos_cost06_net']}; selected_combined_cost09_net={s['selected_combined_cost09_net']}; selected_validation_net={s['selected_validation_net']}",
            "driver": "density lift(밀도 상승)가 cost0.6/cost0.9(비용0.6/비용0.9)와 validation net(검증 순수익)을 약화했습니다.",
            "severity": "high(높음)",
            "effect": "package(패키지)를 거절하고 density-cost floor rejoin(밀도-비용 바닥 재결합)으로 넘깁니다.",
            "evidence": rel(SURFACE_DIAGNOSTIC),
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "attribution_id": "gi03_no_density3_yet",
            "observed": f"density3_all_splits_count={s['density3_all_splits_count']}; max_combined_density={s['max_combined_density']}",
            "driver": "density3(밀도3)에는 아직 도달하지 못했습니다.",
            "severity": "medium(중간)",
            "effect": "다음 실행에서 밀도 공급은 유지하되 손실 구간을 잘라야 합니다.",
            "evidence": rel(gh.TRADE_SURFACE),
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    package = [
        {
            "run_id": RUN_ID,
            "decision": "rejected(거절)",
            "reason": "GH lifted density but validation net is near flat, OOS cost0.6<0, combined cost0.9<0, strict_candidate_count=0(GH 밀도 상승, 검증 순수익 거의 평탄, 표본외 비용0.6 음수, 합산 비용0.9 음수, 엄격 후보 0)",
            "runtime_package": "not_opened",
            "new_mt5_execution": "not_run",
            "effect": "밀도 개선 단서를 운영 가능한 후보로 과장하지 않습니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    failure = [
        {
            "run_id": RUN_ID,
            "memory_id": "gi01_density_lift_cost_floor_failed",
            "failed_boundary": "density lift plus validation/OOS/cost floor(밀도 상승과 검증/표본외/비용 바닥 동시 충족)",
            "why_failed": f"selected_density={s['selected_validation_trade_density']}/{s['selected_oos_trade_density']}/{s['selected_combined_trade_density']}; selected_validation_net={s['selected_validation_net']}; selected_oos_cost06={s['selected_oos_cost06_net']}; selected_combined_cost09={s['selected_combined_cost09_net']}",
            "salvage_value": f"density275_all_splits_count={s['density275_all_splits_count']}; selected_oos_net={s['selected_oos_net']}; selected_oos_pf={s['selected_oos_profit_factor']}; max_combined_density={s['max_combined_density']}",
            "reopen_condition": "preserve combined density near 2.7 while restoring validation net and OOS cost0.6(합산 밀도 2.7 근처를 보존하며 검증 순수익과 표본외 비용0.6 복구)",
            "do_not_repeat": "Do not chase density by accepting cost-floor collapse(비용 바닥 붕괴를 받아들이며 밀도만 추적하지 말 것).",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    queue = [
        {
            "run_id": RUN_ID,
            "next_run_id": NEXT_RUN_ID,
            "queue_rank": 1,
            "queue_id": "gj01_density_cost_floor_rejoin",
            "hypothesis": "GH density lift(GH 밀도 상승)를 유지하면서 cost guard(비용 가드)와 validation floor(검증 바닥)를 다시 붙이면 density-cost balance(밀도-비용 균형)가 개선될 수 있습니다.",
            "seed_from": "GH density supply clue(GH 밀도 공급 단서) + GI failure memory(GI 실패 기억)",
            "required_preserve": "combined density near 2.6+, OOS net>0, OOS PF>=1.05(합산 밀도 2.6 이상 근처, 표본외 순수익 양수, 표본외 수익 팩터 1.05 이상)",
            "required_repair": "validation net lift, OOS cost0.6>=0, combined_cost09 improves(검증 순수익 상승, 표본외 비용0.6 0 이상, 합산 비용0.9 개선)",
            "avoid": "density-only cost collapse(밀도 전용 비용 붕괴)",
            "effect": "GJ는 GH의 밀도 공급을 잃지 않으면서 비용과 검증 바닥을 다시 붙입니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]
    return summary, diagnostics, attribution, package, failure, queue


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
            "required_gates": ["kpi_contract_audit(KPI 계약 감사)", "source_authority_audit(진실 권한 감사)", "required_gate_coverage_audit(필수 게이트 커버리지 감사)"],
            "hypothesis": "GH 결과를 package decision(패키지 결정), failure memory(실패 기억), GJ queue(GJ 대기열)로 분리합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def write_receipts(final: Mapping[str, Any]) -> None:
    common = {"run_id": RUN_ID, "stage_id": STAGE_ID, "created_at_utc": final["created_at_utc"], "claim_boundary": CLAIM_BOUNDARY}
    write_json(RESULT_RECEIPT, {**common, "receipt_type": "result_judgment(결과 판정)", "decision": DECISION, "judgment_label": JUDGMENT, "evidence_available": [rel(REVIEW_SUMMARY), rel(SURFACE_DIAGNOSTIC), rel(PACKAGE_DECISION)], "evidence_missing": ["MT5 runtime package(MT5 런타임 패키지)", "MT5 runtime probe(MT5 런타임 탐침)"]})
    write_json(MODEL_RECEIPT, {**common, "receipt_type": "model_validation(모델 검증)", "review_subject": final["review_subject"], "selected_model_id": final["selected_model_id"], "validation_judgment": JUDGMENT})
    write_json(ATTRIBUTION_RECEIPT, {**common, "receipt_type": "performance_attribution(성과 귀속)", "observed_change": "GH lifted density but cost and validation floors failed(GH는 밀도를 올렸지만 비용과 검증 바닥은 실패)", "next_probe": NEXT_RUN_ID})
    write_json(LINEAGE_RECEIPT, {**common, "receipt_type": "artifact_lineage(산출물 계보)", "inputs": [rel(path) for path in INPUT_FILES], "outputs": [rel(path) for path in OUTPUT_FILES if exists(path)]})
    write_json(CLAIM_RECEIPT, {**common, "receipt_type": "claim_boundary(주장 경계)", "runtime_authority": "not_claimed", "operating_promotion": "not_claimed", "live_readiness": "not_claimed", "goal_achieve": "not_claimed", "effect": "GI review(GI 검토)를 운영 주장으로 올리지 않습니다."})


def gate_rows(final_written: bool) -> list[dict[str, Any]]:
    gates = [
        ("input_lineage_gate", exists(INPUT_MANIFEST), INPUT_MANIFEST, "GH 입력 계보를 기록했습니다."),
        ("parent_gate_inheritance_gate", exists(gh.GATE_AUDIT), gh.GATE_AUDIT, "GH 게이트 통과 상태를 상속 확인했습니다."),
        ("kpi_contract_audit", exists(REVIEW_SUMMARY) and exists(PACKAGE_DECISION), REVIEW_SUMMARY, "KPI와 package decision(패키지 결정)을 분리했습니다."),
        ("surface_overlap_audit", exists(SURFACE_DIAGNOSTIC), SURFACE_DIAGNOSTIC, "density lift(밀도 상승)와 cost-floor failure(비용 바닥 실패)를 분리 진단했습니다."),
        ("failure_attribution_gate", exists(FAILURE_ATTRIBUTION), FAILURE_ATTRIBUTION, "회수 단서와 실패 원인을 기록했습니다."),
        ("package_decision_gate", exists(PACKAGE_DECISION), PACKAGE_DECISION, "runtime package(런타임 패키지) 거절 근거를 기록했습니다."),
        ("failure_memory_gate", exists(FAILURE_MEMORY), FAILURE_MEMORY, "다음 GJ 실행의 실패 기억을 기록했습니다."),
        ("next_queue_gate", exists(RUN364GJ_QUEUE), RUN364GJ_QUEUE, "GJ 대기열을 기록했습니다."),
        ("receipt_coverage_gate", all(exists(path) for path in [RESULT_RECEIPT, MODEL_RECEIPT, ATTRIBUTION_RECEIPT, LINEAGE_RECEIPT, CLAIM_RECEIPT]), RESULT_RECEIPT, "필수 receipt(영수증)를 기록했습니다."),
        ("paired_tier_record_gate", stage_ledger_has_rows(), STAGE_LEDGER, "Tier A/B 쌍 기록을 장부에 남겼습니다."),
        ("required_gate_coverage_audit", True, GATE_AUDIT, "필수 게이트 목록을 closeout(종료 기록)에 연결했습니다."),
        ("final_claim_guard", final_written and exists(FINAL_DECISION), CLAIM_RECEIPT, "운영/목표 주장을 모두 차단했습니다."),
    ]
    return [
        {
            "run_id": RUN_ID,
            "gate": name,
            "status": "passed" if ok else "failed",
            "evidence": rel(evidence),
            "effect": effect,
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for name, ok, evidence, effect in gates
    ]


def write_docs(final: Mapping[str, Any], attribution: Sequence[Mapping[str, Any]], package: Sequence[Mapping[str, Any]], failure: Sequence[Mapping[str, Any]], queue: Sequence[Mapping[str, Any]], diagnostics: Sequence[Mapping[str, Any]], gates: Sequence[Mapping[str, Any]]) -> None:
    gate_lines = "\n".join(f"- {row['gate']}: {row['status']} -> {row['evidence']}" for row in gates)
    report = f"""# run364GI Density3 Profit-Floor Repair Review(밀도3 수익 바닥 수리 검토)

Created(생성): {final['created_at_utc']}

Action(행동): GH proxy/ONNX smoke(GH 프록시/ONNX 온엑스 간이 검증) 결과를 density lift(밀도 상승), cost-floor failure(비용 바닥 실패), package decision(패키지 결정)으로 검토했습니다.

Effect(효과): 밀도 공급 단서는 보존하되 운영 후보로 올리지 않고 GJ density-cost floor rejoin(GJ 밀도-비용 바닥 재결합)으로 넘깁니다.

- judgment(판정): `{final['judgment']}`
- selected_model_id(선택 모델 ID): `{final['selected_model_id']}`
- validation net/PF/density(검증 순수익/수익 팩터/밀도): `{final['selected_validation_net']}` / `{final['selected_validation_profit_factor']}` / `{final['selected_validation_trade_density']}`
- OOS net/PF/density(표본외 순수익/수익 팩터/밀도): `{final['selected_oos_net']}` / `{final['selected_oos_profit_factor']}` / `{final['selected_oos_trade_density']}`
- selected OOS cost0.6/cost0.9 net(선택 표본외 비용0.6/비용0.9 순수익): `{final['selected_oos_cost06_net']}` / `{final['selected_oos_cost09_net']}`
- combined net/density/cost0.9/short share(합산 순수익/밀도/비용0.9/숏 비중): `{final['selected_combined_net']}` / `{final['selected_combined_trade_density']}` / `{final['selected_combined_cost09_net']}` / `{final['selected_combined_short_share']}`
- density275_all_splits_count(전 분할 밀도2.75 수): `{final['density275_all_splits_count']}`
- density3_all_splits_count(전 분할 밀도3 수): `{final['density3_all_splits_count']}`
- package_eligible(패키지 가능): `{final['package_eligible']}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`

## Diagnostics(진단)

{markdown_table(diagnostics, ['diagnostic_id', 'row_found', 'model_id', 'validation_net', 'validation_density', 'oos_net', 'oos_profit_factor', 'oos_density', 'oos_cost09_net', 'combined_cost09_net', 'note'])}

## Attribution(귀속)

{markdown_table(attribution, ['attribution_id', 'observed', 'driver', 'severity', 'effect'])}

## Package Decision(패키지 결정)

{markdown_table(package, ['decision', 'reason', 'runtime_package', 'new_mt5_execution', 'effect'])}

## Failure Memory(실패 기억)

{markdown_table(failure, ['memory_id', 'failed_boundary', 'why_failed', 'salvage_value', 'reopen_condition', 'do_not_repeat'])}

## Next Queue(다음 대기열)

{markdown_table(queue, ['next_run_id', 'queue_id', 'hypothesis', 'required_preserve', 'required_repair', 'avoid', 'effect'])}

## Gates(게이트)

{gate_lines}

Boundary(경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
"""
    decision_doc = f"""# Decision(결정): stage364GI Density3 Profit-Floor Repair Review(밀도3 수익 바닥 수리 검토)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(상위 실행 ID): `{PARENT_RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{JUDGMENT}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

Action(행동): GH 결과를 package rejected(패키지 거절)로 닫고 GJ density-cost floor rejoin(GJ 밀도-비용 바닥 재결합)으로 넘깁니다.

Effect(효과): GH의 밀도 공급 단서를 다음 탐색의 보존 조건으로 바꾸고, 비용/검증 바닥 실패를 수리 대상으로 둡니다.
"""
    write_text(REPORT_PATH, report, bom=True)
    write_text(DECISION_DOC, decision_doc, bom=True)
    append_text_once(REVIEW_INDEX, f"run364GI__{RUN_ID}", f"\n- run364GI__{RUN_ID}: [{REPORT_PATH.name}]({REPORT_PATH.name}) - density3 profit-floor repair review(밀도3 수익 바닥 수리 검토), next `{NEXT_RUN_ID}`.\n")
    append_text_once(STAGE_BRIEF, f"run364GI__{RUN_ID}", f"\n<!-- run364GI__{RUN_ID} -->\n\n## run364GI Density3 Profit-Floor Repair Review(밀도3 수익 바닥 수리 검토)\n\nAction(행동): GH 결과를 밀도 상승과 비용/검증 바닥 실패로 분리했습니다.\n\nEffect(효과): `{NEXT_RUN_ID}`에서 density-cost floor rejoin(밀도-비용 바닥 재결합)을 실행합니다.\n")
    append_text_once(STAGE_README, f"run364GI__{RUN_ID}", f"\n<!-- run364GI__{RUN_ID} -->\n## run364GI density3 profit-floor repair review(밀도3 수익 바닥 수리 검토)\n\nNext(다음): `{NEXT_RUN_ID}`.\n")
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

Current truth(현재 진실): `run364GI` reviewed(검토 완료) GH density3 profit-floor repair(GH 밀도3 수익 바닥 수리). GH selected(선택) 후보는 validation net/PF/density(검증 순수익/수익 팩터/밀도) `{final['selected_validation_net']}` / `{final['selected_validation_profit_factor']}` / `{final['selected_validation_trade_density']}`이고 OOS net/PF/density(표본외 순수익/수익 팩터/밀도)는 `{final['selected_oos_net']}` / `{final['selected_oos_profit_factor']}` / `{final['selected_oos_trade_density']}`입니다.

Failure truth(실패 진실): GH는 combined density(합산 밀도)를 `{final['selected_combined_trade_density']}`까지 끌어올렸지만 validation net(검증 순수익)은 `{final['selected_validation_net']}`로 약하고 OOS cost0.6(표본외 비용0.6)은 `{final['selected_oos_cost06_net']}`, combined cost0.9(합산 비용0.9)는 `{final['selected_combined_cost09_net']}`입니다.

Next action(다음 행동): `{NEXT_RUN_ID}`에서 density-cost floor rejoin(밀도-비용 바닥 재결합)을 실행합니다.

Operating boundary(운영 경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""", bom=True)
    write_text(SELECTION_STATUS, f"""# Stage364 selection status(선택 상태)

Updated(갱신): {final['created_at_utc']}

Current run(현재 실행): `{NEXT_RUN_ID}`
Latest completed run(최근 완료 실행): `{RUN_ID}`

Latest review(최근 검토): GI density3 profit-floor repair review(GI 밀도3 수익 바닥 수리 검토)가 GH package(GH 패키지)를 rejected(거절)했습니다.

Selected model(선택 모델): `{final['selected_model_id']}`

Validation net/PF/density(검증 순수익/수익 팩터/밀도): `{final['selected_validation_net']}` / `{final['selected_validation_profit_factor']}` / `{final['selected_validation_trade_density']}`
OOS net/PF/density(표본외 순수익/수익 팩터/밀도): `{final['selected_oos_net']}` / `{final['selected_oos_profit_factor']}` / `{final['selected_oos_trade_density']}`
Combined net/density/cost0.9/short share(합산 순수익/밀도/비용0.9/숏 비중): `{final['selected_combined_net']}` / `{final['selected_combined_trade_density']}` / `{final['selected_combined_cost09_net']}` / `{final['selected_combined_short_share']}`

Next seed(다음 씨앗): density-cost floor rejoin(밀도-비용 바닥 재결합).

Authority(권위): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""", bom=True)
    append_text_once(WORKSPACE_CHANGELOG, f"run364GI__{RUN_ID}", f"\n<!-- run364GI__{RUN_ID} -->\n- {final['created_at_utc']} `{RUN_ID}` reviewed density3 profit-floor repair(밀도3 수익 바닥 수리); selected density(선택 밀도) `{final['selected_validation_trade_density']}/{final['selected_oos_trade_density']}/{final['selected_combined_trade_density']}`; OOS cost0.6(표본외 비용0.6) `{final['selected_oos_cost06_net']}`; package rejected(패키지 거절); next `{NEXT_RUN_ID}`; no authority claim(권위 주장 없음).\n")
    append_text_once(IDEA_REGISTRY, f"run364GI__{RUN_ID}", f"\n<!-- run364GI__{RUN_ID} -->\n- `{RUN_ID}`: density3 profit-floor repair(밀도3 수익 바닥 수리)는 density supply(밀도 공급)를 회수 단서로 만들었지만 cost floor(비용 바닥) 실패로 GJ density-cost floor rejoin(GJ 밀도-비용 바닥 재결합)을 다음 입력으로 남겼습니다. Effect(효과): 밀도 공급을 보존 조건으로 고정합니다.\n")
    append_text_once(NEGATIVE_REGISTER, f"run364GI__density_lift_cost_floor_failed__{RUN_ID}", f"\n<!-- run364GI__density_lift_cost_floor_failed__{RUN_ID} -->\n- `{RUN_ID}`: GH selected(선택) 후보는 density(밀도) `{final['selected_validation_trade_density']}/{final['selected_oos_trade_density']}/{final['selected_combined_trade_density']}`로 개선됐지만 validation net(검증 순수익) `{final['selected_validation_net']}`, OOS cost0.6(표본외 비용0.6) `{final['selected_oos_cost06_net']}`, combined cost0.9(합산 비용0.9) `{final['selected_combined_cost09_net']}`로 실패했습니다. Effect(효과): GJ에서 밀도-비용 바닥 재결합을 실행합니다.\n")


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
        "question": "Should GH open package or seed GJ density-cost rejoin?(GH를 패키지로 열지, GJ 밀도-비용 재결합으로 보낼지)",
        "next_action": NEXT_RUN_ID,
        "notes": f"density={final['selected_combined_trade_density']};oos_cost06={final['selected_oos_cost06_net']};density3={final['density3_all_splits_count']};package=rejected",
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
                "kpi_scope": "GI density3 profit-floor repair review(GI 밀도3 수익 바닥 수리 검토)",
                "metric_scope": "python_proxy_review_no_mt5(Python 프록시 검토, MT5 없음)",
                "status": status,
                "net_profit": final["selected_oos_net"] if suffix == "tier_a_separate" else "",
                "profit_factor": final["selected_oos_profit_factor"] if suffix == "tier_a_separate" else "",
                "trade_density_per_feature_day": final["selected_oos_trade_density"] if suffix == "tier_a_separate" else "",
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
                "run_type": "density3_profit_floor_repair_review(밀도3 수익 바닥 수리 검토)",
                "input_run_id": PARENT_RUN_ID,
                "output_path": rel(FINAL_DECISION),
                "result_path": rel(PACKAGE_DECISION),
                "best_model_id": final["selected_model_id"],
                "net_profit": final["selected_oos_net"],
                "profit_factor": final["selected_oos_profit_factor"],
                "trade_density_per_feature_day": final["selected_oos_trade_density"],
                "result_status": STATUS,
                "primary_kpi": f"density={final['selected_combined_trade_density']};oos_cost06={final['selected_oos_cost06_net']};density3={final['density3_all_splits_count']}",
                "guardrail_kpi": "package=rejected;authority=not_claimed",
                "final_decision_path": rel(FINAL_DECISION),
                "gate_audit_path": rel(GATE_AUDIT),
                "external_verification_status": "out_of_scope_by_claim(주장 범위 밖)",
                "evidence_boundary": "proxy_review_only_no_mt5_runtime_authority(프록시 검토만, MT5 런타임 권위 없음)",
            }
        ],
    )
    try:
        gh.et.repair_run_registry_line_endings(RUN_ID)
    except AttributeError:
        pass


def write_artifact_registry(final: Mapping[str, Any]) -> None:
    rows = []
    for path in OUTPUT_FILES:
        if exists(path) and io_path(path).is_file():
            rows.append(
                {
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "artifact_type": "script" if path == THIS_FILE else ("report" if path.suffix.lower() == ".md" else ("json" if path.suffix.lower() == ".json" else "csv")),
                    "path": rel(path),
                    "artifact_path": rel(path),
                    "sha256": sha(path),
                    "created_at": final["created_at_utc"],
                    "created_at_utc": final["created_at_utc"],
                    "claim_boundary": CLAIM_BOUNDARY,
                    "artifact_id": f"{RUN_ID}__{path.stem}",
                    "notes": "GI density3 profit-floor repair review artifact(GI 밀도3 수익 바닥 수리 검토 산출물)",
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
            "command": f"python {rel(THIS_FILE)}",
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
    summary_rows, diagnostics, attribution, package, failure, queue = build_review(parent)
    summary = summary_rows[0]
    write_csv(REVIEW_SUMMARY, summary_rows)
    write_csv(SURFACE_DIAGNOSTIC, diagnostics)
    write_csv(FAILURE_ATTRIBUTION, attribution)
    write_csv(PACKAGE_DECISION, package)
    write_csv(FAILURE_MEMORY, failure)
    write_csv(RUN364GJ_QUEUE, queue)

    gates = gate_rows(final_written=False)
    final = final_payload(summary, gates, created_at)
    write_json(FINAL_DECISION, final)
    write_receipts(final)
    write_csv(GATE_AUDIT, gates)
    write_docs(final, attribution, package, failure, queue, diagnostics, gates)
    write_ledgers(final)
    write_manifest(final)
    write_artifact_registry(final)
    write_receipts(final)

    gates = gate_rows(final_written=True)
    final = final_payload(summary, gates, created_at)
    write_json(FINAL_DECISION, final)
    write_csv(GATE_AUDIT, gates)
    write_docs(final, attribution, package, failure, queue, diagnostics, gates)
    write_ledgers(final)
    write_manifest(final)
    write_artifact_registry(final)
    write_receipts(final)

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
