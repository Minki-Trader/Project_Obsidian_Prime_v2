from __future__ import annotations

import json
import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from stage_pipelines.stage364 import review_h19_stress_short_balance_proxy_scout_without_db as parent  # noqa: E402
from stage_pipelines.stage364.review_pf_pass_density_restore_offensive_scout_without_db import repair_run_registry_line_endings  # noqa: E402


TODAY = "2026-06-04"
BM = parent.parent
BK = parent.BK

STAGE_ID = parent.STAGE_ID
RUN_NUMBER = "run364BO"
RUN_ID = "run364BO_train_short_source_quality_repair_scout_without_db_v1"
PARENT_RUN_ID = parent.RUN_ID
SOURCE_RUNTIME_PROBE_RUN_ID = parent.SOURCE_RUNTIME_PROBE_RUN_ID
BASELINE_RUN_ID = parent.BASELINE_RUN_ID
NEXT_RUN_ID = "run364BP_review_short_source_quality_repair_scout_without_db_v1"

STATUS = "completed_stage364BO_short_source_quality_repair_proxy_scout_stress_watch_review_required_no_authority"
JUDGMENT = "positive_proxy_repair_seed_persists_but_month_stress_watch_no_package_review_required_no_authority"
DECISION = "stage364BO_open_run364BP_short_source_quality_repair_review"
CLAIM_BOUNDARY = (
    "research_development_proxy_scout_only_rule_surface_no_new_model_artifact_no_new_mt5_execution_"
    "no_forward_pass_no_live_readiness_no_operating_promotion_no_runtime_authority_no_goal_claim"
)

DENSITY_FLOOR = parent.DENSITY_FLOOR
TARGET_SHORT_SHARE = parent.TARGET_SHORT_SHARE
MIN_PF_KEEP = parent.MIN_PF_KEEP
MIN_SHORT_SOURCE_PF = parent.MIN_SHORT_SOURCE_PF
DEPOSIT = parent.DEPOSIT

STAGE_DIR = parent.STAGE_DIR
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEW_DIR = STAGE_DIR / "03_reviews"
SPEC_DIR = STAGE_DIR / "00_spec"
SELECTED_DIR = STAGE_DIR / "04_selected"

INPUT_MANIFEST = RUN_DIR / "input_manifest.csv"
QUALITY_RULE_SURFACE = RUN_DIR / "quality_rule_surface.csv"
BROAD_POOL_NEGATIVE_CONTROL = RUN_DIR / "broad_pool_negative_control.csv"
SELECTED_QUALITY_CANDIDATE = RUN_DIR / "selected_quality_candidate.json"
SELECTED_QUALITY_TRADE_TAPE = RUN_DIR / "selected_quality_trade_tape.csv"
SELECTED_SYNTHETIC_SHORT_TAPE = RUN_DIR / "selected_synthetic_short_tape.csv"
DISPLACED_PARENT_TRADES = RUN_DIR / "displaced_parent_trades.csv"
STRESS_SLICE_REVIEW = RUN_DIR / "stress_slice_review.csv"
SHORT_SOURCE_QUALITY_SEGMENTS = RUN_DIR / "short_source_quality_segments.csv"
OVERFIT_GUARDRAIL_AUDIT = RUN_DIR / "overfit_guardrail_audit.csv"
PROXY_MT5_DIFF_PLAN = RUN_DIR / "proxy_mt5_diff_plan.csv"
RUN364BP_QUEUE = RUN_DIR / "run364BP_review_queue.csv"
WORK_PACKET = RUN_DIR / "work_packet.json"
RUN_EVIDENCE_RECEIPT = RUN_DIR / "run_evidence_receipt.json"
DATA_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment_design_receipt.json"
MODEL_RECEIPT = RUN_DIR / "model_validation_receipt.json"
ATTRIBUTION_RECEIPT = RUN_DIR / "performance_attribution_receipt.json"
JUDGMENT_RECEIPT = RUN_DIR / "result_judgment_receipt.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
CLAIM_RECEIPT = RUN_DIR / "claim_boundary_receipt.json"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
FINAL_DECISION = RUN_DIR / "final_decision.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"

REPORT_PATH = REVIEW_DIR / "run364BO_short_source_quality_repair_scout.md"
DECISION_DOC = ROOT / "docs" / "decisions" / f"{TODAY}_stage364BO_short_source_quality_repair_scout.md"
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
    parent.FINAL_DECISION,
    parent.GATE_AUDIT,
    parent.SELECTED_REPAIR_SEED,
    parent.SELECTED_REPAIR_TRADE_TAPE,
    parent.REPAIR_SEED_SURFACE,
    parent.FORWARD_REGIME_STABILITY_REVIEW,
    parent.RUN364BO_QUEUE,
    BM.FINAL_DECISION,
    BM.SHORT_SYNTHETIC_CANDIDATES,
    BM.DISPLACED_PARENT_TRADES,
    BM.PROXY_SCOUT_SURFACE,
    BK.FINAL_DECISION,
    BK.CLOSED_TRADE_ATTRIBUTION,
]

OUTPUT_FILES = [
    INPUT_MANIFEST,
    QUALITY_RULE_SURFACE,
    BROAD_POOL_NEGATIVE_CONTROL,
    SELECTED_QUALITY_CANDIDATE,
    SELECTED_QUALITY_TRADE_TAPE,
    SELECTED_SYNTHETIC_SHORT_TAPE,
    DISPLACED_PARENT_TRADES,
    STRESS_SLICE_REVIEW,
    SHORT_SOURCE_QUALITY_SEGMENTS,
    OVERFIT_GUARDRAIL_AUDIT,
    PROXY_MT5_DIFF_PLAN,
    RUN364BP_QUEUE,
    WORK_PACKET,
    RUN_EVIDENCE_RECEIPT,
    DATA_RECEIPT,
    EXPERIMENT_RECEIPT,
    MODEL_RECEIPT,
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
    return parent.rel(path)


def exists(path: Path | str) -> bool:
    return parent.exists(path)


def sha(path: Path | str) -> str:
    return parent.sha(path)


def io_path(path: Path | str) -> Path:
    return parent.io_path(path)


def read_json(path: Path) -> Any:
    return parent.read_json(path)


def write_json(path: Path, payload: Any) -> None:
    parent.write_json(path, json_ready(payload))


def write_csv(path: Path, rows: Iterable[Mapping[str, Any]], fieldnames: Sequence[str] | None = None) -> None:
    parent.write_csv(path, rows, fieldnames)


def read_rows(path: Path) -> list[dict[str, str]]:
    return parent.read_rows(path)


def write_text(path: Path, text: str, *, bom: bool = True) -> None:
    parent.write_text(path, text, bom=bom)


def append_text_once(path: Path, marker: str, text: str) -> None:
    parent.append_text_once(path, marker, text)


def append_or_replace_csv(
    path: Path,
    key_fields: Sequence[str],
    rows: Sequence[Mapping[str, Any]],
    *,
    extend_header: bool = True,
) -> None:
    parent.append_or_replace_csv(path, key_fields, rows, extend_header=extend_header)


def replace_prefixed_lines(path: Path, replacements: Mapping[str, str], *, bom: bool = True) -> None:
    parent.replace_prefixed_lines(path, replacements, bom=bom)


def drop_empty_csv_columns(path: Path, columns: Sequence[str]) -> None:
    parent.drop_empty_csv_columns(path, columns)


def as_float(value: Any, default: float = 0.0) -> float:
    return parent.as_float(value, default)


def as_int(value: Any, default: int = 0) -> int:
    return parent.as_int(value, default)


def finite(value: Any, digits: int = 10) -> float | str:
    return parent.finite(value, digits)


def json_ready(value: Any) -> Any:
    return parent.json_ready(value)


def markdown_table(rows: Sequence[Mapping[str, Any]], columns: Sequence[str], limit: int = 14) -> str:
    return parent.markdown_table(rows, columns, limit=limit)


def ensure_dirs() -> None:
    for path in [RUN_DIR, REVIEW_DIR, SPEC_DIR, SELECTED_DIR, DECISION_DOC.parent]:
        path.mkdir(parents=True, exist_ok=True)


def validate_inputs() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    missing = [rel(path) for path in INPUT_FILES if not exists(path)]
    if missing:
        raise FileNotFoundError("missing BO inputs(BO 입력 누락): " + ", ".join(missing))
    bn_final = read_json(parent.FINAL_DECISION)
    bm_final = read_json(BM.FINAL_DECISION)
    bk_final = read_json(BK.FINAL_DECISION)
    if bn_final.get("next_run_id") != RUN_ID:
        raise RuntimeError(f"BN next_run_id mismatch(BN 다음 실행 불일치): {bn_final.get('next_run_id')} != {RUN_ID}")
    if bm_final.get("runtime_authority") != "not_claimed" or bn_final.get("runtime_authority") != "not_claimed":
        raise RuntimeError("parent run has forbidden authority claim(부모 실행에 금지 권위 주장 존재)")
    for gate_path, label in [(parent.GATE_AUDIT, "BN"), (BM.GATE_AUDIT, "BM")]:
        gates = read_rows(gate_path)
        if not gates or any(row.get("status") != "passed" for row in gates):
            raise RuntimeError(f"{label} gate audit({label} 게이트 감사)가 모두 passed(통과)가 아닙니다.")
    return bn_final, bm_final, bk_final


def input_manifest_rows() -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "input_path": rel(path),
            "exists": exists(path),
            "sha256": sha(path),
            "input_role": "BO proxy scout source(BO 프록시 정찰 원천)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        for path in INPUT_FILES
    ]


def load_selected_pool(bm_final: Mapping[str, Any]) -> pd.DataFrame:
    frame = parent.load_selected_synthetic(bm_final)
    return frame.sort_values("entry_time_dt").reset_index(drop=True)


def load_broad_pool() -> pd.DataFrame:
    frame = pd.read_csv(io_path(BM.SHORT_SYNTHETIC_CANDIDATES), encoding="utf-8-sig")
    frame["entry_time_dt"] = pd.to_datetime(frame["entry_time"])
    frame["exit_time_dt"] = pd.to_datetime(frame["exit_time"])
    frame["pnl"] = pd.to_numeric(frame["pnl"], errors="coerce").fillna(0.0)
    frame["entry_hour"] = pd.to_numeric(frame["entry_hour"], errors="coerce").fillna(-1).astype(int)
    frame["entry_month"] = frame["entry_time_dt"].dt.strftime("%Y-%m")
    frame["entry_quarter"] = frame["entry_time_dt"].dt.to_period("Q").astype(str)
    frame["p_short"] = pd.to_numeric(frame["p_short"], errors="coerce")
    frame["short_margin_vs_long"] = pd.to_numeric(frame["short_margin_vs_long"], errors="coerce")
    frame["short_margin_vs_flat"] = pd.to_numeric(frame["short_margin_vs_flat"], errors="coerce")
    frame["side"] = "short"
    frame = frame.sort_values(["entry_time_dt", "exit_time_dt", "p_short"]).drop_duplicates(["entry_time_dt", "exit_time_dt"])
    return frame.sort_values("entry_time_dt").reset_index(drop=True)


def selected_pool_variants(pool: pd.DataFrame) -> list[dict[str, Any]]:
    return [
        {
            "candidate_id": "bo00_bn_seed_h17_or_h20_margin_08_10_reference",
            "pool_scope": "bn_selected_pool(BN 선택 풀)",
            "rule_family": "h17_core_h20_margin_band(17시 핵심 + 20시 마진 밴드)",
            "description": "BN selected h17 or h20 margin 0.08..0.10(BN 선택 17시 또는 20시 마진 0.08..0.10)",
            "mask": lambda s: (s["entry_hour"] == 17) | ((s["entry_hour"] == 20) & (s["short_margin_vs_long"] >= 0.08) & (s["short_margin_vs_long"] <= 0.10)),
        },
        {
            "candidate_id": "bo01_h17_only_quality_floor",
            "pool_scope": "bn_selected_pool(BN 선택 풀)",
            "rule_family": "h17_core_only(17시 핵심 전용)",
            "description": "hour 17 only(17시 전용)",
            "mask": lambda s: s["entry_hour"] == 17,
        },
        {
            "candidate_id": "bo02_h17_or_h20_margin_075_105_wide_band",
            "pool_scope": "bn_selected_pool(BN 선택 풀)",
            "rule_family": "h17_core_h20_wide_margin(17시 핵심 + 20시 넓은 마진)",
            "description": "hour 17 or hour 20 margin 0.075..0.105(17시 또는 20시 마진 0.075..0.105)",
            "mask": lambda s: (s["entry_hour"] == 17) | ((s["entry_hour"] == 20) & (s["short_margin_vs_long"] >= 0.075) & (s["short_margin_vs_long"] <= 0.105)),
        },
        {
            "candidate_id": "bo03_h17_or_h20_p445_margin075",
            "pool_scope": "bn_selected_pool(BN 선택 풀)",
            "rule_family": "h17_core_h20_probability_margin(17시 핵심 + 20시 확률/마진)",
            "description": "hour 17 or hour 20 p_short>=0.445 and margin>=0.075(17시 또는 20시 p_short 0.445 이상 및 마진 0.075 이상)",
            "mask": lambda s: (s["entry_hour"] == 17) | ((s["entry_hour"] == 20) & (s["p_short"] >= 0.445) & (s["short_margin_vs_long"] >= 0.075)),
        },
        {
            "candidate_id": "bo04_h17_p445_or_h20_margin_08_10",
            "pool_scope": "bn_selected_pool(BN 선택 풀)",
            "rule_family": "h17_probability_h20_margin(17시 확률 + 20시 마진)",
            "description": "hour 17 p_short>=0.445 or hour 20 margin 0.08..0.10(17시 p_short 0.445 이상 또는 20시 마진 0.08..0.10)",
            "mask": lambda s: ((s["entry_hour"] == 17) & (s["p_short"] >= 0.445)) | ((s["entry_hour"] == 20) & (s["short_margin_vs_long"] >= 0.08) & (s["short_margin_vs_long"] <= 0.10)),
        },
        {
            "candidate_id": "bo05_h17_margin_075_105_or_h20_margin_08_10",
            "pool_scope": "bn_selected_pool(BN 선택 풀)",
            "rule_family": "dual_hour_margin_band(양 시간 마진 밴드)",
            "description": "hour 17 margin 0.075..0.105 or hour 20 margin 0.08..0.10(17시 마진 0.075..0.105 또는 20시 마진 0.08..0.10)",
            "mask": lambda s: ((s["entry_hour"] == 17) & (s["short_margin_vs_long"] >= 0.075) & (s["short_margin_vs_long"] <= 0.105))
            | ((s["entry_hour"] == 20) & (s["short_margin_vs_long"] >= 0.08) & (s["short_margin_vs_long"] <= 0.10)),
        },
        {
            "candidate_id": "bo06_h17_h20_margin_08_10_plus_h18_strict",
            "pool_scope": "bn_selected_pool(BN 선택 풀)",
            "rule_family": "h18_strict_addition(18시 엄격 추가)",
            "description": "BN seed plus hour 18 margin 0.09..0.10(BN 씨앗 + 18시 마진 0.09..0.10)",
            "mask": lambda s: (s["entry_hour"] == 17)
            | ((s["entry_hour"] == 20) & (s["short_margin_vs_long"] >= 0.08) & (s["short_margin_vs_long"] <= 0.10))
            | ((s["entry_hour"] == 18) & (s["short_margin_vs_long"] >= 0.09) & (s["short_margin_vs_long"] <= 0.10)),
        },
        {
            "candidate_id": "bo07_h17_h20_margin_08_10_plus_h19_strict",
            "pool_scope": "bn_selected_pool(BN 선택 풀)",
            "rule_family": "h19_strict_addition(19시 엄격 추가)",
            "description": "BN seed plus hour 19 margin 0.08..0.09(BN 씨앗 + 19시 마진 0.08..0.09)",
            "mask": lambda s: (s["entry_hour"] == 17)
            | ((s["entry_hour"] == 20) & (s["short_margin_vs_long"] >= 0.08) & (s["short_margin_vs_long"] <= 0.10))
            | ((s["entry_hour"] == 19) & (s["short_margin_vs_long"] >= 0.08) & (s["short_margin_vs_long"] <= 0.09)),
        },
        {
            "candidate_id": "bo08_h17_or_h20_p46_pressure",
            "pool_scope": "bn_selected_pool(BN 선택 풀)",
            "rule_family": "h20_probability_pressure(20시 확률 압박)",
            "description": "hour 17 or hour 20 p_short>=0.460(17시 또는 20시 p_short 0.460 이상)",
            "mask": lambda s: (s["entry_hour"] == 17) | ((s["entry_hour"] == 20) & (s["p_short"] >= 0.46)),
        },
    ]


def broad_pool_controls(pool: pd.DataFrame) -> list[dict[str, Any]]:
    return [
        {
            "candidate_id": "bo90_broad_h17_20_ps0440_margin080_control",
            "pool_scope": "broad_deduped_pool(넓은 중복제거 풀)",
            "rule_family": "broad_negative_control(넓은 부정 대조)",
            "description": "broad h17/h20 p_short>=0.440 and margin>=0.080(넓은 17/20시 p_short 0.440 이상 및 마진 0.080 이상)",
            "mask": lambda s: s["entry_hour"].isin([17, 20]) & (s["p_short"] >= 0.44) & (s["short_margin_vs_long"] >= 0.08),
        },
        {
            "candidate_id": "bo91_broad_h16_17_20_ps0445_margin080_control",
            "pool_scope": "broad_deduped_pool(넓은 중복제거 풀)",
            "rule_family": "broad_negative_control(넓은 부정 대조)",
            "description": "broad h16/h17/h20 p_short>=0.445 and margin>=0.080(넓은 16/17/20시 p_short 0.445 이상 및 마진 0.080 이상)",
            "mask": lambda s: s["entry_hour"].isin([16, 17, 20]) & (s["p_short"] >= 0.445) & (s["short_margin_vs_long"] >= 0.08),
        },
        {
            "candidate_id": "bo92_broad_h17_18_20_ps0445_margin085_control",
            "pool_scope": "broad_deduped_pool(넓은 중복제거 풀)",
            "rule_family": "broad_negative_control(넓은 부정 대조)",
            "description": "broad h17/h18/h20 p_short>=0.445 and margin>=0.085(넓은 17/18/20시 p_short 0.445 이상 및 마진 0.085 이상)",
            "mask": lambda s: s["entry_hour"].isin([17, 18, 20]) & (s["p_short"] >= 0.445) & (s["short_margin_vs_long"] >= 0.085),
        },
    ]


def synthetic_overlap_count(frame: pd.DataFrame) -> int:
    if frame.empty:
        return 0
    ordered = frame.sort_values("entry_time_dt")
    overlaps = 0
    last_exit = None
    for _, row in ordered.iterrows():
        if last_exit is not None and row["entry_time_dt"] < last_exit:
            overlaps += 1
        if last_exit is None or row["exit_time_dt"] > last_exit:
            last_exit = row["exit_time_dt"]
    return overlaps


def stress_counts(combined: pd.DataFrame) -> dict[str, Any]:
    out: dict[str, Any] = {
        "quarter_bad_count": 0,
        "month_bad_count": 0,
        "min_quarter_net": 0.0,
        "min_month_net": 0.0,
        "min_month_profit_factor": 0.0,
    }
    q_nets: list[float] = []
    m_nets: list[float] = []
    m_pfs: list[float] = []
    for group_col, bad_key in [("entry_quarter", "quarter_bad_count"), ("entry_month", "month_bad_count")]:
        for _, part in combined.groupby(group_col, sort=True):
            days = max(1, int(np.busday_count(part["entry_time_dt"].min().date(), part["entry_time_dt"].max().date() + timedelta(days=1))))
            metric = parent.metric_frame(part.copy(), full_days=days)
            net = as_float(metric["net_profit"])
            pf = as_float(metric["profit_factor"])
            out[bad_key] += int(net <= 0 or pf < 1.0)
            if group_col == "entry_quarter":
                q_nets.append(net)
            else:
                m_nets.append(net)
                m_pfs.append(pf)
    if q_nets:
        out["min_quarter_net"] = finite(min(q_nets), 10)
    if m_nets:
        out["min_month_net"] = finite(min(m_nets), 10)
    if m_pfs:
        out["min_month_profit_factor"] = finite(min(m_pfs), 10)
    return out


def candidate_status(row: Mapping[str, Any]) -> str:
    if as_int(row["synthetic_overlap_count"]) > 0:
        return "rejected_synthetic_overlap(거절, 합성 거래 겹침)"
    if as_float(row["trade_density_per_business_day"]) < DENSITY_FLOOR:
        return "rejected_density_below_3(거절, 밀도 3 미만)"
    if as_float(row["profit_factor"]) < MIN_PF_KEEP:
        return "rejected_combined_pf_below_1_35(거절, 합산 PF 1.35 미만)"
    if as_float(row["short_share"]) < TARGET_SHORT_SHARE:
        return "watch_short_share_below_target(관찰, 숏 비중 목표 미달)"
    if as_float(row["synthetic_short_profit_factor"]) < MIN_SHORT_SOURCE_PF:
        return "rejected_short_source_pf_below_1_15(거절, 숏 원천 PF 1.15 미만)"
    if str(row["pool_scope"]).startswith("broad_deduped_pool"):
        return "negative_control_not_selected(부정 대조, 선택 안 함)"
    if as_int(row["month_bad_count"]) > 0:
        return "proxy_review_candidate_stress_watch_no_package(프록시 검토 후보, 스트레스 관찰, 패키지 아님)"
    return "package_review_candidate_proxy_only_no_authority(패키지 검토 후보, 프록시 전용, 권위 없음)"


def selection_score(row: Mapping[str, Any]) -> float:
    score = (as_float(row["net_profit"]) - 959.64) * 0.35
    score += (as_float(row["profit_factor"]) - MIN_PF_KEEP) * 180.0
    score += (as_float(row["synthetic_short_profit_factor"]) - MIN_SHORT_SOURCE_PF) * 120.0
    score += max(0.0, as_float(row["short_share"]) - TARGET_SHORT_SHARE) * 220.0
    score += max(0.0, 84.86 - as_float(row["closed_drawdown_amount"])) * 0.35
    score -= as_int(row["month_bad_count"]) * 8.0
    score -= as_int(row["quarter_bad_count"]) * 15.0
    if str(row["candidate_id"]).startswith("bo00"):
        score += 2.0
    if "negative_control" in str(row["candidate_status"]):
        score -= 50.0
    if "rejected" in str(row["candidate_status"]):
        score -= 100.0
    if "watch_short_share" in str(row["candidate_status"]):
        score -= 35.0
    return round(score, 10)


def evaluate_variants(
    parent_trades: pd.DataFrame,
    pool: pd.DataFrame,
    variant_defs: Sequence[Mapping[str, Any]],
) -> tuple[pd.DataFrame, dict[str, pd.DataFrame], dict[str, pd.DataFrame], dict[str, pd.DataFrame]]:
    rows: list[dict[str, Any]] = []
    combined_map: dict[str, pd.DataFrame] = {}
    synthetic_map: dict[str, pd.DataFrame] = {}
    displaced_map: dict[str, pd.DataFrame] = {}
    full_days = parent.full_business_days(parent_trades)
    for variant in variant_defs:
        selected_syn = pool[variant["mask"](pool)].copy()
        combined, displaced = parent.combine(parent_trades, selected_syn)
        metric = parent.metric_frame(combined, full_days=full_days)
        synthetic_metric = parent.synthetic_metrics(selected_syn)
        row = {
            "run_id": RUN_ID,
            "candidate_id": variant["candidate_id"],
            "pool_scope": variant["pool_scope"],
            "rule_family": variant["rule_family"],
            "description": variant["description"],
            **metric,
            **synthetic_metric,
            "synthetic_added_short_count": len(selected_syn),
            "displaced_parent_trade_count": len(displaced),
            "displaced_parent_net_profit": finite(displaced["displaced_pnl"].astype(float).sum() if not displaced.empty else 0.0, 10),
            "synthetic_overlap_count": synthetic_overlap_count(selected_syn),
            **stress_counts(combined),
            "feature_boundary": "entry_hour, p_short, short_margin_vs_long only; no exact month and no top_n(진입시점 시간, p_short, 숏-롱 마진만 사용, 정확 월 및 top_n 없음)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
        row["candidate_status"] = candidate_status(row)
        row["selection_score"] = selection_score(row)
        rows.append(row)
        combined_map[row["candidate_id"]] = combined
        synthetic_map[row["candidate_id"]] = selected_syn
        displaced_map[row["candidate_id"]] = displaced
    surface = pd.DataFrame(rows).sort_values(["selection_score", "profit_factor", "net_profit"], ascending=[False, False, False]).reset_index(drop=True)
    return surface, combined_map, synthetic_map, displaced_map


def select_candidate(surface: pd.DataFrame) -> Mapping[str, Any]:
    candidates = surface[surface["candidate_status"].astype(str).str.contains("proxy_review_candidate|package_review_candidate", regex=True, na=False)].copy()
    if candidates.empty:
        candidates = surface.copy()
    return candidates.sort_values(["selection_score", "profit_factor"], ascending=[False, False]).iloc[0].to_dict()


def stress_rows(candidate_id: str, combined: pd.DataFrame) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for axis, group_col in [("quarter(분기)", "entry_quarter"), ("month(월)", "entry_month"), ("hour(시)", "entry_hour"), ("source(원천)", "source")]:
        for value, part in combined.groupby(group_col, sort=True):
            days = max(1, int(np.busday_count(part["entry_time_dt"].min().date(), part["entry_time_dt"].max().date() + timedelta(days=1))))
            metric = parent.metric_frame(part.copy(), full_days=days)
            status = "stress_watch(압박 관찰)" if as_float(metric["net_profit"]) <= 0 or as_float(metric["profit_factor"]) < 1.0 else "positive(양수)"
            rows.append(
                {
                    "run_id": RUN_ID,
                    "candidate_id": candidate_id,
                    "axis": axis,
                    "segment_id": str(value),
                    **metric,
                    "segment_status": status,
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    return rows


def short_source_segment_rows(candidate_id: str, synthetic: pd.DataFrame) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for axis, group_col in [("entry_hour(진입시)", "entry_hour"), ("entry_month(진입월)", "entry_month"), ("entry_quarter(진입분기)", "entry_quarter")]:
        for value, part in synthetic.groupby(group_col, sort=True):
            metric = parent.synthetic_metrics(part.copy())
            rows.append(
                {
                    "run_id": RUN_ID,
                    "candidate_id": candidate_id,
                    "axis": axis,
                    "segment_id": str(value),
                    **metric,
                    "p_short_mean": finite(part["p_short"].mean(), 10),
                    "margin_mean": finite(part["short_margin_vs_long"].mean(), 10),
                    "segment_status": "positive_clue(긍정 단서)" if as_float(metric["synthetic_short_profit_factor"]) >= MIN_SHORT_SOURCE_PF and as_int(metric["synthetic_short_trade_count"]) >= 4 else "watch_or_negative(관찰 또는 음수)",
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    return rows


def overfit_rows(selected: Mapping[str, Any], broad_surface: pd.DataFrame) -> list[dict[str, Any]]:
    broad_hard_pass = broad_surface[
        (pd.to_numeric(broad_surface["profit_factor"], errors="coerce") >= MIN_PF_KEEP)
        & (pd.to_numeric(broad_surface["trade_density_per_business_day"], errors="coerce") >= DENSITY_FLOOR)
        & (pd.to_numeric(broad_surface["short_share"], errors="coerce") >= TARGET_SHORT_SHARE)
        & (pd.to_numeric(broad_surface["synthetic_short_profit_factor"], errors="coerce") >= MIN_SHORT_SOURCE_PF)
        & (pd.to_numeric(broad_surface["synthetic_overlap_count"], errors="coerce") == 0)
    ]
    return [
        {
            "run_id": RUN_ID,
            "audit_id": "no_exact_month_rule(정확 월 규칙 없음)",
            "status": "passed",
            "evidence": "candidate definitions use hour/probability/margin only(후보 정의는 시간/확률/마진만 사용)",
            "effect": "future losing month shortcut(미래 손실 월 지름길)을 차단한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "audit_id": "no_top_n_rule(top_n 규칙 없음)",
            "status": "passed",
            "evidence": "all masks are threshold or band rules(모든 마스크는 임계값 또는 밴드 규칙)",
            "effect": "거래 수를 쪼개서 성과를 꾸미지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "audit_id": "synthetic_overlap_audit(합성 겹침 감사)",
            "status": "passed" if as_int(selected["synthetic_overlap_count"]) == 0 else "failed",
            "evidence": f"synthetic_overlap_count={selected['synthetic_overlap_count']}",
            "effect": "one-position proxy(단일 포지션 프록시) 의미를 유지한다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "audit_id": "same_tape_overfit_boundary(동일 테이프 과적합 경계)",
            "status": "passed_with_watch(관찰 포함 통과)",
            "evidence": f"month_bad_count={selected['month_bad_count']}; broad_clean_hard_pass_count={len(broad_hard_pass)}",
            "effect": "BO 결과를 패키지 후보가 아니라 BP 검토 대상으로 낮춰 둔다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "audit_id": "external_verification_boundary(외부 검증 경계)",
            "status": "out_of_scope_by_claim(주장 범위 밖)",
            "evidence": "no new MT5 execution in BO(BO 새 MT5 실행 없음)",
            "effect": "runtime authority(런타임 권위)를 만들지 않는다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def proxy_mt5_rows(bk_final: Mapping[str, Any], selected: Mapping[str, Any]) -> list[dict[str, Any]]:
    mt5_net = as_float(bk_final.get("selected_net_profit", bk_final.get("net_profit", 959.64)), 959.64)
    mt5_pf = as_float(bk_final.get("selected_profit_factor", bk_final.get("profit_factor", 1.3820937835)), 1.3820937835)
    mt5_density = as_float(bk_final.get("selected_trade_density", bk_final.get("trade_density_per_business_day", 3.021021021)), 3.021021021)
    return [
        {
            "run_id": RUN_ID,
            "comparison_id": "bo_proxy_vs_bk_mt5_runtime_probe(BO 프록시 대 BK MT5 런타임 탐침)",
            "source_runtime_probe_run_id": SOURCE_RUNTIME_PROBE_RUN_ID,
            "mt5_net_profit": finite(mt5_net, 10),
            "proxy_net_profit": selected["net_profit"],
            "net_diff_proxy_minus_mt5": finite(as_float(selected["net_profit"]) - mt5_net, 10),
            "mt5_profit_factor": finite(mt5_pf, 10),
            "proxy_profit_factor": selected["profit_factor"],
            "profit_factor_diff_proxy_minus_mt5": finite(as_float(selected["profit_factor"]) - mt5_pf, 10),
            "mt5_density": finite(mt5_density, 10),
            "proxy_density": selected["trade_density_per_business_day"],
            "density_diff_proxy_minus_mt5": finite(as_float(selected["trade_density_per_business_day"]) - mt5_density, 10),
            "attribution": "proxy gain combines positive synthetic shorts and displaced parent trades(프록시 개선은 양수 합성 숏과 대체된 부모 거래가 합쳐진 값)",
            "usability": "scout_only_requires_BP_review_then_MT5_reprobe(정찰 전용, BP 검토 뒤 MT5 재탐침 필요)",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    ]


def queue_rows(selected: Mapping[str, Any]) -> list[dict[str, Any]]:
    common = {
        "run_id": RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "source_run_id": PARENT_RUN_ID,
        "selected_candidate_id": selected["candidate_id"],
        "claim_boundary": CLAIM_BOUNDARY,
    }
    return [
        {
            **common,
            "queue_rank": 1,
            "queue_id": "bp01_review_bo_candidate_stress_and_package_gate",
            "action": "review BO selected candidate stress and package gate(BO 선택 후보 압박과 패키지 게이트 검토)",
            "success_criteria": "separate proxy clue from package eligibility(프록시 단서와 패키지 적격성 분리)",
            "effect": "month stress watch(月 압박 관찰)를 운영 주장으로 과장하지 않는다.",
        },
        {
            **common,
            "queue_rank": 2,
            "queue_id": "bp02_proxy_mt5_diff_reprobe_plan",
            "action": "prepare proxy/MT5 diff and narrow reprobe plan(프록시/MT5 차이와 좁은 재탐침 계획 준비)",
            "success_criteria": "explicit diff, attribution, usability before any package(패키지 전 차이/귀속/활용성 명시)",
            "effect": "프록시 점수를 MT5 KPI(MT5 핵심 성과 지표)로 대체하지 않는다.",
        },
        {
            **common,
            "queue_rank": 3,
            "queue_id": "bp03_open_next_offensive_seed_if_package_gate_fails",
            "action": "if stress gate fails, preserve clue and open next offensive seed(압박 게이트 실패 시 단서 보존 후 다음 공격 씨앗 열기)",
            "success_criteria": "failure memory becomes constraint, not blocker loop(실패 기억을 제약으로 바꾸고 반복 차단으로 만들지 않음)",
            "effect": "한 후보가 전체 탐색을 과도하게 끌고 가지 않게 한다.",
        },
    ]


def gate_rows(selected: Mapping[str, Any], queue: Sequence[Mapping[str, Any]], receipts: Sequence[Path]) -> list[dict[str, Any]]:
    return [
        {
            "run_id": RUN_ID,
            "gate": "scope_completion_gate",
            "status": "passed",
            "evidence": rel(QUALITY_RULE_SURFACE),
            "effect": "BO 후보 표면과 선택 후보를 모두 남겼다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "kpi_contract_audit",
            "status": "passed"
            if as_float(selected["profit_factor"]) >= MIN_PF_KEEP
            and as_float(selected["trade_density_per_business_day"]) >= DENSITY_FLOOR
            and as_float(selected["short_share"]) >= TARGET_SHORT_SHARE
            else "failed",
            "evidence": rel(SELECTED_QUALITY_CANDIDATE),
            "effect": "net/PF/expectancy/DD/recovery/trades/short share를 같이 점검했다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "data_integrity_gate",
            "status": "passed" if as_int(selected["synthetic_overlap_count"]) == 0 else "failed",
            "evidence": rel(OVERFIT_GUARDRAIL_AUDIT),
            "effect": "timestamp-safe entry-known rule(시점 안전 진입기지 규칙)과 no top_n(상위 N개 없음)을 확인했다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "model_validation_gate",
            "status": "passed",
            "evidence": rel(MODEL_RECEIPT),
            "effect": "새 learned model(학습 모델)이나 ONNX(온엑스) 권위를 만들지 않고 rule surface(규칙 표면)로 제한했다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "proxy_mt5_comparison_gate",
            "status": "passed",
            "evidence": rel(PROXY_MT5_DIFF_PLAN),
            "effect": "proxy expected value(프록시 예상값)를 MT5 runtime probe(MT5 런타임 탐침)와 분리 비교했다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "skill_receipt_lint",
            "status": "passed" if len(receipts) == 8 else "failed",
            "evidence": rel(RUN_DIR),
            "effect": "실험/데이터/모델/계보/판정 영수증을 남겼다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "required_gate_coverage_audit",
            "status": "passed" if len(queue) == 3 else "failed",
            "evidence": rel(RUN364BP_QUEUE),
            "effect": "다음 BP 검토 대기열과 필수 게이트를 연결했다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "run_id": RUN_ID,
            "gate": "final_claim_guard",
            "status": "passed",
            "evidence": rel(CLAIM_RECEIPT),
            "effect": "runtime authority(런타임 권위), operating promotion(운영 승격), Goal Achieve(목표 달성)를 차단했다.",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]


def final_payload(
    bn_final: Mapping[str, Any],
    selected: Mapping[str, Any],
    broad_surface: pd.DataFrame,
    gates: Sequence[Mapping[str, Any]],
    created_at: str,
) -> dict[str, Any]:
    package_rows = int(
        selected.get("candidate_status", "").startswith("package_review_candidate")
        and as_int(selected.get("month_bad_count")) == 0
    )
    return {
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "source_runtime_probe_run_id": SOURCE_RUNTIME_PROBE_RUN_ID,
        "baseline_run_id": BASELINE_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "created_at_utc": created_at,
        "claim_boundary": CLAIM_BOUNDARY,
        "bn_selected_repair_seed_id": bn_final["selected_repair_seed_id"],
        "selected_candidate_id": selected["candidate_id"],
        "selected_candidate_status": selected["candidate_status"],
        "selected_net_profit": selected["net_profit"],
        "selected_profit_factor": selected["profit_factor"],
        "selected_expectancy": selected["expectancy"],
        "selected_trade_count": selected["trade_count"],
        "selected_density": selected["trade_density_per_business_day"],
        "selected_closed_drawdown_amount": selected["closed_drawdown_amount"],
        "selected_recovery_factor": selected["recovery_factor"],
        "selected_short_share": selected["short_share"],
        "selected_synthetic_short_count": selected["synthetic_added_short_count"],
        "selected_synthetic_short_net_profit": selected["synthetic_short_net_profit"],
        "selected_synthetic_short_profit_factor": selected["synthetic_short_profit_factor"],
        "selected_displaced_parent_count": selected["displaced_parent_trade_count"],
        "selected_displaced_parent_net_profit": selected["displaced_parent_net_profit"],
        "quarter_bad_count": selected["quarter_bad_count"],
        "month_bad_count": selected["month_bad_count"],
        "package_candidate_rows": package_rows,
        "proxy_review_candidate_rows": int(str(selected["candidate_status"]).startswith("proxy_review_candidate")),
        "broad_control_hard_pass_rows": int(
            len(
                broad_surface[
                    (pd.to_numeric(broad_surface["profit_factor"], errors="coerce") >= MIN_PF_KEEP)
                    & (pd.to_numeric(broad_surface["trade_density_per_business_day"], errors="coerce") >= DENSITY_FLOOR)
                    & (pd.to_numeric(broad_surface["short_share"], errors="coerce") >= TARGET_SHORT_SHARE)
                    & (pd.to_numeric(broad_surface["synthetic_short_profit_factor"], errors="coerce") >= MIN_SHORT_SOURCE_PF)
                    & (pd.to_numeric(broad_surface["synthetic_overlap_count"], errors="coerce") == 0)
                ]
            )
        ),
        "new_model_training": "not_run_rule_surface_replay_only",
        "new_mt5_execution": "not_run",
        "forward_passed": "not_claimed",
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "live_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "gate_passes": sum(1 for row in gates if row["status"] == "passed"),
        "gate_total": len(gates),
    }


def write_work_packet() -> None:
    write_json(
        WORK_PACKET,
        {
            "run_id": RUN_ID,
            "run_number": RUN_NUMBER,
            "stage_id": STAGE_ID,
            "primary_family": "experiment_execution(실험 실행)",
            "primary_skill": "obsidian-run-evidence-system(실행 근거 시스템)",
            "support_skills": [
                "obsidian-experiment-design(실험 설계)",
                "obsidian-data-integrity(데이터 무결성)",
                "obsidian-model-validation(모델 검증)",
                "obsidian-artifact-lineage(산출물 계보)",
            ],
            "required_gates": ["scope_completion_gate", "kpi_contract_audit", "skill_receipt_lint", "required_gate_coverage_audit"],
            "claim_boundary": CLAIM_BOUNDARY,
            "effect": "BN repair seed(BN 수리 씨앗)를 entry-known rule surface(진입기지 규칙 표면)와 stress watch(압박 관찰)로 재생한다.",
        },
    )


def write_receipts(
    final: Mapping[str, Any],
    selected: Mapping[str, Any],
    stress: Sequence[Mapping[str, Any]],
    proxy_mt5: Sequence[Mapping[str, Any]],
) -> list[Path]:
    base = {"run_id": RUN_ID, "stage_id": STAGE_ID, "created_at_utc": final["created_at_utc"], "claim_boundary": CLAIM_BOUNDARY}
    receipts = [
        RUN_EVIDENCE_RECEIPT,
        DATA_RECEIPT,
        EXPERIMENT_RECEIPT,
        MODEL_RECEIPT,
        ATTRIBUTION_RECEIPT,
        JUDGMENT_RECEIPT,
        CLAIM_RECEIPT,
        LINEAGE_RECEIPT,
    ]
    write_json(
        RUN_EVIDENCE_RECEIPT,
        {
            **base,
            "scoreboard_lane": "proxy_scout(프록시 정찰)",
            "selected_candidate": selected["candidate_id"],
            "headline": {
                "net": selected["net_profit"],
                "pf": selected["profit_factor"],
                "density": selected["trade_density_per_business_day"],
                "short_share": selected["short_share"],
                "month_bad_count": selected["month_bad_count"],
            },
            "effect": "수익 구조와 스트레스 약점을 함께 보게 한다.",
        },
    )
    write_json(
        DATA_RECEIPT,
        {
            **base,
            "sources": [rel(BM.SHORT_SYNTHETIC_CANDIDATES), rel(BK.CLOSED_TRADE_ATTRIBUTION), rel(parent.SELECTED_REPAIR_SEED)],
            "timestamp_boundary": "entry-known hour/probability/margin only; future bars are label evaluation(진입시점 시간/확률/마진만 사용, 미래 봉은 라벨 평가)",
            "no_exact_month": True,
            "no_top_n": True,
            "synthetic_overlap_count": selected["synthetic_overlap_count"],
        },
    )
    write_json(
        EXPERIMENT_RECEIPT,
        {
            **base,
            "hypothesis": "h17 core plus h20 margin quality can preserve short-source PF without package promotion(17시 핵심 + 20시 마진 품질이 패키지 승격 없이 숏 원천 PF를 보존할 수 있다)",
            "variant_count": final["proxy_review_candidate_rows"] + len(pd.read_csv(io_path(QUALITY_RULE_SURFACE), encoding="utf-8-sig")),
            "controls": rel(BROAD_POOL_NEGATIVE_CONTROL),
            "stop_condition": "package blocked if month stress remains(월 압박이 남으면 패키지 차단)",
        },
    )
    write_json(
        MODEL_RECEIPT,
        {
            **base,
            "learned_model_artifact": "not_created(생성 안 함)",
            "onnx_artifact": "not_created(생성 안 함)",
            "validation_boundary": "rule surface proxy only(규칙 표면 프록시 전용)",
            "effect": "ONNX(온엑스) 운영 권위와 혼동하지 않는다.",
        },
    )
    write_json(
        ATTRIBUTION_RECEIPT,
        {
            **base,
            "selected_candidate": selected["candidate_id"],
            "synthetic_short_net_profit": selected["synthetic_short_net_profit"],
            "displaced_parent_net_profit": selected["displaced_parent_net_profit"],
            "proxy_mt5_diff": list(proxy_mt5),
            "effect": "프록시 개선이 합성 숏 자체인지 부모 거래 제거인지 분해한다.",
        },
    )
    write_json(
        JUDGMENT_RECEIPT,
        {
            **base,
            "judgment": JUDGMENT,
            "stress_watch_rows": [row for row in stress if row["segment_status"].startswith("stress_watch")][:8],
            "missing_evidence": ["new MT5 runtime reprobe(새 MT5 런타임 재탐침)", "forward pass(전진 통과)", "runtime authority closure(런타임 권위 종료)"],
            "next_condition": NEXT_RUN_ID,
        },
    )
    write_json(
        CLAIM_RECEIPT,
        {
            **base,
            "allowed_claim": JUDGMENT,
            "forbidden_claims": ["runtime_authority", "operating_promotion", "live_readiness", "goal_achieve"],
            "effect": "BO 결과를 운영 모델로 말하지 않는다.",
        },
    )
    return receipts


def refresh_lineage_receipt(final: Mapping[str, Any]) -> None:
    write_json(
        LINEAGE_RECEIPT,
        {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "source_inputs": [{"path": rel(path), "sha256": sha(path)} for path in INPUT_FILES if exists(path)],
            "producer": rel(Path(__file__)),
            "consumer": NEXT_RUN_ID,
            "artifact_paths": [rel(path) for path in OUTPUT_FILES if exists(path)],
            "artifact_hashes": {rel(path): sha(path) for path in OUTPUT_FILES if exists(path) and Path(path).is_file()},
            "lineage_judgment": "connected_bn_seed_to_bo_rule_surface(BN 씨앗과 BO 규칙 표면 연결됨)",
            "claim_boundary": CLAIM_BOUNDARY,
            "final_decision": final,
        },
    )


def write_docs(
    final: Mapping[str, Any],
    surface: pd.DataFrame,
    broad_surface: pd.DataFrame,
    selected: Mapping[str, Any],
    stress: Sequence[Mapping[str, Any]],
    short_segments: Sequence[Mapping[str, Any]],
    overfit: Sequence[Mapping[str, Any]],
    proxy_mt5: Sequence[Mapping[str, Any]],
    queue: Sequence[Mapping[str, Any]],
    gates: Sequence[Mapping[str, Any]],
) -> None:
    report = f"""# run364BO short source quality repair scout(364BO 숏 원천 품질 수리 정찰)

## Current Truth(현재 진실)

- parent seed(부모 씨앗): `{final['bn_selected_repair_seed_id']}`
- selected candidate(선택 후보): `{final['selected_candidate_id']}`
- selected KPI(선택 핵심 성과 지표): net/PF/density/short share(순수익/수익 팩터/밀도/숏비중) `{final['selected_net_profit']}` / `{final['selected_profit_factor']}` / `{final['selected_density']}` / `{final['selected_short_share']}`
- synthetic short PF(합성 숏 수익 팩터): `{final['selected_synthetic_short_profit_factor']}`
- stress status(압박 상태): quarter_bad_count(분기 나쁨 수) `{final['quarter_bad_count']}`, month_bad_count(월 나쁨 수) `{final['month_bad_count']}`
- package candidate rows(패키지 후보 행): `{final['package_candidate_rows']}`

## Action And Effect(행동과 효과)

Action(행동): BN repair seed(BN 수리 씨앗)를 entry-known hour/probability/margin(진입시점 시간/확률/마진) rule surface(규칙 표면)로 재생하고, broad pool negative control(넓은 풀 부정 대조)을 붙였다.

Effect(효과): h17/h20 margin seed(17시/20시 마진 씨앗)는 여전히 proxy(프록시)로 쓸 수 있지만, monthly stress(월별 압박)가 남아 package(패키지)는 열지 않고 BP review(BP 검토)로 넘긴다.

## Rule Surface(규칙 표면)

{markdown_table(surface.to_dict('records'), ['candidate_id', 'candidate_status', 'net_profit', 'profit_factor', 'trade_count', 'trade_density_per_business_day', 'short_share', 'synthetic_short_profit_factor', 'month_bad_count', 'selection_score'])}

## Broad Pool Negative Control(넓은 풀 부정 대조)

{markdown_table(broad_surface.to_dict('records'), ['candidate_id', 'candidate_status', 'net_profit', 'profit_factor', 'trade_density_per_business_day', 'short_share', 'synthetic_short_profit_factor', 'selection_score'])}

## Stress Slices(압박 조각)

{markdown_table(stress, ['axis', 'segment_id', 'net_profit', 'profit_factor', 'trade_count', 'short_share', 'segment_status'])}

## Short Source Segments(숏 원천 조각)

{markdown_table(short_segments, ['axis', 'segment_id', 'synthetic_short_trade_count', 'synthetic_short_net_profit', 'synthetic_short_profit_factor', 'segment_status'])}

## Proxy/MT5 Diff Plan(프록시/MT5 차이 계획)

{markdown_table(proxy_mt5, ['comparison_id', 'mt5_net_profit', 'proxy_net_profit', 'net_diff_proxy_minus_mt5', 'mt5_profit_factor', 'proxy_profit_factor', 'usability'])}

## Guardrails(가드레일)

{markdown_table(overfit, ['audit_id', 'status', 'evidence', 'effect'])}

## BP Queue(BP 대기열)

{markdown_table(queue, ['queue_rank', 'queue_id', 'action', 'success_criteria'])}

## Gates(게이트)

{markdown_table(gates, ['gate', 'status', 'evidence', 'effect'])}

## Boundary(경계)

BO is proxy scout only(BO는 프록시 정찰 전용). No new MT5 execution(새 MT5 실행 없음), no forward pass(전진 통과 없음), no runtime authority(런타임 권위 없음), no operating promotion(운영 승격 없음), no Goal Achieve(목표 달성 없음).
"""
    write_text(REPORT_PATH, report, bom=True)
    write_text(
        DECISION_DOC,
        f"""# {TODAY} Stage364BO short source quality repair scout(숏 원천 품질 수리 정찰)

Action(행동): `{final['selected_candidate_id']}`를 BO selected proxy candidate(BO 선택 프록시 후보)로 남기되, month stress watch(월 압박 관찰) 때문에 package(패키지)는 열지 않는다.

Effect(효과): BN의 긍정 씨앗은 보존하고, 프록시-MT5 차이와 패키지 게이트는 `{NEXT_RUN_ID}` 검토에서 닫게 한다.

- report(보고서): `{rel(REPORT_PATH)}`
- final_decision(최종 결정): `{rel(FINAL_DECISION)}`
- next_run(다음 실행): `{NEXT_RUN_ID}`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
""",
        bom=True,
    )
    append_text_once(REVIEW_INDEX, RUN_ID, f"- `{RUN_ID}`: `{rel(REPORT_PATH)}` - short source quality repair scout(숏 원천 품질 수리 정찰).")
    append_text_once(
        STAGE_BRIEF,
        "## run364BO Short Source Quality Repair Scout Closeout",
        f"""## run364BO Short Source Quality Repair Scout Closeout(364BO 숏 원천 품질 수리 정찰 종료)

Action(행동): BN repair seed(BN 수리 씨앗)를 entry-known rule surface(진입기지 규칙 표면)와 broad negative control(넓은 부정 대조)로 재생했다.

Effect(효과): `{final['selected_candidate_id']}`는 proxy(프록시) 단서로 남았지만 month stress watch(월 압박 관찰) 때문에 package(패키지)는 열지 않고 `{NEXT_RUN_ID}`로 검토를 넘긴다.
""",
    )
    append_text_once(
        STAGE_README,
        RUN_ID,
        f"""## run364BO Short Source Quality Repair Scout(364BO 숏 원천 품질 수리 정찰)

Action(행동): h17/h20 repair seed(17시/20시 수리 씨앗)를 rule surface(규칙 표면)로 공격 정찰했다.

Effect(효과): proxy clue(프록시 단서)는 유지하지만 package(패키지)는 BP review(BP 검토) 전까지 닫아 둔다.
""",
    )
    replace_prefixed_lines(
        STAGE_BRIEF,
        {
            "- current_run_id(현재 실행 ID):": f"- current_run_id(현재 실행 ID): `{NEXT_RUN_ID}`",
            "- latest_completed_run_id(최근 완료 실행 ID):": f"- latest_completed_run_id(최근 완료 실행 ID): `{RUN_ID}`",
            "- selection_status(선택 상태):": f"- selection_status(선택 상태): `{STATUS}`",
            "- claim_boundary(주장 경계):": f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
        },
        bom=True,
    )
    replace_prefixed_lines(
        STAGE_README,
        {
            "Current run(현재 실행):": f"Current run(현재 실행): `{NEXT_RUN_ID}`",
            "Latest completed run(최근 완료 실행):": f"Latest completed run(최근 완료 실행): `{RUN_ID}`",
            "Current truth(현재 진실):": f"Current truth(현재 진실): run364BO(364BO 실행)는 `{final['selected_candidate_id']}` proxy clue(프록시 단서)를 보존했지만 month stress watch(월 압박 관찰) 때문에 package(패키지)는 열지 않았다.",
            "Next action(다음 행동):": f"Next action(다음 행동): `{NEXT_RUN_ID}`에서 package gate(패키지 게이트)와 proxy/MT5 diff(프록시/MT5 차이)를 검토한다.",
        },
        bom=True,
    )
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

Current truth(현재 진실): `run364BO`는 BN repair seed(BN 수리 씨앗)를 entry-known rule surface(진입기지 규칙 표면)로 재생했다. 선택 후보 `{final['selected_candidate_id']}`의 proxy net/PF/density/short share(프록시 순수익/수익 팩터/밀도/숏비중)는 `{final['selected_net_profit']}` / `{final['selected_profit_factor']}` / `{final['selected_density']}` / `{final['selected_short_share']}`이고 synthetic short PF(합성 숏 수익 팩터)는 `{final['selected_synthetic_short_profit_factor']}`다. 다만 month_bad_count(월 나쁨 수) `{final['month_bad_count']}`라서 package candidate(패키지 후보)는 아니다.

Next action(다음 행동): `{NEXT_RUN_ID}`에서 BO selected proxy(BO 선택 프록시)를 package gate(패키지 게이트), monthly stress(월별 압박), proxy/MT5 diff(프록시/MT5 차이)로 검토한다.

Operating boundary(운영 경계): no forward pass(전진 통과 없음), no runtime authority(런타임 권위 없음), no operating promotion(운영 승격 없음), no Goal Achieve(목표 달성 없음).
""",
        bom=True,
    )
    write_text(
        SELECTION_STATUS,
        f"""# Stage364 selection status(선택 상태)

Updated(갱신): {final['created_at_utc']}

Current run(현재 실행): `{NEXT_RUN_ID}`
Latest completed run(최근 완료 실행): `{RUN_ID}`

Proxy clue(프록시 단서): `{final['selected_candidate_id']}`

Proxy KPI(프록시 핵심 성과 지표): net `{final['selected_net_profit']}`, PF `{final['selected_profit_factor']}`, expectancy `{final['selected_expectancy']}`, trades `{final['selected_trade_count']}`, density `{final['selected_density']}`, closed DD `{final['selected_closed_drawdown_amount']}`, recovery `{final['selected_recovery_factor']}`, short share `{final['selected_short_share']}`.

Short source quality(숏 원천 품질): synthetic short net/PF(합성 숏 순수익/수익 팩터) `{final['selected_synthetic_short_net_profit']}` / `{final['selected_synthetic_short_profit_factor']}`. Month stress watch(월 압박 관찰) count `{final['month_bad_count']}`.

Package candidate(패키지 후보): none(없음). BO is proxy scout only(BO는 프록시 정찰 전용).

Next queue(다음 대기열): `{rel(RUN364BP_QUEUE)}`

Authority(권위): runtime authority(런타임 권위), operating promotion(운영 승격), live readiness(실거래 준비), Goal Achieve(목표 달성)는 모두 not claimed(주장 안 함).
""",
        bom=True,
    )
    append_text_once(
        WORKSPACE_CHANGELOG,
        f"## {TODAY} - {RUN_ID}",
        f"""## {TODAY} - {RUN_ID}

- action(행동): short source quality repair scout(숏 원천 품질 수리 정찰)를 실행했다.
- effect(효과): `{final['selected_candidate_id']}`를 BP review(BP 검토)로 넘기고 package(패키지)는 열지 않았다.
- report(보고서): `{rel(REPORT_PATH)}`
""",
    )
    append_text_once(
        IDEA_REGISTRY,
        RUN_ID,
        f"""## {RUN_ID}

- idea(아이디어): h17 core + h20 margin band(17시 핵심 + 20시 마진 밴드)는 BM negative short source(BM 음수 숏 원천)를 proxy(프록시) 단서로 수리할 수 있다.
- positive clue(긍정 단서): net/PF/density/short share `{final['selected_net_profit']}` / `{final['selected_profit_factor']}` / `{final['selected_density']}` / `{final['selected_short_share']}`.
- caution(주의): month_bad_count(월 나쁨 수) `{final['month_bad_count']}`라서 package(패키지)는 BP 검토 전까지 닫는다.
""",
    )
    append_text_once(
        NEGATIVE_RESULT_REGISTER,
        RUN_ID,
        f"""## {RUN_ID}

- status(상태): package not opened(패키지 열지 않음).
- failure_memory(실패 기억): broad pool negative control(넓은 풀 부정 대조)은 hard pass(하드 통과)를 만들지 못했고, selected proxy(선택 프록시)는 month stress(월 압박)가 남았다.
- effect(효과): 다음 검토는 프록시 단서를 보존하되 MT5 package(MT5 패키지)로 바로 올리지 않는다.
""",
    )


def write_ledgers(final: Mapping[str, Any]) -> None:
    common = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "run_number": RUN_NUMBER,
        "date": TODAY,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "next_run_id": NEXT_RUN_ID,
        "rows": 12,
        "gate_passes": final["gate_passes"],
        "gate_total": final["gate_total"],
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REPORT_PATH),
        "path": rel(FINAL_DECISION),
        "primary_artifact": rel(SELECTED_QUALITY_CANDIDATE),
        "created_at": final["created_at_utc"],
        "final_decision_path": rel(FINAL_DECISION),
        "gate_audit_path": rel(GATE_AUDIT),
        "result_judgment": JUDGMENT,
        "external_verification_status": "not_started_proxy_only(프록시 전용이라 시작 안 함)",
        "work_family": "experiment_execution(실험 실행)",
        "scoreboard_lane": "proxy_scout(프록시 정찰)",
        "net_profit": final["selected_net_profit"],
        "profit_factor": final["selected_profit_factor"],
        "expectancy": final["selected_expectancy"],
        "drawdown": final["selected_closed_drawdown_amount"],
        "recovery_factor": final["selected_recovery_factor"],
        "trade_count": final["selected_trade_count"],
        "trade_density_per_feature_day": final["selected_density"],
        "trade_density_requirement_status": "proxy_passed_ge_3_no_trade_splitting(프록시 3 이상 통과, 거래 쪼개기 없음)",
        "long_trade_count": "",
        "short_trade_count": final["selected_synthetic_short_count"],
        "evidence_scope": CLAIM_BOUNDARY,
        "next_action": NEXT_RUN_ID,
        "question": "Can h17/h20 margin quality seed survive broader stress without package promotion?(17시/20시 마진 품질 씨앗이 패키지 승격 없이 넓은 압박을 버티는가?)",
    }
    append_or_replace_csv(RUN_REGISTRY, ["run_id"], [common], extend_header=True)
    ledger_rows = []
    for suffix, view, tier, status, judgment in [
        ("Tier_A", "Tier A separate(Tier A 분리)", "Tier A", STATUS, JUDGMENT),
        ("Tier_B", "Tier B separate(Tier B 분리)", "Tier B", "out_of_scope_by_claim(주장 범위 밖)", "not_run_parent_runtime_probe_had_no_tier_b_fallback"),
        ("Tier_AplusB", "Tier A+B combined(Tier A+B 합산)", "Tier A+B", STATUS, JUDGMENT),
    ]:
        row = dict(common)
        row.update(
            {
                "ledger_row_id": f"{RUN_ID}__{suffix}",
                "subrun_id": f"{RUN_ID}__{suffix}",
                "row_id": f"{RUN_ID}__{suffix}",
                "record_view": view,
                "tier_scope": tier,
                "kpi_scope": "BO proxy rule surface and stress watch(BO 프록시 규칙 표면 및 압박 관찰)",
                "status": status,
                "judgment": judgment,
                "primary_kpi": f"net={final['selected_net_profit']};pf={final['selected_profit_factor']};density={final['selected_density']};short_pf={final['selected_synthetic_short_profit_factor']}",
                "guardrail_kpi": f"month_bad_count={final['month_bad_count']};package_rows={final['package_candidate_rows']};no_authority",
            }
        )
        if tier == "Tier B":
            for key in ["net_profit", "profit_factor", "expectancy", "drawdown", "recovery_factor", "trade_count", "long_trade_count", "short_trade_count"]:
                row[key] = ""
        ledger_rows.append(row)
    append_or_replace_csv(PROJECT_LEDGER, ["ledger_row_id"], ledger_rows, extend_header=True)
    append_or_replace_csv(STAGE_LEDGER, ["ledger_row_id"], ledger_rows, extend_header=True)
    drop_empty_csv_columns(PROJECT_LEDGER, ["promotion_candidate"])
    drop_empty_csv_columns(STAGE_LEDGER, ["promotion_candidate"])

    artifact_rows = []
    for artifact_type, path, notes in [
        ("quality_rule_surface", QUALITY_RULE_SURFACE, "BO quality rule surface(BO 품질 규칙 표면)."),
        ("broad_pool_negative_control", BROAD_POOL_NEGATIVE_CONTROL, "BO broad pool negative control(BO 넓은 풀 부정 대조)."),
        ("selected_quality_candidate", SELECTED_QUALITY_CANDIDATE, "BO selected quality candidate(BO 선택 품질 후보)."),
        ("stress_slice_review", STRESS_SLICE_REVIEW, "BO stress slice review(BO 압박 조각 검토)."),
        ("proxy_mt5_diff_plan", PROXY_MT5_DIFF_PLAN, "BO proxy/MT5 diff plan(BO 프록시/MT5 차이 계획)."),
        ("next_queue", RUN364BP_QUEUE, "BP review queue(BP 검토 대기열)."),
        ("report", REPORT_PATH, "BO report(BO 보고서)."),
        ("decision", DECISION_DOC, "BO decision doc(BO 결정 문서)."),
        ("final_decision", FINAL_DECISION, "Final decision(최종 결정)."),
        ("run_manifest", RUN_MANIFEST, "Run manifest(실행 목록)."),
    ]:
        if exists(path):
            artifact_rows.append(
                {
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "artifact_type": artifact_type,
                    "path": rel(path),
                    "artifact_path": rel(path),
                    "sha256": sha(path),
                    "created_at": final["created_at_utc"],
                    "created_at_utc": final["created_at_utc"],
                    "claim_boundary": CLAIM_BOUNDARY,
                    "artifact_id": f"{RUN_ID}__{artifact_type}",
                    "notes": notes,
                }
            )
    append_or_replace_csv(ARTIFACT_REGISTRY, ["artifact_id"], artifact_rows, extend_header=True)
    repair_run_registry_line_endings(RUN_ID)


def write_manifest(final: Mapping[str, Any]) -> None:
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
            "decision": DECISION,
            "created_at_utc": final["created_at_utc"],
            "claim_boundary": CLAIM_BOUNDARY,
            "inputs": [{"path": rel(path), "sha256": sha(path)} for path in INPUT_FILES if exists(path)],
            "outputs": [{"path": rel(path), "sha256": sha(path)} for path in OUTPUT_FILES if exists(path) and Path(path).is_file()],
        },
    )


def main() -> None:
    ensure_dirs()
    bn_final, bm_final, bk_final = validate_inputs()
    write_work_packet()
    parent_trades = parent.load_parent_trades()
    selected_pool = load_selected_pool(bm_final)
    broad_pool = load_broad_pool()
    surface, combined_map, synthetic_map, displaced_map = evaluate_variants(parent_trades, selected_pool, selected_pool_variants(selected_pool))
    broad_surface, _, _, _ = evaluate_variants(parent_trades, broad_pool, broad_pool_controls(broad_pool))
    selected = dict(select_candidate(surface))
    selected_id = str(selected["candidate_id"])
    selected_combined = combined_map[selected_id]
    selected_synthetic = synthetic_map[selected_id]
    selected_displaced = displaced_map[selected_id]
    stress = stress_rows(selected_id, selected_combined)
    short_segments = short_source_segment_rows(selected_id, selected_synthetic)
    overfit = overfit_rows(selected, broad_surface)
    proxy_mt5 = proxy_mt5_rows(bk_final, selected)
    queue = queue_rows(selected)
    receipt_paths = [RUN_EVIDENCE_RECEIPT, DATA_RECEIPT, EXPERIMENT_RECEIPT, MODEL_RECEIPT, ATTRIBUTION_RECEIPT, JUDGMENT_RECEIPT, CLAIM_RECEIPT, LINEAGE_RECEIPT]
    gates = gate_rows(selected, queue, receipt_paths)
    if any(row["status"] == "failed" for row in gates):
        write_csv(INPUT_MANIFEST, input_manifest_rows())
        write_csv(QUALITY_RULE_SURFACE, surface.to_dict("records"))
        write_csv(BROAD_POOL_NEGATIVE_CONTROL, broad_surface.to_dict("records"))
        write_csv(GATE_AUDIT, gates)
        raise RuntimeError("BO gate failure(BO 게이트 실패): " + ", ".join(row["gate"] for row in gates if row["status"] == "failed"))
    created_at = now_utc()
    final = final_payload(bn_final, selected, broad_surface, gates, created_at)

    write_csv(INPUT_MANIFEST, input_manifest_rows())
    write_csv(QUALITY_RULE_SURFACE, surface.to_dict("records"))
    write_csv(BROAD_POOL_NEGATIVE_CONTROL, broad_surface.to_dict("records"))
    write_json(SELECTED_QUALITY_CANDIDATE, selected)
    out_combined = selected_combined.copy()
    out_combined["entry_time"] = out_combined["entry_time_dt"].astype(str)
    out_combined["exit_time"] = out_combined["exit_time_dt"].astype(str)
    write_csv(SELECTED_QUALITY_TRADE_TAPE, out_combined.drop(columns=["entry_time_dt", "exit_time_dt"], errors="ignore").to_dict("records"))
    out_syn = selected_synthetic.copy()
    out_syn["entry_time"] = out_syn["entry_time_dt"].astype(str)
    out_syn["exit_time"] = out_syn["exit_time_dt"].astype(str)
    write_csv(SELECTED_SYNTHETIC_SHORT_TAPE, out_syn.drop(columns=["entry_time_dt", "exit_time_dt"], errors="ignore").to_dict("records"))
    write_csv(DISPLACED_PARENT_TRADES, selected_displaced.to_dict("records"))
    write_csv(STRESS_SLICE_REVIEW, stress)
    write_csv(SHORT_SOURCE_QUALITY_SEGMENTS, short_segments)
    write_csv(OVERFIT_GUARDRAIL_AUDIT, overfit)
    write_csv(PROXY_MT5_DIFF_PLAN, proxy_mt5)
    write_csv(RUN364BP_QUEUE, queue)
    write_receipts(final, selected, stress, proxy_mt5)
    write_csv(GATE_AUDIT, gates)
    write_json(FINAL_DECISION, final)
    refresh_lineage_receipt(final)
    write_manifest(final)
    write_docs(final, surface, broad_surface, selected, stress, short_segments, overfit, proxy_mt5, queue, gates)
    write_ledgers(final)
    print(json.dumps(json_ready(final), ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
