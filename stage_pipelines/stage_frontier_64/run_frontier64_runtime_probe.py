from __future__ import annotations

import argparse
import json
import math
import sys
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from foundation.alpha import scout_runner as scout  # noqa: E402
from foundation.control_plane.ledger import io_path, json_ready, path_exists  # noqa: E402
from foundation.models.onnx_bridge import sha256_file  # noqa: E402
from foundation.mt5 import runtime_support as mt5  # noqa: E402
from stage_pipelines.stage_frontier_03 import frontier03b_regime_asymmetric_label_proxy_scout as f03b  # noqa: E402
from stage_pipelines.stage_frontier_23 import frontier23b_payoff_asymmetry_pf_source_proxy_scout as f23b  # noqa: E402
from stage_pipelines.stage_frontier_52.run_frontier52_runtime_probe import execute_attempts, override_set_file  # noqa: E402
from stage_pipelines.stage_frontier_59 import run_frontier59_runtime_probe as f59  # noqa: E402
from stage_pipelines.stage_frontier_64 import frontier64b_loss_cluster_hazard_proxy_scout as f64b  # noqa: E402
from stage_pipelines.stage_frontier_64 import frontier64d_handoff_adapter_repair as f64d  # noqa: E402
from stage_pipelines.stage_frontier_runtime_backfill import run_frontier_runtime_probe_backfill as backfill  # noqa: E402


STAGE_NUM = 64
STAGE_ID = f64b.STAGE_ID
RUN_ID = "frontier64E_mt5_runtime_probe_loss_cluster_hazard_v1"
RUN_NUMBER = "frontier64E"
PARENT_RUN_ID = f64d.RUN_ID
NEXT_RUN_ID = "frontier64F_stage_closeout_loss_cluster_hazard_v1"

STAGE_ROOT = f64b.STAGE_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
MT5_ROOT = RUN_ROOT / "mt5"
FEATURE_ROOT = RUN_ROOT / "feature_matrices"
TELEMETRY_ROOT = RUN_ROOT / "runtime_telemetry"
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
SELECTED_ROOT = STAGE_ROOT / "04_selected"
REPORT_PATH = REVIEWS_ROOT / "runtime_probe_report.md"
GAP_REPORT_PATH = REVIEWS_ROOT / "proxy_runtime_gap_report.md"
F64D_FINAL = STAGE_ROOT / "02_runs" / f64d.RUN_ID / "handoff_adapter_repair.json"

DEFAULT_PORTABLE_ROOT = Path("C:/Users/awdse/AppData/Local/ObsidianPrime/mt5_portable_run329E")
DEFAULT_TERMINAL = DEFAULT_PORTABLE_ROOT / "terminal64.exe"
DEFAULT_METAEDITOR = DEFAULT_PORTABLE_ROOT / "MetaEditor64.exe"
DEFAULT_COMMON_FILES = DEFAULT_PORTABLE_ROOT / "Common" / "Files"
DEFAULT_TESTER_PROFILE_ROOT = DEFAULT_PORTABLE_ROOT / "MQL5" / "Profiles" / "Tester"
DEFAULT_TERMINAL_DATA_ROOT = DEFAULT_PORTABLE_ROOT

RUNTIME_POLICY = {
    "InpDecisionMode": "argmax_probe",
    "InpShortThreshold": 0.0,
    "InpLongThreshold": 0.0,
    "InpMinMargin": 0.0,
    "InpInvertSignal": False,
    "InpFallbackInvertSignal": False,
    "InpCloseOnFlatSignal": False,
    "InpReverseOnOppositeSignal": False,
    "InpCloseOnlyOnOppositeSignal": False,
    "InpEntryTransitionOnly": True,
    "InpEntryTransitionRearmMinConfidenceDelta": 0.0,
    "InpMaxHoldBars": 2,
    "InpReentryCooldownBars": 0,
    "InpSameDirectionReentryCooldownBars": 0,
    "InpAtrSltpEnabled": True,
    "InpAtrPeriod": f59.ATR_PERIOD,
    "InpAtrStopMultiplier": f59.ATR_STOP_MULT,
    "InpAtrTakeProfitMultiplier": f59.ATR_TP_MULT,
    "InpAtrMinStopPoints": f59.ATR_MIN_STOP_POINTS,
    "InpAtrMaxStopPoints": f59.ATR_MAX_STOP_POINTS,
    "InpAtrMinTakeProfitPoints": f59.ATR_MIN_TP_POINTS,
    "InpAtrMaxTakeProfitPoints": f59.ATR_MAX_TP_POINTS,
    "InpRuntimeVetoTapeEnabled": True,
    "InpRuntimeVetoTapeUseCommonFiles": True,
    "InpRuntimeVetoTapeDelimiter": ",",
}


@dataclass(frozen=True)
class F64RuntimeSpec:
    stage_num: int
    stage_id: str
    parent_run_id: str
    source_run_id: str
    candidate_id: str
    model_id: str
    model_path: Path
    onnx_path: Path
    decision_mode: str
    short_threshold: float
    long_threshold: float
    min_margin: float
    max_hold_bars: int
    cooldown_bars: int
    source_contract: str
    source_note: str

    @property
    def run_number(self) -> str:
        return RUN_NUMBER

    @property
    def run_id(self) -> str:
        return RUN_ID

    @property
    def run_root(self) -> Path:
        return RUN_ROOT

    @property
    def mt5_root(self) -> Path:
        return MT5_ROOT

    @property
    def feature_root(self) -> Path:
        return FEATURE_ROOT

    @property
    def telemetry_copy_root(self) -> Path:
        return TELEMETRY_ROOT


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Frontier64 MT5 runtime probe for repaired loss-cluster hazard handoff.")
    parser.add_argument("--terminal-path", default=str(DEFAULT_TERMINAL))
    parser.add_argument("--metaeditor-path", default=str(DEFAULT_METAEDITOR))
    parser.add_argument("--common-files-root", default=str(DEFAULT_COMMON_FILES))
    parser.add_argument("--tester-profile-root", default=str(DEFAULT_TESTER_PROFILE_ROOT))
    parser.add_argument("--terminal-data-root", default=str(DEFAULT_TERMINAL_DATA_ROOT))
    parser.add_argument("--timeout-seconds", type=int, default=900)
    parser.add_argument("--wait-timeout-seconds", type=int, default=240)
    parser.add_argument("--materialize-only", action="store_true")
    parser.add_argument("--refresh-docs-only", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    created_at = utc_now()
    mkdirs()
    if args.refresh_docs_only:
        refresh_docs()
        print(json.dumps({"status": "refreshed_docs", "run_id": RUN_ID}, ensure_ascii=False, indent=2))
        return 0

    context = load_context()
    base = f64b.build_base()
    signals = load_repaired_signals()
    split_payload = materialize_split_payload(base, signals)
    spec = candidate_spec(context)
    attempts = materialize_attempts(spec, split_payload, base["feature_order"], base["feature_order_hash"], Path(args.common_files_root), context)
    attempts = apply_runtime_policy_overrides(attempts, context)
    write_handoff_artifacts(context, split_payload, attempts)

    compile_payload = backfill.compile_runtime_ea(Path(args.metaeditor_path))
    terminal_probe = backfill.terminal_processes()
    execution_payload = execute_attempts(args, spec, attempts, compile_payload, terminal_probe, created_at)
    runtime_rows = backfill.build_runtime_summary_rows(spec, attempts, execution_payload, split_payload)
    runtime_rows = attach_runtime_density(runtime_rows, split_payload)
    backfill.write_csv(RUN_ROOT / "mt5_runtime_probe_summary.csv", runtime_rows)
    classification = "runtime_probe_observation_no_authority"
    if not any(row.get("runtime_status") == "completed" and row.get("report_status") == "completed" for row in runtime_rows):
        classification = "blocked_attempt_failed"
    proxy_gap_rows = proxy_runtime_gap_rows(context, runtime_rows)
    backfill.write_csv(RUN_ROOT / "proxy_runtime_gap.csv", proxy_gap_rows)
    final = {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "candidate_id": context["f64d_final"]["source_best_candidate"],
        "selected_adapter_id": context["f64d_final"]["selected_adapter_id"],
        "classification": classification,
        "runtime_probe_status": classification,
        "judgment": stage_judgment(classification, runtime_rows),
        "model_artifacts": context["f64d_final"]["model_artifacts"],
        "runtime_policy": runtime_policy(context),
        "runtime_rows": runtime_rows,
        "proxy_runtime_gap_rows": proxy_gap_rows,
        "claim_boundary": backfill.claim_boundary_payload(),
        "created_at_utc": created_at,
        "next_run_id": NEXT_RUN_ID,
    }
    backfill.write_json(RUN_ROOT / "final_decision.json", final)
    backfill.write_json(RUN_ROOT / "run_manifest.json", final)
    write_reports(final, runtime_rows, proxy_gap_rows, attempts, execution_payload)
    backfill.upsert_backfill_status_ledger(
        STAGE_NUM,
        STAGE_ID,
        created_at,
        classification,
        {
            "status": classification,
            "reason": "frontier64_mandatory_mt5_runtime_probe_recorded",
            "checks": {
                "candidate_id": final["candidate_id"],
                "selected_adapter_id": final["selected_adapter_id"],
                "onnx_path": context["f64d_final"]["model_artifacts"]["onnx_path"],
                "runtime_policy": runtime_policy(context),
            },
        },
        spec,  # type: ignore[arg-type]
        runtime_rows,
    )
    update_workspace_state(final)
    update_registers(final)
    print(json.dumps(json_ready({"status": classification, "run_id": RUN_ID, "judgment": final["judgment"], "runtime_rows": runtime_rows}), ensure_ascii=False, indent=2))
    return 0 if classification != "blocked_attempt_failed" else 1


def mkdirs() -> None:
    for path in (RUN_ROOT, MT5_ROOT, FEATURE_ROOT, TELEMETRY_ROOT, REVIEWS_ROOT, SELECTED_ROOT):
        io_path(path).mkdir(parents=True, exist_ok=True)


def load_context() -> dict[str, Any]:
    if not path_exists(F64D_FINAL):
        raise FileNotFoundError(f"F64D final decision missing(최종 판단 누락): {F64D_FINAL.as_posix()}")
    f64d_final = backfill.read_json(F64D_FINAL)
    if not bool(f64d_final.get("repair_pass")):
        raise RuntimeError("F64D repair did not pass(F64D 수리 미통과)")
    veto_path = STAGE_ROOT / "02_runs" / f64d.RUN_ID / "runtime_veto_tape.csv"
    if not path_exists(veto_path):
        raise FileNotFoundError(f"F64D runtime veto tape missing(런타임 차단 테이프 누락): {veto_path.as_posix()}")
    return {"f64d_final": f64d_final, "runtime_veto_tape": veto_path}


def load_repaired_signals() -> dict[str, np.ndarray]:
    run_root = STAGE_ROOT / "02_runs" / f64d.RUN_ID
    repaired_path = run_root / "selected_repaired_runtime_signal.npy"
    adapter_path = run_root / "selected_adapter_signal.npy"
    if not path_exists(repaired_path) or not path_exists(adapter_path):
        raise FileNotFoundError("F64D repaired signal artifacts missing(F64D 수리 신호 산출물 누락)")
    return {
        "repaired_signal": np.load(io_path(repaired_path)),
        "adapter_signal": np.load(io_path(adapter_path)),
    }


def materialize_split_payload(base: Mapping[str, Any], signals: Mapping[str, np.ndarray]) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    rows_for_expected: list[dict[str, Any]] = []
    frame = base["frame"].copy()
    feature_order = list(base["feature_order"])
    x_raw = np.asarray(base["x_raw"], dtype="float64")
    finite = np.asarray(base["finite"], dtype=bool)
    repaired_signal = np.asarray(signals["repaired_signal"], dtype="int8")
    adapter_signal = np.asarray(signals["adapter_signal"], dtype="int8")
    runtime_frame = pd.concat(
        [
            frame[["timestamp", "symbol", "split"]].reset_index(drop=True),
            pd.DataFrame(x_raw, columns=feature_order),
        ],
        axis=1,
    )
    for runtime_split, source_split in (("validation_is", "validation"), ("oos", "oos")):
        split_all = runtime_frame["split"].astype(str).eq(source_split).to_numpy()
        export_mask = split_all & finite
        export_frame = runtime_frame.loc[export_mask].copy()
        feature_path = FEATURE_ROOT / f"{RUN_ID}_{runtime_split}_features.csv"
        feature_export = mt5.export_mt5_feature_matrix_csv(export_frame, feature_order, feature_path)
        expected_signal = repaired_signal[export_mask]
        raw_adapter_signal = adapter_signal[export_mask]
        expected = expected_signal_summary(export_frame, expected_signal, raw_adapter_signal, runtime_split)
        rows_for_expected.append(expected)
        out[runtime_split] = {
            "source_split": source_split,
            "frame": export_frame,
            "signal": expected_signal,
            "raw_adapter_signal": raw_adapter_signal,
            "feature_export": feature_export,
            "expected": expected,
            "from_date": backfill.split_date_range(export_frame)[0],
            "to_date": backfill.split_date_range(export_frame)[1],
        }
    backfill.write_csv(RUN_ROOT / "expected_signal_summary.csv", rows_for_expected)
    return out


def expected_signal_summary(frame: pd.DataFrame, signal: np.ndarray, adapter_signal: np.ndarray, runtime_split: str) -> dict[str, Any]:
    timestamps = pd.to_datetime(frame["timestamp"], utc=True).reset_index(drop=True)
    days = backfill.count_scope_days(timestamps) if len(timestamps) else 0
    signal_count = int((signal != 0).sum())
    adapter_count = int((adapter_signal != 0).sum())
    return {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "split": runtime_split,
        "rows": int(len(frame)),
        "days_in_scope": int(days),
        "decision_mode": "argmax_probe_with_runtime_veto_tape(최대확률 탐침과 런타임 차단 테이프)",
        "signal_count": signal_count,
        "long_count": int((signal == 1).sum()),
        "short_count": int((signal == -1).sum()),
        "flat_count": int((signal == 0).sum()),
        "adapter_raw_signal_count": adapter_count,
        "adapter_raw_long_count": int((adapter_signal == 1).sum()),
        "adapter_raw_short_count": int((adapter_signal == -1).sum()),
        "adapter_raw_flat_count": int((adapter_signal == 0).sum()),
        "expected_density_per_day": float(signal_count / days) if days else 0.0,
        "expected_raw_signal_density_per_day": float(adapter_count / days) if days else 0.0,
    }


def candidate_spec(context: Mapping[str, Any]) -> F64RuntimeSpec:
    artifacts = context["f64d_final"]["model_artifacts"]
    return F64RuntimeSpec(
        stage_num=STAGE_NUM,
        stage_id=STAGE_ID,
        parent_run_id=PARENT_RUN_ID,
        source_run_id=f64d.RUN_ID,
        candidate_id=str(context["f64d_final"]["source_best_candidate"]),
        model_id=str(context["f64d_final"]["selected_adapter_id"]),
        model_path=Path(str(artifacts["model_path"])),
        onnx_path=Path(str(artifacts["onnx_path"])),
        decision_mode="argmax",
        short_threshold=0.0,
        long_threshold=0.0,
        min_margin=0.0,
        max_hold_bars=2,
        cooldown_bars=0,
        source_contract="f64_direction_adapter_3class_argmax_plus_runtime_veto_tape",
        source_note="F64D repaired handoff separates simple direction adapter ONNX(방향 어댑터 온엑스) and loss-cluster hazard runtime veto tape(손실 군집 위험 런타임 차단 테이프).",
    )


def materialize_attempts(
    spec: F64RuntimeSpec,
    split_payload: Mapping[str, Mapping[str, Any]],
    feature_order: Sequence[str],
    feature_hash: str,
    common_files_root: Path,
    context: Mapping[str, Any],
) -> list[dict[str, Any]]:
    identity = scout.RunIdentity(
        stage_id=spec.stage_id,
        stage_number=spec.stage_num,
        run_number=RUN_NUMBER,
        run_id=RUN_ID,
        exploration_label="frontier64E_mt5_runtime_probe(전선64E MT5 런타임 탐침)",
        common_run_root="Project_Obsidian_Prime_v2/frontier64E_mt5_runtime_probe",
    )
    rule = scout.ThresholdRule(
        threshold_id=f"{RUN_ID}_argmax_probe",
        short_threshold=0.0,
        long_threshold=0.0,
        min_margin=0.0,
    )
    common_veto = scout.common_ref("veto", Path(str(context["runtime_veto_tape"])).name, context=identity)
    mt5.copy_to_common_files(common_files_root, ROOT / spec.onnx_path, scout.common_ref("models", spec.onnx_path.name, context=identity))
    mt5.copy_to_common_files(common_files_root, ROOT / str(context["runtime_veto_tape"]), common_veto)
    attempts: list[dict[str, Any]] = []
    for runtime_split, payload in split_payload.items():
        attempt_name = f"frontier64e_tier_a_{runtime_split}"
        mt5.copy_to_common_files(
            common_files_root,
            ROOT / str(payload["feature_export"]["path"]),
            scout.common_ref("features", Path(str(payload["feature_export"]["path"])).name, context=identity),
        )
        attempt = scout.materialize_mt5_attempt_files(
            run_output_root=spec.run_root,
            tier_name=scout.TIER_A,
            split_name=runtime_split,
            local_onnx_path=ROOT / spec.onnx_path,
            local_feature_matrix_path=ROOT / str(payload["feature_export"]["path"]),
            rule=rule,
            feature_count=len(feature_order),
            feature_order_hash=feature_hash,
            from_date=str(payload["from_date"]),
            to_date=str(payload["to_date"]),
            stem_prefix=attempt_name,
            record_view_prefix="mt5_frontier64e_tier_a",
            attempt_role="tier_a_runtime_probe",
            decision_mode="argmax_probe",
            max_hold_bars=spec.max_hold_bars,
            reentry_cooldown_bars=0,
            same_direction_reentry_cooldown_bars=0,
            entry_transition_only=True,
            entry_transition_rearm_min_confidence_delta=0.0,
            context=identity,
        )
        attempt.update(
            {
                "attempt_name": attempt_name,
                "candidate_id": spec.candidate_id,
                "model_id": spec.model_id,
                "source_run_id": spec.source_run_id,
                "decision_mode": spec.decision_mode,
                "ini_name": scout.mt5_short_profile_ini_name(scout.TIER_A, runtime_split, context=identity),
                "common_runtime_veto_tape_path": common_veto,
            }
        )
        attempts.append(attempt)
    return attempts


def apply_runtime_policy_overrides(attempts: Sequence[Mapping[str, Any]], context: Mapping[str, Any]) -> list[dict[str, Any]]:
    patched: list[dict[str, Any]] = []
    policy = runtime_policy(context)
    for attempt in attempts:
        row = dict(attempt)
        policy_with_tape = {**policy, "InpRuntimeVetoTapePath": str(row["common_runtime_veto_tape_path"])}
        set_payload = dict(row["set"])
        set_path = Path(str(set_payload["path"]))
        override_set_file(set_path, policy_with_tape)
        set_payload["sha256"] = sha256_file(set_path)
        set_payload["runtime_policy_override"] = json_ready(policy_with_tape)
        row["set"] = set_payload
        row["runtime_policy"] = json_ready(policy_with_tape)
        patched.append(row)
    backfill.write_json(MT5_ROOT / "runtime_policy_override_manifest.json", {"policy": policy, "attempts": patched})
    return patched


def runtime_policy(context: Mapping[str, Any]) -> dict[str, Any]:
    return {
        **RUNTIME_POLICY,
        "InpModelId": str(context["f64d_final"]["selected_adapter_id"]),
    }


def write_handoff_artifacts(context: Mapping[str, Any], split_payload: Mapping[str, Mapping[str, Any]], attempts: Sequence[Mapping[str, Any]]) -> None:
    backfill.write_json(
        RUN_ROOT / "source_truth_snapshot.json",
        {
            "parent_run_id": PARENT_RUN_ID,
            "f64d_final": context["f64d_final"],
            "runtime_veto_tape": str(context["runtime_veto_tape"]),
            "split_expected": {split: payload["expected"] for split, payload in split_payload.items()},
        },
    )
    backfill.write_json(MT5_ROOT / "handoff_manifest.json", {"attempts": attempts, "runtime_policy": runtime_policy(context)})


def attach_runtime_density(runtime_rows: Sequence[Mapping[str, Any]], split_payload: Mapping[str, Mapping[str, Any]]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for row in runtime_rows:
        item = dict(row)
        expected = split_payload[str(item.get("split"))]["expected"]
        days = float(expected.get("days_in_scope", 0) or 0)
        trades = safe_float(item.get("trade_count"))
        order_attempts = safe_float(item.get("mt5_order_attempt_count"))
        item["days_in_scope"] = int(days)
        item["runtime_trades_per_day"] = float(trades / days) if days and math.isfinite(trades) else 0.0
        item["runtime_order_attempts_per_day"] = float(order_attempts / days) if days and math.isfinite(order_attempts) else 0.0
        item["expected_signal_density_per_day"] = expected.get("expected_density_per_day")
        item["expected_raw_signal_density_per_day"] = expected.get("expected_raw_signal_density_per_day")
        out.append(item)
    return out


def proxy_runtime_gap_rows(context: Mapping[str, Any], runtime_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    proxy_metrics = {row["split"]: row for row in context["f64d_final"]["selected_metric_rows"]}
    split_map = {"validation_is": "validation", "oos": "oos"}
    rows: list[dict[str, Any]] = []
    for row in runtime_rows:
        runtime_split = str(row.get("split"))
        proxy_split = split_map.get(runtime_split, runtime_split)
        proxy = proxy_metrics.get(proxy_split, {})
        pf = as_float(row.get("profit_factor"))
        dd = as_float(row.get("max_drawdown_percent"))
        density = as_float(row.get("runtime_trades_per_day"))
        proxy_pf = as_float(proxy.get("profit_factor"))
        proxy_dd = as_float(proxy.get("dd_risk"))
        proxy_density = as_float(proxy.get("trades_per_day"))
        rows.append(
            {
                "split": runtime_split,
                "proxy_split": proxy_split,
                "proxy_profit_factor": proxy_pf,
                "mt5_profit_factor": pf,
                "profit_factor_gap_mt5_minus_proxy": none_gap(pf, proxy_pf),
                "proxy_dd_risk": proxy_dd,
                "mt5_max_drawdown_percent": dd,
                "dd_gap_mt5_minus_proxy": none_gap(dd, proxy_dd),
                "proxy_trades_per_day": proxy_density,
                "mt5_trades_per_day": density,
                "density_gap_mt5_minus_proxy": none_gap(density, proxy_density),
                "signal_count_diff": row.get("signal_count_diff"),
                "feature_ready_diff": row.get("feature_ready_diff"),
            }
        )
    return rows


def stage_judgment(classification: str, runtime_rows: Sequence[Mapping[str, Any]]) -> str:
    if classification == "blocked_attempt_failed":
        return "blocked_mt5_runtime_probe_attempt_failed_no_authority(차단, MT5 런타임 탐침 시도 실패, 권위 없음)"
    completed = [row for row in runtime_rows if row.get("runtime_status") == "completed" and row.get("report_status") == "completed"]
    if len(completed) < 2:
        return "runtime_probe_observation_incomplete_no_authority(런타임 탐침 관찰 불완전, 권위 없음)"
    both_positive = all((as_float(row.get("profit_factor")) or 0.0) > 1.0 for row in completed)
    dd_ok = all((as_float(row.get("max_drawdown_percent")) or 999.0) < 10.0 for row in completed)
    density_ok = all(5.0 <= (as_float(row.get("runtime_trades_per_day")) or -1.0) <= 10.0 for row in completed)
    if both_positive and dd_ok and density_ok:
        return "runtime_probe_observation_preserved_clue_no_authority(런타임 탐침 관찰 보존 단서, 권위 없음)"
    return "negative_memory_runtime_probe_quality_gap_no_authority(부정 기억, 런타임 탐침 품질 차이, 권위 없음)"


def write_reports(
    final: Mapping[str, Any],
    runtime_rows: Sequence[Mapping[str, Any]],
    proxy_gap_rows: Sequence[Mapping[str, Any]],
    attempts: Sequence[Mapping[str, Any]],
    execution_payload: Mapping[str, Any],
) -> None:
    del attempts, execution_payload
    f03b.write_text_sig(REPORT_PATH, runtime_probe_report_text(final, runtime_rows))
    f03b.write_text_sig(GAP_REPORT_PATH, proxy_runtime_gap_report_text(proxy_gap_rows))
    f03b.write_text_sig(REVIEWS_ROOT / "required_gate_coverage_audit.md", gate_audit_text(final))
    f03b.write_text_sig(SELECTED_ROOT / "selection_status.md", selection_status_text(final))
    f03b.write_json(SELECTED_ROOT / "selection_status.json", selection_status_json(final))


def runtime_probe_report_text(final: Mapping[str, Any], runtime_rows: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        "# F64E Runtime Probe Report(F64E 런타임 탐침 보고)",
        "",
        f"- judgment(판정): `{final.get('judgment')}`",
        f"- run(실행): `{RUN_ID}`",
        f"- adapter(어댑터): `{final.get('selected_adapter_id')}`",
        "",
        "| split(분할) | runtime(런타임) | report(보고서) | PF(수익 팩터) | DD%(손실폭) | trades/day(일 거래) | signal diff(신호 차이) | feature diff(피처 차이) |",
        "|---|---|---|---:|---:|---:|---:|---:|",
    ]
    for row in runtime_rows:
        lines.append(
            f"| {row.get('split')} | {row.get('runtime_status')} | {row.get('report_status')} | "
            f"{row.get('profit_factor')} | {row.get('max_drawdown_percent')} | {row.get('runtime_trades_per_day')} | "
            f"{row.get('signal_count_diff')} | {row.get('feature_ready_diff')} |"
        )
    lines.extend(
        [
            "",
            "Action(행동): F64D direction adapter ONNX(방향 어댑터 온엑스)와 runtime veto tape(런타임 차단 테이프)를 MT5 Strategy Tester(MT5 전략 테스터)에 전달했다.",
            "",
            "Effect(효과): proxy(프록시)에서 줄인 handoff gap(인계 차이)이 실제 EA(전문가 자문)와 tester economics(테스터 경제성)에서도 유지되는지 관찰했다.",
            "",
            "Boundary(경계): runtime_probe_observation(런타임 탐침 관찰) only; no authority(권위 없음).",
            "",
        ]
    )
    return "\n".join(lines)


def proxy_runtime_gap_report_text(rows: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        "# F64 Proxy-Runtime Gap Report(F64 프록시-런타임 차이 보고)",
        "",
        "| split(분할) | proxy PF(프록시 PF) | MT5 PF(MT5 PF) | PF gap(PF 차이) | proxy DD(프록시 손실폭) | MT5 DD(MT5 손실폭) | density gap(빈도 차이) | signal diff(신호 차이) |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in rows:
        lines.append(
            f"| {row.get('split')} | {fmt(row.get('proxy_profit_factor'))} | {fmt(row.get('mt5_profit_factor'))} | "
            f"{fmt(row.get('profit_factor_gap_mt5_minus_proxy'))} | {fmt(row.get('proxy_dd_risk'))} | "
            f"{fmt(row.get('mt5_max_drawdown_percent'))} | {fmt(row.get('density_gap_mt5_minus_proxy'))} | {row.get('signal_count_diff')} |"
        )
    lines.append("")
    return "\n".join(lines)


def gate_audit_text(final: Mapping[str, Any]) -> str:
    return f"""# F64 Required Gate Coverage Audit(F64 필수 게이트 커버리지 감사)

- stage_open_grok_review(단계 개방 그록 검토): `accepted(수용)`
- proxy_completed(프록시 완료): `{f64b.RUN_ID}`
- pre_mt5_grok_review(비싼 MT5 전 그록 검토): `needs_local_verification(로컬 검증 필요)`
- local_handoff_verification(로컬 인계 검증): `blocked_handoff_adapter_mismatch(차단, 인계 어댑터 불일치)`
- capped_handoff_adapter_repair(상한 있는 인계 어댑터 수리): `{f64d.RUN_ID}`
- mt5_runtime_probe(MT5 런타임 탐침): `{final.get('runtime_probe_status')}`
- proxy_runtime_gap(프록시-런타임 차이): `recorded(기록됨)`
- final_claim_guard(최종 주장 보호): forbidden claims(금지 주장) 모두 not_claimed(주장 없음).
"""


def selection_status_text(final: Mapping[str, Any]) -> str:
    return f"""# F64 Selection Status(F64 선택 상태)

- stage(단계): `{STAGE_ID}`
- current_run(현재 실행): `{RUN_ID}`
- status(상태): `{final.get('classification')}`
- judgment(판정): `{final.get('judgment')}`
- selected_proxy_candidate(선택 프록시 후보): `{final.get('candidate_id')}`
- selected_direction_adapter(선택 방향 어댑터): `{final.get('selected_adapter_id')}`
- runtime_probe_report(런타임 탐침 보고서): `{REPORT_PATH.as_posix()}`
- proxy_runtime_gap_report(프록시-런타임 차이 보고서): `{GAP_REPORT_PATH.as_posix()}`
- next_run(다음 실행): `{NEXT_RUN_ID}`
- boundary(경계): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 not_claimed(주장 없음).
"""


def selection_status_json(final: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "stage_id": STAGE_ID,
        "current_run_id": RUN_ID,
        "status": final.get("classification"),
        "judgment": final.get("judgment"),
        "selected_proxy_candidate": final.get("candidate_id"),
        "selected_direction_adapter": final.get("selected_adapter_id"),
        "runtime_probe_report": REPORT_PATH.as_posix(),
        "proxy_runtime_gap_report": GAP_REPORT_PATH.as_posix(),
        "next_run_id": NEXT_RUN_ID,
        "claim_boundary": final.get("claim_boundary"),
    }


def update_workspace_state(final: Mapping[str, Any]) -> None:
    rows = {str(row.get("split")): row for row in final.get("runtime_rows", [])}
    val = rows.get("validation_is", {})
    oos = rows.get("oos", {})
    text = f"""current_stage_id: {STAGE_ID}
current_run_id: {RUN_ID}
latest_completed_run_id: {RUN_ID}
current_status: {final.get('classification')}
current_judgment: {final.get('judgment')}
next_stage_id: null
next_run_id: {NEXT_RUN_ID}
runtime_probe_status: runtime_probe_observation_no_authority
runtime_authority: not_claimed
operating_promotion: not_claimed
live_readiness: not_claimed
goal_achieve: not_claimed
updated_at_utc: '{utc_now()}'
notes:
  - "F64E MT5 runtime probe: validation_is PF={val.get('profit_factor')} DD={val.get('max_drawdown_percent')} trades={val.get('trade_count')} density/day={val.get('runtime_trades_per_day')} signal_diff={val.get('signal_count_diff')} feature_ready_diff={val.get('feature_ready_diff')}; OOS PF={oos.get('profit_factor')} DD={oos.get('max_drawdown_percent')} trades={oos.get('trade_count')} density/day={oos.get('runtime_trades_per_day')} signal_diff={oos.get('signal_count_diff')} feature_ready_diff={oos.get('feature_ready_diff')}."
  - "F64E uses direction adapter ONNX(방향 어댑터 온엑스)+runtime veto tape(런타임 차단 테이프), not runtime authority(런타임 권위)."
  - "No completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성) claimed(주장 없음)."
"""
    f03b.write_text_sig(f03b.WORKSPACE_STATE, text)
    f03b.write_text_sig(f03b.CURRENT_WORKING_STATE, current_working_state_text(final))


def current_working_state_text(final: Mapping[str, Any]) -> str:
    return f"""# Current Working State(현재 작업 상태)

Frontier64(F64, 전선 64단계)는 F64E MT5 runtime probe(MT5 런타임 탐침)를 기록했다.

- stage(단계): `{STAGE_ID}`
- current_run(현재 실행): `{RUN_ID}`
- judgment(판정): `{final.get('judgment')}`
- selected_proxy_candidate(선택 프록시 후보): `{final.get('candidate_id')}`
- selected_direction_adapter(선택 방향 어댑터): `{final.get('selected_adapter_id')}`
- next_run(다음 실행): `{NEXT_RUN_ID}`

Action(행동): F64D repaired handoff(수리된 인계)를 MT5 Strategy Tester(MT5 전략 테스터)에 실행했다.

Effect(효과): proxy-runtime gap(프록시-런타임 차이)을 실제 tester KPI(테스터 성과 지표), signal_diff(신호 차이), feature_ready_diff(피처 준비 차이)로 기록했다.

Claim boundary(주장 경계): runtime_probe_observation(런타임 탐침 관찰)까지만 말한다. completion(완성), baseline(기준선), promotion(승격), runtime authority(런타임 권위), live readiness(실거래 준비), Goal Achieve(목표 달성)는 주장하지 않는다.
"""


def update_registers(final: Mapping[str, Any]) -> None:
    f64d.f64c.append_once(f03b.IDEA_REGISTRY, RUN_ID, idea_entry(final))
    if str(final.get("judgment", "")).startswith("negative_memory"):
        f64d.f64c.append_once(f03b.NEGATIVE_RESULT_REGISTER, RUN_ID, negative_entry(final))


def idea_entry(final: Mapping[str, Any]) -> str:
    return f"\n## {RUN_ID}\n\n- Stage(단계): `{STAGE_ID}`\n- Idea(아이디어): F64 loss-cluster hazard gate(손실 군집 위험 게이트)를 repaired MT5 handoff(수리된 MT5 인계)로 runtime probe(런타임 탐침)했다.\n- Result(결과): `{final.get('judgment')}`\n- Evidence(근거): `{REPORT_PATH.as_posix()}`\n- Boundary(경계): runtime_probe_observation only(런타임 탐침 관찰 전용), no authority(권위 없음).\n"


def negative_entry(final: Mapping[str, Any]) -> str:
    return f"\n## {RUN_ID}\n\n- Stage(단계): `{STAGE_ID}`\n- Negative memory(부정 기억): `{final.get('judgment')}`\n- Evidence(근거): `{REPORT_PATH.as_posix()}` and `{GAP_REPORT_PATH.as_posix()}`.\n- Boundary(경계): no authority(권위 없음), no completion(완성 없음).\n"


def refresh_docs() -> None:
    final = backfill.read_json(RUN_ROOT / "final_decision.json")
    runtime_rows = list(final["runtime_rows"])
    proxy_gap_rows = list(final["proxy_runtime_gap_rows"])
    execution_payload = backfill.read_json(RUN_ROOT / "mt5_execution_result.json") if path_exists(RUN_ROOT / "mt5_execution_result.json") else {}
    handoff = backfill.read_json(MT5_ROOT / "handoff_manifest.json") if path_exists(MT5_ROOT / "handoff_manifest.json") else {"attempts": []}
    write_reports(final, runtime_rows, proxy_gap_rows, handoff.get("attempts", []), execution_payload)
    update_workspace_state(final)
    update_registers(final)


def safe_float(value: Any) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return math.nan
    return number if math.isfinite(number) else math.nan


def as_float(value: Any) -> float | None:
    number = safe_float(value)
    return number if math.isfinite(number) else None


def none_gap(left: float | None, right: float | None) -> float | None:
    if left is None or right is None:
        return None
    return float(left - right)


def fmt(value: Any) -> str:
    number = safe_float(value)
    return f"{number:.6g}" if math.isfinite(number) else "n/a"


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


if __name__ == "__main__":
    raise SystemExit(main())
