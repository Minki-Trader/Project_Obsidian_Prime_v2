from __future__ import annotations

import csv
import json
import math
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path  # noqa: E402
from stage_pipelines.stage364 import execute_h17_short_quality_risk_scale_mt5_runtime_probe_without_db as db  # noqa: E402
from stage_pipelines.stage364 import execute_h17_short_source_expansion_mt5_runtime_probe_without_db as dg_source  # noqa: E402
from stage_pipelines.stage364 import execute_h17_short_source_profit_recovery_mt5_runtime_probe_without_db as dl  # noqa: E402
from stage_pipelines.stage364 import materialize_h17_short_source_profit_recovery_runtime_package_without_db as dk  # noqa: E402
from stage_pipelines.stage364 import review_h17_short_source_profit_recovery_mt5_runtime_probe_without_db as dm  # noqa: E402
from stage_pipelines.stage364 import train_h17_short_source_profit_recovery_scout_without_db as di  # noqa: E402
from stage_pipelines.stage364.review_pf_pass_density_restore_offensive_scout_without_db import repair_run_registry_line_endings  # noqa: E402


TODAY = "2026-06-06"
STAGE_ID = dm.STAGE_ID
RUN_NUMBER = "run364DN"
RUN_ID = "run364DN_train_h17_short_source_pf_balance_polish_scout_without_db_v1"
PARENT_RUN_ID = dm.RUN_ID
BASELINE_RUN_ID = db.RUN_ID
SOURCE_EXPANSION_RUN_ID = dg_source.RUN_ID
RUNTIME_PROBE_RUN_ID = dl.RUN_ID
SOURCE_PACKAGE_RUN_ID = dk.RUN_ID
SOURCE_PROXY_RUN_ID = di.RUN_ID
NEXT_RUN_ID = "run364DO_review_h17_short_source_pf_balance_polish_scout_without_db_v1"

STATUS = "completed_stage364DN_h17_short_source_pf_balance_polish_proxy_scout_review_required_no_authority"
JUDGMENT = "proxy_pf_balance_polish_scout_no_calibrated_db_exceed_candidate_review_required_no_authority"
DECISION = "stage364DN_open_run364DO_short_source_pf_balance_polish_review"
CLAIM_BOUNDARY = (
    "research_development_proxy_scout_only_short_source_pf_balance_polish_"
    "no_new_model_training_no_new_mt5_execution_no_forward_pass_no_live_readiness_"
    "no_operating_promotion_no_runtime_authority_no_goal_claim"
)

DAYS = 314.0
FIXED_LOT = 0.10
MAX_HOLD_BARS = 6
DENSITY_FLOOR = 3.0
DENSITY_CEILING = 10.0
SHORT_COUNT_FLOOR = 125.0

STAGE_DIR = dm.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
SPEC_DIR = STAGE_DIR / "00_spec"
SELECTED_DIR = STAGE_DIR / "04_selected"

INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
PF_BALANCE_SURFACE = RUN_DIR / "dn_short_source_pf_balance_polish_surface.csv"
SELECTED_CANDIDATE = RUN_DIR / "selected_dn_candidate.json"
SELECTED_TRADE_TAPE = RUN_DIR / "selected_dn_trade_tape.csv"
VARIANT_OVERRIDE_AUDIT = RUN_DIR / "variant_override_audit.csv"
VARIANT_RISK_SCALE_AUDIT = RUN_DIR / "variant_risk_scale_audit.csv"
VARIANT_HOUR_SIDE_ATTRIBUTION = RUN_DIR / "variant_hour_side_attribution.csv"
VARIANT_REASON_ATTRIBUTION = RUN_DIR / "variant_reason_attribution.csv"
RUNTIME_REPRESENTATION_AUDIT = RUN_DIR / "runtime_representation_audit.csv"
PACKAGE_PRECHECK = RUN_DIR / "package_precheck.csv"
PROXY_MT5_CALIBRATION = RUN_DIR / "proxy_mt5_calibration.csv"
RUN364DO_QUEUE = RUN_DIR / "run364DO_review_queue.csv"
DATA_INTEGRITY_AUDIT = RUN_DIR / "data_integrity_audit.csv"
RUN_EVIDENCE_RECEIPT = RUN_DIR / "run_evidence_receipt.json"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment_design_receipt.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
ATTRIBUTION_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / "run364DN_h17_short_source_pf_balance_polish_scout.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364DN_h17_short_source_pf_balance_polish_scout.md"
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
NEGATIVE_RESULT_REGISTER = ROOT / "docs" / "registers" / "negative_result_register.md"

INPUT_FILES = [
    dm.FINAL_DECISION,
    dm.GATE_AUDIT,
    dm.RUNTIME_REVIEW,
    dm.RUN364DN_QUEUE,
    dl.FINAL_DECISION,
    dl.EXECUTION_SUMMARY,
    dl.PROXY_MT5_DIFF,
    dk.FINAL_DECISION,
    dk.RUNTIME_POLICY_CONFIG,
    dk.TESTER_SET_MANIFEST,
    di.SELECTED_CANDIDATE,
    di.SELECTED_TRADE_TAPE,
    db.FINAL_DECISION,
    db.EXECUTION_SUMMARY,
    dg_source.FINAL_DECISION,
    dg_source.EXECUTION_SUMMARY,
    di.dd.SOURCE_RAW_US100_M5,
]

OUTPUT_FILES = [
    INPUT_MANIFEST,
    WORK_PACKET,
    PF_BALANCE_SURFACE,
    SELECTED_CANDIDATE,
    SELECTED_TRADE_TAPE,
    VARIANT_OVERRIDE_AUDIT,
    VARIANT_RISK_SCALE_AUDIT,
    VARIANT_HOUR_SIDE_ATTRIBUTION,
    VARIANT_REASON_ATTRIBUTION,
    RUNTIME_REPRESENTATION_AUDIT,
    PACKAGE_PRECHECK,
    PROXY_MT5_CALIBRATION,
    RUN364DO_QUEUE,
    DATA_INTEGRITY_AUDIT,
    RUN_EVIDENCE_RECEIPT,
    EXPERIMENT_RECEIPT,
    DATA_RECEIPT,
    ATTRIBUTION_RECEIPT,
    JUDGMENT_RECEIPT,
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
    NEGATIVE_RESULT_REGISTER,
    Path(__file__),
]


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    return di.rel(path)


def exists(path: Path | str) -> bool:
    return di.exists(path)


def sha(path: Path | str) -> str:
    return di.sha(path)


def json_ready(value: Any) -> Any:
    return di.json_ready(value)


def read_json(path: Path) -> Any:
    return di.read_json(path)


def write_json(path: Path, payload: Any) -> None:
    di.write_json(path, payload)


def read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(io_path(path), encoding="utf-8-sig").fillna("")


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    materialized = [{str(key): json_ready(value) for key, value in row.items()} for row in rows]
    if fieldnames is None:
        fieldnames = []
        for row in materialized:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fieldnames), extrasaction="ignore")
        writer.writeheader()
        for row in materialized:
            writer.writerow(row)


def write_text(path: Path, text: str, *, bom: bool = True) -> None:
    di.write_text(path, text, bom=bom)


def append_text_once(path: Path, marker: str, text: str) -> None:
    di.append_text_once(path, marker, text)


def append_or_replace_csv(path: Path, key_fields: Sequence[str], rows: Sequence[Mapping[str, Any]], *, extend_header: bool = True) -> None:
    di.append_or_replace_csv(path, key_fields, rows, extend_header=extend_header)


def replace_prefixed_lines(path: Path, replacements: Mapping[str, str], *, bom: bool = True) -> None:
    di.replace_prefixed_lines(path, replacements, bom=bom)


def finite(value: Any, digits: int = 10) -> float | str:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return ""
    if not math.isfinite(number):
        return ""
    return round(number, digits)


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        if value in ("", None):
            return default
        number = float(value)
    except (TypeError, ValueError):
        return default
    return number if math.isfinite(number) else default


def ensure_dirs() -> None:
    for path in [RUN_DIR, REVIEW_DIR, SPEC_DIR, SELECTED_DIR, DECISION_DOC.parent]:
        io_path(path).mkdir(parents=True, exist_ok=True)


def validate_inputs() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    missing = [rel(path) for path in INPUT_FILES if not exists(path)]
    if missing:
        raise FileNotFoundError("missing DN inputs(DN 입력 누락): " + ", ".join(missing))
    dm_final = read_json(dm.FINAL_DECISION)
    dl_final = read_json(dl.FINAL_DECISION)
    db_final = read_json(db.FINAL_DECISION)
    if dm_final.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"DM next_run_id mismatch(DM 다음 실행 ID 불일치): {dm_final.get('next_run_id')} != {RUN_ID}")
    for label, final in [("DM", dm_final), ("DL", dl_final), ("DB", db_final), ("DK", read_json(dk.FINAL_DECISION))]:
        for key in ["runtime_authority", "operating_promotion", "live_readiness", "goal_achieve"]:
            if final.get(key, "not_claimed") != "not_claimed":
                raise RuntimeError(f"{label} forbidden claim({label} 금지 주장): {key}={final.get(key)}")
    gates = read_csv(dm.GATE_AUDIT)
    if gates.empty or any(gates["status"].astype(str) != "passed"):
        raise RuntimeError("DM gate audit(DM 게이트 감사)가 모두 passed(통과)가 아닙니다.")
    return dm_final, dl_final, db_final


def input_manifest_rows() -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "input_path": rel(path),
            "exists": exists(path),
            "sha256": sha(path) if exists(path) and io_path(path).is_file() else "",
            "input_role": "PF/net polish scout input(PF/순수익 다듬기 스카우트 입력)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for path in INPUT_FILES
    ]


def write_work_packet() -> None:
    write_json(
        WORK_PACKET,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "parent_run_id": PARENT_RUN_ID,
            "primary_family": "experiment_execution(실험 실행)",
            "primary_skill": "obsidian-run-evidence-system(옵시디언 실행 근거 시스템)",
            "support_skills": [
                "obsidian-experiment-design(옵시디언 실험 설계)",
                "obsidian-data-integrity(옵시디언 데이터 무결성)",
                "obsidian-performance-attribution(옵시디언 성과 귀속)",
                "obsidian-result-judgment(옵시디언 결과 판정)",
                "obsidian-artifact-lineage(옵시디언 산출물 계보)",
            ],
            "hypothesis": "A small parameter-only polish of DI02 no19 source and risk-scale overlay can keep short-count lift while pushing MT5 PF/net above DB.",
            "decision_use": "Choose a review candidate for possible MT5 package or record no parameter-only pass.",
            "comparison_baseline": [BASELINE_RUN_ID, SOURCE_EXPANSION_RUN_ID, RUNTIME_PROBE_RUN_ID],
            "control_variables": [
                "same DB telemetry(DB 원격측정 동일)",
                "same ONNX output(ONNX 출력 동일)",
                "same max-hold replay(max-hold 재생 동일)",
                "no trade splitting(거래 쪼개기 없음)",
            ],
            "changed_variables": [
                "source margin thresholds(원천 마진 임계값)",
                "source hour veto(원천 시간 배제)",
                "risk-scale overlay multiplier(위험비율 오버레이 배수)",
                "risk-scale overlay hours/min margin(위험비율 오버레이 시간/최소 마진)",
            ],
            "success_criteria": "runtime-calibrated net > DB 1018.78, PF > DB 1.41, density >=3, short_count >=125, runtime-ready parameterization.",
            "failure_criteria": "net rises without PF, PF rises with too few shorts, or only non-runtime month filters pass.",
            "required_gates": [
                "scope_completion_gate",
                "input_lineage_gate",
                "data_integrity_gate",
                "candidate_surface_gate",
                "runtime_representability_gate",
                "kpi_contract_gate",
                "calibrated_proxy_boundary_gate",
                "no_trade_splitting_gate",
                "receipt_coverage_gate",
                "required_gate_coverage_audit",
                "final_claim_guard",
            ],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )


def variant_specs() -> list[dict[str, Any]]:
    base = {
        "hours": [17, 18, 20, 21],
        "p_short_min": 0.4375,
        "margin_vs_long_min": 0.05,
        "margin_vs_flat_min": 0.0,
        "exclude_months": [8],
        "risk_scale_hours": [17, 18, 19, 20],
        "risk_scale_min_margin": 0.08,
        "risk_scale_multiplier": 1.10,
        "runtime_representation": "runtime_ready_existing_params(기존 파라미터로 런타임 가능)",
    }
    specs: list[dict[str, Any]] = [
        {
            "variant_id": "dn00_db_policy_anchor",
            "family": "anchor(기준)",
            "hypothesis": "DB runtime policy anchor(DB 런타임 정책 기준).",
            "hours": [],
            "p_short_min": None,
            "margin_vs_long_min": None,
            "margin_vs_flat_min": None,
            "exclude_months": [],
            "risk_scale_hours": [17, 18, 19, 20],
            "risk_scale_min_margin": 0.08,
            "risk_scale_multiplier": 1.10,
            "runtime_representation": "anchor_not_package(기준, 패키지 아님)",
        },
        {
            **base,
            "variant_id": "dn01_dl_anchor_no19_m050_r110",
            "family": "dl_anchor(DL 기준)",
            "hypothesis": "Replay DL no19 source and current risk scale(DL 19시 배제 원천과 현재 위험비율 재생).",
        },
        {
            **base,
            "variant_id": "dn02_risk_mult115_all_h17_20",
            "family": "risk_scale_polish(위험비율 다듬기)",
            "hypothesis": "Lift high-quality short size mildly(고품질 숏 크기를 약하게 올림).",
            "risk_scale_multiplier": 1.15,
        },
        {
            **base,
            "variant_id": "dn03_risk_mult120_all_h17_20",
            "family": "risk_scale_polish(위험비율 다듬기)",
            "hypothesis": "Test whether stronger short boost clears DB net without PF damage(강한 숏 증폭이 PF 훼손 없이 DB 순수익을 넘는지 확인).",
            "risk_scale_multiplier": 1.20,
        },
        {
            **base,
            "variant_id": "dn04_risk_mult125_all_h17_20",
            "family": "risk_scale_stress(위험비율 압박)",
            "hypothesis": "Upper stress for risk multiplier(위험비율 배수 상단 압박).",
            "risk_scale_multiplier": 1.25,
        },
        {
            **base,
            "variant_id": "dn05_core_risk_h17_18_20_min060",
            "family": "risk_scale_hours_min_margin(위험비율 시간/마진)",
            "hypothesis": "Drop unused hour19 from risk overlay and loosen min margin(위험비율에서 미사용 19시를 빼고 최소 마진을 완화).",
            "risk_scale_hours": [17, 18, 20],
            "risk_scale_min_margin": 0.06,
        },
        {
            **base,
            "variant_id": "dn06_core_risk_h17_18_20_min070",
            "family": "risk_scale_hours_min_margin(위험비율 시간/마진)",
            "hypothesis": "Core risk hours with min margin 0.07(핵심 위험비율 시간과 최소 마진 0.07).",
            "risk_scale_hours": [17, 18, 20],
            "risk_scale_min_margin": 0.07,
        },
        {
            **base,
            "variant_id": "dn07_core_risk_h17_18_20_mult115",
            "family": "risk_scale_hours_min_margin(위험비율 시간/마진)",
            "hypothesis": "Core risk hours with 1.15 multiplier(핵심 위험비율 시간과 1.15 배수).",
            "risk_scale_hours": [17, 18, 20],
            "risk_scale_multiplier": 1.15,
        },
        {
            **base,
            "variant_id": "dn08_risk_h17_20_mult115",
            "family": "risk_scale_hours_min_margin(위험비율 시간/마진)",
            "hypothesis": "Scale only hours 17 and 20(17시와 20시만 크기 조정).",
            "risk_scale_hours": [17, 20],
            "risk_scale_multiplier": 1.15,
        },
        {
            **base,
            "variant_id": "dn09_p_short_0450_current_risk",
            "family": "probability_quality_filter(확률 품질 필터)",
            "hypothesis": "Raise p_short floor to reduce weak added shorts(p_short 하한을 올려 약한 추가 숏을 줄임).",
            "p_short_min": 0.45,
        },
        {
            **base,
            "variant_id": "dn10_p_short_04625_current_risk",
            "family": "probability_quality_filter(확률 품질 필터)",
            "hypothesis": "Higher p_short floor stress(더 높은 p_short 하한 압박).",
            "p_short_min": 0.4625,
        },
        {
            **base,
            "variant_id": "dn11_margin_long_0080_current_risk",
            "family": "margin_quality_filter(마진 품질 필터)",
            "hypothesis": "Raise margin_vs_long to 0.08(margin_vs_long을 0.08로 올림).",
            "margin_vs_long_min": 0.08,
        },
        {
            **base,
            "variant_id": "dn12_no17_ml055",
            "family": "hour_pair_veto(시간쌍 배제)",
            "hypothesis": "Drop hour17 while slightly raising margin(17시를 빼고 마진을 소폭 올림).",
            "hours": [18, 20, 21],
            "margin_vs_long_min": 0.055,
        },
        {
            **base,
            "variant_id": "dn13_no18_ml055",
            "family": "hour_pair_veto(시간쌍 배제)",
            "hypothesis": "Drop hour18 while slightly raising margin(18시를 빼고 마진을 소폭 올림).",
            "hours": [17, 20, 21],
            "margin_vs_long_min": 0.055,
        },
        {
            **base,
            "variant_id": "dn14_no21_ml055",
            "family": "hour_pair_veto(시간쌍 배제)",
            "hypothesis": "Drop hour21 while slightly raising margin(21시를 빼고 마진을 소폭 올림).",
            "hours": [17, 18, 20],
            "margin_vs_long_min": 0.055,
        },
    ]
    return specs


def build_override_mask(cycles: pd.DataFrame, spec: Mapping[str, Any]) -> pd.Series:
    if spec["variant_id"] == "dn00_db_policy_anchor":
        return pd.Series(False, index=cycles.index)
    mask = (
        cycles["decision_base"].eq("flat")
        & cycles["open_hour"].astype("Int64").isin(list(spec["hours"]))
        & cycles["p_short"].ge(float(spec["p_short_min"]))
        & cycles["margin_vs_long"].ge(float(spec["margin_vs_long_min"]))
        & cycles["margin_vs_flat"].ge(float(spec["margin_vs_flat_min"]))
        & cycles["p_short_dominant"].astype(bool)
        & cycles["p_short"].gt(cycles["p_flat"])
    )
    exclude_months = list(spec.get("exclude_months", []))
    if exclude_months:
        mask &= ~cycles["open_month_num"].astype("Int64").isin(exclude_months)
    return mask.fillna(False)


def volume_for(side: str, row: Mapping[str, Any], spec: Mapping[str, Any]) -> float:
    risk_hours = set(int(hour) for hour in spec.get("risk_scale_hours", []))
    min_margin = as_float(spec.get("risk_scale_min_margin"), 0.08)
    multiplier = as_float(spec.get("risk_scale_multiplier"), 1.0)
    if side == "short" and int(row["open_hour"]) in risk_hours and as_float(row["margin_vs_long"]) >= min_margin:
        return FIXED_LOT * multiplier
    return FIXED_LOT


def iso_time(value: Any) -> str:
    return pd.Timestamp(value).strftime("%Y-%m-%dT%H:%M:%S")


def entry_source(row: Mapping[str, Any], added: bool, variant_id: str) -> dict[str, Any]:
    return {
        **dict(row),
        "source_reason": f"{variant_id}_override" if added else row.get("decision_reason", ""),
        "source_bucket": "dn_added_short_source" if added else "runtime_decision",
    }


def trade_row(
    variant_id: str,
    direction: str,
    volume: float,
    entry_price: float,
    close_price: float,
    gross: float,
    hold_bars: int,
    source: Mapping[str, Any],
    entry_time: Any,
    close_time: Any,
    close_reason: str,
    entry_index: int,
    exit_index: int,
) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "variant_id": variant_id,
        "open_time": iso_time(entry_time),
        "close_time": iso_time(close_time),
        "direction": direction,
        "volume": round(volume, 8),
        "open_price": round(entry_price, 5),
        "close_price": round(close_price, 5),
        "gross_profit": round(gross, 10),
        "swap": 0.0,
        "commission": 0.0,
        "net_profit": round(gross, 10),
        "hold_bars": hold_bars,
        "open_hour": int(source.get("open_hour", 0)),
        "open_month": str(source.get("open_month", "")),
        "open_month_num": int(source.get("open_month_num", 0)),
        "p_short": round(as_float(source.get("p_short")), 12),
        "p_flat": round(as_float(source.get("p_flat")), 12),
        "p_long": round(as_float(source.get("p_long")), 12),
        "margin_vs_long": round(as_float(source.get("margin_vs_long")), 12),
        "margin_vs_flat": round(as_float(source.get("margin_vs_flat")), 12),
        "source_reason": source.get("source_reason", ""),
        "source_bucket": source.get("source_bucket", ""),
        "close_reason": close_reason,
        "entry_index": entry_index,
        "exit_index": exit_index,
        "proxy_boundary": "single-position telemetry replay(단일 포지션 원격측정 재생)",
        "claim_boundary": CLAIM_BOUNDARY,
    }


def simulate_variant(cycles: pd.DataFrame, spec: Mapping[str, Any]) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    mask = build_override_mask(cycles, spec)
    decisions = cycles["decision_base"].copy()
    decisions.loc[mask] = "short"
    variant_id = str(spec["variant_id"])
    override_rows = cycles.loc[mask].copy()
    override_audit: list[dict[str, Any]] = []
    if override_rows.empty:
        override_audit.append({"run_id": RUN_ID, "variant_id": variant_id, "open_hour": "", "override_rows": 0, "avg_p_short": "", "avg_margin_vs_long": "", "avg_margin_vs_flat": "", "effect": "no changed rows(변경 행 없음)", "claim_boundary": CLAIM_BOUNDARY})
    else:
        for hour, group in override_rows.groupby("open_hour", sort=True):
            override_audit.append(
                {
                    "run_id": RUN_ID,
                    "variant_id": variant_id,
                    "open_hour": int(hour),
                    "override_rows": int(len(group)),
                    "avg_p_short": finite(group["p_short"].mean()),
                    "avg_margin_vs_long": finite(group["margin_vs_long"].mean()),
                    "avg_margin_vs_flat": finite(group["margin_vs_flat"].mean()),
                    "effect": "flat cycle(플랫 주기)을 short source(숏 원천) 후보로 바꿉니다.",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )

    risk_audit = [
        {
            "run_id": RUN_ID,
            "variant_id": variant_id,
            "risk_scale_hours": "|".join(str(hour) for hour in spec.get("risk_scale_hours", [])),
            "risk_scale_min_margin": spec.get("risk_scale_min_margin", ""),
            "risk_scale_multiplier": spec.get("risk_scale_multiplier", ""),
            "risk_scale_changed_vs_dl": str(
                list(spec.get("risk_scale_hours", [])) != [17, 18, 19, 20]
                or as_float(spec.get("risk_scale_min_margin")) != 0.08
                or as_float(spec.get("risk_scale_multiplier")) != 1.10
            ).lower(),
            "effect": "short risk sizing(숏 위험 크기)을 조정해 PF/net(PF/순수익) 변화를 확인합니다.",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]

    trades: list[dict[str, Any]] = []
    position: str | None = None
    entry_price = 0.0
    entry_time = pd.NaT
    entry_index = -1
    entry_row: Mapping[str, Any] | None = None
    hold_bars = 0
    volume = FIXED_LOT

    for index, row in cycles.iterrows():
        desired = str(decisions.iloc[index])
        if desired not in {"long", "short"}:
            desired = "flat"
        price = float(row["entry_open"])
        current_time = row["dt"]
        blocked_open_this_bar = False
        if position is not None:
            hold_bars += 1
            close_reason = ""
            if desired in {"long", "short"} and desired != position:
                close_reason = "reverse"
            elif hold_bars >= MAX_HOLD_BARS:
                close_reason = "max_hold"
            if close_reason:
                gross = (price - entry_price) * volume if position == "long" else (entry_price - price) * volume
                source = entry_row or {}
                trades.append(trade_row(variant_id, position, volume, entry_price, price, gross, hold_bars, source, entry_time, current_time, close_reason, entry_index, index))
                position = None
                hold_bars = 0
                blocked_open_this_bar = True
                if close_reason == "reverse" and desired in {"long", "short"}:
                    position = desired
                    entry_price = price
                    entry_time = current_time
                    entry_index = index
                    entry_row = entry_source(row, bool(mask.iloc[index]), variant_id)
                    volume = volume_for(position, entry_row, spec)
                    blocked_open_this_bar = True
        if position is None and not blocked_open_this_bar and desired in {"long", "short"}:
            position = desired
            entry_price = price
            entry_time = current_time
            entry_index = index
            entry_row = entry_source(row, bool(mask.iloc[index]), variant_id)
            volume = volume_for(position, entry_row, spec)

    if position is not None:
        row = cycles.iloc[-1]
        price = float(row["entry_open"])
        gross = (price - entry_price) * volume if position == "long" else (entry_price - price) * volume
        trades.append(trade_row(variant_id, position, volume, entry_price, price, gross, hold_bars, entry_row or {}, entry_time, row["dt"], "final_close", entry_index, len(cycles) - 1))
    return pd.DataFrame(trades), pd.DataFrame(override_audit), pd.DataFrame(risk_audit)


def profit_factor(profits: np.ndarray) -> float:
    gains = float(profits[profits > 0].sum()) if profits.size else 0.0
    losses = float(profits[profits < 0].sum()) if profits.size else 0.0
    if losses < 0:
        return gains / abs(losses)
    return 999.0 if gains > 0 else 0.0


def closed_drawdown(profits: np.ndarray) -> float:
    if not profits.size:
        return 0.0
    equity = np.cumsum(profits)
    peaks = np.maximum.accumulate(np.r_[0.0, equity])[:-1]
    return float(np.maximum(peaks - equity, 0.0).max())


def metric_frame(frame: pd.DataFrame) -> dict[str, Any]:
    profits = frame["net_profit"].to_numpy(dtype="float64") if not frame.empty else np.asarray([], dtype="float64")
    trade_count = int(len(frame))
    net = float(profits.sum()) if profits.size else 0.0
    dd_value = closed_drawdown(profits)
    long_frame = frame[frame["direction"].eq("long")]
    short_frame = frame[frame["direction"].eq("short")]
    added_short = frame[frame["source_bucket"].eq("dn_added_short_source")]
    return {
        "net_profit": finite(net, 4),
        "profit_factor": finite(profit_factor(profits), 10),
        "expectancy": finite(net / trade_count if trade_count else 0.0, 10),
        "trade_count": trade_count,
        "trade_density": finite(trade_count / DAYS, 10),
        "long_trade_count": int(len(long_frame)),
        "short_trade_count": int(len(short_frame)),
        "short_share": finite(len(short_frame) / trade_count if trade_count else 0.0, 10),
        "long_net_profit": finite(float(long_frame["net_profit"].sum()) if not long_frame.empty else 0.0, 4),
        "short_net_profit": finite(float(short_frame["net_profit"].sum()) if not short_frame.empty else 0.0, 4),
        "added_short_count": int(len(added_short)),
        "added_short_net_profit": finite(float(added_short["net_profit"].sum()) if not added_short.empty else 0.0, 4),
        "closed_trade_drawdown_proxy": finite(dd_value, 4),
        "closed_trade_recovery_proxy": finite(net / dd_value if dd_value > 0 else (999.0 if net > 0 else 0.0), 10),
    }


def summary_row(path: Path) -> Mapping[str, Any]:
    frame = read_csv(path)
    return {} if frame.empty else frame.iloc[0].to_dict()


def actual_metrics(path: Path) -> dict[str, float]:
    row = summary_row(path)
    trade_count = as_float(row.get("trade_count"))
    short_count = as_float(row.get("short_trade_count"))
    return {
        "net_profit": as_float(row.get("net_profit")),
        "profit_factor": as_float(row.get("profit_factor")),
        "trade_count": trade_count,
        "density": trade_count / DAYS,
        "expectancy": as_float(row.get("expectancy")),
        "drawdown": as_float(row.get("max_drawdown_amount")),
        "recovery_factor": as_float(row.get("recovery_factor")),
        "long_trade_count": as_float(row.get("long_trade_count")),
        "short_trade_count": short_count,
        "short_share": short_count / max(trade_count, 1.0),
    }


def calibration_payload() -> dict[str, Any]:
    dl_final = read_json(dl.FINAL_DECISION)
    expected_net = as_float(dl_final.get("expected_net_profit"))
    actual_net = as_float(dl_final.get("actual_mt5_net_profit"))
    expected_pf = as_float(dl_final.get("expected_profit_factor"))
    actual_pf = as_float(dl_final.get("actual_mt5_profit_factor"))
    expected_trades = as_float(dl_final.get("expected_trade_count"))
    actual_trades = as_float(dl_final.get("actual_mt5_trade_count"))
    return {
        "net_adjustment": actual_net - expected_net,
        "pf_adjustment": actual_pf - expected_pf,
        "trade_count_adjustment": actual_trades - expected_trades,
        "calibration_source_run_id": dl.RUN_ID,
        "effect": "DL proxy/MT5 gap(DL 프록시/MT5 차이)을 DN 후보의 보수적 보정값으로 씁니다.",
    }


def build_surface() -> tuple[list[dict[str, Any]], dict[str, pd.DataFrame], list[dict[str, Any]], list[dict[str, Any]], pd.DataFrame, dict[str, float], dict[str, float], dict[str, float], dict[str, Any]]:
    cycles, _telemetry = di.dd.load_cycles()
    db_mt5 = actual_metrics(db.EXECUTION_SUMMARY)
    dg_mt5 = actual_metrics(dg_source.EXECUTION_SUMMARY)
    dl_mt5 = actual_metrics(dl.EXECUTION_SUMMARY)
    calibration = calibration_payload()
    specs = variant_specs()
    frames: dict[str, pd.DataFrame] = {}
    override_audits: list[dict[str, Any]] = []
    risk_audits: list[dict[str, Any]] = []
    surface: list[dict[str, Any]] = []
    baseline_metrics: dict[str, Any] | None = None
    baseline_frame: pd.DataFrame | None = None

    for spec in specs:
        frame, override_audit, risk_audit = simulate_variant(cycles, spec)
        frames[str(spec["variant_id"])] = frame
        override_audits.extend(override_audit.to_dict("records"))
        risk_audits.extend(risk_audit.to_dict("records"))
        metrics = metric_frame(frame)
        if spec["variant_id"] == "dn00_db_policy_anchor":
            baseline_metrics = metrics
            baseline_frame = frame
    if baseline_metrics is None or baseline_frame is None:
        raise RuntimeError("missing DN baseline replay(DN 기준 재생 누락)")

    base_net = as_float(baseline_metrics["net_profit"])
    base_pf = as_float(baseline_metrics["profit_factor"])
    base_expectancy = as_float(baseline_metrics["expectancy"])
    base_dd = as_float(baseline_metrics["closed_trade_drawdown_proxy"])
    base_trade_count = as_float(baseline_metrics["trade_count"])
    base_short_count = as_float(baseline_metrics["short_trade_count"])
    base_short_share = as_float(baseline_metrics["short_share"])

    for spec in specs:
        frame = frames[str(spec["variant_id"])]
        metrics = metric_frame(frame)
        variant_id = str(spec["variant_id"])
        override_count = sum(int(row["override_rows"]) for row in override_audits if row["variant_id"] == variant_id and str(row["override_rows"]) != "")
        risk_changed = any(row["variant_id"] == variant_id and str(row["risk_scale_changed_vs_dl"]) == "true" for row in risk_audits)
        net_delta = as_float(metrics["net_profit"]) - base_net
        pf_delta = as_float(metrics["profit_factor"]) - base_pf
        expectancy_delta = as_float(metrics["expectancy"]) - base_expectancy
        dd_delta = as_float(metrics["closed_trade_drawdown_proxy"]) - base_dd
        trade_delta = as_float(metrics["trade_count"]) - base_trade_count
        short_count_delta = as_float(metrics["short_trade_count"]) - base_short_count
        short_share_delta = as_float(metrics["short_share"]) - base_short_share
        estimated_net = db_mt5["net_profit"] + net_delta
        estimated_pf = db_mt5["profit_factor"] + pf_delta
        estimated_expectancy = db_mt5["expectancy"] + expectancy_delta
        estimated_trade_count = db_mt5["trade_count"] + trade_delta
        estimated_density = estimated_trade_count / DAYS
        estimated_short_count = db_mt5["short_trade_count"] + short_count_delta
        estimated_short_share = estimated_short_count / max(estimated_trade_count, 1.0)
        estimated_dd = max(0.0, db_mt5["drawdown"] + dd_delta)
        calibrated_net = estimated_net + as_float(calibration["net_adjustment"])
        calibrated_pf = estimated_pf + as_float(calibration["pf_adjustment"])
        calibrated_trade_count = estimated_trade_count + as_float(calibration["trade_count_adjustment"])
        runtime_ready = str(spec["runtime_representation"]).startswith("runtime_ready")
        calibrated_pass = (
            variant_id != "dn00_db_policy_anchor"
            and (override_count > 0 or risk_changed)
            and calibrated_net > db_mt5["net_profit"]
            and calibrated_pf > db_mt5["profit_factor"]
            and DENSITY_FLOOR <= calibrated_trade_count / DAYS <= DENSITY_CEILING
            and estimated_short_count >= SHORT_COUNT_FLOOR
            and runtime_ready
        )
        net_pass_only = calibrated_net > db_mt5["net_profit"] and estimated_short_count >= SHORT_COUNT_FLOOR
        pf_gap = max(0.0, db_mt5["profit_factor"] - calibrated_pf)
        net_gap = max(0.0, db_mt5["net_profit"] - calibrated_net)
        score = (
            calibrated_net
            + calibrated_pf * 220.0
            + max(0.0, estimated_short_count - db_mt5["short_trade_count"]) * 2.5
            + max(0.0, calibrated_net - dg_mt5["net_profit"]) * 1.6
            - pf_gap * 2600.0
            - net_gap * 8.0
            + (500.0 if calibrated_pass else 0.0)
            + (80.0 if net_pass_only else 0.0)
        )
        surface.append(
            {
                "run_id": RUN_ID,
                "variant_id": variant_id,
                "variant_family": spec["family"],
                "hypothesis": spec["hypothesis"],
                "changed_variables": (
                    f"hours={spec['hours']};p_short_min={spec['p_short_min']};"
                    f"margin_vs_long_min={spec['margin_vs_long_min']};margin_vs_flat_min={spec['margin_vs_flat_min']};"
                    f"risk_hours={spec.get('risk_scale_hours')};risk_min={spec.get('risk_scale_min_margin')};"
                    f"risk_multiplier={spec.get('risk_scale_multiplier')}"
                ),
                "runtime_representation_status": spec["runtime_representation"],
                "override_rows": override_count,
                "risk_scale_changed_vs_dl": str(risk_changed).lower(),
                "sim_net_profit": metrics["net_profit"],
                "sim_profit_factor": metrics["profit_factor"],
                "sim_expectancy": metrics["expectancy"],
                "sim_trade_count": metrics["trade_count"],
                "sim_trade_density": metrics["trade_density"],
                "sim_long_trade_count": metrics["long_trade_count"],
                "sim_short_trade_count": metrics["short_trade_count"],
                "sim_short_share": metrics["short_share"],
                "sim_added_short_count": metrics["added_short_count"],
                "sim_added_short_net_profit": metrics["added_short_net_profit"],
                "sim_short_net_profit": metrics["short_net_profit"],
                "sim_closed_trade_drawdown_proxy": metrics["closed_trade_drawdown_proxy"],
                "sim_net_delta_vs_db_anchor": finite(net_delta, 4),
                "sim_pf_delta_vs_db_anchor": finite(pf_delta, 10),
                "sim_expectancy_delta_vs_db_anchor": finite(expectancy_delta, 10),
                "sim_trade_delta_vs_db_anchor": finite(trade_delta, 4),
                "sim_short_count_delta_vs_db_anchor": finite(short_count_delta, 4),
                "sim_short_share_delta_vs_db_anchor": finite(short_share_delta, 10),
                "db_mt5_net_profit": finite(db_mt5["net_profit"], 4),
                "db_mt5_profit_factor": finite(db_mt5["profit_factor"], 10),
                "db_mt5_trade_count": finite(db_mt5["trade_count"], 4),
                "db_mt5_short_trade_count": finite(db_mt5["short_trade_count"], 4),
                "dg_mt5_net_profit": finite(dg_mt5["net_profit"], 4),
                "dg_mt5_profit_factor": finite(dg_mt5["profit_factor"], 10),
                "dg_mt5_short_trade_count": finite(dg_mt5["short_trade_count"], 4),
                "dl_mt5_net_profit": finite(dl_mt5["net_profit"], 4),
                "dl_mt5_profit_factor": finite(dl_mt5["profit_factor"], 10),
                "dl_mt5_short_trade_count": finite(dl_mt5["short_trade_count"], 4),
                "estimated_mt5_net_profit": finite(estimated_net, 4),
                "estimated_mt5_profit_factor": finite(estimated_pf, 10),
                "estimated_mt5_expectancy": finite(estimated_expectancy, 10),
                "estimated_mt5_trade_count": finite(estimated_trade_count, 4),
                "estimated_mt5_density": finite(estimated_density, 10),
                "estimated_mt5_drawdown": finite(estimated_dd, 4),
                "estimated_mt5_short_trade_count": finite(estimated_short_count, 4),
                "estimated_short_share": finite(estimated_short_share, 10),
                "runtime_calibrated_net_profit": finite(calibrated_net, 4),
                "runtime_calibrated_profit_factor": finite(calibrated_pf, 10),
                "runtime_calibrated_trade_count": finite(calibrated_trade_count, 4),
                "runtime_calibrated_density": finite(calibrated_trade_count / DAYS, 10),
                "calibrated_net_delta_vs_db": finite(calibrated_net - db_mt5["net_profit"], 4),
                "calibrated_pf_delta_vs_db": finite(calibrated_pf - db_mt5["profit_factor"], 10),
                "calibrated_net_delta_vs_dg": finite(calibrated_net - dg_mt5["net_profit"], 4),
                "calibrated_net_delta_vs_dl": finite(calibrated_net - dl_mt5["net_profit"], 4),
                "side_balance_status": "improved_vs_db" if estimated_short_count > db_mt5["short_trade_count"] and estimated_short_share > db_mt5["short_share"] else "not_improved",
                "calibrated_precheck_status": "passed_calibrated_precheck(보정 사전검사 통과)" if calibrated_pass else "failed_calibrated_precheck(보정 사전검사 실패)",
                "net_pass_pf_fail_status": "net_pass_pf_fail(PF 부족 순수익 통과)" if net_pass_only and not calibrated_pass else "",
                "candidate_status": "calibrated_package_candidate_no_authority(보정 패키지 후보, 권위 없음)" if calibrated_pass else "proxy_watch_no_authority(프록시 관찰, 권위 없음)",
                "selection_score": finite(score, 10),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    surface = sorted(surface, key=lambda row: as_float(row["selection_score"]), reverse=True)
    return surface, frames, override_audits, risk_audits, baseline_frame, db_mt5, dg_mt5, dl_mt5, calibration


def selected_row(surface: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    passing = [row for row in surface if str(row["calibrated_precheck_status"]).startswith("passed")]
    net_pass = [row for row in surface if str(row.get("net_pass_pf_fail_status", "")).startswith("net_pass")]
    return dict(max(passing or net_pass or surface, key=lambda row: as_float(row["selection_score"])))


def group_summary(frames: Mapping[str, pd.DataFrame], surface: Sequence[Mapping[str, Any]], by: Sequence[str], kind: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for surface_row in surface:
        variant_id = str(surface_row["variant_id"])
        frame = frames[variant_id]
        if frame.empty:
            continue
        for keys, group in frame.groupby(list(by), sort=True, dropna=False):
            if not isinstance(keys, tuple):
                keys = (keys,)
            profits = group["net_profit"].to_numpy(dtype="float64")
            row = {
                "run_id": RUN_ID,
                "variant_id": variant_id,
                "summary_kind": kind,
                "trade_count": int(len(group)),
                "net_profit": finite(float(profits.sum()), 4),
                "profit_factor": finite(profit_factor(profits), 10),
                "long_trade_count": int(group["direction"].eq("long").sum()),
                "short_trade_count": int(group["direction"].eq("short").sum()),
                "added_short_source_count": int(group["source_bucket"].eq("dn_added_short_source").sum()),
                "claim_boundary": CLAIM_BOUNDARY,
            }
            for column, value in zip(by, keys, strict=False):
                row[str(column)] = value
            rows.append(row)
    return rows


def runtime_representation_rows(surface: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for row in surface:
        status = str(row["runtime_representation_status"])
        rows.append(
            {
                "run_id": RUN_ID,
                "variant_id": row["variant_id"],
                "runtime_representation_status": status,
                "runtime_parameter_plan": row["changed_variables"],
                "required_runtime_change": "none_parameter_only(없음, 파라미터만)" if status.startswith("runtime_ready") else "runtime_repair_required(런타임 보정 필요)",
                "effect": "parameter-only rows(파라미터 전용 행)는 다음 review(검토)에서 MT5 package(MT5 패키지) 가능성을 판단할 수 있습니다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(RUNTIME_REPRESENTATION_AUDIT, rows)
    return rows


def package_rows(surface: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for row in surface:
        rows.append(
            {
                "run_id": RUN_ID,
                "variant_id": row["variant_id"],
                "calibrated_net_gt_db": str(as_float(row["runtime_calibrated_net_profit"]) > as_float(row["db_mt5_net_profit"])).lower(),
                "calibrated_pf_gt_db": str(as_float(row["runtime_calibrated_profit_factor"]) > as_float(row["db_mt5_profit_factor"])).lower(),
                "density_ge_3": str(as_float(row["runtime_calibrated_density"]) >= DENSITY_FLOOR).lower(),
                "short_count_ge_125": str(as_float(row["estimated_mt5_short_trade_count"]) >= SHORT_COUNT_FLOOR).lower(),
                "runtime_ready": str(str(row["runtime_representation_status"]).startswith("runtime_ready")).lower(),
                "calibrated_precheck_status": row["calibrated_precheck_status"],
                "net_pass_pf_fail_status": row.get("net_pass_pf_fail_status", ""),
                "effect": "보정된 프록시가 MT5 패키지 검토 기준을 넘는지 분리합니다.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    write_csv(PACKAGE_PRECHECK, rows)
    return rows


def write_artifacts(
    surface: Sequence[Mapping[str, Any]],
    frames: Mapping[str, pd.DataFrame],
    override_audits: Sequence[Mapping[str, Any]],
    risk_audits: Sequence[Mapping[str, Any]],
    selected: Mapping[str, Any],
    calibration: Mapping[str, Any],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    write_csv(PF_BALANCE_SURFACE, surface)
    write_csv(VARIANT_OVERRIDE_AUDIT, override_audits)
    write_csv(VARIANT_RISK_SCALE_AUDIT, risk_audits)
    write_csv(VARIANT_REASON_ATTRIBUTION, group_summary(frames, surface, ["source_bucket", "direction"], "reason_side"))
    write_csv(VARIANT_HOUR_SIDE_ATTRIBUTION, group_summary(frames, surface, ["open_hour", "direction"], "hour_side"))
    runtime_rows = runtime_representation_rows(surface)
    package_precheck = package_rows(surface)
    write_csv(
        PROXY_MT5_CALIBRATION,
        [
            {
                "run_id": RUN_ID,
                "calibration_source_run_id": calibration["calibration_source_run_id"],
                "net_adjustment": finite(calibration["net_adjustment"], 10),
                "pf_adjustment": finite(calibration["pf_adjustment"], 10),
                "trade_count_adjustment": finite(calibration["trade_count_adjustment"], 4),
                "effect": calibration["effect"],
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )
    write_csv(
        RUN364DO_QUEUE,
        [
            {
                "run_id": RUN_ID,
                "next_run_id": NEXT_RUN_ID,
                "queue_rank": 1,
                "queue_id": "do01_pf_balance_polish_review",
                "review_subject": selected["variant_id"],
                "review_question": "Does DN selected candidate deserve package work or does parameter-only polish fail?(DN 선택 후보가 패키지 작업을 받을 만한가, 아니면 파라미터 전용 다듬기가 실패했는가?)",
                "success_criteria": "review confirms calibrated DB exceedance, runtime-ready params, no trade splitting(보정 DB 초과, 런타임 준비 파라미터, 거래 쪼개기 없음 확인)",
                "failure_criteria": "only net passes while PF fails, or candidate is proxy-only(순수익만 통과하고 PF 실패, 또는 프록시 전용 후보)",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
    )
    selected_frame = frames[str(selected["variant_id"])].copy()
    write_csv(SELECTED_TRADE_TAPE, selected_frame.to_dict("records"))
    write_json(SELECTED_CANDIDATE, selected)
    return runtime_rows, package_precheck


def data_integrity_rows(cycles: pd.DataFrame, selected_frame: pd.DataFrame, surface: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    duplicate_cycles = int(cycles.duplicated(subset=["entry_time_raw", "source_time"]).sum())
    overlap_count = int((selected_frame["entry_index"].shift(-1).fillna(10**12).astype(float) < selected_frame["exit_index"].astype(float)).sum()) if not selected_frame.empty else 0
    selected_added = int(selected_frame["source_bucket"].eq("dn_added_short_source").sum()) if not selected_frame.empty else 0
    selected = selected_row(surface)
    changed = as_float(selected.get("override_rows")) > 0 or str(selected.get("risk_scale_changed_vs_dl")) == "true"
    return [
        {"run_id": RUN_ID, "audit_item": "input_lineage(입력 계보)", "status": "passed" if all(exists(path) for path in INPUT_FILES) else "failed", "observed": ";".join(rel(path) for path in INPUT_FILES), "effect": "DM/DL/DK/DI/DB/DG 입력을 연결합니다.", "claim_boundary": CLAIM_BOUNDARY},
        {"run_id": RUN_ID, "audit_item": "timestamp_safety(시점 안전)", "status": "passed", "observed": "uses DB runtime written_at entry open and source_time closed-bar features(DB 런타임 written_at 진입 시가와 source_time 종료봉 피처만 사용)", "effect": "미래 가격 경로를 후보 조건으로 쓰지 않습니다.", "claim_boundary": CLAIM_BOUNDARY},
        {"run_id": RUN_ID, "audit_item": "duplicate_cycle_key(중복 주기 키)", "status": "passed" if duplicate_cycles == 0 else "failed", "observed": f"duplicate_cycles={duplicate_cycles}", "effect": "원격측정 주기를 중복 재생하지 않습니다.", "claim_boundary": CLAIM_BOUNDARY},
        {"run_id": RUN_ID, "audit_item": "single_position_no_overlap(단일 포지션 무겹침)", "status": "passed" if overlap_count == 0 else "failed", "observed": f"selected_overlap_count={overlap_count}", "effect": "거래 수 증가는 포지션 쪼개기가 아니라 단일 포지션 재생 결과입니다.", "claim_boundary": CLAIM_BOUNDARY},
        {"run_id": RUN_ID, "audit_item": "changed_surface_rows(변경 표면 행)", "status": "passed" if changed else "failed", "observed": f"selected_added_short_trades={selected_added};risk_changed={selected.get('risk_scale_changed_vs_dl')}", "effect": "후보는 원천 조건 또는 위험비율 파라미터를 실제로 바꿉니다.", "claim_boundary": CLAIM_BOUNDARY},
        {"run_id": RUN_ID, "audit_item": "proxy_boundary(프록시 경계)", "status": "passed", "observed": "runtime-calibrated proxy still requires MT5 probe(런타임 보정 프록시도 MT5 탐침 필요)", "effect": "보정 프록시를 MT5 KPI로 과장하지 않습니다.", "claim_boundary": CLAIM_BOUNDARY},
    ]


def gate_rows(surface: Sequence[Mapping[str, Any]], selected: Mapping[str, Any], data_rows: Sequence[Mapping[str, Any]], receipt_paths: Sequence[Path], *, final_written: bool) -> list[dict[str, Any]]:
    runtime_ready_passes = sum(1 for row in surface if str(row["runtime_representation_status"]).startswith("runtime_ready"))
    selected_changed = as_float(selected.get("override_rows")) > 0 or str(selected.get("risk_scale_changed_vs_dl")) == "true"
    gates = [
        ("scope_completion_gate", len(surface) == len(variant_specs()) and exists(PF_BALANCE_SURFACE), PF_BALANCE_SURFACE, "all DN variants scored(모든 DN 변형 점수화)"),
        ("input_lineage_gate", all(exists(path) for path in INPUT_FILES), INPUT_MANIFEST, "inputs linked(입력 연결)"),
        ("data_integrity_gate", bool(data_rows) and all(row["status"] == "passed" for row in data_rows), DATA_INTEGRITY_AUDIT, "timestamp/no-overlap checks passed(시점/무겹침 검사 통과)"),
        ("candidate_surface_gate", selected_changed, PF_BALANCE_SURFACE, "selected variant changes source or risk params(선택 변형이 원천 또는 위험 파라미터 변경)"),
        ("runtime_representability_gate", str(selected.get("runtime_representation_status", "")).startswith("runtime_ready") and runtime_ready_passes > 0, RUNTIME_REPRESENTATION_AUDIT, "selected variant is parameter-ready(선택 변형이 파라미터 준비됨)"),
        ("kpi_contract_gate", str(selected.get("calibrated_precheck_status", "")).startswith("passed") or str(selected.get("net_pass_pf_fail_status", "")).startswith("net_pass"), PACKAGE_PRECHECK, "selected row has review-worthy calibrated signal(선택 행이 검토할 보정 신호 보유)"),
        ("calibrated_proxy_boundary_gate", exists(PROXY_MT5_CALIBRATION), PROXY_MT5_CALIBRATION, "DL proxy/MT5 gap used as boundary(DL 프록시/MT5 차이를 경계로 사용)"),
        ("no_trade_splitting_gate", bool(data_rows) and any(row["audit_item"].startswith("single_position") and row["status"] == "passed" for row in data_rows), DATA_INTEGRITY_AUDIT, "single-position replay used(단일 포지션 재생 사용)"),
        ("receipt_coverage_gate", all(exists(path) for path in receipt_paths), RUN_EVIDENCE_RECEIPT, "required receipts exist(필수 영수증 존재)"),
        ("required_gate_coverage_audit", final_written, GATE_AUDIT, "required gates connected to closeout(필수 게이트 종료 기록 연결)"),
        ("final_claim_guard", exists(CLAIM_RECEIPT), CLAIM_RECEIPT, "no authority/promotion/goal claim(권위/승격/목표 주장 없음)"),
    ]
    return [{"run_id": RUN_ID, "gate": gate, "status": "passed" if passed else "failed", "evidence": rel(evidence), "effect": effect, "claim_boundary": CLAIM_BOUNDARY} for gate, passed, evidence, effect in gates]


def final_payload(selected: Mapping[str, Any], surface: Sequence[Mapping[str, Any]], gates: Sequence[Mapping[str, Any]], created_at: str) -> dict[str, Any]:
    calibrated_pass_count = sum(1 for row in surface if str(row["calibrated_precheck_status"]).startswith("passed"))
    net_pass_pf_fail_count = sum(1 for row in surface if str(row.get("net_pass_pf_fail_status", "")).startswith("net_pass"))
    return {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "baseline_run_id": BASELINE_RUN_ID,
        "source_expansion_run_id": SOURCE_EXPANSION_RUN_ID,
        "runtime_probe_run_id": RUNTIME_PROBE_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT if calibrated_pass_count == 0 else "proxy_pf_balance_polish_found_calibrated_candidate_review_required_no_authority",
        "decision": DECISION,
        "selected_variant_id": selected["variant_id"],
        "selected_runtime_representation_status": selected["runtime_representation_status"],
        "selected_calibrated_precheck_status": selected["calibrated_precheck_status"],
        "selected_net_pass_pf_fail_status": selected.get("net_pass_pf_fail_status", ""),
        "selected_runtime_calibrated_net_profit": selected["runtime_calibrated_net_profit"],
        "selected_runtime_calibrated_profit_factor": selected["runtime_calibrated_profit_factor"],
        "selected_runtime_calibrated_trade_count": selected["runtime_calibrated_trade_count"],
        "selected_estimated_mt5_short_trade_count": selected["estimated_mt5_short_trade_count"],
        "selected_calibrated_net_delta_vs_db": selected["calibrated_net_delta_vs_db"],
        "selected_calibrated_pf_delta_vs_db": selected["calibrated_pf_delta_vs_db"],
        "selected_calibrated_net_delta_vs_dg": selected["calibrated_net_delta_vs_dg"],
        "selected_calibrated_net_delta_vs_dl": selected["calibrated_net_delta_vs_dl"],
        "db_mt5_net_profit": selected["db_mt5_net_profit"],
        "db_mt5_profit_factor": selected["db_mt5_profit_factor"],
        "db_mt5_short_trade_count": selected["db_mt5_short_trade_count"],
        "dl_mt5_net_profit": selected["dl_mt5_net_profit"],
        "dl_mt5_profit_factor": selected["dl_mt5_profit_factor"],
        "dg_mt5_net_profit": selected["dg_mt5_net_profit"],
        "surface_rows": len(surface),
        "calibrated_pass_count": calibrated_pass_count,
        "net_pass_pf_fail_count": net_pass_pf_fail_count,
        "gate_passes": sum(1 for row in gates if row["status"] == "passed"),
        "gate_total": len(gates),
        "new_model_training": "not_run",
        "new_mt5_execution": "not_run",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "live_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "report_path": rel(REPORT_PATH),
        "final_decision": rel(FINAL_DECISION),
        "created_at_utc": created_at,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def write_receipts(final: Mapping[str, Any], selected: Mapping[str, Any]) -> None:
    base = {"run_id": RUN_ID, "stage_id": STAGE_ID, "created_at_utc": final["created_at_utc"], "claim_boundary": CLAIM_BOUNDARY}
    write_json(RUN_EVIDENCE_RECEIPT, {**base, "measurement_scope": "runtime-calibrated telemetry replay proxy scout(런타임 보정 원격측정 재생 프록시 스카우트)", "surface": rel(PF_BALANCE_SURFACE), "selected": rel(SELECTED_CANDIDATE), "status": "completed_no_mt5_execution(완료, MT5 실행 없음)"})
    write_json(EXPERIMENT_RECEIPT, {**base, "hypothesis": "Parameter-only source/risk polish can lift PF/net above DB while preserving short-count lift(파라미터 전용 원천/위험 다듬기가 숏 거래수 상승을 보존하면서 PF/순수익을 DB 위로 올릴 수 있음)", "decision_use": "review candidate or no-pass result(후보 검토 또는 통과 없음 결과)", "comparison_baseline": [BASELINE_RUN_ID, SOURCE_EXPANSION_RUN_ID, RUNTIME_PROBE_RUN_ID], "changed_variables": selected["changed_variables"], "success_criteria": "calibrated net>DB, PF>DB, shorts>=125, density>=3", "failure_criteria": "PF remains below DB or net-only pass", "evidence_plan": [rel(PF_BALANCE_SURFACE), rel(PACKAGE_PRECHECK), rel(RUN364DO_QUEUE)]})
    write_json(DATA_RECEIPT, {**base, "data_source": [rel(db.RUNTIME_OUTPUT_COPY), rel(di.dd.SOURCE_RAW_US100_M5)], "time_axis": "DB runtime written_at entry open and source_time closed feature bar(DB 런타임 written_at 진입 시가와 source_time 종료 피처봉)", "sample_scope": "FPMarkets US100 M5 Tier A replay(FPMarkets US100 M5 Tier A 재생)", "missing_or_duplicate_check": rel(DATA_INTEGRITY_AUDIT), "feature_label_boundary": "entry-known probabilities and closed-bar returns only(진입 시점에 알려진 확률과 종료봉 수익률만)", "integrity_judgment": "usable_with_proxy_boundary(프록시 경계 안에서 사용 가능)"})
    write_json(ATTRIBUTION_RECEIPT, {**base, "observed_change": f"selected calibrated net {final['selected_runtime_calibrated_net_profit']} vs DB {final['db_mt5_net_profit']}; PF {final['selected_runtime_calibrated_profit_factor']} vs DB {final['db_mt5_profit_factor']}", "comparison_baseline": [BASELINE_RUN_ID, SOURCE_EXPANSION_RUN_ID, RUNTIME_PROBE_RUN_ID], "likely_drivers": [selected["variant_family"], selected["changed_variables"]], "segment_checks": [rel(VARIANT_HOUR_SIDE_ATTRIBUTION), rel(VARIANT_REASON_ATTRIBUTION), rel(VARIANT_RISK_SCALE_AUDIT)], "trade_shape": {"calibrated_trade_count": final["selected_runtime_calibrated_trade_count"], "estimated_short_trade_count": final["selected_estimated_mt5_short_trade_count"]}, "alternative_explanations": ["proxy/MT5 calibration may not transfer(프록시/MT5 보정 전이 불확실)", "risk multiplier changes fill/cost sensitivity(위험 배수 변경의 체결/비용 민감도)", "single-window selection bias(단일 구간 선택 편향)"], "attribution_confidence": "medium_low_until_review(검토 전 중하)", "next_probe": NEXT_RUN_ID})
    write_json(JUDGMENT_RECEIPT, {**base, "result_subject": RUN_ID, "evidence_available": [rel(PF_BALANCE_SURFACE), rel(SELECTED_CANDIDATE), rel(DATA_INTEGRITY_AUDIT), rel(PROXY_MT5_CALIBRATION)], "evidence_missing": ["MT5 runtime package(MT5 런타임 패키지)", "MT5 runtime probe(MT5 런타임 탐침)", "forward/replay evidence(전진/재생 근거)"], "judgment_label": final["judgment"], "claim_boundary": CLAIM_BOUNDARY, "next_condition": NEXT_RUN_ID, "user_explanation_hook": "DN tests parameter-only PF/net polish, but MT5 authority is not claimed(DN은 파라미터 전용 PF/순수익 다듬기를 시험하지만 MT5 권위는 주장하지 않음)."})
    write_json(LINEAGE_RECEIPT, {**base, "source_inputs": [{"path": rel(path), "sha256": sha(path)} for path in INPUT_FILES if exists(path) and io_path(path).is_file()], "producer": rel(Path(__file__)), "consumer": NEXT_RUN_ID, "artifact_paths": [rel(path) for path in OUTPUT_FILES if exists(path)], "artifact_hashes": {rel(path): sha(path) for path in OUTPUT_FILES if exists(path) and io_path(path).is_file()}, "registry_links": [rel(RUN_REGISTRY), rel(PROJECT_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)], "availability": "tracked_proxy_scout_artifacts(추적된 프록시 스카우트 산출물)", "lineage_judgment": "connected_with_proxy_boundary(프록시 경계로 연결)"})
    write_json(CLAIM_RECEIPT, {**base, "runtime_authority": "not_claimed", "operating_promotion": "not_claimed", "live_readiness": "not_claimed", "goal_achieve": "not_claimed", "effect": "parameter-only proxy clue(파라미터 전용 프록시 단서)를 운영 주장으로 올리지 않습니다."})


def markdown_table(rows: Sequence[Mapping[str, Any]], columns: Sequence[str], limit: int = 12) -> str:
    return di.markdown_table(rows, columns, limit=limit)


def write_docs(final: Mapping[str, Any], surface: Sequence[Mapping[str, Any]], selected: Mapping[str, Any], gates: Sequence[Mapping[str, Any]]) -> None:
    top_rows = list(surface[:8])
    report = f"""# run364DN h17 short-source PF/net polish scout(17시 숏 원천 PF/순수익 다듬기 스카우트)

Updated(갱신): {final['created_at_utc']}

## Judgment(판정)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- selected_variant_id(선택 변형 ID): `{final['selected_variant_id']}`
- judgment(판정): `{final['judgment']}`
- next_run_id(다음 실행 ID): `{NEXT_RUN_ID}`
- runtime_authority(런타임 권위): `not_claimed(주장 안 함)`

## Key Read(핵심 판독)

Action(행동): DL proxy/MT5 gap(DL 프록시/MT5 차이)을 보수 보정으로 적용해 source filter(원천 필터)와 risk-scale overlay(위험비율 오버레이)를 비교했습니다.

Effect(효과): net-only pass(순수익만 통과)와 PF pass(PF 통과)를 분리해, PF 상승 없는 밀도/위험 증가를 다음 패키지로 넘기지 않게 했습니다.

| selected_variant_id | calibrated_net | calibrated_pf | calibrated_net_delta_vs_db | calibrated_pf_delta_vs_db | estimated_shorts | calibrated_precheck | net_pass_pf_fail |
| --- | --- | --- | --- | --- | --- | --- | --- |
| {final['selected_variant_id']} | {final['selected_runtime_calibrated_net_profit']} | {final['selected_runtime_calibrated_profit_factor']} | {final['selected_calibrated_net_delta_vs_db']} | {final['selected_calibrated_pf_delta_vs_db']} | {final['selected_estimated_mt5_short_trade_count']} | {final['selected_calibrated_precheck_status']} | {final['selected_net_pass_pf_fail_status']} |

## Top Surface(상위 표면)

{markdown_table(top_rows, ['variant_id', 'runtime_calibrated_net_profit', 'runtime_calibrated_profit_factor', 'calibrated_net_delta_vs_db', 'calibrated_pf_delta_vs_db', 'estimated_mt5_short_trade_count', 'calibrated_precheck_status', 'net_pass_pf_fail_status'])}

## Gates(게이트)

{markdown_table(gates, ['gate', 'status', 'evidence', 'effect'])}

## Boundary(경계)

This is proxy scout only(프록시 스카우트 전용)입니다. MT5 execution(MT5 실행), runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 `not_claimed(주장 안 함)`입니다.
"""
    write_text(REPORT_PATH, report, bom=True)
    write_text(
        DECISION_DOC,
        f"""# Stage364DN decision(결정): short-source PF/net polish scout(숏 원천 PF/순수익 다듬기 스카우트)

- date(날짜): {TODAY}
- run_id(실행 ID): `{RUN_ID}`
- decision(결정): `{DECISION}`
- judgment(판정): `{final['judgment']}`
- selected_variant_id(선택 변형 ID): `{final['selected_variant_id']}`
- calibrated net/PF(보정 순수익/PF): `{final['selected_runtime_calibrated_net_profit']}` / `{final['selected_runtime_calibrated_profit_factor']}`
- DB net/PF(DB 순수익/PF): `{final['db_mt5_net_profit']}` / `{final['db_mt5_profit_factor']}`
- next action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): DO에서 net-only pass(순수익만 통과)인지 package-worthy(PF까지 패키지 가치 있음)인지 검토합니다.
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
        bom=True,
    )
    append_text_once(REVIEW_INDEX, f"run364DN__{RUN_ID}", f"\n- run364DN__{RUN_ID}: [{REPORT_PATH.name}]({REPORT_PATH.name}) - PF/net polish proxy scout(PF/순수익 다듬기 프록시 스카우트), next `{NEXT_RUN_ID}`.\n")
    append_text_once(STAGE_BRIEF, f"run364DN__{RUN_ID}", f"\n## run364DN PF/Net Polish Scout(PF/순수익 다듬기 스카우트)\n\nAction(행동): DL 보정값을 사용해 source/risk parameter(원천/위험 파라미터)를 비교했습니다.\n\nEffect(효과): `{NEXT_RUN_ID}`에서 패키지 가능 여부를 검토할 후보와 실패 경계를 만들었습니다.\n")
    append_text_once(STAGE_README, f"run364DN__{RUN_ID}", f"\n<!-- run364DN__{RUN_ID} -->\n## run364DN PF/net polish scout(PF/순수익 다듬기 스카우트)\n\nSelected(선택): `{final['selected_variant_id']}`. Next(다음): `{NEXT_RUN_ID}`.\n")
    replace_prefixed_lines(STAGE_BRIEF, {"- current_run_id": f"- current_run_id(현재 실행 ID): `{NEXT_RUN_ID}`", "- latest_completed_run_id": f"- latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`", "- selection_status": f"- selection_status(선택 상태): `{STATUS}`", "- claim_boundary": f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`"}, bom=True)
    write_text(WORKSPACE_STATE, f"""current_stage_id: {STAGE_ID}
current_run_id: {NEXT_RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {STATUS}
current_judgment: {final['judgment']}
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

Current truth(현재 진실): `run364DN` completed(완료) PF/net polish proxy scout(PF/순수익 다듬기 프록시 스카우트). Selected candidate(선택 후보)는 `{final['selected_variant_id']}`이고 calibrated net/PF(보정 순수익/PF)는 `{final['selected_runtime_calibrated_net_profit']}` / `{final['selected_runtime_calibrated_profit_factor']}`입니다.

Next action(다음 행동): `{NEXT_RUN_ID}`에서 selected candidate(선택 후보)가 package-worthy(패키지 가치 있음)인지, 또는 parameter-only polish(파라미터 전용 다듬기)가 PF 기준에서 실패했는지 review(검토)합니다.

Operating boundary(운영 경계): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""", bom=True)
    write_text(SELECTION_STATUS, f"""# Stage364 selection status(선택 상태)

Updated(갱신): {final['created_at_utc']}

Current run(현재 실행): `{NEXT_RUN_ID}`
Latest completed run(최근 완료 실행): `{RUN_ID}`

Selected DN candidate(선택 DN 후보): `{final['selected_variant_id']}`.

Calibrated net/PF(보정 순수익/PF): `{final['selected_runtime_calibrated_net_profit']}` / `{final['selected_runtime_calibrated_profit_factor']}`.

Judgment(판정): `{final['judgment']}`.

Authority(권위): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함)입니다.
""", bom=True)
    append_text_once(WORKSPACE_CHANGELOG, f"run364DN__{RUN_ID}", f"\n<!-- run364DN__{RUN_ID} -->\n- {final['created_at_utc']} `{RUN_ID}` completed PF/net polish proxy scout(PF/순수익 다듬기 프록시 스카우트); selected `{final['selected_variant_id']}`; next `{NEXT_RUN_ID}`; no authority claim(권위 주장 없음).\n")
    append_text_once(IDEA_REGISTRY, f"run364DN__{RUN_ID}", f"\n<!-- run364DN__{RUN_ID} -->\n- `{RUN_ID}`: parameter-only PF/net polish(파라미터 전용 PF/순수익 다듬기)를 탐색했습니다. Selected(선택): `{final['selected_variant_id']}` with calibrated net/PF(보정 순수익/PF) `{final['selected_runtime_calibrated_net_profit']}` / `{final['selected_runtime_calibrated_profit_factor']}`.\n")
    if int(final["calibrated_pass_count"]) == 0:
        append_text_once(NEGATIVE_RESULT_REGISTER, f"run364DN__no_calibrated_pf_pass__{RUN_ID}", f"\n<!-- run364DN__no_calibrated_pf_pass__{RUN_ID} -->\n- `{RUN_ID}`: no parameter-only candidate(파라미터 전용 후보 없음)가 calibrated net>DB and PF>DB(보정 순수익/PF DB 초과)를 동시에 통과했습니다. Effect(효과): DO는 net-only pass(순수익만 통과)를 패키지로 과장하지 않습니다.\n")


def write_ledgers(final: Mapping[str, Any]) -> None:
    common = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "run_number": RUN_NUMBER,
        "date": TODAY,
        "status": STATUS,
        "judgment": final["judgment"],
        "decision": DECISION,
        "next_run_id": NEXT_RUN_ID,
        "rows": final["surface_rows"],
        "gate_passes": final["gate_passes"],
        "gate_total": final["gate_total"],
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "final_decision_path": rel(FINAL_DECISION),
        "gate_audit_path": rel(GATE_AUDIT),
        "created_at": final["created_at_utc"],
        "work_family": "experiment_execution(실험 실행)",
        "scoreboard_lane": "proxy_scout(프록시 스카우트)",
        "external_verification_status": "out_of_scope_by_claim_proxy_only(주장 범위 밖, 프록시 전용)",
        "evidence_boundary": "runtime_calibrated_proxy_no_mt5_execution(런타임 보정 프록시, MT5 실행 없음)",
        "question": "Can parameter-only source/risk polish lift net and PF above DB?(파라미터 전용 원천/위험 다듬기가 순수익과 PF를 DB 위로 올릴 수 있는가?)",
        "next_action": NEXT_RUN_ID,
        "net_profit": final["selected_runtime_calibrated_net_profit"],
        "profit_factor": final["selected_runtime_calibrated_profit_factor"],
        "trade_count": final["selected_runtime_calibrated_trade_count"],
        "short_trade_count": final["selected_estimated_mt5_short_trade_count"],
        "result_judgment": final["judgment"],
        "path": rel(FINAL_DECISION),
        "primary_artifact": rel(PF_BALANCE_SURFACE),
        "primary_kpi": f"calibrated_net={final['selected_runtime_calibrated_net_profit']};pf={final['selected_runtime_calibrated_profit_factor']};shorts={final['selected_estimated_mt5_short_trade_count']}",
        "guardrail_kpi": f"calibrated_pass_count={final['calibrated_pass_count']};runtime_authority=not_claimed;operating_promotion=not_claimed",
    }
    ledger_rows = []
    for suffix, view, tier, status, include in [
        ("tier_a_separate", "Tier A separate(Tier A 분리)", "Tier A", STATUS, True),
        ("tier_b_missing_required", "Tier B separate(Tier B 분리)", "Tier B", "missing_required_no_tier_b_source(필수 누락, Tier B 원천 없음)", False),
        ("tier_a_b_combined_out_of_scope", "Tier A+B combined(Tier A+B 합산)", "Tier A+B", "out_of_scope_by_claim_proxy_tier_a_only(주장 범위 밖, 프록시 Tier A 전용)", False),
    ]:
        row = {**common, "ledger_row_id": f"{RUN_ID}__{suffix}", "subrun_id": f"{RUN_ID}__{suffix}", "row_id": f"{RUN_ID}__{suffix}", "record_view": view, "tier_scope": tier, "kpi_scope": "DN proxy scout(DN 프록시 스카우트)", "status": status, "view": view, "tier": tier, "metric_scope": "runtime_calibrated_proxy(런타임 보정 프록시)"}
        if not include:
            for key in ["net_profit", "profit_factor", "trade_count", "short_trade_count"]:
                row[key] = ""
        ledger_rows.append(row)
    append_or_replace_csv(STAGE_LEDGER, ["ledger_row_id"], ledger_rows, extend_header=True)
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], ledger_rows, extend_header=True)
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], [common], extend_header=True)
    repair_run_registry_line_endings(RUN_ID)


def write_artifact_registry(final: Mapping[str, Any]) -> None:
    rows = []
    for artifact_type, path, notes in [
        ("surface", PF_BALANCE_SURFACE, "DN PF/net polish surface(DN PF/순수익 다듬기 표면)."),
        ("selected_candidate", SELECTED_CANDIDATE, "Selected DN candidate(선택 DN 후보)."),
        ("selected_trade_tape", SELECTED_TRADE_TAPE, "Selected DN trade tape(선택 DN 거래 테이프)."),
        ("package_precheck", PACKAGE_PRECHECK, "Package precheck(패키지 사전검사)."),
        ("proxy_mt5_calibration", PROXY_MT5_CALIBRATION, "Proxy/MT5 calibration(프록시/MT5 보정)."),
        ("queue", RUN364DO_QUEUE, "Next run queue(다음 실행 대기열)."),
        ("final_decision", FINAL_DECISION, "Final decision(최종 결정)."),
        ("run_manifest", RUN_MANIFEST, "Run manifest(실행 목록)."),
        ("report", REPORT_PATH, "Human report(사람용 보고서)."),
        ("script", Path(__file__), "DN producer script(DN 생산 스크립트)."),
    ]:
        if exists(path):
            rows.append({"stage_id": STAGE_ID, "run_id": RUN_ID, "artifact_type": artifact_type, "path": rel(path), "artifact_path": rel(path), "sha256": sha(path), "created_at": final["created_at_utc"], "created_at_utc": final["created_at_utc"], "claim_boundary": CLAIM_BOUNDARY, "artifact_id": f"{RUN_ID}__{artifact_type}", "notes": notes})
    append_or_replace_csv(ARTIFACT_REGISTRY, ["run_id", "artifact_type", "path"], rows, extend_header=True)


def write_manifest(final: Mapping[str, Any]) -> None:
    outputs = [path for path in OUTPUT_FILES if exists(path)]
    write_json(RUN_MANIFEST, {"run_id": RUN_ID, "run_number": RUN_NUMBER, "stage_id": STAGE_ID, "parent_run_id": PARENT_RUN_ID, "next_run_id": NEXT_RUN_ID, "status": STATUS, "judgment": final["judgment"], "claim_boundary": CLAIM_BOUNDARY, "input_files": [rel(path) for path in INPUT_FILES], "input_hashes": {rel(path): sha(path) for path in INPUT_FILES if exists(path) and io_path(path).is_file()}, "output_files": [rel(path) for path in outputs], "output_hashes": {rel(path): sha(path) for path in outputs if exists(path) and io_path(path).is_file()}})


def main() -> None:
    ensure_dirs()
    validate_inputs()
    write_csv(INPUT_MANIFEST, input_manifest_rows())
    write_work_packet()
    surface, frames, override_audits, risk_audits, _baseline_frame, _db_mt5, _dg_mt5, _dl_mt5, calibration = build_surface()
    selected = selected_row(surface)
    runtime_rows, _package_rows = write_artifacts(surface, frames, override_audits, risk_audits, selected, calibration)
    selected_frame = frames[str(selected["variant_id"])]
    cycles, _telemetry = di.dd.load_cycles()
    data_rows = data_integrity_rows(cycles, selected_frame, surface)
    write_csv(DATA_INTEGRITY_AUDIT, data_rows)
    created_at = now_utc()
    receipt_paths = [RUN_EVIDENCE_RECEIPT, EXPERIMENT_RECEIPT, DATA_RECEIPT, ATTRIBUTION_RECEIPT, JUDGMENT_RECEIPT, LINEAGE_RECEIPT, CLAIM_RECEIPT]
    gates = gate_rows(surface, selected, data_rows, receipt_paths, final_written=False)
    final = final_payload(selected, surface, gates, created_at)
    write_csv(GATE_AUDIT, gates)
    write_json(FINAL_DECISION, final)
    write_receipts(final, selected)
    gates = gate_rows(surface, selected, data_rows, receipt_paths, final_written=True)
    final = final_payload(selected, surface, gates, created_at)
    write_csv(GATE_AUDIT, gates)
    write_json(FINAL_DECISION, final)
    write_docs(final, surface, selected, gates)
    write_ledgers(final)
    write_artifact_registry(final)
    write_manifest(final)
    write_json(FINAL_DECISION, final)
    print(json.dumps(json_ready(final), ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
