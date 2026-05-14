from __future__ import annotations

import argparse
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
from stage_pipelines.stage56 import independent_event_source_route_branch as aw  # noqa: E402


STAGE_ID = "56_base_engine__dense_tier_a_engine_and_tier_b_fallback_selection"
RUN_NUMBER = "run50AY"
PARENT_RUN_ID = "run50AY_stage56_agreement_firewall_density_recovery_v1"
PACKET_ID = "stage56_run50AY_agreement_firewall_density_recovery_v1"
EXPLORATION_LABEL = "stage56_BaseEngine__AgreementFirewallDensityRecovery"
BOUNDARY = "research_baseline_selection_only_no_operating_claim"
JUDGMENT = "in_progress_no_selected_research_baseline"
STAGE_ROOT = Path("stages") / STAGE_ID
RUN_ROOT = STAGE_ROOT / "02_runs" / RUN_NUMBER
REVIEWS_ROOT = STAGE_ROOT / "03_reviews"
PACKET_ROOT = Path("docs/agent_control/packets") / PACKET_ID
REPORT_PATH = REVIEWS_ROOT / "run50AY_agreement_firewall_density_recovery.md"
RESULTS_CSV_PATH = REVIEWS_ROOT / "run50AY_summary.csv"
AUDIT_CSV_PATH = REVIEWS_ROOT / "run50AY_audit.csv"
SOURCE_SUMMARY_CSV_PATH = REVIEWS_ROOT / "run50AY_source_summary.csv"
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
SIGNAL_COLUMN = "stage56_agreement_firewall_event_signal"
COMMON_ROOT = f"Project_Obsidian_Prime_v2/stage56/{RUN_NUMBER}_agreement_firewall_density_recovery"
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
class CompositeVariant:
    variant_id: str
    group: str
    primary: SourceRef
    secondary: SourceRef
    composite_mode: str
    max_hold_bars: int
    reentry_cooldown_bars: int
    routed_fallback_enabled: bool
    notes: str


S45C04 = SourceRef(45, "c04_histvol_ratio_expansion", "realized volatility expansion")
S47C03 = SourceRef(47, "c03_majority_agreement", "majority agreement signal")

DEFAULT_VARIANTS: tuple[CompositeVariant, ...] = (
    CompositeVariant(
        "v05_s47_breadth_vix_h3c3_no_b",
        "agreement_core_s47_context_recovery",
        S47C03,
        S45C04,
        "agreement_plus_s47_breadth_vix",
        3,
        3,
        False,
        "Agreement core plus Stage47-only recovery when mega8 breadth >= 0.50 and VIX zscore < 1.402633; Tier B fallback disabled in routed path.",
    ),
    CompositeVariant(
        "v06_s47_us100_vix_h3c3_no_b",
        "agreement_core_s47_relative_weakness_recovery",
        S47C03,
        S45C04,
        "agreement_plus_s47_us100_vix",
        3,
        3,
        False,
        "Agreement core plus Stage47-only recovery when US100 underperforms mega8 by validation q25 and VIX zscore < 1.402633; Tier B fallback disabled in routed path.",
    ),
    CompositeVariant(
        "v07_s47_s45_context_h2c2_no_b",
        "agreement_core_dual_context_recovery",
        S47C03,
        S45C04,
        "agreement_plus_s47_breadth_vix_s45_low_adx",
        2,
        2,
        False,
        "Agreement core plus Stage47 breadth/VIX recovery and Stage45 low-ADX recovery; shorter lifecycle probes density without Tier B fallback.",
    ),
    CompositeVariant(
        "v08_s47_s45_context_h3c3_with_b",
        "agreement_core_dual_context_recovery_tier_b_audit",
        S47C03,
        S45C04,
        "agreement_plus_s47_breadth_vix_s45_low_adx",
        3,
        3,
        True,
        "Same context recovery as v07 with Tier B fallback enabled to expose whether fallback creates hidden OOS damage.",
    ),
)


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    try:
        return path.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def write_json(path: Path, payload: Any) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(json.dumps(json_ready(payload), ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_md(path: Path, text: str) -> None:
    io_path(path.parent).mkdir(parents=True, exist_ok=True)
    io_path(path).write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def write_csv(path: Path, rows: Sequence[Mapping[str, Any]], columns: Sequence[str] | None = None) -> None:
    aw.write_csv(path, rows, columns)


def selected_variants(args: argparse.Namespace) -> list[CompositeVariant]:
    variants = list(DEFAULT_VARIANTS)
    if args.variant_id:
        wanted = set(args.variant_id)
        variants = [variant for variant in variants if variant.variant_id in wanted]
    if args.max_variants is not None:
        variants = variants[: int(args.max_variants)]
    if not variants:
        raise RuntimeError("no run50AY variants selected")
    return variants


def variant_payload(variant: CompositeVariant) -> dict[str, Any]:
    return {
        "variant_id": variant.variant_id,
        "group": variant.group,
        "primary": variant.primary.__dict__,
        "secondary": variant.secondary.__dict__,
        "composite_mode": variant.composite_mode,
        "max_hold_bars": variant.max_hold_bars,
        "reentry_cooldown_bars": variant.reentry_cooldown_bars,
        "routed_fallback_enabled": variant.routed_fallback_enabled,
        "notes": variant.notes,
    }


def source_frame(common: pd.DataFrame, source: SourceRef, context_cache: dict[int, Mapping[str, Any]]) -> pd.DataFrame:
    topic = aw.STAGE_TOPICS[source.stage_number]
    context = context_cache.setdefault(source.stage_number, aw.build_stage_model_context(common, topic))
    specs = {spec.candidate_id: spec for spec in aw.build_broad_candidate_grid(topic)}
    spec = specs[source.candidate_id]
    frame = aw.apply_candidate_to_table(common, topic, spec, context)
    return pd.DataFrame(
        {
            "stage56_event_source_row_id": common["stage56_event_source_row_id"].to_numpy(),
            source.key: pd.to_numeric(frame[topic.signal_column], errors="coerce").fillna(0).astype("int8").to_numpy(),
        }
    )


def _numeric(frame: pd.DataFrame, column: str) -> pd.Series:
    return pd.to_numeric(frame[column], errors="coerce")


def combine_signals(frame: pd.DataFrame, primary: pd.Series, secondary: pd.Series, mode: str) -> pd.Series:
    p = pd.to_numeric(primary, errors="coerce").fillna(0).astype("int8")
    s = pd.to_numeric(secondary, errors="coerce").fillna(0).astype("int8")
    agree = p.ne(0) & p.eq(s)
    s47_only = p.ne(0) & s.eq(0)
    s45_only = s.ne(0) & p.eq(0)
    s47_breadth_vix = (
        s47_only
        & _numeric(frame, "mega8_pos_breadth_1").ge(0.50)
        & _numeric(frame, "vix_zscore_20").lt(1.402633)
    )
    s47_us100_vix = (
        s47_only
        & _numeric(frame, "us100_minus_mega8_equal_return_1").lt(-0.000296751)
        & _numeric(frame, "vix_zscore_20").lt(1.402633)
    )
    s45_low_adx = (
        s45_only
        & _numeric(frame, "adx_14").lt(18.214526)
        & _numeric(frame, "minutes_from_cash_open").ge(35.0)
    )
    if mode == "primary_flatfill":
        signal = np.where(p.ne(0), p, s)
    elif mode == "no_conflict_union":
        conflict = p.ne(0) & s.ne(0) & p.ne(s)
        signal = np.where(conflict, 0, np.where(p.ne(0), p, s))
    elif mode == "agreement_only":
        signal = np.where(agree, p, 0)
    elif mode == "agreement_plus_s47_breadth_vix":
        signal = np.where(agree | s47_breadth_vix, p, 0)
    elif mode == "agreement_plus_s47_us100_vix":
        signal = np.where(agree | s47_us100_vix, p, 0)
    elif mode == "agreement_plus_s47_breadth_vix_s45_low_adx":
        signal = np.where(agree | s47_breadth_vix, p, np.where(s45_low_adx, s, 0))
    else:
        raise ValueError(f"unknown composite mode: {mode}")
    return pd.Series(signal, index=primary.index, dtype="int8")


def build_variant_frames(
    variants: Sequence[CompositeVariant],
    common: pd.DataFrame,
) -> tuple[dict[str, pd.DataFrame], list[dict[str, Any]], dict[str, Any], list[dict[str, Any]]]:
    context_cache: dict[int, Mapping[str, Any]] = {}
    source_cache: dict[str, pd.DataFrame] = {}
    frames: dict[str, pd.DataFrame] = {}
    summary_rows: list[dict[str, Any]] = []
    lineage: list[dict[str, Any]] = aw.source_lineage_entries()
    lineage.append(
        {
            "role": "run50AW_source_evidence",
            "path": rel(Path("docs/agent_control/packets/stage56_run50AW_independent_event_source_route_v1/aggregate_summary.json")),
            "sha256": sha256_file_lf_normalized(Path("docs/agent_control/packets/stage56_run50AW_independent_event_source_route_v1/aggregate_summary.json")),
            "artifact_kind": "prior_evidence",
            "affects": "agreement firewall density recovery branch design",
            "required_for_reproducibility": True,
        }
    )
    for variant in variants:
        for source in (variant.primary, variant.secondary):
            source_cache.setdefault(source.key, source_frame(common, source, context_cache))
        frame = common.copy()
        frame = frame.merge(source_cache[variant.primary.key], on="stage56_event_source_row_id", how="left")
        frame = frame.merge(source_cache[variant.secondary.key], on="stage56_event_source_row_id", how="left")
        frame["primary_signal"] = pd.to_numeric(frame[variant.primary.key], errors="coerce").fillna(0).astype("int8")
        frame["secondary_signal"] = pd.to_numeric(frame[variant.secondary.key], errors="coerce").fillna(0).astype("int8")
        frame[SIGNAL_COLUMN] = combine_signals(frame, frame["primary_signal"], frame["secondary_signal"], variant.composite_mode)
        frame["variant_id"] = variant.variant_id
        frame["primary_source"] = variant.primary.key
        frame["secondary_source"] = variant.secondary.key
        frame["composite_mode"] = variant.composite_mode
        frame["entry_decision"] = frame[SIGNAL_COLUMN].map({-1: "short", 0: "flat", 1: "long"}).fillna("flat")
        frames[variant.variant_id] = frame
        summary_rows.extend(source_summary_rows(variant, frame))
    context_manifest = {
        f"stage{stage}": aw.model_context_manifest(context)
        for stage, context in context_cache.items()
    }
    return frames, summary_rows, context_manifest, lineage


def source_summary_rows(variant: CompositeVariant, frame: pd.DataFrame) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for split in ("validation", "oos"):
        for tier in (mt5.TIER_A, mt5.TIER_B):
            view = frame.loc[frame["split"].astype(str).eq(split) & frame["tier_label"].astype(str).eq(tier)]
            p = pd.to_numeric(view["primary_signal"], errors="coerce").fillna(0)
            s = pd.to_numeric(view["secondary_signal"], errors="coerce").fillna(0)
            c = pd.to_numeric(view[SIGNAL_COLUMN], errors="coerce").fillna(0)
            rows.append(
                {
                    "variant_id": variant.variant_id,
                    "split": split,
                    "tier": tier,
                    "primary_source": variant.primary.key,
                    "secondary_source": variant.secondary.key,
                    "composite_mode": variant.composite_mode,
                    "rows": int(len(view)),
                    "primary_nonflat": int(p.ne(0).sum()),
                    "secondary_nonflat": int(s.ne(0).sum()),
                    "composite_nonflat": int(c.ne(0).sum()),
                    "source_agree_nonflat": int((p.ne(0) & p.eq(s)).sum()),
                    "source_conflict_nonflat": int((p.ne(0) & s.ne(0) & p.ne(s)).sum()),
                    "composite_long": int(c.eq(1).sum()),
                    "composite_short": int(c.eq(-1).sum()),
                }
            )
    return rows


def export_model_artifact() -> dict[str, Any]:
    path = RUN_ROOT / "models" / "stage56_composite_event_signal_discrete_score_table.csv"
    return export_single_discrete_signal_score_table(
        path,
        feature_order=(SIGNAL_COLUMN,),
        logit_strength=4.0,
        format_name="stage56_agreement_firewall_single_signal_ebm_table_csv_v1",
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
            "tier_label",
            "routing_source",
            "partial_context_subtype",
            "entry_decision",
        ),
    )
    payload["path"] = rel(Path(payload["path"]))
    return payload


def export_candidate_feature_matrices(
    variants: Sequence[CompositeVariant],
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
    variants: Sequence[CompositeVariant],
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
                "model_id": f"{PARENT_RUN_ID}_{variant.variant_id}_composite_signal_table",
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
                    fallback_model_id=f"{PARENT_RUN_ID}_{variant.variant_id}_tier_b_composite_signal_table" if fallback else None,
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
                payload["primary_source"] = variant.primary.key
                payload["secondary_source"] = variant.secondary.key
                payload["composite_mode"] = variant.composite_mode
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


def split_days(split: str) -> float:
    return VALIDATION_DAYS if split == "validation_is" else OOS_DAYS


def audit_rows_for_result(result: Mapping[str, Any], variants: Sequence[CompositeVariant], cost_stress_per_trade: float) -> list[dict[str, Any]]:
    market_data = MarketData.load(REPO_ROOT)
    reference_audits, reference_capture = aw.reopen._reference_capture_by_split(market_data, cost_stress_per_trade)
    by_view = {str(record.get("record_view")): record for record in result.get("mt5_kpi_records", [])}
    rows: list[dict[str, Any]] = list(reference_audits)
    for variant in variants:
        variant_run_id = f"{PARENT_RUN_ID}_{variant.variant_id}"
        for split in ("validation_is", "oos"):
            record_view = f"mt5_routed_{variant.variant_id}_{split}"
            record = by_view.get(record_view, {})
            report_path = aw.report_path_from_record(record)
            if not report_path:
                rows.append(
                    {
                        "variant_id": variant.variant_id,
                        "run_id": variant_run_id,
                        "record_view": record_view,
                        "split": split,
                        "status": "missing_report",
                        "report_path": "",
                        "error": "report_path_missing",
                    }
                )
                continue
            rows.append(
                aw.reopen._audit_report(
                    variant_id=variant.variant_id,
                    run_id=variant_run_id,
                    record_view=record_view,
                    report_path=Path(report_path),
                    market_data=market_data,
                    cost_stress_per_trade=cost_stress_per_trade,
                    reference_capture=reference_capture.get(split),
                )
            )
    return rows


def build_summary_rows(
    variants: Sequence[CompositeVariant],
    kpi_records: Sequence[Mapping[str, Any]],
    audit_rows: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    by_record = {str(record.get("record_view")): record for record in kpi_records}
    audits = {
        (str(row.get("variant_id")), str(row.get("record_view"))): row
        for row in audit_rows
        if str(row.get("variant_id", "")).startswith("v")
    }
    rows: list[dict[str, Any]] = []
    for variant in variants:
        row: dict[str, Any] = {
            "variant_id": variant.variant_id,
            "group": variant.group,
            "primary_source": variant.primary.key,
            "secondary_source": variant.secondary.key,
            "composite_mode": variant.composite_mode,
            "max_hold_bars": variant.max_hold_bars,
            "reentry_cooldown_bars": variant.reentry_cooldown_bars,
            "routed_fallback_enabled": variant.routed_fallback_enabled,
            "notes": variant.notes,
        }
        for split in ("validation_is", "oos"):
            split_prefix = "validation" if split == "validation_is" else "oos"
            for view_name, record_view in (
                ("tier_a", f"mt5_tier_a_only_{variant.variant_id}_{split}"),
                ("tier_b", f"mt5_tier_b_fallback_only_{variant.variant_id}_{split}"),
                ("routed", f"mt5_routed_{variant.variant_id}_{split}"),
            ):
                record = by_record.get(record_view, {})
                trade_count = aw.as_float(aw.mt5_metric(record, "trade_count", "total_trades"), 0.0)
                row[f"{view_name}_{split_prefix}_net"] = aw.mt5_metric(record, "net_profit")
                row[f"{view_name}_{split_prefix}_pf"] = aw.mt5_metric(record, "profit_factor")
                row[f"{view_name}_{split_prefix}_trades"] = aw.mt5_metric(record, "trade_count", "total_trades")
                row[f"{view_name}_{split_prefix}_trades_per_day"] = None if trade_count is None else trade_count / split_days(split)
                row[f"{view_name}_{split_prefix}_max_dd"] = aw.mt5_metric(record, "max_drawdown_amount", "max_drawdown")
                row[f"{view_name}_{split_prefix}_expectancy"] = aw.mt5_metric(record, "expectancy")
                row[f"{view_name}_{split_prefix}_report_path"] = aw.report_path_from_record(record)
            audit = audits.get((variant.variant_id, f"mt5_routed_{variant.variant_id}_{split}"), {})
            row[f"routed_{split_prefix}_cost_stressed_expectancy"] = audit.get("cost_stressed_expectancy")
            row[f"routed_{split_prefix}_mfe_capture_ratio"] = audit.get("mfe_capture_ratio")
            row[f"routed_{split_prefix}_same_move_reentry_ratio"] = audit.get("same_move_reentry_ratio")
            row[f"routed_{split_prefix}_trades_per_day_after_12bar_cooldown"] = audit.get("trades_per_day_after_cooldown")
            row[f"routed_{split_prefix}_density_gain_survives_12bar_cooldown"] = audit.get("density_gain_survives_12bar_cooldown")
        failed = aw.failure_reasons(row)
        row["passed_stage56_research_baseline_gate"] = not failed
        row["failure_reasons"] = ";".join(failed)
        rows.append(row)
    rows.sort(key=aw.best_row_sort_key, reverse=True)
    return rows


def best_row(rows: Sequence[Mapping[str, Any]]) -> Mapping[str, Any] | None:
    return max(rows, key=aw.best_row_sort_key) if rows else None


def fmt(value: Any) -> str:
    return aw.fmt(value)


def write_report(rows: Sequence[Mapping[str, Any]], audit_rows: Sequence[Mapping[str, Any]], result: Mapping[str, Any]) -> None:
    best = best_row(rows) or {}
    lines = [
        "# Stage56 run50AY Agreement Firewall Density Recovery(합의 방화벽 밀도 회복)",
        "",
        f"- run_id(실행 ID): `{PARENT_RUN_ID}`",
        f"- packet_id(묶음 ID): `{PACKET_ID}`",
        "- selected_research_baseline(선택 연구 기준선): `none`",
        f"- external_verification_status(외부 검증 상태): `{result.get('external_verification_status')}`",
        f"- claim_boundary(주장 경계): `{BOUNDARY}`",
        "",
        "Action(행동): run50AX(실행50AX)의 trade attribution(거래 귀속)에서 agreement core(합의 핵심)는 살리고 single-source gap(단일 원천 빈칸)은 context firewall(문맥 방화벽)로 제한해 실제 MT5 routed path(라우팅 경로)에서 시험했다.",
        "Effect(효과): density recovery(밀도 회복)가 same-move split(동일 이동 분할)과 Tier B damage(티어 B 손상) 없이 살아나는지 확인한다.",
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
        "| variant | mode | val day | oos day | val PF | oos PF | val net | oos net | failures |",
        "|---|---|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in rows:
        lines.append(
            "| {variant} | {mode} | {vday} | {oday} | {vpf} | {opf} | {vnet} | {onet} | {fail} |".format(
                variant=row.get("variant_id", ""),
                mode=row.get("composite_mode", ""),
                vday=fmt(row.get("routed_validation_trades_per_day")),
                oday=fmt(row.get("routed_oos_trades_per_day")),
                vpf=fmt(row.get("routed_validation_pf")),
                opf=fmt(row.get("routed_oos_pf")),
                vnet=fmt(row.get("routed_validation_net")),
                onet=fmt(row.get("routed_oos_net")),
                fail=row.get("failure_reasons", ""),
            )
        )
    lines.extend(["", "## Audit Summary(감사 요약)", "", "| variant | split | MFE capture | same move | cooldown day | cost-stressed exp |", "|---|---|---:|---:|---:|---:|"])
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
    lines.extend(["", "Judgment(판정): `in_progress_no_selected_research_baseline`.", "Effect(효과): run50AY(실행50AY)는 progress evidence(진행 근거)이고 Stage56(56단계)은 계속 open(열림)이다."])
    write_md(REPORT_PATH, "\n".join(lines))


def artifact_rows(result: Mapping[str, Any], variants: Sequence[CompositeVariant], lineage: Sequence[Mapping[str, Any]], extra_paths: Sequence[Path]) -> list[dict[str, Any]]:
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
        add(f"stage56_{RUN_NUMBER}_{aw.safe_name(path.stem, 80)}", path.suffix.lstrip(".") or "artifact", path, "Stage56 run50AY evidence artifact.")
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


def write_ledgers(result: Mapping[str, Any], variants: Sequence[CompositeVariant], artifacts: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    external = str(result.get("external_verification_status") or "blocked")
    run_rows = [
        {
            "run_id": PARENT_RUN_ID,
            "stage_id": STAGE_ID,
            "lane": "stage56_agreement_firewall_density_recovery",
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
                "notes": f"primary={variant.primary.key};secondary={variant.secondary.key};mode={variant.composite_mode};views=tier_a_only,tier_b_fallback_only,routed_total;boundary=runtime_probe_only",
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
            "record_view": "stage56_agreement_firewall_density_recovery_parent_review",
            "tier_scope": mt5.TIER_AB,
            "kpi_scope": "stage56_selected_research_baseline_search",
            "scoreboard_lane": "runtime_probe",
            "status": "completed" if external == "completed" else "blocked",
            "judgment": JUDGMENT,
            "path": rel(REPORT_PATH),
            "primary_kpi": "selected_research_baseline=none",
            "guardrail_kpi": f"completed_variants={len(variants)};terminal_condition=not_satisfied;stage56_remains_open=1;no_operating_claim=1",
            "external_verification_status": external,
            "notes": "run50AY agreement firewall density recovery branch; actual MT5 evidence only.",
        }
    )
    stage_payload = upsert_csv_rows(STAGE_RUN_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, ledger_rows, key="ledger_row_id")
    project_payload = upsert_csv_rows(PROJECT_ALPHA_LEDGER_PATH, ALPHA_LEDGER_COLUMNS, ledger_rows, key="ledger_row_id")
    artifact_payload = upsert_csv_rows(ARTIFACT_REGISTRY_PATH, aw.ARTIFACT_COLUMNS, list(artifacts), key="artifact_id")
    return {"run_registry": run_payload, "stage_ledger": stage_payload, "project_alpha_ledger": project_payload, "artifact_registry": artifact_payload}


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

Stage56(56단계)는 unfinished optimization campaign(미완성 최적화 캠페인)으로 계속 열린다. Effect(효과): run50AY(실행50AY)는 agreement core(합의 핵심)에 context firewall(문맥 방화벽)을 붙여 OOS density(표본외 밀도)와 quality(품질)가 함께 살아나는지 확인한 중간 근거다.

## Latest Evidence(최신 근거)

- latest_batch(최신 묶음): `{PARENT_RUN_ID}`
- best_variant(현재 최선 변형): `{best_id}`
- selected_research_baseline(선택 연구 기준선): `none`
- validation/OOS trades/day(검증/표본외 일 거래): `{val_day}` / `{oos_day}`
- validation/OOS PF(검증/표본외 수익 팩터): `{val_pf}` / `{oos_pf}`
- validation/OOS net(검증/표본외 순손익): `{val_net}` / `{oos_net}`

## Current Bottleneck(현재 병목)

- run50AY judgment(실행50AY 판정): selected_research_baseline(선택 연구 기준선)은 `none`이다. Effect(효과): failure_reasons(실패 사유) `{failures}` 때문에 hard condition(강한 조건)을 넘지 못한다.
- next_hypothesis_branch(다음 가설 분기): `continue_agreement_firewall_or_open_new_model_branch`

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

## Latest Run50AY Intermediate Evidence(최신 50AY 중간 근거)

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


def append_progress(best: Mapping[str, Any]) -> None:
    existing = io_path(PROGRESS_LOG_PATH).read_text(encoding="utf-8-sig") if path_exists(PROGRESS_LOG_PATH) else ""
    existing = re.sub(
        r"\n## [^\n]* run50AY Agreement Firewall Density Recovery\(합의 방화벽 밀도 회복\)\n.*?(?=\n## |\Z)",
        "",
        existing.rstrip(),
        flags=re.S,
    )
    entry = f"""

## {utc_now()} run50AY Agreement Firewall Density Recovery(합의 방화벽 밀도 회복)

- action(행동): run50AX(실행50AX) trade attribution(거래 귀속)에서 드러난 agreement core(합의 핵심)를 유지하고, single-source gap(단일 원천 빈칸)을 context firewall(문맥 방화벽)로 제한해 actual MT5 validation/OOS(실제 MT5 검증/표본외)를 실행했다.
- effect(효과): density recovery(밀도 회복)가 same-move split(동일 이동 분할)과 Tier B damage(티어 B 손상) 없이 살아나는지 기록했다.
- correction(정정): Tier B fallback(티어 B 대체)은 일부 변형에서 disabled(비활성화)하고, 별도 Tier B fallback-only(대체 단독) 실행으로 손상 여부를 기록했다. Effect(효과): fallback(대체)이 hidden OOS damage(숨은 표본외 손상)를 만들었는지 분리해서 볼 수 있다.
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
        f"- Stage56(56단계) `{STAGE_ID}`: run50AY(실행50AY) agreement firewall density recovery(합의 방화벽 밀도 회복) 완료; "
        f"best_variant(현재 최선 변형)은 `{best.get('variant_id', 'none')}`이고 validation/OOS(검증/표본외) trades/day(일 거래 수) "
        f"`{fmt(best.get('routed_validation_trades_per_day'))}` / `{fmt(best.get('routed_oos_trades_per_day'))}`, "
        f"PF(수익 팩터) `{fmt(best.get('routed_validation_pf'))}` / `{fmt(best.get('routed_oos_pf'))}`, "
        f"net(순손익) `{fmt(best.get('routed_validation_net'))}` / `{fmt(best.get('routed_oos_net'))}`이며 selected_research_baseline(선택 연구 기준선)은 `none`이다. "
        f"Effect(효과): `{best.get('failure_reasons', '')}` 때문에 hard condition(강한 완료 조건)을 통과하지 못해 Stage56(56단계)을 계속 open(열림)으로 둔다."
    )
    run50ax_focus_pattern = (
        r"(?m)^- Stage56\(56단계\) `"
        + re.escape(STAGE_ID)
        + r"`: run50AY\(실행50AY\) agreement firewall density recovery\(합의 방화벽 밀도 회복\) 완료; .*\n"
    )
    text = re.sub(run50ax_focus_pattern, "", text)
    text = re.sub(r"current_focus:\n", f"current_focus:\n{focus}\n", text, count=1)
    block = (
        "\nstage56_run50ay_agreement_firewall_density_recovery:\n"
        f"  packet_id: {PACKET_ID}\n"
        f"  current_run_id: {PARENT_RUN_ID}\n"
        f"  best_variant: {best.get('variant_id', 'none')}\n"
        "  selected_research_baseline: none\n"
        f"  failure_reasons: {best.get('failure_reasons', '')}\n"
        "  boundary: research_baseline_selection_only_no_operating_claim\n"
        "  next_action: continue_agreement_firewall_or_open_new_model_branch\n"
    )
    if "stage56_run50ay_agreement_firewall_density_recovery:" in text:
        text = re.sub(r"\nstage56_run50ay_agreement_firewall_density_recovery:\n(?:  .*\n?)*\Z", block, text.rstrip(), flags=re.M)
    else:
        text = text.rstrip() + "\n" + block
    path.write_text(text.rstrip() + "\n", encoding="utf-8-sig")


def write_run_files(
    result: Mapping[str, Any],
    variants: Sequence[CompositeVariant],
    summary_rows: Sequence[Mapping[str, Any]],
    audit_rows: Sequence[Mapping[str, Any]],
    source_summary_rows_payload: Sequence[Mapping[str, Any]],
    source_lineage: Sequence[Mapping[str, Any]],
    context_manifest: Mapping[str, Any],
    ledger_payload: Mapping[str, Any],
) -> None:
    write_csv(RESULTS_CSV_PATH, summary_rows)
    write_csv(AUDIT_CSV_PATH, audit_rows, aw.reopen.AUDIT_COLUMNS)
    write_csv(SOURCE_SUMMARY_CSV_PATH, source_summary_rows_payload)
    write_json(RUN_ROOT / "run_manifest.json", {"run_id": PARENT_RUN_ID, "stage_id": STAGE_ID, "run_number": RUN_NUMBER, "packet_id": PACKET_ID, "variants": [variant_payload(variant) for variant in variants], "attempts": result.get("attempts", []), "common_copies": result.get("common_copies", []), "compile": result.get("compile", {}), "external_verification_status": result.get("external_verification_status"), "judgment": JUDGMENT, "boundary": BOUNDARY})
    write_json(RUN_ROOT / "kpi_record.json", {"run_id": PARENT_RUN_ID, "stage_id": STAGE_ID, "packet_id": PACKET_ID, "mt5_kpi_records": result.get("mt5_kpi_records", []), "strategy_tester_reports": result.get("strategy_tester_reports", []), "execution_results": result.get("execution_results", []), "external_verification_status": result.get("external_verification_status"), "judgment": JUDGMENT, "boundary": BOUNDARY})
    write_json(RUN_ROOT / "source_context_manifest.json", context_manifest)
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
    parser = argparse.ArgumentParser(description="Run Stage56 agreement firewall density recovery branch.")
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
    args = parse_args(argv)
    variants = selected_variants(args)
    common, route_coverage, _ = aw.build_common_table()
    frames, source_summary, context_manifest, lineage = build_variant_frames(variants, common)
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
        "model_artifacts": {"stage56_agreement_firewall": model_artifact},
        "common_copies": common_copies,
        "route_coverage": route_coverage,
        "source_lineage": lineage,
        "python_candidate_summary": source_summary,
        "model_family": "agreement_firewall_discrete_signal_score_table",
        "feature_set_id": "stage56_agreement_firewall_event_signal",
        "label_id": "label_v1_fwd12_m5_logret_train_q33_3class",
        "split_contract": "split_v1_calendar_train_20220901_20241231_val_20250101_20250930_oos_20251001_20260413",
        "claim_boundary": BOUNDARY,
    }
    result = execute_or_materialize(prepared, args)
    audit_rows = audit_rows_for_result(result, variants, float(args.cost_stress_per_trade)) if result.get("mt5_kpi_records") else []
    summary_rows = build_summary_rows(variants, result.get("mt5_kpi_records", []), audit_rows)
    write_report(summary_rows, audit_rows, result)
    extra_paths = [REPORT_PATH, RESULTS_CSV_PATH, AUDIT_CSV_PATH, SOURCE_SUMMARY_CSV_PATH, RUN_ROOT / "run_manifest.json", RUN_ROOT / "kpi_record.json", RUN_ROOT / "source_context_manifest.json", RUN_ROOT / "source_lineage.json", AGGREGATE_SUMMARY_PATH]
    artifacts = artifact_rows(result, variants, lineage, extra_paths)
    ledger_payload = write_ledgers(result, variants, artifacts)
    write_run_files(result, variants, summary_rows, audit_rows, source_summary, lineage, context_manifest, ledger_payload)
    artifacts = artifact_rows(result, variants, lineage, extra_paths)
    ledger_payload = write_ledgers(result, variants, artifacts)
    write_json(AGGREGATE_SUMMARY_PATH, {**aw.read_json(AGGREGATE_SUMMARY_PATH), "ledger_payload": ledger_payload})
    aggregate_artifact = [
        row
        for row in artifact_rows(result, variants, lineage, [AGGREGATE_SUMMARY_PATH])
        if row.get("artifact_id") == f"stage56_{RUN_NUMBER}_{aw.safe_name(AGGREGATE_SUMMARY_PATH.stem, 80)}"
    ]
    if aggregate_artifact:
        upsert_csv_rows(ARTIFACT_REGISTRY_PATH, aw.ARTIFACT_COLUMNS, aggregate_artifact, key="artifact_id")
    if summary_rows:
        update_current_truth(summary_rows)
    print(json.dumps(json_ready({"status": "ok", "run_id": PARENT_RUN_ID, "selected_research_baseline": "none", "stage56_remains_open": True, "external_verification_status": result.get("external_verification_status"), "summary_csv": RESULTS_CSV_PATH.as_posix(), "audit_csv": AUDIT_CSV_PATH.as_posix(), "aggregate_summary": AGGREGATE_SUMMARY_PATH.as_posix(), "best_variant": best_row(summary_rows)}), ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
