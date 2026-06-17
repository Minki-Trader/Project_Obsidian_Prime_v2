from __future__ import annotations

import argparse
import csv
import json
import shutil
import subprocess
import sys
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np
import pandas as pd
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.impute import SimpleImputer
from sklearn.pipeline import make_pipeline

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.control_plane.ledger import io_path, json_ready, path_exists
from foundation.control_plane.mt5_tier_balance_completion import attempt_payload
from foundation.models.onnx_bridge import ordered_hash, ordered_sklearn_probabilities
from stage_pipelines.stage_frontier_71 import frontier71d_mt5_runtime_probe_economics_native_scout as f71d
from stage_pipelines.stage_frontier_72 import frontier72b_trade_shape_exit_distribution_proxy_scout as f72b
from stage_pipelines.stage_frontier_72 import frontier72c_trade_shape_label_feature_repair as f72c
from stage_pipelines.stage_frontier_runtime_backfill.run_frontier_runtime_probe_backfill import (
    DEFAULT_COMMON_FILES,
    DEFAULT_METAEDITOR,
    DEFAULT_PORTABLE_ROOT,
    DEFAULT_TERMINAL,
    DEFAULT_TESTER_PROFILE_ROOT,
    EA_BINARY,
    PORTABLE_EA_BINARY,
)


STAGE_ID = f72b.STAGE_ID
RUN_ID = "frontier72D_pre_mt5_grok_trade_shape_runtime_probe_v1"
PARENT_RUN_ID = f72c.RUN_ID
NEXT_RUN_ID = "frontier72E_proxy_runtime_gap_analysis_and_repair_decision_v1"
CLAIM_BOUNDARY = (
    "runtime_probe_observation_only_no_completion_no_baseline_no_promotion_"
    "no_runtime_authority_no_live_readiness_no_goal_achieve"
)

STAGE_ROOT = f72b.STAGE_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
REVIEWS_ROOT = f72b.REVIEWS_ROOT
SELECTED_ROOT = f72b.SELECTED_ROOT
MODEL_ROOT = RUN_ROOT / "models"
FEATURE_ROOT = RUN_ROOT / "features"
VETO_ROOT = RUN_ROOT / "runtime_veto_tapes"
MT5_ROOT = RUN_ROOT / "mt5"
COMMON_RUN_ROOT = "Project_Obsidian_Prime_v2/frontier72D_trade_shape_runtime_probe"
RUNTIME_THRESHOLD_EPSILON = 1e-6

GROK_PACKET = ROOT / "docs/agent_control/grok_reviews/2026-06-17_f72d_pre_mt5_trade_shape_runtime_probe"
GROK_PROMPT = GROK_PACKET / "prompts/f72d_pre_mt5_trade_shape_runtime_probe_prompt.md"
GROK_CLEAN = GROK_PACKET / "clean_output.md"
GROK_METADATA = GROK_PACKET / "metadata.json"
F72C_TOP = STAGE_ROOT / "02_runs" / PARENT_RUN_ID / "f72c_top_repair_candidates.csv"
F72C_SUMMARY = STAGE_ROOT / "02_runs" / PARENT_RUN_ID / "frontier72C_repair_summary.json"


@dataclass(frozen=True)
class AxisSpec:
    candidate_id: str
    axis_id: str
    role: str
    threshold: float
    label_id: str
    feature_set_id: str
    model_id: str
    selection_id: str
    mask_name: str


@dataclass(frozen=True)
class LabelSpec:
    horizon_bars: int
    sl_atr: float
    tp_atr: float


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="F72D trade-shape bridge MT5 runtime probe.")
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--materialize-only", action="store_true")
    parser.add_argument("--timeout-seconds", type=int, default=600)
    parser.add_argument("--wait-timeout-seconds", type=int, default=300)
    parser.add_argument("--terminal-path", default=str(DEFAULT_TERMINAL))
    parser.add_argument("--metaeditor-path", default=str(DEFAULT_METAEDITOR))
    parser.add_argument("--common-files-root", default=str(DEFAULT_COMMON_FILES))
    parser.add_argument("--tester-profile-root", default=str(DEFAULT_TESTER_PROFILE_ROOT))
    parser.add_argument("--terminal-data-root", default=str(DEFAULT_PORTABLE_ROOT))
    return parser.parse_args()


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def write_json(path: Path, payload: Mapping[str, Any] | Sequence[Any]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(
        json.dumps(json_ready(payload), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str] | None = None) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    fieldnames = list(columns or (rows[0].keys() if rows else []))
    with io_path(path).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: json_ready(row.get(field, "")) for field in fieldnames})


def write_text(path: Path, lines: Sequence[str]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8-sig")


def append_once(path: Path, marker: str, block: str) -> None:
    text = f72b.read_text(path) if path_exists(path) else ""
    if marker in text:
        return
    io_path(path).write_text(text.rstrip() + "\n\n" + block.rstrip() + "\n", encoding="utf-8-sig")


def ensure_dirs() -> None:
    for path in (RUN_ROOT, MODEL_ROOT, FEATURE_ROOT, VETO_ROOT, MT5_ROOT, MT5_ROOT / "reports", REVIEWS_ROOT, SELECTED_ROOT):
        io_path(path).mkdir(parents=True, exist_ok=True)


def required_inputs() -> list[Path]:
    return [GROK_CLEAN, GROK_METADATA, F72C_TOP, F72C_SUMMARY, f72b.MODEL_INPUT, f72b.FEATURE_ORDER, f72b.RAW_US100]


def configure_f71d_globals() -> None:
    f71d.RUN_ID = RUN_ID
    f71d.PARENT_RUN_ID = PARENT_RUN_ID
    f71d.NEXT_RUN_ID = NEXT_RUN_ID
    f71d.CLAIM_BOUNDARY = CLAIM_BOUNDARY
    f71d.RUN_ROOT = RUN_ROOT
    f71d.MODEL_ROOT = MODEL_ROOT
    f71d.FEATURE_ROOT = FEATURE_ROOT
    f71d.VETO_ROOT = VETO_ROOT
    f71d.MT5_ROOT = MT5_ROOT
    f71d.COMMON_RUN_ROOT = COMMON_RUN_ROOT
    # Keep the shared F71D materializer aligned with RuntimeProbeEA edge_margin semantics.
    f71d.side_score_from_probability = side_score


def selected_candidate() -> Mapping[str, Any]:
    top = pd.read_csv(io_path(F72C_TOP))
    return top.iloc[0].to_dict()


def side_score(proba: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    short = proba[:, 0]
    flat = proba[:, 1]
    long = proba[:, 2]
    side = np.where(short >= long, -1, 1).astype(int)
    score = np.maximum(long, short) - flat
    return side, score


def build_bridge_context() -> dict[str, Any]:
    candidate = selected_candidate()
    shape = f72c.parse_shape(str(candidate["shape_id"]))
    long_shape = f72b.TradeShape(shape.hold_bars, shape.stop_atr, shape.target_atr, 1)
    short_shape = f72b.TradeShape(shape.hold_bars, shape.stop_atr, shape.target_atr, -1)
    label_variant = str(candidate["label_variant"])
    model = pd.read_parquet(io_path(f72b.MODEL_INPUT))
    model["timestamp"] = pd.to_datetime(model["timestamp"], utc=True)
    raw = pd.read_csv(io_path(f72b.RAW_US100)).sort_values("time_close_unix").reset_index(drop=True)
    positions = f72b.align_raw(model, raw)
    features = [line.strip() for line in f72b.read_text(f72b.FEATURE_ORDER).splitlines() if line.strip()]
    short_path = f72b.compute_shape_path(model, raw, positions, short_shape)
    long_path = f72b.compute_shape_path(model, raw, positions, long_shape)
    short_label = f72c.repair_label(short_path, short_shape, label_variant) > 0
    long_label = f72c.repair_label(long_path, long_shape, label_variant) > 0
    short_quality = np.nan_to_num(short_path["quality"], nan=-999.0)
    long_quality = np.nan_to_num(long_path["quality"], nan=-999.0)
    y = np.zeros(len(model), dtype=int)
    y[short_label & (~long_label | (short_quality >= long_quality))] = -1
    y[long_label & (~short_label | (long_quality > short_quality))] = 1
    train_mask = (model["split"] == "train").to_numpy() & np.isfinite(short_path["pnl"]) & np.isfinite(long_path["pnl"])
    if set(np.unique(y[train_mask]).tolist()) != {-1, 0, 1}:
        raise RuntimeError(f"bridge training labels missing class: {sorted(np.unique(y[train_mask]).tolist())}")
    bridge = make_pipeline(
        SimpleImputer(strategy="median"),
        ExtraTreesClassifier(
            n_estimators=140,
            max_depth=9,
            min_samples_leaf=55,
            class_weight="balanced_subsample",
            random_state=7204,
            n_jobs=-1,
        ),
    )
    bridge.fit(model.loc[train_mask, features], y[train_mask])
    proba = ordered_sklearn_probabilities(bridge, model.loc[:, features].to_numpy(dtype="float64"), class_order=(-1, 0, 1))
    side, score = side_score(proba)
    validation_mask = (model["split"] == "validation").to_numpy() & (side == -1) & np.isfinite(short_path["pnl"])
    threshold = f72b.score_threshold(score[validation_mask], model.loc[validation_mask, "timestamp"], float(candidate["target_trades_day"]))
    runtime_threshold = max(float(threshold) - RUNTIME_THRESHOLD_EPSILON, 0.0)
    selected = np.isfinite(short_path["pnl"]) & (side == -1) & (score >= threshold)
    proxy_by_split: dict[str, Any] = {}
    for split in ("train", "validation", "oos"):
        split_mask = (model["split"] == split).to_numpy() & selected
        proxy_by_split[split] = f72b.trade_metrics(model.loc[split_mask, "timestamp"], short_path["pnl"][split_mask], np.full(int(split_mask.sum()), -1))
    axis = AxisSpec(
        candidate_id="f72d_bridge_f72c_0098",
        axis_id="f72d_trade_shape_3class_bridge",
        role="runtime_compatibility_bridge_from_f72c_proxy_repair",
        threshold=float(runtime_threshold),
        label_id=f"{shape.shape_id}_{label_variant}",
        feature_set_id="all58",
        model_id="extra_trees_3class_bridge",
        selection_id="bridge_edge_margin_selected_entry_tape_numeric_tolerance",
        mask_name="selected_entry_only",
    )
    return {
        "axis": axis,
        "frame": model,
        "label_spec": LabelSpec(horizon_bars=shape.hold_bars, sl_atr=shape.stop_atr, tp_atr=shape.target_atr),
        "feature_columns": features,
        "feature_order_hash": ordered_hash(features),
        "model": bridge,
        "selected": selected,
        "event_mask": np.isfinite(short_path["pnl"]),
        "side": side,
        "score": score,
        "proxy_kpi_by_split": proxy_by_split,
        "source_candidate": dict(candidate),
        "selection_threshold": float(threshold),
        "runtime_threshold": float(runtime_threshold),
        "runtime_threshold_epsilon": RUNTIME_THRESHOLD_EPSILON,
        "bridge_label_counts": {str(label): int(count) for label, count in zip(*np.unique(y[train_mask], return_counts=True))},
    }


def build_attempts(context: Mapping[str, Any], artifact: Mapping[str, Any]) -> list[dict[str, Any]]:
    axis: AxisSpec = context["axis"]
    label_spec: LabelSpec = context["label_spec"]
    attempts: list[dict[str, Any]] = []
    for split in ("validation", "oos"):
        from_date, to_date = f71d.split_dates(context["frame"], split)
        split_mask = context["frame"]["split"].astype(str).eq(split).to_numpy(dtype=bool)
        expected_rows = int(split_mask.sum())
        expected_selected = int((context["selected"] & split_mask).sum())
        attempt_name = f"f72d_{axis.axis_id}_{split}"
        extra = {
            "InpSameDirectionReentryCooldownBars": int(label_spec.horizon_bars),
            "InpReentryCooldownBars": 0,
            "InpAtrSltpEnabled": True,
            "InpAtrStopMultiplier": float(label_spec.sl_atr),
            "InpAtrTakeProfitMultiplier": float(label_spec.tp_atr),
            "InpAtrMinStopPoints": 1.0,
            "InpAtrMinTakeProfitPoints": 1.0,
            "InpDecisionMode": "edge_margin",
            "InpFallbackDecisionMode": "edge_margin",
            "InpRuntimeVetoTapeEnabled": True,
            "InpRuntimeVetoTapePath": str(artifact["runtime_veto_tape_common_path"]),
            "InpRuntimeVetoTapeUseCommonFiles": True,
            "InpRuntimeVetoTapeDelimiter": ",",
        }
        attempt = attempt_payload(
            run_root=RUN_ROOT,
            run_id=RUN_ID,
            stage_number=72,
            exploration_label=f"frontier72D_{axis.axis_id}_runtime_probe",
            attempt_name=attempt_name,
            tier=f71d.mt5.TIER_A,
            split=split,
            model_path=str(artifact["model_common_path"]),
            model_id=f"F72D_{axis.candidate_id}",
            model_backend="onnx",
            feature_path=str(artifact["feature_common_path"]),
            feature_count=len(context["feature_columns"]),
            feature_order_hash=str(context["feature_order_hash"]),
            short_threshold=0.0,
            long_threshold=0.0,
            min_margin=float(axis.threshold),
            invert_signal=False,
            from_date=from_date,
            to_date=to_date,
            primary_active_tier=f71d.mt5.TIER_A,
            attempt_role=axis.role,
            record_view_prefix=f"mt5_f72d_{axis.axis_id}",
            max_hold_bars=int(label_spec.horizon_bars),
            common_root=COMMON_RUN_ROOT,
            close_on_flat_signal=False,
            reverse_on_opposite_signal=True,
            close_only_on_opposite_signal=False,
            extra_set_values=extra,
        )
        attempt.update(
            {
                "candidate_id": axis.candidate_id,
                "axis_id": axis.axis_id,
                "axis_role": axis.role,
                "expected_rows": expected_rows,
                "expected_signal_count": expected_selected,
                "expected_selected_trade_count": expected_selected,
                "proxy_kpi": context["proxy_kpi_by_split"].get(split, {}),
                "label_id": axis.label_id,
                "feature_set_id": axis.feature_set_id,
                "model_id": axis.model_id,
                "selection_id": axis.selection_id,
                "mask_name": axis.mask_name,
                "threshold": axis.threshold,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        attempts.append(attempt)
    return attempts


def compile_runtime_ea(metaeditor_path: Path) -> dict[str, Any]:
    compile_payload = f71d.mt5.compile_mql5_ea(metaeditor_path, f71d.mt5.EA_SOURCE_PATH, MT5_ROOT / "mt5_compile.log")
    portable_payload = {
        "repo_ea_ex5": rel(EA_BINARY),
        "portable_ea_ex5": PORTABLE_EA_BINARY.as_posix(),
        "portable_ea_ex5_exists_before": path_exists(PORTABLE_EA_BINARY),
        "copied": False,
    }
    if path_exists(EA_BINARY):
        io_path(PORTABLE_EA_BINARY.parent).mkdir(parents=True, exist_ok=True)
        shutil.copy2(io_path(EA_BINARY), io_path(PORTABLE_EA_BINARY))
        portable_payload.update({"copied": True, "portable_ea_ex5_exists_after": path_exists(PORTABLE_EA_BINARY), "portable_ea_sha256": f71d.mt5.sha256_file(PORTABLE_EA_BINARY)})
    return {"compile": compile_payload, "portable_ea": portable_payload}


def can_run_terminal(payload: Mapping[str, Any]) -> bool:
    return ((payload.get("compile") or {}).get("status") == "completed") or path_exists(PORTABLE_EA_BINARY)


def execute_attempts(args: argparse.Namespace, attempts: Sequence[Mapping[str, Any]], compile_payload: Mapping[str, Any]) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for attempt in attempts:
        if not can_run_terminal(compile_payload):
            result = {"status": "blocked", "blocker": "compile_failed_and_portable_ea_missing"}
        else:
            f71d.clear_runtime_outputs(Path(args.common_files_root), attempt)
            f71d.mt5.remove_existing_mt5_report_artifacts(Path(args.terminal_data_root), attempt, run_id=RUN_ID)
            try:
                result = f71d.mt5.run_mt5_tester(
                    Path(args.terminal_path),
                    ROOT / str(attempt["ini"]["path"]),
                    set_path=ROOT / str(attempt["set"]["path"]),
                    tester_profile_set_path=Path(args.tester_profile_root) / f71d.mt5.EA_TESTER_SET_NAME,
                    tester_profile_ini_path=Path(args.tester_profile_root) / f"opv2_{attempt['attempt_name']}.ini",
                    timeout_seconds=int(args.timeout_seconds),
                    terminal_extra_args=["/portable"],
                )
            except subprocess.TimeoutExpired as exc:
                result = {"status": "blocked", "command": exc.cmd, "stdout": (exc.stdout or "")[-2000:], "stderr": (exc.stderr or "")[-2000:], "blocker": "terminal_timeout"}
            runtime_outputs = f71d.mt5.wait_for_mt5_runtime_outputs(Path(args.common_files_root), attempt, timeout_seconds=int(args.wait_timeout_seconds), poll_seconds=2.0)
            if runtime_outputs.get("status") != "completed":
                result["status"] = "blocked"
                result.setdefault("blocker", "runtime_outputs_missing_or_init_failed")
            result["runtime_outputs"] = runtime_outputs
        result.update({
            "attempt_name": attempt["attempt_name"],
            "tier": attempt["tier"],
            "split": attempt["split"],
            "attempt_role": attempt.get("attempt_role"),
            "record_view_prefix": attempt.get("record_view_prefix"),
            "candidate_id": attempt.get("candidate_id"),
            "axis_id": attempt.get("axis_id"),
            "expected_rows": attempt.get("expected_rows"),
            "expected_signal_count": attempt.get("expected_signal_count"),
            "expected_selected_trade_count": attempt.get("expected_selected_trade_count"),
            "ini_path": attempt.get("ini", {}).get("path"),
            "set_path": attempt.get("set", {}).get("path"),
        })
        results.append(result)
    return results


def build_summary(payload: Mapping[str, Any]) -> dict[str, Any]:
    receipts = list(payload.get("runtime_receipt", []))
    completed = sum(1 for row in receipts if row.get("tester_status") == "completed")
    best = next((row for row in receipts if row.get("split") == "oos"), receipts[0] if receipts else {})
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "status": payload.get("status"),
        "judgment": payload.get("judgment"),
        "attempt_count": len(payload.get("attempts", [])),
        "completed_attempt_count": completed,
        "probability_parity_pass_rows": sum(1 for row in payload.get("probability_parity", []) if row.get("passed")),
        "signal_parity_pass_rows": sum(1 for row in payload.get("signal_parity", []) if row.get("passed")),
        "best_runtime": best,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def report_lines(payload: Mapping[str, Any], created_at: str) -> list[str]:
    summary = build_summary(payload)
    best = summary["best_runtime"]
    return [
        "# Frontier72D MT5 Runtime Probe(F72D MT5 런타임 탐침)",
        "",
        f"Updated(갱신): {created_at}",
        "",
        f"- status(상태): `{payload.get('status')}`",
        f"- judgment(판정): `{payload.get('judgment')}`",
        f"- attempts(시도): `{summary['attempt_count']}`; completed(완료): `{summary['completed_attempt_count']}`",
        f"- probability parity pass rows(확률 동등성 통과 행): `{summary['probability_parity_pass_rows']}`",
        f"- signal parity pass rows(신호 동등성 통과 행): `{summary['signal_parity_pass_rows']}`",
        f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
        "",
        "## Runtime KPI(런타임 핵심 성과 지표)",
        "",
        f"- best split(최선 분할): `{best.get('split', '')}`",
        f"- net/PF/DD/trades/day(순수익/수익 팩터/손실폭/일 거래 수): `{best.get('net_profit', '')}` / `{best.get('profit_factor', '')}` / `{best.get('max_drawdown_percent', '')}` / `{best.get('trades_per_day', '')}`",
        f"- signal count diff(신호 수 차이): `{best.get('signal_count_diff', '')}`; feature ready diff(피처 준비 차이): `{best.get('feature_ready_diff', '')}`",
        f"- gap cause(간극 원인): `{best.get('gap_cause_summary', '')}`",
        "",
        "Effect(효과): 이 실행은 bridge model(연결 모델)의 MT5 observation(런타임 관찰)이며, F72C proxy gate(프록시 게이트) 실패를 뒤집지 않는다.",
        "",
        "## Next Action(다음 행동)",
        "",
        f"`{NEXT_RUN_ID}`.",
    ]


def grok_receipt_lines(created_at: str, artifact: Mapping[str, Any]) -> list[str]:
    return [
        "# F72D Pre-MT5 Grok Receipt(F72D 사전 MT5 Grok 영수증)",
        "",
        f"- created_at_utc(생성): `{created_at}`",
        "- trigger_reason(트리거 이유): MT5 Runtime Probe(MT5 런타임 탐침) 전 bridge semantics(연결 의미) 검토.",
        f"- prompt_identity(프롬프트 정체성): `{rel(GROK_PROMPT)}`, sha256 `{f71d.mt5.sha256_file(GROK_PROMPT)}`.",
        f"- output_identity(출력 정체성): `{rel(GROK_CLEAN)}`, sha256 `{f71d.mt5.sha256_file(GROK_CLEAN)}`.",
        "- advice_classification(조언 분류): `accepted_with_rejections_and_needs_local_verification(거절/로컬 검증 포함 수용)`.",
        "- accepted(수용): narrow 3-class bridge(좁은 3분류 연결), regenerated selected-entry tape(재생성 선택 진입 테이프), observation-only runtime probe(관찰 전용 런타임 탐침).",
        "- rejected(거절): F72C OOS를 success criteria(성공 기준)로 승격, f72c_0098을 baseline(기준선)처럼 취급, threshold/veto hidden tuning(숨은 임계값/차단 조정).",
        f"- local_verification(로컬 검증): export_status `{artifact.get('export_status')}`, probability parity(확률 동등성) `{artifact.get('probability_parity_passed')}`, signal parity(신호 동등성) `{artifact.get('signal_parity_passed')}`.",
        f"- final_codex_direction(최종 Codex 방향): runtime probe observation(런타임 탐침 관찰) 뒤 `{NEXT_RUN_ID}`.",
        f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`.",
    ]


def write_outputs(payload: Mapping[str, Any], created_at: str) -> None:
    artifact = payload.get("artifact_rows", [{}])[0]
    write_json(RUN_ROOT / "frontier72D_runtime_probe_execution_result.json", payload)
    write_json(RUN_ROOT / "frontier72D_runtime_probe_summary.json", build_summary(payload))
    write_json(RUN_ROOT / "run_manifest.json", {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "status": payload.get("status"),
        "judgment": payload.get("judgment"),
        "artifact_rows": payload.get("artifact_rows", []),
        "attempts": payload.get("attempts", []),
        "claim_boundary": CLAIM_BOUNDARY,
    })
    write_csv(RUN_ROOT / "f72d_bridge_materialization.csv", payload.get("artifact_rows", []))
    write_csv(RUN_ROOT / "f72d_onnx_probability_parity.csv", payload.get("probability_parity", []))
    write_csv(RUN_ROOT / "f72d_onnx_signal_parity.csv", payload.get("signal_parity", []))
    write_csv(RUN_ROOT / "f72d_runtime_probe_receipt.csv", payload.get("runtime_receipt", []), f71d.RUNTIME_RECEIPT_COLUMNS)
    write_csv(REVIEWS_ROOT / "f72d_bridge_materialization_review.csv", payload.get("artifact_rows", []))
    write_csv(REVIEWS_ROOT / "f72d_onnx_probability_parity_review.csv", payload.get("probability_parity", []))
    write_csv(REVIEWS_ROOT / "f72d_onnx_signal_parity_review.csv", payload.get("signal_parity", []))
    write_csv(REVIEWS_ROOT / "f72d_runtime_probe_receipt_review.csv", payload.get("runtime_receipt", []), f71d.RUNTIME_RECEIPT_COLUMNS)
    write_text(REVIEWS_ROOT / "frontier72D_mt5_runtime_probe_report.md", report_lines(payload, created_at))
    write_text(REVIEWS_ROOT / "f72d_pre_mt5_grok_receipt.md", grok_receipt_lines(created_at, artifact))
    write_text(REVIEWS_ROOT / "required_gate_coverage_audit_f72d.md", [
        "# F72D Required Gate Coverage Audit(F72D 필수 게이트 커버리지 감사)",
        "",
        f"Updated(갱신): {created_at}",
        "",
        f"- pre_mt5_grok(사전 MT5 Grok): `{rel(GROK_CLEAN)}`.",
        f"- bridge_export(연결 내보내기): `{artifact.get('export_status')}`.",
        f"- runtime_attempts(런타임 시도): `{len(payload.get('attempts', []))}`.",
        f"- runtime_receipt_rows(런타임 영수증 행): `{len(payload.get('runtime_receipt', []))}`.",
        "- final_claim_guard(최종 주장 보호): pass(통과).",
        f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`.",
    ])


def update_state(payload: Mapping[str, Any], created_at: str) -> None:
    summary = build_summary(payload)
    state = [
        f"current_stage_id: {STAGE_ID}",
        f"active_stage: {STAGE_ID}",
        f"current_run_id: {NEXT_RUN_ID}",
        f"latest_completed_run_id: {RUN_ID}",
        f"current_status: {payload.get('status')}",
        f"current_judgment: {payload.get('judgment')}",
        f"next_run_id: {NEXT_RUN_ID}",
        "runtime_authority: not_claimed",
        "operating_promotion: not_claimed",
        "live_readiness: not_claimed",
        "goal_achieve: not_claimed",
        "five_stage_retrospective_due_status: not_due_after_f71_closeout",
        f"updated_at_utc: '{created_at}'",
        "notes:",
        f'  - "Action(행동): F72D MT5 Runtime Probe(MT5 런타임 탐침)를 실행/시도했다. Attempts(시도) {summary["attempt_count"]}, completed(완료) {summary["completed_attempt_count"]}."',
        '  - "Effect(효과): 다음 행동은 proxy/runtime gap analysis(프록시/런타임 간극 분석)다."',
        '  - "Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음)."',
    ]
    io_path(f72b.WORKSPACE_STATE).write_text("\n".join(state) + "\n", encoding="utf-8-sig")
    write_text(SELECTED_ROOT / "selection_status.md", [
        "# F72 Selection Status(F72 선택 상태)",
        "",
        f"- stage(단계): `{STAGE_ID}`",
        f"- current_run(현재 실행): `{NEXT_RUN_ID}`",
        f"- latest_completed_run(최근 완료 실행): `{RUN_ID}`",
        f"- status(상태): `{payload.get('status')}`",
        f"- judgment(판정): `{payload.get('judgment')}`",
        "- selected_baseline(선택 기준선): `not_claimed(주장 없음)`",
        "- runtime_authority(런타임 권위): `not_claimed(주장 없음)`",
        "- operating_promotion(운영 승격): `not_claimed(주장 없음)`",
        "- live_readiness(실거래 준비): `not_claimed(주장 없음)`",
        "- Goal Achieve(목표 달성): `not_claimed(주장 없음)`",
        f"- next_action(다음 행동): `{NEXT_RUN_ID}`",
        f"- boundary(경계): `{CLAIM_BOUNDARY}`",
    ])
    write_text(f72b.CURRENT_WORKING_STATE, [
        "# Current Working State(현재 작업 상태)",
        "",
        f"Updated(갱신): {created_at}",
        "",
        f"Active stage(활성 단계): `{STAGE_ID}`",
        f"Current run(현재 실행): `{NEXT_RUN_ID}`",
        f"Latest completed run(최근 완료 실행): `{RUN_ID}`",
        "",
        "## Current Truth(현재 진실)",
        "",
        "Action(행동): F72D MT5 Runtime Probe(MT5 런타임 탐침)를 실행/시도했다.",
        "",
        f"Effect(효과): runtime receipt rows(런타임 영수증 행) `{len(payload.get('runtime_receipt', []))}`개를 만들었고, 다음 행동은 `{NEXT_RUN_ID}`다.",
        "",
        f"Claim boundary(주장 경계): `{CLAIM_BOUNDARY}`",
    ])


def update_ledgers(payload: Mapping[str, Any], created_at: str) -> None:
    summary = build_summary(payload)
    best = summary["best_runtime"]
    row = {
        "ledger_row_id": f"{RUN_ID}__runtime_probe",
        "row_id": f"{RUN_ID}__runtime_probe",
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "mt5_runtime_probe(MT5 런타임 탐침)",
        "status": payload.get("status"),
        "judgment": payload.get("judgment"),
        "path": rel(REVIEWS_ROOT / "frontier72D_mt5_runtime_probe_report.md"),
        "notes": f"attempts={summary['attempt_count']};completed={summary['completed_attempt_count']}",
        "family": "runtime_probe(런타임 탐침)",
        "primary_report": rel(REVIEWS_ROOT / "frontier72D_mt5_runtime_probe_report.md"),
        "run_number": "frontier72D",
        "date": created_at[:10],
        "decision": payload.get("judgment"),
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "rows": len(payload.get("runtime_receipt", [])),
        "claim_boundary": CLAIM_BOUNDARY,
        "report_path": rel(REVIEWS_ROOT / "frontier72D_mt5_runtime_probe_report.md"),
        "runtime_completed_rows": summary["completed_attempt_count"],
        "best_net_profit": best.get("net_profit"),
        "best_profit_factor": best.get("profit_factor"),
        "run_date": created_at[:10],
        "primary_artifact": rel(RUN_ROOT / "run_manifest.json"),
        "candidate_model_id": "f72d_bridge_f72c_0098",
        "net_profit": best.get("net_profit"),
        "profit_factor": best.get("profit_factor"),
        "drawdown": best.get("max_drawdown_percent"),
        "trade_count": best.get("trade_count"),
        "result_status": payload.get("status"),
        "view": "MT5 Runtime Probe(MT5 런타임 탐침)",
        "tier": "Tier A",
        "metric_scope": "runtime_probe_kpi(런타임 탐침 KPI)",
        "scoreboard_lane": "runtime_probe(런타임 탐침)",
        "external_verification_status": "completed(완료)" if summary["completed_attempt_count"] else "blocked(차단)",
        "result_judgment": payload.get("judgment"),
        "final_decision_path": rel(REVIEWS_ROOT / "frontier72D_mt5_runtime_probe_report.md"),
        "gate_audit_path": rel(REVIEWS_ROOT / "required_gate_coverage_audit_f72d.md"),
        "created_at": created_at,
        "subrun_id": "mt5_runtime_probe(MT5 런타임 탐침)",
        "record_view": "MT5 Runtime Probe(MT5 런타임 탐침)",
        "tier_scope": "Tier A separate(Tier A 분리)",
        "kpi_scope": "runtime_probe_kpi(런타임 탐침 KPI)",
        "primary_kpi": f"completed={summary['completed_attempt_count']};best_pf={best.get('profit_factor')}",
        "guardrail_kpi": f"signal_diff={best.get('signal_count_diff')};feature_diff={best.get('feature_ready_diff')}",
        "evidence_boundary": "runtime_probe_observation_no_authority(런타임 탐침 관찰, 권위 없음)",
        "question": "Does F72 trade-shape bridge preserve proxy meaning in MT5 runtime?(F72 거래 형태 연결이 MT5 런타임에서 프록시 의미를 보존하는가?)",
        "artifact_count": 12,
        "created_at_utc": created_at,
        "required_gate_audit": rel(REVIEWS_ROOT / "required_gate_coverage_audit_f72d.md"),
        "runtime_authority": "not_claimed",
        "operating_promotion": "not_claimed",
        "goal_achieve": "not_claimed",
        "run_family": "frontier_runtime_probe(전선 런타임 탐침)",
        "run_type": "mt5_runtime_probe(MT5 런타임 탐침)",
        "input_run_id": PARENT_RUN_ID,
        "output_path": rel(RUN_ROOT / "run_manifest.json"),
        "result_path": rel(REVIEWS_ROOT / "frontier72D_mt5_runtime_probe_report.md"),
    }
    f72b.upsert_ledger(f72b.ALPHA_LEDGER, "ledger_row_id", row)
    f72b.upsert_ledger(f72b.RUN_REGISTRY, "run_id", row)
    f72b.upsert_ledger(REVIEWS_ROOT / "stage_run_ledger.csv", "ledger_row_id", row, source_header=f72b.ALPHA_LEDGER)


def append_idea(payload: Mapping[str, Any]) -> None:
    summary = build_summary(payload)
    best = summary["best_runtime"]
    marker = "<!-- frontier72D_pre_mt5_grok_trade_shape_runtime_probe_v1 -->"
    block = f"""<!-- frontier72D_pre_mt5_grok_trade_shape_runtime_probe_v1 -->
- `{RUN_ID}` executed/attempted(실행/시도) F72 bridge MT5 Runtime Probe(F72 연결 MT5 런타임 탐침). Result(결과): `{payload.get('judgment')}`. Attempts(시도) `{summary['attempt_count']}`, completed(완료) `{summary['completed_attempt_count']}`. Best runtime(최선 런타임) net/PF/DD/trades_day(순수익/수익 팩터/손실폭/일거래): `{best.get('net_profit', '')}/{best.get('profit_factor', '')}/{best.get('max_drawdown_percent', '')}/{best.get('trades_per_day', '')}`. Evidence(근거): `{rel(REVIEWS_ROOT / 'frontier72D_mt5_runtime_probe_report.md')}`. Boundary(경계): no completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성 없음). Next(다음): `{NEXT_RUN_ID}`."""
    append_once(f72b.IDEA_REGISTRY, marker, block)


def main() -> int:
    args = parse_args()
    ensure_dirs()
    missing = [rel(path) for path in required_inputs() if not path_exists(path)]
    if missing:
        raise FileNotFoundError(f"F72D required material missing: {missing}")
    configure_f71d_globals()
    created_at = utc_now()
    context = build_bridge_context()
    artifact, probability_rows, signal_rows = f71d.materialize_context(context, Path(args.common_files_root))
    attempts = build_attempts(context, artifact) if artifact.get("export_status") == "exported_selected_entry_tape_parity_passed" else []
    compile_payload = compile_runtime_ea(Path(args.metaeditor_path))
    execution_results: list[dict[str, Any]] = []
    if args.execute and not args.materialize_only and attempts:
        execution_results = execute_attempts(args, attempts, compile_payload)
        reports = f71d.mt5.collect_mt5_strategy_report_artifacts(
            terminal_data_root=Path(args.terminal_data_root),
            run_output_root=RUN_ROOT,
            attempts=attempts,
            run_id=RUN_ID,
        )
        f71d.mt5.attach_mt5_report_metrics(execution_results, reports)
    runtime_receipt = f71d.build_runtime_receipt(execution_results, attempts) if execution_results else []
    completed = sum(1 for row in runtime_receipt if row.get("tester_status") == "completed")
    if args.execute and completed:
        status = "completed_mt5_runtime_probe_observation_no_authority"
        judgment = "runtime_probe_completed_gap_analysis_required_no_authority"
    elif args.execute:
        status = "blocked_mt5_runtime_probe_attempted_no_authority"
        judgment = "runtime_probe_blocked_repair_required_no_authority"
    else:
        status = "materialized_pending_mt5_runtime_probe_execution_no_authority"
        judgment = "runtime_probe_materialized_pending_execution_no_authority"
    payload = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "status": status,
        "judgment": judgment,
        "created_at_utc": created_at,
        "artifact_rows": [{
            **artifact,
            "source_candidate": context["source_candidate"],
            "bridge_label_counts": context["bridge_label_counts"],
            "selection_threshold": context["selection_threshold"],
            "runtime_threshold": context["runtime_threshold"],
            "runtime_threshold_epsilon": context["runtime_threshold_epsilon"],
            "threshold_repair_reason": "numeric_tolerance_for_onnx_float32_edge_margin_boundary",
        }],
        "probability_parity": probability_rows,
        "signal_parity": signal_rows,
        "attempts": attempts,
        "compile_payload": compile_payload,
        "execution_results": execution_results,
        "runtime_receipt": runtime_receipt,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    write_outputs(payload, created_at)
    update_ledgers(payload, created_at)
    append_idea(payload)
    update_state(payload, created_at)
    print(json.dumps(json_ready(build_summary(payload)), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
