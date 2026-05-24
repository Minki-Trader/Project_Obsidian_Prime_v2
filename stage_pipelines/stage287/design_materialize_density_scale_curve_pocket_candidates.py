from __future__ import annotations

import csv
import hashlib
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import (  # noqa: E402
    ALPHA_LEDGER_COLUMNS,
    RUN_REGISTRY_COLUMNS,
    io_path,
    json_ready,
    path_exists,
    sha256_file_lf_normalized,
    upsert_csv_rows,
    write_csv_rows,
)
from foundation.models.onnx_bridge import ordered_hash  # noqa: E402


STAGE_ID = "287_onnx_candidate_campaign__density_scale_curve_pocket_rebuild"
RUN_ID = "run287A_design_materialize_density_scale_curve_pocket_candidates_v1"
RUN_NUMBER = "run287A"
SOURCE_RUN_ID = "run286C_review_trade_density_curve_quality_mt5_probe_v1"
STATUS = "completed_density_scale_curve_pocket_candidate_inputs_materialized_no_selection"
JUDGMENT = "curve_pocket_rebuild_candidate_inputs_materialized_no_candidate_selection"
NEXT_ACTION = "run287B_execute_density_scale_curve_pocket_mt5_probe"
UPDATED_ON = "2026-05-24"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_"
    "no_deployment_no_onnx_until_candidate_package_gate"
)

STAGE_ROOT = ROOT / "stages" / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER
INPUTS = STAGE_ROOT / "01_inputs"
REVIEWS = STAGE_ROOT / "03_reviews"
SELECTED = STAGE_ROOT / "04_selected" / "selection_status.md"
REVIEW_INDEX = REVIEWS / "review_index.md"
STAGE_LEDGER = REVIEWS / "stage_run_ledger.csv"
PAYLOAD_DIR = RUN_ROOT / "payloads"
HANDOFF_DIR = RUN_ROOT / "handoff"
MT5_HANDOFF_DIR = RUN_ROOT / "mt5_handoff"

SOURCE_Q02 = ROOT / "stages/279_onnx_candidate_campaign__directional_runtime_mapping_rebuild/02_runs/run279B/payloads/run279B_cp277D_breakout_q02_payload.parquet"
SOURCE_D = ROOT / "stages/286_onnx_candidate_campaign__trade_density_curve_quality_rebuild/02_runs/run286A/payloads/run286A_cp286D_trend_density_thr48_payload.parquet"
SOURCE_E = ROOT / "stages/286_onnx_candidate_campaign__trade_density_curve_quality_rebuild/02_runs/run286A/payloads/run286A_cp286E_macro_blend_density_payload.parquet"
SEED_QUEUE = INPUTS / "stage287_density_scale_curve_pocket_seed_queue.csv"
INPUT_REFS = INPUTS / "input_refs.md"

PRIOR_AUDIT = RUN_ROOT / "prior_stage_utilization_audit.csv"
BRANCH_QUEUE = RUN_ROOT / "branch_design_queue.csv"
CANDIDATE_SUPPLY = RUN_ROOT / "candidate_supply_diagnostics.csv"
PAYLOAD_MANIFEST = RUN_ROOT / "candidate_payload_manifest.csv"
MT5_QUEUE = RUN_ROOT / "mt5_probe_queue.csv"
DESIGN_RECEIPT = RUN_ROOT / "experiment_design_receipt.json"
DATA_RECEIPT = RUN_ROOT / "data_integrity_receipt.json"
LINEAGE = RUN_ROOT / "artifact_lineage_receipt.json"
RESULT_JUDGMENT = RUN_ROOT / "result_judgment.csv"
GATE_AUDIT = RUN_ROOT / "required_gate_coverage_audit.csv"
RUN_MANIFEST = RUN_ROOT / "run_manifest.json"
REPORT = REVIEWS / "run287A_density_scale_curve_pocket_materialization_report.md"

RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
IDEA_REGISTER = ROOT / "docs" / "registers" / "idea_registry.md"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
PRODUCER = Path("stage_pipelines/stage287/design_materialize_density_scale_curve_pocket_candidates.py")

BRANCH_COLUMNS = (
    "stage287_branch_id",
    "materialized_branch_id",
    "package_id",
    "experiment_lane",
    "fresh_thesis",
    "source_payload",
    "decision_surface",
    "risk_logic",
    "max_hold_bars",
    "close_on_flat_signal",
    "same_direction_reentry_cooldown_bars",
    "adapter_path",
    "runtime_handoff",
    "success_criteria",
    "failure_criteria",
    "claim_boundary",
)
SUPPLY_COLUMNS = (
    "materialized_branch_id",
    "package_id",
    "tier_scope",
    "split",
    "days",
    "rows",
    "active_signal_count",
    "active_signals_per_day",
    "long_signal_count",
    "short_signal_count",
    "max_hold_bars",
    "approx_trade_count",
    "approx_trades_per_day",
    "trade_density_screen",
)
MANIFEST_COLUMNS = (
    "queue_id",
    "materialized_branch_id",
    "stage287_branch_id",
    "package_id",
    "queue_role",
    "payload_path",
    "payload_hash",
    "handoff_path",
    "handoff_hash",
    "mt5_tier_a_signal_path",
    "mt5_tier_a_signal_hash",
    "mt5_tier_b_stress_signal_path",
    "mt5_tier_b_stress_signal_hash",
    "mt5_actual_routed_signal_path",
    "mt5_actual_routed_signal_hash",
    "direction_surface_hash",
    "direction_feature_order_hash",
    "max_hold_bars",
    "close_on_flat_signal",
    "same_direction_reentry_cooldown_bars",
    "tier_a_validation_signal_count",
    "tier_a_oos_signal_count",
    "tier_b_validation_signal_count",
    "tier_b_oos_signal_count",
    "actual_routed_validation_signal_count",
    "actual_routed_oos_signal_count",
    "approx_validation_trades_per_day",
    "approx_oos_trades_per_day",
    "selected_candidate",
    "adapter_package",
    "onnx_readiness",
    "claim_boundary",
)
AUDIT_COLUMNS = ("prior_stage", "evidence_path", "used_for", "effect")
RESULT_COLUMNS = (
    "result_subject",
    "evidence_available",
    "evidence_missing",
    "judgment_label",
    "judgment_class",
    "claim_boundary",
    "next_condition",
    "user_explanation_hook",
)
GATE_COLUMNS = ("gate_name", "status", "evidence_path", "effect")
STAGE_LEDGER_COLUMNS = (
    "row_id",
    "stage_id",
    "run_id",
    "view",
    "tier_scope",
    "scoreboard",
    "status",
    "judgment",
    "evidence_boundary",
    "report_path",
    "notes",
)
ARTIFACT_COLUMNS = (
    "artifact_id",
    "artifact_type",
    "path",
    "sha256",
    "stage_id",
    "run_id",
    "created_at_utc",
    "notes",
)


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path | str) -> str:
    item = Path(str(path))
    try:
        return item.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return item.as_posix()


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(
        json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> None:
    write_csv_rows(path, columns, rows)


def sha256_file(path: Path) -> str:
    return sha256_file_lf_normalized(path)


def read_csv_dicts(path: Path) -> list[dict[str, str]]:
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def replace_line_prefix(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + replacement + "\n"


def append_once(text: str, marker: str, addition: str) -> str:
    if marker in text:
        return text
    return text.rstrip() + "\n\n" + addition.rstrip() + "\n"


def prepend_focus(text: str, focus: str, marker: str) -> str:
    if marker in text:
        return text
    anchor = "current_focus:\n"
    if anchor in text:
        return text.replace(anchor, anchor + focus, 1)
    return text.rstrip() + "\ncurrent_focus:\n" + focus


def surface_hash(parts: Mapping[str, Any]) -> str:
    payload = json.dumps(json_ready(parts), ensure_ascii=False, sort_keys=True).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def as_num(series: pd.Series) -> pd.Series:
    return pd.to_numeric(series, errors="coerce").fillna(0.0)


def sign(series: pd.Series) -> np.ndarray:
    return np.sign(as_num(series)).astype("int8").to_numpy()


def load_sources() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    q02 = pd.read_parquet(io_path(SOURCE_Q02)).copy()
    d = pd.read_parquet(io_path(SOURCE_D)).copy()
    e = pd.read_parquet(io_path(SOURCE_E)).copy()
    for frame in (q02, d, e):
        frame["timestamp"] = pd.to_datetime(frame["timestamp"], utc=True)
    if not q02["timestamp"].equals(d["timestamp"]) or not q02["timestamp"].equals(e["timestamp"]):
        raise RuntimeError("source timestamp mismatch")
    return q02, d, e


def branch_specs() -> list[dict[str, Any]]:
    return [
        {
            "stage287_branch_id": "run287A_cp287A_consensus_session_switch",
            "materialized_branch_id": "run287A_cp287A_consensus_session_switch",
            "package_id": "cp287A_consensus_session_switch_surface",
            "experiment_lane": "session_switch_defensive(세션 전환 방어형)",
            "fresh_thesis": "D/E consensus(D/E 합의) plus session switch(세션 전환)로 7-8 trades/day(일 거래)를 유지하며 late/cash pocket(후반/현금장 포켓)을 줄인다.",
            "source_payload": "cp286D_cp286E_density_scale_clues",
            "decision_surface": "D/E agree(D/E 합의) 우선, cash session(현금장)은 D+score>=0.50, late session(후반장)은 E+macro agreement(매크로 합의).",
            "risk_logic": "max_hold(최대 보유)=9, threshold-only repair(임계값 단독 수리) 금지.",
            "max_hold_bars": 9,
            "close_on_flat_signal": False,
            "same_direction_reentry_cooldown_bars": 0,
            "success_criteria": "4-10 trades/day(일 거래), cp282D보다 높은 net profit(순수익), 낮은 local pocket(국소 포켓).",
            "failure_criteria": "deep rolling pocket(깊은 이동 포켓) 또는 session/month hole(세션/월 구멍)이 남으면 실패.",
        },
        {
            "stage287_branch_id": "run287A_cp287B_volnorm_pressure_release",
            "materialized_branch_id": "run287A_cp287B_volnorm_pressure_release",
            "package_id": "cp287B_volnorm_pressure_release_surface",
            "experiment_lane": "volatility_pressure_defensive(변동성/압력 방어형)",
            "fresh_thesis": "volatility-normalized trend(변동성 정규화 추세)와 signal pressure release(신호 압력 완화)로 4-5 trades/day(일 거래) 하한과 smoother curve(더 부드러운 곡선)를 동시에 본다.",
            "source_payload": "cp286D_density_scale_clue",
            "decision_surface": "majority trend(다수 추세), score>=0.52, vol 0.55-1.45, zscore<=1.6, rolling pressure<=8.",
            "risk_logic": "max_hold(최대 보유)=6, close_on_flat(평탄 신호 청산)=true.",
            "max_hold_bars": 6,
            "close_on_flat_signal": True,
            "same_direction_reentry_cooldown_bars": 0,
            "success_criteria": "lower-band(하단) 4-5 trades/day(일 거래)와 더 부드러운 local curve(국소 곡선).",
            "failure_criteria": "net scale(수익 규모)가 사라지거나 density(밀도)가 4 trades/day(일 거래) 아래면 실패.",
        },
        {
            "stage287_branch_id": "run287A_cp287C_macro_countercheck_hold6",
            "materialized_branch_id": "run287A_cp287C_macro_countercheck_hold6",
            "package_id": "cp287C_macro_countercheck_hold6_surface",
            "experiment_lane": "macro_countercheck_balanced(매크로 대조 균형형)",
            "fresh_thesis": "macro countercheck(매크로 대조)와 shorter hold(짧은 보유)로 6-7 trades/day(일 거래)와 pocket asymmetry(포켓 비대칭) 축소를 함께 본다.",
            "source_payload": "cp286E_density_scale_clue",
            "decision_surface": "entry/trend fallback(진입/추세 대체)이 score>=0.50이고 macro or DI agreement(매크로 또는 DI 합의)를 요구한다.",
            "risk_logic": "max_hold(최대 보유)=6, opposite signal(반대 신호)에서 reverse(전환), flat-close(평탄 청산) 없음.",
            "max_hold_bars": 6,
            "close_on_flat_signal": False,
            "same_direction_reentry_cooldown_bars": 0,
            "success_criteria": "6-8 trades/day(일 거래)와 cp286E보다 낮은 rolling pocket(이동 포켓).",
            "failure_criteria": "PF(수익 팩터)나 curve(곡선)가 몇 개월에 지배되면 실패.",
        },
        {
            "stage287_branch_id": "run287A_cp287D_session_asymmetric_hold9",
            "materialized_branch_id": "run287A_cp287D_session_asymmetric_hold9",
            "package_id": "cp287D_session_asymmetric_hold9_surface",
            "experiment_lane": "session_asymmetric_balanced(세션 비대칭 균형형)",
            "fresh_thesis": "cash session(현금장)과 late session(후반장)에 서로 다른 evidence(근거)를 요구해 8-9 trades/day(일 거래)를 본다.",
            "source_payload": "stage267_session_weakness_plus_cp286D_E",
            "decision_surface": "cash session(현금장)은 trend density(추세 밀도), late session(후반장)은 stronger macro/DI agreement(강한 매크로/DI 합의).",
            "risk_logic": "max_hold(최대 보유)=9, flat-close(평탄 청산) 없음, late pocket exposure(후반 포켓 노출) 축소.",
            "max_hold_bars": 9,
            "close_on_flat_signal": False,
            "same_direction_reentry_cooldown_bars": 0,
            "success_criteria": "8-9 trades/day(일 거래)와 두 session bucket(세션 버킷)이 모두 비파괴적이면 성공.",
            "failure_criteria": "late/cash session(후반/현금장)이 persistent negative bucket(지속 손실 버킷)이 되면 실패.",
        },
        {
            "stage287_branch_id": "run287A_cp287E_consensus_pullback_mix",
            "materialized_branch_id": "run287A_cp287E_consensus_pullback_mix",
            "package_id": "cp287E_consensus_pullback_mix_surface",
            "experiment_lane": "aggressive_smoothness_mix(공격형 매끄러움 혼합)",
            "fresh_thesis": "consensus(합의)와 moderate pullback re-entry(중간 되돌림 재진입)로 8-10 trades/day(일 거래)와 extreme-z pocket(극단 z 포켓) 완화를 같이 본다.",
            "source_payload": "cp286D_cp286E_density_scale_clues",
            "decision_surface": "D/E consensus(D/E 합의) 또는 moderate pullback fallback(중간 되돌림 대체) with score>=0.55 and macro/EMA agreement(매크로/EMA 합의).",
            "risk_logic": "max_hold(최대 보유)=6으로 aggressive density(공격형 밀도)는 허용하되 long underwater pocket(긴 잠수 포켓)을 줄인다.",
            "max_hold_bars": 6,
            "close_on_flat_signal": False,
            "same_direction_reentry_cooldown_bars": 0,
            "success_criteria": "8-10 trades/day(일 거래), cp286E보다 높은 scale(규모), deep rolling pocket(깊은 이동 포켓) 없음.",
            "failure_criteria": "overtrading(과거래) 또는 one-month contribution(한 달 기여) 지배가 생기면 실패.",
        },
    ]


def approximate_trades(signal: np.ndarray, max_hold_bars: int) -> int:
    trades = 0
    position = 0
    hold = 0
    for value in signal.astype("int8"):
        current = int(value)
        if position == 0:
            if current != 0:
                trades += 1
                position = current
                hold = 1
            continue
        hold += 1
        if current == 0:
            position = 0
            hold = 0
        elif current == -position:
            trades += 1
            position = current
            hold = 1
        elif hold >= max_hold_bars:
            position = 0
            hold = 0
    return trades


def signal_label(value: int) -> str:
    return "long" if value > 0 else "short" if value < 0 else "flat"


def build_pressure(frame: pd.DataFrame, signal: np.ndarray) -> np.ndarray:
    pressure = np.zeros(len(frame), dtype="float64")
    temp = pd.DataFrame({"tier": frame["tier_scope"], "split": frame["split"], "active": signal != 0})
    for _, group in temp.groupby(["tier", "split"], sort=False):
        pressure[group.index.to_numpy()] = group["active"].astype("int8").rolling(12, min_periods=1).sum().to_numpy()
    return pressure


def build_signal(q02: pd.DataFrame, d: pd.DataFrame, e: pd.DataFrame, spec: Mapping[str, Any]) -> np.ndarray:
    d_signal = as_num(d["route_signal_value"]).astype("int8").to_numpy()
    e_signal = as_num(e["route_signal_value"]).astype("int8").to_numpy()
    entry = as_num(q02["entry_signal"]).astype("int8").to_numpy()
    score = as_num(q02["candidate_decision_score"]).to_numpy()
    vol = as_num(q02["historical_vol_5_over_20"]).to_numpy()
    z_abs = as_num(q02["return_zscore_20"]).abs().to_numpy()
    di = sign(q02["di_spread_14"])
    ema = sign(q02["ema20_ema50_diff"])
    rsi = sign(q02["rsi_14_slope_3"])
    mega = sign(q02["us100_minus_mega8_equal_return_1"])
    top3 = sign(q02["us100_minus_top3_weighted_return_1"])
    trend = np.sign(di + ema + rsi).astype("int8")
    macro = np.where((mega + top3) > 0, 1, np.where((mega + top3) < 0, -1, 0)).astype("int8")
    fallback = np.where(entry != 0, entry, np.where(trend != 0, trend, ema)).astype("int8")
    hour = q02["timestamp"].dt.hour.to_numpy()
    cash = (hour >= 16) & (hour < 21)
    late = hour >= 21
    pressure = build_pressure(q02, d_signal)
    branch_id = str(spec["materialized_branch_id"])
    if branch_id.endswith("cp287A_consensus_session_switch"):
        return np.where(
            (d_signal == e_signal) & (d_signal != 0),
            d_signal,
            np.where(cash & (d_signal != 0) & (score >= 0.50), d_signal, np.where(late & (e_signal != 0) & (macro == e_signal), e_signal, 0)),
        ).astype("int8")
    if branch_id.endswith("cp287B_volnorm_pressure_release"):
        mask = (trend != 0) & (score >= 0.52) & (vol >= 0.55) & (vol <= 1.45) & (z_abs <= 1.6) & (pressure <= 8)
        return np.where(mask, trend, 0).astype("int8")
    if branch_id.endswith("cp287C_macro_countercheck_hold6"):
        agreed = ((macro == fallback) & (macro != 0)) | (di == fallback)
        mask = (fallback != 0) & (score >= 0.50) & agreed & (vol >= 0.50) & (vol <= 1.55) & (z_abs <= 1.7)
        return np.where(mask, fallback, 0).astype("int8")
    if branch_id.endswith("cp287D_session_asymmetric_hold9"):
        cash_mask = cash & (trend != 0) & (score >= 0.48) & (vol >= 0.45) & (vol <= 1.65) & (z_abs <= 1.8)
        late_mask = late & (fallback != 0) & (score >= 0.54) & ((macro == fallback) | (di == fallback)) & (vol >= 0.50) & (vol <= 1.55) & (z_abs <= 1.5)
        return np.where(cash_mask | late_mask, np.where(cash, trend, fallback), 0).astype("int8")
    if branch_id.endswith("cp287E_consensus_pullback_mix"):
        consensus = (d_signal == e_signal) & (d_signal != 0) & (z_abs <= 2.0)
        pullback = (z_abs >= 0.4) & (z_abs <= 1.4) & (fallback != 0) & (score >= 0.55) & ((macro == fallback) | (ema == fallback))
        return np.where(consensus | pullback, np.where(consensus, d_signal, fallback, ), 0).astype("int8")
    raise ValueError(branch_id)


def signal_counts(frame: pd.DataFrame, max_hold_bars: int) -> dict[tuple[str, str], dict[str, Any]]:
    rows: dict[tuple[str, str], dict[str, Any]] = {}
    for (tier, split), group in frame.groupby(["tier_scope", "split"], sort=False):
        if split not in {"validation", "oos"}:
            continue
        signal = as_num(group["route_signal_value"]).astype("int8").to_numpy()
        days = int(pd.to_datetime(group["timestamp"], utc=True).dt.date.nunique())
        approx = approximate_trades(signal, max_hold_bars)
        rows[(str(tier), str(split))] = {
            "days": days,
            "rows": int(len(group)),
            "active_signal_count": int((signal != 0).sum()),
            "active_signals_per_day": float((signal != 0).sum() / days) if days else 0.0,
            "long_signal_count": int((signal == 1).sum()),
            "short_signal_count": int((signal == -1).sum()),
            "max_hold_bars": max_hold_bars,
            "approx_trade_count": approx,
            "approx_trades_per_day": float(approx / days) if days else 0.0,
        }
    return rows


def export_signal_csv(frame: pd.DataFrame, path: Path, tier_scope: str) -> Path:
    export = frame.loc[
        frame["tier_scope"].astype(str).eq(tier_scope),
        ["timestamp", "split", "tier_scope", "route_signal_value", "route_signal_label"],
    ].copy()
    export["timestamp"] = pd.to_datetime(export["timestamp"], utc=True).dt.strftime("%Y-%m-%d %H:%M:%S")
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    export.to_csv(io_path(path), index=False, lineterminator="\n", encoding="utf-8")
    return path


def prior_audit_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    refs = read_csv_dicts(SEED_QUEUE) if path_exists(SEED_QUEUE) else []
    for row in refs:
        rows.append(
            {
                "prior_stage": "Stage286(286단계)",
                "evidence_path": rel(SEED_QUEUE),
                "used_for": row.get("source_package_id", ""),
                "effect": "density/scale clue(밀도/규모 단서)만 가져오고 candidate(후보) 이름은 계승하지 않는다.",
            }
        )
    for path, used_for in [
        (ROOT / "stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_monthly_weakness_matrix.csv", "monthly_weakness_memory(월별 약점 기억)"),
        (ROOT / "stages/267_adapter_research__baseline_candidate_racing_protocol/03_reviews/stage267_segment_weakness_matrix.csv", "segment_weakness_memory(구간 약점 기억)"),
        (ROOT / "stages/282_onnx_candidate_campaign__validation_first_asymmetric_confirmation_rebuild/02_runs/run282C/curve_stability_summary.csv", "curve_stability_memory(곡선 안정성 기억)"),
        (ROOT / "stages/286_onnx_candidate_campaign__trade_density_curve_quality_rebuild/02_runs/run286C/local_curve_pocket_diagnostics.csv", "local_curve_pocket_memory(국소 곡선 포켓 기억)"),
    ]:
        if path_exists(path):
            rows.append(
                {
                    "prior_stage": "prior_stage_reference(이전 단계 참고)",
                    "evidence_path": rel(path),
                    "used_for": used_for,
                    "effect": "Stage287(287단계) gate(게이트)에 curve pocket(곡선 포켓), month/session weakness(월/세션 약점)을 반영한다.",
                }
            )
    return rows


def materialize() -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[Path]]:
    q02, d, e = load_sources()
    branch_rows: list[dict[str, Any]] = []
    supply_rows: list[dict[str, Any]] = []
    manifest_rows: list[dict[str, Any]] = []
    artifacts: list[Path] = []
    for index, spec in enumerate(branch_specs(), start=1):
        signal = build_signal(q02, d, e, spec)
        payload = q02.copy()
        payload["package_id"] = spec["package_id"]
        payload["stage287_branch_id"] = spec["stage287_branch_id"]
        payload["materialized_branch_id"] = spec["materialized_branch_id"]
        payload["queue_role"] = spec["experiment_lane"]
        payload["fresh_thesis"] = spec["fresh_thesis"]
        payload["route_policy"] = spec["decision_surface"]
        payload["signal_policy"] = "stage287_density_scale_curve_pocket_route_signal"
        payload["route_signal_value"] = signal
        payload["route_signal_label"] = [signal_label(int(value)) for value in signal]
        payload["signal_active"] = (signal != 0).astype("int8")
        payload["max_hold_bars"] = int(spec["max_hold_bars"])
        payload["close_on_flat_signal"] = bool(spec["close_on_flat_signal"])
        payload["same_direction_reentry_cooldown_bars"] = int(spec["same_direction_reentry_cooldown_bars"])
        payload["runtime_handoff_status"] = "materialized_for_run287B_mt5_probe"
        payload["payload_claim_boundary"] = BOUNDARY
        direction_hash = surface_hash(
            {key: spec[key] for key in ("package_id", "decision_surface", "risk_logic", "max_hold_bars", "close_on_flat_signal")}
        )
        feature_hash = ordered_hash(("route_signal_value",))
        payload["direction_surface_hash"] = direction_hash
        payload["direction_feature_order_hash"] = feature_hash
        payload_path = PAYLOAD_DIR / f'{spec["materialized_branch_id"]}_payload.parquet'
        io_path(payload_path.parent).mkdir(parents=True, exist_ok=True)
        payload.to_parquet(io_path(payload_path), index=False)
        handoff_path = HANDOFF_DIR / f'{spec["materialized_branch_id"]}_handoff.json'
        write_json(
            handoff_path,
            {
                **spec,
                "direction_surface_hash": direction_hash,
                "direction_feature_order_hash": feature_hash,
                "selected_candidate": "none",
                "adapter_package": "none",
                "onnx_readiness": "not_claimed",
                "claim_boundary": BOUNDARY,
            },
        )
        tier_a_signal = export_signal_csv(payload, MT5_HANDOFF_DIR / f'{spec["materialized_branch_id"]}_tier_a_signal.csv', "Tier A")
        tier_b_signal = export_signal_csv(payload, MT5_HANDOFF_DIR / f'{spec["materialized_branch_id"]}_tier_b_signal.csv', "Tier B")
        routed_signal = export_signal_csv(payload, MT5_HANDOFF_DIR / f'{spec["materialized_branch_id"]}_actual_routed_signal.csv', "Tier A")
        counts = signal_counts(payload, int(spec["max_hold_bars"]))
        for (tier, split), count_row in counts.items():
            per_day = float(count_row["approx_trades_per_day"])
            supply_rows.append(
                {
                    **count_row,
                    "materialized_branch_id": spec["materialized_branch_id"],
                    "package_id": spec["package_id"],
                    "tier_scope": tier,
                    "split": split,
                    "trade_density_screen": "in_target_band" if 4.0 <= per_day <= 10.0 else "outside_target_band",
                }
            )
        tier_a_val = counts.get(("Tier A", "validation"), {})
        tier_a_oos = counts.get(("Tier A", "oos"), {})
        tier_b_val = counts.get(("Tier B", "validation"), {})
        tier_b_oos = counts.get(("Tier B", "oos"), {})
        manifest_rows.append(
            {
                "queue_id": f"run287A_queue_{index:02d}",
                "materialized_branch_id": spec["materialized_branch_id"],
                "stage287_branch_id": spec["stage287_branch_id"],
                "package_id": spec["package_id"],
                "queue_role": spec["experiment_lane"],
                "payload_path": rel(payload_path),
                "payload_hash": sha256_file(payload_path),
                "handoff_path": rel(handoff_path),
                "handoff_hash": sha256_file(handoff_path),
                "mt5_tier_a_signal_path": rel(tier_a_signal),
                "mt5_tier_a_signal_hash": sha256_file(tier_a_signal),
                "mt5_tier_b_stress_signal_path": rel(tier_b_signal),
                "mt5_tier_b_stress_signal_hash": sha256_file(tier_b_signal),
                "mt5_actual_routed_signal_path": rel(routed_signal),
                "mt5_actual_routed_signal_hash": sha256_file(routed_signal),
                "direction_surface_hash": direction_hash,
                "direction_feature_order_hash": feature_hash,
                "max_hold_bars": spec["max_hold_bars"],
                "close_on_flat_signal": spec["close_on_flat_signal"],
                "same_direction_reentry_cooldown_bars": spec["same_direction_reentry_cooldown_bars"],
                "tier_a_validation_signal_count": tier_a_val.get("active_signal_count", 0),
                "tier_a_oos_signal_count": tier_a_oos.get("active_signal_count", 0),
                "tier_b_validation_signal_count": tier_b_val.get("active_signal_count", 0),
                "tier_b_oos_signal_count": tier_b_oos.get("active_signal_count", 0),
                "actual_routed_validation_signal_count": tier_a_val.get("active_signal_count", 0),
                "actual_routed_oos_signal_count": tier_a_oos.get("active_signal_count", 0),
                "approx_validation_trades_per_day": tier_a_val.get("approx_trades_per_day", 0),
                "approx_oos_trades_per_day": tier_a_oos.get("approx_trades_per_day", 0),
                "selected_candidate": "none",
                "adapter_package": "none",
                "onnx_readiness": "not_claimed",
                "claim_boundary": BOUNDARY,
            }
        )
        branch_rows.append(
            {
                **spec,
                "adapter_path": "deferred_until_curve_quality_passes",
                "runtime_handoff": "single route_signal table(단일 경로 신호 표) with branch-specific max_hold(분기별 최대 보유)",
                "claim_boundary": BOUNDARY,
            }
        )
        artifacts.extend([payload_path, handoff_path, tier_a_signal, tier_b_signal, routed_signal])
    return branch_rows, supply_rows, manifest_rows, artifacts


def report_markdown(manifest_rows: Sequence[Mapping[str, Any]]) -> str:
    rows = [
        f"- `{row['package_id']}`: max_hold(최대 보유) `{row['max_hold_bars']}`, validation approx(검증 근사) `{float(row['approx_validation_trades_per_day']):.2f}`, OOS approx(표본외 근사) `{float(row['approx_oos_trades_per_day']):.2f}` trades/day(일 거래)."
        for row in manifest_rows
    ]
    return f"""# run287A Density Scale Curve Pocket Materialization(287A 밀도/규모/곡선 포켓 물질화)

- stage_id(단계 ID): `{STAGE_ID}`
- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- branch_count(분기 수): `{len(manifest_rows)}`
- selected_candidate(선택 후보): `none`
- Adapter package(어댑터 패키지): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- next_action(다음 행동): `{NEXT_ACTION}`

## Candidate Queue(후보 대기열)

{chr(10).join(rows)}

Effect(효과): 각 branch(분기)는 4-10 trades/day(일 거래) 목표를 향한 구조 실험이며, MT5 probe(MT5 탐침) 전에는 성과 후보가 아니다.
"""


def write_outputs(
    branch_rows: Sequence[Mapping[str, Any]],
    supply_rows: Sequence[Mapping[str, Any]],
    manifest_rows: Sequence[Mapping[str, Any]],
    payload_artifacts: Sequence[Path],
    created_at: str,
) -> list[Path]:
    audit_rows = prior_audit_rows()
    write_csv(PRIOR_AUDIT, AUDIT_COLUMNS, audit_rows)
    write_csv(BRANCH_QUEUE, BRANCH_COLUMNS, branch_rows)
    write_csv(CANDIDATE_SUPPLY, SUPPLY_COLUMNS, supply_rows)
    write_csv(PAYLOAD_MANIFEST, MANIFEST_COLUMNS, manifest_rows)
    write_csv(MT5_QUEUE, MANIFEST_COLUMNS, manifest_rows)
    write_json(
        DESIGN_RECEIPT,
        {
            "hypothesis": "density_scale_curve_pocket_rebuild",
            "decision_use": "feed run287B MT5 probe only",
            "comparison_baseline": "cp286D/cp286E density-scale clues and cp282D low-scale ONNX technical reference",
            "success_criteria": "4-10 trades/day, stronger net scale, smoother local balance curve",
            "failure_criteria": "deep local pockets, weak session/month holes, below-density or low net scale",
            "evidence_plan": [rel(PRIOR_AUDIT), rel(CANDIDATE_SUPPLY), rel(MT5_QUEUE)],
            "claim_boundary": BOUNDARY,
        },
    )
    write_json(
        DATA_RECEIPT,
        {
            "source_q02_rows": len(pd.read_parquet(io_path(SOURCE_Q02))),
            "source_d_rows": len(pd.read_parquet(io_path(SOURCE_D))),
            "source_e_rows": len(pd.read_parquet(io_path(SOURCE_E))),
            "label_or_future_columns_added": False,
            "claim_boundary": BOUNDARY,
        },
    )
    write_csv(
        RESULT_JUDGMENT,
        RESULT_COLUMNS,
        [
            {
                "result_subject": "run287A_materialized_candidate_inputs",
                "evidence_available": rel(PAYLOAD_MANIFEST),
                "evidence_missing": "MT5 runtime KPI and curve review",
                "judgment_label": JUDGMENT,
                "judgment_class": "inconclusive_until_mt5_probe(탐침 전 불충분)",
                "claim_boundary": BOUNDARY,
                "next_condition": NEXT_ACTION,
                "user_explanation_hook": "곡선 포켓 재구성 후보 입력을 만들었지만 성과 후보는 아니다.",
            }
        ],
    )
    write_csv(
        GATE_AUDIT,
        GATE_COLUMNS,
        [
            {
                "gate_name": "prior_stage_utilization(이전 단계 활용)",
                "status": "passed",
                "evidence_path": rel(PRIOR_AUDIT),
                "effect": "과거 stage(단계) 자료를 후보 설계에 연결했다.",
            },
            {
                "gate_name": "no_threshold_only_repair(임계값 단독 수리 없음)",
                "status": "passed",
                "evidence_path": rel(BRANCH_QUEUE),
                "effect": "session(세션), volatility(변동성), pressure(압력), hold(보유)를 함께 바꿨다.",
            },
            {
                "gate_name": "no_candidate_no_onnx_claim(후보와 온엑스 주장 없음)",
                "status": "passed",
                "evidence_path": rel(RESULT_JUDGMENT),
                "effect": "MT5(MetaTrader 5, 메타트레이더5) 전 성과 주장을 막는다.",
            },
        ],
    )
    write_md(REPORT, report_markdown(manifest_rows))
    artifacts = [
        PRIOR_AUDIT,
        BRANCH_QUEUE,
        CANDIDATE_SUPPLY,
        PAYLOAD_MANIFEST,
        MT5_QUEUE,
        DESIGN_RECEIPT,
        DATA_RECEIPT,
        RESULT_JUDGMENT,
        GATE_AUDIT,
        REPORT,
        *payload_artifacts,
    ]
    write_json(
        LINEAGE,
        {
            "run_id": RUN_ID,
            "producer": PRODUCER.as_posix(),
            "source_artifacts": [rel(SOURCE_Q02), rel(SOURCE_D), rel(SOURCE_E), rel(SEED_QUEUE), rel(INPUT_REFS)],
            "produced_artifacts": [rel(path) for path in artifacts if path_exists(path)],
            "claim_boundary": BOUNDARY,
        },
    )
    artifacts.append(LINEAGE)
    write_json(
        RUN_MANIFEST,
        {
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "status": STATUS,
            "judgment": JUDGMENT,
            "created_at_utc": created_at,
            "branch_count": len(manifest_rows),
            "mt5_queue_rows": len(manifest_rows),
            "next_action": NEXT_ACTION,
            "selected_candidate": "none",
            "adapter_package": "none",
            "onnx_readiness": "not_claimed",
            "claim_boundary": BOUNDARY,
        },
    )
    artifacts.append(RUN_MANIFEST)
    return [path for path in artifacts if path_exists(path)]


def update_docs_and_registers(created_at: str, artifacts: Sequence[Path], manifest_rows: Sequence[Mapping[str, Any]]) -> None:
    upsert_csv_rows(
        RUN_REGISTRY,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "onnx_candidate_campaign_density_scale_curve_pocket",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT),
                "notes": f"branches={len(manifest_rows)};next_action={NEXT_ACTION}",
            }
        ],
        key="run_id",
    )
    upsert_csv_rows(
        ALPHA_LEDGER,
        ALPHA_LEDGER_COLUMNS,
        [
            {
                "ledger_row_id": f"{RUN_ID}__materialization",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": RUN_NUMBER,
                "parent_run_id": SOURCE_RUN_ID,
                "record_view": "candidate_supply_diagnostics",
                "tier_scope": "Tier A/Tier B/Tier A+B",
                "kpi_scope": "structural_scout",
                "scoreboard_lane": "density_scale_curve_pocket",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT),
                "primary_kpi": f"mt5_queue_rows={len(manifest_rows)}",
                "guardrail_kpi": "prior_stage_audit_no_threshold_only_repair",
                "external_verification_status": "not_attempted_run287A_materialization",
                "notes": "MT5 probe required before result judgment.",
            }
        ],
        key="ledger_row_id",
    )
    upsert_csv_rows(
        STAGE_LEDGER,
        STAGE_LEDGER_COLUMNS,
        [
            {
                "row_id": f"{RUN_ID}__materialization",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "view": "density_scale_curve_pocket_materialization",
                "tier_scope": "Tier A/Tier B/Tier A+B",
                "scoreboard": "candidate_supply_diagnostics",
                "status": STATUS,
                "judgment": JUDGMENT,
                "evidence_boundary": "no_candidate_no_adapter_no_onnx",
                "report_path": rel(REPORT),
                "notes": f"mt5_queue_rows={len(manifest_rows)};next_action={NEXT_ACTION}",
            }
        ],
        key="row_id",
    )
    artifact_rows = [
        {
            "artifact_id": f"{RUN_ID}__{hashlib.sha1(rel(path).encode('utf-8')).hexdigest()[:12]}",
            "artifact_type": "stage287_density_scale_curve_pocket_artifact",
            "path": rel(path),
            "sha256": sha256_file(path),
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": created_at,
            "notes": "run287A density scale curve pocket materialization(287A 밀도/규모/곡선 포켓 물질화)",
        }
        for path in artifacts
        if path_exists(path)
    ]
    upsert_csv_rows(ARTIFACT_REGISTRY, ARTIFACT_COLUMNS, artifact_rows, key="artifact_id")
    selected = io_path(SELECTED).read_text(encoding="utf-8-sig") if path_exists(SELECTED) else "# Stage287 Selection Status(287단계 선택 상태)\n"
    selected = replace_line_prefix(selected, "- stage_status(단계 상태):", f"- stage_status(단계 상태): `{STATUS}`")
    selected = replace_line_prefix(selected, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    selected = replace_line_prefix(selected, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    selected = append_once(selected, "run287A_report", f"- run287A_report(287A 보고서): `{rel(REPORT)}`")
    selected = append_once(selected, "run287A_mt5_queue", f"- run287A_mt5_queue(287A MT5 대기열): `{rel(MT5_QUEUE)}`")
    write_md(SELECTED, selected)

    review_index = io_path(REVIEW_INDEX).read_text(encoding="utf-8-sig") if path_exists(REVIEW_INDEX) else "# Stage287 Review Index(287단계 검토 색인)\n"
    review_index = append_once(review_index, "run287A_report", f"- run287A_report(287A 보고서): `{rel(REPORT)}`")
    write_md(REVIEW_INDEX, review_index)

    current = io_path(CURRENT_STATE).read_text(encoding="utf-8-sig")
    current = replace_line_prefix(current, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_line_prefix(current, "- status(상태):", f"- status(상태): `{STATUS}`")
    current = replace_line_prefix(current, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    current = append_once(
        current,
        "run287A_summary",
        f"- run287A_summary(287A 요약): density/scale curve-pocket rebuild(밀도/규모 곡선 포켓 재구성) 후보 `{len(manifest_rows)}`개를 물질화했다. Effect(효과): 과거 stage(단계) 약점 자료를 연결했고 threshold-only repair(임계값 단독 수리)는 피했다.",
    )
    write_md(CURRENT_STATE, current)

    workspace = io_path(WORKSPACE_STATE).read_text(encoding="utf-8-sig")
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    workspace = replace_line_prefix(workspace, "updated_on:", f"updated_on: '{UPDATED_ON}'")
    focus = (
        f"- >-\n"
        f"  Stage287(287단계) run287A(287A 실행) density scale curve pocket materialization(밀도/규모/곡선 포켓 물질화) `{RUN_ID}`. "
        f"Effect(효과): 후보 `{len(manifest_rows)}`개를 MT5 probe(MT5 탐침) 대기열로 넘기며 후보/어댑터/온엑스 주장은 하지 않는다.\n"
    )
    workspace = prepend_focus(workspace, focus, RUN_ID)
    write_md(WORKSPACE_STATE, workspace)

    changelog = io_path(CHANGELOG).read_text(encoding="utf-8-sig")
    changelog = append_once(
        changelog,
        RUN_ID,
        f"## {UPDATED_ON} run287A Density scale curve pocket materialization(287A 밀도/규모/곡선 포켓 물질화)\n\n"
        f"- status(상태): `{STATUS}`\n"
        f"- judgment(판정): `{JUDGMENT}`\n"
        f"- effect(효과): 후보 `{len(manifest_rows)}`개를 MT5 probe queue(MT5 탐침 대기열)로 만들었다.\n"
        f"- boundary(경계): selected candidate(선택 후보), Adapter package(어댑터 패키지), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 `none/not_claimed`다.\n",
    )
    write_md(CHANGELOG, changelog)

    idea = io_path(IDEA_REGISTER).read_text(encoding="utf-8-sig")
    idea = append_once(
        idea,
        "IDEA-ST287-RUN287A-DENSITY-SCALE-CURVE-POCKET",
        f"| `IDEA-ST287-RUN287A-DENSITY-SCALE-CURVE-POCKET` | `{STAGE_ID}` | density/scale curve-pocket rebuild(밀도/규모 곡선 포켓 재구성) 후보 `{len(manifest_rows)}`개 | `Tier A used + Tier B fallback stress + actual routed total` | `materialized_no_candidate` | 과거 stage(단계) 자료를 활용해 session/volatility/hold(세션/변동성/보유) 구조를 바꾼다. |",
    )
    write_md(IDEA_REGISTER, idea)


def main() -> None:
    for path in [RUN_ROOT, PAYLOAD_DIR, HANDOFF_DIR, MT5_HANDOFF_DIR, REVIEWS]:
        io_path(path).mkdir(parents=True, exist_ok=True)
    created_at = utc_now()
    branch_rows, supply_rows, manifest_rows, payload_artifacts = materialize()
    artifacts = write_outputs(branch_rows, supply_rows, manifest_rows, payload_artifacts, created_at)
    update_docs_and_registers(created_at, artifacts, manifest_rows)
    print(
        json.dumps(
            {
                "run_id": RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "branch_count": len(manifest_rows),
                "mt5_queue_rows": len(manifest_rows),
                "selected_candidate": "none",
                "adapter_package": "none",
                "onnx_readiness": "not_claimed",
                "goal_achieve": "not_claimed",
                "next_action": NEXT_ACTION,
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
