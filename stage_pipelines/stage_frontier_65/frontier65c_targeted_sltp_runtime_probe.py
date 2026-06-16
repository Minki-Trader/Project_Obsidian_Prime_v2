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
from stage_pipelines.stage_frontier_52.run_frontier52_runtime_probe import execute_attempts, override_set_file  # noqa: E402
from stage_pipelines.stage_frontier_59 import run_frontier59_runtime_probe as f59  # noqa: E402
from stage_pipelines.stage_frontier_64 import frontier64b_loss_cluster_hazard_proxy_scout as f64b  # noqa: E402
from stage_pipelines.stage_frontier_64 import frontier64c_handoff_verification as f64c  # noqa: E402
from stage_pipelines.stage_frontier_64 import frontier64d_handoff_adapter_repair as f64d  # noqa: E402
from stage_pipelines.stage_frontier_64 import run_frontier64_runtime_probe as f64e  # noqa: E402
from stage_pipelines.stage_frontier_65 import frontier65_gap_attribution as f65b  # noqa: E402
from stage_pipelines.stage_frontier_runtime_backfill import run_frontier_runtime_probe_backfill as backfill  # noqa: E402


STAGE_NUM = 65
STAGE_ID = f65b.STAGE_ID
RUN_ID = "frontier65C_targeted_sltp_unit_runtime_probe_v1"
RUN_NUMBER = "frontier65C"
PARENT_RUN_ID = f65b.RUN_B
NEXT_RUN_ID = "frontier65D_stage_closeout_runtime_semantics_gap_attribution_v1"

STAGE_ROOT = f65b.STAGE_ROOT
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_ID
MT5_ROOT = RUN_ROOT / "mt5"
FEATURE_ROOT = RUN_ROOT / "feature_matrices"
TELEMETRY_ROOT = RUN_ROOT / "runtime_telemetry"
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
SELECTED_ROOT = STAGE_ROOT / "04_selected"

GROK_PACKET = Path("docs/agent_control/grok_reviews/2026-06-16_frontier65_pre_mt5_sltp_unit_probe/small_review")
GROK_PROMPT = GROK_PACKET / "prompt.md"
GROK_CLEAN_OUTPUT = GROK_PACKET / "clean_output.md"
GROK_METADATA = GROK_PACKET / "metadata.json"

DEFAULT_PORTABLE_ROOT = f64e.DEFAULT_PORTABLE_ROOT
DEFAULT_TERMINAL = f64e.DEFAULT_TERMINAL
DEFAULT_METAEDITOR = f64e.DEFAULT_METAEDITOR
DEFAULT_COMMON_FILES = f64e.DEFAULT_COMMON_FILES
DEFAULT_TESTER_PROFILE_ROOT = f64e.DEFAULT_TESTER_PROFILE_ROOT
DEFAULT_TERMINAL_DATA_ROOT = f64e.DEFAULT_TERMINAL_DATA_ROOT

POINT_SCALE_FROM_PRICE_UNITS = 100.0
UNIT_ADJUSTED_POLICY = {
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
    "InpAtrMinStopPoints": f59.ATR_MIN_STOP_POINTS * POINT_SCALE_FROM_PRICE_UNITS,
    "InpAtrMaxStopPoints": f59.ATR_MAX_STOP_POINTS * POINT_SCALE_FROM_PRICE_UNITS,
    "InpAtrMinTakeProfitPoints": f59.ATR_MIN_TP_POINTS * POINT_SCALE_FROM_PRICE_UNITS,
    "InpAtrMaxTakeProfitPoints": f59.ATR_MAX_TP_POINTS * POINT_SCALE_FROM_PRICE_UNITS,
    "InpRuntimeVetoTapeEnabled": True,
    "InpRuntimeVetoTapeUseCommonFiles": True,
    "InpRuntimeVetoTapeDelimiter": ",",
}


@dataclass(frozen=True)
class F65RuntimeSpec:
    stage_num: int
    stage_id: str
    parent_run_id: str
    source_run_id: str
    candidate_id: str
    model_id: str
    model_path: Path
    onnx_path: Path
    decision_mode: str
    max_hold_bars: int
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
    parser = argparse.ArgumentParser(description="Run Frontier65 targeted SLTP unit MT5 runtime probe.")
    parser.add_argument("--terminal-path", default=str(DEFAULT_TERMINAL))
    parser.add_argument("--metaeditor-path", default=str(DEFAULT_METAEDITOR))
    parser.add_argument("--common-files-root", default=str(DEFAULT_COMMON_FILES))
    parser.add_argument("--tester-profile-root", default=str(DEFAULT_TESTER_PROFILE_ROOT))
    parser.add_argument("--terminal-data-root", default=str(DEFAULT_TERMINAL_DATA_ROOT))
    parser.add_argument("--timeout-seconds", type=int, default=900)
    parser.add_argument("--wait-timeout-seconds", type=int, default=240)
    parser.add_argument("--materialize-only", action="store_true")
    parser.add_argument("--refresh-docs-only", action="store_true")
    parser.add_argument("--write-pre-mt5-prompt-only", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    mkdirs()
    if args.write_pre_mt5_prompt_only:
        f03b.write_text_sig(GROK_PROMPT, pre_mt5_prompt())
        print(json.dumps({"status": "wrote_pre_mt5_prompt", "prompt": GROK_PROMPT.as_posix()}, ensure_ascii=False, indent=2))
        return 0
    if args.refresh_docs_only:
        final = backfill.read_json(RUN_ROOT / "final_decision.json")
        final["post_run_diagnostics"] = post_run_diagnostics(final)
        final["judgment"] = stage_judgment(final.get("classification", ""), final.get("runtime_rows", []), final.get("proxy_runtime_gap_rows", []), final["post_run_diagnostics"])
        backfill.write_json(RUN_ROOT / "final_decision.json", final)
        write_reports(final, list(final["runtime_rows"]), list(final["proxy_runtime_gap_rows"]))
        update_workspace_state(final)
        update_registers(final)
        print(json.dumps({"status": "refreshed_docs", "run_id": RUN_ID}, ensure_ascii=False, indent=2))
        return 0

    created_at = utc_now()
    context = load_context()
    base = f64b.build_base()
    signals = load_repaired_signals()
    split_payload = materialize_split_payload(base, signals)
    spec = candidate_spec(context)
    attempts = materialize_attempts(
        spec,
        split_payload,
        base["feature_order"],
        base["feature_order_hash"],
        Path(args.common_files_root),
        context,
    )
    attempts = apply_runtime_policy_overrides(attempts, context)
    write_handoff_artifacts(context, split_payload, attempts)

    if args.materialize_only:
        final = build_final(created_at, context, [], [], "materialized_only_no_mt5_run")
        backfill.write_json(RUN_ROOT / "final_decision.json", final)
        print(json.dumps({"status": "materialized_only", "run_id": RUN_ID}, ensure_ascii=False, indent=2))
        return 0

    compile_payload = backfill.compile_runtime_ea(Path(args.metaeditor_path))
    terminal_probe = backfill.terminal_processes()
    execution_payload = execute_attempts(args, spec, attempts, compile_payload, terminal_probe, created_at)
    runtime_rows = backfill.build_runtime_summary_rows(spec, attempts, execution_payload, split_payload)
    runtime_rows = attach_runtime_density(runtime_rows, split_payload)
    backfill.write_csv(RUN_ROOT / "mt5_runtime_probe_summary.csv", runtime_rows)
    proxy_gap_rows = proxy_runtime_gap_rows(context, runtime_rows)
    backfill.write_csv(RUN_ROOT / "proxy_runtime_gap_after_unit_adjustment.csv", proxy_gap_rows)
    classification = classify_runtime_probe(runtime_rows)
    diagnostics = post_run_diagnostics({"runtime_rows": runtime_rows})
    final = build_final(created_at, context, runtime_rows, proxy_gap_rows, classification, diagnostics)
    backfill.write_json(RUN_ROOT / "final_decision.json", final)
    backfill.write_json(RUN_ROOT / "run_manifest.json", final)
    write_reports(final, runtime_rows, proxy_gap_rows)
    update_workspace_state(final)
    update_registers(final)
    print(
        json.dumps(
            json_ready(
                {
                    "status": final["classification"],
                    "judgment": final["judgment"],
                    "run_id": RUN_ID,
                    "runtime_rows": runtime_rows,
                    "next_run_id": NEXT_RUN_ID,
                }
            ),
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if classification != "blocked_attempt_failed" else 1


def mkdirs() -> None:
    for path in (RUN_ROOT, MT5_ROOT, FEATURE_ROOT, TELEMETRY_ROOT, REVIEWS_ROOT, SELECTED_ROOT, GROK_PACKET):
        io_path(path).mkdir(parents=True, exist_ok=True)


def load_context() -> dict[str, Any]:
    required = [f65b.RUN_B_ROOT / "gap_attribution_summary.json", f65b.F64D_FINAL, GROK_PROMPT, GROK_CLEAN_OUTPUT, GROK_METADATA]
    missing = [path.as_posix() for path in required if not path_exists(path)]
    if missing:
        raise FileNotFoundError(f"F65C context missing(F65C 문맥 누락): {missing}")
    f64d_final = backfill.read_json(f65b.F64D_FINAL)
    if not bool(f64d_final.get("repair_pass")):
        raise RuntimeError("F64D repair did not pass(F64D 수리 미통과)")
    veto_path = f65b.F64D_ROOT / "runtime_veto_tape.csv"
    if not path_exists(veto_path):
        raise FileNotFoundError(f"F64D runtime veto tape missing(런타임 차단 테이프 누락): {veto_path.as_posix()}")
    return {
        "f65b_final": backfill.read_json(f65b.RUN_B_ROOT / "gap_attribution_summary.json"),
        "f64d_final": f64d_final,
        "runtime_veto_tape": veto_path,
        "grok_clean": io_path(GROK_CLEAN_OUTPUT).read_text(encoding="utf-8-sig"),
        "grok_metadata": backfill.read_json(GROK_METADATA),
    }


def load_repaired_signals() -> dict[str, np.ndarray]:
    repaired_path = f65b.F64D_ROOT / "selected_repaired_runtime_signal.npy"
    adapter_path = f65b.F64D_ROOT / "selected_adapter_signal.npy"
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
        "decision_mode": "argmax_probe_with_runtime_veto_tape_and_unit_adjusted_sltp(최대확률 탐침, 런타임 차단 테이프, 단위 보정 손절/익절)",
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


def candidate_spec(context: Mapping[str, Any]) -> F65RuntimeSpec:
    artifacts = context["f64d_final"]["model_artifacts"]
    return F65RuntimeSpec(
        stage_num=STAGE_NUM,
        stage_id=STAGE_ID,
        parent_run_id=PARENT_RUN_ID,
        source_run_id=f64d.RUN_ID,
        candidate_id=str(context["f64d_final"]["source_best_candidate"]),
        model_id="f65c_unit_adjusted_" + str(context["f64d_final"]["selected_adapter_id"]),
        model_path=Path(str(artifacts["model_path"])),
        onnx_path=Path(str(artifacts["onnx_path"])),
        decision_mode="argmax",
        max_hold_bars=2,
        source_contract="f65_unit_adjusted_sltp_probe_reuses_f64d_direction_adapter_and_veto_tape",
        source_note="F65C changes only ATR SL/TP point scaling(ATR 손절/익절 포인트 스케일) to test F65B unit-semantics clue(단위 의미 단서).",
    )


def materialize_attempts(
    spec: F65RuntimeSpec,
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
        exploration_label="frontier65C_targeted_sltp_unit_probe(전선65C 표적 손절익절 단위 탐침)",
        common_run_root="Project_Obsidian_Prime_v2/frontier65C_targeted_sltp_unit_probe",
    )
    rule = scout.ThresholdRule(
        threshold_id=f"{RUN_ID}_argmax_probe_unit_adjusted",
        short_threshold=0.0,
        long_threshold=0.0,
        min_margin=0.0,
    )
    common_veto = scout.common_ref("veto", Path(str(context["runtime_veto_tape"])).name, context=identity)
    mt5.copy_to_common_files(common_files_root, ROOT / spec.onnx_path, scout.common_ref("models", spec.onnx_path.name, context=identity))
    mt5.copy_to_common_files(common_files_root, ROOT / str(context["runtime_veto_tape"]), common_veto)
    attempts: list[dict[str, Any]] = []
    for runtime_split, payload in split_payload.items():
        attempt_name = f"frontier65c_tier_a_{runtime_split}"
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
            record_view_prefix="mt5_frontier65c_tier_a",
            attempt_role="tier_a_unit_adjusted_runtime_probe",
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
        **UNIT_ADJUSTED_POLICY,
        "InpModelId": "f65c_unit_adjusted_" + str(context["f64d_final"]["selected_adapter_id"]),
    }


def write_handoff_artifacts(
    context: Mapping[str, Any],
    split_payload: Mapping[str, Mapping[str, Any]],
    attempts: Sequence[Mapping[str, Any]],
) -> None:
    backfill.write_json(
        RUN_ROOT / "source_truth_snapshot.json",
        {
            "parent_run_id": PARENT_RUN_ID,
            "f65b_final": context["f65b_final"],
            "f64d_final": context["f64d_final"],
            "runtime_veto_tape": str(context["runtime_veto_tape"]),
            "split_expected": {split: payload["expected"] for split, payload in split_payload.items()},
            "unit_adjusted_policy": runtime_policy(context),
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
    f64e_gap = {row["split"]: row for row in context["f65b_final"]["attribution"]["layers"]}
    rows: list[dict[str, Any]] = []
    for row in runtime_rows:
        runtime_split = str(row.get("split"))
        proxy_split = split_map.get(runtime_split, runtime_split)
        proxy = proxy_metrics.get(proxy_split, {})
        prior = f64e_gap.get(runtime_split, {})
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
                "mt5_profit_factor_unit_adjusted": pf,
                "profit_factor_gap_mt5_minus_proxy_unit_adjusted": none_gap(pf, proxy_pf),
                "f64e_mt5_profit_factor_original": prior.get("mt5_profit_factor"),
                "profit_factor_delta_unit_adjusted_minus_f64e": none_gap(pf, as_float(prior.get("mt5_profit_factor"))),
                "proxy_dd_risk": proxy_dd,
                "mt5_max_drawdown_percent_unit_adjusted": dd,
                "dd_gap_mt5_minus_proxy_unit_adjusted": none_gap(dd, proxy_dd),
                "f64e_mt5_max_drawdown_percent_original": prior.get("mt5_max_drawdown_percent"),
                "dd_delta_unit_adjusted_minus_f64e": none_gap(dd, as_float(prior.get("mt5_max_drawdown_percent"))),
                "proxy_trades_per_day": proxy_density,
                "mt5_trades_per_day_unit_adjusted": density,
                "density_gap_mt5_minus_proxy_unit_adjusted": none_gap(density, proxy_density),
                "signal_count_diff": row.get("signal_count_diff"),
                "feature_ready_diff": row.get("feature_ready_diff"),
            }
        )
    return rows


def classify_runtime_probe(runtime_rows: Sequence[Mapping[str, Any]]) -> str:
    completed = [row for row in runtime_rows if row.get("runtime_status") == "completed" and row.get("report_status") == "completed"]
    if len(completed) < 2:
        return "blocked_attempt_failed"
    return "runtime_probe_observation_unit_adjusted_sltp_no_authority(런타임 탐침 관찰, 단위 보정 손절/익절, 권위 없음)"


def build_final(
    created_at: str,
    context: Mapping[str, Any],
    runtime_rows: Sequence[Mapping[str, Any]],
    proxy_gap_rows: Sequence[Mapping[str, Any]],
    classification: str,
    diagnostics: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    diagnostics_payload = dict(diagnostics or {})
    return {
        "created_at_utc": created_at,
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "run_number": RUN_NUMBER,
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "classification": classification,
        "runtime_probe_status": classification,
        "judgment": stage_judgment(classification, runtime_rows, proxy_gap_rows, diagnostics_payload),
        "candidate_id": context["f64d_final"]["source_best_candidate"],
        "selected_adapter_id": context["f64d_final"]["selected_adapter_id"],
        "source_attribution_clue": context["f65b_final"].get("primary_attribution_clue"),
        "grok_pre_mt5_classification": classify_grok(context["grok_clean"]),
        "grok_prompt": GROK_PROMPT.as_posix(),
        "grok_output": GROK_CLEAN_OUTPUT.as_posix(),
        "grok_metadata": context["grok_metadata"],
        "runtime_policy": runtime_policy(context),
        "runtime_rows": list(runtime_rows),
        "proxy_runtime_gap_rows": list(proxy_gap_rows),
        "post_run_diagnostics": diagnostics_payload,
        "claim_boundary": backfill.claim_boundary_payload(),
        "next_run_id": NEXT_RUN_ID,
    }


def stage_judgment(
    classification: str,
    runtime_rows: Sequence[Mapping[str, Any]],
    proxy_gap_rows: Sequence[Mapping[str, Any]],
    diagnostics: Mapping[str, Any] | None = None,
) -> str:
    if classification == "blocked_attempt_failed":
        return "blocked_mt5_runtime_probe_attempt_failed_no_authority(차단, MT5 런타임 탐침 시도 실패, 권위 없음)"
    completed = [row for row in runtime_rows if row.get("runtime_status") == "completed" and row.get("report_status") == "completed"]
    if len(completed) < 2:
        return "runtime_probe_observation_incomplete_no_authority(런타임 탐침 관찰 불완전, 권위 없음)"
    original_pf_improved = any((as_float(row.get("profit_factor_delta_unit_adjusted_minus_f64e")) or 0.0) > 0.2 for row in proxy_gap_rows)
    dd_ok = all((as_float(row.get("max_drawdown_percent")) or 999.0) < 10.0 for row in completed)
    density_ok = all(5.0 <= (as_float(row.get("runtime_trades_per_day")) or -1.0) <= 10.0 for row in completed)
    exit_delta_rows = list((diagnostics or {}).get("exit_shape_delta_rows", []))
    exit_shape_supported = bool(exit_delta_rows) and all(
        (as_float(row.get("close_max_hold_rate_unit_adjusted")) or 0.0) > 0.2
        and (as_float(row.get("stop_rate_delta_unit_adjusted_minus_f64e")) or 0.0) < -0.1
        for row in exit_delta_rows
    )
    if exit_shape_supported and original_pf_improved and dd_ok and density_ok:
        return "runtime_probe_observation_sltp_unit_clue_supported_four_axis_still_no_authority(런타임 탐침 관찰, 손절/익절 단위 단서 지원, 네 축 양호, 권위 없음)"
    if exit_shape_supported and original_pf_improved:
        return "runtime_probe_observation_sltp_unit_clue_supported_economics_incomplete_no_authority(런타임 탐침 관찰, 손절/익절 단위 단서 지원, 경제성 불완전, 권위 없음)"
    return "runtime_probe_observation_sltp_unit_adjustment_inconclusive_no_authority(런타임 탐침 관찰, 손절/익절 단위 보정 불충분, 권위 없음)"


def write_reports(
    final: Mapping[str, Any],
    runtime_rows: Sequence[Mapping[str, Any]],
    proxy_gap_rows: Sequence[Mapping[str, Any]],
) -> None:
    diagnostics = final.get("post_run_diagnostics", {}) if isinstance(final.get("post_run_diagnostics"), Mapping) else {}
    if diagnostics:
        backfill.write_csv(RUN_ROOT / "unit_adjusted_trade_shape.csv", list(diagnostics.get("trade_shape_rows", [])))
        backfill.write_csv(RUN_ROOT / "unit_adjusted_telemetry_actions.csv", list(diagnostics.get("telemetry_action_rows", [])))
        backfill.write_csv(RUN_ROOT / "unit_adjusted_exit_shape_delta.csv", list(diagnostics.get("exit_shape_delta_rows", [])))
    f03b.write_text_sig(REVIEWS_ROOT / "runtime_probe_unit_adjusted_report.md", runtime_probe_report_text(final, runtime_rows))
    f03b.write_text_sig(REVIEWS_ROOT / "proxy_runtime_gap_after_unit_adjustment_report.md", proxy_gap_report_text(proxy_gap_rows))
    f03b.write_text_sig(REVIEWS_ROOT / "grok_pre_mt5_unit_probe_receipt.md", grok_receipt_text(final))
    f03b.write_text_sig(REVIEWS_ROOT / "required_gate_coverage_audit.md", gate_audit_text(final))
    f03b.write_text_sig(SELECTED_ROOT / "selection_status.md", selection_status_text(final))
    f03b.write_json(SELECTED_ROOT / "selection_status.json", selection_status_json(final))


def runtime_probe_report_text(final: Mapping[str, Any], runtime_rows: Sequence[Mapping[str, Any]]) -> str:
    diagnostics = final.get("post_run_diagnostics", {}) if isinstance(final.get("post_run_diagnostics"), Mapping) else {}
    exit_rows = list(diagnostics.get("exit_shape_delta_rows", [])) if diagnostics else []
    lines = [
        "# F65C Unit-Adjusted Runtime Probe(F65C 단위 보정 런타임 탐침)",
        "",
        f"- judgment(판정): `{final.get('judgment')}`",
        f"- run(실행): `{RUN_ID}`",
        f"- adapter(어댑터): `{final.get('selected_adapter_id')}`",
        f"- Grok pre-MT5(비싼 MT5 전 그록): `{final.get('grok_pre_mt5_classification')}`",
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
    if exit_rows:
        lines.extend(
            [
                "",
                "## Exit Shape Delta(청산 형태 변화)",
                "",
                "| split(분할) | F64E stop%(기존 손절률) | F65C stop%(보정 손절률) | F64E maxhold%(기존 최대보유률) | F65C close_max_hold%(보정 최대보유 청산률) | median hold sec(중앙 보유초) |",
                "|---|---:|---:|---:|---:|---:|",
            ]
        )
        for row in exit_rows:
            lines.append(
                f"| {row.get('split')} | {pct(row.get('f64e_mt5_stop_rate'))} | {pct(row.get('stop_rate_unit_adjusted'))} | "
                f"{pct(row.get('f64e_mt5_maxhold_rate'))} | {pct(row.get('close_max_hold_rate_unit_adjusted'))} | "
                f"{fmt(row.get('duration_seconds_median'))} |"
            )
    lines.extend(
        [
            "",
            "Action(행동): F64D direction adapter ONNX(방향 어댑터 온엑스)와 runtime veto tape(런타임 차단 테이프)는 유지하고, ATR SL/TP points(ATR 손절/익절 포인트)를 proxy price units(프록시 가격 단위)에 맞게 100배로 보정해 MT5 Strategy Tester(MT5 전략 테스터)를 실행했다.",
            "",
            "Effect(효과): F65B의 unit-semantics clue(단위 의미 단서)가 실제 runtime economics(런타임 경제성) 차이를 줄이는지 관찰한다.",
            "",
            "Boundary(경계): runtime_probe_observation(런타임 탐침 관찰) only; no authority(권위 없음).",
            "",
        ]
    )
    return "\n".join(lines)


def proxy_gap_report_text(rows: Sequence[Mapping[str, Any]]) -> str:
    lines = [
        "# F65C Proxy-Runtime Gap After Unit Adjustment(F65C 단위 보정 후 프록시-런타임 차이)",
        "",
        "| split(분할) | proxy PF(프록시 PF) | F64E MT5 PF(기존 MT5 PF) | F65C MT5 PF(보정 MT5 PF) | PF delta(보정-기존) | proxy DD(프록시 손실폭) | F65C DD(보정 손실폭) | density gap(빈도 차이) |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in rows:
        lines.append(
            f"| {row.get('split')} | {fmt(row.get('proxy_profit_factor'))} | {fmt(row.get('f64e_mt5_profit_factor_original'))} | "
            f"{fmt(row.get('mt5_profit_factor_unit_adjusted'))} | {fmt(row.get('profit_factor_delta_unit_adjusted_minus_f64e'))} | "
            f"{fmt(row.get('proxy_dd_risk'))} | {fmt(row.get('mt5_max_drawdown_percent_unit_adjusted'))} | "
            f"{fmt(row.get('density_gap_mt5_minus_proxy_unit_adjusted'))} |"
        )
    lines.append("")
    return "\n".join(lines)


def post_run_diagnostics(final: Mapping[str, Any]) -> dict[str, Any]:
    telemetry_rows = unit_adjusted_telemetry_actions()
    trade_rows = unit_adjusted_trade_shape()
    prior_rows = {
        row["split"]: row
        for row in backfill.read_json(f65b.RUN_B_ROOT / "gap_attribution_summary.json")["attribution"]["exit_rows"]
    }
    telemetry_by_split = {row["split"]: row for row in telemetry_rows}
    delta_rows: list[dict[str, Any]] = []
    for trade in trade_rows:
        split = str(trade["split"])
        prior = prior_rows.get(split, {})
        telemetry = telemetry_by_split.get(split, {})
        trades = int_value(trade.get("out_trade_count"))
        close_max_hold = int_value(telemetry.get("close_max_hold_count"))
        stop_rate = ratio(int_value(trade.get("sl_count")), trades)
        tp_rate = ratio(int_value(trade.get("tp_count")), trades)
        close_max_hold_rate = ratio(close_max_hold, trades)
        delta_rows.append(
            {
                "split": split,
                "f64e_mt5_stop_rate": as_float(prior.get("mt5_stop_rate")) or 0.0,
                "stop_rate_unit_adjusted": stop_rate,
                "stop_rate_delta_unit_adjusted_minus_f64e": stop_rate - (as_float(prior.get("mt5_stop_rate")) or 0.0),
                "f64e_mt5_take_rate": as_float(prior.get("mt5_take_rate")) or 0.0,
                "take_rate_unit_adjusted": tp_rate,
                "f64e_mt5_maxhold_rate": as_float(prior.get("mt5_maxhold_rate")) or 0.0,
                "close_max_hold_rate_unit_adjusted": close_max_hold_rate,
                "close_max_hold_count_unit_adjusted": close_max_hold,
                "duration_seconds_median": trade.get("duration_seconds_median"),
                "duration_seconds_mean": trade.get("duration_seconds_mean"),
                "exit_shape_verdict": "unit_shape_supported(단위 형태 지원)"
                if close_max_hold_rate > 0.2 and stop_rate < (as_float(prior.get("mt5_stop_rate")) or 0.0)
                else "unit_shape_inconclusive(단위 형태 불충분)",
            }
        )
    return {
        "telemetry_action_rows": telemetry_rows,
        "trade_shape_rows": trade_rows,
        "exit_shape_delta_rows": delta_rows,
    }


def unit_adjusted_telemetry_actions() -> list[dict[str, Any]]:
    root = RUN_ROOT / "runtime_telemetry"
    rows: list[dict[str, Any]] = []
    for split, stem in (("validation_is", "frontier65c_tier_a_validation_is"), ("oos", "frontier65c_tier_a_oos")):
        df = read_csv_frame(root / f"{stem}_telemetry.csv")
        cycles = df[df["record_type"].astype(str) == "cycle"].copy()
        action = cycles["exec_action"].fillna("").astype(str)
        position_before = cycles["position_before"].fillna("").astype(str)
        rows.append(
            {
                "split": split,
                "cycle_rows": int(len(cycles)),
                "open_long_count": int(action.eq("open_long").sum()),
                "open_short_count": int(action.eq("open_short").sum()),
                "close_max_hold_count": int(action.eq("close_max_hold").sum()),
                "hold_same_direction_count": int(action.eq("hold_same_direction").sum()),
                "hold_existing_count": int(action.eq("hold_existing").sum()),
                "flat_no_position_count": int(action.eq("flat_no_position").sum()),
                "position_before_with_position_count": int((position_before != "none").sum()),
            }
        )
    return rows


def unit_adjusted_trade_shape() -> list[dict[str, Any]]:
    report_root = io_path(RUN_ROOT / "mt5" / "reports")
    rows: list[dict[str, Any]] = []
    for path in report_root.iterdir():
        if path.suffix.lower() != ".htm":
            continue
        split = "validation_is" if "validation" in path.name else "oos"
        deals = f65b.parse_mt5_deals(path)
        out_deals = deals[deals["direction"].astype(str) == "out"].copy()
        out_deals["profit_num"] = pd.to_numeric(out_deals["profit"], errors="coerce")
        out_deals["reason"] = (
            out_deals["comment"].fillna("").astype(str).str.extract(r"^(sl|tp|close|max)", expand=False).fillna("other")
        )
        duration_series = paired_durations_seconds(deals)
        gross_profit = float(out_deals.loc[out_deals["profit_num"] > 0.0, "profit_num"].sum())
        gross_loss = float(-out_deals.loc[out_deals["profit_num"] < 0.0, "profit_num"].sum())
        rows.append(
            {
                "split": split,
                "out_trade_count": int(len(out_deals)),
                "sl_count": int(out_deals["reason"].eq("sl").sum()),
                "tp_count": int(out_deals["reason"].eq("tp").sum()),
                "non_sltp_out_count": int((~out_deals["reason"].isin(["sl", "tp"])).sum()),
                "gross_profit": gross_profit,
                "gross_loss": gross_loss,
                "net_profit": float(out_deals["profit_num"].sum()),
                "profit_factor": gross_profit / gross_loss if gross_loss > 0.0 else None,
                "duration_seconds_mean": safe_series_mean(duration_series),
                "duration_seconds_median": safe_series_median(duration_series),
                "duration_seconds_q25": safe_series_quantile(duration_series, 0.25),
                "duration_seconds_q75": safe_series_quantile(duration_series, 0.75),
                "duration_seconds_max": safe_series_max(duration_series),
                "duration_le_1s_count": int((duration_series <= 1.0).sum()),
                "duration_le_300s_count": int((duration_series <= 300.0).sum()),
                "duration_gt_300s_count": int((duration_series > 300.0).sum()),
                "report_path": path.as_posix().replace("\\\\?\\", ""),
            }
        )
    return rows


def paired_durations_seconds(deals: pd.DataFrame) -> pd.Series:
    rows = deals[deals["direction"].astype(str).isin(["in", "out"])].copy().reset_index(drop=True)
    durations: list[float] = []
    for idx in range(0, len(rows) - 1, 2):
        if rows.loc[idx, "direction"] == "in" and rows.loc[idx + 1, "direction"] == "out":
            start = pd.to_datetime(rows.loc[idx, "time"], errors="coerce")
            end = pd.to_datetime(rows.loc[idx + 1, "time"], errors="coerce")
            if pd.notna(start) and pd.notna(end):
                durations.append(float((end - start).total_seconds()))
    return pd.Series(durations, dtype="float64")


def grok_receipt_text(final: Mapping[str, Any]) -> str:
    metadata = final["grok_metadata"]
    return f"""# F65 Grok Pre-MT5 Receipt(F65 비싼 MT5 전 그록 영수증)

- trigger_reason(트리거 이유): expensive MT5 runtime probe(비싼 MT5 런타임 탐침) before RUN_C.
- review_size(검토 크기): `small review(소규모 검토)`.
- prompt(프롬프트): `{GROK_PROMPT.as_posix()}`
- prompt_sha256(프롬프트 해시): `{metadata.get('prompt_hash')}`
- clean_output(정리 출력): `{GROK_CLEAN_OUTPUT.as_posix()}`
- clean_output_sha256(정리 출력 해시): `{sha256_file(GROK_CLEAN_OUTPUT)}`
- classification(분류): `{final['grok_pre_mt5_classification']}`
- local_verification(로컬 검증): runtime policy(런타임 정책), F64D artifacts(F64D 산출물), F65B clue(F65B 단서)를 로컬에서 읽고 RUN_C를 실행했다.
- final_codex_direction(최종 코덱스 방향): unit-adjusted runtime probe(단위 보정 런타임 탐침), no authority(권위 없음).
"""


def gate_audit_text(final: Mapping[str, Any]) -> str:
    return f"""# F65 Required Gate Coverage Audit(F65 필수 게이트 커버리지 감사)

- stage_open_grok_review(단계 개방 그록 검토): `accepted(수용)`
- proxy_runtime_gap_attribution(프록시-런타임 차이 귀속): `{PARENT_RUN_ID}`
- pre_mt5_grok_review(비싼 MT5 전 그록 검토): `{final['grok_pre_mt5_classification']}`
- targeted_mt5_runtime_probe(표적 MT5 런타임 탐침): `{RUN_ID}` / `{final['runtime_probe_status']}`
- proxy_runtime_gap_after_unit_adjustment(단위 보정 후 프록시-런타임 차이): `recorded(기록됨)`
- stage_closeout(단계 마감): `pending(대기)` / next `{NEXT_RUN_ID}`
- final_claim_guard(최종 주장 보호): forbidden claims(금지 주장) 모두 not_claimed(주장 없음).
"""


def selection_status_text(final: Mapping[str, Any]) -> str:
    return f"""# F65 Selection Status(F65 선택 상태)

- stage(단계): `{STAGE_ID}`
- current_run(현재 실행): `{RUN_ID}`
- status(상태): `{final.get('classification')}`
- judgment(판정): `{final.get('judgment')}`
- selected_proxy_candidate(선택 프록시 후보): `{final.get('candidate_id')}`
- selected_direction_adapter(선택 방향 어댑터): `{final.get('selected_adapter_id')}`
- runtime_probe_report(런타임 탐침 보고서): `{(REVIEWS_ROOT / 'runtime_probe_unit_adjusted_report.md').as_posix()}`
- proxy_runtime_gap_report(프록시-런타임 차이 보고서): `{(REVIEWS_ROOT / 'proxy_runtime_gap_after_unit_adjustment_report.md').as_posix()}`
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
        "runtime_probe_report": (REVIEWS_ROOT / "runtime_probe_unit_adjusted_report.md").as_posix(),
        "proxy_runtime_gap_report": (REVIEWS_ROOT / "proxy_runtime_gap_after_unit_adjustment_report.md").as_posix(),
        "next_run_id": NEXT_RUN_ID,
        "claim_boundary": final.get("claim_boundary"),
    }


def update_workspace_state(final: Mapping[str, Any]) -> None:
    rows = {str(row.get("split")): row for row in final.get("runtime_rows", [])}
    val = rows.get("validation_is", {})
    oos = rows.get("oos", {})
    text = f"""current_stage_id: {STAGE_ID}
active_stage: {STAGE_ID}
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
  - "F65C unit-adjusted MT5 runtime probe(단위 보정 MT5 런타임 탐침): validation_is PF={val.get('profit_factor')} DD={val.get('max_drawdown_percent')} trades={val.get('trade_count')} density/day={val.get('runtime_trades_per_day')}; OOS PF={oos.get('profit_factor')} DD={oos.get('max_drawdown_percent')} trades={oos.get('trade_count')} density/day={oos.get('runtime_trades_per_day')}."
  - "RUN_C validates(검증) F65B unit-semantics clue(단위 의미 단서) only as runtime probe observation(런타임 탐침 관찰), not authority(권위 아님)."
  - "No completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성) claimed(주장 없음)."
"""
    f03b.write_text_sig(f03b.WORKSPACE_STATE, text)
    f03b.write_text_sig(f03b.CURRENT_WORKING_STATE, current_working_state_text(final))


def current_working_state_text(final: Mapping[str, Any]) -> str:
    return f"""# Current Working State(현재 작업 상태)

Frontier65(F65, 전선 65단계)는 F65C targeted MT5 runtime probe(표적 MT5 런타임 탐침)를 기록했다.

- stage(단계): `{STAGE_ID}`
- current_run(현재 실행): `{RUN_ID}`
- judgment(판정): `{final.get('judgment')}`
- selected_proxy_candidate(선택 프록시 후보): `{final.get('candidate_id')}`
- selected_direction_adapter(선택 방향 어댑터): `{final.get('selected_adapter_id')}`
- next_run(다음 실행): `{NEXT_RUN_ID}`

Action(행동): F64D ONNX(온엑스)와 veto tape(차단 테이프)는 유지하고 SL/TP points(손절/익절 포인트)를 proxy price unit(프록시 가격 단위)에 맞춰 100배로 보정한 MT5 Strategy Tester(MT5 전략 테스터)를 실행했다.

Effect(효과): F65B unit-semantics clue(단위 의미 단서)가 runtime economics(런타임 경제성) 차이를 줄이는지 관찰했다.

Claim boundary(주장 경계): runtime_probe_observation(런타임 탐침 관찰)까지만 말한다. completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 주장하지 않는다.
"""


def update_registers(final: Mapping[str, Any]) -> None:
    f64c.upsert_csv(f03b.RUN_REGISTRY, "run_id", run_registry_row(final))
    f64c.upsert_csv(f03b.ALPHA_LEDGER, "ledger_row_id", ledger_row(final))
    f64c.upsert_csv(STAGE_ROOT / "03_reviews" / "stage_run_ledger.csv", "ledger_row_id", ledger_row(final))
    f64c.append_once(f03b.CHANGELOG, RUN_ID, changelog_entry(final))
    f64c.append_once(f03b.IDEA_REGISTRY, RUN_ID, idea_entry(final))


def run_registry_row(final: Mapping[str, Any]) -> dict[str, Any]:
    oos = row_by_split(final.get("runtime_rows", []), "oos")
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "lane": "targeted_mt5_runtime_probe_unit_adjusted_sltp(표적 MT5 런타임 탐침, 단위 보정 손절/익절)",
        "status": final["classification"],
        "judgment": final["judgment"],
        "path": (REVIEWS_ROOT / "runtime_probe_unit_adjusted_report.md").as_posix(),
        "notes": f"oos_pf={oos.get('profit_factor')};oos_dd={oos.get('max_drawdown_percent')};next={NEXT_RUN_ID}",
        "family": "runtime_parity(런타임 동등성)",
        "primary_report": (REVIEWS_ROOT / "runtime_probe_unit_adjusted_report.md").as_posix(),
        "run_number": RUN_NUMBER,
        "date": final["created_at_utc"][:10],
        "decision": final["judgment"],
        "parent_run_id": PARENT_RUN_ID,
        "next_run_id": NEXT_RUN_ID,
        "claim_boundary": "runtime_probe_observation_only_no_authority(런타임 탐침 관찰 전용, 권위 없음)",
        "report_path": (REVIEWS_ROOT / "runtime_probe_unit_adjusted_report.md").as_posix(),
        "profit_factor": oos.get("profit_factor", ""),
        "drawdown": oos.get("max_drawdown_percent", ""),
        "trade_count": oos.get("trade_count", ""),
        "view": "mt5_runtime_probe(엠티5 런타임 탐침)",
        "tier": "Tier A(티어 A)",
        "metric_scope": "mt5_runtime_probe_unit_adjusted_sltp(단위 보정 손절/익절 MT5 런타임 탐침)",
        "external_verification_status": "completed(완료)",
        "result_judgment": final["judgment"],
        "created_at": final["created_at_utc"],
        "created_at_utc": final["created_at_utc"],
        "required_gate_audit": (REVIEWS_ROOT / "required_gate_coverage_audit.md").as_posix(),
        "runtime_authority": "not_claimed(주장 없음)",
        "operating_promotion": "not_claimed(주장 없음)",
        "run_family": "frontier_mt5_runtime_probe(전선 MT5 런타임 탐침)",
        "run_type": "mt5_runtime_probe(엠티5 런타임 탐침)",
        "input_run_id": PARENT_RUN_ID,
        "output_path": (RUN_ROOT / "final_decision.json").as_posix(),
        "result_path": (RUN_ROOT / "final_decision.json").as_posix(),
        "selected_profit_factor": oos.get("profit_factor", ""),
        "selected_trade_density": oos.get("runtime_trades_per_day", ""),
        "goal_achieve": "not_claimed(주장 없음)",
        "source_authority": "reference_not_inheritance(참조이지 상속 아님)",
        "trade_density": oos.get("runtime_trades_per_day", ""),
        "max_drawdown_percent": oos.get("max_drawdown_percent", ""),
    }


def ledger_row(final: Mapping[str, Any]) -> dict[str, Any]:
    oos = row_by_split(final.get("runtime_rows", []), "oos")
    row = run_registry_row(final)
    row.update(
        {
            "ledger_row_id": f"{RUN_ID}__tier_a_runtime_probe",
            "subrun_id": f"{RUN_ID}__tier_a_runtime_probe",
            "record_view": "Tier A separate(티어 A 분리)",
            "tier_scope": "Tier A separate(티어 A 분리)",
            "kpi_scope": "unit_adjusted_sltp_runtime_probe(단위 보정 손절/익절 런타임 탐침)",
            "scoreboard_lane": "runtime_probe(런타임 탐침)",
            "primary_kpi": f"oos_pf={oos.get('profit_factor')};oos_density={oos.get('runtime_trades_per_day')};oos_dd={oos.get('max_drawdown_percent')}",
            "guardrail_kpi": "no_completion_no_authority_stage_closeout_pending(완성/권위 없음, 단계 마감 대기)",
        }
    )
    return row


def changelog_entry(final: Mapping[str, Any]) -> str:
    return f"\n## {final['created_at_utc'][:10]} Frontier65C Targeted MT5 Probe(F65C 표적 MT5 탐침)\n\n- action(행동): `{RUN_ID}`로 SL/TP point unit(손절/익절 포인트 단위)을 proxy price unit(프록시 가격 단위)에 맞춘 MT5 runtime probe(런타임 탐침)를 실행했다.\n- effect(효과): F65B unit-semantics clue(단위 의미 단서)를 실제 Strategy Tester(전략 테스터)에서 관찰하고 `{NEXT_RUN_ID}` 마감 검토로 넘겼다.\n- boundary(경계): runtime probe observation(런타임 탐침 관찰)이며 completion/baseline/promotion/runtime authority/live readiness/Goal Achieve(완성/기준선/승격/런타임 권위/실거래 준비/목표 달성)는 주장하지 않는다.\n"


def idea_entry(final: Mapping[str, Any]) -> str:
    return f"\n## {RUN_ID}\n\n- Stage(단계): `{STAGE_ID}`\n- Idea(아이디어): SL/TP point unit adjustment(손절/익절 포인트 단위 보정)이 F64 proxy-runtime gap(프록시-런타임 차이)을 줄이는지 확인한다.\n- Result(결과): `{final.get('judgment')}`\n- Evidence(근거): `{(REVIEWS_ROOT / 'runtime_probe_unit_adjusted_report.md').as_posix()}` and `{(REVIEWS_ROOT / 'proxy_runtime_gap_after_unit_adjustment_report.md').as_posix()}`.\n- Next(다음): `{NEXT_RUN_ID}`\n- Boundary(경계): runtime_probe_observation only(런타임 탐침 관찰 전용), no authority(권위 없음).\n"


def pre_mt5_prompt() -> str:
    return """Frontier65 pre-MT5 review(전선65 비싼 MT5 전 검토)입니다.

Please answer only from this bounded snapshot(제한 스냅샷). Do not inspect files(파일 확인 금지), run tools(도구 실행 금지), browse(브라우징 금지), or perform local verification(로컬 검증 금지). If evidence is insufficient, say `needs_local_verification(로컬 검증 필요)`.

## Current Local Finding(현재 로컬 발견)

- F65B attribution scout(귀속 탐색)는 F64E proxy-runtime gap(프록시-런타임 차이)을 층별로 분해했다.
- feature_ready_diff(피처 준비 차이)는 validation/OOS `0/0`.
- raw adapter signal(원 어댑터 신호), runtime veto tape(런타임 차단 테이프), entry transition gate(진입 전환 게이트)는 telemetry(런타임 기록)와 수량상 맞았다.
- signal count gap(신호 수 차이): validation/OOS expected after veto(차단 후 예상) `4073 / 3325`, entry transition block(진입 전환 차단) `2973 / 2483`, actual non-flat(실제 비관망) `1100 / 842`.
- PF/DD economics gap(수익 팩터/손실폭 경제성 차이): validation/OOS proxy PF `1.0727 / 1.1081`, MT5 PF `0.35 / 0.70`, proxy DD `4.319 / 3.154`, MT5 DD `28.23 / 7.92`.
- Exit shape(청산 형태): proxy maxhold(프록시 최대보유) `58.9% / 56.7%`, MT5 maxhold(실제 최대보유) `0% / 0%`; MT5 stop rate(손절률) `79.5% / 67.5%`.
- ATR unit clue(ATR 단위 단서): proxy ATR price median(프록시 ATR 가격 중앙값) `31.09 / 36.67`, MT5 ATR points median(MT5 ATR 포인트 중앙값) `3506.64 / 4025.96`, inferred point(추정 포인트) about `0.009`.

## Proposed RUN_C(제안 RUN_C)

Run(실행): `frontier65C_targeted_sltp_unit_runtime_probe_v1`.

Action(행동): reuse F64D direction adapter ONNX(방향 어댑터 온엑스), feature matrix(피처 행렬), and runtime veto tape(런타임 차단 테이프), but change only ATR SL/TP point inputs(ATR 손절/익절 포인트 입력) by multiplying point thresholds by `100`: stop min/max `40/180` becomes `4000/18000`, take min/max `60/280` becomes `6000/28000`.

Effect(효과): if the unit-semantics clue(단위 의미 단서) is real, MT5 exit shape(청산 형태) should move away from immediate SL/TP(즉시 손절/익절) and closer to proxy maxhold behavior(프록시 최대보유 동작). This is still runtime_probe_observation(런타임 탐침 관찰), not authority(권위).

## Review Request(검토 요청)

1. Classification(분류): `accepted(수용)`, `rejected(거절)`, or `needs_local_verification(로컬 검증 필요)`.
2. Is RUN_C a narrow sufficient MT5 check(좁은 충분 MT5 확인) for the F65B clue?
3. What must be recorded to avoid overclaiming(과장 주장 방지)?
4. Forbidden claims check(금지 주장 확인): completion/baseline/promotion/runtime authority/live readiness/Goal Achieve.
"""


def classify_grok(clean: str) -> str:
    lower = clean.lower()
    if "rejected" in lower:
        return "rejected(거절)"
    if "accepted" in lower and "needs_local_verification" in lower:
        return "accepted_with_local_verification(수용, 로컬 검증 포함)"
    if "accepted" in lower:
        return "accepted(수용)"
    return "needs_local_verification(로컬 검증 필요)"


def row_by_split(rows: Sequence[Mapping[str, Any]], split: str) -> dict[str, Any]:
    for row in rows:
        if str(row.get("split")) == split:
            return dict(row)
    return {}


def read_csv_frame(path: Path) -> pd.DataFrame:
    return f65b.read_csv_frame(path)


def int_value(value: Any) -> int:
    return f65b.int_value(value)


def ratio(part: int, whole: int) -> float:
    return f65b.ratio(part, whole)


def safe_series_mean(series: pd.Series) -> float:
    return f65b.safe_series_mean(series)


def safe_series_median(series: pd.Series) -> float:
    return f65b.safe_series_median(series)


def safe_series_max(series: pd.Series) -> float:
    return f65b.safe_series_max(series)


def safe_series_quantile(series: pd.Series, q: float) -> float:
    return f65b.safe_series_quantile(series, q)


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


def pct(value: Any) -> str:
    number = safe_float(value)
    return f"{number * 100.0:.2f}%" if math.isfinite(number) else "n/a"


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


if __name__ == "__main__":
    raise SystemExit(main())
