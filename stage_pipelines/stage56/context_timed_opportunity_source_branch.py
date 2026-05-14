from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

import numpy as np
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from foundation.alpha.discrete_signal_table import export_single_discrete_signal_score_table  # noqa: E402
from foundation.control_plane.alpha_run_ledgers import build_mt5_alpha_ledger_rows  # noqa: E402
from foundation.control_plane.ledger import (  # noqa: E402
    ALPHA_LEDGER_COLUMNS,
    RUN_REGISTRY_COLUMNS,
    io_path,
    json_ready,
    path_exists,
    sha256_file_lf_normalized,
    upsert_csv_rows,
)
from foundation.control_plane.mt5_tier_balance_completion import (  # noqa: E402
    COMMON_FILES_ROOT_DEFAULT,
    METAEDITOR_PATH_DEFAULT,
    TERMINAL_DATA_ROOT_DEFAULT,
    TERMINAL_PATH_DEFAULT,
    TESTER_PROFILE_ROOT_DEFAULT,
    attempt_payload,
    copy_to_common,
    execute_prepared_run,
    split_dates_from_frame,
)
from foundation.control_plane.mt5_trade_attribution import MarketData  # noqa: E402
from foundation.models.onnx_bridge import ordered_hash  # noqa: E402
from foundation.mt5 import runtime_support as mt5  # noqa: E402
from stage_pipelines.stage56 import agreement_firewall_density_recovery_branch as agreement  # noqa: E402
from stage_pipelines.stage56 import independent_event_source_route_branch as aw  # noqa: E402


STAGE_ID = "56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection"
RUN_NUMBER = "run50BA"
PARENT_RUN_ID = "run50BA_stage56_context_timed_opportunity_source_v1"
PACKET_ID = "stage56_run50BA_context_timed_opportunity_source_v1"
EXPLORATION_LABEL = "stage56_BaseEngine__ContextTimedOpportunitySource"
BOUNDARY = "research_baseline_selection_only_no_operating_claim"
JUDGMENT = "in_progress_no_selected_research_baseline"
STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
PACKET_ROOT = Path("docs/agent_control/packets") / PACKET_ID
REPORT_PATH = REVIEWS_ROOT / "run50BA_context_timed_opportunity_source.md"
RESULTS_CSV_PATH = REVIEWS_ROOT / "run50BA_summary.csv"
AUDIT_CSV_PATH = REVIEWS_ROOT / "run50BA_audit.csv"
SOURCE_SUMMARY_CSV_PATH = REVIEWS_ROOT / "run50BA_source_summary.csv"
AGGREGATE_SUMMARY_PATH = PACKET_ROOT / "aggregate_summary.json"
RUN_REGISTRY_PATH = Path("docs/registers/run_registry.csv")
ARTIFACT_REGISTRY_PATH = Path("docs/registers/artifact_registry.csv")
STAGE_RUN_LEDGER_PATH = REVIEWS_ROOT / "stage_run_ledger.csv"
PROJECT_ALPHA_LEDGER_PATH = Path("docs/registers/alpha_run_ledger.csv")
PROGRESS_LOG_PATH = Path("docs/agent_control/packets/stage56_reopen_goal_v1/progress_log.md")
SELECTION_STATUS_PATH = STAGE_ROOT / "04_selected/selection_status.md"
WORKSPACE_STATE_PATH = Path("docs/workspace/workspace_state.yaml")
CURRENT_WORKING_STATE_PATH = Path("docs/context/current_working_state.md")
VALIDATION_DAYS = 183.0
OOS_DAYS = 195.0
SIGNAL_COLUMN = "stage56_context_timed_event_signal"
COMMON_ROOT = f"Project_Obsidian_Prime_v2/stage56/{RUN_NUMBER}_context_timed_opportunity_source"
SHORT_THRESHOLD = 0.55
LONG_THRESHOLD = 0.55
MIN_MARGIN = 0.0


@dataclass(frozen=True)
class SourceRef:
    stage_number: int
    candidate_id: str
    label: str

    @property
    def key(self) -> str:
        return f"s{self.stage_number}_{self.candidate_id}"


@dataclass(frozen=True)
class SlotRule:
    slot_index: int
    side: int
    feature: str
    op: str
    threshold: float
    rule_id: str


@dataclass(frozen=True)
class ContextTimedVariant:
    variant_id: str
    group: str
    slot_width_minutes: int
    rules: tuple[SlotRule, ...]
    max_hold_bars: int
    reentry_cooldown_bars: int
    routed_fallback_enabled: bool
    notes: str
    composite_mode: str
    primary: SourceRef = SourceRef(56, "context_timed_slot_source", "context timed slot source")
    secondary: SourceRef = SourceRef(56, "none", "no secondary source")


def rule(slot: int, side: int, feature: str, op: str, threshold: float, tag: str) -> SlotRule:
    return SlotRule(slot, side, feature, op, threshold, f"s{slot}_{'long' if side > 0 else 'short'}_{tag}")


DEFAULT_VARIANTS: tuple[ContextTimedVariant, ...] = (
    ContextTimedVariant(
        "v09_slot30_cycle_dense_h2c12_no_b",
        "slot30_context_cycle_density",
        30,
        (
            rule(0, 1, "bb_position_20", ">=", 0.21625104919075966, "bb_ge25"),
            rule(2, -1, "bb_position_20", "<=", 0.7814855724573135, "bb_le75"),
            rule(3, 1, "di_spread_14", ">=", -1.7898940443992615, "di_ge50"),
            rule(5, -1, "vix_zscore_20", ">=", -0.2129696011543274, "vix_ge50"),
            rule(7, 1, "adx_14", "<=", 30.660185470581055, "adx_le67"),
            rule(8, -1, "atr_14_over_atr_50", "<=", 1.0898461043834686, "atr_le25"),
            rule(11, 1, "us100_minus_mega8_equal_return_1", ">=", -0.00034740639239316806, "us_ge25"),
        ),
        2,
        12,
        False,
        "30-minute slot cycle with same-side spacing pressure and Tier B disabled in routed path.",
        "context_slot_cycle_dense",
    ),
    ContextTimedVariant(
        "v10_slot30_cycle_quality_h2c12_no_b",
        "slot30_context_cycle_quality",
        30,
        (
            rule(0, 1, "bb_position_20", ">=", 0.3001814126968384, "bb_ge33"),
            rule(2, -1, "di_spread_14", "<=", -11.482649803161621, "di_le25"),
            rule(3, 1, "di_spread_14", ">=", -1.7898940443992615, "di_ge50"),
            rule(5, -1, "vix_zscore_20", ">=", -0.2129696011543274, "vix_ge50"),
            rule(7, 1, "adx_14", "<=", 30.660185470581055, "adx_le67"),
            rule(8, -1, "atr_14_over_atr_50", "<=", 1.0898461043834686, "atr_le25"),
            rule(11, 1, "us100_minus_mega8_equal_return_1", ">=", -1.4847938928141957e-05, "us_ge50"),
        ),
        2,
        12,
        False,
        "Stricter context thresholds to test whether proxy quality survives actual MT5 density loss.",
        "context_slot_cycle_quality",
    ),
    ContextTimedVariant(
        "v11_slot30_dense_control_h2c12_with_b",
        "slot30_dense_tier_b_damage_probe",
        30,
        (
            rule(0, 1, "bb_position_20", ">=", 0.21625104919075966, "bb_ge25"),
            rule(1, 1, "bb_position_20", ">=", 0.7038815921545029, "bb_ge67"),
            rule(2, -1, "bb_position_20", "<=", 0.7814855724573135, "bb_le75"),
            rule(3, 1, "di_spread_14", ">=", -1.7898940443992615, "di_ge50"),
            rule(4, -1, "di_spread_14", "<=", -8.151259412765503, "di_le33"),
            rule(5, -1, "vix_zscore_20", ">=", -0.2129696011543274, "vix_ge50"),
            rule(7, 1, "adx_14", "<=", 30.660185470581055, "adx_le67"),
            rule(8, -1, "atr_14_over_atr_50", "<=", 1.0898461043834686, "atr_le25"),
            rule(9, -1, "vix_zscore_20", ">=", -0.2129696011543274, "vix_ge50"),
            rule(10, -1, "rsi_14", "<=", 50.00534248352051, "rsi_le50"),
            rule(11, 1, "us100_minus_mega8_equal_return_1", ">=", -0.00034740639239316806, "us_ge25"),
        ),
        2,
        12,
        True,
        "Dense control with Tier B fallback enabled to expose hidden OOS damage versus density recovery.",
        "context_slot_dense_control",
    ),
    ContextTimedVariant(
        "v12_slot30_early_mid_bias_h2c12_no_b",
        "slot30_early_mid_late_bias",
        30,
        (
            rule(0, 1, "bb_position_20", ">=", 0.21625104919075966, "bb_ge25"),
            rule(1, 1, "bb_position_20", ">=", 0.7038815921545029, "bb_ge67"),
            rule(3, 1, "return_zscore_20", ">=", 0.44723787158727646, "ret_ge67"),
            rule(4, -1, "di_spread_14", "<=", -8.151259412765503, "di_le33"),
            rule(5, -1, "vix_zscore_20", ">=", -0.2129696011543274, "vix_ge50"),
            rule(7, 1, "adx_14", "<=", 30.660185470581055, "adx_le67"),
            rule(10, -1, "rsi_14", "<=", 50.00534248352051, "rsi_le50"),
            rule(11, 1, "us100_minus_mega8_equal_return_1", ">=", -0.00034740639239316806, "us_ge25"),
        ),
        2,
        12,
        False,
        "Early/mid/late context bias branch to test whether broad daily distribution beats model thresholding.",
        "context_slot_early_mid_late_bias",
    ),
)


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str] | None = None) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    if columns is None:
        ordered: list[str] = []
        for row in rows:
            for key in row:
                if key not in ordered:
                    ordered.append(key)
        columns = tuple(ordered)
    with io_path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(columns), lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        writer.writerows([json_ready(row) for row in rows])


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(io_path(path).read_text(encoding="utf-8-sig"))


def selected_variants(args: argparse.Namespace) -> list[ContextTimedVariant]:
    variants = list(DEFAULT_VARIANTS)
    if args.variant_id:
        wanted = set(args.variant_id)
        variants = [variant for variant in variants if variant.variant_id in wanted]
    if args.max_variants is not None:
        variants = variants[: int(args.max_variants)]
    if not variants:
        raise RuntimeError("no run50BA variants selected")
    return variants


def variant_payload(variant: ContextTimedVariant) -> dict[str, Any]:
    return {
        "variant_id": variant.variant_id,
        "group": variant.group,
        "slot_width_minutes": variant.slot_width_minutes,
        "rules": [rule_item.__dict__ for rule_item in variant.rules],
        "max_hold_bars": variant.max_hold_bars,
        "reentry_cooldown_bars": variant.reentry_cooldown_bars,
        "routed_fallback_enabled": variant.routed_fallback_enabled,
        "composite_mode": variant.composite_mode,
        "notes": variant.notes,
    }


def _condition(frame: pd.DataFrame, rule_item: SlotRule) -> pd.Series:
    values = pd.to_numeric(frame[rule_item.feature], errors="coerce")
    if rule_item.op == ">=":
        return values.ge(rule_item.threshold)
    if rule_item.op == "<=":
        return values.le(rule_item.threshold)
    raise ValueError(f"unknown op: {rule_item.op}")


def build_variant_frame(common: pd.DataFrame, variant: ContextTimedVariant) -> pd.DataFrame:
    frame = common.copy()
    timestamp = pd.to_datetime(frame["timestamp"], utc=True)
    frame["_date"] = timestamp.dt.strftime("%Y-%m-%d")
    minutes = pd.to_numeric(frame["minutes_from_cash_open"], errors="coerce")
    frame["_slot"] = np.floor(minutes / float(variant.slot_width_minutes))
    frame[SIGNAL_COLUMN] = np.zeros(len(frame), dtype="int8")
    frame["context_rule_id"] = ""
    frame["context_slot"] = ""
    frame["context_slot_width_minutes"] = variant.slot_width_minutes
    frame["primary_signal"] = 0
    frame["secondary_signal"] = 0
    for rule_item in variant.rules:
        mask = (
            frame["_slot"].eq(rule_item.slot_index)
            & minutes.between(0, 389, inclusive="both")
            & _condition(frame, rule_item)
        )
        matches = frame.loc[mask].sort_values("timestamp").groupby(["split", "_date", "tier_label", "_slot"], sort=False).head(1)
        frame.loc[matches.index, SIGNAL_COLUMN] = np.int8(rule_item.side)
        frame.loc[matches.index, "context_rule_id"] = rule_item.rule_id
        frame.loc[matches.index, "context_slot"] = str(rule_item.slot_index)
        frame.loc[matches.index, "primary_signal"] = np.int8(rule_item.side)
    frame["variant_id"] = variant.variant_id
    frame["primary_source"] = variant.primary.key
    frame["secondary_source"] = variant.secondary.key
    frame["composite_mode"] = variant.composite_mode
    frame["entry_decision"] = frame[SIGNAL_COLUMN].map({-1: "short", 0: "flat", 1: "long"}).fillna("flat")
    return frame.drop(columns=["_date", "_slot"])


def source_summary_rows(variant: ContextTimedVariant, frame: pd.DataFrame) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for split in ("train", "validation", "oos"):
        for tier in (mt5.TIER_A, mt5.TIER_B):
            view = frame.loc[frame["split"].astype(str).eq(split) & frame["tier_label"].astype(str).eq(tier)]
            signal = pd.to_numeric(view[SIGNAL_COLUMN], errors="coerce").fillna(0).astype("int8")
            rows.append(
                {
                    "variant_id": variant.variant_id,
                    "split": split,
                    "tier": tier,
                    "slot_width_minutes": variant.slot_width_minutes,
                    "rule_count": len(variant.rules),
                    "rows": int(len(view)),
                    "context_nonflat": int(signal.ne(0).sum()),
                    "context_long": int(signal.eq(1).sum()),
                    "context_short": int(signal.eq(-1).sum()),
                    "context_rule_nonflat": json.dumps(
                        view.loc[signal.ne(0), "context_rule_id"].astype(str).value_counts().to_dict(),
                        ensure_ascii=False,
                        sort_keys=True,
                    ),
                }
            )
    return rows


def build_variant_frames(
    variants: Sequence[ContextTimedVariant],
    common: pd.DataFrame,
) -> tuple[dict[str, pd.DataFrame], list[dict[str, Any]], list[dict[str, Any]]]:
    frames: dict[str, pd.DataFrame] = {}
    summary_rows: list[dict[str, Any]] = []
    lineage = aw.source_lineage_entries()
    for role, path, affects in (
        ("run50AX_source_composite_evidence", Path("docs/agent_control/packets/stage56_run50AX_source_composite_density_quality_v1/aggregate_summary.json"), "density frontier and same-move failure memory"),
        ("run50AY_agreement_firewall_evidence", Path("docs/agent_control/packets/stage56_run50AY_agreement_firewall_density_recovery_v1/aggregate_summary.json"), "agreement firewall failure memory"),
        ("run50AZ_cooldown12_broad_source_evidence", Path("docs/agent_control/packets/stage56_run50AZ_cooldown12_broad_model_source_v1/aggregate_summary.json"), "broad source same-move improvement and density failure memory"),
    ):
        lineage.append(
            {
                "role": role,
                "path": rel(path),
                "sha256": sha256_file_lf_normalized(path) if path_exists(path) and io_path(path).is_file() else "missing",
                "artifact_kind": "prior_evidence",
                "affects": affects,
                "required_for_reproducibility": True,
            }
        )
    for variant in variants:
        frame = build_variant_frame(common, variant)
        frames[variant.variant_id] = frame
        summary_rows.extend(source_summary_rows(variant, frame))
    return frames, summary_rows, lineage


def export_model_artifact() -> dict[str, Any]:
    path = RUN_ROOT / "models" / "stage56_context_timed_event_signal_discrete_score_table.csv"
    return export_single_discrete_signal_score_table(
        path,
        feature_order=(SIGNAL_COLUMN,),
        logit_strength=4.0,
        format_name="stage56_context_timed_single_signal_ebm_table_csv_v1",
    )


def export_feature_matrix(path: Path, frame: pd.DataFrame) -> dict[str, Any]:
    payload = mt5.export_mt5_feature_matrix_csv(
        frame,
        (SIGNAL_COLUMN,),
        path,
        metadata_columns=(
            "variant_id",
            "primary_source",
            "secondary_source",
            "composite_mode",
            "context_rule_id",
            "context_slot",
            "context_slot_width_minutes",
            "tier_label",
            "routing_source",
            "partial_context_subtype",
            "entry_decision",
        ),
    )
    payload["path"] = rel(Path(payload["path"]))
    return payload


def export_candidate_feature_matrices(
    variants: Sequence[ContextTimedVariant],
    frames: Mapping[str, pd.DataFrame],
) -> dict[str, dict[str, Any]]:
    exports: dict[str, dict[str, Any]] = {}
    for variant in variants:
        frame = frames[variant.variant_id]
        for source_split, runtime_split, split_token in (("validation", "validation_is", "val"), ("oos", "oos", "oos")):
            split_frame = frame.loc[frame["split"].astype(str).eq(source_split)]
            for tier_value, tier_name, tier_token in (
                (mt5.TIER_A, "tier_a", "a"),
                (mt5.TIER_B, "tier_b_fallback", "b"),
            ):
                tier_frame = split_frame.loc[split_frame["tier_label"].astype(str).eq(tier_value)].copy()
                out_path = RUN_ROOT / variant.variant_id / "features" / f"{variant.variant_id}_{tier_token}_{split_token}.csv"
                exports[f"{variant.variant_id}_{tier_name}_{runtime_split}"] = export_feature_matrix(out_path, tier_frame)
    return exports


def resolve_artifact_path(value: Any) -> Path:
    path = Path(str(value))
    if path.is_absolute():
        return path
    if path_exists(REPO_ROOT / path):
        return REPO_ROOT / path
    return RUN_ROOT / path


def copy_runtime_inputs(
    feature_exports: Mapping[str, Mapping[str, Any]],
    model_artifact: Mapping[str, Any],
    common_files_root: Path,
) -> list[dict[str, Any]]:
    copied: list[dict[str, Any]] = []
    model_path = resolve_artifact_path(model_artifact["path"])
    copied.append(copy_to_common(model_path, f"{COMMON_ROOT}/models/{model_path.name}", common_files_root))
    for payload in feature_exports.values():
        local_path = resolve_artifact_path(payload["path"])
        copied.append(copy_to_common(local_path, f"{COMMON_ROOT}/features/{local_path.name}", common_files_root))
    return copied


def build_attempts(
    variants: Sequence[ContextTimedVariant],
    common: pd.DataFrame,
    feature_exports: Mapping[str, Mapping[str, Any]],
    model_artifact: Mapping[str, Any],
) -> list[dict[str, Any]]:
    attempts: list[dict[str, Any]] = []
    model_name = Path(str(model_artifact["path"])).name
    model_common = f"{COMMON_ROOT}/models/{model_name}"
    feature_hash = ordered_hash((SIGNAL_COLUMN,))
    extra_set_values = {
        "InpEntryTransitionOnly": False,
        "InpEntryTransitionRearmMinConfidenceDelta": 0.0,
        "InpAtrSltpEnabled": False,
        "InpAtrPeriod": 14,
        "InpAtrStopMultiplier": 0.0,
        "InpAtrTakeProfitMultiplier": 0.0,
    }
    for variant_index, variant in enumerate(variants, 1):
        variant_short = f"x{variant_index:02d}"
        variant_extra = {**extra_set_values, "InpReentryCooldownBars": int(variant.reentry_cooldown_bars)}
        for source_split, runtime_split in (("validation", "validation_is"), ("oos", "oos")):
            split_token = "val" if runtime_split == "validation_is" else "oos"
            split_frame = common.loc[
                common["split"].astype(str).eq(source_split)
                & common["tier_label"].astype(str).eq(mt5.TIER_A)
            ]
            from_date, to_date = split_dates_from_frame(split_frame, source_split)
            tier_a_matrix = Path(str(feature_exports[f"{variant.variant_id}_tier_a_{runtime_split}"]["path"])).name
            tier_b_matrix = Path(str(feature_exports[f"{variant.variant_id}_tier_b_fallback_{runtime_split}"]["path"])).name
            base_kwargs = {
                "run_root": RUN_ROOT / variant.variant_id,
                "run_id": f"{PARENT_RUN_ID}_{variant_short}",
                "stage_number": 56,
                "exploration_label": EXPLORATION_LABEL,
                "split": runtime_split,
                "model_path": model_common,
                "model_id": f"{PARENT_RUN_ID}_{variant.variant_id}_context_timed_signal_table",
                "model_backend": "ebm_table",
                "feature_count": 1,
                "feature_order_hash": feature_hash,
                "short_threshold": SHORT_THRESHOLD,
                "long_threshold": LONG_THRESHOLD,
                "min_margin": MIN_MARGIN,
                "invert_signal": False,
                "from_date": from_date,
                "to_date": to_date,
                "max_hold_bars": variant.max_hold_bars,
                "common_root": COMMON_ROOT,
                "close_on_flat_signal": False,
                "reverse_on_opposite_signal": True,
                "extra_set_values": variant_extra,
            }
            for role, role_token, tier, feature_path, primary_tier, record_prefix, fallback in (
                ("tier_a_only", "ta", mt5.TIER_A, f"{COMMON_ROOT}/features/{tier_a_matrix}", "tier_a", f"mt5_tier_a_only_{variant.variant_id}", False),
                ("tier_b_fallback_only", "tb", mt5.TIER_B, f"{COMMON_ROOT}/features/{tier_b_matrix}", "tier_b_fallback", f"mt5_tier_b_fallback_only_{variant.variant_id}", False),
                ("routed", "rt", mt5.TIER_AB, f"{COMMON_ROOT}/features/{tier_a_matrix}", "tier_a", f"mt5_routed_{variant.variant_id}", True),
            ):
                payload = attempt_payload(
                    **base_kwargs,
                    attempt_name=f"{variant_short}_{role_token}_{split_token}",
                    tier=tier,
                    feature_path=feature_path,
                    primary_active_tier=primary_tier,
                    attempt_role="routed_total" if role == "routed" else "tier_only_total",
                    record_view_prefix=record_prefix,
                    fallback_enabled=variant.routed_fallback_enabled if fallback else False,
                    fallback_model_path=model_common if fallback else None,
                    fallback_model_id=f"{PARENT_RUN_ID}_{variant.variant_id}_tier_b_context_timed_signal_table" if fallback else None,
                    fallback_model_backend="ebm_table" if fallback else None,
                    fallback_feature_path=f"{COMMON_ROOT}/features/{tier_b_matrix}" if fallback else None,
                    fallback_feature_count=1 if fallback else None,
                    fallback_feature_order_hash=feature_hash if fallback else None,
                    fallback_short_threshold=SHORT_THRESHOLD if fallback else None,
                    fallback_long_threshold=LONG_THRESHOLD if fallback else None,
                    fallback_min_margin=MIN_MARGIN if fallback else None,
                    fallback_invert_signal=False if fallback else None,
                )
                payload["variant_id"] = variant.variant_id
                payload["composite_mode"] = variant.composite_mode
                payload["context_rule_count"] = len(variant.rules)
                attempts.append(payload)
    return attempts


def execute_or_materialize(prepared: Mapping[str, Any], args: argparse.Namespace) -> dict[str, Any]:
    if args.materialize_only:
        return {
            **dict(prepared),
            "compile": {"status": "not_attempted_materialize_only"},
            "execution_results": [],
            "strategy_tester_reports": [],
            "mt5_kpi_records": [],
            "external_verification_status": "materialized_only",
            "judgment": "materialized_only_no_mt5_evidence",
        }
    return execute_prepared_run(
        prepared,
        terminal_path=Path(args.terminal_path),
        metaeditor_path=Path(args.metaeditor_path),
        terminal_data_root=Path(args.terminal_data_root),
        common_files_root=Path(args.common_files_root),
        tester_profile_root=Path(args.tester_profile_root),
        timeout_seconds=int(args.timeout_seconds),
    )


def configure_agreement_helpers() -> None:
    agreement.RUN_NUMBER = RUN_NUMBER
    agreement.PARENT_RUN_ID = PARENT_RUN_ID
    agreement.PACKET_ID = PACKET_ID
    agreement.EXPLORATION_LABEL = EXPLORATION_LABEL
    agreement.RUN_ROOT = RUN_ROOT
    agreement.REPORT_PATH = REPORT_PATH
    agreement.RESULTS_CSV_PATH = RESULTS_CSV_PATH
    agreement.AUDIT_CSV_PATH = AUDIT_CSV_PATH
    agreement.AGGREGATE_SUMMARY_PATH = AGGREGATE_SUMMARY_PATH
    agreement.STAGE_RUN_LEDGER_PATH = STAGE_RUN_LEDGER_PATH
    agreement.PROJECT_ALPHA_LEDGER_PATH = PROJECT_ALPHA_LEDGER_PATH
    agreement.RUN_REGISTRY_PATH = RUN_REGISTRY_PATH


def best_row(rows: Sequence[Mapping[str, Any]]) -> Mapping[str, Any] | None:
    return agreement.best_row(rows)


def fmt(value: Any) -> str:
    return agreement.fmt(value)


def write_report(rows: Sequence[Mapping[str, Any]], audit_rows: Sequence[Mapping[str, Any]], result: Mapping[str, Any]) -> None:
    best = best_row(rows) or {}
    lines = [
        "# Stage56 run50BA Context-Timed Opportunity Source(문맥/시간 기회 원천)",
        "",
        f"- run_id(실행 ID): `{PARENT_RUN_ID}`",
        f"- packet_id(묶음 ID): `{PACKET_ID}`",
        "- selected_research_baseline(선택 연구 기준선): `none`",
        f"- external_verification_status(외부 검증 상태): `{result.get('external_verification_status')}`",
        f"- claim_boundary(주장 경계): `{BOUNDARY}`",
        "",
        "Action(행동): 시간 슬롯(time slot, 시간 구간)별 첫 조건 충족 이벤트만 신호로 내보내 actual MT5 validation/OOS(실제 MT5 검증/표본외)를 실행했다.",
        "Effect(효과): OOS density(표본외 밀도)가 같은 이동 재진입(same-move re-entry, 동일 이동 재진입) 없이 살아나는지 모델 원천을 바꿔 확인한다.",
        "",
        "## Best Read(최선 판독)",
        "",
        f"- best_variant(최선 변형): `{best.get('variant_id', 'none')}`",
        f"- validation/OOS trades/day(검증/표본외 일 거래): `{fmt(best.get('routed_validation_trades_per_day'))}` / `{fmt(best.get('routed_oos_trades_per_day'))}`",
        f"- validation/OOS PF(검증/표본외 수익 팩터): `{fmt(best.get('routed_validation_pf'))}` / `{fmt(best.get('routed_oos_pf'))}`",
        f"- validation/OOS net(검증/표본외 순손익): `{fmt(best.get('routed_validation_net'))}` / `{fmt(best.get('routed_oos_net'))}`",
        f"- failure_reasons(실패 사유): `{best.get('failure_reasons', '')}`",
        "",
        "## Variant Summary(변형 요약)",
        "",
        "| variant | mode | fallback | val day | oos day | val PF | oos PF | val net | oos net | failures |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in rows:
        lines.append(
            "| {variant} | {mode} | {fallback} | {vday} | {oday} | {vpf} | {opf} | {vnet} | {onet} | {fail} |".format(
                variant=row.get("variant_id", ""),
                mode=row.get("composite_mode", ""),
                fallback=row.get("routed_fallback_enabled", ""),
                vday=fmt(row.get("routed_validation_trades_per_day")),
                oday=fmt(row.get("routed_oos_trades_per_day")),
                vpf=fmt(row.get("routed_validation_pf")),
                opf=fmt(row.get("routed_oos_pf")),
                vnet=fmt(row.get("routed_validation_net")),
                onet=fmt(row.get("routed_oos_net")),
                fail=row.get("failure_reasons", ""),
            )
        )
    lines.extend(
        [
            "",
            "## Tier Views(티어 보기)",
            "",
            "| variant | Tier A val/OOS net | Tier B-only val/OOS net | routed val/OOS net |",
            "|---|---:|---:|---:|",
        ]
    )
    for row in rows:
        lines.append(
            "| {variant} | {ta} / {tao} | {tb} / {tbo} | {rv} / {ro} |".format(
                variant=row.get("variant_id", ""),
                ta=fmt(row.get("tier_a_validation_net")),
                tao=fmt(row.get("tier_a_oos_net")),
                tb=fmt(row.get("tier_b_validation_net")),
                tbo=fmt(row.get("tier_b_oos_net")),
                rv=fmt(row.get("routed_validation_net")),
                ro=fmt(row.get("routed_oos_net")),
            )
        )
    lines.extend(
        [
            "",
            "## Audit Summary(감사 요약)",
            "",
            "| variant | split | MFE capture | same move | cooldown day | cost-stressed exp |",
            "|---|---|---:|---:|---:|---:|",
        ]
    )
    for row in audit_rows:
        variant = str(row.get("variant_id") or "")
        if not variant.startswith("v"):
            continue
        lines.append(
            "| {variant} | {split} | {mfe} | {same} | {cool} | {cse} |".format(
                variant=variant,
                split=row.get("split", ""),
                mfe=fmt(row.get("mfe_capture_ratio")),
                same=fmt(row.get("same_move_reentry_ratio")),
                cool=fmt(row.get("trades_per_day_after_cooldown")),
                cse=fmt(row.get("cost_stressed_expectancy")),
            )
        )
    lines.extend(
        [
            "",
            "Judgment(판정): `in_progress_no_selected_research_baseline`.",
            "Effect(효과): run50BA(실행50BA)는 progress evidence(진행 근거)이며 Stage56(56단계)는 계속 open(열림)이다.",
        ]
    )
    write_md(REPORT_PATH, "\n".join(lines))


def artifact_rows(
    result: Mapping[str, Any],
    variants: Sequence[ContextTimedVariant],
    lineage: Sequence[Mapping[str, Any]],
    extra_paths: Sequence[Path],
) -> list[dict[str, Any]]:
    created = utc_now()
    rows: list[dict[str, Any]] = []

    def add(artifact_id: str, artifact_type: str, path: Path | str, notes: str) -> None:
        p = Path(str(path))
        resolved = p if p.is_absolute() else REPO_ROOT / p
        is_file = path_exists(resolved) and io_path(resolved).is_file()
        sha = sha256_file_lf_normalized(resolved) if is_file else "directory_or_not_feasible"
        rows.append(
            {
                "artifact_id": artifact_id,
                "artifact_type": artifact_type,
                "path": rel(p),
                "sha256": sha,
                "stage_id": STAGE_ID,
                "run_id": PARENT_RUN_ID,
                "created_at_utc": created,
                "notes": notes,
            }
        )

    for path in extra_paths:
        add(f"stage56_{RUN_NUMBER}_{aw.safe_name(path.stem, 80)}", path.suffix.lstrip(".") or "artifact", path, "Stage56 run50BA evidence artifact.")
    for item in lineage:
        path = str(item.get("path") or "")
        if path:
            add(f"stage56_{RUN_NUMBER}_lineage_{aw.safe_name(str(item.get('role')), 60)}", str(item.get("artifact_kind") or "lineage"), path, str(item.get("affects") or "source lineage"))
    for report in result.get("strategy_tester_reports", []):
        html = report.get("html_report", {}) if isinstance(report.get("html_report"), Mapping) else {}
        if html.get("path"):
            add(f"stage56_{RUN_NUMBER}_mt5_report_{aw.safe_name(str(report.get('attempt_name') or report.get('report_name')), 100)}", "mt5_html_report", str(html["path"]), "Actual MT5 Strategy Tester HTML report.")
    for variant in variants:
        add(f"stage56_{RUN_NUMBER}_{variant.variant_id}_run_root", "run_root", RUN_ROOT / variant.variant_id, "Variant run directory; child artifact hashes are recorded separately.")
    return rows


def write_ledgers(result: Mapping[str, Any], variants: Sequence[ContextTimedVariant], artifacts: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    external = str(result.get("external_verification_status") or "blocked")
    run_rows = [
        {
            "run_id": PARENT_RUN_ID,
            "stage_id": STAGE_ID,
            "lane": "stage56_context_timed_opportunity_source",
            "status": "completed" if external == "completed" else "blocked",
            "judgment": JUDGMENT,
            "path": rel(RUN_ROOT),
            "notes": f"variant_count={len(variants)};selected_research_baseline=none;stage56_remains_open=1;boundary={BOUNDARY}",
        }
    ]
    for variant in variants:
        run_rows.append(
            {
                "run_id": f"{PARENT_RUN_ID}_{variant.variant_id}",
                "stage_id": STAGE_ID,
                "lane": "alpha_runtime_probe",
                "status": "reviewed" if external == "completed" else "blocked",
                "judgment": "inconclusive_single_split_scout_mt5_routed_completed" if external == "completed" else "blocked_mt5_execution",
                "path": rel(RUN_ROOT / variant.variant_id),
                "notes": f"mode={variant.composite_mode};views=tier_a_only,tier_b_fallback_only,routed_total;fallback_enabled={variant.routed_fallback_enabled};boundary=runtime_probe_only",
            }
        )
    run_payload = upsert_csv_rows(RUN_REGISTRY_PATH, RUN_REGISTRY_COLUMNS, run_rows, key="run_id")
    ledger_rows: list[dict[str, Any]] = []
    for variant in variants:
        records = [record for record in result.get("mt5_kpi_records", []) if f"_{variant.variant_id}_" in str(record.get("record_view"))]
        ledger_rows.extend(
            build_mt5_alpha_ledger_rows(
                run_id=f"{PARENT_RUN_ID}_{variant.variant_id}",
                stage_id=STAGE_ID,
                mt5_kpi_records=records,
                run_output_root=RUN_ROOT / variant.variant_id,
                external_verification_status=external,
            )
        )
    ledger_rows.append(
        {
            "ledger_row_id": f"{PARENT_RUN_ID}__parent_review",
            "stage_id": STAGE_ID,
            "run_id": PARENT_RUN_ID,
            "subrun_id": "parent_review",
            "parent_run_id": PARENT_RUN_ID,
            "record_view": "stage56_context_timed_opportunity_source_parent_review",
            "tier_scope": mt5.TIER_AB,
            "kpi_scope": "stage56_selected_research_baseline_search",
            "scoreboard_lane": "runtime_probe",
            "status": "completed" if external == "completed" else "blocked",
            "judgment": JUDGMENT,
            "path": rel(REPORT_PATH),
            "primary_kpi": "selected_research_baseline=none",
            "guardrail_kpi": f"completed_variants={len(variants)};terminal_condition=not_satisfied;stage56_remains_open=1;no_operating_claim=1",
            "external_verification_status": external,
            "notes": "run50BA context-timed opportunity source branch; actual MT5 evidence only.",
        }
    )
    stage_payload = upsert_csv_rows(STAGE_RUN_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, ledger_rows, key="ledger_row_id")
    project_payload = upsert_csv_rows(PROJECT_ALPHA_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, ledger_rows, key="ledger_row_id")
    artifact_payload = upsert_csv_rows(ARTIFACT_REGISTRY_PATH, aw.ARTIFACT_COLUMNS, list(artifacts), key="artifact_id")
    return {"run_registry": run_payload, "stage_ledger": stage_payload, "project_alpha_ledger": project_payload, "artifact_registry": artifact_payload}


def append_progress(best: Mapping[str, Any]) -> None:
    existing = io_path(PROGRESS_LOG_PATH).read_text(encoding="utf-8-sig") if path_exists(PROGRESS_LOG_PATH) else ""
    entry = f"""

## {utc_now()} run50BA Context-Timed Opportunity Source(문맥/시간 기회 원천)

- action(행동): slot/context rule(시간 구간/문맥 규칙)로 하루 여러 독립 신호를 만들고 actual MT5 validation/OOS(실제 MT5 검증/표본외)를 실행했다.
- effect(효과): threshold relaxation(문턱값 완화)이 아니라 opportunity source(기회 원천) 자체가 density/PF/net(밀도/수익 팩터/순손익)을 만들 수 있는지 확인했다.
- best_variant(현재 최선 변형): `{best.get('variant_id', 'none')}`
- validation/OOS trades/day(검증/표본외 일 거래): `{fmt(best.get('routed_validation_trades_per_day'))}` / `{fmt(best.get('routed_oos_trades_per_day'))}`
- validation/OOS PF(검증/표본외 수익 팩터): `{fmt(best.get('routed_validation_pf'))}` / `{fmt(best.get('routed_oos_pf'))}`
- validation/OOS net(검증/표본외 순손익): `{fmt(best.get('routed_validation_net'))}` / `{fmt(best.get('routed_oos_net'))}`
- decision(결정): selected_research_baseline(선택 연구 기준선)=`none`; failure_reasons(실패 사유)=`{best.get('failure_reasons', '')}`.
"""
    write_md(PROGRESS_LOG_PATH, existing.rstrip() + entry)


def update_workspace_state(best: Mapping[str, Any]) -> None:
    path = io_path(WORKSPACE_STATE_PATH)
    text = path.read_text(encoding="utf-8-sig")
    text = re.sub(r"^current_run_id: .*$", f"current_run_id: {PARENT_RUN_ID}", text, count=1, flags=re.MULTILINE)
    focus = (
        f"- Stage56(56단계) `{STAGE_ID}`: run50BA(실행50BA) context-timed opportunity source(문맥/시간 기회 원천) 완료; "
        f"best_variant(현재 최선 변형)은 `{best.get('variant_id', 'none')}`이고 validation/OOS(검증/표본외) trades/day(일 거래 수) "
        f"`{fmt(best.get('routed_validation_trades_per_day'))}` / `{fmt(best.get('routed_oos_trades_per_day'))}`, "
        f"PF(수익 팩터) `{fmt(best.get('routed_validation_pf'))}` / `{fmt(best.get('routed_oos_pf'))}`, "
        f"net(순손익) `{fmt(best.get('routed_validation_net'))}` / `{fmt(best.get('routed_oos_net'))}`이며 selected_research_baseline(선택 연구 기준선)은 `none`이다. "
        f"Effect(효과): `{best.get('failure_reasons', '')}` 때문에 hard condition(강한 완료 조건)을 통과하지 못해 Stage56(56단계)을 계속 open(열림)으로 둔다."
    )
    text = re.sub(r"current_focus:\n", f"current_focus:\n{focus}\n", text, count=1)
    block = (
        "\nstage56_run50ba_context_timed_opportunity_source:\n"
        f"  packet_id: {PACKET_ID}\n"
        f"  current_run_id: {PARENT_RUN_ID}\n"
        f"  best_variant: {best.get('variant_id', 'none')}\n"
        "  selected_research_baseline: none\n"
        f"  failure_reasons: {best.get('failure_reasons', '')}\n"
        "  boundary: research_baseline_selection_only_no_operating_claim\n"
        "  next_action: evaluate_context_timed_failure_or_open_separate_model_branch\n"
    )
    if "stage56_run50ba_context_timed_opportunity_source:" in text:
        text = re.sub(r"\nstage56_run50ba_context_timed_opportunity_source:\n(?:  .*\n?)*\Z", block, text.rstrip(), flags=re.M)
    else:
        text = text.rstrip() + "\n" + block
    path.write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def update_current_truth(rows: Sequence[Mapping[str, Any]]) -> None:
    best = best_row(rows) or {}
    best_id = best.get("variant_id", "none")
    failures = best.get("failure_reasons", "")
    val_day = fmt(best.get("routed_validation_trades_per_day"))
    oos_day = fmt(best.get("routed_oos_trades_per_day"))
    val_pf = fmt(best.get("routed_validation_pf"))
    oos_pf = fmt(best.get("routed_oos_pf"))
    val_net = fmt(best.get("routed_validation_net"))
    oos_net = fmt(best.get("routed_oos_net"))
    write_md(
        CURRENT_WORKING_STATE_PATH,
        f"""# Current Working State(현재 작업 상태)

- current_packet(현재 작업 묶음): `{PACKET_ID}`
- current run(현재 실행): `{PARENT_RUN_ID}`
- active stage(활성 단계): `{STAGE_ID}`
- selected_research_baseline(선택 연구 기준선): `none`
- status(상태): active_in_progress(활성 진행 중)
- terminal_condition(종료 조건): useful BaselineAdapter(유용한 기준선 어댑터) hard condition(강한 완료 조건) not_satisfied(미충족)

Stage56(56단계)는 unfinished optimization campaign(미완성 최적화 캠페인)으로 계속 열린다. Effect(효과): run50BA(실행50BA)는 context-timed opportunity source(문맥/시간 기회 원천)가 real density(실제 밀도)와 OOS quality(표본외 품질)를 동시에 만들 수 있는지 확인한 중간 근거다.

## Latest Evidence(최신 근거)

- latest_batch(최신 묶음): `{PARENT_RUN_ID}`
- best_variant(현재 최선 변형): `{best_id}`
- selected_research_baseline(선택 연구 기준선): `none`
- validation/OOS trades/day(검증/표본외 일 거래): `{val_day}` / `{oos_day}`
- validation/OOS PF(검증/표본외 수익 팩터): `{val_pf}` / `{oos_pf}`
- validation/OOS net(검증/표본외 순손익): `{val_net}` / `{oos_net}`

## Current Bottleneck(현재 병목)

- run50BA judgment(실행50BA 판정): selected_research_baseline(선택 연구 기준선)은 `none`이다. Effect(효과): failure_reasons(실패 사유) `{failures}` 때문에 hard condition(강한 완료 조건)을 통과하지 못했다.
- next_hypothesis_branch(다음 가설 분기): `evaluate_context_timed_failure_or_open_separate_model_branch`

Forbidden claims(금지 주장): live_readiness(실거래 준비), runtime_authority(런타임 권위), operating_promotion(운영 승격), operating_reference(운영 기준), production_baseline(운영 기준선), reviewed_closed(검토 종료).
""",
    )
    write_md(
        SELECTION_STATUS_PATH,
        f"""# Stage56 Selection Status(56단계 선택 상태)

- stage_status(단계 상태): `active_in_progress`
- latest_run_id(최신 실행 ID): `{PARENT_RUN_ID}`
- current run(현재 실행): `{PARENT_RUN_ID}`
- current_judgment(현재 판정): `in_progress_no_selected_research_baseline`
- selected_research_baseline(선택 연구 기준선): `none`
- latest_batch_best_variant_intermediate(최신 묶음 최선 변형 중간 근거): `{best_id}`

## Latest Run50BA Intermediate Evidence(최신 50BA 중간 근거)

- packet(묶음): `{PACKET_ID}`
- report(보고서): `{REPORT_PATH.as_posix()}`
- summary_csv(요약 CSV): `{RESULTS_CSV_PATH.as_posix()}`
- audit_csv(감사 CSV): `{AUDIT_CSV_PATH.as_posix()}`
- aggregate_summary(합산 요약): `{AGGREGATE_SUMMARY_PATH.as_posix()}`

Best read(최선 판독) `{best_id}` validation/OOS(검증/표본외) trades/day(일 거래 수) `{val_day}` / `{oos_day}`, PF(수익 팩터) `{val_pf}` / `{oos_pf}`, net(순손익) `{val_net}` / `{oos_net}`이다.

Failure(실패): `{failures}`. Effect(효과): selected_research_baseline(선택 연구 기준선)을 만들지 않고 Stage56(56단계)을 계속 open(열림)으로 둔다.
""",
    )
    append_progress(best)
    update_workspace_state(best)


def write_run_files(
    result: Mapping[str, Any],
    variants: Sequence[ContextTimedVariant],
    summary_rows: Sequence[Mapping[str, Any]],
    audit_rows: Sequence[Mapping[str, Any]],
    source_summary_rows_payload: Sequence[Mapping[str, Any]],
    source_lineage: Sequence[Mapping[str, Any]],
    ledger_payload: Mapping[str, Any],
) -> None:
    write_csv(RESULTS_CSV_PATH, summary_rows)
    write_csv(AUDIT_CSV_PATH, audit_rows, aw.reopen.AUDIT_COLUMNS)
    write_csv(SOURCE_SUMMARY_CSV_PATH, source_summary_rows_payload)
    write_json(RUN_ROOT / "run_manifest.json", {"run_id": PARENT_RUN_ID, "stage_id": STAGE_ID, "run_number": RUN_NUMBER, "packet_id": PACKET_ID, "variants": [variant_payload(variant) for variant in variants], "attempts": result.get("attempts", []), "common_copies": result.get("common_copies", []), "compile": result.get("compile", {}), "external_verification_status": result.get("external_verification_status"), "judgment": JUDGMENT, "boundary": BOUNDARY})
    write_json(RUN_ROOT / "kpi_record.json", {"run_id": PARENT_RUN_ID, "stage_id": STAGE_ID, "packet_id": PACKET_ID, "mt5_kpi_records": result.get("mt5_kpi_records", []), "strategy_tester_reports": result.get("strategy_tester_reports", []), "execution_results": result.get("execution_results", []), "external_verification_status": result.get("external_verification_status"), "judgment": JUDGMENT, "boundary": BOUNDARY})
    write_json(RUN_ROOT / "source_lineage.json", list(source_lineage))
    write_json(
        AGGREGATE_SUMMARY_PATH,
        {
            "run_id": PARENT_RUN_ID,
            "packet_id": PACKET_ID,
            "stage_id": STAGE_ID,
            "selected_research_baseline": "none",
            "stage56_remains_open": True,
            "terminal_condition": "not_satisfied",
            "external_verification_status": result.get("external_verification_status"),
            "best_variant": best_row(summary_rows),
            "summary_csv_path": RESULTS_CSV_PATH.as_posix(),
            "audit_csv_path": AUDIT_CSV_PATH.as_posix(),
            "source_summary_csv_path": SOURCE_SUMMARY_CSV_PATH.as_posix(),
            "report_path": REPORT_PATH.as_posix(),
            "ledger_payload": ledger_payload,
            "artifact_hashes": {
                "summary_csv_sha256": sha256_file_lf_normalized(RESULTS_CSV_PATH) if path_exists(RESULTS_CSV_PATH) else None,
                "audit_csv_sha256": sha256_file_lf_normalized(AUDIT_CSV_PATH) if path_exists(AUDIT_CSV_PATH) else None,
                "source_summary_csv_sha256": sha256_file_lf_normalized(SOURCE_SUMMARY_CSV_PATH) if path_exists(SOURCE_SUMMARY_CSV_PATH) else None,
                "report_sha256": sha256_file_lf_normalized(REPORT_PATH) if path_exists(REPORT_PATH) else None,
            },
            "forbidden_claims": {
                "live_readiness": False,
                "runtime_authority": False,
                "operating_promotion": False,
                "operating_reference": False,
                "production_baseline": False,
                "reviewed_closed": False,
            },
        },
    )


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Stage56 context-timed opportunity source branch.")
    parser.add_argument("--materialize-only", action="store_true")
    parser.add_argument("--variant-id", action="append", default=[])
    parser.add_argument("--max-variants", type=int)
    parser.add_argument("--cost-stress-per-trade", type=float, default=0.50)
    parser.add_argument("--common-files-root", default=str(COMMON_FILES_ROOT_DEFAULT))
    parser.add_argument("--terminal-data-root", default=str(TERMINAL_DATA_ROOT_DEFAULT))
    parser.add_argument("--tester-profile-root", default=str(TESTER_PROFILE_ROOT_DEFAULT))
    parser.add_argument("--terminal-path", default=str(TERMINAL_PATH_DEFAULT))
    parser.add_argument("--metaeditor-path", default=str(METAEDITOR_PATH_DEFAULT))
    parser.add_argument("--timeout-seconds", type=int, default=240)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    configure_agreement_helpers()
    args = parse_args(argv)
    variants = selected_variants(args)
    common, route_coverage, _ = aw.build_common_table()
    frames, source_summary, lineage = build_variant_frames(variants, common)
    model_artifact = export_model_artifact()
    feature_exports = export_candidate_feature_matrices(variants, frames)
    common_copies = copy_runtime_inputs(feature_exports, model_artifact, Path(args.common_files_root))
    attempts = build_attempts(variants, common, feature_exports, model_artifact)
    prepared = {
        "run_id": PARENT_RUN_ID,
        "stage_id": STAGE_ID,
        "stage_number": 56,
        "run_number": RUN_NUMBER,
        "run_root": RUN_ROOT,
        "packet_id": PACKET_ID,
        "attempts": attempts,
        "feature_exports": feature_exports,
        "model_artifacts": {"stage56_context_timed": model_artifact},
        "common_copies": common_copies,
        "route_coverage": route_coverage,
        "source_lineage": lineage,
        "python_candidate_summary": source_summary,
        "model_family": "context_timed_discrete_signal_score_table",
        "feature_set_id": "stage56_context_timed_event_signal",
        "label_id": "label_v1_fwd12_m5_logret_train_q33_3class",
        "split_contract": "split_v1_calendar_train_20220901_20241231_val_20250101_20250930_oos_20251001_20260413",
        "claim_boundary": BOUNDARY,
    }
    result = execute_or_materialize(prepared, args)
    audit_rows = agreement.audit_rows_for_result(result, variants, float(args.cost_stress_per_trade)) if result.get("mt5_kpi_records") else []
    summary_rows = agreement.build_summary_rows(variants, result.get("mt5_kpi_records", []), audit_rows)
    write_report(summary_rows, audit_rows, result)
    extra_paths = [
        REPORT_PATH,
        RESULTS_CSV_PATH,
        AUDIT_CSV_PATH,
        SOURCE_SUMMARY_CSV_PATH,
        RUN_ROOT / "run_manifest.json",
        RUN_ROOT / "kpi_record.json",
        RUN_ROOT / "source_lineage.json",
        AGGREGATE_SUMMARY_PATH,
        Path(str(model_artifact["path"])),
        Path(__file__).resolve(),
    ]
    artifacts = artifact_rows(result, variants, lineage, extra_paths)
    ledger_payload = write_ledgers(result, variants, artifacts)
    write_run_files(result, variants, summary_rows, audit_rows, source_summary, lineage, ledger_payload)
    artifacts = artifact_rows(result, variants, lineage, extra_paths)
    ledger_payload = write_ledgers(result, variants, artifacts)
    write_json(AGGREGATE_SUMMARY_PATH, {**read_json(AGGREGATE_SUMMARY_PATH), "ledger_payload": ledger_payload})
    aggregate_artifact = [
        row
        for row in artifact_rows(result, variants, lineage, [AGGREGATE_SUMMARY_PATH])
        if row.get("artifact_id") == f"stage56_{RUN_NUMBER}_{aw.safe_name(AGGREGATE_SUMMARY_PATH.stem, 80)}"
    ]
    if aggregate_artifact:
        upsert_csv_rows(ARTIFACT_REGISTRY_PATH, aw.ARTIFACT_COLUMNS, aggregate_artifact, key="artifact_id")
    if summary_rows:
        update_current_truth(summary_rows)
    print(
        json.dumps(
            json_ready(
                {
                    "status": "ok",
                    "run_id": PARENT_RUN_ID,
                    "selected_research_baseline": "none",
                    "stage56_remains_open": True,
                    "external_verification_status": result.get("external_verification_status"),
                    "summary_csv": RESULTS_CSV_PATH.as_posix(),
                    "audit_csv": AUDIT_CSV_PATH.as_posix(),
                    "aggregate_summary": AGGREGATE_SUMMARY_PATH.as_posix(),
                    "best_variant": best_row(summary_rows),
                }
            ),
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
