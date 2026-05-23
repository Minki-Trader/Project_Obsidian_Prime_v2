from __future__ import annotations

import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Sequence

import pandas as pd


STAGE_ID = "272_onnx_candidate_campaign__time_risk_router_pressure_probe"
RUN_ID = "run272B_materialize_time_risk_router_pressure_probe_payloads_v1"
SOURCE_RUN_ID = "run272A_design_time_risk_router_pressure_probe_packet_v1"
STATUS = "completed_time_risk_router_pressure_probe_payload_materialization_no_candidate_selection"
JUDGMENT = "pressure_probe_payloads_materialized_no_runtime_or_candidate_claim"
NEXT_ACTION = "run272C_execute_or_prepare_time_risk_router_mt5_probe"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_"
    "no_deployment_no_onnx_until_candidate_package_gate"
)

ROOT = Path(".")
STAGE = ROOT / "stages" / STAGE_ID
RUN272A = STAGE / "02_runs" / "run272A"
RUN_DIR = STAGE / "02_runs" / "run272B"
PAYLOAD_DIR = RUN_DIR / "payloads"
HANDOFF_DIR = RUN_DIR / "handoff"
MT5_DIR = RUN_DIR / "mt5_handoff"
REVIEWS = STAGE / "03_reviews"
SELECTED = STAGE / "04_selected"

BRANCH_PLAN = RUN272A / "pressure_branch_plan.csv"
BRANCH_SUPPLY = RUN272A / "branch_supply_metrics.csv"
WEAK_SLICE_MAP = RUN272A / "weak_slice_pressure_map.csv"
DESIGN_QUEUE = RUN272A / "mt5_probe_design_queue.csv"
RUN272A_MANIFEST = RUN272A / "run_manifest.json"
RUN272A_LINEAGE = RUN272A / "artifact_lineage_receipt.json"

SOURCE_SCORE_TABLE = (
    ROOT
    / "stages"
    / "271_onnx_candidate_campaign__fresh_edge_rebuild_after_nonfilter_failure"
    / "02_runs"
    / "run271D"
    / "scores"
    / "cp271B_fresh_edge_scores.parquet"
)
SUPPORT_SCORE_TABLE = (
    ROOT
    / "stages"
    / "271_onnx_candidate_campaign__fresh_edge_rebuild_after_nonfilter_failure"
    / "02_runs"
    / "run271D"
    / "scores"
    / "cp271D_fresh_edge_scores.parquet"
)
SOURCE_HANDOFF = (
    ROOT
    / "stages"
    / "271_onnx_candidate_campaign__fresh_edge_rebuild_after_nonfilter_failure"
    / "02_runs"
    / "run271D"
    / "handoff"
    / "cp271B.json"
)
SUPPORT_HANDOFF = (
    ROOT
    / "stages"
    / "271_onnx_candidate_campaign__fresh_edge_rebuild_after_nonfilter_failure"
    / "02_runs"
    / "run271D"
    / "handoff"
    / "cp271D.json"
)

PROBE_PAYLOAD_MANIFEST = RUN_DIR / "probe_payload_manifest.csv"
MT5_PROBE_QUEUE = RUN_DIR / "mt5_probe_queue.csv"
PAYLOAD_READINESS = RUN_DIR / "payload_readiness_receipt.csv"
TIER_RECEIPT = RUN_DIR / "tier_receipt.csv"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment_design_receipt.json"
DATA_INTEGRITY_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_VALIDATION_RECEIPT = RUN_DIR / "model_validation_receipt.json"
RESULT_JUDGMENT = RUN_DIR / "result_judgment.csv"
PAYLOAD_SAMPLES = RUN_DIR / "payload_samples.json"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"
LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
RUN_REPORT = REVIEWS / "run272B_report.md"
REVIEW_INDEX = REVIEWS / "review_index.md"
STAGE_LEDGER = REVIEWS / "stage_run_ledger.csv"
SELECTION_STATUS = SELECTED / "selection_status.md"

RUN_REGISTRY = ROOT / "docs" / "registers" / "run_registry.csv"
ALPHA_LEDGER = ROOT / "docs" / "registers" / "alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs" / "registers" / "artifact_registry.csv"
IDEA_REGISTER = ROOT / "docs" / "registers" / "idea_registry.md"
CURRENT_STATE = ROOT / "docs" / "context" / "current_working_state.md"
WORKSPACE_STATE = ROOT / "docs" / "workspace" / "workspace_state.yaml"
CHANGELOG = ROOT / "docs" / "workspace" / "changelog.md"

LABEL_OR_FUTURE_PREFIXES = ("label", "future_")
LABEL_PAYLOAD_EXCLUDE = {
    "label",
    "label_alignment_flag",
    "evaluation_label_available",
    "future_log_return_12",
    "future_timestamp",
    "horizon_bars",
    "horizon_minutes",
}
KEY_COLUMNS = ["timestamp", "symbol", "split", "tier_view"]

MANIFEST_COLUMNS = [
    "variant_id",
    "queue_id",
    "queue_role",
    "variant_role",
    "materialization_judgment",
    "next_queue_action",
    "payload_path",
    "payload_hash",
    "handoff_path",
    "handoff_hash",
    "mt5_tier_a_signal_path",
    "mt5_tier_a_signal_hash",
    "decision_surface_hash",
    "tier_a_oos_decision_count",
    "tier_a_oos_decision_rate",
    "selected_candidate",
    "onnx_readiness",
    "performance_claim",
]
MT5_QUEUE_COLUMNS = [
    "queue_id",
    "variant_id",
    "queue_role",
    "payload_path",
    "handoff_path",
    "mt5_tier_a_signal_path",
    "feature_order_hash",
    "decision_surface_hash",
    "signal_policy",
    "required_before_external_claim",
    "claim_boundary",
]
TIER_RECEIPT_COLUMNS = [
    "variant_id",
    "tier_view",
    "split",
    "rows",
    "decision_count",
    "decision_rate",
    "long_signal_count",
    "short_signal_count",
    "support_identity_match_rate",
    "claim_boundary",
]
READINESS_COLUMNS = ["check_name", "status", "effect"]
RESULT_COLUMNS = [
    "result_subject",
    "evidence_available",
    "evidence_missing",
    "judgment_label",
    "claim_boundary",
    "next_condition",
    "user_explanation_hook",
]
RUN_REGISTRY_COLUMNS = ["run_id", "stage_id", "lane", "status", "judgment", "path", "notes"]
ALPHA_LEDGER_COLUMNS = [
    "ledger_row_id",
    "stage_id",
    "run_id",
    "subrun_id",
    "parent_run_id",
    "record_view",
    "tier_scope",
    "kpi_scope",
    "scoreboard_lane",
    "status",
    "judgment",
    "path",
    "primary_kpi",
    "guardrail_kpi",
    "external_verification_status",
    "notes",
]
STAGE_LEDGER_COLUMNS = [
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
]
ARTIFACT_COLUMNS = [
    "artifact_id",
    "artifact_type",
    "path",
    "sha256",
    "stage_id",
    "run_id",
    "created_at_utc",
    "notes",
]


def rel(path: Path) -> str:
    return path.as_posix()


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def ensure_dirs() -> None:
    for path in [RUN_DIR, PAYLOAD_DIR, HANDOFF_DIR, MT5_DIR, REVIEWS, SELECTED]:
        path.mkdir(parents=True, exist_ok=True)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], fieldnames: Sequence[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = path.with_name(path.name + ".tmp")
    with temp_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({name: row.get(name, "") for name in fieldnames})
    temp_path.replace(path)


def write_json(path: Path, payload: Mapping[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_md(path: Path, text: str) -> None:
    path.write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8-sig") as f:
        return json.load(f)


def must_exist(paths: Sequence[Path]) -> None:
    missing = [rel(path) for path in paths if not path.exists()]
    if missing:
        raise FileNotFoundError("Missing required input artifacts: " + "; ".join(missing))


def upsert_csv_rows(path: Path, fieldnames: Sequence[str], rows: Sequence[Mapping[str, Any]], key: str) -> None:
    existing = read_csv_rows(path) if path.exists() else []
    by_key = {row.get(key, ""): row for row in existing if row.get(key, "")}
    for row in rows:
        by_key[str(row[key])] = {name: str(row.get(name, "")) for name in fieldnames}
    write_csv(path, list(by_key.values()), fieldnames)


def append_once(text: str, marker: str, block: str) -> str:
    if marker in text:
        return text
    return text.rstrip() + "\n\n" + block.rstrip() + "\n"


def replace_line_prefix(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + replacement + "\n"


def replace_section(text: str, heading: str, block: str) -> str:
    lines = text.splitlines()
    try:
        start = lines.index(heading)
    except ValueError:
        return text.rstrip() + "\n\n" + heading + "\n\n" + block.rstrip() + "\n"
    end = len(lines)
    for index in range(start + 1, len(lines)):
        if lines[index].startswith("## "):
            end = index
            break
    replacement = [heading, "", *block.rstrip().splitlines(), ""]
    return "\n".join([*lines[:start], *replacement, *lines[end:]]).rstrip() + "\n"


def remove_focus_items(text: str, marker: str) -> str:
    lines = text.splitlines()
    try:
        start = lines.index("current_focus:")
    except ValueError:
        return text
    end = len(lines)
    for index in range(start + 1, len(lines)):
        line = lines[index]
        if line and not line.startswith((" ", "-")):
            end = index
            break
    focus_lines = lines[start + 1:end]
    kept: list[str] = []
    index = 0
    while index < len(focus_lines):
        line = focus_lines[index]
        if not line.startswith("- >-"):
            kept.append(line)
            index += 1
            continue
        block_end = index + 1
        while block_end < len(focus_lines) and not focus_lines[block_end].startswith("- >-"):
            block_end += 1
        block = focus_lines[index:block_end]
        if not any(marker in block_line for block_line in block):
            kept.extend(block)
        index = block_end
    return "\n".join([*lines[: start + 1], *kept, *lines[end:]]).rstrip() + "\n"


def prepend_focus(text: str, block: str) -> str:
    marker = "current_focus:\n"
    if block.strip() in text or marker not in text:
        return text
    return text.replace(marker, marker + block, 1)


def json_ready(payload: Mapping[str, Any]) -> dict[str, Any]:
    output: dict[str, Any] = {}
    for key, value in payload.items():
        if hasattr(value, "item"):
            output[key] = value.item()
        else:
            output[key] = value
    return output


def short_variant_id(variant_id: str) -> str:
    parts = variant_id.split("_")
    return parts[1] if len(parts) > 1 and parts[1].startswith("q") else variant_id.replace("run272A_", "", 1)


def safe_rate(numerator: float, denominator: float) -> float:
    return round(float(numerator) / float(denominator), 8) if denominator else 0.0


def branch_mask(df: pd.DataFrame, variant: Mapping[str, Any]) -> pd.Series:
    thresholds = json.loads(str(variant["thresholds_json"]))
    variant_id = str(variant["variant_id"])
    if variant_id == "run272A_q01_base_router_reference":
        return df["materialized_decision_flag"].astype(int).eq(1)
    if variant_id == "run272A_q02_oos_alignment_tight_router":
        return (
            df["candidate_decision_score"].ge(thresholds["decision_min"])
            & df["phase_opportunity_score"].ge(thresholds["opportunity_min"])
            & df["phase_risk_score"].le(thresholds["risk_max"])
            & df["session_clock_risk"].le(thresholds["session_max"])
        )
    if variant_id == "run272A_q03_route_mix_rebalance_router":
        return (
            df["candidate_decision_score"].ge(thresholds["decision_min"])
            & df["phase_opportunity_score"].ge(thresholds["opportunity_min"])
            & df["phase_risk_score"].le(thresholds["risk_max"])
        )
    if variant_id == "run272A_q04_weak_clock_throttle_router":
        return (
            df["candidate_decision_score"].ge(thresholds["decision_min"])
            & df["phase_opportunity_score"].ge(thresholds["opportunity_min"])
            & df["session_clock_risk"].le(thresholds["session_max"])
            & df["weekday_phase"].ne(thresholds["blocked_weekday_phase"])
        )
    raise ValueError(f"run272B only materializes queued run272A variants, got {variant_id}")


def source_paths() -> list[Path]:
    return [
        BRANCH_PLAN,
        BRANCH_SUPPLY,
        WEAK_SLICE_MAP,
        DESIGN_QUEUE,
        RUN272A_MANIFEST,
        RUN272A_LINEAGE,
        SOURCE_SCORE_TABLE,
        SUPPORT_SCORE_TABLE,
        SOURCE_HANDOFF,
        SUPPORT_HANDOFF,
        SELECTION_STATUS,
    ]


def load_inputs() -> tuple[pd.DataFrame, pd.DataFrame, list[dict[str, str]], dict[str, dict[str, str]], dict[str, Any], dict[str, Any]]:
    must_exist(source_paths())
    queue = read_csv_rows(DESIGN_QUEUE)
    branches = {row["variant_id"]: row for row in read_csv_rows(BRANCH_PLAN)}
    queued_variants = []
    for row in queue:
        if row.get("materialization_status") != "ready_for_run272B_payload_materialization":
            continue
        variant_id = row["variant_id"]
        if variant_id not in branches:
            raise ValueError(f"Queue variant missing from branch plan: {variant_id}")
        merged = dict(branches[variant_id])
        merged.update(
            {
                "queue_id": row["queue_id"],
                "queue_role": row["queue_role"],
                "mt5_probe_question": row["mt5_probe_question"],
                "success_condition": row["success_condition"],
                "discard_condition": row["discard_condition"],
                "required_evidence": row["required_evidence"],
            }
        )
        queued_variants.append(merged)
    if len(queued_variants) != 4:
        raise ValueError(f"Expected 4 queued run272B variants, got {len(queued_variants)}")

    cp271b = pd.read_parquet(SOURCE_SCORE_TABLE)
    cp271d = pd.read_parquet(SUPPORT_SCORE_TABLE)
    for name, frame in {"source": cp271b, "support": cp271d}.items():
        missing = [column for column in KEY_COLUMNS if column not in frame.columns]
        if missing:
            raise ValueError(f"{name} score table missing key columns: {missing}")
        if frame.duplicated(KEY_COLUMNS).any():
            raise ValueError(f"{name} score table has duplicated timestamp/symbol/split/tier rows")
        frame["timestamp"] = pd.to_datetime(frame["timestamp"], utc=True)

    required_source = {
        "candidate_decision_score",
        "phase_opportunity_score",
        "phase_risk_score",
        "session_clock_risk",
        "month_regime_pressure",
        "chron_phase_age",
        "weekday_phase",
        "risk_action_code",
        "route_code",
        "materialized_decision_flag",
        "input_feature_order_hash",
        "expected_feature_order_hash",
        "missing_required_feature_count",
    }
    missing_source = sorted(required_source.difference(cp271b.columns))
    if missing_source:
        raise ValueError(f"cp271B score table missing required columns: {missing_source}")
    return cp271b, cp271d, queued_variants, branches, load_json(SOURCE_HANDOFF), load_json(SUPPORT_HANDOFF)


def support_identity_map(cp271d: pd.DataFrame) -> pd.DataFrame:
    support = cp271d[KEY_COLUMNS + [
        "package_id",
        "input_feature_order_hash",
        "expected_feature_order_hash",
        "missing_required_feature_count",
        "decision_rule_hash",
        "risk_rule_hash",
        "adapter_schema_hash",
        "score_columns_hash",
    ]].copy()
    support["support_identity_match_flag"] = (
        support["input_feature_order_hash"].eq(support["expected_feature_order_hash"])
        & pd.to_numeric(support["missing_required_feature_count"], errors="coerce").fillna(999).eq(0)
    ).astype("int8")
    return support.rename(
        columns={
            "package_id": "support_package_id",
            "input_feature_order_hash": "support_input_feature_order_hash",
            "expected_feature_order_hash": "support_expected_feature_order_hash",
            "missing_required_feature_count": "support_missing_required_feature_count",
            "decision_rule_hash": "support_decision_rule_hash",
            "risk_rule_hash": "support_risk_rule_hash",
            "adapter_schema_hash": "support_adapter_schema_hash",
            "score_columns_hash": "support_score_columns_hash",
        }
    )


def payload_base_columns(df: pd.DataFrame) -> list[str]:
    excluded = {
        column
        for column in df.columns
        if column in LABEL_PAYLOAD_EXCLUDE or column.startswith(LABEL_OR_FUTURE_PREFIXES)
    }
    return [column for column in df.columns if column not in excluded]


def route_signal(row: pd.Series) -> int:
    if int(row["variant_decision_flag"]) != 1:
        return 0
    if row["route_code"] == "long":
        return 1
    if row["route_code"] == "short":
        return -1
    return 0


def materialization_judgment(queue_role: str) -> tuple[str, str]:
    if queue_role == "reference_control_payload":
        return "reference_payload_materialized_no_candidate_claim", "include_as_control"
    if queue_role == "primary_pressure_payload":
        return "primary_pressure_payload_materialized_no_candidate_claim", "include_for_mt5_probe"
    if queue_role == "route_mix_payload":
        return "route_mix_payload_materialized_no_candidate_claim", "include_for_mt5_probe"
    if queue_role == "weak_slice_throttle_payload":
        return "weak_slice_throttle_payload_materialized_no_candidate_claim", "include_for_mt5_probe"
    return "unknown_payload_role_materialized_with_boundary", "hold_for_manual_review"


def counts_by_tier_split(payload: pd.DataFrame, variant_id: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for (tier_view, split), group in payload.groupby(["tier_view", "split"], dropna=False):
        decision_count = int(group["variant_decision_flag"].sum())
        rows.append(
            {
                "variant_id": variant_id,
                "tier_view": tier_view,
                "split": split,
                "rows": len(group),
                "decision_count": decision_count,
                "decision_rate": safe_rate(decision_count, len(group)),
                "long_signal_count": int(group["route_signal_value"].eq(1).sum()),
                "short_signal_count": int(group["route_signal_value"].eq(-1).sum()),
                "support_identity_match_rate": safe_rate(group["support_identity_match_flag"].sum(), len(group)),
                "claim_boundary": BOUNDARY,
            }
        )
    return rows


def materialize_payloads(
    cp271b: pd.DataFrame,
    cp271d: pd.DataFrame,
    variants: Sequence[Mapping[str, str]],
    source_handoff: Mapping[str, Any],
    support_handoff: Mapping[str, Any],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    support = support_identity_map(cp271d)
    base_columns = payload_base_columns(cp271b)
    manifest_rows: list[dict[str, Any]] = []
    queue_rows: list[dict[str, Any]] = []
    tier_rows: list[dict[str, Any]] = []
    samples: dict[str, Any] = {}

    for variant in variants:
        variant_id = str(variant["variant_id"])
        token = short_variant_id(variant_id)
        mask = branch_mask(cp271b, variant)
        payload = cp271b[base_columns].copy()
        payload["variant_id"] = variant_id
        payload["source_run_id"] = SOURCE_RUN_ID
        payload["run272b_queue_id"] = variant["queue_id"]
        payload["queue_role"] = variant["queue_role"]
        payload["variant_role"] = variant["variant_role"]
        payload["variant_decision_flag"] = mask.astype("int8")
        payload["route_signal_value"] = payload.apply(route_signal, axis=1).astype("int8")
        payload["route_signal_label"] = payload["route_signal_value"].map({1: "long", -1: "short", 0: "flat"})
        payload["payload_claim_boundary"] = BOUNDARY
        payload = payload.merge(support, on=KEY_COLUMNS, how="left")
        payload["support_identity_match_flag"] = payload["support_identity_match_flag"].fillna(0).astype("int8")

        decision_surface_hash = sha256_text(
            json.dumps(
                json_ready(
                    {
                        "variant_id": variant_id,
                        "decision_rule": variant["decision_rule"],
                        "thresholds_json": variant["thresholds_json"],
                        "source_feature_order_hash": source_handoff["feature_order_hash"],
                    }
                ),
                ensure_ascii=False,
                sort_keys=True,
            )
        )
        payload["variant_decision_surface_hash"] = decision_surface_hash
        payload["source_model_hash"] = source_handoff["model_hash"]
        payload["source_adapter_schema_hash"] = source_handoff["adapter_schema_hash"]
        payload["source_feature_order_hash"] = source_handoff["feature_order_hash"]

        payload_path = PAYLOAD_DIR / f"{token}_payload.parquet"
        payload.to_parquet(payload_path, index=False)

        tier_a = payload[payload["tier_view"].eq("Tier A separate")].copy()
        tier_a["timestamp"] = tier_a["timestamp"].dt.strftime("%Y-%m-%dT%H:%M:%SZ")
        mt5_path = MT5_DIR / f"{token}_tier_a_signals.csv"
        tier_a[
            [
                "timestamp",
                "symbol",
                "split",
                "variant_id",
                "variant_decision_flag",
                "route_signal_value",
                "route_signal_label",
                "route_code",
                "risk_action_code",
                "candidate_decision_score",
                "phase_opportunity_score",
                "phase_risk_score",
                "session_clock_risk",
                "month_regime_pressure",
                "support_identity_match_flag",
            ]
        ].to_csv(mt5_path, index=False, lineterminator="\n")

        local_tier_rows = counts_by_tier_split(payload, variant_id)
        tier_rows.extend(local_tier_rows)
        tier_a_oos = next(
            row
            for row in local_tier_rows
            if row["tier_view"] == "Tier A separate" and row["split"] == "oos"
        )
        judgment, next_queue_action = materialization_judgment(str(variant["queue_role"]))
        handoff_payload = {
            "run_id": RUN_ID,
            "stage_id": STAGE_ID,
            "source_run_id": SOURCE_RUN_ID,
            "variant_id": variant_id,
            "queue_id": variant["queue_id"],
            "queue_role": variant["queue_role"],
            "variant_role": variant["variant_role"],
            "materialization_judgment": judgment,
            "next_queue_action": next_queue_action,
            "source_package": source_handoff["package_id"],
            "support_control": support_handoff["package_id"],
            "decision_rule": variant["decision_rule"],
            "thresholds": json.loads(str(variant["thresholds_json"])),
            "decision_surface_hash": decision_surface_hash,
            "feature_order_hash": source_handoff["feature_order_hash"],
            "model_hash": source_handoff["model_hash"],
            "adapter_schema_hash": source_handoff["adapter_schema_hash"],
            "support_adapter_schema_hash": support_handoff["adapter_schema_hash"],
            "payload_path": rel(payload_path),
            "payload_hash": sha256_file(payload_path),
            "mt5_tier_a_signal_path": rel(mt5_path),
            "mt5_tier_a_signal_hash": sha256_file(mt5_path),
            "tier_view_counts": {
                f"{row['tier_view']}|{row['split']}": {
                    "rows": row["rows"],
                    "decision_count": row["decision_count"],
                    "decision_rate": row["decision_rate"],
                    "long_signal_count": row["long_signal_count"],
                    "short_signal_count": row["short_signal_count"],
                    "support_identity_match_rate": row["support_identity_match_rate"],
                }
                for row in local_tier_rows
            },
            "signal_policy": "variant_decision_flag(분기 판단 플래그)이 1이면 route_code(경로 코드)를 구조 신호로 보존하고, MT5 replay policy(MT5 재생 정책)는 run272C에서 확정한다.",
            "label_payload_policy": "label/future columns(라벨/미래 열)은 payload parquet(페이로드 파케이)와 MT5 signal CSV(MT5 신호 CSV)에서 제외했다.",
            "selected_candidate": "none",
            "onnx_readiness": "not_claimed",
            "goal_achieve": "not_claimed",
            "claim_boundary": BOUNDARY,
        }
        handoff_path = HANDOFF_DIR / f"{token}.json"
        write_json(handoff_path, handoff_payload)

        manifest_rows.append(
            {
                "variant_id": variant_id,
                "queue_id": variant["queue_id"],
                "queue_role": variant["queue_role"],
                "variant_role": variant["variant_role"],
                "materialization_judgment": judgment,
                "next_queue_action": next_queue_action,
                "payload_path": rel(payload_path),
                "payload_hash": sha256_file(payload_path),
                "handoff_path": rel(handoff_path),
                "handoff_hash": sha256_file(handoff_path),
                "mt5_tier_a_signal_path": rel(mt5_path),
                "mt5_tier_a_signal_hash": sha256_file(mt5_path),
                "decision_surface_hash": decision_surface_hash,
                "tier_a_oos_decision_count": tier_a_oos["decision_count"],
                "tier_a_oos_decision_rate": tier_a_oos["decision_rate"],
                "selected_candidate": "none",
                "onnx_readiness": "not_claimed",
                "performance_claim": "none",
            }
        )
        queue_rows.append(
            {
                "queue_id": f"run272C_{token}",
                "variant_id": variant_id,
                "queue_role": "control_reference" if next_queue_action == "include_as_control" else "active_pressure_probe",
                "payload_path": rel(payload_path),
                "handoff_path": rel(handoff_path),
                "mt5_tier_a_signal_path": rel(mt5_path),
                "feature_order_hash": source_handoff["feature_order_hash"],
                "decision_surface_hash": decision_surface_hash,
                "signal_policy": "route_preserving_structural_signal_pending_run272C_replay_policy",
                "required_before_external_claim": "MT5 runtime output;trade list;balance/equity curve;time-slice KPI",
                "claim_boundary": BOUNDARY,
            }
        )
        sample = payload[
            [
                "timestamp",
                "split",
                "tier_view",
                "variant_decision_flag",
                "route_signal_value",
                "candidate_decision_score",
                "phase_opportunity_score",
                "phase_risk_score",
                "support_identity_match_flag",
            ]
        ].head(3).copy()
        sample["timestamp"] = sample["timestamp"].dt.strftime("%Y-%m-%dT%H:%M:%SZ")
        samples[variant_id] = sample.to_dict("records")

    return manifest_rows, queue_rows, tier_rows, samples


def experiment_receipt(payload_count: int, queue_count: int) -> dict[str, Any]:
    return {
        "hypothesis": "time-risk router(시간 위험 라우터) 압박 분기를 label-free payload(라벨 없는 페이로드)로 만들면 run272C(272C 실행) MT5 probe(MT5 탐침)를 좁게 준비할 수 있다.",
        "decision_use": "run272C_execute_or_prepare_time_risk_router_mt5_probe 실행 여부와 입력 대상을 정한다.",
        "comparison_baseline": "run272A_q01_base_router_reference",
        "control_variables": "symbol=US100;timeframe=M5;source package=cp271B;support control=cp271D;feature_order_hash fixed",
        "changed_variables": "run272A pressure branch(압박 분기)를 payload parquet(페이로드 파케이), handoff JSON(인계 JSON), MT5 signal CSV(MT5 신호 CSV)로 물질화한다.",
        "sample_scope": "Tier A separate, Tier B separate, Tier A+B combined structural payload views; train/validation/oos splits",
        "success_criteria": "4 queued branches materialize with label columns dropped, support identity attached, and MT5 queue paths present.",
        "failure_criteria": "missing payload, feature order mismatch, support identity break, label/future columns in runtime handoff, or empty Tier A OOS signal supply.",
        "invalid_conditions": "source score table missing, branch thresholds unreadable, duplicate timestamp/symbol/split/tier rows, or MT5 CSV includes labels.",
        "stop_conditions": "Do not claim candidate, ONNX readiness, runtime authority, or trading KPI until run272C external/runtime evidence exists.",
        "evidence_plan": "probe_payload_manifest;mt5_probe_queue;tier_receipt;payload_readiness;handoff json;run_manifest;lineage;ledgers",
        "payload_count": payload_count,
        "mt5_queue_rows": queue_count,
        "claim_boundary": BOUNDARY,
    }


def data_integrity_receipt(
    cp271b: pd.DataFrame,
    cp271d: pd.DataFrame,
    input_hashes: Mapping[str, str],
) -> dict[str, Any]:
    dropped = sorted(
        column
        for column in cp271b.columns
        if column in LABEL_PAYLOAD_EXCLUDE or column.startswith(LABEL_OR_FUTURE_PREFIXES)
    )
    return {
        "data_source": rel(SOURCE_SCORE_TABLE),
        "support_source": rel(SUPPORT_SCORE_TABLE),
        "time_axis": "timestamp(타임스탬프)은 UTC closed M5 bar(UTC 마감 M5 봉)로 해석하고 정렬한다.",
        "sample_scope": {
            "symbol": sorted(cp271b["symbol"].dropna().unique().tolist()),
            "rows": int(len(cp271b)),
            "tier_views": sorted(cp271b["tier_view"].dropna().unique().tolist()),
            "splits": sorted(cp271b["split"].dropna().unique().tolist()),
            "start": str(cp271b["timestamp"].min()),
            "end": str(cp271b["timestamp"].max()),
        },
        "missing_or_duplicate_check": {
            "source_duplicate_key_rows": int(cp271b.duplicated(KEY_COLUMNS).sum()),
            "support_duplicate_key_rows": int(cp271d.duplicated(KEY_COLUMNS).sum()),
            "source_missing_required_feature_count_max": int(cp271b["missing_required_feature_count"].max()),
        },
        "feature_label_boundary": "label/future columns(라벨/미래 열)은 branch mask(분기 마스크) 계산과 runtime handoff(런타임 인계)에 쓰지 않고 payload에서 제거했다.",
        "split_boundary": "train/validation/oos split(학습/검증/표본외 분할)은 run271D score table(271D 점수표)을 그대로 보존한다.",
        "leakage_risk": "run272A alignment read(정렬 판독)를 이미 보고 난 뒤 payload를 고르는 selection bias(선택 편향)가 남아 있어 candidate claim(후보 주장)은 금지한다.",
        "label_columns_dropped_from_payload": dropped,
        "data_hash_or_identity": dict(input_hashes),
        "integrity_judgment": "usable_with_boundary",
    }


def model_validation_receipt(payload_count: int) -> dict[str, Any]:
    return {
        "model_family": "fixed cp271B score surface(고정 cp271B 점수 표면); no new model training(새 모델 학습 없음)",
        "target_and_label": "label(라벨)은 payload(페이로드)에 포함하지 않으며 previous alignment read(이전 정렬 판독)에만 쓰였다.",
        "split_method": "frozen train/validation/oos split(고정 학습/검증/표본외 분할)",
        "selection_metric": "materialization readiness(물질화 준비), OOS supply floor(표본외 공급 바닥), support identity(보조 정체성)",
        "secondary_metrics": "decision_rate, route_signal mix, support_identity_match_rate, missing_required_feature_count",
        "threshold_policy": "run272A train-quantile thresholds(272A 학습 분위수 임계값)을 그대로 소비한다.",
        "overfit_risk": "multiple pressure branches(다중 압박 분기)를 본 뒤 4개만 물질화했으므로 selection bias(선택 편향)가 있다.",
        "calibration_risk": "candidate_decision_score(후보 판단 점수)는 probability(확률)가 아니라 rank-like score(순위형 점수)다.",
        "comparison_baseline": "run272A_q01_base_router_reference",
        "payload_count": payload_count,
        "validation_judgment": "payload_materialized_no_candidate_selection",
        "claim_boundary": BOUNDARY,
    }


def result_rows(payload_count: int, queue_count: int) -> list[dict[str, str]]:
    return [
        {
            "result_subject": "run272B time-risk router payload materialization(272B 시간 위험 라우터 페이로드 물질화)",
            "evidence_available": "payload parquet;handoff json;MT5 signal CSV;tier receipt;readiness receipt;manifest;lineage",
            "evidence_missing": "MT5 runtime output;trade list;balance/equity curve;trading KPI;Adapter package;ONNX export/parity",
            "judgment_label": "payload_materialized_no_candidate_selection",
            "claim_boundary": BOUNDARY,
            "next_condition": NEXT_ACTION,
            "user_explanation_hook": f"{payload_count}개 payload(페이로드)와 {queue_count}개 MT5 queue(탐침 대기열)를 만들었지만 후보나 ONNX 준비는 아니다.",
        }
    ]


def write_stage_outputs(
    manifest_rows: Sequence[Mapping[str, Any]],
    queue_rows: Sequence[Mapping[str, Any]],
    tier_rows: Sequence[Mapping[str, Any]],
    samples: Mapping[str, Any],
    cp271b: pd.DataFrame,
    cp271d: pd.DataFrame,
    input_hashes: Mapping[str, str],
) -> None:
    write_csv(PROBE_PAYLOAD_MANIFEST, manifest_rows, MANIFEST_COLUMNS)
    write_csv(MT5_PROBE_QUEUE, queue_rows, MT5_QUEUE_COLUMNS)
    write_csv(TIER_RECEIPT, tier_rows, TIER_RECEIPT_COLUMNS)
    write_csv(
        PAYLOAD_READINESS,
        [
            {
                "check_name": "queued_payloads_materialized",
                "status": "passed",
                "effect": f"payloads={len(manifest_rows)};mt5_queue_rows={len(queue_rows)}",
            },
            {
                "check_name": "label_columns_removed",
                "status": "passed",
                "effect": "label/future columns(라벨/미래 열)을 payload parquet(페이로드 파케이)와 MT5 signal CSV(MT5 신호 CSV)에서 제거했다.",
            },
            {
                "check_name": "support_identity_attached",
                "status": "passed",
                "effect": "cp271D support control(보조 대조)을 timestamp/symbol/split/tier key(키)로 붙였다.",
            },
            {
                "check_name": "performance_claim_boundary",
                "status": "out_of_scope_by_claim",
                "effect": "MT5 runtime output(MT5 런타임 출력)과 trading KPI(거래 KPI)는 아직 없다.",
            },
        ],
        READINESS_COLUMNS,
    )
    write_json(PAYLOAD_SAMPLES, samples)
    write_json(EXPERIMENT_RECEIPT, experiment_receipt(len(manifest_rows), len(queue_rows)))
    write_json(DATA_INTEGRITY_RECEIPT, data_integrity_receipt(cp271b, cp271d, input_hashes))
    write_json(MODEL_VALIDATION_RECEIPT, model_validation_receipt(len(manifest_rows)))
    write_csv(RESULT_JUDGMENT, result_rows(len(manifest_rows), len(queue_rows)), RESULT_COLUMNS)


def report_markdown(manifest_rows: Sequence[Mapping[str, Any]], queue_rows: Sequence[Mapping[str, Any]]) -> str:
    rows = "\n".join(
        f"- `{row['variant_id']}`: role(역할) `{row['queue_role']}`, Tier A OOS decision_rate(Tier A 표본외 판단 비율) `{row['tier_a_oos_decision_rate']}`, judgment(판정) `{row['materialization_judgment']}`"
        for row in manifest_rows
    )
    queue = "\n".join(
        f"- `{row['queue_id']}` -> `{row['variant_id']}`: `{row['queue_role']}`"
        for row in queue_rows
    )
    return f"""# run272B Time-Risk Router Payload Materialization(272B 시간 위험 라우터 페이로드 물질화)

- run_id(실행 ID): `{RUN_ID}`
- status(상태): `{STATUS}`
- judgment(판정): `{JUDGMENT}`
- payload_count(페이로드 수): `{len(manifest_rows)}`
- mt5_queue_rows(MT5 탐침 대기열 행): `{len(queue_rows)}`
- selected_candidate(선택 후보): `none`
- ONNX readiness(온엑스 준비): `not_claimed`
- Goal Achieve(목표 달성): `not_claimed`
- next_action(다음 행동): `{NEXT_ACTION}`

## Plain Result(쉬운 결과)

run272B(272B 실행)는 run272A(272A 실행)의 queued pressure branches(대기 중 압박 분기)를 payload parquet(페이로드 파케이), handoff JSON(인계 제이슨), MT5 signal CSV(MT5 신호 CSV)로 물질화했다.
효과(effect, 효과): run272C(272C 실행)가 MT5(`MetaTrader 5`, 메타트레이더5) runtime probe(런타임 탐침)를 준비하거나 실행할 수 있는 파일 단위가 생겼다.

## Materialized Payloads(물질화된 페이로드)

{rows}

## MT5 Probe Queue(MT5 탐침 대기열)

{queue}

## Gate Coverage(게이트 커버리지)

- experiment_design(실험 설계): hypothesis/comparison/control/evidence plan(가설/비교/고정/근거 계획)을 receipt(영수증)에 기록했다.
- data_integrity(데이터 무결성): label/future columns(라벨/미래 열)을 payload(페이로드)와 MT5 signal CSV(MT5 신호 CSV)에서 제거했다.
- model_validation(모델 검증): 새 training(학습) 없이 fixed score surface(고정 점수 표면)를 물질화한 범위로 제한했다.
- artifact_lineage(산출물 계보): source inputs(원천 입력), producer(생산자), consumer(소비자), hashes(해시), registry links(등록부 연결)를 기록했다.
- result_judgment(결과 판정): payload materialized(페이로드 물질화)만 말하고 candidate/ONNX/runtime claim(후보/온엑스/런타임 주장)은 열지 않는다.

## Boundary(경계)

`{BOUNDARY}`
"""


def update_ledgers(manifest_rows: Sequence[Mapping[str, Any]], queue_rows: Sequence[Mapping[str, Any]]) -> None:
    payload_count = len(manifest_rows)
    queue_count = len(queue_rows)
    upsert_csv_rows(
        STAGE_LEDGER,
        STAGE_LEDGER_COLUMNS,
        [
            {
                "row_id": f"{RUN_ID}__tier_a_payload",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "view": "time_risk_router_payload_materialization",
                "tier_scope": "Tier A separate",
                "scoreboard": "structural_payload_materialization",
                "status": STATUS,
                "judgment": JUDGMENT,
                "evidence_boundary": "payload_materialization_only_no_runtime_kpi",
                "report_path": rel(RUN_REPORT),
                "notes": f"payload_count={payload_count};mt5_queue_rows={queue_count};Tier A signal CSVs materialized.",
            },
            {
                "row_id": f"{RUN_ID}__tier_b_payload",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "view": "time_risk_router_payload_materialization",
                "tier_scope": "Tier B separate",
                "scoreboard": "structural_payload_materialization",
                "status": STATUS,
                "judgment": JUDGMENT,
                "evidence_boundary": "tier_b_structural_payload_no_runtime_authority",
                "report_path": rel(RUN_REPORT),
                "notes": "Tier B partial-context rows are preserved as structural payload evidence only.",
            },
            {
                "row_id": f"{RUN_ID}__tier_ab_payload",
                "stage_id": STAGE_ID,
                "run_id": RUN_ID,
                "view": "time_risk_router_payload_materialization",
                "tier_scope": "Tier A+B combined",
                "scoreboard": "structural_payload_materialization",
                "status": STATUS,
                "judgment": JUDGMENT,
                "evidence_boundary": "combined_structural_view_no_routed_pnl_claim",
                "report_path": rel(RUN_REPORT),
                "notes": f"Combined view supports run272C input preparation; next_action={NEXT_ACTION}.",
            },
        ],
        key="row_id",
    )
    upsert_csv_rows(
        RUN_REGISTRY,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE_ID,
                "lane": "payload_materialization",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(RUN_REPORT),
                "notes": f"payload_count={payload_count};mt5_queue_rows={queue_count};selected_candidate=none;onnx_readiness=not_claimed;next_action={NEXT_ACTION}.",
            }
        ],
        key="run_id",
    )
    alpha_rows = [
        {
            "ledger_row_id": f"{RUN_ID}__tier_a_payload",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "tier_a_payload",
            "parent_run_id": SOURCE_RUN_ID,
            "record_view": "Tier A payload materialization(티어 A 페이로드 물질화)",
            "tier_scope": "Tier A separate",
            "kpi_scope": "payload_materialization_no_trading_kpi",
            "scoreboard_lane": "structural_payload_materialization",
            "status": STATUS,
            "judgment": JUDGMENT,
            "path": rel(PROBE_PAYLOAD_MANIFEST),
            "primary_kpi": f"payload_count={payload_count};mt5_queue_rows={queue_count}",
            "guardrail_kpi": "label_columns_removed=true;selected_candidate=none;onnx_readiness=not_claimed",
            "external_verification_status": "out_of_scope_by_claim_payload_materialization_only",
            "notes": "Tier A signal CSVs are prepared for run272C, not yet MT5 runtime evidence.",
        },
        {
            "ledger_row_id": f"{RUN_ID}__tier_b_payload",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "tier_b_payload",
            "parent_run_id": SOURCE_RUN_ID,
            "record_view": "Tier B payload materialization(티어 B 페이로드 물질화)",
            "tier_scope": "Tier B separate",
            "kpi_scope": "payload_materialization_no_trading_kpi",
            "scoreboard_lane": "structural_payload_materialization",
            "status": STATUS,
            "judgment": JUDGMENT,
            "path": rel(TIER_RECEIPT),
            "primary_kpi": f"payload_count={payload_count}",
            "guardrail_kpi": "tier_b_runtime_authority=not_claimed",
            "external_verification_status": "out_of_scope_by_claim_payload_materialization_only",
            "notes": "Tier B remains a paired structural context view.",
        },
        {
            "ledger_row_id": f"{RUN_ID}__tier_ab_payload",
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "subrun_id": "tier_ab_payload",
            "parent_run_id": SOURCE_RUN_ID,
            "record_view": "Tier A+B payload materialization(티어 A+B 페이로드 물질화)",
            "tier_scope": "Tier A+B combined",
            "kpi_scope": "payload_materialization_no_trading_kpi",
            "scoreboard_lane": "structural_payload_materialization",
            "status": STATUS,
            "judgment": JUDGMENT,
            "path": rel(TIER_RECEIPT),
            "primary_kpi": f"payload_count={payload_count};mt5_queue_rows={queue_count}",
            "guardrail_kpi": "combined_record_is_structural_not_routed_total",
            "external_verification_status": "out_of_scope_by_claim_payload_materialization_only",
            "notes": "Combined record is structural payload accounting only.",
        },
    ]
    upsert_csv_rows(ALPHA_LEDGER, ALPHA_LEDGER_COLUMNS, alpha_rows, key="ledger_row_id")


def build_manifest(
    created_at: str,
    manifest_rows: Sequence[Mapping[str, Any]],
    queue_rows: Sequence[Mapping[str, Any]],
    input_hashes: Mapping[str, str],
    artifacts: Sequence[Path],
) -> dict[str, Any]:
    payload = {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "source_run_id": SOURCE_RUN_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "created_at_utc": created_at,
        "producer": "stage_pipelines/stage272/materialize_time_risk_router_pressure_probe_payloads.py",
        "entry_command": "python stage_pipelines/stage272/materialize_time_risk_router_pressure_probe_payloads.py",
        "source_inputs": [rel(path) for path in source_paths()],
        "input_hashes": dict(input_hashes),
        "output_artifacts": [rel(path) for path in artifacts if path.exists()],
        "output_hashes": {rel(path): sha256_file(path) for path in artifacts if path.exists()},
        "payload_count": len(manifest_rows),
        "mt5_queue_rows": len(queue_rows),
        "selected_candidate": "none",
        "selected_research_baseline": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "external_verification_status": "out_of_scope_by_claim_payload_materialization_only",
        "claim_boundary": BOUNDARY,
        "next_action": NEXT_ACTION,
    }
    write_json(RUN_MANIFEST, payload)
    return payload


def update_state_docs(payload_count: int, queue_count: int) -> None:
    selection = SELECTION_STATUS.read_text(encoding="utf-8-sig")
    selection = replace_line_prefix(selection, "- stage_status(", f"- stage_status(단계 상태): `{STATUS}`")
    selection = replace_line_prefix(selection, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    selection = replace_line_prefix(selection, "- last_completed_run(", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
    selection = replace_line_prefix(selection, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    selection = replace_section(
        selection,
        "## Current Meaning(현재 의미)",
        f"run272B(272B 실행)는 run272A(272A 실행)의 MT5 probe design queue(MT5 탐침 설계 대기열) `4`행을 payload parquet(페이로드 파케이) `{payload_count}`개와 MT5 probe queue(MT5 탐침 대기열) `{queue_count}`행으로 물질화했다.\n효과(effect, 효과): run272C(272C 실행)가 MT5(`MetaTrader 5`, 메타트레이더5) runtime probe(런타임 탐침)를 준비하거나 실행할 수 있지만, 아직 candidate package(후보 패키지) 선택이나 ONNX readiness(온엑스 준비)는 없다.",
    )
    selection = append_once(selection, "run272B_payload_manifest", f"- run272B_payload_manifest(272B 페이로드 목록): `{rel(PROBE_PAYLOAD_MANIFEST)}`")
    selection = append_once(selection, "run272B_mt5_probe_queue", f"- run272B_mt5_probe_queue(272B MT5 탐침 대기열): `{rel(MT5_PROBE_QUEUE)}`")
    selection = append_once(selection, "run272B_report", f"- run272B_report(272B 보고): `{rel(RUN_REPORT)}`")
    write_md(SELECTION_STATUS, selection)

    review = REVIEW_INDEX.read_text(encoding="utf-8-sig")
    review = append_once(
        review,
        "run272B_report",
        f"- run272B_report(272B 보고): `{rel(RUN_REPORT)}`\n- run272B_payload_manifest(272B 페이로드 목록): `{rel(PROBE_PAYLOAD_MANIFEST)}`\n- run272B_mt5_probe_queue(272B MT5 탐침 대기열): `{rel(MT5_PROBE_QUEUE)}`\n- run272B_lineage(272B 계보): `{rel(LINEAGE_RECEIPT)}`",
    )
    write_md(REVIEW_INDEX, review)

    current = CURRENT_STATE.read_text(encoding="utf-8-sig")
    current = replace_line_prefix(current, "- current_run(", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_line_prefix(current, "- status(", f"- status(상태): `{STATUS}`")
    current = replace_line_prefix(current, "- next_action(", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    current = replace_line_prefix(
        current,
        "- run272B_summary(",
        f"- run272B_summary(272B 요약): run272B(272B 실행)는 time-risk router pressure probe payloads(시간 위험 라우터 압박 탐침 페이로드)를 물질화했다. Effect(효과): payload parquet(페이로드 파케이) `{payload_count}`개와 MT5 probe queue(MT5 탐침 대기열) `{queue_count}`행을 만들었고, selected candidate(선택 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 주장하지 않는다.",
    )
    current = append_once(
        current,
        "run272B_summary",
        f"- run272B_summary(272B 요약): run272B(272B 실행)는 time-risk router pressure probe payloads(시간 위험 라우터 압박 탐침 페이로드)를 물질화했다. Effect(효과): payload parquet(페이로드 파케이) `{payload_count}`개와 MT5 probe queue(MT5 탐침 대기열) `{queue_count}`행을 만들었고, selected candidate(선택 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 주장하지 않는다.",
    )
    write_md(CURRENT_STATE, current)

    workspace = WORKSPACE_STATE.read_text(encoding="utf-8-sig")
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    focus = (
        "- >-\n"
        f"  Stage272(272단계) run272B(272B 실행) time-risk router pressure probe payload materialization(시간 위험 라우터 압박 탐침 페이로드 물질화) `{RUN_ID}`. "
        f"Effect(효과): payload parquet(페이로드 파케이) `{payload_count}`개와 MT5 probe queue(MT5 탐침 대기열) `{queue_count}`행을 만들었고, selected candidate(선택 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 주장하지 않는다.\n"
    )
    workspace = remove_focus_items(workspace, RUN_ID)
    workspace = prepend_focus(workspace, focus)
    write_md(WORKSPACE_STATE, workspace)

    change = CHANGELOG.read_text(encoding="utf-8-sig") if CHANGELOG.exists() else "# Changelog(변경 기록)\n"
    change = append_once(
        change,
        RUN_ID,
        f"## 2026-05-23 run272B time-risk router payload materialization(272B 시간 위험 라우터 페이로드 물질화)\n\n- status(상태): `{STATUS}`\n- judgment(판정): `{JUDGMENT}`\n- effect(효과): payload parquet(페이로드 파케이) `{payload_count}`개와 MT5 probe queue(MT5 탐침 대기열) `{queue_count}`행을 만들었다.\n- boundary(경계): selected candidate(선택 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 `none/not_claimed`다.\n",
    )
    write_md(CHANGELOG, change)

    if IDEA_REGISTER.exists():
        ideas = IDEA_REGISTER.read_text(encoding="utf-8-sig")
        ideas = append_once(
            ideas,
            "IDEA-ST272-TIME-RISK-ROUTER-PRESSURE-PROBE-RUN272B",
            f"| `IDEA-ST272-TIME-RISK-ROUTER-PRESSURE-PROBE-RUN272B` | `{STAGE_ID}` | run272A(272A 실행)의 pressure branch(압박 분기)를 payload parquet(페이로드 파케이)와 MT5 signal CSV(MT5 신호 CSV)로 물질화한다 | `Tier A + Tier B paired exploration(Tier A + Tier B 쌍 탐색)` | `payload_materialized_no_candidate` | payload(페이로드) `{payload_count}`개, MT5 queue(MT5 대기열) `{queue_count}`행, selected candidate(선택 후보) 없음 |",
        )
        write_md(IDEA_REGISTER, ideas)


def write_lineage(manifest: Mapping[str, Any], artifacts: Sequence[Path]) -> None:
    lineage_artifacts = list(artifacts) + [RUN_MANIFEST, LINEAGE_RECEIPT, RUN_REPORT, REVIEW_INDEX, SELECTION_STATUS]
    payload = {
        "source_inputs": manifest["source_inputs"],
        "producer": manifest["producer"],
        "consumer": [NEXT_ACTION, rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
        "artifact_paths": [rel(path) for path in lineage_artifacts if path.exists()],
        "artifact_hashes": {rel(path): sha256_file(path) for path in lineage_artifacts if path.exists() and path != LINEAGE_RECEIPT},
        "registry_links": [rel(RUN_REGISTRY), rel(ALPHA_LEDGER), rel(STAGE_LEDGER), rel(ARTIFACT_REGISTRY)],
        "availability": "tracked_generated_stage_local",
        "lineage_judgment": "connected_with_boundary",
        "claim_boundary": BOUNDARY,
    }
    write_json(LINEAGE_RECEIPT, payload)


def update_artifact_registry(created_at: str, artifacts: Sequence[Path]) -> None:
    artifact_rows = [
        {
            "artifact_id": f"{RUN_ID}__{path.name.replace('.', '_')}",
            "artifact_type": "run272B_payload_materialization_artifact",
            "path": rel(path),
            "sha256": sha256_file(path),
            "stage_id": STAGE_ID,
            "run_id": RUN_ID,
            "created_at_utc": created_at,
            "notes": "run272B time-risk router payload materialization artifact.",
        }
        for path in artifacts
        if path.exists()
    ]
    upsert_csv_rows(ARTIFACT_REGISTRY, ARTIFACT_COLUMNS, artifact_rows, key="artifact_id")


def generated_artifacts() -> list[Path]:
    artifacts = [
        PROBE_PAYLOAD_MANIFEST,
        MT5_PROBE_QUEUE,
        PAYLOAD_READINESS,
        TIER_RECEIPT,
        EXPERIMENT_RECEIPT,
        DATA_INTEGRITY_RECEIPT,
        MODEL_VALIDATION_RECEIPT,
        RESULT_JUDGMENT,
        PAYLOAD_SAMPLES,
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


def execute() -> dict[str, Any]:
    ensure_dirs()
    created_at = utc_now()
    input_hashes = {rel(path): sha256_file(path) for path in source_paths()}
    cp271b, cp271d, variants, _branches, source_handoff, support_handoff = load_inputs()
    manifest_rows, queue_rows, tier_rows, samples = materialize_payloads(
        cp271b, cp271d, variants, source_handoff, support_handoff
    )
    write_stage_outputs(manifest_rows, queue_rows, tier_rows, samples, cp271b, cp271d, input_hashes)
    write_md(RUN_REPORT, report_markdown(manifest_rows, queue_rows))
    update_ledgers(manifest_rows, queue_rows)
    update_state_docs(len(manifest_rows), len(queue_rows))
    artifacts_without_manifest = [path for path in generated_artifacts() if path not in {RUN_MANIFEST, LINEAGE_RECEIPT}]
    manifest = build_manifest(created_at, manifest_rows, queue_rows, input_hashes, artifacts_without_manifest)
    write_lineage(manifest, artifacts_without_manifest)
    update_artifact_registry(created_at, generated_artifacts())
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "payload_count": len(manifest_rows),
        "mt5_queue_rows": len(queue_rows),
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": NEXT_ACTION,
        "report": rel(RUN_REPORT),
    }


if __name__ == "__main__":
    print(json.dumps(execute(), indent=2, ensure_ascii=False))
