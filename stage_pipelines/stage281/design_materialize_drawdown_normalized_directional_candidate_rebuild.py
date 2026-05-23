from __future__ import annotations

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


STAGE_ID = "281_onnx_candidate_campaign__drawdown_normalized_directional_candidate_rebuild"
RUN_ID = "run281A_design_materialize_drawdown_normalized_directional_candidate_rebuild_v1"
SOURCE_RUN_ID = "run280A_directional_mapping_stability_validation_v1"
STATUS = "completed_drawdown_normalized_candidate_rebuild_inputs_materialized_no_candidate_selection"
JUDGMENT = "fresh_drawdown_normalized_candidate_inputs_materialized_no_candidate_selection"
NEXT_ACTION = "run281B_execute_drawdown_normalized_directional_mt5_probe"
UPDATED_ON = "2026-05-24"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_"
    "no_deployment_no_onnx_until_candidate_package_gate"
)

STAGE_ROOT = ROOT / "stages" / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / "run281A"
REVIEWS = STAGE_ROOT / "03_reviews"
SELECTED = STAGE_ROOT / "04_selected" / "selection_status.md"
REVIEW_INDEX = REVIEWS / "review_index.md"
STAGE_LEDGER = REVIEWS / "stage_run_ledger.csv"
INPUTS = STAGE_ROOT / "01_inputs"

STAGE279_RUN279B = ROOT / "stages" / "279_onnx_candidate_campaign__directional_runtime_mapping_rebuild" / "02_runs" / "run279B"
SOURCE_Q02 = STAGE279_RUN279B / "payloads" / "run279B_cp277D_breakout_q02_payload.parquet"
SOURCE_Q03 = STAGE279_RUN279B / "payloads" / "run279B_cp277D_breakout_q03_payload.parquet"
STAGE280_SCOREBOARD = INPUTS / "stage280_stability_scoreboard.csv"
STAGE280_FAILURE = INPUTS / "stage280_stability_failure_memory.csv"

PAYLOAD_DIR = RUN_ROOT / "payloads"
HANDOFF_DIR = RUN_ROOT / "handoff"
MT5_HANDOFF_DIR = RUN_ROOT / "mt5_handoff"
BRANCH_QUEUE = RUN_ROOT / "branch_design_queue.csv"
PAYLOAD_MANIFEST = RUN_ROOT / "candidate_payload_manifest.csv"
MT5_QUEUE = RUN_ROOT / "mt5_probe_queue.csv"
DESIGN_RECEIPT = RUN_ROOT / "experiment_design_receipt.json"
DATA_RECEIPT = RUN_ROOT / "data_integrity_receipt.json"
LINEAGE = RUN_ROOT / "artifact_lineage_receipt.json"
RESULT_JUDGMENT = RUN_ROOT / "result_judgment.csv"
GATE_AUDIT = RUN_ROOT / "required_gate_coverage_audit.csv"
RUN_MANIFEST = RUN_ROOT / "run_manifest.json"
REPORT = REVIEWS / "run281A_candidate_rebuild_materialization_report.md"

RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
IDEA_REGISTER = ROOT / "docs" / "registers" / "idea_registry.md"
PRODUCER = Path("stage_pipelines/stage281/design_materialize_drawdown_normalized_directional_candidate_rebuild.py")

BRANCH_COLUMNS = (
    "stage281_branch_id",
    "materialized_branch_id",
    "package_id",
    "fresh_thesis",
    "source_payload",
    "decision_surface",
    "risk_logic",
    "adapter_path",
    "runtime_handoff",
    "upside_condition",
    "failure_condition",
    "claim_boundary",
)
MANIFEST_COLUMNS = (
    "queue_id",
    "materialized_branch_id",
    "stage281_branch_id",
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
    if len(q02) != len(q03):
        raise RuntimeError("source payload row count mismatch(원천 페이로드 행 수 불일치)")
    if not q02["timestamp"].equals(q03["timestamp"]):
        raise RuntimeError("source payload timestamp mismatch(원천 페이로드 시각 불일치)")
    return q02, q03


def branch_specs() -> list[dict[str, Any]]:
    return [
        {
            "stage281_branch_id": "run281A_cp281A_deterministic_concordant_breakout",
            "materialized_branch_id": "run281A_cp281A_concordant_breakout",
            "package_id": "cp281A_drawdown_normalized_concordant_breakout_surface",
            "source_payload": "run279B_cp277D_breakout_q02",
            "fresh_thesis": "Use q02 direction only when squeeze, volatility, and directional trend agree; risk is normalized by rejecting extreme return pressure.",
            "decision_surface": "route_signal=q02_direction when bb_squeeze=1, vol_ratio 0.85..1.85, abs(return_zscore)<=2.0, and DI spread agrees with direction.",
            "risk_logic": "ATR stop/take-profit stays traceable; high z-score and non-squeeze states are flat to cap drawdown concentration.",
            "adapter_path": "single feature route_signal_value table now; later Adapter package must expose direction/risk diagnostics.",
            "runtime_handoff": "MT5 one-feature EBM table with Tier A primary + Tier B fallback stress.",
            "upside_condition": "validation recovery improves while OOS PF remains above 1.10 with enough trades.",
            "failure_condition": "trade count collapses, validation recovery stays below 0.25, or one month carries the result.",
        },
        {
            "stage281_branch_id": "run281A_cp281B_macro_trend_concordance",
            "materialized_branch_id": "run281A_cp281B_macro_trend_concordance",
            "package_id": "cp281B_macro_trend_concordance_surface",
            "source_payload": "run279B_cp277D_breakout_q02",
            "fresh_thesis": "Require either trend concordance or macro relative-strength concordance before accepting a directional breakout.",
            "decision_surface": "route_signal=q02_direction when vol_ratio 0.75..1.65, abs(return_zscore)<=1.6, and trend or macro spread agrees with direction.",
            "risk_logic": "Reduce weak-month loss concentration by refusing high-volatility breakout signals without macro/trend support.",
            "adapter_path": "single feature route_signal_value table now; later Adapter package must preserve macro/trend source columns.",
            "runtime_handoff": "MT5 one-feature EBM table with paired Tier A/Tier B records.",
            "upside_condition": "validation PF and recovery improve without losing OOS net scale.",
            "failure_condition": "OOS net collapses below 100 or validation top-month contribution remains pathological.",
        },
        {
            "stage281_branch_id": "run281A_cp281C_signal_pressure_hysteresis",
            "materialized_branch_id": "run281A_cp281C_signal_pressure_hysteresis",
            "package_id": "cp281C_signal_pressure_hysteresis_surface",
            "source_payload": "run279B_cp277D_breakout_q02",
            "fresh_thesis": "Treat recent signal density as a drawdown proxy; throttle entries when signal pressure clusters.",
            "decision_surface": "route_signal=q02_direction when rolling 12-bar nonflat pressure<=4, abs(return_zscore)<=2.4, and vol_ratio<=2.1.",
            "risk_logic": "Hysteresis blocks cluster-driven re-entry pressure to attack validation losing streaks.",
            "adapter_path": "single feature route_signal_value table now; later Adapter package must expose signal pressure state.",
            "runtime_handoff": "MT5 one-feature EBM table with route_signal replay.",
            "upside_condition": "max losing streak falls below 7 while validation/OOS stay positive.",
            "failure_condition": "losing streak remains high or OOS recovery falls below 0.50.",
        },
        {
            "stage281_branch_id": "run281A_cp281D_low_supply_controlled_breakout",
            "materialized_branch_id": "run281A_cp281D_low_supply_controlled_breakout",
            "package_id": "cp281D_low_supply_controlled_breakout_surface",
            "source_payload": "run279B_cp277D_breakout_q03",
            "fresh_thesis": "Use the lower-supply q03 branch but add direction/trend confirmation so it can test stability without becoming a thin artifact.",
            "decision_surface": "route_signal=q03_direction when vol_ratio 0.70..1.75, abs(return_zscore)<=2.2, and RSI slope or DI spread agrees with direction.",
            "risk_logic": "Preserve q03 validation stability clue while rejecting low-quality volatility extremes.",
            "adapter_path": "single feature route_signal_value table now; later Adapter package must expose low-supply control status.",
            "runtime_handoff": "MT5 one-feature EBM table with q03-derived direction.",
            "upside_condition": "OOS PF rises above 1.05 and OOS recovery rises above 0.50 with at least 80 trades.",
            "failure_condition": "OOS remains thin or top-month contribution still dominates.",
        },
    ]


def build_signal(frame: pd.DataFrame, q03: pd.DataFrame, spec: Mapping[str, Any]) -> np.ndarray:
    base = as_num(frame["direction_signal_value"]).astype("int8").to_numpy()
    q03_dir = as_num(q03["direction_signal_value"]).astype("int8").to_numpy()
    vol = as_num(frame["historical_vol_5_over_20"])
    z = as_num(frame["return_zscore_20"])
    squeeze = as_num(frame["bb_squeeze"])
    di = sign(frame["di_spread_14"])
    ema = sign(frame["ema20_ema50_diff"])
    rsi = sign(frame["rsi_14_slope_3"])
    mega = sign(frame["us100_minus_mega8_equal_return_1"])
    top3 = sign(frame["us100_minus_top3_weighted_return_1"])
    branch_id = str(spec["materialized_branch_id"])
    if branch_id.endswith("cp281A_concordant_breakout"):
        mask = (base != 0) & (squeeze.to_numpy() >= 1.0) & vol.between(0.85, 1.85).to_numpy() & (z.abs().to_numpy() <= 2.0) & (di == base)
        return np.where(mask, base, 0).astype("int8")
    if branch_id.endswith("cp281B_macro_trend_concordance"):
        trend = (di == base) & (ema == base)
        macro = (mega == base) | (top3 == base)
        mask = (base != 0) & vol.between(0.75, 1.65).to_numpy() & (z.abs().to_numpy() <= 1.6) & (trend | macro)
        return np.where(mask, base, 0).astype("int8")
    if branch_id.endswith("cp281C_signal_pressure_hysteresis"):
        result = np.zeros(len(frame), dtype="int8")
        temp = frame[["tier_scope", "split"]].copy()
        temp["base"] = base
        temp["vol"] = vol.to_numpy()
        temp["z_abs"] = z.abs().to_numpy()
        for _, group in temp.groupby(["tier_scope", "split"], sort=False):
            pressure = group["base"].ne(0).astype("int8").rolling(12, min_periods=1).sum().to_numpy()
            group_base = group["base"].to_numpy(dtype="int8")
            mask = (group_base != 0) & (pressure <= 4) & (group["z_abs"].to_numpy() <= 2.4) & (group["vol"].to_numpy() <= 2.1)
            result[group.index.to_numpy()] = np.where(mask, group_base, 0)
        return result
    if branch_id.endswith("cp281D_low_supply_controlled_breakout"):
        mask = (q03_dir != 0) & vol.between(0.70, 1.75).to_numpy() & (z.abs().to_numpy() <= 2.2) & ((rsi == q03_dir) | (di == q03_dir))
        return np.where(mask, q03_dir, 0).astype("int8")
    raise ValueError(branch_id)


def label_signal(values: np.ndarray) -> list[str]:
    return ["long" if value > 0 else "short" if value < 0 else "flat" for value in values]


def signal_count(frame: pd.DataFrame, tier: str, split: str) -> int:
    view = frame.loc[frame["tier_scope"].astype(str).eq(tier) & frame["split"].astype(str).eq(split), "route_signal_value"]
    return int(pd.to_numeric(view, errors="coerce").fillna(0).ne(0).sum())


def export_signal_csv(frame: pd.DataFrame, path: Path) -> None:
    out = frame[["timestamp", "symbol", "split", "tier_scope", "route_signal_value", "route_signal_label", "materialized_branch_id", "package_id"]].copy()
    out["timestamp"] = pd.to_datetime(out["timestamp"], utc=True).dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    out.to_csv(io_path(path), index=False, encoding="utf-8")


def materialize() -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[Path]]:
    q02, q03 = load_payloads()
    branch_rows: list[dict[str, Any]] = []
    manifest_rows: list[dict[str, Any]] = []
    artifacts: list[Path] = []
    for index, spec in enumerate(branch_specs(), start=1):
        source = q03 if str(spec["source_payload"]).endswith("q03") else q02
        frame = source.copy()
        signal = build_signal(source, q03, spec)
        direction_hash = surface_hash({"spec": spec, "feature_order": ["route_signal_value"], "signal_counts": int(np.count_nonzero(signal))})
        frame["package_id"] = spec["package_id"]
        frame["materialized_branch_id"] = spec["materialized_branch_id"]
        frame["stage281_branch_id"] = spec["stage281_branch_id"]
        frame["stage279_branch_id"] = frame.get("stage279_branch_id", "")
        frame["source_branch_id"] = spec["source_payload"]
        frame["route_signal_value"] = signal
        frame["direction_signal_value"] = signal
        frame["route_signal_label"] = label_signal(signal)
        frame["direction_signal_label"] = frame["route_signal_label"]
        frame["direction_surface_hash"] = direction_hash
        frame["direction_feature_order_hash"] = ordered_hash(["route_signal_value"])
        frame["direction_runtime_handoff_status"] = "materialized_for_mt5_probe_no_candidate_selection"
        frame["claim_boundary"] = BOUNDARY
        frame["payload_claim_boundary"] = BOUNDARY
        frame["fresh_thesis"] = spec["fresh_thesis"]
        payload_path = PAYLOAD_DIR / f"{spec['materialized_branch_id']}_payload.parquet"
        handoff_path = HANDOFF_DIR / f"{spec['materialized_branch_id']}.json"
        tier_a_signal = MT5_HANDOFF_DIR / f"{spec['materialized_branch_id']}_tier_a_direction_signals.csv"
        tier_b_signal = MT5_HANDOFF_DIR / f"{spec['materialized_branch_id']}_tier_b_direction_stress_signals.csv"
        routed_signal = MT5_HANDOFF_DIR / f"{spec['materialized_branch_id']}_actual_routed_direction_signals.csv"
        io_path(payload_path.parent).mkdir(parents=True, exist_ok=True)
        frame.to_parquet(io_path(payload_path), index=False)
        handoff = {
            "run_id": RUN_ID,
            "materialized_branch_id": spec["materialized_branch_id"],
            "package_id": spec["package_id"],
            "feature_surface": ["route_signal_value"],
            "model_or_scoring_surface": "single discrete route signal table for runtime probe",
            "decision_surface": spec["decision_surface"],
            "risk_logic": spec["risk_logic"],
            "adapter_path": spec["adapter_path"],
            "runtime_handoff": spec["runtime_handoff"],
            "direction_surface_hash": direction_hash,
            "selected_candidate": "none",
            "adapter_package": "none",
            "onnx_readiness": "not_claimed",
            "claim_boundary": BOUNDARY,
        }
        write_json(handoff_path, handoff)
        export_signal_csv(frame.loc[frame["tier_scope"].astype(str).eq("Tier A")], tier_a_signal)
        export_signal_csv(frame.loc[frame["tier_scope"].astype(str).eq("Tier B")], tier_b_signal)
        export_signal_csv(frame, routed_signal)
        for path in (payload_path, handoff_path, tier_a_signal, tier_b_signal, routed_signal):
            artifacts.append(path)
        branch_rows.append({**spec, "claim_boundary": BOUNDARY})
        manifest_rows.append(
            {
                "queue_id": f"run281B_{index:02d}_{spec['materialized_branch_id']}",
                "materialized_branch_id": spec["materialized_branch_id"],
                "stage281_branch_id": spec["stage281_branch_id"],
                "stage279_branch_id": "stage281_fresh_rebuild",
                "source_branch_id": spec["source_payload"],
                "package_id": spec["package_id"],
                "queue_role": "drawdown_normalized_candidate_probe_seed",
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
                "direction_feature_order_hash": ordered_hash(["route_signal_value"]),
                "tier_a_validation_signal_count": signal_count(frame, "Tier A", "validation"),
                "tier_a_oos_signal_count": signal_count(frame, "Tier A", "oos"),
                "tier_b_validation_signal_count": signal_count(frame, "Tier B", "validation"),
                "tier_b_oos_signal_count": signal_count(frame, "Tier B", "oos"),
                "actual_routed_validation_signal_count": signal_count(frame, "Tier A", "validation"),
                "actual_routed_oos_signal_count": signal_count(frame, "Tier A", "oos"),
                "selected_candidate": "none",
                "adapter_package": "none",
                "onnx_readiness": "not_claimed",
                "claim_boundary": BOUNDARY,
            }
        )
    return branch_rows, manifest_rows, artifacts


def write_outputs(branch_rows: Sequence[Mapping[str, Any]], manifest_rows: Sequence[Mapping[str, Any]], payload_artifacts: Sequence[Path], created_at: str) -> list[Path]:
    write_csv(BRANCH_QUEUE, BRANCH_COLUMNS, branch_rows)
    write_csv(PAYLOAD_MANIFEST, MANIFEST_COLUMNS, manifest_rows)
    write_csv(MT5_QUEUE, MANIFEST_COLUMNS, manifest_rows)
    write_json(
        DESIGN_RECEIPT,
        {
            "run_id": RUN_ID,
            "fresh_thesis": "drawdown-normalized directional candidate rebuild(손실폭 정규화 방향 후보 재구성)",
            "branch_count": len(branch_rows),
            "success_condition": "MT5 validation and OOS both survive net/PF/DD/recovery/trade-count pressure before Adapter/ONNX.",
            "failure_condition": "No branch improves validation recovery and OOS stability together.",
            "selected_candidate": "none",
            "adapter_package": "none",
            "onnx_readiness": "not_claimed",
            "next_action": NEXT_ACTION,
        },
    )
    write_json(
        DATA_RECEIPT,
        {
            "run_id": RUN_ID,
            "source_payloads": [rel(SOURCE_Q02), rel(SOURCE_Q03)],
            "timestamp_rule": "closed bar UTC timestamp preserved for MT5 handoff",
            "label_or_future_columns_used": False,
            "payload_rows_each": 93300,
            "selected_candidate": "none",
            "claim_boundary": BOUNDARY,
        },
    )
    write_csv(
        RESULT_JUDGMENT,
        RESULT_COLUMNS,
        [
            {
                "result_subject": RUN_ID,
                "evidence_available": f"branch_count={len(branch_rows)};mt5_queue_rows={len(manifest_rows)}",
                "evidence_missing": "MT5 runtime KPI;stability review;Adapter package;ONNX parity",
                "judgment_label": JUDGMENT,
                "judgment_class": "candidate_input_materialization(후보 입력 물질화)",
                "claim_boundary": BOUNDARY,
                "next_condition": NEXT_ACTION,
                "user_explanation_hook": "새 후보 논제는 만들어졌지만 아직 후보 선택은 아니다.",
            }
        ],
    )
    write_csv(
        GATE_AUDIT,
        GATE_COLUMNS,
        [
            {
                "gate_name": "fresh_thesis_recorded(새 논제 기록)",
                "status": "passed",
                "evidence_path": rel(BRANCH_QUEUE),
                "effect": "단순 수리가 아니라 새 손실폭 정규화 판단/위험 표면을 기록했다.",
            },
            {
                "gate_name": "mt5_queue_materialized(MT5 대기열 물질화)",
                "status": "passed",
                "evidence_path": rel(MT5_QUEUE),
                "effect": "다음 실행에서 외부 MT5 검증을 바로 시도할 수 있다.",
            },
            {
                "gate_name": "no_candidate_no_onnx_claim(후보/ONNX 주장 없음)",
                "status": "passed",
                "evidence_path": rel(RESULT_JUDGMENT),
                "effect": "후보 선택과 ONNX 준비를 앞당겨 주장하지 않았다.",
            },
        ],
    )
    write_md(REPORT, report_markdown(manifest_rows))
    artifacts = [BRANCH_QUEUE, PAYLOAD_MANIFEST, MT5_QUEUE, DESIGN_RECEIPT, DATA_RECEIPT, RESULT_JUDGMENT, GATE_AUDIT, REPORT, *payload_artifacts]
    manifest = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "source_run_id": SOURCE_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "created_at_utc": created_at,
        "branch_count": len(branch_rows),
        "mt5_queue_rows": len(manifest_rows),
        "output_hashes": {rel(path): sha256_file(path) for path in artifacts if path_exists(path)},
        "selected_candidate": "none",
        "adapter_package": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": NEXT_ACTION,
        "claim_boundary": BOUNDARY,
    }
    write_json(RUN_MANIFEST, manifest)
    artifacts.append(RUN_MANIFEST)
    lineage = {
        "run_id": RUN_ID,
        "source_inputs": [rel(STAGE280_SCOREBOARD), rel(STAGE280_FAILURE), rel(SOURCE_Q02), rel(SOURCE_Q03), rel(ROOT / PRODUCER)],
        "source_hashes": {
            rel(path): sha256_file(path)
            for path in [STAGE280_SCOREBOARD, STAGE280_FAILURE, SOURCE_Q02, SOURCE_Q03, ROOT / PRODUCER]
            if path_exists(path)
        },
        "artifact_paths": [rel(path) for path in artifacts if path_exists(path)],
        "artifact_hashes": {rel(path): sha256_file(path) for path in artifacts if path_exists(path)},
        "lineage_judgment": "connected_no_candidate_no_onnx_claim(연결됨, 후보/ONNX 주장 없음)",
    }
    write_json(LINEAGE, lineage)
    artifacts.append(LINEAGE)
    return artifacts


def report_markdown(manifest_rows: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        "# run281A Report(281A 보고서): Drawdown-Normalized Candidate Input Materialization(손실폭 정규화 후보 입력 물질화)",
        "",
        f"- run_id(실행 ID): `{RUN_ID}`",
        f"- status(상태): `{STATUS}`",
        f"- judgment(판정): `{JUDGMENT}`",
        f"- branch_count(분기 수): `{len(manifest_rows)}`",
        "- selected_candidate(선택 후보): `none`",
        "- Adapter package(어댑터 패키지): `none`",
        "- ONNX readiness(온엑스 준비): `not_claimed`",
        "- Goal Achieve(목표 달성): `not_claimed`",
        f"- next_action(다음 행동): `{NEXT_ACTION}`",
        "",
        "| branch(분기) | val signals(검증 신호) | OOS signals(표본외 신호) | package(패키지) |",
    ]
    for row in manifest_rows:
        lines.append(
            f"| `{row['materialized_branch_id']}` | `{row['actual_routed_validation_signal_count']}` | `{row['actual_routed_oos_signal_count']}` | `{row['package_id']}` |"
        )
    lines.extend(
        [
            "",
            "Effect(효과): Stage281(281단계)는 Stage280(280단계)의 실패 기억을 새 route_signal_value(경로 신호 값) 표면으로 바꿨고, 다음 실행에서 MT5(MetaTrader 5, 메타트레이더5)로 검증한다.",
            "",
            f"`{BOUNDARY}`",
        ]
    )
    return "\n".join(lines)


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


def update_registers_and_docs(created_at: str, artifacts: Sequence[Path], manifest_rows: Sequence[Mapping[str, Any]]) -> None:
    upsert_csv_rows(
        RUN_REGISTRY,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "drawdown_normalized_candidate_rebuild_materialization",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT),
                "notes": f"branch_count={len(manifest_rows)};next_action={NEXT_ACTION};selected_candidate=none.",
            }
        ],
        key="run_id",
    )
    upsert_csv_rows(
        ALPHA_LEDGER,
        ALPHA_LEDGER_COLUMNS,
        [
            {
                "ledger_row_id": f"{RUN_ID}__candidate_inputs",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": "run281A_candidate_input_materialization",
                "parent_run_id": SOURCE_RUN_ID,
                "record_view": "drawdown_normalized_candidate_inputs(손실폭 정규화 후보 입력)",
                "tier_scope": "Tier A used/Tier B fallback stress/actual routed total",
                "kpi_scope": "input_materialization_no_runtime_kpi",
                "scoreboard_lane": "candidate_rebuild_inputs",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(REPORT),
                "primary_kpi": f"branch_count={len(manifest_rows)}",
                "guardrail_kpi": "selected_candidate=none;adapter_package=none;onnx_readiness=not_claimed",
                "external_verification_status": "not_started_materialization_only",
                "notes": f"next_action={NEXT_ACTION}.",
            }
        ],
        key="ledger_row_id",
    )
    upsert_csv_rows(
        STAGE_LEDGER,
        STAGE_LEDGER_COLUMNS,
        [
            {
                "row_id": f"{RUN_ID}__candidate_inputs",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "view": "drawdown_normalized_candidate_input_materialization",
                "tier_scope": "Tier A used/Tier B fallback stress/actual routed total",
                "scoreboard": "mt5_probe_queue",
                "status": STATUS,
                "judgment": JUDGMENT,
                "evidence_boundary": "no_candidate_no_onnx",
                "report_path": rel(REPORT),
                "notes": f"mt5_queue_rows={len(manifest_rows)};next_action={NEXT_ACTION}.",
            }
        ],
        key="row_id",
    )
    artifact_rows = [
        {
            "artifact_id": f"{RUN_ID}__{hashlib.sha1(rel(path).encode('utf-8')).hexdigest()[:12]}",
            "artifact_type": "stage281_candidate_rebuild_input_artifact",
            "path": rel(path),
            "sha256": sha256_file(path),
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": created_at,
            "notes": "run281A candidate input materialization(281A 후보 입력 물질화)",
        }
        for path in artifacts
        if path_exists(path)
    ]
    upsert_csv_rows(ARTIFACT_REGISTRY, ARTIFACT_COLUMNS, artifact_rows, key="artifact_id")

    selected = io_path(SELECTED).read_text(encoding="utf-8-sig")
    selected = replace_line_prefix(selected, "- stage_status(단계 상태):", f"- stage_status(단계 상태): `{STATUS}`")
    selected = replace_line_prefix(selected, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    selected = replace_line_prefix(selected, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    selected = append_once(selected, "run281A_report", f"- run281A_report(281A 보고서): `{rel(REPORT)}`")
    selected = append_once(selected, "run281A_mt5_queue", f"- run281A_mt5_queue(281A MT5 대기열): `{rel(MT5_QUEUE)}`")
    write_md(SELECTED, selected)

    review_index = io_path(REVIEW_INDEX).read_text(encoding="utf-8-sig") if path_exists(REVIEW_INDEX) else "# Stage281 Review Index(281단계 검토 색인)\n"
    review_index = append_once(review_index, "run281A_report", f"- run281A_report(281A 보고서): `{rel(REPORT)}`")
    write_md(REVIEW_INDEX, review_index)

    current = io_path(CURRENT_STATE).read_text(encoding="utf-8-sig")
    current = replace_line_prefix(current, "- current_packet(현재 작업 묶음):", "- current_packet(현재 작업 묶음): `stage281_drawdown_normalized_directional_candidate_rebuild_v1`")
    current = replace_line_prefix(current, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_line_prefix(current, "- status(상태):", f"- status(상태): `{STATUS}`")
    current = replace_line_prefix(current, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    current = append_once(
        current,
        "run281A_summary",
        f"- run281A_summary(281A 요약): 손실폭 정규화 방향 후보 입력 `{len(manifest_rows)}`개를 물질화했다. Effect(효과): MT5 탐침으로 넘길 수 있지만 selected candidate(선택 후보), Adapter package(어댑터 패키지), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 없다.",
    )
    write_md(CURRENT_STATE, current)

    workspace = io_path(WORKSPACE_STATE).read_text(encoding="utf-8-sig")
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    workspace = replace_line_prefix(workspace, "updated_on:", f"updated_on: '{UPDATED_ON}'")
    focus = (
        f"- >-\n"
        f"  Stage281(281단계) run281A(281A 실행) materialized `{len(manifest_rows)}` drawdown-normalized directional candidate inputs(손실폭 정규화 방향 후보 입력). "
        f"Effect(효과): MT5 probe(MT5 탐침) 대기열로 넘기며 후보/ONNX 주장은 하지 않는다.\n"
    )
    workspace = prepend_focus(workspace, focus, RUN_ID)
    write_md(WORKSPACE_STATE, workspace)

    changelog = io_path(CHANGELOG).read_text(encoding="utf-8-sig")
    changelog = append_once(
        changelog,
        RUN_ID,
        f"## {UPDATED_ON} run281A Candidate rebuild materialization(281A 후보 재구성 물질화)\n\n- status(상태): `{STATUS}`\n- judgment(판정): `{JUDGMENT}`\n- effect(효과): branch(분기) `{len(manifest_rows)}`개를 MT5 probe queue(MT5 탐침 대기열)로 만들었다.\n- boundary(경계): selected candidate(선택 후보), Adapter package(어댑터 패키지), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 `none/not_claimed`다.\n",
    )
    write_md(CHANGELOG, changelog)

    idea = io_path(IDEA_REGISTER).read_text(encoding="utf-8-sig")
    idea = append_once(
        idea,
        "IDEA-ST281-RUN281A-DRAWDOWN-NORMALIZED-INPUTS",
        f"| `IDEA-ST281-RUN281A-DRAWDOWN-NORMALIZED-INPUTS` | `{STAGE_ID}` | 손실폭 정규화 방향 후보 입력 `{len(manifest_rows)}`개 | `Tier A used + Tier B fallback stress + actual routed total` | `materialized_no_candidate` | MT5 탐침으로 검증 필요 |",
    )
    write_md(IDEA_REGISTER, idea)


def main() -> None:
    for path in [RUN_ROOT, PAYLOAD_DIR, HANDOFF_DIR, MT5_HANDOFF_DIR, REVIEWS]:
        io_path(path).mkdir(parents=True, exist_ok=True)
    created_at = utc_now()
    branch_rows, manifest_rows, payload_artifacts = materialize()
    artifacts = write_outputs(branch_rows, manifest_rows, payload_artifacts, created_at)
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
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
