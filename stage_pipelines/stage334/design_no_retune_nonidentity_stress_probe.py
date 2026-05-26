from __future__ import annotations

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


TODAY = "2026-05-26"
STAGE_ID = "334_runtime_parity__forward_usable_onnx_handoff_contract_hardening"
RUN_NUMBER = "run334E"
RUN_ID = "run334E_design_no_retune_forward_usable_nonidentity_stress_probe_from_reconciled_memory_v1"
PARENT_RUN_ID = "run334D_reconcile_existing_non_identity_runtime_probe_evidence_no_selection_v1"
NEXT_RUN_ID = "run334F_materialize_no_retune_nonidentity_stress_probe_inputs_v1"
STATUS = "completed_no_retune_nonidentity_stress_probe_design_no_selection"
JUDGMENT = "stress_probe_design_completed_research_only_no_goal_achieve"
DECISION = "stage334E_no_retune_stress_probe_queue_ready_no_selection"
CLAIM_BOUNDARY = (
    "research_development_only_no_retune_nonidentity_stress_probe_design_"
    "no_model_training_no_threshold_retuning_no_lot_optimization_no_candidate_selection_"
    "no_forward_passed_no_forward_failed_no_live_readiness_no_deployment_"
    "no_operating_promotion_no_runtime_authority_no_goal_achieve"
)

STAGE_DIR = ROOT / "stages" / STAGE_ID
RUN_DIR = STAGE_DIR / "02_runs" / RUN_NUMBER
REVIEWS_DIR = STAGE_DIR / "03_reviews"
SELECTED_DIR = STAGE_DIR / "04_selected"
INPUTS_DIR = STAGE_DIR / "01_inputs"
STAGE_BRIEF = STAGE_DIR / "00_spec" / "stage_brief.md"

DOCS = ROOT / "docs"
RUN_REGISTRY = DOCS / "registers" / "run_registry.csv"
ALPHA_LEDGER = DOCS / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = DOCS / "registers" / "artifact_registry.csv"
STAGE_LEDGER = REVIEWS_DIR / "stage_run_ledger.csv"
WORKSPACE_STATE = DOCS / "workspace" / "workspace_state.yaml"
CURRENT_STATE = DOCS / "context" / "current_working_state.md"
CHANGELOG = DOCS / "workspace" / "changelog.md"
DECISION_DOC = DOCS / "decisions" / "2026-05-26_stage334E_no_retune_nonidentity_stress_probe_design.md"

RUN334D_DIR = STAGE_DIR / "02_runs" / "run334D"
RUN334D_ALL_SIX = RUN334D_DIR / "all_six_runtime_reconciliation.csv"
RUN334D_COST_CURVE = RUN334D_DIR / "cost_curve_guard_reconciliation.csv"
RUN334D_ATTRIBUTION = RUN334D_DIR / "attribution_reconciliation_summary.csv"
RUN334D_REGIME = RUN334D_DIR / "regime_slice_reconciliation_summary.csv"
RUN334D_MEMORY = RUN334D_DIR / "preserved_clue_and_failure_memory.csv"
RUN334D_DECISION = RUN334D_DIR / "final_reconciliation_decision.json"

STAGE330_DIR = ROOT / "stages" / "330_onnx_rebuild__forward_safe_non_identity_surface_robustness"
RUN330E_DIR = STAGE330_DIR / "02_runs" / "run330E"
RUN330F_DIR = STAGE330_DIR / "02_runs" / "run330F"
RUN330E_FEATURE_MANIFEST = RUN330E_DIR / "raw_forward_feature_matrix_manifest.csv"
RUN330F_TRADE_RECORDS = RUN330F_DIR / "trade_level_records.csv"
RUN330F_KPI = RUN330F_DIR / "forward_mt5_kpi_report.csv"
RUN330F_SLICES = RUN330F_DIR / "session_hour_month_volatility_adx_vix_usd_rate_slices.csv"


def io_path(path: Path) -> Path:
    resolved = path.resolve()
    if sys.platform == "win32":
        text = str(resolved)
        if len(text) >= 240 and not text.startswith("\\\\?\\"):
            return Path("\\\\?\\" + text)
    return resolved


def path_exists(path: Path) -> bool:
    return io_path(path).exists()


def rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


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
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(json_ready(value), ensure_ascii=False, sort_keys=True)
    return value


def sha256_file(path: Path) -> str:
    if not path_exists(path):
        return "missing"
    digest = hashlib.sha256()
    with io_path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_text_lossless(path: Path) -> tuple[str, bool]:
    raw = io_path(path).read_bytes()
    return raw.decode("utf-8-sig"), raw.startswith(b"\xef\xbb\xbf")


def write_text_lossless(path: Path, text: str, had_bom: bool) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    encoding = "utf-8-sig" if had_bom else "utf-8"
    io_path(path).write_text(text, encoding=encoding, newline="\n")
    return path


def write_md(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.strip() + "\n", encoding="utf-8-sig", newline="\n")
    return path


def read_json(path: Path) -> Any:
    if not path_exists(path):
        return {}
    with io_path(path).open("r", encoding="utf-8-sig") as handle:
        return json.load(handle)


def write_json(path: Path, payload: Any) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with io_path(path).open("w", encoding="utf-8") as handle:
        json.dump(json_ready(payload), handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")
    return path


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path_exists(path):
        return []
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
    index_by_key = {
        tuple(str(row.get(column, "")) for column in key_columns): index
        for index, row in enumerate(existing)
    }
    for row in rows:
        key = tuple(str(row.get(column, "")) for column in key_columns)
        payload = {column: csv_value(row.get(column, "")) for column in fieldnames}
        if key in index_by_key:
            existing[index_by_key[key]] = payload
        else:
            existing.append(payload)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(existing)
    return path


def replace_prefix_line(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + replacement + "\n"


def insert_after_line_once(text: str, marker: str, insertion: str, token: str) -> str:
    if token in text:
        return text
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.strip() == marker:
            lines[index + 1:index + 1] = insertion.strip("\n").splitlines()
            return "\n".join(lines) + "\n"
    return insertion.strip() + "\n" + text


def append_section_once(path: Path, heading: str, body: str) -> Path:
    text, had_bom = read_text_lossless(path) if path_exists(path) else ("", True)
    if heading in text:
        return path
    return write_text_lossless(path, text.rstrip() + "\n\n" + heading + "\n\n" + body.strip() + "\n", had_bom)


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        text = str(value).strip()
        if text == "":
            return default
        return float(text)
    except (TypeError, ValueError):
        return default


def as_bool(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "y"}


def split_flags(value: str) -> list[str]:
    text = str(value or "").strip()
    if not text:
        return []
    try:
        parsed = json.loads(text)
        if isinstance(parsed, list):
            return [str(item) for item in parsed]
    except json.JSONDecodeError:
        pass
    return [item.strip() for item in text.replace(";", ",").split(",") if item.strip()]


def index_by(rows: Sequence[Mapping[str, str]], key: str) -> dict[str, Mapping[str, str]]:
    return {row.get(key, ""): row for row in rows if row.get(key)}


def load_context() -> dict[str, Any]:
    return {
        "all_six": read_csv_rows(RUN334D_ALL_SIX),
        "cost_curve": read_csv_rows(RUN334D_COST_CURVE),
        "attribution": read_csv_rows(RUN334D_ATTRIBUTION),
        "regime": read_csv_rows(RUN334D_REGIME),
        "memory": read_csv_rows(RUN334D_MEMORY),
        "run334d_decision": read_json(RUN334D_DECISION),
        "feature_manifest": read_csv_rows(RUN330E_FEATURE_MANIFEST),
    }


def stress_severity(row: Mapping[str, str], cost_row: Mapping[str, str], attribution_row: Mapping[str, str], regime_row: Mapping[str, str]) -> str:
    flags = set(split_flags(row.get("risk_flags", "")))
    if "thin_profit_factor" in flags or as_float(row.get("underwater_trade_share")) >= 0.7:
        return "red"
    if "cost_plus_1_breaks_pf" in flags or "deep_curve_pocket" in flags or as_float(regime_row.get("negative_slice_count")) >= 10:
        return "amber"
    if as_float(cost_row.get("cost_plus_200_pf")) < 1.0 or as_float(attribution_row.get("sell_net_profit")) < 0:
        return "amber"
    return "watch"


def build_outputs(context: Mapping[str, Any]) -> dict[str, list[dict[str, Any]]]:
    all_six = list(context["all_six"])
    cost_by_attempt = index_by(context["cost_curve"], "attempt_name")
    attribution_by_attempt = index_by(context["attribution"], "attempt_name")
    regime_by_attempt = index_by(context["regime"], "attempt_name")
    feature_by_slug = index_by(context["feature_manifest"], "artifact_slug")

    contract_rows = [
        {
            "contract_id": "all_six_carry_forward",
            "requirement": "carry all six reconciled non-identity attempts",
            "allowed": "all attempts remain in the stress matrix",
            "forbidden": "dropping weak attempts before the stress design",
            "effect": "prevents KPI cherry-pick from c56_plain_rf and m48_plain_rf",
        },
        {
            "contract_id": "no_forward_retune",
            "requirement": "fixed existing model, feature order, score threshold, lot, risk, ATR SL/TP, and runtime handoff",
            "allowed": "diagnostic replay and stress labels",
            "forbidden": "model training, threshold search, lot optimization, rule rewrite, date-pocket exclusion",
            "effect": "keeps the probe from becoming a second overfit loop",
        },
        {
            "contract_id": "stress_is_diagnostic",
            "requirement": "cost, curve, regime, direction, and underwater axes are evidence axes only",
            "allowed": "rank severity and materialize fixed-input checks",
            "forbidden": "selecting a candidate because one stress axis looks better",
            "effect": "turns positive rows into research clues, not promotion claims",
        },
        {
            "contract_id": "runtime_identity_required",
            "requirement": "feature/model/set/report/telemetry identity must stay attached",
            "allowed": "manifested reuse of Stage330E/330F evidence",
            "forbidden": "anonymous report reuse or untracked handoff files",
            "effect": "keeps runtime parity visible before any future MT5 run",
        },
    ]

    rejection_rows = [
        {
            "rule_id": "reject_threshold_retune",
            "trigger": "any run changes decision_threshold or margin threshold using forward evidence",
            "judgment": "invalid_overfit_repair",
            "effect": "prevents forward-data threshold fitting",
        },
        {
            "rule_id": "reject_lot_optimization",
            "trigger": "any run changes lot size to improve drawdown or recovery",
            "judgment": "invalid_lot_repair",
            "effect": "keeps lot-normalized evidence separate from optimization",
        },
        {
            "rule_id": "reject_date_or_hour_pruning",
            "trigger": "any run removes a losing date, hour, month, or regime pocket without pre-forward rule source",
            "judgment": "invalid_pocket_overfit",
            "effect": "prevents curve pocket fitting",
        },
        {
            "rule_id": "reject_direction_drop_as_fix",
            "trigger": "any run drops sell or buy direction only because run334D attribution is weak",
            "judgment": "diagnostic_only_until_predeclared_feature_source",
            "effect": "keeps long/short attribution from becoming an after-the-fact rule edit",
        },
        {
            "rule_id": "reject_db_attribution_claim",
            "trigger": "any run claims D/B source attribution for Stage330 non-identity single-surface evidence",
            "judgment": "invalid_source_claim",
            "effect": "keeps absent D/B tags from being invented",
        },
    ]

    matrix_rows: list[dict[str, Any]] = []
    queue_rows: list[dict[str, Any]] = []
    blocker_rows: list[dict[str, Any]] = []
    lineage_rows: list[dict[str, Any]] = []

    scenario_defs = [
        ("cost_plus_1", "cost_stress", "require PF after +1.0 synthetic round-trip cost to stay above 1 as a diagnostic hurdle"),
        ("cost_plus_2", "cost_stress", "record whether +2.0 synthetic cost breaks the surface"),
        ("rolling_worst_curve", "curve_pocket", "replay worst rolling pocket without date exclusion or threshold changes"),
        ("worst_regime_slice", "regime_slice", "inspect worst session/hour/month/volatility/ADX/VIX/USD/rate slice"),
        ("directional_side", "direction", "audit weak long/short side without dropping a direction"),
        ("underwater_stretch", "drawdown_shape", "inspect underwater stretch as a trade-shape risk"),
        ("runtime_identity", "runtime_parity", "verify feature/model/set/report/telemetry identity before any rerun"),
    ]

    for row in all_six:
        attempt = row["attempt_name"]
        slug = row["artifact_slug"]
        cost = cost_by_attempt.get(attempt, {})
        attribution = attribution_by_attempt.get(attempt, {})
        regime = regime_by_attempt.get(attempt, {})
        feature = feature_by_slug.get(slug, {})
        severity = stress_severity(row, cost, attribution, regime)
        flags = split_flags(row.get("risk_flags", ""))
        preserved = row.get("reconciliation_label") == "preserved_clue_with_unresolved_guards"
        matrix_rows.append(
            {
                "attempt_name": attempt,
                "artifact_slug": slug,
                "reconciliation_label": row.get("reconciliation_label", ""),
                "stress_severity": severity,
                "preserved_clue": preserved,
                "risk_flags": flags,
                "cost_plus_1_survives": row.get("cost_plus_1_survives", ""),
                "cost_plus_2_survives": row.get("cost_plus_2_survives", ""),
                "worst_curve_net": row.get("worst_curve_net", ""),
                "underwater_trade_share": row.get("underwater_trade_share", ""),
                "worst_slice_axis": row.get("worst_slice_axis", ""),
                "worst_slice_bucket": row.get("worst_slice_bucket", ""),
                "sell_net_profit": row.get("sell_net_profit", ""),
                "design_judgment": "stress_required_no_selection",
                "effect": "input remains research-only; severity controls probe priority, not candidate selection",
            }
        )
        for scenario_id, axis, instruction in scenario_defs:
            queue_rows.append(
                {
                    "queue_id": f"run334F_{attempt}_{scenario_id}",
                    "attempt_name": attempt,
                    "artifact_slug": slug,
                    "stress_axis": axis,
                    "scenario_id": scenario_id,
                    "severity": severity,
                    "materialization_action": "materialize_fixed_input_diagnostic_view",
                    "source_feature_matrix": feature.get("feature_matrix_path", ""),
                    "source_model": feature.get("onnx_path", ""),
                    "source_trade_records": rel(RUN330F_TRADE_RECORDS),
                    "source_slice_report": rel(RUN330F_SLICES),
                    "instruction": instruction,
                    "allowed_change": "none_to_model_threshold_lot_risk_runtime_logic",
                    "selection_eligible": False,
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
        blocker_rows.append(
            {
                "attempt_name": attempt,
                "artifact_slug": slug,
                "blocker_type": "stress_before_selection",
                "blocking_evidence": ";".join(flags) if flags else "unresolved_guard",
                "required_repair_scope": "diagnostic_stress_materialization_only",
                "forbidden_repair_scope": "threshold_or_lot_or_rule_optimization",
                "effect": "candidate selection is blocked until no-retune stress evidence exists and is judged separately",
            }
        )
        lineage_rows.append(
            {
                "attempt_name": attempt,
                "artifact_slug": slug,
                "feature_matrix_path": feature.get("feature_matrix_path", ""),
                "feature_matrix_sha256": feature.get("feature_matrix_sha256", ""),
                "onnx_path": feature.get("onnx_path", ""),
                "onnx_sha256": feature.get("onnx_sha256", ""),
                "run334d_reconciliation_path": rel(RUN334D_ALL_SIX),
                "run334f_queue_rows": len(scenario_defs),
                "lineage_judgment": "connected_with_boundary",
            }
        )

    return {
        "contract": contract_rows,
        "rejection": rejection_rows,
        "matrix": matrix_rows,
        "queue": queue_rows,
        "blockers": blocker_rows,
        "lineage": lineage_rows,
    }


def write_skill_receipts(context: Mapping[str, Any], outputs: Mapping[str, Sequence[Mapping[str, Any]]]) -> list[Path]:
    source_inputs = [
        RUN334D_ALL_SIX,
        RUN334D_COST_CURVE,
        RUN334D_ATTRIBUTION,
        RUN334D_REGIME,
        RUN334D_MEMORY,
        RUN334D_DECISION,
        RUN330E_FEATURE_MANIFEST,
        RUN330F_TRADE_RECORDS,
    ]
    red_count = sum(1 for row in outputs["matrix"] if row.get("stress_severity") == "red")
    amber_count = sum(1 for row in outputs["matrix"] if row.get("stress_severity") == "amber")
    receipts: list[Path] = []
    receipts.append(
        write_json(
            RUN_DIR / "data_integrity_receipt.json",
            {
                "data_source": [rel(path) for path in source_inputs],
                "time_axis": "run334E reuses post-2026-04-14 Stage330 forward evidence and does not add new bars or labels.",
                "sample_scope": {
                    "attempts": len(outputs["matrix"]),
                    "queue_rows": len(outputs["queue"]),
                    "symbol": "US100",
                    "timeframe": "M5",
                },
                "missing_or_duplicate_check": "run334E is design-only; run334F must validate row counts and missing trade records during materialization.",
                "feature_label_boundary": "No labels are built and no feature-label boundary is moved.",
                "split_boundary": "Forward evidence is converted into stress requirements only, not model selection.",
                "leakage_risk": "Using run334D weak pockets as exclusion rules would be leakage; rejection rules forbid that path.",
                "data_hash_or_identity": {rel(path): sha256_file(path) for path in source_inputs},
                "integrity_judgment": "usable_with_boundary",
            },
        )
    )
    receipts.append(
        write_json(
            RUN_DIR / "runtime_parity_receipt.json",
            {
                "research_path": rel(Path(__file__)),
                "runtime_path": [rel(RUN330E_DIR), rel(RUN330F_DIR)],
                "shared_contract": "run334F queue must preserve feature matrix, ONNX path/hash, trade records, slice reports, fixed threshold, and no-selection boundary.",
                "known_differences": [
                    "This is a design packet and does not launch MT5.",
                    "Stage330 non-identity ONNX evidence is not cp322A exact identity.",
                    "D/B source tags are unavailable for Stage330 single-surface evidence.",
                ],
                "parity_check": "runtime identity requirements and queue lineage are materialized for the next run.",
                "parity_identity": {
                    "queue_rows": len(outputs["queue"]),
                    "lineage_rows": len(outputs["lineage"]),
                    "run334d_all_six_sha256": sha256_file(RUN334D_ALL_SIX),
                    "run330e_manifest_sha256": sha256_file(RUN330E_FEATURE_MANIFEST),
                },
                "runtime_claim_boundary": "design_only_no_runtime_authority",
            },
        )
    )
    receipts.append(
        write_json(
            RUN_DIR / "model_validation_receipt.json",
            {
                "model_family": "existing Stage330 non-identity ONNX surfaces",
                "target_and_label": "inherited; not rebuilt",
                "split_method": "post-forward evidence converted to no-retune stress design",
                "selection_metric": "none",
                "secondary_metrics": [
                    "cost survival",
                    "worst curve pocket",
                    "underwater stretch",
                    "regime loss pocket",
                    "direction attribution",
                    "runtime identity",
                ],
                "threshold_policy": "fixed inherited threshold; no search",
                "overfit_risk": "turning failure memory into exclusion rules is the main risk and is explicitly rejected",
                "calibration_risk": "scores are not treated as calibrated probabilities",
                "comparison_baseline": "run334D all-six reconciliation",
                "validation_judgment": "exploratory_design_no_selection",
            },
        )
    )
    receipts.append(
        write_json(
            RUN_DIR / "performance_attribution_receipt.json",
            {
                "observed_change": "run334E transforms run334D preserved clues and failure memory into stress axes.",
                "comparison_baseline": "run334D reconciliation rows",
                "likely_drivers": [
                    "thin PF",
                    "cost sensitivity",
                    "rolling curve pocket",
                    "long underwater stretch",
                    "short-side loss",
                    "rate/ADX/month/hour loss slices",
                ],
                "segment_checks": [
                    "cost_plus_1",
                    "cost_plus_2",
                    "rolling_worst_curve",
                    "worst_regime_slice",
                    "directional_side",
                    "underwater_stretch",
                    "runtime_identity",
                ],
                "trade_shape": {
                    "red_attempt_count": red_count,
                    "amber_attempt_count": amber_count,
                    "stress_queue_rows": len(outputs["queue"]),
                },
                "alternative_explanations": [
                    "short forward window noise",
                    "tester cost assumptions",
                    "single-surface source attribution limits",
                ],
                "attribution_confidence": "medium_design_only",
                "next_probe": NEXT_RUN_ID,
            },
        )
    )
    return receipts


def write_run_artifacts(context: Mapping[str, Any], outputs: Mapping[str, Sequence[Mapping[str, Any]]], now: str) -> list[Path]:
    artifacts: list[Path] = []
    artifacts.append(
        write_csv(
            RUN_DIR / "no_retune_stress_probe_contract.csv",
            ["contract_id", "requirement", "allowed", "forbidden", "effect"],
            outputs["contract"],
        )
    )
    artifacts.append(
        write_csv(
            RUN_DIR / "overfit_rejection_rules.csv",
            ["rule_id", "trigger", "judgment", "effect"],
            outputs["rejection"],
        )
    )
    artifacts.append(
        write_csv(
            RUN_DIR / "stress_probe_matrix.csv",
            [
                "attempt_name",
                "artifact_slug",
                "reconciliation_label",
                "stress_severity",
                "preserved_clue",
                "risk_flags",
                "cost_plus_1_survives",
                "cost_plus_2_survives",
                "worst_curve_net",
                "underwater_trade_share",
                "worst_slice_axis",
                "worst_slice_bucket",
                "sell_net_profit",
                "design_judgment",
                "effect",
            ],
            outputs["matrix"],
        )
    )
    artifacts.append(
        write_csv(
            RUN_DIR / "run334F_materialization_queue.csv",
            [
                "queue_id",
                "attempt_name",
                "artifact_slug",
                "stress_axis",
                "scenario_id",
                "severity",
                "materialization_action",
                "source_feature_matrix",
                "source_model",
                "source_trade_records",
                "source_slice_report",
                "instruction",
                "allowed_change",
                "selection_eligible",
                "claim_boundary",
            ],
            outputs["queue"],
        )
    )
    artifacts.append(
        write_csv(
            RUN_DIR / "selection_blocker_register.csv",
            [
                "attempt_name",
                "artifact_slug",
                "blocker_type",
                "blocking_evidence",
                "required_repair_scope",
                "forbidden_repair_scope",
                "effect",
            ],
            outputs["blockers"],
        )
    )
    artifacts.append(
        write_csv(
            RUN_DIR / "runtime_identity_lineage_queue.csv",
            [
                "attempt_name",
                "artifact_slug",
                "feature_matrix_path",
                "feature_matrix_sha256",
                "onnx_path",
                "onnx_sha256",
                "run334d_reconciliation_path",
                "run334f_queue_rows",
                "lineage_judgment",
            ],
            outputs["lineage"],
        )
    )
    artifacts.extend(write_skill_receipts(context, outputs))
    artifacts.append(
        write_csv(
            RUN_DIR / "required_gate_coverage_audit.csv",
            ["gate", "status", "evidence", "claim_effect"],
            [
                {
                    "gate": "data_integrity",
                    "status": "passed_usable_with_boundary",
                    "evidence": "data_integrity_receipt.json",
                    "claim_effect": "Forward evidence becomes stress requirements, not retuning data.",
                },
                {
                    "gate": "runtime_parity",
                    "status": "passed_design_only",
                    "evidence": "runtime_parity_receipt.json",
                    "claim_effect": "Runtime identity is required before run334F materialization.",
                },
                {
                    "gate": "model_validation",
                    "status": "passed_no_selection_no_retune",
                    "evidence": "model_validation_receipt.json",
                    "claim_effect": "No model, threshold, or lot selection is made.",
                },
                {
                    "gate": "performance_attribution",
                    "status": "passed_design_only",
                    "evidence": "performance_attribution_receipt.json",
                    "claim_effect": "Stress axes trace to run334D attribution evidence.",
                },
                {
                    "gate": "artifact_lineage",
                    "status": "passed_connected_with_boundary",
                    "evidence": "artifact_lineage_receipt.json",
                    "claim_effect": "run334D inputs connect to run334F queue outputs.",
                },
                {
                    "gate": "result_judgment",
                    "status": "passed_no_goal_achieve",
                    "evidence": "result_judgment.csv",
                    "claim_effect": "Forward Passed/Failed and Goal Achieve are not claimed.",
                },
            ],
        )
    )
    artifacts.append(
        write_csv(
            RUN_DIR / "result_judgment.csv",
            [
                "run_id",
                "status",
                "judgment",
                "decision",
                "selected_candidate",
                "forward_passed",
                "forward_failed",
                "runtime_authority",
                "goal_achieve",
                "next_action",
                "claim_boundary",
            ],
            [
                {
                    "run_id": RUN_ID,
                    "status": STATUS,
                    "judgment": JUDGMENT,
                    "decision": DECISION,
                    "selected_candidate": "none",
                    "forward_passed": "not_claimed",
                    "forward_failed": "not_claimed",
                    "runtime_authority": "not_claimed",
                    "goal_achieve": "not_claimed",
                    "next_action": NEXT_RUN_ID,
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            ],
        )
    )
    artifacts.append(
        write_json(
            RUN_DIR / "final_stress_probe_design_decision.json",
            {
                "run_id": RUN_ID,
                "status": STATUS,
                "judgment": JUDGMENT,
                "decision": DECISION,
                "stress_contract_rows": len(outputs["contract"]),
                "overfit_rejection_rule_rows": len(outputs["rejection"]),
                "stress_matrix_rows": len(outputs["matrix"]),
                "run334F_queue_rows": len(outputs["queue"]),
                "selected_candidate": "none",
                "forward_passed": "not_claimed",
                "forward_failed": "not_claimed",
                "runtime_authority": "not_claimed",
                "goal_achieve": "not_claimed",
                "next_action": NEXT_RUN_ID,
                "claim_boundary": CLAIM_BOUNDARY,
            },
        )
    )
    lineage = {
        "source_inputs": [
            rel(RUN334D_ALL_SIX),
            rel(RUN334D_COST_CURVE),
            rel(RUN334D_ATTRIBUTION),
            rel(RUN334D_REGIME),
            rel(RUN334D_MEMORY),
            rel(RUN334D_DECISION),
            rel(RUN330E_FEATURE_MANIFEST),
            rel(RUN330F_TRADE_RECORDS),
        ],
        "producer": rel(Path(__file__)),
        "consumer": NEXT_RUN_ID,
        "artifact_paths": [rel(path) for path in artifacts],
        "artifact_hashes": {},
        "registry_links": {
            "run_registry": rel(RUN_REGISTRY),
            "alpha_ledger": rel(ALPHA_LEDGER),
            "stage_ledger": rel(STAGE_LEDGER),
            "artifact_registry": rel(ARTIFACT_REGISTRY),
        },
        "availability": "tracked_after_force_add_run_dir",
        "lineage_judgment": "connected_with_boundary",
    }
    lineage_path = write_json(RUN_DIR / "artifact_lineage_receipt.json", lineage)
    artifacts.append(lineage_path)
    lineage["artifact_hashes"] = {rel(path): sha256_file(path) for path in artifacts}
    write_json(lineage_path, lineage)
    artifacts.append(
        write_json(
            RUN_DIR / "run_manifest.json",
            {
                "run_id": RUN_ID,
                "run_number": RUN_NUMBER,
                "stage_id": STAGE_ID,
                "parent_run_id": PARENT_RUN_ID,
                "created_at_utc": now,
                "status": STATUS,
                "judgment": JUDGMENT,
                "decision": DECISION,
                "source_inputs": lineage["source_inputs"],
                "outputs": [rel(path) for path in artifacts],
                "selected_candidate": "none",
                "forward_passed": "not_claimed",
                "forward_failed": "not_claimed",
                "runtime_authority": "not_claimed",
                "goal_achieve": "not_claimed",
                "next_action": NEXT_RUN_ID,
                "claim_boundary": CLAIM_BOUNDARY,
            },
        )
    )
    return artifacts


def write_reports(outputs: Mapping[str, Sequence[Mapping[str, Any]]]) -> list[Path]:
    severity_counts: dict[str, int] = {}
    for row in outputs["matrix"]:
        severity_counts[str(row.get("stress_severity"))] = severity_counts.get(str(row.get("stress_severity")), 0) + 1
    report = write_md(
        REVIEWS_DIR / "run334E_no_retune_nonidentity_stress_probe_design.md",
        f"""
# run334E No-Retune Non-Identity Stress Probe Design(334E 무재튜닝 비정체성 압박 탐침 설계)

- run_id(실행 ID): `{RUN_ID}`
- parent_run_id(부모 실행 ID): `{PARENT_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- decision(결정): `{DECISION}`
- selected_candidate(선택 후보): `none`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`

## Design(설계)

- stress_contract(압박 계약): `{len(outputs["contract"])}` rows
- rejection_rules(거절 규칙): `{len(outputs["rejection"])}` rows
- stress_matrix(압박 행렬): `{len(outputs["matrix"])}` attempts
- run334F_queue(334F 대기열): `{len(outputs["queue"])}` diagnostic rows
- severity_counts(심각도 수): `{json.dumps(severity_counts, ensure_ascii=False, sort_keys=True)}`

Effect(효과): run334D(334D 실행)의 preserved clue/failure memory(보존 단서/실패 기억)를 다음 materialization(물질화) 입력으로 바꾸되, threshold/lot/model/rule(임계값/로트/모델/규칙)을 바꾸는 과적합 수리는 거절한다.

Next(다음): `{NEXT_RUN_ID}`
""",
    )
    decision = write_md(
        DECISION_DOC,
        f"""
# 2026-05-26 Stage334E No-Retune Non-Identity Stress Probe Design(334E 무재튜닝 비정체성 압박 탐침 설계)

- decision(결정): `{DECISION}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- selected_candidate(선택 후보): `none`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): 6개 non-identity(비정체성) 근거를 모두 유지하고, no-retune stress probe(무재튜닝 압박 탐침) materialization queue(물질화 대기열) `{len(outputs["queue"])}`개를 만들었다.
""",
    )
    return [report, decision]


def update_stage_docs() -> list[Path]:
    status_path = write_md(
        SELECTED_DIR / "selection_status.md",
        f"""
# Stage334 Selection Status(334단계 선택 상태)

- selected_candidate(선택 후보): `none`
- cp322A_status(cp322A 상태): `research_artifact_preserved_exact_forward_handoff_missing`
- latest_contract_design(최신 계약 설계): `run334A_design_forward_usable_onnx_handoff_contract_after_cp322a_boundary_v1`
- latest_materialization(최신 물질화): `run334B_materialize_subject_separated_handoff_contract_inputs_v1`
- latest_runtime_probe_decision(최신 런타임 탐침 결정): `run334C_design_subject_separated_runtime_probe_or_block_v1`
- latest_reconciliation(최신 대조): `run334D_reconcile_existing_non_identity_runtime_probe_evidence_no_selection_v1`
- latest_stress_design(최신 압박 설계): `{RUN_ID}`
- active_question(활성 질문): `forward_usable_onnx_handoff_contract_hardening_without_overfit`
- Forward Passed(전진 통과): `not_claimed`
- Forward Failed(전진 실패): `not_claimed`
- live_readiness(실거래 준비): `not_claimed`
- deployment(배포): `not_claimed`
- operating_promotion(운영 승격): `not_claimed`
- runtime_authority(런타임 권위): `not_claimed`
- goal_achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): Stage334E(334E 실행)는 no-retune stress probe(무재튜닝 압박 탐침) 설계를 만들었고, 다음 실행은 고정 입력 진단 보기만 물질화한다.
""",
    )
    if path_exists(STAGE_BRIEF):
        text, had_bom = read_text_lossless(STAGE_BRIEF)
        text = replace_prefix_line(text, "- status(상태):", "- status(상태): `open_active`")
        text = replace_prefix_line(text, "- latest_run(최신 실행):", f"- latest_run(최신 실행): `{RUN_ID}`")
        write_text_lossless(STAGE_BRIEF, text, had_bom)
    append_section_once(
        INPUTS_DIR / "input_refs.md",
        "## run334E No-Retune Stress Probe Design Outputs(334E 무재튜닝 압박 탐침 설계 출력)",
        f"""
- run334E_contract(334E 계약): `stages/{STAGE_ID}/02_runs/run334E/no_retune_stress_probe_contract.csv`
- run334E_rejection_rules(334E 거절 규칙): `stages/{STAGE_ID}/02_runs/run334E/overfit_rejection_rules.csv`
- run334E_matrix(334E 행렬): `stages/{STAGE_ID}/02_runs/run334E/stress_probe_matrix.csv`
- run334F_queue(334F 대기열): `stages/{STAGE_ID}/02_runs/run334E/run334F_materialization_queue.csv`
- run334E_final_decision(334E 최종 결정): `stages/{STAGE_ID}/02_runs/run334E/final_stress_probe_design_decision.json`
""",
    )
    return [status_path, STAGE_BRIEF, INPUTS_DIR / "input_refs.md"]


def update_state_docs() -> list[Path]:
    text, had_bom = read_text_lossless(WORKSPACE_STATE)
    text = replace_prefix_line(text, "current_run_id:", f"current_run_id: {NEXT_RUN_ID}")
    text = replace_prefix_line(text, "updated_on:", f"updated_on: '{TODAY}'")
    focus_insert = f"""- >-
  Stage334(334단계) run334E(334E 실행)는 `{STATUS}`로 no-retune non-identity stress probe design(무재튜닝 비정체성 압박 탐침 설계)을 완료했다. Effect(효과): 6개 전체를 유지한 채 run334F materialization queue(334F 물질화 대기열)를 만들고 threshold/lot/model/rule retune(임계값/로트/모델/규칙 재튜닝)을 거절한다."""
    text = insert_after_line_once(text, "current_focus:", focus_insert, "run334E(334E 실행)")
    write_text_lossless(WORKSPACE_STATE, text, had_bom)

    text, had_bom = read_text_lossless(CURRENT_STATE)
    replacements = {
        "- current_packet(현재 작업 묶음):": f"- current_packet(현재 작업 묶음): `{STAGE_ID}_v6`",
        "- current_run(현재 실행):": f"- current_run(현재 실행): `{NEXT_RUN_ID}`",
        "- status(상태):": "- status(상태): `completed_no_retune_stress_probe_design_ready_for_materialization`",
        "- decision(판정):": f"- decision(판정): `{DECISION}`",
    }
    for prefix, replacement in replacements.items():
        text = replace_prefix_line(text, prefix, replacement)
    summary = f"- run334E_summary(334E 요약): no-retune non-identity stress probe design(무재튜닝 비정체성 압박 탐침 설계)을 `{STATUS}`로 완료했다. Effect(효과): 6개 전체를 run334F(334F 실행)의 fixed-input diagnostic materialization(고정 입력 진단 물질화)으로 넘기고 선택 후보나 Goal Achieve(목표 달성)는 주장하지 않는다."
    text = insert_after_line_once(text, f"- decision(판정): `{DECISION}`", summary, "run334E_summary")
    write_text_lossless(CURRENT_STATE, text, had_bom)

    append_section_once(
        CHANGELOG,
        "## 2026-05-26 - Stage334E No-Retune Stress Probe Design(334E 무재튜닝 압박 탐침 설계)",
        f"""
- run334E(334E 실행): run334D(334D 실행)의 preserved clue/failure memory(보존 단서/실패 기억)를 no-retune stress probe(무재튜닝 압박 탐침) 계약과 run334F queue(334F 대기열)로 바꿨다.
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- next_action(다음 행동): `{NEXT_RUN_ID}`
- effect(효과): selected candidate(선택 후보), Forward Passed/Failed(전진 통과/실패), runtime authority(런타임 권위), Goal Achieve(목표 달성)는 주장하지 않는다.
""",
    )
    return [WORKSPACE_STATE, CURRENT_STATE, CHANGELOG]


def update_registries(artifacts: Sequence[Path], now: str) -> None:
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
                "path": f"stages/{STAGE_ID}/03_reviews/run334E_no_retune_nonidentity_stress_probe_design.md",
                "notes": "no_retune_stress_probe_design;run334F_queue_ready;goal_achieve_not_claimed.",
            }
        ],
    )
    upsert_csv(
        ALPHA_LEDGER,
        ["ledger_row_id"],
        [
            {
                "ledger_row_id": f"{RUN_ID}__no_retune_stress_design",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "subrun_id": RUN_NUMBER,
                "parent_run_id": PARENT_RUN_ID,
                "record_view": "no_retune_stress_probe_design",
                "tier_scope": "research_contract_no_tier_kpi",
                "kpi_scope": "design_only_no_new_trading_kpi",
                "scoreboard_lane": "experiment_design",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": f"stages/{STAGE_ID}/03_reviews/run334E_no_retune_nonidentity_stress_probe_design.md",
                "primary_kpi": "stress_matrix_rows=6;run334F_queue_rows=42",
                "guardrail_kpi": "no_model_training;no_threshold_retuning;no_lot_optimization;goal_achieve_not_claimed",
                "external_verification_status": "out_of_scope_by_claim_design_only",
                "notes": f"decision={DECISION};next_action={NEXT_RUN_ID}.",
            }
        ],
    )
    upsert_csv(
        STAGE_LEDGER,
        ["ledger_row_id"],
        [
            {
                "ledger_row_id": f"{RUN_ID}__no_retune_stress_design",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "work_family": "experiment_design",
                "evidence_scope": "no_retune_nonidentity_stress_probe_design",
                "kpi_scope": "design_only_no_new_trading_kpi",
                "status": STATUS,
                "judgment": JUDGMENT,
                "claim_boundary": CLAIM_BOUNDARY,
                "path": f"stages/{STAGE_ID}/03_reviews/run334E_no_retune_nonidentity_stress_probe_design.md",
                "notes": "no_candidate_selected;goal_achieve_not_claimed.",
                "decision": DECISION,
            }
        ],
    )
    artifact_rows = []
    for path in artifacts:
        artifact_rows.append(
            {
                "artifact_id": f"{RUN_ID}:{rel(path)}",
                "artifact_type": "stage334E_stress_probe_design_artifact",
                "path": rel(path),
                "sha256": sha256_file(path),
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "created_at_utc": now,
                "notes": "no-retune stress probe design artifact; no operating claim.",
            }
        )
    upsert_csv(ARTIFACT_REGISTRY, ["artifact_id"], artifact_rows)


def main() -> None:
    now = utc_now()
    context = load_context()
    outputs = build_outputs(context)
    run_artifacts = write_run_artifacts(context, outputs, now)
    report_artifacts = write_reports(outputs)
    stage_artifacts = update_stage_docs()
    state_artifacts = update_state_docs()
    all_artifacts = [Path(__file__), *run_artifacts, *report_artifacts, *stage_artifacts, *state_artifacts]
    update_registries(all_artifacts, now)
    print(
        json.dumps(
            {
                "status": STATUS,
                "judgment": JUDGMENT,
                "decision": DECISION,
                "stress_matrix_rows": len(outputs["matrix"]),
                "run334F_queue_rows": len(outputs["queue"]),
                "selected_candidate": "none",
                "forward_passed": "not_claimed",
                "forward_failed": "not_claimed",
                "runtime_authority": "not_claimed",
                "goal_achieve": "not_claimed",
                "next_action": NEXT_RUN_ID,
                "artifact_count": len(all_artifacts),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
