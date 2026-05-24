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


STAGE_ID = "289_onnx_candidate_campaign__regime_conditioned_edge_surface_rebuild"
RUN_ID = "run289A_design_materialize_regime_conditioned_edge_candidates_v1"
RUN_NUMBER = "run289A"
STATUS = "completed_regime_conditioned_edge_candidates_materialized_no_selection"
JUDGMENT = "regime_conditioned_edge_candidate_inputs_materialized_no_candidate_selection"
NEXT_ACTION = "run289B_execute_regime_conditioned_edge_mt5_probe"
UPDATED_ON = "2026-05-24"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_"
    "no_deployment_no_onnx_until_candidate_package_gate"
)

STAGE_ROOT = ROOT / "stages" / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER
REVIEWS = STAGE_ROOT / "03_reviews"
SELECTED = STAGE_ROOT / "04_selected" / "selection_status.md"
REVIEW_INDEX = REVIEWS / "review_index.md"
STAGE_LEDGER = REVIEWS / "stage_run_ledger.csv"
PAYLOAD_DIR = RUN_ROOT / "payloads"
HANDOFF_DIR = RUN_ROOT / "handoff"
SOURCE_E = ROOT / "stages/287_onnx_candidate_campaign__density_scale_curve_pocket_rebuild/02_runs/run287A/payloads/run287A_cp287E_consensus_pullback_mix_payload.parquet"

BRANCH_QUEUE = RUN_ROOT / "branch_design_queue.csv"
CANDIDATE_SUPPLY = RUN_ROOT / "candidate_supply_diagnostics.csv"
PAYLOAD_MANIFEST = RUN_ROOT / "candidate_payload_manifest.csv"
MT5_QUEUE = RUN_ROOT / "mt5_probe_queue.csv"
REPORT = REVIEWS / "run289A_regime_conditioned_edge_materialization_report.md"
RESULT_JUDGMENT = RUN_ROOT / "result_judgment.csv"
GATE_AUDIT = RUN_ROOT / "required_gate_coverage_audit.csv"
RUN_MANIFEST = RUN_ROOT / "run_manifest.json"
LINEAGE = RUN_ROOT / "artifact_lineage_receipt.json"

RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
PRODUCER = Path("stage_pipelines/stage289/design_materialize_regime_conditioned_edge_candidates.py")

BRANCH_COLUMNS = ("stage289_branch_id", "materialized_branch_id", "package_id", "fresh_thesis", "decision_surface", "risk_logic", "max_hold_bars", "close_on_flat_signal", "claim_boundary")
SUPPLY_COLUMNS = ("materialized_branch_id", "package_id", "tier_scope", "split", "days", "rows", "active_signal_count", "active_signals_per_day", "long_signal_count", "short_signal_count", "max_hold_bars", "approx_trade_count", "approx_trades_per_day", "trade_density_screen")
MANIFEST_COLUMNS = ("queue_id", "materialized_branch_id", "stage289_branch_id", "package_id", "queue_role", "payload_path", "payload_hash", "handoff_path", "handoff_hash", "direction_surface_hash", "direction_feature_order_hash", "max_hold_bars", "close_on_flat_signal", "same_direction_reentry_cooldown_bars", "approx_validation_trades_per_day", "approx_oos_trades_per_day", "selected_candidate", "adapter_package", "onnx_readiness", "claim_boundary")
RESULT_COLUMNS = ("result_subject", "evidence_available", "evidence_missing", "judgment_label", "judgment_class", "claim_boundary", "next_condition", "user_explanation_hook")
GATE_COLUMNS = ("gate_name", "status", "evidence_path", "effect")
STAGE_LEDGER_COLUMNS = ("row_id", "stage_id", "run_id", "view", "tier_scope", "scoreboard", "status", "judgment", "evidence_boundary", "report_path", "notes")
ARTIFACT_COLUMNS = ("artifact_id", "artifact_type", "path", "sha256", "stage_id", "run_id", "created_at_utc", "notes")


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


def source_features() -> tuple[pd.DataFrame, dict[str, np.ndarray]]:
    frame = pd.read_parquet(io_path(SOURCE_E)).copy()
    frame["timestamp"] = pd.to_datetime(frame["timestamp"], utc=True)
    sig = as_num(frame["route_signal_value"]).astype("int8").to_numpy()
    score = as_num(frame["candidate_decision_score"]).to_numpy()
    vol = as_num(frame["historical_vol_5_over_20"]).to_numpy()
    zabs = as_num(frame["return_zscore_20"]).abs().to_numpy()
    di = sign(frame["di_spread_14"])
    ema = sign(frame["ema20_ema50_diff"])
    rsi = sign(frame["rsi_14_slope_3"])
    trend = np.sign(di + ema + rsi).astype("int8")
    mega = sign(frame["us100_minus_mega8_equal_return_1"])
    top3 = sign(frame["us100_minus_top3_weighted_return_1"])
    macro = np.where((mega + top3) > 0, 1, np.where((mega + top3) < 0, -1, 0)).astype("int8")
    hour = frame["timestamp"].dt.hour.to_numpy()
    cash = (hour >= 16) & (hour < 21)
    late = hour >= 21
    squeeze = as_num(frame["bb_squeeze"]).to_numpy() if "bb_squeeze" in frame.columns else np.zeros(len(frame))
    return frame, {"sig": sig, "score": score, "vol": vol, "zabs": zabs, "di": di, "trend": trend, "macro": macro, "cash": cash, "late": late, "squeeze": squeeze}


def branch_specs() -> list[dict[str, Any]]:
    return [
        ("cp289A_cash_macro_vol_hold4", 4, "cash macro/DI vol bound(현금장 매크로/DI 변동성 제한)"),
        ("cp289B_cash_trend_zwide_hold6", 6, "cash trend/macro wider z(현금장 추세/매크로 넓은 z)"),
        ("cp289C_cash_late_strict_hold6", 6, "cash plus strict late(현금장 + 엄격 후반장)"),
        ("cp289D_trend_macro_all_hold4", 4, "all-session trend macro strict(전체 세션 추세 매크로 엄격)"),
        ("cp289E_cash_non_extreme_hold6", 6, "cash non-extreme density(현금장 비극단 밀도)"),
    ]


def build_signal(name: str, f: Mapping[str, np.ndarray]) -> np.ndarray:
    sig = f["sig"]
    score = f["score"]
    vol = f["vol"]
    zabs = f["zabs"]
    di = f["di"]
    trend = f["trend"]
    macro = f["macro"]
    cash = f["cash"]
    late = f["late"]
    squeeze = f["squeeze"]
    if name.startswith("cp289A"):
        mask = cash & (sig != 0) & (score >= 0.55) & ((macro == sig) | (di == sig)) & (vol >= 0.55) & (vol <= 1.35) & (zabs <= 1.35)
    elif name.startswith("cp289B"):
        mask = cash & (sig != 0) & (score >= 0.52) & ((trend == sig) | (macro == sig)) & (vol >= 0.50) & (vol <= 1.55) & (zabs <= 1.70)
    elif name.startswith("cp289C"):
        mask = (
            (cash & (score >= 0.55) & (zabs <= 1.40) & ((macro == sig) | (di == sig)))
            | (late & (score >= 0.62) & (zabs <= 1.10) & (macro == sig) & (trend == sig))
        ) & (sig != 0)
    elif name.startswith("cp289D"):
        mask = (sig != 0) & (score >= 0.58) & (trend == sig) & ((macro == sig) | (di == sig)) & (vol >= 0.55) & (vol <= 1.45) & (zabs <= 1.50)
    elif name.startswith("cp289E"):
        mask = cash & (sig != 0) & (score >= 0.50) & (vol <= 1.45) & (zabs <= 1.40) & (squeeze <= 1.0)
    else:
        raise ValueError(name)
    return np.where(mask, sig, 0).astype("int8")


def signal_label(value: int) -> str:
    return "long" if value > 0 else "short" if value < 0 else "flat"


def approximate_trades(signal: np.ndarray, hold_limit: int) -> int:
    trades = 0
    pos = 0
    hold = 0
    for value in signal.astype("int8"):
        current = int(value)
        if pos == 0:
            if current:
                trades += 1
                pos = current
                hold = 1
            continue
        hold += 1
        if current == 0:
            pos = 0
            hold = 0
        elif current == -pos:
            trades += 1
            pos = current
            hold = 1
        elif hold >= hold_limit:
            pos = 0
            hold = 0
    return trades


def materialize() -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[Path]]:
    frame, features = source_features()
    branch_rows: list[dict[str, Any]] = []
    supply_rows: list[dict[str, Any]] = []
    manifest_rows: list[dict[str, Any]] = []
    artifacts: list[Path] = []
    for index, (name, hold, thesis) in enumerate(branch_specs(), start=1):
        signal = build_signal(name, features)
        payload = frame.copy()
        branch_id = f"run289A_{name}"
        package_id = f"{name}_surface"
        payload["stage289_branch_id"] = branch_id
        payload["materialized_branch_id"] = branch_id
        payload["package_id"] = package_id
        payload["queue_role"] = "regime_conditioned_edge_surface"
        payload["fresh_thesis"] = thesis
        payload["route_signal_value"] = signal
        payload["route_signal_label"] = [signal_label(int(value)) for value in signal]
        payload["signal_active"] = (signal != 0).astype("int8")
        payload["max_hold_bars"] = hold
        payload["close_on_flat_signal"] = True
        payload["payload_claim_boundary"] = BOUNDARY
        surface_hash = hashlib.sha256(json.dumps({"name": name, "hold": hold, "thesis": thesis}, ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()
        feature_hash = ordered_hash(("route_signal_value",))
        payload["direction_surface_hash"] = surface_hash
        payload["direction_feature_order_hash"] = feature_hash
        payload_path = PAYLOAD_DIR / f"{branch_id}_payload.parquet"
        io_path(payload_path.parent).mkdir(parents=True, exist_ok=True)
        payload.to_parquet(io_path(payload_path), index=False)
        handoff_path = HANDOFF_DIR / f"{branch_id}_handoff.json"
        write_json(handoff_path, {"stage289_branch_id": branch_id, "package_id": package_id, "fresh_thesis": thesis, "max_hold_bars": hold, "close_on_flat_signal": True, "direction_surface_hash": surface_hash, "direction_feature_order_hash": feature_hash, "claim_boundary": BOUNDARY})
        counts: dict[tuple[str, str], dict[str, Any]] = {}
        for (tier, split), group in payload.groupby(["tier_scope", "split"], sort=False):
            if split not in {"validation", "oos"}:
                continue
            group_signal = as_num(group["route_signal_value"]).astype("int8").to_numpy()
            days = int(pd.to_datetime(group["timestamp"], utc=True).dt.date.nunique())
            approx = approximate_trades(group_signal, hold)
            counts[(str(tier), str(split))] = {"days": days, "rows": len(group), "active_signal_count": int((group_signal != 0).sum()), "active_signals_per_day": float((group_signal != 0).sum() / days), "long_signal_count": int((group_signal == 1).sum()), "short_signal_count": int((group_signal == -1).sum()), "max_hold_bars": hold, "approx_trade_count": approx, "approx_trades_per_day": float(approx / days)}
        for (tier, split), row in counts.items():
            supply_rows.append({**row, "materialized_branch_id": branch_id, "package_id": package_id, "tier_scope": tier, "split": split, "trade_density_screen": "in_target_band" if 4.0 <= row["approx_trades_per_day"] <= 10.0 else "outside_target_band"})
        val = counts.get(("Tier A", "validation"), {})
        oos = counts.get(("Tier A", "oos"), {})
        manifest_rows.append({"queue_id": f"run289A_queue_{index:02d}", "materialized_branch_id": branch_id, "stage289_branch_id": branch_id, "package_id": package_id, "queue_role": "regime_conditioned_edge_surface", "payload_path": rel(payload_path), "payload_hash": sha256_file_lf_normalized(payload_path), "handoff_path": rel(handoff_path), "handoff_hash": sha256_file_lf_normalized(handoff_path), "direction_surface_hash": surface_hash, "direction_feature_order_hash": feature_hash, "max_hold_bars": hold, "close_on_flat_signal": True, "same_direction_reentry_cooldown_bars": 0, "approx_validation_trades_per_day": val.get("approx_trades_per_day", 0), "approx_oos_trades_per_day": oos.get("approx_trades_per_day", 0), "selected_candidate": "none", "adapter_package": "none", "onnx_readiness": "not_claimed", "claim_boundary": BOUNDARY})
        branch_rows.append({"stage289_branch_id": branch_id, "materialized_branch_id": branch_id, "package_id": package_id, "fresh_thesis": thesis, "decision_surface": name, "risk_logic": f"max_hold={hold};close_on_flat=true", "max_hold_bars": hold, "close_on_flat_signal": True, "claim_boundary": BOUNDARY})
        artifacts.extend([payload_path, handoff_path])
    return branch_rows, supply_rows, manifest_rows, artifacts


def report_markdown(manifest_rows: Sequence[Mapping[str, Any]]) -> str:
    lines = [f"- `{row['package_id']}`: validation approx(검증 근사) `{float(row['approx_validation_trades_per_day']):.2f}`, OOS approx(표본외 근사) `{float(row['approx_oos_trades_per_day']):.2f}` trades/day(일 거래), max_hold(최대 보유) `{row['max_hold_bars']}`." for row in manifest_rows]
    return f"# run289A Regime Conditioned Edge Materialization(289A 국면 조건부 엣지 물질화)\n\n- status(상태): `{STATUS}`\n- judgment(판정): `{JUDGMENT}`\n- branch_count(분기 수): `{len(manifest_rows)}`\n- selected_candidate(선택 후보): `none`\n- Adapter package(어댑터 패키지): `none`\n- ONNX readiness(온엑스 준비): `not_claimed`\n- next_action(다음 행동): `{NEXT_ACTION}`\n\n## Queue(대기열)\n\n{chr(10).join(lines)}\n"


def write_outputs(branch_rows: Sequence[Mapping[str, Any]], supply_rows: Sequence[Mapping[str, Any]], manifest_rows: Sequence[Mapping[str, Any]], artifacts: Sequence[Path], created_at: str) -> list[Path]:
    for path in (RUN_ROOT, PAYLOAD_DIR, HANDOFF_DIR, REVIEWS):
        io_path(path).mkdir(parents=True, exist_ok=True)
    write_csv(BRANCH_QUEUE, BRANCH_COLUMNS, branch_rows)
    write_csv(CANDIDATE_SUPPLY, SUPPLY_COLUMNS, supply_rows)
    write_csv(PAYLOAD_MANIFEST, MANIFEST_COLUMNS, manifest_rows)
    write_csv(MT5_QUEUE, MANIFEST_COLUMNS, manifest_rows)
    write_csv(RESULT_JUDGMENT, RESULT_COLUMNS, [{"result_subject": RUN_ID, "evidence_available": rel(PAYLOAD_MANIFEST), "evidence_missing": "MT5 runtime KPI and curve review", "judgment_label": JUDGMENT, "judgment_class": "inconclusive_until_mt5_probe(탐침 전 불충분)", "claim_boundary": BOUNDARY, "next_condition": NEXT_ACTION, "user_explanation_hook": "국면 조건부 엣지 후보 입력을 만들었지만 성과 후보는 아니다."}])
    write_csv(GATE_AUDIT, GATE_COLUMNS, [{"gate_name": "fresh_edge_surface(새 엣지 표면)", "status": "passed", "evidence_path": rel(BRANCH_QUEUE), "effect": "exit-only repair(청산 단독 수리)를 끊고 국면 조건부 판단 표면을 만들었다."}, {"gate_name": "no_candidate_no_onnx_claim(후보와 온엑스 주장 없음)", "status": "passed", "evidence_path": rel(RESULT_JUDGMENT), "effect": "MT5 전 성과 주장을 막는다."}])
    write_md(REPORT, report_markdown(manifest_rows))
    final = [BRANCH_QUEUE, CANDIDATE_SUPPLY, PAYLOAD_MANIFEST, MT5_QUEUE, RESULT_JUDGMENT, GATE_AUDIT, REPORT, *artifacts]
    write_json(LINEAGE, {"run_id": RUN_ID, "producer": PRODUCER.as_posix(), "source_artifacts": [rel(SOURCE_E)], "produced_artifacts": [rel(path) for path in final if path_exists(path)], "claim_boundary": BOUNDARY})
    final.append(LINEAGE)
    write_json(RUN_MANIFEST, {"stage_id": STAGE_ID, "run_id": RUN_ID, "status": STATUS, "judgment": JUDGMENT, "created_at_utc": created_at, "branch_count": len(manifest_rows), "mt5_queue_rows": len(manifest_rows), "next_action": NEXT_ACTION, "selected_candidate": "none", "adapter_package": "none", "onnx_readiness": "not_claimed", "claim_boundary": BOUNDARY})
    final.append(RUN_MANIFEST)
    return [path for path in final if path_exists(path)]


def update_docs(created_at: str, artifacts: Sequence[Path], manifest_rows: Sequence[Mapping[str, Any]]) -> None:
    upsert_csv(RUN_REGISTRY, RUN_REGISTRY_COLUMNS, [{"run_id": RUN_ID, "stage_id": STAGE_ID, "lane": "regime_conditioned_edge_materialization", "status": STATUS, "judgment": JUDGMENT, "path": rel(REPORT), "notes": f"branches={len(manifest_rows)};next_action={NEXT_ACTION}"}], key="run_id")
    upsert_csv(ALPHA_LEDGER, ALPHA_LEDGER_COLUMNS, [{"ledger_row_id": f"{RUN_ID}__materialization", "stage_id": STAGE_ID, "run_id": RUN_ID, "subrun_id": RUN_NUMBER, "parent_run_id": "run288C_review_risk_reward_exit_asymmetry_mt5_probe_v1", "record_view": "regime_conditioned_edge_materialization", "tier_scope": "Tier A/Tier B/Tier A+B", "kpi_scope": "structural_scout", "scoreboard_lane": "regime_conditioned_edge", "status": STATUS, "judgment": JUDGMENT, "path": rel(REPORT), "primary_kpi": f"mt5_queue_rows={len(manifest_rows)}", "guardrail_kpi": "no_candidate_claim", "external_verification_status": "not_attempted_run289A_materialization", "notes": "MT5 probe required before result judgment."}], key="ledger_row_id")
    upsert_csv(STAGE_LEDGER, STAGE_LEDGER_COLUMNS, [{"row_id": f"{RUN_ID}__materialization", "stage_id": STAGE_ID, "run_id": RUN_ID, "view": "regime_conditioned_edge_materialization", "tier_scope": "Tier A/Tier B/Tier A+B", "scoreboard": "candidate_supply_diagnostics", "status": STATUS, "judgment": JUDGMENT, "evidence_boundary": "no_candidate_no_adapter_no_onnx", "report_path": rel(REPORT), "notes": f"mt5_queue_rows={len(manifest_rows)};next_action={NEXT_ACTION}"}], key="row_id")
    artifact_rows = [{"artifact_id": f"{RUN_ID}__{hashlib.sha1(rel(path).encode('utf-8')).hexdigest()[:12]}", "artifact_type": "stage289_regime_edge_artifact", "path": rel(path), "sha256": sha256_file_lf_normalized(path), "stage_id": STAGE_ID, "run_id": RUN_ID, "created_at_utc": created_at, "notes": "run289A regime conditioned edge materialization(289A 국면 조건부 엣지 물질화)"} for path in artifacts if path_exists(path)]
    upsert_csv(ARTIFACT_REGISTRY, ARTIFACT_COLUMNS, artifact_rows, key="artifact_id")
    selected = io_path(SELECTED).read_text(encoding="utf-8-sig")
    selected = replace_line_prefix(selected, "- stage_status(단계 상태):", f"- stage_status(단계 상태): `{STATUS}`")
    selected = replace_line_prefix(selected, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    selected = replace_line_prefix(selected, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    selected = append_once(selected, "run289A_report", f"- run289A_report(289A 보고서): `{rel(REPORT)}`")
    selected = append_once(selected, "run289A_mt5_queue", f"- run289A_mt5_queue(289A MT5 대기열): `{rel(MT5_QUEUE)}`")
    write_md(SELECTED, selected)
    review_index = io_path(REVIEW_INDEX).read_text(encoding="utf-8-sig")
    review_index = append_once(review_index, "run289A_report", f"- run289A_report(289A 보고서): `{rel(REPORT)}`")
    write_md(REVIEW_INDEX, review_index)
    current = io_path(CURRENT_STATE).read_text(encoding="utf-8-sig")
    current = replace_line_prefix(current, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_line_prefix(current, "- status(상태):", f"- status(상태): `{STATUS}`")
    current = replace_line_prefix(current, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    current = append_once(current, "run289A_summary", f"- run289A_summary(289A 요약): regime-conditioned edge surface(국면 조건부 엣지 표면) 후보 `{len(manifest_rows)}`개를 물질화했다. Effect(효과): session/volatility/macro/trend(세션/변동성/매크로/추세) 조건으로 MT5 탐침 대기열을 만든다.")
    write_md(CURRENT_STATE, current)
    workspace = io_path(WORKSPACE_STATE).read_text(encoding="utf-8-sig")
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    workspace = replace_line_prefix(workspace, "updated_on:", f"updated_on: '{UPDATED_ON}'")
    focus = f"- >-\n  Stage289(289단계) run289A(289A 실행) regime-conditioned edge materialization(국면 조건부 엣지 물질화) `{RUN_ID}`. Effect(효과): 후보 `{len(manifest_rows)}`개를 MT5 probe(MT5 탐침) 대기열로 넘기며 후보/어댑터/온엑스 주장은 하지 않는다.\n"
    workspace = prepend_focus(workspace, focus, RUN_ID)
    write_md(WORKSPACE_STATE, workspace)
    changelog = io_path(CHANGELOG).read_text(encoding="utf-8-sig")
    changelog = append_once(changelog, RUN_ID, f"## {UPDATED_ON} run289A Regime-conditioned edge materialization(289A 국면 조건부 엣지 물질화)\n\n- status(상태): `{STATUS}`\n- judgment(판정): `{JUDGMENT}`\n- effect(효과): 후보 `{len(manifest_rows)}`개를 MT5 probe queue(MT5 탐침 대기열)로 만들었다.\n- boundary(경계): selected candidate(선택 후보), Adapter package(어댑터 패키지), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 `none/not_claimed`다.\n")
    write_md(CHANGELOG, changelog)


def main() -> None:
    created_at = utc_now()
    branch_rows, supply_rows, manifest_rows, payload_artifacts = materialize()
    artifacts = write_outputs(branch_rows, supply_rows, manifest_rows, payload_artifacts, created_at)
    update_docs(created_at, artifacts, manifest_rows)
    print(json.dumps({"run_id": RUN_ID, "status": STATUS, "judgment": JUDGMENT, "branch_count": len(manifest_rows), "mt5_queue_rows": len(manifest_rows), "selected_candidate": "none", "adapter_package": "none", "onnx_readiness": "not_claimed", "goal_achieve": "not_claimed", "next_action": NEXT_ACTION}, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
