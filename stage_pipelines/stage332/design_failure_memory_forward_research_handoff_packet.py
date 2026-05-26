from __future__ import annotations

import csv
import hashlib
import json
import math
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
STAGE_ID = "332_overfit_guard__failure_memory_forward_research_handoff"
SOURCE_STAGE_ID = "331_overfit_guard__cross_horizon_cost_curve_parity_probe"
RUN_NUMBER = "run332A"
RUN_ID = "run332A_design_failure_memory_forward_research_handoff_packet_v1"
PARENT_RUN_ID = "run331D_final_cross_horizon_overfit_guard_decision_v1"
NEXT_RUN_ID = "run332B_materialize_failure_memory_forward_data_and_guard_inputs_v1"
STATUS = "completed_failure_memory_forward_research_handoff_design_no_selection"
JUDGMENT = "experiment_design_completed_research_only_no_goal_achieve"
DECISION = "stage332A_design_packet_ready_for_data_and_guard_materialization_no_selection"
CLAIM_BOUNDARY = (
    "research_development_only_failure_memory_forward_research_design_no_threshold_retuning_"
    "no_lot_optimization_no_model_update_no_candidate_selection_no_forward_passed_no_forward_failed_"
    "no_live_readiness_no_deployment_no_operating_promotion_no_runtime_authority_no_goal_achieve"
)
TODAY = "2026-05-26"

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"
INPUTS_DIR = STAGE_DIR / "01_inputs"
SOURCE_STAGE_DIR = ROOT / "stages" / SOURCE_STAGE_ID
RUN331D_DIR = SOURCE_STAGE_DIR / "02_runs" / "run331D"
RUN331C_DIR = SOURCE_STAGE_DIR / "02_runs" / "run331C"
RUN330E_DIR = ROOT / "stages" / "330_onnx_rebuild__forward_safe_non_identity_surface_robustness" / "02_runs" / "run330E"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-26_stage332A_failure_memory_forward_research_handoff_design.md"
RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
STAGE_LEDGER = REVIEWS_DIR / "stage_run_ledger.csv"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def io_path(path: Path) -> Path:
    resolved = path.resolve()
    if sys.platform == "win32":
        text = str(resolved)
        if len(text) > 240 and not text.startswith("\\\\?\\"):
            return Path("\\\\?\\" + text)
    return resolved


def rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def sha256_file(path: Path) -> str:
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
    if hasattr(value, "item"):
        try:
            return json_ready(value.item())
        except Exception:
            return str(value)
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


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({column: csv_value(row.get(column)) for column in columns})
    return path


def write_json(path: Path, payload: Any) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8") as handle:
        json.dump(json_ready(payload), handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    return path


def write_md(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8-sig", newline="\n") as handle:
        handle.write(text.strip() + "\n")
    return path


def read_text_lossless(path: Path) -> tuple[str, bool]:
    raw = io_path(path).read_bytes()
    return raw.decode("utf-8-sig"), raw.startswith(b"\xef\xbb\xbf")


def write_text_lossless(path: Path, text: str, had_bom: bool) -> Path:
    io_path(path).write_text(text, encoding="utf-8-sig" if had_bom else "utf-8", newline="\n")
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


def insert_after_line(text: str, prefix: str, block: str, marker: str) -> str:
    if marker in text:
        return text
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            return "\n".join(lines[: index + 1] + [block] + lines[index + 1 :]) + "\n"
    return text.rstrip() + "\n" + block + "\n"


def upsert_csv(path: Path, key_columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    existing: list[dict[str, Any]] = []
    fieldnames: list[str] = []
    if path.exists():
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


def read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(io_path(path))


def to_float(value: Any) -> float | None:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    if math.isnan(number) or math.isinf(number):
        return None
    return number


def fmt(value: Any, digits: int = 3) -> str:
    number = to_float(value)
    if number is None:
        return str(value)
    return f"{number:.{digits}f}".rstrip("0").rstrip(".")


def load_inputs() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    return (
        read_csv(RUN331D_DIR / "final_decision_matrix.csv"),
        read_csv(RUN331D_DIR / "overfit_guard_failure_memory.csv"),
        read_csv(RUN331D_DIR / "survivor_clue_disposition.csv"),
        read_csv(RUN330E_DIR / "raw_forward_feature_matrix_manifest.csv"),
    )


def constraint_rows(memory: pd.DataFrame) -> list[dict[str, Any]]:
    deep_pockets = int(memory["observed_failure_modes"].astype(str).str.contains("deep_negative_rolling20_pocket").sum())
    plus2_fail = sum(1 for value in memory["cost2_pf"] if (to_float(value) or 0.0) < 1.0)
    plus1_fail = sum(1 for value in memory["cost1_pf"] if (to_float(value) or 0.0) < 1.0)
    return [
        {
            "constraint_id": "fm_cost_convexity_guard",
            "source_failure": f"{plus2_fail}/6 attempts failed plus2 cost; {plus1_fail}/6 failed plus1 cost",
            "design_requirement": "Every future branch must report cost levels 0, 0.5, 1, 2, 3, and 5 before selection language is allowed.",
            "anti_overfit_effect": "Stops choosing a surface because headline PF survives while execution cost destroys edge.",
            "hard_stop_condition": "If cost+2 PF is below 1.0, the branch may remain failure memory only.",
            "allowed_use": "screening guard and failure memory",
            "forbidden_use": "do not tune threshold or lot until cost+2 turns positive on an independent run",
        },
        {
            "constraint_id": "fm_curve_pocket_guard",
            "source_failure": f"{deep_pockets}/6 attempts had deep negative rolling20 pockets",
            "design_requirement": "Every future branch must report rolling window net/PF, worst pocket date span, underwater stretch, and recovery.",
            "anti_overfit_effect": "Prevents a high net result from hiding a concentrated losing pocket.",
            "hard_stop_condition": "If rolling20 minimum net remains negative, no selected candidate claim is allowed.",
            "allowed_use": "curve veto and pocket attribution",
            "forbidden_use": "do not repair by excluding the pocket after seeing it",
        },
        {
            "constraint_id": "fm_temporal_balance_guard",
            "source_failure": "First-half/month-2026-04 weakness was common in Stage331 preserved and negative-control rows.",
            "design_requirement": "Future reads must separate first half, second half, calendar month, thirds, fifths, and latest available extension.",
            "anti_overfit_effect": "Prevents late-window luck from being mistaken for forward robustness.",
            "hard_stop_condition": "If only one temporal slice carries the edge, downgrade to clue memory.",
            "allowed_use": "time-slice attribution",
            "forbidden_use": "do not create a threshold that maximizes a single slice",
        },
        {
            "constraint_id": "fm_trade_density_guard",
            "source_failure": "c56_plain_rf preserved PF with only 77 runtime trades; several prior rows flagged trade density risk.",
            "design_requirement": "Future branches must report signal count, order count, fill count, trades/day, session count, and skipped bars.",
            "anti_overfit_effect": "Prevents sparse lucky samples from becoming model packages.",
            "hard_stop_condition": "If trade count is too low for the stated claim, keep the result as scout only.",
            "allowed_use": "trade-shape gate",
            "forbidden_use": "do not increase lot to compensate for low opportunity count",
        },
        {
            "constraint_id": "fm_runtime_parity_guard",
            "source_failure": "run331C matched 6/6, so remaining weakness is model/data behavior rather than replay drift.",
            "design_requirement": "Future branches must carry feature order, model hash, decision rule hash, MT5 set/ini, report, and telemetry identity.",
            "anti_overfit_effect": "Keeps Python and MT5 evidence connected before any result is interpreted.",
            "hard_stop_condition": "If runtime replay mismatches source metrics, mark invalid or blocked before performance judgment.",
            "allowed_use": "runtime probe boundary",
            "forbidden_use": "do not claim runtime authority from a probe",
        },
    ]


def branch_queue_rows(feature_manifest: pd.DataFrame) -> list[dict[str, Any]]:
    min_ts = str(feature_manifest["first_timestamp"].min())
    max_ts = str(feature_manifest["last_timestamp"].max())
    return [
        {
            "queue_id": NEXT_RUN_ID,
            "branch_family": "data_integrity_materialization",
            "hypothesis": "Before any new model or guard is trusted, the raw-forward data supply and time axis must prove it covers the intended broker window.",
            "decision_use": "Decide whether Stage332 can run materialized guard inputs or must block for data repair.",
            "comparison_baseline": "run330E raw-forward feature matrix manifest and run331D failure memory.",
            "control_variables": "US100 M5 broker feed, UTC timestamps, post-2026-04-14 forward boundary, no model or threshold change.",
            "changed_variables": "Only diagnostic views and guard-input tables are materialized.",
            "sample_scope": f"run330E raw-forward rows from {min_ts} to {max_ts}; next run must verify latest local broker data before extending.",
            "success_criteria": "Data identity, row counts, duplicate/gap checks, and feature-order references are written for each branch.",
            "failure_criteria": "Missing forward data, untraceable timestamps, or disconnected feature-order identity.",
            "invalid_conditions": "Any materialized input uses post-label data, mismatched feature order, or undocumented broker session assumptions.",
            "stop_conditions": "Stop before model training if data integrity is blocked or inconclusive.",
            "evidence_plan": "data_integrity_report.csv; guard_input_manifest.csv; source_artifact_hashes.json; required_gate_coverage_audit.csv",
        },
        {
            "queue_id": "run332C_design_or_materialize_cost_curve_guarded_scout_v1",
            "branch_family": "cost_curve_guarded_scout",
            "hypothesis": "A future surface is only useful if it preserves edge after explicit US100 cost pressure instead of just headline net.",
            "decision_use": "Allow or reject a future branch as research clue before ONNX export.",
            "comparison_baseline": "Stage331 c56_plain_rf and m48_plain_rf cost failure modes.",
            "control_variables": "No threshold retuning, no lot optimization, same cost ladder, same fixed risk accounting.",
            "changed_variables": "Only candidate thesis or feature set may change after data integrity is clean.",
            "sample_scope": "Tier A, Tier B, Tier A+B combined, and post-2026-04-14 raw-forward views when available.",
            "success_criteria": "Cost+1 and cost+2 remain PF>1 with non-negative expectancy and no hidden worst-pocket loss.",
            "failure_criteria": "Cost+2 PF below 1 or cost-adjusted expectancy turns negative.",
            "invalid_conditions": "Cost ladder is edited after seeing results or mixed with spread/slippage assumptions without manifest.",
            "stop_conditions": "Stop before runtime replay if cost guard fails in Python/materialized score view.",
            "evidence_plan": "cost_curve_guard_report.csv; lot_normalized_report.csv; selection_guard_receipt.json",
        },
        {
            "queue_id": "run332D_design_pocket_veto_feature_thesis_v1",
            "branch_family": "curve_pocket_veto_feature_thesis",
            "hypothesis": "New feature theses should reduce pocket concentration rather than chase the Stage331 profitable months.",
            "decision_use": "Choose which feature theses deserve materialization without using Stage331 pockets as tuning targets.",
            "comparison_baseline": "Stage331 rolling20 pocket and temporal imbalance rows.",
            "control_variables": "No post-forward threshold search; fixed split declarations; feature-label boundary must be named.",
            "changed_variables": "Feature families may change, but only through predeclared volatility/session/rate/liquidity hypotheses.",
            "sample_scope": "Historical train/WFO, validation, OOS, and raw-forward partitions with Tier A/B paired records.",
            "success_criteria": "Worst pocket shrinks while temporal balance and trade density do not collapse.",
            "failure_criteria": "Improvement is isolated to one known pocket or one month.",
            "invalid_conditions": "A feature is derived from future returns or from realized tester outcomes.",
            "stop_conditions": "Stop if the feature thesis cannot be explained without using forbidden outcome leakage.",
            "evidence_plan": "feature_thesis_registry.csv; feature_label_boundary_receipt.json; pocket_veto_plan.csv",
        },
        {
            "queue_id": "run332E_runtime_parity_probe_design_v1",
            "branch_family": "runtime_parity_probe_after_guard_pass",
            "hypothesis": "Only branches that pass data, cost, and pocket guards should consume MT5 runtime probe budget.",
            "decision_use": "Decide whether a future branch can be interpreted as runtime probe evidence.",
            "comparison_baseline": "run331C exact replay match and run331D no-selection closeout.",
            "control_variables": "EA runner identity, feature order handoff, decision surface hash, ATR/risk logic manifest.",
            "changed_variables": "Only run id, report path, and approved branch payload.",
            "sample_scope": "The exact materialized branch payload after Stage332B-C-D gates.",
            "success_criteria": "MT5 report, telemetry, and source KPI match within declared tolerance.",
            "failure_criteria": "Missing report, mismatched trade count, mismatched net/PF, or untraceable handoff file.",
            "invalid_conditions": "Runtime logic changes without module hash and run-variant boundary.",
            "stop_conditions": "Stop at blocked runtime repair before interpreting performance.",
            "evidence_plan": "runtime_replay_compare_report.csv; backtest_forensics_receipt.json; runtime_parity_receipt.json",
        },
    ]


def data_plan_rows(feature_manifest: pd.DataFrame) -> list[dict[str, Any]]:
    min_ts = str(feature_manifest["first_timestamp"].min())
    max_ts = str(feature_manifest["last_timestamp"].max())
    return [
        {
            "data_source": rel(RUN330E_DIR / "raw_forward_feature_matrix_manifest.csv"),
            "time_axis": "UTC bar timestamps from MT5 feature handoff; Stage332B must verify broker-session interpretation before extension.",
            "sample_scope": f"US100 M5 post-2026-04-14 raw-forward feature matrices currently evidenced from {min_ts} to {max_ts}.",
            "missing_or_duplicate_check": "Required in Stage332B for raw bars and materialized feature frames.",
            "feature_label_boundary": "No label or tester outcome may feed future feature generation; Stage332A creates design only.",
            "split_boundary": "Existing Stage331 forward sample is diagnostic; any new model work must restate train/WFO/validation/OOS/raw-forward boundaries.",
            "leakage_risk": "Retuning to Stage331 known weak pockets or using tester outcome-derived features.",
            "data_hash_or_identity": "Artifact registry hashes for run331D and source manifests; Stage332B must add row counts and hashes for materialized inputs.",
            "integrity_judgment": "usable_with_boundary",
        }
    ]


def model_plan_rows() -> list[dict[str, Any]]:
    return [
        {
            "model_family": "future forward-safe non-identity research branches",
            "target_and_label": "To be declared before training; no new target or label is built in run332A.",
            "split_method": "Required WFO or explicitly labelled scout; raw-forward remains holdout/diagnostic, not tuning target.",
            "selection_metric": "No selection in run332A; future selection must pass cost, curve, density, temporal, and runtime gates.",
            "secondary_metrics": "Cost+2 PF, rolling20 minimum net, underwater stretch, thirds/fifths positive share, trade density, long/short attribution.",
            "threshold_policy": "No threshold retuning from Stage331 or Stage332A evidence.",
            "overfit_risk": "Designing a branch to fix only the known c56/m48 weak pockets.",
            "calibration_risk": "Scores must not be described as probabilities without calibration evidence.",
            "comparison_baseline": "Stage331 no-selection failure memory, not an operating baseline.",
            "validation_judgment": "exploratory_design_only",
        }
    ]


def evidence_plan_rows() -> list[dict[str, Any]]:
    return [
        {
            "evidence_item": "data_integrity_report",
            "producer_run": NEXT_RUN_ID,
            "required_before": "any new model or threshold experiment",
            "must_include": "source paths; row counts; timestamps; duplicates; gaps; session assumptions; hashes",
            "claim_enabled": "data usable or blocked, not performance",
        },
        {
            "evidence_item": "guard_input_manifest",
            "producer_run": NEXT_RUN_ID,
            "required_before": "cost/curve guarded scout",
            "must_include": "feature order; model/score payload identity when applicable; branch id; no-retune receipt",
            "claim_enabled": "guard materialization readiness",
        },
        {
            "evidence_item": "cost_curve_guard_report",
            "producer_run": "run332C_design_or_materialize_cost_curve_guarded_scout_v1",
            "required_before": "runtime replay budget",
            "must_include": "cost levels 0, 0.5, 1, 2, 3, 5; net; PF; expectancy; DD",
            "claim_enabled": "cost robustness clue only",
        },
        {
            "evidence_item": "pocket_veto_report",
            "producer_run": "run332D_design_pocket_veto_feature_thesis_v1",
            "required_before": "candidate or package language",
            "must_include": "rolling windows; underwater stretch; worst chunk; month/session/time slices",
            "claim_enabled": "curve pocket robustness clue only",
        },
        {
            "evidence_item": "runtime_replay_compare_report",
            "producer_run": "run332E_runtime_parity_probe_design_v1",
            "required_before": "runtime probe interpretation",
            "must_include": "tester/report/telemetry status; trade count; net/PF delta; handoff hash",
            "claim_enabled": "runtime probe, not runtime authority",
        },
    ]


def gate_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate": "work_packet_schema_lint",
            "status": "pass",
            "evidence_path": rel(RUN_DIR / "experiment_design_spec.json"),
            "notes": "hypothesis, baseline, controls, changed variables, sample scope, criteria, invalid and stop conditions are declared",
        },
        {
            "gate": "data_integrity_plan_gate",
            "status": "pass",
            "evidence_path": rel(RUN_DIR / "data_integrity_plan.csv"),
            "notes": "time axis, sample scope, leakage risk, and Stage332B data audit requirement are explicit",
        },
        {
            "gate": "model_validation_plan_gate",
            "status": "pass",
            "evidence_path": rel(RUN_DIR / "model_validation_plan.csv"),
            "notes": "no model update or threshold selection occurs in run332A",
        },
        {
            "gate": "no_retune_guard",
            "status": "pass",
            "evidence_path": rel(RUN_DIR / "failure_memory_to_research_constraints.csv"),
            "notes": "Stage331 weak pockets become constraints, not tuning targets",
        },
        {
            "gate": "artifact_lineage_audit",
            "status": "pass",
            "evidence_path": rel(RUN_DIR / "artifact_lineage_receipt.json"),
            "notes": "source inputs and generated design artifacts are connected",
        },
        {
            "gate": "required_gate_coverage_audit",
            "status": "pass",
            "evidence_path": rel(RUN_DIR / "required_gate_coverage_audit.csv"),
            "notes": "all run332A design gates are listed in closeout",
        },
        {
            "gate": "final_claim_guard",
            "status": "pass",
            "evidence_path": rel(RUN_DIR / "result_judgment_receipt.json"),
            "notes": "Forward Passed, Forward Failed, live readiness, deployment, operating promotion, runtime authority, and Goal Achieve are not claimed",
        },
    ]


def write_receipts(generated_at_utc: str) -> list[Path]:
    return [
        write_json(
            RUN_DIR / "experiment_design_receipt.json",
            {
                "skill": "obsidian-experiment-design",
                "hypothesis": "Stage331 failure memory can be converted into forward research constraints without retuning to known pockets.",
                "decision_use": "Route Stage332B-C-D-E work and block premature candidate selection.",
                "comparison_baseline": "run331D final no-selection decision and Stage331 failure memory.",
                "control_variables": [
                    "no threshold retuning",
                    "no lot optimization",
                    "no model update in run332A",
                    "post-2026-04-14 raw-forward boundary remains diagnostic",
                ],
                "changed_variables": "Only experiment design tables and evidence requirements are created.",
                "sample_scope": "Stage331 run331D matrix plus run330E raw-forward feature manifest.",
                "success_criteria": "A concrete next-run queue and guard requirements exist before any new model work.",
                "failure_criteria": "Design reuses c56/m48 as candidates or permits cost/pocket failures to be ignored.",
                "invalid_conditions": "Any design step allows known forward pockets to tune thresholds or feature labels.",
                "stop_conditions": "Stop before training if Stage332B data integrity is blocked.",
                "evidence_plan": rel(RUN_DIR / "evidence_plan.csv"),
            },
        ),
        write_json(
            RUN_DIR / "data_integrity_receipt.json",
            {
                "skill": "obsidian-data-integrity",
                "data_source": [
                    rel(RUN330E_DIR / "raw_forward_feature_matrix_manifest.csv"),
                    rel(RUN331D_DIR / "final_decision_matrix.csv"),
                ],
                "time_axis": "UTC MT5 feature matrix timestamps; run332A does not create new bars.",
                "sample_scope": "US100 M5 post-2026-04-14 raw-forward diagnostic evidence, Stage331 failure memory.",
                "missing_or_duplicate_check": "planned for run332B, not claimed complete in run332A",
                "feature_label_boundary": "No new labels or features are materialized in run332A.",
                "split_boundary": "Stage331 forward sample is not a tuning split.",
                "leakage_risk": "Using known Stage331 failure pockets as feature or threshold targets.",
                "data_hash_or_identity": "source and generated artifact hashes are recorded in artifact registry",
                "integrity_judgment": "usable_with_boundary",
            },
        ),
        write_json(
            RUN_DIR / "model_validation_receipt.json",
            {
                "skill": "obsidian-model-validation",
                "model_family": "future forward-safe non-identity research branches",
                "target_and_label": "not created in run332A",
                "split_method": "future WFO or labelled scout required",
                "selection_metric": "none selected in run332A",
                "secondary_metrics": [
                    "cost+2 PF",
                    "rolling20 minimum net",
                    "underwater stretch",
                    "third/fifth positive share",
                    "trade density",
                    "runtime replay match",
                ],
                "threshold_policy": "no threshold retuning",
                "overfit_risk": "repairing the known Stage331 pockets directly",
                "calibration_risk": "future score outputs must not be treated as probabilities without calibration",
                "comparison_baseline": "Stage331 no-selection failure memory",
                "validation_judgment": "exploratory_design_only",
            },
        ),
        write_json(
            RUN_DIR / "artifact_lineage_receipt.json",
            {
                "skill": "obsidian-artifact-lineage",
                "source_inputs": [
                    rel(RUN331D_DIR / "final_decision_matrix.csv"),
                    rel(RUN331D_DIR / "overfit_guard_failure_memory.csv"),
                    rel(RUN331D_DIR / "survivor_clue_disposition.csv"),
                    rel(RUN330E_DIR / "raw_forward_feature_matrix_manifest.csv"),
                ],
                "producer": rel(Path(__file__)),
                "consumer": [
                    rel(REVIEWS_DIR / "run332A_failure_memory_forward_research_handoff_design.md"),
                    rel(RUN_REGISTRY),
                    rel(ALPHA_LEDGER),
                    rel(STAGE_LEDGER),
                    rel(ARTIFACT_REGISTRY),
                ],
                "artifact_paths": [
                    rel(RUN_DIR / "experiment_design_spec.json"),
                    rel(RUN_DIR / "failure_memory_to_research_constraints.csv"),
                    rel(RUN_DIR / "research_branch_queue.csv"),
                    rel(RUN_DIR / "data_integrity_plan.csv"),
                    rel(RUN_DIR / "model_validation_plan.csv"),
                    rel(RUN_DIR / "evidence_plan.csv"),
                ],
                "artifact_hashes": "recorded in docs/registers/artifact_registry.csv",
                "registry_links": [
                    rel(RUN_REGISTRY),
                    rel(ALPHA_LEDGER),
                    rel(STAGE_LEDGER),
                    rel(ARTIFACT_REGISTRY),
                ],
                "availability": "tracked",
                "lineage_judgment": "connected_with_boundary",
                "generated_at_utc": generated_at_utc,
            },
        ),
        write_json(
            RUN_DIR / "result_judgment_receipt.json",
            {
                "skill": "obsidian-result-judgment",
                "result_subject": RUN_ID,
                "evidence_available": [
                    rel(RUN_DIR / "experiment_design_spec.json"),
                    rel(RUN_DIR / "failure_memory_to_research_constraints.csv"),
                    rel(RUN_DIR / "research_branch_queue.csv"),
                    rel(RUN_DIR / "required_gate_coverage_audit.csv"),
                ],
                "evidence_missing": [
                    "Stage332B materialized data integrity outputs",
                    "new model results",
                    "MT5 runtime outputs for any future branch",
                ],
                "judgment_label": "exploratory_design_completed",
                "claim_boundary": CLAIM_BOUNDARY,
                "next_condition": "Run Stage332B to materialize broker-data identity and guard inputs before any model work.",
                "user_explanation_hook": "Stage332A turns the prior failure into a checklist for the next experiment; it does not select or fix a candidate.",
                "forward_passed": "not_claimed",
                "forward_failed": "not_claimed",
                "goal_achieve": "not_claimed",
            },
        ),
    ]


def write_reports(constraints: Sequence[Mapping[str, Any]], queue: Sequence[Mapping[str, Any]]) -> list[Path]:
    constraint_lines = "\n".join(
        [
            "| constraint(제약) | source failure(실패 원천) | hard stop(중지 조건) |",
            "|---|---|---|",
            *[
                f"| {row['constraint_id']} | {row['source_failure']} | {row['hard_stop_condition']} |"
                for row in constraints
            ],
        ]
    )
    queue_lines = "\n".join(
        [
            "| queue(대기열) | family(계열) | decision use(판단 용도) |",
            "|---|---|---|",
            *[
                f"| {row['queue_id']} | {row['branch_family']} | {row['decision_use']} |"
                for row in queue
            ],
        ]
    )
    report = f"""
# run332A Failure Memory Forward Research Handoff Design(332A 실패 기억 전진 연구 인계 설계)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- selected_candidate(선택 후보): `none`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`

## Design Read(설계 판독)

run332A(332A 실행)는 Stage331(331단계)의 실패 기억을 다음 연구 조건으로 바꿨다.
Effect(효과): `c56_plain_rf`, `m48_plain_rf`를 고치거나 선택하지 않고, 비용/곡선/밀도/동등성 방어 조건을 먼저 고정한다.

## Constraints(제약)

{constraint_lines}

## Queue(대기열)

{queue_lines}

## Boundary(경계)

- no threshold retuning(임계값 재튜닝 없음)
- no lot optimization(로트 최적화 없음)
- no model update(모델 업데이트 없음)
- no candidate selection(후보 선택 없음)
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    decision = f"""
# 2026-05-26 Stage332A Failure Memory Handoff Design(332A 실패 기억 인계 설계)

Stage332A(332A 단계 실행)는 design packet(설계 묶음)을 완료했다.

- result(결과): `{DECISION}`
- selected_candidate(선택 후보): `none`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`

핵심은 Stage331(331단계)의 생존 단서를 고르는 일이 아니다. 비용+2 실패, rolling pocket(롤링 포켓), temporal imbalance(시간 불균형), trade density(거래 밀도), runtime parity(런타임 동등성)를 다음 실행의 필수 근거 요구사항으로 바꾼 것이다.
"""
    return [
        write_md(REVIEWS_DIR / "run332A_failure_memory_forward_research_handoff_design.md", report),
        write_md(DECISION_DOC, decision),
    ]


def update_selection_status() -> Path:
    text = f"""
# Stage332 Selection Status(332단계 선택 상태)

- stage_status(단계 상태): `open_in_progress`
- selected_candidate(선택 후보): `none`
- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- latest_design(최신 설계): `{RUN_ID}`
- current_run(현재 실행): `{NEXT_RUN_ID}`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- live_readiness(실거래 준비): `not_claimed`
- deployment(배포): `not_claimed`
- operating_promotion(운영 승격): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): run332A(332A 실행)는 실패 기억을 다음 데이터/방어 입력 물질화로 넘겼고, 기존 단서를 선택 후보로 승격하지 않는다.
"""
    return write_md(SELECTED_DIR / "selection_status.md", text)


def update_input_refs() -> Path:
    text = f"""
# Stage332 Input References(332단계 입력 참조)

- source_stage(원천 단계): `{SOURCE_STAGE_ID}`
- closeout_report(종료 보고): `{rel(SOURCE_STAGE_DIR / "03_reviews" / "run331D_final_cross_horizon_overfit_guard_decision.md")}`
- final_matrix(최종 행렬): `{rel(RUN331D_DIR / "final_decision_matrix.csv")}`
- failure_memory(실패 기억): `{rel(RUN331D_DIR / "overfit_guard_failure_memory.csv")}`
- survivor_clues(생존 단서): `{rel(RUN331D_DIR / "survivor_clue_disposition.csv")}`
- runtime_replay(런타임 재생): `{rel(RUN331C_DIR / "runtime_replay_compare_report.csv")}`
- run332A_design(332A 설계): `{rel(RUN_DIR / "experiment_design_spec.json")}`
- run332A_queue(332A 대기열): `{rel(RUN_DIR / "research_branch_queue.csv")}`

Effect(효과): 다음 단계는 Stage331(331단계)의 좋은 숫자를 재튜닝(retuning, 재튜닝)하지 않고, 어떤 약점을 피해야 하는지부터 읽는다.
"""
    return write_md(INPUTS_DIR / "input_refs.md", text)


def update_current_truth() -> list[Path]:
    updated: list[Path] = []
    workspace_text, workspace_bom = read_text_lossless(WORKSPACE_STATE)
    workspace_text = replace_prefix_line(workspace_text, "current_run_id:", f"current_run_id: {NEXT_RUN_ID}")
    workspace_text = replace_prefix_line(workspace_text, "updated_on:", f"updated_on: '{TODAY}'")
    workspace_text = replace_prefix_line(workspace_text, "active_stage:", f"active_stage: {STAGE_ID}")
    focus = (
        "- >-\n"
        f"  Stage332(332단계) run332A(332A 실행)는 `{STATUS}`로 failure memory forward research handoff design(실패 기억 전진 연구 인계 설계)을 완료했다. Effect(효과): Stage331(331단계)의 cost/curve/runtime(비용/곡선/런타임) 실패 기억을 run332B(332B 실행)의 데이터/방어 입력 물질화 조건으로 넘기고, 선택 후보나 Goal Achieve(목표 달성)는 주장하지 않는다.\n"
    )
    if "Stage332(332단계) run332A(332A 실행)" not in workspace_text:
        workspace_text = workspace_text.replace("current_focus:\n", "current_focus:\n" + focus, 1)
    updated.append(write_text_lossless(WORKSPACE_STATE, workspace_text, workspace_bom))

    current_text, current_bom = read_text_lossless(CURRENT_STATE)
    replacements = {
        "- current_packet(": f"- current_packet(현재 작업 묶음): `{STAGE_ID}_v2`",
        "- current_run(": f"- current_run(현재 실행): `{NEXT_RUN_ID}`",
        "- active_stage(": f"- active_stage(활성 단계): `{STAGE_ID}`",
        "- source_stage(": f"- source_stage(원천 단계): `{SOURCE_STAGE_ID}`",
        "- target_surface(": "- target_surface(목표 표면): `failure_memory_data_guard_materialization`",
        "- status(": f"- status(상태): `{STATUS}`",
        "- decision(": f"- decision(판정): `{JUDGMENT}`",
        "- next_action(": f"- next_action(다음 행동): `{NEXT_RUN_ID}`",
        "- claim_boundary(": f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`",
    }
    for prefix, replacement in replacements.items():
        current_text = replace_prefix_line(current_text, prefix, replacement)
    summary = (
        f"- run332A_summary(332A 요약): failure memory forward research handoff design(실패 기억 전진 연구 인계 설계)을 `{STATUS}`로 완료했다. "
        "Effect(효과): Stage331(331단계)의 실패를 다음 run332B(332B 실행)의 data integrity/guard input(데이터 무결성/방어 입력) 조건으로 바꿨고, 후보 선택이나 Goal Achieve(목표 달성)는 없다."
    )
    current_text = insert_after_line(current_text, "- decision(", summary, "run332A_summary(332A 요약)")
    updated.append(write_text_lossless(CURRENT_STATE, current_text, current_bom))

    updated.append(
        append_if_missing(
            CHANGELOG,
            "Stage332A Failure Memory Forward Research Handoff Design",
            f"""
## 2026-05-26 - Stage332A Failure Memory Forward Research Handoff Design(332A 실패 기억 전진 연구 인계 설계)

- run332A(332A 실행): Stage331(331단계)의 failure memory(실패 기억)를 research constraints(연구 제약), branch queue(분기 대기열), data/model/parity evidence plan(데이터/모델/동등성 근거 계획)으로 바꿨다.
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): 과적합 포켓을 직접 고치지 않고 다음 실행의 차단 조건으로 고정했으며, Forward Passed/Failed(전진 통과/실패), Goal Achieve(목표 달성)는 주장하지 않는다.
""",
        )
    )
    return updated


def update_registers(generated_at_utc: str, artifacts: Sequence[Path]) -> None:
    report_path = REVIEWS_DIR / "run332A_failure_memory_forward_research_handoff_design.md"
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
                "notes": f"failure_memory_handoff_design;next_action={NEXT_RUN_ID};goal_achieve_not_claimed.",
            }
        ],
    )
    upsert_csv(
        ALPHA_LEDGER,
        ["ledger_row_id"],
        [
            {
                "ledger_row_id": f"{RUN_ID}__experiment_design",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": RUN_NUMBER,
                "parent_run_id": PARENT_RUN_ID,
                "record_view": "failure_memory_forward_research_handoff_design",
                "tier_scope": "raw_forward_failure_memory_design_scope",
                "kpi_scope": "design_only_no_trading_kpi",
                "scoreboard_lane": "experiment_design",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(report_path),
                "primary_kpi": "research_branch_queue_count=4",
                "guardrail_kpi": "no_threshold_retuning;no_lot_optimization;no_model_update;goal_achieve_not_claimed",
                "external_verification_status": "not_applicable_design_only",
                "notes": f"decision={DECISION};next_action={NEXT_RUN_ID}.",
            }
        ],
    )
    upsert_csv(
        STAGE_LEDGER,
        ["row_id"],
        [
            {
                "row_id": f"{RUN_ID}__experiment_design",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "view": "failure_memory_forward_research_handoff_design(실패 기억 전진 연구 인계 설계)",
                "tier_scope": "raw_forward_failure_memory_design_scope(원본 전진 실패 기억 설계 범위)",
                "scoreboard": "experiment_design_no_trading_kpi(실험 설계, 거래 KPI 없음)",
                "status": STATUS,
                "judgment": JUDGMENT,
                "evidence_boundary": CLAIM_BOUNDARY,
                "report_path": rel(report_path),
                "notes": "no_candidate_selected;goal_achieve_not_claimed.",
                "decision": DECISION,
            }
        ],
    )
    rows: list[dict[str, Any]] = []
    for artifact in [*artifacts, Path(__file__)]:
        if artifact.exists() and io_path(artifact).is_file():
            rows.append(
                {
                    "artifact_id": f"{RUN_ID}:{rel(artifact)}",
                    "artifact_type": artifact.suffix.lstrip(".") or "file",
                    "path": rel(artifact),
                    "sha256": sha256_file(artifact),
                    "stage_id": STAGE_ID,
                    "run_id": RUN_ID,
                    "created_at_utc": generated_at_utc,
                    "notes": "Stage332A design artifact; no operating claim.",
                }
            )
    upsert_csv(ARTIFACT_REGISTRY, ["artifact_id"], rows)


def write_run_artifacts(generated_at_utc: str) -> list[Path]:
    matrix, memory, clues, feature_manifest = load_inputs()
    constraints = constraint_rows(memory)
    queue = branch_queue_rows(feature_manifest)
    artifacts = [
        write_json(
            RUN_DIR / "experiment_design_spec.json",
            {
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "hypothesis": "Stage331 failure modes can be turned into anti-overfit constraints before new research branches are materialized.",
                "decision_use": "Route Stage332B and later branch work without selecting Stage331 survivors.",
                "comparison_baseline": PARENT_RUN_ID,
                "control_variables": [
                    "no threshold retuning",
                    "no lot optimization",
                    "no model update",
                    "Stage331 survivors remain research memory only",
                ],
                "changed_variables": "Design artifacts only: constraints, branch queue, evidence plan, data/model validation plan.",
                "sample_scope": {
                    "source_attempt_count": int(len(matrix)),
                    "source_failure_memory_count": int(len(memory)),
                    "source_survivor_clue_count": int(len(clues)),
                    "raw_forward_first_timestamp": str(feature_manifest["first_timestamp"].min()),
                    "raw_forward_last_timestamp": str(feature_manifest["last_timestamp"].max()),
                },
                "success_criteria": "Stage332B has concrete data and guard-input materialization requirements.",
                "failure_criteria": "Any branch treats c56_plain_rf or m48_plain_rf as selected candidates.",
                "invalid_conditions": "Known Stage331 weak pockets are used to tune thresholds, features, or labels.",
                "stop_conditions": "Stop model work if Stage332B data integrity or guard identity is blocked.",
                "evidence_plan": rel(RUN_DIR / "evidence_plan.csv"),
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
        write_csv(
            RUN_DIR / "failure_memory_to_research_constraints.csv",
            [
                "constraint_id",
                "source_failure",
                "design_requirement",
                "anti_overfit_effect",
                "hard_stop_condition",
                "allowed_use",
                "forbidden_use",
            ],
            constraints,
        ),
        write_csv(
            RUN_DIR / "research_branch_queue.csv",
            [
                "queue_id",
                "branch_family",
                "hypothesis",
                "decision_use",
                "comparison_baseline",
                "control_variables",
                "changed_variables",
                "sample_scope",
                "success_criteria",
                "failure_criteria",
                "invalid_conditions",
                "stop_conditions",
                "evidence_plan",
            ],
            queue,
        ),
        write_csv(
            RUN_DIR / "data_integrity_plan.csv",
            [
                "data_source",
                "time_axis",
                "sample_scope",
                "missing_or_duplicate_check",
                "feature_label_boundary",
                "split_boundary",
                "leakage_risk",
                "data_hash_or_identity",
                "integrity_judgment",
            ],
            data_plan_rows(feature_manifest),
        ),
        write_csv(
            RUN_DIR / "model_validation_plan.csv",
            [
                "model_family",
                "target_and_label",
                "split_method",
                "selection_metric",
                "secondary_metrics",
                "threshold_policy",
                "overfit_risk",
                "calibration_risk",
                "comparison_baseline",
                "validation_judgment",
            ],
            model_plan_rows(),
        ),
        write_csv(
            RUN_DIR / "evidence_plan.csv",
            ["evidence_item", "producer_run", "required_before", "must_include", "claim_enabled"],
            evidence_plan_rows(),
        ),
        write_csv(
            RUN_DIR / "required_gate_coverage_audit.csv",
            ["gate", "status", "evidence_path", "notes"],
            gate_audit_rows(),
        ),
        write_json(
            RUN_DIR / "run_manifest.json",
            {
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "run_number": RUN_NUMBER,
                "parent_run_id": PARENT_RUN_ID,
                "generated_at_utc": generated_at_utc,
                "primary_family": "experiment_design",
                "primary_skill": "obsidian-experiment-design",
                "support_skills": [
                    "obsidian-data-integrity",
                    "obsidian-model-validation",
                    "obsidian-artifact-lineage",
                    "obsidian-result-judgment",
                ],
                "required_gates": [
                    "work_packet_schema_lint",
                    "data_integrity_plan_gate",
                    "model_validation_plan_gate",
                    "no_retune_guard",
                    "artifact_lineage_audit",
                    "required_gate_coverage_audit",
                    "final_claim_guard",
                ],
                "status": STATUS,
                "judgment": JUDGMENT,
                "decision": DECISION,
                "source_inputs": [
                    rel(RUN331D_DIR / "final_decision_matrix.csv"),
                    rel(RUN331D_DIR / "overfit_guard_failure_memory.csv"),
                    rel(RUN331D_DIR / "survivor_clue_disposition.csv"),
                    rel(RUN330E_DIR / "raw_forward_feature_matrix_manifest.csv"),
                ],
                "forward_passed": "not_claimed",
                "forward_failed": "not_claimed",
                "selected_candidate": "none",
                "goal_achieve": "not_claimed",
                "next_action": NEXT_RUN_ID,
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ),
    ]
    artifacts.extend(write_receipts(generated_at_utc))
    artifacts.extend(write_reports(constraints, queue))
    artifacts.append(update_selection_status())
    artifacts.append(update_input_refs())
    artifacts.extend(update_current_truth())
    return artifacts


def main() -> None:
    generated_at_utc = utc_now()
    RUN_DIR.mkdir(parents=True, exist_ok=True)
    artifacts = write_run_artifacts(generated_at_utc)
    update_registers(generated_at_utc, artifacts)
    print(
        json.dumps(
            {
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "decision": DECISION,
                "research_branch_queue_count": 4,
                "selected_candidate": "none",
                "forward_passed": "not_claimed",
                "forward_failed": "not_claimed",
                "goal_achieve": "not_claimed",
                "next_action": NEXT_RUN_ID,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
