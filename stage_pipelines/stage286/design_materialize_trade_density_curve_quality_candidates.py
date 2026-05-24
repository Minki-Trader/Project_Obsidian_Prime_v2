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


STAGE_ID = "286_onnx_candidate_campaign__trade_density_curve_quality_rebuild"
RUN_ID = "run286A_design_materialize_trade_density_curve_quality_candidates_v1"
SOURCE_RUN_ID = "run285A_export_cp282d_adapter_to_onnx_and_runtime_reproduction_v1"
STATUS = "completed_trade_density_curve_quality_candidate_inputs_materialized_no_selection"
JUDGMENT = "high_scale_signal_density_candidates_materialized_no_candidate_selection"
NEXT_ACTION = "run286B_execute_trade_density_curve_quality_mt5_probe"
UPDATED_ON = "2026-05-24"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_"
    "no_deployment_no_onnx_until_candidate_package_gate"
)

STAGE_ROOT = ROOT / "stages" / STAGE_ID
SPEC = STAGE_ROOT / "00_spec" / "stage_brief.md"
INPUTS = STAGE_ROOT / "01_inputs"
RUN_ROOT = STAGE_ROOT / "02_runs" / "run286A"
REVIEWS = STAGE_ROOT / "03_reviews"
SELECTED = STAGE_ROOT / "04_selected" / "selection_status.md"
REVIEW_INDEX = REVIEWS / "review_index.md"
STAGE_LEDGER = REVIEWS / "stage_run_ledger.csv"

PAYLOAD_DIR = RUN_ROOT / "payloads"
HANDOFF_DIR = RUN_ROOT / "handoff"
MT5_HANDOFF_DIR = RUN_ROOT / "mt5_handoff"
REQUIREMENT_CONTRACT = RUN_ROOT / "stage286_requirement_contract.json"
BASELINE_ATTRIBUTION = RUN_ROOT / "cp282d_baseline_gap_attribution.csv"
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
REPORT = REVIEWS / "run286A_trade_density_curve_quality_materialization_report.md"
INPUT_REFS = INPUTS / "input_refs.md"

STAGE279_RUN279B = ROOT / "stages" / "279_onnx_candidate_campaign__directional_runtime_mapping_rebuild" / "02_runs" / "run279B"
SOURCE_Q02 = STAGE279_RUN279B / "payloads" / "run279B_cp277D_breakout_q02_payload.parquet"
SOURCE_Q03 = STAGE279_RUN279B / "payloads" / "run279B_cp277D_breakout_q03_payload.parquet"
STAGE282_REVIEW = ROOT / "stages" / "282_onnx_candidate_campaign__validation_first_asymmetric_confirmation_rebuild" / "02_runs" / "run282C"
STAGE282_SCOREBOARD = STAGE282_REVIEW / "stability_scoreboard.csv"
STAGE282_TRADE_QUALITY = STAGE282_REVIEW / "trade_quality_summary.csv"
STAGE282_CURVE = STAGE282_REVIEW / "curve_stability_summary.csv"
STAGE285_FINAL = (
    ROOT
    / "stages"
    / "285_onnx_candidate_campaign__onnx_export_parity_runtime_reproduction_cp282d"
    / "03_reviews"
    / "run285A_final_candidate_package_report.md"
)

RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
IDEA_REGISTER = ROOT / "docs" / "registers" / "idea_registry.md"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
PRODUCER = Path("stage_pipelines/stage286/design_materialize_trade_density_curve_quality_candidates.py")

BRANCH_COLUMNS = (
    "stage286_branch_id",
    "materialized_branch_id",
    "package_id",
    "experiment_lane",
    "fresh_thesis",
    "source_payload",
    "decision_surface",
    "risk_logic",
    "adapter_path",
    "runtime_handoff",
    "target_trade_density",
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
    "approx_trade_count_max_hold_12",
    "approx_trades_per_day_max_hold_12",
    "trade_density_screen",
)
MANIFEST_COLUMNS = (
    "queue_id",
    "materialized_branch_id",
    "stage286_branch_id",
    "stage279_branch_id",
    "source_branch_id",
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
BASELINE_COLUMNS = (
    "evidence_subject",
    "validation_value",
    "oos_value",
    "stage286_gap",
    "effect",
)
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
    return hashlib.sha256(json.dumps(json_ready(parts), ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()


def as_num(series: pd.Series) -> pd.Series:
    return pd.to_numeric(series, errors="coerce").fillna(0.0)


def sign(series: pd.Series) -> np.ndarray:
    return np.sign(as_num(series)).astype("int8").to_numpy()


def load_payloads() -> tuple[pd.DataFrame, pd.DataFrame]:
    q02 = pd.read_parquet(io_path(SOURCE_Q02)).copy()
    q03 = pd.read_parquet(io_path(SOURCE_Q03)).copy()
    q02["timestamp"] = pd.to_datetime(q02["timestamp"], utc=True)
    q03["timestamp"] = pd.to_datetime(q03["timestamp"], utc=True)
    if len(q02) != len(q03) or not q02["timestamp"].equals(q03["timestamp"]):
        raise RuntimeError("source payload mismatch(원천 페이로드 불일치)")
    return q02, q03


def branch_specs() -> list[dict[str, Any]]:
    return [
        {
            "stage286_branch_id": "run286A_cp286A_entry_dense_direct",
            "materialized_branch_id": "run286A_cp286A_entry_dense_direct",
            "package_id": "cp286A_entry_dense_direct_surface",
            "experiment_lane": "defensive_density_floor(방어형 밀도 하한)",
            "source_payload": "run279B_cp277D_breakout_q02",
            "fresh_thesis": "Use the older entry_signal(진입 신호) as dense supply, then judge whether profit scale rises before any Adapter(어댑터) work.",
            "decision_surface": "route_signal=entry_signal when candidate score and volatility stay inside broad risk bounds.",
            "risk_logic": "Keep cp282D-like hold behavior in the first probe, using density as the changed variable.",
            "adapter_path": "deferred_until_trade_density_curve_quality_passes",
            "runtime_handoff": "single discrete route_signal_value -1/0/+1 table through MT5 replay",
            "target_trade_density": "near lower bound, expected around 3.4 trades/day with max_hold 12; useful as floor control.",
            "success_criteria": "Beats cp282D net scale without creating a local curve pocket and can be retested with shorter hold if close to 4 trades/day.",
            "failure_criteria": "Trade density remains below 4 trades/day or net/PF decays versus cp282D.",
        },
        {
            "stage286_branch_id": "run286A_cp286B_trend_density_thr58",
            "materialized_branch_id": "run286A_cp286B_trend_density_thr58",
            "package_id": "cp286B_trend_density_thr58_surface",
            "experiment_lane": "defensive_target_density(방어형 목표 밀도)",
            "source_payload": "run279B_cp277D_breakout_q02",
            "fresh_thesis": "A majority trend surface can reach 4-6 trades/day while avoiding the sparse cp282D profit ceiling.",
            "decision_surface": "route_signal=sign(di_spread + ema_diff + rsi_slope) when score>=0.58 and volatility/zscore are bounded.",
            "risk_logic": "Trade density is capped by score threshold and normal volatility, not by narrow repair filters.",
            "adapter_path": "deferred_until_trade_density_curve_quality_passes",
            "runtime_handoff": "single discrete route_signal_value -1/0/+1 table through MT5 replay",
            "target_trade_density": "4-6 trades/day in validation and OOS.",
            "success_criteria": "Validation and OOS actual routed totals both land in 4-10 trades/day with larger net and tolerable local curve shape.",
            "failure_criteria": "PF survives but net remains too small, or curve gain comes from one burst.",
        },
        {
            "stage286_branch_id": "run286A_cp286C_trend_density_thr52",
            "materialized_branch_id": "run286A_cp286C_trend_density_thr52",
            "package_id": "cp286C_trend_density_thr52_surface",
            "experiment_lane": "balanced_density_scale(균형형 밀도/규모)",
            "source_payload": "run279B_cp277D_breakout_q02",
            "fresh_thesis": "Lowering the trend confidence threshold can move the surface toward 6-8 trades/day while preserving enough directional structure.",
            "decision_surface": "route_signal=majority trend when score>=0.52, volatility is normal, and return zscore is not extreme.",
            "risk_logic": "Scale is allowed, but the next review rejects deep monthly/session/local equity pockets.",
            "adapter_path": "deferred_until_trade_density_curve_quality_passes",
            "runtime_handoff": "single discrete route_signal_value -1/0/+1 table through MT5 replay",
            "target_trade_density": "6-8 trades/day in validation and OOS.",
            "success_criteria": "Net scale improves clearly over cp282D with PF/recovery not collapsing and no deep local pocket.",
            "failure_criteria": "Trade count is right but expectancy turns flat or drawdown consumes the extra profit.",
        },
        {
            "stage286_branch_id": "run286A_cp286D_trend_density_thr48",
            "materialized_branch_id": "run286A_cp286D_trend_density_thr48",
            "package_id": "cp286D_trend_density_thr48_surface",
            "experiment_lane": "aggressive_density_upper_band(공격형 밀도 상단)",
            "source_payload": "run279B_cp277D_breakout_q02",
            "fresh_thesis": "An aggressive trend threshold near the upper density band can test whether profit scale exists before curve filters are added.",
            "decision_surface": "route_signal=majority trend when score>=0.48 with broad volatility and zscore bounds.",
            "risk_logic": "Upside is allowed; failure is accepted if local drawdown pockets or overtrading dominate.",
            "adapter_path": "deferred_until_trade_density_curve_quality_passes",
            "runtime_handoff": "single discrete route_signal_value -1/0/+1 table through MT5 replay",
            "target_trade_density": "8-10 trades/day in validation and OOS.",
            "success_criteria": "Profit scale expands without leaving the 4-10 trades/day band and without catastrophic curve holes.",
            "failure_criteria": "Overtrading, PF collapse, or deep local curve pocket.",
        },
        {
            "stage286_branch_id": "run286A_cp286E_macro_blend_density",
            "materialized_branch_id": "run286A_cp286E_macro_blend_density",
            "package_id": "cp286E_macro_blend_density_surface",
            "experiment_lane": "structural_blend_density(구조 혼합 밀도)",
            "source_payload": "run279B_cp277D_breakout_q02_q03_blend",
            "fresh_thesis": "A macro/trend fallback blend can keep target density while reducing one-sided trend damage.",
            "decision_surface": "route_signal uses entry, trend, and macro agreement fallback under score>=0.48 and bounded volatility.",
            "risk_logic": "Macro confirmation is construction logic, not a late filter; curve review decides survival.",
            "adapter_path": "deferred_until_trade_density_curve_quality_passes",
            "runtime_handoff": "single discrete route_signal_value -1/0/+1 table through MT5 replay",
            "target_trade_density": "6-8 trades/day in validation and OOS.",
            "success_criteria": "Keeps target trade density and improves local curve smoothness versus pure trend variants.",
            "failure_criteria": "Duplicate of cp286C/D behavior or lower net scale without curve benefit.",
        },
    ]


def approximate_trades(signal: np.ndarray, max_hold_bars: int = 12) -> int:
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


def build_signal(q02: pd.DataFrame, q03: pd.DataFrame, spec: Mapping[str, Any]) -> np.ndarray:
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
    branch_id = str(spec["materialized_branch_id"])
    if branch_id.endswith("cp286A_entry_dense_direct"):
        mask = (entry != 0) & (score >= 0.42) & (vol >= 0.35) & (vol <= 1.75)
        return np.where(mask, entry, 0).astype("int8")
    if branch_id.endswith("cp286B_trend_density_thr58"):
        mask = (trend != 0) & (score >= 0.58) & (vol >= 0.45) & (vol <= 1.65) & (z_abs <= 2.0)
        return np.where(mask, trend, 0).astype("int8")
    if branch_id.endswith("cp286C_trend_density_thr52"):
        mask = (trend != 0) & (score >= 0.52) & (vol >= 0.45) & (vol <= 1.65) & (z_abs <= 2.0)
        return np.where(mask, trend, 0).astype("int8")
    if branch_id.endswith("cp286D_trend_density_thr48"):
        mask = (trend != 0) & (score >= 0.48) & (vol >= 0.45) & (vol <= 1.65) & (z_abs <= 2.0)
        return np.where(mask, trend, 0).astype("int8")
    if branch_id.endswith("cp286E_macro_blend_density"):
        agreed = ((macro == fallback) & (macro != 0)) | (di == fallback) | (ema == fallback)
        mask = (fallback != 0) & (score >= 0.48) & agreed & (vol >= 0.45) & (vol <= 1.65) & (z_abs <= 1.8)
        q03_dir = as_num(q03["direction_signal_value"]).astype("int8").to_numpy()
        blend = np.where((q03_dir != 0) & (di == q03_dir), q03_dir, fallback).astype("int8")
        return np.where(mask, blend, 0).astype("int8")
    raise ValueError(branch_id)


def signal_label(value: int) -> str:
    return "long" if value > 0 else "short" if value < 0 else "flat"


def signal_counts(frame: pd.DataFrame, signal_col: str = "route_signal_value") -> dict[tuple[str, str], dict[str, Any]]:
    rows: dict[tuple[str, str], dict[str, Any]] = {}
    for (tier, split), group in frame.groupby(["tier_scope", "split"], sort=False):
        if split not in {"validation", "oos"}:
            continue
        signal = pd.to_numeric(group[signal_col], errors="coerce").fillna(0).astype("int8").to_numpy()
        days = int(pd.to_datetime(group["timestamp"], utc=True).dt.date.nunique())
        approx = approximate_trades(signal)
        rows[(str(tier), str(split))] = {
            "days": days,
            "rows": int(len(group)),
            "active_signal_count": int((signal != 0).sum()),
            "active_signals_per_day": float((signal != 0).sum() / days) if days else 0.0,
            "long_signal_count": int((signal == 1).sum()),
            "short_signal_count": int((signal == -1).sum()),
            "approx_trade_count_max_hold_12": approx,
            "approx_trades_per_day_max_hold_12": float(approx / days) if days else 0.0,
        }
    return rows


def export_signal_csv(frame: pd.DataFrame, path: Path, tier_scope: str) -> Path:
    columns = ["timestamp", "split", "tier_scope", "route_signal_value", "route_signal_label"]
    export = frame.loc[frame["tier_scope"].astype(str).eq(tier_scope), columns].copy()
    export["timestamp"] = pd.to_datetime(export["timestamp"], utc=True).dt.strftime("%Y-%m-%d %H:%M:%S")
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    export.to_csv(io_path(path), index=False, lineterminator="\n", encoding="utf-8")
    return path


def materialize() -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[Path]]:
    q02, q03 = load_payloads()
    branch_rows: list[dict[str, Any]] = []
    supply_rows: list[dict[str, Any]] = []
    manifest_rows: list[dict[str, Any]] = []
    artifacts: list[Path] = []
    for index, spec in enumerate(branch_specs(), start=1):
        signal = build_signal(q02, q03, spec)
        payload = q02.copy()
        payload["package_id"] = spec["package_id"]
        payload["stage286_branch_id"] = spec["stage286_branch_id"]
        payload["materialized_branch_id"] = spec["materialized_branch_id"]
        payload["queue_role"] = spec["experiment_lane"]
        payload["fresh_thesis"] = spec["fresh_thesis"]
        payload["route_policy"] = spec["decision_surface"]
        payload["signal_policy"] = "stage286_trade_density_curve_quality_route_signal"
        payload["route_signal_value"] = signal
        payload["route_signal_label"] = [signal_label(int(value)) for value in signal]
        payload["signal_active"] = (signal != 0).astype("int8")
        payload["runtime_handoff_status"] = "materialized_for_run286B_mt5_probe"
        payload["payload_claim_boundary"] = BOUNDARY
        direction_hash = surface_hash(
            {
                "package_id": spec["package_id"],
                "decision_surface": spec["decision_surface"],
                "risk_logic": spec["risk_logic"],
                "source_payload": spec["source_payload"],
            }
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
                "feature_surface": [
                    "candidate_decision_score",
                    "historical_vol_5_over_20",
                    "return_zscore_20",
                    "di_spread_14",
                    "ema20_ema50_diff",
                    "rsi_14_slope_3",
                    "us100_minus_mega8_equal_return_1",
                    "us100_minus_top3_weighted_return_1",
                ],
                "selected_candidate": "none",
                "adapter_package": "none",
                "onnx_readiness": "not_claimed",
                "claim_boundary": BOUNDARY,
            },
        )
        tier_a_signal = export_signal_csv(payload, MT5_HANDOFF_DIR / f'{spec["materialized_branch_id"]}_tier_a_signal.csv', "Tier A")
        tier_b_signal = export_signal_csv(payload, MT5_HANDOFF_DIR / f'{spec["materialized_branch_id"]}_tier_b_signal.csv', "Tier B")
        routed_signal = export_signal_csv(payload, MT5_HANDOFF_DIR / f'{spec["materialized_branch_id"]}_actual_routed_signal.csv', "Tier A")
        counts = signal_counts(payload)
        for (tier, split), count_row in counts.items():
            per_day = float(count_row["approx_trades_per_day_max_hold_12"])
            supply_rows.append(
                {
                    "materialized_branch_id": spec["materialized_branch_id"],
                    "package_id": spec["package_id"],
                    "tier_scope": tier,
                    "split": split,
                    **count_row,
                    "trade_density_screen": "in_target_band" if 4.0 <= per_day <= 10.0 else "outside_target_band",
                }
            )
        tier_a_val = counts.get(("Tier A", "validation"), {})
        tier_a_oos = counts.get(("Tier A", "oos"), {})
        tier_b_val = counts.get(("Tier B", "validation"), {})
        tier_b_oos = counts.get(("Tier B", "oos"), {})
        manifest_rows.append(
            {
                "queue_id": f"run286A_queue_{index:02d}",
                "materialized_branch_id": spec["materialized_branch_id"],
                "stage286_branch_id": spec["stage286_branch_id"],
                "stage279_branch_id": payload["stage279_branch_id"].astype(str).iloc[0],
                "source_branch_id": payload["source_branch_id"].astype(str).iloc[0],
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
                "tier_a_validation_signal_count": tier_a_val.get("active_signal_count", 0),
                "tier_a_oos_signal_count": tier_a_oos.get("active_signal_count", 0),
                "tier_b_validation_signal_count": tier_b_val.get("active_signal_count", 0),
                "tier_b_oos_signal_count": tier_b_oos.get("active_signal_count", 0),
                "actual_routed_validation_signal_count": tier_a_val.get("active_signal_count", 0),
                "actual_routed_oos_signal_count": tier_a_oos.get("active_signal_count", 0),
                "approx_validation_trades_per_day": tier_a_val.get("approx_trades_per_day_max_hold_12", 0),
                "approx_oos_trades_per_day": tier_a_oos.get("approx_trades_per_day_max_hold_12", 0),
                "selected_candidate": "none",
                "adapter_package": "none",
                "onnx_readiness": "not_claimed",
                "claim_boundary": BOUNDARY,
            }
        )
        branch_rows.append({**spec, "claim_boundary": BOUNDARY})
        artifacts.extend([payload_path, handoff_path, tier_a_signal, tier_b_signal, routed_signal])
    return branch_rows, supply_rows, manifest_rows, artifacts


def baseline_gap_rows() -> list[dict[str, Any]]:
    trade_rows = [
        row
        for row in read_csv_dicts(STAGE282_TRADE_QUALITY)
        if row.get("materialized_branch_id") == "run282A_cp282D_macro_trend_countercheck"
        and row.get("tier_scope") == "Tier A+B"
    ]
    curve_rows = [
        row
        for row in read_csv_dicts(STAGE282_CURVE)
        if row.get("materialized_branch_id") == "run282A_cp282D_macro_trend_countercheck"
        and row.get("tier_scope") == "Tier A+B"
    ]
    by_split = {row["split"]: row for row in trade_rows}
    curve_by_split = {row["split"]: row for row in curve_rows}
    val_days = 183
    oos_days = 131
    return [
        {
            "evidence_subject": "cp282D net_profit(순수익)",
            "validation_value": by_split.get("validation_is", {}).get("net_profit", ""),
            "oos_value": by_split.get("oos", {}).get("net_profit", ""),
            "stage286_gap": "Net scale is too small for the new goal.",
            "effect": "Stage286 treats cp282D as reference evidence only.",
        },
        {
            "evidence_subject": "cp282D trade_density(거래 밀도)",
            "validation_value": f"{float(by_split.get('validation_is', {}).get('trade_count', 0) or 0) / val_days:.3f}",
            "oos_value": f"{float(by_split.get('oos', {}).get('trade_count', 0) or 0) / oos_days:.3f}",
            "stage286_gap": "Below required 4-10 trades/day.",
            "effect": "New candidate construction starts before Adapter(어댑터) work.",
        },
        {
            "evidence_subject": "cp282D recovery_factor(회복 계수)",
            "validation_value": curve_by_split.get("validation_is", {}).get("recovery_factor", ""),
            "oos_value": curve_by_split.get("oos", {}).get("recovery_factor", ""),
            "stage286_gap": "Validation recovery is weak relative to required smooth curve.",
            "effect": "Curve pocket review becomes a hard review gate after run286B.",
        },
    ]


def requirement_contract() -> dict[str, Any]:
    return {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "goal_contract": {
            "minimum_trade_count": "must be enough to support 4-10 trades/day in validation and OOS actual routed totals",
            "trade_density": "4-10 trades/day",
            "curve_shape": "balance/equity curve must remain steadily rising in total and zoomed segments without deep local pockets",
            "profit_scale": "must clearly improve over cp282D reference net profit while keeping PF, drawdown, recovery, and expectancy jointly credible",
            "research_scope": "unrestricted model, feature, decision, and risk changes; no narrow repair loop",
            "handoff_gate": "Adapter and ONNX only after trade density, profit scale, and curve quality survive MT5 review",
        },
        "reference_only_inputs": [rel(STAGE285_FINAL), rel(STAGE282_TRADE_QUALITY), rel(STAGE282_CURVE), rel(SOURCE_Q02), rel(SOURCE_Q03)],
        "claim_boundary": BOUNDARY,
    }


def report_markdown(manifest_rows: Sequence[Mapping[str, Any]], supply_rows: Sequence[Mapping[str, Any]]) -> str:
    in_band = [
        row
        for row in supply_rows
        if row.get("tier_scope") == "Tier A"
        and row.get("split") in {"validation", "oos"}
        and row.get("trade_density_screen") == "in_target_band"
    ]
    return f"""# run286A Trade Density Curve Quality Materialization(286A 거래 밀도/곡선 품질 물질화)

- stage_id(단계 ID): `{STAGE_ID}`
- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- branch_count(분기 수): `{len(manifest_rows)}`
- supply_rows(공급 행): `{len(supply_rows)}`
- target_band_rows(목표 범위 행): `{len(in_band)}`
- selected_candidate(선택 후보): `none`
- Adapter package(어댑터 패키지): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- next_action(다음 행동): `{NEXT_ACTION}`

## Fresh Thesis(새 논제)

Stage286(286단계)는 cp282D(282D 후보)의 ONNX(온엑스) 기술 성공을 보존하지 않는다.
Effect(효과): 새 후보는 먼저 4-10 trades/day(일 4-10거래), 순수익 규모, 확대 구간 곡선 품질을 만족해야 한다.

## Candidate Queue(후보 대기열)

{chr(10).join(f"- `{row['package_id']}`: validation approx(검증 근사) `{float(row['approx_validation_trades_per_day']):.2f}` trades/day(일 거래), OOS approx(표본외 근사) `{float(row['approx_oos_trades_per_day']):.2f}` trades/day(일 거래)." for row in manifest_rows)}

## Boundary(경계)

`{BOUNDARY}`

Effect(효과): 이 실행은 MT5(메타트레이더5) 압박 입력을 만든 것이며 후보 선택, Adapter(어댑터), ONNX(온엑스) 진행은 주장하지 않는다.
"""


def write_stage_open_docs() -> None:
    write_md(
        SPEC,
        f"""# Stage286 Trade Density Curve Quality Rebuild(286단계 거래 밀도/곡선 품질 재구성)

- canonical_stage_id(정식 단계 ID): `{STAGE_ID}`
- big_question(큰 질문): 4-10 trades/day(일 4-10거래), 순수익 규모, 확대 구간 곡선 품질을 동시에 만족하는 ONNX-worthy candidate(온엑스 가치 후보)를 새로 만들 수 있는가?
- source_boundary(원천 경계): Stage285(285단계) cp282D(282D 후보)는 reference evidence(참고 근거)로만 쓴다.
- selected_candidate(선택 후보): `none`
- Adapter package(어댑터 패키지): `none`
- ONNX readiness(온엑스 준비): `not_started`

Effect(효과): Adapter(어댑터) 개발 전으로 돌아가 거래 밀도, 순수익 규모, 곡선 품질이 먼저 살아남는 후보만 다음 단계로 넘긴다.
""",
    )
    write_md(
        INPUT_REFS,
        f"""# Stage286 Input Refs(286단계 입력 참조)

- cp282D final package report(cp282D 최종 패키지 보고): `{rel(STAGE285_FINAL)}`
- Stage282 trade quality(Stage282 거래 품질): `{rel(STAGE282_TRADE_QUALITY)}`
- Stage282 curve stability(Stage282 곡선 안정성): `{rel(STAGE282_CURVE)}`
- Source q02 payload(원천 q02 페이로드): `{rel(SOURCE_Q02)}`
- Source q03 payload(원천 q03 페이로드): `{rel(SOURCE_Q03)}`

Effect(효과): 이전 stage(단계)를 참고하지만 후보명이나 ONNX(온엑스) 패키지를 고정 시작점으로 삼지 않는다.
""",
    )
    write_md(
        SELECTED,
        f"""# Stage286 Selection Status(286단계 선택 상태)

- stage_status(단계 상태): `{STATUS}`
- current_packet(현재 작업 묶음): `stage286_trade_density_curve_quality_rebuild_v1`
- current_run(현재 실행): `{RUN_ID}`
- source_stage(원천 단계): `285_onnx_candidate_campaign__onnx_export_parity_runtime_reproduction_cp282d`
- selected_candidate(선택 후보): `none`
- Adapter package(어댑터 패키지): `none`
- ONNX readiness(온엑스 준비): `not_started`
- Goal Achieve(목표 달성): `not_claimed`
- target_trade_density(목표 거래 밀도): `4-10 trades/day(일 4-10거래)`
- next_action(다음 행동): `{NEXT_ACTION}`
- input_refs(입력 참조): `{rel(INPUT_REFS)}`
""",
    )


def write_outputs(
    branch_rows: Sequence[Mapping[str, Any]],
    supply_rows: Sequence[Mapping[str, Any]],
    manifest_rows: Sequence[Mapping[str, Any]],
    payload_artifacts: Sequence[Path],
    created_at: str,
) -> list[Path]:
    write_stage_open_docs()
    write_json(REQUIREMENT_CONTRACT, requirement_contract())
    write_csv(BASELINE_ATTRIBUTION, BASELINE_COLUMNS, baseline_gap_rows())
    write_csv(BRANCH_QUEUE, BRANCH_COLUMNS, branch_rows)
    write_csv(CANDIDATE_SUPPLY, SUPPLY_COLUMNS, supply_rows)
    write_csv(PAYLOAD_MANIFEST, MANIFEST_COLUMNS, manifest_rows)
    write_csv(MT5_QUEUE, MANIFEST_COLUMNS, manifest_rows)
    write_json(
        DESIGN_RECEIPT,
        {
            "run_id": RUN_ID,
            "fresh_thesis": "trade_density_curve_quality_first_candidate_construction",
            "hypothesis": "Dense but bounded route_signal surfaces can expose profit scale before Adapter/ONNX work.",
            "comparison": "cp282D reference metrics only",
            "controls": ["same source payload family", "same first MT5 replay backend", "same max_hold_bars 12 in run286B"],
            "changed_variables": ["decision surface", "signal density", "feature combination"],
            "stop_conditions": [
                "actual routed trade density outside 4-10 trades/day",
                "profit scale fails to improve over cp282D",
                "curve has deep local pocket after review",
            ],
            "claim_boundary": BOUNDARY,
        },
    )
    write_json(
        DATA_RECEIPT,
        {
            "source_rows_q02": len(pd.read_parquet(io_path(SOURCE_Q02))),
            "source_rows_q03": len(pd.read_parquet(io_path(SOURCE_Q03))),
            "label_or_future_columns_added": False,
            "tier_pairing": "Tier A and Tier B materialized in same work packet",
            "claim_boundary": BOUNDARY,
        },
    )
    write_csv(
        RESULT_JUDGMENT,
        RESULT_COLUMNS,
        [
            {
                "result_subject": "run286A_materialized_candidate_inputs",
                "evidence_available": rel(PAYLOAD_MANIFEST),
                "evidence_missing": "MT5 runtime KPI and curve review",
                "judgment_label": JUDGMENT,
                "judgment_class": "inconclusive_until_mt5_probe",
                "claim_boundary": BOUNDARY,
                "next_condition": NEXT_ACTION,
                "user_explanation_hook": "거래 밀도 후보를 만들었지만 아직 성과 후보는 아니다.",
            }
        ],
    )
    write_csv(
        GATE_AUDIT,
        GATE_COLUMNS,
        [
            {
                "gate_name": "fresh_thesis(새 논제)",
                "status": "passed",
                "evidence_path": rel(DESIGN_RECEIPT),
                "effect": "거래 밀도와 곡선 품질을 첫 목표로 둔다.",
            },
            {
                "gate_name": "reference_only_cp282d(cp282D 참고 전용)",
                "status": "passed",
                "evidence_path": rel(BASELINE_ATTRIBUTION),
                "effect": "기존 ONNX(온엑스)를 새 후보로 착각하지 않는다.",
            },
            {
                "gate_name": "no_candidate_no_adapter_no_onnx_claim(후보/어댑터/온엑스 주장 없음)",
                "status": "passed",
                "evidence_path": rel(RESULT_JUDGMENT),
                "effect": "MT5(메타트레이더5) 전 성과 주장을 막는다.",
            },
        ],
    )
    write_md(REPORT, report_markdown(manifest_rows, supply_rows))
    artifacts = [
        SPEC,
        INPUT_REFS,
        REQUIREMENT_CONTRACT,
        BASELINE_ATTRIBUTION,
        BRANCH_QUEUE,
        CANDIDATE_SUPPLY,
        PAYLOAD_MANIFEST,
        MT5_QUEUE,
        DESIGN_RECEIPT,
        DATA_RECEIPT,
        RESULT_JUDGMENT,
        GATE_AUDIT,
        REPORT,
        SELECTED,
        *payload_artifacts,
    ]
    write_json(
        LINEAGE,
        {
            "run_id": RUN_ID,
            "producer": PRODUCER.as_posix(),
            "source_artifacts": [rel(STAGE285_FINAL), rel(STAGE282_TRADE_QUALITY), rel(STAGE282_CURVE), rel(SOURCE_Q02), rel(SOURCE_Q03)],
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


def update_registers_and_docs(created_at: str, artifacts: Sequence[Path], manifest_rows: Sequence[Mapping[str, Any]]) -> None:
    upsert_csv_rows(
        RUN_REGISTRY,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "onnx_candidate_campaign_trade_density_curve_quality",
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
                "ledger_row_id": f"{RUN_ID}__trade_density_materialization",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": "run286A",
                "parent_run_id": SOURCE_RUN_ID,
                "record_view": "candidate_supply_diagnostics",
                "tier_scope": "Tier A/Tier B/Tier A+B",
                "kpi_scope": "structural_scout",
                "scoreboard_lane": "trade_density_curve_quality_first",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT),
                "primary_kpi": f"mt5_queue_rows={len(manifest_rows)}",
                "guardrail_kpi": "no_candidate_no_adapter_no_onnx_claim",
                "external_verification_status": "not_attempted_run286A_materialization",
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
                "view": "candidate_supply_diagnostics",
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
            "artifact_type": "stage286_trade_density_materialization_artifact",
            "path": rel(path),
            "sha256": sha256_file(path),
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": created_at,
            "notes": "run286A trade density candidate materialization(286A 거래 밀도 후보 물질화)",
        }
        for path in artifacts
        if path_exists(path)
    ]
    upsert_csv_rows(ARTIFACT_REGISTRY, ARTIFACT_COLUMNS, artifact_rows, key="artifact_id")

    review_index = io_path(REVIEW_INDEX).read_text(encoding="utf-8-sig") if path_exists(REVIEW_INDEX) else "# Stage286 Review Index(286단계 검토 색인)\n"
    review_index = append_once(review_index, "run286A_report", f"- run286A_report(286A 보고서): `{rel(REPORT)}`")
    write_md(REVIEW_INDEX, review_index)

    current = io_path(CURRENT_STATE).read_text(encoding="utf-8-sig")
    current = replace_line_prefix(current, "- current_packet(현재 작업 묶음):", "- current_packet(현재 작업 묶음): `stage286_trade_density_curve_quality_rebuild_v1`")
    current = replace_line_prefix(current, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_line_prefix(current, "- active_stage(활성 단계):", f"- active_stage(활성 단계): `{STAGE_ID}`")
    current = replace_line_prefix(current, "- source_stage(원천 단계):", "- source_stage(원천 단계): `285_onnx_candidate_campaign__onnx_export_parity_runtime_reproduction_cp282d`")
    current = replace_line_prefix(current, "- status(상태):", f"- status(상태): `{STATUS}`")
    current = replace_line_prefix(current, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    current = replace_line_prefix(current, "- claim_boundary(주장 경계):", f"- claim_boundary(주장 경계): `{BOUNDARY}`")
    current = append_once(
        current,
        "run286A_summary",
        f"- run286A_summary(286A 요약): trade density/curve quality first(거래 밀도/곡선 품질 우선) 후보 `{len(manifest_rows)}`개를 물질화했다. Effect(효과): 4-10 trades/day(일 4-10거래)에 닿는지 MT5(메타트레이더5)로 검증할 수 있고 selected candidate(선택 후보), Adapter package(어댑터 패키지), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 주장하지 않는다.",
    )
    write_md(CURRENT_STATE, current)

    workspace = io_path(WORKSPACE_STATE).read_text(encoding="utf-8-sig")
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    workspace = replace_line_prefix(workspace, "updated_on:", f"updated_on: '{UPDATED_ON}'")
    workspace = replace_line_prefix(workspace, "active_stage:", f"active_stage: {STAGE_ID}")
    focus = (
        f"- >-\n"
        f"  Stage286(286단계) run286A(286A 실행) trade density/curve quality candidate materialization(거래 밀도/곡선 품질 후보 물질화) `{RUN_ID}`. "
        f"Effect(효과): cp282D(282D 후보)는 reference evidence(참고 근거)로 낮추고 `{len(manifest_rows)}`개 후보를 MT5 probe(MT5 탐침) 대기열로 넘기며 후보/어댑터/온엑스 주장은 하지 않는다.\n"
    )
    workspace = prepend_focus(workspace, focus, RUN_ID)
    write_md(WORKSPACE_STATE, workspace)

    changelog = io_path(CHANGELOG).read_text(encoding="utf-8-sig")
    changelog = append_once(
        changelog,
        RUN_ID,
        f"## {UPDATED_ON} run286A Trade density candidate materialization(286A 거래 밀도 후보 물질화)\n\n- status(상태): `{STATUS}`\n- judgment(판정): `{JUDGMENT}`\n- effect(효과): Stage286(286단계)를 열고 후보 `{len(manifest_rows)}`개를 MT5 probe queue(MT5 탐침 대기열)로 만들었다.\n- boundary(경계): selected candidate(선택 후보), Adapter package(어댑터 패키지), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 `none/not_claimed`다.\n",
    )
    write_md(CHANGELOG, changelog)

    idea = io_path(IDEA_REGISTER).read_text(encoding="utf-8-sig")
    idea = append_once(
        idea,
        "IDEA-ST286-RUN286A-TRADE-DENSITY-CURVE-QUALITY",
        f"| `IDEA-ST286-RUN286A-TRADE-DENSITY-CURVE-QUALITY` | `{STAGE_ID}` | trade density/curve quality first(거래 밀도/곡선 품질 우선) 후보 `{len(manifest_rows)}`개 | `Tier A used + Tier B fallback stress + actual routed total` | `materialized_no_candidate` | 4-10 trades/day(일 4-10거래)와 순수익 규모를 먼저 맞춘 뒤 Adapter/ONNX(어댑터/온엑스)로 넘긴다. |",
    )
    write_md(IDEA_REGISTER, idea)


def main() -> None:
    for path in [STAGE_ROOT, SPEC.parent, INPUTS, RUN_ROOT, PAYLOAD_DIR, HANDOFF_DIR, MT5_HANDOFF_DIR, REVIEWS, SELECTED.parent]:
        io_path(path).mkdir(parents=True, exist_ok=True)
    created_at = utc_now()
    branch_rows, supply_rows, manifest_rows, payload_artifacts = materialize()
    artifacts = write_outputs(branch_rows, supply_rows, manifest_rows, payload_artifacts, created_at)
    update_registers_and_docs(created_at, artifacts, manifest_rows)
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
