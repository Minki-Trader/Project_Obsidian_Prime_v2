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
    sha256_file_lf_normalized,
    upsert_csv_rows,
    write_csv_rows,
)


STAGE271_ID = "271_onnx_candidate_campaign__fresh_edge_rebuild_after_nonfilter_failure"
STAGE272_ID = "272_onnx_candidate_campaign__time_risk_router_pressure_probe"
RUN_ID = "run272A_design_time_risk_router_pressure_probe_packet_v1"
SOURCE_RUN_ID = "run271E_screen_fresh_edge_score_surfaces_v1"
SOURCE_SCORE_RUN_ID = "run271D_execute_fresh_edge_scoring_probe_v1"
NEXT_ACTION = "run272B_materialize_time_risk_router_pressure_probe_payloads"
STATUS = "completed_time_risk_router_pressure_probe_packet_design_no_candidate_selection"
JUDGMENT = "pressure_probe_packet_ready_no_candidate_selection"
BOUNDARY = (
    "research_development_only_no_live_readiness_no_runtime_authority_"
    "no_operating_promotion_no_operating_reference_no_production_baseline_"
    "no_deployment_no_onnx_until_candidate_package_gate"
)

STAGE271_ROOT = ROOT / "stages" / STAGE271_ID
STAGE272_ROOT = ROOT / "stages" / STAGE272_ID
RUN_DIR = STAGE272_ROOT / "02_runs" / "run272A"
REVIEWS = STAGE272_ROOT / "03_reviews"
SELECTED = STAGE272_ROOT / "04_selected"

RUN271E_DIR = STAGE271_ROOT / "02_runs" / "run271E"
RUN271D_DIR = STAGE271_ROOT / "02_runs" / "run271D"
RUN271F_DIR = STAGE271_ROOT / "02_runs" / "run271F"

SOURCE_QUEUE = RUN271E_DIR / "stage272_probe_queue.csv"
SOURCE_SCREENING = RUN271E_DIR / "package_screening_summary.csv"
SOURCE_FAILURE_MEMORY = RUN271E_DIR / "screening_failure_memory.csv"
SOURCE_SUPPORT_CONTROL = RUN271E_DIR / "support_control_carry.csv"
SOURCE_WEAK_SCREEN = RUN271E_DIR / "weak_slice_screen_summary.csv"
SOURCE_SCREENING_RECEIPT = RUN271E_DIR / "screening_decision_receipt.json"
SOURCE_RUN271E_MANIFEST = RUN271E_DIR / "run_manifest.json"
SOURCE_RUN271E_LINEAGE = RUN271E_DIR / "artifact_lineage_receipt.json"
SOURCE_RUN271F_HANDOFF = RUN271F_DIR / "stage272_handoff_manifest.json"
SOURCE_RUN271F_LINEAGE = RUN271F_DIR / "artifact_lineage_receipt.json"
SOURCE_CLOSEOUT = STAGE271_ROOT / "03_reviews" / "stage271_closeout_stage272_time_risk_router_handoff.md"
SOURCE_STAGE_BRIEF = STAGE272_ROOT / "00_spec" / "stage_brief.md"
SOURCE_STAGE_INPUTS = STAGE272_ROOT / "01_inputs" / "input_refs.md"
CP271B_SCORE_TABLE = RUN271D_DIR / "scores" / "cp271B_fresh_edge_scores.parquet"
CP271D_SCORE_TABLE = RUN271D_DIR / "scores" / "cp271D_fresh_edge_scores.parquet"
CP271B_HANDOFF = RUN271D_DIR / "handoff" / "cp271B.json"
CP271D_HANDOFF = RUN271D_DIR / "handoff" / "cp271D.json"

BRANCH_PLAN = RUN_DIR / "pressure_branch_plan.csv"
BRANCH_SUPPLY_METRICS = RUN_DIR / "branch_supply_metrics.csv"
WEAK_SLICE_PRESSURE_MAP = RUN_DIR / "weak_slice_pressure_map.csv"
MT5_PROBE_QUEUE = RUN_DIR / "mt5_probe_design_queue.csv"
THRESHOLD_RECEIPT = RUN_DIR / "pressure_threshold_receipt.json"
EXPERIMENT_RECEIPT = RUN_DIR / "experiment_design_receipt.json"
DATA_INTEGRITY_RECEIPT = RUN_DIR / "data_integrity_receipt.json"
MODEL_VALIDATION_RECEIPT = RUN_DIR / "model_validation_receipt.json"
RESULT_JUDGMENT = RUN_DIR / "result_judgment.csv"
RUN_MANIFEST = RUN_DIR / "run_manifest.json"
ARTIFACT_LINEAGE_RECEIPT = RUN_DIR / "artifact_lineage_receipt.json"
RUN_REPORT = REVIEWS / "run272A_report.md"
REVIEW_INDEX = REVIEWS / "review_index.md"
STAGE_LEDGER = REVIEWS / "stage_run_ledger.csv"
SELECTION_STATUS = SELECTED / "selection_status.md"
CURRENT_STATE = ROOT / "docs/context/current_working_state.md"
WORKSPACE_STATE = ROOT / "docs/workspace/workspace_state.yaml"
CHANGELOG = ROOT / "docs/workspace/changelog.md"
RUN_REGISTRY = ROOT / "docs/registers/run_registry.csv"
ALPHA_LEDGER = ROOT / "docs/registers/alpha_run_ledger.csv"
ARTIFACT_REGISTRY = ROOT / "docs/registers/artifact_registry.csv"
IDEA_REGISTER = ROOT / "docs/registers/idea_registry.md"
PRODUCER_PATH = Path("stage_pipelines/stage272/design_time_risk_router_pressure_probe_packet.py")

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
BRANCH_COLUMNS = (
    "variant_id",
    "variant_role",
    "hypothesis",
    "comparison_baseline",
    "decision_rule",
    "thresholds_json",
    "pressure_axis",
    "upside_condition",
    "failure_mode",
    "discard_condition",
    "invalid_conditions",
    "stop_conditions",
    "evidence_plan",
    "next_use",
    "claim_boundary",
)
SUPPLY_COLUMNS = (
    "variant_id",
    "tier_view",
    "split",
    "rows",
    "decision_count",
    "decision_rate",
    "alignment_rate",
    "long_share",
    "short_share",
    "phase_cut_share",
    "clock_hold_share",
    "route_allowed_share",
    "claim_boundary",
)
WEAK_SLICE_COLUMNS = (
    "variant_id",
    "tier_view",
    "split",
    "slice_type",
    "pressure_value",
    "rows",
    "decision_count",
    "decision_rate",
    "alignment_rate",
    "pressure_read",
)
MT5_QUEUE_COLUMNS = (
    "queue_id",
    "variant_id",
    "package_id",
    "queue_role",
    "source_score_table",
    "source_handoff",
    "required_support_control",
    "materialization_status",
    "mt5_probe_question",
    "success_condition",
    "discard_condition",
    "required_evidence",
    "claim_boundary",
)
RESULT_COLUMNS = (
    "result_subject",
    "evidence_available",
    "evidence_missing",
    "judgment_label",
    "claim_boundary",
    "next_condition",
    "user_explanation_hook",
)

LABEL_OR_FUTURE_PREFIXES = ("future_",)
LABEL_COLUMNS = {"label", "label_alignment_flag", "evaluation_label_available"}


def rel(path: Path | str) -> str:
    item = Path(path)
    try:
        return item.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return item.as_posix()


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with io_path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_json(path: Path, payload: Mapping[str, Any]) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(
        json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def write_csv(path: Path, columns: Sequence[str], rows: Sequence[Mapping[str, Any]]) -> None:
    write_csv_rows(path, columns, rows)


def must_exist(paths: Sequence[Path]) -> None:
    missing = [rel(path) for path in paths if not path_exists(path)]
    if missing:
        raise FileNotFoundError("Missing required source artifacts: " + ", ".join(missing))


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def replace_line_prefix(text: str, prefix: str, replacement: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            lines[index] = replacement
            return "\n".join(lines) + "\n"
    return text.rstrip() + "\n" + replacement + "\n"


def append_once(text: str, marker: str, block: str) -> str:
    if marker in text:
        return text
    return text.rstrip() + "\n\n" + block.rstrip() + "\n"


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


def prepend_focus(text: str, block: str) -> str:
    marker = "current_focus:\n"
    if block.strip() in text or marker not in text:
        return text
    return text.replace(marker, marker + block, 1)


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


def source_paths() -> list[Path]:
    return [
        SOURCE_QUEUE,
        SOURCE_SCREENING,
        SOURCE_FAILURE_MEMORY,
        SOURCE_SUPPORT_CONTROL,
        SOURCE_WEAK_SCREEN,
        SOURCE_SCREENING_RECEIPT,
        SOURCE_RUN271E_MANIFEST,
        SOURCE_RUN271E_LINEAGE,
        SOURCE_RUN271F_HANDOFF,
        SOURCE_RUN271F_LINEAGE,
        SOURCE_CLOSEOUT,
        SOURCE_STAGE_BRIEF,
        SOURCE_STAGE_INPUTS,
        CP271B_SCORE_TABLE,
        CP271D_SCORE_TABLE,
        CP271B_HANDOFF,
        CP271D_HANDOFF,
    ]


def source_hashes(paths: Sequence[Path]) -> dict[str, str]:
    output: dict[str, str] = {}
    for path in paths:
        output[rel(path)] = sha256_file(path)
    return output


def load_score_table() -> pd.DataFrame:
    df = pd.read_parquet(io_path(CP271B_SCORE_TABLE))
    if df.empty:
        raise ValueError("cp271B score table is empty.")
    required = {
        "timestamp",
        "split",
        "tier_view",
        "weekday_phase",
        "month_regime_pressure",
        "session_clock_risk",
        "chron_phase_age",
        "phase_risk_score",
        "phase_opportunity_score",
        "candidate_decision_score",
        "risk_action_code",
        "materialized_decision_flag",
        "route_code",
        "label_alignment_flag",
        "evaluation_label_available",
    }
    missing = sorted(required.difference(df.columns))
    if missing:
        raise ValueError(f"Missing required cp271B score columns: {missing}")
    future_columns = sorted(c for c in df.columns if c.startswith(LABEL_OR_FUTURE_PREFIXES))
    if future_columns:
        raise ValueError(f"Future columns are not allowed in pressure design: {future_columns}")
    df = df.copy()
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
    df["month"] = df["timestamp"].dt.strftime("%Y-%m")
    df["utc_hour"] = df["timestamp"].dt.hour.astype(str)
    df["weekday"] = df["timestamp"].dt.day_name()
    df["chron_segment"] = "chron_unknown"
    for (_, _), group_index in df.groupby(["tier_view", "split"]).groups.items():
        order = df.loc[group_index].sort_values("timestamp").index
        ranks = pd.Series(np.arange(len(order)), index=order)
        if len(order) <= 1:
            df.loc[order, "chron_segment"] = "chron_q1"
            continue
        pct = ranks / max(len(order) - 1, 1)
        df.loc[order[pct <= 0.25], "chron_segment"] = "chron_q1"
        df.loc[order[(pct > 0.25) & (pct <= 0.50)], "chron_segment"] = "chron_q2"
        df.loc[order[(pct > 0.50) & (pct <= 0.75)], "chron_segment"] = "chron_q3"
        df.loc[order[pct > 0.75], "chron_segment"] = "chron_q4"
    return df


def train_quantiles(df: pd.DataFrame) -> dict[str, float]:
    tier_a_train = df[(df["tier_view"] == "Tier A separate") & (df["split"] == "train")]
    if tier_a_train.empty:
        raise ValueError("Tier A train rows are required for pressure thresholds.")
    quantile_specs = {
        "decision_p50": ("candidate_decision_score", 0.50),
        "decision_p55": ("candidate_decision_score", 0.55),
        "decision_p60": ("candidate_decision_score", 0.60),
        "decision_p65": ("candidate_decision_score", 0.65),
        "opportunity_p50": ("phase_opportunity_score", 0.50),
        "opportunity_p55": ("phase_opportunity_score", 0.55),
        "opportunity_p60": ("phase_opportunity_score", 0.60),
        "risk_p45": ("phase_risk_score", 0.45),
        "risk_p50": ("phase_risk_score", 0.50),
        "risk_p55": ("phase_risk_score", 0.55),
        "risk_p60": ("phase_risk_score", 0.60),
        "session_p55": ("session_clock_risk", 0.55),
        "session_p65": ("session_clock_risk", 0.65),
        "session_p75": ("session_clock_risk", 0.75),
        "month_p55": ("month_regime_pressure", 0.55),
        "month_p65": ("month_regime_pressure", 0.65),
        "month_p75": ("month_regime_pressure", 0.75),
        "chron_p55": ("chron_phase_age", 0.55),
        "chron_p65": ("chron_phase_age", 0.65),
    }
    return {
        key: float(tier_a_train[column].quantile(q))
        for key, (column, q) in quantile_specs.items()
    }


def branch_plan(q: Mapping[str, float]) -> list[dict[str, Any]]:
    def js(payload: Mapping[str, Any]) -> str:
        return json.dumps(json_ready(payload), ensure_ascii=False, sort_keys=True, separators=(",", ":"))

    common_evidence = "branch_supply_metrics;weak_slice_pressure_map;mt5_probe_design_queue;future_payload_materialization"
    return [
        {
            "variant_id": "run272A_q01_base_router_reference",
            "variant_role": "reference_seed",
            "hypothesis": "Run271D materialized decision(물질화 판단)을 기준 씨앗으로 유지한다.",
            "comparison_baseline": "cp271B run271D materialized_decision_flag",
            "decision_rule": "materialized_decision_flag == 1",
            "thresholds_json": js({}),
            "pressure_axis": "identity_reference",
            "upside_condition": "validation/OOS alignment(검증/표본외 정렬률)이 0.50 근처를 유지하고 route mix(경로 혼합)가 무너지지 않아야 한다.",
            "failure_mode": "OOS alignment weak(표본외 정렬률 약함) 또는 broad supply(과도 공급)",
            "discard_condition": "OOS alignment below 0.49 or decision_rate above 0.55",
            "invalid_conditions": "missing Tier A/Tier B score table or feature order mismatch",
            "stop_conditions": "Use only as reference after run272B materialization.",
            "evidence_plan": common_evidence,
            "next_use": "carry_to_run272B_payload_materialization",
            "claim_boundary": BOUNDARY,
        },
        {
            "variant_id": "run272A_q02_oos_alignment_tight_router",
            "variant_role": "primary_pressure_probe",
            "hypothesis": "Higher opportunity(상방) and bounded phase risk(경계 위험)이 OOS(표본외) 약점을 줄일 수 있다.",
            "comparison_baseline": "run272A_q01_base_router_reference",
            "decision_rule": "decision>=p55 and opportunity>=p55 and risk<=p55 and session<=p75",
            "thresholds_json": js(
                {
                    "decision_min": q["decision_p55"],
                    "opportunity_min": q["opportunity_p55"],
                    "risk_max": q["risk_p55"],
                    "session_max": q["session_p75"],
                }
            ),
            "pressure_axis": "OOS_alignment_watch",
            "upside_condition": "OOS alignment(표본외 정렬률)이 base 대비 개선되고 decision supply(판단 공급)가 0.12~0.50 안에 있어야 한다.",
            "failure_mode": "too_sparse_or_no_oos_alignment_gain",
            "discard_condition": "OOS decision_rate below 0.12 or OOS alignment below base by 0.01",
            "invalid_conditions": "thresholds computed outside Tier A train scope",
            "stop_conditions": "Stop if Tier B diverges from Tier A by more than 0.10 decision rate.",
            "evidence_plan": common_evidence,
            "next_use": "materialize_as_primary_pressure_payload",
            "claim_boundary": BOUNDARY,
        },
        {
            "variant_id": "run272A_q03_route_mix_rebalance_router",
            "variant_role": "route_mix_pressure_probe",
            "hypothesis": "Route mix(경로 혼합)를 명시적으로 감시하면 한쪽 방향 편향 없이 압박 탐침을 만들 수 있다.",
            "comparison_baseline": "run272A_q01_base_router_reference",
            "decision_rule": "decision>=p50 and opportunity>=p50 and risk<=p60",
            "thresholds_json": js(
                {
                    "decision_min": q["decision_p50"],
                    "opportunity_min": q["opportunity_p50"],
                    "risk_max": q["risk_p60"],
                }
            ),
            "pressure_axis": "route_mix_rebalance",
            "upside_condition": "long_share(롱 비율)가 validation/OOS 모두 0.35~0.65 안에 있어야 한다.",
            "failure_mode": "direction_bias_or_supply_inflation",
            "discard_condition": "long_share outside 0.35~0.65 or OOS decision_rate above 0.55",
            "invalid_conditions": "route_code missing or not long/short labelable",
            "stop_conditions": "Stop if route mix guard is the only apparent improvement.",
            "evidence_plan": common_evidence,
            "next_use": "materialize_as_route_mix_probe_payload",
            "claim_boundary": BOUNDARY,
        },
        {
            "variant_id": "run272A_q04_weak_clock_throttle_router",
            "variant_role": "weak_slice_throttle_probe",
            "hypothesis": "Session clock risk(세션 시계 위험)와 Thursday fragility(목요일 취약성)를 눌러 약한 구간 집중을 줄인다.",
            "comparison_baseline": "run272A_q01_base_router_reference",
            "decision_rule": "decision>=p50 and opportunity>=p50 and session<=p55 and weekday_phase!=thursday_fragility",
            "thresholds_json": js(
                {
                    "decision_min": q["decision_p50"],
                    "opportunity_min": q["opportunity_p50"],
                    "session_max": q["session_p55"],
                    "blocked_weekday_phase": "thursday_fragility",
                }
            ),
            "pressure_axis": "weak_clock_throttle",
            "upside_condition": "Thursday(목요일) and clock risk(시계 위험) supply concentration falls without killing OOS supply.",
            "failure_mode": "over_throttle_or_hidden_month_concentration",
            "discard_condition": "OOS decision_rate below 0.10 or month concentration remains above 0.45",
            "invalid_conditions": "weekday_phase missing or derived from wrong timezone",
            "stop_conditions": "Stop if this becomes a pure defensive filter without upside branch.",
            "evidence_plan": common_evidence,
            "next_use": "materialize_as_weak_slice_throttle_payload",
            "claim_boundary": BOUNDARY,
        },
        {
            "variant_id": "run272A_q05_calendar_regime_guard_router",
            "variant_role": "calendar_regime_probe",
            "hypothesis": "Month regime pressure(월 국면 압력)를 제한하면 OOS(표본외) 월 집중 리스크를 낮출 수 있다.",
            "comparison_baseline": "run272A_q01_base_router_reference",
            "decision_rule": "decision>=p50 and opportunity>=p55 and month<=p55 and chron<=p65",
            "thresholds_json": js(
                {
                    "decision_min": q["decision_p50"],
                    "opportunity_min": q["opportunity_p55"],
                    "month_max": q["month_p55"],
                    "chron_max": q["chron_p65"],
                }
            ),
            "pressure_axis": "calendar_regime_guard",
            "upside_condition": "OOS monthly decision concentration(월별 판단 집중)이 base보다 낮고 alignment(정렬률)가 유지돼야 한다.",
            "failure_mode": "calendar_guard_kills_supply",
            "discard_condition": "OOS decision_count below 250 or validation/OOS alignment below 0.49",
            "invalid_conditions": "month derived from non-UTC timestamp",
            "stop_conditions": "Stop if guard only rewrites the weak month without improving broader pressure axes.",
            "evidence_plan": common_evidence,
            "next_use": "materialize_as_calendar_guard_payload",
            "claim_boundary": BOUNDARY,
        },
        {
            "variant_id": "run272A_q06_failure_boundary_high_risk_router",
            "variant_role": "failure_boundary_control",
            "hypothesis": "High risk clock/month states(높은 시간/월 위험 상태)를 따로 떼면 폐기 경계를 더 명확히 볼 수 있다.",
            "comparison_baseline": "run272A_q01_base_router_reference",
            "decision_rule": "decision>=p50 and (session>=p75 or month>=p75 or weekday_phase==thursday_fragility)",
            "thresholds_json": js(
                {
                    "decision_min": q["decision_p50"],
                    "session_min": q["session_p75"],
                    "month_min": q["month_p75"],
                    "flagged_weekday_phase": "thursday_fragility",
                }
            ),
            "pressure_axis": "explicit_failure_boundary",
            "upside_condition": "None(없음). This is failure memory control(실패 기억 대조) only.",
            "failure_mode": "known_weak_slice_exposure",
            "discard_condition": "Any attempt to read this as selected candidate",
            "invalid_conditions": "failure boundary mask overlaps all payload branches",
            "stop_conditions": "Do not materialize as positive MT5 branch unless separately justified.",
            "evidence_plan": common_evidence,
            "next_use": "hold_as_failure_boundary_control",
            "claim_boundary": BOUNDARY,
        },
    ]


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
    if variant_id == "run272A_q05_calendar_regime_guard_router":
        return (
            df["candidate_decision_score"].ge(thresholds["decision_min"])
            & df["phase_opportunity_score"].ge(thresholds["opportunity_min"])
            & df["month_regime_pressure"].le(thresholds["month_max"])
            & df["chron_phase_age"].le(thresholds["chron_max"])
        )
    if variant_id == "run272A_q06_failure_boundary_high_risk_router":
        return (
            df["candidate_decision_score"].ge(thresholds["decision_min"])
            & (
                df["session_clock_risk"].ge(thresholds["session_min"])
                | df["month_regime_pressure"].ge(thresholds["month_min"])
                | df["weekday_phase"].eq(thresholds["flagged_weekday_phase"])
            )
        )
    raise ValueError(f"Unknown variant_id: {variant_id}")


def safe_rate(numerator: float, denominator: float) -> float | str:
    if denominator <= 0:
        return ""
    return round(float(numerator) / float(denominator), 8)


def summarize_branch_supply(df: pd.DataFrame, variants: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for variant in variants:
        mask = branch_mask(df, variant)
        for (tier_view, split), group in df.groupby(["tier_view", "split"], dropna=False):
            local_mask = mask.loc[group.index]
            decisions = group[local_mask]
            decision_count = int(local_mask.sum())
            route_long = int(decisions["route_code"].eq("long").sum()) if decision_count else 0
            route_short = int(decisions["route_code"].eq("short").sum()) if decision_count else 0
            eval_rows = decisions[decisions["evaluation_label_available"].astype(int).eq(1)]
            alignment = (
                float(eval_rows["label_alignment_flag"].astype(float).mean())
                if len(eval_rows)
                else np.nan
            )
            rows.append(
                {
                    "variant_id": variant["variant_id"],
                    "tier_view": tier_view,
                    "split": split,
                    "rows": len(group),
                    "decision_count": decision_count,
                    "decision_rate": safe_rate(decision_count, len(group)),
                    "alignment_rate": round(alignment, 8) if np.isfinite(alignment) else "",
                    "long_share": safe_rate(route_long, decision_count),
                    "short_share": safe_rate(route_short, decision_count),
                    "phase_cut_share": safe_rate(int(decisions["risk_action_code"].eq("phase_cut").sum()), decision_count),
                    "clock_hold_share": safe_rate(int(decisions["risk_action_code"].eq("clock_hold").sum()), decision_count),
                    "route_allowed_share": safe_rate(int(decisions["risk_action_code"].eq("route_allowed").sum()), decision_count),
                    "claim_boundary": BOUNDARY,
                }
            )
    return rows


def pressure_read(decision_rate: float | str, alignment_rate: float | str) -> str:
    d = float(decision_rate) if decision_rate != "" else 0.0
    a = float(alignment_rate) if alignment_rate != "" else np.nan
    if d > 0.55:
        return "supply_spike_watch"
    if d < 0.08:
        return "supply_too_sparse_watch"
    if np.isfinite(a) and a < 0.49:
        return "alignment_weak_watch"
    return "bounded_pressure_slice"


def weak_slice_map(df: pd.DataFrame, variants: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    slice_columns = {
        "weekday": "weekday",
        "month": "month",
        "utc_hour": "utc_hour",
        "chron_segment": "chron_segment",
        "weekday_phase": "weekday_phase",
    }
    for variant in variants:
        mask = branch_mask(df, variant)
        for (tier_view, split), group in df.groupby(["tier_view", "split"], dropna=False):
            local_mask = mask.loc[group.index]
            for slice_type, column in slice_columns.items():
                slice_rows: list[dict[str, Any]] = []
                for value, part in group.groupby(column, dropna=False):
                    part_mask = local_mask.loc[part.index]
                    decisions = part[part_mask]
                    decision_count = int(part_mask.sum())
                    eval_rows = decisions[decisions["evaluation_label_available"].astype(int).eq(1)]
                    alignment = (
                        float(eval_rows["label_alignment_flag"].astype(float).mean())
                        if len(eval_rows)
                        else np.nan
                    )
                    decision_rate = safe_rate(decision_count, len(part))
                    align_value = round(alignment, 8) if np.isfinite(alignment) else ""
                    slice_rows.append(
                        {
                            "variant_id": variant["variant_id"],
                            "tier_view": tier_view,
                            "split": split,
                            "slice_type": slice_type,
                            "pressure_value": str(value),
                            "rows": len(part),
                            "decision_count": decision_count,
                            "decision_rate": decision_rate,
                            "alignment_rate": align_value,
                            "pressure_read": pressure_read(decision_rate, align_value),
                        }
                    )
                ranked = sorted(
                    slice_rows,
                    key=lambda row: (
                        0 if row["pressure_read"] != "bounded_pressure_slice" else 1,
                        -(float(row["decision_rate"]) if row["decision_rate"] != "" else 0.0),
                        float(row["alignment_rate"]) if row["alignment_rate"] != "" else 1.0,
                    ),
                )
                rows.extend(ranked[:3])
    return rows


def finalize_branch_next_use(
    variants: Sequence[Mapping[str, Any]],
    supply_rows: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    oos_by_variant = {
        str(row["variant_id"]): row
        for row in supply_rows
        if row["tier_view"] == "Tier A separate" and row["split"] == "oos"
    }
    finalized: list[dict[str, Any]] = []
    for variant in variants:
        row = dict(variant)
        oos = oos_by_variant.get(str(row["variant_id"]), {})
        decision_count = int(oos.get("decision_count", 0) or 0)
        decision_rate = float(oos.get("decision_rate", 0) or 0)
        if row["variant_role"] not in {"reference_seed", "failure_boundary_control"}:
            if decision_count < 250 or decision_rate < 0.08:
                row["next_use"] = "hold_due_to_oos_supply_floor_failure"
                row["stop_conditions"] = (
                    str(row["stop_conditions"])
                    + " Triggered in run272A: Tier A OOS supply fell below materialization floor."
                )
        finalized.append(row)
    return finalized


def mt5_probe_queue(variants: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    materialize_roles = {
        "reference_seed": "reference_control_payload",
        "primary_pressure_probe": "primary_pressure_payload",
        "route_mix_pressure_probe": "route_mix_payload",
        "weak_slice_throttle_probe": "weak_slice_throttle_payload",
        "calendar_regime_probe": "calendar_guard_payload",
    }
    rows: list[dict[str, Any]] = []
    for variant in variants:
        role = str(variant["variant_role"])
        if role not in materialize_roles:
            continue
        if not str(variant["next_use"]).startswith(("carry_to_", "materialize_")):
            continue
        rows.append(
            {
                "queue_id": f"run272B_{variant['variant_id'].replace('run272A_', '')}",
                "variant_id": variant["variant_id"],
                "package_id": "cp271B_time_risk_phase_router_surface",
                "queue_role": materialize_roles[role],
                "source_score_table": rel(CP271B_SCORE_TABLE),
                "source_handoff": rel(CP271B_HANDOFF),
                "required_support_control": "cp271D_stage270_reference_control_boundary",
                "materialization_status": "ready_for_run272B_payload_materialization",
                "mt5_probe_question": variant["hypothesis"],
                "success_condition": variant["upside_condition"],
                "discard_condition": variant["discard_condition"],
                "required_evidence": "payload_parquet;handoff_json;tier_receipt;MT5_signal_csv;future_MT5_probe",
                "claim_boundary": BOUNDARY,
            }
        )
    return rows


def experiment_receipt(branch_count: int, queue_count: int) -> dict[str, Any]:
    return {
        "hypothesis": "time-risk phase router(시간 위험 국면 라우터)가 OOS(표본외), weak slice(약한 구간), route mix(경로 혼합) 압박을 견디면 다음 MT5 probe(MT5 탐침)로 갈 수 있다.",
        "decision_use": "run272B payload materialization(페이로드 물질화) 여부를 정한다.",
        "comparison_baseline": "run272A_q01_base_router_reference",
        "control_variables": "symbol=US100;timeframe=M5;feature_order_hash=fa06973c24462298ea38d84528b07ca0adf357e506f3bfeea02eb0d5691ab8e2;cp271B score owner unchanged",
        "changed_variables": "pressure branch thresholds(압박 분기 임계값) and weak-slice guards(약한 구간 방어)",
        "sample_scope": "Tier A separate, Tier B separate, Tier A+B combined screen view; rows=93300; splits=train/validation/oos",
        "success_criteria": "At least one non-reference branch has bounded supply and no route mix collapse before payload materialization.",
        "failure_criteria": "All pressure branches are too sparse, over-broad, route-biased, or OOS alignment weak.",
        "invalid_conditions": "missing source score table, feature order mismatch, label used as feature, missing Tier B paired view",
        "stop_conditions": "Do not select candidate or start ONNX until MT5/runtime and Adapter gates exist.",
        "evidence_plan": "pressure_branch_plan;branch_supply_metrics;weak_slice_pressure_map;mt5_probe_design_queue;receipts;ledgers",
        "branch_count": branch_count,
        "mt5_probe_design_queue_rows": queue_count,
        "work_packet_schema_lint": "passed_for_design_packet",
        "claim_boundary": BOUNDARY,
    }


def data_integrity_receipt(df: pd.DataFrame, hashes: Mapping[str, str]) -> dict[str, Any]:
    label_present = sorted(c for c in LABEL_COLUMNS if c in df.columns)
    future_columns = sorted(c for c in df.columns if c.startswith(LABEL_OR_FUTURE_PREFIXES))
    duplicate_count = int(df.duplicated(subset=["timestamp", "tier_view", "split"]).sum())
    return {
        "data_source": rel(CP271B_SCORE_TABLE),
        "time_axis": "timestamp is UTC bar timestamp(UTC 바 타임스탬프) inherited from run271D score table.",
        "sample_scope": {
            "symbol": "US100",
            "timeframe": "M5",
            "rows": int(len(df)),
            "tier_views": sorted(df["tier_view"].dropna().unique().tolist()),
            "splits": sorted(df["split"].dropna().unique().tolist()),
            "start": str(df["timestamp"].min()),
            "end": str(df["timestamp"].max()),
        },
        "missing_or_duplicate_check": {
            "duplicate_timestamp_tier_split_rows": duplicate_count,
            "missing_required_feature_count_max": int(df["missing_required_feature_count"].max()) if "missing_required_feature_count" in df.columns else "",
        },
        "feature_label_boundary": "label columns(라벨 열)은 alignment read(정렬 판독)에만 쓰고 branch decision(분기 판단)에는 사용하지 않는다.",
        "split_boundary": "thresholds computed only from Tier A train(Tier A 학습) rows; validation/OOS are pressure reads only.",
        "leakage_risk": "selection bias from repeated branch design(반복 분기 설계 선택 편향); no future_* columns allowed.",
        "label_columns_present_for_evaluation_only": label_present,
        "future_columns_present": future_columns,
        "data_hash_or_identity": hashes,
        "integrity_judgment": "usable_with_boundary",
    }


def model_validation_receipt(branch_count: int) -> dict[str, Any]:
    return {
        "model_family": "fixed cp271B score surface(고정 cp271B 점수 표면); no new model training(새 모델 학습 없음)",
        "target_and_label": "label_alignment_flag(라벨 정렬 플래그) is evaluation-only structural signal(평가 전용 구조 신호)",
        "split_method": "train threshold design plus validation/OOS pressure read(학습 임계값 설계 및 검증/표본외 압박 판독)",
        "selection_metric": "bounded supply, OOS alignment, route mix, weak-slice concentration",
        "secondary_metrics": "decision_rate, long_share, short_share, phase_cut_share, clock_hold_share",
        "threshold_policy": "train-quantile branch design(학습 분위수 분기 설계), not selected threshold(선택 임계값 아님)",
        "overfit_risk": "multiple branch pressure design can overfit structural scout(구조 스카우트)에 맞춰질 수 있음",
        "calibration_risk": "candidate_decision_score is rank-like score(순위형 점수), not calibrated probability(보정 확률 아님)",
        "comparison_baseline": "run272A_q01_base_router_reference",
        "branch_count": branch_count,
        "validation_judgment": "exploratory_pressure_design_no_candidate_selection",
        "claim_boundary": BOUNDARY,
    }


def result_rows(branch_count: int, queue_count: int) -> list[dict[str, str]]:
    return [
        {
            "result_subject": "run272A pressure design(272A 압박 설계)",
            "evidence_available": f"{rel(BRANCH_PLAN)};{rel(BRANCH_SUPPLY_METRICS)};{rel(WEAK_SLICE_PRESSURE_MAP)}",
            "evidence_missing": "payload parquet(페이로드 parquet);MT5 runtime output(MT5 런타임 출력);trading KPI(거래 핵심 성과 지표);Adapter package(어댑터 패키지)",
            "judgment_label": "exploratory_design_packet_ready_no_candidate_selection",
            "claim_boundary": BOUNDARY,
            "next_condition": NEXT_ACTION,
            "user_explanation_hook": f"{branch_count}개 압박 분기와 {queue_count}개 물질화 대기열을 만들었지만 선택 후보는 아니다.",
        }
    ]


def manifest_payload(
    created_at: str,
    hashes: Mapping[str, str],
    output_hashes: Mapping[str, str],
    branch_count: int,
    queue_count: int,
) -> dict[str, Any]:
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE272_ID,
        "source_run_id": SOURCE_RUN_ID,
        "source_score_run_id": SOURCE_SCORE_RUN_ID,
        "created_at_utc": created_at,
        "producer": rel(PRODUCER_PATH),
        "entry_command": "python stage_pipelines/stage272/design_time_risk_router_pressure_probe_packet.py",
        "source_inputs": hashes,
        "outputs": output_hashes,
        "branch_count": branch_count,
        "mt5_probe_design_queue_rows": queue_count,
        "selected_candidate": "none",
        "selected_research_baseline": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": NEXT_ACTION,
        "claim_boundary": BOUNDARY,
    }


def lineage_payload(artifacts: Sequence[Path], hashes: Mapping[str, str]) -> dict[str, Any]:
    return {
        "source_inputs": hashes,
        "producer": rel(PRODUCER_PATH),
        "consumer": NEXT_ACTION,
        "artifact_paths": [rel(path) for path in artifacts],
        "artifact_hashes": {
            rel(path): sha256_file_lf_normalized(path)
            for path in artifacts
            if path_exists(path)
        },
        "registry_links": [
            rel(RUN_REGISTRY),
            rel(ALPHA_LEDGER),
            rel(STAGE_LEDGER),
            rel(ARTIFACT_REGISTRY),
        ],
        "availability": "tracked_after_commit_or_reproducible_from_command",
        "lineage_judgment": "connected_with_boundary",
        "claim_boundary": BOUNDARY,
    }


def report_markdown(branch_count: int, queue_count: int, supply_rows: Sequence[Mapping[str, Any]]) -> str:
    tier_a_oos = [
        row for row in supply_rows
        if row["tier_view"] == "Tier A separate" and row["split"] == "oos"
    ]
    lines = [
        "# run272A Time-Risk Router Pressure Probe Packet(272A 시간 위험 라우터 압박 탐침 묶음)",
        "",
        f"- run_id(실행 ID): `{RUN_ID}`",
        f"- status(상태): `{STATUS}`",
        f"- judgment(판정): `{JUDGMENT}`",
        f"- branch_count(분기 수): `{branch_count}`",
        f"- mt5_probe_design_queue_rows(MT5 탐침 설계 대기열 행): `{queue_count}`",
        "- selected_candidate(선택 후보): `none`",
        "- ONNX readiness(온엑스 준비): `not_claimed`",
        "- Goal Achieve(목표 달성): `not_claimed`",
        f"- next_action(다음 행동): `{NEXT_ACTION}`",
        "",
        "## Plain Result(쉬운 결과)",
        "",
        "run272A(272A 실행)는 cp271B(271B 패키지)를 후보로 고르지 않고 압박 분기(branch, 분기)로 나눴다.",
        "효과(effect, 효과): run272B(272B 실행)가 payload parquet(페이로드 parquet), handoff JSON(인계 JSON), MT5 signal CSV(MT5 신호 CSV)를 만들 수 있는 대기열을 갖게 됐다.",
        "",
        "## Tier A OOS Pressure Read(Tier A 표본외 압박 판독)",
        "",
    ]
    for row in tier_a_oos:
        lines.append(
            f"- `{row['variant_id']}`: decision_rate(판단 비율) `{row['decision_rate']}`, "
            f"alignment_rate(정렬률) `{row['alignment_rate']}`, long_share(롱 비율) `{row['long_share']}`"
        )
    lines.extend(
        [
            "",
            "## Gate Coverage(게이트 커버리지)",
            "",
            "- work_packet_schema_lint(작업 묶음 스키마 점검): hypothesis/comparison/control/changed variables/evidence plan(가설/비교/고정/변경 변수/근거 계획)을 receipt(영수증)에 기록했다.",
            "- data_integrity(데이터 무결성): timestamp(타임스탬프), split(분할), Tier A/B(티어 A/B), label boundary(라벨 경계)를 기록했다.",
            "- model_validation(모델 검증): 새 모델 학습이 아니라 fixed score surface(고정 점수 표면)의 train-quantile pressure design(학습 분위수 압박 설계)로 제한했다.",
            "- final_claim_guard(최종 주장 방어): selected candidate(선택 후보), ONNX readiness(온엑스 준비), runtime authority(런타임 권위)는 주장하지 않는다.",
            "",
            "## Boundary(경계)",
            "",
            f"`{BOUNDARY}`",
        ]
    )
    return "\n".join(lines)


def update_registers(
    created_at: str,
    artifacts: Sequence[Path],
    branch_count: int,
    queue_count: int,
) -> None:
    upsert_csv_rows(
        RUN_REGISTRY,
        RUN_REGISTRY_COLUMNS,
        [
            {
                "run_id": RUN_ID,
                "stage_id": STAGE272_ID,
                "lane": "experiment_design",
                "status": STATUS,
                "judgment": JUDGMENT,
                "path": rel(RUN_REPORT),
                "notes": f"branch_count={branch_count};mt5_probe_queue_rows={queue_count};selected_candidate=none;onnx_readiness=not_claimed;next_action={NEXT_ACTION}.",
            }
        ],
        key="run_id",
    )
    alpha_rows = [
        {
            "ledger_row_id": f"{RUN_ID}__tier_a_design",
            "stage_id": STAGE272_ID,
            "run_id": RUN_ID,
            "subrun_id": "tier_a_design",
            "parent_run_id": SOURCE_RUN_ID,
            "record_view": "Tier A pressure design(티어 A 압박 설계)",
            "tier_scope": "Tier A separate",
            "kpi_scope": "pressure_design_structural_signal",
            "scoreboard_lane": "structural_scout",
            "status": STATUS,
            "judgment": JUDGMENT,
            "path": rel(BRANCH_SUPPLY_METRICS),
            "primary_kpi": f"branch_count={branch_count};mt5_probe_queue_rows={queue_count}",
            "guardrail_kpi": "selected_candidate=none;onnx_readiness=not_claimed;trading_kpi=none",
            "external_verification_status": "out_of_scope_by_claim_design_only",
            "notes": "Tier A used for train thresholds and validation/OOS pressure read.",
        },
        {
            "ledger_row_id": f"{RUN_ID}__tier_b_design",
            "stage_id": STAGE272_ID,
            "run_id": RUN_ID,
            "subrun_id": "tier_b_design",
            "parent_run_id": SOURCE_RUN_ID,
            "record_view": "Tier B pressure design(티어 B 압박 설계)",
            "tier_scope": "Tier B separate",
            "kpi_scope": "partial_context_pressure_design",
            "scoreboard_lane": "structural_scout",
            "status": STATUS,
            "judgment": "partial_context_design_completed_no_fallback_authority",
            "path": rel(BRANCH_SUPPLY_METRICS),
            "primary_kpi": "Tier B mirrored for pressure design",
            "guardrail_kpi": "no_fallback_authority_claimed",
            "external_verification_status": "out_of_scope_by_claim_design_only",
            "notes": "Tier B remains exploration label only.",
        },
        {
            "ledger_row_id": f"{RUN_ID}__tier_ab_design",
            "stage_id": STAGE272_ID,
            "run_id": RUN_ID,
            "subrun_id": "tier_ab_design",
            "parent_run_id": SOURCE_RUN_ID,
            "record_view": "Tier A+B pressure design(티어 A+B 압박 설계)",
            "tier_scope": "Tier A+B combined",
            "kpi_scope": "combined_design_queue",
            "scoreboard_lane": "structural_scout",
            "status": STATUS,
            "judgment": "combined_design_view_no_routed_pnl_claim",
            "path": rel(MT5_PROBE_QUEUE),
            "primary_kpi": f"mt5_probe_design_queue_rows={queue_count}",
            "guardrail_kpi": "performance_claim=none;synthetic_design_view_only",
            "external_verification_status": "out_of_scope_by_claim_design_only",
            "notes": "Combined record is design view, not routed account performance.",
        },
    ]
    upsert_csv_rows(ALPHA_LEDGER, ALPHA_LEDGER_COLUMNS, alpha_rows, key="ledger_row_id")
    upsert_csv_rows(
        STAGE_LEDGER,
        STAGE_LEDGER_COLUMNS,
        [
            {
                "row_id": f"{RUN_ID}__pressure_design",
                "stage_id": STAGE272_ID,
                "run_id": RUN_ID,
                "view": "time_risk_router_pressure_probe_packet_design",
                "tier_scope": "Tier A+B pressure design",
                "scoreboard": "structural_scout",
                "status": STATUS,
                "judgment": JUDGMENT,
                "evidence_boundary": "design_packet_only_no_candidate_no_onnx",
                "report_path": rel(RUN_REPORT),
                "notes": f"branch_count={branch_count};mt5_probe_queue_rows={queue_count};next_action={NEXT_ACTION}.",
            }
        ],
        key="row_id",
    )
    artifact_rows = [
        {
            "artifact_id": f"{RUN_ID}__{path.name.replace('.', '_')}",
            "artifact_type": "run272A_pressure_design_artifact",
            "path": rel(path),
            "sha256": sha256_file_lf_normalized(path),
            "stage_id": STAGE272_ID,
            "run_id": RUN_ID,
            "created_at_utc": created_at,
            "notes": "run272A time-risk router pressure design artifact.",
        }
        for path in artifacts
        if path_exists(path)
    ]
    upsert_csv_rows(ARTIFACT_REGISTRY, ARTIFACT_COLUMNS, artifact_rows, key="artifact_id")


def update_state_docs(branch_count: int, queue_count: int) -> None:
    selection = io_path(SELECTION_STATUS).read_text(encoding="utf-8-sig")
    selection = replace_line_prefix(selection, "- stage_status(단계 상태):", f"- stage_status(단계 상태): `{STATUS}`")
    selection = replace_line_prefix(selection, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    selection = replace_line_prefix(selection, "- last_completed_run(마지막 완료 실행):", f"- last_completed_run(마지막 완료 실행): `{RUN_ID}`")
    selection = replace_line_prefix(selection, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    selection = replace_section(
        selection,
        "## Current Meaning(현재 의미)",
        f"run272A(272A 실행)는 `cp271B_time_risk_phase_router_surface`를 pressure branch(압박 분기) `{branch_count}`개와 MT5 probe design queue(MT5 탐침 설계 대기열) `{queue_count}`행으로 바꿨다.\n효과(effect, 효과): 다음 run272B(272B 실행)는 payload parquet(페이로드 parquet), handoff JSON(인계 JSON), MT5 signal CSV(MT5 신호 CSV)를 만들 수 있지만, 아직 candidate package(후보 패키지) 선택이나 ONNX readiness(온엑스 준비)는 없다.",
    )
    selection = append_once(selection, "pressure_branch_plan", f"- pressure_branch_plan(압박 분기 계획): `{rel(BRANCH_PLAN)}`")
    selection = append_once(selection, "mt5_probe_design_queue", f"- mt5_probe_design_queue(MT5 탐침 설계 대기열): `{rel(MT5_PROBE_QUEUE)}`")
    write_md(SELECTION_STATUS, selection)

    review = io_path(REVIEW_INDEX).read_text(encoding="utf-8-sig")
    review = append_once(
        review,
        "run272A_report",
        f"- run272A_report(272A 보고): `{rel(RUN_REPORT)}`\n- run272A_pressure_branch_plan(272A 압박 분기 계획): `{rel(BRANCH_PLAN)}`\n- run272A_mt5_probe_design_queue(272A MT5 탐침 설계 대기열): `{rel(MT5_PROBE_QUEUE)}`",
    )
    write_md(REVIEW_INDEX, review)

    current = io_path(CURRENT_STATE).read_text(encoding="utf-8-sig")
    current = replace_line_prefix(current, "- current_run(현재 실행):", f"- current_run(현재 실행): `{RUN_ID}`")
    current = replace_line_prefix(current, "- status(상태):", f"- status(상태): `{STATUS}`")
    current = replace_line_prefix(current, "- next_action(다음 행동):", f"- next_action(다음 행동): `{NEXT_ACTION}`")
    current = replace_line_prefix(
        current,
        "- run272A_summary(272A 요약):",
        f"- run272A_summary(272A 요약): run272A(272A 실행)는 time-risk router pressure probe packet(시간 위험 라우터 압박 탐침 묶음)을 설계했다. Effect(효과): branch(분기) `{branch_count}`개와 MT5 probe design queue(MT5 탐침 설계 대기열) `{queue_count}`행을 만들었고, selected candidate(선택 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 주장하지 않는다.",
    )
    current = append_once(
        current,
        "run272A_summary",
        f"- run272A_summary(272A 요약): run272A(272A 실행)는 time-risk router pressure probe packet(시간 위험 라우터 압박 탐침 묶음)을 설계했다. Effect(효과): branch(분기) `{branch_count}`개와 MT5 probe design queue(MT5 탐침 설계 대기열) `{queue_count}`행을 만들었고, selected candidate(선택 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 주장하지 않는다.",
    )
    write_md(CURRENT_STATE, current)

    workspace = io_path(WORKSPACE_STATE).read_text(encoding="utf-8-sig")
    workspace = replace_line_prefix(workspace, "current_run_id:", f"current_run_id: {RUN_ID}")
    workspace = replace_line_prefix(
        workspace,
        "  Stage272(272단계) run272A(272A 실행) time-risk router pressure probe packet design(시간 위험 라우터 압박 탐침 묶음 설계)",
        f"  Stage272(272단계) run272A(272A 실행) time-risk router pressure probe packet design(시간 위험 라우터 압박 탐침 묶음 설계) `{RUN_ID}`. Effect(효과): branch(분기) `{branch_count}`개와 MT5 probe design queue(MT5 탐침 설계 대기열) `{queue_count}`행을 만들었고, selected candidate(선택 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 주장하지 않는다.",
    )
    focus = (
        "- >-\n"
        f"  Stage272(272단계) run272A(272A 실행) time-risk router pressure probe packet design(시간 위험 라우터 압박 탐침 묶음 설계) `{RUN_ID}`. "
        f"Effect(효과): branch(분기) `{branch_count}`개와 MT5 probe design queue(MT5 탐침 설계 대기열) `{queue_count}`행을 만들었고, selected candidate(선택 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 주장하지 않는다.\n"
    )
    workspace = remove_focus_items(workspace, RUN_ID)
    workspace = prepend_focus(workspace, focus)
    write_md(WORKSPACE_STATE, workspace)

    change = io_path(CHANGELOG).read_text(encoding="utf-8-sig") if path_exists(CHANGELOG) else "# Changelog(변경 기록)\n"
    change = append_once(
        change,
        RUN_ID,
        f"## 2026-05-23 run272A time-risk router pressure design(272A 시간 위험 라우터 압박 설계)\n\n- status(상태): `{STATUS}`\n- judgment(판정): `{JUDGMENT}`\n- effect(효과): branch(분기) `{branch_count}`개와 MT5 probe design queue(MT5 탐침 설계 대기열) `{queue_count}`행을 만들었다.\n- boundary(경계): selected candidate(선택 후보), ONNX readiness(온엑스 준비), Goal Achieve(목표 달성)는 `none/not_claimed`다.\n",
    )
    write_md(CHANGELOG, change)


def update_idea_register(branch_count: int, queue_count: int) -> None:
    ideas = io_path(IDEA_REGISTER).read_text(encoding="utf-8-sig")
    block = (
        f"| `IDEA-ST272-TIME-RISK-ROUTER-PRESSURE-PROBE-RUN272A` | `{STAGE272_ID}` | cp271B(271B 패키지)의 time-risk router(시간 위험 라우터)를 압박 분기 `{branch_count}`개로 나눠 MT5 probe(MT5 탐침) 전 failure boundary(실패 경계)를 본다 | `Tier A + Tier B paired exploration(Tier A + Tier B 쌍 탐색)` | `design_packet_ready_no_candidate` | MT5 probe design queue(MT5 탐침 설계 대기열) `{queue_count}`행. selected candidate(선택 후보), ONNX readiness(온엑스 준비)는 없음 |"
    )
    ideas = append_once(ideas, "IDEA-ST272-TIME-RISK-ROUTER-PRESSURE-PROBE-RUN272A", block)
    write_md(IDEA_REGISTER, ideas)


def execute() -> dict[str, Any]:
    paths = source_paths()
    must_exist(paths)
    io_path(RUN_DIR).mkdir(parents=True, exist_ok=True)
    created_at = utc_now()
    hashes = source_hashes(paths)
    df = load_score_table()
    q = train_quantiles(df)
    variants = branch_plan(q)
    supply_rows = summarize_branch_supply(df, variants)
    variants = finalize_branch_next_use(variants, supply_rows)
    weak_rows = weak_slice_map(df, variants)
    queue = mt5_probe_queue(variants)

    write_csv(BRANCH_PLAN, BRANCH_COLUMNS, variants)
    write_csv(BRANCH_SUPPLY_METRICS, SUPPLY_COLUMNS, supply_rows)
    write_csv(WEAK_SLICE_PRESSURE_MAP, WEAK_SLICE_COLUMNS, weak_rows)
    write_csv(MT5_PROBE_QUEUE, MT5_QUEUE_COLUMNS, queue)
    write_json(THRESHOLD_RECEIPT, {"threshold_source": "Tier A train quantiles(티어 A 학습 분위수)", "thresholds": q, "claim_boundary": BOUNDARY})
    write_json(EXPERIMENT_RECEIPT, experiment_receipt(len(variants), len(queue)))
    write_json(DATA_INTEGRITY_RECEIPT, data_integrity_receipt(df, hashes))
    write_json(MODEL_VALIDATION_RECEIPT, model_validation_receipt(len(variants)))
    write_csv(RESULT_JUDGMENT, RESULT_COLUMNS, result_rows(len(variants), len(queue)))
    provisional_artifacts = [
        BRANCH_PLAN,
        BRANCH_SUPPLY_METRICS,
        WEAK_SLICE_PRESSURE_MAP,
        MT5_PROBE_QUEUE,
        THRESHOLD_RECEIPT,
        EXPERIMENT_RECEIPT,
        DATA_INTEGRITY_RECEIPT,
        MODEL_VALIDATION_RECEIPT,
        RESULT_JUDGMENT,
    ]
    output_hashes = {rel(path): sha256_file_lf_normalized(path) for path in provisional_artifacts}
    write_json(RUN_MANIFEST, manifest_payload(created_at, hashes, output_hashes, len(variants), len(queue)))
    write_md(RUN_REPORT, report_markdown(len(variants), len(queue), supply_rows))
    artifacts = [RUN_MANIFEST, *provisional_artifacts, RUN_REPORT, SELECTION_STATUS, REVIEW_INDEX]
    write_json(ARTIFACT_LINEAGE_RECEIPT, lineage_payload([*artifacts, ARTIFACT_LINEAGE_RECEIPT], hashes))
    artifacts.append(ARTIFACT_LINEAGE_RECEIPT)
    update_registers(created_at, artifacts, len(variants), len(queue))
    update_state_docs(len(variants), len(queue))
    update_idea_register(len(variants), len(queue))
    return {
        "run_id": RUN_ID,
        "stage_id": STAGE272_ID,
        "status": STATUS,
        "judgment": JUDGMENT,
        "branch_count": len(variants),
        "mt5_probe_design_queue_rows": len(queue),
        "selected_candidate": "none",
        "onnx_readiness": "not_claimed",
        "goal_achieve": "not_claimed",
        "next_action": NEXT_ACTION,
        "report": rel(RUN_REPORT),
    }


def main() -> int:
    print(json.dumps(execute(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
