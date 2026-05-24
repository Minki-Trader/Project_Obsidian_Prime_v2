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
    write_csv_rows,
)
from foundation.models.onnx_bridge import ordered_hash  # noqa: E402


STAGE_ID = "288_onnx_candidate_campaign__risk_reward_exit_asymmetry_rebuild"
RUN_ID = "run288A_design_materialize_risk_reward_exit_asymmetry_candidates_v1"
RUN_NUMBER = "run288A"
SOURCE_RUN_ID = "run287C_review_density_scale_curve_pocket_mt5_probe_v1"
STATUS = "completed_risk_reward_exit_asymmetry_candidates_materialized_no_selection"
JUDGMENT = "risk_reward_exit_candidate_inputs_materialized_no_candidate_selection"
NEXT_ACTION = "run288B_execute_risk_reward_exit_asymmetry_mt5_probe"
UPDATED_ON = "2026-05-24"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_"
    "no_deployment_no_onnx_until_candidate_package_gate"
)
FEATURE_ORDER = (
    "run288b_route_signal",
    "exit_close_long_flag",
    "exit_close_short_flag",
    "exit_max_hold_bars",
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

SOURCE_E = ROOT / "stages/287_onnx_candidate_campaign__density_scale_curve_pocket_rebuild/02_runs/run287A/payloads/run287A_cp287E_consensus_pullback_mix_payload.parquet"
SOURCE_B = ROOT / "stages/287_onnx_candidate_campaign__density_scale_curve_pocket_rebuild/02_runs/run287A/payloads/run287A_cp287B_volnorm_pressure_release_payload.parquet"
SEED_QUEUE = INPUTS / "stage288_risk_reward_exit_seed_queue.csv"
INPUT_REFS = INPUTS / "input_refs.md"

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
REPORT = REVIEWS / "run288A_risk_reward_exit_asymmetry_materialization_report.md"

RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
PRODUCER = Path("stage_pipelines/stage288/design_materialize_risk_reward_exit_asymmetry_candidates.py")

BRANCH_COLUMNS = (
    "stage288_branch_id",
    "materialized_branch_id",
    "package_id",
    "source_seed",
    "fresh_thesis",
    "decision_surface",
    "risk_logic",
    "max_hold_bars",
    "close_on_flat_signal",
    "atr_sltp_enabled",
    "atr_stop_multiplier",
    "atr_take_profit_multiplier",
    "exit_risk_overlay_enabled",
    "model_risk_sizing_enabled",
    "feature_order",
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
    "stage288_branch_id",
    "package_id",
    "queue_role",
    "payload_path",
    "payload_hash",
    "handoff_path",
    "handoff_hash",
    "feature_order",
    "feature_order_hash",
    "max_hold_bars",
    "close_on_flat_signal",
    "same_direction_reentry_cooldown_bars",
    "atr_sltp_enabled",
    "atr_period",
    "atr_stop_multiplier",
    "atr_take_profit_multiplier",
    "atr_min_stop_points",
    "atr_max_stop_points",
    "atr_min_take_profit_points",
    "atr_max_take_profit_points",
    "exit_risk_overlay_enabled",
    "exit_risk_close_long_feature_index",
    "exit_risk_close_short_feature_index",
    "exit_risk_close_threshold",
    "exit_risk_min_hold_bars",
    "exit_risk_max_hold_feature_index",
    "model_risk_sizing_enabled",
    "model_risk_min_pct",
    "model_risk_max_pct",
    "model_risk_confidence_floor",
    "model_risk_confidence_ceiling",
    "model_risk_fallback_lot",
    "approx_validation_trades_per_day",
    "approx_oos_trades_per_day",
    "selected_candidate",
    "adapter_package",
    "onnx_readiness",
    "claim_boundary",
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
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> None:
    write_csv_rows(path, columns, rows)


def read_csv_dicts(path: Path) -> list[dict[str, str]]:
    if not path_exists(path):
        return []
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def upsert_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]], key: str) -> None:
    existing = read_csv_dicts(path)
    new_keys = {str(row.get(key, "")).strip() for row in rows}
    merged = [row for row in existing if str(row.get(key, "")).strip() not in new_keys]
    merged.extend(dict(row) for row in rows)
    write_csv(path, columns, merged)


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


def as_num(series: pd.Series) -> pd.Series:
    return pd.to_numeric(series, errors="coerce").fillna(0.0)


def sign(series: pd.Series) -> np.ndarray:
    return np.sign(as_num(series)).astype("int8").to_numpy()


def load_sources() -> dict[str, pd.DataFrame]:
    e = pd.read_parquet(io_path(SOURCE_E)).copy()
    b = pd.read_parquet(io_path(SOURCE_B)).copy()
    for frame in (e, b):
        frame["timestamp"] = pd.to_datetime(frame["timestamp"], utc=True)
    return {"cp287E": e, "cp287B": b}


def branch_specs() -> list[dict[str, Any]]:
    return [
        {
            "stage288_branch_id": "run288A_cp288A_scale_rr18_atr",
            "materialized_branch_id": "run288A_cp288A_scale_rr18_atr",
            "package_id": "cp288A_scale_rr18_atr_surface",
            "source_seed": "cp287E",
            "fresh_thesis": "Scale seed(규모 씨앗)에 ATR 1.0/1.8 reward asymmetry(보상 비대칭)를 적용해 PF/recovery(수익 팩터/회복)를 개선한다.",
            "decision_surface": "cp287E route signal(경로 신호) 유지, exit/risk-reward(청산/위험보상)만 변경.",
            "risk_logic": "ATR SL/TP(ATR 손절/익절) stop=1.0 take=1.8, max_hold(최대 보유)=6.",
            "max_hold_bars": 6,
            "close_on_flat_signal": False,
            "same_direction_reentry_cooldown_bars": 0,
            "atr_sltp_enabled": True,
            "atr_stop_multiplier": 1.0,
            "atr_take_profit_multiplier": 1.8,
            "exit_risk_overlay_enabled": False,
            "model_risk_sizing_enabled": False,
        },
        {
            "stage288_branch_id": "run288A_cp288B_scale_tight_rr30",
            "materialized_branch_id": "run288A_cp288B_scale_tight_rr30",
            "package_id": "cp288B_scale_tight_rr30_surface",
            "source_seed": "cp287E",
            "fresh_thesis": "Tighter stop(짧은 손절)과 larger reward(큰 보상)로 손실 포켓을 잘라내고 순수익 규모를 유지한다.",
            "decision_surface": "cp287E route signal(경로 신호) + close_on_flat(평탄 청산).",
            "risk_logic": "ATR stop=0.7 take=2.1, close_on_flat=true, max_hold=6.",
            "max_hold_bars": 6,
            "close_on_flat_signal": True,
            "same_direction_reentry_cooldown_bars": 0,
            "atr_sltp_enabled": True,
            "atr_stop_multiplier": 0.7,
            "atr_take_profit_multiplier": 2.1,
            "exit_risk_overlay_enabled": False,
            "model_risk_sizing_enabled": False,
        },
        {
            "stage288_branch_id": "run288A_cp288C_scale_overlay_rr22",
            "materialized_branch_id": "run288A_cp288C_scale_overlay_rr22",
            "package_id": "cp288C_scale_overlay_rr22_surface",
            "source_seed": "cp287E",
            "fresh_thesis": "Adverse macro/zscore exit overlay(불리한 매크로/z점수 청산 오버레이)가 curve pocket(곡선 포켓)을 줄일 수 있는지 본다.",
            "decision_surface": "cp287E route signal(경로 신호), overlay close flags(청산 플래그), dynamic max hold(동적 최대 보유).",
            "risk_logic": "ATR stop=0.9 take=2.0, exit overlay enabled, min_hold=2.",
            "max_hold_bars": 8,
            "close_on_flat_signal": False,
            "same_direction_reentry_cooldown_bars": 0,
            "atr_sltp_enabled": True,
            "atr_stop_multiplier": 0.9,
            "atr_take_profit_multiplier": 2.0,
            "exit_risk_overlay_enabled": True,
            "model_risk_sizing_enabled": False,
        },
        {
            "stage288_branch_id": "run288A_cp288D_smooth_control_rr24",
            "materialized_branch_id": "run288A_cp288D_smooth_control_rr24",
            "package_id": "cp288D_smooth_control_rr24_surface",
            "source_seed": "cp287B",
            "fresh_thesis": "Smoother control(매끄러운 대조군)에 reward lift(보상 확대)를 주면 4 trades/day(일 거래) 하한과 수익 규모를 되찾을 수 있는지 본다.",
            "decision_surface": "cp287B route signal(경로 신호), max_hold shorter(짧은 최대 보유).",
            "risk_logic": "ATR stop=0.9 take=2.2, close_on_flat=true, max_hold=5.",
            "max_hold_bars": 5,
            "close_on_flat_signal": True,
            "same_direction_reentry_cooldown_bars": 0,
            "atr_sltp_enabled": True,
            "atr_stop_multiplier": 0.9,
            "atr_take_profit_multiplier": 2.2,
            "exit_risk_overlay_enabled": False,
            "model_risk_sizing_enabled": False,
        },
        {
            "stage288_branch_id": "run288A_cp288E_scale_risk_sized_rr20",
            "materialized_branch_id": "run288A_cp288E_scale_risk_sized_rr20",
            "package_id": "cp288E_scale_risk_sized_rr20_surface",
            "source_seed": "cp287E",
            "fresh_thesis": "Model risk sizing(모델 위험 크기)과 ATR reward(ATR 보상)를 결합해 순수익 규모를 키우되 회복력을 확인한다.",
            "decision_surface": "cp287E route signal(경로 신호), high-confidence discrete table(고신뢰 이산 표) risk sizing.",
            "risk_logic": "ATR stop=1.1 take=2.2, model risk sizing min=0.5% max=1.5%.",
            "max_hold_bars": 6,
            "close_on_flat_signal": False,
            "same_direction_reentry_cooldown_bars": 0,
            "atr_sltp_enabled": True,
            "atr_stop_multiplier": 1.1,
            "atr_take_profit_multiplier": 2.2,
            "exit_risk_overlay_enabled": False,
            "model_risk_sizing_enabled": True,
        },
    ]


def signal_label(value: int) -> str:
    return "long" if value > 0 else "short" if value < 0 else "flat"


def approximate_trades(signal: np.ndarray, max_hold_bars: int) -> int:
    trades = 0
    position = 0
    hold = 0
    for value in signal.astype("int8"):
        current = int(value)
        if position == 0:
            if current:
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


def add_exit_features(frame: pd.DataFrame, overlay: bool) -> pd.DataFrame:
    out = frame.copy()
    signal = as_num(out["route_signal_value"]).astype("int8").to_numpy()
    z_abs = as_num(out["return_zscore_20"]).abs().to_numpy()
    vol = as_num(out["historical_vol_5_over_20"]).to_numpy()
    mega = sign(out["us100_minus_mega8_equal_return_1"])
    top3 = sign(out["us100_minus_top3_weighted_return_1"])
    macro = np.where((mega + top3) > 0, 1, np.where((mega + top3) < 0, -1, 0)).astype("int8")
    if overlay:
        close_long = ((macro < 0) & (z_abs >= 1.0)) | ((signal > 0) & (vol >= 1.55) & (z_abs >= 1.45))
        close_short = ((macro > 0) & (z_abs >= 1.0)) | ((signal < 0) & (vol >= 1.55) & (z_abs >= 1.45))
        dyn_hold = np.where(z_abs >= 1.7, 3, np.where(vol >= 1.45, 4, 6))
    else:
        close_long = np.zeros(len(out), dtype=bool)
        close_short = np.zeros(len(out), dtype=bool)
        dyn_hold = np.zeros(len(out), dtype="int8")
    out["exit_close_long_flag"] = close_long.astype("int8")
    out["exit_close_short_flag"] = close_short.astype("int8")
    out["exit_max_hold_bars"] = dyn_hold.astype("int8")
    out[FEATURE_ORDER[0]] = signal
    return out


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


def materialize() -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[Path]]:
    sources = load_sources()
    branch_rows: list[dict[str, Any]] = []
    supply_rows: list[dict[str, Any]] = []
    manifest_rows: list[dict[str, Any]] = []
    artifacts: list[Path] = []
    feature_order_hash = ordered_hash(FEATURE_ORDER)
    for index, spec in enumerate(branch_specs(), start=1):
        payload = add_exit_features(sources[str(spec["source_seed"])], bool(spec["exit_risk_overlay_enabled"]))
        payload["package_id"] = spec["package_id"]
        payload["stage288_branch_id"] = spec["stage288_branch_id"]
        payload["materialized_branch_id"] = spec["materialized_branch_id"]
        payload["queue_role"] = "risk_reward_exit_asymmetry"
        payload["fresh_thesis"] = spec["fresh_thesis"]
        payload["route_signal_label"] = [signal_label(int(value)) for value in as_num(payload["route_signal_value"]).astype("int8").to_numpy()]
        payload["payload_claim_boundary"] = BOUNDARY
        payload["feature_order_hash"] = feature_order_hash
        payload_path = PAYLOAD_DIR / f'{spec["materialized_branch_id"]}_payload.parquet'
        io_path(payload_path.parent).mkdir(parents=True, exist_ok=True)
        payload.to_parquet(io_path(payload_path), index=False)
        handoff_path = HANDOFF_DIR / f'{spec["materialized_branch_id"]}_handoff.json'
        write_json(handoff_path, {**spec, "feature_order": list(FEATURE_ORDER), "feature_order_hash": feature_order_hash, "claim_boundary": BOUNDARY})
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
        manifest = {
            "queue_id": f"run288A_queue_{index:02d}",
            "materialized_branch_id": spec["materialized_branch_id"],
            "stage288_branch_id": spec["stage288_branch_id"],
            "package_id": spec["package_id"],
            "queue_role": "risk_reward_exit_asymmetry",
            "payload_path": rel(payload_path),
            "payload_hash": sha256_file_lf_normalized(payload_path),
            "handoff_path": rel(handoff_path),
            "handoff_hash": sha256_file_lf_normalized(handoff_path),
            "feature_order": "|".join(FEATURE_ORDER),
            "feature_order_hash": feature_order_hash,
            "max_hold_bars": spec["max_hold_bars"],
            "close_on_flat_signal": spec["close_on_flat_signal"],
            "same_direction_reentry_cooldown_bars": spec["same_direction_reentry_cooldown_bars"],
            "atr_sltp_enabled": spec["atr_sltp_enabled"],
            "atr_period": 14,
            "atr_stop_multiplier": spec["atr_stop_multiplier"],
            "atr_take_profit_multiplier": spec["atr_take_profit_multiplier"],
            "atr_min_stop_points": 0.0,
            "atr_max_stop_points": 0.0,
            "atr_min_take_profit_points": 0.0,
            "atr_max_take_profit_points": 0.0,
            "exit_risk_overlay_enabled": spec["exit_risk_overlay_enabled"],
            "exit_risk_close_long_feature_index": 1,
            "exit_risk_close_short_feature_index": 2,
            "exit_risk_close_threshold": 0.5,
            "exit_risk_min_hold_bars": 2,
            "exit_risk_max_hold_feature_index": 3,
            "model_risk_sizing_enabled": spec["model_risk_sizing_enabled"],
            "model_risk_min_pct": 0.005,
            "model_risk_max_pct": 0.015,
            "model_risk_confidence_floor": 0.55,
            "model_risk_confidence_ceiling": 0.99,
            "model_risk_fallback_lot": 0.10,
            "approx_validation_trades_per_day": tier_a_val.get("approx_trades_per_day", 0),
            "approx_oos_trades_per_day": tier_a_oos.get("approx_trades_per_day", 0),
            "selected_candidate": "none",
            "adapter_package": "none",
            "onnx_readiness": "not_claimed",
            "claim_boundary": BOUNDARY,
        }
        manifest_rows.append(manifest)
        branch_rows.append({**spec, "feature_order": "|".join(FEATURE_ORDER), "claim_boundary": BOUNDARY})
        artifacts.extend([payload_path, handoff_path])
    return branch_rows, supply_rows, manifest_rows, artifacts


def report_markdown(manifest_rows: Sequence[Mapping[str, Any]]) -> str:
    rows = [
        f"- `{row['package_id']}`: ATR stop/take `{row['atr_stop_multiplier']}/{row['atr_take_profit_multiplier']}`, overlay(오버레이) `{row['exit_risk_overlay_enabled']}`, validation approx(검증 근사) `{float(row['approx_validation_trades_per_day']):.2f}`, OOS approx(표본외 근사) `{float(row['approx_oos_trades_per_day']):.2f}` trades/day(일 거래)."
        for row in manifest_rows
    ]
    return f"""# run288A Risk Reward Exit Asymmetry Materialization(288A 위험/보상/청산 비대칭 물질화)

- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- branch_count(분기 수): `{len(manifest_rows)}`
- feature_order(피처 순서): `{ "|".join(FEATURE_ORDER) }`
- selected_candidate(선택 후보): `none`
- Adapter package(어댑터 패키지): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- next_action(다음 행동): `{NEXT_ACTION}`

## Queue(대기열)

{chr(10).join(rows)}

Effect(효과): 방향 신호의 좁은 임계값 수리가 아니라 ATR SL/TP(ATR 손절/익절), exit overlay(청산 오버레이), risk sizing(위험 크기)을 MT5 probe(MT5 탐침)에 넘긴다.
"""


def write_outputs(branch_rows: Sequence[Mapping[str, Any]], supply_rows: Sequence[Mapping[str, Any]], manifest_rows: Sequence[Mapping[str, Any]], artifacts: Sequence[Path], created_at: str) -> list[Path]:
    for path in (RUN_ROOT, PAYLOAD_DIR, HANDOFF_DIR, MT5_HANDOFF_DIR, REVIEWS):
        io_path(path).mkdir(parents=True, exist_ok=True)
    write_csv(BRANCH_QUEUE, BRANCH_COLUMNS, branch_rows)
    write_csv(CANDIDATE_SUPPLY, SUPPLY_COLUMNS, supply_rows)
    write_csv(PAYLOAD_MANIFEST, MANIFEST_COLUMNS, manifest_rows)
    write_csv(MT5_QUEUE, MANIFEST_COLUMNS, manifest_rows)
    write_json(DESIGN_RECEIPT, {"run_id": RUN_ID, "hypothesis": "risk_reward_exit_asymmetry", "feature_order": list(FEATURE_ORDER), "claim_boundary": BOUNDARY})
    write_json(DATA_RECEIPT, {"source_cp287E_rows": len(pd.read_parquet(io_path(SOURCE_E))), "source_cp287B_rows": len(pd.read_parquet(io_path(SOURCE_B))), "label_or_future_columns_added": False, "claim_boundary": BOUNDARY})
    write_csv(RESULT_JUDGMENT, RESULT_COLUMNS, [{"result_subject": RUN_ID, "evidence_available": rel(PAYLOAD_MANIFEST), "evidence_missing": "MT5 runtime KPI and curve review", "judgment_label": JUDGMENT, "judgment_class": "inconclusive_until_mt5_probe(탐침 전 불충분)", "claim_boundary": BOUNDARY, "next_condition": NEXT_ACTION, "user_explanation_hook": "위험/보상/청산 후보 입력을 만들었지만 성과 후보는 아니다."}])
    write_csv(GATE_AUDIT, GATE_COLUMNS, [{"gate_name": "fresh_thesis(새 가설)", "status": "passed", "evidence_path": rel(BRANCH_QUEUE), "effect": "risk/reward/exit(위험/보상/청산) 구조로 질문을 바꿨다."}, {"gate_name": "feature_order_trace(피처 순서 추적)", "status": "passed", "evidence_path": rel(PAYLOAD_MANIFEST), "effect": "route signal(경로 신호)과 overlay feature(오버레이 피처) 순서를 남겼다."}, {"gate_name": "no_candidate_no_onnx_claim(후보와 온엑스 주장 없음)", "status": "passed", "evidence_path": rel(RESULT_JUDGMENT), "effect": "MT5 전 성과 주장을 막는다."}])
    write_md(REPORT, report_markdown(manifest_rows))
    final = [BRANCH_QUEUE, CANDIDATE_SUPPLY, PAYLOAD_MANIFEST, MT5_QUEUE, DESIGN_RECEIPT, DATA_RECEIPT, RESULT_JUDGMENT, GATE_AUDIT, REPORT, *artifacts]
    write_json(LINEAGE, {"run_id": RUN_ID, "producer": PRODUCER.as_posix(), "source_artifacts": [rel(SOURCE_E), rel(SOURCE_B), rel(SEED_QUEUE), rel(INPUT_REFS)], "produced_artifacts": [rel(path) for path in final if path_exists(path)], "claim_boundary": BOUNDARY})
    final.append(LINEAGE)
    write_json(RUN_MANIFEST, {"stage_id": STAGE_ID, "run_id": RUN_ID, "status": STATUS, "judgment": JUDGMENT, "created_at_utc": created_at, "branch_count": len(manifest_rows), "mt5_queue_rows": len(manifest_rows), "next_action": NEXT_ACTION, "selected_candidate": "none", "adapter_package": "none", "onnx_readiness": "not_claimed", "claim_boundary": BOUNDARY})
    final.append(RUN_MANIFEST)
    return [path for path in final if path_exists(path)]


def update_docs_and_registers(created_at: str, artifacts: Sequence[Path], manifest_rows: Sequence[Mapping[str, Any]]) -> None:
    upsert_csv(RUN_REGISTRY, RUN_REGISTRY_COLUMNS, [{"run_id": RUN_ID, "stage_id": STAGE_ID, "lane": "risk_reward_exit_asymmetry_materialization", "status": STATUS, "judgment": JUDGMENT, "path": rel(REPORT), "notes": f"branches={len(manifest_rows)};next_action={NEXT_ACTION}"}], key="run_id")
    upsert_csv(ALPHA_LEDGER, ALPHA_LEDGER_COLUMNS, [{"ledger_row_id": f"{RUN_ID}__materialization", "stage_id": STAGE_ID, "run_id": RUN_ID, "subrun_id": RUN_NUMBER, "parent_run_id": SOURCE_RUN_ID, "record_view": "risk_reward_exit_asymmetry_materialization", "tier_scope": "Tier A/Tier B/Tier A+B", "kpi_scope": "structural_scout", "scoreboard_lane": "risk_reward_exit_asymmetry", "status": STATUS, "judgment": JUDGMENT, "path": rel(REPORT), "primary_kpi": f"mt5_queue_rows={len(manifest_rows)}", "guardrail_kpi": "feature_order_trace_no_candidate_claim", "external_verification_status": "not_attempted_run288A_materialization", "notes": "MT5 probe required before result judgment."}], key="ledger_row_id")
    upsert_csv(STAGE_LEDGER, STAGE_LEDGER_COLUMNS, [{"row_id": f"{RUN_ID}__materialization", "stage_id": STAGE_ID, "run_id": RUN_ID, "view": "risk_reward_exit_asymmetry_materialization", "tier_scope": "Tier A/Tier B/Tier A+B", "scoreboard": "candidate_supply_diagnostics", "status": STATUS, "judgment": JUDGMENT, "evidence_boundary": "no_candidate_no_adapter_no_onnx", "report_path": rel(REPORT), "notes": f"mt5_queue_rows={len(manifest_rows)};next_action={NEXT_ACTION}"}], key="row_id")
    artifact_rows = [{"artifact_id": f"{RUN_ID}__{hashlib.sha1(rel(path).encode('utf-8')).hexdigest()[:12]}", "artifact_type": "stage288_risk_reward_exit_artifact", "path": rel(path), "sha256": sha256_file_lf_normalized(path), "stage_id": STAGE_ID, "run_id": RUN_ID, "created_at_utc": created_at, "notes": "run288A risk reward exit asymmetry materialization(288A 위험/보상/청산 비대칭 물질화)"} for path in artifacts if path_exists(path)]
    upsert_csv(ARTIFACT_REGISTRY, ARTIFACT_COLUMNS, artifact_rows, key="artifact_id")
    selected = io_path(SELECTED).read_text(encoding="utf-8-sig") if path_exists(SELECTED) else "# Stage288 Selection Status(288단계 선택 상태)\n"
    selected = replace_line_prefix(selected, "- stage_status(단계 상태):", f"- stage_status(단계 상태): `{STATUS}`")
    selected = replace_line_prefix(selected, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    selected = replace_line_prefix(selected, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    selected = append_once(selected, "run288A_report", f"- run288A_report(288A 보고서): `{rel(REPORT)}`")
    selected = append_once(selected, "run288A_mt5_queue", f"- run288A_mt5_queue(288A MT5 대기열): `{rel(MT5_QUEUE)}`")
    write_md(SELECTED, selected)
    review_index = io_path(REVIEW_INDEX).read_text(encoding="utf-8-sig") if path_exists(REVIEW_INDEX) else "# Stage288 Review Index(288단계 검토 색인)\n"
    review_index = append_once(review_index, "run288A_report", f"- run288A_report(288A 보고서): `{rel(REPORT)}`")
    write_md(REVIEW_INDEX, review_index)
    current = io_path(CURRENT_STATE).read_text(encoding="utf-8-sig")
    current = replace_line_prefix(current, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_line_prefix(current, "- status(상태):", f"- status(상태): `{STATUS}`")
    current = replace_line_prefix(current, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    current = append_once(current, "run288A_summary", f"- run288A_summary(288A 요약): risk/reward/exit asymmetry(위험/보상/청산 비대칭) 후보 `{len(manifest_rows)}`개를 물질화했다. Effect(효과): ATR SL/TP(ATR 손절/익절), exit overlay(청산 오버레이), risk sizing(위험 크기)을 MT5 탐침 대기열로 넘긴다.")
    write_md(CURRENT_STATE, current)
    workspace = io_path(WORKSPACE_STATE).read_text(encoding="utf-8-sig")
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    workspace = replace_line_prefix(workspace, "updated_on:", f"updated_on: '{UPDATED_ON}'")
    focus = f"- >-\n  Stage288(288단계) run288A(288A 실행) risk reward exit asymmetry materialization(위험/보상/청산 비대칭 물질화) `{RUN_ID}`. Effect(효과): 후보 `{len(manifest_rows)}`개를 MT5 probe(MT5 탐침) 대기열로 넘기며 후보/어댑터/온엑스 주장은 하지 않는다.\n"
    workspace = prepend_focus(workspace, focus, RUN_ID)
    write_md(WORKSPACE_STATE, workspace)
    changelog = io_path(CHANGELOG).read_text(encoding="utf-8-sig")
    changelog = append_once(changelog, RUN_ID, f"## {UPDATED_ON} run288A Risk reward exit asymmetry materialization(288A 위험/보상/청산 비대칭 물질화)\n\n- status(상태): `{STATUS}`\n- judgment(판정): `{JUDGMENT}`\n- effect(효과): 후보 `{len(manifest_rows)}`개를 MT5 probe queue(MT5 탐침 대기열)로 만들었다.\n- boundary(경계): selected candidate(선택 후보), Adapter package(어댑터 패키지), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 `none/not_claimed`다.\n")
    write_md(CHANGELOG, changelog)


def main() -> None:
    created_at = utc_now()
    branch_rows, supply_rows, manifest_rows, payload_artifacts = materialize()
    artifacts = write_outputs(branch_rows, supply_rows, manifest_rows, payload_artifacts, created_at)
    update_docs_and_registers(created_at, artifacts, manifest_rows)
    print(json.dumps({"run_id": RUN_ID, "status": STATUS, "judgment": JUDGMENT, "branch_count": len(manifest_rows), "mt5_queue_rows": len(manifest_rows), "selected_candidate": "none", "adapter_package": "none", "onnx_readiness": "not_claimed", "goal_achieve": "not_claimed", "next_action": NEXT_ACTION}, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
