from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


STAGE_ID = "330_onnx_rebuild__forward_safe_non_identity_surface_robustness"
SOURCE_STAGE_ID = "329_onnx_rebuild__live_feature_control"
RUN_NUMBER = "run330A"
RUN_ID = "run330A_design_forward_safe_non_identity_surface_robustness_packet_v1"
PARENT_RUN_ID = "run329H_cp322A_exact_handoff_repair_feasibility_or_research_artifact_closeout_v1"
NEXT_RUN_ID = "run330B_materialize_forward_safe_non_identity_control_surfaces_v1"
STATUS = "completed_forward_safe_non_identity_design_no_selection"
JUDGMENT = "exploratory_design_completed_no_forward_decision"
DECISION = "stage330A_design_packet_completed_materialization_next_no_candidate_selection"
TODAY = "2026-05-26"
CLAIM_BOUNDARY = (
    "research_development_only_forward_safe_non_identity_onnx_rebuild_no_cp322a_exact_repair_"
    "no_forward_threshold_tuning_no_live_readiness_no_deployment_no_operating_promotion_"
    "no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
SPEC_DIR = STAGE_DIR / "00_spec"
INPUTS_DIR = STAGE_DIR / "01_inputs"
REVIEWS_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"

SOURCE_RUN_DIR = ROOT / "stages" / SOURCE_STAGE_ID / "02_runs"
SOURCE_REVIEW_DIR = ROOT / "stages" / SOURCE_STAGE_ID / "03_reviews"
SOURCE_GAP = SOURCE_RUN_DIR / "run329G" / "raw_forward_session_gap_report.csv"
SOURCE_PRESSURE = SOURCE_RUN_DIR / "run329G" / "overfit_pressure_report.csv"
SOURCE_MT5 = SOURCE_RUN_DIR / "run329F" / "forward_mt5_kpi_report.csv"
SOURCE_COST = SOURCE_RUN_DIR / "run329F" / "cost_stress_report.csv"
SOURCE_CURVE = SOURCE_RUN_DIR / "run329F" / "curve_pocket_report.csv"
SOURCE_CLOSEOUT = SOURCE_RUN_DIR / "run329H" / "stage329_closeout_decision.json"
SOURCE_HANDOFF_QUEUE = SOURCE_RUN_DIR / "run329H" / "next_stage_research_handoff_queue.csv"

RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
STAGE_LEDGER = REVIEWS_DIR / "stage_run_ledger.csv"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-26_stage330A_forward_safe_non_identity_surface_design.md"


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def io_path(path: Path) -> Path:
    resolved = path.resolve()
    if sys.platform == "win32":
        text = str(resolved)
        if not text.startswith("\\\\?\\"):
            return Path("\\\\?\\" + text)
    return resolved


def rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def path_exists(path: Path) -> bool:
    return io_path(path).exists()


def path_is_file(path: Path) -> bool:
    return path_exists(path) and io_path(path).is_file()


def sha256_file(path: Path) -> str:
    if not path_is_file(path):
        return "missing"
    digest = hashlib.sha256()
    with io_path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def json_ready(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): json_ready(item) for key, item in value.items()}
    if isinstance(value, list):
        return [json_ready(item) for item in value]
    if isinstance(value, tuple):
        return [json_ready(item) for item in value]
    if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
        return None
    return value


def csv_value(value: Any) -> Any:
    if value is None:
        return ""
    if isinstance(value, float):
        if math.isnan(value) or math.isinf(value):
            return ""
        return round(value, 10)
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(json_ready(value), ensure_ascii=False, sort_keys=True)
    return value


def read_text_lossless(path: Path) -> tuple[str, bool]:
    raw = io_path(path).read_bytes()
    return raw.decode("utf-8-sig"), raw.startswith(b"\xef\xbb\xbf")


def write_text_lossless(path: Path, text: str, had_bom: bool) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text, encoding="utf-8-sig" if had_bom else "utf-8", newline="\n")
    return path


def read_json(path: Path) -> dict[str, Any]:
    with io_path(path).open("r", encoding="utf-8-sig") as handle:
        return json.load(handle)


def write_json(path: Path, payload: Any) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(json_ready(payload), handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")
    return path


def write_md(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="\n") as handle:
        handle.write(text.strip() + "\n")
    return path


def read_csv(path: Path) -> list[dict[str, str]]:
    with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: csv_value(row.get(column)) for column in columns})
    return path


def upsert_csv(path: Path, key_columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    existing: list[dict[str, Any]] = []
    fieldnames: list[str] = []
    if path_exists(path):
        with io_path(path).open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = list(reader.fieldnames or [])
            existing = [dict(row) for row in reader]
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    by_key = {tuple(str(row.get(column, "")) for column in key_columns): index for index, row in enumerate(existing)}
    for row in rows:
        key = tuple(str(row.get(column, "")) for column in key_columns)
        payload = {column: csv_value(row.get(column, "")) for column in fieldnames}
        if key in by_key:
            existing[by_key[key]] = payload
        else:
            existing.append(payload)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(existing)
    return path


def append_if_missing(path: Path, marker: str, block: str) -> Path:
    text, had_bom = read_text_lossless(path)
    if marker not in text:
        text = text.rstrip() + "\n\n" + block.strip() + "\n"
        write_text_lossless(path, text, had_bom)
    return path


def replace_prefix_line(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            return "\n".join(lines) + ("\n" if text.endswith("\n") else "")
    return text.rstrip() + "\n" + replacement + "\n"


def fnum(value: Any, default: float = 0.0) -> float:
    try:
        if value is None or str(value).strip() == "":
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def index_by(rows: Sequence[Mapping[str, str]], key: str) -> dict[str, Mapping[str, str]]:
    return {str(row.get(key, "")): row for row in rows}


def cost_at(cost_rows: Sequence[Mapping[str, str]], slug: str, extra_cost: float) -> Mapping[str, str]:
    for row in cost_rows:
        if row.get("artifact_slug") == slug and abs(fnum(row.get("extra_cost_per_round_trip_account_ccy")) - extra_cost) < 1e-9:
            return row
    return {}


def worst_curve(curve_rows: Sequence[Mapping[str, str]], slug: str, chunk_type: str) -> Mapping[str, str]:
    candidates = [row for row in curve_rows if row.get("artifact_slug") == slug and row.get("chunk_type") == chunk_type]
    if not candidates:
        return {}
    return min(candidates, key=lambda row: fnum(row.get("net_profit"), default=999999.0))


def stage330_role(slug: str, pressure_level: str) -> tuple[str, str]:
    if slug == "c56_plain":
        return (
            "low_pressure_control_seed_not_selection",
            "best current clue, but still has train/validation sign flip and negative curve pocket",
        )
    if slug == "c56_bal":
        return (
            "medium_pressure_cost_failure_control",
            "nearby core56 control that fails +1 cost stress and keeps curve pocket risk visible",
        )
    if pressure_level == "high":
        return (
            "high_pressure_negative_control",
            "raw/session signal density explosion must be rejected before any ONNX rebuild claim",
        )
    return ("support_control", "keeps comparison coverage without selection")


def source_evidence_rows() -> list[dict[str, Any]]:
    pressure_rows = read_csv(SOURCE_PRESSURE)
    gap_by_slug = index_by(read_csv(SOURCE_GAP), "artifact_slug")
    mt5_by_slug = index_by(read_csv(SOURCE_MT5), "artifact_slug")
    cost_rows = read_csv(SOURCE_COST)
    curve_rows = read_csv(SOURCE_CURVE)
    output: list[dict[str, Any]] = []
    for row in pressure_rows:
        slug = row["artifact_slug"]
        gap = gap_by_slug.get(slug, {})
        mt5 = mt5_by_slug.get(slug, {})
        cost1 = cost_at(cost_rows, slug, 1.0)
        cost2 = cost_at(cost_rows, slug, 2.0)
        rolling = worst_curve(curve_rows, slug, "rolling_worst_net")
        third = worst_curve(curve_rows, slug, "thirds")
        role, note = stage330_role(slug, row.get("pressure_level", ""))
        output.append(
            {
                "artifact_slug": slug,
                "candidate_id": row.get("candidate_id"),
                "feature_set_id": gap.get("feature_set_id"),
                "model_id": gap.get("model_id"),
                "stage330_role": role,
                "pressure_level": row.get("pressure_level"),
                "pressure_score": row.get("pressure_score"),
                "pressure_flags": row.get("pressure_flags"),
                "session_mt5_net": mt5.get("net_profit"),
                "session_mt5_pf": mt5.get("profit_factor"),
                "trade_count": mt5.get("trade_count"),
                "trades_per_day": mt5.get("trades_per_day"),
                "equity_dd_percent": mt5.get("equity_dd_percent"),
                "cost_1_pf": cost1.get("profit_factor_after_cost"),
                "cost_1_net": cost1.get("net_profit_after_cost"),
                "cost_2_pf": cost2.get("profit_factor_after_cost"),
                "raw_session_signal_per_day_ratio": gap.get("raw_session_signal_per_day_ratio"),
                "exclusive_raw_signal_rate": gap.get("exclusive_raw_signal_rate"),
                "raw_row_supply_ratio": gap.get("raw_session_row_ratio"),
                "long_share_shift": gap.get("long_share_shift"),
                "wfo_min_balanced_accuracy": gap.get("wfo_min_balanced_accuracy"),
                "train_oos_balanced_accuracy_gap": gap.get("train_oos_balanced_accuracy_gap"),
                "worst_rolling_net": rolling.get("net_profit"),
                "worst_third_net": third.get("net_profit"),
                "stage330_use_note": note,
                "selection_status": "not_selected",
            }
        )
    return output


def design_guardrails() -> list[dict[str, Any]]:
    return [
        {
            "guardrail_id": "G01_cp322a_exact_boundary",
            "protected_failure_mode": "confusing cp322A exact replay with a new non-identity ONNX",
            "required_evidence": "Stage329H closeout decision and Stage330 claim boundary",
            "pass_condition": "cp322A remains research artifact; Stage330 models use separate identity",
            "fail_condition": "any report says cp322A exact repair, Forward Passed, or operating readiness",
            "effect": "keeps the old frozen artifact from becoming hidden authority",
        },
        {
            "guardrail_id": "G02_no_forward_threshold_tuning",
            "protected_failure_mode": "turning latest forward into threshold search data",
            "required_evidence": "threshold source receipt and fixed-score replay manifest",
            "pass_condition": "thresholds come from training/WFO design only",
            "fail_condition": "threshold chosen by 2026-04-14+ profit, PF, DD, or signal density",
            "effect": "prevents robustness testing from becoming another overfit loop",
        },
        {
            "guardrail_id": "G03_raw_session_gap_guard",
            "protected_failure_mode": "session-parity MT5 success hiding raw-forward signal explosion",
            "required_evidence": "raw rows, session rows, signal/day ratio, exclusive raw signal rate",
            "pass_condition": "raw/session ratio is inside the predeclared review band or rejected as high pressure",
            "fail_condition": "high density explosion is promoted or tuned away after seeing forward",
            "effect": "forces broker data supply behavior to remain visible",
        },
        {
            "guardrail_id": "G04_curve_pocket_guard",
            "protected_failure_mode": "one strong middle pocket hiding late or rolling loss pockets",
            "required_evidence": "thirds, rolling worst net, underwater stretch, recovery record",
            "pass_condition": "negative pocket is explainable and not dominant under fixed rules",
            "fail_condition": "positive net/PF is accepted while worst pocket remains structurally large",
            "effect": "makes curve quality a first-class robustness check",
        },
        {
            "guardrail_id": "G05_cost_stress_guard",
            "protected_failure_mode": "edge vanishing under spread/slippage stress",
            "required_evidence": "0, 0.25, 0.5, 1, 2, 3, 5 cost stress table",
            "pass_condition": "fixed surface survives predeclared cost levels without retuning",
            "fail_condition": "candidate only survives after lot, threshold, or decision rule adjustment",
            "effect": "separates real tolerance from cost-sensitive curve fitting",
        },
        {
            "guardrail_id": "G06_wfo_and_old_oos_guard",
            "protected_failure_mode": "latest forward result overriding unstable old splits",
            "required_evidence": "train, validation, WFO, old OOS, latest forward split receipt",
            "pass_condition": "old split instability is named before latest forward is interpreted",
            "fail_condition": "latest forward is used to excuse train/validation sign flip",
            "effect": "keeps older evidence from being erased by the newest sample",
        },
        {
            "guardrail_id": "G07_regime_slice_guard",
            "protected_failure_mode": "US100-specific macro/rate/volatility regimes hidden in aggregate",
            "required_evidence": "session, hour, month, volatility, ADX, VIX, USD, rate slices",
            "pass_condition": "slice losses and concentrations are reported before final judgment",
            "fail_condition": "aggregate net is used without regime attribution",
            "effect": "makes economic context visible to the forward read",
        },
        {
            "guardrail_id": "G08_runtime_parity_guard",
            "protected_failure_mode": "Python score and MT5 handoff carrying different meaning",
            "required_evidence": "feature order hash, ONNX parity, row-level signal parity, tester output",
            "pass_condition": "research, ONNX, handoff, and MT5 rows agree within stated tolerance",
            "fail_condition": "MetaEditor compile or Python replay is treated as tester proof",
            "effect": "keeps runtime claims below authority until external evidence exists",
        },
        {
            "guardrail_id": "G09_lot_normalization_guard",
            "protected_failure_mode": "risk sizing hiding whether the signal surface itself survives",
            "required_evidence": "lot-normalized net, expectancy, DD, and recovery report",
            "pass_condition": "fixed lots and normalized lots are both recorded",
            "fail_condition": "lot optimization repairs weak signal behavior",
            "effect": "keeps sizing from acting as silent model tuning",
        },
        {
            "guardrail_id": "G10_result_claim_guard",
            "protected_failure_mode": "design completion being mistaken for forward pass",
            "required_evidence": "result judgment and missing evidence list",
            "pass_condition": "run330A closes as design only; no selection, no Goal Achieve",
            "fail_condition": "design packet claims candidate selection or live readiness",
            "effect": "keeps the current run useful without overstating it",
        },
    ]


def robustness_queue() -> list[dict[str, Any]]:
    return [
        {
            "test_id": "T01_forward_data_availability_audit",
            "target_run": NEXT_RUN_ID,
            "subject": "US100 M5 broker data after 2026-04-14",
            "sample_scope": "latest available raw and session-filtered forward bars",
            "required_inputs": "run329B forward feature frames plus current broker export refresh if available",
            "metric_or_output": "row count, gaps, duplicates, first/last timestamp, session coverage",
            "stop_or_block_condition": "blocked_forward_data_missing if latest data is absent or incomplete",
            "claim_effect": "determines whether materialized forward tests can be trusted",
        },
        {
            "test_id": "T02_fixed_threshold_score_replay",
            "target_run": NEXT_RUN_ID,
            "subject": "all Stage329 research ONNX controls",
            "sample_scope": "old train/WFO/OOS identity plus latest forward replay",
            "required_inputs": "run329C ONNX packages, threshold receipts, run329B feature frames",
            "metric_or_output": "score, signal, long/short mix, signal density, ONNX parity",
            "stop_or_block_condition": "invalid if any forward threshold search appears",
            "claim_effect": "materializes fixed-surface evidence without tuning",
        },
        {
            "test_id": "T03_raw_session_gap_pressure",
            "target_run": NEXT_RUN_ID,
            "subject": "raw-forward versus old-session parity supply",
            "sample_scope": "2026-04-14+ forward rows",
            "required_inputs": "raw feature frames and session-filtered feature frames",
            "metric_or_output": "raw/session rows, signal/day ratio, exclusive raw signal rate, side shift",
            "stop_or_block_condition": "reject as high pressure if density explosion repeats",
            "claim_effect": "prevents session-only positives from deciding the surface",
        },
        {
            "test_id": "T04_curve_pocket_and_underwater",
            "target_run": "run330C_forward_mt5_or_score_curve_review_v1",
            "subject": "candidate and negative-control curves",
            "sample_scope": "latest forward split and old split replay",
            "required_inputs": "trade list or score-signal equity proxy",
            "metric_or_output": "worst third, rolling window, underwater start/end, recovery",
            "stop_or_block_condition": "fail forward robustness if a single pocket carries unacceptable loss",
            "claim_effect": "turns equity shape into explicit evidence",
        },
        {
            "test_id": "T05_cost_stress",
            "target_run": "run330C_forward_mt5_or_score_curve_review_v1",
            "subject": "spread and slippage stress",
            "sample_scope": "latest forward and old OOS",
            "required_inputs": "trade list with round-trip count",
            "metric_or_output": "PF and net after 0, 0.25, 0.5, 1, 2, 3, 5 account-currency cost",
            "stop_or_block_condition": "fail if edge only exists at unstressed cost",
            "claim_effect": "checks whether the signal survives realistic frictions",
        },
        {
            "test_id": "T06_regime_attribution",
            "target_run": "run330D_regime_attribution_v1",
            "subject": "US100 macro and technical regimes",
            "sample_scope": "old OOS and latest forward",
            "required_inputs": "volatility, ADX, VIX, USD, rate, month/hour/session slices",
            "metric_or_output": "net/PF/trade count/expectancy by slice",
            "stop_or_block_condition": "inconclusive if regime joins are missing or time-shifted",
            "claim_effect": "finds whether the surface is only one regime pocket",
        },
        {
            "test_id": "T07_long_short_and_source_attribution",
            "target_run": "run330D_regime_attribution_v1",
            "subject": "direction and source contribution",
            "sample_scope": "each materialized surface",
            "required_inputs": "signal source labels and trade direction",
            "metric_or_output": "long/short attribution and source-level net/PF/count",
            "stop_or_block_condition": "inconclusive if signal source cannot be reconstructed",
            "claim_effect": "detects one-sided or source-specific fragility",
        },
        {
            "test_id": "T08_runtime_handoff_parity",
            "target_run": "run330E_mt5_runtime_probe_or_block_v1",
            "subject": "Python, ONNX, handoff, and MT5 tester agreement",
            "sample_scope": "narrow row-level replay plus latest forward tester payload",
            "required_inputs": "feature order CSV, ONNX model, signal payload, EA set file, tester output",
            "metric_or_output": "row-level probability/signal parity and tester telemetry",
            "stop_or_block_condition": "Forward Blocked if tester output or handoff is unavailable",
            "claim_effect": "separates research result from runtime evidence",
        },
        {
            "test_id": "T09_lot_normalized_review",
            "target_run": "run330F_lot_normalized_cost_curve_review_v1",
            "subject": "signal surface independent from lot sizing",
            "sample_scope": "latest forward trade list",
            "required_inputs": "order size, entry/exit, SL/TP, ATR risk fields",
            "metric_or_output": "lot-normalized net, expectancy, DD, recovery",
            "stop_or_block_condition": "inconclusive if lot fields are missing",
            "claim_effect": "checks whether sizing was carrying the result",
        },
        {
            "test_id": "T10_final_forward_decision",
            "target_run": "run330G_final_forward_decision_or_next_stage_v1",
            "subject": "forward-safe non-identity ONNX research packet",
            "sample_scope": "all completed Stage330 evidence",
            "required_inputs": "MT5 report, attribution reports, cost stress, curve pocket, parity receipts",
            "metric_or_output": "Forward Passed, Forward Failed, or Forward Blocked only",
            "stop_or_block_condition": "no final decision if any required evidence is missing",
            "claim_effect": "closes or hands off research without operating claim",
        },
    ]


def anti_overfit_plan() -> list[dict[str, Any]]:
    return [
        {
            "control_id": "AO01_predeclare_subjects",
            "rule": "Stage330B may test c56_plain plus fixed negative controls, but cannot add a late winner from forward profit.",
            "evidence": "stage330B_materialization_queue.csv",
            "effect": "keeps multiple testing visible",
        },
        {
            "control_id": "AO02_forward_holdout_is_read_only",
            "rule": "2026-04-14+ data is read-only for judgment, not for threshold, feature, or lot selection.",
            "evidence": "experiment_design_receipt.json",
            "effect": "protects forward sample from leakage",
        },
        {
            "control_id": "AO03_negative_controls_required",
            "rule": "At least one medium-pressure and two high-pressure controls must be reported next to any low-pressure clue.",
            "evidence": "candidate_evidence_input_matrix.csv",
            "effect": "prevents cherry-picking one appealing curve",
        },
        {
            "control_id": "AO04_density_guard_before_profit",
            "rule": "Raw/session signal density and exclusive raw signal rate are checked before profit interpretation.",
            "evidence": "robustness_test_queue.csv",
            "effect": "stops raw-forward supply mismatch from being hidden by KPI",
        },
        {
            "control_id": "AO05_no_lot_or_cost_repair",
            "rule": "Lot sizing, spread, slippage, ATR SL/TP, and decision rules remain fixed during forward tests.",
            "evidence": "design_guardrail_matrix.csv",
            "effect": "keeps execution settings from repairing a weak model",
        },
        {
            "control_id": "AO06_split_instability_kept",
            "rule": "Train/validation sign flip and WFO gaps are reported even if latest forward is positive.",
            "evidence": "source evidence snapshot",
            "effect": "keeps older instability in the decision",
        },
        {
            "control_id": "AO07_claim_downgrade_default",
            "rule": "Missing tester, feature, regime, or cost evidence downgrades to inconclusive or blocked.",
            "evidence": "result_judgment.csv",
            "effect": "prevents design completion from becoming Goal Achieve",
        },
    ]


def runtime_parity_plan() -> list[dict[str, Any]]:
    return [
        {
            "parity_id": "RP01_feature_order_identity",
            "research_path": "stages/329_onnx_rebuild__live_feature_control/02_runs/run329C/onnx/",
            "runtime_path": "future Stage330 handoff package",
            "shared_contract": "feature names, order, dtype, timestamp convention",
            "known_difference": "Stage330 is not cp322A exact identity; new model identity must be separate",
            "check": "hash feature order CSV and compare to ONNX input schema",
            "claim_boundary": "research_only_until_package_exists",
        },
        {
            "parity_id": "RP02_onnx_probability_parity",
            "research_path": "Python score replay",
            "runtime_path": "ONNX Runtime inference payload",
            "shared_contract": "probability output and active signal threshold",
            "known_difference": "no forward threshold retuning is allowed",
            "check": "row-level probability max abs diff and signal mismatch count",
            "claim_boundary": "model_validation_only",
        },
        {
            "parity_id": "RP03_handoff_payload_parity",
            "research_path": "Stage330 signal payload CSV/JSON",
            "runtime_path": "MT5 Files handoff input",
            "shared_contract": "timestamp, side, score, threshold, lot, ATR SL/TP fields",
            "known_difference": "broker session filter may remove rows and must be counted",
            "check": "row count, hash, and timestamp alignment before tester",
            "claim_boundary": "runtime_probe_only_after_tester_output",
        },
        {
            "parity_id": "RP04_mt5_tester_output",
            "research_path": "Python trade proxy if present",
            "runtime_path": "MT5 strategy tester report and telemetry",
            "shared_contract": "fills, skips, SL/TP, lot logic, costs, time range",
            "known_difference": "MT5 fill/order behavior is external evidence, not inferred",
            "check": "tester output path, report hash, telemetry row count, recomputed KPI",
            "claim_boundary": "no_runtime_authority_without_narrow_external_check",
        },
    ]


def materialization_queue(evidence_rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    queued = []
    for row in evidence_rows:
        slug = str(row["artifact_slug"])
        role = str(row["stage330_role"])
        priority = "P1" if slug == "c56_plain" else ("P2" if slug in {"c56_bal", "m48_plain"} else "P3")
        queued.append(
            {
                "queue_id": f"stage330B_{slug}",
                "next_run_id": NEXT_RUN_ID,
                "artifact_slug": slug,
                "candidate_id": row.get("candidate_id"),
                "feature_set_id": row.get("feature_set_id"),
                "model_id": row.get("model_id"),
                "role": role,
                "priority": priority,
                "allowed_action": "fixed_threshold_replay_and_guarded_payload_materialization",
                "forbidden_action": "forward_threshold_tuning;lot_optimization;decision_surface_repair_after_forward_result",
                "required_outputs": "score_signal_payload;raw_session_gap;onnx_parity_receipt;cost_curve_precheck",
                "effect": "turns Stage329 evidence into controlled Stage330 materialization input",
            }
        )
    queued.append(
        {
            "queue_id": "stage330B_feature_handoff_integrity_all",
            "next_run_id": NEXT_RUN_ID,
            "artifact_slug": "all",
            "candidate_id": "all_stage329_research_onnx_controls",
            "feature_set_id": "all",
            "model_id": "all",
            "role": "mandatory_integrity_audit",
            "priority": "P1",
            "allowed_action": "feature_order_hash_and_forward_data_availability_audit",
            "forbidden_action": "skip_missing_forward_data_or_assume_runtime_parity",
            "required_outputs": "data_integrity_receipt;feature_order_hashes;blocked_forward_data_missing_if_needed",
            "effect": "makes data and handoff availability decide whether testing can continue",
        }
    )
    return queued


def experiment_design_receipt() -> dict[str, Any]:
    return {
        "hypothesis": (
            "A non-identity ONNX built only from live-computable features may be more forward-safe than cp322A exact replay, "
            "but only if it survives raw/session gap, cost, curve, regime, and runtime parity checks without forward tuning."
        ),
        "decision_use": "decide whether to materialize controlled Stage330 surfaces and later judge Forward Passed/Failed/Blocked",
        "comparison_baseline": "Stage329 cp322A exact handoff blocked state plus Stage329 research ONNX controls",
        "control_variables": [
            "no cp322A exact repair claim",
            "no 2026-04-14+ threshold tuning",
            "fixed decision/risk/lot/ATR SLTP logic during replay",
            "raw and session views reported separately",
        ],
        "changed_variables": [
            "subject changes from cp322A identity ONNX to forward-safe non-identity research ONNX controls",
            "Stage330 adds explicit anti-overfit, raw-forward, regime, cost, and runtime parity gates",
        ],
        "sample_scope": "US100 M5 old train/WFO/OOS evidence plus 2026-04-14+ latest broker forward data when available",
        "success_criteria": [
            "fixed surface survives forward, raw/session, curve, cost, regime, and runtime parity evidence",
            "enough trades exist for judgment",
            "no missing forward data or handoff gap remains",
        ],
        "failure_criteria": [
            "net/PF/DD/curve pocket loses core behavior under fixed rules",
            "raw-forward signal density explodes",
            "cost stress or regime slices reveal non-robust one-pocket edge",
        ],
        "invalid_conditions": [
            "forward data incomplete",
            "feature order or timestamp boundary cannot be proven",
            "forward threshold, lot, or rule retuning occurs",
        ],
        "stop_conditions": [
            "blocked_forward_data_missing",
            "runtime parity handoff missing",
            "density explosion repeats in raw forward",
            "required report cannot be produced",
        ],
        "evidence_plan": [
            "frozen forward MT5 report",
            "regime attribution report",
            "source and direction attribution report",
            "lot-normalized report",
            "cost stress report",
            "curve pocket report",
            "final forward decision report",
        ],
    }


def data_integrity_receipt() -> dict[str, Any]:
    source_files = [SOURCE_GAP, SOURCE_PRESSURE, SOURCE_MT5, SOURCE_COST, SOURCE_CURVE, SOURCE_CLOSEOUT]
    return {
        "data_source": [rel(path) for path in source_files],
        "time_axis": "US100 M5 broker/server timestamps; raw and session-filtered views stay separate",
        "sample_scope": "Stage329 latest forward evidence begins 2026-04-14; cp322A exact route handoff has zero rows after 2026-04-13",
        "missing_or_duplicate_check": "run330A inherits Stage329 receipts; run330B must re-audit latest broker rows before materialization",
        "feature_label_boundary": "forward labels and forward profit cannot affect training, threshold, lot, or rule choices",
        "split_boundary": "old train/WFO/OOS evidence is separated from latest 2026-04-14+ forward holdout",
        "leakage_risk": "split-local rank, forward threshold search, and session-only success are the primary leakage paths",
        "data_hash_or_identity": {rel(path): sha256_file(path) for path in source_files},
        "integrity_judgment": "usable_with_boundary_for_design_only",
    }


def model_validation_receipt() -> dict[str, Any]:
    return {
        "model_family": "Stage329 live-computable LogisticRegression research ONNX controls; Stage330A trains no model",
        "target_and_label": "historical classification target inherited from Stage329; latest forward remains read-only",
        "split_method": "old train/WFO/OOS plus separate latest forward holdout after 2026-04-14",
        "selection_metric": "none in run330A; design only",
        "secondary_metrics": "PF, DD, expectancy, raw/session density, exclusive raw signals, cost stress, curve pockets, regime slices",
        "threshold_policy": "fixed from prior training/WFO design; no forward threshold tuning",
        "overfit_risk": "multiple controls, train/validation sign flip, session parity positives, and raw-forward density gaps",
        "calibration_risk": "scores are ordering/control signals, not calibrated probabilities unless separately proven",
        "comparison_baseline": "cp322A blocked exact artifact and Stage329 research controls",
        "validation_judgment": "exploratory_design_completed_no_model_selection",
    }


def runtime_parity_receipt() -> dict[str, Any]:
    return {
        "research_path": rel(Path(__file__)),
        "runtime_path": "not_materialized_in_run330A",
        "shared_contract": "future Stage330 packages must bind feature order, ONNX score, threshold, signal, lot, ATR SL/TP, and timestamp rules",
        "known_differences": "run330A is design only; Stage329 session MT5 evidence is not cp322A exact handoff and not runtime authority",
        "parity_check": "planned_for_run330B_to_run330E",
        "parity_identity": "source hashes captured in artifact_lineage_receipt.json",
        "runtime_claim_boundary": "research_only_no_runtime_authority",
    }


def result_judgment_rows() -> list[dict[str, Any]]:
    return [
        {
            "result_subject": RUN_ID,
            "evidence_available": "Stage329H closeout, Stage329G pressure, Stage329F MT5/cost/curve, Stage330A design artifacts",
            "evidence_missing": "new materialized payloads, refreshed latest forward data audit, MT5 tester output, regime/source/lot-normalized reports",
            "judgment_label": JUDGMENT,
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": NEXT_RUN_ID,
            "user_explanation_hook": "설계는 끝났지만 후보 선택이나 목표 달성은 아니다. 다음은 고정 규칙으로 물질화해 실제 검증하는 단계다.",
        }
    ]


def required_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "experiment_design",
            "status": "covered",
            "artifact_path": rel(RUN_DIR / "experiment_design_receipt.json"),
            "effect": "hypothesis, controls, success/failure/invalid/stop conditions are explicit",
        },
        {
            "gate_id": "data_integrity",
            "status": "covered_for_design",
            "artifact_path": rel(RUN_DIR / "data_integrity_receipt.json"),
            "effect": "forward data is not assumed complete before run330B",
        },
        {
            "gate_id": "model_validation",
            "status": "covered_for_design",
            "artifact_path": rel(RUN_DIR / "model_validation_receipt.json"),
            "effect": "no model selection, no threshold tuning, and overfit risks are named",
        },
        {
            "gate_id": "runtime_parity",
            "status": "planned_not_claimed",
            "artifact_path": rel(RUN_DIR / "runtime_parity_receipt.json"),
            "effect": "runtime authority is not claimed without future tester evidence",
        },
        {
            "gate_id": "result_judgment",
            "status": "covered",
            "artifact_path": rel(RUN_DIR / "result_judgment.csv"),
            "effect": "run330A closes as exploratory design only",
        },
        {
            "gate_id": "artifact_lineage",
            "status": "covered",
            "artifact_path": rel(RUN_DIR / "artifact_lineage_receipt.json"),
            "effect": "input and output hashes are tied to the run",
        },
    ]


def report_md(evidence_rows: Sequence[Mapping[str, Any]], queue_rows: Sequence[Mapping[str, Any]]) -> str:
    c56 = next(row for row in evidence_rows if row["artifact_slug"] == "c56_plain")
    high_count = sum(1 for row in evidence_rows if row["pressure_level"] == "high")
    queue_count = len(queue_rows)
    return f"""
# Run330A Forward-Safe Non-Identity Surface Robustness Design(330A 전진 안전 비정체성 표면 강건성 설계)

- stage(단계): `{STAGE_ID}`
- run(실행): `{RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- selected_candidate(선택 후보): `none`
- goal_achieve(목표 달성): `not_claimed`
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`

## Current Evidence Read(현재 근거 판독)

- cp322A exact replay(정확 재생)는 Stage329H(329H 단계 실행)에서 2026-04-14 이후 exact route-signal(정확 경로 신호) `0`행으로 Forward Blocked(전진 차단)다.
- c56_plain(코어56 일반)은 낮은 압력 단서지만 선택 후보가 아니다. session MT5 PF(세션 MT5 수익 팩터)는 `{c56.get('session_mt5_pf')}`, cost +1 PF(비용 +1 수익 팩터)는 `{c56.get('cost_1_pf')}`, worst rolling net(최악 이동 순손익)은 `{c56.get('worst_rolling_net')}`다.
- high pressure negative control(고압 부정 대조)는 `{high_count}`개다. Effect(효과): 낮은 압력 단서를 고르기 전에 raw/session density explosion(원본/세션 밀도 폭발)을 폐기 기준으로 세운다.

## Design Output(설계 산출)

- guardrails(방어 규칙): `10`
- robustness tests(강건성 시험): `10`
- anti-overfit controls(과적합 방어): `7`
- runtime parity plan(런타임 동등성 계획): `4`
- Stage330B materialization queue(330B 물질화 대기열): `{queue_count}`

## What This Does Not Claim(주장하지 않는 것)

- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- live readiness(실거래 준비): `not_claimed`
- deployment(배포): `not_claimed`
- operating promotion(운영 승격): `not_claimed`
- runtime authority(런타임 권위): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## Next Action(다음 행동)

`{NEXT_RUN_ID}`에서 최신 forward data(전진 데이터)를 먼저 감사하고, 고정 threshold(임계값), 고정 lot/risk(로트/위험), 고정 ATR SL/TP(ATR 손절/익절)로 대조 표면을 물질화한다.

Effect(효과): 수익이 좋아 보이는 한 후보를 바로 고르지 않고, 과적합/동등성/비용/곡선/국면 검증을 먼저 통과해야만 다음 판단으로 간다.
"""


def decision_doc_md() -> str:
    return f"""
# Decision: Stage330A Forward-Safe Non-Identity Design(결정: 330A 전진 안전 비정체성 설계)

- decision(결정): `{DECISION}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- selected_candidate(선택 후보): `none`
- goal_achieve(목표 달성): `not_claimed`

Stage330A(330A 단계 실행)는 cp322A exact repair(정확 수리)를 주장하지 않는다.
Effect(효과): cp322A는 연구 산출물로 보존하고, 새 비정체성 ONNX(온엑스)는 별도 검증 묶음에서만 다룬다.

Forward Passed(전진 통과), Forward Failed(전진 실패), live readiness(실거래 준비), deployment(배포), operating promotion(운영 승격), runtime authority(런타임 권위)는 모두 `not_claimed`다.
"""


def lineage_payload(generated_at_utc: str, artifacts: Sequence[Path]) -> dict[str, Any]:
    input_paths = [SOURCE_GAP, SOURCE_PRESSURE, SOURCE_MT5, SOURCE_COST, SOURCE_CURVE, SOURCE_CLOSEOUT, SOURCE_HANDOFF_QUEUE]
    return {
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "generated_at_utc": generated_at_utc,
        "inputs": [
            {
                "path": rel(path),
                "exists": path_exists(path),
                "sha256": sha256_file(path),
            }
            for path in input_paths
        ],
        "outputs": [
            {
                "path": rel(path),
                "exists": path_exists(path),
                "sha256": sha256_file(path),
            }
            for path in artifacts
            if path_is_file(path)
        ],
        "claim_boundary": CLAIM_BOUNDARY,
    }


def update_stage_docs() -> list[Path]:
    updated: list[Path] = []
    updated.append(
        write_md(
            SELECTED_DIR / "selection_status.md",
            f"""
# Stage330 Selection Status(330단계 선택 상태)

- stage_status(단계 상태): `open_design_completed`
- selected_candidate(선택 후보): `none`
- research_onnx_status(연구 온엑스 상태): `design_completed_no_new_model_trained`
- source_cp322A_status(원천 cp322A 상태): `research_artifact_preserved_exact_forward_handoff_blocked`
- latest_completed_run(최신 완료 실행): `{RUN_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- live_readiness(실거래 준비): `not_claimed`
- deployment(배포): `not_claimed`
- operating_promotion(운영 승격): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): Stage330(330단계)은 설계를 완료했지만 후보 확정이 아니며, 다음은 고정 규칙 물질화와 데이터/동등성 감사다.
""",
        )
    )
    append_if_missing(
        SPEC_DIR / "stage_brief.md",
        "run330A_design_summary",
        f"""
## run330A_design_summary(330A 설계 요약)

- run(실행): `{RUN_ID}`
- status(상태): `{STATUS}`
- decision(결정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): low-pressure clue(낮은 압력 단서)는 선택 후보가 아니라, raw/session gap(원본/세션 간극), cost stress(비용 압박), curve pocket(곡선 포켓), runtime parity(런타임 동등성)를 통과해야 하는 입력으로 남긴다.
""",
    )
    updated.append(SPEC_DIR / "stage_brief.md")
    append_if_missing(
        INPUTS_DIR / "input_refs.md",
        "run330A_design_outputs",
        f"""
## run330A_design_outputs(330A 설계 출력)

- design_report(설계 보고서): `stages/330_onnx_rebuild__forward_safe_non_identity_surface_robustness/03_reviews/run330A_forward_safe_non_identity_surface_robustness_design.md`
- candidate_evidence(후보 근거): `stages/330_onnx_rebuild__forward_safe_non_identity_surface_robustness/02_runs/run330A/candidate_evidence_input_matrix.csv`
- materialization_queue(물질화 대기열): `stages/330_onnx_rebuild__forward_safe_non_identity_surface_robustness/02_runs/run330A/stage330B_materialization_queue.csv`

Effect(효과): run330B(330B 실행)는 이 설계 출력만 입력으로 삼아 forward data audit(전진 데이터 감사)와 고정 규칙 replay(재생)를 시작한다.
""",
    )
    updated.append(INPUTS_DIR / "input_refs.md")
    return updated


def update_current_truth() -> list[Path]:
    updated: list[Path] = []
    workspace_text, workspace_bom = read_text_lossless(WORKSPACE_STATE)
    workspace_text = replace_prefix_line(workspace_text, "current_run_id:", f"current_run_id: {NEXT_RUN_ID}")
    workspace_text = replace_prefix_line(workspace_text, "updated_on:", f"updated_on: '{TODAY}'")
    workspace_text = replace_prefix_line(workspace_text, "active_stage:", f"active_stage: {STAGE_ID}")
    focus = (
        "- >-\n"
        f"  Stage330(330단계) run330A(330A 실행)는 `{STATUS}`로 설계를 완료했다. Effect(효과): c56_plain(낮은 압력 단서)을 선택하지 않고 run330B(330B 실행)의 고정 규칙 물질화와 데이터/동등성 감사로 넘긴다.\n"
    )
    if "Stage330(330단계) run330A(330A 실행)" not in workspace_text:
        workspace_text = workspace_text.replace("current_focus:\n", "current_focus:\n" + focus, 1)
    block_marker = "stage330A_forward_safe_non_identity_design:"
    block = f"""
stage330A_forward_safe_non_identity_design:
  packet_id: {STAGE_ID}_v1
  stage_id: {STAGE_ID}
  status: {STATUS}
  judgment: {JUDGMENT}
  decision: {DECISION}
  completed_run_id: {RUN_ID}
  next_run_id: {NEXT_RUN_ID}
  report_path: stages/330_onnx_rebuild__forward_safe_non_identity_surface_robustness/03_reviews/run330A_forward_safe_non_identity_surface_robustness_design.md
  boundary: {CLAIM_BOUNDARY}
"""
    if block_marker not in workspace_text:
        workspace_text = workspace_text.rstrip() + "\n\n" + block.strip() + "\n"
    write_text_lossless(WORKSPACE_STATE, workspace_text, workspace_bom)
    updated.append(WORKSPACE_STATE)

    current_text, current_bom = read_text_lossless(CURRENT_STATE)
    replacements = {
        "- current_packet(": f"- current_packet(현재 작업 묶음): `{STAGE_ID}_v2`",
        "- current_run(": f"- current_run(현재 실행): `{NEXT_RUN_ID}`",
        "- active_stage(": f"- active_stage(활성 단계): `{STAGE_ID}`",
        "- selected_research_baseline(": "- selected_research_baseline(선택 연구 기준선): `none`",
        "- source_stage(": f"- source_stage(원천 단계): `{SOURCE_STAGE_ID}`",
        "- target_surface(": "- target_surface(목표 표면): `forward_safe_non_identity_surface_robustness`",
        "- adapter_under_review(": "- adapter_under_review(검토 중 어댑터): `none`",
        "- status(": "- status(상태): `stage330_run330A_design_completed_materialization_next`",
        "- decision(": f"- decision(판정): `{DECISION}`",
        "- next_action(": f"- next_action(다음 행동): `{NEXT_RUN_ID}`",
        "- claim_boundary(": f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
    }
    for prefix, replacement in replacements.items():
        current_text = replace_prefix_line(current_text, prefix, replacement)
    summary = (
        f"- run330A_summary(330A 요약): forward-safe non-identity ONNX robustness design(전진 안전 비정체성 온엑스 강건성 설계)을 `{STATUS}`로 닫았다. "
        "Effect(효과): 후보 선택 없이 guardrail(방어 규칙), anti-overfit control(과적합 방어), runtime parity plan(런타임 동등성 계획), run330B materialization queue(330B 물질화 대기열)를 만들었다."
    )
    if "run330A_summary(330A 요약)" not in current_text:
        current_text = current_text.replace(f"- decision(판정): `{DECISION}`\n", f"- decision(판정): `{DECISION}`\n{summary}\n", 1)
    write_text_lossless(CURRENT_STATE, current_text, current_bom)
    updated.append(CURRENT_STATE)

    append_if_missing(
        CHANGELOG,
        "Stage330A Forward-Safe Non-Identity Surface Robustness Design",
        f"""
## 2026-05-26 - Stage330A Forward-Safe Non-Identity Surface Robustness Design(330A 전진 안전 비정체성 표면 강건성 설계)

- run330A(330A 실행): cp322A exact repair(정확 수리)를 주장하지 않고, live-computable non-identity ONNX(실시간 계산 가능 비정체성 온엑스)를 검증하기 위한 설계 묶음을 만들었다.
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- effect(효과): selected candidate(선택 후보), Forward Passed(전진 통과), Forward Failed(전진 실패), Goal Achieve(목표 달성)는 없고, 다음은 `{NEXT_RUN_ID}`다.
""",
    )
    updated.append(CHANGELOG)
    return updated


def update_registers(generated_at_utc: str, artifacts: Sequence[Path]) -> None:
    report_path = REVIEWS_DIR / "run330A_forward_safe_non_identity_surface_robustness_design.md"
    upsert_csv(
        RUN_REGISTRY,
        ["run_id"],
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "experiment_design",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(report_path),
                "notes": "forward_safe_non_identity_design;no_candidate_selection;next_run_materialization;goal_achieve_not_claimed.",
            }
        ],
    )
    ledger_row = {
        "ledger_row_id": f"{RUN_ID}__design_packet",
        "stage_id": STAGE_ID,
        "run_id": RUN_ID,
        "subrun_id": RUN_NUMBER,
        "parent_run_id": PARENT_RUN_ID,
        "record_view": "forward_safe_non_identity_design",
        "tier_scope": "old train/WFO/OOS evidence plus latest forward design scope",
        "kpi_scope": "experiment_design_data_integrity_model_validation_runtime_parity",
        "scoreboard_lane": "experiment_design",
        "status": STATUS,
        "judgment": JUDGMENT,
        "path": rel(report_path),
        "primary_kpi": "design_artifact_count",
        "guardrail_kpi": "no_forward_threshold_tuning;raw_session_gap_guard;runtime_parity_not_claimed",
        "external_verification_status": "out_of_scope_by_claim_design_only",
        "notes": f"decision={DECISION};next_action={NEXT_RUN_ID};goal_achieve_not_claimed.",
    }
    upsert_csv(ALPHA_LEDGER, ["ledger_row_id"], [ledger_row])
    upsert_csv(
        STAGE_LEDGER,
        ["row_id"],
        [
            {
                "row_id": f"{RUN_ID}__design_packet",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "view": "forward_safe_non_identity_design(전진 안전 비정체성 설계)",
                "tier_scope": "old train/WFO/OOS evidence plus latest forward design scope(기존 학습/워크포워드/표본외 및 최신 전진 설계 범위)",
                "scoreboard": "experiment_design_data_integrity_model_validation_runtime_parity(실험 설계/데이터 무결성/모델 검증/런타임 동등성)",
                "status": STATUS,
                "judgment": JUDGMENT,
                "evidence_boundary": CLAIM_BOUNDARY,
                "report_path": rel(report_path),
                "notes": "no_candidate_selection;no_forward_decision;goal_achieve_not_claimed.",
                "decision": DECISION,
            }
        ],
    )
    artifact_rows = []
    for path in artifacts:
        if path_is_file(path):
            artifact_rows.append(
                {
                    "artifact_id": f"{RUN_ID}:{rel(path)}",
                    "artifact_type": "stage330A_forward_safe_non_identity_design_artifact",
                    "path": rel(path),
                    "sha256": sha256_file(path),
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "created_at_utc": generated_at_utc,
                    "notes": "Stage330A design artifact; no selected candidate and no operating claim.",
                }
            )
    upsert_csv(ARTIFACT_REGISTRY, ["artifact_id"], artifact_rows)


def write_outputs(generated_at_utc: str) -> list[Path]:
    evidence = source_evidence_rows()
    guardrails = design_guardrails()
    tests = robustness_queue()
    anti_overfit = anti_overfit_plan()
    parity_plan = runtime_parity_plan()
    queue = materialization_queue(evidence)
    artifacts: list[Path] = []
    artifacts.append(write_json(RUN_DIR / "experiment_design_receipt.json", experiment_design_receipt()))
    artifacts.append(write_json(RUN_DIR / "data_integrity_receipt.json", data_integrity_receipt()))
    artifacts.append(write_json(RUN_DIR / "model_validation_receipt.json", model_validation_receipt()))
    artifacts.append(write_json(RUN_DIR / "runtime_parity_receipt.json", runtime_parity_receipt()))
    artifacts.append(
        write_csv(
            RUN_DIR / "candidate_evidence_input_matrix.csv",
            [
                "artifact_slug",
                "candidate_id",
                "feature_set_id",
                "model_id",
                "stage330_role",
                "pressure_level",
                "pressure_score",
                "pressure_flags",
                "session_mt5_net",
                "session_mt5_pf",
                "trade_count",
                "trades_per_day",
                "equity_dd_percent",
                "cost_1_pf",
                "cost_1_net",
                "cost_2_pf",
                "raw_session_signal_per_day_ratio",
                "exclusive_raw_signal_rate",
                "raw_row_supply_ratio",
                "long_share_shift",
                "wfo_min_balanced_accuracy",
                "train_oos_balanced_accuracy_gap",
                "worst_rolling_net",
                "worst_third_net",
                "stage330_use_note",
                "selection_status",
            ],
            evidence,
        )
    )
    artifacts.append(
        write_csv(
            RUN_DIR / "design_guardrail_matrix.csv",
            ["guardrail_id", "protected_failure_mode", "required_evidence", "pass_condition", "fail_condition", "effect"],
            guardrails,
        )
    )
    artifacts.append(
        write_csv(
            RUN_DIR / "robustness_test_queue.csv",
            [
                "test_id",
                "target_run",
                "subject",
                "sample_scope",
                "required_inputs",
                "metric_or_output",
                "stop_or_block_condition",
                "claim_effect",
            ],
            tests,
        )
    )
    artifacts.append(write_csv(RUN_DIR / "anti_overfit_control_plan.csv", ["control_id", "rule", "evidence", "effect"], anti_overfit))
    artifacts.append(
        write_csv(
            RUN_DIR / "runtime_parity_plan.csv",
            ["parity_id", "research_path", "runtime_path", "shared_contract", "known_difference", "check", "claim_boundary"],
            parity_plan,
        )
    )
    artifacts.append(
        write_csv(
            RUN_DIR / "stage330B_materialization_queue.csv",
            [
                "queue_id",
                "next_run_id",
                "artifact_slug",
                "candidate_id",
                "feature_set_id",
                "model_id",
                "role",
                "priority",
                "allowed_action",
                "forbidden_action",
                "required_outputs",
                "effect",
            ],
            queue,
        )
    )
    artifacts.append(
        write_csv(
            RUN_DIR / "result_judgment.csv",
            [
                "result_subject",
                "evidence_available",
                "evidence_missing",
                "judgment_label",
                "claim_boundary",
                "next_condition",
                "user_explanation_hook",
            ],
            result_judgment_rows(),
        )
    )
    artifacts.append(
        write_csv(RUN_DIR / "required_gate_coverage_audit.csv", ["gate_id", "status", "artifact_path", "effect"], required_gate_rows())
    )
    artifacts.append(write_md(REVIEWS_DIR / "run330A_forward_safe_non_identity_surface_robustness_design.md", report_md(evidence, queue)))
    artifacts.append(write_md(DECISION_DOC, decision_doc_md()))
    artifacts.extend(update_stage_docs())
    artifacts.extend(update_current_truth())
    artifacts.append(
        write_json(
            RUN_DIR / "run_manifest.json",
            {
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "run_number": RUN_NUMBER,
                "parent_run_id": PARENT_RUN_ID,
                "generated_at_utc": generated_at_utc,
                "status": STATUS,
                "judgment": JUDGMENT,
                "decision": DECISION,
                "next_action": NEXT_RUN_ID,
                "claim_boundary": CLAIM_BOUNDARY,
                "selected_candidate": "none",
                "goal_achieve": "not_claimed",
                "external_verification_status": "out_of_scope_by_claim_design_only",
            },
        )
    )
    artifacts.append(write_json(RUN_DIR / "artifact_lineage_receipt.json", lineage_payload(generated_at_utc, artifacts)))
    update_registers(generated_at_utc, artifacts)
    return artifacts


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create Stage330A forward-safe non-identity robustness design artifacts.")
    return parser.parse_args()


def main() -> None:
    _ = parse_args()
    generated_at_utc = utc_now()
    artifacts = write_outputs(generated_at_utc)
    print(
        json.dumps(
            {
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "decision": DECISION,
                "next_action": NEXT_RUN_ID,
                "artifact_count": len(artifacts),
                "selected_candidate": "none",
                "goal_achieve": "not_claimed",
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
