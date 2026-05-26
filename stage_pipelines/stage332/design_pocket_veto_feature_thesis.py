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
RUN_NUMBER = "run332D"
RUN_ID = "run332D_design_pocket_veto_feature_thesis_v1"
PARENT_RUN_ID = "run332C_design_or_materialize_cost_curve_guarded_scout_v1"
NEXT_RUN_ID = "run332E_runtime_parity_probe_design_v1"
STATUS = "completed_pocket_veto_feature_thesis_design_no_selection"
JUDGMENT = "feature_thesis_design_research_only_no_goal_achieve"
DECISION = "stage331_pockets_pre_registered_as_veto_feature_thesis_queue_no_candidate_selection"
CLAIM_BOUNDARY = (
    "research_development_only_pocket_veto_feature_thesis_design_no_threshold_retuning_"
    "no_lot_optimization_no_model_update_no_candidate_selection_no_forward_passed_no_forward_failed_"
    "no_live_readiness_no_deployment_no_operating_promotion_no_runtime_authority_no_goal_achieve"
)
TODAY = "2026-05-26"

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = STAGE_DIR / "03_reviews"
INPUTS_DIR = STAGE_DIR / "01_inputs"
SELECTED_DIR = STAGE_DIR / "04_selected"
RUN332B_DIR = STAGE_DIR / "02_runs" / "run332B"
RUN332C_DIR = STAGE_DIR / "02_runs" / "run332C"
RUN331B_DIR = ROOT / "stages" / "331_overfit_guard__cross_horizon_cost_curve_parity_probe" / "02_runs" / "run331B"
RUN331D_DIR = ROOT / "stages" / "331_overfit_guard__cross_horizon_cost_curve_parity_probe" / "02_runs" / "run331D"
DECISION_DOC = ROOT / "docs" / "decisions" / "2026-05-26_stage332D_pocket_veto_feature_thesis.md"
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


def path_exists(path: Path) -> bool:
    return io_path(path).exists()


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


def append_if_missing(path: Path, marker: str, block: str) -> Path:
    text, had_bom = read_text_lossless(path)
    if marker not in text:
        text = text.rstrip() + "\n\n" + block.strip() + "\n"
        write_text_lossless(path, text, had_bom)
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


def read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(io_path(path))


def read_feature_columns(path: Path) -> list[str]:
    return list(pd.read_csv(io_path(path), nrows=1).columns)


def load_inputs() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    return (
        read_csv(RUN332C_DIR / "guarded_scout_queue.csv"),
        read_csv(RUN332C_DIR / "guarded_scout_matrix.csv"),
        read_csv(RUN332B_DIR / "guard_input_manifest.csv"),
        read_csv(RUN331D_DIR / "survivor_clue_disposition.csv"),
        read_csv(RUN331B_DIR / "resampling_stability_report.csv"),
    )


def feature_availability_rows(guard_inputs: pd.DataFrame) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    wanted = {
        "c56_plain": [
            "atr_14_over_atr_50",
            "historical_vol_5_over_20",
            "return_1_over_atr_14",
            "adx_14",
            "di_spread_14",
            "vix_zscore_20",
            "us10yr_zscore_20",
            "usdx_zscore_20",
            "us100_minus_mega8_equal_return_1",
            "timestamp_hour_derived",
        ],
        "m48_plain": [
            "atr_14_over_atr_50",
            "historical_vol_5_over_20",
            "adx_14",
            "di_spread_14",
            "vix_change_1",
            "vix_zscore_20",
            "us10yr_change_1",
            "us10yr_zscore_20",
            "usdx_change_1",
            "usdx_zscore_20",
            "timestamp_hour_derived",
        ],
    }
    for slug, feature_names in wanted.items():
        source = guard_inputs[guard_inputs["artifact_slug"].astype(str) == slug].iloc[0]
        path = ROOT / str(source["feature_matrix_path"])
        columns = set(read_feature_columns(path))
        for feature in feature_names:
            if feature == "timestamp_hour_derived":
                status = "derivable_from_timestamp_utc_without_future_data" if "timestamp_utc" in columns else "missing_timestamp_source"
                source_column = "timestamp_utc"
            else:
                status = "available_existing_forward_feature" if feature in columns else "not_in_source_feature_matrix"
                source_column = feature if feature in columns else ""
            rows.append(
                {
                    "source_artifact": slug,
                    "feature_name": feature,
                    "availability_status": status,
                    "source_column": source_column,
                    "feature_label_boundary": "uses_bar_t_or_older_no_future_return_no_tester_outcome",
                }
            )
    return rows


def thesis_rows() -> list[dict[str, Any]]:
    sample_scope = "train/WFO, validation, OOS, raw-forward; Tier A/Tier B/Tier A+B records required before selection language"
    controls = (
        "US100 M5; fixed feature-label time boundary; no threshold retuning; no lot optimization; "
        "same cost ladder 0/0.25/0.5/1/2/3/5; rolling20/rolling40 veto; no Stage331 date exclusion"
    )
    return [
        {
            "thesis_id": "pv_c56_volatility_cost_shape_sentry",
            "source_clue": "c56_plain_rf",
            "hypothesis": "c56 low-frequency edge fails when volatility expansion and trend/chop shape raise execution cost.",
            "decision_use": "Decide whether c56-style features deserve materialization as a cost-aware research branch.",
            "comparison_baseline": "run332C c56_plain_rf cost2_pf=0.976076 and rolling20_min_net=-34.86",
            "control_variables": controls,
            "changed_variables": "Predeclared volatility/trend-shape feature family only; no score threshold or lot change.",
            "sample_scope": sample_scope,
            "success_criteria": "cost2_pf>=1, rolling20_min_net>=0, no month/half concentration, trade_count not below declared density floor.",
            "failure_criteria": "Any gain is isolated to known Stage331 pocket or cost2_pf remains below 1.",
            "invalid_conditions": "Uses future return, realized tester outcome, or hard-coded pocket timestamps.",
            "stop_conditions": "Stop before ONNX export if cost2 or rolling pocket veto fails.",
            "evidence_plan": "feature_label_boundary_receipt.json; pocket_veto_plan.csv; cost_curve report; temporal balance report.",
            "feature_family": "volatility_cost_shape",
            "candidate_feature_sources": "atr_14_over_atr_50;historical_vol_5_over_20;return_1_over_atr_14;adx_14;di_spread_14",
            "anti_overfit_rule": "No date/pocket exclusion; feature must be computable before trade decision.",
        },
        {
            "thesis_id": "pv_c56_session_liquidity_veto",
            "source_clue": "c56_plain_rf",
            "hypothesis": "The c56 pocket may be a session/liquidity timing weakness rather than a pure model-score weakness.",
            "decision_use": "Test whether timestamp-derived session features reduce pocket risk without lowering density into noise.",
            "comparison_baseline": "run332C c56_plain_rf low_frequency_claim_warning and rolling20 pocket.",
            "control_variables": controls,
            "changed_variables": "Only timestamp-derived hour/session/weekday features may be added.",
            "sample_scope": sample_scope,
            "success_criteria": "Worst pocket improves across both known and unseen slices; cost2_pf>=1.",
            "failure_criteria": "Only the known May pocket improves or trade count collapses.",
            "invalid_conditions": "Session bin chosen after looking at profitable hours or pocket dates.",
            "stop_conditions": "Stop if session design cannot be predeclared independently of tester outcome.",
            "evidence_plan": "session feature derivation receipt; pocket_veto_plan.csv; density report.",
            "feature_family": "session_liquidity_timing",
            "candidate_feature_sources": "timestamp_utc->hour;timestamp_utc->weekday;timestamp_utc->broker_session_bucket",
            "anti_overfit_rule": "Session buckets must be calendar-derived, not fitted to PnL pockets.",
        },
        {
            "thesis_id": "pv_m48_macro_rate_volatility_guard",
            "source_clue": "m48_plain_rf",
            "hypothesis": "m48 macro breadth fails when VIX, USD, and US10YR shifts create a fragile April/first-half pocket.",
            "decision_use": "Decide whether macro regime interaction deserves materialization before runtime replay budget.",
            "comparison_baseline": "run332C m48_plain_rf cost1_pf=1.001302, cost2_pf=0.672597, rolling20_min_net=-62.79",
            "control_variables": controls,
            "changed_variables": "Only predeclared VIX/USD/US10YR interaction and volatility-shape features may change.",
            "sample_scope": sample_scope,
            "success_criteria": "cost1 no longer near break-even, cost2_pf>=1, rolling20/rolling40 pockets non-negative.",
            "failure_criteria": "May dominates the edge or April remains weak after cost stress.",
            "invalid_conditions": "Macro value is joined with future timestamp or revised after label time.",
            "stop_conditions": "Stop if macro timestamp alignment cannot be proven.",
            "evidence_plan": "macro timestamp integrity receipt; feature_label_boundary_receipt.json; temporal concentration report.",
            "feature_family": "macro_rate_volatility_interaction",
            "candidate_feature_sources": "vix_change_1;vix_zscore_20;us10yr_change_1;us10yr_zscore_20;usdx_change_1;usdx_zscore_20",
            "anti_overfit_rule": "No pocket date exclusion; macro joins must use prior/latest-known values only and never tester outcome.",
        },
        {
            "thesis_id": "pv_m48_breadth_reintroduction_control",
            "source_clue": "m48_plain_rf",
            "hypothesis": "m48 may need a limited breadth/divergence control to avoid macro-only concentration.",
            "decision_use": "Compare macro-only m48 against a bounded breadth reintroduction without resurrecting negative controls.",
            "comparison_baseline": "m48_plain_rf preserved clue plus balanced-family negative controls caught in run332C.",
            "control_variables": controls,
            "changed_variables": "Add only predeclared breadth/divergence source if timestamp-safe; keep model/threshold policy fixed.",
            "sample_scope": sample_scope,
            "success_criteria": "Breadth control improves pocket and cost guards without turning into high-pressure negative-control behavior.",
            "failure_criteria": "Looks like u42/m48 balanced family or only improves one known pocket.",
            "invalid_conditions": "Breadth feature uses future constituent returns or unversioned external data.",
            "stop_conditions": "Stop if breadth source identity or timestamp cannot be reproduced.",
            "evidence_plan": "feature availability audit; data integrity receipt; cost/curve/temporal guard reports.",
            "feature_family": "bounded_breadth_divergence_control",
            "candidate_feature_sources": "us100_minus_mega8_equal_return_1 or equivalent prior-bar breadth source",
            "anti_overfit_rule": "Breadth source must be declared before materialization and must not be tuned by pocket date.",
        },
    ]


def pocket_veto_rows(theses: Sequence[Mapping[str, Any]], scout_matrix: pd.DataFrame, resampling: pd.DataFrame) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for thesis in theses:
        source = str(thesis["source_clue"])
        scout = scout_matrix[scout_matrix["attempt_name"].astype(str) == source].iloc[0].to_dict()
        pocket = resampling[resampling["attempt_name"].astype(str) == source].iloc[0].to_dict()
        rows.append(
            {
                "thesis_id": thesis["thesis_id"],
                "source_clue": source,
                "source_cost2_pf": scout.get("cost2_pf"),
                "source_rolling20_min_net": scout.get("rolling20_min_net"),
                "source_rolling20_start": pocket.get("rolling_min_start"),
                "source_rolling20_end": pocket.get("rolling_min_end"),
                "required_cost_veto": "cost2_pf_ge_1_before_candidate_language",
                "required_curve_veto": "rolling20_min_net_ge_0_and_rolling40_min_net_ge_0_before_candidate_language",
                "required_temporal_veto": "first_half_second_half_months_thirds_fifths_reported_no_single_slice_dependency",
                "forbidden_repair": "no_hardcoded_pocket_dates_no_threshold_retune_no_lot_optimization_no_model_update_in_run332D",
                "status": "pre_registered_veto_plan",
            }
        )
    return rows


def materialization_queue_rows(theses: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for thesis in theses:
        rows.append(
            {
                "queue_id": f"{thesis['thesis_id']}__materialization_candidate",
                "thesis_id": thesis["thesis_id"],
                "source_clue": thesis["source_clue"],
                "materialization_status": "queued_after_runtime_parity_contract_design",
                "next_gate": NEXT_RUN_ID,
                "required_before_materialization": "feature owner path; label boundary receipt; source data identity; no-retune guard; cost/curve veto plan",
                "forbidden_action": "do_not_train_or_export_onnx_from_run332D_design",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return rows


def receipts(
    theses: Sequence[Mapping[str, Any]],
    availability: Sequence[Mapping[str, Any]],
    source_files: Sequence[Path],
) -> dict[str, Any]:
    unavailable = [row for row in availability if row["availability_status"] == "not_in_source_feature_matrix"]
    return {
        "experiment_design_receipt": {
            "hypothesis": "Feature theses can reduce pocket concentration only if they are predeclared and timestamp-safe.",
            "decision_use": "Choose research branches worthy of future materialization, not candidate selection.",
            "comparison_baseline": "run332C guarded scout and Stage331 failure memory.",
            "control_variables": "fixed cost ladder, no threshold retuning, no lot optimization, no Stage331 pocket exclusion.",
            "changed_variables": "future feature families only, not changed in run332D.",
            "sample_scope": "train/WFO, validation, OOS, raw-forward, Tier A/Tier B/Tier A+B required before selection language.",
            "success_criteria": "future branch passes cost2 and rolling pocket veto without temporal concentration.",
            "failure_criteria": "future branch only fixes known pocket or one month.",
            "invalid_conditions": "feature uses future returns, tester outcome, or hard-coded pocket dates.",
            "stop_conditions": "stop before materialization if label boundary or feature source is not reproducible.",
            "evidence_plan": "feature_thesis_registry.csv; feature_label_boundary_receipt.json; pocket_veto_plan.csv; feature_availability_audit.csv",
        },
        "feature_label_boundary_receipt": {
            "time_axis": "timestamp_utc is the feature decision timestamp; derived session/hour features use timestamp only.",
            "allowed_inputs": [
                "US100 M5 bar values at or before decision bar",
                "VIX/USD/US10YR latest-known values at or before decision timestamp",
                "prior-bar breadth/divergence values when source identity is reproducible",
            ],
            "forbidden_inputs": [
                "future returns",
                "realized tester PnL",
                "Stage331 pocket date labels as features",
                "post-forward threshold search",
                "lot optimization",
            ],
            "feature_label_boundary": "features must be computable before trade decision; labels/outcomes are evaluation-only.",
            "boundary_judgment": "usable_for_design_only_materialization_requires_source_identity_receipt",
        },
        "model_validation_receipt": {
            "model_family": "none trained in run332D; future feature-family theses only.",
            "target_and_label": "unchanged and not materialized in run332D.",
            "split_method": "predeclared train/WFO validation OOS raw-forward with Tier A/B paired records required later.",
            "selection_metric": "none; no candidate selection.",
            "secondary_metrics": "cost2_pf, rolling20/rolling40 min net, temporal balance, density, runtime parity.",
            "threshold_policy": "fixed/no retune; run332D does not search thresholds.",
            "overfit_risk": "designing directly from Stage331 pockets; mitigated by forbidding date exclusion and hardcoding.",
            "calibration_risk": "not applicable for design-only run.",
            "comparison_baseline": "run332C guarded scout.",
            "validation_judgment": JUDGMENT,
        },
        "artifact_lineage_receipt": {
            "source_inputs": [rel(path) for path in source_files],
            "producer": rel(Path(__file__)),
            "consumer": [NEXT_RUN_ID, rel(RUN_DIR / "feature_materialization_queue.csv")],
            "artifact_hashes": [{"path": rel(path), "sha256": sha256_file(path), "exists": path_exists(path)} for path in source_files],
            "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(ARTIFACT_REGISTRY), rel(STAGE_LEDGER)],
            "availability": "tracked_outputs_with_source_hashes",
            "lineage_judgment": "connected_with_boundary",
        },
        "no_retune_guard_receipt": {
            "threshold_retuning": "not_performed",
            "lot_optimization": "not_performed",
            "model_update": "not_performed",
            "onnx_export": "not_performed",
            "candidate_selection": "not_performed",
            "unavailable_feature_source_count": len(unavailable),
            "thesis_count": len(theses),
        },
        "result_judgment_receipt": {
            "result_subject": RUN_ID,
            "evidence_available": [
                "feature_thesis_registry.csv",
                "feature_availability_audit.csv",
                "feature_label_boundary_receipt.json",
                "pocket_veto_plan.csv",
                "feature_materialization_queue.csv",
            ],
            "evidence_missing": "no new feature matrix, no trained model, no MT5 result by design",
            "judgment_label": JUDGMENT,
            "claim_boundary": CLAIM_BOUNDARY,
            "next_condition": NEXT_RUN_ID,
        },
    }


def gate_rows(
    theses: Sequence[Mapping[str, Any]],
    availability: Sequence[Mapping[str, Any]],
    output_paths: Sequence[Path],
) -> list[dict[str, Any]]:
    source_ready = all(
        path_exists(path)
        for path in [
            RUN332C_DIR / "guarded_scout_queue.csv",
            RUN332C_DIR / "guarded_scout_matrix.csv",
            RUN332C_DIR / "guard_threshold_spec.json",
            RUN332B_DIR / "guard_input_manifest.csv",
        ]
    )
    hardcoding_guarded = all(
        "pocket" in (str(row.get("invalid_conditions", "")) + str(row.get("anti_overfit_rule", ""))).lower()
        or "date" in (str(row.get("invalid_conditions", "")) + str(row.get("anti_overfit_rule", ""))).lower()
        for row in theses
    )
    timestamp_safe = all(row["feature_label_boundary"] == "uses_bar_t_or_older_no_future_return_no_tester_outcome" for row in availability)
    return [
        {
            "gate": "source_guard_inputs_loaded",
            "status": "pass" if source_ready else "fail",
            "evidence": "run332B guard inputs and run332C guarded scout outputs exist.",
        },
        {
            "gate": "feature_thesis_registry_materialized",
            "status": "pass" if len(theses) == 4 else "fail",
            "evidence": "four predeclared theses written.",
        },
        {
            "gate": "feature_label_boundary_named",
            "status": "pass" if timestamp_safe else "fail",
            "evidence": "every audited feature source uses bar t or older boundary.",
        },
        {
            "gate": "pocket_hardcoding_veto",
            "status": "pass" if hardcoding_guarded else "fail",
            "evidence": "theses forbid hard-coded pocket timestamps.",
        },
        {
            "gate": "no_retune_guard",
            "status": "pass",
            "evidence": "No threshold, lot, model, ONNX, or runtime handoff change was made.",
        },
        {
            "gate": "final_claim_guard",
            "status": "pass" if "no_goal_achieve" in CLAIM_BOUNDARY else "fail",
            "evidence": "No Forward Passed/Failed, live readiness, deployment, operating promotion, runtime authority, or Goal Achieve claim.",
        },
        {
            "gate": "outputs_exist",
            "status": "pass" if all(path_exists(path) for path in output_paths) else "fail",
            "evidence": "Durable run332D CSV/JSON outputs exist.",
        },
    ]


def update_docs(theses: Sequence[Mapping[str, Any]], queue_rows: Sequence[Mapping[str, Any]]) -> None:
    review = f"""
# run332D Pocket Veto Feature Thesis(332D 포켓 거부 피처 논제)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- selected_candidate(선택 후보): `none`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`

## Thesis Read(논제 판독)

- feature_thesis_count(피처 논제 수): `{len(theses)}`
- materialization_queue_count(물질화 대기열 수): `{len(queue_rows)}`
- c56 direction(코어56 방향): volatility/session(변동성/세션)으로 cost+2 failure(비용+2 실패)와 low-frequency pocket(저빈도 포켓)을 사전 거부한다.
- m48 direction(매크로48 방향): VIX/USD/US10YR(빅스/달러/미국10년물) interaction(상호작용)과 breadth control(폭 제어)로 April/first-half concentration(4월/전반 집중)을 사전 거부한다.

Effect(효과): Stage331(331단계) pocket(포켓)을 피처로 외우지 않고, 다음 materialization(물질화) 전에 label boundary(라벨 경계)와 veto rule(거부 규칙)을 고정한다.

## Boundary(경계)

- no threshold retuning(임계값 재튜닝 없음)
- no lot optimization(로트 최적화 없음)
- no model update(모델 업데이트 없음)
- no ONNX export(ONNX 내보내기 없음)
- no candidate selection(후보 선택 없음)
- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`
"""
    write_md(REVIEWS_DIR / "run332D_pocket_veto_feature_thesis.md", review)

    decision = f"""
# Stage332D Pocket Veto Feature Thesis Decision(332D 포켓 거부 피처 논제 결정)

run332D(332D 실행)는 run332C(332C 실행)의 cost/curve guarded scout(비용/곡선 방어 탐침)를 받아 feature thesis registry(피처 논제 등록부), label boundary receipt(라벨 경계 영수증), pocket veto plan(포켓 거부 계획)을 만들었다.
Effect(효과): 다음 run332E(332E 실행)는 future branch(미래 분기)가 runtime probe(런타임 탐침)를 받을 수 있는 parity contract(동등성 계약)를 설계할 수 있다.

- status(상태): `{STATUS}`
- decision(판정): `{DECISION}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- goal_achieve(목표 달성): `not_claimed`
"""
    write_md(DECISION_DOC, decision)

    input_block = f"""
- run332D_feature_thesis_registry(332D 피처 논제 등록부): `{rel(RUN_DIR / "feature_thesis_registry.csv")}`
- run332D_feature_label_boundary(332D 피처 라벨 경계): `{rel(RUN_DIR / "feature_label_boundary_receipt.json")}`
- run332D_pocket_veto_plan(332D 포켓 거부 계획): `{rel(RUN_DIR / "pocket_veto_plan.csv")}`
- run332D_materialization_queue(332D 물질화 대기열): `{rel(RUN_DIR / "feature_materialization_queue.csv")}`
"""
    append_if_missing(INPUTS_DIR / "input_refs.md", "run332D_feature_thesis_registry", input_block)

    selection_path = SELECTED_DIR / "selection_status.md"
    selection_text, selection_bom = read_text_lossless(selection_path)
    selection_text = insert_after_line(
        selection_text,
        "- latest_cost_curve_guarded_scout",
        f"- latest_pocket_veto_feature_thesis(최신 포켓 거부 피처 논제): `{RUN_ID}`",
        "latest_pocket_veto_feature_thesis",
    )
    selection_text = replace_prefix_line(selection_text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{NEXT_RUN_ID}`")
    selection_text = replace_prefix_line(selection_text, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_RUN_ID}`")
    selection_text = replace_prefix_line(
        selection_text,
        "- effect(효과):",
        "- effect(효과): pocket veto feature thesis(포켓 거부 피처 논제)는 미래 피처 분기의 라벨 경계와 포켓 거부 조건을 고정했지만, 후보 선택이나 운영 주장은 없다.",
    )
    write_text_lossless(selection_path, selection_text, selection_bom)

    workspace_text, workspace_bom = read_text_lossless(WORKSPACE_STATE)
    workspace_text = replace_prefix_line(workspace_text, "current_run_id:", f"current_run_id: {NEXT_RUN_ID}")
    block = (
        "- >-\n"
        f"  Stage332(332단계) run332D(332D 실행)는 `{STATUS}`로 pocket veto feature thesis(포켓 거부 피처 논제)를 설계했다. "
        "Effect(효과): c56/m48 preserved clues(보존 단서)를 날짜 포켓 회피가 아니라 timestamp-safe feature thesis(타임스탬프 안전 피처 논제)와 "
        f"run332E(332E 실행)의 runtime parity contract(런타임 동등성 계약) 입력으로 넘기고 Goal Achieve(목표 달성)는 주장하지 않는다."
    )
    workspace_text = insert_after_line(workspace_text, "current_focus:", block, STATUS)
    write_text_lossless(WORKSPACE_STATE, workspace_text, workspace_bom)

    current_text, current_bom = read_text_lossless(CURRENT_STATE)
    current_text = replace_prefix_line(current_text, "- current_packet(현재 작업 묶음):", "- current_packet(현재 작업 묶음): `332_overfit_guard__failure_memory_forward_research_handoff_v5`")
    current_text = replace_prefix_line(current_text, "- current_run(현재 실행):", f"- current_run(현재 실행): `{NEXT_RUN_ID}`")
    current_text = replace_prefix_line(current_text, "- target_surface(목표 표면):", "- target_surface(목표 표면): `runtime_parity_probe_design_after_feature_thesis`")
    current_text = replace_prefix_line(current_text, "- status(상태):", f"- status(상태): `{STATUS}`")
    current_text = replace_prefix_line(current_text, "- decision(판정):", f"- decision(판정): `{DECISION}`")
    current_text = insert_after_line(
        current_text,
        "- decision(판정):",
        f"- run332D_summary(332D 요약): pocket veto feature thesis(포켓 거부 피처 논제)를 `{STATUS}`로 완료했다. Effect(효과): feature thesis(피처 논제) `4`개와 materialization queue(물질화 대기열) `4`개를 만들었지만 모델/임계값/로트/ONNX(모델/임계값/로트/온엑스)는 바꾸지 않았다.",
        "run332D_summary",
    )
    current_text = replace_prefix_line(current_text, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_RUN_ID}`")
    current_text = replace_prefix_line(current_text, "- claim_boundary(주장 경계):", f"- claim_boundary(주장 경계): `{CLAIM_BOUNDARY}`")
    write_text_lossless(CURRENT_STATE, current_text, current_bom)

    changelog_block = f"""
## {TODAY} - Stage332D pocket veto feature thesis(포켓 거부 피처 논제)

- run(실행): `{RUN_ID}`
- status(상태): `{STATUS}`
- effect(효과): Stage331/332C(331/332C단계)의 cost/curve failure memory(비용/곡선 실패 기억)를 feature thesis registry(피처 논제 등록부), label boundary receipt(라벨 경계 영수증), pocket veto plan(포켓 거부 계획), materialization queue(물질화 대기열)로 바꿨다.
- boundary(경계): Forward Passed/Failed(전진 통과/실패), live readiness(실거래 준비), deployment(배포), operating promotion(운영 승격), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 주장하지 않는다.
"""
    append_if_missing(CHANGELOG, "Stage332D pocket veto feature thesis", changelog_block)


def update_registers(output_paths: Sequence[Path]) -> None:
    review_path = REVIEWS_DIR / "run332D_pocket_veto_feature_thesis.md"
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
                "path": rel(review_path),
                "notes": f"pocket_veto_feature_thesis;next_action={NEXT_RUN_ID};goal_achieve_not_claimed.",
            }
        ],
    )
    upsert_csv(
        ALPHA_LEDGER,
        ["ledger_row_id"],
        [
            {
                "ledger_row_id": f"{RUN_ID}__feature_thesis_design",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": RUN_NUMBER,
                "parent_run_id": PARENT_RUN_ID,
                "record_view": "pocket_veto_feature_thesis_design",
                "tier_scope": "pre_materialization_design_requires_future_tier_a_b_pairs",
                "kpi_scope": "design_only_no_new_trading_kpi",
                "scoreboard_lane": "experiment_design",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(review_path),
                "primary_kpi": "feature_thesis_count=4;materialization_queue_count=4",
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
                "row_id": f"{RUN_ID}__feature_thesis_design",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "view": "pocket_veto_feature_thesis_design(포켓 거부 피처 논제 설계)",
                "tier_scope": "pre_materialization_design_requires_future_tier_a_b_pairs(미래 티어 A/B 쌍 필요)",
                "scoreboard": "design_only_no_new_trading_kpi(설계 전용, 새 거래 KPI 없음)",
                "status": STATUS,
                "judgment": JUDGMENT,
                "evidence_boundary": CLAIM_BOUNDARY,
                "report_path": rel(review_path),
                "notes": "no_candidate_selected;goal_achieve_not_claimed.",
                "decision": DECISION,
            }
        ],
    )
    artifact_rows = []
    for path in output_paths:
        artifact_rows.append(
            {
                "artifact_id": f"{RUN_ID}__{path.stem}",
                "artifact_type": path.suffix.lstrip(".") or "artifact",
                "path": rel(path),
                "sha256": sha256_file(path),
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": utc_now(),
                "notes": "run332D durable evidence; design-only research boundary.",
            }
        )
    upsert_csv(ARTIFACT_REGISTRY, ["artifact_id"], artifact_rows)


def main() -> int:
    guarded_queue, scout_matrix, guard_inputs, survivor_clues, resampling = load_inputs()
    theses = thesis_rows()
    availability = feature_availability_rows(guard_inputs)
    pocket_veto = pocket_veto_rows(theses, scout_matrix, resampling)
    materialization_queue = materialization_queue_rows(theses)

    source_files = [
        RUN332C_DIR / "guarded_scout_queue.csv",
        RUN332C_DIR / "guarded_scout_matrix.csv",
        RUN332C_DIR / "guard_threshold_spec.json",
        RUN332B_DIR / "guard_input_manifest.csv",
        RUN331D_DIR / "survivor_clue_disposition.csv",
        RUN331B_DIR / "resampling_stability_report.csv",
    ]

    output_paths = [
        write_csv(
            RUN_DIR / "feature_thesis_registry.csv",
            [
                "thesis_id",
                "source_clue",
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
                "feature_family",
                "candidate_feature_sources",
                "anti_overfit_rule",
            ],
            theses,
        ),
        write_csv(
            RUN_DIR / "feature_availability_audit.csv",
            ["source_artifact", "feature_name", "availability_status", "source_column", "feature_label_boundary"],
            availability,
        ),
        write_csv(
            RUN_DIR / "pocket_veto_plan.csv",
            [
                "thesis_id",
                "source_clue",
                "source_cost2_pf",
                "source_rolling20_min_net",
                "source_rolling20_start",
                "source_rolling20_end",
                "required_cost_veto",
                "required_curve_veto",
                "required_temporal_veto",
                "forbidden_repair",
                "status",
            ],
            pocket_veto,
        ),
        write_csv(
            RUN_DIR / "feature_materialization_queue.csv",
            [
                "queue_id",
                "thesis_id",
                "source_clue",
                "materialization_status",
                "next_gate",
                "required_before_materialization",
                "forbidden_action",
                "claim_boundary",
            ],
            materialization_queue,
        ),
    ]

    receipt_payloads = receipts(theses, availability, source_files)
    for name, payload in receipt_payloads.items():
        output_paths.append(write_json(RUN_DIR / f"{name}.json", payload))
    output_paths.append(write_json(RUN_DIR / "source_artifact_hashes.json", receipt_payloads["artifact_lineage_receipt"]["artifact_hashes"]))

    gate_audit = gate_rows(theses, availability, output_paths)
    output_paths.append(write_csv(RUN_DIR / "required_gate_coverage_audit.csv", ["gate", "status", "evidence"], gate_audit))

    run_manifest = {
        "stage_id": STAGE_ID,
        "run_number": RUN_NUMBER,
        "run_id": RUN_ID,
        "parent_run_id": PARENT_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "decision": DECISION,
        "claim_boundary": CLAIM_BOUNDARY,
        "selected_candidate": "none",
        "forward_passed": "not_claimed",
        "forward_failed": "not_claimed",
        "goal_achieve": "not_claimed",
        "source_files": [rel(path) for path in source_files],
        "outputs": [rel(path) for path in output_paths],
        "feature_thesis_count": len(theses),
        "materialization_queue_count": len(materialization_queue),
        "next_action": NEXT_RUN_ID,
        "created_at_utc": utc_now(),
    }
    output_paths.append(write_json(RUN_DIR / "run_manifest.json", run_manifest))

    update_docs(theses, materialization_queue)
    output_paths.extend([REVIEWS_DIR / "run332D_pocket_veto_feature_thesis.md", DECISION_DOC])
    update_registers(output_paths)

    failed_gates = [row for row in gate_audit if row["status"] != "pass"]
    print(
        json.dumps(
            {
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "decision": DECISION,
                "feature_thesis_count": len(theses),
                "materialization_queue_count": len(materialization_queue),
                "failed_gates": failed_gates,
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
    return 1 if failed_gates else 0


if __name__ == "__main__":
    raise SystemExit(main())
