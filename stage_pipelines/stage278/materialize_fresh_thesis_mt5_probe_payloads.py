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
    read_csv_rows,
    upsert_csv_rows,
    write_csv_rows,
)


STAGE278_ID = "278_onnx_candidate_campaign__fresh_thesis_mt5_probe"
RUN_ID = "run278B_materialize_fresh_thesis_mt5_probe_payloads_v1"
SOURCE_RUN_ID = "run278A_design_fresh_thesis_mt5_probe_packet_v1"
STATUS = "completed_fresh_thesis_mt5_probe_payload_materialization_no_candidate_selection"
JUDGMENT = "fresh_thesis_mt5_probe_payloads_materialized_no_runtime_or_candidate_claim"
NEXT_ACTION = "run278C_execute_or_prepare_fresh_thesis_mt5_probe"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_"
    "no_deployment_no_onnx_until_candidate_package_gate"
)

STAGE = ROOT / "stages" / STAGE278_ID
RUN278A = STAGE / "02_runs" / "run278A"
RUN_DIR = STAGE / "02_runs" / "run278B"
PAYLOAD_DIR = RUN_DIR / "payloads"
HANDOFF_DIR = RUN_DIR / "handoff"
MT5_DIR = RUN_DIR / "mt5_handoff"
REVIEWS = STAGE / "03_reviews"
SELECTED_DIR = STAGE / "04_selected"

BRANCH_PLAN = RUN278A / "probe_branch_plan.csv"
BRANCH_METRICS = RUN278A / "branch_supply_metrics.csv"
DESIGN_QUEUE = RUN278A / "mt5_probe_design_queue.csv"
PAYLOAD_CONTRACT = RUN278A / "payload_contract_plan.csv"
TESTER_PLAN = RUN278A / "tester_identity_plan.csv"
RUN278A_MANIFEST = RUN278A / "run_manifest.json"
RUN278A_LINEAGE = RUN278A / "artifact_lineage_receipt.json"

PROBE_PAYLOAD_MANIFEST = RUN_DIR / "probe_payload_manifest.csv"
MT5_PROBE_QUEUE = RUN_DIR / "mt5_probe_queue.csv"
PAYLOAD_READINESS = RUN_DIR / "payload_readiness_receipt.csv"
TIER_ROUTE_RECEIPT = RUN_DIR / "tier_route_receipt.csv"
PAYLOAD_SAMPLES = RUN_DIR / "payload_samples.json"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment_design_receipt.json"
DATA_INTEGRITY_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
RUNTIME_PARITY_RECEIPT = RUN_DIR / "runtime_parity_receipt.json"
BACKTEST_FORENSICS_PLAN = RUN_DIR / "backtest_forensics_plan.json"
RESULT_JUDGMENT = RUN_DIR / "result_judgment.csv"
GATE_AUDIT = RUN_DIR / "required_gate_coverage_audit.csv"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
RUN_REPORT = REVIEWS / "run278B_report.md"
REVIEW_INDEX = REVIEWS / "review_index.md"
STAGE_LEDGER = REVIEWS / "stage_run_ledger.csv"
SELECTION_STATUS = SELECTED_DIR / "selection_status.md"

RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
IDEA_REGISTER = ROOT / "docs" / "registers" / "idea_registry.md"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"
PRODUCER_PATH = Path("stage_pipelines/stage278/materialize_fresh_thesis_mt5_probe_payloads.py")

KEY_COLUMNS = ("timestamp", "symbol", "split", "tier_scope")
LABEL_OR_FUTURE_PREFIXES = ("label", "future_")
LABEL_OR_FUTURE_COLUMNS = {
    "label",
    "label_alignment_flag",
    "evaluation_label_available",
    "future_log_return_12",
    "future_timestamp",
    "horizon_bars",
    "horizon_minutes",
}

MANIFEST_COLUMNS = (
    "branch_id",
    "queue_id",
    "package_id",
    "variant_role",
    "materialization_judgment",
    "next_queue_action",
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
    "decision_surface_hash",
    "tier_a_oos_signal_count",
    "tier_a_oos_signal_rate",
    "tier_b_oos_signal_count",
    "tier_b_oos_signal_rate",
    "actual_routed_oos_signal_count",
    "actual_routed_oos_signal_rate",
    "selected_candidate",
    "adapter_package",
    "onnx_readiness",
    "performance_claim",
)
MT5_QUEUE_COLUMNS = (
    "queue_id",
    "branch_id",
    "package_id",
    "queue_role",
    "payload_path",
    "handoff_path",
    "mt5_tier_a_signal_path",
    "mt5_tier_b_stress_signal_path",
    "mt5_actual_routed_signal_path",
    "feature_order_hash",
    "decision_surface_hash",
    "adapter_schema_hash",
    "signal_policy",
    "tester_identity_required",
    "required_before_external_claim",
    "claim_boundary",
)
TIER_ROUTE_COLUMNS = (
    "branch_id",
    "package_id",
    "record_view",
    "tier_scope",
    "split",
    "rows",
    "signal_count",
    "signal_rate",
    "source_entry_signal_count",
    "missing_required_feature_count_max",
    "fallback_count_design_proxy",
    "net_profit_claim",
    "claim_boundary",
)
READINESS_COLUMNS = ("check_name", "status", "effect")
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


def rel(path: Path | str) -> str:
    item = Path(str(path))
    try:
        return item.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return item.as_posix()


def repo_path(text: str) -> Path:
    return ROOT / text


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with io_path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(
        json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def write_text(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8")


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> None:
    write_csv_rows(path, columns, rows)


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def must_exist(paths: Sequence[Path]) -> None:
    missing = [rel(path) for path in paths if not path_exists(path)]
    if missing:
        raise FileNotFoundError("Missing required input artifacts: " + "; ".join(missing))


def ensure_dirs() -> None:
    for path in [RUN_DIR, PAYLOAD_DIR, HANDOFF_DIR, MT5_DIR, REVIEWS, SELECTED_DIR]:
        io_path(path).mkdir(parents=True, exist_ok=True)


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


def as_float(value: Any, default: float = 0.0) -> float:
    try:
        number = float(value)
    except Exception:
        return default
    return number if np.isfinite(number) else default


def safe_rate(numerator: float, denominator: float) -> float:
    return round(float(numerator) / float(denominator), 8) if denominator else 0.0


def output_hashes(paths: Sequence[Path]) -> dict[str, str]:
    return {rel(path): sha256_file(path) for path in paths if path_exists(path)}


def load_handoff(path: Path) -> dict[str, Any]:
    payload = read_json(path)
    payload.setdefault("model_hash", "not_applicable_score_surface_only")
    return payload


def source_paths(queue_rows: Sequence[Mapping[str, str]] | None = None) -> list[Path]:
    paths = [BRANCH_PLAN, BRANCH_METRICS, DESIGN_QUEUE, PAYLOAD_CONTRACT, TESTER_PLAN, RUN278A_MANIFEST, RUN278A_LINEAGE]
    if queue_rows:
        for row in queue_rows:
            for score_path in str(row["source_score_tables"]).split(";"):
                if score_path:
                    paths.append(repo_path(score_path))
            if row.get("source_handoff_json"):
                paths.append(repo_path(str(row["source_handoff_json"])))
    return paths


def payload_base_columns(frame: pd.DataFrame) -> list[str]:
    excluded = {
        column
        for column in frame.columns
        if column in LABEL_OR_FUTURE_COLUMNS or column.startswith(LABEL_OR_FUTURE_PREFIXES)
    }
    return [column for column in frame.columns if column not in excluded]


def load_score_tables(queue_row: Mapping[str, str]) -> pd.DataFrame:
    frames = []
    for score_path in str(queue_row["source_score_tables"]).split(";"):
        if score_path:
            frames.append(pd.read_parquet(io_path(repo_path(score_path))))
    if not frames:
        raise ValueError(f"No source score tables for {queue_row.get('branch_id')}")
    frame = pd.concat(frames, ignore_index=True).copy()
    missing = [column for column in KEY_COLUMNS if column not in frame.columns]
    if missing:
        raise ValueError(f"Score table missing key columns for {queue_row.get('branch_id')}: {missing}")
    if frame.duplicated(list(KEY_COLUMNS)).any():
        raise ValueError(f"Score table has duplicated timestamp/symbol/split/tier_scope rows for {queue_row.get('branch_id')}")
    required = {
        "package_id",
        "feature_order_hash",
        "feature_contract_hash",
        "decision_rule_hash",
        "adapter_schema_hash",
        "score_columns_hash",
        "missing_required_feature_count",
        "candidate_decision_score",
        "materialized_decision_flag",
        "entry_signal",
        "route_code",
        "model_risk_pct",
        "atr_stop_multiplier",
        "atr_take_profit_multiplier",
        "max_hold_bars",
        "reentry_cooldown_bars",
    }
    missing_required = sorted(required.difference(frame.columns))
    if missing_required:
        raise ValueError(f"Score table missing required payload columns for {queue_row.get('branch_id')}: {missing_required}")
    frame["timestamp"] = pd.to_datetime(frame["timestamp"], utc=True)
    frame["entry_active"] = pd.to_numeric(frame["materialized_decision_flag"], errors="coerce").fillna(0).astype(int).gt(0)
    return frame


def branch_mask(frame: pd.DataFrame, branch: Mapping[str, str]) -> pd.Series:
    branch_id = str(branch["branch_id"])
    thresholds = json.loads(str(branch.get("thresholds_json") or "{}"))
    active = frame["entry_active"]
    if branch_id.endswith("_q01_base_signal"):
        return active
    if branch_id.endswith("_q02_side_reversal_strict"):
        return (
            active
            & pd.to_numeric(frame["side_reversal_score"], errors="coerce").ge(thresholds["side_reversal_score_min"])
            & pd.to_numeric(frame["divergence_sign_score"], errors="coerce").ge(thresholds["divergence_sign_score_min"])
        ).fillna(False)
    if branch_id.endswith("_q03_session_pressure_cap"):
        return (
            active
            & pd.to_numeric(frame["session_pressure_score"], errors="coerce").le(thresholds["session_pressure_score_max"])
            & pd.to_numeric(frame["candidate_decision_score"], errors="coerce").ge(thresholds["candidate_decision_score_min"])
        ).fillna(False)
    if branch_id.endswith("_q02_contrast_reward_focus"):
        return (
            active
            & pd.to_numeric(frame["contrast_reward_score"], errors="coerce").ge(thresholds["contrast_reward_score_min"])
            & pd.to_numeric(frame["cooldown_score"], errors="coerce").ge(thresholds["cooldown_score_min"])
        ).fillna(False)
    if branch_id.endswith("_q03_late_loss_compression_guard"):
        return (
            active
            & pd.to_numeric(frame["late_loss_compression_score"], errors="coerce").ge(thresholds["late_loss_compression_score_min"])
            & pd.to_numeric(frame["cooldown_score"], errors="coerce").ge(thresholds["cooldown_score_min"])
        ).fillna(False)
    raise ValueError(f"run278B only materializes queued run278A branches, got {branch_id}")


def short_branch_id(branch_id: str) -> str:
    token = branch_id.replace("run278A_", "", 1)
    token = token.replace("directional_asymmetry_reversal_surface_", "dar_")
    token = token.replace("macro_squeeze_failure_contrast_surface_", "msfc_")
    return token


def decision_surface_hash(branch: Mapping[str, str], handoff: Mapping[str, Any]) -> str:
    return sha256_text(
        json.dumps(
            json_ready(
                {
                    "branch_id": branch["branch_id"],
                    "package_id": branch["package_id"],
                    "decision_rule": branch["decision_rule"],
                    "thresholds_json": branch["thresholds_json"],
                    "source_feature_order_hash": handoff.get("feature_order_hash"),
                    "source_decision_rule_hash": handoff.get("decision_rule_hash"),
                    "source_adapter_schema_hash": handoff.get("adapter_schema_hash"),
                }
            ),
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )
    )


def split_view(frame: pd.DataFrame, tier_scope: str, splits: Sequence[str] = ("validation", "oos")) -> pd.DataFrame:
    return frame[
        frame["tier_scope"].astype(str).eq(tier_scope) & frame["split"].astype(str).isin(list(splits))
    ].copy()


def signal_csv_columns() -> list[str]:
    return [
        "timestamp",
        "symbol",
        "split",
        "tier_scope",
        "record_view",
        "branch_id",
        "package_id",
        "signal_active",
        "route_signal_value",
        "route_signal_label",
        "source_entry_signal",
        "route_code",
        "candidate_decision_score",
        "model_risk_pct",
        "atr_stop_multiplier",
        "atr_take_profit_multiplier",
        "max_hold_bars",
        "reentry_cooldown_bars",
        "feature_order_hash",
        "decision_rule_hash",
        "adapter_schema_hash",
        "variant_decision_surface_hash",
        "payload_claim_boundary",
    ]


def write_signal_csv(path: Path, frame: pd.DataFrame, record_view: str) -> None:
    output = frame.copy()
    output["record_view"] = record_view
    output["timestamp"] = pd.to_datetime(output["timestamp"], utc=True).dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    output[signal_csv_columns()].to_csv(io_path(path), index=False, lineterminator="\n", encoding="utf-8")


def receipt_rows_for_view(
    payload: pd.DataFrame,
    branch_id: str,
    package_id: str,
    record_view: str,
    tier_scope: str,
    *,
    fallback_count_design_proxy: int | str,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    view = payload[payload["tier_scope"].astype(str).eq(tier_scope)]
    for split in ["train", "validation", "oos"]:
        part = view[view["split"].astype(str).eq(split)]
        signal_count = int(pd.to_numeric(part["signal_active"], errors="coerce").fillna(0).sum())
        rows.append(
            {
                "branch_id": branch_id,
                "package_id": package_id,
                "record_view": record_view,
                "tier_scope": tier_scope,
                "split": split,
                "rows": int(len(part)),
                "signal_count": signal_count,
                "signal_rate": safe_rate(signal_count, len(part)),
                "source_entry_signal_count": int(pd.to_numeric(part["source_entry_signal"], errors="coerce").fillna(0).sum()),
                "missing_required_feature_count_max": int(part["missing_required_feature_count"].max()) if len(part) else 0,
                "fallback_count_design_proxy": fallback_count_design_proxy,
                "net_profit_claim": "not_claimed_no_mt5_runtime_output",
                "claim_boundary": BOUNDARY,
            }
        )
    return rows


def pick_receipt_value(rows: Sequence[Mapping[str, Any]], branch_id: str, record_view: str, split: str, field: str) -> Any:
    for row in rows:
        if row["branch_id"] == branch_id and row["record_view"] == record_view and row["split"] == split:
            return row[field]
    return ""


def load_inputs() -> tuple[list[dict[str, str]], dict[str, dict[str, str]], dict[str, dict[str, str]], dict[str, dict[str, str]]]:
    queue_rows = read_csv_rows(DESIGN_QUEUE)
    if len(queue_rows) != 6:
        raise ValueError(f"Expected 6 queued run278B branches, got {len(queue_rows)}")
    must_exist(source_paths(queue_rows))
    branch_by_id = {row["branch_id"]: row for row in read_csv_rows(BRANCH_PLAN)}
    contract_by_id = {row["branch_id"]: row for row in read_csv_rows(PAYLOAD_CONTRACT)}
    tester_by_id = {row["branch_id"]: row for row in read_csv_rows(TESTER_PLAN)}
    for row in queue_rows:
        if row["branch_id"] not in branch_by_id:
            raise ValueError(f"Queue branch missing from branch plan: {row['branch_id']}")
        if row["branch_id"] not in contract_by_id:
            raise ValueError(f"Queue branch missing from payload contract: {row['branch_id']}")
        if row["branch_id"] not in tester_by_id:
            raise ValueError(f"Queue branch missing from tester plan: {row['branch_id']}")
    return queue_rows, branch_by_id, contract_by_id, tester_by_id


def materialize_payloads(
    queue_rows: Sequence[Mapping[str, str]],
    branch_by_id: Mapping[str, Mapping[str, str]],
    contract_by_id: Mapping[str, Mapping[str, str]],
    tester_by_id: Mapping[str, Mapping[str, str]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], dict[str, Any], dict[str, str]]:
    manifest_rows: list[dict[str, Any]] = []
    mt5_queue_rows: list[dict[str, Any]] = []
    tier_rows: list[dict[str, Any]] = []
    samples: dict[str, Any] = {}
    source_hashes: dict[str, str] = output_hashes(source_paths(queue_rows))

    for queue_row in queue_rows:
        branch_id = str(queue_row["branch_id"])
        branch = branch_by_id[branch_id]
        contract = contract_by_id[branch_id]
        tester = tester_by_id[branch_id]
        frame = load_score_tables(queue_row)
        handoff_path = repo_path(str(queue_row["source_handoff_json"]))
        handoff = load_handoff(handoff_path)
        mask = branch_mask(frame, branch)
        surface_hash = decision_surface_hash(branch, handoff)
        token = short_branch_id(branch_id)
        base_columns = payload_base_columns(frame)

        payload = frame[base_columns].copy()
        payload["source_run_id"] = SOURCE_RUN_ID
        payload["run278b_queue_id"] = queue_row["queue_id"]
        payload["branch_id"] = branch_id
        payload["variant_role"] = branch["variant_role"]
        payload["fresh_thesis"] = branch["fresh_thesis"]
        payload["route_policy"] = branch["route_policy"]
        payload["signal_policy"] = branch["signal_policy"]
        payload["variant_decision_flag"] = mask.astype("int8")
        payload["signal_active"] = payload["variant_decision_flag"].astype("int8")
        payload["route_signal_value"] = payload["signal_active"].astype("int8")
        payload["route_signal_label"] = payload["signal_active"].map({1: "active", 0: "flat"})
        payload["source_entry_signal"] = pd.to_numeric(payload["entry_signal"], errors="coerce").fillna(0).astype("int8")
        payload["runtime_handoff_status"] = "prepared_for_mt5_probe_no_runtime_claim"
        payload["variant_decision_surface_hash"] = surface_hash
        payload["source_feature_order_hash"] = handoff["feature_order_hash"]
        payload["source_feature_contract_hash"] = handoff["feature_contract_hash"]
        payload["source_decision_rule_hash"] = handoff["decision_rule_hash"]
        payload["source_adapter_schema_hash"] = handoff["adapter_schema_hash"]
        payload["source_score_columns_hash"] = handoff["score_columns_hash"]
        payload["source_model_hash"] = handoff.get("model_hash", "not_applicable_score_surface_only")
        payload["tester_identity_plan"] = tester["tester_identity"]
        payload["payload_claim_boundary"] = BOUNDARY

        payload_path = PAYLOAD_DIR / f"{branch_id}_payload.parquet"
        payload.to_parquet(io_path(payload_path), index=False)

        tier_a = split_view(payload, "Tier A")
        tier_b = split_view(payload, "Tier B")
        routed = tier_a.copy()
        routed["tier_scope"] = "actual routed total"

        tier_a_path = MT5_DIR / f"{branch_id}_tier_a_signals.csv"
        tier_b_path = MT5_DIR / f"{branch_id}_tier_b_stress_signals.csv"
        routed_path = MT5_DIR / f"{branch_id}_actual_routed_total_signals.csv"
        write_signal_csv(tier_a_path, tier_a, "Tier A used(Tier A 사용)")
        write_signal_csv(tier_b_path, tier_b, "Tier B fallback stress(Tier B 대체 스트레스)")
        write_signal_csv(routed_path, routed, "actual routed total(실제 라우팅 전체)")

        local_tier_rows = []
        local_tier_rows.extend(
            receipt_rows_for_view(
                payload,
                branch_id,
                branch["package_id"],
                "Tier A used(Tier A 사용)",
                "Tier A",
                fallback_count_design_proxy="",
            )
        )
        local_tier_rows.extend(
            receipt_rows_for_view(
                payload,
                branch_id,
                branch["package_id"],
                "Tier B fallback stress(Tier B 대체 스트레스)",
                "Tier B",
                fallback_count_design_proxy="",
            )
        )
        local_tier_rows.extend(
            receipt_rows_for_view(
                payload,
                branch_id,
                branch["package_id"],
                "actual routed total(실제 라우팅 전체)",
                "Tier A",
                fallback_count_design_proxy=0,
            )
        )
        tier_rows.extend(local_tier_rows)

        handoff_payload = {
            "run_id": RUN_ID,
            "stage_id": STAGE278_ID,
            "source_run_id": SOURCE_RUN_ID,
            "source_queue_id": queue_row["queue_id"],
            "branch_id": branch_id,
            "package_id": branch["package_id"],
            "variant_role": branch["variant_role"],
            "fresh_thesis": branch["fresh_thesis"],
            "decision_rule": branch["decision_rule"],
            "thresholds": json.loads(str(branch.get("thresholds_json") or "{}")),
            "decision_surface_hash": surface_hash,
            "feature_order_hash": handoff["feature_order_hash"],
            "feature_contract_hash": handoff["feature_contract_hash"],
            "decision_rule_hash": handoff["decision_rule_hash"],
            "adapter_schema_hash": handoff["adapter_schema_hash"],
            "score_columns_hash": handoff["score_columns_hash"],
            "model_hash": handoff.get("model_hash", "not_applicable_score_surface_only"),
            "payload_path": rel(payload_path),
            "payload_hash": sha256_file(payload_path),
            "mt5_tier_a_signal_path": rel(tier_a_path),
            "mt5_tier_a_signal_hash": sha256_file(tier_a_path),
            "mt5_tier_b_stress_signal_path": rel(tier_b_path),
            "mt5_tier_b_stress_signal_hash": sha256_file(tier_b_path),
            "mt5_actual_routed_signal_path": rel(routed_path),
            "mt5_actual_routed_signal_hash": sha256_file(routed_path),
            "route_policy": branch["route_policy"],
            "signal_policy": "active=1, flat=0(활성 1, 관망 0); no long/short direction claim(롱/숏 방향 주장 없음)",
            "tester_identity_plan": tester,
            "materialization_judgment": JUDGMENT,
            "next_queue_action": "include_for_run278C_mt5_probe_preparation",
            "selected_candidate": "none",
            "selected_research_baseline": "none",
            "adapter_package": "none",
            "onnx_readiness": "not_claimed",
            "goal_achieve": "not_claimed",
            "performance_claim": "none",
            "claim_boundary": BOUNDARY,
        }
        handoff_out = HANDOFF_DIR / f"{branch_id}.json"
        write_json(handoff_out, handoff_payload)

        manifest_rows.append(
            {
                "branch_id": branch_id,
                "queue_id": queue_row["queue_id"],
                "package_id": branch["package_id"],
                "variant_role": branch["variant_role"],
                "materialization_judgment": JUDGMENT,
                "next_queue_action": "include_for_run278C_mt5_probe_preparation",
                "payload_path": rel(payload_path),
                "payload_hash": sha256_file(payload_path),
                "handoff_path": rel(handoff_out),
                "handoff_hash": sha256_file(handoff_out),
                "mt5_tier_a_signal_path": rel(tier_a_path),
                "mt5_tier_a_signal_hash": sha256_file(tier_a_path),
                "mt5_tier_b_stress_signal_path": rel(tier_b_path),
                "mt5_tier_b_stress_signal_hash": sha256_file(tier_b_path),
                "mt5_actual_routed_signal_path": rel(routed_path),
                "mt5_actual_routed_signal_hash": sha256_file(routed_path),
                "decision_surface_hash": surface_hash,
                "tier_a_oos_signal_count": pick_receipt_value(local_tier_rows, branch_id, "Tier A used(Tier A 사용)", "oos", "signal_count"),
                "tier_a_oos_signal_rate": pick_receipt_value(local_tier_rows, branch_id, "Tier A used(Tier A 사용)", "oos", "signal_rate"),
                "tier_b_oos_signal_count": pick_receipt_value(
                    local_tier_rows,
                    branch_id,
                    "Tier B fallback stress(Tier B 대체 스트레스)",
                    "oos",
                    "signal_count",
                ),
                "tier_b_oos_signal_rate": pick_receipt_value(
                    local_tier_rows,
                    branch_id,
                    "Tier B fallback stress(Tier B 대체 스트레스)",
                    "oos",
                    "signal_rate",
                ),
                "actual_routed_oos_signal_count": pick_receipt_value(
                    local_tier_rows,
                    branch_id,
                    "actual routed total(실제 라우팅 전체)",
                    "oos",
                    "signal_count",
                ),
                "actual_routed_oos_signal_rate": pick_receipt_value(
                    local_tier_rows,
                    branch_id,
                    "actual routed total(실제 라우팅 전체)",
                    "oos",
                    "signal_rate",
                ),
                "selected_candidate": "none",
                "adapter_package": "none",
                "onnx_readiness": "not_claimed",
                "performance_claim": "none",
            }
        )
        mt5_queue_rows.append(
            {
                "queue_id": f"run278C_{len(mt5_queue_rows) + 1:02d}_{token}",
                "branch_id": branch_id,
                "package_id": branch["package_id"],
                "queue_role": "fresh_thesis_mt5_probe_payload",
                "payload_path": rel(payload_path),
                "handoff_path": rel(handoff_out),
                "mt5_tier_a_signal_path": rel(tier_a_path),
                "mt5_tier_b_stress_signal_path": rel(tier_b_path),
                "mt5_actual_routed_signal_path": rel(routed_path),
                "feature_order_hash": contract["feature_order_hash"],
                "decision_surface_hash": surface_hash,
                "adapter_schema_hash": contract["adapter_schema_hash"],
                "signal_policy": "active_flat_signal_only_no_direction_claim(활성/관망 신호만, 방향 주장 없음)",
                "tester_identity_required": "broker_terminal_snapshot;strategy_tester_report;trade_list;spread_commission_slippage_swap_capture",
                "required_before_external_claim": "MT5 runtime output;tester report;trade list;balance/equity curve;time-slice KPI;trade quality",
                "claim_boundary": BOUNDARY,
            }
        )
        sample = payload[
            [
                "timestamp",
                "split",
                "tier_scope",
                "branch_id",
                "signal_active",
                "route_signal_value",
                "route_signal_label",
                "source_entry_signal",
                "candidate_decision_score",
                "model_risk_pct",
            ]
        ].head(3).copy()
        sample["timestamp"] = pd.to_datetime(sample["timestamp"], utc=True).dt.strftime("%Y-%m-%dT%H:%M:%SZ")
        samples[branch_id] = sample.to_dict("records")

    return manifest_rows, mt5_queue_rows, tier_rows, samples, source_hashes


def split_window_from_rows(rows: Sequence[Mapping[str, Any]], split: str) -> str:
    timestamps: list[pd.Timestamp] = []
    for row in rows:
        payload_path = repo_path(str(row["payload_path"]))
        frame = pd.read_parquet(io_path(payload_path), columns=["timestamp", "split"])
        part = frame[frame["split"].astype(str).eq(split)]
        if not part.empty:
            timestamps.extend([part["timestamp"].min(), part["timestamp"].max()])
    if not timestamps:
        return "missing_required(필수 누락)"
    return f"{min(timestamps).date()}..{max(timestamps).date()}"


def write_stage_outputs(
    manifest_rows: Sequence[Mapping[str, Any]],
    mt5_queue_rows: Sequence[Mapping[str, Any]],
    tier_rows: Sequence[Mapping[str, Any]],
    samples: Mapping[str, Any],
    source_hashes: Mapping[str, str],
) -> None:
    write_csv(PROBE_PAYLOAD_MANIFEST, MANIFEST_COLUMNS, manifest_rows)
    write_csv(MT5_PROBE_QUEUE, MT5_QUEUE_COLUMNS, mt5_queue_rows)
    write_csv(TIER_ROUTE_RECEIPT, TIER_ROUTE_COLUMNS, tier_rows)
    write_csv(
        PAYLOAD_READINESS,
        READINESS_COLUMNS,
        [
            {
                "check_name": "queued_payloads_materialized",
                "status": "passed(통과)",
                "effect": f"payload parquet(페이로드 파케이) {len(manifest_rows)}개와 MT5 queue(MT5 대기열) {len(mt5_queue_rows)}행을 만들었다.",
            },
            {
                "check_name": "paired_tier_signal_files",
                "status": "passed(통과)",
                "effect": "Tier A used/Tier B fallback stress/actual routed total(Tier A 사용/Tier B 대체 스트레스/실제 라우팅 전체) 신호 파일을 분리했다.",
            },
            {
                "check_name": "label_future_columns_removed",
                "status": "passed(통과)",
                "effect": "label/future columns(라벨/미래 열)을 payload(페이로드)와 MT5 signal CSV(MT5 신호 CSV)에 넣지 않았다.",
            },
            {
                "check_name": "runtime_claim_boundary",
                "status": "out_of_scope_by_claim(주장 범위 밖)",
                "effect": "MT5 runtime output(MT5 런타임 출력)과 trading KPI(거래 핵심 성과 지표)는 아직 없다.",
            },
            {
                "check_name": "candidate_onnx_claim_guard",
                "status": "passed(통과)",
                "effect": "selected candidate(선택 후보), Adapter package(어댑터 패키지), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)를 주장하지 않는다.",
            },
        ],
    )
    write_json(PAYLOAD_SAMPLES, samples)
    write_json(
        EXPERIMENT_RECEIPT,
        {
            "run_id": RUN_ID,
            "hypothesis": "fresh thesis score surfaces(새 논제 점수 표면)를 active/flat payload(활성/관망 페이로드)로 물질화하면 MT5 probe(MT5 탐침)를 좁게 준비할 수 있다.",
            "comparison": "cp277C/cp277D base branches(기준 분기) versus strict/focused guard branches(엄격/집중 보호 분기)",
            "controls": "same source score tables(같은 원천 점수표), same feature order hash(같은 피처 순서 해시), same route policy(같은 경로 정책)",
            "changed_variables": "branch decision surface(분기 판단 표면)와 threshold(임계값)",
            "payload_count": len(manifest_rows),
            "mt5_queue_rows": len(mt5_queue_rows),
            "success_criteria": "all queued branches(모든 대기 분기)가 payload, handoff, three route-view signal files(세 라우팅 보기 신호 파일)를 만든다.",
            "failure_criteria": "missing payload(페이로드 누락), missing handoff(인계 누락), empty OOS signal supply(표본외 신호 공급 없음), or label leakage(라벨 누출)",
            "selected_candidate": "none",
            "adapter_package": "none",
            "onnx_readiness": "not_claimed",
            "goal_achieve": "not_claimed",
            "claim_boundary": BOUNDARY,
        },
    )
    write_json(
        DATA_INTEGRITY_RECEIPT,
        {
            "run_id": RUN_ID,
            "source_inputs": [rel(path) for path in source_paths(read_csv_rows(DESIGN_QUEUE))],
            "source_hashes": dict(source_hashes),
            "split_windows": {
                "train": split_window_from_rows(manifest_rows, "train"),
                "validation": split_window_from_rows(manifest_rows, "validation"),
                "oos": split_window_from_rows(manifest_rows, "oos"),
            },
            "key_columns": list(KEY_COLUMNS),
            "feature_label_boundary": "label/future columns(라벨/미래 열)은 branch mask(분기 마스크)와 runtime handoff(런타임 인계)에 쓰지 않는다.",
            "tier_policy": "Tier A primary + Tier B fallback(Tier A 우선 + Tier B 대체); actual routed total(실제 라우팅 전체)은 Tier A rows(Tier A 행) proxy(대리)이며 fallback_count_design_proxy=0이다.",
            "integrity_judgment": "usable_with_boundary(경계 포함 사용 가능)",
            "claim_boundary": BOUNDARY,
        },
    )
    write_json(
        RUNTIME_PARITY_RECEIPT,
        {
            "research_path": rel(PRODUCER_PATH),
            "runtime_path": [row["mt5_actual_routed_signal_path"] for row in manifest_rows],
            "shared_contract": "feature_order_hash(피처 순서 해시), decision_surface_hash(판단 표면 해시), adapter_schema_hash(어댑터 스키마 해시), active/flat signal policy(활성/관망 신호 정책), risk fields(위험 필드)",
            "known_differences": "Python payload(파이썬 페이로드)는 MT5 tester output(MT5 테스터 출력)이 아니며 direction(방향)은 아직 active/flat(활성/관망)이다.",
            "parity_check": "file handoff hash check(파일 인계 해시 점검) and feature/order identity carry-forward(피처/순서 정체성 이월)",
            "parity_identity": {
                "payload_manifest": rel(PROBE_PAYLOAD_MANIFEST),
                "mt5_probe_queue": rel(MT5_PROBE_QUEUE),
                "tier_route_receipt": rel(TIER_ROUTE_RECEIPT),
                "output_hashes": {row["payload_path"]: row["payload_hash"] for row in manifest_rows},
            },
            "runtime_claim_boundary": "runtime_probe_preparation_only(런타임 탐침 준비만 해당)",
            "claim_boundary": BOUNDARY,
        },
    )
    write_json(
        BACKTEST_FORENSICS_PLAN,
        {
            "tester_identity": "must_capture_in_run278C_from_MT5_strategy_tester(run278C에서 MT5 전략 테스터로 캡처 필요)",
            "ea_identity": "no_EA_entrypoint_change_in_run278B(run278B에서 EA 진입점 변경 없음)",
            "report_identity": "missing_until_MT5_execution(MT5 실행 전까지 누락)",
            "trade_evidence": "missing_until_MT5_execution(MT5 실행 전까지 누락)",
            "cost_assumptions": "spread/commission/slippage/swap(스프레드/커미션/슬리피지/스왑) 캡처 필요",
            "forensic_checks": "payload and signal path existence(페이로드와 신호 경로 존재)만 확인했다.",
            "backtest_judgment": "not_applicable_payload_materialization_only(페이로드 물질화 전용으로 해당 없음)",
            "claim_boundary": BOUNDARY,
        },
    )
    write_csv(
        RESULT_JUDGMENT,
        RESULT_COLUMNS,
        [
            {
                "result_subject": "run278B fresh thesis MT5 probe payload materialization(278B 새 논제 MT5 탐침 페이로드 물질화)",
                "evidence_available": "payload parquet(페이로드 파케이);handoff JSON(인계 JSON);MT5 signal CSV(MT5 신호 CSV);tier route receipt(티어 라우팅 영수증);manifest(목록);lineage(계보)",
                "evidence_missing": "MT5 runtime output(MT5 런타임 출력);tester report(테스터 보고서);trade list(거래 목록);balance/equity curve(잔액/평가금 곡선);Adapter package(어댑터 패키지);ONNX parity(온엑스 동등성)",
                "judgment_label": JUDGMENT,
                "judgment_class": "payload_materialized_no_runtime_or_candidate_claim(페이로드 물질화, 런타임/후보 주장 없음)",
                "claim_boundary": BOUNDARY,
                "next_condition": NEXT_ACTION,
                "user_explanation_hook": f"{len(manifest_rows)}개 payload(페이로드)와 {len(mt5_queue_rows)}개 MT5 queue(MT5 대기열)를 만들었지만 후보나 ONNX 준비는 아니다.",
            }
        ],
    )
    write_csv(
        GATE_AUDIT,
        GATE_COLUMNS,
        [
            {
                "gate_name": "payload_contract_gate(페이로드 계약 게이트)",
                "status": "passed_payloads_and_handoffs_created(페이로드와 인계 생성으로 통과)",
                "evidence_path": rel(PROBE_PAYLOAD_MANIFEST),
                "effect": "run278C(278C 실행)가 소비할 파일 단위가 생겼다.",
            },
            {
                "gate_name": "paired_tier_gate(티어 쌍 게이트)",
                "status": "passed_tier_a_tier_b_routed_files_created(Tier A/Tier B/라우팅 파일 생성으로 통과)",
                "evidence_path": rel(TIER_ROUTE_RECEIPT),
                "effect": "Tier A used(Tier A 사용), Tier B fallback stress(Tier B 대체 스트레스), actual routed total(실제 라우팅 전체)을 분리한다.",
            },
            {
                "gate_name": "runtime_parity_boundary_gate(런타임 동등성 경계 게이트)",
                "status": "passed_preparation_only_no_runtime_claim(준비 전용, 런타임 주장 없음으로 통과)",
                "evidence_path": rel(RUNTIME_PARITY_RECEIPT),
                "effect": "file handoff(파일 인계)를 runtime authority(런타임 권위)로 오해하지 않는다.",
            },
            {
                "gate_name": "backtest_forensics_plan_gate(백테스트 포렌식 계획 게이트)",
                "status": "passed_plan_carried_forward_no_tester_output(계획 이월, 테스터 출력 없음으로 통과)",
                "evidence_path": rel(BACKTEST_FORENSICS_PLAN),
                "effect": "tester identity(테스터 정체성)는 run278C(278C 실행)에서 캡처해야 한다.",
            },
            {
                "gate_name": "claim_guard(주장 보호 게이트)",
                "status": "passed_no_selected_candidate_no_adapter_no_onnx_no_goal(선택 후보/어댑터/온엑스/목표 달성 없음으로 통과)",
                "evidence_path": rel(RESULT_JUDGMENT),
                "effect": "후보 선택이나 ONNX readiness(온엑스 준비)를 말하지 않는다.",
            },
        ],
    )


def report_markdown(manifest_rows: Sequence[Mapping[str, Any]], mt5_queue_rows: Sequence[Mapping[str, Any]]) -> str:
    payload_lines = "\n".join(
        (
            f"- `{row['branch_id']}`: Tier A OOS signal_rate(Tier A 표본외 신호 비율) "
            f"`{row['tier_a_oos_signal_rate']}`, Tier B OOS signal_rate(Tier B 표본외 신호 비율) "
            f"`{row['tier_b_oos_signal_rate']}`, routed OOS signal_rate(라우팅 표본외 신호 비율) "
            f"`{row['actual_routed_oos_signal_rate']}`"
        )
        for row in manifest_rows
    )
    queue_lines = "\n".join(
        f"- `{row['queue_id']}` -> `{row['branch_id']}`"
        for row in mt5_queue_rows
    )
    return f"""# run278B Report(278B 보고서): Fresh Thesis MT5 Probe Payload Materialization(새 논제 MT5 탐침 페이로드 물질화)

- run_id(실행 ID): `{RUN_ID}`
- stage_id(단계 ID): `{STAGE278_ID}`
- source_run(원천 실행): `{SOURCE_RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- payload_count(페이로드 수): `{len(manifest_rows)}`
- mt5_queue_rows(MT5 대기열 행): `{len(mt5_queue_rows)}`
- selected_candidate(선택 후보): `none`
- Adapter package(어댑터 패키지): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_ACTION}`

## Plain Result(쉬운 결과)

run278B(278B 실행)는 run278A(278A 실행)의 MT5 probe design queue(MT5 탐침 설계 대기열) `6`행을 payload parquet(페이로드 파케이), handoff JSON(인계 JSON), MT5 signal CSV(MT5 신호 CSV)로 물질화했다.
Effect(효과): run278C(278C 실행)가 MT5(`MetaTrader 5`, 메타트레이더5) runtime probe(런타임 탐침)를 준비하거나 실행할 수 있는 입력 파일이 생겼다.

## Payloads(페이로드)

{payload_lines}

## MT5 Probe Queue(MT5 탐침 대기열)

{queue_lines}

## Boundary(경계)

이 실행(run, 실행)은 payload materialization(페이로드 물질화)만 완료했다.
Effect(효과): selected candidate(선택 후보), Adapter package(어댑터 패키지), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성), runtime result(런타임 결과)는 주장하지 않는다.

`{BOUNDARY}`
"""


def update_ledgers(manifest_rows: Sequence[Mapping[str, Any]], mt5_queue_rows: Sequence[Mapping[str, Any]]) -> None:
    payload_count = len(manifest_rows)
    queue_count = len(mt5_queue_rows)
    upsert_csv_rows(
        RUN_REGISTRY,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE278_ID,
                "lane": "runtime_probe_payload_materialization",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(RUN_REPORT),
                "notes": f"payload_count={payload_count};mt5_queue_rows={queue_count};selected_candidate=none;adapter_package=none;onnx_readiness=not_claimed;next_action={NEXT_ACTION}.",
            }
        ],
        key="run_id",
    )
    upsert_csv_rows(
        STAGE_LEDGER,
        STAGE_LEDGER_COLUMNS,
        [
            {
                "row_id": f"{RUN_ID}__tier_a_payload",
                "stage_id": STAGE278_ID,
                "run_id": RUN_ID,
                "view": "fresh_thesis_mt5_probe_payload_materialization",
                "tier_scope": "Tier A used",
                "scoreboard": "runtime_probe_payload_preparation",
                "status": STATUS,
                "judgment": JUDGMENT,
                "evidence_boundary": "payload_materialization_only_no_runtime_kpi",
                "report_path": rel(RUN_REPORT),
                "notes": f"payload_count={payload_count};Tier A signal files materialized.",
            },
            {
                "row_id": f"{RUN_ID}__tier_b_payload",
                "stage_id": STAGE278_ID,
                "run_id": RUN_ID,
                "view": "fresh_thesis_mt5_probe_payload_materialization",
                "tier_scope": "Tier B fallback stress",
                "scoreboard": "runtime_probe_payload_preparation",
                "status": STATUS,
                "judgment": "tier_b_stress_payload_materialized_no_runtime_authority(티어 B 스트레스 페이로드 물질화, 런타임 권위 없음)",
                "evidence_boundary": "partial_context_payload_only",
                "report_path": rel(RUN_REPORT),
                "notes": "Tier B stress files are paired context evidence only.",
            },
            {
                "row_id": f"{RUN_ID}__actual_routed_payload",
                "stage_id": STAGE278_ID,
                "run_id": RUN_ID,
                "view": "fresh_thesis_mt5_probe_payload_materialization",
                "tier_scope": "actual routed total",
                "scoreboard": "runtime_probe_payload_preparation",
                "status": STATUS,
                "judgment": "actual_routed_payload_prepared_no_tester_output(실제 라우팅 페이로드 준비, 테스터 출력 없음)",
                "evidence_boundary": "routed_payload_only_no_pnl_claim",
                "report_path": rel(RUN_REPORT),
                "notes": f"actual routed total signal files={queue_count};fallback_count_design_proxy=0.",
            },
        ],
        key="row_id",
    )
    upsert_csv_rows(
        ALPHA_LEDGER,
        ALPHA_LEDGER_COLUMNS,
        [
            {
                "ledger_row_id": f"{RUN_ID}__tier_a_payload",
                "stage_id": STAGE278_ID,
                "run_id": RUN_ID,
                "subrun_id": "tier_a_payload",
                "parent_run_id": SOURCE_RUN_ID,
                "record_view": "Tier A used payload materialization(Tier A 사용 페이로드 물질화)",
                "tier_scope": "Tier A used",
                "kpi_scope": "payload_materialization_no_trading_kpi",
                "scoreboard_lane": "runtime_probe_payload_preparation",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(TIER_ROUTE_RECEIPT),
                "primary_kpi": f"payload_count={payload_count};mt5_queue_rows={queue_count}",
                "guardrail_kpi": "selected_candidate=none;adapter_package=none;onnx_readiness=not_claimed",
                "external_verification_status": "out_of_scope_by_claim_payload_materialization_only",
                "notes": "Tier A signal files are prepared for run278C, not runtime evidence.",
            },
            {
                "ledger_row_id": f"{RUN_ID}__tier_b_payload",
                "stage_id": STAGE278_ID,
                "run_id": RUN_ID,
                "subrun_id": "tier_b_payload",
                "parent_run_id": SOURCE_RUN_ID,
                "record_view": "Tier B fallback stress payload materialization(Tier B 대체 스트레스 페이로드 물질화)",
                "tier_scope": "Tier B fallback stress",
                "kpi_scope": "payload_materialization_no_trading_kpi",
                "scoreboard_lane": "runtime_probe_payload_preparation",
                "status": STATUS,
                "judgment": "tier_b_stress_payload_materialized_no_runtime_authority(티어 B 스트레스 페이로드 물질화, 런타임 권위 없음)",
                "path": rel(TIER_ROUTE_RECEIPT),
                "primary_kpi": f"payload_count={payload_count}",
                "guardrail_kpi": "tier_b_runtime_authority=not_claimed",
                "external_verification_status": "out_of_scope_by_claim_payload_materialization_only",
                "notes": "Tier B rows remain paired stress context.",
            },
            {
                "ledger_row_id": f"{RUN_ID}__actual_routed_payload",
                "stage_id": STAGE278_ID,
                "run_id": RUN_ID,
                "subrun_id": "actual_routed_payload",
                "parent_run_id": SOURCE_RUN_ID,
                "record_view": "actual routed total payload materialization(실제 라우팅 전체 페이로드 물질화)",
                "tier_scope": "actual routed total",
                "kpi_scope": "payload_materialization_no_pnl_claim",
                "scoreboard_lane": "runtime_probe_payload_preparation",
                "status": STATUS,
                "judgment": "actual_routed_payload_prepared_no_tester_output(실제 라우팅 페이로드 준비, 테스터 출력 없음)",
                "path": rel(MT5_PROBE_QUEUE),
                "primary_kpi": f"mt5_queue_rows={queue_count};fallback_count_design_proxy=0",
                "guardrail_kpi": "performance_claim=none;runtime_authority=not_claimed",
                "external_verification_status": "out_of_scope_by_claim_payload_materialization_only",
                "notes": "Actual routed total is a signal file view, not tester PnL.",
            },
        ],
        key="ledger_row_id",
    )


def update_state_docs(payload_count: int, queue_count: int) -> None:
    selected = io_path(SELECTION_STATUS).read_text(encoding="utf-8-sig")
    selected = replace_line_prefix(selected, "- stage_status(", f"- stage_status(단계 상태): `{STATUS}`")
    selected = replace_line_prefix(selected, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    selected = replace_line_prefix(selected, "- last_completed_run(", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
    selected = replace_line_prefix(selected, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    selected = append_once(selected, "run278B_payload_manifest", f"- run278B_payload_manifest(278B 페이로드 목록): `{rel(PROBE_PAYLOAD_MANIFEST)}`")
    selected = append_once(selected, "run278B_mt5_probe_queue", f"- run278B_mt5_probe_queue(278B MT5 탐침 대기열): `{rel(MT5_PROBE_QUEUE)}`")
    selected = append_once(selected, "run278B_report", f"- run278B_report(278B 보고서): `{rel(RUN_REPORT)}`")
    write_md(SELECTION_STATUS, selected)

    review = io_path(REVIEW_INDEX).read_text(encoding="utf-8-sig")
    review = append_once(
        review,
        "run278B_report",
        "\n".join(
            [
                f"- run278B_report(278B 보고서): `{rel(RUN_REPORT)}`",
                f"- run278B_payload_manifest(278B 페이로드 목록): `{rel(PROBE_PAYLOAD_MANIFEST)}`",
                f"- run278B_mt5_probe_queue(278B MT5 탐침 대기열): `{rel(MT5_PROBE_QUEUE)}`",
                f"- run278B_tier_route_receipt(278B 티어 라우팅 영수증): `{rel(TIER_ROUTE_RECEIPT)}`",
            ]
        ),
    )
    write_md(REVIEW_INDEX, review)

    current = io_path(CURRENT_STATE).read_text(encoding="utf-8-sig")
    current = replace_line_prefix(current, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_line_prefix(current, "- status(", f"- status(상태): `{STATUS}`")
    current = replace_line_prefix(current, "- target_surface(", "- target_surface(목표 표면): `fresh_thesis_mt5_probe_payload_materialization`")
    current = replace_line_prefix(current, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    current = append_once(
        current,
        "run278B_summary",
        (
            f"- run278B_summary(278B 요약): fresh thesis MT5 probe payloads(새 논제 MT5 탐침 페이로드)를 물질화했다. "
            f"Effect(효과): payload parquet(페이로드 파케이) `{payload_count}`개와 MT5 probe queue(MT5 탐침 대기열) `{queue_count}`행을 만들었고, selected candidate(선택 후보), Adapter package(어댑터 패키지), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 주장하지 않는다."
        ),
    )
    write_md(CURRENT_STATE, current)

    workspace = io_path(WORKSPACE_STATE).read_text(encoding="utf-8-sig")
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    workspace = replace_line_prefix(workspace, "active_stage:", f"active_stage: {STAGE278_ID}")
    focus = (
        "- >-\n"
        f"  Stage278(278단계) run278B(278B 실행) fresh thesis MT5 probe payload materialization(새 논제 MT5 탐침 페이로드 물질화) `{RUN_ID}`. "
        f"Effect(효과): payload parquet(페이로드 파케이) `{payload_count}`개와 MT5 probe queue(MT5 탐침 대기열) `{queue_count}`행을 만들었고 selected candidate(선택 후보), Adapter package(어댑터 패키지), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 주장하지 않는다.\n"
    )
    workspace = prepend_focus(workspace, focus, "Stage278(278단계) run278B(278B 실행)")
    write_text(WORKSPACE_STATE, workspace)

    changelog = io_path(CHANGELOG).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG) else "# Changelog(변경 기록)\n"
    changelog = append_once(
        changelog,
        RUN_ID,
        (
            "## 2026-05-23 run278B Fresh thesis MT5 probe payload materialization(새 논제 MT5 탐침 페이로드 물질화)\n\n"
            f"- status(상태): `{STATUS}`\n"
            f"- judgment(판정): `{JUDGMENT}`\n"
            f"- effect(효과): payload parquet(페이로드 파케이) `{payload_count}`개와 MT5 probe queue(MT5 탐침 대기열) `{queue_count}`행을 만들었다.\n"
            "- boundary(경계): selected candidate(선택 후보), Adapter package(어댑터 패키지), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 `none/not_claimed`다.\n"
        ),
    )
    write_md(CHANGELOG, changelog)

    idea = io_path(IDEA_REGISTER).read_text(encoding="utf-8-sig") if path_exists(IDEA_REGISTER) else "# Idea Register(아이디어 등록부)\n"
    idea = append_once(
        idea,
        "IDEA-ST278-FRESH-THESIS-MT5-PROBE-RUN278B",
        f"| `IDEA-ST278-FRESH-THESIS-MT5-PROBE-RUN278B` | `{STAGE278_ID}` | run278A(278A 실행)의 MT5 probe design queue(MT5 탐침 설계 대기열)를 payload parquet(페이로드 파케이), handoff JSON(인계 JSON), MT5 signal CSV(MT5 신호 CSV)로 물질화한다. | `Tier A used + Tier B fallback stress + actual routed total(Tier A 사용 + Tier B 대체 스트레스 + 실제 라우팅 전체)` | `payload_materialized_no_candidate` | payload(페이로드) `{payload_count}`개, MT5 queue(MT5 대기열) `{queue_count}`행, selected candidate(선택 후보) 없음 |",
    )
    write_md(IDEA_REGISTER, idea)


def generated_artifacts() -> list[Path]:
    artifacts = [
        PROBE_PAYLOAD_MANIFEST,
        MT5_PROBE_QUEUE,
        PAYLOAD_READINESS,
        TIER_ROUTE_RECEIPT,
        PAYLOAD_SAMPLES,
        EXPERIMENT_RECEIPT,
        DATA_INTEGRITY_RECEIPT,
        RUNTIME_PARITY_RECEIPT,
        BACKTEST_FORENSICS_PLAN,
        RESULT_JUDGMENT,
        GATE_AUDIT,
        RUN_REPORT,
        STAGE_LEDGER,
        SELECTION_STATUS,
        RUN_MANIFEST,
        LINEAGE_RECEIPT,
    ]
    artifacts.extend(sorted(PAYLOAD_DIR.glob("*.parquet")))
    artifacts.extend(sorted(HANDOFF_DIR.glob("*.json")))
    artifacts.extend(sorted(MT5_DIR.glob("*.csv")))
    return artifacts


def build_manifest(
    created_at: str,
    manifest_rows: Sequence[Mapping[str, Any]],
    mt5_queue_rows: Sequence[Mapping[str, Any]],
    source_hashes: Mapping[str, str],
    artifacts: Sequence[Path],
) -> dict[str, Any]:
    payload = {
        "run_id": RUN_ID,
        "stage_id": STAGE278_ID,
        "source_run_id": SOURCE_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "created_at_utc": created_at,
        "producer": rel(PRODUCER_PATH),
        "entry_command": f"python {rel(PRODUCER_PATH)}",
        "source_inputs": list(source_hashes.keys()),
        "source_hashes": dict(source_hashes),
        "output_artifacts": [rel(path) for path in artifacts if path_exists(path)],
        "output_hashes": {rel(path): sha256_file(path) for path in artifacts if path_exists(path)},
        "payload_count": len(manifest_rows),
        "mt5_queue_rows": len(mt5_queue_rows),
        "selected_candidate": "none",
        "selected_research_baseline": "none",
        "adapter_package": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "external_verification_status": "out_of_scope_by_claim_payload_materialization_only",
        "claim_boundary": BOUNDARY,
        "next_action": NEXT_ACTION,
    }
    write_json(RUN_MANIFEST, payload)
    return payload


def write_lineage(manifest: Mapping[str, Any], artifacts: Sequence[Path]) -> None:
    lineage_artifacts = list(artifacts) + [RUN_MANIFEST, LINEAGE_RECEIPT, RUN_REPORT, REVIEW_INDEX, SELECTION_STATUS]
    payload = {
        "source_inputs": manifest["source_inputs"],
        "producer": manifest["producer"],
        "consumer": [NEXT_ACTION, rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
        "artifact_paths": [rel(path) for path in lineage_artifacts if path_exists(path)],
        "artifact_hashes": {rel(path): sha256_file(path) for path in lineage_artifacts if path_exists(path) and path != LINEAGE_RECEIPT},
        "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
        "availability": "tracked_generated_stage_local(추적되는 단계 로컬 생성)",
        "lineage_judgment": "connected_with_boundary(경계 포함 연결)",
        "runtime_claim_boundary": "runtime_probe_preparation_only(런타임 탐침 준비만 해당)",
        "claim_boundary": BOUNDARY,
    }
    write_json(LINEAGE_RECEIPT, payload)


def update_artifact_registry(created_at: str, artifacts: Sequence[Path]) -> None:
    artifact_rows = [
        {
            "artifact_id": f"{RUN_ID}__{rel(path).replace('/', '__').replace('.', '_')}",
            "artifact_type": "run278B_fresh_thesis_mt5_probe_payload_artifact",
            "path": rel(path),
            "sha256": sha256_file(path),
            "stage_id": STAGE278_ID,
            "run_id": RUN_ID,
            "created_at_utc": created_at,
            "notes": "run278B fresh thesis MT5 probe payload materialization artifact.",
        }
        for path in artifacts
        if path_exists(path)
    ]
    upsert_csv_rows(ARTIFACT_REGISTRY, ARTIFACT_COLUMNS, artifact_rows, key="artifact_id")


def run() -> dict[str, Any]:
    ensure_dirs()
    created_at = utc_now()
    queue_rows, branch_by_id, contract_by_id, tester_by_id = load_inputs()
    manifest_rows, mt5_queue_rows, tier_rows, samples, source_hashes = materialize_payloads(
        queue_rows,
        branch_by_id,
        contract_by_id,
        tester_by_id,
    )
    write_stage_outputs(manifest_rows, mt5_queue_rows, tier_rows, samples, source_hashes)
    write_md(RUN_REPORT, report_markdown(manifest_rows, mt5_queue_rows))
    update_ledgers(manifest_rows, mt5_queue_rows)
    update_state_docs(len(manifest_rows), len(mt5_queue_rows))

    artifacts_without_manifest = [path for path in generated_artifacts() if path not in {RUN_MANIFEST, LINEAGE_RECEIPT}]
    manifest = build_manifest(created_at, manifest_rows, mt5_queue_rows, source_hashes, artifacts_without_manifest)
    write_lineage(manifest, artifacts_without_manifest)
    final_artifacts = generated_artifacts()
    manifest = build_manifest(created_at, manifest_rows, mt5_queue_rows, source_hashes, final_artifacts)
    write_lineage(manifest, final_artifacts)
    update_artifact_registry(created_at, generated_artifacts())

    return {
        "run_id": RUN_ID,
        "stage_id": STAGE278_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "payload_count": len(manifest_rows),
        "mt5_queue_rows": len(mt5_queue_rows),
        "selected_candidate": "none",
        "adapter_package": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": NEXT_ACTION,
        "report": rel(RUN_REPORT),
    }


def main() -> int:
    print(json.dumps(run(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
